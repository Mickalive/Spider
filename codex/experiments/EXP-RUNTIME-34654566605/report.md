# EXP-RUNTIME-34654566605 — Body-Only Fingerprint Under CDN Compression

## 1. Executive Summary

**Status**: COMPLETE
**Outcome**: SUPPORTS

This experiment tests whether body-only HTTP fingerprint discrimination survives 
CDN-style compression where response bodies are recompressed non-deterministically 
(varying compression algorithm and parameters per request).

## 2. Scientific Question

Does body-only HTTP fingerprint discrimination survive CDN-style compression where 
response bodies are recompressed non-deterministically, causing the compressed body 
hash to differ per request even for identical logical responses?

## 3. Primary Results

### 3.1 Body-Only Discrimination by Compression Level (/userinfo)

| Compression Level | Name | Body-Only | Status-Only | B-RANDOM |
|-------------------|------|-----------|-------------|----------|
| 0 | identity | 0.5000 | 0.5000 | 0.0000 |
| 1 | fixed-gzip-9 | 0.5000 | 0.5000 | 0.0000 |
| 2 | random-gzip-level | 0.3272 | 0.5000 | 0.0000 |
| 3 | random-algo | 0.0944 | 0.5000 | 0.0000 |

### 3.2 Body-Only Discrimination by Compression Level (/introspect)

| Compression Level | Name | Body-Only | Status-Only | B-RANDOM |
|-------------------|------|-----------|-------------|----------|
| 0 | identity | 0.5000 | 0.0000 | 0.0000 |
| 1 | fixed-gzip-9 | 0.5000 | 0.0000 | 0.0000 |
| 2 | random-gzip-level | 0.1828 | 0.0000 | 0.0000 |
| 3 | random-algo | 0.1272 | 0.0000 | 0.0000 |

### 3.3 Derived Metrics

- **M_COMPRESSION_DEGRADATION** (Spearman rho: body-only vs compression level on /userinfo): -0.9487 (p=0.0513)
  - Threshold: <= -0.3
  - PASS

- **M_POSITIVE_CONTROL** (body-only at level 0 on /userinfo): 0.5000
  - Threshold: >= 0.35
  - PASS

- **M_NULL_CONTROL** (B-RANDOM at level 0 on /userinfo): 0.0000
  - Threshold: ~ 0.0
  - PASS

- **M_FIXED_GZIP_CONTROL** (fixed-gzip vs uncompressed): 0.5000 vs 0.5000
  - Threshold: fixed_gzip >= uncompressed - 0.15
  - PASS

- **M_RANDOM_ALGO_VS_FIXED** (random-algo vs fixed-gzip): 0.0944 vs 0.5000
  - Threshold: random-algo < fixed-gzip
  - PASS

## 4. Body Hash Variation

| Compression Level | Unique Hashes | Total Requests | All Same |
|-------------------|---------------|----------------|----------|
| 0 (identity) | 4 | 40 | True |
| 1 (fixed-gzip-9) | 4 | 40 | True |
| 2 (random-gzip-level) | 9 | 40 | False |
| 3 (random-algo) | 15 | 40 | False |

## 5. Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| C_POSITIVE_CONTROL | M_BODY_ONLY_DISC_LEVEL0 >= 0.35 | 0.5 | PASS |
| C_NULL_CONTROL | B-RANDOM ~ 0.0 | 0.0 | PASS |
| C_FIXED_GZIP_PRESERVES | body_only(level=1) >= body_only(level=0) - 0.15 | 0.5 | PASS |
| C_COMPRESSION_DEGRADATION | Spearman rho(BODY_ONLY_DISC, compression_level) <= -0.3 | -0.9486832980505139 | PASS |
| C_RANDOM_ALGO_WORSE | body_only(random-algo) < body_only(fixed-gzip) | 0.09444444444444447 | PASS |
| C_NO_PIPELINE_ERRORS | 0 errors | 0 | PASS |

## 6. Interpretation

All controls pass. Body-only discrimination degrades monotonically under 
non-deterministic compression (Spearman rho <= -0.3). Fixed deterministic 
compression preserves discrimination, while random-level and random-algo 
compression degrade it. Multi-algorithm compression is more destructive than 
single-algorithm.

**Product consequence**: Body-only discrimination degrades under CDN-style 
compression non-determinism. Body-only architecture is NOT production-ready 
for CDN-proxied environments. SPIDER must either:
(a) use a compression-normalization layer that decompresses before hashing,
(b) use header-based or filtered-full-vector fingerprinting instead of body-only, or
(c) restrict body-only to environments where compression is deterministic.

The body-only recommendation from EXP-RUNTIME-34509593940 is bounded to 
uncompressed or deterministic-compression environments only.

## 7. Validity Notes

- Same Keycloak 25.0 Docker deployment as parent experiments
- Same fingerprint algorithm: SHA-256(repr((status, body_sha256, '')))
- Python version: 3.12.14 (main, Aug 13 2026, 02:47:42) [GCC 13.3.0]
- Jitter: 50-150ms uniform between requests
- expired_token is locally-signed HS256, not Keycloak-issued (V6 leakage from parent)
- Brotli module available: True
- Proxy decompresses (if Keycloak sends compressed) and recompresses per condition
- Proxy overrides client Accept-Encoding to identity to get raw response from Keycloak
- Body hash computed on compressed bytes received by client (not raw bytes from Keycloak)
- Body-only discrimination is NOT tautological here — compression directly attacks the body hash
- Seed=44 for compression selection (deterministic across runs)
- **DEV FIX**: gzip mtime=0 used to eliminate gzip header timestamp as non-determinism source; real CDNs also produce deterministic compressed output for same logical body (strip metadata timestamps); this isolates compression algorithm/level effect being tested
- **DEV FIX**: Raw compressed bytes captured via resp.raw.read(decode_content=False) instead of resp.content (which auto-decompresses); correct measurement because SPIDER sees wire bytes from CDN, not decompressed bytes
- Analysis performed on raw_observations.json collected by run_experiment.py

## 8. Unresolved Questions

- Does body-only discrimination survive multiple stacked infrastructure layers with correlated compression?
- Does the result generalize to non-Keycloak OAuth/OIDC providers?
- What is the discrimination floor when bodies are compressed non-deterministically?
- Would a filtered full-vector baseline (status+WWW-Authenticate+Cache-Control+body_hash) survive compression?

## 9. Decision

**Verdict**: SUPPORTS — COMPLETE

The frozen decision rule from spec.json determines the verdict based on the 
six controls evaluated above.