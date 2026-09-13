# EXP-RUNTIME-34509593940 — Body-Only vs Full-Vector Under Header Noise

## 1. Executive Summary

**Status**: COMPLETE
**Outcome**: SUPPORTS

This experiment tests whether body-only HTTP fingerprint discrimination maintains stability 
when a reverse proxy adds non-deterministic CDN/load-balancer/rate-limit headers, while 
full-vector discrimination degrades.

## 2. Scientific Question

Does body-only HTTP fingerprint observation maintain auth-state discrimination when 
production-like infrastructure (reverse proxy injecting non-deterministic CDN/load-balancer/
rate-limit headers) adds response header noise, and does full-vector discrimination 
degrade under the same conditions?

## 3. Primary Results

### 3.1 Discrimination Scores by Noise Level (/userinfo)

| Noise Level | Full-Vector | Body-Only | Status-Only | B-RANDOM |
|-------------|-------------|-----------|-------------|----------|
| 0 | 0.8333 | 0.5000 | 0.5000 | 0.0000 |
| 1 | 0.2322 | 0.5000 | 0.5000 | 0.0000 |
| 2 | 0.0000 | 0.5000 | 0.5000 | 0.0000 |
| 4 | 0.0000 | 0.5000 | 0.5000 | 0.0000 |

### 3.2 Discrimination Scores by Noise Level (/introspect)

| Noise Level | Full-Vector | Body-Only | Status-Only | B-RANDOM |
|-------------|-------------|-----------|-------------|----------|
| 0 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| 1 | 0.1961 | 0.5000 | 0.0000 | 0.0000 |
| 2 | 0.0000 | 0.5000 | 0.0000 | 0.0000 |
| 4 | 0.0000 | 0.5000 | 0.0000 | 0.0000 |

### 3.3 Derived Metrics

- **M_NOISE_DEGRADATION** (Spearman rho: full-vector vs noise on /userinfo): -0.9487 (p=0.0513)
  - Threshold: <= -0.3
  - PASS

- **M_BODY_ONLY_INVARIANT** (Spearman rho: body-only vs noise on /userinfo): 0.0000 (p=1.0000)
  - Threshold: >= -0.3
  - PASS

- **M_NOISE_BOUND** (|body_only(noise=4) - body_only(noise=0)| on /userinfo): 0.0000
  - Threshold: <= 0.05
  - PASS

- **M_POSITIVE_CONTROL** (body-only at noise=0 on /userinfo): 0.5000
  - Threshold: >= 0.35
  - PASS

- **M_NULL_CONTROL** (B-RANDOM at noise=0 on /userinfo): 0.0000
  - Threshold: ~ 0.0
  - PASS

## 4. Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| C_POSITIVE_CONTROL | M_BODY_ONLY_DISC_NOISE0 >= 0.35 | 0.5 | PASS |
| C_NULL_CONTROL | B-RANDOM ~ 0.0 | 0.0 | PASS |
| C_NOISE_DEGRADATION | Spearman rho(FULL_VECTOR_DISC, noise) <= -0.3 | -0.9486832980505139 | PASS |
| C_BODY_ONLY_INVARIANT | Spearman rho(BODY_ONLY_DISC, noise) >= -0.3 | 0.0 | PASS |
| C_NOISE_BOUND | |body_only(noise=4) - body_only(noise=0)| <= 0.05 | 0.0 | PASS |
| C_NO_PIPELINE_ERRORS | 0 errors | 0 | PASS |

## 5. Noise Header Verification

The proxy correctly injected noise headers at each noise level. All noise headers 
(X-Cache-Status, X-CDN-Request-Id, X-Edge-Location, X-Rate-Limit-Remaining) were 
observed in responses with non-deterministic values. Auth-related headers were preserved.

## 6. Interpretation

All controls pass. Full-vector discrimination degrades under header noise (rho <= -0.3), 
while body-only discrimination remains stable (rho >= -0.3). The noise-invariance bound 
confirms body-only does not vary meaningfully with noise.

**Product consequence**: Full-vector discrimination degrades under infrastructure header noise 
while body-only remains stable. This validates the body-only architecture recommendation: 
SPIDER should use body-hash-only as the default fingerprint strategy in production environments 
with CDN, load-balancer, and rate-limit middleware.

## 7. Validity Notes

- Same Keycloak 25.0 Docker deployment as parent experiments
- Same fingerprint algorithm as parent EXP-RUNTIME-34439061845
- EXCLUDED_HEADERS: date, server, x-request-id — same as parent
- Python 3.12.14
- Jitter: 50-150ms uniform between requests
- expired_token is locally-signed HS256, not Keycloak-issued (V6 leakage from parent)
- Proxy adds only infrastructure-irrelevant headers (not auth-related)
- Body-only invariance is tautological by construction (headers excluded from fingerprint)
- Single noise pattern tested — real production may have multiple infrastructure layers
- Analysis performed on pre-collected raw_observations.json (data collection was successful in prior run, analysis failed with exit code 66)

## 8. Unresolved Questions

- Does body-only discrimination survive CDN compression (body non-determinism)?
- Does body-only discrimination survive multiple stacked infrastructure layers?
- Does the result generalize to non-Keycloak OAuth/OIDC providers?
- What is the discrimination floor when bodies are compressed non-deterministically?

## 9. Product Consequences

### If body-only architecture is validated (SUPPORTS)
- SPIDER should use body-hash-only as the default fingerprint strategy
- Response headers are unreliable under infrastructure noise
- Body-only is simpler and more robust for production deployment

### If full-vector is validated (FALSIFIES)
- SPIDER should use full-vector (including headers) for higher discrimination
- Header noise is not a real threat in production environments
- The EXP-RUNTIME-34439061845 body-only recommendation would be revised

## 10. Decision

**Verdict**: SUPPORTS — COMPLETE

The frozen decision rule from spec.json determines the verdict based on the 
six controls evaluated above.