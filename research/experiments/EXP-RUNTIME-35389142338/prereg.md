# EXP-RUNTIME-35389142338 — Preregistration

## Status

DESIGN NOT YET FROZEN.

---

## 1. Experiment Identity

- **Experiment ID:** EXP-RUNTIME-35389142338
- **Lane:** runtime
- **Claim IDs:** C-MEAS-VALID
- **Parent:** EXP-RUNTIME-35330741639 (handoff sha256: 7f63b1ff3a4251a8d16a0b3d48ecef56c68fb80a91d9410f78b80d40ee5b925a)

## 2. Question

Does iterative decompression maintain discrimination when the CDN-like proxy cache is configured with auth-aware semantics (Cache-Control: private, Vary: Authorization, cache key includes Authorization) — resolving the parent's CACHED falsification from a cache-key configuration artifact into a genuine decompression test?

## 3. Hypothesis

The parent falsified CACHED mode (discrimination 0.0 across all 9 cells), but the root cause was naive cache key (URL, Accept-Encoding) excluding Authorization. The proxy served stale first-auth-state body to all states. This is a cache-key semantics issue, not a decompression failure.

If the cache key is extended to include Authorization, each auth state receives its own cached response, and iterative decompression should restore discrimination to 0.5 (matching PASSTHROUGH/RECOMPRESS).

Evidence supporting this hypothesis:
1. Decompression errors were 0 across all 540 parent requests
2. Decompressed hash determinism was all_same=true for all states
3. PASSTHROUGH and RECOMPRESS both achieved 0.5 discrimination through the same proxy infrastructure
4. The audit (V1) explicitly identified this as "CDN cache-key semantics, not iterative decompression failure"

## 4. Falsifier

Decompressed body-only discrimination < 0.3 for any (auth_state, cache_config) combination under auth-aware caching, OR decompressed hash differs from direct-server hash, OR decompression crashes/hangs, OR PASSTHROUGH drops below 0.5 (infrastructure regression), OR auth-aware caching does not restore discrimination above 0.0.

## 5. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-PARENT-DECOMPRESSED-0.5 | Parent PASSTHROUGH/RECOMPRESS discrimination | 0.5 |
| B-PARENT-CACHED-0.0 | Parent naive CACHED discrimination (the failure) | 0.0 |
| B-RANDOM | Random fingerprints | ~0.0 |
| B-AUTH-AWARE-CACHED-0.5 | Auth-aware CACHED if fix works | 0.5 |

## 6. Controls

### Positive Control
**C_PASSTHROUGH_REGRESSION:** PASSTHROUGH discrimination = 0.5 for all cells. Confirms proxy infrastructure unchanged.

### Null Control
**C_NULL_CONTROL:** B-RANDOM = 0.0 for all conditions.

### Reproduction Control
**C_NAIVE_CACHED_REPRODUCTION:** Naive CACHED discrimination = 0.0 for all cells. Reproduces parent's falsification to confirm environment stability.

## 7. Experimental Conditions

Two cache configurations × 9 content conditions × 4 auth states × 5 reps:

**Cache configurations:**
- NAIVE: cache key = (URL, Accept-Encoding) — parent's failing configuration
- AUTH-AWARE: cache key = (URL, Accept-Encoding, Authorization), origin sets Cache-Control: private, Vary: Authorization

**Content conditions:** JSON/HTML/XML × 1KB/10KB/100KB

**Auth states:** no_auth, valid_token, expired_token, invalid_token

**Total requests:** 2 × 9 × 4 × 5 = 360

## 8. Measurement Protocol

1. Start mock origin server (same as parent, Flask/stdlib, 4 auth states, brotli quality 6)
2. Start Python reverse proxy with two cache configurations on separate ports
3. For each cache config, make requests in randomized order (seed=44)
4. For each response: record compressed body, decompressed body (iterative max_depth=5), decompression latency, proxy overhead, headers, status
5. Compute discrimination metric: intra_match_rate - inter_match_rate on decompressed SHA-256 hashes
6. Verify decompressed hash matches parent's direct-server hash for each (auth_state, content_type, size)

## 9. Decision Rule

**SURVIVES_CURRENT_TEST** if ALL:
1. Auth-aware CACHED discrimination ≥ 0.3 for all cells
2. Decompressed hash through auth-aware CACHED matches parent direct-server hash
3. B-RANDOM = 0.0 for all conditions
4. PASSTHROUGH = 0.5 and naive CACHED = 0.0 (reproduces parent)
5. No decompression crashes/hangs
6. Auth-aware CACHED discrimination ≥ 0.3 for all cells

**FALSIFIED-IN-SETTING** if:
- Auth-aware CACHED discrimination < 0.3 for any cell
- Any decompressed hash differs from direct-server hash
- Decompression crashes/hangs on auth-aware cached responses
- PASSTHROUGH drops below 0.5

**MEASUREMENT_INVALID** if:
- Proxy fails to start
- Origin server unreachable
- Cache-Control/Vary headers not correctly applied

## 10. Sample Size and Power

360 total requests (2 cache configs × 9 content conditions × 4 auth states × 5 reps). This matches the parent's per-config density (180 requests per cache config) and provides 5 independent reps per cell for hash determinism verification.

## 11. Scope Boundaries

This experiment tests ONLY:
- Auth-aware caching on localhost Python reverse proxy
- Same mock origin as parent (Flask/stdlib, brotli quality 6)
- Single-layer brotli origin encoding
- Transfer-Encoding: chunked (constant background)
- 4 auth states with distinct response bodies
- HS256 locally-signed tokens

This experiment does NOT test:
- Real CDN infrastructure (Cloudflare/Fastly/Akamai)
- Double/triple-brotli through proxy
- Edge quality diversity
- Accept-Encoding negotiation across CDN nodes
- Production-scale latency/concurrency
- Binary content types
- Cache invalidation dynamics
- Geographic distribution

## 12. Consequences

**Positive outcome:** Auth-aware caching restores discrimination. Claim ceiling advances to include auth-aware CDN caching. Real-CDN experiment narrowed to edge-specific concerns. Product deployment path clarified.

**Negative outcome:** Auth-aware caching does not restore discrimination. Deeper decompression or proxy issue identified. Local fix attempted and failed before costly real-CDN deployment. Product deployment blocked on local infrastructure fix.

**Either outcome** strictly more informative than repeating parent or jumping to real CDN without local validation.
