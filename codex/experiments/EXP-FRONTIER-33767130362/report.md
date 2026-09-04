# EXP-FRONTIER-33767130362 — Causal Effect Heterogeneity in Synthetic Web Transitions

## Executive Summary

**Decision: FALSIFIED-IN-SETTING**

The causal effect heterogeneity metric does not detect any lambda-dependent structure in permutation-based synthetic Web transitions. The analytical heterogeneity is exactly 0 for all lambda levels (a mathematical identity), and the Monte Carlo estimates (~0.05) are sampling noise around 0. The positive control fails catastrophically (0/30 measurements above threshold). This falsifies the specific causal heterogeneity metric applied to permutation-based deterministic functions, but does NOT falsify C-WEB-DYNAMICS broadly.

## 1. What Was Tested

**Question:** Does causal effect heterogeneity (variance of expected next-states across actions under do(A_t=a)) increase monotonically with the action-dependence parameter lambda, demonstrating regime-dependent dynamics via direct interventional analysis?

**Hypothesis:** het(lambda) = lambda^2 * Var_a(E_S[f(S,a)]) increases monotonically with lambda.

**Method:** Ground-truth interventional distributions computed analytically from the known DGP. Monte Carlo estimation from 500 transitions per cell. 8 lambda levels x 3 functions x 10 replications = 240 cells.

## 2. Key Finding: Permutation Functions Are Degenerate

The deterministic functions used in this experiment are **permutations** of {0,...,9} for each action. For any permutation pi of {0,...,9}:

```
sum(pi(s)) = sum({0,...,9}) = 45
mean(pi(s)) = 4.5 for ALL actions
```

Therefore:
```
E_S[f(S, a)] = 4.5 for all actions a
Var_a(E_S[f(S, a)]) = 0
het(lambda) = lambda^2 * 0 = 0 for all lambda
```

This is a mathematical identity, not a sampling artifact. The causal heterogeneity metric is well-defined but produces exactly 0 for this function class.

## 3. Numerical Results

### 3.1 Analytical Heterogeneity
All 8 lambda levels: het = 0.000000 (exact)

### 3.2 Monte Carlo Heterogeneity Estimates
| Lambda | Mean Het | Std Het | True Value |
|--------|----------|---------|------------|
| 0.0    | 0.0523   | 0.0371  | 0          |
| 0.1    | 0.0546   | 0.0543  | 0          |
| 0.2    | 0.0437   | 0.0322  | 0          |
| 0.3    | 0.0586   | 0.0332  | 0          |
| 0.4    | 0.0647   | 0.0536  | 0          |
| 0.5    | 0.0544   | 0.0333  | 0          |
| 0.7    | 0.0537   | 0.0336  | 0          |
| 1.0    | 0.0570   | 0.0513  | 0          |

All values are sampling noise around 0. No lambda level shows signal above noise.

### 3.3 Primary Statistical Test
- **Aggregate Spearman rho(het, lambda):** 0.3333
- **Aggregate Spearman p (one-sided):** 0.2099
- **Threshold:** rho >= 0.65, p < 0.05
- **Result:** FAILS (rho too low, p not significant)

### 3.4 Per-Function Spearman
| Function | Seed | rho | p (one-sided) | Bonferroni threshold |
|----------|------|-----|---------------|---------------------|
| 1        | 42   | -0.476 | 0.884 | 0.0167 |
| 2        | 43   | 0.762  | 0.014 | 0.0167 |
| 3        | 44   | 0.238  | 0.285 | 0.0167 |

Function 2 shows apparent monotonicity (rho=0.76), but this is sampling noise — the true heterogeneity is 0 for all functions. Functions 1 and 3 show no trend.

### 3.5 Two-Way ANOVA (240 observations)
| Effect | F | p | df |
|--------|---|---|-----|
| Lambda | 0.564 | 0.784 | 7 |
| Function | 0.263 | 0.769 | 2 |
| Interaction | 0.652 | 0.819 | 14 |
| Residual | — | — | 216 |

No significant effects. Model R^2 = 0.059.

### 3.6 Effect Size
- **Cohen's d (lambda=1 vs lambda=0):** 0.1046 (very small)

## 4. Control Results

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| Positive (lambda=1, het>=0.5) | het >= 0.5 | het_mean = 0.057 | **FAIL** |
| Null (lambda=0, het ~ 0) | p > 0.05 | p_mean = 0.466 | PASS |
| Permutation null | het ~ 0 | Analytical het = 0 | PASS |
| Function invariance | interaction p > 0.05 | p = 0.819 | PASS |
| Monotonicity | monotonically increasing | Not monotonic | **FAIL** |

The positive control failure is the most informative result: even at lambda=1 (fully action-determined transitions), the heterogeneity is ~0.057, far below the 0.5 threshold. This confirms the permutation degeneracy.

## 5. Why This Happens

The parent experiment (EXP-FRONTIER-33528827909) used **prediction accuracy decomposition**, which IS sensitive to permutation-based structure. Rules that map (state, action) to next-state can achieve 100% accuracy at lambda=1 even when the mean is preserved, because accuracy measures point predictions, not distributional means.

The causal heterogeneity metric measures **variance of expected next-states across actions**. For permutations, all actions have the same expected next-state (4.5), so the variance is 0. The metric is blind to the structure that prediction accuracy detects.

## 6. Implications

### What this falsifies
- The specific causal heterogeneity metric (Var_a(E_S[f(S,a)])) applied to permutation-based deterministic functions
- The hypothesis that this metric can detect lambda-dependent dynamics in this function class

### What this does NOT falsify
- C-WEB-DYNAMICS broadly (the claim that Web transitions contain dynamical structure)
- Prediction accuracy as a detection method (the parent experiment's descriptive finding stands)
- Causal intervention as a general approach (only this specific metric is degenerate)
- The existence of regime-dependent dynamics in synthetic or real Web transitions

### What the next experiment should do
1. Use **non-permutation deterministic functions** where E_S[f(S,a)] varies across actions (e.g., affine functions, state-dependent shifts, or action-dependent offsets)
2. Alternatively, use a different causal metric that captures distributional structure beyond means (e.g., variance of P(S_{t+1}|do(A=a)) as a full distribution)
3. The parent experiment's prediction accuracy approach remains viable with more lambda levels and replications

## 7. Methodology Notes

- **Pipeline:** No errors. status=COMPLETE.
- **Sample size:** 120,000 transitions total (8 x 3 x 10 x 500). Adequate for the metric.
- **Statistical power:** With 8 lambda levels and 10 replications, the Spearman test has adequate power for rho >= 0.65 if the effect exists. The effect does not exist for this function class.
- **Reproducibility:** Frozen seed=42, deterministic functions via numpy RandomState. Results are reproducible.

## 8. Decision Justification

**FALSIFIED-IN-SETTING** because:
1. Aggregate Spearman rho = 0.33 < 0.65 threshold (FAILED)
2. Positive control fails: 0/30 measurements at lambda=1 have het >= 0.5 (FAILED)
3. The failure is explained by a mathematical property of permutation functions, not by insufficient power or pipeline error

The falsification is bounded: it applies to this specific metric applied to this specific function class. The broader claim C-WEB-DYNAMICS remains HYPOTHESIS.
