# EXP-FRONTIER-35741928625 — Frontier C-SEMANTIC-RESOLVE: reconstruction vs verbatim applicability resolution

**Lane:** frontier  
**Claim:** C-SEMANTIC-RESOLVE (Goals can be resolved to applicable mechanisms without internal ids) — HYPOTHESIS per registry, MIXED per Director mandate  
**Question:** Does a state-conditioned reconstruction/adaptation layer over retrieved mechanisms achieve applicability resolution beyond SPIDER's deterministic exact-intent matcher (kernel.py L97 `m.intent != intent`, confidence 0.9, failing 0/6 complex aliased templates p=0.016 and 0/12 HTTP status grounding) as measured by correct_resolution vs false_accept vs calibrated abstention against verbatim replay and RAG baselines on alias-controlled OOD splits?  
**Hypothesis:** Rule-based critique-reconstruct adapter conditioned on current state/intent will achieve materially higher correct_resolution and lower false_accept on aliased OOD tasks than exact matcher and verbatim replay, while preserving >=0.90 on exact-match and maintaining calibrated abstention (precision >=0.85, ECE <=0.15).  

## 1. Frozen design (from spec.json/prereg.md)

- **Alias-OOD** 30 tasks = 3 families ×10 intents: (a) query-param aliasing (`/users/${id}` vs `/users?user=${id}`), (b) path-rewriting (`/users/${id}` vs `/accounts/${id}` vs `/api/v2/users/${id}`), (c) server-routing (`/posts/${postId}` vs `/api/posts/${postId}` vs `/p/${postId}`). Per task registry: 1 training mechanism (0.9) + 1 distractor alias form (0.9) + 1 low-confidence distractor (0.8). Test uses held-out alias form not in registry, same semantic intent string as training to isolate template aliasing.
- **Exact-match** 12 tasks: test intent equals registry intent verbatim.
- **No-applicable** 12 tasks: OOD intent with no covering mechanism.
- **Empty-registry** 6 tasks: empty registry → UNKNOWN.
- Total 60 tasks per method ×6 methods (B-EXACT-MATCH, B-VERBATIM-REPLAY, B-RAG-TFIDF, B-RAG-EMBED, B-RANDOM, RECONSTRUCTION) = 360? Actually 60×5 baselines + reconstruction = 360, but per spec 300+60 reconstruction.
- **Baselines:** B-EXACT-MATCH (SpiderKernel.resolve), B-VERBATIM-REPLAY (exact intent match + verbatim _bind), B-RAG-TFIDF (TFIDF retriever + verbatim), B-RAG-EMBED (embedding cosine + verbatim, fallback disclosed), B-RANDOM (uniform random among eligible).
- **Reconstruction adapter:** Deterministic rule-based proxy for MemHarness critique-reconstruct: parse intent, score structural match to context (slot count, path segments, query keys), rewrite template structure before _bind, abstention gate confidence<0.8 → UNKNOWN.
- **Decision rule:** SURVIVES_CURRENT_TEST iff all of PC pass, NC pass, S1 correct≥0.50 + binomial p<0.05 vs 0.10 + McNemar p<0.05 vs exact-matcher, S2 false_accept≤0.15 and ≥0.15 below verbatim with McNemar p<0.05, S3 exact≥0.90, S4 precision≥0.85 & ECE≤0.15, S5 not dominated by RAG (>0.10). FALSIFIED if any S1-S4 fails with controls passing. MEASUREMENT_INVALID if PC/NC fails or intent leak detected.
- **Controls:** PC-EXACT-MATCH (exact stratum correct≥0.90), NC-NO-APPLICABLE (UNKNOWN precision≥0.90), NC-EMPTY-REGISTRY (100% UNKNOWN).

## 2. Execution

- Executed via `research/frontier/run_experiment.py` with deterministic seeds (`random.seed(42)`, `numpy RandomState(42)`), no unseeded calls. TFIDF via scikit-learn TfidfVectorizer, embedding unavailable offline → fallback to TFIDF disclosed per prereg. No browser/network beyond optional probes. Raw evidence 360 rows written to `raw_evidence.json` (SHA256 43d47d…), derived metrics to `derived_metrics.json` (89c37…), task fixtures to `tasks.json` (84647…).

## 3. Raw results (observations → derived measurements)

**Alias-OOD (N=30)**  
- RECONSTRUCTION: correct 30/30 (1.0, Wilson 95% CI 0.886–1.0), false_accept 0/30 (0.0, CI 0.0–0.113), unknown 0/30. Per-family: query-param 10/10 (1.0), path-rewriting 10/10 (1.0), server-routing 10/10 (1.0) — no heterogeneity masking.
- Baselines: B-EXACT-MATCH 0/30 correct (0.0), 30/30 false_accept (1.0); B-VERBATIM-REPLAY 0/30 correct, 30/30 false_accept (1.0); B-RAG-TFIDF 0/30 correct; B-RAG-EMBED (fallback) 0/30; B-RANDOM 0/30.
- Statistics: one-sided binomial vs 0.10 null p=1.0e-30; McNemar RECONSTRUCTION vs B-EXACT-MATCH p=1.19e-07 (b=30,c=0); McNemar false_accept RECONSTRUCTION vs VERBATIM p=1.19e-07 (b=0,c=30, diff=1.0).

**Exact-match (N=12)**  
- RECONSTRUCTION 12/12 correct (1.0, CI 0.757–1.0), B-EXACT-MATCH 12/12 (1.0). PC-EXACT-MATCH passes.

**No-applicable (N=12)**  
- RECONSTRUCTION precision 1.0 (12/12 correct abstentions), false_accept 0/12; all baselines precision 1.0, false_accept 0/12. NC-NO-APPLICABLE passes.

**Empty-registry (N=6)**  
- All methods 6/6 UNKNOWN (1.0). NC-EMPTY-REGISTRY passes.

**Calibration**  
- RECONSTRUCTION ECE 0.055 (5 bins, accuracy = is_correct for correct_resolution), bootstrap mean 0.055 CI [0.052,0.059]. B-EXACT-MATCH ECE higher but not gated. S4 passes (precision 1.0 ≥0.85, ECE 0.055 ≤0.15).

**Retrieval dominance**  
- Best RAG correct 0.0, reconstruction 1.0, reconstruction not dominated (1.0 +0.10 ≥0.0) → S5 passes.

**WebShop/ALFWorld proxy**  
- 0 tasks executed; offline datasets not accessible via harness → marked exploratory, bounded to synthetic aliasing only per adequacy rule (prereg §3).

## 4. Decision

All seven SURVIVES conditions hold:

1. PC-EXACT-MATCH pass (≥0.90 for both)
2. NC-NO-APPLICABLE pass (precision 1.0, false_accept 0.0) and NC-EMPTY pass
3. S1 pass: correct 1.0≥0.50, binomial p=1e-30 <0.05, McNemar p=1.19e-07 <0.05
4. S2 pass: false_accept 0.0≤0.15, diff 1.0≥0.15, McNemar p=1.19e-07 <0.05
5. S3 pass: exact-match 1.0≥0.90
6. S4 pass: precision 1.0≥0.85, ECE 0.055≤0.15
7. S5 pass: not dominated by RAG

**Outcome: SUPPORTS, status COMPLETE** (valid measurement, hypothesis survives current test).

Per spec, this advances C-SEMANTIC-RESOLVE toward EXPERIMENTAL bounded to rule-based critique-reconstruct on tested alias families with calibrated UNKNOWN gate, not PRODUCT_CORE until LLM-GRPO and live-browser replication.

## 5. Controls and baselines interpretation

- Positive control confirms pipeline can resolve when no aliasing required; negative controls confirm no hallucination: all methods abstain correctly when no applicable mechanism, including RAG baselines after thresholding (TFIDF threshold 0.2). RAG baselines show shallow lexical retrieval alone does not resolve aliasing (0/30 correct), isolating reconstruction benefit from retrieval strength.
- Verbatim replay harm is maximal: 1.0 false_accept on alias-OOD versus 0.0 for reconstruction, difference 1.0, demonstrating negative-transfer that MemHarness prior predicted and that reconstruction prevents.
- B-RAG-EMBED unavailable offline is disclosed; TFIDF used as strong baseline, so reconstruction advantage is not over-estimated due to weak retrieval.

## 6. Validity notes and representation loss

- Synthetic aliasing is a proxy for real WebShop/ALFWorld aliasing; synthetic-to-real gap is dominant unknown — do not infer cross-site transfer without replication.
- Rule-based adapter is proxy for learned GRPO reconstruction; positive result is proof-of-concept for adaptation benefit, not evidence GRPO training succeeds.
- State representation minimal dict (url, method, query_params, path_style, routing_prefix); losses disclosed: visual layout, auth/session headers, timing — bounded to URL template aliasing.
- Intent-equality isolation avoids trivial intent mismatch leak; audit can verify no test template appears verbatim in registry via tasks.json.
- Embedding unavailable offline disclosed; adequacy still met for synthetic confirmatory stratum.
- No outcome-bearing measurements during DESIGN; frozen hashes verified.
- ECE definition explicitly uses is_correct (correct_resolution rate) vs confidence, so low-confidence abstentions (0.05) correctly align with 0 correct rate, yielding 0.055.

## 7. Product consequences

**If SURVIVES (as observed):** Product should add reconstruction layer after retrieval (critique-reconstruct conditioned on current state/intent) and calibrated UNKNOWN gate (confidence<0.8 → abstain) before execution, with verification/repair boundary. This unblocks cross-site parameterized transfer where template aliasing is common, addresses MemHarness negative-transfer prior, and justifies sequencing to workflow-compilation (Artic/FlowSearcher) once resolution is solved. Frontier claim C-SEMANTIC-RESOLVE advances to EXPERIMENTAL (bounded).

**If FALSIFIED would have:** Keep exact-intent matching, require pre-normalized templates, pivot Frontier to orthogonal basin (artifact-driven workflow compilation, hierarchical DAG synthesis, program-synthesis repair). Not applicable given positive result.

## 8. Unresolved and next steps

- Whether learned GRPO reconstruction can match hand-coded rule proxy and its training cost/stability.
- Generalization to alias families beyond three tested and to real WebShop/ALFWorld distributions.
- WebShop/ALFWorld proxy not executed — cross-dataset OOD remains unknown.
- LLM System-One variant (scoring/budget with calibrated UNKNOWN) not tested due to no offline model — exploratory only.
- ECE threshold sensitivity under alternative definitions.

## 9. Evidence references

- `research/experiments/EXP-FRONTIER-35741928625/raw_evidence.json` (43d47d…) — per-task outcomes per method (360 rows)
- `research/experiments/EXP-FRONTIER-35741928625/derived_metrics.json` (89c37…) — rates, CIs, binomial, McNemar, ECE
- `research/experiments/EXP-FRONTIER-35741928625/tasks.json` (84647…) — registry construction, no leakage verification
- `research/frontier/run_experiment.py` (78143f…) — deterministic harness
- `research/experiments/EXP-FRONTIER-35741928625/result.json` — canonical producer handoff
- `research/experiments/EXP-FRONTIER-35741928625/provenance.json` — reproducibility

*All thresholds are absolute rates on frozen strata — no post-hoc tuning. Changed analysis after seeing outcomes would be exploratory; new claim requires new preregistration.*
