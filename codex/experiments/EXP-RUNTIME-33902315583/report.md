# EXP-RUNTIME-33902315583 — Execution Report

## Executive Summary

**Status**: COMPLETE  
**Outcome**: SUPPORTS C-MEAS-VALID SURVIVES

The HTTP fingerprint substrate achieves discrimination 0.833 on a real Flask/PyJWT server with 4 auth states, no synthetic headers, and identical error bodies for expired vs invalid tokens. All three decision criteria pass: discrimination > 0.5 (0.833 > 0.5), null FP rate < 5% (0.0% < 5%), and valid vs expired drift discriminable (Jaccard 0.3505 < 0.5). C-MEAS-VALID survives on real Flask/JWT middleware.

## Results

### Primary Metric: Full-Vector Discrimination

- **Discrimination score**: 0.8333 (threshold: > 0.5) — **PASS**
- **Intra match rate**: 1.000 (perfect within-state consistency)
- **Inter match rate**: 0.167 (only expired/invalid match across states)
- **Bootstrap 95% CI**: [0.0, 1.0] (degenerate at near-perfect separation)
- **Mean intra Jaccard**: 1.0 (identical fingerprints within states)
- **Mean inter Jaccard**: 0.474 (moderate similarity between distinct states)

### Baseline Comparisons

| Baseline | Discrimination | vs Full Vector | Interpretation |
|----------|---------------|----------------|----------------|
| B-STATUS-ONLY | 0.500 | 0.833 > 0.500 | Full vector exceeds (body adds information) |
| B-BODY-ONLY | 0.833 | 0.833 = 0.833 | Full vector equals body-only (headers add no info) |
| B-URL-HASH | 0.000 | — | Straw-man, expected |
| B-RANDOM | 0.000 | — | Straw-man, expected |

**Key architectural finding**: Full vector equals B-BODY-ONLY exactly. Standard headers (Content-Type, Content-Length) add zero discriminating information. Body is the dominant signal. This constrains product architecture: body-based observation is sufficient for this auth drift scenario.

### Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| C_NULL_FP_RATE | < 5% | 0.0% | ✅ |
| C_POSITIVE_DISCRIMINATION | > 0.5 | 0.833 | ✅ |
| C_BASELINE_STATUS_SUPERIORITY | full > B-STATUS | 0.833 > 0.500 | ✅ |
| C_DRIFT_VALID_VS_EXPIRED | Jaccard < 0.5 | 0.3505 | ✅ |
| C_DRIFT_EXPIRED_VS_INVALID | Jaccard >= 0.5 (expected non-discrim) | 1.000 | ✅ |
| C_ERROR_RATE | < 20% | 0.0% | ✅ |

### Drift Pairs

- **valid_token → expired_token**: Jaccard 0.3505 (discriminable — status differs 200 vs 401 AND body differs)
- **expired_token → invalid_token**: Jaccard 1.000 (non-discriminable — identical status, body, headers). This is **correct substrate behavior**, not a failure.

## Interpretation

### C-MEAS-VALID Survives on Real Flask/JWT Middleware

The three mandatory parent gaps are now closed:

1. **V1-REAL-MIDDLEWARE-GAP**: CLOSED. Server is Flask 3.1.3 with PyJWT 2.13.0 HS256 validation — real JWT middleware, not hand-programmed lookup tables. Discrimination 0.833 > 0.5.

2. **V2-SYNTHETIC-HEADER-TAUTOLOGY**: CLOSED. No X-Auth-Level, X-Session, X-User, X-Error headers. Server returns only standard HTTP headers (Content-Type, Content-Length, Server, Date). Discrimination maintained at 0.833.

3. **Identical error bodies**: CLOSED. expired_token and invalid_token return identical 401 responses with body `{"error":"authentication_failed"}`. Substrate correctly reports them as non-discriminable (Jaccard 1.0) while still discriminating valid from expired/invalid (Jaccard 0.3505).

### What Is Established

- Deterministic SHA-256 fingerprint of (status, sorted-headers-excluding-Date/Server, body_sha256, redirect_chain) achieves discrimination 0.833 on real Flask/JWT middleware with 4 auth states and 50-150ms server-side jitter.
- Intra-state fingerprints are perfectly consistent (10/10 match per state, null FP 0%).
- Body is the dominant signal: full vector = B-BODY-ONLY (0.833 = 0.833). Standard headers add no discriminating information.
- Full vector exceeds B-STATUS-ONLY (0.833 > 0.500) because body distinguishes no_auth from expired/invalid when all three share status 401.
- expired_token vs invalid_token correctly non-discriminable (identical bodies).

### What Remains Unknown

- Does the substrate maintain discrimination on production OAuth/OIDC providers with additional response variation?
- What is the FP rate under server-side jitter >150ms or volatile standard headers?
- Does full vector exceed B-BODY-ONLY when standard headers vary with auth state in production?
- Cross-Python-version reproducibility of repr(vector) hashes?

## Validity Threats

1. **Flask vs Production**: Flask with PyJWT is real JWT validation, but production OAuth/OIDC providers may have additional response variation. Findings apply to Flask/JWT specifically.
2. **JSON Serialization**: Python 3.12+ dict ordering is insertion-ordered; `jsonify` produces deterministic output for identical dicts. Mitigated by body_sha256 comparison.
3. **Standard Headers**: Flask/Werkzeug may add headers (e.g., `Connection: close`). These are consistent within auth states and excluded or constant, so they don't affect discrimination.
4. **Sample Size**: 40 requests (4 states × 10 reps) — sufficient for primary discrimination test (>0.5 threshold) but limited for subtle differences.
5. **Bootstrap CI Degenerate**: [0.0, 1.0] reflects near-perfect separation with only 4 states — method resamples states, not requests.
6. **Python Version**: repr(vector) is Python-version-dependent; validated only on Python 3.12.14.
