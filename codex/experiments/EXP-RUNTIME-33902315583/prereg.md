# EXP-RUNTIME-33902315583 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-33902315583
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-04
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

On a real Flask server with PyJWT validation middleware (not hand-programmed lookup tables), no synthetic X-Auth-Level/X-Session/X-User/X-Error headers, and identical error response bodies for expired vs invalid tokens, does the HTTP fingerprint substrate maintain discrimination > 0.5 — and does the full vector (status+body+standard-headers) exceed B-BODY-ONLY when synthetic header tautology is removed and error states share identical bodies?

## 3. Motivation

Prior Runtime experiments established:
- EXP-RUNTIME-33528830833: stdlib HTTP substrate works on toy server (discrimination 1.0, null FP 0%)
- EXP-RUNTIME-33767375933: fixed substrate with deterministic serialization, tested on toy server + httpbin.org
- EXP-RUNTIME-33805283356: Flask server with 5 auth states, discrimination 1.0, but two high-severity gaps identified by audit:
  - V1-REAL-MIDDLEWARE-GAP: server is stdlib http.server, not Flask with real JWT; discrimination is construction-guaranteed by distinct bodies/headers per state
  - V2-SYNTHETIC-HEADER-TAUTOLOGY: X-Auth-Level/X-Session/X-User/X-Error headers perfectly encode state and inflate discrimination

The parent handoff (EXP-RUNTIME-33805283356) established:
- Deterministic SHA-256 fingerprint achieves perfect discrimination 1.0 on synthetic server
- Full vector equals B-BODY-ONLY on synthetic server (bodies fully discriminate)
- URL constancy verified, server-side jitter invariance validated
- Three mandatory parent fixes preserved: sorted-tuple fingerprint, Date/Server exclusion, strong baselines

What remains unknown:
- Does the substrate maintain discrimination on real Flask/JWT middleware?
- When bodies are identical (expired vs invalid), does full vector exceed B-BODY-ONLY?
- Does removing synthetic X- headers preserve discrimination?

This experiment closes both gaps by testing on a real Flask/JWT server without synthetic headers, with expired and invalid tokens returning identical response bodies.

## 4. Hypotheses

### H1: Substrate Discrimination on Real Middleware
Full-vector discrimination > 0.5 on a real Flask/JWT server with 4 auth states.

### H2: Full Vector Exceeds Status-Only
Full-vector discrimination > B-STATUS-ONLY discrimination (body adds information when multiple states share status 401).

### H3: Full Vector Equals Body-Only
Full-vector discrimination = B-BODY-ONLY discrimination (standard headers add no discriminating information beyond what body provides, especially when expired and invalid share identical bodies).

### H4: Null Control
Repeated identical requests with server-side jitter produce FP rate < 5% (timing variation does not cause false fingerprint variation).

### H5: Drift Discriminability
valid_token vs expired_token drift pair is discriminable (Jaccard < 0.5) — status differs (200 vs 401) AND body differs.

### H6: Expired-Invalid Indistinguishability
expired_token vs invalid_token drift pair is NOT discriminable (Jaccard ≈ 1.0) — identical status, body, and standard headers. This is correct substrate behavior, not a failure.

## 5. Server Design

### 5.1 Flask App with JWT Validation

```python
from flask import Flask, request, jsonify
import jwt
import time
from datetime import datetime, timedelta

app = Flask(__name__)
SECRET_KEY = "test-secret-key-12345"

@app.route('/api/data', methods=['GET'])
def get_data():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        # no_auth state: 401
        return jsonify({"error": "authentication_required"}), 401
    
    token = auth_header[7:]  # Remove "Bearer "
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        # valid_token state: 200
        return jsonify({"data": "secret_message", "user": payload.get("sub", "unknown")}), 200
    except jwt.ExpiredSignatureError:
        # expired_token state: 401, IDENTICAL body to invalid
        return jsonify({"error": "authentication_failed"}), 401
    except jwt.InvalidTokenError:
        # invalid_token state: 401, IDENTICAL body to expired
        return jsonify({"error": "authentication_failed"}), 401
```

### 5.2 Auth States

| State | Authorization Header | Status | Body |
|-------|---------------------|--------|------|
| no_auth | (none) | 401 | {"error": "authentication_required"} |
| valid_token | Bearer <valid JWT> | 200 | {"data": "secret_message", "user": "alice"} |
| expired_token | Bearer <expired JWT> | 401 | {"error": "authentication_failed"} |
| invalid_token | Bearer <malformed string> | 401 | {"error": "authentication_failed"} |

**Critical design feature**: expired_token and invalid_token return IDENTICAL response bodies (same status 401, same JSON body). This tests whether the substrate can still discriminate valid from expired/invalid (which differ in status and body) while correctly reporting expired and invalid as indistinguishable.

### 5.3 Token Generation

- valid_token: JWT with sub="alice", exp=(now + 1 hour), signed with HS256
- expired_token: JWT with sub="alice", exp=(1 hour ago), signed with HS256
- invalid_token: "not-a-real-jwt-token" (malformed, fails PyJWT validation)

### 5.4 No Synthetic Headers

Server returns ONLY standard HTTP headers:
- Content-Type: application/json
- Content-Length: (computed)
- Server: Werkzeug/... (Flask default — excluded from fingerprint)
- Date: (computed — excluded from fingerprint)

NO X-Auth-Level, X-Session, X-User, X-Error headers.

## 6. Fingerprint Function

Inherited from parent fixes (EXP-RUNTIME-33805283356):
```
fingerprint = SHA-256(
    status,
    tuple(sorted([
        (k, v) for k, v in headers.items()
        if k.lower() not in ('date', 'server')
    ])),
    SHA-256(body_bytes),
    redirect_chain
)
```

- Deterministic: same input always produces same output
- Excludes Date and Server headers to prevent spurious variance
- Uses body_sha256 (not raw body) to avoid JSON serialization non-determinism
- Sorted tuple eliminates Python hash randomness

## 7. Baselines

### 7.1 B-STATUS-ONLY
SHA-256 of status code string only. Expected to fail to distinguish no_auth (401) from expired/invalid (401). Discrimination < full vector.

### 7.2 B-BODY-ONLY
SHA-256 of response body bytes only. Expected to equal full vector because expired and invalid share identical bodies and standard headers add no discriminating information.

### 7.3 B-URL-HASH
SHA-256 of URL string only. Straw-man, expected 0.0 (URL is constant).

### 7.4 B-RANDOM
Random 256-bit fingerprints. Straw-man, expected ~0.0.

## 8. Controls

### 8.1 Positive Control
valid_token (200, unique body) is distinguishable from all other states. Full-vector discrimination must be > 0.5. This verifies the substrate can detect the difference between 'authenticated successfully' and 'authentication failed' on real Flask/JWT middleware.

### 8.2 Null Control
10 repeated identical requests to the same auth state with server-side jitter (50-150ms). FP rate must be < 5%. Validates timing invariance.

### 8.3 Drift Discriminability
- valid_token vs expired_token: different status (200 vs 401) AND different body → EXPECTED discriminable (Jaccard < 0.5)
- expired_token vs invalid_token: SAME status (401) AND SAME body AND SAME standard headers → EXPECTED non-discriminable (Jaccard ≈ 1.0)

## 9. Sample Size

- 4 states x 10 reps = 40 requests
- Randomized order with seed 44 (inherited from parent)
- Server-side jitter: random.uniform(0.05, 0.15) seconds per request

## 10. Metrics

Stable metric identities (compatible with prior runtime experiments):
- `full_vector_discrimination`: discrimination score for full fingerprint vector
- `full_vector_intra_match_rate`: fraction of within-state pairs that match
- `full_vector_inter_match_rate`: fraction of between-state pairs that match
- `full_vector_mean_intra_jaccard`: mean Jaccard similarity within states
- `full_vector_mean_inter_jaccard`: mean Jaccard similarity between states
- `full_vector_bootstrap_95ci`: bootstrap 95% confidence interval
- `baselines.B-STATUS-ONLY`: discrimination for status-only baseline
- `baselines.B-BODY-ONLY`: discrimination for body-only baseline
- `baselines.B-URL-HASH`: discrimination for URL-only baseline
- `baselines.B-RANDOM`: discrimination for random baseline
- `null_fp_rate`: false positive rate under jitter
- `drift_jaccards`: Jaccard similarities for drift pairs
- `drift_all_discriminable`: whether all expected-discriminable drift pairs are discriminable
- `total_requests`: total requests made
- `error_rate`: fraction of requests that errored

## 11. Decision Rules

### 11.1 C-MEAS-VALID SURVIVES
If ALL of:
1. Full-vector discrimination > 0.5
2. Null control FP rate < 5%
3. valid_token vs expired_token drift pair discriminable (Jaccard < 0.5)

### 11.2 C-MEAS-VALID FALSIFIED
If ANY of:
1. Full-vector discrimination <= 0.5
2. Null FP rate > 5%
3. valid_token vs expired_token drift pair not discriminable (Jaccard >= 0.5)

### 11.3 MEASUREMENT_INVALID
If:
1. Flask server fails to start
2. >20% request errors
3. Server returns unexpected responses (e.g., 500 errors)

### 11.4 Note on Expired-Invalid Pair
expired_token vs invalid_token drift pair is EXPECTED to be non-discriminable (identical status, body, headers). This is correct substrate behavior, not a failure. The substrate correctly reports that these two states are indistinguishable via HTTP observation.

## 12. Validity Threats

### 12.1 Flask vs Production Middleware
Flask with PyJWT is real JWT validation, but production OAuth/OIDC providers may have additional response variation (e.g., different error formats, additional headers, cache-Control). Findings apply to Flask/JWT specifically; broader generalization requires additional experiments.

### 12.2 JSON Serialization Non-determinism
Python dict ordering is insertion-ordered (3.7+), but jsonify may produce slightly different formatting. Mitigation: compare body_sha256, not raw body bytes. If JSON serialization varies, bodies that are semantically identical may have different hashes.

### 12.3 Standard Header Variation
Flask/Werkzeug may add headers not present in the test design (e.g., X-Request-Id, ETag). If these headers vary across requests to the same state, they would inflate inter_match_rate. Mitigation: exclude known variable headers from fingerprint, or accept that standard header variation is part of the real-world signal.

### 12.4 Sample Size
40 requests (4 states x 10 reps) provides limited statistical power for detecting subtle discrimination differences. This is consistent with prior runtime experiments and sufficient for the primary discrimination test (>0.5 threshold).

### 12.5 Seed Dependence
Randomized request order uses seed 44 (inherited from parent). Findings may depend on this specific order. Mitigation: primary metrics are order-independent (discrimination is computed over all pairs).

## 13. Expected Outcomes

### 13.1 Positive Result (C-MEAS-VALID SURVIVES)
- Substrate works on real Flask/JWT middleware without synthetic headers
- Full vector > B-STATUS-ONLY (body adds information)
- Full vector = B-BODY-ONLY (standard headers don't add information)
- Product can build auth drift detection focusing on body changes
- C-MEAS-VALID advances to broader testing (e.g., OAuth/OIDC providers)

### 13.2 Negative Result (C-MEAS-VALID FALSIFIED)
- Substrate fails on real Flask/JWT middleware
- Possible causes: JSON non-determinism, header variation, timing sensitivity
- C-MEAS-VALID does not survive beyond synthetic servers
- Product must use alternative observation mechanisms

### 13.3 Mixed Result
- Substrate discriminates but full vector = B-BODY-ONLY (body is the dominant signal)
- This constrains product architecture: body-based observation is sufficient
- Multi-field observation adds value only when headers vary with auth state

## 14. Analysis Plan

1. Start Flask server on localhost
2. Generate tokens: valid (exp=now+1h), expired (exp=now-1h), invalid (malformed string)
3. Send 40 requests in randomized order (seed=44) with 50-150ms server-side jitter
4. Collect raw observations: status, headers, body_hash, fingerprint, elapsed
5. Compute discrimination metrics and baselines
6. Compute null FP rate from within-state pairs
7. Compute drift Jaccards for valid->expired and expired->invalid pairs
8. Persist raw_observations.json and result.json
9. Report all outcomes with equal prominence

## 15. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 16. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
