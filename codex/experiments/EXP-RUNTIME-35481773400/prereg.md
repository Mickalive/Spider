# EXP-RUNTIME-35481773400 — Preregistration

## Experiment Metadata

- **Experiment ID**: EXP-RUNTIME-35481773400
- **Lane**: runtime
- **Claim IDs**: C-MEAS-VALID
- **Created**: 2026-09-20T01:35:29.668700+00:00
- **Parent**: EXP-RUNTIME-35470447407

## 1. Question

Does iterative decompression correctness (byte-identical output to ground-truth uncompressed body) hold for larger payloads (10KB, 100KB) across gzip compression level extremes (levels 1 and 9) and brotli quality extremes (quality 4 and 8) on localhost buffered proxy with chunked transfer-encoding?

## 2. Hypothesis

Iterative decompression (brotli->gzip->identity, max_depth=5) produces byte-identical output to ground-truth `generate_*_body(state, target_size)` for all 4 auth states, 3 content types (JSON/HTML/XML), 2 payload sizes (10KB, 100KB), and 4 compression configurations (gzip level 1, gzip level 9, brotli quality 4, brotli quality 8) with multi-chunk framing (chunk_size=32), served through localhost buffered proxy with chunked transfer-encoding.

## 3. Background and Motivation

The parent (EXP-RUNTIME-35470447407) established gzip multi-chunk decompression correctness at 240/240 observations with 1KB nominal payloads, combined with established brotli correctness (480/480 total). However, the compressed sizes tested were 95-233 bytes (gzip) and 70-173 bytes (brotli), spanning only 3-8 chunks at chunk_size=32.

At 10KB nominal payload, gzip compressed sizes are typically 2-10KB, spanning 60-300+ chunks. At 100KB nominal, compressed sizes are ~20-50KB, spanning 600-1500+ chunks. These larger compressed sizes stress chunk-boundary handling far more aggressively than the1KB tests. Gzip dictionary references may cross many chunk boundaries, and brotli back-reference dictionaries may span different chunk structures.

Compression level extremes (gzip level 1 vs 9, brotli quality 4 vs 8) produce maximally different compressed structures. Level 1 produces larger, less-compressed output with different dictionary patterns than level 9. These extremes are most likely to reveal level-dependent failure modes.

The parent handoff identified larger payloads as a specific unknown: "Does correctness hold for larger payloads (10KB, 100KB) where gzip/brotli dictionary references cross many chunk boundaries and compressed sizes span 100+ chunks at 32 bytes?"

## 4. Experimental Design

### 4.1 Test Matrix

| Factor | Levels |
|--------|--------|
| Payload size | 10KB (10240 bytes), 100KB (102400 bytes) |
| Content type | JSON, HTML, XML |
| Compression | gzip level 1, gzip level 9, brotli quality 4, brotli quality 8 |
| Auth state | no_auth, valid_token, expired_token, invalid_token |
| Chunk mode | multi-chunk (chunk_size=32) |
| Reps per cell | 5 |

Total test observations: 2 sizes x 3 types x 4 compressions x 4 states x 5 reps = **480 observations**

### 4.2 Baselines and Controls

**Regression controls (1KB, reuse from parent):**
- B-GZIP-MC-1KB: Gzip multi-chunk at1KB (expected: 100% correctness, 240/240 from parent)
- B-BROTLI-MC-1KB: Brotli multi-chunk at 1KB (expected: 100% correctness, 480/480 from parent)

**Correctness oracle baselines:**
- B-IDENTITY-10KB: No compression at10KB (expected: SHA256 matches generate_*_body exactly)
- B-IDENTITY-100KB: No compression at100KB (expected: SHA256 matches generate_*_body exactly)

**Null control:**
- B-RANDOM: Within-state decompressed hash must be deterministic (all_same=true for all states in all cells)

**Positive control:**
- B-BROTLI-MC-1KB must pass 100% (confirms no pipeline regression)

### 4.3 Infrastructure

- Localhost mock OAuth2 server (Flask) on ports 8700-8702/8800-8802
- Python reverse proxy on intermediate ports
- Same mock server as parent experiments
- chunk_size=32 for multi-chunk framing
- Request jitter 50-150ms uniform
- Seed 44 for deterministic server behavior

### 4.4 Observations per Cell

Each cell = (size, content_type, compression, auth_state)
- 5 reps per cell
- 480 total test observations
- Plus ~40 regression/baseline observations

## 5. Measurement Procedure

1. Start mock OAuth2 server with deterministic body generation for10KB and 100KB payloads
2. Start buffered reverse proxy with iterative decompression pipeline
3. For each (size, type, compression, state) cell:
   a. Generate ground-truth body: `SHA256(generate_*_body(state, target_size))`
   b. Send 5 requests with appropriate Accept-Encoding and Authorization headers
   c. Record: raw compressed bytes, decompressed bytes, response headers
   d. Compute: `SHA256(decompressed)`, compare to ground-truth
   e. Classify: correctness_match (SHA256 match), silent_fallback (decompressed == compressed)
4. For baselines: same procedure with no compression (IDENTITY) and 1KB payloads (regression)
5. Aggregate per-cell metrics: correctness_match_rate, silent_fallback_count, decompressed_hash_variation

## 6. Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
- **C1**: `correctness_match_rate == 1.0` for ALL cells across all size x compression x content_type combinations
- **C2**: `silent_fallback_count == 0` for ALL cells
- **C3**: B-GZIP-MC-1KB and B-BROTLI-MC-1KB pass 100% (regression controls)
- **C4**: null_control passes (all_same=true for all states in all cells)

**FALSIFIED** if any correctness failure OR any silent fallback in any cell.

**MEASUREMENT_INVALID** if infrastructure prevents data collection or if correctness oracle baseline (B-IDENTITY) fails for any size.

## 7. Validity Threats

1. **Server determinism**: Flask with seeded RNG should produce deterministic bodies, but 10KB/100KB payloads with padding may have subtle non-determinism. Mitigated by B-IDENTITY baselines and null_control.
2. **Buffer overflow**: The proxy buffers entire upstream then re-chunks; larger payloads may exceed buffer limits. This is a legitimate failure mode to detect.
3. **Compression library bugs**: brotli 1.2.0 or Python gzip may have size-dependent bugs. This is a legitimate failure mode.
4. **Chunk boundary corruption**: At 300+ chunks, multi-byte gzip/brotli symbols spanning chunk boundaries may be corrupted. This is the primary hypothesis being tested.
5. **Timeout**: 100KB responses may take longer to compress/decompress. Mitigated by generous timeout settings.

## 8. Scope and Generalization

This experiment extends the parent's1KB correctness result to realistic web content sizes. If SURVIVES, the claim ceiling advances to include 10KB-100KB payloads under compression level variation on localhost.

**NOT tested in this experiment:**
- Real CDN infrastructure (Cloudflare/Fastly/Akamai) — the critical remaining product gate
- Streaming partial-frame forwarding (proxy buffers entire response)
- Multi-layer encoding (gzip->brotli, max_depth=5 only exercises depth 1)
- Production OAuth/OIDC middleware
- Concurrent clients or production-scale request rates
- Binary content types (only JSON/HTML/XML)
- Gzip levels 2-8 and brotli quality 5-7 (only extremes tested)
