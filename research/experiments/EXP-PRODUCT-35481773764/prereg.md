# EXP-PRODUCT-35481773764 preregistration

## Experiment identity

- **experiment_id**: EXP-PRODUCT-35481773764
- **lane**: product
- **claim_ids**: C-FRESHNESS
- **parent**: EXP-PRODUCT-35476271728 (all 5 frozen conditions pass at n=480, audit PASS)
- **created_at**: 2026-09-20

## 1. Question

Does token_refresh behavioral drift detection remain robust (TP >= 0.85, behavioral_std > 0.05) when co-occurring structural noise includes production-like complexity patterns (pagination metadata, variable-length response bodies, error format variation, CDN cache headers) rather than only the 4 simplistic field-level noise types tested in the parent?

## 2. Hypothesis

Token_refresh behavioral detection (TP >= 0.85) and behavioral variance (std > 0.05) will survive co-occurring production-like structural noise at n=480, because the behavioral signal is derived from JWT validation status (token state, session validity, permission checks) which is independent of response body structure. The parent validated TP=1.0 under 4 simplistic noise types; this experiment tests robustness to structurally complex noise that mimics real API response variation.

## 3. Falsifier

FALSIFIED if any of:
- (F1) token_refresh TP < 0.85 under co-occurring production-like noise at n=480
- (F2) behavioral_std < 0.05 under co-occurring production-like noise at n=480
- (F3) structural discrimination < 0.5 (positive control)
- (F4) FP > 0.15 on production-like noise-only samples
- (F5) TOST at delta=0.15 fails (CI upper bound >= 0.15) for full pooled sample at n=480

MIXED if C1-C4 pass but C5 fails.

## 4. Baselines

### B-SIMPLISTIC-NOISE-N480 (parent)
Parent n=480 result with 4 simplistic noise types (optional_field_addition, description_change, response_time_jitter, field_type_normalization):
- TP=1.0 on all 4 token_refresh+noise conditions
- behavioral_std 0.133-0.141
- FP=0.0
- TOST PASS at delta=0.15 (r=-0.037, CI upper 0.053)

Expected: TP >= 0.85 under production-like noise; behavioral_std > 0.05

### B-ORTHOGONALITY-N480-MOCK
Four prior n=480 mock orthogonality experiments all confirm delta=0.15:
- EXP-GRAPH-35353011131: r=0.046, CI upper 0.135
- EXP-GRAPH-35389145821: r=0.0022, CI upper 0.0916
- EXP-PRODUCT-35445596342: r=-0.0258, CI upper 0.064
- EXP-PRODUCT-35476271728: r=-0.037, CI upper 0.053

Expected: Production-like noise does not introduce behavioral-structural coupling that breaks orthogonality at delta=0.15

## 5. Positive control

### PC-STRUCTURAL-DISCRIMINATION
HTTP fingerprint full-vector discrimination on stochastic Flask+SQLite mock server with 4 auth states (no_auth, valid_token, expired_token, invalid_token). Discrimination must exceed 0.5 to confirm the structural signal is operational.

Expected: Full-vector discrimination > 0.5 (replicating parent 0.8333)

## 6. Null control

### NC-NOISE-FP
Behavioral false positive rate on production-like noise-only samples (4 production-like noise types x 60 samples = 240 noise-only samples, no drift active).

Expected: FP <= 0.15 on noise-only samples

## 7. Production-like structural noise design

4 new noise types REPLACE the 4 parent simplistic types for co-occurring conditions:

### 7.1 pagination_metadata
Adds pagination fields (page, per_page, total_count, has_next) to response body, simulating API list endpoints. Field count varies 2-6 per request. Structural effect: body key count varies by 2-6.

Parent equivalent: optional_field_addition (simpler: adds 1 fixed field)

### 7.2 variable_length_data
Response body data_list length varies 0-8 items per request, simulating real API data return variation. Each item adds 3-5 keys. Structural effect: body key count varies by 0-40.

Parent equivalent: description_change (simpler: changes 1 string field)

### 7.3 error_format_variation
Error responses use different formats depending on error type: 401 returns {error, message, code}, 403 returns {error, message, required_permission}, 500 returns {error, message, request_id}. Structural effect: body structure varies across status codes.

Parent equivalent: field_type_normalization (simpler: changes 1 field's type)

### 7.4 cdn_cache_headers
Adds CDN-specific response headers: X-Cache (HIT/MISS), X-CDN-Cache-Control (max-age varies 0-300), Age (varies 0-60), CF-Ray (random UUID). Structural effect: header count varies by 3-4.

Parent equivalent: response_time_jitter (simpler: timing variation only)

## 8. Measurement validity

1. Stochastic Flask+SQLite mock server matching EXP-PRODUCT-35476271728 (Flask 3.1.3 + SQLite WAL-mode DB + in-memory cache TTL=0.5s + jitter 10-100ms + mixed JWT algorithms HS256/RS256)
2. Token_refresh drift: p_refresh_success=0.7 (Bernoulli), producing bimodal behavioral scores (~0.48 on failure, ~0.65 on success)
3. 4 NEW production-like structural noise types REPLACE the 4 parent simplistic types for co-occurring conditions; the parent types are used ONLY for the isolated baseline comparison
4. Server state fully reset between conditions (set_drift(None) clears all state)
5. N = 480 paired samples minimum (60 per condition x 8 co-occurring conditions) for token_refresh TP and orthogonality; additional 240 production-like noise-only samples for FP measurement
6. Orthogonality tested via TOST equivalence test at delta=0.15 on Fisher-z transformed Pearson correlation
7. All measurements on localhost mock server (127.0.0.1:18951), not production APIs
8. This experiment does NOT make real LLM calls
9. Global RNG seeded at 42 before server thread start; server runs threaded=False, client sequential

## 9. Decision rule

SURVIVES_CURRENT_TEST requires ALL of:
- (C1) structural discrimination > 0.5 (positive control)
- (C2) token_refresh TP >= 0.85 under co-occurring production-like noise at n=480
- (C3) token_refresh behavioral_std > 0.05 under co-occurring production-like noise at n=480
- (C4) FP <= 0.15 on production-like noise-only samples
- (C5) TOST equivalence at delta=0.15 (CI upper bound < 0.15) for full pooled sample

FALSIFIED if any condition fails.

MIXED if C1-C4 pass but C5 fails (equivalence not confirmed under production-like noise despite adequate power).

## 10. Product consequences

### If SURVIVES
- Token_refresh detection robust to production-like structural complexity
- Behavioral signal not limited to simplistic noise patterns
- Strengthens case for production substrate readiness
- C-FRESHNESS claim ceiling expanded to include realistic structural variation
- Moves C-FRESHNESS toward PRODUCT_CORE eligibility (pending production-substrate validation)

### If FALSIFIED
- Token_refresh detection fragile under production-like structural complexity
- Behavioral signal couples with realistic response variation
- Production substrate must handle structural-behavioral coupling
- C-FRESHNESS claim ceiling remains bounded to simplistic noise types only
- Alternative detection strategy required before production deployment

## 11. Estimated cost

Zero new LLM calls. Extends existing stochastic mock server with 4 new noise types. 480 paired phase-B samples + 240 production-like noise-only phase-C samples + 40 phase-A probes + 60 isolated TP samples = ~820 total HTTP cycles on localhost. Runtime ~35-45 minutes single-threaded. No API keys required.

## 12. Expected information gain

MEDIUM-HIGH: directly tests whether the behavioral detection signal generalizes beyond simplistic noise patterns to realistic structural complexity. A positive result strengthens the production-readiness case; a negative result identifies a structural coupling vulnerability before the expensive production substrate is built. Either outcome changes the product architecture decision for C-FRESHNESS.

## 13. Exploration vs confirmatory

This is a CONFIRMATORY experiment. All conditions, thresholds, and decision rules are frozen before execution. The 4 production-like noise types are defined in advance with specific structural effects. The threshold sensitivity analysis from the parent (TP cliff at 0.40) is carried forward but does not affect the primary decision.

## 14. Deviation policy

No deviations permitted after freeze. If infrastructure fails (mock server unreachable, noise implementation bugs), write failure.json and do not weaken the decision rule.
