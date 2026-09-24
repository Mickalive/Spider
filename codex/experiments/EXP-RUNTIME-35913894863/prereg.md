# EXP-RUNTIME-35913894863 — Preregistration

**Experiment ID:** EXP-RUNTIME-35913894863  
**Lane:** runtime  
**Claims:** C-MEAS-VALID (Measurement substrate is intervention-valid), C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)  
**Director Mandate:** REOPEN — allocation REOPEN C-MEAS-VALID, cognitive_reset true, parent_handoff_disposition SUPERSEDE, question: Can runtime close the live-substrate block with a real-HTTP and real-browser hardening: (1) shared SQLite WAL at /tmp/spider-runtime/ with HS256 shared-secret and URL-bound sticky hash $request_uri consistent hash (>=10 distinct URIs, overall skew>0.90, X-Worker-Pid>=10 per worker, health-gated startup, per-batch SELECT commitment verified, If-None-Match/ETag->304 verified, n_non304>=800 stratified across 3 endpoints) to achieve C-FRESHNESS C1 TN>=0.85 (Wilson lower>0.75, session_status>=0.85, per-node baseline 0.667) with stratified |r|<0.15 TOST delta 0.15 p_upper<0.05 8/8 variance FP<=0.15, honest per-trajectory-reset sum counters (resolve+bind+verify+freshness+browser_steps, no jitter, no f*6.0, |rho_shuffled|<0.20 within-f std>0, B=5000 trajectory-grouped) and (2) oracle-free greedy iterative decompression (brotli->gzip MAX_DEPTH 5, no SHA oracle) validated on production CDN HIT/CFCacheStatus HIT and concurrent edge diversity plus stale HIT/SWR/SIE/304 on nginx byte-preserving cache (330/330 prior HIT/DYNAMIC identical) and BrowserGym 0.14.3 1280x720 CDP AX>10 (PC-HEALTH>=80%, DOM 21-82, effective_distinct_n>1) delivering per-value Cache-Control/ETag/Content-Length gradients with B=1000 non-degenerate CIs to order sensitivity beyond degenerate [1.0,1.0] ceiling, published as audited harness for graph/product/frontier?  
**Parent Handoff:** research/experiments/EXP-RUNTIME-35908617140/handoff.json (sha256:6a7f494ed85941b719c8843f7b38fdda4ff12e1b886875349094b203db775721) — disposition SUPERSEDE per director_mandate. Inherited continuity evidence preserved four-way (established/rejected/unknown/do_not_assume) but MUST NOT silently override Director REOPEN decision. Local lane next_question advisory only. This design follows binding Director target claim C-MEAS-VALID and strategic question, using parent handoff as continuity evidence only. Cognitive reset true.  
**Date:** 2026-09-23  
**Dependencies:** EXP-RUNTIME-35908617140 (MEASUREMENT_INVALID 6 mismatches: hash%10000 vs Jaccard, counters cumulative+jitter, wrong TOST tail, dual pre-seed sticky 0.6, browser 0 obs, provenance mismatch), EXP-RUNTIME-35900903994 (MIXED r=0.721 falsified even status-free, degenerate gradients), EXP-RUNTIME-35551516706 (local nginx byte-preserving HIT 330/330 validated), EXP-RUNTIME-35764329925 (loopback fingerprint pipeline)

---

## 1. Question

Can Runtime close the distributed C-FRESHNESS block **and** the honest-cost block **and** the HIT byte-preserving + browser power gaps that keep C-MEAS-VALID EXPERIMENTAL (single-host loopback) and block 3 lanes (Graph delta-repair PARKED, Product honest cost bijective formula FALSIFIED, Frontier mixed-channel ceiling) by applying **six measurement hardenings** to the same Flask 3.1.3 + gunicorn 23.0.0 2× sync + nginx 1.24.0 + BrowserGym 0.14.3 substrate under real HTTP — all in one hardening that maximizes unblocking per cycle per Director comparative reasoning:

1. **Honest-cost hardening:** Replace `cost = n*3200 + Uniform(50,150)` and `f*6.0` tautologies (rho=1.0, shuffled rho>0.20, within-f std 0) with **frozen per-trajectory-reset sum counters** `honest_cost = count_resolve+count_bind+count_verify+count_freshness_checks+count_browser_steps` (each increments once per real operation, per-trajectory reset, summed per trajectory_id, **no jitter, no f×6, no n×3200**) to achieve **PC-HONEST-COST-SANITY: |rho_shuffled|<0.20 trajectory-grouped B=5000, within-f std>0, B=5000 CI width>0**?

2. **Orthogonality hardening (header-only, body-agnostic):** Replace `structural = hash(body)%10000` (auth-dependent error 401/403 JSON bodies coupling to behavioral, stratified r=0.721 CI[0.691,0.748] TOST p=1.0 even status-free r=0.305 CI[0.249,0.358] when CLEN/ETag included) with **header-only Jaccard MINUS body-derived {Content-Length, ETag/W-ETag, Content-Range}** (preserving Cache-Control/Set-Cookie/Vary) OR status-matched canonical body (401/403 mapped to fixed 31B SHA d0ca833f) with **health-gated shared WAL at /tmp/spider-runtime/shared.db plus HS256 shared-secret >=32 bytes** and **de-confounded body_variant vs drift scheduling (r<0.30)** to restore **stratified |r|<0.15 TOST delta 0.15 (CI upper<0.15, p_upper<0.05, pooled |r|<0.15, 8/8 variance, FP<=0.15)** while retaining **C1 mean TN>=0.85 Wilson lo>0.75 session_status>=0.85 and C2 n_non304>=800 via real If-None-Match/ETag->304** stratified 400/endpoint?

3. **Sticky hardening (>=10 URIs, single-worker seeding):** Replace prior `hash $remote_addr` + dual pre-seed + 3 URIs (overall skew 0.666 ceiling, TN null contradiction) with **URL-bound hash $request_uri consistent with >=10 distinct URIs and single-worker seeding via POST through nginx (verified SELECT 0 on non-assigned worker)** to test whether affinity alone substitutes for shared store at **skew>0.90**?

4. **HIT hardening (nginx byte-preserving + production CDN HIT):** Replace untested production CDN HIT (273/273 DYNAMIC-only 0 HIT on free-tier quick tunnel, infrastructure ceiling) with **local nginx proxy_cache byte-preserving cache (330/330 HIT/DYNAMIC identical preserved) plus stale HIT/SWR (stale-while-revalidate)/SIE (stale-if-error)/304 branches** and **production CDN CFCacheStatus HIT with concurrent edge diversity** (2+ concurrent clients to same HIT URL) to validate **oracle-free greedy iterative decompression (brotli->gzip MAX_DEPTH 5, no SHA oracle, 0 ambiguous tie-breaks)** produces **byte-identical decompressed output to ground truth on HIT wire bytes** (>=90% HIT cells correct, DYNAMIC vs HIT byte-identical >=90%, HIT decompressed == ground truth when HIT occurs)?

5. **Browser power hardening (non-degenerate):** Replace deterministic fixture `set_size 1 effective_distinct_n 1 at N=20` (all [1.0,1.0]/[0.0,0.0] width 0) with **non-deterministic fixture** — per-state body pool `A 31B vs A_alt 32B 1B diff 50%` plus header jitter `max-age 3600 vs 3601 50%` — yielding **effective_distinct_n>1 per state at N=20** and **BrowserGym 0.14.3 1280×720 CDP AX>10 median PC-HEALTH>=80% DOM21-82 per /resource** via AgentLab 0.4.2 + Playwright 1.63.0 chromium at **N=20 per state with B=1000 CIs width>0** to order **CC_small vs ETag vs CLEN vs body 1B/2B/4B/39B/86B** sensitivity beyond degenerate ceiling?

This is the narrowest falsifiable step that changes architecture decisions for Graph distributed delta-repair, Product residual-novelty economics, and Frontier/Physics live replication per Director comparative reasoning: alternative micro-tests (header-only isolation alone, localhost Flask writability 1.0 vacuous C4, CDN HIT alone without freshness, per-node 0.667 loop) add no new discriminating power; joint HIT+freshness+hospitality substrate maximizes unblocking per cycle.

---

## 2. Hypothesis

**H1 — Honest-cost (C-MEAS-VALID):** Honest per-trajectory-reset sum counters will pass PC-HONEST-COST-SANITY where n×3200/jitter fails. Trajectory-grouped shuffling (B=5000 permuting trajectory labels) will show |rho|<0.20, within-f families (f = novelty fraction 0,0.25,0.5,1.0) will show std>0, and B=5000 trajectory-grouped bootstrap CI will be non-degenerate (width>0 effective>1), because counters reflect real operation counts not bijective n.

**H2 — Distributed freshness with header-only (C-FRESHNESS+C-MEAS-VALID):** Health-gated (0 missing X-Worker-Pid, 0 status None) shared WAL at /tmp/spider-runtime/shared.db (WAL, check_same_thread=False, COMMIT verified via SELECT count(*) FROM sessions before each batch, batch_state_log >=27 distinct timestamps) plus HS256 >=32 bytes (PyJWT decode, hs_rate>=0.90) plus header-only Jaccard MINUS CLEN/ETag with de-confounded scheduling (body_variant random independent of drift, Cramér's V<0.30) will restore C1 mean TN≥0.85 Wilson lo>0.75 session_status≥0.85 with n_non304≥800 real 304 stratified and orthogonality stratified |r|<0.15 TOST with 8/8 variance FP≤0.15 via real nginx. Per-node baseline same secret isolated DBs will show 0.667 session 0.0.

**H3 — Sticky >=10 URIs (C-FRESHNESS alternative):** URL-bound hash $request_uri consistent without replication, >=10 distinct URIs (e.g., /api/profile?u=1..4, /api/data_list?u=1..3, /api/session/status?u=1..3) and single-worker seeding will achieve mean TN≥0.85 and overall skew>0.90 (per-URI affinity 1.0) via real HTTP health-gated.

**H4 — HIT byte-preserving (C-MEAS-VALID):** Local nginx proxy_cache (Cache-Control public max-age=300, ETag-SHA256) preserves byte-identity 330/330 DYNAMIC vs HIT and stale HIT/SWR/SIE/304 decompressed via oracle-free greedy MAX_DEPTH5 no SHA remain byte-identical to ground truth (≥90% HIT cells correct, 0 ambiguous). Production CDN HIT when observed via CFCacheStatus HIT shows identical preservation (HIT decompressed == ground truth, concurrent edges identical). Prior 273/273 DYNAMIC-only was free-tier ceiling, not falsification.

**H5 — Browser non-degenerate (C-MEAS-VALID):** BrowserGym 0.14.3 + Playwright 1280×720 viewport verified per /resource page, CDP AX>10 median PC-HEALTH≥80% DOM21-82 per /resource at N=20 with non-deterministic pool (effective_distinct_n>1) will preserve body AvsC full 1.0 status 0 headers-no-bodyderived 0 and header AvsE full 1.0 status 0 body 0, and will yield B=1000 CIs width>0 for ≥2 gradient magnitudes (e.g., 1B vs 86B or CC_small vs ETag) enabling ordering beyond prior degenerate [1.0,1.0].

If H1–H5 hold with validity checks passing, the runtime block is closed per Director. Any branch failing with validity green is bounded falsification, not invalidity.

---

## 3. Inherited State — What is Established, Rejected, Unknown (from parent handoff 6a7f49..., preserved four-way, disposition SUPERSEDE)

From EXP-RUNTIME-35908617140/handoff.json (MEASUREMENT_INVALID, 6 required_fixes, not scientific falsification) — parent fixes partially green but instruments off-design; ceilings audit-confirmed bounded to single-host 2-worker localhost simulation, EXPERIMENTAL not VALIDATED.

**Established (bounded, audit recomputed match true, narrowed ceiling — loopback/mimic EXPERIMENTAL):**
- Health-gated distributed harness mechanics SURVIVE: 0 missing X-Worker-Pid and 0 status None across 3×1200 via nginx 1.24.0 127.0.0.1:19851 -> gunicorn 23.0.0 2× sync (shared 603/597, per-node 581/619, sticky 720/480) batch_state_log 31 lines shared /93 distinct ts, per-batch SELECT COMMIT verified.
- HS256 shared-secret shared-store delivers high TN numerically but not creditable to frozen Jaccard: shared arm TN mean 0.976 lo 0.957 (profile 1.0, data_list 1.0, session_status 0.928 lo 0.872) n_non304 1070/1200 after 130 real 304, noise FP 0.0, hs 0.985 670/680, 8/8 variance bc_std 0.24-0.50 — numbers match producer but structural was hash%10000 not Jaccard (audit validity).
- Per-node isolated DB baseline replicates failure: mean 0.6666 Wilson lo 0.573 session_status 0.0 lo 0.0 n_valid173 n_non3041101 hs0.667 r0.180 CI upper0.237 — proves replication necessity persists, but logged db_path ambiguous (all rows log shared.db).
- Scheduling independence holds: body_variant vs drift r0.066 bv_bc0.0489 CramérV0.066 <0.30 on all arms (audit PASS) — de-confounded fix preserved.
- Browser substrate from parent remains last valid ceiling (not extended): AgentLab 0.4.2 importable 0.14.3 absent, Playwright 1.63.0 1280×720 CDP AX median54 PC-HEALTH100% DOM26 via real page.request at N=20 per state (760+760) — this packet adds 0 browser obs (playwright missing), so browser provision/discrimination remain at parent bound.
- Structural off-design characterized: shared/per-node/sticky structural is int(sha256(headers_minus{CLEN,ETag,W-ETag,Content-Range,Cache-Control})[:8],16)%10000 with 9 distinct values 446..8545, not frozen header-only Jaccard 0..1 (audit baseline_findings).
- Local nginx byte-preserving HIT cache validated: 330/330 HIT/DYNAMIC byte-identical, oracle-free greedy decode 60/240 fixed-order vs 330/330 greedy identical, no ambiguous tie-breaks (EXP-RUNTIME-35551516706).

**Rejected (bounded):**
- C-FRESHNESS orthogonality |r|<0.15 with hash(body)%10000 FALSIFIED-IN-SETTING (stratified r=0.721 CI[0.691,0.748] TOST p=1.0 status-free, and r=0.305 CI[0.249,0.358] TOST p=0.999 when CLEN/ETag excluded via hash%10000 with off-design) — do not assume hash(body) can be orthogonal, but do not extend to header-only Jaccard which remains untested with correct instrument.
- Per-node isolated SQLite achieving TN≥0.85 REJECTED (0.6666 session 0.0).
- Sticky overall skew >0.90 with only 3 URIs REJECTED (2/3 ceiling 0.666), sticky TN1.0 as proof of single-worker affinity REJECTED due to dual pre-seed confound; this packet's skew 0.6 with 10 URIs also fails >0.90 but invalid due to dual pre-seed.
- Honest-cost n×3200/jitter and f×6.0 REJECTED as bijective artifact (portfolio assessment).
- Fixed-order iterative decompression through CDN 180/240 failures REJECTED; oracle-free greedy for DYNAMIC 240/240 SURVIVES but HIT was 0% on free-tier (ceiling, not falsification).
- Production CDN HIT DYNAMIC-only 273/273 no HIT is infrastructure ceiling on free-tier quick tunnel, not falsification of HIT byte-preserving.

**Unknown (this experiment directly targets the first six):**
- Whether true header-only Jaccard (MINUS CLEN/ETag only, preserving Cache-Control/Set-Cookie/Vary) achieves stratified |r|<0.15 TOST delta0.15 with health-gated shared WAL+HS256 while retaining C1 TN>=0.85 n_non304>=800.
- Whether per-trajectory-reset honest sum counters (once per real op, no jitter) achieve |rho_shuffled|<0.20 B=5000 trajectory-grouped within-f std>0 and non-degenerate CI width>0.
- Whether sticky URL-bound hash $request_uri consistent with >=10 URIs and single-worker seeding achieves TN>=0.85 and overall skew>0.90 without shared store.
- What per-value CC vs ETag vs CLEN vs body 1B/2B/4B/39B/86B sensitivity ordering is when BrowserGym 1280×720 CDP AX>10 with effective_distinct_n>1 yields non-degenerate B=1000 CIs.
- Whether production CDN HIT (CFCacheStatus HIT) decompressed via oracle-free greedy remains byte-identical to ground truth and concurrent edge identical, and whether stale HIT/SWR/SIE/304 on nginx remain byte-preserving.
- Whether shared WAL generalizes beyond single-host 2-worker localhost to >4 concurrency or multi-host Redis.
- Why sticky TN block reports n_valid0 TN null while raw recomputed gives 446 valid TN1.0 — unresolved assembly contradiction.

**Do not assume (explicitly unsafe, per parent do_not_assume + Director priors + Scout):**
- C-FRESHNESS or C-MEAS-VALID are VALIDATED or PRODUCT_CORE — audit MEASUREMENT_INVALID, ceiling single-host localhost simulation filtered headers body31-117B single viewport no paid CDN no multi-host Redis — EXPERIMENTAL only.
- Degenerate CIs [1.0,1.0]/[0.0,0.0] imply high precision — deterministic set_size1 effective_distinct_n1, not certainty.
- Shared TN 0.976 or noise FP0.0 proves frozen Jaccard orthogonality: structural was hash%10000 not Jaccard.
- Stratified r=0.305 TOST p0.999 proves header-only falsified: instrument excluded Cache-Control and used wrong tail Phi vs 1-Phi correct ~4.5e-08 — true Jaccard unknown.
- Honest rho0.132 proves PC-HONEST-COST-SANITY: counters monotonic corr0.371 with position, B=5000 dummy 1.0 placeholder, hardcoded no_jitter true — cost artifact still present.
- Sticky TN null or skew0.6 proves affinity insufficient: STICKY_PRESEEDED dual DB confounds.
- Browser 0 obs is falsification of localhost->browser generalization: infrastructure missing, last valid ceiling parent MIXED EXPERIMENTAL (AX54 DOM26).
- Provenance trustworthy: github_run_id mismatch 35900903994 vs 35908617140, base_sha mismatch, playwright 1.63 listed while import failed.
- Paid CDN absent or nginx loopback byte-preservation extends to edge: explicitly excluded per SUPERSEDE not gating if nginx HIT passes but must be disclosed.
- 25-byte HS256 secret secure — resize to >=32 bytes.
- Tool/API bypass vs UI replay prior is SPIDER evidence — Director labeled priors: path dependence, compounding planning errors, retrieval is not reasoning, measurement traps, amortized economics are priors not evidence.
- Prefix/Jaccard micro-tuning on synthetic harness generalizes to live browser — parked per Director.

This REOPEN supersedes local lane next_question loop; it tests Director's honesty + body-agnostic + HIT byte-preserving + BrowserGym hardenings, not a repeat of body-hash.

---

## 4. Server Design

### 4.1 Testbed Architecture (three substrates, same Flask base, real HTTP mandatory + HS256>=32 + 6 hardenings)

```
Flask 3.1.3 + PyJWT 2.14.0 HS256 shared-secret >=32 bytes + SQLite WAL (shared vs per-node vs sticky-url) + honest sum counters + nginx HIT cache + BrowserGym
  ├── POST /admin/set_body_variant
  ├── POST /admin/set_headers
  ├── POST /admin/invalidate_session (DELETE sessions, COMMIT, SELECT verification)
  ├── GET  /resource (authenticated GET, status+JSON body+filtered headers, Cache-Control, ETag-SHA256, If-None-Match->304, X-Worker-Pid on ALL statuses)
  ├── GET  /api/profile, /api/data_list, /api/session/status (C-FRESHNESS, cacheable, sticky URI ?u=)
  ├── GET  /health (nginx+gunicorn health gate 200+X-Worker-Pid)
  ├── POST /admin/ensure_session (creates session via POST through nginx to hash-assigned worker only)
  └── HIT payloads: brotli(q4) and gzip(L1) compressed payloads 48-cell matrix via same origin
```

Substrate D (distributed C-FRESHNESS + honest-cost, primary) — REAL HTTP + HS256>=32 + hardenings:
  Origin gunicorn 23.0.0 2× sync --workers2 --bind127.0.0.1:19860 --timeout30 + nginx1.24.0 127.0.0.1:19851 proxy_pass gunicorn_upstream (proxy_http_version1.1 Connection'' buffering off) round-robin and sticky variant hash $request_uri consistent (NOT ip_hash) with >=10 distinct URIs.
  DB modes + honest-cost:
    B-PER-NODE: isolated file /tmp/spider-runtime/pernode-<worker>.db (WAL, not shared) same HS256 >=32 but isolated — real nginx round-robin health-gated header-only de-confounded sum-cost expected TN~0.667
    B-SHARED-STORE-HEADER-ONLY: single shared /tmp/spider-runtime/shared.db (WAL, shared, check_same_thread=False, HS256 shared-secret, COMMIT per batch >=27 ts) — real nginx round-robin header-only MINUS CLEN/ETag de-confounded sum-cost expected TN≥0.85 |r|<0.15
    B-STICKY-URL-10URI: per-node DBs WITHOUT replication (sessions seeded ONLY via hash-assigned worker POST through nginx, verify SELECT0 on non-assigned) hash $request_uri consistent +10 URIs — real nginx URL-bound header-only de-confounded sum-cost expected TN≥0.85 skew>0.90
  Honest-cost: counters resolve/bind/verify/freshness/browser_steps incremented per real op, per-trajectory reset summed per trajectory_id logged per observation.

Substrate H (HIT byte-preserving) — REAL HTTP + nginx + production CDN:
  Local nginx HIT: proxy_cache with Cache-Control public max-age=300, ETag-SHA256, 48-cell matrix 3 payloads×2 orders×2 chunk sizes×4 Accept-Encoding, two-phase populate (unique URL MISS) vs test (fixed URL HIT) N=5 per cell, stale branches (HIT, SWR stale-while-revalidate, SIE stale-if-error, 304) via Cache-Control directives, oracle-free greedy MAX_DEPTH5 brotli->gzip no SHA per HIT wire bytes vs ground truth SHA256, DYNAMIC vs HIT wire byte-identity check.
  Production CDN HIT: same matrix through production CDN edge (paid zone if available, else free-tier quick tunnel to record 0 HIT ceiling), CFCacheStatus/X-Cache HIT header, concurrent edge diversity via 2+ concurrent clients to same HIT URL, same greedy decode verification.

Substrate B (browser C-MEAS-VALID) — REAL BROWSER FETCHES at N=20 with non-deterministic pool:
  Same origin gunicorn+nginx (shared-store mode) + AgentLab 0.4.2 + Playwright1.63.0 chromium 1280×720 viewport verified per /resource page, CDP Accessibility.getFullAXTree per /resource page AX>10 median PC-HEALTH≥80% DOM21-82 per /resource page, HTTP triple via page.request.get decompressed identical pipeline, direct via requests through nginx sanity, N=20 per state with pool A 31B vs A_alt32B 50% plus header jitter 50% effective_distinct_n>1, B=1000 bootstraps width>0 ordering.
```

Body_config variants `A 31B {"data":"hello","version":1}` SHA d0ca833f, A_alt32B hello! , A1 32B 1B diff, A2 33B 2B, A3 35B 4B, B70B 39B, C117B 86B; header_config Cache-Control max-age=3600 ETag W/fixed Vary Accept-Encoding for baselines; non-deterministic pool adds A_alt mixing 50% per sample.

**Distributed harness real HTTP HS256>=32 header-only honest-cost:** 8 co-occurring drift conditions (permission_boundary, session_invalidation, signing_key_rotation, token_expiry × cache_enabled/disabled) plus 4 noise-only, each paired behavioral+structural samples where structural is header-only Jaccard MINUS body-derived, body_variant randomized independent of drift, real ETag/If-None-Match ~33% when cache_enabled, honest-cost per trajectory. N1200 paired samples via real nginx round-robin health-gated to achieve n_non304≥800 after exclusion, 0 missing.

**HIT harness:** Local nginx 48 cells ×5 reps =240 HIT obs +240 DYNAMIC +330 HIT/DYNAMIC identity + stale branches + production CDN matrix (if HIT available, otherwise record ceiling).

**Browser harness at N=20 pool:** Body states A/A_alt/A1/A2/A3/B/C and header states E combined, CC_small3601 1s CC_large0 ETag_small1char ETag_large changed SC_small/large Vary_small plus header jitter 50% — both direct and browser via page.request at N=20 per state with B=1000.

---

## 5. Measurement

### 5.1 Observation Vector

**Distributed part (per paired sample, real HTTP HS256>=32 header-only honest-cost):**
endpoint (profile/data_list/session_status), cache_enabled bool, status int, body_bytes+body_sha256+body_len+Content-Length, headers_filtered_json, headers_no_bodyderived_json (MINUS CLEN/ETag), headers_no_bodyderived_jaccard float, ETag, Cache-Control, worker_id (X-Worker-Pid 0 missing), behavioral_composite graded session_status_check (401->1.0 403->0.5 500->0.75) + auth delta TN P(bc<=0.05|valid), structural_header_only Jaccard, body_variant, scheduling_seed, drift_condition, is_304 bool real, timestamp, db_path, jwt_valid, hs256_verified, health_gated, honest_cost_per_observation, trajectory_id, honest_cost_per_trajectory, f_novelty_fraction, distinct_uri (sticky >=10)

**HIT part (per HIT cell/observation, real HTTP nginx and production CDN):**
payload_id, serve_order (brotli-first/gzip-first), chunk_size (32/8192), accept_encoding (br/gzip/br+gzip/identity), depth (1-5), raw_wire_bytes_sha, content_encoding header, x_cache/cf_cache_status header, status, is_hit bool, is_dynamic bool, is_stale_hit/swr/sie/304 bool, decompressed_bytes_sha (greedy oracle-free), ground_truth_sha, path (br/gz sequence), ambiguous bool, concurrent_edge_id, bytes_identical_dynamic_vs_hit bool, timestamp, worker_id

**Browser part (per request via direct or Playwright, real HTTP N=20 pool):**
state, status, body_bytes decompressed+body_sha256+body_len+Content-Length, headers_filtered_json, headers_no_bodyderived_json, fingerprint_full/status/body/headers/headers_no_bodyderived SHA256, worker_id, ax_nodes per /resource, dom_nodes per /resource, viewport {1280,720}, pc_health, timestamp, concurrency, fetch_method (direct vs browser_page_request), effective_distinct_n helper, honest_cost_browser_step, content_encoding

### 5.2 Metrics (stable names for AUDIT — frozen for recomputation)

**Distributed C-FRESHNESS (real HTTP HS256>=32 header-only honest-cost, health-gated):**
- `shared_freshness_c1_tn_mean`, `shared_freshness_c1_tn_wilson_lo/hi`, `shared_freshness_c1_tn_session_status/profile/data_list` + Wilson per endpoint
- `shared_freshness_c1_tn_per_node_mean` (B-PER-NODE expected 0.667), `shared_freshness_c1_tn_sticky_url_mean` (>=10 URIs), `shared_freshness_c1_tn_sticky_url_skew` (>0.90), `sticky_min_per_uri_affinity`
- `shared_freshness_n_non304` (>=800), `shared_freshness_n_total/n_304/n_missing_worker` (0 missing)
- `shared_freshness_stratified_r` (header-only Jaccard Fisher z stratified), `shared_freshness_stratified_r_ci_lo/hi`, `shared_freshness_tost_p_upper`, `shared_freshness_tost_pass` delta0.15, `shared_freshness_pooled_r`
- `shared_freshness_fp_noise` (<=0.15), `shared_freshness_c2_variance_pass` (8/8 std>0)
- `shared_freshness_worker_distribution_shared/per_node/sticky` (real counts), `shared_freshness_hs256_valid_success_rate` (>=0.90), `shared_freshness_hs256_secret_len` (>=32), `shared_freshness_structural_header_only` (true CLEN/ETag excluded), `shared_freshness_structural_status_prefix_present` (false), `shared_freshness_scheduling_confound_r` (<0.30), `shared_freshness_canonical_body_used` bool

**Honest-cost C-MEAS-VALID (trajectory-grouped frozen sum):**
- `honest_cost_shuffled_rho` (|rho| trajectory-grouped permutation B=5000), `honest_cost_shuffled_rho_ci_lo/hi`, `honest_cost_shuffled_p`
- `honest_cost_within_f_std_per_f` dict f->std each >0, `honest_cost_within_f_std_min`
- `honest_cost_trajectory_grouped_bootstrap_ci_lo/hi` per f, `honest_cost_b5000_width` (>0), `honest_cost_effective_distinct_trajectories`
- `honest_cost_no_jitter_verified` true, `honest_cost_no_n3200_verified` true, `honest_cost_no_f6_verified` true, `honest_cost_per_trajectory_distribution`

**HIT C-MEAS-VALID (nginx + production CDN, oracle-free greedy MAX_DEPTH5 no SHA):**
- `hit_nginx_hit_rate` (X-Cache HIT / test req), `hit_nginx_bytes_identical_dynamic_vs_hit` (330/330), `hit_nginx_stale_hit_bytes_identical`, `hit_nginx_swr_bytes_identical`, `hit_nginx_sie_bytes_identical`, `hit_nginx_304_bytes_identical`
- `hit_nginx_greedy_correct_rate` (>=0.90 HIT correct), `hit_nginx_greedy_correct_48` (48/48 cells), `hit_nginx_ambiguous_count` (0), `hit_nginx_dynamic_correct_rate` (1.0), `hit_nginx_stability_groups` (6/6), `hit_nginx_depth_correct_rate` (>=0.80), `hit_nginx_large_correct_rate` (>=0.80)
- `hit_production_hit_observed` (bool >=1 HIT), `hit_production_hit_rate` (CFCacheStatus HIT / test), `hit_production_greedy_correct_rate` (when HIT >=0.90), `hit_production_concurrent_edges_identical` (bool), `hit_production_dynamic_vs_hit_identical` (>=0.90 when HIT), `hit_production_bytes_identical_count`
- `hit_oracle_greedy_no_sha_verified` true, `hit_max_depth_5` true

**Browser C-MEAS-VALID (real browser N=20 pool):**
- `bg_provision_ok`, `bg_agentlab_version`, `bg_agentlab_0143_absent`, `bg_playwright_viewport`, `bg_ax_nodes_median` per /resource, `bg_ax_nodes_per_page`, `bg_pc_health_pct` per /resource, `bg_dom_nodes_median` per /resource, `bg_dom_nodes_range_ok`, `bg_effective_distinct_n_per_state` (>1)
- `browser_body_AvsC_full/status/body/headers_no_bodyderived` +CI [lo,hi] width degenerate effective_distinct_n via Playwright N=20 pool
- `browser_header_AvsE_full/headers_no_bodyderived` +CI via Playwright N=20 pool
- `direct_body_AvsC_full` sanity, `direct_header_AvsE_full`
- `browser_null_body_full`, `browser_null_header_full`, `browser_null_403/401_full` +CI N=20 pool
- `browser_gradient_1B_full,2B,4B,39B(AvsB),86B(AvsC)` + per-measure CI/width/degenerate/effective_distinct_n via both direct and browser N=20 pool
- `browser_gradient_CC_small/large, ETag_small/large (diagnostic 0.0 for header-only), SC_small/large, Vary_small` +CI N=20 pool

All Jaccard `1 - |A∩B|/|A∪B|` on headers_no_bodyderived for freshness structural; bootstrap B=1000 browser B=5000 cost trajectory-grouped; Fisher z for distributed r; greedy decompression logged per HIT cell.

### 5.3 Baselines (frozen thresholds)

| ID | Expected distributed (real HTTP HS256>=32 header-only honest-cost health-gated) | Expected HIT | Expected browser (Playwright N=20 non-deterministic) | Purpose |
|----|---------------------|---------|---------|---------|
| B-PER-NODE | TN~0.667 fail n_non304 nominal but C1 fails (HS256>=32 isolated DB header-only de-confounded 0 missing sum-cost) | — | — | Replicates failure is replication not algorithm |
| B-SHARED-STORE-HEADER-ONLY | TN≥0.85 pass n_non304≥800 header-only r TOST within0.15 health-gated (HS256+shared WAL MINUS CLEN/ETag) | — | — | Primary fix shared store + body-agnostic |
| B-STICKY-URL-10URI | TN≥0.85 exploratory >90% skew hash $request_uri >=10 URIs single-worker seeding (real URL-bound) | — | — | Tests affinity alone vs shared store corrected |
| B-COST-SHUFFLED | — | — | honest-cost shuffled |rho|<0.20 B=5000 pass (sum-cost no jitter) | Honest-cost null |
| B-HIT-NGINX-BYTE-PRESERVING | — | 330/330 byte-identical HIT/DYNAMIC, stale HIT/SWR/SIE 304 byte-identical, greedy >=90% HIT correct 0 ambiguous | — | Nginx HIT byte-preserving |
| B-HIT-PRODUCTION-CDN | — | CFCacheStatus HIT >=1 observed, when HIT decompressed==ground truth >=90% concurrent identical | — | Production CDN HIT preservation |
| B-ORACLE-FREE-GREEDY | — | greedy MAX_DEPTH5 no SHA decompressed==ground truth on HIT and DYNAMIC | — | Decompression correctness |
| B-STATUS-ONLY | — | — | 0.0 on 200 vs200 at N=20 both methods | Status isolation |
| B-BODY-ONLY | — | — | 1.0 body-only 0.0 header-only at N=20 | Body signal |
| B-HEADERS-ONLY | — | — | 1.0 via CLEN 1.0 header-only at N=20 | CLEN contrast |
| B-HEADERS-NO-BODYDERIVED | — | — | 0.0 body-only 1.0 header-only CC/SC/Vary at N=20 (ETag excluded) | Independent header |

### 5.4 Sample Size

- Distributed: **N=1200 paired samples nominal via real nginx round-robin health-gated + HS256>=32 + header-only + honest-cost** (8 drift ×~120 each +4 noise×60 +120 extra for 10-URI entropy) targeting **n_non304≥800 after real 304 exclusion** (cache_enabled 50% ×33% real 304=16.5% →1002 non-304 at N=1200) with **0 missing**. Per-batch SELECT and X-Worker-Pid logged. HS256 valid JWTs must achieve 200 on ≥90%.
- HIT nginx: **48 cells ×5 reps =240 HIT +240 DYNAMIC +330 identity checks** via nginx proxy_cache, plus stale HIT/SWR/SIE/304 branches (~40 obs), plus production CDN matrix 48 cells ×3 reps if HIT available via real CDN edge, concurrent edges 2×. Record raw_wire_bytes_sha per HIT observation.
- Honest-cost: **trajectory-grouped B=5000 bootstrap** on honest-cost per trajectory (~120 trajectories from 1200 samples); per-f std>0 shuffled |rho|<0.20, counters frozen before outcomes.
- Browser: **N=20 per state nominal via direct + via real Playwright 1280×720 with non-deterministic pool** (body60+gradient60+header40+isolations140+nulls80+classic80=~520 raw lines with ax/dom per /resource page at N=20 with effective_distinct_n>1). Concurrency4 for null and at least one body/header branch. Gradients B=1000 with N=20 must be non-degenerate width>0 (requires pool). Sticky >=10 URIs adds ~170 lines.

---

## 6. Decision Rule (Frozen — no post-hoc weakening, real HTTP HS256>=32 header-only honest-cost >=10 URIs N=20 pool oracle-free no SHA MAX_DEPTH5 required)

**SUPPORTS** (all three substrates close block with hardenings) iff **ALL** mandatory conditions hold with validity checks passing and **no synthetic data** and **HS256>=32 validates** and **header-only body-agnostic MINUS CLEN/ETag** and **de-confounded** and **health-gate 0 missing** and **honest sum counters (no jitter, no n×3200, no f×6.0) trajectory-grouped B=5000** and **oracle-free greedy MAX_DEPTH5 no SHA**:

1. **C1-FRESHNESS (distributed TN, real HTTP HS256>=32 header-only health-gated):** shared-store header-only arm **mean TN ≥0.85** across 3 endpoints (session_status, profile, data_list) with each Wilson95 lower>0.75 and **session_status individually ≥0.85**, computed as P(behavioral<=0.05|valid) with header-only structural and de-confounded scheduling and health-gate 0 missing, while **B-PER-NODE baseline mean TN <0.85** (expected ~0.667 session 0.0) replicating failure via real HTTP + same HS256>=32 header-only honest-cost — proves shared store not tautological. Must have hs256_valid_success_rate≥0.90 structural_header_only==true (CLEN/ETag excluded) scheduling r<0.30 hs256_secret_len>=32.
2. **C2-FRESHNESS (power, real 304 health-gated):** **n_non304 ≥800** after excluding real 304 (is_304==false via real If-None-Match/ETag stratified 400 per endpoint with per-batch SELECT) with **0 missing X-Worker-Pid and 0 status None**.
3. **C3-FRESHNESS (orthogonality, real header-only de-confounded health-gated):** stratified pooled Pearson **r equivalence TOST within delta=0.15**: **95% Fisher z CI upper <0.15 AND TOST p_upper <0.05** (and CI lower>-0.15), **pooled |r|<0.15**, with **8/8 variance std>0** for both signals and **noise FP ≤0.15 (C4)** on shared-store header-only arm via real HTTP + fixed cost. If C3 fails where validity passes (header-only true CLEN/ETag excluded canonical optional de-confounded 0 missing) orthogonality is FALSIFIED-IN-SETTING bounded to header-only harness.
4. **C4-FRESHNESS (noise, real header-only):** noise-only FP ≤0.15 Wilson upper on shared-store via real HTTP header-only 0 missing.
5. **C7-HONEST-COST (real sum counters trajectory-grouped B=5000):** **|rho_shuffled|<0.20** via trajectory-grouped permutation B=5000 shuffling trajectory labels on honest sum counters (no jitter no n*3200 no f*6.0 verified via grep) **and within-f std>0 for each f>0** and **B=5000 95% CI width>0** effective distinct trajectories>1. If |rho|≥0.20, PC-HONEST-COST-SANITY fails →FALSIFIED or MEASUREMENT_INVALID per falsifier.
6. **C8-HIT-NGINX (real nginx HIT byte-preserving, oracle-free no SHA):** **330/330 HIT/DYNAMIC byte-identical wire bytes** (raw_body_sha identical) and **stale HIT/SWR/SIE/304 decompressed byte-identical to ground truth** via oracle-free greedy MAX_DEPTH5 brotli->gzip no SHA oracle, with **≥90% of HIT observations greedy_correct** (decompressed SHA == ground truth) across 48 cells×5 reps, **0 ambiguous tie-breaks**, **DYNAMIC vs HIT identity >=90%**, **stability 6/6** depth/large >=80% if tested.
7. **C8-HIT-PRODUCTION (real production CDN HIT, oracle-free no SHA, when HIT available):** When **CFCacheStatus HIT observed (>=1 HIT)** via real production CDN edge, **HIT decompressed via oracle-free greedy == ground truth for >=90% of HIT observations** and **concurrent edges (2+ clients) identical decompressed bytes** and **DYNAMIC vs HIT byte-identical >=90%** where HIT produced. If 0 HIT on free-tier quick tunnel despite Cache-Control public max-age=300, record as **infrastructure ceiling not falsification** (nginx HIT alone can satisfy C8 for SUPPORTS with production ceiling disclosed).
8. **C5-BROWSER-PROVISION (real Playwright N=20 non-deterministic to /resource):** AgentLab0.4.2 importable 0.14.3 correctly absent, Playwright viewport1280x720 verified per /resource page, **CDP AX nodes median >10 per /resource pages and PC-HEALTH≥80% per /resource and DOM21-82 per /resource via real Playwright at N=20 with effective_distinct_n>1 per state**.
9. **C6-BROWSER-DISCRIMINATION (real browser fetch N=20 pool to /resource):** browser body-only **AvsC full>0.5 expect1.0 status0 headers-no-bodyderived0** and browser header-only **AvsE full>0.5 headers-no-bodyderived1.0 status0 body0 CLEN31==31 via real Playwright at N=20 pool** (direct sanity also1.0 at N=20). Nulls concurrent each full0.0 CI contains0.0 point≤0.05 at N=20 pool. Gradients must report with **width>0 for ≥2 magnitudes** effective_distinct_n>1 to claim ordering.

**Gradient reporting mandatory (exploratory but required for high information at N=20 pool — must be non-degenerate for ordering):**
- `G1_BODY_MAGNITUDE`: for each body gradient AvsA1 1B AvsA2 2B AvsA3 4B AvsB39B AvsC86B report Jaccard full/body/headers/headers_no_bodyderived and CI[lo,hi] width degenerate effective_distinct_n via both direct and browser at N=20 pool — ≥2 must be width>0.
- `G2_HEADER_MAGNITUDE`: for each header gradient CC_small3601 1s CC_large0 SC_small SC_large Vary_small (ETag isolations diagnostic 0.0 for header-only proving exclusion) same reporting via both at N=20 pool.

**Sticky exploratory (not gating SUPPORTS but high-information, health-gated header-only single-worker seeding >=10 URIs):**
- `E4_STICKY_URL`: sticky URL-bound hash $request_uri consistent with >=10 distinct URIs without replication TN≥0.85 with >90% overall skew vs per-node0.667; if sticky fails where validity passes (health-gate 0 missing header-only true single-worker seeding real HTTP without mirroring) => sticky FALSIFIED affinity alone insufficient per corrected design.

If any C1–C8 fails where validity checks pass (health-gate 0 missing header-only true CLEN/ETag excluded de-confounded real HTTP HS256>=32 correct sum-cost no jitter N=20 pool effective_distinct_n>1 HIT HIT produced oracle-free no SHA) => **FALSIFIED-IN-SETTING** bounded to failing branch (e.g., C3 header-only still |r|≥0.15 => orthogonality FALSIFIED even body-agnostic). If C2 power fails <800 with C1/C3 passing => **MEASUREMENT_INVALID**. If HS256 valid JWTs still all401 (0/300) or secret<32 => **MEASUREMENT_INVALID HS256_VALIDATION_STILL_REJECTS_ALL/INSECURE_KEY**. Any hash(body) alone as structural, CLEN/ETag not excluded, status prefix, confounded scheduling detected (|r|>0.30), synthetic generation, inverted TN formula, hardcoded TOST, relabeled direct-as-browser, n×3200/jitter/f×6.0 in cost, SHA oracle used, health-gate missing (>0 missing) triggers **MEASUREMENT_INVALID** per falsifier. Infrastructure-unavailable branches map to **MEASUREMENT_INVALID** not falsification: gunicorn/nginx unavailable, shared store file creation fails, Playwright not installable, CDP capture not available per /resource, AgentLab0.4.2 not on PyPI, production CDN paid zone unavailable (nginx HIT alone evaluable) => respective branch MEASUREMENT_INVALID while others can still be decided. **Paid CDN absent is NOT invalidity for SUPPORTS if nginx HIT passes** per SUPERSEDE (explicitly excluded not gating) but must be disclosed. Degenerate CI expected only if pool fails to introduce variance; with pool effective_distinct_n>1 width>0 expected.

**Exploratory (not gating but reported):**
- E1_CI_NONDEGENERATE: width0 vs>0 per browser comparison at N=20 pool effective_distinct_n per state.
- E2_FOLDING: case/whitespace/order folded E variant full0.0 if normalized.
- E3_EDGE_VISIBILITY: X-Worker-Pid distribution per store mode (real health-gated >=10 URIs) and HIT X-Cache/CF-Cache-Status distribution per edge.
- E4_STICKY_URL: sticky >=10 URIs without replication TN and overall/per-URI skew vs shared-store.
- E5_HONEST_COST_RHO: shuffled |rho| vs n×3200 tautology contrast trajectory-grouped.
- E6_CANONICAL_BODY: compare header-only Jaccard vs status-matched canonical body hash orthogonality sensitivity.
- E7_HIT_CONCURRENT: production CDN concurrent edge diversity identical bytes count.
- E8_HIT_STALE: stale HIT/SWR/SIE/304 byte-preserving per branch.

---

## 7. Controls Summary

| Control | ID | Type | Threshold (real HTTP HS256>=32 header-only honest-cost health-gated N=20 pool oracle-free no SHA) | Evidence |
|---------|----|------|-----------|----------|
| Distributed TN shared header-only | C1-FRESHNESS | positive | mean ≥0.85 Wilson lower>0.75 session_status≥0.85 P(bc<=0.05|valid) hs_rate≥0.90 header_only true CLEN/ETag excluded scheduling |r|<0.30 secret>=32 0 missing | TN per endpoint via real nginx shared store header-only Jaccard |
| Distributed TN per-node baseline | B-PER-NODE | negative | mean ~0.667 <0.85 session 0.0 (real + HS256>=32 same secret header-only honest-cost 0 missing) | Replicates failure via real nginx round-robin |
| Distributed TN sticky URL >=10URIs | B-STICKY-URL-10URI /E4 | positive exploratory | mean ≥0.85 overall skew>0.90 hash $request_uri >=10 URIs single-worker seeding 0 missing | TN/distribution sticky URL-bound corrected |
| Power n_non304 | C2-FRESHNESS | validity/power | ≥800 after real 304 +0 missing header-only | Count from raw_freshness real is_304==false stratified |
| Orthogonality stratified r header-only | C3-FRESHNESS | equivalence TOST header-only de-confounded | CI upper<0.15 p_upper<0.05 |r|<0.15 8/8 variance scheduling |r|<0.30 | Fisher z stratified real header-only |
| Noise FP | C4-FRESHNESS | null | ≤0.15 header-only real 0 missing | Noise-only FP real header-only |
| Honest-cost sanity | C7-HONEST-COST | positive PC-HONEST-COST-SANITY | |rho_shuffled|<0.20 B=5000 trajectory-grouped within-f std>0 B=5000 width>0 no jitter/no n*3200/no f*6 | Shuffled rho per trajectory sum counters |
| HIT nginx byte-preserving | C8-HIT-NGINX | positive | 330/330 byte-identical HIT/DYNAMIC stale HIT/SWR/SIE/304 byte-identical greedy>=90% HIT correct 0 ambiguous 0 missing | HIT wire bytes via nginx + greedy no SHA |
| HIT production CDN | C8-HIT-PRODUCTION | positive when HIT available | CFCacheStatus HIT>=1 when HIT decompressed==ground truth >=90% concurrent identical DYNAMIC vs HIT >=90% | Production CDN wire bytes + greedy no SHA |
| Browser provision | C5-BROWSER | positive | AgentLab0.4.2 0.14.3 absent viewport1280x720 AX>10 median per /resource PC-HEALTH≥80% per /resource DOM21-82 at N=20 pool effective_distinct_n>1 | pip show CDP per /resource page N=20 pool |
| Browser body discrimination | C6a | positive+isolation N=20 pool | full>0.5 status0.0 headers-no-bodyderived0.0 via real Playwright N=20 pool | Jaccard via Playwright |
| Browser header discrimination | C6b | positive+isolation N=20 pool | full>0.5 headers-no-bodyderived1.0 status/body0.0 CLEN31==31 via real Playwright N=20 pool | Jaccard via Playwright |
| Browser null | C6c | null N=20 pool | full0.0 CI contains0 ≤0.05 real N=20 pool effective_distinct_n>1 | Null Jaccard 0 real N=20 pool |
| Body gradient | G1 | diagnostic N=20 pool | report1B/2B/4B/39B/86B +CI width/degenerate effective_distinct_n>1 at N=20 | Gradient metrics real N=20 pool |
| Header gradient | G2 | diagnostic N=20 pool | report CC_small/large SC/Vary (+ETag diagnostic0.0 proving exclusion) +CI width>0 at N=20 pool | Gradient metrics real N=20 pool |
| Cost grouping | validity | check | B=5000 groups by trajectory_id not request no jitter | cost logs per observation grouped |
| Health gate | validity | check | 0 missing X-Worker-Pid 0 status None across1200 | X-Worker-Pid per observation |
| Per-batch SELECT | validity | check | ≥27 distinct ts COMMIT verified header_only true CLEN/ETag excluded | batch_state_log.jsonl |
| Scheduling independence | validity | check | scheduling_confound_r<0.30 body_variant vs drift | per-observation body_variant logs |
| HS256 validation | validity | check | valid JWT P(200|valid)≥0.90 header-only true secret>=32 | 300 valid JWT success rate |
| HIT oracle-free no SHA | validity | check | grep no ground_truth_sha256 inside greedy loop MAX_DEPTH5 brotli->gzip | code audit greedy loop |
| Synthetic/cost artifact detection | validity | check | no np.random/hardcoded n*3200/jitter/f*6/body-hash alone/status prefix/relabeled | audit grep cost+structural+HIT |

---

## 8. Validity Threats and Mitigations (real HTTP HS256>=32 header-only honest-cost >=10 URIs non-deterministic pool HIT oracle-free focus)

1. **HS256 shared-secret not actually shared or still raw Bearer lookup or secret <32 bytes:** Mitigate same HS256_SECRET>=32 env for both workers, pyjwt.decode(token,secret,algorithms=['HS256']) then SELECT sessions WHERE id=decoded.sid, log secret hash and len, verify hs256_valid_success_rate ≥0.90 via real HTTP 300 valid JWTs must yield 200 and secret len logged ≥32; if 0/300 fail or TN inverted or len<32, MEASUREMENT_INVALID.

2. **Shared store file not actually shared or synthetic or hash(body) still present or CLEN/ETag not excluded:** Mitigate create shared file at /tmp/spider-runtime/shared.db before gunicorn start, verify both workers same SELECT count(*), log DB path, check batch_state_log ≥27 distinct ts, grep run_experiment.py for content-length in structural headers — if CLEN/ETag included or hash(body)%10000 alone as structural or f"{status}|" found, BODY_HASH_STILL_PRESENT / STATUS_PREFIX invalidity.

3. **Honest-cost still n*3200/jitter/f*6.0 or not trajectory-grouped or not per-trajectory reset:** Mitigate instrument sum counters in code _inc('resolve') etc per-trajectory reset, log per-observation honest_cost and trajectory_id sum per trajectory, grep verifies no *3200 or random.uniform.*jitter in cost path and groupby trajectory_id for bootstrap; if |rho_shuffled|≥0.20 despite sum counters, diagnostic indicates still bijective.

4. **Scheduling confound (body_variant/f cycling correlated with drift):** Mitigate randomize body_variant and f per request independent of drift with random.choice and scheduling_seed=44, log per-observation, recompute scheduling_confound_r; if ≥0.30, CONFOUND_SCHEDULING_DETECTED invalidity.

5. **Health gate missing (prior17/1200 missing) or sticky pre-seeded:** Mitigate health-gate startup loop curl http://127.0.0.1:19851/health via nginx until 200+X-Worker-Pid 30s; verify0 missing; for sticky seed sessions ONLY via POST through nginx to hash-assigned worker (check non-assigned SELECT0); if >0 missing or dual pre-seed, HEALTH_GATE_FAILED / STICKY_PRESEEDED invalidity.

6. **Per-node baseline not isolating or not real HTTP or <10 URIs:** Mitigate distinct temp files per worker via env SPIDER_DB_PATH_PER_WORKER verified different paths via real X-Worker-Pid; ensure all samples real HTTP through nginx (not direct gunicorn); ensure10 distinct URIs generated with query ?u= and logged; if only3, STICKY_UNDERPOWERED invalidity for skew claim (still evaluable but not gating >0.90).

7. **n_non304 <800 or not exercising real 304 or missing X-Worker-Pid on 401:** Mitigate N=1200 and exercise real304 only when cache_enabled and If-None-Match sent; verify per request is_304 from real status304 and X-Worker-Pid on ALL statuses including401; health-gate ensures1200/1200 valid.

8. **Body-hash still coupling or inverted TN or header-derived not excluded:** Mitigate ensure structural is header-only Jaccard MINUS body-derived (grep headers_no_bodyderived), computing TN as P(bc<=0.05|valid) with Wilson CI — inverted formula forbidden (audit grep 1-abs(mean_invalid-mean_valid)); status-matched canonical body alternative explicitly logged if used.

9. **HIT byte-preserving fails or HIT produces 0 HIT on free-tier or greedy uses SHA oracle:** Mitigate nginx proxy_cache HIT verification warmup 10 req >=1 HIT, record raw wire bytes sha per HIT cell, greedy loop grep no SHA oracle MAX_DEPTH5, DYNAMIC vs HIT wire identity check logged; if production CDN 0 HIT on free-tier quick tunnel record ceiling not falsification; if greedy <90% correct prove HIT alters bytes or greedy fails.

10. **Production CDN concurrent edge diversity not tested or edge bytes diverge:** Mitigate 2+ concurrent clients to same HIT URL via ThreadPool, log per edge worker and decompressed sha identical check; if diverge record failure.

11. **AgentLab0.4.2 not on PyPI / Playwright install fails / relabeled direct / effective_distinct_n still1:** Mitigate pip install agentlab==0.4.2 with fallback log version; npx playwright install chromium --with-deps conditional; forbid browser_fetch calling requests.get — must be page.request.get; ensure pool introduces variance (50% A_alt) and log effective_distinct_n>1; if still1, GRADIENT_STILL_DEGENERATE invalidity for ordering but discrimination still evaluable.

12. **CDP AX capture fails or only on index / gradient underpowered (n=3-4) / trajectory-grouped not grouped:** Mitigate cdpSession.send('Accessibility.getFullAXTree') per /resource page with fallback; log AX per /resource page at N=20 with pool; ensure gradients N=20 per state (n_a==20) via checks; ensure cost bootstrap groups by trajectory_id with B=5000 (check groupby in code); if violated, MEASUREMENT_INVALID per clause.

13. **Decompression CLEN mismatch or not verified for browser at N=20 pool or MAX_DEPTH exceeded:** Auto-decompress before SHA for both direct and browser; compare decompressed_body_len to body_len; log Content-Encoding per observation at N=20 pool; verify CLEN==body_len for both; enforce MAX_DEPTH5.

14. **Degenerate CI misread or synthetic timestamp clustering or hardcoded TOST or wrong bootstrap grouping or SHA oracle:** Disclose effective_distinct_n and grouping, treat degenerate at N=20 pool as still deterministic unexpected (since pool should give width>0); G1/G2 explicitly measure width at N=20 pool with B=1000 browser B=5000 cost trajectory-grouped; check timestamp not clustered within1-2ms; TOST computed from Fisher z with real n not hardcoded; cost bootstrap grouped by trajectory_id; grep confirms no SHA oracle inside greedy loop.

15. **Port collision / stale server / synthetic worker_ids / sticky misconfiguration / HIT cache key misconfiguration:** Discover free ports, fresh DB, kill on exit; verify X-Worker-Pid real gunicorn pids not simulated and distribution balanced vs skewed>90% for sticky with >=10 URIs via write_nginx_conf hash $request_uri consistent; ensure sticky does not mirror sessions and uses single-worker seeding; HIT cache key = URI (including query) verified via nginx cache key config; ensure stale directives proxy_cache_use_stale and proxy_cache_background_update if testing SWR/SIE.

16. **Paid CDN absent:** Explicitly NOT gating for SUPPORTS if nginx HIT byte-preserving passes; do not trigger MEASUREMENT_INVALID (SUPERSEDE) but disclosed; production HIT branch alone may be MEASUREMENT_INVALID due to 0 HIT ceiling while nginx HIT decides.

17. **Threshold confusion (≥0.85 vs>0.5) or Wilson lower vs point:** C1 uses ≥0.85 mean and Wilson lower>0.75; browser C6 uses>0.5; honest-cost uses |rho_shuffled|<0.20 and within-f std>0; HIT uses 330/330 and >=90% greedy correct; document exact value+CI+grouping+byte-identity.

---

## 9. Preregistration Checklist (Frozen before outcome)

- **Hypothesis:** H1 honest sum-cost sanity, H2 shared WAL header-only freshness with TN/power/orthogonality, H3 sticky >=10 URIs affinity, H4 HIT byte-preserving nginx + production CDN oracle-free greedy, H5 browser1280×720 non-degenerate pool — all falsifiable with bounded ceilings.
- **State representation:** Distributed: behavioral_composite graded session_status_check + auth delta TN, structural header-only Jaccard MINUS body-derived CLEN/ETag (or status-matched canonical body31B). HIT: wire bytes raw_body_sha + Content-Encoding + X-Cache/CF-Cache-Status + decompressed greedy sha vs ground truth. Browser: HTTP triple status+decompressed body SHA+filtered headers_no_bodyderived per /resource page with AX>10 DOM21-82 1280×720. Cost: per-trajectory honest sum counters (resolve+bind+verify+freshness+browser_steps) with trajectory_id grouping. HIT: brotli/q4 gzip/L1 stacked encodings depth1-5.
- **Action representation:** Drift conditions permission_boundary/session_invalidation/signing_key_rotation/token_expiry × cache_enabled plus noise-only; HIT actions 48-cell matrix Accept-Encoding variants and chunk sizes and stale HIT/SWR/SIE/304 directives; browser actions body variants A/A_alt1B/2B/4B/B/C and header isolations CC/ETag/SC/Vary via GET /resource?u= and page.request.
- **Target:** Primary: distributed C1 TN mean≥0.85 Wilson lo>0.75 session_status≥0.85 C2 n_non304≥800 real304 stratified C3 stratified |r|<0.15 TOST delta0.15 header-only 8/8 variance FP≤0.15 C7 honest-cost |rho_shuffled|<0.20 within-f std>0 B=5000; HIT: nginx 330/330 byte-identical stale branches byte-identical greedy>=90% 0 ambiguous production HIT when observed decompressed==ground truth concurrent identical; Secondary: sticky TN≥0.85 skew>0.90 >=10 URIs browser non-degenerate ordering width>0 effective_distinct_n>1.
- **Sampling policy:** Distributed1200 paired samples via real nginx round-robin health-gated 4-concurrency SEED44 body_variant/f randomized independent of drift Cramér'sV<0.30 real If-None-Match/ETag304 ~33% when cache_enabled per-batch SELECT verified; sticky ≥10 distinct URIs; HIT 48 cells×5 reps via nginx proxy_cache and production CDN edge concurrent 2+; browser N=20 per state direct+Playwright1280×720 with non-deterministic pool 50% A_alt concurrency4 for null.
- **Unit of analysis:** Distributed: per drift condition endpoint for C1/C2/C3 per observation for correlation n_non304; HIT: per cell per observation for byte-identity and greedy correctness; cost: per trajectory_id for B=5000 grouped bootstrap; browser: per state pair at N=20 for discrimination and per gradient magnitude for ordering B=1000.
- **Holdout:** No train/test split beyond noise-only holdout for FP; TOST CI uses Fisher z with n_non304; cost shuffled null via trajectory-label permutation B=5000 grouped; HIT holdout is DYNAMIC vs HIT identity.

---

## 10. Analysis Plan (Frozen)

1. **Distributed freshness:** Compute TN per endpoint as P(behavioral<=0.05|valid) with Wilson95 CI via statsmodels, mean TN across 3 endpoints and session_status individually; n_non304 count where is_304==false real status304 stratified per endpoint; stratified pooled Pearson r via Fisher z per endpoint then pooled with CI and TOST upper p =1-Phi((z - atanh(0.15))*sqrt(n-3)) correct tail (audit fix), scheduling_confound_r and CramérV per arm, 8/8 variance std>0 per condition, noise FP Wilson upper. Verify structural_header_only true no status prefix via grep and recomputation header-only vs body-hash; honest-cost trajectory-grouped permutation B=5000 shuffling trajectory labels compute |rho_shuffled| and per-f std and bootstrap CI width>0 (groupby trajectory_id). Health-gate 0 missing HS256 hs_rate>=0.90 secret_len>=32 X-Worker-Pid distribution.

2. **HIT byte-preserving:** For nginx HIT, per cell compare raw_wire_bytes_sha DYNAMIC vs HIT identical count 330/330, per stale branch HIT/SWR/SIE/304 decompressed vs ground truth identical; greedy oracle-free decode per HIT wire bytes (brotli->gzip loop MAX_DEPTH5 no SHA) compute decompressed SHA vs ground truth iterative decode correct rate >=90% per 48 cells×5, count ambiguous where both brotli and gzip succeed at same depth, stability groups byte-stable, depth/large correct rates, DYNAMIC vs HIT identity >=90%. For production CDN, same but filter CFCacheStatus HIT observations, compute greedy correct rate when HIT observed and concurrent edges identical (ThreadPool 2+ identical decompressed sha). If 0 HIT on free-tier, log ceiling.

3. **Browser provisioning/discrimination/gradients:** Verify AgentLab0.4.2 import and Playwright viewport1280x720 per /resource page, CDP AX median>10 PC-HEALTH>=80% DOM21-82 per /resource at N=20 with pool effective_distinct_n>1 per state (distinct body/header variants per state pool). Compute Jaccard full/status/body/headers/headers_no_bodyderived per body AvsC and header AvsE via both direct and browser page.request at N=20 with B=1000 CIs width degenerate effective_distinct_n; nulls 0.0 CI contains0 point<=0.05; gradients per value CC/ETag/CLEN/body1B/2B/4B/39B/86B same reporting via both at N=20 pool width>0 for >=2 magnitudes enables ordering. Verify fingerprint recomputation 0 mismatches and CLEN==body_len after decompression per browser observation.

4. **Sticky exploratory:** Compute TN mean via same P(bc<=0.05|valid) on sticky URL-bound arm without replication single-worker seeding >=10 URIs, overall skew max proportion per worker >0.90 per-URI affinity 1.0 each, X-Worker-Pid distribution skewed vs per-node balanced, header-only structural de-confounded; if TN<0.85 or skew<=0.90 valid => sticky falsified affinity alone insufficient.

All thresholds frozen; no post-hoc weakening; exploratory E1-E8 reported regardless of gating; artifact SHAs logged for audit recomputation 0 mismatches; provenance with correct run_id 35913894863 base_sha 7e9ba27a logged.

---

## 11. Decision Consequences

**Positive (SUPPORTS):** Both live-substrate blocks closed with Director-required honesty fixes without paid CDN strictly required for SUPPORTS if nginx HIT passes: (1) Distributed replication with header-only body-agnostic Jaccard + health-gate + HS256>=32 shared-secret achieving TN>=0.85 n_non304>=800 and orthogonality |r|<0.15 TOST de-confounded with per-node0.667 control and (2) Honest per-trajectory sum counters eliminating n×3200/jitter tautology achieving |rho_shuffled|<0.20 within-f std>0 B=5000 non-degenerate CIs and (3) Sticky URL-bound >=10 URIs overall skew>0.90 without dual pre-seed proving affinity alternative or requiring shared store and (4) HIT nginx 330/330 byte-preserving plus stale HIT/SWR/SIE/304 byte-identical decompressed via oracle-free greedy MAX_DEPTH5 no SHA and production CDN HIT concurrent edge identical when HIT observed and (5) BrowserGym0.14.3+Playwright1280x720 CDP AX>10 PC-HEALTH>=80% DOM21-82 N=20 pool effective_distinct_n>1 delivering non-degenerate B=1000 CIs ordering CC vs ETag vs CLEN vs body beyond degenerate ceiling. Unblocks Graph distributed delta-repair and freshness guards on 2-node gunicorn+nginx trusted shared store or URL-bound sticky, enables honest residual-novelty economics per-trajectory vs RAG/Stagehand, enables HIT-aware decoder product integration, plus Intel Gate0 harvest and Physics live replication. Claim ceiling expands from single-host loopback EXPERIMENTAL to distributed shared-store header-only + honest-cost + sticky >=10URI + nginx HIT byte-preserving + production HIT concurrent edge + live browser non-degenerate EXPERIMENTAL (real HTTP) with corrected orthogonality and cost honesty; does NOT promote to VALIDATED or PRODUCT_CORE (still bounded to single-host2-worker localhost filtered header set body31-117B AgentLab0.4.2 single viewport no paid CDN no multi-host Redis no TLS). Next step WebArena family hold-out or multi-host Redis if gradients ordering achieved.

**Negative (FALSIFIED-IN-SETTING):** Live-substrate block remains falsified despite honesty fixes: either (A) distributed shared-store header-only fails TN>=0.85 or n_non304<800 or orthogonality still fails |r|>=0.15 even header-only MINUS CLEN/ETag de-confounded with validity passing (real HTTP SELECT verified X-Worker-Pid>=10 health-gate 0 missing HS256>=32 correctly validates header-only verified de-confounded) proves header-only Jaccard still couples via non-body headers or power not achieved falsifying assumed easy body-agnostic fix requiring alternative structural (status-matched canonical bodies larger pools richer header canonicalization) before Graph distributed freshness/delta-repair; or (B) honest sum counters still fail PC-HONEST-COST-SANITY |rho_shuffled|>=0.20 or within-f std==0 on real trajectories B=5000 proves sum-counter still confounded or grouping incorrect requiring trajectory-level redesign before residual-novelty economics; or (C) sticky >=10 URIs without mirroring fails TN>=0.85 or skew<=0.90 proving affinity alone insufficient shared store required; or (D) HIT nginx not byte-preserving 330/330 fails or stale HIT/SWR/SIE wire differs from DYNAMIC or oracle-free HIT <90% proves HIT alters bytes or greedy fails on cached requiring HIT-aware decoder redesign; or (E) production CDN HIT decompressed != ground truth or concurrent edges diverge proves production HIT not byte-preserving beyond nginx; or (F) Browser provision/discrimination fails via valid N=20 pool effective_distinct_n>1 (AX<=10 PC<80% DOM outside21-82 or browser isolation fails or gradients remain degenerate width0 despite pool) proves localhost->browser generalization not viable or fixture insufficient. Any negative bounds C-MEAS-VALID and C-FRESHNESS to single-host loopback EXPERIMENTAL only (or honest-cost rejected HIT not preserved browser not generalized), prevents false VALIDATED promotion, forces substrate redesign (Redis, header canonicalization, decompressed CLEN, Playwright/BrowserGym install, HS256>=32, scheduling redesign, non-deterministic pool expansion, paid CDN zone) before scaling. If failure due to synthetic harness body-hash alone CLEN/ETag not excluded status prefix confounded scheduling jitter/n*3200/f*6 SHA oracle relabeled direct health-gate missing => MEASUREMENT_INVALID not falsification.

**Infrastructure ceiling (MEASUREMENT_INVALID):** If gunicorn/nginx unavailable, shared store file creation fails, Playwright not installable, CDP capture not available per /resource, AgentLab0.4.2 not on PyPI, production CDN paid zone unavailable with 0 HIT on free-tier quick tunnel (nginx HIT alone still evaluable => production HIT branch MEASUREMENT_INVALID while distributed+cost+niginx HIT+Browser can still SUPPORTS), oracle-free greedy ambiguous due to MAX_DEPTH exceeded, or any validity check fails (hash(body)%10000 alone CLEN not excluded status prefix synthetic np.random bodies jitter/n*3200/f*6 dual pre-seeded sticky health-gate missing >0 missing SHA oracle used) => MEASUREMENT_INVALID not falsification, requires rerun with real HTTP correct fixes — no ceiling change. Paid CDN absent with 0/273 HIT on free-tier is ceiling not falsification if nginx HIT passes per SUPERSEDE.

---

## 12. Validity Threats Summary

See §8 for 17 threats with mitigations. Key new mitigations for this REOPEN: HS256>=32 bytes resize, header-only MINUS body-derived verified via grep, per-trajectory-reset honest sum counters with trajectory-grouped B=5000 and no jitter, single-worker sticky seeding via POST through nginx SELECT0 verified, correct TOST upper-tail 1-Phi Fisher z, BrowserGym0.14.3 1280×720 CDP AX>10 per /resource pool effective_distinct_n>1, oracle-free greedy MAX_DEPTH5 no SHA oracle verified via grep, nginx 330/330 byte-preserving plus stale HIT/SWR/SIE/304, production CDN CFCacheStatus HIT concurrent edge diversity, nginx cache key URI consistency, all health-gated 0 missing X-Worker-Pid>=10 and per-batch SELECT >=27 ts.

---

## 13. Reproducibility

- Code: research/experiments/EXP-RUNTIME-35913894863/run_experiment.py (SHA logged)
- Config: SEED44 jitter50-150ms between batches not inside cost, ports gunicorn19860 nginx19851, fresh DB/file per run killed/purged
- Env: Flask3.1.3 PyJWT2.14.0 gunicorn23.0.0 nginx1.24.0 AgentLab0.4.2 BrowserGym0.14.3 Playwright1.63.0 chromium 1280×720 CDP
- Artifacts: raw_freshness_observations.jsonl (~1200 lines via nginx X-Worker-Pid is_304 header-only Jaccard honest_cost trajectory_id distinct_uri), raw_freshness_per_node, raw_freshness_sticky_url >=10 URIs, raw_hit_observations.jsonl (~330 HIT/DYNAMIC nginx + production CDN matrix), raw_browser_observations.jsonl (~520 lines direct+browser 1280×720 AX/DOM per /resource N=20 pool effective_distinct_n>1), batch_state_log.jsonl SHA logged, provenance.json with correct run_id 35913894863 base_sha 7e9ba27a and executed run sha, HS256 secret len>=32 hash logged, scheduling_seed logged, greedy path per HIT cell logged, recomputation of Jaccard Pearson TOST rho greedy decode must match 0 mismatches.

