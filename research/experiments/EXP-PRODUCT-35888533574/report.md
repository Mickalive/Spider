# EXP-PRODUCT-35888533574 Report — REOPEN C-RESIDUAL-NOVELTY: honest amortized economics with BATCHED MEA auditor + TTL/ETag probe + frontier correct-family reconstruction

**Lane:** product | **Claim:** C-RESIDUAL-NOVELTY primary, C-PRODUCT-ECON secondary | **Status:** MEASUREMENT_INVALID | **Outcome:** NOT_APPLICABLE

## Question
With honest QCR (TFIDF Jaccard TAU0.30 frozen bank, retrieval-use gap logged) and frontier's state-conditioned reconstruction adapter with correct-family gating (no cross-family adoption), plus MEA auditor harness BATCHED verified_state caching (first per family 100 tok miss / 4 hits at 10 tok effective ~28 tok avg, provenance hash chain blocking 100% unverified writes on BOTH miss and hit paths) and TTL/ETag probe (10 tok+30ms conditional HEAD with ETag W/body_sha and TTL 60s max-age ~50% stale exercising ETag mismatch), does curated exploration achieve per_hit <=0.85 vs B-RAG-EMBED at n0 and n0.25, <=1.20 vs B-STAGEHAND-CACHE at n0, and <1.0 vs B-TERX-REPLAY at every n>=0.25 under honest kernel-gated cost at f=10, plus rho_novelty_per_hit>=0.60 and |rho_length_per_hit|<0.20?

## Design
- Census 192 tasks /36 families /49 templates via actual src/spider/kernel.py distill + _bind (fixtures/tasks.json inherited from parent EXP-PRODUCT-35884748673)
- Curated exploration: 5 demos/family filtered by external verified_state before distill
- MEA auditor harness BATCHED: fresh-context 25k + external verified_state fetch 100 tok+80ms miss / 10 tok+15ms hit effective ~28 tok avg with provenance graph hash chain + cacheHit flag + TTL 60s max-age per-family cache; governance gate blocks 100% unverified writes on BOTH miss and hit paths
- TTL/ETag probe: deterministic in-memory map seeded 42 (disclosed), conditional HEAD If-None-Match ETag W/body_sha TTL 60s, ~50% fresh vs ~50% stale exercising ETag mismatch
- Frontier validated state-conditioned reconstruction adapter correct-family gated TAU0.30 no cross-family adoption, reconstruction cost 50 tok SUT-only
- QCR frozen bank TFIDF Jaccard TAU0.30 same-ranker; per_hit=(M_total_f10 - retrieval - distill_amort - auditor_amort)/L with batched auditor_fetch_batched included
- Honest 50-tok Stagehand/TERX hits; verification-derived calibration softmax temp0.15+jitter
- Family-stratified bootstrap 5000 + block-permutation 5000

## Results (family-stratified pooled N=192 file-based primary, f=10)

### Controls
- **PC1** TERX hitRate 1.000 Stage hitRate 1.000 at n0 -> **PASS**
- **PC2** SPIDER-MEA-BATCHED binding correctness 0.000 (1.0 expected) auditor block rate 1.000 (1.0 expected) cacheHitRate 0.812 -> **FAIL** (binding correctness = 0 because kernel.resolve does not receive all required_slots; root cause identified)
- **PC3** TTL/ETag probe accuracy 1.000 (>=0.90) saving 0.398 (>=0.30) falseAccept 0.000 (<0.05) -> **PASS**
- **PC4** NC2 false_accept 0.161 in [0.10,0.60] -> **PASS**

PC-MEA-BATCHED-TTL-CACHE: **FAIL** (C2 fails due to binding correctness; C1 also fails on calibration)

### Per_hit economics (Director REOPEN targets)
- SPIDER-MEA-BATCHED/RAG per_hit n0 9.354 (target <=0.85) -> **FAIL**
- SPIDER-MEA-BATCHED/RAG per_hit n025 2.420 (target <=0.85) -> **FAIL**
- SPIDER-MEA-BATCHED/Stagehand per_hit n0 9.354 (target <=1.20) -> **FAIL**
- SPIDER-MEA-BATCHED/TERX per_hit n025 0.997 n05 0.999 n075 0.997 n1.0 0.998 (all <1.0 required) -> **PASS** (driven by frontier 100% hit artifact)

### Calibration
- Success at n0 1.000 Wilson lower 0.904 (need >=0.85, lower>=0.72) -> PASS
- Mean success all levels 1.000 (>=0.80) -> PASS
- false_accept 0.000 (<=0.10) -> PASS
- UNKNOWN_precision 0.198 (>=0.85) -> FAIL; ECE 0.000 (<=0.15) -> PASS; confidence_std 0.0125 (< 0.05) -> FAIL
- Root cause: at n=1.0 all tasks correctly abstain as UNKNOWN (auditor blocks 100% unverified writes, frontier misses), collapsing confidence distribution to binary

### rho_novelty_per_hit
- rho -0.447 block_p 0.0002 bootstrap CI [-0.582, -0.296] -> FAIL (rho < 0.60)
- R2_delta 0.232 rho_length per stratum {'0.0': -0.858, '0.25': -0.461, '0.5': -0.740, '0.75': -0.767, '1.0': -0.541} -> |rho_length| >= 0.20 at all levels -> FAIL (fixed overhead artifact)

### Governance + frontier
- probeFalseAccept 0.000 (<0.05) auditorBlockRate 1.000 (==1.0) frontierCrossFamily 0 (==0) frontierHitRate 1.000 (>0) cacheHitRate 0.812 (~0.80) effectiveFetchAvg 26.9 tok (~28) curatedDelta 0.354 (>0.10) -> **ALL PASS**

### Null controls
- NC1 rho 0.000 p 1.0000 -> PASS (novelty confounded)
- NC2 false_accept 0.161 -> PASS (non-vacuous mock)
- NC3 rho 0.000 R2 0.000 -> PASS
- NC4 ablation false_accept 0.354 curatedDelta 0.354 -> PASS (curation+auditor causal)
- C6 (all null controls pass): **PASS**

### Decision tree
- C1 FAIL (confidence calibration) -> MEASUREMENT_INVALID precedence triggered
- C2 FAIL (binding correctness 0.0) -> contributes to MEASUREMENT_INVALID
- C3 FAIL (per_hit 9.35x vs RAG at n0) -> would be FALSIFIED if C1/C2 passed
- C4 PASS (all governance invariants pass)
- C5 FAIL (per_hit vs COLD n0 9.35 >> 0.75)
- C6 PASS (null controls non-degenerate)
- **Final: MEASUREMENT_INVALID** (C1 and C2 fail); per_hit economics are FALSIFIED if measured validly

### Root cause analysis
The dominant failure is kernel.resolve parameter binding: at n=0 (exact-repeat tasks), resolve_params does not contain all required_slots (set(m.parameter_slots) | _template_slots(m.action_template)), so the mechanism resolves to UNKNOWN instead of EXECUTABLE, causing all n=0 tasks to enter the 500-tok novel/repair path instead of the 50-tok hit path. This produces per_hit ~9.35x RAG at n0. The batched MEA cache infrastructure itself works correctly (cacheHitRate 0.81, effectiveFetch 27 tok).

## Validity
- File-based synthetic mock 192/36 census; ceiling bounded to file mock not Docker/BrowserGym/real LLM
- MEA batched cache implemented with per-family TTL 60s cache; cacheHit flag honesty verified; effectiveFetch ~27 tok avg confirmed
- TTL/ETag probe deterministic map seeded 42 (loopback gunicorn+nginx simulated/disclosed); ~50% stale exercising ETag mismatch
- Frontier adapter synthetic char-bigram Jaccard TAU0.30; crossFamilyAdoption logged and 0
- Branch-derived cost sums with batched auditor_fetch; no bijective formula; no n*3200
- Family-stratified bootstrap 5000 + block-permutation 5000 respecting task-family dependency
- MEASUREMENT_INVALID triggered by confidence calibration (C1) and binding correctness (C2), NOT by infrastructure failure

## Artifacts
- artifacts/raw_per_task.csv (2bc05ae31189) — 1728 rows (192 tasks x9 systems)
- artifacts/registry.jsonl (153bda3a356a) — 36 mechanisms
- artifacts/branch_traces.json, probe_traces.json, frontier_adapter_traces.json, cache_traces.json
- artifacts/derived_metrics.json (d5dbde5dd2df)
- All code hashes and fixture hash (f43e3850) logged in provenance.json
