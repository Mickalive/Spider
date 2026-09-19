# EXP-PHYSICS-35470449605 — Preregistration

## Status

DESIGN PHASE. Not yet frozen. All outcomes below are pre-declared; no results have been observed.

---

## 1. Question

Does redesigning the 12-state hash-routed SPA to 0% deterministic strata (all CANDIDATES lists contain only distinct next states) eliminate the per-stratum plug-in PMI null bias that persists at +0.742 bits for small strata under the shuffled-action null — and does this redesign enable a valid beyond-Markov K3-K2 test, or is the bias intrinsic to plug-in estimation regardless of determinism ratio?

## 2. Hypotheses

**H0 (null — bias is intrinsic):** All four estimators (weighted-PMI, equal-weight-PMI, median-PMI, KNN-CMI) have |shuffled-action null mean| >= 0.1 bits at N=5000 on the fully-stochastic SPA. The per-stratum plug-in PMI bias persists despite removing all deterministic strata.

**H1 (alternative — bias is environment-caused):** At least one estimator achieves |null_mean| < 0.1 bits on the fully-stochastic SPA. The bias was partially or fully caused by deterministic/stochastic strata mixing.

**H2 (beyond-Markov, conditional on H1):** K3 PMI - K2 PMI > 0.1 bits with bootstrap 95% CI lower > 0.0 at N=5000 on the fully-stochastic SPA, demonstrating valid beyond-Markov detection.

## 3. State Representation

- **State:** URL with hash fragment (same 12-state layout as parent)
- **Action:** One of {form_submit, button_click, js_navigate, menu_select}
- **History:** K=0 (Markov), K=1, K=2, K=3 URL history tuples
- **Target:** url_after (next URL)

## 4. SPA Redesign (0% Deterministic Strata)

The parent SPA has CANDIDATES with 4 candidates per (state, action). Some candidates contain duplicates, creating deterministic strata (where the hash always maps to the same next state regardless of history).

**Redesign:** For every (state, action) pair, all 4 candidates must be distinct integers in {0,...,11} with no self-loops as the sole candidate. Specifically:
- Each CANDIDATES[state][action] list contains exactly 4 distinct next-state indices
- No list contains the same index twice
- The set of 4 candidates covers at least 2 distinct states (trivially satisfied by distinct list)

**Verification:** The determinism check computes, for each (state, action), the fraction of transitions where only one unique next state appears across all collected transitions. If any (state, action) pair has determinism == 1.0, the experiment is MEASUREMENT_INVALID.

**Rationale:** With all strata stochastic, H(S_next | state, action) > 0 for every stratum. If the bias was caused by deterministic strata (where PMI = 0 for the stratum but the weighted average still accumulates positive bias from stochastic strata), this redesign eliminates the source. If the bias persists, it is intrinsic to the plug-in estimator's behavior on strata of varying size with Laplace smoothing.

## 5. Estimators

Same 4 estimators as parent (EXP-PHYSICS-35445596894), identical implementation for comparability:

1. **Weighted-PMI:** Weighted average of per-stratum plug-in conditional PMI, weighted by stratum record count. Laplace alpha=1.0. Parent null_mean = 0.407 bits.

2. **Equal-weight-PMI:** Unweighted average of per-stratum PMI. Parent null_mean = 0.704 bits (worse due to small-stratum up-weighting).

3. **Median-PMI:** Median of per-stratum PMI values. Parent null_mean = 0.686 bits.

4. **KNN-CMI:** KNN mutual information estimator (k=5, alpha=1.0, distance-weighted Laplace smoothing in (state, action) space). Parent null_mean = -0.262 bits (negative bias from extra dimension).

All estimators applied to K=2 state-history records (same as parent primary analysis).

## 6. Sampling Policy

- **N=5000 transitions:** 50 sessions x 100 steps, seed=42
- **N=50000 transitions:** 500 sessions x 100 steps, seed=42 (convergence test, Phase 2 only if H1 passes)
- **MIN_STRATUM_SIZE:** 5 (strata with fewer records are excluded from PMI computation)
- **Session structure:** Each session starts from a random state, actions chosen uniformly at random

## 7. Unit of Analysis

Per-stratum PMI: one PMI value per unique (url_before, history_K) stratum. Weighted by stratum record count for aggregate.

## 8. Holdout

None (all N=5000 used for primary analysis). Convergence test uses N=50000 as descriptive, not confirmatory.

## 9. Nulls and Baselines

- **Primary null:** Shuffled-action permutation (N_SHUFFLE=500). For each permutation, shuffle action labels within each session, recompute per-stratum PMI, take weighted mean.
  - Pass criterion: |mean(shuffled nulls)| < 0.1 bits
  - Unit of permutation: action labels within session (preserves session structure)
- **Baselines:** B-WEIGHTED-PMI, B-KNN-CMI, B-EQUAL-WEIGHT-PMI, B-MEDIAN-PMI (descriptive comparison to parent values)
- **Stratum decomposition:** B-STRATUM-SIZE-DECOMPOSITION into buckets {5-9, 10-19, 20-49} to test whether bias becomes uniform across sizes

## 10. Primary Metric

- **C1:** |shuffled-action null mean| < 0.1 bits for at least one estimator
- **C2 (Phase 2):** K3 PMI - K2 PMI > 0.1 bits with bootstrap 95% CI lower > 0.0

## 11. Expected Direction

If H1 is true (bias is environment-caused): |null_mean| should decrease relative to parent (0.407 bits). The decrease may be partial (e.g., from 0.407 to 0.15) or complete (< 0.1).

If H0 is true (bias is intrinsic): |null_mean| remains >= 0.1 regardless of determinism ratio. The stratum-size decomposition may show the same monotonic pattern (+0.742 at size 5-9, etc.) or a different but still biased pattern.

## 12. Uncertainty Method

- Bootstrap: 200 trajectory-block resamples for CI of K3-K2 difference
- Permutation: 500 shuffled-action permutations for null distribution
- Bonferroni: 2 primary comparisons (weighted-PMI, KNN-CMI), alpha=0.025

## 13. Adequacy Rule

N=5000 is adequate if >= 30% of (state, action) strata have >= 5 records. With 12 states x 4 actions = 48 potential strata and N=5000 transitions, expected stratum size ~104, so this criterion should be met comfortably.

## 14. Falsification / Survival Rule

**FALSIFIED-IN-SETTING** if ANY of:
- C1 fails (all 4 estimators |null_mean| >= 0.1)
- C3 fails (positive control K3 < 1.0 bit or p > 0.001)
- Determinism check fails (any (state, action) has < 2 unique candidates in collected data)

**MEASUREMENT_INVALID** if:
- < 30% of strata have >= 5 records
- < 2 non-empty size buckets in stratum decomposition

**SURVIVES_CURRENT_TEST** if ALL of:
- C1 passes (>= 1 estimator |null_mean| < 0.1)
- C3 passes
- Determinism check passes
- >= 2 non-empty size buckets

**Phase 2 (beyond-Markov) SURVIVES** if additionally:
- C2 passes (K3-K2 > 0.1, CI lower > 0.0)
- C4 passes (|K2(N=50000) - K2(N=5000)| <= 0.2 for best estimator)

## 15. Representation Loss

- URL-only state representation (no DOM, a11y, visual)
- Hash-based next-state selection (deterministic given history, but with stochastic branching)
- In-memory simulation (no browser/network)
- Laplace smoothing introduces small-sample bias (alpha=1.0)
- Weighted averaging across strata of varying size introduces the bias we are trying to diagnose

## 16. Validity Threats

- **V1 (estimator-specific):** The 4 estimators may all share a common bias mechanism not shared by truly orthogonal methods (KSG, Bayesian). A negative result (H0) does not close the entire estimation domain.
- **V2 (SPA ceiling):** The 12-state hash-routed SPA is a simulation, not a real Web SPA. Results may not generalize to production SPAs with DOM, auth, latency, or non-hash routing.
- **V3 (sample size):** N=5000 may be insufficient for some strata to reach stable PMI estimates, especially if the stochastic SPA has higher entropy than the parent.
- **V4 (determinism check):** The determinism check measures empirical determinism in collected data, not theoretical determinism of the CANDIDATES design. With N=5000, some (state, action) pairs may not have enough samples to verify stochastic behavior.
