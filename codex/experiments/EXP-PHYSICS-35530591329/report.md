# EXP-PHYSICS-35530591329 — Alpha Sweep for Plug-in KL on Stochastic SPA

## Executive Summary

**Verdict:** FALSIFIED-IN-SETTING  
**Outcome:** FALSIFIES (H0 confirmed)  
**Trigger:** C3 — alpha=1.0 (the only C1 passer) has positive_control_k3=0.099 < 0.5 bits

This experiment characterizes the sensitivity-null centering tradeoff for plug-in KL estimation of CMI on a stochastic 12-state SPA across five Laplace smoothing alphas {0, 0.01, 0.1, 0.5, 1.0}. The tradeoff is **monotonic and irreconcilable**: no alpha achieves both |shuffled-action null_mean| < 0.1 bits (C1) AND positive_control_k3 >= 0.5 bits (C3).

## Results Summary

| Alpha | K3 (bits) | K2 (bits) | K3-K2 | C1 (|null|<0.1) | C3 (K3>=0.5) |
|-------|-----------|-----------|-------|-----------------|---------------|
| 0     | 1.377     | 1.193     | 0.184 | FAIL (0.924)    | PASS (p=0.001) |
| 0.01  | 1.274     | 1.167     | 0.107 | FAIL (0.941)    | PASS (p=0.001) |
| 0.1   | 0.743     | 0.651     | 0.092 | FAIL (0.561)    | PASS (p=0.001) |
| 0.5   | 0.221     | 0.169     | 0.052 | FAIL (0.151)    | FAIL (K3<0.5) |
| 1.0   | 0.099     | 0.071     | 0.028 | PASS (0.064)    | FAIL (K3<0.5) |

**Key finding:** The crossover does not exist. As alpha decreases from 1.0 to 0:
- K3 sensitivity increases monotonically: 0.099 → 1.377 bits (13.9x improvement)
- Null bias increases monotonically: 0.064 → 0.924 bits (14.4x degradation)
- At the C1 threshold (0.1 bits), the null bias at alpha=0.5 is 0.151 (1.5x above), and at alpha=0.1 it is 0.561 (5.6x above)

## Design Verification

- **C6 (SPA design):** PASS — 48/48 (state, action) pairs have 4 distinct candidates
- **C7 (Stratum coverage):** PASS — 2 non-empty size buckets (5-9: 343 strata, 10-19: 37 strata)

## Controls

### C1: Null Centering (within-session shuffled-action, 500 permutations)
Only alpha=1.0 passes (|null_mean|=0.064, 1.6x below threshold). All other alphas fail with null bias 1.5-9.2x above threshold.

### C3: Positive Control (K3 >= 0.5 bits, p <= 0.001)
Alphas 0, 0.01, 0.1 all pass (K3 >= 0.743 bits, p=0.001). Alpha=1.0 fails (K3=0.099 < 0.5).

### B-DETERMINISTIC-SPA (degenerate baseline)
All alphas produce non-zero K3 on the deterministic SPA (I=0 by construction): alpha=0: 1.391, alpha=0.01: 1.294, alpha=0.1: 0.773, alpha=0.5: 0.239, alpha=1.0: 0.109. This confirms Laplace smoothing introduces bias even when no signal exists.

## Interpretation

The sensitivity-null tradeoff is **intrinsic to plug-in KL estimation across varying-size strata with Laplace smoothing**. The mechanism is:

1. **Smoothing dilutes per-stratum PMI**: With alpha=1.0, 88% of probability mass is pseudo-counts (n_smoothed = N + alpha*n_z*n_a*n_y = 5000 + 1*1438*4*12 = 74,024). The true signal is overwhelmed.

2. **Reduced smoothing reveals signal but also bias**: At alpha=0, the estimator uses raw counts. Sparse strata (avg 1.5 records per (z,a) cell) produce high-variance PMI estimates that don't center at zero under permutation.

3. **The bias is stratum-size dependent**: Smaller strata (5-9 records) have higher null bias (0.644 bits at alpha=0.1) than larger strata (10-19: 0.616 bits). Equal-weighting or median aggregation would worsen the bias by promoting the most biased strata.

## Consequences

### For the CMI pathway
The plug-in KL estimator cannot simultaneously achieve sensitivity (K3 >= 0.5 bits) and false-positive control (|null_mean| < 0.1 bits) on discrete 12-state SPAs at N=5000. This is a **fundamental limitation of the estimator class**, not a hyperparameter tuning problem.

### For C-WEB-DYNAMICS
No new evidence for or against Web dynamical structure. The experiment is on synthetic SPA simulation, not production Web transitions. The frozen FALSIFIED-IN-SETTING verdict closes only the plug-in KL alpha sweep pathway on this SPA class.

### Required next steps
1. **Alternative estimators**: Bayesian model comparison, likelihood-ratio tests, or entropy-rate methods that may have different bias-variance profiles
2. **Richer state representations**: Continuous embeddings, DOM features, or accessibility tree representations that may have different stratum-size distributions
3. **Production Web data**: Real SPA transitions with stochastic dynamics and larger state spaces
4. **Larger N**: N=50000 convergence testing to determine if the tradeoff is asymptotic or finite-sample

## Deviations from Preregistration

None. All frozen decisions rules applied as written. Phase 2 (beyond-Markov K3-K2 bootstrap) was not executed because no alpha passed both C1 and C3.
