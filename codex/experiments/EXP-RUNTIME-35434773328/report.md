# EXP-RUNTIME-35434773328 — Upstream Chunked TE Decompression Test

## Executive Summary

**Outcome: SUPPORTS** — All 7 frozen decision conditions pass. Iterative decompression (brotli->gzip->identity, max_depth=5) survives Transfer-Encoding: chunked on the upstream origin->proxy leg with origin actually serving chunked. This closes the parent's explicit upstream scope gap.

## 1. Context

The parent (EXP-RUNTIME-35401995092) established that iterative decompression preserves decompressed body-only discrimination at 0.5 through chunked TE on the proxy->client leg (downstream). However, the origin was always started with `use_chunked=False`, so the upstream origin->proxy chunked reassembly path was never tested. The parent's audit identified this as a measurement validity gap (V1, severity medium).

This experiment applies three fixes from the parent audit:

- **V1**: Origin server `use_chunked=True` for all configs — origin serves `Transfer-Encoding: chunked` (no `Content-Length`)
- **V2**: Cache HIT path for chunked configs sends ONLY `Transfer-Encoding: chunked` (no `Content-Length`), fixing the HTTP/1.1 double-header violation
- **V3**: `PARENT_REF_HASHES` dead code removed — determinism ground truth established by live recomputation via fresh mock_direct servers

## 2. Results

### 2.1 Primary Metrics

| Config | Decompressed Discrimination (mean) | Compressed Discrimination (mean) |
|--------|-------------------------------------|----------------------------------|
| CL-PASSTHROUGH | 0.5000 | 0.5000 |
| CHUNKED-PASSTHROUGH | 0.5000 | 0.5000 |
| CHUNKED-CACHED | 0.5000 | 0.5000 |

All 27 cells (3 content types x 3 sizes x 3 configs) achieve decompressed body-only discrimination = 0.5. No cell falls below the 0.3 threshold.

### 2.2 Controls

| Control | Status | Observed |
|---------|--------|----------|
| C_NULL_CONTROL (B-RANDOM ~ 0.0) | PASS | 27x 0.0 |
| C_CONTENT_LENGTH_REGRESSION (= 0.5) | PASS | 9x 0.5 |
| C_CHUNKED_CACHED_PRIMARY (>= 0.3) | PASS | 9x 0.5 |
| C_DECOMPRESSED_DETERMINISM (all_same) | PASS | 4 states all true |
| C_DETERMINISM_ACROSS_PATHS (hash match) | PASS | 72/72 match, 0 mismatches |
| C_NO_ERROR_INFLATION (0 errors) | PASS | 0 decompression errors |
| C_ORIGIN_VERIFICATION (origin serves chunked) | PASS | Origin serves TE:chunked, no Content-Length |

### 2.3 Origin Verification (V1 Fix Confirmation)

The `C_ORIGIN_VERIFICATION` control starts fresh mock servers with `use_chunked=True` and verifies that the origin response headers contain `Transfer-Encoding: chunked` and do NOT contain `Content-Length`. This confirms that the V1 fix is correctly applied and the upstream origin->proxy chunked reassembly path is genuinely exercised.

### 2.4 Determinism

Within-state decompressed hashes are all identical (`all_same=true`) for all 4 auth states across all 27 cells, confirming decompression is deterministic and not corrupted by chunk boundaries splitting brotli multi-byte symbols.

Cross-path determinism holds: decompressed hash through chunked proxy matches direct-server hash for 72/72 conditions (9 content-size combinations x 4 auth states x 2 chunked configs). Zero mismatches.

### 2.5 Error Analysis

Zero decompression errors across all 540+ requests. No brotli/gzip decompression failures on chunked streams, falsifying the hypothesis that chunk boundaries split multi-byte symbols.

## 3. Interpretation

### 3.1 Core Finding

Chunked TE on the upstream origin->proxy leg is transparent to the proxy's reassembly pipeline. The proxy correctly reassembles the chunked stream from the origin into a coherent byte stream before forwarding/decompressing. This is consistent with the parent's downstream-only result (0.5 discrimination, 0 errors) and extends coverage to the full end-to-end path (origin->proxy->client).

### 3.2 Fixes Validated

- **V1 (origin chunked)**: Origin now serves `Transfer-Encoding: chunked` without `Content-Length` for all chunked conditions. Verified by `C_ORIGIN_VERIFICATION`. The upstream reassembly path is genuinely exercised.
- **V2 (double-header)**: Cache HIT path now sends only `Transfer-Encoding: chunked` for chunked configs, eliminating the HTTP/1.1 violation. No discrimination or error impact observed.
- **V3 (dead code)**: `PARENT_REF_HASHES` removed. Determinism ground truth established by live recomputation via fresh mock_direct servers (72/72 match).

### 3.3 Regression

Content-Length PASSTHROUGH mode reproduces the parent baseline at 0.5 for all 9 CL cells, confirming proxy infrastructure is unchanged and any chunked effect is attributable to framing, not proxy drift.

### 3.4 Claim Ceiling

The claim ceiling expands from the parent's "proxy->client chunked downstream only" to include "end-to-end chunked TE (origin->proxy->client) on localhost mock infrastructure." Specifically:

- **Established**: Iterative decompression survives end-to-end chunked TE (origin->proxy->client) in both PASSTHROUGH and AUTH-AWARE CACHED modes on localhost mock infrastructure
- **Remaining blockers for C-MEAS-VALID**: Real CDN infrastructure (Cloudflare/Fastly/Akamai), Accept-Encoding negotiation, quality variation, geographic latency, multi-layer brotli, binary content, production-scale concurrency

### 3.5 Limitations

1. **Mock-only**: localhost Python reverse proxy does not replicate real CDN behavior
2. **Deterministic brotli**: quality 6 deterministic compression means 0.5 discrimination is a mock ceiling, not a production ceiling
3. **3-way error collapse**: no_auth/expired/invalid share identical bodies, limiting discrimination expressiveness
4. **N=5 per cell**: sufficient for deterministic system but no uncertainty quantification for stochastic environments
5. **No real CDN**: chunked TE framing from real CDN edge may differ from localhost mock

## 4. Product Consequences

### Positive
Iterative decompression survives end-to-end chunked TE (origin->proxy->client) in both passthrough and cached modes. This closes the parent's explicit upstream scope gap and completes the chunked TE story on localhost. Product team can proceed with chunked TE as a supported transport mode on localhost mock infrastructure. The remaining blocker for C-MEAS-VALID shifts to real CDN infrastructure only.

### Negative
None — all decision conditions pass.

## 5. Claim Updates

If SURVIVES_CURRENT_TEST (as observed):
- C-MEAS-VALID: advance to EXPERIMENTAL with expanded claim ceiling to include end-to-end chunked TE (origin->proxy->client) on localhost mock infrastructure

## 6. Unresolved

1. Does iterative decompression survive real CDN infrastructure (Cloudflare/Fastly/Akamai) with auth-aware cache configuration and chunked TE?
2. Does iterative decompression survive double/triple-brotli multi-layer encoding through a chunked proxy (max_depth=5 limit)?
3. What is production-scale latency/CPU at N>1000 with MB-scale natural content and concurrent clients through real or realistic chunked proxy?
4. Does iterative decompression work for binary content types or genuinely incorrect Content-Encoding on incompressible data?
5. How does proxy behavior interact with CDN-specific header manipulation (X-Cache, Via, X-Forwarded-For) and Accept-Encoding negotiation across multiple CDN nodes?
6. What is the maximum practical decompression depth for real-world multi-layer encoding scenarios?
