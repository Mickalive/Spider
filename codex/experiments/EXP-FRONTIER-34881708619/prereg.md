# EXP-FRONTIER-34881708619 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34881708619
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-14
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does pooled binned TV estimation maintain a fundamental advantage over per-type estimation when both use equal sample size (250 transitions per type), or does the 67% per-type/pooled ratio from the parent experiment reflect a sample-size confound rather than an estimator difference?

## 3. Motivation

The density-divergence line of C-WEB-DYNAMICS experiments has established:

- **EXP-FRONTIER-34773875458**: Pooled binned TV (20×20 grid) detects action-conditional structure under non-stationarity (Spearman rho=0.929), but with severe absolute attenuation: pooled BC TV at lambda=1 drops from 0.952 (stationary) to 0.051 (non-stationary) — a 94.6% loss.

- **EXP-FRONTIER-34794649996**: Per-type bias correction with N=200 permutations per type does NOT recover signal: mean per-type BC TV at lambda=1 = 0.034, which is 0.67× pooled BC TV 0.051 and far below the >0.2 threshold. Null control fails (4/8 types >0.01 at lambda=0). Per-type instrument is noise-dominated at n=250/type (0.625 expected counts/bin on 400-bin grid).

The auditor identified a critical confound (audit.json required_fixes[3]): the per-type vs pooled comparison confounds estimator type with sample size. Per-type uses N=250 transitions per type while pooled uses N=2000 pooled transitions (250 per type × 8 types). The 67% ratio may reflect:
- **Estimator difference**: pooled estimation is fundamentally better at heterogeneous data because it borrows strength across types
- **Sample size bias**: per-type at 250/type is too sparse for stable estimation; with 2000/type per-type would match or exceed pooled

This is the minimum disambiguating step. The handoff recommends: "Design a Frontier experiment testing per-type vs pooled binned TV with EQUAL sample size to disentangle estimator contamination from sparsity bias."

## 4. Hypotheses

### H1: Pooled Advantage at Equal n
Pooled BC TV computed on subsampled data (250 per type) at lambda=1 is significantly higher than per-type BC TV at lambda=1 across 8 page types (one-sided paired t-test p<0.05, Cohen's d>0.5).

### H2: Positive Control
Pooled BC TV on FULL data (2000 transitions) at lambda=1 replicates parent finding (~0.051 within 0.01).

### H3: Null Control
Per-type BC TV at lambda=0 is ≤0.01 across all 8 page types (same threshold as parent per-type null control, EXP-FRONTIER-34794649996). Additionally, pooled subsampled BC TV at lambda=0 is ≤0.01 (verifies subsampling does not introduce false positives).

### H4: Subsampling Validity
Pooled subsampled BC TV at lambda=1 is ≤ pooled full BC TV at lambda=1 (subsampling cannot increase signal).

## 5. Data Generation

### 5.1 Reuse Parent DGP

Identical to EXP-FRONTIER-34794649996 non-stationary condition:
- 8 page types with different dynamics (rotation/scaling/translation, low/high noise, shifted centers)
- Same function parameters (THETA, OFFSET_A, SCALE, OFFSET_B, T_C, ALPHA_C)
- Same noise model (heteroscedastic Gaussian with state-dependent variance)
- Page type assignment: `type = (transition_index // 250) mod 8`

### 5.2 Lambda Levels

8 lambda levels: 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0

### 5.3 Sample Size

- 2000 transitions per lambda level (250 per page type × 8 types)
- 5 replications per lambda level
- Total: 80,000 non-stationary transitions (identical to parent)

### 5.4 Seed Independence

Same formula as parent: `cell_seed = BASE_SEED * 100000 + lambda_idx * 1000 + rep_idx * 10 + 999`

This ensures exact data replication with parent for validation.

## 6. Measures

### 6.1 Per-Type BC TV (Recomputed from Parent Data)

For each page type separately on the full 250 transitions per type:
- Compute empirical P(S_{t+1} | A=a) using 20×20 grid binning
- TV_max over action pairs
- Per-type permutation null: N=200 permutations shuffling action labels within type
- Per-type BC TV = max(0, observed_TV - per-type perm_mean_TV)

This recomputes the parent's per-type estimate on the SAME data used for pooled subsampled estimation, ensuring data-level fairness.

### 6.2 Pooled Full BC TV (Baseline Comparison)

For all 2000 transitions pooled across types:
- Compute empirical P(S_{t+1} | A=a) using 20×20 grid binning
- TV_max over action pairs
- Pooled permutation null: N=200 permutations shuffling action labels across all types
- Pooled full BC TV = max(0, observed_TV - perm_mean_TV)

This replicates the parent's pooled estimate for validation.

### 6.3 Pooled Subsampled BC TV (Primary Comparison)

For the SAME 2000 transitions, but subsampled to 250 per type:
- Randomly select 250 transitions per page type (using deterministic seed)
- Pool all 2000 selected transitions (8 types × 250)
- Compute empirical P(S_{t+1} | A=a) using 20×20 grid binning
- TV_max over action pairs
- Pooled subsampled permutation null: N=200 permutations on the subsampled data
- Pooled subsampled BC TV = max(0, observed_TV - perm_mean_TV)

**Key**: This uses the same 250 transitions per type as per-type estimation, but analyzes them as pooled. Any advantage over per-type reflects the pooling mechanism, not more data.

### 6.4 Frequency Baseline

Marginal P(S_{t+1}) pooled across all actions and page types on full 2000 transitions.

## 7. Statistical Tests

### 7.1 Primary: Paired Comparison at Equal n

- Paired t-test: pooled subsampled BC TV vs per-type BC TV at lambda=1 across 8 page types
- One-sided: pooled subsampled > per-type
- Threshold: p < 0.05
- Effect size: Cohen's d > 0.5

### 7.2 Secondary: Full-vs-Subsampled Pooled

- Paired t-test: pooled full BC TV vs pooled subsampled BC TV at lambda=1 across 5 replications
- Two-sided: quantify subsampling loss
- This tests H4 (subsampling validity)

### 7.3 Spearman Scaling

- Spearman rho(pooled subsampled BC TV, lambda) across 8 lambda levels
- Compare with parent pooled rho=0.929 and per-type aggregate rho=0.76
- Tests whether subsampling degrades rank detection

### 7.4 Per-Type Scaling Recovery

- Spearman rho(per-type BC TV, lambda) recomputed on same data
- Compare with parent per-type aggregate rho=0.76
- Tests replication of parent per-type finding

## 8. Controls

### 8.1 Positive Control (Pooled Full Replication)

Pooled full BC TV at lambda=1 must be within 0.01 of parent value (~0.051).
- Verifies: data generation pipeline matches parent
- Verifies: pooled estimation pipeline is correct
- Threshold: |pooled_full_bc - 0.051| < 0.01

### 8.2 Null Control (Subsampled Null)

Pooled subsampled BC TV at lambda=0 must be ≤0.01 across all 8 page types.
- Verifies: subsampling does not introduce false positives
- Threshold: per-type BC TV ≤0.01 at lambda=0 (same as parent per-type null control)
- Note: this is a stricter threshold than the parent pooled null (which had 2000 transitions); subsampled pooled at 250/type may be noisier

### 8.3 Subsampling Consistency Control

Pooled subsampled BC TV at lambda=1 ≤ pooled full BC TV at lambda=1 across all 5 replications.
- Verifies: subsampling cannot increase signal (monotonicity)
- If violated, subsampling introduces artifact

### 8.4 Per-Type Replication Control

Recomputed per-type aggregate BC TV at lambda=1 must be within 0.01 of parent value (0.034).
- Verifies: per-type pipeline on same data produces same result
- Threshold: |recomputed_per_type_bc - 0.034| < 0.01

## 9. Validity Threats

### 9.1 Subsampling Variance

With 5 replications and 250 per type, the subsampled pooled estimate has higher variance than full pooled. The paired t-test across 8 types (not 5 reps) partially addresses this by using types as the pairing unit. Report confidence intervals.

### 9.2 Sparse Binning at Equal n

Both estimators operate at 0.625 expected counts/bin (250 transitions, 400 bins). The sparse regime inflates both raw TV and perm means. Bias correction via permutation subtraction addresses this, but the absolute magnitude may remain small for both.

### 9.3 Permutation Null Consistency

The per-type perm null shuffles within type (N=200); the pooled subsampled perm null shuffles across all types in the subsample (N=200). These are different null models: per-type null assumes exchangeability within type; pooled null assumes exchangeability across types. This is intentional — it tests whether the pooled null (which is what practitioners would use) gives different BC TV than the per-type null.

### 9.4 Synthetic-to-Real Gap

All evidence remains synthetic 2D [0,1]^2. No inference to real Web DOM transitions is justified. This experiment tests estimator methodology, not Web dynamics directly.

### 9.5 Decision Rule Sensitivity

The primary test uses paired t-test across 8 types at one lambda level (lambda=1). With n=8, power is limited for small effects. The Cohen's d>0.5 threshold ensures the effect, if detected, is practically meaningful. Report both p-value and effect size.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST

If ALL of:
1. Pooled subsampled BC TV > per-type BC TV at lambda=1 (one-sided paired t-test p<0.05 across 8 types)
2. Cohen's d > 0.5 for the difference
3. Positive control passes (|pooled_full_bc - 0.051| < 0.01)
4. Null control passes (per-type BC TV ≤0.01 at lambda=0 across all 8 types AND pooled subsampled BC TV ≤0.01 at lambda=0)
5. No pipeline errors

### 10.2 FALSIFIED-IN-SETTING

If ANY of:
1. Pooled subsampled BC TV ≤ per-type BC TV at lambda=1 (p>0.05 OR negative effect)
2. Cohen's d ≤ 0.5 (effect too small to be practically meaningful)

### 10.3 MEASUREMENT_INVALID

If:
1. Pipeline errors prevent computation
2. Sample size insufficient (<250 transitions per type)
3. Subsampling consistency control violated (subsampled > full)
4. Positive control fails (|pooled_full_bc - 0.051| ≥ 0.01)
5. Null control fails (per-type BC TV >0.01 at lambda=0 in any type OR pooled subsampled BC TV >0.01 at lambda=0)

## 11. Analysis Plan

1. **Data Generation**: Generate 80,000 non-stationary transitions using parent frozen seeds (same as EXP-FRONTIER-34794649996)
2. **Per-Type BC TV**: Recompute per-type BC TV on 250 transitions per type with N=200 per-type permutations
3. **Pooled Full BC TV**: Recompute pooled BC TV on all 2000 transitions with N=200 pooled permutations
4. **Subsampled Pooled BC TV**: For each rep, subsample 250 per type, pool, compute BC TV with N=200 pooled permutations on subsampled data
5. **Primary Comparison**: Paired t-test across 8 types at lambda=1 (pooled subsampled vs per-type)
6. **Secondary Comparisons**: Full vs subsampled pooled; Spearman scaling; per-type replication
7. **Controls**: Verify all four control conditions
8. **Reporting**: Report all outcomes with equal prominence, confidence intervals, and effect sizes

## 12. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations, random generation, and subsampling
- `scipy.stats` for paired t-tests and Spearman correlation
- `collections.Counter` for binning
- Standard library only

Code will be committed to `research/experiments/EXP-FRONTIER-34881708619/` before execution.

## 13. Pre-registered Expectations

From the parent audit (required_fixes[3]):
- The audit identifies the 67% ratio as potentially confounded by sample size
- If the ratio is estimator-driven, pooled subsampled > per-type at equal n (H1 supported)
- If the ratio is sample-size-driven, pooled subsampled ≈ per-type at equal n (H1 falsified)
- The audit recommends this as "the minimum disambiguating step before either closing the density-divergence approach or continuing with denser estimation"

From the chain of Frontier experiments:
- Pooled BC Spearman rho=0.929 is established and replicated
- Per-type BC at n=250/type is noise-dominated (null 4/8 >0.01, CV up to 1.59)
- Frequency baseline (0.335) is 6.5× pooled BC, indicating absolute signal remains far below marginal structure

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
