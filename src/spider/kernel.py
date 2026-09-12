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


# ─── Leaf-path helpers for parameterized distillation ─────────────────────

_METADATA_KEYS = {
    "timestamp", "request_duration_ms", "retry_count", "user_agent",
    "response_time_ms", "cache_hit", "result_count",
}


def _collect_leaf_paths(obj: Any, prefix: str = "") -> list[str]:
    """Collect all leaf paths in a nested dict/list structure."""
    paths: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            child = f"{prefix}.{k}" if prefix else k
            if isinstance(v, (dict, list)):
                paths.extend(_collect_leaf_paths(v, child))
            else:
                paths.append(child)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            child = f"{prefix}[{i}]"
            if isinstance(item, (dict, list)):
                paths.extend(_collect_leaf_paths(item, child))
            else:
                paths.append(child)
    return paths


def _is_metadata_path(path: str) -> bool:
    top = path.split(".")[0].split("[")[0]
    return top in _METADATA_KEYS


def _get_value_at_path(obj: Any, path: str) -> Any:
    parts = path.replace("[", ".").replace("]", "").split(".")
    current = obj
    for part in parts:
        if part == "":
            continue
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return current


def _set_template_value(template: Any, path: str, value: Any) -> Any:
    result = copy.deepcopy(template)
    parts = path.replace("[", ".").replace("]", "").split(".")
    current = result
    for part in parts[:-1]:
        if part == "":
            continue
        if isinstance(current, dict):
            current = current[part]
        elif isinstance(current, list):
            current = current[int(part)]
    last = parts[-1]
    if isinstance(current, dict):
        current[last] = value
    elif isinstance(current, list):
        current[int(last)] = value
    return result


def _compute_jaccard(set1: set[str], set2: set[str]) -> float:
    if not set1 and not set2:
        return 1.0
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 0.0


def _compute_structure_similarity(observations: list) -> float:
    path_sets = [_collect_leaf_paths(obs["action"]) for obs in observations]
    if len(path_sets) < 2:
        return 1.0
    similarities = []
    for i in range(len(path_sets)):
        for j in range(i + 1, len(path_sets)):
            similarities.append(_compute_jaccard(set(path_sets[i]), set(path_sets[j])))
    return sum(similarities) / len(similarities) if similarities else 0.0


def _check_constant_value_anchor(path_values: dict) -> tuple[bool, str | None]:
    for path, info in path_values.items():
        values = info["values"]
        if len(set(str(v) for v in values)) == 1:
            return True, path
    return False, None


def _field_path_to_slot_name(path: str) -> str:
    parts = path.split(".")
    return parts[-1]


# ─── Fix1: Suffix Guard ──────────────────────────────────────────────────

def _find_common_prefix_suffix(values: list[str]) -> tuple[str, str]:
    """Common prefix/suffix with Fix1: reject single-char suffixes not preceded
    by structural delimiters (?, =, &)."""
    if not values:
        return "", ""

    # Common prefix
    prefix = values[0]
    for v in values[1:]:
        while not v.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                break

    # Common suffix (raw)
    suffix = values[0]
    for v in values[1:]:
        while not v.endswith(suffix):
            suffix = suffix[1:]
            if not suffix:
                break

    # FIX 1: Suffix Guard — reject single-char suffixes not preceded by
    # structural delimiters (?, =, &)
    if suffix and len(suffix) <= 1:
        pos = len(values[0]) - len(suffix) - 1
        if pos < 0 or values[0][pos] not in ('?', '=', '&'):
            suffix = ''  # Reject non-structural single-char suffix

    return prefix, suffix


# ─── Fix2: Delimiter-Bound Prefix Validation ──────────────────────────────

def _validate_prefix_boundary(full_prefix: str) -> bool:
    """FIX 2: Delimiter-Bound Prefix Validation (last-char variant).
    Require the common prefix to end at a structural boundary: / ? = & or EOS.
    This is the implementation validated in EXP-PRODUCT-34642376433, NOT the
    prereg next-char variant (which would false-reject P1/G1)."""
    if not full_prefix:
        return True  # Empty prefix always valid
    last_char = full_prefix[-1]
    return last_char in ('/', '?', '=', '&')


# ─── Parameterized distillation ───────────────────────────────────────────

def distill_parameterized(kernel_self: Any, observations: list[Observation]) -> Mechanism | None:
    """Parameterized distill for SpiderKernel: leaf-path extraction + Fix1 + Fix2
    + empty-prefix guard. Frozen as specification (not EXPLORATORY)."""
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

    all_paths_per_obs = [_collect_leaf_paths(o.action) for o in successful]
    path_sets = [set(p) for p in all_paths_per_obs]
    common_paths = path_sets[0]
    for ps in path_sets[1:]:
        common_paths = common_paths & ps

    mean_jaccard = _compute_structure_similarity(
        [{"action": o.action} for o in successful]
    )

    path_values = {}
    for path in sorted(common_paths):
        values = []
        for obs in successful:
            v = _get_value_at_path(obs.action, path)
            values.append(v)
        str_values = [str(v) for v in values]
        prefix, suffix = _find_common_prefix_suffix(str_values)  # Fix 1 applied
        path_values[path] = {
            "values": values,
            "prefix": prefix,
            "suffix": suffix,
        }

    has_constant_anchor, anchor_path = _check_constant_value_anchor(path_values)

    varying_paths = []
    for path, info in path_values.items():
        if _is_metadata_path(path):
            continue
        unique_vals = set(str(v) for v in info["values"])
        if len(unique_vals) > 1:
            varying_paths.append(path)

    if not varying_paths:
        return None

    # FIX 2: Delimiter-Bound Prefix Validation
    # Check each varying path: does the full prefix end at a structural boundary?
    # EMPTY-PREFIX GUARD (frozen): reject parameterization when common prefix is empty
    filtered_varying_paths = []
    for vpath in varying_paths:
        info = path_values[vpath]
        values = [str(v) for v in info["values"]]
        full_prefix, _ = _find_common_prefix_suffix(values)
        # Empty prefix means truly disjoint values — no parameterizable shared structure
        if not full_prefix:
            continue
        if _validate_prefix_boundary(full_prefix):
            filtered_varying_paths.append(vpath)
    varying_paths = filtered_varying_paths

    if not varying_paths:
        return None

    # Recompute slot_prefixes for surviving paths
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

    # Build template
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
        mechanism_id=f"obs-{oid}",
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
