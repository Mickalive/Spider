# EXP-FRONTIER-35757768022 preregistration — Frontier C-SEMANTIC-RESOLVE: genuine reconstruction to live BrowserGym + orthogonal alias families (header/body/auth) with learned vs rule comparison

**Lane:** frontier — Charter: search outside current solution basin for high-upside falsifiable mechanisms that could radically reduce agent exploration or change SPIDER architecture.
**Claim:** C-SEMANTIC-RESOLVE (Goals can be resolved to applicable mechanisms without internal ids) — Status HYPOTHESIS per registry; bounded EXPERIMENTAL per parent synthetic URL POC (30/30 rule-based SURVIVES, ECE 0.0738) not yet replicated on live BrowserGym nor orthogonal header/body/auth families nor with learned adapter.
**Director mandate:** REOPEN to C-SEMANTIC-RESOLVE, `cognitive_reset=false`, `parent_handoff_disposition=USE`, `comparative_reasoning` prioritizes live-browser semantic reconstruction over another synthetic TV variant (see request.json:director_mandate). Binding question verbatim in `request.json:director_mandate.question` — tested here as genuine (non-oracle) state-conditioned reconstruction adapter without ground-truth signals, generalizing beyond synthetic URL aliasing to live WebShop/ALFWorld and orthogonal alias families (header ApiKey/X-Reset-Token, body JSON field, auth permission) at BrowserGym 1280x720 with real CDP AX trees, with calibrated UNKNOWN and economics vs rule proxy and RAG. Continuity evidence from parent handoff preserved per AGENTS.md.
**Experiment ID:** EXP-FRONTIER-35757768022 — **Freeze required before any outcome inspection.**

## 1. Question and hypothesis

**Operational question (Director binding):** Does a genuine (non-oracle) state-conditioned reconstruction adapter that critiques/reconstructs the retrieved template via structural analysis of `(intent, observation-derived state from real DOM/AX tree at 1280x720, retrieved_template)` — without access to ground-truth `alias_family/query_key/target_prefix/header_key/body_field/auth_scope` signals and without hardcoded confidence — generalize beyond synthetic URL aliasing POC (30/30 rule-based synthetic SURVIVES) to live-browser WebShop/ALFWorld aliasing and to orthogonal alias families (header-based ApiKey/X-Reset-Token, body JSON field, auth permission) at BrowserGym 1280x720 with real CDP AX trees: alias-OOD `correct_resolution >=0.50` (binomial p<0.05 vs 0.10, McNemar p<0.05 vs exact matcher), `false_accept <=0.15` (>=0.15 below verbatim replay, p<0.05), `exact-match >=0.90`, `no-applicable UNKNOWN precision >=0.85` with `ECE <=0.15`, and report training cost/stability and verification-boundary economics vs rule-based proxy and vs RAG baseline?

**Hypothesis (directional):** Yes — a lightweight genuine reconstruction adapter that parses `intent` verb+resource, scores each candidate mechanism's template structurally against the **observation-derived** state (slot count, path segments, query-key / header-key / body-field presence, prefix structure, AX-tree derived URL/header/body signals) selects or rewrites the best template then `_bind`, with confidence derived from normalized structural match score (softmax temp 0.15 + deterministic jitter gated UNKNOWN when max_score <0.80, not hardcoded 0.95/0.05), will achieve substantially higher `correct_resolution` and lower `false_accept` on alias-OOD including orthogonal header/body/auth families and live BrowserGym tasks than exact matching and verbatim replay, while preserving `>=0.90` on exact-match and maintaining calibrated abstention (`precision >=0.85`, `ECE <=0.15`). A learned GRPO/System-One variant trained only on synthetic orthogonal alias families (not on held-out-3 variations nor live tasks) to critique/reconstruct from `(intent, observation-derived state, retrieved_template)` with model-derived calibrated confidence will match the rule-based proxy within 0.10 absolute on alias-OOD correct and within 0.05 on ECE, with measurable training cost/stability and verification economics.

**Null hypothesis:** Genuine reconstruction does not improve over exact matching/verbatim, or does so only by inflating false accepts / miscalibration — alias-OOD `correct <0.40` or not significantly above exact matcher (0/30 expected), or `false_accept >0.25` or not `>=0.15` below verbatim, or exact-match regression, or abstention miscalibration (ECE >0.25, precision <0.70). Learned variant fails to match rule proxy (>0.15 below) or shows instability CV>0.5. Live BrowserGym shows no generalization (correct <0.30).

**Inherited state (from parent handoff EXP-FRONTIER-35752577234 — USE disposition, sha 70b4b75c):**
- Established: `C-SEMANTIC-RESOLVE` genuine rule-based reconstruction ceiling EXPERIMENTAL (bounded): alias-OOD 30/30 correct (1.0 Wilson [0.886,1.0] binomial p=1e-30 vs 0.10, McNemar p=1.19e-07 vs B-EXACT-MATCH), false_accept 0.0 (diff 1.0 vs verbatim), per-family 10/10 each (query-param 7+3 held-out, path-rewriting 7+3, server-routing 7+3) held-out 9/9 1.0, exact-match 12/12 1.0, no-applicable 12/12 UNKNOWN 1.0, empty 6/6, ECE 0.0738 (5 bins, bootstrap mean 0.0737 CI [0.066,0.081], bimodal conf 0.058 vs 0.919), S1-S5 all PASS, audit PASS. Bounded to synthetic URL template aliasing only, rule-based structural inversion, minimal derived dict (url,method,url_path,url_query,url_segments), softmax confidence temp 0.15 + jitter gate 0.80. Baselines: B-EXACT-MATCH 0/30, B-VERBATIM 0/30 1.0 false, B-RAG-TFIDF 0/30, B-RAG-EMBED 0/30, B-RANDOM 0/30. Validity controls PASS with inspectable `reconstruct_resolve(intent, derived_context, retrieved_candidates, params)` only observation-derived fields, forbidden keys only in hidden_expected, confidence varies (0.91-0.97 vs 0.05-0.06). Prior narrow ceiling preserved: SpiderKernel.resolve L97/112 fails alias aliasing (0/16 alias, 0/12 status). Parent oracle MEASUREMENT_INVALID (EXP-FRONTIER-35741928625) superseded.
- Rejected (bounded): deterministic exact-intent matching and verbatim replay without structural rewriting rejected for alias-OOD URL families at equal confidence 0.9 (0/30, McNemar p=1.19e-07); shallow lexical retrieval then verbatim bind rejected (0/30) when intent held equal; naive replay maximal harm (1.0 false_accept) on tested synthetic distribution. Not global rejection; no bounded rejection of reconstruction class (current 1.0 is rule-based POC only).
- Unknown (binding): learnability of GRPO/System-One vs hand-coded rule and training cost/stability/calibration with model-derived confidence; generalization to real WebShop/ALFWorld live-browser and to header/body/auth families (proxy 0/20 prior); whether perfect 1.0 reflects synthetic easiness ('val' pattern, tightly coupled inversion) vs robustness; calibration sensitivity (ECE bimodal, threshold 0.80); System-One scoring/budget variant not tested; product economics (verification/repair boundary, false_accept vs abstention tradeoff).
- Do-not-assume (binding): Do not assume 30/30 / 0.0 false_accept / ECE 0.0738 generalizes beyond synthetic URL aliasing with minimal derived dict to real Web, production SPAs, DOM/auth/session/drift — synthetic-to-real gap dominant; do not assume rule proxy validates GRPO learnability; do not assume ECE bootstrap proves real calibration with different binning/abstention conventions (bimodal 18 at 0.058 vs 42 at 0.919, threshold 0.80 kernel min_confidence); do not assume per-family uniform 10/10 or held-out 9/9 demonstrates wild heterogeneity (structurally similar variants); do not assume B-EXACT 0/30 or RAG 0/30 proves any retriever fails (intent held equal); do not assume WebShop/ALFWorld generalization without live-browser replication with real Playwright traces and DOM/response verification; do not treat MEASUREMENT_INVALID repair as global VALIDATED — status EXPERIMENTAL rule-based; requires learned+live gates for PRODUCT_CORE; do not infer cross-site parameterized transfer without verification boundary.

This design directly addresses the two dominant unknowns (learned stability and synthetic-to-real gap) while preserving the Director's REOPEN target. It does NOT repeat the prior 30+ freshness/PMI/TV loops (graph 9/10, frontier 13/15 tunnel) — orthogonal mechanism per charter.

## 2. State, action, target, unit of analysis

**State representation (raw → derived):**
- Raw (live BrowserGym): Playwright at viewport 1280x720, CDP AX tree snapshot, observed `url`, `method` (GET/POST), `headers_observed` (standard headers via CDP/network), `body_observed` (JSON string/body if present via network/DOM), plus `intent` string (goal). Derived: `url_path` (split `/`), `url_query` dict (parse `?k=v`), `url_segments` list, `header_keys_observed` (lowercased keys), `body_json_keys` (parsed JSON keys if applicable), `ax_tree_text_hash` (hash of visible text for verification), truncated AX text 2k tokens for parsing. **Losses disclosed:** visual layout pixels, timing, auth/session token values beyond key presence — if they matter for broader resolution, effect bounded to tested header/body/auth aliasing.
- Raw (synthetic orthogonal): `url` string as observed, `method`, synthetic `headers_observed`/`body_observed` dicts. Derived same fields without AX tree to isolate orthogonal alias mechanism.
- **Forbidden:** `alias_family`, `query_key`, `target_prefix`, `routing_prefix`, `target_style`, `path_style`, `header_key`, `body_field`, `auth_scope`, `expected_template`, `resource` answer labels are NOT in derived context; stored only as hidden `expected` metadata for scoring, not passed to methods. Audit will verify no read of forbidden keys and no constant confidence.

**Action representation:**
- Mechanism `action_template` is URL/header/body/auth template strings with `${slot}` (e.g., `/users/${id}`, `ApiKey: ${token}` vs `X-Reset-Token: ${token}`, `{"apiKey":"${token}"}` vs `{"key":"${token}"}`, `scope:${perm}`). Binding via deterministic `kernel._bind` plus header/body field substitution (string replace). Genuine reconstruction may (a) score each candidate template's structural match to derived state (count `${}` slots, match segments, detect query/header/body key presence, AX parsing) and select best, and/or (b) rewrite template structure before `_bind` (path↔query, header rename ApiKey↔X-Reset-Token↔X-Api-Key, body field rename apiKey↔key↔api_token, permission scope mapping) conditioned **only** on `(intent, derived_state, retrieved_template/candidates)`. No hidden_expected access.

**Target (primary measurand):**
- Per-task outcome in `{correct_resolution, false_accept, UNKNOWN}` (mutually exclusive, sum to 1 per stratum).
  - `correct_resolution` = adapter selects (or rewrites to) alias-correct template and `bound_action` (url+header+body) equals `expected_bound` (hidden_expected_template bound with params, including header/body field equality).
  - `false_accept` = selects wrong template or binds incorrectly when should abstain/select correct; includes resolving when should UNKNOWN.
  - `UNKNOWN` = correctly abstains when no applicable mechanism (no-applicable/empty) or calibrated gate `confidence<0.80`.
- Secondary: calibration — `ECE` over 5 confidence bins (confidence derived from structural/model score), abstention precision/recall; per-family (header/body/auth) and held-out-3 subset breakdown; live vs synthetic breakdown; training cost/stability (wall-clock, tokens/calls, variance); verification economics (retrieval+reconstruction+verification steps, cost per task).

**Unit of analysis:** Single `resolve+bind(+optional genuine rewrite)` call per task. Paired design: each task evaluated under each method (within-task). Resampling unit is task (block bootstrap over tasks, trajectory-grouped for live BrowserGym if tasks share site/session).

## 3. Sampling policy and holdout

**Registry construction (frozen, no outcome leakage):**
- Synthetic orthogonal alias-OOD: 30 tasks = 3 families ×10 intents.
  - Families: (a) header-based (`ApiKey: ${token}` vs `X-Reset-Token: ${token}` vs `X-Api-Key: ${token}` vs `Authorization: Bearer ${token}`), (b) body JSON field (`{"apiKey":"${token}"}` vs `{"key":"${token}"}` vs `{"api_key":"${token}"}` vs `{"token":"${token}"}`), (c) auth permission (`scope=read` vs `admin_scope=${perm}` vs `X-Scope: ${perm}`).
  - Per task: registry has 1 training mechanism (one alias form at 0.9), 1 distractor alias form at 0.9, 1 low-confidence distractor at 0.8. Test query uses held-out alias form with **same semantic intent string** as training (so exact matcher would succeed if it ignored template aliasing). Train template never equals test template.
  - Within each family, 7 tasks standard variations covered by documentation examples, 3 held-out variations (e.g., novel header `X-Api-Key`, body field `api_token`, permission `X-Scope`) requiring structural generalization beyond table lookup. Report overall 30 plus held-out-9 subset.
- Live BrowserGym alias-OOD: Attempt 20 WebShop +20 ALFWorld sampled offline via BrowserGym 0.14.3 at 1280x720 with CDP AX tree. Map to same mechanism abstraction (intent = natural language goal / observation summary, template = action with slots manifested as header/body/URL aliasing in real request). Registry built from training trajectories (distinct intent strings), test tasks are held-out goal variations where alias manifests in observed AX/DOM headers/body/URL. No test live template verbatim in registry. If offline unavailable or truncation >50%, mark exploratory and bound confirmatory claim to synthetic orthogonal only.
- Exact-match: 12 tasks where test `intent` equals registry intent verbatim, same slot names, preconditions match — no aliasing required (header/body/auth exact).
- No-applicable: 12 tasks where test intent OOD with no covering mechanism (registry has other intents; correct answer UNKNOWN).
- Empty-registry: 6 tasks with empty registry → UNKNOWN 100%.
- Total synthetic: 60 tasks per method ×7 methods = 420 calls. Live adds up to 40×7=280 calls if available.

**Holdout integrity:**
- Alias families stratified; train/test alias forms disjoint. No test template verbatim in registry (0/30 synthetic leakage check; same for live if available).
- TF-IDF / embedding fit on train registry strings (intent+template) only; test templates not in fit.
- Genuine rule set derived from training alias documentation only; held-out alias forms require structural inference (e.g., count header/body keys, segments) not direct map.
- Derived context filtered to exclude forbidden keys via harness `derive_state(observed_url, headers_observed, body_observed, ax_tree)` that outputs only allowed fields.
- Seeds deterministic (`np.random.RandomState(42)`, `random.seed(42)`; LEARNED uses 42,43,44 for stability), no unseeded calls.
- Live tasks split by site (WebShop vs ALFWorld) with no site identity leakage into retriever; retriever fit on train registry only.

**Holdout unit:** Task-level; preprocessing fit on TRAIN only; site/task identity does not leak (synthetic intent strings or BrowserGym goal strings synthetic per task, not dataset IDs).

## 4. Baselines, positive/null controls, validity gate

**Baselines (strong, per AGENTS.md):**
- B-EXACT-MATCH — ID `B-EXACT-MATCH`
- B-VERBATIM-REPLAY — ID `B-VERBATIM-REPLAY`
- B-RAG-TFIDF — ID `B-RAG-TFIDF`
- B-RAG-EMBED — ID `B-RAG-EMBED`
- B-RANDOM — ID `B-RANDOM`
- RECONSTRUCTION-RULE (genuine rule-based) — ID `RECONSTRUCTION-RULE`
- RECONSTRUCTION-LEARNED (GRPO/System-One) — ID `RECONSTRUCTION-LEARNED`
Details in spec.json:baselines. All baselines respect forbidden-key prohibition; confidence for baselines is retriever score or kernel confidence, not hardcoded.

**Positive controls (must pass for confirmatory):**
- PC-EXACT-MATCH (ID `PC-EXACT-MATCH`): On exact-match (12), B-EXACT-MATCH and RECONSTRUCTION-RULE must achieve `correct >=0.90` and `false_accept <=0.10`. Failure → MEASUREMENT_INVALID.
- PC-BROWSERGYM-HEALTH (ID `PC-BROWSERGYM-HEALTH`): At least 80% of attempted live BrowserGym tasks load DOM/AX at 1280x720 without truncation/timeout (AX nodes>10). If <80%, live stratum is exploratory, claim bounds to synthetic orthogonal only (not MEASUREMENT_INVALID).

**Null controls (must pass):**
- NC-NO-APPLICABLE (ID `NC-NO-APPLICABLE`): On no-applicable (12), all methods UNKNOWN with `precision >=0.90` and `false_accept <=0.10`.
- NC-EMPTY-REGISTRY (ID `NC-EMPTY-REGISTRY`): Empty registry (6) → UNKNOWN 100%.
- Failure → MEASUREMENT_INVALID.

**Validity threats and mitigations:**
- *Oracle leak (parent failure):* Prior synthetic oracle read `alias_family/query_key` etc. Mitigation: harness filters context to derived fields only; reconstruct signature `reconstruct(intent, derived_state, candidates, params)` with no hidden_expected; audit inspects code for forbidden key reads and constant confidence → MEASUREMENT_INVALID.
- *Hardcoded confidence → fake ECE:* Confidence must be softmax over candidate scores or model-derived (critic), vary across tasks (std>0.05); audit checks ECE uses derived confidence not constants; report distribution.
- *Representation loss:* Synthetic orthogonal lacks AX heterogeneity; live BrowserGym adds it. Do not claim broader resolution beyond tested header/body/auth + WebShop/ALFWorld.
- *Retrieval confounding:* RAG baselines isolate retrieval vs reconstruction; require reconstruction not >0.10 below best RAG.
- *Calibration misreporting:* Report ECE over 5 bins with Wilson/bootstrap CI; bimodal confidence disclosed.
- *Vacuous isolation:* Ensure full>body and full>status non-vacuous where applicable for synthetic header/body tasks; trajectory-grouped permutation for live.
- *Training leakage for LEARNED:* LEARNED sees only train split; held-out and live held out; audit training logs.
- *BrowserGym flakiness:* PC-BROWSERGYM-HEALTH gates; infrastructure failure not counted as falsification.

## 5. Primary metric, expected direction, uncertainty

**Primary metric:** `correct_resolution_rate_alias_OOD` = #correct / N for RECONSTRUCTION-RULE on synthetic orthogonal alias-OOD (N=30) and separately on live BrowserGym alias-OOD if N_live>=20. Held-out-9 subset diagnostic.

**Expected direction:** RECONSTRUCTION-RULE > exact matcher (0.0 expected) and > verbatim. Target `>=0.50` absolute, with `false_accept <=0.15` and `>=0.15` below verbatim. LEARNED within 0.10 of RULE.

**Secondary gated metrics:** `false_accept_rate_alias_OOD`, `correct_resolution_exact_match`, `unknown_precision_no_applicable`, `ECE` (5 bins, derived confidence), per-family rates, training cost/stability (wall-clock, tokens/calls, variance across 3 seeds), verification economics (retrieval+reconstruction+verification steps/cost).

**Uncertainty:**
- Wilson 95% CI for rates.
- One-sided binomial RECONSTRUCTION vs 0.10 chance null (p<0.05).
- Paired McNemar RECONSTRUCTION-RULE vs B-EXACT-MATCH (correct) and vs B-VERBATIM-REPLAY (false_accept) on alias-OOD (p<0.05).
- Block bootstrap 2000 resamples (trajectory-grouped for live) for ECE CI and RAG comparison.
- Live BrowserGym same tests with Wilson CIs.

## 6. Adequacy rule

Sample adequate if synthetic orthogonal alias-OOD N>=30 reached, exact-match N>=12, no-applicable N>=12 plus empty 6, PC and NC evaluated, no stratum >20% missing due to harness errors, audit finds no oracle leak, and LEARNED training logs available or disclosed unavailable. If live BrowserGym proxy unavailable or PC-BROWSERGYM-HEALTH fails (<80% healthy), adequacy still met for synthetic orthogonal confirmatory stratum (disclosed as bounded) provided primary N thresholds met; do not claim live generalization. If synthetic alias-OOD N<24 or PC/NC fail, MEASUREMENT_INVALID.

## 7. Falsification / survival rule (frozen decision rule, see spec.json:decision_rule)

**SURVIVES_CURRENT_TEST iff ALL (synthetic orthogonal primary):**
1. PC-EXACT-MATCH passes (correct >=0.90 for B-EXACT-MATCH and RECONSTRUCTION-RULE on exact-match; false_accept <=0.10).
2. NC-NO-APPLICABLE passes (UNKNOWN precision >=0.90, false_accept <=0.10) AND NC-EMPTY 100% UNKNOWN.
3. Alias-OOD S1: RECONSTRUCTION-RULE correct >=0.50 AND binomial p<0.05 vs 0.10 null AND McNemar p<0.05 vs B-EXACT-MATCH.
4. S2: RECONSTRUCTION-RULE false_accept <=0.15 AND strictly below B-VERBATIM-REPLAY by >=0.15 absolute with McNemar p<0.05 on false_accept.
5. S3: RECONSTRUCTION-RULE exact-match correct >=0.90 (no regression); if LEARNED available also >=0.85.
6. S4: RECONSTRUCTION-RULE no-applicable precision >=0.85 AND ECE <=0.15 (5 bins, derived confidence).
7. Not dominated by retrieval: RECONSTRUCTION-RULE correct not >0.10 below best RAG verbatim correct.

**Live BrowserGym exploratory confirmation (if N_live>=20 and PC-BROWSERGYM-HEALTH passes):** Report same S1-S2 on live; synthesis SURVIVES requires synthetic gates plus live correct >=0.50 (binomial p<0.05 vs 0.10) and false_accept <=0.15. If live fails but synthetic passes, overall SURVIVES bounded to synthetic orthogonal with disclosure.

**LEARNED non-inferiority (exploratory):** Report LEARNED correct within 0.10 of RULE and ECE within 0.05; if LEARNED underperforms by >0.15 or ECE exceeds by >0.10 or CV>0.5, LEARNED falsified but RULE may still SURVIVE.

**FALSIFIED-IN-SETTING if controls pass but S1 fails (correct <0.40 or not above exact) OR S2 fails (false_accept >0.25 or not below verbatim) OR S3 fails OR S4 fails.** Bounded to genuine adapter class and orthogonal alias families incl held-out and live when measured. LEARNED falsification does not alone falsify RULE.

**MEASUREMENT_INVALID if PC or NC fails, or audit detects oracle leak (forbidden key access or hardcoded confidence) or constant confidence, or synthetic alias-OOD N<24, or >20% harness errors, or intent-equality registry leakage, or systematic BrowserGym load failure is not re-labeled as falsification but as exploratory bound.**

All thresholds absolute rates on frozen strata — no post-hoc tuning. Changed analysis after seeing outcomes is exploratory; new claim requires new preregistration.

## 8. Product and claim consequences

- **If SURVIVES (synthetic orthogonal + live BrowserGym with calibration):** C-SEMANTIC-RESOLVE advances to EXPERIMENTAL (bounded to genuine reconstruction on orthogonal header/body/auth and live WebShop/ALFWorld at BrowserGym 1280x720 with calibrated UNKNOWN, both rule and if learned matches). Product should add reconstruction+calibrated abstention layer after retrieval and before execution (critique-reconstruct conditioned on intent+observation-derived state from DOM/AX at 1280x720+retrieved template, confidence-gated UNKNOWN<0.80), with verification/repair boundary and freshness guard. Unblocks cross-site parameterized transfer where header/body/auth aliasing common, addresses MemHarness negative-transfer prior, and justifies sequencing to workflow-compilation (Artic/FlowSearcher). Not PRODUCT_CORE until learned GRPO stability and end-to-end economics replicate at scale. Report economics: retrieval+reconstruction+verification cost per successful task vs RAG vs verbatim; training cost/stability vs rule proxy.
- **If FALSIFIED:** Do not add reconstruction layer for these families/live; keep exact-intent matching, require pre-normalized intents or explicit alias catalogs/server-side normalization/per-site header/body mapping. Frontier pivot to orthogonal basin (artifact-driven workflow compilation, hierarchical DAG synthesis, program-synthesis repair, cache invalidation). C-SEMANTIC-RESOLVE remains HYPOTHESIS (bounded falsification for tested genuine adapter on tested orthogonal families/live, not global). Learned GRPO failure indicates training instability or synthetic-to-real gap, not blanket rejection of critique-reconstruct class.
- **If MEASUREMENT_INVALID:** No claim update; fix harness (remove leak, derive confidence, restore controls, repair BrowserGym fixture loading) and re-run. Parent's MEASUREMENT_INVALID does not support or falsify claim; PC-BROWSERGYM-HEALTH failure bounds claim to synthetic only.

## 9. Cost and information gain

**Estimated cost:** Low-moderate — 60 synthetic + up to 40 live =100 tasks ×7 methods =700 deterministic resolve calls + offline retrieval (<15 min CPU no LLM for RULE). LEARNED GRPO training adds 1-3h wall-clock if using local small LM or hosted LLM ~200k-500k tokens with 3 seeds; report wall-clock/tokens. Live BrowserGym at 1280x720 adds <40 Playwright navigations with CDP AX extraction (<30 min if fixtures local). Total compute <4h single runner, no large datasets committed. Offline embedding local CPU. If LLM unavailable, LEARNED disclosed unavailable and cost <30 min.

**Expected information gain:** Very high — first valid test of learned (GRPO/System-One) vs rule-based genuine reconstruction and first orthogonal-family (header ApiKey/X-Reset-Token, body JSON field, auth permission) plus live-browser WebShop/ALFWorld validation at BrowserGym 1280x720 with real CDP AX trees — directly addresses Director's REOPEN mandate (REOPEN C-SEMANTIC-RESOLVE after synthetic tunneling closed, rationale leverages BrowserGym 0.14.3 unified traces) and parent handoff's two dominant unknowns (learnability/training cost/stability and synthetic-to-real gap). Either outcome changes product/architecture decision: positive validates retrieval+reconstruction vs exact matcher for broader aliasing and unblocks cross-site transfer sequencing with calibrated abstention and measured economics; negative falsifies adaptation prior for orthogonal families/live and cleanly parks semantic claim forcing pivot to compilation/synthesis. Strong baselines (exact, verbatim, TFIDF, embed, random) and PC/NC with calibration gates (UNKNOWN precision, ECE) plus header/body/auth non-vacuous isolation and trajectory-grouped permutation ensure non-retrieval explanation. Orthogonal to 30+ prior freshness/PMI/TV loops and to narrow URL-only POC (30/30 synthetic), satisfying frontier charter to leave solution basin. Reports training cost/stability and verification-boundary economics vs rule proxy and RAG for product decision; covers agent priors (path dependence, verification discrimination, work compression, strong baselines, body/status conflation) distinguished from SPIDER evidence.

## 10. Provenance and artifacts

Code roots: `research/frontier/` and `research/harness/` only (per `research/lanes/registry.json:frontier`). Artifacts: `run_experiment.py` (genuine reconstruct_resolve RULE and LEARNED harness, GRPO training script if used), `tasks.json` (synthetic orthogonal and live BrowserGym fixtures with hidden_expected separated), `raw_evidence.json` (per-task outcomes per method incl live), `derived_metrics.json` (rates, Wilson CIs, McNemar, binomial, ECE incl bootstrap, per-family/held-out/live breakdown, training cost/stability, economics), `provenance.json` (commit, seeds, BrowserGym version 0.14.3, viewport 1280x720, CDP AX extraction hash, dataset hashes). No `src/` edits. No outcome-bearing measurements during DESIGN. Audit must be able to inspect forbidden-key filtering, confidence derivation, GRPO training logs, and BrowserGym fixture loading.

## 11. Inheritance and disposition

Parent handoff `EXP-FRONTIER-35752577234` is USE per `request.json:director_mandate.parent_handoff_disposition=USE`. Its established narrow ceiling (0/30 alias vs 30/30 genuine, PC 12/12, NC 12/12+6/6, ECE 0.0738), baselines, controls, and rejected bounded exact-matcher are preserved; its unknown and do_not_assume are binding (especially oracle 1.0, hardcoded ECE, per-family uniformity, synthetic-to-real gap, GRPO learnability, cross-site transfer not unblocked). Director mandate REOPEN to C-SEMANTIC-RESOLVE with `cognitive_reset=false` supersedes any residual local continuation; per AGENTS.md precedence, `director_mandate` is binding and `parent_handoff.next_question` is advisory continuity only — here they align (both ask learned + live BrowserGym + orthogonal families). This experiment implements the mandated genuine non-oracle repair expanded to orthogonal header/body/auth families at BrowserGym 1280x720 with real AX trees plus learned System-One/GRPO comparison with cost/economics, satisfying charter to leave TV divergence basin. The five agent priors listed in `request.json:director_mandate.agent_priors_used` are used as priors (path dependence, local optima verification, work compression, strong baselines, substrate conflation) distinguished from SPIDER evidence which has not shown LLM benefit vs retrieval, no valid repair cost, zero valid cost-vs-novelty curves, degenerate baselines, and vacuous C4.

## 12. Validity notes explicit

- Synthetic orthogonal aliasing is proxy for real WebShop/ALFWorld header/body/auth aliasing; synthetic-to-real gap remains dominant unknown — do not infer cross-site transfer without live BrowserGym replication at 1280x720 with real AX (exploratory strata disclosed, PC-BROWSERGYM-HEALTH gates).
- Genuine rule-based adapter is proxy for learned GRPO critique-reconstruct — positive result for RULE is proof-of-concept for structural adaptation benefit, not evidence GRPO training succeeds or calibrates; LEARNED arm directly tests this with cost/stability reporting and 3-seed variance.
- Confidence threshold 0.80 for UNKNOWN is kernel `min_confidence`; calibration assessed via ECE on derived/model scores over 5 bins with bootstrap CI, not assumed; hardcoded constants trigger MEASUREMENT_INVALID.
- BrowserGym 0.14.3 traces are offline fixtures; if live Playwright at 1280x720 fails systematically, do not re-label as falsification — bound to synthetic orthogonal.
- Header-based ApiKey/X-Reset-Token, body JSON field, and auth permission families are orthogonal to prior query-param/path-rewriting/server-routing — they test header/body non-vacuous isolation (full>body>status) and trajectory-grouped permutation; prior U(1.0) does not guarantee orthogonal family success.
- All 235+ prior experiments' tunneling diagnostics motivate this orthogonal design — do not repeat freshness/PMI/TV loops; this is Director-mandated exit from W-DYNAMICS TV basin per portfolio assessment.
- No `src/spider/kernel.py` edits in this frontier experiment; verification boundary is measured but not yet productized.
