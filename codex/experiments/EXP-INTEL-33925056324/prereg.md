# EXP-INTEL-33925056324 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-33925056324
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT
- **Date**: 2026-09-05
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can SPIDER's fragment extraction logic be adapted to extract reusable fragments from WebArena's accessibility tree observation format, and what is the transformation cost?

## 3. Motivation

Prior intel experiment EXP-INTEL-33842055594 established that WebArena's observation format is REQUIRES_TRANSFORM (PARTIALLY_COMPATIBLE). DOM is present via CDP but requires non-trivial transformation: recomposition of split observation channels (text string + obs_nodes_info metadata), viewport filtering override (current_viewport_only=False), truncation handling, and ARIA role to HTML tag mapping.

The critical unknown is whether this transformation cost is recoverable: whether SPIDER fragment extraction actually works against WebArena's observation format. This experiment tests that using synthetic observations that mimic WebArena's exact format, without Docker deployment.

## 4. Hypotheses

### H1: Element Recall
A minimal adapter that recomposes split observation channels can extract >90% of elements from synthetic WebArena observations across three site types.

### H2: Attribute Preservation
Extracted elements preserve >80% of attributes (ARIA properties: focused, expanded, required, hasPopup) across all site types.

### H3: Hierarchy Preservation
Extracted elements preserve >80% of parent-child relationships across all site types.

### H4: Positive Control
Adapter extracts all 100 elements from the positive control synthetic observation with correct attributes.

### H5: Null Control
Adapter extracts zero elements from the null control (screenshots-only) observation.

## 5. Synthetic Data Generation

### 5.1 Accessibility Tree Format

Synthetic observations will mimic WebArena's exact output:
- `obs["text"]`: formatted indented string with element IDs, roles, names, properties
- `obs_nodes_info`: dict mapping element ID to `{backend_id, union_bound, text}`
- `obs["image"]`: base64 placeholder (not used)

Example element string: `[4] button "Submit" focused: True`

### 5.2 Site Types

Three synthetic site types with distinct element patterns:

1. **E-commerce** (product listing): 100 elements total
   - 20 links (product titles, categories)
   - 30 buttons (add to cart, wishlist, compare)
   - 50 textboxes (search, quantity, filter inputs)
   - Hierarchy: root -> sections -> groups -> elements

2. **Social forum** (thread view): 100 elements total
   - 25 links (user profiles, reply, quote)
   - 35 buttons (like, report, follow)
   - 40 textboxes (comment, reply, search)
   - Hierarchy: root -> posts -> actions -> elements

3. **Collaborative coding** (file tree): 100 elements total
   - 15 links (file names, directory links)
   - 40 buttons (expand, collapse, rename, delete)
   - 45 textboxes (file search, commit message, branch name)
   - Hierarchy: root -> directories -> files -> actions

### 5.3 Sample Size

- 3 site types x 100 elements = 300 total elements
- Each element has unique ID, role, name, properties, parent-child relationship
- Synthetic generation uses deterministic seed (seed=42) for reproducibility

## 6. Adapter Implementation

### 6.1 Current SPIDER Fragment Extraction

SPIDER's current fragment extraction operates on raw HTML pages (quotes.toscrape.com, books.toscrape.com). It extracts elements by parsing HTML tags, attributes, and hierarchy. This serves as baseline reference only.

### 6.2 Minimal Adapter for Accessibility Tree

The adapter will:
1. Parse the formatted indented string to extract element IDs, roles, names, properties
2. Parse indentation to reconstruct parent-child hierarchy
3. Map element IDs to `obs_nodes_info` metadata for backend_id, union_bound, text
4. Override viewport filtering (assume all elements are visible)
5. Output extracted fragments with identity, hierarchy, attributes, text

### 6.3 Code Location

Adapter code will be committed to `research/intel/webarena_adapter.py` before execution.

## 7. Measures

### 7.1 Primary Metric
- **element_recall**: fraction of synthetic elements successfully extracted (elements with correct ID, role, name)

### 7.2 Secondary Metrics
- **attribute_preservation**: fraction of extracted elements with correct ARIA properties (focused, expanded, required, hasPopup)
- **hierarchy_preservation**: fraction of extracted elements with correct parent-child relationships
- **transformation_cost_lines**: lines of code required for adapter (qualitative)

### 7.3 Per-Site Metrics
All metrics computed per site type and aggregated.

## 8. Controls

### 8.1 Positive Control
- Synthetic observation with 100 elements, known structure
- Expected: element_recall = 1.0, attribute_preservation = 1.0, hierarchy_preservation = 1.0

### 8.2 Null Control
- Synthetic observation with only screenshot (base64) and empty text
- Expected: element_recall = 0.0, attribute_preservation = 0.0, hierarchy_preservation = 0.0

### 8.3 Baseline Control
- Current SPIDER fragment extraction on raw HTML (reference only, not executed)
- Provides context for what "good" looks like on compatible format

## 9. Statistical Tests

### 9.1 Primary Test
- One-sample t-test: element_recall > 0.90 across site types
- One-sample t-test: attribute_preservation > 0.80 across site types
- One-sample t-test: hierarchy_preservation > 0.80 across site types

### 9.2 Effect Size
- Cohen's d for each metric vs threshold (0.90, 0.80, 0.80)

### 9.3 Site Type Comparison
- Paired t-test: metric differences across site types
- Coefficient of variation across site types

## 10. Validity Threats

### 10.1 Synthetic-to-Real Gap
Synthetic observations may not reflect real WebArena DOM. Mitigation: format mimics exact WebArena output; if adapter fails on synthetic, it will fail on real.

### 10.2 Adapter Simplicity
Minimal adapter may not capture all transformation nuances. Mitigation: adapter focuses on core extraction (identity, hierarchy, attributes, text); complex transformations (viewport override, truncation handling) are out of scope.

### 10.3 Sample Size
Only 300 elements across 3 site types. Mitigation: sufficient for detecting large effects (d>0.8) with >80% power.

### 10.4 Element Diversity
Synthetic elements may not capture real WebArena element diversity. Mitigation: three distinct site types cover e-commerce, social, coding patterns.

## 11. Decision Rules

### 11.1 SUPPORTS
If ALL of:
1. element_recall >= 0.90 across all site types
2. attribute_preservation >= 0.80 across all site types
3. hierarchy_preservation >= 0.80 across all site types
4. Positive control passes (recall = 1.0)
5. Null control passes (recall = 0.0)
6. No pipeline errors

### 11.2 FALSIFIES
If ANY of:
1. element_recall < 0.50 across any site type
2. attribute_preservation < 0.50 across any site type
3. Positive control fails (recall < 0.90)
4. Null control fails (recall > 0.0)
5. Pipeline errors prevent extraction

### 11.3 MIXED
Otherwise (partial success, metrics between thresholds)

## 12. Expected Outcomes

### 12.1 Positive Result (SUPPORTS)
- Transformation cost is low; adapter requires minimal code
- WebArena 812-task corpus expansion is worth the REQUIRES_TRANSFORM overhead
- C-CROSSSITE and C-LLM-INHERIT can proceed with integration experiment
- Graph lane can design Docker-based integration experiment

### 12.2 Negative Result (FALSIFIES)
- Transformation cost high; adapter requires extensive code or fails to extract
- 2-site corpus remains practical bound
- Intel lane should assess whether other benchmarks offer lower-transformation-cost path
- VisualWebArena or other benchmarks may be better candidates

### 12.3 Mixed Result
- Partial extraction success; some site types work, others don't
- Requires site-specific adapters or additional transformation logic
- Integration experiment should focus on compatible site types first

## 13. Analysis Plan

1. **Data Generation**: Generate 3 synthetic site types (100 elements each) with deterministic seed=42
2. **Adapter Implementation**: Write minimal adapter in `research/intel/webarena_adapter.py`
3. **Extraction**: Run adapter on each synthetic observation
4. **Metric Computation**: Compute element_recall, attribute_preservation, hierarchy_preservation per site type
5. **Statistical Tests**: One-sample t-tests vs thresholds, effect sizes
6. **Controls**: Verify positive and null controls
7. **Reporting**: Report all outcomes with equal prominence

## 14. Analysis Code

Analysis will be implemented in Python using:
- `json` for parsing observation metadata
- `re` for parsing formatted indented string
- `statistics` for mean, stdev, t-tests
- Standard library only (no external dependencies)

Code will be committed to `research/intel/` before execution.

## 15. Pre-registered Expectations

From prior intel experiment:
- WebArena provides structured DOM via CDP (accessibility_tree mode)
- Observation split across text string and obs_nodes_info metadata requires recomposition
- ARIA properties (focused, expanded, required) are available in accessibility tree
- HTML attributes (class, id, href) are NOT available in accessibility_tree mode (only in html mode)
- Adapter should handle ARIA properties; HTML attributes are out of scope for this experiment

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.