# EXP-RUNTIME-35137033384 — Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-35137033384
- **Lane**: runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Parent**: EXP-RUNTIME-35130682006 (brotli quality range fix, SURVIVES_CURRENT_TEST with audit REVISE)
- **Design date**: 2026-09-16
- **Mode**: DESIGN only (no outcome-bearing measurements)

## 2. Question

Does decompression-normalization (SHA256 on decompressed body + status) preserve body-only discrimination under realistic CDN-like non-determinism simulated via a CDN-noise proxy layer?

## 3. Hypotheses

**H1** (primary): Decompression-normalization preserves discrimination >= 0.5 on /userinfo under CDN-like non-determinism (varying brotli quality, chunked transfer-encoding, CDN headers, Accept-Encoding negotiation, response caching) because `brotli.decompress()` reverses any valid brotli compression regardless of quality level, and the decompressed logical body is invariant under these CDN transformations.

**H2**: Algorithm-equivalence between brotli and gzip decompression-normalization holds (|diff| < 0.1) under CDN noise because both algorithms decompress to the same logical body; CDN noise affects compressed wire bytes but not decompressed bytes.

**H3**: Compressed-byte-only hashing degrades under CDN-like non-determinism to < 0.35 on /userinfo because varying quality + chunked encoding + caching produce different compressed wire bytes for the same logical body.

## 4. CDN-Noise Proxy Design

The CDN-noise proxy sits between the HTTP client and the mock OAuth2 server (port 5000). It intercepts every response from the mock server and applies6 categories of CDN-like non-determinism before returning it to the client.

### 4.1 brotli Quality Variation

Each response is compressed with brotli at a quality level randomly selected from {4,5,6,7,8} using a per-request random draw from a seeded RNG. This simulates per-edge quality selection where different CDN edges or cache states produce different compression levels for the same content.

**Rationale**: The parent handoff identifies per-edge brotli quality as the primary non-determinism source. Prior experiments used fixed quality per condition; this varies quality per request.

### 4.2 Chunked Transfer-Encoding

Approximately 30% of responses (random draw per request) are wrapped in HTTP chunked transfer-encoding before being returned to the client. The compressed body is split into chunks of 1-4 KB with proper chunk framing (`{size_hex}\r\n{data}\r\n...0\r\n\r\n`).

**Rationale**: Real CDNs frequently use chunked transfer-encoding, especially for responses where the final size is not known at the start of transmission. This tests whether the decompression pipeline correctly handles chunked framing before brotli decompression.

### 4.3 CDN-Specific Response Headers

Every response receives CDN-specific headers that vary per request:
- `CF-Ray`: random hex string (simulates Cloudflare request ID)
- `X-Cache`: randomly "HIT" or "MISS" (simulates cache status)
- `Age`: random integer 0-300 (simulates cached response age in seconds)
- `Via`: "1.1 varnish" (simulates CDN proxy chain)

**Rationale**: Real CDNs inject response headers that change per request. These headers should not affect decompression-normalization because the hash is computed on the decompressed body + status, not on headers. This control verifies header non-interference.

### 4.4 Accept-Encoding Negotiation

The CDN-noise proxy occasionally overrides the client's Accept-Encoding preference:
- 20% of requests: CDN responds with `Content-Encoding: gzip` instead of `br`, compressing the body with gzip (level 9) regardless of client preference
- 5% of requests: CDN responds with no Content-Encoding (identity), returning the uncompressed body

**Rationale**: Real CDNs negotiate compression based on their own policies, edge capabilities, and cache state. The client may advertise `br` but receive `gzip` or uncompressed. Decompression-normalization must handle all three cases by checking Content-Encoding and decompressing accordingly.

### 4.5 Response Caching

The CDN-noise proxy maintains a simple in-memory cache keyed by (path, auth-state). Approximately 30% of requests are served from cache, returning a previously stored response with modified CDN headers (X-Cache: HIT, Age > 0). The cached response preserves the original compression and encoding.

**Rationale**: Real CDNs cache responses and serve them to subsequent requests. Cache hits return identical wire bytes but different CDN headers. This tests whether decompression-normalization handles cache consistency (same logical body, same decompressed bytes, different wire representation).

### 4.6 Content-Length Variation

When chunked transfer-encoding is applied, the Content-Length header is omitted (as required by HTTP spec). When identity encoding is used, Content-Length reflects the uncompressed size. When brotli/gzip is used, Content-Length reflects the compressed size.

**Rationale**: Real CDNs produce varying Content-Length values depending on encoding. This is a passive consequence of the other noise sources, not an independent manipulation.

### 4.7 Implementation Constraints

- CDN-noise proxy runs on localhost (no network non-localhost variability)
- All noise parameters are controlled by a seeded RNG for reproducibility
- The proxy is a simple HTTP forward proxy or reverse proxy (not a full CDN)
- The mock OAuth2 server is unchanged from parent (Flask + PyJWT, same4 auth states)

## 5. Baselines

| Baseline ID | Description | Expected /userinfo | Source |
|---|---|---|---|
| B-DECOMPRESSED-VARYING-BROTLI-CDN | Decompressed body hash under CDN-noise proxy (brotli quality {4,5,6,7,8} + chunked + headers + caching + Accept-Encoding negotiation) | >= 0.5 | THIS EXPERIMENT |
| B-COMPRESSED-VARYING-BROTLI-CDN | Compressed-byte-only hashing under CDN-noise proxy | < 0.35 (H3) | THIS EXPERIMENT |
| B-DECOMPRESSED-VARYING-GZIP | Decompressed body hash under gzip {1,3,5,7,9} | 0.5 | PARENT reference |
| B-STATUS-ONLY | Status code discrimination | 0.5 | PARENT reference |
| B-RANDOM | Random fingerprint (null) | ~0.0 | PARENT reference |

## 6. Controls

| Control | Type | Expected | Pass criterion |
|---|---|---|---|
| C_DECOMPRESSION_DETERMINISM | Positive | Within-state decompressed hash variation = 0 for all states under CDN-noise | All4 states x 2 endpoints: 0/20 variation |
| C_NULL_CONTROL | Null | B-RANDOM ~ 0.0 at all conditions | Mean < 0.01 |
| C_CDN_NOISE_ACTIVE | Positive | Compressed-byte hashes vary across requests for same logical body | Compressed hash variation > 1 for at least 1 state |
| C_ALGORITHM_EQUIVALENCE | Positive | \|B-DECOMPRESSED-VARYING-GZIP(parent) - B-DECOMPRESSED-VARYING-BROTLI-CDN\| < 0.1 | diff < 0.1 |

## 7. Metrics

### Primary

- **discrimination**: Jaccard distance between fingerprint sets across auth states, computed as `mean_{i!=j} |F_i XOR F_j| / |F_i UNION F_j|` where F_i is the set of fingerprints for auth state i. Reported per endpoint (/userinfo, /introspect) and per baseline.

- **within_state_variation**: For each (endpoint, state, baseline): fraction of requests where the fingerprint differs from the first request for that state. Expected = 0 for decompression-normalization, > 0 for compressed-byte-only.

### Secondary

- **compressed_hash_variation**: Number of distinct compressed-body hashes per state under CDN-noise proxy. Expected > 1 (CDN noise produces different compressed bytes).

- **decompressed_hash_variation**: Number of distinct decompressed-body hashes per state under CDN-noise proxy. Expected = 0 (decompression-normalization produces identical bytes).

- **algorithm_equivalence_diff**: |B-DECOMPRESSED-VARYING-GZIP(parent) - B-DECOMPRESSED-VARYING-BROTLI-CDN|. Expected < 0.1.

## 8. Sample Size

- N = 20 requests per auth state per endpoint
- 4 auth states x 2 endpoints x 20 reps = 160 requests for B-DECOMPRESSED-VARYING-BROTLI-CDN
- 160 requests for B-COMPRESSED-VARYING-BROTLI-CDN
- Total: 320 requests (plus reference data from parent, not re-executed)

## 9. Randomization

- **Seed**: 44 (frozen from parent, for reproducibility)
- **CDN noise seed**: derived as `seed + hash("CDN_NOISE") % 10000` using deterministic hashlib (fixes parent audit finding V_HASH_NON_DETERMINISM)
- **Quality selection**: uniform random from {4,5,6,7,8} per request using seeded numpy RNG
- **Chunked encoding**: Bernoulli(0.3) per request using seeded numpy RNG
- **Accept-Encoding override**: Bernoulli(0.2) for gzip override, Bernoulli(0.05) for identity, using seeded numpy RNG
- **Cache hit**: Bernoulli(0.3) per request using seeded numpy RNG

## 10. Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:
1. Within-state decompressed hash variation = 0 for all states (positive control passes)
2. B-RANDOM ~ 0.0 (null control passes)
3. B-DECOMPRESSED-VARYING-BROTLI-CDN decompressed discrimination >= 0.5 on /userinfo (H1 survives)
4. |B-DECOMPRESSED-VARYING-GZIP(parent=0.5) - B-DECOMPRESSED-VARYING-BROTLI-CDN| < 0.1 (H2 survives)

**ALGORITHM-EQUIVALENT** if condition (4) holds.

**ALGORITHM-DEPENDENT** if condition (4) fails (|diff| >= 0.1).

**FALSIFIED-IN-SETTING** if condition (3) fails (decompression-normalization fails under CDN noise).

**MEASUREMENT_INVALID** if pipeline errors, sample size insufficient, or CDN-noise proxy fails to introduce non-determinism (all compressed hashes identical despite noise injection).

## 11. Validity Threats

1. **Simulator fidelity**: The CDN-noise proxy simulates specific non-determinism sources but cannot capture all real CDN behavior (edge selection, load balancing, geographic routing, TLS fingerprinting, real caching TTLs). A positive result is necessary but not sufficient for real-CDN deployment.

2. **Localhost only**: All traffic is localhost, so network-level CDN behaviors (latency variation, packet loss, connection reuse) are not tested. This is acceptable for mechanism validation but not for production latency measurement.

3. **Mock OAuth2 server**: The mock server has4 states with 3-way error collapse (identical error bodies), capping discrimination at 0.5. This structural ceiling is inherited from the parent and does not weaken the CDN-noise test.

4. **Brotli quality range**: The effective brotli diversity for 1KB JSON is2 variants (q4 distinct vs q5-8 identical), as established by the parent audit. The CDN-noise proxy varies quality per request but the compressed outputs for q5-8 are identical, so the effective noise is weaker than it appears. This is a known limitation.

5. **No real Accept-Encoding negotiation**: Real CDNs negotiate Accept-Encoding based on client hints, edge capabilities, and cache state. The proxy's Bernoulli override is a simplified model.

6. **Cache model**: The proxy's cache is a simple in-memory store with Bernoulli hit rate. Real CDN caches have TTLs, invalidation, and hierarchical caching. This is acceptable for mechanism validation.

## 12. Product Consequence

**If SURVIVES_CURRENT_TEST**: The claim ceiling for C-MEAS-VALID advances from "synthetic proxy only" to "synthetic proxy + CDN simulator with realistic non-determinism". Product may proceed to real-CDN validation (Cloudflare Workers or equivalent) with higher confidence. The decompression-normalization mechanism is validated against5 specific CDN non-determinism sources.

**If FALSIFIED-IN-SETTING**: The mechanism fails under controlled CDN-like conditions. The design space narrows to: (a) identify which CDN noise source causes failure (quality variation vs chunked encoding vs Accept-Encoding negotiation vs caching), (b) design a fix or alternative normalization, (c) re-test in simulator before any real-CDN investment.

**If MEASUREMENT_INVALID**: The CDN-noise proxy failed to introduce non-determinism or the pipeline has errors. Diagnose and re-design. No scientific conclusion possible.

## 13. Restrictions

- DESIGN mode only: no outcome-bearing measurements
- Do not modify frozen parent files (EXP-RUNTIME-35130682006)
- Do not git commit/push/switch/reset
- Only edit files within research/experiments/EXP-RUNTIME-35137033384/
