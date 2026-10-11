# EXP-GRAPH-37992949248 — EXECUTE report (graph, C-FRESHNESS)

**status=COMPLETE · outcome=SUPPORTS · branch=EXTRACTION-DEFECT-CONFIRMED · Part II gate=DATA-INSUFFICIENT-D1V-DEGENERATE · GATE F=True · M-D1V-DEGENERACY-MODE=ANCHOR_TRANSPORT_COUPLING · secondary_label=FEASIBILITY-D1V-SINGLE-ANCHOR-TRANSPORT-COUPLED**

This packet implements the CORRECTED GATE-C3 predicate: pass = first_request_cookieless AND pairwise_disjoint_on_name_value_after_filter (the SOLE disjointness check), with session_identifying_disjoint demoted to a non-gating diagnostic, and adds the mandate clause M-N-D1V-ANCHORS>=2. GATE F (estimator capability, V16 same-code-path positive+null controls) is read BEFORE any GATE-B read. It re-runs the frozen two-path extraction read, then reads the incumbent value-blind guard versus the value-aware guard on real value-only rotation with anchor-clustered bounds.

## 1. Raw evidence and certificate (GATE C)

- Requests: 40 (all GET, cap 200); all first requests cookie-free: True.
- M-CERT-ROUTE-OK=4/4, M-CERT-BODY-VARIABLE=4/4, M-CERT-FIELD-PRESENT=3/4.
- M-CERT-SESSION-ISOLATION-PASS=True; NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS=True.
- M-CERT-NEG-VALUES-A=0, M-CERT-NEG-VALUES-B=0 (all four negatives).

## 2. Part I — extraction validity under the repaired certificate (GATE E)

- **CAL-POS-1**: verdict_A=RECOVERED_SESSION_SCOPED (distinct=16), verdict_B=RECOVERED_SESSION_SCOPED (distinct=16), route_ok=4/4, distinct_body=4/4.
- **CAL-POS-2**: verdict_A=RECOVERED_SESSION_SCOPED (distinct=5), verdict_B=RECOVERED_SESSION_SCOPED (distinct=5), route_ok=4/4, distinct_body=4/4.
- **CAL-POS-3**: verdict_A=RECOVERED_SESSION_SCOPED (distinct=5), verdict_B=RECOVERED_SESSION_SCOPED (distinct=5), route_ok=4/4, distinct_body=4/4.
- **CAL-POS-4**: verdict_A=NO_FIELD (distinct=0), verdict_B=NO_FIELD (distinct=0), route_ok=4/4, distinct_body=4/4.
- M-EXTRACT-AGREE-VALUESET=4/4, M-EXTRACT-AGREE-VERDICT=4/4, M-CANARY-PASS=True, M-EXTRACT-KAPPA=None.
- M-N-SESSION-SCOPED-CONFIRMED=3/4, M-N-REPRESENTATION-LOSS=1/4, M-N-EXTRACTION-UNRELIABLE=0/4.

## 3. Part II — repaired drift population and explicit false-accept bound (GATE B)

- M-N-D1V=6 over M-N-D1V-ANCHORS=1 (['CAL-POS-2']); M-N-DECISIONS-D1V=1; nondegenerate=True; M-N-D1V-BASE-ADEQUATE=False; M-D1V-ANCHOR-CLUSTERED-EVALUABLE=False.
- Mandate Q2 per-anchor diagnostics (descriptive, non-gating): {"M-D1V-BLOCKER-CAL-POS-1": "BODY_DERIVED_ETAG", "M-D1V-BLOCKER-CAL-POS-2": "NONE", "M-D1V-BLOCKER-CAL-POS-3": "TOKEN_BEARING_FINAL_URL", "M-D1V-BLOCKER-CAL-POS-4": "NO_FIELD", "M-TRANSPORT-BODY-DERIVATION-CAL-POS-1": true, "M-TRANSPORT-BODY-DERIVATION-CAL-POS-2": "not_applicable", "M-TRANSPORT-BODY-DERIVATION-CAL-POS-3": "not_applicable", "M-TRANSPORT-BODY-DERIVATION-CAL-POS-4": "not_applicable", "M-TRANSPORT-COUPLING-STABILITY-CAL-POS-1": "UNCHANGED", "M-TRANSPORT-COUPLING-STABILITY-CAL-POS-2": "UNCHANGED", "M-TRANSPORT-COUPLING-STABILITY-CAL-POS-3": "UNCHANGED", "M-TRANSPORT-COUPLING-STABILITY-CAL-POS-4": "UNCHANGED"}.
- Channels (path A): {"CH-POSTCOND-SEM": {"fire": 0, "not_fire": 48, "status": "INACTIVE-ON-POPULATION", "waived": true}, "CH-PRECOND-BINDING": {"fire": 36, "not_fire": 12, "satisfied": true, "status": "ACTIVE", "waived": false}, "CH-STRUCT-SIG": {"fire": 16, "not_fire": 32, "satisfied": true, "status": "ACTIVE", "waived": false}, "CH-TRANSPORT-VALIDATOR": {"fire": 36, "not_fire": 12, "satisfied": true, "status": "ACTIVE", "waived": false}}.
- M-FA-INCUMBENT-D1V=1.0 (UB97=None); M-FA-VALUEAWARE-D1V=0.0 (UB97=None); M-PAIRED-FA-DIFF-D1V=1.0 (LB=None, UB=None).
- Part II gate branch: **DATA-INSUFFICIENT-D1V-DEGENERATE** (status-non-changing).
- M-D1V-DEGENERACY-MODE=ANCHOR_TRANSPORT_COUPLING; secondary label=FEASIBILITY-D1V-SINGLE-ANCHOR-TRANSPORT-COUPLED; M-N-D1V-BLOCKED-ANCHORS=3; M-D1V-INTERVAL-DEGENERATE=False.

## 4. GATE F — estimator capability control (read before GATE B)

- M-ESTIMATOR-POSITIVE-CONTROL-PASS=True (2-anchor heterogeneous LOW=0.3333333333333333, UB97=0.5); NC-ESTIMATOR-CONTROL-SENSITIVITY=True (1-anchor null; homogeneous zero-width pass=True). Same estimator function, B and seed as the real D1V read (V16 partial binding; population-assay binding is out of scope of this mandate).

## 5. Timescale diagnostic (CC-H)

- CAL-POS-1: PER_REQUEST_SCALE (warm_var=1.0, fresh_var=1.0, body_var=1.0).
- CAL-POS-2: PER_REQUEST_SCALE (warm_var=1.0, fresh_var=1.0, body_var=1.0).
- CAL-POS-3: PER_REQUEST_SCALE (warm_var=1.0, fresh_var=1.0, body_var=1.0).
- CAL-POS-4: NO_ROTATION (warm_var=0.0, fresh_var=0.0, body_var=1.0).

## 6. Controls

- GATE-C1: PASS
- GATE-C2: PASS
- GATE-C3: PASS
- GATE-C4: PASS
- GATE-F: PASS
- PC-ESTIMATOR-NONDEGENERATE: PASS
- NC-ESTIMATOR-CONTROL-SENSITIVITY: PASS
- GATE-E1: PASS
- GATE-E2: PASS
- GATE-E3: PASS
- PC-EXTRACT-CANARY: PASS
- PC-GUARD-LOGIC: PASS
- NC-CAL-NEG-ALL-REJECTED: PASS
- NC-PATH-INDEPENDENCE: PASS
- NC-SESSION-ISOLATION-REPAIRED: PASS
- NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS: PASS
- NC-NONDEGENERATE-ESTIMATOR: PASS
- NC-D1V-ANCHOR-NONDEGENERACY: DEGENERATE-OR-INSUFFICIENT
- F-BLIND-DEGENERATE: OBSERVED
- ASSERT-WRITE-SCOPE: None

## 7. Interpretation (bounded)

The repaired certificate passed and both independently written stdlib paths agree on per-field value sets and session-scoped verdicts; the parent's failure on these anchors is attributable to an instrument/extraction certificate defect, not to representation loss. C-FRESHNESS may advance at most to EXPERIMENTAL, only via the DIRECTOR (CC-B). No promotion is authorized.
Part II is DATA-INSUFFICIENT-D1V-DEGENERATE (F-BLIND-DEGENERATE): the D1V population spans a single anchor, so every anchor-clustered resample is identical and GATE-B is NOT READ. Whether the value-aware channel is necessary on value-only rotation remains UNKNOWN; never a blindness/necessity result. M-D1V-DEGENERACY-MODE=ANCHOR_TRANSPORT_COUPLING; secondary label=FEASIBILITY-D1V-SINGLE-ANCHOR-TRANSPORT-COUPLED (emitted).

No promotion into Product Core, no replay-by-assumption. M-INVISIBLE-STALE-PREV is null, never 0.0; SB-02 and SB-04 remain unmeasured by design.
