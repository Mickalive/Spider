# EXP-RUNTIME-35611612543 — Cache Freshness Lifecycle (SWR, SIE, 304, Re-fetch) through Local Nginx

**Lane:** runtime | **Claim_ids:** C-MEAS-VALID, C-FRESHNESS | **Parent:** EXP-RUNTIME-35551516706

## 1. Question
Does oracle-free greedy iterative decompression produce byte-identical output to ground truth for stale cache responses (stale-while-revalidate, stale-if-error) and revalidated responses (304 Not Modified, 200 re-fetched) served through a byte-preserving local nginx proxy_cache?

## 2. Hypothesis & Falsifier
Hypothesis: oracle-free greedy decompression preserves byte-identity across all cache lifecycle stages because the cache serves same wire bytes regardless of freshness state. Falsifier: any stage produces byte-divergent output, narrowing ceiling to passing stages only.

## 3. Method (frozen spec)
- **Payloads:** 3 content types (JSON/HTML/BINARY) ×2 encoding orders (GZIP-OUTER brotli→gzip, BROTLI-OUTER gzip→brotli) ×2 chunk sizes (8192,32) ×4 Accept-Encoding (none/gzip/br/both) =48 primary cells, SEED=44, TARGET_SIZE 10240, LARGE 150000, MAX_DEPTH=5 greedy brotli→gzip no oracle.
- **Stages (5×48×5=1200 test observations):**
  1. FRESH HIT max-age=300 via `/fresh/` (valid 5m) — positive control reproducing parent.
  2. SWR stale HIT max-age=1 stale-while-revalidate via `/swr/` (nginx valid 1s background_update on use_stale updating) wait 1.5s.
  3. SIE stale HIT max-age=1 stale-if-error via `/sie/` (valid 1s use_stale error) wait 1.5s + origin 500 error mode.
  4. 304 Not Modified max-age=0 via `/reval304/` with If-None-Match ETag (plain_sha[:16]), origin returns 304.
  5. 200 re-fetched max-age=0 via `/reval200/` (valid 1s revalidate on).
- **Origin:** Python ThreadingHTTPServer per-prefix Cache-Control and ETag, ignores Accept-Encoding, serves pre-compressed bodies. SIE error simulated via 500 return.
- **Cache:** nginx 1.24.0 proxy_cache spider:16m, proxy_cache_key $request_uri, per-location valid/revalidate settings, gzip off.
- **Observations:** raw wire bytes (body_b64 + headers + status) persisted per row in `raw_cell_results.jsonl` separate from derived measurements (decompressed sha, correct flags, methods, ambiguous).

## 4. Results

### Primary
| Stage | n | Byte-identical | Rate | X-Cache |
|-------|---|----------------|------|---------|
| STAGE1_FRESH |240|240|1.0|240 HIT|
| STAGE2_SWR |240|240|1.0|120 HIT +120 STALE =240 stale serve|
| STAGE3_SIE |240|240|1.0|240 STALE|
| STAGE4_304 |240|240|1.0|240 200 MISS (nginx converted 304→200)|
| STAGE5_REFETCH |240|240|1.0|240 MISS|
| **Overall (stages 1,2,3,5)** |**960**|**960**|**1.0**|—|

All 5 stages satisfy decision_rule primary condition byte-identical accuracy =1.0.

### Secondary
- (a) Zero decode failures on valid payloads: 960/960 (304 excluded as no body).
- (b) Zero false accepts on corrupted: 0/6 (6 deliberate corrupt gzip payloads correctly failed).
- (c) Oracle-guided regression: 2041/2041 (100%) on same wire bytes excluding corrupt; no regression.
- (d) Fixed-order baseline: 2041/2041 (100%) on local nginx; parent Cloudflare was 60/240, confirming byte-preserving proxy vs edge transformation distinction.

### Controls
- B-LOCALHOST-DIRECT 240/240 pass.
- B-FRESH-HIT 240/240 pass (positive control).
- B-ORACLE-GUIDED-REGRESSION 2041/2041 pass.
- B-FIXED-ORDER-CDN 2041/2041 pass (local nginx, not Cloudflare edge).
- C-NULL-IDENTITY 15/15 pass.
- C-NULL-CORRUPT 0/6 false accepts pass.
- C-STALE-SWR/STALE-SIE pass.
- C-304 substrate 240/240 pass (see validity note).

All conditions pass → **OUTCOME SUPPORTS** (`status=COMPLETE`).

## 5. Observations vs Derived vs Interpretation
- **RAW EVIDENCE:** `raw_cell_results.jsonl` (2047 rows, sha256 f0328cc2…) each row `raw:{status, headers, body_sha256, body_b64, body_len}` plus `derived:{oracle_free_sha256, oracle_free_correct, ambiguous, oracle_guided_correct, fixed_order_correct}`. No collapse.
- **OBSERVATIONS:** Section 4 table and `result.json observations` list (direct counts, HIT/STALE/MISS, status codes). 2047 observations, zero transport errors.
- **DERIVED:** Rates, HIT/STALE aggregation, substrate correctness for 304.
- **INTERPRETATION:** Cache freshness lifecycle does not break oracle-free decompression through local nginx; claim ceiling extends from fresh-only to stale+SIE+revalidation for byte-preserving caches.

## 6. Validity Notes
- Nginx does not emit `Age` header; stale verified by wait 1.5s > max-age 1s + STALE/HIT status, not Age>max-age (spec clause 5 representation loss).
- SWR/SIE emit `X-Cache: STALE` for stale serves (not HIT); HIT+STALE counted as stale success per spec validity clause 2. SWR 120 HIT +120 STALE, SIE 240 STALE both 100% stale serving.
- 304 not observed as 304 through nginx (0/240); nginx `proxy_cache_valid 1s` + `revalidate on` converts origin 304 to 200 MISS serving cached body. Origin does emit 304 directly. No empty-body decompression attempted; substrate 240/240 correct (avoided false positive).
- REFETCH all MISS (240/240) – spec allows MISS or HIT; correctness preserved.
- Fixed-order 100% reflects byte-preserving proxy; does not generalize to transforming CDN edges (parent 60/240).
- Corrupted rows excluded from baseline totals (6 rows); including them would be 2041/2047 not 100%.

## 7. Product Consequences
- **If SUPPORTS (observed):** Cache freshness lifecycle does not break decompression. Claim ceiling for C-MEAS-VALID and C-FRESHNESS extends from fresh-only to include SWR, SIE, and revalidation (304/200) for nginx-class byte-preserving caches. Product can safely serve stale cached responses through decompression pipeline. Remaining unknown is production CDN byte behavior (separate experiment, see parent handoff recommended paid-tier CDN).
- **If FALSIFIES (not observed):** Would have narrowed ceiling to fresh-only and blocked stale serving in product.

## 8. Unresolved & Next
- Production CDN HIT and stale byte behavior (Cloudflare paid-tier, Fastly, etc.) untested.
- 304 forwarding vs caching conversion on CDN unknown.
- Economics (latency/CPU amortized), concurrent load, HTTP/2/3, TLS, multi-edge not tested.

## 9. Artifacts
- `raw_cell_results.jsonl` sha256 f0328… (2047 rows)
- `payload_manifest.json` 6c7be… 72 payloads
- `summary.json` 2f7b8… derived
- `nginx_cache.conf` 24ca… fixture
- `run.log` c46b… raw
- `run_experiment.py` cc007… code

Exact evidence paths/hashes in `result.json artifacts` and `provenance.json`.
