# EXP-RUNTIME-35538865067 — Real-CDN Iterative Decompression Correctness (EXECUTE report)

- `experiment_id`: EXP-RUNTIME-35538865067 · `lane`: runtime · `status`: COMPLETE · `outcome`: **FALSIFIES**
- Frozen inputs: `request.json` (b823b814…), `spec.json` (b78e058d…), `prereg.md` (4aadb45e…), `freeze.json` (380fabd9…).
- Claim: C-MEAS-VALID. Parent: EXP-RUNTIME-35530588298 (localhost decompressor-API streaming, 840/840, audit PASS).

This report interprets `result.json`. It does not contradict it. Raw evidence lives in
`raw_cell_results.jsonl` (513 rows, each split `raw` vs `derived`), `payload_manifest.json`,
`forensic_rows.json`, `tunnel.log` / `forensic_tunnel.log`, `run.log` / `forensic.log`.

## 1. What was executed (frozen protocol, no redesign)

- Origin: Python threaded HTTP server on 127.0.0.1 serving parent-faithful high-entropy
  payloads (JSON 5.57, HTML 4.66, BINARY 7.69 bits/byte; 10 240 B nominal) pre-compressed in
  two orders — GZIP-OUTER (inner brotli q4, outer gzip L1) and BROTLI-OUTER (inner gzip L1,
  outer brotli q4) — with correct `Content-Encoding`, plus identity payloads.
- CDN: two Cloudflare free-tier quick tunnels (`cloudflared` 2026.9.1, edge sjc01),
  verified reachable by `/health` probes through the public URL before measuring.
- Client: raw `http.client` reads (no content-decoding middleware), so recorded bytes are
  wire bytes. Streaming decompression unwraps outer-then-inner at 8192- and 32-byte feed
  granularity (parent-faithful); ground truth is within-run full-body iterative decode.
- Matrix: 48 conditions (3 payload × 2 orders × 2 chunk sizes × 4 Accept-Encoding variants)
  × 5 reps = 240 localhost + 240 CDN observations, unique URLs + 200–500 ms jitter on CDN;
  6 fixed-URL cache triplets (1 s spacing); 15 CDN identity observations.
- Post-matrix forensic probe (36 fetches, fresh tunnel): captured delivered bytes and ran
  gzip/brotli/iterative decode attempts to diagnose the failure mode required by the
  frozen decision rule.

## 2. Result

- **Positive control B-LOCALHOST-DIRECT: 240/240 correct, 240/240 byte passthrough.**
  The environment is valid; CDN inferences are licensed. Parent re-validation holds.
- **CDN main matrix: 60/240 correct (0.25).** The only passing cells are GZIP-OUTER
  fetched with client `Accept-Encoding` containing gzip (12/48 cells, 5/5 each).
  All other 36 cells fail 0/5 with decoder errors. Zero transport errors: this is CDN
  behavior, not infrastructure failure — a valid scientific negative (`status=COMPLETE`,
  `outcome=FALSIFIES`).
- **No chunk-size effect**: 8192 vs 32 agree on all 48 cells. The failure is purely
  Accept-Encoding × outer-encoding interaction.

## 3. Diagnosed failure mode (Accept-Encoding negotiation, three transforms)

Cloudflare transparently decodes/re-encodes origin `Content-Encoding` based on what the
client advertises (forensics: `forensic_rows.json`, all decode attempts recorded):

1. **Gunzip when client omits gzip.** GZIP-OUTER + AE `br`/`none` → inner-brotli bytes
   served with no `Content-Encoding` (forensic `br_dc` OK, iterative decode == ground truth).
2. **Always de-brotli.** BROTLI-OUTER is never byte-identical (0/120 passthrough, any AE).
   Text types are re-gzipped when the client accepts gzip (`Content-Encoding: gzip`,
   iterative decode == ground truth); octet-stream is served as decoded inner-gzip bytes
   with no `Content-Encoding` (mislabeled framing — unrecoverable without sniffing).
3. **Silent re-encode under an unchanged header.** HTML GZIP-OUTER + AE gzip is delivered
   as `Content-Encoding: gzip` but different bytes (2752 → 2759 B); still valid gzip of
   the same inner content. Header comparison alone cannot detect this class.
4. **Identity text gets compressed.** CDN gzip-compresses identity JSON/HTML when the
   client accepts gzip (benign, reversible); octet-stream identity passes through 5/5.

Consequence for the frozen decision rule: C1 fails (60/240), C2 fails (header match
60/240, byte passthrough 40/240), C4 fails literally (5/15, benign cause), C3 passes as
*serve stability* (6/6 triplets byte-stable; correctness only 3/6). Baselines
B-CDN-RAW-PASSTHROUGH (0/60), B-CDN-GZIP-ONLY (30/60), B-CDN-BROTLI-ONLY (0/60),
B-CDN-IDENTITY (5/15) all fail; only B-LOCALHOST-DIRECT passes.

## 4. The key diagnostic (bounds the damage and points at the fix)

Encoding-agnostic iterative full-body decode (try brotli → try gzip until identity)
recovers ground truth on **24/24 JSON/HTML forensic CDN deliveries** despite the
transforms. The failure is in the *fixed origin-order framing assumption* (replay the
origin's layer stack against wire bytes), not byte corruption. A decoder that sniffs
the delivered bytes instead of assuming origin order is the identified next fix — it
was **not** executed as a frozen condition and is therefore a hypothesis, not a result.

## 5. Scope / what this does not show

- Single edge (sjc01), single provider (Cloudflare free tier), 10 KB nominal, depth 2,
  gzip L1 / brotli q4, sequential requests. No concurrency, no >100 KB, no depths 3–5.
- `cf-cache-status` was DYNAMIC on all 273 CDN responses: no cache HIT was observed, so
  stale-cache serving is untested; C3 PASS means consecutive-serve stability only.
- BINARY forensic ground-truth comparison is in-session only (parent-known
  PYTHONHASHSEED dependence); within-run correctness comparisons are unaffected.

## 6. Product consequence (frozen negative branch)

Per the frozen `product_consequence_negative`: CDN Accept-Encoding negotiation breaks
fixed-order iterative decompression — C-MEAS-VALID is **blocked from Product Core
promotion** until the decompression path is made encoding-agnostic (sniff delivered
bytes / iterative decode) and that fix is validated through the same CDN protocol.
The failure mode is diagnosed precisely enough to specify that fix as the next
experiment; localhost results (three layers, parent chain) are untouched by this
falsification.
