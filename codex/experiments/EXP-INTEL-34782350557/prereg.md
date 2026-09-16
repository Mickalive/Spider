# EXP-INTEL-34782350557 preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-34782350557
- **Lane**: Intel
- **Claims**: C-MEAS-VALID, C-CROSSSITE, C-LLM-INHERIT
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-INTEL-34718481334 (parent_handoff sha256: 26f6e86ec59114547c854fedfd0cf349d5e69d1fe3712a4c4456f9014399fce3)

## 2. Scientific Question

Does the interactive fraction metric maintain within-type stability and between-type discrimination when the element definition is tightened to exclude form-descendant DIV/SPAN/LABEL (role-only counting: button, link, textbox, combobox, etc. without the form-membership clause), and what are the resulting per-type means — computable from existing EXP-INTEL-34718481334 raw measurement data without new Docker execution?

## 3. Motivation

The parent experiment (EXP-INTEL-34718481334) established that full-page interactive fraction (locatable/total_dom under DEF-FALLBACK-INTERACTIVE) is stable within page types (listing CV 0.0048, detail CV 0.037) and discriminates between types (ratio 582). However, the independent audit identified a serious construct validity threat: **VF-DEFINITION-OVERCOUNT** — the definition counts form-descendant DIV/SPAN/LABEL as interactive (due to the form-membership clause), inflating the numerator with elements that lack interactive roles. The audit's locatable_sample analysis showed 17-19 out of 20 sampled elements inForm true with role div/span.

This threatens the metric's interpretation: does it measure interactivity or merely form scaffolding? The audit recommended tightening the definition to role-only counting (button, link, textbox, combobox, etc. without the form-membership clause) and recomputing from existing raw data.

This experiment directly addresses that recommendation. It is computable from existing raw measurement data (exp347_raw_results.json) without new Docker execution, making it zero-cost and immediate.

## 4. Hypotheses

### H1: Stability under tightening
The interactive fraction metric maintains within-type stability (CV < 0.3) for at least 2 page types with n>=2 under the tightened definition.

### H2: Discrimination under tightening
Between-type variance exceeds within-type variance under the tightened definition (metric still discriminates page types).

### H3: Ordering preservation
Per-type means maintain original ordering: listing > detail > cart.

### H4: Positive control
Tightened definition locatable count > 0 on all tasks (definition not overly restrictive).

### H5: Null control
Tightened definition locatable count ≤ original definition locatable count on all tasks (removing elements reduces count).

## 5. Data Source

### 5.1 Existing Raw Measurement Data
- **File**: `research/experiments/EXP-INTEL-34718481334/exp347_raw_results.json`
- **Structure**: JSON with `measurements` array, each containing `locatable_sample` array with per-element `role` and `inForm` fields.
- **Tasks**: 7 successful tasks (checkout tasks failed with connection refused):
  - 3 product_listing: clothing-shoes-jewelry, electronics, beauty-personal-care
  - 3 product_detail: camera, pet_camera, vr_bag
  - 1 cart: cart_1

### 5.2 Original Metrics (Baseline)
From parent experiment result.json and audit.json:
- Listing mean interactive fraction: 0.048 (CV 0.0048)
- Detail mean: 0.024 (CV 0.037)
- Cart: 0.0185 (CV 0.0 due to pseudoreplication)
- Discrimination ratio: 582 (deduped)

## 6. Definitions

### 6.1 Original Definition (DEF-FALLBACK-INTERACTIVE)
Elements with non-null bounding box AND (role in interactive set OR has onclick/onsubmit handler OR is within a form element OR has aria-label/aria-describedby with non-empty text).

### 6.2 Tightened Definition (ROLE-ONLY)
Elements with non-null bounding box AND role in interactive set ['button', 'link', 'textbox', 'checkbox', 'radio', 'combobox', 'listbox', 'menuitem', 'tab', 'slider', 'spinbutton', 'searchbox', 'switch']. No form-membership clause, no onclick/onsubmit, no aria-label/aria-describedby.

### 6.3 Derived Metrics
- **tightened_locatable_count**: Number of elements matching tightened definition per task.
- **tightened_interactive_fraction**: tightened_locatable_count / total_dom_elements per task.
- **tightened_within_type_cv**: Coefficient of variation of tightened_interactive_fraction within each page type (listing, detail, cart).
- **tightened_between_type_variance**: Variance of page-type means of tightened_interactive_fraction.
- **tightened_within_type_variance**: Mean of per-type variances of tightened_interactive_fraction.

## 7. Analysis Plan

### 7.1 Data Extraction
For each task in exp347_raw_results.json:
1. Extract `locatable_sample` array.
2. Count elements where `role` is in the interactive set (tightened_locatable_count).
3. Extract `total_dom_elements` (unchanged).
4. Compute `tightened_interactive_fraction = tightened_locatable_count / total_dom_elements`.

### 7.2 Per-Type Aggregation
Group tasks by `page_type` (product_listing, product_detail, cart). Compute per-type:
- Mean tightened_interactive_fraction
- Standard deviation
- CV = std / mean (if mean > 0; else undefined)
- Sample size n

### 7.3 Stability Assessment
- Compute within-type CV for each page type with n>=2.
- Primary criterion: at least 2 page types have CV < 0.3.

### 7.4 Discrimination Assessment
- Compute between-type variance: variance of the 3 per-type means.
- Compute within-type variance: mean of the 3 per-type variances (weighted by n-1).
- Criterion: between-type variance > within-type variance.

### 7.5 Ordering Assessment
- Compare listing mean > detail mean > cart mean.
- Allow ties only if means are within 0.001 (rounding tolerance).

### 7.6 Control Verification
- Positive control: tightened_locatable_count > 0 for all tasks.
- Null control: tightened_locatable_count <= original_locatable_count for all tasks (original locatable_elements from parent data).

### 7.7 Original Baseline Comparison
- Compute delta between original and tightened interactive fractions per task.
- Report per-type mean delta.

## 8. Statistical Tests

No inferential statistics required; the analysis is descriptive and deterministic given the fixed raw data. The decision rules are based on thresholds (CV < 0.3, variance ratio > 1, ordering).

## 9. Controls

### 9.1 Positive Control (H4)
- Expected: tightened_locatable_count > 0 on all tasks.
- Verification: count elements with interactive role on each page.
- Failure mode: If zero, tightened definition is too restrictive (no button/link/etc. on some pages).

### 9.2 Null Control (H5)
- Expected: tightened_locatable_count <= original_locatable_count on all tasks.
- Verification: compare to original locatable_elements from parent.
- Failure mode: If equal, form-membership clause added no elements (unlikely given audit finding).

### 9.3 Replication Control
- Compare tightened means to original means; expect systematic downward shift.
- If shift is zero across all tasks, the form-membership clause did not affect counts (contradicts audit).

## 10. Validity Threats

### 10.1 Data Completeness
- 7 tasks across 3 page types (cart n=1). Low sample sizes limit stability estimation.
- Mitigation: Report exact sample sizes and acknowledge limitations.

### 10.2 Pseudoreplication
- Cart tasks may include identical measurements of same URL (parent finding).
- Mitigation: Report both raw and deduped statistics.

### 10.3 Definition Ambiguity
- Tightened definition uses role field from accessibility tree; role values may be inconsistent across browsers.
- Mitigation: Use frozen raw data from consistent Chromium environment.

### 10.4 Total DOM Variability
- Total DOM elements vary across tasks; denominator variation could affect fraction stability.
- Mitigation: Already observed in parent; tightened definition inherits same denominator.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. tightened_locatable_count > 0 on all tasks (positive control passes)
2. within-type CV < 0.3 for at least 2 page types with n>=2 (stability holds)
3. between-type variance > within-type variance (discrimination holds)
4. per-type means ordering listing > detail > cart (ordering preserved)
5. No raw data missing role/inForm fields on any task

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. tightened_locatable_count = 0 on any task (definition too restrictive)
2. within-type CV > 0.3 for all page types (stability lost)
3. between-type variance ≤ within-type variance (discrimination lost)
4. per-type means ordering reverses (e.g., detail > listing)

### 11.3 MEASUREMENT_INVALID
If:
1. Raw measurement data missing role or inForm fields on any task
2. exp347_raw_results.json not readable or corrupted
3. Fewer than 3 page types represented in data

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Metric robust to definition tightening: captures interactive elements beyond form scaffolding.
- Product can use this metric for yield monitoring.
- Confidence in construct validity increases.
- Next step: test metric generalization to other sites (cross-site measurement).

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Metric is artifact of form scaffolding; approach closed for this definition family.
- Intel lane pivots to alternative yield approaches.
- Product cannot rely on this metric.

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Raw data incomplete; cannot answer question.
- Need to re-collect data with proper fields.

## 13. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 14. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.