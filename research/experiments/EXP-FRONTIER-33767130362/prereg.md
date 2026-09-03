# EXP-FRONTIER-33767130362 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-33767130362
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-03
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-FRONTIER-33528827909 (MEASUREMENT_INVALID)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does the causal effect heterogeneity of actions across states increase monotonically with the action-dependence parameter lambda, demonstrating regime-dependent dynamics in synthetic Web-like state transitions via direct causal intervention rather than correlational prediction accuracy?

## 3. Motivation

### What the parent experiment established (EXP-FRONTIER-33528827909)

The parent experiment tested whether prediction accuracy advantage of action-conditioned rules over memory scales monotonically with lambda. It produced:

**Established (descriptive):**
- Monotonic increase of rule-memory accuracy difference with lambda: 0.053 at λ=0, 0.087 at λ=0.25, 0.307 at λ=0.5, 0.653 at λ=1.0
- Spearman rho=1.0 (perfect monotonic) across 4 lambda levels
- Positive control passes: rules 100% at λ=1; null control passes: p=0.094 at λ=0
- Lambda explains 96.7% of variance in rule-memory difference (ANOVA F=58.99)

**Rejected (measurement invalid):**
- Inferential claim of Bonferroni-corrected significance: exact permutation p=0.042 one-sided with n=4 lambda levels, after Bonferroni x12 p>=0.5. Primary monotonicity test CANNOT achieve significance with 4 levels.
- Function invariance failure: CV metric invalid at low means (CV inflated by small denominators), ANOVA interaction unestimable (saturated design, 0 residual df), function main effect p=0.97.
- Producer reported impossible p-values (p=0.0 for n=4).

**Unknown:**
- Does monotonicity survive with properly powered design?
- Can causal intervention reveal regime-dependent dynamics beyond correlational prediction?
- How do synthetic results translate to real Web transitions?

**Do Not Assume:**
- Monotonicity is inferentially proven (descriptive only)
- Function invariance failure is real (CV metric invalid)
- This experiment falsifies C-WEB-DYNAMICS
- Synthetic-to-real translation
- Small-sample low-lambda results are stable
- Null control is evidence of absence (power <20%)

### Why this experiment is different

The parent experiment used **prediction accuracy decomposition**: train a rule model, train a memory baseline, compare accuracy. This approach has three inherent limitations:

1. **Model training introduces sampling variance**: Rule accuracy depends on the train/test split, which introduces noise especially at low lambda where signal is weak.
2. **The comparison metric (rule - memory accuracy) conflates action information with state information**: Memory accuracy also varies with lambda (because P(S_{t+1}|S_t) is non-uniform even when action-independent), making the difference metric noisy.
3. **The Spearman test with n=4 lambda levels has minimal power**: exact permutation p=0.042 one-sided cannot survive Bonferroni correction.

This experiment uses **causal effect heterogeneity via direct interventional analysis**: instead of training models and comparing accuracy, we compute ground-truth interventional distributions P(S_{t+1} | do(A_t = a)) from the known data-generating process, then measure how much these distributions vary across actions.

**Key advantages:**
- No model training → no train/test split noise
- Ground-truth interventional distributions (computed analytically from the DGP) → no estimation error
- The heterogeneity metric directly measures what we care about: do different actions have different causal effects?
- 8 lambda levels (vs. 4) → substantially more power for Spearman test
- 10 replications per cell → proper variance estimation

## 4. Hypotheses

### H1: Monotonic Scaling
The causal effect heterogeneity (variance of expected next-states across actions) increases monotonically with lambda. Aggregate Spearman rho(heterogeneity, lambda) >= 0.65.

### H2: Positive Control
At lambda=1 (fully action-determined), heterogeneity >= 0.5 across all 3 deterministic functions.

### H3: Null Control
At lambda=0 (action-independent), heterogeneity is indistinguishable from zero (permutation test p > 0.05).

### H4: Function Invariance
The monotonicity finding is consistent across 3 independent deterministic functions (no significant function x lambda interaction in two-way ANOVA, p > 0.05).

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

### 5.2 Deterministic Functions

Three independent frozen lookup tables (seeds 42, 43, 44) that map (state, action) to a unique next state. Each function is a different permutation of the state space for each action. Same functions as parent experiment.

### 5.3 Lambda Levels

Eight conditions (higher resolution than parent's 4 levels):
- **lambda=0.0**: Pure noise, no action-dependence (null control)
- **lambda=0.1**: Very low action-dependence
- **lambda=0.2**: Low action-dependence
- **lambda=0.3**: Low-moderate action-dependence
- **lambda=0.4**: Moderate action-dependence
- **lambda=0.5**: Mixed regime, half noise half signal
- **lambda=0.7**: High action-dependence
- **lambda=1.0**: Pure signal, full action-dependence (positive control)

### 5.4 Sample Size

- 500 transitions per lambda level per function per replication (8 levels x 3 functions x 10 replications x 500 = 120,000 total transitions)
- No train/test split: all transitions used for interventional distribution computation
- Each replication uses a distinct frozen seed (seed = 42 + replication_index for base generation)

## 6. Causal Effect Heterogeneity Metric

### 6.1 Interventional Distribution

For a given lambda level and deterministic function, the interventional distribution under do(A_t = a) is:

P(S_{t+1} | do(A_t = a)) = lambda * delta_{f(S_t, a)} + (1-lambda) * Uniform(S)

where delta is the point mass at the deterministic next state and S_t ~ Uniform(S).

### 6.2 Expected Next-State Under Intervention

E[S_{t+1} | do(A_t = a)] = lambda * E_S[f(S, a)] + (1-lambda) * 4.5

where E_S[f(S, a)] is the average of f(s, a) over all states s.

### 6.3 Causal Effect Heterogeneity

For a given lambda level and function, the heterogeneity is:

het(lambda) = Var_a(E[S_{t+1} | do(A_t = a)])

where the variance is over the 4 actions {click, fill, submit, navigate}.

At lambda=0: het = 0 (all actions have E[S_{t+1}] = 4.5).
At lambda=1: het = Var_a(E_S[f(S, a)]) > 0 (each action maps to a distinct permutation).
At intermediate lambda: het scales proportionally with lambda^2 (since het = lambda^2 * Var_a(E_S[f(S,a)])).

### 6.4 Monte Carlo Estimation

For each replication, generate 500 transitions at a given lambda and function. Group by action (expect ~125 per action). Compute sample mean next-state for each action. Compute variance of the 4 sample means. This is the Monte Carlo estimate of het.

### 6.5 Primary Statistic

Spearman rank correlation between het(lambda) and lambda across the 8 levels, averaged across functions (aggregate test, n=8, single comparison).

## 7. Measures

### 7.1 Primary Metric
- **causal_het_by_lambda**: Average heterogeneity at each lambda level, averaged across 3 functions x 10 replications
- **spearman_rho_aggregate**: Spearman correlation between causal_het_by_lambda and lambda (n=8, single aggregate comparison)

### 7.2 Secondary Metrics
- Per-function heterogeneity at each lambda level
- Per-replication heterogeneity at each lambda level (variance across replications)
- Per-action expected next-states at each lambda level
- Monte Carlo standard error of heterogeneity estimates
- Cohen's d of heterogeneity at lambda=1 vs lambda=0

### 7.3 Comparison Metrics
- Prediction accuracy difference (rule - memory) from parent experiment at matching lambda levels (qualitative comparison only)

## 8. Null Models

### 8.1 Permutation Null
For each replication at each lambda level, shuffle action labels across transitions and recompute heterogeneity. The shuffled heterogeneity distribution provides the null distribution for testing whether observed heterogeneity is significantly > 0.

### 8.2 Frequency Null
Under no action-dependence (lambda=0), the expected heterogeneity is 0. The permutation null at lambda=0 should yield heterogeneity consistent with sampling noise around 0.

## 9. Statistical Tests

### 9.1 Primary Test
- Spearman rank correlation: rho(causal_het_by_lambda, lambda) across 8 lambda levels
- One-sided test: rho > 0
- **Aggregate test (single comparison, no Bonferroni correction needed)**: rho >= 0.65, p < 0.05 one-sided. For n=8, exact one-sided p(rho >= 0.619) = 0.025; rho >= 0.65 gives p < 0.05 one-sided.
- **Per-function tests (3 comparisons, Bonferroni corrected)**: rho >= 0.83, p < 0.0021 one-sided (alpha = 0.05/3 = 0.0167). These are secondary confirmation.

### 9.2 Permutation Tests
- At lambda=0: permutation test for heterogeneity > 0 (one-sided, 1000 permutations)
- At lambda=1: permutation test for heterogeneity > 0.5 (one-sided, 1000 permutations)

### 9.3 Two-Way ANOVA
- causal_het ~ lambda + function + lambda:function
- Non-significant interaction term (p > 0.05) supports function invariance
- With 8 levels x 3 functions x 10 replications = 240 observations, adequate residual df for interaction estimation (unlike parent's saturated design)

### 9.4 Effect Size
- Cohen's d for heterogeneity at lambda=1 vs lambda=0

## 10. Controls

### 10.1 Positive Control (lambda=1)
- Heterogeneity >= 0.5 across all 3 functions
- This verifies: deterministic functions produce detectable causal heterogeneity, pipeline correctly computes interventional distributions

### 10.2 Null Control (lambda=0)
- Heterogeneity not significantly > 0 (permutation test p > 0.05)
- This verifies: pipeline does not detect causal structure when absent

### 10.3 Permutation Null Control
- Shuffled action labels yield heterogeneity near zero at all lambda levels
- This verifies: observed heterogeneity is driven by action-dependence, not sampling artifacts

### 10.4 Function Invariance Control
- Heterogeneity should be similar across functions at each lambda level
- Two-way ANOVA interaction p > 0.05
- With 240 observations (8 x 3 x 10), residual df = 240 - 8 - 3 - 24 = 205 (adequate for interaction estimation)

## 11. Validity Threats

### 11.1 Synthetic-to-Real Gap
Synthetic transitions may not reflect real Web dynamics. **Mitigation**: this is a controlled validation experiment. If the causal heterogeneity metric cannot detect known structure in synthetic data, it cannot be trusted on real data.

### 11.2 Monte Carlo Estimation Error
With ~125 transitions per action per cell, per-action means have SE ~0.26. The variance of 4 means has sampling variability. **Mitigation**: 10 replications provide direct variance estimation; report confidence intervals.

### 11.3 Deterministic Function Choice
Only 3 permutation-based functions tested. Other deterministic structures might show different behavior. **Mitigation**: require consistent results across all 3 functions; significant function x lambda interaction invalidates the finding.

### 11.4 Multiple Comparisons
Aggregate test is a single comparison (no correction needed). Per-function tests use Bonferroni x3. **Mitigation**: primary test is aggregate; per-function tests are secondary.

### 11.5 Spearman Power with n=8
With n=8 lambda levels, the exact Spearman test has limited power for moderate rho values. **Mitigation**: rho=1.0 from parent experiment suggests the effect is strong; 8 levels give substantially more power than 4; report exact p-values.

### 11.6 Comparison with Parent Experiment
This experiment uses a different metric (causal heterogeneity vs. prediction accuracy) and different statistical tests. Results are not directly comparable. **Mitigation**: qualitative comparison only; the two experiments test the same underlying hypothesis (regime-dependent dynamics) via different detection methods.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Aggregate Spearman rho(causal_het_by_lambda, lambda) >= 0.65, p < 0.05 one-sided (single aggregate comparison, no Bonferroni correction)
2. Positive control passes: heterogeneity >= 0.5 at lambda=1 across all functions
3. Null control passes: heterogeneity not significantly > 0 at lambda=0 (permutation p > 0.05)
4. No significant function x lambda interaction (two-way ANOVA p > 0.05)
5. No pipeline errors

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. Aggregate Spearman rho < 0.65 or p > 0.05 one-sided
2. Positive control fails (heterogeneity < 0.5 at lambda=1 in any function)
3. Null control fails (heterogeneity significantly > 0 at lambda=0)
4. Significant function x lambda interaction (p < 0.05)

### 12.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. Deterministic functions generate degenerate transitions
3. Monte Carlo variance is excessive (heterogeneity CV across replications > 0.5)

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates that Web-like transitions have regime-dependent causal structure
- Validates causal effect heterogeneity as an alternative detection method to prediction accuracy
- The causal approach avoids the statistical pitfalls of the parent experiment (no model training, ground-truth interventional distributions, more lambda levels)
- Justifies stratified causal analysis of real Web data
- Physics lane should investigate action-type-stratified causal effects

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- Suggests that either (a) the causal heterogeneity metric is not sensitive to dynamical variation in this setting, or (b) the synthetic model does not produce detectable causal regime effects
- Does NOT falsify C-WEB-DYNAMICS entirely — only this specific causal detection method
- Physics lane should try other approaches (information-theoretic, multi-scale, geometric)

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Data Generation**: Generate 120,000 transitions at 8 lambda levels x 3 functions x 10 replications x 500 transitions
2. **Interventional Distribution Computation**: For each replication-lambda-function cell, group transitions by action, compute sample mean next-state per action
3. **Heterogeneity Computation**: Compute variance of 4 per-action means → heterogeneity estimate
4. **Primary Test**: Spearman correlation between average heterogeneity and lambda (n=8, single comparison, no correction)
5. **Per-Function Tests**: Spearman correlation per function (n=8 each, Bonferroni x3 corrected)
6. **Permutation Tests**: At lambda=0 and lambda=1, test heterogeneity against permutation null (1000 permutations)
7. **Two-Way ANOVA**: heterogeneity ~ lambda + function + lambda:function (240 observations)
8. **Controls**: Verify positive, null, permutation null, and function invariance controls
9. **Robustness**: Report confidence intervals and effect sizes
10. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations, random generation, and variance computation
- `scipy.stats` for Spearman correlation
- `scipy.stats.f_oneway` or `statsmodels` for two-way ANOVA
- `collections.Counter` for action-grouped counting
- Standard library only (no custom estimators required)

Code will be committed to `research/frontier/causal_heterogeneity/` before execution.

## 16. Pre-registered Expectations

From prior work and theoretical derivation:
- het(lambda) = lambda^2 * Var_a(E_S[f(S, a)]) for the synthetic DGP
- This implies het scales quadratically with lambda (not linearly), so Spearman rho should be high (monotonic increasing) even if the relationship is non-linear
- With 8 lambda levels spanning 0 to 1, Spearman should detect the monotonic trend
- The parent experiment's descriptive rho=1.0 suggests the effect is strong enough to detect with 8 levels

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
