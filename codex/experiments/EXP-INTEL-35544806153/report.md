# EXP-INTEL-35544806153 — Report

## Status: MEASUREMENT_INVALID (C2 FAIL, frozen decision rule)

## Summary

This experiment tests whether a non-parametric empirical CDF mapping of the margin distribution can predict ranking agreement at n=15 and n=20 and extrapolate to full-DOM n=50/82. The empirical CDF mapping F(n) = proportion(margin_i > 0) is by construction identical to the diagnostic indicator under template invariance.

**Key finding**: The empirical CDF exactly reproduces observed agreement at all training points (C1 PASS, 0.00pp residual at all points). However, the frozen decision rule requires strict monotonicity across all 4 points including the n=5→n=10 step where F(5) = F(10) = 0.0 (C2 FAIL). The linear extrapolation from n=15→n=20 slope predicts F(50) = 0.96 > 0.80 (C3 FAIL). Under frozen rules: C1=PASS, C2=FAIL → MEASUREMENT_INVALID.

## Detailed Results

### Empirical CDF Values

| n | F(n) | prop_agree | n_positive | n_zero | n_negative | mean_margin |
|---|------|-----------|------------|--------|------------|-------------|
| 5  | 0.0000 | 0.0000 | 0 | 5070 | 4930 | -4.90e-05 |
| 10 | 0.0000 | 0.0000 | 0 | 2464 | 7536 | -1.35e-04 |
| 15 | 0.4996 | 0.4996 | 4996 | 0 | 3774 | +2.66e-05 |
| 20 | 0.5654 | 0.5654 | 5654 | 0 | 3747 | +3.97e-04 |

### Step-Function Structure

The data exhibits a clear step-function pattern:
- **n=5 to n=10**: Both 0.0 — all margins negative, no ranking agreement. The margin distribution is entirely below zero.
- **n=10 to n=15**: Jump from 0.0 to 0.4996 — the "phase transition". The mean margin crosses zero (from -1.35e-04 to +2.66e-05). 4996 of 10000 iterations now have positive margins.
- **n=15 to n=20**: Plateau from 0.4996 to 0.5654 — only +6.6pp increase. Growth decelerates 7.6x (ratio = 0.132).

The jump accounts for 88.4% of the total increase; the plateau accounts for only 11.6%.

### Decision Rule Evaluation

| Criterion | Expected | Observed | Pass? |
|-----------|----------|----------|-------|
| C1: Reproduction | Residual <1pp at n=15 and n=20 | 0.00pp at both | PASS |
| C2: Monotonicity | F(20)>F(15)>F(10)>F(5) | F(10)=F(5)=0.0 (tie) | FAIL |
| C3: Extrapolation <80% | F(50)<0.80 | F(50)=0.9602 | FAIL |

**Verdict under frozen rule**: C1=PASS, C2=FAIL → MEASUREMENT_INVALID

### Extrapolation Analysis

Linear extrapolation from n=15→n=20 slope (0.01316/element):
- F(50) = 0.9602 (96.0%) — exceeds 80% threshold
- F(82) = 1.3813 (138.1%) — exceeds 1.0, physically impossible for a proportion

This demonstrates that linear extrapolation of a bounded [0,1] quantity from step-function data is fundamentally inappropriate. The linear model cannot capture saturation behavior.

Alternative linear extrapolations are even more extreme:
- From n=5→n=20 slope: F(50) = 1.696
- From n=10→n=20 slope: F(50) = 2.262

### Null Control

The NC1 linear null comparison passes: difference from constant-trend null is 39.48pp >> 5pp threshold. The empirical CDF extrapolation contains substantial non-trivial structure beyond a constant trend.

## Interpretation

The empirical CDF mapping is, by construction under template invariance, identical to the diagnostic proportion(margin>0). It provides zero information beyond what was already known from the parent's positive control. The mapping is the true data-generating process at training points, not an independent model that could be validated.

The most scientifically informative observation is the **7.6x growth deceleration** from the jump phase (n=10→15) to the plateau phase (n=15→20). If this deceleration pattern continues, the proportion would saturate well below 100% at full DOM, suggesting the ranking agreement plateau is structural. However, this observation cannot be validated with only 2 points on the plateau and linear extrapolation.

The frozen C2 decision rule requires strict monotonicity F(10) > F(5), but F(10) = F(5) = 0.0. The prereg text says "monotonic increase from n=10 to n=20" suggesting the author intended to test from n=10 onward. This is a specification design flaw.

## Product Consequence

Under the frozen rule, MEASUREMENT_INVALID provides no validated product decision. The empirical CDF approach does not yield a usable extrapolation model. The Intel lane should consider:

1. **Pivoting to Docker-based direct full-DOM measurement** (EXP-INTEL-35462974425) — four consecutive model-based approaches have now failed to produce validated extrapolations.
2. **Fitting a saturating parametric model** (logistic, Hill function, Richards) to the 4-point data to capture the step-function structure — but this is outside the frozen non-parametric spec.
3. **Resolving the C2 specification flaw** — if the prereg intent was monotonicity from n=10 onward, a corrected decision rule would yield C1=PASS, C2=PASS, C3=FAIL → EMPIRICAL_CDF_PREDICTS_CROSSING, which justifies Docker re-collection.

## Comparison to Prior Models

| Model | n=15 residual | n=20 residual | R2 | Verdict |
|-------|-------------|-------------|-----|---------|
| B1: Phi(median/std) | 34.59pp | 18.96pp | — | REJECTED |
| B2: Sign-fraction power law | 12.39pp | 7.41pp | 0.8797 | REJECTED |
| B3: Phi(mean/std) | — | 17.84pp | — | REJECTED |
| B4: Diagnostic indicator | 0.00pp | 0.00pp | — | Near-exact |
| **Empirical CDF** | **0.00pp** | **0.00pp** | **—** | **IDENTICAL to B4** |

The empirical CDF mapping adds no predictive value beyond the already-known diagnostic indicator. Both parametric and non-parametric modeling approaches have now failed to produce a validated extrapolation model.
