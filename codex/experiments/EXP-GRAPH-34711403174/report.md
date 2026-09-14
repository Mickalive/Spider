# EXP-GRAPH-34711403174 — Freshness Detection Report

## Executive Summary

**Status**: COMPLETE  
**Outcome**: SUPPORTS  
**Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)

A simple postcondition-similarity freshness score based on Jaccard similarity of `(field_path, type)` pairs achieved **100% true-positive rate** and **0% false-positive rate** across three resource families with distinct drift patterns. The experiment SURVIVES_CURRENT_TEST per all frozen decision rule conditions.

## Scientific Question

Does comparing cached mechanism postconditions against live endpoint responses provide reliable staleness detection across resource families with different drift patterns?

## Result

| Metric | Value | 95% CI | Threshold |
|--------|-------|--------|-----------|
| True-positive rate | 1.0 | [0.796, 1.0] | >= 0.8 |
| False-positive rate | 0.0 | [0.0, 0.278] | <= 0.1 |
| Per-family TP (users) | 1.0 | — | > 0.7 |
| Per-family TP (posts) | 1.0 | — | > 0.7 |
| Per-family TP (comments) | 1.0 | — | > 0.7 |

**Confusion matrix**: TP=15, FN=0, FP=0, TN=10

## Per-Drift-Pattern Analysis

### Add-field (users): phone added at request 6
- Pre-drift similarity: 1.0 (requests 1-5)
- Post-drift similarity: 0.75 (requests 6-10)
- Detection: 5/5 correct

### Change-type (posts): id changes from integer to string at request 6
- Pre-drift similarity: 1.0 (requests 1-5)
- Post-drift similarity: 0.6 (requests 6-10)
- Detection: 5/5 correct

### Remove-field (comments): author removed at request 6
- Pre-drift similarity: 1.0 (requests 1-5)
- Post-drift similarity: 0.75 (requests 6-10)
- Detection: 5/5 correct

## Sensitivity Analysis

| Threshold | TP Rate | FP Rate |
|-----------|---------|---------|
| 0.7 | 0.333 | 0.0 |
| 0.8 | 1.0 | 0.0 |
| 0.85 | 1.0 | 0.0 |
| 0.9 | 1.0 | 0.0 |
| 0.95 | 1.0 | 0.0 |

The frozen threshold 0.85 is well-calibrated. Threshold 0.7 is too low: it catches change-type drift (similarity 0.6) but misses add-field and remove-field drift (similarity 0.75). All thresholds >= 0.8 produce perfect detection with zero false positives on this dataset.

## Controls

### Positive Control (add-field drift)
- **Expected**: Similarity drops below 0.85, detection rate 100%
- **Observed**: Similarity = 0.75 at requests 6-10, detected_stale = true for all 5
- **PASS**

### Null Control (stable endpoint)
- **Expected**: Similarity always 1.0, false-positive rate 0%
- **Observed**: Similarity = 1.0 for all 10 requests, 0 false positives
- **PASS**

## Interpretation

The experiment provides strong proof-of-concept support for C-FRESHNESS. A simple Jaccard similarity metric on `(field_path, type)` pairs cleanly separates fresh from stale postconditions with zero errors across the three tested drift patterns. The separation is unambiguous: fresh similarity is always 1.0, stale similarity is at most 0.75, and the threshold 0.85 sits well between these distributions.

### What This Validates

1. **Structural drift is detectable**: Adding, removing, or changing types of fields produces measurable Jaccard similarity drops.
2. **Threshold 0.85 is robust**: It works for all three tested drift patterns with wide margin.
3. **Zero false positives on stable endpoints**: The null control confirms no spurious staleness signals.

### Scope Limitations

This is a **proof-of-concept in a controlled mock environment**, not a general validation:

1. **Synthetic drift only**: Drift patterns are clean and deterministic. Real-world drift may be noisier or involve partial changes.
2. **Flat schema**: The `(field_path, type)` representation does not capture nested structures, value constraints, or optional fields.
3. **Small sample**: 10 requests per family, 40 total. Adequate for deterministic drift but limited for stochastic patterns.
4. **No real APIs tested**: All requests go to a local mock server. Real endpoints have latency, rate limits, authentication, and variable response formats.
5. **No semantic drift**: The experiment tests structural drift (schema changes) but not semantic drift (same fields, different meaning).

### Comparison to Baselines

- **No detection** (always assume fresh): TP=0%, FP=0% — misses all drift
- **Random detection** (50%): TP~50%, FP~50% — unreliable
- **Postcondition similarity** (this experiment): TP=100%, FP=0% — significantly better

## Product Consequence

**Positive**: Freshness scoring can be integrated into the kernel to trigger re-validation of cached mechanisms. This validates C-FRESHNESS at proof-of-concept level for structural drift detection.

**Caveat**: Integration should be limited to structural drift detection until real-world validation is performed. The product lane should not assume this method detects semantic drift, nested schema changes, or drift on complex real-world APIs without further testing.

## Decision Rule Evaluation

All frozen conditions met:
1. ✅ True-positive rate >= 0.8 (observed: 1.0)
2. ✅ False-positive rate <= 0.1 (observed: 0.0)
3. ✅ Per-family TP > 0.7 for each drift pattern (observed: 1.0 for all)
4. ✅ No mock server failures (0 failures)

**Decision: SURVIVES_CURRENT_TEST**
