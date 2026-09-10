# EXP-RUNTIME-34509593940 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34509593940
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Parent**: EXP-RUNTIME-34439061845 (WWW-Authenticate transfer falsified, body-only architecture)
- **Date**: 2026-09-10
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can body-only HTTP fingerprint observation (body hash as sole discriminating signal) maintain auth-state discrimination across production-like Keycloak middleware with non-deterministic infrastructure headers that add CDN, load-balancer, compression, and rate-limit noise?

## 3. Motivation

The parent experiment (EXP-RUNTIME-34439061845) established:

1. WWW-Authenticate discrimination is /userinfo-specific, not Keycloak-level (0/3 endpoints)
2. Body-only observation is the robust architecture for auth-state discrimination
3. /userinfo: full-vector = WWW-Auth-only = 0.833, body-only = 0.5
4. /introspect: full-vector = body-only = 0.5
5. expired_token and invalid_token are indistinguishable by any observable

The parent handoff poses: "Can body-only HTTP fingerprint observation maintain auth-state discrimination across production-like Keycloak middleware with CDN, load-balancer, compression, and rate-limit headers that add non-deterministic variance to responses?"

This experiment directly tests that question by deploying a reverse proxy that injects realistic infrastructure headers at controlled noise intensities.

## 4. Hypotheses

### H1: Body-Only Invariance (M_BODY_ONLY_INVARIANT)
Body-only discrimination on /userinfo remains >= 0.7 across all noise levels (0, 1, 2, 4 injected headers).

**Rationale**: Body-only fingerprints hash only (status, body). Since infrastructure noise adds headers (not body changes), body-only should be completely invariant.

### H2: Weak-Body Invariance (M_WEAK_BODY_INVARIANT)
Body-only discrimination on /introspect remains >= 0.3 across all noise levels.

**Rationale**: /introspect has body-only discrimination of 0.5 (weaker signal). Even if body-only is invariant, the floor is lower. 0.3 is the minimum useful threshold.

### H3: Noise Degradation (M_NOISE_DEGRADATION)
Full-vector discrimination on /userinfo degrades monotonically with noise intensity (Spearman rho <= -0.5 between full-vector discrimination and noise level).

**Rationale**: Full-vector fingerprints include headers. Non-deterministic headers create within-state fingerprint variation, reducing intra-match rate and thus discrimination.

### H4: Positive Control
At noise=0, /userinfo body-only discrimination >= 0.8 (parent observed 0.833).

**Rationale**: Confirms the measurement pipeline reproduces the parent result before noise injection.

### H5: Null Control
At noise=0, /userinfo body-only discrimination > 0.4.

**Rationale**: Floor is 0.4 because expired and invalid tokens are indistinguishable by body (3 distinct body groups: valid=200, no_auth=401, expired==invalid=401).

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
- Expected discrimination: body-only >= 0.8 at noise=0

### 6.2 Secondary: /introspect (POST)
- URL: http://127.0.0.1:18081/realms/spider-test/protocol/openid-connect/token/introspect (via proxy)
- Method: POST
- Body: token=<token>&client_id=spider-client&client_secret=spider-secret-12345
- Expected discrimination: body-only = 0.5 at noise=0

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
- **M_BODY_ONLY_DISC_NOISE{0,1,2,4}_USERINFO**: Body-only discrimination on /userinfo at each noise level
- **M_FULL_VECTOR_DISC_NOISE{0,1,2,4}_USERINFO**: Full-vector discrimination on /userinfo at each noise level
- **M_BODY_ONLY_DISC_NOISE{0,1,2,4}_INTROSPECT**: Body-only discrimination on /introspect at each noise level
- **M_FULL_VECTOR_DISC_NOISE{0,1,2,4}_INTROSPECT**: Full-vector discrimination on /introspect at each noise level

### Derived Metrics
- **M_NOISE_DEGRADATION**: Spearman rho between full-vector discrimination and noise level on /userinfo
- **M_BODY_ONLY_INVARIANT**: min body-only discrimination across noise levels on /userinfo
- **M_WEAK_BODY_INVARIANT**: min body-only discrimination across noise levels on /introspect
- **M_NOISE_CURVE_SLOPE**: Linear regression slope of full-vector discrimination vs noise level on /userinfo

### Control Metrics
- **M_POSITIVE_CONTROL**: Body-only discrimination at noise=0 on /userinfo (must >= 0.8)
- **M_NULL_CONTROL**: Body-only discrimination at noise=0 on /userinfo (must > 0.4)

## 11. Controls

### 11.1 Positive Control (noise=0, /userinfo)
- Body-only discrimination must >= 0.8
- Verifies: pipeline reproduces parent result (0.833)
- Tolerance: 0.05 below parent (session timing variation)

### 11.2 Null Control (noise=0, /userinfo)
- Body-only discrimination must > 0.4
- Verifies: pipeline does not produce spurious noise
- Floor: 3 distinct body groups (valid=200, no_auth=401, expired==invalid=401)

### 11.3 Noise-Invariance Control
- Body-only discrimination at noise=4 must equal body-only at noise=0 on /userinfo (within 0.02)
- Verifies: body-only is truly invariant to header noise
- This is the primary scientific test

### 11.4 Degradation Control
- Full-vector discrimination at noise=4 must be < full-vector at noise=0 on /userinfo
- Verifies: header noise actually degrades full-vector as expected

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

## 13. Decision Rules

### 13.1 SURVIVES_CURRENT_TEST
If ALL of:
1. M_POSITIVE_CONTROL >= 0.8 (positive control passes)
2. M_NULL_CONTROL > 0.4 (null control passes)
3. M_BODY_ONLY_INVARIANT >= 0.7 (body-only discrimination >= 0.7 at ALL noise levels on /userinfo)
4. M_WEAK_BODY_INVARIANT >= 0.3 (body-only discrimination >= 0.3 at ALL noise levels on /introspect)
5. M_NOISE_DEGRADATION <= -0.5 (full-vector degrades with noise on /userinfo)
6. No pipeline errors

### 13.2 FALSIFIED-IN-SETTING
If ANY of:
1. M_BODY_ONLY_INVARIANT < 0.7 (body-only degrades under header noise on /userinfo)
2. M_NOISE_DEGRADATION > -0.5 (full-vector does NOT degrade, body-only advantage is marginal)

### 13.3 MEASUREMENT_INVALID
If:
1. M_POSITIVE_CONTROL < 0.8 (pipeline does not reproduce parent result)
2. M_NULL_CONTROL <= 0.4 (pipeline produces spurious noise)
3. Keycloak fails to start or proxy fails
4. Insufficient data (< 8 reps per cell)

### 13.4 MIXED
If body-only invariant holds but degradation is marginal (-0.5 < rho < 0):
- Body-only is robust but full-vector does not clearly degrade
- Product implication: body-only is safe but full-vector may also be acceptable
- Verdict ceiling: CONSTRAINED rather than SURVIVES

## 14. Expected Outcomes

### 14.1 Positive Result (SURVIVES_CURRENT_TEST)
- Body-only fingerprint discrimination is production-ready under infrastructure noise
- SPIDER can safely use body-hash-only observation in production with CDN/load-balancer/compression/rate-limit
- Product architecture should adopt body-only as default fingerprint strategy
- No further infrastructure-robustness testing needed for body-only

### 14.2 Negative Result (FALSIFIED-IN-SETTING)
- Body-only discrimination degrades under header noise
- Product must invest in noise-robust body normalization or retain header-aware fingerprinting
- The EXP-RUNTIME-34439061845 body-only recommendation must be revised
- New experiment needed: body normalization techniques for noisy infrastructure

### 14.3 Mixed Result (MIXED)
- Body-only is invariant but full-vector does not degrade
- Both approaches may be acceptable in production
- Product can choose based on implementation simplicity (body-only is simpler)
- No strong evidence against either approach

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
