# EXP-GRAPH-35481774794 — Preregistration

## Claim

**C-FRESHNESS**: SPIDER can detect when inherited knowledge is stale.

Orthogonality at delta=0.15: behavioral signals (auth/session drift) and structural signals (cache/schema drift) are Pearson-correlated |r| < 0.15 under production-like infrastructure.

## Background

Four independent localhost mock experiments (n=480 each, all audit PASS) established C-FRESHNESS orthogonality: r = 0.0022, 0.0463, 0.0335, -0.0258. B-FLASK-ONLY baseline (no CDN/OAuth/dynamic content) confirmed r=0.0263, TOST PASS.

Parent EXP-GRAPH-35476270792 produced MIXED outcome (C5 FAIL, C7 FAIL) on a production-like testbed with CDN simulation, OAuth middleware, and dynamic content. However, audit identified three measurement defects contaminating the result:

1. **V3 selection bias**: Valid cache-enabled non-304 composition skewed 91% session_status (40/44), inflating pooled r from true stratified ~0.04 to -0.126 and C5 heterogeneity diff from ~0.25 to 0.466.
2. **V_ETAG_PERMISSION_LEAKAGE**: Expired tokens default to read-etag, violating structural independence for write-permission conditions.
3. **Insufficient power**: n=480 gives minimum detectable |r| ~0.09, insufficient for C5/C7 thresholds.

Audit-computed non-304 per-endpoint r (profile 0.009, data_list 0.122, session -0.013) and stratified pooled r ~0.04 suggest the true signal is near-zero within endpoints.

## Question

After three targeted measurement corrections, does the frozen decision rule yield CONFIRMED (all C1-C7 pass) or REJECTED (any fails) at delta=0.15 on the production-like testbed?

## Hypothesis

C-FRESHNESS orthogonality at delta=0.15 will be CONFIRMED once measurement defects are corrected. The true pooled non-304 r is ~0.04 (stratified), well below delta=0.15.

## Experimental Design

### Testbed

Same production-like testbed as parent:
- Flask 3.1.3, PyJWT RS256, SQLite WAL-mode
- CDN simulation (ETag-SHA256, Cache-Control max-age/no-store, stale-while-revalidate)
- 3 endpoints: /api/user/profile, /api/data/list, /api/session/status
- 8 conditions: {valid, expired} x {cache_enabled, cache_disabled} x {read, write}

### Three Targeted Fixes

**Fix 1: V3 Selection Bias** — Endpoint-stratified pooling

Instead of raw pooled concatenation, compute endpoint-stratified pooled r:

```
r_stratified = sum(n_i * r_i) / sum(n_i)
```

where i indexes endpoints, n_i is endpoint sample count, r_i is endpoint Pearson r. This removes the artifact of endpoint-heterogeneity inflating pooled r.

Apply to: C3 (pooled equivalence), C4 (TOST), C5 (cache heterogeneity).

**Fix 2: V_ETAG_PERMISSION_LEAKAGE** — Session-derived permission_level

In `testbed_server.py _make_unauthorized_response()`:
- Currently: permission_level defaults to 'read' because expired tokens don't carry permission payload
- Fix: Pass permission_level explicitly from request handler context (before token expiry check), or derive from session/endpoint context independent of token validity
- Verify: valid and expired write-permission requests produce overlapping ETags (same stable_key)

**Fix 3: Power Increase** — n >= 800

Increase paired samples from 480 to >= 800 across conditions. This reduces SE from ~0.050 to ~0.035 and minimum detectable |r| from ~0.09 to ~0.07, providing adequate power for C5 heterogeneity and C7 negative control thresholds.

### Sampling Protocol

- n >= 800 paired samples from 3 endpoints x 2 cache modes x 2 auth states = 12 cells
- Minimum 60 samples per cell (up from parent's 40)
- Equal allocation across endpoints (no endpoint dominance)
- Randomized request order within endpoint batches
- All request_ids use uuid.uuid4() for all status codes (V1 fix verified)

### Signal Extraction

**Behavioral signals** (same as parent, verified TP=1.0):
- status_code (401 = expired)
- X-Token-Validation header
- session_state_change indicator
- auth_boundary_shift indicator

**Structural signals** (headers-only, EXCLUDING 304):
- ETag change (0/1)
- Cache-Control change (0/1)
- Normalized Shannon entropy of UUID-based request_id
- SHA256(request_id)[:16] as int % 10000 / 10000

304 responses excluded from ALL correlations (pooled, per-endpoint, per-cache) because they use different structural construction (fixed 0.2 vs variable sha256).

## Controls

### Positive Control
Token validation failure detection: TP >= 0.85 across all endpoints. Expired tokens must be correctly identified as behavioral drift. TP=1.0 in all prior experiments.

### Null Control
Structural signal std > 0 across all non-304 conditions. ETag, Cache-Control, and UUID-based content should produce non-zero variation even on cache-disabled responses.

### Baseline 1: B-LOCALHOST-MOCK
Prior localhost Flask mock: pooled r=0.0022-0.046, all PASS (4 experiments, n=480 each). Expected: |r| < 0.15.

### Baseline 2: B-FLASK-ONLY
Plain Flask without CDN/OAuth/dynamic content, with genuine token validation. Parent: r=0.0263, TOST PASS, n=480. Expected: |r| < 0.15.

### Baseline 3: B-PARENT-CONFOUND-REPRODUCTION (Negative Control)
Reproduces V1 confound: request_id uses token_hex for expired, uuid4 for valid. Expected: |r| >= 0.15 (confirms V1 was genuine). Parent: |r|=0.120 (FAIL at n=480). At n>=800 with stronger entropy bifurcation, expect |r| >= 0.15.

## Decision Rule

**CONFIRMED** if ALL:
- C1: behavioral TP >= 0.85 across all endpoints
- C2: >= 2/3 endpoints have non-304 behavioral std > 0 AND >= 2/3 have non-304 structural std > 0
- C3: 95% CI upper of endpoint-stratified pooled r (non-304) < 0.15
- C4: TOST p_upper < 0.05 at delta=0.15 (one-sided, non-304)
- C5: endpoint-stratified cache-mode heterogeneity |r_enabled - r_disabled| < 2 * SE
- C6: B-FLASK-ONLY |r| < 0.15
- C7: B-PARENT-CONFOUND |r| >= 0.15

**REJECTED** if ANY condition fails.

**MEASUREMENT_INVALID** if infrastructure failure prevents data collection (endpoint unreachable, testbed construction fails, n < 400).

## Validity Threats

1. **Endpoint heterogeneity**: Session_status endpoint has higher structural mean (~0.57) than profile/data_list (~0.29-0.31). Stratified pooling corrects for this but residual heterogeneity may persist.
2. **B-PARENT-CONFOUND at n=480**: Parent observed |r|=0.120 < 0.15. At n>=800, the stronger entropy bifurcation (token_hex vs uuid4) may reach |r| >= 0.15. If it does not, the negative control interpretation changes (V1 confound weaker than assumed, or header-only extraction dilutes effect).
3. **ETag permission fix effectiveness**: The fix must ensure write-permission expired requests produce the same ETag as write-permission valid requests. Verification: overlap check.
4. **Generalization ceiling**: Orthogonality on localhost production-like testbed does not prove orthogonality on distributed production infrastructure with real CDN hierarchies, concurrent client load, or cache invalidation on session change.

## Product Consequences

**Positive**: C-FRESHNESS advances toward VALIDATED. Parallel-channel architecture justified. Product deploys dual-signal freshness: behavioral for auth/session drift, structural for cache/schema drift.

**Negative**: C-FRESHNESS fails on production-like infrastructure. Parallel-channel architecture NOT justified. Product pivots to fused classifiers or abandons structural signals.

## Computation

Estimated 2-3 compute-hours: code fixes (~45 min), execution (~1 hour at n>=800), analysis (~1 hour).

## Frozen After

This preregistration is frozen at the time of freeze.json creation. No modifications after freeze.
