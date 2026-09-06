from __future__ import annotations

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


# ─── Field-path relevance + structure-similarity ──────────────────────────────

# Fields that are part of the action template (included for induction)
ACTION_TEMPLATE_PATHS = {"method", "url", "body", "headers", "query"}

# Top-level keys that are metadata (excluded from induction)
METADATA_KEYS = {
    "timestamp", "request_duration_ms", "retry_count", "user_agent",
    "response_time_ms", "cache_hit", "result_count",
}


def _collect_leaf_paths(d: Any, prefix: str = "") -> list[str]:
    """Collect leaf paths from a nested dict, flattening to dot-separated paths."""
    paths = []
    if isinstance(d, dict):
        for k, v in d.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                paths.extend(_collect_leaf_paths(v, new_prefix))
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    item_prefix = f"{new_prefix}[{i}]"
                    if isinstance(item, dict):
                        paths.extend(_collect_leaf_paths(item, item_prefix))
                    else:
                        paths.append(item_prefix)
            else:
                paths.append(new_prefix)
    return paths


def _is_metadata_path(path: str) -> bool:
    """Check if a path is a metadata field (excluded from induction)."""
    top_key = path.split(".")[0].split("[")[0]
    return top_key in METADATA_KEYS


def _get_value_at_path(d: Any, path: str) -> Any:
    """Get value at a dot-separated path in a nested dict."""
    keys = path.split(".")
    current = d
    for key in keys:
        if "[" in key:
            name, idx = key.split("[")
            idx = int(idx.rstrip("]"))
            current = current.get(name, [None] * (idx + 1))[idx]
        else:
            current = current.get(key) if isinstance(current, dict) else None
        if current is None:
            return None
    return current


def _compute_jaccard(set1: set[str], set2: set[str]) -> float:
    """Compute Jaccard similarity between two sets."""
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 0.0


def _check_constant_value_anchor(actions: list[dict], shared_paths: set[str]) -> tuple[bool, str | None]:
    """Check if at least one shared path has identical values across ALL actions."""
    for path in shared_paths:
        values = [_get_value_at_path(a, path) for a in actions]
        if len(set(str(v) for v in values)) == 1:
            return True, path
    return False, None


def _find_common_prefix_suffix(values: list[str]) -> tuple[str, str]:
    """Find common prefix and suffix among a list of string values."""
    if not values:
        return "", ""

    # Find common prefix
    prefix = ""
    min_len = min(len(v) for v in values)
    for i in range(min_len):
        chars = set(v[i] for v in values)
        if len(chars) == 1:
            prefix += values[0][i]
        else:
            break

    # Find common suffix (after removing prefix from values)
    suffix = ""
    remaining = [v[len(prefix):] for v in values]
    min_rem = min(len(v) for v in remaining)
    for i in range(1, min_rem + 1):
        chars = set(v[-i] for v in remaining)
        if len(chars) == 1:
            suffix = values[0][-i] + suffix
        else:
            break

    return prefix, suffix


def _extract_parameter_candidates(template: dict, observations: list[Observation]) -> dict:
    """
    Extract parameter candidates using field-path relevance.

    Only consider fields within action-template-relevant paths (body, headers, url).
    Exclude top-level metadata (timestamp, request_duration_ms, etc).
    """
    template_paths = set()
    for path in _collect_leaf_paths(template):
        if not _is_metadata_path(path):
            template_paths.add(path)

    # Collect varying values per path across observations
    path_values = {}
    for path in template_paths:
        values = [_get_value_at_path(obs.action, path) for obs in observations]
        if values and all(v is not None for v in values):
            str_values = [str(v) for v in values]
            if len(set(str_values)) > 1:  # Varying values
                prefix, suffix = _find_common_prefix_suffix(str_values)
                path_values[path] = {
                    "values": str_values,
                    "prefix": prefix,
                    "suffix": suffix,
                }

    return path_values


def _compute_structure_similarity(actions: list[dict], path_values: dict) -> tuple[float, bool, list[str]]:
    """
    Two-part structure-similarity check.

    (a) Jaccard >= 0.75 on leaf paths (after metadata exclusion)
    (b) At least one shared path has constant values across all observations

    Note: path_values is a dict of {path: {"values": [...], "prefix": ..., "suffix": ...}}
    We use the shared_paths from _check_constant_value_anchor for the constant-value check.
    """
    # Get all leaf paths from each action (metadata excluded)
    action_path_sets = []
    for action in actions:
        paths = set()
        for p in _collect_leaf_paths(action):
            if not _is_metadata_path(p):
                paths.add(p)
        action_path_sets.append(paths)

    # Compute pairwise Jaccard
    if len(action_path_sets) < 2:
        return 0.0, False, []

    pairwise_jaccards = []
    for i in range(len(action_path_sets)):
        for j in range(i + 1, len(action_path_sets)):
            pairwise_jaccards.append(_compute_jaccard(action_path_sets[i], action_path_sets[j]))
    mean_jaccard = sum(pairwise_jaccards) / len(pairwise_jaccards)

    # Find shared paths across ALL actions
    if action_path_sets:
        shared_paths = action_path_sets[0]
        for ps in action_path_sets[1:]:
            shared_paths = shared_paths & ps
    else:
        shared_paths = set()

    # Check constant-value anchor on shared paths
    has_anchor, anchor_path = _check_constant_value_anchor(actions, shared_paths)

    return mean_jaccard, has_anchor, list(shared_paths)


def _detect_double_prefix(template_url: str, param_value: str) -> tuple[str, str | None]:
    """
    Double-prefix detection for suffix-empty templates.

    When template has prefix but no suffix (e.g., user-${url}), check if param
    starts with prefix. If so, strip prefix and use remainder.
    """
    matches = list(_PARAMETER.finditer(template_url))
    if not matches:
        return param_value, None

    match = matches[0]
    prefix = template_url[:match.start()]
    suffix = template_url[match.end():]
    slot_name = match.group(1)

    # If suffix is empty and param starts with prefix, strip prefix
    if not suffix and param_value.startswith(prefix):
        stripped = param_value[len(prefix):]
        return stripped, slot_name

    return param_value, slot_name


def _set_template_value(d: dict, path: str, new_value: Any) -> None:
    """Set a value at a dot-separated path in a nested dict."""
    keys = path.split(".")
    current = d
    for key in keys[:-1]:
        if "[" in key:
            name, idx = key.split("[")
            idx = int(idx.rstrip("]"))
            current = current.setdefault(name, [None] * (idx + 1))
            current = current[idx]
        else:
            current = current.setdefault(key, {})
    final_key = keys[-1]
    if "[" in final_key:
        name, idx = final_key.split("[")
        idx = int(idx.rstrip("]"))
        if name not in current:
            current[name] = [None] * (idx + 1)
        current[name][idx] = new_value
    else:
        current[final_key] = new_value


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

    def distill_parameterized(
        self,
        observations: list[Observation],
        mechanism_id: str = "param-unknown",
        min_confidence: float = 0.8,
    ) -> tuple[Mechanism, dict] | None:
        """
        Induce a parameterized mechanism from multiple observations using
        field-path relevance noise filter and two-part structure-similarity check.

        Returns (Mechanism, diagnostics_dict) or None if induction fails.
        """
        if len(observations) < 2:
            return None

        # Step 1: Extract parameter candidates using field-path relevance
        first_template = observations[0].action
        path_values = _extract_parameter_candidates(first_template, observations)

        if not path_values:
            return None

        # Step 2: Structure-similarity check
        actions = [obs.action for obs in observations]
        mean_jaccard, has_anchor, shared_paths = _compute_structure_similarity(actions, path_values)

        if mean_jaccard < 0.75 or not has_anchor:
            return None

        # Step 3: Build action template and parameter slots
        action_template = json.loads(json.dumps(first_template))  # Deep copy

        parameter_slots = []
        slot_to_path = {}

        for path, info in sorted(path_values.items()):
            # Determine slot name from path
            slot_name = path.split(".")[-1].split("[")[0]
            if slot_name in parameter_slots:
                slot_name = f"{slot_name}_{len(parameter_slots)}"

            parameter_slots.append(slot_name)
            slot_to_path[slot_name] = path

            # Build template string with prefix/suffix pattern
            prefix = info["prefix"]
            suffix = info["suffix"]
            template_str = f"{prefix}${{{slot_name}}}{suffix}"

            # Set the template value
            _set_template_value(action_template, path, template_str)

        # Step 4: Handle double-prefix in URL template
        if "url" in action_template:
            url_template = action_template["url"]
            # Check if template already has ${slot} pattern
            if not _PARAMETER.search(url_template):
                # No parameter in URL yet - check for double-prefix scenario
                for obs in observations:
                    url_val = obs.action.get("url", "")
                    stripped, detected_slot = _detect_double_prefix(url_template, url_val)
                    if detected_slot:
                        break

        mechanism = Mechanism(
            mechanism_id=mechanism_id,
            intent=observations[0].intent,
            preconditions={},
            action_template=action_template,
            postconditions={},
            parameter_slots=parameter_slots,
            evidence=[],
            confidence=min(0.8, mean_jaccard),
        )

        diagnostics = {
            "path_values": {k: {"values": v["values"], "prefix": v["prefix"], "suffix": v["suffix"]}
                            for k, v in path_values.items()},
            "mean_jaccard": mean_jaccard,
            "has_constant_anchor": has_anchor,
            "anchor_path": [p for p in shared_paths if _check_constant_value_anchor(actions, [p])[0]],
            "shared_paths": shared_paths,
            "parameter_slots": parameter_slots,
            "slot_to_path": slot_to_path,
        }

        return mechanism, diagnostics
