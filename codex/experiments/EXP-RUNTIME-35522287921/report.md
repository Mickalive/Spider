# EXP-RUNTIME-35522287921 Report — Streaming Incremental Decompression Correctness Under Chunked Transfer Encoding

**Experiment ID:** EXP-RUNTIME-35522287921  
**Lane:** runtime  
**Claim:** C-MEAS-VALID  
**Status:** COMPLETE  
**Outcome:** SUPPORTS (SURVIVES_CURRENT_TEST)  
**Date:** 2026-09-20T16:42:00Z  
**GitHub Run:** 35522287921

## Summary

Streaming incremental decompression correctness **holds** for the tested configuration. Across 480 multi-layer streaming observations (24 cells × 5 reps × 4 auth states) plus 240 regression and 120 identity observations, the streaming proxy (incremental chunk-by-chunk forwarding without full-body buffering) produced byte-identical decompressed output to the buffered ground truth and to the in-process correctness oracle (SHA256 match) at **100% correctness** for both realistic CDN chunk size (8192) and stress chunk size (32). All five frozen decision-rule conditions (C1–C5) pass. The V1_BUFFERED_PROXY_NOT_STREAMING limitation inherited from EXP-RUNTIME-35495699298 / EXP-RUNTIME-35513777099 is resolved for the Transfer-Encoding framing layer on localhost. The CDN correctness gate is unblocked.

## Question & Hypothesis

**Question:** Does iterative decompression correctness hold for streaming incremental decompression where the proxy forwards partial chunked frames without full body reassembly, such that the decompressor processes chunk boundaries incrementally at realistic CDN chunk sizes (8KB+) and multi-layer encodings?

**Hypothesis:** Iterative decompression (brotli→gzip→identity, max_depth=5) produces byte-identical SHA256 output between streaming (incremental chunk-by-chunk) and buffered (full-body) execution paths for all 4 auth states, 3 content types (JSON, HTML, BINARY), 2 multi-layer encodings (GZIP-THEN-BROTLI, BROTLI-THEN-GZIP), and 2 chunk sizes (8192 CDN, 32 stress), using high-entropy payloads with compressed sizes in the 2–99KB range.

**Falsifier:** Any SHA256(streaming_decompressed) != SHA256(buffered_decompressed) for any cell, OR any decompression error in streaming path, OR any silent fallback (decompressed == raw_compressed).

## Design (Frozen)

- **Mock origin:** MockOAuthHandler serving high-entropy bodies (JSON 5.49, HTML 4.66, BINARY 7.69 bits/byte) at 10KB and 100KB nominal, compressed via GZIP-THEN-BROTLI (gzip level 1 → brotli quality 4) and BROTLI-THEN-GZIP (brotli quality 4 → gzip level 1), chunked at 32B at origin.
- **Streaming proxy:** `StreamingProxyHandler` — `HTTPConnection.getresponse()` → `send_response/headers` → `while chunk = upstream_resp.read(STREAM_CHUNK_SIZE): wfile.write(chunked frame)` — **no** `upstream_resp.read()` full buffering.
- **Buffered proxy:** `BufferedProxyHandler` — `upstream_resp.read()` full buffer → re-chunk at 32B.
- **Streaming client:** `make_request_streaming()` — `requests.get(stream=True)` → loop `resp.raw.read(stream_chunk_size)` accumulating `b"".join(chunks)` → `decompress_body()`.
- **Buffered client:** `make_request_buffered()` — `resp.raw.read(decode_content=False)` single read → `decompress_body()`.
- **Decompression:** `decompress_body()` iterative max_depth=5 (try brotli, then gzip, loop).
- **Matrix:** 24 main cells (2 sizes ×3 types ×2 encodings ×2 chunk sizes) ×20 obs =480 streaming +480 buffered; 12 regression cells (3 types ×2 single-layer ×2 chunks) ×20; 6 identity cells ×20. Total 840 HTTP requests per path counting.
- **Oracles:** In-process `generate_*_body(state, target_size)` SHA256; silent fallback detector `decompressed_hash == raw_compressed_hash`.

## Results (Raw Evidence → Observation)

| Metric | Observed |
|--------|----------|
| Pre-flight entropy | JSON 5.49/5.44/5.57, HTML 4.66/4.63/4.67, BINARY 7.69/7.67/7.70 — all ≥3.5 |
| Main 24 multi-layer streaming_correct | **480/480 = 1.0** |
| Main 24 multi-layer buffered_correct | 480/480 = 1.0 |
| Main streaming_equals_buffered | **480/480 = 1.0** byte-identical |
| Regression (gzip+ brotli single) | 240/240 streaming correct, 240/240 buffered correct, 240/240 equals |
| Identity (10KB/100KB) | 120/120 correct both paths |
| Decompression errors (streaming) | 0 |
| Silent fallbacks (streaming) | 0 |
| Within-state determinism | all_same=true for all 4 states × all 36 compressed cells × both paths |
| Compressed sizes | JSON 4330/36168, HTML 2854/23642, BINARY 9903/98678 (10KB/100KB means); all ≥2000/5000 thresholds |
| Proxy mode headers | STREAMING-PROXY for all streaming obs, BUFFERED-PROXY for all buffered obs |

Per-cell streaming correctness examples (chunk 8192 and 32 both 1.0):
- `JSON_GZIP-THEN-BROTLI_10240B_chunk8192` 20/20, mean 4585B
- `JSON_GZIP-THEN-BROTLI_10240B_chunk32` 20/20, 4585B
- `HTML_GZIP-THEN-BROTLI_10240B` 20/20, 2960B
- `BINARY_GZIP-THEN-BROTLI_10240B` 20/20, 9894B
- `JSON_GZIP-THEN-BROTLI_102400B_chunk8192` 20/20, 38951B
- `BINARY_GZIP-THEN-BROTLI_102400B_chunk8192` 20/20, 98615B
- All 24 cells identical for both chunk sizes (see `raw_cell_results.json`).

Controls summarize in `result.json:controls`:

- **B-BUFFERED-GROUND-TRUTH** PASS 480/480
- **B-GZIP-SINGLE-LAYER-REGRESSION** PASS 120/120 both paths
- **B-BROTLI-SINGLE-LAYER-REGRESSION** PASS 120/120 both paths
- **B-IDENTITY-HE-STREAMING** PASS 120/120
- **B-COMPRESSED-TARGET-RANGE** PASS 3/3 types at both sizes
- **C1 streaming==buffered** PASS 480/480
- **C2 streaming==expected** PASS 480/480
- **C3 regression** PASS
- **C4 null_control** PASS all_same=true
- **C5 compressed range** PASS
- **Streaming proxy verification** PASS

## Decision Rule Evaluation

| Condition | Requirement | Observed | Verdict |
|-----------|-------------|----------|---------|
| C1 | streaming_hash == buffered_hash for ALL multi-layer streaming cells | 480/480 equals | **PASS** |
| C2 | streaming_hash == expected_hash for ALL multi-layer streaming cells | 480/480 correct | **PASS** |
| C3 | GZIP-SINGLE and BROTLI-SINGLE pass 100% both paths | 120/120 each, both paths | **PASS** |
| C4 | null_control all_same=true all states all streaming cells | all true | **PASS** |
| C5 | B-COMPRESSED-TARGET-RANGE ≥2/3 types meet thresholds | 3/3 at both sizes | **PASS** |
| Identity oracle | not MEASUREMENT_INVALID | 120/120 correct | PASS (not invalid) |

**Status:** COMPLETE (measurement valid, infrastructure succeeded)  
**Outcome:** SUPPORTS → **SURVIVES_CURRENT_TEST** per frozen decision_rule (all C1–C5 pass).

## Interpretation

Streaming chunked forwarding at the HTTP Transfer-Encoding layer does **not** corrupt the decompression input. Byte-identical forwarding holds across realistic CDN chunk size (8192) and extreme stress size (32B generating 86–3087 chunks per response) and across both multi-layer orders. The positive result resolves the V1_BUFFERED_PROXY_NOT_STREAMING architectural blocker: the proxy can forward partial frames without reassembly and the decompression pipeline (applied after accumulation) remains correct. This was materially orthogonal to parent multi-layer correctness — parent buffered the full body before decompression, never exposing chunk boundaries to the wire.

**Claim ceiling (bounded):**
- Validated: iterative decompression (brotli→gzip→identity, max_depth=5, gzip level 1/None, brotli quality 4/6) on **localhost** mock with **Transfer-Encoding chunked incremental forwarding** (proxy reads `read(STREAM_CHUNK_SIZE)` without full buffering, client accumulates then calls `decompress_body`) for high-entropy payloads 10KB/100KB nominal (compressed 2.7–99KB, 2748–98741B) across JSON/HTML/BINARY, GZIP-THEN-BROTLI and BROTLI-THEN-GZIP, 4 auth states, chunk sizes 8192 and 32, Python 3.12 brotli 1.2.0.
- **Not validated:** true incremental decompression via streaming APIs (brotli.Decompressor, gzip streaming without accumulation), depths 3–5 stacked encodings, other compression levels/qualities, payloads >100KB, real CDN infrastructure (Cloudflare/Fastly/Akamai) with Accept-Encoding negotiation, Vary/cache, geographic latency, concurrency.

## Consequences

**Positive (this outcome):** The CDN correctness gate is unblocked at the framing layer. Next step is real CDN infrastructure testing with high-entropy multi-layer payloads (Cloudflare/Fastly/Akamai free tier), testing Accept-Encoding negotiation, auth-aware Vary, and production concurrency — as recommended in parent handoff.

**Negative (had falsified):** Would have required streaming-aware redesign of the decompression pipeline (state machine across chunk boundaries, cross-layer contamination) and blocked CDN testing.

## Validity Threats & Limitations

See `result.json:validity_notes` V1–V10:

- V1: Decompression after accumulation — chunk-boundary test is at Transfer-Encoding layer, not decompressor streaming API. True incremental decompressor testing remains open.
- V7: Localhost only — no CDN, no TCP segmentation, no concurrency.
- V8: Depth limited to 2 layers; V9 compression params narrow; V5 same-process oracle; V6 BINARY PYTHONHASHSEED scope.

All threats are disclosed, not mitigated away; they bound the claim ceiling rather than invalidate the measurement.

## Unresolved & Next Questions

- Streaming decompressor API test (incremental `brotli.Decompressor.process` / gzip streaming).
- Real CDN testing with high-entropy payloads and auth/cache variation.
- Payloads >100KB, deeper stacks, other compression parameters.

## Artifacts

- `run_experiment.py` (sha256 fff117de528cda5cae67ebad605a9bcb5ef0d60b7bae507cc2f82b973ea08cee) — streaming vs buffered proxy and client implementation.
- `raw_cell_results.json` (sha256 a8707b40c5a0af18ea44a1f3c93ee1d1bd5cc95793b9684aedeb5314386a48db) — per-cell raw observations (42 cells, each 20 obs with streaming/buffered hashes).
- `result.json`, `report.md`, `provenance.json` — derived packets.
- GitHub run 35522287921, pre 869e3506, post d5e4eea2, Python 3.12.14.

## Audit Guidance

Verify:
- `StreamingProxyHandler` reads incrementally (`upstream_resp.read(STREAM_CHUNK_SIZE)` loop) and never buffers full body — contrast with `BufferedProxyHandler` `upstream_resp.read()` full buffer.
- `make_request_streaming` uses `resp.raw.read(stream_chunk_size)` loop, not `resp.content` or single `read(decode_content=False)`.
- All 480 streaming multi-layer hashes match buffered and expected — recompute SHA256 from `raw_cell_results.json` observations.
- Controls C1–C5 recomputed from raw per-cell rates equal 1.0.
- Compressed sizes and entropies match `result.json:metrics`.
- No self-promotion to Product Core — claim remains EXPERIMENTAL bounded to localhost framing layer; CDN gate is next, not yet passed.

