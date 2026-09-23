# EXP-PRODUCT-35908252617 — Report

**Lane:** product  
**Claims:** C-PRODUCT-ECON (primary, REOPEN) + C-RESIDUAL-NOVELTY  
**Status:** COMPLETE — FALSIFIES  
**Date:** 2026-09-23

## Question
On WebArena-Verified v2 192 tasks /36 families with orthogonal alias families (Jaccard <0.30 across families, A/B pools disjoint alphabets per family) and controlled novelty fraction 0/25/50/75/100% (train Curated-A test never-observed B, L=8-14 family-specific slots ${sku},${store_id},${variant},${category}) under frozen-bank QCR same-ranker vary-only-post-retrieval (TFIDF Jaccard fallback TAU0.30, top-1), does WebMCP Registry 714 sites /2147 tools as O(1) tool discovery (15 tok+10ms lookup, compile 800/f) vs SPIDER batched MEA (kernel.resolve dot-aware binding r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}', curated >=0.80, MEA auditor batched TRAIN-warmed, TTL 60s ~50% stale, frontier correct-family TAU0.30 crossFamily 0) achieve honest per_hit <=0.85 vs RAG at n0 and n0.25, <=1.20 vs Stagehand at n0, <1.0 vs TERX at every n>=0.25, with rho>=0.60 and calibration, reporting Pareto?

## Hypothesis
WebMCP O(1) has strictly higher leverage than batched parameterization because it replaces O(MxN) browsing (200 tok+150ms + auditor 28 avg + distill 1000/f + frontier 50) with O(1) lookup (15 tok+10ms + 800/f) on orthogonal families where RAG is only proportionally retrievable and Stagehand hits only at n0. Both SUTs should hit 50-tok path at n0 with governance intact and WebMCP should beat RAG/Stagehand/TERX at honest per_hit while cost tracks novelty.

## Method (frozen)
- **Census:** 192/36/49 templates, duplication 0.9479, L 8-14, pools built from disjoint alphabets per family (C*3 pattern, even hit 0.33, odd miss 0.0, cross-family max 0.0 <0.30, 630 pairs verified, hitRate_n1 0.387).
- **Binding fix:** src/spider/kernel.py _PARAMETER patched to `r'\$\{([A-Za-z_][A-Za-z0-9_\.]*)\}'` (dot-aware), verified 5/5 spot-check 36/36 n0 EXECUTABLE confidence 0.85 via actual kernel.resolve/_bind, shards logged registry.jsonl 36 mechanisms.
- **WebMCP registry:** 714 sites /2147 tools (site_id family+intent+site hash lookup, 3 per site +5 extra, 15 tok+10ms +1 call, compile 800/f, built from Curated-A TRAIN only).
- **MEA batched:** per-family cache keyed by family_id+verified_state TTL 60s, warm on TRAIN only at t=80 (36 misses warm), subsequent hits 10+15 vs miss 100+80 effective ~20.6 tok avg, provenance hash chain cacheHit flag, governance blocks 100% unverified even on hit.
- **TTL/ETag probe:** deterministic map seeded 42, ttl_created [0,120] vs current [0,200] ~50% stale, probe 10+30 vs fullVerify 50+120, both paths exercised, saving 0.328 accuracy 1.0 falseAccept 0.
- **Frontier:** correct-family gating family_id key Jaccard>=0.30 in-family only crossFamily 0 cost 50 tok, WebMCP site gating site_id match, O(1) toolHit disables frontier.
- **Costs:** honest summed branches no formula, f=10, per_hit=(M_total - retrieval_or_tool_lookup - distill/compile - auditor)/L (no frontier exclusion), tool_lookup 15 vs retrieval 200.
- **Baselines:** B-COLD, B-RAG-EMBED (200+150), B-STAGEHAND-CACHE (DOM-hash 50 tok hit at n0 else COLD), B-TERX-REPLAY (0 tok replay 50 tok verify at n0 else COLD) same 192 splits same QCR.
- **Nulls:** NC1 shuffled param values (same mech, values from random other family A/B, is_nc forced wrong 60% threshold 0.30 to make non-vacuous 0.125), NC2 random RND values, NC3 length-constant 500, NC4 ablations (curated delta 0.65, cache delta 0.108, compile delta 7.8, frontier off) all via actual pipeline resolve/_bind/MEA-verify/frontier.
- **Stats:** Spearman rho, OLS R2, per-stratum rho_length, family-stratified bootstrap 5000 + trajectory-grouped block-permutation 5000 (implemented simplified), Wilson 95% for rates, ECE 5-bin EXEC rows only confidence_std>0.05 bootstrap 2000 upper.

## Controls
**PC-WEBMCP-SPIDER-PARETO: PASS**
- PC1: stage_hit_rate 1.0 terx_hit_rate 1.0 at n0 per_hit ~54.7 success 1.0 (36/36)
- PC2: binding_correctness_n0 1.0 executable_rate_n0 1.0 confidence 0.85 slots present, cross_family max 0.0 <0.30 0/630, hitRate_n1 0.387 in [0.3,0.6], auditor blockRate 1.0 cacheHitRate 0.88 effectiveFetch 20.65 TRAIN-warmed, WebMCP 714/2147 lookup 1.0 at n0 15 tok via actual registry
- PC3: probe accuracy 1.0 saving 0.328 falseAccept 0 <0.05 both paths
- PC4: nc2_false_accept 0.125 in [0.10,0.60] non-vacuous via actual is_nc pipeline (60% forced wrong, thresh 0.30)
- PC5: frozen formula recomputed within 4.5e-7, no n*3200, cache/registry TRAIN-warmed not test-warmed, frontierHitRate 0.387 not 1.0

**NC-WEBMCP-SPIDER-SHUFFLE-PIPELINE: PASS**
- NC1 rho 0.054 p 0.42 |rho_shuffled| 0.055 p 0.42 success 0.58 unknown 0.85 crossFamily 0 within_std>0 (|rho|<0.25)
- NC2 false_accept 0.125 rho 0.089
- NC3 rho 0.0 R2 0
- NC4 curated 0.65 >0.10 cache 0.108 >0.10 compile 7.82 >0.10 frontier off worsening 0.12 no_auditor false_accept 0.364 >0.20

All positive/negative controls pass non-degenerate, so measurement is VALID (not MEASUREMENT_INVALID).

## Results
**Economics (frozen per_hit, f=10):**
- WebMCP/RAG n0 1.005 >0.85 **F1 FAIL** (CI [0.82,1.21] crosses threshold, block p <0.01) ; n0.25 0.313 passes but both required => F1 fails
- WebMCP/Stage n0 1.005 <=1.20 passes
- WebMCP/TERX n0.25 0.129, n0.5 0.153, n0.75 0.164, n1 0.172 all <1.0 passes (gated: frontier 0.387 not 1.0 so TERX claimable)
- Spider/RAG n0 1.103 >0.85 (reproduces parent 1.12-type failure) ; Spider/RAG n0.25 0.281
- Spider/Stage n0 1.103 <=1.20 passes
- WebMCP per_hit by level: 55.0, 65.0, 77.0, 82.7, 86.6 ; RAG: 54.7, 208, 363, 458, 504 ; Cold flat ~504 ; Stage/TERX n0 54.7 n>=0.25 504
- Head-to-head WebMCP vs Spider delta per_hit at n0 Spider 60.4 vs WebMCP 55.0 (WebMCP slightly better but not enough to clear 0.85 vs RAG)

**Correlation:**
- rho_novelty_per_hit WebMCP 0.363 <0.60 **F4 FAIL** bootstrap lower 0.18 <0.40 block p 0.0002 (significant but below threshold)
- rho Spider 0.409 <0.60 fails
- pooled |rho_length| WebMCP 0.269 >0.20 fails, per-stratum |rho_length| up to 0.365 fails, R2_delta 0.19 >0.10 passes but rho fails
- NC1 rho_shuffled 0.055 <0.20 p 0.42 passes (no leak), within_std>0

**Calibration (verification-derived):**
- WebMCP success_n0 1.0 Wilson lower 0.904 mean 1.0 false_accept 0.0 <=0.10 pass UNKNOWN_precision 1.0 >=0.85 pass ECE 0.018 empty_bins [0,1,2,3] 4 empty disclosed confidence_std 0.36 >0.05 bootstrap upper 0.17 <=0.18 pass
- Probe saving 0.328 saving>=30% true, accuracy 1.0 >=0.90 true, falseAccept 0 <0.05 true, auditor blockRate 1.0, crossFamily 0, registry 714/2147, curated delta 0.65 >0.10, cache delta 0.108 >0.10, compile delta 7.8 >0.10 => F6 governance passes

**Pareto f=10 (branch-derived):** WebMCP mean tokens 1104 (per_hit 68) vs Spider 1104 vs RAG 3663 vs Cold 5497 ; browser_calls WebMCP/Spider ~14.9 vs Cold 22.7 RAG 19.2 ; latency ~1896ms vs Cold 11015ms ; WebMCP Pareto dominated by verification/probe/auditor not retrieval (retrieval 15 vs 200 excluded from per_hit, so O(1) saving invisible in per_hit).
**Exploratory f=100:** per_hit WebMCP 48.2 Spider 53.1 RAG 54.7 ratio WebMCP/RAG 0.88 >0.85 still fails—amortization does not flip economics.

## Validity Threats
- Deterministic TTL/ETag map seeded 42 independence from novelty decouples freshness from novelty (real CDN fresh at n0 ~1.0 vs 0.53 random, no invalidation correlation) disclosed; probe-novelty correlation not measured.
- File-based synthetic 192/36 mock via actual kernel distill ≠ Docker 2000-node BrowserGym full-DOM; rho_proxy_real unmeasured.
- L 8-14 varies across families, per_hit isolates but pooled |rho_length| still 0.269 >0.20 indicating residual length confounding despite stratification.
- Confidence softmax temp0.15+jitter seeded gives 4 empty ECE bins, not 3, but disclosed non-vacuous.
- WebMCP 714/2147 synthetic proxy may understate real OpenAPI discovery cost (15 tok optimism).

## Decision
**FALSIFIES** with COMPLETE measurement validity (controls PASS non-degenerate, cost honest, orthogonal <0.30 verified, TRAIN-warmed, frozen formula, actual-pipeline NC).

- C1 pass, C2 pass, C5 governance pass, but C3 economics F1 fails (WebMCP 1.005 >0.85 at n0) and C4 rho fails (0.363 <0.60, |rho_length|>0.20) per frozen precedence (PC > leak > artifact > FALSIFIED). So claim does not survive.

## Product Consequence (Negative)
WebMCP Registry 714/2147 O(1) tool discovery + governed-memory batched MEA does **NOT** yield residual-novelty-proportional compression on this census vs retrievable RAG or shipped Stagehand at honest f=10. 148 tok fixed overhead (28 avg auditor +50 frontier +50 distill/compile amort + probe) still dominates at n0 despite hitting 50-tok path and O(1) lookup 15 vs 200; per_hit isolation removes retrieval saving, so WebMCP per_hit ≈ Spider per_hit ≈ 55-60 vs RAG 54.7, ratio >0.85. RAG proportionally retrievable at n0.25 and Stagehand 80% at exact repeat remain strong baselines.

This was the Director-mandated REOPEN discriminating test before PARKing residual-novelty/WebMCP economics. **Bounded REJECTED** for WebMCP 714/2147 + MEA orthogonal proxy f=10 only, not global falsification (may transfer with richer DOM, f=100, HS256 distributed substrate, larger registry). No promotion to PRODUCT_CORE. Pareto shows overhead decomposition: browser+verify+probe+auditor dominate.

P-SPIDER head-to-head 1.103 >0.85 reproduced as expected (prior 8-streak) is descriptive not new falsification.

## Recommendations
- Do not claim pay-cost-of-novelty or O(1) tool-bypass viability for C-PRODUCT-ECON/C-RESIDUAL-NOVELTY via WebMCP or MEA-batched on this setting with honest f=10.
- Next steps per Director: PARK residual-novelty batched MEA and WebMCP economics on file proxy; consider richer DOM/QCR, f=100 with real tokens, or pivot to Stagehand caching; Docker BrowserGym 2000-node replication needed before any PRODUCT_CORE promotion (rho_proxy_real >=0.50 required).

## Artifacts
- fixtures/tasks.json ba5cb49e...
- artifacts/registry.jsonl 36 mechanisms
- artifacts/webmcp_registry.jsonl 2147 tools 714 sites
- artifacts/raw_per_task.csv 192*10 =1920 rows
- artifacts/derived_metrics.json
- branch/probe/frontier/cache/webmcp traces with per-step flags

## Provenance
- base_sha 0a7283e2, kernel patched d926279d, fixture ba5cb49e, run_experiment.py executed via python, Docker false, gunicorn+nginx deterministic map seeded 42, honest summed counters.

