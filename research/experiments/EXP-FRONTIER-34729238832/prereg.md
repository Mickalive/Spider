# EXP-FRONTIER-34729238832 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34729238832
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can binned PCA projection to 2D-3D subspaces before divergence computation detect both scaling-type and rotation-type action-dependent structure simultaneously in the same 10D non-Gaussian DGP — or does dimensionality reduction destroy the discriminating information that both kNN TV (full-space neighbor ratios) and KDE (full-space kernel smoothing) each partially capture?

## 3. Motivation

Four consecutive Frontier experiments have established a convergent meta-finding:

1. **EXP-FRONTIER-34065969836** (kNN TV, raw): scaling rho=-0.12 (FAIL), rotation rho=0.93 (PASS)
2. **EXP-FRONTIER-34121473072** (kNN TV, bias-corrected): scaling rho=-0.12 (FAIL), rotation rho=0.93 (PASS)
3. **EXP-FRONTIER-34538185726** (KDE): scaling rho=0.71 (borderline), rotation rho=0.29 (FAIL)
4. All experiments: translation PASS with both estimators

The complementary blind spots (kNN fails scaling, KDE fails rotation) suggest the per-function heterogeneity is not purely estimator-specific. Two competing hypotheses:

**Hypothesis A (Curse of Dimensionality)**: The information for detecting all structure types is present in the 10D data, but full-space estimators lose sensitivity to different structure types at high dimension due to distance concentration. Dimensionality reduction should rescue both simultaneously.

**Hypothesis B (Information-Theoretic Limit)**: The 10D non-Gaussian DGP genuinely lacks sufficient information for simultaneous detection of scaling and rotation. No estimation approach can detect both.

This experiment tests Hypothesis A by projecting 10D states to 2D-3D subspaces via PCA before computing divergence. PCA is materially orthogonal to both kNN (local neighbor ratios) and KDE (full-space kernel smoothing) because it operates on global variance structure rather than local density estimation.

If PCA rescues both scaling and rotation: Hypothesis A supported. The per-function heterogeneity is dimensionality-driven. SPIDER should use dimensionality reduction as preprocessing for divergence computation.

If PCA fails on one or both: Hypothesis B more firmly established. Frontier should pivot to real Web data or orthogonal mechanisms.

## 4. Hypotheses

### H1: PCA Rescues Both Functions
Binned TV divergence on PCA-projected (10D -> 2D/3D) states detects both scaling-type and rotation-type dynamics simultaneously: per-function Spearman rho >= 0.65 with p < 0.0167 (Bonferroni x3) for ALL functions including scaling.

### H2: Positive Control
At lambda=1, binned TV on PCA-projected states >= 0.01 across all 3 functions.

### H3: Null Control
At lambda=0, binned TV on PCA-projected states is indistinguishable from zero (permutation test p > 0.05).

### H4: Function Invariance
No significant function x lambda interaction (two-way ANOVA p > 0.05).

### H5: Dimensionality Comparison
2D PCA projection and 3D PCA projection yield qualitatively similar results (both detect scaling and rotation, or both fail). If 3D succeeds but 2D fails, the information is present but requires more projection dimensions.

## 5. Data Generation

### 5.1 Synthetic Transition Model

Same 10D non-Gaussian DGP as parent experiments:
- State space: S = [0,1]^10 (10D continuous)
- Noise: mixture-of-3-Gaussians heteroscedastic noise
- Transition function: S_{t+1} = f(S_t, A_t, lambda, noise)
- Action space: 4 action types (matching parent design)

### 5.2 Deterministic Functions

Three independent frozen function families (seeds 42, 43, 44):
- **Function 42 (rotation)**: 10D rotation matrix parameterized by action
- **Function 43 (scaling)**: 10D diagonal scaling matrix parameterized by action
- **Function 44 (translation)**: 10D translation vector parameterized by action

### 5.3 Lambda Levels

Eight conditions matching parent design:
- lambda=0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0

### 5.4 Sample Size

- 500 transitions per lambda level per function (8 levels x 3 functions x 500 = 12,000 total)
- 10 independent replications per cell for variance estimation
- Total: 120,000 transitions

## 6. PCA Implementation

### 6.1 PCA Fitting

- Use sklearn.decomposition.PCA
- Fit PCA on each cell independently (per function, per lambda, per replication)
- No cross-cell information leakage
- Principal components computed from full cell data (500 transitions x 10D)

### 6.2 Projection Dimensions

Test two projection targets:
- **2D**: PCA(n_components=2) — most aggressive dimensionality reduction
- **3D**: PCA(n_components=3) — moderate reduction

Both are tested; the frozen decision rule applies to each independently.

### 6.3 Explained Variance Reporting

Record explained variance ratio for each PCA fit to assess how much information is retained in the projection.

## 7. Binned TV Divergence

### 7.1 Implementation

- Project 10D states to 2D or 3D via PCA
- Bin projected states into histogram: 10 bins per dimension
- For each action a, compute histogram H_a of projected next-states conditioned on action a
- TV divergence: TV(H_a, H_b) = 0.5 * sum |H_a(i) - H_b(i)| for all pairs of actions
- Aggregate: mean TV across all action pairs

### 7.2 Rationale

Binned TV on projected states is simpler than KDE (no bandwidth selection) and directly tests whether the information for distinguishing action-conditional distributions survives dimensionality reduction.

## 8. Measures

### 8.1 Primary Metric
- **binned_TV**: Mean TV divergence across action pairs on PCA-projected states
- **Spearman rho(binned_TV, lambda)**: Monotonicity of divergence with action-dependence

### 8.2 Secondary Metrics
- Explained variance ratio of PCA (information retention)
- Per-function Spearman rho (rotation, scaling, translation)
- Cohen's d (lambda=0 vs lambda=1)
- Function invariance (ANOVA interaction)

## 9. Null Models

### 9.1 Shuffle Null
Permute action labels across transitions. TV on shuffled data should be near zero at all lambda levels.

### 9.2 Frequency Null
Predict next-state from marginal distribution P(S_{t+1}). Expected TV: near zero.

## 10. Statistical Tests

### 10.1 Primary Test
- Spearman rank correlation: rho(binned_TV, lambda)
- One-sided test: rho > 0
- Bonferroni correction for 3 functions

### 10.2 Paired Comparisons
- At each lambda level: paired t-test, binned_TV vs permutation null
- Two-sided, alpha=0.05
- Bonferroni corrected

### 10.3 Effect Size
- Cohen's d for binned_TV at lambda=0 vs lambda=1

### 10.4 Function Invariance
- Two-way ANOVA: binned_TV ~ lambda + function + lambda:function
- Non-significant interaction term (p>0.05) supports function invariance

## 11. Controls

### 11.1 Positive Control (lambda=1)
- Binned TV must be >= 0.01 across all 3 functions
- Verifies: PCA + binned TV pipeline detects maximal action-dependent structure

### 11.2 Null Control (lambda=0)
- Binned TV must be indistinguishable from zero (permutation test p > 0.05)
- Verifies: pipeline does not detect structure when absent

### 11.3 Sensitivity Control
- Binned TV should be monotonically increasing across lambda levels
- Tests whether PCA preserves the monotonic scaling relationship

### 11.4 Dimensionality Control
- Compare 2D vs 3D PCA results
- If 3D succeeds but 2D fails, information is present but requires more dimensions
- If both succeed or both fail, result is robust to projection dimensionality

## 12. Validity Threats

### 12.1 Information Loss from Projection
PCA is a linear projection; nonlinear structure may be destroyed. Mitigation: test both 2D and 3D; if 3D succeeds but 2D fails, this is informative. Nonlinear methods (e.g., t-SNE, UMAP) are not tested in this experiment but could follow.

### 12.2 PCA Fit on Small Samples
With 500 transitions and 10D, PCA may not capture the most informative directions. Mitigation: explained variance ratio is reported; if < 50% variance retained, the projection is insufficient and the finding should be interpreted accordingly.

### 12.3 Binned TV Sensitivity
10 bins per dimension may be too coarse or too fine. Mitigation: this is a fixed parameter; sensitivity to bin count is not tested in this experiment but could follow.

### 12.4 Synthetic-to-Real Gap
Same as parent experiments: all evidence is synthetic 10D [0,1]^10 with toy affine families. No DOM embeddings, session history, or real action semantics.

### 12.5 Multiple Comparisons
With 3 functions tested independently, Bonferroni x3 correction is applied. This is conservative but appropriate for confirmatory claims.

## 13. Decision Rules

### 13.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Per-function Spearman rho(binned_TV, lambda) >= 0.65, p < 0.0167 one-sided (Bonferroni x3) for EACH function including scaling
2. Positive control passes: binned TV >= 0.01 at lambda=1 across all functions
3. Null control passes: permutation test p > 0.05 at lambda=0
4. No significant function x lambda interaction (two-way ANOVA p > 0.05)
5. No pipeline errors

### 13.2 FALSIFIED-IN-SETTING
If ANY of:
1. Per-function Spearman rho < 0.65 or p > 0.0167 for ANY function
2. Positive control fails
3. Null control fails
4. Significant function x lambda interaction

### 13.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. PCA fails to converge
3. Binned TV CV across replications > 0.5 at lambda=1
4. Sample size insufficient

## 14. Expected Outcomes

### 14.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates per-function heterogeneity is a curse-of-dimensionality artifact
- The information for detecting all structure types is present in the 10D data
- Full-space estimators (kNN, KDE) lose sensitivity due to high-dimensional geometry
- SPIDER should use PCA/dimensionality reduction as preprocessing for divergence computation
- The kNN scaling failure and KDE rotation failure are estimator limitations, not information-theoretic limits

### 14.2 Negative Result (FALSIFIED-IN-SETTING)
- Per-function heterogeneity is not purely dimensionality-driven
- The information-theoretic limit is more firmly established
- Frontier should pivot to real Web transition data or fundamentally different mechanisms
- The density-divergence approach may be fundamentally limited for simultaneous detection of all structure types

### 14.3 Mixed Result
- PCA rescues one function but not the other (e.g., scaling but not rotation)
- This would indicate that different structure types have different dimensionality requirements
- Further experiments with nonlinear projections or different subspaces may be warranted

### 14.4 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging
- Not scientific evidence for or against

## 15. Analysis Plan

1. **Data Generation**: Generate 120,000 transitions at 8 lambda levels x 3 functions x 10 reps
2. **PCA Projection**: For each cell, fit PCA and project to 2D and 3D
3. **Binned TV**: Compute TV divergence on projected states for each action pair
4. **Statistical Tests**: Spearman correlation, paired t-tests with Bonferroni correction, two-way ANOVA
5. **Controls**: Verify positive, null, sensitivity, and dimensionality controls
6. **Comparison**: Compare PCA-projected results with full-space kNN and KDE results from parent experiments
7. **Reporting**: Report all outcomes with equal prominence

## 16. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for Spearman correlation and t-tests
- `sklearn.decomposition.PCA` for dimensionality reduction
- `statsmodels` for two-way ANOVA
- Standard library only (no custom estimators required)

Code will be committed to `research/frontier/pca_projection/` before execution.

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
