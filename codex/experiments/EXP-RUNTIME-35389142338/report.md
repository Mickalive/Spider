# EXP-RUNTIME-35389142338 Report

## Question

Does iterative decompression maintain discrimination when the CDN-like proxy cache is configured with auth-aware semantics (Cache-Control: private, Vary: Authorization, cache key includes Authorization) — resolving the parent's CACHED falsification from a cache-key configuration artifact into a genuine decompression test?

## Outcome: MIXED

All 6 controls pass. The MIXED outcome is caused by an internal contradiction in the frozen spec's decision rule: condition (1) requires decompressed discrimination >= 0.3 for ALL cells (including NAIVE), but condition (4) requires NAIVE discrimination = 0.0. Both conditions cannot be simultaneously satisfied. The scientific result is clear: auth-aware caching restores discrimination to 0.5.

## Key Findings

| Metric | NAIVE | AUTH-AWARE |
|--------|-------|------------|
| Decompressed discrimination (mean) | 0.0000 | 0.5000 |
| Compressed discrimination (mean) | 0.0000 | 0.5000 |
| All cells >= 0.3 threshold | No (0.0) | Yes (0.5) |
| B-RANDOM | 0.0 | 0.0 |
| Decompression errors | 0 | 0 |
| Hash determinism (within-state) | all_same=True | all_same=True |
| Hash match to direct server | N/A (wrong cached response) | Yes (all 36 checks) |

### Per-Cell Decompressed Discrimination

| Cell | NAIVE | AUTH-AWARE |
|------|-------|------------|
| JSON_1KB | 0.0 | 0.5 |
| JSON_10KB | 0.0 | 0.5 |
| JSON_100KB | 0.0 | 0.5 |
| HTML_1KB | 0.0 | 0.5 |
| HTML_10KB | 0.0 | 0.5 |
| HTML_100KB | 0.0 | 0.5 |
| XML_1KB | 0.0 | 0.5 |
| XML_10KB | 0.0 | 0.5 |
| XML_100KB | 0.0 | 0.5 |

## Controls

| Control | Pass | Description |
|---------|------|-------------|
| C_NULL_CONTROL | True | B-RANDOM = 0.0 for all conditions |
| C_NAIVE_CACHED_REPRODUCTION | True | NAIVE discrimination = 0.0 for all cells (reproduces parent) |
| C_AUTH_AWARE_PRIMARY | True | AUTH-AWARE discrimination >= 0.3 for all cells (min = 0.5) |
| C_DECOMPRESSED_DETERMINISM | True | Within-state decompressed hash all_same=True for all states |
| C_DETERMINISM_ACROSS_PATHS | True | AUTH-AWARE proxy decompressed hash matches direct-server hash |
| C_NO_ERROR_INFLATION | True | 0 decompression errors across all conditions |

## Decision Rule Analysis

The frozen spec's decision rule requires all of:

1. `min_decompressed_disc >= 0.3` for ALL cells → **FAILS** (NAIVE = 0.0)
2. Hash match with direct server → **PASSES**
3. B-RANDOM = 0.0 → **PASSES**
4. NAIVE = 0.0 (reproduces parent) → **PASSES**
5. No decompression crashes → **PASSES**
6. AUTH-AWARE >= 0.3 → **PASSES**

The contradiction: condition (1) requires NAIVE >= 0.3, but condition (4) requires NAIVE = 0.0. The spec was written before the two-config design was finalized. The MIXED outcome is the correct response to a contradictory decision rule.

## Interpretation

The scientific finding is unambiguous:

1. **Auth-aware caching fully restores discrimination**: AUTH-AWARE achieves 0.5 across all 9 content conditions (3 content types × 3 sizes), matching the parent's PASSTHROUGH and RECOMPRESS baselines.

2. **NAIVE caching reproduces the parent's failure**: 0.0 discrimination across all cells, confirming the parent's CACHED falsification was caused by the cache key excluding Authorization.

3. **The parent's CACHED falsification was a cache-key artifact**, not a decompression failure. When the cache key includes Authorization, each auth state receives its own cached response, and iterative decompression correctly distinguishes them.

4. **No decompression issues**: 0 errors across all 360 requests, deterministic hashes within all states, proxy-transparent body bytes.

## Product Implications

- Auth-aware caching (Cache-Control: private / Vary: Authorization with Authorization in cache key) is sufficient for iterative decompression to maintain discrimination.
- The real-CDN experiment can proceed with this cache configuration as the baseline.
- Edge-specific concerns (quality variation, Accept-Encoding negotiation) remain for the real-CDN experiment but the local validation is complete.

## Validity Notes

- Architecture: Client (iterative decompression, max_depth=5) → Python Reverse Proxy → Mock OAuth2 Server (brotli quality 6)
- Two cache configs: NAIVE (URL+Accept-Encoding) and AUTH-AWARE (URL+Accept-Encoding+Authorization)
- Origin sets Cache-Control: private, Vary: Authorization for all responses
- 360 total requests: 4 auth states × 9 conditions × 2 cache configs × 5 reps
- Seed=44 for request ordering (same as parent)
- Expired_token is locally-signed HS256, not real expired token
- Content types are synthetic but structurally realistic
- Proxy uses Content-Length forwarding (not chunked TE) — transparent passthrough

## Unresolved

1. Frozen spec decision rule contradiction (c1 vs c4) requires resolution before verdict
2. Real-CDN experiment remains needed for production deployment validation
3. Accept-Encoding negotiation with real CDN edge nodes not tested locally
4. Brotli quality variation across CDN nodes not tested locally
