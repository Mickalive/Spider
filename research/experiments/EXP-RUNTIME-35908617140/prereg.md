# EXP-RUNTIME-35908617140 — Preregistration

**Experiment ID:** EXP-RUNTIME-35908617140  
**Lane:** runtime  
**Claims:** C-MEAS-VALID (Measurement substrate is intervention-valid), C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)  
**Director Mandate:** REOPEN — Build a shared honest-cost substrate hardening that replaces n*3200/jitter cost with frozen sum counters resolve+bind+verify+freshness+browser_steps (no jitter, no f*6.0, PC-HONEST-COST-SANITY |rho_shuffled|<0.20, within-f std>0, trajectory-grouped bootstrap 5000 CIs) and fixes C-FRESHNESS orthogonality via body-agnostic header-only Jaccard (exclude CLEN/ETag/body-derived or hash status-matched canonical bodies) with health-gated shared WAL+HS256 and URL-sticky affinity ($request_uri consistent hash) to achieve stratified |r|<0.15 TOST delta 0.15 p_upper<0.05 8/8 variance FP<=0.15 with C1 TN>=0.85 Wilson lower>0.75 session_status>=0.85 and C2 n_non304>=800 via real If-None-Match/ETag->304 on shared SQLite WAL, plus browser per-value CC/ETag/CLEN sensitivity gradients at BrowserGym 1280x720 CDP AX>10 via non-deterministic fixture (effective_distinct_n>1) delivering non-degenerate B=1000 CIs to order sensitivity beyond 1.0 ceiling — publish as audited harness for graph/product/frontier?  
**Parent Handoff:** research/experiments/EXP-RUNTIME-35900903994/handoff.json (sha256:ee14c92c1ba0887e382742bbff216c5c983e40a2439335d16aa2e15e3dfee5ea) — **disposition SUPERSEDE** per request.json director_mandate.parent_handoff_disposition. Inherited continuity evidence preserved four-way (established/rejected/unknown/do_not_assume) but MUST NOT silently override Director REOPEN decision. Local lane next_question advisory only. This design follows binding Director target claim C-MEAS-VALID and strategic question, using parent handoff as continuity evidence only. Cognitive reset true.  
**Date:** 2026-09-23  
**Dependencies:** EXP-RUNTIME-35900903994 (MIXED, stratified r=0.721 falsified even status-free, degenerate gradients, sticky pre-seeded 0.666), EXP-RUNTIME-35764329925 (loopback PASS deterministic), EXP-RUNTIME-34015740602 (Oauth middleware), EXP-GRAPH-35389145821 (r=0.0022 single-host mock)

---

## 1. Question

Can Runtime close the distributed C-FRESHNESS block **and** the honest-cost block that currently keep C-MEAS-VALID EXPERIMENTAL (single-host loopback) and block 3 lanes (graph param pilot, physics live, product economics) by applying **five measurement hardenings** to the same Flask 3.1.3 + gunicorn 23.0.0 2× sync + nginx 1.24.0 substrate under real HTTP:

1. **Honest-cost hardening:** Replace `cost = n*3200 + Uniform(50,150) jitter` and `cost = f*6.0` tautologies (portfolio assessment: bijective rho=1.0, shuffled rho>0.20, 0 constant success, within-f std 0) with **frozen sum counters** `honest_cost = count_resolve + count_bind + count_verify + count_freshness_checks + count_browser_steps` (each counter increments once per real operation, logged per observation, summed per trajectory, **no jitter, no f×6.0, no n×3200**) to achieve **PC-HONEST-COST-SANITY: shuffled-label |rho_shuffled|<0.20, within-f std>0 for each f>0, trajectory-grouped bootstrap B=5000 CIs non-degenerate**?

2. **Orthogonality hardening (body-agnostic):** Replace `structural = hash(body)%10000` (which shares auth-dependent error 401/403 JSON bodies like `{"error":"invalid"}` vs success `{"data":"hello"}` content with `behavioral_composite` yielding stratified r=0.721 CI [0.691,0.748] TOST p=1.0 even with status-free prefix removed and scheduling r=0.067 green) with **body-agnostic header-only Jaccard** — `structural_headers = Jaccard(filtered_headers MINUS body-derived {Content-Length, ETag, W/ETag-SHA, Content-Range})` where excluded headers are those deterministically derived from body bytes, OR alternatively `structural = hash(status_matched_canonical_body)` where 401/403 error bodies are replaced by fixed 31B success body `{"data":"hello","version":1}` SHA d0ca833f before hashing so only non-body header variation (Cache-Control `max-age=3600` vs `no-store`, Set-Cookie `session=xyz`, Vary `Origin`) remains — with **health-gated shared WAL at `/tmp/spider-runtime-35908617140/shared.db` plus HS256 shared-secret >=32 bytes** and **de-confounded body_variant vs drift scheduling** to restore **stratified |r|<0.15 TOST delta 0.15 (CI upper<0.15, p_upper<0.05, pooled |r|<0.15, 8/8 variance std>0, FP<=0.15)** while retaining **C1 mean TN>=0.85 Wilson lo>0.75 session_status>=0.85** and **C2 n_non304>=800 via real If-None-Match/ETag->304** stratified 400 per endpoint?

3. **Sticky hardening (>=10 URIs, single-worker seeding):** Replace prior `hash $remote_addr (ip_hash) + replicate_session_to_workers=True` and `hash $request_uri` with 3 URIs (overall skew 0.666 falsely failing >0.90 due to 2/3 ceiling, TN 1.0 non-diagnostic dual pre-seed) with **URL-bound `hash $request_uri consistent` with >=10 distinct URIs** and **single-worker session seeding only on hash-assigned worker after routing through nginx** (verified via SELECT on non-assigned worker returns 0) to test whether affinity alone substitutes for shared store at skew>0.90?

4. **Browser power hardening (non-degenerate):** Replace deterministic fixture `set_size 1 per state effective_distinct_n 1 at N=20` (all discriminations [1.0,1.0] or [0.0,0.0] width 0) with **non-deterministic fixture** — per-state body pool `A {31B,32B 1B diff}` randomized per sample plus probabilistic header jitter (Cache-Control `3600` vs `3601` 50% ) — yielding **effective_distinct_n>1 per state at N=20** and **BrowserGym 1280×720 CDP AX>10 median PC-HEALTH>=80% DOM 21-82 per /resource** via **AgentLab 0.4.2 + Playwright 1.63.0 chromium at N=20 per state with B=1000 CIs width>0** to order **CC vs ETag vs CLEN vs body size 1B/2B/4B/39B/86B** sensitivity beyond degenerate ceiling, while preserving **body AvsC full>0.5 status 0 and header AvsE full>0.5 body 0** isolation?

This is the narrowest falsifiable step that changes architecture decisions for Graph distributed delta-repair, Product residual-novelty economics, and Frontier/Physics live replication per Director comparative reasoning: alternative micro-tests (header-only vs body-only isolation) already PASS 1.0; paid CDN HIT needs separate credentials; leaving runtime IDLE while frontier/graph loop synthetic has opportunity cost of 3 blocked claims.

---

## 2. Hypothesis

**H1 — Honest-cost (C-MEAS-VALID):** Honest sum-counter cost will pass PC-HONEST-COST-SANITY where n×3200/jitter fails. Null distribution via trajectory-grouped shuffling will show |rho|<0.20, within-f families (f = novelty fraction 0,0.25,0.5,1.0) will show std>0, and B=5000 trajectory-grouped bootstrap CI will be non-degenerate (width>0 effective distinct trajectories >1), because counters reflect real operation counts not bijective n.

**H2 — Distributed freshness with header-only (C-FRESHNESS + C-MEAS-VALID):** A health-gated (0 missing X-Worker-Pid, 0 status None) shared SQLite WAL at `/tmp/spider-runtime-35908617140/shared.db` (WAL, check_same_thread=False, COMMIT verified via `SELECT count(*) FROM sessions` before each batch, batch_state_log >=27 distinct timestamps) plus HS256 shared-secret >=32 bytes (PyJWT 2.14.0 decode via `pyjwt.decode(token, secret, algorithms=['HS256'])` then `SELECT sessions WHERE id=payload.sid`, not raw Bearer string) plus header-only Jaccard structural (MINUS CLEN/ETag) with de-confounded scheduling (body_variant random independent of drift, Cramér's V<0.30) will restore C1 mean TN≥0.85 Wilson lo>0.75 session_status≥0.85 (computed P(behavioral<=0.05|valid)) with n_non304≥800 after real 304 stratified 400 per endpoint and orthogonality stratified |r|<0.15 TOST with 8/8 variance and FP≤0.15 via real nginx round-robin. Per-node B-PER-NODE (same HS256 secret, isolated DBs) will show mean 0.667 session_status 0.0 proving replication necessity.

**H3 — Sticky URL-bound >=10 URIs (C-FRESHNESS alternative):** URL-bound `hash $request_uri consistent` without replication, with >=10 distinct URIs (e.g., `/api/profile?u=1..4`, `/api/data_list?u=1..3`, `/api/session/status?u=1..3`) and single-worker seeding, will achieve mean TN≥0.85 and overall skew>0.90 (each distinct URI pinned, per-URI affinity 1.0) via real HTTP health-gated, testing H3 isolation correctly (prior 3-URI ceiling 0.666 not diagnostic).

**H4 — Browser non-degenerate (C-MEAS-VALID):** BrowserGym 1280×720 with AgentLab 0.4.2 + Playwright 1.63.0 chromium viewport 1280×720 verified per /resource page, CDP Accessibility.getFullAXTree median>10 PC-HEALTH≥80% DOM 21-82 per /resource page, with non-deterministic fixture (body pool per state) at N=20 per state via real page.request.get to /resource (decompressed, filtered headers) will preserve body AvsC full 1.0 status 0 headers-no-bodyderived 0 and header AvsE full 1.0 status 0 body 0, and will yield B=1000 CIs with width>0 effective_distinct_n>1 for at least two gradient magnitudes (e.g., 1B vs 86B or CC_small vs ETag) enabling ordering CC vs ETag vs CLEN beyond prior degenerate [1.0,1.0].

If H1–H4 hold with validity checks passing, the runtime block is closed per Director. Any branch failing with validity green is bounded falsification, not invalidity.

---

## 3. Inherited State — What is Established, Rejected, Unknown (from parent handoff ee14c9..., preserved four-way, disposition SUPERSEDE)

From `EXP-RUNTIME-35900903994/handoff.json` (MIXED, audit FAIL producer_claim_supported false) — parent fixes verified green but orthogonality closed falsified; ceilings audit-confirmed but bounded to single-host 2-worker localhost simulation, EXPERIMENTAL not VALIDATED.

**Established (bounded, audit recomputed match true, narrowed ceiling — loopback/mimic EXPERIMENTAL):**
- Distributed freshness detection SURVIVES bounded to single-host 2× gunicorn 23.0.0 + nginx 1.24.0 shared SQLite WAL at `/tmp/spider-runtime-35860330078/shared.db` (WAL, per-batch SELECT 31 lines shared 93 total distinct ts, health-gated 0 missing via GET /health 200+X-Worker-Pid) + HS256 shared-secret PyJWT 2.14.0 decode hs rate 0.983 =669/680 via 4-concurrency SEED 44: mean TN 0.9745 Wilson lo 0.955 (profile 1.0 lo 0.974, data_list 1.0 lo 0.974, session_status 0.923 lo 0.868) vs per-node 0.667 session_status 0.0 lo 0.0, n_non304 1073/1200 after 127 real 304 stratified 400 per endpoint, FP 0.0 hi 0.023, 8/8 variance bc_std 0.24-0.50 struct_std 2470-3838.
- Per-node isolated DB baseline B-PER-NODE replicates failure with same HS256 secret but isolated files via nginx round-robin 613/587 balanced, stratified r 0.300 CI upper 0.353 — proving HS256 alone insufficient without shared store.
- Status-free structural verified no `f"{status}|"` prefix (grep pass), de-confounded scheduling random.choice per request independent of drift scheduling_confound_r 0.0666 <0.30 (audit PASS, 500-9585 hash range).
- Browser substrate provision SURVIVES bounded to AgentLab 0.4.2 (0.14.3 absent), Playwright 1.63.0 1280×720 viewport verified per /resource page, CDP AX median 54 on /resource pages (10 pages), PC-HEALTH 100% DOM median 26 within 21-82 via 760 browser page.request.get +760 direct at N=20 per state, fingerprint byte-identical via sort_keys True decompressed, discrimination body AvsC full 1.0 body 1.0 status 0 headers-no-CLEN 0 (31B vs117B/70B), header AvsE full 1.0 headers-no-CLEN 1.0 status 0 body 0 CLEN 31==31, nulls 0.0 CI [0,0] contains 0.

**Rejected (bounded):**
- C-FRESHNESS orthogonality |r|<0.15 with hash(body) structural FALSIFIED-IN-SETTING even status-free and de-confounded: pooled |r| 0.598 stratified r 0.721 CI [0.691,0.748] TOST p_upper=1.0 >>0.15 with validity green — residual coupling is auth-dependent body content shared between behavioral_composite and hash(body). Do not assume body-hash can be orthogonal.
- Degenerate bootstrap CIs [1.0,1.0] or [0.0,0.0] width 0 as high-precision evidence REJECTED: effective_distinct_n 1 set_size 1 deterministic, correctly disclosed not variance; no sensitivity ordering inferrable.
- Per-node isolated SQLite achieving TN≥0.85 REJECTED (mean 0.667 session_status 0.0).
- Sticky URL-bound affinity overall skew >0.90 with only 3 URIs REJECTED (0.666 fails due to 2/3 ceiling) and sticky TN 1.0 as proof of affinity alone REJECTED due to dual-DB pre-seed confound.
- n×3200/jitter cost and f×6.0 as honest cost REJECTED by portfolio assessment (rho tautology 1.0, shuffled rho>0.20, within-f std 0) — bijective artifact, not measurement.

**Unknown (this experiment directly targets the first four):**
- Whether orthogonality |r|<0.15 is recoverable with body-agnostic header-only Jaccard excluding CLEN/ETag/body-derived or status-matched canonical bodies where error vs success bodies made identical.
- Whether honest sum-counter cost achieves |rho_shuffled|<0.20, within-f std>0 and trajectory-grouped B=5000 non-degenerate CIs vs n×3200 tautology.
- Whether sticky URL affinity alone suffices when sessions seeded only on hash-assigned worker after routing with >=10 URIs for overall skew>0.90 (requires single-worker seeding, not dual pre-seed).
- What per-value CC vs ETag vs CLEN vs body-size sensitivity ordering is when CIs become non-degenerate via non-deterministic fixture effective_distinct_n>1.
- Whether shared WAL generalizes to >4 concurrency or multi-host Redis cluster beyond single-host simulation, and whether header canonicalization changes discrimination.

**Do not assume (explicitly unsafe, per parent do_not_assume + Director priors):**
- C-FRESHNESS or C-MEAS-VALID are VALIDATED or PRODUCT_CORE — audit FAIL, ceiling single-host localhost simulation filtered headers, body 31-117B, single viewport, no paid CDN, no multi-host Redis — EXPERIMENTAL only.
- Degenerate CIs imply high precision — they are deterministic set_size 1, not certainty.
- Sticky TN 1.0 or per-URI affinity 1.0 proves URL-bound substitutes for shared store — pre-seeded dual DB confounds inference.
- Shared SQLite WAL implies multi-host Redis, paid Cloudflare/Fastly HIT/STALE, TLS/HTTP2, or BrowserGym DOM beyond HTTP triple (AX/DOM node counts per /resource only).
- Per-node 0.667 failure avoidable by HS256 shared-secret alone without shared store — proven required.
- Body-hash orthogonality failure implies no structural signal can be orthogonal — falsification bounded to hash(body).
- Loopback single-host results generalize to production SPAs with correlated DOM/state or LLM economics.
- 25-byte HS256 secret is secure — warning disclosed; resize to ≥32 bytes.
- Tool/API bypass vs UI replay prior not evidence — agent priors used only to motivate correct-family gating and mixed composition, not as SPIDER evidence.
- Prefix/Jaccard micro-tuning on synthetic harness generalizes to live browser distribution — parked per Director.

This REOPEN supersedes local lane next_question loop; it tests Director's honesty + body-agnostic hardenings, not a repeat of body-hash.

---

## 4. Server Design

### 4.1 Testbed Architecture (two substrates, same Flask app base, real HTTP mandatory + HS256 >=32 bytes + 5 hardenings)

```
Flask 3.1.3 + PyJWT 2.14.0 HS256 shared-secret >=32 bytes + SQLite WAL (shared vs per-node vs sticky-url) + honest sum counters + optional Redis
  ├── POST /admin/set_body_variant   (admin JWT, writes body_config, COMMIT, BYPASS, SELECT verification, increments count_verify)
  ├── POST /admin/set_headers        (admin JWT, writes header_config, COMMIT, BYPASS)
  ├── POST /admin/invalidate_session (DELETE sessions, COMMIT, BYPASS, SELECT verification, increments count_freshness_checks)
  ├── GET  /resource                 (authenticated GET, status+JSON body+filtered headers, Cache-Control, ETag-SHA256, If-None-Match->304, X-Worker-Pid on ALL statuses)
  ├── GET  /api/profile              (C-FRESHNESS endpoint, profile, cacheable, sticky URI ?u=)
  ├── GET  /api/data_list            (C-FRESHNESS endpoint, data_list, cacheable, sticky URI ?u=)
  ├── GET  /api/session/status       (C-FRESHNESS endpoint, session-dependent, sticky URI ?u=)
  └── GET  /health                   (nginx+gunicorn health gate, 200+X-Worker-Pid)
  └── POST /admin/ensure_session     (creates session via POST through nginx to hash-assigned worker only, increments count_bind)

Substrate D (distributed C-FRESHNESS + honest-cost, primary) — REAL HTTP + HS256 >=32 + hardenings:
  Origin: gunicorn 23.0.0 2× sync --workers 2 --bind 127.0.0.1:19860 --timeout 30
       + nginx 1.24.0 127.0.0.1:19851 proxy_pass http://gunicorn_upstream
         upstream gunicorn_upstream { server 127.0.0.1:19860; }  (round-robin)
         Alternative upstream for B-STICKY-URL-10URI: hash $request_uri consistent; server 127.0.0.1:19860;
  DB modes (real) + HS256 >=32 + honest cost:
    B-PER-NODE: each worker isolated file /tmp/spider-runtime-35908617140/pernode-<worker>.db (WAL, not shared) same HS256 secret >=32 but isolated sessions — real nginx round-robin, health-gated, header-only structural, de-confounded, sum-cost, expected TN~0.667
    B-SHARED-STORE-HEADER-ONLY: single shared file /tmp/spider-runtime-35908617140/shared.db (WAL, shared, check_same_thread=False, same HS256 secret >=32 shared) — real nginx round-robin, health-gated, header-only MINUS CLEN/ETag, de-confounded, sum-cost, expected TN≥0.85 and |r|<0.15
    B-STICKY-URL-10URI: per-node DBs WITHOUT replication (replicate_session_to_workers=False, sessions seeded ONLY via hash-assigned worker POST through nginx) with hash $request_uri consistent + 10 distinct URIs — real nginx URL-bound, health-gated, header-only, de-confounded, sum-cost, expected TN≥0.85 if affinity suffices, >90% overall skew
  Honest-cost instrumentation: counters resolve/bind/verify/freshness/browser_steps incremented per real operation in run_experiment.py, summed per trajectory (trajectory_id = batch or drift condition group), logged per observation as honest_cost_per_trajectory; grep verifies no `*3200` or jitter in cost path.
  Auth fix: Flask validates JWT via pyjwt.decode(Bearer token, HS256_SECRET>=32, algorithms=['HS256']) then SELECT sessions WHERE session_id=payload sid; NOT raw string lookup.
  Structural fix: header-only Jaccard = Jaccard(filtered_headers MINUS {content-length,etag}) where filtered_headers are lowercased sorted headers minus {Date,Server,X-Request-Id,CF-RAY,CF-Cache-Status,X-Cache,Age,X-Worker-Pid}; alternatively status-matched canonical body hash (error bodies mapped to 31B success body).
  Scheduling fix: body_variant and novelty fraction f randomized independent of drift via random.choice, logged, Cramér's V<0.30.
  Health gate: wait_http loops GET http://127.0.0.1:19851/health via nginx until 200+X-Worker-Pid, max 30s.

Substrate B (browser C-MEAS-VALID) — REAL BROWSER FETCHES at N=20 with non-deterministic fixture:
  Same origin gunicorn+nginx as above (shared-store mode for origin, body_config/header_config, body variants 31B/32B/33B/35B/70B/117B)
  + AgentLab 0.4.2 (pip install agentlab==0.4.2) + Playwright 1.63.0 chromium at 1280×720
    - Browser contexts: browser.newContext({viewport:{width:1280,height:720}})
    - Viewport verified per page: page.viewportSize().width==1280 && height==720
    - CDP session per /resource page: cdpSession = await page.context().newCDPSession(page); await cdpSession.send('Accessibility.getFullAXTree')
    - AX capture: Accessibility.getFullAXTree per /resource page (NOT only index)
    - DOM enumeration: await page.evaluate(() => document.querySelectorAll('*').length) per /resource page
    - HTTP triple capture: await page.request.get('http://127.0.0.1:19851/resource?u=...') with decompressed body+headers + fingerprint identical to direct pipeline at N=20 per state, with non-deterministic pool (A states draw 31B vs 32B per sample)
    - Direct sanity: requests.get via same nginx (separate artifact, not relabeled)
```

`body_config` variants `A 31B {"data":"hello","version":1}` SHA `d0ca833f`, `A1 32B 1B diff`, etc.; `header_config` fixed `Cache-Control:max-age=3600, ETag:W/"fixed-aaa-111", Vary:Accept-Encoding` for baselines; non-deterministic pool adds `A_alt 32B {"data":"hello!","version":1}` mixed 50% per sample for variance.

**Distributed harness real HTTP + HS256 >=32 + header-only + honest-cost:** 8 co-occurring drift conditions (permission_boundary, session_invalidation, signing_key_rotation, token_expiry × cache_enabled/disabled) plus 4 noise-only, each paired behavioral+structural samples where `structural` is header-only Jaccard MINUS body-derived, `body_variant` randomized independent of drift, real ETag/If-None-Match exercised to generate 304 (~33% when cache_enabled), honest-cost counters summed per trajectory. Total nominal 1200 paired samples via real nginx round-robin health-gated to achieve n_non304≥800 after exclusion, 0 missing. Each sample logs `X-Worker-Pid`, `is_304`, `body_variant`, `scheduling_seed`, `honest_cost`, `trajectory_id`, `headers_no_bodyderived_json`.

**Browser harness real fetches at N=20 with non-deterministic fixture:** Body states `A 31B baseline + A_alt 32B pool`, `A1 32B 1B diff, A2 33B 2B, A3 35B 4B, B 70B 39B, C 117B 86B` and header states `E combined, CC_small 3601 1s diff, CC_large 0, ETag_small 1char, ETag_large changed, SC_small, SC_large, Vary_small` plus non-deterministic header jitter 50% `max-age 3600 vs 3601`. **Direct via requests through nginx and browser via page.request.get through nginx** both decompressed, filtered identically, at **N=20 per state** with **B=1000 bootstraps** and **effective_distinct_n>1**.

### 4.2 Body and Header States for Browser Part

| State | Body JSON (sort_keys=True) | body_len decomp | Status | Filtered Headers MINUS Body-Derived (Jaccard structural) |
|-------|----------------------------|-----------------|--------|----------------------------------------------------------|
| **A baseline** | `{"data":"hello","version":1}` | 31 | 200 | `Cache-Control:max-age=3600, Vary:Accept-Encoding, Content-Type:application/json` (CLEN 31 and ETag removed for structural) |
| **A_alt pool** | `{"data":"hello!","version":1}` 32B (50% of A samples) | 32 | 200 | identical minus body-derived |
| **A1 grad 1B** | same pool logic | 32 | 200 | identical minus body-derived |
| **A2 grad 2B** | `{"data":"hello!!"}` | 33 | 200 | identical minus body-derived |
| **A3 grad 4B** | `{"data":"hello!!!!"}` | 35 | 200 | identical minus body-derived |
| **B reader** | `{"data":"hello","items":["a","b"],"role":"reader"}` | 70 | 200 | identical minus body-derived |
| **C admin** | `{"admin_note":"sensitive:42",...}` | 117 | 200 | identical minus body-derived |
| **E combined** | 31B | 31 | 200 | `Cache-Control:max-age=0,must-revalidate, Set-Cookie:session=xyz; Path=/; HttpOnly, Vary:Accept-Encoding,Origin` (CLEN/ETag excluded from Jaccard) |
| **Isolations** | same 31B body (or pool) | 31 | 200 | CC_small `max-age=3601` vs CC_large `0`; ETag excluded from structural so ETag isolations expected 0.0 for header-only structural (diagnostic), SC_small `session=abc` vs SC_large, Vary_small etc. |

Structural Jaccard for freshness uses `headers_no_bodyderived_json` only; CLEN/ETag/body-derived excluded. Body-correlated vs independent contrast now: B-HEADERS-ONLY includes CLEN vs B-HEADERS-NO-BODYDERIVED excludes — former should be 1.0 on body-only via CLEN, latter 0.0 proving exclusion.

### 4.3 Honest-Cost Trajectory Definition

- **Unit for cost:** trajectory = single drift condition group (e.g., permission_boundary|cache=0) or batch of 10 paired samples sharing same trajectory_id. Honest cost per trajectory summed from per-observation counters; novelty fraction f = |unique drift conditions in trajectory| / total conditions or proportion of invalid sessions per trajectory.
- **Counters:** `count_resolve` increments on registry lookup for resolve(), `count_bind` on slot binding, `count_verify` on verify() postcondition, `count_freshness_checks` on behavioral composite eval, `count_browser_steps` on browser page.request.
- **Frozen:** counters defined in `run_experiment.py:_inc(key)` with no jitter, no multiplication; grep `honest_cost` shows sum.

---

## 5. Measurement

### 5.1 Observation Vector

**Distributed part (per paired sample, real HTTP + HS256 >=32 + header-only + honest-cost):**
- `endpoint` (profile/data_list/session_status), `cache_enabled` bool, `status` int, `body_bytes` + `body_sha256` + `body_len` + `Content-Length`, `headers_filtered_json`, `headers_no_bodyderived_json` (MINUS CLEN/ETag), `headers_no_bodyderived_jaccard_structural` float, `ETag`, `Cache-Control`, `worker_id` (X-Worker-Pid, 0 missing), `behavioral_composite` (graded session_status_check + auth delta, TN P(bc<=0.05|valid)), `structural_header_only` (Jaccard), `body_variant` (A/A1/A2/B/C), `scheduling_seed`, `drift_condition`, `is_304` bool (real 304), `timestamp`, `db_path`, `jwt_valid`, `hs256_verified`, `health_gated`, `honest_cost_per_observation`, `trajectory_id`, `honest_cost_per_trajectory`, `f_novelty_fraction`, `distinct_uri` (for sticky >=10 URIs)

**Browser part (per request via direct or Playwright, real HTTP at N=20 with non-deterministic fixture):**
- `state`, `status`, `body_bytes` decompressed + `body_sha256` + `body_len` + `Content-Length`, `headers_filtered_json`, `headers_no_bodyderived_json`, `headers_only_jaccard`, `fingerprint_full/status/body/headers/headers_no_bodyderived` (SHA256), `worker_id`, `ax_nodes` (per /resource page), `dom_nodes` (per /resource page), `viewport` ({1280,720}), `pc_health`, `timestamp`, `concurrency`, `fetch_method` (direct vs browser_page_request), `effective_distinct_n` helper, `honest_cost_browser_step`

### 5.2 Metrics (stable names for AUDIT/DIRECTOR — frozen for recomputation)

**Distributed C-FRESHNESS (real HTTP + HS256 >=32 + header-only + honest-cost, health-gated):**
- `shared_freshness_c1_tn_mean`, `shared_freshness_c1_tn_wilson_lo/hi`, `shared_freshness_c1_tn_session_status/profile/data_list` + Wilson per endpoint
- `shared_freshness_c1_tn_per_node_mean` (B-PER-NODE expected 0.667), `shared_freshness_c1_tn_sticky_url_mean` (>=10 URIs)
- `shared_freshness_c1_tn_sticky_url_skew` (max worker share, must be >0.90 with >=10 URIs), `sticky_min_per_uri_affinity` (per-URI affinity 1.0 each)
- `shared_freshness_n_non304` (shared count after real 304, must be >=800), `shared_freshness_n_total/n_304/n_missing_worker` (0 missing)
- `shared_freshness_stratified_r` (header-only Jaccard pooled Fisher z stratified), `shared_freshness_stratified_r_ci_lo/hi`, `shared_freshness_tost_p_upper`, `shared_freshness_tost_pass` (delta 0.15), `shared_freshness_pooled_r`
- `shared_freshness_fp_noise` (noise-only FP header-only, must be <=0.15), `shared_freshness_c2_variance_pass` (8/8 std>0)
- `shared_freshness_worker_distribution_shared/per_node/sticky` (real counts), `shared_freshness_hs256_valid_success_rate` (>=0.90), `shared_freshness_hs256_secret_len` (>=32)
- `shared_freshness_structural_header_only` (bool true, CLEN/ETag excluded), `shared_freshness_structural_status_prefix_present` (false), `shared_freshness_scheduling_confound_r` (<0.30)
- `shared_freshness_canonical_body_used` (bool, status-matched canonical body replacement flag)

**Honest-cost C-MEAS-VALID (trajectory-grouped, frozen sum):**
- `honest_cost_shuffled_rho` (|rho_shuffled| via trajectory-grouped permutation B=5000), `honest_cost_shuffled_rho_ci_lo/hi`, `honest_cost_shuffled_p`
- `honest_cost_within_f_std_per_f` (dict f->std, each >0 for f>0), `honest_cost_within_f_std_min`
- `honest_cost_trajectory_grouped_bootstrap_ci_lo/hi` per f, `honest_cost_b5000_width` (must be >0), `honest_cost_effective_distinct_trajectories`
- `honest_cost_no_jitter_verified` (bool true), `honest_cost_no_n3200_verified` (bool true), `honest_cost_no_f6_verified` (bool true)
- `honest_cost_per_trajectory_distribution` (per trajectory sums)

**Browser C-MEAS-VALID (real browser N=20 with non-deterministic fixture):**
- `bg_provision_ok`, `bg_agentlab_version`, `bg_agentlab_0143_absent`, `bg_playwright_viewport`, `bg_ax_nodes_median` (on /resource), `bg_ax_nodes_per_page`, `bg_pc_health_pct` (on /resource), `bg_dom_nodes_median` (on /resource), `bg_dom_nodes_range_ok`, `bg_effective_distinct_n_per_state` (must be >1)
- `browser_body_AvsC_full/status/body/headers_no_bodyderived` + CI [lo,hi] width degenerate effective_distinct_n via Playwright N=20
- `browser_header_AvsE_full/headers_no_bodyderived` + CI via Playwright N=20
- `direct_body_AvsC_full` sanity, `direct_header_AvsE_full`
- `browser_null_body_full`, `browser_null_header_full`, `browser_null_403/401_full` + CI N=20
- `browser_gradient_1B_full`, `2B`, `4B`, `39B` (AvsB), `86B` (AvsC) + per-measure CI/width/degenerate/effective_distinct_n via both direct and browser N=20 with pool
- `browser_gradient_CC_small/large`, `ETag_small/large` (isolations now via headers_no_bodyderived: ETag expected 0.0 for header-only structural, diagnostic), `SC_small/large`, `Vary_small` + CI N=20
- `direct_gradient_*` same via direct

All Jaccard `1 - |A∩B|/|A∪B|` on headers_no_bodyderived for freshness structural; bootstrap B=1000 browser B=5000 cost trajectory-grouped; Fisher z for distributed r.

### 5.3 Baselines (frozen thresholds)

| ID | Expected distributed (real HTTP + HS256 >=32 + header-only + honest-cost, health-gated) | Expected browser (real Playwright N=20 non-deterministic) | Purpose |
|----|---------------------|------------------|---------|
| B-PER-NODE | TN~0.667 fail, n_non304 nominal but C1 fails (real, HS256 same secret >=32 isolated DB, header-only, de-confounded, 0 missing, sum-cost) | — | Replicates failure is replication not algorithm |
| B-SHARED-STORE-HEADER-ONLY | TN≥0.85 pass, n_non304≥800, header-only r TOST within 0.15 health-gated (real, HS256+shared WAL, MINUS CLEN/ETag) | — | Primary fix: shared store + body-agnostic |
| B-STICKY-URL-10URI | TN≥0.85 exploratory >90% overall skew health-gated without replication, >=10 URIs, single-worker seeding (real URL-bound hash $request_uri) | — | Tests affinity alone vs shared store corrected |
| B-COST-SHUFFLED | — | honest-cost shuffled |rho|<0.20 trajectory-grouped B=5000 pass (sum-cost no jitter) | — | Honest-cost null: bijective artifact absent |
| B-STATUS-ONLY | — | 0.0 on 200 vs200 at N=20 both methods | Status isolation |
| B-BODY-ONLY | — | 1.0 body-only, 0.0 header-only at N=20 | Body signal |
| B-HEADERS-ONLY | — | 1.0 via CLEN body-only, 1.0 header-only at N=20 | Body-correlated CLEN contrast |
| B-HEADERS-NO-BODYDERIVED | — | 0.0 body-only, 1.0 header-only CC/SC/Vary at N=20 (ETag CLEN excluded) | Independent header without body coupling |

### 5.4 Sample Size

- Distributed: **N=1200 paired samples nominal via real nginx round-robin health-gated + HS256 >=32 + header-only + honest-cost** (8 drift × ~120 each + 4 noise-only ×60 + 120 extra for 10-URI entropy) targeting **n_non304≥800 after real 304 exclusion** (cache_enabled 50% ×33% real 304 =16.5% overall →1002 non-304 at N=1200) with **0 missing**. Per-batch SELECT and X-Worker-Pid logged. HS256 valid JWTs must achieve 200 on ≥90%. **Fix verification:** `structural_header_only==true` (CLEN/ETag excluded) and `scheduling_confound_r<0.30` and `honest_cost_no_jitter/no_n3200 true` logged.
- Honest-cost: **trajectory-grouped B=5000 bootstrap** on honest-cost per trajectory (trajectory_id groups, ~120 trajectories from 1200 samples); reports per-f std>0 and shuffled |rho|<0.20. Counters frozen before outcomes.
- Browser: **N=20 per state nominal via direct + via real Playwright 1280×720 with non-deterministic pool** (body 60+gradient 60+header 40+isolations 140+nulls 80+classic 80 = ~520 raw lines with ax/dom per /resource page at N=20 with effective_distinct_n>1). Concurrency 4 for null and at least one body/header branch. Gradients B=1000 with N=20 must be non-degenerate width>0 for ordering (requires pool). Sticky >=10 URIs adds ~170 lines (17 per URI ×10).

---

## 6. Decision Rule (Frozen — no post-hoc weakening, real HTTP + HS256 >=32 + header-only + honest-cost + >=10 URIs + non-deterministic fixture required)

**SUPPORTS** (both substrates + honest-cost close block with hardenings) iff **ALL** mandatory conditions hold with validity checks passing and **no synthetic data** and **HS256 >=32 validates** and **header-only body-agnostic** and **de-confounded** and **health gate 0 missing** and **honest sum counters (no jitter, no n×3200, no f×6.0) with trajectory-grouped B=5000**:

1. **C1-FRESHNESS (distributed TN, real HTTP + HS256 >=32 + header-only, health-gated):** shared-store header-only arm **mean TN ≥0.85** across 3 endpoints (session_status, profile, data_list) with each Wilson 95% lower >0.75 and **session_status individually ≥0.85**, computed as `P(behavioral<=0.05|valid)` with header-only structural and de-confounded scheduling and health gate 0 missing, while **B-PER-NODE baseline mean TN <0.85** (expected ~0.667, session_status 0.0) replicating failure via real HTTP + same HS256 secret >=32 + header-only + honest-cost — proves shared store not tautological. Must have `hs256_valid_success_rate≥0.90`, `structural_header_only==true` (CLEN/ETag excluded), `scheduling_confound_r<0.30`, `hs256_secret_len>=32`.

2. **C2-FRESHNESS (power, real 304, health-gated):** **n_non304 ≥800** after excluding **real** 304 status (counted from `raw_freshness_observations.jsonl` where `is_304==false` via real If-None-Match/ETag, stratified 400 per endpoint, with per-batch SELECT verification) with **0 missing X-Worker-Pid and 0 status None**.

3. **C3-FRESHNESS (orthogonality, real, header-only body-agnostic, de-confounded, health-gated):** stratified pooled Pearson **r equivalence TOST within delta=0.15**: **95% Fisher z CI upper <0.15** AND **TOST p_upper <0.05** (and CI lower >-0.15), **pooled |r|<0.15**, with **8/8 conditions variance std>0** for both behavioral and header-only structural signals and **noise FP ≤0.15** (C4) on shared-store header-only arm via real HTTP + fixed cost. If C3 fails where validity passes (header-only true, CLEN/ETag excluded, canonical body optionally used, de-confounded 0 missing), orthogonality is **FALSIFIED-IN-SETTING** (not rescued by removing body coupling) — bounded to header-only harness.

4. **C4-FRESHNESS (noise, real, header-only):** noise-only FP ≤0.15 (Wilson upper) on shared-store via real HTTP + header-only, 0 missing.

5. **C7-HONEST-COST (real sum counters, trajectory-grouped B=5000):** **|rho_shuffled|<0.20** via trajectory-grouped permutation (B=5000 shuffling trajectory labels) on honest sum counters (no jitter, no n×3200, no f×6.0, verified via grep) **and within-f std>0 for each f>0** and **trajectory-grouped B=5000 bootstrap 95% CI width>0** (effective distinct trajectories>1). If |rho|≥0.20, PC-HONEST-COST-SANITY fails → FALSIFIED or MEASUREMENT_INVALID per falsifier.

6. **C5-BROWSER-PROVISION (real Playwright N=20 non-deterministic to /resource):** `AgentLab 0.4.2` importable, `0.14.3` correctly absent, `Playwright` viewport 1280×720 verified per /resource page, **CDP AX nodes median >10 on /resource pages** and **PC-HEALTH ≥80% on /resource pages** and **DOM nodes 21–82 on /resource pages** via real Playwright at N=20 with **effective_distinct_n>1 per state**.

7. **C6-BROWSER-DISCRIMINATION (real browser fetch N=20 non-deterministic to /resource):** browser body-only **AvsC full>0.5** expect 1.0 with status 0 headers-no-bodyderived 0 and browser header-only **AvsE full>0.5** headers-no-bodyderived 1.0 status 0 body 0 CLEN 31==31 via **real Playwright at N=20 with pool** (direct sanity also 1.0 at N=20). Nulls concurrent each full 0.0 CI contains 0.0 point ≤0.05 at N=20. Gradients must report with **width>0 for at least 2 magnitudes** (effective_distinct_n>1) to claim ordering.

**Gradient reporting mandatory (exploratory but required for high information at N=20 with non-deterministic fixture — must be non-degenerate for ordering):**
- `G1_BODY_MAGNITUDE`: for each body gradient `A vs A1 1B, A vs A2 2B, A vs A3 4B, AvsB 39B, AvsC 86B` report Jaccard full/body/headers/headers_no_bodyderived and CI [lo,hi] width degenerate effective_distinct_n via both direct and browser at N=20 with pool — at least 2 must be width>0.
- `G2_HEADER_MAGNITUDE`: for each header gradient `CC_small 3601 1s, CC_large 0, SC_small, SC_large, Vary_small` (ETag isolations diagnostic: expected 0.0 for header-only structural proving exclusion) same reporting via both at N=20 with pool.

**Sticky exploratory (not gating SUPPORTS but high-information, health-gated, header-only, single-worker seeding, >=10 URIs):**
- `E4_STICKY_URL`: sticky URL-bound `hash $request_uri consistent` with >=10 distinct URIs without replication TN `≥0.85` with >90% overall skew vs per-node 0.667; if sticky fails where validity passes (health gate 0 missing, header-only true, single-worker seeding, real HTTP without mirroring) => sticky FALSIFIED (affinity alone insufficient per corrected design).

If any C1–C7 fails where validity checks pass (health gate 0 missing, header-only true with CLEN/ETag excluded, de-confounded <0.30, real HTTP, HS256 >=32 correct, sum-cost no jitter, N=20 with effective_distinct_n>1) => **FALSIFIED-IN-SETTING** bounded to failing branch (e.g., C3 header-only still |r|≥0.15 => orthogonality FALSIFIED even body-agnostic). If C2 power fails (<800) with C1/C3 passing => **MEASUREMENT_INVALID**. If HS256 valid JWTs still all 401 (0/300) or secret <32 => **MEASUREMENT_INVALID HS256_VALIDATION_STILL_REJECTS_ALL / INSECURE_KEY**. **Any hash(body) alone as structural, CLEN/ETag not excluded, status prefix still present, confounded scheduling detected (|r|>0.30), synthetic generation, inverted TN formula, hardcoded TOST, relabeled direct-as-browser, n×3200/jitter/f×6.0 in cost, or health gate missing (>0 missing) triggers MEASUREMENT_INVALID** per frozen falsifier. Infrastructure-unavailable branches map to **MEASUREMENT_INVALID** not falsification: `gunicorn/nginx unavailable`, `shared store file creation fails`, `Playwright not installable`, `CDP capture not available on /resource`, `AgentLab 0.4.2 not on PyPI` => browser branch MEASUREMENT_INVALID while distributed+cost can still be decided. **Paid CDN absent is NOT invalidity** per SUPERSEDE (explicitly excluded, not gating). Degenerate CI expected only if pool fails to introduce variance; with pool effective_distinct_n>1 width>0 expected.

**Exploratory (not gating but reported):**
- `E1_CI_NONDEGENERATE`: width 0 vs >0 per browser comparison at N=20 with pool, effective_distinct_n per state.
- `E2_FOLDING`: case/whitespace/order folded E variant full 0.0 if normalized.
- `E3_EDGE_VISIBILITY`: X-Worker-Pid distribution per store mode (real, health-gated, >=10 URIs).
- `E4_STICKY_URL`: sticky URL-bound >=10 URIs without replication TN and overall/ per-URI distribution skew vs shared-store.
- `E5_HONEST_COST_RHO`: shuffled |rho| vs n×3200 tautology contrast trajectory-grouped.
- `E6_CANONICAL_BODY`: compare header-only Jaccard vs status-matched canonical body hash orthogonality as sensitivity analysis.

---

## 7. Controls Summary

| Control | ID | Type | Threshold (real HTTP + HS256 >=32 + header-only + honest-cost, health-gated, N=20 pool) | Evidence |
|---------|----|------|-----------|----------|
| Distributed TN shared header-only | C1-FRESHNESS | positive | `mean ≥0.85` Wilson lower >0.75 session_status ≥0.85 `P(bc<=0.05|valid)` `hs256_valid_success_rate≥0.90` `header_only true CLEN/ETag excluded` `scheduling |r|<0.30` `hs256_secret_len≥32` `0 missing` | TN per endpoint via real nginx shared store header-only Jaccard |
| Distributed TN per-node baseline | B-PER-NODE | negative | `mean ~0.667 <0.85` session_status 0.0 (real + HS256 >=32 same secret + header-only + honest-cost + 0 missing) | Replicates failure via real nginx round-robin |
| Distributed TN sticky URL >=10 URIs | B-STICKY-URL-10URI / E4 | positive exploratory | `mean ≥0.85` `overall skew >0.90` `hash $request_uri` with >=10 URIs without replication, single-worker seeding, `0 missing` | TN/distribution sticky URL-bound corrected |
| Power n_non304 | C2-FRESHNESS | validity/power | `≥800` after real 304 + `0 missing` header-only | Count from raw_freshness real is_304==false stratified |
| Orthogonality stratified r header-only | C3-FRESHNESS | equivalence TOST header-only de-confounded | `CI upper <0.15` `p_upper<0.05` `|r|<0.15` 8/8 variance `scheduling |r|<0.30` | Fisher z stratified real header-only |
| Noise FP | C4-FRESHNESS | null | `≤0.15` header-only real `0 missing` | Noise-only FP real header-only |
| Honest-cost sanity | C7-HONEST-COST | positive PC-HONEST-COST-SANITY | `|rho_shuffled|<0.20` trajectory-grouped B=5000, `within-f std>0`, `B=5000 width>0`, `no jitter/no n*3200/no f*6` | Shuffled rho per trajectory sum counters |
| Browser provision | C5-BROWSER | positive | AgentLab 0.4.2, 0.14.3 absent, viewport 1280×720, AX>10 median **on /resource** PC-HEALTH≥80% **on /resource** DOM 21-82 **at N=20 pool effective_distinct_n>1** | pip show, CDP per /resource page N=20 pool |
| Browser body discrimination | C6a | positive+isolation N=20 pool | `full>0.5` `status 0.0` `headers-no-bodyderived 0.0` via **real Playwright N=20 pool** | Jaccard via Playwright |
| Browser header discrimination | C6b | positive+isolation N=20 pool | `full>0.5 headers-no-bodyderived 1.0` `status/body 0.0` `CLEN 31==31` via **real Playwright N=20 pool** | Jaccard via Playwright |
| Browser null | C6c | null N=20 pool | `full 0.0` CI contains 0 ≤0.05 (real, N=20 pool, effective_distinct_n>1) | Null Jaccard 0 real N=20 pool |
| Body gradient | G1 | diagnostic N=20 pool | report 1B/2B/4B/39B/86B +CI width/degenerate effective_distinct_n>1 at N=20 | Gradient metrics real N=20 pool |
| Header gradient | G2 | diagnostic N=20 pool | report CC_small/large SC/Vary (+ETag diagnostic 0.0 proving exclusion) +CI width>0 at N=20 pool | Gradient metrics real N=20 pool |
| Cost grouping | validity | check | trajectory-grouped B=5000 groups by trajectory_id (not request), no jitter | cost logs per observation grouped |
| Health gate | validity | check | `0 missing X-Worker-Pid` `0 status None` across 1200 | X-Worker-Pid per observation |
| Per-batch SELECT | validity | check | ≥27 distinct ts, COMMIT verified, `header_only true CLEN/ETag excluded` | batch_state_log.jsonl |
| Scheduling independence | validity | check | `scheduling_confound_r<0.30` body_variant vs drift | per-observation body_variant logs |
| HS256 validation | validity | check | valid JWT `P(200|valid)≥0.90`, header-only true, secret ≥32 | 300 valid JWT success rate |
| Synthetic/cost artifact detection | validity | check | no np.random/hardcoded n*3200/jitter/f*6/body-hash alone/status prefix/relabeled | audit grep cost + structural |

---

## 8. Validity Threats and Mitigations (real HTTP + HS256 >=32 + header-only + honest-cost + >=10 URIs + non-deterministic fixture focus)

1. **HS256 shared-secret not actually shared or still raw Bearer lookup or secret <32 bytes:** Mitigate same `HS256_SECRET>=32` env for both workers, `pyjwt.decode(token, secret, algorithms=['HS256'])` then `SELECT sessions WHERE id=decoded.sid`, log secret hash and len, verify `hs256_valid_success_rate ≥0.90` via real HTTP 300 valid JWTs must yield 200 and secret len logged ≥32; if 0/300 fail or TN inverted or len<32, MEASUREMENT_INVALID.

2. **Shared store file not actually shared or synthetic or hash(body) still present or CLEN/ETag not excluded:** Mitigate create shared file at `/tmp/spider-runtime-35908617140/shared.db` before gunicorn start, verify both workers same `SELECT count(*)`, log DB path, check `batch_state_log` ≥27 distinct ts, grep `run_experiment.py` for `content-length` in structural headers — if CLEN/ETag included or `hash(body)%10000` alone as structural or `f"{status}|"` found, BODY_HASH_STILL_PRESENT / STATUS_PREFIX invalidity.

3. **Honest-cost still n*3200/jitter/f*6.0 or not trajectory-grouped:** Mitigate instrument sum counters in code `_inc('resolve')` etc., log per-observation honest_cost and trajectory_id, sum per trajectory, grep verifies no `*3200` or `random.uniform.*jitter` in cost path and `groupby trajectory_id` for bootstrap; if |rho_shuffled|≥0.20 despite sum counters, diagnostic indicates still bijective.

4. **Scheduling confound (body_variant/f cycling correlated with drift):** Mitigate randomize body_variant and f per request independent of drift with `random.choice` and `scheduling_seed=44`, log per-observation, recompute `scheduling_confound_r`; if ≥0.30, CONFOUND_SCHEDULING_DETECTED invalidity.

5. **Health gate missing (prior 17/1200 missing) or sticky pre-seeded:** Mitigate health-gate startup loop `curl http://127.0.0.1:19851/health` via nginx until 200+X-Worker-Pid 30s; verify 0 missing; for sticky, seed sessions ONLY via POST through nginx to hash-assigned worker (check non-assigned SELECT 0); if >0 missing or dual pre-seed, HEALTH_GATE_FAILED / STICKY_PRESEEDED invalidity.

6. **Per-node baseline not isolating or not real HTTP or <10 URIs:** Mitigate distinct temp files per worker via env `SPIDER_DB_PATH_PER_WORKER` verified different paths via real X-Worker-Pid; ensure all samples real HTTP through nginx (not direct gunicorn); ensure 10 distinct URIs generated with query `?u=` and logged; if only 3 URIs, STICKY_UNDERPOWERED invalidity for skew claim (still evaluable but not gating >0.90).

7. **n_non304 <800 or not exercising real 304 or missing X-Worker-Pid on 401:** Mitigate N=1200 and exercise real 304 only when cache_enabled and If-None-Match sent; verify per request `is_304` from real status 304 and X-Worker-Pid on ALL statuses including 401; health gate ensures 1200/1200 valid.

8. **Body-hash still coupling or inverted TN or header-derived not excluded:** Mitigate ensure structural is header-only Jaccard MINUS body-derived (grep `headers_no_bodyderived`), computing TN as `P(bc<=0.05|valid)` with Wilson CI — inverted formula forbidden (audit grep `1-abs(mean_invalid-mean_valid)`); status-matched canonical body alternative explicitly logged if used.

9. **AgentLab 0.4.2 not on PyPI / Playwright install fails / relabeled direct / effective_distinct_n still 1:** Mitigate `pip install agentlab==0.4.2` with fallback, log version; `npx playwright install chromium --with-deps` conditional; forbid `browser_fetch` calling `requests.get` — must be `page.request.get`; ensure pool introduces variance (50% A_alt) and log effective_distinct_n>1; if still 1, GRADIENT_STILL_DEGENERATE invalidity for ordering but discrimination still evaluable.

10. **CDP AX capture fails or only on index / gradient underpowered (n=3-4) / trajectory-grouped not grouped:** Mitigate `cdpSession.send('Accessibility.getFullAXTree')` per /resource page with fallback; log AX per /resource page at N=20 with pool; ensure gradients N=20 per state (n_a==20) via checks; ensure cost bootstrap groups by trajectory_id with B=5000 (check `groupby` in code); if violated, MEASUREMENT_INVALID per clause.

11. **Decompression CLEN mismatch or not verified for browser at N=20 pool:** Auto-decompress before SHA for both direct and browser; compare decompressed_body_len to body_len; log Content-Encoding per observation at N=20 with pool; verify CLEN==body_len for both.

12. **Degenerate CI misread or synthetic timestamp clustering or hardcoded TOST or wrong bootstrap grouping:** Disclose effective_distinct_n and grouping, treat degenerate at N=20 with pool as still deterministic unexpected (since pool should give width>0); G1/G2 explicitly measure width at N=20 pool with B=1000 browser B=5000 cost trajectory-grouped; check timestamp not clustered within 1-2ms; TOST computed from Fisher z with real n, not hardcoded; cost bootstrap grouped by trajectory_id.

13. **Port collision / stale server / synthetic worker_ids / sticky misconfiguration:** Discover free ports, fresh DB, kill on exit; verify X-Worker-Pid real gunicorn pids not simulated and distribution balanced vs skewed >90% for sticky with >=10 URIs via `write_nginx_conf` hash $request_uri consistent; ensure sticky does not mirror sessions and uses single-worker seeding.

14. **Paid CDN absent:** Explicitly NOT gating; do not trigger MEASUREMENT_INVALID (SUPERSEDED).

15. **Threshold confusion (≥0.85 vs >0.5) or Wilson lower vs point:** C1 uses ≥0.85 mean and Wilson lower >0.75; browser C6 uses >0.5; honest-cost uses |rho_shuffled|<0.20 and within-f std>0; document exact value+CI+grouping.

---

## 9. Preregistration Checklist (Frozen before outcome)

- **Hypothesis:** H1 honest sum-cost sanity, H2 shared WAL header-only freshness with TN/power/orthogonality, H3 sticky >=10 URIs affinity, H4 browser 1280×720 non-degenerate pool — all falsifiable with bounded ceilings.
- **State representation:** Distributed: behavioral_composite graded session_status_check + auth delta (P(bc<=0.05|valid) TN), structural header-only Jaccard MINUS body-derived CLEN/ETag (or status-matched canonical body 31B). Browser: HTTP triple status+decompressed body SHA+filtered headers_no_bodyderived per /resource page with AX>10 DOM 21-82 1280×720. Cost: per-trajectory honest sum counters (resolve+bind+verify+freshness+browser_steps) with trajectory_id grouping.
- **Action representation:** Drift conditions permission_boundary/session_invalidation/signing_key_rotation/token_expiry × cache_enabled, plus noise-only; browser actions body variants A/A_alt 1B/2B/4B/B/C and header isolations CC/ETag/SC/Vary via GET /resource?u= and page.request.
- **Target:** Primary: distributed C1 TN mean≥0.85 Wilson lo>0.75 session_status≥0.85, C2 n_non304≥800 real 304 stratified, C3 stratified |r|<0.15 TOST delta 0.15 header-only with 8/8 variance FP≤0.15, C7 honest-cost |rho_shuffled|<0.20 within-f std>0 trajectory-grouped B=5000; Secondary: sticky TN≥0.85 skew>0.90 >=10 URIs, browser non-degenerate ordering width>0 effective_distinct_n>1.
- **Sampling policy:** Distributed 1200 paired samples via real nginx round-robin health-gated 4-concurrency SEED 44, body_variant/f randomized independent of drift (Cramér's V<0.30), real If-None-Match/ETag 304 ~33% when cache_enabled, per-batch SELECT verified; sticky ≥10 distinct URIs; browser N=20 per state direct+Playwright 1280×720 with non-deterministic pool 50% A_alt, concurrency 4 for null.
- **Unit of analysis:** Distributed: per drift condition endpoint for C1/C2/C3, per observation for correlation (n_non304); cost: per trajectory_id for B=5000 trajectory-grouped bootstrap; browser: per state pair at N=20 for discrimination and per gradient magnitude for ordering with B=1000.
- **Holdout:** No train/test split beyond noise-only holdout for FP; TOST CI uses Fisher z with n_non304; cost shuffled null via trajectory-label permutation B=5000 (grouped).
- **Nulls/baselines:** B-PER-NODE (0.667 fail), B-SHARED-STORE-HEADER-ONLY (≥0.85, |r|<0.15 header-only), B-STICKY-URL-10URI (>90% skew single-worker seeding), B-COST-SHUFFLED (|rho|<0.20 trajectory-grouped), B-STATUS-ONLY/B-BODY-ONLY/B-HEADERS-ONLY/B-HEADERS-NO-BODYDERIVED, noise-only FP≤0.15.
- **Primary metric:** `shared_freshness_stratified_r` header-only (Fisher z TOST delta 0.15) AND `honest_cost_shuffled_rho` trajectory-grouped (|rho|<0.20) — both must pass along with C1 TN, C2 power, C5/C6 browser provision/discrimination for SUPPORTS.
- **Expected direction:** H1: shuffled |rho| low <0.20 (not bijective), within-f std>0; H2: shared TN high ≥0.85 vs per-node 0.667 low, stratified r near 0 within ±0.15 header-only; H3: sticky TN high if affinity suffices; H4: body AvsC high 1.0, header AvsE high 1.0, body-derived excluded gradients 0.0, non-degenerate width>0 ordering.
- **Uncertainty method:** Distributed r: Fisher z 95% CI and TOST p_upper (delta 0.15, n = n_non304 stratified by endpoint, 8 conditions recomputed); C1 TN Wilson 95% per endpoint; cost: trajectory-grouped bootstrap B=5000 resampling trajectory_ids (not requests) with permutation for shuffled rho and percentile CI; browser: bootstrap B=1000 per comparison at N=20 reporting width/degenerate/effective_distinct_n with pool.
- **Adequacy rule:** Validity checks must pass (health gate 0 missing, per-batch SELECT ≥27 distinct ts, HS256 ≥32 rate≥0.90, header-only true with CLEN/ETag excluded, scheduling |r|<0.30, honest-cost no jitter/n*3200/f*6, N=20 per state with effective_distinct_n>1, trajectory-grouped B=5000 groups>1, decompression CLEN==body_len) or else MEASUREMENT_INVALID. Power: n_non304≥800 or else MEASUREMENT_INVALID for power; cost within-f std>0 or else adequate for honesty claim failure.
- **Falsification/survival rule:** SUPPORTS requires ALL C1/C2/C3/C4/C7/C5/C6 with validity green and sticky+gradient reporting non-degenerate. Any C1-C7 fails with validity green => FALSIFIED-IN-SETTING bounded to failing branch (e.g., header-only r≥0.15 => orthogonality falsified even body-agnostic; |rho_shuffled|≥0.20 => honest-cost falsified). C2 power fail with C1/C3 passing => MEASUREMENT_INVALID. Status prefix/body-hash/CLEN not excluded/n*3200/scheduling confound/relabeled/health gate missing => MEASUREMENT_INVALID not falsification. Infrastructure unavailable => MEASUREMENT_INVALID for that branch while others decidable.

---

## 10. Consequences

**Positive (all C1–C7 pass health-gated header-only de-confounded honest-cost trajectory-grouped B=5000 at N=20 pool, with sticky >=10 URIs and non-degenerate gradients reporting):** Both live-substrate blocks plus honest-cost block closed with Director-required hardenings via valid measurement. Distributed TN≥0.85 with n_non304≥800 and header-only orthogonality |r|<0.15 TOST proves body-agnostic header-only plus scheduling/health fixes restore independence that was falsified at 0.721 via body-hash; honest sum counters eliminate bijective artifact proving cost honesty enabling residual-novelty economics; sticky URL-bound >=10 URIs overall skew>0.90 without dual pre-seed proves affinity alternative or need for shared store correctly tested; BrowserGym/AgentLab 0.4.2 + Playwright 1280×720 with AX>10 PC-HEALTH≥80% DOM 21-82 via real browser fetches with non-deterministic pool provisions live browser substrate where fingerprint discrimination and non-degenerate per-value CC/ETag/CLEN gradients with B=1000 CIs enable sensitivity ordering beyond prior degenerate ceiling. Unblocks Graph distributed delta-repair and freshness guards on 2-node gunicorn+nginx and Intel Gate0 harvest and Physics live replication plus Product economics with honest counters (per_hit vs RAG/Stagehand comparison enabled). Claim ceiling expands from single-host loopback EXPERIMENTAL to **distributed shared-store header-only + honest-cost trajectory-grouped + sticky >=10 URI + live browser non-degenerate EXPERIMENTAL (real HTTP, corrected orthogonality, B=5000 honest-cost)**; does NOT promote to VALIDATED or PRODUCT_CORE (still bounded to single-host 2-worker simulation, filtered header set, body 31-117B, single viewport, no paid CDN, no multi-host Redis). Publish as audited harness for graph/product/frontier with frozen sum counters.

**Negative (any C1–C7 fails where validity passes health-gated header-only de-confounded honest-cost trajectory-grouped N=20 pool with effective_distinct_n>1):** Either honest-cost still fails PC-HONEST-COST-SANITY (|rho_shuffled|≥0.20) despite sum counters proving counter design still confounded or grouping wrong; or distributed header-only fails to restore TN≥0.85/n≥800/orthogonality even header-only de-confounded health-gated proving header-only coupling persists via remaining headers (Cache-Control/Vary) or power not achieved falsifying assumed easy body-agnostic fix; or sticky >=10 URIs fails TN≥0.85 proving affinity alone insufficient; or Browser provision/discrimination fails at N=20 pool via valid measurement. Proves per-node failure not fixable by trivial shared file/sticky/header-only filtration or honest-counter instrumentation insufficient, bounding C-MEAS-VALID and C-FRESHNESS to single-host loopback EXPERIMENTAL only with cost artefact still present, preventing false VALIDATED promotion, forcing redesign (true Redis/multi-host or alternative header/body observation like hash canonical success bodies with larger pools or richer header canonicalization, trajectory cost grouping redesign, pool expansion) before scaling. Negative still requires honest-cost trajectory-grouped report and gradient non-degenerate report to diagnose most fragile magnitude and honest-cost rho.

**MEASUREMENT_INVALID (synthetic or body-hash alone/CLEN not excluded/status prefix/confounded scheduling/relabeled direct/n*3200/jitter/f*6 still present/health gate missing/provision failure/pool still degenerate/secret <32):** Prior packet's falsified orthogonality and degenerate w=0 map to parent MIXED; new status prefix, body-hash alone, CLEN/ETag not excluded, n*3200/jitter/f*6, confounded scheduling, relabeled direct, inverted TN, hardcoded TOST, 17 missing, effective_distinct_n 1 map here via 5 hardenings. No ceiling change; requires rerun with real HTTP + correct header-only + trajectory-grouped honest cost per this prereg. Distinguishes measurement failure from scientific falsification; audit will flag `BODY_HASH_STILL_PRESENT`, `CLEN_ETAG_NOT_EXCLUDED`, `STATUS_PREFIX_STILL_PRESENT`, `COST_ARTIFACT_STILL_PRESENT`, `CONFOUND_SCHEDULING_DETECTED`, `HEALTH_GATE_FAILED`, `GRADIENT_STILL_DEGENERATE`, `TRAJECTORY_GROUPING_INVALID`, `SYNTHETIC_DATA_DETECTED`, `BROWSER_FETCH_RELABELED`, `HS256_VALIDATION_STILL_REJECTS_ALL`, `INSECURE_KEY`, `COMMIT_NOT_VERIFIED`, `STICKY_PRESEEDED`.

Both valid outcomes are high-information and will be consumed by Codex as the distributed+browser+honest-cost promotion decision required before any VALIDATED or PRODUCT_CORE claim.

---

## 11. What is NOT Tested (Scope Boundaries)

- **Paid CDN HIT/STALE/SWR/SIE/304 beyond nginx loopback** — explicitly SUPERSEDE per Director, not tested (no credentials, 0% HIT prior).
- Multi-host **Redis cluster** beyond single-host 2-worker WAL shared file at `/tmp/spider-runtime-35908617140/shared.db` / URL-bound sticky >=10 URIs single-worker seeding — single-host tested; true distributed multi-host remains unresolved unless Redis available.
- **TLS/HTTP2/QUIC** beyond plain HTTP 127.0.0.1 termination.
- Browser **DOM/AX beyond HTTP triple** — AX/DOM node counts per /resource page only at N=20 pool.
- Body sizes beyond **31–117B JSON with sort_keys=True** — CLEN==body_len holds for these bodies at N=20 pool.
- End-to-end **LLM inheritance/cross-site holdout** — not measured (runtime substrate only; per_hit vs RAG/Stagehand reported as comparison only with honest counters, not gating).
- Full **304 lifecycle beyond single HIT** (`STALE/SWR`) best-effort via `Age`/`ETag` on origin.
- **HS256 vs RS256 beyond HS256 >=32** — RS256 tested only if available; focus HS256 shared-secret per Director.

---

## 12. Execution Checklist for EXECUTE

- [ ] Implement `run_experiment.py` with fingerprint functions byte-identical to `research/experiments/EXP-RUNTIME-35764329925/run_experiment.py:compute_fingerprint` (status_only, body_only, headers_only, headers_no_bodyderived), sorted lowercased filtered headers, EXCLUDED {Date,Server,X-Request-Id,CF-RAY,CF-Cache-Status,X-Cache,Age} plus X-Worker-Pid, decompression via `response.content` auto-decompressed for direct and via `page.request` body for browser; ensure audit recomputation 0 mismatches and **no hash(body)%10000 alone as structural** (grep verify headers_no_bodyderived for freshness), **no inverted TN formula** (use `P(bc<=0.05|valid)` + Wilson), **no hardcoded TOST constants**, **no n*3200/jitter/f*6 in cost**.
- [ ] Fix HS256 auth plumbing: Flask validates `Authorization: Bearer <JWT>` via `pyjwt.decode(jwt, HS256_SECRET>=32, algorithms=['HS256'])` then `SELECT sessions WHERE session_id=payload['sid']`; generate secret `secrets.token_bytes(32)` hex, log hash and len>=32, verify `hs256_valid_success_rate ≥0.90` (300 valid JWTs yield 200). Emit `X-Worker-Pid` and `ETag` on ALL statuses including 401. Delete prior raw string lookup and short secret.
- [ ] Implement header-only structural and de-confounded scheduling + honest cost: `structural = jaccard(headers_no_bodyderived_json)` where `headers_no_bodyderived = {k:v for k,v in filtered_headers.items() if k not in ('content-length','etag')}` (and optionally canonical body replacement: if status in [401,403] use fixed 31B body SHA), randomize `body_variant` and `f` per request via `random.Random(scheduling_seed + idx).choice(variants)` independent of drift, log `scheduling_confound_r` and ensure <0.30; instrument honest-cost counters `_counters = {'resolve':0,'bind':0,'verify':0,'freshness':0,'browser':0}` incremented per real op, summed per trajectory_id, logged per observation, trajectory-grouped B=5000.
- [ ] Implement health-gated startup + single-worker sticky seeding: `wait_for_nginx()` loops `GET http://127.0.0.1:19851/health` via nginx until 200+X-Worker-Pid 30s; sample only after healthy; verify `raw_freshness_*.jsonl` has 0 lines with `worker_id==None` or `status==None`; for sticky, create sessions via POST through nginx `http://127.0.0.1:19851/admin/ensure_session?...&uri=...` so hash routes to correct worker, verify non-assigned worker SELECT returns 0 before batch; generate 10 distinct URIs with `?u=1..10` distribution.
- [ ] Implement distributed harness with **real HTTP only + HS256 >=32 + header-only + honest-cost**: reuse harness C-FRESHNESS logic with DB modes B-PER-NODE vs B-SHARED-STORE-HEADER-ONLY vs B-STICKY-URL-10URI, seed 44, jitter 50-150ms inter-batch only (cost jitter 0), N=1200 nominal via real nginx round-robin health-gated, honest-cost per trajectory.
- [ ] Extend Flask app with `body_config/header_config` tables, `/api/profile|/data_list|/session/status` endpoints plus `?u=` query for URI entropy, `/resource` with body pool {31B,32B} 50%, Cache-Control/ETag as configured but ETag excluded from freshness Jaccard.
- [ ] Extend provisioning with `pip install agentlab==0.4.2` and `npx playwright install chromium` and non-deterministic pool: per-state body pool draw `random.choice([31B,32B])` per sample for A states, header jitter 50% `max-age 3600 vs 3601` for variance; verify effective_distinct_n>1 per state.
- [ ] Run distributed 1200 + sticky 1200 + browser 520 lines + honest-cost trajectory-grouped B=5000 + browser B=1000, produce `result.json` (stable metric names), `report.md`, `provenance.json` (code SHA, env versions, DB paths, secret hash len, honest-cost counters SHA, header-only flag, distinct URI count), and raw artifacts `raw_freshness_observations.jsonl`, `raw_freshness_per_node.jsonl`, `raw_freshness_sticky_url.jsonl`, `raw_observations.jsonl`, `ax_dom_pages.jsonl`, `batch_state_log.jsonl`.

---

*Preregistration frozen before outcome observation. Any change after seeing confirmatory outcomes is exploratory and requires new preregistration.*

