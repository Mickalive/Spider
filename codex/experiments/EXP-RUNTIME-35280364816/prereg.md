# Preregistration: EXP-RUNTIME-35280364816

## Experiment Identity

- **Experiment ID**: EXP-RUNTIME-35280364816
- **Lane**: runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Parent**: EXP-RUNTIME-35262264593 (Encoding-Layer Non-Determinism)
- **Parent Handoff SHA256**: 73b0e1ebae68724b41cb53d392eac48d2e3339121fc14a6e3c0e5a708b60747f

## Question

Does iterative decompression (decompress repeatedly until failure or a maximum depth of 3-5) restore decompressed body-only discrimination to >= 0.3 and decompressed hash determinism (all_same=true) under double-brotli and triple-brotli encoding on localhost — and does it maintain discrimination for the 4 single-layer encoding scenarios that already pass?

## Hypothesis

Iterative decompression restores decompression-normalization because the double-brotli failure mode is a client implementation limitation (single-pass decompression stops after removing the outer layer), not a fundamental property of the encoding. Double-encoded responses contain brotli-compressed data wrapped in another brotli layer; decompressing twice recovers the true decompressed body. Triple-encoded responses require three passes. The 4 single-layer scenarios already produce identical decompressed hashes under single-pass decompression, so iterative decompression should maintain their discrimination.

## Falsifier

Decompressed body-only discrimination < 0.3 for any content type at any size under any encoding scenario, OR decompressed hash variation > 1 unique per state for any condition, OR iterative decompression causes crashes/hangs on garbled headers, OR iterative decompression changes hashes for single-layer scenarios (regression), OR triple-brotli is not decompressible by depth 5.

## Design

### Architecture

```
Client (iterative decompression) -> CDN Encoding Proxy (random encoding scenario) -> Mock OAuth2 Server (brotli quality 6)
```

### Modification from Parent

The only code change is in `decompress_body()`: replace single-pass brotli/gzip/identity decompression with iterative decompression that loops until failure or max_depth=5. At each iteration:
1. Try brotli decompress
2. If brotli fails, try gzip decompress
3. If gzip fails, return current data (identity)
4. If brotli or gzip succeeded, increment depth and repeat from step 1

### Encoding Scenarios (6 total, up from 5)

1. **correct_br**: Standard brotli, passes through as-is
2. **missing_ce**: Removes Content-Encoding header (identity transfer)
3. **incorrect_gzip**: Serves brotli bytes with Content-Encoding: gzip
4. **double_br**: Wraps brotli bytes in another brotli layer (depth=2)
5. **triple_br**: Wraps brotli bytes in three brotli layers (depth=3) — NEW
6. **garbled_ce**: Sets Content-Encoding to malformed value

### Content Matrix

- Content types: JSON, HTML, XML
- Payload sizes: 1KB, 10KB, 100KB
- Auth states: no_auth, valid_token, expired_token, invalid_token (4 states, 3-way error collapse)
- Reps per state per condition: 20
- Total: 6 scenarios x 3 types x 3 sizes x 4 states x 20 reps = 4320 requests

### Controls

- **B-RANDOM**: SHA256 on random 32-byte fingerprints. Expected ~0.0.
- **B-SINGLE-PASS-0.2911**: Parent single-pass discrimination (regression floor).
- **B-NO-DOUBLE-BR-0.4486**: Parent discrimination excluding double_br (target floor).
- **C_ENCODING_VARIATION_EXISTS**: >= 4 distinct encoding scenarios per condition.
- **C_NULL_CONTROL**: B-RANDOM ~ 0.0 all conditions.
- **C_DECOMPRESSION_DETERMINISM**: Within-state decompressed hash variation = 0 for all states.
- **C_GRACEFUL_DEGRADATION**: No crashes/hangs from garbled headers.
- **C_TRIPLE_BR_DECOMPRESSIBLE**: Triple-encoded responses decompress successfully (depth <= 5).

### Decision Rule

SURVIVES_CURRENT_TEST if ALL of:
1. decompressed body-only discrimination >= 0.3 for JSON at all sizes
2. decompressed body-only discrimination >= 0.3 for HTML at all sizes
3. decompressed body-only discrimination >= 0.3 for XML at all sizes
4. decompressed hash variation all_same=true for all content types x sizes x states
5. B-RANDOM = 0.0 for all conditions
6. C_ENCODING_VARIATION_EXISTS passes

FALSIFIED-IN-SETTING if any content type has discrimination < 0.3 at any size, OR decompressed hashes differ by encoding scenario, OR iterative decompression introduces regressions on single-layer scenarios.

MEASUREMENT_INVALID if infrastructure failure prevents valid measurements.

## Stability

- Seed: 44 (request ordering)
- Scenario RNG seed: SEED + 7919 (independent from request ordering)
- Mock server brotli quality: 6 (deterministic)
- Max decompression depth: 5
- Jitter: 50-150ms uniform between requests

## Consequences

**Positive**: Claim ceiling advances to 'multi-layer encoding survival including double and triple encoding'. Unlocks CDN deployment with nested encoding.

**Negative**: Failure mode is not a client limitation. Product must add layer-count detection or reject multi-layer responses. CDN deployment blocked until mitigation.
