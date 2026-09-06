# EXP-RUNTIME-34054515149 — Report

## Executive Summary

**Status: COMPLETE | Outcome: SUPPORTS**

When expired_token and invalid_token share **identical** response bodies but Cache-Control varies (no-store vs no-cache) and Set-Cookie is present only for valid_token, the full HTTP fingerprint vector achieves discrimination **1.0**, exceeding B-BODY-ONLY at **0.833** by an incremental header value of **0.167**. This confirms that Cache-Control and Set-Cookie provide independent discrimining information that body-only observation cannot capture when error responses share identical bodies.

## Scientific Question

Does the HTTP fingerprint substrate's full vector exceed B-BODY-ONLY when bodies are NOT perfectly discriminative (identical error bodies for expired/invalid token states) but headers (Cache-Control, Set-Cookie) vary independently with auth state?

## Key Results

| Metric | Value | Threshold | Pass |
|--------|-------|-----------|------|
| Full-vector discrimination | 1.000 | > 0.5 | ✓ |
| B-BODY-ONLY discrimination | 0.833 | — | — |
| Incremental header value | 0.167 | > 0 | ✓ |
| Cache-Control-only discrimination | 0.833 | > 0 | ✓ |
| Set-Cookie-only discrimination | 0.500 | > 0 | ✓ |
| Null FP rate | 0.0% | < 5% | ✓ |
| Full > B-BODY-ONLY | 1.200x | > 1.0 | ✓ |

## Design

This experiment resolves the H4 question that was vacuous at ceiling 1.0 in parent EXP-RUNTIME-34015740602. The parent had 4 distinct bodies, so full vector = B-BODY-ONLY = 1.0 (ceiling effect). Here, expired and invalid share the same body, degrading B-BODY-ONLY to 0.833 (3 groups: no_auth, valid_token, error_group). Cache-Control differentiates expired (no-store) from invalid (no-cache), lifting full vector to 1.0.

**Cache-Control pattern:**
- no_auth: absent
- valid_token: absent
- expired_token: no-store
- invalid_token: no-cache

**Set-Cookie pattern:**
- valid_token: present (session cookie)
- all others: absent

## Decision Rule (frozen)

SURVIVES_CURRENT_TEST if ALL of:
1. full_vector_discrimination > B-BODY-ONLY → **1.0 > 0.833 ✓**
2. full_vector_discrimination > 0.5 → **1.0 > 0.5 ✓**
3. null FP < 5% → **0.0% ✓**
4. Cache-Control-only discrimination > 0 → **0.833 ✓**

**Verdict: SURVIVES_CURRENT_TEST**

## Controls

All 10 controls pass:

- **C_NULL_FP_RATE**: 0.0% (10/10 identical fingerprints per state, 0/180 intra pairs differ)
- **C_POSITIVE_DISCRIMINATION**: 1.0 > 0.5
- **C_CACHE_CONTROL_VARIATION**: 0.833 > 0 — Cache-Control varies by auth state
- **C_SET_COOKIE_VARIATION**: 0.5 > 0 — Set-Cookie present only for valid_token
- **C_INCREMENTAL_HEADER_VALUE**: full=1.0, body_only=0.833, delta=0.167
- **C_BODY_CORRELATION_ETAG**: ETag=0.833 = B-BODY-ONLY=0.833 (body-correlated, redundant)
- **C_BODY_IDENTITY_EXPIRED_INVALID**: expired and invalid share body hash `a138b3ee...`
- **C_DRIFT_VALID_VS_EXPIRED**: Jaccard=0.325 < 0.5
- **C_DRIFT_EXPIRED_VS_INVALID**: Jaccard=0.381 < 0.5 (Cache-Control discriminates)
- **C_ERROR_RATE**: 0.0%

## Interpretation

### Why Cache-Control achieves 0.833 discrimination alone

Cache-Control has 3 distinct values across 4 states: absent (no_auth, valid_token), no-store (expired), no-cache (invalid). Two states share the same Cache-Control value (absent), so body-only grouping yields 3 groups — identical to the body-only case. However, Cache-Control achieves higher discrimination than body alone because it separates expired from invalid, which body cannot.

### Why Set-Cookie achieves 0.5 discrimination alone

Set-Cookie is binary: present (valid_token) vs absent (all others). This separates valid_token from the 3 error states, giving 2 groups. Discrimination = 0.5 because 3 states share the same Set-Cookie value.

### Why full vector = 1.0

The combination of status (200 vs 401), Cache-Control (3 values), and Set-Cookie (binary) uniquely identifies all 4 states. Bodies are redundant for discrimination — they add no additional information beyond what headers already provide.

### Comparison to parent EXP-RUNTIME-34015740602

| | Parent (distinct bodies) | This experiment (identical error bodies) |
|---|---|---|
| Full vector | 1.0 | 1.0 |
| B-BODY-ONLY | 1.0 | 0.833 |
| Incremental header value | 0.0 | **0.167** |
| Cache-Control-only | 0.5 | 0.833 |

The parent's ceiling effect (B-BODY-ONLY = 1.0) masked header value. This experiment reveals the true incremental contribution.

### Comparison to grandparent EXP-RUNTIME-33902315583

The grandparent tested identical error bodies with standard headers only (no Cache-Control, no Set-Cookie). Full vector = B-BODY-ONLY = 0.833. Adding Cache-Control and Set-Cookie lifts full vector to 1.0 — a 20% improvement over body-only.

## Product Consequence

**Headers provide incremental value over body-only observation when bodies are not distinct.** Product architecture should use full vector observation (status + headers + body) rather than body-only, because:
1. Cache-Control captures expired-vs-invalid distinction that body alone cannot
2. Set-Cookie captures valid-token distinction that body alone cannot
3. ETag and Content-Length are body-correlated and add no independent information

The H4 ceiling effect in the parent was an artifact of distinct-body design, not a general property. In production OAuth, error responses often share identical bodies (e.g., generic "authentication failed"), making header observation essential.

## Validity Threats

1. **Claim ceiling bounded to exact Flask/PyJWT localhost config** — does not extend to production OAuth/OIDC providers (Auth0, Okta, Keycloak) with CDN, load-balancer variance, or compressed encoding.
2. **Python-version-dependent** — repr(vector) hashes validated only on Python 3.12.14.
3. **Sample size N=40** — sufficient for primary threshold test but limited power for fine-grained comparisons.
4. **Bootstrap CI degenerate at ceiling** — [1.0, 1.0] is uninformative for product decisions.
5. **Cache-Control values are application-set** — production middleware may use different Cache-Control patterns.
