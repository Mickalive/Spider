# EXP-RUNTIME-34509593940 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34509593940
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Parent**: EXP-RUNTIME-34439061845 (WWW-Authenticate transfer falsified, body-only architecture identified)
- **Date**: 2026-09-10
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does body-only HTTP fingerprint observation maintain auth-state discrimination when production-like infrastructure (reverse proxy injecting non-deterministic CDN/load-balancer/rate-limit headers) adds response header noise, and does full-vector discrimination degrade under the same conditions?

## 3. Motivation

The parent experiment (EXP-RUNTIME-34439061845) established:

1. WWW-Authenticate discrimination is /userinfo-specific, not Keycloak-level (0/3 additional endpoints)
2. Body-only observation is the robust architecture for auth-state discrimination
3. /userinfo: full-vector = 0.833, body-only = 0.5 (WWW-Auth is the discriminating header)
4. /introspect: full-vector = body-only = 0.5 (headers add nothing)
5. expired_token and invalid_token are indistinguishable by any observable

The parent handoff asks: "Can body-only HTTP fingerprint observation maintain auth-state discrimination across production-like Keycloak middleware with CDN, load-balancer, compression, and rate-limit headers?"

**Key insight**: Body-only fingerprints hash only (status, body). Response header noise cannot affect body-only discrimination by construction. The real scientific question is whether full-vector discrimination degrades under header noise, which would justify body-only as the default production strategy. Body-only invariance is a sanity check, not a novel finding.

## 4. Hypotheses

### H1: Noise Degradation (M_NOISE_DEGRADATION) — PRIMARY
Full-vector discrimination on /userinfo degrades with increasing noise intensity (Spearman rho <= -0.3 between full-vector discrimination and noise level).

**Rationale**: Full-vector fingerprints include headers. Non-deterministic headers create within-state fingerprint variation, reducing the intra-match rate and thus discrimination. If this fails, headers are reliable even under noise and body-only offers no advantage.

### H2: Body-Only Invariance (M_BODY_ONLY_INVARIANT) — SANITY CHECK
Body-only discrimination on /userinfo does not degrade with noise (Spearman rho >= -0.3).

**Rationale**: Body-only fingerprints exclude headers. Since noise only adds headers, body-only should be invariant. Failure would indicate the proxy is modifying bodies (measurement failure, not scientific finding).

### H3: Noise-Invariance Bound (M_NOISE_BOUND)
Body-only discrimination at noise=4 is within 0.05 of body-only at noise=0 on /userinfo.

**Rationale**: Quantitative bound on invariance. If body-only varies by more than 0.05, the proxy is not correctly isolating header noise.

### H4: Positive Control
At noise=0, /userinfo body-only discrimination >= 0.35 (parent observed 0.5; tolerance accounts for session timing and N=10).

**Rationale**: Confirms the pipeline reproduces the expected 3-group body-only pattern (valid, no_auth, expired==invalid) before noise injection. The threshold is set conservatively because body-only discrimination of 0.5 with N=10 per state has limited precision.

### H5: Null Control
At noise=0, B-RANDOM discrimination ~ 0.0.

**Rationale**: Random fingerprints should not achieve meaningful discrimination. Verifies measurement pipeline stability.

## 5. Infrastructure

### 5.1 Keycloak Setup
- Docker: quay.io/keycloak/keycloak:25.0, start-dev mode
- Port: 18080 (same as parent experiments)
- Realm: spider-test
- Client: spider-client (client_secret, directAccessGrantsEnabled)
- User: alice / alice123
- Configuration identical to parent EXP-RUNTIME-34439061845

### 5.2 Reverse Proxy
- Python HTTP server on port 18081
- Forwards all requests to Keycloak on 18080
- Adds noise headers to responses based on configured noise level
- Does NOT modify: response body, status code, auth-related headers (Cache-Control, WWW-Authenticate, Set-Cookie, Content-Type)
- Noise injection is per-response (different random values per request)

### 5.3 Noise Levels
| Level | Headers Added | Count | Header Pool |
|-------|--------------|-------|-------------|
| 0 | None | 0 | — |
| 1 | X-Cache-Status | 1 | HIT/MISS/EXPIRED |
| 2 | X-Cache-Status, X-CDN-Request-Id | 2 | HIT/MISS/EXPIRED, random UUID |
| 4 | X-Cache-Status, X-CDN-Request-Id, X-Edge-Location, X-Rate-Limit-Remaining | 4 | HIT/MISS/EXPIRED, random UUID, random edge code, random int 0-100 |

### 5.4 Noise Header Values
- X-Cache-Status: randomly chosen from {HIT, MISS, EXPIRED} per request
- X-CDN-Request-Id: random UUID4 per request
- X-Edge-Location: random 2-letter code from {US, EU, AP, SA, AF} per request
- X-Rate-Limit-Remaining: random integer 0-100 per request
- All values are infrastructure-irrelevant (not related to auth state)

## 6. Endpoints

### 6.1 Primary: /userinfo (GET)
- URL: http://127.0.0.1:18081/realms/spider-test/protocol/openid-connect/userinfo (via proxy)
- Method: GET
- Auth: Authorization header (varies by state)
- Expected body-only discrimination: 0.5 at noise=0 (parent baseline)
- Expected full-vector discrimination: 0.833 at noise=0 (WWW-Auth contributes 0.333)

### 6.2 Secondary: /introspect (POST)
- URL: http://127.0.0.1:18081/realms/spider-test/protocol/openid-connect/token/introspect (via proxy)
- Method: POST
- Body: token=<token>&client_id=spider-client&client_secret=spider-secret-12345
- Expected body-only discrimination: 0.5 at noise=0 (active:true/false)
- Expected full-vector discrimination: 0.5 at noise=0 (headers add nothing on /introspect)

## 7. Auth States

| State | Authorization Header | Expected Status |
|-------|---------------------|-----------------|
| no_auth | (none) | 401 |
| valid_token | Bearer <keycloak_token> | 200 |
| expired_token | Bearer <expired_jwt> | 401 |
| invalid_token | Bearer not-a-real-jwt-token | 401 |

Note: expired_token is locally-signed HS256, not Keycloak-issued. Keycloak treats it as invalid_signature (V6 state construction leakage, carried forward from parent).

## 8. Fingerprint Algorithms

### 8.1 Full-Vector Fingerprint (identical to parent)
```
body_hash = SHA256(response.body)
filtered_headers = {k:v for k,v in response.headers if k.lower() not in EXCLUDED_HEADERS}
vector = (status, tuple(sorted(filtered_headers.items())), body_hash, redirect_chain)
fingerprint = SHA256(repr(vector))
```
EXCLUDED_HEADERS = {date, server, x-request-id}

### 8.2 Body-Only Fingerprint
```
body_hash = SHA256(response.body)
vector = (status, body_hash, '')
fingerprint = SHA256(repr(vector))
```

### 8.3 Discrimination Score
```
discrimination = intra_match_rate - inter_match_rate
```
Where intra_match_rate = fraction of same-state fingerprint pairs that match, inter_match_rate = fraction of different-state fingerprint pairs that match.

## 9. Sample Size

- 4 auth states x 10 repetitions x 4 noise levels x 2 endpoints = 320 total requests
- Per cell: 10 fingerprints per state
- Intra-state pairs per state: C(10,2) = 45
- Total intra-state pairs per endpoint per noise level: 4 x 45 = 180
- Total inter-state pairs per endpoint per noise level: C(4,2) x 10 x 10 = 600

## 10. Measures

### Primary Metrics
- **M_FULL_VECTOR_DISC_NOISE{0,1,2,4}_USERINFO**: Full-vector discrimination on /userinfo at each noise level
- **M_BODY_ONLY_DISC_NOISE{0,1,2,4}_USERINFO**: Body-only discrimination on /userinfo at each noise level
- **M_FULL_VECTOR_DISC_NOISE{0,1,2,4}_INTROSPECT**: Full-vector discrimination on /introspect at each noise level
- **M_BODY_ONLY_DISC_NOISE{0,1,2,4}_INTROSPECT**: Body-only discrimination on /introspect at each noise level

### Derived Metrics
- **M_NOISE_DEGRADATION**: Spearman rho between full-vector discrimination and noise level on /userinfo (PRIMARY — must be <= -0.3)
- **M_BODY_ONLY_INVARIANT**: Spearman rho between body-only discrimination and noise level on /userinfo (SANITY CHECK — must be >= -0.3)
- **M_NOISE_BOUND**: |body_only_noise=4 - body_only_noise=0| on /userinfo (must be <= 0.05)

### Control Metrics
- **M_POSITIVE_CONTROL**: Body-only discrimination at noise=0 on /userinfo (must >= 0.35)
- **M_NULL_CONTROL**: B-RANDOM discrimination at noise=0 (must ~ 0.0)

## 11. Controls

### 11.1 Positive Control (noise=0, /userinfo)
- Body-only discrimination must >= 0.35
- Verifies: pipeline produces 3-group body-only pattern (valid, no_auth, expired==invalid)
- Parent observed 0.5; tolerance accounts for N=10 precision and session timing

### 11.2 Null Control (noise=0)
- B-RANDOM discrimination must ~ 0.0
- Verifies: pipeline does not produce spurious structure from random fingerprints

### 11.3 Degradation Control (PRIMARY)
- Full-vector discrimination at noise=4 must be < full-vector at noise=0 on /userinfo
- Verifies: header noise actually degrades full-vector as expected
- This is the core scientific test

### 11.4 Invariance Control (SANITY CHECK)
- Body-only discrimination at noise=4 must equal body-only at noise=0 on /userinfo (within 0.05)
- Verifies: proxy is correctly isolating header noise (not modifying bodies)
- Failure indicates measurement problem, not scientific finding

## 12. Validity Threats

### 12.1 Proxy Fidelity
The Python reverse proxy may not perfectly replicate CDN/load-balancer behavior. Mitigation: noise headers are drawn from real CDN header names and value distributions. The test is about header noise sensitivity, not specific CDN behavior.

### 12.2 Body Determinism
The proxy does NOT modify response bodies. In real production, CDN compression could produce non-deterministic bodies. This experiment does NOT test body non-determinism. Mitigation: explicitly stated as scope limitation. Body non-determinism is a separate, harder problem.

### 12.3 Sample Size
With 10 repetitions per cell, discrimination score estimates have limited precision. Mitigation: 10 reps is consistent with parent experiments; discrimination is a binary match/mismatch metric with high signal-to-noise.

### 12.4 Keycloak State Construction
expired_token is locally-signed HS256, not Keycloak-issued. Keycloak treats it as invalid_signature. This is the V6 leakage carried forward from parent. Mitigation: explicitly stated in do_not_assume; does not affect body-only discrimination (expired==invalid by body).

### 12.5 Single Infrastructure Pattern
Only one proxy noise pattern is tested. Real production has multiple infrastructure layers. Mitigation: this is the smallest informative test. If body-only survives, more complex patterns can be tested later.

### 12.6 Body-Only Invariance is Tautological
Body-only fingerprints exclude headers by construction. Header noise cannot affect body-only discrimination unless the proxy modifies bodies. The invariance hypothesis is a sanity check, not a scientific finding. Mitigation: the primary test is full-vector degradation (H1), which is falsifiable and scientifically meaningful.

## 13. Decision Rules

### 13.1 SURVIVES_CURRENT_TEST
If ALL of:
1. M_POSITIVE_CONTROL >= 0.35 (positive control passes)
2. M_NULL_CONTROL ~ 0.0 (null control passes)
3. M_NOISE_DEGRADATION <= -0.3 (full-vector degrades with noise on /userinfo)
4. M_BODY_ONLY_INVARIANT >= -0.3 (body-only does not degrade on /userinfo)
5. M_NOISE_BOUND <= 0.05 (body-only noise-invariance bound)
6. No pipeline errors

### 13.2 FALSIFIED-IN-SETTING
If ANY of:
1. M_NOISE_DEGRADATION > -0.3 (full-vector does NOT degrade, body-only offers no advantage)
2. M_BODY_ONLY_INVARIANT < -0.3 AND M_NOISE_BOUND > 0.05 (body-only degrades — proxy modifying bodies, but this is MEASUREMENT_INVALID if confirmed)

### 13.3 MEASUREMENT_INVALID
If:
1. M_POSITIVE_CONTROL < 0.35 (pipeline does not reproduce parent pattern)
2. M_BODY_ONLY_INVARIANT < -0.3 (body-only degrades — proxy modifying bodies, not just headers)
3. Keycloak fails to start or proxy fails
4. Insufficient data (< 8 reps per cell)

### 13.4 CONSTRAINED
If body-only invariant holds AND full-vector degradation is marginal (-0.3 < rho < 0):
- Body-only is robust but full-vector does not clearly degrade
- Product implication: body-only is safe but full-vector may also be acceptable
- Verdict ceiling: CONSTRAINED rather than SURVIVES

## 14. Expected Outcomes

### 14.1 Positive Result (SURVIVES_CURRENT_TEST)
- Full-vector discrimination degrades under header noise; body-only remains stable
- Body-only is the correct default production fingerprint strategy
- SPIDER should ignore response headers in production environments with CDN/load-balancer/rate-limit
- The EXP-RUNTIME-34439061845 body-only recommendation is validated for production

### 14.2 Negative Result (FALSIFIED-IN-SETTING)
- Full-vector does NOT degrade under header noise
- Headers are reliable even under infrastructure noise
- Product should use full-vector (which achieves 0.833 on /userinfo vs body-only 0.5)
- The EXP-RUNTIME-34439061845 body-only recommendation is revised

### 14.3 Mixed Result (CONSTRAINED)
- Body-only is invariant but full-vector degradation is marginal
- Both approaches may be acceptable in production
- Product can choose based on implementation simplicity (body-only is simpler)
- No strong evidence against either approach

### 14.4 Invalid Result (MEASUREMENT_INVALID)
- Pipeline failure, not scientific evidence
- Need to debug proxy before this question can be answered

## 15. Analysis Plan

1. **Infrastructure Setup**: Start Keycloak Docker, configure realm, start reverse proxy
2. **Data Collection**: For each noise level (0, 1, 2, 4), for each endpoint (/userinfo, /introspect), for each auth state (4), make 10 requests through the proxy
3. **Fingerprinting**: Compute both full-vector and body-only fingerprints for each response
4. **Discrimination**: Compute discrimination scores per noise level per endpoint per fingerprint type
5. **Controls**: Verify positive and null controls at noise=0
6. **Degradation Analysis**: Spearman correlation between full-vector discrimination and noise level
7. **Invariance Analysis**: Check body-only discrimination stability across noise levels
8. **Reporting**: Report all outcomes with equal prominence

## 16. Analysis Code

Analysis will be implemented in Python using:
- `requests` for HTTP (same as parent)
- `hashlib` for SHA-256 fingerprinting (same as parent)
- `jwt` for token generation (same as parent)
- `scipy.stats` for Spearman correlation
- `http.server` for reverse proxy
- Standard library only for proxy logic

Code will be committed to `research/experiments/EXP-RUNTIME-34509593940/` before execution.

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
