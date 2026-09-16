# EXP-INTEL-34718481334 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-34718481334
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT
- **Parent Experiment**: EXP-INTEL-34607693437 (verdict: MEASUREMENT_INVALID, audit: MEASUREMENT_INVALID)
- **Date**: 2026-09-12
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does full-page DOM element enumeration (without viewport chrome filtering) produce a stable and meaningful yield metric for SPIDER fragment capture, and what fraction of page elements does the fragment model actually retain?

## 3. Motivation

### 3.1 The Blocking Problem

The 812-task WebArena-Verified corpus is the proposed testbed for C-CROSSSITE (cross-site transfer) and C-LLM-INHERIT (LLM agent inheritance). Interpreting this corpus requires knowing the **fragment yield**: what fraction of page elements does the SPIDER fragment model capture?

Three consecutive experiments (EXP-INTEL-34546944360, EXP-INTEL-34607693437, and this one) have failed to establish a valid yield metric:

1. **Viewport intersection (threshold 0.5, 1280×720)**: Captures only fixed Magento 2 navigation chrome (constant 108 elements, stdev=0.0 across all page types). Not page content. **REJECTED.**

2. **yield_locatable = viewport_elements / locatable_elements**: Numerator (108) and denominator (21-82) use different element definitions. Values >1.0 are mathematically meaningless. **REJECTED.**

3. **CDP yield = viewport_elements / total_dom_elements**: Stable (CV=0.17) but measures chrome ratio, not interactive content yield. **REJECTED as primary metric.**

The parent handoff recommended routing to Runtime lane to develop "content-aware element enumeration." However, the Intel lane can determine WHETHER a viable approach exists before Runtime implements it.

### 3.2 The Key Insight from Parent Data

The parent measured both `locatable_elements` (interactive, using frozen DEF-FALLBACK-INTERACTIVE) and `total_dom_elements` (all DOM nodes). These were never combined into a yield metric because the experiment focused on the broken viewport-based yield.

From parent data:
- **product_listing** (n=2): locatable=82, total_dom≈1675, **interactive_fraction ≈ 0.049**
- **detail** (n=2): locatable=32, total_dom≈1353, **interactive_fraction ≈ 0.024**
- **cart** (n=1): locatable=21, total_dom=1136, **interactive_fraction ≈ 0.0185**

This metric:
- **Varies by page type** (0.049 vs 0.024 vs 0.0185 — 2.7× range)
- **Is stable within types** (locatable counts identical within listing and detail pairs)
- **Does NOT use viewport filtering** (entire page DOM is the denominator)
- **Uses the frozen DEF-FALLBACK-INTERACTIVE definition** (reusable from parent)

This experiment tests whether this metric replicates with fresh samples and stabilizes across page types.

### 3.3 Why This Experiment Is Highest-Information

The denominator question has blocked three experiments. If interactive_fraction (locatable/total_dom) is stable within types and varies between types, it provides a viable content-aware yield metric. If it's unstable, this approach is definitively closed and product lane must accept yield as inherently page-type-dependent.

Either outcome changes a product decision. No other experiment can close this blocking question.

## 4. Hypotheses

### H1: Full-Page DOM Counts Vary by Page Type
Total DOM element counts vary across page types (stdev > 0 across all measured tasks). This verifies the measurement captures page content, not fixed chrome.

**Falsification**: Total DOM counts are constant across all page types (stdev = 0).

### H2: Interactive Fraction Is Stable Within Page Types
Interactive fraction (locatable_elements / total_dom_elements using frozen DEF-FALLBACK-INTERACTIVE) has CV < 0.3 within each page type for types with n ≥ 2 tasks. This verifies the metric is reliable when page type is held constant.

**Falsification**: CV > 0.3 within any page type with n ≥ 2.

### H3: Interactive Fraction Discriminates Between Page Types
Between-type variance of mean interactive fraction exceeds within-type variance. This verifies the metric captures real content differences (product listings have more interactive elements than cart pages).

**Falsification**: Between-type variance ≤ within-type variance (metric does not discriminate).

### H4: Playwright Accessibility Snapshot Viability
Playwright `page.accessibility.snapshot()` returns > 10 nodes on at least 1 task while DOM count > 100. If this holds, the accessibility tree provides richer element information than raw DOM queries.

**Falsification**: Accessibility snapshot returns < 10 nodes on all tasks while DOM count > 100 (accessibility tree is degenerate in headless Chromium, as found by parent via CDP).

### H5: Checkout Page Accessibility (Exploratory)
If checkout page (localhost:8080/checkout/) is accessible without redirect to port 7770, measure its interactive fraction. If it redirects, note as BLOCKED and use checkout/cart/ data from parent for comparison.

**BLOCKED status**: If checkout/ redirects to port 7770, mark BLOCKED with infrastructure proof.

## 5. Measurement Plan

### 5.1 Task Selection

**Shopping tasks**: 10 tasks randomized from WebArena-Verified dataset:
- 3 product-listing pages
- 3 product-detail pages
- 2 cart pages
- 2 checkout pages

Randomization: Use Python `random.Random(seed=99).choices()` to select task URLs from the WebArena-Verified dataset, stratified by page type. Record task IDs and placeholder substitutions. Seed 99 is chosen to avoid overlap with parent (which used its own randomization).

### 5.2 Measurement Protocol

For each task:

1. **Docker setup**: Pull and start `am1n3e/webarena-verified-shopping:latest`. Record image digest (sha256) before measurement.
2. **Browser context**: Create fresh Playwright Chromium browser context (no shared cookies/session). Viewport: 1280×720.
3. **Navigation**: Navigate to task URL. Wait for `networkidle` (Playwright default timeout 30s).
4. **Full-page DOM enumeration** (primary method):
   - Execute JavaScript in page context:
     ```javascript
     // Total DOM elements
     const totalDom = document.querySelectorAll('*').length;
     
     // Elements with bounding box
     const elementsWithBbox = [...document.querySelectorAll('*')].filter(el => {
       const rect = el.getBoundingClientRect();
       return rect.width > 0 && rect.height > 0;
     }).length;
     
     // Interactive elements (DEF-FALLBACK-INTERACTIVE)
     const interactiveRoles = new Set(['button','link','textbox','checkbox','radio','combobox','listbox','menuitem','tab','slider','spinbutton','searchbox','switch']);
     const locatableElements = [...document.querySelectorAll('*')].filter(el => {
       const rect = el.getBoundingClientRect();
       const hasBbox = rect.width > 0 && rect.height > 0;
       if (!hasBbox) return false;
       const role = el.getAttribute('role') || el.tagName.toLowerCase();
       if (interactiveRoles.has(role)) return true;
       if (el.onclick || el.onsubmit) return true;
       if (el.closest('form')) return true;
       if (el.getAttribute('aria-label') || el.getAttribute('aria-describedby')) return true;
       return false;
     }).length;
     
     // Viewport elements (for cross-denominator comparison)
     const viewportRect = {x: 0, y: 0, width: 1280, height: 720};
     const viewportElements = [...document.querySelectorAll('*')].filter(el => {
       const rect = el.getBoundingClientRect();
       const intersection = Math.max(0, Math.min(rect.right, viewportRect.width) - Math.max(rect.left, viewportRect.width)) *
                           Math.max(0, Math.min(rect.bottom, viewportRect.height) - Math.max(rect.top, viewportRect.height));
       const area = rect.width * rect.height;
       return area > 0 && (intersection / area) > 0.5;
     }).length;
     
     JSON.stringify({totalDom, elementsWithBbox, locatableElements, viewportElements});
     ```
5. **Playwright accessibility snapshot** (secondary method):
   - Call `page.accessibility.snapshot()` after DOM enumeration
   - Record tree node count and depth
   - If > 10 nodes, use as secondary metric; if < 10, note as degenerate
6. **Raw artifact**: Save full DOM query results and accessibility snapshot as JSON with sha256.
7. **Cleanup**: Close browser context and Docker container.

### 5.3 Yield Calculation

For each task:
- `interactive_fraction` = locatable_elements / total_dom_elements (primary metric)
- `cdp_yield` = viewport_elements / total_dom_elements (cross-denominator comparison with parent)
- `viewport_locatable_yield` = viewport_elements / locatable_elements (parent's broken metric, for reference)
- `accessibility_node_count` = number of nodes in accessibility snapshot (if available)

### 5.4 Comparison with Parent

For each page type, compare:
- Parent locatable_elements vs this experiment's locatable_elements
- Parent total_dom_elements vs this experiment's total_dom_elements
- New interactive_fraction vs parent's implied interactive_fraction (computed from parent data)

## 6. Controls

### 6.1 Positive Control
- Total DOM count > 100 on all tasks (page content is enumerated)
- Locatable elements > 0 on all tasks (interactive elements exist)
- Playwright accessibility snapshot returns > 0 nodes on at least 1 task

### 6.2 Stability Control
- Interactive fraction within-type CV < 0.3 for at least 2 page types with n ≥ 2
- This is the primary validity test: if the metric is unstable within types, it's not usable

### 6.3 Discrimination Control
- Between-type variance > within-type variance
- Product listings should have higher interactive fraction than cart pages (more links, buttons, forms)

### 6.4 Parent Replication Control
- Locatable elements per page type within 20% of parent values (listing≈82, detail≈32, cart≈21)
- Total DOM per page type within 20% of parent values (listing≈1675, detail≈1353, cart≈1136)
- If replication fails, note as drift and investigate Docker image digest

### 6.5 Checkout Coverage Control
- At least 2 checkout tasks measured (or BLOCKED with infrastructure proof if checkout/ redirects)
- If checkout uses checkout/cart/ (like parent), note as proxy and exclude from primary metrics

### 6.6 Null Control (Definition Stability)
- Interactive fraction computed with frozen DEF-FALLBACK-INTERACTIVE produces non-zero values on all tasks (definition is not degenerate)

## 7. Statistical Analysis

### 7.1 Primary Metrics
- `interactive_fraction_mean`: mean interactive fraction across all tasks
- `interactive_fraction_cv`: CV across all tasks (expected to be moderate due to type variation)
- `interactive_fraction_within_type_cv`: CV within each page type (expected < 0.3)
- `interactive_fraction_between_type_variance`: variance of mean interactive fraction across page types
- `interactive_fraction_within_type_variance`: mean variance within page types
- `discrimination_ratio`: between_type_variance / within_type_variance (expected > 1)

### 7.2 Secondary Metrics
- `total_dom_mean`, `total_dom_stdev`: full-page DOM element counts
- `locatable_mean`, `locatable_stdev`: interactive element counts
- `cdp_yield_mean`, `cdp_yield_cv`: cross-denominator comparison with parent
- `accessibility_snapshot_nodes`: accessibility tree node count (if available)
- `parent_replication_delta`: percentage difference from parent values per page type

### 7.3 No Formal Hypothesis Testing
This experiment is a metric validation exercise, not a confirmatory hypothesis test. The decision rule is threshold-based (CV < 0.3, discrimination ratio > 1). Effect sizes and confidence intervals are reported but not used for binary decisions.

## 8. Validity Threats

### 8.1 Docker Drift
Different image digests may have different page structures. The parent showed CDP yield stable across digests, but locatable counts shifted. **Mitigation**: Record image digest before measurement and compare to parent. If counts differ by > 30%, flag as drift.

### 8.2 Sample Size
10 tasks (3 listing, 3 detail, 2 cart, 2 checkout) may be insufficient for stable CV estimation. The parent used 7 tasks and found viewport CV=0.0 (constant). With 10 tasks and 4 types, within-type CV estimates have wider confidence intervals for n=2 types. **Mitigation**: Report CV with sample size; the threshold (0.3) is conservative.

### 8.3 Checkout Proxy
Checkout tasks may use checkout/cart/ (same as cart page) if checkout/ redirects to port 7770. This means checkout data is actually cart data. **Mitigation**: Note as proxy; exclude checkout from primary metrics if proxy is confirmed. The parent's checkout_proxy finding is expected to persist.

### 8.4 JavaScript Execution Context
DOM queries executed via `page.evaluate()` run in the page's JavaScript context. Some SPAs may modify DOM after load. **Mitigation**: Wait for networkidle before measurement; this is the same protocol as parent.

### 8.5 Accessibility Snapshot Degradation
Parent found CDP Accessibility.getFullAXTree returns only 1 node. Playwright's `page.accessibility.snapshot()` may use a different API path. **Mitigation**: If snapshot returns < 10 nodes, fall back to DOM queries. The primary metric uses DOM, not accessibility tree.

### 8.6 Definition Reuse
The frozen DEF-FALLBACK-INTERACTIVE definition was designed for viewport-filtered measurement. Applying it to full-page elements may capture different element sets. **Mitigation**: The definition is element-level (role, bbox, aria, form membership), not viewport-dependent. Full-page application should capture the same element types, just more of them.

### 8.7 Non-Random Sampling
Tasks are randomized from the WebArena-Verified dataset but the dataset may not represent all shopping pages. **Mitigation**: Known limitation; the experiment bounds yield for the 812-task corpus specifically.

## 9. Decision Rules

### 9.1 SURVIVES_CURRENT_TEST
If ALL of:
1. total_dom_elements stdev > 0 across all measured tasks (page content varies)
2. interactive fraction within-type CV < 0.3 for at least 2 page types with n ≥ 2
3. interactive fraction between-type variance > within-type variance (metric discriminates)
4. at least 8 tasks measured across ≥ 3 page types
5. no pipeline errors

**Consequence**: Full-page interactive fraction is a viable content-aware yield metric. Product lane can use locatable/total_dom for C-CROSSSITE/C-LLM-INHERIT evaluation. Runtime lane can implement the measurement substrate. The 812-task corpus becomes usable.

### 9.2 FALSIFIED-IN-SETTING
If ANY of:
1. total_dom_elements stdev = 0 across all tasks (page content doesn't vary — measurement broken)
2. interactive fraction within-type CV > 0.3 on all page types with n ≥ 2 (metric unstable)
3. interactive fraction between-type variance ≤ within-type variance (metric doesn't discriminate)
4. positive control fails (total_dom < 100 or locatable = 0 on any task)

**Consequence**: Full-page enumeration doesn't stabilize yield. Product lane must either (a) accept yield as page-type-dependent and report per-type yields, (b) use CDP yield (8%) as conservative floor, or (c) abandon yield as a metric.

### 9.3 MIXED
If:
1. Some controls pass but others fail (e.g., within-type stable but between-type doesn't discriminate)
2. Checkout BLOCKED due to infrastructure
3. Accessibility snapshot BLOCKED (returns < 10 nodes)

**Consequence**: Partial viability. Product lane can use the metric with caveats (e.g., per-type calibration required).

### 9.4 MEASUREMENT_INVALID
If:
1. < 8 tasks measured
2. Docker container cannot be started
3. Playwright cannot load pages
4. Script errors prevent measurement

**Consequence**: Not scientific evidence. Infrastructure must be fixed before retry.

## 10. Expected Outcomes

### 10.1 Positive Result (SURVIVES_CURRENT_TEST)
- Full-page interactive fraction validated as content-aware yield metric
- 812-task corpus viability confirmed for C-CROSSSITE/C-LLM-INHERIT
- Product lane proceeds to integration experiments
- Runtime lane implements measurement substrate using DOM queries
- Expected interactive fraction range: 0.02-0.05 (from parent data)

### 10.2 Negative Result (FALSIFIED-IN-SETTING)
- Full-page enumeration doesn't stabilize yield
- Product lane accepts yield as page-type-dependent
- Alternative: use CDP yield (8%) as conservative floor
- The denominator question is closed for this approach

### 10.3 Partial Result (MIXED)
- Metric is stable within types but doesn't discriminate between types
- Product lane uses per-type calibration
- Or: metric discriminates but is unstable within types
- Product lane uses median rather than mean

### 10.4 Invalid Result (MEASUREMENT_INVALID)
- Infrastructure failure, not scientific evidence
- Retry after fixing Docker/Playwright issues

## 11. Artifacts

### 11.1 Required Artifacts
- `measure_fullpage_yield.py`: Frozen measurement script with sha256
- `exp347_raw_results.json`: Per-task measurements with all metrics under all definitions
- `fullpage_sample_<task>.json`: Per-task DOM query results with element counts by type
- `accessibility_snapshot_<task>.json`: Per-task Playwright accessibility snapshot (if available)

### 11.2 Reference Artifacts (from parent)
- `research/experiments/EXP-INTEL-34607693437/frozen_definition.json`: Frozen DEF-FALLBACK-INTERACTIVE (sha256: 9c6bb9a03b6cbcdf206ce9192f5fcf60c79d6df8f65850027aeee50b61f503d5)
- `research/experiments/EXP-INTEL-34607693437/exp346_raw_results.json`: Parent measurements for replication comparison

## 12. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 13. Freeze Statement

This preregistration is frozen BEFORE any measurement code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
