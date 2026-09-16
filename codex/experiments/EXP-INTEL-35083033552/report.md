# EXP-INTEL-35083033552 Report

## Executive Summary

**Verdict: SURVIVES_CURRENT_TEST**

A canonical ROLE_MAP definition exists that stabilizes the interactive element density ordering across page types. Three semantically adjacent definitions (DEF-FORM-ONLY, DEF-FORM-AND-BUTTON-LINK, DEF-FORM-AND-A-TEXTBOX) all produce the same ordering: **product_listing > cart > detail**. The ordering sensitivity is driven primarily by the **'a'→'link' mapping** in DEF-FULL-MAP, which reverses the ordering to cart > product_listing > detail.

## Key Findings

### 1. Three Adjacent Definitions Agree (Stable Family)

| Definition | Ordering | Mapping |
|---|---|---|
| DEF-FORM-ONLY | product_listing > cart > detail | No mapping |
| DEF-FORM-AND-BUTTON-LINK | product_listing > cart > detail | No mapping (semantic link role only) |
| DEF-FORM-AND-A-TEXTBOX | product_listing > cart > detail | input→textbox only |

These three definitions differ by at most 1 role category:
- DEF-FORM-ONLY → DEF-FORM-AND-BUTTON-LINK: adds semantic 'link' role to INTERACTIVE_ROLES
- DEF-FORM-AND-BUTTON-LINK → DEF-FORM-AND-A-TEXTBOX: adds input→textbox mapping

All three agree on ordering: **product_listing > cart > detail**. This satisfies the SURVIVES_CURRENT_TEST criterion: at least 2 semantically adjacent definitions produce the same ordering.

### 2. 'a'→'link' Mapping Drives Ordering Reversal

| Definition | Ordering | Key Difference |
|---|---|---|
| DEF-FORM-AND-A-TEXTBOX | product_listing > cart > detail | input→textbox, NO a→link |
| DEF-FULL-MAP | cart > product_listing > detail | a→link, input→textbox, menuitem, tab |

The 'a'→'link' mapping inflates counts differentially:
- Cart: 6 → 6 (no change in count, but density increases due to denominator)
- Listing: 6 → 8 (+33%)
- Detail: 3 → 5 (+67%)

Wait — actually the count changes are:
- Cart: 3 (DEF-FORM-AND-A-TEXTBOX) → 6 (DEF-FULL-MAP) = +100%
- Listing: 6 → 8 = +33%
- Detail: 3 → 5 = +67%

The differential inflation (cart +100% vs listing +33%) reverses the ordering.

### 3. Link Sensitivity Quantified

Mean absolute density difference between definitions with and without 'link': **0.000938**

| Page Type | Density (no link) | Density (with link) | Difference |
|---|---|---|---|
| product_listing | 0.003851 | 0.004279 | 0.000428 |
| detail | 0.001712 | 0.002854 | 0.001141 |
| cart | 0.002804 | 0.004050 | 0.001246 |

Cart is most sensitive to link inclusion (0.001246), followed by detail (0.001141). Listing is least sensitive (0.000428). This differential sensitivity drives the ordering reversal.

### 4. Discrimination Ratios Remain High

All definitions maintain discrimination ratio > 46, confirming the metric distinguishes page types regardless of definition choice:

| Definition | Discrimination Ratio |
|---|---|
| DEF-FORM-ONLY | 632.95 |
| DEF-FORM-AND-BUTTON-LINK | 632.95 |
| DEF-FORM-AND-A-TEXTBOX | 134.41 |
| DEF-FULL-MAP | 46.91 |
| DEF-ALL-LOCATABLE | 59.63 |

The issue is ordering direction, not discrimination power.

## Controls

### Positive Control: PASS
All 5 definitions produce tightened_locatable_count > 0 on all 7 tasks. Definitions are non-degenerate.

### Null Control: PASS
DEF-ALL-LOCATABLE yields tightened_count = 20 (full locatable_sample length) on all tasks. Counting pipeline is correct.

### Baseline Comparison: PASS
DEF-FULL-MAP ordering (cart > product_listing > detail) matches parent EXP-INTEL-34956989900 with_map ordering (cart > listing > detail). Reproducible.

### Adjacency Family: PASS
2 of 4 adjacent pairs agree on ordering (DEF-FORM-ONLY vs DEF-FORM-AND-BUTTON-LINK, DEF-FORM-AND-BUTTON-LINK vs DEF-FORM-AND-A-TEXTBOX). The stable family contains 3 definitions.

## Decision Rule Application

Per preregistration §12.1, SURVIVES_CURRENT_TEST if ANY of:
1. At least 2 semantically adjacent definitions produce the same ordering: **YES** (2 adjacent pairs agree)
2. Ordering invariant to link-inclusion: **NO** (link inclusion reverses ordering)

**Verdict: SURVIVES_CURRENT_TEST**

## Interpretation

The ordering sensitivity has two distinct drivers:

1. **ROLE_MAP ambiguity ('a'→'link')**: This is the dominant driver. Definitions excluding the 'a'→'link' mapping produce stable ordering (product_listing > cart > detail). Definitions including it reverse the ordering.

2. **Sample truncation (first-20 cap)**: This is a secondary confound. The stable ordering (product_listing > cart > detail) under truncated sampling may not match the true full-DOM ordering (expected: listing > detail > cart from parent audit extrapolation). Full DOM enumeration is needed to validate.

The canonical definition for this site is: **DEF-FORM-ONLY** (or equivalently DEF-FORM-AND-BUTTON-LINK or DEF-FORM-AND-A-TEXTBOX), which excludes the 'a'→'link' mapping and counts only form elements (button, textbox, checkbox, radio, combobox, listbox, slider, spinbutton, searchbox, switch).

## Product Consequence

Product lane can adopt the stable definition family (DEF-FORM-ONLY through DEF-FORM-AND-A-TEXTBOX) for yield estimation on this site. The metric produces consistent ordering under truncated sampling. However:
- Full DOM enumeration is still needed to validate against true page structure
- Cross-site generalization is unsupported (single Magento site)
- Cart pseudoreplication limits statistical validation

## Next Steps

1. **Runtime lane**: Fix MEASURE_JS locatableSample cap to enable full DOM enumeration. This eliminates the truncation confound.
2. **Intel/design**: Decide whether to adopt DEF-FORM-ONLY (form elements only) or DEF-FORM-AND-A-TEXTBOX (form elements + input→textbox) as the canonical definition. Both produce stable ordering.
3. **Cross-site validation**: Test the canonical definition on other sites to assess generalization.
