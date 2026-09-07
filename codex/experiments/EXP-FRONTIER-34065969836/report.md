# EXP-FRONTIER-34065969836 Report

## 1. Executive Summary

**Decision: FALSIFIED-IN-SETTING**

TV distance detection fails to generalize uniformly across 10D non-Gaussian function families. While aggregate monotonicity holds (Spearman ρ=1.0, p<0.001), the scaling function (family B) shows negligible TV response to lambda (ρ=-0.07, p=0.57), causing a significant function × lambda interaction (ANOVA p≈0.0). The 2D Gaussian result does not straightforwardly extend to 10D non-Gaussian settings.

## 2. Raw Evidence

### 2.1 TV Distance by Lambda (kNN k=20, Aggregate)

| λ | TV_max (mean ± SE) |
|---|---------------------|
| 0.0 | 0.5227 ± 0.015 |
| 0.1 | 0.5239 ± 0.015 |
| 0.2 | 0.5280 ± 0.016 |
| 0.3 | 0.5306 ± 0.016 |
| 0.4 | 0.5357 ± 0.016 |
| 0.5 | 0.5484 ± 0.017 |
| 0.7 | 0.5748 ± 0.018 |
| 1.0 | 0.6164 ± 0.020 |

### 2.2 Per-Function TV at Key Lambda Levels

| Function | λ=0.0 | λ=0.5 | λ=1.0 | Separation | Spearman ρ | Monotonic |
|----------|-------|-------|-------|------------|------------|-----------|
| 42 (rotation) | 0.5243 | 0.5439 | 0.5826 | 0.058 | 0.833 | No |
| 43 (scaling) | 0.5237 | 0.5164 | 0.5456 | 0.022 | -0.071 | No |
| 44 (translation) | 0.5203 | 0.5849 | 0.7211 | 0.201 | 1.000 | Yes |

### 2.3 Multi-Scale kNN Analysis

| k | Spearman ρ | Monotonic |
|---|------------|-----------|
| 5 | 0.976 | No |
| 10 | 1.000 | Yes |
| 20 | 1.000 | Yes |
| 50 | 0.881 | No |

Monotonic at 2/4 scales (k=10, k=20).

### 2.4 PCA-Projected Binned TV (Secondary)

| λ | PCA TV (mean ± SE) |
|---|---------------------|
| 0.0 | 0.5799 ± 0.038 |
| 0.1 | 0.4566 ± 0.033 |
| 0.2 | 0.4704 ± 0.030 |
| 0.3 | 0.5013 ± 0.027 |
| 0.4 | 0.5439 ± 0.036 |
| 0.5 | 0.5881 ± 0.029 |
| 0.7 | 0.6421 ± 0.029 |
| 1.0 | 0.7173 ± 0.036 |

PCA TV Spearman ρ=0.762 (p=0.014). Note: PCA TV at λ=0 is anomalously high (0.58) due to marginal distribution non-uniformity after projection.

### 2.5 Clipping Fractions

| Function | λ=0.0 | λ=0.5 | λ=1.0 |
|----------|-------|-------|-------|
| 42 (rotation) | 2.3% | 25.9% | 49.8% |
| 43 (scaling) | 2.5% | 25.1% | 48.6% |
| 44 (translation) | 2.5% | 25.7% | 49.3% |

~50% of transitions are clipped at λ=1, creating edge mass that may inflate TV.

## 3. Derived Measurements

### 3.1 Effect Sizes

- Aggregate Cohen's d (λ=0 vs λ=1): 1.571
- Per-function: rotation d=2.088, scaling d=0.846, translation d=9.111

The scaling function has a substantially smaller effect size (d=0.85) compared to rotation (d=2.09) and translation (d=9.11), explaining the function-invariance failure.

### 3.2 kNN Distance Diagnostics

- Fraction finite distances: 1.000 (all distances computable)
- Max kNN distance: 1.158
- Median kNN distance (k=20): 0.582
- Assessment: PASS — no distance degeneracy in 10D

### 3.3 Permutation Tests

- λ=0: mean p=0.573 (PASS — TV not significantly > 0)
- λ=1: mean p=0.141 (not significant at α=0.05 with 200 permutations)

Note: λ=1 permutation test uses only 200 permutations per cell for speed; the mean p=0.141 is borderline. With 1000 permutations, this would likely be significant for translation but not for scaling.

## 4. Decision Assessment

### 4.1 Condition Checklist

| Condition | Threshold | Observed | Pass |
|-----------|-----------|----------|------|
| Aggregate Spearman ρ | ≥ 0.65, p < 0.05 | ρ=1.0, p≈0 | ✅ |
| Positive control | TV(λ=1) > TV(λ=0) all functions | All pass | ✅ |
| Null control | Permutation p > 0.05 at λ=0 | p=0.573 | ✅ |
| Function invariance | ANOVA interaction p > 0.05 | p≈0.0 | ❌ |
| Multi-scale monotonicity | ≥ 2 of 3 scales monotonic | 2/4 monotonic | ✅ |
| No pipeline errors | — | — | ✅ |

### 4.2 Why Function Invariance Fails

The scaling function (family B) produces state-dependent scaling transformations that, in 10D, generate action-conditional distributions with minimal separability. The TV response (0.524→0.546, separation=0.022) is an order of magnitude weaker than translation (0.520→0.721, separation=0.201).

**Root cause**: State-dependent scaling in 10D compresses/expands the state space uniformly along all dimensions, but the action-dependent component (which dimension drives the scaling) only modulates the scale factor by ±20% of the state value. With 10D state and heteroscedastic mixture noise, this subtle modulation is overwhelmed by noise, producing near-random action-conditional distributions.

In contrast, translation adds an explicit offset proportional to the state value, creating larger separations between action-conditional distributions.

### 4.3 Aggregate vs Per-Function Tension

The aggregate Spearman ρ=1.0 is misleading: it reflects the weighted average of translation (ρ=1.0, strong signal), rotation (ρ=0.83, moderate signal), and scaling (ρ=-0.07, no signal). The aggregate test passes because 2 of 3 functions show strong monotonicity, but this masks the scaling function's complete failure.

The preregistered decision rule requires function invariance (ANOVA interaction p>0.05) precisely to detect this scenario. The significant interaction (p≈0) indicates the TV response is not uniform across function families.

## 5. Comparison with Parent Experiment (EXP-FRONTIER-34061241004)

| Metric | Parent (2D Gaussian) | This (10D Non-Gaussian) |
|--------|---------------------|------------------------|
| Aggregate ρ | 1.0 | 1.0 |
| Cohen's d | 20.3 | 1.6 |
| Function invariance | PASS (p=0.86) | FAIL (p≈0) |
| TV at λ=0 | 0.281 | 0.523 |
| TV at λ=1 | 0.849 | 0.616 |
| TV range | 0.568 | 0.094 |

Key differences:
1. **Noise floor doubled**: 10D mixture noise creates TV floor ~0.52 vs 0.28 in 2D Gaussian
2. **Signal range compressed**: TV range 0.094 in 10D vs 0.568 in 2D (6× reduction)
3. **Function heterogeneity**: 2D Gaussian showed uniform function response; 10D non-Gaussian does not
4. **Effect size reduced**: Cohen's d=1.6 vs 20.3 (13× reduction)

## 6. Product Consequences

### 6.1 Negative Outcome Implications

The hypothesis that TV distance generalizes from 2D Gaussian to 10D non-Gaussian settings is **falsified in the specific setting tested**. The claim ceiling for C-WEB-DYNAMICS regarding TV detection remains bounded to:

- 2D continuous state spaces
- Gaussian (or Gaussian-like) heteroscedastic noise
- Function families with sufficient action-conditional separability

### 6.2 What Survives

- TV monotonicity at the **aggregate level** in 10D (ρ=1.0, p<0.001)
- TV detectability for **translation-like** functions in 10D (ρ=1.0, d=9.1)
- kNN-based TV estimation works in 10D without distance degeneracy
- PCA-projected TV also shows monotonicity (ρ=0.76, p=0.014)

### 6.3 What Fails

- Uniform function invariance in 10D non-Gaussian settings
- Scaling-type transformations in 10D (negligible TV response)
- Direct transfer of 2D effect sizes to 10D (13× reduction)

## 7. Validity Notes

1. **Clipping artefact**: ~50% of transitions clipped at λ=1, creating edge mass. This may inflate TV by making action-conditional distributions more concentrated at boundaries. The true separation may be smaller than observed.
2. **kNN bandwidth sensitivity**: Monotonicity holds at k=10,20 but not k=5,50. The finding is not fully robust to bandwidth choice.
3. **Permutation test power**: 200 permutations per cell may be insufficient for λ=1 detection. Full 1000-permutation tests recommended for audit.
4. **Deterministic function choice**: Only 3 families tested. The scaling function's failure may be specific to the 10D parameterization chosen.
5. **Non-Gaussian noise model**: Mixture of 3 Gaussians is simpler than real Web noise. More complex noise may further degrade TV.

## 8. Unresolved Questions

1. Does the scaling function failure generalize to other scaling-type transformations in 10D?
2. Would bias-corrected TV (subtracting ~0.52 floor) preserve aggregate monotonicity?
3. Does TV work on real Web transitions, or is the synthetic-to-real gap insurmountable?
4. Can alternative high-dimensional TV estimators (KDE, neural density estimation) detect scaling-type structure?
5. Is the 50% clipping fraction a major confound or a minor artefact?

## 9. Artifacts

| Path | Role |
|------|------|
| research/frontier/highdim_nongaussian_tv/analyze.py | Code |
| research/frontier/highdim_nongaussian_tv/raw_tables.json | Raw |
| research/frontier/highdim_nongaussian_tv/result.json | Derived |
| research/frontier/highdim_nongaussian_tv/provenance.json | Derived |
