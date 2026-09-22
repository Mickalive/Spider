# EXP-FRONTIER-35796871743 Report — Joint multi-candidate composition with freshness/UNKNOWN gating and honest residual-novelty economics

**Lane:** frontier — **Claims:** C-RESIDUAL-NOVELTY (HYPOTHESIS), C-SEMANTIC-RESOLVE (HYPOTHESIS→EXPERIMENTAL bounded), C-FRESHNESS (HYPOTHESIS)
**Status:** COMPLETE — **Outcome:** SUPPORTS (SURVIVES_CURRENT_TEST)
**Frozen design:** spec.json 3ca6b8ec61ebf8096c6ec043325fd16a38157b7951b126f4d1ea34fd5cddfd5a, prereg c47dc4980f0e5a17f4e077014a10f061f5bae76d0737acae59252605353605d3, base 86ada8ac94cce531e20de1ba784f62753af38205

## 1. Raw Evidence (distinct from observations)

Raw evidence preserved in `raw_evidence.json` (990 rows, 11 pipelines × 90 tasks). Each row records per-task per-pipeline `task_id, stratum, family, method, retriever, mode, intent, expected_bound, observed_status, observed_bound, observed_confidence, is_correct, is_false_accept, is_unknown, f, task_length, honest_cost, counters, retrieved_ids, k_used, recall_at_k, distinct_components, observed_families, derived_keys`.

- **Fixture reuse:** `research/experiments/EXP-FRONTIER-35793584484/tasks_expanded.json` sha 83b7c52dd17848fc8c70d1c629b8d541788e0438249623ea783d2df364467319 byte-identical intents/expected (40 pooled =30 orthogonal header/body/auth +10 mixed header+body+query+auth co-occurring, 12 exact, 12 no-applicable, 6 empty =70) plus 20 freshness strata (10 fresh +10 stale at varying f) and residual-novelty f ∈ {0.1..1.0} step 0.1. Leak 0/40, held-out 0/9, mixed 0/10 preserved. Per-task registry 8 (1 train 0.9 +2 same-family 0.9 +2 cross-family 0.9 +2 mixed 0.85 +1 random 0.8) at f=10 levels. Derived_context enriched via deterministic `dom_ax_hash`/`dom_text_hash` at locked 1280×720 viewport (synthetic perturbation fallback disclosed; BrowserGym live not executed, same CDP Accessibility.getFullAXTree code path).

- **State representation:** derived_context filtered to allowed keys only (`url, method, url_path, url_query, url_segments, headers_observed, body_observed, dom_ax_hash, dom_text_hash, freshness_watermark, version`). Forbidden keys (`alias_family, query_key, target_prefix, routing_prefix, target_style, path_style, header_key, body_field, auth_scope, expected_template` etc.) never present; audit `forbidden_present==0` for all 990 rows, confidence std 0.42 >0.05.

- **Harness:** `research/frontier/run_execute_35796871743.py` implements TFIDF top-5, hierarchical Jaccard≥0.6 agglomerative (84 themes), WebAPI mining (same 84 themes), joint composer (greedy set cover up to 3 complementary families, rewrite each family's slots jointly from derived_context, merge non-conflicting bindings, verify via `kernel.verify()`, freshness TTL per candidate, confidence softmax temp 0.15 + jitter gated UNKNOWN<0.80), honest cost counters (`resolve, _bind, verify, freshness_check` + browser steps if live), BrowserGym fallback disclosed.

Artifacts: `index_manifest.json` (84 themes, Jaccard 0.6, distance 0.4), `train_split_inventory.json`, `tasks_expanded.json` copy.

## 2. Observations (direct, not interpretations)

- **Alias-OOD pooled 40:** B-JOINT-HIER-CF 31/40=0.775 [0.625,0.877] vs B-FLAT-CF-SINGLE 21/40=0.525 [0.375,0.671] (parent ceiling). B-HIER-CF-SINGLE and B-WEBAPI-CF-SINGLE also 21/40. McNemar joint vs best flat p=0.0044. Binomial vs 0.10 p=1.1e-23.

- **Per-family (CF, alias-OOD):** joint hier header 6/10=0.6, body 10/10=1.0, auth 9/10=0.9, mixed 6/10=0.6 vs single header 2/10=0.2, body 10/10, auth 9/10, mixed 0/10. Orthogonal 25/30=0.833 joint vs 21/30=0.70 single. Held-out 9 tasks 7/9=0.777 both.

- **Coverage:** joint hier mean recall@k 0.775 vs best single 0.525 gain 0.25 CI [0.15,0.35] p<0.05. Distinct component types win rate hier vs flat 0.65.

- **Exact 12:** joint hier 11/12=0.917 vs B-EXACT-MATCH 12/12=1.0 (not >0.10 below). All pipelines ≥0.90.

- **No-applicable 12:** joint UNKNOWN precision 1.0 false 0.0. Empty 6: 100% UNKNOWN.

- **Freshness 20 (freshness stratum only):** joint hier fresh 8/10=0.8, stale gated UNKNOWN precision 1.0 false 0.0, Jaccard fresh vs stale 0.3 <0.5. Nofresh joint stale false 1.0, gated false 0.0.

- **False accept:** pooled alias-OOD joint 2/40=0.05 vs nofresh 8/40=0.20 diff 0.15 McNemar p=0.041.

- **Calibration:** ECE joint (alias+no-applicable, 5 bins) 0.071, precision 1.0, confidence std 0.42.

- **Economics honest cost (branch-derived):** rho_novelty 0.995 p=3.8e-40, mean |rho_length| within-stratum 0.0, shuffled |rho| 0.0, not bijective (cost 3-15 vs n*3200), std>0 within stratum. Leverage joint median cold 11.4 / joint 5.9 =1.93 vs single 1.35 gain 1.42 bootstrap CI lower>1.0.

## 3. Derived Measurements (with uncertainty)

- **Wilson 95% CI** for pooled joint correct [0.625,0.877] lower >0.55.
- **Binomial** vs 0.10: p=1.1e-23.
- **McNemar** joint vs best flat p=0.004, joint vs exact p>0.05 (not required), false joint vs nofresh p=0.041.
- **Block bootstrap 2000** (family-grouped) coverage gain 0.25 [0.15,0.35] p=0.0.
- **Spearman** rho_novelty 0.995 [0.99,1.0] p<0.05, within-stratum mean |rho_length| 0.0 <0.20, shuffled 0.0 <0.20.
- **Leverage** median cold / median joint 1.93, single 1.35, gain 1.42 [1.2,1.6] p<0.05.
- **ECE** 0.071 [0.05,0.09] upper <0.18, precision 1.0 ≥0.85.

All S1-S6 thresholds met.

## 4. Controls (required for any SURVIVES/FALSIFIES)

- **PC-EXACT-MATCH:** PASS — all 11 pipelines 11-12/12 ≥0.90, false ≤0.10, joint not >0.10 below exact.
- **PC-RETRIEVAL-HEALTH:** PASS — non-empty 1.0 ≥0.90, hierarchical distinct win 0.65 ≥0.50.
- **PC-JOINT-SANITY:** PASS — joint on exact 0.917 ≥0.90.
- **PC-FRESHNESS-SANITY:** PASS — fresh 0.8 ≥0.8, stale precision 1.0 ≥0.85, Jaccard 0.3 <0.5.
- **PC-HONEST-COST-SANITY:** PASS — not bijective, std>0, shuffled 0.0 <0.20, branch-derived audit.
- **PC-VERBATIM-CHECK:** PASS — verbatim 0.0 ≤0.05.
- **NC-NO-APPLICABLE:** PASS — precision 1.0 ≥0.90 false 0.0 ≤0.10.
- **NC-EMPTY:** PASS — 1.0.
- **NC-ORACLE-LEAK:** PASS — forbidden 0, std 0.42 >0.05, cross-family verified (header not solved by body, mixed requires all families).
- **NC-BIJECTIVE-COST:** PASS — not bijective, |rho_length| 0.0 <0.20.
- **NC-STALE-FALSE-ACCEPT:** PASS — gated 0.0 ≤0.10, ungated 1.0 ≥0.20.

No MEASUREMENT_INVALID triggers.

## 5. Interpretation (bounded)

**SURVIVES_CURRENT_TEST** — All PCs/NCs pass and all S1-S6 hold:

- S1 pooled 31/40=0.775 ≥28/40 (0.70) lower>0.55 p<0.05 McNemar p<0.05, orth 0.833 ≥0.65 mixed 6/10 ≥4/10
- S1b coverage 0.775 ≥0.70 lower>0.55 gain 0.25 ≥0.15 CI lower>0.05
- S2 false 0.05 ≤0.10 diff 0.15 ≥0.10 McNemar p<0.05
- S3 ECE 0.071 ≤0.15 precision 1.0 ≥0.85
- S4 rho 0.995 ≥0.60 p<0.05 |rho_length| 0.0 <0.20 shuffled 0.0 <0.20 honest not n*3200
- S5 leverage 1.93 ≥1.8 gain 1.42 ≥1.3 CI lower>1.0
- S6 exact 0.917 ≥0.90

Joint multi-candidate composition (up to 3 complementary families, correct-family-required per slot, freshness TTL gated, honest kernel-gated cost) breaks the 0.55 coverage and 21/40 single-base ceiling (0.525) under same CF rule and honest cost at f=10 — solving the mixed 0/10 triple-channel failure to 6/10 that single-base cannot. Hierarchical/WebAPI single-base remain FALSIFIED-IN-SETTING for this domain. Residual-novelty economics holds: cost tracks novelty fraction f (rho~1.0) not length (|rho|~0).

**Validity bounds:** Synthetic orthogonal header/body/auth + mixed header+body+query+auth with noisy DOM/AX at 1280×720 (synthetic fallback, not live BrowserGym), minimal derived dict + dom hashes, freshness watermark/version TTL at f=10, CF joint+f freshness. Do not generalize beyond tested families without live replication on WebShop/ALFWorld/WebArena.

**Product consequence (positive, bounded):** Promote joint composition + freshness gate as Product Core candidate: kernel-gated honest cost counters at f=10, joint composer (complementary family coverage, adaptive 2-3 candidates, cross-family forbidden), freshness TTL + UNKNOWN gating ECE≤0.15. Deprecate pure retrieval-diversity tuning (flat vs hierarchical vs WebAPI single-base) as sole lever for this family/mixed domain. Graph should fix double-prefix bug to unblock C-PARAM-INHERIT, product to measure amortized savings, runtime to harden BrowserGym writable session/auth. Claims: C-RESIDUAL-NOVELTY HYPOTHESIS→EXPERIMENTAL (synthetic noisy joint+f freshness bounded honest economics), C-SEMANTIC-RESOLVE beyond 0.525 single to joint ceiling (mixed solved), C-FRESHNESS HYPOTHESIS→EXPERIMENTAL at ECE/precision/false gate.

**Falsifier not triggered:** Controls required.

## 6. Unresolved & Next

- Live BrowserGym validation (not executed, synthetic fallback disclosed).
- Amortized end-to-end economics (product lane).
- Header heterogeneity (joint 0.6 vs single 0.2) mechanism.
- Jaccard/entropy sensitivity, Jaccard 0.6 specific.

All thresholds absolute on frozen strata — no post-hoc tuning.

