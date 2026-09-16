# EXP-INTEL-35124660457 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35124660457
- **Lane**: Intel
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-16
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the first-20 locatable_sample truncation systematically bias role counts and density-based page-type orderings, and can the direction and magnitude of this bias be estimated from existing raw data without re-crawling?

## 3. Motivation

Parent experiment EXP-INTEL-35112013458 found that the observed 0.3 pairwise ordering agreement across 5 ROLE_MAP definitions does NOT exceed chance-level expectation (null mean 0.5275). The verdict was FALSIFIED-IN-SETTING.

However, the parent handoff identified truncation as the primary validity threat:
- `locatable_sample` is capped at first-20 elements per task
- `locatable_elements` count is 82 per task (listing pages)
- The truncation may systematically exclude roles that appear later in document order
- Different page types (listing, detail, cart) have different DOM structures
- The truncation bias may be page-type-dependent, affecting density calculations

The parent recommended routing to runtime lane to fix the locatableSample cap. This intel experiment characterizes the bias using existing data, providing:
1. Quantified bias magnitude and direction per page type
2. Corrected ordering estimates using full DOM statistics
3. Evidence for or against the truncation being the primary driver of the FALSIFIED result
4. Concrete guidance for the runtime substrate fix

## 4. Hypotheses

### H1: Truncation Bias Exists
The first-20 truncation produces role counts that differ from full-DOM estimated role counts by >10% relative difference for at least one role on at least one page type.

### H2: Bias is Page-Type-Dependent
The truncation bias direction and magnitude differ across page types (listing vs detail vs cart). Specifically, listing pages lose more <a> (link) elements because product links appear deeper in the DOM.

### H3: Full-DOM Correction Changes Ordering
The full-DOM corrected ordering differs from the truncated-sample ordering for at least one page type, indicating the truncation affects the density-based ordering metric.

### H4: Random Sampling Has Lower Bias
Random 20-element samples from the locatable_elements pool show lower mean absolute bias than the first-20 truncation, confirming the bias is due to document-order selection, not small sample size.

## 5. Data Source

### 5.1 Raw Evidence

All data comes from `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json`.

This file contains measurements for 7 tasks on a single Magento shopping site:
- 3 product_listing pages (clothing-shoes-jewelry, beauty-personal-care, electronics)
- 3 detail pages (camera, vr_bag, pet_camera)
- 1 cart page (cart_1)

### 5.2 Available Fields Per Measurement

- `locatable_sample`: First-20 locatable elements with role, tag, bbox
- `locatable_elements`: Total count of locatable elements (82 per task)
- `elements_with_bbox`: Total count of elements with bounding boxes
- `total_dom_elements`: Total DOM element count
- `dom_stats.tagCounts`: Full DOM tag count distribution
- `dom_stats.linksCount`: Total <a> tags in DOM
- `dom_stats.buttonsCount`: Total <button> tags in DOM
- `dom_stats.formsCount`: Total <form> tags in DOM
- `dom_stats.inputsCount`: Total <input> tags in DOM

### 5.3 Key Observations

The first-20 locatable_sample contains elements in document order. For listing pages:
- DOM has 393 <a> tags, but only 16 are in the first-20 sample
- DOM has 15 <button> tags, but only a few are in the sample
- The sample is dominated by header/nav elements (store logo, search form)

## 6. Analysis Plan

### 6.1 Full-DOM Role Count Estimation

For each task, estimate the full-DOM count for each interactive role:

| Role | Full-DOM Estimate Source |
|------|--------------------------|
| link (a→link mapping) | `dom_stats.linksCount` (all <a> tags) |
| button | `dom_stats.buttonsCount` (all <button> tags) |
| form | `dom_stats.formsCount` (all <form> tags) |
| textbox (input→textbox mapping) | `dom_stats.inputsCount` (all <input> tags) |
| combobox, div, label, span | Use truncated-sample counts (no DOM equivalent) |

Note: The `dom_stats` gives raw tag counts, not ARIA role counts. The ARIA role mapping may differ from tag names. However, for the primary interactive roles (a→link, button, form, input→textbox), the tag counts are the best available full-DOM estimate.

### 6.2 Density Computation

For each definition (DEF-FULL-MAP, DEF-FORM-ONLY, isolated a→link):

1. **Truncated density**: count(interactive elements in first-20) / elements_with_bbox
2. **Full-DOM density**: estimate(interactive elements in full DOM) / elements_with_bbox
3. **Bias**: full_DOM_density - truncated_density (signed)
4. **Relative bias**: (full_DOM_density - truncated_density) / truncated_density (if truncated > 0)

### 6.3 Ordering Comparison

For each definition, compare:
- Truncated-sample ordering (descending density by page type)
- Full-DOM corrected ordering

Count how many page types change ordering between truncated and full-DOM.

### 6.4 Random Sample Baseline

For each task:
1. Simulate 1000 random draws of 20 elements from the locatable_elements pool
2. For each draw, compute role counts and density
3. Compare mean absolute bias of random samples vs first-20 truncation
4. This tests whether the bias is due to document-order selection or small sample size

### 6.5 Per-Page-Type Analysis

For each page type (listing, detail, cart):
- Mean truncated density per role
- Mean full-DOM density per role
- Signed and relative bias
- Whether the ordering changes under full-DOM correction

## 7. Controls

### 7.1 Positive Control: a→link Reversal
The a→link reversal (cart>product_listing>detail) must be preserved in the full-DOM corrected ordering for at least one definition. If full-DOM correction eliminates the reversal for all definitions, this confirms the truncation drives the a→link effect.

### 7.2 Null Control: Random Sample Bias
Random 20-element samples should show lower mean absolute bias than the first-20 truncation across all tasks. If random samples show equal or higher bias, the bias is driven by small sample size, not document-order selection.

### 7.3 Degeneracy Control
If locatable_elements < 20 for any task, that task is excluded from random-sample analysis (degenerate).

## 8. Validity Threats

### 8.1 Tag-to-Role Mapping
`dom_stats.tagCounts` gives raw HTML tag counts, not ARIA role counts. The ARIA role mapping (e.g., `<a>` → "link" via ROLE_MAP) may differ from tag names. Mitigation: report both tag-based and role-based estimates; the primary analysis uses tag counts for roles with direct DOM equivalents.

### 8.2 Locatable vs Total DOM
`locatable_elements` (82) is a subset of `elements_with_bbox` (1550) which is a subset of `total_dom_elements` (1696). The full-DOM estimate should use `locatable_elements` as the denominator context, not `total_dom_elements`. Mitigation: use `elements_with_bbox` as the denominator for density computation (consistent with parent).

### 8.3 Small N
Only 7 tasks (3 page types). Cross-page-type comparisons are underpowered. Mitigation: this is a bias characterization study, not a significance test. Report effect sizes and bias magnitudes.

### 8.4 Single Site
All data from one Magento shopping site. Cross-site generalization unsupported. Mitigation: state this limitation explicitly; recommend cross-site testing in handoff.

### 8.5 Random Sample Simulation
The random-sample baseline assumes all 82 locatable elements are equally likely to be sampled. In reality, the locatable_elements pool may have structure (e.g., some elements are not interactive). Mitigation: the random sample tests sampling bias, not role classification accuracy.

## 9. Decision Rules

### 9.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Full-DOM corrected ordering differs from truncated-sample ordering for >=2/7 tasks
2. Bias magnitude (max relative density difference across roles) exceeds 20% for >=2/7 tasks
3. Random-sample baseline shows lower mean absolute bias than first-20 truncation

### 9.2 FALSIFIED-IN-SETTING
If ANY of:
1. Full-DOM corrected ordering is identical to truncated-sample ordering for all 7 tasks
2. Bias magnitude is <10% for all 7 tasks
3. Random-sample baseline shows equal or higher bias than first-20 truncation

### 9.3 MEASUREMENT_INVALID
If:
1. dom_stats fields are missing from any measurement
2. locatable_elements count is unavailable
3. Fewer than 5 tasks have complete data

## 10. Expected Outcomes

### 10.1 Bias is Large and Page-Type-Dependent (H1+H2 supported)
- Truncation significantly biases density calculations
- The FALSIFIED verdict may be an artifact of truncation
- Runtime substrate fix is high priority
- Current density-based ordering metrics are not interpretable

### 10.2 Bias is Small and Uniform (H1+H2 falsified)
- Truncation has minimal effect on density calculations
- The FALSIFIED verdict stands as a genuine null result
- Runtime substrate fix can be deprioritized
- Cross-site testing becomes the priority

### 10.3 Mixed Results
- Bias exists but is not page-type-dependent
- Or bias is page-type-dependent but small in magnitude
- Requires careful interpretation and may need follow-up

## 11. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 12. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
