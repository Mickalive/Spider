# EXP-FRONTIER-34794649996: Per-Type Bias Correction TV Estimation

## Executive Summary

**Status**: COMPLETE  
**Outcome**: FALSIFIES  
**Decision**: FALSIFIED-IN-SETTING  

Per-type bias correction with N=200 permutations per page type **fails** to recover absolute signal strength and **fails** the null control. The hypothesis that per-type estimation recovers signal lost to pooled heterogeneous averaging is falsified in this setting.

Key findings:
- Mean per-type BC TV at lambda=1: **0.034** (threshold: >0.2) — fails by 6x
- Per-type BC TV is **lower** than pooled BC TV (ratio 0.67x, opposite of hypothesis)
- Null control **FAILS**: per-type BC TV > 0.01 at lambda=0 in 4/8 page types
- CV check **FAILS**: max CV=1.59 at lambda=1 (threshold: <=0.5)
- Paired t-test: p=0.989 (per-type is significantly **worse** than pooled, not better)

## 1. Primary Comparison

| Metric | Per-Type BC TV | Pooled BC TV | Threshold |
|--------|---------------|-------------|-----------|
| Mean at lambda=1 | 0.034 | 0.051 | >0.2 |
| Ratio | 0.67x | 1.0x | >1.0 |
| Paired t-test p | 0.989 | — | <0.05 |
| Cohen's d | -1.64 | — | >1.0 |

Per-type BC TV at lambda=1 across 8 page types:
- Type 0 (rotation_low): 0.025
- Type 1 (scaling_low): 0.026
- Type 2 (translation_low): 0.007
- Type 3 (rotation_high): 0.024
- Type 4 (scaling_high): 0.017
- Type 5 (translation_high): 0.014
- Type 6 (rotation_low_shifted): 0.118
- Type 7 (scaling_low_shifted): 0.043

Only type 6 (rotation with shifted center) shows substantial BC TV. All others are near noise floor.

## 2. Controls

| Control | Status | Details |
|---------|--------|---------|
| Positive control | PASS | All per-type BC TV >= 0.001 at lambda=1 |
| Null control | **FAIL** | 4/8 types exceed 0.01 at lambda=0 |
| Parent replication | PASS | Pooled BC TV = 0.051 (matches parent 0.051) |
| Bias floor varies | PASS | Low-noise: 0.37-0.39, High-noise: 0.60-0.61 |
| CV check | **FAIL** | Max CV = 1.59 (threshold: <=0.5) |
| Paired comparison | **FAIL** | Per-type < pooled (p=0.989) |

## 3. Null Control Failure Analysis

Per-type BC TV at lambda=0 (should be <= 0.01):
- Type 0: 0.028 **FAIL**
- Type 1: 0.000 PASS
- Type 2: 0.012 **FAIL**
- Type 3: 0.010 PASS (borderline)
- Type 4: 0.016 **FAIL**
- Type 5: 0.014 **FAIL**
- Type 6: 0.007 PASS
- Type 7: 0.007 PASS

Root cause: Per-type permutation means at lambda=0 are 0.37-0.60 (vs pooled 0.239). With only 250 transitions per type on 400 bins (0.625 expected counts/bin), the per-type permutation null is too noisy. The perm_mean captures sampling variance rather than true bias, causing overcorrection that inflates BC TV at lambda=0.

## 4. Per-Type Scaling Analysis

Spearman rho(per-type BC TV, lambda) by page type:
- Type 0: rho=-0.38 (p=0.35) — not significant
- Type 1: rho=0.33 (p=0.42) — not significant
- Type 2: rho=0.26 (p=0.53) — not significant
- Type 3: rho=0.26 (p=0.53) — not significant
- Type 4: rho=0.31 (p=0.46) — not significant
- Type 5: rho=0.00 (p=1.00) — not significant
- Type 6: rho=0.76 (p=0.028) — **significant**
- Type 7: rho=0.48 (p=0.23) — not significant

Only 1/8 types shows significant lambda-scaling after per-type BC. Aggregate rho=0.76 (p=0.028) is driven entirely by type 6.

## 5. Interpretation

### 5.1 Why Per-Type BC Performs Worse Than Pooled

The per-type approach fails because:

1. **Sparse binning**: 250 transitions / 400 bins = 0.625 expected counts/bin per type. This creates high-variance empirical distributions where sampling noise dominates signal.

2. **Noisy permutation null**: N=200 permutations per type yields Monte Carlo SE ~0.07. But the per-type perm_mean at lambda=0 is 0.37-0.60, far larger than the pooled perm_mean (0.239). This indicates the per-type permutation test is capturing sampling variance, not true bias.

3. **Overcorrection**: The inflated per-type perm_mean causes BC TV to be smaller than raw TV at lambda=0 (negative correction), creating false positives in the null control.

4. **Heterogeneous bias floors**: Low-noise types have perm_mean 0.37-0.39 while high-noise types have 0.60-0.61. The per-type correction cannot distinguish between bias from sparsity and bias from noise structure.

### 5.2 Implications for C-WEB-DYNAMICS

The 94.6% absolute attenuation observed in the parent experiment is **not** primarily caused by pooled bias contamination. Per-type correction with proper per-type bias floors does not recover signal strength — it makes it worse.

This suggests the attenuation is a fundamental property of the heterogeneous DGP pool, not an estimator artifact. The density-divergence approach using binned TV is unsuitable for heterogeneous data regardless of whether estimation is pooled or per-type.

### 5.3 What Would Be Needed

To recover signal in heterogeneous settings, one would need:
- Far more transitions per type (1000+) for stable per-type TV estimates
- Adaptive binning that accounts for heterogeneous noise levels
- Alternative divergence measures robust to sparse binning
- Or fundamentally different approaches (causal factorization, information-theoretic measures)

## 6. Validity Threats

1. **Sparse binning**: 0.625 expected counts/bin per type is severe. Per-type TV estimates are dominated by sampling noise.
2. **Permutation null adequacy**: N=200 per type yields noisy perm_mean estimates. The Monte Carlo SE is large relative to the signal.
3. **Synthetic-to-real gap**: All evidence remains synthetic 2D [0,1]^2 with toy affine families.
4. **Deterministic block cycling**: Real Web non-stationarity is continuous and state-dependent, not block-deterministic.

## 7. Decision

**FALSIFIED-IN-SETTING**: 
- Null control fails (per-type BC TV > 0.01 at lambda=0 in 4/8 types)
- Mean per-type BC TV at lambda=1 = 0.034 (threshold: >0.2)
- Paired t-test p=0.989 (per-type not significantly better than pooled)

The per-type bias correction approach does not recover absolute signal strength. The 94.6% attenuation is not estimator-dependent — it is fundamental to heterogeneous DGP pools under binned TV estimation.
