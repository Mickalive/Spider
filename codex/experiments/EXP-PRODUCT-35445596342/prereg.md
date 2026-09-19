# EXP-PRODUCT-35445596342 Preregistration

## Experiment Identity

- **experiment_id**: EXP-PRODUCT-35445596342
- **lane**: product
- **claim_ids**: C-FRESHNESS
- **created_at**: 2026-09-19T13:23:17.363378+00:00
- **parent_handoff**: EXP-PRODUCT-35434772331 (sha256: 5d023480c998d3879bb77083f057708239d05b791485336f242a417096ae0ff0)

## Parent Handoff Carry-Forward

### Established (from parent)
1. Structural signal (HTTP fingerprint substrate) discriminates auth states on mock SPIDER kernel: discrimination 0.8333, replicating EXP-RUNTIME-33902315583 exactly (C1 passes)
2. Behavioral signal detects all three drift types with 100% accuracy in isolated conditions: TP=1.0 for permission_boundary, session_invalidation, token_refresh (C2 passes)
3. Structural noise does not cause behavioral false positives: FP=0.0 on 240 noise-only samples (C4 passes)
4. C-PRODUCT-ECON is REJECTED: 5+ consecutive PRODUCT experiments with zero real LLM calls, 5.42% thin margin, COLD 7.5x cheaper, analytical line exhausted
5. C-FRESHNESS orthogonality already confirmed by parent EXP-GRAPH-35353011131 under stochastic mock at delta=0.15 (r=0.046, CI upper 0.135, TOST p_upper=0.011)

### Rejected (from parent)
1. C-PRODUCT-ECON (token-based deduplication economics): REJECTED as not viable at current scale
2. Hypothesis that behavioral scoring weights produce differentiated scores: FALSIFIED by measurement (all three drift types score 0.5 due to weight collisions)

### Unknown (from parent)
1. Whether a redesigned behavioral_score with continuous differentiated scoring would produce sufficient variance for orthogonality testing on a stochastic server
2. Whether server state carry-over affects Phase 6 behavioral TP measurements in addition to Phase 4 co-occurring conditions
3. Whether the expired_token/invalid_token fingerprint collision generalizes to production endpoints
4. Whether C-FRESHNESS can advance to PRODUCT_ARCHITECTURE_IMPACT with the stochastic-mock orthogonality baseline without re-measurement in this specific product-lane experiment

### Do Not Assume (from parent)
1. Do not assume behavioral signal has zero variance in general — the zero variance is specific to this deterministic WSGI server with scoring weight collisions; parent stochastic mock achieved behavioral_std 0.14-0.43
2. Do not assume orthogonality is falsified — C3 failure is measurement invalidity (behavioral variance=0.0), not scientific evidence of signal coupling
3. Do not assume C-PRODUCT-ECON closure is based solely on this experiment — it is based on the full evidence chain across 5+ experiments
4. Do not assume C-FRESHNESS is validated or PRODUCT_CORE — it remains EXPERIMENTAL; orthogonality is confirmed only at delta=0.15 under stochastic mock on localhost, not production
5. Do not assume the structural signal (discrimination 0.8333) generalizes to production OAuth/OIDC, CDN, or non-deterministic endpoints — claim ceiling bounded to Flask 3.1.3 + PyJWT 2.13.0 HS256 localhost
6. Do not assume the behavioral TP=1.0 generalizes to co-occurring conditions — TP was measured in Phase 6 with isolated drift conditions, not co-occurring drift+noise where state carry-over occurs

## Scientific Question

Can a redesigned behavioral_score function with continuous differentiated scoring (weighted by drift severity, distinct signal combinations) produce sufficient behavioral variance for orthogonality testing when run on a stochastic Flask+SQLite mock server matching EXP-GRAPH-35353011131, with proper server state reset between conditions?

## Hypothesis

The three root causes of C3 measurement invalidity in EXP-PRODUCT-35434772331 — (a) deterministic WSGI server producing zero behavioral variance, (b) scoring weight collisions producing identical 0.5 scores, (c) server state carry-over contaminating co-occurring conditions — can be fixed by:

1. **Server replacement**: Replace deterministic wsgiref.simple_server with stochastic Flask+SQLite mock matching EXP-GRAPH-35353011131 (Flask 3.1.3 + SQLite WAL-mode DB for session/permission state + in-memory cache with TTL=0.5s + I/O jitter 10-100ms + mixed JWT algorithms HS256/RS256)

2. **Scoring redesign**: Redesign behavioral_score to produce continuous differentiated scores via severity-weighted drift-type-specific signal combinations. Each drift type maps to a distinct score range:
   - permission_boundary: role change + permission reduction signals → distinct range
   - session_invalidation: session validity + revocation signals → distinct range  
   - token_refresh: refresh status + new token signals → distinct range
   The key requirement: scores must be continuous (not binary) and non-overlapping across drift types under co-occurring noise.

3. **State reset**: set_drift(None) must fully reset all server state (current_role='admin', session_valid=True, drift_active=False, drift_type=None, noise_active=False, noise_type=None) before activating new drift, preventing contamination across conditions.

Under these fixes, behavioral_std > 0.05 in >=6 of 8 co-occurring conditions (matching EXP-GRAPH-35353011131 C2_variance), enabling valid TOST equivalence testing at delta=0.15.

## Falsifier

FALSIFIED if:
- (F1) C3 orthogonality still fails with behavioral_std=0.0 (measurement design still broken), OR
- (F2) C1 structural discrimination falls below 0.5 (new server breaks positive control), OR
- (F3) C2 behavioral TP falls below 0.85 (new scoring breaks drift detection), OR
- (F4) C4 noise FP exceeds 0.15 (new server introduces false positives)

MIXED if C1-C2-C4 pass but C3 fails with behavioral_std>0.0 (signals are correlated, not orthogonal).

## Baselines

### B-STRUCTURAL-SIGNAL
HTTP fingerprint substrate discrimination on mock SPIDER kernel. Validated at 0.8333 in EXP-RUNTIME-33902315583 and replicated in EXP-PRODUCT-35434772331 C1. Expected: full-vector discrimination > 0.5 on auth-state changes.

### B-BEHAVIORAL-VARIANCE
Behavioral signal variance under stochastic server from EXP-GRAPH-35353011131. Achieved behavioral_std 0.14-0.43 across 8 co-occurring conditions. Expected: >=6 of 8 co-occurring conditions with behavioral_std > 0.05.

### B-ORTHO-GRAPHII
Orthogonality confirmed by EXP-GRAPH-35353011131 under stochastic mock: r=0.046, CI upper 0.135 < delta=0.15, TOST p_upper=0.011. Expected: 95% CI upper bound on |r| < 0.15, TOST p_upper < 0.05 at delta=0.15.

## Controls

### Positive Control: PC-STRUCTURAL-DISCRIMINATION
Auth-state change detection using HTTP fingerprint substrate on stochastic Flask+SQLite server. Replicates EXP-RUNTIME-33902315583 positive control. Expected: full-vector discrimination > 0.5 on auth-state changes (valid_token vs no_auth vs expired_token vs invalid_token).

### Null Control: NC-NOISE-FP
Structural noise tolerance: optional field additions, timing jitter, response variation that do NOT represent auth drift. FP rate <= 0.15 on noise-only samples. Expected: FP <= 0.15 on structural noise samples.

### Variance Precondition: C2-VARIANCE
>=6 of 8 co-occurring conditions must have behavioral_std > 0.05 AND structural_std > 0.05. This precondition gates the orthogonality test: if behavioral variance is zero, TOST is undefined. Expected: 8/8 conditions with variance (matching EXP-GRAPH-35353011131).

## Measurement Validity

1. Stochastic Flask+SQLite mock server matching EXP-GRAPH-35353011131: Flask 3.1.3 + SQLite WAL-mode DB for session/permission state + in-memory cache with TTL=0.5s + I/O jitter 10-100ms + mixed JWT algorithms (HS256 read/write, RS256 admin)
2. Server state fully reset between conditions: set_drift(None) must clear current_role='admin', session_valid=True, drift_active=False, drift_type=None, noise_active=False, noise_type=None
3. Redesigned behavioral_score produces continuous differentiated scores: each drift type maps to a distinct score range via severity-weighted signal combinations (not simple additive weights that collide)
4. Orthogonality tested via TOST equivalence test with delta=0.15 (CI upper bound < 0.15 confirms shared variance < 2.25%)
5. N >= 480 paired samples (60 per condition x 8 co-occurring conditions) for orthogonality test
6. All measurements use localhost mock server, not production APIs
7. This experiment does NOT make real LLM calls

## Decision Rule

SURVIVES_CURRENT_TEST requires ALL of:
- (C1) HTTP fingerprint discrimination > 0.5 on auth-state changes (positive control)
- (C2) behavioral TP >= 0.85 on auth drift
- (C3) behavioral variance > 0.05 in >=6 of 8 co-occurring conditions AND structural+behavioral orthogonality confirmed at delta=0.15 (CI upper bound < 0.15, TOST p_upper < 0.05)
- (C4) FP <= 0.15 on structural noise

FALSIFIED if any of C1-C4 fail.
MIXED if C1-C2-C4 pass but C3 fails with behavioral_std>0.0 (signals correlated, not orthogonal).
MEASUREMENT_INVALID if C3 fails with behavioral_std=0.0 (design still broken).

## Product Consequence

### If SURVIVES
C-FRESHNESS orthogonality confirmed with differentiated behavioral scoring on stochastic server. C-FRESHNESS advances toward PRODUCT_CORE. The parallel-channel architecture (behavioral + structural as independent channels) is justified for production integration. Freshness guards become the next product gate.

### If FALSIFIED/MIXED
C-FRESHNESS remains EXPERIMENTAL. If behavioral_std remains 0.0, measurement design needs further iteration. If signals are correlated (MIXED), product architecture must pivot to fused classifiers instead of parallel channels.

## Estimated Cost

Zero new LLM calls. Reuses existing HTTP fingerprint substrate code and stochastic Flask+SQLite mock server pattern from EXP-GRAPH-35353011131. Estimated 400-500 lines Python for server + experiment script. 8 conditions x 60 samples = 480 paired HTTP cycles on localhost, ~15-20 minutes execution time. No API keys required.

## Expected Information Gain

HIGH: directly resolves the single blocker (C3 measurement invalidity) that prevents C-FRESHNESS from advancing toward PRODUCT_CORE. Either (a) the three-fix approach works and C-FRESHNESS advances (changing product architecture decision), or (b) it fails and the product must pivot to fused classifiers or further measurement iteration. Either outcome changes a product decision.

## Inherited State Not Modified

- C-PRODUCT-ECON remains REJECTED (closed in prior experiment chain)
- C-PARAM-INHERIT remains EXPERIMENTAL at committed-code synthetic single-slot ceiling
- C-FRESHNESS remains EXPERIMENTAL with orthogonality confirmed at delta=0.15 under stochastic mock in graph lane
- No product promotion authorized by this experiment
- No code changes to production without Director approval
