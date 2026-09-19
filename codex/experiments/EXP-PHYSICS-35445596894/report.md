# EXP-PHYSICS-35445596894 — Execution Report

## 1. Identity

- **experiment_id**: `EXP-PHYSICS-35445596894`
- **lane**: physics
- **claim**: C-WEB-DYNAMICS (see `codex/claim_state.json`)
- **parent**: `EXP-PHYSICS-35403136807` (status `MEASUREMENT_INVALID`; verdict "the positive K3−K2 measurement is invalid; the underlying question whether Web navigation is action-history-dependent remains open")
- **request reason**: pulse
- **frozen inputs**: `request.json`, `spec.json`, `prereg.md`, `freeze.json` (immutable; untouched)

## 2. Frozen question and hypothesis (from `spec.json` / `prereg.md`)

- **Question**: Do bias-corrected conditional-MI estimators reveal action-history (K3) dependence beyond state-history (K2) dependence in the 12-state hash-routed SPA at N=5000?
- **Hypothesis H1 (pre-registered expectation)**: The parent's positive K3−K2 result was caused by estimator bias concentrated in large/deterministic strata; equal-weight, median and KNN-CMI corrections should center the shuffled-action null near zero (< 0.1 bits) and thereby recover a trustworthy K3−K2 measurement.
- **H0 (falsifier C1)**: ALL corrected estimators have null control `|mean| ≥ 0.1` bits at N=5000 → bias is environment-level (deterministic/stochastic strata mixing + plug-in estimation), not estimator-level → `FALSIFIED-IN-SETTING`.
- **Decision rule (priority)**: `FALSIFIED-IN-SETTING` > `MEASUREMENT_INVALID` > `SURVIVES_CURRENT_TEST`.
- **Gate order**: C3 positive control (8-state deterministic SPA; K3 ≥ 1.0 bit, p ≤ 0.001) → C1 null control (500 shuffled-action permutations, `|mean| < 0.1` on K2 records) → C2 (first passer: K3−K2 > 0.1 with 200-resample bootstrap CI lower > 0) → C4 (convergence `|K2(50k)−K2(5k)| ≤ 0.2`).
- **Estimator order**: B-WEIGHTED-PMI (baseline) → B-EQUAL-WEIGHT-PMI → B-MEDIAN-PMI → B-KNN-CMI.
- **Constants**: MIN_STRATUM_SIZE=5; SEED=42; N=5000 reuses parent `raw_transitions.json`; N=50000 freshly simulated.

## 3. Execution

- Environment: Python 3.12.14, numpy 2.5.3, scikit-learn 1.9.1; in-memory simulation per frozen `measurement_validity`.
- Code: `run_experiment.py` (sha `f78fc85f...`); exploratory non-gating addendum `explore.py` (sha `8188262e...`).
- Fidelity checks passed before measurement:
  - Regenerated N=5000 transitions **deep-equal** the parent `raw_transitions.json`; file SHA256 `170df6e3...` matches the frozen hash; in-memory sort_keys SHA `46ed606a...` matches parent `raw_results.sha_raw`.
  - Weighted estimator replicating parent: K2=0.933244, K3=1.220508, positive control K3=1.805624 (p=0.000999), N=50000 K2=1.778725 — all equal to parent values exactly.
- Wall time 92.6 s (screening), +64.3 s (exploratory).
- All raw evidence preserved: `raw_results.json`, `raw_exploratory.json`, `raw_transitions_n50000.json`, `raw_output.txt` (hashes in `result.json.artifacts`).

## 4. Raw evidence → observation → measurement → interpretation (kept distinct)

### 4.1 Positive control (validates the measurement pipelines) — raw evidence in `raw_results.json.screening[*].positive_control_*`

| Estimator | Positive-control K3 (bits) | p-value | Gate C3 |
|---|---|---|---|
| B-WEIGHTED-PMI | 1.805624 | 0.000999 | PASS |
| B-EQUAL-WEIGHT-PMI | 1.809851 | 0.000999 | PASS |
| B-MEDIAN-PMI | 1.872700 | 0.000999 | PASS |
| B-KNN-CMI | 1.190835 | 0.000999 | PASS |

*Observation*: every estimator pipeline detects the deterministic 8-state SPA signal (K3 ≥ 1.0, p at permutation floor 1/1001). *Interpretation*: the C1 failures below are not execution defects; each estimator measures what it claims to measure on known signal.

### 4.2 Null control (the deciding measurement) — `raw_results.json.screening[*].null_control`

| Estimator | K2 observed (bits) | K3 observed (bits) | K3−K2 (bits) | Null mean (bits) | Null std | |null mean| vs 0.1 |
|---|---|---|---|---|---|---|
| B-WEIGHTED-PMI | 0.933244 | 1.220508 | +0.287265 | +0.407057 | 0.007268 | 4.07×, 54.2σ |
| B-EQUAL-WEIGHT-PMI | 1.490475 | 1.446247 | −0.044228 | +0.704217 | 0.012815 | 7.04×, 47.2σ |
| B-MEDIAN-PMI | 1.510964 | 1.476821 | −0.034143 | +0.685611 | 0.018312 | 6.86×, 32.0σ |
| B-KNN-CMI | 0.023350 | 0.203143 | +0.179793 | −0.261904 | 0.007456 | 2.62×, 48.5σ |

(Null = global shuffled-action permutation, N=500, seed 42, K2 records, parent precedent.)

*Observation*: all four estimators have `|null_mean| ≥ 0.1` bits by margins of 2.6–7.0×, all 32–54 standard errors from the threshold; the KNN null is *negative* (−0.262 bits).
*Measurement*: C1 fails for every estimator → falsifier C1 triggered (the frozen rule requires ALL three corrected estimators to fail; here all four, including the baseline, fail).
*Interpretation*: **FALSIFIED-IN-SETTING** — the bias is environment-level (mixing of deterministic and stochastic strata plus small-sample plug-in bias), not estimator-level. The K3−K2 sign is estimator-dependent (+0.287 weighted, −0.044 equal-weight, −0.034 median, +0.180 KNN) and therefore not a trustworthy signal under any of these estimators.

### 4.3 Mechanistic decomposition (exploratory, non-gating) — `raw_exploratory.json`

Per-stratum plug-in PMI under shuffled actions, weighted framework, K2 records, 100 shuffles:

| Stratum size | Mean null stratum PMI (bits) | Median (bits) | n stratum-observations |
|---|---|---|---|
| 5–9 | +0.7424 | +0.7219 | 31,300 |
| 10–19 | +0.5712 | +0.5610 | 8,000 |
| 20–49 | +0.3787 | +0.3617 | 500 |

*Observation*: per-stratum null bias decreases monotonically with stratum size; it is *largest in the small strata*, and it is positive even in fully stochastic strata.
*Interpretation*: This falsifies the preregistered mechanistic hypothesis H1 (bias caused by large-stratum dominance). Because equal-weight/median averaging promote small strata, the corrections make the aggregate null bias *worse* (0.704 / 0.686 vs 0.407). The root cause is the per-stratum plug-in PMI's small-sample bias, which is pervasive rather than concentrated.

### 4.4 Descriptive convergence (non-gating; the frozen C4 gate never engages)

K2 at N=50000 vs N=5000 (bits): weighted 1.778725 (+0.845), equal-weight 1.737681 (+0.247), median 1.883523 (+0.373), KNN 1.284007 (+1.261). K3 at N=50000: 1.525216 / 1.542375 / 1.533341 / 0.801997.

*Observation*: no estimator is within the frozen 0.2-bit convergence band at N=50000; all continue to drift with sample size. *Interpretation*: convergence to a stable estimate is not achievable with these estimators on this SPA at these sample sizes — descriptive context only.

### 4.5 Determinism and parent-packet reproducibility finding

- Determinism at N=5000, recomputed with the parent's own code on the parent's own data: K2 (state-history) det_ratio = 0.315 (407/1292); **K3 (action-history) det_ratio = 0.108 (89/821)**.
- The parent packet records `determinism_K3`: 467/821, det_ratio 0.569, and its narrative attributes the K3-K2 gap to "56.9% deterministic dilution". **This record is not reproducible** from the parent's code and data.
- All other parent quantities replicate exactly (Section 4, §3).

*Validity consequence*: this experiment's verdict rests on the C1 null gate and is unaffected by the discrepancy. The parent-packet determinism record and its narrative reasoning should be corrected by the parent's owners; the discrepancy is recorded in `result.json.observations` and `unresolved`.

## 5. Controls ledger (see `result.json.controls` for full detail)

| Control id | Expected | Observed | Status |
|---|---|---|---|
| B-WEIGHTED-PMI | replicate parent (K2 0.933, null 0.407) | exact replication; null 0.407057 | PASS (replicates, re-fails C1 as frozen) |
| B-EQUAL-WEIGHT-PMI | null < 0.1 if bias were large-stratum-driven | null 0.704217 | FAIL (C1) |
| B-MEDIAN-PMI | null < 0.1 if bias were outlier-driven | null 0.685611 | FAIL (C1) |
| B-KNN-CMI | lower null bias if strata-weighting were root cause | null −0.261904 | FAIL (C1) |
| C3-POSITIVE-CONTROL | K3 ≥ 1.0, p ≤ 0.001, all 4 estimators | 1.806 / 1.810 / 1.873 / 1.191, p=0.000999 | PASS |
| C1-NULL-CONTROL | \|null mean\| < 0.1, all estimators | 0.407 / 0.704 / 0.686 / 0.262 | FAIL → FALSIFIED-IN-SETTING |
| C2-K3-MINUS-K2-BOOTSTRAP | K3−K2 > 0.1, CI lower > 0 (first passer) | not run — no C1 passer | NOT_APPLICABLE |
| C4-CONVERGENCE-N50000 | \|K2(50k)−K2(5k)\| ≤ 0.2 (passer) | not run as gate — no C1 passer | NOT_APPLICABLE |

## 6. Result

- `status`: COMPLETE (valid measurements, no infrastructure failure)
- `outcome`: FALSIFIES (valid scientific negative)
- `verdict`: **FALSIFIED-IN-SETTING**
- Claim update this experiment supports (for DIRECTOR): C-WEB-DYNAMICS K3−K2 hypothesis remains unestablished; the specific estimator-bias-correction path (equal-weight/median/KNN) is rejected as a remedy in this setting.

## 7. Consequences of the outcome

**For the claim**: the "action-history dependence" hypothesis is not supported by any estimator tested; more importantly, the failure of all four estimators to center the null falsifies the pre-registered mechanistic account (bias from large-stratum dominance) and shows the environment-level bias is intrinsic to plug-in stratum PMI estimation on mixed deterministic/stochastic SPAs. The K3−K2 question remains **open** (unknown), not answered in the negative.

**For the next experiment (informing, not prescribing)**:
1. *Truly orthogonal estimators* are untested and should be the next attack: the parent handoff's `do_not_assume` list flags none of KSG-CMI, Bayesian model comparison, likelihood-ratio tests, or consistently smoothed joint counts; any such estimator must pass the same C3→C1 pipeline (positive control + `|null| < 0.1` at N=5000) before trust.
2. A KNN parameter sweep (k, alpha, metric) is cheap and might center the null; but the negative KNN null (−0.262 bits) suggests smoothing-induced depression rather than a fixable configuration.
3. *SPA redesign*: the stratum-size decomposition shows the plug-in bias persists in stochastic strata, so a "0% deterministic strata" redesign may NOT eliminate it — test that claim before prescribing redesign.
4. Determinism accounting (K2 0.315 / K3 0.108) should replace the parent's unreproducible 0.569 record in any downstream narrative.

## 8. Validity notes (summary; full list in `result.json.validity_notes`)

- Valid negative, not infrastructure failure: all gates executed with real measurements; margins 32–54σ.
- Null control uses K2 records (parent precedent) as the frozen spec does not pin the condition; p-values descriptive; the `|mean|` threshold is the decision criterion.
- KNN CMI operationalized as I(Y;X|Z)=E log2 P(Y|Z,X)/P(Y|Z) (k=5, Laplace α=1.0, self-neighbors excluded); frozen "P(Y|Z) improvement over P(Y)" read as the conditional version.
- KNN positive-control p uses global shuffled-action permutation (stratum-free estimator); stratum estimators use within-stratum url_after permutation (parent precedent).
- Simulation-only measurement; no generalization to production SPAs or browser-collected data.

## 9. Unresolved

Full list in `result.json.unresolved`. Highlights: whether any estimator can center the null on this SPA class (open); the true sign/magnitude of beyond-Markov structure (unmeasured); whether 0%-deterministic-strata SPAs escape the bias (untested); KNN parameterizations (untested); asymptotics beyond N=50000 (unknown); parent determinism_K3 record root cause (unknown).