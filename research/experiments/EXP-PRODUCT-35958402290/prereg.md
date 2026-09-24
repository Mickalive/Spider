# EXP-PRODUCT-35958402290 — Preregistration (Product REOPEN C-PRODUCT-ECON)

**Lane:** product — **Claim:** C-PRODUCT-ECON (C-RESIDUAL-NOVELTY and C-FRESHNESS as gated sub-evaluations)  
**Director mandate:** REOPEN with cognitive_reset=true, SUPERSEDE parent handoff, action REOPEN, claim_id C-PRODUCT-ECON, comparative reasoning vs C-RESIDUAL-NOVELTY tuning and C-PARAM-INHERIT slot-syntax  
**Parent:** EXP-PRODUCT-35954196999 handoff MEASUREMENT_INVALID sha f6560fac076e389f2275962332bdfa050e32c903caf9bdb750584d6a5d05ff28 — inherited state preserved per §2, Director SUPERSEDE governs this design  
**Status:** DESIGN — frozen inputs immutable after freeze.json; no outcome inspection permitted

---

## 1. Background & inherited scientific state (from parent handoff + Codex + Scout)

**Established (bounded):**
- Frozen inputs byte-identical verified (request 500888432e900629085d83032bf13d75aa528166427862fc59f4228e7a08e43a, spec 5cf9297b763238b704a78436655121b0d83043f8d9268112ca5d8a27e917a7be, prereg ba51631006aa8d598e6f2e7fdc5c7f50c5ca88db6372901fa35bac9bea068a65). Audit PASS on transmission invariants.
- MV2 kernel dot-regex gate CLEARED only in working tree: `src/spider/kernel.py` line12 `_PARAMETER = r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` sha d926279d 5/5 EXECUTABLE confidence 0.85 with dot-nested binding (${item.id}, ${family.id}); HEAD still pre-patch 46929b3a fails dot-nested. Scientific stack installable (numpy 2.5.3 scipy 1.18.1 sklearn 1.9.1 pandas 3.0.6 flask 3.1.3 pyjwt 2.15.0 gunicorn 26.2.0) with drift vs frozen pins 23.0.0/2.14.0.
- Bounded file-proxy falsification remains ceiling: WebArena-Verified v2 192/36 orthogonal alias families 630 pairs Jaccard 0.0 QCR TAU0.30 + honest f=10 sum counters; StagehandTTL per_hit 1.045 CI[1.034,1.056]>0.85 at n0 fails gate, WebMCP 1.032>0.85, rho_novelty 0.472(<0.60) |rho_length|0.306(>0.20), Pareto M_total_f10 WebMCP 897 vs Stagehand 1773 vs RAG 3703 vs Cold 5497 hidden by per_hit artifact (retrieval 200 vs tool 15 vs SGDR 180 excluded). No new Pareto/rho/calibration evidence from last invalid run (metrics null per contract, controls UNKNOWN except kernel sub-gate, outcome INCONCLUSIVE not FALSIFIED).
- Portfolio: C-FRESHNESS synthetic SURVIVES TN>=0.85 FA<=0.10 ECE<=0.15 at 15% stale but confined to stdlib http.server flat-JSON; C-MEAS-VALID single-node HS256 gate MEASUREMENT_INVALID (92 exps, wsgi path/factory ordering/header de-confounding, EXP-RUNTIME-35949568321 wsgi import loop); C-PARAM-INHERIT stalled 8 consecutive MEASUREMENT_INVALID on WebArena-Verified; Frontier local attractor 17 alias/routing permutations pooled 21/40=0.525<0.60, 0/10 mixed/auth, zero marginal gain. Product C-PRODUCT-ECON 16-streak all MEASUREMENT_INVALID, per_hit falsified 1.005>0.85 rho 0.363<0.60 superseded by M_total_f10.

**Rejected (bounded to file-proxy isolated SQLite):**
- Stagehand selector-cache+TTL and WebMCP/DSM Registry 714/2147 do NOT achieve per_hit<=0.85 at n0 on file-proxy honest f=10; rho tracking does NOT achieve >=0.60 with |rho_length|<0.20 on file-proxy orthogonal only. per_hit~1.0 is metric-design artifact (both StagehandTTL and RAG hit same 50-tok verify after excluding retrieval vs tool) not evidence M_total Pareto fails.
- Kernel HEAD pre-patch regex `r'\$\{[A-Za-z_][A-Za-z0-9_]*\}'` fails dot-nested and was not durable.
- No rejection of honest single-node health-gated correlated freshness Pareto or residual-novelty rho>=0.60; no rejection of DSM O(1) $0.002-0.092 amortized or SGDR vs DSM delta on honest substrate.

**Unknown (this experiment must resolve):**
- Whether /tmp/spider-runtime/shared.db WAL single-worker gunicorn 23.0.0 + nginx 1.24.0 $request_uri sticky hash + PyJWT 2.14.0 HS256 + real If-None-Match/ETag W/body_sha 200 vs 304 loop can be provisioned health-gated with n_non304>=800 stratified 400/endpoint TN>=0.85 freshness fresh ~1.0 at n0 vs ~0.5 stale at n0.25 saving>=30% accuracy>=0.90 falseAccept<0.05.
- Whether Docker BrowserGym 0.14.3 2000-node 1280x720 CDP Accessibility.getFullAXTree + gpt-4o-mini 15-step real tokens/browser_steps/latency exists (GHCR pull + OPENAI_API_KEY) and file-proxy cost tracks real cost rho_proxy_real>=0.50 pooled+per-stratum with |rho_shuffled|<0.20 and |rho_length|<0.20.
- Whether sgdr_index 36 state_key TRAIN-only + WebArena-Verified Hard258 258-task heterogeneous census (or disclosed 192/36 fallback) + qcr_bank TAU0.30 Jaccard<0.30 + dsm_registry 714/2147 + cost_config 50/15/180/10 can be staged TRAIN-only without contamination and measured with 5000 family-stratified trajectory-grouped bootstrap + 5000 block-permutation.
- Whether P-STAGEHAND-TTL correlated probe and DSM O(1) compile (80-94% success 15tok+10ms amortized 800/f) and P-SGDR achieve M_total Pareto tokens>=30% and browser+latency>=20% vs RAG at f=10 and f=100 with accuracy>=0.85 AUROC>=0.75 precision>=0.80 false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 superseding per_hit.

**Do_not_assume (must not be inferred from invalid prior):**
- MEASUREMENT_INVALID is infrastructure failure, not scientific falsification per EXPERIMENT_PACKET s9; file-proxy per_hit~1.0 artifact does not imply M_total Pareto fails on honest substrate.
- Working-tree kernel patch d926279d is not committed: HEAD and prior verdict still pre-patch; do not assume dot-regex durable.
- Stack installable does not imply pin compliance or substrate health: gunicorn 26.2.0!=23.0.0 pyjwt 2.15.0!=2.14.0 drift; nginx binary present != $request_uri sticky running or If-None-Match exercised or n_non304>=800 stratified.
- Docker binary present and pip browsergym index entry != image available (ghcr pull previously denied) or OPENAI_API_KEY provisioned; file-proxy fallback banned for SURVIVES.
- Prior artifacts (qcr 8c69804b, webmcp 2147/714 af3c18e5, tasks 391e8f6c 192/36) are cross-experiment references, not this experiment's staged census; sgdr_index absent repo-wide, Hard258 not staged.
- Runtime C-MEAS-VALID and graph C-FRESHNESS single-node both MEASUREMENT_INVALID beyond synthetic; do not assume validated.

Director comparative reasoning adopted: versus continuing C-RESIDUAL-NOVELTY rho_novelty tuning on file-proxy (already FALSIFIED per_hit and invalid M_total) or another C-PARAM-INHERIT slot-syntax test (MEASUREMENT_INVALID 49 experiments), Pareto dominance test with verification-derived calibration and BrowserGym real gpt-4o-mini replication directly measures commercial viability and dominates narrow Stagehand 2x selector-cache test because it integrates safety, freshness correlated saving, and DSM O(1) amortization at f=10/100 with family-stratified CIs.

---

## 2. Research question (Director binding, refined to falsifiable gate)

On pip-installable WebArena-Verified Hard258 + BrowserGym 0.14.3 2000-node 1280x720 CDP Accessibility.getFullAXTree heterogeneous subset (health-gated single-node Flask HS256 sticky $request_uri + nginx If-None-Match/304 where needed, n_non304>=800 stratified 400/endpoint, TTL 60s max-age conditional probe ETag W/body_sha fresh at n0 ~1.0 vs ~50% stale at n0.25), does honest end-to-end economics (M_total_f10 = tokens+browser_steps+latency+retrieval+verification+freshness with per-trajectory-reset honest sum-counters, 5000 family-stratified trajectory-grouped bootstrap CIs, rho_proxy_real>=0.50 per-stratum |rho_shuffled|<0.20) show residual-novelty rho_novelty>=0.60 vs |rho_length|<0.20 and Pareto dominance at f=10/100 vs RAG-EMBED TAU0.30/QCR, Stagehand 2x selector-cache+TTL, and Agentic Compilation DSM JSON IR O(1) $0.002-0.092 amortized (80-94% compile success, deterministic engine), with verification AUROC>=0.75 precision>=0.80 false_accept<=0.10 UNKNOWN precision>=0.85 per-class ECE<=0.15 Wilson, superseding falsified per_hit (1.005>0.85, rho 0.363<0.60)?

This is the smallest high-information gate that can change C-PRODUCT-ECON from HYPOTHESIS (bounded file-proxy REJECTED) to EXPERIMENTAL on valid substrate or PARK it even on honest substrate, directly testing product bottleneck (verification/UNKNOWN calibration, not retrieval) and external O(1) compilation threat. It formally supersedes the contested per_hit metric if M_total Pareto dominates decisively.

---

## 3. Hypothesis

H1 (primary): With health-gated single-node HS256 sticky substrate and correlated ETag freshness (fresh ~1.0 at n0 vs ~50% stale at n0.25, n_non304>=800 stratified 400/endpoint, single nginx $request_uri sticky + single gunicorn Flask HS256 PyJWT 2.14.0 WAL shared.db) and BrowserGym 2000-node heterogeneous real gpt-4o-mini 15-step tokens+browser_steps+latency, SPIDER freshness-gated inheritance (selector-cache + 10tok/30ms correlated probe + softmax temp0.15+jitter calibration) and DSM JSON IR O(1) (15tok+10ms amortized 800/f, 80-94% compile success deterministic) achieve:
- (a) residual-novelty tracking rho_novelty>=0.60 (Spearman pooled+per-stratum, 95% CI lower >=0.50 pooled >=0.45 per-stratum) with |rho_length|<0.20 and rho_proxy_real>=0.50 per-stratum |rho_shuffled|<0.20, and
- (b) M_total_f10/f100 Pareto dominance tokens>=30% and browser_steps+latency>=20% vs RAG-EMBED TAU0.30/QCR at f=10 and f=100 with accuracy>=0.85, correlated probe saving>=30% accuracy>=0.90 TN>=0.85, AUROC>=0.75 precision>=0.80 false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15, DSM amortized $0.002-0.092, safety CuP non-inferior.

Null hypothesis for controls: Shuffled bindings/probe/DSM/SGDR, length-constant cost, and random-key entry are uncorrelated with novelty/length and have AUROC~0.5, per spec NC.

---

## 4. State / Action / Target representation

- **State representation:** Mechanism preconditions = family+intent+site (+ state_key=family+DOM_hash for SGDR from BrowserGym CDP AX 2000 nodes if Docker else disclosed file-proxy hash). DOM hash = SHA256 of ordered AX tree snapshot (2000-node) truncated at 2000 nodes. Freshness feature = ETag W/body_sha + TTL max-age 60s + probeHit (200 vs 304) stratified.
- **Action representation:** Mechanism action_template with parameter slots `${param}` using dot-regex `r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` (supports nested e.g., `${user.profile.id}`). Binding via _bind full-match vs substring replacement. Verification via kernel.verify postconditions exact match.
- **Target (economics):** Per-trajectory M_total_f10 = sum_tokens + sum_browser_steps + latency_ms_equiv + retrieval (200) + DSM tool (15) + SGDR (180) + verification (50 tok+120ms per verify) + freshness probe (10tok+30ms per step) with per-trajectory-reset honest sum counters (no n*3200 bijective proxy). Derived M_per_hit = (M_total - retrieval/tool/DSM/SGDR - distill/compile - auditor)/L (probe stays in numerator). Primary metric for supersede is M_total_f10/f100 Pareto, not per_hit. Novelty fraction n = slots drawn from B (test) vs Curated-A (train) per family stratified by slot position, realized per trajectory 0/0.25/0.5/0.75/1.0.
- **Calibration target:** Verification confidence (softmax temp0.15+jitter) vs correctness (EXEC rows). AUROC, precision, false_accept, UNKNOWN_precision, per-class ECE 5-bin.
- **Safety target:** ST-WebAgentBench CuP violation rate for DSM tool-bypass vs RAG.

---

## 5. Sampling policy & holdout

- **Census:** Pip-installable WebArena-Verified Hard258 as primary heterogeneous task pool via `pip install browsergym webarena` or repo pip. If Docker image ghcr.io/servicenow/browsergym:0.14.3 unavailable or Hard258 pip manifest missing, fallback to WebArena-Verified v2 192 tasks across 36 orthogonal alias families (A/B disjoint alphabets, Jaccard<0.30 630 pairs via qcr_bank_manifest.json sha 8c69804b) as disclosed heterogeneous subset. Families stratified, trajectory-grouped.
- **Splits:** Per-family disjoint Curated-A (train, for registry induction + qcr bank + dsm + sgdr) / B (test, orthogonal slots) zero overlap. Frozen qcr_bank_manifest TAU0.30 same ranker TFIDF for RAG/SGDR. DSM registry 714/2147 from Curated-A TRAIN only. SGDR index 36 state_key TRAIN only. Test tasks never in curation.
- **Conditions:** 6 conditions x 5 novelty levels = 30 cells family-stratified (COLD, B-RAG, B-STAGEHAND-CACHE, P-STAGEHAND-TTL-CORRELATED, P-DSM-COMPILE-O1, P-SGDR-AWM). Plus 4 null controls trajectory-grouped permutations + ablations.
- **Browser substrate:** Docker BrowserGym 0.14.3 2000-node 1280x720 CDP getFullAXTree, Playwright 1.63.0, gpt-4o-mini 15-step budget same model/tools/budget across conditions. If Docker pull denied or OPENAI_API_KEY absent, primary gate is MEASUREMENT_INVALID (no fallback to file-proxy for SURVIVES).
- **Single-node substrate:** /tmp/spider-runtime/shared.db SQLite WAL single-worker gunicorn 23.0.0 + nginx 1.24.0 $request_uri sticky hash + PyJWT 2.14.0 HS256, If-None-Match/ETag W/body_sha conditional probe health-gated n_non304>=800 stratified 400/endpoint. Single-node is dependency gate per Director: runtime C-MEAS-VALID + graph C-FRESHNESS single-node validated.

---

## 6. Unit of analysis & holdout integrity

- Unit = trajectory (family-stratified, trajectory-grouped). Bootstrap and permutation respect trajectory grouping (block-permutation by trajectory/family, not transition). Stratified by family (36 families) and novelty fraction, with stratified endpoint counts for n_non304.
- Holdout = per-family train/test disjoint; frozen bank and registries TRAIN-only. Verify no test keys in curations via hash check; contamination => PC2 MEASUREMENT_INVALID.
- Preprocessing fit on TRAIN only (TFIDF, QCR bank). No post-state leakage into pre-state features. BrowserGym AX tree snapshot is pre-state only.

---

## 7. Baselines & controls (stable identities for AUDIT/DIRECTOR)

**Baselines (honest same splits, same probe/verify fallback, honest f=10/f=100 amortized, stratified):**
- B-COLD: no memory, 500 tok +2 browser_steps +50+120ms verify per step.
- B-RAG-EMBED-TAU030-QCR: TFIDF/Jaccard TAU0.30 top-1 QCR frozen bank, 200 tok+150ms retrieval.
- B-STAGEHAND-CACHE: DOM-hash selector cache without TTL, hit iff DOM identical (1.0 at n0, 0 at n>=0.25 orthogonal), 2x vendor baseline.
- P-STAGEHAND-TTL-CORRELATED (SUT): selector-cache + correlated 60s ETag probe 10tok+30ms health-gated stratified n_non304>=800 + verification calibration AUROC>=0.75.
- P-DSM-COMPILE-O1 (SUT/competitor): DSM JSON IR O(1) 714/2147 15tok+10ms amortized 800/f 80-94% compile $0.002-0.092 deterministic.
- P-SGDR-AWM (SUT): state-grounded 180tok+120ms rerank, 36 state_key TRAIN-only.

**Positive control PC-SINGLE-NODE-PARETO-CORRELATED (5 checks, any fail => MEASUREMENT_INVALID):**
- PC1 exact-repeat 1.0 hit at n0 5/5 spot-check,
- PC2 orthogonal Jaccard<0.30 max 0.0 + kernel dot-regex 5/5 EXECUTABLE confidence>=0.80 + correlated probe fresh~1.0 stale~50% accuracy>=0.90 saving>=30% TN>=0.85 stratified + DSM 714/2147 80-94% + SGDR 36 hit>=0.5 + Hard258 heterogeneous or disclosed 192/36 fallback,
- PC3 non-vacuous verify false_accept [0.10,0.60] confidence_std>0.05 AUROC null~0.5 true>=0.75,
- PC4 frozen formula within 1e-6 vs summed counters + n_non304 stratified logged,
- PC5 health-gate n_non304>=800 stratified 400/endpoint sticky single-worker HS256 + If-None-Match exercised + BrowserGym 2000-node if available.

**Null control NC-SINGLE-NODE-SHUFFLE-PIPELINE (via actual single-node pipeline, no simulated correctness):**
- NC1 shuffled slots + TTL map random 0.53 vs correlated + DSM + SGDR keys permuted trajectory-grouped: expect |rho|<0.25 ns, |rho_shuffled|<0.20 p>=0.20 per-stratum, |rho_length|<0.20, AUROC 0.45-0.60, success<=COLD, UNKNOWN>=0.80.
- NC2 random family/state keys: false_accept>=0.10 AUROC~0.5.
- NC3 length-constant cost L*500: |rho|~0 R2<0.15.
- NC4 ablations: correlated vs random delta>10%, DSM off vs on, SGDR vs RAG delta, single-node TN 0.85 vs per-node 0.667.

---

## 8. Metrics (stable names, with units)

- `rho_novelty` (Spearman M_per_hit vs n pooled + per-stratum stratified, 95% CI family-stratified trajectory-grouped bootstrap 5000) — primary economics calibration
- `rho_length` (|rho| M_per_hit vs L, pooled+per-stratum stratified) — must be <0.20
- `rho_proxy_real` (Spearman proxy cost vs real gpt-4o-mini tokens+browser_steps+latency pooled+per-stratum stratified) — must be >=0.50 per-stratum
- `rho_shuffled` (|rho| shuffled null pooled+per-stratum stratified, block-permutation 5000 p) — must be <0.20 p>=0.20
- `M_total_f10` , `M_total_f100` (tokens+browser_steps+latency+retrieval/verification/freshness per trajectory honest sum counters) + Pareto decompose tokens vs browser_steps+latency vs accuracy
- `M_per_hit` = (M_total - retrieval/tool/SGDR - distill/compile - auditor)/L (probe stays IN) — contested superseded gate
- `AUROC_verif` , `precision_verif` , `false_accept` , `UNKNOWN_precision` , `ECE_5bin_per_class` + Wilson CIs and bootstrap upper — calibration
- `toolHit` , `SGDRHitRate` , `cacheHit` , `probeHit_correlated` vs `probeHit_random` , `n_non304` stratified, `TN_freshness` — probe/registry diagnostics
- `violation_rate_CuP` (ST-WebAgentBench or synthetic proxy disclosed)
- `compile_success_DSM` , `amortized_cost_DSM` ($0.002-0.092)

All metrics report family-stratified trajectory-grouped bootstrap 5000 CIs and Wilson 95% for rates. Within-family std>0 required; degenerate CI[1,1] flags MEASUREMENT_INVALID. Stratified n_non304 counts required.

---

## 9. Decision rule (frozen, precedence ordered)

Computed on single-node health-gated n_non304>=800 stratified 400/endpoint + Docker BrowserGym 2000-node heterogeneous real tokens branch-derived f=10 honest per-trajectory-reset counters TRAIN-warmed.

1. **MEASUREMENT_INVALID** if any PC1-PC5 fails OR n_non304<800 stratified OR $request_uri sticky violated OR If-None-Match not exercised OR single-node HS256 not at /tmp/spider-runtime/shared.db WAL single-worker OR Docker BrowserGym 0.14.3 + gpt-4o-mini unavailable (rho_proxy_real unmeasurable) OR fixtures missing (Hard258 pip or 192/36 fallback with disclosure, qcr TAU0.30, dsm 714/2147, sgdr 36, cost_config) OR kernel dot-regex not patched OR TRAIN contamination OR degenerate null (|rho_shuffled|>=0.35 p<0.01 or within-std==0 or CI[1,1]) — irrespective of economics, no file-proxy fallback.

2. Else **FALSIFIED** if controls PASS non-degenerate but any primary gate fails: success at n0<0.85 (Wilson lower<0.80) OR AUROC<0.75 OR precision<0.80 OR false_accept>0.10 OR UNKNOWN<0.85 OR ECE>0.15 bootstrap upper>0.18 per-class OR rho_novelty<0.60 (CI lower<0.50 pooled or <0.45 per-stratum stratified) OR |rho_length|>=0.20 OR rho_proxy_real<0.50 per-stratum stratified OR |rho_shuffled|>=0.20 OR Pareto token saving <30% at f=10 vs RAG OR token saving <25% at f=100 OR browser+latency saving <20% OR accuracy<0.85 OR correlated probe saving<30% accuracy<0.90 TN<0.85 stratified OR DSM compile <80% or >94% detached or amortized outside $0.002-0.092 OR CuP violation >RAG+0.02 and >0.05 (absolute) with non-synthetic ST-WebAgentBench.

3. Else **SURVIVES** iff ALL hold with PC PASS non-degenerate stratified: (C1) success>=0.85 Wilson>=0.80 AUROC>=0.75 precision>=0.80 false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18; (C2) rho_novelty>=0.60 pooled CI>=0.50 per-stratum>=0.45 with |rho_length|<0.20 pooled+per-stratum stratified and rho_proxy_real>=0.50 per-stratum stratified |rho_shuffled|<0.20 p>=0.20; (C3) Pareto tokens>=30% vs RAG and browser+latency>=20% at f=10 and f=100 accuracy>=0.85 with correlated probe saving>=30% accuracy>=0.90 TN>=0.85 stratified and DSM 80-94% $0.002-0.092; (C4) CuP non-inferior or disclosed synthetic proxy not blocking if C1-C3 pass (flagged unresolved).

**SUPERSEDE clause (Director rationale):** If per_hit=(M_total - retrieval/tool/SGDR - distill/compile - auditor)/L CI clears >0.85 at BOTH n0 and n0.25 (5000 bootstrap, falsified 1.005>0.85 parent) but M_total_f10/f100 Pareto dominates decisively (tokens >=30% DSM >=25% SGDR >=30% StagehandTTL vs RAG at f=10 and f=100 latency>=20% accuracy>=0.85 rho_proxy_real>=0.50 per-stratum stratified n_non304>=800 stratified correlated delta>10% AUROC>=0.75 safety non-inferior) then per_hit artifact demonstrated and M_total Pareto supersedes per_hit as PRODUCT_CORE gate — verdict recommends supersession in handoff, not per_hit promotion.

Previous falsification bounded to file-proxy with rho 0.363<0.60 is NOT reopened without health-gated real-token replication.

---

## 10. Product consequences

**Positive (SURVIVES):** C-PRODUCT-ECON HYPOTHESIS → EXPERIMENTAL bounded to WebArena-Verified Hard258 heterogeneous single-node health-gated 1280x720 stratified (selector-cache+correlated-TTL/ETag 10 vs 50 vs 200 vs 15 DSM vs 180 SGDR honest f=10 + BrowserGym 2000-node rho validated). C-FRESHNESS → EXPERIMENTAL for correlated probe + C-RESIDUAL-NOVELTY economics validated at rho>=0.60. First valid single-node+real-token evidence that gated inheritance beats shipped Stagehand 2x cache+TTL and RAG and is Pareto-competitive with DSM O(1) $0.002-0.092 at f=10/100. Justifies shipping correlated-gating as interim vs Stagehand cache-only, with Pareto frontier + rho as pricing prior for compilation vs inheritance. No PRODUCT_CORE without explicit DIRECTOR promote_to_product true. DSM delta informs O(1) vs SGDR choice.

**Negative (FALSIFIED with controls PASS n_strat>=400 rho_proxy>=0.50 AUROC>=0.75):** Selector-cache+correlated ETag and DSM O(1) do NOT yield Pareto dominance or rho>=0.60 even on honest substrate; PARK C-RESIDUAL-NOVELTY/C-PRODUCT-ECON economics even on honest correlated substrate per Director PIVOT, pivoting Product to ST-WebAgentBench CuP or Intel diverse-site grounding or richer SPA sampling before PRODUCT_CORE. Joint falsification of DSM and SGDR triggers architecture choice: compilation vs continuous inheritance.

**Measurement invalid:** No claim update; handoff carries smallest next action (runtime single-node hardening, gunicorn 23.0.0/PyJWT 2.14.0 pin, nginx $request_uri sticky, BrowserGym pull/OPENAI_API_KEY, n_non304>=800 stratified, If-None-Match loop) without inventing economics. Preserves established/rejected distinctions.

---

## 11. Validity threats & controls

- **Representation loss:** DOM truncation at 2000 nodes, file-proxy hash fallback disclosed; browser events/network/auth/session preserved via Flask HS256 + BrowserGym AX.
- **Policy confounding:** Same gpt-4o-mini + same 15-step budget/tools across conditions; trajectory-grouped permutation isolates policy regularity from environment dynamics.
- **Site/task leakage:** Frozen qcr_bank TAU0.30 same ranker, hard families disjoint, site gating mandatory; audit recomputes parity within 1e-6 stratified.
- **Bijective proxy:** Honest per-trajectory sum counters enforced; any n*3200 reported => MEASUREMENT_INVALID.
- **Verification calibration threat:** Softmax temp0.15+jitter prevents linear 0.95-n*0.12 tautology; confidence_std>0.05 and AUROC vs shuffled null required; empty ECE bins disclosed stratified.
- **Stale freshness:** Seeded-42 0.53 decorrelated contrast vs correlated ETag W/body_sha fresh~1.0 isolates novelty correlation; TN>=0.85 health-gated stratified vs per-node 0.667 artifact.
- **Cost model threat:** DSM $0.002-0.092 amortized 800/f verified against real tool catalog, not assumed; per_hit excludes retrieval/tool/SGDR/compile but M_total includes them — Pareto vs per_hit artifact disclosed.
- **Safety threat:** ST-WebAgentBench CuP or disclosed synthetic proxy; DSM tool-bypass must not increase violation >0.05 absolute.
- **Stratification threat:** n_non304 must be ≥400 per endpoint; pooled 800 without stratification is insufficient.

---

## 12. Cost & information gain

**Estimated cost:** Moderate single-node health-gated stratified: 258 (or 192) x6 x5 levels =1290/960 + ~600-750 nulls + ~400-500 ablations = ~2290-2540 deterministic resolve/_bind/probe/DSM/SGDR verify trials on single-node HS256 sticky WAL + TFIDF offline. Wall <90min CPU proxy (<160min if Docker BrowserGym 2000-node loopback health-gated n_non304>=800 stratified). Storage ~3000-4000 row CSV + registry/dsm/sgdr + branch_traces. If Docker+gpt-4o-mini: 258x6x15 steps ~4650 browser calls ~3870 LLM calls <$30 plus snapshots/logs. Honest sum counters, no bijective n*3200.

**Expected information gain:** Decisive gating per Director after 15-streak invalid and bounded per_hit falsification 1.005>0.85. Health-gated single-node + TTL 60s correlated freshness + heterogeneous BrowserGym + AUROC calibration is diagnosed missing prerequisite. Smallest test that can change decision: positive reopens C-PRODUCT-ECON to EXPERIMENTAL and justifies interim shipping with Pareto pricing vs DSM O(1); per_hit artifact supersession formally replaces contested metric with M_total Pareto; double failure PARKs residual-novelty/DSM economics on honest substrate and forces pivot to CuP/richer SPA. Vs 18th alias permutation (0/10 mixed header+body+query+auth zero marginal gain) marginal information ~0. Pareto vs DSM is now product bottleneck, not retrieval.

---

## 13. Execution checklist (frozen, must log or MEASUREMENT_INVALID)

- [ ] Pin gunicorn 23.0.0 and PyJWT 2.14.0 exactly (vs installed 26.2.0/2.15.0 drift) before SURVIVES
- [ ] Provision /tmp/spider-runtime/shared.db WAL single-worker sticky, nginx 1.24.0 $request_uri hash, If-None-Match/ETag W/body_sha 200 vs 304, n_non304>=800 stratified 400/endpoint health-gated TN>=0.85
- [ ] Pip-install WebArena-Verified Hard258 + BrowserGym 0.14.3 2000-node 1280x720 CDP getFullAXTree; log versions, hashes, viewport, node count, image pull, OPENAI_API_KEY presence, rho_proxy_real per-stratum stratified
- [ ] Stage qcr_bank_manifest TAU0.30 Jaccard<0.30, dsm_registry 714/2147, sgdr_index 36 state_key TRAIN-only, cost_config 50/15/180/10, kernel dot-regex d926279d
- [ ] Run 5000 family-stratified trajectory-grouped bootstrap + 5000 block-permutation with per-stratum rho_length/shuffled/proxy thresholds stratified
- [ ] Report AUROC/precision/false_accept/UNKNOWN/ECE per-class + CuP safety (or synthetic proxy disclosed) + DSM $0.002-0.092 amortized + stratified n_non304
- [ ] Preserve raw evidence, recomputable hashes, frozen formula audit within 1e-6, unresolved distinct from measurement failure

*No outcome-bearing measurement was run during DESIGN. This preregistration is frozen before freeze.json.*
