# EXP-INTEL-34047713704 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-34047713704
- **Lane**: Intel
- **Claims**: C-CROSSSITE (Reusable mechanisms transfer across website holdout), C-LLM-INHERIT (A real LLM agent benefits from SPIDER beyond strong memory/instruction baselines)
- **Date**: 2026-09-06
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Do heuristic fragment yield estimates from EXP-INTEL-33945226776 match actual DOM extraction on live WebArena Docker pages, and is Method 1 (element-count) or aggregated median more predictive of live yield?

## 3. Motivation

Prior Intel work (EXP-INTEL-33945226776) performed heuristic analysis of 812 WebArena tasks across 6 site types, finding:

- Aggregated median yield >50% for all 6 site types (0.517-0.65)
- Method disagreement (Spearman rho -0.943 to 0.371) and Kruskal-Wallis p=0.999 — estimates are non-discriminating priors
- Method 1 (element-count, the only method modeling viewport+pruning) gives materially lower yields: shopping 0.365, gitlab 0.484, wikipedia 0.517
- Method 2 (char-length at UTTERANCE_MAX_LENGTH=8192) is degenerate: yields 1.0 for 5/6 site types, inflating aggregated medians
- max_obs_length=1920 (LLM input limit) is the binding constraint, not UTTERANCE_MAX_LENGTH=8192
- Null control failed (wikipedia 0.517 > 0.40 threshold)
- Auditor ceiling bounds this to "heuristic exploratory triage only"

The central unresolved question is whether these heuristic estimates match actual fragment extraction on live WebArena Docker pages. This experiment deploys WebArena Docker for 3 tasks (one shopping, one gitlab, one wikipedia) to measure actual fragment yield, truncation at 8192/1920, viewport filtering, and IGNORED_ACTREE_PROPERTIES pruning on live DOM.

This resolves whether:
1. The 812-task corpus is suitable for C-CROSSSITE and C-LLM-INHERIT integration
2. Method 1 (element-count, shopping 0.365) or aggregated median (0.65) is more predictive of live yield
3. The 324 LOC REQUIRES_TRANSFORM implementation is justified
4. Intel should assess VisualWebArena/Mind2Web as alternatives

## 4. Hypotheses

### H1: Method 1 Calibration
Live fragment yield will be within +/-0.10 of Method 1 (element-count) estimates for at least 2 of 3 tested site types (shopping M1=0.365, gitlab M1=0.484, wikipedia M1=0.517).

### H2: Shopping Positive Control
Shopping task will have highest actual fragment yield due to structured product data with interactive elements. Expected: actual yield >0.30 (based on M1 estimate 0.365 with live DOM typically having more elements than heuristic estimates). Shopping yield must exceed wikipedia yield.

### H3: Wikipedia Negative Control
Wikipedia task will have lowest actual fragment yield among the three site types. Expected: actual yield <0.60 (based on all heuristic estimates 0.517-1.0). Wikipedia yield must be less than both shopping and gitlab yields.

### H4: Truncation Sensitivity
max_obs_length=1920 will be the binding constraint for shopping and gitlab (sensitivity ratio <0.7), matching heuristic estimates (shopping 0.37, gitlab 0.471).

## 5. Task Selection

Following parent handoff recommendation (EXP-INTEL-33945226776/handoff.json):

### 5.1 Shopping Task
- **Site type**: shopping (consumer-facing e-commerce)
- **Page type**: product listing page with interactive elements (buttons, textboxes, links)
- **Rationale**: Highest heuristic element diversity (21 unique types), positive control for C-CROSSSITE
- **Selection criteria**: Task must involve product browsing/search, not account management

### 5.2 Gitlab Task
- **Site type**: gitlab (self-hosted code repository)
- **Page type**: project/repository view with file tree, actions, search
- **Rationale**: High heuristic element diversity (21 unique types), tests code-focused interaction patterns
- **Selection criteria**: Task must involve repository navigation, not CI/CD configuration

### 5.3 Wikipedia Task (Negative Control)
- **Site type**: wikipedia (CMS, minimal interactive elements)
- **Page type**: article page with navigation, content, minimal interactivity
- **Rationale**: Lowest heuristic yield (0.517), only 16 tasks in corpus, tests CMS complexity bound
- **Selection criteria**: Task must involve article reading/navigation, not editing

## 6. Measurement Protocol

### 6.1 Docker Deployment
1. Clone WebArena repository at base_sha 8bc5034
2. Build Docker images for shopping, gitlab, wikipedia sites
3. Start container instances for each site type
4. Verify containers are healthy and accessible

### 6.2 Task Execution
1. For each selected task:
   a. Initialize WebArena environment with task definition
   b. Navigate to initial URL
   c. Extract observation using WebArena's observation interface:
      - obs["text"]: formatted indented string with element IDs, roles, names, properties
      - obs_nodes_info: dict mapping element ID to {backend_id, union_bound, text}
   d. Record raw observation and metadata
   e. Terminate environment

### 6.3 Fragment Extraction Pipeline
For each raw observation:
1. Parse accessibility tree using research/intel/webarena_adapter.py
2. Count total elements (N_total)
3. Apply viewport filtering (current_viewport_only=True):
   - Filter elements by IN_VIEWPORT_RATIO_THRESHOLD=0.6
   - Count viewport elements (N_viewport)
4. Apply IGNORED_ACTREE_PROPERTIES pruning:
   - Remove properties: focusable, editable, readonly, level, settable, multiline, invalid
   - Count pruned properties per element
5. Compute formatted observation string length (L_formatted)
6. Apply truncation at UTTERANCE_MAX_LENGTH=8192:
   - Count elements surviving truncation (N_8192)
7. Apply truncation at max_obs_length=1920:
   - Count elements surviving truncation (N_1920)

### 6.4 Yield Computation
For each truncation level:
- yield_8192 = N_8192 / N_total
- yield_1920 = N_1920 / N_total
- sensitivity_ratio = yield_1920 / yield_8192

Viewport filtering yield:
- viewport_yield = N_viewport / N_total

## 7. Metrics

### 7.1 Primary Metrics
- **actual_yield_by_site_type**: {shopping: float, gitlab: float, wikipedia: float} at max_obs_length=1920
- **method1_vs_actual_deviation**: |method1_estimate - actual_yield| for each site type
- **truncation_sensitivity_ratio**: yield_1920 / yield_8192 for each site type

### 7.2 Secondary Metrics
- **total_elements_by_site_type**: N_total for each task
- **formatted_string_length**: L_formatted for each observation
- **viewport_filtering_effect**: 1 - viewport_yield for each site type
- **property_pruning_effect**: average properties pruned per element
- **aggregated_median_vs_actual_deviation**: |aggregated_median - actual_yield| for each site type

### 7.3 Derived Metrics
- **yield_ranking_agreement**: Does actual yield ranking match M1 ranking (wikipedia > gitlab > shopping)?
- **method1_predictive_power**: Absolute deviation of M1 from actual yield, averaged across site types
- **corpus_suitability_score**: Fraction of tested site types with actual yield >0.30

## 8. Controls

### 8.1 Positive Control (Shopping)
- **Expected**: actual yield >0.30 (based on M1 estimate 0.365 with live DOM typically having more elements)
- **Pass condition**: shopping yield >0.30 AND shopping yield > wikipedia yield
- **Fail condition**: shopping yield <0.25 OR shopping yield < wikipedia yield

### 8.2 Negative Control (Wikipedia)
- **Expected**: actual yield <0.60 (based on all heuristic estimates 0.517-1.0)
- **Pass condition**: wikipedia yield <0.60 AND wikipedia yield < shopping yield AND wikipedia yield < gitlab yield
- **Fail condition**: wikipedia yield >0.60 OR wikipedia yield > shopping yield

### 8.3 Truncation Sensitivity Control
- **Expected**: sensitivity_ratio <0.7 for shopping and gitlab (matching heuristic estimates shopping 0.37, gitlab 0.471)
- **Pass condition**: shopping sensitivity_ratio <0.7 AND gitlab sensitivity_ratio <0.7
- **Fail condition**: shopping sensitivity_ratio >0.8 OR gitlab sensitivity_ratio >0.8

### 8.4 Adapter Functionality Control
- **Expected**: webarena_adapter.py parses all observations without errors
- **Pass condition**: all 3 observations parsed, no parsing errors
- **Fail condition**: parsing errors on any observation

## 9. Decision Rules

### 9.1 SUPPORTS
If ALL of:
1. Docker deployment succeeds for all 3 tasks
2. heuristic_vs_actual_deviation <=0.10 for >=2 site types (using M1 estimates)
3. Shopping yield >0.30
4. Gitlab yield >0.30
5. Wikipedia yield < shopping yield
6. Wikipedia yield < gitlab yield

Then: C-CROSSSITE and C-LLM-INHERIT move toward EXPERIMENTAL with caveat that 3-task sample is small. Product lane can proceed with REQUIRES_TRANSFORM implementation.

### 9.2 FALSIFIES
If ANY of:
1. Shopping yield <0.25 OR gitlab yield <0.35
2. Wikipedia yield > shopping yield OR Wikipedia yield > gitlab yield
3. heuristic_vs_actual_deviation >0.15 for >=2 site types (using M1 estimates)

Then: 2-site corpus remains practical bound. Intel should assess VisualWebArena/Mind2Web as alternatives.

### 9.3 MIXED
If NOT SUPPORTS AND NOT FALSIFIES:
- Shopping or gitlab yield between 0.25-0.30
- OR heuristic_vs_actual_deviation between 0.10-0.15 for >=1 site type
- OR truncation sensitivity inconsistent with estimates

Then: Inconclusive. Need larger task sample (5-10 tasks per site type).

### 9.4 MEASUREMENT_INVALID
If:
1. Docker deployment fails for >=1 task
2. Accessibility tree parsing fails for >=1 observation
3. Observation text is empty for >=1 task
4. WebArena environment produces invalid observations (e.g., screenshot-only without DOM)

## 10. Validity Threats

### 10.1 Sample Size
With only 3 tasks (1 per site type), estimates have high sampling error. A single task may not be representative of its site type. Mitigation: report confidence intervals and acknowledge small sample in verdict. The experiment is designed as a proof-of-concept for Docker deployment feasibility and heuristic calibration, not a comprehensive yield survey.

### 10.2 Task Selection Bias
Selected tasks may not be representative of their site types. Mitigation: select tasks following parent recommendation criteria (product listing for shopping, project view for gitlab, article for wikipedia). Document exact task URLs and characteristics.

### 10.3 Docker vs Production Environment
WebArena Docker environment may differ from production websites in DOM structure, JavaScript rendering, and element counts. Mitigation: acknowledge Docker-specific findings. If Docker yield is substantially different from heuristic estimates, this itself is informative about Docker-based benchmark validity.

### 10.4 Accessibility Tree Completeness
WebArena's accessibility tree may not capture all DOM elements (e.g., elements hidden from assistive technology). Mitigation: compare accessibility_tree mode vs html mode if both are available. Acknowledge representation loss in validity_notes.

### 10.5 Viewport Dependency
Viewport filtering depends on viewport size and scroll position. WebArena uses fixed viewport dimensions. Mitigation: measure with current_viewport_only=True (default) and=False to bound viewport effect. Report both yields.

### 10.6 Heuristic Estimate Uncertainty
Heuristic estimates from EXP-INTEL-33945226776 have known weaknesses: Method 2 is degenerate, Method 1 uses assumed viewport coverage and pruning fractions, Kruskal-Wallis p=0.999 shows no discrimination. Mitigation: use M1 as primary calibration target (most conservative), also report deviation from aggregated median for comparison.

## 11. Analysis Plan

1. **Docker Setup**: Deploy WebArena Docker for shopping, gitlab, wikipedia sites at base_sha 8bc5034
2. **Task Execution**: Run 3 tasks, extract raw observations (obs["text"] + obs_nodes_info)
3. **Parsing**: Parse accessibility trees using webarena_adapter.py, verify no errors
4. **Element Counting**: Count total elements, viewport elements, pruned elements per observation
5. **Truncation Measurement**: Compute formatted string length, measure yield at 8192 and 1920
6. **Yield Computation**: Compute actual_yield, viewport_yield, sensitivity_ratio per site type
7. **Heuristic Comparison**: Compare actual yield to M1 estimates (primary) and aggregated median (secondary)
8. **Control Checks**: Verify positive control (shopping >0.30), negative control (wikipedia <0.60), truncation sensitivity (<0.7), adapter functionality (no errors)
9. **Decision**: Apply frozen decision rule (SUPPORTS/FALSIFIES/MIXED/MEASUREMENT_INVALID)
10. **Reporting**: Report all metrics, controls, deviations, and validity threats

## 12. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

Deviations that require labeling:
- Changing task selection criteria
- Modifying truncation thresholds (8192/1920)
- Changing viewport filtering parameters
- Adding or removing site types
- Modifying yield computation formula
- Changing decision rule thresholds

## 13. Freeze Statement

This preregistration is frozen BEFORE any Docker deployment, task execution, or outcome data inspection. The experiment will be executed exactly as described here.
