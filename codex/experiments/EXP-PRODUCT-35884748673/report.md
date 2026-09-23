# EXP-PRODUCT-35884748673 Report — REOPEN C-RESIDUAL-NOVELTY honest-cost with MEA+TTL+frontier

**Lane:** product | **Claim:** C-RESIDUAL-NOVELTY primary, C-PRODUCT-ECON secondary | **Status:** COMPLETE | **Outcome:** FALSIFIES

## Question
After fixing TTL freshness model to 60s max-age with ~50% stale probes exercising ETag mismatch, wiring MEA auditor to actually block 100% unverified writes and log per-task provenance, making P-SPIDER-MEA cost branch-derived on realized novelty (hit 50 tok vs novel 500 tok + repair 500 + retrieval 200 + auditor 100 + probe 10 vs fullVerify 50 + distill 1000/f at f=10), importing frontier's validated state-conditioned reconstruction adapter with correct-family gating (no cross-family key adoption) and implementing honest QCR TFIDF Jaccard TAU0.30 retrieval over frozen bank with retrieval-use gap logging, does curated exploration + MEA auditor harness + TTL/ETag probe achieve per_hit <=0.85 vs RAG-EMBED at n0 and n0.25, <=1.20 vs Stagehand at n0, and <1.0 vs TERX at every n>=0.25 under honest kernel-gated cost at f=10 on 192/36 WebArena-Verified v2 census with family-stratified bootstrap 5000 and block-permutation 5000 and verification-derived calibration (false_accept<=0.10 UNKNOWN_precision>=0.85 ECE<=0.15), reporting Pareto (accuracy vs tokens vs browser+latency) vs gpt-4o-mini+Playwright Docker replication?

## Design
- Census 192 tasks /36 families /49 templates via actual src/spider/kernel.py distill_parameterized Jaccard>=0.55 constant-anchor field-path relevance body.*|headers.*|url (disclosed 0.55 vs 0.75 threshold, logs 0.75 as target)
- Curated exploration: 5 demos/family filtered by external verified_state hash matching postcondition before distill
- MEA auditor harness: fresh-context execution (context <=25k truncated, no history carryover, retrieval injected at provenance edge), external verified_state fetch 100 tok+80ms before registry promotion, governance gate blocks 100% unverified writes with provenance hash chain
- TTL/ETag probe: deterministic in-memory TTL/ETag map seeded 42 TTL 60s max-age via simulated gunicorn+nginx loopback (disclosed), conditional HEAD If-None-Match ETag W/body_sha 10 tok+30ms vs fullVerify 50 tok+120ms with SWR fallback, ~50% fresh vs ~50% stale exercising ETag mismatch per-step flags probeHit/etagMatched/ttlValid logged
- Frontier validated state-conditioned reconstruction adapter correct-family gated TAU0.30 no cross-family adoption, in-family reconstruction only 50 tok, crossFamilyAdoption must be 0
- QCR frozen bank 36 families Curated-A pools A/B disjoint TFIDF Jaccard TAU0.30 same-ranker all retrievers, retrieval-use gap logged, honestly retrievable at n=0.25 (proportional Jaccard)
- Honest kernel-gated branch-derived cost f=10 (retrieval 200+150ms, auditor_fetch 100+80ms SUT only, probe 10+30ms vs fullVerify 50+120ms, hit 50+1 call, novel/failed 500+2, repair 500+2, distill 1000/f + auditor 100/f amortized, frontier 50+40ms)

## Results (family-stratified pooled N=192 file-based primary, f=10)

### Controls
- **PC1** TERX hitRate 1.000 Stage hitRate 1.000 at n0 (expected 1.0) -> PASS
- **PC2** SPIDER-MEA binding 5/5 per family at n0 via _bind correctness 1.000 (expected 1.0) auditor blocks 1.000 (expected 1.0) -> PASS
- **PC3** TTL/ETag probe discrimination accuracy 1.000 (>=0.90) latency saving 0.375 (>=0.30) probeFalseAccept 0.000 (<0.05) ttlValidRate 0.562 (~0.50 stale) -> PASS
- **PC4** NC2 false_accept 0.120 in [0.10,0.60] -> PASS

Overall PC-MEA-AND-TTL-CACHE: **PASS** (failure -> MEASUREMENT_INVALID per precedence)

### Per_hit economics (Director REOPEN targets)
- SPIDER-MEA/RAG per_hit n0 1.143 (target <=0.85) -> FAIL
- SPIDER-MEA/RAG per_hit n0.25 0.298 (target <=0.85) -> PASS
- SPIDER-MEA/Stagehand per_hit n0 1.143 (target <=1.20) -> PASS
- SPIDER-MEA/TERX per_hit n0.25 0.123 (<1.0) n0.5 0.124 n0.75 0.123 n1.0 0.123 (all <1.0 required) -> PASS

### Calibration (verification-derived, non-vacuous MockEnv wrong-bound p=0.15 + true UNKNOWN when auditor rejects/probe stale/frontier gating rejects)
- Success at n0 1.000 Wilson lower 0.904 (need >=0.85, lower>=0.72) -> PASS
- Mean success all levels 1.000 (>=0.80)
- false_accept 0.000 (<=0.10) -> PASS
- UNKNOWN_precision 1.000 (>=0.85) UNKNOWN rate 0.234 (>=0.05)
- ECE_exec 0.018 empty bins [0, 1, 2, 3] (need <=0.15, std>0.05) confidence_std 0.408 -> PASS

### Work compression
- rho_novelty_per_hit -0.028 block_p 0.5063 bootstrap CI [-0.195867432465515, 0.13952803853995688]
- R2_delta_per_hit -0.613 rho_length per stratum {'0.0': -0.8116517539830552, '0.25': -0.7530823800948219, '0.5': -0.8508452274711803, '0.75': -0.8273383480953576, '1.0': -0.7695490524497987}
- SPIDER-MEA/COLD total n0 0.188 (<=0.75) n1 0.188 (<=1.10 via UNKNOWN)

### Governance + frontier
- probeFalseAccept 0.000 (<0.05) auditorBlockRate 1.000 (==1.0) frontierCrossFamily 0 (==0) frontierHitRate 1.000 (>0) curatedDelta 0.354 (>0.10 or NC4 fa>0.10)

### Null controls
- NC1 rho 0.000 p 1.000 (|rho|<0.25 p>=0.05) -> PASS
- NC2 false_accept 0.120 (>=0.10 or |rho|<0.35)
- NC3 rho 0.000 R2 0.000 (|rho|<0.25 R2<0.15)
- NC4 ablation false_accept 0.354 (>0.10 shows auditor delta)

## Decision
- **Status:** COMPLETE
- **Outcome:** FALSIFIES
- **Reasons:** ['C2 passed but C3 pivot per_hit targets failed (MEA overhead dominates)']
- **Criteria:** C1 True C2 True C3 False C4 True C5 True C6 True

## Interpretation
- Raw evidence separate from observations/measurements/interpretations per AGENTS.md. Per_hit isolation via (M_total_f10 - retrieval - distill - auditor)/L removes binary-gating artifact. Probe saving measured from both fresh vs stale paths with ~50% stale exercising ETag mismatch, auditor blocks 100% unverified writes with provenance hash chain, frontier correct-family gating 0 cross-family adoption enforced, QCR retrieval-use gap logged.
- If SUPPORTS: first non-parameterization evidence that governed-memory + cheap verification + correct-family reconstruction achieves honest-cost per_hit targets parameterization failed. Promote to EXPERIMENTAL bounded to file-based proxy; no PRODUCT_CORE without Docker replication.
- If FALSIFIES: governed-memory pivot (curated+MEA+TTL+frontier) as ported does not yield residual-novelty-proportional compression on this census vs retrievable RAG or shipped Stagehand cache; Stagehand 80% speedup remains dominant at exact repeat and RAG proportional at n0.25 remains strong baseline where SPIDER fails. Keep exact-intent or per-site mapping; prioritize kernel freshness/delta-repair or semantic-resolve orthogonal levers.
- If MEASUREMENT_INVALID: controls define invalid measurement apparatus, not falsification of hypothesis; exact failure.json reason and smallest next action required.

## Artifacts
- fixtures/tasks.json sha f43e38503952a53ce5272817cbed93ecc6b17b0730d98ddeff6bf00631f03e10
- artifacts/registry.jsonl sha fdf21c5982a9e43c398a99ac7654d1d3c908e6cec77c4302210a5eb2e13a2c8b 36 mechanisms distinct via distill_parameterized
- artifacts/raw_per_task.csv sha 53f493d749a3517fc2456d5b1b5367c89d1f199ae922fea096ee1e18510d06ff 1728 rows
- artifacts/branch_traces.json sha 0a219a261997ae5fd0a27b4223b16b8c98fb9c2da8f969fc760e435477cc4766
- artifacts/probe_traces.json
- artifacts/frontier_adapter_traces.json crossFamily must 0
- artifacts/derived_metrics.json sha 81d85987018a746ca5cbd3f8ee19eb610d817f976481d7a14d559e587abc1cea
- artifacts/cost_config.json honest 50-tok hits, probe 10 vs 50, frontier 50, f=10
- artifacts/qcr_bank_manifest.json frozen bank TAU0.30
- provenance.json docker_available false, ceiling file-based mock synthetic

## Validity Notes
File-based synthetic census bounded; Docker 2000-node BrowserGym 1280x720 gpt-4o-mini not executed; probe simulated deterministic map seeded 42 disclosed; frontier adapter synthetic char-bigram Jaccard disclosed.

## Unresolved
Proxy vs real Docker correlation rho_proxy_real not measured; f=100 amortization unknown; richer DOM transfer unknown.
