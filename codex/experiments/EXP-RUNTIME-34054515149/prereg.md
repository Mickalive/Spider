# EXP-RUNTIME-34054515149 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34054515149
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-06
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Handoff**: EXP-RUNTIME-34015740602 (CONSTRAINED, C-MEAS-VALID survives narrowly)

## 2. Scientific Question

Does the HTTP fingerprint substrate's full vector exceed B-BODY-ONLY when bodies are NOT perfectly discriminative (e.g., identical error bodies for expired/invalid token states) but headers (Cache-Control, Set-Cookie) vary independently with auth state?

## 3. Motivation

Parent experiment EXP-RUNTIME-34015740602 established discrimination 1.0 on Flask/PyJWT with 4 DISTINCT bodies. The H4 exploratory test (full vector > B-BODY-ONLY) was vacuous due to ceiling effect: with all 4 bodies distinct, discrimination is at 1.0 and headers cannot improve beyond perfect. The auditor correctly identified this as V3-DISTINCT-BODY-CEILING-CONFOUND.

The auditor noted that Cache-Control and Set-Cookie each achieve 0.5 discrimination alone (audit single_header_discrimination) but are redundant when bodies already achieve perfect discrimination (1.0). The critical unknown is whether these headers add incremental value when body signal is degraded.

Grandparent EXP-RUNTIME-33902315583 tested the identical-error-body scenario (expired_token and invalid_token sharing identical bodies) with standard headers only (Content-Type, Content-Length, Connection). Full vector equaled B-BODY-ONLY (0.833 = 0.833). But that experiment used only standard headers that do NOT vary with auth state. Cache-Control and Set-Cookie were not present.

This experiment combines both conditions: identical error bodies (degraded body signal) + production-like headers that vary with auth state (Cache-Control no-store/no-cache, Set-Cookie session). This is the only design that can answer the H4 question.

## 4. Hypotheses

### H1: Incremental Header Value
When expired_token and invalid_token share identical bodies, Cache-Control and Set-Cookie provide incremental discrimination. Full vector discrimination > B-BODY-ONLY.

### H2: Cache-Control Discrimination
Cache-Control header varies by auth state (no-store for expired, no-cache for invalid, absent for no_auth/valid_token). Cache-Control-only discrimination > 0.

### H3: Primary Threshold
Full vector discrimination > 0.5 (primary C-MEAS-VALID threshold).

### H4: Null FP
Null FP rate < 5% under server-side jitter 50-150ms uniform.

### H5: Set-Cookie Discrimination
Set-Cookie header varies by auth state (present only for valid_token). Set-Cookie-only discrimination > 0.

## 5. Server Configuration

### 5.1 Middleware
- Flask 3.1.3 + PyJWT 2.13.0 HS256
- Localhost 127.0.0.1 (port TBD, different from parent)

### 5.2 Auth States

| State | Status | Body | Cache-Control | Set-Cookie |
|-------|--------|------|---------------|------------|
| no_auth | 401 | login_required | (absent) | (absent) |
| valid_token | 200 | alice_profile | (absent) | session=abc123 |
| expired_token | 401 | error_response | no-store | (absent) |
| invalid_token | 401 | error_response | no-cache | (absent) |

Key design: expired_token and invalid_token share IDENTICAL bodies (error_response). Cache-Control differs: no-store vs no-cache. Set-Cookie present only for valid_token.

### 5.3 Headers Excluded from Fingerprint
- Date (volatile per-request)
- Server (deployment artifact)
- X-Request-Id (volatile UUID)

### 5.4 Headers Included in Fingerprint
- Cache-Control (varies by state)
- Set-Cookie (varies by state)
- Content-Type (constant)
- Content-Length (body-correlated)
- ETag (body-correlated, W/body_sha)

## 6. Fingerprinting

Deterministic SHA-256 of:
```python
repr((status, tuple(sorted(filtered_headers)), body_sha256, ''))
```

Where `filtered_headers` excludes Date, Server, X-Request-Id. Python 3.12.14.

## 7. Sampling

- N = 40 (4 states x 10 requests)
- Seed = 44 (for comparability with parent)
- Server jitter = 50-150ms uniform
- Client inter-request = 0-200ms
- Per-state: 10 requests, expect identical fingerprints within state

## 8. Baselines

| Baseline | Description | Expected Discrimination |
|----------|-------------|------------------------|
| B-STATUS-ONLY | Fingerprint based on status code only | 0.5 (2 statuses: 200, 401) |
| B-BODY-ONLY | Fingerprint based on body hash only | < 1.0 (expired/invalid share body, so 3 groups not 4) |
| B-URL-HASH | Fingerprint based on URL hash only | 0.0 (same endpoint) |
| B-RANDOM | Random assignment | ~0.0 |

### 8.1 Baseline Baseline Comparison
- B-BODY-ONLY expected: With expired/invalid sharing identical bodies, body-only can distinguish at most 3 groups (no_auth, valid_token, error_group). Discrimination should be less than 1.0.
- Full vector expected: If Cache-Control and Set-Cookie add information, full vector should distinguish all 4 states (Cache-Control differentiates expired vs invalid).

## 9. Measures

### 9.1 Primary Metric
- **full_vector_discrimination**: Jaccard-based discrimination score for full fingerprint vector
- **b_body_only_discrimination**: Jaccard-based discrimination score for body-only fingerprint
- **incremental_header_value**: full_vector_discrimination - b_body_only_discrimination

### 9.2 Secondary Metrics
- Cache-Control-only discrimination
- Set-Cookie-only discrimination
- Per-state fingerprint match rate (intra-state)
- Cross-state fingerprint match rate (inter-state)
- Mean inter-state Jaccard distance
- Bootstrap CI for full_vector_discrimination

### 9.3 Control Metrics
- Null FP rate (per-state identical fingerprints)
- Drift discriminability (valid_token vs expired_token Jaccard, expired_token vs invalid_token Jaccard)

## 10. Controls

### 10.1 Positive Control: Cache-Control Varies with State
Cache-Control-only discrimination > 0. Cache-Control is no-store for expired, no-cache for invalid, absent for no_auth/valid_token. If Cache-Control-only discrimination == 0, the experiment is MEASUREMENT_INVALID (headers do not actually vary as designed).

### 10.2 Null Control: Random Fingerprint
B-RANDOM discrimination ~ 0.0. Random assignment should not achieve meaningful discrimination.

### 10.3 Body Correlation Control: ETag Redundancy
ETag = W/body_sha is body-correlated by construction. ETag-only discrimination should equal body-only discrimination. This verifies body-correlated headers are correctly redundant.

### 10.4 Set-Cookie Control: Valid Token Only
Set-Cookie present only for valid_token. Set-Cookie-only discrimination should distinguish valid_token from other states (at least 3 groups: valid_token, others).

## 11. Decision Rule

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. full_vector_discrimination > B-BODY-ONLY
2. full_vector_discrimination > 0.5
3. null FP < 5%
4. Cache-Control-only discrimination > 0

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. full_vector_discrimination == B-BODY-ONLY (headers add no incremental value)
2. Cache-Control-only discrimination == 0 (headers do not vary with state)

### 11.3 MEASUREMENT_INVALID
If ANY of:
1. full_vector_discrimination <= 0.5 (primary threshold fails)
2. null FP > 5%
3. Server fails to start or respond
4. Fewer than 4 distinct fingerprints observed (setup error)

## 12. Validity Threats

### 12.1 Cache-Control Header Interpretation
Flask/Werkzeug may or may not support arbitrary Cache-Control values in responses. If Cache-Control is not actually present in responses, the experiment is MEASUREMENT_INVALID. Mitigation: verify Cache-Control presence in raw HTTP responses before fingerprinting.

### 12.2 ETag Correlation
ETag = W/body_sha is body-correlated by construction. When expired/invalid share identical bodies, ETag will also be identical. This is expected and does not affect the Cache-Control/Set-Cookie test.

### 12.3 Content-Length Correlation
Content-Length = body length. When expired/invalid share identical bodies, Content-Length will also be identical. This is expected and does not affect the Cache-Control/Set-Cookie test.

### 12.4 Sample Size
N=40 (4 states x 10 requests) provides 10 intra-state pairs per state for fingerprint matching. Sufficient for primary threshold test (>0.5) but limited power for fine-grained comparisons. Same as parent for comparability.

### 12.5 Jitter Range
Server jitter 50-150ms uniform, same as parent. Null FP < 5% expected under this range (established in parent and grandparent).

### 12.6 Python Version Dependency
repr(vector) is Python-version-dependent. Results validated only on Python 3.12.14. Cross-version reproducibility remains unknown (parent unknown).

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
Headers provide incremental value over body-only observation when bodies are not distinct. Cache-Control and Set-Cookie capture auth-state information that body alone cannot. Product architecture should use full vector observation. The H4 ceiling effect in parent was an artifact of distinct-body design, not a general property.

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
Headers add no incremental value even in degraded body scenarios. Body-only observation is sufficient. The H4 ceiling effect in parent reflects a genuine architectural property. Product can safely use body-only observation.

### 13.3 Invalid Result (MEASUREMENT_INVALID)
Infrastructure or setup failure. Not scientific evidence for or against.

## 14. Analysis Plan

1. **Setup Verification**: Confirm Cache-Control and Set-Cookie present in raw HTTP responses for each state
2. **Fingerprinting**: Compute full vector, body-only, status-only, URL-hash, random fingerprints for all 40 requests
3. **Discrimination**: Compute Jaccard-based discrimination score for each fingerprint method
4. **Baselines**: Compare full_vector_discrimination to B-BODY-ONLY, B-STATUS-ONLY, B-URL-HASH, B-RANDOM
5. **Controls**: Verify positive control (Cache-Control varies), null control (random ~ 0), body correlation (ETag = body-only)
6. **Bootstrap**: Compute bootstrap CI for full_vector_discrimination (1000 iterations, resample states with deduplication)
7. **Drift**: Compute Jaccard distances for valid_token vs expired_token, expired_token vs invalid_token
8. **Reporting**: Report all outcomes with equal prominence

## 15. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 16. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
