# EXP-RUNTIME-35774047385 — Preregistration

**Experiment ID:** EXP-RUNTIME-35774047385  
**Lane:** Runtime  
**Claim:** C-MEAS-VALID (Measurement substrate is intervention-valid)  
**Director Mandate:** CONTINUE — Does SHA256(status||body_bytes||sorted_filtered_headers) retain discriminating same-status body-only (body-only 1.0 >0.5, status 0.0, headers-no-CLEN 0.0/1.0, Content-Length 31/70/117 varies) and header-only (full 1.0 > body/status 0.0, headers-only 1.0) with null FP<0.05 and writable permission/session >=0.7 when moved from single-host gunicorn23+nginx loopback to paid-tier CDN (Cloudflare/Fastly HIT/STALE/SWR/SIE/304, Vary/ETag, chunked buffering) and BrowserGym/AgentLab 1280x720 DOM/AX observation layer under 4-client concurrency, reporting per-value magnitude gradients and non-degenerate bootstrap CIs to enable sensitivity ordering beyond the 1.0 ceiling?  
**Parent Handoff:** research/experiments/EXP-RUNTIME-35764329925/handoff.json (sha256:eeacde3308a7d346dc8d133066ac5c056c6aa9062169c6547395bacd028c6577) — **disposition USE** per request.json director_mandate.parent_handoff_disposition. Inherited continuity evidence preserved four-way but does NOT override Director binding question; cognitive_reset true per Director rationale.  
**Date:** 2026-09-22
**Dependencies:** EXP-RUNTIME-35764329925 (gunicorn+nginx loopback PASS), EXP-RUNTIME-35611612543 (nginx decompression 960/960), EXP-INTEL-35766523457

---

## 1. Question

Does the identical HTTP fingerprint substrate — `SHA256(status || body_bytes || sorted_filtered_standard_headers)` with `EXCLUDED_HEADERS={Date,Server,X-Request-Id}` plus disclosed `X-Worker-Pid/CF-RAY/CF-Cache-Status/X-Cache` edge exclusions — retain its discriminating same-status **body-only** and **header-only** behavior with null stability `FP<0.05` and writable permission/session `>=0.7` when moved from single-host `gunicorn 23.0.0 2x sync + nginx 1.24.0 127.0.0.1` loopback to (a) a **paid-tier CDN edge** (`Cloudflare/Fastly` fronting same origin via `HIT/STALE/SWR/SIE/304`, `Vary/ETag` revalidation, chunked/brotli buffering, header folding across PoPs) and (b) a **BrowserGym/AgentLab 1280×720** Playwright HTTP/DOM observation layer, under **4-client concurrency**, with **per-value magnitude gradients** and **non-degenerate bootstrap CIs** reported to enable sensitivity ordering beyond the prior `1.0` ceiling?

This is the binding Director question for this governed NEW experiment. The parent `next_question` is preserved as continuity evidence (identical question) and per `USE` the Director's target claim `C-MEAS-VALID`, comparative reasoning (vs Redis hardening and vs further localhost payload scaling) and portfolio assessment govern design. This design **does not repeat** another localhost or single-host loopback body/header magnitude variant at `1.0` ceiling — all prior `31/70/117` and 3 header isolations already at ceiling with degenerate CI `width 0`.

---

## 2. Hypothesis

The fingerprint algorithm `hash(status_code || decompressed_body_bytes || sorted_filtered_standard_headers)` with `EXCLUDED_HEADERS={Date,Server,X-Request-Id,CF-RAY,CF-Cache-Status,X-Cache}` (lowercased sorted keys, `sort_keys=True` separators `(',',':')`, bodies decompressed after CDN brotli/gzip) identical to `research/experiments/EXP-RUNTIME-35764329925/run_experiment.py:compute_fingerprint` will on **paid CDN substrate** `Flask 3.1.3 + PyJWT 2.14.0 HS256 + SQLite WAL — origin gunicorn 2x sync 127.0.0.1:19860 -> nginx 127.0.0.1:19851 -> Cloudflare/Fastly edge domain (HIT enabled, BYPASS for admin routes, Vary/ETag revalidation, brotli/gzip, chunked buffering)**:

- **(H1) Body-only retained via edge:** `full(A vs C, 31B vs 117B SHA d0ca833f vs b46c461c both 200)` `1.0 >0.5` with `body-only 1.0` on `AvsC` and `AvsB (70B 67c186f)` `status 0.0` `full>status` strictly `headers-no-CLEN 0.0` `CLEN 31/70/117` varies `==decompressed_body_len` non-CLEN headers identical, null body-A `0.0` `CI contains 0.0 <=0.05`.
- **(H2) Header-only retained via edge:** `full(A vs E, bodies 31B identical CLEN 31 identical) 1.0 >0.5` `headers-only 1.0` `status 0.0` `body 0.0` `headers-no-CLEN 1.0` on combined `E` and each isolated header `CC/ETag/SC` (including small magnitudes `CC max-age 3601 1s diff`, `ETag 1char diff W/"fixed-aaa-112"`, `SC session=abc` value diff, `Vary Accept-Encoding,Origin` vs `Accept-Encoding`) each `full 1.0 headers-only 1.0 status 0.0 body 0.0` after decompression.
- **(H3) Writable permission/session `>=0.7` via edge:** classic `403 vs 200` (`UPDATE users SET role`, `CF-Cache-Status BYPASS/DYNAMIC`) and `401 vs 200` (`DELETE sessions`) each `full >=0.7` expected `1.0` with respective null `0.0` and cross-worker/edge-bypass commit visible (`X-Worker-Pid` distribution `>=10` per worker, `CF-Cache-Status` logged).
- **(H4) BrowserGym/AgentLab retained (conditional):** same `AvsC` and `AvsE` comparands via `BrowserGym AgentLab 1280x720 Playwright fetch` through HTTP/DOM layer capture same triple and achieve same isolation (`body-only 1.0 status 0.0` and `header-only 1.0 body 0.0`) when Docker image `am1n3e/webarena-verified-shopping` or `AgentLab` available; else `E4 NOT_TESTED IMAGE_UNAVAILABLE` not gating.
- **(H5) Gradient diagnostic measured:** per-value body sweep `1B/2B/4B/39B/86B` (`A vs A1 32B`, `A vs A2 33B`, `A vs A3 35B`, `AvsB`, `AvsC`) and header sweep `CC_small/large ETag_small/large SC_small/large Vary_small` each measured with `full/body/headers/headers-no-CLEN` Jaccard and `95%` bootstrap `B=1000` CI `width` and `degenerate` flag; if CDN preserves bytes/headers exactly all remain `1.0` degenerate `width 0` (declared deterministic); if CDN normalizes small deltas or header folding (lowercase/order/whitespace/multi-Set-Cookie coalescing) then smallest magnitudes show `<1.0` with `width>0` enabling ordering `body vs header` sensitivity for freshness calibration.

If `H1-H3` hold via CDN with validity checks passing, `localhost->CDN` promotion gap is closed. If any fails where validity passes, CDN generalization falsified bounded to edge.

---

## 3. Inherited State — What is Established, Rejected, Unknown (from parent handoff, preserved four-way, disposition USE)

From `EXP-RUNTIME-35764329925/handoff.json` (audit PASS) and dependencies — established ceilings are audit PASS but explicitly bounded to single-host loopback (or localhost) `EXPERIMENTAL` not `VALIDATED/PRODUCT_CORE`. This experiment does **not** assume they generalize; it tests whether they do on CDN/BrowserGym.

**Established (bounded, audit PASS, narrowed ceiling — loopback EXPERIMENTAL):**

- HTTP fingerprint `SHA256(status||body_bytes||sorted_filtered_headers)` with `EXCLUDED {Date,Server,X-Request-Id}` plus `X-Worker-Pid` deterministically discriminates same-status body-only `full AvsC 1.0 >0.5 body-only 1.0 AvsB 1.0 status 0.0 headers-no-CLEN 0.0` with `CLEN 31/70/117 ==body_len` and header-only `full AvsE 1.0 >0.5 headers-only 1.0 status 0.0 body 0.0 CLEN 31 identical headers-no-CLEN 1.0` on **gunicorn 23.0.0 2x sync 127.0.0.1:19860 + nginx 1.24.0 127.0.0.1:19851 loopback** with 4-client concurrency and SQLite WAL cross-worker visibility (all 10 mandatory C1-C10 PASS deterministic, `CF` loopback) — `EXP-RUNTIME-35764329925`.
- Per-header isolations each alone sufficient via loopback: `Cache-Control alone 1.0 ETag alone 1.0 Set-Cookie alone 1.0` on full/headers-only; null `0.0 CI[0,0]` folding `0.0`.
- Null stability holds under 4-client concurrency via nginx->gunicorn: `0.0` with `CI[0,0]` and writable permission/session `1.0 >=0.7` visible cross-worker `21/19` distribution — same loopback stack.
- Localhost `Werkzeug` sanity replication still holds `AvsC 1.0 AvsE 1.0` confirming origin variable only; combined localhost+loopback matrix complete but still degenerate CI `width 0 effective N=1`.
- Claim ceiling expanded from localhost `Werkzeug` `EXPERIMENTAL` to production-like single-host loopback `EXPERIMENTAL` not `VALIDATED/PRODUCT_CORE` per audit `V7`; `tunnel_flag true` after 43 consecutive `C-MEAS-VALID`; all tested `31/70/117` and 3 isolations at ceiling `1.0` degenerate no gradient.
- Nginx `HIT/SWR/SIE/304` decompression `960/960` byte-identical on single-host nginx (no paid CDN) — `EXP-RUNTIME-35611612543`.

**Rejected (bounded):**

- Same-status body-only drift undetectable on production-like gunicorn+nginx or via CLEN alone — falsified bounded to loopback: `full 1.0 body 1.0 status 0.0 headers-no-CLEN 0.0`.
- Header-only drift undetectable on gunicorn+nginx or via CLEN alone — falsified bounded: `full 1.0 headers-only 1.0 body 0.0 status 0.0` with `CLEN 31` identical and `headers-no-CLEN 1.0`.
- Full-vector adds no marginal value beyond status/body baselines on isolated branches — falsified where `full 1.0 > status 0.0`; remains vacuous only where both vary.
- Null `FP<0.05` fails under concurrency or header folding breaks isolation — falsified bounded: four concurrent nulls `0.0` folding `0.0`.
- Gunicorn worker isolation prevents cross-worker visibility — falsified bounded to single-host WAL `2-worker`.

**Unknown (this experiment directly targets the first three — per Director binding question):**

- Does discrimination survive **paid-tier CDN** (`Cloudflare/Fastly HIT/STALE/SWR/SIE/304`, edge `Vary/ETag` revalidation, chunked buffering across PoPs, multiple `Set-Cookie` coalescing) beyond `nginx 127.0.0.1` loopback emulation — explicitly `NOT_TESTED`.
- Does discrimination survive **BrowserGym/AgentLab 1280x720** `Playwright fetch` through HTTP/DOM layer — `E4 NOT_TESTED IMAGE_UNAVAILABLE` in parent.
- What is **per-value magnitude gradient / sensitivity ordering** when body sizes/fields or header values vary with smaller magnitudes where discrimination falls below `1.0` and CIs become non-degenerate — all tested magnitudes hit ceiling `1.0`.
- Does `Vary` alone discriminate when isolated vs combined `E`, does TLS/HTTP2/QUIC or distributed Redis multi-host preserve discrimination, does header folding beyond sorted lowercased normalization affect discrimination — unresolved.

**Do not assume (explicitly unsafe):**

- `C-MEAS-VALID` is `VALIDATED` or `PRODUCT_CORE` — audit PASS supports `EXPERIMENTAL` only; degenerate CI is deterministic not high-precision; `promote_to_product false`.
- Loopback gunicorn+nginx results generalize to real CDN, TLS/HTTP2, multi-host Redis, or BrowserGym DOM — explicitly `NOT_TESTED` per audit `V7`.
- Full-vector always adds marginal value — true only on isolated `200 vs 200` branches.
- `Content-Length 31/70/117` proves arbitrary body sizes discriminate — tested only 3 specific bodies with `sort_keys=True`.
- Per-header isolations at `1.0` characterize sensitivity ordering — no gradient measured.
- Bootstrap degenerate CIs imply statistical precision — width `0` reflects byte-identical fingerprints per state `effective N=1`.
- `C-FRESHNESS/C-DELTA-REPAIR` now unblocked for production distributed testing — unblocked only for single-host loopback; CDN/multi-host remains blocked.

This `CONTINUE` does not repeat loopback value-magnitude variants. It tests the **paid-CDN/BrowserGym orthogonal promotion** plus **gradient non-degeneracy**.

---

## 4. Server Design

### 4.1 Testbed Architecture (three topologies, same Flask app)

```
Flask 3.1.3 + PyJWT 2.14.0 HS256 + SQLite WAL (WAL mode, file per run)
  ├── POST /admin/set_body_variant   (admin JWT, writes body_config/content_variant, SQLite COMMIT, CF-Cache-Status BYPASS)
  ├── POST /admin/set_headers        (admin JWT, writes header_config, COMMIT, BYPASS)
  ├── POST /admin/set_role           (UPDATE users SET role, BYPASS)
  ├── POST /admin/invalidate_session (DELETE sessions, BYPASS)
  ├── GET  /resource                 (authenticated GET, status+JSON body+filtered headers, Cache-Control public max-age=60 for HIT vs private for BYPASS)
  └── GET  /protected                (smoke)

Topology L (sanity):             Werkzeug dev 127.0.0.1:<free>  (single client sequential, N=20) — validity gate
Topology P_CDN (primary):        origin gunicorn 23.0.0 2x sync --workers 2 --bind 127.0.0.1:19860 --timeout 30 + nginx 1.24.0 127.0.0.1:19851 (proxy_pass http://gunicorn, proxy_http_version 1.1, proxy_set_header Connection "") fronted by paid CDN edge domain (e.g., spider-runtime-xxxx.paid-cdn.example / Cloudflare) with cache rule /resource max-age=60, Vary Accept-Encoding, ETag revalidation, brotli/gzip on, chunked buffering; purge via API before run, health via curl with CF-Cache-Status header logged; observations via edge HTTPS URL with decompression (requests auto-decompress)
Topology P_BG (conditional):     Same origin accessed via AgentLab/BrowserGym 1280x720 Playwright (page.request / fetch inside browser context) capturing HTTP triple via browser response events, N=20 per state if image available
```

`body_config` table `variant TEXT PRIMARY KEY, body_json TEXT`; initialized `A {"data":"hello","version":1}` 31B. `header_config` table `key TEXT PRIMARY KEY, value TEXT`; fixed `Cache-Control:max-age=3600, ETag:W/"fixed-aaa-111", Vary:Accept-Encoding, Content-Type:application/json`. All `GET /resource` for body-only use same valid JWT; body variation via `body_config`, status `200`. For header-only, `header_config` varied; bodies held `31B`.

**CDN setup:** Requires `CF_API_TOKEN` or `FASTLY_API_KEY` and test domain (env `SPIDER_CDN_DOMAIN`). Script `setup_cdn.sh` provisions DNS -> origin IP, sets cache rule `Cache Rule: /resource Edge TTL 60, Browser TTL 60, Vary Accept-Encoding, Respect ETag`, enables `Brotli`, `Tiered Cache off` for determinism, and `BYPASS` for `/admin/*` via `Cache-Control: no-store`. Purge cache before each batch `curl -X POST /purge`. Log `CF-Cache-Status`/`X-Cache` per observation. If credentials absent, record `MEASUREMENT_INVALID CDN_UNAVAILABLE` with diagnostic and preserve `L` sanity.

**BrowserGym setup:** `docker image inspect am1n3e/webarena-verified-shopping` or `ghcr.io/servicenow/BrowserGym` then `playwright` fetch; if fails mark `NOT_TESTED`.

### 4.2 Body and Header States (identical magnitudes plus gradients for comparability)

| State | Body JSON (sort_keys=True) | body_len decomp | Body SHA-256 (decompressed) | Status | Filtered Headers (non-CLEN) |
|-------|----------------------------|-----------------|------------------------------|--------|------------------------------|
| **A baseline** | `{"data":"hello","version":1}` | 31 | `d0ca833f...` | 200 | `Cache-Control:max-age=3600, ETag:W/"fixed-aaa-111", Vary:Accept-Encoding, Content-Type:application/json, CLEN 31, Connection:keep-alive` constant for body-only |
| **A1 grad 1B** | `{"data":"hello!","version":1}` | 32 | distinct | 200 | identical to A |
| **A2 grad 2B** | `{"data":"hello!!","version":1}` | 33 | distinct | 200 | identical to A |
| **A3 grad 4B** | `{"data":"hello!!!!","version":1}` | 35 | distinct | 200 | identical |
| **B reader** | `{"data":"hello","items":["a","b"],"role":"reader","version":1}` | 70 | `67c186f...` distinct | 200 | identical to A |
| **C admin** | `{"admin_note":"sensitive:42","count":42,"data":"hello","items":["a","b","c"],"role":"admin","version":1}` | 117 | `b46c461c...` distinct | 200 | identical to A |
| **E combined** | `{"data":"hello","version":1}` 31B | 31 | same as A | 200 | `Cache-Control:max-age=0,must-revalidate, ETag:W/"changed-bbb-222", Set-Cookie:session=xyz; Path=/; HttpOnly, Vary:Accept-Encoding,Origin, CLEN 31` |
| **Isolations grad** | same 31B | 31 | same as A | 200 | CC_small `max-age=3601` vs CC_large `max-age=0` ; ETag_small `W/"fixed-aaa-112"` 1char vs ETag_large `changed`; SC_small `session=abc` value diff vs SC_large absent->present; Vary_small `Accept-Encoding` vs `Accept-Encoding,Origin` |
| **P_403** | `{"error":"forbidden"}` | 22 | `387fe7...` | 403 | via CDN BYPASS |
| **S_401** | `{"error":"unauthorized"}` | 25 | `9df36...` | 401 | via CDN BYPASS |

Gradient bodies decompressed SHA must be distinct; CDN must not re-serialize JSON.

---

## 5. Measurement

### 5.1 Observation Vector (per request via CDN/BG decompressed)

- HTTP status `int`, decompressed body exact bytes + `SHA-256` + `decompressed body_len` + `Content-Length` header value `str` (must `== decompressed body_len` or `Transfer-Encoding: chunked` reassembled)
- Raw headers dict + filtered headers dict (minus `EXCLUDED`) + `headers_no_clen` dict (filtered minus `Content-Length`)
- Fingerprints: `full = SHA256(status || decompressed_body_bytes || sorted_filtered_headers_json)`, `status_only`, `body_only`, `headers_only`, `headers_no_clen` — identical functions
- `worker_id` (`X-Worker-Pid` or `CF-RAY` POP), `cdn_cache_status` (`CF-Cache-Status`/`X-Cache`/`Age`), `ETag`/`Vary` raw, `timestamp`, `concurrency` flag

### 5.2 Discrimination Metric

Jaccard distance between fingerprint sets:

```
discrimination = 1.0 - |set_A ∩ set_B| / |set_A ∪ set_B|
```

Sets built from `N=20` fingerprints per state per topology `P_CDN`/`P_BG`. Deterministic set size `1` => `1.0` if any bit differs else `0.0`. Bootstrap `95%` CI `B=1000` resampling; degenerate `[1.0,1.0]/[0.0,0.0]` declared deterministic when set size `1` per state, not precision. `width = hi-lo` reported per magnitude; `degenerate` flag `true` iff `width==0` and `set sizes 1`. Thresholds per Director: `>0.5` body/header positive, `=0.0` status isolation on `200 vs 200`, `>=0.7` classic, `<=0.05` null `FP`.

### 5.3 Baselines

| ID | Source | Expected body-only AvsC 31 vs117 via CDN/BG | Expected header-only AvsE 31 identical via CDN/BG | Purpose |
|----|--------|----------------------------------------------|---------------------------------------------------|---------|
| B-STATUS-ONLY | status only | 0.0 | 0.0 | Strong null: status not signal when held constant |
| B-BODY-ONLY | body SHA only | >0.5 expect 1.0 for all body magnitudes if CDN preserves bytes | 0.0 | Body carries signal when status constant |
| B-HEADERS-ONLY | filtered headers incl CLEN | 1.0 via CLEN only (body-correlated) | 1.0 via CC/ETag/SC/Vary | Body-correlated vs independent header |
| B-HEADERS-NO-CLEN | filtered headers minus CLEN | 0.0 (no independent drift) | 1.0 for combined and small/large isolations | Isolation of independent header signal for gradient ordering |

`B-HEADERS-ONLY 1.0` via CLEN and `B-BODY-ONLY 0.0` on header-only are expected complements.

### 5.4 Sample Size

- Per `P_CDN` primary: body-only `A×20 B×20 C×20 =60` + gradients `A1×20 A2×20 A3×20 =60`; header-only `A×20 E×20 =40` + isolations `CC_small 20 CC_large 20 ETag_small 20 ETag_large 20 SC_small 20 SC_large 20 Vary_small 20 =140`; body null `N1-body A1×20 A2×20 =40` concurrent + header null `A1×20 A2×20 =40` concurrent + classic `P_403 403×20 vs 200×20 =40` `S_401 401×20 vs 200×20 =40` plus nulls `403×20 vs 403×20 401×20 vs 401×20 =40` ; sequential baselines body+header `60+40` ; folding variant `20`; total nominal `~520` lines `P_CDN` (±20). Plus sanity `L` `AvsC AvsE + null` `60` lines. Plus `P_BG` same `AvsC AvsB AvsE isolations null classic` `~80` lines if available.
- `Jitter 50-150ms` uniform between bursts, `SEED 44`, `N=20` per state, effective distinct fingerprints expected `~15` distinct states with degenerate CI disclosure required.

---

## 6. Decision Rule (Frozen — no post-hoc weakening)

**SUPPORTS** (CDN+gradient generalization) iff **ALL** mandatory `C1–C10` hold on paid `CDN` substrate `P_CDN` (edge HTTPS, decompressed, `N=20` per state, concurrency 4 for null and at least one body/header branch, fingerprint identical, `EXCLUDED` as above) **and** sanity `L` passes (`L AvsC 1.0 L AvsE 1.0` else `SYSTEM_BROKEN`):

1. **C1_CDN_FULL_BODY_DRIFT:** `full(A vs C) >0.5` expect `1.0` with `200` on all 40 via `P_CDN` decompressed, body SHA distinct `d0ca833f vs b46c461c`, `CLEN 31 vs117 ==body_len`, non-CLEN identical.
2. **C2_CDN_BODY_ONLY_SIGNAL:** `body-only(A vs C) >0.5` `1.0` and `body-only(A vs B) >0.5` `1.0`; `headers-no-CLEN(A vs C) 0.0` and `headers-no-CLEN(A vs B) 0.0`; `headers-only` may be `1.0` via CLEN (documented).
3. **C3_CDN_STATUS_ISOLATED:** `status-only 0.0` on `AvsC` and `AvsB` via `P_CDN`.
4. **C4_CDN_FULL_EXCEEDS_STATUS_NONVACUOUS:** `full(A vs C) > status-only(A vs C)` strictly `1.0>0.0`.
5. **C5_CDN_NULL_NO_FP:** CDN nulls `N1-body` (body `A` resampled concurrent), `N1-header` (`A` resampled), `403` same-state, `401` same-state each `full 0.0` `CI contains 0.0` `point <=0.05` and `status/body/headers/headers-no-CLEN 0.0`.
6. **C6_CDN_CLEN_VARIES:** `CLEN` differs `31 !=70 !=117` `==body_len` SHA distinct, non-CLEN identical across `A/B/C` via `P_CDN` decompressed (gradient `32/33/35` also `==body_len` and SHA distinct).
7. **C7_CDN_WRITABLE_PERMISSION:** permission `full >=0.7` — (a) reader vs admin body `AvsC` `>=0.7` (auto if `C1 1.0`) and (b) classic `403 vs 200` via `UPDATE users SET role` on `P_CDN` BYPASS with cross-worker/edge visibility `>=10` per worker, `full >=0.7` expect `1.0` body SHA distinct `22B 387fe7` null `0.0`.
8. **C8_CDN_WRITABLE_SESSION:** session `401 vs 200` via `DELETE sessions` on `P_CDN` BYPASS `full >=0.7` expect `1.0` `401 25B 9df36` null `0.0`.
9. **C9_CDN_HEADER_ONLY:** header `full(A vs E) >0.5` `1.0` and `headers-only(A vs E) >0.5` `1.0` via `P_CDN` decompressed with `status 0.0 body 0.0`; plus per-isolation `CC_small CC_large ETag_small ETag_large SC_small SC_large Vary_small` each `full 1.0 headers-only 1.0 status 0.0 body 0.0`.
10. **C10_CDN_CLEN_IDENTITY_HEADER_ONLY:** `CLEN identical 31==31` and body SHA identical across header-only `AvsE` and each isolation via `P_CDN` decompressed.

**Gradient reporting mandatory (exploratory not gating `SUPPORTS` but required for high information and sensitivity ordering):**
- `G1_BODY_MAGNITUDE`: for each body gradient `A vs A1 (1B) A vs A2 (2B) A vs A3 (4B) AvsB (39B) AvsC (86B)` report Jaccard `full/body/headers/headers-no-CLEN` and `CI [lo,hi] width degenerate` — enables smallest detectable body delta via CDN.
- `G2_HEADER_MAGNITUDE`: for each header gradient `CC_small/large ETag_small/large SC_small/large Vary_small` report same — enables most fragile header ordering (which small magnitude still `1.0` vs collapses to `0.0` if CDN normalizes).

If any `C1-C10` fails where validity checks pass → **FALSIFIED-IN-SETTING** bounded to that substrate/branch (body-only vs header-only vs null vs writable vs CLEN). If `P_CDN` credentials/domain unavailable, edge config push fails, or rate-limited with exhausted retry → **MEASUREMENT_INVALID** (`CDN_UNAVAILABLE`/`RATE_LIMITED` etc) not falsification; preserve `L` sanity diagnostics. BrowserGym image unavailable → `P_BG E4 NOT_TESTED` not gating CDN verdict. Degenerate CI `[1.0,1.0]/[0.0,0.0]` is expected deterministic when set size `1` and not invalidity; `width>0` reported as non-degenerate where CDN exposes variance (HIT vs MISS, brotli).

**Exploratory (not gating):**

- `E1_CI_NONDEGENERATE`: width `0` vs `>0` per comparison under concurrency `4` via `P_CDN`; diagnostic of edge variance.
- `E2_FOLDING`: case/whitespace/order folded `E` variant `full(folded vs canonical E) 0.0` if normalized else `>0`.
- `E3_EDGE_VISIBILITY`: `CF-Cache-Status distribution HIT/BYPASS/DYNAMIC` and `X-Worker-Pid` distribution; `<500ms` visibility not separately gating.
- `E4_BROWSERGYM`: same `AvsC/AvsE` via `1280x720` browser layer `>0.5` if image available else `NOT_TESTED`.

---

## 7. Controls Summary

| Control | ID | Type | Threshold | Evidence |
|---------|----|------|-----------|----------|
| Full body drift CDN | C1_CDN | positive | `>0.5` expect `1.0` | `AvsC` full Jaccard via CDN edge decompressed `200 vs200` SHA≠ CLEN≠ |
| Body-only signal CDN | C2_CDN | positive+isolation | `body-only >0.5` on `AvsC+AvsB`; `headers-no-CLEN 0.0` | body-only + headers-no-CLEN Jaccard |
| Status isolated CDN | C3_CDN | strong null | `=0.0` on `AvsC AvsB` | status-only `0` |
| Full > status CDN | C4_CDN | non-vacuous superiority | strictly `>` `1.0>0.0` | full vs status-only on `AvsC` |
| Null stability CDN | C5_CDN | null | `=0.0` CI contains `0` `<=0.05` on 4 nulls concurrent | null Jaccard `0` `CI[0,0]` |
| CLEN varies headers constant CDN | C6_CDN | validity | `CLEN ≠` `==body_len` SHA≠ non-CLEN `=` | header values body_len SHA via CDN |
| Permission writable CDN | C7_CDN | positive `>=0.7`+null | `full >=0.7` `403vs200` `AvsC` + null `0.0` workers `>=10` | Jaccard SELECT `CF-Cache-Status BYPASS` |
| Session writable CDN | C8_CDN | positive `>=0.7`+null | `full >=0.7` `401vs200` + null `0.0` | Jaccard SELECT BYPASS |
| Header-only CDN | C9_CDN | positive+isolation | `full>0.5 headers-only>0.5` on `AvsE` + each small/large isolation `1.0` `status/body 0.0` | header Jaccard isolations via CDN |
| CLEN identity header-only CDN | C10_CDN | validity | `CLEN =` `31==31` SHA `=` | `CLEN 31==31` |
| Body gradient | G1 | diagnostic | report per magnitude `1B/2B/4B/39B/86B` Jaccard+CI | gradient metrics |
| Header gradient | G2 | diagnostic | report `CC_small/large ETag_small/large SC_small/large Vary_small` | gradient metrics |
| CI nondegenerate | E1 | diagnostic | `width 0` vs `>0` | bootstrap width under concurrency |
| Header folding | E2 | diagnostic | `0.0` if normalized | folded vs canonical |
| Edge visibility | E3 | diagnostic | `HIT/BYPASS` distribution | worker + CDN cache status |
| BrowserGym | E4_BG | conditional | `>0.5` if image available else `NOT_TESTED` | BrowserGym fingerprint if available |

---

## 8. Validity Threats and Mitigations

1. **Paid CDN credentials/domain unavailable:** mitigate via env `SPIDER_CDN_DOMAIN`/`CF_API_TOKEN`; if absent declare `MEASUREMENT_INVALID CDN_UNAVAILABLE` with reason, preserve `L` sanity, do not falsify CDN claim; retry once with purge.
2. **CDN brotli/gzip decompression CLEN mismatch:** CDN serves compressed `Content-Encoding: br/gzip` with `Content-Length` of compressed bytes vs decompressed `body_len`; mitigate by auto-decompressing `requests` bodies before SHA and comparing `decompressed_body_len` to decompressed length; log `Content-Encoding` and `CLEN` raw vs decompressed; mismatch without decompression triggers `DECOMPRESSION_MISMATCH` investigation before falsification.
3. **Edge cache HIT serving stale body/header:** stale `HIT` could mask recent `body_config/header_config` write; mitigate by `PURGE` before each batch and using `Cache-Control: no-store` for admin writes plus `CF-Cache-Status BYPASS` for auth routes; verify `SELECT` before batch; if `CF-Cache-Status HIT` on `BYPASS` route mark `HEADER_DRIFT` invalidity.
4. **Body/header not committed / cross-worker stale:** same mitigations as parent plus `500ms` retry and `X-Worker-Pid` distribution logging; `COMMIT_NOT_VERIFIED` invalidity.
5. **Header case/ordering/whitespace folding by CDN:** CDN may lowercase/reorder or strip whitespace/quote; mitigate by sorted lowercased aggregation; folding variant `E2` tests this; if `Connection` varies due to keep-alive log included set; any non-CLEN variation on body-only fails `C6` validity before falsification.
6. **Multiple Set-Cookie coalescing by CDN:** CDN may join multiple `Set-Cookie` into comma-joined single header; mitigate by single `Set-Cookie` only in `E` isolations and logging raw header list with multi-value sorted aggregation.
7. **Status not 200 or rate-limited 429/503 via edge:** `STATUS_MISMATCH` or `RATE_LIMITED` invalidity with retry; verify parity `L` vs `P_CDN`.
8. **Excluded headers drift:** `Date/CF-RAY/CF-Cache-Status/X-Cache/Server` varies but excluded; verify `EXCLUDED` constant.
9. **Degenerate CI misread as precision:** disclose `effective distinct N=1`, treat as deterministic; `G1/G2` explicitly measure width under concurrency for non-degeneracy.
10. **Port collision / stale server / CDN purge delay:** discover free ports for origin, fresh DB, purge cache with `200ms` delay before next batch; record ports/purge ID in provenance.
11. **BrowserGym image unavailable:** `docker image inspect` test; if fails mark `E4_BG NOT_TESTED IMAGE_UNAVAILABLE` not gating `C1-C10`.
12. **Threshold confusion (`>=0.7` vs `>0.5`):** `C1/C2/C9` use `>0.5`, `C7/C8` use `>=0.7` per Director; document exact value+CI.
13. **Gradient ceiling remains 1.0 everywhere:** if all magnitudes `1.0` degenerate, sensitivity ordering is `unknown` but still `SUPPORTS` if `C1-C10` pass; disclose as `width 0` for all and `unresolved` for ordering.
14. **Chunked buffering re-encoding:** `nginx proxy_buffering off` plus CDN chunked may produce `Transfer-Encoding: chunked` without `Content-Length`; reassemble chunks before SHA and treat missing CLEN as `chunked` variant; log.

---

## 9. Consequences

**Positive (all C1–C10 pass via CDN + gradients reported):** `C-MEAS-VALID` ceiling expands from `gunicorn+nginx loopback EXPERIMENTAL` to `paid-tier CDN (HIT/STALE/SWR/SIE/304, Vary/ETag, chunked/brotli) + BrowserGym 1280x720 EXPERIMENTAL` with both non-vacuous branches validated via edge decompressed observation (`full 1.0 >0.5` body-only and header-only, `status/body` isolation `0.0`, `CLEN` isolation, null `<0.05`, writable `>=0.7` cross-worker/BYPASS). Degenerate vs non-degenerate disclosure plus per-value `1B/2B/4B` and `CC_small/large` gradients enable sensitivity ordering beyond ceiling for Graph freshness policy calibration. Closes Director `CONTINUE` binding question and removes portfolio blocker (`tunnel_flag true`, 43-experiment loopback streak) blocking `C-DELTA-REPAIR`/`C-FRESHNESS` distributed work. Still bounded: does not promote to `VALIDATED/PRODUCT_CORE`; paid CDN provider/region/POP, single origin host, filtered header set, body magnitudes `31-117B`, TLS via edge only, `Vary` isolated small vs combined remain partially unresolved beyond tested values; BrowserGym conditional remains `NOT_TESTED` if image unavailable.

**Negative (any C1–C10 fails where validity passes):** Same-status body-only or header-only or null or writable does not generalize to paid CDN edge: edge header normalization (`CF` lowercases/reorders, `Vary` stripping, `ETag` whitespace), brotli/chunked `CLEN` vs decompressed `body_len` mismatch, or edge caching `HIT` stale masks discrimination or null stability breaks. `C-MEAS-VALID` remains `EXPERIMENTAL` bounded to loopback only; CDN generalization falsified bounded to tested edge provider/config. Graph freshness/delta-repair and Physics must not trust HTTP fingerprint on CDN-fronted production until substrate redesign (header canonicalization, decompressed `CLEN` handling, `Connection` exclusion reconsideration, `BYPASS` for drift routes, `Vary` handling). Gradient still reports which magnitude is fragile to direct redesign. Negative is high-information and prevents false promotion.

Both outcomes are high-information and will be consumed by Codex as the CDN promotion decision required before any `VALIDATED` or `PRODUCT_CORE` claim.

---

## 10. What is NOT Tested (Scope Boundaries)

- Multi-host `Redis` cluster or `SQLite` multi-node replication beyond single-host `2-worker` `WAL` + CDN `BYPASS` — single-host edge-bypass visibility tested; true distributed `C-FRESHNESS C1 TN=0.667` fix beyond single host remains unresolved.
- `TLS` version pinning / `HTTP/3 QUIC` beyond CDN edge termination — plain edge `HTTPS` only.
- Full `STALE/SWR/SIE/304` lifecycle beyond single `HIT` and `304 If-None-Match` revalidation probe — best-effort via `CF-Cache-Status STALE/SWR` logging.
- BrowserGym `DOM/AX` capture beyond HTTP triple (rendered text hash, accessibility tree) — HTTP `status/body/headers` only if image available.
- Header values beyond fixed `Cache-Control/ETag/Set-Cookie/Vary` values in table — gradient covers small/large deltas for those 4 headers only.
- Body sizes beyond `31-117B` JSON with `sort_keys=True` — proportional `CLEN==body_len` holds for these bodies after decompression.
- End-to-end cost/latency/tokens/`LLM` inheritance/cross-site holdout — not measured (runtime substrate only).

---

## 11. Execution Checklist for EXECUTE

- [ ] Implement `run_experiment.py` with fingerprint functions byte-identical to `research/experiments/EXP-RUNTIME-35764329925/run_experiment.py:compute_fingerprint` (`status_only`, `body_only`, `headers_only`, `headers_no_clen`), sorted lowercased filtered headers, `EXCLUDED_HEADERS={Date,Server,X-Request-Id,CF-RAY,CF-Cache-Status,CF-Connecting-IP,X-Cache,Age}` plus disclosed `X-Worker-Pid`, decompression via `response.content` auto-decompressed; ensure audit recomputation `0` mismatches.
- [ ] Extend Flask app with same `body_config/header_config` tables, `POST /admin/set_*` with `COMMIT` + `SELECT` verification, `GET /resource` mode-dependent bodies/headers, `X-Worker-Pid` header, `Cache-Control` `public max-age=60` for CDN HIT vs `private/no-store` for BYPASS.
- [ ] Launch topology `L` (Werkzeug free port) for sanity `AvsC AvsE` replication (`60` lines) — must be `1.0` else `SYSTEM_BROKEN`.
- [ ] Install `gunicorn` write per-run `nginx.conf` to `/tmp/spider-runtime-35774047385/nginx/` start `gunicorn --workers 2 --bind 127.0.0.1:19860 app:app` and `nginx -c <conf> -p /tmp/...` `127.0.0.1:19851`; verify health via `curl` before CDN.
- [ ] Provision CDN edge: if `SPIDER_CDN_DOMAIN`+`CF_API_TOKEN`/`FASTLY_API_KEY` set, create DNS -> origin, push cache rules (`/resource` HIT `60s` `Vary Accept-Encoding` `ETag` on, `/admin/*` BYPASS), enable `Brotli`, purge cache, verify edge `GET https://$DOMAIN/resource` returns `200` with `CF-Cache-Status MISS->HIT` and decompressed body `31B`; else record `CDN_UNAVAILABLE`.
- [ ] Execute CDN primary: body-only `A×20 B×20 C×20 =60` + gradients `A1×20 A2×20 A3×20 =60`, header-only `A×20 E×20 =40` + isolations `CC_small 20 CC_large 20 ETag_small 20 ETag_large 20 SC_small 20 SC_large 20 Vary_small 20 =140`, body null concurrent `A1×20 A2×20 =40` header null concurrent `40` classic `P_403 403×20 vs200×20 + null 40` `S_401 401×20 vs200×20 + null 40` sequential baselines `100` folding variant `20` = `~520` CDN observations plus sanity `60` = `~580` raw lines; each logs `state,status,body_sha256,body_len,content_length_header,content_encoding,headers_filtered_json,headers_raw_json,headers_no_clen_json,fingerprint_*,worker_id,cdn_cache_status,timestamp,concurrency`.
- [ ] If `docker image inspect am1n3e/webarena-verified-shopping` or `AgentLab` succeeds, run same `AvsC AvsB AvsE` isolations via `BrowserGym 1280x720 Playwright fetch` (`60-80` lines) capturing same triple; else mark `E4_BG NOT_TESTED`.
- [ ] Produce `raw_observations.jsonl` (`580±20` lines), `batch_state_log.jsonl` (`>=27` lines `SELECT` + `CF-Cache-Status` warmup), `result.json` per `research/EXPERIMENT_PACKET.md §4` with `schema_version lane status outcome metrics controls artifacts observations validity_notes unresolved`.
- [ ] Metrics stable names: `cdn_body_AvsC_full`, `cdn_body_AvsB_full`, `cdn_header_AvsE_full`, `cdn_body_gradient_1B_full`, `cdn_header_gradient_CC_small_full`, `cdn_null_body_full`, `cdn_perm_403_vs_200_full`, `cdn_sess_401_vs_200_full`, `bg_body_AvsC_full` etc plus `bootstrap CI` `width` `degenerate` `effective_distinct_n`; controls stable `C1_CDN-C10_CDN G1 G2 E1-E4_BG` with pass/fail and evidence_refs.
- [ ] Record `provenance.json` with `github_run_id 35774047385 base_sha f50de84` env (`Flask 3.1.3 PyJWT 2.14.0 SQLite 3.45.1 WAL Werkzeug 3.1.8 gunicorn 23.0.0 nginx 1.24.0 CDN provider/version/domain edge cache rules ports SEED 44 EXCLUDED body SHAs/lengths header constants artifact SHA-256 git commit BrowserGym image hash if used CDN purge ID).
- [ ] Must not inspect outcomes before freeze; frozen `spec.json`/`prereg.md`/`freeze.json` immutable after freeze; any deviation after seeing data is exploratory and labeled.
- [ ] Preserve stable control/metric identities for `AUDIT`/`DIRECTOR` transmission per `research/EXPERIMENT_PACKET.md §1`; keep `Jaccard` discrimination identical to parent for comparability; report `effective distinct N` and `degenerate` flag per `metrics`.
- [ ] Handle unavailable substrates gracefully: if CDN credentials missing mark `MEASUREMENT_INVALID CDN_UNAVAILABLE` with diagnostic and preserve `L` sanity; if BrowserGym missing mark `E4_BG NOT_TESTED unresolved` not gating `C1-C10`.

