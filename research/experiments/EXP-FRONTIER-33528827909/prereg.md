# EXP-FRONTIER-33528827909 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-33528827909
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-01
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the predictive advantage of action-conditioned rules over action-independent memory vary across transition regimes, and does this variation reveal dynamical heterogeneity in Web-like state transitions?

## 3. Motivation

Prior Physics work established:
- WP-001: rule-shuffle difference of ~+0.0532 (dimension accuracy)
- WP-002B: rule ~ nearest-neighbor > shuffle in-distribution; 901 transitions, 300 trajectories
- WP-003: MEASUREMENT_INVALID (target leakage)

These results report **average** effects across all transitions. They do not test whether the rule-shuffle difference is uniform or heterogeneous across different types of transitions.

If Web dynamics are regime-dependent (e.g., navigation transitions behave differently from form-submission transitions), then the average rule-shuffle difference is a mixture of qualitatively different regimes. Detecting this heterogeneity would:
1. Explain why average effects are small (+0.0532)
2. Identify which transition types have strong dynamical structure
3. Guide where SPIDER should invest in action-conditioned mechanisms

This experiment tests this using synthetic data where the ground-truth action-dependence is controlled, enabling a clean measurement without data availability constraints.

## 4. Hypotheses

### H1: Monotonic Scaling
The rule-memory accuracy difference scales monotonically with the action-dependence parameter lambda (Spearman rho >= 0.7).

### H2: Positive Control
At lambda=1 (fully action-determined), rules achieve >90% test accuracy.

### H3: Null Control
At lambda=0 (action-independent), rules do not significantly outperform memory (paired t-test p>0.05).

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

The deterministic_function is a frozen lookup table (seed=42) that maps (state, action) to a unique next state.

### 5.2 Lambda Levels

Three conditions:
- **lambda=0.0**: Pure noise, no action-dependence (null control)
- **lambda=0.5**: Mixed regime, half noise half signal
- **lambda=1.0**: Pure signal, full action-dependence (positive control)

### 5.3 Sample Size

- 300 transitions per lambda level (900 total)
- 80/20 train/test split (240 train, 60 test per level)
- Stratified split: equal representation of all (state, action) pairs in train

## 6. Measures

### 6.1 Rule Baseline
- Fit: For each (state, action) pair in train, compute majority-vote next state
- Predict: On test, look up (state, action) and predict majority-vote next state
- Cold start: For unseen (state, action) pairs, predict marginal most common next state

### 6.2 Memory Baseline
- Fit: For each state in train, compute majority-vote next state (ignoring action)
- Predict: On test, look up state and predict majority-vote next state

### 6.3 Primary Metric
- **rule_memory_diff** = accuracy(rule) - accuracy(memory) at each lambda level
- **Spearman rho** between rule_memory_diff and lambda across the 3 levels

### 6.4 Secondary Metrics
- Accuracy of each baseline at each lambda level
- Frequency of (state, action) pairs in train vs test

## 7. Null Models

### 7.1 Shuffle Null
Permute action labels across transitions. Rules trained on shuffled data should perform like memory (rule_memory_diff ≈ 0).

### 7.2 Frequency Null
Predict next state from marginal distribution P(S_{t+1}). Expected accuracy: 1/10 = 10%.

## 8. Statistical Tests

### 8.1 Primary Test
- Spearman rank correlation: rho(rule_memory_diff, lambda)
- One-sided test: rho > 0
- Bonferroni correction for 3 comparisons (one per lambda level)

### 8.2 Paired Comparisons
- At each lambda level: paired t-test, rule accuracy vs memory accuracy
- Two-sided, alpha=0.05
- Bonferroni corrected (3 tests)

### 8.3 Effect Size
- Cohen's d for rule vs memory accuracy at each lambda level

## 9. Controls

### 9.1 Positive Control (lambda=1)
- Rules must achieve >90% accuracy
- This verifies: deterministic_function is learnable, pipeline is correct

### 9.2 Null Control (lambda=0)
- Rules must not significantly outperform memory (paired t-test p>0.05)
- This verifies: pipeline does not detect structure when absent

### 9.3 Sensitivity Control (lambda=0.5)
- Rule-memory difference should be between 0 and the lambda=1 difference
- If this fails, the monotonicity hypothesis is weakened

## 10. Validity Threats

### 10.1 Sample Size
With 60 test transitions per level, we have ~80% power to detect a large effect (d=0.8) at alpha=0.05. Smaller effects may be missed. Mitigation: report confidence intervals alongside p-values.

### 10.2 Synthetic-to-Real Gap
Synthetic transitions may not reflect real Web dynamics. Mitigation: this is a controlled validation experiment. If the pipeline cannot detect known structure in synthetic data, it cannot be trusted on real data.

### 10.3 Discretization
State and action spaces are discrete by construction. No discretization artifacts. Mitigation: N/A.

### 10.4 Deterministic Function Choice
The frozen lookup table is arbitrary. Mitigation: test with 3 different random seeds for the lookup table as a robustness check.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Spearman rho(rule_memory_diff, lambda) >= 0.7, p<0.05 (one-sided, Bonferroni corrected)
2. Rules >90% accuracy at lambda=1 (positive control passes)
3. Rules not significantly > memory at lambda=0 (null control passes)
4. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Spearman rho < 0.7 or p>0.05 after correction
2. Positive control fails (rules <90% at lambda=1)
3. Null control fails (rules significantly > memory at lambda=0)

### 11.3 MEASUREMENT_INVALID
If:
1. Sample size insufficient (<60 test transitions per level)
2. Pipeline errors prevent computation
3. Deterministic function generates degenerate transitions

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates that Web-like transitions can have regime-dependent dynamics
- Justifies stratified analysis of real Web data
- The rule-shuffle difference from WP-002B (+0.0532) may be an average of high-dynamics and low-dynamics transitions
- Physics lane should investigate action-type-stratified dynamics

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Suggests that either (a) the rule framework is not sensitive to dynamical heterogeneity, or (b) the synthetic model does not produce detectable regime effects
- Does NOT falsify C-WEB-DYNAMICS entirely — only this specific detection method
- Physics lane should try other approaches (e.g., information-theoretic, causal)

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Data Generation**: Generate 900 transitions at 3 lambda levels (seed=42)
2. **Train/Test Split**: 80/20 stratified split
3. **Baseline Training**: Fit rule and memory baselines on train
4. **Evaluation**: Compute accuracy on test for each baseline at each level
5. **Statistical Tests**: Spearman correlation, paired t-tests with Bonferroni correction
6. **Controls**: Verify positive and null controls
7. **Robustness**: Repeat with 2 additional seeds for deterministic function
8. **Reporting**: Report all outcomes with equal prominence

## 14. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for Spearman correlation and t-tests
- `collections.Counter` for majority voting
- Standard library only (no custom estimators required)

Code will be committed to `research/frontier/regime_detection/` before execution.

## 15. Pre-registered Expectations

From prior Physics work:
- WP-002B rule-shuffle difference of +0.0532 suggests average action-dependence exists
- If this average is a mixture of regimes, we expect rule_memory_diff to vary with lambda
- If the average is uniform, we expect rule_memory_diff to be constant across lambda

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
