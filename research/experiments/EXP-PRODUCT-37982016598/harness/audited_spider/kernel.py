from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from typing import Any

from .models import Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry


_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

# Sentinel for values absent from a flattened observation.
_MISSING = object()

# Support descriptors are stored as anchored regular expressions. When a stable
# character-class grammar cannot be inferred, resolution falls back to this
# coarse, explicitly-recorded predicate.
_COARSE_SUPPORT = "__COARSE__"


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


def _flatten(value: Any, prefix: tuple[Any, ...] = ()) -> dict[tuple[Any, ...], Any]:
    """Flatten nested dict/list structures to {path_tuple: leaf_value}."""
    out: dict[tuple[Any, ...], Any] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            out.update(_flatten(item, prefix + (key,)))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            out.update(_flatten(item, prefix + (index,)))
    else:
        out[prefix] = value
    return out


def _assign_nested(target: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: dict[Any, Any] = target
    for key in path[:-1]:
        nxt = cursor.get(key)
        if not isinstance(nxt, dict):
            nxt = {}
            cursor[key] = nxt
        cursor = nxt
    cursor[path[-1]] = value


def _common_prefix(values: list[str]) -> str:
    if not values:
        return ""
    prefix = values[0]
    for value in values[1:]:
        limit = min(len(prefix), len(value))
        i = 0
        while i < limit and prefix[i] == value[i]:
            i += 1
        prefix = prefix[:i]
    return prefix


def _common_suffix(values: list[str]) -> str:
    return _common_prefix([v[::-1] for v in values])[::-1]


def _char_class(chars: set[str]) -> str | None:
    """Return a regex character class for a homogeneous character set."""
    digits = set("0123456789")
    lower = set("abcdefghijklmnopqrstuvwxyz")
    upper = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if chars and chars <= digits:
        return "0-9"
    if chars and chars <= lower:
        return "a-z"
    if chars and chars <= upper:
        return "A-Z"
    if chars and chars <= (lower | upper):
        return "a-zA-Z"
    if chars and chars <= (lower | digits):
        return "a-z0-9"
    if chars and chars <= (lower | upper | digits):
        return "a-zA-Z0-9"
    return None


def _infer_support(values: list[str]) -> str:
    """Infer an anchored support pattern from observed identifier values.

    The pattern is deliberately a grammar over the observed character classes
    and literal prefix, widened to a ``+`` quantifier when the observed lengths
    are not uniform, so an unseen in-support identifier generalizes while the
    declared negatives (empty, whitespace, ``/``) are refused.
    """
    values = [str(v) for v in values]
    if not values:
        return _COARSE_SUPPORT
    prefix = _common_prefix(values)
    remains = [v[len(prefix):] for v in values]
    charset = set("".join(remains))
    klass = _char_class(charset)
    if klass is None:
        return _COARSE_SUPPORT
    lengths = {len(r) for r in remains}
    quantifier = "{%d}" % next(iter(lengths)) if len(lengths) == 1 else "+"
    return "^" + re.escape(prefix) + "[" + klass + "]" + quantifier + "$"


def _support_accepts(support: str | None, value: Any) -> bool:
    text = str(value)
    if support is None:
        return True
    if support == _COARSE_SUPPORT:
        return bool(text) and not any(ch.isspace() or ch == "/" for ch in text)
    return re.fullmatch(support, text) is not None


def _derive_structural_name(prefix: str) -> str:
    segment = prefix.rstrip("/").split("/")[-1]
    segment = re.sub(r"[^A-Za-z0-9_]+", "_", segment).strip("_")
    if segment.endswith("s") and not segment.endswith("ss") and len(segment) > 1:
        segment = segment[:-1]
    return segment or "id"


def _derive_leaf_name(path: tuple[Any, ...]) -> str:
    key = re.sub(r"[^A-Za-z0-9_]+", "_", str(path[-1])).strip("_")
    if key.lower().startswith("x_"):
        key = key[2:]
    return key.lower() or "value"


@dataclass
class TrajectoryCounters:
    """Per-trajectory accounting surface for the inherited mechanism path."""

    model_calls: int = 0
    model_tokens: int = 0
    browser_actions: int = 0
    http_requests: int = 0
    retrieval_calls: int = 0
    verification_calls: int = 0
    repair_attempts: int = 0
    latency_ms: float = 0.0

    def add(self, field: str, amount: float = 1) -> None:
        current = getattr(self, field)
        setattr(self, field, current + amount)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class SpiderKernel:
    """Conservative execution-inheritance kernel.

    This kernel is deliberately not a browser agent. It stores and resolves
    validated mechanisms and abstains when applicability is not demonstrated.

    Research 2.0 extension: ``distill_parameterized`` induces a parameterized
    mechanism from repeated successful observations, and ``resolve`` refuses
    bindings whose parameters are missing or outside the inferred support. The
    pre-existing literal ``distill`` path is preserved unchanged so the
    pre-repair control (``B-LITERAL-KERNEL``) can be reproduced.
    """

    def __init__(
        self,
        registry: MechanismRegistry,
        min_confidence: float = 0.8,
        counters: TrajectoryCounters | None = None,
    ):
        self.registry = registry
        self.min_confidence = min_confidence
        self.counters = counters

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

    # -- literal, pre-repair path (kept as the causal-attribution control) ----

    def distill(self, observation: Observation) -> Mechanism | None:
        """Create only a literal candidate mechanism (pre-repair behaviour).

        Generalization/parameter induction is intentionally not guessed here;
        the parameterized path is ``distill_parameterized``. Confidence is the
        historical hardcoded 0.5, which the default ``min_confidence`` of 0.8
        refuses, reproducing the shipped pre-repair semantics exactly.
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

    def _parameterized_confidence(self) -> float:
        # A mechanism whose parameterized postconditions re-verify on every
        # induction observation has demonstrated applicability and is allowed
        # to reach the execution threshold. Selectivity is enforced by the
        # support descriptors, not by keeping every mechanism below threshold.
        return 0.9

    def distill_parameterized(self, observations: list[Observation]) -> Mechanism | None:
        """Induce one parameterized mechanism from repeated successful observations.

        Returns ``None`` when fewer than two successful same-intent
        observations exist, when no action-template field varies, or when the
        structure is not stable. Fields that vary only in the surrounding
        state/next_state (trace id, sequence, timestamp noise) are never
        promoted to parameter slots.
        """
        obs = [o for o in observations if o.success]
        if len(obs) < 2:
            return None
        intents = {o.intent for o in obs}
        if len(intents) != 1:
            return None
        intent = obs[0].intent

        flats = [_flatten(o.action) for o in obs]
        paths: set[tuple[Any, ...]] = set()
        for flat in flats:
            paths.update(flat.keys())

        varying: list[tuple[Any, ...]] = []
        for path in sorted(paths, key=lambda p: tuple(str(x) for x in p)):
            values = [flat.get(path, _MISSING) for flat in flats]
            if any(v is _MISSING for v in values):
                continue
            if len({repr(v) for v in values}) > 1:
                varying.append(path)

        if not varying:
            return None

        template = json.loads(json.dumps(obs[0].action))
        slots: list[str] = []
        supports: dict[str, str] = {}
        slot_values: dict[str, list[Any]] = {}

        for path in varying:
            raw_values = [flat[path] for flat in flats]
            string_values = [str(v) for v in raw_values]
            first = string_values[0]
            is_url = str(path[-1]).lower() == "url" or first.startswith(("http://", "https://"))
            segment_template: str | None = None
            segment_values: list[str] = []
            segment_name: str | None = None
            if is_url and all(isinstance(v, str) for v in raw_values):
                parts = [v.split("/") for v in string_values]
                if parts and all(len(p) == len(parts[0]) for p in parts):
                    varying_indexes = [
                        i for i in range(len(parts[0]))
                        if len({p[i] for p in parts}) > 1
                    ]
                    if len(varying_indexes) == 1:
                        index = varying_indexes[0]
                        segment_values = [p[index] for p in parts]
                        static_prefix = "/".join(parts[0][:index])
                        segment_name = _derive_structural_name(static_prefix + "/")
                        template_parts = list(parts[0])
                        template_parts[index] = "${" + segment_name + "}"
                        segment_template = "/".join(template_parts)

            use_segment = segment_template is not None
            if use_segment:
                name = segment_name or "id"
                placeholder = segment_template
                support = _infer_support(segment_values)
                bound_values: list[Any] = segment_values
            elif is_url and all(isinstance(v, str) for v in raw_values):
                prefix = _common_prefix(string_values)
                suffix = _common_suffix(string_values)
                middle = [
                    v[len(prefix): len(v) - len(suffix)] if suffix else v[len(prefix):]
                    for v in string_values
                ]
                name = _derive_structural_name(prefix)
                placeholder = prefix + "${" + name + "}" + (suffix or "")
                support = _infer_support(middle)
                bound_values = middle
            else:
                name = _derive_leaf_name(path)
                placeholder = "${" + name + "}"
                support = _infer_support(string_values)
                bound_values = raw_values

            base_name = name
            counter = 2
            while name in slots:
                name = f"{base_name}_{counter}"
                counter += 1
                placeholder = placeholder.replace("${" + base_name + "}", "${" + name + "}")

            _assign_nested(template, path, placeholder)
            slots.append(name)
            supports[name] = support
            slot_values[name] = bound_values

        # Stable state fields form the preconditions; noise fields are dropped.
        stable_state = {
            key: value
            for key, value in obs[0].state.items()
            if all(o.state.get(key) == value for o in obs)
        }

        # Parameterized postconditions: stable fields are literal, varying
        # fields that co-vary with a slot are templated, other noise is dropped.
        flat_next = [_flatten(o.next_state) for o in obs]
        next_paths: set[tuple[Any, ...]] = set()
        for flat in flat_next:
            next_paths.update(flat.keys())
        postconditions: dict[str, Any] = {}
        for path in sorted(next_paths, key=lambda p: tuple(str(x) for x in p)):
            values = [flat.get(path, _MISSING) for flat in flat_next]
            if any(v is _MISSING for v in values):
                continue
            if all(v == values[0] for v in values):
                _assign_nested(postconditions, path, values[0])
                continue
            for slot, observed in slot_values.items():
                if values == observed:
                    _assign_nested(postconditions, path, "${" + slot + "}")
                    break

        mechanism_id = "mech-" + hashlib.sha256(
            json.dumps(
                {"intent": intent, "template": template, "slots": slots},
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()[:16]

        mechanism = Mechanism(
            mechanism_id=mechanism_id,
            intent=intent,
            preconditions=stable_state,
            action_template=template,
            postconditions=postconditions,
            parameter_slots=slots,
            verification_rule={"parameter_supports": supports},
            evidence=[self.observe(o)[:16] for o in obs],
            confidence=0.0,
        )

        # Applicability is demonstrated by successful re-verification on the
        # mechanism's own induction observations.
        self_verified = True
        for index, observation in enumerate(obs):
            params = {slot: slot_values[slot][index] for slot in slots}
            bound_post = _bind(mechanism.postconditions, params)
            if not _matches(bound_post, observation.next_state):
                self_verified = False
                break
        mechanism.confidence = self._parameterized_confidence() if self_verified else 0.5
        return mechanism

    def resolve(self, intent: str, context: dict[str, Any], params: dict[str, Any] | None = None) -> Resolution:
        params = params or {}
        if self.counters is not None:
            self.counters.add("retrieval_calls")

        candidates: list[Mechanism] = []
        refusals: list[tuple[Mechanism, str]] = []
        for m in self.registry.all():
            if m.invalidated or m.intent != intent:
                continue
            if not _matches(m.preconditions, context):
                continue
            if not _matches(m.applicability_guards, context):
                continue

            required_slots = set(m.parameter_slots) | _template_slots(m.action_template)
            missing = sorted(slot for slot in required_slots if slot not in params)
            if missing:
                refusals.append((m, f"missing required parameter '{missing[0]}'"))
                continue

            supports = m.verification_rule.get("parameter_supports", {}) if m.verification_rule else {}
            bad = sorted(
                slot
                for slot in required_slots
                if slot in supports and not _support_accepts(supports[slot], params[slot])
            )
            if bad:
                refusals.append((m, f"parameter '{bad[0]}' outside inferred support"))
                continue

            candidates.append(m)

        if not candidates:
            if refusals:
                mechanism, reason = refusals[0]
                return Resolution(
                    ResolutionStatus.EXPLORE,
                    mechanism.mechanism_id,
                    reason,
                    bound_action=None,
                    confidence=mechanism.confidence,
                )
            return Resolution(ResolutionStatus.UNKNOWN, None, "no applicable validated mechanism")

        candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
        best = candidates[0]
        if best.confidence < self.min_confidence:
            return Resolution(
                ResolutionStatus.EXPLORE,
                best.mechanism_id,
                "candidate exists but confidence is below execution threshold",
                confidence=best.confidence,
            )

        return Resolution(
            ResolutionStatus.EXECUTABLE,
            best.mechanism_id,
            "applicability guards and confidence threshold passed",
            bound_action=_bind(best.action_template, params),
            confidence=best.confidence,
        )

    def rebind(self, intent: str, context: dict[str, Any], params: dict[str, Any] | None = None) -> Resolution:
        """One repair attempt: re-bind after a previous rejection.

        Counts a single ``repair_attempts`` event on the inherited path.
        """
        if self.counters is not None:
            self.counters.add("repair_attempts")
        return self.resolve(intent, context, params)

    def verify(self, mechanism_id: str, observed_state: dict[str, Any], params: dict[str, Any] | None = None) -> bool:
        if self.counters is not None:
            self.counters.add("verification_calls")
        mechanism = next((m for m in self.registry.all() if m.mechanism_id == mechanism_id), None)
        if mechanism is None or mechanism.invalidated:
            return False
        required = _bind(mechanism.postconditions, params) if params is not None else mechanism.postconditions
        return _matches(required, observed_state)

    def invalidate(self, mechanism_id: str) -> bool:
        return self.registry.invalidate(mechanism_id)
