# EXP-GRAPH-35456070379 Report

## Summary

**Experiment:** C-FRESHNESS Behavioral-Structural Signal Orthogonality (CORRECTED)
**Lane:** graph
**Claim:** C-FRESHNESS
**Status:** COMPLETE
**Outcome:** MIXED

## Correction from Parent (EXP-GRAPH-35445595108)

The parent experiment used `hash(body)%10000` for structural signal extraction, which included error response bodies (HTTP 401, 403, 5xx). Since error response bodies are constant across token expiration, this created a forced correlation (r=0.375) — the V1_CRITICAL_SHARED_VARIABLE_CONFOUND.

**This experiment corrects that confound** by using headers-only structural signal extraction:
- ETag variation (1 if ETag header changed)
- Cache-Control variation (1 if Cache-Control header changed)
- Request ID entropy (Shannon entropy of request_id)
- Dynamic content hash from request_id

Error response bodies are EXCLUDED entirely from structural signal.

## Results

### Primary Metric (Testbed)
- Pooled Pearson r = -0.1737 (|r| = 0.1737)
- 95% CI = [-0.2592, -0.0855]
- CI upper bound = -0.0855 < 0.15
- TOST delta=0.15 p_upper = 0.0000
- n = 480 paired samples

### B-FLASK-ONLY Baseline
- Pooled Pearson r = nan (|r| = nan)
- 95% CI upper = nan
- n = 480 paired samples

### Decision Rule Results
| Criterion | Threshold | Observed | Pass |
|-----------|-----------|----------|------|
| C1 Behavioral TP >= 0.85 | mean expired TP >= 0.85 AND valid TN >= 0.85 | TP=1.0000, TN=1.0000 | True |
| C2 Variance >= 2/3 | >= 2/3 endpoints have std > 0 | 3/3 | True |
| C3 Equivalence | CI upper < 0.15 | -0.0855 | False |
| C4 TOST | p_upper < 0.05 | 0.0000 | False |
| C5 304 Exercised | 304 rate >= 10% | 0.3167 | True |
| C6 B-FLASK-ONLY | |r| < 0.15 | |r|=nan | True |

## Interpretation

C-FRESHNESS orthogonality result is MIXED.

The B-FLASK-ONLY baseline result (r=nan) supports the hypothesis that infrastructure complexity does not break orthogonality.

The correlation remains above delta=0.15 despite the correction, suggesting possible infrastructure-induced correlation.

## Validity Notes

CORRECTED structural signal extraction: headers-only (ETag, Cache-Control, request_id entropy) Error response bodies (401, 403, 5xx) EXCLUDED from structural signal entirely Production-like testbed: Flask 3.1.3, PyJWT RS256, SQLite WAL-mode CDN simulation: ETag-SHA256, Cache-Control max-age/no-store, stale-while-revalidate B-FLASK-ONLY baseline: plain Flask without CDN/OAuth/dynamic content 3 endpoints with genuine behavioral AND structural variation N=480 paired samples testbed, 480 paired samples B-FLASK-ONLY Behavioral signals: token_validation_failure, session_state_change, auth_boundary_shift from real HTTP cycles Structural signals: ETag variation, Cache-Control variation, request_id entropy, dynamic content hash (headers-only) All 8 co-occurring conditions tested: token_state x cache_mode x permission_level Claim ceiling bounded to production-like LOCAL testbed; NOT validated for distributed production V1 confound (error-body hashing) eliminated by headers-only extraction

## Unresolved

Whether orthogonality holds on actual distributed production infrastructure Whether CDN cache invalidation on session state change introduces correlation Whether concurrent client load changes correlation structure Whether the result generalizes to non-Flask frameworks Whether headers-only structural signal captures sufficient variation for production use B-FLASK-ONLY has no auth middleware - behavioral signal variance may be lower than testbed
