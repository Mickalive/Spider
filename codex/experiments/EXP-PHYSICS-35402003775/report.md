# EXP-PHYSICS-35402003775 — Three Materially Orthogonal Null Frameworks

## Summary

This experiment tests three materially orthogonal null frameworks to determine whether any can center the null at zero for hash-routed SPAs, resolving the inherited ~0.41-bit PMI estimator bias floor that within-stratum permutation cannot eliminate.

**Result: FALSIFIED-IN-SETTING.** All three frameworks fail to center null at zero:
- Parametric bootstrap: null mean = 0.357 bits (3.57x above 0.1 threshold)
- Miller-Madow: null mean = 0.407 bits (4.07x above 0.1 threshold)  
- Conditional entropy: null mean = -0.814 bits (degenerate)

**Outcome: FALSIFIES.** The null control problem is intrinsic to hash-routed SPA design with deterministic/stochastic mixing at N=5000. The Physics lane should pivot to the orthogonal high-upside question of signal decomposition (Markov vs beyond-Markov).

## Background

The parent experiment (EXP-PHYSICS-35389142077) achieved state-history K=2 conditional PMI = 0.933 bits (p=0.001, d=79.7) on the 12-state hash-routed SPA simulation at N=5000, confirming the beyond-Markov signal is real and reproducible. However, within-stratum conditional permutation yielded null mean = 0.417 bits (4.17x above the 0.1 threshold), falsifying the null centering hypothesis.

The inherited bias floor (~0.41 bits) is intrinsic to PMI estimator weighting across deterministic/stochastic strata, not a permutation artifact. This experiment tests three materially orthogonal null frameworks that address the root cause (estimator bias) rather than the permutation scheme.

## Methods

### Testbed
- 12-state SPA simulation with hash-based routing (SHA256)
- 50 sessions x 100 steps = 5000 transitions, seed=42
- 4 action primitives: form_submit, button_click, js_navigate, menu_select

### Framework 1: Parametric Bootstrap Null
- Estimate P(url_after | url_before, history) from data via maximum likelihood with Laplace smoothing (alpha=1.0)
- For each of 1000 bootstrap samples, simulate null transitions from estimated distribution
- Compute PMI on each simulated dataset
- Expected null mean = 0 bits (analytic)

### Framework 2: Miller-Madow Corrected PMI
- Apply Miller-Madow bias correction to PMI estimator:
  PMI_MM = PMI + (V_x - 1)/(2*N_x*ln2) + (V_y - 1)/(2*N_y*ln2) - (V_xy - 1)/(2*N_xy*ln2)
- Compute within-stratum permutation null with corrected estimator
- Expected null mean = 0 bits

### Framework 3: Conditional Entropy Difference
- Compute DeltaH = H(url_after | action, url_before, history) - H(url_after | url_before, history)
- Under within-stratum permutation null, DeltaH should be 0
- Expected null mean = 0 bits

### Positive Controls
- 8-state synthetic deterministic SPA, K=3, N=5000: PMI >= 1.0 bits, p < 0.001
- Conditional entropy positive control: H(S_next|S,H_K=3) > H(S_next|S,H_K=2)

## Results

### Primary Measurements (K=2 on 12-state SPA)

| Framework | Observed PMI | Null Mean | |Null Mean| < 0.1 | Status |
|-----------|--------------|-----------|------------------|--------|
| Parametric Bootstrap | 0.933 bits | 0.357 bits | No (3.57x) | FAIL |
| Miller-Madow | 1.060 bits (MM) | 0.407 bits | No (4.07x) | FAIL |
| Conditional Entropy | -0.933 bits | -0.814 bits | No (8.14x) | FAIL |
| Within-Stratum (parent) | 0.933 bits | 0.417 bits | No (4.17x) | FAIL |

### Positive Controls
- PMI pipeline validated: 8-state SPA K3 PMI = 1.671 bits (state), 1.806 bits (action), p=0.001
- Conditional entropy positive control **FAILS**: H(S|S,H_K=3) = 0.0 on deterministic SPA (degenerate)

### Baseline Reproducibility
- State K2 PMI = 0.933 bits (matches parent exactly)
- Unconditional K0 = 1.419 bits, K1 = 1.531 bits, action K3 = 1.221 bits
- Determinism check: 885/1292 stochastic (68.5%), 407 deterministic (31.5%)

## Interpretation

### Why Parametric Bootstrap Fails
The parametric bootstrap estimates P(url_after|stratum) and simulates null samples from this estimated distribution. The null mean of 0.357 bits (14.5% improvement over within-stratum) indicates the estimated conditional distribution does not fully capture the action-PMI coupling. The bias is reduced but not eliminated, suggesting the bootstrap samples inherit the same weighted-average bias across deterministic/stochastic strata.

### Why Miller-Madow Fails
The Miller-Madow bias correction increases observed PMI from 0.933 to 1.060 bits (+13.6%) but does not reduce the null bias (0.407 vs 0.417). This indicates the bias is not primarily due to finite-sample correction in the PMI estimator, but rather to the weighted averaging across deterministic/stochastic strata. The correction helps the signal but not the null.

### Why Conditional Entropy Fails
The conditional entropy framework yields a degenerate result: observed DeltaH is negative (-0.933 bits), meaning H(S|A,S,H) < H(S|S,H). This occurs because:
1. The conditional entropy estimator is biased downward when action determines next state (deterministic SPAs)
2. The conditional entropy positive control fails: H(S|S,H_K=3) = 0.0 on the 8-state deterministic SPA (all K=3 strata are single-valued)
3. The conditional entropy framework is not suitable for deterministic transition systems

### Convergence Across Frameworks
The null means converge: parametric bootstrap (0.357), Miller-Madow (0.407), within-stratum (0.417). This suggests the bias floor is intrinsic to the PMI estimator weighting across deterministic/stochastic strata, not the estimator choice or permutation scheme.

## Decision Rule Evaluation

**Per-framework evaluation:**
- Parametric bootstrap: FAIL (|null_mean| = 0.357 > 0.1)
- Miller-Madow: FAIL (|null_mean| = 0.407 > 0.1)
- Conditional entropy: FAIL (|null_mean| = 0.814 > 0.1 AND positive control fails)

**Overall verdict:**
- 0/3 frameworks pass all conditions
- FALSIFIED-IN-SETTING per frozen decision rule
- The null control problem is intrinsic to hash-routed SPA design with deterministic/stochastic mixing at N=5000

## Consequences

### For C-WEB-DYNAMICS
The claim remains HYPOTHESIS. The 0.933-bit K2 PMI signal is real and reproducible (p=0.001) but cannot support confirmatory beyond-Markov claim without valid null control. The FALSIFIED-IN-SETTING verdict is due to null control methodology limitation, not absence of signal.

### For the Physics Lane
The lane should pivot to the orthogonal high-upside question: whether the 0.933-bit K2 PMI signal is primarily Markov (action determines next state given current state) or beyond-Markov (history adds information beyond current state). This decomposition does not require null centering (it is a ratio/comparison, not an absolute test).

### For Production SPA Testing
Production testing remains untested. The validated PMI pipeline (0.933 bits, p=0.001) detects signal but without a valid null control, the p-value and significance claims cannot be confirmed. A different falsification framework is needed before production testing is meaningful.

## Validity Threats

1. **Parametric bootstrap model misspecification.** The estimated P_hat may not capture the true data-generating process. The model is deliberately simple (conditional frequency table with Laplace smoothing) to test whether even a basic DGP model outperforms permutation.

2. **Miller-Madow overcorrection.** The correction assumes multinomial sampling; the effective V may differ from observed unique counts. The correction is small (O(1/N)) and does not flip sign.

3. **Conditional entropy estimator bias.** Plug-in entropy estimators have known bias for small samples. The degenerate result (negative DeltaH) confirms the estimator is not suitable for deterministic transition systems.

4. **Deterministic strata dilution.** Same as parent: 31.5% deterministic strata contribute PMI=0 by construction. This dilutes but does not bias the null.

5. **Framework correlation.** The three frameworks are not fully independent — they all operate on the same dataset and share some estimator components. Bonferroni correction for 3 tests is conservative but appropriate.

## Raw Evidence

- Raw transitions: `research/experiments/EXP-PHYSICS-35402003775/raw_transitions.json` (SHA256: 170df6e34c78f64584f5332d61b9a705d87838b61e24eb04bdd4cc1b095c6ade)
- Analysis results: `research/experiments/EXP-PHYSICS-35402003775/analysis_results.json` (SHA256: 4704544873d799ce01a02b627a06877bd3399c010106a8e4cd32743eaef3708b)
- Code: `research/experiments/EXP-PHYSICS-35402003775/run_experiment.py` (SHA256: a170973a5002d39c7172657c27e6a6fa4e53d4811b5a1b99c2de9ee75846bb98)
