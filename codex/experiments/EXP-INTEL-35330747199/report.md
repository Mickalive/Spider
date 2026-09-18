# EXP-INTEL-35330747199: OECD/COINr Sensitivity Analysis on Density Metric Recipe Ambiguity

## Executive Summary

**Status:** COMPLETE | **Outcome:** MIXED | **Claim:** C-MEAS-VALID

The OECD/COINr sensitivity framework was applied to truncated-first-20 density data across 2 recipes × 3 definitions × 7 tasks. The frozen decision rule produced a MIXED outcome: C1 (framework validity), C3 (CI informativeness), C4 (classification discrimination), and C5 (null control) all passed, but C2 (dominance informativeness) failed because the framework is designed for ≥3 alternatives and produces degenerate binary dominance with exactly 2 recipes.

## Key Findings

### 1. Structural Regime Change Between Recipes

The two recipes do not merely produce different density values — they occupy fundamentally different density regimes:

- **Canonical per-iteration (p=0.5):** Mean density ~0.006 across all tasks/definitions. The page is treated as nearly empty.
- **Per-task weighted:** Mean density ~0.30-0.65 depending on page type. The page is treated as 30-65% full.
- **Cross-recipe ratio:** 84.7x. This is not a parameter sensitivity — it is a structural consequence of how each recipe models element inclusion.

### 2. Dominance Is Binary (2-Recipe Limitation)

With exactly 2 recipes, dominance is necessarily 0% or 100%. All 42 task-definition-recipe triples show degenerate dominance. This is a framework limitation, not a scientific finding. The OECD/COINr framework requires ≥3 alternatives to produce meaningful dominance pairs.

### 3. Ranking Certainty Varies by Recipe

- **Per-task weighted:** CI width = 1 for all 7 tasks (perfect ranking certainty)
- **Canonical:** CI width = 2 for product_listing tasks, width = 4 for detail_camera
- **Recipe choice dramatically affects ranking certainty:** weighted is deterministic, canonical is noisy

### 4. Definitions Are Not the Primary Sensitivity Source

Within each recipe, the three definitions (DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK) produce highly correlated rankings (Spearman r > 0.98). The definition choice is not the primary source of recipe sensitivity — the recipe choice itself is.

### 5. Classification Is Heavily Concentrated

13/14 task-recipe pairs classified MEDIUM, 1/14 (detail_camera canonical) classified HIGH. Low entropy (0.37 bits) indicates poor discrimination. The framework struggles to separate sensitivity levels when one recipe dominates so completely.

## Decision Rule Evaluation

| Criterion | Result | Rationale |
|-----------|--------|-----------|
| C1_FRAMEWORK_VALID | **PASS** | 100% of task-definition pairs computable |
| C2_DOMINANCE_INFORMATIVE | **FAIL** | 0 non-degenerate pairs (binary dominance with 2 recipes) |
| C3_CI_INFORMATIVE | **PASS** | CI widths < 50th percentile of density range |
| C4_CLASSIFICATION_DISCRIMINATES | **PASS** | 2 categories assigned (MEDIUM, HIGH) |
| C5_NULL_CONTROL_PASSES | **PASS** | Null dominance within 15% of 50%; null CI width ≥1.3x original |

**Verdict:** MIXED — C2 failure is a framework limitation, not a scientific negative.

## Implications for C-MEAS-VALID

### What This Establishes

1. **Recipe choice is the dominant source of density variation** — not definition choice, not task-type variation.
2. **The two recipes are not interchangeable** — they produce densities that differ by ~85x.
3. **The truncated-first-20 data is sufficient** to detect the structural regime change between recipes.
4. **The OECD/COINr framework is partially applicable** — it correctly identifies recipe sensitivity but cannot discriminate within the 2-recipe setting.

### What This Does NOT Establish

1. **Whether canonical or weighted is "correct"** — this requires grounding against human judgment.
2. **Whether the 84.7x ratio persists with full data** — the locatable_sample cap may distort densities.
3. **Whether a third recipe variant would produce non-degenerate dominance** — untested.

## Recommended Next Actions

1. **Reformulate C2 for 2-recipe comparisons** — use density ratio or ranking reversal rate instead of dominance.
2. **Test with full locatable_sample data** — remove the 20-element cap to verify density scale.
3. **Add a third recipe variant** — test whether the OECD/COINr framework produces informative results with 3+ alternatives.
4. **Ground against human judgment** — determine which recipe better matches human density perception.

## Raw Data Summary

- **Tasks:** 7 (3 product_listing, 3 detail, 1 cart)
- **Definitions:** DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK
- **Recipes:** canonical (p=0.5 independent), pertask_weighted (bbox-normalized)
- **Source:** EXP-INTEL-34782350557 raw_evidence (sha256: da30bd05...)
- **Analysis script:** /tmp/opencode/oecd_sensitivity_analysis.py
