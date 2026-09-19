# EXP-GRAPH-35470449310 preregistration

## Status

DESIGN ONLY — pending freeze by deterministic freezer.

## Experiment Identity

- **Experiment ID:** EXP-GRAPH-35470449310
- **Lane:** graph
- **Claim:** C-FRESHNESS
- **Parent:** EXP-GRAPH-35456070379 (MEASUREMENT_INVALID, audit FAIL, V1 request_id entropy confound, V2 B-FLASK-ONLY degenerate)

## Research Question

After correcting two high-severity measurement validity gaps from the parent experiment, does behavioral-structural signal orthogonality at delta=0.15 hold on the production-like local testbed?

## Hypothesis

C-FRESHNESS orthogonality at delta=0.15 will hold on the production-like testbed with corrected measurement. The parent's REJECTED outcome (|r|=0.1737) was measurement-invalid due to:

1. **V1 request_id entropy confound:** Valid responses used `str(uuid.uuid4())` (36-char UUID, entropy ~3.54) while expired 401 responses used `secrets.token_hex(8)` (16-char hex, entropy ~3.23), creating p=2.7e-34 entropy difference that propagated into the structural composite via `request_id_entropy` (weight 0.2) and `dynamic_content_hash` (weight 0.2) components.

2. **V2 B-FLASK-ONLY degenerate baseline:** `flask_only_server.py` implemented no token validation, producing `behavioral_delta=0.0` for all 480 samples (std=0, r=NaN), making C6 baseline check trivially true and uninformative.

With both confounds corrected, the structural signal (ETag variation + Cache-Control variation + UUID-based dynamic content hash) should be independent of behavioral state (token validation/session/auth), yielding |r| < 0.15 consistent with localhost mock evidence (r=0.0022-0.046 across 4 independent experiments).

## Falsifier

C-FRESHNESS orthogonality is falsified at delta=0.15 if ANY of:

1. 95% CI upper bound of pooled Pearson r >= 0.15 on production-like testbed with corrected signal
2. Fewer than 2/3 endpoints have behavioral signal std > 0
3. Fewer than 2/3 endpoints have structural signal std > 0
4. Behavioral detection TP < 0.85
5. C5 cache-mode heterogeneity check fails: |r_enabled - r_disabled| > 2*SE
6. B-FLASK-ONLY baseline shows |r| >= 0.15

## Baselines

### B-LOCALHOST-MOCK (positive baseline)
Prior localhost Flask mock orthogonality:
- r=0.0022, delta=0.15, PASS (EXP-GRAPH-35389145821, n=480, audit PASS)
- r=0.0463, delta=0.15, PASS (EXP-GRAPH-35353011131, n=480, audit PASS)
- r=-0.0258, delta=0.15, PASS (EXP-PRODUCT-35434772331, n=480, audit PASS)
- r=0.0022, delta=0.15, PASS with HTTP caching (EXP-GRAPH-35389145821, n=480, audit PASS)

Expected: |r| < 0.15, consistent with four prior confirmations.

### B-FLASK-ONLY (infrastructure baseline)
Plain Flask WITHOUT CDN simulation, OAuth middleware, or dynamic content, but WITH genuine token-state variation (valid/expired tokens via Authorization header or query param). Uses same corrected headers-only structural signal extraction.

Expected: |r| < 0.15, confirming orthogonality persists without production-like infrastructure features.

### B-PARENT-CONFOUND-REPRODUCTION (negative control)
Reproduction of parent V1 confound: request_id uses `token_hex` for expired responses and `uuid4` for valid responses (the exact prior defect).

Expected: |r| >= 0.15, confirming V1 was a genuine confound and the fix eliminates it.

## Positive Control

Token validation failure detection: behavioral signal must correctly identify expired vs valid tokens with TP >= 0.85. The testbed_server.py `@require_token` decorator returns 401 for expired tokens and the behavioral signal extractor detects `status_code`, `X-Token-Validation` header, and `session_state_change`. TP=1.0 was achieved in all prior experiments. If TP < 0.85, behavioral signal extraction is broken.

## Null Control

Structural signal std > 0 across all conditions: ETag, Cache-Control, and UUID-based dynamic content should produce non-zero structural variation even on cache-disabled responses. Behavioral std > 0 on the 8 co-occurring conditions (valid/expired x cache_enabled/disabled x read/write).

## Measurement Validity

### Fix V1: request_id entropy confound
ALL responses (200, 304, 401, 403) must generate request_id via `uuid.uuid4()`. NO exceptions for error paths. The prior confound: valid responses used `str(uuid.uuid4())` (36-char, entropy ~3.54) while expired 401 responses used `secrets.token_hex(8)` (16-char, entropy ~3.23), creating p=2.7e-34 entropy difference propagating into structural composite via `request_id_entropy` (weight 0.2) and `dynamic_content_hash` (weight 0.2).

### Fix V2: B-FLASK-ONLY degenerate baseline
`flask_only_server.py` must implement genuine token-state variation:
- Valid tokens: Authorization header with valid JWT or query param `token=valid` -> 200 with behavioral variation
- Expired tokens: Authorization header with expired JWT or query param `token=expired` -> 401 with behavioral variation
- The prior baseline had zero auth middleware, producing `behavioral_delta=0.0` for all 480 samples (std=0, r=NaN)

### Additional validity requirements
- Testbed server produces genuine behavioral AND structural stochastic variation
- CDN simulation implements genuine cache behavior: ETag-SHA256, Cache-Control max-age/no-store, 304 via If-None-Match
- OAuth middleware uses real PyJWT RS256 validation
- Dynamic content includes UUID timestamps, request IDs, user-dependent responses, SQLite WAL-mode
- Network latency jitter configurable (10-500ms) and measured
- Structural signal extraction uses ONLY: (a) ETag change (0/1), (b) Cache-Control change (0/1), (c) normalized Shannon entropy of UUID-based request_id, (d) SHA256(request_id)[:16] as int % 10000 / 10000
- Each endpoint has independent behavioral and structural signal extraction — no shared variables between signal domains
- n >= 480 paired samples from >= 3 endpoints x >= 2 cache modes x >= 2 auth states

## Decision Rule

C-FRESHNESS orthogonality at delta=0.15 is **CONFIRMED** if ALL of:

- **(C1)** Behavioral detection TP >= 0.85 across all endpoints (expired tokens correctly detected as drift)
- **(C2)** At least 2/3 endpoints have behavioral signal std > 0 AND at least 2/3 endpoints have structural signal std > 0
- **(C3)** 95% CI upper bound of pooled Pearson r < 0.15 on production-like testbed
- **(C4)** TOST equivalence test p_upper < 0.05 at delta=0.15
- **(C5)** Cache-mode heterogeneity check: |r_cache_enabled - r_cache_disabled| < 2 * SE (CDN effect on correlation within sampling noise)
- **(C6)** B-FLASK-ONLY baseline shows |r| < 0.15 (orthogonality persists without infrastructure)

C-FRESHNESS orthogonality is **REJECTED** if ANY condition fails.

**MEASUREMENT_INVALID** if infrastructure failure prevents data collection (endpoint unreachable, testbed construction fails, n < 240).

## Sample Size

n >= 480 paired samples from 3 endpoints x 2 cache modes x 2 auth states = 8 co-occurring conditions, minimum 60 samples per condition. This provides adequate power for delta=0.15 equivalence test (minimum detectable |r| ~ 0.09 at n=480).

## Testbed Infrastructure

Reuses parent EXP-GRAPH-35456070379 testbed_server.py (Flask 3.1.3, PyJWT RS256, SQLite WAL-mode, CDN simulation with ETag/Cache-Control/304, 3 endpoints) with two targeted fixes:
1. `testbed_server.py`: Replace `secrets.token_hex(8)` in `_make_unauthorized_response()` with `str(uuid.uuid4())`
2. `flask_only_server.py`: Rebuild with simple token validation (valid/expired via header or query param) creating genuine behavioral variation

## Product Consequences

### If CONFIRMED
C-FRESHNESS advances from EXPERIMENTAL toward VALIDATED on production-like infrastructure. Parallel-channel architecture (separate behavioral and structural signal processing) is justified for product deployment. The orthogonality result extends from localhost mock to production-like server with CDN/OAuth/dynamic content. Product may proceed with dual-signal freshness detection.

### If REJECTED
C-FRESHNESS orthogonality fails on production-like infrastructure even with corrected measurement. Parallel-channel architecture is NOT justified. Product must pivot to fused classifiers or cache-independent structural signals. The localhost mock evidence is insufficient for production deployment.

## Expected Information Gain

Very high: this is the minimum cost experiment that directly resolves the two measurement validity gaps blocking C-FRESHNESS product deployment. The same production-like testbed infrastructure is reused with two targeted code fixes. Either outcome changes a product decision.

## Inherited State from Parent Handoff

### Established
- C-FRESHNESS orthogonality confirmed at delta=0.15 under localhost Flask mock across four independent experiments (all n=480, all audit PASS): r=0.0022, r=0.0463, r=-0.0258, r=0.0022 with HTTP caching
- Behavioral signals validated: TP=1.0 across all co-occurring conditions
- HTTP conditional caching (304 at ~32% rate) does NOT break orthogonality on localhost mock
- Production-like testbed infrastructure (Flask 3.1.3, PyJWT RS256, SQLite WAL, CDN simulation, 3 endpoints) is functional and reusable

### Rejected
- Stable public APIs as testbeds (zero behavioral/structural variance)
- Error-body hashing as structural signal (r=0.375 forced correlation)
- n < 480 sufficient for delta=0.15 equivalence

### Unknown
- Whether orthogonality at delta=0.15 holds on production-like infrastructure with corrected headers-only signal
- Whether B-FLASK-ONLY baseline shows |r| < 0.15 with genuine token-state variation
- Whether per-cache heterogeneity is systematic or sampling noise

### Do Not Assume
- C-FRESHNESS reaches VALIDATED or PRODUCT_CORE — status remains EXPERIMENTAL bounded to localhost mock
- The parent's REJECTED outcome (|r|=0.1737) falsifies orthogonality — measurement-invalid
- localhost mock confirmations are true population correlations under production conditions
- Delta=0.10 confirmed for product deployment
- Production-like infrastructure features break orthogonality — untested due to measurement confounds
