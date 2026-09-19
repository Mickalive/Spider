# EXP-GRAPH-35456070379 preregistration

**Experiment ID:** EXP-GRAPH-35456070379  
**Lane:** graph  
**Claim:** C-FRESHNESS  
**Status:** DESIGN — not yet frozen  

---

## 1. Question

Does behavioral-structural signal orthogonality (|r| < 0.15) hold on a production-like local testbed server when structural signal is defined from headers-only (excluding error response bodies), and does the B-FLASK-ONLY baseline show similar orthogonality?

## 2. Motivation and inherited state

### 2.1 Established (from parent experiments)

- C-FRESHNESS orthogonality at delta=0.15 confirmed under localhost Flask mock across three experiments:
  - Deterministic Flask r=0.0335 (EXP-GRAPH-35330739886)
  - Stochastic Flask+SQLite+cache+jitter r=0.0463 (EXP-GRAPH-35353011131)
  - HTTP conditional caching r=0.0022 (EXP-GRAPH-35389145821)
  - All n=480, all PASS, all audit-verified
- Claim ceiling: localhost Flask mock with controlled stochasticity
- Behavioral signals (token validation, session state change, auth boundary shift, session_status_check) validated detection dimension: TP=1.0 across all co-occurring conditions
- HTTP conditional caching (304 Not Modified) does NOT break orthogonality
- Delta=0.10 orthogonality passes on pooled data (CI upper 0.0916 < 0.10) but per-mode/per-condition CIs exceed 0.10
- Production-like testbed infrastructure is functional and reusable (EXP-GRAPH-35445595108)

### 2.2 Rejected

- Stable public APIs (GitHub 403, JSONPlaceholder deterministic) as testbeds — zero behavioral and structural variance (EXP-GRAPH-35409927045, MEASUREMENT_INVALID)
- Per-caching-mode heterogeneity as systematic — symmetric at +/- 0.061 at n=480 (confirmed sampling noise)
- n=240 sufficient for delta=0.15 equivalence — CI width ~0.25 at n=240 vs ~0.18 at n=480; n>=480 required
- Structural signal definition hash(body)%10000 including error bodies produces valid orthogonality measurement — V1 confound: error body constant for expired tokens creates forced correlation (r=0.375)

### 2.3 Unknown

- Whether orthogonality holds on production-like infrastructure with corrected structural signal extraction (headers-only or success-only)
- Whether CDN/OAuth/dynamic content features introduce genuine correlation (B-FLASK-ONLY baseline not executed)
- Whether expired responses should carry structural headers in production APIs
- What structural signal formulation satisfies independent extraction while retaining product relevance
- Whether the result generalizes to non-Flask frameworks

### 2.4 Do NOT assume

- C-FRESHNESS reaches VALIDATED or PRODUCT_CORE — status remains EXPERIMENTAL bounded to localhost mock
- r=0.375 falsifies orthogonality on production-like infrastructure — measurement-invalid due to shared-variable confound
- pooled r=0.0022 is true population correlation under production conditions — point estimate from localhost mock
- Delta=0.10 confirmed for product deployment — only pooled CI passes
- Production-like infrastructure features introduce correlation — untested due to measurement confound
- r=0.375 represents genuine behavioral-structural coupling — definitional artifact of error-body hashing
- Testbed CDN simulation represents production CDN behavior — single-node Flask in-memory cache

## 3. Hypothesis

C-FRESHNESS orthogonality at delta=0.15 will hold with corrected structural signal extraction (headers-only) because the previous confound (EXP-GRAPH-35445595108) was due to including error response bodies which are constant across token expiration. Removing error bodies eliminates the forced correlation (r=0.375). The production-like infrastructure features (CDN, OAuth, dynamic content) should not introduce correlation when structural signal is extracted from headers-only, as these features affect orthogonal domains. The B-FLASK-ONLY baseline should also show orthogonality, confirming that infrastructure complexity does not break orthogonality.

## 4. Testbed server design

### 4.1 Architecture

Same production-like local testbed server as EXP-GRAPH-35445595108, with corrected signal extraction:
- **CDN simulation:** varnish or nginx reverse proxy with:
  - ETag-SHA256 headers
  - Cache-Control max-age/no-store per endpoint
  - Stale-while-revalidate support
  - Cache invalidation on session state change
  - 304 Not Modified responses for conditional requests
- **OAuth2 middleware:** PyJWT RS256 with:
  - Access tokens (15-min expiry)
  - Refresh tokens (24-hour expiry)
  - Session invalidation on logout/password change
  - Permission boundary (read/write/admin)
  - Token validation failure detection
- **Dynamic content:** Database-backed responses with:
  - Timestamps (server-generated, per-request)
  - Request IDs (UUID v4, per-request)
  - User-dependent responses (role-based content)
  - Database-backed state (SQLite WAL-mode)
- **Configurable network latency:** Jitter injection (10-500ms uniform) on backend calls

### 4.2 B-FLASK-ONLY baseline

Plain Flask server without CDN simulation, OAuth middleware, or dynamic content:
- Static responses with timestamps and request IDs (dynamic content)
- No caching headers
- No token validation (optional simple auth for behavioral variation)
- Same corrected headers-only structural signal extraction

### 4.3 Endpoints (minimum 3)

| Endpoint | Behavioral Variation | Structural Variation |
|----------|---------------------|---------------------|
| `/api/user/profile` | Token validation failure, session state change, permission boundary | ETag varies with profile updates, Cache-Control no-store for admin |
| `/api/data/list` | Rate limiting triggers (token expired vs valid), auth boundary shift | Cache-Control max-age varies, dynamic timestamps, request IDs |
| `/api/session/status` | Session invalidation detection, token refresh required | Cache-Control no-store, ETag varies with session state |

### 4.4 Signal extraction (CORRECTED)

**Behavioral signals (per request):**
- `token_validation_failure`: 1 if token expired/invalid, 0 otherwise
- `session_state_change`: 1 if session ID changed, 0 otherwise
- `auth_boundary_shift`: 1 if permission level changed, 0 otherwise
- `session_status_check`: 1 if session invalidation detected, 0 otherwise

**Structural signals (per response) — HEADERS-ONLY:**
- `etag_variation`: 1 if ETag header changed, 0 otherwise
- `cache_control_variation`: 1 if Cache-Control header changed, 0 otherwise
- `dynamic_content_hash`: SHA-256 of timestamp+request_id+user_dependent fields (from headers or success body only)
- `request_id_entropy`: Shannon entropy of request_id field (if present in headers)

**Excluded from structural signal:**
- Error response bodies (HTTP 401, 403, 5xx)
- Response body hashes for error responses
- Any signal derived from error response content

### 4.5 Co-occurring conditions (minimum 8)

| Condition | Behavioral State | Cache Mode | Auth State |
|-----------|-----------------|------------|------------|
| 1 | Valid token | Cache-enabled | Read permission |
| 2 | Valid token | Cache-enabled | Write permission |
| 3 | Valid token | Cache-disabled | Read permission |
| 4 | Valid token | Cache-disabled | Write permission |
| 5 | Expired token | Cache-enabled | Read permission |
| 6 | Expired token | Cache-enabled | Write permission |
| 7 | Expired token | Cache-disabled | Read permission |
| 8 | Expired token | Cache-disabled | Write permission |

## 5. Sampling plan

- **Unit of analysis:** Paired (behavioral_delta, structural_composite) per request
- **Sample size:** n >= 480 paired samples (60 per co-occurring condition x 8 conditions)
- **Endpoint allocation:** Minimum 3 endpoints x 160 requests each
- **Seed:** Deterministic seed for all random operations (token generation, latency jitter, request ordering)
- **Exclusions:** Exclude requests with HTTP errors (5xx), timeout (>5s), or incomplete responses

## 6. Metrics

### 6.1 Primary metric

- **Pooled Pearson r** between behavioral_delta and structural_composite across all paired samples
- **95% CI** (Fisher z-transformed) of pooled r
- **TOST equivalence test** at delta=0.15: H0: |r| >= 0.15 vs H1: |r| < 0.15

### 6.2 Secondary metrics

- **Per-endpoint Pearson r** (structural heterogeneity check)
- **Per-cache-mode Pearson r** (CDN impact check)
- **Behavioral detection TP** (token validation failure detection rate)
- **Structural signal std** (per-endpoint, per-cache-mode)
- **Cache hit rate** (CDN simulation effectiveness)
- **Network latency distribution** (jitter injection verification)
- **B-FLASK-ONLY pooled Pearson r** (baseline comparison)
- **B-ERROR-BODY-INCLUDED pooled Pearson r** (negative control)

## 7. Decision rule

### 7.1 C-FRESHNESS orthogonality CONFIRMED if ALL:

- **C1:** Behavioral detection TP >= 0.85 across all endpoints
- **C2:** At least 2/3 endpoints have behavioral signal std > 0 AND at least 2/3 endpoints have structural signal std > 0
- **C3:** 95% CI upper bound of pooled Pearson r < 0.15 on production-like testbed with headers-only signal
- **C4:** TOST equivalence test p_upper < 0.05 at delta=0.15
- **C5:** 304 manipulation check passes: cache-enabled and cache-disabled correlations show symmetric heterogeneity within sampling noise (|r_cache_enabled - r_cache_disabled| < 2 * SE at n=480)
- **C6:** B-FLASK-ONLY baseline shows |r| < 0.15 (orthogonality persists without infrastructure)

### 7.2 C-FRESHNESS orthogonality REJECTED if ANY:

- Any condition C1-C6 fails

### 7.3 MEASUREMENT_INVALID if:

- Testbed server construction fails (infrastructure failure)
- Fewer than 240 paired samples collected (data insufficiency)
- Fewer than 2/3 endpoints have behavioral OR structural signal std = 0 (signal extraction failure)

## 8. Validity threats

### 8.1 Internal validity

- **Confounding:** CDN cache behavior may correlate with OAuth token validation (e.g., cache invalidation triggered by token refresh). Mitigation: design endpoints so cache invalidation is independent of token state.
- **Ceiling effect:** If all responses are distinct, discrimination may be at 1.0 and headers cannot improve. Mitigation: include cache-enabled conditions where CDN caching reduces response distinctiveness.
- **Signal extraction failure:** Behavioral or structural signals may be degenerate (std=0). Mitigation: verify signal std > 0 before computing correlation; report per-endpoint signal statistics.
- **Residual confound:** Headers-only extraction may still include some error-related headers (e.g., WWW-Authenticate). Mitigation: explicitly exclude auth-related headers from structural signal if they correlate with behavioral state.

### 8.2 External validity

- **Local testbed vs production:** Testbed is local, not distributed production. CDN simulation is single-node varnish/nginx, not multi-CDN. OAuth middleware is PyJWT, not Auth0/Okta. Mitigation: acknowledge ceiling; testbed eliminates endpoint selection failure but does not prove orthogonality in production.
- **Server framework:** Flask/FastAPI may have different middleware pipelines than Express/Rails/Django. Mitigation: acknowledge framework boundedness; test multiple endpoints with different middleware configurations.

### 8.3 Statistical validity

- **Power:** n=480 provides 80% power for delta=0.15 equivalence test (Fisher z TOST). Minimum detectable |r| = 0.0895 at n=480.
- **Multiple comparisons:** Per-endpoint and per-cache-mode correlations are exploratory; primary inference is pooled r.
- **Bootstrap CI:** Use 1000 bootstrap resamples for CI estimation, stratified by co-occurring condition.

## 9. Analysis plan

### 9.1 Primary analysis

1. Compute behavioral_delta and structural_composite for each paired sample (headers-only)
2. Compute pooled Pearson r across all samples
3. Compute 95% CI using Fisher z-transform
4. Perform TOST equivalence test at delta=0.15
5. Apply decision rule C1-C6

### 9.2 Secondary analysis

1. Per-endpoint Pearson r (structural heterogeneity)
2. Per-cache-mode Pearson r (CDN impact)
3. Per-condition Pearson r (co-occurring condition heterogeneity)
4. Bootstrap CI for pooled r (1000 resamples, stratified)
5. Signal std per endpoint, per cache mode, per condition
6. B-FLASK-ONLY pooled r and CI (baseline comparison)
7. B-ERROR-BODY-INCLUDED pooled r and CI (negative control)

### 9.3 Exploratory analysis

1. Network latency impact on correlation (latency-stratified r)
2. Cache hit rate impact on correlation (hit-rate-stratified r)
3. Token expiry timing impact on correlation (time-since-expiry-stratified r)
4. Comparison of headers-only vs success-body-only structural signal extraction

## 10. Artifacts

- `testbed_server.py` — production-like testbed server implementation (modified for headers-only signal extraction)
- `flask_only_server.py` — B-FLASK-ONLY baseline server implementation
- `run_experiment.py` — experiment execution script
- `experiment_data.json` — raw paired samples
- `analysis.py` — analysis script (compute r, CI, TOST, controls)
- `result.json` — structured results
- `provenance.json` — experiment provenance