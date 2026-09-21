# EXP-PRODUCT-35456068953 Preregistration

## Experiment Identity

- **experiment_id**: EXP-PRODUCT-35456068953
- **lane**: product
- **claim_ids**: C-FRESHNESS
- **created_at**: 2026-09-19T19:00:45.000000+00:00
- **parent_handoff**: EXP-PRODUCT-35445596342 (sha256: 0db18ccaca0210c28dd4a231c489b96d0881106b68cabadec6f9cf0c43ed7760)

## Parent Handoff Carry-Forward

### Established (from parent)

1. Structural signal (HTTP fingerprint substrate) discriminates auth states on mock SPIDER kernel: discrimination 0.8333, replicating EXP-RUNTIME-33902315583 exactly (C1 passes)
2. Behavioral signal detects all three drift types with 100% accuracy in isolated conditions: TP=1.0 for permission_boundary, session_invalidation, token_refresh (C2 passes)
3. Behavioral signal detects drift in co-occurring conditions with structural noise: TP=1.0 on all 8 co-occurring conditions (2 drifts x 4 noises, 60 samples each) -- but note token_refresh excluded from co-occurring set
4. Structural noise does not cause behavioral false positives: FP=0.0 on 240 noise-only samples (C4 passes)
5. C-FRESHNESS orthogonality confirmed at delta=0.15 under stochastic Flask+SQLite mock with three independent replications: EXP-GRAPH-35353011131 (r=0.046, CI upper 0.135, TOST p_upper=0.011, n=480, audit PASS), EXP-GRAPH-35389145821 (r=0.0022, CI upper 0.0916, TOST p_upper=0.0006, n=480, audit PASS, HTTP caching exercised), EXP-PRODUCT-35445596342 (r=-0.0258, CI upper 0.064, TOST p_upper=5.6e-05, n=480, audit PASS, product-lane replication with redesigned behavioral_score)
6. Three root causes of C3 measurement invalidity resolved: (a) stochastic server produces behavioral variance (std 0.087-0.104 vs prior 0.0), (b) redesigned behavioral_score produces non-overlapping drift-type ranges (PB 0.32-0.545, SI 0.75-1.0), (c) server state reset prevents cross-condition contamination (CTL-STATE-RESET pass)
7. Parallel-channel architecture (behavioral + structural as independent channels) justified at localhost stochastic-mock ceiling only
8. C-PRODUCT-ECON is REJECTED: 5+ consecutive PRODUCT experiments with zero real LLM calls, 5.42% thin margin, COLD 7.5x cheaper, analytical line exhausted

### Rejected (from parent)

1. C-PRODUCT-ECON (token-based deduplication economics): REJECTED as not viable at current scale
2. Hypothesis that behavioral scoring weights produce differentiated scores (original additive weights): FALSIFIED by measurement in EXP-PRODUCT-35434772331 (all three drift types score 0.5 due to weight collisions)
3. Six structural signal families for C-FRESHNESS frozen gate: Jaccard (FP=1.0 under structural noise), TF-IDF (FP=1.0 inverted), response-time KS (TP=0.0 inverted), linear Fisher LDA ensemble (AUC=0.625), field-usage profiling (change_type invisible), schema comparison (noise tolerance fails due to unbounded optional field addition scaling)

### Unknown (from parent)

1. Whether the parallel-channel freshness guard orthogonality survives on a non-mock production-like substrate with real OAuth/OIDC middleware, CDN caching, network RTT, and database-backed sessions
2. Whether the expired_token/invalid_token fingerprint collision (identical 401 authentication_failed) generalizes to production endpoints with differentiated error details
3. Whether within-condition behavioral variance (0.087-0.104) and structural variance maintain on real network RTT and cache-freshness distributions beyond localhost jitter/TTL
4. **Whether token_refresh TP (1.0 isolated, deterministic std=0.0 by design) survives co-occurring structural noise -- only isolated token_refresh was TP-tested; the 8-condition orthogonality set covers permission_boundary and session_invalidation only**
5. Whether continuous differentiated scoring for token_refresh (currently fixed 0.65 std=0.0) needs redesign to achieve variance if included in future orthogonality sets
6. Whether 4 structural noise types (optional_field_addition, description_change, response_time_jitter, field_type_normalization) are sufficient coverage for production schema drift or additional noise patterns needed
7. Whether the parallel-channel claim ceiling needs re-measurement on a non-mock substrate before PRODUCT_CORE promotion

### Do Not Assume (from parent)

1. Do not assume C-FRESHNESS is VALIDATED or PRODUCT_CORE -- it remains EXPERIMENTAL; orthogonality is confirmed only at delta=0.15 under stochastic mock on localhost, not production
2. Do not assume the structural signal (discrimination 0.8333) generalizes to production OAuth/OIDC, CDN, or non-deterministic endpoints -- claim ceiling bounded to Flask 3.1.3 + PyJWT 2.14.0 HS256 localhost
3. Do not assume the behavioral TP=1.0 generalizes to co-occurring conditions including token_refresh -- TP was measured in Phase 6 with isolated drift conditions; co-occurring TP was measured only for permission_boundary and session_invalidation
4. Do not assume the pooled r values (-0.0258, 0.046, 0.0022) across three experiments indicate a fixed population correlation -- all are localhost mock measurements with sampling noise; the sign flips are mechanism-free
5. Do not assume C-PRODUCT-ECON closure is based solely on this experiment -- it is based on the full evidence chain across 5+ experiments
6. Do not assume the behavioral variance range (0.087-0.104) reflects production severity distributions -- permission_boundary samples only 3 discrete propagation levels, session_invalidation only 3 graded status codes
7. Do not assume that because three mock experiments confirm orthogonality, production endpoints will behave identically -- real OAuth/OIDC middleware, CDN, and network RTT may introduce correlated structural-behavioral variation not present in mock

## Scientific Question

Does token_refresh behavioral detection (TP) survive co-occurring structural noise at the same severity levels as permission_boundary and session_invalidation, when token_refresh drift is stochastic (randomized refresh success/failure) to produce behavioral variance?

## Hypothesis

Token_refresh behavioral detection (TP) will remain >= 0.85 under co-occurring structural noise because the behavioral signal for token_refresh (refresh token status, new token issued) is independent of structural noise patterns (optional_field_addition, description_change, response_time_jitter, field_type_normalization).

However, prior experiments show token_refresh drift produces deterministic behavioral_score (std=0.0) because refresh always succeeds. To test TP under noise, we must first introduce stochastic token_refresh drift (randomize refresh success/failure) to achieve behavioral variance > 0.05.

Under stochastic token_refresh, behavioral TP will survive noise because the signal (refresh success/failure) is orthogonal to structural noise.

## Falsifier

FALSIFIED if:
- (F1) token_refresh TP < 0.85 under co-occurring noise (drift detection fails), OR
- (F2) token_refresh behavioral_std < 0.05 under stochastic drift (variance insufficient for orthogonality test), OR
- (F3) structural discrimination falls below 0.5 (positive control fails), OR
- (F4) noise FP > 0.15 (false positives)

MIXED if TP >= 0.85 but behavioral_std < 0.05 (detection works but variance insufficient).

## Baselines

### B-TOKEN-REFRESH-ISOLATED
Token_refresh TP in isolation from prior experiments: TP=1.0, std=0.0 (deterministic). Expected: TP >= 0.85 under stochastic drift.

### B-NOISE-TP-PARENT
Permission_boundary and session_invalidation TP under co-occurring noise from EXP-PRODUCT-35445596342: TP=1.0 on all 8 co-occurring conditions. Expected: TP >= 0.85 for token_refresh under same noise conditions.

## Controls

### Positive Control: PC-STRUCTURAL-DISCRIMINATION
HTTP fingerprint substrate discrimination on stochastic Flask+SQLite server (reused from EXP-PRODUCT-35445596342). Expected: full-vector discrimination > 0.5 on auth-state changes.

### Null Control: NC-NOISE-FP
Structural noise tolerance: optional field additions, timing jitter, response variation that do NOT represent auth drift. FP rate <= 0.15 on noise-only samples. Expected: FP <= 0.15 on structural noise samples.

### Variance Precondition: C2-VARIANCE
Token_refresh behavioral_std must be > 0.05 under stochastic drift to enable orthogonality testing. Expected: behavioral_std > 0.05.

## Measurement Validity

1. Stochastic Flask+SQLite mock server matching EXP-PRODUCT-35445596342 (Flask 3.1.3 + SQLite WAL-mode DB + in-memory cache TTL=0.5s + jitter 10-100ms + mixed JWT algorithms)
2. Token_refresh drift randomization: refresh success/failure randomized with probability p_refresh_success (e.g., 0.7) to produce behavioral variance
3. Server state fully reset between conditions (set_drift(None) clears all state)
4. Behavioral_score for token_refresh must be continuous (not fixed 0.65) to reflect refresh success/failure variance
5. Orthogonality tested via TOST equivalence test with delta=0.15 (CI upper bound < 0.15)
6. N >= 480 paired samples (60 per condition x 8 co-occurring conditions) for token_refresh TP and orthogonality
7. All measurements use localhost mock server, not production APIs
8. This experiment does NOT make real LLM calls

## Decision Rule

SURVIVES_CURRENT_TEST requires ALL of:
- (C1) structural discrimination > 0.5 (positive control)
- (C2) token_refresh TP >= 0.85 under co-occurring noise
- (C3) token_refresh behavioral_std > 0.05 under stochastic drift
- (C4) FP <= 0.15 on noise-only samples

FALSIFIED if any condition fails.
MIXED if C1-C2-C4 pass but C3 fails (variance insufficient).

## Product Consequence

### If SURVIVES
Token_refresh detection robust to noise, strengthening C-FRESHNESS claim ceiling. Token_refresh can be included in orthogonality sets, expanding parallel-channel architecture coverage. The three untested drift types become two (token_refresh added, only token_refresh TP-under-noise remains unknown from original 3 drift types).

### If FALSIFIED
Token_refresh detection fragile under noise, requiring either separate handling or fused classifier. C-FRESHNESS claim ceiling remains bounded to permission_boundary and session_invalidation only. Product must decide whether to redesign token_refresh behavioral_score or exclude token_refresh from parallel-channel architecture.

## Estimated Cost

Zero new LLM calls. Reuses existing stochastic mock server with modifications to token_refresh drift randomization (~50 lines Python). 8 conditions x 60 samples = 480 paired HTTP cycles on localhost, ~15-20 minutes. No API keys required.

## Expected Information Gain

HIGH: directly tests whether token_refresh detection (the only untested drift type under co-occurring noise) survives noise, changing C-FRESHNESS claim completeness. Either outcome changes product architecture decision regarding token_refresh inclusion in parallel-channel freshness guards.

## Inherited State Not Modified

- C-PRODUCT-ECON remains REJECTED (closed in prior experiment chain)
- C-PARAM-INHERIT remains EXPERIMENTAL at committed-code synthetic single-slot ceiling
- C-FRESHNESS remains EXPERIMENTAL with orthogonality confirmed at delta=0.15 under stochastic mock in graph lane
- No product promotion authorized by this experiment
- No code changes to production without Director approval
