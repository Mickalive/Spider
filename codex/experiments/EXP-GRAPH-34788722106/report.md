# EXP-GRAPH-34788722106 — Adaptive Jaccard Threshold under Structural Noise

## Executive Summary

**Verdict: FALSIFIED-IN-SETTING**

The adaptive Jaccard freshness threshold T(n)=1-0.8/(n+1) achieves perfect true-drift detection (TP=100%) but produces 100% false positive rate on all structural noise patterns at all schema sizes. The frozen decision rule requires FP upper CI ≤ 0.15; observed FP upper CI = 1.0. The hypothesis that the adaptive threshold can reject structural noise is falsified in this setting.

## 1. Experiment Design

### 1.1 Question
Does adaptive Jaccard freshness threshold T(n)=1-0.8/(n+1) achieve TP≥0.8 and FP≤0.15 under structural noise (optional field churn, null-valued fields, nested object variation) on schemas with 10-50 fields?

### 1.2 Setup
- **Schema sizes**: 10, 20, 30, 50 fields
- **Samples**: 30 fresh + 30 stale per drift pattern per size
- **True drift patterns**: add_field, remove_field, change_type
- **Structural noise patterns**: optional_field_churn (10% add/remove), null_valued_fields (random fields set to null), nested_object_variation (convert field to nested object)
- **Jaccard representation**: (field_path, type) pairs
- **Threshold**: T(n) = 1 - 0.8/(n+1)

## 2. Results

### 2.1 True Drift Detection (TP)
**PASSES all criteria.**

| Schema Size | Threshold | TP Rate | 95% CI Lower | Add-field Margin | Remove-field Margin | Change-type Margin |
|-------------|-----------|---------|--------------|------------------|--------------------|--------------------|
| 10          | 0.9273    | 1.000   | 0.8865       | 0.0182           | 0.0273             | 0.1091             |
| 20          | 0.9619    | 1.000   | 0.8865       | 0.0095           | 0.0119             | 0.0571             |
| 30          | 0.9742    | 1.000   | 0.8865       | 0.0065           | 0.0075             | 0.0387             |
| 50          | 0.9843    | 1.000   | 0.8865       | 0.0039           | 0.0043             | 0.0235             |

- **Overall**: TP=360/360=1.0, CI=[0.9894, 1.0]
- All Wilson CI lower bounds ≥ 0.8865 > 0.8 threshold
- Detection margin positive for all patterns at all sizes

### 2.2 Fresh Response FP (Null Control)
**PASSES all criteria.**

- **Overall**: FP=0/120=0.0, CI=[0.0, 0.031]
- Fresh responses have Jaccard=1.0 by construction (identical field sets)
- No false alarms at any schema size

### 2.3 Structural Noise FP
**FAILS all criteria.**

| Schema Size | Noise Pattern | FP Rate | 95% CI Upper | Mean Jaccard | Threshold |
|-------------|---------------|---------|--------------|--------------|-----------|
| 10          | optional_churn | 1.000 | 1.0000 | 0.8182 | 0.9273 |
| 10          | null_fields    | 1.000 | 1.0000 | 0.8182 | 0.9273 |
| 10          | nested_object  | 1.000 | 1.0000 | 0.8182 | 0.9273 |
| 20          | optional_churn | 1.000 | 1.0000 | 0.8182 | 0.9619 |
| 20          | null_fields    | 1.000 | 1.0000 | 0.8571 | 0.9619 |
| 20          | nested_object  | 1.000 | 1.0000 | 0.9048 | 0.9619 |
| 30          | optional_churn | 1.000 | 1.0000 | 0.8182 | 0.9742 |
| 30          | null_fields    | 1.000 | 1.0000 | 0.8710 | 0.9742 |
| 30          | nested_object  | 1.000 | 1.0000 | 0.9355 | 0.9742 |
| 50          | optional_churn | 1.000 | 1.0000 | 0.8182 | 0.9843 |
| 50          | null_fields    | 1.000 | 1.0000 | 0.8824 | 0.9843 |
| 50          | nested_object  | 1.000 | 1.0000 | 0.9608 | 0.9843 |

- **12 violations** of the frozen decision rule (FP CI upper > 0.15)
- Structural noise patterns modify the (field_path, type) set, causing Jaccard < threshold
- The adaptive threshold approaches 1.0 at large n, leaving no margin for structural variation

## 3. Root Cause Analysis

### 3.1 Why Structural Noise Fails
The adaptive threshold T(n)=1-0.8/(n+1) is designed to detect small structural changes in large schemas. At n=50, T(50)=0.9843, meaning only a 1.6% change in the (field_path, type) set is tolerable.

Structural noise patterns cause larger changes:
- **Optional field churn** (10% add/remove): ~20% of the field set changes (remove 10% + add 10%), producing Jaccard ≈ 0.8182 at n=10
- **Null-valued fields**: Changes the type of ~10% of fields from their original type to "null", producing Jaccard ≈ 0.8182-0.8824
- **Nested object variation**: Converts one field to a nested path, removing one (path,type) pair and adding another, producing Jaccard ≈ 0.8182-0.9608

### 3.2 The Fundamental Tradeoff
The experiment reveals a fundamental limitation of pure Jaccard (field_path, type) for freshness detection:

1. **True drift** (add/remove/change_type) causes Jaccard < threshold → correctly detected
2. **Structural noise** (churn/nulls/nesting) also causes Jaccard < threshold → incorrectly flagged

The threshold cannot distinguish between (1) and (2) because both modify the (field_path, type) set. The only difference is that true drift represents meaningful API evolution while structural noise represents normal variation.

### 3.3 Detection Margin Interpretation
Detection margin (threshold - mean_jaccard) is positive for all patterns, but this is misleading:
- For true drift: positive margin means detection works
- For structural noise: positive margin means false detection occurs

The margin does not discriminate between true drift and structural noise.

## 4. Baseline Comparisons

### 4.1 Fixed Threshold 0.85
Per prior experiments, fixed threshold 0.85 fails at n≥10 because the add-field Jaccard = n/(n+1) exceeds 0.85 for n≥6. This baseline is not re-measured here.

### 4.2 Random Classifier
A random classifier (50% detection, 50% FP) would fail both TP and FP criteria. The adaptive threshold outperforms random on TP but fails on FP for structural noise.

### 4.3 Static Threshold (Mean Stale Jaccard)
A static threshold equal to the mean stale Jaccard across all drift patterns would produce TP=50% (half above, half below), failing the TP≥0.8 criterion. The adaptive threshold outperforms this baseline on TP.

## 5. Decision Rule Application

Applying the frozen decision rule from spec.json:

| Condition | Required | Observed | Status |
|-----------|----------|----------|--------|
| TP CI lower ≥ 0.8 (true drift) | Yes | 0.8865-1.0 | PASS |
| FP CI upper ≤ 0.15 (structural noise) | Yes | 1.0 | **FAIL** |
| Detection margin positive (all patterns) | Yes | 0.0039-0.1661 | PASS |
| Positive control (add_field TP ≥ 0.8) | Yes | 1.0 | PASS |
| Null control (fresh FP = 0) | Yes | 0 | PASS |
| No pipeline errors | Yes | 0 | PASS |

**Result**: FALSIFIED-IN-SETTING (Condition 2 fails)

## 6. Product Consequences

### 6.1 Negative Consequence
The adaptive Jaccard threshold cannot be used as a standalone staleness guard for inherited knowledge in the SPIDER product kernel. Any structural variation (optional fields, null values, nested objects) would be flagged as staleness, producing excessive false alarms.

### 6.2 Required Pivot
Product must either:
1. **Abandon Jaccard-based freshness** for structural noise environments
2. **Combine Jaccard with other staleness signals** (session token validation, semantic embedding similarity, response-time profiling) to distinguish true drift from structural noise
3. **Require schema-specific calibration** to set thresholds that tolerate expected structural noise levels

### 6.3 Not a Domain Closure
This falsification applies to the specific formula T(n)=1-0.8/(n+1) under the tested structural noise patterns. It does not close the broader domain of Jaccard-based freshness detection, which may still work:
- With lower thresholds that trade off TP for FP
- On schemas with predictable structural variation
- Combined with additional signals
- Under different noise patterns

## 7. Limitations

1. **Synthetic data**: Mock schemas may not reflect real API structural noise patterns
2. **Structure-only Jaccard**: (field_path, type) ignores field relationships, cardinality, and semantic meaning
3. **Deterministic generation**: All 30 samples per group are identical (same Jaccard value), limiting variance estimation
4. **Single formula tested**: Only T(n)=1-0.8/(n+1) is tested; other constants in T(n)=1-c/(n+1) may yield different results

## 8. Reproducibility

The experiment is fully reproducible:
- Deterministic random seed: 20260913
- All code in `research/graph/freshness_detection/execute_structural_noise.py`
- Raw evidence preserved in `raw_evidence/` with SHA256 hashes
- Re-run produces identical results
