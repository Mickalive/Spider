# EXP-RUNTIME-35697043449 — Preregistration

**Experiment ID:** EXP-RUNTIME-35697043449  
**Lane:** Runtime  
**Claim:** C-MEAS-VALID (Measurement substrate is intervention-valid)  
**Director Mandate:** PIVOT — cognitive reset, build writable/auth/session/drift controls  
**Date:** 2026-09-22  

---

## 1. Question

Can a Flask+SQLite+JWT localhost testbed implement writable permission-level changes, server-side session invalidation, and auth-state drift such that the HTTP fingerprint substrate produces discriminating positive outcomes for permission escalation and session invalidation, and a valid null outcome for identical-body auth-state drift?

## 2. Hypothesis

The HTTP fingerprint substrate (status + body + standard headers) will discriminate:
- **Permission escalation** (role upgrade changes response from 403 to 200+body) with discrimination > 0.5
- **Session invalidation** (server-side session kill changes response from 200 to 401) with discrimination > 0.5
- **Auth-state drift** (fresh vs near-expiry token, identical responses) with discrimination = 0.0

This demonstrates the substrate attributes response differences to server-side state changes, not confounds.

## 3. Server Design

### 3.1 Testbed Architecture

```
Flask 3.1.3 + PyJWT 2.13.0 (HS256) + SQLite WAL-mode
  ├── /auth/token     — POST, returns JWT for valid credentials
  ├── /protected      — GET, requires valid JWT, returns user data
  ├── /admin          — GET, requires valid JWT + role='admin'
  └── /session/status — GET, requires valid session in SQLite
```

### 3.2 Auth States (4 states)

| State | Token | Role | Session | Expected Response |
|-------|-------|------|---------|-------------------|
| `no_auth` | none | — | — | 401 + `{"error": "authentication_required"}` |
| `valid_reader` | valid JWT, exp=3600s | reader | active | 200 + `{"role": "reader", "access": "limited"}` on /protected; 403 + `{"error": "forbidden"}` on /admin |
| `valid_admin` | valid JWT, exp=3600s | admin | active | 200 + `{"role": "admin", "access": "full", "dashboard": "..."}` on /admin |
| `session_killed` | valid JWT, exp=3600s | reader | **invalidated** | 401 + `{"error": "session_invalid"}` |

### 3.3 Writable Controls

Permission escalation is implemented as a **server-side SQLite write**:
```sql
UPDATE users SET role = 'admin' WHERE username = 'reader';
```
This is committed before the next observation, making the role change observable via HTTP.

Session invalidation is implemented as a **server-side SQLite delete**:
```sql
DELETE FROM sessions WHERE token_hash = ?;
```
This kills the session without invalidating the JWT itself, testing whether the substrate detects server-side session state.

### 3.4 Auth-State Drift (Null Control)

Two tokens with identical claims but different expiry:
- **Fresh token:** `iat=now, exp=now+3600` (3600s remaining)
- **Near-expiry token:** `iat=now-3590, exp=now+10` (10s remaining)

Both are valid JWTs. Server returns **identical** response body, status, and standard headers for both. Discrimination must be 0.0.

## 4. Measurement

### 4.1 Observation Vector

For each request, observe:
- HTTP status code
- Response body (exact bytes)
- Standard headers (excluding Date, Server, X-Request-Id)
- Response time

Fingerprint = hash(status + body + sorted_filtered_headers)

### 4.2 Discrimination Metric

Full-vector Jaccard distance between fingerprint sets from two states:
```
discrimination = 1.0 - Jaccard(fingerprints_A, fingerprints_B)
```

Where fingerprints_A and fingerprints_B are sets of N fingerprints from state A and state B respectively.

### 4.3 Baselines

| Baseline | Fingerprint Source | Purpose |
|----------|-------------------|---------|
| B-STATUS-ONLY | status code only | Tests whether status alone suffices |
| B-BODY-ONLY | response body only | Tests whether body alone suffices |
| B-HEADERS-ONLY | standard headers only | Tests header-only discrimination |

### 4.4 Sample Size

- N=20 per state (4 states × 20 = 80 primary observations)
- N=20 null-control pairs (fresh token vs near-expiry token, same endpoint)
- Total: ~100 observations
- Jitter: 50-150ms uniform between observations

## 5. Decision Rule

ALL of the following must hold for **SUPPORTS**:

1. **C1 PERMISSION_DISC:** full-vector discrimination > 0.5 on permission escalation (valid_reader vs valid_admin on /admin endpoint)
2. **C2 SESSION_DISC:** full-vector discrimination > 0.5 on session invalidation (valid_reader vs session_killed on /protected endpoint)
3. **C3 NULL_BODY:** full-vector discrimination = 0.0 on null control (fresh token vs near-expiry token, same endpoint), bootstrap 95% CI contains 0.0
4. **C4 FULL_EXCEEDS_STATUS:** full-vector discrimination ≥ max(B-STATUS-ONLY, B-BODY-ONLY) on at least one of permission or session conditions
5. **C5 NULL_CONTROL_PASS:** null control discrimination ≤ 0.05

If any condition fails → **FALSIFIED-IN-SETTING** with specific failing condition documented.

If infrastructure prevents valid measurement → **MEASUREMENT_INVALID**.

## 6. Controls

### 6.1 Positive Controls

- **Permission escalation:** SQLite UPDATE committed → subsequent GET /admin changes from 403 to 200+body
- **Session invalidation:** SQLite DELETE committed → subsequent GET /protected changes from 200 to 401

### 6.2 Null Controls

- **Auth-state drift:** fresh vs near-expiry token → identical responses

### 6.3 Regression Controls

- B-STATUS-ONLY must match expected pattern (0.0 for permission if both return same status; 1.0 for session if status changes)
- B-BODY-ONLY must match expected pattern (1.0 for permission if body changes; 1.0 for session if body changes)

## 7. Validity Threats

1. **Server state leakage:** Previous observations may leave residual state → mitigated by fresh server start per run
2. **JWT clock skew:** Token expiry checked against server time → mitigated by using same clock
3. **SQLite WAL visibility:** Writes may not be immediately visible → mitigated by explicit COMMIT + small delay
4. **Header non-determinism:** Some headers may vary → mitigated by excluding Date/Server/X-Request-Id
5. **Session store timing:** Session invalidation may have race conditions → mitigated by sequential request-response

## 8. Consequences

**Positive outcome:** C-MEAS-VALID advances toward VALIDATED. Writable/auth/session/drift controls demonstrated. C-FRESHNESS and C-DELTA-REPAIR unblocked for distributed testing.

**Negative outcome:** C-MEAS-VALID remains EXPERIMENTAL with narrowed ceiling. The HTTP fingerprint substrate cannot discriminate server-side state changes when responses are identical. Alternative substrates required.
