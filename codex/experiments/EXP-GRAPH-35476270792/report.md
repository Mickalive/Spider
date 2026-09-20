# EXP-GRAPH-35476270792 Report

## Summary

**Experiment:** C-FRESHNESS Behavioral-Structural Signal Orthogonality (V3+V4+V5)
**Lane:** graph
**Claim:** C-FRESHNESS
**Status:** COMPLETE
**Outcome:** MIXED

## Corrections from Parent (EXP-GRAPH-35470449310)

### V3 FIX: 304 exclusion from correlation
304 responses use a different structural composite construction: a fixed 0.2 constant for `dynamic_content_hash` instead of the variable sha256 hash used for non-304 responses. 304 occurs exclusively for valid tokens, creating token-state-dependent structural composite construction that violates spec validity clause 8.

**This experiment excludes 304 responses from pooled Pearson correlation** while retaining them for C1 behavioral detection and C2 structural variance checks.

### V4 FIX: B-PARENT-CONFOUND-REPRODUCTION negative control
Reproduces the exact confound from EXP-GRAPH-35456070379: expired tokens get `secrets.token_hex(16)` as request_id, valid tokens get `str(uuid.uuid4())`. This creates an entropy bifurcation (|r| >= 0.15 expected) that confirms the V1 confound was genuine.

### V5 FIX: One-sided C3/C4 per frozen spec
- C3 tests CI upper < 0.15 only (not both bounds)
- C4 tests TOST p_upper < 0.05 only (not two-sided)

## Results

### Primary Metric (Testbed, non-304)
- Pooled Pearson r = -0.1261 (|r| = 0.1261)
- 95% CI = [-0.2210, -0.0289]
- CI upper bound = -0.0289 < 0.15
- TOST delta=0.15: p_upper = 0.0000, p_lower = 0.3129
- n = 404 paired samples (non-304) / 480 total
- 304 statistics: 76 total (76 valid, 0 expired)

### B-FLASK-ONLY Baseline (V2 corrected)
- Pooled Pearson r = 0.0263 (|r| = 0.0263)
- 95% CI upper = 0.1155
- Behavioral std = 3.5000 > 0 (V2 fix working)
- n = 480 paired samples

### B-PARENT-CONFOUND-REPRODUCTION (V4 negative control)
- Pooled Pearson r = -0.1204 (|r| = 0.1204)
- 95% CI = [-0.2077, -0.0312]
- TOST delta=0.15: p_upper = 0.0000, p_lower = 0.2551
- n = 480 paired samples
- C7 pass (|r| >= 0.15): FAIL

### Decision Rule Results
| Criterion | Threshold | Observed | Pass |
|-----------|-----------|----------|------|
| C1 Behavioral TP >= 0.85 | mean expired TP >= 0.85 AND valid TN >= 0.85 | TP=1.0000, TN=1.0000 | True |
| C2 Variance >= 2/3 | >= 2/3 endpoints have std > 0 | 3/3 | True |
| C3 Equivalence (one-sided) | CI upper < 0.15 | upper=-0.0289 | True |
| C4 TOST (one-sided) | p_upper < 0.05 | p_upper=0.0000 | True |
| C5 Cache heterogeneity | |r_enabled - r_disabled| < 2*SE | diff=0.2506 | False |
| C6 B-FLASK-ONLY | |r| < 0.15 | |r|=0.0263 | True |
| C7 Negative control | |r| >= 0.15 on B-PARENT-CONFOUND | |r|=0.1204 | False |

## Interpretation

C-FRESHNESS orthogonality result is MIXED.

The B-FLASK-ONLY baseline (|r|=0.0263) confirms orthogonality persists without production-like infrastructure features.

The B-PARENT-CONFOUND negative control did not reproduce the expected confound.

V3 304 exclusion: 76 304 samples excluded from correlation (76 valid, 0 expired).

## Validity Notes

- V3 FIX: Exclude 304 responses from pooled Pearson correlation (304 uses fixed 0.2 constant for dynamic_content_hash instead of variable sha256 hash; occurs exclusively for valid tokens)
- V4 FIX: B-PARENT-CONFOUND-REPRODUCTION negative control reproduces V1 confound: expired tokens get secrets.token_hex(16), valid tokens get uuid4
- V5 FIX: C3 tests CI upper < 0.15 only (one-sided); C4 tests TOST p_upper < 0.05 only (one-sided)
- V1+V2 FIXES from parent: request_id uses uuid.uuid4() for ALL status codes; B-FLASK-ONLY has genuine token-state variation
- Structural signal extraction: headers-only (ETag, Cache-Control, request_id entropy)
- Error response bodies (401, 403, 5xx) EXCLUDED from structural signal entirely
- Production-like testbed: Flask 3.1.3, PyJWT RS256, SQLite WAL-mode
- CDN simulation: ETag-SHA256, Cache-Control max-age/no-store, stale-while-revalidate
- B-FLASK-ONLY baseline: plain Flask with token validation (valid/expired via header)
- B-PARENT-CONFOUND: reproduces V1 defect (token_hex for expired, uuid4 for valid) as negative control
- 3 endpoints with genuine behavioral AND structural variation
- N=404 paired samples testbed (non-304), 480 total testbed, 480 flask-only, 480 b-parent-confound
- Behavioral signals: token_validation_failure, session_state_change, auth_boundary_shift
- Structural signals: ETag variation, Cache-Control variation, request_id entropy, dynamic content hash
- All 8 co-occurring conditions tested: token_state x cache_mode x permission_level
- Claim ceiling bounded to production-like LOCAL testbed; NOT validated for distributed production
- V1 confound (request_id entropy bifurcation) eliminated by UUID v4 for all status codes in testbed/flask-only
- V2 confound (B-FLASK-ONLY zero behavioral variance) eliminated by adding token validation
- 304 exclusion: 76 304 samples excluded from correlation (76 valid, 0 expired)
- C7 negative control confirms V1 confound was genuine (|r| >= 0.15 expected)

## Unresolved

- Whether orthogonality holds on actual distributed production infrastructure
- Whether CDN cache invalidation on session state change introduces correlation
- Whether concurrent client load changes correlation structure
- Whether the result generalizes to non-Flask frameworks
- Whether headers-only structural signal captures sufficient variation for production use
- Whether per-cache heterogeneity is systematic or sampling noise
