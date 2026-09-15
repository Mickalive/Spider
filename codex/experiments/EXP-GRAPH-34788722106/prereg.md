# EXP-GRAPH-34788722106 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34788722106
- **Lane**: Graph
- **Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does adaptive Jaccard freshness threshold T(n)=1-0.8/(n+1) achieve TP>=0.8 and FP<=0.15 under structural noise (optional field churn, null-valued fields, nested object variation) on schemas with 10-50 fields, and does it maintain detection margin across realistic drift patterns?

## 3. Motivation

Prior experiments established:
- Fixed threshold 0.85 fails for schemas >=10 fields (scaling attack, EXP-GRAPH-34711403174)
- Adaptive threshold T(n)=1-0.8/(n+1) achieves TP=15/15 on flat mock schemas (EXPLORATORY, EXP-GRAPH-34755316488)
- Structural noise FP control was degenerate (Jaccard=1.0 on value changes by construction)
- Need to test FP under structural noise that causes Jaccard < 1.0 on fresh responses

This experiment replaces the degenerate stochastic-variation control with structural-noise stress tests (optional field churn, null-valued fields, nested object variation) to determine if the high adaptive threshold (approaching 1.0 at large n) is viable on real data.

## 4. Hypotheses

### H1: Detection Viability
Adaptive threshold T(n)=1-0.8/(n+1) achieves TP>=0.8 across drift patterns (add_field, remove_field, change_type) for all schema sizes 10-50 fields.

### H2: Noise Rejection
FP rate <= 0.15 across structural noise patterns (optional field churn, null-valued fields, nested object variation) for all schema sizes.

### H3: Detection Margin
Detection margin (threshold - stale Jaccard) remains positive for all drift patterns at all schema sizes.

### H4: Positive Control
Add-field drift (single new field added) must be detected at all schema sizes (TP >= 0.8).

### H5: Null Control
Fresh response with no structural change must not be detected (FP = 0).

## 5. Data Generation

### 5.1 Mock Schemas
Four schema sizes: 10, 20, 30, 50 fields. Each field has a unique path and type (string, integer, boolean, array, object).

### 5.2 Fresh Responses
For each schema size, generate 30 fresh responses by re-requesting same mock endpoint with value changes only (structure unchanged). Jaccard similarity should be 1.0.

### 5.3 Stale Variants (Drift Patterns)
For each schema size, generate 30 stale variants per drift pattern:
1. **add_field**: Add one new field (realistic drift)
2. **remove_field**: Remove one field (realistic drift)
3. **change_type**: Change one field's type (e.g., string → integer)
4. **optional_field_churn**: Randomly add/remove 10% of fields (structural noise)
5. **null_valued_fields**: Set random fields to null (structural noise)
6. **nested_object_variation**: Convert a field to nested object (structural noise)

### 5.4 Jaccard Similarity
Compute Jaccard similarity on (field_path, type) pairs between baseline and each variant.

### 5.5 Adaptive Threshold
For each schema size n, compute T(n) = 1 - 0.8/(n+1).

## 6. Measures

### 6.1 Primary Metrics
- **TP**: Fraction of stale variants where Jaccard < threshold (detected)
- **FP**: Fraction of fresh variants where Jaccard < threshold (false alarm)
- **Detection margin**: threshold - stale Jaccard per drift pattern per schema size

### 6.2 Secondary Metrics
- Jaccard similarity distribution per drift pattern per schema size
- Wilson 95% CI for TP and FP
- Sensitivity analysis: TP/FP at threshold ± 0.05

## 7. Null Models

### 7.1 Fixed Threshold 0.85
Parent scaling attack: fails at n>=10 (TP drops to 0 at n>=15).

### 7.2 Random Classifier
50% detection, 50% false positive. Expected to fail both TP and FP criteria.

## 8. Statistical Tests

### 8.1 Primary Test
- Wilson score interval for TP and FP at each schema size
- 95% CI, two-sided

### 8.2 Detection Margin
- Compute threshold - stale Jaccard for each drift pattern
- Require positive margin for all patterns

### 8.3 Effect Size
- Cohen's h for proportion difference between TP and 0.8, FP and 0.15

## 9. Controls

### 9.1 Positive Control (add_field drift)
- Must be detected at all schema sizes (TP >= 0.8)
- Verifies pipeline correctly detects simple structural drift

### 9.2 Null Control (fresh response)
- Must not be detected (FP = 0)
- Verifies pipeline does not false-alarm on stable endpoints

### 9.3 Scaling Control
- Test across 4 schema sizes (10, 20, 30, 50 fields)
- Verify detection does not degrade with size

### 9.4 Noise Type Control
- Test 3 structural noise patterns (optional churn, nulls, nesting)
- Verify each noise type individually does not cause excessive FP

## 10. Validity Threats

### 10.1 Synthetic-to-Real Gap
Mock schemas may not reflect real API structural noise. Mitigation: patterns are based on real-world observations (optional fields, null values, nested objects).

### 10.2 Sample Size
30 fresh responses per schema size may be insufficient for precise FP estimation. Mitigation: Wilson CIs provide uncertainty bounds; if CI upper bound > 0.15, result is falsified.

### 10.3 Jaccard Representation Loss
Jaccard (field_path,type) ignores field relationships, cardinality, and semantic meaning. Mitigation: this is the exact representation from parent experiments; if it fails, the entire Jaccard direction fails.

### 10.4 Threshold Calibration
The constant 0.8 in T(n)=1-0.8/(n+1) is empirically chosen. If it fails, the adaptive direction may still work with different constants. Mitigation: experiment tests this specific formula; a new preregistration would be needed for other constants.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. TP lower bound of 95% Wilson CI >= 0.8 across drift patterns (add_field, remove_field, change_type) for all schema sizes
2. FP upper bound of 95% Wilson CI <= 0.15 across structural noise patterns for all schema sizes
3. Detection margin positive for all drift patterns at all schema sizes
4. Positive control passes (add_field TP >= 0.8)
5. Null control passes (FP = 0)
6. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. TP lower bound < 0.8 at any schema size for any drift pattern
2. FP upper bound > 0.15 at any schema size for any structural noise pattern
3. Detection margin negative for any drift pattern at any schema size
4. Positive control fails (add_field TP < 0.8)
5. Null control fails (FP > 0)

### 11.3 MEASUREMENT_INVALID
If:
1. Sample sizes insufficient
2. Pipeline errors prevent computation
3. Mock schemas degenerate

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Adaptive Jaccard threshold viable for product integration
- Freshness detection can be added to SPIDER product kernel
- External agents can trust staleness scores based on schema-size-adjusted Jaccard
- Continue with real-API validation

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Adaptive Jaccard threshold fails under structural noise
- Jaccard (field_path,type) cannot distinguish true drift from common variations
- Product must pivot to alternative staleness signals or combine Jaccard with other methods
- Freshness research redirects

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Data Generation**: Generate mock schemas and variants as described
2. **Jaccard Computation**: Compute Jaccard similarity for each pair
3. **Threshold Application**: Apply T(n)=1-0.8/(n+1) per schema size
4. **TP/FP Calculation**: Compute TP and FP per schema size per drift type
5. **Wilson CIs**: Compute 95% Wilson CIs for TP and FP
6. **Detection Margin**: Compute threshold - stale Jaccard per pattern
7. **Control Checks**: Verify positive and null controls
8. **Decision Rule**: Apply frozen decision rule
9. **Reporting**: Report all outcomes with equal prominence

## 14. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for Wilson CIs
- Standard library only

Code will be committed to `research/graph/freshness_detection/` before execution.

## 15. Pre-registered Expectations

From prior experiments:
- Fixed threshold 0.85 fails at n>=10 (scaling attack)
- Adaptive threshold T(n)=1-0.8/(n+1) achieves TP=1.0 on flat schemas (EXPLORATORY)
- Structural noise may cause Jaccard < 1.0 on fresh responses, testing FP rate
- If FP <= 0.15, adaptive threshold is viable; if FP > 0.15, direction should be abandoned

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
