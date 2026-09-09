# EXP-INTEL-34047713704 — Execution Report

## Experiment Identity

- **Experiment ID**: EXP-INTEL-34047713704
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON
- **Status**: BLOCKED
- **Outcome**: NOT_APPLICABLE (infrastructure failure, not scientific falsification)
- **Date**: 2026-09-09
- **Model**: opencode/mimo-v2.5-free

## Executive Summary

**This experiment is BLOCKED.** WebArena Docker images on `ghcr.io/web-arena-x/` require authentication that was not available in this environment. All three Docker image pulls (shopping, gitlab, wikipedia) returned "denied" from GitHub Container Registry.

The central scientific question — whether heuristic yield estimates (0.517-0.65) from EXP-INTEL-33945226776 match actual fragment extraction on live WebArena Docker pages — **remains UNRESOLVED**. No live measurement was possible.

This is an infrastructure failure, NOT a scientific falsification. The heuristic estimates are neither confirmed nor refuted.

## Infrastructure Assessment

### What Worked

| Component | Status | Details |
|-----------|--------|---------|
| Docker Engine | OK | Docker 28.0.4, Compose v2.38.2 |
| Python | OK | Python 3.12.14 |
| Playwright | OK | v1.62.0 installed |
| Chromium | OK | v151.0.7922.34 downloaded |
| Disk Space | OK | 86GB available |
| Memory | OK | 15GB total, 14GB available |

### What Failed

| Component | Status | Error |
|-----------|--------|-------|
| `ghcr.io/web-arena-x/webarena-shopping:latest` | DENIED | `Head "https://ghcr.io/v2/web-arena-x/webarena-shopping/manifests/latest": denied` |
| `ghcr.io/web-arena-x/webarena-gitlab:latest` | DENIED | Same error pattern |
| `ghcr.io/web-arena-x/webarena-wikipedia-like:latest` | DENIED | Same error pattern |
| Alternative tags (v1, v2, stable) | DENIED | All attempted tags denied |

### Root Cause

GitHub Container Registry (ghcr.io) images under `web-arena-x/` require authentication. No `GITHUB_TOKEN` or `GHCR_TOKEN` with `read:packages` scope was available in the execution environment.

## What Was Prepared

A complete measurement script was written at `/tmp/opencode/measure_yield.py` implementing the full REQUIRES_TRANSFORM pipeline:

1. **Docker deployment**: Pull and start containers for shopping, gitlab, wikipedia
2. **Playwright extraction**: Navigate to each container, extract accessibility tree with `page.accessibility.snapshot(depth=None)`
3. **Viewport filtering**: Keep elements within viewport (1280x720) using depth and role heuristics
4. **IGNORED_ACTREE_PROPERTIES pruning**: Remove focusable, editable, readonly, level, settable, multiline, invalid properties
5. **Truncation measurement**: Measure element count at UTTERANCE_MAX_LENGTH=8192 and max_obs_length=1920
6. **Yield computation**: `actual_yield = elements_surviving_full_pipeline / total_elements`

The script is ready to execute once Docker access is resolved.

## Controls Status

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| Positive control (shopping) | Shopping has highest yield >40% | BLOCKED — cannot measure | null |
| Null control (wikipedia) | Wikipedia has lowest yield <60% | BLOCKED — cannot measure | null |
| Docker access | Images pullable from ghcr.io | All 3 denied | **FAIL** |
| Playwright/Chromium | Installed and functional | v1.62.0 + Chromium 151 | PASS |

## Heuristic Baseline (Inherited, Not Re-measured)

From EXP-INTEL-33945226776:

| Site Type | Heuristic Yield (M3) | Method 1 Yield | Aggregated Median |
|-----------|---------------------|----------------|-------------------|
| Shopping | 0.65 | 0.365 | 0.65 |
| Gitlab | 0.60 | 0.484 | 0.60 |
| Wikipedia | 0.517 | 0.517 | 0.517 |

These remain heuristic priors — no live measurement was performed.

## Decision Rule Application

Per the frozen spec.json:

- **SUPPORTS**: Requires yield_delta < 0.15 for ALL 3 site types + positive/null controls pass + no infrastructure failures → **NOT REACHABLE** (infrastructure failure present)
- **FALSIFIES**: Requires yield_delta > 0.15 for any site type OR control violations → **NOT REACHABLE** (no measurement)
- **BLOCKED**: Docker images cannot be pulled → **MATCHED** ✓

**Verdict: BLOCKED**

## Smallest Next Action

1. **Obtain ghcr.io authentication**: Set `GITHUB_TOKEN` with `read:packages` scope, or run `docker login ghcr.io` with a GitHub PAT that has package read permissions
2. **Re-execute this experiment**: The measurement script at `/tmp/opencode/measure_yield.py` is ready; re-run once authentication is available
3. **Alternative**: Check if WebArena provides public demo instances or alternative Docker registries

## Validity Threats

1. **Single observation per task**: Even if Docker were accessible, N=1 per site type is pilot calibration, not powered statistical test
2. **Task selection bias**: Selected tasks may not represent their site type
3. **Playwright vs WebArena rendering**: Accessibility tree extraction may differ from WebArena's custom browser
4. **Viewport simulation**: Without bounding box data, viewport filtering uses depth/role heuristics rather than exact coordinates

## Carry-Forward to Next Experiment

**Established**: Nothing new — this experiment produced no measurements.

**Rejected**: Nothing — no scientific hypothesis was tested.

**Unknown** (unchanged from parent):
- Whether heuristic yield estimates match actual fragment extraction
- Whether Method 1 (shopping 0.365) or aggregated median (0.65) is more predictive
- Whether the 812-task corpus is suitable for C-CROSSSITE/C-LLM-INHERIT

**Do Not Assume** (unchanged from parent):
- WebArena's 812-task corpus is suitable for C-CROSSSITE or C-LLM-INHERIT
- Aggregated median yield >50% is evidential
- The 224 LOC adapter cost generalizes to live integration

**Dependencies**:
- RESOLVE: ghcr.io authentication for WebArena Docker images
- Or: Find alternative public WebArena deployment or benchmarks
