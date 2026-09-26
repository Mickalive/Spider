# EXP-PRODUCT-36129169543 — EXECUTE Report

**Lane:** product · **Status:** COMPLETE · **Outcome:** SUPPORTS (instrument decidable, f\* computable)

> **instrument correctness ONLY — not a scientific or product result**

This report interprets `result.json`; it does not extend it. Outcome SUPPORTS applies only to
the frozen decision row "all three parts PASS → COMPLETE / SUPPORTS". It is not an economics
result, not a PRODUCT_CORE promotion, and not evidence that inheritance pays off in production.

---

## 1. What was executed

Frozen design: `spec.json` (sha 788562e6…) / `prereg.md` (sha e7e282bc…) — immutable, unchanged
throughout. Two runner attempts were made (Section 5); attempt 2 is the reporting attempt.

| Part | Frozen criterion (summary) | Result |
|---|---|---|
| A — harness build & unit test | 5 arms, 8 counter paths non-zero, fail-closed UNKNOWN gate tested, unit tests pass, zero surrogate/default fills | **PASS** (attempt 2; attempt 1 failed on `repair=0` — see §5) |
| B — dry run on certified substrate | health-gated single-node HS256 sticky service; 5×192 trajectories; 8 counters/trajectory; B=5000 bootstrap + B=5000 block permutation; UNKNOWN gates fire; 0 crashes/fills | **PASS** |
| C — break-even reuse count | f\* from measured non-token work only; dominant quantity identified by OAT ±10%; token economics NOT_APPLICABLE/UNKNOWN | **PASS** |

Frozen table applied verbatim: PASS/PASS/PASS → `status=COMPLETE`, `outcome=SUPPORTS`.

## 2. Instrument measurements (attempt 2)

Health gate: 400 non-304 responses (200 per endpoint, ≥180 required), TN_fresh 1.0 (≥0.85),
HS256, nginx sticky, single worker, `W/` ETag seen — **pass**.

Eight counters (integer sums, per-trajectory hard reset), all arms 192/192 trajectories:

| Counter | P-SPIDER | B-COLD | B-INSTRUCTIONS | B-RAG-EMBED | B-DET-EXEC |
|---|---|---|---|---|---|
| resolve | 192 | 0 | 0 | 192 | 0 |
| bind | 384 | 0 | 0 | 384 | 384 |
| verify | 2284 | 2092 | 2092 | 2092 | 2092 |
| freshness | 2092 | 0 | 0 | 0 | 0 |
| repair | **36** | 0 | 0 | 0 | 0 |
| browser_steps | 2092 | 2092 | 2092 | 2092 | 2092 |
| requests | 2092 | 2092 | 2092 | 2092 | 2092 |
| latency_ms (sum) | 4807 | 4705 | 4851 | 4783 | 4776 |

All eight counter paths are non-zero for at least one arm (Part A gate). `repair=36` equals the
36 staleness-injected families (step-0 resource bumped under the substrate's `ep-a:` key right
before the inherited arm). Payload (auxiliary, non-counter): P-SPIDER 3,204 B vs 186,451 B all
baselines. Fail-closed gate: live-browser mode → all five arms `UNKNOWN`, `counters=null`,
`payload_bytes=null`, no fills; scripted mode → `EXECUTABLE`.

Paired CIs (P-SPIDER − baseline; family-stratified trajectory-grouped bootstrap B=5000 +
family-blocked permutation B=5000, seed 42):

| Baseline | Δpayload B (95% CI) | p | Δrequests (95% CI) | Δlatency ms (95% CI) |
|---|---|---|---|---|
| B-COLD | +954.41 [894.63, 1013.17] | 0.0002 | 0 [0, 0], p=1.0 | −0.531 [−1.234, 0.200] |
| B-INSTRUCTIONS | +954.41 [894.63, 1013.17] | 0.0002 | 0 [0, 0], p=1.0 | +0.229 [−0.497, 1.477] |
| B-RAG-EMBED | +954.41 [894.63, 1013.17] | 0.0002 | 0 [0, 0], p=1.0 | (see `ci.json`) |
| B-DETERMINISTIC-EXECUTOR | +954.41 [894.63, 1013.17] | 0.0002 | 0 [0, 0], p=1.0 | −0.161 [−0.775, 0.469] |

Attempt 1 independently showed Δlatency vs COLD +0.115 ms, CI [−0.719, 1.005] — both attempts
have a latency CI spanning 0.

## 3. Break-even reuse count (Part C)

`f* = (build_cost + verify_cost) / (serving_cost_cold − serving_cost_inherited)`

Measured inputs (attempt 2): build 1913.3 ms / 35,027 B (393 harvest requests, 180 mechanisms
distilled, 36 families); verify 106.8 ms / 0 B (36 freshness probes, all 304, auditor 36/36);
serving per trajectory: cold 971.1 B, inherited 16.7 B.

**Primary unit = bytes (the only identifiable unit here):**

- **f\*_bytes = 36.70 reuses**, post-hoc paired family bootstrap CI **[34.57, 39.15]**
  (denominator CI [894.63, 1013.17] B, strictly positive).
- OAT ±10% sensitivity → **dominant quantity: `cold_serving_cost`** (max |rel change| 0.113),
  over `build_cost` (0.100), `inherited_serving_cost` (0.002), `verify_cost` (0.000).

**Latency unit is NOT identifiable:** denominator CI spans 0 in both attempts
(attempt 1: +0.115 ms, CI [−0.719, 1.005], point f\*=14,143; attempt 2: −0.531 ms,
CI [−1.234, 0.200], f\* not computable). On this localhost substrate the 304 body
suppression saves bytes but not measurable round-trip time. Time-domain amortization
must be re-measured on a WAN-like substrate.

**Token economics: NOT_APPLICABLE / UNKNOWN** — no policy-model credential exists and no token
parameter exists in the harness by construction.

## 4. Controls

**PC-INSTRUMENT-CORRECTNESS — PASS.** All frozen expectations observed: 5/5 arms × 192/192,
eight counters, CIs compute, UNKNOWN gates fire with null counters, zero crashes / surrogate
fills / default fills / transport errors / substrate integrity failures, 39 unit tests OK.

**NC-SHUFFLED-FAMILY-STRATIFIED — MIXED (both readings reported, neither privileged).**
Statistic (pre-registered in the runner): Δ = latency_ms(B-INSTRUCTIONS) − latency_ms(B-COLD)
per trajectory — identical HTTP work in both arms, avoiding the parent's inherited
deterministic-coupling failure mode.

- *Shuffled-null reading* (frozen sentence: "Shuffled … must satisfy", matching spec
  expected-behavior "shuffled correlations near zero; p ≥ 0.20"): ρ_shuffled median −0.0045,
  per-stratum shuffled ρ_length medians all |ρ| < 0.02, blocked-permutation p = 0.972 → **PASS**.
- *Observed-rho reading* (stricter: gate on observed per-stratum ρ(Δ, L)): **FAIL** in 3/5
  strata (0.0: ρ=0.382, n=45, permutation p=0.009; 0.5: ρ=0.269, n=42, p=0.084; 0.6667:
  ρ=0.268, n=21, p=0.23); pooled ρ=+0.170. Attempt 1 failed *different* strata with
  *opposite signs* (0.3333: −0.481; 0.6667: −0.492; pooled −0.054).

Same fixed task→(L, rid) mapping in both attempts, yet signs flip → no deterministic
counter-formula coupling (and latency is measured, not formulaic); but the literal
observed-data gate failure stands as recorded. Controls are not part of the frozen
decision table; the MIXED result bounds interpretation and is queued for AUDIT/DIRECTOR.
Exactly two attempts exist, triggered by the Part A defect (§5), not by NC; neither was
discarded and no third attempt was made.

Baselines — B-COLD (absolute cold cost), B-INSTRUCTIONS (NC reference), B-RAG-EMBED
(TAU=0.30, k=5, honest counters), B-DETERMINISTIC-EXECUTOR (no-memory null): all executed
as specified and recorded in `controls`.

## 5. Attempts, defects and corrections (no outcome shopping)

1. **Attempt 1** (archived verbatim under `artifacts/attempt1/`): Part A **FAIL** —
   `repair=0` because staleness injection bumped bare `rid`s while the substrate serves
   `ep-a:`-prefixed keys (the parent's own `run_experiment.py` bumps `ep-a:{rid}`).
   Fixed to mirror the parent; **no gate, threshold, statistic or control changed.**
2. **Sensitivity defect:** OAT dropped both sides when one perturbation left the valid
   region (denominator sign flip), hiding the dominant quantity. Fixed to evaluate sides
   independently; attempt 2 reports `cold_serving_cost` correctly.
3. **Trace-hygiene defect:** the attempt-archival unlink used a wrong path, so attempt 2's
   request trace appended to attempt 1's file. Verified byte-prefix boundary (first 10,889
   lines == attempt-1 archive), split with the mixed original preserved; documented in
   `artifacts/raw/trace_file_correction.json`. Counters/CIs never read that file.

## 6. Consequences of this outcome

Per frozen `product_consequence_positive`: (1) the accounting instrument is now frozen,
unit-tested and dry-run-verified — the next unblocking event converts into a run, not an
infrastructure cycle; (2) the break-even number and its sensitivity are known *in bytes*;
(3) C-PRODUCT-ECON may advance from HYPOTHESIS toward EXPERIMENTAL on **instrument
readiness only**; (4) **no PRODUCT_CORE promotion** — this is not an economics result;
(5) the superseded Pareto packet stays superseded pending Runtime capability ledger.

Had a part failed validly, the frozen negative consequences would apply (diagnose the exact
gap; C-PRODUCT-ECON remains HYPOTHESIS; no Pareto retry). Infrastructure failure would have
been MEASUREMENT_INVALID — neither occurred in the reporting attempt.

## 7. Disclosed validity limits

See `validity_notes` in `result.json` (13 entries). Headline: localhost substrate makes
f\*_latency_ms unidentifiable; f\*_bytes is protocol-bound; the RAG arm's frozen "200 token +
150 ms cost model" text was not instantiated (token economics frozen NOT_APPLICABLE;
measurement_validity forbids synthetic jitter) — its latency is honest local retrieval time;
NC sentence ambiguity; mixed-trace correction; kernel dot-regex patch absent (fixtures have
no dotted slots; unchanged inherited note).

## 8. Key artifacts

`result.json` (contract) · `provenance.json` · code: `src/spider/eval_harness.py`,
`tests/test_eval_harness.py` (39 tests), `run_dryrun.py` · raw:
`artifacts/raw/{trajectories,request_trace,unit_tests,build,verify_pass,staleness_injection,health_gate_trace,trace_file_correction}.*` ·
derived: `artifacts/derived/{metrics_summary,breakeven,ci,null_control,health_gate,gate_demo,capability_probe,f_bytes_ci_supplement}.json` ·
attempt 1 archive: `artifacts/attempt1/`. All with sha256 in `result.json.artifacts`.
