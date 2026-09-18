# EXP-GRAPH-35262262505 Preregistration: Graded Session-Status Intensity for TP-Preserving Variance

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-35262262505
- **Lane**: graph
- **Parent**: EXP-GRAPH-35237975537 (handoff sha256: cef7179d7126b4414b11ef418ccfb73108c779f29085c69692ba6bc562aac73e)
- **Claim**: C-FRESHNESS - SPIDER can detect when inherited knowledge is stale
- **Date**: 2026-09-18

## 2. Background and Motivation

The parent experiment (EXP-GRAPH-35237975537) identified a **fundamental TP/variance trade-off** in session_invalidation behavioral variance:

**The problem**: The 50/50 coin flip for session validity randomization creates within-condition variance (C2 PASS, 8/8 std>0) but dilutes TP to 0.729 (C1 FAIL) because valid sessions (coin flip = valid) produce behavioral=0 and are counted as drift misses. The audit (V1_C1_FAIL_BY_DESIGN_ARTIFACT) identifies this as a design flaw, not a measurement problem.

**Root cause analysis**:
- When coin flip = invalid (50%): session_change=1, session_status_code=401, behavioral_composite=5.0 -> TP detected
- When coin flip = valid (50%): session_change=0, session_status_code=200, behavioral_composite=0.0 -> false negative
- Mean TP = (0.467 + 0.467 + 0.433 + 0.467) / 4 = 0.459 for SI conditions, diluted by valid sessions
- Wilson lower CI 0.27-0.30 < 0.75 threshold

**The insight**: The variance mechanism (mixing valid/invalid sessions) directly conflicts with the detection mechanism (session_change=1 indicates drift). Any design that creates variance by labeling non-drift as drift will dilute TP.

**The proposed fix**: Instead of mixing valid/invalid sessions, keep session_change=1 for ALL session_invalidation samples (all sessions are invalid) and vary only the **session_status_check intensity** (the /session/status HTTP response code). By randomly choosing from {401, 403, 500} for the /session/status endpoint, session_status_check gains variance ({1.0, 0.5, 0.75}) while session_change stays at 1 for every sample. This preserves TP while creating within-condition variance.

**Prior evidence preserved from parent handoff (established)**:
- Permission_boundary behavioral signals achieve TP=1.0 (Wilson lower 0.886) on all 4 PB co-occurring conditions
- PB tolerates all 4 structural noise patterns with FP=0.0
- Pooled Pearson r=0.1387 (|r|<0.3, permutation p=0.031) survives C3 in isolation but is heterogeneous (PB r=0.051, SI r=0.189)
- Null control FP=0.0 on 120 noise-only samples replicates
- Six structural/schema-based signal families remain falsified for C-FRESHNESS frozen gate

**Rejected from parent**:
- Session validity randomization via 50/50 coin flip as a path to valid orthogonality test
- The specific preregistered TTL 5-15s + token expiry jitter +-1s stochastic variation model
- signing_key_rotation as a co-occurring drift pattern

## 3. Question

Can varying session_status_check intensity (HTTP status code {401, 403, 500}) while keeping session_change=1 for all session_invalidation samples achieve within-condition behavioral variance (std>0) without diluting TP below 0.85, breaking the TP/variance trade-off identified in EXP-GRAPH-35237975537?

## 4. Hypothesis

When the behavioral composite includes a session_status_check signal that varies across invalid states (401 -> 1.0, 403 -> 0.5, 500 -> 0.75) while session_change remains constant at 1 for all session_invalidation samples, behavioral composite gains within-condition variance (std > 0) without diluting TP. This is because:
1. session_change=1 fires for every SI sample (preserving detection)
2. session_status_check varies across {0.5, 0.75, 1.0} (creating variance)
3. No valid sessions are mixed into drift labels (no false negatives)

The resulting behavioral composite range for SI: [1*3 + 0.5*2, 1*3 + 1.0*2] = [4.0, 5.0] with intermediate values at 4.5 (for 403) and 4.75 (for 500), creating std > 0 while TP = 1.0.

## 5. Design Changes from Parent

| Aspect | Parent (EXP-GRAPH-35237975537) | This Experiment |
|--------|---------------------------------|-----------------|
| Session validity | 50/50 coin flip (valid/invalid) | ALL invalid (session_change=1 for every sample) |
| session_status_check variation | Binary: 200->0.0 or 401->1.0 | Graded: 401->1.0, 403->0.5, 500->0.75 |
| Session_status_check mapping | (3 - status_code)/2 (arithmetic nonsense) | Direct mapping: 401->1.0, 403->0.5, 500->0.75 |
| Behavioral composite range for SI | Bimodal: 0.0 (valid) or 5.0 (invalid) | Continuous: 4.0 to 5.0 |
| session_change for SI | 0 or 1 (coin flip) | Always 1 |
| TP for SI | 0.433-0.467 (diluted) | Expected 1.0 (no dilution) |
| Behavioral std for SI | ~2.49 (bimodal) | Expected ~0.4 (graded) |
| All other aspects | Same | Same |

## 6. Experimental Conditions

### 6.1 Drift Patterns (behavioral signals)

| Pattern | Mechanism | Expected Behavioral Signal |
|---------|-----------|---------------------------|
| permission_boundary | Set write=False, admin=False | HTTP 403 on /api/write, /api/admin; HTTP 200 on /api/read |
| session_invalidation | Clear server-side session store + vary /session/status code | /session/status returns {401, 403, or 500} randomly; session_change=1 always |

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

**permission_boundary drift** (same as parent):
- Random permission subset from: {read:T, write:F, admin:F}, {read:T, write:T, admin:F}, {read:T, write:F, admin:T}
- Excludes all-True baseline and all-False which blocks everything

**session_invalidation drift** (NEW - graded intensity):
- Session store cleared (session_change=1 for ALL samples)
- /session/status HTTP status code randomly chosen from {401, 403, 500} with equal probability (1/3 each)
- This creates graded session_status_check values: 401->1.0, 403->0.5, 500->0.75
- NO coin flip for session validity; all sessions are invalid

**Structural noise** (same as parent):
- optional_field_addition: random 1-3 new fields
- description_change: all fields updated (deterministic given schema)
- field_type_normalization: all compatible fields swapped (deterministic given schema)
- response_time_jitter: random 50-150ms (uniform)

## 7. Measurement Protocol

### 7.1 Server Setup

Flask 3.x + PyJWT HS256 on localhost. Modifications from parent:
1. Modify `/session/status` endpoint to return randomly chosen status code from {401, 403, 500} when session is invalid (instead of always 401)
2. Same `/schema` endpoint (unauthenticated GET, returns current schema)
3. Same `/api/read`, `/api/write`, `/api/admin` endpoints

### 7.2 Per-Sample Sequence

1. Get baseline schema from `/schema` (unauthenticated)
2. Apply drift pattern (permission change or session invalidation)
3. Apply noise pattern (schema modification)
4. For each of 3 probed endpoints (read, write, admin):
   - Send request with current token and session
   - Record HTTP status code (200/401/403)
5. Query `/session/status` (authenticated) to get session validity and status code
6. Query `/schema` (unauthenticated) to get current structural state
7. Compute behavioral composite: `token_val_rate * 2 + session_change * 3 + auth_boundary * 1 + session_status_check * 2`
8. Compute structural composite: `max(schema_diff_magnitude, 1.0 - jaccard_similarity)` from baseline vs current /schema response

### 7.3 Signal Definitions

**Behavioral composite** (augmented from parent):
- token_val_rate = count(401 responses) / 3
- session_change = 1 if session invalid, 0 otherwise (always 1 for SI conditions)
- auth_boundary = count(403 responses) / 3
- session_status_check = direct mapping of /session/status HTTP status code:
  - 200 -> 0.0 (session valid) [never used in SI conditions]
  - 401 -> 1.0 (session invalid, standard)
  - 403 -> 0.5 (session invalid, forbidden)
  - 500 -> 0.75 (session invalid, server error)
- composite = token_val_rate * 2 + session_change * 3 + auth_boundary * 1 + session_status_check * 2

**Structural composite** (same as parent, from unauthenticated /schema):
- baseline_schema = schema from /schema before drift/noise
- current_schema = schema from /schema after drift/noise
- jaccard = Jaccard index of (field_name, field_type) pairs
- schema_diff = weighted diff magnitude
- composite = max(schema_diff, 1.0 - jaccard)

### 7.4 Expected Behavioral Composite Values

For session_invalidation conditions (all samples have session_change=1):
- Minimum: token_val_rate*2 + 1*3 + auth_boundary*1 + 0.5*2 = token_val_rate*2 + 4.0 (when /session/status returns 403)
- Maximum: token_val_rate*2 + 1*3 + auth_boundary*1 + 1.0*2 = token_val_rate*2 + 5.0 (when /session/status returns 401)
- Intermediate: token_val_rate*2 + 1*3 + auth_boundary*1 + 0.75*2 = token_val_rate*2 + 4.5 (when /session/status returns 500)

Expected std > 0 because session_status_check varies across {0.5, 0.75, 1.0}.

## 8. Controls

### 8.1 Positive Control

**PC-STATUS-VARIANCE-WITH-DETECTION**: session_invalidation conditions must produce:
- Behavioral composite with std > 0 (from varying session_status_check across {401, 403, 500})
- session_change = 1 for ALL 30 samples (no false negatives)
- TP = 1.0 (all 30/30 detected as drift)

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
- Plus 4 noise-only conditions x 30 = 120 null control samples (aligned with parent execution)
- Total: ~360 request sequences
- Estimated runtime: ~10 minutes

## 11. Validity Threats

1. **Deterministic mock server**: All measurements on localhost Flask. Real APIs may have stochastic field availability, CDN caching, rate limiting. Claim ceiling bounded to deterministic mock.

2. **Limited drift patterns**: Only permission_boundary and session_invalidation tested. signing_key_rotation excluded (blocks all endpoints).

3. **Unauthenticated /schema and /session/status endpoints**: Synthetic constructs not present in real APIs in this form. Real-world probes may require different mechanisms.

4. **Graded status code mapping**: The mapping 401->1.0, 403->0.5, 500->0.75 is arbitrary. Different mappings might change the correlation structure. However, any mapping that creates variance while keeping session_change=1 is valid for the hypothesis.

5. **Composite score weighting**: Weights (2, 3, 1, 2) are inherited from parent, not optimized. Different weights might change the correlation.

6. **Pooled Pearson r**: Primary metric pools across all conditions. Per-condition correlation might differ. Exploratory per-condition analysis reported but not confirmatory.

7. **Session_status_check variance magnitude**: Expected std ~0.4 (from 3 values {0.5, 0.75, 1.0}) is smaller than parent's bimodal std ~2.49. This is intentional (graded vs bimodal) but may affect power.

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
5. Verify session_status_check distribution across {401, 403, 500} is approximately uniform (10 each per condition)

### 12.3 Validity Checks

1. Verify all co-occurring conditions have behavioral std > 0 and structural std > 0
2. Verify positive control: session_invalidation conditions have behavioral std > 0 AND TP = 1.0
3. Verify session_change = 1 for ALL session_invalidation samples (no coin flip)
4. Verify null control FP = 0.0
5. Report any conditions where one signal is constant (std = 0)

## 13. Consequences

### If C1-C4 ALL PASS (TP >= 0.85, variance > 0, |r| < 0.3, FP = 0.0):

- The TP/variance trade-off is broken
- C-FRESHNESS gains a validated second detection channel
- Product pipeline can integrate behavioral signals alongside structural signals
- Architecture: parallel independent channels for freshness detection
- Next step: test behavioral signals on real OAuth/OIDC middleware (Auth0/Okta/Keycloak)

### If C1 PASS but C3 FAIL (|r| >= 0.3):

- Behavioral and structural signals are confirmed non-orthogonal
- Product pipeline must use composite multi-signal classifiers
- Architecture: fused classifier for freshness detection
- Next step: design optimal classifier fusion

### If C1 FAIL again:

- The session_status_check intensity variation mechanism is insufficient
- Need fundamentally different approach: composite multi-signal classifiers from the start, or restrict confirmatory test to permission_boundary conditions only (n=120, r=0.051)
- Next step: pivot to PB-only confirmatory test with wider permission subsets (all 7 non-empty subsets, n>=60 per condition)

### If C2 FAILS (< 6/8 conditions with variance):

- The graded status code mapping does not produce sufficient behavioral variance
- Root cause analysis: is the mapping range (0.5 to 1.0) too narrow?
- Possible fix: widen range (e.g., 401->1.0, 403->0.2, 500->0.6) or add response body variation

## 14. Deviation from Parent Design

This experiment deviates from the parent's preregistered design in one material way:

**Parent**: 50/50 coin flip for session validity (valid sessions mixed into drift labels)
**This experiment**: ALL sessions invalid (session_change=1 for every SI sample), with graded session_status_check intensity via {401, 403, 500} status codes

This deviation is justified because:
1. The parent's coin-flip design was identified as the root cause of C1 FAIL (audit V1_C1_FAIL_BY_DESIGN_ARTIFACT)
2. The graded intensity approach is the audit's recommended fix (approach (a): "vary session_status_check intensity while keeping session_change=1 for all drift samples")
3. The parent's measurement was INVALID, not a scientific negative; this design tests the audit's recommended correction

The parent's other deviations (TTL 5-15s not implemented, noise-only n=120 not 240) are corrected or preserved:
- TTL model: replaced by graded status code (different mechanism, not TTL)
- Noise-only n=120: preserved aligned with parent execution (not 240 as originally spec'd)
