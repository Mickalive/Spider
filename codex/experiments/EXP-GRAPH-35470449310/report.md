# EXP-GRAPH-35470449310 Report

## Summary

**Experiment:** C-FRESHNESS Behavioral-Structural Signal Orthogonality (V1+V2 CORRECTED)
**Lane:** graph
**Claim:** C-FRESHNESS
**Status:** COMPLETE
**Outcome:** MIXED

## Corrections from Parent (EXP-GRAPH-35456070379)

### V1 FIX: request_id entropy confound
The parent used `secrets.token_hex(8)` for expired 401 responses and `str(uuid.uuid4())` for valid responses, creating a p=2.7e-34 entropy difference that propagated into the structural composite via `request_id_entropy` (weight 0.2) and `dynamic_content_hash` (weight 0.2).

**This experiment uses `str(uuid.uuid4())` for ALL status codes** (200, 304, 401, 403), eliminating the entropy confound entirely.

### V2 FIX: B-FLASK-ONLY degenerate baseline
The parent's flask_only_server.py had zero auth middleware, producing `behavioral_delta=0.0` for all 480 samples (std=0, r=NaN), making C6 trivially true and uninformative.

**This experiment's flask_only_server.py implements genuine token-state variation** via a `/token` endpoint that creates valid/expired tokens. Tokens are validated on each request, producing 401 for expired tokens.

## Results

### Primary Metric (Testbed)
- Pooled Pearson r = -0.0877 (|r| = 0.0877)
- 95% CI = [-0.1758, 0.0018]
- CI upper bound = 0.0018 < 0.15
- TOST delta=0.15: p_upper = 0.0000, p_lower = 0.0837
- n = 480 paired samples

### B-FLASK-ONLY Baseline (V2 corrected)
- Pooled Pearson r = 0.0260 (|r| = 0.0260)
- 95% CI upper = 0.1152
- Behavioral std = 3.5000 > 0 (V2 fix working)
- n = 480 paired samples

### Decision Rule Results
| Criterion | Threshold | Observed | Pass |
|-----------|-----------|----------|------|
| C1 Behavioral TP >= 0.85 | mean expired TP >= 0.85 AND valid TN >= 0.85 | TP=1.0000, TN=1.0000 | True |
| C2 Variance >= 2/3 | >= 2/3 endpoints have std > 0 | 3/3 | True |
| C3 Equivalence | CI within (-0.15, 0.15) | CI=[-0.1758,0.0018] | False |
| C4 TOST | p_upper < 0.05 | p_upper=0.0000 | False |
| C5 Cache heterogeneity | |r_enabled - r_disabled| < 2*SE | diff=0.2203 | False |
| C6 B-FLASK-ONLY | |r| < 0.15 | |r|=0.0260 | True |

## Interpretation

C-FRESHNESS orthogonality result is MIXED.

The B-FLASK-ONLY baseline (|r|=0.0260) confirms orthogonality persists without production-like infrastructure features.

The corrections did not fully resolve the measurement validity gaps.

## Validity Notes

- V1 FIX: ALL request_ids use uuid.uuid4() for ALL status codes (200, 304, 401, 403)
- V2 FIX: B-FLASK-ONLY has genuine token-state variation via /token endpoint
- Structural signal extraction: headers-only (ETag, Cache-Control, request_id entropy)
- Error response bodies (401, 403, 5xx) EXCLUDED from structural signal entirely
- Production-like testbed: Flask 3.1.3, PyJWT RS256, SQLite WAL-mode
- CDN simulation: ETag-SHA256, Cache-Control max-age/no-store, stale-while-revalidate
- B-FLASK-ONLY baseline: plain Flask with token validation (valid/expired via header)
- 3 endpoints with genuine behavioral AND structural variation
- N=480 paired samples testbed, 480 paired samples B-FLASK-ONLY
- Behavioral signals: token_validation_failure, session_state_change, auth_boundary_shift
- Structural signals: ETag variation, Cache-Control variation, request_id entropy, dynamic content hash
- All 8 co-occurring conditions tested: token_state x cache_mode x permission_level
- Claim ceiling bounded to production-like LOCAL testbed; NOT validated for distributed production
- V1 confound (request_id entropy bifurcation) eliminated by UUID v4 for all status codes
- V2 confound (B-FLASK-ONLY zero behavioral variance) eliminated by adding token validation

## Unresolved

- Whether orthogonality holds on actual distributed production infrastructure
- Whether CDN cache invalidation on session state change introduces correlation
- Whether concurrent client load changes correlation structure
- Whether the result generalizes to non-Flask frameworks
- Whether headers-only structural signal captures sufficient variation for production use
- Whether per-cache heterogeneity is systematic or sampling noise
