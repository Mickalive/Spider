# EXP-FRONTIER-33932275169 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-33932275169
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-05
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-FRONTIER-33863640568 (FALSIFIED-IN-SETTING)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does TV distance or variance-of-means detect lambda-scaling of dynamical structure in non-affine (quadratic) synthetic Web transitions, or is the validated metric class limited to affine functions?

## 3. Motivation

### What the parent experiment established (EXP-FRONTIER-33863640568)

The parent experiment tested whether causal heterogeneity metrics detect lambda-scaling in affine deterministic functions f(s,a) = (c_a * s + b_a) mod 10. It produced:

**Established:**
- Causal heterogeneity metric Var_a(E_S[do(A=a)]) works for affine functions: aggregate Spearman rho=0.9762, p~1.6e-05, Cohen d=1.54
- TV distance is more sensitive: rho=1.0, d=13.4, strictly >= het at every lambda level
- Permutation functions are degenerate (Var_a=0 identically) — specific to function class, not metric
- Null control passes (no false positives)

**Rejected:**
- Permutation functions as test class for causal heterogeneity
- Uniform positive control thresholds for heterogeneous function classes
- Zero-interaction ANOVA expectation when functions have intentionally different Var_a

**Unknown:**
- Whether real Web transitions exhibit mean-varying structure suitable for this metric
- Whether TV distance or JSD should be the primary metric
- Whether the metric generalizes beyond affine functions
- How synthetic results translate to real Web transitions

**Do Not Assume:**
- C-WEB-DYNAMICS is established or falsified
- Metric generalizes beyond affine functions
- FALSIFIED-IN-SETTING reflects metric insensitivity (it reflects mis-calibrated controls)
- Synthetic-to-real translation applies
- ANOVA interaction failure is evidence against the metric
- TV saturation at lambda=1 indicates insensitivity

### Why this experiment is different

The parent experiment validated the metric for **affine functions** only. The critical open question is whether the metric generalizes to non-affine function classes. This experiment tests **quadratic functions** f(s,a) = (c_a * s^2 + b_a * s + d_a) mod 10, which are:
- Non-affine (quadratic in s, not linear)
- Non-permutation (generally non-injective, multiple inputs map to same output)
- More Web-like (real Web transitions are not affine maps)

If TV distance scales with lambda for quadratic functions, the metric generalizes and can be used broadly. If it fails, the metric is specific to affine functions and the lane should pivot.

### Inherited carry_forward from parent handoff

**Established:**
- Causal heterogeneity metric works for affine functions (rho=0.9762)
- TV distance is more sensitive than variance-of-means (d=13.4 vs 1.54)
- Null control passes
- Control failures were design issues, not metric failures

**Rejected:**
- Permutation functions as test class
- Uniform positive control thresholds
- Zero-interaction ANOVA expectation

**Unknown:**
- Whether metric generalizes beyond affine functions
- Whether TV or JSD should be primary metric
- Synthetic-to-real translation

**Do Not Assume:**
- C-WEB-DYNAMICS is established or falsified
- Metric generalizes beyond affine functions
- Synthetic-to-real translation

## 4. Hypotheses

### H1: TV Monotonic Scaling
TV distance between action-conditional next-state distributions increases monotonically with lambda. Aggregate Spearman rho(TV, lambda) >= 0.65.

### H2: Variance-of-Means Scaling
Variance-of-means metric Var_a(E_S[do(A=a)]) increases monotonically with lambda. Spearman rho(het, lambda) >= 0.5.

### H3: Positive Control
At lambda=1, TV distance > function-specific analytical thresholds across all 3 quadratic functions.

### H4: Null Control
At lambda=0, TV distance is indistinguishable from zero (permutation test mean p > 0.05).

### H5: Function Invariance
No significant function x lambda interaction for TV distance (two-way ANOVA p > 0.05).

## 5. Data Generation

### 5.1 Synthetic Transition Model

Generate transitions (S_t, A_t, S_{t+1}) where:
- State space: S = {0, 1, ..., 9} (10 discrete states)
- Action space: A = {click, fill, submit, navigate} (4 action types)
- Transition function: S_{t+1} = f(S_t, A_t, lambda, noise)

For each transition:
1. Draw current state S_t uniformly from S
2. Draw action A_t uniformly from A
3. With probability lambda: S_{t+1} = deterministic_function(S_t, A_t)
4. With probability (1-lambda): S_{t+1} = random from S (uniform)

### 5.2 Quadratic Deterministic Functions

Three independent quadratic functions f(s,a) = (c_a * s^2 + b_a * s + d_a) mod 10 with different coefficient sets:

**Function 1 (seed=42):**
- click: c=1, b=0, d=0 → f(s) = s^2 mod 10
- fill: c=3, b=1, d=2 → f(s) = (3s^2 + s + 2) mod 10
- submit: c=2, b=4, d=1 → f(s) = (2s^2 + 4s + 1) mod 10
- navigate: c=1, b=2, d=5 → f(s) = (s^2 + 2s + 5) mod 10

**Function 2 (seed=43):**
- click: c=2, b=1, d=0 → f(s) = (2s^2 + s) mod 10
- fill: c=1, b=3, d=4 → f(s) = (s^2 + 3s + 4) mod 10
- submit: c=3, b=0, d=2 → f(s) = (3s^2 + 2) mod 10
- navigate: c=2, b=2, d=1 → f(s) = (2s^2 + 2s + 1) mod 10

**Function 3 (seed=44):**
- click: c=1, b=4, d=3 → f(s) = (s^2 + 4s + 3) mod 10
- fill: c=2, b=1, d=0 → f(s) = (2s^2 + s) mod 10
- submit: c=1, b=0, d=7 → f(s) = (s^2 + 7) mod 10
- navigate: c=3, b=2, d=1 → f(s) = (3s^2 + 2s + 1) mod 10

**Properties:**
- All functions are non-affine (quadratic in s)
- All functions are non-permutation (generally non-injective)
- Each has analytically computable Var_a(E_S[f(S,a)]) > 0 (verified in analysis)

### 5.3 Lambda Levels

Six conditions (balanced resolution):
- **lambda=0.0**: Pure noise, no action-dependence (null control)
- **lambda=0.2**: Low action-dependence
- **lambda=0.4**: Moderate action-dependence
- **lambda=0.6**: Moderate-high action-dependence
- **lambda=0.8**: High action-dependence
- **lambda=1.0**: Pure signal, full action-dependence (positive control)

### 5.4 Sample Size

- 500 transitions per lambda level per function per replication (6 levels x 3 functions x 10 replications x 500 = 90,000 total transitions)
- No train/test split: all transitions used for interventional distribution computation
- Each replication uses a distinct frozen seed (seed = func_seed * 10000 + rep_idx * 100 + 42)

## 6. Causal Effect Metrics

### 6.1 TV Distance (PRIMARY)

For a given lambda level and function, compute TV distance between all pairs of action-conditional distributions:

TV(lambda) = (1/6) * sum_{a != a'} TV(P(S_{t+1}|do(A=a)), P(S_{t+1}|do(A=a')))

where TV(P, Q) = 0.5 * sum_s |P(s) - Q(s)| is the total variation distance.

At lambda=0: TV = 0 (all actions have identical uniform distributions).
At lambda=1: TV is maximal (each action has a distinct deterministic distribution).

### 6.2 Variance-of-Means (SECONDARY)

For a given lambda level and function:

het(lambda) = Var_a(E_S[do(A_t = a)])

where E_S[do(A=a)] = lambda * E_S[f(S,a)] + (1-lambda) * 4.5.

### 6.3 Analytical Values

For each quadratic function, compute:
- E_S[f(S,a)] analytically for each action a
- Var_a(E_S[f(S,a)]) analytically
- TV between action-conditional distributions analytically at lambda=1

These provide ground-truth values for positive control calibration.

## 7. Measures

### 7.1 Primary Metric
- **tv_by_lambda**: Average TV distance at each lambda level, averaged across 3 functions x 10 replications
- **spearman_rho_tv**: Spearman correlation between tv_by_lambda and lambda (n=6, single aggregate comparison)

### 7.2 Secondary Metrics
- **het_by_lambda**: Average variance-of-means at each lambda level
- **spearman_rho_het**: Spearman correlation between het_by_lambda and lambda
- Per-function TV and het at each lambda level
- Per-replication TV and het at each lambda level (variance across replications)
- Cohen's d of TV at lambda=1 vs lambda=0
- Frequency baseline P(S_{t+1}) marginal distribution at all lambda levels

### 7.3 Comparison Metrics
- TV distance vs variance-of-means at each lambda level (sensitivity comparison)
- Qualitative comparison with parent experiment's affine function results

## 8. Null Models

### 8.1 Permutation Null
For each replication at each lambda level, shuffle action labels across transitions and recompute TV and het. The shuffled distribution provides the null for testing whether observed metrics are significantly > 0.

### 8.2 Frequency Null
Under no action-dependence (lambda=0), the expected TV is 0. The permutation null at lambda=0 should yield TV consistent with sampling noise around 0.

## 9. Statistical Tests

### 9.1 Primary Test
- Spearman rank correlation: rho(tv_by_lambda, lambda) across 6 lambda levels
- One-sided test: rho > 0
- **Aggregate test (single comparison, no Bonferroni correction needed)**: rho >= 0.65, p < 0.05 one-sided. For n=6, exact one-sided p(rho >= 0.65) < 0.05.

### 9.2 Per-Function Tests
- Spearman correlation per function (n=6 each, Bonferroni x3 correction): rho >= 0.83, p < 0.0021 one-sided

### 9.3 Permutation Tests
- At lambda=0: permutation test for TV > 0 (one-sided, 1000 permutations)
- At lambda=1: permutation test for TV > threshold (one-sided, 1000 permutations)

### 9.4 Two-Way ANOVA
- TV ~ lambda + function + lambda:function
- Non-significant interaction term (p > 0.05) supports function invariance
- With 6 levels x 3 functions x 10 reps = 180 observations, adequate residual df

### 9.5 Effect Size
- Cohen's d for TV at lambda=1 vs lambda=0

## 10. Controls

### 10.1 Positive Control (lambda=1)
- TV > function-specific analytical thresholds across all 3 functions
- Thresholds based on analytical TV at lambda=1 computed from known quadratic coefficients
- This verifies: quadratic functions produce detectable distributional differences, pipeline correctly computes TV

### 10.2 Null Control (lambda=0)
- TV not significantly > 0 (permutation test mean p > 0.05)
- This verifies: pipeline does not detect structure when absent

### 10.3 Permutation Null Control
- Shuffled action labels yield TV near zero at all lambda levels
- This verifies: observed TV is driven by action-dependence, not sampling artifacts

### 10.4 Function Invariance Control
- TV should be similar across functions at each lambda level (after normalization by function-specific Var_a)
- Two-way ANOVA interaction p > 0.05

## 11. Validity Threats

### 11.1 Synthetic-to-Real Gap
Synthetic quadratic transitions may not reflect real Web dynamics. **Mitigation**: this is a controlled validation experiment. If the metric cannot detect known structure in non-affine synthetic data, it cannot be trusted on real data.

### 11.2 Quadratic Function Class
Only 3 quadratic functions tested. Other non-affine structures might show different behavior. **Mitigation**: require consistent results across all 3 functions; significant interaction invalidates the finding.

### 11.3 Monte Carlo Estimation Error
With ~125 transitions per action per cell, per-action TV estimates have sampling variability. **Mitigation**: 10 replications provide direct variance estimation; report confidence intervals.

### 11.4 Multiple Comparisons
Aggregate test is a single comparison (no correction needed). Per-function tests use Bonferroni x3.

### 11.5 TV Saturation
TV distance is bounded [0, 1] and may saturate at high lambda. **Mitigation**: 6 lambda levels provide good resolution; saturation at lambda=1 does not affect monotonicity detection.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Aggregate Spearman rho(tv_by_lambda, lambda) >= 0.65, p < 0.05 one-sided
2. Positive control passes: TV at lambda=1 > function-specific thresholds across all functions
3. Null control passes: TV not significantly > 0 at lambda=0 (permutation p > 0.05)
4. No significant function x lambda interaction for TV (two-way ANOVA p > 0.05)
5. Variance-of-means shows monotonic scaling (Spearman rho >= 0.5)
6. No pipeline errors

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. Aggregate Spearman rho < 0.65 or p > 0.05
2. Positive control fails
3. Null control fails
4. Significant function x lambda interaction for TV (p < 0.05)
5. Variance-of-means rho < 0.5

### 12.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. Degenerate functions (Var_a = 0 for all actions in any function)
3. TV CV across replications > 0.5

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates that TV distance generalizes beyond affine functions to non-affine (quadratic) Web-like transitions
- Validates TV distance as a robust metric for Web-dynamical regime detection
- The Frontier lane can proceed with TV as primary metric for future experiments
- Product lane can use TV-based regime detection in the SPIDER pipeline
- Variance-of-means also generalizes, providing a simpler secondary metric

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- Suggests that TV distance is specific to affine function classes
- The Frontier lane should pivot to prediction-accuracy approaches or new distributional metrics
- Does NOT falsify C-WEB-DYNAMICS — only this specific detection method's generality is constrained

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Data Generation**: Generate 90,000 transitions at 6 lambda levels x 3 functions x 10 replications x 500 transitions
2. **Analytical Computation**: Compute Var_a(E_S[f(S,a)]) and analytical TV for each function at lambda=1
3. **Interventional Distribution Computation**: For each replication-lambda-function cell, group transitions by action, compute empirical distribution P(S_{t+1}|do(A=a))
4. **TV Computation**: Compute pairwise TV between all action-conditional distributions, average
5. **Heterogeneity Computation**: Compute variance of 4 per-action means
6. **Primary Test**: Spearman correlation between average TV and lambda (n=6, single comparison)
7. **Per-Function Tests**: Spearman correlation per function (n=6 each, Bonferroni x3)
8. **Permutation Tests**: At lambda=0 and lambda=1, test TV against permutation null (1000 permutations)
9. **Two-Way ANOVA**: TV ~ lambda + function + lambda:function (180 observations)
10. **Controls**: Verify positive, null, permutation null, and function invariance controls
11. **Frequency Baseline**: Report P(S_{t+1}) marginal distribution at all lambda levels
12. **Robustness**: Report confidence intervals and effect sizes
13. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations, random generation, and variance computation
- `scipy.stats` for Spearman correlation
- `statsmodels` for two-way ANOVA
- `collections.Counter` for action-grouped counting
- Standard library only (no custom estimators required)

Code will be committed to `research/frontier/nonaffine_validation/` before execution.

## 16. Pre-registered Expectations

From prior work and theoretical derivation:
- For quadratic functions f(s,a) = (c_a * s^2 + b_a * s + d_a) mod 10, E_S[f(S,a)] varies across actions when coefficients differ
- TV(lambda) should scale monotonically with lambda (Spearman rho >= 0.65)
- Variance-of-means should also scale but may be less sensitive than TV
- The parent experiment's TV rho=1.0 on affine functions suggests the effect is strong; quadratic functions should produce comparable or smaller effects
- Function invariance is expected if functions are drawn from the same quadratic class

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
