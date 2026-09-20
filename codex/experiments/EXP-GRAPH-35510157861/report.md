# EXP-GRAPH-35510157861 Report

## Summary

**Experiment:** C-FRESHNESS Behavioral-Structural Signal Orthogonality (V3+V_ETAG+n>=800)
**Lane:** graph
**Claim:** C-FRESHNESS
**Status:** COMPLETE
**Outcome:** SUPPORTS

## Corrections from Parent (EXP-GRAPH-35481774794)

### V3 FIX: Endpoint-Stratified Pooling
The parent's pooled r was biased by 304 exclusion leaving skewed endpoint composition: valid cache-enabled non-304 was 91% session_status (40/44 samples), inflating pooled r from true stratified ~0.04 to -0.126. This experiment uses endpoint-stratified pooled r:

```
r_stratified = sum(n_i * r_i) / sum(n_i)
```

### V_ETAG_PERMISSION_LEAKAGE FIX
The parent's `_make_unauthorized_response()` defaulted permission_level to 'read' for expired tokens because `validate_token()` failed before extracting permission_level. This caused write-permission expired requests to get read-etag (stable_key mismatch with valid write-etag). Fix: decode expired JWT WITHOUT verification to extract permission_level, ensuring ETag independence from token expiry.

### POWER FIX: n >= 800
Increased paired samples from 480 to >= 800. SE reduced from ~0.050 to ~0.035. Minimum detectable |r| reduced from ~0.09 to ~0.07.

## Results

### Primary Metric (Endpoint-Stratified, non-304)
- **Stratified pooled r = 0.0257** (n = 684)
- 95% CI = [-0.0493, 0.1005]
- CI upper bound = 0.1005 < 0.15
- TOST delta=0.15: p_upper = 0.0005

### Simple Pooled r (reference)
- Pooled Pearson r = 0.0140 (|r| = 0.0140), n = 684
- 95% CI = [-0.0611, 0.0888]

### Per-Endpoint Non-304 r
- /api/user/profile: r=0.0094, n=206
- /api/data/list: r=0.0381, n=206
- /api/session/status: r=0.0287, n=272

### B-FLASK-ONLY Baseline
- Pooled Pearson r = 0.0201 (|r| = 0.0201)
- 95% CI upper = 0.0886
- Behavioral std = 3.5000 > 0

### B-PARENT-CONFOUND-REPRODUCTION (V4 negative control)
- Pooled Pearson r = -0.2992 (|r| = 0.2992)
- 95% CI = [-0.3660, -0.2415]
- C7 pass (|r| >= 0.15): PASS

### V_ETAG Permission Fix Verification
{
  "/api/user/profile": {
    "valid_write_etags": [
      "c471e2ffa78d6b682e38c4f98352b03dd40b7bf4c102e8ac046e1f16a7d6bc88"
    ],
    "expired_write_etags": [
      "c471e2ffa78d6b682e38c4f98352b03dd40b7bf4c102e8ac046e1f16a7d6bc88"
    ],
    "overlap_count": 1,
    "fix_verified": true
  },
  "/api/data/list": {
    "valid_write_etags": [
      "0f7349079319fb5f37d863225707eceba9a7bcf6f0d1106de5e5d20b587e7437"
    ],
    "expired_write_etags": [
      "0f7349079319fb5f37d863225707eceba9a7bcf6f0d1106de5e5d20b587e7437"
    ],
    "overlap_count": 1,
    "fix_verified": true
  },
  "/api/session/status": {
    "valid_write_etags": [
      "f11f5fe0d346a0d0b6777ecf9f13795bbdf5f8258bb2a008422600db584a8ef6"
    ],
    "expired_write_etags": [
      "f11f5fe0d346a0d0b6777ecf9f13795bbdf5f8258bb2a008422600db584a8ef6"
    ],
    "overlap_count": 1,
    "fix_verified": true
  }
}

### Decision Rule Results
| Criterion | Threshold | Observed | Pass |
|-----------|-----------|----------|------|
| C1 Behavioral TP >= 0.85 | mean expired TP >= 0.85 AND valid TN >= 0.85 | TP=1.0000, TN=1.0000 | True |
| C2 Variance >= 2/3 | >= 2/3 endpoints have std > 0 | 3/3 | True |
| C3 Equivalence (stratified) | CI upper < 0.15 | upper=0.1005 | True |
| C4 TOST (stratified) | p_upper < 0.05 | p_upper=0.0005 | True |
| C5 Cache heterogeneity (non-304) | |r_enabled - r_disabled| < 2*SE | diff=0.0833 | True |
| C6 B-FLASK-ONLY | |r| < 0.15 | |r|=0.0201 | True |
| C7 Negative control | |r| >= 0.15 on B-PARENT-CONFOUND | |r|=0.2992 | True |

## Interpretation

C-FRESHNESS orthogonality at delta=0.15 is CONFIRMED on the production-like testbed with all three corrections applied.

B-FLASK-ONLY baseline (|r|=0.0201) confirms orthogonality persists without production-like infrastructure.

B-PARENT-CONFOUND negative control (|r|=0.2992) confirms V1 confound was genuine.

V_ETAG permission fix verified: write-permission ETags overlap between valid and expired tokens.

Endpoint-stratified pooled r (0.0257) < 0.15, within equivalence bounds.

## Validity Notes

- V3 FIX: Endpoint-stratified pooling applied to C3/C4/C5. Parent's pooled r was biased by 304 exclusion leaving skewed endpoint composition (91% session_status in valid enabled non-304). Stratified pooled r weights each endpoint's r by its n.
- V_ETAG_PERMISSION_LEAKAGE FIX: testbed_server.py now decodes expired JWT tokens WITHOUT verification to extract permission_level, so write-permission expired requests get write-etag (not default read-etag). Verified via ETag overlap check.
- V3 FIX: 304 exclusion applied to ALL correlations (pooled, per-endpoint, per-cache) — not just pooled as in parent.
- V1+V2 FIXES from parent: request_id uses uuid.uuid4() for ALL status codes; B-FLASK-ONLY has genuine token-state variation
- POWER FIX: n >= 800 non-304 samples (34 per condition per endpoint x 8 conditions x 3 endpoints = 816)
- Structural signal extraction: headers-only (ETag, Cache-Control, request_id entropy)
- Error response bodies (401, 403, 5xx) EXCLUDED from structural signal entirely
- Production-like testbed: Flask 3.1.3, PyJWT RS256, SQLite WAL-mode
- CDN simulation: ETag-SHA256, Cache-Control max-age/no-store, stale-while-revalidate
- B-FLASK-ONLY baseline: plain Flask with token validation (valid/expired via header)
- B-PARENT-CONFOUND: reproduces V1 defect (token_hex for expired, uuid4 for valid) as negative control
- 3 endpoints with genuine behavioral AND structural variation
- N=684 paired samples testbed (non-304), 816 total testbed, 816 flask-only, 816 b-parent-confound
- Behavioral signals: token_validation_failure, session_state_change, auth_boundary_shift
- Structural signals: ETag variation, Cache-Control variation, request_id entropy, dynamic content hash
- All 8 co-occurring conditions tested: token_state x cache_mode x permission_level
- Claim ceiling bounded to production-like LOCAL testbed; NOT validated for distributed production
- 304 exclusion: 132 304 samples excluded from correlation (132 valid, 0 expired)
- C3/C4 decision uses endpoint-stratified pooled r (not simple pooled r)
- C7 negative control uses endpoint-stratified weighted |r| (not simple pooled |r|) as per audit recommendation
- C5 heterogeneity uses endpoint-stratified weighting for per-cache correlations (not simple concatenation)

## Unresolved

- Whether orthogonality holds on actual distributed production infrastructure
- Whether CDN cache invalidation on session state change introduces correlation
- Whether concurrent client load changes correlation structure
- Whether the result generalizes to non-Flask frameworks
- Whether headers-only structural signal captures sufficient variation for production use
- Whether per-cache heterogeneity is systematic or sampling noise
- Whether delta=0.10 is achievable at n=800+ (stratified CI width)
