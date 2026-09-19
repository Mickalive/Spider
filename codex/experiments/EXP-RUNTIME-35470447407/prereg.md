# EXP-RUNTIME-35470447407 preregistration

## Background

Parent experiment EXP-RUNTIME-35456070671 established decompression correctness for brotli under chunked transfer encoding on a localhost mock server: 360/360 correctness passes across 4 auth states x 3 content types x 3 chunk configurations (MULTI-CHUNK, SINGLE-CHUNK, IDENTITY), with 0 silent fallbacks, 0 decompression errors, and deterministic within-state grouping.

The parent handoff identifies the following as the primary unknown:

> Does iterative decompression correctness hold for gzip multi-chunk (not just brotli)?

Gzip is the second most common content-encoding on the Web (after identity/no-compression). The iterative decompression pipeline currently validates only brotli. If gzip decompression fails under chunked framing, the product cannot ship gzip support—a significant gap given that many CDNs and servers default to gzip.

## Scope

This experiment tests gzip decompression correctness under chunked transfer encoding, using the same correctness control methodology as the parent.

### In scope
- Gzip multi-chunk (chunk_size=32 bytes) correctness
- Gzip single-chunk (chunk_size=1024 bytes) correctness  
- 4 auth states: no_auth, valid_token, expired_token, invalid_token
- 3 content types: JSON, HTML, XML
- 10 reps per cell, 240 total gzip observations
- Brotli multi-chunk regression check (positive control)
- IDENTITY baseline (correctness oracle validation)
- Silent fallback detection
- Within-state determinism check

### Out of scope
- Real CDN infrastructure (Cloudflare/Fastly/Akamai)—requires external deployment
- Larger payloads (10KB, 100KB)—tests chunk-boundary stress but not encoding correctness
- Multi-layer encoding (gzip->brotli, brotli->gzip)—tests depth, not encoding
- Brotli quality variation (4-8)—tests compression parameter sensitivity
- Streaming partial-frame forwarding—tests proxy architecture

## Hypothesis

Iterative decompression (gzip->identity, max_depth=5) produces byte-identical output to ground-truth `generate_*_body(state, target_size)` for all 4 auth states across 3 content types at 1KB nominal with gzip multi-chunk framing.

## Falsifier

Any `SHA256(decompressed) != SHA256(generate_*_body(state, target_size))` across all 240 gzip observations, OR any silent fallback (`SHA256(decompressed) == SHA256(raw_compressed)`) for gzip-compressed responses.

## Controls

### Positive control: B-BROTLI-MC
Brotli multi-chunk correctness (chunk_size=32, brotli quality=6). Must pass 100% to confirm no regression in decompression pipeline infrastructure. Established 360/360 in parent; re-tested here as regression gate.

### Baselines
1. **B-IDENTITY**: No compression. Hash must match `generate_*_body()` exactly. Validates correctness oracle.
2. **B-GZIP-SC**: Gzip single-chunk (chunk_size=1024). Tests gzip correctness without chunk-boundary stress. If GZIP-SC passes but GZIP-MC fails, chunk boundaries are the failure mode.
3. **B-BROTLI-MC**: Brotli multi-chunk. Established in parent; re-tested as regression gate.

### Null control: B-RANDOM
Within-state decompressed hash must be deterministic (`all_same=true` for all 4 auth states across all gzip cells). Any within-state hash variation indicates non-deterministic decompression or server behavior.

## Architecture

```
Client (Python) -> Python Reverse Proxy -> Flask Mock OAuth2 Server
         |                    |                      |
    iterative           chunked TE              auth-aware
   decompression        framing              response bodies
    (max_depth=5)       (chunk_size)        (generate_*_body)
```

- **Mock origin**: Flask app with PyJWT validation, deterministic body generation via `generate_*_body(state, target_size)`
- **Reverse proxy**: Python HTTP proxy that applies Content-Encoding (gzip/brotli) and chunked Transfer-Encoding
- **Client**: Makes requests, collects raw compressed bytes, applies iterative decompression, compares SHA256 hashes

## Measurement plan

1. Start mock origin server on localhost
2. Start reverse proxy on localhost (configured for gzip compression, chunk_size=32 for MULTI-CHUNK, chunk_size=1024 for SINGLE-CHUNK)
3. For each cell (4 states x 3 content types x 3 chunk modes):
   - Make 10 requests with jitter 50-150ms
   - Record: raw response bytes, Content-Encoding header, Transfer-Encoding header
   - Apply iterative decompression (max_depth=5)
   - Compute SHA256(decompressed) and SHA256(generate_*_body(state, target_size))
   - Record: correctness match, silent fallback detection, decompression latency
4. Repeat for brotli multi-chunk (positive control regression check)
5. Compute aggregate metrics

## Decision rule

**SURVIVES_CURRENT_TEST** requires ALL of:
- C1: `correctness_match_rate == 1.0` for ALL 12 gzip cells
- C2: `silent_fallback_count == 0` for ALL gzip cells
- C3: B-BROTLI-MC passes 100% (no regression)
- C4: Null control passes (all_same=true for all states in all gzip cells)

**FALSIFIED** if any correctness failure OR any silent fallback in gzip cells.

**MEASUREMENT_INVALID** if infrastructure prevents data collection.

## Validity threats

1. **Gzip non-determinism**: Unlike brotli at fixed quality, Python's `gzip.compress()` with default parameters should be deterministic for identical inputs, but this must be verified by within-state grouping. If gzip introduces non-determinism (e.g., from timestamp-dependent headers), the correctness control still applies but the null control may fail.

2. **Compression-level mismatch**: Gzip default compression level may differ from brotli quality=6 in compression ratio. This does not affect correctness but may affect chunk count and chunk-boundary behavior.

3. **Chunk-boundary alignment**: gzip compressed output (300-600 bytes for 1KB input) spans 10-19 chunks at 32 bytes. If gzip's compression dictionary creates symbols that cross chunk boundaries differently than brotli, chunk-boundary failure modes may differ. This is precisely the question being tested.

4. **Mock server fidelity**: Localhost Flask server does not replicate CDN-specific header manipulation, Accept-Encoding negotiation, or geographic latency. This experiment tests encoding correctness, not CDN infrastructure behavior.

## Scope boundaries

- Results apply to: Python 3.12 stdlib gzip, localhost Flask mock, chunk_size=32/1024, 1KB payloads, 4 auth states, 3 content types
- Results do NOT apply to: real CDN infrastructure, larger payloads, multi-layer encoding, brotli quality variation, streaming proxies
- C-MEAS-VALID product readiness still requires CDN infrastructure validation (parent's primary unknown)
