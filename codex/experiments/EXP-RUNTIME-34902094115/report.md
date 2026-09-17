# EXP-RUNTIME-34902094115 — Execution Report

## 1. Experiment Summary

**Experiment ID**: EXP-RUNTIME-34902094115
**Lane**: Runtime
**Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
**Status**: COMPLETE
**Outcome**: SUPPORTS

## 2. Scientific Question

Does body-only HTTP fingerprint discrimination survive deterministic CDN compression when response body sizes increase from 0-729 bytes to KB-scale JSON (1KB, 10KB, 100KB)?

## 3. Key Results

### Primary Finding

Body-only discrimination is **fully preserved at 0.5** across all three body sizes (1KB, 10KB, 100KB) under all three compression conditions (brotli, gzip, identity). Within-state body hash variation is **zero** across all 10 repetitions for every state, confirming code-level determinism of both brotli (quality 6) and gzip (level 9, mtime=0) at KB-scale.

### Decision Rule Assessment

All 8 conditions for SURVIVES_CURRENT_TEST are met at every body size:

| Control | 1KB | 10KB | 100KB |
|---------|-----|------|-------|
| C1: Positive (identity >= 0.35) | 0.5 PASS | 0.5 PASS | 0.5 PASS |
| C2: Null (B-RANDOM ~ 0.0) | 0.0 PASS | 0.0 PASS | 0.0 PASS |
| C3: Deterministic brotli preserves | 0.5 PASS | 0.5 PASS | 0.5 PASS |
| C4: Deterministic gzip preserves | 0.5 PASS | 0.5 PASS | 0.5 PASS |
| C5: Within-state deterministic | True PASS | True PASS | True PASS |
| C6: Mixed-client degrades | 0.224 PASS | 0.224 PASS | 0.224 PASS |
| C7: Status-only invariant | 0.5 PASS | 0.5 PASS | 0.5 PASS |
| C8: No pipeline errors | 0 PASS | 0 PASS | 0 PASS |

## 4. Determinism Verification

Within-state compressed body hash variation is **0/10 across all 120 state x profile x size cells**. This confirms:

- Python `brotli.compress(data, quality=6)` is a deterministic function: same input always produces identical compressed bytes
- Python `gzip.GzipFile(compresslevel=9, mtime=0)` is deterministic: mtime=0 eliminates timestamp non-determinism
- Both algorithms produce identical compressed output for the same logical body regardless of body size (1KB through 100KB)

## 5. Cross-Client Divergence

Mixed-client discrimination (Client A brotli + Client C identity alternating) drops to **0.2237** from 0.5 single-client at all body sizes. This confirms:

- Different Accept-Encoding headers cause the CDN to select different compression algorithms
- Different algorithms produce different compressed bytes for the same logical body
- Body hash computed on compressed wire bytes therefore diverges across clients
- The divergence is consistent across 1KB, 10KB, and 100KB body sizes

## 6. Compression Ratios

Observed compressed body sizes (valid_token state, /userinfo endpoint):

| Algorithm | 1KB raw | 1KB compressed | 10KB raw | 10KB compressed | 100KB raw | 100KB compressed |
|-----------|---------|----------------|----------|-----------------|-----------|------------------|
| brotli | 2060 | 1094 | 20492 | 11001 | 204812 | 112854 |
| gzip | 2060 | 1186 | 20492 | 11936 | 204812 | 117211 |
| identity | 2060 | 2060 | 20492 | 20492 | 204812 | 204812 |

Compression ratios are roughly 47% (brotli) and 42% (gzip) for random data. These are consistent across repetitions, confirming determinism.

## 7. Interpretation

The substrate ceiling established by EXP-RUNTIME-34741873198 (body-only at 0.5 for 0-729 bytes) is now **extended to at least 100KB JSON responses**. The critical finding is that body-only discrimination is not affected by body size under deterministic compression:

1. **Deterministic compression is size-invariant**: brotli quality 6 and gzip level 9 (mtime=0) produce identical compressed bytes for the same logical body regardless of whether the body is 1KB or 100KB
2. **Body-only discrimination is robust**: compression does not introduce noise that would reduce discrimination at larger body sizes
3. **Cross-client divergence is real at all sizes**: different compression algorithms consistently produce different hashes, confirming this is an intrinsic property of compression, not a size-dependent artifact

## 8. Product Consequences

### Positive Consequence (achieved)

Body-only discrimination survives deterministic CDN compression at KB-scale JSON responses (up to 100KB). SPIDER can use body-only as the default production fingerprint strategy for endpoints returning JSON responses up to 100KB without compression-normalization overhead, provided the client's Accept-Encoding is stable. The EXP-RUNTIME-34741873198 body-only recommendation is strengthened for realistic API response sizes.

### What This Does NOT Establish

- This experiment tests a synthetic deterministic proxy, not a real CDN. Real CDNs may have additional non-determinism.
- Results apply to deterministic brotli (quality 6) and gzip (level 9, mtime=0). Other quality levels may behave differently.
- Body-only is NOT incremental over status-only on /userinfo where status codes discriminate (0.5 both).
- Body-only IS incremental over status-only on /introspect where all states return HTTP 200 (0.5 vs 0.0).

## 9. Validity Notes

- Mock OAuth2 server (not Keycloak) returning JSON with random data field
- Same fingerprint algorithm as parent: SHA-256(repr((status, body_sha256, '')))
- Proxy configured per client profile to apply fixed algorithm (not per-request header negotiation)
- Body hash computed on compressed bytes received by client (not raw bytes from server)
- Python gzip is deterministic: same input + same level = same output (mtime=0 eliminates timestamp non-determinism)
- Python brotli is deterministic: same input + same level = same output
- Body-only discrimination is NOT tautological — compression directly attacks the body hash
- expired_token is locally-signed HS256, not real expired token

## 10. Unresolved Questions

1. Does body-only discrimination survive a real CDN (Cloudflare/Fastly/Akamai)?
2. Does the result generalize to larger/more diverse body content-types beyond JSON?
3. What discrimination floor remains when hashing decompressed bodies (normalization layer)?
4. Would a filtered full-vector baseline survive compression?
5. Does result generalize to production OAuth2 with real CDN and load-balancer?
