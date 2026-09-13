# EXP-FRONTIER-34538185726 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34538185726
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-10
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-FRONTIER-34121473072 (FALSIFIED-IN-SETTING)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Can kernel density estimation (KDE) with cross-validated bandwidth detect scaling-type action-dependent structure that kNN TV misses in the same 10D non-Gaussian DGP — or does the scaling failure reflect a fundamental information-theoretic limit where multiplicative state modulation is indistinguishable from heteroscedastic noise at finite sample sizes?

## 3. Motivation

### What the parent experiments established

Two experiments have converged on the same conclusion: **kNN TV cannot detect scaling-type dynamics in 10D non-Gaussian spaces, regardless of bias correction.**

**EXP-FRONTIER-34065969836** (raw kNN TV):
- Translation: rho=1.0 (strong signal)
- Rotation: rho=0.83 (moderate)
- Scaling: rho=0.16 (negligible)
- Function invariance decisively fails (ANOVA p~0)

**EXP-FRONTIER-34121473072** (bias-corrected kNN TV):
- Translation: rho=1.0, bias-corrected bc_TV at lambda=1 = 0.189
- Rotation: rho=0.93, bc_TV at lambda=1 = 0.052
- Scaling: rho=-0.12 (p=0.61), bc_TV at lambda=1 = 0.020
- Bias correction removes the kNN floor (~0.528) but scaling rho remains -0.12
- Conclusion: scaling failure is genuine signal absence, not estimator artefact

**The key unresolved question is whether this is kNN-specific or information-theoretic.**

### Why KDE is materially different from kNN TV

kNN TV and KDE estimate density divergence through fundamentally different mathematical principles:

| Property | kNN TV | KDE |
|----------|--------|-----|
| Density estimation | Implicit (via neighbor counts) | Explicit (kernel smoothing) |
| Bandwidth/bandwidth-like | Fixed k (number of neighbors) | Adaptive h (kernel bandwidth) |
| Bias source | Finite-k bias floor (~0.528 in 10D) | Bandwidth-dependent smoothing bias |
| Sensitivity to variance modulation | Low (local neighbor ratios are scale-invariant) | Potentially higher (explicit density shape) |
| Curse of dimensionality | Distance concentration | Distance concentration |

The critical difference: **kNN's local neighbor ratio is inherently scale-invariant** — it compares whether a point's k-th neighbor in distribution A is closer than its k-th neighbor in distribution B. Scaling changes the spread of a distribution without necessarily changing local density ratios in the way kNN measures them. KDE, by contrast, estimates the full density shape and can potentially detect that scaling changes the variance structure of the conditional distribution.

### Hypothesis

If KDE can detect scaling structure that kNN misses, the scaling failure was kNN-specific (estimator artefact due to scale-invariant local ratios). If KDE also fails, the failure is an information-theoretic limit: multiplicative state modulation in 10D produces action-conditional distributions that are statistically indistinguishable from heteroscedastic noise at N=500 per cell.

### Why this is the minimum next experiment

The handoff from EXP-FRONTIER-34121473072 recommends testing alternative density divergence estimators (KDE, binned PCA, neural density estimation). KDE is the most direct test because:
1. It operates on the same mathematical object (density divergence) as kNN TV
2. It uses a fundamentally different estimation principle (kernel smoothing vs. neighbor counting)
3. It can be implemented with standard libraries (scipy/sklearn) without new infrastructure
4. It provides a clean binary answer: either KDE detects scaling or it doesn't

If KDE fails, the Frontier lane should accept the information-theoretic limit for synthetic data and pivot to real Web transition data (the other unknown in the parent handoff).

## 4. Hypotheses

### H1: KDE Detects Scaling
KDE-based JS divergence for scaling-type dynamics increases monotonically with lambda. Per-function Spearman rho >= 0.65 with p < 0.0167 one-sided (Bonferroni x3).

### H2: Positive Control
At lambda=1 (fully action-determined), KDE JS divergence >= 0.01 across all 3 functions.

### H3: Null Control
At lambda=0 (action-independent), KDE JS divergence is indistinguishable from zero (permutation test p > 0.05).

### H4: Function Invariance
KDE detection is consistent across 3 functions (no significant function x lambda interaction in two-way ANOVA, p > 0.05).

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
- Noise is state-dependent (heteroscedastic), which is the key challenge for scaling detection

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
- No train/test split: all transitions used for KDE fitting (permutation null uses same data with shuffled labels)

## 6. KDE Implementation

### 6.1 Density Estimation

For each cell (lambda, function, replication):
1. Group 500 transitions by action → ~125 transitions per action
2. For each action a, fit KDE on the 125 next-state vectors S_next ∈ R^10 using `scipy.stats.gaussian_kde`
3. KDE uses Gaussian kernel with bandwidth selected via 5-fold cross-validated log-likelihood
4. Bandwidth search: 20 log-spaced values in [0.01, 2.0]; scipy gaussian_kde accepts a bandwidth_factor parameter that scales the standard Scott's rule bandwidth

### 6.2 Jensen-Shannon Divergence

For each cell, compute pairwise JS divergence between all 6 action pairs:
- JS(P_a || P_b) = 0.5 * KL(P_a || M) + 0.5 * KL(P_b || M), where M = 0.5*(P_a + P_b)
- KL estimated via Monte Carlo: KL(P_a || M) ≈ (1/N) Σ log(p_a(x_i) / m(x_i)) for x_i ~ P_a
- N_KL = 125 samples per direction (sampled from each KDE)
- Primary metric: max JS across all 6 action pairs (most sensitive to any pair differing)
- Secondary: mean JS across all 6 pairs (most stable)

### 6.3 Bandwidth Selection

- `scipy.stats.gaussian_kde` uses Scott's rule by default: h = N^{-1/(d+4)} * std
- We apply a bandwidth_factor (scalar multiplier) to this default, searching over 20 log-spaced values in [0.01, 2.0]
- For each candidate factor, compute 5-fold cross-validated log-likelihood on the data
- Select the factor maximizing mean validation log-likelihood
- Same bandwidth_factor used for all 4 action-conditional KDEs within a cell

### 6.4 Bias Correction

Same approach as parent:
- For each cell, compute permutation-null JS divergence (shuffle action labels, recompute JS)
- N_PERMUTATIONS = 50 per cell (matching parent pragmatic choice)
- Bias-corrected JS = max(0, raw_JS - mean(perm_JS))
- The permutation null destroys action-dependence while preserving state-space structure

## 7. Measures

### 7.1 Primary Metric
- **kde_js_max_by_lambda**: Maximum pairwise JS divergence at each lambda level, averaged across 3 functions x 10 replications
- **spearman_rho_per_function**: Spearman correlation between kde_js_max and lambda for each function (n=8, Bonferroni x3 corrected)

### 7.2 Secondary Metrics
- Mean pairwise JS divergence (averaged across 6 action pairs) at each lambda level
- Per-replication JS divergence (variance across replications)
- Bandwidth selected by cross-validation at each cell
- Comparison with kNN TV bias-corrected divergence from parent (qualitative)
- Cohen's d of JS divergence at lambda=1 vs lambda=0
- Two-way ANOVA: JS ~ lambda + function + lambda:function

### 7.3 Comparison with Parent
- Direct comparison of KDE JS divergence vs kNN TV bc_divergence for scaling-type dynamics at each lambda level
- If KDE scaling rho >= 0.65 and kNN TV scaling rho = -0.12: KDE rescues scaling detection
- If KDE scaling rho < 0.65: both estimators fail, information-theoretic limit

## 8. Null Models

### 8.1 Permutation Null
For each cell, shuffle action labels across transitions and recompute KDE + JS divergence. The shuffled JS distribution provides the null for testing whether observed JS is significantly > 0.

### 8.2 Frequency Null
Under no action-dependence (lambda=0), all action-conditional densities are identical to the marginal P(S_next). Expected JS divergence = 0.

## 9. Statistical Tests

### 9.1 Primary Test (Per-Function)
- Spearman rho between kde_js_max and lambda for each function (n=8 levels)
- One-sided test: rho > 0
- Bonferroni corrected: p < 0.05/3 = 0.0167 per function
- Required rho threshold: >= 0.65 (for n=8, exact p(rho>=0.619) = 0.025 one-sided; rho>=0.65 gives p < 0.05)

### 9.2 Aggregate Test (Secondary)
- Spearman rho on aggregate kde_js_max (averaged across functions)
- Single comparison, no Bonferroni correction
- Threshold: rho >= 0.65, p < 0.05 one-sided

### 9.3 Permutation Tests
- At lambda=0: test JS > 0 (one-sided, 50 permutations per cell)
- At lambda=1: test JS > 0.01 (one-sided, 50 permutations per cell)

### 9.4 Two-Way ANOVA
- JS_divergence ~ lambda + function + lambda:function
- With 240 observations (8 x 3 x 10), adequate residual df for interaction estimation
- Non-significant interaction (p > 0.05) supports function invariance

### 9.5 Effect Size
- Cohen's d for JS divergence at lambda=1 vs lambda=0

## 10. Controls

### 10.1 Positive Control (lambda=1)
- KDE JS divergence >= 0.01 across all 3 functions
- Verifies: KDE pipeline correctly detects maximal action-dependent structure

### 10.2 Null Control (lambda=0)
- KDE JS divergence not significantly > 0 (permutation test p > 0.05)
- Verifies: KDE pipeline does not detect structure when absent

### 10.3 Permutation Null Control
- Shuffled action labels yield JS divergence near zero at all lambda levels
- Verifies: observed JS is driven by action-dependence, not sampling artifacts

### 10.4 Function Invariance Control
- Two-way ANOVA interaction p > 0.05
- With 240 observations, residual df = 240 - 8 - 3 - 14 = 215 (adequate)

## 11. Validity Threats

### 11.1 KDE Bandwidth Sensitivity
KDE performance in 10D depends critically on bandwidth selection. Too small h → high variance; too large h → over-smoothing. **Mitigation**: 5-fold cross-validation with 20-point log-space grid. Report selected bandwidths across cells.

### 11.2 Curse of Dimensionality in 10D
KDE convergence rate degrades as O(n^{-4/(4+d)}) in d dimensions. At d=10, convergence is slow. **Mitigation**: This is the same challenge kNN faces. If KDE also fails in 10D, the curse of dimensionality may be the binding constraint (information-theoretic limit). Report KDE bandwidth and effective sample size per action (~125).

### 11.3 Monte Carlo Estimation of JS Divergence
JS divergence estimated via Monte Carlo with 125 samples per direction. SE of KL estimate ~ O(1/sqrt(N)). **Mitigation**: 10 replications provide direct variance estimation; report confidence intervals.

### 11.4 Synthetic-to-Real Gap
Same DGP as parent experiments. Findings are limited to controlled synthetic transitions. **Mitigation**: this is a controlled methodological comparison. If KDE cannot detect known structure in synthetic data, it cannot be trusted on real data.

### 11.5 Computation Time
240 KDE fits with cross-validated bandwidth selection in 10D. **Mitigation**: estimated 30-60 minutes wall-clock; within acceptable bounds for a single experiment.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Per-function Spearman rho(KDE_JS, lambda) >= 0.65 with p < 0.0167 one-sided for ALL 3 functions (including scaling)
2. Positive control passes: KDE JS >= 0.01 at lambda=1 across all functions
3. Null control passes: permutation p > 0.05 at lambda=0
4. No significant function x lambda interaction (ANOVA p > 0.05)
5. No pipeline errors

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. Per-function Spearman rho < 0.65 or p > 0.0167 for ANY function
2. Positive control fails
3. Null control fails
4. Significant function x lambda interaction (p < 0.05)

### 12.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. KDE bandwidth selection fails (all cells select boundary bandwidth)
3. JS divergence CV across replications > 0.5 at lambda=1

## 13. Expected Outcomes

### 13.1 KDE Rescues Scaling (scaling rho >= 0.65)
- Scaling failure was kNN-specific (kNN's scale-invariant local ratios miss variance modulation)
- KDE is the preferred estimator for action-dependent structure in 10D
- kNN TV should be documented as having a known blind spot for scaling-type dynamics
- Frontier lane: apply KDE to real Web transition data

### 13.2 KDE Fails on Scaling, Detects Translation (scaling rho < 0.65, translation rho >= 0.65)
- Both kNN and KDE fail on scaling → information-theoretic limit in 10D
- Action-dependent structure exists only for translation-like dynamics
- C-WEB-DYNAMICS claim ceiling: limited to translation-like (location-shifting) dynamics
- Frontier lane: pivot to real Web data or orthogonal mechanisms (binned PCA, neural density)

### 13.3 KDE Fails on All Functions
- KDE is not suitable for 10D non-Gaussian DGP
- Possible causes: bandwidth sensitivity, curse of dimensionality, insufficient sample size
- MEASUREMENT_INVALID or FALSIFIED-IN-SETTING depending on controls
- Frontier lane: try binned PCA projection or neural density estimation

### 13.4 Information-Theoretic Limit Established
- If both kNN and KDE fail on scaling across multiple estimation principles
- Multiplicative state modulation in 10D is indistinguishable from heteroscedastic noise at N=500
- C-WEB-DYNAMICS claim ceiling bounded to translation-like dynamics only
- Frontier lane must use real Web data to test whether real-world dynamics are translation-like

## 14. Analysis Plan

1. **Data Generation**: Generate 120,000 transitions (8 levels x 3 functions x 10 reps x 500)
2. **KDE Fitting**: For each cell, fit 4 action-conditional KDEs with CV bandwidth
3. **JS Divergence**: Compute pairwise JS between all 6 action pairs, take max and mean
4. **Permutation Null**: Shuffle actions, recompute JS (50 perms per cell)
5. **Bias Correction**: Subtract perm null mean from raw JS
6. **Primary Test**: Per-function Spearman rho (n=8, Bonferroni x3)
7. **Aggregate Test**: Aggregate Spearman rho (single comparison)
8. **Permutation Tests**: At lambda=0 and lambda=1
9. **Two-Way ANOVA**: JS ~ lambda + function + lambda:function (240 obs)
10. **Controls**: Verify positive, null, permutation null, function invariance
11. **Comparison**: KDE JS vs kNN TV bc_divergence (qualitative)
12. **Reporting**: All outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for Spearman correlation
- `scipy.stats.gaussian_kde` for KDE fitting with bandwidth selection (no sklearn required)
- `statsmodels` for two-way ANOVA (or manual implementation with scipy)
- Standard library only

Code will be committed to `research/frontier/kde_divergence/` before execution.

## 16. Pre-registered Expectations

From prior work and theoretical reasoning:
- KDE should detect translation-type dynamics (strong signal, same as kNN TV)
- KDE should detect rotation-type dynamics (moderate signal, same as kNN TV)
- KDE may or may not detect scaling-type dynamics (the key question)
- If KDE detects scaling: kNN's scale-invariant local ratios were the bottleneck
- If KDE fails on scaling: information-theoretic limit, both estimators agree
- Bandwidth in 10D is expected to be moderate (0.1-1.0 range) due to curse of dimensionality
- JS divergence at lambda=1 should be substantial (0.01-0.1 range) for translation/rotation

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
