# EXP-RUNTIME-35456070671 preregistration

## Identity

- **Experiment ID**: EXP-RUNTIME-35456070671
- **Lane**: runtime
- **Claim IDs**: C-MEAS-VALID
- **Parent**: EXP-RUNTIME-35445595071 (multi-chunk brotli reassembly, framing transparency established, decompression correctness NOT established)
- **Parent Handoff SHA256**: 2ee49f556b2b348ae351faae298bffc21d1361dbd5164fcbbb4e1a1a5edbba8f

## Question

Can decompressed payload byte-equality to ground-truth uncompressed body be verified via direct correctness controls, establishing that iterative decompression actually produces correct output rather than silently falling back to compressed bytes that happen to preserve state-grouping discrimination?

## Background and Motivation

The parent experiment (EXP-RUNTIME-35445595071) established that chunked transfer-encoding is transparent to the iterative decompression pipeline: multi-chunk brotli payloads spanning 3-6 chunks at chunk_size=32 process without crashes or loss of state-grouping discrimination (all discrimination 0.5, B-RANDOM 0.0, 0 counted errors, 480 requests).

However, the parent audit identified two critical degeneracies that prevent this from establishing decompression **correctness**:

1. **V1_DEGENERATE_ERROR_CONTROL**: `decompress_body()` (lines 387-405) never raises an exception. It silently catches all brotli/gzip errors and returns the input unchanged. Error count is tautologically 0. The metric cannot detect silent fallback.

2. **V2_INSENSITIVE_DISCRIMINATION**: Decompressed discrimination (0.5) equals compressed discrimination (0.5). Both are determined by the 3-way error collapse (no_auth/expired/invalid share identical bodies). The discrimination metric cannot distinguish successful brotli decompression from silent fallback to compressed bytes that happen to preserve the same state-grouping structure.

**The gap**: We know chunking doesn't crash the pipeline, but we do NOT know if decompression actually produces correct output. Before advancing to real CDN testing (the product-readiness blocker for C-MEAS-VALID), correctness must be established. Otherwise the entire decompression-normalization line rests on an unverified assumption.

## Hypothesis

Iterative decompression (brotli->gzip->identity, max_depth=5) produces byte-identical output to the ground-truth uncompressed body for all 4 auth states across all content types and chunk configurations, because:

1. The mock server generates bodies via deterministic `generate_*_body(state, target_size)` functions
2. `brotli.compress` at fixed quality is a pure function (deterministic compression)
3. HTTP chunked TE reassembles into contiguous bytes before the decompression layer sees it
4. Iterative decompression correctly peels compression layers (brotli first, then gzip fallback)

Therefore: `SHA256(decompress_body(raw_body)) == SHA256(generate_*_body(state, target_size))` for every observation.

## Falsifier

Decompression correctness fails if ANY of:

1. **Byte mismatch**: Decompressed body hash != expected body hash for any observation (correctness control fails, indicating silent fallback or byte corruption)
2. **Silent fallback**: Decompressed body hash == raw body hash when Content-Encoding is brotli (decompression returned input unchanged)
3. **No decompression**: `raw_body == decompressed` for any brotli-compressed response (decompression did not alter bytes)

Any of these triggers **FALSIFIED-IN-SETTING**, meaning the decompression pipeline has a latent correctness bug that must be fixed before CDN testing.

## Experimental Design

### Architecture

Same as parent:
```
Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server
```

### Conditions

Three conditions (two compressed + one identity baseline):

| Condition | Origin Compression | chunk_size | Client Decompression | Purpose |
|---|---|---|---|---|
| MULTI-CHUNK | brotli quality 6 | 32 bytes | iterative | Test correctness under multi-chunk framing |
| SINGLE-CHUNK | brotli quality 6 | 1024 bytes | iterative | Parent baseline regression |
| IDENTITY | none (Content-Length) | N/A | none | Ground-truth reference |

### Content Types

Three content types at 1KB nominal size:
- JSON: `{"sub":"alice","name":"Alice",...}` padded to 1024 bytes
- HTML: User profile/error page padded to 1024 bytes
- XML: Response document padded to 1024 bytes

### Auth States

Four states (same as parent):
- `no_auth`: no Authorization header
- `valid_token`: HS256 JWT with future exp
- `expired_token`: HS256 JWT with past exp
- `invalid_token`: non-JWT string

### Sample Size

N=10 per state per condition (reduced from parent N=20 since correctness is binary pass/fail).

Total: 3 conditions x 3 content types x 4 states x 10 reps = 360 requests
Plus: connectivity tests, verification requests, overhead ~420 total.

### Seed

SEED=44 (same as parent for reproducibility).

## Measurements

### Primary Metric: Correctness Match Rate

For each observation `i` with auth state `s`:
```
expected_hash[i] = SHA256(generate_*_body(s, target_size))
decompressed_hash[i] = SHA256(decompress_body(raw_body, content_encoding))
correctness_match[i] = (decompressed_hash[i] == expected_hash[i])
```

Aggregate: `correctness_match_rate = sum(correctness_match) / N`

**Decision**: 100% correctness match rate required for all cells.

### Secondary Metric: Silent Fallback Detection

For each brotli-compressed observation:
```
silent_fallback[i] = (SHA256(decompressed) == SHA256(raw_body))
```

If any silent_fallback is True, decompression returned input unchanged.

### Tertiary Metrics

- **Decompression verification**: `raw_body != decompressed` for all brotli-compressed responses
- **Discrimination**: Intra-state match rate minus inter-state match rate (expected: 0.5 structural ceiling)
- **Determinism**: `all_same` per state across reps (expected: true)
- **B-RANDOM**: Random fingerprint discrimination (expected: 0.0)
- **Decompression errors**: Exception count + silent fallback count (expected: 0)
- **Latency**: Decompression time per observation

## Controls

### Positive Control

For each of 4 auth states, SHA256(decompressed) == SHA256(expected) for all observations. Structural ceiling: 100% correctness across all states and conditions.

### Null Control

B-RANDOM: Random SHA-256 fingerprint on the same response set. Passes if discrimination = 0.0.

### Regression Control

SINGLE-CHUNK condition reproduces parent: discrimination 0.5, determinism all_same=true, 0 errors.

### Identity Baseline

IDENTITY condition (no compression): hash matches expected for 100% of observations. Verifies server generates correct bodies and the expected hash computation is correct.

## Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:

1. Correctness match rate == 100% for ALL cells (correctness control pass)
2. Silent fallback count == 0 for ALL brotli-compressed observations
3. Decompressed body-only discrimination >= 0.3 for ALL cells (expected: 0.5)
4. Decompressed hash determinism all_same=true for ALL states across ALL conditions
5. B-RANDOM = 0.0 for ALL cells
6. 0 decompression errors (exceptions + silent fallbacks) across ALL requests
7. IDENTITY baseline hash matches expected for 100% of observations

**FALSIFIED-IN-SETTING** if ANY of conditions (1), (2), or (6) fails.

**MEASUREMENT_INVALID** if infrastructure prevents valid correctness measurement (e.g., generate_*_body() not available to correctness checker, or server fails to start).

## Product Consequence

### Positive Outcome

Decompression correctness is established: iterative decompression produces byte-identical output to ground-truth uncompressed body. This resolves the V1/V2 degeneracy and removes the decompression-correctness blocker for real CDN testing. C-MEAS-VALID advances to real CDN readiness.

### Negative Outcome

Decompression correctness fails: iterative decompression silently produces wrong output. This is a fundamental blocker for C-MEAS-VALID product readiness. The entire decompression-normalization line rests on an unverified assumption. Product team must diagnose and fix the decompression pipeline before any CDN testing.

## Validity Threats

1. **Server determinism**: If `generate_*_body()` or `brotli.compress()` produce non-deterministic output, expected hash may not match. Mitigated by fixed quality=6 and deterministic padding.
2. **Proxy byte corruption**: If the proxy corrupts bytes during re-chunking, decompressed output won't match expected. Mitigated by parent passing framing transparency test.
3. **Brotli library bug**: If brotli.decompress silently returns wrong bytes, correctness check catches it. This is the point of the experiment.
4. **Hash collision**: SHA-256 collision probability is negligible (2^-128).
5. **Localhost only**: Does not establish correctness on real CDN infrastructure. That is the next experiment if this passes.

## Scope Boundaries

This experiment tests:
- Decompression correctness on localhost mock infrastructure
- Brotli quality 6 only (not quality variation)
- chunk_size=32 (multi-chunk) and 1024 (single-chunk)
- JSON/HTML/XML at 1KB nominal size
- 4 auth states with 3-way error collapse

This experiment does NOT test:
- Real CDN infrastructure (Cloudflare/Fastly/Akamai)
- Brotli quality variation (4-8)
- Larger payloads (10KB, 100KB) under correctness controls
- gzip multi-chunk under correctness controls
- Streaming partial-frame forwarding
- Production OAuth/OIDC middleware
- Binary content types
