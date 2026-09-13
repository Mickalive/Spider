# EXP-FRONTIER-34729238832 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34729238832
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-FRONTIER-34538185726 (MEASUREMENT_INVALID)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Can PCA projection of 10D state vectors to a 2D principal subspace before binned histogram Jensen-Shannon divergence computation detect both scaling-type and rotation-type action-dependent structure simultaneously in the same 10D non-Gaussian DGP — or does dimensionality reduction destroy the discriminating information that both kNN TV (full-space neighbor ratios) and KDE (full-space kernel smoothing) each partially capture?

## 3. Motivation

### What the parent experiments established

Four Frontier experiments have converged on the same meta-finding: **no single full-space density-divergence estimator works uniformly across all function families in this 10D non-Gaussian DGP.** The complementary blind spots are:

| Experiment | Estimator | Translation rho | Rotation rho | Scaling rho | Function Invariance |
|---|---|---|---|---|---|
| EXP-FRONTIER-34065969836 | kNN TV (raw) | 1.0 | 0.83 | 0.16 | FAIL |
| EXP-FRONTIER-34121473072 | kNN TV (bias-corrected) | 1.0 | 0.93 | -0.12 | FAIL |
| EXP-FRONTIER-34538185726 | KDE (CV bandwidth) | 0.81 | 0.29 | 0.71 | FAIL |

Key observations:
- kNN TV detects rotation (0.93) but fails scaling (-0.12)
- KDE partially detects scaling (0.71) but fails rotation (0.29)
- Both detect translation (>=0.81)
- Function invariance decisively fails in ALL experiments (ANOVA p~0)

The parent audit (EXP-FRONTIER-34538185726) identified this as potentially a **curse-of-dimensionality artefact**: different estimation principles lose sensitivity to different types of structure at high dimension due to distance concentration. If this is correct, dimensionality reduction before divergence estimation should rescue the blind spots.

### Why PCA projection is materially different from full-space estimation

The three tested estimation principles (kNN neighbor ratios, KDE kernel smoothing, permutation-null bias correction) all operate in the full 10D space. PCA projection is a fundamentally different intervention:

| Property | kNN TV / KDE (full-space) | PCA projection |
|---|---|---|
| Dimensionality | 10D (distance concentration) | 2D (concentrated signal) |
| Estimation | Local (kNN) or global (KDE) density | Linear subspace projection |
| Bandwidth/parameter | k or h (sensitive to 10D geometry) | Number of components (insensitive) |
| Signal preservation | Loses different structure per estimator | Preserves principal variance directions |

PCA captures the directions of maximum variance, which is precisely where scaling (variance modulation) and rotation (directional transformation) manifest. By projecting to 2D before divergence computation, we test whether the information for scaling and rotation detection exists in the data but is lost by full-space estimation.

### Hypothesis

If PCA projection to 2D before binned histogram JS divergence detects both scaling AND rotation simultaneously (per-function rho >= 0.65 with Bonferroni-corrected p < 0.025 for both), the per-function heterogeneity was a curse-of-dimensionality artefact. The Frontier lane should adopt PCA-projected divergence as its primary detection mechanism.

If PCA projection fails on one or both function families, the information-theoretic limit is more firmly established and the Frontier lane must pivot to real Web transition data or orthogonal mechanisms (neural density estimation, causal factorization, multi-scale analysis).

### Why this is the minimum next experiment

The parent handoff explicitly recommends testing binned PCA projection before divergence computation as the minimum next experiment before pivoting to real Web data. This is because:
1. Three full-space experiments have converged on complementary blind spots — more full-space estimator variations would have near-zero marginal information gain
2. PCA projection tests a materially orthogonal hypothesis (dimensionality vs estimation principle)
3. The implementation is straightforward (numpy SVD + binned histogram) with no new infrastructure
4. Either outcome (rescue or failure) is decisive for the Frontier lane strategy

## 4. Hypotheses

### H1: PCA Rescues Both Scaling and Rotation
PCA-projected binned JS divergence for scaling-type dynamics increases monotonically with lambda (Spearman rho >= 0.65, p < 0.025 one-sided Bonferroni x2). Same for rotation-type dynamics. Both functions pass simultaneously.

### H2: Positive Control
At lambda=1, binned JS divergence on 2D-projected states >= 0.01 across all 3 functions.

### H3: Null Control
At lambda=0, binned JS divergence is indistinguishable from zero (permutation test p > 0.05 per function, Fisher combined).

### H4: Translation Preservation
PCA projection does not destroy translation detection: translation rho >= 0.65 (maintains parent full-space detection).

### H5: Function Invariance
Detection is consistent across 3 functions (no significant function x lambda interaction, two-way ANOVA p > 0.05).

## 5. Data Generation

### 5.1 Synthetic Transition Model

Same DGP as parent experiments:
- State space: S = [0,1]^10 (10D continuous)
- Action space: A = {click, fill, submit, navigate} (4 actions)
- Transition: S_next = f(S, A, lambda) + noise
- Boundary: clip to [0,1]

For each transition:
1. Draw S ~ Uniform([0,1]^10)
2. Draw A uniformly from 4 actions
3. With probability lambda: S_next = deterministic_function(S, A) + mixture_noise(S)
4. With probability (1-lambda): S_next ~ Mixture-of-3-Gaussians centered at 0.5

### 5.2 Deterministic Functions

Same functions as parent (identical implementation):
- **Function 44 (translation)**: S_next = S + t(S, A), where t depends on S values and action direction
- **Function 42 (rotation)**: S_next = R(S, A) @ (S - 0.5) + 0.5 + offset, rotation angle depends on S[action_dim]
- **Function 43 (scaling)**: S_next = scale_factor * (S - 0.5) + 0.5 + offset, scale_factor = 1.0 + 0.2 * S[action_dim] * sign

### 5.3 Noise Model

Mixture-of-3-Gaussians heteroscedastic noise (identical to parent):
- 50% N(0, sigma_base), 30% N(0.1*sigma_base, 0.5*sigma_base), 20% N(-0.1*sigma_base, 2*sigma_base)
- sigma_base = 0.05 * (1 + 0.5 * ||S - 0.5||)
- Noise is state-dependent (heteroscedastic)

### 5.4 Lambda Levels

Eight conditions (same as parent):
- **lambda=0.0**: Pure noise, no action-dependence (null control)
- **lambda=0.1**: Very low action-dependence
- **lambda=0.2**: Low action-dependence
- **lambda=0.3**: Low-moderate action-dependence
- **lambda=0.4**: Moderate action-dependence
- **lambda=0.5**: Mixed regime
- **lambda=0.7**: High action-dependence
- **lambda=1.0**: Pure signal, full action-dependence (positive control)

### 5.5 Sample Size

- 500 transitions per lambda level per function per replication
- 8 levels x 3 functions x 10 replications x 500 = 120,000 total transitions
- Same total as parent for direct comparison

## 6. PCA Projection

### 6.1 PCA Fitting

For each replication:
1. Generate lambda=1 transitions for all 3 functions (3 x 500 = 1500 transitions)
2. Pool the next-state vectors S_next ∈ R^10
3. Fit PCA via SVD: [U, S, Vt] = np.linalg.svd(X - mean(X), full_matrices=False)
4. Principal components = Vt[0:2] (top 2 eigenvectors)
5. Explained variance ratio = S[0:2]^2 / sum(S^2)
6. Projection matrix W = Vt[0:2].T (10D → 2D)

### 6.2 PCA Health Check

Before divergence computation, verify:
1. Explained variance ratio for top 2 components >= 50% (otherwise PCA is not capturing meaningful structure)
2. Condition number of projection matrix is finite (no degenerate projection)
3. Projected points span [0,1]^2 (or close to it) after min-max scaling

If any health check fails, verdict = MEASUREMENT_INVALID.

### 6.3 Projection Application

For each cell (lambda, function, replication):
1. Generate 500 transitions
2. Project S_next vectors: Z = (S_next - mean_X) @ W where mean_X and W are from step 6.1
3. Min-max scale Z to [0,1]^2 (using min/max from lambda=1 pooled data for consistency)

### 6.4 Why 2D (not 3D or 1D)

2D is the primary projection dimension because:
1. It maximally reduces dimensionality while preserving 2D structure (rotation is inherently 2D)
2. Binned histogram on 20x20 grid = 400 bins, adequate for 500 samples (~1.25 per bin average)
3. 2D is visually inspectable for debugging
4. Kaiser criterion (eigenvalue > 1) typically selects 2-3 components for this DGP

If 2D explained variance < 50%, test 3D as secondary (20x20x20 = 8000 bins, potentially sparse).

## 7. Binned Histogram Jensen-Shannon Divergence

### 7.1 Histogram Construction

For each cell (lambda, function, replication):
1. Project 500 transitions to 2D → Z ∈ [0,1]^2
2. Group by action → ~125 transitions per action
3. For each action a, compute 2D histogram: H_a[i,j] = count of points in bin (i,j) / total
4. Bin edges: 20 equally spaced bins in [0,1] per dimension → 20x20 = 400 bins
5. Apply Laplace smoothing: H_a_smooth[i,j] = (H_a[i,j] + epsilon) / (1 + epsilon * 400) where epsilon = 1e-10

### 7.2 Jensen-Shannon Divergence

For each cell, compute pairwise JS divergence between all 6 action pairs:
- JS(P_a || P_b) = 0.5 * KL(P_a || M) + 0.5 * KL(P_b || M)
- M = 0.5 * (P_a + P_b)
- KL(P || Q) = sum(P[i,j] * log(P[i,j] / Q[i,j])) for all bins where P[i,j] > 0
- Primary metric: max JS across all 6 action pairs
- Secondary: mean JS across all 6 pairs

### 7.3 Why Binned Histogram Instead of KDE

The parent KDE experiment (EXP-FRONTIER-34538185726) identified bandwidth selection as a key validity threat (V7: over-smoothing in 10D, mean bandwidth factor 1.24x Scott's rule). Binned histogram avoids this entirely:
- No bandwidth parameter to select
- No kernel smoothing to tune
- Fixed 20x20 grid is deterministic
- Computationally faster (no iterative bandwidth search)
- In 2D, bin counts are stable with ~125 samples per action

The trade-off: binned histogram is less smooth than KDE and may miss structure that falls between bins. With 20x20 bins on [0,1]^2, bin width is 0.05, which is adequate for detecting the translation offsets (~0.1) and scaling modulations (~0.2) in this DGP.

### 7.4 Bias Correction

Same approach as parent:
- For each cell, compute permutation-null JS divergence (shuffle action labels, recompute JS)
- N_PERMUTATIONS = 100 per cell (increased from parent's 50 for better resolution)
- Bias-corrected JS = max(0, raw_JS - mean(perm_JS))

### 7.5 JS Variance Estimation

To address parent audit finding V5 (MC variance vs DGP variance conflation):
- Compute JS divergence 5 times per cell with different random seeds for bin assignment (jitter bin edges by +/- 10% of bin width)
- Report mean and SD across 5 JS computations
- If JS CV across 5 computations > 0.3 at lambda=1, flag as measurement stability concern

## 8. Measures

### 8.1 Primary Metric
- **pca_binned_js_max_by_lambda**: Maximum pairwise binned JS divergence at each lambda level, averaged across 3 functions x 10 replications
- **spearman_rho_per_function**: Spearman correlation between pca_binned_js_max and lambda for scaling (func 43) and rotation (func 42) independently (n=8, Bonferroni x2 corrected)

### 8.2 Secondary Metrics
- Mean pairwise JS divergence (averaged across 6 action pairs) at each lambda level
- Per-replication JS divergence (variance across replications)
- PCA explained variance ratio for top 2 components
- PCA eigenvalue spectrum
- Comparison with parent kNN TV and KDE (qualitative)
- Cohen's d of JS divergence at lambda=1 vs lambda=0
- Two-way ANOVA: JS ~ lambda + function + lambda:function

### 8.3 Comparison with Parent
- Direct comparison of PCA-projected binned JS vs parent kNN TV bc_divergence and KDE bc_JS for scaling-type dynamics
- If PCA scaling rho >= 0.65 and both parent estimators fail (kNN -0.12, KDE 0.71 p>0.0167): PCA rescues scaling
- If PCA scaling rho < 0.65: dimensionality reduction does not help, information-theoretic limit

## 9. Null Models

### 9.1 Permutation Null
For each cell, shuffle action labels across transitions and recompute binned histogram + JS divergence. The shuffled JS distribution provides the null for testing whether observed JS is significantly > 0.

### 9.2 Frequency Null
Under no action-dependence (lambda=0), all action-conditional histograms are identical to the marginal P(S_next). Expected JS divergence = 0.

## 10. Statistical Tests

### 10.1 Primary Test (Per-Function: Scaling + Rotation)
- Spearman rho between pca_binned_js_max and lambda for scaling (func 43) and rotation (func 42)
- One-sided test: rho > 0
- Bonferroni corrected: p < 0.05/2 = 0.025 per function
- Required rho threshold: >= 0.65

### 10.2 Translation Preservation Test
- Spearman rho for translation (func 44)
- Single comparison, threshold rho >= 0.65, p < 0.05 one-sided
- Must not degrade below parent's full-space rho=0.81

### 10.3 Aggregate Test (Secondary)
- Spearman rho on aggregate pca_binned_js_max (averaged across functions)
- Single comparison, no Bonferroni correction
- Threshold: rho >= 0.65, p < 0.05 one-sided

### 10.4 Permutation Tests
- At lambda=0: per-function test JS > 0 (one-sided, 100 permutations per cell)
- Fisher's method to combine p-values across 10 replications per function
- Combined p < 0.05 indicates null control failure

### 10.5 Two-Way ANOVA
- JS_divergence ~ lambda + function + lambda:function
- With 240 observations (8 x 3 x 10), adequate residual df for interaction estimation
- Non-significant interaction (p > 0.05) supports function invariance

### 10.6 Effect Size
- Cohen's d for JS divergence at lambda=1 vs lambda=0

## 11. Controls

### 11.1 Positive Control (lambda=1)
- Binned JS >= 0.01 across all 3 functions
- Verifies: PCA + binned JS pipeline detects maximal action-dependent structure

### 11.2 Null Control (lambda=0)
- Permutation test p > 0.05 per function (Fisher combined across reps)
- Verifies: pipeline does not detect structure when absent

### 11.3 Permutation Null Control
- Shuffled action labels yield JS divergence near zero at all lambda levels
- Verifies: observed JS is driven by action-dependence, not sampling artifacts

### 11.4 Function Invariance Control
- Two-way ANOVA interaction p > 0.05
- With 240 observations, residual df = 240 - 8 - 3 - 14 = 215 (adequate)

### 11.5 PCA Health Control
- Explained variance ratio for top 2 components >= 50%
- Verifies: PCA captures meaningful variance structure

### 11.6 Measurement Stability Control
- JS CV across replications < 0.5 at lambda=1 for all functions
- Verifies: binned JS computation is stable

## 12. Validity Threats

### 12.1 PCA Information Loss
Projection from 10D to 2D discards 8 dimensions of information. If the scaling or rotation structure lies primarily in discarded dimensions, PCA will not rescue detection. **Mitigation**: PCA captures maximum-variance directions; scaling and rotation modify variance structure along principal axes. Test 3D projection as secondary if 2D explained variance < 50%.

### 12.2 Binned Histogram Granularity
20x20 bins on [0,1]^2 may be too coarse or too fine. **Mitigation**: 20 bins gives 0.05 bin width, adequate for detecting offsets of ~0.1 (translation) and modulations of ~0.2 (scaling). Sensitivity analysis: if primary result is borderline, test 10x10 and 30x30 grids.

### 12.3 Sparse Bin Counts
With ~125 samples per action and 400 bins, expected ~0.3 counts per bin per action. Many bins will be empty. **Mitigation**: Laplace smoothing (epsilon=1e-10) prevents log(0) in KL computation. Empty bins contribute near-zero KL. JS divergence is well-defined for sparse histograms.

### 12.4 Synthetic-to-Real Gap
Same DGP as parent experiments. Findings are limited to controlled synthetic transitions. **Mitigation**: this is a controlled methodological comparison. If PCA cannot detect known structure in synthetic data, it cannot be trusted on real data.

### 12.5 PCA Fitting on Lambda=1 Data
PCA is fitted on lambda=1 data (maximum signal), which may overfit to the lambda=1 structure. At lower lambda levels, the signal is weaker and the PCA projection may not be optimal. **Mitigation**: PCA captures population-level variance structure, not lambda-specific artifacts. Lambda=1 provides the clearest signal for fitting; projection is applied to all lambda levels consistently.

### 12.6 Non-Stationarity Across Lambda
Different lambda levels produce different distributions of S_next. PCA fitted on lambda=1 may not be optimal for lambda=0.1. **Mitigation**: this is by design — we test whether the lambda=1 structure (where signal is strongest) generalizes across lambda levels. If PCA projection from lambda=1 data fails at low lambda, the detection is not robust.

## 13. Decision Rules

### 13.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Scaling-type Spearman rho >= 0.65 with p < 0.025 one-sided (Bonferroni x2)
2. Rotation-type Spearman rho >= 0.65 with p < 0.025 one-sided (Bonferroni x2)
3. Positive control passes: binned JS >= 0.01 at lambda=1 across all functions
4. Null control passes: per-function permutation p > 0.05 at lambda=0 (Fisher combined)
5. No significant function x lambda interaction (ANOVA p > 0.05)
6. Translation-type Spearman rho >= 0.65
7. JS CV across replications < 0.5 at lambda=1 for all functions
8. No pipeline errors

### 13.2 FALSIFIED-IN-SETTING
If ANY of:
1. Scaling rho < 0.65 or p > 0.025
2. Rotation rho < 0.65 or p > 0.025
3. Positive control fails
4. Null control fails
5. Significant function x lambda interaction (p < 0.05)
6. Translation rho drops below 0.65

### 13.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. PCA explained variance ratio < 50% for top 2 components
3. Binned JS computation produces NaN or Inf values
4. PCA projection matrix is degenerate (condition number = Inf)

## 14. Expected Outcomes

### 14.1 PCA Rescues Both Scaling and Rotation (SURVIVES_CURRENT_TEST)
- Per-function heterogeneity was a curse-of-dimensionality artefact
- Dimensionality reduction is the key to detecting action-dependent structure in high-dimensional state spaces
- Frontier lane should adopt PCA-projected divergence as primary detection mechanism
- C-WEB-DYNAMICS claim ceiling expands from translation-only to include scaling and rotation
- Product consequence: SPIDER's detection pipeline should include PCA projection step
- Next experiment: test on real Web transition data

### 14.2 PCA Rescues Scaling but Not Rotation (FALSIFIED-IN-SETTING)
- Scaling failure was partially dimensionality-related (PCA helps)
- Rotation failure is information-theoretic or requires different projection (nonlinear)
- C-WEB-DYNAMICS claim ceiling: translation + scaling, not rotation
- Frontier lane: try nonlinear projection (autoencoder) for rotation, or accept rotation limit

### 14.3 PCA Rescues Rotation but Not Scaling (FALSIFIED-IN-SETTING)
- Rotation failure was dimensionality-related (PCA helps)
- Scaling failure is information-theoretic (multiplicative modulation invisible in any projection)
- C-WEB-DYNAMICS claim ceiling: translation + rotation, not scaling
- Frontier lane: accept scaling limit, pivot to real Web data

### 14.4 PCA Fails on Both Scaling and Rotation (FALSIFIED-IN-SETTING)
- Information-theoretic limit firmly established across all tested estimation principles
- No tested method (kNN, KDE, PCA+binned) can detect scaling or rotation in this DGP
- C-WEB-DYNAMICS claim ceiling bounded to translation-like dynamics only
- Frontier lane MUST pivot to real Web transition data
- Synthetic DGP study is complete — no further synthetic experiments needed

### 14.5 Measurement Invalid (MEASUREMENT_INVALID)
- PCA or binned JS pipeline has implementation issues
- Not scientific evidence for or against
- Debug and retry

## 15. Analysis Plan

1. **Data Generation**: Generate 120,000 transitions (8 levels x 3 functions x 10 reps x 500)
2. **PCA Fitting**: Fit PCA on lambda=1 pooled data, extract top 2 components
3. **PCA Health Check**: Verify explained variance >= 50%, condition number finite
4. **Projection**: Project all transitions to 2D, min-max scale to [0,1]^2
5. **Histogram Construction**: 20x20 bins per action per cell, Laplace smoothing
6. **JS Divergence**: Pairwise JS across 6 action pairs, take max
7. **Variance Estimation**: 5 JS computations per cell with jittered bins
8. **Permutation Null**: Shuffle actions, recompute JS (100 perms per cell)
9. **Bias Correction**: Subtract perm null mean from raw JS
10. **Primary Test**: Per-function Spearman rho for scaling and rotation (n=8, Bonferroni x2)
11. **Translation Test**: Per-function Spearman rho for translation (single comparison)
12. **Aggregate Test**: Aggregate Spearman rho (single comparison)
13. **Permutation Tests**: Per-function at lambda=0 (Fisher combined) and lambda=1
14. **Two-Way ANOVA**: JS ~ lambda + function + lambda:function (240 obs)
15. **Controls**: Verify all 6 controls pass
16. **Comparison**: PCA binned JS vs parent kNN TV and KDE (qualitative)
17. **Reporting**: All outcomes with equal prominence

## 16. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations, random generation, and SVD (PCA)
- `scipy.stats` for Spearman correlation
- `scipy.stats` for two-way ANOVA (or manual implementation)
- Standard library only (no sklearn required for PCA — numpy SVD suffices)

Code will be committed to `research/frontier/pca_binned_divergence/` before execution.

## 17. Pre-registered Expectations

From prior work and theoretical reasoning:
- PCA should capture the principal variance directions where scaling and rotation manifest
- Translation should be preserved (translation offsets are along principal axes)
- Binned histogram JS in 2D should be stable with ~125 samples per action
- PCA explained variance should be > 70% for top 2 components (10D DGP with structured functions)
- If PCA rescues both: dimensionality was the binding constraint
- If PCA fails: information-theoretic limit, pivot to real Web data
- Bandwidth-free binned JS should avoid the over-smoothing issue that plagued KDE

## 18. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 19. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
