# EXP-INTEL-34546944360 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-34546944360
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT
- **Date**: 2026-09-11
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

What is the correct yield denominator for SPIDER fragment model — CDP accessibility tree node count or Playwright locatable element count — and does the locatable yield (~0.38) hold across randomized shopping page types with scrolled content?

## 3. Motivation

The parent experiment (EXP-INTEL-34377576886) established:
- CDP accessibility tree: ~2296 nodes, ~258 locatable, 98 viewport elements (N=2 pilot)
- Heuristic yield 0.65: FALSIFIED under both denominators
- Method1 yield 0.365: FALSIFIED under CDP (32pp delta), SUPPORTED under locatable (1.5pp delta)

The denominator ambiguity is the single blocking question for interpreting the 812-task corpus. Under CDP denominator (98/2296=0.0427), both heuristic and Method1 are falsified. Under locatable denominator (98/258=0.38), Method1 is SUPPORTED within 1.5pp.

Method1 modeled ~150 interactive elements for shopping product-listing pages. The key insight: 150 elements is far closer to 258 locatable elements than 2296 CDP nodes. This suggests Method1 counted interactive/locatable elements, not full AX tree nodes.

**This experiment resolves the denominator ambiguity by:**
1. Examining Method1 derivation to confirm what it counted
2. Measuring yield across 8+ randomized shopping tasks
3. Reporting BOTH yield_cdp and yield_locatable for each task
4. Testing scrolled content to determine if initial-viewport is representative
5. Measuring gitlab and reddit tasks for site-type variation

## 4. Hypotheses

### H1: Denominator Resolution
Method1's 150-element shopping model counts locatable/interactive elements, not CDP nodes. This can be confirmed by examining the derivation in EXP-INTEL-33945226776.

### H2: Locatable Yield Stability
yield_locatable = viewport_elements / locatable_elements is stable across shopping page types (CV < 0.2 across 8+ tasks).

### H3: Method1 Agreement
yield_locatable mean is within 10pp of Method1's 0.365 estimate.

### H4: Scrolled Yield
Scrolled yield differs from initial viewport yield by <20pp on >50% of tasks, indicating initial-viewport measurement is representative.

### H5: Site-Type Variation
Gitlab and reddit tasks show yield patterns that differ from shopping by >10pp, indicating site-type-specific denominator requirements.

## 5. Task Selection

### 5.1 Shopping Tasks (8-10 tasks)
Randomly selected from WebArena-Verified dataset covering:
- **Product-listing**: pages showing multiple products (search results, category pages)
- **Detail**: individual product pages with reviews, specifications
- **Cart**: shopping cart pages with item lists
- **Checkout**: checkout flow pages

Task IDs selected from the 192 shopping tasks in WebArena-Verified, ensuring representation across page types.

### 5.2 Site-Type Comparison (2 tasks)
- **Gitlab**: 1 task from webarena-gitlab (code review, issue, or project page)
- **Reddit**: 1 task from webarena-reddit (forum post or comment thread)

## 6. Measurement Protocol

### 6.1 Initial Viewport Measurement
For each task:
1. Launch Playwright browser (Chromium 151.0.7922.34)
2. Navigate to task URL
3. Wait for page load (networkidle)
4. Run geometry-faithful viewport script:
   - Capture CDP accessibility tree
   - Count total CDP nodes (total_cdp_elements)
   - Count locatable elements via Playwright locators (locatable_elements)
   - Count viewport elements via bounding_box intersection with 1280x720 rect (viewport_elements)
5. Save raw accessibility tree as artifact

### 6.2 Scrolled Measurement
For each task (after initial viewport measurement):
1. Scroll to bottom: `page.evaluate('window.scrollTo(0, document.body.scrollHeight)')`
2. Wait 2 seconds for lazy-loaded content
3. Re-run geometry-faithful viewport script on scrolled viewport
4. Save scrolled accessibility tree as artifact

### 6.3 Derived Metrics
For each task:
- **yield_cdp** = viewport_elements / total_cdp_elements (CDP denominator)
- **yield_locatable** = viewport_elements / locatable_elements (locatable denominator)
- **yield_scrolled_cdp** = scrolled_viewport_elements / total_cdp_elements_scrolled
- **yield_scrolled_locatable** = scrolled_viewport_elements / locatable_elements_scrolled
- **scroll_delta_cdp** = yield_scrolled_cdp - yield_cdp
- **scroll_delta_locatable** = yield_scrolled_locatable - yield_locatable

## 7. Baselines

### 7.1 Method1 Estimate
From EXP-INTEL-33945226776: shopping yield 0.365 (element-count method, 150 elements).
Comparison: yield_locatable mean should be within 10pp.

### 7.2 Heuristic Estimate
From EXP-INTEL-33945226776: shopping yield 0.65 (FALSIFIED under both denominators).
Comparison: for reference only, not a validation target.

### 7.3 Parent N=2 Pilot
From EXP-INTEL-34377576886: yield_cdp = 0.0427, yield_locatable = 0.38, 98 viewport elements, 258 locatable.
Comparison: N=8+ should replicate or refute these values.

## 8. Controls

### 8.1 Positive Control
Geometry-faithful viewport script produces non-empty counts on all tasks (viewport_elements > 0, locatable_elements > viewport_elements).

### 8.2 Denominator Mapping Control
Method1's 150-element estimate can be traced to a specific counting method in the derivation code. If the derivation is unavailable or ambiguous, the denominator remains UNKNOWN.

### 8.3 Stability Control
CV of yield_locatable across shopping tasks < 0.2. If CV > 0.2, yield is page-type-dependent and a single denominator does not apply.

## 9. Statistical Tests

### 9.1 Primary: CV of yield_locatable
Coefficient of variation across shopping tasks. Threshold: CV < 0.2 for stability.

### 9.2 Method1 Agreement
Mean absolute deviation of yield_locatable from 0.365. Threshold: < 0.10 (10pp).

### 9.3 Scroll Effect
Paired t-test: yield_locatable vs yield_scrolled_locatable across tasks. Threshold: p > 0.05 (no significant difference) OR mean absolute difference < 0.20.

### 9.4 Site-Type Comparison
Two-sample t-test: shopping yield_locatable vs gitlab/reddit yield_locatable. Exploratory, not decision-critical.

## 10. Validity Threats

### 10.1 Denominator Mapping Uncertainty
Method1 derivation may not clearly specify what was counted. Mitigation: examine code/comments in EXP-INTEL-33945226776; if ambiguous, report as UNKNOWN and recommend code inspection.

### 10.2 Page-Type Sampling
8-10 shopping tasks may not cover all page-type variation. Mitigation: explicitly categorize tasks by page type and report per-type yield.

### 10.3 Scroll Measurement
Lazy-loaded content may not be fully captured by scroll-to-bottom. Mitigation: 2s settle time; report scrolled yield separately.

### 10.4 Docker Container State
Container may have changed since parent experiment. Mitigation: verify container health before measurement; report container status.

### 10.5 Task URL Availability
WebArena-Verified task URLs may be stale or broken. Mitigation: skip failed tasks and report failure count; target N≥8 successful measurements.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Method1 derivation confirms locatable element counting (H1 supported)
2. yield_locatable CV < 0.2 across 8+ shopping tasks (H2 supported)
3. yield_locatable mean within 10pp of 0.365 (H3 supported)
4. Scrolled yield differs < 20pp on > 50% of tasks (H4 supported)
5. No infrastructure failures preventing measurement

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Method1 derivation confirms CDP node counting (denominator ambiguity resolved but against locatable)
2. yield_locatable CV > 0.2 across shopping tasks (unstable yield)
3. yield_locatable mean differs > 10pp from 0.365 (Method1 not validated)
4. Scrolled yield differs > 20pp on > 50% of tasks (initial viewport not representative)

### 11.3 MIXED
If:
1. Locatable yield is stable for some page types but not others
2. Gitlab/reddit show fundamentally different yield patterns
3. Denominator mapping is partially resolved (e.g., Method1 counts "interactive elements" which overlaps both denominators)

### 11.4 BLOCKED
If:
1. Docker container is not running or not accessible
2. Playwright/Chromium fails to launch
3. Geometry-faithful script fails on all tasks
4. WebArena-Verified task URLs are all stale

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Denominator ambiguity resolved: locatable is correct
- Fragment model workable at ~38% yield for shopping
- 812-task corpus suitable for C-CROSSSITE/C-LLM-INHERIT evaluation
- Product lane can proceed to next phase

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Denominator ambiguity resolved but against locatable (CDP is correct)
- Fragment model captures only ~4% of content
- Observation pipeline needs fundamental redesign
- Product lane must explore alternative architectures

### 12.3 Mixed Result (MIXED)
- Denominator varies by page type or site
- No single denominator applies universally
- Product lane needs page-type-specific yield models
- C-CROSSSITE evaluation requires yield-aware task selection

### 12.4 Blocked Result (BLOCKED)
- Infrastructure prevents measurement
- Denominator remains UNKNOWN
- Next experiment must resolve infrastructure first

## 13. Analysis Plan

1. **Denominator Mapping**: Examine Method1 derivation in EXP-INTEL-33945226776
2. **Task Selection**: Randomly select 8-10 shopping tasks + 1 gitlab + 1 reddit from WebArena-Verified
3. **Measurement**: Run geometry-faithful script on each task (initial viewport + scrolled)
4. **Derived Metrics**: Compute yield_cdp, yield_locatable, scroll deltas for each task
5. **Stability Analysis**: CV of yield_locatable across shopping tasks
6. **Method1 Comparison**: Mean absolute deviation from 0.365
7. **Scroll Analysis**: Paired comparison of initial vs scrolled yield
8. **Site-Type Comparison**: Shopping vs gitlab/reddit yield patterns
9. **Reporting**: All outcomes with equal prominence

## 14. Artifacts

- Raw accessibility trees for each task (initial + scrolled)
- Measurement script (geometry-faithful viewport)
- Task selection manifest (task IDs, page types, URLs)
- Derived metrics per task
- Summary statistics across tasks

## 15. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 16. Freeze Statement

This preregistration is frozen BEFORE any measurement code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
