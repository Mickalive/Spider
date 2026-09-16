# EXP-FRONTIER-34913743596 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34913743596
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-15
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Do alternative divergence measures (KDE with cross-validated bandwidth, kNN mutual information) maintain per-type null control and low CV at equal per-type n (250/type) where binned TV fails due to sparse binning (0.625 expected counts/bin)?

## 3. Motivation

The density-divergence line of C-WEB-DYNAMICS experiments has established:

- **EXP-FRONTIER-34773875458**: Pooled binned TV (20×20 grid) detects action-conditional structure under non-stationarity (Spearman rho=0.929), but with severe absolute attenuation: pooled BC TV at lambda=1 drops from 0.952 (stationary) to 0.051 (non-stationary) — a 94.6% loss.

- **EXP-FRONTIER-34794649996**: Per-type bias correction with N=200 permutations per type does NOT recover signal: mean per-type BC TV at lambda=1 = 0.034, which is 0.67× pooled BC TV 0.051 and far below the >0.2 threshold. Null control fails (4/8 types >0.01 at lambda=0). Per-type instrument is noise-dominated at n=250/type (0.625 expected counts/bin on 400-bin grid).

- **EXP-FRONTIER-34881708619**: Pooled subsampled BC TV at equal per-type n (250/type) is 0.0510, ratio 1.49× per-type 0.0343. Preregistered paired t-test across 8 types: t=1.33 p_one=0.113 d=0.47 FAILS both p<0.05 and d>0.5. The 1.49× ratio confounds 5.0 vs 0.625 expected counts/bin density, so the question is not resolved.

The auditor identified that the per-type limitation may be specific to the binned TV estimator in sparse regimes (audit.json required_fixes[3]). The handoff recommends: "Design a Frontier experiment testing alternative divergence measures (KDE with cross-validated bandwidth, kNN mutual information, or kernel-based divergence) on the same synthetic 2D [0,1]^2 DGP with 8 heterogeneous page types at equal per-type n (250/type)."

## 4. Hypotheses

### H1: Per-Type Null Control with Alternative Measures
KDE and kNN measures achieve per-type null control (divergence <= permutation-based threshold at lambda=0) across all 8 page types. This would demonstrate that the per-type limitation is specific to binned TV sparse binning.

### H2: Positive Control
Pooled subsampled divergence (KDE and kNN) at lambda=1 is > pooled subsampled divergence at lambda=0 (detectable signal). This verifies each measure can detect action-conditioned structure in the DGP.

### H3: Low CV at Lambda=1
KDE and kNN per-type divergence at lambda=1 have CV <=0.5 across 5 replications for all 8 page types. This would indicate stable estimation at 250/type.

### H4: Improvement Over Binned TV
At least one alternative measure achieves both per-type null control and CV <=0.5 at lambda=1, whereas binned TV fails both (null control 4/8 >0.01, CV max 1.59).

## 5. Data Generation

### 5.1 Reuse Parent DGP

Identical to EXP-FRONTIER-34881708619 (which reused EXP-FRONTIER-34794649996):
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

### 6.1 KDE Divergence (Per-Type and Pooled)

For each page type separately on the full 250 transitions per type:
- Estimate joint density P(S_{t+1}, A) using Gaussian kernel density estimation (scipy.stats.gaussian_kde with bw_method='scott')
- Compute conditional density P(S_{t+1} | A=a) for each action a
- Compute KL divergence D_KL(P(S_{t+1} | A=a) || P(S_{t+1})) for each action a
- Use maximum KL divergence across actions as the measure
- Permutation null: N=200 permutations shuffling action labels within type
- Per-type KDE divergence = max(0, observed_KL - perm_mean_KL)

Pooled subsampled KDE divergence:
- For the SAME 2000 transitions, subsampled to 250 per type
- Pool all 2000 selected transitions (8 types × 250)
- Compute KDE divergence on pooled data
- Pooled subsampled permutation null: N=200 permutations on the subsampled data

### 6.2 kNN Mutual Information (Per-Type and Pooled)

For each page type separately on the full 250 transitions per type:
- Estimate mutual information I(S_{t+1}; A) using kNN estimator (k=5, Kraskov et al.)
- This is a non-parametric measure that does not depend on binning
- Permutation null: N=200 permutations shuffling action labels within type
- Per-type kNN MI = max(0, observed_MI - perm_mean_MI)

Pooled subsampled kNN MI:
- For the SAME 2000 transitions, subsampled to 250 per type
- Pool all 2000 selected transitions (8 types × 250)
- Compute kNN MI on pooled data
- Pooled subsampled permutation null: N=200 permutations on the subsampled data

### 6.3 Binned TV (Reference Only)

For comparison with parent results, recompute binned TV using identical 20×20 grid binning. This is not a primary measure but ensures comparability.

## 7. Statistical Tests

### 7.1 Primary: Per-Type Null Control

For each measure (KDE and kNN) separately:
- At lambda=0, per-type divergence <= permutation threshold (95th percentile of null distribution) across all 8 page types
- Count number of types that pass null control
- Decision: all 8 types must pass for the measure to pass null control

### 7.2 Secondary: CV Check

For each measure (KDE and kNN) separately:
- At lambda=1, compute CV across 5 replications for each page type
- Decision: CV <=0.5 for all 8 types across both measures

### 7.3 Positive Control

For each measure:
- Pooled subsampled divergence at lambda=1 > pooled subsampled divergence at lambda=0
- One-sided paired t-test across 5 replications, p<0.05

### 7.4 Comparison with Binned TV

- Compare per-type null control pass rates: alternative measures vs binned TV
- Compare CV at lambda=1: alternative measures vs binned TV
- Compute ratio of divergence magnitudes: alternative measures vs binned TV

## 8. Controls

### 8.1 Positive Control (Signal Detection)

Pooled subsampled divergence at lambda=1 > pooled subsampled divergence at lambda=0 for both KDE and kNN.
- Verifies: each measure can detect action-conditioned structure
- If fails: measure is insensitive to the DGP; MEASUREMENT_INVALID

### 8.2 Null Control (False Positive Control)

Per-type divergence at lambda=0 <= permutation threshold for all 8 page types for both KDE and kNN.
- Verifies: measures do not produce false positives in the null regime
- Threshold: 95th percentile of 200 permutations per type
- If fails: measure has inflated false positives; FALSIFIED-IN-SETTING

### 8.3 CV Control (Stability)

CV across 5 replications <=0.5 for all 8 page types at lambda=1 for both KDE and kNN.
- Verifies: measures produce stable estimates at 250/type
- If fails: measure is unstable at this sample size; FALSIFIED-IN-SETTING

### 8.4 Binned TV Replication Control

Recomputed binned TV per-type null control and CV match parent results (4/8 null control fail, CV max 1.59).
- Verifies: parent results are reproducible on same data
- If fails: pipeline error; MEASUREMENT_INVALID

## 9. Validity Threats

### 9.1 KDE Bandwidth Selection

KDE performance depends on bandwidth. Using Scott's rule (bw_method='scott') may not be optimal for the DGP. Mitigation: also test with cross-validated bandwidth (leave-one-out likelihood maximization) as a sensitivity analysis.

### 9.2 kNN Parameter Choice

kNN MI with k=5 may not be optimal for n=250. Mitigation: also test with k=3 and k=10 as sensitivity analysis.

### 9.3 Permutation Null Consistency

Permutation nulls assume exchangeability within type. For KDE and kNN, this may not hold if the density estimator is sensitive to label shuffling. Mitigation: compute null distribution empirically and verify that null divergence is near zero (as expected for random labels).

### 9.4 Synthetic-to-Real Gap

All evidence remains synthetic 2D [0,1]^2. No inference to real Web DOM transitions is justified. This experiment tests estimator methodology, not Web dynamics directly.

### 9.5 Sample Size Limitation

250 transitions per type may still be insufficient for stable KDE/kNN estimation. If both measures fail CV control, the limitation may be sample size, not estimator choice. Future experiments could increase per-type sample size.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST

If ALL of:
1. KDE per-type null control passes (all 8 types <= threshold at lambda=0)
2. kNN per-type null control passes (all 8 types <= threshold at lambda=0)
3. KDE CV <=0.5 for all 8 types at lambda=1
4. kNN CV <=0.5 for all 8 types at lambda=1
5. Positive control passes for both KDE and kNN (pooled divergence at lambda=1 > pooled divergence at lambda=0)
6. No pipeline errors

### 10.2 FALSIFIED-IN-SETTING

If ANY of:
1. KDE per-type null control fails (any type > threshold at lambda=0)
2. kNN per-type null control fails (any type > threshold at lambda=0)
3. KDE CV >0.5 for any type at lambda=1
4. kNN CV >0.5 for any type at lambda=1

### 10.3 MEASUREMENT_INVALID

If:
1. Pipeline errors prevent computation
2. Positive control fails (pooled divergence at lambda=1 <= pooled divergence at lambda=0 for either measure)
3. Sample size insufficient (<250 transitions per type)
4. Binned TV replication control fails (does not match parent results)

## 11. Analysis Plan

1. **Data Generation**: Use identical transitions from parent EXP-FRONTIER-34881708619 (reuse cached data)
2. **KDE Divergence**: For each lambda level, each rep, each page type, compute KDE divergence with Scott bandwidth
3. **kNN Mutual Information**: For each lambda level, each rep, each page type, compute kNN MI with k=5
4. **Binned TV Reference**: Recompute binned TV for comparison
5. **Permutation Nulls**: For each measure, each type, compute 200 permutation nulls
6. **Null Control**: Check per-type divergence <= 95th percentile of null at lambda=0
7. **CV Check**: Compute CV across 5 reps at lambda=1
8. **Positive Control**: Check pooled divergence at lambda=1 > pooled divergence at lambda=0
9. **Comparison**: Compare alternative measures with binned TV
10. **Reporting**: Report all outcomes with equal prominence

## 12. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for KDE (gaussian_kde) and statistical tests
- `sklearn.neighbors.KNeighborsRegressor` for kNN MI estimation (or custom implementation)
- Standard library only

Code will be committed to `research/experiments/EXP-FRONTIER-34913743596/` before execution.

## 13. Pre-registered Expectations

From the parent audit:
- The binned TV per-type limitation is attributed to sparse binning (0.625 expected counts/bin)
- KDE and kNN do not depend on fixed grid binning and may be robust to sparse regimes
- If the limitation is estimator-specific, alternative measures should achieve per-type null control
- If the limitation is fundamental to per-type estimation at 250/type, alternative measures will also fail

From statistical theory:
- KDE with adaptive bandwidth should handle sparse data better than fixed-grid binning
- kNN MI is non-parametric and should be more robust to sample size limitations
- However, both measures may still have high variance at n=250

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
