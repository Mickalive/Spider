# EXP-FRONTIER-33932275169 — Non-Affine (Quadratic) Validation Report

## Executive Summary

**Decision: FALSIFIED-IN-SETTING** — The frozen decision rule triggers falsification because the two-way ANOVA interaction term is significant (F=32.5064, p=0.0), violating the function-invariance condition. However, this interaction is **expected by design**: the 3 quadratic functions have intentionally different Var_a values (0.125, 0.3125, 0.1875), and the parent handoff explicitly warns "do not assume the ANOVA interaction failure is evidence against the metric."

**Key finding:** TV distance shows perfect monotonic scaling with lambda across all 3 quadratic functions (Spearman rho=1.0, p<0.001), with large effect sizes (Cohen's d=7.85). The metric generalizes beyond affine functions to non-affine quadratic transitions. The ANOVA interaction reflects genuine differences in function-specific Var_a, not metric failure.

## 1. Experiment Overview

- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure)
- **Question**: Does TV distance detect lambda-scaling in non-affine (quadratic) synthetic Web transitions?
- **Hypothesis**: Both TV distance and variance-of-means scale monotonically with lambda for quadratic functions
- **Falsifier**: Any of: aggregate Spearman rho < 0.65, positive control failure, null control failure, significant ANOVA interaction, het rho < 0.5

## 2. Raw Evidence

### 2.1 Analytical Ground Truth

| Function | Var_a | TV at lambda=1 | E_S[f(S,click)] | E_S[f(S,fill)] | E_S[f(S,submit)] | E_S[f(S,navigate)] |
|----------|-------|----------------|------------------|----------------|-------------------|---------------------|
| 42       | 0.125 | 0.7667         | 4.50             | 4.00           | 5.00              | 4.50                |
| 43       | 0.3125| 0.7500         | 3.50             | 4.00           | 4.50              | 3.00                |
| 44       | 0.1875| 0.5333         | 4.50             | 3.50           | 4.50              | 4.50                |

All functions are non-affine (quadratic in s), non-permutation (generally non-injective), and have analytically verifiable Var_a > 0.

### 2.2 TV Distance by Lambda (Aggregate)

| Lambda | TV (mean ± std) | Het (mean ± std) |
|--------|-----------------|-------------------|
| 0.0    | 0.1498 ± 0.0238 | 0.0523 ± 0.0378  |
| 0.2    | 0.2083 ± 0.0329 | 0.0473 ± 0.0445  |
| 0.4    | 0.3246 ± 0.0558 | 0.0835 ± 0.0450  |
| 0.6    | 0.4438 ± 0.0646 | 0.0841 ± 0.0546  |
| 0.8    | 0.5810 ± 0.0834 | 0.1929 ± 0.0854  |
| 1.0    | 0.7028 ± 0.0968 | 0.2417 ± 0.1524  |

TV distance shows strict monotonic increase with lambda. The effect is large: Cohen's d = 7.85 (TV) and 1.71 (het) comparing lambda=1 vs lambda=0.

### 2.3 Per-Function TV by Lambda

| Lambda | Func 42 | Func 43 | Func 44 |
|--------|---------|---------|---------|
| 0.0    | 0.1524  | 0.1410  | 0.1560  |
| 0.2    | 0.2187  | 0.2218  | 0.1845  |
| 0.4    | 0.3673  | 0.3466  | 0.2601  |
| 0.6    | 0.4918  | 0.4777  | 0.3620  |
| 0.8    | 0.6463  | 0.6276  | 0.4692  |
| 1.0    | 0.7760  | 0.7619  | 0.5704  |

All 3 functions show perfect monotonic TV scaling (Spearman rho=1.0 for each). Function 44 has lower absolute TV values due to its lower analytical TV ceiling (0.5333 vs 0.7667/0.7500).

## 3. Statistical Tests

### 3.1 Primary Test: Spearman Correlation (TV)

- **Aggregate rho**: 1.0000 (p < 0.001, one-sided)
- **Threshold**: rho >= 0.65, p < 0.05
- **Result**: PASS

### 3.2 Per-Function Spearman (TV)

| Function | rho | p (one-sided) |
|----------|-----|---------------|
| 1 (seed=42) | 1.0000 | < 0.001 |
| 2 (seed=43) | 1.0000 | < 0.001 |
| 3 (seed=44) | 1.0000 | < 0.001 |

All functions show perfect monotonic scaling.

### 3.3 Secondary Test: Spearman Correlation (het)

- **Aggregate rho**: 0.9429 (p = 0.0024, one-sided)
- **Threshold**: rho >= 0.5
- **Result**: PASS

### 3.4 Two-Way ANOVA

| Source | F | p | df |
|--------|---|---|-----|
| Lambda | 2174.30 | 0.0 | 5 |
| Function | 330.13 | 0.0 | 2 |
| Lambda × Function | 32.51 | 0.0 | 10 |
| Residual | — | — | 162 |

- **Model R²**: 0.9865
- **Interaction pass**: FAIL (p = 0.0 < 0.05)

**Important context**: The significant interaction is expected by design. The 3 functions have intentionally different Var_a values (0.125, 0.3125, 0.1875), producing different TV scaling slopes. This is signal (functions have different sensitivity to lambda), not pipeline failure. The parent handoff explicitly states: "do not assume the ANOVA interaction failure is evidence against the metric."

### 3.5 Permutation Tests

- **Lambda=0 null control**: mean p = 0.508 (PASS, p > 0.05)
- **Lambda=1 positive control**: all functions above 80% of analytical threshold (PASS)

### 3.6 Effect Sizes

- **Cohen's d (TV, lambda=1 vs 0)**: 7.8471 (very large)
- **Cohen's d (het, lambda=1 vs 0)**: 1.7057 (large)
- **TV CV at lambda=1**: 0.1377 (valid, < 0.5)

## 4. Control Assessment

| Control | Status | Evidence |
|---------|--------|----------|
| Positive control | PASS | All 3 functions: TV > 80% analytical threshold at lambda=1 |
| Null control | PASS | Permutation test mean p=0.508 at lambda=0 |
| Permutation null | PASS | Analytically verified |
| Function invariance | FAIL | ANOVA interaction p=0.0 (expected by design) |

## 5. Decision Rule Evaluation

Frozen decision rule requires ALL of:
1. Aggregate Spearman rho(TV, lambda) >= 0.65, p < 0.05 → **PASS** (rho=1.0)
2. Positive control passes → **PASS**
3. Null control passes → **PASS**
4. No significant function x lambda interaction (p > 0.05) → **FAIL** (p=0.0)
5. Variance-of-means monotonic (rho >= 0.5) → **PASS** (rho=0.9429)
6. No pipeline errors → **PASS**

**Result**: FALSIFIED-IN-SETTING due to condition 4 failure.

## 6. Interpretation

### 6.1 What This Experiment Establishes

Despite the formal falsification, the scientific content is clear:

1. **TV distance generalizes to non-affine functions**: Perfect monotonic scaling (rho=1.0) across all 3 quadratic functions demonstrates the metric is not limited to affine function classes.

2. **Effect sizes are large**: Cohen's d=7.85 for TV and 1.71 for het indicate strong, detectable action-dependent structure in quadratic transitions.

3. **Positive and null controls pass**: The pipeline correctly detects structure when present (lambda=1) and does not produce false positives (lambda=0).

4. **Variance-of-means also generalizes**: Secondary metric shows monotonic scaling (rho=0.9429), though less sensitive than TV.

### 6.2 The ANOVA Interaction Issue

The frozen decision rule's ANOVA interaction condition is too conservative for heterogeneous function classes. When functions are designed to have different Var_a values, a significant interaction is expected and informative—it tells us that different Web regions may have different sensitivity to action-dependence. This is useful signal, not a metric failure.

The parent handoff's `do_not_assume` explicitly warns against interpreting ANOVA interaction as evidence against the metric. The frozen decision rule was carried forward from the parent experiment where it was already identified as mis-calibrated.

### 6.3 Comparison with Parent Experiment (Affine Functions)

| Metric | Parent (Affine) | This Experiment (Quadratic) |
|--------|-----------------|-----------------------------|
| TV Spearman rho | 1.0 | 1.0 |
| Het Spearman rho | 0.9762 | 0.9429 |
| Cohen's d (TV) | 13.4 | 7.85 |
| Cohen's d (het) | 1.54 | 1.71 |
| Null control | PASS (p=0.466) | PASS (p=0.508) |
| ANOVA interaction | FAIL (expected) | FAIL (expected) |

TV distance maintains perfect monotonic scaling across both function classes. The smaller Cohen's d for TV in quadratic functions (7.85 vs 13.4) reflects the lower analytical TV ceilings for some quadratic functions (0.5333 for function 44 vs 0.8-1.0 for affine functions).

## 7. Product Consequences

### 7.1 If Decision Were SURVIVES_CURRENT_TEST

TV distance would be validated for broad use in SPIDER's product pipeline for Web-dynamical regime detection. Different Web regions with different action-dependence levels could be detected through distributional analysis.

### 7.2 Actual Decision: FALSIFIED-IN-SETTING

The formal falsification constrains the decision rule, not the metric. The scientific evidence strongly supports TV distance generalizing to non-affine functions. The Frontier lane should:

1. **Retain TV distance as primary metric** — the scientific evidence is overwhelming despite the formal falsification
2. **Relax the ANOVA interaction condition** for future experiments with heterogeneous function classes
3. **Proceed to test on real or realistic Web data** — the synthetic-to-real gap remains the dominant unknown

## 8. Validity Threats

1. **Synthetic-to-real gap**: All evidence is from known-coefficient quadratic DGPs. Real Web transitions may have different structure.
2. **ANOVA interaction condition**: The frozen decision rule's function-invariance condition is too conservative for heterogeneous function classes. This is a known issue from the parent experiment.
3. **Sampling noise at lambda=0**: TV is elevated (0.1498 vs theoretical 0) due to finite sample size (500 transitions per cell). Permutation test confirms this is not statistically significant.

## 9. Artifacts

- `analyze.py`: Frozen analysis code (SHA256: bc24c3a8...)
- `raw_tables.json`: Per-replication per-function per-lambda TV and het values (SHA256: e90d1aab...)
- `frequency_baseline.json`: Marginal next-state distributions at all lambda levels (SHA256: ed58b31b...)
- `analytical_ground_truth.json`: Analytical Var_a, TV, and action-conditional distributions (SHA256: 34859d47...)
