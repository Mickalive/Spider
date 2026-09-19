# EXP-INTEL-35462974425 — Report

## Experiment Metadata

- **Experiment ID**: EXP-INTEL-35462974425
- **Lane**: intel
- **Status**: BLOCKED
- **Outcome**: NOT_APPLICABLE
- **Parent**: EXP-INTEL-35445596324 (MIXED verdict, C6 FAIL: canonical recipe agreement 55.95% at truncated-first-20)

## Executive Summary

**The experiment is BLOCKED by data unavailability.** The frozen C3 gate requires that `locatable_sample` contain >20 elements for at least 5 of 7 tasks. All 7 tasks have exactly 20 elements in `locatable_sample` — the raw data was truncated to first-20 DOM elements at collection time in EXP-INTEL-34782350557. Full DOM locatable_sample (n=21-82 per task) is not available in the existing raw evidence. The hypothesis about full DOM ranking stability remains **UNTESTED**.

## C3 Gate Result

| Metric | Value |
|--------|-------|
| Tasks with locatable_sample > 20 | 0/7 |
| Threshold | >=5 |
| C3 PASS | **FALSE** |
| Experiment Status | **BLOCKED** |

### Element Count Details

| Task | locatable_sample | locatable_elements | elements_with_bbox | page_type |
|------|-----------------|-------------------|-------------------|-----------|
| listing_clothing-shoes-jewelry | 20 | 82 | 1550 | product_listing |
| listing_beauty-personal-care | 20 | 82 | 1560 | product_listing |
| listing_electronics | 20 | 82 | 1564 | product_listing |
| detail_camera | 20 | 32 | 1215 | detail |
| detail_vr_bag | 20 | 32 | 1149 | detail |
| detail_pet_camera | 20 | 32 | 1143 | detail |
| cart_1 | 20 | 21 | 1070 | cart |

**Critical distinction**: `locatable_elements` (82/32/21) is the total count of locatable elements on the page. `locatable_sample` is a per-element array containing tag/role/ariaLabel/inForm/x/y/w/h for each element. The `locatable_sample` array was capped at 20 elements at collection time, while the page metadata reports the full count.

## Frozen Decision Rule Evaluation

Per the frozen decision_rule:

- **C1**: NOT EVALUATED (blocked by C3)
- **C2**: NOT EVALUATED (blocked by C3)
- **C3**: **FAIL** — 0/7 tasks have locatable_sample > 20 elements
- **C4-C7**: NOT EVALUATED (blocked by C3)

**Verdict mapping**: NOT C3 → BLOCKED (data unavailable, experiment cannot proceed)

## Baseline Context (Truncated-First-20)

For reference, baseline controls were run on the available truncated-first-20 data:

| Control | Result | Notes |
|---------|--------|-------|
| PC1 (positive control) | PASS (eta2=1.0 for all features) | Confirms template invariance on truncated data |
| NC1 (null control) | PASS (eta2=0.0) | Hierarchy density degenerate, consistent with parent |
| Non-recipe pipeline max eta2 | 0.999645 | Matches parent exactly |
| Ranking preserved | True (all 6 combos) | Listing > detail preserved |

These results confirm the truncated-first-20 data is consistent with the parent experiment, but provide NO evidence about full DOM behavior.

## Root Cause

The data truncation occurred at collection time in EXP-INTEL-34782350557. The collection substrate (SPIDER browser automation on the Magento Docker container `am1n3e/webarena-verified-shopping:latest`) recorded `locatable_sample` capped at 20 elements per task, while the page metadata correctly reports the full element counts (82/32/21 locatable elements, 1550-1564/1215-1143/1070 elements_with_bbox).

This truncation was not detected in prior experiments because all prior experiments operated within the truncated-first-20 range. The parent experiment (EXP-INTEL-35445596324) specifically tested sample-size sensitivity at n=5/10/15/20, all within the available range. The full DOM question was identified as the highest-information next step, but the data to answer it was never collected.

## Unblocked Next Step

To unblock this experiment, full DOM `locatable_sample` must be re-collected from the Magento Docker container. The smallest action:

1. Start the Magento Docker container (`am1n3e/webarena-verified-shopping:latest`)
2. Navigate to the 7 task URLs
3. Collect ALL elements with bbox (not truncated to first-20)
4. Record the full `locatable_sample` array per task

Estimated cost: 5-10 minutes of browser automation + the offline analysis from this script.

## Product Consequences

**No product consequence authorized.** The BLOCKED status means:

- The MIXED verdict from parent EXP-INTEL-35445596324 remains the latest valid evidence
- Recipe density viability for MIXED handling is still unresolved
- The 31x recipe material gap (EXP-INTEL-35264637598) remains unactionable
- Product lane must continue using non-recipe density only (100% ranking agreement per parent B3)

The hypothesis that ranking instability is a truncation artifact vs. structural limitation is **carried forward unresolved**.
