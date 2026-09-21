# EXP-PHYSICS-35403136807 — Execution Report

## Verdict: MEASUREMENT_INVALID

**Status:** MEASUREMENT_INVALID (C4 null control fails: |mean| = 0.407 > 0.1 threshold)
**Outcome:** NOT_APPLICABLE (measurement invalidation prevents scientific conclusion on Markov-vs-beyond-Markov question)

---

## 1. Executive Summary

This experiment attempted to resolve whether the 0.933-bit K2 PMI signal on the 12-state hash-routed SPA is Markov or beyond-Markov, by comparing K3 PMI (action-history conditioned) vs K2 PMI (state-history conditioned). The measurement is **MEASUREMENT_INVALID** because the PMI estimator has systematic positive bias (null control |mean| = 0.407 bits) that prevents interpreting any absolute PMI value. Furthermore, the K3-K2 difference test — designed to be immune to null centering — also fails: the bootstrap 95% CI for K3-K2 includes zero, and the bootstrap is not centered on the observed value, indicating fundamental estimator instability.

The most important finding is that the PMI estimator's bias is **asymptotic**, not finite-sample: at N=50000 (10x the primary sample), K2 PMI *increases* from 0.933 to 1.779 bits, rather than converging to a stable value. This rules out finite-sample explanations and indicates the weighted-averaged PMI estimator does not converge to a meaningful information-theoretic quantity.

## 2. Replication

| Metric | Parent Value | This Experiment | Status |
|--------|-------------|-----------------|--------|
| K1 PMI | 1.531 | 1.530902 | Replicated |
| K2 PMI | 0.933 | 0.933244 | Replicated (exact) |
| K3 PMI | 1.221 | 1.220508 | Replicated (within rounding) |

All three PMI values replicate the parent experiment (EXP-PHYSICS-35402003775) within rounding error, confirming measurement reproducibility of the point estimates. The issue is not reproducibility but the *interpretability* of the estimator.

## 3. Primary Test: K3 - K2 Difference

| Statistic | Value |
|-----------|-------|
| K3 - K2 point estimate | 0.287265 bits |
| Bootstrap mean difference | -0.108602 bits |
| Bootstrap 95% CI | [-0.275462, 0.080288] |
| CI includes 0? | **Yes** |
| Bootstrap std | 0.094866 |

The point estimate K3 - K2 = 0.287 bits is positive, which naively suggests action-history conditioning adds information beyond state-history conditioning. However:

1. **The bootstrap 95% CI includes zero** [-0.275, 0.080], so the difference is not statistically significant.
2. **The bootstrap mean (-0.109) is not centered on the observed value (0.287)**. This is a severe anomaly: a valid bootstrap should be approximately centered on the observed statistic. The discrepancy indicates that K3 PMI is highly unstable under session resampling.

**Diagnosis of bootstrap instability:** K3 uses action-history strata (821 total, 510 used) while K2 uses state-history strata (1292 total, 398 used). K3's strata are more fragmented because they depend on consecutive action sequences, which are rarer than consecutive state sequences. When bootstrap resampling drops a session, entire K3 strata can disappear, reducing the K3 estimate. When a session is duplicated, small strata get inflated. The net effect is that K3 is systematically reduced in bootstrap samples (mean K3_boot = 0.824 vs observed 1.221) while K2 is stable (mean K2_boot = 0.933).

## 4. Controls

### C3: Positive Control (PASS)
- 8-state deterministic SPA, K3 PMI = 1.806 >= 1.0 bit, p = 0.001
- The measurement pipeline works correctly on fully deterministic environments

### C4: Null Control (FAIL → MEASUREMENT_INVALID)
- Shuffled-action null mean = 0.407 bits, far exceeding the 0.1 threshold
- This is a **systematic positive bias** in the PMI estimator, not a genuine signal
- Root cause: weighted averaging across strata with heterogeneous sizes (5 to hundreds of records) combined with Laplace smoothing creates a systematic upward bias
- Same finding as parent experiment

### C2: K2 vs K1 (UNEXPECTED)
- K2 = 0.933 < K1 = 1.531, meaning conditioning on current state REDUCES action PMI
- This is expected in this SPA: K1 uses 12 coarse unconditional strata where action is highly predictive; K2 uses 1292 fine-grained state-history strata where many are small and noisy

## 5. Exploratory: N=50000 Bias Scaling

| Metric | N=5000 | N=50000 | Change |
|--------|--------|---------|--------|
| K2 PMI | 0.933 | 1.779 | +84.5% |
| Strata used | 398/1292 | 1436/1540 | More strata captured |
| Determinism ratio | 0.315 | 0.026 | Lower at scale |

K2 PMI *increases* from 0.933 to 1.779 at 10x sample size. This demonstrates that the PMI estimator bias is **asymptotic**, not finite-sample. This contradicts H2 (which predicted the bias would decrease with N) and has critical implications:

- The null bias floor does not vanish at large N
- The weighted-averaged PMI does not converge to a stable information-theoretic quantity
- All prior absolute PMI measurements (K0 through K3) are affected by this asymptotic bias

## 6. Interpretation

**Why the Markov-vs-beyond-Markov question cannot be answered:**

The frozen decision rule gates on C4 (null control). C4 fails with |mean| = 0.407 >> 0.1. Per the preregistered rules, this triggers MEASUREMENT_INVALID regardless of the C1 result. The experiment is measurement-invalid.

**Even without C4 gating, the result would be inconclusive:**
- C1 requires BOTH K3-K2 > 0.1 AND CI lower > 0.0. The CI includes zero, so C1 fails.
- The bootstrap instability means the K3-K2 difference test is unreliable even as a ratio test.

**The root cause is the estimator, not the SPA:**

The hash-routed SPA is well-defined and reproducible. The deterministic/stochastic strata mix is stable. The issue is specifically the *weighted-averaged Laplace-smoothed PMI estimator* which:
1. Has a systematic positive bias that scales with N (asymptotic)
2. Produces different bias levels for different conditioning orders (K1, K2, K3)
3. Is not robust to trajectory-level resampling for high-order conditioning (K3)

## 7. Implications for Physics Lane

This experiment demonstrates that the PMI estimator requires fundamental revision before any PMI-based claims can be made. The recommended next steps:

1. **Estimator revision:** Replace weighted-averaged PMI with a bias-corrected estimator. Options:
   - Unweighted (equal strata weight) PMI
   - Median PMI across strata
   - Direct CMI estimation (e.g., KSG estimator or Bennett et al.)
   - Proper null centering using the strata distribution
2. **Re-run Markov-vs-beyond-Markov test** with corrected estimator
3. **Characterize asymptotic bias:** Does K2 PMI plateau at large N, or continue growing?

## 8. Artifact Inventory

| Artifact | Role | SHA256 |
|----------|------|--------|
| raw_transitions.json | raw | 46ed606a08615b86... |
| raw_results.json | derived | See provenance.json |
| run_experiment.py | code | See provenance.json |
| raw_output.txt | raw | See provenance.json |
| result.json | derived | This file |
| report.md | derived | This file |
| provenance.json | derived | This file |
