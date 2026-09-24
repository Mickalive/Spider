# EXP-RUNTIME-35937588416 preregistration — Minimal Single-Node Honesty Gate (Runtime PIVOT, SUPERSEDE)

**Lane:** runtime — **Claim:** C-MEAS-VALID (measurement substrate is intervention-valid)  
**Director mandate:** PIVOT, cognitive_reset=true, parent_handoff_disposition=SUPERSEDE (global-director-PIVOT, cycle 35937189245)  
**Binding question (Director):** Can the minimal single-node honesty gate be restored without distributed WAL: single Flask HS256 origin with header-only Jaccard minus {Content-Length,ETag,W-ETag,Content-Range} preserving Cache-Control/Set-Cookie/Vary, delivering real If-None-Match/ETag->304 (n_non304>=800 stratified 400/endpoint, per-batch SELECT commitment verified, X-Worker-Pid>=10 per worker) and oracle-free greedy brotli->gzip MAX_DEPTH5 byte-identical 330/330 HIT/DYNAMIC on nginx 1.24.0 byte-preserving proxy, plus honest per-trajectory-reset sum counters (resolve+bind+verify+freshness+browser_steps, no jitter, no n*3200, no f*6.0, |rho_shuffled|<0.20 within-f std>0 trajectory-grouped B=5000) and BrowserGym 0.14.3 + Playwright 1.63.0 1280x720 CDP Accessibility.getFullAXTree AX>10 PC-HEALTH>=80% DOM21-82 effective_distinct_n>1 delivering non-degenerate per-value Cache-Control/ETag/Content-Length gradients (B=1000 CIs) ordering sensitivity beyond degenerate [1.0,1.0]?

**Inheritance discipline:** Parent handoff `research/experiments/EXP-RUNTIME-35913894863/handoff.json` (MEASUREMENT_INVALID, sha 4563235a...) is continuity evidence only per AGENTS.md. Its `next_question` (health-gated shared WAL HS256>=32 URL-sticky 2x gunicorn via nginx 19851 with 48-cell HIT) is **advisory, not binding** under SUPERSEDE. This experiment **supersedes** that distributed proposal and tests the smaller single-node gate Director identifies as highest-VOI. Four-way distinctions preserved below — established islands are reused as dependencies, not re-proved; rejected surrogates must not be re-introduced.

## 1. Hypothesis

**H1-SINGLE-NODE-HONESTY (C-MEAS-VALID):** A minimal single-node Flask 3.1.3 + PyJWT HS256 origin (secret >=32 bytes, PyJWT decode, hs256_valid_success>=0.90) with single SQLite WAL at `/tmp/spider-runtime/35937588416/app.db` (WAL, `check_same_thread=False`, COMMIT verified via `SELECT count(*) FROM sessions` per batch, `batch_state_log >=10` distinct timestamps) plus **header-only Jaccard** structural (`filtered headers MINUS body-derived {Content-Length, ETag, W-ETag, Content-Range}` preserving Cache-Control/Set-Cookie/Vary) with **de-confounded scheduling** (`body_variant` random independent of drift, scheduling r<0.30, Cramers V<0.30) will achieve, in one run:

- (a) **Real ETag/If-None-Match ->304** with `n_non304>=800` stratified 400 per endpoint (`/api/profile` and `/api/data_list`, `Cache-Control` public/no-store variants, `ETag`-SHA256),
- (b) **Single-node discriminating freshness** `TN>=0.85` Wilson lower>0.75 (single-node baseline; distributed replication not required for this gate),
- (c) **Header-only orthogonality** stratified `|r|<0.15` TOST delta0.15 `p_upper<0.05` CI upper<0.15, pooled `|r|<0.15`, 8/8 variance `FP<=0.15`,
- (d) **Honest per-trajectory-reset sum counters** `honest_cost = count_resolve+count_bind+count_verify+count_freshness+count_browser_steps` (once per real op, summed per `trajectory_id`, no jitter, no `n*3200`, no `f*6.0`) with `|rho_shuffled|<0.20` trajectory-grouped `B=5000`, `within-f std>0`, CI width>0,
- (e) **nginx 1.24.0 proxy_cache byte-preserving** `330/330` HIT/DYNAMIC byte-identical wire bytes and decompressed output via **oracle-free greedy `brotli->gzip` MAX_DEPTH5 no SHA oracle** `>=90%` HIT cells correct `0` ambiguous,
- (f) **BrowserGym 0.14.3 + Playwright 1.63.0 1280x720 CDP `Accessibility.getFullAXTree` `AX>10` median `PC-HEALTH>=80%` `DOM21-82` per `/resource` `N=20` pool `effective_distinct_n>1`** delivering `B=1000` non-degenerate CIs for body `1B/2B/4B/39B/86B` and `CC_small vs ETag vs CLEN` ordering beyond degenerate `[1.0,1.0]`.

This isolates the three confounded failures that blocked 50 prior runtime experiments (body/header conflation, oracle tautology via `ground_truth_sha`, bijective cost via `n*3200/jitter/f*6.0`) at low cost before scaling to distributed `2x gunicorn + nginx round-robin shared WAL`.

## 2. State representation

- **HTTP state:** `compute_fingerprint = SHA256(status || decompressed_body_bytes || sorted_filtered_headers_json)` where `filtered_headers_json` is `sorted(filtered_headers)` lowercased, `sort_keys=True`, separators `(',',':')`, `EXCLUDED = {Date, Server, X-Request-Id, CF-RAY, CF-Cache-Status, X-Cache, Age, X-Worker-Pid}`. Bodies are **auto-decompressed** before SHA for direct and Playwright `page.request.get` triple.
- **Structural for orthogonality (C3):** **header-only Jaccard** on `headers_no_bodyderived_json` = `filtered_headers MINUS {Content-Length, ETag, W-ETag, Content-Range}`. Must preserve `Cache-Control`, `Set-Cookie`, `Vary`. Header Jaccard = `|A∩B|/|A∪B|` on header-name-value tokens. Verification via `grep`: `filter_headers` must exclude those four, must include `Cache-Control`. `hash(body)%10000` alone is forbidden (`BODY_HASH_STILL_PRESENT`).
- **Behavioral:** `bc<=0.05` indicator for `valid` auth state; `TN = P(bc<=0.05|valid)`.
- **Honest cost:** per-trajectory sum counter keyed by `trajectory_id`, not request id.
- **HIT:** raw wire bytes `raw_body_sha256`, `Content-Encoding`, `X-Cache`/`CF-Cache-Status`, status.
- **Browser:** per-`/resource` CDP AX tree + `querySelectorAll` DOM count + HTTP triple, viewport `1280x720`.

## 3. Action representation

- Auth/session drift dimension: `valid HS256` vs `expired` vs `invalid` vs `session-deleted` (real PyJWT verify). Each paired sample is `(before drift, after drift)` with `body_variant` random.
- Header/body manipulations: `body_variant` ∈ {31B, 32B, 33B, 35B, 70B, 117B} plus `CC_small` vs `ETag` vs `CLEN` header variants for browser gradients.
- HIT populate vs test: unique URL (DYNAMIC) vs fixed URL (HIT) through nginx `proxy_cache public max-age=300`.

## 4. Target

- **Primary:** Single-node freshness discrimination `TN = P(bc<=0.05 | valid, header-only)` and header-only orthogonality `r(header_only_Jaccard, behavioral_indicator)` with TOST equivalence.
- **Secondary (gating honest-cost):** `rho(honest_cost_per_trajectory, novelty_fraction f)` and `|rho_shuffled|` under trajectory-grouped permutation.
- **Secondary (HIT):** `fraction HIT decompressed == ground_truth` under oracle-free greedy and `fraction DYNAMIC vs HIT byte-identical`.
- **Secondary (browser):** `full-vector discrimination` via triple (status+body+headers_no_bodyderived) vs single-field baselines at `N=20` per state, plus per-magnitude gradient `B=1000` CI width.

## 5. Sampling policy

- **Freshness/304:** `N~1200` paired samples targeting `n_non304>=800` after real `If-None-Match/ETag->304` filtering, stratified `400` per endpoint (`/api/profile` 400, `/api/data_list` 400) with `Cache-Control` public `max-age=5` vs `no-store` sub-strata, `ETag` as SHA256 of body. `SEED=44`, jitter `50-150ms` **between bursts only, not inside honest_cost**. `body_variant` assignment `U{all variants}` independent of drift. Real HTTP via localhost direct (or nginx single-upstream passthrough when HIT matrix overlapped). `X-Worker-Pid` logged per observation (single worker or small pool).
- **HIT:** `48` cells (3 payloads ×2 orders ×2 chunk sizes ×4 Accept-Encoding) ×5 reps = `~330` lines (including `DYNAMIC`+`HIT`+stale). Two-phase per cell: Phase 1 populate (unique URL), Phase 2 test (fixed URL). Ground truth = SHA256 of iterative known-order decode of origin-served payload.
- **Honest cost:** Cost trajectories with `f ∈ {0,0.2,0.4,0.6,0.8,1.0}` (novelty fraction), `trajectory_id` groups of `~10` observations each, honest sum counter incremented once per real `resolve/bind/verify/freshness/browser_steps` call.
- **Browser:** `N=20` per state (`A`, `A_alt`, `B`, `C`, `E`) with `50%` pool `A_alt 32B` vs `A 31B` and `50%` header jitter per observation → `effective_distinct_n>1`. `concurrency=4`, `B=1000` bootstrap per comparison.

## 6. Unit of analysis

- Freshness/orthogonality: **paired sample** (`pre, post, is_304, header_only_Jaccard, bc, drift_label, endpoint, body_variant, trajectory_id, honest_cost`).
- HIT: **cell observation** (`raw_body_sha256, Content-Encoding, X-Cache, decompressed_sha, path, ambiguous_flag`).
- Honest-cost: **trajectory** (aggregated sum per `trajectory_id`).
- Browser: **resource page** (`/resource` triple at `N=20` pool).

## 7. Holdout / stratification

- No ML holdout beyond TOST/CI construction, but **endpoint stratification** is frozen: `n_non304>=800` must include `>=400` per endpoint (`/api/profile`, `/api/data_list`). Reported metrics must include both stratified and pooled values. Fisher-z CI for `r` with `n_non304` denominator. Missing stratified target triggers `INSUFFICIENT_STRATIFICATION` validity flag, not `SUPPORTS`.

## 8. Nulls / baselines

| ID | Description | Expected behaviour |
|---|---|---|
| **B-HEADER-ONLY-JACCARD** | Header-only Jaccard MINUS body-derived preserving CC/Set-Cookie/Vary (primary intervention) | `TN>=0.85`, `|r|<0.15` TOST pass |
| **B-BODY-HASH-REJECTED** | Rejected surrogate `hash(body)%10000` / `hash(headers)%10000` / including CLEN/ETag | `r≈0.72` (all), `≈0.30` status-free → **REJECTED** (proves conflation) |
| **B-ORACLE-GUIDED-REGRESSION** | Oracle-guided with `ground_truth_sha` inside loop (regression) | `240/240` — not evidence for oracle-free claim |
| **B-ORACLE-FREE-GREEDY** | Oracle-free greedy `brotli->gzip` MAX_DEPTH5 no SHA | `>=90%` HIT correct, `0` ambiguous |
| **B-HIT-NGINX-BYTE-PRESERVING** | Local nginx `1.24.0` `proxy_cache` `330/330` HIT/DYNAMIC identity | `330/330` identical, stale branches identical |
| **B-COST-SHUFFLED** | Trajectory-grouped `B=5000` permutation of `f` labels for honest cost | `|rho_shuffled|<0.20` `within-f std>0` |
| **B-STATUS-ONLY** | `hash(status)` only | `0.0` on `200 vs 200` body/header variants |
| **B-BODY-ONLY** | `hash(decompressed body)` only | `1.0` on body-varying `AvsC`, `0.0` on body-identical header-only |
| **B-HEADERS-NO-BODYDERIVED** | `headers MINUS CLEN/ETag/W-ETag/Content-Range` | `0.0` body-only, `1.0` header-only independent |

Null controls: `NC-ORTHOGONALITY-NOISE` (noise-only structural jitter expecting `FP<=0.15`), `NC-COST-SHUFFLED` (`|rho_shuffled|<0.20` must hold even when `f` shuffled), `NC-HIT-NO-CACHE` (no-cache identity null), `NC-BROWSER-SAME-STATE` (`0.0` discrimination when same body resampled).

## 9. Primary metric & expected direction

- **C1 (gate):** `mean_TN = mean_endpoint TN` and `Wilson lower 95% >0.75` and `session_status>=0.85` (single-node header-only). **Pass if `>=0.85` / `>0.75`.**
- **C2:** `n_non304>=800` stratified `400` per endpoint (real `304` filtering).
- **C3/C4:** `TOST delta=0.15` for `r = Pearson(header_only_Jaccard, behavioral_indicator)`: **Pass if** `CI upper<0.15` **and** `p_upper<0.05` **and** `CI lower>-0.15` **and** pooled `|r|<0.15` **and** `8/8` variance `FP<=0.15`.
- **C5:** `|rho_shuffled|<0.20` trajectory-grouped `B=5000`, `within-f std>0`, `CI width>0`.
- **C6:** HIT `330/330` byte-identical and `oracle-free >=90%` HIT correct `0` ambiguous.
- **C7/C8:** Browser `PC-HEALTH>=80%` `DOM21-82` `AX>10` `N=20` pool `effective_distinct_n>1`, discrimination `full>0.5` with correct baselines `0.0`, gradients `B=1000` width>0 for `>=2` magnitudes → ordering claim.

Expected: **Pass** for `C1-C6` if header-only + honest sum + oracle-free are correct; **Fail** if any confound persists. `B-BODY-HASH-REJECTED` expected to **fail** even with same data (validates filter necessity).

## 10. Uncertainty method

- `TN` Wilson `95%` lower bound per endpoint + mean.
- `r` Fisher-z transformed CI `95%` with `n_non304` denominator; TOST `p_upper = 1 - Phi((fisher_r - fisher_delta)/se)` (correct tail, not `Phi` alone — prior error `~1.0` vs `4.5e-08`).
- `rho_shuffled`: trajectory-grouped permutation `B=5000` (group=`trajectory_id`), within-f `std` and CI width reported.
- Browser `full vs null`: `B=1000` bootstrap per comparison `N=20`, `effective_distinct_n` and CI width reported; degenerate `[1.0,1.0]` with `effective=1` is **not** precision.
- Per-batch `SELECT` timestamps for commitment verification.

## 11. Adequacy rule

- `n_non304>=800` with `>=400` per endpoint after filtering `is_304==false` and `hs256_valid_success>=0.90`.
- `batch_state_log >=10` distinct `count(*) FROM sessions` timestamps with `COMMIT` verified.
- `health-gate` `0` missing `GET /health` via origin (or nginx single-upstream) `200 + X-Worker-Pid` (retry 30s).
- Browser `N=20` per state with `effective_distinct_n>1` via pool, `AX>10` median `PC-HEALTH>=80%` `DOM21-82`.
- If adequacy fails → `MEASUREMENT_INVALID` (not `SUPPORTS`/`FALSIFIED`).

## 12. Falsification / survival rule

**SUPPORTS (single-node honesty gate restored)** requires **ALL** mandatory with validity passing:

- `C1` `mean TN>=0.85` `Wilson lo>0.75` header-only (single-node).
- `C2` `n_non304>=800` stratified `400` per endpoint `0` missing.
- `C3/C4` `TOST p_upper<0.05` `CI upper<0.15` `pooled|r|<0.15` `8/8` variance `FP<=0.15` header-only de-confounded `r<0.30`.
- `C5` `|rho_shuffled|<0.20` trajectory-grouped `B=5000` `within-f std>0` `width>0`.
- `C6` `330/330` HIT/DYNAMIC byte-identical + `oracle-free >=90%` `0` ambiguous + stale branches identical.
- `C7` browser provision `AX>10` `PC-HEALTH>=80%` `DOM21-82` `N=20` pool `effective>1`.
- `C8` browser discrimination + gradient `B=1000` width>0 for `>=2` magnitudes (ordering beyond degenerate).

**Degraded SUPPORTS_SINGLE_NODE_NO_BROWSER:** `C1-C6` pass but `C7/C8` provision fails because `Playwright/BrowserGym` not installed despite health-gate — counts as honesty-gate pass without browser, not full `SUPPORTS`.

**FALSIFIED-IN-SETTING:** Any `C1-C6` fails while validity passes → bounded falsification on `Flask 3.1.3 + PyJWT 2.14.0 HS256 + SQLite WAL + nginx 1.24.0 + 1280x720` localhost. `B-BODY-HASH-REJECTED` failure does **not** count as falsification of header-only — it is expected.

**MEASUREMENT_INVALID** if any validity gate fails: `hash(body)%10000` alone, `CLEN/ETag` not excluded, status prefix, synthetic `np.random` bodies, `jitter`/`n*3200`/`f*6.0` in cost, `SHA oracle` inside greedy loop, `health-gate` missing, `direct relabeled as browser`, `SELECT commitment` not verified, recompute mismatch. Production CDN `0` HIT is **ceiling** not gating if nginx `C6` passes. Distributed `shared-WAL`/`sticky` remain `UNKNOWN` — not implied by single-node result.

Per contract, `status` describes measurement validity; valid negative is `status=COMPLETE` `outcome=FALSIFIES`, not infrastructure failure.

## 13. Validity threats & mitigations

| Threat | Mitigation | Audited check |
|---|---|---|
| **Body/header conflation** (`CLEN/ETag` body-derived in structural) | `MINUS` set enforced via `grep`; `B-BODY-HASH-REJECTED` proves failure when included | `grep filter_headers` + recompute Jaccard |
| **Oracle tautology** (`ground_truth_sha` inside greedy loop → `240/240`) | `grep` no `ground_truth_sha` in loop; `MAX_DEPTH5` fixed; ambiguous flag logged | `grep` + path audit |
| **Bijective honest-cost** (`n*3200`, `f*6.0`, `random.gauss` jitter) | Frozen sum `resolve+bind+verify+freshness+browser_steps` per `trajectory_id`, trajectory-grouped `B=5000`, `grep` bans | `grep` + `|rho_shuffled|<0.20` |
| **Scheduling confound** (`body_variant` correlated with drift) | Random independent assignment + recomputed `Pearson`/`CramersV <0.30` | `r`/`V` recompute |
| **TOST wrong tail** (`Phi` vs `1-Phi` → `p~1.0` vs `4.5e-08`) | Fisher-z correct `p_upper = 1-Phi((z_delta - z_r)/se)` | Audit recompute |
| **nginx HIT absent** (free-tier `0` HIT `273/273` DYNAMIC-only) | Local `nginx 1.24.0` `proxy_cache` with warmup `>=1` HIT required; `330/330` identity checked | `X-Cache` log |
| **Degenerate browser CI** (`[1.0,1.0]` with `effective=1` claimed as precision) | `N=20` pool `A vs A_alt 50%` + `effective_distinct_n>1` + `B=1000` width>0 mandatory | `effective_distinct_n` audit |
| **Single-node vs distributed confusion** | Explicit scope: single-node only, distributed remains `UNKNOWN` | `provenance` path notes `/35937588416/app.db` single file |

## 14. Consequences

- **If SUPPORTS:** Minimal honesty gate closes. Single-node `TN>=0.85` + `|r|<0.15` + `|rho_shuffled|<0.20` + `330/330` + `oracle-free >=90%` + browser `AX>10` `DOM21-82` `B=1000` non-degenerate CIs validates the audited harness cross-lane needs. Claim ceiling expands from `local nginx island EXPERIMENTAL` to `single-node honest substrate EXPERIMENTAL` (real HTTP `127.0.0.1`, `31-117B`, single viewport). Does **not** promote `C-MEAS-VALID` to `VALIDATED`/`PRODUCT_CORE` (still bounded single-host). Authorizes next experiment: distributed `HS256` shared-WAL `800`-stratified HIT (`2x gunicorn 19860+19861` via `nginx 19851` round-robin) and honest residual-novelty economics vs `RAG`/`Stagehand`.
- **If FALSIFIED-IN-SETTING (valid):** Honesty fix insufficient even at single-node. Bounds `C-MEAS-VALID` to loopback `EXPERIMENTAL` without honesty, prevents false `VALIDATED` promotion, forces true header canonicalization / counter grouping / nginx config redesign before distributed.
- **If MEASUREMENT_INVALID:** Synthetic or validity breach — no ceiling change, requires fixed rerun. Distributed hypotheses stay `UNKNOWN`.

## 15. Parent handoff continuity (SUPERSEDE, not repeat)

- **Established (reused, not re-proved):** `local nginx 1.24.0 proxy_cache byte-preserving HIT 330/330` (`EXP-RUNTIME-35551516706` `240/240` `330/330` `0` ambiguous), `C-FRESHNESS` orthogonality at `delta0.15` **confirmed only on localhost mock `n=480`** (`EXP-GRAPH-35389145821` `r=0.0022` `CI upper 0.0916` `TOST p0.0006` audit `PASS`), prior distributed `r≈-0.0381` but `TN 0.6667` per-node.
- **Rejected (must not reuse):** `per-node isolated SQLite` achieving `TN>=0.85` (`mean 0.6666 session 0.0`), `hash(body)%10000` as header-only surrogate (`r=0.721` `p=1.0`), `honest-cost n*3200/jitter/f*6.0` (`|rho_shuffled|>0.20`), fixed-order decompression `60/240`, sticky `skew 0.666` with `3` URIs.
- **Unknown (tested here at single-node):** Whether header-only `MINUS` body-derived + per-batch `SELECT` + real `304` `n_non304>=800` + honest sum `|rho_shuffled|<0.20` + oracle-free `MAX_DEPTH5` + browser `AX>10` pool achieve `C1-C8` without distributed WAL.
- **Do-not-assume:** Do not assume `TN 0.976`/`r 0.72`/`rho 0.132` from prior `MEASUREMENT_INVALID` prove frozen header-only/honest-cost; `0.0` metrics from prior `0/15` health-gate are null not falsification; degenerate `CI [1.0,1.0]` with `effective=1` is ceiling artifact; prior `0 HIT` on free-tier is ceiling not falsification of `byte-preserving`; `C-MEAS-VALID`/`C-FRESHNESS` are **not** `VALIDATED`/`PRODUCT_CORE` (audit `MEASUREMENT_INVALID`, ceiling `EXPERIMENTAL`).

## 16. Estimated cost & information gain

**Cost:** Low — `single Flask` (or single `gunicorn` worker) + optional single-upstream `nginx 1.24.0` + `SQLite WAL` at `/tmp/spider-runtime/35937588416/app.db` (no `2x` `gunicorn` `shared WAL`, no paid CDN). `N~1200` for `n_non304>=800` `~8-10min`, HIT `48×5` `~6-8min`, honest-cost `B=5000` `~1-2min`, browser `AgentLab 0.14.3` + `Playwright npx chromium` `~3-5min` + `N=20` pool `~10-12min`. Total `~30-40min`.

**Expected information gain:** Very high per Director `comparative_reasoning`: first joint isolation of `body/header` + `oracle` + `cost` confounds at minimal cost, unblocking `Graph` `C-FRESHNESS`/`DELTA-REPAIR`, `Product` residual-novelty honest economics, and `Frontier` live replication before any distributed `shared-WAL` `800`-stratified HIT retry. Valid positive or negative directly changes `Codex` ceiling from degenerate `single-host loopback [1.0,1.0]` to honest single-node `EXPERIMENTAL` or bounded falsified single-node.

## 17. Provenance to be logged

`run_experiment.py` `SHA`, `freeze.json` hashes, `HS256` secret `len>=32` hash, `Flask/PyJWT/SQLite/Werkzeug/nginx/AgentLab/Playwright/CDP/BrowserGym 0.14.3` versions, per-observation `scheduling_seed`, `body_variant`, `trajectory_id`, `honest_cost`, `X-Worker-Pid`, `is_304`, `header_only_Jaccard`, `batch_state_log` SHA, `raw_freshness_observations.jsonl` (`~1200`), `raw_hit_observations.jsonl` (`~330`), `raw_browser_observations.jsonl` (`~520`). Recompute of `Jaccard/Pearson/TOST/rho/greedy` must match `0` mismatches.

## 18. Disclosure

Single-node only. `TLS/HTTP2/QUIC` beyond `plain HTTP 127.0.0.1` not tested, `multi-host Redis` beyond single-host single `WAL` not tested, distributed `shared WAL` and `sticky` affinity remain `UNKNOWN` not tested here, `BrowserGym` DOM beyond HTTP triple not tested, body sizes beyond `31-117B` `sort_keys True` not tested, paid CDN `HIT` beyond `nginx` loopback is ceiling check only.

