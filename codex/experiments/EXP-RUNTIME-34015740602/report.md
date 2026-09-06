# EXP-RUNTIME-34015740602 — Report

## Experiment Summary

**Experiment ID**: EXP-RUNTIME-34015740602
**Lane**: Runtime
**Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
**Status**: COMPLETE
**Outcome**: SUPPORTS

## Question

Does the HTTP fingerprint substrate maintain discrimination > 0.5 on a production-like OAuth/OIDC middleware with realistic response variation (cache-Control, ETag, X-Request-Id, Set-Cookie, rate-limit headers) — and does the full vector (status + body + all headers) ever exceed B-BODY-ONLY when headers vary independently with auth state?

## Result

**C-MEAS-VALID SURVIVES** on production-like OAuth middleware with realistic header variation.

All three mandatory decision criteria pass:

1. **Full-vector discrimination: 1.000000 > 0.5** — perfect discrimination across 4 auth states
2. **Null control FP rate: 0.0% < 5%** — no false fingerprints under server-side jitter 50-150ms
3. **valid_token vs expired_token drift discriminable: Jaccard 0.3280 < 0.5** — drift detection works

## Key Findings

### 1. Perfect Discrimination (1.000000)

Full-vector discrimination improved from 0.833 (parent Flask/JWT) to 1.000000 on production-like middleware. This improvement is driven by the frozen design change: expired_token and invalid_token now return **distinct** response bodies (unlike the parent experiment where they were identical). With distinct bodies, all 4 states are perfectly separable.

### 2. Full Vector Equals B-BODY-ONLY (1.0 = 1.0)

Despite adding production-realistic headers (cache-Control, ETag, Set-Cookie), the full vector does **not** exceed B-BODY-ONLY. The body remains the dominant signal. This is the same finding as the parent Flask/JWT experiment (0.833 = 0.833), now replicated on production-like middleware with realistic header variation.

**Implication for product architecture**: Body-based observation is sufficient for auth drift detection on production-like OAuth middleware. Multi-field observation (status + body + filtered headers) adds no discriminating information over body-only. Product can use simpler body-only observation with fewer failure modes.

### 3. Set-Cookie and cache-Control Add No Independent Information

The experiment was specifically designed to test whether Set-Cookie (present only for valid_token) and cache-Control (varies by auth state) add independent discriminating information when headers vary with auth state. The answer is **no**: these headers are redundant with the body signal. When bodies are fully discriminative (all 4 states have distinct bodies), headers cannot improve discrimination beyond 1.0.

### 4. X-Request-Id Exclusion Validated

X-Request-Id (UUID per request) was correctly excluded from the fingerprint. Each auth state produced exactly 1 unique fingerprint across 10 repetitions, confirming that volatile per-request identifiers do not cause false fingerprint variation when excluded.

### 5. Expired vs Invalid Now Discriminable

Unlike the parent experiment (Jaccard 1.0 — identical bodies), expired_token vs invalid_token are now discriminable (Jaccard 0.3316 < 0.5) because they return distinct error messages. This confirms the substrate correctly discriminates when bodies differ, even when status codes are identical.

## Baseline Comparison

| Baseline | Discrimination | Interpretation |
|----------|---------------|----------------|
| Full vector | 1.000000 | Perfect discrimination |
| B-BODY-ONLY | 1.000000 | Equal to full vector — body is dominant |
| B-STATUS-ONLY | 0.500000 | 3 states share status 401 — cannot distinguish |
| B-URL-HASH | 0.000000 | URL is constant — no information |
| B-RANDOM | 0.000000 | Random — no information |

Full vector > B-STATUS-ONLY (1.0 > 0.5) because body distinguishes no_auth from expired/invalid when all three share status 401.

## Controls

All 6 controls pass:

- **C_NULL_FP_RATE**: 0.0% < 5% — server-side jitter does not cause false fingerprint variation
- **C_POSITIVE_DISCRIMINATION**: 1.0 > 0.5 — substrate discriminates auth states
- **C_BASELINE_STATUS_SUPERIORITY**: Full vector > B-STATUS-ONLY — body adds value over status alone
- **C_DRIFT_VALID_VS_EXPIRED**: Jaccard 0.3280 < 0.5 — drift between valid and expired is detectable
- **C_DRIFT_EXPIRED_VS_INVALID**: Jaccard 0.3316 < 0.5 — distinct error bodies are discriminable (unlike parent)
- **C_ERROR_RATE**: 0.0% < 20% — all requests succeeded

## Comparison to Parent (EXP-RUNTIME-33902315583)

| Metric | Parent (Flask/JWT) | This Experiment (OAuth-like) |
|--------|-------------------|------------------------------|
| Full-vector discrimination | 0.833 | 1.000 |
| B-BODY-ONLY | 0.833 | 1.000 |
| Full = Body-only | Yes (0.833 = 0.833) | Yes (1.0 = 1.0) |
| Null FP rate | 0.0% | 0.0% |
| valid vs expired Jaccard | 0.3505 | 0.3280 |
| expired vs invalid Jaccard | 1.0 (identical bodies) | 0.3316 (distinct bodies) |
| Headers | Standard only | Production-realistic |
| Error bodies | Identical (expired=invalid) | Distinct |

The improvement from 0.833 to 1.0 is entirely explained by the design change (distinct error bodies), not by the production-like headers. Full vector still equals B-BODY-ONLY in both experiments.

## Product Consequences

- **If full vector > B-BODY-ONLY**: Product should use multi-field observation (status + body + filtered headers). **NOT OBSERVED** — this outcome did not occur.
- **If full vector = B-BODY-ONLY**: Body-only observation sufficient → simpler product architecture. **OBSERVED** — product can use body-only observation.
- **If full vector < B-BODY-ONLY**: Headers introduce noise → product should exclude volatile headers. **NOT OBSERVED**.

**Recommendation**: Product should use body-based observation for auth drift detection on production-like OAuth middleware. Set-Cookie and cache-Control do not add independent discriminating information when bodies are fully discriminative. The claim ceiling for C-MEAS-VALID extends to production-like OAuth middleware with realistic header variation.

## Validity Threats

1. **Mock vs Production**: Server is a Flask app with local token introspection, not a real OAuth/OIDC provider (Auth0, Okta, Keycloak). Production providers may add CDN headers, load-balancer variance, rate-limiting, compressed encoding not captured here.
2. **X-Request-Id Exclusion**: X-Request-Id is excluded because it is a per-request UUID. If a production provider uses X-Request-Id that encodes auth state, this exclusion would lose information.
3. **Body Distinctness**: Unlike the parent (expired/invalid sharing identical bodies), this experiment uses distinct error messages. This makes discrimination easier. The parent's identical-body scenario is already established.
4. **ETag Correlation**: ETag is computed from body_hash, so it is perfectly correlated with body. It adds no independent information.
5. **Sample Size**: N=40 (4 states × 10 reps) is sufficient for the primary threshold test (>0.5) but limited statistical power for fine-grained baseline comparisons.
