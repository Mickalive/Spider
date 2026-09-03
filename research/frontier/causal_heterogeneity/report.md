# EXP-FRONTIER-33767130362 — Causal Effect Heterogeneity in Synthetic Web Transitions

## Executive Summary

**Decision: FALSIFIED-IN-SETTING**

The causal effect heterogeneity metric (variance of expected next-states across actions under do(A_t=a)) does **not** increase monotonically with lambda when applied to permutation-based deterministic functions. The aggregate Spearman rho = 0.33 (p_one_sided = 0.21), failing the threshold of rho >= 0.65 with p < 0.05.

**Root cause**: Permutation functions are mathematically degenerate for this metric. For any permutation of {0,...,9}, the mean is always 4.5. Therefore E_S[f(S, a)] = 4.5 for all actions, making Var_a(E_S[f(S, a)]) = 0 and het(lambda) = 0 for all lambda. The Monte Carlo estimates (~0.04-0.07) are sampling noise around the true value of 0.

This is a **scientific negative**, not an infrastructure failure. The pipeline executed correctly.

## 1. Analytical Result

The preregistration predicted:

> het(lambda) = lambda^2 * Var_a(E_S[f(S, a)])

This formula is correct. However, for permutation functions:
- E_S[f(S, a)] = (1/10) * sum of permuted values = (1/10) * 45 = 4.5 for ALL actions
- Var_a(E_S[f(S, a)]) = Var(4.5, 4.5, 4.5, 4.5) = 0
- Therefore het(lambda) = lambda^2 * 0 = 0 for ALL lambda

This was verified computationally: analytical heterogeneity = 0.000000 at every lambda level.

## 2. Monte Carlo Results

| Lambda | Het Mean | Het Std | Het Min | Het Max |
|--------|----------|---------|---------|---------|
| 0.0    | 0.0523   | 0.0371  | 0.0036  | 0.1499  |
| 0.1    | 0.0546   | 0.0543  | 0.0029  | 0.2545  |
| 0.2    | 0.0437   | 0.0328  | 0.0062  | 0.1160  |
| 0.3    | 0.0586   | 0.0338  | 0.0048  | 0.1295  |
| 0.4    | 0.0647   | 0.0546  | 0.0018  | 0.2271  |
| 0.5    | 0.0544   | 0.0339  | 0.0075  | 0.1712  |
| 0.7    | 0.0537   | 0.0342  | 0.0157  | 0.1278  |
| 1.0    | 0.0570   | 0.0522  | 0.0061  | 0.1849  |

All values are consistent with sampling noise around 0. No monotonic trend is visible.

## 3. Statistical Tests

### 3.1 Primary: Spearman Correlation

| Test | rho | p (one-sided) | Pass? |
|------|-----|---------------|-------|
| Aggregate (n=8) | 0.3333 | 0.2099 | No (need rho >= 0.65, p < 0.05) |
| Function 1 (seed=42) | -0.4762 | 0.8835 | No |
| Function 2 (seed=43) | 0.7619 | 0.0140 | No (need rho >= 0.83, p < 0.0167) |
| Function 3 (seed=44) | 0.2381 | 0.2851 | No |

Only Function 2 shows a positive correlation, but it does not survive Bonferroni correction. Functions 1 and 3 show no trend or a negative trend. This inconsistency is expected when the true effect is zero — the observed correlations are sampling noise.

### 3.2 Two-Way ANOVA (240 observations)

| Effect | F | p | df |
|--------|---|---|-----|
| Lambda | 0.5643 | 0.7844 | 7 |
| Function | 0.2626 | 0.7693 | 2 |
| Interaction | 0.6516 | 0.8193 | 14 |
| Residual | — | — | 216 |

- Lambda effect: NOT significant (p = 0.78). No evidence that lambda influences heterogeneity.
- Function effect: NOT significant (p = 0.77). Functions behave similarly.
- Interaction: NOT significant (p = 0.82). Function invariance holds (by default, since nothing is significant).
- Model R² = 0.059. The model explains almost none of the variance.

### 3.3 Permutation Tests

- **Lambda=0**: Mean permutation p = 0.466 (not significant). Null control PASSES.
- **Lambda=1**: 0/30 measurements have heterogeneity >= 0.5. Positive control FAILS.

### 3.4 Effect Size

- Cohen's d (lambda=1 vs lambda=0) = 0.10 (small). No detectable difference.

## 4. Control Assessment

| Control | Expected | Observed | Pass? |
|---------|----------|----------|-------|
| Positive (lambda=1, het >= 0.5) | het >= 0.5 | het_mean = 0.057 | **FAIL** |
| Null (lambda=0, het ~ 0) | p > 0.05 | mean_p = 0.466 | PASS |
| Permutation null | het ~ 0 | Analytical het = 0 | PASS |
| Function invariance | interaction p > 0.05 | p = 0.82 | PASS |
| Monotonicity | het increasing with lambda | rho = 0.33 | **FAIL** |

The positive control failure is the most informative result: it demonstrates that permutation functions fundamentally cannot produce the heterogeneity this metric measures.

## 5. Interpretation

### What this experiment shows

The causal effect heterogeneity metric, as defined in the preregistration, is **incompatible with permutation-based deterministic functions**. This is a mathematical fact:

- Permutations preserve the mean of the input set
- For a uniform state space {0,...,9}, the mean is 4.5
- Therefore E_S[f(S, a)] = 4.5 for all actions, regardless of the permutation
- Therefore Var_a(E_S[f(S, a)]) = 0
- Therefore het(lambda) = 0 for all lambda

The Monte Carlo estimates (~0.05) are sampling noise from finite samples (500 transitions, ~125 per action), not evidence of signal.

### What this does NOT show

- This does NOT falsify C-WEB-DYNAMICS (the claim that Web transformations contain predictive dynamical structure).
- This does NOT show that causal intervention is useless for detecting regime-dependent dynamics.
- This does NOT show that permutation-based transitions lack dynamical structure (the parent experiment detected prediction accuracy differences via rules vs. memory).

### What went wrong in the design

The preregistration's theoretical derivation assumed Var_a(E_S[f(S, a)]) > 0 for permutation functions. This assumption was incorrect. The derivation should have noted that:

1. For any permutation pi of {0,...,9}: sum(pi(s)) = sum({0,...,9}) = 45
2. Therefore E_S[pi(S)] = 45/10 = 4.5 for any permutation pi
3. Therefore Var_a(E_S[f(S, a)]) = 0 for permutation functions

This is a design-level error in the preregistration, not an execution error.

## 6. Implications for C-WEB-DYNAMICS

The claim C-WEB-DYNAMICS states that "Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity." This experiment does not challenge that claim. It challenges only:

1. The specific causal heterogeneity metric (variance of expected next-states across actions)
2. Applied to permutation-based deterministic functions

A different choice of deterministic functions (e.g., affine functions f(s, a) = (a*s + b) mod 10, or state-dependent functions that don't preserve the mean) would produce Var_a(E_S[f(S, a)]) > 0 and could properly test the causal heterogeneity hypothesis.

## 7. Recommendations

1. **Do not promote this result as evidence against C-WEB-DYNAMICS.** The negative result is specific to the metric-function combination.

2. **Design a follow-up experiment** with non-permutation deterministic functions that break the mean-preservation property. Candidate functions:
   - Affine: f(s, a) = (w_a * s + b_a) mod 10, where w_a varies across actions
   - Polynomial: f(s, a) = (s^2 + a_index * s) mod 10
   - State-dependent: f(s, a) = (s + a_index) mod 10 (addition, not permutation)

3. **Retain the causal heterogeneity metric** as a detection method — it is mathematically sound, just incompatible with permutation functions.

4. **Document the permutation mean-preservation property** as a known limitation for future experiment design.

## 8. Artifact Inventory

| Artifact | Path | Role |
|----------|------|------|
| Analysis code | research/frontier/causal_heterogeneity/analyze.py | code |
| Result JSON | research/frontier/causal_heterogeneity/result.json | derived |
| Provenance JSON | research/frontier/causal_heterogeneity/provenance.json | derived |
| Frozen prereg | research/frontier/causal_heterogeneity/prereg.md | fixture |
| Frozen spec | research/frontier/causal_heterogeneity/spec.json | fixture |
| Frozen request | research/frontier/causal_heterogeneity/request.json | fixture |
