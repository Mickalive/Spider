# Preregistration — EXP-GRAPH-37978902447

- **Lane:** graph
- **Claim:** C-FRESHNESS (owner_lanes `[graph, runtime, product]`; current status HYPOTHESIS)
- **Parent:** EXP-GRAPH-37964565784 (`handoff.json` sha256 `61a29cee…c386cdb`), disposition **USE** (continuity only)
- **Grandparent:** EXP-GRAPH-37950584469
- **Director mandate:** cycle_id `37978016186`, action `CONTINUE`, target C-FRESHNESS, `cognitive_reset=true`, `parent_handoff_disposition=USE`
- **Authored:** 2026-10-09, before any anchor is contacted in this transaction.

This preregistration is frozen together with `spec.json` (and `request.json`) by
`freeze.json`. It is the binding design; after freeze nothing here may be weakened
after outcomes are seen.

---

## 0. No-outcome-at-DESIGN statement

DESIGN performed **no outcome-bearing measurement**: no HTTP request, no extraction,
no anchor or candidate probe, and no inspection of any outcome beyond the already
published parent packet and accepted Codex evidence. The only computation DESIGN
performed is the **mandate-required satisfiability dry-run on pinned synthetic
inputs** recorded in `spec.pre_freeze_satisfiability_dry_run`; it uses no network
and no anchor data and cannot pre-empt the confirmatory objects. Anchor behaviour is
asserted only in `spec.substrate_certificate` with its evidence class and the exact
already-frozen artifact.

---

## 1. Why this experiment exists (diagnosis of the parent)

The parent EXP-GRAPH-37964565784 died at **GATE-C3** as `MEASUREMENT_INVALID / F-CERT`
— a **second consecutive control-plane design defect**, not a scientific negative.
Its frozen `repaired_session_isolation_predicate` conjoined three requirements:

```
pass = first_request_cookieless
       AND session_identifying_disjoint
       AND pairwise_disjoint_on_name_value_after_filter      # <-- defect
```

`session_identifying_disjoint` (all session-identifying cookie **names** pairwise
disjoint) is structurally unsatisfiable for real session cookies, whose names recur
across independent sessions by design. The audit (`audit.json.required_fixes[0]`)
intended a **disjunction**, and `derived/certificate.json` shows the
`(name,value)`-after-filter branch was already `true` for all 8 anchors. This is the
**third** consecutive attempt on this gate, so the Director added a binding pre-freeze
satisfiability precondition and a hard-stop rule.

## 2. The corrected GATE-C3 predicate (the only design change)

```
M-CERT-SESSION-ISOLATION-PASS :=
    first_request_cookieless
    AND pairwise_disjoint_on_name_value_after_filter(jars)

pairwise_disjoint_on_name_value_after_filter(jars) :=
    for all i < j:
        filter_allowlist(jar_i) INTERSECT filter_allowlist(jar_j) == {}
    where filter_allowlist removes every (name,value) whose NAME is in the frozen
    constant-configuration allowlist:
        preferred_language, GeoIP, NetworkProbeLimit,
        WMF-Last-Access, WMF-Last-Access-Global, CentralAuthAnonTopLevel
```

- `pairwise_disjoint_on_name_value_after_filter` is the **sole** disjointness check.
- `session_identifying_disjoint` is **demoted to a non-gating diagnostic**
  (`M-CERT-SESSION-IDENTIFYING-DISJOINT`); it is *expected* to be false where servers
  reuse session cookie names with distinct values, and that is correct.
- Unknown/new cookies are **not** auto-exempted: any shared non-allowlisted
  `(name,value)` pair fails.
- See `spec.repaired_session_isolation_predicate`.

## 3. Pre-freeze satisfiability dry-run (mandate precondition)

Executed by DESIGN on pinned synthetic inputs (seed `37978902447`), recorded in
`spec.pre_freeze_satisfiability_dry_run`. Result: **the corrected predicate is
satisfiable and not vacuous, and every declared membership class is reachable.**

Truth table (observed `pass` under the corrected predicate vs the parent AND):

| case | pattern | corrected | parent AND |
|---|---|---|---|
| T1 | session names shared, values **distinct**, allowlisted constants shared | **PASS** | FAIL |
| T2 | one non-allowlisted `(name,value)` pair shared | FAIL | FAIL |
| T3 | allowlisted constant only shared | PASS | PASS |
| T4 | allowlisted shared **plus** a shared non-allowlisted pair | FAIL | FAIL |
| T5 | empty jars | PASS | PASS |
| T6 | first request carried a Cookie | FAIL | FAIL |
| T7 | legitimate session names shared, values distinct | **PASS** | FAIL |
| T8 | unknown cookie name shared with **same** value | FAIL | PASS |
| T9 | unknown cookie name shared with distinct values | PASS | PASS |
| T10 | three-way same-value overlap | FAIL | FAIL |

**Defect caught pre-freeze:** the parent's `NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS`
fixture tested shared session cookie **names**, which the corrected sole
`(name,value)` check deliberately allows — a name-level fixture would have made the
corrected predicate look vacuous. The corrected fixture requires a shared
non-allowlisted `(name,value)` **pair** (T2/T4/T8) to fail.

Reachability certificate (all `true`): 5 anchor verdicts
(`RECOVERED_SESSION_SCOPED / RECOVERED_INVARIANT / RECOVERED_EMPTY / NO_FIELD /
UNREACHABLE`); 4 drift families (`F-FRESH`, `F-VALUE(D1V)`, `F-STRUCT`,
`F-TRANSPORT`); all 4 guard channels both fire and not-fire; all GATE-B branches
(`INCUMBENT-BLIND-CONFIRMED`, `INCUMBENT-NOT-BLIND`, `DATA-INSUFFICIENT-D1V`,
`DATA-INSUFFICIENT-D1V-DEGENERATE`); all D1/D2/D3 decision branches; predicate pass
and fail reachable. The one-anchor bootstrap is shown degenerate and the two-anchor
bootstrap non-degenerate.

## 4. Hypotheses

**H-MAIN (Part I).** After the corrected GATE-C3 passes, both independently written
stdlib paths recover ≥2 distinct non-empty exact token values across K=4 fresh
sessions on ≥3 of 4 anchors and agree on the per-field value set and session-scoped
verdict (`M-EXTRACT-AGREE-VALUESET ≥ 3`, `M-EXTRACT-AGREE-VERDICT ≥ 3`), so
`M-N-SESSION-SCOPED-CONFIRMED ≥ 3 of 4` and the parent's failure is an **extraction
defect**, not representation loss.

**H-GUARD (Part II, co-primary, read only if D1).** Over the frozen drift-trial
population, the value-blind incumbent `B-INCUMBENT-SIGNAL-ONLY` false-accepts on the
D1V family at a materially higher rate than `B-VALUE-AWARE`
(`M-PAIRED-FA-DIFF-D1V ≥ 0.10`, anchor-clustered 97.5% lower bound > 0). **New
non-degeneracy clause:** the anchor-clustered bound is read only if
`M-N-D1V-ANCHORS ≥ 2`; with a single anchor every bootstrap resample is identical.

**H-TIMESCALE (diagnostic).** Warm-jar value-variation rate is within 0.10 of the
fresh-jar value-variation rate on ≥2 anchors → `PER_REQUEST_SCALE`, bounding any
value-binding verdict to a short-lived applicability check.

## 5. Anchors, substrate and instrument (inherited frozen)

- **Positive anchors** (credential-free, server-rendered, GET-only):
  `CAL-POS-1` gitlab.com/-/trial_registrations/new/,
  `CAL-POS-2` auth.wikimedia.org/enwiki/…Special:CreateAccount,
  `CAL-POS-3` en.wikipedia.org/…Special:UserLogin&action=form,
  `CAL-POS-4` meta.discourse.org/. `CAL-POS-5` retired (404).
- **Negative anchors:** `CAL-NEG-1` iana.org, `CAL-NEG-2` jsdelivr CPython README,
  `CAL-NEG-3` debian.org, `CAL-NEG-4` httpbin.org/forms/post — must yield zero
  in-list values under both paths (`NC-CAL-NEG-ALL-REJECTED`).
- **K=4** fresh disjoint-jar sessions (S1..S4), first request cookie-free,
  `Connection: close`, ≥2.0 s same-host pacing.
- **Two independently written stdlib extraction paths** `P-EXTRACT-A` (html.parser)
  and `P-EXTRACT-B` (regex/lexer, hand-written entity decoder, no shared helper),
  both fed the byte-identical stored body; AST import-attestation required
  (`NC-PATH-INDEPENDENCE`).
- **Retained raw bodies** per (anchor, session) with per-record sha256, so the
  packet is re-analyzable without re-fetching (`V10`).
- **Warm-jar diagnostic:** 2 same-jar re-captures per anchor (`NC-TIME-VS-SESSION`).

## 6. Trial population, D1V definition and guard

A trial is a (AGSI instance, recorded session, current session) pair; AGSI keys are
`(anchor_id, field_name, structure_signature)` plus a count-stable occurrence
ordinal (`NC-TRIAL-CONSTRUCTION-STABILITY`, inherited repaired keying). Label is
`STALE` iff live value ≠ recorded value byte-exact.

```
D1V := STALE
       AND NOT structural_change
       AND NOT transport_change
structural_change := structure_signature (type_class, form_action, form_method,
                      sorted input_name_set) differs
transport_change  := (ETag, Last-Modified, Cache-Control max-age, Vary) or final_url differs
```

`endpoint_change` and `postcond_change` are observed and reported but do **not**
exclude a trial from D1V under the frozen rule. Guard model is unchanged:
`B-INCUMBENT-SIGNAL-ONLY` = REUSE iff none of `CH-STRUCT-SIG`,
`CH-TRANSPORT-VALIDATOR`, `CH-POSTCOND-SEM` fires; `B-VALUE-AWARE` = REUSE iff
live == recorded.

## 7. Mandate Q2 — can the D1V population span more than one anchor?

The mandate asks whether a D1V population spanning **more than one anchor** makes
`M-PAIRED-FA-DIFF-D1V` evaluable with a non-degenerate anchor-clustered lower bound.
This packet answers it explicitly and at zero extra request cost:

1. A new pre-registered requirement `M-N-D1V-ANCHORS ≥ 2` gates the Part II read;
   otherwise branch **`DATA-INSUFFICIENT-D1V-DEGENERATE`** and no blindness claim.
2. A pre-registered per-anchor diagnostic `M-D1V-BLOCKER-{anchor}`
   (`NONE | BODY_DERIVED_ETAG | TOKEN_BEARING_FINAL_URL | STRUCTURAL_ENDPOINT_DRIFT |
   NO_FIELD | UNREACHABLE`) and `M-TRANSPORT-BODY-DERIVATION-{anchor}` records **why**
   an anchor does not contribute D1V.

**Design-derived expectation** (from inherited parent RAW evidence; not a new
measurement, not a gate value):
- `CAL-POS-1`: ETag == `sha256(body)[:32]` on 4/4 parent sessions; `transport_change`
  is forced by value rotation → D1V structurally unreachable.
- `CAL-POS-3`: `final_url` carries a distinct `centralauthLoginToken` per session →
  `transport_change` forced → D1V structurally unreachable.
- `CAL-POS-2`: stable transport → the parent's only D1V anchor (M-N-D1V=6).
- `CAL-POS-4`: `NO_FIELD` → no value trials.

Therefore the mandate's Q2 is **expected to resolve `DATA-INSUFFICIENT-D1V-DEGENERATE`**.
This is decision-changing: powering the blindness/necessity read requires either a
different anchor population or an instrument redesign that decouples body-derived
validators from value rotation — neither authorized by this mandate. If a second
anchor does contribute D1V, Gate-B is read with its anchor-clustered bound.

## 8. Controls (frozen identities)

- **Baselines:** `B-SINGLE-PATH-A`, `B-SINGLE-PATH-B`, `B-PARENT-METHOD-REIMPL`,
  `B-INCUMBENT-SIGNAL-ONLY`, `B-VALUE-AWARE`, `B-FULL-GUARD`, `B-NO-GUARD-REPLAY`.
- **Positive controls:** `PC-EXTRACT-CANARY` (CAL-POS-1 ≥2 distinct
  `authenticity_token`, both paths), `PC-GUARD-LOGIC` (SYN-GUARD-* fixtures).
- **Negative controls:** `NC-CAL-NEG-ALL-REJECTED`, `NC-EXTRACT-EMPTY-VALUE`,
  `NC-EXTRACT-JSSTRING`, `NC-PATH-INDEPENDENCE`, `NC-SESSION-ISOLATION-REPAIRED`,
  `NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS` (corrected to the `(name,value)` level),
  `NC-TRIAL-CONSTRUCTION-STABILITY`, `NC-TIME-VS-SESSION`,
  `NC-NONDEGENERATE-ESTIMATOR`, `NC-OPEN-GET-ONLY`,
  `NC-D1V-ANCHOR-NONDEGENERACY` (new), `NC-TRANSPORT-VALUE-COUPLING-DECLARED` (new).
- **Guard channels:** `CH-STRUCT-SIG`, `CH-TRANSPORT-VALIDATOR`, `CH-POSTCOND-SEM`,
  `CH-PRECOND-BINDING`.

## 9. Decision rule (ordered, fail-closed)

- **GATE C** (before extraction): `C1` route-ok ≥3/4 and field-present ≥3/4; `C2`
  zero negative-anchor values both paths; `C3` corrected isolation predicate **and**
  not-vacuous control. Failure → `MEASUREMENT_INVALID / INCONCLUSIVE / F-CERT`.
  `C4` body-variation <3/4 → `COMPLETE / INCONCLUSIVE / NO-BODY-VARIATION`.
- **GATE E:** `E1` canary; `E2` fixtures, path independence, trial-construction
  stability. Failure → `MEASUREMENT_INVALID / INCONCLUSIVE / F-INSTR`.
  `E3` dual-path agreement ≥3/4. Fail → `COMPLETE / MIXED / EXTRACTION-UNRELIABLE`.
- **Decision:** `D1` session-scoped ≥3/4 → `COMPLETE / SUPPORTS /
  EXTRACTION-DEFECT-CONFIRMED`; `D2` representation-loss ≥3/4 → `COMPLETE /
  FALSIFIES / REPRESENTATION-LOSS-CONFIRMED`; else `D3` → `COMPLETE / MIXED /
  MIXED-ANCHORS`.
- **GATE B** (only if D1): if `M-N-D1V < 6` or `M-N-DECISIONS-D1V < 2` or
  `M-N-D1V-ANCHORS < 2` or the non-degeneracy control fails → the degenerate or
  insufficient branch, Part II reported null. Else if `M-PAIRED-FA-DIFF-D1V ≥ 0.10`
  and its clustered low bound > 0 → `INCUMBENT-BLIND-CONFIRMED`; else
  `INCUMBENT-NOT-BLIND`. Gate-B branches do not change status/outcome.

Status/outcome vocabulary and the branch→status/outcome map are fixed in
`spec.transmission_contract`.

## 10. Validity threats and scope (CC-A..CC-I, SB-01..SB-07)

- Bounds to the 4 pinned anchors, K=4, stdlib HTTP, one capture date, one egress
  path; no prevalence over "the Web" (`CC-A`).
- C-FRESHNESS may advance **at most to EXPERIMENTAL**, only via the DIRECTOR
  (`CC-B`).
- No JavaScript/browser/Docker/local server/credentials/model calls
  (`SB-01`, `V05`).
- No re-fit of the guard, D1V definition, thresholds, or anchors; the only design
  change is the corrected predicate plus the dry-run and the anchor-count clause
  (`SB-06`).
- The transport-value coupling diagnostic is descriptive and zero-extra-cost, enters
  no gate (`SB-07`).
- `M-INVISIBLE-STALE-PREV` is `null`, never `0.0` (`SB-04`).
- SB-02 permission-boundary change is unreachable on credential-free public origins
  and is not tested.

## 11. Consequence of both outcomes

**Positive** (D1, and Part II read + blind-confirmed): the credential-free no-JS
substrate is a usable calibration substrate; C-FRESHNESS may advance to EXPERIMENTAL;
the value-aware channel is measurably necessary; a `PER_REQUEST_SCALE` timescale
classification bounds the guard to a short-lived applicability check.

**Negative / bounded** (D2, E3-fail, not-blind, or degenerate D1V): representation
loss or instrument unreliability blocks calibration; or the value-aware channel may be
deleted; or Part II is a pre-declared power statement (`DATA-INSUFFICIENT-D1V` /
`DATA-INSUFFICIENT-D1V-DEGENERATE`) with the blocker diagnostic establishing that the
blindness question cannot be powered on these anchors. In every F-INSTR/F-CERT branch
no product change is authorized, C-FRESHNESS stays HYPOTHESIS, and
replay-by-assumption is not authorized.

## 12. Hard stop

This is the third consecutive certificate attempt on this gate. If this attempt is
**also** `MEASUREMENT_INVALID` on a predicate/class defect, the next Director cycle
should PARK Graph and mandate a one-time repair of the certificate machinery in
Runtime/Product instead of another inline patch.
