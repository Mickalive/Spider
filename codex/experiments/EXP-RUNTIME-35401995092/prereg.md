# EXP-RUNTIME-35401995092 — Preregistration

## Experiment Identity

- **Experiment ID**: EXP-RUNTIME-35401995092
- **Lane**: runtime
- **Claim IDs**: C-MEAS-VALID
- **Parent**: EXP-RUNTIME-35389142338 (auth-aware caching restores discrimination to 0.5 with Content-Length forwarding)
- **Date**: 2026-09-19

## Question

Does iterative decompression survive Transfer-Encoding: chunked through the localhost proxy with auth-aware cache configuration — closing the parent's explicit Content-Length-only scope gap before real CDN deployment?

## Background

The parent experiment (EXP-RUNTIME-35389142338) established that auth-aware caching (URL+Accept-Encoding+Authorization in cache key, Cache-Control: private, Vary: Authorization) restores decompressed body-only discrimination to 0.5 across all 9 content conditions (JSON/HTML/XML × 1KB/10KB/100KB), matching the PASSTHROUGH/RECOMPRESS baseline. However, the parent used Content-Length forwarding in all conditions and explicitly listed chunked TE as an unknown:

> "Does iterative decompression survive Transfer-Encoding: chunked through a real CDN proxy independently of Content-Length? (This experiment used Content-Length; chunked TE was not varied)"

Real CDNs commonly use chunked TE for dynamic content, compressed responses, and streaming. This experiment closes that scope gap on localhost before real CDN investment.

## Hypothesis

Transfer-Encoding: chunked is transparent to the iterative decompression pipeline because:

1. The proxy reassembles chunks into a coherent byte stream before the client receives it
2. The brotli/gzip decompressor operates on logical body bytes, not transport framing
3. The parent's 0.5 discrimination is a property of auth-aware cache semantics, not Content-Length framing

If chunked TE is transparent, discrimination should remain at 0.5. If chunked TE causes incomplete frame delivery (e.g., decompressor sees individual chunks as separate brotli streams, or chunk boundaries split multi-byte symbols), discrimination will drop below 0.3 or decompression errors will appear.

## Falsifier

- Decompressed body-only discrimination < 0.3 for any (auth_state, content_type × size) combination under chunked TE
- Decompression errors > 0 for any chunked TE condition
- Decompressed hash mismatch between chunked proxy and direct-server (determinism failure)
- Content-Length PASSTHROUGH discrimination drops below 0.5 (infrastructure regression)
- Chunked AUTH-AWARE CACHED discrimination < 0.3 for any cell (caching + chunked interaction)

## Design

### Configurations (3)

| ID | Transport | Cache Mode | Description |
|----|-----------|------------|-------------|
| CL-PASSTHROUGH | Content-Length | PASSTHROUGH | Parent baseline, regression control |
| CHUNKED-PASSTHROUGH | Chunked TE | PASSTHROUGH | Primary test: chunked in passthrough |
| CHUNKED-CACHED | Chunked TE | AUTH-AWARE CACHED | Primary test: chunked + caching interaction |

### Content Conditions (9)

3 content types × 3 sizes:
- JSON × {1KB, 10KB, 100KB}
- HTML × {1KB, 10KB, 100KB}
- XML × {1KB, 10KB, 100KB}

### Auth States (4)

- no_auth
- valid_token
- expired_token
- invalid_token

### Repetitions

N=5 reps per (auth_state, content_condition, config)

### Total Requests

4 × 9 × 3 × 5 = 540

### Seed

44 (same as parent for comparability)

## Baselines

| ID | Expected | Purpose |
|----|----------|---------|
| B-PARENT-CONTENT-LENGTH-0.5 | 0.5 | Regression: proxy infrastructure unchanged |
| B-PARENT-NAIVE-CACHED-0.0 | 0.0 | Regression: cache-key semantics unchanged |
| B-RANDOM | 0.0 | Null: spurious structure detection |
| B-CHUNKED-CACHED-0.5 | 0.5 | Primary test: chunked + auth-aware caching |

## Controls

### Positive Control

C_CONTENT_LENGTH_REGRESSION: Content-Length PASSTHROUGH discrimination = 0.5 for all cells. Confirms proxy infrastructure is unchanged from parent.

### Null Control

C_NULL_CONTROL: B-RANDOM ≈ 0.0 for all conditions. Random fingerprints cannot produce discriminating structure.

### Determinism Controls

- C_DECOMPRESSED_DETERMINISM: Within-state decompressed hash all_same=true for all states across all configs
- C_DETERMINISM_ACROSS_FRAMING: Decompressed hash through chunked proxy matches direct-server hash for same condition

## Metrics

### Primary

- `decompressed_body_only_discrimination`: Fraction of within-state decompressed hash pairs that are identical, averaged across auth states. Range [0, 1]. Threshold ≥ 0.3.

### Secondary

- `compressed_body_only_discrimination`: Same metric on compressed (pre-decompression) body hash
- `status_only_discrimination`: Same metric on HTTP status code only
- `decompression_errors`: Count of brotli/gzip/identity decompression failures
- `proxy_overhead_ms`: Time added by proxy (proxy timestamp − origin timestamp)
- `decompression_latency_ms`: Time for client-side iterative decompression

## Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:
1. Decompressed body-only discrimination ≥ 0.3 for ALL (auth_state, config) combinations under chunked TE
2. Decompressed hash through chunked proxy matches direct-server hash (determinism across framing)
3. B-RANDOM = 0.0 for all conditions
4. Content-Length PASSTHROUGH discrimination = 0.5 for all cells
5. 0 decompression errors on chunked TE conditions
6. Chunked AUTH-AWARE CACHED discrimination ≥ 0.3 for all cells

**FALSIFIED-IN-SETTING** if any:
- Chunked TE discrimination < 0.3 for any cell
- Decompressed hash mismatch across transport framing
- Decompression errors > 0 on chunked responses
- Content-Length PASSTHROUGH drops below 0.5

**MEASUREMENT_INVALID** if:
- Proxy fails to start
- Origin unreachable through proxy
- Chunked TE not correctly applied (origin still sends Content-Length)

## Measurement Validity

- Same mock origin server as parent (localhost Flask/stdlib, brotli quality 6)
- Same Python reverse proxy as parent on separate localhost port
- Origin configured to serve chunked responses (no Content-Length header) for chunked conditions
- Accept-Encoding: 'br, gzip, identity' in all conditions
- Iterative decompression max_depth=5 (same as parent)
- Seed=44 for request ordering

## Product Consequences

### Positive

Iterative decompression survives chunked TE. This closes the parent's explicit scope gap and strengthens the case for real CDN readiness. Remaining blocker: real CDN infrastructure only (edge-specific concerns).

### Negative

Chunked TE breaks iterative decompression. This identifies a specific transport-framing constraint requiring resolution before CDN deployment. Root causes may include: decompressor cannot handle chunked framing, proxy does not reassemble chunks correctly, or chunk boundaries split brotli symbols.

## Expected Information Gain

HIGH. This is the minimum-cost experiment that closes the parent's explicit Content-Length-only scope gap. Either outcome (pass or fail) is strictly more informative than repeating the parent or jumping to real CDN with an untested transport mode. Cost: < 540 requests, < 3 minutes execution.
