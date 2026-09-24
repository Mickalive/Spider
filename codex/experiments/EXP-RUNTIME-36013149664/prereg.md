# EXP-RUNTIME-36013149664 preregistration — Minimal Single-Node Honesty Gate REOPEN (Runtime REOPEN, USE)

**Lane:** runtime — **Claim:** C-MEAS-VALID (measurement substrate is intervention-valid)  
**Director mandate:** REOPEN, cognitive_reset=true, parent_handoff_disposition=USE, allocation claim C-MEAS-VALID (global-director-REOPEN, cycle 36012412113, request 192c2f740c1d2d1f48260210)  
**Binding question (Director):** Can the minimal single-node honesty gate be restored with corrected wsgi import path (sys.path insert experiment directory via Path(__file__).parent), factory-pattern directory-before-DB, Flask verified listening on 127.0.0.1:19860 before nginx 1.24.0:19851 health gate (200+X-Worker-Pid retry), real If-None-Match/ETag->304 n_non304>=800 stratified 400/endpoint per-batch SELECT >=10 distinct ts, header-only Jaccard MINUS {Content-Length,ETag,W-ETag,Content-Range} preserving Cache-Control/Set-Cookie/Vary de-confounded |r|<0.30, honest per-trajectory-reset sum-counter (resolve+bind+verify+freshness+browser_steps, |rho_shuffled|<0.20 p>=0.20 via 1000 block perms, within-f std>0, null FP<=0.05 degenerate CI not allowed, within-f std>0), achieving full-vector discrimination >0.5 with full > max(body,status) non-vacuously?

**Inheritance discipline:** Parent handoff `research/experiments/EXP-RUNTIME-36004383518/handoff.json` (MEASUREMENT_INVALID, sha 5504038f5afd3a6ff96c129965259650559d928c42d1b2f254dff03fd7f586c1) is continuity evidence with disposition USE per request. Its `next_question` (single-node honesty gate with factory-pattern WSGI fix, header-only Jaccard, honest sum, HIT 330/330, browser pool) is advisory continuity state. The Director REOPEN cognitive_reset is binding research direction and supersedes local continuation; this design refines the Director question into the smallest rigorous falsifiable experiment, not a drift back to distributed 800-stratified or broader permission/session drift scope (explicitly rejected as premature in Director comparative_reasoning). Four-way distinctions are preserved below — established islands are reused as dependencies, not re-proved; rejected surrogates must not be re-introduced; UNKNOWN is tested here at minimal cost; do_not_assume are explicitly guarded. Director `agent_priors_used` are labeled priors, not SPIDER evidence, distinguished throughout. This experiment is the wsgi+factory-corrected retry of EXP-RUNTIME-36004383518 as recommended in its audit V-NGINX-DUPLICATE-LOCATION-ROOT-CAUSE.

## 1. Hypothesis

**H1-SINGLE-NODE-HONESTY-REOPEN (C-MEAS-VALID):** A minimal single-node Flask 3.1.3 + PyJWT HS256 origin (secret >=32 bytes, SHA logged, real `jwt.decode` HS256 verification at origin `hs256_valid_success>=0.90`) with single SQLite WAL at `/tmp/spider-runtime/36013149664/app.db` (WAL, `check_same_thread=False`, `COMMIT` verified via `SELECT count(*) FROM sessions` per batch, `batch_state_log >=10` distinct timestamps, corrected wsgi import `sys.path.insert(0, str(Path(__file__).parent))` for `create_app()` + factory-pattern `def create_app()` ensuring directory `/tmp/spider-runtime/36013149664` exists BEFORE `init_db`, Flask verified listening on `127.0.0.1:19860` via socket connect retry 30s before nginx) plus **header-only Jaccard** structural (`filtered headers MINUS body-derived {Content-Length, ETag, W-ETag, Content-Range}` preserving `Cache-Control`/`Set-Cookie`/`Vary`, lowercased sorted keys, no `hash(body)%10000`, no status prefix) with **de-confounded scheduling** (`body_variant` random independent of drift, scheduling `|r|<0.30`, Cramers `V<0.30`, SEED=44, jitter 50-150ms between bursts only not inside honest_cost) plus **gunicorn 23.0.0 single worker + nginx 1.24.0:19851 health-gated** (`GET /health` 200 + `X-Worker-Pid` header 0 missing, retry 15x1s, warmup >=1 HIT) plus **honest per-trajectory-reset sum counters** `honest_cost = count_resolve+count_bind+count_verify+count_freshness+count_browser_steps` (once per real op, summed per `trajectory_id`, no jitter, no `n*3200`, no `f*6.0`, trajectory-grouped block permutation `B=1000`) will simultaneously achieve:

- (a) **Real ETag/If-None-Match ->304** with `n_non304>=800` stratified 400 per endpoint (`/api/profile` 400, `/api/data_list` 400, `Cache-Control` public/no-store variants, `ETag` SHA256 of body),
- (b) **Header-only orthogonality** de-confounded `|r|<0.30` `V<0.30` on header-only Jaccard MINUS body-derived (pooled and stratified),
- (c) **Honest-cost non-bijective** trajectory-grouped block `B=1000` `|rho_shuffled|<0.20` `p>=0.20` `within-f std>0` `null FP<=0.05` `width>0` `effective>1`,
- (d) **Full-vector discrimination** `>0.5` with `full > max(body-only, status-only)` by `>=0.05` non-vacuously (`B=1000` bootstrap `width>0` `effective_distinct_n>1`) on body-varying AvsC and header-varying AvsE probe pairs via localhost direct 19860 and nginx single-upstream 19851.

This isolates the three confounded failures that blocked 53 prior runtime experiments (body/header conflation via `hash%10000` r~0.72, bijective cost via `n*3200/jitter/f*6.0` |rho|>=0.20, directory/wsgi race 0/15 health-gate at EXP-RUNTIME-36004383518) at low single-node cost before scaling to distributed `2x gunicorn + nginx shared WAL`. Success publishes the harness for graph/product/frontier consumption; failure proves fixes insufficient even at single-node.

## 2. State representation

- **HTTP state:** `compute_fingerprint(status, decompressed_body_bytes, filtered_headers_no_bodyderived)` = `SHA256(status || decompressed_body_bytes || sorted_filtered_headers_no_bodyderived_json)` where `sorted_filtered_headers_no_bodyderived_json` is `filtered_headers MINUS {content-length,etag,w-etag,content-range}` with lowercased keys, `sort_keys=True`, separators `(',',':')`, bodies auto-decompressed (brotli->gzip greedy MAX_DEPTH5 without SHA oracle) before SHA for direct and nginx passthrough, `EXCLUDED = {Date, Server, X-Request-Id, CF-RAY, CF-Cache-Status, X-Cache, Age, X-Worker-Pid}` excluded from fingerprint but `X-Worker-Pid` logged per observation. HS256 secret len>=32 SHA logged.
- **Structural for orthogonality (B-HEADER-ONLY-JACCARD):** header-only Jaccard `|A∩B|/|A∪B|` on `headers_no_bodyderived` token sets (header-name-value strings). Must preserve `Cache-Control`, `Set-Cookie`, `Vary`. Verification via `grep`: `filter_headers` must exclude the four body-derived keys, must include `Cache-Control`. `hash(body)%10000` alone is forbidden (`BODY_HASH_STILL_PRESENT` => MEASUREMENT_INVALID). Status prefix in structural triggers `STATUS_PREFIX_PRESENT`.
- **Behavioral:** `bc` indicator for `valid` auth state vs `invalid/expired`; `TN = P(bc<=threshold|valid)` reported with Wilson interval if computed, but primary gate is full-vector discrimination (see §4).
- **Honest cost:** per-trace `honest_cost` sum counter keyed by `trajectory_id` (block), not request id or batch.
- **Full-vector vs baselines:** same paired probe pairs evaluated under `B-FULL-VECTOR`, `B-BODY-ONLY` (hash body), `B-STATUS-ONLY` (hash status), `B-HEADERS-NO-BODYDERIVED` (header-only Jaccard) for body-varying (31B vs 117B etc) and header-varying (bodies identical 31B, headers differ CC vs Set-Cookie) conditions.
- **HIT/Browser secondary:** HIT wire bytes and BrowserGym DOM are disclosed as secondary observations not gating primary SUPPORTS (see §7 disclosure).

## 3. Action representation

- Auth/session drift dimension: `valid HS256` vs `expired` vs `invalid` vs `session-deleted` (real PyJWT `jwt.decode` HS256 verify at origin, not raw Bearer lookup). Each paired sample is `(before drift, after drift)` with `body_variant` random independent.
- Header/body manipulations: `body_variant` ∈ {31B, 32B, 70B, 117B} plus `CC_small` vs `ETag` vs `CLEN` header variants for discrimination gradients; `Cache-Control` public `max-age=5` vs `no-store` strata for 304.
- HIT populate vs test (secondary): unique URL (DYNAMIC, cache-bypass) vs fixed URL (HIT) through nginx `proxy_cache public max-age=300` at :19851, warmup 10 req — recorded if executed but not gating.
- Honest-cost trajectories: `f ∈ {0,0.2,0.4,0.6,0.8,1.0}` novelty fraction, `trajectory_id` groups of ~10 observations.
- Factory action: `mkdir -p /tmp/spider-runtime/36013149664` before `init_db`, `gunicorn --workers 1 --bind 127.0.0.1:19860 'run_experiment:create_app()'` factory pattern with `wsgi.py` inserting `sys.path`.

## 4. Target

- **Primary:** Full-vector discrimination `D_full = P(fingerprint differs | body or header varies)` on paired probes (body-varying AvsC, header-varying AvsE) with `D_full>0.5` and `D_full > max(D_body_only, D_status_only)` non-vacuously.
- **Secondary (gating):** Real ETag 304 correctness `n_non304>=800` stratified, header-only orthogonality `r(header_only_Jaccard, behavioral_indicator)` with `|r|<0.30`, honest-cost correlation `rho(honest_cost_per_trajectory, f)` and `|rho_shuffled|` under block permutation `B=1000`.
- **Secondary (disclosed):** HIT byte-identity and BrowserGym provision are reported but not gating primary decision.

## 5. Sampling policy

- **Freshness/304:** `N~1200` paired samples targeting `n_non304>=800` after real `If-None-Match/ETag->304` filtering, stratified `400` per endpoint (`/api/profile` 400, `/api/data_list` 400) with `Cache-Control` public `max-age=5` vs `no-store` sub-strata, `ETag` as SHA256 of body. `SEED=44`, jitter `50-150ms` **between bursts only, not inside honest_cost**. `body_variant` assignment `U{all variants}` independent of drift. Real HTTP via localhost direct `:19860` (or nginx single-upstream passthrough when full-vector overlapped). `X-Worker-Pid` logged per observation (single worker). Per-batch `SELECT count(*) FROM sessions` logged.
- **Honest cost:** Cost trajectories with `f` levels, `trajectory_id` groups of `~10` observations each, honest sum counter incremented once per real `resolve/bind/verify/freshness/browser_steps` call, summed per `trajectory_id`, block permuted by `trajectory_id`.
- **Full-vector discrimination:** Same paired probes as freshness, `B=1000` bootstrap per comparison (body-varying and header-varying separately), `effective_distinct_n>1` via header jitter and body pool if applicable, viewport plain HTTP (no browser required for primary).
- **HIT secondary (if run):** `48` cells ×5 reps `~330` lines if executed via nginx single-upstream; two-phase populate vs test.

## 6. Unit of analysis

- 304/orthogonality/full-vector: **paired sample** (`pre, post, is_304, header_only_Jaccard, fingerprint_full/body/status, drift_label, endpoint, body_variant, trajectory_id, honest_cost, X-Worker-Pid`).
- Honest-cost: **trajectory** (aggregated sum per `trajectory_id`, block = trajectory).
- Secondary HIT: **cell observation** if executed.

## 7. Holdout / stratification

- No ML holdout beyond bootstrap CI construction, but **endpoint stratification is frozen:** `n_non304>=800` must include `>=400` per endpoint (`/api/profile`, `/api/data_list`). Reported metrics must include both stratified and pooled values. `batch_state_log >=10` distinct `count(*) FROM sessions` timestamps required. Missing stratified target triggers `INSUFFICIENT_STRATIFICATION` MEASUREMENT_INVALID, not SUPPORTS. Full-vector reported pooled and per-probe-type (body-varying vs header-varying).

## 8. Nulls / baselines

| ID | Description | Expected behaviour |
|---|---|---|
| **B-FULL-VECTOR** | Full-vector SHA(status||body||headers_no_bodyderived) primary | `>0.5` and `>max(body,status)` by >=0.05 non-degenerate |
| **B-BODY-ONLY** | `hash(decompressed body)` only | `1.0` on body-varying AvsC, `0.0` on body-identical header-only |
| **B-STATUS-ONLY** | `hash(status)` only | `0.0` on `200 vs 200` variants |
| **B-HEADER-ONLY-JACCARD** | Header-only Jaccard MINUS body-derived preserving CC/Set-Cookie/Vary | `|r|<0.30` `V<0.30` de-confounded |
| **B-HEADER-HASH-REJECTED** | Rejected surrogate `hash(body)%10000` / including CLEN/ETag | `r≈0.72` → **REJECTED** (proves conflation) |
| **B-COST-SHUFFLED** | Block-permuted `B=1000` by trajectory_id for honest cost | `|rho_shuffled|<0.20` `p>=0.20` `within-f std>0` |
| **B-HEADERS-NO-BODYDERIVED** | `headers MINUS CLEN/ETag/W-ETag/Content-Range` alone | `0.0` body-only, `1.0` header-only |

Null controls: `NC-ORTHOGONALITY-NOISE` (noise-only structural jitter expecting `|r|<0.30`), `NC-COST-SHUFFLED` (`|rho_shuffled|<0.20 p>=0.20`), `NC-BROWSER-SAME-STATE-ANALOG` (`0.0` when same body resampled via direct/nginx), `NC-HEADER-HASH-REJECTED` (surrogate must fail), `NC-FACTORY-REGRESSION` (module-level init must reproduce prior failure).

## 9. Primary metric & expected direction

- **C1 (304 gate):** `n_non304>=800` stratified `400` per endpoint with `hs256_valid_success>=0.90` and `batch_state_log>=10` distinct ts. **Pass if >=800 and >=400/endpoint.**
- **C2 (orthogonality):** `r = Pearson(header_only_Jaccard, behavioral_indicator)` pooled and stratified, plus `CramersV`. **Pass if `|r|<0.30` and `V<0.30` de-confounded** (Director threshold). Report Fisher-z CI.
- **C3 (honest-cost):** block-permuted `|rho_shuffled|<0.20` `p>=0.20` via `B=1000` (block=trajectory_id), `within-f std>0`, `null FP<=0.05`, `CI width>0` `effective>1`. **Pass if all hold.**
- **C4 (full-vector non-vacuous):** `D_full>0.5` (Wilson or bootstrap lower>0.35) **and** `D_full > max(D_body, D_status) +0.05` with `B=1000` bootstrap `width>0` `effective>1` (non-degenerate) on both body-varying and header-varying sets. Status 0.0 and headers-no-bodyderived 0.0 on body-only as manipulation checks. **Pass if full exceeds baselines non-vacuously.**

Expected: **Pass** for `C1-C4` if wsgi+factory fix, header-only MINUS filter, honest block-permuted sum, and full-vector composition are correct; **Fail** if any confound persists. `B-HEADER-HASH-REJECTED` expected to **fail** even with same data (validates filter necessity). `B-COST-SHUFFLED` expected to correctly remove bijective artifact only after per-trajectory block grouping.

## 10. Uncertainty method

- `n_non304` counts and `hs_rate` Wilson `95%` lower bound.
- `r` Fisher-z transformed CI `95%` with `n_non304` denominator; `CramersV` also; `p` from Fisher-z TOST equivalent for |r|<0.30 bound (correct tail `1-Phi`).
- `rho_shuffled`: block permutation `B=1000` (block=`trajectory_id`), within-f `std` and CI width reported; `effective>1` required; `p` = proportion `|rho_perm| >= |rho_obs|` (two-sided).
- Full-vector `D`: `B=1000` bootstrap per comparison, `effective_distinct_n` and CI width reported; degenerate `[1.0,1.0]` with `effective=1` is **not** precision. Difference `D_full - max(D_body,D_status)` bootstrapped for ordering.
- Per-batch `SELECT` timestamps for commitment verification; health-gate attempts logged.

## 11. Adequacy rule

- `n_non304>=800` with `>=400` per endpoint after filtering `is_304==false` and `hs256_valid_success>=0.90`.
- `batch_state_log >=10` distinct `count(*) FROM sessions` timestamps with `COMMIT` verified.
- `health-gate` `0` missing `GET /health` via origin 200 + `X-Worker-Pid` (retry 30s, Flask verified listening before nginx).
- `wsgi` path insertion and factory pattern verified via `grep` (no module-level `app` before wipe).
- Full-vector `B=1000` with `effective_distinct_n>1` and `width>0` for ordering claim.
- If adequacy fails → `MEASUREMENT_INVALID` (not `SUPPORTS`/`FALSIFIED`). Production CDN `0` HIT is **ceiling** not gating if single-node passes (disclosed).

## 12. Falsification / survival rule

**SUPPORTS (single-node honesty gate restored, harness publishable)** requires **ALL** mandatory with validity passing including wsgi+factory fix:

- `C1` `n_non304>=800` stratified `400` per endpoint `0` missing `hs_rate>=0.90` `batch>=10 ts`.
- `C2` header-only de-confounded `|r|<0.30` `V<0.30` `p` correctly computed on header-only Jaccard MINUS body-derived.
- `C3` `|rho_shuffled|<0.20` `p>=0.20` block `B=1000` `within-f std>0` `FP<=0.05` `width>0` `effective>1`.
- `C4` `D_full>0.5` and `D_full>max(D_body,D_status)+0.05` non-degenerate `width>0` `effective>1` on both probe types.

**FALSIFIED-IN-SETTING:** Any `C1-C4` fails while validity passes (wsgi fixed, health-gated, header-only MINUS correct, honest sum block-permuted correctly, fingerprints decompressed) → bounded falsification on `Flask 3.1.3 + PyJWT HS256 + gunicorn 23.0.0 + nginx 1.24.0` localhost. `B-HEADER-HASH-REJECTED` failure does **not** count as falsification — it is expected.

**MEASUREMENT_INVALID** if any validity gate fails: `hash(body)%10000` alone, `CLEN/ETag` not excluded, status prefix, synthetic `np.random` bodies without HTTP, `jitter`/`n*3200`/`f*6.0` in cost, health-gate missing or Flask not listening verified, directory not before DB, `wsgi` path not inserted, `jwt.decode` not used, recompute mismatch, degenerate CI claimed as precision. Secondary HIT/browser failures do not trigger MEASUREMENT_INVALID for primary gate but are disclosed.

Per contract, `status` describes measurement validity; valid negative is `status=COMPLETE` `outcome=FALSIFIES`, not infrastructure failure.

## 13. Validity threats & mitigations

| Threat | Mitigation | Audited check |
|---|---|---|
| **Body/header conflation** (`CLEN/ETag` in structural) | `MINUS` set enforced via `grep`; `B-HEADER-HASH-REJECTED` proves failure when included | `grep filter_headers` + recompute Jaccard |
| **Factory/directory/wsgi race** (`app=create_app()` before wipe, missing sys.path) | `def create_app()` factory, `mkdir -p` before `init_db`, `wsgi.py` `sys.path.insert Path(__file__).parent`, `gunicorn 'run_experiment:create_app()'`, socket verify `127.0.0.1:19860` retry 30s | `grep` wsgi Path + no module-level init + socket log |
| **Nginx duplicate location** (prior `'[emerg] duplicate location \"/\"'`) | Single `location /` block via corrected `_write_nginx_conf`, `nginx -t` syntax ok before health gate | `nginx -t` log + config SHA |
| **Health-gate race** (Flask not listening before nginx 19851) | Verify Flask listening via socket/curl loop before nginx start, retry GET /health `200+X-Worker-Pid` 15×1s | Health log 0 missing |
| **Bijective honest-cost** (`n*3200`, `f*6.0`, jitter) | Frozen sum `resolve+bind+verify+freshness+browser_steps` per `trajectory_id`, block permutation `B=1000`, `grep` bans | `grep` + `|rho_shuffled|<0.20 p>=0.20` |
| **Scheduling confound** (body_variant correlated with drift) | Random independent assignment + recomputed `Pearson`/`CramersV <0.30` | `r`/`V` recompute |
| **Degenerate CI** (`[1.0,1.0]` with `effective=1` claimed as precision) | `B=1000` width>0 mandatory, `effective_distinct_n>1`, difference bootstrap for ordering | `effective_distinct_n` audit |
| **Single-node vs distributed confusion** | Explicit scope: single-node only, distributed shared-WAL `UNKNOWN` | `provenance` path notes `/36013149664/app.db` single file |
| **Raw Bearer lookup tautology** (no jwt.decode) | `grep` must show `jwt.decode` HS256, `hs256_valid_success>=0.90` | Code + metric |

## 14. Consequences

- **If SUPPORTS:** Minimal honesty gate closes and harness publishes. Single-node `n_non304>=800` + `|r|<0.30` + `|rho_shuffled|<0.20 p>=0.20` + `D_full>0.5` `full>max(body,status)` non-vacuously validates the audited harness cross-lane needs. Claim ceiling expands from `local nginx island EXPERIMENTAL` (`EXP-RUNTIME-35551516706 330/330`) to `single-node honest substrate EXPERIMENTAL` (real HTTP `127.0.0.1:19860/19851`, `31-117B`, single viewport, health-gated factory+wsgi-fixed) — does **not** promote `C-MEAS-VALID` to `VALIDATED`/`PRODUCT_CORE` (still bounded single-host). Publishes `research/experiments/EXP-RUNTIME-36013149664/` harness and `substrates/` for graph/product/frontier reuse. Authorizes next experiment: distributed `HS256` shared-WAL `800`-stratified HIT (`2x gunicorn 19860+19861` via `nginx 19851` round-robin/hash `$request_uri` with `>=10` URIs) and honest residual-novelty economics vs `RAG`/`Stagehand` Pareto.
- **If FALSIFIED-IN-SETTING (valid):** Honesty fix insufficient even at single-node with factory+wsgi fix. Bounds `C-MEAS-VALID` to loopback `EXPERIMENTAL` without compositive discrimination, prevents false `VALIDATED` promotion, forces true header canonicalization / counter grouping / nginx config redesign before distributed. Distributed hypotheses remain `UNKNOWN`.
- **If MEASUREMENT_INVALID:** Synthetic or validity breach — no ceiling change, requires fixed rerun per parent `recommended_action` (wsgi, factory, nginx config, jwt.decode, header-only MINUS, block-permuted sum, health gate). Distributed hypotheses stay `UNKNOWN`.

## 15. Parent handoff continuity (USE, cognitive_reset true)

- **Established (reused, not re-proved, from handoff + Codex):** `local nginx 1.24.0 proxy_cache byte-preserving HIT 330/330` (`EXP-RUNTIME-35551516706` `240/240` `330/330` `0` ambiguous audit PASS) as dependency; `C-FRESHNESS` orthogonality at `delta0.15` confirmed only on localhost mock `n=480` (`EXP-GRAPH-35389145821` `r=0.0022` `CI upper 0.0916` `TOST p0.0006` audit PASS) — not superseded; `code readiness` declared (HS256 len 49 >=32, `filter_headers` excludes CLEN/ETag, jitter between bursts only) but blocked by health gate and requires re-verification after wsgi+factory fix; prior distributed correlation at `EXP-GRAPH-35611618323 r=-0.0381 TOST p2e-08 n844` but per-node C1 mean TN 0.6667 remains bounded ceiling for distributed shared-store.
- **Rejected (must not reuse, per handoff):** `per-node isolated SQLite` achieving `TN>=0.85` (`mean 0.6666 session 0.0`) — shared replication required for distributed; `hash(body)%10000` as header-only surrogate (`r=0.721` `p=1.0` status-free 0.305) — do not extend to frozen header-only Jaccard; `honest-cost n*3200/jitter/f*6.0` bijective artifact — synthetic stubs not executed do not rehabilitate honesty; fixed-order iterative decompression `180/240` failures and sticky `skew>0.90` with 3 URIs `ceiling 0.666` — require `>=10` URIs hash.
- **Unknown (tested here at single-node with wsgi+factory fix):** Whether health-gated single Flask HS256>=32 with `sys.path Path(__file__).parent` wsgi and directory exists before `/tmp/spider-runtime/36013149664/app.db` and Flask bound verified before nginx health gate achieves `C1` `n_non304>=800` stratified `400/endpoint` per-batch SELECT >=10 distinct ts and `C2` header-only Jaccard `MINUS {CLEN,ETag,W-ETag,Content-Range}` de-confounded `|r|<0.30` and `C3` honest sum `|rho_shuffled|<0.20 p>=0.20` `within-f std>0` and `C4` full-vector `>0.5` `full>max(body,status)` non-vacuously; whether `B-HEADER-HASH-REJECTED` reproducibly fails; whether single-node generalizes beyond `127.0.0.1` plain HTTP (TLS/HTTP2/QUIC, multi-host Redis, production CDN — out of scope); whether distributed shared-WAL `2x gunicorn` via nginx achieves distributed C1 — remains UNKNOWN pending this gate.
- **Do-not-assume (guarded):** Do not assume `0.0` metrics from prior `0/15` health-gate are falsification (null not falsification per EXPERIMENT_PACKET.md s1); do not assume degenerate `CIs [1.0,1.0]` with `effective=1` is precision; do not assume prior `TN 0.976 / r 0.721 / rho 0.132` from prior `MEASUREMENT_INVALID` prove frozen hypotheses (conflated surrogates); do not assume `C-MEAS-VALID`/`C-FRESHNESS` are `VALIDATED`/`PRODUCT_CORE` (audit `MEASUREMENT_INVALID`, ceiling `EXPERIMENTAL`); do not assume paid CDN `0` HIT falsifies byte-preserving; do not treat Director labeled priors (path dependence, compounding salience, thresholded fingerprint, parameterization orthogonality, tool bypass, degeneracy) as SPIDER-established evidence — they are priors requiring hardenings; do not infer beyond localhost mock without `n_non304>=800` and correct block permutation.
- **Director priors distinguished:** `agent_priors_used` (path-dependent salience pollution, thresholded fingerprint caching ECE<=0.15, parameterization Jaccard<0.30 orthogonal families, O(1) tool bypass, degeneracy heterogeneous `|S|>=16`, cost structure/budget-matched baselines, evaluation variance) are explicitly labeled priors used to require `header-only MINUS`, `block-permuted` sum, `full>max` non-degenerate guards — not SPIDER evidence. This design tests them falsifiably.

## 16. Estimated cost & information gain

**Cost:** Low — `single Flask` via `gunicorn 23.0.0` single worker + optional single-upstream `nginx 1.24.0:19851` + `SQLite WAL` at `/tmp/spider-runtime/36013149664/app.db` (no `2x` `shared WAL`, no paid CDN). `N~1200` for `n_non304>=800` `~8-10min`, header-only and full-vector `B=1000` block perms `~1-2min` each, honest-cost `B=1000` `~1-2min`. Total `~15-20min` deterministic (previous HIT 330 and browser `N=20` pool moved to out-of-scope secondary). Code roots `research/harness`, `research/runtime`, `substrates`.

**Expected information gain:** Very high per Director `comparative_reasoning` and portfolio assessment (337 canonical exps, zero VALIDATED, sole SURVIVES synthetic): first joint isolation of `body/header` + `cost` + `wsgi/factory race` confounds at minimal cost, unblocking `Graph` delta-repair/freshness, `Product` residual-novelty honest economics, and `Frontier` live replication before any distributed `shared-WAL` `800`-stratified HIT retry. Valid positive or negative directly changes `Codex` ceiling from degenerate `single-host loopback [1.0,1.0]` to honest single-node `EXPERIMENTAL` or bounded falsified single-node. Comparative alternatives (broader permission/session drift, production SWR economics, immediate distributed correlated vs random null) rejected because they build on still-failing single-node invariants. Harness publish has cross-lane VOI dominating any complex distributed repeat.

## 17. Provenance to be logged

`run_experiment.py` `SHA`, `wsgi.py` `SHA` with `Path(__file__).parent` insertion, `freeze.json` hashes, `HS256` secret `len>=32` hash, `Flask 3.1.3` `PyJWT 2.14.0` `gunicorn 23.0.0` `nginx 1.24.0` `Werkzeug` `SQLite WAL` versions, per-observation `scheduling_seed`, `body_variant`, `trajectory_id`, `honest_cost`, `X-Worker-Pid`, `is_304`, `header_only_Jaccard`, `fingerprint_full/body/status`, `batch_state_log` SHA, `raw_freshness_observations.jsonl` (`~1200`), `provenance.json` fields. Recompute of `Jaccard/Pearson/CramersV/rho/full-vector bootstrap` must match `0` mismatches. Publish harness SHA for graph/product/frontier `substrates/` consumption. `nginx -t` output and health-gate attempt log required.

## 18. Disclosure

Single-node only. `TLS/HTTP2/QUIC` beyond `plain HTTP 127.0.0.1:19860/19851` not tested, `multi-host Redis` beyond single-host single `WAL` not tested, distributed `shared WAL` `2x gunicorn` and `sticky` affinity remain `UNKNOWN` not tested here, HIT `330/330` byte-preserving and `BrowserGym 0.14.3+Playwright 1.63.0` DOM `1280x720` beyond HTTP triple are secondary/ out-of-scope for primary gate (disclosed), body sizes beyond `31-117B` `sort_keys True` not tested, paid CDN `HIT` beyond `nginx` loopback is ceiling check only not gating if `C1-C4` pass. `If-None-Match/ETag->304` is real HTTP only via health-gated origin. Honest cost is `resolve+bind+verify+freshness+browser_steps` sum per `trajectory_id` block only. Header-only is `Jaccard MINUS {Content-Length,ETag,W-ETag,Content-Range}` preserving `Cache-Control/Set-Cookie/Vary` de-confounded. Scope limited to localhost Flask+SQLite WAL on `127.0.0.1` as authorized by lane registry `allowed_code_roots` `research/harness`, `research/runtime`, `substrates`.
