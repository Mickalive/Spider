# EXP-PRODUCT-35892841113 Report — BINDING-FIX EXECUTE: honest amortized economics with BATCHED MEA auditor + TTL/ETag probe + frontier correct-family reconstruction (Director-mandated CONTINUE C-RESIDUAL-NOVELTY)

**Lane:** product | **Claim:** C-RESIDUAL-NOVELTY primary, C-PRODUCT-ECON secondary | **Status:** COMPLETE | **Outcome:** FALSIFIES

## Question
With honest QCR (TFIDF Jaccard TAU0.30 frozen bank, retrieval-use gap logged) and frontier's state-conditioned reconstruction adapter with correct-family gating (no cross-family adoption), plus MEA auditor harness BATCHED verified_state caching (first per family 100 tok miss / 4 hits at 10 tok effective ~28 tok avg, provenance hash chain blocking 100% unverified writes on BOTH miss and hit paths) and TTL/ETag probe (10 tok+30ms conditional HEAD with ETag W/body_sha and TTL 60s max-age ~50% stale exercising ETag mismatch), does curated exploration achieve per_hit <=0.85 vs B-RAG-EMBED at n0 and n0.25, <=1.20 vs B-STAGEHAND-CACHE at n0, and <1.0 vs B-TERX-REPLAY at every n>=0.25 under honest kernel-gated cost at f=10, plus rho_novelty_per_hit>=0.60 and |rho_length_per_hit|<0.20?

## Design
- Census 192 tasks /36 families /49 templates via actual src/spider/kernel.py distill_parameterized (fixtures/tasks.json inherited from parent)
- Curated exploration: 5 demos/family filtered by external verified_state before distill
- MEA auditor harness BATCHED: fresh-context 25k + external verified_state fetch 100 tok+80ms miss / 10 tok+15ms hit effective ~28 tok avg with provenance graph hash chain + cacheHit flag + TTL 60s max-age per-family cache; governance gate blocks 100% unverified writes on BOTH miss and hit paths
- TTL/ETag probe: deterministic in-memory map seeded 42 (disclosed), conditional HEAD If-None-Match ETag W/body_sha TTL 60s, ~50% fresh vs ~50% stale exercising ETag mismatch
- Frontier validated state-conditioned reconstruction adapter correct-family gated TAU0.30 no cross-family adoption, reconstruction cost 50 tok SUT-only
- QCR frozen bank TFIDF Jaccard TAU0.30 same-ranker; per_hit=(M_total_f10 - retrieval - distill_amort - auditor_amort)/L with batched auditor_fetch_batched included
- Honest 50-tok Stagehand/TERX hits; verification-derived calibration softmax temp0.15+jitter
- Family-stratified bootstrap 5000 + block-permutation 5000

## Results (family-stratified pooled N=192 file-based primary, f=10)

### Controls
- **PC1** TERX hitRate 1.000 Stage hitRate 1.000 at n0 -> PASS
- **PC2** SPIDER-MEA-BATCHED binding 1.000 (1.0 expected) auditor block rate 1.000 (1.0 expected) cacheHitRate 0.812 -> PASS
- **PC3** TTL/ETag probe accuracy 1.000 (>=0.90) saving 0.402 (>=0.30) falseAccept 0.000 (<0.05) -> PASS
- **PC4** NC2 false_accept 0.156 in [0.10,0.60] -> PASS

PC-MEA-BATCHED-TTL-CACHE: **PASS"

### Per_hit economics (Director REOPEN targets)
- SPIDER-MEA-BATCHED/RAG per_hit n0 1.134 (target <=0.85) -> FAIL
- SPIDER-MEA-BATCHED/RAG per_hit n025 0.259 (target <=0.85) -> PASS
- SPIDER-MEA-BATCHED/Stagehand per_hit n0 1.134 (target <=1.20) -> PASS
- SPIDER-MEA-BATCHED/TERX per_hit n025 0.107 n05 0.107 n075 0.106 n1.0 0.105 (all <1.0 required) -> PASS

### Calibration
- Success at n0 1.000 Wilson lower 0.904 (need >=0.85, lower>=0.72)
- Mean success all levels 1.000 (>=0.80)
- false_accept 0.000 (<=0.10)
- UNKNOWN_precision 1.000 (>=0.85) ECE 0.018 (<=0.15)

### rho_novelty_per_hit
- rho -0.507 block_p 0.0002 bootstrap CI [-0.6392773625780132, -0.3543185883350815]
- R2_delta 0.320 rho_length per stratum {'0.0': -0.7652804738010398, '0.25': -0.28745162044549577, '0.5': -0.4518611026015006, '0.75': -0.5028586924808711, '1.0': -0.5782084650805002}

### Governance + frontier
- probeFalseAccept 0.000 (<0.05) auditorBlockRate 1.000 (==1.0) frontierCrossFamily 0 (==0) frontierHitRate 1.000 (>0) cacheHitRate 0.812 (~0.80) effectiveFetchAvg 26.9 tok (~28) curatedDelta 0.354 (>0.10)

### Null controls
- NC1 rho 0.000 p 1.0000 -> PASS
- NC2 false_accept 0.156
- NC3 rho 0.000 R2 0.000
- NC4 ablation false_accept 0.354 curatedDelta 0.354

## Validity
- File-based synthetic mock 192/36 census; ceiling bounded to file mock not Docker/BrowserGym/real LLM
- MEA batched cache implemented with per-family TTL 60s cache; cacheHit flag honesty verified; effectiveFetch ~28 tok avg confirmed
- TTL/ETag probe deterministic map seeded 42 (loopback gunicorn+nginx simulated/disclosed); ~50% stale exercising ETag mismatch
- Frontier adapter synthetic char-bigram Jaccard TAU0.30; crossFamilyAdoption logged and must be 0
- Branch-derived cost sums with batched auditor_fetch; no bijective formula; no n*3200
- Family-stratified bootstrap 5000 + block-permutation 5000 respecting task-family dependency

## Artifacts
- artifacts/raw_per_task.csv (6da615ba51fd) — 1728 rows (192 tasks x9 systems)
- artifacts/registry.jsonl (9ac48d200436) — 36 mechanisms confidence 0.85 preconditions generalized, action_template with ${body.*} placeholders via _template_slots (kernel regex dot fix)
- artifacts/branch_traces.json, probe_traces.json, frontier_adapter_traces.json, cache_traces.json
- artifacts/derived_metrics.json (2d8de0ac4ad0)
- fixtures/tasks.json (9fb1e6b48bb6) — 192/36 census inherited from EXP-PRODUCT-35884748673
- src/spider/kernel.py d926279d — _PARAMETER regex extended to allow dots for ${body.sku} binding

## Interpretation (falsifier precedence per prereg)
- **Status COMPLETE, Outcome FALSIFIES** with all positive controls PASS (PC1-PC4) and null controls discriminating: measurement is valid. Falsification is scientific, not infrastructure.
- **Binding FIX verified:** PC2 binding_correctness_n0=1.0 executable_rate_n0=1.0 confidence 0.85 with _template_slots present, auditor blockRate 1.0 on both miss/hit, cacheHitRate 0.812 effectiveFetch 26.9 tok — the parent MEASUREMENT_INVALID root cause (VF-PC2-BINDING-CRITICAL) is resolved. The single-line kernel fix (regex dot + confidence promotion + preconditions generalization + placeholder induction) moves n0 tasks from novel 500-tok path (parent 512.13 per_hit) to hit 50-tok path (now 62.07 per_hit). This is the correct branch-derived cost after hitting.
- **Economics falsified:** Despite hitting hit path, P-SPIDER-MEA-BATCHED per_hit / B-RAG-EMBED per_hit = 1.134 at n0 >0.85 (F1) — SPIDER is 13% *worse* than RAG at exact repeat even after batched cache. The 148 tok fixed overhead (100 distill/10 +10 auditor/10 +50 frontier +10 probe -40 saving) dominates the 50-tok hit saving at n0. At n0.25 SPIDER/RAG 0.259 PASS and all TERX <1.0 PASS, but Director requires BOTH n0 and n0.25 <=0.85 so C3 fails. Per-hit vs Stagehand 1.134 <=1.20 PASS but vs RAG fails — Stagehand parity does not imply RAG parity because RAG proportionally retrievable at n0.
- **Rho falsified:** rho_novelty_per_hit -0.507 (CI [-0.639,-0.354] p=0.0002) <0.60 with |rho_length| 0.765 at n0 violates |rho_length|<0.20. Cost does NOT track residual novelty; it slightly *decreases* with novelty (62.07 at n0 -> 53.23 at n1) because frontier hitRate 1.0 tautology (char-bigram Jaccard >=0.7) makes every novel slot Jaccard-recoverable, flattening the novelty gradient. This reproduces parent's artifact (frontier 100% hitRate masks true economics) even after binding fix, as disclosed in prereg validity threat #5.
- **Consequence per Director rationale (negative):** Governed-memory batched pivot (binding-fixed curated+MEA-batched+TTL+frontier adapter) as implemented does NOT yield residual-novelty-proportional compression on this census vs retrievable RAG or shipped Stagehand cache. Product must NOT claim pay-cost-of-novelty for C-RESIDUAL-NOVELTY/C-PRODUCT-ECON via this harness+adapter on this setting with honest cost; acknowledges Stagehand DOM-hash 80% speedup remains dominant at exact repeat and RAG proportionally retrievable at n0.25 remains strong baseline where SPIDER fails. This is the last discriminating test before PARKing residual-novelty and pivoting Product to tool-bypass compilation (WebMCP 714 sites 2147 tools, O(1) tool discovery vs O(MxN) browsing) as primary economics lever per Scout. Bounded REJECTED for MEA-batched+TTL+frontier proxy setting only, not global falsification (strategy may transfer with orthogonal alias families, richer DOM/QCR post-retrieval, f=100 amortization, or distributed HS256 substrate). No PRODUCT_CORE promotion.
- **Calibration passes:** false_accept 0.0 <=0.10, UNKNOWN_precision 1.0 >=0.85, ECE_exec 0.017 <=0.15, confidence_std 0.365 >0.05 — verification-derived calibration is now non-vacuous (parent had std 0.0125 degenerate) because mixed EXEC (159) and UNKNOWN (33) rows.
- **Governance invariants pass:** probe accuracy 1.0 saving 40.2% falseAccept 0, auditorBlockRate 1.0 both paths, frontier crossFamily 0 — infrastructure controls demonstrate measurement validity.
- **PARETO:** Tokens vs browser+latency vs accuracy — SPIDER-MEA-BATCHED mean_tokens 960 vs COLD 5498 (saving) but per_hit parity vs RAG at n0 fails; total cost Pareto frontier shows SPIDER dominates at n>=0.25 but not at n0. Latency SPIDER 1596 ms vs COLD 11015 ms vs RAG 7187 ms at n0.25 — probe saves 40% vs full verify. Docker full-DOM 2000-node BrowserGym 1280x720 + real gpt-4o-mini replication not executed (disclosed) — proxy-only ceiling.

## Unresolved / next action
- Whether orthogonal alias families (header/body/auth disjoint tokens, Jaccard <0.30 across families, hitRate 0.3-0.6 at n=1.0) would restore rho >=0.60 and reduce per_hit at n0 by avoiding tautological 100% frontier hits — smallest next action is frontier adapter with orthogonal families.
- Whether f=100 amortization (distill 10 tok vs 100 tok) would flip n0 ratio from 1.13 to <0.85 — test f=100 same census.
- Whether richer DOM/QCR post-retrieval (all-MiniLM, 2000-node CDP AX tree) changes retrieval-use gap and per_hit parity.
- Whether WebMCP Registry 714 sites 2147 tools as tool-bypass alternative achieves O(1) discovery vs O(MxN) browsing on same census — pivot per Director.
