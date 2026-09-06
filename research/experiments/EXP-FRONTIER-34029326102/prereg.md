# EXP-FRONTIER-34029326102 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34029326102
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-06
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does TV distance maintain its ability to detect action-dependent dynamical structure when synthetic Web transitions include realistic noise mechanisms (action-dependent heteroscedasticity, non-stationarity, state-dependent stochasticity), or does the signal degrade below detection threshold under realistic noise, rendering all prior clean-DGP validation insufficient for product deployment?

## 3. Motivation

Two successive synthetic experiments (EXP-FRONTIER-33863640568 affine, EXP-FRONTIER-33932275169 quadratic) confirm TV distance detects action-dependent dynamical structure with perfect monotonic scaling (Spearman rho=1.0) in controlled DGPs. However, all evidence is from clean, deterministic, lambda-ramped DGPs where action-dependence is artificially controlled via a single parameter.

Real Web transitions are expected to be:
- **Stochastic**: not purely deterministic; actions produce probabilistic outcomes
- **Noisy**: environmental noise varies by action type (e.g., form submissions are noisier than navigation)
- **Non-stationary**: website behavior changes over time
- **State-dependent**: some states (e.g., error pages) have noisier transitions than others

The dominant unknown is the **synthetic-to-real gap**: whether TV distance detection survives these realistic noise mechanisms. A further clean-DGP experiment would add marginal information compared to testing under noise.

This experiment bridges the gap by systematically degrading clean DGPs with three orthogonal noise models, each capturing a different aspect of real Web transitions.

## 4. Hypotheses

### H1: Positive Control
At noise_intensity=0 (clean DGP), TV distance equals the analytical value from EXP-FRONTIER-33932275169 within 10% across all 3 functions. This verifies pipeline consistency.

### H2: Monotonic Degradation
TV distance degrades monotonically with noise intensity for each noise model. Aggregate Spearman rho(TV, noise_intensity) >= 0.65 with p < 0.05 one-sided.

### H3: Moderate-Noise Detection
At noise_intensity=0.5, TV remains significantly above the permutation null (permutation p < 0.05). This is the critical test: can TV detect structure under moderate realistic noise?

### H4: High-Noise Convergence
At noise_intensity=1.0, TV approaches the permutation null (mean TV at high noise < 2x the permutation-null TV). Noise destroys the signal.

### H5: Function Invariance
The degradation pattern is consistent across 3 independent deterministic functions (no significant function x noise_model interaction in two-way ANOVA, p > 0.05).

## 5. Data Generation

### 5.1 Base DGP

Same as EXP-FRONTIER-33932275169:
- State space: S = {0, 1, ..., 9} (10 discrete states)
- Action space: A = {click, fill, submit, navigate} (4 action types)
- Transition function: S_{t+1} = f(S_t, A_t) where f is quadratic: f(s,a) = (c_a * s^2 + b_a * s + d_a) mod 10
- 3 deterministic functions (seeds 42, 43, 44) with known analytical TV at lambda=1

### 5.2 Noise Models

Three orthogonal noise models, each parameterized by noise_intensity ∈ {0.0, 0.25, 0.5, 0.75, 1.0}:

#### Model A: Action-Dependent Heteroscedastic Noise
Different actions have different noise levels. This models the real Web where form submissions are noisier than navigation.

For each action a, define action-specific noise concentration κ_a:
- κ_click = 10 (low noise: navigation is predictable)
- κ_fill = 5 (moderate noise: form filling is somewhat predictable)
- κ_submit = 2 (high noise: submission outcomes are variable)
- κ_navigate = 8 (low-moderate noise: page loads are mostly predictable)

Transition: S_{t+1} ~ Categorical(softmax(κ_a * noise_intensity * one_hot(f(s,a)) + (1-noise_intensity*κ_a/10) * uniform))

More precisely:
- With probability (1 - noise_intensity * w_a): S_{t+1} = f(s, a) deterministically
- With probability noise_intensity * w_a: S_{t+1} ~ Uniform(S)

where w_a = κ_a / max(κ) is the action-specific weight:
- w_click = 10/10 = 1.0
- w_fill = 5/10 = 0.5
- w_submit = 2/10 = 0.2
- w_navigate = 8/10 = 0.8

#### Model B: Non-Stationary Dynamics
Website behavior changes over time. This models real Web drift.

Two sub-models blended:
- Function f1 (seed 42): "initial website state"
- Function f2 (seed 43): "drifted website state"

At time step t:
- With probability (1 - noise_intensity * (t/T)): S_{t+1} = f1(s, a)
- With probability noise_intensity * (t/T): S_{t+1} = f2(s, a)

where T is the total number of transitions. This creates a gradual drift from f1 to f2.

#### Model C: State-Dependent Stochasticity
Some states have noisier transitions. This models error pages, loading states, etc.

Define per-state noise levels based on state index:
- States 0-3: low noise (κ=10) — "stable" states
- States 4-6: moderate noise (κ=5) — "transitional" states
- States 7-9: high noise (κ=2) — "unstable" states

Transition: S_{t+1} ~ Categorical(softmax(κ_s * noise_intensity * one_hot(f(s,a)) + (1-noise_intensity*κ_s/10) * uniform))

where κ_s is the state-specific concentration:
- κ_s = 10 for s ∈ {0,1,2,3}
- κ_s = 5 for s ∈ {4,5,6}
- κ_s = 2 for s ∈ {7,8,9}

### 5.3 Lambda Levels (Noise Intensity)

Five conditions:
- **noise_intensity=0.0**: Pure clean DGP, no noise (positive control)
- **noise_intensity=0.25**: Low noise (25% signal degradation)
- **noise_intensity=0.5**: Moderate noise (50% signal degradation) — critical test
- **noise_intensity=0.75**: High noise (75% signal degradation)
- **noise_intensity=1.0**: Maximum noise (100% signal degradation, approaches uniform)

### 5.4 Sample Size

- 1000 transitions per noise_model x noise_intensity x function x replication
- 10 replications per cell (3 noise_models x 5 intensities x 3 functions x 10 reps = 450 cells)
- Total transitions: 450,000
- Permutation tests at noise_intensity=0.0 and noise_intensity=1.0: 1000 shuffles per replication

## 6. Measures

### 6.1 TV Distance
For each cell:
1. Compute empirical P(S_{t+1} | do(A=a)) from transitions for each action a
2. Compute average pairwise TV distance: TV = (1/6) * sum_{i<j} TV(P_a_i, P_a_j)
3. TV(P, Q) = 0.5 * sum_s |P(s) - Q(s)|

### 6.2 Variance-of-Means (het)
For each cell:
1. Compute per-action mean next-state: mean_a = E[S_{t+1} | A=a]
2. Compute variance across actions: het = Var_a(mean_a)

### 6.3 Primary Metric
- **TV_degradation_spearman**: Spearman rho between TV and noise_intensity across the 5 levels, computed per noise model and per function
- **TV_at_moderate_noise**: TV value at noise_intensity=0.5, compared to permutation null

### 6.4 Secondary Metrics
- TV at each noise level for each function for each noise model
- Variance-of-means at each noise level for each function for each noise model
- Permutation p-values at noise_intensity=0.0 and 1.0
- Cohen's d for TV at noise_intensity=0 vs noise_intensity=0.5

## 7. Null Models

### 7.1 Permutation Null
Permute action labels across transitions. TV between shuffled action-conditional distributions should be near zero. Compute at noise_intensity=0.0 and noise_intensity=1.0.

### 7.2 Frequency Null
Predict next-state from marginal distribution P(S_{t+1}). TV between frequency and action-conditional distributions should equal TV at that noise level.

### 7.3 Clean-DGP Ceiling
TV values from EXP-FRONTIER-33932275169 provide the performance ceiling. Any degradation is due to noise, not metric insensitivity.

## 8. Statistical Tests

### 8.1 Primary Test
- Spearman rank correlation: rho(TV, noise_intensity) per noise model
- One-sided test: rho > 0
- Single comparison per noise model (3 noise models = 3 comparisons, Bonferroni x3)

### 8.2 Permutation Tests
- At noise_intensity=0.0: permutation test p > 0.05 (null control: TV not significantly > 0 when noise=0)
- At noise_intensity=1.0: permutation test p > 0.05 (null control: TV not significantly > 0 when noise=1)

### 8.3 Effect Size
- Cohen's d for TV at noise_intensity=0 vs noise_intensity=0.5

### 8.4 Function Invariance
- Two-way ANOVA: TV ~ noise_intensity + function + noise_intensity:function
- Non-significant interaction term (p > 0.05) supports function invariance

## 9. Controls

### 9.1 Positive Control (noise_intensity=0)
TV must match analytical value from EXP-FRONTIER-33932275169 within 10% across all 3 functions. This verifies pipeline consistency with prior validated experiments.

### 9.2 Null Control (noise_intensity=1.0)
TV must not significantly exceed the permutation null (permutation p > 0.05). This verifies noise destroys detectable structure.

### 9.3 Sensitivity Control (noise_intensity=0.5)
TV must remain significantly above the permutation null (permutation p < 0.05). This is the critical test of robustness.

### 9.4 Degradation Control
TV at each level must be <= TV at the previous level (monotonic degradation). Non-monotonic degradation indicates noise-type-specific effects.

## 10. Validity Threats

### 10.1 Sample Size
With 1000 transitions per cell and ~250 transitions per action, Monte Carlo SE of per-action means is sqrt(p*(1-p)/250) ~ 0.03. TV estimation is reliable. With 10 replications, TV variance estimation is adequate.

### 10.2 Noise Model Calibration
The three noise models use different parameterizations. Direct comparison across models requires normalization. Mitigation: each model is analyzed independently; cross-model comparison uses relative degradation (TV at noise=0.5 / TV at noise=0).

### 10.3 Synthetic-to-Real Gap (Remaining)
Even with realistic noise, synthetic transitions may not capture all real-Web complexity (e.g., continuous state spaces, authentication state, network latency). Mitigation: this experiment narrows the gap; full closure requires real Web data.

### 10.4 Deterministic Function Choice
3 functions from EXP-FRONTIER-33932275169 (quadratic, seeds 42-44) ensure comparability but limit diversity. Mitigation: function x noise_model interaction test checks consistency.

### 10.5 Multiple Comparisons
3 noise models x 1 primary test each = 3 comparisons. Bonferroni x3 is conservative. Mitigation: report both corrected and uncorrected p-values; focus on effect sizes.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Positive control passes: TV at noise_intensity=0 matches analytical value within 10% across all functions
2. Null control passes: TV at noise_intensity=1.0 not significantly above permutation null (p > 0.05)
3. Aggregate Spearman rho(TV, noise_intensity) >= 0.65 with p < 0.05 (one-sided, Bonferroni x3) for EACH noise model
4. No significant function x noise_model interaction (two-way ANOVA p > 0.05)
5. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Positive control fails
2. Null control fails
3. Spearman rho < 0.65 or p > 0.05 for ANY noise model
4. Significant function x noise_model interaction (p < 0.05)

### 11.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. TV CV across replications > 0.5 at noise_intensity=0 (indicates unstable baseline)
3. Deterministic functions generate degenerate transitions under noise

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates TV distance is robust to realistic noise mechanisms
- Clean-DGP validation generalizes to noisy Web-like transitions
- SPIDER can use TV distance in product pipelines without requiring perfectly clean data
- The synthetic-to-real gap, while real, does not invalidate TV-based detection at moderate noise
- Physics lane can proceed with TV-based regime detection on real Web data

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Clean-DGP validation is insufficient for product deployment
- TV distance is not robust to realistic noise
- SPIDER must either (a) develop noise-robust TV variants, (b) restrict TV to high-signal regimes, or (c) abandon TV as primary metric
- Physics lane should investigate alternative detection methods
- Does NOT falsify C-WEB-DYNAMICS entirely — only TV as the detection method under noise

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Data Generation**: Generate 450,000 transitions across 3 noise_models x 5 intensities x 3 functions x 10 reps x 1000 transitions
2. **TV Computation**: Compute empirical action-conditional distributions and pairwise TV for each cell
3. **Heterogeneity Computation**: Compute variance-of-means for each cell
4. **Permutation Tests**: Run 1000-shuffle permutation tests at noise_intensity=0.0 and 1.0
5. **Spearman Correlation**: Compute rho(TV, noise_intensity) per noise model and per function
6. **ANOVA**: Two-way ANOVA: TV ~ noise_intensity + function + noise_intensity:function
7. **Effect Sizes**: Cohen's d for TV at noise=0 vs noise=0.5
8. **Control Checks**: Verify positive, null, sensitivity, and degradation controls
9. **Reporting**: Report all outcomes with equal prominence

## 14. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for Spearman correlation and permutation tests
- `statsmodels` for two-way ANOVA
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-FRONTIER-34029326102/` before execution.

## 15. Pre-registered Expectations

From prior work:
- Clean DGPs (noise_intensity=0) should reproduce EXP-FRONTIER-33932275169 results (TV rho=1.0)
- Action-dependent noise (Model A) should degrade TV more slowly than uniform noise because the most predictable actions (click, navigate) retain structure longer
- Non-stationary noise (Model B) should degrade TV faster because the signal shifts rather than simply noising
- State-dependent noise (Model C) should show non-uniform degradation: states 0-3 retain structure longer than states 7-9
- Variance-of-means should degrade faster than TV under all noise models (consistent with EXP-FRONTIER-33932275169 where TV dominated het)

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
