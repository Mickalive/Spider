# EXP-GRAPH-35752541832 preregistration

**Experiment ID:** EXP-GRAPH-35752541832
**Lane:** graph
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally
**Status:** DESIGN — not yet frozen (freeze via deterministic freeze.json before EXECUTE)
**Director mandate:** PIVOT, SUPERSEDE — target claim C-DELTA-REPAIR, cognitive_reset=true, parent_handoff EXP-GRAPH-35741890679 (MEASUREMENT_INVALID) disposition USE. The inherited next_question is continuity evidence only and does not drive this design per AGENTS.md precedence and research/EXPERIMENT_PACKET.md §2. Request request_hash 4de9da9cddb21b8c9ee0958a41d72cce5eac0e90c91a5a4b98991aeb1a75b5cd.

---

## 1. Question

After runtime's verified byte-preserving nginx HIT-cache substrate (oracle-free decompression 960/960 byte-identical across HIT/SWR/SIE/304 stages), does a controlled single-resource local perturbation — single DOM attribute/text change, endpoint param/header change, or Cache-Control/ETag mutation — require only localized repair (bounded tokens/browser/verification cost, contamination < threshold) versus full cold re-exploration, with repair cost amortized over retrieval frequency, **when measured with a real LLM agent, real Playwright execution, and real verify() on actual DOM/response state**?

Refined falsifiable form: Is mean localized repair cost <50% of full re-exploration tokens and <40% of browser interactions, with contamination <10%, verification AUROC ≥0.75 (precision ≥0.80), and amortized repair cheaper than full at n_reuses=10, when repairing a single-resource perturbation on the real nginx HIT-cache localhost substrate?

This is the binding Director question. The parent handoff asked the identical question but answered it only as a deterministic simulation (audit REVISE: no real LLM, Playwright, verify, or nginx). This design preserves the question and fixes the measurement to be real.

## 2. Motivation and inherited state

### 2.1 Director mandate and strategic context

The Global Research Director (cycle 35751960273, request 675bb0be8936334007f51057) performed a PIVOT with cognitive_reset=true across 230+ experiments. Diagnosis: Graph is trapped (9/10 FRESHNESS, 14 recent) on marginal orthogonality r-variants after confirmation on mock (r=0.0022 CI upper 0.0916) and single-node production-like (r=0.041) and distributed C1 TN=0.667 failure is session-store non-replication, not orthogonality, so further mock r-variants have low information gain. Runtime just delivered first validated HIT/SWR/SIE/304 byte-preserving substrate (oracle-free decompression 960/960 byte-identical) enabling the next gate C-DELTA-REPAIR: localized repair vs cold. This directly tests SPIDER's core compression promise (later-agent pays residual novelty) with end-to-end cost + verification + contamination, untested after 1 total delta-repair experiment (MEASUREMENT_INVALID).

Comparative reasoning (per mandate): Continuing FRESHNESS (e.g., r at delta=0.10 or n>=800 distributed without session fix) repeats confounded measurement and yields <0.05 effect vs verified substrate-enabled repair test which can falsify/support local repairability. Alternatives C-PARAM-INHERIT starved and C-RESIDUAL-NOVELTY synthetic mocks are better served by product real-LLM test and by first demonstrating repair boundedness; semantic resolution is higher leverage for frontier with calibration focus. Delta-repair has highest cross-lane unblocking per unit effort.

Dependencies per mandate:
- runtime:EXP-RUNTIME-35611612543 byte-preserving nginx HIT/SWR/SIE/304 substrate
- runtime:EXP-RUNTIME-35741906498 header/body isolation for verification signal

Agent priors used (separately labeled, not SPIDER evidence): path dependence/salience bias compounding, exact replay vs semantic retrieval collapse under shift, looping/error cascades detectable from telemetry and repairable by rollback, incremental computation/local DOM mutations. These informed prioritization only.

Portfolio assessment: 38/230 MEASUREMENT_INVALID shows substrate validity remains bottleneck; depth on localhost mocks is exhausted; breadth on real LLM+Playwright+verification is next leverage point. The current design is the smallest rigorous high-information experiment that can change C-DELTA-REPAIR state and product repair architecture.

### 2.2 Established (from Codex and accepted experiments + parent handoff)

From Codex/registry:
- C-MEAS-VALID header-only discrimination on localhost, C-FRESHNESS orthogonality r~0.04 on mock/single-node, Bayesian null control on synthetic SPA — narrow validated core.
- C-PARAM-INHERIT narrow single-char POC survives in harness but kernel integration falsified for noisy observations — not blocking for delta-repair.
- Runtime C-MEAS-VALID narrowly survives on Flask 3.1.3 + PyJWT 2.13.0 HS256 localhost (full-vector discrimination 1.0, null FP 0.0%) and on verified nginx HIT-cache substrate with byte-preserving decompression (oracle-free) — dependency for this experiment.

From parent EXP-GRAPH-35741890679 (MEASUREMENT_INVALID, audit REVISE) — bounded to simulation only, not rejected generally:
- Deterministic simulation with 36 instances (3 families x2 variants x6 seeds, TRAIN 18 TEST 18 stratified) +24 unrelated mechanisms +960 synthetic byte bodies achieved: pooled repair success 0.833 CI [0.681,0.921] all and 0.944 CI [0.742,0.990] TEST (F-DOM 0.833/1.0, F-ENDPOINT 0.75/0.833, F-CACHE 0.917/1.0), cold cost 2244 tokens 8.7 browser at 94.4% success, at simulated-cost ratios token 0.613 CI [0.569,0.661] and browser 0.431 CI [0.396,0.469] failing <0.50/<0.40, verification AUROC 1.0 prec/rec 1.0 by construction (threshold 0.6 TRAIN-fit, random AUROC 0.667), contamination mean 0.0046 max 0.083 <0.10 (hardcoded to 2 events), amortized 4744 tokens vs cold 2226 (2.1x) failing, verbatim replay 0.028 (1/36) proving breaking perturbations, retrieval RAG 0.333 (repair +50pp), oracle hand-patch 1.0 at 120 tokens/1 browser (5.3% cold), synthetic byte identity 960/960=1.0 via gzip.decompress.
- Synthetic byte identity via oracle-free gzip.decompress yields 960/960 identical SHA across HIT/SWR/SIE/304 on synthetic strings, but not validated on real nginx with production Content-Encoding/chunked/Vary (audit SUBSTRATE_SIMULATION_NOT_REAL_NGINX).
- Baseline ordering in simulation: verbatim near 0 confirms breaking; retrieval partially succeeds (0.333) but repair heuristic exceeds it; oracle ceiling far cheaper (120 tokens) than heuristic (1430), leaving 12x headroom unexplained.

### 2.3 Rejected / bounded

- Cost-bounded localized repair (<50% tokens, <40% browser, amortized < cold at 10 reuses) FOR THE DETERMINISTIC SIMULATION parameterization (hardcoded COLD_TOKENS_BASE 2250, retrieval 320, verify 180, heuristic repair 1364) — audit: amortization mathematical consequence, simulation not measurement. This bounded simulation falsification does NOT reject C-DELTA-REPAIR on real LLM/Playwright/nginx substrate (audit claim_ceiling explicitly limits to simulation only).
- C-PRODUCT-ECON logistic extrapolation — definitively REJECTED (6-model vacuous step, R2=1.0 = null).
- No broader rejection: C-DELTA-REPAIR on real substrate, multi-resource (2-3) radius, cross-page drift, distributed Redis session store, header-only vs body-changing perturbations, or alternative repair strategies remain untested and not rejected.
- C-FRESHNESS reaching VALIDATED/PRODUCT_CORE — not warranted; bounded to LOCAL + distributed correlation, C1 gated.

### 2.4 Unknown (carry_forward unknown from parent, preserved)

- Whether a real LLM agent achieves repair token cost <50% cold and browser <40% cold on F-DOM/E1/F-CACHE single-resource perturbations with real token billing and Playwright execution.
- Whether real verification on actual DOM/response discriminates correct vs incorrect patch with AUROC>=0.75 precision>=0.80 without perfect-separation artifact.
- Whether contamination remains <10% and false_accept <5% when measured on real registry/mechanism state vs hardcoded events.
- Whether amortized cost at 10 reuses (< cold) holds with real retrieval costs and real verification costs vs hardcoded 320/180.
- Whether nginx HIT/SWR/SIE/304 byte identity holds on real nginx 1.2x with production gzip/chunked beyond synthetic 960 bodies.
- Whether per-family cost heterogeneity exists at adequate TEST n (current TEST n=6 per family exploratory, Wilson half-width ~0.22) and whether multi-resource radius, cross-page, distributed Redis, or production CDN change repair economics.
- Whether residual-novelty amortization and verification generalize to production DOM where controller/oracle disagree on functional correctness.

### 2.5 Do NOT assume (carry_forward do_not_assume, preserved and binding)

- That frozen C1-C3 PASS (PC1 1.0, PC2 0.917, byte identity 1.0, NC controls) constitutes measurement validity — all inputs were hardcoded/synthetic, so PASS is artifactual not probative (audit SIMULATION_NOT_MEASUREMENT, SUBSTRATE_SIMULATION_NOT_REAL_NGINX).
- That token ratio 0.613 and browser ratio 0.431 or amortized 2.1x cold reflect real LLM economics — they are simulation parameter ratios, real costs may be substantially lower/higher; do not budget product repair at 61% cold based on simulation.
- That verification AUROC=1.0/precision=1.0 indicates real verification discriminates — scores were deterministically generated with perfect separation by instance_id.
- That contamination mean 0.0046 proves low contamination in real registry — values were hardcoded to 2 events.
- That C5/C8 failure falsifies C-DELTA-REPAIR generally — it falsifies only the cheapest single-resource simulation parameterization; real LLM with real observation may achieve thresholds.
- That success >=80% pooled/ >=70% per-family in simulation implies functional repair transfers to real DOM/a11y tree — simulated DOM is selector strings not accessibility tree.
- That C-DELTA-REPAIR holds because C-FRESHNESS orthogonality correlation holds (r~0.002-0.046) — orthogonal claims per prereg do_not_assume.
- That synthetic 960/960 byte identity validates runtime HIT-cache substrate for C-DELTA-REPAIR — synthetic gzip on strings vs production nginx/CDN are distinct.
- That zero or distant perturbation null controls (cost0 cont0) validate real repair pipeline calibration — they are null by construction in simulation.
- That 36 instances with TEST n=6 per family is adequately powered for per-family cost CIs — it is exploratory; this design raises to 48 total (TEST n=8 per family minimum) and notes the upgrade path to 72.

## 3. Hypothesis

C-DELTA-REPAIR hypothesis (H1, real-substrate version): A single-resource local perturbation is repairable by a localized patch (re-target selector, rebind param slot, update header expectation, refresh cache key) without full-task re-exploration, with bounded cost and low contamination, when measured with a real LLM, real Playwright, and real verify() on actual nginx+Flask state.

Operational predictions on held-out TEST:
1. Localized repair succeeds on ≥80% of perturbation instances (≥70% per family).
2. Mean repair tokens <0.50 × mean full cold re-exploration tokens; mean browser interactions <0.40 × full; mean verification steps ≤2.
3. Verification discriminates correct vs incorrect patch (AUROC ≥0.75, precision ≥0.80 at operating threshold calibrated on TRAIN).
4. Contamination of unrelated mechanisms <0.10.
5. Amortized cost (repair + verification + 10×retrieval_cost) < full cold cost at n_reuses=10.

Byte-preserving HIT-cache substrate guarantees cache correctness is orthogonal: decompressed body SHA256 identity across HIT/SWR/SIE/304 is ≥0.99 pre-perturbation, so post-perturbation divergence is attributable to the controlled local change.

Null H0: repair cost ≥ full cost or contamination ≥0.10 or success <0.80 or verification near chance, so local patch is not separated from full re-exploration.

## 4. State, action, and target representation

### 4.1 State representation (frozen for this experiment)

Pre-state S_current: (Mechanism registry snapshot, page DOM snapshot + accessibility tree subset via Playwright, HTTP response headers (ETag, Cache-Control, Content-Encoding), URL+query, cache state HIT/SWR/SIE/304). Raw observables preserved: full DOM, a11y tree, decompressed body bytes, headers, cache status header. No hash-only surrogate.

Post-state S_next: (updated DOM/response after perturbation or after repair, verification postconditions match on actual state).

### 4.2 Action representation

- Repair action: patch := {selector rewrite | param slot rebind | header expectation update | cache key refresh}, executed as single registry mutation + 1–2 Playwright probes (goto, evaluate selector existence, fetch) with real LLM generation.
- Full re-exploration action: real LLM agent trajectory from scratch (observe → plan → act → verify) with same model/tools/budget, no registry reuse, via Playwright.

### 4.3 Target

Binary repair success (verify()=true on actual state AND independent oracle ground-truth functional correctness) plus continuous cost metrics. No target leakage: verification threshold calibrated on TRAIN perturbation split only; post-state never leaks into pre-state features for threshold fitting; perturbation manifest never in repair prompt.

## 5. Sampling plan

- **Unit of analysis:** single perturbation instance (one resource, one mutation) on real nginx+Flask.
- **Perturbation families (3 × 2 variants × 8 seeds = 48 instances):**
  - F-DOM: (D1) single attribute change (#submit-123→#submit-124, data-testid rename), (D2) single text node change (button label "Submit"→"Send") — applied to real Flask templates, observed via Playwright a11y tree.
  - F-ENDPOINT: (E1) query param rename (?id=→?item=), (E2) header name change (X-Request-Id → X-Req-Id) — applied to real Flask route + nginx config.
  - F-CACHE: (C1) Cache-Control max-age 60→3600, (C2) ETag value mutation (SHA change reflecting body change) — applied to real response headers.
- **Unrelated mechanism set:** N≥24 mechanisms from distinct intents/endpoints for contamination measurement (real registry).
- **Pre-perturbation mechanisms:** distilled from successful pre-perturbation observations (confidence 0.5 literal, promoted to ≥0.8 for validated), via real Playwright runs.
- **Seeds:** deterministic per instance (hashlib.sha256 derivation, never Python hash()); record seed manifest.
- **Exclusions:** nginx config reload failure, 5xx unrelated to perturbation, Playwright timeout >10s — logged and retried once; exclude only if persistent infrastructure failure, then count toward n and require n≥48 else MEASUREMENT_INVALID (not as repair failure).
- **Substrate:** nginx 1.2x reverse-proxy + Flask 3.1.3 backend + PyJWT HS256 + SQLite, localhost, Content-Encoding gzip where applicable, oracle-free decompression path (gzip.decompress without oracle lookup).
- **Upgrade path:** if compute allows, expand to 72 instances (3×2×12 seeds) to achieve per-family TEST n=12 for powered per-family CIs; 48 is minimum.

## 6. Holdout and contamination control

- **Holdout by perturbation instance:** threshold calibration (verification operating point) fit on TRAIN half (24), evaluated on held-out TEST half (24). Family-stratified split (TRAIN seeds 0-3, TEST seeds 4-7 per variant). If expanded to 72, TRAIN 36 TEST 36.
- **Registry isolation:** clone registry before each repair; measure contamination as fraction of uninvolved mechanisms where post-repair verify status flips or false-accept introduced, using frozen pre-perturbation evaluation suite via real verify(). No shared mutable state across instances beyond deterministic seeds.
- **Perturbation manifest holdout:** repair agent never sees manifest old→new mapping; only sees pre-perturbation mechanism + post-perturbation observation (real DOM snapshot + response) + verify() outcome. Audit will check prompt logs for leakage.

## 7. Baselines, controls, and metrics

### 7.1 Baselines (strong, hit-capable, real execution)

- B-COLD-FULL-REEXPLORATION — full cost reference (real LLM+Playwright).
- B-VERBATIM-REPLAY — 0-token replay fails post-perturbation (real Playwright, proves breaking).
- B-RETRIEVAL-RAG — semantic trajectory retrieval without patch (real retrieval + Playwright replay).
- B-ORACLE-HAND-PATCH — cost ceiling (1 probe + 1 verify, real execution).
- B-RUNTIME-BYTE-IDENTITY — ≥0.99 pre-perturbation identity on real nginx (not synthetic).

### 7.2 Positive control

PC-LOCALIZED-REPAIR-SUCCEEDS: PC1 unperturbed execute+verify 100% (real); PC2 known-break single-attribute with oracle patch ≥90% success and cost ratio <0.5 vs B-COLD on real pipeline.

### 7.3 Null control

NC-ZERO-AND-DISTANT-PERTURBATION: NC1 zero perturbation cost=0 contamination=0 (real); NC2 distant perturbation no-op (real). Random-patch permutation null verifies AUROC ~0.5 on real verify() scores.

### 7.4 Primary and secondary metrics (stable identities for AUDIT — preserves frozen IDs from parent)

- M-repair_success_rate (pooled, per-family; Wilson 95% CI)
- M-repair_tokens_mean, M-repair_tokens_ratio_vs_cold (bootstrap 95% CI)
- M-browser_interactions_mean, M-browser_ratio_vs_cold (bootstrap 95% CI)
- M-verification_steps_mean, M-verification_auroc, M-verification_precision, M-verification_recall
- M-contamination_rate (unrelated mechanisms), M-false_accept_rate
- M-amortized_cost_tokens_10, M-amortized_cost_browser_10, M-cold_cost_tokens, M-cold_cost_browser
- M-byte_identity_hit_swr_sie_304_sha_match_rate (pre and post, real)
- M-retrieval_cost_tokens (real, not hardcoded), M-replay_success_rate, M-retrieval_success_rate
- M-wall_time_seconds

All metrics recorded per instance in raw_evidence/experiment_data.json with SHA256; derived aggregates in result.json. Token counts are real API prompt+completion tokens.

### 7.5 Uncertainty and adequacy

Resampling unit = perturbation instance (independent by construction via registry clone + cache purge). 95% Wilson CIs for rates, bootstrap (by instance, 2000 resamples) for cost ratios. Adequacy: 48 instances gives pooled TEST n=24 (±0.14 Wilson half-width at p=0.8); per-family TEST n=8 gives ±0.26 (flagged exploratory). If TEST n<24 pooled, MEASUREMENT_INVALID. Per-family gates are exploratory at n=8 but pre-registered as required ≥0.70; upgrade to 72 (per-family TEST n=12, ±0.22) is recommended and pre-authorized without new prereg if budget allows, with decision_rule unchanged.

## 8. Decision rule (frozen, verbatim in spec.json)

All thresholds applied on frozen pre-registered TEST data only. Gates:

(C1) PC1 success=1.0 and PC2 repair success ≥0.90 on real pipeline; else MEASUREMENT_INVALID.
(C2) NC1 patch cost 0 and NC2 contamination=0 and random-patch false-accept ≤5% with AUROC 0.4-0.6; else MEASUREMENT_INVALID.
(C3) B-RUNTIME-BYTE-IDENTITY pre-perturbation byte identity ≥0.99 on real nginx; else MEASUREMENT_INVALID.

Primary (require ALL to CONFIRM localized repair on TEST):
(C4) repair success ≥0.80 pooled AND ≥0.70 per family on TEST.
(C5) mean repair tokens <0.50× mean B-COLD tokens AND mean browser <0.40× B-COLD AND mean verification steps ≤2 on TEST.
(C6) contamination <0.10 on TEST.
(C7) verification AUROC ≥0.75 and precision ≥0.80 at operating threshold (threshold from TRAIN) on TEST.
(C8) amortized cost at n_reuses=10 (repair+verification+10×retrieval) < B-COLD cost (both tokens and browser) on TEST means.

CONFIRMED if C1–C8 all PASS. FALSIFIED-IN-SETTING if any of C4–C8 fails while C1–C3 PASS (valid negative). MEASUREMENT_INVALID if C1–C3 fails or pooled TEST n<24 or byte identity fails. MIXED if family-heterogeneous (≥1 family passes C4–C8 while another fails) — report per-family ceilings and do not claim pooled confirmation. Effect sizes, CIs, per-family breakdown required.

## 9. Validity threats

- **Target leakage:** post-state body/URL leaking into repair decision without verification. Mitigation: repair prompt sees only pre-mechanism + post-observation, threshold fit TRAIN-only, audit checks prompt logs contain no manifest label.
- **Split integrity:** verification threshold fit on TEST would inflate AUROC. Mitigation: TRAIN/TEST split per §6, audit recomputes split compliance; scores are real verify() confidences not instance_id-derived.
- **Sampling integrity:** non-independent instances sharing global nginx state. Mitigation: per-instance cache purge (proxy_cache purge) + registry clone, seed determinism via hashlib.
- **Representation integrity:** DOM hash collapsing distinct states or byte digest missing mutation. Mitigation: store raw decompressed bytes + full DOM snapshot + a11y tree + headers, not hash alone; hash is derived.
- **Policy confounding:** agent LLM may memorize perturbation pattern rather than observe. Mitigation: variant diversity (6 variants), unrelated mechanism contamination, retrieval baseline comparison, prompt contains no perturbation pattern description.
- **Ceiling effects:** oracle hand-patch trivially 1 probe — does not prove autonomous repair is cheap. Mitigation: autonomous repair cost measured separately vs oracle ceiling via real execution, not conflated.
- **Falsifier mis-specification:** single family failure should not falsify all families. Mitigation: per-family gating and MIXED outcome preserved.
- **Simulation replay risk:** reusing hardcoded costs. Mitigation: this design explicitly forbids hardcoded cost constants; audit will verify tokens are from real LLM API responses and browser counts from Playwright traces; any simulation fallback triggers MEASUREMENT_INVALID per required_fixes.
- **Substrate simulation drift:** synthetic gzip vs real nginx. Mitigation: byte identity recomputed on real nginx fetches with oracle-free decompression; record nginx.conf and decompression code hash.

## 10. Analysis plan

1. Verify C1–C3 substrate/controls on real pipeline; if fail, halt as MEASUREMENT_INVALID and report.
2. Compute per-instance success, real tokens, real browser steps, real verification AUROC/precision (threshold from TRAIN), contamination via real verify() on TEST.
3. Compute pooled and per-family aggregates with Wilson CIs for rates, bootstrap CIs for cost ratios on TEST.
4. Compute amortized cost: repair+verification+10×retrieval (real retrieval cost) vs cold on TEST.
5. Apply C4–C8 decision rule on TEST split only.
6. Report per-family and pooled with raw_evidence hashes and per-instance CSV; preserve nginx/Flask/Playwright/LLM provenance.

## 11. Product consequences

- **Positive (C1–C8 PASS on real measurement):** C-DELTA-REPAIR advances HYPOTHESIS→EXPERIMENTAL (VALIDATED candidate) for single-resource perturbations on real nginx HIT-cache localhost. Justifies localized repair boundary (patch+verify) with 10× amortization, unblocks residual-novelty economics. No promotion to Product Core — localhost only, single-resource, single model; next expand to 2-3 resource radius and distributed Redis session store.
- **Negative (C4–C8 fails, C1–C3 PASS on real measurement):** Single-resource locality fails at smallest radius even with real LLM+browser+verify; product must budget repair ≈ cold cost and default to full re-exploration or RAG+fused fallback. Prevents premature repair-layer promotion and contamination risk. Graph lane pivots to C-RESIDUAL-NOVELTY matched families or C-SEMANTIC-RESOLVE abstention per Director portfolio. A valid negative here is high information — it closes the cheapest repair hypothesis.

Both outcomes are first-class and change a decision. Neither is treated as infrastructure failure.

## 12. Estimated cost and information gain

Low-Medium (but real): ~6 compute-hours, ~170k tokens single LLM model (48 instances, real nginx 1.2x + Flask HS256 + Playwright localhost). Very high information gain: first real measurement of C-DELTA-REPAIR (0/224 valid; prior was simulation that falsified C5/C8 as parameter artifacts). Either CONFIRMED or FALSIFIED-IN-SETTING materially changes claim state and next allocation for graph/runtime/product. Advances beyond saturated FRESHNESS tunnel (14 recent) per Director PIVOT rationale; cross-lane unblocking highest per unit effort.

## 13. Consequences of both outcomes

Both positive and negative outcomes are first-class and change a decision. Positive proceeds to broader radius/distributed substrate and informs SpiderKernel.invalidate() design; negative closes the cheapest repair hypothesis and redirects investment to residual-novelty matched families or semantic abstention. Neither is treated as infrastructure failure. MEASUREMENT_INVALID (C1-C3 fails) is not a negative scientific result and requires substrate fix before retry.

## 14. Preregistration freeze

This prereg.md and spec.json are frozen via freeze.json before any outcome-bearing measurement. A changed analysis after seeing outcomes is exploratory; a new confirmatory claim requires a new preregistration and untouched evidence. This design does not run outcome-bearing measurements. All 7 audit required_fixes from EXP-GRAPH-35741890679 are addressed by mandating real LLM, real Playwright, real verify(), real contamination, real nginx, increased sample adequacy, and decoupled threshold calibration.

