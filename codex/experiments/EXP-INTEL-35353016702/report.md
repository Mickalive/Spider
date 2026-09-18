# EXP-INTEL-35353016702 — 3-recipe OECD/COINr framework analysis

## Executive Summary

**FALSIFIED-IN-SETTING**: The meta-analytic mean recipe (canonical + weighted)/2 does NOT break the 2-recipe dominance degeneracy. All 3 pairwise dominance comparisons remain strictly degenerate (0% or 100%). The 2-recipe degeneracy is NOT a mathematical artifact of having exactly 2 alternatives — it persists with 3 recipes because the meta-analytic mean always ranks between the two originals by mathematical construction.

## Frozen Design

- **Experiment**: EXP-INTEL-35353016702
- **Lane**: intel
- **Claim**: C-MEAS-VALID
- **Data source**: Truncated-first-20 locatable_sample from EXP-INTEL-34782350557
- **Scope**: 7 tasks × 3 definitions × 3 recipes = 63 pairwise comparisons

## Results

### Density Matrix

| Recipe | Mean Density | Range |
|--------|-------------|-------|
| Canonical (p=0.5) | 0.006 | 0.0004 – 0.009 |
| Weighted (area) | 0.195 | 0.003 – 0.301 |
| Mean ((C+W)/2) | 0.101 | 0.002 – 0.154 |

The canonical recipe produces near-zero densities because p=0.5 independent inclusion on a sparse locatable sample (20 elements) yields very low expected counts. The weighted recipe produces much higher densities because area-based weighting amplifies the signal from larger elements.

### Dominance Pairs

| Comparison | Dominance A | Dominance B | Status |
|-----------|-------------|-------------|--------|
| canonical vs weighted | 0.0% | 100.0% | DEGENERATE |
| canonical vs mean | 0.0% | 100.0% | DEGENERATE |
| weighted vs mean | 100.0% | 0.0% | DEGENERATE |

**Zero non-degenerate dominance pairs.** All 3 comparisons are strictly degenerate.

### Ranking Analysis

The meta-analytic mean recipe ranks EXACTLY between canonical and weighted on ALL 21 task-definition pairs:
- Position 0 (highest): weighted (21/21 pairs)
- Position 1 (middle): mean (21/21 pairs)
- Position 2 (lowest): canonical (21/21 pairs)

**Zero ranking changes.** The mean recipe never produces a ranking that differs from the canonical-weighted ordering.

### Null Control

Shuffling the mean recipe's density values across task-definition pairs produces ~1.988 non-degenerate pairs on average (std=0.109). The real mean recipe produces 0 non-degenerate pairs. The real value is BELOW the null mean, confirming the meta-analytic mean is maximally uninformative.

### Decision Rule Evaluation

| Criterion | Threshold | Observed | Result |
|-----------|-----------|----------|--------|
| C1_FRAMEWORK_VALID | >=80% valid | 100% (63/63) | PASS |
| C2_NONDEGENERATE_EXISTS | >=1 non-degenerate | 0/3 | **FAIL** |
| C3_THIRD_RECIPE_DISTINCT | >=3 ranking changes | 0/21 | **FAIL** |
| C4_NULL_CONTROL_PASSES | real > shuffled | 0 < 1.988 | **FAIL** |

**Verdict**: FALSIFIED-IN-SETTING (C1 passes, C2 fails)

## Interpretation

### Why the Meta-Analytic Mean Fails

The failure is **mathematical, not empirical**. For any two numbers x < y:
- x < (x+y)/2 < y (always true)
- (x+y)/2 never equals x or y (unless x = y)

Since canonical density < weighted density on ALL 21 task-definition pairs:
- canonical < mean < weighted (always)
- mean never equals canonical or weighted
- mean always ranks between them

This means:
1. canonical vs mean: canonical always loses (0% dominance)
2. mean vs weighted: mean always loses (0% dominance)
3. canonical vs weighted: canonical always loses (0% dominance)

The 2-recipe degeneracy (0%/100% dominance) persists with 3 recipes.

### Implications for C-MEAS-VALID

The 2-recipe degeneracy is NOT a mathematical artifact of having exactly 2 alternatives. It is a property of the density metric's extreme recipe sensitivity: canonical produces ~0.006, weighted produces ~0.195, and any linear combination falls between them.

The MIXED outcome decision rule CANNOT be resolved by adding more linear combination recipes. The density metric lacks sufficient task-dependent recipe sensitivity to produce non-degenerate dominance with linear combinations.

### What Would Break the Degeneracy

A **non-linear** third recipe might break the degeneracy if it produces rankings that sometimes fall outside the canonical-weighted range. Examples:
- A recipe that weights elements by DOM hierarchy depth (structural, not area-based)
- A recipe that uses a different probability model (e.g., conditional inclusion based on element relationships)
- A recipe that weights elements by their semantic role rather than their bounding box

However, this would require defining and implementing a structurally different recipe, not a simple linear combination.

### Product Consequence

**Negative**: The MIXED outcome decision rule remains unresolved. The density metric program must either:
1. Adopt an alternative approach (density ratio, ranking reversal rate)
2. Restrict density metric use to recipe-insensitive task-definition pairs (if any exist)
3. Await a fundamentally different third recipe (not a linear combination)
4. Abandon dominance-based MIXED outcome handling entirely

C-MEAS-VALID status remains EXPERIMENTAL. This experiment attempted framework operationalization, not empirical measurement validation.

## Claim Ceiling

Bounded to:
- Truncated-first-20 locatable_sample (7 tasks, 1 site, 3 definitions)
- Meta-analytic mean recipe (simplest possible third recipe)
- OECD/COINr dominance framework
- Linear combination third recipe

NOT generalizable to:
- Non-linear third recipes
- Full DOM enumeration (BLOCKED by runtime substrate)
- Cross-site generalization
- Alternative MIXED outcome frameworks
