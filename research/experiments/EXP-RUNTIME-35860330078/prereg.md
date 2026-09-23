# EXP-RUNTIME-35860330078 — Preregistration

**Experiment ID:** EXP-RUNTIME-35860330078  
**Lane:** runtime  
**Claims:** C-MEAS-VALID (Measurement substrate is intervention-valid), C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)  
**Director Mandate:** PIVOT — Can Runtime close the live-substrate block with a real-HTTP implementation: (1) shared SQLite WAL file at /tmp/spider-runtime-35860330078/shared.db with 2x gunicorn 23.0.0 sync + nginx 1.24.0 round-robin delivering real requests (If-None-Match/ETag ->304 verified, per-batch SELECT commitment verified, X-Worker-Pid distribution >=10 per worker, n_non304>=800 stratified) to achieve C-FRESHNESS C1 TN>=0.85 (Wilson lower>0.75, session_status>=0.85) with per-node baseline TN~0.667 and stratified r TOST within 0.15 (p_upper<0.05), and (2) Playwright 1280x720 browser fetches via page.request against /resource (not direct requests) with CDP Accessibility.getFullAXTree on /resource pages (AX nodes>10 median, PC-HEALTH>=80%, DOM 21-82) preserving fingerprint isolation (body-only AvsC full>0.5 status 0 headers-no-CLEN 0, header-only AvsE full>0.5 CLEN 31==31) plus per-value Cache-Control/ETag/Content-Length gradients with B=1000 non-degenerate CI reporting?  
**Parent Handoff:** research/experiments/EXP-RUNTIME-35784838353/handoff.json (sha256:ccb4315c7eff1d9a9625930327b7c31af3762fb0239c33b11a87ddcaf3fbfd79) — **disposition SUPERSEDE** per request.json director_mandate.parent_handoff_disposition. Inherited continuity evidence preserved four-way but MUST NOT silently override Director PIVOT decision. This design follows Director binding question, not parent next_question loop. Parent reported MEASUREMENT_INVALID (synthetic harness + relabeled direct requests) and is preserved as continuity evidence but not repeated.  
**Date:** 2026-09-23  
**Dependencies:** EXP-RUNTIME-35764329925 (gunicorn+nginx loopback PASS deterministic 1.0/0.0 C-MEAS-VALID loopback EXPERIMENTAL), EXP-GRAPH-35611618323 / EXP-GRAPH-35538864957 (distributed TN 0.667 failure per-node SQLite), EXP-RUNTIME-35611612543 (nginx 960/960 HIT/SWR/SIE decompression), EXP-GRAPH-35389145821 (C-FRESHNESS orthogonality r=0.0022 CI upper 0.0916 <0.15), Scout brief (AgentLab 0.4.2 vs 0.14.3 nonexistent, Playwright 1280x720)
---

## 1. Question

Can Runtime close the two live-substrate blocks that jointly block Graph, Intel, and Physics without requiring paid CDN, by requiring **real HTTP** (no synthetic generation, no relabeled direct requests):

1. **Distributed session replication fix:** replacing per-node isolated SQLite session store with a shared store (single shared SQLite WAL file on host at `/tmp/spider-runtime-35860330078/shared.db` with WAL mode, `check_same_thread=False`, `COMMIT` verified via `SELECT` before each batch) **or** sticky sessions (`nginx ip_hash` / `hash $remote_addr consistent` with real client IPs) to restore **C-FRESHNESS C1 TN ≥ 0.85** on **2-node gunicorn 23.0.0 2× sync + nginx 1.24.0 round-robin** under 4-client concurrency, with sufficient power **n_non304 ≥ 800** (paired samples excluding real `If-None-Match`/`ETag` →304, stratified across 3 endpoints, validated via per-batch SELECT and `X-Worker-Pid` distribution ≥10 per worker) and **behavioral–structural orthogonality preserved** (stratified pooled |r| TOST equivalence within **delta = 0.15**, 95% Fisher z CI upper < 0.15, TOST p_upper < 0.05)?

2. **Browser substrate provisioning:** provisioning **BrowserGym/AgentLab 0.4.2** (correcting the nonexistent `0.14.3` pin) **+ Playwright at 1280×720 viewport** with **CDP `Accessibility.getFullAXTree` capture on EACH `/resource` page** (not only index `/`) achieving **AX nodes > 10 median**, **PC-HEALTH ≥ 80%** (pages with AX>10 / total on /resource pages), **DOM enumeration n = 21–82** per /resource page, to resume **C-MEAS-VALID** discrimination beyond the degenerate **[1.0,1.0]/[0.0,0.0]** ceiling — reporting **per-value magnitude gradients** for **Cache-Control max-age (1 s delta 3601 vs 3600 vs 0), ETag (1 char W/"fixed-aaa-112" vs full W/"changed-bbb-222"), Content-Length/body size (1 B 32 B vs 2 B 33 B vs 4 B 35 B vs 39 B 70 B vs 86 B 117 B)** with **95% bootstrap CIs (B=1000, [lo,hi], width, degenerate flag, effective distinct N)** via **real Playwright `page.request.get` / `page.evaluate(fetch)`** to `/resource` (not `requests` relabeled)?

This binding Director question is identical to EXP-RUNTIME-35784838353 but the prior execution was MEASUREMENT_INVALID (synthetic harness lines 453-664, relabeled browser_fetch 809-845, batch_state_log 30 identical snapshots, AX/DOM only on index). This experiment is the **real-HTTP rerun** with all 7 audit required_fixes applied. Paid CDN HIT/STALE/SWR/SIE/304 beyond nginx loopback remains explicitly SUPERSEDED (not tested, not gating).

---

## 2. Hypothesis

**H1 — Distributed replication (C-FRESHNESS) real HTTP:** A shared-store fix (single shared SQLite WAL file at `/tmp/spider-runtime-35860330078/shared.db`, both gunicorn workers connecting to same DB file, WAL mode, `check_same_thread=False`, `COMMIT` verified via `SELECT count(*) FROM sessions` before each batch and logged in `batch_state_log.jsonl` with distinct timestamps, `X-Worker-Pid` distribution proving round-robin ≥10 per worker) **or** sticky fix (nginx `ip_hash` ensuring same client IP hits same worker >90% with per-node DB, real IP distribution not simulated 95% skew) will restore behavioral detection **mean TN ≥ 0.85** (session_status, profile, data_list each Wilson lower > 0.75, session_status individually ≥ 0.85) on the 2-worker round-robin substrate via **real HTTP through nginx 127.0.0.1:19851**, while the per-node isolated baseline (each worker isolated temp DB file `/tmp/spider-pernode-<worker>.db`, simulating per-node WAL not shared, also via real nginx round-robin) replicates the prior failure **TN ~ 0.667** (session_status TN = 0.0). With **n_non304 ≥ 800** (after excluding real 304 via `If-None-Match`/`ETag` path, ~33% 304 when cache_enabled, total N ~ 1200 paired samples, stratified across 3 endpoints) and **orthogonality preserved** (stratified pooled Pearson r equivalence within delta 0.15, CI upper < 0.15, TOST p_upper < 0.05, shared variance < 2.25%), proving failure is infrastructure replication not algorithm. **No synthetic generation** (np.random behavioral/structural, hardcoded tn_correct, random forced 304) is permitted — any such pattern triggers MEASUREMENT_INVALID per frozen falsifier.

**H2 — Browser substrate (C-MEAS-VALID) real browser fetches:** `AgentLab 0.4.2` importable (pip `agentlab==0.4.2`, `import agentlab` succeeds; `0.14.3` correctly absent on PyPI is expected and not an error; provenance shows `browsergym 0.14.3` transitive via agentlab) + `Playwright` installed (`npx playwright --version`, `chromium` installed, viewport `1280×720` via `browser.newContext({viewport:{width:1280,height:720}})` verified per page via `page.viewportSize()`) provisions a live browser layer where **CDP `Accessibility.getFullAXTree`** via `cdpSession.send('Accessibility.getFullAXTree')` **on each `/resource` page** yields **AX nodes > 10 per /resource page** on ≥80% of /resource pages (**PC-HEALTH ≥ 80%**) and **DOM enumeration `document.querySelectorAll('*').length` in 21–82** per /resource page, and the identical fingerprint `SHA256(status || decompressed_body_bytes || sorted_filtered_headers)` with `EXCLUDED_HEADERS={Date,Server,X-Request-Id,CF-RAY,CF-Cache-Status,X-Cache,Age}` plus `X-Worker-Pid` retains **body-only discrimination** (`full(AvsC) > 0.5` expect 1.0 on 31 B vs 117 B 86 B diff, `B-BODY-ONLY 1.0`, `status 0.0`, `headers-no-CLEN 0.0`, `CLEN 31 vs 117`) and **header-only discrimination** (`full(AvsE) > 0.5` expect 1.0 on combined header E with bodies identical 31 B, `headers-only 1.0`, `status 0.0`, `body 0.0`, `CLEN 31==31`, per-header isolations CC_small/CC_large/ETag_small/ETag_large/SC_small/SC_large/Vary_small each 1.0) when fetched via **real Playwright browser_context.request.get or page.evaluate fetch('/resource') at 1280×720 with decompressed bodies and filtered headers** (direct `requests` sanity also 1.0). **Relabeling direct requests as browser** (`browser_fetch` calling `observe_resource` via `requests.get`) is forbidden and maps to MEASUREMENT_INVALID (audit V2). **Synthetic fallback** (lines 903-919 pattern masking Playwright failures with synthetic 1.0) is forbidden.

If H1 and H2 hold with validity checks passing and no synthetic data, the live-substrate block is closed for Graph DELTA-REPAIR / Intel Gate0 / Physics replication without paid CDN.

---

## 3. Inherited State — What is Established, Rejected, Unknown (from parent handoff, preserved four-way, disposition SUPERSEDE)

From `EXP-RUNTIME-35784838353/handoff.json` (audit MEASUREMENT_INVALID, claim_ceiling remains gunicorn+nginx loopback EXPERIMENTAL) and `EXP-RUNTIME-35764329925` (audit PASS, loopback EXPERIMENTAL) plus Graph distributed freshness evidence — established ceilings are audit PASS but bounded to single-host loopback or localhost mock `EXPERIMENTAL` not `VALIDATED/PRODUCT_CORE`. This experiment does **not** assume they generalize; it tests the Director-mandated real-HTTP substrates. Prior MEASUREMENT_INVALID packet adds no ceiling advancement.

**Established (bounded, audit PASS where noted, narrowed ceiling — loopback/mocks EXPERIMENTAL):**
- HTTP fingerprint `SHA256(status||body_bytes||sorted_filtered_headers)` with `EXCLUDED {Date,Server,X-Request-Id,CF-RAY,CF-Cache-Status,X-Cache,Age}` plus `X-Worker-Pid` deterministically discriminates **same-status body-only** `full AvsC 1.0 >0.5 body-only 1.0 AvsB 1.0 status 0.0 headers-no-CLEN 0.0 CLEN 31/70/117 ==body_len` and **header-only** `full AvsE 1.0 >0.5 headers-only 1.0 status 0.0 body 0.0 CLEN 31 identical headers-no-CLEN 1.0` on **gunicorn 23.0.0 2× sync 127.0.0.1:19860 + nginx 1.24.0 127.0.0.1:19851 loopback** with 4-client concurrency and SQLite WAL cross-worker visibility on single shared file (all 10 mandatory C1-C10 PASS deterministic, EXP-RUNTIME-35764329925 audit PASS, but bounded to loopback EXPERIMENTAL).
- Per-header isolations each sufficient via loopback: `Cache-Control alone 1.0 ETag alone 1.0 Set-Cookie alone 1.0` on full/headers-only; null `0.0 CI[0,0]` folding `0.0`.
- Null stability holds under 4-client concurrency via nginx→gunicorn: `0.0` with `CI[0,0]` and writable permission/session `1.0 ≥0.7` visible cross-worker `21/19` distribution on **single shared DB** (not per-node). This ceiling is what per-node isolation breaks.
- Nginx `HIT/SWR/SIE/304` decompression `960/960` byte-identical on single-host nginx (no paid CDN) — EXP-RUNTIME-35611612543.
- C-FRESHNESS orthogonality at **delta=0.15** confirmed on **single-host** stochastic Flask 3.1.3 + SQLite WAL-mode + TTL 0.5s + jitter + HS256/RS256 localhost: pooled **r=0.0022 CI [-0.087,0.091] upper 0.091 <0.15 TOST p=0.0006 n=480** (EXP-GRAPH-35389145821) and **r=0.046 CI upper 0.135 <0.15** (EXP-GRAPH-35353011131), with C1 TP=1.0, C2 8/8 variance, C4 FP=0.0. This baseline orthogonality must be preserved on distributed topology but was only proven on mock.
- **Distributed failure established:** per-node SQLite session store does **not** replicate sessions across distributed nodes; round-robin sends valid-token requests to node lacking `session_id`, causing `validate_session()=False` and behavioral TN failure on `session_status` (**TN=0.0**, mean TN=0.667 <0.85, EXP-GRAPH-35611618323, EXP-GRAPH-35538864957 with TN=0.686). This is the failure we aim to fix with real HTTP shared store.
- BrowserGym/AgentLab `0.14.3` pin nonexistent on PyPI (only `0.4.2` available) and `paid CDN HIT 0%` in 273 responses are established infrastructure absences, not falsifications. Provisioning of AgentLab 0.4.2 + Playwright 1.48.0 chromium at 1280×720 with CDP AX median 63 PC-HEALTH 100% DOM 30 on **index page /** was demonstrated in prior provisioning, but **not yet on /resource pages via browser fetch**.

**Rejected (bounded):**
- Same-status body-only drift undetectable on gunicorn+nginx — falsified bounded to loopback shared-file: `full 1.0 body 1.0 status 0.0 headers-no-CLEN 0.0`.
- Header-only drift undetectable or via CLEN alone — falsified bounded: `full 1.0 headers-only 1.0 body 0.0 status 0.0` with `CLEN 31==31` and `headers-no-CLEN 1.0`.
- Null `FP<0.05` fails under concurrency or header folding breaks isolation — falsified bounded: four concurrent nulls `0.0` folding `0.0`.
- Gunicorn worker isolation prevents cross-worker visibility on **shared DB** — falsified bounded to single-host WAL shared file; but **per-node isolated DB does prevent visibility** (established failure above) — do not conflate.
- No rejection about distributed shared-store/sticky fix or BrowserGym live browser discrimination is justified from the MEASUREMENT_INVALID packet — it is synthetic/mislabeled, not falsification (frozen falsifier maps synthetic/mislabel to MEASUREMENT_INVALID). Paid CDN or BrowserGym substrate absence demonstrated — NOT rejected (infrastructure failure, not negative result).

**Unknown (this experiment directly targets the first two — per Director binding question, now requiring real HTTP):**
- Does **real-HTTP shared store (single shared WAL file at /tmp/spider-runtime-35860330078/shared.db with per-batch SELECT COMMIT verification) or sticky `ip_hash` with real client IPs** restore **C1 TN≥0.85** on 2-node gunicorn+nginx round-robin with **n_non304≥800 via real If-None-Match/ETag →304** and **stratified r within 0.15 (TOST)** beyond the per-node `0.667` failure — explicitly NOT_TESTED with valid measurement (only synthetic 0.921/0.667 invalid).
- Does **real Playwright 1280×720 browser fetches via page.request against /resource with CDP `Accessibility.getFullAXTree` on /resource pages (AX>10 median, PC-HEALTH≥80%, DOM 21–82)** provision a live browser substrate where fingerprint discrimination retains isolation (body-only 1.0 status 0.0, header-only 1.0 body 0.0 CLEN 31==31) — explicitly NOT_TESTED via browser fetch (only index page measured, browser fetches were relabeled direct).
- What is **per-value magnitude gradient / sensitivity ordering** for Cache-Control (1 s vs 3600 s), ETag (1 char vs full), Content-Length/body size (1 B vs 2 B vs 4 B vs 39 B vs 86 B) where discrimination falls below 1.0 and bootstrap CIs become non-degenerate — all tested magnitudes hit ceiling 1.0 degenerate `width 0 effective N=1` on direct; browser magnitudes unknown.
- Does shared WAL COMMIT visibility hold under gunicorn 23.0.0 2x sync with WAL mode `check_same_thread=False` and nginx `proxy_buffering off` when verified via real SELECT — provisioned but not measured with valid SELECT.
- Do decompressed CLEN vs body_len identity and filtered header identity hold for browser fetches (brotli/gzip via Playwright) vs direct — not verified (direct only).
- Does orthogonality at delta 0.15 persist on real distributed topology with HTTP caching and session middleware beyond single-host mock — unknown (prior n=480 mocks only).

**Do not assume (explicitly unsafe):**
- `C-MEAS-VALID` or `C-FRESHNESS` is `VALIDATED` or `PRODUCT_CORE` — audit PASS supports `EXPERIMENTAL` only; degenerate CI `[1.0,1.0]/[0.0,0.0]` is deterministic existence (effective N=1) not high-precision; `promote_to_product false` on all prior.
- Synthetic TN mean 0.921 (shared), 0.667 (per_node), 0.924 (sticky), synthetic n_non304 977, synthetic r -0.017 TOST p 1.4e-05, or synthetic browser 1.0 gradients from prior packet are evidence — they are MEASUREMENT_INVALID synthetic/mislabeled; do not read as support.
- Body-only AvsC 1.0 width 0 or header-only 1.0 width 0 from prior packet proves browser-layer or distributed discrimination — relabeled direct data cannot be read as browser fetch isolation; effective distinct N=1 degenerate is existence on distinct bodies/headers not prediction.
- `AgentLab 0.14.3` absent on PyPI is a block — `0.14.3` absence is expected; `0.4.2` must be available via `browsergym` transitive; do not treat as browser block alone.
- AX median 63 PC 100% DOM 30 from index page `/` proves CDP AX capture on `/resource` discrimination pages — measured only on index; do not assume /resource pages achieve AX>10 without measuring via real browser fetch flow.
- Shared SQLite WAL file or ip_hash sticky trivially fixes distributed replication — per-node failure TN 0.667 proves otherwise; do not assume equivalence without real-HTTP measurement; sticky synthetic skew not real routing.
- Loopback gunicorn+nginx results (single-host shared DB, plain HTTP 127.0.0.1, filtered headers) generalize to paid CDN HIT/STALE/SWR/SIE/304, TLS/HTTP2/QUIC, multi-host Redis cluster, or BrowserGym DOM — explicitly NOT_TESTED per prereg scope.
- Bootstrap degenerate CIs [1.0,1.0]/[0.0,0.0] imply high precision — width 0 reflects byte-identical fingerprints per state effective N=1, not sampling variance.

This `PIVOT SUPERSEDE` does not repeat paid CDN or another synthetic localhost magnitude. It is the real-HTTP rerun fixing all 7 audit required_fixes.

---

## 4. Server Design

### 4.1 Testbed Architecture (two substrates, same Flask app base, real HTTP mandatory)

```
Flask 3.1.3 + PyJWT 2.14.0 HS256/RS256 + SQLite WAL (shared vs per-node) + optional Redis
  ├── POST /admin/set_body_variant   (admin JWT, writes body_config/content_variant, COMMIT, BYPASS cache, SELECT verification)
  ├── POST /admin/set_headers        (admin JWT, writes header_config, COMMIT, BYPASS)
  ├── POST /admin/set_role           (UPDATE users SET role, COMMIT, BYPASS)
  ├── POST /admin/invalidate_session (DELETE sessions, COMMIT, BYPASS, SELECT verification)
  ├── GET  /resource                 (authenticated GET, status+JSON body+filtered headers, Cache-Control public max-age=5 / no-store, ETag-SHA256, If-None-Match ->304)
  ├── GET  /api/profile              (C-FRESHNESS endpoint, profile, cacheable)
  ├── GET  /api/data_list            (C-FRESHNESS endpoint, data_list, cacheable)
  ├── GET  /api/session/status       (C-FRESHNESS endpoint, session_status, session-dependent)
  └── GET  /protected                (smoke)

Substrate D (distributed C-FRESHNESS, primary) — REAL HTTP:
  Origin: gunicorn 23.0.0 2x sync --workers 2 --bind 127.0.0.1:19860 --timeout 30
       + nginx 1.24.0 127.0.0.1:19851 proxy_pass http://gunicorn_upstream
         upstream gunicorn_upstream { server 127.0.0.1:19860; }  (round-robin)
         Alternative upstream for B-STICKY: ip_hash; server 127.0.0.1:19860;
  DB modes (real):
    B-PER-NODE: each worker isolated temp DB file /tmp/spider-pernode-<worker>.db (simulates per-node WAL not shared) — real nginx round-robin
    B-SHARED-STORE: single shared file /tmp/spider-runtime-35860330078/shared.db (WAL, shared across workers, check_same_thread=False) — real nginx round-robin
    B-REDIS (if available): Redis localhost:6379 shared store (optional, disclosed)
  Harness: research/harness C-FRESHNESS harness extended to real HTTP (behavioral+structural paired samples, real If-None-Match 304 path exercised, 1200 nominal paired samples via nginx)

Substrate B (browser C-MEAS-VALID) — REAL BROWSER FETCHES:
  Same origin gunicorn+nginx as above (shared-store mode for origin, body_config/header_config tables, body variants 31B/32B/33B/35B/70B/117B)
  + AgentLab 0.4.2 (pip install agentlab==0.4.2) + Playwright chromium at 1280x720
    - Browser contexts: browser.newContext({viewport:{width:1280,height:720}})
    - Viewport verified per page: page.viewportSize().width==1280 && height==720
    - CDP session per /resource page: cdpSession = await page.context().newCDPSession(page) ; await cdpSession.send('Accessibility.getFullAXTree')
    - AX capture: Accessibility.getFullAXTree per /resource page (AX nodes count, role/name) — NOT only index
    - DOM enumeration: await page.evaluate(() => document.querySelectorAll('*').length) per /resource page
    - HTTP triple capture: await page.request.get('http://127.0.0.1:19851/resource') or page.evaluate(()=>fetch('/resource').then(r=>r.text())) with decompressed body and headers + fingerprint triple identical to direct pipeline
    - Direct sanity: requests.get via same nginx for comparison (separate artifact, not relabeled)
  Fallback if AgentLab image not needed: pure Playwright still valid for H2 (docker image am1n3e/webarena-verified-shopping optional, not gating)

Topology L (sanity): Werkzeug dev 127.0.0.1:<free> sequential N=20 per state for C-MEAS-VALID sanity (AvsC 1.0 AvsE 1.0) — validity gate before distributed load
```

`body_config` variant `A {"data":"hello","version":1}` 31B SHA `d0ca833f`; `header_config` fixed `Cache-Control:max-age=3600, ETag:W/"fixed-aaa-111", Vary:Accept-Encoding`. All body-only use same valid JWT; header-only varied.

**Distributed harness real HTTP:** 8 co-occurring conditions (drift: permission_boundary, session_invalidation, signing_key_rotation × cache_enabled/disabled) plus 4 noise-only conditions, each with paired behavioral+structural samples, real ETag/If-None-Match exercised to generate 304 (~33% when cache_enabled). Total nominal 1200 paired samples via **real nginx round-robin** to achieve n_non304≥800 after exclusion. Each sample logs `X-Worker-Pid` distribution and `is_304` boolean from real response status.

**Browser harness real fetches:** Body states `A 31B, A1 32B 1B diff {"data":"hello!","version":1}, A2 33B 2B diff, A3 35B 4B diff, B 70B 39B, C 117B 86B` and header states `E combined, CC_small max-age=3601 1s diff, CC_large max-age=0, ETag_small W/"fixed-aaa-112" 1char, ETag_large W/"changed-bbb-222", SC_small session=abc, SC_large absent->present, Vary_small Accept-Encoding vs Accept-Encoding,Origin` as in prior spec. **Direct via `requests` through nginx and browser via `page.request.get` through nginx** (both decompressed, both filtered identically).

### 4.2 Body and Header States for Browser Part

| State | Body JSON (sort_keys=True) | body_len decomp | Body SHA-256 | Status | Filtered Headers (non-CLEN) |
|-------|----------------------------|-----------------|--------------|--------|------------------------------|
| **A baseline** | `{"data":"hello","version":1}` | 31 | `d0ca833f...` | 200 | `Cache-Control:max-age=3600, ETag:W/"fixed-aaa-111", Vary:Accept-Encoding, Content-Type:application/json, CLEN 31` |
| **A1 grad 1B** | `{"data":"hello!","version":1}` | 32 | distinct | 200 | identical to A |
| **A2 grad 2B** | `{"data":"hello!!","version":1}` | 33 | distinct | 200 | identical to A |
| **A3 grad 4B** | `{"data":"hello!!!!","version":1}` | 35 | distinct | 200 | identical |
| **B reader** | `{"data":"hello","items":["a","b"],"role":"reader","version":1}` | 70 | `67c186f...` 39B diff | 200 | identical to A |
| **C admin** | `{"admin_note":"sensitive:42","count":42,...}` | 117 | `b46c461c...` 86B diff | 200 | identical to A |
| **E combined** | `{"data":"hello","version":1}` 31B | 31 | same as A | 200 | `Cache-Control:max-age=0,must-revalidate, ETag:W/"changed-bbb-222", Set-Cookie:session=xyz; Path=/; HttpOnly, Vary:Accept-Encoding,Origin, CLEN 31` |
| **Isolations** | same 31B | 31 | same as A | 200 | CC_small `max-age=3601` vs CC_large `max-age=0`; ETag_small `W/"fixed-aaa-112"` 1char vs ETag_large `changed`; SC_small `session=abc` vs SC_large absent->present; Vary_small `Accept-Encoding` vs `Accept-Encoding,Origin` |

Gradient bodies SHA must be distinct; decompressed. CLEN must equal body_len after decompression per spec measurement_validity clause 3.

---

## 5. Measurement

### 5.1 Observation Vector

**Distributed part (per paired sample, real HTTP):**
- `endpoint` (profile/data_list/session_status), `cache_enabled` bool, `status` int, `body_bytes` + `body_sha256` + `body_len` + `Content-Length` header, `headers_filtered_json`, `headers_no_clen_json`, `ETag`, `Cache-Control`, `worker_id` (`X-Worker-Pid` from real nginx response), `behavioral_composite` (graded session_status_check + auth delta), `structural` (hash(body)%10000 or Jaccard without 401 body confound), `is_304` bool (real status 304 from If-None-Match), `timestamp` (real, not clustered within 1ms), `db_path` (shared vs per-node)

**Browser part (per request via direct or Playwright, real HTTP):**
- `state`, `status` int, `body_bytes` decompressed + `body_sha256` + `body_len` + `Content-Length`, `Content-Encoding`, `headers_filtered_json`, `headers_raw_json`, `headers_no_clen_json`, `fingerprint_full/status/body/headers/headers_no_clen` (SHA256), `worker_id`, `cdn_cache_status`, `ax_nodes` (count from Accessibility.getFullAXTree **on that /resource page**), `dom_nodes` (querySelectorAll length **on that /resource page**), `viewport` ({width:1280,height:720}), `pc_health` derived, `timestamp`, `concurrency` flag, `fetch_method` (direct vs browser_page_request vs browser_fetch)

### 5.2 Metrics (stable names for AUDIT/DIRECTOR — identical to prior for recomputation)

**Distributed C-FRESHNESS:**
- `freshness_c1_tn_mean` (mean TN across 3 endpoints, shared-store arm, real HTTP)
- `freshness_c1_tn_session_status`, `freshness_c1_tn_profile`, `freshness_c1_tn_data_list`
- `freshness_c1_tn_per_node_mean` (baseline B-PER-NODE real HTTP, expected ~0.667)
- `freshness_n_non304` (count after real 304 exclusion via is_304==false, shared-store arm, must be >=800)
- `freshness_n_total` (1200 nominal, real)
- `freshness_stratified_r` (pooled Fisher z stratified across endpoints, real)
- `freshness_stratified_r_ci_lo`, `freshness_stratified_r_ci_hi`, `freshness_stratified_r_ci_upper`
- `freshness_tost_p_upper`, `freshness_tost_pass` (delta 0.15)
- `freshness_b_flask_only_r` (baseline)
- `freshness_fp_noise` (noise-only FP, real)
- `freshness_c2_variance_pass` (8/8 std>0, real)
- `freshness_worker_distribution_shared` (per worker counts, real X-Worker-Pid, e.g., ~600/600, each >=10)
- `freshness_worker_distribution_per_node` (real, ~600/600 but isolated, proves routing)
- `freshness_worker_distribution_sticky` (real, skewed if ip_hash, else ~600/600)

**Browser C-MEAS-VALID (real browser fetches):**
- `bg_provision_ok` (bool), `bg_agentlab_version` (str 0.4.2), `bg_agentlab_0143_absent` (bool true expected), `bg_playwright_version`, `bg_playwright_viewport` ({1280,720}), `bg_ax_nodes_median` (**on /resource pages**), `bg_ax_nodes_per_page` (list per /resource page), `bg_pc_health_pct` (pages_AX>10 on /resource / total /resource pages), `bg_dom_nodes_median` (**on /resource pages**), `bg_dom_nodes_per_page` (per /resource page), `bg_dom_nodes_range_ok` (bool 21-82 on /resource pages)
- `browser_body_AvsC_full`, `browser_body_AvsC_body_only`, `browser_body_AvsC_status_only`, `browser_body_AvsC_headers_no_clen` + CI `[lo,hi]` `width` `degenerate` `effective_distinct_n` (via real Playwright to /resource)
- `browser_header_AvsE_full`, `browser_header_AvsE_headers_only` + CI etc (via real Playwright)
- `direct_body_AvsC_full` (sanity via direct requests through nginx), `direct_header_AvsE_full` (sanity)
- `browser_null_body_full`, `browser_null_header_full`, `browser_null_403_full`, `browser_null_401_full` + CI (via real Playwright concurrency 4)
- `browser_gradient_1B_full`, `browser_gradient_2B_full`, `browser_gradient_4B_full`, `browser_gradient_39B_full` (AvsB), `browser_gradient_86B_full` (AvsC) + per-measure CI/width/degenerate (via real browser)
- `browser_gradient_CC_small_full`, `browser_gradient_CC_large_full`, `browser_gradient_ETag_small_full`, `browser_gradient_ETag_large_full`, `browser_gradient_SC_small_full`, `browser_gradient_SC_large_full`, `browser_gradient_Vary_small_full` + CI (via real browser)
- `direct_gradient_*` same via direct fetch for comparison

All Jaccard discriminations `1 - |A∩B|/|A∪B|`, bootstrap `B=1000` for browser part; Fisher z for distributed r. Degenerate `[1.0,1.0]/[0.0,0.0]` disclosed as deterministic when set size 1 per state (effective distinct N=1).

### 5.3 Baselines

| ID | Expected distributed (real HTTP) | Expected browser (real Playwright to /resource) | Purpose |
|----|---------------------|------------------|---------|
| B-PER-NODE | TN~0.667 fail, n_non304 nominal but C1 fails (real) | — | Proves failure is replication |
| B-SHARED-STORE | TN≥0.85 pass, n_non304≥800, r TOST within 0.15 (real) | — | Primary fix |
| B-STICKY | TN≥0.85 exploratory (real ip_hash) | — | Alternative fix |
| B-STATUS-ONLY | — | 0.0 on 200 vs200 (real direct + real browser) | Status isolation |
| B-BODY-ONLY | — | 1.0 body-only, 0.0 header-only (real both) | Body signal |
| B-HEADERS-ONLY | — | 1.0 via CLEN body-only, 1.0 header-only (real both) | Body-correlated vs independent |
| B-HEADERS-NO-CLEN | — | 0.0 body-only, 1.0 header-only isolations (real both) | Independent header |

### 5.4 Sample Size

- Distributed: **N=1200 paired samples nominal via real nginx round-robin** (8 co-occurring conditions × ~120 each + 4 noise-only ×60 + 120 extra) targeting **n_non304≥800 after real 304 exclusion** (cache_enabled 50% × 33% real 304 = 16.5% overall 304 → 1002 non-304 at N=1200). Prior N=480 gave 684 non-304; scaling to 1200 with real 304 path ensures ≥800. Per-batch SELECT verification and X-Worker-Pid logged per sample.
- Browser: **N=20 per state nominal via direct through nginx + via real Playwright 1280x720 to /resource** (body 60+gradient 60+header 40+isolations 140+nulls 80+classic 80 = ~460 lines) plus sanity L 60 = ~520 raw_observations.jsonl lines with ax/dom per /resource page. Concurrency 4 for null and at least one body/header branch. Gradient per-value CI B=1000. All via real HTTP.

---

## 6. Decision Rule (Frozen — no post-hoc weakening, real HTTP required)

**SUPPORTS** (both substrates close block) iff **ALL** mandatory conditions hold with validity checks passing and **no synthetic data**:

1. **C1-FRESHNESS (distributed TN, real HTTP):** shared-store (or sticky) arm **mean TN ≥ 0.85** across 3 endpoints (session_status, profile, data_list) with each Wilson 95% lower > 0.75 and **session_status individually ≥ 0.85**, while **B-PER-NODE baseline mean TN < 0.85** (expected ~0.667, session_status 0.0) replicating failure via real HTTP — proves fix not tautological. Must be measured via real nginx round-robin with 4-concurrency, SEED 44, X-Worker-Pid distribution verified.
2. **C2-FRESHNESS (power, real 304):** **n_non304 ≥ 800** after excluding **real** 304 status (counted from `raw_freshness_observations.jsonl` where `is_304==false` via real If-None-Match/ETag, stratified across 3 endpoints, with per-batch SELECT verification). If n_non304 <800 but C1 passes, still **MEASUREMENT_INVALID** for power not falsification unless underpowered with disclosed SE.
3. **C3-FRESHNESS (orthogonality, real):** stratified pooled Pearson **r equivalence TOST within delta=0.15**: **95% Fisher z CI upper < 0.15** AND **TOST p_upper < 0.05** (and CI lower > -0.15), **pooled |r| < 0.15**, with **8/8 conditions variance std>0** for both behavioral and structural signals and **noise FP ≤ 0.15** (C4) on shared-store arm via real HTTP. `B-FLASK-ONLY |r|~0.02` trivially.
4. **C4-FRESHNESS (noise, real):** noise-only FP ≤ 0.15 (Wilson upper) on shared-store via real HTTP.
5. **C5-BROWSER-PROVISION (real Playwright to /resource):** `AgentLab 0.4.2` importable (`import agentlab` version `0.4.2` via `pip show`), `0.14.3` correctly absent (import fails or not on PyPI), `Playwright` installed with **viewport 1280×720 verified per /resource page** (`page.viewportSize().width==1280 && height==720`), **CDP AX nodes median >10 on /resource pages** and **PC-HEALTH ≥ 80% on /resource pages** (count pages with AX>10 / total /resource pages) and **DOM nodes median 21–82 on /resource pages** (each /resource page `21 ≤ dom_nodes ≤ 82`).
6. **C6-BROWSER-DISCRIMINATION (real browser fetch to /resource):** browser body-only **AvsC full > 0.5** expect `1.0` with `status 0.0` `headers-no-CLEN 0.0` and browser header-only **AvsE full > 0.5** `headers-only 1.0` `status 0.0` `body 0.0` `CLEN 31==31` via **real Playwright fetch to /resource at 1280×720** (direct sanity also `1.0` via real requests through nginx). Nulls concurrent each `full 0.0` `CI contains 0.0` `point ≤0.05` via real browser.

**Gradient reporting mandatory (exploratory not gating SUPPORTS but required for high information, real HTTP):**
- `G1_BODY_MAGNITUDE`: for each body gradient `A vs A1 1B, A vs A2 2B, A vs A3 4B, AvsB 39B, AvsC 86B` report Jaccard `full/body/headers/headers-no-CLEN` and `CI [lo,hi] width degenerate effective_distinct_n` via both direct (real) and browser (real Playwright to /resource).
- `G2_HEADER_MAGNITUDE`: for each header gradient `CC_small 3601 1s, CC_large 0, ETag_small 1char, ETag_large changed, SC_small value diff, SC_large absent->present, Vary_small Accept-Encoding vs Accept-Encoding,Origin` same reporting via both direct and browser — enables most fragile header ordering.

If any C1–C6 fails where validity checks pass and data is real HTTP → **FALSIFIED-IN-SETTING** bounded to failing branch (distributed vs browser, body vs header vs null). If shared-store and sticky both fail where per-node correctly fails via real HTTP → distributed **FALSIFIED**. If browser provision fails but distributed passes → **MIXED** (distributed SUPPORTS, browser FALSIFIED/INVALID). If C2 power fails (<800) with C1/C3 passing → **MEASUREMENT_INVALID** (underpowered) not falsification. **Any synthetic generation or relabeled direct-as-browser triggers MEASUREMENT_INVALID** per frozen falsifier, not SUPPORTS/FALSIFIED. Infrastructure-unavailable branches map to **MEASUREMENT_INVALID** not falsification: `gunicorn/nginx unavailable`, `shared store file creation fails at /tmp/spider-runtime-35860330078/shared.db`, `Playwright not installable`, `CDP capture not available on /resource pages`, `AgentLab 0.4.2 not on PyPI` (unexpected) → browser branch MEASUREMENT_INVALID while distributed can still be decided. **Paid CDN absent is NOT invalidity** per SUPERSEDE. Degenerate CI `[1.0,1.0]/[0.0,0.0]` is expected deterministic when set size 1 and not invalidity.

**Exploratory (not gating):**
- `E1_CI_NONDEGENERATE`: width 0 vs >0 per comparison under concurrency 4 (real).
- `E2_FOLDING`: case/whitespace/order folded E variant `full(folded vs canonical E) 0.0` if normalized.
- `E3_EDGE_VISIBILITY`: `X-Worker-Pid` distribution per store mode (real).
- `E4_STICKY`: sticky `ip_hash` TN and distribution skew vs shared-store (real IPs).

---

## 7. Controls Summary

| Control | ID | Type | Threshold (real HTTP) | Evidence |
|---------|----|------|-----------|----------|
| Distributed TN shared | C1-FRESHNESS | positive | `mean ≥0.85` Wilson lower >0.75 session_status ≥0.85 | TN per endpoint via real nginx round-robin shared store |
| Distributed TN per-node baseline | B-PER-NODE | negative baseline | `mean ~0.667 <0.85` session_status 0.0 (real) | Replicates prior failure via real nginx |
| Power n_non304 | C2-FRESHNESS | validity/power | `≥800` after real 304 exclusion | Count from raw_freshness real is_304==false |
| Orthogonality stratified r | C3-FRESHNESS | equivalence TOST | `CI upper <0.15` `p_upper<0.05` `|r|<0.15` 8/8 variance | Fisher z stratified real |
| Noise FP | C4-FRESHNESS | null | `≤0.15` (real) | Noise-only FP real |
| Browser provision | C5-BROWSER | positive | AgentLab 0.4.2, 0.14.3 absent, viewport 1280×720, AX>10 median **on /resource**, PC-HEALTH≥80% **on /resource**, DOM 21–82 **on /resource** | pip show, CDP per /resource page, DOM len per /resource page |
| Browser body discrimination | C6a | positive+isolation | `full>0.5` `status 0.0` `headers-no-CLEN 0.0` via **real Playwright to /resource** | Jaccard via Playwright |
| Browser header discrimination | C6b | positive+isolation | `full>0.5 headers-only 1.0` `status/body 0.0` `CLEN 31==31` via **real Playwright to /resource** | Jaccard via Playwright |
| Browser null | C6c | null | `full 0.0` CI contains 0 ≤0.05 (real) | Null Jaccard 0 real |
| Body gradient | G1 | diagnostic | report per magnitude 1B/2B/4B/39B/86B +CI via **real both** | Gradient metrics real |
| Header gradient | G2 | diagnostic | report CC_small/large ETag_small/large SC_small/large Vary +CI via **real both** | Gradient metrics real |
| Sticky exploratory | E4 | diagnostic | TN≥0.85 if ip_hash (real) | Sticky TN/distribution real |
| X-Worker-Pid distribution | validity | check | ≥10 per worker for round-robin (real) | X-Worker-Pid per observation |
| Per-batch SELECT | validity | check | ≥27 lines distinct timestamps, COMMIT verified | batch_state_log.jsonl real |
| Synthetic detection | validity | check | no np.random/hardcoded tn_correct/forced 304/simulated worker_ids | audit pattern search |

---

## 8. Validity Threats and Mitigations (real HTTP focus)

1. **Shared store file not actually shared across workers (per-node still) or synthetic:** Mitigate by creating shared file at `/tmp/spider-runtime-35860330078/shared.db` before gunicorn start, verifying both workers report same `SELECT count(*) FROM sessions` before batch via real HTTP, logging DB path per worker in provenance and per observation, checking `batch_state_log.jsonl` has ≥27 lines with distinct timestamps (not 30 identical cluster). If file not shared or synthetic pattern detected, `COMMIT_NOT_VERIFIED` / `SYNTHETIC_DATA_DETECTED` invalidity.
2. **Per-node baseline not isolating enough (still shared) or not real HTTP:** Mitigate by using distinct temp files per worker via `gunicorn --config` with env `SPIDER_DB_PATH_PER_WORKER` and verifying different file paths per worker via real X-Worker-Pid; ensure all samples are real HTTP through nginx (not direct to gunicorn bypass). Log per-node vs shared paths.
3. **n_non304 <800 due to 304 rate mis-estimation or not exercising real 304:** Mitigate by setting N=1200 (2.5× parent 480) and exercising real 304 path only when `cache_enabled` and `If-None-Match` sent to nginx; verify per request `is_304` from real status 304. If still <800, disclose SE and mark underpowered MEASUREMENT_INVALID.
4. **Structural–behavioral shared-variable confound (hash(body) includes 401 body):** Mitigate by ensuring structural signal excludes auth error bodies (only 200 bodies hashed, 401 bodies imputed constant or excluded per spec clause 8), verifying structural std>0 separately for valid/expired via real HTTP.
5. **AgentLab 0.4.2 not on PyPI / Playwright install fails / relabeled direct:** Mitigate by `pip install agentlab==0.4.2` with `--index-url`, fallback to `browsergym` package, log version; `npx playwright install chromium --with-deps` conditional; **forbid** `browser_fetch` calling `requests.get` — must be `page.request.get` or `fetch`; if fails mark MEASUREMENT_INVALID `PLAYWRIGHT_UNAVAILABLE` / `AGENTLAB_VERSION_MISMATCH` for browser branch and still decide distributed branch. Remove synthetic fallback (prior lines 903-919).
6. **CDP AX capture fails or only on index /**: Mitigate by using `cdpSession.send('Accessibility.getFullAXTree')` **per /resource page** with fallback to `page.accessibility.snapshot()`; log AX nodes per /resource page; if 0 nodes on /resource pages mark `CDP_AX_CAPTURE_FAILED` invalidity for browser health but not for distributed; ensure index-only capture is flagged as invalid (audit V4).
7. **Viewport not 1280×720 due to headless default:** Mitigate by explicitly `browser.newContext({viewport:{width:1280,height:720}})` and verifying `page.viewportSize()` per /resource page is 1280×720.
8. **Decompression CLEN mismatch (brotli/gzip) or not verified for browser:** Auto-decompress before SHA for both direct and browser; compare decompressed_body_len to body_len; log Content-Encoding per observation including browser; verify CLEN==body_len for both.
9. **Degenerate CI misread as precision or synthetic timestamp clustering:** Disclose `effective_distinct_n=1`, treat as deterministic; G1/G2 explicitly measure width under concurrency 4 with real data; check timestamp distribution is not clustered within 1-2ms (synthetic detection).
10. **Port collision / stale server / synthetic worker_ids:** Discover free ports for gunicorn/nginx, fresh DB, kill on exit; verify X-Worker-Pid values are real gunicorn pids (not simulated 16115/16116 cluster) and distribution ≥10 per worker.
11. **Paid CDN credentials absent:** Explicitly NOT gating; do not trigger MEASUREMENT_INVALID (SUPERSEDE).
12. **Relabeled direct-as-browser or synthetic harness reuse:** Audit will grep `run_experiment.py` for `np.random`, `hardcoded tn_correct`, `random 304 forced >=1000`, `browser_fetch` calling `observe_resource`/`requests`; any match with real HTTP absent triggers MEASUREMENT_INVALID per frozen falsifier.
13. **Threshold confusion (≥0.85 vs >0.5):** C1 uses ≥0.85, browser C6 uses >0.5; document exact value+CI+Wilson.

---

## 9. Consequences

**Positive (all C1–C6 pass via real HTTP + gradients reported):** Both live-substrate blocks closed without paid CDN via valid measurement. Distributed TN≥0.85 with n_non304≥800 and orthogonality preserved via real shared WAL proves shared store (or sticky) fixes replication beyond per-node 0.667; Graph can proceed to distributed C-FRESHNESS/DELTA-REPAIR on 2-node gunicorn+nginx. BrowserGym/AgentLab 0.4.2 + Playwright 1280×720 with AX>10, PC-HEALTH≥80%, DOM 21–82 on /resource pages via real browser fetches provisions a live browser observation substrate where HTTP fingerprint discrimination remains non-degenerate in disclosure (per-value CC/ETag/CLEN gradients with B=1000 CIs) beyond degenerate loopback ceiling. Unblocks Intel Gate0 harvest (BrowserGym provision + shared session store) and Physics live replication (AX DOM capture) and enables sensitivity ordering for freshness policy calibration. Claim ceiling expands from single-host loopback EXPERIMENTAL to **distributed shared-store + live browser EXPERIMENTAL (real HTTP)**; does NOT promote to VALIDATED or PRODUCT_CORE (still bounded to single-host 2-worker simulation, filtered header set, body 31–117B, AgentLab 0.4.2, single viewport, no paid CDN, no multi-host Redis).

**Negative (any C1–C6 fails where validity passes via real HTTP):** Either distributed shared-store/sticky fails to restore TN≥0.85/n≥800/orthogonality, or BrowserGym provision/discrimination fails via valid measurement. Proves per-node failure not fixable by trivial shared file/ip_hash or browser layer not viable; loopback emulation does not predict distributed/browser behavior. Bounds C-MEAS-VALID and C-FRESHNESS to single-host loopback EXPERIMENTAL only, prevents false VALIDATED promotion, forces redesign (true Redis/multi-host or alternative DOM observation) before scaling. Negative still requires gradient reporting to diagnose most fragile magnitude.

**MEASUREMENT_INVALID (synthetic or relabeled or provision failure):** Prior packet's synthetic harness and relabeled direct requests map here. No ceiling change; requires rerun with real HTTP per this prereg. Distinguishes measurement failure from scientific falsification; audit will flag `SYNTHETIC_DATA_DETECTED` or `BROWSER_FETCH_RELABELED`.

Both valid outcomes are high-information and will be consumed by Codex as the distributed+browser promotion decision required before any VALIDATED or PRODUCT_CORE claim.

---

## 10. What is NOT Tested (Scope Boundaries)

- **Paid CDN HIT/STALE/SWR/SIE/304 beyond nginx loopback** — explicitly SUPERSEDED per Director, not tested (no credentials, 0% HIT prior, zero VOI).
- Multi-host **Redis cluster** or SQLite multi-node replication beyond single-host 2-worker WAL shared file at `/tmp/spider-runtime-35860330078/shared.db` / ip_hash sticky — single-host shared file tested; true distributed multi-host remains unresolved unless Redis available.
- **TLS/HTTP2/QUIC** beyond plain HTTP 127.0.0.1 termination.
- Browser **DOM/AX beyond HTTP triple** (rendered text hash, accessibility tree beyond node counts, visual layout, computed style) — AX/DOM node counts per /resource page only.
- Body sizes beyond **31–117B JSON with sort_keys=True** — CLEN==body_len holds for these bodies.
- End-to-end **cost/latency/tokens/LLM inheritance/cross-site holdout** — not measured (runtime substrate only).
- Full **304 lifecycle beyond single HIT** (`STALE/SWR`) best-effort via `Age`/`ETag` on origin.

---

## 11. Execution Checklist for EXECUTE

- [ ] Implement `run_experiment.py` with fingerprint functions byte-identical to `research/experiments/EXP-RUNTIME-35764329925/run_experiment.py:compute_fingerprint` (status_only, body_only, headers_only, headers_no_clen), sorted lowercased filtered headers, EXCLUDED {Date,Server,X-Request-Id,CF-RAY,CF-Cache-Status,X-Cache,Age} plus X-Worker-Pid, decompression via `response.content` auto-decompressed for direct and via `page.request` body for browser; ensure audit recomputation 0 mismatches and **no synthetic generation code**.
- [ ] Implement distributed harness with **real HTTP only**: reuse research/harness C-FRESHNESS logic (behavioral graded session_status_check, structural hash, paired samples, real If-None-Match 304) with DB modes B-PER-NODE (isolated files) vs B-SHARED-STORE (shared file at /tmp/spider-runtime-35860330078/shared.db WAL) vs B-STICKY (nginx ip_hash). Seed 44, jitter 50-150ms, N=1200 nominal via **real nginx round-robin**. Prior synthetic lines 453-664 must be deleted.
- [ ] Extend Flask app with `body_config/header_config` tables, `/api/profile|/data_list|/session/status` endpoints with `Cache-Control public max-age=5` / `no-store` and `ETag-SHA256`, `X-Worker-Pid` header, admin routes with COMMIT+SELECT verification per batch.
- [ ] Launch topology D: write per-run `nginx.conf` to `/tmp/spider-runtime-35860330078/nginx/` start `gunicorn --workers 2 --bind 127.0.0.1:19860 app:app` and `nginx -c <conf> -p /tmp/...` `127.0.0.1:19851`; verify health via real curl and `X-Worker-Pid` distribution ≥10 per worker. Run B-PER-NODE baseline first via real HTTP to replicate TN~0.667, then B-SHARED-STORE primary (and B-STICKY exploratory) with round-robin verified via real requests.
- [ ] Execute distributed primary: **1200 paired samples via real nginx round-robin** with 4-concurrency bursts, log `raw_freshness_observations.jsonl` (~1200 lines, real timestamps, real X-Worker-Pid) + `batch_state_log.jsonl` (>=27 lines distinct timestamps + warmup), compute TN per endpoint (Wilson), n_non304 via real is_304, stratified r Fisher z CI and TOST, variance, FP. Verify no synthetic timestamp clustering.
- [ ] Provision browser substrate: `pip install agentlab==0.4.2` (verify `0.14.3` absent, not error), `pip install playwright`, `npx playwright install chromium --with-deps` if needed, verify `AgentLab 0.4.2` importable and `playwright --version`.
- [ ] Launch browser contexts at **1280x720**, create CDP session **per /resource page**, capture `Accessibility.getFullAXTree` (AX nodes count) and `document.querySelectorAll('*').length` (DOM nodes) **per /resource page** (not only index), log viewport, AX>10, PC-HEALTH, DOM 21-82. Run browser body-only/header-only/gradient/null/classic batches via **real Playwright fetch to /resource** (page.request.get with decompressed body, filtered headers, fingerprint triple) N=20 per state + direct sanity via real requests through nginx. **Delete prior relabel logic (lines 809-845)** and synthetic fallback (903-919).
- [ ] Produce `raw_observations.jsonl` (~520 lines: ~260 direct via gunicorn+nginx + ~260 browser via real Playwright 1280x720 to /resource) with fields `state,status,body_sha256,body_len,content_length_header,content_encoding,headers_filtered_json,headers_raw_json,headers_no_clen_json,fingerprint_*,worker_id,ax_nodes,dom_nodes,viewport,fetch_method,cdn_cache_status,timestamp,concurrency` where ax_nodes/dom_nodes are per /resource page and fetch_method distinguishes direct vs browser.
- [ ] Metrics stable names: `freshness_c1_tn_mean`, `freshness_n_non304`, `freshness_stratified_r`, `freshness_tost_p_upper`, `bg_ax_nodes_median`, `bg_pc_health_pct`, `browser_body_AvsC_full`, `browser_gradient_1B_full`, etc plus CI width degenerate effective_distinct_n; controls stable `C1-FRESHNESS..C6-BROWSER G1 G2 E1-E4` with pass/fail and evidence_refs. All via real HTTP.
- [ ] Record `provenance.json` with `github_run_id 35860330078 base_sha 00da54cecc6ed5fb0db8969a42b72066cc4af993` env (Flask 3.1.3 PyJWT 2.14.0 SQLite 3.45.1 WAL Werkzeug 3.1.8 gunicorn 23.0.0 nginx 1.24.0 AgentLab 0.4.2 Playwright CDP versions, ports, SEED 44, EXCLUDED, body SHAs/lengths, header constants, artifact SHA-256, git commit, DB paths `/tmp/spider-runtime-35860330078/shared.db` vs per-node).
- [ ] Must not inspect outcomes before freeze; frozen `spec.json`/`prereg.md`/`freeze.json` immutable after freeze; any deviation after seeing data is exploratory and labeled. **Remove all synthetic harness and relabel code before freeze**.
- [ ] Preserve stable control/metric identities for `AUDIT`/`DIRECTOR` transmission per `research/EXPERIMENT_PACKET.md §1`; keep Jaccard discrimination identical to parent for comparability; report effective distinct N and degenerate flag per metrics; ensure `batch_state_log.jsonl` has distinct timestamps and `raw_freshness_*.jsonl` not clustered.
- [ ] Handle unavailable substrates gracefully: if shared store file creation fails mark `MEASUREMENT_INVALID SQLITE_SHARED_STORE_UNAVAILABLE` for distributed branch with diagnostic; if Playwright/AgentLab not installable mark `MEASUREMENT_INVALID PLAYWRIGHT_UNAVAILABLE` for browser branch and still decide distributed branch (MIXED), and vice versa; paid CDN absent NOT gating. **Synthetic fallback is forbidden** — provision failure must be reported as MEASUREMENT_INVALID not masked with synthetic 1.0.

