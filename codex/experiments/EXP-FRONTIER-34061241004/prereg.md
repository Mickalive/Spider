# EXP-FRONTIER-34061241004 Preregistration

## Status: DESIGN — NOT YET FROZEN

---

## 1. Context and Inherited State

This experiment continues from EXP-FRONTIER-34029326102 (handoff SHA256: f7d2a875c7227e81f12fe501a3b16f34f6b5145138fbc14c29ce44b7ab4fc244).

### Chain of Frontier Experiments

| Experiment | Method | Status | Key Finding |
|---|---|---|---|
| EXP-FRONTIER-33528827909 | Prediction accuracy decomposition | MEASUREMENT_INVALID | Descriptive monotonic rule-memory diff with lambda (rho=1.0), but statistical inference invalid (Bonferroni mismatch, saturated ANOVA) |
| EXP-FRONTIER-33767130362 | Causal heterogeneity (variance of means) | MEASUREMENT_INVALID | Permutation functions degenerate: Var_a(E_S[f(S,a)]) = 0 identically |
| EXP-FRONTIER-33863640568 | Causal heterogeneity + affine functions | FALSIFIED-IN-SETTING | Affine functions non-degenerate but TV signal not tested; causal het fails |
| EXP-FRONTIER-33932275169 | Quadratic DGP generalization | FALSIFIED-IN-SETTING | TV detects quadratic structure; function invariance fails |
| EXP-FRONTIER-34029326102 | TV distance noise robustness | FALSIFIED-IN-SETTING | All primary metrics pass (rho=-1.0, Cohen d 1.39-2.40); controls mis-calibrated |

### Established from Parent (EXP-FRONTIER-34029326102)

- TV distance degrades strictly monotonically with synthetic uniform-mixture noise in 10-state 4-action quadratic DGPs: aggregate Spearman rho = -1.0 (|rho| = 1.0), Cohen d 1.39-2.40 for noise=0 vs 0.5, p = 0.000 at moderate noise (0.5).
- TV retains substantial signal even at maximum synthetic noise: TV at noise_intensity=1.0 ranges 0.3156-0.4745 (45-68% of clean-DGP TV), well above estimated permutation null ~0.11.
- Positive control passes: TV at noise_intensity=0 matches analytical values within 10% for all 3 functions.
- Three orthogonal synthetic noise models (action-dependent, non-stationary, state-dependent) show consistent degradation patterns.
- TV dominates variance-of-means (het) as a detection metric.

### Rejected from Parent

- Sign-reversed Spearman (rho >= 0.65 with p < 0.05 one-sided positive) as valid falsification condition — correct test is |rho| >= 0.65.
- Null control expectation (noise_intensity=1.0 must be non-significant) when max uniform noise on finite state space preserves deterministic signal.
- ANOVA interaction p > 0.05 as falsification when testing heterogeneous function classes with different analytical TV ceilings.

### Unknown (Inherited)

- Whether real Web transitions exhibit Var_a(E_S[f]) > 0 suitable for TV detection, or are permutation-like (mean-preserving) — **the synthetic-to-real gap is the dominant unknown**.
- Whether TV remains robust under combined noise models (e.g., simultaneous action+state+temporal noise).
- Whether frequency baseline P(S_{t+1}) confounds conditional TV — completely absent from prior experiments.
- Whether heteroscedasticity across noise levels invalidates standard ANOVA/Spearman CIs.
- Generalization beyond 3 quadratic coefficient sets, 10-state discrete modulo space, and uniform-replacement noise.

### Do Not Assume (Inherited)

- Do not assume TV distance works on real Web transitions — all evidence is synthetic DGP with uniform-replacement noise on 10-state discrete quadratic modulo-10 space.
- Do not assume "realistic noise mechanisms" label means Web-realistic — prior code implements only (1-noise*w)*deterministic + noise*w*Uniform(10).
- Do not assume C-WEB-DYNAMICS is established — claim concerns real Web dynamics; synthetic-to-real gap untested.
- Do not assume product deployment readiness — no end-to-end economics, real Web data, or product integration tested.
- Do not assume combined noise robustness — only individual noise models tested.
- Do not assume effect sizes (Cohen d 1.39-2.40) generalize to Web — tiny 10-state space with huge analytical separation.

---

## 2. Scientific Question

Does TV distance detect action-dependent dynamical structure in realistic synthetic Web transition DGPs with continuous state, state-dependent dynamics, and heteroscedastic noise, or does the synthetic-to-real gap render all synthetic DGP validation insufficient for product deployment?

---

## 3. Motivation

### Why This Experiment Is Necessary

Five successive Frontier experiments have established that TV distance works on synthetic DGPs with uniform-mixture noise on 10-state discrete permutation states. The parent handoff identifies the synthetic-to-real gap as the **sole remaining bottleneck** for C-WEB-DYNAMICS product deployment:

> "Three successive synthetic experiments confirm TV distance detects action-dependent dynamical structure with perfect monotonic scaling and large effect sizes in controlled synthetic DGPs, including under realistic synthetic noise mechanisms. The synthetic-to-real gap is now the sole remaining bottleneck for C-WEB-DYNAMICS and product deployment readiness."

The parent's recommended_action explicitly states:

> "Do NOT repeat another synthetic noise-robustness or lambda-ramping experiment — the metric is validated for two function classes (affine, quadratic) with perfect scaling and robust to synthetic noise; marginal information gain from further synthetic experiments is low."

### Why Realistic Synthetic (Not Real Web Data)

Real Web transition data requires runtime infrastructure (recorded agent sessions with DOM state tracking) that is not available in this lane. The parent handoff acknowledges this:

> "If real Web data is unavailable, test on realistic synthetic DGPs with Web-faithful stochasticity (continuous state, state-dependent dynamics, authentication/latency) — not another uniform-mixture synthetic."

This experiment bridges the gap by testing TV distance on DGPs that have key Web-faithful properties:

1. **Continuous state space**: Real Web states are high-dimensional (DOM trees, embeddings), not 10 discrete states
2. **State-dependent dynamics**: Real Web transitions depend on current state in structured ways
3. **Heteroscedastic noise**: Real Web has non-trivial noise where predictability varies by state (some pages are more stable than others)

### Why This Is High-Information

This is the smallest experiment that can change a claim or product decision:

- **Positive result**: TV detects structure in Web-faithful DGPs → opens path to real Web data testing → product lane can design TV-based regime detection
- **Negative result**: TV fails in Web-faithful DGPs → synthetic-to-real gap is real → product lane must pivot to real data collection or alternative metrics
- **Comparison with uniform-mixture**: Quantifies whether Web-faithful dynamics help or hurt TV detection (not just whether TV works)

---

## 4. Hypotheses

### H1: Monotonic Scaling
TV distance between action-conditional next-state distributions increases monotonically with lambda in Web-faithful DGPs. Aggregate Spearman rho(tv_by_lambda, lambda) >= 0.65 with p < 0.05 one-sided.

### H2: Positive Control
At lambda=1 (fully action-determined transitions), TV >= 0.1 across all 3 function families. This verifies the pipeline can detect action-dependent structure in continuous state spaces with heteroscedastic noise.

### H3: Null Control
At lambda=0 (pure Gaussian noise), TV is indistinguishable from zero (permutation test p > 0.05). This verifies the pipeline does not detect structure when none exists.

### H4: Function Invariance
The monotonicity finding is consistent across 3 independent deterministic function families (no significant function x lambda interaction in two-way ANOVA, p > 0.05).

### H5: Web-Faithful Signal Strength
TV at lambda=1 in Web-faithful DGPs is not significantly LOWER than uniform-mixture DGPs at matched lambda (one-sided paired t-test p > 0.05). This tests whether Web-faithful dynamics produce larger or smaller signal than uniform-mixture noise.

---

## 5. Deterministic Function Design

### 5.1 Web-Faithful State Space

Continuous 2D state space: S = [0, 1]^2 (unit square).

This is a minimal continuous state that captures the key difference from prior experiments (10 discrete states). Real Web states are higher-dimensional, but 2D continuous is sufficient to test whether TV works beyond discrete permutation states.

### 5.2 Function Family A: Rotation-Based

For action a_i with angle theta_i:
```
f(s, a_i) = R(theta_i) * (s - center) + center + offset_i
```
where R(theta) is a 2D rotation matrix, center = [0.5, 0.5], and offset_i varies by action.

Parameters:
- theta = [0, pi/4, pi/2, 3*pi/4] (rotation angles)
- offset = [[0.1, 0], [0, 0.1], [-0.1, 0], [0, -0.1]] (action-dependent translations)

### 5.3 Function Family B: Scaling-Based

For action a_i with scale factors [sx_i, sy_i]:
```
f(s, a_i) = [sx_i * (s[0] - 0.5) + 0.5, sy_i * (s[1] - 0.5) + 0.5] + offset_i
```

Parameters:
- scale = [[1.2, 1.2], [0.8, 1.2], [1.2, 0.8], [0.8, 0.8]]
- offset = [[0.05, 0.05], [-0.05, 0.05], [0.05, -0.05], [-0.05, -0.05]]

### 5.4 Function Family C: Translation-Based

For action a_i with translation vector t_i:
```
f(s, a_i) = s + t_i + alpha_i * sin(2*pi*s)
```

Parameters:
- t = [[0.15, 0], [0, 0.15], [-0.15, 0], [0, -0.15]]
- alpha = [0.1, 0.1, 0.1, 0.1] (sinusoidal perturbation)

### 5.5 Analytic Verification

For each function family, compute E_S[f(S, a)] numerically (10,000 samples from Uniform([0,1]^2)) and verify:
1. E_S[f(S, a_i)] differs across actions (non-degenerate)
2. Var_a(E_S[f(S, a)]) > 0 (positive analytical heterogeneity)
3. TV between pushforward distributions f(S, a_i) is bounded below

If any function family is degenerate (identical means for all actions), replace with a different parameterization before execution.

### 5.6 Noise Model

Heteroscedastic Gaussian noise:
```
s_next = f(s, a) + epsilon, epsilon ~ N(0, sigma(s)^2 * I_2)
```
where sigma(s) = sigma_base * (1 + beta * ||s - center||)

Parameters:
- sigma_base = 0.05 (base noise level)
- beta = 0.5 (heteroscedasticity: noise increases near boundaries)

This is more realistic than uniform-mixture noise because:
- Noise is continuous (not discrete replacement)
- Noise variance depends on state (some states are more predictable)
- Noise is additive (not replacement)

---

## 6. Lambda Ramping

Same framework as prior experiments:
- lambda = 0.0: pure Gaussian noise, no action-dependence (null control)
- lambda = 0.1-0.7: mixed regime
- lambda = 1.0: fully deterministic action-dependent transitions

Transition generation:
```
For each transition:
  s ~ Uniform([0,1]^2)
  a ~ Uniform(ACTIONS)
  if rng.random() < lambda:
    s_next = f(s, a)  # deterministic function
  else:
    s_next ~ N(center, sigma_base^2 * I_2)  # Gaussian noise (not uniform)
```

Lambda levels: [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0] (8 levels)

---

## 7. Sample Size

- 500 transitions per lambda level per function per replication
- 8 lambda levels x 3 functions x 10 replications x 500 transitions = 120,000 total transitions
- No train/test split: all transitions used for TV computation
- Each replication uses a distinct frozen seed (seed = func_seed * 10000 + rep_idx * 100 + 42)

---

## 8. Metrics

### 8.1 Primary Metric: Total Variation Distance

TV_max(lambda) = max_{a,a'} TV(P(S_{t+1}|do(A=a)), P(S_{t+1}|do(A=a')))

Where TV(P, Q) = (1/2) * integral |P(s) - Q(s)| ds.

Computed from empirical action-conditional next-state distributions:
1. For each function x lambda x replication, group 500 transitions by action (~125 per action).
2. For each action pair (a, a'), compute TV between the empirical 2D distributions.
3. TV_max = maximum TV across all 6 action pairs.

TV computation: bin the 2D state space into a 20x20 grid (400 bins), compute empirical distributions, and calculate TV as half the L1 distance.

### 8.2 Secondary Metric: Mean TV

TV_mean(lambda) = mean_{a,a'} TV(P(S_{t+1}|do(A=a)), P(S_{t+1}|do(A=a')))

Average TV across all action pairs, not just maximum. Provides less noisy estimate of action-dependence.

### 8.3 Aggregate Statistics

- Aggregate Spearman rho(tv_max_by_lambda, lambda) with one-sided p-value
- Per-function Spearman rho with Bonferroni-corrected p-value (3 functions, alpha = 0.05/3)
- Cohen's d (lambda=1 vs lambda=0) for effect size
- Two-way ANOVA: tv_max ~ lambda + function + lambda:function

### 8.4 Comparison with Uniform-Mixture DGP

For each lambda level, compare TV_max in Web-faithful DGP with TV_max from prior uniform-mixture experiments (EXP-FRONTIER-34029326102, quadratic functions). Use paired t-test (one-sided) to test whether Web-faithful TV is LOWER (the hypothesis being tested).

---

## 9. Controls

### 9.1 Positive Control (lambda=1)
TV_max >= 0.1 across all 3 functions.
Rationale: With continuous state and state-dependent dynamics, action-conditional distributions should be distinguishable. TV >= 0.1 is achievable (prior uniform-mixture experiments achieved TV 0.32-0.47 at max noise).

### 9.2 Null Control (lambda=0)
TV_max not significantly > 0 (permutation test p > 0.05).
Rationale: Pure Gaussian noise yields identical distributions across actions.

### 9.3 Permutation Null
Shuffled action labels yield TV near zero at all lambda levels.
Verified analytically: shuffling action labels makes P(S_{t+1}|do(A=a)) identical for all actions.

### 9.4 Function Invariance
No significant function x lambda interaction (two-way ANOVA p > 0.05).
All functions should show similar TV(lambda) curves because the metric depends on the DGP structure, not specific transformation parameters.

### 9.5 Monotonicity Sensitivity
TV_max_means are monotonically non-decreasing across lambda levels.

### 9.6 Frequency Baseline
Compute P(S_{t+1}) from marginal next-state distribution. Expected heterogeneity under no action-dependence. This addresses the inherited unknown: "Whether frequency baseline P(S_{t+1}) confounds conditional TV."

---

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Aggregate Spearman rho(tv_max_by_lambda, lambda) >= 0.65, p < 0.05 one-sided
2. Positive control passes: TV_max >= 0.1 at lambda=1 across all functions
3. Null control passes: permutation test p > 0.05 at lambda=0
4. No significant function x lambda interaction (ANOVA p > 0.05)
5. Web-faithful TV at lambda=1 is not significantly LOWER than uniform-mixture (one-sided p > 0.05)
6. No pipeline errors

### 10.2 FALSIFIED-IN-SETTING
If ANY of:
1. Aggregate Spearman rho < 0.65 or p > 0.05
2. Positive control fails (TV < 0.1 at lambda=1 in any function)
3. Null control fails (TV significantly > 0 at lambda=0)
4. Significant function x lambda interaction (p < 0.05)
5. Web-faithful TV at lambda=1 is significantly LOWER than uniform-mixture (one-sided p < 0.05)

### 10.3 MEASUREMENT_INVALID
If:
- Pipeline errors
- Degenerate functions (TV between action-conditional deterministic distributions = 0 for all actions in any function)
- TV heterogeneity CV across replications > 0.5

---

## 11. Analysis Plan

1. **Function verification**: For each function family, compute E_S[f(S, a)] numerically (10,000 samples). Verify they differ across actions. Compute analytical Var_a(E_S[f(S,a)]) and pairwise TV between pushforward distributions.

2. **Data generation**: Generate 120,000 transitions using frozen seeds and Web-faithful DGP.

3. **TV computation**: For each function x lambda x replication, compute TV_max and TV_mean from empirical action-conditional 2D distributions (20x20 grid binning).

4. **Frequency baseline**: Compute P(S_{t+1}) from marginal distribution. Compute TV between P(S_{t+1}) and each action-conditional distribution. This assesses whether marginal non-uniformity confounds conditional TV.

5. **Primary test**: Aggregate Spearman rho(tv_max_means_by_lambda, lambda_levels).

6. **Per-function tests**: Spearman rho per function (n=8 each, Bonferroni x3 corrected).

7. **Permutation tests**: At lambda=0 and lambda=1, test TV against permutation null (1000 permutations).

8. **Two-way ANOVA**: tv_max ~ lambda + function + lambda:function (240 observations).

9. **Comparison with uniform-mixture**: For each lambda level, paired comparison of TV_max with prior experiment results. One-sided t-test: is Web-faithful TV lower?

10. **Controls**: Verify positive, null, permutation null, function invariance, and monotonicity controls.

11. **Effect size**: Cohen's d (lambda=1 vs lambda=0).

12. **Reporting**: Report all outcomes with equal prominence.

---

## 12. Validity Threats

### 12.1 State Space Dimensionality
2D continuous state is a minimal test of TV on continuous distributions. Real Web states are higher-dimensional. **Mitigation**: 2D is sufficient to test whether TV works beyond discrete permutation states. Higher-dimensional testing is a separate experiment.

### 12.2 Grid Binning for TV
TV computation uses 20x20 grid binning, which introduces discretization. **Mitigation**: 20x20 = 400 bins for 2D is adequate resolution for 500 transitions per cell (~1.25 per bin on average). Report sensitivity to bin size (10x10, 20x20, 30x30).

### 12.3 Synthetic-to-Real Gap (Remaining)
Even with Web-faithful properties, this is still synthetic data. Real Web has authentication, latency, session state, DOM structure. **Mitigation**: If TV works here, it's more likely to work on real data than if it only works on uniform-mixture DGPs. This experiment reduces but does not eliminate the gap.

### 12.4 Lambda Ramping Assumption
The DGP uses the same lambda-ramping framework as prior experiments. Real Web may not have a single action-dependence parameter. **Mitigation**: Lambda-ramping is a controlled experimental framework, not a claim about Web structure.

### 12.5 Multiple Comparisons
Aggregate test is single comparison (no correction). Per-function tests use Bonferroni x3. **Mitigation**: Primary test is aggregate; per-function tests are secondary.

### 12.6 TV Binning Sensitivity
TV computed from binned distributions may be sensitive to bin size. **Mitigation**: Report TV at multiple bin sizes (10x10, 20x20, 30x30) and verify qualitative consistency.

---

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- TV detects action-dependent structure in Web-faithful DGPs
- Opens path to real Web data testing
- Product lane can design TV-based regime detection
- C-WEB-DYNAMICS claim strengthens (still HYPOTHESIS, but detection validated in more realistic setting)

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- TV fails in Web-faithful DGPs
- Synthetic-to-real gap is real
- Product lane must pivot: real data collection, alternative metrics, or abandon TV detection
- C-WEB-DYNAMICS remains HYPOTHESIS; TV constrained to uniform-mixture DGPs

### 13.3 Mixed Result
- TV works in some function families but not others → function invariance fails
- TV works at high lambda but not low lambda → threshold effect
- Web-faithful TV is similar to uniform-mixture TV → no evidence gap exists

### 13.4 Invalid Result (MEASUREMENT_INVALID)
- Pipeline debugging needed
- Not scientific evidence for or against

---

## 14. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations, random generation, and distribution computation
- `scipy.stats` for Spearman correlation and t-tests
- `scipy.stats` or `statsmodels` for two-way ANOVA
- `scipy.spatial.distance` for TV computation (L1 distance on binned distributions)
- Standard library only (no custom estimators required)

Code will be committed to `research/frontier/web_faithful_tv/` before execution.

---

## 15. Pre-registered Expectations

From prior work and theoretical analysis:
- Web-faithful DGPs with continuous state should produce LARGER TV than uniform-mixture DGPs at the same lambda, because state-dependent dynamics concentrate probability mass rather than spreading it uniformly
- Heteroscedastic noise should not destroy TV signal because noise is additive (not replacement) and state-dependent (not uniform)
- TV at lambda=0 should be near zero because pure Gaussian noise is identical across actions
- TV at lambda=1 should be bounded below by the pairwise TV between deterministic pushforward distributions (analytically computable)

From the parent experiment:
- Uniform-mixture TV at noise=1.0 was 0.3156-0.4745
- Web-faithful TV at lambda=1 should be >= this range (more structure, less noise)

---

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

---

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
