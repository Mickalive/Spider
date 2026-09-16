# EXP-GRAPH-35130682058 preregistration

## 1. Experiment ID and lane
- **experiment_id**: EXP-GRAPH-35130682058
- **lane**: graph
- **claim_ids**: C-FRESHNESS

## 2. Question
Can a multi-signal ensemble combining structural similarity (Jaccard) and temporal response-time (KS statistic) discriminate true schema drift from structural noise with TP>=0.8 and FP<=0.15 on a controlled mock server, when each individual signal family alone fails?

## 3. Hypothesis
A linear discriminant ensemble of (1 - Jaccard) and KS D, with frozen weights learned on a training split of existing raw data, will achieve TP>=0.8 and FP<=0.15 on a held-out test split, demonstrating that orthogonal signals provide complementary discriminative power that no single signal achieves alone.

## 4. Falsifier
No operating point of the ensemble ROC curve achieves both TP>=0.8 and FP<=0.15 on the held-out test split, or the ensemble fails to exceed the best single-signal performance (Jaccard FP=1.0, KS FP=0.1875).

## 5. Baselines
1. Single-signal Jaccard (field_path,type) with adaptive threshold T(n)=1-0.8/(n+1) — FP=1.0 at all sizes (EXP-GRAPH-34788722106)
2. Single-signal KS two-sample test on response-time distributions — TP=0.0, FP=0.1875 (EXP-GRAPH-35083040517)
3. Majority-vote ensemble of Jaccard and KS (both must agree) — expected FP reduction but TP may drop
4. Weighted linear discriminant with frozen coefficients learned on training split

## 6. Positive control
Ensemble must correctly classify all true drift patterns (add_field, remove_field, change_type) as stale on the training split (TP=1.0).

## 7. Null control
Ensemble must correctly classify all fresh copies (identical schemas) as fresh on the training split (FP=0.0).

## 8. Measurement validity
- Raw data from EXP-GRAPH-34788722106 (Jaccard) and EXP-GRAPH-35083040517 (response-time) are from the same mock server with computation-dependent timing (R²=0.9999, +9.3ms/field)
- Schema sizes 10,20,50 are common to both datasets
- Drift patterns are identical across experiments (add_field, remove_field, change_type, optional_field_churn, null_valued_fields, nested_object_variation)
- N=30 per condition per size in both experiments
- Deterministic seed for train/test split (seed=20260916)

## 9. Decision rule
Condition (1): ensemble ROC curve on held-out test split contains an operating point with TP>=0.8 and FP<=0.15.
Condition (2): ensemble TP at that operating point exceeds max(TP_Jaccard, TP_KS) at matching FP.
Condition (3): ensemble FP at that operating point is less than min(FP_Jaccard, FP_KS) at matching TP.
All three conditions must hold for SURVIVES_CURRENT_TEST.

## 10. Product consequence
- Positive: Multi-signal ensemble becomes a candidate freshness detection mechanism for Product Core; triggers end-to-end economics measurement (C-PRODUCT-ECON).
- Negative: Orthogonal signal combination does not rescue discrimination; C-FRESHNESS remains HYPOTHESIS pending fundamentally different signal families (e.g., session token validation, field-usage profiling) or direct schema comparison.

## 11. Expected cost
Low: reanalysis of existing raw data (no new data collection). Compute: O(N * n_signals) where N ~ 900 conditions (3 sizes * 6 patterns * 30 samples).

## 12. Expected information gain
High: if ensemble succeeds, changes product decision (freshness detection becomes viable). If ensemble fails, rules out simple combination of tested signals and redirects to orthogonal approaches.

## 13. Data sources
- `research/experiments/EXP-GRAPH-34788722106/raw_evidence/derived_measurements.json` — Jaccard similarity per condition
- `research/experiments/EXP-GRAPH-35083040517/raw_evidence/response_time_per_condition.json` — KS D per condition
- `research/experiments/EXP-GRAPH-34788722106/raw_evidence/mock_schemas.json` — schema definitions for labeling

## 14. Analysis plan
1. Load both datasets and align on (schema_size, drift_pattern, sample_index).
2. For each condition, compute feature vector: [1 - Jaccard, KS_D].
3. Label each sample as stale (drift pattern in {add_field, remove_field, change_type}) or fresh (fresh copy) or noise (structural noise patterns). Note: fresh copies are not present in the raw data; we will treat each fresh-stale pair as a matched comparison. Actually, the raw data contains per-condition aggregated metrics, not per-sample. We need per-sample data. Check if raw measurements contain per-sample Jaccard and KS D. If not, we cannot compute ROC. We may need to simulate per-sample data from aggregated metrics assuming normal distribution. That's a limitation.

Given the time, I'll adjust the analysis plan: we will use aggregated per-condition metrics to compute approximate ROC by treating each condition as a sample. This is a limitation but acceptable for a proof-of-concept.

Let's update the prereg with this limitation. We'll add a validity note.

I'll edit the prereg again to add a section on limitations. Let's first read the current prereg to see where to add. I'll add after section 14. Let's replace the whole file with a more complete version. Let's write a new prereg.md from scratch. Let's use the write tool.</think><tool_call>
<function=write>
<parameter=filePath>/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35130682058/prereg.md
