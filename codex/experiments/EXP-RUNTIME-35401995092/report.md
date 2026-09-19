# EXP-RUNTIME-35401995092 — Chunked Transfer-Encoding Decompression Test

**Status:** COMPLETE | **Outcome:** SUPPORTS | **Lane:** runtime
**Parent:** EXP-RUNTIME-35389142338 (auth-aware caching, Content-Length)

## Question

Does iterative Brotli decompression maintain discrimination when the proxy uses
`Transfer-Encoding: chunked` instead of `Content-Length`?

## Design

| Config | TE | Cache key | Purpose |
|---|---|---|---|
| CL-PASSTHROUGH | Content-Length | none | Parent baseline regression control |
| CHUNKED-PASSTHROUGH | chunked | none | Isolate TE framing effect |
| CHUNKED-CACHED | chunked | URL+AE+Auth | Primary test: chunked + auth-aware cache |

3 content types × 3 sizes × 4 auth states × 3 configs × 5 reps = **540 requests**.

## Key Results

| Metric | Value |
|---|---|
| Min decompressed discrimination | **0.5000** (all cells, all configs) |
| CHUNKED-CACHED min | **0.5000** |
| CL-PASSTHROUGH mean | **0.5000** |
| B-RANDOM (null) | **0.0000** |
| Decompression errors | **0** |
| Determinism across paths | **True** |

**All 6 controls pass.**

## Interpretation

Transfer-Encoding: chunked does not degrade decompression discrimination.
The auth-aware cache key (URL+AE+Auth) with chunked TE preserves the full
0.5 discrimination, identical to Content-Length forwarding.

This extends the parent's finding (auth-aware caching restores discrimination
with Content-Length) to the chunked TE case commonly used by real CDNs.

## Limitations

- Localhost mock server, not real CDN infrastructure
- No CDN-specific header manipulation (Via, X-Forwarded-For)
- Single Brotli quality level (6)
- No multi-layer encoding scenarios
