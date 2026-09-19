# EXP-RUNTIME-35445595071 preregistration

## Experiment Identity

- **Experiment ID**: EXP-RUNTIME-35445595071
- **Lane**: runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Parent**: EXP-RUNTIME-35434773328 (SURVIVES_CURRENT_TEST, chunked TE on localhost)
- **Parent Handoff**: research/experiments/EXP-RUNTIME-35434773328/handoff.json

## Question

Does iterative decompression (brotli→gzip→identity, max_depth=5) survive multi-chunk brotli reassembly where compressed payloads span multiple HTTP chunks, preserving decompressed body-only discrimination at 0.5 and hash determinism?

## Background and Motivation

The parent experiment (EXP-RUNTIME-35434773328) established that iterative decompression preserves body-only discrimination at 0.5 through end-to-end chunked TE (origin→proxy→client) on localhost. However, three audit findings bound the claim ceiling:

- **V1**: CL-PASSTHROUGH origin was also chunked (contamination of regression control)
- **V2**: All compressed body_sizes (70-176 bytes) fit in a single chunk (chunk_size=1024), so multi-chunk brotli boundary splitting is untested
- **V3**: Origin verification is on fresh verify servers, not the measured origins

The parent's `do_not_assume` list explicitly states: "Multi-chunk reassembly works — all compressed body_sizes are 70-176 bytes (chunk_size=1024), chunk boundaries never split brotli payload."

This experiment directly tests V2 by reducing chunk_size from 1024 to 32 bytes, forcing all compressed payloads to span 3-6 chunks. If chunk boundaries corrupt brotli multi-byte symbols, decompression will fail and real CDN deployment is fundamentally blocked (production CDNs apply arbitrary chunking). If decompression succeeds, one critical blocker for C-MEAS-VALID product readiness is removed.

## Hypothesis

Iterative decompression will correctly reassemble and decompress brotli payloads that span multiple HTTP chunks, because:
1. HTTP chunked transfer-encoding is a framing layer above the application data
2. The HTTP client reassembles chunks into a contiguous byte stream before the decompression layer sees it
3. Broli decompression operates on the reassembled contiguous stream

Therefore, reducing chunk_size from 1024 to 32 bytes will not corrupt decompression or degrade discrimination.

## Falsifier

Iterative decompression fails under multi-chunk reassembly if ANY of:
1. Decompression errors > 0 on any multi-chunk response
2. Decompressed hash determinism fails (all_same != true for any state×condition cell)
3. Decompressed body-only discrimination drops below 0.3 for any cell

Any of these triggers FALSIFIED-IN-SETTING.

## Experimental Design

### Infrastructure

- **Mock OAuth2 Flask server** on localhost, serving brotli-compressed responses
- **chunk_size = 32 bytes** (down from 1024 in parent), forcing 3-6 chunks per compressed payload
- Origin serves `Transfer-Encoding: chunked` without `Content-Length` (use_chunked=True) for ALL cells, eliminating V1 contamination
- Auth-aware caching: URL+Accept-Encoding+Authorization cache key, Cache-Control: private, Vary: Authorization
- Iterative decompression: brotli.decompress with gzip fallback, max_depth=5

### Conditions

| Content Type | Size | Auth States | Chunk Config | Reps | Requests |
|---|---|---|---|---|---|
| JSON | 1KB | 4 | chunk_size=32 | 20 | 80 |
| HTML | 1KB | 4 | chunk_size=32 | 20 | 80 |
| XML | 1KB | 4 | chunk_size=32 | 20 | 80 |
| JSON | 1KB | 4 | chunk_size=1024 (B-SINGLE-CHUNK) | 20 | 80 |
| HTML | 1KB | 4 | chunk_size=1024 (B-SINGLE-CHUNK) | 20 | 80 |
| XML | 1KB | 4 | chunk_size=1024 (B-SINGLE-CHUNK) | 20 | 80 |

**Total**: 480 requests

### Auth States (4)

1. no_auth: 200, login_required body
2. valid_token: 200, alice_profile body, Set-Cookie session
3. expired_token: 401, auth_failed body, Cache-Control no-store
4. invalid_token: 401, auth_failed body (identical to expired), Cache-Control no-cache

### Baselines

- **B-SINGLE-CHUNK**: chunk_size=1024 (parent baseline, all payloads in one chunk)
- **B-RANDOM**: Random SHA-256 fingerprint on multi-chunk responses (null model)

### Metrics

1. **decompressed_body_only_discrimination**: Jaccard-based intra/inter ratio on SHA-256 of (status, decompressed_body) across auth states. Expected: 0.5 (structural ceiling from 3-way error collapse).
2. **decompressed_hash_determinism**: all_same=true if all reps of same state×condition produce identical decompressed hash.
3. **decompression_error_rate**: fraction of requests where iterative decompression fails. Expected: 0.
4. **multi_chunk_discrimination**: discrimination computed only on responses where compressed payload exceeded chunk_size (multi-chunk responses). Expected: 0.5.

## Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:
1. decompressed_body_only_discrimination >= 0.3 for ALL multi-chunk cells (expected: 0.5)
2. decompressed_hash_determinism all_same=true for ALL states across ALL conditions
3. B-RANDOM = 0.0 for ALL cells
4. 0 decompression errors across ALL requests
5. multi_chunk_discrimination >= 0.3 for ALL cells (expected: 0.5)

**FALSIFIED-IN-SETTING** if ANY of conditions (1)-(4) fails.

**MEASUREMENT_INVALID** if infrastructure prevents valid multi-chunk generation (e.g., all payloads still fit in one chunk despite chunk_size=32).

## Validity Threats

1. **Chunk-size enforcement**: If the mock server's chunked writer still buffers before sending, effective chunk_size may be larger than 32. Mitigation: verify chunk sizes via network capture or response header inspection.
2. **Brotli padding**: Brotli's LZ77 dictionary may pad small payloads above 32 bytes, but if total compressed size < 32, no splitting occurs. Mitigation: use incompressible padding to force compressed size > 32.
3. **Client reassembly**: urllib may buffer internally, making chunk boundaries invisible to decompression. This is expected behavior (chunking is a transport concern), but means we test reassembly+decompression as a unit, not brotli symbol splitting in isolation.
4. **Single content size**: Only 1KB tested; larger payloads (10KB, 100KB) may have different chunk-boundary interactions. Bounded claim ceiling to 1KB.

## Scope Boundaries

This experiment tests ONLY:
- Multi-chunk brotli reassembly on localhost with chunk_size=32
- Iterative decompression (max_depth=5) with brotli→gzip→identity fallback
- 1KB JSON/HTML/XML with synthetic padding
- 4 auth states with 3-way error collapse

This experiment does NOT test:
- Real CDN infrastructure (Cloudflare/Fastly/Akamai)
- Accept-Encoding negotiation (client sends no Accept-Encoding)
- Geographic latency or production-scale concurrency
- Binary content types or MB-scale payloads
- Multi-chunk gzip or identity encoding
- CL-PASSTHROUGH regression (V1 contamination, separate orthogonal experiment)

## Product Consequences

**If positive**: Multi-chunk brotli reassembly works. The V2 single-chunk degeneracy blocker is removed. C-MEAS-VALID advances toward real CDN readiness. Product team may proceed with CDN deployment testing.

**If negative**: Multi-chunk brotli reassembly fails. Chunked framing corrupts brotli compressed data when boundaries split multi-byte symbols. This is a fundamental blocker for real CDN deployment. Product team must implement chunk-boundary-aware decompression or avoid chunked TE for compressed responses. C-MEAS-VALID product readiness is blocked pending a fix.
