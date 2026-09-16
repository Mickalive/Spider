# EXP-GRAPH-35130682058 Report: Multi-signal Ensemble Freshness Detection

## Executive Summary

The multi-signal ensemble combining structural similarity (Jaccard) and temporal response-time (KS D) fails to achieve the preregistered decision criteria on the held-out test split. The ensemble does not contain any operating point with TP≥0.8 and FP≤0.15. The hypothesis that orthogonal signals provide complementary discriminative power that no single signal achieves alone is **FALSIFIED** in this setting.

## Experiment Overview

**Question**: Can a multi-signal ensemble combining structural similarity (Jaccard) and temporal response-time (KS statistic) discriminate true schema drift from structural noise with TP≥0.8 and FP≤0.15 on a controlled mock server, when each individual signal family alone fails?

**Hypothesis**: A linear discriminant ensemble of (1 - Jaccard) and KS D, with frozen weights learned on a training split of existing raw data, will achieve TP≥0.8 and FP≤0.15 on a held-out test split.

**Decision Rule**: All three conditions must hold:
1. Ensemble ROC curve contains an operating point with TP≥0.8 and FP≤0.15
2. Ensemble TP at that operating point exceeds max(TP_Jaccard, TP_KS) at matching FP
3. Ensemble FP at that operating point is less than min(FP_Jaccard, FP_KS) at matching TP

## Raw Evidence

Data sources:
- Jaccard similarity per condition: `research/experiments/EXP-34788722106/raw_evidence/derived_measurements.json`
- Response-time KS D per condition: `research/experiments/EXP-35083040517/raw_evidence/response_time_per_condition.json`

Total conditions: 24 (4 schema sizes × 6 patterns)
- Drift patterns (label=1): 12 (add_field, remove_field, change_type × 4 sizes)
- Noise patterns (label=0): 12 (optional_field_churn, null_valued_fields, nested_object_variation × 4 sizes)

Note: Fresh copies (label=0) are not included in the primary discrimination task.

## Analysis

### Feature Construction

For each condition, two features were computed:
1. **Jaccard divergence**: 1 - mean_jaccard (higher = more structural change)
2. **KS D**: Two-sample Kolmogorov-Smirnov statistic on response-time distributions (higher = more temporal difference)

### Train/Test Split

Deterministic stratified split (seed=20260916):
- Training: 16 conditions (8 drift, 8 noise)
- Test: 8 conditions (4 drift, 4 noise)

### Ensemble Learning

Fisher's Linear Discriminant Analysis (LDA) on training split:
- Weights: w = [-7.14, -1.33]
- Intercept: w0 = 1.14
- Decision rule: classify as drift if w·x + w0 ≥ threshold

The negative weights indicate that both features **inversely** predict drift: higher Jaccard divergence and higher KS D are associated with noise, not drift. This is counterintuitive but reflects the data: noise patterns (especially nested_object_variation) produce larger structural and temporal changes than true drift.

### Results

| Metric | Ensemble | Jaccard | KS D | Majority Vote |
|--------|----------|---------|------|---------------|
| TP (test) | 0.50 | 0.25 | 0.75 | 0.00 |
| FP (test) | 0.00 | 0.25 | 0.50 | 0.25 |
| AUC (test) | 0.625 | - | - | - |

### Decision Rule Evaluation

1. **Condition 1**: ❌ No operating point satisfies TP≥0.8 and FP≤0.15 simultaneously. Best point: TP=0.50, FP=0.00 (threshold=0.46).

2. **Condition 2**: ❌ Not evaluated (Condition 1 fails).

3. **Condition 3**: ❌ Not evaluated (Condition 1 fails).

### Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| Positive control (train) | TP=1.0 | TP=0.25 | ❌ |
| Null control (train) | FP=0.0 | FP=0.0 | ✅ |

The positive control fails: the ensemble correctly classifies only 25% of drift patterns on the training set. This indicates the linear discriminant cannot separate drift from noise in the 2D feature space.

### Single-Signal Baselines

**Jaccard alone**: At best Youden index, TP=0.25, FP=0.25. The adaptive threshold T(n)=1-0.8/(n+1) yields FP=1.0 at all sizes (as established in EXP-GRAPH-34788722106).

**KS D alone**: At best Youden index, TP=0.75, FP=0.50. The KS test detects nested_object_variation (noise) more often than true drift, confirming the inverted direction.

**Majority vote**: Both signals must agree (normalized >0.5). Yields TP=0.0, FP=0.25. The strict agreement requirement eliminates all true drift detections.

## Observations

1. The ensemble weights are inversely signed for both features, indicating that drift patterns have **lower** Jaccard divergence and KS D than noise patterns in this dataset.

2. The ROC AUC of 0.625 is only slightly above random (0.5), confirming minimal discriminative power.

3. Noise patterns (optional_field_churn, null_valued_fields, nested_object_variation) overlap substantially with drift patterns in the 2D feature space.

4. nested_object_variation (noise) consistently produces higher KS D (0.50-0.53) than most drift patterns, making it indistinguishable from drift in the temporal signal.

5. The positive control failure indicates the linear discriminant cannot even separate the training data, let alone generalize.

## Interpretation

The multi-signal ensemble fails to rescue discrimination when each individual signal fails. The root cause is that the two tested signal families (structural Jaccard and temporal KS D) are not complementary in this setting: both are confounded by structural complexity in the same way. Noise patterns that add more fields (nested_object_variation adds 2 fields) produce larger structural and temporal changes than true drift patterns (add_field adds 1 field).

The hypothesis that orthogonal signals provide complementary discriminative power is falsified for these specific signal families. However, the broader question of whether **any** multi-signal ensemble could succeed remains open. The tested signals may not be truly orthogonal: both measure magnitude of structural change, not semantic meaningfulness.

## Product Consequence

**Negative**: Orthogonal signal combination does not rescue discrimination. C-FRESHNESS remains HYPOTHESIS pending fundamentally different signal families (e.g., session token validation, field-usage profiling) or direct schema comparison.

## Limitations

1. **Aggregated data**: Raw data consists of per-condition aggregated metrics (mean Jaccard, KS D), not per-sample measurements. ROC is computed over 24 conditions, not individual samples. This severely limits statistical power.

2. **Tiny test set**: Only 8 test conditions, resulting in coarse ROC curves and limited operating points.

3. **Linear ensemble**: The spec mandates a linear discriminant, which may be insufficient for nonlinear decision boundaries.

4. **Mock server**: Computation-dependent timing (R²=0.9999) confounds temporal signals with structural complexity.

5. **No fresh copies in primary task**: Fresh copies are easily distinguishable but not part of the drift-vs-noise discrimination task.

## Next Steps

1. Test fundamentally different signal families (session tokens, field-usage profiling, direct schema diff)
2. Explore nonlinear ensemble methods (SVM, random forest) on the same features
3. Collect per-sample data to enable proper ROC analysis with sufficient statistical power
4. Consider direct schema comparison as an alternative approach (bypassing indirect signals)

## Conclusion

The multi-signal ensemble of Jaccard and KS D fails to achieve TP≥0.8 and FP≤0.15 on the held-out test split. The hypothesis is falsified in this setting. The graph lane should pivot to orthogonal signal families or direct schema comparison for freshness detection.