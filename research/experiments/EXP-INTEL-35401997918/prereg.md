# EXP-INTEL-35401997918 Preregistration

## Experiment Identity

- **Experiment ID**: EXP-INTEL-35401997918
- **Lane**: intel
- **Parent Experiment**: EXP-INTEL-35375593989 (verdict: FALSIFIED-IN-SETTING, audit: FAIL)
- **Parent Handoff**: `research/experiments/EXP-INTEL-35375593989/handoff.json`
- **Created**: 2026-09-18

## Claims

- **Claim IDs**: C-MEAS-VALID

## Scientific Context

### What is established (from parent handoff)

1. **Recipe choice is MATERIAL**: 31x canonical/weighted density gap (EXP-INTEL-35264637598)
2. **Linear combinations CANNOT break OECD/COINr degeneracy**: mathematical identity — (canonical+weighted)/2 always ranks between originals (EXP-INTEL-35353016702)
3. **Within each recipe, definitions are highly correlated**: Spearman r > 0.98 (EXP-INTEL-3330747199)
4. **Canonical per-iteration p=0.5 is principled** (EXP-INTEL-35264637598)
5. **Density ratio R = canonical/weighted varies 17x (CV=0.70)** across 21 task-definition pairs but variation is definition-driven (10x between DEF-FORM-ONLY and DEF-FULL-MAP), not task-type-driven (1.78x) (EXP-INTEL-35375593989 audit)
6. **Spearman correlations between density ratio and task-type/recipe-sensitivity proxies are non-significant** (|rho|<0.23, p>0.30) with correct task-major ordering (EXP-INTEL-35375593989 audit VF-1)
7. **Task-type structure in density ratio is not statistically significant** (eta-squared=0.144 < 0.20 threshold; permutation p=0.23) (EXP-INTEL-35375593989 audit VF-2)

### What is rejected

1. OECD/COINr framework with 2 recipes is NOT informative (construct failure) (EXP-INTEL-35330747199)
2. Linear third recipe CANNOT break degeneracy — mathematical identity (EXP-INTEL-35353016702)
3. SURVIVES_REVERSAL_PERSISTS decision rule not achievable (EXP-INTEL-35264637598)
4. Density ratio R = canonical/weighted as MIXED outcome decision rule — falsified: definition-driven variation, non-significant task-type correlation (EXP-INTEL-35375593989)

### What is unknown (from parent handoff)

1. Would a structurally non-linear third recipe (DOM hierarchy, semantic weighting, conditional inclusion) break the ordering constraint that linear combinations cannot? **← THIS EXPERIMENT ADDRESSES THIS**
2. Is MIXED outcome resolvable at all within the OECD/COINr framework, or should it be abandoned entirely?
3. Full-DOM generalization of density values and ratios — blocked by runtime lane removing locatableSample cap
4. Cross-site generalization of ratio/threshold behavior — blocked by cross-site data availability
5. Whether the density ratio captures genuine recipe sensitivity or just definition artifact — partially answered (definition artifact)

### What must not be assumed

- OECD/COINr framework has been validated for SPIDER — it has not
- 31x canonical/weighted ratio is validated on full DOM — only tested on truncated-first-20 sample
- FALSIFIED-IN-SETTING generalizes to full DOM — truncated sample may change density values
- Density metric is entirely useless — recipe choice is MATERIAL (31x canonical/weighted gap)
- Recipe choice is a nuisance parameter — it is MATERIAL (31x canonical/weighted gap)

## Question

Does a structurally non-linear third recipe (DOM hierarchy-depth weighting with exponential decay) produce density rankings outside the canonical-weighted convex hull, thereby breaking the 2-recipe degeneracy that blocks MIXED outcome resolution?

## Hypothesis

A DOM hierarchy-weighted density recipe, where element weight = exp(-alpha * depth) with depth measured from the root DOM node, produces a density ranking across task-definition pairs that is not bounded between the canonical and weighted recipe rankings. This would demonstrate that non-linear structural weighting can break the ordering constraint that linear combinations cannot.

## Falsifier

The non-linear recipe is falsified if ANY of:

- **F1**: The hierarchy-weighted density ranking is monotonically bounded between canonical and weighted rankings on all 21 pairs (i.e., for every pair, min(canonical_density, weighted_density) <= hierarchy_density <= max(canonical_density, weighted_density)), meaning the non-linear recipe fails to escape the convex hull.
- **F2**: |Spearman(hierarchy_density, canonical_density)| > 0.90 AND |Spearman(hierarchy_density, weighted_density)| > 0.90, meaning the non-linear recipe is effectively a linear combination of the existing two.
- **F3**: The hierarchy-weighted density has zero variance across all 21 pairs (CV < 0.01), meaning the recipe is constant and uninformative.

## Baselines

1. **B1_CANONICAL_RECIPE**: Canonical per-iteration p=0.5 density from EXP-INTEL-35264637598
2. **B2_WEIGHTED_RECIPE**: Area-weighted density from EXP-INTEL-35264637598
3. **B3_LINEAR_MEAN**: Meta-analytic mean (canonical+weighted)/2 — maximally degenerate (EXP-INTEL-35353016702)
4. **B4_DENSITY_RATIO**: Density ratio R = canonical/weighted — definition-driven (EXP-INTEL-35375593989)

## Positive Control

**PC1_HIERARCHY_VARIATION**: DOM hierarchy depth varies across page types (listing pages have deeper nesting than cart pages). The hierarchy-weighted density should reflect this structural difference. Expected: hierarchy-weighted density differs across listing/detail/cart task types, with at least one inter-type ratio > 1.1.

## Null Control

**NC1_RANDOM_WEIGHTS**: When element weights are randomly assigned (uniform [0,1] per element, seeded), the resulting density ranking should not show the non-linear structure of the hierarchy recipe. Expected: random-weight density has |Spearman(random, canonical)| < 0.30 AND |Spearman(random, weighted)| < 0.30. The hierarchy recipe should show stronger structure than random weights.

## Measurement Validity

1. Density values reconstructed from existing raw evidence (EXP-INTEL-34782350557 raw_results.json, sha256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050) for 7 tasks x 3 definitions x 2 recipes.
2. DOM hierarchy depth extracted from raw DOM structure in parent experiment's observation data. Each element's depth is its distance from the root `<html>` node.
3. Hierarchy-weighted density: sum(exp(-alpha * depth_i) * match_i) / sum(exp(-alpha * depth_i)) for alpha in {0.1, 0.3, 0.5}. Convex combination of element matches weighted by exponential depth decay. Weighting is structural (DOM tree position) not density-based.
4. Bounded to truncated-first-20 locatable_sample (7 tasks, 1 site Magento, 3 definitions).
5. All computations deterministic and reproducible from raw evidence artifact.
6. Alpha parameter swept to test sensitivity; primary analysis uses alpha=0.3.

## Decision Rule

Conjunctive:

- **C1_HIERARCHY_VARIATION**: CV of hierarchy-weighted density across all 21 pairs >= 0.10.
- **C2_OUTSIDE_CONVEX_HULL**: At least 3 of 21 pairs (>=14.3%) have hierarchy_density outside [min(canonical, weighted), max(canonical, weighted)].
- **C3_NOT_LINEAR_COMBINATION**: |Spearman(hierarchy, canonical)| < 0.90 OR |Spearman(hierarchy, weighted)| < 0.90.
- **C4_TASK_TYPE_STRUCTURE**: eta-squared(hierarchy_density, page_type) >= 0.10.

**Verdict rules:**
- C1 AND C2 AND C3 AND C4 → SURVIVES_CURRENT_TEST
- C1 AND C2 AND NOT C3 → MIXED
- C1 AND NOT C2 → FALSIFIED-IN-SETTING
- NOT C1 → FALSIFIED-IN-SETTING

## Product Consequence

**Positive**: MIXED outcome program gains a viable non-linear third recipe. Product lane can use 3-recipe classification instead of degenerate dominance.

**Negative**: MIXED outcome program is closed. Remaining options: (a) abandon density-based MIXED handling, restrict to recipe-insensitive pairs; (b) accept density metric recipe sensitivity is irreducible without fundamentally different metric.

## Estimated Cost

LOW — offline computation on existing reconstructed data. No browser/network work. Estimated < 2000 LLM tokens.

## Expected Information Gain

HIGH — directly resolves whether non-linear DOM structural weighting can break the convex hull constraint. Either outcome is decisive for the MIXED decision rule strategy.
