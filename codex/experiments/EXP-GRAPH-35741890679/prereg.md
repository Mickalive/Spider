# EXP-GRAPH-35741890679 preregistration

**Experiment ID:** EXP-GRAPH-35741890679
**Lane:** graph
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally
**Status:** DESIGN — not yet frozen (freeze via deterministic freeze.json before EXECUTE)
**Director mandate:** PIVOT, SUPERSEDE — target claim C-DELTA-REPAIR, cognitive_reset=true, parent_handoff EXP-GRAPH-35611618323 SUPERSEDE disposition. The inherited next_question (distributed Redis/sticky-routing for C-FRESHNESS) is continuity evidence only and does not drive this design per AGENTS.md precedence and research/EXPERIMENT_PACKET.md §2.

---

## 1. Question

After runtime's verified byte-preserving nginx HIT-cache substrate (oracle-free decompression 960/960 byte-identical across HIT/SWR/SIE/304 stages), does a controlled single-resource local perturbation — single DOM attribute/text change, endpoint param/header change, or Cache-Control/ETag mutation — require only localized repair (bounded tokens/browser/verification cost, contamination < threshold) versus full cold re-exploration, with repair cost amortized over retrieval frequency?

Refined falsifiable form: Is mean localized repair cost <50% of full re-exploration tokens and <40% of browser interactions, with contamination <10%, verification AUROC ≥0.75 (precision ≥0.80), and amortized repair cheaper than full at n_reuses=10, when repairing a single-resource perturbation on the nginx HIT-cache localhost substrate?

## 2. Motivation and inherited state

### 2.1 Director mandate and strategic context

The Global Research Director (cycle 35741318902, request 03d5190ad07ed3eccbc250d3) performed a cognitive reset across 224 canonical experiments. Diagnosis: Graph 30-streak and Runtime 40-streak on C-FRESHNESS/C-MEAS-VALID localhost mocks with pooled r=0.002–0.046 (CI upper 0.06–0.135, TOST PASS at delta=0.15) and production-like stratified r≈0.041 (CI upper 0.116) and even distributed 2-node Flask r=−0.038 to −0.058 (CI upper <0.15) despite C1 TN=0.667. The 31st freshness replication (session-affinity Redis fix) would only raise C1 TN to 1.0 on /api/session/status — already-identified infrastructure artefact, marginal information low. Three lanes idle; C-DELTA-REPAIR has 0/224 experiments yet is priority for graph/runtime/product and directly tests "pay novelty not whole task" with repair boundaries. Runtime's nginx HIT/SWR/SIE 960/960 byte-identical oracle-free substrate now unblocks controlled local perturbations. First measurement here changes architecture/product decision; another freshness replication does not.

Comparative reasoning (per mandate): vs CONTINUE C-FRESHNESS distributed Redis/sticky routing (handoff) — correlation already demonstrated, low marginal gain; vs PIVOT to C-SEMANTIC-RESOLVE calibrated abstention (0/6 alias fails p=0.016) — also neglected but delta-repair is completely untested and prerequisite for residual-novelty amortization; vs C-PARAM-INHERIT noisy observations — kernel distill_parameterized falsified twice (D1 noise, E1 pattern-absence) and needs Intel AX-validated families first.

Agent priors used (separately labeled, not SPIDER evidence): path dependence/local optima compounding, applicability guards/false-accept economics, identifiability/history-conditioned baselines, and tunneling diagnostics. These informed prioritization only.

### 2.2 Established (from Codex and accepted experiments)

- C-FRESHNESS orthogonality at delta=0.15 CONFIRMED on LOCAL testbed (stratified r=0.041–0.058, CI upper 0.09–0.125, TOST PASS, n_non304=684–844) and correlation confirmed distributed (r=−0.038, CI upper 0.029 <0.15, TOST p=2e−08, n=844) per EXP-GRAPH-35611618323 audit PASS. C3–C7 all PASS distributed; C1 failure is session non-replication, not correlation.
- HS256 symmetric JWT with shared TESTBED_SECRET resolves token cross-node validation (TP=1.0) vs prior RSA bug.
- Runtime C-MEAS-VALID narrowly survives on Flask 3.1.3 + PyJWT 2.13.0 HS256 localhost (full-vector discrimination 1.0, null FP 0.0%) and on verified nginx HIT-cache substrate with byte-preserving decompression (oracle-free) — dependency for this experiment.
- C-PARAM-INHERIT narrow single-char POC survives in harness but kernel integration falsified twice for noisy observations — not blocking for delta-repair.
- Parent EXP-GRAPH-35611618323 established: NumpyEncoder fix, B-CONCURRENT N=5 coupling absent, B-CONFOUND distributed |r|=0.912.

### 2.3 Rejected / bounded

- C-FRESHNESS reaches VALIDATED/PRODUCT_CORE — not warranted; bounded to LOCAL + distributed correlation, C1 gated.
- Stateless round-robin without session affinity for distributed CONFIRMED — falsified.
- HTTP caching as common cause for |r|>0.15 — falsified across 8+ mocks.
- C-PRODUCT-ECON logistic extrapolation — definitively REJECTED (6-model vacuous step).
- C-WEB-DYNAMICS TV/KDE only-translation-detectable (rho 1.0 d=9.1, scaling −0.12) — synthetic-only ceiling.

### 2.4 Unknown

- Whether any local perturbation is repairable locally (0 prior experiments for C-DELTA-REPAIR).
- Repair cost, contamination, verification boundary, and amortization — all unknown.
- Whether runtime HIT-cache byte identity holds under controlled mutations (assumed per dependency but re-verified here).
- Residual-novelty economics beyond doc survey, cross-site holdout, LLM-inheritance with strong baselines.

### 2.5 Do NOT assume

- C-DELTA-REPAIR holds because freshness correlation holds — orthogonal claims.
- Distributed session-affinity fix generalizes to repair locality — distinct substrate concerns.
- Localized repair is cheaper — this is the hypothesis under test, not an assumption.
- Verbatim replay or RAG retrieval suffices for drift — must be measured vs repair.
- 960/960 byte identity generalizes beyond localhost nginx — bounded to stated fixture.
- Single-resource success implies multi-resource or distributed repair success.
- C-FRESHNESS handoff `next_question` determines this experiment — superseded by Director PIVOT per AGENTS.md and research/EXPERIMENT_PACKET.md.

## 3. Hypothesis

C-DELTA-REPAIR hypothesis (H1): A single-resource local perturbation is repairable by a localized patch (re-target selector, rebind param slot, update header expectation, refresh cache key) without full-task re-exploration, with bounded cost and low contamination.

Operational predictions:

1. Localized repair succeeds on ≥80% of perturbation instances (≥70% per family).
2. Mean repair tokens <0.50 × mean full cold re-exploration tokens; mean browser interactions <0.40 × full.
3. Verification discriminates correct vs incorrect patch (AUROC ≥0.75, precision ≥0.80 at operating threshold).
4. Contamination of unrelated mechanisms <0.10.
5. Amortized cost (repair + verification + 10×retrieval_cost) < full cold cost at n_reuses=10.

Byte-preserving HIT-cache substrate guarantees cache correctness is orthogonal: decompressed body SHA256 identity across HIT/SWR/SIE/304 is 960/960 pre-perturbation, so post-perturbation divergence is attributable to the controlled local change, not decompression artefacts.

Null H0: repair cost ≥ full cost or contamination ≥0.10 or success <0.80 or verification near chance, so local patch is not separated from full re-exploration.

## 4. State, action, and target representation

### 4.1 State representation (frozen for this experiment)

Pre-state S_current: (Mechanism registry snapshot, page DOM snapshot + accessibility tree subset, HTTP response headers (ETag, Cache-Control, Content-Encoding), URL+query, cache state HIT/SWR/SIE/304). Raw observation preserved: DOM, headers, decompressed body bytes, cache status header.

Post-state S_next: (updated DOM/response after perturbation or after repair, verification postconditions match).

### 4.2 Action representation

- Repair action: patch := {selector rewrite | param slot rebind | header expectation update | cache key refresh}, executed as single registry mutation + 1–2 Playwright probes (goto, evaluate selector existence, fetch).
- Full re-exploration action: LLM agent trajectory from scratch (observe → plan → act → verify) with same model/tools/budget, no registry reuse.

### 4.3 Target

Binary repair success (verify()=true and oracle ground-truth functional correctness) plus continuous cost metrics. No target leakage: verification threshold calibrated on TRAIN perturbation split only; post-state never leaks into pre-state features for threshold fitting.

## 5. Sampling plan

- **Unit of analysis:** single perturbation instance (one resource, one mutation).
- **Perturbation families (3 × 2 variants × 6 seeds = 36 instances):**
  - F-DOM: (D1) single attribute change (#submit-123→#submit-124, data-testid rename), (D2) single text node change (button label "Submit"→"Send").
  - F-ENDPOINT: (E1) query param rename (?id=→?item=), (E2) header name change (X-Request-Id → X-Req-Id).
  - F-CACHE: (C1) Cache-Control max-age 60→3600, (C2) ETag value mutation (SHA change reflecting body change).
- **Unrelated mechanism set:** N≥20 mechanisms from distinct intents/endpoints for contamination measurement.
- **Pre-perturbation mechanisms:** distilled from successful pre-perturbation observations (confidence 0.5 literal, promoted to ≥0.8 for validated).
- **Seeds:** deterministic per instance (hash-based derivation, never Python hash()); record seed manifest.
- **Exclusions:** nginx config reload failure, 5xx unrelated to perturbation, Playwright timeout >10s — logged and retried once; exclude only if persistent infrastructure failure (then MEASUREMENT_INVALID).
- **Substrate:** nginx 1.2x reverse-proxy + Flask 3.1.3 backend + PyJWT HS256 + SQLite, localhost, Content-Encoding gzip where applicable, oracle-free decompression path (gzip.decompress without oracle lookup).

## 6. Holdout and contamination control

- **Holdout by perturbation instance:** threshold calibration (verification operating point) fit on TRAIN half of instances (18), evaluated on held-out TEST half (18). Family-stratified split.
- **Registry isolation:** clone registry before each repair; measure contamination as fraction of uninvolved mechanisms where post-repair verify status flips or false-accept introduced, using frozen pre-perturbation evaluation suite. No shared mutable state across instances.
- **Perturbation manifest holdout:** repair agent never sees manifest old→new mapping; only sees pre-perturbation mechanism + post-perturbation observation (DOM/response) + verify() outcome.

## 7. Baselines, controls, and metrics

### 7.1 Baselines (strong, hit-capable)

- B-COLD-FULL-REEXPLORATION — full cost reference.
- B-VERBATIM-REPLAY — 0-token replay fails post-perturbation (proves perturbation is breaking).
- B-RETRIEVAL-RAG — semantic trajectory retrieval without patch.
- B-ORACLE-HAND-PATCH — cost ceiling (1 probe + 1 verify).
- B-RUNTIME-BYTE-IDENTITY — 960/960 pre-perturbation identity check.

### 7.2 Positive control

PC-LOCALIZED-REPAIR-SUCCEEDS: PC1 unperturbed execute+verify 100%; PC2 known-break single-attribute with oracle patch ≥90% success and cost ratio <0.5 vs B-COLD. Both computed identically to primary repair pipeline.

### 7.3 Null control

NC-ZERO-AND-DISTANT-PERTURBATION: NC1 zero perturbation cost=0 contamination=0; NC2 distant perturbation no-op. Random-patch permutation null verifies AUROC baseline 0.5.

### 7.4 Primary and secondary metrics (stable identities for AUDIT)

- M-repair_success_rate (pooled, per-family; Wilson 95% CI)
- M-repair_tokens_mean, M-repair_tokens_ratio_vs_cold
- M-browser_interactions_mean, M-browser_ratio_vs_cold
- M-verification_steps_mean, M-verification_auroc, M-verification_precision, M-verification_recall
- M-contamination_rate (unrelated mechanisms), M-false_accept_rate
- M-amortized_cost_tokens_10, M-amortized_cost_browser_10, M-cold_cost_tokens, M-cold_cost_browser
- M-byte_identity_hit_swr_sie_304_sha_match_rate (pre and post)
- M-retrieval_cost_tokens (for amortization), M-replay_success_rate, M-retrieval_success_rate
- M-wall_time_seconds (exploratory)

All metrics recorded per instance in raw_evidence/experiment_data.json with SHA256; derived aggregates in result.json.

### 7.5 Uncertainty and adequacy

Resampling unit = perturbation instance (independent by construction). 95% Wilson CIs for rates, bootstrap (by instance, 2000 resamples) for cost ratios. Adequacy: 36 instances gives ±0.14 CI half-width at p=0.8; per-family 12 gives ±0.22 — flagged as narrow but pre-registered. If n<24, MEASUREMENT_INVALID.

## 8. Decision rule (frozen, verbatim in spec.json)

All thresholds applied on frozen pre-registered TEST data only. Gates:

(C1) PC1 success=1.0 and PC2 repair success ≥0.90; else MEASUREMENT_INVALID.
(C2) NC1 cost=0 and NC2 contamination=0 and random-patch false-accept ≤5%; else MEASUREMENT_INVALID.
(C3) B-RUNTIME-BYTE-IDENTITY pre-perturbation byte-identity ≥0.99 (960/960 equivalent); else MEASUREMENT_INVALID.

Primary (require ALL to CONFIRM localized repair):
(C4) repair success ≥0.80 pooled AND ≥0.70 per family.
(C5) mean repair tokens <0.50× mean B-COLD tokens AND mean browser <0.40× B-COLD AND mean verification steps ≤2.
(C6) contamination <0.10.
(C7) verification AUROC ≥0.75 and precision ≥0.80 at operating threshold.
(C8) amortized cost at n_reuses=10 (repair+verification+10×retrieval) < B-COLD cost (both tokens and browser).

CONFIRMED if C1–C8 all PASS. FALSIFIED-IN-SETTING if any of C4–C8 fails while C1–C3 PASS (valid negative). MEASUREMENT_INVALID if C1–C3 fails or n<24 or byte identity fails. MIXED if family-heterogeneous (≥1 family passes C4–C8 while another fails) — report per-family ceilings and do not claim pooled confirmation. Effect sizes, CIs, per-family breakdown required.

## 9. Validity threats

- **Target leakage:** post-state body/URL leaking into repair decision without verification. Mitigation: repair prompt sees only pre-mechanism + post-observation, threshold fit TRAIN-only, audit checks no manifest label in prompt.
- **Split integrity:** verification threshold fit on TEST would inflate AUROC. Mitigation: TRAIN/TEST split per §6, audit recomputes split compliance.
- **Sampling integrity:** non-independent instances sharing global nginx state. Mitigation: per-instance Flask+nginx cache isolation (cache purge + registry clone), seed determinism via hashlib.
- **Representation integrity:** DOM hash collapsing distinct states or byte digest missing mutation. Mitigation: store raw decompressed bytes + DOM snapshot + headers, not hash alone; hash is derived.
- **Policy confounding:** agent LLM may memorize perturbation pattern rather than observe. Mitigation: variant diversity, unrelated mechanism contamination, retrieval baseline comparison.
- **Ceiling effects:** oracle hand-patch trivially 1 probe — does not prove autonomous repair is cheap. Mitigation: autonomous repair cost measured separately vs oracle ceiling, not conflated.
- **Falsifier mis-specification:** single family failure should not falsify all families. Mitigation: per-family gating and MIXED outcome preserved.

## 10. Analysis plan

1. Verify C1–C3 substrate/controls; if fail, halt as MEASUREMENT_INVALID and report.
2. Compute per-instance success, tokens, browser steps, verification AUROC/precision (threshold from TRAIN), contamination.
3. Compute pooled and per-family aggregates with Wilson/bootstrap CIs.
4. Compute amortized cost: repair+verification+10×retrieval vs cold.
5. Apply C4–C8 decision rule on TEST split.
6. Report per-family and pooled; preserve raw_evidence hashes.

## 11. Product consequences

- **Positive (C1–C8 PASS):** C-DELTA-REPAIR advances HYPOTHESIS→EXPERIMENTAL/VALIDATED for single-resource perturbations on nginx HIT-cache localhost. Justifies localized repair boundary (patch+verify) with 5–10× amortization, unblocks residual-novelty economics. No promotion to Product Core — localhost only, synthetic drift.
- **Negative (C4–C8 fails, C1–C3 PASS):** Single-resource locality fails at smallest radius; product must budget repair ≈ cold cost and default to full re-exploration or RAG+fused fallback. Prevents premature repair-layer promotion and contamination risk. Graph lane pivots to C-RESIDUAL-NOVELTY matched families or C-SEMANTIC-RESOLVE abstention per Director portfolio.

## 12. Estimated cost and information gain

Low-Medium (~5 compute-hours, localhost nginx+Flask, single LLM model). Very high information gain: first measurement of C-DELTA-REPAIR (0/224), directly tests "pay novelty not whole task" with strong 0-token replay baseline, contamination, and byte-preserving substrate dependency. Either outcome changes claim state and next allocation per Director PIVOT rationale.

## 13. Consequences of both outcomes

Both positive and negative outcomes are first-class and change a decision. Positive proceeds to broader radius/distributed substrate; negative closes the cheapest repair hypothesis and redirects investment. Neither is treated as infrastructure failure.

## 14. Preregistration freeze

This prereg.md and spec.json are frozen via freeze.json before any outcome-bearing measurement. A changed analysis after seeing outcomes is exploratory; a new confirmatory claim requires a new preregistration and untouched evidence. This design does not run outcome-bearing measurements.

