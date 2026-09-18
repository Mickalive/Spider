# EXP-GRAPH-35353011131 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-35353011131
- **Lane**: graph
- **Claim IDs**: C-FRESHNESS
- **Parent**: EXP-GRAPH-35330739886 (MIXED — CI upper 0.123 < delta=0.15, but fails at delta=0.10)
- **Parent Handoff SHA256**: 5cc7a1a746a9c46bce93dc664812eba7010bd4d4a224fc0861171087a2daee93

## 2. Question

Does behavioral-structural signal orthogonality (|r| < 0.15) persist when the mock API introduces genuine stochastic behavior via DB-backed state, cache TTL expiry, timing jitter, mixed JWT algorithms (HS256+RS256), and production-like middleware error modes — or does real-world stochasticity introduce correlation that breaks the parallel-channel product architecture?

## 3. Hypothesis

The parent EXP-GRAPH-35330739886 established near-zero pooled correlation (|r|=0.0335, CI upper 0.123 < delta=0.15) on DETERMINISTIC Flask 3.1.3 + PyJWT HS256 localhost with graded session_status_check. This experiment tests whether the same orthogonality holds when the server introduces four sources of genuine stochasticity absent from the parent:

1. **SQLite DB-backed state**: Session and permission state stored in SQLite with real file I/O, concurrent read/write timing, and WAL-mode locking — replacing the parent's deterministic in-memory dict.
2. **Cache TTL expiry**: In-memory cache with configurable TTL causes stale/fresh response alternation, introducing temporal variability in structural signals.
3. **Timing jitter**: Real I/O operations (DB reads, cache lookups, JWT signing with RS256) introduce genuine latency variation, replacing the parent's simulated jitter.
4. **Mixed JWT algorithms**: HS256 for read/write endpoints, RS256 for admin endpoints — simulating production middleware diversity with different cryptographic primitives.

**Expected mechanism of independence**: Behavioral signals (token validation success rate, session state changes, permission boundary shifts, session_status_check) measure access-control state. Structural signals (Jaccard similarity, schema diff magnitude from unauthenticated /schema) measure API contract shape. These are causally independent channels: the former depends on auth middleware state, the latter depends on schema generation logic. DB/cache/timing variation should not introduce correlation unless DB state simultaneously affects both auth validation and schema generation.

## 4. Falsifier

The hypothesis is falsified if ANY of:

1. **C1_drift_tp fails**: mean TP < 0.85 OR any Wilson lower CI < 0.75
2. **C2_variance fails**: < 6/8 co-occurring conditions with std > 0 for both behavioral and structural signals
3. **C3_equivalence fails**: 95% CI upper bound on |r| >= 0.15 (TOST at delta=0.15 does NOT pass AND CI upper bound >= 0.15)
4. **C4_null_control fails**: FP > 0.0 on noise-only samples

## 5. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-PARENT-DETERMINISTIC-N480 | Parent EXP-GRAPH-35330739886: n=480, |r|=0.0335, CI upper 0.123, TOST pass at delta=0.15 on deterministic Flask+HS256 | CI upper 0.123 < 0.15 |
| B-STOCHASTIC-FLASK-DB-CACHE | New server: Flask + SQLite + cache TTL + timing jitter + mixed JWT (HS256+RS256), same 8 conditions, N=60/condition | CI upper < 0.15 if orthogonality holds |

## 6. Controls

### 6.1 Positive Control (PC-TP-VARIANCE-STOCHASTIC)

Verify that the stochastic server still produces detectable behavioral drift:

- **Threshold**: mean TP >= 0.85 AND all Wilson lower CI > 0.75
- **Purpose**: Ensures stochasticity does not break the measurement pipeline's ability to detect drift
- **Expected**: All 8 conditions produce detectable behavioral signals

### 6.2 Null Control (NC-FP-STOCHASTIC)

Verify zero false positives on noise-only conditions:

- **Threshold**: FP = 0.0 across all noise-only samples
- **Purpose**: Ensures noise patterns (structural modification only) do not create spurious behavioral signals
- **Expected**: Behavioral composite = 0.0 for all noise-only samples

### 6.3 Inherited Controls (verified from parent raw_evidence)

- **C1_drift_tp**: Verified from parent EXP-GRAPH-35308806969 raw_evidence (mean TP=1.0, Wilson lower=0.940)
- **C2_variance**: Verified from parent (8/8 conditions with variance)
- **C4_null_control**: Verified from parent (FP=0.0 on 240 noise-only samples)

These inherited controls are verified against parent raw_evidence, not re-measured.

## 7. Measurement Validity Threats

1. **DB locking contention**: SQLite WAL-mode may serialize concurrent requests, reducing stochastic variation. Mitigation: use separate DB connections per request, WAL-mode with busy_timeout.
2. **Cache hit rate**: If cache TTL is too long, structural signals may be constant (no stale/fresh alternation). Mitigation: TTL = 0.5s with request间隔 ~1s ensures ~50% stale rate.
3. **RS256 key generation**: RSA key generation is deterministic for fixed seed. Mitigation: generate keys once at server start, use fixed seed.
4. **Timing jitter floor**: If jitter is too small, timing-based behavioral variation may be negligible. Mitigation: jitter range 10-100ms (realistic for local DB I/O).
5. **Sample size**: n=480 may still be underpowered for delta=0.10 (parent needs n~865). This experiment targets delta=0.15 only.
6. **Single server instance**: All conditions run on the same machine. Real production servers have different performance characteristics. Claim ceiling bounded to localhost.

## 8. Decision Rule

**PASS** if ALL of:
1. C1_drift_tp: mean TP >= 0.85 AND all Wilson lower CI > 0.75
2. C2_variance: >= 6/8 co-occurring conditions have std > 0 for both signals
3. C3_equivalence: 95% CI upper bound on |r| < 0.15 (via Fisher z-transform)
4. C4_null_control: FP = 0.0 on noise-only samples

**MIXED** if C1-C2-C4 PASS and C3 fails only due to underpowering (CI upper 0.10-0.15, |r| < 0.15 but CI upper >= 0.15).

**FAIL** if any criterion fails (non-power reason).

The CI-based decision rule uses two-sided 95% CI (z=1.96), which is more conservative than TOST (z=1.645 per side). This follows the parent's frozen decision rule methodology.

## 9. Sample Size and Power

- **N_SAMPLES**: 60 per condition (8 co-occurring + 4 noise-only = 12 conditions)
- **Total paired samples**: 480 (8 conditions x 60 samples)
- **SEED**: 42
- **Power analysis**: Fisher z-transform. At n=480, minimum detectable |r| for p<0.05 is ~0.0895. For true |r|=0.05, minimum n=1538. At observed |r| ~0.03 (parent), n=480 is sufficient for delta=0.15 but NOT for delta=0.10.
- **Target equivalence margin**: delta=0.15 (shared variance < 2.25%)

## 10. Conditions

### 10.1 Co-occurring Conditions (8)

| # | Drift Pattern | Noise Pattern | Description |
|---|---------------|---------------|-------------|
| 1 | permission_boundary | optional_field_addition | PB + new schema fields |
| 2 | permission_boundary | description_change | PB + field description updates |
| 3 | permission_boundary | response_time_jitter | PB + timing variation |
| 4 | permission_boundary | field_type_normalization | PB + type coercions |
| 5 | session_invalidation | optional_field_addition | SI + new schema fields |
| 6 | session_invalidation | description_change | SI + field description updates |
| 7 | session_invalidation | response_time_jitter | SI + timing variation |
| 8 | session_invalidation | field_type_normalization | SI + type coercions |

### 10.2 Noise-Only Conditions (4, null control)

| # | Noise Pattern | Description |
|---|---------------|-------------|
| 9 | optional_field_addition | Structural noise only, no drift |
| 10 | description_change | Structural noise only, no drift |
| 11 | response_time_jitter | Structural noise only, no drift |
| 12 | field_type_normalization | Structural noise only, no drift |

### 10.3 Stochastic Elements (NEW vs parent)

| Element | Parent (deterministic) | This Experiment (stochastic) |
|---------|----------------------|------------------------------|
| Session state | In-memory dict | SQLite DB with WAL-mode |
| Cache | None | In-memory cache with TTL=0.5s |
| Timing | Simulated jitter | Real I/O jitter (10-100ms) |
| JWT algorithm | HS256 only | HS256 (read/write) + RS256 (admin) |
| Error modes | Deterministic status codes | Stochastic from DB/cache failures |

## 11. Signal Computation

### 11.1 Behavioral Composite

```
composite = token_val_rate * 2 + session_change * 3 + auth_boundary * 1 + session_status_check * 2
```

Where:
- `token_val_rate` = token_validation_failures / 3.0 (range [0, 1])
- `session_change` = 1 if session invalid, 0 if valid (range {0, 1})
- `auth_boundary` = auth_boundary_shifts / 3.0 (range [0, 1])
- `session_status_check` = graded mapping: 401->1.0, 403->0.5, 500->0.75, 200->0.0

### 11.2 Structural Composite

```
structural = max(schema_diff_magnitude, 1.0 - jaccard_similarity)
```

Where:
- `jaccard_similarity` = Jaccard index of (field_name, field_type) pairs between baseline and current schema
- `schema_diff_magnitude` = weighted diff (field addition/removal = 1.0, type change = 0.5, description change = 0.3)

### 11.3 Correlation

- **Pooled Pearson r**: across all 480 paired (behavioral_i, structural_i) samples
- **95% CI**: Fisher z-transform: z = 0.5*ln((1+r)/(1-r)), SE = 1/sqrt(n-3), CI = tanh(z +/- 1.96*SE)
- **TOST**: Two one-sided tests at alpha=0.05 each, delta=0.15

## 12. Inherited Established/Rejected/Unknown/Do-Not-Assume

### Established (from parent handoff)

1. Behavioral-structural signal orthogonality confirmed at delta=0.15 on deterministic Flask 3.1.3 + PyJWT HS256 localhost: pooled r=0.0335, CI upper 0.123 < 0.15
2. TP/variance trade-off broken and verified: graded session_status_check achieves mean TP=1.0 with within-condition variance
3. Power analysis: for true |r|=0.05, minimum n=1538; at n=480, minimum detectable |r|=0.0895
4. TOST equivalence test is appropriate methodology for very-low-magnitude correlations
5. Per-condition heterogeneity: 1/8 conditions significant at alpha=0.05 (expected under null)

### Rejected (from parent handoff)

1. Permutation p<0.05 as sole confirmatory criterion for |r|<0.1 — underpowered at any practical n
2. Session validity randomization via 50/50 coin flip — breaks C1 TP
3. signing_key_rotation as co-occurring drift — blocks all endpoints
4. delta=0.10 achievable at n=480 with CI-based rule — needs n~865

### Unknown (from parent handoff)

1. Whether orthogonality holds on real APIs with stochastic DB/cache/CDN
2. Whether delta=0.10 is practically required or delta=0.15 sufficient
3. Whether single significant per-condition r=-0.314 replicates
4. Whether alternative JWT algorithms (RS256/ES256) preserve correlation structure
5. Whether wider stochastic variation changes pooled r estimate

### Do-Not-Assume (from parent handoff)

1. C-FRESHNESS is VALIDATED or reaches PRODUCT_CORE — status remains EXPERIMENTAL
2. Parallel channels are universally justified — justified ONLY if delta=0.15 acceptable
3. Orthogonality transfers to real APIs — this experiment tests a stochastic mock, not production
4. The pooled r=0.0335 is the true population correlation
5. Per-condition table errors affect C3 decision
6. n=480 is sufficient for any equivalence margin

## 13. Product Consequences

### Positive Outcome (CI upper < 0.15)

C-FRESHNESS orthogonality confirmed under stochastic API conditions. Product pipeline integrates behavioral + structural as independent parallel channels with quantified shared-variance ceiling < 2.25%. The parallel-channel architecture is justified for production deployment pending real-API validation.

### Negative Outcome (CI upper >= 0.20)

Behavioral and structural signals are not practically independent under stochastic conditions. Product architecture must pivot to fused classifiers. The cost of fused classifiers (additional model call, increased latency) must be measured against the cost of parallel channels with monitoring.

### Mixed Outcome (CI upper 0.15-0.20)

Decision depends on product risk tolerance. delta=0.15 acceptable -> parallel channels with monitoring and alerting for correlation drift. delta=0.10 required -> fused classifiers or larger n (~865 for delta=0.10).

## 14. Claim Ceiling

If orthogonality holds: bounded to Flask 3.1.3 + SQLite + in-memory cache + PyJWT HS256/RS256 on localhost, 8 co-occurring conditions, 480 paired samples, delta=0.15. NOT validated for: production databases, distributed caches, network latency, OAuth/OIDC, stochastic SPA frontends, or delta=0.10.

## 15. Code and Infrastructure

- **mock_server.py**: New Flask server with SQLite DB, cache TTL, mixed JWT algorithms (HS256+RS256), timing jitter
- **run_experiment.py**: Adapted from EXP-GRAPH-35308806969 with new MockServerManager for stochastic server
- **Dependencies**: Flask, PyJWT, requests, numpy, scipy (same as parent)
- **Execution**: localhost only, no external network calls, ~15-20 minutes
