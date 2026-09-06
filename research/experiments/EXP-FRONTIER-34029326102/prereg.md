# EXP-FRONTIER-34029326102 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34029326102
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Parent**: EXP-FRONTIER-33932275169 (quadratic TV distance validation)
- **Date**: 2026-09-06
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does TV distance maintain monotonic lambda-scaling of dynamical structure detection under realistic stochastic noise conditions, or does noise destroy the metric's discriminating power before product-relevant noise levels are reached?

## 3. Motivation

### 3.1 Parent Evidence

EXP-FRONTIER-33932275169 validated TV distance on quadratic synthetic DGPs:
- TV scales perfectly monotonically with lambda (aggregate Spearman rho=1.0)
- TV dominates variance-of-means at every lambda level (d=7.85 vs 1.71)
- Null control passes (permutation p=0.508)
- Positive control passes (all functions exceed 0.8x analytical threshold)

The parent verdict was FALSIFIED-IN-SETTING due to a mis-calibrated ANOVA interaction control inherited from the affine experiment — not due to metric failure. All primary metrics pass with large effects.

### 3.2 Inherited Unknowns

The parent handoff identifies the synthetic-to-real gap as the dominant unknown:
- Whether real Web transitions exhibit Var_a(E_S[f])>0 suitable for TV detection
- Whether real Web transitions are permutation-like (mean-preserving) requiring different metrics
- Whether finite-sample TV bias at null (0.1498 vs theoretical 0) causes false positives in noisier data

### 3.3 Why Noise Testing Is the Minimum Next Step

The parent handoff recommends testing on real or realistic Web data. Real Web data requires browser infrastructure (Playwright, site access, state tracking) not available in this experiment. Stochastic noise injection is the minimum informative approximation: it tests whether TV distance degrades gracefully under conditions that approximate real Web properties (stochastic transitions, variable noise, state-dependent dynamics).

Key real-Web properties approximated by noise injection:
- **Stochastic server responses**: Same action from same state can yield different next states (additive uniform noise)
- **Variable page complexity**: Some pages have dynamic content, ads, A/B tests (heteroscedastic noise)
- **Mixed dynamics**: Different transition types have different noise characteristics (mixed noise)
- **Mean-preserving transitions**: Some Web transitions add spread without shifting the mean state (mean-preserving spread)

## 4. Hypotheses

### H1: Graceful Degradation
TV scaling (Spearman rho(TV, lambda)) degrades monotonically with noise fraction across all noise types. The relationship between noise fraction and TV scaling strength is monotonic (Spearman rho >= 0.7).

### H2: Noise-Type Ordering
Mean-preserving noise breaks TV scaling first (at lowest noise fraction), additive uniform noise breaks it last. Ordering: mean-preserving < heteroscedastic < mixed < additive-uniform in terms of noise fraction at which TV scaling breaks (rho < 0.7).

### H3: Persistence Threshold
TV scaling persists (rho >= 0.7) at noise_fraction <= 0.6 for ALL noise types. This defines a product-relevant robustness bound.

### H4: Positive Control
At lambda=1, noise_fraction=0: rules achieve >90% test accuracy across all 3 function families (replicating parent).

### H5: Null Control
At lambda=0, noise_fraction=0: rules do not significantly outperform memory (paired t-test p>0.05) (replicating parent).

## 5. Data Generation

### 5.1 Base Signal (Same as Parent)

Three quadratic function families (seeds 42, 43, 44):
- f(s,a) = (c_a * s^2 + b_a * s + d_a) mod 10
- State space: S = {0, 1, ..., 9} (10 states)
- Action space: A = {click, fill, submit, navigate} (4 actions)
- Lambda parameterizes mix of deterministic signal vs uniform noise

### 5.2 Noise Injection Model

For each transition (S_t, A_t, S_{t+1}):
1. Generate deterministic signal: S_signal = f(S_t, A_t) (from quadratic function)
2. With probability lambda: S_{t+1} = S_signal
3. With probability (1-lambda): S_{t+1} = draw from noise distribution (varies by DGP variant)

The noise fraction controls the probability of drawing from the noise distribution rather than the deterministic signal. This is identical to the parent's lambda-ramping mechanism but with different noise distributions.

### 5.3 DGP Variants

**DGP-1: Pure Signal (Baseline)**
- Noise distribution: Uniform over S = {0,...,9}
- Same as parent: 100% signal at lambda=1, 100% uniform at lambda=0
- Purpose: Replicate parent results exactly

**DGP-2: Additive Uniform**
- Noise distribution: Uniform over S = {0,...,9}
- Identical to DGP-1 in mathematical form
- Purpose: Explicit replication arm; differences from DGP-1 would indicate implementation error

**DGP-3: Heteroscedastic State-Dependent**
- Noise distribution: Mixture — with probability 0.7, uniform over all states; with probability 0.3, uniform over a biased subset
- Biased subset for each state s: {(s+5) mod 10, (s+6) mod 10, (s+7) mod 10} (3-state neighborhood)
- Meaning: some transitions are noisier than others depending on current state
- Purpose: Approximate pages with variable dynamic content (e.g., homepage vs article page)

**DGP-4: Mixed Noise**
- Noise distribution: Randomly select one of three sub-distributions per transition:
  - 1/3 probability: uniform over S (additive uniform)
  - 1/3 probability: heteroscedastic (biased subset as in DGP-3)
  - 1/3 probability: action-dependent (noise centered on f(S_t, A_other) for random A_other != A_t)
- Purpose: Approximate real Web where different transition types have different noise characteristics

**DGP-5: Mean-Preserving Spread**
- Noise distribution: Symmetric around deterministic signal
- S_{t+1} = (S_signal + delta) mod 10, where delta ~ Uniform({-2,-1,0,1,2})
- At lambda=0: S_{t+1} is uniform (symmetric spread covers all states)
- At lambda=1: S_{t+1} = S_signal (no spread)
- Purpose: Test whether TV detects variance changes when the mean is preserved. If Var_a(E_S[f]) is the key quantity, mean-preserving spread should reduce TV scaling more than asymmetric noise.

### 5.4 Noise Fraction Levels

Seven levels: 0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0
- 0.0: Pure noise (null control condition)
- 0.2-0.4: Low noise (realistic for stable Web pages)
- 0.6: Moderate noise (realistic for dynamic pages)
- 0.8-0.9: High noise (realistic for highly dynamic/interactive pages)
- 1.0: Pure signal (positive control condition)

### 5.5 Sample Size

- 500 transitions per noise-fraction x DGP-variant x function cell
- 5 independent replications per cell (different RNG seeds)
- Total: 7 noise fractions x 5 DGP variants x 3 functions x 500 transitions x 5 replications = 52,500 transitions
- 80/20 train/test split: 400 train, 100 test per cell

### 5.6 Random Seeds

- Base seed: 42 (same as parent)
- Function seeds: 42, 43, 44 (same as parent)
- Replication seeds: 1000, 1001, 1002, 1003, 1004
- Noise injection uses seeded RNG per cell

## 6. Measures

### 6.1 TV Distance (Primary)
- For each lambda level within a cell: compute TV = (1/|A|) * sum_a ||P(S_{t+1}|S_t, A_t=a) - P(S_{t+1}|S_t)||_1
- Averaged over random S_t draws from test set
- Same computation as parent

### 6.2 Variance-of-Means (Secondary)
- For each lambda level: compute Var_a(E_S[f(S,a)])
- Expected to degrade faster than TV under noise

### 6.3 Baselines
- Rule accuracy: per-(state,action) majority vote from train
- Memory accuracy: per-state majority vote from train
- Rule-memory difference: accuracy(rule) - accuracy(memory)
- Shuffle accuracy: rules trained on shuffled action labels

### 6.4 Primary Metric
- **rho_TV_by_noise**: Spearman rho between TV and lambda at each noise fraction, averaged across functions and replications
- **monotonic_degradation**: Spearman rho between rho_TV_by_noise and noise_fraction (across 7 noise levels)

### 6.5 Secondary Metrics
- Cohen's d for TV at lambda=1 vs lambda=0 at each noise fraction
- Permutation p-value for TV at noise=0 (replication of parent null test)
- Per-function rho_TV_by_noise for consistency check
- Variance of rho_TV across replications at each noise fraction
- Variance-of-means rho_het_by_noise for comparison

## 7. Null Models

### 7.1 Shuffle Null
Permute action labels. Rules trained on shuffled data should have rho_TV ≈ 0 at all noise fractions.

### 7.2 Frequency Null
Predict next state from marginal distribution P(S_{t+1}). Expected accuracy: 1/10 = 10%.

### 7.3 Per-Replication Variance
5 replications per cell provide empirical variance of TV estimates. If variance is high (CV > 0.3 across replications), the metric is unstable at that noise level.

## 8. Statistical Tests

### 8.1 Primary Test: Monotonic Degradation
- Spearman rho(rho_TV_at_noise_fraction, noise_fraction) for each noise type
- One-sided: rho < 0 (negative correlation = degradation with noise)
- Bonferroni correction for 5 noise types x 3 functions = 15 comparisons

### 8.2 Persistence Threshold
- At each noise fraction: one-sided t-test, rho_TV > 0.7
- Bonferroni corrected across 7 noise fractions x 5 noise types = 35 comparisons

### 8.3 Noise-Type Ordering
- Compare noise fraction at which rho_TV drops below 0.7 across noise types
- Non-parametric: Kruskal-Wallis test on per-replication rho_TV at each noise fraction

### 8.4 Effect Size
- Cohen's d for TV at lambda=1 vs lambda=0 at each noise fraction

### 8.5 TV vs Variance-of-Means
- Paired comparison: rho_TV vs rho_het at each noise fraction
- Expected: rho_TV >= rho_het at all noise levels (replicating parent finding)

## 9. Controls

### 9.1 Positive Control (lambda=1, noise=0)
- Rules must achieve >90% accuracy across all 3 functions
- Replicates parent positive control
- Verifies pipeline integrity

### 9.2 Null Control (lambda=0, noise=0)
- Rules must not significantly outperform memory (paired t-test p>0.05)
- Replicates parent null control

### 9.3 DGP-1 Replication Control
- DGP-1 (pure signal) results must match parent experiment within 10% relative error
- rho_TV aggregate at noise=0 should be ~1.0 (perfect monotonic)
- If replication fails, pipeline has implementation error

### 9.4 Variance-of-Means Comparison
- At each noise fraction: rho_TV >= rho_het
- If variance-of-means outperforms TV at any noise level, the parent finding does not generalize

### 9.5 Cross-Function Consistency
- At each noise fraction: CV of rho_TV across 3 functions should be < 0.3
- If CV > 0.3, function-specific effects dominate noise effects

## 10. Validity Threats

### 10.1 Synthetic-to-Real Gap
Stochastic noise injection approximates but does not replicate real Web transition noise. Real Web transitions may have correlated noise, non-stationary dynamics, or continuous state spaces. Mitigation: this is a controlled robustness test; failure here strongly suggests failure on real data, while success is necessary but not sufficient.

### 10.2 Noise Model Specificity
The 5 DGP variants are parametric approximations. Real Web noise may have different structure. Mitigation: test multiple noise types to bound the range of noise characteristics under which TV works.

### 10.3 Sample Size
500 transitions per cell, 100 test samples. Power analysis: for detecting rho_TV = 0.7 with n=6 lambda levels, power is ~80% at alpha=0.05. Smaller effects at high noise may be underpowered. Mitigation: report confidence intervals; 5 replications provide variance estimates.

### 10.4 Finite-Sample TV Bias
Parent observed TV=0.1498 at null (theoretical 0) with 125 transitions per action. With 500 transitions per cell, bias should be smaller (~0.075 expected as 1/sqrt(500) scaling). Mitigation: measure and report TV at lambda=0 for each noise fraction.

### 10.5 Interaction Between Lambda and Noise
The experiment varies both lambda and noise fraction independently. If lambda x noise fraction interaction is strong, the interpretation becomes more complex. Mitigation: two-way ANOVA on rho_TV as function of lambda and noise fraction.

### 10.6 Replication Independence
5 replications use different RNG seeds but share the same deterministic function and noise model. Independence assumption is valid for the statistic of interest (rho_TV) but not for raw transitions. Mitigation: report both per-replication and aggregate statistics.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Monotonic degradation: Spearman rho(rho_TV, noise_fraction) >= 0.7 for each noise type (Bonferroni corrected, 15 comparisons)
2. Persistence: rho_TV >= 0.7 at noise_fraction <= 0.6 for ALL noise types
3. Positive control: rules >90% at lambda=1, noise=0 (all functions)
4. Null control: rules not significantly > memory at lambda=0, noise=0
5. DGP-1 replication: rho_TV at noise=0 within 10% of parent (rho=1.0)
6. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. rho_TV < 0.7 at noise_fraction <= 0.4 for any noise type
2. Monotonic degradation rho < 0.7 (TV scaling does not degrade smoothly with noise)
3. Positive control fails
4. Null control fails
5. DGP-1 replication fails (rho_TV at noise=0 deviates >20% from parent)

### 11.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. Fewer than 3 of 5 replications complete
3. Sample sizes insufficient (<100 test transitions per cell)

## 12. Expected Outcomes

### 12.1 Best Case (SURVIVES_CURRENT_TEST)
- TV distance is robust to stochastic noise at product-relevant levels
- Graceful degradation provides a calibration bound for real-world deployment
- Mean-preserving noise breaks TV first, confirming that variance structure matters
- Product can deploy TV-based regime detection with quantified confidence bounds

### 12.2 Moderate Case (FALSIFIED-IN-SETTING at high noise)
- TV breaks at noise_fraction = 0.6-0.8 (moderate noise)
- Product must preprocess transitions to reduce noise before TV computation
- Still informative: quantifies the noise threshold for regime detection

### 12.3 Worst Case (FALSIFIED-IN-SETTING at low noise)
- TV breaks at noise_fraction <= 0.4 (low noise)
- Synthetic-to-real gap is likely insurmountable for raw TV distance
- Product must develop alternative metrics or noise-reduction preprocessing
- Frontier should explore fundamentally different approaches

### 12.4 Invalid (MEASUREMENT_INVALID)
- Pipeline needs debugging
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Data Generation**: Generate 52,500 transitions across 7 noise fractions x 5 DGP variants x 3 functions x 5 replications
2. **Train/Test Split**: 80/20 stratified by lambda within each cell
3. **TV Computation**: Compute TV at each lambda level within each cell
4. **Baseline Fitting**: Fit rule and memory baselines on train, evaluate on test
5. **Statistical Tests**: Spearman correlations, persistence tests, ANOVA, effect sizes
6. **Control Verification**: Check positive, null, replication, and cross-metric controls
7. **Robustness**: Report confidence intervals, per-replication variance, cross-function CV
8. **Reporting**: Report all outcomes with equal prominence

## 14. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for Spearman correlation, t-tests, Kruskal-Wallis
- `scipy.stats.f_oneway` or `statsmodels` for two-way ANOVA
- `collections.Counter` for majority voting
- Standard library only (no custom estimators)

Code will be committed to `research/frontier/noise_robustness/` before execution.

## 15. Pre-registered Expectations

From parent experiment:
- TV distance has perfect monotonic scaling on clean DGPs (rho=1.0)
- TV dominates variance-of-means (d=7.85)
- Variance-of-means has lower sensitivity (rho=0.9429, non-monotonic dip)

Expected under noise:
- TV scaling degrades monotonically with noise fraction
- Mean-preserving noise degrades TV faster than asymmetric noise (because it reduces Var_a directly)
- Variance-of-means degrades faster than TV under all noise types
- Cross-function consistency holds at low noise, degrades at high noise

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
