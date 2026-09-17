# EXP-GRAPH-35237975537 Preregistration: Session-Status Probing for Valid Orthogonality Test

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-35237975537
- **Lane**: graph
- **Parent**: EXP-GRAPH-35191029030 (handoff sha256: b86e49915b03105f3ad44bb3f700d3536eca78895038d8f6cb7c215f5e46363a)
- **Claim**: C-FRESHNESS - SPIDER can detect when inherited knowledge is stale
- **Date**: 2026-09-17

## 2. Background and Motivation

The parent experiment (EXP-GRAPH-35191029030) achieved directional improvement over its parent (EXP-GRAPH-35166507358):
- C1 PASS: TP=1.0 for all 8 co-occurring conditions (drift detection)
- C2 PASS: 99.2% signal observability (both behavioral > 0 AND structural > 0)
- C4 PASS: FP=0.0 on 120 noise-only samples (null control)
- **C3 FAIL**: Pooled |r|=0.0498 (directionally low, 12x lower than parent 0.593) but **MEASUREMENT_INVALID** because only 4/8 conditions had within-condition variance

Root cause: session_invalidation drift produces constant behavioral signal (std=0.0) because API endpoints (/api/read, /api/write, /api/admin) only check JWT token and permissions, not session validity. Session_state_changes is always 1, behavioral composite constant at 3.0 for all 120 session_invalidation samples. This makes the pooled r confounded by 120 constant values with zero variance.

The orthogonality hypothesis remains **untested, not falsified**. The minimum fix is to add a /session/status endpoint that actually checks session state, making session_invalidation produce behavioral variance.

## 3. Question

Can adding a /session/status endpoint probing to the behavioral composite produce within-condition variance (std>0) on all 8 co-occurring conditions, enabling a valid pooled Pearson r test of behavioral-structural orthogonality?

## 4. Hypothesis

When the behavioral composite includes a `session_status_check` signal derived from a `/session/status` endpoint (which returns 200 for valid sessions and 401 for invalid sessions), session_invalidation conditions gain behavioral variance because the endpoint actually checks session state. This produces std>0 on all 8 co-occurring conditions, enabling a valid pooled Pearson r test.

The parent's r=0.0498 is directionally low but confounded by 120 constant behavioral values; with proper variance on all conditions, the confirmatory pooled |r| test can determine whether behavioral and structural signals are genuinely orthogonal.

## 5. Design Changes from Parent

| Aspect | Parent (EXP-GRAPH-35191029030) | This Experiment |
|--------|---------------------------------|-----------------|
| Session validity check | None (endpoints check JWT + permissions only) | Added /session/status endpoint (200=valid, 401=invalid) |
| Behavioral composite formula | token_val_rate*2 + session_change*3 + auth_boundary*1 | token_val_rate*2 + session_change*3 + auth_boundary*1 + session_status_check*2 |
| session_status_check | Not present | (3 - status_code_of_/session/status) / 2 - ranges 0 to 1 |
| session_invalidation behavioral std | 0.0 (constant) | Expected > 0 (session status varies with TTL/jitter) |
| All other aspects | Same | Same |

The only code change is: (a) add /session/status endpoint to mock server, (b) add session_status_check to behavioral composite formula, (c) query /session/status as part of per-sample sequence.

## 6. Experimental Conditions

### 6.1 Drift Patterns (behavioral signals)

| Pattern | Mechanism | Expected Behavioral Signal |
|---------|-----------|---------------------------|
| permission_boundary | Set write=False, admin=False | HTTP 403 on /api/write, /api/admin; HTTP 200 on /api/read |
| session_invalidation | Clear server-side session store | /session/status returns 401 (session invalid) |

### 6.2 Noise Patterns (structural signals)

| Pattern | Mechanism | Expected Structural Signal |
|---------|-----------|---------------------------|
| optional_field_addition | Add 1-3 random fields to schema | Schema diff > 0 |
| description_change | Append " (updated)" to field descriptions | Schema diff > 0 |
| response_time_jitter | Add 50-150ms delay | No structural change (structural = 0) |
| field_type_normalization | Swap integer/boolean types | Schema diff > 0 |

### 6.3 Co-occurring Conditions (8 total)

1. permission_boundary + optional_field_addition
2. permission_boundary + description_change
3. permission_boundary + response_time_jitter
4. permission_boundary + field_type_normalization
5. session_invalidation + optional_field_addition
6. session_invalidation + description_change
7. session_invalidation + response_time_jitter
8. session_invalidation + field_type_normalization

### 6.4 Within-Condition Stochastic Variation

For each of 30 samples per condition:

**permission_boundary drift**:
- Random permission subset from: {read:T, write:F, admin:F}, {read:T, write:T, admin:F}, {read:T, write:F, admin:T}
- Excludes all-True baseline and all-False which blocks everything

**session_invalidation drift**:
- Session TTL randomized 5-15s (uniform)
- Token expiry jitter +/-1s (uniform)
- These create genuine session validity variation that /session/status detects

**Structural noise**:
- optional_field_addition: random 1-3 new fields
- description_change: all fields updated (deterministic given schema)
- field_type_normalization: all compatible fields swapped (deterministic given schema)
- response_time_jitter: random 50-150ms (uniform)

## 7. Measurement Protocol

### 7.1 Server Setup

Flask 3.x + PyJWT HS256 on localhost. Modifications from parent:
1. Add `/session/status` endpoint (authenticated GET, checks session store, returns 200 if valid, 401 if cleared)
2. Same `/schema` endpoint (unauthenticated GET, returns current schema)
3. Same `/api/read`, `/api/write`, `/api/admin` endpoints

### 7.2 Per-Sample Sequence

1. Get baseline schema from `/schema` (unauthenticated)
2. Apply drift pattern (permission change or session invalidation)
3. Apply noise pattern (schema modification)
4. For each of 3 probed endpoints (read, write, admin):
   - Send request with current token and session
   - Record HTTP status code (200/401/403)
5. Query `/session/status` (authenticated) to get session validity
6. Query `/schema` (unauthenticated) to get current structural state
7. Compute behavioral composite: `token_val_rate * 2 + session_change * 3 + auth_boundary * 1 + session_status_check * 2`
8. Compute structural composite: `max(schema_diff_magnitude, 1.0 - jaccard_similarity)` from baseline vs current /schema response

### 7.3 Signal Definitions

**Behavioral composite** (augmented from parent):
- token_val_rate = count(401 responses) / 3
- session_change = 1 if session invalid, 0 otherwise (from /session/status)
- auth_boundary = count(403 responses) / 3
- session_status_check = (3 - status_code_of_/session/status) / 2
  - 200 -> 0.0 (session valid)
  - 401 -> 1.0 (session invalid)
- composite = token_val_rate * 2 + session_change * 3 + auth_boundary * 1 + session_status_check * 2

**Structural composite** (same as parent, from unauthenticated /schema):
- baseline_schema = schema from /schema before drift/noise
- current_schema = schema from /schema after drift/noise
- jaccard = Jaccard index of (field_name, field_type) pairs
- schema_diff = weighted diff magnitude
- composite = max(schema_diff, 1.0 - jaccard)

## 8. Controls

### 8.1 Positive Control

**PC-SESSION-STATUS-VARIANCE**: session_invalidation conditions must produce behavioral composite with std>0. The /session/status endpoint detects session state, which varies with session TTL randomization and token expiry jitter.

### 8.2 Null Control

**NC-SCHEMA-NOISE-ONLY**: Schema noise applied WITHOUT drift should produce FP=0.0 on behavioral signals. Same as parent.

## 9. Decision Rules

| Criterion | ID | Threshold | Rationale |
|-----------|----|-----------|-----------|
| Drift detection | C1_drift_tp | Mean TP >= 0.85, all Wilson lower > 0.75 | Behavioral signals detect drift under co-occurring noise |
| Variance gate | C2_variance | >= 6/8 conditions have std>0 for BOTH signals | Minimum for valid pooled r test |
| Orthogonality | C3_orthogonality | Pearson |r| < 0.3 on pooled paired scores, perm p < 0.05 | Primary hypothesis test |
| Null control | C4_null_control | FP = 0.0 on noise-only | Behavioral signals do not fire on structural noise |

**Overall PASS**: ALL four criteria pass.
**Overall FAIL**: Any criterion fails.
**MEASUREMENT_INVALID**: Fewer than 6 of 8 co-occurring conditions have std>0 for both signals, or fewer than 240 paired samples available.

## 10. Sample Size

- 2 drift patterns x 4 noise patterns = 8 co-occurring conditions
- 30 samples per condition = 240 paired (behavioral, structural) scores
- Plus 8 noise-only conditions x 30 = 240 null control samples
- Total: ~480 request sequences
- Estimated runtime: ~10 minutes

## 11. Validity Threats

1. **Deterministic mock server**: All measurements on localhost Flask. Real APIs may have stochastic field availability, CDN caching, rate limiting. Claim ceiling bounded to deterministic mock.

2. **Limited drift patterns**: Only permission_boundary and session_invalidation tested. signing_key_rotation excluded (blocks all endpoints).

3. **Unauthenticated /schema and /session/status endpoints**: Synthetic constructs not present in real APIs in this form. Real-world probes may require different mechanisms.

4. **Stochastic variation range**: Permission subsets limited to 3 options, session TTL 5-15s. Wider variation might reveal different correlation structure.

5. **Composite score weighting**: Weights (2, 3, 1, 2) are designed to balance signal contributions but not optimized. Different weights might change the correlation.

6. **Pooled Pearson r**: Primary metric pools across all conditions. Per-condition correlation might differ. Exploratory per-condition analysis reported but not confirmatory.

## 12. Analysis Plan

### 12.1 Primary Analysis

1. Compute paired (behavioral_i, structural_i) scores for all samples across all co-occurring conditions
2. Verify variance gate: >= 6/8 conditions have std>0 for both signals
3. Compute Pearson r on the pooled 240 paired scores
4. Compute permutation p-value (1000 permutations of behavioral scores)

### 12.2 Secondary Analyses (exploratory)

1. Per-condition Pearson r (8 conditions x 30 samples each)
2. Per-drift-pattern Pearson r (permission_boundary vs session_invalidation)
3. Spearman rank correlation (robustness check)
4. Within-condition coefficient of variation for both signals

### 12.3 Validity Checks

1. Verify all co-occurring conditions have behavioral std > 0 and structural std > 0
2. Verify positive control: session_invalidation conditions have behavioral std > 0
3. Verify null control FP = 0.0
4. Report any conditions where one signal is constant (std = 0)

## 13. Consequences

### If C3_orthogonality PASSES (|r| < 0.3):

- C-FRESHNESS gains a validated second detection channel
- Product pipeline can integrate behavioral signals alongside structural signals
- Architecture: parallel independent channels for freshness detection
- Next step: test behavioral signals on real OAuth/OIDC middleware (Auth0/Okta/Keycloak)

### If C3_orthogonality FAILS (|r| >= 0.3):

- Behavioral and structural signals are confirmed non-orthogonal
- Product pipeline must use composite multi-signal classifiers
- Architecture: fused classifier for freshness detection
- Next step: design optimal classifier fusion

### If C2_variance FAILS (< 6/8 conditions with variance):

- The /session/status endpoint fix was insufficient for session_invalidation conditions
- Root cause analysis needed: does /session/status actually vary, or is session invalidation too deterministic?
- Possible pivot: restrict confirmatory test to permission_boundary conditions only (n=120, r=0.051 from parent)
