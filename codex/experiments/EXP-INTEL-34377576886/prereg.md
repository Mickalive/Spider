# EXP-INTEL-34377576886 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-34377576886
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON
- **Date**: 2026-09-09
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-INTEL-34047713704 (BLOCKED on Docker auth)

## 2. Scientific Question

Can ANY publicly-accessible WebArena deployment path (Docker Hub WebArena-Verified images or Mind2Web HuggingFace dataset) provide a live DOM surface for measuring actual fragment yield, thereby resolving whether heuristic yield estimates (0.517-0.65) are calibrated OR whether Mind2Web offers a viable alternative testbed?

## 3. Motivation

Three prior Intel experiments have attempted to validate heuristic yield estimates for the WebArena 812-task corpus:

1. **EXP-INTEL-33945226776**: Heuristic yield estimates computed. Aggregated medians: shopping 0.65, reddit 0.65, gitlab 0.60, shopping_admin 0.60, map 0.598, wikipedia 0.517. Method 1 (element-count) gives materially lower yields for some types (shopping 0.365 vs 0.65). Central question: are these calibrated?

2. **EXP-INTEL-34047713704**: BLOCKED. Docker images from ghcr.io/web-arena-x/ denied without authentication. Playwright + Chromium confirmed working. Measurement script prepared but viewport filtering uses depth/role heuristic instead of geometry-faithful union_bound. Central question remains unanswered.

3. **Prior design attempt for this experiment**: Failed with exit code 66. Existing spec.json tested 3 Docker paths (Docker Hub, ZIM+Kiwix, ghcr.io). Design was comprehensive but execution failed.

4. **This experiment (EXP-INTEL-34377576886, revised)**: Simplified design testing 2 paths: (A) Docker Hub shopping image (smallest, no auth required), (B) Mind2Web HuggingFace (Docker-free alternative). Addresses auditor required_fixes: geometry-faithful viewport filtering, durable artifact hashes, pilot disclosure.

**Key new finding from this design phase**: WebArena-Verified (ServiceNow) images are publicly available on Docker Hub (am1n3e/*), not just ghcr.io. Shopping image is 5GB (single-platform). These were NOT tested in prior experiments. Mind2Web (OSU-NLP-Group) provides 2000+ tasks across 137 websites with trajectory data on HuggingFace — no Docker required.

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
- Whether max_obs_length=1920 is binding truncation on live pages
- Whether 812-task corpus is suitable for C-CROSSSITE/C-LLM-INHERIT
- Whether Docker Hub images work on linux/amd64
- Whether Mind2Web is structurally compatible with SPIDER fragment model
- Whether VisualWebArena offers lower-uncertainty path if both fail

**do_not_assume**:
- Heuristic estimates are calibrated (they are unvalidated priors)
- Aggregated median yield >50% is evidential (Method 2 is degenerate)
- 224 LOC adapter cost generalizes to live integration
- Synthetic adapter scores predict live performance
- Positive control (shopping 0.65) is robust (Method 1 gives 0.365)
- BLOCKED status implies heuristic estimates are wrong (they are unvalidated)
- Depth/role viewport heuristic is equivalent to geometry-faithful implementation
- N=1 pilot can generalize to full 812-task corpus
- Resolving Docker auth alone is sufficient (viewport filtering must also be corrected)
- Docker Hub images are available on amd64 (wikipedia is arm64-only)
- Mind2Web HTML snapshots are equivalent to live DOM (they are static dumps)

## 4. Hypotheses

### H1: Path A Viability (Docker Hub Shopping)
The Docker Hub image `am1n3e/webarena-verified-shopping:latest` is pullable on linux/amd64 within 10 minutes and serves HTTP content on an exposed port.

### H2: Path B Viability (Mind2Web)
The Mind2Web dataset (osu-nlp-group/Mind2Web) loads successfully from HuggingFace and contains >=50% of tasks with HTML snapshots AND trajectory/action data.

### H3: Heuristic Calibration (conditional on H1 success)
If Path A succeeds, actual measured yield (with geometry-faithful viewport filtering) is within 15 percentage points of the heuristic estimate for shopping (0.65).

### H4: Pipeline Functionality (conditional on H1 success)
If Path A succeeds, the observation pipeline (accessibility tree extraction + geometry-faithful viewport filtering + pruning + truncation) produces a non-empty observation with measurable yield.

## 5. Infrastructure Census (Step 1)

### 5.1 Path A: Docker Hub WebArena-Verified Shopping Image
Test sequence:
1. `docker pull --platform linux/amd64 am1n3e/webarena-verified-shopping:latest` (5GB claimed)
2. Record: pull status, actual image size, platform mismatch errors, timeout (10min limit)
3. If pull succeeds: `docker run -d -p 8080:8080 am1n3e/webarena-verified-shopping:latest`
4. Verify HTTP response at http://localhost:8080
5. Record: container start status, HTTP response code, response time

### 5.2 Path B: Mind2Web Dataset Assessment
1. Load dataset: `datasets.load_dataset("osu-nlp-group/Mind2Web")`
2. Analyze splits: train/dev/test sizes
3. Count unique websites across all splits
4. Check for HTML content: does any field contain HTML markup?
5. Check for trajectory data: are action sequences included?
6. Sample 1 task: examine full structure (fields, data types, completeness)
7. Record: dataset size, website count, HTML availability, trajectory availability

### 5.3 Infrastructure Prerequisites
- Docker daemon running (verified in parent)
- Playwright 1.62.0 + Chromium installed (verified in parent)
- 86GB disk / 15GB RAM available (verified in parent)
- Internet access for Docker Hub and HuggingFace

## 6. Measurement Pipeline (Steps 3-4, conditional on Path A success)

### 6.1 Task Selection
Select 1 shopping task from WebArena-Verified dataset (HuggingFace AmineHA/WebArena-Verified):
- Filter: site_type == "shopping"
- Select: first task with non-empty starting_url
- Record: task_id, starting_url, intent, eval_spec

### 6.2 Viewport Filtering (GEOMETRY-FAITHFUL)
**CRITICAL**: Replace depth/role heuristic with geometry-faithful implementation.

Implementation:
```python
# CORRECT: Geometry-faithful viewport filtering
# Use Playwright locator.bounding_box() for each element
# intersect with viewport rectangle (0, 0, 1280, 720)
# keep elements with intersection_area / element_area > 0.5

from playwright.sync_api import sync_playwright

viewport_rect = {"x": 0, "y": 0, "width": 1280, "height": 720}

def compute_intersection_area(box, viewport):
    """Compute intersection area between element bounding box and viewport."""
    x1 = max(box["x"], viewport["x"])
    y1 = max(box["y"], viewport["y"])
    x2 = min(box["x"] + box["width"], viewport["x"] + viewport["width"])
    y2 = min(box["y"] + box["height"], viewport["y"] + viewport["height"])
    if x1 >= x2 or y1 >= y2:
        return 0.0
    return (x2 - x1) * (y2 - y1)

def is_in_viewport(element, viewport, threshold=0.5):
    """Check if element is sufficiently within viewport."""
    box = element.bounding_box()
    if box is None:
        return False
    element_area = box["width"] * box["height"]
    if element_area == 0:
        return False
    intersection = compute_intersection_area(box, viewport)
    return (intersection / element_area) > threshold

# PROHIBITED as primary: Depth/role heuristic
# keep indent <= 4 or role in viewport_roles  ← VALIDITY GAP
```

### 6.3 Pipeline Steps
For the selected task:
1. Launch Playwright headless Chromium (viewport 1280x720)
2. Navigate to task starting_url
3. Wait for page load (networkidle or 10s timeout)
4. Extract accessibility tree via CDP (page.evaluate with Accessibility.getFullAXTree)
5. Apply geometry-faithful viewport filtering (section 6.2)
6. Apply IGNORED_ACTREE_PROPERTIES pruning (remove: focused, hash, keyshortcuts, level, bonusDescription, description, descriptionFrom, details, readonly, required, checked, expanded, popup, cursor, roleDescription, value, valueForRange, valuemin, valuemax, valuetext)
7. Truncate at UTTERANCE_MAX_LENGTH=8192 (character-level) and max_obs_length=1920 (element-level)
8. Compute: total_elements, viewport_elements, pruned_elements, truncated_elements
9. Compute: actual_yield = truncated_elements / total_elements
10. Save raw accessibility tree with sha256 hash

### 6.4 Data Preservation
Save for each measurement:
- Raw accessibility tree (JSON) with sha256 hash
- Filtered/pruned/truncated element counts
- Actual yield
- Viewport geometry parameters (1280x720)
- Deployment path used (A or B)
- Any errors or warnings
- Playwright version, Chromium version, Python version

## 7. Measures

### 7.1 Primary Metric
- **actual_yield**: elements_surviving_pipeline / total_elements_in_observation

### 7.2 Secondary Metrics
- **yield_delta**: |actual_yield - heuristic_yield|
- **viewport_filter_rate**: viewport_elements / total_elements
- **pruning_rate**: pruned_elements / viewport_elements
- **truncation_rate**: truncated_elements / pruned_elements
- **total_elements**: raw accessibility tree size
- **character_count**: observation character count after truncation

### 7.3 Infrastructure Metrics
- **docker_hub_pull_success**: boolean
- **docker_hub_image_size_gb**: float
- **docker_hub_pull_time_seconds**: float
- **docker_container_start_success**: boolean
- **docker_http_response_code**: integer
- **mind2web_load_success**: boolean
- **mind2web_task_count**: integer
- **mind2web_website_count**: integer
- **mind2web_html_available**: boolean
- **mind2web_trajectory_available**: boolean
- **playwright_available**: boolean
- **measurement_time_seconds**: float

## 8. Null Models

### 8.1 Heuristic Baseline
Heuristic estimates from EXP-INTEL-33945226776. Primary comparison: yield_delta < 0.15.

### 8.2 Method 1 Baseline
Element-count estimates. Secondary comparison: which heuristic method is closer to actual?

### 8.3 Frequency Baseline
If actual_yield ≈ 1.0, pipeline is not filtering meaningfully. If actual_yield ≈ 0.0, pipeline is too aggressive.

## 9. Controls

### 9.1 Positive Control (Pipeline Functionality)
If Path A deploys, observation pipeline must produce non-empty observation with >0 elements. Verifies pipeline can extract structured data from live DOM.

### 9.2 Null Control (Environment Functionality)
If Path A deploys, at least 1 shopping task starting URL must return HTTP 200. If 404/500, environment is not functional (infrastructure finding).

### 9.3 Viewport Control (Geometry Faithfulness)
Viewport filtering uses locator.bounding_box() intersection, NOT depth/role heuristic. If bounding_box is not achievable (e.g., elements not queryable), measurement is labeled as pilot with error bound.

### 9.4 Mind2Web Control (Structural Compatibility)
Mind2Web assessment must check: (a) HTML snapshots present in >=50% of tasks, (b) trajectory/action data present, (c) >=100 unique websites. If any check fails, Mind2Web is structurally incompatible.

## 10. Validity Threats

### 10.1 Platform Mismatch
Docker Hub shopping image may be arm64-only. Mitigation: test with --platform linux/amd64 explicitly; if no amd64 image exists, this is an infrastructure finding.

### 10.2 Docker Image Size
Shopping image is 5GB. May exceed disk or timeout constraints. Mitigation: 10min timeout; if pull fails, record exact error and move to Path B.

### 10.3 Mind2Web HTML Snapshots
Mind2Web may store HTML as compressed files, URLs, or derived features — not raw HTML. Mitigation: explicitly check for HTML markup in dataset fields; if not present, disclose as structural gap.

### 10.4 Sample Size
N=1 per viable path (pilot calibration). Cannot generalize to 812-task corpus. Mitigation: disclose as pilot; require minimum 2-3 tasks per site type before SUPPORTS verdict for C-CROSSSITE/C-LLM-INHERIT.

### 10.5 Heuristic Baseline Method Disagreement
Method 1 (shopping 0.365) and aggregated median (shopping 0.65) disagree by 28.5pp. Decision rule uses heuristic_yield (aggregated median) as primary; Method 1 is secondary comparison.

### 10.6 Viewport Filtering Approximation
Geometry-faithful bounding_box intersection requires elements to be queryable via Playwright locators. If accessibility tree nodes don't have corresponding locators, fallback to depth/role heuristic with explicit pilot label.

### 10.7 Static vs Live DOM
Mind2Web HTML snapshots are static dumps, not live DOM. Yield measurements on Mind2Web would not reflect dynamic content, JavaScript execution, or network requests. Disclosure required.

## 11. Decision Rules

### 11.1 SUPPORTS (Path A)
If ALL of:
1. Path A succeeds (Docker Hub shopping image pullable and serving HTTP)
2. actual_yield within 15pp of heuristic_yield (0.65) for shopping
3. Positive control passes (pipeline produces non-empty observation)
4. Viewport filtering is geometry-faithful or explicitly labeled as pilot approximation

### 11.2 SUPPORTS (Path B)
If ALL of:
1. Path A fails (Docker Hub shopping image not pullable or not serving)
2. Mind2Web loads successfully
3. Mind2Web has >=50% tasks with HTML snapshots AND trajectory data
4. Mind2Web has >=100 unique websites

### 11.3 FALSIFIES (Heuristic)
If:
1. Path A succeeds AND actual_yield deviates >15pp from heuristic (0.65)

### 11.4 FALSIFIES (Mind2Web)
If:
1. Path A fails AND Mind2Web has <50% tasks with HTML snapshots OR no trajectory data OR <100 websites

### 11.5 BLOCKED
If:
1. Path A fails (Docker Hub shopping image not pullable or not serving HTTP)
2. AND Path B fails (Mind2Web doesn't load or is structurally incompatible)

### 11.6 MEASUREMENT_INVALID
If:
1. Path A succeeds but pipeline errors prevent yield computation
2. Viewport filtering cannot be implemented (neither geometry-faithful nor heuristic)
3. Raw data artifacts cannot be preserved

## 12. Expected Outcomes

### 12.1 SUPPORTS (Path A)
- Docker Hub shopping image works on linux/amd64
- Heuristic yield estimate (0.65) is calibrated within 15pp
- Intel can recommend shopping site type for C-CROSSSITE/C-LLM-INHERIT testing
- Other site types remain unvalidated

### 12.2 SUPPORTS (Path B)
- Docker Hub shopping image doesn't work
- Mind2Web is structurally compatible (HTML + trajectories + diverse sites)
- Intel can recommend Mind2Web as Docker-free alternative for cross-site diversity
- Different corpus than WebArena — separate yield calibration needed

### 12.3 FALSIFIES (Heuristic)
- Docker Hub shopping image works
- Heuristic yield estimate (0.65) is NOT calibrated (>15pp deviation)
- 812-task corpus heuristic priors are unreliable
- Intel should reassess VisualWebArena or other benchmarks

### 12.4 FALSIFIES (Mind2Web)
- Docker Hub shopping image doesn't work
- Mind2Web lacks HTML snapshots or trajectory data
- Mind2Web cannot serve as SPIDER testbed
- Intel should assess VisualWebArena or other benchmarks

### 12.5 BLOCKED
- Neither Docker Hub nor Mind2Web works
- Complete infrastructure census available for next design
- Intel should consider: (a) VisualWebArena (different Docker images), (b) public WebArena demo instances, (c) AWS AMI approach

## 13. Analysis Plan

1. **Infrastructure Census**: Test Path A (Docker Hub shopping), Path B (Mind2Web). Record exact status.
2. **Measurement** (conditional on Path A): Deploy shopping environment, run Playwright pipeline, compute yield.
3. **Comparison**: Compare actual_yield to heuristic_yield and Method 1.
4. **Controls**: Verify positive control (non-empty observation) and null control (HTTP 200).
5. **Decision**: Apply frozen decision_rule.

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any infrastructure verification or measurement execution. The experiment will be executed exactly as described here.
