# EXP-FRONTIER-35752577234 preregistration — Frontier C-SEMANTIC-RESOLVE: genuine non-oracle reconstruction vs verbatim

**Lane:** frontier — Charter: search outside current solution basin for high-upside falsifiable mechanisms that could radically reduce agent exploration or change SPIDER architecture.
**Claim:** C-SEMANTIC-RESOLVE (Goals can be resolved to applicable mechanisms without internal ids) — Status HYPOTHESIS per registry; MIXED narrow ceiling per prior (SpiderKernel.resolve L97 `m.intent != intent`, L112 confidence sort fails 0/6 complex alias families query-param/path-rewriting/server-routing p=0.016 at confidence 0.9 and 0/12 status grounding, plus 0/10 simple aliasing; see handoff EXP-FRONTIER-35741928625).
**Director mandate:** PIVOT to C-SEMANTIC-RESOLVE, `cognitive_reset=true`, `parent_handoff_disposition=USE`. Binding question verbatim in `request.json:director_mandate.question` — tested here as genuine (non-oracle) state-conditioned reconstruction adapter vs verbatim replay with calibrated abstention. Continuity evidence from parent handoff preserved per AGENTS.md.
**Experiment ID:** EXP-FRONTIER-35752577234 — **Freeze required before any outcome inspection.**

## 1. Question and hypothesis

**Operational question:** Does a genuine (non-oracle) state-conditioned reconstruction adapter that critiques/reconstructs the retrieved template via structural analysis of `(intent, observation-derived state, retrieved_template)` — without access to ground-truth `alias_family/query_key/target_prefix` signals and without hardcoded confidence — achieve alias-OOD `correct_resolution >=0.50` (binomial p<0.05 vs 0.10, McNemar p<0.05 vs exact matcher) and `false_accept <=0.15` (>=0.15 below verbatim, p<0.05) while preserving `exact-match >=0.90` and `no-applicable UNKNOWN precision >=0.85` with `ECE <=0.15`, tested on the same three alias families (query-param, path-rewriting, server-routing) plus held-out variations and a limited live-browser WebShop/ALFWorld proxy where available?

**Hypothesis (directional):** Yes — a lightweight genuine reconstruction adapter that parses `intent` verb+resource, scores each candidate mechanism's template structurally against the **observation-derived** state (slot count, path segments, query-key presence, prefix structure derived only from observed `url/method`), selects or rewrites the best template then `_bind`, with confidence derived from normalized structural match score (not hardcoded) and calibrated UNKNOWN gate `confidence<0.80`, will achieve substantially higher `correct_resolution` and lower `false_accept` on alias-OOD (incl held-out) than exact matching and verbatim replay, while preserving `>=0.90` on exact-match and maintaining calibrated abstention (`precision >=0.85`, `ECE <=0.15`) when no applicable mechanism exists.

**Null hypothesis:** Genuine reconstruction does not improve over exact matching/verbatim, or does so only by inflating false accepts / miscalibration — alias-OOD `correct <0.40` or not significantly above exact matcher (0/30 expected), or `false_accept >0.25` or not `>=0.15` below verbatim, or exact-match regression, or abstention miscalibration.

**Inherited state (from parent handoff EXP-FRONTIER-35741928625 — USE disposition):**
- Established: `C-SEMANTIC-RESOLVE` narrow ceiling EXPERIMENTAL for deterministic exact matcher (0/16 combined alias failures, 0/12 status grounding, baseline descriptive B-EXACT 0/30 alias-OOD, B-VERBATIM 0/30, RAG-TFIDF 0/30; PC 12/12 and NC 12/12+6/6 on exact/no-applicable — see carry_forward.established).
- Rejected: Bounded rejection of deterministic exact-template matching with equal confidence; **no** bounded rejection of reconstruction/adaptation class (parent oracle 1.0 result was MEASUREMENT_INVALID, not valid evidence).
- Unknown: Whether genuine structural reconstruction without ground-truth signals can meet gates on these families + held-out; learnability via GRPO/LLM System-One; generalization to WebShop/ALFWorld/real Web; embedding retriever effect; economics.
- Do-not-assume (binding): Do not assume parent's 30/30 (1.0) or ECE 0.055 demonstrates adaptation — it was hardcoded oracle reading `alias_family/query_key/target_prefix` and ignoring retrieved template (audit required_fixes run_experiment.py:379-434). Do not assume per-family 10/10 heterogeneity or calibration. Do not assume synthetic proxies real aliasing. Do not assume rule-based proxy validates GRPO learnability. Do not infer cross-site transfer without WebShop/ALFWorld replication. Do not treat MEASUREMENT_INVALID as FALSIFIED.

This design repairs the validity threat: forbidden signals and hardcoded confidence are prohibited and audited.

## 2. State, action, target, unit of analysis

**State representation (raw → derived):**
- Raw: `context` derived from observation: `url` string as observed in browser address bar, `method` (GET). Derived: `url_path` (split `/`), `url_query` dict (parse `?k=v`), `url_segments` list, and `intent` string. **Losses disclosed:** visual layout, auth/session headers, timing, DOM — none used for aliasing; if they matter for broader semantic resolution, effect is bounded to tested URL template aliasing. **Forbidden:** `alias_family`, `query_key`, `target_prefix`, `routing_prefix`, `target_style`, `path_style`, `resource` answer labels are NOT in derived context; they exist only as hidden `expected` metadata for scoring, not passed to methods. Audit will verify no read of forbidden keys and no constant confidence.

**Action representation:**
- Mechanism `action_template` is URL template string with `${slot}` (e.g., `/users/${id}`, `/accounts/${id}?user=${id}`, `/api/v2/users/${id}`). Binding via deterministic `kernel._bind`. Genuine reconstruction may (a) score each candidate template's structural match to derived state (count `${}` slots, match segments, detect query presence) and select best, and/or (b) rewrite template structure before `_bind` (path↔query-param, prefix normalization) conditioned **only** on `(intent, derived_state, retrieved_template/candidates)`. No hidden_expected access.

**Target (primary measurand):**
- Per-task outcome in `{correct_resolution, false_accept, UNKNOWN}` (mutually exclusive, sum to 1 per stratum).
  - `correct_resolution` = adapter selects (or rewrites to) alias-correct template and `bound_action` equals `expected_bound` (hidden_expected_template bound with params).
  - `false_accept` = selects wrong template or binds incorrectly when should abstain/select correct; includes resolving when should UNKNOWN.
  - `UNKNOWN` = correctly abstains when no applicable mechanism (no-applicable/empty) or calibrated gate `confidence<0.80`.
- Secondary: calibration — `ECE` over 5 confidence bins (confidence derived from structural score), abstention precision/recall; per-family and held-out-3 subset breakdown.

**Unit of analysis:** Single `resolve+bind(+optional genuine rewrite)` call per task. Paired design: each task evaluated under each method (within-task). Resampling unit is task (block bootstrap over tasks, not transitions).

## 3. Sampling policy and holdout

**Registry construction (frozen, no outcome leakage):**
- Alias-OOD stratum: 30 tasks = 3 families ×10 intents.
  - Families: (a) query-param (`/users/${id}` vs `/users?user=${id}`), (b) path-rewriting (`/users/${id}` vs `/accounts/${id}` vs `/api/v2/users/${id}`), (c) server-routing (`/posts/${postId}` vs `/api/posts/${postId}` vs `/p/${postId}`). Per task: registry has 1 training mechanism (one alias form at 0.9), 1 distractor alias form at 0.9, 1 low-confidence distractor at 0.8. Test query uses held-out alias form with **same semantic intent string** as training (so exact matcher would succeed if it ignored template). Train template never equals test template.
  - Within each family, 7 tasks are standard variations covered by documentation examples, 3 are held-out variations (e.g., novel prefix `/api/users`, `/v2/accounts/${id}`, `/post/${postId}`) requiring structural generalization beyond table lookup. Report overall 30 plus held-out-9 subset.
- Exact-match stratum: 12 tasks where test `intent` equals registry intent verbatim, same slot names, preconditions match — no aliasing required.
- No-applicable stratum: 12 tasks where test intent is OOD with no covering mechanism (registry has other intents; correct answer UNKNOWN).
- Empty-registry: 6 tasks with empty registry → UNKNOWN 100%.
- Total 60 tasks per method ×6 methods = 360 calls.

**Holdout integrity:**
- Alias families stratified; train/test alias forms disjoint. No test template verbatim in registry (0/30 leakage check).
- TF-IDF / embedding fit on train registry strings (intent+template) only; test templates not in fit.
- Genuine rule set derived from training documentation only; held-out alias forms require structural inference (e.g., count segments/query keys) not direct map.
- Derived context filtered to exclude forbidden keys via harness function `derive_state(observed_url)` that outputs only `url, method, url_path, url_query, url_segments`.
- Seeds deterministic (`np.random.RandomState(42)`, `random.seed(42)`), no unseeded calls.

**WebShop/ALFWorld OOD proxy (exploratory, not confirmatory if unavailable):**
- Attempt to sample 20 WebShop trajectories (product search intents) and 20 ALFWorld (pick/place) offline via harness if datasets accessible. Map to same mechanism abstraction (intent = natural language goal, template = action with slots). Use derived state from observation (accessibility tree text or URL if available). Same metric definitions. If offline unavailable or truncation >50%, mark exploratory and bound confirmatory claim to synthetic aliasing only — do not claim cross-dataset generalization.

**Holdout unit:** Task-level; preprocessing fit on TRAIN only; site/task identity does not leak (intent strings synthetic, not dataset IDs).

## 4. Baselines, positive/null controls, validity gate

**Baselines (strong, per AGENTS.md):**
- B-EXACT-MATCH: `SpiderKernel.resolve` L97 exact intent equality, confidence sort. ID `B-EXACT-MATCH`.
- B-VERBATIM-REPLAY: top-1 by exact intent match in registry order, verbatim `_bind` without rewrite. ID `B-VERBATIM-REPLAY`.
- B-RAG-TFIDF: TF-IDF over intent+template, top-1 then verbatim. ID `B-RAG-TFIDF`.
- B-RAG-EMBED: embedding cosine all-MiniLM-L6-v2 offline deterministic, top-1 then verbatim; if unavailable mark unavailable and use TF-IDF as strong with disclosure. ID `B-RAG-EMBED`.
- B-RANDOM: uniform random among eligible intent-matching candidates else UNKNOWN. ID `B-RANDOM`.
- RECONSTRUCTION (genuine): structural analysis scorer+rewriter + calibrated gate. ID `RECONSTRUCTION`.

All baselines respect forbidden-key prohibition; confidence for baselines is retriever score or kernel confidence, not hardcoded.

**Positive control (must pass):**
- PC-EXACT-MATCH (ID `PC-EXACT-MATCH`): On exact-match stratum (12), B-EXACT-MATCH and RECONSTRUCTION must achieve `correct >=0.90` and `false_accept <=0.10`. Failure → MEASUREMENT_INVALID.

**Null controls (must pass):**
- NC-NO-APPLICABLE (ID `NC-NO-APPLICABLE`): On no-applicable (12), all methods must return UNKNOWN with `precision >=0.90` and `false_accept <=0.10`.
- NC-EMPTY-REGISTRY (ID `NC-EMPTY-REGISTRY`): Empty registry (6) → UNKNOWN 100%.
- Failure → MEASUREMENT_INVALID (hallucination/miscalibration).

**Validity threats and mitigations:**
- *Oracle leak (parent failure):* Prior adapter read `alias_family/query_key/target_prefix` and hardcoded 0.95. Mitigation: harness filters context to derived fields only; reconstruct function signature `reconstruct(intent, derived_state, candidates, params)` with no access to hidden_expected; audit inspects code for forbidden key reads and for constant confidence return; detection → MEASUREMENT_INVALID.
- *Hardcoded confidence → fake ECE:* Mitigation: confidence must be computed from structural scores (e.g., normalized softmax or score/max_score) and vary across tasks; audit checks ECE computation uses derived confidence not constants; report confidence distribution.
- *Representation loss:* No DOM/auth — bounded to URL template aliasing. Do not claim broader resolution beyond tested families.
- *Retrieval strength confounding:* RAG baselines isolate retrieval vs reconstruction; claim requires reconstruction not dominated by retrieval (>0.10 below best RAG).
- *Calibration misreporting:* Report ECE over 5 bins with Wilson CIs and bootstrap CI; do not report accuracy alone.

## 5. Primary metric, expected direction, uncertainty

**Primary metric:** `correct_resolution_rate_alias_OOD` = #correct / 30 for RECONSTRUCTION on alias-OOD (overall, plus held-out-9 subset diagnostic).

**Expected direction:** RECONSTRUCTION > exact matcher (0.0 expected) and > verbatim. Target `>=0.50` absolute, with `false_accept <=0.15` and `>=0.15` below verbatim.

**Secondary gated metrics:** `false_accept_rate_alias_OOD`, `correct_resolution_exact_match`, `unknown_precision_no_applicable`, `ECE` (5 bins, derived confidence).

**Uncertainty:**
- Wilson 95% CI for rates.
- One-sided binomial RECONSTRUCTION vs 0.10 chance null (p<0.05).
- Paired McNemar RECONSTRUCTION vs B-EXACT-MATCH (correct) and vs B-VERBATIM-REPLAY (false_accept) on alias-OOD (p<0.05).
- Block bootstrap 2000 resamples over tasks for ECE CI and for any RAG comparison.

## 6. Adequacy rule

Sample adequate if alias-OOD N>=30 reached, exact-match N>=12, no-applicable N>=12 plus empty 6, PC and NC evaluated, no stratum >20% missing due to harness errors, and audit finds no oracle leak. If WebShop/ALFWorld proxy unavailable, adequacy still met for synthetic aliasing confirmatory stratum (disclosed as bounded) provided primary N thresholds met; do not claim cross-site generalization. If alias-OOD N<24 or PC/NC fail, MEASUREMENT_INVALID.

## 7. Falsification / survival rule (frozen decision rule, see spec.json:decision_rule)

**SURVIVES_CURRENT_TEST iff ALL:**
1. PC-EXACT-MATCH passes (correct >=0.90 for B-EXACT-MATCH and RECONSTRUCTION on exact-match; false_accept <=0.10).
2. NC-NO-APPLICABLE passes (UNKNOWN precision >=0.90, false_accept <=0.10) AND NC-EMPTY 100% UNKNOWN.
3. Alias-OOD S1: RECONSTRUCTION correct >=0.50 AND binomial p<0.05 vs 0.10 null AND McNemar p<0.05 vs B-EXACT-MATCH.
4. S2: RECONSTRUCTION false_accept <=0.15 AND strictly below B-VERBATIM-REPLAY by >=0.15 absolute with McNemar p<0.05 on false_accept.
5. S3: RECONSTRUCTION exact-match correct >=0.90 (no regression).
6. S4: RECONSTRUCTION no-applicable precision >=0.85 AND ECE <=0.15 (5 bins, derived confidence).
7. Not dominated by retrieval: RECONSTRUCTION correct not >0.10 below best RAG (TFIDF/embed) verbatim correct.

**FALSIFIED-IN-SETTING if controls pass but S1 fails (correct <0.40 or not above exact) OR S2 fails (false_accept >0.25 or not below verbatim) OR S3 fails OR S4 fails.** Bounded to genuine adapter class and alias families incl held-out variations.

**MEASUREMENT_INVALID if PC or NC fails, or audit detects oracle leak (forbidden key access or hardcoded confidence), or alias-OOD N<24, or >20% harness errors, or intent-equality registry leakage.**

All thresholds absolute rates on frozen strata — no post-hoc tuning. Changed analysis after seeing outcomes is exploratory; new claim requires new preregistration.

## 8. Product and claim consequences

- **If SURVIVES:** C-SEMANTIC-RESOLVE advances to EXPERIMENTAL (bounded to genuine rule-based critique-reconstruct on tested alias families incl held-out with calibrated UNKNOWN). Product should add reconstruction+calibrated abstention layer after retrieval and before execution, with verification boundary. Frontier sequences to workflow compilation (Artic/FlowSearcher) after resolution solved. Not PRODUCT_CORE until LLM-GRPO/System-One and live-browser/WebShop replication validate learnability.
- **If FALSIFIED:** Do not add reconstruction layer; keep exact-intent matching, require pre-normalized intents or explicit alias catalogs. Frontier pivot to orthogonal basin (artifact-driven workflow compilation, hierarchical DAG synthesis, program-synthesis repair). C-SEMANTIC-RESOLVE remains HYPOTHESIS (bounded falsification for tested genuine adapter, not global).
- **If MEASUREMENT_INVALID:** No claim update; fix harness (remove leak, derive confidence, restore controls) and re-run. Parent's MEASUREMENT_INVALID does not support or falsify claim.

## 9. Cost and information gain

**Estimated cost:** Very low — 360 deterministic resolve calls + offline retrieval (<10 min CPU, no paid model calls for primary genuine adapter; optional live-browser proxy ~40 Playwright navigations <5 min). No large datasets committed. Offline embedding is local CPU only.

**Expected information gain:** High — first *valid* Frontier test of Director's orthogonal reconstruction-vs-verbatim mechanism, repairing prior oracle failure (30/30, ECE 0.055) that left calibrated applicability untested. Directly addresses MIXED ceiling and stale-intent false_accept risk (long-horizon path dependence prior). Either outcome changes product/architecture decision and supersedes bundled residual-novelty contradiction. Orthogonal to 30+ prior freshness/PMI/TV loops (graph 9/10, frontier 13/15 tunnel) with strong baselines and calibration gates ensuring non-retrieval explanation.

## 10. Provenance and artifacts

Code roots: `research/frontier/` and `research/harness/` only (per `research/lanes/registry.json:frontier`). Artifacts: `run_experiment.py` (genuine reconstruct_resolve), `tasks.json` (with hidden_expected separated), `raw_evidence.json` (per-task outcomes per method), `derived_metrics.json` (rates, CIs, McNemar, ECE incl bootstrap), `provenance.json` (commit, seeds, dataset hashes). No `src/` edits. No outcome-bearing measurements during DESIGN. Audit must be able to inspect forbidden-key filtering and confidence derivation.

## 11. Inheritance and disposition

Parent handoff `EXP-FRONTIER-35741928625` is USE per `request.json:director_mandate.parent_handoff_disposition=USE`. Its established narrow ceiling (0/16 alias, 0/12 status), baselines, and controls are preserved; its rejected bounded exact-matcher is preserved; its unknown and do_not_assume are binding (especially oracle 1.0, hardcoded ECE, per-family uniformity, synthetic-to-real gap, GRPO learnability). Director mandate PIVOT to C-SEMANTIC-RESOLVE with cognitive reset supersedes any residual-novelty continuation; per AGENTS.md precedence, `director_mandate` overrides `parent_handoff.next_question` drift, but here they align. This experiment implements the mandated genuine non-oracle repair on the same three families plus held-out variations, satisfying charter to leave TV divergence basin.

## 12. Validity notes explícit

- Synthetic aliasing is proxy for real WebShop/ALFWorld aliasing; synthetic-to-real gap remains dominant unknown — do not infer cross-site transfer without WebShop/ALFWorld replication (exploratory strata disclosed).
- Genuine rule-based adapter is proxy for learned GRPO critique-reconstruct — positive result is proof-of-concept for structural adaptation benefit, not evidence GRPO training succeeds.
- Confidence threshold 0.80 for UNKNOWN is kernel `min_confidence`; calibration assessed via ECE on derived scores, not assumed; hardcoded constants trigger MEASUREMENT_INVALID.
- All 230+ prior experiments' tunneling diagnostics motivate this orthogonal design — do not repeat freshness/PMI/TV loops; this is Director-mandated exit from W-DYNAMICS TV basin.

