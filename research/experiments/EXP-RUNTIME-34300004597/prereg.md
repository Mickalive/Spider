# EXP-RUNTIME-34300004597 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34300004597
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Parent**: EXP-RUNTIME-34054515149 (SURVIVES_CURRENT_TEST, full 1.0 > body 0.833, incremental 0.167)
- **Date**: 2026-09-09
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the HTTP fingerprint substrate maintain full-vector discrimination and incremental header value on a real OAuth/OIDC identity provider (self-hosted Keycloak) where Cache-Control and Set-Cookie patterns are determined by the IdP middleware rather than application-set per auth state?

## 3. Motivation

### Parent Chain Summary

- **EXP-RUNTIME-33902315583**: C-MEAS-VALID survives narrowly on Flask/PyJWT localhost with standard headers. Full == B-BODY-ONLY (0.833 = 0.833) — body is dominant signal.
- **EXP-RUNTIME-34015740602**: H4 ceiling confound identified. Full == B-BODY-ONLY (1.0 = 1.0) reflects body dominance under distinct-body design, not proof headers are non-discriminative.
- **EXP-RUNTIME-34054515149**: H4 ceiling confound resolved. When expired/invalid share identical bodies, Cache-Control no-store vs no-cache provides 0.167 incremental discrimination (full 1.0 vs body 0.833). But audit V4 (ENGINEERED-HEADER-TAUTOLOGY-CONSTRAINT) established that incremental header value is by construction (application-set Cache-Control/Set-Cookie per auth state in Flask middleware), not discovery of natural production header variance.

### The Ecological Validity Gap

The parent claim ceiling is bounded to Flask 3.1.3 + PyJWT 2.13.0 HS256 on localhost with application-set headers. The V4 audit explicitly identified this as the critical unknown:

> "The incremental header value is by construction (application-set Cache-Control/Set-Cookie per auth state in Flask middleware), not discovery of natural production header variance."

On a real OAuth/OIDC provider (Keycloak, Auth0, Okta):
- Cache-Control may be constant or absent across all auth states
- Set-Cookie patterns are determined by IdP middleware, not application code
- Headers may include CDN/load-balancer artifacts not present in Flask

If Cache-Control is constant on the real IdP, full vector will equal B-BODY-ONLY (no incremental header value), and the product recommendation to use full vector does not transfer.

This experiment is the ecological validity test that the parent audit identified as the highest-priority next step for C-MEAS-VALID.

## 4. Hypotheses

### H1: IdP Header Variation
Keycloak naturally varies Cache-Control by auth state: no-store for expired_token, no-cache for invalid_token (matching Flask behavior). Cache-Control-only discrimination > 0.

### H2: Incremental Header Value
Full-vector discrimination > B-BODY-ONLY on Keycloak. Cache-Control and Set-Cookie provide independent discriminating information that body-only observation cannot capture.

### H3: Positive Control
Full-vector discrimination > 0.5 (primary threshold). Null FP < 5% under natural network jitter.

### H4: Ecological Validity
The incremental header value observed on Flask (0.167) transfers to Keycloak, demonstrating that the V4 tautology constraint does not limit product applicability. Alternatively, if incremental header value = 0, the V4 tautology is confirmed.

## 5. Keycloak Setup

### 5.1 Deployment
- Keycloak 25.x via Docker (`quay.io/keycloak/keycloak:25.0`)
- Dev mode (`start-dev`) on localhost:8080
- Realm: `spider-test`
- Client: `spider-client` (confidential, direct access grants enabled)

### 5.2 Auth States
1. **no_auth**: No Authorization header → 401 Unauthorized
2. **valid_token**: Bearer <valid HS256 JWT> → 200 OK with user profile body
3. **expired_token**: Bearer <expired JWT> → 401 with error body
4. **invalid_token**: Bearer <malformed token> → 401 with IDENTICAL error body

### 5.3 Body Design
- expired_token and invalid_token return IDENTICAL JSON error bodies (same as Flask parent)
- This is the critical design: body-only cannot distinguish these two states
- Any discrimination beyond body-only must come from headers

### 5.4 Header Observations (Not Controlled)
- Cache-Control: determined by Keycloak middleware (NOT application-set)
- Set-Cookie: determined by Keycloak session management
- ETag: body-correlated (W/body_sha), expected redundant
- Other headers: any IdP-specific headers (WWW-Authenticate, X-Content-Type-Options, etc.)

## 6. Measurement Protocol

### 6.1 Fingerprint
Deterministic SHA-256 of sorted-tuple vector:
```
SHA-256(repr((status, tuple(sorted(filtered_headers.items())), body_sha256, '')))
```
Excludes: Date, Server, X-Request-Id (volatile per-request, inherited from parent)

### 6.2 Sampling
- N = 40 requests (4 states x 10 reps)
- Randomized execution order (seed 44 for comparability with parent)
- Natural network jitter (no synthetic jitter — IdP has its own timing)
- Inter-request delay: 0-200ms (client-side)

### 6.3 Baselines
- B-STATUS-ONLY: SHA-256(status code only) → expected ~0.5
- B-BODY-ONLY: SHA-256(body bytes only) → expected < 1.0 (expired/invalid share body)
- B-URL-HASH: SHA-256(URL only) → expected 0.0
- B-RANDOM: random 256-bit → expected ~0.0

### 6.4 Single-Header Discrimination
- Cache-Control-only: SHA-256(Cache-Control value) per state
- Set-Cookie-only: SHA-256(Set-Cookie value) per state
- ETag-only: SHA-256(ETag value) per state (body correlation control)

## 7. Controls

### 7.1 Positive Control: Cache-Control Variation
Cache-Control-only discrimination > 0. If Keycloak does not vary Cache-Control by auth state, this control fails and the V4 tautology is confirmed on a real IdP.

### 7.2 Positive Control: Set-Cookie Variation
Set-Cookie-only discrimination > 0. If Keycloak does not vary Set-Cookie by auth state, Set-Cookie adds no information.

### 7.3 Null Control: Random Fingerprint
B-RANDOM discrimination ~ 0.0. Verifies pipeline does not produce spurious discrimination.

### 7.4 Body Correlation Control: ETag Redundancy
ETag-only discrimination ≈ B-BODY-ONLY. ETag is body-correlated by construction and should add no independent information.

### 7.5 Body Identity Control
expired_token and invalid_token share identical body hashes. Verifies the key design constraint.

### 7.6 Error Rate Control
Error rate < 20%. Too many failed requests indicate infrastructure instability.

### 7.7 Drift Discriminability
Consecutive state pairs (valid→expired, expired→invalid) have Jaccard < 0.5 (discriminable).

## 8. Decision Rules

### 8.1 SURVIVES_CURRENT_TEST
If ALL of:
1. full_vector_discrimination > B-BODY-ONLY (incremental header value exists)
2. full_vector_discrimination > 0.5 (primary threshold)
3. null FP < 5% (measurement stability)
4. Cache-Control-only discrimination > 0 (IdP varies Cache-Control)

### 8.2 FALSIFIED-IN-SETTING
If ANY of:
1. full_vector_discrimination == B-BODY-ONLY (no incremental header value on real IdP)
2. Cache-Control-only discrimination == 0 (IdP does not vary Cache-Control by auth state)

### 8.3 MEASUREMENT_INVALID
If:
1. full_vector_discrimination <= 0.5 (fails primary threshold)
2. null FP > 5% (measurement instability)
3. Error rate > 20% (infrastructure failure)

### 8.4 BLOCKED
If Keycloak deployment fails (Docker unavailable, port conflict, configuration error). This is infrastructure failure, not scientific falsification.

## 9. Validity Threats

### 9.1 Docker/Infrastructure Availability
Keycloak requires Docker. If Docker is not available in the runner environment, the experiment is BLOCKED. Mitigation: document exact failure and smallest unblocking action (install Docker, use different runner, use Auth0 test tenant).

### 9.2 Keycloak Configuration Variability
Keycloak's Cache-Control/Set-Cookie behavior may depend on version, configuration, and endpoint. Mitigation: document exact Keycloak version and configuration; test the /userinfo endpoint specifically.

### 9.3 Body Identity Guarantee
expired_token and invalid_token must return identical bodies. Keycloak may return different error messages for expired vs invalid tokens. Mitigation: configure custom error mapper or use identical token formats that produce identical error responses.

### 9.4 Synthetic-to-Real Gap
Keycloak localhost is still not production OAuth/OIDC with CDN, load-balancer, and rate-limit headers. This experiment narrows the gap but does not eliminate it.

### 9.5 Sample Size
N=40 (4 states x 10 reps) is the same as the parent. Sufficient for primary discrimination test but limited power for fine-grained comparisons.

### 9.6 Python Version Dependence
repr(vector) is Python-version-dependent. Fingerprints will not reproduce across Python versions. This is a known limitation inherited from the parent.

## 10. Analysis Plan

1. **Deploy Keycloak**: Docker container with pre-configured realm and client
2. **Generate tokens**: valid (HS256), expired (HS256, exp in past), invalid (malformed string)
3. **Execute requests**: 40 requests in randomized order (seed 44)
4. **Capture observations**: status, headers, body, timing per request
5. **Compute fingerprints**: full vector, baselines, single-header
6. **Compute discrimination**: intra/inter match rates, Jaccard similarities
7. **Bootstrap CI**: 1000 bootstrap resamples for discrimination score
8. **Controls**: positive (CC, SC), null (random), body correlation (ETag), body identity, error rate, drift
9. **Decision**: Apply frozen decision rule
10. **Report**: raw observations, derived metrics, interpretation bounded by measurements

## 11. Expected Outcomes

### 11.1 Positive Result (SURVIVES_CURRENT_TEST)
- IdP naturally varies Cache-Control/Set-Cookie by auth state
- Full vector > body-only on real OAuth/OIDC
- Product recommendation to use full vector is ecologically valid
- V4 tautology constraint does not limit product applicability
- C-MEAS-VALID claim extends to real IdP pattern

### 11.2 Negative Result (FALSIFIED-IN-SETTING)
- IdP does not vary Cache-Control by auth state (or variation is constant)
- Full vector == body-only on real OAuth/OIDC
- V4 tautology confirmed: incremental header value was by construction in Flask
- Product architecture should use body-only observation
- C-MEAS-VALID claim remains bounded to synthetic Flask pattern

### 11.3 Invalid Result (MEASUREMENT_INVALID)
- Infrastructure instability (high error rate, measurement noise)
- Not scientific evidence for or against
- Redesign required

### 11.4 Blocked Result (BLOCKED)
- Docker unavailable or Keycloak deployment fails
- Not scientific evidence
- Document exact failure and unblocking action

## 12. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 13. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
