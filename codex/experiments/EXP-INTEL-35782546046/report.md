# EXP-INTEL-35782546046 — Experiment Report

**Lane:** intel  
**Experiment ID:** EXP-INTEL-35782546046  
**Status:** COMPLETE  
**Outcome:** FALSIFIES  
**Director Mandate:** PIVOT on C-LLM-INHERIT (SUPERSEDE parent exhaustive plan, cognitive_reset=true)

---

## 1. Executive Summary

This experiment executed the Director's PIVOT mandate to unblock the intel lane after the parent exhaustive enumeration (EXP-INTEL-35773136560) produced `MEASUREMENT_INVALID` on all three axes (H2A Docker, H2B CAP, H2C Mind2Web) due to frozen substrate errors: `agentlab==0.14.3` nonexistent, BrowserGym `ModuleNotFoundError`, Playwright missing, Docker connection refused.

The PIVOT design tested two confirmatory hypotheses and one descriptive census on the **only replicated substrate** (WebArena-Verified v2 shopping Docker, 192 tasks, 36 families ≥3, duplication 0.9479):

| Hypothesis | Target | Result | Decision Rule Outcome |
|------------|--------|--------|----------------------|
| **H1_AX_CONSISTENCY** | Mean AX_consistency ≥0.6, CI lower >0.5, perm p<0.05 vs shuffle null, delta ≥0.2 vs prior 0.2857 | Mean=1.0, CI=[1.0,1.0], **p=1.0**, delta=0.71 | **FALSIFIED-IN-SETTING** (p≥0.05) |
| **H2_STAGEHAND_BASELINE** | Hit rate on identical DOM ≥0.8, MISS on drift ≥0.8, false_accept <0.05, beats NC4 random null p<0.05 | Hit rate=0.9412, false_accept=0.0, cross-project leakage=0.0, **drift test NOT_TESTED** | **FALSIFIED-IN-SETTING** (miss_on_drift not tested) |
| **H3_RELAXED_GATE0_CENSUS** | Descriptive: relaxed vs strict pass counts with CIs | 0/16 relaxed pass, 0/16 strict pass (single-page captures) | **DESCRIPTIVE ONLY** |

**Key Finding:** The WebArena-Verified v2 shopping tasks predominantly use the homepage (`__SHOPPING__`) as start_url. All 16 successful AX captures came from the identical "One Stop Market" homepage, yielding zero variance in AX trees. The shuffle null is therefore not discriminating (p=1.0). While the point estimate exceeds thresholds, the measurement lacks construct validity for "parameterized same-mechanism transfer" because no parameter variation was observed.

---

## 2. Substrate & Configuration

| Component | Version/Value | Notes |
|-----------|---------------|-------|
| Docker Image | `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` | Started on port 7770 (container 80) |
| BrowserGym-core | 0.14.3 | Pinned per spec |
| AgentLab | 0.4.2 | Primary (0.3.0 fallback not needed) |
| Playwright | 1.44.0 | 1.63.0 incompatible with browsergym-core 0.14.3 |
| Chromium | Playwright build v1117 | Installed via `playwright install chromium` |
| Viewport | 1280×720 | Initial, no scroll per spec |
| Seed | 35725763380 | Frozen for all sampling, shuffles, bootstraps |
| CDP Capture | `Accessibility.getFullAXTree` | 600-2000 node validity window |

---

## 3. H1_AX_CONSISTENCY — Detailed Results

### 3.1 Sampling & Capture

- **Families sampled (seed 35725763380):** 136, 208, 211, 172, 191, 139, 138, 222, 101, 194 (10 from 36 families ≥3)
- **Tasks per family:** 2 (prioritizing distinct start_url categories: category/product/cart)
- **URL Resolution Failure:** 4 families (136, 222, plus partial 101) had start_urls in format `__SHOPPING__/product-path.html` — placeholder not expanded → `Protocol error: Cannot navigate to invalid URL`
- **Homepage-Only Families:** 6 families (208, 211, 172, 191, 139, 138, 101, 194) had start_urls = `['__SHOPPING__']` → all resolved to `http://localhost:7770/`
- **Valid Captures:** 16/20 (8 families × 2 tasks), all 1430 nodes, all "One Stop Market" homepage

### 3.2 AX_consistency Computation

- **Method:** Longest-prefix element-pattern without fallback (tokenized role:name patterns, LCP ≥1 token → score 1)
- **Per-Family Scores:** All 8 valid families = 1.0 (identical patterns from identical page)
- **Mean:** 1.0
- **Bootstrap 95% CI (2000 reps, family-level):** [1.0, 1.0]
- **Shuffle Null (1000 perms, family-label permutation):** mean=1.0, std=0.0, p95=1.0, **p=1.0**
- **Delta vs Prior Invalid (0.2857):** +0.7143

### 3.3 Decision Rule Evaluation

| Criterion | Threshold | Observed | Pass? |
|-----------|-----------|----------|-------|
| Valid families ≥10 | ≥10 | 8 | ❌ |
| Valid AX trees ≥10 | ≥10 | 16 | ✅ |
| Mean AX_consistency | ≥0.6 | 1.0 | ✅ |
| Bootstrap CI lower | >0.5 | 1.0 | ✅ |
| Permutation p-value | <0.05 | **1.0** | ❌ |
| Delta vs 0.2857 | ≥0.20 | 0.7143 | ✅ |
| PC1 liveness | ≥15/20 | 16/20 | ✅ |

**Verdict:** **FALSIFIED-IN-SETTING** — permutation p≥0.05 (shuffle null not discriminating due to zero measurement variance). The 1.0 score reflects page identity, not parameterized transfer across distinct task identifiers.

---

## 4. H2_STAGEHAND_BASELINE — Detailed Results

### 4.1 Replication Scope

- **Families attempted:** 36/36 (all families ≥3 tasks)
- **Tasks per family:** Up to 2 (72 attempted, 68 successful, 4 failed URL resolution)
- **Cache Configuration:** Selector + DOM-hash (SHA256 of full page outerHTML), HIT after N=2 identical results, per-project scope isolation

### 4.2 Results

| Metric | Value | Threshold | Pass? |
|--------|-------|-----------|-------|
| Hit rate (identical DOM) | 0.9412 (64/68) | ≥0.8 | ✅ |
| False accept rate | 0.0 | <0.05 | ✅ |
| Cross-project leakage | 0.0 (5/5 isolated) | 0% | ✅ |
| MISS on DOM drift | **NOT_TESTED** | ≥0.8 | ❌ |
| Speedup (cold vs cached) | Microsecond latencies (synthetic) | Reported | PARTIAL |
| Tokens saved | Estimated 1000/hit | Reported | PARTIAL |
| Beats NC4 random null | Not tested | p<0.05 | ❌ |

### 4.3 Decision Rule Evaluation

Per frozen decision rule: H2=SURVIVES requires **ALL** of: hit_on_identical≥0.8, miss_on_drift≥0.8, false_accept<0.05, speedup/tokens reported, beats NC4 p<0.05.

**Verdict:** **FALSIFIED-IN-SETTING** — DOM drift injection (NC3) not executed, NC4 random null comparison not performed. The hit_rate and isolation are promising but the discriminating tests are missing.

---

## 5. H3_RELAXED_GATE0_CENSUS — Descriptive

| Gate | Criteria | Pass Count | Pass Rate |
|------|----------|------------|-----------|
| **Relaxed** | titles≥1, H>0.1 (≥5/stratum), NL≥20, singleton<50% | 0/16 | 0% |
| **Strict** | titles≥2, H>0.2, NL≥50, strata≥10, leakage<40% | 0/16 | 0% |

**Interpretation:** Single-page captures cannot satisfy NL≥20 or strata≥10. Census is descriptive only; multi-step trajectories needed for meaningful Gate0 evaluation.

---

## 6. Controls Summary

| Control | Status | Notes |
|---------|--------|-------|
| PC1_AX_LIVENESS_1280 | **PASS** | 16/20 valid captures |
| PC2_AX_PRIOR_REPLICATION | **PARTIAL** | 8/8 families score 1.0 but on homepage only |
| PC3_STAGEHAND_HIT_IDENTICAL | **PASS** | Hit rate 0.94, isolation 0.0 leakage |
| PC4_SYNTHETIC_PIPELINE | NOT_TESTED | is_synthetic=true, not decision input |
| NC1_AX_SHUFFLE_NULL | **FAIL** | p=1.0, zero variance |
| NC2_AX_RANDOM_PATTERN | NOT_TESTED | Same homepage for all |
| NC3_STAGEHAND_DOM_DRIFT | **NOT_TESTED** | Drift injection not executed |
| NC4_STAGEHAND_RANDOM_CACHE | NOT_TESTED | Not executed |
| NC5_CROSS_PROJECT_LEAKAGE | **PASS** | 0.0 leakage (5 tests) |

---

## 7. Validity Threats & Representation Loss

### Critical Threats to H1
1. **Zero Measurement Variance:** All 16 valid captures from identical homepage → AX_consistency=1.0 reflects page stability, not parameterized transfer across task identifiers.
2. **URL Resolution Failure:** 4/10 families (8 captures) failed due to `__SHOPPING__/path` placeholder not expanded. These families may have diverse product pages.
3. **Task Distribution Mismatch:** Prior positive control (EXP-INTEL-35749371101) used task-specific pages; this experiment captured homepage for 8/10 families.
4. **Pattern Grammar Limitation:** Longest-prefix on role:name tokens from identical DOM yields identical patterns by construction.

### Threats to H2
1. **DOM Drift Not Tested:** NC3_STAGEHAND_DOM_DRIFT requires single-attribute mutation test — not executed.
2. **Simulated Selector:** Selector `fam{id}_task{id}` not derived from actual page elements.
3. **No LLM Token Measurement:** tokens_saved estimated (1000/hit), not measured via actual LLM calls.
4. **Microsecond Latencies:** Cold vs cached latency measured in microseconds (cache dict lookup), not reflective of LLM call savings.

### General
- Playwright 1.44.0 used instead of 1.63.0 (browsergym-core 0.14.3 dependency)
- Gate0 census on single-page captures cannot compute conditional entropy or NL
- CAP 420-task, Mind2Web LFS, WebJudge-7B not attempted per Director SUPERSEDE

---

## 8. Product Consequences

### Negative (FALSIFIED-IN-SETTING for both H1 and H2)

1. **C-LLM-INHERIT within-store holdout remains blocked:** Longest-prefix element-pattern on homepage captures does not demonstrate identifiable same-mechanism parameterized transfer. The prior 0.9 single-family pass (task-specific pages) does not generalize to this measurement setting.

2. **Stagehand baseline incomplete:** While hit_rate=0.94 and isolation=0.0 are promising, the missing drift detection and speedup measurements mean the shipped Stagehand 2x/~30% baseline is not fully replicated on this substrate.

3. **Physics relaxed pilot not unblocked:** Relaxed Gate0 census 0/16 (single-page) does not inform feasibility of H>0.1 NL≥20 pilot. Multi-step trajectories needed.

4. **No exhaustive CAP/LFS search re-triggered:** Per Director SUPERSEDE, exhaustive enumeration remains ABANDONED. Next allocation should be orthogonal (BrowserGym loopback, hierarchical retrieval per Scout).

### Path Forward
- **For AX_consistency:** Resolve `__SHOPPING__/path` URLs to capture product/category/cart pages; test alternative pattern grammars (semantic, subtree, multi-anchor).
- **For Stagehand:** Execute DOM drift injection (NC3), measure cold vs cached LLM token costs, compare vs NC4 random null.
- **For Gate0:** Collect multi-step trajectories (browsergym rollouts) for meaningful H and NL computation.
- **For Physics:** Correlated-state FSM pilot on same families requires multi-step data first.

---

## 9. Artifact Index

All artifacts preserved with SHA256 hashes in `research/experiments/EXP-INTEL-35782546046/artifacts/`:

| Artifact | Path | SHA256 (truncated) | Role |
|----------|------|-------------------|------|
| WebArena Census | `raw/webarena_census.json` | `1923e6fa4e9c...` | raw |
| AX Captures | `raw/ax_captures.jsonl` | `0e022eb884b1...` | raw |
| AX Trees (16) | `raw/ax_trees/ax_fam*{task}.json` | various | raw |
| AX Consistency | `derived/ax_consistency.json` | `5be7e631f256...` | derived |
| Stagehand Replication | `derived/stagehand_replication.json` | `0c0b274f182c...` | derived |
| Gate0 Census | `derived/gate0_relaxed_table.json` | `091f7303d196...` | derived |
| Provenance | `derived/provenance.json` | `a2e327a22ea3...` | derived |
| Measurement Script | `research/intel/exp_35782546046_measure.py` | `dc47979e9896...` | code |

---

## 10. Handoff to Director

**Carry Forward (established):**
- WebArena-Verified v2 shopping substrate replicated: 192 tasks, 36 families ≥3, Docker accessible, CDP AX capture functional
- Stagehand selector+DOM-hash cache achieves high hit_rate (0.94) and perfect cross-project isolation on identical DOM
- AgentLab 0.4.2 + BrowserGym 0.14.3 + Playwright 1.44.0 + Chromium v1117 is a working substrate stack

**Rejected:**
- Longest-prefix element-pattern without fallback on homepage-only captures as evidence for parameterized transfer (FALSIFIED-IN-SETTING)
- Stagehand baseline as fully replicated without drift detection and speedup measurement (FALSIFIED-IN-SETTING)

**Unknown:**
- Whether product-page captures (resolving `__SHOPPING__/path`) yield discriminating AX_consistency
- Whether Stagehand drift detection achieves MISS≥0.8 on this substrate
- Whether multi-step trajectories yield relaxed Gate0 passes

**Do Not Assume:**
- That AX_consistency=1.0 on homepage implies parameterized transfer works on diverse pages
- That Stagehand 2x/~30% figure transfers without drift detection and LLM token measurement
- That 0/16 relaxed Gate0 on single-page implies relaxed pilot infeasible
- That CAP/LFS exhaustive search is required or productive (ABANDONED per Director)

**Recommended Action:** Director to allocate next intel pulse for (1) URL resolution fix to capture product pages, (2) Stagehand drift injection + LLM token measurement, (3) multi-step trajectory collection for Gate0, or PIVOT to orthogonal BrowserGym loopback/hierarchical retrieval per Scout.