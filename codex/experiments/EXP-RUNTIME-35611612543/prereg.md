# EXP-RUNTIME-35611612543 preregistration

## Status

DESIGN NOT YET FROZEN. This preregistration is the DESIGN-phase output. It becomes immutable after FREEZE.

## Experiment Identity

- **experiment_id**: EXP-RUNTIME-35611612543
- **lane**: runtime
- **claim_ids**: C-MEAS-VALID, C-FRESHNESS
- **parent**: EXP-RUNTIME-35551516706 (sha256 be5276a0cebf8bcddc0db071cdb76c51e843eba37acf86b86123b38e02f1af7f)
- **reason**: pulse

## 1. Question

Does oracle-free greedy iterative decompression produce byte-identical output to ground truth for stale cache responses (stale-while-revalidate, stale-if-error) and revalidated responses (304 Not Modified, 200 re-fetched) served through a byte-preserving local nginx proxy_cache?

## 2. Background and Motivation

The parent experiment (EXP-RUNTIME-35551516706) established 100% byte-identical decompression on local nginx proxy_cache: 330/330 cached-path observations, 48/48 DYNAMIC-vs-HIT, all controls pass. However, the parent's claim ceiling is bounded by a critical gap: **all serves were within the 300s max-age window** (fresh cache only). Cache freshness edge cases — stale-while-revalidate, stale-if-error, 304 Not Modified, and 200 re-fetched after expiry — were not exercised.

In production CDN deployment, stale cache serving is common: CDNs serve stale content during revalidation windows (stale-while-revalidate) and origin failures (stale-if-error). If the cache alters wire bytes during stale serving (e.g., re-encoding, transcoding, or partial transformation), the oracle-free decompression pipeline would produce incorrect output.

The parent handoff explicitly lists "Cache freshness edge cases: expiry, revalidation, 304 Not Modified, stale-while-revalidate, stale-if-error were not exercised" as an unknown.

This experiment fills that gap using local nginx proxy_cache, which is within the parent's validated infrastructure scope.

## 3. Hypothesis

Oracle-free greedy decompression preserves byte-identity across all cache lifecycle stages (fresh HIT, stale HIT via SWR, stale HIT via SIE, 304 Not Modified, 200 re-fetched) through local nginx proxy_cache, because the cache serves the same wire bytes regardless of freshness state.

## 4. Falsifier

If any cache lifecycle stage produces byte-divergent output (oracle-free decompressed bytes differ from origin ground truth), the specific failure mode is documented and the freshness ceiling is narrowed to the passing stages only.

## 5. State Representation

Same as parent:
- 3 content types: HTML (`text/html`), JSON (`application/json`), binary (`application/octet-stream`)
- 2 Content-Encoding orders: Identity → Compressed, Compressed → Compressed
- 2 chunk sizes: 32, 8192
- 4 Accept-Encoding variants: `br`, `gzip`, `br, gzip`, `gzip, br`
- SEED=44 for deterministic payload generation
- Total primary cells: 3 x 2 x 2 x 4 = 48

## 6. Cache Lifecycle Stages (NEW vs parent)

The parent tested only FRESH cache (stage 1). This experiment adds 4 stages:

### Stage 1: FRESH cache HIT (positive control)
- max-age=300, request within 300s of population
- Expected: X-Cache: HIT, Age < 300
- Establishes baseline reproducing parent finding

### Stage 2: STALE cache HIT via stale-while-revalidate (SWR)
- max-age=1, stale-while-revalidate=86400
- Wait >1s after population, then request
- Expected: X-Cache: HIT (served stale while revalidating in background)
- nginx serves stale content immediately; revalidation is async

### Stage 3: STALE cache HIT via stale-if-error (SIE)
- max-age=1, stale-if-error=86400
- Stop origin server, then request
- Expected: X-Cache: HIT (served stale because origin is unavailable)
- Origin must be stopped/restarted between stages

### Stage 4: 304 Not Modified (revalidation)
- max-age=0 (forces revalidation on every request)
- Client sends If-None-Match with ETag from prior response
- Expected: HTTP 304, no body served
- 304 carries no body, so decompression is not applicable; this stage tests that the observation substrate correctly handles 304 (no false positive)

### Stage 5: 200 re-fetched after expiry
- max-age=0 (forces revalidation on every request)
- Client sends If-None-Match; origin returns 200 with fresh content
- Expected: HTTP 200 with body, X-Cache: MISS or HIT (depending on nginx revalidation behavior)
- Tests that re-fetched content decompresses identically to origin

## 7. Action Representation

Same as parent: HTTP GET with Accept-Encoding header varied across 4 variants. No browser, no Playwright, no model calls.

## 8. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-LOCALHOST-DIRECT | Origin direct fetch, no proxy, oracle-free decode | 100% byte-identical |
| B-FRESH-HIT | Cache HIT within max-age (parent's design) | 100% byte-identical |
| B-ORACLE-GUIDED-REGRESSION | Oracle-guided decode on same wire bytes | 100% correct, no regression |
| B-FIXED-ORDER-CDN | Fixed-order decode on same wire bytes | 480/480 on local nginx (parent value) |

## 9. Positive Control

Fresh cache HIT stage (stage 1) with identical payloads to parent's 48/48 design. Expected: 100% byte-identical. Validates test infrastructure reproduces parent finding.

## 10. Null Controls

- Identity (uncompressed) payloads through each stage: expected 100% (no decompression applied)
- Deliberately corrupted brotli/gzip payloads: expected decode failure (not byte-divergent output)

## 11. Measurement Plan

### 11.1 Infrastructure Setup

```bash
# Python origin server serving deterministic payloads
# with configurable Cache-Control headers per payload

# nginx proxy_cache configuration:
proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=test_cache:10m
    max_size=100m inactive=60s;

# Stage-specific server blocks with different Cache-Control:
# Stage 1: Cache-Control: public, max-age=300
# Stage 2: Cache-Control: public, max-age=1, stale-while-revalidate=86400
# Stage 3: Cache-Control: public, max-age=1, stale-if-error=86400
# Stage 4: Cache-Control: public, max-age=0
# Stage 5: Cache-Control: public, max-age=0
```

### 11.2 Observation Procedure

For each stage:
1. Populate cache (if applicable — stages 1-3 require prior population)
2. Wait appropriate time for freshness state (stage 2: >1s, stage 3: stop origin)
3. Fetch through proxy with Accept-Encoding variant
4. Record: HTTP status, X-Cache header, Age header, Content-Encoding, raw wire bytes (body), Content-Length
5. Independently fetch from origin (no cache) to get ground truth
6. Apply oracle-free greedy decode to both cached and origin responses
7. Compare decompressed bytes

### 11.3 Sample Size

Per stage: 48 cells x 5 reps = 240 observations
Total: 5 stages x 240 = 1200 observations
(Stages 4-5 may have fewer applicable cells due to 304 having no body)

### 11.4 Raw Evidence Persistence

- `raw_cell_results.jsonl`: one row per observation with fields:
  - experiment_id, stage, cell_id, content_type, encoding_order, chunk_size, accept_encoding, rep
  - http_status, x_cache, age, content_encoding_header, content_length
  - raw_wire_bytes_sha256, origin_wire_bytes_sha256
  - oracle_free_correct, oracle_free_decompressed_sha256, origin_decompressed_sha256
  - oracle_guided_correct, fixed_order_correct
  - timestamp, session_kind (STAGE_1_FRESH, STAGE_2_SWR, STAGE_3_SIE, STAGE_4_304, STAGE_5_REFETCH)

## 12. Decision Rule

### Primary condition
- byte_identical_accuracy = 1.0 across ALL 5 cache lifecycle stages
  - Stage 1: all 240 observations byte-identical
  - Stage 2: all 240 observations byte-identical
  - Stage 3: all 240 observations byte-identical
  - Stage 4: all 304 responses correctly identified (no body to decompress)
  - Stage 5: all 200 re-fetch observations byte-identical

### Secondary conditions
- (a) zero decode failures on valid payloads across all stages
- (b) zero false accepts on corrupted payloads
- (c) oracle-guided regression passes (no regression vs parent)
- (d) fixed-order baseline reproduces parent local-nginx value

### Outcome mapping
- **SUPPORTS**: ALL conditions pass
- **FALSIFIES**: ANY stage shows byte-divergence (document specific stage, cell, encoding)
- **MIXED**: some stages pass, others fail
- **BLOCKED**: infrastructure prevents cache lifecycle testing
- **MEASUREMENT_INVALID**: controls fail or data quality insufficient

## 13. Product Consequences

### If SUPPORTS
- Cache freshness lifecycle does not break oracle-free decompression
- Claim ceiling extends from fresh-only to include stale serving (SWR, SIE) and revalidation
- Strengthens C-MEAS-VALID and C-FRESHNESS evidence
- Product can safely serve stale cached responses through decompression pipeline
- Remaining unknown: production CDN byte behavior (separate infrastructure requirement)

### If FALSIFIES
- Stale cache serving breaks oracle-free decompression
- Claim ceiling narrows to fresh-only cache behavior
- Production deployment must avoid stale cache serving through decompression
- C-FRESHNESS evidence weakened
- Specific failure mode documented for mitigation

## 14. Validity Threats

1. **nginx-specific behavior**: nginx proxy_cache may not replicate production CDN stale-serving behavior. Result bounded to nginx-class caches.
2. **Stage 3 (SIE) implementation**: Stopping/restarting origin within a test run is fragile. May need manual intervention.
3. **Stage 4 (304)**: 304 has no body; the "byte-identical" comparison is not applicable. Stage 4 tests observation substrate correctness (correctly identifying 304), not decompression.
4. **Cache key variation**: nginx may use different cache keys for different Accept-Encoding variants. Need consistent cache key design.
5. **Timing sensitivity**: Stage 2 (SWR) requires >1s wait. Stage 3 (SIE) requires origin stop. Both introduce timing dependencies.
6. **Encodings during stale serving**: nginx may re-encode during stale serving if client Accept-Encoding differs from origin. This is the specific failure mode being tested.

## 15. Scope Limitations

- Bounded to local nginx 1.24.0 proxy_cache. Production CDN behavior is a separate experiment.
- Does not test: Cloudflare, Fastly, Akamai, CloudFront, or any external CDN.
- Does not test: HTTP/2, HTTP/3, TLS, multi-edge, cross-region.
- Does not test: concurrent load, performance economics (parent unknown).
- Does not test: cache key collision, cache poisoning, partial content (206).
