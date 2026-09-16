# EXP-FRONTIER-34773875458 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-34773875458
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does TV detection of translation-like action-dependent structure survive non-stationary dynamics where different page types have different transition functions — the defining property of real Web data that all five prior synthetic Frontier experiments lack?

## 3. Motivation

Five consecutive Frontier experiments on synthetic data converge on the same finding:
- EXP-FRONTIER-33528827909: Rule-memory difference scales monotonically with lambda (rho=1.0), but function invariance fails at low lambda
- EXP-FRONTIER-34065969836: kNN TV fails scaling (rho=-0.12) but detects rotation (rho=0.93)
- EXP-FRONTIER-34121473072: Bias-corrected kNN TV confirms scaling failure persists
- EXP-FRONTIER-34538185726: KDE partially detects scaling (rho=0.71) but fails rotation (rho=0.29)
- EXP-FRONTIER-34729238832: PCA dimensionality reduction fails to rescue simultaneous detection

Translation is the only consistently detectable signal across all experiments. All five experiments use **stationary** synthetic DGPs (i.i.d. transitions from a single function family). Real Web data is fundamentally **non-stationary**: different pages have different dynamics (forms vs navigation vs buttons), different noise levels, and different state spaces.

The parent handoff (EXP-FRONTIER-34729238832) identifies the dominant unknown:
> "Whether real Web DOM transitions exhibit translation-like, scaling-like, or rotation-like action-dependent structure — ALL Frontier evidence is synthetic."

And recommends:
> "Testing real Web data is the minimum next experiment to determine whether C-WEB-DYNAMICS has any empirical grounding."

However, no real Web transition dataset exists in the repository, and building browser-based collection infrastructure is beyond a single Frontier experiment scope (Playwright/Selenium not available in the environment). This experiment takes the smallest intermediate step: testing whether TV detection survives **non-stationary dynamics**, which is the key property of real Web data that all prior experiments lacked.

**Key improvements over parent experiment (addressing audit findings):**
1. **Bias-corrected TV** (parent audit V2): Primary metric is observed_TV minus perm_mean_TV at lambda=0, eliminating bias floor inflation
2. **Fisher combined p-values** (parent audit V8): Permutation null uses Fisher combining instead of mean-of-p-values aggregation
3. **Independent seeds per cell** (parent audit V7): Seed incorporates lambda_idx to ensure independence across lambda levels

If detection survives non-stationarity, the synthetic-to-real gap may be smaller than feared, justifying investment in real data collection. If detection fails, non-stationarity is a fundamental barrier, and the synthetic experiments are uninformative about real Web dynamics.

## 4. Hypotheses

### H1: Non-Stationary Detection
TV_max on non-stationary pooled data shows monotonic scaling with lambda: Spearman rho(bias_corrected_TV, lambda) >= 0.5.

### H2: Bounded Degradation
Detection degrades under non-stationarity but remains useful: rho_degradation (stationary rho minus non-stationary rho) < 0.4.

### H3: Positive Control
At lambda=1, bias_corrected_TV >= 0.001 in non-stationary condition across all replications (detection survives mixing of heterogeneous page types).

### H4: Null Control
At lambda=0, Fisher combined permutation p > 0.05 in non-stationary condition (no false positive under non-stationary noise).

### H5: Page-Type Invariance
No significant page_type x lambda interaction in non-stationary condition (two-way ANOVA p > 0.05), indicating detection is not driven by a single dominant page type.

## 5. Data Generation

### 5.1 Stationary Condition (Baseline)

Identical to EXP-FRONTIER-34061241004 (Web-faithful TV):
- 3 function families: rotation (seed=42), scaling (seed=43), translation (seed=44)
- 8 lambda levels: 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0
- Heteroscedastic Gaussian noise: sigma = SIGMA_BASE * (1 + BETA * ||s - center||)
- SIGMA_BASE = 0.05, BETA = 0.5, center = (0.5, 0.5)
- 200 transitions per cell (function x lambda)
- 5 replications per cell

### 5.2 Non-Stationary Condition

8 page types with different dynamics, cycling deterministically:

| Page Type | Function | Seed | Noise Level | Center |
|-----------|----------|------|-------------|--------|
| 0 | rotation | 42 | low (0.05) | (0.5, 0.5) |
| 1 | scaling | 43 | low (0.05) | (0.5, 0.5) |
| 2 | translation | 44 | low (0.05) | (0.5, 0.5) |
| 3 | rotation | 42 | high (0.10) | (0.5, 0.5) |
| 4 | scaling | 43 | high (0.10) | (0.5, 0.5) |
| 5 | translation | 44 | high (0.10) | (0.5, 0.5) |
| 6 | rotation | 42 | low (0.05) | (0.3, 0.7) |
| 7 | scaling | 43 | low (0.05) | (0.3, 0.7) |

Page type assignment: `type = (transition_index // 250) mod 8` within each lambda level.

Each page type generates 250 transitions per lambda level, yielding 2000 total transitions per lambda level (pooled across 8 types).

8 lambda levels x 2000 transitions x 5 replications = 80,000 total non-stationary transitions.

### 5.3 Function Implementations

Reuse exact function implementations from EXP-FRONTIER-34061241004:
- `rotation_func(s, action_idx)`: Rotation by theta[action_idx] around center + offset
- `scaling_func(s, action_idx)`: Scaling by SCALE[action_idx] around center + offset
- `translation_func(s, action_idx)`: Translation by T[action_idx] + sinusoidal perturbation

Parameters (frozen from EXP-FRONTIER-34061241004):
- THETA = [0, pi/4, pi/2, 3*pi/4]
- OFFSET_A = [[0.1,0], [0,0.1], [-0.1,0], [0,-0.1]]
- SCALE = [[1.2,1.2], [0.8,1.2], [1.2,0.8], [0.8,0.8]]
- OFFSET_B = [[0.05,0.05], [-0.05,0.05], [0.05,-0.05], [-0.05,-0.05]]
- T_C = [[0.15,0], [0,0.15], [-0.15,0], [0,-0.15]]
- ALPHA_C = [0.1, 0.1, 0.1, 0.1]

### 5.4 Lambda Generation

For each transition:
1. Draw current state s ~ Uniform([0,1]^2)
2. Draw action a_idx ~ Uniform({0,1,2,3})
3. Determine page type from transition index
4. With probability lambda: s_next = func(s, a_idx) + noise(page_type)
5. With probability (1-lambda): s_next ~ Normal(center, SIGMA_BASE^2 * I_2)
6. Clip s_next to [0,1]

### 5.5 Seed Independence (Addressing Parent Audit V7)

To ensure independent transitions per cell, use unique seed per cell:
```
cell_seed = func_seed * 100000 + lambda_idx * 1000 + rep_idx * 10 + BASE_SEED
```
where BASE_SEED = 42, lambda_idx is the index into LAMBDA_LEVELS (0-7), and rep_idx is the replication index (0-4).

This ensures different lambda levels within the same function/replication use independent RNG streams, unlike the parent experiment which reused seeds across lambda levels.

## 6. Measures

### 6.1 TV Distance (Primary)
- Compute empirical P(S_{t+1} | A=a) using 20x20 grid binning (400 bins)
- TV_max = max_{a,a'} (1/2) sum |P(S|a) - P(S,a')| over all action pairs
- Computed on pooled transitions within each lambda level (non-stationary) or cell (stationary)

### 6.2 Bias-Corrected TV (Primary Metric)
- Compute perm_mean_TV at lambda=0: mean TV across 200 permutations with shuffled action labels
- bias_corrected_TV = max(0, observed_TV - perm_mean_TV)
- This eliminates the bias floor identified in parent audit V2 (raw TV at lambda=0 was 0.32 in 2D, inflating all measurements)

### 6.3 Permutation Null with Fisher Combining
- Shuffle action labels within each page type (preserving page-type structure)
- Recompute bias-corrected TV on shuffled data
- N_perm = 200 per cell (minimum; increase to 500 if computational budget allows)
- Per-function Fisher combined p-value: F = -2 * sum(ln(p_i)) ~ chi^2(2k) where k is number of replications
- Combined p-value across functions: Fisher combine per-function p-values
- This addresses parent audit V8 (mean-of-p-values aggregation is invalid)

### 6.4 Frequency Baseline
- Compute marginal P(S_{t+1}) pooled across all actions
- TV between marginal and each action-conditional distribution
- Mean TV across actions as frequency baseline

### 6.5 Per-Page-Type TV (Exploratory)
- Compute bias_corrected_TV for each page type separately (within-type stationary analysis)
- Compare per-type TV to pooled non-stationary TV
- Identifies which page types contribute most/least to pooled signal

## 7. Statistical Tests

### 7.1 Primary: Spearman Correlation
- rho(bias_corrected_TV, lambda) across 8 lambda levels
- One-sided test: rho > 0
- Bonferroni correction: x1 (single primary comparison per condition)

### 7.2 Degradation Test
- rho_degradation = rho_stationary - rho_non_stationary
- Paired comparison: same lambda levels, different stationarity conditions
- Threshold: rho_degradation < 0.4

### 7.3 Fisher Combined Permutation Test
- At lambda=0: Fisher combined p > 0.05 (null control)
- At lambda=1: Fisher combined p < 0.05 (positive control confirmation)
- N >= 200 permutations per cell

### 7.4 Two-Way ANOVA (Non-Stationary)
- bias_corrected_TV ~ lambda + page_type + lambda:page_type
- Non-significant interaction (p > 0.05) supports page-type invariance
- Note: 8 page types x 8 lambda levels = 64 cells, estimable with 5 replications per cell

### 7.5 Effect Size
- Cohen's d for bias_corrected_TV at lambda=0 vs lambda=1 in non-stationary condition
- Threshold: d > 1.0 (large effect)

## 8. Controls

### 8.1 Positive Control (lambda=1, Non-Stationary)
- bias_corrected_TV >= 0.001 across all replications
- Verifies: detection survives mixing of 8 heterogeneous page types at maximal signal

### 8.2 Null Control (lambda=0, Non-Stationary)
- Fisher combined permutation p > 0.05
- Verifies: no false positive under non-stationary noise distributions

### 8.3 Stationary Replication Control
- Stationary condition replicates EXP-FRONTIER-34061241004 findings
- rho_stationary >= 0.9 (expected: rho=1.0 based on prior result)
- Verifies: baseline measurement is reproducible

### 8.4 Per-Page-Type Control
- Each page type individually shows monotonic TV scaling (rho >= 0.5 per type)
- Verifies: each page type has detectable action-dependent structure before pooling

## 9. Validity Threats

### 9.1 Sample Size
With 2000 transitions per lambda level in non-stationary condition (~250 per page type), TV estimation on 400-bin grid has adequate support. Monte Carlo SE ~ sqrt(1/250) ~ 0.06 per page type. With 8 types pooled, SE ~ 0.02. Power for rho >= 0.5 with 8 lambda levels is > 0.95 (based on prior experiments).

### 9.2 Page-Type Switching Frequency
Switching every 250 transitions creates 8 blocks per lambda level. If switching is too fast (fewer transitions per block), within-block TV estimation degrades. 250 transitions per block is adequate for 400-bin TV (0.625 transitions per bin per block). If needed, increase to 500 transitions per block (4000 total per lambda level).

### 9.3 Pooled TV Interpretation
Pooled TV across page types measures average action-dependent structure. If page types have opposing dynamics (e.g., rotation pushes state left, scaling pushes state right), pooling could cancel out structure. The 8 page types are chosen to have complementary (not opposing) dynamics to minimize this risk.

### 9.4 Synthetic-to-Real Gap Persists
This experiment tests non-stationarity, not all aspects of the synthetic-to-real gap. Real Web data also has continuous high-dimensional state spaces, non-Gaussian noise, temporal correlations, and missing data. This experiment isolates one dimension (non-stationarity) while holding others constant.

### 9.5 Multiple Comparisons
Primary test is a single Spearman correlation per condition (2 conditions total). Bonferroni correction is x1 for each condition. Exploratory per-page-type tests are labeled as such and cannot support confirmatory claims.

### 9.6 Bias Floor Mitigation (Addressing Parent Audit V2)
Raw TV has bias floor ~0.32 in 2D at lambda=0. Bias-corrected TV (observed - perm_mean) should be near zero at lambda=0, making positive control meaningful. If bias-corrected TV at lambda=0 remains > 0.01, the bias correction is insufficient and MEASUREMENT_INVALID.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST
If ALL of:
1. rho(bias_corrected_TV, lambda) >= 0.5 in non-stationary condition (one-sided p < 0.05)
2. rho_degradation < 0.4
3. Positive control passes (bias_corrected_TV >= 0.001 at lambda=1)
4. Null control passes (Fisher combined p > 0.05 at lambda=0)
5. No significant page_type x lambda interaction (ANOVA p > 0.05)
6. No pipeline errors

### 10.2 FALSIFIED-IN-SETTING
If ANY of:
1. rho < 0.5 in non-stationary condition
2. rho_degradation >= 0.4
3. Positive control fails
4. Null control fails
5. Significant page_type x lambda interaction (p < 0.05)

### 10.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent TV computation
2. CV across replications > 0.5 at lambda=1 in non-stationary condition
3. Fewer than 2000 transitions per lambda level collected
4. Bias-corrected TV at lambda=0 > 0.01 (bias correction insufficient)

## 11. Expected Outcomes

### 11.1 Positive Result (SURVIVES_CURRENT_TEST)
- Non-stationarity is not a fundamental barrier to TV detection
- The synthetic-to-real gap may be smaller than feared
- Justify investment in real Web data collection infrastructure
- SPIDER should proceed to browser-based transition recording
- The translation-detection finding generalizes beyond stationary DGPs

### 11.2 Negative Result (FALSIFIED-IN-SETTING)
- Non-stationarity degrades TV detection below useful levels
- The synthetic-to-real gap is fundamental, not just representational
- All five prior synthetic experiments are uninformative about real Web dynamics
- Frontier should abandon density-divergence approach for real Web data
- Pivot to per-page-type estimation, causal factorization, or information-theoretic measures

### 11.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging
- Not scientific evidence for or against
- Re-run with corrected infrastructure

## 12. Analysis Plan

1. **Data Generation**: Generate stationary and non-stationary transitions using frozen parameters with independent seeds per cell
2. **TV Computation**: Compute raw TV_max for each condition at each lambda level
3. **Bias Correction**: Compute perm_mean_TV at lambda=0, subtract from all TV values
4. **Permutation Tests**: Run 200 permutations per cell, compute Fisher combined p-values
5. **Spearman Correlation**: Compute rho and p-value for each condition on bias-corrected TV
6. **Degradation**: Compute rho_degradation between conditions
7. **ANOVA**: Two-way ANOVA on non-stationary data (lambda x page_type)
8. **Controls**: Verify all positive/null/replication controls
9. **Exploratory**: Per-page-type TV analysis
10. **Reporting**: Report all outcomes with equal prominence

## 13. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for Spearman correlation and Fisher combined p-values
- `statsmodels` for two-way ANOVA
- Standard library only (no custom estimators)

Code will be committed to `research/experiments/EXP-FRONTIER-34773875458/` before execution.

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
