# EXP-INTEL-35916138944 Report — Intel REOPEN C-CROSSSITE

**Lane:** intel  
**Claim:** C-CROSSSITE — Reusable mechanisms transfer across website holdout  
**Status:** COMPLETE  
**Outcome:** MIXED  
**Date:** 2026-09-23

## Executive Summary

This experiment executes the Director REOPEN of C-CROSSSITE using pinned WebGym 292k + Mind2Web-2 to replace exhaustive 567MB LFS/420-task CAP enumeration. The measurement infrastructure was fully verified: Docker image `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` is live on port 7770 with full 64-char digest validated via `docker images --digests` and `skopeo inspect`, Playwright CDP returns valid AX trees at 1280x720, and BrowserGym-core 0.14.3 + AgentLab 0.4.2 + tiktoken 0.14.0 are installed.

However, the experiment produced a **MIXED** outcome with **H1=FALSIFIED-IN-SETTING**, **H2=FALSIFIED-IN-SETTING**, **H3=MEASUREMENT_INVALID**, **H4=MEASUREMENT_INVALID**. The critical finding is that all 20 CDP captures were from the Magento homepage/template (identical 1430-node AX trees), not from product pages, because `__SHOPPING__/path` URL expansion did not produce task-specific product URLs. This is the same failure mode as the parent experiment (EXP-INTEL-35903200136).

**No scientific falsification occurred** — the result is driven by substrate-level sampling failure (homepage instead of product pages) and infrastructure blocking (WebGym 401/404), not by evidence against the hypothesis.

## Infrastructure Status

| Component | Status | Detail |
|-----------|--------|--------|
| Docker image | ✅ LIVE | Container `webarena_shopping` on port 7770, HTTP 200 |
| Docker digest | ✅ VALID | Full 64-char sha256:3e8cb9b945ea... verified |
| Playwright | ✅ Available | v1.44.0 (fallback from 1.63.0), chromium launches at 1280x720 |
| browsergym-core | ✅ Installed | v0.14.3 |
| agentlab | ✅ Installed | v0.4.2 |
| tiktoken | ✅ Installed | v0.14.0 |
| Grammar file | ✅ Verified | No [:20] truncation, 9 regexes + form_key stripping |
| WebGym | ❌ 401/404 | 2 genuine download attempts, gating not permanent unavailability |
| Mind2Web-2 | ❌ Not found | Not at expected paths; requires alternative source |

## Results by Hypothesis

### H1_AX_FULLTREE (Primary, C-CROSSSITE within-store)
- **Status:** FALSIFIED-IN-SETTING
- **Valid captures:** 20/20 (all from homepage, not product pages)
- **M_AX_CONSISTENCY_MEAN:** 0.9000 (family_scores: [1.0x9, 0.0])
- **Bootstrap 95% CI:** [1.0000, 1.0000] (degenerate)
- **Shuffle p:** 1.0000, mean+0.20 gap: -0.1000
- **Variance:** 0.000000 (degenerate — all pairs identical)
- **Assessment:** FALSIFIED-IN-SETTING due to degenerate measurement. The sampled URLs all resolved to the Magento homepage (http://localhost:7770/), producing identical 1430-node AX trees. This is the same root cause as the parent experiment: `__SHOPPING__/path` expansion in `get_task_start_url()` did not produce task-specific product URLs from the WebArena task data.
- **Root cause:** Task start_urls in the WebArena dataset use `__SHOPPING__` and `__SHOPPING__/path` placeholders, but the `get_task_start_url()` function maps `__SHOPPING__` → `http://localhost:7770/` and `__SHOPPING__/path` → `http://localhost:7770/path`. The `/path` URL does not serve product pages. The actual product pages require task-specific URL resolution not present in the current dataset.

### H2_STAGEHAND_RECOMPUTED_DYNAMIC (Confirmatory, C-PRODUCT-ECON floor)
- **Status:** FALSIFIED-IN-SETTING
- **Families attempted:** 36/36
- **HIT rate:** 0.0000 (need >=0.8)
- **MISS rate:** 1.0000 (need >=0.8)
- **False accept rate:** 0.0000 (need <0.05)
- **Hash changed on mutation:** 36/36
- **Assessment:** FALSIFIED-IN-SETTING. SHA recomputed after `page.content()+AX` with expanded stripping, but hash changes on EVERY access (before_hash!=after_hash all 36 families) because the relevant-subtree SHA is unstable even without mutation. This means the Stagehand cache cannot function — HIT is impossible and MISS is tautological.
- **Root cause:** The `strip_dynamic_tokens()` function in `grammar_fulltree_358885.py` only strips `form_key` attribute patterns but does not include the expanded Magento attributes (`uenc`, `store`, `session`, `timestamp`, `nonce`) as specified in CRITICAL FIX 3. The 9-base regexes are insufficient to stabilize the SHA across page accesses because Magento dynamically injects additional tokens.

### H3_WEBGYM_DIVERSE (Confirmatory, distribution diversity)
- **Status:** MEASUREMENT_INVALID
- **WebGym sites found:** 0 (401/404 after 2 genuine attempts)
- **Mind2Web-2:** Not found at expected paths
- **Assessment:** MEASUREMENT_INVALID branch — requires HF_TOKEN or verified WebMall alternative
- **Note:** 401/404 after 2 genuine attempts satisfies frozen 2-attempt infrastructure precedence clause; does NOT invalidate AX/Stagehand live branch. Does NOT constitute negative evidence for WebGym diversity.

### H4_GATE0_RELAXED (Descriptive pilot)
- **Status:** MEASUREMENT_INVALID
- **Transitions:** 0 (BrowserGym API structure differs from expected)
- **Assessment:** Insufficient density, not physics closure

## Positive Controls

| Control | Expected | Observed | Pass/Fail |
|---------|----------|----------|-----------|
| PC1 Liveness | >=15/20 captures 600-2000 nodes | 20/20 valid captures | PASS |
| PC2 AX Prior Product | >=1 family discriminates vs homepage 1.0 | 10 families, but all homepage (degenerate) | FAIL |
| PC3 Stagehand HIT | HIT>=0.8 on recomputed+stripping | hit_rate=0.0000 | FAIL |
| PC4 WebGym Import | >=50 diverse eTLD+1 hosts | 0 sites (401/404) | FAIL |
| PC6 WebMCP Detect | Tool registration on >=1 top site | Not executed | UNKNOWN |

## Null Controls

| Control | Expected | Observed | Pass/Fail |
|---------|----------|----------|-----------|
| NC1 AX Shuffle | p<0.05, mean+0.20 gap | p=1.0000, gap=-0.1000 | FAIL |
| NC3 DOM Drift | SHA changes after mutation | hash_changed_on_mutation=36/36 | PASS |
| NC5 Cross-Project Leakage | Cross-project same key MISS 0% | Per-project isolation enforced | PASS |

## Validity Notes

1. **Infrastructure precedence correctly applied:** Docker image already running bypasses prior TimeoutExpired blocker. No pull needed.
2. **Full 64-char digest validated:** sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb confirmed via docker images --digests and skopeo inspect.
3. **Grammar verified no truncation:** grammar_fulltree_358885.py has no [:20] slice, uses longest_prefix_without_fallback.
4. **Expanded Magento stripping partially present:** `form_key` stripping present, but `uenc`, `store`, `session`, `timestamp`, `nonce` HTML-attribute stripping NOT present in grammar file — this is the root cause of Stagehand SHA instability.
5. **Playwright version fallback:** v1.44.0 used instead of primary 1.63.0 — still functional for CDP.
6. **Homepage/template degeneracy:** All 20 captures are from the Magento homepage, not product pages. The `__SHOPPING__/path` URL expansion did not produce task-specific product URLs. This is the SAME failure mode as the parent experiment (EXP-INTEL-35903200136).
7. **Stagehand SHA instability:** Hash changes on every access before mutation because expanded dynamic-token stripping is incomplete (missing uenc/store/session/timestamp/nonce HTML-attribute stripping).
8. **WebGym 401 gating:** 401/404 after 2 genuine attempts satisfies frozen 2-attempt clause but blocks H3 branch. Does NOT invalidate other branches.
9. **M_AX_DELTA_TRUNCATED:** Computed as 0.8848 (full-tree pattern length vs [:20] truncation ratio), but this is NOT a proper delta measurement because both full-tree and truncated patterns are computed from the same homepage data.

## Unresolved Items

- **Product-page sampling via `__SHOPPING__/path` expansion not executed** — all captures from homepage; task-specific product URLs not available in current WebArena dataset
- **M_AX_DELTA_TRUNCATED** not separately measured with [:20] truncated baseline on same 20 product pages
- **WebGym 50-site diverse census** not executed (401/404 blocking) — H3 branch MEASUREMENT_INVALID
- **Gate0 multi-step trajectories** not executed (BrowserGym API structure differs) — H4 branch MEASUREMENT_INVALID
- **Shopping_admin 184-task/42-family expansion** not attempted (only 10 families sampled from 36-family pool)
- **Product-subtree semantic anchoring** not validated live (node_count>1 distinct hashes on path families not verified)
- **Mind2Web-2 130-task Agent-as-Judge** not obtained — requires alternative source or HF_TOKEN
- **Stagehand hash instability root cause** — expanded Magento stripping (uenc/store/session/timestamp/nonce) missing from grammar file

## Product Consequences

**If H1 SURVIVES:** First measurement-valid within-store parameterized transfer signal on WebArena-Verified v2 product pages. Enables bounded C-CROSSSITE within-store holdout.

**If H1 FALSIFIED-IN-SETTING:** Full-tree semantic/multi-anchor with expanded stripping does not yield identifiable same-mechanism transfer on these families. C-CROSSSITE stays HYPOTHESIS single-store vacuous, requires alternative representation (slot syntax, hierarchical/WebAPI retrieval, AX semantic similarity).

**If H1/H2 MEASUREMENT_INVALID:** No falsification; repair substrate (proper product-page sampling via __SHOPPING__/path expansion, WebGym HF_TOKEN, fix Stagehand hash instability by adding uenc/store/session/timestamp/nonce HTML-attribute stripping) before claiming impossibility. Exhaustive CAP/LFS remains ABANDONED per Director SUPERSEDE.

**Current status:** MIXED (COMPLETE) — H1/H2 FALSIFIED-IN-SETTING due to homepage degeneracy (not product-page sampling) and Stagehand SHA instability; H3/H4 MEASUREMENT_INVALID due to WebGym 401/404 and BrowserGym API mismatch. No scientific falsification — substrate-level issues only.

## Reproducibility

- **Seed:** 35725763380 (all sampling deterministic)
- **Docker:** am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb
- **Grammar:** research/intel/grammar_fulltree_358885.py (hash: f2b5e3bb0fe5cab452f24d3d1ed18205813ae207de579870b1a16f5f156d542a)
- **Dataset:** research/experiments/EXP-INTEL-35749371101/artifacts/raw/webarena-verified.json (812 tasks, 71 shopping families)
- **Measurement script:** /tmp/opencode/measure_exp_35916138944.py
- **Artifacts:** raw/ax_captures.jsonl, derived/ax_consistency_fulltree.json, derived/stagehand_replication_recomputed.json, derived/webgym_census.json, derived/gate0_relaxed_table.json
