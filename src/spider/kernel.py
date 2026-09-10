from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from .models import Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry


_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

# Paths considered metadata (not part of the action template)
ACTION_TEMPLATE_PATHS: list[str] = ["method", "url", "body", "headers"]
METADATA_KEYS: set[str] = {
    "timestamp", "request_duration_ms", "retry_count", "user_agent",
    "response_time_ms", "cache_hit", "result_count",
}


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


# ─── Helper functions for parameter induction ────────────────────────────────


def _collect_leaf_paths(obj: Any, prefix: str = "") -> list[str]:
    """Enumerate dotted leaf paths in a nested dict/list structure."""
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
    """Check if a dotted path refers to metadata (not action content)."""
    top = path.split(".")[0].split("[")[0]
    return top in METADATA_KEYS


def _get_value_at_path(obj: Any, path: str) -> Any:
    """Extract value at a dotted path in a nested structure."""
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
    """Set value at a dotted path in a nested structure, returning new structure."""
    import copy
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
    """Compute Jaccard similarity between two sets."""
    if not set1 and not set2:
        return 1.0
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 0.0


def _check_constant_value_anchor(path_values: dict[str, dict]) -> tuple[bool, str | None]:
    """Check if any path has a constant value across all observations."""
    for path, info in path_values.items():
        values = info["values"]
        if len(set(str(v) for v in values)) == 1:
            return True, path
    return False, None


def _find_common_prefix_suffix(values: list[str]) -> tuple[str, str]:
    """Compute common prefix and suffix of a list of strings."""
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
        while not v.endswith(suffix):
            suffix = suffix[1:]
            if not suffix:
                break
    return prefix, suffix


def _extract_parameter_candidates(
    action: dict[str, Any], template_paths: list[str]
) -> list[str]:
    """Identify paths that are candidates for parameterization."""
    candidates = []
    for path in template_paths:
        if _is_metadata_path(path):
            continue
        candidates.append(path)
    return candidates


def _compute_structure_similarity(observations: list[Observation]) -> float:
    """Compute pairwise Jaccard similarity of leaf paths across observations."""
    all_paths = [_collect_leaf_paths(obs.action) for obs in observations]
    path_sets = [set(p) for p in all_paths]
    if len(path_sets) < 2:
        return 1.0
    sims = []
    for i in range(len(path_sets)):
        for j in range(i + 1, len(path_sets)):
            sims.append(_compute_jaccard(path_sets[i], path_sets[j]))
    return sum(sims) / len(sims) if sims else 0.0


def _field_path_to_slot_name(path: str) -> str:
    """Convert a dotted path to a slot name (last component, sanitized)."""
    parts = path.replace("[", ".").replace("]", "").split(".")
    last = parts[-1] if parts else path
    return re.sub(r"[^a-zA-Z0-9_]", "_", last)


def _bind(value: Any, params: dict[str, Any], prefixes: dict[str, str] | None = None) -> Any:
    """Bind parameter values into a template, with optional prefix stripping.

    When prefixes is provided and a slot has a prefix:
    - If the param value starts with the prefix: strip prefix, then substitute
      (avoids double-prefix: 'site-d' -> 'd' -> 'site-d' via template prefix)
    - If the param value does NOT start with prefix: substitute directly
      (template prefix is added: 'd' -> 'site-d')
    """
    if prefixes is None:
        prefixes = {}

    if isinstance(value, str):
        full = _PARAMETER.fullmatch(value)
        if full:
            slot = full.group(1)
            raw_param = params.get(slot, "")
            if slot in prefixes and isinstance(raw_param, str) and raw_param.startswith(prefixes[slot]):
                return raw_param[len(prefixes[slot]):]
            return str(raw_param)

        def replace(match: re.Match[str]) -> str:
            slot = match.group(1)
            raw_param = params.get(slot, "")
            if slot in prefixes and isinstance(raw_param, str) and raw_param.startswith(prefixes[slot]):
                return str(raw_param[len(prefixes[slot]):])
            return str(raw_param)

        return _PARAMETER.sub(replace, value)
    if isinstance(value, dict):
        return {k: _bind(v, params, prefixes) for k, v in value.items()}
    if isinstance(value, list):
        return [_bind(v, params, prefixes) for v in value]
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
            bound_action=_bind(best.action_template, params, prefixes=getattr(best, 'slot_prefixes', None) or {}),
            confidence=best.confidence,
        )

    def distill_parameterized(
        self,
        observations: list[Observation],
        mechanism_id: str = "param-auto",
    ) -> tuple[Mechanism, dict[str, Any]] | None:
        """Distill a parameterized mechanism from multiple observations.

        Bind-time slot-level prefix extraction:
        - Template retains the FULL prefix (no distill-time stripping)
        - slot_prefixes stores the slot-level prefix for each parameter slot
        - _bind() checks at bind time whether to strip prefix (avoids double-prefix)

        Returns (mechanism, diagnostics) or None if insufficient data.
        """
        if not observations or len(observations) < 2:
            return None

        # Filter to successful observations with the same intent
        successful = [o for o in observations if o.success]
        if len(successful) < 2:
            return None

        intent = successful[0].intent
        # Only keep observations with the same intent (prevents parameterizing unrelated observations)
        same_intent = [o for o in successful if o.intent == intent]
        if len(same_intent) < 2:
            return None
        successful = same_intent

        # Collect leaf paths from each observation's action
        all_paths_per_obs = [_collect_leaf_paths(obs.action) for obs in successful]

        # Find common paths (present in ALL observations)
        path_sets = [set(p) for p in all_paths_per_obs]
        common_paths = path_sets[0]
        for ps in path_sets[1:]:
            common_paths = common_paths & ps

        # Compute structural similarity
        mean_jaccard = _compute_structure_similarity(successful)

        # For each common path, collect values across observations
        path_values: dict[str, dict[str, Any]] = {}
        for path in sorted(common_paths):
            values = []
            for obs in successful:
                v = _get_value_at_path(obs.action, path)
                values.append(v)
            # Compute prefix/suffix for string values
            str_values = [str(v) for v in values]
            prefix, suffix = _find_common_prefix_suffix(str_values)
            path_values[path] = {
                "values": values,
                "prefix": prefix,
                "suffix": suffix,
            }

        # Check for constant anchor
        has_constant_anchor, anchor_path = _check_constant_value_anchor(path_values)

        # Identify varying paths (non-constant, non-metadata)
        varying_paths = []
        for path, info in path_values.items():
            if _is_metadata_path(path):
                continue
            unique_vals = set(str(v) for v in info["values"])
            if len(unique_vals) > 1:
                varying_paths.append(path)

        if not varying_paths:
            # No varying fields — cannot parameterize
            return None

        # Shared paths (present in common but not necessarily varying)
        shared_paths = sorted(common_paths)

        # Compute slot prefixes from training values for each varying path
        # The slot-level prefix is the part of the common prefix that comes AFTER
        # the URL/structural prefix (i.e., after the last '/' before the varying part).
        # This avoids double-prefix at bind-time: template has URL prefix + slot prefix,
        # and _bind() strips slot prefix if value already contains it.
        slot_prefixes: dict[str, str] = {}
        for vpath in varying_paths:
            info = path_values[vpath]
            values = [str(v) for v in info["values"]]
            # The slot-level prefix: longest common prefix of the values,
            # but only the part after the last '/' in the common prefix
            full_prefix, _ = _find_common_prefix_suffix(values)
            # Find last '/' in the full prefix to separate URL prefix from slot prefix
            last_slash = full_prefix.rfind('/')
            if last_slash >= 0:
                slot_prefix = full_prefix[last_slash + 1:]
            else:
                slot_prefix = full_prefix
            slot_name = _field_path_to_slot_name(vpath)
            slot_prefixes[slot_name] = slot_prefix

        # Build the action template: replace varying leaf values with ${slot_name}
        # The template RETAINS the full prefix (no distill-time stripping).
        # This preserves the VALUE CONTRACT: callers can pass short or full values.
        # - Short values: template prefix provides the prefix automatically
        # - Full values: _bind() strips the slot prefix to avoid double-prefix
        template = dict(successful[0].action)
        parameter_slots = []
        for vpath in varying_paths:
            slot_name = _field_path_to_slot_name(vpath)
            parameter_slots.append(slot_name)
            # Get the common prefix/suffix for this path
            info = path_values[vpath]
            prefix = info["prefix"]
            suffix = info["suffix"]
            # Create template value: prefix + ${slot} + suffix (RETAINS full prefix)
            template_value = f"{prefix}${{{slot_name}}}{suffix}"
            template = _set_template_value(template, vpath, template_value)

        # Create mechanism
        # Note: preconditions are empty for parameterized mechanisms.
        # The state varies per observation and is not part of the action template.
        mechanism = Mechanism(
            mechanism_id=mechanism_id,
            intent=intent,
            preconditions={},
            action_template=template,
            postconditions={},
            parameter_slots=parameter_slots,
            slot_prefixes=slot_prefixes,
            evidence=[self.observe(o)[:16] for o in successful],
            confidence=0.9,
        )

        diagnostics = {
            "mean_jaccard": mean_jaccard,
            "has_constant_anchor": has_constant_anchor,
            "anchor_path": [anchor_path] if anchor_path else [],
            "shared_paths": shared_paths,
            "path_values": path_values,
            "slot_prefixes": slot_prefixes,
        }

        return mechanism, diagnostics

    def verify(self, mechanism_id: str, observed_state: dict[str, Any]) -> bool:
        mechanism = next((m for m in self.registry.all() if m.mechanism_id == mechanism_id), None)
        if mechanism is None or mechanism.invalidated:
            return False
        return _matches(mechanism.postconditions, observed_state)

    def invalidate(self, mechanism_id: str) -> bool:
        return self.registry.invalidate(mechanism_id)
