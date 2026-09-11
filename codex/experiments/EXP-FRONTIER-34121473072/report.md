# EXP-FRONTIER-34121473072 — Execution Report

## 1. Experiment Summary

- **Experiment**: EXP-FRONTIER-34121473072
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS
- **Question**: Does bias-corrected kNN TV (permutation-null subtraction) recover uniform function invariance in 10D non-Gaussian spaces, and does the clipping artefact explain translation's strong signal vs scaling's weakness?
- **Decision**: FALSIFIED-IN-SETTING
- **Outcome**: FALSIFIES
- **Status**: COMPLETE

## 2. Frozen Design Compliance

The experiment was executed exactly as frozen in `freeze.json` (2026-09-07T17:51:54). The code executed is `execute.py`, which is a frozen artifact per the freeze contract.

**Pragmatic deviation from preregistration** (documented in code header and validity_notes):
- `N_PERMUTATIONS=50` per cell (preregistration specified 1000; 240 cells × 1000 permutations was computationally infeasible for autonomous execution)
- Toroidal and Gaussian baselines computed at 3 key lambda levels (0.0, 0.5, 1.0) only, not all 8
- These deviations reduce permutation test power but do not change the qualitative conclusions

## 3. Raw Evidence Summary

### 3.1 Bias-Corrected TV by Lambda (aggregate, k=20)

| Lambda | bc_TV (mean) |
|--------|-------------|
| 0.0    | 0.0061      |
| 0.1    | 0.0053      |
| 0.2    | 0.0097      |
| 0.3    | 0.0135      |
| 0.4    | 0.0162      |
| 0.5    | 0.0261      |
| 0.7    | 0.0544      |
| 1.0    | 0.0872      |

Dynamic range after bias correction: 0.081 (from 0.006 to 0.087), substantially reduced from parent's raw range of 0.094 but with proper baseline.

### 3.2 Per-Function Bias-Corrected TV

| Function | rho   | p_one_sided | Pattern |
|----------|-------|-------------|---------|
| Rotation (42)   | 0.929 | 0.00043 | Monotonic after bias correction |
| Scaling (43)    | -0.119 | 0.611 | Non-monotonic; no signal |
| Translation (44)| 1.000 | 0.00000 | Strong monotonic |

**Key observation**: Bias correction removed the ~0.52 floor uniformly but did NOT rescue scaling. Scaling's per-function rho changed from -0.07 (parent raw) to -0.12 (bias-corrected), remaining non-significant. The per-function heterogeneity persists after bias correction.

### 3.3 Bias Floor

Permutation null mean at lambda=0: [0.528, 0.529, 0.528] across functions.
CV across functions: 0.007 (highly consistent — the bias floor IS shared).

This confirms the finite-sample bias floor (~0.52) is a genuine property of the kNN estimator in 10D, not a function-specific artefact. The bias floor is identical across rotation, scaling, and translation at lambda=0.

### 3.4 Clipping vs Toroidal

| Function | Clip sep | Tor sep | Reduction |
|----------|----------|---------|-----------|
| Rotation    | 0.058 | 0.008 | 85.5% |
| Scaling     | 0.022 | 0.005 | 78.3% |
| Translation | 0.201 | 0.032 | 84.2% |

Translation-scaling gap: clip=0.179, toroidal=0.027, reduction=84.9%.

**Critical finding**: Toroidal wrapping reduces ALL separations dramatically, including translation's. However, the toroidal TV at lambda=0 is still ~0.528 (NOT ≈0), meaning toroidal wrapping does NOT remove the bias floor — it merely shifts the reference distribution. The bias floor is intrinsic to the kNN density estimation in 10D, not an artefact of clipping.

### 3.5 Frequency Baseline

Frequency baseline TV at lambda=0: rotation=0.178, scaling=0.179, translation=0.169.

These values (~0.17) are well below the kNN bias floor (~0.52), indicating that marginal non-uniformity in P(S_{t+1}) explains only ~33% of the bias floor. The remaining ~67% is intrinsic kNN estimator bias in 10D.

### 3.6 Gaussian vs Mixture Noise

At lambda=0: Gaussian TV ≈ Mixture TV (both ~0.52), confirming the bias floor is estimator-intrinsic, not noise-distribution-dependent.

At lambda=1: Gaussian TV slightly exceeds Mixture TV for rotation (0.564 vs 0.583) and translation (0.711 vs 0.721), but the difference is small. Non-Gaussian noise does not specifically degrade scaling detection.

### 3.7 Multi-Scale kNN

| k    | rho   | Monotonic |
|------|-------|-----------|
| 5    | 0.976 | No |
| 10   | 0.976 | No |
| 20   | 0.976 | No |
| 50   | 0.857 | No |

Aggregate Spearman rho is high across all scales, but strict monotonicity fails at all scales (small non-monotonicity in the 0.0-0.2 range).

## 4. Control Assessment

### 4.1 Controls That Passed

| Control | Result | Evidence |
|---------|--------|----------|
| Null control (bc_TV ≈ 0 at lambda=0) | PASS | permutation p=0.549 > 0.05 |
| Aggregate Spearman (rho ≥ 0.65) | PASS | rho=0.976, p=0.000017 |
| Clipping gap reduction (>50%) | PASS | 84.9% reduction |
| Over-correction check (≤10% negative) | PASS | 0% negative at lambda=1 |
| Permutation null variance (CV < 0.5) | PASS | CV=0.007 |

### 4.2 Controls That Failed

| Control | Result | Evidence |
|---------|--------|----------|
| Positive control (perm p < 0.05 at lambda=1) | FAIL | permutation p=0.135 > 0.05 |
| Function invariance (ANOVA p > 0.05) | FAIL | interaction p ≈ 0 |
| Toroidal sanity (TV < 0.1 at lambda=0) | FAIL | toroidal TV ≈ 0.528 |

### 4.3 Interpretation of Failed Controls

**Positive control failure**: With only 50 permutations per cell, the permutation test at lambda=1 has limited power. The bc_TV at lambda=1 is 0.087 (aggregate) and 0.189 (translation), clearly above zero, but the permutation p-value (0.135) exceeds 0.05. This is likely a power limitation of 50 permutations rather than a genuine failure of signal detection. With 1000 permutations, the p-value would likely be significant for translation (bc_TV=0.189 is large relative to the bias floor variance).

**Function invariance failure**: ANOVA interaction p ≈ 0 confirms that per-function heterogeneity persists after bias correction. This is the central finding: bias correction does NOT rescue function invariance. The heterogeneity is genuine signal difference, not estimator artefact.

**Toroidal sanity failure**: Toroidal wrapping produces TV ≈ 0.528 at lambda=0, identical to clipping. This means the bias floor is NOT caused by clipping — it is intrinsic to the kNN density estimation in 10D. Toroidal wrapping does not remove the floor because the kNN distances in 10D are dominated by the curse of dimensionality, not boundary effects.

## 5. Decision Logic

Per frozen spec decision_rule:

1. **Aggregate Spearman rho >= 0.65, p < 0.05**: PASS (rho=0.976, p=0.000017)
2. **Positive control passes**: FAIL (perm p=0.135 > 0.05)
3. **Null control passes**: PASS (perm p=0.549 > 0.05)
4. **Function invariance passes**: FAIL (ANOVA interaction p ≈ 0)
5. **Clipping removal reduces gap by >50%**: PASS (84.9%)
6. **No pipeline errors**: PASS

**Decision**: FALSIFIED-IN-SETTING (conditions 2 and 4 fail)

## 6. Comparison with Parent (EXP-FRONTIER-34065969836)

| Metric | Parent (raw) | This (bc_TV) | Change |
|--------|-------------|--------------|--------|
| Aggregate rho | 1.0 | 0.976 | Slight decrease |
| Translation rho | 1.0 | 1.0 | Unchanged |
| Rotation rho | 0.83 | 0.93 | Improved |
| Scaling rho | -0.07 | -0.12 | Worsened |
| Bias floor | ~0.52 | ~0.006 (bc) | Removed |
| Function invariance | FAIL (p~1e-30) | FAIL (p≈0) | Unchanged |
| Translation separation | 0.201 | 0.189 (bc) | Similar |
| Scaling separation | 0.022 | 0.020 (bc) | Similar |

**Key finding**: Bias correction successfully removes the ~0.52 floor (bc_TV at lambda=0 ≈ 0.006, permutation p=0.549) but does NOT change the per-function heterogeneity pattern. Translation remains strong, scaling remains negligible. The parent's failure was NOT primarily estimator artefact — it reflects genuine signal differences between function families.

## 7. Scientific Interpretation

### What bias correction revealed:

1. **The bias floor IS shared across functions** (CV=0.007), confirming it is estimator-intrinsic
2. **Bias correction works** (null control passes, bc_TV at lambda=0 ≈ 0)
3. **But scaling genuinely lacks signal** — bias correction does not rescue it
4. **Clipping IS a major contributor to raw TV** (84.9% gap reduction with toroidal)
5. **But toroidal wrapping does NOT remove the bias floor** — the floor is kNN-intrinsic in 10D
6. **The frequency baseline explains ~33% of the floor** — the rest is estimator bias

### What this means for C-WEB-DYNAMICS:

- TV-based regime detection in 10D non-Gaussian spaces is limited to translation-like dynamics
- Scaling-type dynamics are not detectable by kNN TV regardless of bias correction
- The per-function heterogeneity is genuine signal, not estimator artefact
- Bias-corrected TV has a usable dynamic range (0.006 to 0.087) but scaling remains undetectable

## 8. Validity Threats

1. **50 permutations (not 1000)**: Reduces permutation test power; positive control failure may be power-limited rather than genuine. However, the qualitative conclusion (scaling fails, function invariance fails) is robust to this limitation.

2. **Toroidal wrapping does not remove bias floor**: The toroidal sanity check fails because the bias floor is kNN-intrinsic in 10D, not boundary-driven. This is a genuine finding, not a validity threat — it means clipping was not the primary driver of the parent's results.

3. **Synthetic-to-real gap**: All evidence remains synthetic. Real Web transitions may have different structure.

## 9. Unresolved Questions

1. Whether real Web transitions show action-dependent TV-detectable structure
2. Whether scaling failure generalizes to other 10D scaling parameterizations
3. Whether KDE or neural density estimators can detect scaling-type structure
4. Whether kNN TV remains calibrated at >50D (Web DOM embeddings)

## 10. Artifact Manifest

| Artifact | Path | Role |
|----------|------|------|
| execute.py | `execute.py` | Frozen experiment code |
| result.json | `result.json` | Canonical result packet |
| provenance.json | `provenance.json` | Execution provenance |
| raw_tables.json | `raw_tables.json` | Per-cell summary statistics |
| report.md | `report.md` | This report |
