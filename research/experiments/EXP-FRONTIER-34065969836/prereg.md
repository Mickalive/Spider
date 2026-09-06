# EXP-FRONTIER-34065969836 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34065969836
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-06
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-FRONTIER-34061241004 (SURVIVES_CURRENT_TEST)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does TV distance detect action-dependent dynamical structure in higher-dimensional (10D) continuous state spaces with non-Gaussian heteroscedastic noise, or does the 2D result fail to generalize when state dimensionality and noise distribution complexity increase toward Web-realistic conditions?

## 3. Motivation

### What the parent experiment established (EXP-FRONTIER-34061241004)

The parent experiment tested TV distance on continuous2D affine DGP with heteroscedastic Gaussian noise. It established:

**Established:**
- TV distance scales monotonically with lambda: aggregate Spearman rho=1.0 (p<0.001)
- TV at lambda=0: 0.281, lambda=1: 0.849 (0.58 above finite-sample floor)
- Cohen's d=20.30 aggregate (17.81-21.95 per-function)
- All 6 frozen decision conditions pass
- Function invariance confirmed: ANOVA interaction p=0.862
- Positive control TV>=0.1 at lambda=1 (0.843-0.856)
- Null control permutation p=0.456 at lambda=0

**Rejected (methodological):**
- Positive control threshold >=0.1 is below empirical noise floor (~0.27), non-discriminating
- Finite-sample TV bias ~0.27 from 20x20 binning with ~125 samples/action not subtracted
- WF vs UM comparison uses mismatched estimators (empirical binned vs analytical) with n=3
- State clipping to [0,1] unquantified

**Unknown:**
- Whether TV generalizes to higher dimensions (>2D)
- Whether TV works with non-Gaussian noise
- Whether TV works on real Web transitions (synthetic-to-real gap)
- Whether bias-corrected TV preserves monotonicity
- Whether multi-resolution binning (10x10, 20x20, 30x30) affects results

**Do Not Assume:**
- 2D result generalizes to higher dimensions
- 'Web-faithful' label means Web-realistic
- Product deployment readiness
- TV works on real Web transitions
- Bias correction preserves monotonicity

### Why this experiment is different

The parent experiment validated TV on **2D continuous state with Gaussian heteroscedastic noise**. This experiment tests two critical generalization dimensions simultaneously:

1. **Dimensionality**: 10D vs 2D — tests whether TV detection survives the curse of dimensionality in state space
2. **Noise distribution**: Non-Gaussian (mixture of 3 Gaussians) vs Gaussian — tests whether TV is sensitive to noise distribution shape

**Key advantages over parent:**
- Directly addresses the "environment expressiveness" limitation (V11)
- Uses bias-corrected TV estimation (addresses V6 binning bias)
- Includes multi-resolution binning sensitivity analysis (addresses V6 required_fixes)
- Tests Gaussian vs non-Gaussian noise isolation (new comparison)
- Same lambda-ramping design enables direct quantitative comparison with parent

**Why not real Web data?**
The parent handoff recommends testing on real Web transition data (recorded agent sessions with DOM state tracking) as the minimum substrate. However, no such data exists in the repository. The parent's alternative is: "test on higher-dimensional synthetic DGPs (>2D, 10-50D) with non-Gaussian noise to stress-test generalization before claiming Web-readiness." This experiment follows that alternative path.

## 4. Hypotheses

### H1: Monotonic Scaling
TV distance between action-conditional next-state distributions increases monotonically with lambda in 10D non-Gaussian DGP. Aggregate Spearman rho(bias_corrected_tv, lambda) >= 0.65 with p < 0.05 one-sided.

### H2: Positive Control
At lambda=1 (fully action-determined), bias-corrected TV >= 0.05 across all 3 deterministic function families. This verifies the pipeline can detect action-dependent structure in 10D non-Gaussian state spaces.

### H3: Null Control
At lambda=0 (pure non-Gaussian noise), bias-corrected TV is indistinguishable from zero (permutation test p > 0.05). This verifies the pipeline does not detect structure when absent.

### H4: Function Invariance
The monotonicity finding is consistent across 3 independent deterministic function families (no significant function x lambda interaction in two-way ANOVA, p > 0.05).

### H5: Multi-Resolution Robustness
Monotonicity holds across at least 2 of 3 bin resolutions (10x10, 20x20, 30x30 grids projected to 2D via PCA). This verifies the finding is not an artefact of specific binning.

### H6: Bias Correction Preservation
Bias-corrected TV preserves monotonicity (Spearman rho >= 0.65) — the finite-sample bias subtraction does not destroy the signal.

## 5. Data Generation

### 5.1 Synthetic Transition Model

Generate transitions (S_t, A_t, S_{t+1}) where:
- State space: S = [0,1]^10 (10-dimensional continuous unit hypercube)
- Action space: A = {click, fill, submit, navigate} (4 action types)
- Transition function: S_{t+1} = f(S_t, A_t, lambda, noise)

For each transition:
1. Draw current state S_t uniformly from [0,1]^10
2. Draw action A_t uniformly from A
3. With probability lambda: S_{t+1} = deterministic_function(S_t, A_t) + epsilon
4. With probability (1-lambda): S_{t+1} = noise (mixture of Gaussians centered at 0.5)

where epsilon ~ MixtureOfGaussians(state-dependent parameters)

### 5.2 Deterministic Functions

Three independent frozen deterministic function families generalized to 10D:

**(A) Rotation (seed=42):** Apply state-dependent rotation matrix R(S_t) to S_t under action A_t. Rotation angle depends on state and action: theta = 0.1 * S_t[action_index] * action_sign. R is a 10x10 rotation matrix parameterized by theta.

**(B) Scaling (seed=43):** Apply state-dependent scaling matrix D(S_t) to S_t under action A_t. Scale factor depends on state and action: scale = 1.0 + 0.2 * S_t[action_index] * action_sign. D is a diagonal matrix with scale factors.

**(C) Translation (seed=44):** Apply state-dependent translation t(S_t) to S_t under action A_t. Translation vector depends on state and action: t_i = 0.1 * S_t[i] * action_sign(action, i). Includes sin modulation: t_i += 0.05 * sin(2*pi*S_t[i]).

Each function family uses a different action mapping (which dimension of S_t determines the transformation parameters) to ensure functional diversity.

### 5.3 Non-Gaussian Noise Model

Heteroscedastic mixture of 3 Gaussians:
- For each dimension i of the next-state:
  - sigma_base_i = 0.05 * (1 + 0.5 * ||S_t - center||_2) (state-dependent scale)
  - Component weights: [0.5, 0.3, 0.2] (fixed across states)
  - Component means: [0, +0.1*sigma_base_i, -0.1*sigma_base_i] (relative to deterministic target)
  - Component stds: [sigma_base_i, 0.5*sigma_base_i, 2.0*sigma_base_i]
- Sample from mixture: pick component according to weights, then sample Gaussian
- Clip resulting state to [0,1]^10 (same as parent; clipping artefact quantified separately)

This creates non-Gaussian noise with:
- Heavy tails (third component has 2x std)
- Skewness (asymmetric component means)
- State-dependent heteroscedasticity (sigma_base varies with state)

### 5.4 Lambda Levels

Eight conditions (same as parent):
- **lambda=0.0**: Pure non-Gaussian noise, no action-dependence (null control)
- **lambda=0.1**: Very low action-dependence
- **lambda=0.2**: Low action-dependence
- **lambda=0.3**: Low-moderate action-dependence
- **lambda=0.4**: Moderate action-dependence
- **lambda=0.5**: Mixed regime, half noise half signal
- **lambda=0.7**: High action-dependence
- **lambda=1.0**: Pure signal, full action-dependence (positive control)

### 5.5 Sample Size

- 500 transitions per lambda level per function per replication (8 levels x 3 functions x 10 replications x 500 = 120,000 total transitions)
- No train/test split: all transitions used for TV computation
- Each replication uses a distinct frozen seed (seed = func_seed * 10000 + rep_idx * 100 + 42)

## 6. TV Distance Computation

### 6.1 State Projection

10D state space projected to 2D via PCA for TV computation:
- Fit PCA on all transitions for a given lambda/function/replication
- Project to first 2 principal components (explaining maximum variance)
- Compute TV on projected 2D distributions

This enables direct comparison with parent's 2D TV while testing high-dimensional state.

### 6.2 Multi-Resolution Binning

TV computed on three grid resolutions:
- **10x10 grid** (100 bins): coarse resolution, less bias, more variance
- **20x20 grid** (400 bins): medium resolution, matches parent
- **30x30 grid** (900 bins): fine resolution, more bias, less variance

For each resolution:
1. Bin projected 2D state into grid cells
2. Compute empirical action-conditional distributions P(S_{t+1}|do(A_t=a)) via bin counts
3. Compute TV_max = max_{a,a'} TV(P_a, P_{a'}) where TV is sum of absolute differences / 2

### 6.3 Bias Correction

Finite-sample bias correction via permutation-null subtraction:
1. Compute TV_max on original data (includes finite-sample bias)
2. Compute TV_max on permutation-null data (action labels shuffled, 1000 permutations)
3. Bias_corrected_TV = max(0, TV_max - mean(perm_TV_max))

This subtracts the upward bias from finite-sample sparsity (~0.27 in parent's 20x20 setting).

### 6.4 Primary Statistic

Spearman rank correlation between bias_corrected_TV_max and lambda across the 8 levels, averaged across functions (aggregate test, n=8, single comparison).

## 7. Measures

### 7.1 Primary Metric
- **bias_corrected_tv_by_lambda**: Average bias-corrected TV_max at each lambda level, averaged across 3 functions x 10 replications
- **spearman_rho_aggregate**: Spearman correlation between bias_corrected_tv_by_lambda and lambda (n=8, single aggregate comparison)

### 7.2 Secondary Metrics
- Per-function bias-corrected TV at each lambda level
- Per-replication bias-corrected TV at each lambda level (variance across replications)
- Raw TV_max (before bias correction) at each lambda level
- Permutation null TV_max distribution at each lambda level
- Monte Carlo standard error of TV estimates
- Cohen's d of bias-corrected TV at lambda=1 vs lambda=0
- Fraction of transitions clipped per lambda/function
- PCA variance explained by first 2 components

### 7.3 Multi-Resolution Metrics
- Bias-corrected TV at 10x10, 20x20, 30x30 resolutions
- Monotonicity preservation across resolutions
- Resolution sensitivity (difference in TV between resolutions)

### 7.4 Comparison Metrics
- Raw TV from parent experiment EXP-FRONTIER-34061241004 at matched lambda levels
- Gaussian vs non-Gaussian noise comparison (10D Gaussian baseline computed in same experiment)

## 8. Null Models

### 8.1 Permutation Null
For each replication at each lambda level, shuffle action labels across transitions and recompute TV. The shuffled TV distribution provides the null for bias correction and for testing whether observed TV is significantly > 0.

### 8.2 Frequency Baseline
Under no action-dependence (lambda=0), the expected bias-corrected TV is 0. The permutation null at lambda=0 should yield bias-corrected TV consistent with zero.

### 8.3 Gaussian Noise Baseline
Same 10D DGP but with single Gaussian noise (not mixture). Computed in parallel to isolate whether non-Gaussian noise specifically degrades TV detection.

## 9. Statistical Tests

### 9.1 Primary Test
- Spearman rank correlation: rho(bias_corrected_tv_by_lambda, lambda) across 8 lambda levels
- One-sided test: rho > 0
- **Aggregate test (single comparison, no Bonferroni correction needed)**: rho >= 0.65, p < 0.05 one-sided. For n=8, exact one-sided p(rho >= 0.619) = 0.025; rho >= 0.65 gives p < 0.05 one-sided.
- **Per-function tests (3 comparisons, Bonferroni corrected)**: rho >= 0.65 with p < 0.017 one-sided (alpha = 0.05/3 = 0.0167). These are secondary confirmation.

### 9.2 Permutation Tests
- At lambda=0: permutation test for bias-corrected TV > 0 (one-sided, 1000 permutations)
- At lambda=1: permutation test for bias-corrected TV > 0.05 (one-sided, 1000 permutations)

### 9.3 Two-Way ANOVA
- bias_corrected_tv ~ lambda + function + lambda:function
- Non-significant interaction term (p > 0.05) supports function invariance
- With 8 levels x 3 functions x 10 replications = 240 observations, adequate residual df for interaction estimation

### 9.4 Multi-Resolution Consistency
- For each resolution (10x10, 20x20, 30x30): compute Spearman rho
- Report which resolutions show monotonicity
- Require at least 2 of 3 to show monotonicity for decision rule

### 9.5 Effect Size
- Cohen's d for bias-corrected TV at lambda=1 vs lambda=0

## 10. Controls

### 10.1 Positive Control (lambda=1)
- Bias-corrected TV >= 0.05 across all 3 functions
- This verifies: deterministic functions produce detectable TV structure in 10D non-Gaussian setting

### 10.2 Null Control (lambda=0)
- Bias-corrected TV not significantly > 0 (permutation p > 0.05)
- This verifies: pipeline does not detect structure when absent

### 10.3 Permutation Null Control
- Shuffled action labels yield bias-corrected TV near zero at all lambda levels
- This verifies: observed TV is driven by action-dependence, not sampling artifacts

### 10.4 Function Invariance Control
- Two-way ANOVA interaction p > 0.05
- With 240 observations, residual df adequate for interaction estimation

### 10.5 Multi-Resolution Control
- Monotonicity holds across at least 2 of 3 bin resolutions
- This verifies: finding is not artefact of specific binning

### 10.6 Gaussian vs Non-Gaussian Control
- Compare TV at lambda=1 in 10D Gaussian vs 10D non-Gaussian
- Non-Gaussian should not be significantly lower (one-sided test p > 0.05)
- This isolates whether non-Gaussian noise specifically degrades TV

## 11. Validity Threats

### 11.1 Curse of Dimensionality
10D state space may produce sparse binning even with PCA projection to 2D. **Mitigation**: PCA projection reduces effective dimensionality; multi-resolution binning tests sensitivity; bias correction accounts for sparsity.

### 11.2 PCA Information Loss
Projection to 2D may lose action-dependent structure. **Mitigation**: PCA maximizes variance projection; if action-dependent structure is in low-variance directions, TV will miss it — this is a genuine limitation disclosed in validity_notes.

### 11.3 Non-Gaussian Noise Complexity
Mixture of 3 Gaussians may be too simple or too complex. **Mitigation**: compare with Gaussian baseline in same experiment; report sensitivity to noise parameters.

### 11.4 Clipping Artefact
Clipping to [0,1]^10 after noise addition truncates tails. **Mitigation**: report fraction clipped per lambda/function; compare with toroidal wrapping if clipping fraction > 10%.

### 11.5 Deterministic Function Choice
Only 3 permutation-based functions tested. **Mitigation**: require consistent results across all 3; significant function x lambda interaction invalidates finding.

### 11.6 Multiple Comparisons
Aggregate test is single comparison (no correction needed). Per-function tests use Bonferroni x3. **Mitigation**: primary test is aggregate; per-function tests are secondary.

### 11.7 Comparison with Parent Experiment
Different dimensionality (10D vs 2D) and noise distribution (non-Gaussian vs Gaussian). Results not directly comparable. **Mitigation**: qualitative comparison only; the two experiments test generalization, not replication.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Aggregate Spearman rho(bias_corrected_tv_by_lambda, lambda) >= 0.65, p < 0.05 one-sided
2. Positive control passes: bias-corrected TV >= 0.05 at lambda=1 across all functions
3. Null control passes: bias-corrected TV not significantly > 0 at lambda=0 (permutation p > 0.05)
4. No significant function x lambda interaction (two-way ANOVA p > 0.05)
5. Monotonicity holds across at least 2 of 3 bin resolutions
6. No pipeline errors

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. Aggregate Spearman rho < 0.65 or p > 0.05 after bias correction
2. Positive control fails (bias-corrected TV < 0.05 at lambda=1 in any function)
3. Null control fails (bias-corrected TV significantly > 0 at lambda=0)
4. Significant function x lambda interaction (p < 0.05)
5. Monotonicity fails at all 3 bin resolutions

### 12.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. Deterministic functions generate degenerate transitions
3. Bias correction produces negative TV values at lambda=1 (indicates bias > signal)
4. PCA fails to capture meaningful variance (< 50% explained by first 2 components)

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates TV generalizes beyond 2D Gaussian to 10D non-Gaussian settings
- Substantially expands claim ceiling for C-WEB-DYNAMICS
- Justifies designing TV-based regime detection for high-dimensional Web state spaces
- Product lane can begin integrating TV into exploration strategy
- Opens path to testing on real Web data with calibrated confidence

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- Demonstrates TV does NOT generalize beyond 2D Gaussian settings
- 2D result is isolated to low-dimensional Gaussian noise
- Frontier lane must either (A) pivot to real Web data, (B) develop different metrics, or (C) accept TV limitation
- C-WEB-DYNAMICS remains HYPOTHESIS; TV detection constrained to 2D Gaussian DGPs

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Data Generation**: Generate 120,000 transitions at 8 lambda levels x 3 functions x 10 reps (seed=42 for base)
2. **PCA Projection**: Fit PCA on all transitions per lambda/function/replication, project to 2D
3. **Multi-Resolution Binning**: Compute TV on 10x10, 20x20, 30x30 grids
4. **Bias Correction**: Compute permutation-null TV, subtract from raw TV
5. **Statistical Tests**: Spearman correlation, permutation tests, two-way ANOVA
6. **Controls**: Verify positive, null, function invariance, multi-resolution, Gaussian vs non-Gaussian controls
7. **Robustness**: Report confidence intervals, effect sizes, clipping fractions, PCA variance explained
8. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for Spearman correlation and t-tests
- `scipy.stats.f_oneway` or `statsmodels` for two-way ANOVA
- `sklearn.decomposition.PCA` for dimensionality reduction
- Standard library only (no custom estimators required)

Code will be committed to `research/frontier/highdim_nongaussian_tv/` before execution.

## 16. Pre-registered Expectations

From prior experiments:
- Parent (EXP-FRONTIER-34061241004): TV monotonic in 2D Gaussian, rho=1.0, d=20.3
- If TV generalizes to 10D non-Gaussian: expect rho >= 0.65, d > 1.0 (smaller than 2D due to dimensionality)
- If TV does NOT generalize: expect rho < 0.65 or monotonicity failure at multiple resolutions
- Non-Gaussian noise may reduce separability compared to Gaussian (heavier tails, skewness)
- PCA projection to 2D may lose information (if action-dependent structure is in low-variance directions)

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
