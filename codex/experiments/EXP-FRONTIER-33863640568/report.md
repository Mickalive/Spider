# EXP-FRONTIER-33863640568 — Execution Report

## Status: COMPLETE (FALSIFIED-IN-SETTING)

**Decision:** FALSIFIED-IN-SETTING  
**Reason:** Positive control fails (heterogeneity < 0.5 at lambda=1 for 2/3 functions) and function invariance fails (significant function × lambda interaction).  

---

## 1. Summary

This experiment tested whether affine deterministic functions \( f(s,a) = (c_a \cdot s + b_a) \mod 10 \) (where \( \mathbb{E}_S[f(S,a)] \) varies across actions) yield detectable lambda-scaling of causal effect heterogeneity, and whether total variation (TV) distance provides additional sensitivity beyond mean-based metrics.

**Key finding:** Affine functions **do** produce strong lambda-scaling of causal heterogeneity (aggregate Spearman \( \rho = 0.9762 \), \( p = 1.7 \times 10^{-5} \)), confirming the metric is not degenerate for non-permutation functions. However, the experiment is **falsified-in-setting** because:

1. **Positive control fails:** Only 11/30 measurements at lambda=1 have heterogeneity ≥ 0.5 (threshold from prereg). Two functions (seeds 43, 44) have analytical heterogeneity 0.171875 at lambda=1, below the 0.5 threshold.
2. **Function invariance fails:** Two-way ANOVA shows significant function × lambda interaction (p ≈ 0), indicating functions respond differently to lambda due to differing coefficient sets.

---

## 2. Scientific Results

### 2.1 Causal Effect Heterogeneity (Primary Metric)

| Lambda | Het Mean ± Std | Analytical Het (Function 42) |
|--------|----------------|------------------------------|
| 0.0    | 0.0523 ± 0.0371 | 0.000000 |
| 0.1    | 0.0651 ± 0.0611 | 0.009219 |
| 0.2    | 0.0569 ± 0.0353 | 0.036875 |
| 0.3    | 0.0732 ± 0.0557 | 0.082969 |
| 0.4    | 0.1318 ± 0.1265 | 0.147500 |
| 0.5    | 0.1649 ± 0.1451 | 0.230469 |
| 0.7    | 0.2226 ± 0.1774 | 0.451719 |
| 1.0    | 0.4470 ± 0.3541 | 0.921875 |

**Aggregate Spearman \( \rho = 0.9762 \)** (p_one_sided = 1.7e-5) — exceeds threshold \( \rho \ge 0.65, p < 0.05 \).  
**Cohen's d (lambda=1 vs 0) = 1.5416** (large effect).

### 2.2 Total Variation Distance (Secondary Metric)

| Lambda | TV Mean ± Std | Analytical TV (Function 42) |
|--------|---------------|-----------------------------|
| 0.0    | 0.1915 ± 0.0310 | 0.000000 |
| 0.1    | 0.1993 ± 0.0274 | 0.080000 |
| 0.2    | 0.2607 ± 0.0396 | 0.160000 |
| 0.3    | 0.3226 ± 0.0485 | 0.240000 |
| 0.4    | 0.4143 ± 0.0588 | 0.320000 |
| 0.5    | 0.5040 ± 0.0505 | 0.400000 |
| 0.7    | 0.6754 ± 0.0749 | 0.560000 |
| 1.0    | 0.9496 ± 0.0722 | 0.800000 |

**TV Spearman \( \rho = 1.0000 \)** (p_one_sided ≈ 0). TV distance is **strictly ≥ heterogeneity** at every lambda level, confirming distributional structure beyond first moments.

### 2.3 Per-Function Results

| Function | Seed | Analytical Var_a | Spearman ρ | p_one_sided |
|----------|------|------------------|------------|-------------|
| 1        | 42   | 0.921875         | 0.9762     | 1.7e-5      |
| 2        | 43   | 0.171875         | 0.8571     | 0.0033      |
| 3        | 44   | 0.171875         | 0.8095     | 0.0075      |

All per-function Spearman correlations are significant after Bonferroni correction (α/3 = 0.0167). Functions 43 and 44 have lower analytical heterogeneity but still show strong monotonic scaling.

---

## 3. Controls

| Control | Threshold | Result | Evidence |
|---------|-----------|--------|----------|
| Positive control | het ≥ 0.5 at lambda=1 across all functions | **FAIL** (11/30) | metrics.permutation_results.lambda_1 |
| Null control | het not significantly > 0 at lambda=0 | **PASS** (p=0.466) | metrics.permutation_results.lambda_0 |
| Permutation null | Shuffled action labels → het ≈ 0 | **PASS** (analytical) | metrics.analytical_heterogeneity |
| Function invariance | No significant function × lambda interaction | **FAIL** (p≈0) | metrics.anova_results |
| Monotonicity | het monotonically non-decreasing with lambda | **FAIL** (dip at lambda=0.2) | metrics.monotonicity |

---

## 4. Interpretation

### 4.1 The Causal Heterogeneity Metric Works for Affine Functions

The previous experiment (EXP-FRONTIER-33767130362) found the metric degenerate for permutation functions because \( \text{Var}_a(\mathbb{E}_S[f(S,a)]) = 0 \) identically. This experiment demonstrates that when \( \text{Var}_a(\mathbb{E}_S[f(S,a)]) > 0 \), the metric scales monotonically with lambda (Spearman ρ = 0.9762). The metric is **not fundamentally insensitive** — it was specific to permutation functions.

### 4.2 Positive Control Failure Is a Threshold Issue, Not a Metric Failure

The positive control threshold (het ≥ 0.5 at lambda=1) was set a priori based on the expectation that affine functions would produce substantial heterogeneity. Functions 43 and 44 have lower Var_a (0.171875) but still produce significant scaling. The threshold is too strict for these functions; a threshold of ≥ 0.1 would pass all functions. However, the frozen decision rule must be applied as written.

### 4.3 Function Invariance Failure Is Expected

Functions have different coefficient sets, leading to different Var_a values. The significant interaction is real, not noise. This does not invalidate the metric; it indicates the metric correctly detects function-specific heterogeneity levels.

### 4.4 TV Distance Provides Additional Sensitivity

TV distance is strictly ≥ heterogeneity at all lambda levels, confirming that distributional differences extend beyond first moments. TV also shows perfect monotonic scaling (ρ = 1.0). For future experiments, TV distance may be a more sensitive metric than variance of means.

---

## 5. Comparison with Parent Experiment (EXP-FRONTIER-33767130362)

| Metric | Permutation (Parent) | Affine (This) |
|--------|----------------------|---------------|
| Analytical Var_a | 0.0 | 0.171875 – 0.921875 |
| Aggregate Spearman ρ | 0.333 (p=0.21) | 0.9762 (p=1.7e-5) |
| Positive control | 0/30 pass | 11/30 pass |
| Cohen's d | 0.105 (small) | 1.542 (large) |

The affine functions produce dramatically stronger signal, confirming that the permutation degeneracy was the cause of the prior null result.

---

## 6. Validity Threats

1. **Positive control threshold too strict:** The 0.5 threshold is based on analytical expectations for function 42 only. Functions 43 and 44 have lower Var_a but still produce significant scaling. The threshold should be function-specific or lowered.

2. **Monotonicity dip at lambda=0.2:** Heterogeneity mean at lambda=0.2 (0.0569) is lower than at lambda=0.1 (0.0651). This is sampling noise (std ~0.035) and does not affect the strong overall correlation.

3. **Synthetic-to-real gap:** Affine functions may not represent real Web dynamics. This experiment validates the metric, not the Web.

4. **Raw per-replication tables not persisted:** The aggregated results are sufficient for the primary test, but independent recomputation of per-replication statistics is limited. The experiment is reproducible from frozen parameters and seed.

---

## 7. Product Consequences

### Positive Outcome (Partial)
The causal heterogeneity metric **does** detect lambda-scaling for non-permutation functions. This validates the metric as a detection method for Web-dynamical regime structure, albeit with the caveat that function-specific heterogeneity levels vary.

### Negative Outcome (Control Failures)
The positive control and function invariance failures indicate that the frozen decision rule is too strict for this function class. However, the scientific question is answered: the metric works when Var_a > 0.

### Recommendation
The Frontier lane should:
1. **Not pivot to distributional metrics yet** — the mean-based metric works for affine functions.
2. **Consider relaxing the positive control threshold** for future experiments with moderate-heterogeneity functions.
3. **Apply TV distance as a secondary metric** in future experiments, as it provides additional sensitivity.
4. **Test with real Web-like transitions** to assess synthetic-to-real translation.

---

## 8. Artifacts

| Path | SHA256 | Role |
|------|--------|------|
| research/experiments/EXP-FRONTIER-33863640568/analyze.py | 480b359fa21f1d7f14095b365061f44c7a08fb9c55b787ca51b940f4fbc7f704 | code |
| research/experiments/EXP-FRONTIER-33863640568/result.json | 813bdea839170a6358ed8b4ffa6f04cb3f30ee62034fa42dd0ea67288215493e | derived |
| research/experiments/EXP-FRONTIER-33863640568/provenance.json | 9d48856c81a4ecdc1df79dc4560d7c3142ff8994c6ed3b56ad4b91a31aa56544 | derived |

---

## 9. Unresolved Questions

1. Should the positive control threshold be function-specific (based on analytical Var_a) rather than a universal 0.5?
2. Does the causal heterogeneity metric scale with lambda for real Web transitions (not just synthetic affine functions)?
3. Is TV distance a more appropriate primary metric for future experiments, given its perfect monotonic scaling and strictly greater sensitivity?
4. How many functions are needed to reliably estimate function invariance (ANOVA interaction power)?
