# EXP-FRONTIER-34121473072 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34121473072
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-07
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-FRONTIER-34065969836 (FALSIFIED-IN-SETTING)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does bias-corrected kNN TV (permutation-null subtraction removing the ~0.52 finite-sample floor) recover uniform function invariance in 10D non-Gaussian spaces, or does the scaling function failure persist after bias correction — and does the clipping artefact (~50% at lambda=1) quantitatively explain translation's strong signal (separation=0.201) vs scaling's weakness (separation=0.022)?

## 3. Motivation

### What the parent experiment established (EXP-FRONTIER-34065969836)

The parent experiment tested whether TV distance generalizes from 2D Gaussian to 10D non-Gaussian settings. It produced:

**Established:**
- kNN-based TV works in 10D [0,1]^10 without distance degeneracy (fraction finite distances = 1.0)
- Translation-type dynamics produce strong TV signal: Spearman rho=1.0, Cohen's d=9.11, separation=0.201
- Rotation-type dynamics produce moderate TV signal: rho=0.83, d=2.09, separation=0.058
- Scaling-type dynamics produce negligible TV signal: rho=-0.07, d=0.85, separation=0.022
- Aggregate Spearman rho=1.0 but driven by translation dominance
- Function invariance decisively fails (ANOVA p~1e-30)

**Rejected:**
- Uniform TV generalization from 2D Gaussian to 10D non-Gaussian — function invariance failure
- Positive control redefinition (tv_at_1 > tv_at_0 instead of permutation null test) — spec requires permutation null p<0.05

**Unknown (from parent audit):**
- Whether kNN bias floor ~0.52 is ignorable — it exceeds the entire dynamic range (0.094 aggregate)
- Whether clipping to [0,1] at lambda=1 ~50% creates edge mass that inflates TV at high lambda differentially by function
- Whether frequency baseline P(S_{t+1}) explains the ~0.52 TV floor at lambda=0
- Whether Gaussian vs non-Gaussian noise comparison would show scaling recovers under Gaussian noise

**Do Not Assume (from parent audit):**
- Do not assume aggregate Spearman rho=1.0 means TV works uniformly — it is weighted average of translation (rho=1.0), rotation (rho=0.83), and scaling (rho=-0.07)
- Do not assume kNN TV bias floor ~0.52 is ignorable — it exceeds the entire dynamic range
- Do not assume clipping to [0,1] is neutral — ~50% of transitions clipped at lambda=1
- Do not assume frozen decision rule thresholds are well-calibrated — positive control threshold >=0.1 is below noise floor (~0.52)

### Why this experiment is different

The parent experiment used raw kNN TV without bias correction. The audit identified three critical validity threats:

1. **kNN bias floor ~0.52**: At lambda=0 (no action-dependence), TV is ~0.52 instead of 0. This floor exceeds the entire dynamic range (0.094 aggregate, 0.201 translation, 0.022 scaling). The entire observed signal may be within the noise floor.

2. **Clipping artefact**: ~50% of transitions are clipped to [0,1] at lambda=1. Clipping creates edge mass that inflates TV at high lambda. Differential clipping by function family may explain translation's strong signal vs scaling's weakness.

3. **Missing baselines**: Frequency baseline P(S_{t+1}) and Gaussian noise baseline were specified in the parent preregistration but never computed.

This experiment addresses all three by:
- Applying permutation-null bias subtraction at each lambda/function/kNN scale
- Testing toroidal wrapping as alternative to clipping
- Computing frequency and Gaussian noise baselines
- Using 1000 permutations per cell (vs parent's 200)

If bias correction rescues scaling and improves function invariance, the parent's per-function heterogeneity was estimator artefact. If not, scaling genuinely lacks signal and the Frontier lane must pivot.

## 4. Hypotheses

### H1: Bias-Corrected Monotonicity
After permutation-null bias subtraction, bias-corrected TV still scales monotonically with lambda. Aggregate Spearman rho(bias_corrected_TV, lambda) >= 0.65, p < 0.05 one-sided.

### H2: Bias-Corrected Function Invariance
After bias subtraction, the per-function heterogeneity is reduced because the bias floor is shared across function families. Two-way ANOVA interaction p > 0.05 on bias-corrected TV.

### H3: Positive Control
After bias correction, TV at lambda=1 remains detectably above zero across all 3 functions (bias-corrected TV > 0, permutation p < 0.05). Bias subtraction does not destroy genuine signal.

### H4: Null Control
After bias correction, TV at lambda=0 is indistinguishable from zero (bias-corrected TV ≈ 0, permutation p > 0.05). Bias subtraction successfully removes the finite-sample floor.

### H5: Clipping Quantification
Toroidal wrapping (modular arithmetic) reduces translation's separation advantage over scaling by >50% compared to clipping. This tests whether clipping differentially inflates translation vs scaling.

### H6: Frequency Baseline
The frequency baseline P(S_{t+1}) explains a substantial fraction (>50%) of the ~0.52 TV floor at lambda=0, confirming that marginal non-uniformity contributes to the bias.

## 5. Data Generation

### 5.1 Synthetic Transition Model

Same as parent: transitions (S_t, A_t, S_{t+1}) where:
- State space: [0,1]^10 continuous
- Action space: 4 actions
- 3 function families: rotation (seed=42), scaling (seed=43), translation (seed=44)
- Mixture-of-3-Gaussians heteroscedastic noise per state dimension

### 5.2 Lambda Levels

Eight conditions (same as parent): 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0

### 5.3 Sample Size

- 500 transitions per lambda level per function per replication (same as parent)
- 10 replications per cell
- Total: 120,000 transitions (same as parent)
- Plus: 1000 permutations per cell for bias floor estimation (240 cells x 1000 = 240,000 permutation samples)

### 5.4 Bias Correction Method

For each lambda level, function family, and kNN scale k:
1. Compute raw kNN TV from observed transitions
2. Compute permutation-null TV: shuffle action labels 1000 times, compute TV for each shuffle
3. Bias_corrected_TV(lambda) = raw_TV(lambda) - mean(permutation_null_TV(lambda))
4. This removes the finite-sample bias floor ~0.52 at lambda=0

### 5.5 Clipping Alternatives

Two boundary treatments:
- **Clipping** (parent method): transitions outside [0,1]^10 are clipped to boundary
- **Toroidal wrapping**: transitions outside [0,1]^10 are wrapped using modular arithmetic: x_wrapped = x - floor(x)

### 5.6 Frequency Baseline

For each lambda level and function:
1. Compute marginal next-state distribution P(S_{t+1}) by averaging across all actions
2. Compute TV between P(S_{t+1} | do(A=click)) and P(S_{t+1} | do(A=fill)) using the marginal as reference
3. This measures how much of the observed TV at lambda=0 is due to marginal non-uniformity

### 5.7 Gaussian Noise Baseline

Same 10D state space with single-Gaussian heteroscedastic noise (not mixture):
- For each state dimension i, noise ~ N(0, sigma_i^2) where sigma_i depends on state
- Compare TV between Gaussian and mixture-of-Gaussians noise at matched lambda levels
- Isolate whether non-Gaussian noise specifically degrades scaling detection

## 6. Measures

### 6.1 Primary Metric
- **bias_corrected_tv_by_lambda**: Bias-corrected kNN TV at each lambda level, averaged across functions and replications, at k=20 (matching parent's primary scale)
- **spearman_rho_bias_corrected**: Spearman correlation between bias_corrected_tv_by_lambda and lambda (n=8, single aggregate comparison)

### 6.2 Secondary Metrics
- Per-function bias-corrected TV at each lambda level
- Per-kNN-scale bias-corrected TV (k=5, 10, 20, 50)
- Bias floor magnitude at lambda=0 (permutation null mean)
- Translation-scaling separation ratio before and after bias correction
- Toroidal vs clipping TV difference per function
- Frequency baseline TV at each lambda level
- Gaussian vs mixture noise TV difference

### 6.3 Comparison Metrics
- Raw (uncorrected) TV from parent EXP-FRONTIER-34065969836 (direct reuse of parent raw_tables.json)

## 7. Null Models

### 7.1 Permutation Null (for bias floor)
1000 permutations per cell: shuffle action labels, recompute TV. Mean permutation TV at each lambda level is the bias floor for subtraction.

### 7.2 Frequency Baseline
TV between action-conditional distributions using marginal P(S_{t+1}) as reference. Expected to explain part of the ~0.52 floor at lambda=0.

### 7.3 Gaussian Noise Baseline
Same DGP with single-Gaussian noise. Tests whether non-Gaussian mixture noise specifically affects scaling detection.

## 8. Statistical Tests

### 8.1 Primary Test
- Spearman rank correlation: rho(bias_corrected_tv, lambda) across 8 lambda levels
- One-sided test: rho > 0
- Aggregate test (single comparison, no Bonferroni): rho >= 0.65, p < 0.05
- For n=8, rho >= 0.65 gives p < 0.05 one-sided

### 8.2 Per-Function Tests
- Per-function Spearman rho on bias-corrected TV
- Bonferroni x3 correction: rho >= 0.83, p < 0.017

### 8.3 Permutation Tests
- At lambda=0: permutation test for bias-corrected TV ≈ 0 (p > 0.05)
- At lambda=1: permutation test for bias-corrected TV > 0 (p < 0.05)

### 8.4 Two-Way ANOVA
- bias_corrected_TV ~ lambda + function + lambda:function
- Non-significant interaction (p > 0.05) supports function invariance
- With 8 levels x 3 functions x 10 reps = 240 observations, adequate residual df

### 8.5 Clipping Comparison
- Paired t-test: TV(clipping) vs TV(toroidal) at lambda=1 for each function
- Effect size: Cohen's d of clipping vs toroidal

### 8.6 Frequency Baseline Comparison
- Correlation between frequency baseline TV and raw TV floor at lambda=0
- Fraction of raw TV at lambda=0 explained by frequency baseline

## 9. Controls

### 9.1 Positive Control (lambda=1)
After bias correction, TV at lambda=1 must be > 0 across all functions (permutation p < 0.05). Verifies bias subtraction does not destroy genuine signal.

### 9.2 Null Control (lambda=0)
After bias correction, TV at lambda=0 must be ≈ 0 (permutation p > 0.05). Verifies bias subtraction removes the finite-sample floor.

### 9.3 Bias Floor Consistency
Permutation null TV at lambda=0 should be consistent across function families (CV < 0.1), confirming the bias floor is shared.

### 9.4 Toroidal Wrapping Sanity Check
TV at lambda=0 with toroidal wrapping should be ≈ 0 (no clipping artefact at lambda=0).

## 10. Validity Threats

### 10.1 Bias Over-Correction
If permutation null overestimates the true bias floor, bias-corrected TV could be negative at lambda=1. Mitigation: flag as MEASUREMENT_INVALID if >10% of bias-corrected TV values are negative at lambda=1.

### 10.2 Permutation Null Variance
With 1000 permutations per cell, the permutation null estimate has SE ≈ sd(permutation_TVs) / sqrt(1000). If variance is high (>0.1), the bias floor estimate is noisy. Mitigation: report permutation null variance; flag MEASUREMENT_INVALID if CV > 0.5 across replications at lambda=0.

### 10.3 Toroidal Wrapping Distortion
Toroidal wrapping changes the geometry of the state space (points near boundary 0 wrap to near boundary 1). This may introduce artefactual structure. Mitigation: compare TV at lambda=0 with toroidal wrapping — should be ≈ 0.

### 10.4 Synthetic-to-Real Gap
Same as parent: findings limited to controlled synthetic DGP.

### 10.5 kNN Scale Sensitivity
Bias correction may behave differently at different kNN scales. Mitigation: test at k=5, 10, 20, 50 and report per-scale results.

### 10.6 Frequency Baseline Interpretation
If frequency baseline explains most of the TV floor, the residual (bias-corrected TV) may have insufficient dynamic range for meaningful function invariance testing. Mitigation: report dynamic range after bias correction and assess whether it supports discriminating tests.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Aggregate Spearman rho(bias_corrected_TV, lambda) >= 0.65, p < 0.05 one-sided
2. Positive control passes: bias-corrected TV > 0 at lambda=1 across all functions
3. Null control passes: bias-corrected TV ≈ 0 at lambda=0 (permutation p > 0.05)
4. Function invariance passes: two-way ANOVA interaction p > 0.05
5. Clipping removal reduces translation's separation advantage over scaling by >50%
6. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Aggregate Spearman rho < 0.65 or p > 0.05
2. Positive control fails
3. Null control fails
4. Function invariance still fails (interaction p < 0.05)
5. Clipping removal does not reduce translation-scaling gap by >50%

### 11.3 MEASUREMENT_INVALID
If:
1. Pipeline errors
2. >10% of bias-corrected TV values negative at lambda=1 (over-correction)
3. Permutation null CV > 0.5 across replications at lambda=0
4. Toroidal wrapping produces TV > 0.1 at lambda=0 (geometry artefact)

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Bias correction rescues function invariance: per-function heterogeneity was estimator artefact (shared bias floor + clipping)
- TV-based regime detection validated for 10D non-Gaussian settings with proper bias correction
- Product lane can integrate bias-corrected TV with calibrated thresholds
- C-WEB-DYNAMICS claim ceiling expanded to 10D non-Gaussian (not just 2D Gaussian)

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Scaling genuinely lacks action-dependent structure detectable by TV
- Bias correction does not rescue scaling or function invariance
- TV limited to translation-like dynamics in high-dimensional non-Gaussian spaces
- Frontier lane must pivot: alternative estimators (KDE, neural density) or real Web data

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Bias correction methodology needs refinement
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Data Generation**: Generate 120,000 transitions using parent's DGP (same seeds, same functions, same noise model)
2. **Raw TV Computation**: Compute kNN TV at k=5,10,20,50 for each cell (reproduce parent's results)
3. **Permutation Null**: For each cell, shuffle action labels 1000 times, compute TV for each shuffle, store full null distribution
4. **Bias Correction**: Subtract permutation null mean from raw TV at each lambda/function/kNN scale
5. **Toroidal Wrapping**: Re-generate transitions with toroidal wrapping instead of clipping; recompute TV
6. **Frequency Baseline**: Compute marginal P(S_{t+1}) TV at each lambda level
7. **Gaussian Noise Baseline**: Generate 10D transitions with single-Gaussian noise; compute TV
8. **Statistical Tests**: Spearman correlation, ANOVA, permutation tests, paired t-tests
9. **Controls**: Verify positive, null, bias floor consistency, toroidal sanity
10. **Reporting**: Report all outcomes with equal prominence

## 14. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for Spearman correlation and t-tests
- `scipy.stats.f_oneway` or `statsmodels` for two-way ANOVA
- `sklearn.neighbors.KDTree` for kNN distance computation
- Standard library only

Code will be committed to `research/experiments/EXP-FRONTIER-34121473072/` before execution.

## 15. Pre-registered Expectations

From parent experiment:
- Raw TV at lambda=0 ≈ 0.52 (bias floor)
- Translation separation = 0.201, scaling separation = 0.022
- Function invariance fails (ANOVA p~1e-30)

Expected after bias correction:
- Bias-corrected TV at lambda=0 ≈ 0 (by construction)
- Bias-corrected TV dynamic range reduced (floor removed, ceiling may also drop)
- If bias floor is shared across functions, function invariance should improve
- If clipping inflates translation more than scaling, toroidal wrapping should reduce the gap

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
