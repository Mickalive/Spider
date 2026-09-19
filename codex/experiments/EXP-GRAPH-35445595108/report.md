# EXP-GRAPH-35445595108: C-FRESHNESS Orthogonality on Production-like Testbed

**Experiment ID:** EXP-GRAPH-35445595108  
**Lane:** graph  
**Claim:** C-FRESHNESS  
**Status:** COMPLETE  
**Outcome:** FALSIFIES  

---

## 1. Summary

C-FRESHNESS behavioral-structural signal orthogonality at delta=0.15 is **FALSIFIED** on a production-like local testbed server with CDN simulation, OAuth2 middleware, dynamic content, and database-backed state.

- **Pearson r = 0.3751** (95% CI [0.2956, 0.4496], CI upper 0.4496 > 0.15)
- **TOST p_upper = 0.9998** (equivalence at delta=0.15 fails)
- **C1 Behavioral Detection:** PASS (expired_TP=1.0000, valid_TN=1.0000)
- **C2 Variance Gate:** PASS (3/3 endpoints have both behavioral and structural variance)
- **C3 Orthogonality:** FAIL (CI upper 0.4496 > 0.15)
- **C4 Null Control:** PASS (structural signal std > 0 with cache disabled)
- **C5 304 Manipulation:** PASS (304 rate = 0.3167 >= 0.10)

---

## 2. Experiment Design

### 2.1 Testbed Server Architecture

Production-like local testbed server combining:
- **CDN Simulation:** Flask-based ETag-SHA256 with Cache-Control max-age/no-store, stale-while-revalidate, 304 Not Modified responses
- **OAuth2 Middleware:** PyJWT RS256 with access tokens (15-min expiry), refresh tokens, session invalidation, permission boundary
- **Dynamic Content:** Database-backed responses (SQLite WAL-mode) with timestamps, request IDs, user-dependent responses
- **Configurable Network Latency:** Jitter injection (10-200ms uniform)

### 2.2 Endpoints

| Endpoint | Behavioral Variation | Structural Variation |
|----------|---------------------|---------------------|
| `/api/user/profile` | Token validation, session state, permission boundary | ETag-SHA256, Cache-Control, dynamic content |
| `/api/data/list` | Rate limiting, token expiry, auth boundary | Cache-Control max-age, timestamps, request IDs |
| `/api/session/status` | Session invalidation detection | Cache-Control no-store, ETag |

### 2.3 Co-occurring Conditions (8)

Token state (valid/expired) x Cache mode (enabled/disabled) x Permission (read/write)

### 2.4 Sampling Plan

- **N = 480** paired samples (60 per condition x 8 conditions)
- **3 endpoints** x 160 requests each
- **Seed:** 42
- **Behavioral signal:** Weighted composite of token_validation_failure, session_state_change, auth_boundary_shift
- **Structural signal:** SHA-256 hash of stable content identifiers

---

## 3. Results

### 3.1 Primary Metric

| Metric | Value |
|--------|-------|
| Pearson r (pooled) | 0.3751 |
| 95% CI | [0.2956, 0.4496] |
| CI upper | 0.4496 |
| TOST p_upper at delta=0.15 | 0.9998 |
| N | 480 |

### 3.2 Per-Endpoint Results

| Endpoint | Pearson r | p-value | n |
|----------|-----------|---------|---|
| /api/user/profile | 0.2065 | 0.0088 | 160 |
| /api/data/list | 0.3491 | 6.04e-06 | 160 |
| /api/session/status | 0.3201 | 3.69e-05 | 160 |

All three endpoints show significant positive correlation (p < 0.01).

### 3.3 Per-Cache-Mode Results

| Mode | Pearson r | n |
|------|-----------|---|
| Cache-enabled | 0.3062 | 240 |
| Cache-disabled | 0.2918 | 240 |

Correlation persists regardless of cache mode, suggesting the correlation is not caused by CDN caching alone.

### 3.4 Behavioral Detection (C1)

- **Expired token conditions:** TP rate = 1.0000 (all 240 expired-token samples correctly identified)
- **Valid token conditions:** TN rate = 1.0000 (all 240 valid-token samples correctly identified)
- C1 PASS

### 3.5 Variance Gate (C2)

All 3 endpoints have both behavioral and structural signal variance > 0:
- /api/user/profile: behavioral_std=2.98, structural_std=0.15
- /api/data/list: behavioral_std=2.98, structural_std=0.19
- /api/session/status: behavioral_std=3.50, structural_std=0.22
- C2 PASS

### 3.6 Null Control (C4)

Structural signal has non-zero standard deviation with cache disabled:
- null_control_std > 0
- C4 PASS

### 3.7 304 Manipulation Check (C5)

304 responses occur in 31.67% of cache-enabled requests, confirming the CDN simulation is functional.
- C5 PASS

---

## 4. Interpretation

### 4.1 Key Finding

C-FRESHNESS orthogonality is **falsified** on the production-like testbed. The correlation between behavioral and structural signals (r=0.375, CI upper 0.450) significantly exceeds the delta=0.15 threshold. This is in contrast to the localhost Flask mock baseline (r=0.0022 to 0.0463) where orthogonality was confirmed.

### 4.2 What Caused the Correlation?

The production-like infrastructure introduces correlation between behavioral and structural signals through several mechanisms:

1. **Token expiry affects both signals simultaneously:** When a token expires, the `@require_token` decorator returns 401 (behavioral signal), and the response body changes to an error format (structural signal), creating a strong correlation.

2. **Session state affects content:** The session state (valid/invalid) influences both the behavioral signal (session_state_change) and the structural signal (different response content for invalid sessions).

3. **Permission boundaries affect response content:** Different permission levels produce different response bodies, which correlates with the auth boundary signal.

4. **Dynamic content creation:** The server generates content that depends on both the token state and the user identity, creating a structural signal that varies with behavioral state.

### 4.3 Implications

The localhost Flask mock (r=0.0022 to 0.0463) may have underestimated the correlation because it lacked the real infrastructure features that create coupling between behavioral and structural signals. The production-like testbed demonstrates that CDN simulation, OAuth2 middleware, and dynamic content introduce correlation that violates the C-FRESHNESS orthogonality assumption.

### 4.4 What Did NOT Cause the Correlation?

- **CDN caching alone:** Correlation persists at similar levels with cache disabled (r=0.292) and enabled (r=0.306), suggesting CDN caching is not the primary cause.
- **304 manipulation:** The 304 manipulation check passed, confirming the CDN simulation is functional.

---

## 5. Validity Considerations

### 5.1 Internal Validity

- **Behavioral signal construction:** The behavioral composite (weighted sum of token_validation_failure, session_state_change, auth_boundary_shift) may conflate different types of behavioral variation. The correlation could be driven primarily by token validation failures, which naturally correlate with response body changes.
- **Structural signal construction:** The structural signal uses SHA-256 hashes of stable content identifiers, which may not adequately capture structural variation independent of behavioral state.
- **Sample size:** N=480 provides adequate power (min detectable |r| = 0.0895 at n=480).

### 5.2 External Validity

- **Local testbed:** The testbed is local (127.0.0.1), not distributed production. CDN simulation is single-node Flask, not multi-CDN. OAuth middleware is PyJWT, not Auth0/Okta.
- **Single framework:** All code is Flask 3.1.3. Results may not generalize to Express, Django, or Rails.
- **Limited infrastructure features:** The testbed lacks distributed cache coherence, CDN purge, concurrent client load, and other production features.

### 5.3 Statistical Validity

- **Power:** n=480 provides 80% power for delta=0.15 equivalence test.
- **Multiple comparisons:** Per-endpoint and per-cache-mode correlations are exploratory; primary inference is pooled r.
- **Bootstrap CI:** Fisher z-transformed CI is used for the primary analysis.

---

## 6. Product Consequences

### 6.1 If C-FRESHNESS FALSIFIES (Current Outcome)

- **Parallel-channel architecture is NOT justified** on production-like infrastructure
- Product must pivot to **fused classifiers** (combined behavioral-structural signal) or **cache-independent structural signals**
- The localhost mock evidence is **insufficient for production deployment**
- The critical gap for C-FRESHNESS remains open

### 6.2 What Would Have Been Needed

If orthogonality had been confirmed, the parallel-channel architecture would have been justified for product deployment, with behavioral signals for auth/session drift and structural signals for cache/schema drift.

---

## 7. Next Steps

1. **Identify the specific mechanism causing correlation:** Decompose the correlation into token validation, session state, permission boundary, and dynamic content components.
2. **Test with orthogonal infrastructure features:** Separate CDN simulation, OAuth2, and dynamic content to identify which feature introduces the most correlation.
3. **Test on non-Flask frameworks:** Determine if the correlation is framework-specific.
4. **Consider alternative structural signals:** Use signals that are truly independent of behavioral state.
5. **Test with production infrastructure:** Deploy on actual CDN + OAuth infrastructure if available.

---

## 8. Artifacts

- `testbed_server.py` — Production-like testbed server implementation
- `run_experiment.py` — Experiment execution script
- `raw_evidence/experiment_data.json` — Raw paired samples (480)
- `result.json` — Structured results
- `provenance.json` — Experiment provenance

---

## 9. Comparison with Previous Experiments

| Experiment | Environment | r | CI upper | Result |
|------------|-------------|---|----------|--------|
| EXP-GRAPH-35330739886 | Deterministic Flask | 0.0335 | < 0.15 | SUPPORTS |
| EXP-GRAPH-35353011131 | Stochastic Flask+SQLite | 0.0463 | < 0.15 | SUPPORTS |
| EXP-GRAPH-35389145821 | HTTP conditional caching | 0.0022 | 0.0916 | SUPPORTS |
| **EXP-GRAPH-35445595108** | **Production-like testbed** | **0.3751** | **0.4496** | **FALSIFIES** |

The correlation increases dramatically from localhost mock (r ~ 0.002-0.046) to production-like testbed (r = 0.375). This suggests that production-like infrastructure features introduce correlation that the localhost mock cannot replicate.
