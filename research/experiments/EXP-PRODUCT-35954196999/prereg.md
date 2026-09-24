# EXP-PRODUCT-35954196999 — Preregistration (Product REOPEN C-PRODUCT-ECON)

**Lane:** product — **Claim:** C-PRODUCT-ECON (C-RESIDUAL-NOVELTY and C-FRESHNESS as gated sub-evaluations)  
**Director mandate:** REOPEN with cognitive_reset, SUPERSEDE parent handoff, action REOPEN, claim_id C-PRODUCT-ECON, single-node HS256 honesty gate dependencies  
**Parent:** EXP-PRODUCT-35951662423 handoff MEASUREMENT_INVALID (sha 202e61277460798dbae088b6c45b91977f21997a808a6aff5b4b033600f59e3a) — inherited state preserved per §2, but Director SUPERSEDE governs this design  
**Status:** DESIGN — frozen inputs immutable after freeze.json; no outcome inspection permitted

---

## 1. Background & inherited scientific state (from parent handoff + Codex)

**Established (bounded):**
- Frozen inputs byte-identical to prior freeze verified (audit V1). MV2 kernel dot-regex gate CLEARED: `src/spider/kernel.py` line12 `_PARAMETER = r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` sha d926279d 5/5 EXECUTABLE confidence 0.85, pre-patch 46929b3a fails on dot-nested slots. Scientific stack installable (numpy 2.5.3, scipy 1.18.1, sklearn 1.9.1, pandas 3.0.6, flask 3.1.3, pyjwt 2.15.0, gunicorn 26.2.0) — version drift vs frozen 23.0.0/2.14.0 remains.
- Bounded file-proxy falsification remains ceiling: WebArena-Verified v2 192/36 orthogonal alias families 630 pairs Jaccard 0.0 QCR TAU0.30 + honest f=10 sum counters; StagehandTTL per_hit 1.045 CI[1.034,1.056]>0.85 at n0 fails gate, WebMCP per_hit 1.032>0.85 at n0, rho_novelty 0.472(<0.60) |rho_length|0.306(>0.20), Pareto M_total_f10 WebMCP 897 vs Stagehand 1773 vs RAG 3703 vs Cold 5497 hidden by per_hit artifact (retrieval 200 vs tool 15 vs SGDR 180 excluded). No new Pareto/rho/calibration evidence from last invalid run (metrics null).
- Audit PASS confirms no fabrication (no n*3200 bijective proxy, no seeded-42 stale fallback, no deg CI).
- Portfolio: C-FRESHNESS synthetic SURVIVES TN>=0.85 but distributed n>=800 HS256 transfer MEASUREMENT_INVALID; C-MEAS-VALID closed 960/960 nginx HIT locally but Flask HS256 infinite-loop blocks distributed; C-PARAM-INHERIT 49 exps no EXECUTABLE>=0.75 on live browser; frontier alias catalog 20-21/40=0.525<0.60, C-WEB-DYNAMICS 71 exps negative log BF, C-RESIDUAL-NOVELTY/C-PRODUCT-ECON falsified per_hit 1.005>0.85 rho 0.363<0.60.

**Rejected (bounded to file-proxy isolated SQLite seeded-42):**
- Stagehand selector-cache+TTL and WebMCP/DSM Registry 714/2147 do NOT achieve per_hit<=0.85 at n0 on file-proxy honest f=10; rho tracking does NOT achieve >=0.60 with |rho_length|<0.20 on file-proxy orthogonal only. per_hit~1.0 is metric-design artifact (both StagehandTTL and RAG hit same 50-tok verify after excluding retrieval vs tool) not evidence Pareto fails.

**Unknown (this experiment must resolve):**
- Whether single-node HS256 sticky substrate at /tmp/spider-runtime/shared.db (WAL single-worker gunicorn 23.0.0 pinned vs 26.2.0, nginx 1.24.0 $request_uri sticky hash, PyJWT 2.14.0 HS256, real If-None-Match/ETag W/body_sha 200 vs 304) with n_non304>=800 TN>=0.85 can be provisioned with correlated 60s ETag freshness.
- Whether Docker BrowserGym 0.14.3 2000-node 1280x720 Playwright 1.63.0 + gpt-4o-mini 15-step real tokens/browser_steps+latency with rho_proxy_real>=0.50 pooled+per-stratum exists (OPENAI_API_KEY + pullable ghcr.io/servicenow/browsergym:0.14.3 required; previously denied).
- Whether sgdr_index 36 state_key + 192/36 census + qcr_bank TAU0.30 + dsm_registry 714/2147 + cost_config 50/15/180/10 can be staged TRAIN-only without contamination and verify calibration/AUROC/safety on honest pipeline.
- Whether pip WebArena-Verified Hard 258 heterogeneous subset measures Pareto vs DSM $0.002-0.092 amortized 80-94% compile success deterministic engine.

**Do_not_assume (must not be inferred from invalid prior):**
- MEASUREMENT_INVALID ≠ falsification; file-proxy numbers do not transfer to honest single-node health-gated correlated substrate; per_hit~1.0 artifact ≠ Pareto non-dominance; seeded-42 0.53 decorrelated ≠ correlated ETag W/body_sha fresh ~1.0; docker binary presence ≠ substrate availability; Pareto requires rho_proxy_real>=0.50 per-stratum + |rho_shuffled|<0.20 + |rho_length|<0.20 + n_non304>=800 trajectory-grouped; calibration/safety not PASS until measured honestly; kernel dot-regex alone does not imply economics.

Director comparative reasoning adopted: vs PARK pending distributed 800-stratified (would idle product while frontier/graph idle), vs alternative C-LLM-INHERIT subsumed by Pareto (same gpt-4o-mini/tools/budget 15 steps + ECE gates), vs standalone compiled-workflow shootout (Pareto already includes WebMCP 714/2147 + DSM 99% TreeWalker plus RAG/Stagehand). REOPEN after 15-streak invalid justified because honest health-gated sum-counters invalidates prior falsification scope.

---

## 2. Research question (Director binding, refined to falsifiable gate)

On pip-installable WebArena-Verified Hard 258 + BrowserGym 0.14.3 2000-node 1280x720 CDP Accessibility.getFullAXTree heterogeneous subset (health-gated single-node Flask HS256 sticky $request_uri + nginx If-None-Match/304 where needed, n_non304>=800, TTL 60s max-age conditional probe ETag W/body_sha fresh at n0 ~1.0 vs ~50% stale at n0.25), does honest end-to-end economics (M_total_f10 = tokens+browser_steps+latency+retrieval+verification+freshness with per-trajectory-reset honest sum-counters, 5000 family-stratified trajectory-grouped bootstrap CIs, rho_proxy_real>=0.50 per-stratum |rho_shuffled|<0.20) show residual-novelty rho_novelty>=0.60 vs |rho_length|<0.20 and Pareto dominance at f=10/100 vs RAG-EMBED TAU0.30/QCR, Stagehand 2x selector-cache+TTL, and Agentic Compilation DSM JSON IR O(1) $0.002-0.092 amortized (80-94% compile success, deterministic engine), with verification AUROC>=0.75 precision>=0.80 false_accept<=0.10 UNKNOWN precision>=0.85 per-class ECE<=0.15 Wilson, superseding falsified per-hit (1.005>0.85, rho 0.363<0.60)?

This is the smallest high-information gate that can change C-PRODUCT-ECON from HYPOTHESIS bounded file-proxy REJECTED to EXPERIMENTAL on valid substrate or PARK it even on honest substrate, directly testing product bottleneck (verification/UNKNOWN calibration, not retrieval) and external O(1) compilation threat.

---

## 3. Hypothesis

H1 (primary): With health-gated single-node HS256 sticky substrate and correlated ETag freshness (fresh ~1.0 at n0 vs ~50% stale at n0.25, n_non304>=800, single nginx $request_uri sticky + single gunicorn Flask HS256 PyJWT 2.14.0, WAL shared.db) and BrowserGym 2000-node heterogeneous real gpt-4o-mini 15-step tokens+browser_steps+latency, SPIDER freshness-gated inheritance (selector-cache + 10tok/30ms correlated probe + softmax temp0.15+jitter calibration) and DSM JSON IR O(1) (15tok/10ms amortized 800/f, 80-94% compile success deterministic) achieve:
- (a) residual-novelty tracking rho_novelty>=0.60 (Spearman pooled+per-stratum, 95% CI lower >=0.50 pooled >=0.45 per-stratum) with |rho_length|<0.20 and rho_proxy_real>=0.50 per-stratum |rho_shuffled|<0.20, and
- (b) M_total_f10/f100 Pareto dominance tokens>=30% and browser_steps+latency>=20% vs RAG-EMBED TAU0.30/QCR at f=10 and f=100 with accuracy>=0.85, correlated probe saving>=30% accuracy>=0.90 TN>=0.85, AUROC>=0.75 precision>=0.80 false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15, DSM amortized $0.002-0.092, safety CuP non-inferior.

Null hypothesis for null controls: Shuffled bindings/probe/DSM/SGDR, length-constant cost, and random-key entry are uncorrelated with novelty/length and have AUROC~0.5, per spec NC.

---

## 4. State / Action / Target representation

- **State representation:** Mechanism preconditions = family+intent+site (+ state_key=family+DOM_hash for SGDR from BrowserGym CDP AX 2000 nodes if Docker else disclosed file-proxy hash). DOM hash = SHA256 of ordered AX tree snapshot (2000-node) truncated at 2000 nodes. Freshness feature = ETag W/body_sha + TTL max-age 60s + probeHit (200 vs 304).
- **Action representation:** Mechanism action_template with parameter slots `${param}` using dot-regex r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}' (supports nested e.g., `${user.profile.id}`). Binding via _bind full-match vs substring replacement. Verification via kernel.verify postconditions exact match.
- **Target (economics):** Per-trajectory M_total_f10 = sum_tokens + sum_browser_steps + latency_ms_equiv + retrieval (200) + DSM tool (15) + SGDR (180) + verification (50 tok+120ms per verify) + freshness probe (10tok+30ms per step) with per-trajectory-reset honest sum counters (no n*3200 bijective proxy). Derived M_per_hit = (M_total - retrieval/tool/DSM/SGDR - distill/compile - auditor)/L (probe stays in numerator). Primary metric for supersede is M_total_f10/f100 Pareto, not per_hit. Novelty fraction n = slots drawn from B (test) vs Curated-A (train) per family stratified by slot position, realized per trajectory 0/0.25/0.5/0.75/1.0.
- **Calibration target:** Verification confidence (softmax temp0.15+jitter) vs correctness (EXEC rows). AUROC, precision, false_accept, UNKNOWN_precision, per-class ECE 5-bin.

---

## 5. Sampling policy & holdout

- **Census:** Pip-installable WebArena-Verified Hard 258 as primary heterogeneous task pool via `pip install browsergym webarena` or repo pip. If Docker image ghcr.io/servicenow/browsergym:0.14.3 unavailable or Hard 258 pip manifest missing, fallback to WebArena-Verified v2 192 tasks across 36 orthogonal alias families (A/B disjoint alphabets, Jaccard<0.30 630 pairs via qcr_bank_manifest.json sha 8c69804b) as disclosed heterogeneous subset. Families stratified, trajectory-grouped.
- **Splits:** Per-family disjoint Curated-A (train, for registry induction + qcr bank + dsm + sgdr) / B (test, orthogonal slots) zero overlap. Frozen qcr_bank_manifest TAU0.30 same ranker TFIDF for RAG/SGDR. DSM registry 714/2147 from Curated-A TRAIN only. SGDR index 36 state_key TRAIN only. Test tasks never in curation.
- **Conditions:** 6 conditions x 5 novelty levels = 30 cells family-stratified (COLD, B-RAG, B-STAGEHAND-CACHE, P-STAGEHAND-TTL-CORRELATED, P-DSM-COMPILE-O1, P-SGDR-AWM). Plus 4 null controls trajectory-grouped permutations + ablations.
- **Browser substrate:** Docker BrowserGym 0.14.3 2000-node 1280x720 CDP getFullAXTree, Playwright 1.63.0, gpt-4o-mini 15-step budget same model/tools/budget across conditions. If Docker pull denied or OPENAI_API_KEY absent, primary gate is MEASUREMENT_INVALID (no fallback to file-proxy for SURVIVES).
- **Single-node substrate:** /tmp/spider-runtime/shared.db SQLite WAL single-worker gunicorn 23.0.0 + nginx 1.24.0 $request_uri sticky hash + PyJWT 2.14.0 HS256, If-None-Match/ETag W/body_sha conditional probe health-gated n_non304>=800. Single-node is dependency gate per Director: runtime C-MEAS-VALID + graph C-FRESHNESS single-node validated.

---

## 6. Unit of analysis & holdout integrity

- Unit = trajectory (family-stratified, trajectory-grouped). Bootstrap and permutation respect trajectory grouping (block-permutation by trajectory/family, not transition). Stratified by family (36 families) and novelty fraction.
- Holdout = per-family train/test disjoint; frozen bank and registries TRAIN-only. Verify no test keys in curations via hash check; contamination => PC2 MEASUREMENT_INVALID.
- Preprocessing fit on TRAIN only (TFIDF, QCR bank). No post-state leakage into pre-state features.

---

## 7. Baselines & controls (stable identities for AUDIT/DIRECTOR)

**Baselines (honest same splits, same probe/verify fallback, honest f=10/f=100 amortized):**
- B-COLD: no memory, 500 tok +2 browser_steps +50+120ms verify per step.
- B-RAG-EMBED-TAU030-QCR: TFIDF/Jaccard TAU0.30 top-1 QCR frozen bank, 200 tok+150ms retrieval.
- B-STAGEHAND-CACHE: DOM-hash selector cache without TTL, hit iff DOM identical (1.0 at n0, 0 at n>=0.25 orthogonal), 2x speedup vendor baseline.
- P-STAGEHAND-TTL-CORRELATED (SUT): selector-cache + correlated 60s ETag probe 10tok+30ms health-gated n_non304>=800 + verification calibration AUROC>=0.75.
- P-DSM-COMPILE-O1 (SUT/competitor): DSM JSON IR O(1) 714/2147 15tok+10ms amortized 800/f 80-94% compile $0.002-0.092 deterministic.
- P-SGDR-AWM (SUT): state-grounded 180tok+120ms rerank, 36 state_key TRAIN-only.

**Positive control PC-SINGLE-NODE-PARETO-CORRELATED (5 checks, any fail => MEASUREMENT_INVALID):**
- PC1 exact-repeat 1.0 hit at n0 5/5 spot-check,
- PC2 orthogonal Jaccard<0.30 max 0.0 + kernel dot-regex 5/5 EXECUTABLE confidence>=0.80 + correlated probe fresh~1.0 stale~50% accuracy>=0.90 saving>=30% TN>=0.85 + DSM 714/2147 80-94% + SGDR 36 hit>=0.5 + Hard258 heterogeneous or disclosed 192/36 fallback,
- PC3 non-vacuous verify false_accept [0.10,0.60] confidence_std>0.05 AUROC null~0.5 true>=0.75,
- PC4 frozen formula within 1e-6 vs summed counters + n_non304 logged,
- PC5 health-gate n_non304>=800 sticky single-worker HS256 + If-None-Match exercised + BrowserGym 2000-node if available.

**Null control NC-SINGLE-NODE-SHUFFLE-PIPELINE (via actual single-node pipeline, no simulated correctness):**
- NC1 shuffled slots + TTL map random 0.53 vs correlated + DSM + SGDR keys permuted trajectory-grouped: expect |rho|<0.25 ns, |rho_shuffled|<0.20 p>=0.20 per-stratum, |rho_length|<0.20, AUROC 0.45-0.60, success<=COLD, UNKNOWN>=0.80.
- NC2 random family/state keys: false_accept>=0.10 AUROC~0.5.
- NC3 length-constant cost L*500: |rho|~0 R2<0.15.
- NC4 ablations: correlated vs random delta>10%, DSM off vs on, SGDR vs RAG delta, single-node TN 0.85 vs per-node 0.667.

---

## 8. Metrics (stable names, with units)

- `rho_novelty` (Spearman M_per_hit vs n pooled + per-stratum, 95% CI family-stratified trajectory-grouped bootstrap 5000) — primary economics calibration
- `rho_length` (|rho| M_per_hit vs L, pooled+per-stratum) — must be <0.20
- `rho_proxy_real` (Spearman proxy cost vs real gpt-4o-mini tokens+browser_steps+latency pooled+per-stratum) — must be >=0.50 per-stratum
- `rho_shuffled` (|rho| shuffled null pooled+per-stratum, block-permutation 5000 p) — must be <0.20 p>=0.20
- `M_total_f10` , `M_total_f100` (tokens+browser_steps+latency+retrieval/verification/freshness per trajectory honest sum counters) + Pareto decompose tokens vs browser_steps+latency vs accuracy
- `M_per_hit` = (M_total - retrieval/tool/SGDR - distill/compile - auditor)/L (probe stays IN) — contested superseded gate
- `AUROC_verif` , `precision_verif` , `false_accept` , `UNKNOWN_precision` , `ECE_5bin_per_class` + Wilson CIs and bootstrap upper — calibration
- `toolHit` , `SGDRHitRate` , `cacheHit` , `probeHit_correlated` vs `probeHit_random` , `n_non304` , `TN_freshness` — probe/registry diagnostics
- `violation_rate_CuP` (ST-WebAgentBench or synthetic proxy disclosed)
- `compile_success_DSM` , `amortized_cost_DSM` ($0.002-0.092)

All metrics report family-stratified trajectory-grouped bootstrap 5000 CIs and Wilson 95% for rates. Within-family std>0 required; degenerate CI[1,1] flags MEASUREMENT_INVALID.

---

## 9. Decision rule (frozen, precedence ordered)

Computed on single-node health-gated n_non304>=800 + Docker BrowserGym 2000-node heterogeneous real tokens branch-derived f=10 honest per-trajectory-reset counters TRAIN-warmed.

1. **MEASUREMENT_INVALID** if any PC1-PC5 fails OR n_non304<800 OR $request_uri sticky violated OR If-None-Match not exercised OR single-node HS256 not at /tmp/spider-runtime/shared.db WAL single-worker OR Docker BrowserGym 0.14.3 + gpt-4o-mini unavailable (rho_proxy_real unmeasurable) OR fixtures missing (Hard258 pip or 192/36 fallback with disclosure, qcr TAU0.30, dsm 714/2147, sgdr 36, cost_config) OR kernel dot-regex not patched OR TRAIN contamination OR degenerate null (|rho_shuffled|>=0.35 p<0.01 or within-std==0 or CI[1,1]) — irrespective of economics, no file-proxy fallback.

2. Else **FALSIFIED** if controls PASS non-degenerate but any primary gate fails: success at n0<0.85 (Wilson lower<0.80) OR AUROC<0.75 OR precision<0.80 OR false_accept>0.10 OR UNKNOWN<0.85 OR ECE>0.15 bootstrap upper>0.18 per-class OR rho_novelty<0.60 (CI lower<0.50 pooled or <0.45 per-stratum) OR |rho_length|>=0.20 OR rho_proxy_real<0.50 per-stratum OR |rho_shuffled|>=0.20 OR Pareto token saving <30% at f=10 vs RAG OR token saving <25% at f=100 OR browser+latency saving <20% OR accuracy<0.85 OR correlated probe saving<30% accuracy<0.90 TN<0.85 OR DSM compile <80% or >94% detached or amortized outside $0.002-0.092 OR CuP violation >RAG+0.02 and >0.05 (absolute) with non-synthetic ST-WebAgentBench.

3. Else **SURVIVES** iff ALL hold with PC PASS non-degenerate: (C1) success>=0.85 Wilson>=0.80 AUROC>=0.75 precision>=0.80 false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18; (C2) rho_novelty>=0.60 pooled CI>=0.50 per-stratum>=0.45 with |rho_length|<0.20 pooled+per-stratum and rho_proxy_real>=0.50 per-stratum |rho_shuffled|<0.20 p>=0.20; (C3) Pareto tokens>=30% vs RAG and browser+latency>=20% at f=10 and f=100 accuracy>=0.85 with correlated probe saving>=30% accuracy>=0.90 TN>=0.85 and DSM 80-94% $0.002-0.092; (C4) CuP non-inferior or disclosed synthetic proxy not blocking if C1-C3 pass (flagged unresolved).

**SUPERSEDE clause (Director rationale):** If per_hit=(M_total - retrieval/tool/SGDR - distill/compile - auditor)/L CI clears >0.85 at BOTH n0 and n0.25 (5000 bootstrap, falsified 1.005>0.85 parent) but M_total_f10/f100 Pareto dominates decisively (tokens >=30% DSM >=25% SGDR >=30% StagehandTTL vs RAG at f=10 and f=100 latency>=20% accuracy>=0.85 rho_proxy_real>=0.50 per-stratum n_non304>=800 correlated delta>10% AUROC>=0.75 safety non-inferior) then per_hit artifact demonstrated and M_total Pareto supersedes per_hit as PRODUCT_CORE gate — verdict recommends supersession in handoff, not per_hit promotion.

Previous falsification bounded to file-proxy with rho 0.363<0.60 is NOT reopened without health-gated real-token replication.

---

## 10. Product consequences

**Positive (SURVIVES):** C-PRODUCT-ECON HYPOTHESIS → EXPERIMENTAL bounded to WebArena-Verified Hard 258 heterogeneous single-node health-gated 1280x720 (selector-cache+correlated-TTL/ETag 10 vs 50 vs 200 vs 15 DSM vs 180 SGDR honest f=10 + BrowserGym 2000-node rho validated). C-FRESHNESS → EXPERIMENTAL for correlated probe + C-RESIDUAL-NOVELTY economics validated at rho>=0.60. First valid single-node+real-token evidence that gated inheritance beats shipped Stagehand 2x cache+TTL and RAG and is Pareto-competitive with DSM O(1) $0.002-0.092 at f=10/100. Justifies shipping correlated-gating as interim vs Stagehand cache-only, with Pareto frontier + rho as pricing prior for compilation vs inheritance. No PRODUCT_CORE without explicit DIRECTOR promote_to_product true. DSM delta informs O(1) vs SGDR choice.

**Negative (FALSIFIED with controls PASS n>=800 rho_proxy>=0.50 AUROC>=0.75):** Selector-cache+correlated ETag and DSM O(1) do NOT yield Pareto dominance or rho>=0.60 even on honest substrate; PARK C-RESIDUAL-NOVELTY/C-PRODUCT-ECON economics even on honest correlated substrate per Director PIVOT, pivoting Product to ST-WebAgentBench CuP or Intel diverse-site grounding or richer SPA sampling before PRODUCT_CORE. Joint falsification of DSM and SGDR triggers architecture choice: compilation vs continuous inheritance.

**Measurement invalid:** No claim update; handoff carries smallest next action (runtime single-node hardening, gunicorn 23.0.0/PyJWT 2.14.0 pin, nginx $request_uri sticky, BrowserGym pull/OPENAI_API_KEY, n_non304>=800, If-None-Match loop) without inventing economics.

---

## 11. Validity threats & controls

- **Representation loss:** DOM truncation at 2000 nodes, file-proxy hash fallback disclosed; browser events/network/auth/session preserved via Flask HS256 + BrowserGym AX.
- **Policy confounding:** Same gpt-4o-mini + same 15-step budget/tools across conditions; trajectory-grouped permutation isolates policy regularity from environment dynamics.
- **Site/task leakage:** Frozen qcr_bank TAU0.30 same ranker, hard families disjoint, site gating mandatory; audit recomputes parity within 1e-6.
- **Bijective proxy:** Honest per-trajectory sum counters enforced; any n*3200 reported => MEASUREMENT_INVALID.
- **Verification calibration threat:** Softmax temp0.15+jitter prevents linear 0.95-n*0.12 tautology; confidence_std>0.05 and AUROC vs shuffled null required; empty ECE bins disclosed.
- **Stale freshness:** Seeded-42 0.53 decorrelated contrast vs correlated ETag W/body_sha fresh~1.0 isolates novelty correlation; TN>=0.85 health-gated vs per-node 0.667 artifact.
- **Cost model threat:** DSM $0.002-0.092 amortized 800/f verified against real tool catalog, not assumed; per_hit excludes retrieval/tool/SGDR/compile but M_total includes them — Pareto vs per_hit artifact disclosed.
- **Safety threat:** ST-WebAgentBench CuP or disclosed synthetic proxy; DSM tool-bypass bypass must not increase violation >0.05 absolute.

---

## 12. Cost & information gain

**Estimated cost:** Moderate single-node health-gated: 258 (or 192) x6 x5 levels =1290/960 + ~600-750 nulls + ~400-500 ablations = ~2290-2540 deterministic resolve/_bind/probe/DSM/SGDR verify trials on single-node HS256 sticky WAL + TFIDF offline. Wall <90min CPU proxy (<160min if Docker BrowserGym 2000-node loopback health-gated n_non304>=800). Storage ~3000-4000 row CSV + registry/dsm/sgdr + branch_traces. If Docker+gpt-4o-mini: 258x6x15 steps ~4650 browser calls ~3870 LLM calls <$30 plus snapshots/logs. Honest sum counters, no bijective n*3200.

**Expected information gain:** Decisive gating per Director after 15-streak invalid and bounded per_hit falsification 1.005>0.85. Health-gated single-node + TTL 60s correlated freshness + heterogeneous BrowserGym + AUROC calibration is diagnosed missing prerequisite. Smallest test that can change decision: positive reopens C-PRODUCT-ECON to EXPERIMENTAL and justifies interim shipping with Pareto pricing vs DSM O(1); per_hit artifact supersession formally replaces contested metric with M_total Pareto; double failure PARKs residual-novelty/DSM economics on honest substrate and forces pivot to CuP/richer SPA. Vs 18th alias permutation (0/10 mixed header+body+query+auth zero marginal gain) marginal information ~0. Pareto vs DSM is now product bottleneck, not retrieval.

---

## 13. Execution checklist (frozen, must log or MEASUREMENT_INVALID)

- [ ] Pin gunicorn 23.0.0 and PyJWT 2.14.0 exactly (vs installed 26.2.0/2.15.0 drift) before SURVIVES
- [ ] Provision /tmp/spider-runtime/shared.db WAL single-worker sticky, nginx 1.24.0 $request_uri hash, If-None-Match/ETag W/body_sha 200 vs 304, n_non304>=800 health-gated TN>=0.85
- [ ] Pip-install WebArena-Verified Hard 258 + BrowserGym 0.14.3 2000-node 1280x720 CDP getFullAXTree; log versions, hashes, viewport, node count, image pull, OPENAI_API_KEY presence, rho_proxy_real per-stratum
- [ ] Stage qcr_bank_manifest TAU0.30 Jaccard<0.30, dsm_registry 714/2147, sgdr_index 36 state_key TRAIN-only, cost_config 50/15/180/10, kernel dot-regex d926279d
- [ ] Run 5000 family-stratified trajectory-grouped bootstrap + 5000 block-permutation with per-stratum rho_length/shuffled/proxy thresholds
- [ ] Report AUROC/precision/false_accept/UNKNOWN/ECE per-class + CuP safety (or synthetic proxy disclosed) + DSM $0.002-0.092 amortized
- [ ] Preserve raw evidence, recomputable hashes, frozen formula audit within 1e-6, unresolved distinct from measurement failure

*No outcome-bearing measurement was run during DESIGN. This preregistration is frozen before freeze.json.*
