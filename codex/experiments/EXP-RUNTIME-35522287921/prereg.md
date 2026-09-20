# EXP-RUNTIME-35522287921 Preregistration

## Title

Streaming Incremental Decompression Correctness Under Chunked Transfer Encoding

## Experiment ID

EXP-RUNTIME-35522287921

## Lane

runtime

## Claim IDs

C-MEAS-VALID

## Question

Does iterative decompression correctness hold for streaming incremental decompression where the proxy forwards partial chunked frames without full body reassembly, such that the decompressor processes chunk boundaries incrementally at realistic CDN chunk sizes (8KB+) and multi-layer encodings?

## Hypothesis

Iterative decompression (brotli->gzip->identity, max_depth=5) produces byte-identical SHA256 output between streaming (incremental chunk-by-chunk) and buffered (full-body) execution paths for all 4 auth states, 3 content types (JSON, HTML, BINARY), 2 multi-layer encoding configurations (GZIP-THEN-BROTLI, BROTLI-THEN-GZIP), and 2 chunk sizes (8KB realistic CDN, 32-byte stress test), using high-entropy non-redundant payloads with compressed sizes in the 2-99KB range.

## Falsifier

Any SHA256(streaming_decompressed) != SHA256(buffered_decompressed) across all observations for any (size, encoding, content_type, state, chunk_size) cell, OR any decompression error in the streaming path, OR any silent fallback (streaming_decompressed == raw_compressed) for any compressed response.

## Background and Motivation

### Inherited State from Parent Chain

**Established (do not re-test):**
- Iterative decompression (brotli->gzip->identity, max_depth=5) correctness on localhost buffered mock for HIGH-ENTROPY non-redundant payloads with multi-layer stacked encodings: 240/240 multi-layer correctness across 12 cells (EXP-RUNTIME-35513777099, audit REVISE with ceiling bounded)
- High-entropy payload generators validated: JSON (5.49 bits/byte), HTML (4.66 bits/byte), Binary (7.69 bits/byte) - all above 3.5 bits/byte Shannon threshold
- Compressed sizes genuinely realistic for multi-layer: 10KB nominal -> 2.7-9.9KB compressed; 100KB nominal -> 22.6-98.8KB compressed
- Gzip/brotli multi-chunk decompression correctness on localhost buffered mock: 600/600 combined (EXP-RUNTIME-35470447407 + EXP-RUNTIME-35456070671)
- Within-state determinism preserved across all cells: decompressed hash all_same=true
- B-COMPRESSED-TARGET-RANGE passes: 3/3 content types achieve realistic compressed sizes

**Critical Limitation (V1_BUFFERED_PROXY_NOT_STREAMING, inherited from EXP-RUNTIME-35495699298, confirmed in EXP-RUNTIME-35513777099):**
The current architecture buffers the full upstream body before re-chunking and the client reassembles before decompressing. The decompressor never observes a chunk boundary. Specifically:
- `ReverseProxyHandler._proxy_request()` calls `upstream_resp.read()` (line 554) to buffer the entire upstream response
- The proxy then re-chunks the buffered body in 32-byte frames (lines 564-575)
- `make_request()` calls `resp.raw.read(decode_content=False)` (line 695) to reassemble the full chunked stream
- `decompress_body()` receives a single contiguous byte string (line 791)

**Why this matters:** Real CDNs (Cloudflare, Fastly, Akamai) serve chunked Transfer-Encoding responses without guaranteeing that the full compressed body is available as a contiguous byte string. If the decompression pipeline fails when chunk boundaries intersect compressed data blocks, the CDN correctness gate is moot.

**The next question (from parent handoff):** "Does iterative decompression correctness hold for streaming incremental decompression where the proxy forwards partial chunked frames without full body reassembly?"

### Why This Is Materially Orthogonal

This experiment tests a different architectural property than the parent:
- **Parent tested:** Can iterative decompression handle stacked compression layers (max_depth>1) when the full body is available?
- **This tests:** Can iterative decompression handle arbitrary chunk boundaries when the body arrives incrementally?

A positive result from the parent does NOT imply streaming correctness: the decompressor's internal state machine may depend on seeing complete compressed blocks, which the buffered path guarantees but the streaming path does not.

## Experimental Design

### Architecture Changes

**Streaming Proxy (new):**
```
class StreamingProxyHandler(BaseHTTPRequestHandler):
    """Forwards upstream chunks directly without buffering the full body."""
    
    def _proxy_request(self, method="GET"):
        # Connect to upstream, forward request
        conn = HTTPConnection(upstream_host, upstream_port)
        conn.request(method, self.path, ...)
        upstream_resp = conn.getresponse()
        
        # Forward status and headers
        self.send_response(upstream_resp.status)
        for key, value in upstream_resp.getheaders():
            self.send_header(key, value)
        self.send_header("X-Proxy-Mode", "STREAMING-PROXY")
        self.end_headers()
        
        # Stream chunks directly: read from upstream, write to client
        while True:
            chunk = upstream_resp.read(STREAM_CHUNK_SIZE)
            if not chunk:
                break
            self.wfile.write(chunk)
        self.wfile.flush()
```

Key difference from parent: no `resp_body = upstream_resp.read()` buffering. Chunks flow through as they arrive.

**Streaming Client (new):**
```
def make_request_streaming(url, auth_header=None, stream_chunk_size=8192):
    """Read response incrementally, accumulate raw bytes."""
    resp = requests.get(url, headers=headers, stream=True)
    chunks = []
    while True:
        chunk = resp.raw.read(stream_chunk_size)
        if not chunk:
            break
        chunks.append(chunk)
    raw_bytes = b"".join(chunks)
    return {"body": raw_bytes, ...}
```

Key difference from parent: reads in `stream_chunk_size` increments instead of `resp.raw.read(decode_content=False)` which reassembles the full chunked stream.

### Test Matrix

**Main streaming cells (24 cells, 120 observations each path):**
| Content Type | Encoding | Size | Chunk Size |
|-------------|----------|------|------------|
| JSON | GZIP-THEN-BROTLI | 10KB | 8192 (8KB CDN) |
| JSON | GZIP-THEN-BROTLI | 10KB | 32 (stress) |
| JSON | BROTLI-THEN-GZIP | 10KB | 8192 |
| JSON | BROTLI-THEN-GZIP | 10KB | 32 |
| JSON | GZIP-THEN-BROTLI | 100KB | 8192 |
| JSON | GZIP-THEN-BROTLI | 100KB | 32 |
| JSON | BROTLI-THEN-GZIP | 100KB | 8192 |
| JSON | BROTLI-THEN-GZIP | 100KB | 32 |
| HTML | GZIP-THEN-BROTLI | 10KB | 8192 |
| HTML | GZIP-THEN-BROTLI | 10KB | 32 |
| HTML | BROTLI-THEN-GZIP | 10KB | 8192 |
| HTML | BROTLI-THEN-GZIP | 10KB | 32 |
| HTML | GZIP-THEN-BROTLI | 100KB | 8192 |
| HTML | GZIP-THEN-BROTLI | 100KB | 32 |
| HTML | BROTLI-THEN-GZIP | 100KB | 8192 |
| HTML | BROTLI-THEN-GZIP | 100KB | 32 |
| BINARY | GZIP-THEN-BROTLI | 10KB | 8192 |
| BINARY | GZIP-THEN-BROTLI | 10KB | 32 |
| BINARY | BROTLI-THEN-GZIP | 10KB | 8192 |
| BINARY | BROTLI-THEN-GZIP | 10KB | 32 |
| BINARY | GZIP-THEN-BROTLI | 100KB | 8192 |
| BINARY | GZIP-THEN-BROTLI | 100KB | 32 |
| BINARY | BROTLI-THEN-GZIP | 100KB | 8192 |
| BINARY | BROTLI-THEN-GZIP | 100KB | 32 |

Each cell: 4 auth states x 5 reps = 20 observations per path (streaming + buffered).

**Total observations:** 24 cells x 20 = 480 streaming + 480 buffered = 960.

**Regression baselines (6 cells, 120 observations per path):**
- JSON_GZIP-SINGLE_10240B, HTML_GZIP-SINGLE_10240B, BINARY_GZIP-SINGLE_10240B (single-layer gzip)
- JSON_BROTLI-SINGLE_10240B, HTML_BROTLI-SINGLE_10240B, BINARY_BROTLI-SINGLE_10240B (single-layer brotli)

**Identity baselines (6 cells, 120 observations per path):**
- JSON_IDENTITY-10KB_10240B, HTML_IDENTITY-10KB_10240B, BINARY_IDENTITY-10KB_10240B
- JSON_IDENTITY-100KB_102400B, HTML_IDENTITY-100KB_102400B, BINARY_IDENTITY-100KB_100KB

### Verification Protocol

For each observation:
1. Make request through streaming proxy, accumulate chunks incrementally
2. Decompress streaming body with iterative `decompress_body()`
3. Make request through buffered proxy (same upstream server, same state)
4. Decompress buffered body with iterative `decompress_body()`
5. Compute expected body from `generate_*_body(state, target_size)`
6. Record three hashes: `streaming_hash`, `buffered_hash`, `expected_hash`
7. Correctness requires: `streaming_hash == buffered_hash == expected_hash`

### Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
- **C1:** `streaming_decompressed_hash == buffered_decompressed_hash` for ALL multi-layer streaming cells (byte-identical streaming vs buffered)
- **C2:** `streaming_decompressed_hash == expected_hash` for ALL multi-layer streaming cells (streaming matches ground truth)
- **C3:** B-GZIP-SINGLE-LAYER-REGRESSION and B-BROTLI-SINGLE-LAYER-REGRESSION pass 100% in both paths (regression controls)
- **C4:** null_control passes (all_same=true for all states in all streaming cells)
- **C5:** B-COMPRESSED-TARGET-RANGE passes (at least 2/3 content types >= 2000B at 10KB and >= 5000B at 100KB)

**FALSIFIED** if:
- Any streaming decompressed hash differs from buffered hash, OR
- Any streaming decompressed hash differs from expected hash, OR
- Any decompression error in streaming path

**MEASUREMENT_INVALID** if:
- Infrastructure prevents data collection, OR
- Identity baseline fails, OR
- B-COMPRESSED-TARGET-RANGE fails

### Baseline Descriptions

| ID | Description | Expected |
|----|-------------|----------|
| B-BUFFERED-GROUND-TRUTH | Full-body buffered decompression (parent established 240/240) | 100% correctness |
| B-GZIP-SINGLE-LAYER-REGRESSION | Single-layer gzip at 10KB HE | 100% both paths |
| B-BROTLI-SINGLE-LAYER-REGRESSION | Single-layer brotli at 10KB HE | 100% both paths |
| B-IDENTITY-HE-STREAMING | IDENTITY at 10KB/100KB through streaming proxy | 100% correctness |
| B-COMPRESSED-TARGET-RANGE | Compressed sizes >= 2KB (10KB) / >= 5KB (100KB) | 2/3 content types pass |
| B-RANDOM | Within-state hash determinism | all_same=true |

## Controls

- **Positive control:** B-BUFFERED-GROUND-TRUTH confirms test infrastructure produces correct results under the established buffered path before comparing streaming
- **Null control:** B-RANDOM confirms within-state determinism (all_same=true for all 5 reps per state)
- **Regression controls:** B-GZIP/BROTLI-SINGLE-LAYER-REGRESSION confirm single-layer pipeline not degraded by streaming proxy changes

## Validity Threats

1. **STREAM_CHUNK_SIZE selection:** If the streaming client's read chunk size does not align with the proxy's forwarding chunk size, the client may reassemble implicitly. Mitigation: use `resp.raw.read(1)` or small fixed read size to force incremental processing.
2. **Python requests library buffering:** `requests` with `stream=True` may buffer internally. Mitigation: use `resp.raw.read(chunk_size)` directly, not `resp.iter_content()`.
3. **BROTLI streaming state:** Brotli decompressor may require complete Brotli frames, not arbitrary byte splits. This is the scientific question being tested.
4. **BINARY cross-run reproducibility:** PYTHONHASHSEED-dependent hash(state) in body header (inherited V3 from parent). Mitigation: record PYTHONHASHSEED, compare streaming vs buffered within same process.
5. **Same-process oracle:** Correctness oracle uses in-process generator (inherited V6 from parent). Bounded: correctness means "matches deterministic generator", not "matches independent corpus".

## Consequences

**Positive outcome:** Streaming decompression is validated. The proxy can forward partial chunked frames without full body reassembly, and decompression correctness is preserved. This resolves V1_BUFFERED_PROXY_NOT_STREAMING, unblocking the CDN correctness gate. Next step: real CDN infrastructure testing (Cloudflare/Fastly/Akamai free tier).

**Negative outcome:** Streaming decompression fails. Chunk boundaries corrupt the decompression state machine. The decompression pipeline requires streaming-aware redesign. Diagnosis required: incremental decompression state machine failure, chunk-boundary dictionary references, or cross-layer state contamination. CDN testing blocked until resolved.

## Estimated Cost

~960 HTTP requests to localhost mock server (480 streaming + 480 buffered), <15 minutes execution, no external infrastructure, no API costs.

## Expected Information Gain

High. This experiment directly tests the V1_BUFFERED_PROXY_NOT_STREAMING limitation inherited from the parent chain. The parent established 240/240 multi-layer correctness but explicitly noted that chunk boundaries never intersect compression layers. Streaming correctness is architecturally orthogonal to multi-layer correctness and cannot be inferred from the parent's results. Either outcome is highly decision-relevant for the C-MEAS-VALID Product Core readiness path.
