# EXP-INTEL-34607693437 Report

## Executive Summary

**Status**: MEASUREMENT_INVALID | **Outcome**: FALSIFIES

The frozen measurement script contains a counting bug that produces meaningless `yield_locatable` values (>1.0 on all tasks). The viewport constant anomaly (exactly 108 elements across all page types) persists, and viewport samples reveal the measurement captures only Magento 2 navigation chrome, not page content. This is a structural measurement failure, not a page content finding.

The forensic analysis of Method1's 150-element estimate was successful but INCONCLUSIVE: the estimate is a pre-computed heuristic input, not traceable to any DOM/accessibility tree counting method. The fallback definition (DEF-FALLBACK-INTERACTIVE) was frozen and documented.

GitLab and Reddit tasks remain BLOCKED (Docker images not pulled).

## 1. Forensic Analysis

### 1.1 Method1 Trace Result: INCONCLUSIVE

The forensic analysis of `analysis_output.json` from EXP-INTEL-33945226776 revealed:

- Method1's 150-element estimate for `product_listing` is a **pre-computed heuristic INPUT** to the yield model, not an OUTPUT of any element-counting algorithm.
- The estimate appears to be a judgment-based "typical DOM node count" (round numbers: 150, 120, 60 for different page types).
- There is **no code** in the derivation that traverses a DOM or accessibility tree to produce the number 150.
- The element definition is **UNKNOWN**: the `estimated_elements` field does not specify what constitutes an "element."

**Mapping to candidate definitions**:
- Definition 1 (all-elements-with-bbox): POSSIBLE but unlikely — 150 is too low for all visible elements (parent measured 1392-1571).
- Definition 2 (interactive-only): PLAUSIBLE — 150 interactive elements is reasonable for a product listing with ~20 products.
- Definition 3 (parent CSS selectors): PLAUSIBLE — parent measured 258 under CSS selectors.

**Conclusion**: The forensic analysis cannot resolve which candidate definition Method1's 150 maps to. The functional fallback definition (Definition 2, interactive-only) was frozen.

### 1.2 Fallback Definition Frozen

**Definition ID**: DEF-FALLBACK-INTERACTIVE

**Text**: Elements with non-null bounding box (width > 0 AND height > 0) AND (role is one of: button, link, textbox, checkbox, radio, combobox, listbox, menuitem, tab, slider, spinbutton, searchbox, switch OR has onclick/onsubmit handler OR is within a form element OR has aria-label or aria-describedby with non-empty text).

**Rationale**: This captures "interactive elements that an agent can use for inheritance" — the functional purpose of the SPIDER fragment model. It is the most defensible definition when the original derivation is ambiguous.

**Expected yield range**: 0.25-0.40 (from parent experiment: ~0.32 under interactive-only).

## 2. Measurement Results

### 2.1 Raw Measurements

7 shopping tasks measured (2 product_listing, 2 detail, 1 cart, 2 checkout):

| Task | Type | DOM Elements | Viewport | Locatable | yield_cdp | yield_locatable |
|------|------|-------------|----------|-----------|-----------|----------------|
| listing_tools | product_listing | 1653 | 108 | 82 | 0.0653 | 1.3171 |
| listing_clothing | product_listing | 1696 | 108 | 82 | 0.0637 | 1.3171 |
| detail_camera | detail | 1395 | 108 | 32 | 0.0774 | 3.3750 |
| detail_vr_bag | detail | 1310 | 108 | 32 | 0.0824 | 3.3750 |
| cart_1 | cart | 1136 | 108 | 21 | 0.0951 | 5.1429 |
| checkout_cart_1 | checkout | 1136 | 108 | 21 | 0.0951 | 5.1429 |
| checkout_cart_2 | checkout | 1136 | 108 | 21 | 0.0951 | 5.1429 |

### 2.2 Critical Bug: yield_locatable > 1.0

**All yield_locatable values are > 1.0** (range: 1.32-5.14). This is mathematically impossible if viewport should be a subset of locatable.

**Root cause**: The counting bug:
- `viewport_elements` counts **ALL** DOM elements in the viewport rect (108), including non-interactive elements (HEADER, DIV, UL, LI, SPAN).
- `locatable_elements` counts only **interactive** elements matching the frozen definition (21-82).
- `yield_locatable = viewport_elements / locatable_elements` uses **different element definitions** for numerator and denominator.

**Impact**: All `yield_locatable` values are invalid and cannot be used for any yield claim.

### 2.3 Viewport Constant Anomaly

**Viewport elements = 108 across ALL 7 tasks** (stdev = 0.0). This is the same anomaly from the parent experiment.

**Viewport sample analysis**: All 20 sampled viewport elements across ALL page types are identical Magento 2 navigation header elements:
- HEADER, DIV, DIV, UL, LI, A, LI, A, LI, A, LI, A, LI, A, A, A, SPAN, DIV, SPAN, SPAN
- Interactive fraction: 6/20 = 30% (all "A" = link elements)
- Non-interactive: HEADER, DIV, UL, LI, SPAN

**Diagnosis**: The viewport measurement captures **fixed navigation chrome**, not page content. The 108 elements are the Magento 2 header bar, which is identical across all page types.

### 2.4 Corrected Estimates

Estimating viewport_locatable (interactive elements in viewport) from viewport_sample:
- Estimated viewport_locatable: 108 × 30% = 32
- Corrected yield_locatable by page type:
  - product_listing: 32/82 = 0.39 (within expected range 0.25-0.40)
  - detail: 32/32 = 1.0 (all locatable elements in viewport — possible if all interactive elements are above fold)
  - cart: 32/21 = 1.52 (>1.0, impossible — estimate unreliable)
  - checkout: 32/21 = 1.52 (>1.0, impossible — estimate unreliable)

**Note**: Corrected estimates are unreliable because the viewport_sample is biased toward early DOM elements (navigation), not a random sample of viewport elements.

### 2.5 CDP Yield

`yield_cdp` (viewport_elements / total_dom_elements) has CV = 0.17 across all tasks (below 0.2 threshold). Mean = 0.082, slightly higher than parent 0.0426. CDP yield is stable but measures a different quantity (all DOM elements, not just interactive).

## 3. Hypothesis Evaluation

### H1: Definition Resolution — INCONCLUSIVE
Forensic analysis could not trace Method1's 150-element estimate to a specific counting method. Fallback definition frozen (DEF-FALLBACK-INTERACTIVE).

### H2: Yield Stability — FAIL
Corrected yield_locatable CV = 0.48 (threshold: <0.2). Yield varies significantly by page type. Even corrected estimates are unreliable due to viewport anomaly.

### H3: Method1 Compatibility — FAIL
Corrected mean yield_locatable = 1.05, delta = 68.5pp from Method1 0.365 (threshold: <15pp). Method mismatch even under corrected counting.

### H4: Checkout Yield — FAIL
Checkout tasks use checkout/cart/ (same as cart page). Checkout_cart_1 and checkout_cart_2 are identical to cart_1. True checkout page behavior not measured. Checkout delta from other page types = 66.3pp (threshold: <20pp).

### H5: Site-Type Comparison — BLOCKED
Docker images for GitLab and Reddit not pulled. H5 cannot be tested.

### H6: Viewport Anomaly — PERSISTS
Viewport elements constant at 108 across ALL page types. Viewport samples show only navigation header. Measurement captures fixed chrome, not page content.

## 4. Decision Rule Application

Per the frozen decision rules:

1. **Forensic analysis**: INCONCLUSIVE (definition_resolved=false, fallback_frozen=true) ✓
2. **yield_locatable CV**: 0.48 > 0.2 (yield unstable) ✗
3. **Method1 compatibility**: delta = 68.5pp > 15pp (method mismatch) ✗
4. **Checkout coverage**: 2 tasks measured, but same as cart page (not true checkout) ⚠
5. **Viewport anomaly**: PERSISTS (constant 108, captures navigation chrome only) ✗

**Verdict**: FALSIFIED-IN-SETTING (viewport anomaly persists, yield unstable, method mismatch)

**Status**: MEASUREMENT_INVALID (counting bug makes yield_locatable meaningless)

## 5. Consequences

### 5.1 For C-CROSSSITE / C-LLM-INHERIT
The 812-task corpus **cannot be used for yield claims** under the frozen definition. The viewport measurement captures navigation chrome, not page content. Product lane must either:
1. Redesign the observation pipeline to capture page content (not just viewport intersection)
2. Use CDP yield (8.2%) as the conservative floor
3. Explore alternative measurement approaches (e.g., full-page accessibility tree, scroll-based measurement)

### 5.2 For Denominator Resolution
The denominator ambiguity **cannot be resolved** by this experiment because the measurement approach (viewport intersection) fails to capture page content. The fallback definition (interactive-only) is frozen but untestable with the current measurement method.

### 5.3 For Method1
Method1's 0.365 estimate **cannot be validated or falsified** because:
1. The element definition is unknown (forensic inconclusive)
2. The measurement approach fails to capture page content (viewport anomaly)
3. Even corrected estimates are unreliable

## 6. Recommendations

1. **Fix the viewport measurement**: The current approach (viewport intersection with threshold 0.5) captures only fixed navigation chrome. Need a method that captures page content elements.
2. **Investigate the 108 constant**: Determine why exactly 108 DOM elements intersect the viewport. Is this the Magento 2 header element count? Does scrolling reveal more elements?
3. **Fix the counting bug**: Ensure viewport_locatable and locatable use the same element definition (both should count only interactive elements).
4. **Access true checkout page**: Resolve the port 7770 redirect to measure actual checkout behavior.
5. **Pull GitLab/Reddit Docker images**: Enable H5 site-type comparison.

## 7. Artifacts

- `exp346_raw_results.json`: Raw measurements for 7 tasks (fa71b3b...)
- `measure_yield_exp346.py`: Frozen measurement script (ee76fc9a...)
- `frozen_definition.json`: DEF-FALLBACK-INTERACTIVE (9c6bb9a0...)
- `method1_trace.json`: Forensic analysis (bab6a99a...)
- `artifacts/exp346_raw_results.json`: Duplicate raw results (2df4a7ce...)
- `artifacts/viewport_sample_*.json`: Viewport element samples per task
- `artifacts/raw_ax_tree_*.json`: Raw accessibility tree data per task
