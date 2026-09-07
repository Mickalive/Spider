# EXP-INTEL-33945226776 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-33945226776
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON
- **Date**: 2026-09-05
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-INTEL-33925056324 (SUPPORTS, ceiling: synthetic adapter validation only)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Given WebArena's public task definitions, site configurations, and source code (without Docker deployment), what is the estimated page complexity distribution, truncation risk, and fragment yield across task types, and which 2-3 task types maximize information gain for the C-CROSSSITE/C-LLM-INHERIT integration experiment?

## 3. Motivation

### What the parent experiment established (EXP-INTEL-33925056324)

The parent experiment tested a 224-line adapter on synthetic WebArena observations. It established:

**Established (synthetic-only ceiling):**
- Adapter parses synthetic WebArena accessibility tree string + obs_nodes_info with perfect scores (element_recall=1.0, attribute_preservation=1.0, hierarchy_preservation=1.0) across 3 site types (100 elements each)
- Transformation cost: 224 LOC, 0 dependencies, 0 API calls

**Rejected:**
- Broader SUPPORTS ceiling ("transformation cost is low; 812-task corpus worth REQUIRES_TRANSFORM overhead") — NOT justified by synthetic-only results
- Synthetic scores are tautological (generator and adapter share identical formatting grammar)

**Unknown:**
- Whether adapter works on real WebArena Docker output
- Whether truncation (UTTERANCE_MAX_LENGTH=8192, max_obs_length=1920) discards fragments
- Whether viewport filtering (current_viewport_only=True) removes critical elements
- Whether REQUIRES_TRANSFORM overhead negates corpus expansion value

**Do Not Assume:**
- Transformation cost is low for live WebArena
- C-CROSSSITE or C-LLM-INHERIT are unblocked
- Synthetic scores predict live performance

### Why this experiment is different

The parent experiment asked: "Can the adapter parse WebArena's format?" This experiment asks: "Is WebArena's dataset suitable for C-CROSSSITE testing, before deploying Docker?"

This is an Intel-appropriate question: stress-testing the dataset to alter the experimental design. The parent handoff recommended a graph-lane Docker integration experiment. Intel cannot deploy Docker, but Intel CAN determine whether Docker deployment is worth pursuing by analyzing the public task distribution and estimating fragment yield from source code constants.

**Key difference from prior work:**
- EXP-INTEL-33528832113: structural proxies (S1-S5) — "is WebArena structurally suitable?"
- EXP-INTEL-33842055594: source inspection — "what format does WebArena use?"
- EXP-INTEL-33925056324: synthetic adapter — "can the adapter parse the format?"
- **This experiment**: task distribution analysis — "which tasks are worth integrating, and is the corpus worth the transformation cost?"

## 4. Hypotheses

### H1: Site-Type Differentiation
WebArena's 4 site types have distinct page complexity profiles that are distinguishable from task metadata and source code constants (not requiring live page rendering).

### H2: Fragment Yield Sufficiency
At least 2 site types have >50% of tasks with estimated fragment yield >50% after REQUIRES_TRANSFORM overhead.

### H3: Transformation Cost Boundedness
The REQUIRES_TRANSFORM overhead (truncation + viewport filtering + node pruning) removes <50% of extractable elements for the recommended task types, making the 812-task corpus expansion worth the cost.

### H4: Task-Type Ranking Stability
The ranking of site types by estimated fragment yield is stable across 3 independent estimation methods (element-count-based, char-length-based, task-type-based).

## 5. Data Sources

### 5.1 WebArena Task Definitions

Source: WebArena public GitHub repository (github.com/web-arena-x/webarena, main branch)

Files to parse:
- Task definition JSON files (site_type, URL patterns, task_description, evaluation scripts)
- Site configuration files (4 site types: e-commerce/shopping, social forum/reddit, collaborative coding/gitlab, CMS/wikipedia)
- Source code constants: UTTERANCE_MAX_LENGTH=8192, max_obs_length=1920, IN_VIEWPORT_RATIO_THRESHOLD=0.6, IGNORED_ACTREE_PROPERTIES, valid_node filtering rules

### 5.2 Task Categorization

For each task, extract:
- **site_type**: shopping, reddit, gitlab, wikipedia (or equivalent)
- **URL patterns**: page types visited (product listing, product detail, thread, comment, file, commit, article, edit)
- **task_description_length**: character count of task description (proxy for page complexity)
- **evaluation_type**: evaluation method (DOM-based, text-match, URL-match, program-based)

### 5.3 Source Code Constants

Extract from WebArena source code:
- UTTERANCE_MAX_LENGTH (observation_space truncation)
- max_obs_length (LLM input truncation)
- IN_VIEWPORT_RATIO_THRESHOLD (viewport filtering)
- IGNORED_ACTREE_PROPERTIES (node pruning)
- valid_node rules (node filtering)
- clean_accessibility_tree (post-processing)

## 6. Estimation Methods

### 6.1 Element-Count-Based Estimation

For each site type, estimate typical DOM element count per page:
- E-commerce (shopping): product listings typically have 50-200 elements (product cards, filters, navigation, search)
- Social forum (reddit): thread views typically have 30-150 elements (comments, voting, navigation)
- Collaborative coding (gitlab): file/commit views typically have 40-120 elements (file tree, diff, comments)
- CMS (wikipedia): article views typically have 20-80 elements (text, infobox, navigation, TOC)

Estimate fragment yield as: elements_surviving / total_elements, where elements_surviving accounts for:
- Truncation: elements beyond UTTERANCE_MAX_LENGTH=8192 chars are lost
- Viewport filtering: elements outside viewport (current_viewport_only=True) are lost
- Node pruning: elements matching IGNORED_ACTREE_PROPERTIES are lost

### 6.2 Char-Length-Based Estimation

For each site type, estimate formatted observation string length:
- Each element contributes ~50-100 chars (id + role + name + properties + indent)
- At UTTERANCE_MAX_LENGTH=8192, maximum ~80-160 elements survive truncation
- At max_obs_length=1920 (LLM input), maximum ~19-38 elements survive

Estimate fragment yield as: min(1, UTTERANCE_MAX_LENGTH / estimated_total_chars)

### 6.3 Task-Type-Based Estimation

For each URL pattern within a site type, estimate page complexity:
- Product listing pages: high complexity (many product cards, filters, sorting)
- Product detail pages: moderate complexity (product info, reviews, related items)
- Thread views: moderate complexity (comments, voting, navigation)
- File/commit views: moderate complexity (code, comments, navigation)
- Article views: low-moderate complexity (text, infobox, references)

Rank URL patterns by estimated complexity and compute weighted average fragment yield per site type.

## 7. Measures

### 7.1 Primary Metrics

- **estimated_fragment_yield_by_site_type**: Median estimated fragment yield (fraction of elements surviving transformation) per site type, averaged across estimation methods
- **site_type_ranking**: Ranking of site types by estimated fragment yield (highest to lowest)
- **recommended_task_types**: Top 2-3 task types (site_type × URL_pattern) that maximize information gain for C-CROSSSITE testing

### 7.2 Secondary Metrics

- **page_complexity_distribution**: Per site type, distribution of estimated element counts
- **truncation_risk_by_site_type**: Fraction of tasks estimated to exceed UTTERANCE_MAX_LENGTH=8192
- **viewport_filtering_impact_by_site_type**: Estimated fraction of elements outside viewport
- **node_pruning_impact_by_site_type**: Estimated fraction of elements matching IGNORED_ACTREE_PROPERTIES
- **transformation_overhead_ratio**: Estimated transformation cost (LOC + runtime) vs 2-site baseline
- **method_agreement**: Correlation between 3 estimation methods across site types

### 7.3 Comparison Metrics

- **synthetic_baseline**: Element recall from EXP-INTEL-33925056324 (1.0, tautological upper bound)
- **structural_proxy_baseline**: S1-S5 scores from EXP-INTEL-33528832113 (5/5, structural suitability)

## 8. Null Models

### 8.1 Uniform Complexity Null
If all site types have identical page complexity (no differentiation), the analysis cannot recommend task types. This would mean WebArena's 4 site types are not meaningfully different for fragment extraction, and the 812-task corpus provides no advantage over a single site type.

### 8.2 Truncation-Dominated Null
If >80% of tasks across all site types exceed UTTERANCE_MAX_LENGTH=8192, the analysis would show that truncation dominates fragment loss, and the REQUIRES_TRANSFORM overhead is prohibitive regardless of site type.

## 9. Statistical Tests

### 9.1 Site-Type Differentiation
- Kruskal-Wallis test: Do estimated fragment yields differ significantly across 4 site types?
- Post-hoc Dunn test with Bonferroni correction: Which site types differ?
- Effect size: eta-squared for site-type explained variance

### 9.2 Method Agreement
- Spearman rank correlation between estimation methods across site types
- Intraclass correlation coefficient (ICC) for method agreement
- Cohen's kappa for binary classification (yield >50% vs <50%) across methods

### 9.3 Threshold Tests
- One-sample proportion test: Is estimated fragment yield >50% for recommended task types?
- Binomial test: Is the number of site types with yield >50% >= 2?

## 10. Controls

### 10.1 Positive Control (E-commerce)
E-commerce site type should have the highest estimated fragment yield due to structured product data (product cards with titles, prices, images, buttons). Expected: >60% fragment yield, >30 unique element types per page.

### 10.2 Null Control (CMS/Wikipedia)
CMS site type should have the lowest estimated fragment yield due to minimal interactive elements (text content, simple navigation). Expected: <40% fragment yield, <15 unique element types per page.

### 10.3 Truncation Sensitivity Control
At max_obs_length=1920 (LLM input limit), fragment yield should be substantially lower than at UTTERANCE_MAX_LENGTH=8192. If yields are similar, truncation is not the binding constraint.

### 10.4 Method Robustness Control
The 3 estimation methods should agree on site-type ranking (Spearman rho > 0.7). If they disagree substantially, the analysis is method-dependent and results are exploratory.

## 11. Validity Threats

### 11.1 Heuristic Estimation
Fragment yield estimates are heuristic, not measured from live pages. Mitigation: use 3 independent methods and require agreement; clearly label estimates as bounds, not measurements.

### 11.2 Source Code Drift
WebArena source code constants may change between versions. Mitigation: use the specific commit referenced in the request.json (base_sha); record exact commit hash in provenance.

### 11.3 Task Definition Incompleteness
Task definitions may not fully describe page complexity (e.g., a "search" task may visit pages of varying complexity). Mitigation: categorize by URL pattern within site type, not just site type; report per-URL-pattern estimates.

### 11.4 Synthetic-to-Real Gap
Heuristic estimates may not match live page rendering. Mitigation: this is a pre-analysis to guide the graph-lane experiment, not a replacement for it. Estimates are decision-support, not final evidence.

### 11.5 Cherry-Picking Risk
Recommending specific task types could be seen as cherry-picking. Mitigation: the recommendation is based on pre-registered criteria (fragment yield >50%, element diversity >20 types); the graph-lane experiment should validate on the recommended types AND at least one non-recommended type as a negative control.

## 12. Decision Rules

### 12.1 SUPPORTS
If ALL of:
1. >=2 site types have estimated median fragment yield >50% (across estimation methods)
2. Recommended 2-3 task types have estimated element diversity >20 unique element types per page
3. Method agreement: Spearman rho > 0.7 between estimation methods on site-type ranking
4. No pipeline errors

### 12.2 FALSIFIES
If ANY of:
1. All site types have estimated median fragment yield <30%
2. No site type has element diversity >15 unique element types per page
3. Method disagreement: Spearman rho < 0.3 between any pair of estimation methods

### 12.3 MIXED
If:
1. Some site types have yield >50% but others <30% (partial differentiation)
2. Method agreement is moderate (0.3 < rho < 0.7)
3. Recommended tasks have yield >50% but element diversity <20

### 12.4 MEASUREMENT_INVALID
If:
1. WebArena task definitions cannot be parsed (repo structure changed)
2. Source code constants are not found (code restructured)
3. Pipeline errors prevent computation

## 13. Expected Outcomes

### 13.1 Positive Result (SUPPORTS)
- Graph lane should proceed with Docker integration on the recommended 2-3 task types
- C-CROSSSITE and C-LLM-INHERIT move toward EXPERIMENTAL with bounded task selection
- Intel provides the task-type ranking that guides the integration experiment
- The 812-task corpus expansion is justified by estimated fragment yield

### 13.2 Negative Result (FALSIFIES)
- 2-site corpus remains practical bound for C-CROSSSITE/C-LLM-INHERIT
- Intel should assess whether VisualWebArena, Mind2Web, or other benchmarks offer lower transformation cost
- The graph lane should NOT deploy Docker for WebArena integration
- The REQUIRES_TRANSFORM overhead negates the corpus expansion value

### 13.3 Mixed Result (MIXED)
- Some site types are suitable, others are not
- Graph lane should deploy Docker only for the recommended site types
- The integration experiment should include a negative control (non-recommended site type)
- Intel should investigate whether the unsuitable site types can be improved (e.g., html mode vs accessibility_tree mode)

## 14. Analysis Plan

1. **Data Collection**: Clone WebArena repo (or fetch relevant files from GitHub), parse task definition JSONs, extract source code constants
2. **Task Categorization**: For each task, extract site_type, URL patterns, task_description_length, evaluation_type
3. **Element-Count Estimation**: For each site type, estimate typical DOM element count per page type (product listing, thread, file, article)
4. **Char-Length Estimation**: For each site type, estimate formatted observation string length and truncation point
5. **Task-Type Estimation**: For each URL pattern, estimate page complexity and fragment yield
6. **Aggregation**: Compute median fragment yield per site type, averaged across methods
7. **Ranking**: Rank site types by estimated fragment yield; select top 2-3 as recommended task types
8. **Statistical Tests**: Kruskal-Wallis for site-type differentiation, Spearman for method agreement, proportion tests for thresholds
9. **Controls**: Verify positive control (e-commerce >60%), null control (CMS <40%), truncation sensitivity, method robustness
10. **Reporting**: Report all outcomes with equal prominence, including uncertainty bounds on heuristic estimates

## 15. Analysis Code

Analysis will be implemented in Python using:
- `json` for parsing task definitions
- `requests` or `urllib` for fetching files from GitHub (if not cloning)
- `numpy` for array operations and statistics
- `scipy.stats` for Kruskal-Wallis, Spearman, proportion tests
- `collections.Counter` for element type counting
- Standard library only (no custom estimators required)

Code will be committed to `research/intel/webarena_task_analysis/` before execution.

## 16. Pre-registered Expectations

From prior work and domain knowledge:
- E-commerce (shopping) should have highest fragment yield: product listings are element-dense with structured data
- Social forum (reddit) should have moderate fragment yield: thread views have comments but less structured data
- Collaborative coding (gitlab) should have moderate fragment yield: file/commit views have code but less interactive elements
- CMS (wikipedia) should have lowest fragment yield: article views are content-heavy with minimal interactive elements
- Truncation at max_obs_length=1920 is the binding constraint for most tasks (not UTTERANCE_MAX_LENGTH=8192)
- Viewport filtering removes 30-50% of elements on typical pages (IN_VIEWPORT_RATIO_THRESHOLD=0.6)

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
