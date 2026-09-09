# EXP-INTEL-34047713704 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-34047713704
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON
- **Date**: 2026-09-07
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-INTEL-33945226776 (MIXED)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Do heuristic fragment yield estimates (0.517-0.65) from EXP-INTEL-33945226776 match actual fragment extraction on live WebArena Docker pages with `current_viewport_only=True`, `clean_accessibility_tree` filtering, and `IGNORED_ACTREE_PROPERTIES` pruning?

## 3. Motivation

### What the parent experiment established (EXP-INTEL-33945226776)

The parent experiment performed heuristic analysis of 812 WebArena tasks across 6 site types without deploying Docker. It found:

**Established (descriptive):**
- WebArena has 6 site types (not 4): gitlab (196 tasks), shopping (192), shopping_admin (182), reddit (114), map (112), wikipedia (16)
- Heuristic median yield estimates: shopping 0.65, reddit 0.65, gitlab 0.60, shopping_admin 0.60, map 0.598, wikipedia 0.517
- Method 1 (element-count, modeling viewport+pruning) gives materially lower yields: shopping 0.365, gitlab 0.484, wikipedia 0.517
- max_obs_length=1920 is the binding constraint, not UTTERANCE_MAX_LENGTH=8192
- Shopping truncation sensitivity ratio: 0.37 (most sensitive); wikipedia: 0.897 (least sensitive)

**Rejected (measurement invalid):**
- All 4 hypotheses (H1-H4) are NOT confirmed: method disagreement (Spearman rho -0.943 to 0.371), Kruskal-Wallis p=0.999
- Aggregated median yield >50% is inflated by degenerate Method 2 (char-length)
- Producer's broader interpretation not justified as evidential

**Unknown:**
- Whether heuristic yield estimates match actual fragment extraction on live WebArena Docker pages
- Whether Method 1 (element-count, shopping 0.365) or aggregated median (0.65) is more predictive of live yield
- Whether the 812-task corpus is suitable for C-CROSSSITE/C-LLM-INHERIT testing

**Do Not Assume:**
- WebArena's 812-task corpus is suitable for C-CROSSSITE or C-LLM-INHERIT (all yield estimates are heuristic priors)
- Aggregated median yield >50% is evidential (Method 2 is degenerate)
- The 224 LOC adapter cost generalizes to live integration
- Synthetic adapter scores predict live performance

### Why this experiment is different

The parent experiment used **heuristic estimation**: domain knowledge of typical web page element counts and source code constants to estimate yields. This approach has fundamental limitations:
1. Estimates are based on analyst priors, not measurements
2. Three estimation methods disagree substantially (rho -0.943 to 0.371)
3. Kruskal-Wallis p=0.999 suggests estimates lack discriminating power

This experiment uses **live Docker deployment**: deploy WebArena's self-hosted websites in Docker, use Playwright to render pages, extract actual accessibility trees, and measure fragment yield through the full REQUIRES_TRANSFORM pipeline.

**Key advantages:**
- Ground-truth measurements from actual rendered pages
- Tests the complete pipeline (viewport filtering + pruning + truncation)
- Resolves whether heuristic estimates are calibrated or misleading
- Directly determines whether the 812-task corpus is worth deploying

**Key limitation:**
- Only 3 tasks tested (1 per site type) — this is a pilot calibration, not a powered statistical test
- Infrastructure may fail (Docker images, Playwright, dependencies)

## 4. Hypotheses

### H1: Heuristic Calibration
Heuristic yield estimates are within 15 percentage points of actual measured yield for all 3 tested site types (shopping, gitlab, wikipedia).

### H2: Positive Control
Shopping task has the highest actual yield among the 3 tested site types, with >40% of DOM elements surviving the full pipeline.

### H3: Null Control
Wikipedia task has the lowest actual yield among the 3 tested site types, with <60% of DOM elements surviving.

### H4: Truncation Sensitivity
max_obs_length=1920 is the binding truncation constraint for shopping (sensitivity ratio <0.5), confirming the parent experiment's finding.

## 5. Infrastructure Setup

### 5.1 Docker Deployment

Deploy WebArena websites using Docker Compose:
- **Shopping**: `ghcr.io/web-arena-x/webarena-shopping:latest` (e-commerce site)
- **Gitlab**: `ghcr.io/web-arena-x/webarena-gitlab:latest` (code hosting)
- **Wikipedia**: `ghcr.io/web-arena-x/webarena-wikipedia-like:latest` (CMS)

Each container runs a self-hosted website with pre-populated data.

### 5.2 Playwright Setup

Install Playwright for headless browser automation:
```bash
pip install playwright
playwright install chromium
```

### 5.3 WebArena Package

Install WebArena's observation extraction code:
```bash
git clone https://github.com/web-arena-x/webarena.git /tmp/webarena
cd /tmp/webarena && pip install -e .
```

### 5.4 Task Selection

Select 1 task per site type from WebArena's task definitions:
- **Shopping**: A product search/listing task (high element density)
- **Gitlab**: A project/code viewing task (moderate element density)
- **Wikipedia**: An article reading task (low element density, negative control)

Task definitions are taken from WebArena's `test.raw.json` file at base_sha 8bc5034.

## 6. Measurement Procedure

### 6.1 Page Rendering

For each selected task:
1. Start the corresponding Docker container
2. Navigate Playwright to the task's starting URL
3. Wait for page load (networkidle)
4. Capture the full accessibility tree using Playwright's `page.accessibility.snapshot()`

### 6.2 Accessibility Tree Extraction

From the rendered page:
1. Extract the raw accessibility tree (all elements, not viewport-filtered)
2. Extract the viewport-filtered tree (`current_viewport_only=True`, viewport 1280x720)
3. Apply `IGNORED_ACTREE_PROPERTIES` pruning (remove focusable, editable, readonly, level, settable, multiline, invalid properties)
4. Format as WebArena's observation string: `[id] role "name" prop1: val1 prop2: val2`

### 6.3 Fragment Yield Measurement

For each task, compute:
- **total_elements**: total elements in raw accessibility tree
- **viewport_elements**: elements within viewport (1280x720)
- **pruned_elements**: elements surviving IGNORED_ACTREE_PROPERTIES pruning
- **truncated_8192**: elements within UTTERANCE_MAX_LENGTH=8192 chars
- **truncated_1920**: elements within max_obs_length=1920 chars
- **actual_yield**: elements surviving full pipeline / total elements

### 6.4 Comparison Metrics

For each task:
- **yield_delta**: |actual_yield - heuristic_yield|
- **yield_ratio**: actual_yield / heuristic_yield
- **truncation_sensitivity**: truncated_1920 / truncated_8192
- **element_diversity**: unique roles in extracted observation

## 7. Decision Rules

### 7.1 SUPPORTS
If ALL of:
1. yield_delta < 0.15 for shopping
2. yield_delta < 0.15 for gitlab
3. yield_delta < 0.15 for wikipedia
4. Shopping has highest actual yield
5. Wikipedia has lowest actual yield
6. No infrastructure failures

### 7.2 FALSIFIES
If ANY of:
1. yield_delta > 0.15 for any site type
2. Shopping does NOT have highest actual yield (violates positive control)
3. Wikipedia does NOT have lowest actual yield (violates null control)

### 7.3 BLOCKED
If:
1. Docker images cannot be pulled (network/disk failure)
2. Playwright cannot be installed or run
3. WebArena environment fails to start for all 3 tasks
4. Accessibility tree extraction fails for all 3 tasks

## 8. Validity Threats

### 8.1 Small Sample Size
Only 3 tasks tested (1 per site type). This is a pilot calibration, not a powered test. Results may not generalize to the full 812-task corpus. **Mitigation**: report exact measurements and confidence intervals; design follow-up experiment with more tasks if SUPPORTS.

### 8.2 Task Selection Bias
Selected tasks may not be representative of their site type. A product listing page may have different yield than a product detail page. **Mitigation**: select tasks with typical intent descriptions (not edge cases); report which specific task was tested.

### 8.3 Infrastructure Failure
Docker deployment may fail due to network, disk, or dependency constraints. This is NOT a scientific falsification. **Mitigation**: distinguish BLOCKED (infrastructure) from FALSIFIES (scientific). If BLOCKED, document exact failure and smallest next action.

### 8.4 Playwright vs WebArena Rendering
Playwright's accessibility tree extraction may differ from WebArena's internal extraction (which uses a custom browser). **Mitigation**: use WebArena's own observation extraction code where possible; document any differences.

### 8.5 Single Observation Per Task
Each task produces one observation (initial page load). Real agent interaction produces multiple observations across page navigations. **Mitigation**: this experiment measures initial page complexity, not full task trajectory. Follow-up can measure multi-step yield.

## 9. Expected Outcomes

### 9.1 SUPPORTS
- Heuristic estimates are calibrated within 15pp
- The 812-task corpus is suitable for C-CROSSSITE/C-LLM-INHERIT testing
- Graph lane can proceed with Docker integration
- Intel provides the task-type ranking grounded in live measurements

### 9.2 FALSIFIES
- Heuristic estimates are not calibrated
- The 812-task corpus yield is unknown
- Intel should reassess VisualWebArena, Mind2Web, or other benchmarks
- Graph lane should not deploy Docker on unvalidated corpus

### 9.3 BLOCKED
- Infrastructure barriers prevent live measurement
- Smallest next action: resolve specific Docker/Playwright/dependency failure
- Does NOT inform scientific question; informs infrastructure investment

## 10. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 11. Freeze Statement

This preregistration is frozen BEFORE any Docker deployment, Playwright installation, or outcome data is collected. The experiment will be executed exactly as described here.
