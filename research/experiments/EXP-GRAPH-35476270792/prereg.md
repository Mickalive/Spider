# EXP-GRAPH-35476270792 preregistration

## Status

DESIGN ONLY — pending freeze by deterministic freezer.

## Experiment Identity

- **Experiment ID:** EXP-GRAPH-35476270792
- **Lane:** graph
- **Claim:** C-FRESHNESS
- **Parent:** EXP-GRAPH-35470449310 (MEASUREMENT_INVALID, audit REVISE, V3 304 cache-hit coupling, V4 B-PARENT missing, V5 C3/C4 two-sided deviation)

## Research Question

After eliminating V3 (304 cache-hit structural coupling) by excluding 304 responses from pooled correlation and by running the missing B-PARENT-CONFOUND-REPRODUCTION baseline, does behavioral-structural signal orthogonality at delta=0.15 hold on the production-like local testbed?

## Hypothesis

C-FRESHNESS orthogonality at delta=0.15 will hold on the production-like testbed once V3 is eliminated. The parent's MIXED outcome (|r|=0.0877 pooled, C3/C4 FAIL under two-sided interpretation) was measurement-invalid due to:

1. **V3 304 cache-hit structural coupling:** 304 responses use a different structural composite construction (fixed 0.2 constant for dynamic_content_hash instead of variable sha256 hash, run_experiment.py:363-374) and occur exclusively for valid tokens (76 valid 304 vs 0 expired). This token-state-dependent construction violates spec measurement_validity clause 8 (no shared variables between signal domains) and inflates cache-mode heterogeneity. The simplest fix is to exclude 304 responses from pooled correlation entirely.

2. **V4 B-PARENT missing:** The frozen spec requires B-PARENT-CONFOUND-REPRODUCTION negative control (request_id via token_hex for expired vs uuid for valid, expected |r|>=0.15) to confirm the V1 entropy confound was genuine. Producer never executed this baseline.

3. **V5 C3/C4 two-sided deviation:** Producer implemented C3 as CI within (-0.15, 0.15) (both bounds) and C4 as two-sided TOST pass, while frozen spec defines C3 as CI upper < 0.15 (one-sided) and C4 as TOST p_upper < 0.05 (one-sided). Under frozen one-sided rule, the parent data would have C3 PASS (upper 0.0018 < 0.15) and C4 PASS (p_upper 8.88e-08 < 0.05); only C5 (heterogeneity) fails.

With 304 excluded from correlation, B-PARENT executed, and C3/C4 interpreted one-sided, the remaining non-304 structural signal should be independent of behavioral state, yielding |r| < 0.15 consistent with localhost mock evidence.

## Falsifier

C-FRESHNESS orthogonality is falsified at delta=0.15 if ANY of:

1. 95% CI upper bound of pooled Pearson r (non-304 only) >= 0.15 on production-like testbed
2. Fewer than 2/3 endpoints have behavioral signal std > 0
3. Fewer than 2/3 endpoints have non-304 structural signal std > 0
4. Behavioral detection TP < 0.85
5. C5 cache-mode heterogeneity check fails: |r_enabled - r_disabled| > 2*SE (on non-304 samples)
6. B-FLASK-ONLY baseline shows |r| >= 0.15
7. B-PARENT-CONFOUND-REPRODUCTION shows |r| < 0.15 (negative control fails to reproduce V1 confound)

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
Reproduction of parent V1 confound: request_id uses `token_hex` for expired responses and `uuid4` for valid responses (the exact prior defect). This is a negative control — if it shows |r| < 0.15, the V1 confound was not genuine or the fix is incomplete.

Expected: |r| >= 0.15 (confirming V1 was a genuine confound and the fix eliminates it).

## Positive Control

Token validation failure detection: behavioral signal must correctly identify expired vs valid tokens with TP >= 0.85. The testbed_server.py `@require_token` decorator returns 401 for expired tokens and the behavioral signal extractor detects `status_code`, `X-Token-Validation` header, and `session_state_change`. TP=1.0 was achieved in all prior experiments. If TP < 0.85, behavioral signal extraction is broken.

## Null Control

Structural signal std > 0 across all conditions (non-304 samples): ETag, Cache-Control, and UUID-based dynamic content should produce non-zero structural variation even on cache-disabled responses. Behavioral std > 0 on the 8 co-occurring conditions (non-304 only).

## Measurement Validity

### V3 FIX: Exclude 304 from pooled correlation
304 responses use a different structural composite construction (fixed 0.2 constant for dynamic_content_hash instead of variable sha256 hash, run_experiment.py:363-374) and occur exclusively for valid tokens (76 valid vs 0 expired in parent). This creates token-state-dependent structural construction. The fix: exclude all 304 responses from pooled Pearson correlation and from per-endpoint/per-cache correlations (C3, C4, C5, C6). Retain 304 samples in behavioral detection (C1) and structural variance (C2) checks only. Alternatively, use identical sha256(request_id) hash-based construction for 304 responses.

### V1 FIX VERIFIED (from parent)
ALL request_ids use uuid.uuid4() for all status codes. Entropy valid=3.723 vs expired=3.716, p=0.477 (no difference). Parent p=2.7e-34 eliminated.

### V2 FIX VERIFIED (from parent)
B-FLASK-ONLY has genuine token-state variation via /token endpoint, behavioral_std=3.5 > 0, r=0.026 defined (not NaN).

### V4: B-PARENT-CONFOUND-REPRODUCTION
Implement execution path in run_experiment.py that uses `secrets.token_hex(16)` for expired request_ids and `str(uuid.uuid4())` for valid request_ids. Run same n=480 protocol. Expected |r| >= 0.15.

### V5: C3/C4 one-sided decision rule
C3 tests 95% CI upper < 0.15 only (not both bounds). C4 tests TOST p_upper < 0.05 only (not two-sided). Under frozen one-sided rule, parent data would have C3 PASS (upper 0.0018 < 0.15) and C4 PASS (p_upper 8.88e-08 < 0.05).

### Additional validity requirements
- Testbed server produces genuine behavioral AND structural stochastic variation
- CDN simulation implements genuine cache behavior: ETag-SHA256, Cache-Control max-age/no-store, 304 handling via If-None-Match
- OAuth middleware uses real PyJWT RS256 validation — not hand-programmed lookup tables
- Dynamic content includes UUID timestamps, request IDs, user-dependent responses, SQLite WAL-mode
- Network latency jitter configurable (10-500ms) and measured
- Structural signal extraction uses ONLY: (a) ETag change (0/1), (b) Cache-Control change (0/1), (c) normalized Shannon entropy of UUID-based request_id, (d) SHA256(request_id)[:16] as int % 10000 / 10000
- Each endpoint has independent behavioral and structural signal extraction — no shared variables between signal domains
- n >= 480 paired samples from >= 3 endpoints x >= 2 cache modes x >= 2 auth states

## Decision Rule

C-FRESHNESS orthogonality at delta=0.15 is **CONFIRMED** if ALL of:

- **(C1)** Behavioral detection TP >= 0.85 across all endpoints (expired tokens correctly detected as drift)
- **(C2)** At least 2/3 endpoints have behavioral signal std > 0 AND at least 2/3 endpoints have non-304 structural signal std > 0
- **(C3)** 95% CI upper bound of pooled Pearson r (non-304 samples only) < 0.15 on production-like testbed
- **(C4)** TOST equivalence test p_upper < 0.05 at delta=0.15 (one-sided, non-304 samples only)
- **(C5)** Cache-mode heterogeneity check (non-304 samples): |r_cache_enabled - r_disabled| < 2 * SE (CDN effect on correlation within sampling noise)
- **(C6)** B-FLASK-ONLY baseline shows |r| < 0.15 (orthogonality persists without infrastructure)
- **(C7)** B-PARENT-CONFOUND-REPRODUCTION shows |r| >= 0.15 (negative control passes, confirming V1 was genuine)

C-FRESHNESS orthogonality is **REJECTED** if ANY condition fails.

**MEASUREMENT_INVALID** if infrastructure failure prevents data collection (endpoint unreachable, testbed construction fails, n < 240).

## Sample Size

n >= 480 paired samples from 3 endpoints x 2 cache modes x 2 auth states = 8 co-occurring conditions, minimum 60 samples per condition. This provides adequate power for delta=0.15 equivalence test (minimum detectable |r| ~ 0.09 at n=480).

## Testbed Infrastructure

Reuses parent EXP-GRAPH-35470449310 testbed_server.py (Flask 3.1.3, PyJWT RS256, SQLite WAL-mode, CDN simulation with ETag/Cache-Control/304, 3 endpoints) and flask_only_server.py (with V2 token validation fix) with two targeted code fixes:
1. `run_experiment.py`: Exclude 304 responses from pooled correlation (and from per-endpoint/per-cache correlation calculations). Alternatively, use identical sha256(request_id) hash-based structural composite construction for 304 responses.
2. `run_experiment.py`: Implement B-PARENT-CONFOUND-REPRODUCTION execution path (request_id via token_hex for expired, uuid4 for valid).

## Product Consequences

### If CONFIRMED
C-FRESHNESS advances from EXPERIMENTAL toward VALIDATED on production-like infrastructure. Parallel-channel architecture (separate behavioral and structural signal processing) is justified for product deployment. The orthogonality result extends from localhost mock to production-like server with CDN/OAuth/dynamic content, eliminating the critical gap for C-FRESHNESS product deployment. Product may proceed with dual-signal freshness detection.

### If REJECTED
C-FRESHNESS orthogonality fails on production-like infrastructure even with corrected measurement and excluded 304 coupling. Parallel-channel architecture is NOT justified. Product must pivot to fused classifiers or cache-independent structural signals. The localhost mock evidence is insufficient for production deployment.

## Expected Information Gain

Very high: this is the minimum cost experiment that directly resolves the two remaining measurement validity gaps (V3 coupling, V4 missing control) blocking a clean CONFIRMED or REJECTED verdict. The same production-like testbed infrastructure is reused with two small targeted code fixes. Either outcome changes a product decision. A clean MEASUREMENT_INVALID verdict is also informative and would direct further investigation.

## Inherited State from Parent Handoff

### Established
- V1 request_id entropy confound FIXED: all status codes use uuid.uuid4(), entropy valid=3.723 vs expired=3.716, p=0.477 (no difference). Parent p=2.7e-34 eliminated.
- V2 B-FLASK-ONLY degeneracy FIXED: flask_only_server.py implements genuine token validation (valid/expired via /token endpoint), behavioral_std=3.5 > 0, r=0.0260, TOST PASS at delta=0.15, CI [-0.064, 0.115]. Parent r=NaN eliminated.
- C-FRESHNESS orthogonality confirmed at delta=0.15 under localhost stochastic Flask mock across three independent experiments (all n=480, all audit PASS): deterministic Flask r=0.0335 (EXP-GRAPH-35330739886), stochastic Flask+SQLite+cache+jitter r=0.0463 (EXP-GRAPH-35353011131), HTTP conditional caching r=0.0022 (EXP-GRAPH-35389145821).
- C-FRESHNESS orthogonality confirmed at delta=0.15 on stochastic Flask+SQLite mock (EXP-PRODUCT-35445596342): pooled r=-0.0258, CI upper 0.064, TOST p_upper 5.6e-05. Second independent confirmation.
- B-FLASK-ONLY baseline confirms orthogonality persists WITHOUT CDN/OAuth/dynamic content infrastructure: r=0.0260, |r|=0.0260, CI upper 0.115 < 0.15, TOST PASS at delta=0.15, behavioral_std=3.5. Infrastructure is NOT required for orthogonality.
- Behavioral signals (token validation failure, session state change, auth boundary shift) validated: TP=1.0 across all co-occurring conditions on both localhost mock and production-like testbed.
- Production-like testbed infrastructure (Flask 3.1.3, PyJWT RS256, SQLite WAL, CDN simulation with ETag/Cache-Control/stale-while-revalidate, 3 endpoints) is functional and reusable.

### Rejected
- Stable public APIs (GitHub 403, JSONPlaceholder) as testbeds — zero behavioral and structural variance (EXP-GRAPH-35409927045, MEASUREMENT_INVALID).
- Structural signal hash(body)%10000 including error bodies produces valid orthogonality measurement — V1 confound: error body constant for expired tokens creates forced correlation (r=0.375 parent EXP-GRAPH-35445595108).
- Headers-only structural signal with different request_id generators per status code is independent of behavioral state — V1 confound: valid entropy 3.542 vs expired 3.233, p=2.7e-34 (EXP-GRAPH-35456070379). FIXED in parent.
- HTTP caching as common cause raising |r| above 0.15 — three independent experiments show orthogonality under HTTP caching (r=0.0022-0.046).
- n=240 sufficient for delta=0.15 equivalence — n>=480 required (CI width ~0.25 at n=240 vs ~0.18 at n=480).
- Frozen REJECTED outcome (|r|=0.1737, EXP-GRAPH-35456070379) falsifies orthogonality on production-like infrastructure — measurement-invalid due to V1/V2 (now fixed).
- 304 cache-hit structural composite construction is independent of behavioral state — V3 confound identified in parent (fixed 0.2 for 304 vs variable hash for non-304, 304 occurs only for valid tokens). FIX: exclude 304 from correlation.

### Unknown
- Whether the 304 cache-hit structural coupling (V3) explains the per-endpoint cache-enabled negative correlations (r=-0.275, -0.334) or if genuine infrastructure-modulated correlation exists.
- Whether B-PARENT-CONFOUND-REPRODUCTION would show |r|>=0.15 under identical conditions, confirming parent V1 entropy bifurcation was the sole cause of r=0.1737.
- Whether orthogonality at delta=0.15 holds on production-like infrastructure when 304 structural coupling is eliminated and B-PARENT baseline is executed.
- Whether per-cache heterogeneity (|r_enabled - r_disabled|=0.22 > 2*SE=0.18) is systematic or sampling noise; requires replication at n>=800.
- Whether orthogonality at delta=0.15 holds on actual distributed production infrastructure with real CDN hierarchies, OAuth/OIDC middleware, and concurrent client load.
- Whether CDN cache invalidation on session state change introduces correlation under distributed cache conditions.
- Whether headers-only structural signal (ETag + Cache-Control + request_id entropy + dynamic content hash) captures sufficient variation for production freshness detection.

### Do Not Assume
- C-FRESHNESS reaches VALIDATED or PRODUCT_CORE — status remains EXPERIMENTAL bounded to localhost stochastic mock.
- The pooled |r|=0.088 constitutes evidence that production-like infrastructure breaks orthogonality — measurement is invalid due to V3 coupling and V4 missing control; no causal inference warranted.
- The B-FLASK-ONLY result (r=0.026) transfers to production-like infrastructure — B-FLASK-ONLY lacks CDN simulation, OAuth middleware, and dynamic content.
- The per-endpoint cache-enabled negative correlations (r=-0.275, -0.334) represent genuine behavioral-structural coupling — may be artifacts of V3 304 structural construction coupling.
- Delta=0.10 is achievable at n=480 — CI width ~0.178 exceeds 2*delta=0.10; minimum detectable |r| ~0.09 at n=480.
- Production-like infrastructure features (CDN/OAuth/dynamic content) break orthogonality — untested due to measurement confounds; B-FLASK-ONLY baseline (no infrastructure, r=0.026) suggests infrastructure is NOT the causal factor.
- Testbed CDN simulation represents production CDN behavior — single-node Flask in-memory cache, not multi-CDN with real cache hierarchies.
- Frozen C3/C4 two-sided interpretation is scientifically required — frozen spec defines C3 as CI-upper-only and C4 as TOST-p-upper-only; producer deviation to two-sided caused spurious FAIL.
