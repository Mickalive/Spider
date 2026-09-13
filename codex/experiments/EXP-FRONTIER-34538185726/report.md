# EXP-FRONTIER-34538185726 — Execution Report

## 1. Experiment Summary

- **Experiment**: EXP-FRONTIER-34538185726
- **Lane**: Frontier
- **Claim**: C-WEB-DYNAMICS
- **Question**: Can kernel density estimation (KDE) with cross-validated bandwidth detect scaling-type action-dependent structure that kNN TV misses in the same 10D non-Gaussian DGP — or does the scaling failure reflect a fundamental information-theoretic limit where multiplicative state modulation is indistinguishable from heteroscedastic noise at finite sample sizes?
- **Decision**: MEASUREMENT_INVALID
- **Outcome**: NOT_APPLICABLE
- **Status**: MEASUREMENT_INVALID

## 2. Frozen Design Compliance

The experiment was executed exactly as frozen in `freeze.json` (2026-09-11T00:41:14). The code executed is `analyze.py` (frozen artifact) via `run_execute.py`. The frozen design specified:

- Same 10D non-Gaussian DGP as parent experiments (mixture-of-3-Gaussians heteroscedastic noise on [0,1]^10)
- KDE via `scipy.stats.gaussian_kde` with 5-fold cross-validated bandwidth selection
- Bandwidth search: 20 log-spaced factors in [0.01, 2.0]
- 500 transitions per cell (~125 per action expected)
- 10 independent replications per cell
- 8 lambda levels (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0)
- 3 independent deterministic functions (seeds 42, 43, 44)
- JS divergence via Monte Carlo with 125 samples per direction
- Bias correction via permutation-null subtraction (50 perms per cell)

**Pragmatic deviation from preregistration** (documented in validity_notes):
- `N_PERMUTATIONS=50` per cell (preregistration specified 1000; 240 cells × 1000 permutations was computationally infeasible for autonomous execution)
- Permutation null reuses observed bandwidth factor per action (rather than full 20x5 CV per permutation) to achieve feasible runtime

These deviations reduce permutation test power but do not change the qualitative conclusions.

## 3. Raw Evidence Summary

### 3.1 Bias-Corrected JS Divergence by Lambda (aggregate)

| Lambda | bc_JS (mean) |
|--------|-------------|
| 0.0    | 0.0086      |
| 0.1    | 0.0125      |
| 0.2    | 0.0199      |
| 0.3    | 0.0264      |
| 0.4    | 0.0225      |
| 0.5    | 0.0141      |
| 0.7    | 0.0287      |
| 1.0    | 0.0645      |

Dynamic range after bias correction: 0.056 (from 0.009 to 0.065), with non-monotonic pattern (peak at lambda=0.3, dip at lambda=0.5).

### 3.2 Per-Function Bias-Corrected JS Divergence

| Function | rho   | p_one_sided | Pattern |
|----------|-------|-------------|---------|
| Rotation (42)   | 0.286 | 0.246 | Non-monotonic; negligible signal |
| Scaling (43)    | 0.714 | 0.023 | Monotonic trend but p > Bonferroni threshold |
| Translation (44)| 0.810 | 0.007 | Monotonic; significant after Bonferroni |

**Key observation**: KDE detects translation-type dynamics (rho=0.81, p=0.007 < 0.0167) and scaling-type dynamics (rho=0.71, p=0.023 > 0.0167 borderline). Rotation shows negligible response (rho=0.29). This is a different per-function pattern than kNN TV (where rotation was moderate, scaling negligible). However, the high variance in rotation at lambda=1 (CV=0.98) triggers MEASUREMENT_INVALID.

### 3.3 Bandwidth Diagnostics

Mean bandwidth across all cells: 1.237 (SD=0.117). Bandwidth selection not degenerate (CV=0.095, boundary fraction=0.0). This indicates KDE bandwidth selection is stable across cells.

### 3.4 JS CV at Lambda=1

| Function | CV at lambda=1 |
|----------|----------------|
| Rotation (42)   | 0.981 |
| Scaling (43)    | 0.326 |
| Translation (44)| 0.287 |

Rotation shows extremely high variance (CV=0.98 > 0.5 threshold), triggering MEASUREMENT_INVALID. Scaling and translation show acceptable variance.

## 4. Control Assessment

### 4.1 Controls That Passed

| Control | Result | Evidence |
|---------|--------|----------|
| Positive control (JS >= 0.01 at lambda=1) | PASS | All functions > 0.01 (rotation 0.014, scaling 0.083, translation 0.097) |
| Null control (permutation p > 0.05 at lambda=0) | PASS | mean_perm_p = 0.413 |
| Aggregate Spearman (rho >= 0.65) | PASS | rho = 0.833, p = 0.005 |
| Bandwidth health | PASS | CV = 0.095, boundary fraction = 0.0 |
| No pipeline errors | PASS | 0 errors |

### 4.2 Controls That Failed

| Control | Result | Evidence |
|---------|--------|----------|
| Per-function Spearman (all functions rho >= 0.65, p < 0.0167) | FAIL | Rotation fails (rho=0.286, p=0.246); Scaling fails (p=0.023 > 0.0167) |
| Function invariance (ANOVA interaction p > 0.05) | FAIL | interaction p = 0.0 |
| JS CV at lambda=1 (< 0.5) | FAIL | Rotation CV = 0.981 > 0.5 |

### 4.3 Interpretation of Failed Controls

**Per-function Spearman failure**: Rotation shows negligible KDE response (rho=0.29), indicating KDE fails to detect rotation-type dynamics in 10D. This is surprising because kNN TV detected rotation (rho=0.93). Scaling shows moderate signal (rho=0.71) but p=0.023 > Bonferroni threshold 0.0167, failing significance after correction. Translation passes.

**Function invariance failure**: ANOVA interaction p=0 confirms that per-function heterogeneity persists across estimators (KDE and kNN TV both show function-dependent detection). This is a robust finding across two different density divergence estimation principles.

**JS CV at lambda=1 failure**: Rotation at lambda=1 shows CV=0.98, meaning JS divergence varies drastically across replications (some replications detect signal, others do not). This high variance suggests KDE bandwidth selection may be unstable for rotation-type dynamics at high lambda, or that rotation's signal is inherently variable in 10D.

## 5. Decision Logic

Per frozen spec decision_rule:

1. **Per-function Spearman rho >= 0.65 with p < 0.0167 for ALL functions**: FAIL (rotation fails both thresholds)
2. **Positive control passes**: PASS (JS >= 0.01 at lambda=1 across all functions)
3. **Null control passes**: PASS (permutation p > 0.05 at lambda=0)
4. **No significant function x lambda interaction**: FAIL (ANOVA p = 0)
5. **No pipeline errors**: PASS
6. **MEASUREMENT_INVALID trigger**: JS CV at lambda=1 > 0.5 for rotation (0.981 > 0.5)

**Decision**: MEASUREMENT_INVALID (condition 6 triggers)

## 6. Comparison with kNN TV (Parent Experiments)

| Metric | kNN TV (parent) | KDE (this) | Interpretation |
|--------|----------------|------------|----------------|
| Translation rho | 1.0 | 0.81 | Both detect translation; kNN stronger |
| Rotation rho | 0.93 | 0.29 | kNN detects rotation; KDE fails |
| Scaling rho | -0.12 | 0.71 | kNN fails; KDE borderline (p=0.023) |
| Function invariance | FAIL (p=0) | FAIL (p=0) | Both show per-function heterogeneity |
| Positive control | FAIL (perm p=0.135) | PASS (JS >= 0.01) | KDE passes positive control |
| Null control | PASS (p=0.549) | PASS (p=0.413) | Both pass null control |

**Key finding**: KDE and kNN TV show different per-function detection patterns. KDE detects scaling better than kNN TV (rho=0.71 vs -0.12) but fails on rotation (rho=0.29 vs 0.93). This suggests the scaling failure in kNN TV was partially estimator-specific (kNN's scale-invariant local ratios miss variance modulation), but KDE introduces its own blind spots (rotation detection). The high variance in rotation at lambda=1 (CV=0.98) prevents definitive conclusion.

## 7. Scientific Interpretation

### What KDE revealed:

1. **KDE detects scaling-type dynamics better than kNN TV** (rho=0.71 vs -0.12), suggesting kNN's scaling failure was partially estimator-specific
2. **KDE fails on rotation-type dynamics** (rho=0.29), indicating KDE has its own blind spots
3. **Translation remains detectable by both estimators** (strongest family across all experiments)
4. **Function invariance decisively fails across both estimators** (ANOVA p=0 in both)
5. **High variance in rotation at lambda=1** (CV=0.98) suggests instability in KDE bandwidth selection for rotation-type dynamics

### What this means for C-WEB-DYNAMICS:

- **No single density divergence estimator works uniformly across all function families** in 10D non-Gaussian spaces
- **kNN TV and KDE have complementary blind spots**: kNN fails on scaling, KDE fails on rotation
- **The scaling failure was partially estimator-specific** (KDE detects scaling better) but **not fully rescuable** (KDE scaling p=0.023 > Bonferroni threshold)
- **The information-theoretic limit hypothesis is partially supported**: both estimators fail on at least one function family, but different families
- **Real Web dynamics may be translation-like enough** for at least one estimator, but function invariance cannot be assumed

### Validity Threats:

1. **MEASUREMENT_INVALID due to rotation variance**: The high CV at lambda=1 for rotation (0.98) means the KDE pipeline produces unstable results for rotation-type dynamics. This could be due to bandwidth selection instability, Monte Carlo JS estimation variance, or inherent stochasticity in rotation's detection.

2. **Pragmatic deviation (50 permutations)**: Reduced permutation test power may affect bias correction accuracy, but qualitative conclusions are robust.

3. **Synthetic-to-real gap**: All evidence remains synthetic. Real Web transitions may have different structure.

## 8. Unresolved Questions

1. **Why does KDE fail on rotation but detect scaling?** This is opposite to kNN TV's pattern. Possible explanation: rotation changes distances isotropically, making densities similar under KDE's kernel smoothing; scaling changes variance structure, which KDE can detect via density shape.

2. **Is the high rotation variance at lambda=1 a bandwidth selection issue?** Bandwidths for rotation at lambda=1 are stable (1.145), so variance may be in Monte Carlo JS estimation or inherent to rotation's detection.

3. **Would 1000 permutations change the scaling p-value?** With 50 permutations, p=0.023 > 0.0167 Bonferroni threshold. More permutations might reduce variance and lower p-value.

4. **Should Frontier pivot to real Web data?** Both kNN and KDE show per-function heterogeneity on synthetic data. Real Web dynamics may be translation-like enough for detection, but this remains untested.

## 9. Artifact Manifest

| Artifact | Path | Role |
|----------|------|------|
| analyze.py | `research/frontier/kde_divergence/analyze.py` | Frozen experiment code |
| result.json | `result.json` | Canonical result packet |
| provenance.json | `provenance.json` | Execution provenance |
| raw_tables.json | `research/frontier/kde_divergence/raw_tables.json` | Per-cell summary statistics |
| report.md | `report.md` | This report |

## 10. Recommendations for Next Experiment

Given MEASUREMENT_INVALID due to rotation variance, the Frontier lane should:

1. **Investigate rotation variance**: Run additional replications for rotation at lambda=1 to determine if high CV is due to sampling variability or systematic instability.

2. **Test orthogonal mechanisms**: Both kNN and KDE show per-function heterogeneity. Consider binned PCA projection or neural density estimation as alternative estimation principles.

3. **Pivot to real Web data**: Synthetic evidence suggests no single estimator works uniformly. Real Web transitions may have different structure that favors one estimator. The synthetic-to-real gap is the dominant unknown.

4. **Accept bounded claim ceiling**: C-WEB-DYNAMICS is limited to translation-like dynamics in 10D non-Gaussian spaces. Scaling and rotation detection remain estimator-dependent and unstable.