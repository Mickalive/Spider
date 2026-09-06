# EXP-INTEL-33945226776: WebArena Task Distribution Analysis

## Executive Summary

**Status**: COMPLETE | **Outcome**: MIXED | **Lane**: Intel

This experiment analyzed WebArena's 812-task corpus to estimate page complexity, truncation risk, and fragment yield across site types, determining whether the 812-task corpus expansion justifies the REQUIRES_TRANSFORM overhead for C-CROSSSITE/C-LLM-INHERIT integration.

**Key finding**: All 6 site types have estimated median fragment yield >50% (range: 0.517-0.65), suggesting the REQUIRES_TRANSFORM overhead does NOT negate the corpus expansion value. However, the three estimation methods disagree substantially on site-type rankings (Spearman rho from -0.943 to 0.371), making the analysis exploratory rather than confirmatory.

## Motivation

The parent experiment (EXP-INTEL-33925056324) validated a 224-line adapter on synthetic WebArena observations with perfect scores (element_recall=1.0), but the auditor established this as a self-consistency check on shared formatting grammar, not independent validation. The parent handoff recommended a Docker integration experiment, but Intel cannot deploy Docker. Intel CAN determine whether Docker deployment is worth pursuing by analyzing the public task distribution and estimating fragment yield from source code constants.

This experiment bridges the gap: it provides the task-type ranking that guides the graph-lane integration experiment, without requiring Docker deployment.

## Methodology

Three independent estimation methods were applied to WebArena's 812 tasks across 6 site types:

### Method 1: Element-Count-Based
Estimates typical DOM element counts per page type (product listings: 150, threads: 100, articles: 45) and computes fragment yield as the fraction surviving truncation (UTTERANCE_MAX_LENGTH=8192), viewport filtering (IN_VIEWPORT_RATIO_THRESHOLD=0.6), and node pruning (IGNORED_ACTREE_PROPERTIES).

### Method 2: Char-Length-Based
Estimates formatted observation string length (25-120 chars per element) and computes yield at two truncation points: UTTERANCE_MAX_LENGTH=8192 and max_obs_length=1920 (LLM input limit).

### Method 3: Task-Type-Based
Uses intent length as a proxy for page complexity, adjusted by site-type baseline complexity factors. Incorporates task diversity metrics (unique templates, eval type diversity).

## Results

### Site-Type Distribution

| Site Type | Tasks | Median Yield | Mean Yield | Element Diversity | Unique Templates |
|-----------|-------|-------------|------------|-------------------|------------------|
| gitlab | 196 | 0.600 | 0.695 | 21 | 44 |
| map | 112 | 0.598 | 0.716 | 16 | 30 |
| reddit | 114 | 0.650 | 0.700 | 17 | 23 |
| shopping | 192 | 0.650 | 0.645 | 21 | 49 |
| shopping_admin | 182 | 0.600 | 0.689 | 22 | 41 |
| wikipedia | 16 | 0.517 | 0.672 | 17 | 3 |

**Observation**: WebArena has 6 site types (not 4 as hypothesized). The 'map' and 'shopping_admin' categories were not anticipated in the original 4-type model.

### Method Agreement

| Method Pair | Spearman rho | Interpretation |
|-------------|-------------|----------------|
| M1-M2 (element-count vs char-length) | 0.371 | Weak positive |
| M1-M3 (element-count vs task-type) | -0.943 | Strong negative |
| M2-M3 (char-length vs task-type) | -0.543 | Moderate negative |

**Critical finding**: Methods disagree substantially. Method 1 (element-count) penalizes shopping for high element counts (150 elements for product listings). Method 2 (char-length) gives shopping high yield at UTTERANCE_MAX_LENGTH=8192 (most pages fit). Method 3 (task-type) ranks by intent complexity, not element density.

### Truncation Sensitivity

| Site Type | Yield at 8192 | Yield at 1920 | Sensitivity Ratio |
|-----------|--------------|--------------|-------------------|
| shopping | 0.938 | 0.347 | 0.370 |
| reddit | 1.000 | 0.439 | 0.439 |
| gitlab | 1.000 | 0.471 | 0.471 |
| shopping_admin | 1.000 | 0.453 | 0.453 |
| map | 1.000 | 0.702 | 0.702 |
| wikipedia | 1.000 | 0.897 | 0.897 |

**Key finding**: max_obs_length=1920 is the binding constraint, not UTTERANCE_MAX_LENGTH=8192. Shopping is most sensitive (0.37 ratio), meaning LLM input truncation discards 65% of elements on dense product pages.

### Statistical Tests

- **Kruskal-Wallis**: H=0.158, df=5, p=0.999 — No statistically significant yield differences across site types
- **Threshold tests**: 6/6 site types above 50%, 0/6 below 30%
- **Positive control (shopping)**: PASS — yield 0.65, diversity 21
- **Null control (wikipedia)**: PASS — lowest yield (0.517), but exceeds pre-registered 40% threshold

## Recommended Task Types

Based on the analysis, the following 2-3 site types maximize information gain for C-CROSSSITE testing:

### Primary Recommendations
1. **shopping** (192 tasks, yield 0.65, diversity 21) — Highest task count, structured product data, element-dense pages
2. **gitlab** (196 tasks, yield 0.60, diversity 21) — Highest task count, code-oriented, distinct from shopping
3. **shopping_admin** (182 tasks, yield 0.60, diversity 22) — Highest element diversity, admin-oriented

### Negative Control
- **wikipedia** (16 tasks, yield 0.517, diversity 17) — Lowest yield, simplest pages, fewest tasks

### Rationale
The recommended types have:
- Median yield >50% (all three exceed 0.60)
- Element diversity >20 (21-22 unique element types)
- High task counts (182-196 tasks each)
- Distinct page structures (product listings, code views, admin dashboards)

## Decision Assessment

### SUPPORTS Criteria
- >=2 site types with yield >50%: **PASS** (6/6)
- Recommended types with diversity >20: **PASS** (21-22)
- Method agreement rho >0.7: **FAIL** (0.371, -0.943, -0.543)

### FALSIFIES Criteria
- All site types yield <30%: **NOT MET** (0/6)
- No type with diversity >15: **NOT MET** (3 types >20)
- Method disagreement rho <0.3: **MET** (m1_m3 = -0.943)

### Verdict: MIXED

The analysis partially supports the hypothesis: site types have distinct profiles and recommended types have sufficient yield and diversity. However, method disagreement means the rankings are exploratory, not confirmatory. The graph-lane integration experiment should validate on recommended types AND include a negative control (wikipedia).

## Product Consequences

### If SUPPORTS (not reached due to method disagreement)
- Graph lane proceeds with Docker integration on recommended types
- C-CROSSSITE and C-LLM-INHERIT move toward EXPERIMENTAL
- 812-task corpus expansion justified

### Current MIXED Verdict
- Graph lane should proceed with Docker integration on recommended types, but with explicit validation that heuristic estimates match live DOM
- C-CROSSSITE and C-LLM-INHERIT remain HYPOTHESIS bounded to 2-site corpus until live validation
- Intel should investigate whether VisualWebArena or Mind2Web offer lower-transformation-cost paths

### If FALSIFIES (not reached)
- 2-site corpus remains practical bound
- Intel assesses alternative benchmarks
- Graph lane does NOT deploy Docker for WebArena

## Validity Threats

1. **Heuristic estimates**: All yield estimates are based on domain knowledge, not live measurements. Kruskal-Wallis p=0.999 suggests estimates may lack discriminating power.
2. **Method disagreement**: Three methods produce contradictory rankings (rho -0.943 to 0.371). The analysis is method-dependent.
3. **Source code drift**: Constants (UTTERANCE_MAX_LENGTH=8192, max_obs_length=1920) may change between versions.
4. **Sample imbalance**: Wikipedia has only 16 tasks vs 196 for gitlab. Wikipedia estimates may not be representative.
5. **Viewport estimates**: Viewport coverage (0.45-0.65) is estimated from typical layouts, not actual WebArena rendering.

## Next Steps

1. **Graph lane**: Deploy Docker for 2-3 recommended task types, measure actual fragment yield, compare with heuristic estimates
2. **Intel**: Investigate whether VisualWebArena's SoM annotations or Mind2Web's task diversity offer lower-cost cross-site testing
3. **Method refinement**: Develop estimation methods that agree on ranking, or validate that disagreement is intrinsic to the problem
