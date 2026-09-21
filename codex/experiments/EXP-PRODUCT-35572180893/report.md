# EXP-PRODUCT-35572180893 — Execution Report

## Summary

**Outcome: FALSIFIES** — The freshness guard discriminating operating point hypothesis is falsified under genuine Gaussian overlap.

**Primary falsification reason**: Orthogonality (TOST delta=0.15) breaks at 50% overlap (TOST CI upper = 0.168 > 0.15, pearson r = 0.080). This violates the spec.json decision rule condition (c): "orthogonality breaks at any condition."

**Secondary falsification reason** (prereg.md step 4): Calibrated threshold is None at 75% and 100% overlap — no threshold in the 50-point grid satisfies both TPR>=0.85 and FPR<=0.10 at those conditions.

## What Was Measured

### Gaussian Overlap Verification

The Gaussian distribution design (failure N(0.295, 0.05), noise N(μ_noise, 0.05)) achieved empirical overlap close to targets:

| Condition | Target | Empirical | μ_noise |
|-----------|--------|-----------|---------|
| 0% | 0% | 0.42% | 0.095 |
| 25% | 25% | 23.75% | 0.1663 |
| 50% | 50% | 44.17% | 0.195 |
| 75% | 75% | 67.5% | 0.2237 |
| 100% | 100% | 96.25% | 0.295 |

This is a major improvement over the parent experiment (EXP-PRODUCT-35551517868) which used uniform-shift overlap and produced 0% actual overlap at the 25% and 50% conditions.

### Calibrated Threshold Response

| Overlap | Calibrated Threshold | Precision | Recall | F1 | FP Rate |
|---------|---------------------|-----------|--------|-----|---------|
| 0% | 0.20 | 0.996 | 1.000 | 0.998 | 0.42% |
| 25% | 0.25 | 0.950 | 0.942 | 0.946 | 5.0% |
| 50% | 0.27 | 0.944 | 0.913 | 0.928 | 5.42% |
| 75% | None | — | — | — | — |
| 100% | None | — | — | — | — |

The threshold DOES increase gradually among conditions with valid thresholds (0.20 → 0.25 → 0.27), confirming the hypothesis that the parent's flat-then-jump pattern was partly an artifact of the uniform-shift design. However, at 75% and 100% overlap, no valid operating point exists.

### FP at Baseline Threshold 0.20

| Overlap | FP Rate at 0.20 | TP Rate at 0.20 |
|---------|-----------------|-----------------|
| 0% | 0.42% | 100% |
| 25% | 23.75% | 99.17% |
| 50% | 44.17% | 99.17% |
| 75% | 67.5% | 97.5% |
| 100% | 96.25% | 98.75% |

FP binding below 75% is confirmed: at 25% overlap, 23.75% of noise samples exceed threshold 0.20. At 50% overlap, 44.17% do. This demonstrates that genuine distributional overlap produces false accepts at the baseline threshold.

### Orthogonality (TOST)

| Overlap | Pearson r | CI Upper | TOST Pass |
|---------|-----------|----------|-----------|
| 0% | -0.023 | 0.066 | YES |
| 25% | -0.029 | 0.061 | YES |
| 50% | 0.080 | 0.168 | **NO** |
| 75% | 0.046 | 0.135 | YES |
| 100% | -0.026 | 0.064 | YES |

The 50% overlap condition is the sole orthogonality failure. The behavioral freshness score becomes positively correlated with the structural signal (r=0.080), with the 90% CI upper bound (0.168) exceeding the TOST equivalence margin (delta=0.15).

This is a non-monotonic pattern: orthogonality holds at 0%, 25%, 75%, and 100% but fails at 50%. The 75% and 100% conditions have valid orthogonality despite having no calibrated threshold — suggesting that orthogonality and threshold validity are independent properties.

## Interpretation

### What the hypothesis got right

1. **Genuine overlap produces earlier FP binding**: The parent experiment found FP=0 at 25% and 50% overlap (due to the uniform-shift flaw). This experiment found FP=23.75% and FP=44.17% at those conditions, confirming that genuine distributional overlap does produce false accepts at the baseline threshold.

2. **Threshold increases gradually**: Among conditions with valid thresholds, the calibrated threshold increases from 0.20 to 0.25 to 0.27 — a gradual response, not the parent's flat-then-jump pattern.

### What falsifies the hypothesis

1. **Orthogonality breaks at 50% overlap**: The freshness guard's behavioral score becomes correlated with the structural signal at moderate overlap. This violates the assumption that the two dimensions are independent, which is foundational to the guard's design.

2. **No valid threshold at 75% and 100% overlap**: At high overlap, no operating point achieves both TPR>=0.85 and FPR<=0.10. The guard fundamentally cannot separate noise from failure when distributions overlap heavily.

### Implications for C-FRESHNESS

The discriminating operating point exists in a bounded range:
- **Usable**: 0%-25% overlap (valid threshold, orthogonality holds, FP binding is moderate)
- **Marginal**: 50% overlap (valid threshold exists but orthogonality fails)
- **Unusable**: 75%-100% overlap (no valid threshold)

In production, this means the freshness guard can discriminate noise from failure when the noise level is low relative to genuine failures (≤25% overlap). At moderate noise levels (50%), discrimination is possible but the independence assumption breaks down. At high noise levels (≥75%), the guard cannot operate effectively.

**C-FRESHNESS remains EXPERIMENTAL** — the hypothesis of a discriminating operating point under genuine overlap is partially supported but falsified by the orthogonality failure at 50% overlap.

## Note on Code vs. Frozen Decision Rule

The `run_experiment.py` code internally computed `overall_hypothesis_outcome: "HYPOTHESIS_SUPPORTED"` based on monotonicity (0.20 < 0.25 < 0.27) and FP binding (FP > 0 at 25% and 50%). This is correct for those two criteria.

However, the frozen spec.json decision_rule states the claim is FALSIFIED if "orthogonality breaks at any condition" (condition (c)). The prereg.md also states FALSIFIED if "calibrated_threshold is None at any condition" (step 4). Both conditions trigger. This result.json applies the frozen decision rule correctly, overriding the code's internal assessment.

The code's decision logic implemented steps 7-9 of the prereg decision tree but did not implement steps 4-6 (gate checks). This is a code bug, not a scientific ambiguity.
