# EXP-GRAPH-35530590140 — Preregistration

## Claim

**C-FRESHNESS**: SPIDER can detect when inherited knowledge is stale.

Orthogonality at delta=0.15: behavioral signals (auth/session drift) and structural signals (cache/schema drift) are Pearson-correlated |r| < 0.15 under production-like infrastructure.

## Background

Four independent localhost mock experiments (n=480 each, all audit PASS) established C-FRESHNESS orthogonality: r = 0.0022, 0.0463, 0.0335, -0.0258. B-FLASK-ONLY baseline (no CDN/OAuth/dynamic content) confirmed r=0.0263, TOST PASS.

Parent EXP-GRAPH-35510157861 produced REJECTED outcome (C7 FAIL under consistent non-304 exclusion) on a production-like testbed with CDN simulation, OAuth middleware, and dynamic content. The parent successfully corrected three measurement defects (V_ETAG_PERMISSION_LEAKAGE, C5 pooling bug, C7 definition), but the C7 negative control itself was fragile: its pass/fail depended on 304 inclusion/exclusion rather than on whether the V1 confound was genuine.

Root cause: V1 confound (token_hex vs uuid4 request_id generation) is strong on profile/data_list but null on session_status, and 304 inclusion inflates it because 304s are all-valid and carry the token_hex-vs-uuid4 entropy difference in structural composite. Under consistent non-304 exclusion, C7 FAILS (stratified weighted |r|=0.0735 <0.15).

## Question

After redesigning the B-PARENT-CONFOUND negative control to use a fixed request_id for expired responses (\"expired\") versus UUID for valid responses, thereby creating a confound robust to 304 inclusion/exclusion, does the frozen decision rule yield CONFIRMED (all C1-C7 pass) or REJECTED at delta=0.15 on the production-like testbed with n_non304>=800?

## Hypothesis

C-FRESHNESS orthogonality at delta=0.15 will be CONFIRMED once the fragile V1 confound is replaced with a robust confound. The new confound (fixed \"expired\" request_id for expired responses) creates a strong entropy difference (zero vs high) that correlates with behavioral state, independent of 304 caching. The confound is expected to produce endpoint-stratified weighted |r| >= 0.15 on non-304 samples, confirming the negative control passes. All other conditions C1-C6 are expected to pass as in the parent experiment (C1-C6 PASS).

## Experimental Design

### Testbed

Same production-like testbed as parent:
- Flask 3.1.3, PyJWT RS256, SQLite WAL-mode
- CDN simulation (ETag-SHA256, Cache-Control max-age/no-store, stale-while-revalidate)
- 3 endpoints: /api/user/profile, /api/data/list, /api/session/status
- 8 conditions: {valid, expired} x {cache_enabled, cache_disabled} x {read, write}

### Negative Control Redesign

**B-PARENT-CONFOUND-V2**: Fixed request_id for expired responses

In `testbed_server.py`:
- For expired responses: set request_id = \"expired\" (fixed string)
- For valid responses: set request_id = uuid.uuid4() (random UUID)
- This creates a strong entropy difference (zero vs high) that correlates with behavioral state
- The confound is independent of 304 caching because 304 responses are excluded from analysis
- The confound affects all endpoints uniformly (same mechanism)

Implementation detail:
- In `_make_unauthorized_response()`: change `request_id = str(uuid.uuid4())` to `request_id = \"expired\"`
- In `_make_response()`: keep `request_id = str(uuid.uuid4())` for valid responses
- All other code remains unchanged (V_ETAG fix, C5 stratification, etc.)

### Sampling Protocol

- n >= 800 paired samples from 3 endpoints x 2 cache modes x 2 auth states = 12 cells
- Minimum 60 samples per cell (up from parent's 40)
- Equal allocation across endpoints (no endpoint dominance)
- Randomized request order within endpoint batches
- All request_ids use uuid.uuid4() for valid responses, \"expired\" for expired responses (V2 confound)
- Primary testbed uses uuid.uuid4() for ALL status codes (V1 fix verified)

### Signal Extraction

**Behavioral signals** (same as parent, verified TP=1.0):
- status_code (401 = expired)
- X-Token-Validation header
- session_state_change indicator
- auth_boundary_shift indicator

**Structural signals** (headers-only, EXCLUDING 304):
- ETag change (0/1)
- Cache-Control change (0/1)
- Normalized Shannon entropy of UUID-based request_id (for valid responses)
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

### Baseline 3: B-PARENT-CONFOUND-V2 (Negative Control)
Redesigned negative control: request_id uses fixed string \"expired\" for expired responses, uuid4 for valid responses. Expected: endpoint-stratified weighted |r| >= 0.15 on non-304 samples (confirms confound is genuine). The confound is robust to 304 inclusion/exclusion because 304 responses are excluded from analysis.

## Decision Rule

**CONFIRMED** if ALL:
- C1: behavioral TP >= 0.85 across all endpoints
- C2: >= 2/3 endpoints have non-304 behavioral std > 0 AND >= 2/3 have non-304 structural std > 0
- C3: 95% CI upper of endpoint-stratified pooled r (non-304) < 0.15
- C4: TOST p_upper < 0.05 at delta=0.15 (one-sided, non-304)
- C5: endpoint-stratified cache-mode heterogeneity |r_enabled - r_disabled| < 2 * SE
- C6: B-FLASK-ONLY |r| < 0.15
- C7: B-PARENT-CONFOUND-V2 endpoint-stratified weighted |r| >= 0.15

**REJECTED** if ANY condition fails.

**MEASUREMENT_INVALID** if infrastructure failure prevents data collection (endpoint unreachable, testbed construction fails, n < 400).

## Validity Threats

1. **V2 confound effectiveness**: The fixed \"expired\" request_id must produce a strong entropy difference (zero vs high) that correlates with behavioral state. Expected: strong correlation because request_id entropy is zero for expired responses and high for valid responses.
2. **304 exclusion consistency**: Both primary testbed and B-PARENT-CONFOUND-V2 must exclude 304 responses consistently. The confound is independent of 304 handling because 304 responses are excluded from analysis.
3. **Generalization ceiling**: Orthogonality on localhost production-like testbed does not prove orthogonality on distributed production infrastructure with real CDN hierarchies, concurrent client load, or cache invalidation on session change.
4. **Confound specificity**: The V2 confound tests whether the measurement can detect a known confound; it does not test whether the real-world confound exists. A PASS confirms the measurement is sensitive; a FAIL would indicate the measurement is insensitive to this specific confound.

## Product Consequences

**Positive**: C-FRESHNESS advances toward VALIDATED. Parallel-channel architecture justified. Product deploys dual-signal freshness: behavioral for auth/session drift, structural for cache/schema drift.

**Negative**: C-FRESHNESS fails on production-like infrastructure even with robust negative control. Parallel-channel architecture NOT justified. Product pivots to fused classifiers or abandons structural signals.

## Computation

Estimated 1-2 compute-hours: code change (~10 min), execution (~1 hour at n>=800), analysis (~1 hour).

## Frozen After

This preregistration is frozen at the time of freeze.json creation. No modifications after freeze.