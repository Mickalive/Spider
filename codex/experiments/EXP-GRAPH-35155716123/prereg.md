# EXP-GRAPH-35155716123 Preregistration

## Experiment Identity

- **Experiment ID**: EXP-GRAPH-35155716123
- **Lane**: graph
- **Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)
- **Parent**: EXP-GRAPH-35154724244 (direct schema comparison, FALSIFIED-IN-SETTING)
- **Parent Handoff SHA256**: 07667213ff9a290be1a2c0ff28cb307b04ab22d16f6cac2f3abbf6f0bc396a1b

## 1. Research Question

Do session-level behavioral signals (token validation failure detection, cookie state inspection, authentication boundary probing) provide drift-vs-noise discrimination on a fundamentally different dimension from all six tested structural/schema-based signal families, thereby evading the magnitude confound?

## 2. Hypothesis

Session-level behavioral signals detect auth/session state drift (token expiry, session invalidation, permission boundary changes) with TP >= 0.90 and FP <= 0.15, while structural noise (field additions, description changes) that does not affect auth state produces FP <= 0.15 on behavioral signals. Behavioral signals are orthogonal to the best structural signal (Pearson r < 0.3) and achieve AUC > 0.80, demonstrating a complementary detection dimension for C-FRESHNESS.

## 3. Inherited State (from parent handoff)

### Established
- Six structural/schema-based signal families tested and all falsified for C-FRESHNESS frozen gate in deterministic mock: Jaccard, TF-IDF, response-time KS, linear Fisher LDA ensemble, field-usage profiling, direct schema comparison
- Schema diff is orthogonal to Jaccard structural similarity (Pearson r=-0.590)
- The magnitude confound is structural: optional_field_addition noise scales diff magnitude linearly with schema size, dominating subtle drift at all sizes
- C4 type-aware validation failure is measurement-invalid (mock conformance tautology), not evidence against type-aware detection

### Rejected
- Direct schema comparison as standalone drift-vs-noise discriminator
- Any single structural/schema-based signal family providing complete C-FRESHNESS discrimination
- Linear Fisher LDA ensemble of structural signals rescuing individual failures (AUC=0.625)

### Unknown
- Whether session-level behavioral signals provide drift-vs-noise discrimination on a fundamentally different dimension
- Whether composite multi-signal classifiers achieve discrimination none achieve individually
- Whether real APIs with stochastic behavior preserve any discrimination gaps measured in deterministic mock

### Do Not Assume
- C-FRESHNESS is globally closed or rejected (six bounded families falsified in specific settings)
- Session-level behavioral signals will succeed (orthogonal by dimension but actual discrimination untested)
- Deterministic mock results transfer to real APIs

## 4. Experimental Design

### 4.1 Mock API Server

Build a Flask API server with:

- **JWT token endpoint**: Issues real JWT tokens (PyJWT HS256) with configurable expiry, claims (user_id, role, permissions), and signing key
- **Session cookie endpoint**: Uses real Flask session mechanism with server-side session store
- **Protected resource endpoints**: Return structured JSON responses with configurable fields
- **Auth middleware**: Validates tokens/cookies on protected endpoints, returns 401/403 for invalid/expired/insufficient credentials

The server runs on localhost with deterministic responses (no stochastic variation within conditions).

### 4.2 Drift Patterns (auth state changes)

Five drift patterns that change ONLY auth state while structural properties remain constant:

| ID | Drift Pattern | Description | Expected Behavioral Signal |
|----|--------------|-------------|---------------------------|
| D1 | token_expiry | Server-side token signing key rotation makes old tokens invalid | Token validation failure rate jumps from 0% to 100% |
| D2 | session_invalidation | Server-side session store cleared, all session cookies become invalid | Session cookie validation failure rate jumps from 0% to 100% |
| D3 | permission_boundary | User role changed from admin to read-only, write endpoints return 403 | Permission boundary probing detects new 403 responses |
| D4 | signing_key_rotation | Server rotates HMAC signing key, old tokens fail validation | Token validation failure rate jumps from 0% to 100% |
| D5 | cookie_clearance | Server clears session cookie on response (Set-Cookie: session=; Max-Age=0) | Cookie state inspection detects missing session cookie |

### 4.3 Noise Patterns (structural changes without auth impact)

Four noise patterns that change ONLY structural properties while auth state remains constant:

| ID | Noise Pattern | Description | Expected Behavioral Signal |
|----|--------------|-------------|---------------------------|
| N1 | optional_field_addition | Add 10% of schema size as new optional fields to response | No behavioral signal change (fields not auth-related) |
| N2 | description_change | Modify field descriptions in OpenAPI-style metadata | No behavioral signal change |
| N3 | response_time_jitter | Add 50-200ms random delay to responses | No behavioral signal change |
| N4 | field_type_normalization | Change field value representations (e.g., string timestamps to ISO format) | No behavioral signal change |

### 4.4 Schema Sizes

Test at 5 schema sizes: n=10, 20, 30, 40, 50 fields per response. This matches the parent experiment design and enables testing whether behavioral signals are affected by the magnitude confound.

### 4.5 Conditions

Total: 9 patterns (5 drift + 4 noise) x 5 schema sizes = 45 conditions.
Each condition: 30 identical request sequences = 30 samples.
Total samples: 45 x 30 = 1,350.

### 4.6 Behavioral Signal Features

Compute three behavioral signal features per request sequence:

1. **token_validation_rate**: Fraction of requests where token validation fails (0.0 = all valid, 1.0 = all invalid)
2. **session_state_change**: Binary indicator of session cookie state change (0 = no change, 1 = changed)
3. **auth_boundary_shift**: Count of new 403 responses from permission-probing requests

Composite behavioral signal: weighted combination of the three features (weights to be determined by the signal's ability to discriminate drift from noise).

### 4.7 Structural Signal Features (for orthogonality comparison)

Compute two structural signal features per condition (matching parent experiments):

1. **jaccard_similarity**: Jaccard index of response field sets between baseline and current
2. **schema_diff_magnitude**: Weighted diff magnitude between baseline and current schema

## 5. Controls

### 5.1 Positive Control

Server rotates signing key (D4). Old tokens become cryptographically invalid. Behavioral token-validation signal MUST detect this. If the positive control fails, the behavioral signal implementation is broken.

### 5.2 Null Control

Apply noise pattern N1 (optional_field_addition) at schema size n=10. Behavioral signals MUST NOT detect this as auth drift. If the null control fires, behavioral signals are confounded with structural signals.

### 5.3 Baselines

- **B-STRUCTURAL-JACCARD**: Jaccard structural similarity from parent experiments (FP=1.0 under structural noise)
- **B-STRUCTURAL-SCHEMA-DIFF**: Schema diff magnitude from parent experiments (r=-0.59 orthogonal to Jaccard)
- **B-STRUCTURAL-ENSEMBLE**: Linear Fisher LDA ensemble from parent experiments (AUC=0.625)
- **B-RANDOM**: Random classifier (expected AUC=0.50)

## 6. Decision Rule

ALL of C1-C5 must pass for behavioral signals to survive the C-FRESHNESS gate:

- **C1 (drift detection)**: TP rate >= 0.90 across all 5 drift patterns (D1-D5). TP = behavioral signal fires when drift is present.
- **C2 (noise tolerance)**: FP rate <= 0.15 across all 4 noise patterns (N1-N4). FP = behavioral signal fires when only structural noise is present.
- **C3 (discrimination)**: Behavioral signal AUC >= 0.80 on drift vs no-change discrimination.
- **C4 (orthogonality)**: Pearson correlation between behavioral composite signal and best structural signal < 0.3 across all 45 conditions.
- **C5 (positive control)**: Signing-key-rotation (D4) produces behavioral signal change > 3x null-control standard deviation.

## 7. Analysis Plan

### 7.1 Primary Analysis

For each drift pattern Di and noise pattern Nj at each schema size s:

1. Compute behavioral signal features for all 30 samples
2. Compute TP rate for drift patterns (fraction of samples where behavioral signal fires)
3. Compute FP rate for noise patterns (fraction of samples where behavioral signal fires)
4. Compute AUC for drift vs no-change discrimination
5. Compute Pearson r between behavioral composite and best structural signal

### 7.2 Control Evaluation

1. Verify positive control: D4 behavioral signal change > 3x null standard deviation
2. Verify null control: N1 behavioral signal does not fire
3. Compute baseline AUCs for structural signals on same data
4. Compare behavioral AUC to structural baselines

### 7.3 Validity Checks

1. Verify all JWT tokens are cryptographically valid (not simulated)
2. Verify session cookies use real Flask session mechanism
3. Verify drift patterns change ONLY auth state (no structural variation)
4. Verify noise patterns change ONLY structural properties (no auth variation)
5. Verify deterministic computation (zero within-condition variance)

## 8. Consequences

### If C1-C5 all pass (behavioral signals survive):
- New detection dimension for C-FRESHNESS established
- Product architecture can integrate behavioral signals as complementary to structural signals
- Next experiment: test composite multi-signal classifier (behavioral + structural) for complete C-FRESHNESS discrimination
- Claim status: C-FRESHNESS advances from HYPOTHESIS toward EXPERIMENTAL

### If C1 or C2 fails (behavioral signals falsified):
- Seven signal families tested, all fail C-FRESHNESS in deterministic mock
- C-FRESHNESS domain may require fundamentally different experimental designs:
  - Real API deployments with DB/cache/CDN stochasticity
  - Production client traffic patterns
  - Stochastic field availability
  - Composite multi-signal classifiers on real data
- Claim status: C-FRESHNESS remains HYPOTHESIS with narrowed search space

### If C3-C5 fail but C1-C2 pass (behavioral signals work but confounded):
- Behavioral signals detect drift but are correlated with structural signals
- Composite classifier may still provide value through ensemble effects
- Next experiment: test whether behavioral + structural ensemble exceeds individual signal performance
- Claim status: C-FRESHNESS remains HYPOTHESIS with partial evidence

## 9. Representation Loss

- Mock API server is deterministic; real APIs have stochastic behavior (CDN caching, load balancing, rate limiting)
- JWT tokens use HS256; real deployments may use RS256/ES256 with different validation behavior
- Session cookies use server-side store; real deployments may use JWT-based sessions
- Drift patterns are clean (only auth changes); real drift often co-occurs with structural changes
- All conditions are synthetic; no evidence about production API behavior
- Behavioral signals are computed from HTTP response status codes and headers; real behavioral signals may include timing, retry patterns, and user-agent detection

## 10. Scope Limitations

- Claim ceiling bounded to: Flask 3.x + PyJWT 2.x HS256 on localhost, 5 drift patterns, 4 noise patterns, 5 schema sizes, deterministic computation
- Does NOT extend to: production OAuth/OIDC (Auth0/Okta/Keycloak), CDN/caching, load-balancer, rate-limit, stochastic field availability, real client traffic, or non-deterministic API behavior
- Does NOT test: composite multi-signal classifiers, real-world drift co-occurrence, or production deployment patterns
