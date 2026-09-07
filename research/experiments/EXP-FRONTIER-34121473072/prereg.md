# EXP-FRONTIER-34121473072 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34121473072
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-07
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does bias-corrected kNN TV recover uniform function invariance in 10D non-Gaussian spaces after removing finite-sample bias floor, and does clipping artefact quantitatively explain the translation-scaling asymmetry?

## 3. Motivation

Parent experiment EXP-FRONTIER-34065969836 falsified uniform TV generalization from 2D Gaussian to 10D non-Gaussian settings via function invariance failure (ANOVA p~1e-30) and positive control failure under frozen spec (permutation p~0.14 at lambda=1). However, the audit identified two critical validity threats that may change the quantitative picture:

1. **kNN bias floor ~0.52**: TV at pure-noise lambda=0 is 0.5227 (k=20) aggregate, not ~0. The entire dynamic range (0.094 aggregate, 0.201 translation, 0.022 scaling) is within the noise floor. Bias-corrected TV not computed.

2. **Clipping artefact**: ~50% of transitions clipped to [0,1]^10 at lambda=1 (0.498 rotation, 0.486 scaling, 0.493 translation) vs 2.3-2.5% at lambda=0. Edge mass inflates TV at high lambda differentially by function family.

These threats may explain why translation shows strong signal (separation=0.201) while scaling shows weak signal (separation=0.022). The next experiment must apply the audit's required_fixes before the scaling failure can be attributed to genuine signal absence vs estimator artefact.

## 4. Hypotheses

### H1: Bias Correction Rescues Function Invariance
After subtracting per-lambda permutation mean (bias correction), the function x lambda interaction becomes non-significant (two-way ANOVA p>0.05). This would indicate that the observed function invariance failure is an artefact of non-uniform bias across functions.

### H2: Scaling Monotonic Recovers After Bias Correction
After bias correction, scaling function (seed=43) shows monotonic increase (Spearman rho>=0.5, p<0.05). This would indicate that scaling failure was due to bias floor masking a weak but real signal.

### H3: Clipping Artefact Explains Part of Translation Signal
Toroidal wrapping (eliminating clipping) reduces translation separation by >30% but not >80%. This would indicate that clipping inflates translation signal but does not fully explain it.

### H4: Frequency Baseline Explains Bias Floor
The marginal next-state distribution P(S_{t+1}) is non-uniform, contributing to the ~0.52 TV floor at lambda=0. Frequency baseline TV quantifies this contribution.

## 5. Data Generation

### 5.1 Synthetic Transition Model (Identical to Parent)

Same DGP as EXP-FRONTIER-34065969836:

- State space: S = [0,1]^10 (continuous, uniform)
- Action space: A = {click, fill, submit, navigate} (4 actions)
- Transition function: S_{t+1} = f(S_t, A_t, lambda) + noise
- Noise: mixture-of-3-Gaussians heteroscedastic (parent's noise model)
- Lambda levels: 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0 (8 levels)
- Function families: rotation (seed=42), scaling (seed=43), translation (seed=44)
- 500 transitions per cell, 10 reps per cell
- Total transitions: 3 funcs x 8 lambdas x 10 reps x 500 = 120,000

### 5.2 Frozen Random Seed

Seed=42 for base DGP; function seeds 42,43,44 identical to parent.

## 6. Measures

### 6.1 Bias-Corrected kNN TV

For each lambda, function, kNN scale (k=5,10,20,50):
1. Compute TV at lambda (TV_raw) as in parent
2. Compute permutation mean at same lambda: permute action labels 1000 times, compute TV for each permutation, take mean (perm_mean)
3. Bias-corrected TV = max(0, TV_raw - perm_mean)

### 6.2 Toroidal Wrapping

For each transition: after noise addition, wrap coordinates modulo 1: S_wrap = S mod 1. This eliminates clipping to [0,1]^10. Compute TV on wrapped transitions.

### 6.3 Frequency Baseline

Compute marginal next-state distribution P(S_{t+1}) across all transitions at each lambda. Compute expected TV under independence: TV_freq = TV(P(S_{t+1}) || uniform). This quantifies floor contribution from marginal non-uniformity.

### 6.4 Gaussian Noise Baseline

Generate same DGP but replace mixture-of-3-Gaussians with single Gaussian heteroscedastic noise (same variance parameters). Compute TV at each lambda/function. Isolate non-Gaussian effect.

### 6.5 Clipping Fraction

Compute fraction of transitions where any coordinate is clipped to [0,1] (i.e., after noise addition, coordinate <0 or >1). Report per lambda/function.

### 6.6 Primary Metric

- **bias_corrected_tv_max_k20**: bias-corrected TV at k=20 (primary estimator)
- **Spearman rho** between bias_corrected_tv_max_k20 and lambda per function
- **Function invariance**: two-way ANOVA interaction p-value on bias_corrected_tv

### 6.7 Secondary Metrics

- Raw TV (un-corrected) for comparison with parent
- Effect sizes (Cohen's d) lambda=0 vs lambda=1 after bias correction
- Multiscale monotonicity across k=5,10,20,50
- Toroidal TV separation (translation, scaling, rotation)
- Frequency baseline TV
- Gaussian baseline TV per function/lambda

## 7. Null Models

### 7.1 Permutation Null (Bias Estimation)

For each lambda/function/kNN scale: permute action labels 1000 times, compute TV for each permutation. Mean of permutation distribution = bias estimate. Subtract from raw TV.

### 7.2 Frequency Null

Predict next state from marginal P(S_{t+1}). Expected TV under independence = TV(P(S_{t+1}) || uniform). If non-zero, explains part of floor.

### 7.3 Gaussian Null

Same DGP with single Gaussian noise. If scaling recovers under Gaussian noise, isolates non-Gaussianity as cause of scaling failure.

## 8. Statistical Tests

### 8.1 Primary: Spearman Correlation on Bias-Corrected TV

- Per function: rho(bias_corrected_tv, lambda)
- One-sided test: rho > 0
- Bonferroni correction for 3 functions x 1 test = 3 comparisons
- Threshold: rho >= 0.5 with p < 0.05 after correction

### 8.2 Function Invariance (Two-Way ANOVA)

- Model: bias_corrected_tv ~ lambda + function + lambda:function
- Interaction p > 0.05 supports invariance
- Full model with replications (10 reps per cell) provides residual df

### 8.3 Clipping Sensitivity

- Paired t-test: TV_raw vs TV_toroidal at lambda=1 across functions
- Separation after toroidal wrapping > 0.05 required for positive control

### 8.4 Bias Correction Magnitude

- Compute mean bias per lambda (permutation mean)
- Report bias-corrected dynamic range: (TV_max - bias_max) - (TV_min - bias_min)

## 9. Controls

### 9.1 Positive Control (Translation)
After bias correction, translation function (seed=44) shows monotonic increase (rho>=0.8, p<0.05) with separation >0.05 between lambda=0 and lambda=1.

### 9.2 Null Control (Scaling)
After bias correction, scaling function (seed=43) shows no monotonic increase (rho<0.5, p>0.05) if scaling failure persists; OR if scaling recovers, rho>=0.5 p<0.05.

### 9.3 Bias Floor Uniformity
Bias (permutation mean) should be similar across functions at each lambda. If bias differs substantially across functions, function invariance failure may be bias-driven.

### 9.4 Toroidal Clipping Control
Toroidal wrapping should not change TV at lambda=0 (where clipping is minimal). If it does, indicates boundary artefact in DGP.

### 9.5 Frequency Baseline Control
Frequency baseline TV should be near zero if marginal distribution is uniform. If non-zero, quantifies floor contribution.

## 10. Validity Threats

### 10.1 Same DGP as Parent
This experiment uses identical synthetic data. Findings are bounded to this DGP; synthetic-to-real gap persists.

### 10.2 Permutation Bias Estimation
1000 permutations per cell gives bias estimate with SE ~0.01 (assuming TV variance ~0.01). Bias correction may introduce noise if permutation variance high. Mitigation: report bias SE per cell.

### 10.3 Toroidal Wrapping Distortion
Wrapping modulo 1 may distort spatial structure if transitions cross boundaries frequently. Mitigation: compute clipping fraction; if >50% at lambda=1, wrapping may distort more than clipping.

### 10.4 Gaussian Baseline Mismatch
Single Gaussian noise may not match mixture variance parameters exactly. Mitigation: use same variance parameters as mixture marginal.

### 10.5 Multiple Comparisons
3 functions x 4 kNN scales = 12 secondary comparisons. Bonferroni correction applied to primary per-function tests (3 comparisons).

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Function invariance passes (two-way ANOVA interaction p>0.05) on bias-corrected TV
2. Scaling monotonic passes (rho>=0.5, p<0.05) on bias-corrected TV
3. Translation separation >0.05 after toroidal wrapping
4. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Function invariance fails (interaction p<0.05) AND scaling monotonic fails (rho<0.5, p>0.05)
2. Translation separation <0.05 after toroidal wrapping (clipping explains >80% of signal)
3. Positive control fails (translation monotonic rho<0.8)

### 11.3 MIXED
If mixed results: e.g., function invariance passes but scaling fails, or vice versa.

### 11.4 MEASUREMENT_INVALID
If pipeline errors or sample size insufficient (<500 transitions per cell).

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Bias correction rescues scaling and function invariance
- Scaling failure was estimator artefact, not genuine signal absence
- TV distance works uniformly across function families in 10D non-Gaussian spaces after bias correction
- Claim C-WEB-DYNAMICS strengthened for high-dimensional settings
- Product lane can consider TV-based regime detection across diverse dynamical families

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Bias correction does not rescue scaling
- Scaling-type dynamics are not detectable by kNN TV in high-dimensional spaces
- TV claim bounded to translation-like dynamics only
- Product lane should focus on translation-like dynamics or alternative estimators

### 12.3 Mixed Result (MIXED)
- Bias correction partially rescues function invariance but scaling remains weak
- Clipping artefact partially explains translation signal
- Requires nuanced interpretation and possibly further experiments

## 13. Analysis Plan

1. **Data Generation**: Regenerate same DGP as parent (seed=42, same functions, lambdas, reps). Total 120,000 transitions.
2. **Raw TV Computation**: Compute kNN TV at k=5,10,20,50 for each transition set.
3. **Permutation Bias Estimation**: For each lambda/function/kNN scale, permute actions 1000 times, compute TV, take mean.
4. **Bias Correction**: TV_corrected = max(0, TV_raw - perm_mean).
5. **Toroidal Wrapping**: Wrap coordinates modulo 1, recompute TV.
6. **Frequency Baseline**: Compute marginal P(S_{t+1}), compute TV under independence.
7. **Gaussian Baseline**: Generate same DGP with single Gaussian noise, compute TV.
8. **Statistical Tests**: Spearman correlation on bias-corrected TV, two-way ANOVA, paired t-tests for clipping sensitivity.
9. **Controls**: Verify positive, null, bias uniformity, toroidal, frequency controls.
10. **Reporting**: Report raw and bias-corrected results, effect sizes, confidence intervals.

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.

## 16. Parent Handoff Inheritance

### Established (from parent carry_forward)
- kNN-based TV estimator works in 10D [0,1]^10 without distance degeneracy
- Translation-type dynamics produce strong TV signal in 10D non-Gaussian DGP (rho=1.0, d=9.11)
- Rotation-type dynamics produce moderate TV signal (rho=0.83)
- Scaling-type dynamics produce negligible TV signal (rho=-0.07)
- kNN TV finite-sample bias floor ~0.52 at lambda=0 across all kNN scales
- Aggregate Spearman rho=1.0 holds but driven by translation dominance

### Rejected (from parent)
- Uniform TV generalization from 2D Gaussian to 10D non-Gaussian settings (decisively falsified)
- Producer's positive control redefinition (invalid under frozen spec)

### Unknown (from parent)
- Whether bias-corrected kNN TV preserves aggregate monotonic rho=1.0
- Whether clipping artefact quantitatively explains translation's strong signal
- Whether scaling failure replicates under alternative parameterizations
- Whether Gaussian vs non-Gaussian noise comparison shows difference
- Whether frequency baseline explains ~0.52 TV floor
- Whether kNN TV remains calibrated at >10D
- Whether real Web transitions show action-dependent structure
- Whether rotation's non-monotonic dip is noise or genuine

### Do Not Assume (from parent)
- Do not assume TV works on real Web transitions (all evidence synthetic)
- Do not assume C-WEB-DYNAMICS is established (claim ceiling bounded)
- Do not assume product deployment readiness
- Do not assume aggregate rho=1.0 means TV works uniformly
- Do not assume bias floor ~0.52 is ignorable
- Do not assume clipping to [0,1] is neutral
- Do not assume frozen decision rule thresholds are well-calibrated
- Do not assume effect sizes generalize to real Web
- Do not assume combined noise robustness
- Do not assume multi-scale monotonicity is fully robust
