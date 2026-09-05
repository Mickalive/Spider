from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from .models import Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry


_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


# ═══════════════════════════════════════════════════════════════════════════════
# Multi-Parameter Induction Engine (ported from EXP-PRODUCT-33741671686)
# ═══════════════════════════════════════════════════════════════════════════════

def _deep_get(obj: Any, path: tuple) -> Any:
    """Get a nested value by path tuple. E.g., _deep_get(d, ('body', 'name'))."""
    current = obj
    for key in path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current


def _deep_set(obj: dict, path: tuple, value: Any) -> None:
    """Set a nested value by path tuple."""
    current = obj
    for key in path[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[path[-1]] = value


def _collect_leaf_paths(obj: Any, prefix: tuple = ()) -> list[tuple]:
    """Collect all leaf paths in a nested dict/list structure."""
    paths = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            paths.extend(_collect_leaf_paths(v, prefix + (k,)))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            paths.extend(_collect_leaf_paths(item, prefix + (str(i),)))
    else:
        paths.append(prefix)
    return paths


def _common_prefix_and_suffix(values: list[str]) -> tuple[str, str, list[str]]:
    """Find common prefix and suffix across a list of string values.
    Returns (prefix, suffix, varying_middle_values).
    """
    if len(values) < 2:
        return ("", "", values)

    # Find common prefix
    prefix = values[0]
    for v in values[1:]:
        while not v.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                break

    # Find common suffix (on the full strings, not after prefix removal)
    suffix = values[0]
    for v in values[1:]:
        while not v.endswith(suffix):
            suffix = suffix[1:]
            if not suffix:
                break

    # Varying middle values: strip prefix and suffix from each value
    middles = []
    for v in values:
        mid = v[len(prefix):]
        if suffix and mid.endswith(suffix):
            mid = mid[:-len(suffix)]
        middles.append(mid)

    return (prefix, suffix, middles)


def _is_varying_field(field_values: list[Any]) -> bool:
    """Check if a field genuinely varies across observations."""
    if len(field_values) < 2:
        return False
    str_values = [json.dumps(v, sort_keys=True) for v in field_values]
    return len(set(str_values)) > 1


def _field_path_to_slot_name(field_path: tuple, values: list[str]) -> str:
    """Generate a descriptive slot name from field path and observed values."""
    last_seg = str(field_path[-1]).lower()
    name = re.sub(r'[^a-z0-9_]', '_', last_seg)
    name = re.sub(r'_+', '_', name).strip('_')
    if not name:
        name = "param"
    return name


def _extract_varying_values_multi(observations: list[Observation]) -> dict:
    """Extract varying fields across observations with distinct slot naming.

    Returns dict: {
        'slots': {slot_name: {'field_path': tuple, 'prefix': str, 'suffix': str, 'values': list}},
        'template': dict (action template with ${slot} placeholders),
        'slot_count': int,
    }
    """
    if len(observations) < 2:
        return {'slots': {}, 'template': {}, 'slot_count': 0}

    # Collect all leaf paths from the first observation's action
    all_paths = set()
    for obs in observations:
        all_paths.update(_collect_leaf_paths(obs.action))

    # Check each path for variation across observations
    varying_fields = {}
    for path in all_paths:
        values = [_deep_get(obs.action, path) for obs in observations]
        if _is_varying_field(values):
            str_values = [str(v) for v in values if v is not None]
            if str_values and all(isinstance(v, str) for v in values if v is not None):
                varying_fields[path] = str_values
            elif str_values:
                varying_fields[path] = [json.dumps(v) for v in values if v is not None]

    if not varying_fields:
        return {'slots': {}, 'template': {}, 'slot_count': 0}

    # Create distinct slot names for each varying field
    slots = {}
    used_names = set()

    for field_path, values in varying_fields.items():
        base_name = _field_path_to_slot_name(field_path, values)
        name = base_name
        counter = 1
        while name in used_names:
            name = f"{base_name}_{counter}"
            counter += 1
        used_names.add(name)

        prefix, suffix, middles = _common_prefix_and_suffix(values)

        slots[name] = {
            'field_path': field_path,
            'prefix': prefix,
            'suffix': suffix,
            'values': middles,
            'raw_values': values,
        }

    # Build template with ${slot} placeholders
    template = json.loads(json.dumps(observations[0].action))

    for slot_name, slot_info in slots.items():
        field_path = slot_info['field_path']
        prefix = slot_info['prefix']
        suffix = slot_info['suffix']

        if prefix or suffix:
            template_val = f"{prefix}${{{slot_name}}}{suffix}"
        else:
            template_val = f"${{{slot_name}}}"

        _deep_set(template, field_path, template_val)

    return {
        'slots': slots,
        'template': template,
        'slot_count': len(slots),
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

    def distill_parameterized(
        self,
        observations: list[Observation],
        mechanism_id: str = "param-multi",
        intent: str | None = None,
    ) -> Mechanism | None:
        """Multi-parameter induction: extract multiple distinct parameter slots.

        This extends single-parameter distill() to handle multiple varying fields
        with distinct slot naming, prefix/suffix extraction, and template generation.
        """
        if not observations:
            return None

        successful = [obs for obs in observations if obs.success]
        if not successful:
            return None

        result = _extract_varying_values_multi(successful)

        if result['slot_count'] == 0:
            return None

        obs_intent = intent or successful[0].intent

        # Merge preconditions from all observations (first observation)
        preconditions = dict(successful[0].state)

        # Postconditions from last observation
        postconditions = dict(successful[-1].next_state)

        # Build evidence list
        evidence = [hashlib.sha256(json.dumps(obs.action, sort_keys=True).encode()).hexdigest()[:16]
                    for obs in successful]

        # Confidence: higher when more training observations agree
        confidence = min(0.9, 0.5 + 0.1 * len(successful))

        return Mechanism(
            mechanism_id=mechanism_id,
            intent=obs_intent,
            preconditions=preconditions,
            action_template=result['template'],
            postconditions=postconditions,
            parameter_slots=sorted(result['slots'].keys()),
            evidence=evidence,
            confidence=confidence,
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
