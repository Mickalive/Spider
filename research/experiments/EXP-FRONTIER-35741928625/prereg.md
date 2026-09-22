# EXP-FRONTIER-35741928625 preregistration — Frontier C-SEMANTIC-RESOLVE: reconstruction vs verbatim applicability resolution

**Lane:** frontier — Charter: search outside current solution basin for high-upside falsifiable mechanisms that could radically reduce agent exploration or change SPIDER architecture.
**Claim:** C-SEMANTIC-RESOLVE (Goals can be resolved to applicable mechanisms without internal ids) — Status HYPOTHESIS per registry; MIXED per Director mandate (exact matcher fails 0/6 aliased templates p=0.016, confidence 0.9, and 0/12 HTTP status grounding).
**Director mandate:** PIVOT, SUPERSEDE parent handoff EXP-FRONTIER-35651943981 (bundled C-RESIDUAL-NOVELTY contradiction). Binding question verbatim in `request.json:director_mandate.question` — tested here as reconstruction/adaptation layer over retrieved mechanisms vs verbatim replay.
**Experiment ID:** EXP-FRONTIER-35741928625 — **Freeze required before any outcome inspection.**

## 1. Question and hypothesis

**Operational question:** Does a state-conditioned reconstruction/adaptation layer over retrieved mechanisms achieve applicability resolution beyond SPIDER's deterministic exact-intent matcher (`src/spider/kernel.py` L97 `m.intent != intent`, L112 `candidates.sort(key=confidence)`), which is bounded to fail 0/6 complex aliased templates (query-param / path-rewriting / server-routing, p=0.016) and 0/12 symmetric status grounding?

**Hypothesis (directional):** Yes — a MemHarness-style critique-reconstruct adapter (template critique + rewrite conditioned on current state/intent) or Jev-Mem System-One control-plane adapter (routing/budget/scoring with calibrated UNKNOWN abstention at confidence <0.8) will achieve substantially higher `correct_resolution` and lower `false_accept` on alias-OOD tasks than exact matching and verbatim replay, while preserving `>=0.90` on exact-match and maintaining calibrated abstention (`precision >=0.85`, `ECE <=0.15`) when no applicable mechanism exists.

**Null hypothesis:** Reconstruction does not improve over exact matching/verbatim, or does so only by inflating false accepts / miscalibration — i.e., alias-OOD `correct_resolution <0.40` or not significantly above exact matcher (0/30), or `false_accept >0.25` or not below verbatim, or exact-match regression, or abstention miscalibration.

## 2. State, action, target, unit of analysis

**State representation (raw → derived):**
- Raw: `context` dict with `url`, `method`, `query_params`, `path_style`, `routing_prefix`, plus intent string. Derived from observation state; no DOM/browser required. Losses disclosed: visual layout, auth/session headers, timing — none used for aliasing; if they matter, effect is bounded to tested alias families.

**Action representation:**
- Mechanism `action_template` is a URL template string containing `${slot}` parameters (e.g., `/users/${id}`, `/accounts/${id}?user=${id}`, `/api/v2/users/${id}`). Binding via deterministic `kernel._bind`. Reconstruction may rewrite template structure before binding (path ↔ query-param, prefix normalization) conditioned on `(intent, context, retrieved template)`.

**Target (primary measurand):**
- Per-task outcome in `{correct_resolution, false_accept, UNKNOWN}` (mutually exclusive, sums to 1 per stratum).
  - `correct_resolution` = adapter/kernel selects (or rewrites to) the alias-correct template and `bound_action` verifies against expected postcondition (or HTTP 200 where probed).
  - `false_accept` = selects wrong template or binds incorrectly when should abstain / select correct.
  - `UNKNOWN` = correctly abstains when no applicable mechanism (no-applicable stratum) or confidence-gated abstention.
- Secondary: calibration — `ECE` over 5 confidence bins, abstention precision/recall, and grounding: HTTP status 200 vs 4xx on 12 probes.

**Unit of analysis:** Single `resolve+bind(+optional rewrite)` call per task. Paired design: each task evaluated under each method (within-task comparison). Resampling unit is the task (block bootstrap over tasks, not transitions).

## 3. Sampling policy and holdout

**Registry construction (frozen, no outcome leakage):**
- Alias-OOD stratum: 30 tasks = 3 alias families × 10 intents.
  - Families: (a) query-param aliasing (`/users/${id}` vs `/users?user=${id}`), (b) path-rewriting (`/users/${id}` vs `/accounts/${id}` vs `/api/v2/users/${id}`), (c) server-routing (`/posts/${postId}` vs `/api/posts/${postId}` vs `/p/${postId}`).
  - Per task: registry contains 1 training mechanism (one alias form), 1 distractor alias form at equal confidence 0.9, 1 lower-confidence distractor at 0.8. Test query uses the held-out alias form with same semantic intent string as training (so exact matcher would succeed if it ignored template). Train template never appears as test template.
- Exact-match stratum: 12 tasks where test intent string equals registry intent verbatim, same slot names, preconditions match.
- No-applicable stratum: 12 tasks where test intent is out-of-distribution with no covering mechanism or preconditions mismatched; correct answer is UNKNOWN.
- Total 54 + 6 control probes (PC/NC) = 60 tasks per method.

**Holdout integrity:**
- Alias families are stratified; within-family, train/test alias forms are disjoint. No test template appears verbatim in registry.
- TF-IDF / embedding retrievers fit only on train registry strings (intent + template). Test templates not in fit.
- Reconstruction rule set derived from training documentation only; held-out alias variations (e.g., `/api/users` not in mapping table) require generalization.
- Seeds deterministic (`np.random.RandomState(42)`, `random.seed(42)`), no unseeded calls.

**WebShop/ALFWorld OOD proxy (exploratory, not confirmatory if unavailable):**
- Attempt to sample 20 WebShop trajectories (product search intents) and 20 ALFWorld (pick/place) offline via harness if datasets accessible. Same metric definitions. If offline unavailable or truncation >50%, mark exploratory and bound confirmatory claim to synthetic aliasing only — do not claim cross-dataset generalization.

**Holdout unit:** Task-level; preprocessing fit on TRAIN registry only; site/task identity does not leak (intent strings are synthetic, not dataset IDs).

## 4. Baselines, positive/null controls, validity gate

**Baselines (strong, per AGENTS.md):**
- B-EXACT-MATCH: current `SpiderKernel.resolve` (L97 exact intent equality, confidence sort).
- B-VERBATIM-REPLAY: retrieve top-1 by exact intent match, verbatim `_bind` without rewrite.
- B-RAG-TFIDF: TF-IDF retriever over intent+template, top-1 then verbatim.
- B-RAG-EMBED: embedding cosine retriever (all-MiniLM-L6-v2 or equivalent offline, deterministic), top-1 then verbatim. If model unavailable offline, document and use TF-IDF as strong baseline.
- B-RANDOM: uniform random over eligible mechanisms.

**Positive control (must pass for measurement to be valid):**
- PC-EXACT-MATCH: On exact-match stratum (12 tasks), B-EXACT-MATCH and reconstruction must achieve `correct_resolution >=0.90` and `false_accept <=0.10`. Failure → MEASUREMENT_INVALID (harness bug, not hypothesis).

**Null control (must pass):**
- NC-NO-APPLICABLE: On no-applicable stratum (12 tasks), all methods must return UNKNOWN with precision `>=0.90` and `false_accept <=0.10`.
- NC-EMPTY-REGISTRY: Empty registry → UNKNOWN 100%.
- Failure → MEASUREMENT_INVALID (hallucination/miscalibration).

**Measurement validity threats and mitigations:**
- *Intent-equality leak:* Test intent equals train intent for alias-OOD (to isolate template aliasing). Audit will verify reconstruction does not access test template verbatim except via context-derived signal. If leak detected → MEASUREMENT_INVALID.
- *Template simple vs complex aliasing:* Prior work tested simple path aliasing 0/10; this tests complex query-param/path-rewriting/server-routing (0/6 prior). Report separately per family to avoid aggregation masking heterogeneity.
- *Representation loss:* No DOM/auth/session — bounded to URL template aliasing. Do not claim broader semantic resolution beyond tested alias families.
- *LLM stochasticity:* Primary adapter is deterministic rule-based proxy for MemHarness critique-reconstruct (scoring + rewrite table). Optional LLM adapter, if tested, uses temperature 0 and seeded decoding; report variance across 3 seeds as exploratory.
- *Retrieval strength confounding:* RAG baselines isolate retrieval vs reconstruction. Claim requires reconstruction not dominated by retrieval alone (reconstruction correct not >0.10 below best RAG verbatim).
- *Calibration misreporting:* Report ECE over 5 bins with Wilson CIs; do not report accuracy alone.

## 5. Primary metric, expected direction, uncertainty

**Primary metric:** `correct_resolution_rate_alias_OOD` = #correct / 30 on alias-OOD stratum for reconstruction adapter.

**Expected direction:** Reconstruction > exact matcher (0.0) and > verbatim. Target `>=0.50` absolute, with `false_accept <=0.15`.

**Secondary gated metrics:** `false_accept_rate_alias_OOD`, `correct_resolution_exact_match`, `unknown_precision_no_applicable`, `ECE`.

**Uncertainty:**
- Wilson 95% CI for rates.
- One-sided binomial test of reconstruction vs 0.10 chance null (p<0.05).
- Paired McNemar test for reconstruction vs B-EXACT-MATCH and vs B-VERBATIM-REPLAY on alias-OOD (p<0.05).
- Block bootstrap (2000 resamples over tasks) for ECE CI.

## 6. Adequacy rule

Sample is adequate if: alias-OOD N>=30 reached, exact-match and no-applicable each N>=12 reached, PC and NC evaluated, and no stratum has >20% missing due to harness errors. If WebShop/ALFWorld proxy unavailable, adequacy still met for synthetic aliasing confirmatory stratum (disclosed as bounded).

## 7. Falsification / survival rule (frozen decision rule, see spec.json:decision_rule)

**SURVIVES_CURRENT_TEST iff ALL:**
1. PC-EXACT-MATCH passes (correct >=0.90 on exact-match for B-EXACT-MATCH and reconstruction).
2. NC-NO-APPLICABLE passes (UNKNOWN precision >=0.90, false_accept <=0.10).
3. Alias-OOD S1: reconstruction correct >=0.50 AND binomial p<0.05 vs 0.10 null AND McNemar p<0.05 vs B-EXACT-MATCH (expected 0 correct).
4. S2: reconstruction false_accept <=0.15 AND strictly below B-VERBATIM-REPLAY by >=0.15 absolute with McNemar p<0.05.
5. S3: reconstruction exact-match correct >=0.90 (no regression).
6. S4: reconstruction no-applicable precision >=0.85 AND ECE <=0.15.
7. Not dominated by retrieval: reconstruction correct not >0.10 below best RAG verbatim correct.

**FALSIFIED-IN-SETTING if controls pass but S1 fails (correct <0.40 or not above exact matcher) OR S2 fails (false_accept >0.25 or not below verbatim) OR S3 fails OR S4 fails.** Bounded to tested adapter class and alias families.

**MEASUREMENT_INVALID if PC or NC fails, or intent-equality leak detected, or alias-OOD N<24.**

All thresholds are absolute rates on frozen strata — no post-hoc tuning. A changed analysis after seeing outcomes is exploratory; new claim requires new preregistration.

## 8. Product and claim consequences

- **If SURVIVES:** C-SEMANTIC-RESOLVE advances to EXPERIMENTAL (bounded to rule-based critique-reconstruct on tested alias families with calibrated UNKNOWN). Product should add reconstruction+calibrated abstention after retrieval and before execution, with verification boundary. Frontier sequences to workflow compilation (Artic/FlowSearcher) after resolution solved. Not PRODUCT_CORE until LLM-GRPO and live-browser replication.
- **If FALSIFIED:** Do not add reconstruction layer; keep exact-intent matching, require pre-normalized intents or explicit alias catalogs. Frontier pivot to orthogonal basin (artifact-driven workflow compilation, hierarchical DAG synthesis, program-synthesis repair). C-SEMANTIC-RESOLVE remains HYPOTHESIS (bounded falsification for tested adapter, not global).
- **If MEASUREMENT_INVALID:** No claim update; fix harness/controls and re-run.

## 9. Cost and information gain

**Estimated cost:** Very low — 300 deterministic resolve calls + offline retrieval (<10 min CPU, no paid model calls for primary adapter; optional LLM adapter ~60 calls, <$5). No browser/network beyond 12 optional HTTP probes.

**Expected information gain:** High — first Frontier test of Director's orthogonal reconstruction-vs-verbatim mechanism, directly addressing MIXED C-SEMANTIC-RESOLVE ceiling and MemHarness negative-transfer prior, with strong baselines and positive/null controls to isolate reconstruction benefit from retrieval strength. Either outcome changes product/architecture decision and supersedes the bundled residual-novelty contradiction that blocked Frontier. Orthogonal to 30+ prior freshness/PMI/TV loops.

## 10. Provenance and artifacts

Code roots: `research/frontier/` and `research/harness/` only (per `research/lanes/registry.json:frontier allowed_code_roots`). Artifacts: `run_experiment.py`, `raw_evidence.json` (per-task outcomes per method), `derived_metrics.json` (rates, CIs, McNemar, ECE), `provenance.json` (commit, seeds, dataset hashes). No `src/` edits. No outcome-bearing measurements during DESIGN.

## 11. Inheritance and supersession

Parent handoff `EXP-FRONTIER-35651943981` is SUPERSEDED per `request.json:director_mandate.parent_handoff_disposition=SUPERSEDE`. Its established strong novelty gradient (rho -0.982) and rejected bundled rule are preserved as continuity evidence but do not authorize continuation of recalibrated residual-novelty tweaks. This experiment implements Director's PIVOT to C-SEMANTIC-RESOLVE with cognitive reset, satisfying `AGENTS.md` precedence: `director_mandate` overrides `parent_handoff.next_question`.

## 12. Validity notes explícit

- Synthetic aliasing is a proxy for real WebShop/ALFWorld aliasing; synthetic-to-real gap remains the dominant unknown — do not infer cross-site transfer without WebShop/ALFWorld replication.
- Rule-based adapter is a proxy for learned GRPO reconstruction — positive result is proof-of-concept for adaptation benefit, not evidence that GRPO training succeeds.
- Confidence threshold 0.8 for UNKNOWN is the kernel's `min_confidence`; calibration assessed via ECE, not assumed.
- All 224 prior experiments' tunneling diagnostics (Graph30/Runtime40/Physics42) motivate this orthogonal design — do not repeat freshness/PMI loops.
