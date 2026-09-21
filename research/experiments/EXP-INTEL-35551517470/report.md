# Report: EXP-INTEL-35551517470 — Bounded Saturating Function Extrapolation

## Executive Summary

**Verdict per frozen decision rules: SURVIVES** (C1 AND C2 AND C3 all PASS).

**Scientific interpretation: MIXED.** The logistic and Hill functions achieve perfect or near-perfect in-sample fits (R²=1.0 and 0.999994 respectively) and produce physically valid extrapolations. However, the extrapolation is **informationally trivial**: both functions predict F(50)=F(82)≈0.5654, which is **identical to the constant null** (F(n)=0.5654 for all n). The model-based path survives the frozen decision gates but provides zero new predictive information beyond the raw observation at n=20.

## 1. Training Data

Training points from `analysis_output_snr.json` (canonical tag_entropy × DEF-FULL-MAP):

| n | F(n) | Source |
|---|------|--------|
| 5 | 0.0000 | proportion(margin>0) at n=5 |
| 10 | 0.0000 | proportion(margin>0) at n=10 |
| 15 | 0.4996 | proportion(margin>0) at n=15 |
| 20 | 0.5654 | proportion(margin>0) at n=20 |

Step-function structure: 0→0→0.50→0.57 with 7.6× growth deceleration.

## 2. Fit Results

### Logistic: F(n) = L/(1+exp(-k·(n-n0)))

- **Parameters**: L=0.5654, k=10.75, n0=14.81
- **R²**: 1.0000 (perfect interpolation)
- **Max residual**: 3.78×10⁻⁸ pp (effectively zero)
- **AIC**: -161.66, **BIC**: -163.50
- **F(50)**: 0.5654, **F(82)**: 0.5654

The logistic learns a **step-function approximation**: the steepness k=10.75 creates a near-discontinuous transition at n≈14.8, capturing the 0→0.50 jump. The asymptote L=0.5654 is learned directly from the n=20 observation. For all n>15, the function is at its asymptote: F(n)≈0.5654.

### Hill: F(n) = L·n^h/(K^h+n^h)

- **Parameters**: L=0.5657, h=20.0, K=13.56
- **R²**: 0.999994
- **Max residual**: 0.128 pp
- **AIC**: -41.46, **BIC**: -43.30
- **F(50)**: 0.5657, **F(82)**: 0.5657

The Hill coefficient h=20.0 indicates an extremely steep transition (effectively a step). The half-max K=13.56 is consistent with the midpoint of the n=10→n=15 jump. Like the logistic, it saturates to L≈0.5657 for all n>15.

### Richards: F(n) = L/(1+(n/n0)^a)^(1/v)

- **Parameters**: L=0.2755, n0=100.0, a=0.01, v=20.0 (at bounds)
- **R²**: -0.0002 (worse than horizontal mean)
- **Max residual**: 29.92 pp
- **AIC**: -72.75, **BIC**: -75.21
- **Converged**: No — stuck at boundary values

The 4-parameter Richards family fails to capture the step structure. With 4 data points and 4 parameters, the optimization landscape is degenerate. The function collapses to a nearly flat line at F≈0.266.

## 3. Decision Rule Evaluation

| Criterion | Threshold | Logistic | Hill | Result |
|-----------|-----------|----------|------|--------|
| C1: R² ≥ 0.90 | 0.90 | 1.0000 | 0.999994 | **PASS** |
| C1: max_resid < 10pp | 10pp | 3.78e-8pp | 0.128pp | **PASS** |
| C2: F(50) ∈ [0,1] | [0,1] | 0.5654 | 0.5657 | **PASS** |
| C2: F(82) ∈ [0,1] | [0,1] | 0.5654 | 0.5657 | **PASS** |
| C3: R² > 0.93 | 0.93 | 1.0000 | 0.999994 | **PASS** |
| C3: max_resid < 8pp | 8pp | 3.78e-8pp | 0.128pp | **PASS** |

**C1 PASS, C2 PASS, C3 PASS → VERDICT: SURVIVES per frozen rules.**

## 4. Critical Observation: Extrapolation Equivalence to Constant Null

The **constant null** B5 (F(n)=0.5654 for all n, from parent EXP-INTEL-3544806153) predicts:
- F(50) = 0.5654
- F(82) = 0.5654

The logistic predicts:
- F(50) = 0.5654
- F(82) = 0.5654

The Hill predicts:
- F(50) = 0.5657
- F(82) = 0.5657

**The saturating function extrapolation is informationally identical to the constant null.** The R² improvement (1.0 vs -1.25 for constant null, 1.0 vs 0.8797 for parent power law) is purely in-sample. The extrapolation power is zero: the model learns that the data saturates at the observed value and predicts the plateau continues forever.

This is not a failure of the fitting procedure — it is a fundamental limitation of the data. With only 4 training points (and 2 at zero), there is no information to distinguish:
- L=0.5654 (plateau hypothesis)
- L=0.80 (threshold crossing at full DOM)
- L=1.0 (continued growth)

The asymptotic value L is entirely determined by the single observation at n=20.

## 5. Parent Baseline Comparison

| Model | R² | Max Residual | F(50) | F(82) |
|-------|-----|-------------|-------|-------|
| **Logistic (this experiment)** | 1.000 | 3.78e-8pp | 0.5654 | 0.5654 |
| **Hill (this experiment)** | 1.000 | 0.128pp | 0.5657 | 0.5657 |
| Parent best: sign-fraction power law | 0.8797 | 12.39pp | (invalid) | (invalid) |
| Parent: Phi(median/std) | N/A | 34.59pp@n15 | (invalid) | (invalid) |
| Parent: Phi(mean/std) | N/A | 17.8pp@n20 | (invalid) | (invalid) |
| Constant null (B5) | -1.25 | 56.54pp | 0.5654 | 0.5654 |
| Empirical CDF linear (B4) | N/A | N/A | 0.9602 | 1.3813 |

The logistic improves over the parent's best model (R²=0.8797) by 0.1203 in R² and by 12.39pp in maximum residual. However, the parent's model was already REJECTED at C1/C2, so improvement over a rejected model is a low bar.

## 6. Interpretation

### What the SURVIVES verdict means

Per the frozen decision rules, a saturating function provides a "validated extrapolation that improves over all prior models." The logistic and Hill functions satisfy all three conjunctive criteria.

### What the SURVIVES verdict does NOT mean

1. **It does NOT mean the model provides new predictive information.** The extrapolation F(50)=0.5654 is the constant null. No new information is gained beyond the raw observation at n=20.

2. **It does NOT mean ranking agreement will plateau at 56% at full DOM.** The logistic learns L=0.5654 because that is the only non-zero observation available. With different data (e.g., n=25 showing F=0.65), the logistic would learn a different L.

3. **It does NOT change the product decision on Docker investment.** The extrapolation predicts F(50)=0.5654 < 0.80, consistent with the plateau hypothesis. But this prediction carries extreme uncertainty (the PI90 from the parent's power law was [0.845, 1.0] — wildly different from the logistic's 0.5654).

### The step-function truth

Both the logistic and Hill achieve their perfect fits by learning **step-function approximations** (k=10.75, h=20.0). This confirms the parent handoff's analysis: the data has genuine step-function structure (0,0,0.50,0.57) that cannot be captured by smooth functional forms without becoming step-like themselves.

The step-function structure is a **threshold phenomenon**: ranking agreement is zero below n=10, jumps to ~50% at n=15, and plateaus. This is not a smooth saturation — it is a phase transition in ranking stability.

## 7. Product Consequences

### Per frozen spec

- **Positive (C1 AND C2 AND C3)**: "A validated bounded extrapolation exists. If the best-fit function predicts F(50) < 0.80, the plateau is structural and recipe density is limited — product lane should use non-recipe density."

### Actual product implication

The logistic predicts F(50)=0.5654 < 0.80. However, this prediction is:
- Identical to the constant null (no model needed)
- Based on only 4 training points with 2 at zero
- Derived from a step-function approximation, not a genuine saturation model

**Recommendation**: The SURVIVES outcome should NOT change the Docker investment decision. The extrapolation provides no new information. Docker-based direct full-DOM measurement (EXP-INTEL-35462974425) remains the only path to an empirical answer on whether ranking agreement crosses 80% at n=21-82.

## 8. Validity Threats

1. **Overfitting**: 4 data points with 3 parameters (logistic) — perfect interpolation is guaranteed, not informative.
2. **Extrapolation equivalence**: The model extrapolation is identical to the constant null. The R² improvement is purely in-sample.
3. **Step-function approximation**: The logistic's steepness k=10.75 is a smooth approximation to a discontinuous step. The model does not capture a genuine saturation mechanism.
4. **Information ceiling**: With 4 points (2 at zero), the asymptotic value L is entirely determined by the n=20 observation. No functional form can discriminate between competing full-DOM hypotheses.
5. **Frozen decision rule gap**: The rules do not include a criterion for "extrapolation provides new information beyond constant null." The SURVIVES verdict is correct per the rules but scientifically trivial.
