# EXP-PHYSICS-35445596894 — Preregistration

## Experiment Identity

- **Experiment ID:** EXP-PHYSICS-35445596894
- **Lane:** physics
- **Claim IDs:** C-WEB-DYNAMICS
- **Parent:** EXP-PHYSICS-35403136807 (MEASUREMENT_INVALID — estimator non-convergence)
- **Created:** 2026-09-19

## 1. Question

Can bias-corrected conditional mutual information estimators (equal-weight PMI, median PMI, or direct CMI via KNN) recover stable, finite-sample-convergent measurements on the 12-state hash-routed SPA, and does any corrected estimator detect K3-K2 > 0.1 bits with valid null centering?

## 2. Background and Motivation

The parent experiment (EXP-PHYSICS-35403136807) established that the weighted-averaged Laplace-smoothed PMI estimator is **asymptotically non-convergent**: K2 PMI grows from 0.933 (N=5000) to 1.779 (N=50000, +84.5%). Null control bias floor ~0.41 bits is intrinsic to weighted averaging across heterogeneous strata, confirmed by 5 independent frameworks (parametric bootstrap 0.357, Miller-Madow 0.407, conditional entropy -0.814, within-stratum 0.417, shuffled-action 0.407).

The root cause is the weighted averaging across strata with wildly different sizes (5 to hundreds). Large strata dominate the weight but may have low PMI, while small strata above the MIN_STRATUM_SIZE=5 threshold can have high variance PMI estimates from Laplace smoothing. The interaction creates systematic upward bias that **increases** with N.

The parent handoff recommended: "Develop and validate a bias-corrected CMI estimator that converges as N increases. Apply to same SPA. Decision rule: if corrected estimator's null control |mean| < 0.1 AND K3-K2 > 0.1 with bootstrap CI lower > 0.0, the beyond-Markov question is answered."

This experiment implements exactly that recommendation.

## 3. Hypotheses

**H1 (estimator-convergence):** At least one of three bias-corrected estimators produces null control |mean| < 0.1 bits at N=5000.

**H2 (beyond-Markov):** If a convergent estimator is found, K3 PMI - K2 PMI > 0.1 bits with bootstrap CI lower > 0.0.

**H0 (no-estimator-fix):** All three corrected estimators have null |mean| >= 0.1 bits, indicating environment-level bias.

## 4. Estimators

### 4.1 B-WEIGHTED-PMI (baseline)
Original weighted-averaged PMI from parent. Re-run in this codebase for direct comparison. Each stratum's PMI is weighted by n_stratum / N_total.

### 4.2 B-EQUAL-WEIGHT-PMI
Each stratum contributes equally (weight = 1/N_strata) regardless of size. Removes large-stratum dominance. If bias is driven by size-weighting, this should eliminate it.

### 4.3 B-MEDIAN-PMI
Median of per-stratum PMI values. Robust to outlier strata with extreme PMI from small-sample Laplace smoothing. If bias is driven by a few extreme strata, median should be stable.

### 4.4 B-KNN-CMI
Direct CMI estimation via KNN classifier: I(X;Y|Z) estimated from P(Y|Z) improvement over P(Y). Bypasses strata entirely. Uses sklearn KNeighborsClassifier with k=5, operating on (history, action, next_state) tuples encoded as integers. If strata weighting is the root cause, this non-parametric approach should show lower null bias.

## 5. Data

- **SPA:** 12-state SHA256 hash-routed SPA (same as all parent experiments)
- **N=5000:** Reuse parent raw_transitions.json (SHA256: 170df6e34c78f64584f5332d61b9a705d87838b61e24eb04bdd4cc1b095c6ade). 50 sessions x 100 steps, SEED=42.
- **N=50000:** New collection (same seed, 50 sessions x 1000 steps) for convergence test.

## 6. Controls

### 6.1 Positive Control
8-state deterministic SPA: K3 PMI >= 1.0 bit, p <= 0.001, for EACH estimator independently.

### 6.2 Null Control
Shuffled-action permutation (N_SHUFFLE=500): globally reassign action labels. For each estimator, |mean_null| < 0.1 bits required. Reduced from 1000 to 4 estimators for compute feasibility; null std ~0.007 so N=500 gives adequate power.

### 6.3 Convergence Test
Best estimator (first to pass C1) re-run at N=50000. |K2(N=50000) - K2(N=5000)| <= 0.2 bits required.

## 7. Decision Rule

### Phase 1: Estimator Screening (N=5000)

For each estimator in order [weighted-PMI, equal-weight-PMI, median-PMI, KNN-CMI]:

1. **C3 gate:** If positive_control K3 < 1.0 -> estimator MEASUREMENT_INVALID, skip to next.
2. **C1 gate:** If |null_mean| >= 0.1 -> estimator fails bias correction.

### Phase 2: Signal Decomposition (if any estimator passes C1)

For first estimator to pass C1:

3. **C2 gate:** K3-K2 > 0.1 AND bootstrap 95% CI lower > 0.0 -> SURVIVES_CURRENT_TEST. Otherwise -> FALSIFIED-IN-SETTING.
4. **C4 gate:** Run at N=50000. |K2(50000) - K2(5000)| > 0.2 -> MEASUREMENT_INVALID.

### Verdict Priority

FALSIFIED-IN-SETTING > MEASUREMENT_INVALID > SURVIVES_CURRENT_TEST

If all estimators fail C1: verdict = FALSIFIED-IN-SETTING (estimator-level fix insufficient).

## 8. Validity Threats

1. **KNN CMI sensitivity to k:** Different k values may give different results. Default k=5; sensitivity to k=3 and k=10 explored if KNN passes C1.
2. **Laplace smoothing interaction with equal-weight:** Equal-weight averaging may amplify noise from small strata where Laplace smoothing has largest effect. Null control should detect this.
3. **Deterministic strata at K3:** K3 has 56.9% deterministic strata, meaning PMI=0 for those. Equal-weight and median will be pulled toward 0, which is conservative (against false positive beyond-Markov claim).
4. **Convergence test power:** 0.2-bit threshold is large relative to expected differences; chosen to detect only substantial non-convergence.
5. **In-memory SPA only:** No inference to production SPAs warranted regardless of outcome.
6. **KNN non-parametric assumptions:** KNN CMI assumes sufficient local neighborhood density; with sparse strata, may underestimate true CMI. The positive control validates this is not fatal.

## 9. Consequences

**Positive (SURVIVES_CURRENT_TEST):** Bias-corrected estimator resolves the PMI interpretability impasse. Beyond-Markov structure demonstrated on this SPA, justifying richer state representation for SPIDER and reopening the Markov-vs-beyond-Markov decomposition program.

**Negative (FALSIFIED-IN-SETTING on C1):** Bias is environment-level, not estimator-level. The PMI research program on this SPA class requires SPA redesign (0% deterministic strata, stochastic-only transitions) before any estimator can produce interpretable results. The deterministic/stochastic strata mixing is the root cause.

**Negative (FALSIFIED-IN-SETTING on C2):** Signal is Markov even with correct estimator. History conditioning adds no information beyond current state for this SPA class. SPIDER state representation need not extend beyond current state for SPA-like environments.

## 10. Consequences of Each Outcome

| Outcome | Implication for C-WEB-DYNAMICS | Next Action |
|---------|-------------------------------|-------------|
| SURVIVES_CURRENT_TEST | Beyond-Markov structure demonstrated | Test on stochastic-only SPA; then production |
| FALSIFIED (C1 all fail) | Estimator-level fix insufficient | Redesign SPA to 0% deterministic strata |
| FALSIFIED (C2) | Signal is Markov | Accept Markov; test history on stochastic SPA |
| MEASUREMENT_INVALID | Estimator not converged | Try larger N or different KNN k |
