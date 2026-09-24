# EXP-PRODUCT-35951662423 preregistration — Product C-PRODUCT-ECON Pareto supersession on health-gated single-node HS256 + BrowserGym

**Lane:** product | **Claim:** C-PRODUCT-ECON (C-RESIDUAL-NOVELTY auxiliary) | **Director action:** REOPEN cognitive_reset true parent disposition SUPERSEDE | **Experiment ID:** EXP-PRODUCT-35951662423

## 1. Binding mandate and strategic question

Director mandates REOPEN C-PRODUCT-ECON with SUPERSEDE of parent handoff EXP-PRODUCT-35949571341. The inherited `next_question` proposed repeating a distributed HS256 shared-WAL experiment that was already MEASUREMENT_INVALID twice for identical substrate absence (no shared.db, no PyJWT, no gunicorn, n_non304 null). Director supersedes that distributed target as overly ambitious and not minimal: single-node health-gated HS256 sticky $request_uri is the minimal viable honest substrate.

**Strategic question (binding):** On a health-gated single-node HS256 sticky $request_uri If-None-Match/304 substrate (n>=800 non-304, TTL 60s max-age conditional probe with ETag W/body_sha ~50% stale at n=0.25 vs ~1.0 at n=0) plus Docker BrowserGym 0.14.3 2000-node 1280x720 real gpt-4o-mini 15-step tokens/browser_steps+latency with rho_proxy_real>=0.50 and per-stratum |rho_shuffled|<0.20 and |rho_length|<0.20, does honest M_total_f10 Pareto dominance (tokens vs browser+latency vs accuracy at f=10/100, 5000 family-stratified bootstrap + 5000 block-permutation) superseding the contested per_hit=(M_total_f10 - retrieval - distill/compile - auditor)/L <=0.85 (falsified 1.005>0.85 rho 0.363<0.60) achieve dominance vs RAG-EMBED TAU0.30 QCR, Stagehand selector-cache+TTL (2x speedup ~30% cost) and WebMCP Registry 714/2147 O(1) compilation (800/f amortized) and SGDR/AWM with verification-derived calibration false_accept<=0.10 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18 and ST-WebAgentBench safety, thereby formally testing PRODUCT_CORE gate?

DESIGN converts this into the smallest rigorous falsifiable experiment below. No outcome-bearing measurement was inspected during DESIGN.

## 2. Inherited state (preserve established/rejected/unknown/do_not_assume)

**Continuity source:** `research/experiments/EXP-PRODUCT-35949571341/handoff.json` sha fe154850345223a6d607233a4e6cbae3b07b60a4fe656775df8dc09178fdd9ed, verdict MEASUREMENT_INVALID audit PASS.

**Established (carry_forward.established):** frozen inputs unmutated byte-identical; distributed HS256 shared-WAL single-worker sticky health-gated substrate entirely absent (no shared.db, no PyJWT, no gunicorn, nginx stock no sticky, n_non304 null); scientific and Docker substrate absent (numpy/scipy/sklearn/pandas, browsergym/playwright, BrowserGym image, OPENAI_API_KEY absent rho unmeasurable); fixtures absent (192/36 census, qcr_bank, webmcp_registry, sgdr_index); kernel HEAD 46929b3a lacks dot patch d926279d; producer correctly honored frozen falsifier precedence metrics {} controls UNKNOWN MEASUREMENT_INVALID no file-proxy fallback; maximum justified ceiling remains bounded file-proxy falsification Stagehand per_hit 1.045 CI[1.034,1.056]>0.85 and WebMCP 1.032>0.85 at n0 f=10 rho 0.472 |rho_length|0.306 Pareto M_total WebMCP 897 vs Stagehand 1773 vs RAG 3703 vs Cold 5497 hidden by per_hit artifact; audit PASS confirms no fabrication.

**Rejected (bounded):** Stagehand and WebMCP do NOT achieve per_hit <=0.85 vs RAG at n0 on 192/36 file-proxy honest f=10 (bounded REJECTED to file-proxy isolated SQLite without correlated freshness or BrowserGym); per_hit ~1.0 at n0 is metric-design artifact (both hit same 50-tok verify path retrieval 200 vs tool 15 vs SGDR 180 excluded) not viability evidence; rho_novelty 0.472<0.60 and |rho_length|0.306>0.20 so residual-novelty not demonstrated on file-proxy; no rejection of M_total Pareto on honest correlated substrate.

**Unknown (remains):** whether single-node HS256 health-gated $request_uri n_non304>=800 with correlated ETag conditional probe can be provisioned; whether Docker BrowserGym 2000-node real tokens with rho_proxy_real>=0.50 per-stratum thresholds can be provisioned; whether scientific stack 5000-bootstrap+5000-permutation computable; whether kernel dot patch reappliable and 5/5 EXECUTABLE; whether 192/36 orthogonal fixtures generable TRAIN-only; whether correlated freshness flips per_hit parity vs RAG; whether SGDR vs WebMCP delta <20%; whether M_total Pareto dominance supersedes per_hit; whether calibration and safety thresholds hold on honest substrate.

**Do_not_assume:** MEASUREMENT_INVALID is not falsification; file-proxy numbers do not transfer to honest substrate; per_hit ~1.0 artifact does not imply viability; seeded-42 random 0.53 stale != correlated freshness fresh ~1.0 vs ~0.5 n_non304>=800; per-node TN 0.667 != distributed/single-node TN 0.986; Docker/nginx binary presence != substrate availability; Pareto claim requires rho>=0.50 per-stratum |rho_length|<0.20 |rho_shuffled|<0.20 n_non304>=800 family-stratified bootstrap+permutation; safety not PASS until measured; kernel HEAD without dot insufficient; C-PRODUCT-ECON global rejection bounded to file-proxy only.

**Director SUPERSEDE disposition:** Parent handoff's distributed shared-WAL question is preserved as continuity evidence but not executed. This experiment tests the minimal single-node variant that retains health-gated $request_uri stickiness, correlated freshness, and BrowserGym real-token correlation required for a valid Pareto claim.

## 3. Question and hypothesis

See spec.json question. Hypothesis: single-node health-gated HS256 sticky correlated freshness is discriminating; Stagehand TTL, WebMCP O(1), SGDR will show M_total_f10 Pareto dominance vs RAG and Cold at f=10 and f=100 with accuracy>=0.85 while per_hit remains artifact ~1.0; correlated saving>=30% accuracy>=0.90; SGDR vs WebMCP delta <20% would show state-grounded retrieval captures O(1) benefit; rho_proxy_real>=0.50 validates proxy.

## 4. Falsifier with precedence (frozen)

Precedence-ordered per spec.json falsifier: PC/n_non304/health-gate/substrate/rho/fixtures/kernel TRAIN contamination -> MEASUREMENT_INVALID (no fallback, no n*3200, no seeded-42 proxy). Degenerate nulls (|rho_shuffled|>=0.35, within-std 0, CI[1,1]) -> MEASUREMENT_INVALID. Else FALSIFIED if any Pareto/calibration/safety gate fails when controls PASS. SUPERSEDE if per_hit fails but Pareto dominates decisively with thresholds.

## 5. Baselines and SUTs (stable identities)

- B-COLD — cold no-memory denominator.
- B-RAG-EMBED-TAU030-QCR — RAG TAU0.30 QCR primary comparator (200 tok retrieval).
- B-STAGEHAND-CACHE — Stagehand cache without TTL (shipped baseline).
- P-STAGEHAND-TTL — primary SUT Stagehand+correlated TTL (10 tok probe).
- P-WEBMCP-TOOL — secondary WebMCP 714/2147 O(1) 15 tok +800/f compile.
- P-SGDR-AWM — secondary SGDR 180 tok state-conditioned rerank.
All share identical 192 tasks / same frozen bank / same single-node health-gated $request_uri n_non304>=800 / same sgdr_index / same splits.

Frozen per_hit formula: M_per_hit = (M_total_f10 - retrieval_or_tool_or_SGDR - distill_compile_amort - auditor_amort)/L . Correlated probe cost stays IN. M_total_f10/f100 includes all plus browser+latency if Docker.

## 6. Positive and null controls (stable identities)

Positive control PC-SINGLE-NODE-PARETO-CORRELATED (5 gates): PC1 exact-repeat hit_rate 1.0 per_hit ~50; PC2 orthogonal Jaccard<0.30 kernel binding 1.0/1.0 confidence>=0.80 correlated probe fresh ~1.0 vs stale ~0.5 accuracy>=0.90 saving>=30% registry 714/2147 hit 1.0 SGDR 36 hit>=0.5; PC3 non-vacuous verify false_accept 0.10-0.60 confidence_std>0.05; PC4 frozen formula within 1e-6 rho logged; PC5 single-node health-gate n_non304>=800 sticky health_gated. Any fail -> MEASUREMENT_INVALID.

Null control NC-SINGLE-NODE-SHUFFLE-PIPELINE (4 gates): NC1 shuffled probe/registry/SGDR/adapter/cache via actual single-node pipeline Expect |rho|<0.25 |rho_shuffled|<0.20 per-stratum |rho_length|<0.20 success collapse; NC2 random entry Expect false_accept>=0.10; NC3 length-constant cost per_hit 500 Expect rho~0 R2<0.15; NC4 ablations correlated vs random delta >10% etc. Degenerate or warm-cache triggers MEASUREMENT_INVALID.

## 7. Measurement validity, metrics, and representation loss

Metrics (stable, units):
- M_total_f10_tokens, M_total_f100_tokens, M_total_f10_latency_ms, M_total_f10_browser_calls
- M_per_hit_f10_tokens, M_per_hit_f100_tokens
- success_rate (1.0 ideal at n0), accuracy vs novelty curve
- rho_novelty_per_hit (primary Spearman), rho_total, rho_length (pooled+per-stratum), rho_proxy_real (pooled+per-stratum), rho_shuffled (per-stratum)
- false_accept_rate, UNKNOWN_precision, ECE_5bin, ECE_bootstrap_upper, confidence_std, confidence_mean
- n_non304 count, probeHitRate per n, fresh_at_n0, stale_at_n0.25, saving_vs_fullVerify
- WebMCP lookup hitRate, SGDR hitRate, cacheHitRate per n, SGDR delta vs WebMCP, toolHit vs SGDRHit gaps, curatedDelta
- violation_rate per ST-WebAgentBench (or proxy)

Validity (MV1-MV13 in spec): census orthogonal families Jaccard<0.30; kernel dot-regex patched; single-node HS256 n_non304>=800 health-gated $request_uri; correlated TTL vs random contrast n_non304>=800; Docker BrowserGym rho>=0.50; WebMCP 714/2147 honest; SGDR TRAIN-only state_key 36; novelty hold-out QCR correct-family gating; length co-variation disclosure; baselines identical splits; abstention verification-derived non-vacuous; statistics family-stratified 5000 bootstrap +5000 block-permutation plus Pareto+ safety; safety ST-WebAgentBench.

Representation loss: file-proxy hash vs real BrowserGym CDP AX 2000-node DOM hash disclosed; body_sha vs full DOM ETag disclosed; single-node ignores distributed WAL contention; nginx $request_uri sticky approximates health-gate but not multi-worker load; synthetic orthogonal mock if fixtures absent bounds ceiling to synthetic; 8-14 step WebArena-Verified v2 templates vs full WebArena.

## 8. Decision rule (frozen thresholds)

Primary thresholds family-stratified pooled N~192 f=10 honest sum counters on single-node health-gated $request_uri n_non304>=800 + Docker BrowserGym real tokens. If substrate or rho unmeasurable or n<800 or sticky violated or SGDR missing -> MEASUREMENT_INVALID. Compute Wilson95% rates, bootstrap5000 CIs, block-permutation5000 p.

SURVIVES iff ALL: (C1) success at n0>=0.85 Wilson lower>=0.80 false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 bootstrap upper<=0.18; (C2) Pareto dominance: StagehandTTL or WebMCP or SGDR M_total_f10 saving >=30% tokens and >=20% browser+latency vs RAG at f=10 and at f=100 with accuracy>=0.85 and rho_proxy_real>=0.50 per-stratum |rho_length|<0.20 |rho_shuffled|<0.20 n>=800 correlated delta>10%; (C3) freshness saving>=30% accuracy>=0.90 falseAccept<0.05 fresh~1.0 stale 0.40-0.60 n>=800; (C4) controls all PASS non-degenerate orthogonal Jaccard<0.30 kernel binding 1.0/1.0.

FALSIFIED if controls PASS but any C1-C4 fails. SUPERSEDE if per_hit>0.85 (bootstrap CI clears, block p<0.01 at n0/n0.25) but C2-C4 PASS Pareto decisively -> recommend superseding per_hit with Pareto as gate. Else MEASUREMENT_INVALID.

Family-stratified bootstrap respects |rho_shuffled| and per-stratum thresholds; within-family std>0 check.

## 9. Validity threats and mitigations

- Health-gate / n_non304 gaming: require real If-None-Match exercised, 960/960 oracle-free probe TN>=0.85, disclose per-batch SELECT vs file-proxy, sticky hash logged; if n_non304<800 -> MEASUREMENT_INVALID.
- n*3200 bijective formula: honest summed M_total via single-node counters, audit within 1e-6.
- Jitter gaming: ECE bootstrap upper<=0.18 and confidence_std>0.05 alongside point ECE<=0.15.
- Degenerate CI[1,1]: flagged MEASUREMENT_INVALID not PASS.
- Test-warmed registry/probe/SGDR: verify TRAIN-only build via manifest hash and provenance chain; cross-family hitRate at n>=0.25 must not be 1.0.
- Task-length confound: per-stratum |rho_length|<0.20 and ANOVA disclosure.
- Proxy vs real divergence: rho_proxy_real>=0.50 pooled+per-stratum gates supersession; disclose.
- Seeded-42 random vs correlated freshness conflation: correlated flag true for SUTs, random NC-only, delta>10% required.
- Scope overclaim: SURVIVES ceiling bounded to WebArena-Verified v2 orthogonal single-node 192/36; no cross-site or full WebArena claim.

## 10. Consequences

Positive (SURVIVES): C-PRODUCT-ECON HYPOTHESIS->EXPERIMENTAL bounded to orthogonal single-node 192/36 with selector-cache+correlated-TTL/ETag (10 vs 50 vs 200 vs 15 vs 180 toks honest counters) and C-FRESHNESS->EXPERIMENTAL for correlated probe; first single-node+BrowserGym real-token evidence beating shipped Stagehand cache and RAG at honest cost with rho validated; SGDR vs WebMCP delta informs O(1) vs rerank choice; justifies shipping selector-cache+correlated-gating interim; no PRODUCT_CORE without DIRECTOR verdict.

Negative (FALSIFIED): if controls PASS non-degenerate but Pareto not dominant (saving <25% tokens or <20% latency or accuracy<0.85 or rho<0.50 or n<800 or calibration fails): selector-cache+correlated gating does NOT yield dominance even on honest single-node correlated substrate; and if WebMCP and SGDR also not Pareto at f=10/f100 -> joint falsification triggers PARK residual-novelty/WebMCP/SGDR economics even on honest substrate per Director PIVOT to CuP/richer SPA sampling.

Supersession (SUPERSEDE): if per_hit remains >0.85 but Pareto dominates decisively with thresholds PASS -> formally demonstrate per_hit artifact (excludes retrieval/tool/SGDR) and recommend superseding contested per_hit<=0.85 with M_total_f10 Pareto tokens vs browser+latency vs accuracy at f=10/100 as primary gate before promotion decision.

## 11. Estimated cost and information gain

Cost: ~1960 deterministic single-node pipeline trials (192x6x5 novelty + nulls+ablations) single SQLite WAL PyJWT nginx n_non304>=800 + TFIDF SGDR offline + wrong-bound branches; <80min CPU proxy (<140min with Docker BrowserGym Playwright loopback); storage per-task CSV ~3000 rows plus registry/sgdr/manifest hashes health-gated; Docker+gpt-4o-mini exploratory <$25; no LLM key for proxy gate.

Gain: Decisive gating per Director REOPEN SUPERSEDE cognitive_reset; per_hit already falsified 1.005>0.85 rho 0.363<0.60 |rho_length|0.306 on file-proxy; M_total_f10 Pareto vs shipped Stagehand/WebMCP/SGDR with real BrowserGym tokens+latency is only falsifiable product-defensible economics mapping to 8-14 step budgets; single-node health-gated n_non304>=800 correlated freshness is diagnosed missing prerequisite; smallest test that can reopen C-PRODUCT-ECON to EXPERIMENTAL on valid substrate (SURVIVES) or formally supersede per_hit with Pareto (SUPERSEDE) or permanently PARK residual-novelty economics even on honest substrate (FALSIFIED); vs repeating per_hit on same proxy expected PASS <0.1 would not change decision.

## 12. Provenance and reproducibility

Record: git base_sha 922763b9806a7fc914aa62351837dfa3e61bddce, request hash 0da1d29568fea7b44bfb323195b7d3762859abd4a40b2212a780ccfb80d61d48, prereg/spec hashes after freeze, kernel.py patched sha, src/spider/kernel.py line12 regex, registry.jsonl (36) webmcp_registry 714/2147 sgdr_index 36 hashes, qcr_bank_manifest hash, cost_config, shared.db WAL path sticky flag n_non304, nginx/gunicorn/PyJWT versions, BrowserGym 0.14.3 Playwright 1.63.0 viewport CDP AX hash, OPENAI_API_KEY hash placeholder, scipy/sklearn versions, per-task branch_traces and probe_traces correlated vs random, curated manifest. Fresh-context EXECUTE must verify frozen_input_hashes per freeze.json before running.
