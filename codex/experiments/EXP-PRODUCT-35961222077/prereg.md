# EXP-PRODUCT-35961222077 — Preregistration (Product REOPEN C-LLM-INHERIT)

**Lane:** product — **Claims:** C-LLM-INHERIT (primary, gated to C-PRODUCT-ECON / C-RESIDUAL-NOVELTY / C-FRESHNESS sub-evaluations)  
**Director mandate:** REOPEN with cognitive_reset=true, SUPERSEDE parent handoff, action REOPEN, claim_id C-LLM-INHERIT, comparative reasoning vs C-RESIDUAL-NOVELTY tuning and C-PARAM-INHERIT slot-syntax  
**Parent:** EXP-PRODUCT-35958402290 handoff MEASUREMENT_INVALID sha 60f491a6ba4cef9fc1da9dc3d4a88699e2dfb035b22de97861f6821712fabcfd — inherited state preserved per §2, Director SUPERSEDE governs this design  
**Status:** DESIGN — frozen inputs immutable after freeze.json; no outcome inspection permitted

---

## 1. Background & inherited scientific state (from parent handoff + Codex + Scout + Director)

**Established (bounded):**
- Frozen inputs byte-identical verified for parent (request 16e47e0f19cfcfbd5a2d0043fecd7bed9a2920da9c9207b120a975f40524bee6, spec 456a2e549253ce6e1b7ef38b63da070c7e00c8d3af79966748f53d4e9b524354, prereg a74bc9081de963b4dbd272adf5f84655b071ac61ca737aefeac09c9d7b1dc936, freeze 2026-09-24T05:09:24.251549Z) with provenance head 67101aa, no frozen file edited, audit PASS on transmission invariants.
- MV2 kernel dot-regex gate CLEARED only in working tree: `src/spider/kernel.py` line12 `r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` sha d926279d 5/5 EXECUTABLE confidence 0.85 with dot-nested binding (${item.id}, ${family.id}, ${site.name}, ${user.profile.id}) family-gate UNKNOWN; HEAD still pre-patch 46929b3a fails dot-nested — not durable across clean checkouts. Required for correct-family reconstruction.
- Bounded file-proxy falsification remains ceiling: WebArena-Verified v2 192/36 orthogonal alias families 630 pairs Jaccard 0.0 QCR TAU0.30 + honest f=10 sum counters; StagehandTTL per_hit 1.045 CI[1.034,1.056]>0.85 at n0 fails gate, WebMCP 1.032>0.85, rho_novelty 0.472 (<0.60) |rho_length|0.306 (>0.20), Pareto M_total_f10 WebMCP 897 vs Stagehand 1773 vs RAG 3703 vs Cold 5497 hidden by per_hit artifact (retrieval 200 vs tool 15 vs SGDR 180 excluded). No new Pareto/rho/calibration evidence from last invalid run (metrics null per contract, controls UNKNOWN except kernel sub-gate, outcome INCONCLUSIVE not FALSIFIED per audit PASS).
- Portfolio: C-FRESHNESS synthetic SURVIVES TN>=0.85 FA<=0.10 at 15% stale but confined to stdlib http.server flat-JSON; C-DELTA-REPAIR 1.0 repair 0.0 contamination synthetic; C-MEAS-VALID single-node HS256 gate MEASUREMENT_INVALID (wsgi path/factory ordering, EXP-RUNTIME-35949568321 wsgi import loop); C-PARAM-INHERIT stalled 8 consecutive MEASUREMENT_INVALID on WebArena-Verified; C-LLM-INHERIT starved 0/60 recent (last FALSIFIED 35797365772 synthetic overselling token saving); Frontier local attractor 17 alias/routing permutations pooled 21/40=0.525<0.60, 0/10 mixed/auth, zero marginal gain p=1.0; Product C-PRODUCT-ECON 17-streak all MEASUREMENT_INVALID after per_hit 1.005>0.85 rho 0.363<0.60 bounded file-proxy.
- Pin compliance partially achieved in parent working tree: gunicorn 23.0.0 PASS and pyjwt 2.14.0 PASS (vs drift 26.2.0/2.15.0), scientific stack installable numpy 2.5.3 scipy 1.18.1 sklearn 1.9.1 pandas 3.0.6 flask 3.1.3 de-risking 5000 bootstrap; nginx 1.24.0 binary present but $request_uri sticky not running.

**Rejected (bounded to file-proxy isolated SQLite, not global):**
- On file-proxy WebArena-Verified v2, per_hit<=0.85 viability FAILS: StagehandTTL per_hit 1.045>0.85 at n0 (requires <=0.85 at BOTH n0 and n0.25) and WebMCP 1.032>0.85 at n0, rho_novelty 0.472<0.60 |rho_length|0.306>0.20. This is metric-design artifact (both SUT and RAG hit same 50-tok verify after excluding 200 vs 15 vs 180) not evidence M_total Pareto fails.
- Kernel HEAD pre-patch regex `r'\$\{[A-Za-z_][A-Za-z0-9_]*\}'` fails dot-nested and was not durable.
- No rejection of honest single-node health-gated correlated freshness Pareto or residual-novelty rho>=0.60; no rejection of DSM O(1) 80-94% $0.002-0.092 amortized or SGDR vs DSM delta <20% or safety CuP on honest substrate; no rejection of real LLM inheritance vs instructions/RAG/Stagehand — those remain untested end-to-end with same model/tools/budget.

**Unknown (this experiment must resolve):**
- Whether /tmp/spider-runtime/shared.db WAL single-worker gunicorn 23.0.0 + nginx 1.24.0 $request_uri sticky hash + PyJWT 2.14.0 HS256 + real If-None-Match/ETag W/body_sha 200 vs 304 loop can be provisioned health-gated with n_non304>=800 stratified 400/endpoint TN>=0.85 freshness fresh ~1.0 at n0 vs ~0.5 stale at n0.25 saving>=30% accuracy>=0.90 falseAccept<0.05.
- Whether Docker BrowserGym 0.14.3 2000-node 1280x720 CDP Accessibility.getFullAXTree + gpt-4o-mini 15-step real tokens/browser_steps/latency exists (GHCR pull authorization + OPENAI_API_KEY provisioned) and file-proxy cost tracks real cost rho_proxy_real>=0.50 pooled+per-stratum with |rho_shuffled|<0.20 and |rho_length|<0.20.
- Whether sgdr_index 36 state_key TRAIN-only + WebArena-Verified Hard258 258-task heterogeneous census (or disclosed 192/36 fallback) + qcr_bank_manifest TAU0.30 Jaccard<0.30 + dsm_registry 714/2147 + cost_config 50/15/180/10 can be staged TRAIN-only without contamination (value_set_A intersect B empty) and measured with 5000 family-stratified trajectory-grouped bootstrap + 5000 block-permutation.
- Whether P-SPIDER freshness-gated 0.95/0.85 Jaccard 0.85 + deterministic localized repair + correct-family reconstruction (verified_state MEA auditor, TTL 60s max-age conditional probe) achieves margin >=0.12 vs EACH baseline (COLD, INSTRUCTIONS, RAG k5, Stagehand) at f=10/100 with AUROC>=0.75 precision>=0.80 false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 and M_total Pareto savings >=25% vs COLD <=0.85x vs RAG family-stratified, superseding per_hit artifact.

**Do_not_assume (must not be inferred from invalid prior):**
- MEASUREMENT_INVALID is infrastructure failure not scientific falsification per EXPERIMENT_PACKET s9; file-proxy per_hit~1.0 artifact (both SUT and RAG hit same 50-tok verify after excluding retrieval vs tool) does not imply M_total Pareto or LLM inheritance fails on honest health-gated substrate.
- Working-tree kernel patch d926279d is not committed: HEAD 67101aa still pre-patch 46929b3a (also parent verdict dac04e60 blob cfec9866); do not assume dot-regex durable across clean checkouts; must commit before SURVIVES claim.
- Installable scientific stack (numpy 2.5.3 etc) and now-compliant gunicorn 23.0.0/pyjwt 2.14.0 pins do not imply substrate health: nginx 1.24.0 binary present does not imply $request_uri sticky running or If-None-Match exercised or n_non304>=800 stratified 400/endpoint or TN>=0.85.
- Docker binary present and pip browsergym index entry exist do not imply BrowserGym image available (ghcr pull previously denied, no local image) or OPENAI_API_KEY provisioned; file-proxy fallback is banned by frozen falsifier for SURVIVES.
- Prior-run artifacts (qcr_bank_manifest 8c69804b, webmcp_registry af3c18e5 2147/714, tasks.json 391e8f6c 192/36, cost_config 55fa25af) are cross-experiment immutable references evidencing fixture availability for future staging, not this experiment's staged census; sgdr_index absent repo-wide, Hard258 census not staged for this experiment.
- Runtime C-MEAS-VALID single-node HS256 gate remains MEASUREMENT_INVALID (EXP-RUNTIME-35949568321 wsgi sys.path loop) and graph C-FRESHNESS only synthetic stdlib flat-JSON SURVIVES; do not assume distributed or single-node health-gated substrate validated beyond flat-JSON.
- Pareto vs per_hit supersession not tested: both per_hit and M_total remain null (explicit unknown per contract, not zero), controls UNKNOWN with no degenerate CI[1,1] or |rho_shuffled|>=0.35 false PASS; audit recomputed_metrics {} confirms no fabrication.

Director comparative reasoning adopted: Vs continuing per_hit 1.005 file-proxy optimization on 192/36 alias families: per_hit already FALSIFIED-IN-SETTING and superseded by M_total_f10 Pareto per handoff, and bijective n*3200 proxy invalid — further optimization has zero product decision value. Vs C-RESIDUAL-NOVELTY matched-novelty pilot alone: Product should test external-agent inheritance directly (cold vs instructions vs retrieval vs SPIDER) rather than only rho_novelty correlation; Frontier will simultaneously probe residual-novelty verification economics with honest sum-counter, covering economics orthogonal basin without duplication. Vs waiting for distributed WAL: product can proceed on single-node sticky HS256 which Graph/Runtime already validate, testing economics at f=10/100 without blocking on 2x shared-WAL.

Agent priors used (distinguished from SPIDER evidence): path dependence/local optima, long-horizon error compounding/verification bottleneck, measurement traps (degenerate CIs, bijective proxy), generalization vs memorization (zero-overlap holdout), exploration cost structure (rho_novelty vs rho_length, Pareto vs per_hit).

---

## 2. Research question (Director binding, refined to falsifiable gate)

On health-gated single-node HS256 sticky $request_uri If-None-Match/304 substrate (n_non304>=800 stratified 400/endpoint where needed) plus Docker BrowserGym 0.14.3 2000-node 1280x720 CDP AX>10 and real gpt-4o-mini 15-step Playwright (same model/tools/budget), with honest per-trajectory-reset sum counters resolve+bind+verify+freshness+browser_steps (no jitter/n*3200/f*6.0, |rho_shuffled|<0.20, rho_proxy_real>=0.50, per-stratum |rho_length|<0.20, trajectory-grouped B=5000 bootstrap + 5000 block-permutation) and family hold-out (train A test never-observed B value_set_A intersect B empty, orthogonal alias families Jaccard<0.30, L=8-14 family-specific), does SPIDER (freshness-gated 0.95/0.85 Jaccard 0.85 + deterministic localized repair + correct-family reconstruction, verified_state MEA auditor, TTL 60s max-age conditional probe ETag W/body_sha) vs B-COLD vs B-INSTRUCTIONS vs B-RAG-EMBED TAU0.30/QCR k5 vs Stagehand selector-cache achieve success margin >=0.12 vs each baseline at f=10/100, false_accept<=0.10 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18, verification AUROC>=0.75 precision>=0.80, and honest amortized saving >=25% vs COLD and <=0.85x vs RAG (family-stratified CIs) plus Pareto M_total tokens vs browser+latency vs accuracy dominance, superseding falsified per_hit 1.005>0.85 rho 0.363<0.60?

This is the smallest high-information gate that can change C-LLM-INHERIT from HYPOTHESIS (0/60 starved, last FALSIFIED synthetic) to EXPERIMENTAL on valid substrate or PARK it even on honest substrate, directly testing product core promise 'real LLM agent benefits from SPIDER beyond strong memory/instruction baselines' with same model/tools/budget — never before tested end-to-end. It formally supersedes contested per_hit metric if M_total Pareto dominates decisively.

---

## 3. Hypothesis

H1 (primary, C-LLM-INHERIT): With health-gated single-node HS256 sticky substrate and correlated ETag freshness (fresh ~1.0 at n0 vs ~50% stale at n0.25, n_non304>=800 stratified 400/endpoint, single nginx 1.24.0 $request_uri sticky hash + single gunicorn Flask HS256 PyJWT 2.14.0 WAL shared.db) and BrowserGym 0.14.3 2000-node 1280x720 CDP AX + gpt-4o-mini 15-step same model/tools/budget, SPIDER freshness-gated inheritance (Jaccard 0.95/0.85 alias 0.85 + deterministic localized repair single-field re-bind + correct-family reconstruction via dot-regex + TTL 60s max-age conditional probe 10tok+30ms + verified_state MEA auditor softmax temp0.15+jitter UNKNOWN<0.80) will:

- (a) achieve success margin >=0.12 vs EACH of B-COLD, B-INSTRUCTIONS, B-RAG-EMBED k5, B-STAGEHAND-CACHE at f=10 and f=100 (Wilson lower + bootstrap CI);
- (b) satisfy calibration: false_accept<=0.10, UNKNOWN precision>=0.85, ECE<=0.15 per-class 5-bin bootstrap upper<=0.18, AUROC>=0.75 precision>=0.80, confidence_std>0.05;
- (c) achieve residual-novelty tracking rho_novelty>=0.60 pooled+per-stratum with |rho_length|<0.20 and |rho_shuffled|<0.20, rho_proxy_real>=0.50 per-stratum where BrowserGym real tokens measured, and M_total_f10/f100 Pareto dominance tokens>=25% vs COLD and <=0.85 vs RAG at both f=10/f=100 with browser+latency >=20% saving, correlated probe saving>=30% accuracy>=0.90 TN>=0.85.
- (d) supersede per_hit artifact: if per_hit remains >0.85 at n0/n0.25 but M_total Pareto dominates, recommend formal supersession.

Null for controls: Shuffled bindings/probe/registry, length-constant cost, and random-key entry are uncorrelated with novelty/length and have AUROC~0.5, per spec NC.

---

## 4. State / Action / Target representation

- **State representation:** Mechanism preconditions = family+intent+site (+ state_key=family+DOM_hash for SGDR if exercised from BrowserGym CDP AX 2000 nodes). DOM hash = SHA256 of ordered AX tree snapshot truncated at 2000 nodes, viewport 1280x720. Freshness feature = ETag W/body_sha + TTL max-age 60s + probeHit (200 vs 304) stratified 400/endpoint. Family orthogonality Jaccard<0.30 ensures state distinctness.
- **Action representation:** Mechanism action_template with parameter slots `${param}` using dot-regex `r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` (supports nested e.g., `${user.profile.id}`, `${item.id}`). Binding via _bind full-match vs substring replacement. Verification via kernel.verify postconditions exact match + MEA auditor verified_state.
- **Target (inheritance):** Per-trajectory success (binary: task completed correctly vs not) under same gpt-4o-mini 15-step Playwright budget; cost target per-trajectory M_total_f10/f100 = sum_tokens + sum_browser_steps + latency_ms_equiv + retrieval (200) + verification (50 tok+120ms per verify) + freshness probe (10tok+30ms per step) with per-trajectory-reset honest sum counters (no n*3200). Derived M_per_hit = (M_total - retrieval/tool/SGDR - distill/compile - auditor)/L (probe stays in). Novelty fraction n = slots drawn from B (test) vs Curated-A (train) per family stratified by slot position, realized per trajectory 0/0.25/0.5/0.75/1.0; L 8-14 family-specific constant within family orthogonal to n.
- **Calibration target:** Verification confidence (softmax temp0.15+jitter [-0.05,0.05]) vs correctness (EXEC rows). AUROC, precision, false_accept, UNKNOWN_precision, per-class ECE 5-bin.
- **Cost model:** Honest sum counters; probe 10 vs retrieval 200 vs SGDR 180 vs DSM 15 (if exercised) honored; no bijective proxy.

---

## 5. Sampling policy & holdout

- **Census:** Pip-installable WebArena-Verified Hard258 as primary heterogeneous task pool via `pip install browsergym webarena` or repo pip. If Docker image ghcr.io/servicenow/browsergym:0.14.3 unavailable or Hard258 pip manifest missing, fallback to WebArena-Verified v2 192 tasks across 36 orthogonal alias families (A/B disjoint alphabets, Jaccard<0.30 630 pairs via qcr_bank_manifest.json 8c69804b, tasks.json 391e8f6c) as disclosed heterogeneous subset. Families stratified, trajectory-grouped.
- **Splits:** Per-family disjoint Curated-A (train, for registry induction + qcr bank + sgdr) / B (test, orthogonal slots) zero overlap value_set_A intersect B empty. Frozen qcr_bank_manifest TAU0.30 same ranker TFIDF for RAG. Registry 714/2147 equiv from Curated-A TRAIN only. Test tasks never in curation.
- **Conditions:** 5 conditions x 5 novelty levels = 25 cells family-stratified (B-COLD, B-INSTRUCTIONS, B-RAG-EMBED k5, B-STAGEHAND-CACHE, P-SPIDER-FRESH-REPAIR-LLM). Plus 4 null controls trajectory-grouped permutations + ablations. Same model/tools/budget per condition.
- **Browser substrate:** Docker BrowserGym 0.14.3 2000-node 1280x720 CDP getFullAXTree, Playwright 1.63.0, gpt-4o-mini 15-step budget same model/tools/budget across conditions. If Docker pull denied or OPENAI_API_KEY absent, primary gate is MEASUREMENT_INVALID (no fallback to file-proxy for SURVIVES per Director).
- **Single-node substrate (where needed):** /tmp/spider-runtime/shared.db SQLite WAL single-worker gunicorn 23.0.0 + nginx 1.24.0 $request_uri sticky hash + PyJWT 2.14.0 HS256, If-None-Match/ETag W/body_sha conditional probe health-gated n_non304>=800 stratified 400/endpoint. Validated TN>=0.85 vs per-node 0.667 artifact. Log shared.db WAL worker=1 JWT alg TN n_non304 stratified sticky hash ETag.

---

## 6. Unit of analysis & holdout integrity

- Unit = trajectory (family-stratified, trajectory-grouped). Bootstrap and permutation respect trajectory grouping (block-permutation by trajectory/family, not transition). Stratified by family (36 families) and novelty fraction, with stratified endpoint counts for n_non304 where applicable.
- Holdout = per-family train/test disjoint; frozen bank and registry TRAIN-only. Verify value_set_A intersect B empty via hash check; contamination => PC MEASUREMENT_INVALID.
- Preprocessing fit on TRAIN only (TFIDF, QCR bank). No post-state leakage into pre-state features. BrowserGym AX tree snapshot is pre-state only. Same gpt-4o-mini model/tools/budget across conditions ensures policy confounding controlled.
- Per-hit isolation: M_per_hit reported per trajectory excluding fixed retrieval/distill but including probe; M_total reported for economics. Probe stays in numerator to avoid per_hit artifact.

---

## 7. Baselines & controls (stable identities for AUDIT/DIRECTOR)

**Baselines (honest same splits, same probe/verify fallback, honest f=10/f=100 amortized, stratified, same LLM budget):**
- B-COLD: no memory, 500 tok +2 browser_steps +50+120ms verify per step. Denominator for saving.
- B-INSTRUCTIONS: hand-authored family template prompt, 200 tok instruction amortized f=10->20 (f=100->2) + full steps.
- B-RAG-EMBED-TAU030-QCR-K5: TFIDF/Jaccard TAU0.30 top-k k=5 (k1 sensitivity) QCR frozen bank, 200 tok+150ms retrieval, verbatim bind only.
- B-STAGEHAND-CACHE: DOM-hash selector cache without TTL, hit iff DOM identical (1.0 at n0, 0 at n>=0.25), 50 tok+120ms +1 step hit.
- P-SPIDER-FRESH-REPAIR-LLM (SUT): selector-cache + correlated 60s ETag probe 10tok+30ms health-gated n_non304>=800 stratified + correct-family reconstruction + deterministic localized repair + verified_state MEA auditor softmax temp0.15+jitter UNKNOWN<0.80.

**Positive control PC-SINGLE-NODE-LLM-PARETO-CORRELATED (5 checks, any fail => MEASUREMENT_INVALID):**
- PC1 exact-repeat 1.0 hit at n0 5/5 spot-check via health-gated sticky,
- PC2 orthogonal Jaccard<0.30 max 0.0 + kernel dot-regex 5/5 EXECUTABLE confidence>=0.80 + value_set disjoint + correlated probe fresh~1.0 stale~50% accuracy>=0.90 saving>=30% TN>=0.85 stratified,
- PC3 non-vacuous verify false_accept [0.10,0.60] confidence_std>0.05 AUROC null~0.5 true>=0.75,
- PC4 frozen formula within 1e-6 vs summed counters + n_non304 stratified + rho_proxy_real logged,
- PC5 health-gate n_non304>=800 stratified 400/endpoint sticky single-worker HS256 + If-None-Match exercised + BrowserGym 2000-node gpt-4o-mini 15-step health AX>10.

**Null control NC-SINGLE-NODE-SHUFFLE-PIPELINE-LLM (via actual pipeline, no simulated correctness):**
- NC1 shuffled slots + TTL map random 0.53 vs correlated + correct-family keys permuted trajectory-grouped: expect |rho|<0.25 ns, |rho_shuffled|<0.20 p>=0.20 per-stratum, |rho_length|<0.20, AUROC 0.45-0.60, success<=COLD, UNKNOWN>=0.80.
- NC2 random family/state keys: false_accept>=0.10 AUROC~0.5.
- NC3 length-constant cost L*500: |rho|~0 R2<0.15.
- NC4 ablations: correlated vs random delta>10%, single-node TN 0.85 vs per-node 0.667.

---

## 8. Metrics (stable names, with units)

- `success_rate` per condition/n (binary, Wilson 95% CI) and `success_margin_vs_baseline` (SPIDER minus each baseline at f=10/100, bootstrap CI) — primary LLM inheritance
- `false_accept` (EXECUTABLE wrong binding failing verify via MockEnv 15% wrong-bound)
- `UNKNOWN_precision` = TP_UNKNOWN/(TP+FP_UNKNOWN) where UNKNOWN correct when freshness<0.25 or confidence<0.80 or probe stale
- `ECE_5bin_per_class` + bootstrap upper (EXEC rows only, 3 empty bins disclosed, 5-bin)
- `AUROC_verif` , `precision_verif` (confidence vs correctness)
- `M_total_f10` , `M_total_f100` (tokens+browser_steps+latency+retrieval/verification/freshness per trajectory honest sum counters) + Pareto decompose tokens vs browser_steps+latency vs accuracy
- `M_per_hit` = (M_total - retrieval/tool/SGDR - distill/compile - auditor)/L (probe stays IN) — secondary superseded gate
- `rho_novelty` (Spearman M_per_hit vs n pooled + per-stratum stratified, 95% CI 5000 bootstrap) — residual-novelty tracking
- `rho_length` (|rho| M_per_hit vs L, pooled+per-stratum stratified) — must be <0.20
- `rho_proxy_real` (Spearman proxy cost vs real gpt-4o-mini tokens+browser_steps+latency pooled+per-stratum stratified) — must be >=0.50 where Docker measured
- `rho_shuffled` (|rho| shuffled null pooled+per-stratum stratified, block-permutation 5000 p) — must be <0.20 p>=0.20
- `probeHit_correlated` vs `probeHit_random` , `n_non304` stratified, `TN_freshness` — probe diagnostics
- `R2_novelty` , `R2_length` , `R2_delta` per spec if reported

All metrics report family-stratified trajectory-grouped bootstrap 5000 CIs and Wilson 95% for rates. Within-family std>0 required; degenerate CI[1,1] flags MEASUREMENT_INVALID. Stratified n_non304 counts required where substrate exercised.

---

## 9. Decision rule (frozen, precedence ordered)

Computed on health-gated single-node n_non304>=800 stratified 400/endpoint where substrate needed + Docker BrowserGym 2000-node heterogeneous real tokens branch-derived f=10 honest per-trajectory-reset counters TRAIN-warmed. Same model/tools/budget across conditions.

1. **MEASUREMENT_INVALID** if any PC1-PC5 fails OR n_non304<800 stratified where substrate required OR $request_uri sticky violated OR If-None-Match not exercised where required OR single-node HS256 not at /tmp/spider-runtime/shared.db WAL single-worker OR Docker BrowserGym 0.14.3 + gpt-4o-mini 15-step unavailable (rho_proxy_real unmeasurable) OR fixtures missing (Hard258 pip or 192/36 fallback with disclosure, qcr TAU0.30, dsm 714/2147, sgdr 36, cost_config) OR kernel dot-regex not patched OR TRAIN contamination (value_set_A intersect B non-empty) OR bijective proxy detected OR degenerate null (|rho_shuffled|>=0.35 p<0.01 or within-std==0 or CI[1,1] or confidence_std<=0.05) — irrespective of economics, no file-proxy fallback for SURVIVES.

2. Else **FALSIFIED** if controls PASS non-degenerate but any primary gate fails: success margin <0.12 vs any baseline at f=10 or f=100 (CI includes <=0) OR success at n0<0.85 OR false_accept>0.10 OR UNKNOWN<0.85 OR ECE>0.15 bootstrap upper>0.18 per-class OR AUROC<0.75 OR precision<0.80 OR rho_novelty<0.60 (CI lower<0.50 pooled or <0.45 per-stratum) OR |rho_length|>=0.20 OR rho_proxy_real<0.50 per-stratum OR |rho_shuffled|>=0.20 OR M_total_f10 saving <25% vs COLD OR M_total ratio >0.85 vs RAG at f=10 or f=100 OR browser+latency saving <20% OR correlated probe saving<30% accuracy<0.90 TN<0.85 stratified. Controls must be PASS non-degenerate.

3. Else **SURVIVES** iff ALL hold with PC PASS non-degenerate stratified: (C1) success margin >=0.12 vs EACH baseline at f=10 and f=100 (Wilson+bootstrap CI >0, success>=0.85 at n0) AND false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18 AND AUROC>=0.75 precision>=0.80; (C2) rho_novelty>=0.60 pooled CI>=0.50 per-stratum>=0.45 with |rho_length|<0.20 pooled+per-stratum and rho_proxy_real>=0.50 per-stratum |rho_shuffled|<0.20 p>=0.20; (C3) Pareto tokens>=25% (Director mandates >=30% vs RAG where measured) vs B-RAG and browser+latency>=20% at f=10 and f=100 accuracy>=0.85 with correlated probe saving>=30% accuracy>=0.90 TN>=0.85 stratified and same-model LLM replication logged; (C4) safety non-inferior if measured or disclosed synthetic proxy not blocking if C1-C3 pass.

**SUPERSEDE clause (Director rationale):** If per_hit=(M_total - retrieval/tool/SGDR - distill/compile - auditor)/L CI clears >0.85 at BOTH n0 and n0.25 (5000 bootstrap, parent falsified 1.005>0.85 rho 0.363<0.60) but M_total_f10/f100 Pareto dominates decisively (tokens >=30% vs RAG and browser+latency >=20% at both f, accuracy>=0.85, rho>=0.60 per-stratum n>=400, AUROC>=0.75, correlated delta>10% vs seeded-42 0.53) then per_hit artifact demonstrated and M_total Pareto supersedes per_hit as PRODUCT_CORE gate — verdict recommends supersession, not per_hit promotion. Previous per_hit falsification bounded to file-proxy with rho 0.363<0.60 is NOT reopened without health-gated real-token replication.

---

## 10. Product consequences

**Positive (SURVIVES):** C-LLM-INHERIT HYPOTHESIS → EXPERIMENTAL bounded to WebArena-Verified Hard258 heterogeneous single-node health-gated 1280x720 stratified with same gpt-4o-mini 15-step Playwright (freshness-gated 0.95/0.85 Jaccard 0.85 + deterministic localized repair + correct-family reconstruction + TTL 60s ETag W/body_sha + verified_state MEA auditor). C-FRESHNESS → EXPERIMENTAL for correlated probe + C-RESIDUAL-NOVELTY economics validated at rho>=0.60. First valid single-node+real-token evidence that a real LLM agent benefits from SPIDER beyond strong baselines (cold vs instructions vs RAG k5 vs Stagehand) with margin >=0.12 and Pareto economics >=25% saving <=0.85 vs RAG. Justifies shipping SPIDER inheritance as interim vs Stagehand cache-only, with Pareto frontier and rho as pricing prior for compilation vs inheritance. No PRODUCT_CORE without explicit DIRECTOR promote_to_product true.

**Negative (FALSIFIED with controls PASS n_strat>=400 rho_proxy>=0.50 AUROC>=0.75):** Real LLM inheritance does NOT yield margin >=0.12 or Pareto dominance or rho>=0.60 even on honest substrate; PARK C-LLM-INHERIT/C-PRODUCT-ECON economics even on honest correlated substrate per Director PIVOT, pivoting Product to ST-WebAgentBench CuP or Intel diverse-site grounding or richer SPA sampling or DSM/SGDR O(1) architecture before PRODUCT_CORE. Joint falsification triggers architecture choice: inheritance vs compilation.

**Measurement invalid:** No claim update; handoff carries smallest next action (runtime single-node hardening, gunicorn 23.0.0/PyJWT 2.14.0 pin, nginx $request_uri sticky, BrowserGym pull/OPENAI_API_KEY, n_non304>=800 stratified, If-None-Match loop, kernel patch) without inventing economics. Preserves established/rejected/unknown/do_not_assume distinctions.

---

## 11. Validity threats & controls

- **Representation loss:** DOM truncation at 2000 nodes, file-proxy hash fallback disclosed; browser events/network/auth/session preserved via Flask HS256 + BrowserGym AX.
- **Policy confounding:** Same gpt-4o-mini + same 15-step budget/tools across conditions; trajectory-grouped permutation isolates policy regularity from environment dynamics.
- **Site/task leakage:** Frozen qcr_bank TAU0.30 same ranker, orthogonal families Jaccard<0.30 value_set_A intersect B empty, site gating mandatory; audit recomputes parity within 1e-6 stratified.
- **Bijective proxy:** Honest per-trajectory sum counters enforced; any n*3200/f*6.0/jitter => MEASUREMENT_INVALID.
- **Verification calibration threat:** Softmax temp0.15+jitter prevents linear 0.95-n*0.12 tautology; confidence_std>0.05 and AUROC vs shuffled null required; empty ECE bins disclosed stratified.
- **Stale freshness:** Seeded-42 0.53 decorrelated contrast vs correlated ETag W/body_sha fresh~1.0 isolates novelty correlation; TN>=0.85 health-gated stratified vs per-node 0.667 artifact.
- **Cost model threat:** Honest sum counters; probe 10 vs retrieval 200 vs SGDR 180 honored; per_hit excludes retrieval/tool but M_total includes them — Pareto vs per_hit artifact disclosed. Family-stratified CIs prevent degenerate [1.0,1.0].
- **LLM non-determinism:** Same model seed temp0 for determinism; gpt-4o-mini 15-step budget fixed; trajectory-grouped bootstrap respects correlation.
- **Stratification threat:** n_non304 must be ≥400 per endpoint; pooled 800 without stratification insufficient.
- **Contamination:** TRAIN-only induction; test B never in curation; hash verification.

---

## 12. Cost & information gain

**Estimated cost:** Moderate single-node health-gated stratified + LLM replication: 258 (or 192) x5 x5 levels =1290/960 + ~600-750 nulls + ~200 ablations = ~2290-2540 deterministic resolve/_bind/verify trials on single-node HS256 sticky WAL + TFIDF offline. Wall <90min CPU proxy (<160min if Docker BrowserGym 2000-node loopback health-gated n_non304>=800 stratified heterogeneous). Storage per-trajectory CSV ~3000-4000 rows branch_traces. If Docker+gpt-4o-mini: 258x5x15 steps Playwright ~3600-4650 browser_calls ~2880-3870 gpt-4o-mini calls <$30 plus snapshots/logs. Honest sum counters, no bijective n*3200.

**Expected information gain:** Decisive gating per Director REOPEN SUPERSEDE cognitive_reset: C-LLM-INHERIT starved 0/60 recent and Product 17-streak local attractor on per_hit 1.005>0.85 rho 0.363<0.60 already superseded by M_total Pareto — further per_hit tuning has zero decision value. Health-gated single-node + TTL 60s correlated probe is minimal realistic staleness regime that makes LLM inheritance discriminating, and comparing vs shipped Stagehand 2x and RAG k5 and instructions with same model/tools/budget directly measures commercial viability and dominates narrow Stagehand test because it integrates calibration and Pareto economics. Single-node correlated freshness (fresh at n0 ~1.0 vs 0.53 random) with health-gated $request_uri n_non304>=800 stratified plus BrowserGym 2000-node heterogeneous and AUROC calibration is diagnosed single missing prerequisite before PARK or metric supersession. Smallest test that can change decision: positive reopens C-LLM-INHERIT to EXPERIMENTAL and justifies interim shipping with Pareto pricing; per_hit artifact supersession formally replaces contested metric with M_total Pareto; double failure PARKs LLM inheritance even on honest substrate and pivots to CuP/richer SPA. Vs 18th alias permutation marginal ~0. High leverage.

---

## 13. Execution checklist (frozen, must log or MEASUREMENT_INVALID)

- [ ] Pin gunicorn 23.0.0 and PyJWT 2.14.0 exactly before SURVIVES
- [ ] Provision /tmp/spider-runtime/shared.db WAL single-worker sticky, nginx 1.24.0 $request_uri hash, If-None-Match/ETag W/body_sha 200 vs 304, n_non304>=800 stratified 400/endpoint health-gated TN>=0.85 where substrate needed
- [ ] Pip-install WebArena-Verified Hard258 + BrowserGym 0.14.3 2000-node 1280x720 CDP getFullAXTree + gpt-4o-mini 15-step same model/tools/budget; log versions, hashes, viewport, node count, image pull, OPENAI_API_KEY, rho_proxy_real per-stratum stratified
- [ ] Stage qcr_bank_manifest TAU0.30 Jaccard<0.30 630 pairs 0.0, value_set disjoint, dsm_registry 714/2147, sgdr_index 36 state_key TRAIN-only, cost_config 50/15/180/10, kernel dot-regex d926279d; verify TRAIN-only no contamination
- [ ] Run honest per-trajectory-reset sum counters (no n*3200/jitter), family-stratified trajectory-grouped 5000 bootstrap + 5000 block-permutation with per-stratum rho_length/shuffled/proxy thresholds stratified
- [ ] Report success margin >=0.12 vs each baseline at f=10/100, AUROC/precision/false_accept/UNKNOWN/ECE per-class, Pareto M_total vs RAG, rho_novelty>=0.60, rho_proxy_real>=0.50, TN, probeHit correlated vs random, n_non304 stratified
- [ ] Preserve raw evidence, recomputable hashes, frozen formula audit within 1e-6, unresolved distinct from measurement failure

*No outcome-bearing measurement was run during DESIGN. This preregistration is frozen before freeze.json.*
