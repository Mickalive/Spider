# EXP-FRONTIER-35789949165 — WebAPI endpoint+method+auth-scope mining vs hierarchical retrieval complementarity

**Lane:** frontier | **Claim:** C-SEMANTIC-RESOLVE | **Status:** COMPLETE **Outcome:** MIXED
**Question:** Does WebAPI endpoint+method+auth-scope mining provide higher-leverage alias-OOD resolution than hierarchical decoupling-before-aggregation retrieval complementarity on same validated synthetic orthogonal header/body/auth + mixed splits (40 pooled, 30 orthogonal, 10 mixed, 9 held-out) without BrowserGym?

## 1. Result in one sentence
WebAPI endpoint mining achieves strong alias-OOD resolution (39/40 0.975) statistically superior to exact-match (binomial p 9e-27, McNemar p 1.9e-09) and far below verbatim false_accept (0.025 vs 1.0 McNemar p 7.9e-10) with calibrated ECE 0.139 and no regression on exact-match (12/12), **but shows zero complementarity advantage over flat K5 or hierarchical** (coverage gain 0.0 CI [0.0,0.0] p 1.0, density gain -0.03 p 0.85) under pool 8>k=5, so S1-S5 pass but **S6 fails → MIXED**.

## 2. Frozen design recap
- **Fixture:** byte-identical reuse of EXP-FRONTIER-35773143736 tasks.json sha 4abf1487 (40 pooled =30 orthogonal 3 families x10 +10 mixed, 12 exact, 12 no-applicable, 6 empty =70 tasks) but **per-task registry expanded 3→8** (1 train 0.9 +2 same-family 0.9 +2 cross-family 0.9 +2 mixed fragments 0.85 +1 random 0.8) to fix parent structural pool<=k (coverage 1.0 for all) limitation. Leak 0/40, 0/9 held-out, 0/10 mixed. No BrowserGym.
- **Pipelines (8 paired):** B-EXACT-MATCH, B-VERBATIM-REPLAY, B-FLAT-RAG-TFIDF-K5 +reconstruction, B-FLAT-RAG-EMBED-K5 +reconstruction (all-MiniLM-L6-v2, available), B-FLAT-RAG-EMBED-K1 verbatim ablation, B-RANDOM-K5 +reconstruction, H-HIERARCHICAL-XMEMORY-KADAPTIVE (reuse byte-identical code sha 2d6640, TFIDF centroids, Jaccard>=0.6 agglomerative, adaptive k 2-5, entropy>0.4 or distinct<2), H-WEBAPI-ENDPOINT-MINING-KADAPTIVE (endpoint catalog derived from train registry, endpoint components parse method+path+header/body/auth, Jaccard 0.6 endpoint themes 84, top-down complementary, adaptive k 3-5, deterministic endpoint invocation via same choose_adoptions+rewrite_template_multi before _bind, softmax temp 0.15 + jitter gated UNKNOWN<0.80).
- **Controls (frozen):** PC-EXACT-MATCH (>=0.90), PC-RETRIEVAL-HEALTH (non-empty >=90%, distinct >= flat >=50%), PC-WEBAPI-INDEX-BUILT (>=3 themes >=6 components), NC-NO-APPLICABLE (prec >=0.90), NC-EMPTY (100%), NC-ORACLE-LEAK (no forbidden keys, std>0.05), NC-FLAT-COLLAPSE diagnostic. EMBED-K1 exempt from NC gate, exact/verbatim exempt from oracle std per parent.
- **Metrics:** pooled correct (binomial vs 0.10, McNemar vs exact), false_accept vs verbatim, coverage recall@k, density, ECE 5 bins, per-family/held-out/mixed, block bootstrap 2000 trajectory-grouped by family, Wilson CI.

## 3. Raw evidence (distinct from derived)
- 560 paired calls, 0 harness errors.
- **Alias-OOD 40:** WebAPI 39/40 0.975 Wilson [0.871,0.996], hier 39/40 0.975, TFIDF-K5 39/40 0.975, EMBED-K5 39/40 0.975, RANDOM 39/40 0.975, EMBED-K1 38/40 0.95 (verb. ablation), EXACT 0/40, VERBATIM 0/40. Orthogonal 29/30 0.967, mixed 10/10 1.0, held-out 8/9 0.889 for WebAPI/hier/flat (single auth heldout failure).
- **Coverage:** 1.0 for all pipelines (WebAPI 1.0, hier 1.0, flat 1.0, random 1.0). Gain WebAPI vs best flat 0.0 bootstrap mean 0.0 CI [0.0,0.0] p 1.0; hier vs flat 0.0. Density WebAPI 1.68 vs flat 1.71 gain -0.03 p 0.85.
- **Controls:** exact 12/12 all, no-applicable precision 1.0 false 0.0 (checked), empty 6/6, non-empty 1.0 all, distinct win 0.825, index hier 84 webapi 84 components 45 episodes 168, oracle leak 0 forbidden, conf std 0.09 >0.05 (checked pipelines).
- **Calibration:** WebAPI ECE 0.1389 bootstrap mean 0.138 CI [0.08,0.18] <=0.15 pass, UNKNOWN precision 1.0 >=0.85 pass, false 0.025 <=0.15 and 0.975 below verbatim.

## 4. Derived measurements
- **S1:** WebAPI pooled 0.975 >=0.50 binomial p 9e-27 <0.05 McNemar vs exact p 1.9e-09 <0.05 orth 0.967 >=0.50 mixed 1.0 >=0.40 heldout 0.889 >=0.50 **PASS**
- **S2:** false 0.025 <=0.15 and 0.975 below verbatim 1.0 McNemar p 7.9e-10 <0.05 **PASS**
- **S3:** exact 12/12 1.0 >=0.90 not >0.10 below exact (0.0 diff) and not >0.10 below hier (0.0) **PASS**
- **S4:** precision 1.0 >=0.85 ECE 0.1389 <=0.15 bootstrap upper 0.18 <=0.18 **PASS**
- **S5:** not >0.10 below hier (0.0) and not >0.10 below best flat (0.0) McNemar vs hier p 1.0 (parity) **PASS**
- **S6:** coverage gain 0.0 <0.15 fail, bootstrap p 1.0 fail, CI low 0.0 fail, density gain -0.03 fail **FAIL**
- Overall: **S1-S5 pass, S6 fail → MIXED** per prereg §7 (SURVIVES requires S1-S6, MIXED if S1-S5 pass but S6 fails, FALSIFIED if S1/S2 severe fail).

## 5. Interpretation (separate from raw)
MIXED means WebAPI endpoint mining **does not provide higher-leverage alias-OOD resolution than hierarchical or even flat K5** on this synthetic with minimal derived dict, even after fixing pool saturation (8>5). The reconstruction rule (adopt-any-observed-key-not-in-registry + rewrite_template_multi) is **too powerful**: any non-empty candidate set yields correct bound because observed alias key (Authorization, token, X-Permission etc.) is never in registry union (held-out), so recall is 1.0 for all retrievers including random. Pool 8>k is identifiable in principle but **non-discriminating** under this reconstruction.

Hierarchical prior MIXED (coverage 0.0 due to pool<=k, 63 singleton themes) is **replicated in a stronger sense**: even with 84 themes and pool 8>k, hierarchical and WebAPI remain tied with flat (all 39/40) and density identical. Endpoint mining at the endpoint-theme level provides no complementarity beyond header/body/auth template rewriting; tool/API bypass prior (Fetch/WebMCP) not validated here.

Product consequence per spec: **Do NOT replace hierarchical or flat RAG with WebAPI mining layer**; keep existing retrieval (exact-intent scan or flat RAG when intent differs) and genuine reconstruction proxy as value-add; prioritize explicit alias catalogs or server-side normalization for these families. C-SEMANTIC-RESOLVE remains EXPERIMENTAL at rule-based ceiling 39/40 (vs prior 40/40) bounded to synthetic orthogonal header/body/auth + mixed with minimal derived dict, hierarchical MIXED persists, WebAPI MIXED adds no higher-leverage evidence. No promotion to Product Core.

## 6. Validity threats
- Synthetic 0 live tasks; derived_context tautologically contains answer key not in registry; synthetic-to-real gap dominant (no BrowserGym 1280x720, no AX, no production SPA).
- Reconstruction confound: genuine rule masks retrieval differences; ablation B-EMBED-K1 (verbatim) shows retrieval alone 0.95 vs 0.0 for exact, but K5+recon still 0.975 for all, so retrieval bottleneck not tested.
- One pooled failure (auth heldout) suggests minor registry expansion imperfection but not gating.
- ECE 0.139 with 3 of 5 bins empty (bimodal conf), std 0.09, calibration transfer limited.
- 84 themes (vs 63 singleton parent) indicates grouping exercised but not leveraged for coverage.

## 7. What would change the claim
- Disable reconstruction or require correct-family candidate for rewrite to make coverage discriminating, or use verbatim bind baseline to test retrieval alone.
- Test live BrowserGym where derived_context noisy and reconstruction may fail, making complementary discovery valuable.
- Direct endpoint invocation vs template rewriting on real Fetch/WebMCP substrate with auth-scope discovery.

## 8. Artifacts
- `raw_evidence.json` (49cb41...), `derived_metrics.json` (1d1c67...), `index_manifest.json` (c56d22...), `train_split_inventory.json` (4922ca...), `tasks_expanded.json` (544707...), `run_execute_35789949165.py` (code).

*Frozen spec/prereg/decision_rule: spec.json sha 5f1b15..., prereg sha b45bd6..., freeze 2026-09-22T22:05:01Z.*
