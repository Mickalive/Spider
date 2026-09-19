# Preregistration: EXP-GRAPH-35409927045

## Behavioral-Structural Signal Orthogonality on Real External APIs

**Experiment ID:** EXP-GRAPH-35409927045  
**Lane:** graph  
**Claim:** C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)  
**Date:** 2026-09-19  
**Preregistered by:** SPIDER Research 2.0 Graph Lane Designer  

---

## 1. Background and Motivation

### 1.1 Prior Evidence

Three successive localhost mock experiments have confirmed behavioral-structural signal orthogonality at delta=0.15:

1. **EXP-GRAPH-35267029550** (deterministic Flask): r=0.0335, CI upper 0.123 < 0.15, MIXED (permutation p=0.465 underpowered)
2. **EXP-GRAPH-35353011131** (stochastic Flask+SQLite+cache+jitter): r=0.0463, CI upper 0.135 < 0.15, **PASS** (all C1-C4)
3. **EXP-GRAPH-35389145821** (HTTP caching with If-None-Match/304): r=0.0022, CI upper 0.0916 < 0.15, **PASS** (all C1-C5)

The parent (EXP-GRAPH-35389145821) established: C-FRESHNESS behavioral-structural orthogonality at delta=0.15 is confirmed under operational HTTP conditional caching with proper If-None-Match/304 manipulation at n=480. Claim ceiling bounded to localhost Flask mock.

### 1.2 Critical Gap

The claim ceiling remains bounded to localhost Flask mock. The inherited next question from the parent handoff is:

> Does behavioral-structural signal orthogonality (|r| < 0.15) hold on real external APIs with production databases, distributed caches/CDN, network latency, OAuth/OIDC middleware, and stochastic SPA frontends?

This is the single critical gap for C-FRESHNESS product deployment. Localhost mock experiments cannot answer this question because:

- Real APIs have network latency variation (50-500ms+) vs mock's 1-5ms jitter
- Real APIs may use CDN caching with different ETag/304 semantics than Flask's in-memory cache
- Real APIs have rate limiting that creates behavioral signal variation not present in mock
- Real API response schemas may have natural stochastic variation (timestamps, request IDs)
- Real API auth middleware (OAuth/OIDC) creates different behavioral signal patterns than PyJWT

### 1.3 Experiment Goal

Test whether behavioral-structural signal orthogonality transfers from localhost mock to real external APIs. This is the minimum discriminating experiment that can change the C-FRESHNESS product decision.

---

## 2. Hypothesis

**H1 (alternative):** Behavioral and structural signals are approximately uncorrelated on real public APIs: pooled Pearson r between behavioral composite and structural signal has 95% CI upper bound < 0.15 (delta=0.15 TOST equivalence).

**H0 (null):** Behavioral and structural signals are correlated on real public APIs: CI upper bound >= 0.15.

---

## 3. State Representation

### 3.1 Behavioral Signals

Extracted from HTTP response headers and status codes on real API endpoints:

| Signal | Source | Description |
|--------|--------|-------------|
| rate_limit_remaining | X-RateLimit-Remaining header | Low values indicate rate limit pressure |
| rate_limit_detection | rate_limit_remaining < 10 | Binary: rate limit approaching |
| auth_challenge | 401/403 status on auth probe | Binary: auth boundary shift detected |
| cache_freshness | Cache-Control max-age / no-store | Staleness indicator from cache headers |
| response_time_ms | Round-trip time | Latency variation (proxy for server load) |
| status_class | HTTP status code bin (2xx/3xx/4xx/5xx) | Response category |

**Composite formula:** Same as parent (adapted for real API headers):
```
behavioral_composite = rate_limit_detection * 2 + auth_challenge * 3 + cache_freshness * 1 + status_class_score * 2
```

Where status_class_score = {200: 0.0, 301: 0.2, 304: 0.1, 401: 1.0, 403: 0.5, 404: 0.3, 429: 0.8, 500: 0.75}

### 3.2 Structural Signals

Computed from response body JSON schema (field names and types):

| Signal | Description |
|--------|-------------|
| jaccard_similarity | Jaccard((name,type) pairs) between baseline and current response |
| schema_diff_magnitude | Weighted field add/remove/type-change/description-change magnitude |
| structural_composite | max(schema_diff_magnitude, 1.0 - jaccard_similarity) |

Same computation as parent (compute_jaccard_similarity, compute_schema_diff_magnitude).

### 3.3 Representation Loss

- Real API response bodies may contain timestamps, request IDs, or other naturally varying fields that create structural variation unrelated to "staleness"
- Auth probe behavioral signals depend on API's auth model (some APIs don't require auth)
- Cache headers are infrastructure-dependent and may not be present on all APIs
- Response time is a noisy proxy for server load

---

## 4. Action Representation

For each paired sample:

1. **Baseline request:** GET endpoint with standard headers, record response body, headers, status, timing
2. **Conditional request:** GET endpoint with If-None-Match (if ETag available), record 304/200
3. **Auth probe (if applicable):** GET endpoint with invalid Bearer token, record 401/403
4. **Current request:** GET endpoint (after brief delay for natural variation), record response body, headers, status, timing

---

## 5. Target API Endpoints

### 5.1 Primary Endpoints

| Endpoint | URL | Auth Required | ETag Support | Rationale |
|----------|-----|---------------|--------------|-----------|
| GitHub Repos | https://api.github.com/repos/octocat/Hello-World | No (public) | Yes | Real API with rate limiting, ETags, rich schema |
| GitHub Users | https://api.github.com/users/octocat | No (public) | Yes | Different schema, same infrastructure |
| JSONPlaceholder | https://jsonplaceholder.typicode.com/posts/1 | No | No | Simple REST, no rate limiting, stable schema |

### 5.2 Fallback Endpoints

If primary endpoints unreachable:

| Endpoint | URL | Notes |
|----------|-----|-------|
| httpbin Get | https://httpbin.org/get | Returns request headers as body |
| httpbin Headers | https://httpbin.org/response-headers?X-Test=1 | Custom headers |

### 5.3 Endpoint Selection Criteria

- Must be publicly accessible without authentication (for baseline)
- Must return JSON responses (for structural signal extraction)
- Should have some natural variation (for behavioral signal variance)
- Rate limit policy must allow ~200 requests within experiment duration

---

## 6. Sampling Policy

### 6.1 Sample Size

- **N_SAMPLES = 160** per endpoint (480 total across 3 endpoints)
- This matches the parent's n=480 for direct CI comparison
- Minimum for delta=0.15 TOST with expected |r| < 0.05: n ~ 350 (adequate)

### 6.2 Sampling Procedure

For each endpoint, for each sample i (1 to N_SAMPLES):

1. GET baseline, record body/headers/status/timing
2. If ETag available: GET with If-None-Match, record 304/200 (C5 check)
3. Wait 1-2 seconds (rate limit respect + natural variation)
4. Auth probe: GET with "Bearer invalid_token_${i}", record 401/403 (if auth endpoint)
5. GET current, record body/headers/status/timing
6. Compute behavioral composite from headers/status
7. Compute structural composite from baseline vs current body

### 6.3 Randomization

- Seed: SEED=42
- Request order within condition: deterministic (endpoint顺序固定)
- Permutation test for null: 1000 random label permutations

### 6.4 Exclusions

- Network timeout (>15s): exclude sample, record as missing
- Non-JSON response: exclude sample, record as missing
- HTTP 5xx: exclude from structural analysis, include in behavioral analysis
- Duplicate request (same ETag + same response): exclude from structural (no variation)

---

## 7. Unit of Analysis

Each paired (baseline, current) request to a single endpoint is one observation. Observations are paired by endpoint and sample index.

---

## 8. Holdout

No train/test split. This is a single confirmatory test on pooled data. The parent's three-generation evidence base serves as the "training" context; this experiment is the held-out test on real APIs.

---

## 9. Controls

### 9.1 Positive Control (PC-AUTH-DETECTION)

**Purpose:** Verify that behavioral signal extraction works on real APIs.

**Procedure:** For each endpoint that supports auth probing (GitHub), send requests with invalid Bearer tokens. Behavioral signals should detect auth boundary shifts.

**Pass criterion:** At least 1/2 GitHub endpoints shows behavioral signal variance > 0 when probed with valid vs invalid auth. Wilson lower CI on detection rate > 0.75.

### 9.2 Null Control (NC-STABLE-ENDPOINT)

**Purpose:** Verify no false behavioral detection on stable endpoints.

**Procedure:** Query JSONPlaceholder /posts/1 repeatedly (no auth, no rate limiting). Behavioral composite should be 0 for all samples.

**Pass criterion:** FP = 0.0 (no samples with behavioral composite > 0 on stable endpoint).

### 9.3 Anti-Null (B-MOCK-ANTI-NULL)

**Purpose:** Verify the measurement can detect correlation when present.

**Procedure:** On one endpoint (httpbin), artificially couple signals: set behavioral_composite = structural_composite + noise. This creates known correlation.

**Pass criterion:** |r| > 0.3 on the anti-null endpoint, demonstrating the measurement is sensitive to correlation.

---

## 10. Primary Metric

**Pooled Pearson correlation coefficient r** between behavioral composite and structural composite across all valid paired samples from all endpoints.

**Equivalence test:** TOST at delta=0.15. CI upper bound on |r| must be < 0.15 for H1 to pass.

**Secondary metrics:**
- Per-endpoint r values
- Per-endpoint behavioral and structural signal distributions
- Behavioral detection rate (TP) on auth probes
- False positive rate on stable endpoint
- 304 rate on ETag-supporting endpoints (C5 manipulation check)
- Network success rate per endpoint

---

## 11. Expected Direction

H1 predicts |r| < 0.15 (orthogonality). The parent mock result (r=0.0022) suggests the true correlation is near zero.

If real APIs show higher |r| than mock, the most likely explanations are:
1. CDN caching creates correlated staleness signatures (behavioral cache headers + structural body changes)
2. Rate limiting creates behavioral variation that coincidentally correlates with schema changes
3. Network latency variation introduces noise that affects both signals

---

## 12. Uncertainty Method

- 95% Fisher z-transformed CI for Pearson r
- TOST equivalence test at delta=0.15 with alpha=0.05
- Wilson CI for proportions (TP rate, FP rate)
- Bootstrap CI (1000 resamples) for per-endpoint correlations

---

## 13. Adequacy Rule

The experiment is adequate if:
- >= 2/3 target APIs are reachable (C5)
- >= 480 valid paired samples collected
- Both behavioral and structural signals have variance > 0 on >= 3/3 endpoints (C2)
- Behavioral detection works on at least one endpoint (C1)

If network access is completely unavailable: status=BLOCKED, no scientific conclusion.

---

## 14. Falsification / Survival Rule

**SUPPORTS (H1 survives):** ALL five conditions C1-C5 pass (spec.json decision_rule).

**FALSIFIES:** C3 fails with CI upper >= 0.20 (signals correlated on real APIs).

**MIXED:** C3 fails with CI upper in [0.15, 0.20) (inconclusive, larger sample needed).

**MEASUREMENT_INVALID:** C1, C2, or C4 fails (behavioral extraction or variance insufficient).

**BLOCKED:** C5 fails (network unavailable).

---

## 15. Deviation Policy

No deviations from this preregistration are permitted after execution begins. All analysis decisions are frozen above.

If a target API becomes unavailable mid-experiment:
- If >= 2 APIs remain: continue with remaining endpoints
- If < 2 APIs remain: status=BLOCKED

If response format changes (non-JSON): exclude affected samples, do not redesign.

---

## 16. Consequences

**If SUPPORTS:** C-FRESHNESS advances toward VALIDATED. Parallel-channel architecture (independent behavioral + structural freshness detectors) is justified for product deployment. Product can implement independent freshness probes without fused classification overhead.

**If FALSIFIES:** C-FRESHNESS requires fused classifier or fundamentally different signal architecture. Behavioral and structural signals are coupled on real APIs (e.g., CDN caching creates correlated staleness signatures). Product must combine signals into a single detector or find cache-independent structural signals.

**If MIXED:** Decision deferred. Larger sample (n >= 1000) or more endpoints needed. C-FRESHNESS remains EXPERIMENTAL.

**If BLOCKED:** No scientific conclusion. Re-run when network access available. Consider enhanced mock with production-like features as interim step.
