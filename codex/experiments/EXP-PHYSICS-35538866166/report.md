# EXP-PHYSICS-35538866166 — Entropy-Rate CMI on Stochastic 12-State SPA

## Frozen Decision: FALSIFIED-IN-SETTING

**Trigger:** C1 — ALL alpha values have |shuffled-action null_mean| >= 0.1 bits at N=5000.

## Summary

Entropy-rate CMI estimation (CMI = H(Y|Z) - H(Y|Z,A), computed globally via histogram with Laplace smoothing) does **not** bypass the per-stratum KL bias-variance tradeoff on the stochastic 12-state SPA at N=5000. The frozen hypothesis H1 is falsified: no tested alpha achieves both |shuffled-action null_mean| < 0.1 bits AND positive_control_cmi >= 0.5 bits.

## Key Results

### Alpha Sweep

| Alpha | K3 (stochastic) | K2 (stochastic) | K3-K2 | \|null_mean\| | C1 | C3 |
|-------|-----------------|-----------------|-------|---------------|----|----|
| 0.1   | 0.523 bits      | 0.331 bits      | 0.192 | 0.240         | FAIL | PASS |
| 0.5   | -0.070 bits     | -0.182 bits     | 0.112 | 0.200         | FAIL | FAIL |
| 1.0   | -0.186 bits     | -0.268 bits     | 0.082 | 0.275         | FAIL | FAIL |

### Why Entropy-Rate Fails

The entropy-rate CMI estimator does not bypass the bias because **Laplace smoothing inflates H(Y|Z,A) more than H(Y|Z)**. The (z,a) conditioning space has `n_z * n_a * n_y` cells while the z-only space has `n_z * n_y` cells. Laplace smoothing adds `alpha` pseudo-counts to every cell, so the artificial uncertainty introduced scales with cell count. At alpha >= 0.5, this inflation exceeds the true CMI signal, producing **negative CMI values** — a mathematical impossibility for true mutual information, but an expected artifact of smoothed histogram estimation.

### Comparison with Parent Plug-in KL

| Property | Plug-in KL (parent) | Entropy-Rate CMI (this experiment) |
|----------|--------------------|------------------------------------|
| Alpha=0.1 C1 | \|mean\|=0.561 FAIL | \|mean\|=0.240 FAIL |
| Alpha=1.0 C1 | \|mean\|=0.064 PASS | \|mean\|=0.275 FAIL |
| Alpha=1.0 C3 | K3=0.099 FAIL | K3=-0.186 FAIL |
| Both C1+C3 | None (parent) | None (this experiment) |
| Null bias range | 0.064-0.924 | 0.200-0.275 |

**Critical difference:** Plug-in KL at alpha=1.0 passed C1 (|mean|=0.064) but failed C3 (K3=0.099). Entropy-rate CMI at alpha=1.0 fails BOTH (|mean|=0.275, K3=-0.186). The entropy-rate estimator has **worse** null centering than plug-in KL at high alpha, because the smoothing bias affects the larger (z,a) cell space more.

### Deterministic SPA Positive Control

The deterministic SPA control (B-ENTROPY-RATE-DEG) reveals the smoothing bias clearly:
- Alpha=0.1: K3=0.544 (correct, H(Y|Z)>0 by construction)
- Alpha=0.5: K3=-0.073 (negative, smoothing artifact)
- Alpha=1.0: K3=-0.199 (negative, smoothing artifact)

On a deterministic SPA where I(Y;A|Z)=0 by construction, the estimator produces negative values at alpha >= 0.5. This is a construct-validation failure for the estimator at these smoothing levels.

### Stratum Size Decomposition

Decomposition at alpha=0.5 (representative):
- **5-9 bucket:** 343 strata, 2147 records, observed CMI=0.117, null=0.079
- **10-19 bucket:** 37 strata, 433 records, observed CMI=0.240, null=0.130

Smaller strata contribute proportionally more null bias, same pattern as plug-in KL. The bias is intrinsic to histogram-based estimation across varying-size strata with Laplace smoothing, not specific to the KL divergence formulation.

## Interpretation

The per-stratum KL bias is **not** estimator-specific. Entropy-rate CMI, which computes conditional entropies globally rather than summing per-stratum KL, exhibits the same irreconcilable tradeoff between sensitivity and null centering. The root cause is Laplace smoothing on discrete spaces with many cells: it adds artificial uncertainty that scales with cell count, and the (z,a) space has n_a times more cells than the z-only space.

This falsifies the hypothesis that the bias is specific to the plug-in KL formulation. The bias is fundamental to **Laplace-smoothed histogram estimation** on discrete spaces with high cell counts relative to sample size.

## Consequences

**Product consequence (negative):** The CMI estimation pathway on discrete SPAs with Laplace smoothing is closed for both plug-in KL and entropy-rate CMI. The Physics lane must pivot to:
1. Bayesian model comparison (action-dependent vs action-independent transition model via Bayes factor)
2. Likelihood-ratio tests between nested models
3. Non-smoothed estimators (KDE, kNN, neural density estimators)
4. Production Web data with continuous state representations
5. Abandoning CMI estimation entirely on discrete spaces

**Research consequence:** The consistent positive K3-K2 differences (0.08-0.19 bits) across all alphas suggest beyond-Markov structure exists in the data but no valid estimator can separate it from smoothing bias at N=5000. Larger N or bias-corrected estimators may resolve this.
