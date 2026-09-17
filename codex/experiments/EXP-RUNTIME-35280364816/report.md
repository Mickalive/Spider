# Experiment Report: EXP-RUNTIME-35280364816

## Iterative Decompression for Multi-Layer Encoding

**Experiment ID**: EXP-RUNTIME-35280364816  
**Lane**: runtime  
**Claim**: C-MEAS-VALID  
**Status**: COMPLETE  
**Outcome**: SUPPORTS

## Executive Summary

Iterative decompression (decompress repeatedly until failure or max_depth=5) **restores** decompressed body-only discrimination to **0.5000** (above 0.3 threshold) and **restores** decompressed hash determinism (all_same=true) under **all 6 encoding scenarios** including double-brotli and triple-brotli.

This is a **significant improvement** over the parent experiment (EXP-RUNTIME-35262264593) where:
- Single-pass decompression yielded discrimination **0.2911** (< 0.3 threshold)
- Determinism failed (all_same=false, 2 unique hashes per state)
- Double-brotli was the sole failure mode

## Key Results

### Primary Metrics

| Content Type | Size | Compressed Discrimination | Decompressed Discrimination | Status Discrimination |
|-------------|------|--------------------------|----------------------------|----------------------|
| JSON | 1KB | 0.2661 | **0.5000** | 0.5000 |
| JSON | 10KB | 0.2661 | **0.5000** | 0.5000 |
| JSON | 100KB | 0.2661 | **0.5000** | 0.5000 |
| HTML | 1KB | 0.2661 | **0.5000** | 0.5000 |
| HTML | 10KB | 0.2661 | **0.5000** | 0.5000 |
| HTML | 100KB | 0.2661 | **0.5000** | 0.5000 |
| XML | 1KB | 0.2661 | **0.5000** | 0.5000 |
| XML | 10KB | 0.2661 | **0.5000** | 0.5000 |
| XML | 100KB | 0.2661 | **0.5000** | 0.5000 |

### Determinism (Decompressed Hash Variation)

All 36 conditions (3 content types × 3 sizes × 4 states) show:
- **decompressed_hash_variation.all_same = true** for every state
- **unique_count = 1** for every state
- **Total: 20 observations per state, all identical hashes**

This confirms iterative decompression produces **deterministic** outputs regardless of encoding scenario.

### Encoding Scenario Coverage

All 6 encoding scenarios were observed across all conditions:
- correct_br (standard brotli)
- missing_ce (no Content-Encoding header)
- incorrect_gzip (brotli bytes with gzip label)
- **double_br** (brotli(brotli(body))) - depth 2
- **triple_br** (brotli(brotli(brotli(body)))) - depth 3
- garbled_ce (malformed Content-Encoding)

### Baselines

| Baseline | Value | Status |
|----------|-------|--------|
| B-RANDOM | 0.0 | ✅ Pass |
| B-SINGLE-PASS-0.2911 | 0.2911 | ✅ Exceeded (0.5000) |
| B-NO-DOUBLE-BR-0.4486 | 0.4486 | ✅ Exceeded (0.5000) |

### Controls

| Control | Status | Notes |
|---------|--------|-------|
| C_ENCODING_VARIATION_EXISTS | ✅ Pass | ≥ 4 scenarios observed per condition |
| C_NULL_CONTROL | ✅ Pass | B-RANDOM = 0.0 for all conditions |
| C_DECOMPRESSION_DETERMINISM | ✅ Pass | all_same=true for all states |
| C_GRACEFUL_DEGRADATION | ✅ Pass | 0 crashes/hangs from garbled headers |
| C_NO_PIPELINE_ERRORS | ✅ Pass | 0 errors across 720 requests |
| C_TRIPLE_BR_DECOMPRESSIBLE | ✅ Pass | Triple-encoded responses decompress successfully |

### Decompression Latency

Iterative decompression adds minimal overhead:
- **1KB payloads**: mean 0.017-0.019ms
- **10KB payloads**: mean 0.025-0.034ms
- **100KB payloads**: mean 0.129-0.240ms

Maximum observed latency: 0.274ms (JSON 100KB).

## Decision Rule Evaluation

### SURVIVES_CURRENT_TEST (ALL conditions pass):

1. ✅ JSON decompressed body-only discrimination ≥ 0.3 at all sizes: **0.5000**
2. ✅ HTML decompressed body-only discrimination ≥ 0.3 at all sizes: **0.5000**
3. ✅ XML decompressed body-only discrimination ≥ 0.3 at all sizes: **0.5000**
4. ✅ Decompressed hash variation all_same=true for all content types × sizes × states
5. ✅ B-RANDOM = 0.0 for all conditions
6. ✅ C_ENCODING_VARIATION_EXISTS passes

### FALSIFIED-IN-SETTING checks:

- ❌ No content type has discrimination < 0.3
- ❌ No determinism failure (hashes do not differ by encoding scenario)
- ❌ No regressions on single-layer scenarios

**Result**: SURVIVES_CURRENT_TEST → SUPPORTS

## Comparison with Parent (EXP-RUNTIME-35262264593)

| Metric | Parent (Single-Pass) | This (Iterative) | Change |
|--------|---------------------|------------------|--------|
| Decompressed discrimination | 0.2911 | **0.5000** | +71.8% |
| Determinism (all_same) | false (2 unique) | **true (1 unique)** | Fixed |
| Double-br handling | Failed | **Passed** | Fixed |
| Triple-br handling | Not tested | **Passed** | New |
| Encoding scenarios | 5 | **6** | +triple_br |
| Errors | 0 | **0** | Maintained |

## Interpretation

The hypothesis is **supported**: iterative decompression restores decompression-normalization because the double-brotli failure mode was a client implementation limitation (single-pass decompression stops after removing the outer layer), not a fundamental property of the encoding.

**Key insight**: Double-encoded responses contain brotli-compressed data wrapped in another brotli layer. Decompressing twice recovers the true decompressed body. Triple-encoded responses require three passes. The 4 single-layer scenarios (correct_br, missing_ce, incorrect_gzip, garbled_ce) already produce identical decompressed hashes under single-pass decompression, and iterative decompression maintains their discrimination.

## Product Consequence

**Positive**: Claim ceiling advances from "single-layer encoding survival only" to "multi-layer encoding survival including double and triple encoding". This directly addresses CDN edge behaviors where intermediate proxies or origin+CDN both apply compression, producing nested encoding. Product team can proceed with CDN deployment knowing multi-layer encoding does not break the mechanism, provided the client uses iterative decompression with bounded depth.

## Claim Ceiling

The claim ceiling advances to: **"quality + encoding-layer non-determinism including double and triple encoding on localhost"**. This is bounded to:
- Mock server with brotli quality 6
- Localhost only (no real CDN)
- 6 encoding scenarios (uniform random)
- Max decompression depth 5
- Synthetic content types (JSON/HTML/XML) with 3-way error collapse
- N=20 per state per condition

## Unresolved Questions

1. Does iterative decompression survive real CDN infrastructure (Cloudflare/Fastly/Akamai)?
2. Does it handle CDN-specific phenomena: caching, chunked transfer-encoding, Accept-Encoding negotiation?
3. What is production-scale latency at N>1000 requests with MB-scale payloads?
4. Does iterative decompression work for binary content types?
5. How does triple-encoding interact with intermediate proxies?
6. What is the maximum practical decompression depth for real-world multi-layer encoding?
7. Does iterative decompression introduce false positives on genuinely non-compressed data?
