# EXP-RUNTIME-35513777099 — Multi-Layer Encoding Decompression Correctness

## Preregistration

**Experiment ID:** EXP-RUNTIME-35513777099
**Lane:** runtime
**Claim IDs:** C-MEAS-VALID
**Date:** 2026-09-20
**Parent:** EXP-RUNTIME-35495699298 (single-layer correctness on high-entropy payloads)

## Question

Does iterative decompression correctness hold for multi-layer compressed encodings (gzip->brotli, brotli->gzip) where max_depth>1?

## Hypothesis

Iterative decompression (brotli->gzip->identity, max_depth=5) produces byte-identical output to ground-truth high-entropy `generate_*_body(state, target_size)` for all 4 auth states, 3 content types, 2 payload sizes, and 2 multi-layer encoding configurations.

## Architecture

```
Client (iterative decompression, max_depth=5)
  -> Python Reverse Proxy (chunked forwarding)
    -> Mock OAuth2 Server (multi-layer compressed responses)
```

The mock server applies two layers of compression:
- **GZIP-THEN-BROTLI:** `body -> gzip.compress(level=1) -> brotli.compress(quality=4) -> chunked transfer`
- **BROTLI-THEN-GZIP:** `body -> brotli.compress(quality=4) -> gzip.compress(level=1) -> chunked transfer`

The client's iterative decompression must correctly unwrap both layers.

## Conditions

### Main Experimental Cells (2 sizes x 3 types x 2 multi-layer encodings x 4 states x 5 reps = 240 observations)

| Size | Content Types | Encodings | States | Reps |
|------|---------------|-----------|--------|------|
| 10KB | JSON, HTML, Binary | GZIP-THEN-BROTLI, BROTLI-THEN-GZIP | no_auth, valid_token, expired_token, invalid_token | 5 |

| Size | Content Types | Encodings | States | Reps |
|------|---------------|-----------|--------|------|
| 100KB | JSON, HTML, Binary | GZIP-THEN-BROTLI, BROTLI-THEN-GZIP | no_auth, valid_token, expired_token, invalid_token | 5 |

### Regression Controls (1KB)

- **B-GZIP-SINGLE-LAYER-REGRESSION:** Single-layer gzip at 10KB high-entropy (parent established 240/240)
- **B-BROTLI-SINGLE-LAYER-REGRESSION:** Single-layer brotli at 10KB high-entropy (parent established 240/240)

### Identity Baselines (correctness oracle)

- **B-IDENTITY-HE-10KB:** No compression at 10KB high-entropy
- **B-IDENTITY-HE-100KB:** No compression at 100KB high-entropy

## Falsifier

Any `SHA256(decompressed) != SHA256(generate_*_body(state, target_size))` across all observations for any cell, OR any silent fallback (`SHA256(decompressed) == SHA256(raw_compressed)`) for any compressed response, OR any cell where `compressed_size_bytes mean < 2000`.

## Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:

- **C1:** `correctness_match_rate == 1.0` for ALL multi-layer cells
- **C2:** `silent_fallback_count == 0` for ALL multi-layer cells
- **C3:** Regression controls pass 100%
- **C4:** Null control passes (within-state determinism: `all_same=true`)
- **C5:** Compressed target range passes (at least 2/3 content types achieve mean compressed_size >= 2000 at 10KB and >= 5000 at 100KB)

**FALSIFIED** if any correctness failure OR any silent fallback in any multi-layer cell.

**MEASUREMENT_INVALID** if infrastructure prevents data collection, if correctness oracle baseline fails, or if B-COMPRESSED-TARGET-RANGE fails.

## Controls

### Positive Control
Single-layer correctness must pass 100% (regression from parent chain).

### Null Control
Within-state decompressed hash must be deterministic (`all_same=true` for all 4 auth states across all multi-layer cells).

### Baselines
- B-GZIP-SINGLE-LAYER-REGRESSION
- B-BROTLI-SINGLE-LAYER-REGRESSION
- B-IDENTITY-HE-10KB
- B-IDENTITY-HE-100KB
- B-COMPRESSED-TARGET-RANGE
- B-RANDOM (within-state hash determinism)

## Measurement Validity

1. Multi-layer encodings exercise max_depth>1: the iterative decompression pipeline must correctly unwrap two layers of compression
2. High-entropy payload generators reused from parent EXP-RUNTIME-35495699298 (validated at Shannon entropy >= 3.5 bits/byte)
3. Correctness oracle validated via B-IDENTITY-HE baselines
4. Compressed size validation ensures payloads are not degenerate
5. Deterministic server with seeded RNG (seed=44)
6. Silent fallback detection: SHA256(decompressed) == SHA256(raw_compressed) classified as failure
7. chunk_size=32 for multi-chunk framing (60-3000+ chunks)
8. Request jitter 50-150ms uniform
9. Python 3.12 stdlib gzip + brotli 1.2.0

## Product Consequences

### Positive
Multi-layer encoding correctness validated. Claim ceiling expands from "single-layer only" to "multi-layer". V2_UNKNOWN limitation resolved. C-MEAS-VALID advances toward Product Core.

### Negative
Multi-layer encodings fail correctness. Decompression pipeline has a stacked-encoding failure mode. Product cannot handle real-world CDN scenarios where multiple Content-Encoding layers are applied. Diagnosis of specific failure mode required.

## Estimated Cost

~160 HTTP requests to localhost mock server, <10 minutes execution, no external infrastructure.

## Expected Information Gain

High: directly tests V2_UNKNOWN from parent carry_forward. Parent established 720/720 single-layer correctness (max_depth=1) but max_depth>1 was never exercised. Either outcome is highly decision-relevant.
