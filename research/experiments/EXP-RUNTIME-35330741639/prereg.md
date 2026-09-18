# EXP-RUNTIME-35330741639 — Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-35330741639
- **Lane**: runtime
- **Claim IDs**: C-MEAS-VALID
- **Parent**: EXP-RUNTIME-35290615081 (handoff sha256: `1b5c80195b49a58c89691fcccc92320ed669a474586994f6e737b1c1969852df`)
- **Trigger**: pulse
- **Base SHA**: f14b01cf8dbd10513705c8c9606023c4a27ac30f

## 2. Scientific Question

Does iterative decompression survive CDN-like proxy behaviors — specifically Accept-Encoding negotiation, response caching, and Transfer-Encoding: chunked — that real CDN infrastructure (Cloudflare/Fastly/Akamai) applies between origin and client?

## 3. Hypothesis

The parent validated iterative decompression on localhost with a direct mock server. Real CDN infrastructure introduces intermediate behaviors orthogonal to multi-layer encoding:

- **Caching**: CDN caches compressed response, serves without re-compression. Does not change compressed bytes — should survive.
- **Re-compression**: CDN decompresses origin response and re-compresses with its own algorithm/quality. Adds at most one layer — max_depth=5 should handle.
- **Chunked TE**: CDN uses Transfer-Encoding: chunked. Transport-layer concern resolved before body processing — should not affect decompressed bytes.

If iterative decompression is format-invariant, it should survive all three behaviors.

## 4. Inherited State (from parent handoff)

### Established
- Iterative decompression (max_depth=5) restores decompression-normalization under triple-brotli for ALL auth states including valid_token on localhost
- Decompressed body-only discrimination 0.5 across all (state, content_type x size) combinations
- Decompressed hash determinism all_same=true for all states
- Compressed-only discrimination 0.2781 < 0.3 confirms decompression is necessary
- No decompression errors, no crashes/hangs

### Rejected
- Single-pass client decompression does NOT survive double/triple-brotli
- Compressed-only body hashing is NOT sufficient for format-invariant discrimination

### Unknown
- Does iterative decompression survive real CDN infrastructure?
- What is production-scale latency at N>1000?
- Does it work for binary content types?
- Maximum practical decompression depth for real-world encoding?

### Do NOT Assume
- Production-readiness (real CDN untested)
- Structural discrimination ceiling of 0.5 applies to production
- Localhost latency represents production cost
- Format-invariance extends to binary content types
- Max depth of 5 is sufficient for all real-world encoding

## 5. Experimental Design

### 5.1 Infrastructure

| Component | Description |
|-----------|-------------|
| Mock origin server | localhost, 4 auth states, JSON/HTML/XML x 1KB/10KB/100KB, brotli quality 6 (deterministic). Same as parent. |
| Python reverse proxy | Separate localhost port. Accepts client requests, forwards to origin, applies configured proxy behavior. |
| Client | Same as parent: iterative decompression (brotli→gzip→identity, max_depth=5). |

### 5.2 Proxy Behaviors (independent variable)

| Behavior | Description | CDN Analogy |
|----------|-------------|-------------|
| PASSTHROUGH | Forward request/response unmodified. Chunked TE always applied. | CDN with cache disabled |
| CACHED | Cache compressed response by (URL, Accept-Encoding) for 60s. Serve from cache on repeat. Chunked TE. | CDN with caching enabled |
| RECOMPRESS | Fetch origin, decompress, re-compress with proxy's own brotli quality 8. Chunked TE. | CDN re-compressing at edge |

### 5.3 Test Matrix

- **Auth states**: no_auth, valid_token, expired_token, invalid_token (4)
- **Content types**: JSON, HTML, XML (3)
- **Sizes**: 1KB, 10KB, 100KB (3)
- **Proxy behaviors**: PASSTHROUGH, CACHED, RECOMPRESS (3)
- **Reps per cell**: 5
- **Total requests**: 4 × 3 × 3 × 3 × 5 = 540

### 5.4 Assignment

Deterministic round-robin. For each (content_type × size), create a plan of 5 reps per auth_state per proxy_behavior. Assign in round-robin order. Seed=44 for request ordering.

## 6. Controls

| ID | Type | Description | Expected |
|----|------|-------------|----------|
| B-PARENT-DECOMPRESSED-0.5 | Baseline | Parent decompressed discrimination | 0.5 |
| B-PARENT-COMPRESSED-0.2781 | Baseline | Parent compressed discrimination | 0.2781 |
| B-RANDOM | Null | SHA256 on random 32-byte fingerprints | ~0.0 |
| B-DIRECT-PASSTHROUGH | Baseline | Proxy passthrough (no caching, no re-compression) | 0.5 |
| C_PROXY_PASSTHROUGH_EQUIVALENCE | Positive control | Passthrough discrimination = 0.5 for all cells | Pass |
| C_NULL_CONTROL | Null control | B-RANDOM ~ 0.0 | Pass |

## 7. Metrics

### Primary
- **decompressed_body_only_discrimination**: Jaccard distance between decompressed-body SHA256 hashes across auth states, per (content_type × size × proxy_behavior). Threshold: >= 0.3.
- **decompressed_hash_determinism**: all_same=true for within-state decompressed hash variation. Extended: decompressed hash through each proxy behavior must match parent's direct-server hash.

### Secondary
- **compressed_body_only_discrimination**: Jaccard on compressed bytes. Reference only (may differ from parent due to re-compression).
- **decompression_latency_ms**: Per-response decompression time. Reference only.
- **decompression_errors**: List of any failures. Must be empty.
- **proxy_overhead_ms**: Time added by proxy layer. Reference only.

## 8. Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:
1. decompressed_body_only_discrimination >= 0.3 for ALL (auth_state, proxy_behavior) combinations
2. decompressed hash through each proxy_behavior matches parent's direct-server hash for same (auth_state, content_type, size) — determinism across proxy paths
3. B-RANDOM = 0.0 for all conditions
4. C_PROXY_PASSTHROUGH_EQUIVALENCE passes (passthrough discrimination = 0.5)
5. No decompression crashes/hangs
6. Regression: all 4 auth states maintain discrimination >= 0.3 under passthrough

**FALSIFIED-IN-SETTING** if:
- Any (auth_state, proxy_behavior) has discrimination < 0.3
- Any decompressed hash through proxy differs from direct-server hash
- Decompression crashes/hangs on cached or re-compressed responses

**MEASUREMENT_INVALID** if:
- Proxy fails to start or origin unreachable through proxy
- Chunked TE causes connection failures
- Fewer than 5 reps completed per cell

## 9. Consequences

### Positive
- Claim ceiling advances to include 'CDN proxy layer does not break iterative decompression'
- Product team can deploy with standard CDN configurations (caching, re-compression, chunked TE)
- Narrows real-CDN experiment to edge-specific concerns (quality variation, edge selection, cache invalidation)

### Negative
- Specific failure mode identifies CDN configuration constraint:
  - Caching breaks → CDN must pass Content-Encoding unmodified
  - Re-compression breaks → origin must set Cache-Control: no-transform
  - Chunked TE breaks → client must buffer full response before decompression

## 10. Scope Boundaries

This experiment tests locally-simulated CDN behaviors only. It does NOT test:
- Real CDN infrastructure (Cloudflare/Fastly/Akamai)
- Edge-specific quality variation
- Accept-Encoding negotiation across multiple CDN nodes
- Cache invalidation or TTL expiration behavior
- CDN-specific header manipulation (X-Cache, X-CDN, etc.)
- Geographic latency or edge selection

Real CDN testing remains the blocking dependency for C-MEAS-VALID product readiness.
