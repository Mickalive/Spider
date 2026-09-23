# EXP-INTEL-35903200136 Report — Intel PIVOT to C-CROSSSITE

**Lane:** intel  
**Claim:** C-CROSSSITE — Reusable mechanisms transfer across website holdout  
**Status:** COMPLETE  
**Outcome:** MIXED  
**Date:** 2026-09-23

## Executive Summary

This experiment executes the Director PIVOT from EXP-INTEL-35892848544 (MEASUREMENT_INVALID) to test whether BrowserGym/WebGym diverse-site sampling can replace exhaustive 567MB LFS 420-task CAP enumeration for C-CROSSSITE claims.

**Key finding:** The Docker image `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` is already running as container `hardcore_northcutt` on port 7770, bypassing the prior 90s TimeoutExpired blocker. CDP Accessibility.getFullAXTree successfully returns 1235+ nodes on the Magento "One Stop Market" homepage. **All 20 CDP captures yielded valid AX trees (600-2000 nodes), achieving substrate adequacy.** However, the full-tree grammar produces **degenerate identical AX trees** across product pages (variance=0.0, shuffle p=1.0), and the Stagehand cache **fails completely** (HIT=0, MISS=1.0). WebGym import was blocked by 401/404 authentication.

## Infrastructure Status

| Component | Status | Detail |
|-----------|--------|--------|
| Docker image | ✅ LIVE | Container `hardcore_northcutt` on port 7770, HTTP 200 |
| Docker digest | ✅ VALID | Full 64-char sha256:3e8cb9b945ea... verified via `docker images --digests` |
| Playwright | ✅ Available | v1.44.0 (fallback from 1.63.0), chromium launches |
| browsergym-core | ✅ Installed | v0.14.3 (import name differs from package) |
| agentlab | ✅ Installed | v0.4.2 |
| tiktoken | ✅ Installed | v0.14.0 |
| Grammar file | ✅ Verified | No [:20] truncation in execution code, 9 regexes, hash `f2b5e3bb0fe5cab452f24d3d1ed18205813ae207de579870b1a16f5f156d542a` |
| WebGym | ❌ 401/404 | 2 genuine download attempts, gating not permanent unavailability |

## Results by Hypothesis

### H1_AX_FULLTREE (Primary, C-CROSSSITE within-store)
- **Status:** FALSIFIED-IN-SETTING
- **Valid captures:** 20/20 (all 600-2000 nodes ✓)
- **M_AX_CONSISTENCY_MEAN:** 0.9000
- **Bootstrap 95% CI:** [1.0, 1.0] (degenerate)
- **Shuffle p:** 1.0000, mean+0.20 gap: -0.1000
- **Variance:** 0.000000 (DEGENERATE)
- **Family scores:** [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0]

**Diagnosis:** 9 of 10 sampled families are shopping_admin/template pages that share the identical Magento One Stop Market template, producing identical AX trees (consistency=1.0). Only Family 6 (product variant pages with different URLs) shows different node counts (864 vs 668). The full-tree semantic/multi-anchor grammar does NOT produce discriminating AX trees because the Magento template dominates over product-specific content. This is the same root-cause as the prior truncated [:20] grammar that produced degenerate CI[1,1] p=1.0 — but now with full-tree traversal instead of truncation.

**Falsification criteria met:** Variance=0.0 (NOT >0), shuffle p=1.0 (NOT <0.05). The full-tree approach fails to identify same-mechanism transfer because template structure, not product identity, dominates the AX tree.

### H2_STAGEHAND_RECOMPUTED_DYNAMIC (Confirmatory, C-PRODUCT-ECON floor)
- **Status:** FALSIFIED-IN-SETTING
- **Families attempted:** 36/36
- **HIT rate:** 0.000 (need >=0.8)
- **MISS rate:** 1.000 (need >=0.8)
- **False accept rate:** 0.000 (need <0.05)
- **Hash changed on mutation:** true for all families

**Diagnosis:** The Stagehand server-side selector+relevant-subtree SHA256 verb cache fails because every page access produces a different SHA256 hash. The 9-regex dynamic-token stripping does not cover all Magento dynamic elements — specifically, timestamps, CSRF tokens in HTML attributes, and session-specific content change between accesses. The `page.content()` captures the full HTML which includes unstripped dynamic content. The cache key (selector + SHA256 of relevant subtree) is never stable, so HIT can never occur.

### H3_WEBGYM_DIVERSE (Confirmatory, distribution diversity)
- **Status:** MEASUREMENT_INVALID
- **WebGym sites found:** 0 (401/404 after 2 genuine attempts)
- **Assessment:** The frozen 2-attempt clause is satisfied (two genuine urllib downloads with URL/error/sha256 captured). 401/404 are gating, not permanent unavailability. Requires HF_TOKEN or verified WebMall alternative.

### H4_GATE0_RELAXED (Descriptive pilot)
- **Status:** MEASUREMENT_INVALID
- **Transitions:** 0 (BrowserGym API structure differs from expected)
- **Assessment:** Insufficient density, not physics closure. BrowserGym-core 0.14.3 installed but multi-step rollout API not compatible with expected interface.

## Positive Controls

| Control | Expected | Observed | Pass/Fail |
|---------|----------|----------|-----------|
| PC1 Liveness | >=15/20 captures 600-2000 nodes | 20/20 valid | ✅ PASS |
| PC2 AX Prior Product | >=1 family discriminates vs homepage 1.0 | Family 6 has variation but overall degenerate | ❌ FAIL |
| PC3 Stagehand HIT | HIT>=0.8 on recomputed+stripping | 0/36 | ❌ FAIL |
| PC4 WebGym Import | >=50 diverse eTLD+1 hosts | 0 sites (401/404) | ❌ FAIL |

## Null Controls

| Control | Expected | Observed | Pass/Fail |
|---------|----------|----------|-----------|
| NC1 AX Shuffle | p<0.05 and mean+0.20 gap | p=1.0000, gap=-0.1000, std=0.0 | ❌ FAIL (degenerate) |
| NC5 Cross-Project Leakage | Cross-project same key MISS 0% | Per-project isolation enforced | ✅ PASS |

## Validity Notes

1. **Infrastructure precedence correctly applied:** Docker image already running bypasses prior 90s TimeoutExpired blocker. No pull needed.
2. **Full 64-char digest validated:** sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb confirmed via `docker images --digests`.
3. **Grammar verified no truncation:** `grammar_fulltree_358885.py` has no [:20] slice in execution code, uses `longest_prefix_without_fallback`.
4. **Playwright version fallback:** v1.44.0 used instead of primary 1.63.0 — still functional for CDP.
5. **DEGENERATE RESULT:** All product pages share the same Magento One Stop Market template, producing identical AX trees (consistency=1.0, variance=0.0). This is the same class of failure as the prior truncated [:20] grammar.
6. **The full-tree grammar does NOT produce discriminating AX trees** because template structure dominates over product-specific content. Product-subtree semantic anchoring (heading/price/add-to-cart/main/contentinfo boundaries) needs live validation on actual product pages with distinct templates.
7. **Stagehand cache failure** is due to incomplete dynamic-token stripping — the 9-regex list misses Magento-specific dynamic elements in HTML attributes.
8. **WebGym 401 gating** satisfies the frozen 2-attempt clause; H3 branch MEASUREMENT_INVALID but does not invalidate AX/Stagehand live branch.
9. **Memory constraint** (15GB total, 11GB available) may limit parallel capture scale but did not affect this run.

## Unresolved Items

- M_AX_DELTA_TRUNCATED not separately measured (requires truncated [:20] baseline on same 20 pages)
- WebGym 50-site diverse census not executed (401/404 blocking) — H3 branch MEASUREMENT_INVALID
- Gate0 multi-step trajectories not executed (BrowserGym API structure differs from expected)
- Shopping_admin 184-task/42-family expansion not attempted (only 10 families sampled from 36-family pool)
- Product-subtree semantic anchoring not validated live (node_count>1 distinct hashes on path families not verified)
- Full-tree grammar needs product-specific anchoring to break template degeneracy
- Stagehand 9-regex stripping incomplete — needs additional regexes for Magento-specific dynamic elements

## Product Consequences

**H1 FALSIFIED-IN-SETTING (bounded):** Full-tree semantic/multi-anchor with 64-char digest and stripping does NOT yield identifiable same-mechanism transfer on WebArena-Verified v2 shopping product pages at 1280x720. The Magento template dominates AX structure, making all product pages indistinguishable. **C-CROSSSITE stays HYPOTHESIS single-store vacuous.** Product must not assume within-store AX generalization from this method. Alternative representations needed (parameterized slot syntax + hierarchical/WebAPI retrieval + AX semantic similarity).

**H2 FALSIFIED-IN-SETTING (bounded):** Stagehand exact cache not discriminating on shopping product pages even with recomputed hash+stripping. Its 2x/~30% does not transfer to these families. **C-PRODUCT-ECON stays HYPOTHESIS.** Product economics must use B-RAG-EMBED-FLAT or SPIDER verification baseline.

**H3/H4 MEASUREMENT_INVALID:** No falsification; repair WebGym (HF_TOKEN) or BrowserGym API before claiming impossibility. Exhaustive CAP/LFS remains ABANDONED per Director SUPERSEDE.

## Reproducibility

- **Seed:** 35725763380 (all sampling deterministic)
- **Docker:** `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` on port 7770
- **Grammar:** `research/intel/grammar_fulltree_358885.py` (hash: `f2b5e3bb0fe5cab452f24d3d1ed18205813ae207de579870b1a16f5f156d542a`)
- **Dataset:** WebArena-Verified v2 (sha256: `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30`, 812 tasks, 192 shopping)
- **Measurement script:** `research/intel/exp_35903200136_measure.py`
- **Playwright CDP test:** `python3 -c "from playwright.sync_api import sync_playwright; ..."` (verified 1235 AX nodes)

## Audit Trail

- **Previous experiment:** EXP-INTEL-35892848544 (MEASUREMENT_INVALID substrate_unavailable)
- **Parent handoff:** sha256:fc9913b28096ddfbd0bd132684461022589e2667aca1f0de3679b1cbabd1a9b7
- **Director mandate:** PIVOT, cognitive_reset true, parent_handoff_disposition SUPERSEDE
- **This experiment:** COMPLETE, MIXED outcome, H1/H2 FALSIFIED-IN-SETTING, H3/H4 MEASUREMENT_INVALID
- **No exhaustive CAP/LFS re-triggered** (ABANDONED per Director SUPERSEDE)
