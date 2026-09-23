# EXP-RUNTIME-35900903994 — Preregistration

**Experiment ID:** EXP-RUNTIME-35900903994  
**Lane:** runtime  
**Claims:** C-FRESHNESS (SPIDER can detect when inherited knowledge is stale), C-MEAS-VALID (Measurement substrate is intervention-valid)  
**Director Mandate:** CONTINUE — Can C-FRESHNESS orthogonality be restored to stratified |r|<0.15 (TOST delta 0.15, CI upper<0.15, p_upper<0.05, 8/8 variance, FP<=0.15) with status-free structural signal (hash(body) only, no status prefix) and de-confounded body_variant vs drift scheduling plus health-gated nginx startup (0 missing X-Worker-Pid, 0 status None) while retaining C1 TN>=0.85 mean Wilson lower>0.75 session_status>=0.85 and C2 n_non304>=800 via real If-None-Match/ETag->304 on shared SQLite WAL at /tmp/spider-runtime-35860330078/shared.db with HS256 shared-secret, and can URL-bound sticky hash $request_uri consistent without session mirroring achieve TN>=0.85 vs per-node 0.667, and can browser per-value gradients at prereg N=20 per state yield non-degenerate B=1000 CIs to order CC/ETag/CLEN sensitivity beyond degenerate [1.0,1.0] ceiling?  
**Parent Handoff:** research/experiments/EXP-RUNTIME-35884739384/handoff.json (sha256:c59f4ae41947e91d00036baabb0318b14a4e004639138c78976dbed6f9d85154) — **disposition USE** per request.json director_mandate.parent_handoff_disposition. Inherited continuity evidence preserved four-way but MUST NOT silently override Director CONTINUE decision. This design follows Director binding question, not parent next_question loop. Parent reported MIXED (audit REVISE: shared TN 0.986 lo 0.969 passes C1, n_non304 1052 passes C2, but orthogonality falsified r=-0.357 fails C3, sticky used ip_hash with mirrored sessions, 17/1200 status None, gradients at n=3-4 vs prereg 20). Cognitive reset true.  
**Date:** 2026-09-23  
**Dependencies:** EXP-RUNTIME-35764329925 (gunicorn+nginx loopback PASS deterministic 1.0/0.0 EXPERIMENTAL), EXP-RUNTIME-35884739384 (MIXED REVISE), EXP-RUNTIME-35611612543 (nginx 960/960 decompression), EXP-GRAPH-35389145821 (C-FRESHNESS orthogonality r=0.0022 on single-host mock)

---

## 1. Question

Can Runtime close the distributed C-FRESHNESS block with **four measurement fixes** applied to the same Flask 3.1.3 + gunicorn 23.0.0 2× sync + nginx 1.24.0 round-robin substrate, while preserving browser substrate power:

1. **Orthogonality fix:** replacing confounded structural signal `f"{status}|{body_variant}|"+body` (which leaks behavioral status into structural and correlates body_variant cycling with drift, yielding pooled r -0.357 stratified [-0.409,-0.303] and status-free r +0.62) with **status-free structural = hash(decompressed_body_bytes) only** and **de-confounded body_variant vs drift scheduling** (body_variant randomized uniformly independent of drift condition) to restore **stratified |r|<0.15 TOST within delta=0.15 (CI upper<0.15, p_upper<0.05, 8/8 variance std>0, FP<=0.15)**, plus **health-gated nginx startup (0 missing X-Worker-Pid, 0 status None)** on the shared SQLite WAL at `/tmp/spider-runtime-35860330078/shared.db` with HS256 shared-secret, while retaining **C1 TN>=0.85 (mean Wilson lower>0.75, session_status>=0.85)** and **C2 n_non304>=800 via real If-None-Match/ETag->304** stratified across 3 endpoints?

2. **Sticky isolation fix:** replacing prior `hash $remote_addr (ip_hash) + replicate_session_to_workers=True` (1200/1200 pin to one worker with mirrored sessions) with **URL-bound `hash $request_uri consistent` without session mirroring** (per-node DBs not replicated, same HS256 secret) to achieve **TN>=0.85 vs per-node 0.667** with >90% URL affinity skew via real HTTP, testing whether affinity alone can substitute for shared store?

3. **Browser power fix:** restoring **per-value gradients to prereg N=20 per state** (vs prior n=3-4) via real Playwright 1280×720 page.request to `/resource` with **B=1000 bootstrap CIs [lo,hi] width/degenerate/effective_distinct_n** for each magnitude (body 1B/2B/4B/39B/86B, headers CC_small 3601 1s / CC_large 0 / ETag_small 1char / ETag_large changed / SC / Vary) to yield **non-degenerate CIs that order CC vs ETag vs CLEN sensitivity beyond degenerate [1.0,1.0] ceiling**, while preserving **browser provision (AgentLab 0.4.2, viewport 1280×720, CDP AX median>10 on /resource, PC-HEALTH>=80%, DOM 21-82 per /resource page)** and **fingerprint isolation (body AvsC full>0.5 status 0 headers-no-CLEN 0, header AvsE full>0.5 CLEN 31==31)**?

This binding CONTINUE is the narrowest falsifiable step that changes architecture decision for Graph delta-repair and product residual-novelty economics per Director comparative reasoning: alternative PIVOTs to paid CDN or another localhost header/body discrimination are SUPERSEDED/ceiling-limited and do not unblock distributed freshness invalidity.

---

## 2. Hypothesis

**H1 — Distributed shared-store with fixes (C-FRESHNESS):** A shared-store fix (single shared SQLite WAL file at `/tmp/spider-runtime-35860330078/shared.db`, both gunicorn workers connecting to same DB file, WAL mode, `check_same_thread=False`, `COMMIT` verified via `SELECT count(*) FROM sessions` before each batch and logged in `batch_state_log.jsonl` with distinct timestamps not clustered, `X-Worker-Pid` distribution proving round-robin ≥10 per worker) **plus HS256 shared-secret replication** (Flask validates PyJWT token with shared secret on both workers, mapping Bearer JWT to session row correctly — fixing prior raw string lookup where 0/300 valid succeed) **with two additional validity fixes** — (a) **status-free structural**: `structural = hash(decompressed_body_bytes) only` (body_sha256 or hash(body)%10000 without status/body_variant prefix), and (b) **de-confounded scheduling**: `body_variant` (A 31B, A1 32B 1B diff, A2 33B 2B, A3 35B 4B, B 70B 39B, C 117B 86B) assigned uniformly random independent of drift condition (permission_boundary, session_invalidation, signing_key_rotation, token_expiry × cache_enabled) rather than cycling deterministically with drift — **and (c) health-gated startup**: harness gates on `GET http://127.0.0.1:19851/health` via nginx returning 200 with `X-Worker-Pid` present (retry up to 30s, effective 0 missing X-Worker-Pid and 0 status None) — will restore behavioral detection **mean TN ≥ 0.85** (session_status, profile, data_list each Wilson lower > 0.75, session_status individually ≥ 0.85, computed as true-negative rate `P(behavioral<=0.05|valid)`) with **n_non304 ≥ 800** after excluding real 304 via `If-None-Match`/`ETag` stratified across 3 endpoints, and will restore **orthogonality stratified pooled |r|<0.15 (Fisher z 95% CI upper<0.15, TOST p_upper<0.05, CI lower>-0.15)** with **8/8 variance std>0** and **noise FP≤0.15** on the shared-store arm via real HTTP. Per-node isolated baseline (each worker isolated temp DB `/tmp/spider-pernode-<worker>.db`, same HS256 secret but no shared sessions, also via real nginx round-robin, health-gated) replicates prior failure **TN ~0.667 (session_status 0.0)** proving HS256 alone insufficient.

**H2 — Sticky URL-bound without replication (C-FRESHNESS alternative):** A sticky-session fix **URL-bound** (`nginx hash $request_uri consistent`, not `ip_hash`/`$remote_addr`) with same HS256 secret but **without replicate_session_to_workers** (per-node DBs remain isolated) using **real URL distribution** (3 endpoints `/api/profile`, `/api/data_list`, `/api/session/status` with varied body_variant/query providing URL entropy) will achieve **mean TN ≥0.85 (session_status≥0.85 Wilson lo>0.75) with >90% affinity skew** (e.g., same URI repeatedly hits same worker, distribution skewed >90% for sticky vs balanced ≥10 per worker for round-robin) and **n_non304≥800**, demonstrating URL affinity can substitute for shared-store replication when sticky holds. Prior sticky used `ip_hash` collapsing to 1200/1200 on one worker with mirrored sessions; this isolates affinity correctly.

**H3 — Browser substrate at N=20 with non-degenerate CIs (C-MEAS-VALID):** `AgentLab 0.4.2` importable (pip `agentlab==0.4.2`, `0.14.3` correctly absent) + `Playwright 1.63.0 chromium` at **1280×720 viewport** (`browser.newContext({viewport:{width:1280,height:720}})`, verified per page) with **CDP `Accessibility.getFullAXTree` per /resource page** yielding **AX nodes>10 median, PC-HEALTH≥80% on /resource pages, DOM 21-82 per /resource page**, retains **body-only discrimination** (`full AvsC >0.5` expect 1.0 body 1.0 status 0 headers-no-CLEN 0) and **header-only discrimination** (`full AvsE >0.5` headers-only 1.0 status 0 body 0 CLEN 31==31) via **real Playwright `page.request.get` at N=20 per state** (not n=3-4) to `/resource` with decompressed bodies/filtered headers, and enables **per-value gradient sensitivity ordering** (body 1B/2B/4B/39B/86B, header CC_small 3601 1s vs 0, ETag_small 1char vs large changed, SC, Vary) each with **B=1000 bootstrap CI [lo,hi] width degenerate effective_distinct_n** — with N=20, effective distinct variance becomes measurable (width>0 possible under concurrency 4) allowing ordering beyond prior degenerate ceiling where n=3-4 guaranteed width 0.

If H1–H3 hold with validity checks passing, the distributed browser block is closed per Director.

---

## 3. Inherited State — What is Established, Rejected, Unknown (from parent handoff c59f4a..., preserved four-way, disposition USE)

From `EXP-RUNTIME-35884739384/handoff.json` (MIXED REVISE) and `EXP-RUNTIME-35764329925` (PASS loopback EXPERIMENTAL) plus `EXP-RUNTIME-35611612543` — ceilings are audit-confirmed but bounded to single-host gunicorn+nginx loopback or shared WAL without fixes, EXPERIMENTAL not VALIDATED.

**Established (bounded, audit recomputed within 1e-12, narrowed ceiling — loopback/mimic EXPERIMENTAL):**
- Shared SQLite WAL at `/tmp/spider-runtime-35860330078/shared.db` (WAL, check_same_thread=False, COMMIT verified via per-batch SELECT 31 lines distinct timestamps) + HS256 shared-secret (PyJWT 2.14.0 decode via shared secret) behind 2× gunicorn 23.0.0 + nginx 1.24.0 round-robin restores C-FRESHNESS detection: **shared TN mean 0.986 Wilson lo 0.969 (profile 1.0 lo 0.973, data_list 1.0 lo 0.973, session_status 0.958 lo 0.911)** with **n_non304 1052/1183** after 131 real If-None-Match/ETag->304 stratified 400 per endpoint, **HS256 success 0.991 (665/671)**, X-Worker-Pid 588/595 ≥10, 8/8 variance std>0, FP 0.0 vs per-node 0.666 session_status 0.0 (V1-V3 PASS).
- Per-node B-PER-NODE baseline 0.666 replicates distributed failure via real nginx round-robin (597/603) with same HS256 secret but isolated DB files, proving HS256 alone insufficient without shared store.
- Browser provision AgentLab 0.4.2 importable (0.14.3 correctly absent), Playwright 1.63.0 chromium viewport 1280×720 verified per /resource page, CDP Accessibility.getFullAXTree median 54 on /resource PC-HEALTH 100% DOM median 26 on /resource via real page.request fetches (raw_observations 396 lines: 198 browser+198 direct, ax_dom_pages 10 pages), fingerprint SHA256(status||decompressed_body||sorted_filtered_headers) byte-identical to EXP-RUNTIME-35764329925, decompressed CLEN==body_len verified 0 mismatches (31B vs 32/33/35/70/117B), filtered headers identical across body-only.
- Fingerprint discrimination preserved: body-only AvsC full 1.0 status 0 headers-no-CLEN 0, header-only AvsE full 1.0 status 0 body 0 CLEN 31==31, nulls 0.0 CI [0.0,0.0] contains 0 — but degenerate [1.0,1.0]/[0.0,0.0] effective_distinct_n=1 disclosed not high precision, all per-value gradients (1B/2B/4B/39B/86B CC/ETag/SC/Vary) 1.0 degenerate at n=3-4.

**Rejected (bounded):**
- C-FRESHNESS behavioral-structural orthogonality at delta=0.15 **FALSIFIED-IN-SETTING** on this harness: shared r -0.357 CI [-0.409,-0.303] pooled |r| 0.355 >0.15, per-endpoint -0.47/-0.39/-0.19, per_node -0.28, sticky -0.33 — valid falsification despite 8/8 variance and FP 0.0; not hardcoded.
- Common status-prefixed structural signal `f"{status}|{body_variant}|"+body` violates measurement_validity clause 8; status-free recomputation worsens to +0.62 pooled, so confound does not rescue C3 — rejected as valid structural definition.
- Per-node isolated DB (or HS256 alone without shared store) achieving TN>=0.85 rejected: mean 0.666 session_status 0.0 with 1107 non-304 via real HTTP — shared store required beyond HS256.
- Degenerate CI width 0 as high-precision evidence rejected: effective distinct N=1 deterministic.

**Unknown (this experiment directly targets the first three — per Director CONTINUE):**
- Whether orthogonality can be restored to |r|<0.15 with status-free structural (hash(body) only) and de-confounded body_variant vs drift scheduling; current harness body_variant cycle correlates with drift yielding |r| 0.35-0.62 including sign flip.
- Whether URL-bound sticky hash $request_uri consistent alone without replicate_session_to_workers achieves TN>=0.85 and real affinity >90% skew vs per-node 0.667; current sticky used ip_hash with 1200/1200 pin and mirrored sessions so affinity isolation untested.
- What per-value CC/ETag/CLEN/body-size sensitivity ordering is when CIs become non-degenerate at prereg N=20; all tested magnitudes are degenerate at n=3-4 so ordering unknown.
- Whether shared WAL generalizes to multi-host Redis cluster or tolerates >4 concurrency.
- Whether eliminating 17 missing X-Worker-Pid (1.4% connection-refused before nginx ready) via health-gated startup changes tail TN/power.
- Whether richer DOM/AX beyond node counts would yield non-zero predictive PMI on deterministic vs correlated non-deterministic SPAs.

**Do not assume (explicitly unsafe):**
- C-MEAS-VALID or C-FRESHNESS are VALIDATED or PRODUCT_CORE — audit status REVISE, ceiling single-host loopback EXPERIMENTAL only, single viewport 1280×720, body 31-117B, filtered header set.
- Degenerate CIs [1.0,1.0]/[0.0,0.0] width 0 imply high precision — they are deterministic existence with effective distinct N=1, not variance.
- Sticky TN 0.960 proves URL-bound affinity or sticky alternatives to shared store — sticky used hash $remote_addr not $request_uri and mirrored sessions, so affinity confounded.
- Shared SQLite WAL implies multi-host Redis, paid CDN HIT/STALE/SWR, TLS/HTTP2/QUIC, or BrowserGym DOM beyond HTTP triple — explicitly SUPERSEDED/NOT_TESTED.
- Loopback results generalize to production SPAs with correlated DOM/state, multi-step forms, or LLM inheritance/product economics — not measured.
- 17 missing worker_ids or 396 vs 520 nominal lines are negligible for tail claims — must gate harness and restore N=20.
- Structural r near 0 or hardcoded TOST — prior MEASUREMENT_INVALID synthetic TOST/TN artifacts remain invalid; current r validly non-zero and falsified.
- True-negative rate can be computed as 1-|mean_invalid-mean_valid| — inverted formula rewards indistinguishability; correct is P(bc<=0.05|valid) with Wilson CI.

This CONTINUE does not repeat paid CDN or synthetic localhost magnitude; it is the real-HTTP rerun fixing all 4 audit required_fixes.

---

## 4. Server Design

### 4.1 Testbed Architecture (two substrates, same Flask app base, real HTTP mandatory + HS256 fix + 4 validity fixes)

```
Flask 3.1.3 + PyJWT 2.14.0 HS256 shared-secret + SQLite WAL (shared vs per-node vs sticky-url) + optional Redis
  ├── POST /admin/set_body_variant   (admin JWT, writes body_config/content_variant, COMMIT, BYPASS cache, SELECT verification)
  ├── POST /admin/set_headers        (admin JWT, writes header_config, COMMIT, BYPASS)
  ├── POST /admin/set_role           (UPDATE users SET role, COMMIT, BYPASS)
  ├── POST /admin/invalidate_session (DELETE sessions, COMMIT, BYPASS, SELECT verification)
  ├── GET  /resource                 (authenticated GET, status+JSON body+filtered headers, Cache-Control public max-age=5 / no-store, ETag-SHA256, If-None-Match ->304, X-Worker-Pid on ALL statuses including 401)
  ├── GET  /api/profile              (C-FRESHNESS endpoint, profile, cacheable)
  ├── GET  /api/data_list            (C-FRESHNESS endpoint, data_list, cacheable)
  ├── GET  /api/session/status       (C-FRESHNESS endpoint, session_status, session-dependent)
  └── GET  /health                   (nginx+gunicorn health gate, returns 200 with X-Worker-Pid)
  └── GET  /protected                (smoke)
  └── POST /admin/state snapshot     (SELECT count(*) FROM sessions for batch_state_log)

Substrate D (distributed C-FRESHNESS, primary) — REAL HTTP + HS256 + fixes:
  Origin: gunicorn 23.0.0 2x sync --workers 2 --bind 127.0.0.1:19860 --timeout 30
       + nginx 1.24.0 127.0.0.1:19851 proxy_pass http://gunicorn_upstream
         upstream gunicorn_upstream { server 127.0.0.1:19860; }  (round-robin)
         Alternative upstream for B-STICKY-URL: hash $request_uri consistent; server 127.0.0.1:19860;  (URL-bound sticky)
  DB modes (real) + HS256 shared-secret:
    B-PER-NODE: each worker isolated temp file /tmp/spider-pernode-<worker>.db (WAL, not shared) with SAME HS256 secret but isolated sessions — real nginx round-robin, health-gated, status-free structural, de-confounded scheduling, expected TN~0.667
    B-SHARED-STORE: single shared file /tmp/spider-runtime-35860330078/shared.db (WAL, shared across workers, check_same_thread=False, same HS256 secret shared) — real nginx round-robin, health-gated, status-free, de-confounded, expected TN>=0.85 and orthogonality restored
    B-STICKY-URL: per-node DB files WITHOUT replication (replicate_session_to_workers=False) with hash $request_uri consistent — real nginx URL-bound, health-gated, status-free, de-confounded, expected TN>=0.85 if affinity suffices, >90% skew
  Auth fix: Flask validates JWT via pyjwt.decode(Bearer token, HS256_SECRET, algorithms=['HS256']) then SELECT sessions WHERE session_id=payload sid; NOT raw Bearer string lookup. ETag/If-None-Match and X-Worker-Pid emitted on ALL statuses including 401.
  Structural fix: structural_signal = hash(decompressed_body_bytes) only (sha256 or %10000), grep-verified no status prefix.
  Scheduling fix: body_variant chosen via random.choice independent of drift condition with logged seed, independence verified via |r|<0.30.
  Health gate: wait_http loops GET http://127.0.0.1:19851/health via nginx until 200 with X-Worker-Pid, max 30s before sampling.

Substrate B (browser C-MEAS-VALID) — REAL BROWSER FETCHES at N=20:
  Same origin gunicorn+nginx as above (shared-store mode for origin, body_config/header_config tables, body variants 31B/32B/33B/35B/70B/117B)
  + AgentLab 0.4.2 (pip install agentlab==0.4.2) + Playwright chromium at 1280x720
    - Browser contexts: browser.newContext({viewport:{width:1280,height:720}})
    - Viewport verified per page: page.viewportSize().width==1280 && height==720
    - CDP session per /resource page: cdpSession = await page.context().newCDPSession(page); await cdpSession.send('Accessibility.getFullAXTree')
    - AX capture: Accessibility.getFullAXTree per /resource page (AX nodes count) — NOT only index
    - DOM enumeration: await page.evaluate(() => document.querySelectorAll('*').length) per /resource page
    - HTTP triple capture: await page.request.get('http://127.0.0.1:19851/resource') or page.evaluate(()=>fetch('/resource').then(r=>r.text())) with decompressed body and headers + fingerprint triple identical to direct pipeline at N=20 per state
    - Direct sanity: requests.get via same nginx for comparison (separate artifact, not relabeled)
```

`body_config` variant `A {"data":"hello","version":1}` 31B SHA `d0ca833f`; `header_config` fixed `Cache-Control:max-age=3600, ETag:W/"fixed-aaa-111", Vary:Accept-Encoding`. All body-only use same valid HS256 JWT; header-only varied. Health gate ensures 1200/1200 valid lines.

**Distributed harness real HTTP + HS256 + fixes:** 8 co-occurring conditions (drift: permission_boundary, session_invalidation, signing_key_rotation, token_expiry × cache_enabled/disabled) plus 4 noise-only conditions, each with paired behavioral+structural samples where `structural` is status-free body hash, `body_variant` randomized independent of drift, real ETag/If-None-Match exercised to generate 304 (~33% when cache_enabled). Total nominal 1200 paired samples via **real nginx round-robin health-gated** to achieve n_non304≥800 after exclusion, health-gated 0 missing. Each sample logs `X-Worker-Pid` distribution and `is_304` boolean from real response status plus `body_variant` and `scheduling_seed`.

**Browser harness real fetches at N=20:** Body states `A 31B, A1 32B 1B diff {"data":"hello!","version":1}, A2 33B 2B diff, A3 35B 4B diff, B 70B 39B, C 117B 86B` and header states `E combined, CC_small max-age=3601 1s diff, CC_large max-age=0, ETag_small W/"fixed-aaa-112" 1char, ETag_large W/"changed-bbb-222", SC_small session=abc, SC_large absent->present, Vary_small Accept-Encoding vs Accept-Encoding,Origin`. **Direct via `requests` through nginx and browser via `page.request.get` through nginx** (both decompressed, both filtered identically) at **N=20 per state** (browser gradients n_a=20 n_b=20, not 3-4) with **B=1000 bootstraps**.

### 4.2 Body and Header States for Browser Part

| State | Body JSON (sort_keys=True) | body_len decomp | Status | Filtered Headers (non-CLEN) |
|-------|----------------------------|-----------------|--------|------------------------------|
| **A baseline** | `{"data":"hello","version":1}` | 31 | 200 | `Cache-Control:max-age=3600, ETag:W/"fixed-aaa-111", Vary:Accept-Encoding, Content-Type:application/json, CLEN 31` |
| **A1 grad 1B** | `{"data":"hello!","version":1}` | 32 | 200 | identical to A |
| **A2 grad 2B** | `{"data":"hello!!","version":1}` | 33 | 200 | identical to A |
| **A3 grad 4B** | `{"data":"hello!!!!","version":1}` | 35 | 200 | identical |
| **B reader** | `{"data":"hello","items":["a","b"],"role":"reader","version":1}` | 70 | 200 | identical to A |
| **C admin** | `{"admin_note":"sensitive:42","count":42,...}` | 117 | 200 | identical to A |
| **E combined** | `{"data":"hello","version":1}` 31B | 31 | 200 | `Cache-Control:max-age=0,must-revalidate, ETag:W/"changed-bbb-222", Set-Cookie:session=xyz; Path=/; HttpOnly, Vary:Accept-Encoding,Origin, CLEN 31` |
| **Isolations** | same 31B | 31 | 200 | CC_small `max-age=3601` vs CC_large `max-age=0`; ETag_small `W/"fixed-aaa-112"` 1char vs ETag_large `changed`; SC_small `session=abc` vs SC_large absent->present; Vary_small `Accept-Encoding` vs `Accept-Encoding,Origin` |

Gradient bodies SHA must be distinct; decompressed. CLEN must equal body_len after decompression. Structural for orthogonality uses hash(body) only.

---

## 5. Measurement

### 5.1 Observation Vector

**Distributed part (per paired sample, real HTTP + HS256 + fixes):**
- `endpoint` (profile/data_list/session_status), `cache_enabled` bool, `status` int, `body_bytes` + `body_sha256` + `body_len` + `Content-Length` header, `headers_filtered_json`, `headers_no_clen_json`, `ETag`, `Cache-Control`, `worker_id` (`X-Worker-Pid` from real nginx response, on ALL statuses, 0 missing required), `behavioral_composite` (graded session_status_check + auth delta, true-negative P(bc<=0.05|valid)), `structural` (status-free hash(body)%10000 or Jaccard — WITHOUT status prefix, verified), `body_variant` (A/A1/A2/A3/B/C), `scheduling_seed`, `drift_condition`, `is_304` bool (real status 304), `timestamp` (real, not clustered), `db_path` (shared vs per-node vs sticky-url), `jwt_valid` bool, `hs256_verified` bool, `health_gated` bool

**Browser part (per request via direct or Playwright, real HTTP at N=20):**
- `state`, `status` int, `body_bytes` decompressed + `body_sha256` + `body_len` + `Content-Length`, `Content-Encoding`, `headers_filtered_json`, `headers_raw_json`, `headers_no_clen_json`, `fingerprint_full/status/body/headers/headers_no_clen` (SHA256), `worker_id`, `cdn_cache_status`, `ax_nodes` (count from Accessibility.getFullAXTree **on that /resource page**), `dom_nodes` (querySelectorAll length **on that /resource page**), `viewport` ({width:1280,height:720}), `pc_health` derived, `timestamp`, `concurrency` flag, `fetch_method` (direct vs browser_page_request), `effective_distinct_n` helper

### 5.2 Metrics (stable names for AUDIT/DIRECTOR — identical to prior for recomputation plus fixes)

**Distributed C-FRESHNESS (real HTTP + HS256 + fixes):**
- `freshness_c1_tn_mean` (shared-store, status-free, de-confounded, health-gated, correct formula)
- `freshness_c1_tn_session_status`, `freshness_c1_tn_profile`, `freshness_c1_tn_data_list` (Wilson 95% CI per endpoint)
- `freshness_c1_tn_per_node_mean` (baseline B-PER-NODE health-gated, expected ~0.667)
- `freshness_c1_tn_sticky_url_mean` (B-STICKY-URL without replication, health-gated, expected >=0.85 if affinity suffices)
- `freshness_c1_tn_sticky_url_skew` (max worker share >0.90)
- `freshness_n_non304` (shared-store count after real 304 exclusion, must be >=800, with 0 missing)
- `freshness_n_total`, `freshness_n_304`, `freshness_n_missing_worker` (must be 0)
- `freshness_stratified_r` (status-free pooled Fisher z stratified, health-gated, de-confounded)
- `freshness_stratified_r_ci_lo`, `freshness_stratified_r_ci_hi`, `freshness_tost_p_upper`, `freshness_tost_pass` (delta 0.15)
- `freshness_pooled_r`, `freshness_b_flask_only_r` (baseline)
- `freshness_fp_noise` (noise-only FP health-gated, status-free)
- `freshness_c2_variance_pass` (8/8 std>0, real, status-free)
- `freshness_worker_distribution_shared` (per worker counts, health-gated real)
- `freshness_worker_distribution_per_node` (real, ~600/600 balanced)
- `freshness_worker_distribution_sticky_url` (real, skewed >90% per sticky URL)
- `freshness_hs256_valid_success_rate` (must be >=0.90)
- `freshness_structural_status_prefix_present` (bool must be false)
- `freshness_scheduling_confound_r` (|r| between body_variant and drift, must be <0.30)
- `freshness_valid_vs_invalid_bc_means` (for audit)

**Browser C-MEAS-VALID (real browser fetches at N=20):**
- `bg_provision_ok`, `bg_agentlab_version`, `bg_agentlab_0143_absent`, `bg_playwright_version`, `bg_playwright_viewport`, `bg_ax_nodes_median` (**on /resource**), `bg_ax_nodes_per_page`, `bg_pc_health_pct` (**on /resource**), `bg_dom_nodes_median` (**on /resource**), `bg_dom_nodes_range_ok`
- `browser_body_AvsC_full`, `browser_body_AvsC_status`, `browser_body_AvsC_body`, `browser_body_AvsC_headers_no_clen` + CI `[lo,hi]` `width` `degenerate` `effective_distinct_n` (via real Playwright at N=20)
- `browser_header_AvsE_full`, `browser_header_AvsE_headers_only`, `browser_header_AvsE_headers_no_clen` + CI at N=20
- `direct_body_AvsC_full` (sanity via direct at N=20), `direct_header_AvsE_full`
- `browser_null_body_full`, `browser_null_header_full`, `browser_null_403_full`, `browser_null_401_full` + CI at N=20
- `browser_gradient_1B_full`, `browser_gradient_2B_full`, `browser_gradient_4B_full`, `browser_gradient_39B_full` (AvsB), `browser_gradient_86B_full` (AvsC) + per-measure CI/width/degenerate/effective_distinct_n via both direct and browser at N=20
- `browser_gradient_CC_small_full`, `browser_gradient_CC_large_full`, `browser_gradient_ETag_small_full`, `browser_gradient_ETag_large_full`, `browser_gradient_SC_small_full`, `browser_gradient_SC_large_full`, `browser_gradient_Vary_small_full` + CI at N=20
- `direct_gradient_*` same via direct fetch for comparison

All Jaccard `1 - |A∩B|/|A∪B|`, bootstrap `B=1000` for browser part at N=20; Fisher z for distributed r. Health gate 0 missing disclosed.

### 5.3 Baselines

| ID | Expected distributed (real HTTP + HS256 + fixes, health-gated) | Expected browser (real Playwright N=20 to /resource) | Purpose |
|----|---------------------|------------------|---------|
| B-PER-NODE | TN~0.667 fail, n_non304 nominal but C1 fails (real, HS256 same secret but isolated DB, status-free, de-confounded, 0 missing) | — | Proves failure is replication, HS256 alone insufficient |
| B-SHARED-STORE | TN≥0.85 pass, n_non304≥800, r TOST within 0.15 health-gated status-free de-confounded (real, HS256+shared WAL) | — | Primary fix: shared store + fixes |
| B-STICKY-URL | TN≥0.85 exploratory >90% skew health-gated status-free de-confounded without replication (real URL-bound hash $request_uri) | — | Tests affinity alone vs shared store |
| B-STATUS-ONLY | — | 0.0 on 200 vs200 at N=20 (real both) | Status isolation |
| B-BODY-ONLY | — | 1.0 body-only, 0.0 header-only at N=20 (real both) | Body signal |
| B-HEADERS-ONLY | — | 1.0 via CLEN body-only, 1.0 header-only at N=20 (real both) | Body-correlated vs independent |
| B-HEADERS-NO-CLEN | — | 0.0 body-only, 1.0 header-only isolations at N=20 (real both) | Independent header |

### 5.4 Sample Size

- Distributed: **N=1200 paired samples nominal via real nginx round-robin health-gated + HS256 + fixes** (8 co-occurring conditions × ~120 each + 4 noise-only ×60 + 120 extra) targeting **n_non304≥800 after real 304 exclusion** (cache_enabled 50% × 33% real 304 = 16.5% overall 304 → 1002 non-304 at N=1200) with **0 missing X-Worker-Pid/status None** via health gate. Prior N=480 gave 684 non-304; scaling to 1200 with real 304 path and health gate ensures ≥800. Per-batch SELECT verification and X-Worker-Pid logged per sample. HS256 valid JWTs must achieve 200 on ≥90% (270/300). **Fix verification:** `structural_status_prefix_present==false` and `scheduling_confound_r<0.30` logged.
- Browser: **N=20 per state nominal via direct through nginx + via real Playwright 1280×720 to /resource** (body 60+gradient 60+header 40+isolations 140+nulls 80+classic 80 = ~460 distinct fetches ×2 arms = ~520 raw_observations.jsonl lines with ax/dom per /resource page at N=20). Concurrency 4 for null and at least one body/header branch. Gradient per-value CI B=1000 with N=20 enables non-degenerate ordering. Health-gated distributed and N=20 browser both via real HTTP.

---

## 6. Decision Rule (Frozen — no post-hoc weakening, real HTTP + HS256 + 4 fixes required)

**SUPPORTS** (both substrates close block with fixes) iff **ALL** mandatory conditions hold with validity checks passing and **no synthetic data** and **HS256 correctly validates** and **status-free** and **de-confounded** and **health gate 0 missing**:

1. **C1-FRESHNESS (distributed TN, real HTTP + HS256 + fixes, health-gated):** shared-store arm **mean TN ≥ 0.85** across 3 endpoints (session_status, profile, data_list) with each Wilson 95% lower > 0.75 and **session_status individually ≥ 0.85**, computed as `P(behavioral_composite<=0.05 | valid JWT)` with status-free structural and de-confounded scheduling and health gate 0 missing, while **B-PER-NODE baseline mean TN < 0.85** (expected ~0.667, session_status 0.0) replicating failure via real HTTP + same HS256 secret + fixes — proves shared store + fixes not tautological. Must be measured via real nginx round-robin health-gated with 4-concurrency, SEED 44, X-Worker-Pid distribution verified, and `hs256_valid_success_rate >=0.90` and `structural_status_prefix_present==false` and `scheduling_confound_r<0.30`.

2. **C2-FRESHNESS (power, real 304, health-gated):** **n_non304 ≥ 800** after excluding **real** 304 status (counted from `raw_freshness_observations.jsonl` where `is_304==false` via real If-None-Match/ETag, stratified across 3 endpoints, with per-batch SELECT verification) with **0 missing X-Worker-Pid and 0 status None**. If n_non304 <800 but C1 passes, still **MEASUREMENT_INVALID** for power not falsification.

3. **C3-FRESHNESS (orthogonality, real, status-free, de-confounded, health-gated):** stratified pooled Pearson **r equivalence TOST within delta=0.15**: **95% Fisher z CI upper < 0.15** AND **TOST p_upper < 0.05** (and CI lower > -0.15), **pooled |r| < 0.15**, with **8/8 conditions variance std>0** for both behavioral and structural (structural status-free) signals and **noise FP ≤ 0.15** (C4) on shared-store arm via real HTTP + fixes. If C3 fails where validity passes (status-free, de-confounded, 0 missing), orthogonality is **FALSIFIED-IN-SETTING** (not rescued by removing confound).

4. **C4-FRESHNESS (noise, real, status-free):** noise-only FP ≤ 0.15 (Wilson upper) on shared-store via real HTTP + fixes, status-free.

5. **C5-BROWSER-PROVISION (real Playwright N=20 to /resource):** `AgentLab 0.4.2` importable, `0.14.3` correctly absent, `Playwright` viewport 1280×720 verified per /resource page, **CDP AX nodes median >10 on /resource pages** and **PC-HEALTH ≥ 80% on /resource pages** and **DOM nodes 21–82 on /resource pages** via real Playwright at N=20.

6. **C6-BROWSER-DISCRIMINATION (real browser fetch N=20 to /resource):** browser body-only **AvsC full>0.5** expect 1.0 with status 0 headers-no-CLEN 0 and browser header-only **AvsE full>0.5** headers-only 1.0 status 0 body 0 CLEN 31==31 via **real Playwright at N=20** (direct sanity also 1.0 at N=20). Nulls concurrent each full 0.0 CI contains 0.0 point ≤0.05 at N=20.

**Gradient reporting mandatory (exploratory not gating SUPPORTS but required for high information at N=20):**
- `G1_BODY_MAGNITUDE`: for each body gradient `A vs A1 1B, A vs A2 2B, A vs A3 4B, AvsB 39B, AvsC 86B` report Jaccard full/body/headers/headers-no-CLEN and CI [lo,hi] width degenerate effective_distinct_n via both direct and browser at N=20.
- `G2_HEADER_MAGNITUDE`: for each header gradient `CC_small 3601 1s, CC_large 0, ETag_small 1char, ETag_large changed, SC_small, SC_large, Vary_small` same reporting via both at N=20 — enables most fragile header ordering beyond degenerate ceiling. If gradients remain degenerate at N=20, ordering remains unknown but correctly powered.

**Sticky exploratory (not gating SUPPORTS but high-information, health-gated, status-free, without replication):**
- `E4_STICKY_URL`: sticky URL-bound `hash $request_uri consistent` without replicate_session_to_workers TN `>=0.85` with >90% skew vs per-node 0.667; if sticky fails where validity passes (health gate 0 missing, status-free, real HTTP, without mirroring) => sticky FALSIFIED (affinity alone insufficient).

If any C1–C6 fails where validity checks pass (health gate 0 missing, status-free, de-confounded, real HTTP, HS256 correct, N=20) => **FALSIFIED-IN-SETTING** bounded to failing branch. If shared-store C3 fails (|r|>=0.15) even status-free/de-confounded => orthogonality **FALSIFIED-IN-SETTING** not truncated. If browser provision fails but distributed passes => **MIXED**. If C2 power fails (<800) with C1/C3 passing => **MEASUREMENT_INVALID**. If HS256 valid JWTs still all 401 (0/300) => **MEASUREMENT_INVALID HS256_VALIDATION_STILL_REJECTS_ALL**. **Any status prefix still present, confounded scheduling detected (|r|>0.30), synthetic generation, inverted TN formula, hardcoded TOST, or relabeled direct-as-browser, or health gate missing (>0 missing) triggers MEASUREMENT_INVALID** per frozen falsifier. Infrastructure-unavailable branches map to **MEASUREMENT_INVALID** not falsification: `gunicorn/nginx unavailable`, `shared store file creation fails`, `Playwright not installable`, `CDP capture not available on /resource pages`, `AgentLab 0.4.2 not on PyPI` => browser branch MEASUREMENT_INVALID while distributed can still be decided. **Paid CDN absent is NOT invalidity** per SUPERSEDE. Degenerate CI expected deterministic when set size 1 at N=20 for identical bodies but now correctly powered.

**Exploratory (not gating):**
- `E1_CI_NONDEGENERATE`: width 0 vs >0 per comparison at N=20.
- `E2_FOLDING`: case/whitespace/order folded E variant full 0.0 if normalized.
- `E3_EDGE_VISIBILITY`: X-Worker-Pid distribution per store mode (real, health-gated).
- `E4_STICKY_URL`: sticky URL-bound without replication TN and distribution skew vs shared-store.

---

## 7. Controls Summary

| Control | ID | Type | Threshold (real HTTP + HS256 + fixes, health-gated, N=20) | Evidence |
|---------|----|------|-----------|----------|
| Distributed TN shared | C1-FRESHNESS | positive | `mean ≥0.85` Wilson lower >0.75 session_status ≥0.85 `P(bc<=0.05|valid)` `hs256_valid_success_rate>=0.90` `status_prefix false` `scheduling |r|<0.30` `0 missing` | TN per endpoint via real nginx shared store + fixes |
| Distributed TN per-node baseline | B-PER-NODE | negative baseline | `mean ~0.667 <0.85` session_status 0.0 (real + HS256 same secret + fixes + 0 missing) | Replicates failure via real nginx |
| Distributed TN sticky URL | E4_STICKY_URL | positive exploratory | `mean ≥0.85` `>90% skew` `hash $request_uri` without replication, `0 missing` | TN/distribution sticky URL-bound isolated |
| Power n_non304 | C2-FRESHNESS | validity/power | `≥800` after real 304 exclusion + `0 missing` | Count from raw_freshness real is_304==false |
| Orthogonality stratified r | C3-FRESHNESS | equivalence TOST status-free de-confounded | `CI upper <0.15` `p_upper<0.05` `|r|<0.15` 8/8 variance `scheduling |r|<0.30` | Fisher z stratified real status-free |
| Noise FP | C4-FRESHNESS | null | `≤0.15` status-free real `0 missing` | Noise-only FP real |
| Browser provision | C5-BROWSER | positive | AgentLab 0.4.2, 0.14.3 absent, viewport 1280×720, AX>10 median **on /resource** PC-HEALTH≥80% **on /resource** DOM 21-82 **at N=20** | pip show, CDP per /resource page at N=20 |
| Browser body discrimination | C6a | positive+isolation at N=20 | `full>0.5` `status 0.0` `headers-no-CLEN 0.0` via **real Playwright N=20** | Jaccard via Playwright |
| Browser header discrimination | C6b | positive+isolation at N=20 | `full>0.5 headers-only 1.0` `status/body 0.0` `CLEN 31==31` via **real Playwright N=20** | Jaccard via Playwright |
| Browser null | C6c | null at N=20 | `full 0.0` CI contains 0 ≤0.05 (real, N=20) | Null Jaccard 0 real N=20 |
| Body gradient | G1 | diagnostic at N=20 | report per magnitude 1B/2B/4B/39B/86B +CI width/degenerate at N=20 | Gradient metrics real N=20 |
| Header gradient | G2 | diagnostic at N=20 | report CC_small/large ETag_small/large SC/Vary +CI at N=20 | Gradient metrics real N=20 |
| Health gate | validity | check | `0 missing X-Worker-Pid` `0 status None` across 1200 | X-Worker-Pid per observation |
| Per-batch SELECT | validity | check | ≥27 lines distinct timestamps, COMMIT verified, `structural_status_prefix false` | batch_state_log.jsonl |
| Scheduling independence | validity | check | `scheduling_confound_r<0.30` (body_variant vs drift) | per-observation body_variant logs |
| HS256 validation | validity | check | valid JWT `P(200|valid)>=0.90`, status-free structural | 300 valid JWT success rate |
| Synthetic detection | validity | check | no np.random/hardcoded tn_correct/forced 304/status prefix /relabeled | audit grep |

---

## 8. Validity Threats and Mitigations (real HTTP + HS256 + 4 fixes focus)

1. **HS256 shared-secret not actually shared or still raw Bearer lookup:** Mitigate by configuring same `HS256_SECRET` env for both workers, implementing `pyjwt.decode(token, secret, algorithms=['HS256'])` then `SELECT sessions WHERE id=decoded.sid`, logging secret hash, verifying `hs256_valid_success_rate >=0.90` via real HTTP (300 valid JWTs must yield 200). If 0/300 fail or TN inverted, MEASUREMENT_INVALID.

2. **Shared store file not actually shared or synthetic or status prefix remains:** Mitigate by creating shared file at `/tmp/spider-runtime-35860330078/shared.db` before gunicorn start, verifying both workers report same `SELECT count(*) FROM sessions` via real HTTP, logging DB path per observation, checking `batch_state_log.jsonl` has ≥27 distinct timestamps and grep `run_experiment.py` for `f\"{status}|` — if found, STATUS_PREFIX_STILL_PRESENT invalidity.

3. **Scheduling confound (body_variant cycling correlated with drift):** Mitigate by randomizing body_variant per request independent of drift condition with `random.choice` and `scheduling_seed=44` sub-seeds, logging per-observation body_variant, recomputing `scheduling_confound_r` between body_variant hash and behavioral bc; if |r|>=0.30, CONFOUND_SCHEDULING_DETECTED invalidity. Prior harness had |r| 0.35-0.62.

4. **Health gate missing (prior 17/1200 status None/X-Worker-Pid missing):** Mitigate by health-gating startup: loop `curl http://127.0.0.1:19851/health` via nginx until 200 with `X-Worker-Pid` for up to 30s before sampling; verify 0 missing across all 1200 lines; if >0 missing, HEALTH_GATE_FAILED invalidity (not falsification) and requires rerun.

5. **Per-node baseline not isolating or not real HTTP:** Mitigate by using distinct temp files per worker via env `SPIDER_DB_PATH_PER_WORKER` and verifying different paths per worker via real X-Worker-Pid; ensure all samples real HTTP through nginx (not direct to gunicorn bypass). Log per-node vs shared vs sticky-url paths. Sticky-url must have `replicate_session_to_workers=False` verified via code.

6. **n_non304 <800 or not exercising real 304 or missing X-Worker-Pid on 401:** Mitigate by N=1200 and exercising real 304 only when cache_enabled and If-None-Match sent to nginx; verify per request `is_304` from real status 304 and X-Worker-Pid on ALL statuses including 401 (prior omitted on 401). Health gate ensures 1200/1200 valid.

7. **Structural–behavioral shared-variable confound (status prefix) or inverted TN:** Mitigate by ensuring structural excludes status (status-free hash) and computing TN as `P(bc<=0.05|valid)` with Wilson CI — inverted formula forbidden (audit grep `1-abs(mean_invalid-mean_valid)`). Status-free verified via grep and recomputation r with/without status.

8. **AgentLab 0.4.2 not on PyPI / Playwright install fails / relabeled direct:** Mitigate by `pip install agentlab==0.4.2` with fallback to `browsergym`, log version; `npx playwright install chromium --with-deps` conditional; forbid `browser_fetch` calling `requests.get` — must be `page.request.get` or `fetch`; if fails mark MEASUREMENT_INVALID for browser branch and still decide distributed branch. Remove synthetic fallback.

9. **CDP AX capture fails or only on index / gradient underpowered (n=3-4):** Mitigate by using `cdpSession.send('Accessibility.getFullAXTree')` **per /resource page** with fallback to `page.accessibility.snapshot()`; log AX per /resource page at N=20; if 0 nodes on /resource pages mark CDP_AX_CAPTURE_FAILED; ensure browser gradients use N=20 per state (n_a==20) via checks; if n=3-4 as prior, GRADIENT_UNDERPOWERED invalidity for ordering (still evaluable for discrimination).

10. **Decompression CLEN mismatch (brotli/gzip) or not verified for browser at N=20:** Auto-decompress before SHA for both direct and browser; compare decompressed_body_len to body_len; log Content-Encoding per observation at N=20; verify CLEN==body_len for both.

11. **Degenerate CI misread or synthetic timestamp clustering or hardcoded TOST:** Disclose effective_distinct_n, treat degenerate at N=20 as deterministic (if still 1.0, indicates true determinism not underpowering since n=20); G1/G2 explicitly measure width at N=20 with B=1000; check timestamp not clustered within 1-2ms; TOST must be computed from Fisher z with real n, not hardcoded.

12. **Port collision / stale server / synthetic worker_ids / sticky misconfiguration:** Discover free ports, fresh DB, kill on exit; verify X-Worker-Pid are real gunicorn pids not simulated and distribution balanced for round-robin vs skewed >90% for sticky-url via `write_nginx_conf` hash $request_uri consistent; ensure sticky-url does not mirror sessions.

13. **Paid CDN absent:** Explicitly NOT gating; do not trigger MEASUREMENT_INVALID (SUPERSEDED).

14. **Threshold confusion (≥0.85 vs >0.5) or Wilson lower vs point:** C1 uses ≥0.85 mean and Wilson lower >0.75; browser C6 uses >0.5; document exact value+CI.

15. **Sticky URL-bound vs round-robin vs ip_hash confusion:** Document sticky config (`hash $request_uri consistent` without replication) and verify distribution skewed >90% for sticky-url vs balanced for round-robin via real X-Worker-Pid at N=1200 health-gated.

---

## 9. Consequences

**Positive (all C1–C6 pass health-gated status-free de-confounded at N=20, gradients reported, sticky optional):** Both live-substrate blocks closed with Director-required fixes via valid measurement. Distributed TN≥0.85 with n_non304≥800 and orthogonality |r|<0.15 TOST status-free de-confounded health-gated proves shared WAL + HS256 shared-secret plus scheduling/health fixes restore both detection and independence that were falsified at -0.357/+0.62; sticky URL-bound without replication achieving TN≥0.85 proves affinity alternative. BrowserGym/AgentLab 0.4.2 + Playwright 1280×720 with AX>10 PC-HEALTH≥80% DOM 21-82 on /resource pages at N=20 via real browser fetches provisions live browser substrate where HTTP fingerprint discrimination remains non-degenerate in disclosure (per-value CC/ETag/CLEN gradients with B=1000 CIs at N=20) enabling sensitivity ordering beyond prior degenerate ceiling. Unblocks Graph distributed delta-repair and freshness guards on 2-node gunicorn+nginx and Intel Gate0 harvest and Physics live replication. Claim ceiling expands from single-host loopback EXPERIMENTAL to **distributed shared-store + sticky HS256 URL-bound + live browser EXPERIMENTAL (real HTTP, corrected orthogonality, N=20)**; does NOT promote to VALIDATED or PRODUCT_CORE (still bounded to single-host 2-worker simulation, filtered header set, body 31-117B, AgentLab 0.4.2, single viewport, no paid CDN, no multi-host Redis).

**Negative (any C1–C6 fails where validity passes health-gated status-free de-confounded N=20):** Either distributed shared-store fails to restore TN≥0.85/n≥800/orthogonality even status-free de-confounded health-gated, or sticky URL-bound without replication fails TN≥0.85, or Browser provision/discrimination fails at N=20 via valid measurement. Proves per-node failure not fixable by trivial shared file/sticky or orthogonality not restorable with this harness, or affinity alone insufficient, or browser layer not viable. Bounds C-MEAS-VALID and C-FRESHNESS to single-host loopback EXPERIMENTAL only, prevents false VALIDATED promotion, forces redesign (true Redis/multi-host or alternative orthogonality metric or redesigned scheduling or Playwright install) before scaling. Negative still requires gradient reporting at N=20 to diagnose most fragile magnitude.

**MEASUREMENT_INVALID (synthetic or status prefix present or confounded scheduling or health gate missing or HS256 still rejecting all valid or provision failure or gradients underpowered):** Prior packet's falsified orthogonality and sticky misconfiguration map to parent MIXED; new status prefix, confounded scheduling, relabeled direct, inverted TN, hardcoded TOST, 17 missing worker_ids map here via 4 required_fixes. No ceiling change; requires rerun with real HTTP + correct TN formula per this prereg. Distinguishes measurement failure from scientific falsification; audit will flag `STATUS_PREFIX_STILL_PRESENT`, `CONFOUND_SCHEDULING_DETECTED`, `HEALTH_GATE_FAILED`, `GRADIENT_UNDERPOWERED`, `SYNTHETIC_DATA_DETECTED`, `BROWSER_FETCH_RELABELED`, `HS256_VALIDATION_STILL_REJECTS_ALL`, `COMMIT_NOT_VERIFIED`.

Both valid outcomes are high-information and will be consumed by Codex as the distributed+browser promotion decision required before any VALIDATED or PRODUCT_CORE claim.

---

## 10. What is NOT Tested (Scope Boundaries)

- **Paid CDN HIT/STALE/SWR/SIE/304 beyond nginx loopback** — explicitly SUPERSEDED per Director, not tested (no credentials, 0% HIT prior, zero VOI).
- Multi-host **Redis cluster** or SQLite multi-node replication beyond single-host 2-worker WAL shared file at `/tmp/spider-runtime-35860330078/shared.db` / URL-bound sticky without replication — single-host tested; true distributed multi-host remains unresolved unless Redis available.
- **TLS/HTTP2/QUIC** beyond plain HTTP 127.0.0.1 termination.
- Browser **DOM/AX beyond HTTP triple** (rendered text hash, accessibility tree beyond node counts, visual layout, computed style) — AX/DOM node counts per /resource page only at N=20.
- Body sizes beyond **31–117B JSON with sort_keys=True** — CLEN==body_len holds for these bodies at N=20.
- End-to-end **cost/latency/tokens/LLM inheritance/cross-site holdout** — not measured (runtime substrate only).
- Full **304 lifecycle beyond single HIT** (`STALE/SWR`) best-effort via `Age`/`ETag` on origin.
- **HS256 vs RS256 beyond HS256 shared-secret** — RS256 tested only if available; focus HS256 shared-secret per Director.

---

## 11. Execution Checklist for EXECUTE

- [ ] Implement `run_experiment.py` with fingerprint functions byte-identical to `research/experiments/EXP-RUNTIME-35764329925/run_experiment.py:compute_fingerprint` (status_only, body_only, headers_only, headers_no_clen), sorted lowercased filtered headers, EXCLUDED {Date,Server,X-Request-Id,CF-RAY,CF-Cache-Status,X-Cache,Age} plus X-Worker-Pid, decompression via `response.content` auto-decompressed for direct and via `page.request` body for browser; ensure audit recomputation 0 mismatches and **no synthetic generation code**, **no inverted TN formula** (use `P(bc<=0.05|valid)` + Wilson), **no hardcoded TOST constants**, **no status prefix in structural** (grep verify `hash(body)` only).
- [ ] Fix HS256 auth plumbing: Flask validates `Authorization: Bearer <JWT>` via `pyjwt.decode(jwt, HS256_SECRET, algorithms=['HS256'])` then `SELECT sessions WHERE session_id=payload['sid']`; verify `hs256_valid_success_rate >=0.90` (300 valid JWTs yield 200). Emit `X-Worker-Pid` and `ETag` on ALL statuses including 401 so round-robin and 304 verifiable. Delete prior raw string lookup and inverted TN.
- [ ] Implement status-free structural and de-confounded scheduling: `structural_signal = sha256(decompressed_body_bytes)` or `hash(body)%10000` without status; randomize `body_variant` per request via `random.Random(scheduling_seed + idx).choice(variants)` independent of drift condition; log `scheduling_confound_r` and ensure <0.30.
- [ ] Implement health-gated startup: `wait_for_nginx()` loops `GET http://127.0.0.1:19851/health` via nginx until 200 with `X-Worker-Pid` present up to 30s; sample only after healthy; verify `raw_freshness_*.jsonl` has 0 lines with `worker_id==None` or `status==None`; if >0, HEALTH_GATE_FAILED.
- [ ] Implement distributed harness with **real HTTP only + HS256 + fixes**: reuse research/harness C-FRESHNESS logic (behavioral graded session_status_check, structural status-free, paired samples, real If-None-Match 304) with DB modes B-PER-NODE (isolated files + same HS256 secret) vs B-SHARED-STORE (shared file at /tmp/spider-runtime-35860330078/shared.db WAL + HS256 shared-secret) vs B-STICKY-URL (nginx `hash $request_uri consistent` without replicate_session_to_workers). Seed 44, jitter 50-150ms, N=1200 nominal via **real nginx round-robin health-gated**.
- [ ] Extend Flask app with `body_config/header_config` tables, `/api/profile|/data_list|/session/status` endpoints with `Cache-Control public max-age=5` / `no-store` and `ETag-SHA256`, `X-Worker-Pid` header on all statuses, `/health` endpoint, admin routes with COMMIT+SELECT verification per batch.
- [ ] Launch topology D: write per-run `nginx.conf` to `/tmp/spider-runtime-35860330078/nginx/` start `gunicorn --workers 2 --bind 127.0.0.1:19860 app:app` and `nginx -c <conf> -p /tmp/...` `127.0.0.1:19851`; verify health via real curl + `X-Worker-Pid` distribution ≥10 per worker health-gated. Run B-PER-NODE baseline first via real HTTP + HS256 + fixes to replicate TN~0.667, then B-SHARED-STORE primary and B-STICKY-URL exploratory with `hash $request_uri` without replication and routing verified via real requests (round-robin balanced vs sticky-url skewed >90%).
- [ ] Execute distributed primary: **1200 paired samples via real nginx round-robin health-gated + HS256 + status-free + de-confounded** with 4-concurrency bursts, log `raw_freshness_observations.jsonl` (~1200 lines, 0 missing) + `raw_freshness_per_node.jsonl` + `raw_freshness_sticky_url.jsonl` + `batch_state_log.jsonl` (>=27 lines distinct timestamps + warmup), compute TN per endpoint as `P(bc<=0.05|valid)` with Wilson CI, n_non304 via real is_304, stratified r Fisher z CI and TOST status-free computed from data (not hardcoded), variance, FP, `scheduling_confound_r`, `structural_status_prefix_present`. Verify no synthetic timestamp clustering and health gate 0 missing.
- [ ] Provision browser substrate: `pip install agentlab==0.4.2` (verify `0.14.3` absent, not error), `pip install playwright`, `npx playwright install chromium --with-deps` if needed, verify `AgentLab 0.4.2` importable and `playwright --version`.
- [ ] Launch browser contexts at **1280x720**, create CDP session **per /resource page**, capture `Accessibility.getFullAXTree` (AX nodes count) and `document.querySelectorAll('*').length` (DOM nodes) **per /resource page** (not only index), log viewport, AX>10, PC-HEALTH, DOM 21-82. Run browser body-only/header-only/gradient/null/classic batches via **real Playwright fetch to /resource at N=20 per state** (page.request.get with decompressed body, filtered headers, fingerprint triple) + direct sanity via real requests through nginx at N=20. **Delete prior relabel logic and synthetic fallback**; verify n_a==20 not 3-4.
- [ ] Produce `raw_observations.jsonl` (~520 lines: ~260 direct via gunicorn+nginx + ~260 browser via real Playwright 1280x720 to /resource at N=20) with fields `state,status,body_sha256,body_len,content_length_header,content_encoding,headers_filtered_json,headers_raw_json,headers_no_clen_json,fingerprint_*,worker_id,ax_nodes,dom_nodes,viewport,fetch_method,cdn_cache_status,timestamp,concurrency` where ax_nodes/dom_nodes are per /resource page and fetch_method distinguishes direct vs browser and N=20, plus health-gated distributed logs.
- [ ] Metrics stable names: `freshness_c1_tn_mean`, `freshness_n_non304`, `freshness_stratified_r`, `freshness_tost_p_upper`, `freshness_scheduling_confound_r`, `bg_ax_nodes_median`, `bg_pc_health_pct`, `browser_body_AvsC_full`, `browser_gradient_1B_full` at N=20, etc plus CI width degenerate effective_distinct_n; controls stable `C1-FRESHNESS..C6-BROWSER G1 G2 E1-E4 STICKY-URL` with pass/fail and evidence_refs. All via real HTTP + HS256 + fixes health-gated at N=20.
- [ ] Record `provenance.json` with `github_run_id 35900903994 base_sha 6f579bd834c5ad36234ca444c401e3dd6301d35d` env (Flask 3.1.3 PyJWT 2.14.0 SQLite 3.45.1 WAL Werkzeug 3.1.8 gunicorn 23.0.0 nginx 1.24.0 AgentLab 0.4.2 Playwright CDP versions, ports, SEED 44, EXCLUDED, body SHAs/lengths, header constants, artifact SHA-256, git commit, DB paths `/tmp/spider-runtime-35860330078/shared.db` vs per-node vs sticky-url, HS256_SECRET hash, scheduling_seed, health_gate status).
- [ ] Must not inspect outcomes before freeze; frozen `spec.json`/`prereg.md`/`freeze.json` immutable after freeze; any deviation after seeing data is exploratory and labeled. **Remove status prefix, confounded scheduling, missing health gate, and underpowered gradients before freeze**.
- [ ] Preserve stable control/metric identities for `AUDIT`/`DIRECTOR` transmission per `research/EXPERIMENT_PACKET.md §1`; keep Jaccard discrimination identical to parent for comparability; report effective distinct N and degenerate flag per metrics; ensure `batch_state_log.jsonl` has distinct timestamps and `raw_freshness_*.jsonl` has 0 missing worker_ids/status None and N=20 for browser; verify `hs256_valid_success_rate` before computing TN and `structural_status_prefix_present==false` and `scheduling_confound_r<0.30`.
- [ ] Handle unavailable substrates gracefully: if shared store file creation fails mark `MEASUREMENT_INVALID SQLITE_SHARED_STORE_UNAVAILABLE` for distributed branch; if Playwright/AgentLab not installable mark `MEASUREMENT_INVALID PLAYWRIGHT_UNAVAILABLE` for browser branch and still decide distributed branch (MIXED); if HS256 still rejects all valid mark `MEASUREMENT_INVALID HS256_VALIDATION_STILL_REJECTS_ALL`; if status prefix or confounded scheduling detected mark `MEASUREMENT_INVALID STATUS_PREFIX/CONFOUND`; if health gate fails mark `MEASUREMENT_INVALID HEALTH_GATE_FAILED`; if browser gradients <20 mark `MEASUREMENT_INVALID GRADIENT_UNDERPOWERED`. Paid CDN absent NOT gating. **Synthetic fallback is forbidden** — provision failure must be reported as MEASUREMENT_INVALID not masked with synthetic 1.0.

