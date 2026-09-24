# EXP-FRONTIER-35937602723 — EXECUTE report (frontier, C-SEMANTIC-RESOLVE)

**status:** COMPLETE — **outcome:** SUPPORTS

## Pooled alias-OOD (n=40)
| pipeline | correct | false accept | unknown | rate |
|---|---|---|---|---|
| B-EXACT-MATCH-CF | 20 | 20 | 0 | 0.500 |
| B-FLAT-TFIDF-K5-CF | 20 | 20 | 0 | 0.500 |
| H-HIERARCHICAL-CF | 20 | 20 | 0 | 0.500 |
| B-ENDPOINT-CATALOG-CF | 20 | 20 | 0 | 0.500 |
| B-JOINT-ALIAS-ROUTING-CF | 40 | 0 | 0 | 1.000 |
| B-RANDOM-K5-CF | 11 | 29 | 0 | 0.275 |
| B-STAGEHAND | 0 | 0 | 40 | 0.000 |

## S1-S6 decision
| gate | requirement (frozen) | observed | pass |
|---|---|---|---|
| S1 pooled | joint>=0.60, Wilson lower>0.35, binom p<0.05, McNemar<0.05 | 1.0 / 0.9124 / 1.00e-40 / {'B-EXACT-MATCH-CF': {'b': 20, 'c': 0, 'p': 1.91e-06}, 'B-FLAT-TFIDF-K5-CF': {'b': 20, 'c': 0, 'p': 1.91e-06}, 'H-HIERARCHICAL-CF': {'b': 20, 'c': 0, 'p': 1.91e-06}, 'B-ENDPOINT-CATALOG-CF': {'b': 20, 'c': 0, 'p': 1.91e-06}} | True |
| S2 coverage | >=0.60, gain>=0.10, bs lower>0.05, perm p<0.05 | 1.0 / 0.5 / 0.5 / 0.005 | True |
| S3 family | header>=4/10 mixed>=4/10 | 1.0 / 1.0 (auth diag 1.0) | True |
| S4 false | <=0.15, precision>=0.85 | 0.0 / 1.0 | True |
| S5 ECE | <=0.15, bs upper<=0.18 | 0.0895 / 0.1096 | True |
| S6 cost | joint<=2x strong baselines, amortized in [0.002,0.092] | {'B-FLAT-TFIDF-K5-CF': 1.605, 'H-HIERARCHICAL-CF': 1.904, 'B-ENDPOINT-CATALOG-CF': 1.904} / 0.056616 (vs exact diag {'B-EXACT-MATCH-CF': 2.341}) | True |

## Controls (frozen IDs)
| id | expected | observed | verdict |
|---|---|---|---|
| PC-EXACT-MATCH | rate>=0.90 false<=0.10 on exact-match stratum | {"false": 0, "rate": 1.0} | PASS |
| PC-ALIAS-CATALOG-BUILT | Jaccard>=0.6 classes, families covered (header/auth/body/query), distinct manifest | {"catalog_size": 13, "classes": 13, "families_covered": ["body", "header_auth", "header_token", "query"], "min_pairwise_jaccard_per_class": [0.0]} | PASS |
| PC-ENDPOINT-CATALOG | centroids>=6, Jaccard>=0.6 clustered, nonempty | {"n_centroids": 51, "nonempty": 51} | PASS |
| PC-HIERARCHICAL | themes>=3, episodes==registry size | {"n_episodes": 168, "n_themes": 84} | PASS |
| PC-FLAT-HEALTH | retrieval non-empty>=90%, distinct across retrievers>=50% | {"distinct": "40/40", "empty": "0/40"} | PASS |
| PC-OPENAPI-SYNTHETIC | spec fetch 200 parsed for joint tasks | {"paths": 14, "spec_200": 52, "spec_non_200": 0} | PASS |
| PC-ROUTING-DIFF | before!=after >=8 pairs, task-relevant fraction computed | {"diff_pairs": 10, "task_relevant_frac": 0.525} | PASS |
| PC-HONEST-COST-SANITY | all pipelines |rho_shuffled|<0.20, within-f std>0, not n*3200, cost==sum counters | {"B-ENDPOINT-CATALOG-CF": {"perm_p": 0.3035, "rho": 0.1583, "within_std": {"0": 0.775, "1": 0.9, "2": 0.458, "3": 1.044}}, "B-EXACT-MATCH-CF": {"perm_p": 0.3582, "rho": 0.1583, "within_std": {"0": 0.775, "1": 0.9, "2": 0.458, "3": 1.044}}, "B-FLAT-TFIDF-K5-CF": {"perm_p": 0.3035, "rho": 0.1583, "within_std": {"0": 0.775, "1": 0.9, "2": 0.458, "3": 1.044}}, "B-JOINT-ALIAS-ROUTING-CF": {"perm_p": 1.0, "rho": 0.0, "within_std": {"0": 1.428, "1": 0.9, "2": 0.781, "3": 1.044}}, "B-RANDOM-K5-CF": {"perm_p": 0.3582, "rho": 0.155, "within_std": {"0": 0.775, "1": 0.9, "2": 0.7, "3": 1.044}}, "B-STAGEHAND": {"perm_p": 1.0, "rho": 0.0, "within_std": {"0": 0.775, "1": 0.9, "2": 0.458, "3": 1.044}}, "H-HIERARCHICAL-CF": {"perm_p": 0.3383, "rho": 0.1583, "within_std": {"0": 0.775, "1": 0.9, "2": 0.458, "3": 1.044}}} | PASS |
| PC-CONFIDENCE-DERIVED | derived pipelines conf std>0.05 | {"B-ENDPOINT-CATALOG-CF": 0.0582, "B-FLAT-TFIDF-K5-CF": 0.0583, "B-JOINT-ALIAS-ROUTING-CF": 0.0648, "H-HIERARCHICAL-CF": 0.0582} | PASS |
| PC-FRESHNESS-NONCIRCULAR | freshness constant per task, never depends on outcome | {"freshness_total_per_pipeline": {"B-ENDPOINT-CATALOG-CF": 40, "B-EXACT-MATCH-CF": 40, "B-FLAT-TFIDF-K5-CF": 40, "B-JOINT-ALIAS-ROUTING-CF": 40, "B-RANDOM-K5-CF": 40, "B-STAGEHAND": 40, "H-HIERARCHICAL-CF": 40}} | PASS |
| NC-NO-APPLICABLE | all pipelines unknown_precision>=0.85 false<=0.15 on no-applicable | {"B-ENDPOINT-CATALOG-CF": {"false": 0, "precision": 1.0}, "B-EXACT-MATCH-CF": {"false": 0, "precision": 1.0}, "B-FLAT-TFIDF-K5-CF": {"false": 0, "precision": 1.0}, "B-JOINT-ALIAS-ROUTING-CF": {"false": 0, "precision": 1.0}, "B-RANDOM-K5-CF": {"false": 0, "precision": 1.0}, "B-STAGEHAND": {"false": 0, "precision": 1.0}, "H-HIERARCHICAL-CF": {"false": 0, "precision": 1.0}} | PASS |
| NC-EMPTY | all pipelines 100% UNKNOWN on empty-registry | {"B-ENDPOINT-CATALOG-CF": 1.0, "B-EXACT-MATCH-CF": 1.0, "B-FLAT-TFIDF-K5-CF": 1.0, "B-JOINT-ALIAS-ROUTING-CF": 1.0, "B-RANDOM-K5-CF": 1.0, "B-STAGEHAND": 1.0, "H-HIERARCHICAL-CF": 1.0} | PASS |
| NC-ORACLE-LEAK | forbidden-key reads 0, registry leak 0/40 on discriminating tasks | {"exact_stratum_registry_equals_expected_control_design": 12, "forbidden_key_reads": 0, "registry_leak_tasks_discriminating": 0} | PASS |
| NC-BIJECTIVE-COST | honest_cost never equals n*3200, no jitter counters | {"browser_steps_all_zero": true, "max_proxy_hits": 0} | PASS |
| NC-STAGEHAND | stagehand 0/40 on alias-OOD | {"correct": 0, "unknown": 40} | PASS |

## Adequacy && interpretation
- adequacy_pass=True; harness_errors=0/40; leak forbidden_reads=0, discriminating_registry_leak=0/40 (exact stratum control design: 12/12)
- SUPPORTS: joint composition (greedy set-cover, min-2 distinct, alias routing, adoption) rescues pooled 1.00 vs single-candidate ceiling 0.50, non-vacuously (complementary_frac mean 1.0, k={2: 30, 3: 10}).
- Synthetic saturation disclosed; live hetero question remains open (frozen deferral).
- Economics: build_units=28308, amortized $0.056616/task at f=10 (modeled, disclosed).

## Artifacts
- `research/experiments/EXP-FRONTIER-35937602723/raw_evidence.json` sha256 `3d8c2fe7ec4b9b61d00835b5171c6a196e4911649ba9e57bd3f3b1e9a6e385f9` (raw)
- `research/experiments/EXP-FRONTIER-35937602723/derived_metrics.json` sha256 `d0b1abe3113974e229848e94a406138fff2a9ae83381fa6c574004ef1cdb655e` (derived)
- `research/experiments/EXP-FRONTIER-35937602723/alias_catalog_manifest.json` sha256 `261d361d133580ee0cb9969689548879a044e81cee7d930b6581eb62cc602b5a` (derived)
- `research/experiments/EXP-FRONTIER-35937602723/endpoint_catalog_manifest.json` sha256 `a9695ab2511767140eb23deb0a70fd8f84084f0d9d51ac9cfea3754c36d3227a` (derived)
- `research/experiments/EXP-FRONTIER-35937602723/hierarchical_manifest.json` sha256 `efb5c35190efecd9125362afece798050b1bdc62f899335fcd57486f2e0d5fe7` (derived)
- `research/experiments/EXP-FRONTIER-35937602723/routing_manifest.json` sha256 `56d41d07df012911eb0cb3004619358aaef3d4b23e1f1eaafc6ec0f6cee63cd4` (derived)
- `research/experiments/EXP-FRONTIER-35937602723/index_manifest.json` sha256 `7064dab6a444ac8f9e33fbf6c67f7ddcefb0a1fcf461da6ce1e05e7b05073c34` (derived)
- `research/experiments/EXP-FRONTIER-35937602723/train_split_inventory.json` sha256 `ea8fcedcc7e1754aeded7a3aebb6466ac5c68d47cec293320543d11d093b2772` (derived)
- `research/experiments/EXP-FRONTIER-35937602723/joint_manifest.json` sha256 `512b60d308ef728a540202b8c571bf457178bd372fd5912ce1a81561b6328c44` (derived)
- `research/experiments/EXP-FRONTIER-35937602723/fetch_manifest.json` sha256 `ba095b77f648ee7c718b23adec1ec936aac95f6a842ca212fd04b4d1ef5a41af` (evidence)
- `research/experiments/EXP-FRONTIER-35937602723/freeze.json` sha256 `062233f0db7b5558f907636a110590e750d5359206332935aa8e0c15d0884351` (fixture)
