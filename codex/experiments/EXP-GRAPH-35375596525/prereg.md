# EXP-GRAPH-35375596525 — Preregistration

## 1. Title

Behavioral-Structural Signal Orthogonality Under HTTP Caching Semantics

## 2. Authors / Owner

Graph Lane — SPIDER Research 2.0

## 3. Version

1.0 — 2026-09-18

## 4. Claim

**C-FRESHNESS** (status: EXPERIMENTAL): SPIDER can detect when inherited knowledge is stale.

Sub-claim under test: Behavioral and structural detection signals are practically independent (|r| < 0.15, shared variance < 2.25%) when the API server includes HTTP-level caching semantics (Cache-Control, ETag, If-None-Match, 304 Not Modified).

## 5. Background

The parent experiment EXP-GRAPH-35353011131 confirmed orthogonality at delta=0.15 on a stochastic Flask server with:
- SQLite DB-backed sessions
- In-memory cache with TTL-based expiry
- Response timing jitter from real I/O
- Mixed JWT algorithms (HS256 + RS256)

Result: pooled r=0.0463, CI upper 0.135 < 0.15, TOST p_upper=0.011 at delta=0.15. All four frozen decision conditions (C1-C4) passed.

The parent's carry_forward identified HTTP caching as the single most pervasive production-API feature absent from the stochastic mock. This experiment adds HTTP-level caching semantics to the same stochastic infrastructure.

## 6. Hypothesis

**H0**: HTTP caching semantics do NOT introduce correlation between behavioral and structural signals. |r| remains < 0.15 under Cache-Control, ETag, and conditional request conditions.

**Mechanism**: Behavioral signals (token validation, session state, auth boundary) are computed from auth middleware BEFORE cache lookup. Structural signals (schema shape from /schema) are determined by API contract, not cache state. HTTP caching affects response delivery (304 vs 200, timing) but not the causal content of either signal channel.

## 7. State Representation

### 7.1 Behavioral Signal (unchanged from parent)

Composite of four real HTTP request/response derived features:
- `token_val_rate` (weight 2): rate of token validation successes/failures
- `session_change` (weight 3): binary session state change detection
- `auth_boundary` (weight 1): auth boundary shift detection
- `session_status_check` (weight 2): graded status check (401→1.0, 403→0.5, 500→0.75)

### 7.2 Structural Signal (unchanged from parent)

Composite computed from unauthenticated `/schema` endpoint:
- Jaccard similarity of schema field sets
- Schema diff magnitude
- structural = max(schema_diff_magnitude, 1.0 - jaccard_similarity)

### 7.3 New: HTTP Caching Layer

Two caching modes tested:
- **Enabled**: Cache-Control: max-age=5; ETag generated from response body SHA-256; If-None-Match conditional requests return 304 Not Modified
- **Disabled**: Cache-Control: no-store on all responses; no ETag; no conditional requests

## 8. Action Representation

Same as parent: real HTTP request/response cycles against a Flask mock server. Actions include:
- GET /resource/{id} — normal resource access
- GET /schema — unauthenticated schema endpoint
- POST /auth/validate — token validation
- POST /session/check — session state check
- Drift patterns applied as server-side state mutations between sample groups

## 9. Drift Patterns

| Pattern | Description | Effect |
|---------|-------------|--------|
| `permission_boundary` | Admin permission granted/revoked | Auth boundary shifts; session_status_check changes |
| `session_invalidation` | Active session terminated server-side | Session state changes; token validation fails |

## 10. Noise Patterns

Same as parent (structural signal only):
- `optional_field_addition` — extra fields added to schema response
- `description_change` — field descriptions modified
- `response_time_jitter` — artificial response delay variation
- `field_type_normalization` — field types coerced to standard names

## 11. Co-occurring Conditions

4 conditions (2 drift × 2 caching mode):

| ID | Drift | Caching |
|----|-------|---------|
| `drift_perm_boundary+cache_enabled` | permission_boundary | Cache-Control + ETag |
| `drift_perm_boundary+cache_disabled` | permission_boundary | no-store |
| `drift_session_inval+cache_enabled` | session_invalidation | Cache-Control + ETag |
| `drift_session_inval+cache_disabled` | session_invalidation | no-store |

## 12. Sample Size

- N_SAMPLES = 60 per condition
- 4 co-occurring conditions × 60 = **240 paired samples**
- SEED = 42

Power analysis: at n=240, minimum detectable |r| = 0.129 (Fisher z). This is powered for delta=0.15 equivalence testing (observed |r| < 0.129 would have CI upper < 0.15).

## 13. Decision Rule

### 13.1 C1 — Drift True Positive

Mean TP >= 0.85 AND all per-condition Wilson lower CI > 0.75.

TP is computed per condition as the fraction of samples where the behavioral composite correctly detects the applied drift.

### 13.2 C2 — Signal Variance

>= 4/4 co-occurring conditions have std > 0 for BOTH behavioral and structural signals.

### 13.3 C3 — Equivalence

95% CI upper bound on pooled |r| < 0.15 via Fisher z-transform (TOST-equivalent).

Procedure:
1. Compute pooled Pearson r across all 240 paired samples
2. Apply Fisher z-transform: z = arctanh(r)
3. SE = 1/sqrt(n-3) = 1/sqrt(237)
4. CI on z: z ± 1.96 * SE
5. Back-transform to r: tanh(z ± 1.96 * SE)
6. Test: CI_upper < 0.15

### 13.4 C4 — Null Control

FP = 0.0 on noise-only samples.

Noise-only samples have structural noise applied but NO behavioral drift. Behavioral composite should remain 0.0.

### 13.5 Verdict

- **PASS**: C1 AND C2 AND C3 AND C4 all pass → orthogonality confirmed under HTTP caching
- **MIXED**: C1-C2-C4 pass, C3 fails with CI upper in [0.10, 0.15) → underpowered, not falsified
- **FAIL**: Any C fails → orthogonality not confirmed; product must pivot

## 14. Positive Control

**PC-TP-VARIANCE-CACHE**: Verify the server with HTTP caching produces detectable behavioral drift. Mean TP >= 0.85, all Wilson lower CI > 0.75. This confirms the measurement pipeline is not broken by HTTP caching changes (304 responses, ETag headers).

## 15. Null Control

**NC-FP-CACHE**: Verify zero false positives on noise-only conditions. FP = 0.0 across all noise-only samples. Confirms structural noise does not create spurious behavioral signal.

## 16. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-PARENT-STOCHASTIC-N480 | Parent result: r=0.0463, CI upper 0.135, delta=0.15 PASS | CI upper < 0.15 |
| B-NO-CACHE-HEADERS | This server with Cache-Control: no-store (HTTP caching disabled) | CI upper < 0.15 |

## 17. Falsification Conditions

The hypothesis is FALSIFIED if ANY of:
1. C1_drift_tp fails (mean TP < 0.85 OR any Wilson lower CI < 0.75)
2. C2_variance fails (< 4/4 conditions with std > 0)
3. C3_equivalence fails (CI upper >= 0.15 AND TOST fails at delta=0.15)
4. C4_null_control fails (FP > 0.0)

## 18. Measurement Validity Threats

1. **ETag determinism**: ETags computed from response body hash. If response bodies vary stochastically (cache TTL, jitter), ETags may change between requests to the same resource, creating structural signal variation that is an artifact of timing rather than schema change. Mitigation: ETags computed from content-only hash (excluding timing headers).

2. **304 response content**: 304 Not Modified responses carry no body. The structural signal computation must handle empty-body responses gracefully (use cached schema or ETag-only comparison).

3. **Cache-Control interaction with in-memory TTL**: The parent's in-memory cache (TTL=0.5s) and HTTP Cache-Control (max-age=5) operate at different layers. Both are present in the "enabled" condition. This is intentional — it simulates real production where application-level and HTTP-level caching coexist.

4. **Sample size reduction**: n=240 (vs parent's n=480) reduces power. Minimum detectable |r| = 0.129 vs parent's 0.090. This is acceptable because the question is delta=0.15 equivalence, not tighter margins.

5. **Localhost network**: All requests are localhost. No CDN, no distributed cache, no network latency beyond localhost round-trip. This bounds the claim ceiling to "HTTP caching semantics on localhost" — production CDN behavior remains untested.

## 19. Product Consequence

**If PASS (CI upper < 0.15)**: C-FRESHNESS advances. Parallel-channel architecture (behavioral + structural as independent channels) is justified for production APIs with HTTP caching. Product pipeline can integrate both channels without fused classifiers.

**If FAIL (CI upper >= 0.20)**: C-FRESHNESS stalls. HTTP caching introduces non-negligible correlation. Product must pivot to fused classifiers or redesign the structural signal to be cache-independent.

**If MIXED (CI upper 0.10-0.15)**: C-FRESHNESS remains EXPERIMENTAL. More data needed. Parallel channels tentatively justified but with monitoring.

## 20. Consequences of Negative Outcome

A negative result (FAIL) does NOT close C-FRESHNESS. It means the specific structural signal (schema shape from /schema) is not cache-independent. Product alternatives:
1. Use cache-independent structural signals (e.g., OpenAPI spec hash, API contract version)
2. Fuse behavioral and structural into a single detector
3. Strip cache-dependent variance from structural signal before correlation measurement

## 21. What This Experiment Does NOT Test

- Real external APIs (GitHub, Stripe, etc.) — only localhost mock
- CDN-distributed caching — only single-server in-memory cache
- OAuth/OIDC middleware — only JWT validation
- Network latency beyond localhost — no WAN simulation
- Concurrent client load — sequential requests only
- delta=0.10 equivalence — underpowered at n=240

## 22. Artifact Paths

- Mock server: `research/experiments/EXP-GRAPH-35375596525/mock_server.py`
- Experiment runner: `research/experiments/EXP-GRAPH-35375596525/run_experiment.py`
- Raw evidence: `research/experiments/EXP-GRAPH-35375596525/raw_evidence/experiment_data.json`
