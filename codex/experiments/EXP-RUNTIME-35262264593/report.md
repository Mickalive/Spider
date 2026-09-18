# Report: EXP-RUNTIME-35262264593 — Encoding-Layer Non-Determinism

## Experiment Summary

**Question**: Does decompression-normalization (SHA256 on decompressed body + status) maintain body-only discrimination ≥ 0.3 under CDN-like encoding-layer non-determinism?

**Answer**: FALSIFIES. Decompression-normalization fails under double-brotli encoding (a realistic CDN scenario where content is compressed twice). The mechanism also fails the determinism requirement: decompressed hashes differ by encoding scenario within the same auth state.

## Key Findings

### 1. Double-Encoding Breaks Decompression (FALSIFIER CONFIRMED)

The `double_br` scenario (brotli bytes wrapped in another brotli layer) produces a **different decompressed hash** than all other scenarios for the same auth state and content type.

**Evidence**: For JSON_1KB valid_token:
- `correct_br`: decompressed_hash = `d15e53a2cc4d32d4...` (correct body)
- `double_br`: decompressed_hash = `ea561a2a9c6efe39...` (STILL COMPRESSED — this is the single-layer brotli hash, not the decompressed body)

**Root cause**: The client decompresses once based on `Content-Encoding: br`. For double-encoded data, one decompression pass strips the outer layer but leaves the inner brotli-compressed data. The resulting "decompressed" output is actually still brotli-compressed, producing a different hash than the truly decompressed body.

**Body size evidence**: `double_br` responses are 87 bytes (valid_token) vs 83 bytes (correct_br) — the 4-byte difference is the brotli framing overhead from the inner compressed layer.

### 2. Four of Five Scenarios Work Correctly

The following encoding scenarios all produce **identical decompressed hashes** for the same auth state:

| Scenario | Content-Encoding | Decompressed Hash | Matches Correct? |
|----------|-----------------|-------------------|-----------------|
| correct_br | `br` | `d15e53a2...` | ✅ Yes |
| missing_ce | `none` | `d15e53a2...` | ✅ Yes |
| incorrect_gzip | `gzip` | `d15e53a2...` | ✅ Yes |
| garbled_ce | `br; quality=invalid` | `d15e53a2...` | ✅ Yes |
| double_br | `br` | `ea561a2a...` | ❌ No |

The client's decompression fallback strategy (brotli → gzip → identity) successfully handles:
- Missing Content-Encoding (tries brotli, succeeds)
- Incorrect gzip label (tries gzip, fails, tries brotli, succeeds)
- Garbled encoding value (tries brotli, succeeds — the semicolon doesn't prevent brotli matching)

### 3. Discrimination Below Threshold

All 9 content-type × size conditions show decompressed body-only discrimination of **0.2911**, which is below the 0.3 threshold.

This is caused by the `double_br` scenario creating 2 unique fingerprints per state instead of 1. With 4 states where each has 2 unique fingerprints (one from correct scenarios, one from double_br), the intra-state match rate increases, reducing discrimination.

### 4. Determinism Failure (Condition 4 Fails)

The frozen decision rule requires `decompressed_hash_variation all_same=true` for all content types × sizes × states. This **FAILS**: every state shows `all_same=false` with 2 unique decompressed hashes per state (one from correct scenarios, one from double_br).

This is not a measurement artifact — it is a genuine determinism failure caused by encoding-layer variation.

## Controls

| Control | Expected | Observed | Pass? |
|---------|----------|----------|-------|
| C_ENCODING_VARIATION_EXISTS | ≥ 3 distinct scenarios per condition | 5/5 scenarios observed | ✅ PASS |
| C_NULL_CONTROL (B-RANDOM) | ~ 0.0 | 0.0 for all conditions | ✅ PASS |
| C_DECOMPRESSION_DETERMINISM | all_same=true | all_same=false for all states | ❌ FAIL |
| C_GRACEFUL_DEGRADATION | No crashes/hangs | 0 errors | ✅ PASS |
| C_NO_PIPELINE_ERRORS | 0 errors | 0 errors | ✅ PASS |

## Decision Rule Evaluation

Per frozen spec.json:

1. ❌ JSON discrimination ≥ 0.3 at all sizes: **FAILS** (0.2911 < 0.3)
2. ❌ HTML discrimination ≥ 0.3 at all sizes: **FAILS** (0.2911 < 0.3)
3. ❌ XML discrimination ≥ 0.3 at all sizes: **FAILS** (0.2911 < 0.3)
4. ❌ Determinism (all_same=true): **FAILS** (double_br creates different hashes)
5. ✅ B-RANDOM = 0.0: **PASSES**
6. ✅ C_ENCODING_VARIATION_EXISTS: **PASSES**

**Result**: FALSIFIED-IN-SETTING — decompressed body-only discrimination < 0.3 for all types at all sizes, AND decompressed hashes differ by encoding scenario.

## Interpretation

### What This Means for the Claim Ceiling

The frozen claim ceiling was "non-deterministic quality only" from the parent experiment. This experiment attempted to advance it to "quality + encoding-layer non-determinism." The experiment **fails** to advance the ceiling.

**Specific failure mode**: Double-brotli encoding is a realistic CDN scenario (e.g., when a CDN edge compresses already-compressed origin responses, or when intermediate proxies add their own compression). The mechanism depends on the client performing the correct number of decompression passes, which is not guaranteed when Content-Encoding headers are corrupted.

### What Works

- **Missing Content-Encoding**: Client fallback correctly decompresses brotli data even without a header
- **Incorrect Content-Encoding label**: Client fallback correctly falls back from gzip to brotli
- **Garbled Content-Encoding**: Client fallback correctly handles malformed headers
- **All non-double scenarios are deterministic**: 4/5 scenarios produce identical decompressed hashes

### What Fails

- **Double-encoding**: Single-pass decompression produces compressed intermediate data, not the original body
- **Discrimination below 0.3**: The double-br scenario dilutes discrimination from0.5 to 0.2911

### Product Consequences

The hypothesis is **falsified in this setting**. Decompression-normalization depends on Content-Encoding headers being at most single-layer corrupted. Double-encoded responses require:
1. Iterative decompression (decompress until decompression fails or a maximum depth is reached)
2. OR Content-Encoding validation before decompression
3. OR rejection of double-encoded responses at the CDN/client layer

Real-CDN deployment is **blocked** for encoding corruption scenarios until the double-encoding failure mode is addressed.

## Scope Boundaries

- Results bounded to localhost mock server with encoding-layer proxy
- No real CDN infrastructure (Cloudflare/Fastly/Akamai) tested
- No chunked transfer-encoding, HTTP/2 framing, or response caching tested
- No natural (non-padded) content at production scale tested
- brotli library version 1.2.0 behavior; production HTTP clients may differ
