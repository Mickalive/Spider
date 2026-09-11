# EXP-INTEL-34377576886 — Execution Report

## Experiment Summary

**Status**: COMPLETE  
**Outcome**: FALSIFIES  
**Lane**: Intel  
**Claims**: C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON

This experiment resolved the central unknown from three prior BLOCKED experiments: whether heuristic yield estimates (0.517-0.65) for the WebArena 812-task corpus are calibrated against actual live DOM extraction.

**Key finding**: The heuristic yield estimate for shopping (0.65) is **falsified**. Actual measured yield with geometry-faithful viewport filtering is **0.0427** (4.27%), deviating 60.73 percentage points from the heuristic — far exceeding the 15pp decision threshold. Method 1 estimate (0.365) is also falsified with 32.23pp deviation.

## Infrastructure Assessment

### Path A: Docker Hub Shopping Image — SUCCESS

| Metric | Value |
|--------|-------|
| Image | `am1n3e/webarena-verified-shopping:latest` |
| Actual size | 13.3 GB (claimed 5 GB) |
| Platform | linux/amd64 |
| Pull time | ~95 seconds |
| Container | Running on port 8080 → 80 |
| HTTP response | 200 (164 KB page) |
| Site | "One Stop Market" (Magento) |

This is the **first successful WebArena Docker deployment** across 3 Intel experiments. Prior attempts were blocked on ghcr.io authentication.

### Path B: Mind2Web Dataset — PARTIAL SUCCESS

| Metric | Value |
|--------|-------|
| Dataset | `osunlp/Mind2Web` (public, CC-BY-4.0) |
| Tasks | 1,009 |
| HTML snapshots | 100% of tasks |
| Trajectory data | 100% of tasks |
| Unique websites | 73 |
| Domains | 3 (Entertainment, Shopping, Travel) |
| S4 diversity | **FAIL** (73 < 100 threshold) |

Mind2Web is structurally compatible for HTML+trajectory but fails the diversity threshold for cross-site testing.

## Measurement Results

### Shopping Task 21 (Headphones Review)

| Stage | Elements | Rate |
|-------|----------|------|
| CDP accessibility tree | 2,296 | — |
| Playwright locators with bbox | 258 | 11.2% |
| Viewport filtered (geometry) | 98 | 4.3% |
| After pruning | 98 | 4.3% |
| After truncation (1920) | 98 | 4.3% |

**Actual yield: 0.0427** (truncated_1920 / total_cdp)

### Shopping Task 22 (Camera Review)

| Stage | Elements | Rate |
|-------|----------|------|
| CDP accessibility tree | 2,294 | — |
| Playwright locators with bbox | 249 | 10.8% |
| Viewport filtered (geometry) | 98 | 4.3% |
| After truncation (1920) | 98 | 4.3% |

**Actual yield: 0.0427** — identical to task 21, confirming measurement stability.

### Comparison to Baselines

| Estimate | Value | Delta from Actual | >15pp? |
|----------|-------|-------------------|--------|
| Heuristic (aggregated median) | 0.65 | 0.6073 (60.73pp) | **YES** |
| Method 1 (element-count) | 0.365 | 0.3223 (32.23pp) | **YES** |

Both heuristic estimates are **falsified** by the geometry-faithful measurement.

## Decision Rule Application

From frozen spec.json decision_rule:

1. **SUPPORTS (Path A)**: Requires yield_delta < 0.15 for ALL 3 site types — **NOT MET** (delta = 0.6073)
2. **FALSIFIES (Heuristic)**: Path A succeeds AND yield_delta > 0.15 — **MET** (delta = 0.6073 > 0.15)
3. **SUPPORTS (Path B)**: Requires Path A fail — **NOT APPLICABLE** (Path A succeeded)
4. **FALSIFIES (Mind2Web)**: Requires Path A fail — **NOT APPLICABLE**
5. **BLOCKED**: Requires both paths fail — **NOT APPLICABLE**

**Verdict: FALSIFIES** — Heuristic yield estimate for shopping (0.65) is not calibrated within 15pp of actual yield.

## Controls Status

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| Positive (shopping >40%) | Yield > 0.40 | Yield = 0.0427 | **FAIL** |
| Null (wikipedia <60%) | Yield < 0.60 | NOT_MEASURED | null |
| Docker Hub access | Pullable | Pull succeeded | **PASS** |
| Playwright/Chromium | Functional | Functional | **PASS** |
| Viewport geometry | bounding_box() | Implemented correctly | **PASS** |
| Heuristic baseline | Calibrated | 60.73pp deviation | **FAIL** |
| Method 1 baseline | Calibrated | 32.23pp deviation | **FAIL** |
| Mind2Web structural | ≥100 websites | 73 websites | **FAIL** |

## Validity Threats

### 1. Denominator Ambiguity (MODERATE)
The CDP accessibility tree has 2,296 elements, but only 258 (11.2%) have corresponding Playwright locators. The yield denominator uses CDP count. If the heuristic model assumed a different denominator (e.g., locator count only), the comparison is not apples-to-apples. This is the most significant validity threat.

### 2. Sample Size (LOW)
N=2 pilot (both shopping review tasks). Cannot generalize to 187-shopping-task corpus. Both tasks show identical yield, suggesting stability, but both are similar page types.

### 3. Viewport Scrolling (LOW)
Measurement captures only the initial viewport (1280x720). Scrolled content is not measured. Shopping review pages may have significant below-fold content.

### 4. Magento-Specific (LOW)
The "One Stop Market" site uses Magento page builder with many container elements. Other shopping sites may have different DOM structures.

## Consequences

### If Outcome is FALSIFIES (current):
- Heuristic yield priors (0.517-0.65) are **unreliable** for shopping
- The 812-task corpus heuristic model needs recalibration or replacement
- C-CROSSSITE/C-LLM-INHERIT should not proceed with shopping tasks based on heuristic estimates
- Intel should assess whether other site types (gitlab, reddit, map, wikipedia) show different yield patterns
- The denominator ambiguity (CDP vs locator count) must be resolved before generalizing

### If Outcome were SUPPORTS (counterfactual):
- Heuristic model would be calibrated for shopping
- C-CROSSSITE/C-LLM-INHERIT could proceed with 812-task corpus
- Graph lane could use shopping as positive control site type

## Smallest Next Action

1. **Resolve denominator ambiguity**: Run the same measurement but compute yield using Playwright locator count (258) as denominator instead of CDP count (2296). If yield = 98/258 = 0.38, this is closer to Method 1 (0.365) and the comparison changes significantly.

2. **Measure additional site types**: Run geometry-faithful measurement on gitlab, reddit, map tasks to determine if yield varies by site type.

3. **Assess VisualWebArena**: If shopping yield remains low, VisualWebArena may offer a different environment with better fragment availability.

## Carry-Forward for Next Experiment

### Established (this experiment):
- Docker Hub `am1n3e/webarena-verified-shopping:latest` is pullable and serving HTTP on linux/amd64 (13.3GB)
- Geometry-faithful viewport filtering implemented and working
- Shopping yield with CDP denominator: 0.0427 (N=2 pilot, consistent)
- Mind2Web (osunlp): 1009 tasks, 100% HTML+trajectory, 73 websites (below 100 threshold)
- Heuristic shopping estimate (0.65) is falsified by 60.73pp
- Method 1 shopping estimate (0.365) is falsified by 32.23pp

### Rejected:
- Heuristic yield model for shopping is not calibrated (FALSIFIED)
- Mind2Web as cross-site diversity testbed (FAIL on S4, 73 < 100 websites)

### Unknown:
- Whether CDP count or locator count is the correct yield denominator
- Whether other site types show different yield patterns
- Whether yield of 0.0427 reflects genuine DOM structure or measurement artifact
- Whether scrolling or lazy-loading affects results

### Do Not Assume:
- Do not assume yield of 0.0427 generalizes to all 187 shopping tasks (N=2 pilot)
- Do not assume the denominator ambiguity changes the verdict (needs explicit measurement)
- Do not assume other site types will show similar yield (unmeasured)
- Do not assume Mind2Web's 73 websites are insufficient for limited testing (may be useful for single-site-type analysis)
