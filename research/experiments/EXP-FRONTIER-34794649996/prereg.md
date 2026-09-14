# EXP-FRONTIER-34794649996 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34794649996
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-14
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does per-page-type binned TV estimation with per-type bias correction recover absolute signal strength lost to pooled heterogeneous averaging, or is the 94.6% attenuation a fundamental property of action-dependent structure in non-stationary DGPs?

## 3. Motivation

The parent experiment (EXP-FRONTIER-34773875458) established that pooled binned TV detection survives non-stationarity (Spearman rho=0.929), but with severe absolute attenuation: pooled BC TV at lambda=1 drops from 0.952 (stationary) to 0.051 (non-stationary) — a 94.6% loss. The frequency baseline (0.335) is 6x larger than the non-stationary signal.

The auditor flagged a critical methodological issue: the per-type bias floor was contaminated. The pooled permutation null (N=2000) was used for per-type BC TV estimates where true bias floors vary by noise level (0.10-0.15 low-noise vs 0.35-0.38 high-noise). This contamination could explain the attenuation.

**Key question:** Is the 94.6% attenuation:
- **Estimator-dependent** (addressable): pooled bias correction contaminates per-type estimates; per-type bias correction recovers signal strength
- **Fundamental** (closing density-divergence): heterogeneous page types irrecoverably destroy pooled signal regardless of estimator

This is the minimum step to determine whether the absolute magnitude gap is fixable before any real-data investment. The auditor explicitly warns: "Do not promote to product or to real-data collection solely on rho."

## 4. Hypotheses

### H1: Per-Type Recovery
Mean per-type BC TV at lambda=1 > 0.2 across 8 page types (vs pooled BC TV 0.051).

### H2: Significant Improvement
Per-type BC TV significantly higher than pooled BC TV (paired t-test p<0.05 across 8 page types).

### H3: Positive Control
At lambda=1, per-type BC TV >=0.001 across all 8 page types.

### H4: Null Control
At lambda=0, per-type BC TV <=0.01 across all 8 page types.

## 5. Data Generation

### 5.1 Reuse Parent DGP

Identical to EXP-FRONTIER-34773875458 non-stationary condition:
- 8 page types with different dynamics (rotation/scaling/translation, low/high noise, shifted centers)
- Same function parameters (THETA, OFFSET_A, SCALE, OFFSET_B, T_C, ALPHA_C)
- Same noise model (heteroscedastic Gaussian with state-dependent variance)
- Page type assignment: `type = (transition_index // 250) mod 8`

### 5.2 Lambda Levels

8 lambda levels: 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0

### 5.3 Sample Size

- 2000 transitions per lambda level (250 per page type × 8 types)
- 5 replications per lambda level
- Total: 80,000 non-stationary transitions (same as parent)

### 5.4 Seed Independence

Same seed formula as parent: `cell_seed = func_seed * 100000 + lambda_idx * 1000 + rep_idx * 10 + BASE_SEED`

## 6. Measures

### 6.1 Per-Page-Type TV (Primary)

For each page type separately:
- Compute empirical P(S_{t+1} | A=a) using 20×20 grid binning (400 bins)
- TV_max = max_{a,a'} (1/2) sum |P(S|a) - P(S,a')| over all action pairs
- Computed on transitions within each page type only (within-type stationary analysis)

### 6.2 Per-Type Bias-Corrected TV (Primary Metric)

For each page type:
- Compute per-type permutation null: shuffle action labels within that page type
- N_perm = 200 permutations per page type per lambda level
- Per-type perm_mean_TV = mean TV across permutations
- Per-type BC TV = max(0, observed_TV - per-type perm_mean_TV)

**Critical difference from parent:** Per-type bias floor uses N=200 permutations within each page type, not pooled N=2000 across all types.

### 6.3 Pooled BC TV (Comparison)

Recompute pooled BC TV using parent methodology for direct comparison:
- Pooled perm_mean_TV at lambda=0 across all page types (N=2000 permutations)
- Pooled BC TV = observed_TV - pooled perm_mean_TV

### 6.4 Frequency Baseline

Marginal P(S_{t+1}) pooled across all actions and page types.

## 7. Statistical Tests

### 7.1 Primary: Paired Comparison

- Paired t-test: per-type BC TV vs pooled BC TV at lambda=1 across 8 page types
- One-sided: per-type > pooled
- Threshold: p < 0.05

### 7.2 Effect Size

- Cohen's d for per-type BC TV vs pooled BC TV at lambda=1
- Threshold: d > 1.0 (large effect)

### 7.3 Per-Type Scaling

- Spearman rho(per-type BC TV, lambda) for each page type
- Threshold: rho >= 0.5 per type

### 7.4 Aggregated Scaling

- Mean per-type BC TV across all 8 page types at each lambda level
- Spearman rho(mean per-type BC TV, lambda)
- Threshold: rho >= 0.5

## 8. Controls

### 8.1 Positive Control (lambda=1)
- Per-type BC TV >=0.001 across all 8 page types
- Verifies: per-type bias correction does not destroy detection

### 8.2 Null Control (lambda=0)
- Per-type BC TV <=0.01 across all 8 page types
- Verifies: per-type bias correction does not create false positives

### 8.3 Parent Replication Control
- Pooled BC TV at lambda=1 replicates parent finding (~0.051)
- Verifies: measurement pipeline is consistent with parent experiment

### 8.4 Bias Floor Verification
- Per-type perm_mean_TV at lambda=0 should vary by noise level:
  - Low-noise types: ~0.10-0.15
  - High-noise types: ~0.35-0.38
- If all per-type perm_mean_TV are identical, bias correction is not truly per-type

## 9. Validity Threats

### 9.1 Sample Size per Type
With 250 transitions per page type per lambda level on 400 bins, expected counts per bin per type = 0.625. This is sparse. Per-type TV estimates may be noisy. Mitigation: report confidence intervals; focus on lambda=1 where signal is strongest.

### 9.2 Permutation Null Adequacy
N=200 permutations per page type may yield noisy perm_mean_TV estimates. Monte Carlo SE ~ sqrt(1/200) ~ 0.07. Mitigation: this is sufficient to detect large differences (0.051 vs >0.2).

### 9.3 Multiple Comparisons
8 page types × 8 lambda levels = 64 cells. Primary comparison is paired t-test across 8 types at lambda=1 (single test). Per-type scaling tests are exploratory.

### 9.4 Synthetic-to-Real Gap
This experiment uses the same synthetic DGP as parent. Findings validate per-type bias correction methodology but do not directly demonstrate recovery on real Web data.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Mean per-type BC TV at lambda=1 > 0.2 across 8 page types
2. Per-type BC TV > pooled BC TV (paired t-test p < 0.05)
3. Positive control passes (per-type BC TV >=0.001 at lambda=1 in all types)
4. Null control passes (per-type BC TV <=0.01 at lambda=0 in all types)
5. No pipeline errors

### 10.2 FALSIFIED-IN-SETTING
If ANY of:
1. Mean per-type BC TV <=0.1 at lambda=1
2. Paired t-test p > 0.05 (no significant improvement)
3. Positive control fails
4. Null control fails

### 10.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent per-type TV computation
2. Per-type permutation null computation fails
3. Fewer than 250 transitions per page type per lambda level

## 11. Expected Outcomes

### 11.1 Positive Result (SURVIVES_CURRENT_TEST)
- Attenuation is estimator-dependent, not fundamental
- Per-type bias correction recovers absolute signal strength
- SPIDER should use per-type estimation for real Web data
- Density-divergence approach remains viable for heterogeneous data
- Justifies further investment in real-data collection

### 11.2 Negative Result (FALSIFIED-IN-SETTING)
- Attenuation is fundamental to heterogeneous DGP pools
- Per-type estimation does not recover absolute strength
- Density-divergence approach unsuitable for real Web data
- Frontier should pivot to orthogonal mechanisms
- C-WEB-DYNAMICS claim ceiling narrowed to stationary DGPs only

### 11.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging
- Not scientific evidence for or against
- Re-run with corrected infrastructure

## 12. Analysis Plan

1. **Data Generation**: Generate non-stationary transitions using parent DGP parameters
2. **Per-Type TV**: Compute TV for each page type separately at each lambda level
3. **Per-Type Bias Correction**: Compute per-type permutation nulls (N=200) and subtract
4. **Pooled BC TV**: Recompute pooled BC TV for direct comparison
5. **Statistical Tests**: Paired t-test, effect size, per-type scaling
6. **Controls**: Verify positive, null, replication, and bias floor controls
7. **Exploratory**: Per-type scaling analysis
8. **Reporting**: Report all outcomes with equal prominence

## 13. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for paired t-test and Spearman correlation
- Standard library only (no custom estimators)

Code will be committed to `research/experiments/EXP-FRONTIER-34794649996/` before execution.

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.