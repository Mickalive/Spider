# EXP-INTEL-34956989900 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-34956989900
- **Lane**: Intel
- **Claims**: C-MEAS-VALID, C-CROSSSITE, C-LLM-INHERIT
- **Date**: 2026-09-15
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does element density normalized by `elements_with_bbox` (rather than `total_dom`) resolve the denominator sensitivity that confounded the ordering test under tightened role-only definition, using existing EXP-INTEL-34718481334 raw measurement data?

## 3. Motivation

### 3.1 Parent Experiment History

The parent experiment (EXP-INTEL-34782350557) tested whether a tightened role-only definition of interactive elements would preserve the ordering listing > detail > cart. Under the original definition (DEF-FALLBACK-INTERACTIVE), ordering held: listing 0.048 > detail 0.024 > cart 0.0185.

Under the tightened definition with `total_dom` denominator, ordering reversed: cart 0.00528 > listing 0.00469 > detail 0.00374. This appeared to falsify the metric.

### 3.2 Audit Findings

The audit identified two critical confounds:

1. **VF-DENOMINATOR-SENSITIVITY (major)**: `total_dom` varies across page types (listing ~1700, detail ~1300, cart 1136). Cart's smaller DOM inflates its fraction despite fewer tightened elements. The ordering reversal is driven by denominator variation, not interactive density differences.

2. **VF-SAMPLE-TRUNCATION-CRITICAL (critical)**: `locatable_sample` is capped at 20 entries while `locatable_elements` are 82 (listing), 32 (detail), 21 (cart). Tightened counts are underestimates by factors 4.1x (listing), 1.6x (detail), 1.05x (cart). Differential undercount contributes to ordering reversal.

3. **BF-ORDERING-REVERSAL-ARTIFACT**: Extrapolation to full locatable set (proportional estimate) restores ordering listing 0.019 > detail 0.006 > cart 0.0055, demonstrating the reversal is an artifact of truncated sampling, not a robust tightened-definition effect.

### 3.3 Proposed Resolution

The audit recommended testing `elements_with_bbox` as an alternative denominator. This is the visible-element denominator (elements with bounding boxes in the accessibility tree), which is:
- Smaller than `total_dom` (includes invisible/structural elements)
- More relevant to user-visible interactive density
- Available in existing raw data (1550-1564 listing, 1143-1215 detail, 1070 cart)

If element density (tightened/elements_with_bbox) is more stable than fraction (tightened/total_dom), it resolves the denominator sensitivity confound.

## 4. Hypotheses

### H1: Denominator Resolution
Element density (tightened/elements_with_bbox) ordering listing > detail > cart holds under at least one ROLE_MAP variant.

### H2: Discrimination Preservation
Between-type variance exceeds within-type variance (discrimination ratio > 1.0) under elements_with_bbox denominator.

### H3: Variance Reduction
The coefficient of variation (CV) of element density across page types is lower than the CV of fraction under total_dom denominator.

### H4: ROLE_MAP Sensitivity
Ordering under elements_with_bbox is stable across both ROLE_MAP variants (with and without 'a'->'link' mapping).

## 5. Data Source

### 5.1 Raw Measurement Data
- **Source**: `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json`
- **Origin**: EXP-INTEL-34718481334 frozen measurement data
- **Docker image**: `am1n3e/webarena-verified-shopping:latest`
- **Tasks**: 7 unique pages (3 listing, 3 detail, 1 cart with duplicate)
- **Fields per task**: `total_dom_elements`, `elements_with_bbox`, `locatable_elements`, `locatable_sample` (truncated to 20)

### 5.2 Tightened Counts (from Parent)
- Reuse parent tightened counts from `EXP-INTEL-34782350557/raw_evidence/tightened_results.json`
- These are from the truncated first-20 sample with ROLE_MAP ('a'->'link', 'input'->'textbox')
- For ROLE_MAP-free variant, recompute from `locatable_sample` role values

### 5.3 elements_with_bbox Values (Extracted from Raw)
| Task | total_dom | elements_with_bbox | locatable_elements |
|------|-----------|-------------------|--------------------|
| listing_clothing-shoes-jewelry | 1696 | 1550 | 82 |
| listing_beauty-personal-care | 1707 | 1560 | 82 |
| listing_electronics | 1712 | 1564 | 82 |
| detail_camera | 1395 | 1215 | 32 |
| detail_vr_bag | 1310 | 1149 | 32 |
| detail_pet_camera | 1304 | 1143 | 32 |
| cart_1 | 1136 | 1070 | 21 |

## 6. Analysis Plan

### 6.1 Density Computation
For each of the 7 tasks, compute:
1. **With ROLE_MAP**: `tightened_count_with_map / elements_with_bbox` and `tightened_count_with_map / total_dom`
2. **Without ROLE_MAP**: `tightened_count_without_map / elements_with_bbox` and `tightened_count_without_map / total_dom`

### 6.2 ROLE_MAP-free Tightened Counts
Recompute from `locatable_sample` role values without mapping:
- `INTERACTIVE_ROLES = {'button', 'link', 'textbox', 'checkbox', 'radio', 'combobox', 'listbox', 'menuitem', 'tab', 'slider', 'spinbutton', 'searchbox', 'switch'}`
- Count elements where `role in INTERACTIVE_ROLES` (without 'a'->'link' mapping)
- Parent audit recomputed: listing 6, detail 2, cart 3

### 6.3 Per-Type Statistics
For each denominator × ROLE_MAP combination:
- Per-type mean density
- Per-type CV
- Between-type variance
- Within-type variance (deduped cart: n=1 distinct)
- Discrimination ratio (between/within)

### 6.4 Ordering Test
For each combination, report ordering of type means (listing, detail, cart).

### 6.5 Comparison with Parent
Compare elements_with_bbox density ordering with:
- Parent total_dom fraction ordering (reversed: cart > listing > detail)
- Parent extrapolated full-locatable-set ordering (listing > detail > cart)

## 7. Controls

### 7.1 Positive Control
All tasks have tightened_locatable_count > 0 (reuses parent: listing 8, detail 5, cart 6 with map; listing 6, detail 2, cart 3 without map).

### 7.2 Null Control
tightened_locatable_count <= original_locatable_elements on all tasks (reuses parent).

### 7.3 Denominator Sensitivity Control
The ratio `elements_with_bbox / total_dom` should be > 0.8 for all tasks (visible elements are most of DOM). If this fails, elements_with_bbox is not a meaningfully different denominator.

### 7.4 Extrapolation Consistency
Ordering under elements_with_bbox should be consistent with parent audit's extrapolated full-locatable-set ordering (listing > detail > cart), providing cross-validation.

## 8. Validity Threats

### 8.1 Sample Truncation (Inherited)
Tightened counts are from truncated first-20 sample, not full DOM enumeration. Density values are proportional estimates. Ordering may still be affected by differential truncation (listing 4.1x undercount, detail 1.6x, cart 1.05x). Mitigation: compare with extrapolated ordering from parent audit.

### 8.2 Cart Pseudoreplication (Inherited)
Cart n=2 identical entries (same URL). Deduped cart n=1 distinct. Within-type CV for cart is undefined. Mitigation: report deduped statistics separately.

### 8.3 ROLE_MAP Deviation (Inherited)
The 'a'->'link' mapping inflates counts by 33-150%. Without mapping, detail drops from 5 to 2 (60% reduction). This is an undocumented deviation from frozen spec. Mitigation: test both variants explicitly.

### 8.4 Single-Site Generalization
All data from one Magento shopping site. elements_with_bbox behavior on other sites unknown. Mitigation: bounded to this site; cross-site claims remain unsupported.

### 8.5 Proportional Estimation Assumption
Extrapolation assumes truncated sample is representative of full locatable set. If truncated first-20 are systematically different from remaining elements, proportional estimates may be biased. Mitigation: acknowledge as limitation; full DOM enumeration required for definitive test.

## 9. Decision Rules

### 9.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Element density ordering listing > detail > cart holds under elements_with_bbox in at least one ROLE_MAP variant
2. Between-type variance > within-type variance (discrimination ratio > 1.0) under elements_with_bbox in at least one ROLE_MAP variant
3. Positive control passes (all tightened > 0)
4. Null control passes (tightened <= original)

### 9.2 FALSIFIED-IN-SETTING
If ANY of:
1. Element density ordering does NOT hold under elements_with_bbox in any ROLE_MAP variant
2. Discrimination ratio <= 1.0 under elements_with_bbox in all variants
3. Positive or null control fails

### 9.3 MEASUREMENT_INVALID
If:
1. elements_with_bbox values are missing from raw data
2. Raw data file is corrupted or inaccessible
3. Extraction script fails

## 10. Expected Outcomes

### 10.1 Positive Result (SURVIVES_CURRENT_TEST)
- Resolves denominator sensitivity confound from EXP-INTEL-34782350557
- Validates elements_with_bbox as appropriate normalizer for interactive density
- Advances metric toward product-ready yield estimation
- Provides denominator-controlled basis for cross-site comparison
- Next step: cross-site measurement with full DOM enumeration

### 10.2 Negative Result (FALSIFIED-IN-SETTING)
- elements_with_bbox does not resolve denominator sensitivity
- Interactive fraction metric remains denominator-confounded
- Product lane must seek alternative normalization or abandon fraction-based yield metrics
- Does NOT close the metric approach entirely — only this specific denominator

### 10.3 Invalid Result (MEASUREMENT_INVALID)
- Data extraction infrastructure issue, not scientific evidence
- Requires data repair before retesting

## 11. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 12. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
