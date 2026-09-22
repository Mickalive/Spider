# EXP-PRODUCT-35777355953 preregistration

**Experiment ID:** EXP-PRODUCT-35777355953
**Lane:** product
**Claim:** C-SEMANTIC-RESOLVE — Goals can be resolved to applicable mechanisms without internal ids
**Status:** DESIGN — not yet frozen (freeze via deterministic freeze.json before EXECUTE)
**Director mandate:** PIVOT, SUPERSEDE — target claim C-SEMANTIC-RESOLVE, cognitive_reset=false, parent_handoff EXP-PRODUCT-35773128019 SUPERSEDE disposition. The inherited next_question (corrected kernel-integrated distill_parameterized for C-PARAM-INHERIT on WebArena-Verified v2 family hold-out) is continuity evidence only and does not drive this design per AGENTS.md precedence and research/EXPERIMENT_PACKET.md §2.

---

## 1. Question

Does porting Frontier's SURVIVES critique-reconstruct adapter (non-oracle structural analysis of intent + observation-derived AX state/retrieved_template without alias_family/query_key/target_prefix/header_key/body_field/auth_scope, model-derived calibrated confidence) into `src/spider/kernel.py` `resolve()` preserve alias-OOD correct>=0.50 (binomial p<0.05 vs 0.10, McNemar p<0.05 vs exact matcher), false_accept<=0.15 (>=0.15 below verbatim replay p<0.05), exact-match>=0.90, UNKNOWN precision>=0.85, ECE<=0.15 on synthetic orthogonal header/body/auth alias-OOD and live-browser WebShop/ALFWorld at BrowserGym 0.14.3 1280x720 with real CDP AX trees including mixed multi-channel (header+body+query) and production-SPA heterogeneity, while reporting end-to-end economics (tokens/browser/latency/retrieval+reconstruction+verification amortized) vs verbatim replay vs RAG vs rule-based proxy and vs instruction baselines with training cost/stability?

Refined falsifiable form: On synthetic pooled alias-OOD 40 tasks (30 orthogonal: 10 header ApiKey/X-Reset-Token/Bearer +10 body apiKey/key/token +10 auth scope/admin_scope/permission, each with 3 held-out variations, plus 10 mixed multi-channel header+body+query within one request) and on live BrowserGym WebShop/ALFWorld at 1280x720 with real CDP AX trees, does the product-kernel port achieve (a) synthetic pooled correct>=0.50 with binomial p<0.05 vs 0.10 and McNemar p<0.05 vs B-EXACT-MATCH (expected 0/40), (b) per-family and held-out subsets >=0.50 and mixed >=0.40, (c) false_accept<=0.15 at least 0.15 below verbatim replay with McNemar p<0.05, (d) exact-match >=0.90, (e) UNKNOWN precision>=0.85 and ECE<=0.15, (f) within 0.10 correct and 0.05 ECE of Frontier rule proxy, while reporting economics and training stability?

---

## 2. Motivation and inherited state

### 2.1 Director mandate and strategic context

The Global Research Director (cycle 35776736948, request c6395307da7a61b15855a409) diagnoses SPIDER at 247 canonical experiments as substrate-rich but claim-poor: only C-SEMANTIC-RESOLVE has clean momentum (3 consecutive SURVIVES via non-oracle reconstruction on synthetic + planned live WebShop/ALFWorld in Frontier), C-MEAS-VALID expanded to production loopback gunicorn+nginx EXPERIMENTAL, C-FRESHNESS orthogonality empirically real (r~0.02-0.04 TOST p~2e-08) but blocked on distributed session replication, while central promises C-RESIDUAL-NOVELTY, C-LLM-INHERIT, C-PRODUCT-ECON, C-PARAM-INHERIT remain HYPOTHESIS/MEASUREMENT_INVALID with no discriminating work-compression test.

Director action for product is **PIVOT, SUPERSEDE** to C-SEMANTIC-RESOLVE. Comparative reasoning (per mandate): vs continuing C-PARAM-INHERIT distill_parameterized kernel fix on WebArena family hold-out (5 consecutive kernel-integration failures, synthetic prevalence 0.8958 but AX consistency initially 0.2857 MEASUREMENT_INVALID, requires 10 families/60 tasks and amortized saving >=25% gate never passed — higher infrastructure risk than semantic-resolve which already survived live-browser intent); vs end-to-end C-LLM-INHERIT cold vs SPIDER economics (blocked pending Intel Gate0 0/3); semantic-resolve port reuses Frontier's validated harness, directly measures Skyvern-beating parameterized generalization (header/body/auth aliasing) and abstention calibration that prior hardcoded-confidence products lacked.

Rationale: Product is IDLE (streak 3, last MEASUREMENT_INVALID) despite Frontier delivering only sustained SURVIVES (3 audit PASS on non-oracle adapter: correct>=0.50, false_accept<=0.15, exact-match>=0.90, UNKNOWN precision>=0.85, ECE<=0.15 on synthetic + planned live). Porting audited Frontier capability into product kernel with strong-baseline economics is Product's charter and lowest-risk path to shipped inheritance.

Agent priors used (separately labeled, not SPIDER evidence): long-horizon path dependence / early verification, LLM overweighting of salient context (ECE<=0.15 and UNKNOWN precision>=0.85 gates essential), marginal information decay after estimator variants vs orthogonal levels, caching/replay strength vs strong RAG/instruction baselines at equal budget, and browser/network/session validity separation. These informed prioritization only.

### 2.2 Established (from Codex and accepted experiments)

- C-SEMANTIC-RESOLVE narrow synthetic SURVIVES x3 (audit PASS):
  - EXP-FRONTIER-35752577234: URL template aliasing (query-param/path-rewriting/server-routing) 30/30 1.0 Wilson [0.886,1.0] binomial p=1e-30 vs 0.10, McNemar p=1.19e-07 vs B-EXACT-MATCH 0/30, false_accept 0.0 vs verbatim 1.0 gap 1.0, exact-match 12/12 1.0, UNKNOWN precision 1.0, ECE 0.0738 synthetic orthogonal, audit PASS no oracle leak, softmax temp 0.15 + jitter, confidence std not constant.
  - EXP-FRONTIER-35757768022: orthogonal header/body/auth 30/30 1.0 (header ApiKey/X-Reset-Token/Authorization->X-Api-Key/X-Auth-Key/Api-Token, body apiKey/key/token->api_token/authToken/access_key, auth scope/admin_scope/X-Permission->permission/access_scope/X-Scope) inc held-out 9/9 1.0, ECE 0.0758, channel isolation headers-only 20/30 body-only 10/30 url-only 0/30 (non-vacuous), live 0 tasks and LEARNED unavailable correctly disclosed per freeze, remains EXPERIMENTAL not VALIDATED — audit PASS.
  - EXP-FRONTIER-35766532429: pooled 40/40 1.0 (orthogonal 30/30 1.0, mixed header+body+query 10/10 1.0 including compositional generalization), per-family 10/10 each held-out 9/9 1.0, false_accept 0.0 vs verbatim 1.0 gap 1.0 McNemar p=6.98e-10, ECE 0.0803, channel isolation non-vacuous (RULE-URL-ONLY 0/40, headers-only 20/40, body-only 10/40, mixed 0/10 single-channel), audit PASS recomputed exactly, bounded ceiling synthetic only (minimal derived dict, no AX tree, synthetic observation tautologically encodes answer via bound-then-parse), 0 live / 0 learned not fabricated.
- Prior ceiling on C-SEMANTIC-RESOLVE rejected: kernel exact-intent matcher L97 fails 0/10 path aliasing (EXP-GRAPH-34409639346) and 0/6 query-param/path-rewriting/server-routing (EXP-GRAPH-34586318405 combined 0/16), HTTP status grounding 0/12 falsified on jsonplaceholder; MEASUREMENT_INVALID oracle 30/30 (EXP-FRONTIER-35741928625) repaired by genuine adapter. Parent MEASUREMENT_INVALID due to forbidden-key oracle reading and hardcoded confidence is not evidence for genuine reconstruction.
- Frontier adapters are genuine non-oracle: signature (intent, derived_context, candidates, params) only url/method/path/query/segments/headers_observed/body_observed (+ AX for live), forbidden keys only in hidden_expected, confidence derived softmax temp 0.15 + deterministic jitter, gated UNKNOWN<0.80, registry leak 0/40.
- Production loopback substrate EXP-RUNTIME-35764329925 narrow SURVIVES (10/10 C1-C10, gunicorn+nginx) provides header/body/status discrimination but is orthogonal to semantic aliasing — this experiment does not require nginx HIT-cache.

### 2.3 Rejected / bounded

- That exact intent matching (kernel.py L97 `m.intent != intent` with confidence sort L112) solves aliasing — bounded rejection 0/16 across path and complex aliasing; product must add reconstruction.
- That oracle leak adapter (reading alias_family/query_key/target_prefix etc.) validates C-SEMANTIC-RESOLVE — bounded rejection as MEASUREMENT_INVALID (audit finds hardcoded 0.95/0.05 confidence, ECE 0.055 artificial, 30/30 trivial).
- That synthetic 1.0 reflects robustness to real DOM/AX noise — bounded: Frontier audit V1 notes derived_context tautologically encodes answer (expected_template bound then parsed back via adopt-any-observed-key), 1.0 is trivial copy, not AX denoising; ECE bimodal (3 empty bins) limits calibration transfer; no live inference yet at product level.
- That C-SEMANTIC-RESOLVE is VALIDATED/PRODUCT_CORE — remains EXPERIMENTAL; prior Frontier SURVIVES explicitly not VALIDATED until learned GRPO 3-seed and live-browser replication with economics.
- That C-PARAM-INHERIT narrow single-char POC (10 identifiers audit PASS) or harness-only 21/21 multi-param binding generalizes to real LLM family hold-out — bounded narrow ceiling, 5 kernel-integration failures, this experiment supersedes that thread per Director.
- That synthetic constants demonstrate economics — prior Product MEASUREMENT_INVALID (hardcoded tokens) is not evidence.

### 2.4 Unknown

- Does the Frontier adapter retain 1.0 (or >=0.50) when ported verbatim into product `src/spider/kernel.py` `resolve()` with product MechanismRegistry/models, real CDP AX tree parsing at 1280x720, Playwright BrowserGym integration, and product test harness (not Frontier's research/frontier/run_experiment.py)?
- Does synthetic pooled 40/40 (orthogonal 30/30 + mixed 10/10) parity hold within 0.10 correct and 0.05 ECE vs Frontier proxy after port (code path, imports, hash, confidence derivation fidelity)?
- Does mixed multi-channel composition (header+body+query within one request) generalize compositionally via product port (single-channel rewrites composed), or does single-channel isolation remain (RULE-HEADERS-ONLY 20/40, BODY-ONLY 10/40 from Frontier)?
- Does live BrowserGym WebShop/ALFWorld at 1280x720 with real CDP AX trees (not synthetic URL dict) achieve alias-OOD correct>=0.50 and false_accept<=0.15 with calibrated UNKNOWN/ECE on header/body/auth aliasing including mixed within one request and production-SPA heterogeneity (AX nodes>10, viewport diversity)?
- What are BrowserGym health rate, AX tree truncation/noise impact, and production-SPA heterogeneity effect on port?
- What are end-to-end economics: retrieval+reconstruction+verification tokens/browser/latency amortized per successful task vs B-VERBATIM-REPLAY (0-token replay where applicable) vs B-RAG-TFIDF/B-RAG-EMBED (strong retrieval) vs R-FRONTIER-RULE-PROXY vs B-INSTRUCTION (200 tokens instruction amortized f=10), and training cost/stability (rule port near-zero vs GRPO 3-seed CV if trained)?
- Is confidence calibration (ECE<=0.15, UNKNOWN precision>=0.85) preserved after port on synthetic and live (bimodal ECE regime with 3 empty bins noted)?

### 2.5 Do NOT assume

- Do not assume synthetic 40/40 1.0 from Frontier guarantees live-browser 0.50 or mixed 10/10 generalization — synthetic derived_context is tautological bound-then-parse; live AX noise, header/body extraction fidelity, and mixed composition are dominant unknowns this experiment measures.
- Do not assume ported code inherits Frontier ECE 0.08 or 1.0 trivially — product kernel integration may regress confidence derivation, jitter gating, or UNKNOWN handling; ECE and std>0.05 must be remeasured.
- Do not assume 1.0 pooled implies header/body/auth per-family equally easy — channel isolation from Frontier (url-only 0/40, headers-only 20/40, body-only 10/40, mixed 0/10 single-channel) shows family heterogeneity; assume nothing about production-SPA alias distribution.
- Do not assume live BrowserGym 0.14.3 WebShop/ALFWorld tasks are template-identical to synthetic header/body/auth families — live alias manifestation requires AX/DOM header/body parsing and may partially overlap synthetic families; report per-family live breakdown, not pooled-only.
- Do not assume C-SEMANTIC-RESOLVE is globally validated if synthetic pooled SURVIVES but live fails (or PC-BROWSERGYM-HEALTH <80%) — then claim bounds to synthetic orthogonal+mixed only with disclosure, not PRODUCT_CORE, per frozen rule.
- Do not assume C-PARAM-INHERIT WebArena family hold-out (192 tasks/49 templates/36 families dup 0.9479 AX 0.9) is exercised here — this experiment is C-SEMANTIC-RESOLVE alias-OOD, not WebArena resource parametrization; do not conflate.
- Do not assume instruction baseline (200 tokens) is dominated — must be measured at equal model/tools/budget with honest amortization; Skyvern-like code-caching baseline insight from Scout is prior, not SPIDER evidence.
- Do not assume training cost near-zero for rule port means GRPO learned variant is unnecessary — report training cost/stability explicitly; rule-vs-learned non-inferiority is exploratory for product.

---

## 3. Hypothesis

C-SEMANTIC-RESOLVE port hypothesis (H1–H2):

A product-kernel port of Frontier's genuine rule-based critique-reconstruct adapter into `src/spider/kernel.py` — conditioned only on (intent, observation-derived state from real DOM/AX tree at 1280x720 or synthetic URL/header/body dict, retrieved_template/candidates) with structural scoring (slot count, path segments, query/header/body key presence, prefix structure) and deterministic rewrite handling header+body+query including mixed multi-channel composition via alphabetically-sorted adopt-any-observed-key-not-in-registry + multi-field rewrite before `_bind`, confidence = softmax over candidate scores (temp 0.15) + deterministic jitter gated UNKNOWN when max_score<0.80 (not hardcoded, std>0.05) — will:

1. Preserve synthetic pooled alias-OOD correct>=0.50 (bonus >=0.90, target parity 1.0 within 0.10 of Frontier 40/40) with binomial p<0.05 vs 0.10 and McNemar p<0.05 vs B-EXACT-MATCH (0/40), per-family each >=0.50, held-out >=0.50, mixed >=0.40, false_accept<=0.15 with >=0.15 gap vs B-VERBATIM-REPLAY (1.0) McNemar p<0.05, exact-match>=0.90 (12/12), UNKNOWN precision>=0.85, ECE<=0.15.
2. Generalize to live BrowserGym WebShop/ALFWorld at 0.14.3 1280x720 with real CDP AX trees on header/body/auth aliasing including mixed multi-channel within one request and production-SPA heterogeneity, achieving live alias-OOD correct>=0.50 (if N_live>=20) with same binomial/McNemar thresholds and false_accept<=0.15 and calibration preserved.

Null H0: port corrupts fidelity (>0.10 drop vs frontier proxy or ECE >0.10 gap), or synthetic-to-real gap closes the effect (live <0.40 or false_accept>0.25), or calibration fails (ECE>0.15, UNKNOWN precision<0.85), so reconstruction does not provide product-level inheritance advantage beyond exact matching.

---

## 4. State, action, and target representation

### 4.1 State representation (frozen)

Pre-state S_current (context dict supplied to `resolve`): only observation-derived fields from real browser or synthetic fiction:
- `intent` (string goal)
- `url` (observed string at 1280x720), `method`, `url_path`, `url_query` dict, `url_segments` list, `headers_observed` dict, `body_observed` (JSON/string if available), `ax_tree_snapshot` (CDP AX tree text snapshot hash + truncated 2k tokens for parsing, viewport 1280x720) — for synthetic tasks `ax_tree_snapshot` absent and dict is minimal (url/method/headers_observed/body_observed).
Forbidden ground-truth signals (`alias_family`, `query_key`, `target_prefix`, `routing_prefix`, `target_style`, `path_style`, `header_key`, `body_field`, `auth_scope`, `expected_template`) stored ONLY as `hidden_expected` metadata not passed to any method. Audit inspects product kernel code for reads of forbidden keys.

Post-state S_next: resolved `bound_action` (URL/header/body with `${slot}` substituted) verified against `hidden_expected_template` bound equality including header/body field equality and for mixed all channels jointly.

### 4.2 Action representation

Mechanism `action_template` is string template containing `${slot}` parameters in URL path, query param, header value (e.g., `ApiKey: ${token}`), body JSON field, or auth scope, and for mixed tasks simultaneously header+body+query slots. Binding via deterministic kernel `_bind` plus header/body field substitution. Product reconstruction scores candidate templates' structural match to observation-derived state and/or rewrites template structure before `_bind` conditioned ONLY on (intent, observation-derived state, retrieved_template/candidates). Confidence derived from normalized structural score (softmax temp 0.15) + deterministic jitter; no hidden_expected access; constant confidence prohibited.

### 4.3 Target

Categorical resolution outcome per task:
- `correct_resolution` — bound_action equals hidden_expected bound equality (inc header/body/mixed channels jointly);
- `false_accept` — resolved to wrong template or bound incorrectly or should have abstained;
- `UNKNOWN` — correctly abstained when no applicable mechanism or gated confidence<0.80.

Calibration target: Expected Calibration Error over 5 confidence bins using derived confidence, plus abstention precision/recall. No target leakage: verification uses hidden_expected only after resolution; threshold gating <0.80 fixed in code, not fit on test.

---

## 5. Sampling plan

- **Unit of analysis:** single alias-OOD task (intent + derived state + registry).
- **Synthetic orthogonal alias-OOD:** 30 tasks = 3 families x10 intents (a) header-based (ApiKey vs X-Reset-Token vs Authorization Bearer aliasing), (b) body JSON field (apiKey vs key vs api_key vs token), (c) auth permission (scope read vs admin_scope vs permission header). Each family 7 standard +3 held-out novel forms (e.g., X-Api-Key, api_token, X-Scope) requiring key/segment analysis. Report 10/family and held-out-9 pooled.
- **Synthetic mixed multi-channel:** 10 tasks where aliasing spans header+body+query within one request (e.g., header ApiKey + body apiKey + query permission simultaneously aliased to X-Api-Key + body key + header X-Scope), requiring joint multi-field rewriting; registry training uses single-channel forms only.
- **Synthetic controls:** exact-match 12, no-applicable 12, empty-registry 6 — total 70 synthetic tasks per method.
- **Live BrowserGym WebShop/ALFWorld:** attempt 20 WebShop +20 ALFWorld =40 tasks +10 live mixed if feasible at BrowserGym 0.14.3 1280x720 with real CDP AX trees; exploratory if fewer. Production-SPA heterogeneity disclosed via viewport 1280x720 and AX diversity (nodes>10, url and method observed).
- **Registry per task:** exactly one training mechanism (train alias) + one distractor alias template equal confidence 0.9 + one exact-match distractor at 0.8, all preconditions={} guards={}.
- **Seeds:** deterministic 42,43,44 for stability triple; single harness seed 42 otherwise. BrowserGym viewport fixed 1280x720.
- **Exclusions:** harness error >20% then MEASUREMENT_INVALID; Playwright timeout >10s logged and retried once; otherwise task counts as false.

---

## 6. Holdout and contamination control

- **Holdout by alias form:** train never sees test alias form nor mixed composition (verify 0/40 synthetic templates appear verbatim in registry; same for live if available at BrowserGym). TF-IDF/embedding fit on train registry only. Reconstruction rule derived from training alias documentation only; held-out and mixed require structural generalization.
- **Registry isolation:** clone registry before each task; no shared mutable state.
- **Split integrity:** verification threshold gating <0.80 fixed, not fit on test; ECE computed on held-out alias-OOD only. Family-stratified bootstrap for CIs respects site/session grouping for live.
- **Contamination:** audit checks no method accesses hidden_expected or test-template verbatim except via observation parsing; intent-equality leak verified 0/40; live split by website (WebShop vs ALFWorld) with no site identity leakage into retriever.

---

## 7. Baselines, controls, and metrics

### 7.1 Baselines (strong, hit-capable)

| ID | Description | Expected |
|---|---|---|
| B-EXACT-MATCH | Current kernel L97 exact intent equality, min_confidence 0.8 | 0/40 alias-OOD |
| B-VERBATIM-REPLAY | Exact intent scan + verbatim _bind without rewrite | 1.0 false_accept |
| B-RAG-TFIDF | TF-IDF retriever + verbatim bind, fit train only | 0/40 alias-OOD |
| B-RAG-EMBED | Embedding cosine retriever + verbatim bind, deterministic offline | 0/40 |
| B-RANDOM | Uniform random among intent-matching mechanisms | ~5-10% chance |
| B-INSTRUCTION | Hand-authored site instructions without retrieval/reconstruction, 200 tok amortized f=10 | below product port |
| P-SPIDER-RECONSTRUCT | **Product port under test:** src/spider/kernel.py with critique-reconstruct adapter (scorer+multi-field rewriter, softmax temp0.15+jitter gated <0.80) | 40/40 1.0 synthetic |
| R-FRONTIER-RULE-PROXY | Reference Frontier RECONSTRUCTION-RULE (same logic) for parity delta | 40/40 1.0 |

### 7.2 Positive control

**PC-EXACT-MATCH:** On exact-match stratum N>=12 where test intent verbatim equals registry intent, P-SPIDER-RECONSTRUCT and R-FRONTIER-RULE-PROXY and B-EXACT-MATCH must achieve correct>=0.90 and false_accept<=0.10. Verifies product port resolves when no adaptation needed.

**PC-BROWSERGYM-HEALTH:** >=80% of attempted live tasks must load DOM/AX at 1280x720 without truncation/timeout (AX nodes>10, url/method observed). If <80% healthy, live stratum is exploratory and claim bounds to synthetic orthogonal+mixed only (not MEASUREMENT_INVALID).

### 7.3 Null control

**NC-NO-APPLICABLE:** On no-applicable stratum N>=12 where test intent OOD with no covering mechanism, every method must UNKNOWN with precision>=0.90 and false_accept<=0.10.

**NC-EMPTY-REGISTRY:** Empty registry N>=6 with any intent returns UNKNOWN 100% (validates no hallucination).

### 7.4 Primary and secondary metrics (stable identities for AUDIT)

- `M-alias-correct-pooled` (synthetic 40, Wilson 95% CI) and `M-alias-correct-orthogonal` (30), `M-alias-correct-mixed` (10), `M-alias-correct-per-family` (header 10, body 10, auth 10), `M-alias-heldout-correct` (9), `M-live-alias-correct-pooled` (if N_live>=20)
- `M-false-accept-pooled` (alias-OOD), `M-false-accept-vs-verbatim-gap`
- `M-exact-match-correct` (12), `M-no-applicable-unknown-precision`, `M-empty-registry-unknown`
- `M-ece-5bin`, `M-confidence-std`, `M-unknown-precision`
- `M-binomial-p-vs-0.10`, `M-mcnemar-p-vs-exact`, `M-mcnemar-p-false-vs-verbatim`
- Economics: `M-tokens-per-task` (retrieval+reconstruction+verification), `M-browser-calls`, `M-latency-ms`, `M-amortized-cost-per-success`, `M-retrieval-cost`, `M-reconstruction-cost`, `M-verification-cost`, `M-training-wall-clock`, `M-training-tokens`, `M-cv-across-3-seeds`
- Product parity: `M-port-delta-correct-vs-frontier`, `M-port-delta-ece-vs-frontier`

All metrics recorded per task in `raw_evidence/experiment_data.json` with SHA256; derived aggregates in `result.json`.

### 7.5 Uncertainty and adequacy

Resampling unit = task (independent by construction for synthetic; trajectory-grouped block for live if needed). Wilson 95% CI for rates, bootstrap 2000 block-permutation for ECE and McNemar, family/site-stratified where applicable. Adequacy: N>=40 synthetic pooled gives power for binomial vs 0.10 at p=0.50: power 0.92 at alpha 0.05 (n=40 true 0.50 vs null 0.10). Mixed N=10 is diagnostic (wide CI [0.722,1.0] at 10/10). Live N>=20 gives power 0.80 at p=0.50. If N<32 synthetic pooled, MEASUREMENT_INVALID.

---

## 8. Decision rule (frozen, verbatim in spec.json)

All primary thresholds on synthetic alias-OOD pooled (N>=40 unless stated); live BrowserGym exploratory/confirmatory per stated gating. Compute per-method rates with Wilson CI; paired McNemar for product vs B-EXACT-MATCH (correct) and vs B-VERBATIM-REPLAY (false_accept); one-sided binomial vs 0.10; bootstrap ECE CI 2000.

**SURVIVES_CURRENT_TEST** iff ALL hold:

(C1) PC-EXACT-MATCH passes (product and frontier proxy correct>=0.90 false_accept<=0.10 on exact-match 12/12) and PC-BROWSERGYM-HEALTH either passes (>=80% healthy) or correctly bounds live to exploratory;

(C2) NC-NO-APPLICABLE passes (product UNKNOWN precision>=0.90 false<=0.10) AND NC-EMPTY 100% UNKNOWN;

(C3) alias-OOD pooled S1: P-SPIDER-RECONSTRUCT correct>=0.50 AND binomial p<0.05 vs 0.10 AND McNemar p<0.05 vs B-EXACT-MATCH (0/40 expected) AND orthogonal subset correct>=0.50 and mixed subset correct>=0.40 and per-family each >=0.50 with held-out >=0.50;

(C4) S2: product false_accept<=0.15 AND strictly below B-VERBATIM-REPLAY by >=0.15 with McNemar p<0.05 on false_accept;

(C5) S3: product exact-match stratum correct>=0.90 (no regression, within 0.05 of frontier proxy);

(C6) S4: product no-applicable precision>=0.85 AND ECE<=0.15 (5 bins, derived confidence std>0.05);

(C7) not dominated by retrieval: product pooled correct not >0.10 below best RAG verbatim correct on same alias-OOD;

(C8) port fidelity: product pooled correct within 0.10 absolute of R-FRONTIER-RULE-PROXY and ECE within 0.05 (largest per-family gap <=0.10).

**FALSIFIED-IN-SETTING** if C3-C8 fail while C1-C2 PASS (valid negative).

**MIXED** if C3 passes but C4 or C6 fails (correct but miscalibrated/harmful).

**MEASUREMENT_INVALID** if C1 or C2 fails, oracle leak or hardcoded confidence detected, alias-OOD N<32, harness errors >20%, BrowserGym integration broken for product kernel synthesis, or product kernel hash unchanged (no port).

Live confirmatory (if N_live>=20 and PC-BROWSERGYM-HEALTH passes): report same S1-S2 on live pooled+orthogonal+mixed; synthesis SURVIVES requires synthetic C3-C8 plus live alias-OOD correct>=0.50 binomial p<0.05 vs 0.10 and false_accept<=0.15; if live fails but synthetic passes, overall SURVIVES bounded to synthetic orthogonal+mixed with disclosure (not FALSIFIED). Economics/training reported regardless but not gating unless economics degrades >2x vs frontier proxy.

---

## 9. Validity threats

- **Target leakage:** post-state hidden_expected leaking into reconstruction decision without observation parsing. Mitigation: harness filters forbidden keys before resolve, threshold gating TRAIN-only, audit checks zero forbidden-key reads and zero registry leak 0/40.
- **Split integrity:** TF-IDF/embedding fit on TEST would inflate RAG baseline. Mitigation: fit on TRAIN only, audit recomputes.
- **Sampling integrity:** non-independent tasks sharing global state. Mitigation: per-task registry clone, seed determinism via hashlib, trajectory-grouped bootstrap for live.
- **Representation integrity:** synthetic derived_context tautologically contains answer (bound-then-parse) vs live AX tree noise. Mitigation: disclose synthetic tautology, require live stratum for non-trivial claim, report channel isolation (url-only 0/40 vs headers-only 20/40) proving not vacuous single-channel.
- **Policy confounding:** agent LLM memorizing alias table rather than observing. Mitigation: held-out 9 novel forms (X-Api-Key, api_token, X-Scope) requiring key/segment analysis, mixed composition requiring generalization, audit checks generic adopt-any-observed-key logic not table lookup.
- **Calibration gaming:** hardcoded confidence 0.95/0.05 would fake ECE. Mitigation: require std>0.05 across tasks, softmax derivation inspectable, ECE computed with derived confidence, audit checks constant.
- **Browser substrate:** BrowserGym Playwright 0.14.3 install/truncation could make live appear failed. Mitigation: PC-BROWSERGYM-HEALTH gate (80% healthy), report viewport 1280x720 and AX nodes>10, scope live to exploratory if health fails.
- **Falsifier mis-specification:** single family or single mixed failure should not be pooled away. Mitigation: per-family gating and MIXED outcome preserved.

---

## 10. Analysis plan

1. Verify product port committed to src/spider/kernel.py (hash diff vs base f705c96a, audit import checks no forbidden keys, confidence std>0.05).
2. Verify C1-C2 substrate/controls; if fail, halt as MEASUREMENT_INVALID and report.
3. Compute synthetic pooled, orthogonal, mixed, per-family, held-out, exact-match, no-applicable, empty-registry rates with Wilson/bootstrap; compute McNemar and binomial p-values; compute ECE 5-bin and confidence std.
4. Compute live BrowserGym pooled if N_live>=20 with same metrics and Wilson CI, plus viewport/AX health.
5. Compute port fidelity deltas vs R-FRONTIER-RULE-PROXY (pooled correct and ECE gaps).
6. Compute economics: tokens/browser/latency per method, retrieval+reconstruction+verification amortized per success vs B-RAG/B-VERBATIM/B-INSTRUCTION/frontier proxy; report training wall-clock/tokens/CV across 3 seeds (42,43,44).
7. Apply C3-C8 decision rule on synthetic; synthesis over live per gating.
8. Report pooled, per-family, held-out, mixed, live breakdown; preserve raw_evidence hashes.

---

## 11. Product consequences

- **Positive (C1–C8 PASS synthetic, and live confirmatory or correctly bounded exploratory):** Validates genuine non-oracle reconstruction beyond URL path/query to orthogonal header/body/auth including mixed header+body+query composition on real CDP AX trees at 1280x720 with production-SPA heterogeneity, parity fidelity to Frontier within delta, calibrated abstention. Product should add reconstruction layer after retrieval (critique-reconstruct conditioned on intent+observation-derived AX state+retrieved_template, confidence-gated UNKNOWN<0.80) before _bind/execute, with verification/repair boundary. Unblocks cross-site parameterized transfer where header/body/auth aliasing is common. C-SEMANTIC-RESOLVE advances from EXPERIMENTAL (narrow synthetic) to VALIDATED at product-kernel level bounded to genuine reconstruction on tested orthogonal families + mixed + live (PRODUCT_CORE candidate pending learned GRPO 3-seed stability and end-to-end at scale); `promote_to_product=true` pending audit PASS and browser integration tests. Report economics vs strong baselines for C-PRODUCT-ECON sequencing.
- **Negative (C3–C8 fails, C1–C3 PASS):** Port or generalization fails (mixed <0.40, live <0.40, false_accept>0.15, ECE>0.15, or >0.10/0.05 degradation vs frontier). Product must NOT add reconstruction layer for these families/compositions/live; keep exact-intent matching, require exact intents or pre-normalized templates; prioritize explicit alias catalogs, server-side routing normalization, or per-site mapping tables. Frontier mechanism closed for this adapter class/families incl held-out/mixed/live; next Frontier attack tests orthogonal basin (workflow compilation, DAG synthesis, program-synthesis repair). C-SEMANTIC-RESOLVE remains EXPERIMENTAL at prior 40/40 synthetic narrow ceiling (bounded falsification for tested adapter, not global falsification). Product lane pivots per Director guidance to runtime session-affinity, residual-novelty, or alternative semantic mechanisms.

---

## 12. Estimated cost and information gain

Low-moderate: 70 synthetic + up to 50 live =120 tasks x8 methods =960 deterministic kernel resolve+bind calls plus TF-IDF/embedding offline (<25 min CPU, no paid LLM for rule port). Product port code change <200 lines in src/spider/kernel.py plus tests. BrowserGym 0.14.3 + Playwright chromium at 1280x720 adds <50 browser navigations (<45 min). Total <5h single runner, no large datasets committed. Very high information gain: first product-level test of 3x SURVIVES genuine reconstruction by porting audit-PASS adapter into shippable kernel and testing live generalization plus mixed composition plus parity and economics vs verbatim/RAG/instruction/Skyvern-relevant baselines — directly decides PRODUCT_CORE promotion for C-SEMANTIC-RESOLVE and unblocks cross-site transfer sequencing. Either outcome decisively changes claim/product decision and informs whether narrow synthetic 1.0 transfers beyond tautological observation to real AX heterogeneity.

---

## 13. Consequences of both outcomes

Both positive and negative outcomes are first-class and change a decision. Positive proceeds to PRODUCT_CORE promotion path and broader radius/distributed substrate and learned GRPO stability; negative cleanly closes this product-kernel adapter hypothesis for header/body/auth/mixed/live and redirects investment to orthogonal mechanisms. Neither is treated as infrastructure failure unless PC/NC or oracle leak fails, in which case MEASUREMENT_INVALID preserves decision pending repair without false falsification.

---

## 14. Preregistration freeze

This prereg.md and spec.json are frozen via freeze.json before any outcome-bearing measurement. A changed analysis after seeing outcomes is exploratory; a new confirmatory claim requires a new preregistration and untouched evidence. This design does not run outcome-bearing measurements.
