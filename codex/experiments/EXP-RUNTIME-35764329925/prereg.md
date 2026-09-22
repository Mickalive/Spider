# EXP-RUNTIME-35764329925 — Preregistration

**Experiment ID:** EXP-RUNTIME-35764329925  
**Lane:** Runtime  
**Claim:** C-MEAS-VALID (Measurement substrate is intervention-valid)  
**Director Mandate:** PIVOT — Does the HTTP fingerprint substrate SHA256(status||body_bytes||sorted_filtered_headers) retain discriminating same-status body-only (200 vs 200, body-only >0.5, status-only 0.0, full > status strictly, headers-no-CLEN 0.0, Content-Length varies) and header-only discrimination with null stability (FP<0.05) and writable permission/session controls >=0.7 when moved from localhost Flask dev server to production WSGI (gunicorn)/nginx/CDN or BrowserGym/AgentLab substrates with concurrency, realistic header folding/ordering, and distributed session replication where bootstrap CIs become non-degenerate?  
**Parent Handoff:** research/experiments/EXP-RUNTIME-35749360317/handoff.json (sha256:cab2dbc0a99272a536a37c9ee2c92d23a4bf1cba7b3fa4edbe9bc85845b94865) — **disposition SUPERSEDE** per request.json director_mandate.parent_handoff_disposition. Inherited continuity evidence preserved four-way but does NOT govern design; Director's PIVOT question is binding.  
**Date:** 2026-09-22

---

## 1. Question

Does the identical HTTP fingerprint substrate — `SHA256(status || body_bytes || sorted_filtered_standard_headers)` with `EXCLUDED_HEADERS={Date,Server,X-Request-Id}` — retain its discriminating same-status body-only and header-only behavior with null stability and writable permission/session controls (≥0.7) when moved from localhost Flask dev server (Werkzeug 3.1.8) to a production-like WSGI stack (gunicorn sync workers) + nginx reverse proxy (emulating CDN header folding/ordering, proxy buffering) and, where Docker image available, BrowserGym/AgentLab 1280×720 observation substrate, under concurrency and distributed session replication where bootstrap CIs are tested for non-degeneracy?

This is the binding Director question for this governed NEW experiment. The parent `next_question` is preserved as continuity evidence (it is the same question) but per SUPERSEDE the Director's target claim, cognitive reset rationale, and portfolio assessment govern design. This design **does not repeat** another localhost-only body/header magnitude variant (all prior localhost variants hit ceiling 1.0, degenerate CI [1.0,1.0]/[0.0,0.0], no gradient).

---

## 2. Hypothesis

The fingerprint algorithm `hash(status_code || body_bytes || sorted_filtered_standard_headers)` with `EXCLUDED_HEADERS=[Date,Server,X-Request-Id]` identical to `research/experiments/EXP-RUNTIME-35749360317/run_experiment.py:compute_fingerprint` (and `...:compute_fingerprint_status_only`, `...:compute_fingerprint_body_only`, `...:compute_fingerprint_headers_only`, plus `compute_fingerprint_headers_no_clen`) will on **production-like stack** `Flask 3.1.3 + PyJWT 2.14.0 HS256 + SQLite WAL — served via gunicorn (2× sync workers, bind 127.0.0.1:19860) + nginx 1.25+ reverse proxy (listen 127.0.0.1:19851 proxy_pass to gunicorn upstream, proxy_set_header Host $host, proxy_http_version 1.1)`:

- **(H1) Same-status body-only discrimination retained:** `full(A vs C) >0.5` expected `1.0` deterministic where `A` and `C` both return `200` but byte-different JSON bodies via writable `body_config/content_variant` (≈31 B vs 117 B SHA distinct `d0ca833f843c...` vs `b46c461cceee...`), `body-only >0.5` on `A vs C` and `A vs B` (70 B `67c186f2cee...`), `status-only =0.0`, `full > status` strictly (1.0 > 0.0, complement to header-only), `headers-no-CLEN =0.0` (no independent header drift), `Content-Length` varies `31/70/117` and equals `body_len`, non-CLEN filtered headers identical, null body-A resampled `0.0` CI contains 0.0 ≤0.05.

- **(H2) Header-only discrimination retained:** `full(A vs E) >0.5` expected `1.0` where `A` and `E` both `200`, bodies byte-identical `31B SHA d0ca833f...`, `Content-Length 31` identical, filtered headers vary (`Cache-Control max-age=3600→max-age=0,must-revalidate`, `ETag W/\"fixed-aaa-111\"→W/\"changed-bbb-222\"`, `Set-Cookie absent→session=xyz`, `Vary Accept-Encoding→Accept-Encoding,Origin`), `headers-only >0.5` expected `1.0`, `status-only 0.0`, `body-only 0.0`, `headers-no-CLEN >0.5`, `Content-Length` identical. Each isolated header (Cache-Control only, ETag only, Set-Cookie only) also `full 1.0 headers-only 1.0 status 0.0 body 0.0`.

- **(H3) Writable permission/session controls ≥0.7 retained across workers:** classic permission escalation `403 vs 200` (`UPDATE users SET role`) and session invalidation `401 vs 200` (`DELETE sessions`) committed to SQLite WAL (or Redis if available) via shared file, observed via nginx round-robin to both gunicorn workers, each `full ≥0.7` expected `1.0`, respective null 403 resampled and 401 resampled `0.0` ≤0.05; additionally `headers-no-CLEN` remains 0.0 on body-only and `body-only` 0.0 on header-only under production stack.

- **(H4) Concurrency non-degenerate CI measured:** with 4 concurrent clients via `ThreadPoolExecutor` (20 requests per state, 4 parallel) through nginx→gunicorn, null false-positive remains `<0.05` (`0.0`), bootstrap 95% CI `B=1000` width measured: if fingerprints remain byte-identical per state, CI degenerate `[0.0,0.0]/[1.0,1.0]` declared deterministic not precision (per prior audits V1); if nginx/gunicorn introduces variance (Connection keep-alive vs close, Via, X-Request-Id — but excluded — so filtered set should stay deterministic), `headers-no-CLEN 0.0` must still hold.

- **(H5) Header folding/ordering/case robustness:** logical header value determines fingerprint, not serialization whitespace/order/case (sorted lowercased keys, `sort_keys=True` separators `(',',':')`), tested by varying case/whitespace/order of `header_config`.

If all mandatory H1–H3 hold on production stack, the localhost→production promotion gap is closed for this substrate. If any fails where validity checks pass, production generalization is falsified.

---

## 3. Inherited State — What is Established, Rejected, Unknown (from parent handoff, preserved four-way, disposition SUPERSEDE)

From `EXP-RUNTIME-35749360317/handoff.json` (parent) and `EXP-RUNTIME-35741906498` (grandparent) — established ceilings are audit PASS but explicitly bounded to localhost Flask dev (Werkzeug). This experiment does **not** assume they generalize; it tests whether they do.

**Established (bounded, audit PASS, narrowed ceiling — localhost only, EXPERIMENTAL not VALIDATED/PRODUCT_CORE):**

- HTTP fingerprint `SHA256(status||body_bytes||sorted_filtered_headers)` with `EXCLUDED_HEADERS={Date,Server,X-Request-Id}` deterministically discriminates **header-only** server-state drift `full 1.0 headers-only 1.0 status 0.0 body 0.0` with `Content-Length 31` identical and body SHA `d0ca833f843c...` identical on `127.0.0.1:19848` Flask 3.1.3 + PyJWT 2.14.0 HS256 + SQLite WAL (Werkzeug 3.1.8 Py3.12.14 SEED 44, `N=20` nominal effective distinct `N=1` degenerate CI, audit PASS 0 mismatches) — `EXP-RUNTIME-35741906498`.

- Per-header isolations each alone sufficient: `Cache-Control alone 1.0`, `ETag alone 1.0`, `Set-Cookie alone 1.0` on full/headers-only; null `A1 vs A2 0.0 CI [0.0,0.0]` and exploratory `E1 vs E2 0.0`.

- Same-status **body-only** drift discriminated complementarily on same localhost config at `127.0.0.1:19849`: `full 1.0 >0.5 body-only 1.0 >0.5` on `A vs C` (31 B vs 117 B SHA `d0ca833f...` vs `b46c461cceee...`) and `A vs B` (70 B `67c186f2cee...`), `status 0.0` (200 vs 200), `headers-no-CLEN 0.0`, `headers-only 1.0` solely via `Content-Length 31/70/117 == body_len`, `full > status` strictly `1.0>0.0` (complement to header-only's `full 1.0 > max(status 0.0,body 0.0)`), `Content-Length` isolation verified, audit PASS 0 mismatches on 300 lines, 27 `batch_state_log` — `EXP-RUNTIME-35749360317`.

- Writable classic controls on localhost Flask: permission escalation `403 vs 200` and session invalidation `401 vs 200` achieve Jaccard `1.0 ≥0.7` deterministic with same-state null `0.0` and body SHA distinct (`403 22B 387fe7...`, `401 25B 9df36...`); plus body-filtered `200 vs 200` via `body_config A vs C`; nginx `HIT/HIT/SWR/SIE/304` 960/960 byte-identical decompression — `EXP-RUNTIME-35611612543`.

- Combined localhost matrix (header-only bodies identical + body-only status constant + status-varying maximally-distinct + null stability) is complete for Flask dev server HS256, still bounded to single sequential client, degenerate CI effective `N=1`, jitter `50-150ms` no observable effect.

**Rejected (bounded to localhost Flask dev):**

- Header-only drift undetectable when bodies/status identical, or detectable only via `Content-Length` correlation — falsified: `full 1.0 headers-only 1.0` with `CLEN 31` constant and body identical.
- Same-status body-only drift undetectable when bodies differ but status `200` (or detectable only with status leakage/independent header drift) — falsified: `full 1.0 >0.5 body-only 1.0 status 0.0 headers-no-CLEN 0.0 CLEN 31/70/117` on localhost.
- Full-vector adds no marginal value beyond `body/status` (prior vacuous `full==body==status==1.0` where both vary) — falsified for header-only and body-only isolated branches; remains vacuous where both vary.

**Unknown (this experiment directly targets the first three — per Director binding question):**

- Does discrimination hold on production WSGI (`gunicorn`), `nginx`, `CDN` (Cloudflare paid-tier/Fastly/Akamai/CloudFront), load balancer with realistic header handling, header ordering/whitespace/case folding, multiple `Set-Cookie`, compression — Flask dev only tested.
- Does discrimination hold under concurrency, `HTTP/2`, `TLS`, multi-client, or non-deterministic header emission where bootstrap CI becomes non-degenerate and sensitivity ordering emerges (currently all isolations hit ceiling `1.0`, no gradient).
- Does distributed or CDN-cached header/body handling preserve discrimination for `C-FRESHNESS`/`C-DELTA-REPAIR` beyond localhost single-node SQLite WAL — distributed `C-FRESHNESS` previously failed `C1 TN=0.667` due to per-node SQLite non-replication; Redis/sticky routing untested.
- What is per-body and per-header signal strength gradient when bodies/headers vary with smaller magnitudes or multiple concurrent changes — all tested 31/70/117 and 3 header isolations at ceiling `1.0`.
- Does `Vary` header alone discriminate when isolated — tested only as part of combined `E` state.
- Does nginx/CDN `HIT` vs `MISS` byte-preserving behavior generalize beyond localhost nginx instance tested.

**Do not assume (explicitly unsafe):**

- `C-MEAS-VALID` is `VALIDATED` or `PRODUCT_CORE` — audit PASS supports `EXPERIMENTAL` only; promote `false`.
- Localhost Flask dev server results generalize to production `WSGI` (`gunicorn`), `nginx`, `CDN`, distributed SQLite replication, `BrowserGym/AgentLab` — explicitly untested per validity notes and audit `V2`.
- Bootstrap CI degenerate at `1.0/0.0` reflects high sampling precision — degenerate because all `20` fingerprints per state byte-identical (effective `N=1`); jitter had no observable effect (`V1`).
- Full-vector always adds marginal value — true only for isolated branches; prior maximally-distinct remains vacuous.
- `Content-Length` variation `31/70/117` proves arbitrary body sizes discriminate — tested only 3 specific JSON bodies.
- Role-based permission-filtered body (two tokens same `body_config`) was separately measured — not tested (realized via `body_config` variant `A vs C` per frozen rule).
- `BrowserGym`/`AgentLab` 1280×720 or paid-tier `CDN HIT` HIT/SWR/SIE generalizes from localhost — not tested.

This `PIVOT` does not repeat localhost value-magnitude variations. It tests the production promotion that the 42-experiment localhost streak left as the systemic enabler gap.

---

## 4. Server Design

### 4.1 Testbed Architecture (two topologies, same Flask app)

```
Flask 3.1.3 + PyJWT 2.14.0 HS256 + SQLite WAL (WAL mode, file per run)
  ├── POST /admin/set_body_variant   (admin JWT, writes body_config/content_variant, SQLite COMMIT)
  ├── POST /admin/set_headers        (admin JWT, writes header_config, COMMIT)
  ├── POST /admin/set_role           (UPDATE users SET role)
  ├── POST /admin/invalidate_session (DELETE sessions)
  ├── GET  /resource                 (authenticated GET, returns status+JSON body+filtered headers)
  └── GET  /protected                (smoke)

Topology L (sanity replication):  Werkzeug dev server 127.0.0.1:<free>  (single client sequential, N=20 per state)
Topology P (primary):             gunicorn 22+ sync --workers 2 --bind 127.0.0.1:19860 --timeout 30  +  nginx 1.25+ listening 127.0.0.1:19851 proxy_pass http://gunicorn_upstream (upstream gunicorn 127.0.0.1:19860, round-robin, proxy_http_version 1.1, proxy_set_header Host $host, proxy_set_header Connection "", proxy_buffering off for /resource)
```

`body_config` table schema: `variant TEXT PRIMARY KEY, body_json TEXT`; initialized `variant='A'` `{"data":"hello","version":1}` 31 B. `POST /admin/set_body_variant` updates row + `COMMIT` before `200`. `header_config` table: `key TEXT PRIMARY KEY, value TEXT`; fixed `Cache-Control:max-age=3600`, `ETag:W/\"fixed-aaa-111\"`, `Vary:Accept-Encoding`, no `Set-Cookie`, `Content-Type:application/json`. All `GET /resource` for body-only use same valid JWT; body variation driven by `body_config`, status stays `200`. For header-only, `header_config` varied; bodies held `31B`.

**Gunicorn+nginx startup:** discover free ports (default `19860`/`19851` or next free), write per-run `nginx.conf` to `/tmp/spider-runtime-35764329925/nginx.conf` with `events { worker_connections 1024; } http { upstream gunicorn { server 127.0.0.1:19860; } server { listen 19851; location / { proxy_pass http://gunicorn; proxy_set_header Host $host; proxy_http_version 1.1; proxy_set_header Connection ""; } } }`, start `gunicorn` `app:app` then `nginx -c <conf> -p /tmp/spider-runtime-...`, verify `/resource` via curl before measurement, kill on exit. Log `gunicorn --version`, `nginx -V`, config SHA, ports in `provenance.json`. If binary missing, record `MEASUREMENT_INVALID` with category `NGINX_UNAVAILABLE`/`GUNICORN_UNAVAILABLE`.

**Authentication:** JWT `sub` only, role lookup from SQLite (same as parent). For classic controls, `UPDATE users SET role` and `DELETE sessions` committed before `GET`.

### 4.2 Body and Header States (identical magnitudes to parent for comparability)

| State | Body JSON (sort_keys=True) | body_len | Body SHA-256 | Status | Filtered Headers (non-CLEN constant or varied) |
|-------|----------------------------|----------|--------------|--------|-----------------------------------------------|
| **A baseline** | `{"data":"hello","version":1}` | 31 | `d0ca833f843c6d70ec9d6755f52a92dcbfc8b4ab601b871bced09ad027172e34` | 200 | `Cache-Control:max-age=3600, ETag:W/\"fixed-aaa-111\", Vary:Accept-Encoding, Content-Type:application/json, Content-Length:31, Connection:close` (constant for body-only) |
| **B reader** | `{"data":"hello","items":["a","b"],"role":"reader","version":1}` | 70 | `67c186f2cee...` distinct | 200 | identical to A (body-only branch) |
| **C admin** | `{"admin_note":"sensitive:42","count":42,"data":"hello","items":["a","b","c"],"role":"admin","version":1}` | 117 | `b46c461cceee...` distinct | 200 | identical to A (body-only branch) |
| **E header-variant** | `{"data":"hello","version":1}` (same 31B) | 31 | same as A | 200 | `Cache-Control:max-age=0,must-revalidate, ETag:W/\"changed-bbb-222\", Set-Cookie:session=xyz; Path=/; HttpOnly, Vary:Accept-Encoding, Origin, Content-Type:application/json, Content-Length:31` |
| **Isolations** | same 31B | 31 | same as A | 200 | Cache-Control only *or* ETag only *or* Set-Cookie only varied, others at A baseline |
| **P_403** | `{"error":"forbidden"}` | 22 | `387fe7...` | 403 | via nginx/gunicorn, filtered headers constant |
| **S_401** | `{"error":"unauthorized"}` | 25 | `9df36...` | 401 | via nginx/gunicorn |

Header folding test variant: same logical values as `E` but sent with varied case (`cache-control: max-age=0`) and extra whitespace/order (`ETag :  W/\"changed-bbb-222\"` plus `Set-Cookie` ordering) — fingerprint must normalize via sorted lowercased aggregation so discrimination remains `0.0` between folded vs canonical.
---

## 5. Measurement

### 5.1 Observation Vector (per request)

- HTTP status code `int`
- Response body exact bytes + `SHA-256` + length `int` + `Content-Length` header value `str` (must `== body_len` unless nginx chunked — then `Transfer-Encoding: chunked` logged and body reassembled)
- Raw headers dict `dict` + filtered headers dict (minus `EXCLUDED_HEADERS`) + `headers_no_clen` dict (filtered minus `Content-Length`)
- Fingerprints: `full = SHA256(status || body_bytes || sorted_filtered_headers_json)`, `status_only = SHA256(status)`, `body_only = SHA256(body_SHA256)`, `headers_only = SHA256(sorted_filtered_headers_json)`, `headers_no_clen = SHA256(sorted_filtered_headers_without_CLEN)` — identical functions to parent `run_experiment.py`
- `worker_id` (gunicorn worker pid via `X-Worker-Pid` response header if injected by app, else `unknown`), `timestamp`, `concurrency` flag (`sequential` vs `concurrent`)

### 5.2 Discrimination Metric

Jaccard distance between fingerprint sets:

```
discrimination = 1.0 - |set_A ∩ set_B| / |set_A ∪ set_B|
```

Sets built from `N=20` fingerprints per state per topology. With deterministic responses expected set size `1` per state, discrimination `1.0` if any bit differs, `0.0` if identical. Bootstrap 95% CI `B=1000` by resampling fingerprint sets with replacement, but reported as degenerate when set size `1` (expected). Effective distinct `N` and set size reported. Thresholds per Director: `>0.5` for body-only/header-only positive, `=0.0` for status isolation on same-status, `≥0.7` for classic permission/session positives, `≤0.05` for null `FP`.

### 5.3 Baselines

| ID | Source | Expected on body-only A vs C (200 vs 200, 31 vs 117) via nginx→gunicorn | Expected on header-only A vs E (200 vs 200, 31 identical) via nginx→gunicorn | Purpose |
|----|--------|------------------------------------------------|------------------------------------------------|---------|
| B-STATUS-ONLY | status only | 0.0 | 0.0 | Strong null: proves status not signal when held constant |
| B-BODY-ONLY | body SHA only | >0.5 expected 1.0 | 0.0 | Body carries signal when status constant |
| B-HEADERS-ONLY | filtered headers incl. CLEN | 1.0 via CLEN only (body-correlated) | 1.0 via Cache-Control/ETag/Set-Cookie | Body-correlated vs independent header |
| B-HEADERS-NO-CLEN | filtered headers minus CLEN | 0.0 (no independent drift) | 1.0 (independent header drift) | Isolation of independent header signal |

`B-HEADERS-ONLY 1.0` on body-only via `Content-Length` and `B-BODY-ONLY 0.0` on header-only with identical bodies are expected complements, not failures. Classic controls `403 vs 200` / `401 vs 200` expected `B-STATUS-ONLY 1.0` `B-BODY-ONLY 1.0`.

### 5.4 Sample Size

- Per topology `P` (gunicorn+nginx, primary): body-only `A×20, B×20, C×20 =60`; header-only `A×20, E×20 =40` plus 3 isolations `Cache-Control×20 + ETag×20 + Set-Cookie×20 =60`; body null `N1-body A1×20 + A2×20 =40` (concurrent); header null `A1×20 + A2×20 =40` (concurrent); classic `P_403 403×20 vs 200×20 =40`, `S_401 401×20 vs 200×20 =40` plus their nulls `403×20 vs 403×20` `401×20 vs 401×20 =40`; sequential baseline repeats body-only + header-only `60+40` for non-concurrent comparison. Total nominal lines production `≈ 360` (±20 for folding variant). Plus sanity topology `L` (Werkzeug) replication `A×20 + C×20 + E×20 =60` as control. `Jitter 50-150ms` uniform between bursts, `SEED=44`. Effective distinct fingerprints expected `≈10` (A,B,C,E + isolations) with degenerate CI disclosure required. `N=20` per state gives `140+` operational replication for audit recomputation; inferential power not the bottleneck (deterministic `1.0` at ceiling).

---

## 6. Decision Rule (Frozen — no post-hoc weakening)

**SUPPORTS** (production generalization) iff **ALL** mandatory `C1–C10` hold on the production `WSGI+nginx` topology `P` ( `127.0.0.1:19851` nginx → `127.0.0.1:19860` gunicorn 2 workers, `N=20` per state nominal, at least concurrent null, fingerprint algorithm identical, `EXCLUDED_HEADERS={Date,Server,X-Request-Id}`):

1. **C1_FULL_BODY_DRIFT_PROD:** `full(A vs C) >0.5` expected `1.0` deterministic with `status=200` on all 40 observations in `A` and `C` via `P`, body `SHA` distinct `d0ca833f...` vs `b46c461cceee...`, `Content-Length 31 vs 117` and `==body_len`, non-CLEN filtered headers identical.
2. **C2_BODY_ONLY_SIGNAL_PROD:** `body-only(A vs C) >0.5` expected `1.0` AND `>0.5` on `A vs B` (70 B vs 31 B); `headers-no-CLEN(A vs C) =0.0` and `headers-no-CLEN(A vs B) =0.0`; `headers-only` may be `1.0` solely via `Content-Length` (documented, not failure).
3. **C3_STATUS_ISOLATED_PROD:** `status-only =0.0` on `A vs C` and `A vs B` via `P` (any `>0.0` fails isolation, not same-status).
4. **C4_FULL_EXCEEDS_STATUS_NONVACUOUS_PROD:** `full(A vs C) > status-only(A vs C)` strictly (`1.0 > 0.0`, complement to header-only).
5. **C5_NULL_NO_FALSE_POSITIVE_PROD:** null `N1-body` (body `A` resampled, two independent `N=20` batches via `P` concurrent) `full =0.0` with `95%` bootstrap CI containing `0.0` and point `≤0.05` (`FP<0.05`), plus `status-only 0.0` `body-only 0.0` `headers-only 0.0` `headers-no-CLEN 0.0` on same null; same thresholds hold for header null `A` resampled via `P` concurrent, and for `403` same-state and `401` same-state nulls via `P` (`0.0` each).
6. **C6_CONTENT_LENGTH_VARIES_AND_HEADERS_CONSTANT_PROD:** `Content-Length` differs proportional to `body_len` (`31 !=70 !=117`) and `body_len` differs and `body SHA` distinct, while non-CLEN filtered headers (`Cache-Control, ETag, Vary, Set-Cookie`) identical across `A/B/C` via `P` and `Content-Length == body_len` on each observation. For header-only, `C10` below covers inverse identity.
7. **C7_WRITABLE_PERMISSION_PROD:** writable permission controls `full ≥0.7` — (a) permission-filtered body `reader 200 vs admin 200` (`A vs C`, auto `≥0.7` if `C1` `1.0`) and (b) classic escalation `403 vs 200` via `UPDATE users SET role` with committed SQLite WAL on `P` with cross-worker visibility (≥10 requests per worker verified via `X-Worker-Pid` header or pid log), `full ≥0.7` expected `1.0`, `body SHA` distinct `403 22B 387fe7...`, `status 403 vs 200` verified, same-state `403` null `0.0` ≤0.05.
8. **C8_WRITABLE_SESSION_PROD:** writable session invalidation `401 vs 200` via `DELETE sessions` on `P` with cross-worker commit, `full ≥0.7` expected `1.0` `status 401 vs 200` verified, `body SHA` distinct `401 25B 9df36...`, same-state `401` null `0.0` ≤0.05.
9. **C9_HEADER_ONLY_PROD:** header-only `full(A vs E) >0.5` expected `1.0` and `headers-only(A vs E) >0.5` expected `1.0` via `P`, with `status-only(A vs E) =0.0` `body-only(A vs E) =0.0`; additionally per-isolation `Cache-Control-only`, `ETag-only`, `Set-Cookie-only` each `full 1.0 headers-only 1.0 status 0.0 body 0.0` via `P`.
10. **C10_CLEN_IDENTITY_HEADER_ONLY_PROD:** `Content-Length` identical `31==31` and `body SHA` identical across header-only `A vs E` and each isolation via `P`, proving header-only not body-confounded (inverse of `C6`).

If any of `C1–C10` fails where validity checks pass → **FALSIFIED-IN-SETTING** for production generalization (bounded to `gunicorn+nginx` localhost, `Flask 3.1.3 HS256`, `2` workers, nginx reverse proxy, `127.0.0.1`, filtered header set, body magnitudes `31/70/117`, header values as above).

If infrastructure prevents verification → **MEASUREMENT_INVALID** with category (`GUNICORN_UNAVAILABLE`, `NGINX_UNAVAILABLE`, `PORT_BIND_FAIL`, `COMMIT_NOT_VERIFIED`, `STATUS_MISMATCH`, `BODY_NOT_DISTINCT`, `HEADER_DRIFT`, `BROWSERGYM_IMAGE_UNAVAILABLE`, `CONCURRENCY_START_FAIL`, `FINGERPRINT_MISMATCH`) retryability and diagnostic. Sanity failure of topology `L` (localhost Werkzeug replication not `1.0`) also triggers `MEASUREMENT_INVALID` (system broken, not production falsification). Degenerate bootstrap CI `[1.0,1.0]/[0.0,0.0]` is EXPECTED deterministic and is not measurement invalidity when set sizes `1` and validity checks pass.

**Exploratory (not gating SUPPORTS, but reported and high-information):**

- `E1_CI_NONDEGENERATE`: bootstrap CI width `>0` measured under concurrency `4` via `P`; hypothesis is degenerate `width 0` remains if fingerprints deterministic; non-degenerate width would indicate nginx-introduced header variance (e.g., `Connection: keep-alive` vs `close` if not excluded — but excluded set does not include `Connection`? Actually `Connection` is INCLUDED per filtered set, so keep-alive differences would be visible; `C5` would then fail if null gains variance — so `E1` is the diagnostic of that mechanism). Report width per comparison.
- `E2_HEADER_FOLDING`: case/whitespace/order folded header variant discrimination `full(folded vs canonical E) =0.0` (normalized) vs `>0` (not normalized). Logged but not gating `C9`.
- `E3_DISTRIBUTED_VISIBILITY`: permission/session write visible to both gunicorn workers within `500ms` (`SELECT` verifies on second worker, `X-Worker-Pid` distribution logged). If not visible, `E3` fails but `C7/C8` would also fail (since batch would see stale state), so not separately gating.
- `E4_BROWSERGYM`: `BrowserGym/AgentLab` `1280×720` HTTP-layer fingerprint discrimination for same `A vs C` and `A vs E` if image `am1n3e/webarena-verified-shopping` or `AgentLab` available; if `docker image inspect` fails, that substrate marked `NOT_TESTED` `unresolved` and does not affect `C1–C10`.

---

## 7. Controls Summary

| Control | ID | Type | Threshold | Evidence |
|---------|----|------|-----------|----------|
| Full body drift (prod) | C1 | positive | `>0.5` expect `1.0` | `A vs C` full Jaccard `1.0` via nginx→gunicorn, `200 vs 200`, body SHA ≠, CLEN ≠ |
| Body-only signal (prod) | C2 | positive + isolation | `body-only >0.5` on `A vs C` + `A vs B`; `headers-no-CLEN 0.0` | body-only Jaccard, headers-no-CLEN Jaccard |
| Status isolated (prod) | C3 | strong null | `=0.0` on `A vs C` and `A vs B` | status-only Jaccard `0` |
| Full > status (prod) | C4 | non-vacuous superiority | strictly `>` (`1.0 >0.0`) | full vs status-only on `A vs C` |
| Null stability (prod) | C5 | null | `=0.0` CI contains `0` ≤0.05 on body null, header null, 403 null, 401 null (concurrent) | null Jaccard `0` CI `[0,0]` |
| CLEN varies, headers constant (prod) | C6 | validity | `CLEN ≠` SHA ≠, non-CLEN `=` | header values, body_len, SHA |
| Permission writable (prod) | C7 | positive `≥0.7` + null | `full ≥0.7` on `200vs200` + `403vs200` cross-worker; null `0.0` | permission Jaccard, SELECT commit, worker distribution |
| Session writable (prod) | C8 | positive `≥0.7` + null | `full ≥0.7` on `401vs200` cross-worker; null `0.0` | session Jaccard, SELECT, worker distribution |
| Header-only (prod) | C9 | positive + isolation | `full >0.5 headers-only >0.5` on `A vs E` + each isolation `1.0`; `status 0.0 body 0.0` | header-only Jaccard, isolations |
| CLEN identity header-only (prod) | C10 | validity | `CLEN =` SHA `=` across `A vs E` | CLEN `31==31` SHA equal |
| CI nondegenerate (exploratory) | E1 | diagnostic | width `0` vs `>0` | bootstrap CI width under concurrency |
| Header folding (exploratory) | E2 | diagnostic | `0.0` if normalized | folded vs canonical Jaccard |
| Distributed visibility (exploratory) | E3 | diagnostic | visible `<500ms` both workers | worker pid log, SELECT timing |
| BrowserGym (conditional) | E4 | conditional | `>0.5` if image available else `NOT_TESTED` | BrowserGym fingerprint if available |

---

## 8. Validity Threats and Mitigations

1. **gunicorn/nginx binary unavailable:** mitigate by attempting `pip install gunicorn` and `apt-get`/`docker nginx:alpine` fallback; if still unavailable, declare `MEASUREMENT_INVALID` with category `GUNICORN_UNAVAILABLE`/`NGINX_UNAVAILABLE` and preserve localhost `L` result as continuity; do not falsify production claim.
2. **Body/header not committed / stale read across workers:** `POST /admin/set_*` not visible to second gunicorn worker → mitigate by SQLite `WAL` + `SELECT` verification before each batch plus `100ms` inter-batch delay and `500ms` retry; log `body_config`/`header_config` per worker via `X-Worker-Pid` header; if divergence, mark `DISTRIBUTED_DIVERGENCE` and treat as `MEASUREMENT_INVALID` for that batch, retry once.
3. **Body serialization variance:** mitigated by fixing `json.dumps(sort_keys=True, separators=(',',':'))` server-side; verify `SHA-256` inequality before discrimination; `Content-Length == len(body_bytes)` must hold; nginx `chunked` reassembled before SHA.
4. **nginx header case/ordering/whitespace folding breaks isolation:** `Connection` is currently INCLUDED in filtered set, so `keep-alive` vs `close` differences between workers could create spurious `headers-only` variance on body-only branch → mitigate by documenting included set includes `Connection`; if `Connection` varies due to nginx keep-alive, that variance is real transport-header signal and `C2` would correctly detect it as body-correlated `1.0` via `Connection`? Actually `Connection` is constant `close` in parent; we set `proxy_set_header Connection ""` and `proxy_buffering off` to keep `Connection: close` constant; verify non-CLEN `Connection` identical across body-only states; any variation fails `C6` validity and triggers investigation before falsification.
5. **Multiple Set-Cookie coalescing by nginx:** nginx may join multiple `Set-Cookie` into comma-joined single header vs multiple headers → mitigate by testing single `Set-Cookie` only in `E` isolations; log raw `headers_raw` list preserving multiple values; compare sorted multi-value aggregation in `run_experiment.py`.
6. **Status not 200:** any `500/401/403` during body/header-only batches via `P` fails validity for that comparison; mitigated by same valid JWT and verifying parity between `L` and `P` (if `L` is `200` but `P` is `500` → `MEASUREMENT_INVALID` nginx config error, not falsification of header/body signal).
7. **Excluded headers drift:** `Date` varies per request but excluded; include only filtered; verify `EXCLUDED_HEADERS` constant; `Server` (nginx vs Werkzeug) varies but excluded `0` leakage.
8. **Header_config drift during body batches:** `Cache-Control/ETag/Vary` mutated by leftover state → set `header_config` once before body batches and verify identical `SELECT` before each; any non-CLEN difference fails `C6`.
9. **Degenerate CI misread as precision:** disclose effective distinct `N=1`, treat CI as deterministic, do not claim narrow inferential precision; same mitigation as parent; `E1` explicitly measures width under concurrency.
10. **Port collision / stale server:** discover free ports, start fresh per run, record ports in provenance, kill `gunicorn`+`nginx` on exit; SQLite file fresh per run.
11. **BrowserGym image unavailable:** `docker image inspect am1n3e/webarena-verified-shopping` test; if fails, mark `E4 NOT_TESTED` with `IMAGE_UNAVAILABLE` and do not gate `C1–C10`.
12. **Threshold confusion (`≥0.7` vs `>0.5`):** `C1/C2/C9` use `>0.5` (sensitive), `C7/C8` use `≥0.7` per Director for classic controls; document exact value and CI.
13. **Workload conflation:** production topology measurements run in fixed order `L sanity → P body-only → P header-only + isolations → P concurrent nulls → P classic controls` logged; order preserves worker warmup before classic controls.

---

## 9. Consequences

**Positive (all C1–C10 pass on production WSGI+nginx):** `C-MEAS-VALID` ceiling expands from localhost Flask dev `EXPERIMENTAL` to production-like `gunicorn+nginx` `EXPERIMENTAL` with both non-vacuous branches validated on same stack (`full 1.0 >0.5` body-only and header-only, `status 0.0 body 0.0` isolations, `Content-Length` isolation, null `<0.05`, classic writable `≥0.7` cross-worker). This closes the Director's binding `PIVOT` question and removes the top portfolio blocker (42-experiment localhost streak, `tunnel_flag true`, degenerate CI). Unblocked: `Graph C-DELTA-REPAIR` (4× `BLOCKED`) can proceed with trusted substrate for local perturbation measurement on production middleware; `C-FRESHNESS` can proceed to distributed replication fix (Redis/sticky routing) using this substrate with verified `header folding`/`ordering` robustness; `Physics` beyond-memory tests can use `gunicorn+nginx` as observation layer. Still bounded: does NOT promote to `VALIDATED`/`PRODUCT_CORE`; paid-tier `CDN HIT/HIT/SWR/SIE` (960/960 analogue), `TLS`/`HTTP2`, multi-host `Redis` cluster, `BrowserGym 1280×720` DOM capture (if image unavailable), value-magnitude gradient (still ceiling `1.0`), `Vary` isolation remain `unresolved`.

**Negative (any C1–C10 fails where validity passes):** Same-status body-only or header-only or null or writable behavior does not generalize to production `WSGI+nginx`: `nginx` header folding/ordering, proxy buffering, `gunicorn` worker isolation, or `SQLite WAL` cross-worker visibility breaks discrimination or isolation (`full ≤0.5` or `status !=0.0` or `headers-no-CLEN !=0.0` or `CLEN` not varying/identical or `null >0.05` or `writable <0.7`). `C-MEAS-VALID` remains `EXPERIMENTAL` bounded to Flask dev server only; production `CDN`/`distributed` generalization falsified. `Graph` freshness/delta-repair and `Physics` must NOT trust HTTP fingerprint on production middleware until substrate redesign (header canonicalization via lowercasing/sorting, `Content-Length` handling for chunked, `Connection` exclusion reconsideration, worker-shared state via Redis). Negative is equally high-information: it prevents false product promotion, bounds the substrate correctly, and directs the next design to the failing branch (body-only vs header-only vs distributed visibility).

Both outcomes are high-information and will be consumed by the Codex as the production promotion decision required before any `CDN` paid-tier or `BrowserGym` family hold-out can be trusted. Neither outcome alone closes `Vary` isolation or per-value gradient, which remain `unresolved`.

---

## 10. What is NOT Tested (Scope Boundaries)

- Paid-tier `CDN` (`Cloudflare`/`Fastly`/`Akamai`/`CloudFront`) `HIT`/`STALE`/`SWR`/`SIE`/`304` lifecycle beyond localhost `nginx` emulation — explicitly `NOT_TESTED` (nginx is local proxy, not real edge cache); `CDN HIT 960/960`-analogue remains unresolved beyond `EXP-RUNTIME-35611612543` localhost.
- `TLS`/`HTTP2`/`HTTPS` termination, `QUIC`, load balancer sticky routing — plain `http 127.0.0.1` only.
- Multi-host `Redis` cluster or `SQLite` multi-node replication beyond single-host `2`-worker `gunicorn` + shared `WAL` file — single-host cross-worker visibility tested; true distributed `C-FRESHNESS C1 TN=0.667` fix beyond single host remains unresolved.
- `BrowserGym`/`AgentLab` `1280×720` browser `DOM`/`API` state capture beyond `HTTP` layer — tested only if Docker image available; otherwise `NOT_TESTED`.
- `Header` value magnitudes beyond fixed `Cache-Control:max-age=3600/3600` and `ETag:W/\"fixed-aaa-111\"` vs `W/\"changed-bbb-222\"` and single `Set-Cookie:session=xyz` — no gradient beyond those values.
- `Vary: Accept-Encoding,Origin` alone isolation — combined `E` only.
- End-to-end cost/latency/tokens/`LLM` inheritance/cross-site holdout — not measured (runtime substrate only).
- `Freshness` correlation `r` or `delta-repair` amortization — graph-level claims, not runtime substrate.

---

## 11. Execution Checklist for EXECUTE

- [ ] Implement `run_experiment.py` with fingerprint functions byte-identical to `research/experiments/EXP-RUNTIME-35749360317/run_experiment.py:compute_fingerprint` (`compute_fingerprint_status_only`, `compute_fingerprint_body_only`, `compute_fingerprint_headers_only`, `compute_fingerprint_headers_no_clen`), sorted lowercased filtered headers, `EXCLUDED_HEADERS={Date,Server,X-Request-Id}`, for audit recomputation `0` mismatches.
- [ ] Implement Flask app extension with same `body_config`/`header_config` tables, `POST /admin/set_*` with `COMMIT` + `SELECT` verification, `GET /resource` returning mode-dependent bodies/headers, `X-Worker-Pid` header (via `os.getpid()`) for worker distribution logging.
- [ ] Launch topology `L` (Werkzeug dev, free port) for sanity `A vs C` and `A vs E` replication (60 lines).
- [ ] Install `gunicorn`, write per-run `nginx.conf` to `/tmp/spider-runtime-35764329925/nginx/`, start `gunicorn --workers 2 --bind 127.0.0.1:19860 app:app` and `nginx -c <conf> -p /tmp/spider-runtime-...` listening `127.0.0.1:19851`, verify health via `curl` before measurement, log versions/config SHA/ports in `provenance.json`.
- [ ] Execute production body-only (`A×20 B×20 C×20 =60`), header-only (`A×20 E×20 =40` + 3 isolations `Cache-Control×20 ETag×20 Set-Cookie×20 =60`), body null concurrent (`A1×20 A2×20 =40`), header null concurrent (`A1×20 A2×20 =40`), classic `P_403 403×20 vs 200×20` + null, `S_401 401×20 vs 200×20` + null (`=80+40`), sequential baselines (`60+40`), folding variant (`20`) — total `≈360` lines production plus `60` sanity = `≈420` raw lines; each request logs `state, status, body_sha256, body_len, content_length_header, headers_filtered_json, headers_raw_json, headers_no_clen_json, fingerprint_full/status/body/headers/headers_no_clen, worker_id, timestamp, concurrency`.
- [ ] If `docker image inspect am1n3e/webarena-verified-shopping` or `AgentLab` succeeds, run same `A vs C` + `A vs E` comparands via `BrowserGym` `1280×720` `Playwright` fetch (HTTP layer) and log as additional substrate; else mark `E4 NOT_TESTED` with reason.
- [ ] Produce `raw_observations.jsonl` (420±20 lines), `batch_state_log.jsonl` (≥27 lines with `SELECT` commit verification and worker pid), `experiment_result.json` (derived) and canonical `result.json` per `research/EXPERIMENT_PACKET.md §4` with `schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics` (stable names `body_drift_full_AvsC_prod`, `header_drift_full_AvsE_prod`, `classic_perm_full_prod`, etc.), `controls` (stable `C1–C10` plus `E1–E4` exploratory), `artifacts` (path+sha256), `observations`, `validity_notes`, `unresolved`.
- [ ] Record `provenance.json` with `github_run_id 35764329925`, `base_sha 52a886763fa1439999258b92f4ed743cb70f4bfd`, env (`Flask 3.1.3`, `PyJWT 2.14.0`, `SQLite 3.45.1 WAL`, `Werkzeug 3.1.8`, `gunicorn` version, `nginx -V` version, `Python 3.12.14`, ports `19860/19851`, `SEED 44`, `EXCLUDED_HEADERS`, `body_config` bodies/SHAs/lengths, `header_config` constants, artifact `SHA-256`, git commit, BrowserGym image hash if used).
- [ ] Must not inspect outcomes before freeze; frozen `spec.json`/`prereg.md`/`freeze.json` immutable after freeze; any deviation after seeing data is exploratory and labeled as such.
- [ ] Preserve stable control/metric identities (`C1–C10`, `B-STATUS-ONLY`, `B-BODY-ONLY`, `B-HEADERS-ONLY`, `B-HEADERS-NO-CLEN`) for `AUDIT`/`DIRECTOR` transmission per `research/EXPERIMENT_PACKET.md §1`; keep `Jaccard` discrimination definition identical to parent for comparability.
- [ ] Handle unavailable substrates gracefully: if `gunicorn`/`nginx` binary missing, write `MEASUREMENT_INVALID` with category and preserve degenerate CI disclosure; if `BrowserGym` missing, mark `E4 NOT_TESTED unresolved` not gating.
