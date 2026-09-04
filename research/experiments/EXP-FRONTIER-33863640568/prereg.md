# EXP-FRONTIER-33863640568 — Preregistration

## Status: DESIGN FROZEN (pending freeze.json)

---

## 1. Context and Inherited State

This experiment continues from EXP-FRONTIER-33767130362 (handoff SHA256: 128562014c5c09d2793692cd05297d571da9cefc4059be95bdc469498fb0e7d8).

**Established from parent:**
- Analytic identity: for any permutation pi of {0..9}, Var_a(E_S[pi_a(S)]) = 0 because E[pi_a(S)] = 4.5 for all actions.
- Causal heterogeneity metric het(lambda) = lambda^2 * Var_a(E_S[f(S,a)]) is mathematically correct but yields het=0 for all lambda when Var=0.
- Monte Carlo estimates ~0.04-0.07 are sampling noise around true value of 0.
- Pipeline executed correctly (status=COMPLETE, 120,000 transitions, 240 cells).

**Rejected from parent:**
- Permutation functions as a test class for causal heterogeneity.
- The hypothesis that het(lambda) detects regime dynamics when Var_a(E_S[f(S,a)]) = 0.
- Positive control threshold het >= 0.5 at lambda=1 for permutation functions.

**Unknown (inherited):**
- Whether non-permutation functions yield detectable het(lambda).
- Whether distributional metrics detect structure beyond means.
- How synthetic results translate to real Web transitions.

**Do Not Assume:**
- C-WEB-DYNAMICS is not falsified by this experiment.
- Causal heterogeneity as a general approach is not invalid — only permutation functions are degenerate.
- The parent's prediction-accuracy finding (rho=1.0) is not refuted.

---

## 2. Scientific Question

Can non-permutation deterministic functions (affine maps where E_S[f(S,a)] varies across actions) yield detectable lambda-scaling of causal effect heterogeneity?

---

## 3. Hypothesis

When synthetic Web-like transitions use affine deterministic functions f(s,a) = (c_a * s + b_a) mod 10 where c_a and b_a vary by action (ensuring E_S[f(S,a)] differs across actions), the causal effect heterogeneity metric Var_a(E_S[do(A=a)]) will scale monotonically with lambda, with aggregate Spearman rho >= 0.65 and p < 0.05 one-sided.

---

## 4. Deterministic Function Design

### 4.1 Affine Function Family

Three affine functions with different coefficient sets:

**Function 1 (seed=42):**
- c = [2, 3, 5, 7] (action multipliers)
- b = [1, 3, 0, 6] (action offsets)
- f(s, a_i) = (c_i * s + b_i) mod 10

**Function 2 (seed=43):**
- c = [3, 4, 6, 8]
- b = [2, 5, 1, 4]
- f(s, a_i) = (c_i * s + b_i) mod 10

**Function 3 (seed=44):**
- c = [2, 6, 4, 9]
- b = [7, 2, 8, 3]
- f(s, a_i) = (c_i * s + b_i) mod 10

### 4.2 Analytic Verification

For each function, E_S[f(S, a_i)] = (c_i * E[S] + b_i) mod 10 is NOT simply c_i * 4.5 + b_i because mod 10 is nonlinear. Instead:

E_S[f(S, a_i)] = (1/10) * sum_{s=0}^{9} (c_i * s + b_i) mod 10

This must be computed numerically for each function/action pair and verified to differ across actions. If any function has E_S[f(S, a)] identical for all actions, it is degenerate and must be replaced.

### 4.3 Expected Analytical Heterogeneity

het(lambda) = lambda^2 * Var_a(E_S[f(S, a)])

At lambda=1: het = Var_a(E_S[f(S, a)]) — analytically computable from the function parameters.
At lambda=0: het = 0 (pure noise, no action-dependence).

---

## 5. Data Generation

- State space: {0, 1, ..., 9}
- Actions: ['click', 'fill', 'submit', 'navigate'] (4 actions)
- Lambda levels: [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0] (8 levels)
- Transitions per cell: 500
- Replications per cell: 10
- Functions: 3 (seeds 42, 43, 44)
- Total transitions: 8 * 3 * 10 * 500 = 120,000

Transition generation:
```
For each transition:
  s ~ Uniform({0..9})
  a ~ Uniform(ACTIONS)
  if rng.random() < lambda:
    s_next = f(s, a)  # deterministic function
  else:
    s_next ~ Uniform({0..9})  # pure noise
```

Seed mechanism: `func_seed * 10000 + rep_idx * 100 + 42` for each replication RNG.

---

## 6. Metrics

### 6.1 Primary Metric: Causal Effect Heterogeneity

het(lambda) = Var_a(E_S[do(A=a)])

Computed from Monte Carlo samples:
1. Group transitions by action.
2. Compute sample mean next-state per action: mean_a = E[S_{t+1} | A_t = a].
3. Compute variance of the 4 sample means: het = Var(mean_click, mean_fill, mean_submit, mean_navigate).

### 6.2 Secondary Metric: Total Variation Distance

TV_max(lambda) = max_{a,a'} TV(P(S_{t+1}|do(A=a)), P(S_{t+1}|do(A=a')))

Where TV(P, Q) = (1/2) * sum_s |P(s) - Q(s)|.

Computed from empirical action-conditional next-state distributions (10-state histograms).

### 6.3 Aggregate Statistics

- Aggregate Spearman rho(het_by_lambda, lambda) with one-sided p-value
- Per-function Spearman rho with Bonferroni-corrected p-value (3 functions, alpha=0.05/3)
- Cohen's d (lambda=1 vs lambda=0) for effect size
- Two-way ANOVA: lambda effect, function effect, interaction

---

## 7. Controls

### 7.1 Positive Control
At lambda=1, heterogeneity >= 0.5 across all 3 functions.
Rationale: With affine functions, Var_a(E_S[f(S,a)]) > 0, so het(1) = Var_a > 0. With 10 states and 4 distinct affine maps, the variance should be substantial.

### 7.2 Null Control
At lambda=0, permutation test p > 0.05 (heterogeneity not significantly > 0).
Rationale: Pure noise yields identical interventional distributions across actions.

### 7.3 Permutation Null
Shuffled action labels yield heterogeneity near zero at all lambda levels.
Verified analytically: shuffling action labels makes E[S_{t+1}|do(A=a)] identical for all actions.

### 7.4 Function Invariance
No significant function x lambda interaction (two-way ANOVA p > 0.05).
All functions should show similar het(lambda) curves because the metric depends on Var_a(E_S[f(S,a)]) which is a property of the function class, not specific coefficients.

### 7.5 Monotonicity Sensitivity
het_means are monotonically non-decreasing across lambda levels.

---

## 8. Decision Rules

### Primary Decision
SURVIVES_CURRENT_TEST if ALL of:
1. Aggregate Spearman rho(het_by_lambda, lambda) >= 0.65 with p < 0.05 one-sided
2. Positive control passes: heterogeneity >= 0.5 at lambda=1 across all functions
3. Null control passes: heterogeneity not significantly > 0 at lambda=0 (permutation p > 0.05)
4. No significant function x lambda interaction (two-way ANOVA p > 0.05)
5. No pipeline errors

FALSIFIED-IN-SETTING if ANY of:
1. Aggregate Spearman rho < 0.65 or p > 0.05
2. Positive control fails
3. Null control fails
4. Significant function x lambda interaction

MEASUREMENT_INVALID if:
- Pipeline errors
- Degenerate functions (Var_a(E_S[f(S,a)]) = 0 for all actions in any function)
- Heterogeneity CV across replications > 0.5

### Secondary Confirmation
Per-function Spearman tests: rho >= 0.83 with p < 0.017 (Bonferroni x3 correction).

### TV Distance Secondary
TV_max(lambda) should also scale monotonically with lambda and be >= het(lambda) at each level (since TV captures full distributional differences, not just first-moment variance).

---

## 9. Analysis Plan

1. **Function verification**: For each function, compute E_S[f(S, a)] for all 4 actions. Verify they differ. If any function is degenerate, replace and re-verify.

2. **Analytical heterogeneity**: Compute het_analytical = Var_a(E_S[f(S,a)]) for each function. This is the ground-truth value at lambda=1.

3. **Data generation**: Generate 120,000 transitions using frozen seeds.

4. **Monte Carlo heterogeneity estimation**: For each function x lambda x replication, compute het_mc from the 500 transitions.

5. **TV distance computation**: For each function x lambda x replication, compute TV_max from empirical action-conditional distributions.

6. **Primary test**: Aggregate Spearman rho(het_mc_means_by_lambda, lambda_levels).

7. **Controls**: Permutation tests at lambda=0 and lambda=1, ANOVA, monotonicity check.

8. **Effect size**: Cohen's d (lambda=1 vs lambda=0).

9. **Comparison with prior**: Contrast het_mc values with prior experiment's permutation-based values at matched lambda levels.

---

## 10. Validity Threats

1. **Mod 10 nonlinearity**: The mod operation may reduce Var_a(E_S[f(S,a)]). Mitigation: verify analytically that Var > 0 before running.

2. **Small state space**: 10 states limits the maximum possible TV distance. Mitigation: 10 states is sufficient for detection; this is synthetic validation, not real-Web demonstration.

3. **Synthetic-to-real gap**: Affine functions may not represent real Web dynamics. Mitigation: this experiment validates the metric, not the Web. Real-data application is a separate experiment.

4. **Function invariance**: With only 3 functions, ANOVA interaction power is limited. Mitigation: functions are designed to have substantially different coefficient sets to maximize detectable differences.

5. **TV distance sensitivity**: TV distance may be insensitive to subtle distributional differences. Mitigation: TV is a standard, well-understood metric; insensitivity would itself be informative.

---

## 11. Artifacts to Persist

- `analyze.py` — frozen analysis script (code role)
- `spec.json` — this specification (fixture role)
- `prereg.md` — this preregistration (fixture role)
- `request.json` — immutable work request (fixture role)
- `result.json` — structured measurements (derived role)
- `provenance.json` — execution provenance (derived role)

---

## 12. Expected Outcomes and Consequences

### Positive outcome (het scales with lambda for affine functions)
- Validates causal heterogeneity metric as a detection method
- Opens path to real-Web regime detection
- TV distance provides additional distributional characterization
- Next: apply to real Web transition data with regime stratification

### Negative outcome (het does not scale for affine functions)
- Causal heterogeneity metric (Var_a of expected next-states) is fundamentally insensitive regardless of function class
- Pivot to: TV/JSD distributional metrics, or prediction-accuracy approaches with larger-n designs
- Does not falsify C-WEB-DYNAMICS — only this specific metric

### Mixed outcome (het scales but controls fail)
- Informative about metric limitations
- Follow-up with modified controls or larger samples
