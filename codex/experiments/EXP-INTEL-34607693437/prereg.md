# EXP-INTEL-34607693437 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-34607693437
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT
- **Parent Experiment**: EXP-INTEL-34546944360 (verdict: MIXED, audit: REVISE)
- **Date**: 2026-09-11
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

What is the canonical definition of "locatable elements" for SPIDER fragment yield, and does yield_locatable stabilize across randomized shopping page types (including checkout) under that frozen definition?

## 3. Motivation

### 3.1 The Blocking Problem

The 812-task WebArena-Verified corpus is the proposed testbed for C-CROSSSITE (cross-site transfer) and C-LLM-INHERIT (LLM agent inheritance). Interpreting this corpus requires knowing the **fragment yield**: what fraction of page elements does the SPIDER fragment model capture?

The denominator for yield calculation is ambiguous:
- **Definition 1** (all elements with bounding box): yield_locatable ≈ 0.079 (1354 elements)
- **Definition 2** (interactive elements only): yield_locatable ≈ 0.32 (~336 elements)
- **Definition 3** (parent CSS selectors): yield_locatable ≈ 0.42 (258 elements)

This 5× range means the denominator choice determines whether the fragment model captures 8% (nearly useless) or 42% (workable) of page elements. The choice also determines whether Method1's 0.365 estimate is SUPPORTED (within 5pp under Definition 3) or FALSIFIED (28.6pp under Definition 1).

### 3.2 Why This Experiment Is Highest-Information

The parent experiment (EXP-INTEL-34546944360) confirmed:
- CDP yield 0.0426 is stable and replicable (CV=0.12 across 20 tasks)
- Heuristic 0.65 is falsified robustly (>23pp under any denominator)
- **The denominator ambiguity IS the result**, not a detail

The audit's primary required fix: "Define canonical locatable_elements before any yield claim."

Until the definition is frozen, no yield claim can be made, and the 812-task corpus viability is UNKNOWN. This experiment resolves that blocking question.

### 3.3 Forensic Approach

The parent experiment discovered that Method1's 150-element estimate was derived from analysis_output.json but the derivation did not specify what constitutes an "element." The most discriminating next step is to **trace the derivation code** to determine what Method1 actually counted, then freeze that definition.

This is a forensic analysis, not a measurement. It resolves the definitional question before any yield measurement occurs.

## 4. Hypotheses

### H1: Definition Resolution (Forensic)
Method1's 150-element shopping estimate can be traced to a specific element-counting method in the derivation code (analysis_output.json from EXP-INTEL-33945226776). The traced method maps to one of the three candidate definitions:
- (a) All elements with non-null bounding box (Definition 1)
- (b) Interactive elements only — links, buttons, inputs, form controls (Definition 2)
- (c) Parent CSS selector enumeration (Definition 3)

**Falsification**: The forensic analysis cannot trace the 150-element estimate to a specific counting method. All three definitions remain equally plausible after code inspection.

### H2: Yield Stability Under Frozen Definition
Under the canonical definition frozen by H1 (or the functional fallback if H1 is inconclusive), yield_locatable = viewport_elements / locatable_elements has CV < 0.2 across 8+ randomized shopping tasks covering product-listing, detail, cart, and checkout.

**Falsification**: CV > 0.2 across shopping tasks, indicating yield depends on page type rather than being a stable property of the fragment model.

### H3: Method1 Compatibility (only if definition resolved)
Under the frozen canonical definition (if forensic resolves it), yield_locatable mean is within 15pp of Method1's 0.365 estimate.

**Falsification**: Mean yield_locatable differs from Method1 by >15pp, indicating the frozen definition does not match what Method1 modeled.

### H4: Checkout Yield
Checkout page yield_locatable under the frozen definition is within 20pp of the mean yield across other page types (product-listing, detail, cart).

**Falsification**: Checkout yield differs from other page types by >20pp on >50% of checkout tasks, indicating checkout has structurally different element composition.

### H5: Site-Type Comparison (Exploratory)
If Docker images for GitLab and Reddit are available, yield_locatable under the frozen definition is within 2× of the shopping mean on at least one GitLab and one Reddit task.

**BLOCKED status**: If Docker images are unavailable, mark BLOCKED with infrastructure proof. This hypothesis is exploratory — the primary experiment resolves the denominator for shopping; site-type generalization is a follow-up.

### H6: Viewport Anomaly Resolution
Per-task viewport element counts vary across page types (stdev > 0 across 8+ tasks), OR the constant-108 pattern is explained as fixed chrome/navigation with evidence (e.g., all 108 elements are header/navrole types).

**Falsification**: Viewport elements remain exactly 108 across all page types including checkout with no explanation — measurement captures only fixed chrome, not page content.

## 5. Forensic Analysis Plan

### 5.1 Source Materials
- Method1 derivation code: `analysis_output.json` from EXP-INTEL-33945226776
- Method1 measurement script (if available in /tmp or research artifacts)
- Parent pilot scripts: `measure_yield_geo_v2.py` (sha256: 15a2ad056dea51a4e907ceece1d176007122f3b9dec415ea87234061167f1d4e)
- Parent experiment scripts: `measure_yield_exp345_final.py`

### 5.2 Analysis Steps
1. Load analysis_output.json and locate the 150-element estimate for product_listing
2. Trace the derivation backward: what function computed this value? What inputs did it use?
3. Identify the element-counting method: what selector/filter was applied to the accessibility tree?
4. Map the counted elements to one of the three candidate definitions
5. If the mapping is ambiguous, document why and proceed to the fallback definition

### 5.3 Fallback Definition
If the forensic analysis is inconclusive (cannot trace 150 to a specific method), freeze the **functional definition**:
- Elements with non-null bounding box (width > 0 AND height > 0)
- AND role is one of: button, link, textbox, checkbox, radio, combobox, listbox, menuitem, tab, slider, spinbutton, searchbox, switch
- OR has an onclick/onsubmit handler or is within a form element
- OR has aria-label or aria-describedby with non-empty text

This captures "interactive elements that an agent can use for inheritance" — the functional purpose of the SPIDER fragment model. This is equivalent to Definition 2 (interactive-only), which gave yield ≈ 0.32 in the parent experiment.

### 5.4 Definition Freeze Record
The frozen definition will be recorded in the experiment's metrics with:
- Definition text (exact selector/filter logic)
- Source (forensic trace or fallback rationale)
- Mapping to candidate definitions (which of the three it corresponds to)
- Expected yield range (from parent experiment data)

## 6. Measurement Plan

### 6.1 Task Selection

**Shopping tasks**: 8 tasks randomized from WebArena-Verified dataset:
- 2 product-listing pages
- 2 product-detail pages
- 2 cart pages
- 2 checkout pages

Randomization: Use Python `random.Random(seed=FROZEN_SEED).choices()` to select task URLs from the WebArena-Verified dataset, stratified by page type. Record task IDs and placeholder substitutions.

**Site-type comparison** (exploratory):
- 1 GitLab task from am1n3e/webarena-verified-gitlab (if Docker image available)
- 1 Reddit task from am1n3e/webarena-verified-reddit (if Docker image available)
- If unavailable: mark BLOCKED with infrastructure proof (Docker pull failure logs)

### 6.2 Measurement Protocol

For each task:
1. **Docker setup**: Pull and start the target container. Record image digest (sha256) before measurement.
2. **Browser context**: Create fresh Playwright browser context (no shared cookies/session).
3. **Navigation**: Navigate to the task URL. Wait for networkidle.
4. **Initial viewport measurement**:
   - Capture viewport dimensions (1280×720)
   - Run frozen definition script to count:
     - `viewport_elements`: elements with bbox intersection with viewport rect (threshold 0.5)
     - `locatable_elements`: elements matching frozen canonical definition
     - `total_cdp_elements`: full CDP accessibility tree node count
   - Save per-task viewport element sample (first 20 element roles/types) for anomaly investigation
5. **Raw artifact**: Save full accessibility tree as JSON with sha256.
6. **Cleanup**: Close browser context and Docker container.

### 6.3 Yield Calculation

For each task:
- `yield_cdp` = viewport_elements / total_cdp_elements
- `yield_locatable` = viewport_elements / locatable_elements (under frozen definition)
- `method1_delta_cdp` = |yield_cdp - 0.0426| (parent CDP yield)
- `method1_delta_locatable` = |yield_locatable - 0.365| (Method1 estimate)

### 6.4 Viewport Anomaly Investigation

For each task, save:
- Per-task viewport_elements count (not just aggregate)
- Per-task locatable_elements count
- Per-task element type distribution (what roles are in the viewport)
- Compare across page types to determine if 108 is fixed chrome or page-specific

## 7. Controls

### 7.1 Positive Control
- Non-empty viewport_elements (>0) on all tasks
- Non-empty locatable_elements (>viewport_elements) on all tasks
- Forensic analysis produces either a traceable method or a documented inconclusiveness record

### 7.2 Stability Control
- CV of yield_locatable across all measured shopping tasks < 0.2

### 7.3 Method1 Compatibility Control (only if definition resolved)
- Mean yield_locatable within 15pp of Method1 0.365 under frozen definition

### 7.4 Checkout Coverage Control
- At least 2 checkout tasks measured
- Checkout yield within 20pp of other page types

### 7.5 Null Control (Definition Ambiguity)
- If forensic analysis is inconclusive AND fallback yield also has CV>0.2, report MIXED with definition_ambiguous
- This is a valid negative outcome, not an infrastructure failure

## 8. Statistical Analysis

### 8.1 Primary Metrics
- `yield_locatable_mean`: mean yield across all shopping tasks
- `yield_locatable_cv`: coefficient of variation across shopping tasks
- `method1_delta_pp`: absolute difference from Method1 0.365 in percentage points
- `definition_resolved`: boolean (forensic analysis succeeded or not)
- `fallback_frozen`: boolean (if forensic inconclusive, was fallback frozen)

### 8.2 Secondary Metrics
- `yield_cdp_mean`, `yield_cdp_cv`: CDP yield for cross-denominator comparison
- `viewport_elements_per_task`: per-task counts for anomaly investigation
- `page_type_yields`: yield by page type (product-listing, detail, cart, checkout)
- `gitlab_reddit_yields`: yield on site-type comparison tasks (if measured)

### 8.3 No Formal Hypothesis Testing
This experiment is a measurement and definition-freeze exercise, not a confirmatory hypothesis test. The decision rule is threshold-based (CV < 0.2, delta < 15pp), not p-value-based. Effect sizes and confidence intervals are reported but not used for binary decisions.

## 9. Validity Threats

### 9.1 Forensic Ambiguity
Method1's derivation may be genuinely ambiguous — the 150-element estimate may not map cleanly to any of the three candidate definitions. Mitigation: use the functional fallback definition and document the ambiguity. This is a valid outcome, not a failure.

### 9.2 Docker Drift
Different image digests may have different page structures. The parent experiment showed CDP yield is stable across digests (0.0426 vs 0.0427), but locatable counts shifted (258 vs 1392). Mitigation: record image digest before measurement and compare to parent.

### 9.3 Viewport Constancy Anomaly
The constant 108 viewport elements across page types suggests a fixed header/chrome artifact or a measurement bug. If this persists, yield calculation may be measuring chrome, not page content. Mitigation: per-task viewport sample to investigate; H6 explicitly tests this.

### 9.4 Sample Size
8 shopping tasks may be insufficient for stable CV estimation. The parent used 10 tasks and found CV=0.16. With 8 tasks, CV estimates have wider confidence intervals. Mitigation: report CV with confidence interval; the threshold (0.2) is conservative.

### 9.5 Non-Random Sampling
Tasks are randomized from the dataset but the dataset itself may not represent all shopping pages. Mitigation: this is a known limitation; the experiment bounds yield for the 812-task corpus specifically, not all shopping pages universally.

### 9.6 Checkout Page Availability
Checkout pages may require authentication or specific cart state. If checkout tasks cannot be loaded, mark BLOCKED for checkout coverage and note as validity threat.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Forensic analysis traces Method1 150-element estimate to a specific counting method (definition_resolved=true) OR forensic is inconclusive but functional fallback is frozen (fallback_frozen=true)
2. yield_locatable CV < 0.2 across all measured shopping tasks (yield stable)
3. If definition_resolved=true: yield_locatable mean within 15pp of Method1 0.365 (method compatible)
4. At least 2 checkout tasks measured with yield within 20pp of other page types
5. Per-task viewport sample saved (H6 investigated)
6. No pipeline errors

**Consequence**: Denominator resolved (forensic or fallback). 812-task corpus viability assessed. Product lane can proceed to integration experiments using frozen definition.

### 10.2 FALSIFIED-IN-SETTING
If ANY of:
1. Forensic resolves definition BUT yield_locatable CV > 0.2 (yield unstable)
2. Forensic resolves definition BUT yield_locatable mean differs from Method1 by >15pp (method mismatch)
3. Positive control fails (empty counts on any task)
4. Viewport anomaly persists (constant 108) with no explanation AND yield under frozen definition is not page-specific

**Consequence**: Definition resolved but yield not workable. Product lane must redesign observation pipeline or use CDP yield (4%) as conservative floor.

### 10.3 MIXED
If:
1. Forensic analysis is inconclusive (definition_ambiguous) AND fallback yield also has CV>0.2
2. OR checkout tasks BLOCKED due to infrastructure
3. OR gitlab/reddit BLOCKED due to infrastructure

**Consequence**: Definition ambiguous by construction. 812-task corpus cannot be reliably used for yield claims. Product lane must either redesign or accept ambiguity.

### 10.4 MEASUREMENT_INVALID
If:
1. Docker container cannot be started
2. Playwright cannot load pages
3. Script errors prevent measurement
4. Sample size insufficient (<5 tasks measured)

## 11. Expected Outcomes

### 11.1 Positive Result (SURVIVES_CURRENT_TEST)
- Canonical definition frozen and validated
- 812-task corpus viability confirmed
- Product lane proceeds to C-CROSSSITE/C-LLM-INHERIT integration
- Future experiments use frozen definition consistently

### 11.2 Negative Result (FALSIFIED-IN-SETTING)
- Definition resolved but yield not workable
- Product lane must redesign observation pipeline
- Alternative: use CDP yield (4%) as conservative lower bound

### 11.3 Ambiguous Result (MIXED)
- Definition cannot be resolved from code
- Denominator ambiguity is structural, not solvable
- Product lane must accept ambiguity or redesign

## 12. Artifacts

### 12.1 Required Artifacts
- `frozen_definition.json`: Canonical definition text, source, mapping to candidate definitions
- `measure_yield_exp346.py`: Frozen measurement script with sha256
- `exp346_raw_results.json`: Per-task measurements with all yields under all definitions
- `raw_ax_tree_<task>_initial.json`: Raw accessibility tree per task with sha256
- `viewport_sample_<task>.json`: Per-task viewport element sample for anomaly investigation

### 12.2 Forensic Artifacts
- `method1_trace.json`: Forensic analysis trace showing derivation of 150-element estimate
- `definition_analysis.json`: Comparison of traced method to three candidate definitions

## 13. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 14. Freeze Statement

This preregistration is frozen BEFORE any forensic analysis is conducted or any outcome data is inspected. The experiment will be executed exactly as described here. The forensic analysis (Section 5) is a pre-measurement definitional exercise, not an outcome-bearing measurement.
