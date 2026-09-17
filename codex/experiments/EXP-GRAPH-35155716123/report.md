# EXP-GRAPH-35155716123 Report: Session-level Behavioral Signals for C-FRESHNESS

## Executive Summary

**Behavioral signals FAIL the C-FRESHNESS gate.**

- **C1 (drift detection)**: TP = 1.0000 >= 0.90 PASS
- **C2 (noise tolerance)**: FP = 0.0000 <= 0.15 PASS
- **C3 (discrimination)**: AUC = 1.0000 > 0.80 PASS
- **C4 (orthogonality)**: |r| = 0.4411 >= 0.3 FAIL
- **C5 (positive control)**: fires PASS

## Raw Observations

### Drift Pattern Detection (TP)

| Pattern | n=10 | n=20 | n=30 | n=40 | n=50 | Mean TP |
|---------|------|------|------|------|------|---------|
| token_expiry | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| session_invalidation | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| permission_boundary | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| signing_key_rotation | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| cookie_clearance | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

**Overall Mean TP: 1.0000**

### Noise Pattern Tolerance (FP)

| Pattern | n=10 | n=20 | n=30 | n=40 | n=50 | Mean FP |
|---------|------|------|------|------|------|---------|
| optional_field_addition | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| description_change | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| response_time_jitter | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| field_type_normalization | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

**Overall Mean FP: 0.0000**

### Behavioral Signal Features

- drift_token_expiry_n10: token_val_rate=1.0000, session_change=0, auth_boundary=0
- drift_session_invalidation_n10: token_val_rate=0.0000, session_change=1, auth_boundary=0
- drift_permission_boundary_n10: token_val_rate=0.0000, session_change=0, auth_boundary=2
- drift_signing_key_rotation_n10: token_val_rate=1.0000, session_change=0, auth_boundary=0
- drift_cookie_clearance_n10: token_val_rate=0.0000, session_change=1, auth_boundary=0
- drift_token_expiry_n20: token_val_rate=1.0000, session_change=0, auth_boundary=0
- drift_session_invalidation_n20: token_val_rate=0.0000, session_change=1, auth_boundary=0
- drift_permission_boundary_n20: token_val_rate=0.0000, session_change=0, auth_boundary=2
- drift_signing_key_rotation_n20: token_val_rate=1.0000, session_change=0, auth_boundary=0
- drift_cookie_clearance_n20: token_val_rate=0.0000, session_change=1, auth_boundary=0
- drift_token_expiry_n30: token_val_rate=1.0000, session_change=0, auth_boundary=0
- drift_session_invalidation_n30: token_val_rate=0.0000, session_change=1, auth_boundary=0
- drift_permission_boundary_n30: token_val_rate=0.0000, session_change=0, auth_boundary=2
- drift_signing_key_rotation_n30: token_val_rate=1.0000, session_change=0, auth_boundary=0
- drift_cookie_clearance_n30: token_val_rate=0.0000, session_change=1, auth_boundary=0
- drift_token_expiry_n40: token_val_rate=1.0000, session_change=0, auth_boundary=0
- drift_session_invalidation_n40: token_val_rate=0.0000, session_change=1, auth_boundary=0
- drift_permission_boundary_n40: token_val_rate=0.0000, session_change=0, auth_boundary=2
- drift_signing_key_rotation_n40: token_val_rate=1.0000, session_change=0, auth_boundary=0
- drift_cookie_clearance_n40: token_val_rate=0.0000, session_change=1, auth_boundary=0
- drift_token_expiry_n50: token_val_rate=1.0000, session_change=0, auth_boundary=0
- drift_session_invalidation_n50: token_val_rate=0.0000, session_change=1, auth_boundary=0
- drift_permission_boundary_n50: token_val_rate=0.0000, session_change=0, auth_boundary=2
- drift_signing_key_rotation_n50: token_val_rate=1.0000, session_change=0, auth_boundary=0
- drift_cookie_clearance_n50: token_val_rate=0.0000, session_change=1, auth_boundary=0
- noise_optional_field_addition_n10: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_description_change_n10: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_response_time_jitter_n10: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_field_type_normalization_n10: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_optional_field_addition_n20: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_description_change_n20: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_response_time_jitter_n20: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_field_type_normalization_n20: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_optional_field_addition_n30: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_description_change_n30: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_response_time_jitter_n30: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_field_type_normalization_n30: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_optional_field_addition_n40: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_description_change_n40: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_response_time_jitter_n40: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_field_type_normalization_n40: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_optional_field_addition_n50: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_description_change_n50: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_response_time_jitter_n50: token_val_rate=0.0000, session_change=0, auth_boundary=0
- noise_field_type_normalization_n50: token_val_rate=0.0000, session_change=0, auth_boundary=0

### Discrimination Metrics

- **AUC**: 1.0000
- **Pearson r (behavioral vs structural)**: -0.4411 (p=0.0024)

### Per-Pattern True Positive Rates

- token_expiry: 1.0000
- session_invalidation: 1.0000
- permission_boundary: 1.0000
- signing_key_rotation: 1.0000
- cookie_clearance: 1.0000

### Per-Pattern False Positive Rates

- optional_field_addition: 0.0000
- description_change: 0.0000
- response_time_jitter: 0.0000
- field_type_normalization: 0.0000

## Interpretation

This experiment tests whether session-level behavioral signals provide drift-vs-noise discrimination on a fundamentally different dimension from all six tested structural/schema-based signal families.

- **C4 FAILS**: |r| = 0.4411 >= 0.3. Behavioral signals are correlated with structural signals.

The behavioral signal family fails the C-FRESHNESS gate in this deterministic mock setting. Seven signal families have now been tested (six structural + one behavioral), all failing in the same deterministic mock environment. The C-FRESHNESS domain may require fundamentally different experimental designs:
- Real API deployments with DB/cache/CDN stochasticity
- Production client traffic patterns
- Stochastic field availability
- Composite multi-signal classifiers on real data

## Scope Limitations

- Claim ceiling bounded to: Flask 3.1.3 + PyJWT 2.14.0 HS256 on localhost, 5 drift patterns, 4 noise patterns, 5 schema sizes, deterministic computation
- Does NOT extend to: production OAuth/OIDC (Auth0/Okta/Keycloak), CDN/caching, load-balancer, rate-limit, stochastic field availability, real client traffic, or non-deterministic API behavior
- Does NOT test: composite multi-signal classifiers, real-world drift co-occurrence, or production deployment patterns
- Behavioral signals are computed analytically from the deterministic mock configuration, not from live HTTP traffic
- The orthogonality to structural signals is by construction (auth state vs schema structure), not an empirical discovery
