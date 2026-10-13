# EXP-GRAPH-38205284279 — EXECUTE report

- experiment_id: `EXP-GRAPH-38205284279`
- lane: `graph` (claim `C-SEMANTIC-RESOLVE`)
- stage: EXECUTE
- frozen runner sha256: `d9edd0dc9e6a243847758c062744f4db6ffc9a93c986dcbf863f6a31bb7ffd4c` (matches `CANONICAL-RUNNER-SHA256`)
- frozen status emitted: **`MEASUREMENT_INVALID`**; decision `null`
- producer outcome: `NOT_APPLICABLE`

This report explains, but does not exceed, the frozen design and does not silently
contradict `result.json`. The evidence chain is kept distinct:
`RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT -> INTERPRETATION`.

## 1. What was executed (raw evidence)

The runner was extracted verbatim from `prereg.md#FROZEN-RUNNER` (block restored with
exactly one trailing newline) and re-hashed to the frozen `CANONICAL-RUNNER-SHA256`. The
three `freeze.json.artifact_hashes` paths were re-hashed and matched byte-for-byte. Two
`--mechanics-only` canary runs were byte-identical; the scored run was executed twice and
both outputs were byte-identical.

Raw artifacts (all in `raw_evidence/`):

| artifact | sha256 | note |
|---|---|---|
| `runner_tframe_g3.py` | `d9edd0dc…d4c` | equals canonical runner hash |
| `canary_mech_run1.json` / `canary_mech_run2.json` | `7e1c5f72…2e2` | byte-identical |
| `run_output.json` | `c80a8f42…27d` | scored stdout (286665 bytes) |
| `run_output_rerun.json` | `c80a8f42…27d` | byte-identical re-run |
| `run_output.err` | `e3b0c442…855` | empty (exit 0) |

Command: `python3 raw_evidence/runner_tframe_g3.py > raw_evidence/run_output.json`.
No model, network, browser, credential or third-party package was used (Python 3.12.15,
stdlib only; `numpy` absent).

## 2. Observation: the frozen decision rule returned no verdict

The frozen runner emitted:

```
status = "MEASUREMENT_INVALID"
decision = null
invalid_reasons = ["treatment-not-live: AXIS-G3-NEW test executed_app == 0 or == all applicable"]
```

Liveness arithmetic on `AXIS-G3-NEW` test: `executed_app = 36`,
`n_applicable_test = 36`, `unresolved_applicable = 0`, so the frozen predicate
`0 < executed_app < n_applicable_test` is **False**. Every applicable G3 test row is
executed; the structural abstention clauses fire on **0 applicable rows** on that split.

## 3. Derived measurements (frozen output, no interpretation)

Per-axis Arm A (`tframeplus`) test metrics:

| axis | coverage | pooled_false_accept | unknown_precision | selective_acc | gate |
|---|---|---|---|---|---|
| `AXIS-G3-NEW` | 1.0000 | 0.1000 | 1.0000 | 1.0000 | MET |
| `AXIS-G2-RETEST` | 0.9250 | 0.0000 | 0.8333 | 1.0000 | NOT MET (UP<0.85) |
| `AXIS-G1-PRIMARY` | 0.9464 | 0.0556 | 1.0000 | 0.9057 | MET |
| `AXIS-G1-ALTLEX` | 0.9464 | 0.0556 | 1.0000 | 1.0000 | MET |

Other derived facts:

- `selection_preserved = true` on all four axes.
- Removing C7 (`tframe_frozen`) raises G3 test pooled_false_accept 0.10 → 0.20 and G2
  test 0.00 → 0.10; C7 fires on 0 applicable rows on every axis and on 2 G3 / 4 G2 /
  2 G1 / 1 ALT OOS rows. On `AXIS-G2-RETEST` C7 fires on the named rows `oos_010` and
  `oos_014` (plus `oos_006`, `oos_023`).
- Arm B (`B-RETRIEVAL-TFIDF`) is live: G3 pooled_false_accept 0.05, coverage 0.9167,
  unknown_precision 0.8636 (gate-met) with selective_acc 0.2727, fitted `tau=0.4278`,
  `mu=0.0`; G2 pooled_false_accept 0.70 (gate-not-met). Fork = `BOTH_PASS_G3`.
- Controls moved as declared (PC-AXIS-G1-ALTLEX gate-met; NC-EXEC-ALL 0.28–0.50 vs Arm A
  0.0–0.10; NC-ABSTAIN-ALL coverage 0; shuffled 0.038–0.083; random-role 0.027–0.111;
  random-gate 0.70–0.94 with UP 0.05–0.33; incumbent 0.167–0.20).

## 4. Interpretation (clearly separated from the above)

- The frozen transaction is **not** an infrastructure failure. It completed deterministically
  and declared its own pre-declared invalidity condition. EXECUTE therefore reports
  `status=MEASUREMENT_INVALID` and `outcome=NOT_APPLICABLE`; it does not convert the state
  into a scientific negative, and it does not rewrite the frozen rule.
- The invalidity is narrow. Arm A is globally discriminating on the primary surface
  (0.10 pooled false accepts vs 0.45 execute-all), but it did not abstain on any applicable
  G3 test row, which is exactly what the frozen liveness predicate checks. Whether this
  should be treated as genuine degeneracy or as an over-strict pre-declared predicate is an
  adjudication for AUDIT/DIRECTOR, not EXECUTE.
- Independently of the invalidity, the observed gate vector would not have changed the
  headline ship decision: `AXIS-G2-RETEST` is gate-not-met on `unknown_precision`
  (0.8333 < 0.85), so both `DECIDE_SHIP_TFRAME_BROAD` and `DECIDE_SHIP_TFRAME_SCOPED` are
  unreachable and the remaining frozen branch is `DECIDE_REQUIRE_RETRIEVAL_B`. This is a
  re-evaluation of the frozen branch logic on the observed metrics; the runner's own
  emitted `decision` is `null`.
- The retrieval fork `BOTH_PASS_G3` is coupled to the same test split (a pre-declared
  `design_review.json` nonblocking finding) and Arm B's G3 selective_acc (0.2727) is far
  below Arm A's (1.0), so "both pass the gate" does not by itself indicate retrieval
  superiority on mechanism identity.

## 5. Validity threats and representation loss

- The G3 surface is synthetic, blind-authored and statically embedded; no live-Web behavior
  is measured. The applicable half is structurally simple by construction; the OOS half is
  the discriminating half.
- The frozen liveness check is evaluated only on the G3 test split; the design's
  `freeze_eligibility.treatment_liveness` was validated on G3 calibration (38/39 applicable
  executed, 1 abstention), and the test split happened to contain no applicable-row
  abstention.
- Arm B's fitted G3 margin threshold is 0.0, so on G3 the margin component is inactive;
  disclosed as a comparator representation feature.
- All four axes share the same frozen selector `B-LEX-STRONG`; a code regression there would
  invalidate treatment and baselines together.

## 6. Decision consequences (as frozen, not adjudicated here)

Per `prereg.md#9`, a `MEASUREMENT_INVALID` packet yields `decision=null`; no ship scope is
licensed and no product action follows from this packet alone. Product keeps the
conservative shipped abstention boundary until an audited verdict says otherwise. This
packet does not promote anything and does not self-authorize a successor experiment.
