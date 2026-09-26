from __future__ import annotations

import hashlib
import json
import os
import re
from typing import Any, Iterable, Mapping, Sequence

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


# --------------------------------------------------------------------------- #
# Parameter induction (C-PARAM-INHERIT)
# --------------------------------------------------------------------------- #
#
# ``distill`` above deliberately creates only a *literal* mechanism. The functions
# below implement the durable, deterministic parameter-induction capability that
# C-PARAM-INHERIT needs: they read nothing but a list of successful
# ``Observation`` records and return ``Mechanism`` objects whose
# ``action_template`` carries ``${slot}`` placeholders for the parts of the
# action that varied across the evidence.
#
# Three rules make the induction conservative rather than inventive:
#
# 1. *Allowlist* - only ``ACTION_FIELD_ALLOWLIST`` top-level keys of
#    ``Observation.action`` are inspected. Volatile substrate metadata
#    (``timestamp``, ``request_id``, ``trace_id``, ...) is never turned into a
#    parameter slot.
# 2. *Linkage* - a varying field whose values are exactly covered by a varying
#    context field (e.g. the ``items``/``tags`` token in the path is exactly the
#    value of ``state["collection"]``) is named after that context field, so the
#    slot is re-bindable from the caller's task context at resolve time.
#    A context field that varies but is *not* referenced by the induced template
#    is dropped: an abstraction nobody can bind is not a capability.
# 3. *Structure gate* - a mechanism is emitted only when the observations are
#    structurally similar (mean pairwise Jaccard of action shapes >= 0.75) **and**
#    at least one constant-value anchor pins the group. Unrelated evidence yields
#    no mechanism at all rather than hallucinated slots.
#
# Confidence is derived from the evidence, never hardcoded: a Beta posterior mean
# over the group's observed success rate multiplied by a leave-one-out
# re-construction consistency rate. The leave-one-out term is what stops a
# mechanism whose structure is an artefact of a single observation from being
# executable.

#: Only these top-level keys of ``Observation.action`` are inspected.
ACTION_FIELD_ALLOWLIST: tuple[str, ...] = ("method", "url", "path", "body", "headers", "query")

#: Keys whose values are volatile substrate metadata; a varying value under one of
#: these is dropped instead of induced.
VOLATILE_KEY_DENYLIST: frozenset[str] = frozenset(
    {
        "timestamp", "ts", "time", "clock", "request_id", "requestid",
        "trace_id", "traceid", "span_id", "received_at", "elapsed_ms",
        "latency_ms", "duration_ms", "uptime", "etag", "last_modified",
        "date", "server_time", "nonce", "cursor", "session_id", "sessionid",
        "cookie", "set_cookie", "server", "content_length", "random",
    }
)

#: Header names carrying credentials. A durable mechanism must not persist a
#: bearer token, so these become a parameter slot bound at resolve time.
SECRET_HEADER_KEYS: frozenset[str] = frozenset(
    {"authorization", "proxy-authorization", "x-api-key", "x-auth-token"}
)

SECRET_HEADER_SLOT = "auth_token"
TERMINAL_IDENTIFIER_SLOT = "id"

#: Minimum mean pairwise Jaccard similarity of action shapes for a group to be
#: considered one coherent mechanism.
STRUCTURE_JACCARD_THRESHOLD = 0.75

#: Weak Beta(2, 1) prior for the per-group success rate.
_BETA_ALPHA = 2.0
_BETA_BETA = 1.0


def _observation_id(observation: Observation) -> str:
    raw = json.dumps(
        {
            "intent": observation.intent,
            "state": observation.state,
            "action": observation.action,
            "next_state": observation.next_state,
            "success": observation.success,
            "provenance": observation.provenance,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def _copy_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _copy_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_copy_value(v) for v in value]
    return value


def _common_prefix(values: Sequence[str]) -> str:
    return os.path.commonprefix(list(values)) if values else ""


def _common_suffix(values: Sequence[str]) -> str:
    reversed_common = os.path.commonprefix([v[::-1] for v in values])
    return reversed_common[::-1] if values else ""


def _freeze(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _linkable(values: Sequence[Any], links: Mapping[str, frozenset[Any]]) -> str | None:
    """Return the varying context field whose observed values cover ``values``."""
    observed = frozenset(_freeze(v) for v in values)
    for name in sorted(links):
        if observed and observed <= links[name]:
            return name
    return None


def _structural_slot(field_path: str, *, terminal: bool) -> str:
    """Name a slot that no context field accounts for.

    Convention: the terminal segment of a ``path``/``url`` is the resource
    identifier and is named ``id``; anything else is named after its own field.
    """
    if terminal:
        return TERMINAL_IDENTIFIER_SLOT
    leaf = re.sub(r"\[\d+\]", "", field_path.split(".")[-1])
    return leaf or "param"


def _is_volatile_key(key: str) -> bool:
    return key.strip().lower() in VOLATILE_KEY_DENYLIST


def _shape(action: Mapping[str, Any]) -> frozenset[str]:
    """Structural signature of an action: key paths plus value types, no values."""
    out: set[str] = set()

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key in sorted(value):
                walk(value[key], f"{path}.{key}" if path else key)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, f"{path}[{index}]")
        else:
            out.add(f"{path}:{type(value).__name__}")

    for key in sorted(action):
        if key in ACTION_FIELD_ALLOWLIST:
            walk(action[key], key)
    return frozenset(out)


def _jaccard(left: frozenset[str], right: frozenset[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _template_parts(template: str) -> list[tuple[str, str]]:
    parts: list[tuple[str, str]] = []
    cursor = 0
    for match in _PARAMETER.finditer(template):
        if match.start() > cursor:
            parts.append(("literal", template[cursor : match.start()]))
        parts.append(("slot", match.group(1)))
        cursor = match.end()
    if cursor < len(template):
        parts.append(("literal", template[cursor:]))
    return parts


def _slot_regex(template: str) -> re.Pattern[str] | None:
    parts = _template_parts(template)
    if not any(kind == "slot" for kind, _ in parts):
        return None
    body = "".join(
        f"(?P<{text}>.*?)" if kind == "slot" else re.escape(text)
        for kind, text in parts
    )
    try:
        return re.compile(body + r"\Z", re.DOTALL)
    except re.error:  # pragma: no cover - defensive
        return None


def align_parameters(template: Any, observed: Any, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Recover the slot values that map an induced ``template`` onto ``observed``.

    Returns ``None`` when ``observed`` is not an instance of ``template``. This is
    the alignment used both by the leave-one-out self-check and by callers that
    want to bind a mechanism without knowing its slot names in advance.
    """
    out: dict[str, Any] = dict(params or {})
    if not _align(template, observed, out):
        return None
    return out


def _align(template: Any, observed: Any, params: dict[str, Any]) -> bool:
    if isinstance(template, str):
        whole = _PARAMETER.fullmatch(template)
        if whole is not None:
            # A whole-value slot accepts any scalar the evidence contained, not
            # only a string: an integer-valued query parameter (limit, offset,
            # page) must round-trip as an integer, otherwise alignment silently
            # fails on exactly the fields that carry the most information.
            if not isinstance(observed, (str, int, float, bool)):
                return False
            params[whole.group(1)] = observed
            return True
        match = _slot_regex(template)
        if not isinstance(observed, str):
            return False
        if match is None:
            return template == observed
        found = match.match(observed)
        if found is None:
            return False
        params.update({k: v for k, v in found.groupdict().items()})
        return True
    if isinstance(template, dict):
        if not isinstance(observed, dict) or set(template) != set(observed):
            return False
        return all(_align(template[k], observed[k], params) for k in template)
    if isinstance(template, list):
        if not isinstance(observed, list) or len(template) != len(observed):
            return False
        return all(_align(t, o, params) for t, o in zip(template, observed))
    return template == observed


def _induce_path(values: Sequence[str], field_path: str, links: Mapping[str, frozenset[Any]]) -> tuple[str, list[str]]:
    segments = [v.split("/") for v in values]
    widths = {len(s) for s in segments}
    if len(widths) != 1:
        name = _structural_slot(field_path, terminal=True)
        return "${%s}" % name, [name]
    width = widths.pop()
    parts: list[str] = []
    slots: list[str] = []
    for index in range(width):
        column = [s[index] for s in segments]
        if all(item == column[0] for item in column):
            parts.append(column[0])
            continue
        if any("/" in item for item in column):
            # The identifier is itself a compound value (a whole URL). Splicing it
            # segment-wise would let a bound full URL be double-prefixed, so the
            # whole varying value becomes one slot.
            name = _structural_slot(field_path, terminal=True)
            parts.append("${%s}" % name)
            slots.append(name)
            continue
        linked = _linkable(column, links)
        if linked is not None:
            parts.append("${%s}" % linked)
            slots.append(linked)
            continue
        terminal = index == width - 1
        name = _structural_slot(f"{field_path}[{index}]", terminal=terminal)
        prefix = _common_prefix(column)
        suffix = _common_suffix(column)
        if prefix or suffix:
            parts.append(f"{prefix}${{{name}}}{suffix}")
        else:
            parts.append("${%s}" % name)
        slots.append(name)
    return "/".join(parts), _dedupe(slots)


def _induce_field(
    values: Sequence[Any],
    field_path: str,
    links: Mapping[str, frozenset[Any]],
    *,
    terminal: bool = False,
) -> tuple[Any, list[str]]:
    first = values[0]
    if all(item == first for item in values):
        redacted, found = _redact_secrets(first, field_path)
        return redacted, found

    if all(isinstance(item, str) for item in values):
        if any("/" in item for item in values):
            prefix = _common_prefix(values)
            suffix = _common_suffix(values)
            scheme = re.match(r"^[A-Za-z][A-Za-z0-9+.\-]*://", prefix)
            anchored = len(prefix) > (len(scheme.group(0)) if scheme else 0) or bool(suffix)
            if anchored:
                return _induce_path(values, field_path, links)
            # No anchor beyond the scheme: these are whole-value identifiers (each
            # value is itself a URL). Splicing a shared prefix onto a full URL is
            # exactly the double-prefix defect, so the whole value stays one slot.
            name = _structural_slot(field_path, terminal=True)
            return "${%s}" % name, [name]
        linked = _linkable(values, links)
        if linked is not None:
            return "${%s}" % linked, [linked]
        prefix = _common_prefix(values)
        suffix = _common_suffix(values)
        name = _structural_slot(field_path, terminal=terminal)
        shortest = min(len(item) for item in values)
        if prefix and suffix and len(prefix) + len(suffix) >= shortest:
            return "${%s}" % name, [name]
        if prefix or suffix:
            return f"{prefix}${{{name}}}{suffix}", [name]
        return "${%s}" % name, [name]

    if all(isinstance(item, dict) for item in values):
        keys: list[str] = []
        for item in values:
            for key in item:
                if _is_volatile_key(key):
                    continue
                if key not in keys:
                    keys.append(key)
        template: dict[str, Any] = {}
        slots: list[str] = []
        for key in keys:
            if key.strip().lower() in SECRET_HEADER_KEYS:
                # A durable mechanism must never persist a credential.
                template[key] = "${%s}" % SECRET_HEADER_SLOT
                slots.append(SECRET_HEADER_SLOT)
                continue
            if not all(key in item for item in values):
                continue  # structurally absent in some evidence: treat as noise
            sub, sub_slots = _induce_field(
                [item[key] for item in values], f"{field_path}.{key}", links
            )
            template[key] = sub
            slots.extend(sub_slots)
        return template, _dedupe(slots)

    if all(isinstance(item, list) for item in values):
        lengths = {len(item) for item in values}
        if len(lengths) == 1:
            out: list[Any] = []
            slots = []
            for index in range(lengths.pop()):
                sub, sub_slots = _induce_field(
                    [item[index] for item in values], f"{field_path}[{index}]", links
                )
                out.append(sub)
                slots.extend(sub_slots)
            return out, _dedupe(slots)

    name = _linkable(values, links) or _structural_slot(field_path, terminal=terminal)
    return "${%s}" % name, [name]


def _dedupe(items: Iterable[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        if item not in out:
            out.append(item)
    return out


def _redact_secrets(value: Any, field_path: str) -> tuple[Any, list[str]]:
    """Strip credentials from a value that is being copied verbatim.

    A field that happens to be constant across the evidence is still a field, and
    an ``Authorization`` header is constant far more often than it is safe: a
    durable mechanism that persists a bearer token is a credential leak with a
    long half-life. The constant fast path must not be a way around redaction.
    """
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        slots: list[str] = []
        for key, item in value.items():
            if key.strip().lower() in SECRET_HEADER_KEYS:
                out[key] = "${%s}" % SECRET_HEADER_SLOT
                slots.append(SECRET_HEADER_SLOT)
                continue
            sub, sub_slots = _redact_secrets(item, f"{field_path}.{key}")
            out[key] = sub
            slots.extend(sub_slots)
        return out, _dedupe(slots)
    if isinstance(value, list):
        items: list[Any] = []
        slots = []
        for index, item in enumerate(value):
            sub, sub_slots = _redact_secrets(item, f"{field_path}[{index}]")
            items.append(sub)
            slots.extend(sub_slots)
        return items, _dedupe(slots)
    return _copy_value(value), []


def _structure_similarity(actions: Sequence[Mapping[str, Any]]) -> float:
    if len(actions) < 2:
        return 1.0
    shapes = [_shape(action) for action in actions]
    total = 0.0
    pairs = 0
    for i in range(len(shapes)):
        for j in range(i + 1, len(shapes)):
            total += _jaccard(shapes[i], shapes[j])
            pairs += 1
    return total / pairs if pairs else 1.0


def _has_constant_anchor(observations: Sequence[Observation]) -> bool:
    for key in ACTION_FIELD_ALLOWLIST:
        present = [o.action[key] for o in observations if key in o.action]
        if present and all(item == present[0] for item in present):
            if key in SECRET_HEADER_KEYS:
                continue
            return True
    return False


def _group_by_intent(observations: Sequence[Observation]) -> dict[str, list[Observation]]:
    groups: dict[str, list[Observation]] = {}
    for observation in observations:
        groups.setdefault(observation.intent, []).append(observation)
    return groups


def _global_state_constants(observations: Sequence[Observation]) -> dict[str, Any]:
    """Context fields that are constant across *all* successful evidence.

    Volatile substrate metadata (session ids, cursors, timestamps) is excluded by
    the same denylist that protects action fields: a session identifier is
    session-scoped substrate noise, not a precondition a mechanism may impose. A
    mechanism that pinned it could never be inherited across sessions.
    """
    if not observations:
        return {}
    state = observations[0].state
    return {
        key: value
        for key, value in state.items()
        if not _is_volatile_key(key)
        and all(key in o.state and o.state[key] == value for o in observations)
    }


def _present_state_keys(observations: Sequence[Observation]) -> list[str]:
    if not observations:
        return []
    keys: list[str] = []
    for key in observations[0].state:
        if _is_volatile_key(key):
            continue
        if all(key in o.state for o in observations) and key not in keys:
            keys.append(key)
    return keys


def _induce_candidate(
    intent: str,
    observations: Sequence[Observation],
    global_constants: Mapping[str, Any],
) -> Mechanism | None:
    """Induce the *structure* of one intent group, or abstain.

    Returns a ``Mechanism`` whose ``confidence`` is still ``0.0``. Confidence is
    assigned by :func:`_build_group_mechanism` alone, so the leave-one-out
    self-check can re-induce structure without recursing into itself.
    """
    if len(observations) < 2:
        return None
    actions = [o.action for o in observations]
    if _structure_similarity(actions) < STRUCTURE_JACCARD_THRESHOLD:
        return None
    if not _has_constant_anchor(observations):
        return None

    state = observations[0].state
    state_keys = _present_state_keys(observations)
    group_constants = {
        key: state[key]
        for key in state_keys
        if all(o.state.get(key) == state[key] for o in observations)
    }
    varying_context = [key for key in state_keys if key not in group_constants]
    links: dict[str, frozenset[Any]] = {
        key: frozenset(_freeze(o.state[key]) for o in observations) for key in sorted(varying_context)
    }

    preconditions = {
        key: value
        for key, value in global_constants.items()
        if all(key in o.state for o in observations)
    }
    guards = {key: value for key, value in group_constants.items() if key not in preconditions}

    action_template: dict[str, Any] = {}
    slots: list[str] = []
    for key in ACTION_FIELD_ALLOWLIST:
        if key in SECRET_HEADER_KEYS:
            action_template[key] = "${%s}" % SECRET_HEADER_SLOT
            slots.append(SECRET_HEADER_SLOT)
            continue
        present = [o.action[key] for o in observations if key in o.action]
        if not present or len(present) != len(observations):
            continue
        value, found = _induce_field(
            present, key, links, terminal=key in ("path", "url")
        )
        action_template[key] = value
        slots.extend(found)

    referenced = _template_slots(action_template)
    parameter_slots = _dedupe(slots) + [name for name in sorted(links) if name in referenced]
    parameter_slots = _dedupe(parameter_slots)
    if not parameter_slots:
        return None  # no transferable abstraction: nothing to inherit

    postconditions = {
        key: value
        for key, value in observations[0].next_state.items()
        if all(o.next_state.get(key) == value for o in observations)
    }
    verification_rule: dict[str, Any] = {}
    if "status" in postconditions:
        verification_rule = {"status": postconditions["status"], "source": "observed_success_postcondition"}

    distinct_ids = {
        _freeze(o.provenance.get("identifier"))
        for o in observations
        if o.provenance.get("identifier") is not None
    }
    sessions = {
        _freeze(o.state.get("session_id")) for o in observations if o.state.get("session_id")
    }

    signature = hashlib.sha256(
        _freeze({"intent": intent, "template": action_template, "slots": parameter_slots}).encode()
    ).hexdigest()[:12]

    return Mechanism(
        mechanism_id=f"param-{intent}-{signature}",
        intent=intent,
        preconditions=dict(preconditions),
        action_template=action_template,
        postconditions=dict(postconditions),
        parameter_slots=parameter_slots,
        auth_scope=preconditions.get("auth"),
        freshness={
            "observed_distinct_identifiers": len(distinct_ids),
            "observed_sessions": len(sessions),
            "observed_conditional_get": any(
                o.provenance.get("status") == 304 for o in observations
            ),
        },
        applicability_guards=guards,
        verification_rule=verification_rule,
        failure_boundary={
            "unbound_slot_policy": "abstain",
            "below_min_confidence_status": "EXPLORE",
            "structure_jaccard_threshold": STRUCTURE_JACCARD_THRESHOLD,
        },
        repair_scope={"policy": "none", "note": "delta repair is C-DELTA-REPAIR, out of scope here"},
        evidence=sorted(_observation_id(o)[:16] for o in observations),
        confidence=0.0,
    )


def _build_group_mechanism(
    intent: str,
    observations: Sequence[Observation],
    global_constants: Mapping[str, Any],
) -> Mechanism | None:
    """Induce one mechanism from one intent group, with evidence-derived confidence."""
    mechanism = _induce_candidate(intent, observations, global_constants)
    if mechanism is None:
        return None
    successes = sum(1 for o in observations if o.success)
    posterior_mean = (successes + _BETA_ALPHA) / (len(observations) + _BETA_ALPHA + _BETA_BETA)
    loo_consistency, _ = _leave_one_out_consistency(intent, observations, global_constants)
    mechanism.confidence = round(posterior_mean * loo_consistency, 6)
    return mechanism


def _leave_one_out_consistency(
    intent: str, observations: Sequence[Observation], global_constants: Mapping[str, Any]
) -> tuple[float, int]:
    """Fraction of observations reconstructible from a structure induced without them.

    A template that exists only because of one observation cannot reconstruct that
    observation once it has been removed, so this term is an identifiability check
    on the induced structure and not a restatement of the success rate.
    """
    if len(observations) < 3:
        return 0.0, 0
    consistent = 0
    attempted = 0
    for index in range(len(observations)):
        rest = observations[:index] + observations[index + 1 :]
        candidate = _induce_candidate(intent, rest, global_constants)
        if candidate is None:
            continue
        params = align_parameters(candidate.action_template, observations[index].action)
        if params is None:
            continue
        attempted += 1
        if _bind(candidate.action_template, params) == observations[index].action:
            consistent += 1
    if attempted == 0:
        return 0.0, 0
    return consistent / attempted, attempted


def distill_parameterized(observations: list[Observation]) -> list[Mechanism]:
    """Induce transferable, parameter-slot mechanisms from successful observations.

    Deterministic and model-free. Only successful observations are used. One
    mechanism is returned per intent group that passes the structure gate, and
    ``confidence`` is derived from that group's own evidence (Beta posterior mean
    over the observed success rate times leave-one-out re-construction
    consistency) rather than being a constant. Nothing outside
    ``ACTION_FIELD_ALLOWLIST`` is read, and no field absent from every observation
    of a group is invented.

    ``freshness`` here is *evidence-scope metadata* (how many distinct identifiers
    and sessions the evidence covered, whether a 304 was observed). It is not a
    staleness decision; C-FRESHNESS is a separate claim and is not exercised by
    this function. Likewise ``repair_scope`` records that no repair capability
    exists rather than implying one.
    """
    successful = [o for o in observations if o.success]
    if not successful:
        return []
    global_constants = _global_state_constants(successful)
    mechanisms: list[Mechanism] = []
    for intent in sorted(_group_by_intent(successful)):
        group = [o for o in successful if o.intent == intent]
        mechanism = _build_group_mechanism(intent, group, global_constants)
        if mechanism is not None:
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
        return _observation_id(observation)

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

    def distill_parameterized(self, observations: list[Observation], register: bool = True) -> list[Mechanism]:
        """Durable kernel entry point for parameter induction.

        Delegates to the module-level :func:`distill_parameterized` and, by default,
        upserts the result into this kernel's registry so the mechanisms are
        resolvable through the ordinary :meth:`resolve` path.
        """
        mechanisms = distill_parameterized(observations)
        if register:
            for mechanism in mechanisms:
                self.registry.upsert(mechanism)
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

        candidates.sort(
            key=lambda m: (m.confidence, len(set(m.parameter_slots) | _template_slots(m.action_template))),
            reverse=True,
        )
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
