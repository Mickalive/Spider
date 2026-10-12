# EXECUTE report: EXP-RUNTIME-38194351940

- **Experiment ID:** EXP-RUNTIME-38194351940
- **Lane:** runtime
- **Claim:** C-MEAS-VALID (substrate-validity evidence only; no claim-status change, no Product promotion)
- **Substrate class:** SBA-CREDENTIAL-FREE-V3 (Session-Mechanism-Inheritance), credential-free, deterministic, stdlib-only
- **Stage:** EXECUTE (frozen request/spec/prereg/freeze/design_review; inputs immutable)
- **Status / outcome / frozen decision label:** `COMPLETE` / `SUPPORTS` / `ROBUST`
- **Canonical packet:** `result.json`, `provenance.json`, `report.md`, `artifacts/`

## 1. What was run

The complete EXECUTE harness was reconstructed byte-for-byte from
`spec.json.design_satisfiability_probe.source` into `run_experiment.py` and its sha256 was verified
to equal the frozen `source_sha256` (`acbb1e1f64cdb14e4d5a645e7bb800cbaf42091bc45ecfb40107abda890340e9`)
**before scoring**. Two non-outcome-bearing paths and one outcome-bearing path were executed:

| mode | role | stdout sha256 | frozen sha256 | match |
|---|---|---|---|---|
| `--mode probe` | V1 fidelity / transport / control sanity | `92eb44d005888784d56addbbc35ae41869f9df1f57f9490c2c651c933e1da79e` | same | yes |
| `--mode selftest` | frozen evaluator path | `208b7be424037a8e7348d243d61158c506da573fc096fcd2a68adc2ea3d4794c` | same | yes |
| `--mode scored` | outcome-bearing 56-cell x 20-session matrix, run twice | `artifacts/run_scored.json` | n/a (EXECUTE-only) | — |

The scored matrix (`56` cells x `20` sessions = `1120` bank instances) was run twice inside the frozen
harness; the two runs were byte-identical (`determinism_ok=true`). Wall clock ~19m50s. No model calls,
no browser work, no external network and no LLM endpoint were used (loopback stdlib HTTP only), so B3 is
not required and this ran independently of Intel's endpoint work.

## 2. Raw result (observations, not interpretation)

Success rate by family / novelty / arm (aggregated over 20 sessions per cell):

| arm | F1 0.00 | F1 0.25 | F1 0.50 | F1 0.75 | F2 0.00 | F2 0.25 | F2 0.50 | F2 0.75 |
|---|---|---|---|---|---|---|---|---|
| T-MECHANISM-INHERIT | 1.000 | 1.000 | **1.000** | **1.000** | 1.000 | 1.000 | **1.000** | **1.000** |
| PC-EXACT-REPLAY | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| B-CROSS-SESSION-COMPILE | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| B-WITHIN-SESSION-RECEIPT | 1.000 | 1.000 | 0.875 | 0.875 | 1.000 | 1.000 | 0.900 | 0.900 |
| B-WITHIN-SESSION-COMPOSE | 1.000 | 1.000 | 0.875 | 0.875 | 1.000 | 1.000 | 0.900 | 0.900 |
| B-RETRIEVAL-REPLAY | 1.000 | 1.000 | 0.875 | 0.875 | 1.000 | 1.000 | 0.900 | 0.900 |
| B-MEMORYLESS | 1.000 | 1.000 | 0.875 | 0.875 | 1.000 | 1.000 | 0.900 | 0.900 |

Every retention comparator certifies at all four scored cells (12/12). Treatment margin over each
retention comparator is `0.125` (F1, K=8) and `0.100` (F2, K=10); the retention frontier (scopes within
`MARGIN_FLOOR=0.05` of T) is empty at every scored cell. Counter distinctness vs T at novelty 0.5:
`B-WITHIN-SESSION-RECEIPT` 2/4, `B-WITHIN-SESSION-COMPOSE` 2/4, `B-RETRIEVAL-REPLAY` 3/4, `B-MEMORYLESS`
2/4. Matched correctness equals success rate in all 56 cells; minimum arm success rate is `0.875`
>= `CORRECTNESS_FLOOR=0.80`. All observed aggregate counters reproduce the frozen per-instance
predictions exactly (e.g. T F1: 680/20=34 http, 0 retrieval, 320/20=16 verification, 0 repair;
`B-RETRIEVAL-REPLAY` F1: 36 http, 8 retrieval, 16 verification, 1 repair).

Controls: `NC-MECHANISM-OFF` (exposed chain answer) drives the within-session retention comparator to
`1.0` in both families, destroying the certificate direction. `NC-MECHANISM-NONDEGENERATE`: 100 sampled
instances, `a_zero=0`, `duplicate_x=0`, `solve_fail=0`, `query_collision=0`, `min_query_gap=399759921`.
`NC-NO-LEAK`/protocol invariants: 15/15 hold; the chain task `resource_id` is null in scored sessions
and the required answer appears in no scored body. `NC-CEILING-BAND`: all seven arms `1.0` at novelty
0.0. `NC-IDENTITY-DISCLOSURE`: `B-CROSS-SESSION-COMPILE` equals T in all 8 cells.

## 3. Gates and frozen decision

All twelve evaluated validity gates are true:

`V1_code_fidelity_manifest`, `V2_transport_conformance`, `V3_no_leak`, `V4_determinism`,
`V5_arm_liveness`, `V6_counter_instrumentation`, `V7_matched_correctness`, `V8_ceiling_band`,
`V8_identity_disclosure`, `V8_mechanism_nondegenerate`, `V8_mechanism_off`,
`V8_retention_counter_distinctness`.

Applying the frozen decision rule precedence (MEASUREMENT_INVALID first, then ROBUST, else PARTIAL, else
COLLAPSED) yields `decision_label = ROBUST`, mapped to `outcome = SUPPORTS` and `status = COMPLETE` per
`spec.decision_rule.outcome_enum_mapping` / `result_status_mapping`. The retention ladder (no
retention-only scope closes the range) is a declared control and predictor, not a validity gate; it is
empty at all scored cells, consistent with ROBUST.

## 4. Interpretation (does not exceed the frozen claim)

The hardened V3 credential-free bank supplies a memory-robust, non-ceiling dynamic range against a
frozen within-session full-receipt-memory comparator and against cross-session retention of all raw
calibration examples, at both families and both scored bands, while a cross-session compile-capable arm
reaches the ceiling. The separation is compile-vs-retain over identical raw information: the scored
session contains no labelled `(x, M(x))` pair, so receipt retention cannot recover `M(x_q)`, and
nearest-input replay returns a stored `y != M(x_q)`. This discharges readiness blocker B2 **for this
substrate construction** and supplies substrate-validity evidence for C-MEAS-VALID only. It does **not**
promote any mechanism to Product Core, does not change C-MEAS-VALID status, and does not by itself
authorize the flagship four-arm benchmark (which independently requires B1 and B3).

## 5. Threats to validity / scope

- **Synthetic substrate, not an external agent.** This is an internally-built credential-free bank; it
  does not establish user-facing value, a market moat, or how real external comparator arms behave.
- **Disclosed identity.** `B-CROSS-SESSION-COMPILE` is success- and counter-identical to T by
  construction. It is not a certificate comparator (`retention_certifies` requires a strictly positive
  margin). The discriminating signal is carried by the retention comparators.
- **Deterministic, no sampling noise.** Rates are exact `(K-1)/K` or `1.0`; there is no statistical
  uncertainty. Validity rests on gates and control identifiability, not on power.
- **Band restriction.** The rule is evaluated only at novelty `>= 0.50`.
- **One hidden-function family.** Only the affine family `M(x)=(a*x+b) mod P` and `K in {8,10}` were
  measured; the result certifies this construction, not every memory-carried mechanism.
- **No claim promotion.** Substrate-validity evidence for C-MEAS-VALID only.

## 6. What this does not answer

Whether real external comparator arms behave like within-session receipt memory; whether the result
transfers to `K` outside `{8,10}` or other hidden-function classes; whether B1/B3 can be resolved so the
four-arm benchmark can run at all. These are recorded in `result.json.unresolved` for AUDIT/DIRECTOR.
