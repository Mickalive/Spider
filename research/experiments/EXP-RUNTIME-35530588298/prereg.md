# EXP-RUNTIME-35530588298 — Preregistration

## Title

True Incremental Decompressor Streaming Correctness Under Multi-Layer Encodings

## Lane

runtime

## Claim

C-MEAS-VALID (Measurement substrate is intervention-valid)

## Question

Does iterative decompression correctness hold when compressed data is fed chunk-by-chunk to streaming decompressor APIs (`brotli.Decompressor.process`, `gzip.GzipFile`) without full accumulation, such that the decompressor state machine across arbitrary block boundaries produces byte-identical output to full-body decompression for multi-layer encodings at realistic CDN chunk sizes (8KB+) and stress chunk sizes (32B)?

## Motivation

Parent experiment EXP-RUNTIME-35522287921 established 840/840 streaming decompression correctness at the HTTP Transfer-Encoding framing layer. However, the parent explicitly noted that `decompress_body` is called on **accumulated bytes** after the streaming proxy forwards all chunks — the decompressor never observes a chunk boundary during processing. The parent's carry_forward unknown #2 asks:

> Does correctness hold for true incremental decompression where decompress_body is fed chunk-by-chunk via streaming decompressor APIs (brotli.Decompressor.process, gzip streaming) without full accumulation?

This is a prerequisite for CDN testing: real CDNs serve data incrementally, and if the decompressor state machine fails across block boundaries, CDN testing would be meaningless. This experiment is materially orthogonal to the TE framing test and cannot be inferred from it.

## Hypothesis

H1: `brotli.Decompressor().process(chunk)` fed CHUNK_SIZE chunks then `.flush()` produces byte-identical output to `brotli.decompress(full_data)` for all cell configurations.

H2: `gzip.GzipFile(io.BytesIO(compressed)).read(CHUNK_SIZE)` loops produce byte-identical output to `gzip.decompress(full_data)` for all cell configurations.

H3: Multi-layer streaming decompression (outer layer via streaming API, then inner layer via streaming API on the result) produces byte-identical output to full-body multi-layer decompression.

## Falsifier

Any `SHA256(streaming_decompressed) != SHA256(fullbody_decompressed)` across all observations for any (size, encoding, content_type, state, chunk_size) cell, OR any decompression error/exception in the streaming API path, OR any silent fallback (`streaming_decompressed == raw_compressed` bytes) for any compressed response.

## Experimental Design

### 1. Payload Generation

Reuse validated high-entropy generators from parent EXP-RUNTIME-35522287921:

- `generate_json_he_body(state, target_size)`: JSON with UUIDs, random floats, Shannon entropy ~5.5 bits/byte
- `generate_html_he_body(state, target_size)`: HTML with real Wikipedia paragraphs, Shannon entropy ~4.7 bits/byte
- `generate_binary_he_body(state, target_size)`: Structured random payloads, Shannon entropy ~7.7 bits/byte

States: `no_auth`, `valid_token`, `expired_token`, `invalid_token` (4 states)
Sizes: 10KB (10240 bytes), 100KB (102400 bytes)
Reps per cell: 5

### 2. Compression Configurations

Multi-layer (primary):
- GZIP-THEN-BROTLI: `body -> gzip.compress(level=1) -> brotli.compress(quality=4)`
- BROTLI-THEN-GZIP: `body -> brotli.compress(quality=4) -> gzip.compress(level=1)`

Single-layer (regression):
- GZIP-SINGLE: `body -> gzip.compress(level=None)` (default level)
- BROTLI-SINGLE: `body -> brotli.compress(quality=6)`

IDENTITY (oracle validation):
- `body` passed through unchanged

### 3. Decompression Paths

**Full-body path** (ground truth):
```python
# Single layer
decompressed = brotli.decompress(compressed_data)  # or gzip.decompress
# Multi-layer (outer first)
inner_compressed = brotli.decompress(compressed_data)  # outer
decompressed = gzip.decompress(inner_compressed)       # inner
```

**Streaming API path** (test):
```python
# Brotli streaming
d = brotli.Decompressor()
for i in range(0, len(compressed_data), chunk_size):
    chunk = compressed_data[i:i+chunk_size]
    output_parts.append(d.process(chunk))
output_parts.append(d.flush())
streaming_result = b''.join(output_parts)

# Gzip streaming
import io
buf = io.BytesIO(compressed_data)
gz = gzip.GzipFile(fileobj=buf)
parts = []
while True:
    chunk = gz.read(chunk_size)
    if not chunk:
        break
    parts.append(chunk)
streaming_result = b''.join(parts)
```

**Multi-layer streaming**: Feed outer compressed data to outer streaming decompressor, collect inner compressed bytes, feed inner compressed bytes to inner streaming decompressor.

### 4. Chunk Sizes

- 8192 bytes: realistic CDN frame size (Cloudflare default)
- 32 bytes: stress test, maximizes chunk count and block boundary crossings

### 5. Cells

| Size | Encoding | Content Type | States | Reps | Chunk Sizes | Streaming Cells |
|------|----------|-------------|--------|------|-------------|----------------|
| 10KB, 100KB | GZIP-THEN-BROTLI, BROTLI-THEN-GZIP | JSON, HTML, BINARY | 4 | 5 | 8192, 32 | 2x2x3x4x5x2 = 480 |

Plus baselines: 120 single-layer + 120 identity = 240
Total: ~720 in-process comparisons (no HTTP needed)

## Controls

### Positive Control
B-FULLBODY-GROUND-TRUTH: full-body decompression correctness oracle validated via SHA256 match against generate_*_body(). Must pass 100% to confirm test infrastructure is functional.

### Regression Controls
B-GZIP-SINGLE-LAYER-REGRESSION: single-layer gzip streaming decompressor at 10KB.
B-BROTLI-SINGLE-LAYER-REGRESSION: single-layer brotli streaming decompressor at 10KB.

### Null Control
Within-state determinism: decompressed_hash must be identical across all 5 repetitions for each cell. Any variation indicates non-deterministic decompression.

### Identity Baseline
B-IDENTITY-HE-STREAMING: uncompressed high-entropy data fed through streaming path. Validates byte-preservation.

### Compressed Size Validation
B-COMPRESSED-TARGET-RANGE: at least 2/3 content types achieve mean compressed_size_bytes >= 2000 at 10KB and >= 5000 at 100KB under multi-layer encoding.

## Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
- C1: `streaming_hash == fullbody_hash` for ALL multi-layer streaming cells
- C2: `streaming_hash == expected_hash` for ALL multi-layer streaming cells
- C3: B-GZIP-SINGLE-LAYER-REGRESSION and B-BROTLI-SINGLE-LAYER-REGRESSION pass 100%
- C4: null_control passes (all_same=true for all states in all streaming cells)
- C5: B-COMPRESSED-TARGET-RANGE passes

**FALSIFIED** if any streaming decompressed hash differs from fullbody hash, or any decompression error in streaming API path.

**MEASUREMENT_INVALID** if infrastructure prevents data collection, identity baseline fails, or B-COMPRESSED-TARGET-RANGE fails.

## Validity Threats

1. **brotli.Decompressor.process() may buffer internally**: The brotli streaming API may buffer data internally and only produce output when a complete block is available. This is expected behavior, not a failure — the output must still match full-body decompression byte-for-byte.

2. **Multi-layer unwrapping order**: The outer decompressor must complete before the inner decompressor can begin. In streaming mode, this means collecting all outer decompressed bytes (which are inner compressed bytes) before feeding to inner decompressor. This is a sequential requirement, not a parallel one.

3. **Flush semantics**: `brotli.Decompressor().flush()` must be called to finalize output. Forgetting flush may produce truncated output — this would be caught by the correctness check.

4. **gzip multi-member**: gzip files may contain multiple members. The test uses single-member compressed data, consistent with parent.

## Product Consequence

**Positive**: True incremental decompressor streaming validated. Resolves V1_STREAMING_DECOMPRESSOR_POST_ACCUMULATION. Unblocks CDN correctness gate. Real CDNs serve data incrementally; decompressor streaming correctness is prerequisite for real-CDN testing and true incremental proxy operation.

**Negative**: Streaming decompressor APIs fail correctness. The decompressor state machine has a streaming failure mode not exposed by accumulated-byte testing. CDN testing blocked. Diagnosis required: block-boundary handling, dictionary window references, flush semantics, or cross-layer state contamination.

## Estimated Cost

Low: ~720 in-process decompression comparisons, no HTTP requests, no external infrastructure, <5 minutes execution.
