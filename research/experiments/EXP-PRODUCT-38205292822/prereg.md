# EXP-PRODUCT-38205292822 — ship the certified ingested-declaration guard

Lane: **product** · design_contract_version: **2** · request base_sha `40dfc33d90d4c3b0a139fc8c3f434257de623eb5` · chain_depth 0.

<!-- BEGIN CANONICAL-HASHES -->
- experiment_id: `EXP-PRODUCT-38205292822`
- carrier pre-state: `src/spider/kernel.py` git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` · sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`
- carrier post-state (this experiment installs it): sha256 `3a6caf970f5c86db19419f7ae57c7125f409eceba922eb2d5a9f5964140bb1b3`
- pre-promotion literal (ablation): git blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50` · sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`
- parent handoff: `research/experiments/EXP-PRODUCT-38201227093/handoff.json` (sha256 `bf5642316138ba7d0c35cbe1b314e1b489fdde35071accd9839484306899c869`)
- request: `research/experiments/EXP-PRODUCT-38205292822/request.json` (sha256 `016ab584459fd890764169c3c6bee9a92cca3cefba31f82b5d74cb56d19083cb`)
- claim ids: `C-PARAM-INHERIT` (CHALLENGED, EXPERIMENTAL), `C-SEMANTIC-RESOLVE` (RETAINED, HYPOTHESIS)
<!-- END CANONICAL-HASHES -->

## 1. Director mandate and inherited state

The Global Research Director allocated `CONTINUE` / `REOPEN` of `C-PARAM-INHERIT` with two binding questions:

1. Can the ingested-declared-grammar applicability guard be implemented as an **ACTUAL shipped change in `src/spider/kernel.py`** — not an in-run support descriptor — surviving a regression gate plus an adversarial / partially-observable-declaration test, holding zero false accepts, zero out-of-grammar HTTP executions and zero refusal-semantics violations while raising safe coverage on the pinned-subrange FAM-D (`region-00[0-9]`) and the non-pinned FAM-F / FAM-G?
2. Since BP-DECL-OVERWIDE proved the training-consistency gate cannot detect an over-wide unsound declaration (201 false accepts under an all-true declaration), **what certification step establishes declaration soundness** — and if soundness is not certifiable in the general case, **what bounded closed-world trust boundary** must the shipped kernel enforce, with UNKNOWN preferred over unsafe inheritance?

Inherited from the exact parent handoff (`EXP-PRODUCT-38201227093`), preserved without silent rewrite:

- **established**: the in-run declared-grammar guard `T-DECLARED-GUARD` was safe+complete on the extended seven-family bank (FA=0, HTTP-on-OUT=0, refusal-executed=0, coverage 1.0 vs shipped 0.6750); the carrier identity `718efa6a…` holds; the safe+complete ceiling `B-DECLARED-FULL` exists (FA=0, coverage 1.0); the purely observational ambiguity guard is bounded UNSAFE on FAM-F (FA=4); the parent data-driven widening is bounded negative (FA=18).
- **rejected** (bounded): the specific purely observational pre-bind ambiguity-refusal rule; the hypothesis that no safe+complete support exists on this bank; the hypothesis that a training-consistency gate can detect an unsound over-wide declaration; the hypothesis that the shipped conservative support is a safety defect.
- **unknown**: (i) whether the guard still holds as REAL shipped code (no `src/spider/` file was modified; no guard regression suite existed); (ii) how to certify declaration soundness in a real setting; (iii) the full space of observational rules; (iv) real-world cost/staleness of obtaining SOUND declared grammars; (v) the four-arm C-LLM-INHERIT benchmark is dependency-gated on Runtime B2 and Intel B3.
- **do_not_assume**: do not read the parent as advancing either claim; do not promote; do not generalize T-DECLARED-GUARD FA=0 into a general safety claim; do not treat the T-AMBIGUITY-GUARD UNSAFE as the overall falsifier; do not re-run the promotion certificate (EXP-PRODUCT-38180719830) or the observational-widening negative (EXP-PRODUCT-38197856050); do not substitute the carrier (identity/binding failure is BLOCKED/MEASUREMENT_INVALID, never a scientific negative).

## 2. Question, hypothesis, falsifier

**Question.** When the declared-grammar guard is REAL shipped code in `src/spider/kernel.py` that adopts an ingested declaration only after a **closed-world certificate** against a frozen audited negative bank, does it (a) preserve safe+complete resolution on sound declarations, (b) refuse a training-consistent over-wide declaration that the parent gate adopts, and (c) how far does its soundness guarantee extend?

**Hypothesis.** A shipped `SpiderKernel.ingest_declaration` that replaces a mechanism's inferred parameter support with an ingested declaration **iff** `certify_declaration` accepts it (declaration is a valid regex that accepts every training positive and rejects every value of a frozen audited negative bank) will (i) under a SOUND declaration hold FA=0 / HTTP-on-OUT=0 / refusal-executed=0 at coverage 1.0 (a strict safe-coverage gain over shipped 0.6750), (ii) under a training-consistent OVER-WIDE declaration refuse it and preserve the shipped boundary (FA=0), whereas the parent training-consistency gate adopts it and inherits 201 false accepts, and (iii) is **not** a general soundness proof: a certificate-passing declaration whose over-accept lies outside the audited bank still yields false accepts, so the correct product boundary is closed-world plus UNKNOWN-first abstention.

**Falsifier.** The shipped-certificate arm is falsified if it is not safe where it must be: `M-CERT-SOUND-FALSE-ACCEPT-COUNT > 0`, `M-CERT-SOUND-HTTP-ON-OUT > 0`, `M-CERT-SOUND-REFUSAL-EXECUTED-COUNT > 0`, `M-CERT-OVERWIDE-FALSE-ACCEPT-COUNT > 0`, `M-CERT-OVERWIDE-HTTP-ON-OUT > 0`, or `M-CERT-OVERWIDE-REFUSAL-EXECUTED-COUNT > 0`. The safe-coverage-gain claim is weakened to MIXED if the shipped certificate rejects a sound declaration (`M-CERT-SOUND-COVERAGE < 1.0`). Any control/validity gate failing (`PC-CERT-ADMITS-SOUND`, `PC-CERT-REFUSES-OVERWIDE`, `PC-CERT-REFUSES-UNDER`, `PC-INGEST-ABSTAIN`, `PC-UNSAFE-RAW`, `NC-REJECT-ALL`, `B-SHIPPED`, `B-DECLARED-FULL`, `BP-EVASION-CERT-PASS`, `M-REGRESSION`, `M-INSTALL-POST`, `M-CARRIER-PRE`, `V8_FREEZE_BINDING`) is `MEASUREMENT_INVALID`, never a negative scientific result.

## 3. Treatment, baselines and controls (stable ids)

`T-CERT-GUARD` — the shipped `src/spider/kernel.py` (`ingest_declaration` + module-level `certify_declaration`), called with the frozen audited negative bank `CERT_NEG`.

Declaration regimes (frozen): `R-SOUND` (each family's true declared grammar), `R-OVERWIDE` (`^<prefix>.*$`, training-consistent but unsound — the parent BP-DECL-OVERWIDE regime), `R-EVASION` (`^(?:<true inner>|<held-out negative>)$`, certificate-passing but unsound), `R-UNDER` (`^<first training value>$`, too narrow).

- `B-SHIPPED` — induced conservative supports; safety floor (FA=0, coverage 0.6750). Same value/logic as the parent's frozen `EXPECTED_SHIPPED`.
- `C-TRAINING-GATE` — the parent `declared_guard_support` comparator (adopt iff every training value fullmatches the declaration). Under `R-OVERWIDE` it must over-accept (`M-GATE-OVERWIDE-FALSE-ACCEPT-COUNT >= 1`, expected 201).
- `B-DECLARED-FULL` — raw declared grammar under `R-SOUND`; safe+complete ceiling (FA=0, coverage 1.0).
- `A-RAW-DECL` — unconditional adoption of the regime declaration, no guard; ablation proving the over-wide declaration's unsoundness is intrinsic.
- `PC-CERT-ADMITS-SOUND` / `PC-CERT-REFUSES-OVERWIDE` / `PC-CERT-REFUSES-UNDER` — positive controls on the real certificate decision.
- `PC-INGEST-ABSTAIN` — on refusal the mechanism keeps the shipped inferred support and records `declaration_certificate.status == "REFUSED"`.
- `PC-UNSAFE-RAW` — `A-RAW-DECL` under `R-OVERWIDE` over-accepts.
- `NC-REJECT-ALL` — empty registry accepts nothing and issues no HTTP.
- `BP-EVASION-CERT-PASS` — boundary probe: the certificate admits `R-EVASION` and the arm false-accepts; establishes the closed-world limit.
- `PC-EXACT-REPLAY`, `PC-DETERMINISM-REPEAT`, `M-REGRESSION`, `M-CARRIER-PRE`, `M-INSTALL-POST`, `M-SUPPORT-IDENTITY`, `V8_FREEZE_BINDING`, `B-LITERAL-KERNEL`.

## 4. Decision rule (frozen)

Validity/control gates must all PASS: `V8_FREEZE_BINDING`, `M-CARRIER-PRE`, `M-INSTALL-POST`, `M-REGRESSION`, `PC-DETERMINISM-REPEAT`, `PC-EXACT-REPLAY`, `B-LITERAL-KERNEL`, `M-SUPPORT-IDENTITY`, `PC-CERT-ADMITS-SOUND`, `PC-CERT-REFUSES-OVERWIDE`, `PC-CERT-REFUSES-UNDER`, `PC-INGEST-ABSTAIN`, `PC-UNSAFE-RAW`, `B-SHIPPED`, `B-DECLARED-FULL`, `NC-REJECT-ALL`, `PC-DISCRIMINATION`, `BP-EVASION-CERT-PASS`. Otherwise `status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`.

On validity:
- `FALSIFIES` if any safety invariant is violated in `T-CERT-GUARD` under `R-SOUND` or `R-OVERWIDE` (false accepts / HTTP-on-OUT / executed refusals).
- `SUPPORTS` if `M-CERT-SOUND-FALSE-ACCEPT-COUNT=0`, `M-CERT-SOUND-COVERAGE=1.0`, `M-CERT-OVERWIDE-FALSE-ACCEPT-COUNT=0`, and `M-GATE-OVERWIDE-FALSE-ACCEPT-COUNT>=1` (strict discrimination).
- `MIXED` otherwise (safe but coverage < 1.0 under the sound declaration).

Claim status: the frozen `spec.json#decision_rule` mandates `C-PARAM-INHERIT` RETAINED at EXPERIMENTAL in all branches; no promotion is authorized by this packet.

## 5. Adversarial / partially-observable declaration test

`R-OVERWIDE` is the partially-observable over-wide declaration: it is consistent with every observed training value yet admits out-of-grammar identifiers. `R-EVASION` is the adversarial declaration that passes the certificate because its single over-accept (`HELDOUT`) is withheld from the audited bank; it makes the closed-world boundary operational and is a required, expected-positive boundary control, not the overall falsifier. `CERT_NEG` is deterministic: for each family every frozen payload-class value and every `out_wrong_subrange` value that the true declared grammar rejects, excluding exactly the one held-out blind spot. The bank construction is re-derived in the runner, so the audited bank identity is bound by the prereg hash.

## 6. Sandboxed satisfiability evidence (DESIGN probe, non-outcome-bearing)

DESIGN ran the runner in `EXP_PROBE_MODE=1` before freeze (hermetic temp package, repo untouched) and observed: `R-SOUND` `T-CERT-GUARD` FA=0 coverage=1.0; `R-OVERWIDE` `T-CERT-GUARD` FA=0 coverage=0.675 (refused) vs `C-TRAINING-GATE` FA=201 (reproduces the recorded parent boundary); `R-EVASION` certificate admitted with FA=7; `R-UNDER` refused; `B-SHIPPED` FA=0 coverage=0.675; regression 3/3. These are satisfiability checks, not the frozen measurement.

## 7. Frozen installed kernel and runner

The installed kernel is the exact `POST_KERNEL` block below; EXECUTE materializes it, verifies sha256 `3a6caf97…`, and writes it to `src/spider/kernel.py` (pre-state must be the carrier `718efa6a…`, or the post-state for an idempotent re-run). `src/spider/kernel.py` is deliberately **not** in `freeze_artifacts` because it is the treatment object; its identity is pinned by the two sha256 constants and, in EXECUTE, by the written file. The deterministic runner in the `FROZEN RUNNER` block contains no outcome-conditioned branching.

<!-- BEGIN POST_KERNEL -->
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


def certify_declaration(declaration: str, positives: list[Any], negatives: list[Any]) -> tuple[bool, str]:
    """Closed-world certificate for an ingested applicability grammar.

    A declared grammar may be adopted in place of the inferred parameter support
    only when it is a valid regular expression that (1) accepts every observed
    training positive and (2) rejects every value in the audited negative bank.
    The certificate is deliberately CLOSED-WORLD: it bounds a declaration to the
    audited negatives and is not a general proof that the declaration's accept set
    equals the true admissible set, so callers must keep the audited bank under
    change control and prefer abstention over execution for uncertified values.
    """
    if not isinstance(declaration, str) or not declaration:
        return False, "declaration is not a non-empty string"
    try:
        pattern = re.compile(declaration)
    except re.error as exc:
        return False, "declaration is not a valid regex: " + str(exc)
    for value in positives:
        if pattern.fullmatch(str(value)) is None:
            return False, "declaration rejects a training positive"
    for value in negatives:
        if pattern.fullmatch(str(value)) is not None:
            return False, "declaration accepts an audited negative"
    return True, "certified against the audited negative bank"


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

    def ingest_declaration(
        self,
        mechanism: Mechanism,
        declaration: str,
        positives: list[Any],
        negative_bank: list[Any],
        slot: str,
    ) -> Mechanism:
        """Adopt an ingested declared grammar only when it passes the closed-world
        certificate; otherwise keep the conservative inferred supports.

        On certificate success the named slot's support is replaced by the declared
        grammar (safe widening of the applicability boundary).  On failure the
        inferred supports are preserved unchanged and the failed certificate is
        recorded on the mechanism, so resolution keeps the shipped conservative
        boundary and abstains (UNKNOWN/EXPLORE) instead of executing a value the
        uncertified declaration cannot justify.
        """
        certified, reason = certify_declaration(declaration, positives, negative_bank)
        rule = dict(mechanism.verification_rule or {})
        supports = dict(rule.get("parameter_supports", {}))
        rule["declaration_certificate"] = {
            "status": "CERTIFIED" if certified else "REFUSED",
            "reason": reason,
            "slot": slot,
        }
        if certified:
            supports[slot] = declaration
        rule["parameter_supports"] = supports
        mechanism.verification_rule = rule
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
<!-- END POST_KERNEL -->

<!-- BEGIN FROZEN RUNNER -->
"""FROZEN RUNNER — EXP-PRODUCT-38205292822.

Ship the ingested-declared-grammar applicability guard as REAL code in
src/spider/kernel.py with a closed-world declaration-soundness certificate, and
measure safety/coverage across four frozen declaration regimes on the frozen
seven-family bank.  Deterministic, stdlib-only, credential-free, no external
network (loopback oracle only).  Probe mode (EXP_PROBE_MODE=1) materializes the
post kernel in a temp package instead of touching the repo and records
UNBOUND-RUN for V8 when freeze.json is absent.
"""
from __future__ import annotations

import copy
import hashlib
import http.server
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

# -- canonical identities (mirrors prereg CANONICAL-HASHES) --
CARRIER_BLOB = "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796"
CARRIER_SHA256 = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
POST_SHA256 = "3a6caf970f5c86db19419f7ae57c7125f409eceba922eb2d5a9f5964140bb1b3"
EXPERIMENT_ID = "EXP-PRODUCT-38205292822"
EXP_DIR = "research/experiments/EXP-PRODUCT-38205292822"
EXPECTED_MIN_CONFIDENCE = 0.8
COARSE = "__COARSE__"

# -- frozen seven-family bank (byte-identical reproduction of the parent bank) --
FAMILIES = [
    {"fam": "A", "intent": "read_item", "resource": "item", "id_prefix": "item",
     "declared": r"^item\-[0-9]{3}$",
     "train": ["item-001", "item-002", "item-003", "item-004", "item-005"],
     "in_extra": ["item-000", "item-006", "item-007", "item-010", "item-042",
                  "item-099", "item-100", "item-123", "item-256", "item-500", "item-999"],
     "out_wrong_subrange": []},
    {"fam": "B", "intent": "read_account", "resource": "account", "id_prefix": "acct",
     "declared": r"^acct\-[0-9]{4}$",
     "train": ["acct-0001", "acct-0002", "acct-0003", "acct-0004", "acct-0005"],
     "in_extra": ["acct-0006", "acct-0007", "acct-0010", "acct-0042", "acct-0099",
                  "acct-0100", "acct-0123", "acct-0256", "acct-0500", "acct-0999",
                  "acct-1000", "acct-9999"],
     "out_wrong_subrange": []},
    {"fam": "C", "intent": "read_doc", "resource": "doc", "id_prefix": "doc",
     "declared": r"^doc\-[0-9]{1,4}$",
     "train": ["doc-01", "doc-02", "doc-03", "doc-04", "doc-05"],
     "in_extra": ["doc-0", "doc-1", "doc-9", "doc-10", "doc-11", "doc-99",
                  "doc-100", "doc-123", "doc-999", "doc-1000", "doc-9999"],
     "out_wrong_subrange": []},
    {"fam": "D", "intent": "read_region", "resource": "region", "id_prefix": "region",
     "declared": r"^region\-00[0-9]$",
     "train": ["region-000", "region-001", "region-002", "region-003", "region-004",
               "region-005", "region-006", "region-007", "region-008", "region-009"],
     "in_extra": [],
     "out_wrong_subrange": ["region-010", "region-011", "region-042", "region-099",
                            "region-100", "region-123", "region-256", "region-500",
                            "region-999"]},
    {"fam": "E", "intent": "read_invoice", "resource": "invoice", "id_prefix": "invoice",
     "declared": r"^invoice\-[0-9]{4}$",
     "train": ["invoice-0001", "invoice-0002", "invoice-0003", "invoice-0004",
               "invoice-0005"],
     "in_extra": ["invoice-0000", "invoice-0006", "invoice-0042", "invoice-0099",
                  "invoice-0100", "invoice-0500", "invoice-0999", "invoice-1000",
                  "invoice-1234", "invoice-9999"],
     "out_wrong_subrange": []},
    {"fam": "F", "intent": "read_case", "resource": "case", "id_prefix": "case",
     "declared": r"^case\-z[a-z]{2}$",
     "train": ["case-zab", "case-zcd", "case-zef", "case-zgh", "case-zij"],
     "in_extra": ["case-zaa", "case-zmn", "case-zop", "case-zqr", "case-zzy",
                  "case-zzz"],
     "out_wrong_subrange": ["case-aab", "case-bcd", "case-xyz", "case-0ab",
                            "case-za", "case-zz11"]},
    {"fam": "G", "intent": "read_token", "resource": "token", "id_prefix": "token",
     "declared": r"^token\-ab[a-z]$",
     "train": ["token-aba", "token-abb", "token-abc", "token-abd", "token-abe",
               "token-abf", "token-abg", "token-abh", "token-abi", "token-abj",
               "token-abk", "token-abl", "token-abm", "token-abn", "token-abo",
               "token-abp", "token-abq", "token-abr", "token-abs", "token-abt",
               "token-abu", "token-abv", "token-abw", "token-abx", "token-aby",
               "token-abz"],
     "in_extra": ["token-abb"],
     "out_wrong_subrange": ["token-aaa", "token-aac", "token-bbb", "token-xyz",
                            "token-zzz"]},
]
FAM_BY_ID = {f["fam"]: f for f in FAMILIES}
FAM_ORDER = [f["fam"] for f in FAMILIES]

EXPECTED_SHIPPED = {
    "A": r"^item\-00[0-9]{1}$", "B": r"^acct\-000[0-9]{1}$",
    "C": r"^doc\-0[0-9]{1}$", "D": r"^region\-00[0-9]{1}$",
    "E": r"^invoice\-000[0-9]{1}$", "F": r"^case\-z[a-z]{2}$",
    "G": r"^token\-ab[a-z]{1}$",
}
# -- four frozen declaration regimes --------------------------------
R_SOUND = {f["fam"]: f["declared"] for f in FAMILIES}
R_OVERWIDE = {f["fam"]: "^" + re.escape(f["id_prefix"]) + ".*$" for f in FAMILIES}
R_UNDER = {f["fam"]: "^" + re.escape(f["train"][0]) + "$" for f in FAMILIES}
# Held-out blind spot = one REAL bank value-grammar negative withheld from the
# audited bank (see prereg CERT-AUDIT); the evasion declaration is true|heldout.
HELDOUT = {"A": "item-abc", "B": "acct-abc", "C": "doc-abc", "D": "region-011",
           "E": "invoice-abc", "F": "case-aab", "G": "token-aaa"}
R_EVASION = {f["fam"]: "^(?:" + f["declared"][1:-1] + "|" + re.escape(HELDOUT[f["fam"]]) + ")$"
             for f in FAMILIES}

PAYLOAD_CLASSES = [
    ("LEN-TOO-SHORT1", lambda p, v: p + "-0"),
    ("LEN-TOO-SHORT2", lambda p, v: p + "-00"),
    ("LEN-TOO-LONG1", lambda p, v: p + "-" + "0" * 4),
    ("LEN-TOO-LONG2", lambda p, v: p + "-" + "0" * 5),
    ("LEN-TOO-LONG3", lambda p, v: p + "-" + "0" * 6),
    ("ALPHA-TAIL", lambda p, v: p + "-00a"),
    ("ALPHA-ALL", lambda p, v: p + "-abc"),
    ("ALPHA-HEAD", lambda p, v: p + "-a00"),
    ("HEX", lambda p, v: p + "-0x1"),
    ("CASE-UP", lambda p, v: p.upper() + "-000"),
    ("CASE-TITLE", lambda p, v: p.capitalize() + "-000"),
    ("SEP-US", lambda p, v: p + "_000"),
    ("SEP-DOT", lambda p, v: p + ".000"),
    ("SEP-COLON", lambda p, v: p + ":000"),
    ("SEP-SLASH", lambda p, v: p + "/000"),
    ("WS-EMPTY", lambda p, v: ""),
    ("WS-SPACE", lambda p, v: " "),
    ("WS-TAB", lambda p, v: "\t"),
    ("WS-NL", lambda p, v: "\n"),
    ("WS-TRAIL", lambda p, v: v + " "),
    ("WS-LEAD", lambda p, v: " " + v),
    ("INJ-SEMI", lambda p, v: v + ";x"),
    ("INJ-SQ", lambda p, v: v + "'"),
    ("INJ-DQ", lambda p, v: v + '"'),
    ("INJ-NUL", lambda p, v: v + "\x00"),
    ("INJ-TRAV", lambda p, v: "../../etc/passwd"),
    ("INJ-ABS", lambda p, v: "/api/" + p + "s/" + v),
    ("INJ-URL", lambda p, v: "http://evil.example/" + v),
    ("INJ-DOTDOT", lambda p, v: v + "/../secret"),
    ("QRY", lambda p, v: v + "?x=1"),
    ("FRAG", lambda p, v: v + "#frag"),
    ("PCT", lambda p, v: v.replace("0", "%30", 1)),
    ("UNI-AR", lambda p, v: p + "-00\u0663"),
    ("UNI-FW", lambda p, v: p + "-00\uff10"),
    ("OTH-USER", lambda p, v: "user-000"),
    ("OTH-ORDER", lambda p, v: "order-000"),
    ("OTH-CAT", lambda p, v: p + "x000"),
    ("BIG-1000", lambda p, v: p + "-" + "0" * 1000),
    ("BIG-64", lambda p, v: p + "-" + "9" * 64),
]
TYPE_PAYLOADS = [None, 0, 0.0, True, False, [], ["X"], {}, {"id": "X"}, b"X"]

# Audited negative bank classes: every class value that the family's TRUE
# declared grammar rejects becomes an audited negative, EXCEPT the single
# held-out blind-spot value (which must remain a real bank negative).
CERT_NEG_CLASSES = [
    "LEN-TOO-SHORT1", "LEN-TOO-SHORT2", "LEN-TOO-LONG1", "LEN-TOO-LONG2",
    "LEN-TOO-LONG3", "ALPHA-TAIL", "ALPHA-HEAD", "HEX", "SEP-US", "SEP-DOT",
    "SEP-COLON", "SEP-SLASH", "INJ-TRAV", "INJ-ABS", "INJ-URL", "INJ-DOTDOT",
    "QRY", "FRAG", "BIG-64", "BIG-1000", "UNI-AR", "UNI-FW", "CASE-UP",
    "CASE-TITLE", "OTH-USER", "OTH-ORDER", "OTH-CAT", "PCT", "WS-EMPTY",
    "WS-SPACE", "WS-TAB", "WS-NL", "WS-TRAIL", "WS-LEAD", "INJ-SEMI", "INJ-SQ",
    "INJ-DQ", "INJ-NUL",
]
_PK = dict(PAYLOAD_CLASSES)


def build_cert_neg():
    """Deterministic audited negative bank, keyed by family."""
    bank = {}
    for f in FAMILIES:
        fam = f["fam"]
        rx = re.compile(f["declared"])
        negs = []
        for cls in CERT_NEG_CLASSES:
            val = _PK[cls](f["id_prefix"], f["train"][0])
            if isinstance(val, str) and rx.fullmatch(val) is None and val != HELDOUT[fam]:
                negs.append(val)
        for w in f["out_wrong_subrange"]:
            if rx.fullmatch(w) is None and w != HELDOUT[fam]:
                negs.append(w)
        if HELDOUT[fam] in negs or rx.fullmatch(HELDOUT[fam]) is not None:
            raise RuntimeError("held-out blind spot is not a value-grammar negative for " + fam)
        bank[fam] = negs
    return bank


CERT_NEG = build_cert_neg()


def build_bank():
    bank = []
    for f in FAMILIES:
        ctx = {"resource_type": f["resource"], "authenticated": True}
        slot = f["resource"]
        v0 = f["train"][0]

        def add(bid, value, intent=None, context=None, params=None, _f=f, _slot=slot):
            bank.append({"bid": bid, "fam": _f["fam"], "value": value,
                         "intent": _f["intent"] if intent is None else intent,
                         "context": dict(ctx) if context is None else context,
                         "params": dict(params) if params is not None else {_slot: value}})

        for i, v in enumerate(f["in_extra"]):
            add("F%s-IN-E%02d" % (f["fam"], i), v)
        for i, v in enumerate(f["train"]):
            add("F%s-IN-T%02d" % (f["fam"], i), v)
        for name, fn in PAYLOAD_CLASSES:
            add("F%s-OG-%s" % (f["fam"], name), fn(f["id_prefix"], v0))
        for i, wv in enumerate(f["out_wrong_subrange"]):
            add("F%s-OG-WRONGRANGE%02d" % (f["fam"], i), wv)
        for i, val in enumerate(TYPE_PAYLOADS):
            add("F%s-OG-TYPE%02d" % (f["fam"], i), val)
        vv = f["train"][1]
        add("F%s-OG-CTX-USERTYPE" % f["fam"], vv, context={"resource_type": "other", "authenticated": True})
        add("F%s-OG-CTX-NOAUTH" % f["fam"], vv, context={"resource_type": f["resource"], "authenticated": False})
        add("F%s-OG-CTX-MISSING" % f["fam"], vv, context={"resource_type": f["resource"]})
        add("F%s-OG-CTX-EMPTY" % f["fam"], vv, context={})
        add("F%s-OG-CTX-INTENT" % f["fam"], vv, intent="delete_" + f["resource"])
        add("F%s-OG-CTX-WRONGKEY" % f["fam"], vv, params={"wrong_key": vv})
        add("F%s-OG-CTX-NOPARAM" % f["fam"], vv, params={})
    return bank


def label_of(item):
    f = FAM_BY_ID[item["fam"]]
    v = item["value"]
    if not isinstance(v, str):
        return "OUT"
    if re.fullmatch(f["declared"], v) is None:
        return "OUT"
    if item["intent"] != f["intent"]:
        return "OUT"
    if item["context"] != {"resource_type": f["resource"], "authenticated": True}:
        return "OUT"
    if item["params"] != {f["resource"]: v}:
        return "OUT"
    return "IN"


def value_repr(v):
    try:
        return json.dumps(v)
    except Exception:
        return repr(v)


def detect_repo_root() -> Path:
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "pyproject.toml").exists() and (p / "src/spider").exists():
            return p
        p = p.parent
    raise RuntimeError("repo root not found upward from runner")


REPO_ROOT = Path(os.environ.get("EXP_TARGET_ROOT") or str(detect_repo_root()))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_source(spec: str) -> bytes:
    if spec.startswith("git:"):
        out = subprocess.run(["git", "-C", str(REPO_ROOT), "cat-file", "blob", spec[4:]],
                             capture_output=True)
        if out.returncode != 0:
            raise RuntimeError("git blob unavailable: " + out.stderr.decode()[:200])
        return out.stdout
    if spec.startswith("file:"):
        return Path(spec[5:]).read_bytes()
    raise RuntimeError("unknown source spec: " + spec)


# --------------------------------------------------------------- loopback oracle
VALID_PATH_RES = {f["fam"]: re.compile("/api/" + f["resource"] + "s/" + f["declared"][1:])
                  for f in FAMILIES}


class OracleHandler(http.server.BaseHTTPRequestHandler):
    count = 0

    def do_GET(self):
        type(self).count += 1
        path = self.path.split("?", 1)[0]
        matched = next((fam for fam, rx in VALID_PATH_RES.items() if rx.fullmatch(path)), None)
        if matched is not None:
            ident = path.rsplit("/", 1)[-1]
            body = {"type": FAM_BY_ID[matched]["resource"], "id": ident, "data": "res:" + ident}
            self.send_response(200)
        else:
            body = {"error": "not_found", "path": path}
            self.send_response(404)
        payload = json.dumps(body).encode()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


def start_oracle():
    handler = type("Oracle", (OracleHandler,), {"count": 0})
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1], handler


def execute_action(bound):
    url = bound.get("url") if isinstance(bound, dict) else None
    if not isinstance(url, str):
        return None, {"exec_error": "no_url"}
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())
    except Exception as exc:
        return None, {"exec_error": type(exc).__name__ + ": " + str(exc)[:160]}


def drop_modules():
    for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
        sys.modules.pop(m, None)


def make_arm_registry(mechs, support_by_fam, tmpdir, tag):
    reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry
    reg = reg_cls(Path(tmpdir) / ("mechanisms_%s.jsonl" % tag))
    for fam in FAM_ORDER:
        m = copy.deepcopy(mechs[fam])
        if support_by_fam is not None:
            m.verification_rule = {"parameter_supports": {
                s: support_by_fam[fam] for s in m.parameter_slots}}
        reg.upsert(m)
    return reg


def evaluate(kernel, bank, handler):
    records = []
    for item in bank:
        http0 = handler.count
        rec = {"bid": item["bid"], "fam": item["fam"], "label": label_of(item),
               "value": value_repr(item["value"])}
        try:
            r = kernel.resolve(item["intent"], dict(item["context"]), dict(item["params"]))
            rec["status"] = r.status.value
            rec["reason"] = r.reason
            bound = r.bound_action
        except Exception as exc:
            rec["status"] = "RESOLVE_ERROR"
            rec["reason"] = type(exc).__name__ + ": " + str(exc)[:160]
            bound = None
        rec["bound"] = bound is not None
        ex_status, body, verify = None, None, None
        if bound is not None:
            ex_status, body = execute_action(bound)
            if ex_status == 200 and isinstance(body, dict):
                try:
                    verify = kernel.verify(item.get("_mech_id"), body, dict(item["params"]))
                except Exception:
                    verify = False
            elif ex_status is not None:
                verify = False
        rec["exec_status"] = ex_status
        rec["verify"] = verify
        rec["exec_error"] = body.get("exec_error") if isinstance(body, dict) else None
        rec["http_delta"] = handler.count - http0
        records.append(rec)
    return records


def _summarize(records):
    n_in = sum(1 for r in records if r["label"] == "IN")
    n_out = sum(1 for r in records if r["label"] == "OUT")
    accepts = [r for r in records if r["status"] == "EXECUTABLE"]
    fa = [r for r in records if r["label"] == "OUT" and r["status"] == "EXECUTABLE"]
    sfa = [r for r in fa if r["exec_status"] == 200 and r["verify"] is True]
    fr = [r for r in records if r["label"] == "IN" and r["status"] != "EXECUTABLE"]
    http_out = sum(r["http_delta"] for r in records if r["label"] == "OUT")
    http_total = sum(r["http_delta"] for r in records)
    refusal_exec = sum(1 for r in records
                       if r["label"] == "OUT" and r["status"] != "EXECUTABLE"
                       and r["http_delta"] > 0)
    cov = (n_in - len(fr)) / n_in if n_in else None
    return {
        "n_in": n_in, "n_out": n_out, "accept_count": len(accepts),
        "false_accept_count": len(fa), "silent_false_accept_count": len(sfa),
        "false_reject_count": len(fr), "coverage": cov,
        "http_on_out_label": http_out, "http_total": http_total,
        "refusal_executed_count": refusal_exec,
        "false_accept_bids": [r["bid"] for r in fa],
        "silent_false_accept_bids": [r["bid"] for r in sfa],
        "false_reject_bids": [r["bid"] for r in fr],
    }


def summarize(records):
    out = _summarize(records)
    out["per_family"] = {}
    for fam in FAM_ORDER:
        sub = [r for r in records if r["fam"] == fam]
        out["per_family"][fam] = _summarize(sub)
    return out


# --------------------------------------------------------------- V8 freeze bind
def _extract(text, name):
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END "
                  + re.escape(name) + r" -->", text, re.S)
    if not m:
        raise RuntimeError("block %s not found in prereg.md" % name)
    return m.group(1)


def v8_freeze_binding(result):
    probe = os.environ.get("EXP_PROBE_MODE") == "1"
    exp = REPO_ROOT / EXP_DIR
    freeze_path = exp / "freeze.json"
    if not freeze_path.exists():
        if probe:
            result["observations"].append({"type": "binding",
                                           "V8": "UNBOUND-RUN: no freeze.json (probe mode only)."})
            result["certificate"]["V8_FREEZE_BINDING"] = {
                "status": "PASS", "prereg_sha_matches": None,
                "runner_source_matches_frozen_block": None, "artifact_hashes_match": None,
                "reason": "UNBOUND-RUN (probe mode only): no freeze.json; satisfiability probe"}
            return True
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "freeze.json missing at %s (EXECUTE mode)" % freeze_path}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    try:
        freeze = json.loads(freeze_path.read_text())

        def norm(s):
            return s.replace("\r\n", "\n").rstrip()

        prereg_b = (exp / "prereg.md").read_bytes()
        block = _extract(prereg_b.decode("utf-8"), "FROZEN RUNNER")
        this_src = Path(__file__).resolve().read_text(encoding="utf-8")
        ok_a = hashlib.sha256(prereg_b).hexdigest() == freeze["hashes"]["prereg.md"]
        ok_b = norm(this_src) == norm(block)
        ok_c = all(hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest() == h
                   for rel, h in freeze.get("artifact_hashes", {}).items())
    except Exception as exc:
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID", "reason": "freeze binding unreadable: " + str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    ok_all = ok_a and ok_b and ok_c
    result["certificate"]["V8_FREEZE_BINDING"] = {
        "status": "PASS" if ok_all else "FAIL", "prereg_sha_matches": ok_a,
        "runner_source_matches_frozen_block": ok_b, "artifact_hashes_match": ok_c,
        "reason": "hash-bound prereg; running source == FROZEN RUNNER block; freeze artifacts intact"}
    if not ok_all:
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    return True


def post_kernel_bytes():
    """Materialize the frozen post-change kernel from the POST_KERNEL block."""
    exp = REPO_ROOT / EXP_DIR
    text = (exp / "prereg.md").read_text(encoding="utf-8")
    body = _extract(text, "POST_KERNEL")
    return (body + "\n").encode("utf-8")


# -------------------------------------------------------------------- one run
def run_once(carrier_cls, counters_cls, reg_cls, obs_cls):
    server, port, handler = start_oracle()
    try:
        tmp = tempfile.mkdtemp(prefix="exp38205292822_")
        reg_cls(Path(tmp) / "base.jsonl")
        mechs = {}
        identity = {}
        for f in FAMILIES:
            obs = []
            for ident in f["train"]:
                url = "http://127.0.0.1:%d/api/%ss/%s" % (port, f["resource"], ident)
                st, body = execute_action({"url": url})
                if st != 200:
                    raise RuntimeError("induction GET %s -> %s" % (ident, st))
                obs.append(obs_cls(intent=f["intent"],
                                   state={"resource_type": f["resource"], "authenticated": True},
                                   action={"method": "GET", "url": url},
                                   next_state=body, success=True,
                                   provenance={"exp": EXPERIMENT_ID, "role": "induction"}))
            reg = reg_cls(Path(tmp) / ("base_%s.jsonl" % f["fam"]))
            kernel = carrier_cls(reg, counters=counters_cls())
            m = kernel.distill_parameterized(obs)
            if m is None:
                raise RuntimeError("distill_parameterized returned None for fam " + f["fam"])
            reg.upsert(m)
            mechs[f["fam"]] = m
            identity[f["fam"]] = {"slots": list(m.parameter_slots),
                                  "support": m.verification_rule["parameter_supports"],
                                  "confidence": m.confidence}

        bank = build_bank()
        ids = [b["bid"] for b in bank]
        if len(ids) != len(set(ids)):
            raise RuntimeError("duplicate bank bids")
        for it in bank:
            it["_mech_id"] = mechs[it["fam"]].mechanism_id

        shipped = {fam: mechs[fam].verification_rule["parameter_supports"][FAM_BY_ID[fam]["resource"]]
                   for fam in FAM_ORDER}
        for fam in FAM_ORDER:
            if shipped[fam] != EXPECTED_SHIPPED[fam]:
                raise RuntimeError("shipped support drift fam %s: %s" % (fam, shipped[fam]))

        # -- certificate arm: real shipped ingest_declaration code path --
        def cert_arm(regime, tag):
            supports = {}
            status = {}
            abstain = {}
            for fam in FAM_ORDER:
                m = copy.deepcopy(mechs[fam])
                reg2 = reg_cls(Path(tmp) / ("cert_%s_%s.jsonl" % (tag, fam)))
                k = carrier_cls(reg2, counters=counters_cls())
                k.ingest_declaration(m, regime[fam], list(FAM_BY_ID[fam]["train"]),
                                     CERT_NEG[fam], FAM_BY_ID[fam]["resource"])
                sup = m.verification_rule["parameter_supports"][FAM_BY_ID[fam]["resource"]]
                st = m.verification_rule["declaration_certificate"]["status"]
                supports[fam] = sup
                status[fam] = st
                abstain[fam] = (sup == shipped[fam]) if st == "REFUSED" else None
            return supports, status, abstain

        # -- parent training-consistency gate comparator --
        def gate_arm(regime):
            supports = {}
            for fam in FAM_ORDER:
                rx = re.compile(regime[fam])
                vals = FAM_BY_ID[fam]["train"]
                consistent = bool(vals) and all(rx.fullmatch(v) is not None for v in vals)
                supports[fam] = regime[fam] if consistent else shipped[fam]
            return supports

        def arm(support_by_fam, tag):
            reg = make_arm_registry(mechs, support_by_fam, tmp, tag)
            k = carrier_cls(reg, counters=counters_cls())
            return summarize(evaluate(k, bank, handler))

        regimes = [("R-SOUND", R_SOUND), ("R-OVERWIDE", R_OVERWIDE),
                   ("R-EVASION", R_EVASION), ("R-UNDER", R_UNDER)]
        cert_support = {}
        cert_status = {}
        cert_abstain = {}
        for rname, regime in regimes:
            s, st, ab = cert_arm(regime, rname)
            cert_support[rname] = s
            cert_status[rname] = st
            cert_abstain[rname] = ab

        arms = {}
        for rname, regime in regimes:
            arms[rname] = {
                "T-CERT-GUARD": arm(cert_support[rname], "cert_" + rname),
                "C-TRAINING-GATE": arm(gate_arm(regime), "gate_" + rname),
                "A-RAW-DECL": arm(regime, "raw_" + rname),
            }
        shipped_rec = arm(None, "shipped")
        arms["R-SOUND"]["B-SHIPPED"] = shipped_rec
        arms["R-OVERWIDE"]["B-SHIPPED"] = shipped_rec
        declared_full = arm(R_SOUND, "declared_full")
        arms["R-SOUND"]["B-DECLARED-FULL"] = declared_full

        empty_reg = reg_cls(Path(tmp) / "reg_empty.jsonl")
        nc_recs = evaluate(carrier_cls(empty_reg, counters=counters_cls()), bank, handler)

        replay = []
        for f in FAMILIES:
            for ident in f["train"]:
                r = carrier_cls(reg_cls(Path(tmp) / ("base_%s.jsonl" % f["fam"])),
                                counters=counters_cls()).resolve(
                    f["intent"], {"resource_type": f["resource"], "authenticated": True},
                    {f["resource"]: ident})
                replay.append({"fam": f["fam"], "id": ident, "status": r.status.value})

        return {
            "mechanism_identity": identity,
            "shipped_support": shipped,
            "cert_status": cert_status,
            "cert_abstain_preserved": cert_abstain,
            "arms": arms,
            "nc_reject_all": summarize(nc_recs),
            "pc_exact_replay": {"status": "PASS" if all(x["status"] == "EXECUTABLE"
                                                        for x in replay) else "FAIL",
                                "replay": replay},
        }
    finally:
        server.shutdown()


def main():
    result = {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": "product",
              "certificate": {}, "identities": {}, "observations": [], "unresolved": []}
    if not v8_freeze_binding(result):
        return result

    probe = os.environ.get("EXP_PROBE_MODE") == "1"
    kernel_path = REPO_ROOT / "src/spider/kernel.py"

    # ---- P0 identity baseline + P1/P2 install or hermetic materialization ----
    try:
        pre = sha256_bytes(kernel_path.read_bytes())
        result["identities"]["pre_install_sha256"] = pre
        if pre not in (CARRIER_SHA256, POST_SHA256):
            raise RuntimeError("pre-state kernel %s is neither carrier nor post" % pre)
        post_bytes = post_kernel_bytes()
        post = sha256_bytes(post_bytes)
        result["identities"]["post_materialized_sha256"] = post
        if post != POST_SHA256:
            raise RuntimeError("materialized kernel sha %s != frozen POST_SHA256" % post)
        if probe:
            temp_dir = tempfile.mkdtemp(prefix="exp38205292822_pkg_")
            pkg = Path(temp_dir) / "spider"
            pkg.mkdir(parents=True)
            for name in ("models.py", "registry.py", "__init__.py"):
                (pkg / name).write_bytes((REPO_ROOT / "src/spider" / name).read_bytes())
            (pkg / "kernel.py").write_bytes(post_bytes)
            sys.path.insert(0, temp_dir)
            imported_from = str(pkg)
        else:
            kernel_path.write_bytes(post_bytes)
            installed = sha256_bytes(kernel_path.read_bytes())
            if installed != POST_SHA256:
                raise RuntimeError("installed kernel sha %s != frozen POST_SHA256" % installed)
            sys.path.insert(0, str(REPO_ROOT / "src"))
            imported_from = str(kernel_path)
        drop_modules()
        spider = __import__("spider")
        Carrier = spider.SpiderKernel
        obs_cls = spider.Observation
        counters_cls = __import__("spider.kernel", fromlist=["TrajectoryCounters"]).TrajectoryCounters
        reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry
        min_conf = Carrier.__init__.__defaults__[0]
        if min_conf != EXPECTED_MIN_CONFIDENCE:
            raise RuntimeError("shipped min_confidence default %s != %s"
                               % (min_conf, EXPECTED_MIN_CONFIDENCE))
        result["identities"]["imported_from"] = imported_from
        result["certificate"]["M-CARRIER-PRE"] = {
            "status": "PASS",
            "reason": "pre-state src/spider/kernel.py == frozen carrier %s" % CARRIER_SHA256}
        result["certificate"]["M-INSTALL-POST"] = {
            "status": "PASS",
            "reason": "installed/materialized kernel sha256 == frozen POST_SHA256 %s" % POST_SHA256}
    except Exception as exc:
        result["certificate"]["M-INSTALL-POST"] = {
            "status": "MEASUREMENT_INVALID", "reason": "kernel install/materialize failed: " + str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result

    # -- B-LITERAL-KERNEL ablation (inherited id): the pre-promotion literal
    #    lacks distill_parameterized, so it cannot construct the mechanism.
    try:
        lit = read_source("git:cfec98660b0277ccbf295e8a4119e8d81ddccf50")
        with tempfile.TemporaryDirectory() as td:
            pkg = Path(td) / "spider"
            pkg.mkdir(parents=True)
            for name in ("models.py", "registry.py", "__init__.py"):
                (pkg / name).write_bytes((REPO_ROOT / "src/spider" / name).read_bytes())
            (pkg / "kernel.py").write_bytes(lit)
            saved = list(sys.path)
            sys.path.insert(0, td)
            drop_modules()
            litpkg = __import__("spider")
            has_param = hasattr(litpkg.SpiderKernel, "distill_parameterized")
            sys.path[:] = saved
            drop_modules()
        result["certificate"]["B-LITERAL-KERNEL"] = {
            "status": "PASS" if not has_param else "FAIL",
            "has_distill_parameterized": has_param,
            "reason": "pre-promotion literal kernel lacks distill_parameterized"}
    except Exception as exc:
        result["certificate"]["B-LITERAL-KERNEL"] = {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result

    # -- re-import the installed/materialized carrier (ablation swapped sys.path) --
    drop_modules()
    if probe:
        sys.path.insert(0, imported_from.rsplit("/spider", 1)[0])
    spider = __import__("spider")
    Carrier = spider.SpiderKernel
    obs_cls = spider.Observation
    counters_cls = __import__("spider.kernel", fromlist=["TrajectoryCounters"]).TrajectoryCounters
    reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry

    run1 = run_once(Carrier, counters_cls, reg_cls, obs_cls)
    run2 = run_once(Carrier, counters_cls, reg_cls, obs_cls)
    det = (json.dumps(run1["arms"], sort_keys=True, default=repr)
           == json.dumps(run2["arms"], sort_keys=True, default=repr)
           and run1["mechanism_identity"] == run2["mechanism_identity"]
           and run1["shipped_support"] == run2["shipped_support"]
           and run1["cert_status"] == run2["cert_status"])
    result["certificate"]["PC-DETERMINISM-REPEAT"] = {
        "status": "PASS" if det else "FAIL",
        "reason": "two independent runs produce identical arm metrics, certificate decisions and identity"}

    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test_*.py")
    tr = unittest.TextTestRunner(verbosity=0).run(suite)
    result["certificate"]["M-REGRESSION"] = {
        "status": "PASS" if (tr.wasSuccessful() and tr.testsRun >= 3) else "FAIL",
        "tests_run": tr.testsRun, "failures": len(tr.failures), "errors": len(tr.errors)}

    g = run1["arms"]
    d_sound = g["R-SOUND"]["T-CERT-GUARD"]
    d_over = g["R-OVERWIDE"]["T-CERT-GUARD"]
    gate_over = g["R-OVERWIDE"]["C-TRAINING-GATE"]
    raw_over = g["R-OVERWIDE"]["A-RAW-DECL"]
    d_ev = g["R-EVASION"]["T-CERT-GUARD"]
    d_under = g["R-UNDER"]["T-CERT-GUARD"]
    s = g["R-SOUND"]["B-SHIPPED"]
    dfull = g["R-SOUND"]["B-DECLARED-FULL"]
    nc = run1["nc_reject_all"]

    result["certificate"]["M-SUPPORT-IDENTITY"] = {
        "status": "PASS" if run1["shipped_support"] == EXPECTED_SHIPPED else "FAIL",
        "shipped": run1["shipped_support"],
        "reason": "induced shipped supports match frozen DESIGN constants"}
    result["certificate"]["PC-CERT-ADMITS-SOUND"] = {
        "status": "PASS" if all(st == "CERTIFIED" for st in run1["cert_status"]["R-SOUND"].values()) else "FAIL",
        "status_by_family": run1["cert_status"]["R-SOUND"],
        "reason": "certificate admits the sound declared grammar for every family"}
    result["certificate"]["PC-CERT-REFUSES-OVERWIDE"] = {
        "status": "PASS" if all(st == "REFUSED" for st in run1["cert_status"]["R-OVERWIDE"].values()) else "FAIL",
        "status_by_family": run1["cert_status"]["R-OVERWIDE"],
        "reason": "certificate refuses the training-consistent over-wide declaration for every family"}
    result["certificate"]["PC-CERT-REFUSES-UNDER"] = {
        "status": "PASS" if all(st == "REFUSED" for st in run1["cert_status"]["R-UNDER"].values()) else "FAIL",
        "status_by_family": run1["cert_status"]["R-UNDER"],
        "reason": "certificate is not a rubber stamp: a too-narrow declaration is refused"}
    result["certificate"]["PC-INGEST-ABSTAIN"] = {
        "status": "PASS" if all(v is True for v in run1["cert_abstain_preserved"]["R-OVERWIDE"].values()) else "FAIL",
        "abstain_preserved_by_family": run1["cert_abstain_preserved"]["R-OVERWIDE"],
        "reason": "on refusal the shipped inferred support is preserved unchanged"}
    result["certificate"]["PC-UNSAFE-RAW"] = {
        "status": "PASS" if raw_over["false_accept_count"] >= 1 else "FAIL",
        "false_accept_count": raw_over["false_accept_count"],
        "reason": "positive control: unconditional adoption of the over-wide declaration over-accepts"}
    result["certificate"]["B-SHIPPED"] = {
        "status": "PASS" if s["false_accept_count"] == 0 else "FAIL",
        "false_accept_count": s["false_accept_count"], "false_reject_count": s["false_reject_count"],
        "coverage": s["coverage"], "http_on_out_label": s["http_on_out_label"],
        "per_family": s["per_family"], "reason": "shipped conservative supports (safety floor)"}
    result["certificate"]["B-DECLARED-FULL"] = {
        "status": "PASS" if (dfull["false_accept_count"] == 0 and dfull["coverage"] == 1.0) else "FAIL",
        "false_accept_count": dfull["false_accept_count"], "coverage": dfull["coverage"],
        "per_family": dfull["per_family"],
        "reason": "safe+complete support ceiling under the sound declaration"}
    result["certificate"]["NC-REJECT-ALL"] = {
        "status": "PASS" if (nc["accept_count"] == 0 and nc["http_total"] == 0) else "FAIL",
        "accept_count": nc["accept_count"], "http_total": nc["http_total"],
        "reason": "null floor: empty registry accepts nothing and issues no HTTP"}
    result["certificate"]["PC-EXACT-REPLAY"] = run1["pc_exact_replay"]

    result["certificate"]["T-CERT-GUARD-R-SOUND"] = {
        "status": "PASS" if (d_sound["false_accept_count"] == 0 and d_sound["coverage"] == 1.0
                             and d_sound["http_on_out_label"] == 0
                             and d_sound["refusal_executed_count"] == 0) else "FAIL",
        "false_accept_count": d_sound["false_accept_count"],
        "false_reject_count": d_sound["false_reject_count"], "coverage": d_sound["coverage"],
        "http_on_out_label": d_sound["http_on_out_label"],
        "refusal_executed_count": d_sound["refusal_executed_count"],
        "per_family": d_sound["per_family"],
        "reason": "PRIMARY: shipped certificate adopts the sound declaration; safe+complete"}
    result["certificate"]["T-CERT-GUARD-R-OVERWIDE"] = {
        "status": "PASS" if (d_over["false_accept_count"] == 0 and d_over["http_on_out_label"] == 0
                             and d_over["refusal_executed_count"] == 0) else "FAIL",
        "false_accept_count": d_over["false_accept_count"], "coverage": d_over["coverage"],
        "http_on_out_label": d_over["http_on_out_label"],
        "refusal_executed_count": d_over["refusal_executed_count"],
        "per_family": d_over["per_family"],
        "reason": "PRIMARY: shipped certificate refuses the over-wide declaration; holds the shipped boundary"}
    result["certificate"]["C-TRAINING-GATE-R-OVERWIDE"] = {
        "status": "PASS" if gate_over["false_accept_count"] >= 1 else "FAIL",
        "false_accept_count": gate_over["false_accept_count"],
        "false_accept_bids": gate_over["false_accept_bids"],
        "coverage": gate_over["coverage"], "per_family": gate_over["per_family"],
        "reason": "comparator: the parent training-consistency gate adopts the over-wide declaration"}
    result["certificate"]["PC-DISCRIMINATION"] = {
        "status": "PASS" if (d_over["false_accept_count"] == 0 and gate_over["false_accept_count"] >= 1) else "FAIL",
        "cert_false_accept_count": d_over["false_accept_count"],
        "gate_false_accept_count": gate_over["false_accept_count"],
        "reason": "the certificate strictly dominates the training-consistency gate on the audited over-wide class"}
    result["certificate"]["BP-EVASION-CERT-PASS"] = {
        "status": "PASS" if (all(st == "CERTIFIED" for st in run1["cert_status"]["R-EVASION"].values())
                             and d_ev["false_accept_count"] >= 1) else "FAIL",
        "certificate_admitted_by_family": run1["cert_status"]["R-EVASION"],
        "false_accept_count": d_ev["false_accept_count"],
        "false_accept_bids": d_ev["false_accept_bids"],
        "reason": "boundary: a certificate-passing but unsound declaration still yields false accepts; "
                  "the certificate is closed-world, not a general soundness proof"}
    result["certificate"]["R-UNDER-DETAIL"] = {
        "status": "PASS" if d_under["false_accept_count"] == 0 else "FAIL",
        "coverage": d_under["coverage"],
        "reason": "too-narrow declaration is refused and the shipped support is preserved"}

    validity_gates = ("V8_FREEZE_BINDING", "M-CARRIER-PRE", "M-INSTALL-POST", "M-REGRESSION",
                      "PC-DETERMINISM-REPEAT", "PC-EXACT-REPLAY", "B-LITERAL-KERNEL",
                      "M-SUPPORT-IDENTITY", "PC-CERT-ADMITS-SOUND", "PC-CERT-REFUSES-OVERWIDE",
                      "PC-CERT-REFUSES-UNDER", "PC-INGEST-ABSTAIN", "PC-UNSAFE-RAW",
                      "B-SHIPPED", "B-DECLARED-FULL", "NC-REJECT-ALL", "PC-DISCRIMINATION",
                      "BP-EVASION-CERT-PASS")
    failed = [k for k in validity_gates if result["certificate"][k]["status"] != "PASS"]
    if failed:
        result["status"], result["outcome"] = "MEASUREMENT_INVALID", "NOT_APPLICABLE"
        result["reason"] = "instrument/validity/control gates failed: " + ", ".join(failed)
        return result

    result["arms"] = g
    result["metrics"] = {
        "M-CERT-SOUND-FALSE-ACCEPT-COUNT": d_sound["false_accept_count"],
        "M-CERT-SOUND-HTTP-ON-OUT": d_sound["http_on_out_label"],
        "M-CERT-SOUND-REFUSAL-EXECUTED-COUNT": d_sound["refusal_executed_count"],
        "M-CERT-SOUND-COVERAGE": d_sound["coverage"],
        "M-CERT-SOUND-COVERAGE-BY-FAMILY": {f: d_sound["per_family"][f]["coverage"] for f in FAM_ORDER},
        "M-CERT-OVERWIDE-FALSE-ACCEPT-COUNT": d_over["false_accept_count"],
        "M-CERT-OVERWIDE-HTTP-ON-OUT": d_over["http_on_out_label"],
        "M-CERT-OVERWIDE-REFUSAL-EXECUTED-COUNT": d_over["refusal_executed_count"],
        "M-CERT-OVERWIDE-COVERAGE": d_over["coverage"],
        "M-GATE-OVERWIDE-FALSE-ACCEPT-COUNT": gate_over["false_accept_count"],
        "M-RAW-OVERWIDE-FALSE-ACCEPT-COUNT": raw_over["false_accept_count"],
        "M-CERT-EVASION-FALSE-ACCEPT-COUNT": d_ev["false_accept_count"],
        "M-CERT-EVASION-FALSE-ACCEPT-BIDS": d_ev["false_accept_bids"],
        "M-CERT-UNDER-COVERAGE": d_under["coverage"],
        "M-CERT-UNDER-FALSE-ACCEPT-COUNT": d_under["false_accept_count"],
        "M-B-SHIPPED-FALSE-ACCEPT-COUNT": s["false_accept_count"],
        "M-B-SHIPPED-COVERAGE": s["coverage"],
        "M-B-DECLARED-FULL-FALSE-ACCEPT-COUNT": dfull["false_accept_count"],
        "M-B-DECLARED-FULL-COVERAGE": dfull["coverage"],
        "M-COVERAGE-DELTA-VS-SHIPPED": (None if d_sound["coverage"] is None
                                        else d_sound["coverage"] - s["coverage"]),
        "M-REGRESSION-TESTS-RUN": result["certificate"]["M-REGRESSION"]["tests_run"],
        "M-REFUSAL-SEMANTICS-VIOLATIONS": (d_sound["refusal_executed_count"]
                                           + d_over["refusal_executed_count"]),
        "M-CERT-SOUND-ADOPTED-BY-FAMILY": run1["cert_status"]["R-SOUND"],
        "M-CERT-OVERWIDE-REFUSED-BY-FAMILY": run1["cert_status"]["R-OVERWIDE"],
        "M-CERT-EVASION-ADOPTED-BY-FAMILY": run1["cert_status"]["R-EVASION"],
        "M-BANK-N-IN": d_sound["n_in"],
        "M-BANK-N-OUT": d_sound["n_out"],
    }
    result["bank"] = {"n_items": len(build_bank()), "n_in": d_sound["n_in"], "n_out": d_sound["n_out"],
                      "per_family_n_in": {f: d_sound["per_family"][f]["n_in"] for f in FAM_ORDER},
                      "per_family_n_out": {f: d_sound["per_family"][f]["n_out"] for f in FAM_ORDER},
                      "cert_neg_sizes": {f: len(CERT_NEG[f]) for f in FAM_ORDER}}

    # ---- primary decision ----
    if (d_sound["false_accept_count"] > 0 or d_sound["http_on_out_label"] > 0
            or d_sound["refusal_executed_count"] > 0 or d_over["false_accept_count"] > 0
            or d_over["http_on_out_label"] > 0 or d_over["refusal_executed_count"] > 0):
        result["status"], result["outcome"] = "COMPLETE", "FALSIFIES"
        result["decision"] = "SHIPPED_CERTIFICATE_UNSAFE"
        result["reason"] = ("the shipped certificate arm bound out-of-grammar values "
                            "(R-SOUND FA=%d, R-OVERWIDE FA=%d); the guard is not safe"
                            % (d_sound["false_accept_count"], d_over["false_accept_count"]))
    elif d_sound["coverage"] == 1.0 and gate_over["false_accept_count"] >= 1:
        result["status"], result["outcome"] = "COMPLETE", "SUPPORTS"
        result["decision"] = ("SHIPPED_CERTIFICATE_SAFE_AND_COMPLETE__REFUSES_AUDITED_OVERWIDE__"
                              "CLOSED_WORLD_BOUNDARY_FA=%d" % d_ev["false_accept_count"])
        result["reason"] = ("the shipped certificate adopts the sound declaration (FA=0, coverage 1.0 "
                            "vs shipped %.4f) and refuses the audited over-wide declaration that the "
                            "training-consistency gate adopts (cert FA=0 vs gate FA=%d); a "
                            "certificate-passing unsound declaration still yields %d false accept(s), "
                            "so the trust boundary is closed-world"
                            % (s["coverage"], gate_over["false_accept_count"], d_ev["false_accept_count"]))
    else:
        result["status"], result["outcome"] = "COMPLETE", "MIXED"
        result["decision"] = "SHIPPED_CERTIFICATE_SAFE_BUT_INCOMPLETE"
        result["reason"] = ("the shipped certificate held FA=0 but coverage %.4f < 1.0 under the sound "
                            "declaration (false rejects %d)"
                            % (d_sound["coverage"], d_sound["false_reject_count"]))
    result["boundary"] = {
        "closed_world": True,
        "admitted_unsound_declaration_false_accept_count": d_ev["false_accept_count"],
        "held_out_blind_spot_by_family": dict(HELDOUT),
        "statement": ("ingested declarations are adopted only against the frozen audited negative bank; "
                      "an unsound declaration whose over-accept lies outside that bank passes the "
                      "certificate, so the shipped kernel must enforce a closed-world trust boundary and "
                      "prefer UNKNOWN over unsafe inheritance for uncertified declarations"),
    }
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True, default=repr))
<!-- END FROZEN RUNNER -->
