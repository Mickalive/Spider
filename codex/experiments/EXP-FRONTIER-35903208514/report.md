# EXP-FRONTIER-35903208514 EXECUTE report

**Lane:** frontier — **status:** COMPLETE — **outcome:** SUPPORTS — **decision_label:** SURVIVES_CURRENT_TEST

## Question
Alias catalog + routing normalization + Fetch/WebMCP OpenAPI discovery + joint multi-candidate CF composition vs hierarchical/flat baselines on frozen fixture sha `83b7c52dd17848fc...` under correct-family gating and honest cost.

## Primary result (JOINT-ALIAS-FETCH)
| metric | value | threshold |
|---|---|---|
| pooled correct | 40/40 = 1.000 | >=0.50 |
| Wilson lower | 0.912 | >0.35 |
| binomial p vs 0.10 | 1e-40 | <0.05 |
| McNemar vs exact p | 2.15e-05 | <0.05 |
| McNemar vs best flat p | 3.64e-05 | <0.05 |
| McNemar vs hier p | 3.64e-05 | <0.05 |
| coverage | 1.000 | >=0.60 |
| coverage gain obs (ci_lo) | 0.250 (0.250) | >=0.10 / lo>0.05 |
| density gain | 0.939 p=0.0005 | >0 p<0.05 |
| header / auth / mixed | 10/10 / 10/10 / 10/10 | >=4 each |
| false_accept rate | 0.000 (gap vs Stagehand 0.450) | <=0.15, gap>=0.15 |
| precision no-applicable | 1.000 | >=0.85 |
| ECE (upper) | 0.116 (0.132) | <=0.15 (<=0.18) |
| amortized $ f=10 | 0.00743 | 0.002–0.092 |

**S1–S6:** {"S1_pooled_wilson_binom_mcnemar": true, "S2_coverage_gain_density": true, "S3_per_family_header_auth_mixed": true, "S4_false_accept_precision": true, "S5_ece": true, "S6_economics": true}

## Controls
All controls pass: **True**. See `result.controls` keyed by stable PC/NC ids.

## Interpretation
Controls passed and JOINT-ALIAS-FETCH met S1–S6: factorization + joint composition **supports** the frozen hypothesis on this synthetic CF substrate (bounded).

## Product consequence (frozen)
- Positive path: prioritize explicit alias catalogs + routing + joint composition over retrieval diversity for these families (only if SURVIVES).
- Negative path: do **not** add alias/routing/joint Fetch layer as higher-leverage; keep flat RAG/exact and pursue orthogonal basins.

## Artifacts
- raw_evidence.json (per-task per-pipeline outcomes, counters, honest_cost)
- derived_metrics.json, alias_catalog_manifest.json, routing_manifest.json, fetch_manifest.json, joint_manifest.json, index_manifest.json
- provenance.json (commits, census, hashes, harness_errors)

## Validity
See `validity_notes` in result.json. Live BrowserGym unavailable; embed unavailable; claim bounded to synthetic fixture families.
