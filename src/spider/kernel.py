from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any

from .models import Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry


_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def _matches(required: dict[str, Any], actual: dict[str, Any]) -> bool:
    return all(actual.get(k) == v for k, v in required.items())


def _template_slots(value: Any) -> set[str]:
    if isinstance(value, str):
        return set(_PARAMETER.findall(value))
    if isinstance(value, dict):
        out: set[str] = set()
        for item in value.values():
            out.update(_template_slots(item))
        return out
    if isinstance(value, list):
        out: set[str] = set()
        for item in value:
            out.update(_template_slots(item))
        return out
    return set()


def _bind(value: Any, params: dict[str, Any]) -> Any:
    if isinstance(value, str):
        full = _PARAMETER.fullmatch(value)
        if full:
            return params[full.group(1)]

        def replace(match: re.Match[str]) -> str:
            return str(params[match.group(1)])

        return _PARAMETER.sub(replace, value)
    if isinstance(value, dict):
        return {k: _bind(v, params) for k, v in value.items()}
    if isinstance(value, list):
        return [_bind(v, params) for v in value]
    return value


class SpiderKernel:
    """Conservative first execution-inheritance kernel.

    This kernel is deliberately not a browser agent. It stores and resolves validated mechanisms.
    It abstains when applicability is not demonstrated.
    """

    def __init__(self, registry: MechanismRegistry, min_confidence: float = 0.8):
        self.registry = registry
        self.min_confidence = min_confidence

    def observe(self, observation: Observation) -> str:
        raw = json.dumps({
            "intent": observation.intent,
            "state": observation.state,
            "action": observation.action,
            "next_state": observation.next_state,
            "success": observation.success,
            "provenance": observation.provenance,
        }, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(raw).hexdigest()

    def distill(self, observation: Observation) -> Mechanism | None:
        """Create only a literal candidate mechanism.

        Generalization/parameter induction is intentionally not guessed here; Research 2.0 must
        earn that capability through C-PARAM-INHERIT and related gates.
        """
        if not observation.success:
            return None
        oid = self.observe(observation)[:16]
        return Mechanism(
            mechanism_id=f"obs-{oid}",
            intent=observation.intent,
            preconditions=dict(observation.state),
            action_template=dict(observation.action),
            postconditions=dict(observation.next_state),
            evidence=[oid],
            confidence=0.5,
        )

    def resolve(self, intent: str, context: dict[str, Any], params: dict[str, Any] | None = None) -> Resolution:
        params = params or {}
        candidates = []
        for m in self.registry.all():
            if m.invalidated or m.intent != intent:
                continue
            if not _matches(m.preconditions, context):
                continue
            if not _matches(m.applicability_guards, context):
                continue

            required_slots = set(m.parameter_slots) | _template_slots(m.action_template)
            if any(slot not in params for slot in required_slots):
                continue
            candidates.append(m)

        if not candidates:
            return Resolution(ResolutionStatus.UNKNOWN, None, "no applicable validated mechanism")

        candidates.sort(key=lambda m: m.confidence, reverse=True)
        best = candidates[0]
        if best.confidence < self.min_confidence:
            return Resolution(ResolutionStatus.EXPLORE, best.mechanism_id, "candidate exists but confidence is below execution threshold", confidence=best.confidence)

        return Resolution(
            ResolutionStatus.EXECUTABLE,
            best.mechanism_id,
            "applicability guards and confidence threshold passed",
            bound_action=_bind(best.action_template, params),
            confidence=best.confidence,
        )

    def verify(self, mechanism_id: str, observed_state: dict[str, Any]) -> bool:
        mechanism = next((m for m in self.registry.all() if m.mechanism_id == mechanism_id), None)
        if mechanism is None or mechanism.invalidated:
            return False
        return _matches(mechanism.postconditions, observed_state)

    def invalidate(self, mechanism_id: str) -> bool:
        return self.registry.invalidate(mechanism_id)


# ─── Parameterized distillation helpers (Fix1+Fix2+Fix3) ────────────────

# Paths that carry metadata, not parameterizable content
_METADATA_PATHS = {"method", "headers", "body.timestamp", "body.cache", "headers.authorization", "headers.content-type"}


def _is_metadata_path(path: str) -> bool:
    """Check if a leaf path is metadata (non-parameterizable)."""
    return path in _METADATA_PATHS


def _collect_leaf_paths(d: Any, prefix: str = "") -> list[str]:
    """Collect all leaf paths from a nested dict/list structure."""
    paths = []
    if isinstance(d, dict):
        for k, v in d.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            if isinstance(v, (dict, list)):
                paths.extend(_collect_leaf_paths(v, new_prefix))
            else:
                paths.append(new_prefix)
    elif isinstance(d, list):
        for i, item in enumerate(d):
            new_prefix = f"{prefix}[{i}]"
            if isinstance(item, (dict, list)):
                paths.extend(_collect_leaf_paths(item, new_prefix))
            else:
                paths.append(new_prefix)
    return paths


def _get_value_at_path(d: Any, path: str) -> Any:
    """Get value at a dot-separated path in a nested dict."""
    parts = path.replace("[", ".").replace("]", "").split(".")
    current = d
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def _set_template_value(template: dict, path: str, value: Any) -> dict:
    """Set value at a dot-separated path in a nested dict (returns new dict)."""
    result = copy.deepcopy(template)
    parts = path.replace("[", ".").replace("]", "").split(".")
    current = result
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]
    current[parts[-1]] = value
    return result


def _field_path_to_slot_name(path: str) -> str:
    """Convert a field path to a slot name (last segment, sanitized)."""
    parts = path.replace("[", ".").replace("]", "").split(".")
    name = parts[-1]
    name = re.sub(r'[^A-Za-z0-9_]', '_', name)
    if not name or not name[0].isalpha():
        name = 'slot_' + name
    return name.lower()


def _find_common_prefix_suffix(values: list[str]) -> tuple[str, str]:
    """Find common prefix and suffix across string values.

    Fix1 (suffix guard): single-char suffixes are excluded unless
    preceded by a structural delimiter (?, =, &).
    """
    if not values:
        return "", ""
    prefix = values[0]
    for v in values[1:]:
        while not v.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                break
    suffix = values[0]
    for v in values[1:]:
        while not suffix or not v.endswith(suffix):
            suffix = suffix[1:]
            if not suffix:
                break
    # Fix1: exclude single-char suffixes not preceded by structural delimiters
    if len(suffix) == 1 and suffix:
        pos = values[0].rfind(suffix)
        if pos > 0:
            preceding = values[0][pos - 1]
            if preceding not in ('?', '=', '&'):
                suffix = ""
    return prefix, suffix


def _validate_prefix_boundary(prefix: str) -> bool:
    """Fix2: Validate that prefix ends at a structural delimiter boundary.

    The last character of the prefix must be in /?=& (structural delimiters)
    to ensure the prefix doesn't split mid-token.
    """
    if not prefix:
        return False
    last_char = prefix[-1]
    return last_char in ('/', '?', '=', '&')


def _compute_jaccard(a: set, b: set) -> float:
    """Compute Jaccard similarity between two sets."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _compute_structure_similarity(template1: dict, template2: dict) -> float:
    """Compute structural similarity between two action templates."""
    slots1 = _template_slots(template1)
    slots2 = _template_slots(template2)
    return _compute_jaccard(slots1, slots2)


def _check_constant_value_anchor(values: list[str]) -> bool:
    """Check if there's a constant (non-varying) value anchor across observations."""
    if len(values) < 2:
        return True
    return len(set(values)) == 1


def _is_protocol_only_prefix(prefix: str) -> bool:
    """Fix3: Reject common prefixes that are only scheme+authority without meaningful path content.

    A prefix is 'protocol-only' if it contains only the scheme and authority
    (e.g., 'https://', 'http://', 'https://a.com') with no path segment after the host.
    Prefixes ending with '/' are NOT protocol-only — they have a path delimiter
    indicating parameterizable content follows.
    """
    if not prefix:
        return False
    parts = prefix.split("://", 1)
    if len(parts) != 2:
        return False
    scheme, rest = parts
    if not rest:
        return True
    if "/" not in rest:
        return True
    return False


def distill_parameterized(
    _unused_kernel: Any,
    observations: list,
    mechanism_id: str = "param-auto",
) -> Mechanism | None:
    """Distill parameterized mechanism from multiple observations.

    Uses longest common prefix/suffix heuristic with:
    - Fix1: suffix guard (exclude single-char suffixes not preceded by delimiters)
    - Fix2: delimiter-bound prefix validation (last_char in /?=&)
    - Fix3: protocol-only prefix rejection (minimum meaningful path content)
    - empty-prefix guard (reject when common prefix is empty)

    Returns Mechanism with parameterized template and slot_prefixes, or None on failure.
    """
    if not observations or len(observations) < 2:
        return None

    successful = [o for o in observations if o.success]
    if len(successful) < 2:
        return None

    intent = successful[0].intent
    same_intent = [o for o in successful if o.intent == intent]
    if len(same_intent) < 2:
        return None
    successful = same_intent

    # Collect common leaf paths across all observations
    all_paths_per_obs = [_collect_leaf_paths(o.action) for o in successful]
    path_sets = [set(p) for p in all_paths_per_obs]
    common_paths = path_sets[0]
    for ps in path_sets[1:]:
        common_paths = common_paths & ps

    # For each common path, compute common prefix/suffix of values
    path_values = {}
    for path in sorted(common_paths):
        values = []
        for obs in successful:
            v = _get_value_at_path(obs.action, path)
            values.append(v)
        str_values = [str(v) for v in values]
        prefix, suffix = _find_common_prefix_suffix(str_values)
        path_values[path] = {
            "values": values,
            "prefix": prefix,
            "suffix": suffix,
        }

    # Find varying paths (exclude metadata)
    varying_paths = []
    for path, info in path_values.items():
        if _is_metadata_path(path):
            continue
        unique_vals = set(str(v) for v in info["values"])
        if len(unique_vals) > 1:
            varying_paths.append(path)

    if not varying_paths:
        return None

    # Fix3: Reject protocol-only prefixes
    for vpath in varying_paths:
        info = path_values[vpath]
        full_prefix = info["prefix"]
        if _is_protocol_only_prefix(full_prefix):
            return None

    # Empty-prefix guard: reject when common prefix is empty
    filtered_varying_paths = []
    for vpath in varying_paths:
        info = path_values[vpath]
        if info["prefix"]:
            filtered_varying_paths.append(vpath)
    varying_paths = filtered_varying_paths

    if not varying_paths:
        return None

    # Fix2: Validate prefix boundaries (last_char in /?=&)
    fix2_filtered = []
    for vpath in varying_paths:
        info = path_values[vpath]
        if _validate_prefix_boundary(info["prefix"]):
            fix2_filtered.append(vpath)
    varying_paths = fix2_filtered

    if not varying_paths:
        return None

    # Compute slot_prefixes (metadata-only, does not affect template)
    slot_prefixes = {}
    for vpath in varying_paths:
        info = path_values[vpath]
        values = [str(v) for v in info["values"]]
        full_prefix, _ = _find_common_prefix_suffix(values)
        last_slash = full_prefix.rfind('/')
        if last_slash >= 0:
            slot_prefix = full_prefix[last_slash + 1:]
        else:
            slot_prefix = full_prefix
        slot_name = _field_path_to_slot_name(vpath)
        slot_prefixes[slot_name] = slot_prefix

    # Build parameterized template
    template = dict(successful[0].action)
    parameter_slots = []
    for vpath in varying_paths:
        slot_name = _field_path_to_slot_name(vpath)
        parameter_slots.append(slot_name)
        info = path_values[vpath]
        prefix = info["prefix"]
        suffix = info["suffix"]
        template_value = f"{prefix}${{{slot_name}}}{suffix}"
        template = _set_template_value(template, vpath, template_value)

    oid = hashlib.sha256(
        json.dumps({
            "intent": intent,
            "action": template,
        }, sort_keys=True).encode()
    ).hexdigest()[:16]

    mechanism = Mechanism(
        mechanism_id=f"param-{oid}",
        intent=intent,
        preconditions=dict(successful[0].state) if hasattr(successful[0], 'state') else {},
        action_template=template,
        postconditions=dict(successful[0].next_state) if hasattr(successful[0], 'next_state') else {},
        parameter_slots=parameter_slots,
        evidence=[oid],
        confidence=0.9,
        slot_prefixes=slot_prefixes,
    )
    return mechanism
