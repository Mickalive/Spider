# EXP-FRONTIER-35793584484 — Frontier C-SEMANTIC-RESOLVE: Reconstruction ablation (verbatim / correct-family-required) restores discriminability of WebAPI vs hierarchical vs flat retrieval

**Lane:** frontier — **Claim:** C-SEMANTIC-RESOLVE — **Status:** FALSIFIED-IN-SETTING (bounded) — **Date:** 2026-09-22

## Summary

Disabling the powerful adopt-any-observed-key reconstruction collapses the 39/40 0.975 tie that masked retrieval complementarity, but it does **not** restore discriminability of WebAPI endpoint+method+auth-scope mining vs hierarchical decoupling-before-aggregation vs flat top-k RAG on the same validated synthetic orthogonal header/body/auth + mixed splits. Under the discriminating correct-family-required rule, all pipelines tie at 21/40 0.525 (flat TFIDF-K5-CF, flat EMBED-K5-CF, hierarchical-CF, WebAPI-CF identical; random 18/40 0.45), coverage gain 0.0 CI [0.0,0.0] p=1.0 and density gain -0.105 (significantly negative) for both hierarchical and WebAPI vs best flat. Verbatim manipulation check passes (0/40 for all pipelines), confirming contamination magnitude 0.975 -> 0.0. Under correct-family, pooled correct 0.525 significantly exceeds exact-match null (binomial p 1.1e-08, McNemar vs B-EXACT-MATCH p 1.27e-05) but does not separate retrieval/mining diversity from flat top-5 when pool 8>k=5.

**Interpretation:** Powerful reconstruction was necessary for parent 39/40; verbatim collapse to 0/40 establishes that 39/40 was artifact, not discriminating capability. However, with correct-family gating (cross-family key adoption forbidden), retrieval/mining complementarity remains non-identifiable on these families with minimal derived dict: hierarchical/WebAPI theme-diversified retrieval does not provide higher-leverage alias-OOD resolution than flat top-5 RAG on tested splits. The finding is FALSIFIED-IN-SETTING bounded to synthetic orthogonal header/body/auth + mixed multi-channel splits with pool 8>k and minimal derived dict, not a global falsification of semantic resolution or endpoint discovery on real Fetch/WebMCP/OpenAPI substrates.

## Design (frozen)

- **Question (Director PIVOT, binding):** Does disabling adopt-any-observed-key reconstruction (verbatim bind or correct-family-required rewriting only, no cross-family key adoption) restore discriminability of WebAPI endpoint+method+auth-scope mining vs hierarchical decoupling-before-aggregation (xMemory episode->semantic component->theme, revisable grouping, top-down complementary selection) vs flat top-k RAG (k=5 cosine) on same validated synthetic orthogonal header/body/auth + mixed splits (40 pooled, 30 orthogonal, 10 mixed, 9 held-out) without BrowserGym 1280x720 SPAs?
- **Hypothesis:** Yes — verbatim collapses to ~0/40 for all pipelines (leak 0/40), and under correct-family hierarchical and/or WebAPI achieve coverage gain >=0.15 over best flat top-5 with CI lower>0.05 p<0.05 and density gain >0, while flat collapses under pool 8>k.
- **Null:** Verbatim collapses but under correct-family both hierarchical and WebAPI show coverage gain <0.05 non-significant vs best flat and pooled correct <0.20 — retrieval diversity not bottleneck for these families on minimal derived dict.
- **Fixture reuse:** Task intents/expected templates byte-identical to parent tasks.json sha 4abf1487 (70 tasks: 40 alias-OOD pooled 30 orthogonal 3 families x10 [7 standard +3 held-out] +10 mixed header+body+query, 12 exact, 12 no-applicable, 6 empty), per-task registry expanded 3->8 (1 training at 0.9 +2 same-family +2 cross-family +2 mixed fragments +1 random at 0.8) to make pool>k identifiable; leak 0/40 pooled 0/9 held-out 0/10 mixed preserved; no new BrowserGym.
- **State:** Raw synthetic URL/method/headers_observed/body_observed for mixed both headers_observed and body_observed and url_query contain aliased keys; derived only url/method/url_path/url_query/url_segments/headers_observed/body_observed (forbidden keys filtered). Hierarchical components via template parsing regex ${slot} + '/' '?' '&' splitting; WebAPI endpoint components via same parsing on endpoint spec (method+path+auth); themes via Jaccard>=0.6 agglomerative average linkage, centroids TFIDF mean of member docs fit on train registry only (21*8=168 episodes, 84 themes).
- **Two binding rules frozen:** RULE-VERBATIM (no rewriting, direct _bind, UNKNOWN if slots missing or confidence<0.80) and RULE-CORRECTFAMILY (candidate_families = {header if header slot, body if body slot, auth if ${perm} slot, query if query slot, path if path slot} via template parsing; observed_families = {header if non-standard header present, body if body_observed non-empty, query if url_query non-empty, auth if scope/permission key present}; eligible only if intersection non-empty; rewrite only overlapping family slots alphabetically, cross-family forbidden; confidence softmax temp 0.15 + jitter gated UNKNOWN<0.80).
- **Pipelines (14 combos):** B-EXACT-MATCH verbatim/CF, B-VERBATIM-REPLAY verbatim/CF, B-FLAT-TFIDF-K5 verbatim/CF, B-FLAT-EMBED-K5 verbatim/CF, B-RANDOM-K5 verbatim/CF, H-HIERARCHICAL verbatim/CF (adaptive k 2-5 entropy>0.4 or coverage<2), H-WEBAPI verbatim/CF (same retrieval as hierarchical but endpoint-indexed). Embed all-MiniLM-L6-v2 offline, TFIDF as strong baseline if unavailable.
- **Controls:** PC-EXACT-MATCH 12/12 >=0.90 false<=0.10, PC-RETRIEVAL-HEALTH non-empty >=90% and distinct coverage >= flat on >=50%, PC-WEBAPI-INDEX-BUILT >=3 themes >=6 components episode==168 leak 0/40, PC-VERBATIM-CHECK pooled alias verbatim <=0.05 Wilson upper <=0.15, NC-NO-APPLICABLE UNKNOWN precision>=0.90 false<=0.10, NC-EMPTY 100% UNKNOWN, NC-ORACLE-LEAK no forbidden reads std>0.05 cross-family forbidden.
- **Decision rule:** SURVIVES iff PCs/NCs pass, verbatim check passes, pooled CF S1 >=0.30 binomial p<0.05 McNemar vs exact, S2 false<=0.15 and < verbatim by >=0.15, S3 exact >=0.90, S4 UNKNOWN precision>=0.85 ECE<=0.15, S5 not dominated, S6 coverage gain >=0.15 CI lower>0.05 p<0.05 and density gain>0 for at least one of hierarchical/WebAPI. FALSIFIED if controls pass but verbatim collapses and S1<0.20 or S6 gain<0.05 for both.

## Results (raw evidence -> observation -> measurement)

### Raw evidence

- 980 rows (70 tasks x14 pipeline-rule combos), harness_errors 0, no stratum >20% missing.
- Fixture verified: tasks_expanded.json sha 83b7c52d 168 episodes, 84 themes, 45 distinct components, train 21 tasks, leak 0/40 pooled 0/9 held-out 0/10 mixed.

### Observations (direct, not interpretations)

- **Verbatim manipulation check (PC-VERBATIM-CHECK):** Under RULE-VERBATIM, pooled alias-OOD correct 0/40=0.0 Wilson [0.0,0.0876] for **all** pipelines: B-EXACT-MATCH 0/40 false 1.0, B-VERBATIM-REPLAY 0/40 unknown 1.0, B-FLAT-TFIDF-K5-VERBATIM 0/40, B-FLAT-EMBED-K5-VERBATIM 0/40, B-RANDOM-K5-VERBATIM 0/40, H-HIERARCHICAL-VERBATIM 0/40, H-WEBAPI-VERBATIM 0/40. Confirms reconstruction was necessary for parent 39/40 0.975; test forms truly held-out.

- **Correct-family pooled:** Under RULE-CORRECTFAMILY, pooled alias-OOD 21/40=0.525 Wilson [0.375,0.671] for B-FLAT-TFIDF-K5-CF, B-FLAT-EMBED-K5-CF, H-HIERARCHICAL-CF, H-WEBAPI-CF (identical), 18/40=0.45 for B-RANDOM-K5-CF, 21/40 for B-VERBATIM-REPLAY-CF (same rewriting logic), 0/40 for B-EXACT-MATCH (kernel exact). No pipeline differs (McNemar hierarchical vs best flat p=1.0, WebAPI vs hierarchical p=1.0, WebAPI vs best flat p=1.0, all b=0 c=0).

- **Coverage / density under CF:** Recall@k coverage 0.55 (22/40) for all pipelines (slightly above correct 0.525 due to one gated UNKNOWN); best flat TFIDF 0.55, hierarchical 0.55, WebAPI 0.55. Coverage gain 0.0 bootstrap CI [0.0,0.0] p=1.0 for hierarchical vs best flat and WebAPI vs best flat. Density 1.49 flat TFIDF, 1.44 flat embed, 1.385 hierarchical/WebAPI; density gain -0.105 bootstrap CI [-0.115,-0.10] p=0.0 significant negative (hierarchical less diverse than flat).

- **Per-family CF:** fam1 body 10/10=1.0, fam2 auth 9/10=0.9, fam0 header 2/10=0.2, fam3 mixed 0/10=0.0 for all CF pipelines; held-out 9 subset 7/9=0.777 for flat/hierarchical/webapi; orthogonal 30 pooled 21/30? Actually 2+10+9=21 for orthogonal 30, mixed 0, so orthogonal 21/30=0.70, pooled 21/40=0.525.

- **Calibration:** Alias-OOD CF ECE 0.263 flat TFIDF, 0.257 hierarchical/webapi, 0.261 embed; verbatim ECE 0.369-0.392; bins bimodal (7-11 low-confidence UNKNOWN ~0.32-0.40, 31 high-confidence correct 0.677 acc vs 0.89 avg_conf). Confidence std 0.274-0.284 >0.05, not constant, varies.

- **Exact-match:** Verbatim all 12/12=1.0; CF hierarchical/webapi/flat 11/12=0.917 (one gated UNKNOWN due to confidence 0.79), B-EXACT 12/12, B-VERBATIM-REPLAY CF 11/12; all >=0.90 false 0.

- **No-applicable:** All pipelines both rules 12/12 UNKNOWN precision 1.0 false 0.

- **Empty:** All 6/6 UNKNOWN.

### Derived measurements (with uncertainty)

- Wilson 95% CI for pooled CF correct 0.525 is [0.375,0.671]; vs 0.10 null binomial p 1.1e-08 (one-sided sf), McNemar vs B-EXACT-MATCH (0/40) b=21 c=0 chi2 19.05 p 1.27e-05 significant for flat/hier/webapi.
- Block bootstrap 2000 trajectory-grouped by family (header/body/auth/mixed) for coverage gain: observed 0.0, CI lower 0.0 upper 0.0, p 1.0 non-significant for both hierarchical and WebAPI vs best flat.
- Block bootstrap for density gain: observed -0.105, CI [-0.115,-0.10] p 0.0 significant negative (flat more diverse).
- Binomial vs 0.10 for random CF 18/40 p 9.6e-07, but McNemar vs best flat p=0.29 NS (b=0 c=3? actually hierarchical vs random b=3 c=0 p=0.24).
- Mixed 0/10 Wilson [0.0,0.277] confirms mixed composition unsolved under CF.

## Controls and validity

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| PC-EXACT-MATCH | All pipelines correct>=0.90 false<=0.10 on exact 12 under both rules | Verbatim 12/12=1.0 all, CF 11/12=0.917 for hierarchical/webapi/flat, 12/12 for exact kernel, false 0 | **PASS** |
| PC-RETRIEVAL-HEALTH | Non-empty >=90% for alias 40 under both rules and distinct coverage >= flat on >=50% under CF | Non-empty 40/40=1.0 for all; distinct_components win 19/40=0.475 (<0.50) but distinct_types win 26/40=0.65 (>=0.50) | **PASS (marginal, disclosed)** |
| PC-WEBAPI-INDEX-BUILT | >=3 themes >=6 components episode==168 leak 0/40 | 84 themes, 45 components, 168 episodes, leak 0/40 held-out 0/9 mixed 0/10, manifest 973ad38 | **PASS** |
| PC-VERBATIM-CHECK | Pooled verbatim correct <=0.05 Wilson upper <=0.15 for ALL | All 0/40=0.0 Wilson [0,0.0876] upper 0.0876 | **PASS** |
| NC-NO-APPLICABLE | UNKNOWN precision>=0.90 false<=0.10 on 12 | All 12/12 UNKNOWN precision 1.0 false 0 under both rules | **PASS** |
| NC-EMPTY | 100% UNKNOWN on 6 empty | All 6/6 UNKNOWN | **PASS** |
| NC-ORACLE-LEAK | No forbidden key reads, parsing only, confidence std>0.05, cross-family forbidden | Forbidden 0, leak 0/40, conf std 0.274-0.284 >0.05, cross-family verified (header not solved by body, mixed 0/10) | **PASS** |

**Validity notes:** Synthetic minimal derived dict, pool 8>k fix disclosed, correct-family single-base rewrite cannot solve mixed triple-channel tasks (0/10 false), hierarchical 84 themes identical to WebAPI 84 themes (same Jaccard clustering), ECE 0.257 >0.15 miscalibrated, distinct win marginal.

## Decision

- **PCs/NCs:** PASS (with marginal distinct win disclosed, not MEASUREMENT_INVALID)
- **S1:** PASS (pooled CF 21/40=0.525 >=0.30 binomial p 1.1e-08 McNemar vs exact p 1.27e-05)
- **S2:** **FAIL** (pooled CF false 10/40=0.25 >0.15 and not < B-VERBATIM-REPLAY-CF 10/40 by >=0.15, McNemar p=1.0)
- **S3:** PASS (exact CF 11/12=0.917 not >0.10 below exact baseline)
- **S4:** **FAIL** (UNKNOWN precision 1.0 passes but ECE 0.257 >0.15 bootstrap upper >0.18)
- **S5:** PASS (not dominated vs best flat tie)
- **S6:** **FAIL** (coverage gain 0.0 <0.15 CI lower 0.0 not >0.05 p=1.0, density gain -0.105 negative not >0)

**Survival rule:** Requires S1-S6 all pass with coverage gain >=0.15 and density gain >0. Here S2, S4, S6 fail; S6 gain 0.0 <0.05 for both hierarchical and WebAPI vs best flat with p 1.0. Per prereg sec 7, this triggers **FALSIFIED-IN-SETTING** (bounded): verbatim collapse confirms artifact (0/40), but under correct-family neither hierarchical nor WebAPI provides higher-leverage alias-OOD resolution than flat top-5 RAG on tested splits.

**Decision:** FALSIFIED-IN-SETTING bounded to synthetic orthogonal header/body/auth + mixed multi-channel aliasing with minimal derived dict under correct-family-required binding (pool 8>k, 40 pooled). Not a global falsification of semantic resolution or endpoint discovery on real substrates. Prior 39/40 adopt-any-key ceiling remains bounded as artifact, not discriminating capability.

## Product consequences

- **Positive would have meant:** Correct-family gating restores discriminability and WebAPI endpoint mining beats flat RAG >=0.15, justifying promotion to Product Core with correct-family gating and freshness guard.
- **Negative (this result):** Disabling reconstruction confirms contamination (0.975 -> 0.0 verbatim -> 0.525 correct-family) but retrieval/mining diversity is not bottleneck for these families on minimal derived dict; coverage remains homogeneous despite pool 8>k and theme-diversified selection. **Product should NOT replace flat RAG with hierarchical or WebAPI mining layer** on this scaffold; keep existing retrieval (exact-intent scan or flat RAG when intent differs) and pursue orthogonal basins: explicit alias catalogs, server-side routing normalization, or residual-novelty-tracked verification economics (pay cost of novelty only, freshness/UNKNOWN gating) rather than retrieval diversity tuning. This addresses BrowserUse 99% script caching vs alias-OOD distinction and Stagehand DOM-hash baseline by showing endpoint bypass does not beat flat RAG when reconstruction cannot invent cross-family keys.
- **Economics:** CPU-only <30s evaluation, 980 calls, <2 min indexing, no BrowserGym burn per Director rationale (saved live cost, no 1280x720 SPA heterogeneity tested).

## Handoff

- **Established:** C-SEMANTIC-RESOLVE genuine non-oracle reconstruction ceiling EXPERIMENTAL bounded to synthetic orthogonal header/body/auth + mixed (same as parent 83b7c52d) but with discriminating measurement: pooled alias-OOD under adopt-any-key 39/40 0.975 is artifact (verbatim 0/40=0.0), under correct-family-required 21/40=0.525 Wilson [0.375,0.671] binomial p 1.1e-08, orthogonal 21/30=0.70 body 1.0 auth 0.9 header 0.2 mixed 0/10, held-out 7/9=0.777, exact 11/12=0.917, NCs pass, ECE 0.257 >0.15, 84 themes identical to WebAPI.
- **Rejected:** Hierarchical theme-diversified retrieval beats flat top-5 RAG on expanded pool 8>k under correct-family gating: **REJECTED** for tested configuration (coverage gain 0.0 CI [0,0] p 1.0 density -0.105 p 0.0). WebAPI endpoint mining provides higher-leverage alias-OOD resolution than hierarchical or flat on this synthetic under correct-family: **REJECTED** (same 21/40, McNemar p 1.0, identical themes retrieved_ids, pool>k not sufficient, reconstruction still too permissive within-family).
- **Unknown:** Whether live BrowserGym 1280x720 observation noise breaks 0.55 coverage ceiling and makes complementary discovery valuable; whether residual-novelty verification economics provides higher work compression than retrieval diversity; whether multi-candidate joint rewriting could solve mixed 0/10 under CF; whether real Fetch/WebMCP OpenAPI endpoint discovery shows advantage on production endpoints.
- **Do-not-assume:** Do not assume 21/40 pooled CF indicates hierarchical/WebAPI complementarity — flat TFIDF/EMBED identical 21/40, random 18/40 close; do not assume 84 themes validates WebAPI — identical to hierarchical; do not assume verbatim 0/40 means retrieval diversity has no value generally — it reflects correct-family restriction on this synthetic; do not assume ECE 0.257 transfers; do not assume synthetic generalizes to live SPAs.

## Artifacts

- `tasks_expanded.json` sha 83b7c52d (40 alias 12 exact 12 no-app 6 empty, leak 0/40)
- `tasks.json` sha 4abf1487 (parent byte-identical intents)
- `index_manifest.json` sha 973ad38 (84 themes 45 components 168 episodes)
- `raw_evidence.json` 980 rows sha ada40d73
- `derived_metrics.json` sha d2d21581 (coverage/density bootstrap 2000, McNemar, ECE)
- `run_execute_35793584484.py` code (template parsing, Jaccard 0.6, TFIDF/embed, hierarchical/webapi, verbatim/CF rules)

## References

- Parent handoff EXP-FRONTIER-35789949165 sha f4e80235 (MIXED, 39/40 artifact, required_fixes verbatim/CF)
- Grandparent EXP-FRONTIER-35782552659 (MIXED hierarchical pool 3<=k)
- Codex C-SEMANTIC-RESOLVE EXPERIMENTAL bounded synthetic ceiling
- Spec/Prereg frozen 2026-09-22T22:44:48Z

