# EXP-GRAPH-35237975537 Report: Session-Status Probing for Valid Orthogonality Test

## Executive Summary

**Orthogonality hypothesis SURVIVES: |r| = 0.1387 < 0.3, permutation p = 0.0310.**
Behavioral and structural signals are independently observable on the same conditions.

**Decision criteria:**
- **C1 (drift TP >= 0.85, all Wilson lower > 0.75)**: mean TP = 0.7292, all_wilson_lower > 0.75 = False -> FAIL
- **C2 (variance >= 6/8 conditions)**: 8/8 conditions with variance -> PASS
- **C3 (orthogonality |r| < 0.3)**: |r| = 0.1387, p = 0.0310 -> PASS
- **C4 (null FP = 0.0)**: FP = 0.0000 -> PASS

**Overall: FAIL**

**Measurement validity**: VALID (8/8 conditions with variance, 240 paired samples)

## Design Changes from Parent (EXP-GRAPH-35191029030)

| Aspect | Parent | This Experiment |
|--------|--------|-----------------|
| /session/status endpoint | Returns HTTP 200 with valid=true/false | Returns HTTP 200 for valid, HTTP 401 for invalid |
| Behavioral composite formula | token_val_rate*2 + session_change*3 + auth_boundary*1 | token_val_rate*2 + session_change*3 + auth_boundary*1 + session_status_check*2 |
| session_status_check | Not present | (3 - HTTP_status_code) / 2 → 0.0 for 200, 1.0 for 401 |
| session_invalidation variance | Always invalidated (constant behavioral = 3.0) | Randomly vary (50/50) session validity |
| Within-condition stochastic variation | Permission subsets for PB, token expiry jitter for SI | Same + randomized session validity for SI |

## Experimental Conditions

### Co-occurring Conditions (8 total)

| Condition | Drift | Noise | Samples | Variance |
|-----------|-------|-------|---------|----------|
| cooccur_permission_boundary+optional_field_addition | permission_boundary | optional_field_addition | 30 | OK (b_std=0.1652, s_std=1.1596) |
| cooccur_permission_boundary+description_change | permission_boundary | description_change | 30 | OK (b_std=0.1571, s_std=0.6283) |
| cooccur_permission_boundary+response_time_jitter | permission_boundary | response_time_jitter | 30 | OK (b_std=0.1571, s_std=0.9775) |
| cooccur_permission_boundary+field_type_normalization | permission_boundary | field_type_normalization | 30 | OK (b_std=0.1633, s_std=0.6236) |
| cooccur_session_invalidation+optional_field_addition | session_invalidation | optional_field_addition | 30 | OK (b_std=2.4944, s_std=1.0205) |
| cooccur_session_invalidation+description_change | session_invalidation | description_change | 30 | OK (b_std=2.4944, s_std=0.6669) |
| cooccur_session_invalidation+response_time_jitter | session_invalidation | response_time_jitter | 30 | OK (b_std=2.4777, s_std=0.9286) |
| cooccur_session_invalidation+field_type_normalization | session_invalidation | field_type_normalization | 30 | OK (b_std=2.4944, s_std=0.6768) |

### Per-Condition Pearson r (Exploratory)

| Condition | r | p |
|-----------|---|---|
| cooccur_permission_boundary+optional_field_addition | 0.1924 | 0.3084 |
| cooccur_permission_boundary+description_change | -0.3189 | 0.0859 |
| cooccur_permission_boundary+response_time_jitter | 0.3135 | 0.0917 |
| cooccur_permission_boundary+field_type_normalization | -0.2728 | 0.1447 |
| cooccur_session_invalidation+optional_field_addition | 0.2990 | 0.1085 |
| cooccur_session_invalidation+description_change | 0.1636 | 0.3875 |
| cooccur_session_invalidation+response_time_jitter | 0.2149 | 0.2541 |
| cooccur_session_invalidation+field_type_normalization | 0.1053 | 0.5797 |

### Per-Drift-Pattern Pearson r (Exploratory)

| Drift Pattern | Samples | r |
|---------------|---------|---|
| permission_boundary | 120 | 0.0514 |
| session_invalidation | 120 | 0.1894 |

## Primary Analysis

### Pooled Pearson Correlation

- **r = 0.1387** (|r| = 0.1387)
- **p = 0.0310** (permutation test, 1000 permutations)
- **n = 240** paired samples (8 conditions × 30 samples)
- **C3 threshold**: |r| < 0.3 -> PASS

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
| cooccur_session_invalidation+optional_field_addition | 2.4944 | 1.0205 | YES |
| cooccur_session_invalidation+description_change | 2.4944 | 0.6669 | YES |
| cooccur_session_invalidation+response_time_jitter | 2.4777 | 0.9286 | YES |
| cooccur_session_invalidation+field_type_normalization | 2.4944 | 0.6768 | YES |

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
3. **Session validity randomization**: 50/50 coin flip simulates session validity; real APIs use TTL/expiry.
4. **Pooled Pearson r**: Per-condition correlation may differ; exploratory analysis reported.
5. **Composite score weighting**: Behavioral weights (2, 3, 1, 2) inherited from parent, not optimized.

## Product Consequences

### If C3 PASSES (|r| < 0.3):

- C-FRESHNESS gains a validated second detection channel
- Product pipeline can integrate behavioral signals alongside structural signals
- Architecture: parallel independent channels for freshness detection
- Next step: test behavioral signals on real OAuth/OIDC middleware (Auth0/Okta/Keycloak)
