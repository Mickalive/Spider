# EXP-RUNTIME-35551516706 — EXECUTE report

- Lane: `runtime` · Status: `COMPLETE` · Outcome: `SUPPORTS`
- Claim under test: `C-MEAS-VALID` — oracle-free greedy iterative decompression is byte-valid against ground truth on cached (stale-compressed) CDN-like HTTP responses.
- Frozen design: `request.json`, `spec.json`, `prereg.md`, `freeze.json` (immutable, git `611585ed`). Executed exactly as frozen.

## 1. Frozen question and hypothesis

**Question (from `request.json`):** On a local nginx caching reverse proxy that produces real `cf-cache-status: HIT`-equivalent responses, does oracle-free greedy iterative decompression produce byte-identical output to ground truth for cached (stale) responses, and does the decompressed output differ from the DYNAMIC-path decompressed output?

**Hypothesis (frozen):** A local nginx `proxy_cache` in front of the same Python origin produces real cache HITs; oracle-free greedy iterative decode (try brotli → gzip until neither succeeds, MAX_DEPTH=5, no SHA256 oracle) produces byte-identical output to ground truth for ≥90% of cache HIT observations; cache HIT wire bytes are byte-identical to DYNAMIC wire bytes per payload; the parent's 0% HIT rate was an infrastructure ceiling (Cloudflare free tier), not a property of the greedy decoder.

## 2. Infrastructure (Phase 0)

- Stack: Python 3.12.14 origin (`ThreadingHTTPServer`, `brotli 1.2.0`) on `127.0.0.1:18794`; nginx `1.24.0 (Ubuntu)` `proxy_cache` reverse proxy on `127.0.0.1:18080`.
- Cache config (`nginx_cache.conf`, artifact): `proxy_cache_key $request_uri` (URI only), `proxy_cache_valid 200 5m`, `gzip off`, keys_zone `spider:16m`, `use_temp_path off`. Origin serves `Cache-Control: public, max-age=300` and ignores `Accept-Encoding` (pre-compressed bodies per token).
- Warm-up: 10 consecutive GETs to one fixed URL → `X-Cache: MISS,HIT×9` (9/10 HIT). HIT capability confirmed on the first attempt; no config relaxation was required.
- Cache-key negative control: DYNAMIC phase used unique cache-busting query per request → 240/240 `X-Cache: MISS`, proving the cache is really keyed and engaged.

## 3. Payload matrix (frozen)

48 cells = 3 content types (JSON/HTML/BINARY, entropy 4.66–7.70 bits/byte) × 2 layer orders (GZIP-OUTER, BROTLI-OUTER) × 2 chunk sizes (8192, 32) × 4 Accept-Encoding variants (none/gzip/br/gzip,br), SEED=44, REPS=5, MAX_DEPTH=5, TARGET_SIZE=10240. Plus depth 3/4/5 stacked encodings, >100KB large payloads, identity (uncompressed) payloads, and 6 stability groups. Ground truth: for all 72 registered payloads `fullbody_decompress(compressed) == plain body` (`gt_is_plain` true).

## 4. Results by phase

| Phase | Purpose | Result |
|---|---|---|
| 0 | infra validation / warm-up HIT | 9/10 HIT; nginx -t clean |
| 1 | B-LOCALHOST-DIRECT (positive control, origin direct) | 240/240 oracle-free correct |
| 2 | DYNAMIC through nginx (cache-busted, 240 MISS) | 240/240 oracle-free correct |
| 3 | HIT path (48×5 populate+test) | 240/240 test responses X-Cache: HIT; 240/240 oracle-free correct |
| 4 | C8 DYNAMIC-vs-HIT wire identity | 48/48 cells byte-identical |
| 5 | C3 stability (6×3) + C4 identity (15) | 6/6 groups stable; 15/15 correct |
| 6 | C5 depth 3–5 (45) | 45/45 = 100% |
| 7 | C6 large >100KB (30) | 30/30 = 100% |
| 8 | B-ORACLE-GUIDED-REGRESSION + B-FIXED-ORDER-CDN (480 rows) | 480/480 and 480/480 |

## 5. Decision rule (frozen) — all conditions

| Condition | Threshold | Observed | Pass |
|---|---|---|---|
| C1 | all 48 primary cache HIT cells recover ground truth (all reps) | 48/48 | ✔ |
| C2 | ≥90% of cache HIT observations byte-identical | 330/330 = 1.0 (312/312 among x-cache==HIT) | ✔ |
| C3 | 6/6 stability groups byte-stable + correctly decoded | 6/6 | ✔ |
| C4 | 15/15 identity observations recover ground truth | 15/15 | ✔ |
| C5 | depth 3–5 ≥80% correct | 45/45 = 1.0 | ✔ |
| C6 | large >100KB ≥80% correct | 30/30 = 1.0 | ✔ |
| C7 | zero ambiguous tie-breaks | 0 / 1078 | ✔ |
| C8 | DYNAMIC vs HIT wire bytes identical ≥90% of cells | 48/48 = 1.0 | ✔ |

Verdict per frozen mapping (C1 pass ∧ C2 pass ∧ C8 pass ∧ all others pass) → **SUPPORTS**.

## 6. Baselines and controls

- **B-LOCALHOST-DIRECT (positive control):** 240/240 — the greedy decoder is exact on origin bytes; establishes the experiment can detect mistakes.
- **B-ORACLE-GUIDED-REGRESSION:** 480/480 on the same wire bytes as the frozen tests — no regression vs parent's 240/240 Cloudflare DYNAMIC.
- **B-FIXED-ORDER-CDN:** 480/480 (parent Cloudflare value: 60/240). Local nginx does **not** re-encode bytes, so origin framing holds 100%. This is consistent with — and further confirms — the parent's established finding that *the CDN edge, not byte corruption, broke the fixed-order framing assumption*. The 60/240 figure remains Cloudflare-specific; this experiment's substrate cannot reproduce CDN edge transformation.
- **B-DYNAMIC-VS-HIT-IDENTITY (null control):** 48/48 cells byte-identical → the hypothesis that "cache serve alters bytes" is falsified for a byte-preserving local proxy.
- **C-CACHE-MISS-KEY-NEGATIVE:** 240/240 DYNAMIC requests were MISS → cache was genuinely engaged.

## 7. Interpretation (bounded)

1. **The parent's 0% HIT rate was an infra ceiling.** A local nginx `proxy_cache` yields real HIT responses (240/240 test-phase). The runtime mechanism can obtain stale-compressed cached responses.
2. **Oracle-free greedy decode is byte-valid on cached responses.** 100% byte-identical to ground truth across 330 cached-path observations (all session kinds 1078/1078), including depth-3/4/5 stacks, >100KB payloads, and uncompressed identity payloads. No ambiguous tie-breaks.
3. **Cache HIT serving did not alter bytes** (C8 48/48, stability 6/6, fixed-order 480/480) — for a byte-preserving local proxy.
4. **The confidence ceiling of this run is bounded to nginx-class byte-preserving caches.** Whether real CDN edges (e.g., Cloudflare) transform cached-response bytes on serve remains untested (parent had no HIT observations on Cloudflare free tier to test it). See `unresolved` in `result.json`.

## 8. Evidence integrity

- `raw_cell_results.jsonl` (12.4 MB, sha256 `7563c068…`): every row = `raw` (wire bytes base64 + headers + status) distinct from `derived` (all three decode algorithms over the same bytes). 0 transport errors, 0 duplicate keys, 0 raw/derived SHA mismatches — independently recomputable.
- `payload_manifest.json`, `summary.json`, `hit_vs_dynamic.json` (C8 per-cell detail), `nginx_cache.conf`, `run.log` — hashes in `result.json.artifacts`.
- No git mutation was performed in EXECUTE; frozen inputs were already committed at `611585ed`, run artifacts are working-tree files.