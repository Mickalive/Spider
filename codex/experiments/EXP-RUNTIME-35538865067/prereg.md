# EXP-RUNTIME-35538865067 — CDN Decompression Correctness

## STATUS: DESIGN NOT YET FROZEN

---

## 1. Research Question

Does iterative brotli/gzip decompression correctness hold when high-entropy multi-layer compressed payloads are served through real CDN infrastructure (Cloudflare free tier via cloudflared tunnel) with Accept-Encoding negotiation, Vary/cache semantics, geographic latency, and TCP segmentation?

## 2. Background and Motivation

The parent experiment (EXP-RUNTIME-35530588298) validated in-process decompressor API streaming across 840 multi-layer observations: brotli.Decompressor.process(chunk) and gzip.GzipFile.read(CHUNK_SIZE) both produce byte-identical output to full-body decompression. This resolved the V1_STREAMING_DECOMPRESSOR_POST_ACCUMULATION limitation.

The full localhost decompression chain is now validated across three orthogonal layers:
1. Iterative multi-layer decompression (EXP-RUNTIME-35513777099)
2. HTTP Transfer-Encoding framing streaming (EXP-RUNTIME-35522287921)
3. Decompressor API streaming (EXP-RUNTIME-35530588298)

The sole remaining blocker for C-MEAS-VALID Product Core readiness is real CDN infrastructure. CDN introduces:
- **Accept-Encoding negotiation**: CDN may re-encode, upgrade, or downgrade content encoding
- **Vary/cache semantics**: CDN may cache compressed responses and serve stale or re-encoded versions
- **Geographic latency**: Network conditions may affect chunk boundaries and timing
- **TCP segmentation**: Real network introduces fragmentation not present on localhost
- **Connection management**: HTTP/2, keep-alive, and connection pooling

These factors cannot be replicated on localhost. This experiment is materially orthogonal to all three localhost layers.

## 3. Hypothesis

**H1**: Iterative decompression (brotli→gzip→identity, max_depth=5) of high-entropy multi-layer compressed payloads served through Cloudflare CDN produces byte-identical output to ground truth.

**H0 (Falsifier)**: CDN-served compressed payloads produce different decompressed output than localhost ground truth, OR CDN silently re-encodes payloads, OR CDN caching causes stale/different responses.

## 4. Experimental Design

### 4.1 Infrastructure Setup

1. **Local origin server**: Python HTTP server serving high-entropy multi-layer compressed payloads on localhost:PORT
2. **Cloudflare Tunnel**: `cloudflared tunnel --url http://localhost:PORT` creates a public URL through Cloudflare's CDN
3. **Payload serving**: Each request returns a pre-compressed payload with appropriate Content-Encoding header

### 4.2 Payload Matrix

**Payload types** (inherited from parent, validated high-entropy generators):
- JSON: UUIDs, random floats, 5.49 bits/byte
- HTML: real Wikipedia paragraphs, 4.66 bits/byte
- Binary: structured random payloads, 7.69 bits/byte

**Compression layers**:
- Single: gzip(brotli(data)) — outer gzip, inner brotli
- Double: brotli(gzip(data)) — outer brotli, inner gzip

**Chunk sizes**:
- 8192 bytes (production CDN typical frame size)
- 32 bytes (stress test — maximum chunk count)

**Accept-Encoding variants**:
- No header (raw passthrough)
- `gzip` only
- `br` (brotli) only
- `gzip, br` (both advertised)

### 4.3 Conditions

Total conditions: 3 payload types × 2 compression orders × 2 chunk sizes × 4 Accept-Encoding variants = 48 conditions

Minimum N=5 observations per condition = 240 minimum observations

### 4.4 Measurements

For each observation:
1. `content_encoding_actual`: Content-Encoding header in CDN response
2. `content_length_actual`: Content-Length header in CDN response
3. `decompressed_sha256`: SHA256 of decompressed output using iterative decompressor
4. `ground_truth_sha256`: SHA256 of full-body decompression output (computed offline)
5. `streaming_equals_fullbody`: bool — decompressed_sha256 == ground_truth_sha256
6. `response_status`: HTTP status code
7. `response_time_ms`: Round-trip time
8. `cdn_serve_id`: Unique ID for this CDN serve (for cache testing)

### 4.5 Cache Test

For each unique payload (compressed form), make 3 consecutive requests with 1-second intervals. All three must produce identical decompressed output. This tests whether CDN caching causes stale or modified responses.

## 5. Controls

### Positive Control (B-LOCALHOST-DIRECT)
Same payloads served directly from localhost HTTP server without CDN tunnel. Re-validates parent's 840/840 result. If this fails, the environment is broken.

### Null Control (B-CDN-IDENTITY)
Uncompressed (identity) payloads served through CDN. If CDN corrupts uncompressed data, compressed data cannot be trusted.

### Baseline: B-CDN-RAW-PASSTHROUGH
CDN-served with no Accept-Encoding header — tests whether CDN preserves bytes when no negotiation occurs.

### Baseline: B-CDN-GZIP-ONLY
CDN-served with Accept-Encoding: gzip — tests CDN gzip negotiation and potential re-encoding.

### Baseline: B-CDN-BROTLI-ONLY
CDN-served with Accept-Encoding: br — tests CDN brotli negotiation and potential re-encoding.

### Baseline: B-CDN-IDENTITY
CDN-served uncompressed payloads — tests whether CDN corrupts or modifies uncompressed data.

## 6. Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL conditions:
- C1: CDN-served compressed payloads decompress to byte-identical SHA256 as ground truth for ALL conditions
- C2: CDN does not silently re-encode (Content-Encoding matches pre-compression, OR if CDN upgrades, upgraded encoding decompresses identically)
- C3: CDN caching does not cause stale/different responses (3 consecutive requests identical)
- C4: Identity payloads pass through CDN without byte corruption
- Positive control passes: B-LOCALHOST-DIRECT
- Null control passes: B-CDN-IDENTITY

**FALSIFIES** if any condition fails. Diagnosis required:
- Accept-Encoding failure: CDN re-encodes or upgrades encoding
- Cache failure: Stale responses from CDN cache
- Byte corruption: Decompressed output differs from ground truth
- Infrastructure failure: Tunnel not established, requests fail, etc.

## 7. Validity Threats

1. **Cloudflare Tunnel instability**: Tunnel may drop during experiment — mitigate with retry logic and health checks
2. **CDN rate limiting**: Cloudflare may rate-limit rapid requests — mitigate with jitter 200-500ms between requests
3. **CDN edge variation**: Different Cloudflare edge nodes may serve different responses — this is a feature, not a bug (tests real CDN behavior)
4. **Accept-Encoding mismatch**: CDN may not support brotli on free tier — record actual Content-Encoding and adapt
5. **Payload size too small for CDN caching**: Small payloads may not be cached — use 10KB+ payloads
6. **cloudflared binary availability**: Binary may not be installable in CI — check and report as infrastructure failure

## 8. Expected Information Gain

**If CDN passes**: The full decompression chain is validated across localhost AND real CDN. C-MEAS-VALID is nearly ready for Product Core promotion. Only kernel integration testing remains.

**If CDN fails**: The specific failure mode identifies the next fix:
- Accept-Encoding re-encoding → adjust compression strategy or CDN configuration
- Cache staleness → add cache-busting headers or adjust CDN cache rules
- Byte corruption → investigate TCP segmentation or CDN proxy behavior

Both outcomes change a product decision. This is the sole remaining blocker for C-MEAS-VALID Product Core readiness.

## 9. Claim Ceiling

This experiment bounds C-MEAS-VALID to:
- Cloudflare free tier CDN infrastructure
- High-entropy multi-layer compressed payloads (10KB-100KB)
- brotli quality 4 (default) and gzip level 6 (default)
- 8KB and 32B chunk sizes
- Python 3.12+ with brotli 1.2.0
- Single tunnel (no geographic distribution testing)

NOT validated by this experiment:
- Cloudflare paid tier or other CDN providers (Fastly, Akamai, AWS CloudFront)
- Very large payloads (>100KB)
- Brotli quality 5-11 or gzip level 1-9
- Geographic latency effects (single edge node)
- Concurrent clients (single connection)
- HTTP/1.1 vs HTTP/2 behavioral differences
- CDN re-encoding at different quality levels
