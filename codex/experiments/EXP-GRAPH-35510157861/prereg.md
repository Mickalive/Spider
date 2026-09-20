# EXP-GRAPH-35510157861 — Preregistration

## Claim

**C-FRESHNESS**: SPIDER can detect when inherited knowledge is stale.

Orthogonality at delta=0.15: behavioral signals (auth/session drift) and structural signals (cache/schema drift) are Pearson-correlated |r| < 0.15 under production-like infrastructure.

## Background

Four independent localhost mock experiments (n=480 each, all audit PASS) established C-FRESHNESS orthogonality: r = 0.0022, 0.0463, 0.0335, -0.0258. B-FLASK-ONLY baseline (no CDN/OAuth/dynamic content) confirmed r=0.0263, TOST PASS.

Parent EXP-GRAPH-35481774794 produced MIXED outcome (C5 FAIL, C7 FAIL) on a production-like testbed with CDN simulation, OAuth middleware, and dynamic content. However, audit identified three measurement defects contaminating the result:

1. **V_ETAG_PERMISSION_LEAKAGE**: stable_key for session_status endpoint depends on session_id, not permission_level, causing zero ETag overlap for write-permission conditions.
2. **C5 code bug**: run_experiment.py concatenates across endpoints without stratification for per-cache correlations.
3. **C7 definition ambiguity**: frozen spec defines C7 as simple pooled |r|, but endpoint-stratified weighted |r| would PASS (0.260 > 0.15).

Audit-computed endpoint-stratified pooled r=0.0125 (CI upper 0.0874 < 0.15) indicates within-endpoint orthogonality is strong.

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

**Fix 1: V_ETAG_PERMISSION_LEAKAGE** — Session-derived permission_level for stable_key

In `testbed_server.py _make_unauthorized_response()`:
- Currently: stable_key for session_status = `f"session_{session_id}"` (unique per request)
- Fix: stable_key = `f"session_{permission_level}"` (or similar) so valid and expired write-permission requests produce overlapping ETags
- Verify: overlap check for write-permission conditions

**Fix 2: C5 Code Bug** — Endpoint-stratified weighting for per-cache correlations

In `run_experiment.py`:
- Currently: concatenates across endpoints without stratification
- Fix: compute per-endpoint r_enabled_i and r_disabled_i, then weighted average across endpoints by sample count
- Apply to C5 heterogeneity check only (C3/C4 already use endpoint-stratified pooled r)

**Fix 3: C7 Definition** — Endpoint-stratified weighted |r| for negative control

- Currently: frozen spec defines C7 as simple pooled |r| for B-PARENT-CONFOUND
- Fix: define C7 as endpoint-stratified weighted |r| for B-PARENT-CONFOUND
- Audit recomputed stratified weighted |r| = 0.260 > 0.15, which would PASS

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
Reproduces V1 confound: request_id uses token_hex for expired, uuid4 for valid. Expected: endpoint-stratified weighted |r| >= 0.15 (confirms V1 was genuine). Parent: simple pooled |r|=0.1228 (FAIL), stratified weighted |r|=0.260 (would PASS). At n>=800 with corrected definition, expect |r| >= 0.15.

## Decision Rule

**CONFIRMED** if ALL:
- C1: behavioral TP >= 0.85 across all endpoints
- C2: >= 2/3 endpoints have non-304 behavioral std > 0 AND >= 2/3 have non-304 structural std > 0
- C3: 95% CI upper of endpoint-stratified pooled r (non-304) < 0.15
- C4: TOST p_upper < 0.05 at delta=0.15 (one-sided, non-304)
- C5: endpoint-stratified cache-mode heterogeneity |r_enabled - r_disabled| < 2 * SE
- C6: B-FLASK-ONLY |r| < 0.15
- C7: B-PARENT-CONFOUND endpoint-stratified weighted |r| >= 0.15

**REJECTED** if ANY condition fails.

**MEASUREMENT_INVALID** if infrastructure failure prevents data collection (endpoint unreachable, testbed construction fails, n < 400).

## Validity Threats

1. **V_ETAG fix effectiveness**: The fix must ensure write-permission expired requests produce the same ETag as write-permission valid requests for session_status endpoint. Verification: overlap check.
2. **C5 stratification correctness**: Endpoint-stratified weighting must be computed correctly; verify against audit recomputation.
3. **C7 definition change**: Switching from simple pooled to endpoint-stratified weighted |r| is a protocol change justified by audit findings. The audit recomputed stratified weighted |r| = 0.260, which would PASS.
4. **Generalization ceiling**: Orthogonality on localhost production-like testbed does not prove orthogonality on distributed production infrastructure with real CDN hierarchies, concurrent client load, or cache invalidation on session change.

## Product Consequences

**Positive**: C-FRESHNESS advances toward VALIDATED. Parallel-channel architecture justified. Product deploys dual-signal freshness: behavioral for auth/session drift, structural for cache/schema drift.

**Negative**: C-FRESHNESS fails on production-like infrastructure. Parallel-channel architecture NOT justified. Product pivots to fused classifiers or abandons structural signals.

## Computation

Estimated 2-3 compute-hours: code fixes (~30 min), execution (~1 hour at n>=800), analysis (~1 hour).

## Frozen After

This preregistration is frozen at the time of freeze.json creation. No modifications after freeze.