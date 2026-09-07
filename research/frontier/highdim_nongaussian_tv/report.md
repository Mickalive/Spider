# EXP-FRONTIER-34065969836: Report — 10D Non-Gaussian TV Distance Detection

## 1. Experiment Summary

**Question:** Does TV distance detect action-dependent dynamical structure in higher-dimensional (10D) continuous state spaces with non-Gaussian heteroscedastic noise?

**Design:** 10D state space [0,1]^10, 3 function families (rotation/scaling/translation generalized to 10D), 8 lambda levels, 10 replications, 500 transitions per cell, kNN-based TV in full 10D (no dimensionality reduction), PCA-projected binned TV as secondary.

**Decision:** FALSIFIED-IN-SETTING — function invariance condition fails (ANOVA interaction p=0.000). The scaling function shows no monotonic TV-lambda relationship (rho=-0.071, p=0.567), while rotation (rho=0.833, p=0.005) and translation (rho=1.0, p<0.001) show monotonic detection. The hypothesis that TV generalizes uniformly to 10D non-Gaussian settings is falsified by function heterogeneity.

## 2. Derived Measurements

### 2.1 Primary Test: Aggregate Spearman Correlation

| Metric | Value | Threshold | Pass |
|--------|-------|-----------|------|
| Aggregate Spearman rho | 1.0000 | >= 0.65 | YES |
| One-sided p-value | 0.000000 | < 0.05 | YES |

The aggregate test passes because pooling all functions recovers a monotonic trend. However, this masks critical per-function heterogeneity (Section 2.2).

### 2.2 Per-Function Analysis

| Function | Spearman rho | p (one-sided) | Monotonic | Cohen's d |
|----------|-------------|---------------|-----------|-----------|
| 42 (rotation) | 0.8333 | 0.0051 | No* | 2.09 |
| 43 (scaling) | -0.0714 | 0.5667 | No | 0.85 |
| 44 (translation) | 1.0000 | 0.0000 | Yes | 9.11 |
| Aggregate | 1.0000 | 0.0000 | Yes | 1.57 |

*Rotation shows a non-monotonic dip at lambda=0.2 (TV=0.5100) before recovering, but Spearman rho remains significant.

**Translation** produces the strongest signal: TV ranges from 0.520 (lambda=0) to 0.721 (lambda=1), a separation of 0.201. **Rotation** shows moderate signal: 0.524 to 0.583, separation 0.058. **Scaling** shows negligible signal: 0.524 to 0.546, separation 0.022 — essentially flat across all lambda levels.

### 2.3 TV Means by Lambda (kNN k=20, Aggregate)

| Lambda | TV Mean | Std Error |
|--------|---------|-----------|
| 0.0 | 0.5227 | 0.008 |
| 0.1 | 0.5239 | 0.006 |
| 0.2 | 0.5280 | 0.008 |
| 0.3 | 0.5306 | 0.008 |
| 0.4 | 0.5357 | 0.008 |
| 0.5 | 0.5484 | 0.010 |
| 0.7 | 0.5748 | 0.012 |
| 1.0 | 0.6164 | 0.014 |

The aggregate curve is monotonically increasing, but driven primarily by the translation function.

### 2.4 Multi-Scale kNN Analysis

| kNN Scale | Spearman rho | p (one-sided) | Monotonic |
|-----------|-------------|---------------|-----------|
| k=5 | 0.9762 | 0.000017 | No |
| k=10 | 1.0000 | 0.000000 | Yes |
| k=20 | 1.0000 | 0.000000 | Yes |
| k=50 | 0.8810 | 0.001925 | No |

Monotonicity holds at 2/4 scales (k=10, k=20). At k=5 and k=50, non-monotonicity appears due to the scaling function's flat response across all lambda levels. The signal is scale-dependent but present at intermediate k values.

### 2.5 Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| Positive (TV@1 > null) | Detectably above null | Separation: rot=0.058, scal=0.022, trans=0.201 | YES |
| Null (permutation p>0.05 at lambda=0) | p > 0.05 | p=0.573 | YES |
| Function invariance (ANOVA p>0.05) | p > 0.05 | p=0.000 | NO |
| Multi-scale monotonicity (>=2/4) | >=2 scales | 2/4 scales | YES |
| kNN distance diagnostics | >50% finite | 100% finite | YES |
| No pipeline errors | None | None | YES |

### 2.6 Secondary: PCA-Projected Binned TV

| Lambda | PCA TV Mean |
|--------|-------------|
| 0.0 | 0.5799 |
| 0.1 | 0.4566 |
| 0.2 | 0.4704 |
| 0.3 | 0.5013 |
| 0.4 | 0.5439 |
| 0.5 | 0.5881 |
| 0.7 | 0.6421 |
| 1.0 | 0.7173 |

PCA-projected TV Spearman rho=0.762 (p=0.014), showing monotonicity. The PCA approach is weaker than kNN (rho=0.762 vs 1.0) because it discards information in 8 of 10 dimensions. The non-monotonic dip at lambda=0.1 (TV=0.457) in PCA but not kNN suggests PCA information loss affects low-signal regimes.

### 2.7 Clipping Fractions

At lambda=1, approximately 49% of transitions are clipped to [0,1]^10 boundaries across all functions. This is substantial and may compress the signal, particularly for functions that produce larger state displacements (translation > rotation > scaling).

## 3. Interpretation

### 3.1 Why Function Invariance Fails

The scaling function (seed=43) applies state-dependent diagonal scaling centered at 0.5:
```
s_new[i] = scale_factor * (s[i] - 0.5) + 0.5 + offset[i]
```
where scale_factor = 1.0 + 0.2 * s[action_dim] * action_sign.

This transformation modifies magnitudes but preserves the relative ordering of state dimensions. In 10D, the scaling effect is distributed across all dimensions with small offsets (0.05 * s[i]), making the action-dependent shift small relative to the non-Gaussian noise (sigma_base ~0.05-0.15). The TV estimator cannot distinguish scaled from unscaled distributions at this signal-to-noise ratio.

By contrast, rotation (seed=42) applies Givens rotations that mix dimensions, creating directional shifts that are detectable by kNN. Translation (seed=44) adds state-dependent vectors with sin modulation, creating the strongest separability (Cohen's d=9.11).

### 3.2 Comparison with Parent Experiment (2D Gaussian)

| Metric | Parent (2D Gaussian) | This (10D Non-Gaussian) |
|--------|---------------------|------------------------|
| Aggregate rho | 1.000 | 1.000 |
| Aggregate Cohen's d | 20.30 | 1.57 |
| TV at lambda=0 | 0.281 | 0.523 |
| TV at lambda=1 | 0.849 | 0.616 |
| Function invariance | PASS (p=0.862) | FAIL (p=0.000) |
| TV range (0 to 1) | 0.568 | 0.094 |

The 10D non-Gaussian setting shows:
1. **Much smaller effect size** (d=1.57 vs 20.30): Non-Gaussian noise and high dimensionality severely reduce separability.
2. **Higher noise floor** (0.523 vs 0.281): The mixture noise creates larger baseline TV.
3. **Narrower signal range** (0.094 vs 0.568): The maximum TV separation is compressed.
4. **Function-dependent detection**: Only translation and rotation show monotonic TV; scaling does not.

### 3.3 What This Means for C-WEB-DYNAMICS

The hypothesis that TV distance generalizes uniformly to 10D non-Gaussian settings is **falsified in this specific setting**. However:

- **TV does detect action-dependent structure in 10D** for some transformation types (translation, rotation).
- **TV fails for scaling-type transformations** where the action-dependent shift is small relative to noise.
- **The aggregate test passes** because the translation function dominates the signal.

The claim ceiling is now: TV distance detects action-dependent structure in 10D non-Gaussian spaces **when the deterministic transformation produces directional shifts (rotation/translation) that exceed the noise floor**, but **not when the transformation produces only magnitude changes (scaling)**.

### 3.4 Validity Threats

1. **Clipping artefact**: 49% clipping at lambda=1 compresses tails and may inflate TV near boundaries. This could explain the high noise floor (0.523 at lambda=0).
2. **kNN bias in high dimensions**: kNN TV has different bias properties in 10D vs 2D. The noise floor of ~0.52 may reflect kNN estimation bias rather than true distribution overlap.
3. **Function choice**: Only 3 function families tested. The scaling family may be an outlier; other transformation types may behave differently.
4. **Sample size**: 500 transitions per cell (~125 per action) may be insufficient for kNN TV in 10D to achieve adequate power for all transformation types.

## 4. Product Consequences

### If Positive (SURVIVES_CURRENT_TEST)
- Demonstrates TV generalizes to 10D non-Gaussian settings
- Justifies TV-based regime detection for high-dimensional Web state spaces
- Product lane can begin integrating TV into exploration strategy

### If Negative (FALSIFIED-IN-SETTING) — OBSERVED
- TV detection in 10D is **transformation-dependent**: works for rotation/translation, fails for scaling
- The 2D result does NOT generalize uniformly to higher dimensions
- Product lane should NOT deploy TV-based regime detection for arbitrary high-dimensional state spaces without verifying the transformation type
- C-WEB-DYNAMICS remains HYPOTHESIS with a narrower claim ceiling: TV detects structure only when deterministic transformations produce directional shifts exceeding the noise floor
- Frontier lane should either (A) test on real Web data, (B) develop transformation-aware detection, or (C) accept TV limitation to specific DGP classes

## 5. Unresolved Questions

1. Does the scaling function failure generalize, or is it specific to the diagonal scaling DGP?
2. Does clipping to [0,1] contribute to the high noise floor (0.523 at lambda=0)?
3. Would bias-corrected kNN TV (permutation-null subtraction) preserve monotonicity for translation/rotation?
4. Does Gaussian (not mixture) noise in 10D produce better separation?
5. Can transformation-aware TV (separate analysis per transformation type) salvage the detection?

## 6. Decision Assessment

**FALSIFIED-IN-SETTING**: The frozen decision rule requires function invariance (ANOVA interaction p>0.05). The observed interaction p=0.000 fails this condition. The hypothesis that TV generalizes to 10D non-Gaussian settings with uniform function invariance is falsified.

**Bounded conclusion**: TV distance detects action-dependent structure in 10D non-Gaussian spaces for rotation and translation transformations but not for scaling. The aggregate Spearman rho=1.0 is driven by translation dominance, not uniform detection.
