# EXP-RUNTIME-35445595071 — Multi-Chunk Brotli Reassembly Report

## Summary

**Outcome: SUPPORTS** — Iterative decompression (brotli→gzip→identity, max_depth=5) correctly reassembles and decompresses brotli payloads that span multiple HTTP chunks. All 5 frozen decision-rule conditions pass. All 7 controls pass. The V2 single-chunk degeneracy blocker is removed.

## Raw Evidence

- **480 total requests** across 3 content types (JSON, HTML, XML) × 2 chunk configurations × 4 auth states × 20 reps
- **MULTI-CHUNK (chunk_size=32 bytes)**: compressed payloads range 70–173 bytes, spanning 3–6 chunks per request
- **SINGLE-CHUNK (chunk_size=1024 bytes)**: all compressed payloads fit in one chunk (parent baseline regression)
- **Origin**: serves Transfer-Encoding: chunked without Content-Length for ALL cells (C_ORIGIN_VERIFICATION 9/9 pass)
- **0 decompression errors** across all 480 requests

## Decision Rule Evaluation

| Condition | Required | Observed | Pass? |
|---|---|---|---|
| (1) decompressed_body_only_discrimination ≥ 0.3 for ALL multi-chunk cells | ≥ 0.3 | min = 0.5 (all 3 cells) | ✅ |
| (2) decompressed hash determinism all_same=true for ALL states × ALL conditions | all_same | 4/4 states × 6 cells = all true | ✅ |
| (3) B-RANDOM = 0.0 for ALL cells | = 0.0 | 0.0 for all 6 cells | ✅ |
| (4) 0 decompression errors across ALL requests | = 0 | 0 | ✅ |
| (5) multi-chunk discrimination ≥ 0.3 for ALL cells | ≥ 0.3 | min = 0.5 (all 3 cells) | ✅ |

**Result**: SURVIVES_CURRENT_TEST — all 5 conditions satisfied.

## Controls

| Control | Expected | Observed | Pass? |
|---|---|---|---|
| C_NULL_CONTROL | B-RANDOM ≈ 0.0 | all 0.0 | ✅ |
| C_SINGLE_CHUNK_REGRESSION | decompressed disc ≥ 0.5 | mean = 0.5 | ✅ |
| C_MULTI_CHUNK_PRIMARY | decompressed disc ≥ 0.3 | min = 0.5 | ✅ |
| C_COMPRESSED_SIZE_VERIFICATION | all payloads > 32 bytes | JSON 70-83, HTML 172-173, XML 161-165 | ✅ |
| C_DECOMPRESSED_DETERMINISM | all_same = true | 4/4 states true | ✅ |
| C_NO_ERROR_INFLATION | 0 errors | 0 | ✅ |
| C_ORIGIN_VERIFICATION | TE:chunked, no CL | 3/3 content types verified | ✅ |

## Interpretation

### Mechanism

The hypothesis is confirmed: HTTP chunked transfer-encoding is a framing layer above the application data. The HTTP client reassembles chunks into a contiguous byte stream before the decompression layer sees it. Broli decompression operates on the reassembled contiguous stream. Therefore, chunk boundaries that split brotli compressed data do not corrupt decompression.

### Evidence strength

- **Compressed payload sizes** (70–173 bytes) with chunk_size=32 force 3–6 chunks per request, confirming genuine multi-chunk splitting
- **Determinism**: all_same=true for all states across all conditions — each auth state produces identical decompressed hash regardless of chunk boundary positions
- **Discrimination**: 0.5 across all cells, matching the structural ceiling from 3-way error collapse (no_auth/expired/invalid share identical bodies)
- **Regression**: SINGLE-CHUNK baseline reproduces parent result (discrimination = 0.5)

### What this removes

The parent experiment (EXP-RUNTIME-35434773328) had audit finding V2: "all compressed body_sizes 70-176 bytes fit in a single chunk (chunk_size=1024), so multi-chunk brotli boundary splitting is untested." This experiment directly resolves V2. The `do_not_assume` item "Multi-chunk reassembly works" is now established for localhost mock infrastructure with chunk_size=32.

### What remains unknown

1. **Real CDN infrastructure** (Cloudflare/Fastly/Akamai) with Accept-Encoding negotiation, quality variation, geographic latency — the sole remaining blocker for C-MEAS-VALID product readiness
2. **Larger payloads** (10KB, 100KB) where chunk boundaries may split brotli dictionary references across larger compressed streams
3. **gzip encoding** under multi-chunk splitting (only brotli tested)
4. **CDN-specific chunking algorithms** that may differ from Python's chunked writer

### Claim ceiling

This experiment establishes that multi-chunk brotli reassembly works on localhost with:
- chunk_size=32 bytes (forcing 3–6 chunks per 70–173 byte compressed payload)
- brotli quality 6
- 1KB uncompressed JSON/HTML/XML with synthetic padding
- 4 auth states with 3-way error collapse
- Python 3.12.14 + brotli 1.2.0 + requests 2.34.2
- Origin serves chunked without Content-Length
- Client sends Accept-Encoding: br, gzip, identity

Does NOT establish: behavior under real CDN, larger payloads, gzip multi-chunk, Accept-Encoding negotiation, geographic latency, production-scale concurrency.
