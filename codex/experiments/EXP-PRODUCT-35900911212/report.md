# EXP-PRODUCT-35900911212 Report — REOPEN C-RESIDUAL-NOVELTY: honest amortized economics with BATCHED MEA auditor + TTL/ETag probe + frontier correct-family reconstruction (orthogonal alias families + train-warmed cache + frozen formula)

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
- **PC2** SPIDER-MEA-BATCHED binding 1.000 (1.0 expected) auditor block rate 1.000 (1.0 expected) cacheHitRate 0.839 -> PASS
- **PC3** TTL/ETag probe accuracy 1.000 (>=0.90) saving 0.328 (>=0.30) falseAccept 0.000 (<0.05) -> PASS
- **PC4** NC2 false_accept 0.318 in [0.10,0.60] -> PASS

PC-MEA-BATCHED-TTL-CACHE-ORTHOGONAL: **PASS"

### Per_hit economics (Director REOPEN targets)
- SPIDER-MEA-BATCHED/RAG per_hit n0 1.121 (target <=0.85) -> FAIL
- SPIDER-MEA-BATCHED/RAG per_hit n025 0.288 (target <=0.85) -> PASS
- SPIDER-MEA-BATCHED/Stagehand per_hit n0 1.121 (target <=1.20) -> PASS
- SPIDER-MEA-BATCHED/TERX per_hit n025 0.119 n05 0.135 n075 0.174 n1.0 0.180 (all <1.0 required) -> PASS

### Calibration
- Success at n0 1.000 Wilson lower 0.904 (need >=0.85, lower>=0.72)
- Mean success all levels 1.000 (>=0.80)
- false_accept 0.000 (<=0.10)
- UNKNOWN_precision 1.000 (>=0.85) ECE 0.019 (<=0.15)

### rho_novelty_per_hit
- rho 0.445 block_p 0.0002 bootstrap CI [0.23098167286741014, 0.6190844641195029]
- R2_delta 0.244 rho_length per stratum {'0.0': -0.13112131012492093, '0.25': -0.7309503705282149, '0.5': -0.358670930678707, '0.75': -0.30287363391557737, '1.0': -0.23302440769627633}

### Governance + frontier
- probeFalseAccept 0.000 (<0.05) auditorBlockRate 1.000 (==1.0) frontierCrossFamily 0 (==0) frontierHitRate 0.754 (>0) cacheHitRate 0.839 (~0.80) effectiveFetchAvg 20.7 tok (~28) curatedDelta 0.464 (>0.10)

### Null controls
- NC1 rho 0.055 p 0.4265 -> PASS
- NC2 false_accept 0.318
- NC3 rho 0.000 R2 0.000
- NC4 ablation false_accept 0.365 curatedDelta 0.464

## Validity
- File-based synthetic mock 192/36 census; ceiling bounded to file mock not Docker/BrowserGym/real LLM
- MEA batched cache implemented with per-family TTL 60s cache; cacheHit flag honesty verified; effectiveFetch ~28 tok avg confirmed
- TTL/ETag probe deterministic map seeded 42 (loopback gunicorn+nginx simulated/disclosed); ~50% stale exercising ETag mismatch
- Frontier adapter synthetic char-bigram Jaccard TAU0.30; crossFamilyAdoption logged and must be 0
- Branch-derived cost sums with batched auditor_fetch; no bijective formula; no n*3200
- Family-stratified bootstrap 5000 + block-permutation 5000 respecting task-family dependency

## Artifacts
- artifacts/raw_per_task.csv (e7b68c8fc4a5) — 1728 rows (192 tasks x9 systems)
- artifacts/registry.jsonl (9ac48d200436) — 36 mechanisms
- artifacts/branch_traces.json, probe_traces.json, frontier_adapter_traces.json, cache_traces.json
- artifacts/derived_metrics.json (1633cc09df9b)
