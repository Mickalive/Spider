# EXP-RUNTIME-33805283356 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-33805283356
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-03
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

On a constant-URL server where auth state varies and response bodies differ accordingly, does the HTTP fingerprint substrate maintain discrimination — and does the full observation vector exceed single-field baselines (B-STATUS-ONLY, B-BODY-ONLY) when bodies vary with auth state?

## 3. Motivation

Prior Runtime work (EXP-RUNTIME-33767375933) established:
- Deterministic sorted-tuple fingerprint achieves discrimination 1.0 on a 5-state toy server with client-side jitter
- Date/Server header exclusion prevents spurious variance
- B-STATUS-ONLY (0.7) and B-BODY-ONLY (1.0) are competitive baselines on the toy server
- Phase B httpbin.org was URL-tautological: status code encoded in URL path, B-URL-HASH=1.0, B-STATUS-ONLY=1.0, full vector adds nothing (audit V1-EXTERNAL-TAUTOLOGY)

The parent handoff identified the critical gap: **all prior discrimination tests used either hand-programmed servers (toy) or URL-tautological endpoints (httpbin).** No test exists for a server where (a) the URL is constant, (b) auth state varies, (c) response bodies differ with auth state, and (d) the server is real (not hand-programmed to return fixed responses).

This experiment fills that gap using a Flask app with real auth middleware, constant URL, and auth-varying responses.

## 4. Hypotheses

### H1: Full-Vector Discrimination
The deterministic sorted-tuple fingerprint achieves discrimination score > 0.5 on the constant-URL Flask server with 5 auth states.

### H2: Full Vector Exceeds Status-Only
B-STATUS-ONLY discrimination < full-vector discrimination. This is expected because 3 of 5 auth states return status 200 (no_auth, valid_token, session_cookie), so status alone cannot fully discriminate.

### H3: Null Control
Server-side jitter (50-150ms random processing delay) does not cause false fingerprint variation. FP rate < 5%.

### H4: Drift Discriminability
Consecutive drift pairs (valid_token→expired_token, expired_token→invalid_token) are all discriminable (Jaccard < 0.5).

## 5. Server Design

### 5.1 Flask Auth Server

A Flask app serving a single endpoint `GET /api/data` where the response depends on the Authorization header or Cookie:

| Auth State | Auth Input | Status | Body Content |
|------------|-----------|--------|-------------|
| no_auth | (none) | 200 | Public page data |
| valid_token | Bearer tok_valid_abc123 | 200 | Private dashboard data (different from no_auth) |
| expired_token | Bearer tok_expired_xyz789 | 401 | Token expired error |
| invalid_token | Bearer tok_invalid_wrong | 403 | Invalid token error |
| session_cookie | session=sess_cookie_def456 | 200 | Session-bound user data (different from no_auth and valid_token) |

Key properties:
- URL is constant: `GET /api/data` for all states
- 3 distinct status codes: 200 (3 states), 401 (1 state), 403 (1 state)
- 5 distinct response bodies
- Server-side processing delay: `time.sleep(random.uniform(0.05, 0.15))` per request

### 5.2 Why This Server Design

- **Constant URL**: Eliminates URL-tautological discrimination (parent V1-EXTERNAL-TAUTOLOGY)
- **Real auth logic**: Flask middleware, not hand-programmed fixed responses
- **Body variation**: All 5 states return different bodies, testing whether full vector captures body variation
- **Status overlap**: 3 states share status 200, forcing B-STATUS-ONLY to fail on those pairs
- **Server-side jitter**: Tests timing confound that parent audit (V5-JITTER-WEAK) identified as untested

## 6. Fingerprint Method

Deterministic SHA-256 of sorted-tuple vector:

```python
vector = (
    status,
    tuple(sorted(headers_filtered.items())),  # exclude Date, Server
    body_sha256,
    redirect_chain,
)
fingerprint = sha256(repr(vector))
```

Inherited from parent with no changes. The `repr(vector)` call is Python-version-dependent (parent V6-REPR-VERSION-DEPENDENCE) — this is a known limitation, not a blocker.

## 7. Measures

### 7.1 Primary Metric
- **discrimination_score** = intra_match_rate - inter_match_rate
  - intra_match_rate: fraction of same-state fingerprint pairs that are identical
  - inter_match_rate: fraction of different-state fingerprint pairs that are identical
  - Range: [-1, 1]. Perfect discrimination = 1. No discrimination = 0.
  - Survival threshold: > 0.5

### 7.2 Baselines
- **B-STATUS-ONLY**: SHA-256 of status code string only. Expected to fail: 3 states share status 200.
- **B-BODY-ONLY**: SHA-256 of response body bytes only. Expected to succeed: all 5 bodies differ.
- **B-URL-HASH**: SHA-256 of URL string. Expected 0.0 (URL is constant).
- **B-RANDOM**: Random 256-bit fingerprints. Expected ~0.0.

### 7.3 Drift Metrics
- Jaccard similarity between consecutive drift pairs: valid_token→expired_token, expired_token→invalid_token
- All pairs must have Jaccard < 0.5 (discriminable)

### 7.4 Bootstrap Confidence Interval
- 1000 bootstrap resamples of state pairs for discrimination score 95% CI

## 8. Null Models

### 8.1 Server-Jitter Null
Repeat requests to the same auth state with server-side jitter. If jitter causes fingerprint variation, FP rate > 5%. This tests whether the fingerprint is invariant to timing when timing is excluded from the vector.

### 8.2 URL-Constant Null
B-URL-HASH should achieve discrimination = 0.0 because URL is constant. If it achieves > 0, the server design is broken.

## 9. Controls

### 9.1 Positive Control
Full-vector discrimination > 0.5. Verifies: (a) server produces distinct responses per auth state, (b) fingerprint captures the variation, (c) jitter does not destroy discrimination.

### 9.2 Null Control (Server-Jitter)
FP rate < 5% when repeating identical auth-state requests with 50-150ms server-side jitter. Verifies: (a) fingerprint excludes timing, (b) server-side variation does not cause false fingerprint variation.

### 9.3 Baseline Superiority
B-STATUS-ONLY discrimination < full-vector discrimination. Verifies: full vector adds value over status-only monitoring. Expected to hold because 3 states share status 200.

### 9.4 Drift Control
All consecutive drift pairs discriminable (Jaccard < 0.5). Verifies: auth-state transitions produce observable fingerprint changes.

## 10. Validity Threats

### 10.1 Flask vs Production
Flask is a development server, not production middleware. Findings may not transfer to production auth systems with caching, CDN, load balancers. Mitigation: this is a controlled validation; production testing is a separate experiment.

### 10.2 Python-Version Dependence
`repr(vector)` is Python-version-dependent (parent V6). Fingerprints may not reproduce across Python versions. Mitigation: within-experiment discrimination is unaffected; cross-version portability is a known limitation.

### 10.3 Sample Size
50 requests (5 states x 10 reps) provides adequate power for discrimination > 0.5 detection. With 10 reps per state, intra-state pairs = 45, inter-state pairs = 1000+. Discrimination estimates are stable.

### 10.4 Server-Side Jitter Range
50-150ms jitter is moderate. Production servers may have higher variance (100ms-2s). Mitigation: this tests the mechanism's invariance to timing, not production-level jitter. Higher jitter can be tested later.

### 10.5 Auth State Design
5 auth states with 3 distinct status codes is a controlled design. Real auth middleware may have more states (rate-limited, permission-denied, etc.). Mitigation: the experiment tests whether the substrate can discriminate auth-varying responses, not exhaustiveness of auth states.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Full-vector discrimination > 0.5
2. Null control FP rate < 5%
3. B-STATUS-ONLY discrimination < full-vector discrimination
4. All drift pairs discriminable (Jaccard < 0.5)
5. No pipeline errors

### 11.2 FALSIFIED
If ANY of:
1. Full-vector discrimination <= 0.5
2. B-STATUS-ONLY discrimination >= full-vector discrimination
3. Null control FP rate >= 5%
4. Any drift pair not discriminable (Jaccard >= 0.5)

### 11.3 MEASUREMENT_INVALID
If:
1. Server fails to start
2. >20% request errors
3. Pipeline errors prevent computation

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Substrate works on constant-URL auth-varying server
- Full vector adds value over status-only (B-STATUS-ONLY fails because 3 states share status 200)
- B-BODY-ONLY may equal full vector (bodies fully discriminate)
- C-MEAS-VALID advances to broader testing
- Product can build auth drift detection on this substrate

### 12.2 Negative Result (FALSIFIED)
- If full vector <= 0.5: substrate fails on non-tautological servers (not just toy servers)
- If B-STATUS-ONLY >= full vector: status alone suffices for auth drift (full vector unnecessary)
- If null FP > 5%: server-side timing confounds fingerprint
- C-MEAS-VALID does not survive for general HTTP-level auth observation

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Server infrastructure issue, not scientific evidence

## 13. Analysis Plan

1. **Server Setup**: Start Flask app on localhost with auth middleware and 50-150ms jitter
2. **Request Execution**: 50 requests (5 states x 10 reps), randomized order (seed=44), 0-200ms client jitter
3. **Fingerprinting**: Compute deterministic sorted-tuple fingerprint per request
4. **Metrics**: Compute discrimination score, bootstrap CI, per-baseline discrimination
5. **Controls**: Verify positive, null, baseline superiority, drift controls
6. **Raw Evidence**: Persist raw_observations.json with status, headers, body_hash, fingerprint, elapsed, timestamp
7. **Reporting**: Report all outcomes with equal prominence

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
