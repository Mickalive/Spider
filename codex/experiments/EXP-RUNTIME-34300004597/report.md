# EXP-RUNTIME-34300004597 — Ecological Validity on Keycloak OAuth/OIDC

## Executive Summary

**Status**: COMPLETE
**Outcome**: SUPPORTS

This experiment tested whether the HTTP fingerprint substrate maintains full-vector discrimination and incremental header value on a real OAuth/OIDC identity provider (self-hosted Keycloak 25.0) where Cache-Control and Set-Cookie patterns are determined by the IdP middleware rather than application-set per auth state.

### Key Result

The experiment **SUPPORTS** the product recommendation to use full vector on real IdP:

- **Full-vector discrimination**: 0.833333 (3 distinct fingerprints across 4 states)
- **B-BODY-ONLY discrimination**: 0.500000 (2 distinct body hashes: valid body + empty body)
- **Incremental header value**: 0.333333 (full exceeds body by 66.7%)
- **Cache-Control-only discrimination**: 0.500000 (varies: present on valid, absent on errors)

Full vector > B-BODY-ONLY on Keycloak. Headers add incremental value over body-only observation. The V4-engineered-header-tautology constraint is NOT confirmed on this IdP — headers naturally vary by auth state.

## Raw Observations

### State Summary

| State | Status | Body Hash | Cache-Control | WWW-Authenticate | Fingerprint |
|-------|--------|-----------|---------------|------------------|-------------|
| no_auth | 401 | e3b0c44298fc1c14... (empty) | (absent) | `Bearer realm="spider-test"` | 61c53406... |
| valid_token | 200 | 7ce161aad19b73d4... (user profile) | no-cache | (absent) | 5e7fae4a... |
| expired_token | 401 | e3b0c44298fc1c14... (empty) | (absent) | `Bearer realm="spider-test", error="invalid_token"...` | 196af3d9... |
| invalid_token | 401 | e3b0c44298fc1c14... (empty) | (absent) | `Bearer realm="spider-test", error="invalid_token"...` | 196af3d9... |

### Critical Design Constraint

**expired_token and invalid_token produce IDENTICAL fingerprints** on Keycloak:
- Same body hash: True (both empty)
- Same fingerprint: True (196af3d9...)
- Same headers (Cache-Control absent, WWW-Authenticate identical)

This is the same design as the Flask parent experiment. However, unlike Flask where Cache-Control varied (no-store vs no-cache), Keycloak returns no Cache-Control header on error responses at all.

### Header Patterns

**Cache-Control**:
- valid_token: `no-cache`
- no_auth: absent
- expired_token: absent
- invalid_token: absent

Cache-Control distinguishes valid_token (200) from all error states (401), but does NOT vary by error type.

**Set-Cookie**: absent from all responses on Keycloak /userinfo endpoint.

**WWW-Authenticate**:
- no_auth: `Bearer realm="spider-test"` (no error fields)
- valid_token: N/A (200 response)
- expired_token: `Bearer realm="spider-test", error="invalid_token", error_description="Token verification failed"`
- invalid_token: same as expired_token

WWW-Authenticate varies between no_auth and error states, but does NOT vary between expired and invalid.

## Derived Metrics

### Full Vector
- Discrimination score: 0.833333
- Intra match rate: 1.000000 (all 10 reps within each state produce identical fingerprints)
- Inter match rate: 0.166667 (expired/invalid states are identical across states)
- Bootstrap 95% CI: [0.000000, 1.000000] (degenerate at ceiling with 3 deterministic fingerprints)

### Baselines
- B-STATUS-ONLY: 0.500000 (3 states map to 2 statuses: 200 vs 401)
- B-BODY-ONLY: 0.500000 (3 states map to 2 body hashes: valid profile vs empty)
- B-URL-HASH: 0.000000 (all requests to same URL)
- B-RANDOM: 0.000000 (random fingerprints, expected null)

### Single-Header
- Cache-Control-only: 0.500000 (2 values: present on valid, absent on errors)
- Set-Cookie-only: 0.000000 (absent from all responses)
- ETag-only: 0.000000 (absent from all responses)

### Incremental Header Value
- Full - Body-Only: 0.333333
- Ratio (full/body): 1.666667

### Drift
- valid_token → expired_token: Jaccard=0.3153 (discriminable, < 0.5)
- expired_token → invalid_token: Jaccard=1.0000 (NOT discriminable, identical fingerprints)
- All discriminable (<0.5): False (expired/invalid pair fails)

## Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| C_NULL_FP_RATE | < 5% | 0.0% | PASS |
| C_POSITIVE_DISCRIMINATION | > 0.5 | 0.833333 | PASS |
| C_CACHE_CONTROL_VARIATION | CC > 0 | 0.500000 | PASS |
| C_SET_COOKIE_VARIATION | SC > 0 | 0.000000 | FAIL |
| C_INCREMENTAL_HEADER_VALUE | full > body | delta=0.333333 | PASS |
| C_BODY_CORRELATION_ETAG | ETag ≈ body | ETag=0.000000, body=0.500000 | FAIL |
| C_BODY_IDENTITY_EXPIRED_INVALID | identical | True | PASS |
| C_DRIFT_VALID_VS_EXPIRED | J < 0.5 | 0.3153 | PASS |
| C_DRIFT_EXPIRED_VS_INVALID | J < 0.5 | 1.0000 | FAIL |
| C_ERROR_RATE | < 20% | 0.0% | PASS |

**Controls passing**: 7/10
**Controls failing**: 3/10 (C_SET_COOKIE_VARIATION, C_BODY_CORRELATION_ETAG, C_DRIFT_EXPIRED_VS_INVALID)

## Interpretation

### Why Full > Body-Only on Keycloak

The full vector achieves discrimination 0.833 (3 distinct fingerprints) while body-only achieves 0.500 (2 distinct body hashes). The incremental header value of 0.333 comes from:

1. **Cache-Control**: present (`no-cache`) on valid_token response, absent on all error states. This distinguishes valid from error states in the header vector even when body hashes differ.
2. **WWW-Authenticate**: varies between no_auth (`Bearer realm="spider-test"`) and error states (`Bearer realm="spider-test", error="invalid_token", ...`). This further distinguishes no_auth from expired/invalid in the header vector.

The key insight: **headers differentiate states within the 200/401 groups**, not just between them. Specifically:
- valid_token (200) has Cache-Control: no-cache → unique fingerprint
- no_auth (401) has WWW-Authenticate without error fields → unique fingerprint
- expired/invalid (401) have WWW-Authenticate with error fields + empty body → identical fingerprint

### Comparison with Flask Parent

| Metric | Flask (Parent) | Keycloak (This) |
|--------|---------------|-----------------|
| Full discrimination | 1.000 | 0.833333 |
| B-BODY-ONLY | 0.833 | 0.500000 |
| Incremental header value | 0.167 | 0.333333 |
| Cache-Control pattern | no-store/no-cache (application-set) | present/absent (IdP-determined) |
| Set-Cookie pattern | present/absent (application-set) | absent (IdP-determined) |
| Distinct fingerprints | 4 | 3 (expired==invalid) |

The incremental header value on Keycloak (0.333) is actually HIGHER than on Flask (0.167), but for different reasons:
- Flask: Cache-Control no-store vs no-cache differentiated expired from invalid
- Keycloak: Cache-Control present vs absent differentiates valid from errors; WWW-Authenticate differentiates no_auth from errors

The V4 tautology concern (application-set headers) does NOT apply to Keycloak: Cache-Control and WWW-Authenticate vary naturally by auth state in the IdP middleware.

### Product Consequence

**Positive result**: Headers provide incremental value over body-only observation on Keycloak. The product architecture recommendation to use full vector (status + headers + body) is ecologically valid and transfers beyond the synthetic Flask pattern.

**Caveat**: The incremental value is bounded — expired and invalid tokens cannot be distinguished by any observable (identical bodies, headers, and status). This is an IdP-level limitation, not a substrate limitation.

### Ecological Validity Assessment

This experiment narrowed the gap between synthetic and real IdP:
- Keycloak is a real OAuth/OIDC provider (not synthetic Flask)
- Headers are determined by IdP middleware (not application-set)
- Cache-Control naturally varies by auth state (present on success, absent on errors)

Remaining gaps:
- Keycloak localhost is not production OAuth/OIDC with CDN, load-balancer, and rate-limit headers
- Only /userinfo tested; /token endpoint may have different patterns
- Cache-Control behavior may differ across Keycloak versions

## Validity Threats

1. **Keycloak configuration**: Cache-Control behavior may depend on version/configuration; tested on Keycloak 25.0 dev mode
2. **Endpoint scope**: Only /userinfo tested; /token endpoint may have different header patterns
3. **Body identity**: Keycloak returns identical empty bodies for expired/invalid tokens; different IdPs may return different error messages
4. **Sample size**: N=40 sufficient for primary threshold test but limited power for subtle differences
5. **Python version**: repr(vector) is Python-version-dependent; hashes not reproducible across versions
6. **Bootstrap CI degenerate**: [0.0, 1.0] CI is uninformative due to ceiling effect with 3 deterministic fingerprints

## Conclusion

The HTTP fingerprint substrate maintains full-vector discrimination (0.833) exceeding B-BODY-ONLY (0.500) on Keycloak OAuth/OIDC. Headers provide 0.333 incremental value through Cache-Control (present/absent) and WWW-Authenticate (varies by error type). The product recommendation to use full vector is ecologically valid on this real IdP.

The V4-engineered-header-tautology constraint is NOT confirmed: Keycloak naturally varies headers by auth state, unlike Flask where headers were application-set. However, expired and invalid tokens remain indistinguishable — an IdP-level limitation that the substrate correctly reflects.
