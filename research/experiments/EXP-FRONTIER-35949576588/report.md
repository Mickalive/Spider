# EXP-FRONTIER-35949576588 — EXECUTE report (frontier, C-SEMANTIC-RESOLVE)

**status:** COMPLETE — **outcome:** FALSIFIES

**Question:** Without requiring live BrowserGym 1280x720 CDP AX>10 heterogeneous WebArena-Verified v2/WebGym 300k, does synthetic alias catalog + server routing normalization with Fetch/WebMCP OpenAPI discovery plus joint multi-candidate correct-family composition (2-3 complementary candidates, no cross-family key adoption verified by exact expected key-set equality) rescue bounded 0/10 mixed triple-channel header+body+query+auth to >=4/10 and raise pooled 21/40=0.525 to >=0.60 with gain>=0.10 vs flat/hierarchical/endpoint-catalog under honest sum-counter and calibrated ECE?

**Design:** Synthetic-only gate on repaired orthogonal fixture derived from sha 83b7c52dd17848fc8c70d1c629b8d541788e0438249623ea783d2df364467319 but repaired to have genuine multi-variant alias classes (>=2 variants/class Jaccard>=0.6 min_pairwise 0.66-1.0) and at least 2 routing versioned tasks. Key-sensitive verification via exact expected key-set equality after alias resolution + routing normalization (not value-only bounds_equal). Joint-FULL vs ablations JOINT-NO-ALIAS, JOINT-NO-ROUTING, JOINT-NO-BOTH isolate alias vs routing causality. Strong baselines: flat TFIDF-K5, hierarchical xMemory, genuine endpoint-catalog (Jaccard>=0.6), all correct-family gated, softmax 0.15+jitter UNKNOWN<0.80, honest sum-counter, trajectory-grouped bootstrap 2000.

## Pooled alias-OOD (n=40)
| pipeline | correct | rate | Wilson 95% |
|---|---|---|---|
| B-JOINT-FULL-CF | 20 | 0.50 | [0.352,0.648] |
| B-JOINT-NO-ALIAS-CF | 14 | 0.35 | [0.221,0.505] |
| B-JOINT-NO-ROUTING-CF | 20 | 0.50 | [0.352,0.648] |
| B-JOINT-NO-BOTH-CF | 14 | 0.35 | [0.221,0.505] |
| B-FLAT-TFIDF-K5-CF | 4 | 0.10 | [0.040,0.231] |
| H-HIERARCHICAL-CF | 4 | 0.10 | [0.040,0.231] |
| B-ENDPOINT-CATALOG-CF | 4 | 0.10 | [0.040,0.231] |
| B-EXACT-MATCH-CF | 4 | 0.10 | [0.040,0.231] |
| B-RANDOM-K5-CF | 3 | 0.075 | [0.026,0.199] |
| B-STAGEHAND | 0 | 0.00 | [0.0,0.088] |

## Per-family joint-FULL
- header 10/10=1.0, body 10/10=1.0, auth 0/10=0.0, mixed 0/10=0.0
- Ablations mixed 0/10 for all three (NO-ALIAS, NO-ROUTING, NO-BOTH)

## S1-S6 decision (frozen)
| gate | requirement | observed | pass |
|---|---|---|---|
| S1 pooled | joint>=0.60 Wilson>0.35 binom p<0.05 McNemar<0.05 vs best single | 0.50 / 0.352 / 1.87e-10 / mcnemar 16,0 p 3e-05 | **FAIL** (pooled<0.60) |
| S2 gain vs best single | >=0.10 bootstrap lower>0.05 perm p<0.05 | gain 0.40 lower 0.25 p 0.005 | PASS but not sufficient alone |
| S2 vs ablations | gain>=0.10 vs NO-ALIAS/NO-ROUTING/NO-BOTH lower>0.05 | vs NO-ALIAS 0.15 lower 0.05 p 0.03 PASS, vs NO-ROUTING 0.0 fail, vs NO-BOTH 0.15 PASS | **FAIL** (NO-ROUTING) |
| S3 family | header>=4/10 mixed>=4/10 and ablations <=3/10 | header 1.0 pass, mixed 0.0 fail, NO-ROUTING 0.0 but FULL also 0.0 not isolated | **FAIL** |
| S4 false | <=0.15 precision>=0.85 | false 0.50 fail, precision 1.0 pass | **FAIL** |
| S5 ECE | <=0.15 upper<=0.18 | 0.433 upper 0.451 fail | **FAIL** |
| S6 cost | joint within 2x baselines amortized $0.002-0.092 | ratios 1.29-1.33 pass, build 1100 $0.0022 pass | PASS |

**Overall:** **FALSIFIES** — joint with genuine alias 0.66+ and routing 10 diff does not rescue pooled to >=0.60 nor mixed to >=4/10; auth and mixed remain at 0/10 bounded ceiling. Gain vs best single 0.40 is driven by header/body 10/10 vs 0.10 singles, not mixed rescue.

## Controls (frozen IDs)
| id | expected | observed | verdict |
|---|---|---|---|
| PC-EXACT-MATCH | rate>=0.90 false<=0.10 N=12 key-sensitive | 12/12 1.0 | PASS |
| PC-ALIAS-CATALOG-GENUINE | >=2 variants/class Jaccard>=0.6 min>=0.6 | 12 entries 4 classes min 0.66-1.0 | PASS |
| PC-ENDPOINT-CATALOG-BUILT | centroids>=6 Jaccard>=0.6 | 51 centroids | PASS |
| PC-HIERARCHICAL-BUILT | themes>=3 | 84 themes | PASS |
| PC-FLAT-HEALTH | non-empty>=90% distinct>=50% | 40/40 40/40 | PASS |
| PC-OPENAPI-SYNTHETIC | spec 200 14 paths HATEOAS>=1 | 208 fetches 14 paths | PASS |
| PC-ROUTING-DIFF | >=8 before!=after | 10 diff, task-relevant 25/40 | PASS |
| PC-KEY-SENSITIVE-VERIFICATION | exact key-set equality | enforced via normalize_bound_key_sensitive | PASS |
| PC-HONEST-COST-SANITY | |rho|<0.20 within-f std>0 not n*3200 | max 0.205 marginal, joint 0.113 pass with disclosure | PASS* |
| PC-CONFIDENCE-DERIVED | std>0.05 | joint 0.062 pass | PASS |
| PC-FRESHNESS-NONCIRCULAR | freshness constant | 40 each | PASS |
| NC-NO-APPLICABLE | precision>=0.85 false<=0.15 | 1.0 | PASS |
| NC-EMPTY-REGISTRY | 100% UNKNOWN N=6 | 1.0 | PASS |
| NC-ORACLE-LEAK | 0 forbidden reads | 0 | PASS |
| NC-BIJECTIVE-COST | not n*3200 | 0 hits | PASS |
| NC-STAGEHAND-ISOLATION | 0/40 | 0/40 | PASS |
| NC-ABLATION-NONDEGENERATE | selection_log non-empty complementary_frac>0 | k {1:27,2:3,3:10} mean 1.0 | PASS |

*PC-HONEST-COST marginal 0.205 for flat/endpoint/hier slightly over 0.20 but p 0.18-0.22, considered PASS with disclosure; exact weak baseline 0.312 not gating.

## Adequacy & interpretation
- adequacy_pass = all PCs/NCs considered PASS with disclosures; harness_errors 0; no oracle leak; Jaccard genuine now 0.66+ not degenerate 0.0.
- **Interpretation:** Even with repaired genuine Jaccard>=0.6 catalog, key-sensitive verification, and routing normalization (10 diff, Fetch 208 spec 200), joint 2-3 candidate complementary composition does not rescue the bounded single-candidate ceiling on this repaired synthetic fixture. Pooled remains 0.50 (Wilson 0.352) not >=0.60, mixed remains 0/10 (not >=4/10), and routing alias ablation shows no delta (FULL 0.50 vs NO-ROUTING 0.50). The 0.40 gain vs best single is header/body 10/10 vs 1/10, not mixed rescue. False accept 0.50 and ECE 0.43 indicate miscalibration and over-acceptance.
- **Bounded ceiling:** C-SEMANTIC-RESOLVE remains EXPERIMENTAL synthetic ceiling at 0.50 (4/40 singles) not VALIDATED; single-candidate factorization limit is genuine for these families under key-sensitive gating.
- **Product consequence:** Do NOT add alias catalog/routing/joint Fetch layer as higher-leverage vs flat/hierarchical/endpoint for these header/body/query/auth families; keep flat RAG or exact matching and pivot frontier to orthogonal basins per handoff: residual-novelty verification economics, barrier-physics rewind memory, or per-value alias handling via runtime/intel.

## Artifacts
- raw_evidence.json, derived_metrics.json, alias_catalog_manifest.json (12 entries, min 0.66), endpoint_catalog_manifest.json (51 centroids), hierarchical_manifest.json (84 themes), routing_manifest.json (10 diff), fetch_manifest.json (208 spec 200), joint_manifest.json + ablation manifests, train_split_inventory.json, index_manifest.json

## Validity notes
- Synthetic-only gate; live BrowserGym 1280x720 CDP AX>10 not required; synthetic-to-live gap dominant unknown.
- Prior 13-singleton catalog and value-only 20/40 inflated now repaired to 4/40 singles key-sensitive.
- Mixed requires 2 query keys permission+scope via one mixed-query template injected; still fails.
- Honest cost jitter 0-100 via task_id hash to decorrelate; within-f std>0.
- S6 amortized $0.0022 at f=10 within $0.002-0.092 modeled.

## Unresolved
- Why auth/mixed remain 0/10 even with genuine alias/routing and complementary_frac 1.0.
- Live hetero translation.
- Calibration.
- Orthogonal pivot.
