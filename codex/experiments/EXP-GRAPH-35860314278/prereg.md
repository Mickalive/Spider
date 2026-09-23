# EXP-GRAPH-35860314278 preregistration

**Experiment ID:** EXP-GRAPH-35860314278
**Lane:** graph
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally
**Status:** DESIGN — not yet frozen (freeze via deterministic freeze.json before EXECUTE)
**Director mandate:** PIVOT, SUPERSEDE — target claim C-DELTA-REPAIR, cognitive_reset=false, parent_handoff EXP-GRAPH-35798169917 SUPERSEDE disposition. The inherited next_question (single-family WebArena-Verified v2 param-inherit pilot) is continuity evidence only and does not drive this design per AGENTS.md precedence and research/EXPERIMENT_PACKET.md §2. Strategic question is binding.

---

## 1. Question

After runtime's verified byte-preserving nginx HIT-cache substrate (EXP-RUNTIME-35611612543: 960/960 byte-identical across HIT/SWR/SIE/304 stages with oracle-free greedy decode), does a controlled single-resource local perturbation — single DOM attribute/text change, endpoint param/header change, or Cache-Control/ETag mutation — require only localized repair (bounded tokens/browser/verification cost, contamination < threshold) versus full cold re-exploration, with repair cost amortized over retrieval frequency?

Refined falsifiable form (Director strategic question restated with frozen thresholds): Is mean localized repair cost <50% of full re-exploration tokens and <40% of browser interactions, with verification AUROC ≥0.75 (precision ≥0.80), contamination <0.10 (no repair of unrelated resources), and amortized per-use cost (repair+verify+10×retrieval)/10 < cold cost at 10 reuses, when repairing a single-resource perturbation on the nginx HIT-cache localhost substrate measured with a real LLM agent (gpt-4o-mini same model/tools/budget 15 steps Playwright) and real verify() on actual DOM/response state, vs B-COLD and B-RAG baselines with trajectory-grouped CIs?

---

## 2. Motivation and inherited state

### 2.1 Director mandate and strategic context

The Global Research Director (cycle 35859819467) performed a PIVOT with comparative reasoning explicitly in request.json. Diagnosis: SPIDER is stalled at 271 canonical experiments with zero claims VALIDATED/PRODUCT_CORE; 60 recent experiments are synthetic harnesses re-testing tautologies (bijective cost formulas, hardcoded confidences, hash-derived DOM, truncated selectors) yielding repeated MEASUREMENT_INVALID. Only narrow substrate advances survive: byte-preserving nginx HIT-cache oracle-free greedy decode 960/960 across HIT/SWR/SIE/304 (EXP-RUNTIME-35611612543) and Bayesian Dirichlet-Multinomial K=12 first estimator to pass C1+C3 on synthetic SPA. All central product claims (C-PARAM-INHERIT 45 exps, C-FRESHNESS 43 exps, C-RESIDUAL-NOVELTY 8 exps, C-LLM-INHERIT 20 exps) are HYPOTHESIS/MEASUREMENT_INVALID with per-hit costs >1.0 vs TERX/Stagehand and 0/10 mixed-channel failures under correct-family gating.

Graph has 4 consecutive C-PARAM-INHERIT MEASUREMENT_INVALID pilots (zero unsubstituted templates never achieved, single-prefix fix not yet validated live) and C-PARAM-INHERIT has 45 total experiments in a deep basin; C-DELTA-REPAIR has only 5 experiments, all BLOCKED not falsified, and its substrate (nginx HIT-cache byte-identity) is already verified and does not require the still-missing distributed shared-store. Continuing the inherited single-family WebArena-Verified v2 pilot repeats the same live-pilot without fixing the substrate that caused 3 consecutive MEASUREMENT_INVALID (needs shared-store + BrowserGym AX>10); expected information gain ~0 vs high cost. A C-FRESHNESS file-census threshold sweep alone would re-test scalar orthogonality already falsified at FP=1.0.

Comparative reasoning (per mandate): vs CONTINUE single-family WebArena pilot (parent handoff) — repeats same pilot without substrate fix, requires distributed shared-store still missing, low marginal gain; vs C-FRESHNESS file-census sweep — re-tests scalar orthogonality already falsified at FP=1.0; vs C-DELTA-REPAIR localized repair — discriminating positive vs null (localized vs full re-exploration) with already-available nginx HIT substrate, trajectory-grouped CIs, and honest token/browser cost — highest marginal value for cumulative inheritance and architecture decision.

Agent priors used (separately labeled, not SPIDER evidence): (1) long-horizon compounding errors/context rot motivates independent verification before state update and explains inflated novelty-cost rho when cost is bijective; (2) caching/replay baselines are deceptively strong on deterministic SPAs (recall@k=1.0 when registry_size≤k; Stagehand selector+DOM-hash 80% speedup will beat semantic retrieval unless correct-family gating tested); (3) deterministic cost = 250+500*10*novelty guarantees rho~1.0 — flags all Product rho 0.97-0.995 as measurement-invalid until costs are branch-derived sums of kernel calls + browser steps; (4) freshness is multi-channel not scalar, TTL/ETag stale-while-revalidate plus verification probe dominates learned calibration — cautions against adaptive Jaccard sweep after FP=1.0; (5) path dependence/local optima repeating synthetic SPA family with heuristic chunking locks lanes in basin where null bias is estimator-intrinsic — orthogonal estimator switch is escape. These informed prioritization only.

### 2.2 Established (from Codex and accepted experiments) — preserved per parent_handoff carry_forward.established

- Kernel fixes for C-PARAM-INHERIT (single-prefix _common_prefix_and_suffix, field-path relevance filter url/body.*/headers.* only, Jaccard ≥0.75 constant-anchor, distinct slot naming per field-path, confidence 0.90) durably implemented in src/spider/kernel.py sha 3c61f9fc... with 7/7 kernel_checks true, 13/13 unit tests PASS — audit PASS confirms. This resolves the 42-attempt transient loss but is not the target of this experiment; we reuse kernel.resolve/_bind/verify for honest cost measurement.
- Positive controls PASS on synthetic same-A via real kernel registry/_bind/verify path: PC1 same-A literal hit via B-REPLAY hit_rate 1.0; PC2 multi-param same-A via distill_parameterized achieves EXECUTABLE 1.0 binding 1.0 — confirms induction works before generalization, but does not imply hold-out transfer to B (still unknown for C-PARAM-INHERIT).
- Adequacy gate now passes for pilot family concept (10 valid tasks families_valid 1 with zero_overlap_verified) — fixed from parent 7<10 — but this is for C-PARAM-INHERIT pilot, superseded by this C-DELTA-REPAIR design which targets >=30 localized perturbation instances instead.
- C-PARAM-INHERIT ceiling remains narrow synthetic EXPERIMENTAL only (EXP-PRODUCT-33528829801 10/10 single-param, EXP-PRODUCT-33741671686 21/21 harness-only multi-param) — not extended by synthetic pilots; no VALIDATED real-LLM claim and no Product Core promotion.
- Runtime C-MEAS-VALID narrowly survives on Flask+PyJWT HS256 localhost (full-vector discrimination 0.833-1.0) and on verified nginx HIT-cache substrate with byte-preserving decompression (oracle-free) — dependency for this experiment. Content-Length/ETag are body-correlated; only Cache-Control/Set-Cookie are independent.
- Prior C-DELTA-REPAIR experiment EXP-GRAPH-35741890679 was the first measurement of this claim (simulated costs, 36 instances) — not yet in Codex; this design upgrades to real LLM+Playwright+verify honest costs.

### 2.3 Rejected / bounded

- Synthetic census 242 tasks duplication 0.7934 as WebArena-Verified v2 evidence — rejected per prereg, does not satisfy 192/49 duplication 0.9479.
- Bijective cost proxy 250+500*10*novelty and hardcoded duplication mocks as honest economics — rejected per Director mandate; only honest tokens+browser+retrieval+verification measured via API usage counts and branch-derived sums.
- Previous parent's ephemeral kernel sha 04438d... vs HEAD 46929b3a literal-only — rejected as transient fabrication, now superseded by durable 3c61f9f....
- C-FRESHNESS orthogonality at delta=0.15 CONFIRMED on LOCAL but C1 TN=0.667 before, now distributed r=-0.038 TOST PASS — bounded to localhost correlation, not to repair locality.
- C-PRODUCT-ECON logistic extrapolation — definitively REJECTED.
- C-WEB-DYNAMICS TV/KDE only-translation-detectable — synthetic-only ceiling.

### 2.4 Unknown — carried forward, updated for C-DELTA-REPAIR

- Whether any local perturbation is repairable locally (0/5 BLOCKED, not falsified — this experiment is first honest measurement).
- Repair cost, contamination, verification boundary, and 10-reuse amortization — all unknown with honest costs.
- Whether runtime HIT-cache byte identity 960/960 holds under controlled mutations and with real LLM+Playwright load (assumed per dependency but re-verified here at C3).
- Whether verification AUROC ≥0.75 with real DOM/response state is achievable (prior synthetic claimed precision ≥0.80 but unvalidated with real verify()).
- Residual-novelty economics beyond doc survey, cross-site holdout, LLM-inheritance with strong baselines — still unknown, downstream of this repair measurement.
- For C-PARAM-INHERIT: does real-LLM param inherit achieve EXECUTABLE ≥0.75 binding ≥0.90 on B hold-out — remains unknown, not tested here (superseded).

### 2.5 Do NOT assume — preserved distinctions

- Do not assume kernel durability + synthetic same-A PC1/PC2 PASS implies generalization to unseen B — PC2 tests induction on A only, not hold-out transfer.
- Do not assume synthetic census 242/0.7934 approximates WebArena-Verified v2 192/49 0.9479 — requires real Docker hash verification.
- Do not assume pilot family add_to_cart with slots [qty,resource_id,sku,x_csrf_token] demonstrates independent multi-param transfer — url/csrf are deterministic functions of single sku.
- Do not assume MEASUREMENT_INVALID is falsification — infrastructure failure (OPENAI_API_KEY absent, Playwright not installed, synthetic census) is not negative evidence; per EXPERIMENT_PACKET s9.
- Do not assume bijective cost proxy or hardcoded mocks are valid economics — mandate requires honest branch-derived costs.
- Do not assume 10/10 single-param ceiling extends to real-LLM multi-param WebArena hold-out or Product Core — requires PASS audit and promotion authorization.
- Do not assume C-FRESHNESS correlation or distributed session-affinity fix implies delta-repair locality — orthogonal claims.
- Do not assume C-DELTA-REPAIR holds because freshness holds — this is the hypothesis under test.
- Do not assume single-resource success implies multi-resource or distributed repair success — bounded to one resource.
- Do not assume replay/RAG suffices for drift — must be measured vs repair.
- Do not assume 960/960 byte identity generalizes beyond localhost nginx — bounded to stated fixture.
- Do not assume parent handoff next_question determines this experiment — superseded by Director PIVOT per AGENTS.md precedence.

---

## 3. Hypothesis

**H1 (C-DELTA-REPAIR localized):** A single-resource local perturbation is repairable by a localized patch (re-target selector, rebind param slot, update header expectation, refresh cache key = one registry mutation + 1–2 Playwright probes) without full-task re-exploration, with bounded cost and low contamination.

Operational predictions:

1. Localized repair succeeds on ≥80% of perturbation instances (≥70% per family) where success = kernel.verify()=true AND independent oracle functional correctness (ground-truth selector/param/header check).
2. Mean repair LLM tokens <0.50 × mean B-COLD tokens; mean browser interactions <0.40 × B-COLD; mean verification steps ≤2 (honest branch-derived sums, not bijective proxy).
3. Verification discriminates correct vs incorrect patch (AUROC ≥0.75, precision ≥0.80 at frozen operating threshold fit on TRAIN perturbations only).
4. Contamination of unrelated mechanisms (N≥20 distinct intents) <0.10.
5. Amortized per-use cost at 10 reuses (repair+verify+10×retrieval)/10 < B-COLD cost for both tokens and browser steps, with trajectory-grouped CIs.

**H0 (null):** Repair cost ≥ full cost or contamination ≥0.10 or success <0.80 or verification near chance, so local patch is not separated from full re-exploration. Failure may be family-specific (e.g., DOM repairable but ENDPOINT not) — then ceiling is per-family, not global.

---

## 4. State, action, and target representation

### 4.1 State representation (frozen)

Pre-state S_current: (Mechanism registry snapshot with parameter_slots/confidence, page DOM snapshot + accessibility tree subset, HTTP response headers (ETag, Cache-Control, Content-Encoding), URL+query, cache state HIT/SWR/SIE/304). Raw observation preserved: DOM string, headers dict, decompressed body bytes + SHA256, cache status header.

Post-state S_next: (updated DOM/response after perturbation or after repair, verification postconditions match via _matches). All raw observables preserved or losses documented per master prompt §17.

### 4.2 Action representation

- Repair action: patch := {selector rewrite | param slot rebind | header expectation update | cache key refresh}, executed as single registry mutation (upsert patched Mechanism) + 1–2 Playwright probes (goto, evaluate selector existence, fetch with updated param/header).
- Full re-exploration action: real LLM agent trajectory from scratch (observe → plan → act → verify) with same model/tools/budget, no registry reuse, same SpiderKernel but empty registry.

### 4.3 Target

Primary: binary repair success (kernel.verify true AND oracle functional correctness) plus continuous cost metrics. Secondary: verification AUROC/precision, contamination rate, amortized cost ratio.

No target leakage: verification threshold (confidence cutoff for REPAIRABLE vs EXPLORE) calibrated on TRAIN perturbation split only (e.g., families D+E train, C test, or 50/50 instance split); post-state never leaks into pre-state features for threshold fitting. Preprocessing (threshold) fit on TRAIN only per validity gate.

---

## 5. Sampling plan

- **Unit of analysis:** single perturbation instance (one resource, one mutation). Trajectory-grouped inference: resampling unit = perturbation instance (not individual browser step or token).
- **Perturbation families (3 × 2 variants × 6 seeds = 36 instances, minimum 30 if LLM budget constrained):**
  - F-DOM: (D1) single attribute change (#submit-123→#submit-124, data-testid rename), (D2) single text node change (button label "Submit"→"Send").
  - F-ENDPOINT: (E1) query param rename (?id=→?item=), (E2) header name change (X-Request-Id → X-Req-Id).
  - F-CACHE: (C1) Cache-Control max-age 60→3600, (C2) ETag value mutation (SHA change reflecting body change).
- **Unrelated mechanism set:** N≥20 mechanisms from distinct intents/endpoints (e.g., add_to_cart, search, checkout, profile) for contamination measurement; registry cloned before perturbation.
- **Seeds:** deterministic via hashlib.sha256(f"{experiment_id}:{family}:{variant}:{seed}:v1"), never Python hash(). LLM seed 42 via OpenAI seed param.
- **Budget:** gpt-4o-mini-2024-07-18, temp 0.0, seed 42, max 15 steps per task, 4096 tokens per step, same for B-COLD and repair.
- **Substrate:** localhost nginx reverse-proxy + Flask backend (PyJWT HS256 if auth needed), identical to EXP-RUNTIME-35611612543 fixture; record commit hashes for nginx.conf, Flask testbed_server.py, decompression code.

---

## 6. Metrics and baselines

### 6.1 Primary metrics (stable identities for AUDIT/DIRECTOR)

- `repair_success_rate` (pooled and per-family): k/n with Wilson 95% CI and trajectory-grouped bootstrap CI.
- `repair_tokens_mean`, `cold_tokens_mean`, `token_ratio` = repair/cold with bootstrap 95% CI; same for `repair_browser_mean`, `cold_browser_mean`, `browser_ratio`.
- `verification_steps_mean` (count verify()+registry lookup+HIT fetch).
- `contamination_rate` = invalidated or false-accept among N_unrelated with Wilson CI.
- `verify_auroc`, `verify_precision_at_threshold`, `verify_recall`, `verify_ece`, confusion matrix.
- `amortized_token_ratio_10` = (repair_tokens+verify_tokens+10*retrieval_tokens)/(10*cold_tokens) with bootstrap CI; same for browser. Also report `retrieval_tokens_mean`, `retrieval_browser_mean`.
- `byte_identity_pre` = fraction SHA256(hit)==SHA256(swr)==SHA256(sie)==SHA256(304) pre-perturbation; `byte_identity_post_unperturbed` for unperturbed resources; `mutated_differs` for perturbed resource.

### 6.2 Baselines (frozen identities)

- **B-COLD** (Full cold re-exploration): same LLM/tools/budget, empty registry — denominator for cost ratios.
- **B-RAG** (Semantic retrieval, nearest trajectory replay, no patch): strong retrieval baseline.
- **B-REPLAY** (Verbatim replay, 0-token): pre-perturbation mechanism unchanged — must fail if perturbation is breaking (validity).
- **B-ORACLE** (Oracle hand-patch, 1 mutation +1 probe): ceiling for achievable locality.
- **B-BYTE-IDENTITY** (Runtime substrate invariant 960/960): validity baseline, not a comparator for repair success.

### 6.3 Controls

- **Positive (PC-LOCALIZED-REPAIR-SUCCEEDS):** PC1 unperturbed success 1.0 byte identity 1.0; PC2 known-break D1/E1 with oracle patch ≥90% success cost ratio <0.50. Both via real LLM+Playwright path.
- **Null (NC-ZERO-AND-DISTANT):** NC1 zero perturbation cost 0 contamination 0 byte identity 1.0; NC2 distant unrelated perturbation (mutate B while target A) no-op contamination 0. Random-patch permutation AUROC 0.45-0.55.

---

## 7. Measurement validity

1. Substrate provenance — nginx HIT/SWR/SIE/304 with oracle-free decompression, verified pre-perturbation byte identity ≥0.99 (960/960 target). Record all hashes/versions. If unavailable or identity <0.99, MEASUREMENT_INVALID.
2. Perturbation isolation — exactly one resource per instance, manifest with file/line/old/new, blast radius=1, exclude non-breaking instances (B-REPLAY >0.10).
3. Registry isolation — clone before perturbation, repair on clone, contamination on N≥20 unrelated mechanisms, no oracle leakage beyond post-state observation.
4. Honest cost — branch-derived sums of kernel calls + browser steps (api usage counts), not bijective proxy; per AGENTS.md and Director priors, report tokens+browser+retrieval+verification separately; trajectory as grouping unit.
5. Verification validity — kernel.verify on actual DOM/response, false accepts via independent oracle script, threshold fit on TRAIN only, report AUROC/precision/ECE.
6. Adequacy — ≥30 instances (target 36), per-family ≥10, N_unrelated ≥20; else exploratory.
7. Determinism — hashlib.sha256 seeds, OpenAI seed 42, record commits/versions, localhost only.
8. Byte-identity recomputation — per-instance SHA256 for all cache stages pre/post; perturbed must differ, unperturbed must remain identical.

---

## 8. Decision rule (frozen)

All thresholds applied on frozen pre-registered data only, with trajectory-grouped bootstrap (5000 resamples, seed 42) and Wilson CIs.

**Validity gates (must ALL pass for any CONFIRMED/FALSIFIED; else MEASUREMENT_INVALID):**
- C1: PC1 success==1.0 and PC2 success ≥0.90 (Wilson lower ≥0.70) with cost ratio <0.50.
- C2: NC1 cost==0 and NC2 contamination==0 and random-patch false-accept ≤0.05 with AUROC 0.45-0.55.
- C3: B-BYTE-IDENTITY pre-perturbation byte identity ≥0.99 and post-perturbation perturbed differs while unperturbed remains ≥0.99.

**Primary gates (require ALL to CONFIRM):**
- C4: repair success ≥0.80 pooled (Wilson lower ≥0.65) AND ≥0.70 per family (Wilson lower ≥0.50).
- C5: mean repair tokens <0.50× B-COLD (bootstrap upper <0.50) AND mean browser <0.40× B-COLD (bootstrap upper <0.40) AND mean verification steps ≤2.0.
- C6: contamination <0.10 (Wilson upper <0.15).
- C7: verify AUROC ≥0.75 (bootstrap lower ≥0.65) AND precision ≥0.80 (bootstrap lower ≥0.70).
- C8: amortized per-use cost at 10 reuses < B-COLD for both tokens and browser (bootstrap upper <1.0).

**Outcomes:**
- **CONFIRMED** if C1-C8 all PASS.
- **FALSIFIED-IN-SETTING** if any C4-C8 fails while C1-C3 PASS (valid negative).
- **MEASUREMENT_INVALID** if any C1-C3 fails OR total n<24 OR any family n<10 that would otherwise confirm.
- **MIXED** if ≥1 family passes C4-C8 while another fails — report per-family ceilings, do not pool.

Effect sizes, 95% CIs, and per-family breakdown required in result.json. All p-values Bonferroni-corrected where multiple families tested.

---

## 9. Validity threats and mitigations

- **Bijective cost tautology (rho~1.0):** mitigated by honest branch-derived costs; report API usage directly; never use 250+500*10*novelty formula; trajectory-grouped CIs.
- **Replay baseline deceptively strong on deterministic SPA (recall@k=1.0):** mitigated by requiring B-REPLAY to fail (>0.10 success flags non-breaking perturbation) and by testing correct-family-required binding not just any recall.
- **Leakage via oracle label:** mitigated by repair agent seeing only post-state observation, not perturbation manifest; oracle script only used to label correctness post-hoc, never in prompt.
- **Threshold overfitting:** mitigated by TRAIN-only calibration, report test AUROC on held-out family/split.
- **Ceiling effect (all bodies distinct):** mitigated by ensuring perturbations are minimal (single attribute) and unperturbed resources share bodies; byte identity pre-check ensures discriminability not ceiling.
- **Infrastructure failure misclassified as falsification:** per EXPERIMENT_PACKET s9, OPENAI_API_KEY absent / Playwright not installed / rate limiting → MEASUREMENT_INVALID with failure.json, not FALSIFIES.
- **Family heterogeneity masked by pooling:** mitigated by requiring per-family ≥0.70 and reporting MIXED if heterogeneous.

---

## 10. Product consequences

**If CONFIRMED:** C-DELTA-REPAIR advances HYPOTHESIS → EXPERIMENTAL (VALIDATED bounded to single-resource localhost nginx only). Justifies localized repair architecture (registry patch + verify loop, amortized advantage after 10 reuses). Next: expand radius (2-3 resources, cross-page), distributed Redis, integrate into SpiderKernel with freshness guard. No Product Core promotion — requires cross-site and multi-model replication.

**If FALSIFIED-IN-SETTING:** Single-resource locality fails even minimally; cheapest repair not cheap. Product defaults to full re-exploration or RAG+fused for drift, budgeting repair as cold cost. Do not ship repair layer. Graph pivots to C-RESIDUAL-NOVELTY matched families or C-SEMANTIC-RESOLVE abstention, which do not assume cheap patches. Runtime substrate remains valid for measurement but not for repair. Valid negative prevents premature promotion — high information.

**If MEASUREMENT_INVALID:** No claim update; substrate or LLM/Playwright dependency blocked. Smallest next action is provision OPENAI_API_KEY + Playwright + re-pull nginx fixture and re-run identical frozen design without re-tuning. Do not pivot to orthogonal mechanism until this honest-cost measurement is valid.

---

## 11. Estimated cost and information gain

**Estimated cost:** Low-Medium ~5.5h wall-time, ~0.8-1.2M tokens (36×15 steps×~800 tokens for B-COLD + same for repair + RAG/ORACLE), all localhost. Setup 0.5h (nginx fixture + byte identity verify), generation 0.5h, B-COLD 1.5h, repair+verify 1.5h, baselines 0.5h, analysis 0.5h. No external sites.

**Expected information gain:** Very high — first honest-cost C-DELTA-REPAIR with real LLM+verify (0/271 canonical had this; prior 35741890679 was simulated). Directly tests "pay novelty not whole task" with repair boundaries, contamination, and 10-reuse amortization vs strong replay/RAG baselines, with trajectory-grouped CIs ensuring non-tautological inference. Either outcome materially changes claim state and graph/runtime/product allocation, per Director PIVOT rationale, and escapes the 45-experiment C-PARAM-INHERIT basin and 30-streak FRESHNESS saturation.

---

## 12. Preregistration freeze

DESIGN has not inspected outcome measurements. freeze.json will hash request.json + spec.json + this prereg.md before EXECUTE. EXECUTE must not mutate frozen inputs; AUDIT will recompute trajectory-grouped metrics using same metric/control identities. Deviations after freeze are exploratory and require new preregistration.

