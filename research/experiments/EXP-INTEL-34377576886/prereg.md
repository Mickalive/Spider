# EXP-INTEL-34377576886 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-34377576886
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON
- **Date**: 2026-09-09
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-INTEL-34047713704 (BLOCKED on Docker auth)

## 2. Scientific Question

Can ANY publicly-accessible WebArena deployment path provide a live DOM surface for measuring actual fragment yield, thereby resolving whether heuristic yield estimates (0.517-0.65) are calibrated?

## 3. Motivation

Three prior Intel experiments have attempted to validate heuristic yield estimates for the WebArena 812-task corpus:

1. **EXP-INTEL-33945226776**: Heuristic yield estimates computed. Aggregated medians: shopping 0.65, reddit 0.65, gitlab 0.60, shopping_admin 0.60, map 0.598, wikipedia 0.517. Method 1 (element-count) gives materially lower yields for some types (shopping 0.365 vs 0.65). Central question: are these calibrated?

2. **EXP-INTEL-34047713704**: BLOCKED. Docker images from ghcr.io/web-arena-x/ denied without authentication. Playwright + Chromium confirmed working. Measurement script prepared but viewport filtering uses depth/role heuristic instead of geometry-faithful union_bound. Central question remains unanswered.

3. **This experiment (EXP-INTEL-34377576886)**: Pulse-triggered retry. Prior design attempted same ghcr.io path and failed (failure.json: stage exited code 66). New design must test DIFFERENT deployment paths.

**Key new finding from this design phase**: WebArena-Verified (ServiceNow) images are publicly available on Docker Hub (am1n3e/*), not just ghcr.io. Wikipedia image is 40MB (arm64-only). Shopping image is 5GB (single-platform). Kiwix ZIM files for Wikipedia are freely available (~310MB for 100-article version). These were NOT tested in prior experiments.

**Parent handoff four-way distinction preserved:**

**established** (inherited, not re-measured):
- WebArena 6 site types, 812 tasks at base_sha 8bc5034
- Heuristic yield estimates: shopping 0.65, reddit 0.65, gitlab 0.60, shopping_admin 0.60, map 0.598, wikipedia 0.517
- Method 1 yields: shopping 0.365, reddit 0.45, shopping_admin 0.468, gitlab 0.484, wikipedia 0.517, map 0.598
- Method 2 degenerate: yields 1.0 for 5/6 site types
- Truncation sensitivity: shopping 0.37, reddit 0.439, gitlab 0.471, shopping_admin 0.453, map 0.702, wikipedia 0.897
- ghcr.io images require auth (denied without GITHUB_TOKEN/PAT)
- Playwright 1.62.0 + Chromium work
- Docker 28.0.4 + Compose v2.38.2 running
- Measurement script exists at /tmp/opencode/measure_yield.py (viewport heuristic, sha256 null)

**rejected**: Nothing scientific (BLOCKED is infrastructure failure, not falsification)

**unknown**:
- Whether heuristic estimates match actual yield (CENTRAL QUESTION)
- Whether Method 1 or aggregated median is more predictive
- Whether shopping positive control would show highest yield >40%
- Whether wikipedia null control would show lowest yield <60%
- Whether max_obs_length=1920 is binding truncation on live pages
- Whether 812-task corpus is suitable for C-CROSSSITE/C-LLM-INHERIT
- Whether Docker Hub images work on linux/amd64
- Whether ZIM+Kiwix can serve WebArena-compatible pages
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
- Docker Hub images are available on amd64 (wikipedia is arm64-only)
- ZIM+Kiwix Wikipedia serves the same pages as WebArena Docker Wikipedia

## 4. Hypotheses

### H1: Deployment Path Viability
At least 1 of 3 deployment paths is viable in the current environment:
- **Path A**: Docker Hub am1n3e/webarena-verified-* images pullable on linux/amd64
- **Path B**: ZIM+Kiwix local Wikipedia server serves HTTP content accessible by Playwright
- **Path C**: ghcr.io/web-arena-x images pullable with GITHUB_TOKEN/PAT authentication

### H2: Heuristic Calibration (conditional on H1 success)
If any deployment path succeeds, actual measured yield (with geometry-faithful viewport filtering) is within 15 percentage points of the heuristic estimate for the tested site type.

### H3: Pipeline Functionality (conditional on H1 success)
If any deployment path succeeds, the observation pipeline (accessibility tree extraction + viewport filtering + pruning + truncation) produces a non-empty observation with measurable yield.

## 5. Infrastructure Census (Step 1)

### 5.1 Path A: Docker Hub WebArena-Verified Images
Test in order (smallest to largest):
1. `docker pull --platform linux/amd64 am1n3e/webarena-verified-wikipedia:latest` (40MB claimed, may be arm64-only)
2. `docker pull --platform linux/amd64 am1n3e/webarena-verified-shopping_admin:latest` (1.16GB)
3. `docker pull --platform linux/amd64 am1n3e/webarena-verified-map:latest` (1.11GB)
4. `docker pull --platform linux/amd64 am1n3e/webarena-verified-shopping:latest` (5.05GB)
5. `docker pull --platform linux/amd64 am1n3e/webarena-verified-reddit:latest` (4.26GB)
6. `docker pull --platform linux/amd64 am1n3e/webarena-verified-gitlab:latest` (20.49GB — likely infeasible)

For each attempt, record: pull status, actual image size, platform mismatch errors, timeout status.

### 5.2 Path B: ZIM+Kiwix Wikipedia
1. Download wikipedia_en_100_2026-08.zim (~310MB) from download.kiwix.org
2. Start Kiwix server: `docker run -d -p 8888:80 -v /path/to/zim:/data ghcr.io/kiwix/kiwix-serve:3.3.0 wikipedia_en_100_2026-08.zim`
3. Verify HTTP response at http://localhost:8888
4. This is a DIFFERENT Wikipedia than WebArena's (Kiwix vs Docker self-hosted). Disclosure required.

### 5.3 Path C: ghcr.io Authentication
1. Check GITHUB_TOKEN environment variable
2. Attempt `docker login ghcr.io` with available credentials
3. If login succeeds, pull one image (smallest available)
4. Record exact auth method and error messages

### 5.4 Dataset Analysis (independent of deployment)
1. Load AmineHA/WebArena-Verified from HuggingFace
2. Analyze: site type distribution, multi-site tasks (how many tasks span multiple sites?), intent template complexity, eval evaluator types
3. This provides structural intelligence about the corpus even if no Docker path works

## 6. Measurement Pipeline (Steps 3-5)

### 6.1 Task Selection
Select 1 task per viable deployment path:
- If Path A succeeds: first available task matching the deployed site type
- If Path B succeeds: a Wikipedia task from WebArena-Verified dataset (note: Kiwix Wikipedia is NOT the same as WebArena Docker Wikipedia — disclose this limitation)
- If Path C succeeds: first available task matching the pulled image type

### 6.2 Viewport Filtering (CORRECTED)
**CRITICAL**: Replace depth/role heuristic with geometry-faithful implementation.

Required implementation (in order of preference):
1. **Playwright CDP**: Use `page.evaluate()` to call `Accessibility.getFullAXTree` with `union_bound` geometry, compute viewport intersection ratio
2. **Bounding box**: Use `page.locator().bounding_box()` for each element, intersect with viewport rect (0, 0, 1280, 720)
3. **Pilot approximation**: If neither geometry method is achievable, use depth/role heuristic but explicitly label as pilot with error bound

```python
# CORRECT: Geometry-faithful viewport filtering
# Use Playwright/CDP to get element bounding boxes
# intersect with viewport rectangle (0, 0, 1280, 720)
# keep elements with intersection_area / element_area > IN_VIEWPORT_RATIO_THRESHOLD

# PROHIBITED as primary: Depth/role heuristic
# keep indent <= 4 or role in viewport_roles  ← VALIDITY GAP
```

### 6.3 Pipeline Steps
For each task:
1. Launch Playwright headless Chromium (viewport 1280x720)
2. Navigate to task starting URL
3. Wait for page load (networkidle or 10s timeout)
4. Extract accessibility tree via CDP
5. Apply geometry-faithful viewport filtering (section 6.2)
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
- Deployment path used (A/B/C)
- Any errors or warnings

## 7. Measures

### 7.1 Primary Metric
- **actual_yield**: elements_surviving_pipeline / total_elements_in_observation

### 7.2 Secondary Metrics
- **yield_delta**: |actual_yield - heuristic_yield|
- **viewport_filter_rate**: viewport_elements / total_elements
- **pruning_rate**: pruned_elements / viewport_elements
- **truncation_rate**: truncated_elements / pruned_elements
- **total_elements**: raw accessibility tree size

### 7.3 Infrastructure Metrics
- **deployment_paths_tested**: count
- **deployment_paths_succeeded**: count
- **docker_hub_pullable**: boolean (per image)
- **kiwix_zim_served**: boolean
- **ghcr_auth_success**: boolean
- **playwright_available**: boolean
- **hf_dataset_loaded**: boolean (812 tasks)
- **measurement_time_seconds**: per task

## 8. Null Models

### 8.1 Heuristic Baseline
Heuristic estimates from EXP-INTEL-33945226776. Primary comparison: yield_delta < 0.15.

### 8.2 Method 1 Baseline
Element-count estimates. Secondary comparison: which heuristic method is closer to actual?

### 8.3 Frequency Baseline
If actual yield ≈ 1.0 for all site types, the pipeline is not filtering meaningfully. If actual yield ≈ 0.0, the pipeline is too aggressive.

## 9. Controls

### 9.1 Positive Control (Pipeline Functionality)
If any environment deploys, the observation pipeline must produce a non-empty observation. Verifies pipeline can extract structured data from live DOM.

### 9.2 Infrastructure Control (Deployment Census)
All 3 deployment paths are systematically tested. Even if all fail, the census is informative for the next experiment's design.

### 9.3 Viewport Control (Geometry Faithfulness)
Viewport filtering uses actual bounding-box intersection, not depth/role heuristic. If geometry-faithful implementation is not achievable, measurement is labeled as pilot approximation.

## 10. Validity Threats

### 10.1 Platform Mismatch
Docker Hub Wikipedia image is arm64-only. Shopping image may also be arm64. Mitigation: test with --platform linux/amd64 explicitly; if no amd64 images exist, this is an infrastructure finding.

### 10.2 ZIM+Kiwix Wikipedia ≠ WebArena Docker Wikipedia
Kiwix serves static Wikipedia dumps; WebArena Docker serves a self-hosted Wikipedia with interactive features (edit, search, user pages). Yield on Kiwix may differ from WebArena Docker Wikipedia. Mitigation: disclose explicitly; Kiwix measurement is a lower-bound estimate for pipeline functionality, not a direct yield comparison.

### 10.3 Docker Image Size
Shopping (5GB) and gitlab (20GB) images may exceed disk or timeout constraints. Mitigation: test smallest images first; record pull times; if large images cannot be pulled, this is an infrastructure finding.

### 10.4 Sample Size
N=1 per viable path (pilot calibration). Cannot generalize to 812-task corpus. Mitigation: disclose as pilot; require minimum 2-3 tasks per site type before SUPPORTS verdict for C-CROSSSITE/C-LLM-INHERIT.

### 10.5 Heuristic Baseline Method Disagreement
Method 1 (shopping 0.365) and aggregated median (shopping 0.65) disagree by 28.5pp. Decision rule uses heuristic_yield (aggregated median) as primary; Method 1 is secondary comparison.

### 10.6 Viewport Filtering Approximation
Geometry-faithful CDP union_bound may not be directly accessible. Fallback to bounding_box intersection. If neither achievable, use depth/role heuristic with explicit pilot label and error bound.

## 11. Decision Rules

### 11.1 SUPPORTS
If ALL of:
1. At least 1 deployment path succeeds
2. actual_yield within 15pp of heuristic_yield for the tested site type
3. Positive control passes (pipeline produces non-empty observation)
4. Viewport filtering is geometry-faithful or explicitly labeled as pilot approximation

### 11.2 FALSIFIES
If ANY of:
1. At least 1 deployment path succeeds AND actual_yield deviates >15pp from heuristic
2. At least 1 deployment path succeeds AND positive control fails (empty observation)

### 11.3 BLOCKED
If:
1. ALL 3 deployment paths fail (no environment can be deployed)
2. OR no image is pullable on linux/amd64 within disk/time constraints

### 11.4 MEASUREMENT_INVALID
If:
1. A path deploys but pipeline errors prevent yield computation
2. Viewport filtering cannot be implemented (neither geometry-faithful nor heuristic)
3. Raw data artifacts cannot be preserved

## 12. Expected Outcomes

### 12.1 SUPPORTS
- At least one deployment path works
- Heuristic yield estimate is calibrated within 15pp for that site type
- Intel can recommend that site type for C-CROSSSITE/C-LLM-INHERIT testing
- Other site types remain unvalidated

### 12.2 FALSIFIES
- At least one deployment path works
- Heuristic yield estimate is NOT calibrated (>15pp deviation)
- 812-task corpus heuristic priors are unreliable
- Intel should reassess VisualWebArena/Mind2Web as alternatives

### 12.3 BLOCKED
- No deployment path works in the current environment
- Complete infrastructure census available for next design
- Intel should consider: (a) VisualWebArena (different Docker images), (b) Mind2Web (HuggingFace, no Docker needed), (c) public WebArena demo instances, (d) AWS AMI approach

### 12.4 MEASUREMENT_INVALID
- Pipeline debugging needed
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Infrastructure Census**: Test Path A (Docker Hub), Path B (ZIM+Kiwix), Path C (ghcr.io) in order. Record exact status.
2. **Dataset Analysis**: Load HuggingFace WebArena-Verified. Analyze task metadata. This is independent of Docker.
3. **Measurement**: For each viable path, deploy environment, run Playwright pipeline, compute yield.
4. **Comparison**: Compare actual_yield to heuristic_yield and Method 1.
5. **Controls**: Verify positive control (non-empty observation) and infrastructure control (census completeness).
6. **Decision**: Apply frozen decision_rule.

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any infrastructure verification or measurement execution. The experiment will be executed exactly as described here.
