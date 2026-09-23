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


def _is_relevant_path(path: str) -> bool:
    lower = path.lower()
    return any(kw in lower for kw in ["body", "headers", "url"])


def _flatten_step(step: dict, prefix: str = "") -> dict[str, str]:
    result = {}
    for k, v in step.items():
        path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            result.update(_flatten_step(v, path))
        elif isinstance(v, str):
            result[path] = v
    return result


def _replace_values_with_slots(step: dict, slot_fields: set[str], prefix: str = "") -> dict:
    """Replace actual values with ${slot} placeholders for fields in slot_fields."""
    result = {}
    for k, v in step.items():
        path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            result[k] = _replace_values_with_slots(v, slot_fields, path)
        elif isinstance(v, str) and path in slot_fields:
            result[k] = f"${{{path}}}"
        else:
            result[k] = v
    return result


class SpiderKernel:
    """Conservative first execution-inheritance kernel.

    This kernel is deliberately not a browser agent. It stores and resolves validated mechanisms.
    It abstains when applicability is not demonstrated.
    """

    def __init__(self, registry: MechanismRegistry, min_confidence: float = 0.8, freshness_threshold: float = 0.25):
        self.registry = registry
        self.min_confidence = min_confidence
        self.freshness_threshold = freshness_threshold

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

    def distill_parameterized(self, observations: list[Observation], intent: str, family_id: str) -> Mechanism | None:
        """Induce one parameterized mechanism per family from curated demonstrations."""
        if not observations or not all(o.success for o in observations):
            return None

        # Collect all steps from all observations
        all_steps = []
        for obs in observations:
            steps = obs.action.get("steps", [])
            all_steps.extend(steps)
        if not all_steps:
            return None

        # Collect field-path values across observations
        field_values: dict[str, list[str]] = {}
        for step in all_steps:
            flat = _flatten_step(step)
            for path, val in flat.items():
                if _is_relevant_path(path):
                    field_values.setdefault(path, []).append(val)

        # Create parameter slots for field-paths with varying values
        parameter_slots: list[str] = []
        evidence_values: dict[str, list[str]] = {}
        for field, vals in field_values.items():
            unique_vals = list(set(vals))
            if len(unique_vals) >= 2:
                slot_name = f"${{{field}}}"
                parameter_slots.append(slot_name)
                evidence_values[slot_name] = unique_vals

        if not parameter_slots:
            return None

        # Build action_template with placeholders
        first_steps = observations[0].action.get("steps", [])
        slot_fields = {s.strip("${}").strip() for s in parameter_slots}
        action_template = {"steps": [_replace_values_with_slots(dict(s), slot_fields) for s in first_steps]}
        preconditions = dict(observations[0].state)
        postconditions = dict(observations[0].next_state)
        consistency = len(set(json.dumps(a, sort_keys=True) for a in [o.action for o in observations])) / len(observations)
        confidence = round(0.5 + consistency * 0.4, 2)
        oid = hashlib.sha256(json.dumps([str(o) for o in observations], sort_keys=True).encode()).hexdigest()[:16]

        return Mechanism(
            mechanism_id=f"param-{family_id}",
            intent=intent,
            preconditions=preconditions,
            action_template=action_template,
            postconditions=postconditions,
            parameter_slots=parameter_slots,
            evidence_values=evidence_values,
            confidence=confidence,
            applicability_guards={"family": family_id},
            verification_rule={"postconditions": postconditions},
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
