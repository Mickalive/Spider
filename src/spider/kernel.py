from __future__ import annotations

import hashlib
import json
import math
import random
import re
from typing import Any

from .models import Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry


_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

# Field paths that may carry parameterized identifiers (frozen prereg sec. 4: "field-path-relevant
# body.*, headers.*, url only"). Top-level metadata (e.g. "method") is never parameterized.
_FIELD_ROOT_RELEVANT = ("url", "headers", "body")
_SOFTMAX_TEMPERATURE = 0.15
_CONFIDENCE_JITTER = 0.05


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


def _iter_field_paths(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    """Flatten a nested action dict into (dotted field path, scalar value) pairs.

    Field paths are the alignment key used for structure similarity and for slot induction
    (frozen: Jaccard>=0.75 constant-anchor structure-similarity>=0.75).
    """
    out: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for k, v in value.items():
            p = f"{prefix}.{k}" if prefix else k
            out.extend(_iter_field_paths(v, p))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            p = f"{prefix}[{i}]"
            out.extend(_iter_field_paths(v, p))
    else:
        out.append((prefix, value))
    return out


def _set_path(target: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    node = target
    for part in parts[:-1]:
        node = node.setdefault(part, {})
    node[parts[-1]] = value


def _lcp_length(a: str, b: str) -> int:
    i = 0
    for x, y in zip(a, b):
        if x != y:
            break
        i += 1
    return i


def _value_similarity(a: str, b: str) -> float:
    """Longest-common-prefix based graded similarity in [0, 1]; 1.0 iff equal.

    Used by the runtime confidence estimator. Identifiers drawn from disjoint pools that share
    no prefix (e.g. "A-SKU-00-0" vs "B-SKU-00-0") score 0.0; exact evidence matches score 1.0.
    """
    if a == b:
        return 1.0
    l = _lcp_length(a, b)
    denom = max(1, len(a) + len(b))
    return (2.0 * l) / denom


def _field_values_by_path(actions: list[dict[str, Any]]) -> dict[str, list[Any]]:
    paths: dict[str, list[Any]] = {}
    for action in actions:
        for path, value in _iter_field_paths(action):
            paths.setdefault(path, []).append(value)
    return paths


def _pairwise_structure_jaccard(actions: list[dict[str, Any]]) -> float:
    """Mean pairwise Jaccard over the field-path sets of the given step actions."""
    path_sets = [set(p for p, _ in _iter_field_paths(a)) for a in actions]
    if len(path_sets) < 2:
        return 1.0
    sims: list[float] = []
    for i in range(len(path_sets)):
        for j in range(i + 1, len(path_sets)):
            inter = len(path_sets[i] & path_sets[j])
            union = len(path_sets[i] | path_sets[j])
            sims.append(inter / union if union else 1.0)
    return sum(sims) / len(sims)


def _extract_varying_values(actions: list[dict[str, Any]]) -> tuple[dict[str, list[str]], dict[str, Any]]:
    """Induce parameter slots + constant anchors from aligned (same step) demo actions.

    Returns (evidence_values, induction_stats):
      evidence_values[slot] = distinct observed values for every field whose value varies
      across demos AND whose field path root is a relevant identifier carrier (url/headers/body).
    Fields whose value is identical across all demos are constant anchors (kept literally).
    """
    evidence_values: dict[str, list[str]] = {}
    field_values = _field_values_by_path(actions)
    template: dict[str, Any] = {}
    n_slots = 0
    for path, values in field_values.items():
        distinct = sorted({v for v in values if isinstance(v, str)})
        if len(distinct) == 1:
            _set_path(template, path, distinct[0])
        else:
            root = path.split(".")[0].split("[")[0]
            slot = path.split(".")[-1].split("[")[0]
            if root in _FIELD_ROOT_RELEVANT:
                evidence_values.setdefault(slot, [])
                for v in distinct:
                    if v not in evidence_values[slot]:
                        evidence_values[slot].append(v)
                _set_path(template, path, "${" + slot + "}")
                n_slots += 1
            else:
                # Non-relevant varying metadata: keep first observed value (should not occur
                # in the census mock; recorded for transparency).
                _set_path(template, path, distinct[0])
    stats = {
        "varying_field_paths": [p for p, vs in field_values.items() if len({v for v in vs if isinstance(v, str)}) > 1],
        "structure_jaccard": _pairwise_structure_jaccard(actions),
        "induced_slots": sorted(evidence_values),
    }
    return evidence_values, stats | {"template": template}


class SpiderKernel:
    """Execution-inheritance kernel with parameterized mechanism induction (product lane).

    SUT behavior frozen in EXP-PRODUCT-35793576245 prereg/spec:
      * `distill_parameterized` induces one family-specific mechanism from <=5 aligned demos
        (Jaccard>=0.75 structure similarity, constant anchors, field-path relevance filter,
        family-specific slots, never a generic ['path','store']).
      * `resolve` gates: preconditions/applicability guards, freshness>=0.25 (behavioral score),
        required slots present, runtime evidence-derived confidence (softmax temp 0.15 + seeded
        uniform jitter [-0.05, 0.05]); confidence < min_confidence (0.80) -> UNKNOWN (abstain).
      * `_bind` resolves ${slot} placeholders; postconditions verified via `verify`.
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
        """Create only a literal candidate mechanism (non-parameterized path)."""
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
        intent: str,
        family_id: str,
        jaccard_threshold: float = 0.75,
        structure_threshold: float = 0.75,
    ) -> Mechanism | None:
        """Induce one parameterized mechanism from aligned per-step demo observations.

        Observations must carry `state["step_index"]` so steps align across demos. Every aligned
        step must satisfy pairwise structure Jaccard >= jaccard_threshold; fields with identical
        values across demos become constant anchors; fields with varying values (under a relevant
        root) become ${slot} placeholders with evidence_values gathered from the demos.
        """
        if not observations:
            return None
        by_step: dict[int, list[Observation]] = {}
        for o in observations:
            idx = o.state.get("step_index")
            if idx is None or not o.success:
                return None
            by_step.setdefault(int(idx), []).append(o)

        step_templates: list[dict[str, Any]] = []
        evidence_values: dict[str, list[str]] = {}
        induction: dict[str, Any] = {}
        evidence_ids: list[str] = []
        structure_ok = True

        for idx in sorted(by_step):
            obs = by_step[idx]
            actions = [o.action for o in obs]
            structure = _pairwise_structure_jaccard(actions)
            if structure < jaccard_threshold:
                structure_ok = False
                break
            ev, stats = _extract_varying_values(actions)
            for slot, vals in ev.items():
                evidence_values.setdefault(slot, [])
                for v in vals:
                    if v not in evidence_values[slot]:
                        evidence_values[slot].append(v)
            tmpl = stats["template"]
            step_templates.append(tmpl)
            induction[f"step_{idx}"] = {"structure_jaccard": round(structure, 6), "slots": sorted(ev)}
            evidence_ids.extend(self.observe(o)[:16] for o in obs)

        if not structure_ok or not step_templates or not evidence_values:
            return None

        over_all_jaccard = min(v["structure_jaccard"] for v in induction.values())
        if over_all_jaccard < structure_threshold:
            return None

        return Mechanism(
            mechanism_id=f"param-{family_id}",
            intent=intent,
            preconditions={"family": family_id, "authenticated": True},
            action_template={"steps": step_templates},
            postconditions={"status": 200, "done": True},
            parameter_slots=sorted(evidence_values),
            freshness={"behavioral_score": 0.8, "probe_url": f"file://mock/{family_id}"},
            evidence=sorted(set(evidence_ids)),
            evidence_values={k: sorted(v) for k, v in evidence_values.items()},
            confidence=0.5,  # placeholder: runtime confidence is derived per resolve (see _evidence_confidence)
            verification_rule={
                "postconditions_check": "exact",
                "induction": {
                    "pairwise_structure_jaccard": round(over_all_jaccard, 6),
                    "structure_similarity": round(over_all_jaccard, 6),
                },
            },
            repair_scope={"max_retries": 1, "alternatives_from": "evidence_values"},
        )

    def _evidence_confidence(self, mechanism: Mechanism, params: dict[str, Any]) -> float:
        """Runtime confidence from evidence consistency: softmax(temp=0.15) + seeded jitter.

        Per-slot consistency is 1.0 on an exact evidence match, otherwise the longest-common-
        prefix graded similarity to the nearest evidence value. Averaged over slots, converted
        through the softmax(logit) = sigmoid((2*mean-1)/0.15) map, then a Uniform(-0.05, 0.05)
        jitter whose seed is derived deterministically from (mechanism_id, params).
        Literal (slotless) mechanisms have no parameter risk: their stored confidence stands.
        """
        if not mechanism.parameter_slots:
            return mechanism.confidence
        scores: list[float] = []
        for slot in sorted(set(mechanism.parameter_slots)):
            value = params.get(slot)
            ev = mechanism.evidence_values.get(slot, [])
            if value is None or not ev:
                scores.append(0.0)
            elif value in ev:
                scores.append(1.0)
            else:
                scores.append(max(_value_similarity(value, e) for e in ev))
        s_mean = (sum(scores) / len(scores)) if scores else 0.0
        logit = max(-30.0, min(30.0, (2.0 * s_mean - 1.0) / _SOFTMAX_TEMPERATURE))
        exp_v = math.exp(logit)
        conf = exp_v / (1.0 + exp_v)
        digest = hashlib.sha256(
            f"{mechanism.mechanism_id}|{json.dumps(params, sort_keys=True)}".encode()
        ).hexdigest()
        seed = int(digest[:16], 16)
        jitter = random.Random(seed).uniform(-_CONFIDENCE_JITTER, _CONFIDENCE_JITTER)
        return min(1.0, max(0.0, conf + jitter))

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
            freshness = m.freshness.get("behavioral_score", 1.0) if isinstance(m.freshness, dict) else 1.0
            if freshness < self.freshness_threshold:
                continue
            required_slots = set(m.parameter_slots) | _template_slots(m.action_template)
            if any(slot not in params for slot in required_slots):
                continue
            candidates.append(m)

        if not candidates:
            return Resolution(ResolutionStatus.UNKNOWN, None, "no applicable validated mechanism")

        best = max(candidates, key=lambda m: self._evidence_confidence(m, params))
        confidence = self._evidence_confidence(best, params)
        if confidence < self.min_confidence:
            return Resolution(
                ResolutionStatus.UNKNOWN,
                best.mechanism_id,
                f"candidate exists but evidence-derived confidence {confidence:.4f} below execution threshold {self.min_confidence}",
                confidence=confidence,
            )

        return Resolution(
            ResolutionStatus.EXECUTABLE,
            best.mechanism_id,
            "applicability guards, freshness and confidence threshold passed",
            bound_action=_bind(best.action_template, params),
            confidence=confidence,
        )

    def verify(self, mechanism_id: str, observed_state: dict[str, Any]) -> bool:
        mechanism = next((m for m in self.registry.all() if m.mechanism_id == mechanism_id), None)
        if mechanism is None or mechanism.invalidated:
            return False
        return _matches(mechanism.postconditions, observed_state)

    def invalidate(self, mechanism_id: str) -> bool:
        return self.registry.invalidate(mechanism_id)