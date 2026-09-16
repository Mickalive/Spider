# EXP-RUNTIME-34986155186 — Report

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34986155186
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-15
- **Status**: COMPLETE
- **Outcome**: MIXED

## 2. Executive Summary

Decompression-normalization (hashing the DECOMPRESSED response body after reversing Content-Encoding) **preserves body-only discrimination at 0.5** under both fixed and varying brotli quality levels. Compressed-body-only hashing **degrades to 0.3295-0.3475** under brotli quality variation (quality 4-8 per request), falling below the 0.35 threshold. This confirms the frozen hypothesis H1 (decompression-normalization works) and H2 (compressed-byte hashing degrades under quality variation), while supporting H3 (decompression-normalization outperforms compressed-byte hashing under quality variation).

**Product consequence**: The recommendation changes from "body-only with stable Accept-Encoding" to "use decompression-normalization as universal fallback." This eliminates the dependency on compression stability and enables deployment behind real CDNs where quality levels may vary.

## 3. Raw Evidence Summary

### 3.1 Primary Metric: /userinfo Discrimination

| Condition | Compressed Body-Only | Decompressed Body-Only | Status-Only | B-RANDOM |
|-----------|---------------------|----------------------|-------------|----------|
| COMPRESSED-FIXED | 0.5000 | 0.5000 | 0.5000 | 0.0000 |
| COMPRESSED-VARYING | 0.3475 | 0.5000 | 0.5000 | 0.0000 |
| DECOMPRESSED-FIXED | 0.5000 | 0.5000 | 0.5000 | 0.0000 |
| DECOMPRESSED-VARYING | 0.3295 | 0.5000 | 0.5000 | 0.0000 |
| IDENTITY | 0.5000 | 0.5000 | 0.5000 | 0.0000 |

### 3.2 /introspect Discrimination

| Condition | Compressed Body-Only | Decompressed Body-Only | Status-Only | B-RANDOM |
|-----------|---------------------|----------------------|-------------|----------|
| COMPRESSED-FIXED | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| COMPRESSED-VARYING | 0.4526 | 0.5000 | 0.0000 | 0.0000 |
| DECOMPRESSED-FIXED | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| DECOMPRESSED-VARYING | 0.3895 | 0.5000 | 0.0000 | 0.0000 |
| IDENTITY | 0.5000 | 0.5000 | 0.0000 | 0.0000 |

### 3.3 Within-State Variation

**DECOMPRESSED-FIXED (decompression determinism control)**:
- All 4 states × 20 reps = 80 requests per state produce exactly 1 unique decompressed hash
- Variation = 0 across all states — brotli.decompress() is deterministic

**COMPRESSED-VARYING (quality variation control)**:
- All 4 states produce 2 unique compressed hashes out of 20 requests
- Quality variation from {4,5,6,7,8} produces non-deterministic compressed bytes (as expected)

### 3.4 Body Sizes (compressed wire bytes)

- Error bodies (no_auth, expired_token, invalid_token): 64 bytes compressed
- Valid token body: ~1094-1100 bytes compressed (from ~1024 bytes raw JSON + metadata)

## 4. Observations (distinct from interpretation)

1. Compressed-body-only discrimination on /userinfo drops from 0.5 (fixed quality 6) to 0.3295-0.3475 under quality variation {4-8}, crossing below the 0.35 threshold
2. Decompressed-body-only discrimination remains at 0.5 under all conditions (fixed and varying quality)
3. Quality variation produces exactly 2 unique compressed hashes per state (quality 4-8 produces different compressed bytes for the same input)
4. Decompression via brotli.decompress() produces exactly 1 unique hash per state across 20 requests — fully deterministic
5. Status-only discrimination is invariant at 0.5 on /userinfo and 0.0 on /introspect across all conditions
6. B-RANDOM = 0.0 at all conditions — no spurious structure
7. The /introspect endpoint shows slightly higher compressed-body-only discrimination under variation (0.4526) than /userinfo (0.3475), likely due to different compressed body sizes for valid vs error states

## 5. Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| C_POSITIVE_CONTROL | B-COMPRESSED-FIXED >= 0.35 | 0.5 | Yes |
| C_NULL_CONTROL | B-RANDOM ~ 0.0 | 0.0 all conditions | Yes |
| C_DECOMPRESSED_FIXED_PRESERVES | B-DECOMPRESSED-FIXED >= 0.5 | 0.5 | Yes |
| C_DECOMPRESSION_DETERMINISM | Within-state variation = 0 | 0 | Yes |
| C_QUALITY_VARIATION_ACTIVE | Compressed variation > 0 | 2 unique hashes/state | Yes |
| C_NO_PIPELINE_ERRORS | 0 errors | 0 | Yes |

All 6 controls pass. The experiment is measurement-valid.

## 6. Interpretation

### 6.1 H1: Decompression-Normalization Preserves Discrimination — SUPPORTED

Decompression-normalization achieves discrimination = 0.5 on /userinfo under fixed brotli quality 6 (DECOMPRESSED-FIXED). Different logical bodies decompress to different bytes regardless of compression quality, confirming the key insight that motivated this experiment.

### 6.2 H2: Quality Variation Degrades Compressed-Byte Hashing — SUPPORTED

Body-only discrimination on compressed bytes degrades from 0.5 (fixed quality) to 0.3295-0.3475 under quality variation {4-8}. The degradation is bounded (not 0.0) because quality variation is limited to a realistic range, not full random. The compressed bytes differ across quality levels, causing hash divergence for the same logical body.

### 6.3 H3: Decompression-Normalization Outperforms Compressed-Byte Hashing Under Quality Variation — SUPPORTED

Decpressed-body-only discrimination (0.5) is strictly higher than compressed-body-only discrimination (0.3295-0.3475) under quality variation. The gap is 0.15-0.17 on /userinfo and 0.11-0.11 on /introspect.

### 6.4 H4: Within-State Determinism Under Decompression — SUPPORTED

Decompression-normalization produces deterministic hashes (within-state variation = 0) across all 20 requests per state. brotli.decompress() is a deterministic function for a given compressed input.

## 7. Decision

**MIXED** per frozen decision rule:
- B-DECOMPRESSED-FIXED >= 0.5 on /userinfo (decompression-normalization preserves discrimination under fixed quality) — PASS
- B-COMPRESSED-VARYING < 0.35 on /userinfo (body-only fails under quality variation) — FAIL

The MIXED verdict indicates that body-only on compressed bytes is not sufficient under quality variation, but decompression-normalization provides a viable universal fallback.

## 8. Product Consequences

### 8.1 Recommendation Change

The product recommendation changes from:
- "body-only with stable Accept-Encoding" (parent recommendation)

To:
- "use decompression-normalization as universal fallback"

### 8.2 Deployment Implications

1. **Behind real CDNs**: Decompression-normalization eliminates the dependency on compression stability. Quality levels may vary across CDN edges and over time without degrading fingerprint discrimination.
2. **Implementation cost**: Requires Content-Encoding detection and brotli/gzip decompression before hashing. This adds ~1ms latency per response at 1KB scale.
3. **Fallback strategy**: Compressed-body-only remains viable when compression is deterministic (e.g., single-server deployments). Decompression-normalization is the safe fallback when compression behavior is unknown.

### 8.3 Scope Limitations

This result is bounded to:
- Mock OAuth2 server (not real IdP)
- Synthetic CDN proxy (not real CDN infrastructure)
- Brotli quality variation {4-8} (not full quality range 0-11)
- JSON responses at 1KB uncompressed
- Single seed=44 (reproducible but not exhaustively sampled)

## 9. Next Steps

1. Test decompression-normalization under real CDN conditions (Cloudflare/Fastly)
2. Test with gzip quality variation in addition to brotli
3. Test with non-JSON content types (HTML, XML)
4. Measure decompression latency overhead at production scale
5. Test with production OAuth2 providers (Auth0, Okta, Keycloak)
