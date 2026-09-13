# EXP-RUNTIME-34654566605 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34654566605
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Parent**: EXP-RUNTIME-34509593940 (body-only invariance under header noise)
- **Date**: 2026-09-11
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does body-only HTTP fingerprint discrimination survive CDN-style compression where response bodies are recompressed non-deterministically (varying compression algorithm and parameters per request), causing the compressed body hash to differ per request even for identical logical responses?

## 3. Motivation

The parent experiment (EXP-RUNTIME-34509593940) established that body-only discrimination (status + body hash) is invariant under synthetic header noise, while full-vector discrimination collapses. However, the parent's body-only invariance was **tautological by construction**: the proxy preserved response bodies and only modified headers, so the body hash was unchanged by definition (audit V2, prereg 12.6).

CDN compression is a materially orthogonal threat: it directly modifies the response body bytes that the client receives, causing the compressed body hash to vary per request even for identical logical content. This is the critical unresolved threat carried from the parent's `unknown` and `do_not_assume` categories:

- Unknown: "Does body-only discrimination survive CDN compression (Content-Encoding gzip/br) where response bodies are non-deterministically compressed, causing body hash to vary per request even for identical logical responses?"
- Do-not-assume: "Do not assume body-only recommendation from EXP-RUNTIME-34439061845 is production-ready — it survives only under synthetic header noise; CDN compression remains an open threat"

Real CDNs (Cloudflare, Akamai, AWS CloudFront) vary compression based on:
- Client Accept-Encoding header (gzip vs br vs identity)
- Server-side compression level selection (gzip level 1-9)
- Resource constraints and load
- Response content type and size

If compression is non-deterministic, the same logical response produces different compressed bytes, different body hashes, and body-only discrimination collapses. This experiment directly tests this threat.

## 4. Hypotheses

### H1: Compression Degradation
Body-only discrimination degrades monotonically with compression variability: identity (no variation) > fixed gzip (deterministic) > random gzip level (parameter variation) > random algorithm (algorithm variation). Spearman rho between body-only discrimination and compression variability level <= -0.3.

### H2: Fixed Compression Preserves Discrimination
Fixed gzip level 9 compression produces deterministic output for the same logical body, so compressed body hash is stable and body-only discrimination is preserved (within 0.15 of uncompressed).

### H3: Multi-Algorithm Is More Destructive Than Single-Algorithm
Random algorithm (gzip/brotli/identity) produces more body hash variation than random gzip level alone, because different algorithms produce fundamentally different byte sequences for the same input.

### H4: Positive Control
Body-only discrimination at uncompressed level (identity) >= 0.35 on /userinfo, confirming the measurement pipeline produces the expected 3-group body pattern (valid JSON vs empty vs empty).

### H5: Null Control
B-RANDOM discrimination ~ 0.0 at all compression levels, confirming no spurious structure.

## 5. Data Collection

### 5.1 Infrastructure

- Keycloak 25.0 start-dev via Docker on localhost:18080 (same as parent experiments)
- Compression proxy on localhost:18081, forwarding to Keycloak on 18080
- 4 auth states: no_auth, valid_token, expired_token, invalid_token (same as parent)

### 5.2 Compression Proxy Design

The proxy intercepts HTTP responses from Keycloak and applies compression before forwarding to the client. The proxy:

1. Receives the raw (uncompressed) response from Keycloak
2. Determines the compression condition for this request (based on compression level and RNG)
3. Compresses the response body using the determined algorithm/parameters
4. Sets the Content-Encoding header to match the applied compression
5. Forwards the compressed response to the client

**Critical design choice**: The proxy overrides the client's Accept-Encoding header and applies its own compression per the experimental condition. This ensures non-deterministic compression is applied regardless of client preferences, simulating CDN behavior where the CDN controls compression.

**Body hash computation**: The client (measurement code) computes the body hash on the compressed bytes it receives, not the raw uncompressed bytes from Keycloak. This is the correct measurement because SPIDER in production would see compressed bytes from a CDN.

### 5.3 Compression Levels (4 conditions)

- **Level 0 (identity)**: No compression. Response forwarded as-is. Content-Encoding: identity or absent. Body hash is deterministic (same raw bytes every request).
- **Level 1 (fixed-gzip)**: Always gzip compression level 9. Content-Encoding: gzip. Body hash is deterministic (same compressed output for same input).
- **Level 2 (random-level)**: Random gzip compression level 1-9 per request. Content-Encoding: gzip. Body hash MAY vary (different compression levels produce different output bytes for the same input).
- **Level 3 (random-algo)**: Random choice per request: gzip (random level 1-9), brotli (if available, level 1-6), or identity. Content-Encoding: gzip, br, or absent. Body hash DEFINITELY varies (different algorithms produce fundamentally different byte sequences).

### 5.4 Sample Size

- 4 auth states × 10 requests × 4 compression levels × 2 endpoints = 320 total requests
- 10 requests per auth state per compression level per endpoint
- Same as parent (320 requests) for comparability

### 5.5 Randomization

- Seed=44 for compression level/algorithm selection per request (deterministic, same seed as parent for comparability)
- Jitter: 50-150ms uniform between requests (same as parent)

## 6. Fingerprint Algorithms

### 6.1 Body-Only (Primary)

```
compressed_body = response.body  # bytes received by client (compressed)
body_sha256 = sha256(compressed_body).hexdigest()
fingerprint = sha256(repr((status, body_sha256, ''))).hexdigest()
```

The body hash is computed on the compressed bytes, not the raw bytes. This is the correct measurement for production CDN environments.

### 6.2 Status-Only (Baseline)

```
fingerprint = sha256(repr((status, '', ''))).hexdigest()
```

### 6.3 Random (Null Baseline)

```
fingerprint = sha256(random.getrandbits(256).to_bytes(32, 'big')).hexdigest()
```

## 7. Metrics

### 7.1 Primary Metric: M_COMPRESSION_DEGRADATION

Spearman rank correlation between compression variability level [0, 1, 2, 3] and body-only discrimination on /userinfo. Threshold: rho <= -0.3 (monotonic degradation).

### 7.2 Body-Only Discrimination Per Level

For each compression level l in {0, 1, 2, 3}:
- Compute body-only fingerprints for all requests at that level on /userinfo
- Compute discrimination = intra_match_rate - inter_match_rate
- Report discrimination score

### 7.3 Body Hash Variation Metric

For each compression level l and each auth state s:
- Compute body_sha256 for all 10 requests
- Count unique body_sha256 values (should be 1 for deterministic compression, >1 for non-deterministic)
- Report per-state hash uniqueness

### 7.4 Positive Control: M_POSITIVE_CONTROL

Body-only discrimination at compression level 0 (identity) on /userinfo. Threshold: >= 0.35.

### 7.5 Null Control: M_NULL_CONTROL

B-RANDOM discrimination at compression level 0 on /userinfo. Threshold: ~0.0.

## 8. Baselines

| Baseline | Description | Expected |
|----------|-------------|----------|
| B-UNCOMPRESSED-BODY-ONLY | Body-only at level 0 (identity) | >= 0.35 (3 body groups) |
| B-FIXED-GZIP-BODY-ONLY | Body-only at level 1 (fixed gzip 9) | ≈ uncompressed body-only |
| B-RANDOM-LEVEL-BODY-ONLY | Body-only at level 2 (random gzip 1-9) | < fixed-gzip (degraded) |
| B-RANDOM-ALGO-BODY-ONLY | Body-only at level 3 (random algo) | < random-level (most degraded) |
| B-RANDOM | Random fingerprint | ~ 0.0 |
| B-STATUS-ONLY | Status code only | 0.5 on /userinfo, invariant |

## 9. Controls

### 9.1 Positive Control (Level 0)
Body-only discrimination at identity (no compression) >= 0.35 on /userinfo. Verifies pipeline produces expected 3-group pattern before compression is applied.

### 9.2 Null Control (All Levels)
B-RANDOM ~ 0.0 at all compression levels. Verifies pipeline does not produce spurious structure from compression artifacts.

### 9.3 Fixed Compression Control (Level 1)
Body-only at fixed gzip >= uncompressed body-only - 0.15. Verifies deterministic compression preserves body hash stability.

### 9.4 Compression Application Verification
For levels 1-3, verify Content-Encoding header matches applied compression and compressed body bytes differ from raw body bytes (compression is actually applied, not just header labeling).

## 10. Validity Threats

### 10.1 Compression Module Availability
brotli Python module may not be installed. Mitigation: fallback to gzip-only for level 3 (random level within gzip), document limitation. If brotli unavailable, level 3 becomes "random gzip level" which is less non-deterministic than intended — report and adjust interpretation.

### 10.2 Gzip Determinism
Python gzip module is deterministic: same input + same level = same output. This is the expected behavior for level 1 (fixed-gzip). For level 2 (random-level), different levels produce different output bytes, which is the intended non-determinism source. If gzip output is unexpectedly identical across levels for small bodies, the degradation signal may be weaker than expected — report compressed body sizes.

### 10.3 Body Size Effects
Small response bodies (e.g., empty JSON for expired/invalid tokens) may have compression output that varies less across levels/algorithms than large bodies. Report per-state body sizes and compressed sizes.

### 10.4 Proxy Fidelity
The proxy decompresses (if Keycloak sends compressed) and recompresses. If Keycloak sends uncompressed (likely for localhost start-dev), the proxy compresses raw bytes directly. Verify Keycloak sends uncompressed by checking Content-Encoding on direct requests.

### 10.5 Sample Size
10 requests per cell is small for estimating body hash variation. With N=10, unique hash count of 1-2 may reflect limited sampling. Report exact unique counts and acknowledge limited power for low-variation conditions.

### 10.6 Expired Token Construction
expired_token is locally-signed HS256, not Keycloak-issued (V6 state construction leakage carried from parent). This does not affect compression measurement (compression applies to response body regardless of token validity).

### 10.7 Tautology Disclosure
Unlike the parent's header-noise invariance (which was tautological), compression non-determinism directly attacks the body hash. If body-only discrimination survives, it is NOT tautological — it would mean compression output is more deterministic than assumed. If it degrades, it confirms the hypothesized threat. Either outcome is informative.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. M_POSITIVE_CONTROL >= 0.35 on /userinfo (body-only works without compression)
2. B-RANDOM ~ 0.0 at all compression levels (null control)
3. Body-only at fixed gzip >= uncompressed body-only - 0.15 on /userinfo (fixed compression preserves)
4. Spearman rho(M_BODY_ONLY_DISC, compression_variability_level) <= -0.3 on /userinfo (degradation under non-determinism)
5. Body-only at random-algo < body-only at fixed-gzip on /userinfo (multi-algorithm more destructive)
6. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If (4) fails: body-only does NOT degrade under non-deterministic compression. CDN compression is not a threat. Body-only architecture is validated for CDN environments. The parent's "do-not-assume" caution on CDN compression was overly conservative.

### 11.3 MEASUREMENT_INVALID
If (3) or (5) fails: body-only degrades under fixed deterministic compression or random-algo is not worse than fixed. This indicates the proxy is modifying body content beyond compression (e.g., re-encoding, truncation, header injection into body). Pipeline debugging required.

If (1) or (2) fails: baseline pipeline is broken. Not scientific evidence.

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Body-only discrimination degrades under non-deterministic compression
- Confirms CDN compression is a real threat to body-only architecture
- Product must either use compression-normalization, header-based fingerprinting, or restrict body-only to deterministic-compression environments
- The parent's body-only recommendation is bounded to non-CDN environments
- Claim ceiling for C-MEAS-VALID narrowed: body-only valid only when compression is deterministic or absent

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Body-only discrimination survives non-deterministic compression
- CDN compression is NOT a threat — body hash is stable across compression variations
- Possible explanations: (a) gzip/brotli output is more deterministic than assumed for small bodies, (b) compression level has minimal effect on small JSON responses, (c) body hash stability is a property of the content, not the compression
- Product can use body-only as default in CDN environments
- The parent's "do-not-assume" caution is resolved: body-only IS production-ready for CDN

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Proxy is modifying body content, not just compression
- Pipeline debugging required before this question can be answered
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Data Collection**: Collect 320 HTTP observations (4 states × 10 reps × 4 compression levels × 2 endpoints)
2. **Compression Verification**: For each request, verify Content-Encoding header matches condition and compressed body bytes differ from raw bytes
3. **Body Hash Extraction**: Compute body_sha256 on compressed bytes for each request
4. **Fingerprint Computation**: Compute body-only fingerprints: SHA-256(repr((status, body_sha256, '')))
5. **Discrimination Per Level**: For each compression level, compute intra_match_rate and inter_match_rate across auth states, then discrimination = intra - inter
6. **Hash Variation**: For each compression level and auth state, count unique body_sha256 values across 10 requests
7. **Spearman Correlation**: Compute rho between compression variability level [0,1,2,3] and body-only discrimination on /userinfo
8. **Controls**: Verify positive control (level 0 >= 0.35), null control (B-RANDOM ~ 0.0), fixed compression control (level 1 >= level 0 - 0.15)
9. **Report**: Report all metrics, controls, hash variation counts, compressed body sizes, and validity notes

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
