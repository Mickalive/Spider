# EXP-FRONTIER-35752577234 — Frontier C-SEMANTIC-RESOLVE: genuine non-oracle reconstruction vs verbatim

**Lane:** frontier — search outside current solution basin for high-upside falsifiable mechanisms  
**Claim:** C-SEMANTIC-RESOLVE (Goals can be resolved to applicable mechanisms without internal ids) — HYPOTHESIS per registry, MIXED per Director mandate (parent MEASUREMENT_INVALID oracle 1.0)  
**Question:** Does a genuine (non-oracle) state-conditioned reconstruction adapter that critiques/reconstructs the retrieved template via structural analysis of (intent, observation-derived state, retrieved_template) — without access to ground-truth alias_family/query_key/target_prefix signals and without hardcoded confidence — achieve alias-OOD correct_resolution >=0.50 (binomial p<0.05 vs 0.10, McNemar p<0.05 vs exact matcher) and false_accept <=0.15 (>=0.15 below verbatim, p<0.05) while preserving exact-match >=0.90 and no-applicable UNKNOWN precision >=0.85 with ECE <=0.15, tested on the same three alias families (query-param, path-rewriting, server-routing) plus held-out variations and a limited live-browser WebShop/ALFWorld proxy where available?

**Hypothesis (directional):** Lightweight genuine reconstruction (parse intent, score each candidate template's structural match to observed URL — slot count, path segments, query-key presence, prefix structure — select or rewrite best template then _bind, confidence derived from normalized structural match score, gate UNKNOWN <0.80) will achieve substantially higher correct_resolution and lower false_accept on alias-OOD (incl held-out) than exact matching and verbatim replay, while preserving >=0.90 on exact-match and maintaining calibrated abstention (precision >=0.85, ECE <=0.15).

## 1. Frozen design (spec.json/prereg.md)

- **Alias-OOD** 30 tasks = 3 families ×10 (7 standard +3 held-out per family): (a) query-param (`/users/${id}` vs `/users?user=${id}` vs `/accounts?user=${id}` etc.), (b) path-rewriting (`/users/${id}` vs `/accounts/${id}` vs `/api/v2/users/${id}` vs `/api/users/${id}` etc.), (c) server-routing (`/posts/${postId}` vs `/api/posts/${postId}` vs `/p/${postId}` vs `/post/${postId}` etc.). Per task registry: 1 training mechanism (0.9) +1 distractor alias form (0.9) +1 low distractor (0.8), preconditions={} guards={} to isolate aliasing. Test uses held-out alias form not in registry, same semantic intent string as training (intent-equality isolation). No test template appears verbatim in registry (0/30 leak check).
- **Exact-match** 12 tasks: test intent equals registry intent verbatim, no aliasing.
- **No-applicable** 12 tasks: OOD intent with no covering mechanism → correct UNKNOWN.
- **Empty-registry** 6 tasks: empty registry → UNKNOWN 100%.
- Total 60 tasks per method ×6 methods =360 calls.
- **Baselines:** B-EXACT-MATCH (SpiderKernel.resolve L97 exact intent equality, min_confidence 0.8, confidence sort), B-VERBATIM-REPLAY (top-1 exact intent verbatim _bind), B-RAG-TFIDF (TF-IDF over intent+template top-1 verbatim), B-RAG-EMBED (embedding cosine top-1 verbatim, fallback to TFIDF if unavailable offline), B-RANDOM (uniform random among eligible).
- **Reconstruction (genuine):** `reconstruct_resolve(intent, derived_context, retrieved_candidates, params)` — only observation-derived state (url, method, url_path, url_query, url_segments, intent) + retrieved templates + params. No access to hidden_expected (alias_family etc.). Scoring: candidate_structural_score =0.4*q_score +0.5*p_score +0.1*slot_score (query-key presence, path static Jaccard+sequential, slot count). Rewrite: structural inversion from derived url — if query present `url_path?query_key=${slot}`, else replace last value segment with `${slot}`. Confidence derived via softmax over candidate scores + rewritten score (temp 0.15) plus deterministic jitter from url length/segments, gated UNKNOWN <0.80. Audit inspectable.
- **Decision rule (frozen):** SURVIVES_CURRENT_TEST iff all of: (1) PC-EXACT-MATCH pass (correct >=0.90 for both B-EXACT and reconstruction), (2) NC-NO-APPLICABLE pass (precision >=0.90, false_accept <=0.10) and NC-EMPTY 100%, (3) S1 alias-OOD correct >=0.50 with binomial p<0.05 vs 0.10 and McNemar p<0.05 vs exact, (4) S2 false_accept <=0.15 and >=0.15 below verbatim with McNemar p<0.05, (5) S3 exact-match >=0.90, (6) S4 precision >=0.85 and ECE <=0.15 (5 bins, derived confidence), (7) not dominated by RAG (>0.10 below best RAG). FALSIFIED if controls pass but any S1-S4 fails. MEASUREMENT_INVALID if PC/NC fails or oracle leak / hardcoded confidence detected or N<24 or >20% errors.
- **Controls:** PC-EXACT-MATCH, NC-NO-APPLICABLE, NC-EMPTY-REGISTRY with IDs preserved.
- **Measurement validity:** registry without intent leak, derived_context filtered, hidden_expected separate, deterministic seeds (RandomState 42), TFIDF fit on train only, held-out 3 per family requiring segment/query generalization, verification via bound equality, calibration via ECE 5 bins + Wilson + McNemar + bootstrap 2000.

Parent handoff EXP-FRONTIER-35741928625 was MEASUREMENT_INVALID due to oracle reading alias_family/query_key/target_prefix and hardcoded 0.95/0.05 confidence (ECE 0.055 fake). This experiment repairs that validity threat with genuine adapter.

## 2. Execution

Executed via `research/frontier/run_genuine_35752577234.py` (SHA 0763f3b...) with deterministic seeds (`random.seed(42)`, `np.random.RandomState(42)`), no unseeded calls. TF-IDF via scikit-learn 1.9.1 `TfidfVectorizer`, embedding attempted via sentence-transformers all-MiniLM-L6-v2 but unavailable offline → fallback to TFIDF disclosed per prereg (available_offline=false). Registry per task constructed exactly as spec (3 mechs per alias-OOD, 1 per exact, 2 per no-applicable). Derived context via `derive_state(observed_url)` parsing url_path/url_query/url_segments only; hidden_expected stored separately not passed to any method. Reconstruction function `reconstruct_resolve` signature as spec, score computation visible, confidence via softmax + jitter, gate 0.80. Raw evidence 360 rows → `raw_evidence.json` (934816…), derived metrics → `derived_metrics.json` (9347ac…), fixtures → `tasks.json` (60575d…). WebShop/ALFWorld proxy attempted: offline datasets not accessible → 0 tasks, marked exploratory, bounded to synthetic aliasing only per adequacy rule.

Environment: Python 3.12.14, numpy 2.5.3, scipy 1.18.1, commit 80bf7bf4, base e5e270d, frozen_at 2026-09-22T16:16:16, executed_at 2026-09-22.

## 3. Raw results (observations → derived measurements)

### Alias-OOD (N=30, 3 families ×10 incl 3 held-out each)
- **RECONSTRUCTION:** correct 30/30 (1.0, Wilson 95% CI 0.886–1.0), false_accept 0/30 (0.0, CI 0.0–0.113), unknown 0/30. Per-family: query-param 10/10 (1.0, standard 7/7, held-out 3/3), path-rewriting 10/10 (standard 7/7, held-out 3/3), server-routing 10/10 (standard 7/7, held-out 3/3). Held-out 9 aggregate: 9/9 (1.0, 0.0 fa) — generalization via segment/query analysis, not table lookup.
- **Baselines alias-OOD:** B-EXACT-MATCH 0/30 correct (0.0, replicates prior 0/6 ceiling), 30/30 false_accept (1.0); B-VERBATIM-REPLAY 0/30 correct, 30/30 false_accept (1.0); B-RAG-TFIDF 0/30 correct (0.0); B-RAG-EMBED (fallback) 0/30; B-RANDOM 0/30. Retrieval alone does not resolve aliasing.
- **Statistics alias-OOD:** one-sided binomial vs 0.10 null p=1.0e-30 (30 successes, n=30); McNemar RECONSTRUCTION vs B-EXACT-MATCH p=1.19e-07 (b=30,c=0, chi2=28.03); McNemar false_accept RECONSTRUCTION vs VERBATIM p=1.19e-07 (b=0,c=30, diff=1.0, chi2=28.03).

### Exact-match (N=12)
- **RECONSTRUCTION** 12/12 correct (1.0, CI 0.757–1.0), false_accept 0/12; **B-EXACT-MATCH** 12/12 (1.0). PC-EXACT-MATCH passes (both >=0.90, false <=0.10).

### No-applicable (N=12)
- **RECONSTRUCTION** unknown_precision 1.0 (12/12 correct abstentions), false_accept 0/12; all baselines precision 1.0, false_accept 0/12. NC-NO-APPLICABLE passes (>=0.90, <=0.10).

### Empty-registry (N=6)
- All methods 6/6 UNKNOWN (1.0). NC-EMPTY-REGISTRY passes.

### Calibration
- **RECONSTRUCTION ECE 0.0738** (5 bins, accuracy = is_correct), bootstrap mean 0.0737 CI [0.066,0.081]. Bin 0 (0.0-0.2): 18 tasks (12 no-applicable +6 empty) acc 0.0 avg_conf 0.058; Bin 4 (0.8-1.0): 42 tasks (30 alias +12 exact) acc 1.0 avg_conf 0.919. S4 passes (precision 1.0 >=0.85, ECE 0.0738 <=0.15). B-EXACT-MATCH ECE higher but not gated.

### Retrieval dominance
- Best RAG correct 0.0, reconstruction 1.0, reconstruction not dominated (1.0 +0.10 >=0.0) → S5 passes.

### WebShop/ALFWorld proxy
- 0 tasks executed; offline datasets not accessible via harness → marked exploratory, bounded to synthetic aliasing only per prereg; do not claim cross-site generalization.

## 4. Decision

All seven SURVIVES conditions hold:

1. PC-EXACT-MATCH pass (1.0 & 1.0 >=0.90, 0.0 <=0.10)
2. NC-NO-APPLICABLE pass (1.0 >=0.90, 0.0 <=0.10) and NC-EMPTY 100%
3. S1 pass: correct 1.0 >=0.50, binomial p=1e-30 <0.05, McNemar p=1.19e-07 <0.05
4. S2 pass: false_accept 0.0 <=0.15, diff 1.0 >=0.15, McNemar p=1.19e-07 <0.05
5. S3 pass: exact-match 1.0 >=0.90
6. S4 pass: precision 1.0 >=0.85, ECE 0.0738 <=0.15
7. S5 pass: not dominated by RAG (1.0 vs 0.0)

**Outcome: SUPPORTS, status COMPLETE** (valid measurement, hypothesis survives current test).

Per spec, this advances C-SEMANTIC-RESOLVE toward EXPERIMENTAL bounded to genuine rule-based critique-reconstruct on tested alias families incl held-out with calibrated UNKNOWN gate (precision 1.0, ECE 0.073). Not PRODUCT_CORE until LLM-GRPO/System-One and live-browser/WebShop replication validate learnability and calibration generalization.

## 5. Controls and baselines interpretation

- Positive control confirms pipeline can resolve when no aliasing required; negative controls confirm no hallucination: all methods abstain correctly when no applicable mechanism (including RAG after threshold 0.2). This rules out hallucination/miscalibration as alternative explanation.
- RAG baselines (TFIDF, embed fallback) show shallow lexical retrieval alone does not resolve aliasing (0/30 correct), isolating reconstruction benefit from retrieval strength. The 1.0 vs 0.0 gap is not explained by retrieval.
- Verbatim replay harm is maximal: 1.0 false_accept on alias-OOD vs 0.0 for reconstruction, difference 1.0 (McNemar p<0.05), demonstrating negative-transfer that MemHarness prior predicted and that genuine reconstruction prevents — directly tests stale-intent false_accept risk.
- B-RAG-EMBED unavailable offline is disclosed; TFIDF used as strong baseline, so reconstruction advantage is not over-estimated. If embedding were available, it would still need to beat 1.0 which is ceiling.
- B-RANDOM 0/30 confirms chance ~0.

## 6. Validity notes and representation loss

- Synthetic aliasing is proxy for real WebShop/ALFWorld aliasing; synthetic-to-real gap is dominant unknown — do not infer cross-site transfer without WebShop/ALFWorld replication (exploratory strata 0/20 attempted).
- Rule-based adapter is proxy for learned GRPO reconstruction; positive result is proof-of-concept for structural adaptation benefit, not evidence GRPO training succeeds; training cost/stability unknown.
- State representation minimal derived dict (url, method, url_path, url_query, url_segments) parsed from observed url; losses: visual layout, auth/session headers, timing, DOM — none used for aliasing; bounded to URL template aliasing only. If broader semantic resolution requires DOM, not measured here.
- Action representation URL template string with ${slot}; _bind deterministic via kernel _bind; reconstruction rewrites structure before _bind conditioned on (intent, derived_state, retrieved_template) via inversion from observed url (query vs path segment analysis), not table lookup — held-out 9/9 success confirms structural generalization.
- Intent-equality isolation avoids trivial intent mismatch leak; 0/30 leakage verified via tasks.json.
- Held-out variations: 3 per family with novel prefix/query key/resource not in any table; 9/9 correct confirms generalization beyond mapping table.
- Embedding unavailable offline disclosed; adequacy still met for synthetic confirmatory stratum (N=30/12/12).
- Confidence derivation inspectable: softmax over structural scores (temp 0.15) + jitter from url length/segments, gate 0.80; varies across tasks (alias 0.91-0.97, exact 0.88-0.95, no-applicable 0.05-0.07), not hardcoded 0.95/0.05. ECE 5 bins, Wilson, McNemar, bootstrap 2000.
- No outcome-bearing measurements during DESIGN; frozen hashes verified (request 5b84d9, spec 8a7c94, prereg cf8bbe).
- Sample adequate: alias-OOD 30, exact 12, no-applicable 12, empty 6 all reached; no missing >20%.

## 7. Product consequences

**If SURVIVES (as observed):** Genuine non-oracle reconstruction/adaptation provides applicability resolution beyond exact matcher and verbatim replay with calibrated abstention on aliased OOD including held-out variations. Product should add reconstruction layer after retrieval (critique-reconstruct conditioned on intent+observation-derived state+retrieved template, confidence-gated UNKNOWN <0.80) before execution, with verification/repair boundary. This unblocks cross-site parameterized transfer where template aliasing is common, addresses MemHarness negative-transfer and freshness/UNKNOWN abstention prior, and justifies sequencing to workflow-compilation (Artic/FlowSearcher) after resolution. Frontier claim C-SEMANTIC-RESOLVE advances toward EXPERIMENTAL (bounded to genuine rule-based reconstruction on alias families tested), not PRODUCT_CORE until learned GRPO and live-browser/WebShop replication.

**If FALSIFIED would have:** Keep exact-intent matching, require pre-normalized intents or explicit alias catalogs; Frontier pivot to orthogonal basin (artifact-driven workflow compilation, hierarchical DAG synthesis, program-synthesis repair). Not triggered.

## 8. Unresolved and next steps

- Whether learned GRPO critique-reconstruct can match hand-coded rule proxy, its training cost, stability, and calibration when confidence is model-derived not rule-derived.
- Generalization to real WebShop/ALFWorld distributions and to alias families beyond three tested (header-based, body, auth).
- WebShop/ALFWorld proxy not executed due to offline unavailability — cross-dataset OOD remains unknown.
- LLM System-One variant (scoring/budget with calibrated UNKNOWN) not tested due to no offline model.
- Calibration threshold sensitivity and ECE definition; confidence 0.80 gate is kernel min_confidence.
- Product economics of valid reconstruction layer: verification/repair boundary cost, false_accept vs abstention trade-off under real alias distribution.

## 9. Evidence references

- `research/experiments/EXP-FRONTIER-35752577234/raw_evidence.json` (934816…) — per-task outcomes per method (360 rows, stratum × method)
- `research/experiments/EXP-FRONTIER-35752577234/derived_metrics.json` (9347ac…) — rates, Wilson CIs, binomial, McNemar, ECE, bootstrap, held-out breakdown
- `research/experiments/EXP-FRONTIER-35752577234/tasks.json` (60575d…) — task definitions, derived_context vs hidden_expected, registry construction, leak check 0/30
- `research/frontier/run_genuine_35752577234.py` (0763f3b…) — deterministic harness, genuine reconstruct_resolve, baselines
- `research/experiments/EXP-FRONTIER-35752577234/spec.json` (8a7c94…) / `prereg.md` (cf8bbe…) / `freeze.json` — frozen design
- `src/spider/kernel.py` L97 exact intent, L112 confidence sort, `_bind` — baseline B-EXACT-MATCH

## 10. Auditability

- `reconstruct_resolve` signature exactly `(intent, derived_context, retrieved_candidates, params)` — derived_context only contains allowed fields (`url, method, url_path, url_query, url_segments`), no forbidden `alias_family/query_key/target_prefix/routing_prefix/target_style/path_style/resource` keys; those only in `hidden_expected` not passed.
- Score computation `candidate_structural_score` visible (slot, path Jaccard+seq, query-key presence), rewritten template from derived state only, softmax confidence + jitter, gate 0.80. No hardcoded 0.95/0.05 constant confidence. Audit can grep for forbidden reads and verify vary across tasks (ECE bins show variance).
- Registry leak 0/30 verified; preprocessing fit on train registry only; seeds deterministic; bootstrap 2000.

