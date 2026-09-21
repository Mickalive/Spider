# EXP-RUNTIME-35551516706 — Local CDN Cache HIT Oracle-Free Decode Test

## 1. Identity

**experiment_id**: EXP-RUNTIME-35551516706
**lane**: runtime
**claim_ids**: ["C-MEAS-VALID"]
**created_at**: 2026-09-21T01:38:01.489599+00:00
**parent**: EXP-RUNTIME-35544804817 (MIXED, oracle-free validated for DYNAMIC, HIT untestable on Cloudflare free-tier)

## 2. Inherited State (from EXP-RUNTIME-35544804817 handoff)

### Established
- Oracle-free greedy iterative decompression (try brotli->gzip until neither succeeds, MAX_DEPTH=5, no SHA256 oracle) produces byte-identical output to ground truth on Cloudflare free-tier quick-tunnel DYNAMIC responses: 240/240 primary matrix (48 cells x 5), 240/240 localhost positive control, 15/15 identity null control, ~45/45 depth 3-5, ~30/30 large >100KB, 48/48 HIT-test DYNAMIC bytes, 0 ambiguous tie-breaks.
- Parent's oracle circularity gap (audit V1, EXP-RUNTIME-35542474231) is resolved: the deployable decoder works without SHA256 oracle on DYNAMIC responses.
- Brotli (magic 0xCEB2CF81) and gzip (magic 0x1F8B) have distinct format signatures making greedy try-brotli-then-gzip order unambiguous: zero ambiguous tie-breaks across 693 observations.
- CDN does not corrupt bytes: the parent fixed-origin-order failure was in the framing assumption, not byte transformation.

### Rejected
- Fixed-origin-order iterative decompression through Cloudflare CDN (180/240 failures).
- CDN preserves origin Content-Encoding byte-identical (partially rejected — may vary by CDN tier).
- Gzip/brotli chunk boundary corruption at chunk_size=32.
- Streaming chunked forwarding corruption.

### Unknown (target of this experiment)
- **CDN cache HIT (stale) serving**: 0% HIT on Cloudflare quick tunnel free-tier. Requires production Cloudflare zone with cache enabled, or alternative CDN. THIS EXPERIMENT TESTS THIS ON LOCAL NGINX.
- **Oracle-free decode behavior on CDN cache HIT responses**: are cached compressed bytes byte-identical to DYNAMIC response bytes?
- **Performance economics**: amortized latency and CPU cost of greedy try-brotli-then-gzip loop vs oracle-guided decode.

### Do Not Assume
- C-MEAS-VALID is ready for VALIDATED or PRODUCT_CORE promotion — CDN HIT (stale) serving is untested on real caching infrastructure.
- Oracle-free decode works on all CDN conditions globally — validated only for Cloudflare free-tier quick tunnel DYNAMIC.
- CDN cache HIT behavior is safe — zero HIT observed on Cloudflare free-tier.

## 3. Question

On a local nginx caching reverse proxy that produces real cache HIT responses, does oracle-free greedy iterative decompression produce byte-identical output to ground truth for cached (stale) responses, and does the decompressed output differ from the DYNAMIC-path decompressed output?

## 4. Hypothesis

A local nginx proxy_cache in front of the same Python origin server produces real cache HIT responses. Oracle-free greedy iterative decode produces byte-identical output to ground truth for >=90% of cache HIT observations. Cache HIT wire bytes are byte-identical to DYNAMIC wire bytes for the same payload. The parent's 0% HIT rate on Cloudflare free-tier quick tunnel was an infrastructure ceiling, not a negative scientific result about HIT serving behavior.

## 5. Falsifier

Any of the following falsifies the hypothesis:
1. Fewer than 90% of cache HIT observations produce decompressed output with SHA256 == ground truth under oracle-free greedy decode.
2. Cache HIT wire bytes differ from DYNAMIC wire bytes for the same payload (CDN alters bytes on cache serve).
3. Oracle-free greedy decode enters an infinite loop or returns None for any cache HIT cell.
4. nginx fails to produce any cache HIT responses despite Cache-Control: public, max-age=300 (infrastructure ceiling, not falsification).
5. Oracle-free greedy decode produces different decompression path for HIT vs DYNAMIC for any cell where paths diverge.

## 6. Infrastructure

### Origin Server
- Python 3.12 HTTP server (same as parent EXP-RUNTIME-35544804817).
- Serves brotli (q4) and gzip (L1) compressed payloads.
- Same 48-cell matrix: 3 payloads (JSON, HTML, binary-mixed) x 2 serve orders (brotli-first, gzip-first) x 2 chunk sizes (32, 8192) x 4 Accept-Encoding variants (br, gzip, br+gzip, identity).

### Caching Reverse Proxy
- nginx with proxy_cache module.
- Cache zone configured with Cache-Control: public, max-age=300 respected from origin.
- Produces real X-Cache: HIT / X-Cache: MISS headers.
- Listen on a local port (e.g., 8080), proxy_pass to Python origin.

### Why Local nginx Instead of Cloudflare Free-Tier
- Cloudflare free-tier quick tunnel produces 0% cache HIT rate despite Cache-Control: public, max-age=300 (EXP-RUNTIME-35544804817).
- This is an infrastructure ceiling, not a negative scientific result.
- Local nginx proxy_cache produces real HIT/MISS behavior.
- nginx is available in the CI environment (verified: /usr/sbin/nginx).
- This is the smallest change that enables HIT testing without external CDN costs.

## 7. Algorithm (Frozen)

Oracle-free greedy iterative decode — identical to parent:

```python
MAX_DEPTH = 5

def oracle_free_greedy_decode(raw_bytes):
    current = raw_bytes
    path = []
    ambiguous = False
    for depth in range(MAX_DEPTH):
        br_result = None
        gz_result = None
        try:
            br_result = brotli.decompress(current)
        except Exception:
            pass
        try:
            gz_result = gzip.decompress(current)
        except Exception:
            pass
        if br_result is not None and gz_result is not None:
            ambiguous = True
            path.append("br")
            current = br_result
        elif br_result is not None:
            path.append("br")
            current = br_result
        elif gz_result is not None:
            path.append("gz")
            current = gz_result
        else:
            break
    method = "+".join(path) if path else "identity"
    return current, method, ambiguous
```

No SHA256 check at any point.

## 8. Experimental Protocol

### Phase 0: Infrastructure Validation
1. Start Python origin server with same payload generation as parent.
2. Start nginx with proxy_cache pointing to origin.
3. Verify origin serves payloads correctly (direct request returns 200).
4. Verify nginx proxy passes through correctly (proxy request returns 200).
5. Warm up cache: send 10 requests to same URL, verify at least 1 produces X-Cache: HIT.
6. If no HIT after 10 requests, reconfigure nginx cache settings and retry. If still no HIT, record as infrastructure ceiling (not falsification).

### Phase 1: Origin Ground Truth
1. Serve all 48 payloads from origin (bypassing nginx).
2. For each payload, record: raw wire bytes, Content-Encoding, HTTP status.
3. Compute ground truth SHA256 by iterative decode of origin-served bytes.
4. This is identical to parent Phase 1.

### Phase 2: DYNAMIC Path (Cache Bypass)
1. For each of 48 cells, send request with unique URL (cache-busting query parameter).
2. Record: raw wire bytes, Content-Encoding, X-Cache status (should be MISS).
3. Apply oracle-free greedy decode to wire bytes.
4. Compare decompressed SHA256 with ground truth.
5. This validates oracle-free decode on DYNAMIC responses through nginx proxy (regression check).

### Phase 3: HIT Path (Cache Populate + Test)
1. For each of 48 cells, send request with fixed URL (no cache-busting).
2. Record: raw wire bytes, Content-Encoding, X-Cache status.
3. Wait 1-3 seconds.
4. Send same request again with same fixed URL.
5. Record: raw wire bytes, Content-Encoding, X-Cache status (should be HIT).
6. Apply oracle-free greedy decode to HIT wire bytes.
7. Compare decompressed SHA256 with ground truth.
8. N=5 per cell: repeat populate+test 5 times per cell (total 240 HIT observations).

### Phase 4: DYNAMIC vs HIT Identity Test (C8)
1. For each of 48 cells, compare wire bytes from DYNAMIC response (Phase 2) with wire bytes from HIT response (Phase 3, last rep).
2. Record: bytes_identical (bool), content_encoding_match (bool), content_length_match (bool).
3. If bytes differ, record the diff (first N differing bytes).

### Phase 5: Cache Stability (C3)
1. Select 6 representative payloads (2 JSON, 2 HTML, 1 binary, 1 large).
2. For each, send 3 consecutive requests with same fixed URL.
3. Record: X-Cache status for each request.
4. All 3 responses within a group must have byte-identical wire bytes.
5. Persist per-observation stability rows in raw_cell_results.jsonl (audit V4 gap fix).

### Phase 6: Depth Generalization (C5)
1. Generate depth 3-5 stacked encodings (same protocol as parent).
2. Serve through nginx cache.
3. Apply oracle-free greedy decode to cached wire bytes.
4. Compare decompressed SHA256 with ground truth.

### Phase 7: Large Payload (C6)
1. Generate >100KB payloads (same protocol as parent).
2. Serve through nginx cache.
3. Apply oracle-free greedy decode to cached wire bytes.
4. Compare decompressed SHA256 with ground truth.

### Phase 8: Regression Baselines (Audit V5 Gap Fix)
1. Apply oracle-guided decode (with SHA256 oracle) to the same wire bytes from Phase 2 and Phase 3.
2. Apply fixed-origin-order decode to the same wire bytes from Phase 2 and Phase 3.
3. Record results for B-ORACLE-GUIDED-REGRESSION and B-FIXED-ORDER-CDN.

## 9. Decision Rule (Frozen)

ALL conditions must pass for SURVIVES_CURRENT_TEST:

- **C1**: Oracle-free greedy decode produces byte-identical SHA256 output as ground truth for ALL 48 primary cache HIT cells
- **C2**: >=90% of cache HIT observations match ground truth under oracle-free greedy decode
- **C3**: 6/6 cache stability groups byte-stable under oracle-free decode
- **C4**: 15/15 identity observations recover ground truth under oracle-free decode
- **C5**: Depth 3-5 oracle-free greedy decode recovers ground truth for >=80% of depth observations
- **C6**: Large payload oracle-free greedy decode recovers ground truth for >=80% of >100KB observations
- **C7**: No ambiguous tie-breaks where both brotli and gzip succeed at same layer and produce divergent final SHA256
- **C8**: DYNAMIC and HIT wire bytes are byte-identical for >=90% of cells
- Positive control passes: B-LOCALHOST-DIRECT oracle-free greedy decode matches ground truth (240/240)
- Null control passes: B-DYNAMIC-VS-HIT-IDENTITY wire bytes are byte-identical

**Verdict mapping:**
- IF C1 fails: FALSIFIES oracle-free decode does not restore correctness on cached responses
- IF C1 passes but C2 fails: MIXED oracle-free works for some HIT cells but not all
- IF C1 passes but C8 fails: MIXED oracle-free works but CDN alters bytes on cache serve (new failure mode)
- IF all pass: SUPPORTS oracle-free decode validated for cached responses, C-MEAS-VALID HIT gap closed

## 10. Metrics (Stable Identities for Downstream)

| Metric ID | Description | Target |
|-----------|-------------|--------|
| M-HIT-CORRECT | # cache HIT observations where oracle-free decode SHA256 == ground truth / total HIT observations | >=90% |
| M-HIT-CORRECT-48 | # of 48 primary HIT cells where all 5 reps match ground truth | 48/48 |
| M-DYNAMIC-CORRECT | # DYNAMIC observations where oracle-free decode SHA256 == ground truth / total DYNAMIC observations | 100% |
| M-BYTES-IDENTICAL | # of 48 cells where DYNAMIC and HIT wire bytes are identical | >=48 (100%) |
| M-STABILITY | # of 6 cache stability groups where all 3 consecutive requests are byte-identical | 6/6 |
| M-IDENTITY | # of 15 identity observations where oracle-free decode recovers ground truth | 15/15 |
| M-DEPTH | # depth 3-5 observations where oracle-free decode recovers ground truth / total depth observations | >=80% |
| M-LARGE | # >100KB observations where oracle-free decode recovers ground truth / total large observations | >=80% |
| M-AMBIGUOUS | # observations where both brotli and gzip succeed at same layer | 0 |
| M-HIT-RATE | % of test-phase requests that produce X-Cache: HIT | >50% |

## 11. Consequences

### Positive Outcome (SUPPORTS)
- C-MEAS-VALID HIT gap closes.
- Oracle-free decode validated for both DYNAMIC and HIT responses on local caching infrastructure.
- C-MEAS-VALID advances toward VALIDATED.
- Product lane may integrate encoding-agnostic decoder for CDN-backed deployments.
- Next: test on production Cloudflare paid-tier or alternative CDN for generalization.

### Negative Outcome (FALSIFIES or MIXED)
- C-MEAS-VALID remains EXPERIMENTAL.
- Diagnosis identifies specific failure mode: (a) cache serving different bytes, (b) oracle-free decode failure on cached bytes, (c) ambiguous format detection, or (d) depth/payload generalization.
- Product remains blocked from CDN-cached deployment without SHA oracle.
- Alternative: investigate why nginx cache serves different bytes than origin (if applicable).

### Infrastructure Ceiling (no HITs produced)
- nginx fails to produce cache HITs despite configuration.
- Record as infrastructure ceiling (not falsification).
- C-MEAS-VALID HIT gap remains open.
- Try alternative: Varnish, or Docker-based CDN.

## 12. Validity Threats

1. **Local nginx ≠ production CDN**: nginx proxy_cache may not exhibit the same behavior as Cloudflare/Fastly/Akamai. Cache HIT wire bytes may be identical on nginx but different on production CDN. Claim ceiling bounded to local nginx.
2. **Cache key selection**: nginx cache key defaults to URI. Different cache keys (e.g., including Accept-Encoding) could affect HIT rate. Frozen: cache key = URI only.
3. **Cache warming timing**: 1-3s delay between populate and test may be insufficient for cache to be ready. Phase 0 warm-up validates this.
4. **No concurrent load**: sequential requests only. Concurrent load may affect cache behavior. Not tested.
5. **No HTTP/2 or H3**: nginx HTTP/1.1 only. HTTP/2 or H3 may behave differently. Not tested.
6. **Single edge**: local nginx only. Different CDN edges may have different behavior. Not tested.
