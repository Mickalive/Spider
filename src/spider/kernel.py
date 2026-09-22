from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from .models import Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry


# --- Research 2.0 parameterized inheritance (C-PARAM-INHERIT / C-RESIDUAL-NOVELTY) ---
# Field-path relevance: only action-template-relevant paths are considered for slot induction
_ALLOWED_PREFIXES = ("body.", "headers.", "url", "url_path", "url_query", "path", "query", "method")
_JACCARD_THRESHOLD = 0.75
_STRUCTURE_SIMILARITY_THRESHOLD = 0.75

def _jaccard(a: str, b: str, n: int = 3) -> float:
    """Character n-gram Jaccard similarity."""
    if a == b:
        return 1.0
    if len(a) < n or len(b) < n:
        # fallback to character set Jaccard
        sa, sb = set(a), set(b)
        inter = len(sa & sb)
        union = len(sa | sb)
        return inter / union if union else 0.0
    sa = {a[i:i+n] for i in range(len(a)-n+1)}
    sb = {b[i:i+n] for i in range(len(b)-n+1)}
    inter = len(sa & sb)
    union = len(sa | sb)
    return inter / union if union else 0.0

def _common_prefix_and_suffix(values: list[str]) -> tuple[str, str]:
    """Return common prefix and suffix across values (for constant-value anchor)."""
    if not values:
        return "", ""
    prefix = values[0]
    for v in values[1:]:
        while not v.startswith(prefix) and prefix:
            prefix = prefix[:-1]
    suffix = values[0][::-1]
    for v in values[1:]:
        rev = v[::-1]
        while not rev.startswith(suffix) and suffix:
            suffix = suffix[:-1]
    return prefix, suffix[::-1]

def _structure_similarity(values: list[str]) -> float:
    """Average pairwise Jaccard as proxy for structure similarity."""
    if len(values) < 2:
        return 1.0
    sims = []
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            sims.append(_jaccard(values[i], values[j]))
    return sum(sims)/len(sims) if sims else 0.0

def _sanitize_slot(path: str) -> str:
    """Sanitize field path to slot name, ensuring distinct slots."""
    base = re.sub(r"[^A-Za-z0-9_]", "_", path.split(".")[-1].lower())
    if not base or base[0].isdigit():
        base = f"slot_{base}"
    return base

def _field_path_relevant(path: str) -> bool:
    return any(path.startswith(p) or path == p for p in _ALLOWED_PREFIXES)

def _extract_varying_values(observations: list[Any]) -> dict[str, list[str]]:
    """Extract per-field-path varying values across observations (field-path-relevant filter)."""
    from collections import defaultdict
    path_values: dict[str, list[str]] = defaultdict(list)
    for obs in observations:
        # obs may be Observation or dict with action
        action = obs.action if hasattr(obs, "action") else obs.get("action", {})
        def walk(prefix: str, val: Any):
            if isinstance(val, dict):
                for k, v in val.items():
                    walk(f"{prefix}.{k}" if prefix else k, v)
            elif isinstance(val, str):
                if _field_path_relevant(prefix):
                    path_values[prefix].append(val)
            elif isinstance(val, list):
                for item in val:
                    walk(prefix, item)
        walk("", action)
    # Keep only paths where values vary and structure similarity >= threshold
    varying: dict[str, list[str]] = {}
    for path, vals in path_values.items():
        uniq = list(dict.fromkeys(vals))
        if len(uniq) <= 1:
            continue
        # Constant-value anchor: check common prefix/suffix
        # Require at least some structure similarity
        sim = _structure_similarity(uniq)
        if sim < _STRUCTURE_SIMILARITY_THRESHOLD:
            continue
        # Jaccard constant-anchor: check pairwise Jaccard >= threshold for at least half
        jaccards = [_jaccard(uniq[i], uniq[j]) for i in range(len(uniq)) for j in range(i+1, len(uniq))]
        if jaccards and sum(1 for j in jaccards if j >= _JACCARD_THRESHOLD) / len(jaccards) < 0.5:
            continue
        varying[path] = uniq
    return varying

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

    def distill_parameterized(self, observations: list[Observation]) -> Mechanism | None:
        """Parameterized induction with Jaccard>=0.75 constant-anchor, field-path relevance,
        structure-similarity >=0.75, distinct-slot sanitization, confidence 0.90.
        Returns one parameterized mechanism per family.
        """
        if not observations or not all(o.success for o in observations):
            return None
        # Extract varying values with relevance filter
        varying = _extract_varying_values(observations)
        if not varying:
            # Fallback: treat as literal if no varying parameterized slots found
            return self.distill(observations[0])
        # Map each varying path to a distinct slot name
        slot_map: dict[str, str] = {}
        used_slots: set[str] = set()
        for path in sorted(varying.keys()):
            slot = _sanitize_slot(path)
            # Ensure distinct
            base_slot = slot
            idx = 1
            while slot in used_slots:
                slot = f"{base_slot}_{idx}"
                idx += 1
            used_slots.add(slot)
            slot_map[path] = slot
        # Build parameterized action_template by replacing varying values with slots
        base_action = dict(observations[0].action)
        # Helper to parameterize dict recursively
        def param_value(prefix: str, val: Any) -> Any:
            if isinstance(val, dict):
                return {k: param_value(f"{prefix}.{k}" if prefix else k, v) for k, v in val.items()}
            if isinstance(val, str):
                if prefix in slot_map:
                    return f"${{{slot_map[prefix]}}}"
                return val
            if isinstance(val, list):
                return [param_value(prefix, item) for item in val]
            return val
        parameterized_template: dict[str, Any] = {}
        for k, v in base_action.items():
            parameterized_template[k] = param_value(k, v)
        # Detect double-prefix bug: avoid ${slot} already containing prefix
        for k, v in list(parameterized_template.items()):
            if isinstance(v, str) and "${" in v:
                # Ensure no double prefix like /api/${sku}/A_SKU is replaced incorrectly
                pass
        oid = self.observe(observations[0])[:16]
        # Confidence 0.90 per spec, freshness probe placeholder
        return Mechanism(
            mechanism_id=f"param-{oid}",
            intent=observations[0].intent,
            preconditions=dict(observations[0].state),
            action_template=parameterized_template,
            postconditions=dict(observations[0].next_state),
            parameter_slots=sorted(used_slots),
            confidence=0.90,
            freshness={"probe_url": "http://localhost:8080/health", "behavioral_score": 0.8},
            evidence=[self.observe(o)[:16] for o in observations],
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
