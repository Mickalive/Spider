# EXP-PHYSICS-35476270440 preregistration

## Background

The Physics lane has established that plug-in PMI estimators (weighted, equal-weight, median) and KNN CMI all exhibit significant null bias (|shuffled-action null mean| >= 0.1 bits) on the 12-state hash-routed SPA at N=5000, even after redesigning the SPA to 0% deterministic strata (EXP-PHYSICS-35470449605). The bias is intrinsic to plug-in estimation across strata of varying size, not caused by deterministic/stochastic mixing.

The parent handoff identifies three truly orthogonal estimation frameworks that have not been tested: KSG CMI, Bayesian categorical model comparison, and likelihood-ratio tests. These frameworks avoid stratum partitioning and plug-in smoothing, potentially eliminating the bias.

## Hypotheses

- **H0 (null)**: All three orthogonal estimators have |shuffled-action null mean| >= 0.1 bits at N=5000, indicating the bias is intrinsic to estimation across strata of varying size.
- **H1 (alternative)**: At least one orthogonal estimator achieves |null_mean| < 0.1 bits, indicating the bias was specific to plug-in/KNN construction.
- **H2 (beyond-Markov, conditional on H1)**: K3 PMI - K2 PMI > 0.1 bits with bootstrap 95% CI lower > 0.0 at N=5000.

## Methods

### SPA Design
- 12-state hash-routed SPA with CANDIDATES guaranteeing all (state, action) pairs have 4 distinct next states.
- Determinism check: every (state, action) must have ≥2 unique candidates.
- N=5000 transitions (50 sessions × 100 steps), seed=42.
- Strata with <5 records skipped (MIN_STRATUM_SIZE=5).

### Estimators
1. **B-WEIGHTED-PMI**: Weighted-averaged per-stratum Laplace-smoothed conditional PMI (parent).
2. **B-EQUAL-WEIGHT-PMI**: Equal-weight per-stratum PMI.
3. **B-MEDIAN-PMI**: Median per-stratum PMI.
4. **B-KNN-CMI**: KNN CMI (k=5, alpha=1.0).
5. **B-KSG-CMI**: Kraskov-Stögbauer-Grassberger CMI (sklearn.feature_selection.mutual_info_classif, k=5, alpha=1.0).
6. **B-BAYESIAN-MODEL**: Bayesian categorical transition model (Dirichlet-Multinomial, variational Bayes).
7. **B-LIKELIHOOD-RATIO**: Likelihood-ratio test (full vs reduced model, Bonferroni corrected).

### Null Control
- Shuffled-action null: 500 permutations, action labels shuffled within session.
- Unit of permutation: action-label within session.
- Threshold: |null mean| < 0.1 bits.

### Positive Control
- 8-state deterministic SPA: K3 PMI ≥1.0 bit, p ≤0.001.

### Analysis Plan
- Compute weighted mean PMI across strata for each estimator.
- Compute shuffled-action null distribution (500 permutations).
- Apply Bonferroni correction for 7 comparisons (α=0.00714).
- Decompose bias by stratum size (5-9, 10-19, 20-49).
- If any estimator passes C1, compute K3-K2 difference with bootstrap 95% CI (200 resamples).

## Decision Rules

### FALSIFIED-IN-SETTING
If ANY of:
1. All 7 estimators have |null mean| ≥0.1 bits (C1 fails).
2. Positive control fails for any estimator passing C1 (C3).
3. Determinism check fails (C6).

### MEASUREMENT_INVALID
If:
4. <30% of strata have ≥5 records.
5. <2 non-empty size buckets.
6. Any orthogonal estimator implementation fails.

### SURVIVES_CURRENT_TEST
Requires ALL:
- At least 1 estimator has |null mean| <0.1 bits (C1 passes).
- Positive control passes for that estimator (C3).
- Determinism check passes (C6).
- ≥2 non-empty size buckets (C7).

### Phase 2 (beyond-Markov)
Only if SURVIVES on C1:
- K3-K2 >0.1 bits with bootstrap CI lower >0.0 (C2).
- |K2(N=50000) - K2(N=5000)| ≤0.2 bits (C4).

## Expected Outcomes

- **If H1 passes**: PMI research program unblocked; valid beyond-Markov testing possible.
- **If H0 confirmed**: Pivot to fundamentally different detection paradigms or production Web data.

## Deviation Plan

- If any orthogonal estimator fails due to implementation issues, report as MEASUREMENT_INVALID with explicit error.
- If Bayesian inference fails to converge, use maximum likelihood estimate as fallback and note the deviation.
- If sklearn KSG unavailable, implement KNN CMI with distance-weighted Laplace as approximation.

## Preregistration Timing

This preregistration is frozen before any outcome data is inspected. Any analysis changes after seeing results will be exploratory and clearly labeled.