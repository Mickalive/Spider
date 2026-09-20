# EXP-PHYSICS-35530591329 — Preregistration

## 1. Overview

**Experiment ID:** EXP-PHYSICS-35530591329  
**Lane:** physics  
**Claim IDs:** C-MEAS-VALID, C-WEB-DYNAMICS  
**Parent:** EXP-PHYSICS-35510154353 (FALSIFIED-IN-SETTING)  
**Date:** 2026-09-20  

**Question:** Can plug-in KL with alpha=0.1 or bias-corrected MLE (alpha=0) achieve |shuffled-action null_mean| < 0.1 bits while maintaining positive_control_k3 >= 0.5 bits and p <= 0.001 at N=5000 on the stochastic 12-state SPA — thereby resolving whether hyperparameter tuning unblocks the CMI pathway, or whether null centering degrades with reduced smoothing?

## 2. Hypotheses

- **H0 (null):** For all tested alpha values (0, 0.01, 0.1, 0.5, 1.0), plug-in KL fails to achieve BOTH |shuffled-action null_mean| < 0.1 bits AND positive_control_k3 >= 0.5 bits on the stochastic SPA at N=5000.
- **H1 (alternative):** At least one alpha achieves BOTH |null_mean| < 0.1 bits AND positive_control_k3 >= 0.5 bits on the stochastic SPA at N=5000.
- **H2 (beyond-Markov, conditional on H1):** K3 CMI - K2 CMI > 0.1 bits with bootstrap 95% CI lower > 0.0 at N=5000 for the best alpha passing C1+C3.

## 3. Design

### 3.1 Environment
- Stochastic 12-state SPA: 50% deterministic hash routing + 50% uniform random over 4 CANDIDATES per (state, action).
- Same STATES, ACTIONS, CANDIDATES as parent EXP-PHYSICS-35482477045.
- True I(Y;A|Z) ≈ 1.52 bits (audit-confirmed via exact enumeration and N=50000 empirical plug-in).

### 3.2 Data Collection
- N=5000 transitions (50 sessions × 100 steps).
- Seed=42 for stochastic SPA RNG, independent of session RNG.
- Design verification: all 48/48 (state, action) pairs have 4 distinct candidates.

### 3.3 Estimator
- Plug-in KL estimator: D_KL(P(Y|Z,A) || P(Y|Z)) = Σ_{z,a,y} P(z,a,y) × log₂[P(y|z,a)/P(y|z)].
- Laplace smoothing with variable alpha: {0 (MLE), 0.01, 0.1, 0.5, 1.0}.
- Z = (current_state, history_action_K=3) for K3; Z = (current_state, history_state_K=2) for K2.

### 3.4 Controls
- **C1 (null centering):** Shuffled-action within-session null, 500 permutations per alpha. |mean| < 0.1 bits.
- **C3 (positive control sensitivity):** Positive control on stochastic SPA, K3 ≥ 0.5 bits, permutation p ≤ 0.001.
- **C6 (SPA design):** 48/48 (state, action) pairs with 4 distinct candidates.
- **C7 (stratum coverage):** ≥2 non-empty stratum size buckets.

### 3.5 Baselines
- **B-DETERMINISTIC-SPA:** MLE on deterministic SPA (I=0 by construction).
- **B-PERMUTATION-TEST:** Permutation test conditioned on (state, action) strata.
- **B-PARENT-KSG-K5:** Replicate parent KSG k=5 results.
- **B-KSG-CMI-K10:** KSG CMI with k=10.

## 4. Measures

### 4.1 Primary Measures
- **C1:** |shuffled-action null_mean| < 0.1 bits for at least one alpha.
- **C3:** positive_control_k3 ≥ 0.5 bits with p ≤ 0.001 for at least one alpha passing C1.

### 4.2 Secondary Measures
- **C2 (beyond-Markov):** K3 CMI - K2 CMI > 0.1 bits with bootstrap 95% CI lower > 0.0.
- **C4 (convergence):** |K2(N=50000) - K2(N=5000)| ≤ 0.3 bits for the best alpha.

### 4.3 Design Verification
- **C6:** All 48 (state, action) pairs have 4 distinct candidates.
- **C7:** ≥2 non-empty stratum size buckets.

## 5. Analysis

### 5.1 Per-Alpha Analysis
For each alpha in {0, 0.01, 0.1, 0.5, 1.0}:
1. Compute K3 on stochastic SPA.
2. Compute K2 on stochastic SPA.
3. Run 500 within-session shuffled-action permutations, compute null_mean and |null_mean|.
4. Compute positive control K3 and permutation p (1000 permutations).
5. Compute degenerate control K3 on deterministic SPA.

### 5.2 Decision Rule Application
Apply frozen decision rule (Section 6) to determine verdict.

### 5.3 Phase 2 (conditional on SURVIVES)
If any alpha passes C1+C3:
1. Compute K3 - K2 for that alpha.
2. Compute bootstrap 95% CI for K3 - K2 (200 trajectory-block resamples).
3. Compute convergence: K2 at N=50000 vs N=5000.

## 6. Decision Rules

### 6.1 Verdict Priority
FALSIFIED-IN-SETTING > MEASUREMENT_INVALID > SURVIVES_CURRENT_TEST.

### 6.2 FALSIFIED-IN-SETTING Triggers
1. **C1:** All alphas have |shuffled-action null mean| ≥ 0.1 bits at N=5000.
2. **C3:** For any alpha passing C1, positive_control_k3 < 0.5 bits OR permutation p > 0.001.
3. **C6:** Fewer than 48/48 (state, action) pairs with 4 distinct candidates.

### 6.3 MEASUREMENT_INVALID Triggers
4. Fewer than 30% of (state, action) strata have ≥5 records at N=5000.
5. stratum_size_bias_decomposition has <2 non-empty size buckets.
6. Any alpha implementation fails (e.g., missing dependency, convergence error).

### 6.4 SURVIVES_CURRENT_TEST Requires
- **(C1):** At least 1 alpha has |null_mean| < 0.1 bits.
- **(C3):** Positive control passes for that alpha (K3 ≥ 0.5 bits, p ≤ 0.001).
- **(C6):** Design check passes.
- **(C7):** ≥2 non-empty size buckets.

### 6.5 Phase 2 (beyond-Markov)
Only if SURVIVES on C1:
- **(C2):** K3 CMI - K2 CMI > 0.1 bits AND bootstrap 95% CI lower > 0.0.
- **(C4):** |K2(N=50000) - K2(N=5000)| ≤ 0.3 bits for the best alpha.

## 7. Deviations from Parent

1. **Alpha sweep:** Parent tested only alpha=1.0; this experiment tests alpha=0, 0.01, 0.1, 0.5, 1.0.
2. **Focus on null centering:** Parent measured null_mean only for alpha=1.0; this experiment measures null_mean for each alpha to determine C1-C3 tradeoff.
3. **MLE (alpha=0) inclusion:** Parent recomputed MLE as audit; this experiment measures it as primary.
4. **Phase 2 gating:** Phase 2 (beyond-Markov K3-K2) is conditional on any alpha passing C1+C3, same as parent.

## 8. Inherited Evidence (from parent handoff)

### Established
- Null centering (C1) robust across all estimator families on stochastic 12-state SPA at N=5000 with within-session shuffle.
- sklearn.feature_selection.mutual_info_classif with discrete_features=True is k-invariant on purely discrete data.
- Plug-in KL with alpha=1.0 Laplace smoothing has bias exceeding true signal.
- True I(Y;A|Z) on stochastic 12-state SPA is 1.52 bits.
- KSG CMI k=5 replication exactly matches parent.
- Audit MLE recomputation on same N=5000 records: alpha=0 K3=1.377, alpha=0.1 K3=0.743, alpha=0.01 K3=1.274 — all exceed 0.5 threshold.

### Rejected
- Hypothesis that KSG CMI k=5 insensitivity is due to insufficient neighborhood resolution: FALSIFIED for sklearn discrete_features=True.
- Hypothesis that plug-in KL with alpha=1.0 Laplace smoothing detects the 1.52-bit CMI signal: FALSIFIED.
- Hypothesis that CMI estimation is fundamentally impossible on discrete 12-state SPAs: NOT SUPPORTED by this evidence.

### Unknown
- Whether plug-in KL with alpha=0.1 or alpha=0.01 achieves |shuffled-action null_mean| < 0.1 bits at N=5000 on stochastic SPA.
- Whether bias-corrected MLE (alpha=0, no smoothing) maintains acceptable false positive rate on sparse strata.
- Whether sklearn mutual_info_classif with discrete_features=False makes k effective on this discrete dataset.
- Whether alternative MI estimators detect the 1.52-bit signal while preserving null centering.
- Whether per-(state,action) PMI signal can serve as an alternative detection paradigm for beyond-Markov dynamics.
- Generalization beyond 12-state discrete hash SPA to production Web transitions.

### Do Not Assume
- The frozen FALSIFIED-IN-SETTING verdict closes the C-WEB-DYNAMICS claim or the Physics lane. It closes only the plug-in KL alpha=1.0 and sklearn discrete KSG k=10 pathways on this specific SPA class.
- CMI estimation is fundamentally impossible on discrete SPAs. The audit demonstrates MLE alpha=0 recovers K3=1.377 bits on the same data.
- The 1.52-bit true CMI is undetectable in principle.
- KSG CMI family is universally k-invariant. The invariance is specific to sklearn.feature_selection.mutual_info_classif with discrete_features=True.
- Alpha=1.0 is the only valid Laplace smoothing choice.
- Production Web transitions generalize from this synthetic 12-state SPA.
- The within-session shuffle correction changes C1 pass/fail.

## 9. Validity Threats

1. **Sparse strata:** With 841 K3 strata at N=5000 (avg 1.5 records per (z,a) cell), MLE may have high variance.
2. **Numerical issues:** MLE (alpha=0) may produce log(0) for empty cells; need careful handling.
3. **Null centering degradation:** Reduced smoothing may increase null variance, potentially exceeding 0.1 threshold.
4. **Bootstrap CI degeneracy:** With sparse strata, bootstrap CI may be degenerate at ceiling or floor.
5. **Generalization:** Results are specific to 12-state discrete hash SPA with stochastic mixing 0.5.

## 10. Expected Outcomes

### Positive Outcome
If alpha=0.1 achieves both C1 (|null_mean| < 0.1) and C3 (K3 ≥ 0.5, p ≤ 0.001):
- CMI pathway unblocked; beyond-Markov K3-K2 testing can proceed.
- Plug-in KL with alpha=0.1 becomes preferred estimator for discrete Web state spaces.

### Negative Outcome
If null centering degrades monotonically with alpha (e.g., alpha=0 null_mean ≥ 0.1 while K3 ≥ 0.5):
- Sensitivity-false-positive tradeoff characterized.
- Physics lane must pivot to alternative detection paradigms or production Web data.

### Null Outcome
If all alphas fail C1 or C3:
- Confirms parent FALSIFIED-IN-SETTING is not alpha-specific.
- CMI pathway on discrete 12-state SPA exhausted.

## 11. Consequences

### Positive
- Unblocks beyond-Markov testing.
- Validates plug-in KL with reduced smoothing as preferred tool.
- Opens path to production SPA testing.

### Negative
- Requires pivot to alternative detection paradigms.
- May indicate fundamental limitation of discrete CMI estimation on sparse data.
- Production Web data with continuous state representations becomes necessary.
