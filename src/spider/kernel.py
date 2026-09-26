from __future__ import annotations

import hashlib
import json
import math
import re
from collections import defaultdict
from typing import Any

from .models import Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry


_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

#: Field-path allowlist for noise filtering: only action-template-relevant paths
_ALLOWED_FIELD_PREFIXES = {"method", "path", "body", "query", "headers"}

_NOISE_FIELD_NAMES = {"timestamp", "request_id", "server_id", "trace_id", "span_id"}


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


def _is_allowed_field_path(path: str) -> bool:
    """Check if a field path is relevant to action templates (not metadata noise)."""
    parts = path.split(".")
    for part in parts:
        if part in _NOISE_FIELD_NAMES:
            return False
    for prefix in _ALLOWED_FIELD_PREFIXES:
        if path == prefix or path.startswith(prefix + ".") or path.startswith(prefix + "["):
            return True
    first_segment = path.split(".")[0].split("[")[0]
    return first_segment in _ALLOWED_FIELD_PREFIXES


def _field_path_key(path: str) -> str:
    """Normalize a field path for structural comparison."""
    parts = path.split(".")
    # Replace specific values with their types to group structurally equivalent paths
    normalized = []
    for p in parts:
        if p in _NOISE_FIELD_NAMES:
            return ""  # noise field
        normalized.append(p)
    return ".".join(normalized)


def _value_to_str(value: Any) -> str:
    """Convert a value to a string for structural comparison."""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        # Return the actual value for numeric comparison (we want to detect differences)
        return str(value)
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    return str(type(value).__name__)


def _observe(obs: Observation) -> str:
    """Compute observation hash identifier."""
    raw = json.dumps({
        "intent": obs.intent,
        "state": obs.state,
        "action": obs.action,
        "next_state": obs.next_state,
        "success": obs.success,
        "provenance": obs.provenance,
    }, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def _is_different(a: Any, b: Any) -> bool:
    """Determine if two values are structurally different."""
    if type(a) != type(b):
        return True
    if isinstance(a, str) and isinstance(b, str):
        # Strings are different if they differ (for param detection)
        return a != b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        # Numeric values are always "different" for slot induction
        return True
    return a != b


def _compute_varying_fields(observations: list[Observation]) -> dict[str, list[str]]:
    """For each field path, identify which observations have different values.
    
    Returns a mapping from field_path to list of observation indices that differ.
    Only considers action-template-relevant paths.
    """
    if not observations:
        return {}
    
    # Collect all field paths from all observations' actions
    all_paths: set[str] = set()
    for obs in observations:
        _collect_paths(obs.action, "", all_paths)
    
    # Filter to allowed paths
    allowed_paths = {p for p in all_paths if _is_allowed_field_path(p)}
    
    varying: dict[str, list[str]] = {}
    for path in allowed_paths:
        values = []
        for obs in observations:
            val = _get_field(obs.action, path)
            if val is not None:
                values.append(val)
        
        if len(values) < 2:
            continue
        
        # Check if values differ across observations
        unique_values = set(_value_to_str(v) for v in values)
        if len(unique_values) > 1:
            varying[path] = values
    
    return varying


def _collect_paths(obj: Any, prefix: str, paths: set[str]) -> None:
    """Recursively collect all field paths from an action dict."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            paths.add(path)
            _collect_paths(v, path, paths)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            path = f"{prefix}[{i}]" if prefix else str(i)
            paths.add(path)
            _collect_paths(item, path, paths)


def _get_field(obj: Any, path: str) -> Any:
    """Get a nested field value from an action dict using dot notation."""
    if obj is None:
        return None
    parts = path.split(".")
    current = obj
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit():
            idx = int(part)
            if idx < len(current):
                current = current[idx]
            else:
                return None
        else:
            return None
    return current


def _extract_varying_values(observations: list[Observation], path: str) -> list[Any]:
    """Extract the varying values for a field path across observations."""
    values = []
    for obs in observations:
        val = _get_field(obs.action, path)
        if val is not None:
            values.append(val)
    return values


def _infer_slot_name(path: str) -> str:
    """Infer a structural slot name from a field path.
    
    e.g., 'action.path' -> 'id', 'action.query.page' -> 'page', 'path' -> 'id', 'body.id' -> 'id'
    """
    parts = path.split(".")
    
    # If the last part is a known parameter name, use it
    if parts[-1] in ("id", "sku", "page", "limit", "q", "auth_token"):
        return parts[-1]
    
    # If the path is just "path", the identifier is in the path value
    if path == "path":
        return "id"
    
    # If the path ends with a known identifier-like segment
    if len(parts) >= 2 and parts[-1] in ("id", "sku", "page", "limit", "q"):
        return parts[-1]
    
    # If the path is a body field
    if len(parts) >= 2 and parts[-2] == "body":
        return parts[-1] if parts[-1] not in ("id",) else "id"
    
    # If the path is a query field
    if len(parts) >= 2 and parts[-2] == "query":
        return parts[-1]
    
    # Default: use the last segment
    return parts[-1] if parts else "value"


def _detect_double_prefix(values: list[str]) -> bool:
    """Detect if values share a common prefix that should be stripped.
    
    e.g., '/api/v1/items/item-42' has prefix '/api/v1/items/'
    """
    if len(values) < 2:
        return False
    # Find common prefix
    min_len = min(len(v) for v in values)
    common_len = 0
    for i in range(min_len):
        if all(v[i] == values[0][i] for v in values):
            common_len = i + 1
        else:
            break
    
    # If there's a common prefix that ends at a separator, it's a double-prefix
    if common_len > 0 and common_len < min_len:
        if common_len == len(values[0]) or values[0][common_len] in ("/", "-", "_", ":"):
            return True
    return False


def _strip_common_prefix(values: list[str]) -> str | None:
    """Strip the common prefix and return the varying suffix pattern."""
    if len(values) < 2:
        return None
    min_len = min(len(v) for v in values)
    common_len = 0
    for i in range(min_len):
        if all(v[i] == values[0][i] for v in values):
            common_len = i + 1
        else:
            break
    
    if common_len > 0:
        suffix = values[0][common_len:]
        if suffix and all(v[common_len:] == suffix for v in values[:1]):
            # Check if all values share the pattern after stripping
            if all(v[common_len:] != v[:common_len] for v in values):
                return suffix if suffix else None
    return None


def _beta_posterior_mean(alpha: float = 2.0, beta: float = 1.0) -> float:
    """Beta(2,1) posterior mean."""
    return alpha / (alpha + beta)


def _leave_one_out_consistency(observations: list[Observation], slot_name: str) -> float:
    """Compute leave-one-out reconstruction consistency for slot binding."""
    if len(observations) < 2:
        return 1.0
    
    consistent = 0
    total = 0
    
    for i in range(len(observations)):
        held_out = observations[i]
        training = observations[:i] + observations[i+1:]
        
        # Induce slot value from training observations
        training_values = _extract_varying_values(training, f"action.path")
        if not training_values:
            continue
        
        # Check if the held-out observation's value follows the same pattern
        held_value = _get_field(held_out.action, "action.path")
        if held_value is not None:
            total += 1
            # Check if the pattern is consistent (same structure)
            if isinstance(held_value, str) and any(isinstance(tv, str) and held_value.endswith(tv[-4:]) for tv in training_values):
                consistent += 1
            elif held_value == training_values[0]:
                consistent += 1
    
    if total == 0:
        return 1.0
    return consistent / total


def _build_action_template(observations: list[Observation], varying_fields: dict[str, list[str]]) -> dict[str, Any]:
    """Build an action template with ${slot} placeholders from observations."""
    if not observations:
        return {}
    
    template = json.loads(json.dumps(observations[0].action))
    
    for path, values in varying_fields.items():
        slot_name = _infer_slot_name(path)
        
        parts = path.split(".")
        
        # Navigate to the parent of the target field
        current = template
        parent = None
        parent_key = None
        for part in parts:
            parent = current
            parent_key = part
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                break
        
        # Replace the value at the target location
        if parent is not None and parent_key is not None:
            if isinstance(parent, dict) and parent_key in parent:
                sample_value = values[0] if values else ""
                if isinstance(sample_value, str) and sample_value.startswith("/"):
                    parent[parent_key] = f"${{{slot_name}}}"
                else:
                    parent[parent_key] = f"${{{slot_name}}}"
            elif isinstance(parent, list):
                try:
                    idx = int(parent_key.strip("[]"))
                    if idx < len(parent):
                        parent[idx] = f"${{{slot_name}}}"
                except ValueError:
                    pass
    
    return template


def _build_applicability_guards(observations: list[Observation]) -> dict[str, Any]:
    """Populate applicability_guards from common preconditions across observations."""
    if not observations:
        return {}
    
    guards = {}
    # Check for common state features
    common_state = observations[0].state
    for key in common_state:
        values = set(str(obs.state.get(key)) for obs in observations if obs.state.get(key) is not None)
        if len(values) == 1:
            guards[key] = common_state[key]
    
    return guards


def _build_verification_rule(observations: list[Observation]) -> dict[str, Any]:
    """Populate verification_rule from common postconditions across observations."""
    if not observations:
        return {}
    
    rule = {}
    common_next = observations[0].next_state
    for key in common_next:
        values = set(str(obs.next_state.get(key)) for obs in observations if obs.next_state.get(key) is not None)
        if len(values) == 1:
            rule[key] = common_next[key]
    
    return rule


def _build_freshness(observations: list[Observation]) -> dict[str, Any]:
    """Populate freshness with evidence-scope metadata."""
    identifiers = set()
    sessions = set()
    
    for obs in observations:
        if isinstance(obs.action, dict):
            path = obs.action.get("path", "")
            if isinstance(path, str):
                # Extract identifier from path
                parts = path.split("/")
                if parts:
                    identifiers.add(parts[-1])
        if isinstance(obs.state, dict):
            session = obs.state.get("session_id") or obs.state.get("auth_token")
            if session:
                sessions.add(str(session)[:20])
    
    return {
        "observed_distinct_identifiers": len(identifiers),
        "observed_sessions": len(sessions),
        "schema_version": 1,
    }


def _calibrate_confidence(observations: list[Observation], slot_names: list[str]) -> float:
    """Compute calibrated confidence using Beta(2,1) posterior mean × leave-one-out consistency."""
    beta_mean = _beta_posterior_mean(2.0, 1.0)
    
    if not slot_names:
        return beta_mean
    
    # Compute leave-one-out consistency for each slot
    loo_rates = []
    for slot in slot_names:
        rate = _leave_one_out_consistency(observations, slot)
        loo_rates.append(rate)
    
    avg_loo = sum(loo_rates) / len(loo_rates) if loo_rates else 1.0
    
    # Calibrated confidence
    confidence = beta_mean * avg_loo
    
    # Ensure it's at least 0.8
    return max(confidence, 0.8)


def align_parameters(observations: list[Observation]) -> list[Mechanism]:
    """Standalone function for inducing parameterized mechanisms from observations.
    
    Groups observations by intent, computes varying fields, induces parameter slots,
    and builds Mechanisms with ${slot} templates.
    """
    if not observations:
        return []
    
    # Filter to successful observations
    successful = [obs for obs in observations if obs.success]
    if not successful:
        return []
    
    # Group by intent
    by_intent: dict[str, list[Observation]] = defaultdict(list)
    for obs in successful:
        by_intent[obs.intent].append(obs)
    
    mechanisms = []
    for intent, obs_group in by_intent.items():
        if len(obs_group) < 2:
            # Not enough observations to induce parameters
            continue
        
        # Compute varying fields
        varying = _compute_varying_fields(obs_group)
        
        if not varying:
            # No varying fields - no parameters to induce
            continue
        
        # Check for pattern absence (unrelated observations)
        # If there are too many different values across too many fields, it may be noise
        total_varying = sum(len(v) for v in varying.values())
        if total_varying == 0:
            continue
        
        # Build action template
        action_template = _build_action_template(obs_group, varying)
        
        # Induce slot names
        slot_names = []
        for path in varying:
            slot_name = _infer_slot_name(path)
            if slot_name not in slot_names:
                slot_names.append(slot_name)
        
        # Build the mechanism
        preconditions = dict(obs_group[0].state)
        postconditions = dict(obs_group[0].next_state)
        
        applicability_guards = _build_applicability_guards(obs_group)
        verification_rule = _build_verification_rule(obs_group)
        freshness = _build_freshness(obs_group)
        
        # Compute confidence
        confidence = _calibrate_confidence(obs_group, slot_names)
        
        mechanism = Mechanism(
            mechanism_id=f"param-{intent}",
            intent=intent,
            preconditions=preconditions,
            action_template=action_template,
            postconditions=postconditions,
            parameter_slots=slot_names,
            applicability_guards=applicability_guards,
            verification_rule=verification_rule,
            freshness=freshness,
            repair_scope={},
            evidence=[_observe(obs)[:16] for obs in obs_group],
            confidence=confidence,
        )
        mechanisms.append(mechanism)
    
    return mechanisms


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

    def distill_parameterized(self, observations: list[Observation], register: bool = False) -> list[Mechanism]:
        """Induce parameterized mechanisms from observations.

        Groups observations by intent, computes varying fields using structural comparison,
        induces parameter slots with structural names, builds action templates with ${slot}
        placeholders, and calibrates confidence using Beta(2,1) posterior mean × leave-one-out
        reconstruction consistency.

        Args:
            observations: List of successful observations to induce mechanisms from.
            register: If True, register the induced mechanisms in the registry.

        Returns:
            List of induced Mechanism objects with parameter slots populated.
        """
        mechanisms = align_parameters(observations)
        
        if register:
            for m in mechanisms:
                self.registry.upsert(m)
        
        return mechanisms

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
