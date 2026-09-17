# EXP-GRAPH-35191029030 Preregistration: Fixed Co-occurring Drift+Noise Orthogonality for C-FRESHNESS

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-35191029030
- **Lane**: graph
- **Parent**: EXP-GRAPH-35166507358 (handoff sha256: d3160d49adc24043ee606bd272b13622737d0efb926e5c2b62a718cf0d113841)
- **Claim**: C-FRESHNESS — SPIDER can detect when inherited knowledge is stale
- **Date**: 2026-09-17

## 2. Background and Motivation

The parent experiment (EXP-GRAPH-35166507358) established that session-level behavioral signals measured from real HTTP achieve:
- C1 PASS: TP=1.0 for all 5 auth-drift patterns (token_expiry, session_invalidation, permission_boundary, signing_key_rotation, cookie_clearance)
- C2 PASS: FP=0.0 for all 4 structural noise patterns (optional_field_addition, description_change, response_time_jitter, field_type_normalization)
- C3 PASS: AUC=1.0 for drift-vs-noise discrimination
- **C4 FAIL**: Pearson |r|=0.593 on co-occurring conditions (threshold: |r| < 0.3)
- C5 PASS: Positive control 30/30

The C4 failure was caused by a **measurement design flaw**, not evidence against signal orthogonality: 5 of 15 co-occurring conditions used signing_key_rotation as the drift pattern, which blocks ALL endpoints (HTTP 401 on every request). With no accessible endpoints, structural signals (Jaccard, schema_diff) could not be measured and were imputed to 0.0. The pooled correlation of 0.593 reflects deterministic pairing of imputed-zero structural values with non-zero behavioral values, not genuine coupling between the signal families.

The orthogonality hypothesis is **untested, not falsified**. The minimum next step is to fix the co-occurring measurement so both signals are non-trivially observable on the same conditions.

## 3. Question

Can a redesigned co-occurring drift+noise measurement — using drift patterns that do NOT uniformly block all endpoints and an independent unauthenticated structural probe — demonstrate Pearson |r| < 0.3 between behavioral and structural signal scores on genuinely co-occurring conditions?

## 4. Hypothesis

When structural observability is guaranteed via an unauthenticated `/schema` endpoint and drift patterns are chosen to preserve partial endpoint access, behavioral signals and structural signals measure genuinely independent dimensions. The Pearson correlation between paired per-sample scores will be below 0.3.

**Mechanism**: Behavioral signals (HTTP 403 rate, session invalidation) and structural signals (schema diff from /schema) operate on orthogonal server mechanisms (auth middleware vs response generation). With independent stochastic variation in both channels, the correlation should approach 0.

## 5. Design Changes from Parent

| Aspect | Parent (EXP-GRAPH-35166507358) | This Experiment |
|--------|-------------------------------|-----------------|
| Co-occurring drift patterns | signing_key_rotation, session_invalidation, permission_boundary | permission_boundary, session_invalidation ONLY |
| Structural probe | Response body from authenticated /api/read | Unauthenticated /schema endpoint |
| signing_key_rotation in co-occurring | YES (blocks all endpoints → structural=0.0) | EXCLUDED |
| Within-condition variation | Deterministic (constant per condition) | Stochastic (random permission subsets, noise magnitudes) |
| Correlation computation | Pooled condition means | Paired per-sample (behavioral_i, structural_i) |
| Number of co-occurring conditions | 15 (3 drift × 5 schema sizes) | 8 (2 drift × 4 noise patterns) |

## 6. Experimental Conditions

### 6.1 Drift Patterns (behavioral signals)

| Pattern | Mechanism | Expected Behavioral Signal |
|---------|-----------|---------------------------|
| permission_boundary | Set write=False, admin=False | HTTP 403 on /api/write, /api/admin; HTTP 200 on /api/read |
| session_invalidation | Clear server-side session store | Session lookup returns invalid; Set-Cookie cleared |

### 6.2 Noise Patterns (structural signals)

| Pattern | Mechanism | Expected Structural Signal |
|---------|-----------|---------------------------|
| optional_field_addition | Add 1-3 random fields to schema | Schema diff > 0 |
| description_change | Append " (updated)" to field descriptions | Schema diff > 0 |
| response_time_jitter | Add 50-150ms delay | No structural change (structural = 0) |
| field_type_normalization | Swap integer↔boolean types | Schema diff > 0 |

### 6.3 Co-occurring Conditions (8 total)

Each condition pairs one drift pattern with one noise pattern:
1. permission_boundary + optional_field_addition
2. permission_boundary + description_change
3. permission_boundary + response_time_jitter
4. permission_boundary + field_type_normalization
5. session_invalidation + optional_field_addition
6. session_invalidation + description_change
7. session_invalidation + response_time_jitter
8. session_invalidation + field_type_normalization

Note: only 8 co-occurring conditions (2 drift × 4 noise). The parent had 15 (3 drift × 5 schema sizes); we reduce to 2 drift × 4 noise = 8 conditions because:
- signing_key_rotation is excluded (parent confound)
- Schema sizes are not varied (structural signal from /schema is auth-independent, so schema size doesn't create observability confounds)

### 6.4 Within-Condition Stochastic Variation

For each of 30 samples per condition:

**permission_boundary drift**:
- Random permission subset from: {read:T, write:F, admin:F}, {read:T, write:T, admin:F}, {read:T, write:F, admin:T}
- (Excludes all-True baseline and all-False which blocks everything)

**session_invalidation drift**:
- Session TTL randomized 5-15s (uniform)
- Token expiry jitter ±1s (uniform)

**Structural noise**:
- optional_field_addition: random 1-3 new fields
- description_change: all fields updated (deterministic given schema)
- field_type_normalization: all compatible fields swapped (deterministic given schema)
- response_time_jitter: random 50-150ms (uniform)

## 7. Measurement Protocol

### 7.1 Server Setup

Flask 3.x + PyJWT HS256 on localhost (same as parent). Modifications:
1. Add `/schema` endpoint (unauthenticated GET, returns current schema as JSON)
2. No signing_key_rotation endpoint needed for co-occurring conditions

### 7.2 Per-Sample Sequence

1. Get baseline schema from `/schema` (unauthenticated)
2. Apply drift pattern (permission change or session invalidation)
3. Apply noise pattern (schema modification)
4. For each of 3 probed endpoints (read, write, admin):
   - Send request with current token and session
   - Record HTTP status code (200/401/403)
5. Query `/schema` (unauthenticated) to get current structural state
6. Compute behavioral composite: `token_val_rate * 2 + session_change * 3 + auth_boundary * 1`
7. Compute structural composite: `max(schema_diff_magnitude, 1.0 - jaccard_similarity)` from baseline vs current `/schema` response

### 7.3 Signal Definitions

**Behavioral composite** (same as parent):
- token_val_rate = count(401 responses) / 3
- session_change = 1 if session invalid, 0 otherwise
- auth_boundary = count(403 responses) / 3
- composite = token_val_rate * 2 + session_change * 3 + auth_boundary * 1

**Structural composite** (from unauthenticated /schema):
- baseline_schema = schema from /schema before drift/noise
- current_schema = schema from /schema after drift/noise
- jaccard = Jaccard index of (field_name, field_type) pairs
- schema_diff = weighted diff magnitude
- composite = max(schema_diff, 1.0 - jaccard)

## 8. Controls

### 8.1 Positive Control

**PC-PERMISSION-BOUNDARY-DETECTION**: permission_boundary drift on co-occurring conditions should produce TP >= 0.90. The /api/read endpoint remains accessible (HTTP 200), confirming partial endpoint preservation.

### 8.2 Null Control

**NC-SCHEMA-NOISE-ONLY**: Schema noise applied WITHOUT drift should produce FP = 0.0 (no behavioral signals fire).

### 8.3 Structural Observability Check

For each co-occurring condition, verify that:
- Behavioral composite > 0 for >= 25/30 samples (drift is detectable)
- Structural composite > 0 for >= 25/30 samples (structural signal is observable)
- If fewer than 80% of samples have both > 0, the condition is flagged as measurement-invalid

## 9. Decision Rules

| Criterion | ID | Threshold | Rationale |
|-----------|----|-----------|-----------|
| Drift detection | C1_drift_tp | Mean TP >= 0.85 across co-occurring conditions, all Wilson lower > 0.75 | Behavioral signals must detect drift even under co-occurring noise |
| Signal observability | C2_observability | >= 80% of co-occurring sample pairs have BOTH behavioral > 0 AND structural > 0 | Both signals must be non-trivially observable on same samples |
| Orthogonality | C3_orthogonality | Pearson |r| < 0.3 on ALL paired per-sample scores, permutation p < 0.05 | Primary hypothesis test |
| Null control | C4_null_control | FP = 0.0 on noise-only conditions | Behavioral signals don't fire on structural noise |

**Overall PASS**: ALL four criteria pass.
**Overall FAIL**: Any criterion fails.
**MEASUREMENT_INVALID**: Fewer than 6 of 8 co-occurring conditions have within-condition std > 0 for both signals, or fewer than 240 paired samples available.

## 10. Sample Size

- 2 drift patterns × 4 noise patterns = 8 co-occurring conditions
- 30 samples per condition = 240 paired (behavioral, structural) scores
- Plus 8 noise-only conditions × 30 = 240 null control samples
- Total: ~480 request sequences across all conditions
- Estimated runtime: ~10 minutes

## 11. Validity Threats

1. **Deterministic mock server**: All measurements on localhost Flask, not production APIs. Real APIs may have stochastic field availability, CDN caching, rate limiting that changes signal behavior. Claim ceiling bounded to deterministic mock.

2. **Limited drift patterns**: Only permission_boundary and session_invalidation tested. signing_key_rotation (which blocked all endpoints) is excluded. Generalization to other drift patterns untested.

3. **Unauthenticated /schema endpoint**: This is a synthetic construct not present in real APIs. Real-world structural probes may require authentication or be unavailable. The endpoint proves the measurement is possible, not that it's practical.

4. **Stochastic variation range**: Permission subsets limited to 3 options, noise magnitudes limited to 1-3 fields. Wider variation might reveal different correlation structure.

5. **Pooled Pearson r**: The primary metric pools across all conditions. Per-condition correlation might differ (e.g., permission_boundary conditions might show different r than session_invalidation conditions). Exploratory per-condition analysis will be reported but is not confirmatory.

6. **Composite score weighting**: Behavioral composite weights (2, 3, 1) are inherited from the parent and not optimized. Different weights might change the correlation. The weighting is frozen before outcomes are visible.

## 12. Analysis Plan

### 12.1 Primary Analysis

1. Compute paired (behavioral_i, structural_i) scores for all samples across all co-occurring conditions
2. Compute Pearson r on the pooled 240 paired scores
3. Compute permutation p-value (1000 permutations of behavioral scores)
4. Apply Bonferroni correction if needed (single primary test, no correction needed)

### 12.2 Secondary Analyses (exploratory)

1. Per-condition Pearson r (8 conditions × 30 samples each)
2. Per-drift-pattern Pearson r (permission_boundary pooled vs session_invalidation pooled)
3. Spearman rank correlation (robustness check)
4. Within-condition coefficient of variation for both signals

### 12.3 Validity Checks

1. Verify all co-occurring conditions have behavioral std > 0 and structural std > 0
2. Verify positive control TP >= 0.90
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
- Next step: design optimal classifier fusion (weighted combination, learned threshold)
