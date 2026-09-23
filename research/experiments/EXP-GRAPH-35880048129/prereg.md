# EXP-GRAPH-35880048129 preregistration

## 1. Question

After provisioning distributed Flask HS256 2-node with shared store (Redis or shared SQLite WAL at `/tmp/spider-runtime-35784838353/shared.db`) and gunicorn 23.0.0 2x sync + nginx 1.24.0 round-robin delivering real requests (If-None-Match/ETag->304 verified, per-batch SELECT commitment verified, X-Worker-Pid distribution >=10 per worker, n_non304>=800 stratified), does C-FRESHNESS orthogonality at delta=0.15 achieve C1 detection TN>=0.85 (Wilson lower>0.75, per-endpoint session_status>=0.85 vs per-node baseline TN~0.667) and maintain stratified r TOST within 0.15 (p<0.05) with confound detection |r|>0.9, thereby unblocking Graph and Runtime downstream freshness-gated inheritance and delta-repair with honest kernel-gated counters?

Binding Director mandate: PIVOT to C-FRESHNESS (action PIVOT, claim C-FRESHNESS, parent_handoff_disposition=SUPERSEDE). Strategic question and dependencies above are binding; inherited `next_question` from EXP-GRAPH-35876306030 is continuity evidence only.

## 2. Hypothesis

C-FRESHNESS orthogonality at delta=0.15 will be CONFIRMED on distributed shared-store infrastructure after replacing per-node independent SQLite session DBs with a shared store. Gunicorn 23.0.0 2x sync workers + nginx 1.24.0 round-robin delivering REAL HTTP requests will preserve both:

1. **C1 rescue**: behavioral detection TN from 0.667 (session_status 0.0) to >=0.85 (Wilson lower>0.75, per-endpoint session_status>=0.85). Root cause in EXP-GRAPH-35611618323 was per-node SQLite non-replication: valid-token+session_id routed to the worker lacking that session_id => validate_session()=False => behavioral_delta=3.0. Shared Redis or shared SQLite WAL (WAL journal_mode, shared table) makes session lookup hit regardless of worker, so valid behavioral_delta==0.

2. **Correlation preservation**: endpoint-stratified pooled Pearson r remains within [-0.15,0.15], 95% CI upper<0.15, TOST p_upper<0.05 at delta=0.15. Prior distributed orthogonality (r=-0.038 CI upper 0.029 TOST p=2.0e-08 n_non304=844 audit PASS) was independent of session store; shared store should not couple behavioral (token/session/auth/status) and structural (ETag/Cache-Control/UUID entropy/SHA) signals under headers-only extraction.

HS256 shared TESTBED_SECRET (already fixed, TP=1.0) + NumpyEncoder JSON fix + headers-only structural signal + V_ETAG_PERMISSION_LEAKAGE fix + stratified pooling are retained. Confound sensitivity |r|>=0.90 will persist, proving pipeline would detect coupling if present.

## 3. Falsifier

C-FRESHNESS orthogonality at delta=0.15 on distributed shared-store infrastructure is **REJECTED (FALSIFIED)** under valid shared-store + gunicorn+nginx delivery if ANY holds:

- (F1) C1 mean TN <0.85 on B-DISTRIBUTED-SHARED (after 304 exclusion) OR Wilson 95% lower <=0.75 OR per-endpoint /api/session/status TN <0.85 OR improvement vs B-DISTRIBUTED-PER-NODE <0.15 (TN_shared - 0.667 <0.15)
- (F2) <2/3 endpoints have non-304 behavioral std>0 OR <2/3 have non-304 structural std>0
- (F3) 95% CI upper of endpoint-stratified pooled r (non-304) >=0.15
- (F4) TOST p_upper >=0.05 at delta=0.15 (one-sided, non-304)
- (F5) |r_enabled - r_disabled| >=2*SE_pooled (cache-mode heterogeneity)
- (F6) B-LOCAL-ONLY |r|>=0.15 (regression)
- (F7) B-CONFOUND-DISTRIBUTED-SHARED |r| <0.90 (strict negative control; prior 0.912 tightened to 0.90 per Director mandate)

Also FALSIFIED if primary stratified r absolute drift >0.10 from prior -0.038 while F7 still passes (shared store coupling).

**MEASUREMENT_INVALID** if n_non304_shared <400 OR shared-store / gunicorn+nginx / real-request validity fails (see §8) or infrastructure prevents collection. MEASUREMENT_INVALID is not falsification.

## 4. Parent chain and inherited state

### 4.1 Director disposition

`directive_mandate.parent_handoff_disposition = SUPERSEDE`. The inherited handoff EXP-GRAPH-35876306030 (C-PARAM-INHERIT single-family pilot, MEASUREMENT_INVALID on kernel/census gates) is preserved below as continuity evidence but does NOT govern this experiment. Target claim is PIVOT to C-FRESHNESS.

### 4.2 Inherited from EXP-GRAPH-35876306030 (C-PARAM-INHERIT, MEASUREMENT_INVALID)

**Established**: (none — 0/7 kernel functions present, git diff empty, 0 tasks)

**Rejected**: (none — MEASUREMENT_INVALID is substrate failure, not falsification; C-PARAM-INHERIT remains EXPERIMENTAL at narrow synthetic ceilings EXP-PRODUCT-33528829801 10/10 single-param, EXP-PRODUCT-33741671686 21/21 harness-only)

**Unknown**: Whether durable distill_parameterized with single-prefix/field-filter/Jaccard>=0.75 would achieve EXECUTABLE>=0.75 binding>=0.90; generalization to durable Docker census; LLM economics; ECE calibration

**Do not assume**: src/spider/kernel.py at HEAD 07a90be2 sha256 46929b3a contains distill_parameterized (grep 0 hits); tests/test_kernel_param_inherit.py exists (missing); census >=10 B tasks exists (data/webarena_verified_v2.json absent); MEASUREMENT_INVALID equals falsification; file-based synthetic success implies Docker success; LLM unavailable invalidates binding gate; transient harness patch substitutes durable commit. — All preserved; this experiment makes NO claims about C-PARAM-INHERIT kernel/census and does not depend on them.

### 4.3 Established for C-FRESHNESS (from carry_forward of EXP-GRAPH-35611618323 + ancestors, Codex)

- C-FRESHNESS orthogonality at delta=0.15 CONFIRMED on LOCAL (stratified r=0.041-0.058 CI upper 0.09-0.125 TOST PASS n_non304=684-844, C1-C7 PASS, audit PASS; reconfirmed r=0.0584 CI upper 0.1254 n=844)
- C-FRESHNESS orthogonality correlation CONFIRMED on distributed 2-node Flask HS256 per-node (stratified r=-0.038 CI upper 0.029 TOST p=2.0e-08 n_non304=844) — first valid distributed correlation after 3 MEASUREMENT_INVALID; C3/C4/C5/C6/C7 PASS, audit V-C3-C4-ORTHOGONALITY-VERIFIED
- HS256 symmetric JWT with shared TESTBED_SECRET resolves token cross-node validation: TP=1.0 tokens valid on any node (RSA bug resolved)
- JSON serialization fix (NumpyEncoder + recursive sanitize) resolves numpy.bool_/NaN persistence
- Behavioral signals TP=1.0 FP=0.0 on deterministic Flask+JWT localhost (EXP-GRAPH-35262258744/35353011131); orthogonality across 8+ mocks r=0.002-0.058
- B-CONCURRENT N=5 no coupling (r=-0.032 CI upper 0.035)
- B-CONFOUND-DISTRIBUTED negative control |r|=0.912 >=0.15 (V2 fixed request_id confound genuine, per-endpoint -0.928/-0.915/-0.897)
- Runtime narrow C-MEAS-VALID on Flask+PyJWT HS256 4 states (discrimination 0.833-1.0) and byte-preserving HIT-cache context; six structural families falsified for C-FRESHNESS frozen gate

### 4.4 Rejected

- C-FRESHNESS reaches VALIDATED/PRODUCT_CORE (not warranted; C1 gate fails on distributed per-node)
- Stateless round-robin without session affinity/shared store sufficient for CONFIRMED (per-node TN=0.667, session_status 0.0)
- Simple-pooled r as metric (biased; stratified pooling correct)
- HTTP caching as common cause raising |r|>0.15 (8+ experiments orthogonal under caching)
- Body-inclusive structural signals as orthogonal (V1 fix headers-only)
- Six structural families (Jaccard, TF-IDF, response-time KS, LDA, field-usage, schema) for frozen gate (falsified)

### 4.5 Unknown

- Whether sticky affinity or shared Redis/SQLite WAL resolves C1 TN=0.0 while preserving orthogonality (this experiment's question)
- Whether orthogonality holds on real CDN hierarchies beyond Flask in-memory simulation
- Whether N>=50 parallel sessions changes correlation beyond N=5
- Whether result generalizes to non-Flask frameworks (Django/FastAPI/Express)
- Whether per-endpoint local /api/data/list r=0.161 p=0.0099 is systematic heterogeneity or noise
- Whether delta=0.10 achievable at n>=1200

### 4.6 Do not assume

- C-FRESHNESS reaches VALIDATED/PRODUCT_CORE after this run (remains EXPERIMENTAL; Flask localhost, not real CDN)
- MEASUREMENT_INVALID equals evidence against orthogonality (it is infra failure)
- Orthogonality correlation is falsified (C3/C4 pass decisively; C1 failure is detection fidelity, not correlation)
- C1 failure applies to all endpoints (only /api/session/status fails; other endpoints TN=1.0)
- HS256 fix incomplete (it is complete for tokens; session replication is separate)
- File-based synthetic C-PARAM-INHERIT success implies production DOM/AX success (bounded ceiling)
- Any of the 7 kernel functions exist at HEAD without grep/sha256/diff proof
- Shared store trivially fixes session (must be verified via SELECT commitment + TN)

## 5. Implementation changes (single manipulated variable)

### Change 1: Shared store (PRIMARY)

Use ONE of:

- **Option A (preferred) — Redis**: `apt install redis` or Docker redis:7, Flask session/ETag table via `redis.StrictRedis(host='127.0.0.1',port=6379,db=0)`. Both workers connect to same Redis. No per-worker SQLite.
- **Option B — Shared SQLite WAL**: `mkdir -p /tmp/spider-runtime-35784838353 && touch shared.db && sqlite3 shared.db 'PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;'` Both Flask workers open same `shared.db` path with `check_same_thread=False` and WAL mode. Verify via `PRAGMA journal_mode` returns `wal`.

Log store type (`redis|sqlite-wal`), path/sha256, and per-batch SELECT commitment (query row count from separate process).

Remove per-node SQLite files for B-DISTRIBUTED-SHARED; their presence is MEASUREMENT_INVALID.

### Change 2: gunicorn + nginx real-request topology

- Install pinned servers: `pip install gunicorn==23.0.0` and `nginx 1.24.0` (or apt nginx 1.24.0).
- Launch: `gunicorn --workers 2 --worker-class sync --bind 127.0.0.1:18971 --bind 127.0.0.1:18972 testbed_server:app` OR two binds; each worker exposes X-Worker-Pid header (`response.headers['X-Worker-Pid']=str(os.getpid())`).
- Nginx upstream:

```nginx
upstream spider_backend {
    server 127.0.0.1:18971;
    server 127.0.0.1:18972;
}
server {
    listen 18980;
    location / { proxy_pass http://spider_backend; proxy_set_header Host $host; }
}
```

- Experiment client MUST request via `http://127.0.0.1:18980` (nginx), not direct Flask ports. Verify by collecting X-Worker-Pid on every non-304 response and asserting >=10 per worker pid (round-robin proof). Log nginx access.log excerpt.

### Change 3: Real HTTP cache verification

For each endpoint batch, send second GET with `If-None-Match: <prior ETag>` and assert at least one 304 observed per endpoint-batch (304_verified). Verify ETag header present on 200 responses. Log 304 counts per baseline (expected ~16% ~164/1008).

### Change 4: Wilson interval + stricter confound

Compute C1 TN Wilson 95% lower (z=1.96) on pooled valid-token non-304 samples. Require Wilson lower>0.75. Tighten C7 to |r|>=0.90.

Preserve from parent: HS256 (shared TESTBED_SECRET, single secret for all workers), NumpyEncoder, V_ETAG_PERMISSION_LEAKAGE, V3 stratified pooling, V1 UUID, 304 exclusion, cache independence except shared session table, headers-only structural signal, behavioral formula token*2+session*3+auth*1+status*2, degenerate handling.

## 6. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-LOCAL-ONLY | Single-node Flask HS256, no distribution, regression guard | \|r\|<0.15 r~0.04-0.06 |
| B-DISTRIBUTED-PER-NODE | 2-node independent SQLite + HS256 round-robin (replicates EXP-GRAPH-35611618323 FAIL) | TN~0.667 session_status 0.0, r=-0.038 \|r\|<0.15 |
| B-DISTRIBUTED-SHARED | PRIMARY: 2-node + SHARED STORE (Redis or shared SQLite WAL at /tmp/spider-runtime-35784838353/shared.db) + gunicorn 23.0.0 2x sync + nginx 1.24.0 round-robin, real HTTP | TN>=0.85 Wilson lower>0.75 session_status>=0.85, r within 0.15 CI upper<0.15 TOST p<0.05 |
| B-CONFOUND-DISTRIBUTED-SHARED | Same shared-store+nginx topology with V2 confound (fixed 'expired' request_id) | \|r\|>=0.90 |

B-DISTRIBUTED-PER-NODE is the comparator; improvement delta = TN_shared - 0.667 must be >=0.15.

## 7. Controls

### Positive control — C1-BEHAVIORAL-DETECTION

Token validation detection on shared-store distributed: behavioral signal correctly identifies expired vs valid tokens with mean TP>=0.85 TN>=0.85 (after 304 exclusion) Wilson lower TN>0.75 session_status TN>=0.85. Valid-token+session_id must validate regardless of worker.

### Null control — C3-C4-ORTHOGONALITY-NULL

Structural std>0 on all non-304 conditions (independent ETag/Cache-Control/UUID entropy), C2 variance >=2/3 endpoints both signals, orthogonality |r|<0.15 with TOST PASS, confound |r|>=0.90 reproduces on shared store. Proves absence of coupling is not insensitive measurement.

## 8. Decision rule (frozen)

CONFIRMED iff ALL hold on B-DISTRIBUTED-SHARED (304-excluded) plus baselines:

- (C1) mean TP>=0.85 AND mean TN>=0.85 AND Wilson 95% lower TN>0.75 AND /api/session/status TN>=0.85 AND TN_shared - 0.667 >=0.15
- (C2) >=2/3 endpoints std>0 behavioral AND >=2/3 structural
- (C3) 95% CI upper of endpoint-stratified pooled r <0.15
- (C4) TOST p_upper <0.05 at delta=0.15 (one-sided)
- (C5) cache-mode heterogeneity |r_enabled - r_disabled| <2*SE_pooled
- (C6) B-LOCAL-ONLY |r|<0.15
- (C7) B-CONFOUND-DISTRIBUTED-SHARED |r|>=0.90
- (V1) real-request validity: X-Worker-Pid >=10 per worker + If-None-Match/ETag->304 verified + per-batch SELECT commitment verified
- (V2) n_non304_shared >=800 (MEASUREMENT_INVALID if <400; if 400-800, report CI half-width and require half-width<=0.08 to claim CONFIRMED, otherwise MEASUREMENT_INVALID)

If ANY C1-C7/V1 fails, outcome FALSIFIES (falsification precedence over MEASUREMENT_INVALID). MEASUREMENT_INVALID only if V2 n<400 OR shared-store/gunicorn/nginx validity fails OR infrastructure prevents collection.

All thresholds, CIs (Fisher z, SE=1/sqrt(N-3)), TOST (one-sided), Wilson interval (z=1.96), per-endpoint n, worker distribution, 304/SELECT logs must be computed and persisted to raw_evidence.

## 9. Conditions

4 baselines × 42 samples/condition/endpoint × 8 conditions (2 auth {valid,expired} × 2 cache {enabled,disabled} × 2 method {read,write}) × 3 endpoints (/api/user/profile, /api/data/list, /api/session/status) = 1008 total per baseline. Estimated ~84% non-304 (shared store may alter 304 rate; log actual). Targets:

| Baseline | Total | Target non304 | Min for validity |
|----------|-------|---------------|------------------|
| B-LOCAL-ONLY | 1008 | ~844 | 400 |
| B-DISTRIBUTED-PER-NODE | 1008 | ~844 | 400 |
| B-DISTRIBUTED-SHARED | 1008 | >=800 | 400 (validity) |
| B-CONFOUND-DISTRIBUTED-SHARED | 1008 | ~844 | 400 |

## 10. Measurement validity threats

1. **Shared SQLite WAL locking**: SQLite WAL with 2 writers may encounter SQLITE_BUSY. Mitigation: retry with timeout 5s (`timeout=5000`), WAL mode, `PRAGMA busy_timeout=5000`; log retries. If busy errors >5% of requests, flag but do not silently fall back to per-node DB.
2. **Redis unavailability**: If Redis not installable, fall back to shared SQLite WAL at pinned path; log choice. Either satisfies Director mandate.
3. **gunicorn worker pinning**: Sync workers may not distribute evenly under low load. Mitigation: 1008 requests ensures ~500 per worker; verify X-Worker-Pid >=10 each. If distribution fails, check nginx config (round-robin not ip_hash).
4. **Nginx not delivering 304**: Nginx may strip/proxy ETag/Cache-Control. Mitigation: `proxy_pass` preserves headers by default; verify ETag present on 200 and 304 observed on conditional GET. If nginx strips ETag, config is MEASUREMENT_INVALID (must fix `proxy_no_cache`/`expires` not set).
5. **304 rate shift**: Shared store may change ETag stability/permissions, altering 304 rate. Does not affect primary metric (304 excluded) but log rate vs prior 16% and explain.
6. **HS256 secret sharing**: Must be single SHARED_TESTBED_SECRET for all workers (generate once). Prior parent generated per-worker secret inside SingleServerManager.start() — that re-breaks tokens. Verify generation outside worker spawn.
7. **Wilson vs simple proportion**: Wilson lower is stricter at n~500; ensure correct formula: (p + z²/2n - z*sqrt(p(1-p)/n + z²/4n²))/(1+z²/n).
8. **Sample composition vs prior**: Per-node baseline must replicate prior TN=0.667 exactly (same HS256, same behavioral formula) to make delta interpretable. Use same run_experiment_distributed.py code path for B-DISTRIBUTED-PER-NODE with only store difference.

## 11. Expected outcomes and consequences

| Outcome | Meaning | Product consequence |
|---------|---------|---------------------|
| CONFIRMED (all C1-C7+V1-V2 PASS) | Shared store rescues C1 TN>=0.85 Wilson>0.75 session_status>=0.85 while r within 0.15 TOST p<0.05 and confound |r|>0.9 on gunicorn+nginx real requests | C-FRESHNESS HYPOTHESIS->EXPERIMENTAL on distributed shared-store production-like topology. Parallel-channel justified with shared store. Unblocks C-DELTA-REPAIR, freshness-gated C-LLM-INHERIT/C-RESIDUAL-NOVELTY, honest kernel counters. No VALIDATED/PRODUCT_CORE |
| FALSIFIED (any C1-C7/V1 fails) | Shared store does not rescue or couples signals or loses confound sensitivity | C-FRESHNESS remains HYPOTHESIS (bounded FALSIFIED on shared-store topology). Product must not deploy parallel-channel without sticky affinity/redesign; identifies architectural barrier. Prevents unsafe inheritance. |
| MEASUREMENT_INVALID | n<400 or X-Worker-Pid<10/worker or 304 not verified or SELECT not committed or infra failure | No scientific inference. Repair pinned path WAL/Redis, nginx/gunicorn versions, 304/SELECT proof, and re-run. Do not revert to per-node pilot. |

Both CONFIRMED and FALSIFIED are high-information: they resolve the sole C1 failure from EXP-GRAPH-35611618323 (90% solved) and change product/Graph/Runtime dependency decisions.

## 12. Sample size and power

- Target n_non304_shared >=800 (1008 total, ~84% non-304 ~844 expected as prior). Minimum 400 for validity.
- Power at delta=0.15: prior CI half-width 0.067 at n=800, 0.054 at n=1200. At n=844 prior CI upper 0.029 vs 0.15, margin 0.121 >> half-width, so TOST highly powered.
- C1 Wilson lower>0.75 requires TN>=0.85 at n_non304_valid ~422 (valid-token half): Wilson lower at p=0.85 n=422 is 0.813 >0.75; at p=0.80 Wilson lower 0.758 marginal. So 0.85 threshold gives buffer.
- Baseline B-DISTRIBUTED-PER-NODE delta >=0.15 ensures improvement not sampling noise.

## 13. Analysis plan

1. Verify infra: Redis or shared SQLite WAL at /tmp/spider-runtime-35784838353/shared.db exists, journal_mode=WAL, gunicorn 23.0.0 --workers 2, nginx 1.24.0 upstream, X-Worker-Pid distribution >=10/worker, If-None-Match/ETag->304 observed, per-batch SELECT commitment logged.
2. Replicate B-DISTRIBUTED-PER-NODE and assert TN=0.667±0.05 and r within [-0.08,0.02] to confirm comparator fidelity.
3. Verify B-LOCAL-ONLY |r|<0.15 (C6).
4. Compute B-DISTRIBUTED-SHARED C1: per-endpoint TN (304-excluded), mean TN, Wilson lower, session_status TN, delta vs 0.667.
5. Compute C2 per-endpoint std>0 3/3.
6. Compute C3 endpoint-stratified pooled r with Fisher-z 95% CI (upper <0.15).
7. Compute C4 TOST p_upper at delta=0.15 (one-sided, p<0.05).
8. Compute C5 cache-mode heterogeneity |r_en - r_dis| vs 2*SE_pooled.
9. Compute C7 B-CONFOUND-DISTRIBUTED-SHARED |r|>=0.90.
10. All C1-C7+V1-V2 PASS => CONFIRMED else FALSIFIES; if validity fails => MEASUREMENT_INVALID.
11. Persist raw_evidence: experiment_data.json (per-request deltas, headers, X-Worker-Pid, ETag, 304 flag, SELECT count), metrics.json (stratified r, CI, TOST, Wilson, per-endpoint), nginx access.log excerpt, shared.db pragma output, worker Pid histogram.

