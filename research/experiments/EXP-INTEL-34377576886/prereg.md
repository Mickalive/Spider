# EXP-INTEL-34377576886 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-34377576886
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON
- **Date**: 2026-09-09
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-INTEL-34047713704 (BLOCKED on Docker auth)

## 2. Scientific Question

Can ghcr.io Docker authentication be obtained and actual fragment yield measured on live WebArena pages, resolving whether heuristic yield estimates (0.517-0.65) match geometry-faithful viewport-filtered extraction?

## 3. Motivation

Three prior Intel experiments have established:

1. **EXP-INTEL-33945226776**: Heuristic yield estimates computed for 812-task WebArena corpus across 6 site types. Aggregated medians: shopping 0.65, reddit 0.65, gitlab 0.60, shopping_admin 0.60, map 0.598, wikipedia 0.517. Method 1 (element-count) gives materially lower yields for some types. Central question: are these calibrated?

2. **EXP-INTEL-33925056324**: SUPPORTS verdict for C-CROSSSITE and C-LLM-INHERIT at exploratory ceiling. Heuristic triage established WebArena as candidate corpus.

3. **EXP-INTEL-34047713704**: BLOCKED. Docker images from ghcr.io/web-arena-x/ denied without authentication. Playwright + Chromium work. Measurement script prepared but contains viewport filtering heuristic (depth<=4, role-in-viewport_roles) that diverges from spec requirement (geometry-faithful union_bound). Central question remains unanswered.

The parent handoff (EXP-INTEL-34047713704) explicitly carries forward:
- **established**: WebArena 6 site types, 812 tasks; heuristic yields are unvalidated priors; Docker requires auth; Playwright works; measurement script exists with viewport heuristic
- **rejected**: Nothing scientific (BLOCKED ≠ falsified)
- **unknown**: Whether heuristic estimates match actual yield; whether corpus is suitable; whether viewport heuristic approximates geometry
- **do_not_assume**: Heuristic estimates are calibrated; corpus is suitable; Method 2 yields are valid

This experiment directly addresses the parent's next_question: obtain Docker auth, fix viewport filtering, measure actual yield on 2-3 tasks.

## 4. Hypotheses

### H1: Docker Authentication
Docker authentication to ghcr.io/web-arena-x/ can be obtained using GITHUB_TOKEN with read:packages scope or PAT with docker login. If auth succeeds, at least 1 of 3 WebArena Docker images (shopping, gitlab, wikipedia-like) can be pulled successfully.

### H2: Heuristic Calibration
If Docker authentication succeeds, actual measured yield (with geometry-faithful viewport filtering) is within 15 percentage points of the heuristic estimate for at least 2 of 3 tested site types.

### H3: Positive Control
Shopping task (e-commerce) has the highest actual yield among the 3 tested site types, with >40% of DOM elements surviving the full REQUIRES_TRANSFORM pipeline.

### H4: Null Control
Wikipedia task (CMS) has the lowest actual yield among the 3 tested site types, with <60% of DOM elements surviving.

## 5. Infrastructure Verification

### 5.1 Docker Authentication (Step 1)
Before any measurement, verify Docker authentication:
1. Check if GITHUB_TOKEN environment variable is set
2. Attempt `echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin`
3. If GITHUB_TOKEN fails, attempt alternative PAT or anonymous access
4. Record exact auth method and error messages
5. If auth fails for all methods, proceed to BLOCKED branch

### 5.2 Docker Image Pull (Step 2)
For each site type, attempt:
1. `docker pull ghcr.io/web-arena-x/webarena-shopping:latest`
2. `docker pull ghcr.io/web-arena-x/webarena-gitlab:latest`
3. `docker pull ghcr.io/web-arena-x/webarena-wikipedia-like:latest`
4. If latest fails, try tags: v1, v2, stable
5. Record pull status, image sizes, errors

### 5.3 Playwright Verification (Step 3)
Verify Playwright + Chromium installation (confirmed working in parent):
1. `python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(headless=True); b.close(); p.stop()"`
2. Record Playwright version, Chromium version

## 6. Measurement Pipeline

### 6.1 Task Selection
Select 3 tasks (one per site type):
- **Shopping**: First available shopping task from WebArena task registry
- **Gitlab**: First available gitlab task
- **Wikipedia**: First available wikipedia-like task

### 6.2 Viewport Filtering (CORRECTED)
**CRITICAL**: Replace depth/role heuristic from EXP-INTEL-34047713704 with geometry-faithful implementation.

Required implementation:
```python
# CORRECT: Geometry-faithful viewport filtering
# Use Playwright/CDP to get element bounding boxes
# intersect with viewport rectangle (0, 0, 1280, 720)
# keep elements with intersection_area / element_area > IN_VIEWPORT_RATIO_THRESHOLD

# PROHIBITED: Depth/role heuristic
# keep indent <= 4 or role in viewport_roles  ← THIS IS WRONG
```

Implementation options (in order of preference):
1. **Playwright CDP**: Use `page.evaluate()` to call `Accessibility.getFullAXTree` with `union_bound` geometry, compute viewport intersection ratio
2. **Bounding box**: Use `page.locator().bounding_box()` for each element, intersect with viewport rect
3. **WebArena adapter**: Use `research/intel/webarena_adapter.py` `fetch_page_accessibility_tree` if it implements union_bound geometry

If geometry-faithful implementation is not achievable within the execution budget, explicitly label the measurement as "pilot with viewport heuristic approximation" and quantify the approximation error bound.

### 6.3 Pipeline Steps
For each task:
1. Launch Playwright headless Chromium (viewport 1280x720)
2. Navigate to task starting URL
3. Wait for page load (networkidle or 10s timeout)
4. Extract accessibility tree via CDP
5. Apply geometry-faithful viewport filtering (step 6.2)
6. Apply IGNORED_ACTREE_PROPERTIES pruning
7. Truncate at UTTERANCE_MAX_LENGTH=8192 and max_obs_length=1920
8. Compute: total_elements, viewport_elements, pruned_elements, truncated_elements
9. Compute: actual_yield = truncated_elements / total_elements
10. Save raw accessibility tree with sha256 hash

### 6.4 Data Preservation
Save for each task:
- Raw accessibility tree (JSON) with sha256 hash
- Filtered/pruned/truncated element counts
- Actual yield
- Viewport geometry parameters
- Any errors or warnings

## 7. Measures

### 7.1 Primary Metric
- **actual_yield**: elements_surviving_pipeline / total_elements_in_observation for each site type

### 7.2 Secondary Metrics
- **yield_delta**: |actual_yield - heuristic_yield| for each site type
- **viewport_filter_rate**: viewport_elements / total_elements
- **pruning_rate**: pruned_elements / viewport_elements
- **truncation_rate**: truncated_elements / pruned_elements
- **total_elements**: raw accessibility tree size per site type

### 7.3 Infrastructure Metrics
- **docker_auth_success**: boolean
- **docker_images_pulled**: count of successfully pulled images
- **playwright_available**: boolean
- **measurement_time_seconds**: per task

## 8. Null Models

### 8.1 Heuristic Baseline
Heuristic estimates from EXP-INTEL-33945226776: shopping 0.65, gitlab 0.60, wikipedia 0.517. Primary comparison: yield_delta < 0.15.

### 8.2 Method 1 Baseline
Element-count estimates: shopping 0.365, gitlab 0.484, wikipedia 0.517. Secondary comparison: which heuristic method is closer to actual?

### 8.3 Frequency Baseline
If actual yield is near 1.0 for all site types (all elements survive), the pipeline is not filtering meaningfully. If actual yield is near 0.0 for all site types, the pipeline is too aggressive.

## 9. Controls

### 9.1 Positive Control (Shopping)
Shopping task has highest actual yield >40%. Verifies pipeline can extract fragments from complex e-commerce page.

### 9.2 Null Control (Wikipedia)
Wikipedia task has lowest actual yield <60%. Verifies pipeline can distinguish site types.

### 9.3 Infrastructure Control (Docker Auth)
Docker login to ghcr.io succeeds with provided credentials. If fails, experiment is BLOCKED.

### 9.4 Viewport Control (Geometry Faithfulness)
Viewport filtering uses actual bounding-box intersection, not depth/role heuristic. If geometry-faithful implementation is not achievable, measurement is labeled as pilot approximation with error bound.

## 10. Validity Threats

### 10.1 Docker Authentication
Previous attempt (EXP-INTEL-34047713704) found all image pulls denied. If auth remains unavailable, experiment is BLOCKED. Mitigation: attempt multiple auth methods (GITHUB_TOKEN, PAT, anonymous, alternative tags).

### 10.2 Viewport Filtering Approximation
Geometry-faithful viewport filtering via CDP union_bound may not be directly accessible. Fallback to bounding-box intersection with Playwright locators. If neither is achievable, use depth/role heuristic but explicitly label as pilot approximation and bound the error (depth<=4 heuristic over-includes elements by ~10-20% based on parent audit).

### 10.3 Sample Size
N=1 per site type (pilot calibration, not powered statistical test). Cannot generalize to 812-task corpus from 3 tasks. Mitigation: disclose as pilot; require minimum 2-3 tasks per site type before SUPPORTS verdict for C-CROSSSITE/C-LLM-INHERIT.

### 10.4 Task Selection Bias
First available task per site type may not be representative. Mitigation: disclose; future experiments should randomize task selection.

### 10.5 Synthetic-to-Real Gap
WebArena Docker pages are self-hosted, not live production websites. Yield on self-hosted pages may differ from production. Mitigation: this is expected; WebArena is the target corpus for C-CROSSSITE testing.

### 10.6 Heuristic Baseline Method Disagreement
Method 1 (element-count, shopping 0.365) and aggregated median (shopping 0.65) disagree by 28.5pp. The actual yield could be close to either. Decision rule uses heuristic_yield (aggregated median) as primary baseline; Method 1 is secondary comparison.

## 11. Decision Rules

### 11.1 SUPPORTS
If ALL of:
1. Docker authentication succeeds (at least 1 image pulled)
2. actual_yield within 15pp of heuristic_yield for ALL 3 site types
3. Positive control passes (shopping yield >40%)
4. Null control passes (wikipedia yield <60%)
5. Viewport filtering is geometry-faithful or explicitly labeled as pilot approximation

### 11.2 FALSIFIES
If ANY of:
1. Docker authentication succeeds AND actual_yield deviates >15pp for ANY site type
2. Docker authentication succeeds AND positive control fails (shopping yield <40%)
3. Docker authentication succeeds AND null control fails (wikipedia yield >60%)

### 11.3 BLOCKED
If:
1. Docker authentication fails for all 3 site types (all pulls denied)
2. OR Docker images cannot be deployed (insufficient disk/memory)
3. OR Playwright/Chromium not available

### 11.4 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. Viewport filtering cannot be implemented (neither geometry-faithful nor heuristic)
3. Raw data artifacts cannot be preserved

## 12. Expected Outcomes

### 12.1 SUPPORTS
- Heuristic yield estimates are calibrated within 15pp
- 812-task corpus is suitable for C-CROSSSITE/C-LLM-INHERIT testing
- Graph lane can proceed with WebArena Docker integration
- Method 1 (element-count) vs aggregated median dispute resolved by actual measurement

### 12.2 FALSIFIES
- Heuristic yield estimates are not calibrated
- 812-task corpus yield is unknown from heuristics
- Intel should reassess VisualWebArena/Mind2Web as alternatives
- Graph lane should not deploy on WebArena without actual yield validation

### 12.3 BLOCKED
- Docker auth barrier persists
- Central question remains unanswered
- Intel should explore: (a) alternative authentication methods, (b) WebArena public demo instances, (c) VisualWebArena/Mind2Web as lower-uncertainty alternatives
- Infrastructure investment (ghcr.io auth) is the smallest unblocking action

### 12.4 MEASUREMENT_INVALID
- Pipeline needs debugging
- Not scientific evidence for or against
- Must be resolved before retry

## 13. Analysis Plan

1. **Infrastructure Check**: Verify Docker auth, pull images, verify Playwright
2. **Measurement**: For each task (shopping, gitlab, wikipedia):
   a. Deploy Docker container
   b. Launch Playwright, navigate to task URL
   c. Extract accessibility tree
   d. Apply geometry-faithful viewport filtering
   e. Apply IGNORED_ACTREE_PROPERTIES pruning
   f. Truncate at 8192/1920
   g. Compute yield
3. **Comparison**: Compare actual_yield to heuristic_yield (0.65/0.60/0.517) and Method 1 (0.365/0.484/0.517)
4. **Controls**: Verify positive (shopping >40%) and null (wikipedia <60%)
5. **Decision**: Apply frozen decision_rule to determine SUPPORTS/FALSIFIES/BLOCKED

## 14. Carry-Forward from Parent

This experiment preserves the parent handoff (EXP-INTEL-34047713704) four-way distinction:

**established** (inherited, not re-measured):
- WebArena 6 site types, 812 tasks at base_sha 8bc5034
- Heuristic yield estimates: shopping 0.65, reddit 0.65, gitlab 0.60, shopping_admin 0.60, map 0.598, wikipedia 0.517
- Method 1 yields: shopping 0.365, reddit 0.45, shopping_admin 0.468, gitlab 0.484, wikipedia 0.517, map 0.598
- Method 2 degenerate: yields 1.0 for 5/6 site types
- Truncation sensitivity: shopping 0.37, reddit 0.439, gitlab 0.471, shopping_admin 0.453, map 0.702, wikipedia 0.897
- Docker images require auth (denied without GITHUB_TOKEN/PAT)
- Playwright 1.62.0 + Chromium 151.0.7922.34 work
- Docker 28.0.4 + Compose v2.38.2 running

**rejected**: Nothing scientific (BLOCKED is infrastructure failure, not falsification)

**unknown**:
- Whether heuristic estimates match actual yield (CENTRAL QUESTION)
- Whether Method 1 or aggregated median is more predictive
- Whether shopping positive control would show highest yield >40%
- Whether wikipedia null control would show lowest yield <60%
- Whether max_obs_length=1920 is binding truncation on live pages
- Whether 812-task corpus is suitable for C-CROSSSITE/C-LLM-INHERIT
- Whether VisualWebArena/Mind2Web offer lower-uncertainty path

**do_not_assume**:
- Heuristic estimates are calibrated (they are unvalidated priors)
- Aggregated median yield >50% is evidential (Method 2 is degenerate)
- 224 LOC adapter cost generalizes to live integration
- Synthetic adapter scores predict live performance
- Positive control (shopping 0.65) is robust (Method 1 gives 0.365)
- Null control (wikipedia 0.517) is valid (prereg requires <0.40)
- BLOCKED status implies heuristic estimates are wrong (they are unvalidated)
- Depth/role viewport heuristic is equivalent to geometry-faithful union_bound
- N=1 pilot can generalize to full 812-task corpus
- Resolving Docker auth alone is sufficient (viewport filtering must also be corrected)

## 15. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 16. Freeze Statement

This preregistration is frozen BEFORE any infrastructure verification or measurement execution. The experiment will be executed exactly as described here.
