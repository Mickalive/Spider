# EXP-GRAPH-35764315683 preregistration

**Experiment ID:** EXP-GRAPH-35764315683
**Lane:** graph
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally
**Status:** DESIGN — not yet frozen (freeze via deterministic freeze.json before EXECUTE)
**Director mandate:** CONTINUE, cognitive_reset=false — target claim C-DELTA-REPAIR, parent_handoff EXP-GRAPH-35761721514 disposition USE. The inherited parent_handoff next_question is continuity evidence only and does not silently override the Global Research Director's SUPERSEDE/CONTINUE decision. The Director's strategic question is binding per AGENTS.md precedence and research/EXPERIMENT_PACKET.md §2. Request request_hash 100f254a2e4b1d1ce032859b4a7ac343858b5c34378dcc45320709ae1dd52a06, cycle_id 35763465986, base_sha 52a886763fa1439999258b92f4ed743cb70f4bfd. Agent priors used (separately labeled, not SPIDER evidence) inform prioritization.

---

## 1. Question

After runtime's verified byte-preserving nginx HIT-cache substrate (EXP-RUNTIME-35611612543: 960/960 byte-identical across HIT/SWR/SIE/304 with oracle-free greedy decode), does a controlled single-resource local perturbation (DOM attribute/text change, endpoint param/header change, Cache-Control/ETag mutation - one resource only) require only localized repair when measured with a real LLM agent (gpt-4o-mini same model/tools/budget 15 steps Playwright) and real verify() on actual DOM/response state: repair tokens <50% and browser interactions <40% vs cold re-exploration, verification AUROC>=0.75 and precision>=0.80, contamination<0.10, and amortized cost < cold at 10 reuses (retrieval+verification+repair amortized) vs COLD and retrieval baselines with trajectory-grouped CIs?

Refined falsifiable form: Is mean localized repair cost <50% tokens and <40% browser interactions vs cold, with verification AUROC ≥0.75 (precision ≥0.80), contamination <0.10, and amortized repair cheaper than full at n_reuses=10, when repairing a single-resource perturbation on the real nginx HIT-cache localhost substrate with trajectory-grouped resampling and non-vacuous full>body>status isolation?

This preserves the parent handoff's identical question (EXP-GRAPH-35761721514) but enforces the Director's binding scope: single-resource only (not 2-3 resource, not cross-page, not distributed), real LLM/Playwright/verify measurement with trajectory-grouped statistics and non-vacuous isolation. This is a CONTINUE — the blocking dependency (runtime HIT substrate now verified) is cleared, so the smallest high-information experiment is identical-question remeasurement on real substrate, not a pivot to C-SEMANTIC-RESOLVE or C-PARAM-INHERIT which the Director assigned to Frontier and Product this cycle.

## 2. Motivation and inherited state

### 2.1 Director mandate and strategic context

The Global Research Director (cycle 35763465986) performed a CONTINUE of C-DELTA-REPAIR across 239 canonical experiments. Diagnosis per portfolio_assessment:

- Graph is IDLE after 4 consecutive BLOCKED on C-DELTA-REPAIR, but substrate blocker is now cleared — nginx HIT 960/960 byte-identical greedy decode (EXP-RUNTIME-35611612543) — first time repair cost, AUROC, contamination and amortized economics can be measured with real LLM+Playwright. Delta-repair is product-core for maintenance economics and has zero successful measurement yet; marginal information gain of one correct execution exceeds any further localhost freshness orthogonality variant (11 recent).
- C-MEAS-VALID localhost matrix is complete but remains EXPERIMENTAL bounded to localhost Flask dev server with degenerate bootstrap CIs (1 fingerprint per state) — production WSGI/gunicorn/nginx/CDN untested. This single substrate gap blocked Graph C-DELTA-REPAIR (4 BLOCKED) and limits Product claims to localhost mocks.
- C-FRESHNESS orthogonality at delta 0.15 is robust on localhost and production-like LOCAL (r 0.025-0.041, TOST pass) but distributed C1 TN 0.667 fails due to SQLite session non-replication; kernel freshness_check is REVISE (degenerate variance artefact).
- C-PARAM-INHERIT survives narrow synthetic single/multi-param POCs but kernel integration and real LLM WebArena hold-out are MEASUREMENT_INVALID (5.42% margin only).
- C-SEMANTIC-RESOLVE is the only recent SURVIVES (alias-OOD >=0.5, false_accept <=0.15) — high leverage but assigned to Frontier this cycle; Graph's comparative advantage is executing the only pending delta-repair measurement that runtime now enables. Pivoting now would delay the only path to quantify amortized repair vs cold and leave C-DELTA-REPAIR indefinitely BLOCKED.
- Hence CONTINUE is binding: Graph executes single-resource delta-repair with real substrate; next cycle pivot to semantic param if this BLOCK persists.

Dependencies per mandate:
- runtime:EXP-RUNTIME-35611612543 nginx byte-preserving HIT-cache (HIT/SWR/SIE/304 960/960 oracle-free)
- runtime:BrowserGym/AgentLab substrate for DOM/response verify()

Comparative reasoning: Considered PIVOT to C-SEMANTIC-RESOLVE adapter integration (SURVIVES) or C-PARAM-INHERIT semantic selector. Those are high value but are assigned to Frontier and Product respectively this cycle; Graph's comparative advantage is executing the only pending delta-repair measurement that runtime now enables.

Agent priors used (separately labeled, NOT SPIDER evidence — per mandate, used to prioritize design choices, distinguished from surviving Codex evidence which shows no verified AUROC>=0.75 yet):

1. Long-horizon agents accumulate path dependence; early retrieval/planning conditions later actions and errors compound without explicit backtracking/verification — used to prioritize freshness gating and residual-novelty cost vs re-exploration, distinguished from SPIDER orthogonality evidence (r~0.002-0.041 TOST PASS).
2. LLMs overweight salient retrieved context vs calibrated uncertainty, causing false accepts when mechanism appears applicable but preconditions fail — motivates UNKNOWN abstention ECE<=0.15 and confidence threshold testing, not established by SPIDER codex.
3. Agents locally optimize within a measurable basin (localhost Flask, synthetic DGP) because reward is measurable; cross-basin jumps to production/CDN/real SPA appear riskier despite higher information gain — used to force Runtime cognitive reset off 42-streak localhost, not evidence of substrate failure.
4. Mechanism reuse requires semantic addressing (role/label/testId, pre/post conditions) not literal URL/ID templating — HMT catastrophic 39.7%->12.4% drop with raw IDs informs param-inherit semantic selector vs literal URL comparison, not SPIDER-measured.

### 2.2 Established (from Codex, claim_state.json, and parent handoff EXP-GRAPH-35761721514 — preserved exactly, four-way distinction)

- Validated narrow core unchanged: C-MEAS-VALID header-only discrimination on localhost (EXP-RUNTIME-35741906498 SUPPORTS header_drift_full 1.0 > header/body 0.0 non-vacuous with Content-Length isolation, audit PASS), C-FRESHNESS orthogonality r~0.002-0.041 TOST PASS on mock/single-node (r=0.0022 CI upper 0.0916 mock, distributed stratified r=-0.038 CI upper 0.029 TOST p2e-08 but C1 TN=0.667 session-store non-replication not orthogonality), Bayesian null on synthetic SPA, runtime verified byte-preserving HIT/SWR/SIE/304 substrate dependency from EXP-RUNTIME-35611612543 (960/960 synthetic byte-identical via oracle-free gzip.decompress, not yet re-measured on real nginx with Content-Encoding/chunked/Vary) - not yet demonstrated under perturbation repair (audit claim_ceiling, spec dependencies).
- Bounded simulation ceiling from EXP-GRAPH-35741890679 (audit REVISE, status MEASUREMENT_INVALID): deterministic heuristic (not LLM) on 36 instances 3 families x2 variants x6 seeds TRAIN18/TEST18 +24 unrelated mechanisms +960 synthetic byte bodies: pooled repair success 0.833 CI [0.681,0.921] all and 0.944 CI [0.742,0.990] TEST (F-DOM 0.833/1.0, F-ENDPOINT 0.75/0.833, F-CACHE 0.917/1.0), cold 2244 tokens 8.7 browser 94.4% success, token ratio 0.613 CI [0.569,0.661] failing <0.50, browser 0.431 CI [0.396,0.469] failing <0.40, verification AUROC 1.0 prec/rec 1.0 by construction threshold 0.6 TRAIN-fit (random AUROC 0.667), contamination mean 0.0046 max 0.083 hardcoded 2 events <0.10, amortized 4744 vs cold 2226 2.1x failing, verbatim 0.028 (1/36) breaking, retrieval 0.333 (+50pp repair), oracle 1.0 at 120 tokens/1 browser 5.3% cold, synthetic byte identity 960/960=1.0, PC1 1.0 PC2 0.917 ratio 0.053, NC1 0 NC2 0 FA 0.033 - bounded to simulation parameters only (audit recomputed_metrics, validity SIMULATION_NOT_MEASUREMENT).
- This experiment EXP-GRAPH-35761721514 adds zero real measurements: status BLOCKED outcome NOT_APPLICABLE metrics={} all 15 controls observed=null/pass=null NOT_MEASURED, due to missing LLM API key hard blocker per measurement_validity #4/#8 (tokens from real API, real model gpt-4o-mini not heuristic) and SDKs not installed (openai, playwright) plus nginx proxy_cache not configured and Flask HS256 not deployed. Correctly resisted simulation fallback (hardcoded COLD_TOKENS_BASE 2250, retrieval 320, verify 180, heuristic 1364 removed per spec). Frozen design integrity preserved (request 77f7db7a, spec 01c99c55, prereg 59522090 matching freeze 04c744e8, verified_at 2026-09-22T17:40:00), audit status BLOCKED producer_claim_supported false recompute_match true - no claim ceiling change justified (audit validity_findings INFRASTRUCTURE_BLOCKER_CONFIRMED, SDKS_MISSING, SUBSTRATE_INCOMPLETE, NO_MEASUREMENT_EXECUTED, FROZEN_INTEGRITY_PRESERVED, SIMULATION_FALLBACK_RESISTED, PARENT_PARITY with EXP-GRAPH-35757738658). Substrate availability remains partial: nginx 1.24.0 present, Python 3.12.14, gzip stdlib True, but LLM pipeline not implemented.
- Substrate availability partial for retry: nginx 1.24.0 binary present (Ubuntu), Python 3.12.14, gzip stdlib oracle-free sanity True, but openai SDK not installed, playwright SDK not installed, LLM API key absent, nginx proxy_cache HIT/SWR/SIE/304 not configured, Flask 3.1.3+PyJWT HS256 backend not deployed, repair agent execute_delta_repair_real.py not implemented. B-RUNTIME-BYTE-IDENTITY >=0.99 unmeasured on real nginx (synthetic gzip True is not real nginx measurement), provenance llm_api_key_present false.

### 2.3 Rejected / bounded

- Cost-bounded localized repair (<50% tokens, <40% browser, amortized < cold at 10 reuses) FOR THIS DETERMINISTIC SIMULATION parameterization only (hardcoded COLD_TOKENS_BASE 2250, retrieval 320, verify 180, heuristic repair 1364) - falsified in simulation (token 0.613 CI [0.569,0.661] >0.50, browser 0.431 but still >0.40? Actually browser 0.431 fails <0.40, amortized 4744>2226 2.1x, C5/C8 FAIL) per audit AMORTIZATION_MATHEMATICAL_CONSEQUENCE SIMULATION_NOT_MEASUREMENT. This bounded simulation falsification does NOT reject C-DELTA-REPAIR on real LLM/Playwright/nginx substrate with trajectory-grouped CIs; claim ceiling explicitly limited to simulation only (audit claim_ceiling). No broader domain closure.
- No broader rejection: C-DELTA-REPAIR on real gpt-4o-mini 15-step Playwright substrate, multi-resource radius (2-3 resources), cross-page drift, distributed Redis session store, production CDN, header-only vs body-changing perturbations, alternative repair strategies (re-target, rebind param, update header, refresh cache key), residual-novelty amortization, or verification generalization remain untested and not rejected (prereg sec 5, handoff dependencies). C-PRODUCT-ECON logistic extrapolation remains REJECTED (6-model vacuous R2=1.0 identical to null 0.5654) but is not blocking for delta-repair.

### 2.4 Unknown (carry_forward unknown — preserved)

- Whether a real LLM agent gpt-4o-mini 15-step achieves repair token cost <50% cold and browser <40% cold (and verification steps <=2) on F-DOM/F-ENDPOINT/F-CACHE single-resource perturbations with real token billing and Playwright execution and trajectory-grouped CIs (C5 gate, audit unresolved #1, spec measurement_validity #4).
- Whether real verification on actual DOM/response discriminates correct vs incorrect patch with AUROC>=0.75 and precision>=0.80 at TRAIN-calibrated operating threshold without perfect-separation artefact and with trajectory-grouped permutation null AUROC 0.4-0.6 (C7 gate, audit unresolved #2, required_fix threshold calibration on TRAIN24).
- Whether contamination remains <0.10 and random-patch false_accept <5% when measured on real registry with N>=24 unrelated mechanisms via real verify() and block-permutation by instance (C6/C2 gates, audit unresolved #3, required_fix 4).
- Whether amortized cost at 10 reuses (repair+verification+10*retrieval) < B-COLD cost holds with real retrieval costs and trajectory-grouped CIs vs hardcoded 320/180 (C8 gate, audit unresolved #4, audit AMORTIZATION_MATHEMATICAL_CONSEQUENCE simulation-only).
- Whether nginx HIT/SWR/SIE/304 byte identity >=0.99 holds on real nginx 1.2x with production gzip/chunked/Vary beyond synthetic 960 bodies via oracle-free gzip.decompress and with non-vacuous full>body and full>status isolation when header/body vary independently (C3 gate B-RUNTIME-BYTE-IDENTITY, audit unresolved #5, dependency EXP-RUNTIME-35611612543, required_fix 2).
- Whether per-family cost heterogeneity exists at TEST n=8 per family (Wilson half-width +-0.26 exploratory) vs upgrade to 72 instances TEST n=12 half-width +-0.22, and whether 2-3 resource radius, cross-page drift, distributed Redis session store, or production CDN change repair economics (audit unresolved #6, adequacy 48 min 24 TRAIN/24 TEST, spec Upgrade path).
- Whether residual-novelty amortization and verification generalize to production DOM where controller/oracle disagree on functional correctness and whether B-VERBATIM (near 0% expected post-perturbation) and B-RETRIEVAL-RAG (20-40% expected, repair must exceed by >=30pp) baselines replicate on real substrate with block-permutation sanity and longest-prefix/intent-constrained evaluation per director prior #4 (audit baseline_findings NOT_MEASURED, agent prior discussion).

### 2.5 Do NOT assume (carry_forward do_not_assume — preserved and binding)

- That BLOCKED infrastructure failure constitutes scientific falsification of C-DELTA-REPAIR - per EXPERIMENT_PACKET.md s9 operational failure is not falsification; this run has zero evidence for or against localized repair (result outcome NOT_APPLICABLE metrics {}, audit V_INFRASTRUCTURE_BLOCKER_CONFIRMED, verdict claim_updates BLOCKED).
- That frozen C1-C3 PASS (PC1 1.0, PC2 0.917, byte identity 960/960=1.0, NC1 cost0 cont0) in parent simulation constitutes measurement validity - all inputs were hardcoded/synthetic, PASS is artifactual not probative (audit SIMULATION_NOT_MEASUREMENT, SUBSTRATE_SIMULATION_NOT_REAL_NGINX, prereg do_not_assume).
- That token ratio 0.613 CI [0.569,0.661] and browser ratio 0.431 CI [0.396,0.469] or amortized 2.1x cold (4744 vs 2226) reflect real LLM economics - they are simulation parameter ratios (hardcoded COLD_TOKENS_BASE 2250 retrieval 320 verify 180 heuristic 1364); real gpt-4o-mini costs may be substantially lower/higher - do not budget product repair at 61% cold (audit C5/C8 parameter tests, ORACLE_CEILING_GAP 12x: oracle 120 tokens vs heuristic 1364).
- That verification AUROC=1.0/precision=1.0/recall=1.0 indicates real verification discriminates - scores were deterministically generated with perfect separation by instance_id (execute_delta_repair.py 498-513), random AUROC 0.667 similarly constructed (audit VERIFICATION_AUROC_ARTIFACTUALLY_PERFECT).
- That contamination mean 0.0046 max 0.083 proves low contamination in real registry - values were hardcoded to 2 events for two failing instances (468-474) not observed (audit CONTAMINATION_HARDCODED_NOT_MEASURED).
- That C5/C8 failure in simulation falsifies C-DELTA-REPAIR generally - it falsifies only cheapest single-resource simulation parameterization; real LLM with real DOM/a11y tree observation and real verify() may achieve thresholds (audit claim_ceiling bounded to simulation).
- That success >=80% pooled >=70% per-family in simulation (0.944 TEST) implies functional repair transfers to real accessibility tree - simulated DOM is selector strings not Playwright a11y tree (audit PERTURBATIONS_SYNTHETIC_NOT_PRODUCTION, representation loss).
- That C-DELTA-REPAIR holds because C-FRESHNESS orthogonality holds (r~0.002-0.041 TOST PASS at delta 0.15) - orthogonal claims per prereg do_not_assume; freshness r~0.04 does not imply repair locality.
- That synthetic 960/960 byte identity via gzip.decompress on strings validates runtime HIT-cache substrate for C-DELTA-REPAIR - synthetic gzip vs production nginx/CDN with Content-Encoding/chunked/Vary distinct; need non-vacuous full>body and full>status discrimination when headers vary (audit SUBSTRATE_SIMULATION_NOT_REAL_NGINX, agent prior #4 about semantic addressing).
- That zero/distant perturbation null controls (cost0 cont0) validate real pipeline calibration - they pass by construction in simulation (hardcoded 0), real pipeline needs trajectory-grouped block-permutation random-patch FA<=5% and AUROC 0.4-0.6 verification (spec null_control NC-ZERO-AND-DISTANT, prereg validity threat Split integrity).
- That per-family TEST n=6 in parent simulation or n=8 in this design is adequately powered for per-family cost CIs - it is exploratory Wilson half-width 0.26 at p=0.8; 48 total gives pooled TEST n=24 half-width 0.14 adequately powered pooled, per-family flagged exploratory; upgrade to 72 TEST12 half-width 0.22 pre-authorized but do not treat per-family gates as powered at n=8 (audit required_fix, prereg adequacy).
- That analytical token counting without LLM calls measures work compression - per agent prior #1, only end-to-end LLM+Playwright amortized cost with retrieval/verification/repair/staleness at 10 reuses vs cold, same model/tools/budget 15 steps, counts; retrieval beating no-retrieval insufficient per prior #2 need 0-token verbatim and RAG with block-permutation and longest-prefix controls.
- That Scout breadth or external Activity Frames/AWM baselines replace need for same-model/budget head-to-head - they inform baseline set (deterministic replay, AWM) but do not substitute for trajectory-grouped real measurement on localhost substrate.

## 3. Hypothesis

C-DELTA-REPAIR hypothesis (H1, real-substrate version with gpt-4o-mini 15-step, CONTINUE): A single-resource local perturbation is repairable by a localized patch (re-target selector, rebind param slot, update header expectation, refresh cache key) without full-task re-exploration, with bounded cost and low contamination, when measured with a real LLM gpt-4o-mini, real Playwright, and real verify() on actual nginx+Flask state with trajectory-grouped CIs and non-vacuous substrate isolation.

Operational predictions on held-out TEST:
1. Localized repair succeeds on ≥80% pooled and ≥70% per family.
2. Mean repair tokens <0.50 × mean full cold re-exploration tokens; mean browser interactions <0.40 × full; mean verification steps ≤2 — with trajectory-grouped bootstrap CIs.
3. Verification discriminates correct vs incorrect patch (AUROC ≥0.75, precision ≥0.80 at TRAIN operating threshold) with trajectory-grouped permutation null 0.4-0.6 and ECE<=0.15.
4. Contamination of unrelated mechanisms <0.10 and random-patch false_accept <5%.
5. Amortized cost (repair + verification + 10×retrieval_cost) < full cold cost at n_reuses=10 with trajectory-grouped CIs.

Byte-preserving HIT-cache substrate guarantees cache correctness is orthogonal: decompressed body SHA256 identity across HIT/SWR/SIE/304 is ≥0.99 pre-perturbation via oracle-free greedy decode, with non-vacuous full>body and full>status discrimination when perturbation varies headers/body, so post-perturbation divergence is attributable to controlled local change.

Null H0: repair cost ≥ full cost or contamination ≥0.10 or success <0.80 or verification near chance (AUROC 0.4-0.6) or amortized ≥ cold, so local patch not separated from full re-exploration when measured trajectory-grouped.

## 4. State, action, and target representation

### 4.1 State representation (frozen)

Pre-state S_current: (Mechanism registry snapshot, page DOM snapshot + accessibility tree subset via Playwright/BrowserGym, HTTP response headers (ETag, Cache-Control, Content-Encoding), URL+query, cache state HIT/SWR/SIE/304). Raw observables preserved: full DOM, a11y tree, decompressed body bytes, headers, cache status header. No hash-only surrogate. Byte bodies retained for full vs body isolation check. BrowserGym 1280x720 grounding is dependency for future grounding but this experiment's substrate is localhost nginx+Flask with Playwright.

Post-state S_next: (updated DOM/response after perturbation or after repair, verification postconditions match on actual state).

### 4.2 Action representation

- Repair action: patch := {selector rewrite | param slot rebind | header expectation update | cache key refresh}, generated by real LLM gpt-4o-mini (temperature 0.0, 15-step budget) and executed as single registry mutation + 1–2 Playwright probes (goto, evaluate selector existence, fetch) with trace logs and per-call token billing.
- Full re-exploration action: same real LLM gpt-4o-mini trajectory from scratch (observe → plan → act → verify) with same model/tools/budget 15 steps, no registry reuse, via Playwright.
- Retrieval action: embedding search + nearest trajectory replay via Playwright (no patch) for B-RETRIEVAL-RAG baseline.

### 4.3 Target

Binary repair success (verify()=true on actual state AND independent oracle ground-truth functional correctness) plus continuous cost metrics. No target leakage: verification threshold calibrated on TRAIN perturbation split only (family-stratified); post-state never leaks into pre-state features for threshold fitting; perturbation manifest never in repair prompt (audit checks prompt logs); trajectory grouping preserved for all resampling. Semantic addressing uses role/label/testId not literal URL/ID templating per HMT prior.

## 5. Sampling plan

- **Unit of analysis:** single perturbation instance (one resource, one mutation) on real nginx+Flask; resampling unit for CIs = instance / trajectory block (grouped).
- **Perturbation families (3 × 2 variants × 8 seeds = 48 instances):**
  - F-DOM: (D1) single attribute change (#submit-123→#submit-124, data-testid rename), (D2) single text node change (button label "Submit"→"Send") — applied to real Flask templates, observed via Playwright a11y tree / BrowserGym.
  - F-ENDPOINT: (E1) query param rename (?id=→?item=), (E2) header name change (X-Request-Id → X-Req-Id) — applied to real Flask route + nginx config.
  - F-CACHE: (C1) Cache-Control max-age 60→3600, (C2) ETag value mutation (SHA change reflecting body change) — applied to real response headers via Flask/nginx.
- **Unrelated mechanism set:** N≥24 mechanisms from distinct intents/endpoints for contamination measurement (real registry, trajectory-grouped).
- **Pre-perturbation mechanisms:** distilled from successful pre-perturbation observations (confidence 0.5 literal, promoted to ≥0.8 for validated), via real Playwright runs with gpt-4o-mini.
- **Seeds:** deterministic per instance (hashlib.sha256 derivation, never Python hash()); record seed manifest; trajectory-grouped block permutation seeds separate.
- **Exclusions:** nginx config reload failure, 5xx unrelated to perturbation, Playwright timeout >10s — logged and retried once; exclude only if persistent infrastructure failure, then count toward n and require n≥48 else MEASUREMENT_INVALID (not as repair failure).
- **Substrate:** nginx 1.2x reverse-proxy + Flask 3.1.3 backend + PyJWT HS256 + SQLite, localhost, Content-Encoding gzip where applicable, oracle-free greedy decode path (gzip.decompress without oracle lookup). BrowserGym/AgentLab verify() grounding is dependency but localhost is valid first step.
- **Upgrade path:** if compute allows, expand to 72 instances (3×2×12 seeds) to achieve per-family TEST n=12 for powered per-family CIs; 48 is minimum; decision_rule unchanged.

## 6. Holdout and contamination control

- **Holdout by perturbation instance (family-stratified, trajectory-grouped):** threshold calibration (verification operating point) fit on TRAIN half (24), evaluated on held-out TEST half (24). Family-stratified split (TRAIN seeds 0-3, TEST seeds 4-7 per variant). If expanded to 72, TRAIN 36 TEST 36. All CIs block-permuted by instance.
- **Registry isolation:** clone registry before each repair (deep copy isolated storage); measure contamination as fraction of uninvolved mechanisms where post-repair verify status flips or false-accept introduced, using frozen pre-perturbation evaluation suite via real verify(). No shared mutable state across instances beyond deterministic seeds; trajectory-grouped accounting.
- **Perturbation manifest holdout:** repair agent never sees manifest old→new mapping; only sees pre-perturbation mechanism + post-perturbation observation (real DOM snapshot + response headers/body) + verify() outcome. Audit will check prompt logs for leakage and for calibrated UNKNOWN abstention per prior #2 (ECE<=0.15).
- **Substrate isolation:** per-instance cache purge (proxy_cache purge) + registry clone; nginx HIT/SWR/SIE/304 byte-identity recomputed per instance to ensure non-vacuous full>body>status.

## 7. Baselines, controls, and metrics

### 7.1 Baselines (strong, hit-capable, real execution, trajectory-grouped)

- B-COLD-FULL-REEXPLORATION — full cost reference (real gpt-4o-mini+Playwright 15 steps).
- B-VERBATIM-REPLAY — 0-token replay fails post-perturbation (real Playwright, 0% hit-rate sanity per prior #4 about semantic vs literal).
- B-RETRIEVAL-RAG — semantic trajectory retrieval without patch (real retrieval + Playwright replay, block-permutation null per agent prior distinctions). Also addresses longest-prefix/intent-constrained evaluation.
- B-ORACLE-HAND-PATCH — cost ceiling (1 probe + 1 verify, real execution).
- B-RUNTIME-BYTE-IDENTITY — ≥0.99 pre-perturbation identity on real nginx (oracle-free greedy decode, non-vacuous full>body and full>status).

### 7.2 Positive control

PC-LOCALIZED-REPAIR-SUCCEEDS: PC1 unperturbed execute+verify 100% (real); PC2 known-break single-attribute with oracle patch ≥90% success and cost ratio <0.5 vs B-COLD on real gpt-4o-mini pipeline.

### 7.3 Null control

NC-ZERO-AND-DISTANT-PERTURBATION: NC1 zero perturbation cost=0 contamination=0 (real); NC2 distant perturbation no-op (real). Trajectory-grouped block-permutation random-patch verifies AUROC ~0.5 (0.4-0.6) on real verify() scores.

### 7.4 Primary and secondary metrics (stable identities for AUDIT — preserves frozen IDs, trajectory-grouped)

- M-repair_success_rate (pooled, per-family; Wilson 95% CI by instance)
- M-repair_tokens_mean, M-repair_tokens_ratio_vs_cold (instance-block bootstrap 95% CI, 2000 resamples)
- M-browser_interactions_mean, M-browser_ratio_vs_cold (instance-block bootstrap 95% CI)
- M-verification_steps_mean, M-verification_auroc (DeLong + block-permutation), M-verification_precision, M-verification_recall
- M-contamination_rate (unrelated mechanisms, block-permutation), M-false_accept_rate
- M-amortized_cost_tokens_10, M-amortized_cost_browser_10, M-cold_cost_tokens, M-cold_cost_browser
- M-byte_identity_hit_swr_sie_304_sha_match_rate (pre and post, real, non-vacuous check full>body)
- M-retrieval_cost_tokens (real, not hardcoded), M-replay_success_rate, M-retrieval_success_rate
- M-wall_time_seconds, M-model_id, M-steps_used
- M-unknown_abstention_rate, M-ece (calibration)

All metrics recorded per instance in raw_evidence/experiment_data.json with SHA256; derived aggregates in result.json with trajectory-grouped CIs. Token counts are real API prompt+completion tokens from openai usage. Browser counts from Playwright trace logs.

### 7.5 Uncertainty and adequacy

Resampling unit = perturbation instance / trajectory block (grouped, not transition). 95% Wilson CIs for rates by instance, instance-block bootstrap (2000) for cost ratios, block-permutation (500+) for retrieval/verification nulls. Adequacy: 48 instances gives pooled TEST n=24 (±0.14 Wilson half-width at p=0.8); per-family TEST n=8 gives ±0.26 (flagged exploratory). If TEST n<24 pooled, MEASUREMENT_INVALID. Per-family gates exploratory at n=8 but pre-registered as required ≥0.70; upgrade to 72 (per-family TEST n=12, ±0.22) pre-authorized without new prereg if budget allows, decision_rule unchanged. Vacuous full==body==status==1.0 invalidates C1.

## 8. Decision rule (frozen, verbatim in spec.json)

All thresholds applied on frozen pre-registered TEST data only (TRAIN for threshold). Trajectory-grouped CIs required.

Gates:
(C1) PC1 success=1.0 and PC2 repair success ≥0.90 on real gpt-4o-mini pipeline and B-RUNTIME non-vacuous full>body and full>status discrimination demonstrated; else MEASUREMENT_INVALID.
(C2) NC1 patch cost 0 and NC2 contamination=0 and random-patch block-permutation false-accept ≤5% with AUROC 0.4-0.6 trajectory-grouped; else MEASUREMENT_INVALID.
(C3) B-RUNTIME-BYTE-IDENTITY pre-perturbation byte identity ≥0.99 on real nginx (oracle-free greedy decode) and mutation detected post-perturbation; else MEASUREMENT_INVALID.

Primary (require ALL to CONFIRM localized repair on TEST):
(C4) repair success ≥0.80 pooled AND ≥0.70 per family on TEST (Wilson CI reported, trajectory-grouped).
(C5) mean repair tokens <0.50× mean B-COLD tokens AND mean browser <0.40× B-COLD AND mean verification steps ≤2 on TEST (bootstrap CI of ratio < threshold).
(C6) contamination <0.10 on TEST (N≥24 unrelated, block-permutation).
(C7) verification AUROC ≥0.75 and precision ≥0.80 at TRAIN threshold on TEST (trajectory-grouped, ECE<=0.15 checked).
(C8) amortized cost at n_reuses=10 (repair+verification+10×retrieval) < B-COLD cost (both tokens and browser) on TEST means with trajectory-grouped CI.

CONFIRMED if C1–C8 all PASS. FALSIFIED-IN-SETTING if any C4–C8 fails while C1–C3 PASS (valid negative). MEASUREMENT_INVALID if C1–C3 fails or pooled TEST n<24 or vacuous substrate. MIXED if family-heterogeneous (≥1 family passes C4–C8 while another fails) — report per-family ceilings, no pooled confirmation. Effect sizes, CIs, per-family breakdown required. Stable identifiers preserved for AUDIT.

## 9. Validity threats

- **Target leakage:** post-state body/URL leaking into repair decision without verification. Mitigation: repair prompt sees only pre-mechanism + post-observation, threshold fit TRAIN-only, audit checks prompt logs contain no manifest label, trajectory-grouped evaluation.
- **Split integrity:** threshold fit on TEST would inflate AUROC. Mitigation: TRAIN/TEST split per §6, block-permutation audit recomputes split compliance; scores are real verify() confidences not instance_id-derived perfect separation.
- **Sampling integrity:** non-independent instances sharing global nginx state. Mitigation: per-instance cache purge + registry clone, seed determinism via hashlib, trajectory-grouped block bootstrap/permutation.
- **Representation integrity:** DOM hash collapsing distinct states or byte digest missing mutation or body/status conflation (vacuous). Mitigation: store raw decompressed bytes + full DOM + a11y tree + headers, not hash alone; hash derived; require non-vacuous full>body and full>status; semantic selector uses role/label/testId not literal URL/ID.
- **Policy confounding:** agent LLM may memorize perturbation pattern rather than observe. Mitigation: variant diversity (6 variants), unrelated mechanism contamination, retrieval block-permutation baseline, prompt contains no perturbation pattern, gpt-4o-mini salience bias controlled by calibrated UNKNOWN abstention ECE<=0.15 per prior #2.
- **Ceiling effects:** oracle hand-patch trivially 1 probe — does not prove autonomous repair cheap. Mitigation: autonomous repair cost measured separately vs oracle ceiling via real execution, trajectory-grouped.
- **Falsifier mis-specification:** single family failure should not falsify all families. Mitigation: per-family gating and MIXED outcome preserved.
- **Simulation replay risk:** reusing hardcoded costs. Mitigation: this design forbids hardcoded constants (prior COLD_TOKENS_BASE 2250, retrieval 320, verify 180, heuristic 1364 removed); audit verifies tokens from real openai API usage and browser counts from Playwright traces and trajectory-grouped CIs; any simulation fallback triggers MEASUREMENT_INVALID.
- **Substrate simulation drift:** synthetic gzip vs real nginx greedy decode. Mitigation: byte identity recomputed on real nginx fetches with oracle-free decompression; record nginx.conf and decompression code hash; require non-vacuous isolation.
- **Economics mismeasurement:** analytical token counting overstates savings (5.42% synthetic margin observed). Mitigation: end-to-end LLM+Playwright amortized cost including retrieval/verification/repair/staleness at 10 reuses vs cold, same model/tools/budget 15 steps per prior #1.
- **Shortcut inflation:** retrieval/RAG may exploit header/body leakage. Mitigation: longest-prefix and intent-constrained evaluation, plus 0-token verbatim baseline, plus BrowserGym verify() grounding.
- **Calibration failure:** LLM overweighting salient retrieved context vs calibrated uncertainty -> false accepts. Mitigation: UNKNOWN abstention with ECE<=0.15 check, verification threshold calibrated on TRAIN only.

## 10. Analysis plan

1. Verify C1–C3 substrate/controls on real gpt-4o-mini pipeline with trajectory-grouped checks and non-vacuous isolation; if fail, halt as MEASUREMENT_INVALID and report.
2. Compute per-instance success, real tokens (API usage), real browser steps (Playwright traces), real verification AUROC/precision (threshold from TRAIN), contamination via real verify() on TEST with block-permutation, and ECE.
3. Compute pooled and per-family aggregates with Wilson CIs for rates, instance-block bootstrap CIs for cost ratios on TEST.
4. Compute amortized cost: repair+verification+10×retrieval (real retrieval) vs cold on TEST with trajectory-grouped CI.
5. Verify B-VERBATIM 0% and B-RETRIEVAL block-permutation sanity, and non-vacuous full>body>status.
6. Apply C4–C8 decision rule on TEST split only with trajectory-grouped inference.
7. Report per-family and pooled with raw_evidence hashes, per-instance CSV, nginx/Flask/Playwright/LLM provenance, prompt logs for leakage and UNKNOWN calibration, and trajectory-grouped CIs.

## 11. Product consequences

- **Positive (C1–C8 PASS on real trajectory-grouped measurement):** C-DELTA-REPAIR advances HYPOTHESIS→EXPERIMENTAL (VALIDATED candidate) for single-resource perturbations on real nginx HIT-cache localhost with gpt-4o-mini 15-step economics. Justifies localized repair boundary (patch+verify) with 10× amortization, unblocks residual-novelty economics. No promotion to Product Core — localhost only, single-resource, single model; next expand to 2-3 resource radius and distributed Redis session store and production CDN, integrate SpiderKernel.invalidate() with freshness guard and UNKNOWN abstention per prior #2.
- **Negative (C4–C8 fails, C1–C3 PASS on real trajectory-grouped measurement):** Single-resource locality fails at smallest radius even with real LLM+browser+verify and trajectory-grouped CIs; product must budget repair ≈ cold cost and default to full re-exploration or RAG+fused fallback, favoring UNKNOWN/abstain when verification not discriminating. Prevents premature repair-layer promotion and contamination risk. Graph lane pivots to C-RESIDUAL-NOVELTY matched families or C-SEMANTIC-RESOLVE calibrated abstention per Director comparative reasoning (Frontier/Product assignments this cycle; next cycle semantic param). A valid negative is high information — it closes the cheapest repair hypothesis and changes graph/runtime/product allocation.

Both outcomes are first-class and change a decision. Neither is treated as infrastructure failure. MEASUREMENT_INVALID (C1-C3 fails or vacuous) is not a negative scientific result and requires substrate fix before retry.

## 12. Estimated cost and information gain

Low-Medium (but real): ~6 compute-hours, ~170k tokens single LLM gpt-4o-mini 15-step (48 instances, real nginx 1.2x + Flask HS256 + Playwright localhost, trajectory-grouped analysis). Very high information gain: first real trajectory-grouped measurement of C-DELTA-REPAIR (0/239 valid; prior 35761721514 BLOCKED missing API and 35741890679 MEASUREMENT_INVALID simulation that falsified C5/C8 as parameter artifacts). Either CONFIRMED or FALSIFIED-IN-SETTING on trajectory-grouped CIs materially changes claim state and next allocation for graph/runtime/product. Advances beyond saturated FRESHNESS tunnel (11 recent) per Director CONTINUE rationale; cross-lane unblocking highest per unit effort vs C-PARAM-INHERIT and C-SEMANTIC-RESOLVE which are assigned elsewhere this cycle. Directly gates C-PRODUCT-ECON amortized economics.

## 13. Consequences of both outcomes

Both positive and negative outcomes are first-class and change a decision. Positive proceeds to broader radius/distributed substrate and informs SpiderKernel repair design with trajectory-grouped economics; negative closes the cheapest repair hypothesis and redirects investment to residual-novelty matched families or semantic abstention with block-permutation baselines. Neither is treated as infrastructure failure. MEASUREMENT_INVALID is not a negative scientific result and requires substrate fix before retry. Vacuous full==body==status==1.0 also MEASUREMENT_INVALID.

## 14. Preregistration freeze

This prereg.md and spec.json are frozen via freeze.json before any outcome-bearing measurement. A changed analysis after seeing outcomes is exploratory; a new confirmatory claim requires a new preregistration and untouched evidence. This design does not run outcome-bearing measurements. All required controls for EXP-GRAPH-35761721514 BLOCKED are addressed (real LLM, real nginx HIT/SWR/SIE/304 re-measured, real Playwright/BrowserGym verify, real contamination, 48 instances+threshold holdout+trajectory-grouped CIs), plus agent priors #1-#4 guards (backtracking/verification, UNKNOWN ECE<=0.15, measurable basin reset, semantic addressing). EXECUTION must log model id gpt-4o-mini, temperature, max_tokens, provider, per-call tokens, 15-step traces, Playwright traces, nginx/Flask/verify provenance, decompression code hash, and block-permutation seeds for audit of leakage and vacuous isolation. No simulation fallback permitted — hardcoded costs (COLD_TOKENS_BASE 2250 etc.) remain forbidden. Stable metric/control identities are frozen for downstream transmission per research/EXPERIMENT_PACKET.md.

