# EXP-RUNTIME-36004383518 preregistration — Minimal Single-Node Health-Gated Honesty Harness (Runtime CONTINUE, USE)

**Lane:** runtime — **Claim:** C-MEAS-VALID (measurement substrate is intervention-valid)  
**Director mandate:** CONTINUE, cognitive_reset=true, parent_handoff_disposition=USE, allocation claim C-MEAS-VALID (global-director-CONTINUE, cycle 35949179364, request 2baf2a0f42eeb1b4e94fc7f2)  
**Binding question (Director):** Does a minimal single-node health-gated harness (Flask 3.1.3 HS256 PyJWT >=32-char secret at /tmp/spider-runtime/*/app.db origin-checked, gunicorn 23.0.0 single worker + nginx 1.24.0:19851 health-gated 200 + X-Worker-Pid with retry, header-only Jaccard MINUS {Content-Length,ETag,W-ETag,Content-Range} preserving Cache-Control/Set-Cookie/Vary with de-confounded |r|<0.30, per-batch SELECT commitment verified, n_non304>=800 stratified, oracle-free greedy brotli->gzip MAX_DEPTH5 330/330 HIT/DYNAMIC byte-identical, BrowserGym 0.14.3+Playwright 1.63.0 1280x720 CDP Accessibility.getFullAXTree AX>10 PC-HEALTH>=80% DOM21-82 effective_distinct_n>1 non-degenerate CI ordering) achieve If-None-Match/ETag->304 discrimination TN>=0.85 FA<=0.10 with honest per-trajectory-reset sum-counter (resolve+bind+verify+freshness+browser_steps, no jitter/n*3200/f*6.0) and trajectory-grouped B=5000 |rho_shuffled|<0.20, and publish the harness for graph/product/frontier before re-attempting distributed 2x gunicorn+nginx shared-WAL 800-stratified X-Worker-Pid>=2 HS256 /tmp/spider-runtime-*/shared.db?

**Inheritance discipline:** Parent handoff `research/experiments/EXP-RUNTIME-35949568321/handoff.json` (MEASUREMENT_INVALID, sha ea6128f4726da5ada9c61e1b86b0540972e2667a0b14da5cddd12c2942f413a2) is continuity evidence with disposition USE per request. Its `next_question` (single-node honesty gate without distributed WAL, factory-pattern WSGI fix) is binding continuity state and is identical to Director question — not a drift. Four-way distinctions preserved below — established islands are reused as dependencies, not re-proved; rejected surrogates must not be re-introduced; UNKNOWN is tested here; do_not_assume are explicitly guarded. Director `agent_priors_used` are labeled priors, not SPIDER evidence, and are distinguished throughout. This experiment is the infrastructure-fixed retry of EXP-RUNTIME-35949568321 as recommended.

## 1. Hypothesis

**H1-SINGLE-NODE-HONESTY (C-MEAS-VALID):** A minimal single-node Flask 3.1.3 + PyJWT HS256 origin (secret >=32 bytes, PyJWT decode, `hs256_valid_success>=0.90`) with single SQLite WAL at `/tmp/spider-runtime/36004383518/app.db` (WAL, `check_same_thread=False`, `COMMIT` verified via `SELECT count(*) FROM sessions` per batch, `batch_state_log >=10` distinct timestamps, corrected wsgi import `sys.path` via `Path(__file__).parent` for `create_app()` + factory-pattern `def create_app()` ensuring directory `/tmp/spider-runtime/36004383518` exists BEFORE `init_db`, Flask verified listening on `127.0.0.1:19860` before nginx) plus **header-only Jaccard** structural (`filtered headers MINUS body-derived {Content-Length, ETag, W-ETag, Content-Range}` preserving `Cache-Control`/`Set-Cookie`/`Vary`) with **de-confounded scheduling** (`body_variant` random independent of drift, scheduling `|r|<0.30`, Cramers `V<0.30`) plus **gunicorn 23.0.0 single worker + nginx 1.24.0:19851 health-gated** (`GET /health` 200 + `X-Worker-Pid` 0 missing, retry 30s, warmup >=1 HIT) will achieve, in one run:

- (a) **Real ETag/If-None-Match ->304** with `n_non304>=800` stratified 400 per endpoint (`/api/profile` and `/api/data_list`, `Cache-Control` public/no-store variants, `ETag`-SHA256),
- (b) **Single-node discriminating freshness** `TN>=0.85` Wilson lower>0.75 and `FA<=0.10` (`ECE<=0.15` reported) on header-only Jaccard (single-node baseline; distributed replication not required for this gate),
- (c) **Header-only orthogonality** stratified `|r|<0.15` TOST delta0.15 `p_upper<0.05` CI upper<0.15, pooled `|r|<0.15`, 8/8 variance `FP<=0.15`,
- (d) **Honest per-trajectory-reset sum counters** `honest_cost = count_resolve+count_bind+count_verify+count_freshness+count_browser_steps` (once per real op, summed per `trajectory_id`, no jitter, no `n*3200`, no `f*6.0`) with `|rho_shuffled|<0.20` trajectory-grouped `B=5000`, `within-f std>0`, CI width>0,
- (e) **nginx 1.24.0 proxy_cache byte-preserving** `330/330` HIT/DYNAMIC byte-identical wire bytes and decompressed output via **oracle-free greedy `brotli->gzip` MAX_DEPTH5 no SHA oracle** `>=90%` HIT cells correct `0` ambiguous including stale branches,
- (f) **BrowserGym 0.14.3 + Playwright 1.63.0 1280x720 CDP `Accessibility.getFullAXTree` `AX>10` median `PC-HEALTH>=80%` `DOM21-82` per `/resource` `N=20` pool `effective_distinct_n>1`** delivering `B=1000` non-degenerate CIs for body `1B/2B/4B/39B/86B` and `CC vs ETag vs CLEN` ordering beyond degenerate `[1.0,1.0]`.

This isolates the three confounded failures that blocked 51 prior runtime experiments (body/header conflation, oracle tautology via `ground_truth_sha`, bijective cost via `n*3200/jitter/f*6.0`) plus the factory-pattern directory race that caused EXP-RUNTIME-35949568321 `0/15` health-gate failure, at low single-node cost before scaling to distributed `2x gunicorn + nginx round-robin shared WAL`. Success publishes the harness for graph/product/frontier consumption.

## 2. State representation

- **HTTP state:** `compute_fingerprint = SHA256(status || decompressed_body_bytes || sorted_filtered_headers_json)` where `filtered_headers_json` is `sorted(filtered_headers)` lowercased, `sort_keys=True`, separators `(',',':')`, `EXCLUDED = {Date, Server, X-Request-Id, CF-RAY, CF-Cache-Status, X-Cache, Age, X-Worker-Pid}`. Bodies are **auto-decompressed** before SHA for direct and Playwright `page.request.get` triple. HS256 secret len >=32 SHA logged.
- **Structural for orthogonality (C3):** **header-only Jaccard** on `headers_no_bodyderived_json` = `filtered_headers MINUS {Content-Length, ETag, W-ETag, Content-Range}`. Must preserve `Cache-Control`, `Set-Cookie`, `Vary`. Header Jaccard = `|A∩B|/|A∪B|` on header-name-value tokens. Verification via `grep`: `filter_headers` must exclude those four, must include `Cache-Control`. `hash(body)%10000` alone is forbidden (`BODY_HASH_STILL_PRESENT`). `X-Worker-Pid` logged per observation but excluded from Jaccard.
- **Behavioral:** `bc<=0.05` indicator for `valid` auth state; `TN = P(bc<=0.05|valid)` Wilson interval, `FA = P(bc<=0.05|invalid_or_expired)` must be <=0.10, `ECE<=0.15`.
- **Honest cost:** per-trajectory sum counter keyed by `trajectory_id`, not request id or batch.
- **HIT:** raw wire bytes `raw_body_sha256`, `Content-Encoding`, `X-Cache`/`CF-Cache-Status`, status, `X-Worker-Pid`.
- **Browser:** per-`/resource` CDP AX tree + `querySelectorAll` DOM count + HTTP triple, viewport `1280x720`, `effective_distinct_n` computed per state.

## 3. Action representation

- Auth/session drift dimension: `valid HS256` vs `expired` vs `invalid` vs `session-deleted` (real PyJWT verify via `jwt.decode` at origin, not raw Bearer lookup). Each paired sample is `(before drift, after drift)` with `body_variant` random independent.
- Header/body manipulations: `body_variant` ∈ {31B, 32B, 33B, 35B, 70B, 117B} plus `CC_small` vs `ETag` vs `CLEN` header variants for browser gradients; `Cache-Control` public `max-age=5` vs `no-store` strata.
- HIT populate vs test: unique URL (DYNAMIC, cache-bypass) vs fixed URL (HIT) through nginx `proxy_cache public max-age=300` at :19851, warmup 10 req.
- Honest-cost trajectories: `f ∈ {0,0.2,0.4,0.6,0.8,1.0}` novelty fraction, `trajectory_id` groups of ~10 observations.
- Factory action: directory creation `mkdir -p /tmp/spider-runtime/36004383518` before `init_db`, `gunicorn --workers 1 --bind 127.0.0.1:19860 'run_experiment:create_app()'` factory pattern.

## 4. Target

- **Primary:** Single-node freshness discrimination `TN = P(bc<=0.05 | valid, header-only)` and `FA`, plus header-only orthogonality `r(header_only_Jaccard, behavioral_indicator)` with TOST equivalence.
- **Secondary (gating honest-cost):** `rho(honest_cost_per_trajectory, novelty_fraction f)` and `|rho_shuffled|` under trajectory-grouped permutation `B=5000`.
- **Secondary (HIT):** `fraction HIT decompressed == ground_truth` under oracle-free greedy `MAX_DEPTH5` and `fraction DYNAMIC vs HIT byte-identical` raw wire bytes.
- **Secondary (browser):** `full-vector discrimination` via triple (status+body+headers_no_bodyderived) vs single-field baselines at `N=20` per state, plus per-magnitude gradient `B=1000` CI width and ordering.

## 5. Sampling policy

- **Freshness/304:** `N~1200` paired samples targeting `n_non304>=800` after real `If-None-Match/ETag->304` filtering, stratified `400` per endpoint (`/api/profile` 400, `/api/data_list` 400) with `Cache-Control` public `max-age=5` vs `no-store` sub-strata, `ETag` as SHA256 of body. `SEED=44`, jitter `50-150ms` **between bursts only, not inside honest_cost**. `body_variant` assignment `U{all variants}` independent of drift. Real HTTP via localhost direct `:19860` (or nginx single-upstream passthrough when HIT matrix overlapped for efficiency). `X-Worker-Pid` logged per observation (single worker). Per-batch `SELECT count(*) FROM sessions` logged.
- **HIT:** `48` cells (3 payloads ×2 orders ×2 chunk sizes ×4 Accept-Encoding) ×5 reps = `~330` lines (including `DYNAMIC`+`HIT`+stale). Two-phase per cell: Phase 1 populate (unique URL), Phase 2 test (fixed URL). Ground truth = SHA256 of iterative known-order decode of origin-served payload. Stale HIT/SWR/SIE/304 via Cache-Control stale directives when applicable.
- **Honest cost:** Cost trajectories with `f` levels, `trajectory_id` groups of `~10` observations each, honest sum counter incremented once per real `resolve/bind/verify/freshness/browser_steps` call, summed per `trajectory_id`.
- **Browser:** `N=20` per state (`A`, `A_alt`, `B`, `C`, `E`) with `50%` pool `A_alt 32B` vs `A 31B` and `50%` header jitter per observation → `effective_distinct_n>1`. `concurrency=4`, `B=1000` bootstrap per comparison, viewport `1280x720`, CDP `getFullAXTree` per `/resource`.

## 6. Unit of analysis

- Freshness/orthogonality: **paired sample** (`pre, post, is_304, header_only_Jaccard, bc, drift_label, endpoint, body_variant, trajectory_id, honest_cost, X-Worker-Pid`).
- HIT: **cell observation** (`raw_body_sha256, Content-Encoding, X-Cache, decompressed_sha, path, ambiguous_flag, X-Worker-Pid, is_hit`).
- Honest-cost: **trajectory** (aggregated sum per `trajectory_id`).
- Browser: **resource page** (`/resource` triple at `N=20` pool, `AX_nodes, DOM_count, effective_distinct_n`).

## 7. Holdout / stratification

- No ML holdout beyond TOST/CI construction, but **endpoint stratification is frozen:** `n_non304>=800` must include `>=400` per endpoint (`/api/profile`, `/api/data_list`). Reported metrics must include both stratified and pooled values. Fisher-z CI for `r` with `n_non304` denominator. Missing stratified target triggers `INSUFFICIENT_STRATIFICATION` validity flag, not `SUPPORTS`. `batch_state_log >=10` distinct `count(*) FROM sessions` timestamps required.

## 8. Nulls / baselines

| ID | Description | Expected behaviour |
|---|---|---|
| **B-HEADER-ONLY-JACCARD** | Header-only Jaccard MINUS body-derived preserving CC/Set-Cookie/Vary (primary intervention) | `TN>=0.85` `Wilson lo>0.75` `FA<=0.10`, `|r|<0.15` TOST pass |
| **B-BODY-HASH-REJECTED** | Rejected surrogate `hash(body)%10000` / `hash(headers)%10000` / including CLEN/ETag | `r≈0.72` (all), `≈0.30` status-free → **REJECTED** (proves conflation) |
| **B-ORACLE-GUIDED-REGRESSION** | Oracle-guided with `ground_truth_sha` inside loop (regression) | `240/240` — not evidence for oracle-free claim |
| **B-ORACLE-FREE-GREEDY** | Oracle-free greedy `brotli->gzip` MAX_DEPTH5 no SHA | `>=90%` HIT correct, `0` ambiguous |
| **B-HIT-NGINX-BYTE-PRESERVING** | Local nginx `1.24.0` `proxy_cache` `330/330` HIT/DYNAMIC identity single-upstream | `330/330` identical, stale branches identical |
| **B-COST-SHUFFLED** | Trajectory-grouped `B=5000` permutation of `f` labels for honest cost | `|rho_shuffled|<0.20` `within-f std>0` |
| **B-STATUS-ONLY** | `hash(status)` only | `0.0` on `200 vs 200` body/header variants |
| **B-BODY-ONLY** | `hash(decompressed body)` only | `1.0` on body-varying `AvsC`, `0.0` on body-identical header-only |
| **B-HEADERS-NO-BODYDERIVED** | `headers MINUS CLEN/ETag/W-ETag/Content-Range` | `0.0` body-only, `1.0` header-only independent |

Null controls: `NC-ORTHOGONALITY-NOISE` (noise-only structural jitter expecting `FP<=0.15`), `NC-COST-SHUFFLED` (`|rho_shuffled|<0.20` must hold even when `f` shuffled), `NC-HIT-NO-CACHE` (no-cache identity null), `NC-BROWSER-SAME-STATE` (`0.0` discrimination when same body resampled), `NC-FACTORY-REGRESSION` (module-level `app=create_app()` before wipe must reproduce prior failure).

## 9. Primary metric & expected direction

- **C1 (gate):** `mean_TN = mean_endpoint TN` and `Wilson lower 95% >0.75` and `FA<=0.10` (and `ECE<=0.15` reported) header-only single-node. **Pass if `TN>=0.85` / `Wilson lo>0.75` / `FA<=0.10`.**
- **C2:** `n_non304>=800` stratified `400` per endpoint (real `304` filtering, `hs256_valid_success>=0.90`).
- **C3/C4:** `TOST delta=0.15` for `r = Pearson(header_only_Jaccard, behavioral_indicator)`: **Pass if** `CI upper<0.15` **and** `p_upper<0.05` **and** `CI lower>-0.15` **and** pooled `|r|<0.15` **and** `8/8` variance `FP<=0.15` header-only de-confounded.
- **C5:** `|rho_shuffled|<0.20` trajectory-grouped `B=5000`, `within-f std>0`, `CI width>0` `effective>1` on honest sum counters.
- **C6:** HIT `330/330` byte-identical and `oracle-free >=90%` HIT correct `0` ambiguous including stale branches.
- **C7/C8:** Browser `PC-HEALTH>=80%` `DOM21-82` `AX>10` `N=20` pool `effective_distinct_n>1`, discrimination `full>0.5` with correct baselines `0.0`, gradients `B=1000` width>0 for `>=2` magnitudes → ordering claim.

Expected: **Pass** for `C1-C6` if header-only + honest sum + oracle-free + factory fix are correct; **Fail** if any confound persists. `B-BODY-HASH-REJECTED` expected to **fail** even with same data (validates filter necessity). `TRAJECTORY-GROUPED` expected to correctly remove bijective artifact.

## 10. Uncertainty method

- `TN` Wilson `95%` lower bound per endpoint + mean; `FA` Wilson interval; `ECE` computed.
- `r` Fisher-z transformed CI `95%` with `n_non304` denominator; TOST `p_upper = 1 - Phi((fisher_r - fisher_delta)/se)` (correct tail, not `Phi` alone — prior error `~1.0` vs `4.5e-08`); Cramers V also.
- `rho_shuffled`: trajectory-grouped permutation `B=5000` (group=`trajectory_id`), within-f `std` and CI width reported; `effective>1` required.
- Browser `full vs null`: `B=1000` bootstrap per comparison `N=20`, `effective_distinct_n` and CI width reported; degenerate `[1.0,1.0]` with `effective=1` is **not** precision (prior degeneracy prior per Director).
- Per-batch `SELECT` timestamps for commitment verification; health-gate attempts logged.

## 11. Adequacy rule

- `n_non304>=800` with `>=400` per endpoint after filtering `is_304==false` and `hs256_valid_success>=0.90`.
- `batch_state_log >=10` distinct `count(*) FROM sessions` timestamps with `COMMIT` verified.
- `health-gate` `0` missing `GET /health` via origin 200 + `X-Worker-Pid` (retry 30s, Flask verified listening before nginx).
- Browser `N=20` per state with `effective_distinct_n>1` via pool, `AX>10` median `PC-HEALTH>=80%` `DOM21-82`.
- If adequacy fails → `MEASUREMENT_INVALID` (not `SUPPORTS`/`FALSIFIED`). Production CDN `0` HIT is **ceiling** not gating if nginx `C6` passes.

## 12. Falsification / survival rule

**SUPPORTS (single-node honesty gate restored, harness publishable)** requires **ALL** mandatory with validity passing including factory fix:

- `C1` `mean TN>=0.85` `Wilson lo>0.75` `FA<=0.10` header-only (single-node).
- `C2` `n_non304>=800` stratified `400` per endpoint `0` missing `hs_rate>=0.90`.
- `C3/C4` `TOST p_upper<0.05` `CI upper<0.15` `pooled|r|<0.15` `8/8` variance `FP<=0.15` header-only de-confounded `|r|<0.30` `V<0.30`.
- `C5` `|rho_shuffled|<0.20` trajectory-grouped `B=5000` `within-f std>0` `width>0` `effective>1`.
- `C6` `330/330` HIT/DYNAMIC byte-identical + `oracle-free >=90%` `0` ambiguous + stale branches identical.
- `C7` browser provision `AX>10` `PC-HEALTH>=80%` `DOM21-82` `N=20` pool `effective>1`.
- `C8` browser discrimination + gradient `B=1000` width>0 for `>=2` magnitudes (ordering beyond degenerate).

**Degraded SUPPORTS_SINGLE_NODE_NO_BROWSER:** `C1-C6` pass but `C7/C8` provision fails because `Playwright/BrowserGym` not installed despite health-gate and `effective>1` logic satisfied — counts as honesty-gate pass without browser, publishes harness, authorizes distributed. Full `SUPPORTS` requires browser.

**FALSIFIED-IN-SETTING:** Any `C1-C6` fails while validity passes (factory fixed, health-gated, header-only MINUS correct, honest sum correctly grouped, oracle-free correctly implemented) → bounded falsification on `Flask 3.1.3 + PyJWT HS256 + gunicorn 23.0.0 + nginx 1.24.0 + 1280x720` localhost. `B-BODY-HASH-REJECTED` failure does **not** count as falsification of header-only — it is expected and confirms necessity of filter.

**MEASUREMENT_INVALID** if any validity gate fails: `hash(body)%10000` alone, `CLEN/ETag` not excluded, status prefix, synthetic `np.random` bodies without HTTP, `jitter`/`n*3200`/`f*6.0` in cost, `SHA oracle` inside greedy loop, `health-gate` missing or Flask not verified listening or directory not before DB or `direct relabeled as browser`, `SELECT commitment` not verified, recompute mismatch, `X-Worker-Pid` not logged. Production CDN `0` HIT is **ceiling** not gating if nginx `C6` passes. Distributed `shared-WAL`/`sticky` remain `UNKNOWN` — not implied by single-node result.

Per contract, `status` describes measurement validity; valid negative is `status=COMPLETE` `outcome=FALSIFIES`, not infrastructure failure.

## 13. Validity threats & mitigations

| Threat | Mitigation | Audited check |
|---|---|---|
| **Body/header conflation** (`CLEN/ETag` body-derived in structural) | `MINUS` set enforced via `grep`; `B-BODY-HASH-REJECTED` proves failure when included | `grep filter_headers` + recompute Jaccard |
| **Factory/directory race** (`app=create_app()` before wipe deletes DB, no listening verify) | `def create_app()` factory, `mkdir -p` before `init_db`, `gunicorn 'run_experiment:create_app()'`, socket verify `127.0.0.1:19860` retry 30s before nginx | `grep` no module-level init + socket log |
| **Oracle tautology** (`ground_truth_sha` inside greedy loop → `240/240`) | `grep` no `ground_truth_sha` in loop; `MAX_DEPTH5` fixed; ambiguous flag logged | `grep` + path audit |
| **Bijective honest-cost** (`n*3200`, `f*6.0`, `random.gauss` jitter) | Frozen sum `resolve+bind+verify+freshness+browser_steps` per `trajectory_id`, trajectory-grouped `B=5000`, `grep` bans | `grep` + `|rho_shuffled|<0.20` |
| **Scheduling confound** (`body_variant` correlated with drift) | Random independent assignment + recomputed `Pearson`/`CramersV <0.30` | `r`/`V` recompute |
| **TOST wrong tail** (`Phi` vs `1-Phi` → `p~1.0` vs `4.5e-08`) | Fisher-z correct `p_upper = 1-Phi((z_delta - z_r)/se)` | Audit recompute |
| **nginx HIT absent** (free-tier `0` HIT) | Local `nginx 1.24.0` `proxy_cache` single-upstream with warmup `>=1` HIT required; `330/330` identity checked | `X-Cache` log |
| **Health-gate race** (Flask not listening before nginx 19851) | Verify Flask listening via socket/curl loop before nginx start, retry GET /health `200+X-Worker-Pid` 15×1s | Health log |
| **Degenerate browser CI** (`[1.0,1.0]` with `effective=1` claimed as precision) | `N=20` pool `A vs A_alt 50%` + `effective_distinct_n>1` + `B=1000` width>0 mandatory | `effective_distinct_n` audit |
| **Single-node vs distributed confusion** | Explicit scope: single-node only, distributed shared-WAL `UNKNOWN` | `provenance` path notes `/36004383518/app.db` single file |

## 14. Consequences

- **If SUPPORTS (or SUPPORTS_SINGLE_NODE_NO_BROWSER):** Minimal honesty gate closes and harness publishes. Single-node `TN>=0.85` + `FA<=0.10` + `|r|<0.15` + `|rho_shuffled|<0.20` + `330/330` + `oracle-free >=90%` + browser `AX>10` `DOM21-82` `B=1000` non-degenerate CIs validates the audited harness cross-lane needs. Claim ceiling expands from `local nginx island EXPERIMENTAL` (`EXP-RUNTIME-35551516706 330/330`) to `single-node honest substrate EXPERIMENTAL` (real HTTP `127.0.0.1:19860/19851`, `31-117B`, single viewport, health-gated factory-fixed) — does **not** promote `C-MEAS-VALID` to `VALIDATED`/`PRODUCT_CORE` (still bounded single-host). Publishes `research/experiments/EXP-RUNTIME-36004383518/` harness and `substrates/` for graph/product/frontier reuse. Authorizes next experiment: distributed `HS256` shared-WAL `800`-stratified HIT (`2x gunicorn 19860+19861` via `nginx 19851` round-robin `$request_uri` + shared `shared.db`) and honest residual-novelty economics vs `RAG`/`Stagehand` Pareto.
- **If FALSIFIED-IN-SETTING (valid):** Honesty fix insufficient even at single-node with factory fix. Bounds `C-MEAS-VALID` to loopback `EXPERIMENTAL` without honesty, prevents false `VALIDATED` promotion, forces true header canonicalization / counter grouping / nginx config redesign before distributed. Distributed hypotheses remain `UNKNOWN`.
- **If MEASUREMENT_INVALID:** Synthetic or validity breach — no ceiling change, requires fixed rerun per recommended_action. Distributed hypotheses stay `UNKNOWN`.

## 15. Parent handoff continuity (USE, not repeat, cognitive_reset true)

- **Established (reused, not re-proved, from handoff + Codex):** `local nginx 1.24.0 proxy_cache byte-preserving HIT 330/330` (`EXP-RUNTIME-35551516706` `240/240` `330/330` `0` ambiguous audit PASS) as dependency; `C-FRESHNESS` orthogonality at `delta0.15` confirmed only on localhost mock `n=480` (`EXP-GRAPH-35389145821` `r=0.0022` `CI upper 0.0916` `TOST p0.0006` audit PASS) — not superseded by this MEASUREMENT_INVALID; `code readiness` declared (HS256 len 49 >=32, `filter_headers` excludes CLEN/ETag, jitter between bursts only) but blocked by health gate and requires re-verification after factory fix; prior distributed correlation at `EXP-GRAPH-35611618323 r=-0.0381 TOST p2e-08 n844` but per-node C1 mean TN 0.6667 remains bounded ceiling for distributed shared-store.
- **Rejected (must not reuse, per handoff):** `per-node isolated SQLite` achieving `TN>=0.85` (`mean 0.6666 session 0.0`) — shared replication required for distributed; `hash(body)%10000` as header-only surrogate (`r=0.721` `p=1.0` status-free 0.305) — do not extend to frozen header-only Jaccard; `honest-cost n*3200/jitter/f*6.0` bijective artifact — synthetic stubs not executed do not rehabilitate honesty; fixed-order iterative decompression `180/240` failures and sticky `skew>0.90` with 3 URIs `ceiling 0.666` — require `>=10` URIs hash.
- **Unknown (tested here at single-node with factory fix):** Whether health-gated single Flask HS256>=32 with directory exists before `/tmp/spider-runtime/36004383518/app.db` creation and Flask bound verified before nginx health gate achieves `C1` mean `TN>=0.85` Wilson lo>0.75 and `C2` `n_non304>=800` stratified 400/endpoint per-batch SELECT >=10 distinct ts; whether header-only Jaccard `MINUS {CLEN,ETag,W-ETag,Content-Range}` with `|r|<0.30` achieves orthogonality stratified `|r|<0.15` TOST; whether honest sum counters `|rho_shuffled|<0.20`; whether nginx HIT `330/330` oracle-free `>=90%` 0 ambiguous; whether BrowserGym pool delivers non-degenerate CIs ordering beyond `[1.0,1.0]`; whether single-node generalizes beyond `127.0.0.1` plain HTTP (TLS/HTTP2/QUIC, multi-host Redis, production CDN — out of scope); whether distributed shared-WAL `2x gunicorn` via nginx achieves distributed C1 — remains UNKNOWN pending this gate.
- **Do-not-assume (guarded):** Do not assume `0.0` metrics from prior `0/15` health-gate are falsification (null not falsification per EXPERIMENT_PACKET.md s1); do not assume degenerate `CIs [1.0,1.0]` with `effective=1` is precision; do not assume prior `TN 0.976 / r 0.721 / rho 0.132` from prior `MEASUREMENT_INVALID` prove frozen hypotheses (conflated surrogates); do not assume `C-MEAS-VALID`/`C-FRESHNESS` are `VALIDATED`/`PRODUCT_CORE` (audit `MEASUREMENT_INVALID`, ceiling `EXPERIMENTAL`); do not assume paid CDN `0` HIT falsifies byte-preserving; do not treat Director labeled priors (path dependence, compounding salience, thresholded fingerprint, parameterization orthogonality, tool bypass, degeneracy `1.0 [1.0,1.0]`) as SPIDER-established evidence — they are priors requiring hardenings; do not infer beyond localhost mock without `n_non304>=800` and correct TOST.
- **Director priors distinguished:** `agent_priors_used` (path-dependent salience pollution, thresholded fingerprint caching ECE<=0.15, parameterization Jaccard<0.30 orthogonal families, O(1) tool/API bypass, measurement degeneracy heterogeneous |S|>=16) are explicitly labeled priors used to require `trajectory-grouped permutation`, `header-only MINUS`, `ECE` reporting, `family-specific slots`, and `non-degenerate CI` guards — not SPIDER evidence. This design tests them falsifiably.

## 16. Estimated cost & information gain

**Cost:** Low — `single Flask` via `gunicorn 23.0.0` single worker + optional single-upstream `nginx 1.24.0:19851` + `SQLite WAL` at `/tmp/spider-runtime/36004383518/app.db` (no `2x` `shared WAL`, no paid CDN). `N~1200` for `n_non304>=800` `~8-10min`, HIT `48×5` `~6-8min`, honest-cost `B=5000` `~1-2min`, browser `BrowserGym 0.14.3` + `Playwright npx chromium` `~3-5min` + `N=20` pool `~10-12min`. Total `~30-40min` deterministic. Code roots `research/harness`, `research/runtime`, `substrates`.

**Expected information gain:** Very high per Director `comparative_reasoning` and portfolio assessment (319 canonical exps, zero VALIDATED, sole SURVIVES synthetic `C-FRESHNESS EXP-GRAPH-35947468747`): first joint isolation of `body/header` + `oracle` + `cost` + `factory race` confounds at minimal cost, unblocking `Graph` delta-repair/freshness, `Product` residual-novelty honest economics, and `Frontier` live replication before any distributed `shared-WAL` `800`-stratified HIT retry. Valid positive or negative directly changes `Codex` ceiling from degenerate `single-host loopback [1.0,1.0]` (heterogeneous `|S|>=16` required) to honest single-node `EXPERIMENTAL` or bounded falsified single-node. Comparative alternative (immediate distributed `n>=800` URL-sticky `$request_uri` hash) rejected because it builds on still-failing single-node invariants (`X-Worker-Pid` unverified, header Jaccard includes CLEN/ETag, degenerate CI). Harness publish has cross-lane VOI dominating any complex distributed repeat. Addresses Scout honest sum-counter `|rho_shuffled|<0.20` and `B=5000` guards.

## 17. Provenance to be logged

`run_experiment.py` `SHA`, `freeze.json` hashes, `HS256` secret `len>=32` hash (`57a0f183` prior len 49), `Flask 3.1.3` `PyJWT 2.14.0` `gunicorn 23.0.0` `nginx 1.24.0` `Werkzeug` `SQLite WAL` `BrowserGym 0.14.3` `AgentLab 0.4.2` `Playwright 1.63.0` `CDP` versions, per-observation `scheduling_seed`, `body_variant`, `trajectory_id`, `honest_cost`, `X-Worker-Pid`, `is_304`, `header_only_Jaccard`, `is_hit`, `raw_body_sha256`, `Content-Encoding`, `batch_state_log` SHA, `raw_freshness_observations.jsonl` (`~1200`), `raw_hit_observations.jsonl` (`~330`), `raw_browser_observations.jsonl` (`~520`), `provenance.json` fields. Recompute of `Jaccard/Pearson/TOST/rho/greedy` must match `0` mismatches. Publish harness SHA for graph/product/frontier `substrates/` consumption.

## 18. Disclosure

Single-node only. `TLS/HTTP2/QUIC` beyond `plain HTTP 127.0.0.1:19860/19851` not tested, `multi-host Redis` beyond single-host single `WAL` not tested, distributed `shared WAL` `2x gunicorn` and `sticky` affinity remain `UNKNOWN` not tested here, `BrowserGym` DOM beyond HTTP triple not tested, body sizes beyond `31-117B` `sort_keys True` not tested, paid CDN `HIT` beyond `nginx` loopback is ceiling check only not gating if `C6` passes. `If-None-Match/ETag->304` is real HTTP only via health-gated origin. Honest cost is `resolve+bind+verify+freshness+browser_steps` sum per `trajectory_id` only. Header-only is `Jaccard MINUS {Content-Length,ETag,W-ETag,Content-Range}` preserving `Cache-Control/Set-Cookie/Vary` de-confounded. Scope limited to localhost Flask+SQLite WAL on `127.0.0.1` as authorized by lane registry `allowed_code_roots` `research/harness`, `research/runtime`, `substrates`.

