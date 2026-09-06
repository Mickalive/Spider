# EXP-RUNTIME-34015740602 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34015740602
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-06
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-RUNTIME-33902315583 (C-MEAS-VALID survives narrowly on Flask/JWT localhost)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does the HTTP fingerprint substrate maintain discrimination > 0.5 on a production-like OAuth/OIDC middleware with realistic response variation (cache-Control, ETag, X-Request-Id, Set-Cookie, rate-limit headers) — and does the full vector (status + body + all headers) ever exceed B-BODY-ONLY when headers vary independently with auth state?

## 3. Motivation

### What the parent experiment established (EXP-RUNTIME-33902315583)

The parent experiment tested C-MEAS-VALID on a real Flask 3.1.3 + PyJWT 2.13.0 HS256 server with 4 auth states, no synthetic headers, and standard headers only. It produced:

**Established:**
- Full-vector discrimination 0.833 > 0.5 on real Flask/JWT middleware
- Full vector equals B-BODY-ONLY exactly (0.833 = 0.833) — standard headers add zero discriminating information
- Full vector exceeds B-STATUS-ONLY (0.833 > 0.5) because body distinguishes no_auth from expired/invalid when all three share status 401
- Null FP rate 0.0% < 5% under server-side jitter 50-150ms
- valid_token vs expired_token drift discriminable (Jaccard 0.3505 < 0.5)
- expired_token vs invalid_token correctly non-discriminable (Jaccard 1.0 — identical bodies, correct behavior)
- Three mandatory fixes preserved: sorted-tuple fingerprint, Date/Server exclusion, competitive baselines

**Rejected:**
- Full observation vector adds value over body-only on Flask/JWT — REJECTED (0.833 = 0.833)
- Stdlib http.server results transfer to production — REJECTED
- C-MEAS-VALID is SUPPORTED for production OAuth/OIDC — REJECTED (claim ceiling narrow)

**Unknown:**
- Does substrate maintain discrimination on production OAuth/OIDC with additional response variation?
- Does full vector ever exceed B-BODY-ONLY when headers vary independently with auth state?
- What is FP rate under CDN/load-balancer variance or volatile headers?

**Do Not Assume:**
- Flask/JWT results transfer to production OAuth/OIDC
- Full observation vector is necessary for discrimination
- Null FP <5% holds beyond 50-150ms jitter
- Sample size N=40 is sufficient for subtle discrimination differences

### Why this experiment is different

The parent experiment used a minimal Flask/JWT server with only standard headers (Content-Type, Content-Length). Production OAuth/OIDC providers add realistic response variation that could affect discrimination:

1. **cache-Control varies by auth state**: Production providers return `no-store` for authenticated responses (preventing caching of sensitive data) and `no-cache` for error responses. This creates a header-level signal that varies with auth state.
2. **ETag is body-dependent**: Production providers return `ETag: W/"<hash>"` computed from the response body. This is correlated with body_hash but adds header-level information.
3. **Set-Cookie for authenticated responses**: Production providers return session cookies only for successful authentication. This is a binary header signal (present/absent) that varies with auth state.
4. **X-Request-Id is a UUID per request**: This is volatile and MUST be excluded from the fingerprint (it varies per request regardless of auth state). Testing this exclusion is important for production deployment.
5. **Bodies are DIFFERENT across error states**: Unlike the parent experiment (where expired and invalid shared identical bodies), this experiment uses distinct error messages for expired vs invalid tokens. This tests whether the substrate discriminates when bodies differ but status is shared.

The key test: **does full vector exceed B-BODY-ONLY when headers vary independently with auth state?** On the parent Flask/JWT server, full vector = B-BODY-ONLY because headers were constant. On production-like middleware, Set-Cookie and cache-Control may add independent discriminating information, making full vector > B-BODY-ONLY. Alternatively, if bodies are fully discriminative, full vector will still equal B-BODY-ONLY (headers are redundant with body).

## 4. Hypotheses

### H1: Discrimination Maintenance
Full-vector discrimination > 0.5 on production-like OAuth middleware with realistic header variation.

### H2: Null Control
Null FP rate < 5% under server-side jitter 50-150ms when X-Request-Id (volatile per-request UUID) is excluded from the fingerprint.

### H3: Drift Discrimination
valid_token vs expired_token drift pair is discriminable (Jaccard < 0.5).

### H4: Multi-Field Value (Exploratory)
Full vector exceeds B-BODY-ONLY when Set-Cookie and cache-Control vary with auth state. This is exploratory — the parent experiment found full vector = B-BODY-ONLY, and this may hold on production-like middleware if bodies are fully discriminative.

## 5. Server Design

### 5.1 OAuth-Like Middleware

Flask app with token introspection via local lookup (not external OIDC provider). Response headers are production-realistic:

| Auth State | Status | Body | cache-Control | Set-Cookie | ETag |
|------------|--------|------|---------------|------------|------|
| no_auth | 401 | {"error":"login_required","message":"Authentication required"} | no-cache | (absent) | W/"<body_sha>" |
| valid_token | 200 | {"sub":"alice","name":"Alice","email":"alice@example.com","iat":...,"exp":...} | no-store | session=<token> | W/"<body_sha>" |
| expired_token | 401 | {"error":"token_expired","message":"Token has expired"} | no-cache | (absent) | W/"<body_sha>" |
| invalid_token | 401 | {"error":"invalid_token","message":"Token validation failed"} | no-cache | (absent) | W/"<body_sha>" |

### 5.2 Key Differences from Parent

1. **Bodies are DIFFERENT across all 4 states** (parent had expired/invalid sharing identical bodies)
2. **cache-Control varies by auth state** (parent had constant Content-Type/Content-Length)
3. **Set-Cookie present only for valid_token** (parent had no cookies)
4. **ETag is body-dependent** (parent had no ETag)
5. **X-Request-Id is UUID per request** (EXCLUDED from fingerprint — tests volatile identifier exclusion)

### 5.3 Fingerprint Construction

```
fingerprint = SHA-256(
    status,
    tuple(sorted(headers excluding Date/Server/X-Request-Id)),
    body_sha256,
    redirect_chain
)
```

- **Excluded from vector**: Date (volatile), Server/Werkzeug (volatile), X-Request-Id (per-request UUID)
- **Included in vector**: Status, Content-Type, Content-Length, Cache-Control, ETag, Set-Cookie (when present)
- **Deterministic**: repr(vector) with tuple(sorted(...)) — inherited from parent fixes

## 6. Baselines

### B-STATUS-ONLY
SHA-256 of status code string only. Expected: discrimination ~0.5 (3 states share status 401; cannot distinguish no_auth from expired/invalid).

### B-BODY-ONLY
SHA-256 of response body bytes only. Expected: discrimination >= 0.833 (all 4 states have distinct bodies). May equal full vector if headers add no independent information.

### B-URL-HASH
SHA-256 of URL string only. Expected: 0.0 (URL is constant GET /api/userinfo).

### B-RANDOM
Random 256-bit fingerprints. Expected: ~0.0.

## 7. Controls

### 7.1 Positive Control
valid_token (200, unique body, Set-Cookie present) is distinguishable from all other states. Full-vector discrimination > 0.5.

### 7.2 Null Control
Repeated identical requests to the same auth state with server-side jitter (50-150ms): FP rate < 5%. Validates that jitter and per-request X-Request-Id do not cause false fingerprint variation.

### 7.3 Drift Control
valid_token -> expired_token: Jaccard < 0.5 (discriminable — status differs 200/401, body differs, Set-Cookie differs).
expired_token -> invalid_token: Jaccard may be < 0.5 (bodies are now DIFFERENT, unlike parent) — this tests whether distinct error bodies are discriminable.

## 8. Sample Size

- 4 auth states × 10 reps = 40 requests
- Randomized order with seed 44
- Server-side jitter: random.uniform(0.05, 0.15) seconds per request
- Client-side inter-request delay: random.uniform(0.0, 0.2) seconds

## 9. Statistical Tests

### 9.1 Primary: Discrimination
Full-vector discrimination = 1 - (intra_match_rate + inter_match_rate) / 2
Threshold: > 0.5

### 9.2 Null FP Rate
Per-state FP rate = (unique fingerprints - 1) / (total requests - 1)
Threshold: < 5%

### 9.3 Drift Jaccard
Jaccard(fingerprint_valid, fingerprint_expired) < 0.5

### 9.4 Baseline Comparison
Compare full-vector discrimination to B-STATUS-ONLY, B-BODY-ONLY, B-URL-HASH, B-RANDOM.
Report whether full vector >, =, or < B-BODY-ONLY.

## 10. Decision Rules

### 10.1 C-MEAS-VALID SURVIVES
If ALL of:
1. Full-vector discrimination > 0.5
2. Null control FP rate < 5%
3. valid_token vs expired_token drift discriminable (Jaccard < 0.5)
4. No server errors (>80% requests successful)

### 10.2 C-MEAS-VALID FALSIFIED
If ANY of:
1. Full-vector discrimination <= 0.5
2. Null FP > 5%
3. valid vs expired drift not discriminable

### 10.3 MEASUREMENT_INVALID
If:
1. Flask server fails to start
2. >20% request errors
3. Fingerprint construction errors

### 10.4 Product Architecture Constraint (Exploratory)
- If full vector > B-BODY-ONLY: multi-field observation adds value → product should use status + body + filtered headers
- If full vector = B-BODY-ONLY: body-only observation sufficient → simpler product architecture
- If full vector < B-BODY-ONLY: headers introduce noise → product should exclude volatile headers

## 11. Validity Threats

### 11.1 Mock vs Production
The server is a Flask app with local token introspection, not a real OAuth/OIDC provider (Auth0, Okta, Keycloak). Production providers may add CDN headers, load-balancer variance, rate-limiting, compressed encoding not captured here. **Mitigation**: this is the ecological validity extension from Flask/JWT to production-like headers; real provider testing is a future experiment.

### 11.2 X-Request-Id Exclusion
X-Request-Id is excluded from the fingerprint because it is a per-request UUID. If a production provider uses X-Request-Id that encodes auth state (e.g., different prefix per auth level), this exclusion would lose information. **Mitigation**: document the exclusion; future experiment can test whether request ID prefix is state-discriminative.

### 11.3 Body Distinctness
Unlike the parent experiment (expired/invalid sharing identical bodies), this experiment uses distinct error messages. This makes discrimination easier. **Mitigation**: the distinct-body design tests a different scenario (production-like where error messages differ); the parent's identical-body scenario is already established.

### 11.4 Sample Size
N=40 (4 states × 10 reps) is sufficient for the primary threshold test (>0.5) but limited statistical power for fine-grained baseline comparisons. **Mitigation**: report confidence intervals; primary test is threshold-based.

### 11.5 ETag Correlation
ETag is computed from body_hash, so it is perfectly correlated with body. It adds no independent information. **Mitigation**: document this; the experiment tests whether Set-Cookie and cache-Control (which are NOT correlated with body) add independent information.

## 12. Expected Outcomes

### 12.1 Discrimination Holds + Full Vector > B-BODY-ONLY
- Multi-field observation adds value on production-like middleware
- Set-Cookie and/or cache-Control provide independent discriminating information
- Product should use status + body + filtered headers (Cache-Control, Set-Cookie)
- C-MEAS-VALID claim ceiling extends to production-like OAuth

### 12.2 Discrimination Holds + Full Vector = B-BODY-ONLY
- Body is dominant signal (consistent with Flask/JWT finding)
- Headers are redundant with body even on production-like middleware
- Product can use body-only observation (simpler, fewer failure modes)
- C-MEAS-VALID claim ceiling extends to production-like OAuth

### 12.3 Discrimination Fails
- Substrate not viable for production auth drift detection
- Product must use alternative observation mechanisms
- C-MEAS-VALID does not survive beyond Flask/JWT localhost

### 12.4 Invalid Result
- Pipeline needs debugging
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Server Setup**: Start Flask app with OAuth-like middleware on localhost
2. **Data Collection**: 40 requests (4 states × 10 reps), randomized order, server-side jitter 50-150ms
3. **Raw Observations**: Persist status, all headers, body_hash, fingerprint, elapsed, timestamp per request
4. **Fingerprint Computation**: SHA-256 of (status, sorted headers excluding Date/Server/X-Request-Id, body_sha256, redirect_chain)
5. **Discrimination**: Compute intra/inter match rates, discrimination score
6. **Baselines**: Compute B-STATUS-ONLY, B-BODY-ONLY, B-URL-HASH, B-RANDOM
7. **Null FP**: Per-state false positive rate under jitter
8. **Drift**: Jaccard between valid_token and expired_token fingerprints
9. **Comparison**: Full vector vs B-BODY-ONLY (>, =, <)
10. **Controls**: Verify positive, null, drift controls
11. **Reporting**: Report all outcomes with equal prominence

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
