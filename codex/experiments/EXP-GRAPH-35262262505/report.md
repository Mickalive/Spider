# EXP-GRAPH-35262262505 Report: Graded Session-Status Intensity for TP-Preserving Variance

## Executive Summary

**Orthogonality hypothesis NOT CONFIRMED: |r| = 0.0527 < 0.3 (passes) but permutation p = 0.4136 > 0.05 (fails).**
Behavioral and structural signals show very weak correlation (r² = 0.003, behavioral explains 0.3% of structural variance) but the permutation test lacks statistical power to confirm significance at p < 0.05 with n=240.

**Decision criteria:**
- **C1 (drift TP >= 0.85, all Wilson lower > 0.75)**: mean TP = 1.0000, all_wilson_lower > 0.75 = True -> PASS
- **C2 (variance >= 6/8 conditions)**: 8/8 conditions with variance -> PASS
- **C3 (orthogonality |r| < 0.3)**: |r| = 0.0527, p = 0.4136 -> FAIL
- **C4 (null FP = 0.0)**: FP = 0.0000 -> PASS

**Overall: FAIL**

**Measurement validity**: VALID (8/8 conditions with variance, 240 paired samples)

## Design Changes from Parent (EXP-GRAPH-35237975537)

| Aspect | Parent (50/50 Coin Flip) | This Experiment (Graded Intensity) |
|--------|--------------------------|-------------------------------------|
| Session validity | 50/50 coin flip (valid/invalid) | ALL invalid (session_change=1 for every sample) |
| session_status_check variation | Binary: 200->0.0 or 401->1.0 | Graded: 401->1.0, 403->0.5, 500->0.75 |
| Session_status_check mapping | (3 - status_code)/2 (arithmetic) | Direct mapping: 401->1.0, 403->0.5, 500->0.75 |
| Behavioral composite range for SI | Bimodal: 0.0 (valid) or 5.0 (invalid) | Continuous: 4.0 to 5.0 |
| session_change for SI | 0 or 1 (coin flip) | Always 1 |
| TP for SI | 0.433-0.467 (diluted) | Expected 1.0 (no dilution) |
| Behavioral std for SI | ~2.49 (bimodal) | Expected ~0.4 (graded) |
| All other aspects | Same | Same |

## Experimental Conditions

### Co-occurring Conditions (8 total)

| Condition | Drift | Noise | Samples | Variance |
|-----------|-------|-------|---------|----------|
| cooccur_permission_boundary+optional_field_addition | permission_boundary | optional_field_addition | 30 | OK (b_std=0.1652, s_std=1.1596) |
| cooccur_permission_boundary+description_change | permission_boundary | description_change | 30 | OK (b_std=0.1571, s_std=0.6283) |
| cooccur_permission_boundary+response_time_jitter | permission_boundary | response_time_jitter | 30 | OK (b_std=0.1571, s_std=0.9775) |
| cooccur_permission_boundary+field_type_normalization | permission_boundary | field_type_normalization | 30 | OK (b_std=0.1633, s_std=0.6236) |
| cooccur_session_invalidation+optional_field_addition | session_invalidation | optional_field_addition | 30 | OK (b_std=0.4153, s_std=1.0205) |
| cooccur_session_invalidation+description_change | session_invalidation | description_change | 30 | OK (b_std=0.3742, s_std=0.6669) |
| cooccur_session_invalidation+response_time_jitter | session_invalidation | response_time_jitter | 30 | OK (b_std=0.3948, s_std=0.9286) |
| cooccur_session_invalidation+field_type_normalization | session_invalidation | field_type_normalization | 30 | OK (b_std=0.4180, s_std=0.6768) |

### Per-Condition Pearson r (Exploratory)

| Condition | r | p |
|-----------|---|---|
| cooccur_permission_boundary+optional_field_addition | 0.1924 | 0.3084 |
| cooccur_permission_boundary+description_change | -0.3189 | 0.0859 |
| cooccur_permission_boundary+response_time_jitter | 0.3135 | 0.0917 |
| cooccur_permission_boundary+field_type_normalization | -0.2728 | 0.1447 |
| cooccur_session_invalidation+optional_field_addition | 0.1160 | 0.5416 |
| cooccur_session_invalidation+description_change | 0.1536 | 0.4176 |
| cooccur_session_invalidation+response_time_jitter | -0.0136 | 0.9430 |
| cooccur_session_invalidation+field_type_normalization | 0.0187 | 0.9221 |

### Per-Drift-Pattern Pearson r (Exploratory)

| Drift Pattern | Samples | r |
|---------------|---------|---|
| permission_boundary | 120 | 0.0514 |
| session_invalidation | 120 | 0.0462 |

### Session Status Code Distribution (Session Invalidation Conditions)

| Condition | 401 | 403 | 500 | Total |
|-----------|-----|-----|-----|-------|
| cooccur_session_invalidation+optional_field_addition | 9 | 12 | 9 | 30 |
| cooccur_session_invalidation+description_change | 6 | 12 | 12 | 30 |
| cooccur_session_invalidation+response_time_jitter | 8 | 11 | 11 | 30 |
| cooccur_session_invalidation+field_type_normalization | 10 | 11 | 9 | 30 |

## Primary Analysis

### Pooled Pearson Correlation

- **r = 0.0527** (|r| = 0.0527)
- **p = 0.4136** (permutation test, 1000 permutations)
- **n = 240** paired samples (8 conditions x 30 samples)
- **C3 threshold**: |r| < 0.3 AND permutation p < 0.05 -> FAIL (|r|=0.0527 < 0.3 passes, but p=0.4136 > 0.05 fails)

### Signal Observability (Within-Condition Variance)

- **Conditions with variance (both signals std > 0)**: 8/8
- **Measurement validity**: VALID (8 >= 6 conditions, 240 >= 240 samples)

### Per-Condition Variance Details

| Condition | Behavioral Std | Structural Std | Has Variance |
|-----------|----------------|----------------|--------------|
| cooccur_permission_boundary+optional_field_addition | 0.1652 | 1.1596 | YES |
| cooccur_permission_boundary+description_change | 0.1571 | 0.6283 | YES |
| cooccur_permission_boundary+response_time_jitter | 0.1571 | 0.9775 | YES |
| cooccur_permission_boundary+field_type_normalization | 0.1633 | 0.6236 | YES |
| cooccur_session_invalidation+optional_field_addition | 0.4153 | 1.0205 | YES |
| cooccur_session_invalidation+description_change | 0.3742 | 0.6669 | YES |
| cooccur_session_invalidation+response_time_jitter | 0.3948 | 0.9286 | YES |
| cooccur_session_invalidation+field_type_normalization | 0.4180 | 0.6768 | YES |

## Controls

### Positive Control: permission_boundary Detection

- **Observed rate**: 1.0000 (30/30)
- **Threshold**: >= 0.90
- **Pass**: YES

### Positive Control: session_status_variance

- **session_invalidation conditions with variance**: 4/4
- **Threshold**: >= 4 (all 4 session_invalidation conditions should have variance)
- **Pass**: YES

### Null Control: Noise-Only FP

- **Observed FP rate**: 0.0000 (0/120)
- **Threshold**: FP = 0.0
- **Pass**: YES

## Validity Threats

1. **Deterministic mock server**: All measurements on localhost Flask, not production APIs.
2. **Limited drift patterns**: Only permission_boundary and session_invalidation tested.
3. **Graded status code mapping**: The mapping 401->1.0, 403->0.5, 500->0.75 is arbitrary. Different mappings might change the correlation structure.
4. **Composite score weighting**: Behavioral weights (2, 3, 1, 2) inherited from parent, not optimized.
5. **Session_status_check variance magnitude**: Expected std ~0.4 (from 3 values (0.5, 0.75, 1.0)) is smaller than parent's bimodal std ~2.49.
6. **Unauthenticated /session/status endpoint**: Synthetic construct not present in real APIs in this form.

## Product Consequences

### C3 fails on permutation p-value (p=0.414 > 0.05) despite very low |r|=0.053:

- The TP/variance trade-off IS broken: C1 PASS (TP=1.0) + C2 PASS (8/8 variance)
- Behavioral and structural signals show very weak correlation (|r|=0.053, r²=0.003)
- However, the permutation test lacks power to confirm significance at p<0.05 with n=240
- The frozen decision rule requires BOTH |r|<0.3 AND p<0.05 for C3 PASS
- Product implication: behavioral and structural signals are near-orthogonal but confirmatory test is underpowered
- Architecture recommendation: use composite multi-signal classifiers as precautionary measure
- Next step: larger sample size (n>=480) to achieve sufficient power for very low correlations
- Alternative: accept near-orthogonality (|r|=0.053) without formal significance confirmation

