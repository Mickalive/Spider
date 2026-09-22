# EXP-RUNTIME-35697043449 — Report

**Experiment ID:** EXP-RUNTIME-35697043449
**Lane:** Runtime
**Claim:** C-MEAS-VALID (Measurement substrate is intervention-valid)
**Status:** COMPLETE
**Outcome:** SUPPORTS

---

## Executive Summary

The HTTP fingerprint substrate (status + body + standard headers) successfully discriminates server-side state changes produced by writable controls on a Flask+SQLite+JWT localhost testbed. All five frozen decision-rule conditions pass:

| Condition | Value | Threshold | Pass |
|-----------|-------|-----------|------|
| C1 PERMISSION_DISC | 1.000 | > 0.5 | ✅ |
| C2 SESSION_DISC | 1.000 | > 0.5 | ✅ |
| C3 NULL_BODY | 0.000 | = 0.0, CI contains 0.0 | ✅ |
| C4 FULL_EXCEEDS_STATUS | 1.0 ≥ 1.0 | ≥ max(B-STATUS-ONLY, B-BODY-ONLY) | ✅ |
| C5 NULL_CONTROL_PASS | 0.000 | ≤ 0.05 | ✅ |

**Verdict:** The substrate discriminates permission escalation (403→200+body) and session invalidation (200→401) with perfect discrimination, while producing a valid null on auth-state drift (fresh vs near-expiry token, identical responses).

---

## 1. Raw Observations

### 1.1 Auth States Tested

| State | Endpoint | Token | Session | Expected | Observed |
|-------|----------|-------|---------|----------|----------|
| no_auth | /protected | none | — | 401 | 401 ✅ |
| valid_reader | /protected | valid JWT | active | 200 | 200 ✅ |
| valid_reader | /admin | valid JWT | active | 403 | 403 ✅ |
| valid_admin | /admin | valid JWT | active | 200 | 200 ✅ |
| session_killed | /protected | valid JWT | invalidated | 401 | 401 ✅ |
| null_fresh | /protected | valid JWT (3600s) | active | 200 | 200 ✅ |
| null_near_expiry | /protected | valid JWT (30s) | active | 200 | 200 ✅ |

### 1.2 Observation Counts

- N=20 per state × 7 states = 140 total observations
- Unique fingerprints per state: 1 (all responses within a state are byte-identical)
- Total raw observations persisted: `raw_observations.jsonl`

### 1.3 Writable Controls Verified

1. **Permission escalation:** SQLite `UPDATE users SET role='admin' WHERE username='reader'` committed → subsequent GET /admin returned 200+admin dashboard body (previously 403+forbidden)
2. **Session invalidation:** SQLite `DELETE FROM sessions WHERE token_hash=?` committed → subsequent GET /protected returned 401+session_invalid (previously 200+user data)
3. **Auth-state drift:** Fresh token (exp=3600s) and near-expiry token (exp=30s) both valid JWTs with identical claims → server returned identical 200+body for both

---

## 2. Discrimination Metrics

### 2.1 Primary Measurements

| Condition | Full-vector Jaccard | 95% CI | Interpretation |
|-----------|---------------------|--------|----------------|
| Permission escalation | 1.000 | [1.0, 1.0] | Perfect discrimination: 403→200+body |
| Session invalidation | 1.000 | [1.0, 1.0] | Perfect discrimination: 200→401 |
| Null control | 0.000 | [0.0, 0.0] | No false positive: identical responses |

### 2.2 Baselines

| Baseline | Permission | Session | Notes |
|----------|-----------|---------|-------|
| B-STATUS-ONLY | 1.0 | 1.0 | Status code alone discriminates both conditions |
| B-BODY-ONLY | 1.0 | 1.0 | Body alone discriminates both conditions |
| B-HEADERS-ONLY | 1.0 | 1.0 | Headers alone discriminate both conditions |

**C4 Analysis:** Full-vector discrimination (1.0) equals max(B-STATUS-ONLY, B-BODY-ONLY) = 1.0 on both conditions. The full vector does not exceed single-field baselines because all baselines achieve ceiling discrimination. This is expected when response bodies and status codes change simultaneously: both status and body independently achieve perfect discrimination, so adding headers cannot improve beyond 1.0.

### 2.3 Bootstrap Confidence Intervals

- Bootstrap N=1000 resamples per comparison
- CI degenerate at [1.0, 1.0] and [0.0, 0.0] because all fingerprints within each state are identical (zero within-state variance)
- This is a consequence of deterministic Flask responses with static JSON bodies: no timing-dependent or header-dependent variation

---

## 3. Interpretation

### 3.1 What the Evidence Shows

The experiment demonstrates that the HTTP fingerprint substrate can attribute response differences to server-side state changes when those changes produce observable HTTP differences:

1. **Permission escalation is detectable:** A SQLite role update (reader→admin) changes the server's authorization check, producing a different HTTP response (403→200+body). The substrate discriminates this with Jaccard=1.0.

2. **Session invalidation is detectable:** A SQLite session deletion changes the server's session validation, producing a different HTTP response (200→401). The substrate discriminates this with Jaccard=1.0.

3. **Auth-state drift produces no false positive:** Two valid JWTs with identical claims (same user, same role) but different expiry times produce identical server responses. The substrate correctly reports Jaccard=0.0.

### 3.2 What This Unblocks

A positive result on C-MEAS-VALID unblocks:
- **C-FRESHNESS:** Session/auth drift detection infrastructure is now available for distributed testing
- **C-DELTA-REPAIR:** Perturbation measurement infrastructure is available for measuring how server-side state changes propagate to observable HTTP differences

### 3.3 Claim Ceiling

The result is bounded to:
- Flask 3.1.3 + PyJWT 2.14.0 HS256 on localhost 127.0.0.1:19847
- 5 auth states with distinct response bodies and status codes
- Headers filtered (Date, Server, X-Request-Id excluded)
- Jitter 50-150ms uniform, N=20, SEED=44
- Server reads role from SQLite (not from JWT payload) on each request
- Responses are deterministic within state (1 unique fingerprint per state)
- No production middleware, no CDN, no network variation

**Not tested:**
- Discrimination when response bodies are identical but server-side state changes only headers
- Discrimination on production middleware with realistic response variation (ETag, Cache-Control, Set-Cookie)
- Discrimination under concurrent load, HTTP/2, TLS, or multi-client scenarios
- Discrimination when partial body changes produce overlapping fingerprint sets

### 3.4 Baseline Equivalence

All baselines (STATUS-ONLY, BODY-ONLY, HEADERS-ONLY) achieve ceiling discrimination (1.0) on both positive conditions. This is because the test design produces maximally distinct responses: different status codes AND different bodies AND different headers. The baselines cannot be discriminated from each other under this design. A future experiment with body-only changes (same status, different body) or header-only changes (same status+body, different headers) would better isolate the marginal contribution of each fingerprint component.

---

## 4. Validity Assessment

| Threat | Mitigation | Residual Risk |
|--------|-----------|---------------|
| Server state leakage | Fresh DB per run, verified initial state | Low |
| JWT clock skew | Same clock for token generation and server | None (localhost) |
| SQLite WAL visibility | Explicit COMMIT + 100ms delay before observation | Low |
| Header non-determinism | Excluded Date/Server/X-Request-Id | Low |
| Session timing race | Sequential request-response, verified session state | Low |
| Near-expiry token expiry | 30s window, N=20 completed in ~6s | Low |
| Response non-determinism | Deterministic Flask responses, 1 unique fingerprint per state | None (ceiling effect) |

---

## 5. Consequences

**If SUPPORTS (observed):**
- C-MEAS-VALID advances toward VALIDATED
- Writable/auth/session/drift controls demonstrated on localhost
- C-FRESHNESS and C-DELTA-REPAIR unblocked for distributed testing
- Runtime lane can provide measurement substrates for other lanes' experiments

**If FALSIFIED (not observed):**
- C-MEAS-VALID remains EXPERIMENTAL with narrowed ceiling
- Alternative substrates (DOM-level, network-level) may be required
- The HTTP fingerprint substrate cannot discriminate server-side state changes when response bodies/status codes do not change

**Actual outcome:** SUPPORTS — all conditions pass with ceiling discrimination values.
