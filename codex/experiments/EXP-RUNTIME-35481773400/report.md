# EXP-RUNTIME-35481773400 — Execution Report

## Executive Summary

**Outcome: SURVIVES_CURRENT_TEST — 720/720 correctness passes, 0 failures, 0 silent fallbacks, 0 decompression errors across all 36 experimental cells.**

All four frozen decision-rule conditions pass:

- **C1**: `correctness_match_rate == 1.0` for ALL 24 main cells (480/480 observations)
- **C2**: `silent_fallback_count == 0` for ALL main cells
- **C3**: B-GZIP-MC-1KB and B-BROTLI-MC-1KB pass 100% (120/120 regression, no pipeline degradation)
- **C4**: null_control passes (all_same=true for all 4 states across all 24 main cells)

IDENTITY baselines (correctness oracle) pass 100% at both 10KB (60/60) and 100KB (60/60).

Audit PASS confirms recomputed metrics match producer.

## Detailed Results

### Phase 1: Main Experimental Cells (2 sizes × 3 types × 4 compressions × 5 reps = 480 observations)

| Size | Type | GZIP-L1-MC | GZIP-L9-MC | BROTLI-Q4-MC | BROTLI-Q8-MC |
|------|------|-----------|-----------|-------------|-------------|
| 10KB | JSON | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ |
| 10KB | HTML | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ |
| 10KB | XML  | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ |
| 100KB | JSON | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ |
| 100KB | HTML | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ |
| 100KB | XML  | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ |

### Phase 2: Regression Controls (1KB, 60 observations)

| Type | GZIP-MC-1KB | BROTLI-MC-1KB |
|------|------------|--------------|
| JSON | 20/20 ✓ | 20/20 ✓ |
| HTML | 20/20 ✓ | 20/20 ✓ |
| XML  | 20/20 ✓ | 20/20 ✓ |

### Phase 3: IDENTITY Baselines (correctness oracle, 120 observations)

| Size | JSON | HTML | XML |
|------|------|------|-----|
| 10KB | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ |
| 100KB | 20/20 ✓ | 20/20 ✓ | 20/20 ✓ |

### Compressed Sizes (mean, bytes)

| Size | Type | GZIP-L1 | GZIP-L9 | BROTLI-Q4 | BROTLI-Q8 |
|------|------|---------|---------|-----------|-----------|
| 10KB | JSON | 152 | 116 | 77 | 75 |
| 10KB | HTML | 329 | 271 | 198 | 178 |
| 10KB | XML | 320 | 263 | 186 | 166 |
| 100KB | JSON | 554 | 205 | 77 | 76 |
| 100KB | HTML | 1036 | 551 | 198 | 178 |
| 100KB | XML | 1058 | 588 | 186 | 166 |

### Decompression Latency (mean, ms)

All decompression latencies were sub-millisecond across all cells (0.01–0.15 ms range), confirming the decompression pipeline has negligible overhead at 10KB–100KB payloads.

## Key Findings

1. **Larger payloads do not break correctness**: The iterative decompression pipeline (brotli→gzip→identity, max_depth=5) produces byte-identical output for 10KB and 100KB payloads across all compression configurations.

2. **Compression level extremes are transparent**: Gzip level 1 (fastest, largest output) and level 9 (slowest, smallest output) both decompress correctly. Brotli quality 4 (minimum) and quality 8 (near maximum) both decompress correctly.

3. **Chunk boundary handling is robust**: At 100KB nominal payload, compressed sizes of 205–1058 bytes span 6–33 chunks at chunk_size=32, and all decompress correctly with no corruption at chunk boundaries.

4. **No size-dependent failure mode detected**: The 100x payload size increase (1KB→100KB) produced no correctness failures, no silent fallbacks, and no decompression errors.

5. **Regression controls pass**: The 1KB conditions from parent EXP-RUNTIME-35470447407 reproduce at 100% correctness, confirming no pipeline regression.

## Interpretation

The frozen hypothesis is supported: iterative decompression correctness (byte-identical output to ground-truth uncompressed body) holds for larger payloads (10KB, 100KB) across gzip compression level extremes (levels 1 and 9) and brotli quality extremes (quality 4 and 8) on localhost buffered proxy with chunked transfer-encoding.

### Claim Ceiling

This experiment advances the C-MEAS-VALID claim ceiling from 1KB to 100KB payloads under compression level variation on localhost. The scope now covers:
- Payload sizes: 1KB–100KB
- Compression formats: gzip (levels 1, 9), brotli (quality 4, 8)
- Content types: JSON, HTML, XML
- Auth states: 4 (no_auth, valid_token, expired_token, invalid_token)
- Chunk framing: chunk_size=32 (multi-chunk)

The sole remaining product-readiness gate for C-MEAS-VALID remains real CDN infrastructure validation (Cloudflare/Fastly/Akamai with auth-aware cache, Accept-Encoding negotiation, multi-layer encoding, geographic latency, and production concurrency).

### What This Experiment Does NOT Establish

- Real CDN correctness (localhost mock only)
- Streaming partial-frame forwarding (proxy buffers entire response)
- Multi-layer encoding (gzip→brotli, only depth 1 exercised)
- Concurrent clients or production-scale request rates
- Binary content types (only JSON/HTML/XML)
- Gzip levels 2–8 and brotli quality 5–7 (only extremes tested)

## Controls Summary

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| C_CORRECTNESS_MATCH | 100% for all cells | 720/720 | ✓ |
| C_SILENT_FALLBACK | 0 for all cells | 0 | ✓ |
| C_REGRESSION_CONTROLS | 100% for 1KB | 120/120 | ✓ |
| C_IDENTITY_BASELINE | 100% for oracle | 120/120 | ✓ |
| C_NULL_CONTROL | all_same=true for all states | true | ✓ |
| C_B_RANDOM | ~0.0 for all cells | 0.0 | ✓ |
| C_NO_ERRORS | 0 errors | 0 | ✓ |

## Decision

**SURVIVES_CURRENT_TEST** — All four frozen decision-rule conditions pass. C-MEAS-VALID claim ceiling advances to include 10KB–100KB payloads under compression level variation on localhost. Real CDN infrastructure remains the final product-readiness gate.
