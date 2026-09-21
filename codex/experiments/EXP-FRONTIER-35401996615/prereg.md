# EXP-FRONTIER-35401996615 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-35401996615
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-18
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does per-type CV stability (<=0.5 at lambda=1) achieve at larger per-type n (500 and 1000/type) with KDE Scott or kNN k=5 under spec-compliant measurement (N=200 permutation nulls, full 8-lambda sweep, Kraskov k=5 kNN estimator, pipeline validation within 5% of parent baselines)?

## 3. Motivation

The density-divergence line of C-WEB-DYNAMICS experiments has established:

- **EXP-FRONTIER-34913743596** (audit PASS): KDE and kNN binning-free estimators achieve per-type null control (8/8 pass) at 250/type where binned TV fails (4/8 pass), confirming the binned TV false-positive is estimator-specific. However, per-type CV stability (<=0.5 at lambda=1) fails for both KDE (max 0.5745 type 4, 7/8 pass, marginal 14.9% over threshold) and kNN (max 0.7550 type 0, 7/8 pass, substantial 51% over threshold). Positive controls pass for both (KDE t=7.81 p=0.0007, kNN t=6.82 p=0.0012).

- **EXP-FRONTIER-35166507552** (MEASUREMENT_INVALID): Attempted sample-size scaling test but failed to execute frozen spec. Key failures: N_PERMS=5 instead of 200, pipeline validation off (KDE CV 0.3748 vs parent 0.5745, 34.8% off), kNN positive control inverted, lambda coverage truncated to 2/8 levels. This experiment adds no valid evidence.

- **Parent handoff**: Identifies two orthogonal paths: (1) sample-size scaling with spec-compliant measurement; (2) confirmatory kNN k=10 at 250/type. Recommends path (1) first.

The KDE marginal CV fail (0.5745, only 14.9% over 0.5) suggests sample-size increase may achieve stability. The kNN substantial CV fail (0.7550, 51% over) suggests the limitation may be more fundamental. This experiment tests the sample-size hypothesis under spec-compliant measurement.

## 4. Hypotheses

### H1: Sample-Size Scaling Resolves KDE Instability
KDE per-type CV <=0.5 for all 8 types at lambda=1 at n=500/type. This would demonstrate that the per-type KDE failure at 250/type (max CV 0.5745) is sample-size-limited.

### H2: Sample-Size Scaling Resolves kNN Instability (Weaker)
kNN per-type CV <=0.5 for all 8 types at lambda=1 at n=500/type or n=1000/type. Given the substantial failure at 250/type (max CV 0.7550), this is less likely but would indicate sample-size limitation rather than fundamental heterogeneity.

### H3: Both Measures Fail at 1000/Type
If CV >0.5 for any type at lambda=1 for BOTH KDE and kNN at n=1000/type, the per-type limitation is fundamental to heterogeneous page-type dynamics, not sample-size-specific.

### H4: Null Control Maintained at Larger Sample Sizes
Per-type null control (divergence <= permutation threshold at lambda=0) holds for all 8 types at all tested sample sizes for both KDE and kNN. If larger samples introduce false positives, the measures have fundamental calibration issues.

## 5. Data Generation

### 5.1 DGP

Identical DGP structure to parent EXP-FRONTIER-34913743596 (which reused EXP-FRONTIER-34881708619):
- 8 page types with different dynamics (rotation/scaling/translation, low/high noise, shifted centers)
- Same function parameters (THETA, OFFSET_A, SCALE, OFFSET_B, T_C, ALPHA_C)
- Same noise model (heteroscedastic Gaussian with state-dependent variance)
- Page type assignment: `type = (transition_index // per_type_n) mod 8`

Page type definitions (frozen from parent):
```python
PAGE_TYPES = [
    (42, 0.05, np.array([0.5, 0.5])),   # rotation, low noise, center
    (43, 0.05, np.array([0.5, 0.5])),   # scaling, low noise, center
    (44, 0.05, np.array([0.5, 0.5])),   # translation, low noise, center
    (42, 0.10, np.array([0.5, 0.5])),   # rotation, high noise, center
    (43, 0.10, np.array([0.5, 0.5])),   # scaling, high noise, center
    (44, 0.10, np.array([0.5, 0.5])),   # translation, high noise, center
    (42, 0.05, np.array([0.3, 0.7])),   # rotation, low noise, shifted
    (43, 0.05, np.array([0.3, 0.7])),   # scaling, low noise, shifted
]
```

### 5.2 Lambda Levels

8 lambda levels (full sweep): 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0

### 5.3 Sample Sizes

Three sample sizes tested:
- **n=250/type**: Pipeline validation (must replicate parent results within 5%)
- **n=500/type**: Primary test (2x parent sample)
- **n=1000/type**: Confirmatory test (4x parent sample)

For n=500: generate 500 i.i.d. transitions per type from the DGP (same random process as parent).
For n=1000: generate 1000 i.i.d. transitions per type from the DGP.

### 5.4 Replications

5 replications per lambda level per sample size (matching parent).

### 5.5 Total Transitions

- n=250/type: 8 lambda x 5 reps x 250 x 8 = 80,000 (pipeline validation)
- n=500/type: 8 lambda x 5 reps x 500 x 8 = 160,000
- n=1000/type: 8 lambda x 5 reps x 1000 x 8 = 320,000
- Grand total: 560,000 transitions

### 5.6 Seed Independence

Same formula as parent: `cell_seed = BASE_SEED * 100000 + lambda_idx * 1000 + rep_idx * 10 + 999`

For n=500 and n=1000, extend the DGP to generate additional i.i.d. draws per type using extended seed offsets. All randomness must use np.random.RandomState with explicit seeds; no unseeded np.random calls.

## 6. Measures

### 6.1 KDE Divergence (Per-Type and Pooled)

For each sample size, each page type, each lambda level, each replication:
- Generate per_type_n transitions from the DGP for that type
- Estimate joint density P(S_{t+1}, A) using Gaussian kernel density estimation (scipy.stats.gaussian_kde with bw_method='scott')
- Compute conditional density P(S_{t+1} | A=a) for each action a
- Compute KL divergence D_KL(P(S_{t+1} | A=a) || P(S_{t+1})) for each action a
- Use maximum KL divergence across actions as the measure
- Permutation null: N=200 permutations shuffling action labels within type
- Per-type KDE divergence = max(0, observed_KL - perm_mean_KL)

Pooled subsampled KDE divergence:
- Pool all transitions across types for that sample size
- Compute KDE divergence on pooled data
- Pooled subsampled permutation null: N=200 permutations on the pooled data

### 6.2 kNN Mutual Information (Per-Type and Pooled)

For each sample size, each page type, each lambda level, each replication:
- Generate per_type_n transitions from the DGP for that type
- Estimate mutual information I(S_{t+1}; A) using kNN estimator (k=5, Kraskov et al. via sklearn.neighbors.NearestNeighbors)
- Permutation null: N=200 permutations shuffling action labels within type
- Per-type kNN MI = max(0, observed_MI - perm_mean_MI)

Pooled subsampled kNN MI:
- Pool all transitions across types for that sample size
- Compute kNN MI on pooled data
- Pooled subsampled permutation null: N=200 permutations on the pooled data

### 6.3 Pipeline Validation (n=250/Type)

At n=250/type, recompute KDE and kNN to verify replication of parent results:
- KDE per-type null control: expect 8/8 pass
- KDE CV at lambda=1: expect max ~0.575 (within 5% = 0.546-0.604)
- kNN per-type null control: expect 8/8 pass
- kNN CV at lambda=1: expect max ~0.755 (within 5% = 0.717-0.793)

## 7. Statistical Tests

### 7.1 Primary: CV Check at Each Sample Size

For each measure (KDE and kNN) at each sample size (250, 500, 1000):
- At lambda=1, compute CV across 5 replications for each page type
- Decision: CV <=0.5 for all 8 types for the measure to pass at that sample size

### 7.2 Secondary: Sample-Size Trend

For each measure, for each page type that fails CV at 250/type:
- Compute CV at 250, 500, and 1000/type
- Report the trend (decreasing, stable, increasing)
- If CV decreases monotonically with n, extrapolate to estimate the n required for CV <=0.5

### 7.3 Null Control at Each Sample Size

For each measure at each sample size:
- At lambda=0, per-type divergence <= permutation threshold (95th percentile of 200 permutations) across all 8 page types
- Count number of types passing null control

### 7.4 Positive Control

For each measure at each sample size:
- Pooled subsampled divergence at lambda=1 > pooled subsampled divergence at lambda=0
- One-sided paired t-test across 5 replications, p<0.05

### 7.5 Pipeline Validation

At n=250/type, verify that KDE and kNN metrics replicate parent results within 5% tolerance.

## 8. Controls

### 8.1 Pipeline Validation Control (n=250/Type)

KDE and kNN metrics at 250/type must replicate parent EXP-FRONTIER-34913743596 within 5%:
- KDE null control: 8/8 pass
- KDE CV max: ~0.575 (within 5% = 0.546-0.604)
- kNN null control: 8/8 pass
- kNN CV max: ~0.755 (within 5% = 0.717-0.793)
- Verifies: pipeline consistency with parent experiment
- If fails: MEASUREMENT_INVALID

### 8.2 Positive Control (Signal Detection)

Pooled subsampled divergence at lambda=1 > pooled subsampled divergence at lambda=0 for both KDE and kNN at all sample sizes.
- Verifies: each measure can detect action-conditioned structure at every tested n
- If fails for any measure at any n: MEASUREMENT_INVALID

### 8.3 Null Control (False Positive Control)

Per-type divergence at lambda=0 <= permutation threshold for all 8 page types for both KDE and kNN at all sample sizes.
- Verifies: measures do not produce false positives in the null regime at any sample size
- If fails at any n for either measure: FALSIFIED-IN-SETTING

### 8.4 Sample-Size Monotonicity Check

For each measure and each type, CV at 250/type >= CV at 500/type >= CV at 1000/type (monotonic decrease). If CV increases with n for any type, this indicates an anomalous estimator behavior that requires investigation.
- This is a descriptive check, not a formal decision criterion

## 9. Validity Threats

### 9.1 DGP Generality

All evidence remains synthetic 2D [0,1]^2 with 8 heterogeneous affine page types and heteroscedastic Gaussian noise. No inference to real Web DOM transitions is warranted. The experiment tests whether sample-size scaling resolves per-type instability in this specific DGP, not whether per-type estimation works on real Web data.

### 9.2 KDE Bandwidth at Larger N

KDE performance depends on bandwidth selection. Scott's rule adapts to sample size, but the bandwidth at n=1000 may differ qualitatively from n=250. If CV fails at n=1000, it could reflect bandwidth misspecification rather than fundamental limitation. Mitigation: report Scott bandwidth at each n and check if bandwidth scaling is reasonable.

### 9.3 kNN Neighbor Count at Larger N

kNN with k=5 may not be optimal at n=1000 (neighbors may be too close). The exploratory kNN k=10 result at 250/type (CV max 0.470) suggests larger k may be beneficial. Mitigation: as a sensitivity analysis, also compute kNN k=10 at n=500 and n=1000 if primary results are ambiguous.

### 9.4 Permutation Null Consistency

Permutation nulls assume exchangeability within type. At larger n, the null distribution may have different shape. Mitigation: compute null distribution empirically and verify null divergence is near zero at all sample sizes.

### 9.5 Sample-Size Extrapolation

If CV passes at n=500 but not n=250, it demonstrates sample-size limitation for the tested DGP. However, the extrapolation to real Web data is not warranted. The conclusion is bounded to the synthetic 2D DGP.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST

If ANY of:
1. KDE CV <=0.5 for all 8 types at lambda=1 at n=500/type, OR
2. KDE CV <=0.5 for all 8 types at lambda=1 at n=1000/type, OR
3. kNN CV <=0.5 for all 8 types at lambda=1 at n=500/type, OR
4. kNN CV <=0.5 for all 8 types at lambda=1 at n=1000/type

AND:
5. Null control passes for all 8 types at all tested sample sizes for the passing measure
6. Positive control passes for the passing measure at all tested sample sizes
7. Pipeline validation at 250/type replicates parent results (KDE CV max 0.546-0.604, kNN CV max 0.717-0.793)

### 10.2 FALSIFIED-IN-SETTING

If:
1. CV >0.5 for any type at lambda=1 for BOTH KDE and kNN at n=1000/type
2. AND null control passes for both measures at n=1000/type
3. AND positive control passes for both measures at n=1000/type

This demonstrates that even 4x the parent sample size does not resolve per-type instability, indicating a fundamental limitation.

### 10.3 MEASUREMENT_INVALID

If:
1. Pipeline errors prevent computation
2. Positive control fails for either measure at any sample size
3. Pipeline validation at 250/type fails to replicate parent results (KDE CV max outside 0.546-0.604, kNN CV max outside 0.717-0.793)
4. Sample size generated is <90% of target per type

## 11. Analysis Plan

1. **Pipeline Validation**: Generate n=250/type transitions, compute KDE and kNN with N=200 permutation nulls, verify replication of parent results within 5%
2. **Primary Test (n=500)**: Generate n=500/type transitions, compute KDE and kNN divergence with N=200 permutation nulls, check CV
3. **Confirmatory Test (n=1000)**: Generate n=1000/type transitions, compute KDE and kNN divergence with N=200 permutation nulls, check CV
4. **Sensitivity (if ambiguous)**: At n=500 and n=1000, also compute kNN k=10 (from exploratory result)
5. **Permutation Nulls**: For each measure, each type, each sample size, compute 200 permutation nulls
6. **Null Control**: Check per-type divergence <= 95th percentile of null at lambda=0 at each sample size
7. **CV Check**: Compute CV across 5 reps at lambda=1 at each sample size
8. **Positive Control**: Check pooled divergence at lambda=1 > pooled divergence at lambda=0 at each sample size
9. **Sample-Size Trend**: Plot CV vs n for each failing type, report trend
10. **Reporting**: Report all outcomes with equal prominence

## 12. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for KDE (gaussian_kde) and statistical tests
- `sklearn.neighbors.NearestNeighbors` for Kraskov et al. kNN MI estimator (k=5)
- Standard library only

Code will be committed to `research/experiments/EXP-FRONTIER-35401996615/` before execution.

## 13. Pre-registered Expectations

From the parent experiment:
- KDE marginal CV fail (0.575, only 14.9% over 0.5) suggests sample-size increase may achieve stability
- kNN substantial CV fail (0.755, 51% over 0.5) suggests the limitation may be more fundamental
- The per-type CV failure generalizes beyond binning to sample-size/heterogeneity at 250/type

From statistical theory:
- KDE bandwidth adapts to sample size (Scott rule: h ~ n^(-1/(d+4)))
- At n=500, KDE bandwidth ~ 0.76x of n=250 bandwidth (sharper density estimate)
- At n=1000, KDE bandwidth ~ 0.60x of n=250 bandwidth
- kNN with fixed k=5 has effective smoothing that decreases with n (neighbors closer)
- Both measures should have lower variance at larger n, but the per-type heterogeneity may persist

Expected outcomes:
- Most likely: KDE passes at n=500 (marginal failure suggests nearby threshold), kNN fails at n=500 but may pass at n=1000
- Alternative: both pass at n=500, or both fail at n=1000
- Unlikely: kNN passes at n=500 but KDE fails (KDE was closer to threshold)

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration. Specifically:
- Testing kNN k=10 at larger n is EXPLORATORY (inherited from parent exploratory result)
- Testing additional bandwidth values for KDE is EXPLORATORY
- Any change to the DGP, lambda levels, or decision rule requires a new preregistration

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
