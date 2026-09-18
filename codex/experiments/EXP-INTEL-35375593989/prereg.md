# EXP-INTEL-35375593989 — Preregistration

## Metadata

- **Experiment ID**: EXP-INTEL-35375593989
- **Lane**: intel
- **Claims**: C-MEAS-VALID
- **Parent**: EXP-INTEL-35353016702 (FALSIFIED-IN-SETTING — linear combination cannot break OECD/COINr degeneracy)
- **Created**: 2026-09-18

## 1. Question

Can a density-ratio continuous sensitivity metric (canonical density / weighted density per task-definition pair) replace discrete OECD/COINr dominance as the MIXED outcome decision rule, producing a principled, stable, and informative classification of recipe-sensitive vs recipe-insensitive task-definition pairs?

## 2. Background and Motivation

The parent experiment (EXP-INTEL-35353016702) demonstrated that linear combination recipes (meta-analytic mean) CANNOT break OECD/COINr dominance degeneracy because (canonical+weighted)/2 always ranks between the two originals by mathematical identity. This is a closed mathematical fact, not an empirical finding.

The MIXED outcome decision rule remains UNRESOLVED. Three candidate pivot paths exist:
- (a) Non-linear third recipe (DOM hierarchy depth, semantic weighting) — requires defining and implementing a new recipe
- (b) Alternative continuous sensitivity metric (density ratio, ranking reversal rate) — can be computed from existing data
- (c) Abandon dominance-based handling — restrict density metric to recipe-insensitive pairs

This experiment tests path (b): the density ratio R = canonical_density / weighted_density as a continuous per-pair sensitivity metric.

### Key Insight

The 2-recipe degeneracy (all dominance 0%/100%) arises because dominance is a discrete global aggregation of pairwise comparisons. The density ratio is a continuous per-pair measure that captures the same structural information (31x cross-recipe gap) without requiring discrete dominance classification. If the ratio varies across task-definition pairs, it can be thresholded for MIXED classification.

## 3. Hypothesis

The density ratio R = canonical_density / weighted_density per task-definition pair:
- (a) varies across task types (is not a universal constant),
- (b) correlates with between-recipe ordering disagreement (higher R => more recipe-sensitive),
- (c) provides a more informative MIXED classification than degenerate 0%/100% dominance.

## 4. Falsifier

The density ratio approach is falsified if ANY of:
- (F1) CV(R) < 0.10 across all 21 pairs (ratio is effectively constant)
- (F2) |Spearman(R, any_proxy)| < 0.30 for all ordering-disagreement proxies
- (F3) No natural threshold separates recipe-sensitive from insensitive pairs (no gap or bimodality)
- (F4) |Spearman(R, weighted)| > 0.95 AND |Spearman(R, canonical)| < 0.30 (ratio adds no info beyond weighted density alone)

## 5. Data Source

- **Raw evidence**: `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json` (sha256 da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050)
- **7 tasks** on 1 Magento site: 3 product_listing, 3 detail, 1 cart
- **3 definitions**: DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK
- **2 recipes**: canonical per-iteration p=0.5, per-task weighted
- **21 task-definition pairs** (7 tasks x 3 definitions)
- **Scope**: truncated-first-20 locatable_sample (locatable_elements 21-82, sample capped at 20)

### Density Computation

For each (task, definition, recipe), density is computed as the fraction of locatable elements matching the definition criteria. The canonical recipe uses independent Bernoulli inclusion at p=0.5 per element. The weighted recipe uses area-based weighting (w = element_area / total_area).

## 6. Metrics

### Primary Metrics

| ID | Name | Description |
|----|------|-------------|
| M1 | R_distribution | Per-pair density ratios: mean, std, CV, min, max, IQR across 21 pairs |
| M2 | R_by_task_type | Mean ratio per page_type group (listing, detail, cart) |
| M3 | R_by_definition | Mean ratio per definition (DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK) |
| M4 | Spearman_R_canonical | Spearman(R, canonical_density) across 21 pairs |
| M5 | Spearman_R_weighted | Spearman(R, weighted_density) across 21 pairs |
| M6 | eta_squared_R_page_type | Eta-squared(R ~ page_type): fraction of ratio variance explained by task type |
| M7 | eta_squared_weighted_page_type | Eta-squared(weighted_density ~ page_type): for C4 redundancy check |
| M8 | threshold_analysis | Best Fisher-exact or Kruskal-Wallis p-value across candidate thresholds T |
| M9 | ratio_bimodality | Hartigan's dip test p-value for bimodality of R distribution |

### Derived Metrics

| ID | Name | Description |
|----|------|-------------|
| M10 | ratio_range | Max(R) / Min(R) across 21 pairs |
| M11 | task_type_separation | Max inter-group mean ratio / Min inter-group mean ratio (listing vs detail vs cart) |

## 7. Controls

### Positive Control

**PC1_KNOWN_REVERSAL_PAIRS**: The 3 task-type groups are known to show recipe reversal (canonical listing>detail>cart vs weighted cart>listing>detail). The density ratio should differ between groups if the ratio captures recipe sensitivity.

Expected: Ratio for cart tasks (where weighted >> canonical) differs from listing tasks. At minimum, the ratio is not identical across all 3 groups.

### Null Control

**NC1_SHUFFLED_RATIO**: When canonical density values are shuffled across task-definition pairs (breaking the task-canonical association), the resulting ratio distribution should lose task-type structure.

Expected: Real ratio distribution shows task-type clustering (ANOVA p < 0.10 or eta-squared >= 0.20). Shuffled distribution shows no clustering (p > 0.05).

### Baselines

- **B1_DEGENERATE_DOMINANCE**: 2-recipe dominance (all 0%/100%). Ratio must exceed this.
- **B2_LINEAR_MEAN_DEGENERACY**: Meta-analytic mean (always between). Ratio must exceed this.
- **B3_CANONICAL_ONLY_BINARY**: Binary threshold on canonical density alone (all 21 flagged since canonical < 0.01).
- **B4_WEIGHTED_ONLY_BINARY**: Binary threshold on weighted density alone.

## 8. Decision Rule

Conjunctive:

- **C1_RATIO_VARIATION**: CV(R) >= 0.10 across 21 pairs
- **C2_RATIO_CORRELATION**: |Spearman(R, canonical)| >= 0.30 OR |Spearman(R, weighted)| >= 0.30 OR eta-squared(R, page_type) >= 0.20
- **C3_THRESHOLD_EXISTENCE**: Best Fisher-exact or Kruskal-Wallis p < 0.10 for some threshold T
- **C4_RATIO_ADDS_INFO**: |Spearman(R, weighted)| < 0.95 OR eta-squared(R, page_type) > eta-squared(weighted, page_type)

Verdicts:
- C1 AND C2 AND C3 AND C4 → SURVIVES_CURRENT_TEST
- C1 AND C2 AND NOT C3 → MIXED
- C1 AND NOT C2 → FALSIFIED-IN-SETTING
- NOT C1 → FALSIFIED-IN-SETTING

## 9. Validity Threats

1. **Truncation bias**: Results are bounded to truncated-first-20 (7 tasks, 1 site). Full-DOM may change density values and ratios.
2. **Small N**: 21 pairs limits statistical power. Fisher exact requires at least 2 pairs per cell.
3. **Definition correlation**: Definitions are highly correlated (Spearman r > 0.98 within recipe). Ratio variation may be dominated by task type, not definition.
4. **Ratio non-identifiability**: R = canonical/weighted is a single number per pair. It cannot distinguish between "canonical is low" and "weighted is high" as the source of ratio variation.
5. **No holdout**: All 21 pairs are used for both exploration and confirmation. This is acceptable for descriptive metrics but limits generalization.

## 10. Consequences

### If SURVIVES_CURRENT_TEST
- Density ratio is a viable continuous MIXED metric
- Full-DOM re-run spec can use ratio-based classification with threshold calibrated from observed distribution
- Product lane can implement ratio-based MIXED decision rule

### If FALSIFIED-IN-SETTING
- Density ratio cannot serve as MIXED metric (constant, uncorrelated, or redundant)
- Remaining options: non-linear third recipe, abandon MIXED handling, or accept irreducible recipe sensitivity
- Full-DOM re-run spec must use alternative MIXED strategy or omit MIXED handling

## 11. Carry Forward from Parent

### Established
- Recipe choice is MATERIAL (31x canonical/weighted gap) — EXP-INTEL-35264637598
- Linear combinations CANNOT break dominance degeneracy (mathematical identity) — EXP-INTEL-35353016702
- Within each recipe, definitions are highly correlated (Spearman r > 0.98) — EXP-INTEL-35330747199
- Canonical per-iteration p=0.5 is principled — EXP-INTEL-35264637598

### Rejected
- OECD/COINr framework with 2 recipes is NOT informative (construct failure) — EXP-INTEL-35330747199
- Linear third recipe CANNOT break degeneracy — EXP-INTEL-35353016702
- SURVIVES_REVERSAL_PERSISTS decision rule not achievable — EXP-INTEL-35264637598

### Unknown
- Would a non-linear third recipe work? — U-1 from parent
- Is MIXED outcome resolvable at all with OECD/COINr? — U-2 from parent
- Full-DOM generalization — blocked by runtime cap

### Do NOT Assume
- OECD/COINr framework has been validated for SPIDER
- 31x ratio is validated on full DOM
- FALSIFIED-IN-SETTING generalizes to full-DOM
- Density metric is entirely useless
- Recipe choice is a nuisance parameter (it is MATERIAL)
