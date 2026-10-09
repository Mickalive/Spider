# EXP-GRAPH-37964565784 — EXECUTE report (graph, C-FRESHNESS)

**status=MEASUREMENT_INVALID · outcome=INCONCLUSIVE · branch=F-CERT · Part II gate=NOT_READ_D1_NOT_REACHED**

This packet repairs the parent's GATE-C3 certificate predicate at design time (audit required_fixes[0]) and re-runs the same frozen two-path extraction read, then reads the incumbent value-blind guard versus the value-aware guard on real value-only rotation with anchor-clustered bounds.

## 1. Raw evidence and certificate (GATE C)

- Requests: 40 (all GET, cap 200); all first requests cookie-free: True.
- M-CERT-ROUTE-OK=4/4, M-CERT-BODY-VARIABLE=4/4, M-CERT-FIELD-PRESENT=3/4.
- M-CERT-SESSION-ISOLATION-PASS=False; NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS=True.
- M-CERT-NEG-VALUES-A=0, M-CERT-NEG-VALUES-B=0 (all four negatives).

## 2. Part I — extraction validity under the repaired certificate (GATE E)

- **CAL-POS-1**: verdict_A=RECOVERED_SESSION_SCOPED (distinct=16), verdict_B=RECOVERED_SESSION_SCOPED (distinct=16), route_ok=4/4, distinct_body=4/4.
- **CAL-POS-2**: verdict_A=RECOVERED_SESSION_SCOPED (distinct=5), verdict_B=RECOVERED_SESSION_SCOPED (distinct=5), route_ok=4/4, distinct_body=4/4.
- **CAL-POS-3**: verdict_A=RECOVERED_SESSION_SCOPED (distinct=5), verdict_B=RECOVERED_SESSION_SCOPED (distinct=5), route_ok=4/4, distinct_body=4/4.
- **CAL-POS-4**: verdict_A=NO_FIELD (distinct=0), verdict_B=NO_FIELD (distinct=0), route_ok=4/4, distinct_body=4/4.
- M-EXTRACT-AGREE-VALUESET=4/4, M-EXTRACT-AGREE-VERDICT=4/4, M-CANARY-PASS=True, M-EXTRACT-KAPPA=None.
- M-N-SESSION-SCOPED-CONFIRMED=3/4, M-N-REPRESENTATION-LOSS=1/4, M-N-EXTRACTION-UNRELIABLE=0/4.

## 3. Part II — repaired drift population and explicit false-accept bound (GATE B)

- M-N-D1V=6 over None anchors; M-N-DECISIONS-D1V=2; nondegenerate=True.
- Channels (path A): {"CH-POSTCOND-SEM": {"fire": 0, "not_fire": 48, "status": "INACTIVE-ON-POPULATION", "waived": true}, "CH-PRECOND-BINDING": {"fire": 36, "not_fire": 12, "satisfied": true, "status": "ACTIVE", "waived": false}, "CH-STRUCT-SIG": {"fire": 15, "not_fire": 33, "satisfied": true, "status": "ACTIVE", "waived": false}, "CH-TRANSPORT-VALIDATOR": {"fire": 36, "not_fire": 12, "satisfied": true, "status": "ACTIVE", "waived": false}}.
- M-FA-INCUMBENT-D1V=None (UB97=None); M-FA-VALUEAWARE-D1V=None (UB97=None); M-PAIRED-FA-DIFF-D1V=None (LB=None, UB=None).
- Part II gate branch: **NOT_READ_D1_NOT_REACHED** (status-non-changing).

## 4. Timescale diagnostic (CC-H)

- CAL-POS-1: PER_REQUEST_SCALE (warm_var=1.0, fresh_var=1.0, body_var=1.0).
- CAL-POS-2: PER_REQUEST_SCALE (warm_var=1.0, fresh_var=1.0, body_var=1.0).
- CAL-POS-3: PER_REQUEST_SCALE (warm_var=1.0, fresh_var=1.0, body_var=1.0).
- CAL-POS-4: NO_ROTATION (warm_var=0.0, fresh_var=0.0, body_var=1.0).

## 5. Controls

- GATE-C1: PASS
- GATE-C2: PASS
- GATE-C3: FAIL
- GATE-C4: PASS
- GATE-E1: PASS
- GATE-E2: PASS
- GATE-E3: PASS
- PC-EXTRACT-CANARY: PASS
- PC-GUARD-LOGIC: PASS
- NC-CAL-NEG-ALL-REJECTED: PASS
- NC-PATH-INDEPENDENCE: PASS
- NC-SESSION-ISOLATION-REPAIRED: FAIL
- NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS: PASS
- NC-NONDEGENERATE-ESTIMATOR: PASS

## 6. Interpretation (bounded)

The repaired certificate failed a blocking gate: terminal MEASUREMENT_INVALID (F-CERT); no claim-level statement is licensed.

No promotion into Product Core, no replay-by-assumption. M-INVISIBLE-STALE-PREV is null, never 0.0; SB-02 and SB-04 remain unmeasured by design.
