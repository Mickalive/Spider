# EXP-RUNTIME-36106663091 — Preregistration

## 1. Experiment Identity
- **experiment_id**: EXP-RUNTIME-36106663091
- **lane**: runtime
- **claim_ids**: [C-MEAS-VALID]
- **parent_handoff**: EXP-RUNTIME-36103366713 (sha256: 7e92e3f578b1ee2237aa0dc87830ae19c7df11a3d16a426e0b361e49c849c81d)
- **director_mandate**: CONTINUE C-MEAS-VALID cognitive_reset=true — highest-leverage portfolio action to repair real-browser intervention substrate

## 2. Strategic Question (Director Mandate)
Can the already bounded-valid distributed stable-header HTTP substrate be extended, **without synthetic fallback**, to real Playwright Chromium/BrowserGym CDP observation plus actual writable, authentication, session, drift, and side-effect controls whose prescribed positive and negative interventions are correctly distinguished?

## 3. Hypothesis
The distributed stable-header substrate at `/tmp/single.db` maintains all canonical C1-C5 gates when measurement is extended to **real** BrowserGym Playwright CDP 1280x720 DOM/AX observation and **real** Playwright writable SPA interactions, with discriminating positive ≥0.5 and all null controls 0.0 (nullFP≤0.05).

## 4. Falsifier
Any single condition failure triggers FALSIFIES (if validity gates pass) or MEASUREMENT_INVALID (if infrastructure fails):
1. **C1**: `freshness_n_non304 < 800` OR per-endpoint `< 400`
2. **C2**: header-only Jaccard `|r| ≥ 0.30` OR `V ≥ 0.30` OR `nullFP > 0.05` OR `variance ≤ 0` OR `std ≤ 0` OR `mean ≥ 1.0` OR `same_state_J < 1.0`
3. **C3**: honest-cost `|rho_shuffled| ≥ 0.20` OR `p < 0.20` OR `within_f_std ≤ 0`
4. **C4**: full-vector `full ≤ 0.5` OR `full ≤ max(body,status)+0.05` OR `diff_lo ≤ 0` OR `null > 0`
5. **C5**: loopback `header_drift ≥ 0.05` OR `body_drift ≥ 0.05` OR `nullFP > 0.0` OR `HIT < 330/330`
6. **Browser health**: `AX_median ≤ 10` OR `PC_HEALTH < 0.80` OR `DOM_median ∉ [21,82]` OR `viewport_ok = false`
7. **TRAIN-only k-means k=20**: `leakage_pass = false` (centroid_diff ≤ 0 OR same_state_J_kmeans < 1.0)
7. **Writable matrix**: `pos_rate < 0.5` OR any `null_rate > 0.0` OR `nullFP > 0.05` OR `dom_delta_pos_rate < 1.0` OR `wal_pos_mutated_rate < 1.0` OR any `null wal_mutated = true`

## 5. Canonical Substrate (Frozen from Parent — No Regression Permitted)
- **DB**: `/tmp/single.db` SQLite WAL `check_same_thread=False` factory `create_app()`
- **WSGI**: `/tmp/wsgi.py` with `sys.path.insert(0, str(Path(__file__).parent))` before `from run_experiment import create_app`
- **Flask**: 2x gunicorn 23.0.0 workers binding `127.0.0.1:19860` and `127.0.0.1:19861` sharing single.db WAL
- **nginx**: exclusive `nginx -c /tmp/single.db.nginx.conf` on port 19851, upstream 2 servers, **single** `hash $request_uri consistent`, real `proxy_cache spider_cache` at `/tmp/single.db.cache` ENABLED
- **Headers**: HMAC-SHA256(TESTBED_SECRET, auth_state)[:16] per auth_state, **NO uuid4**; filtered MINUS `{content-length,etag,w-etag,range}` for header-only; fingerprint EXCLUDES `{Date,Server,X-Request-Id,CF-RAY,CF-Cache-Status,X-Cache,Age,X-Worker-Pid}`
- **Greedy decompression**: brotli→gzip MAX_DEPTH5
- **Honest-cost**: per-trajectory integer sums B=1000 block-permuted by trajectory_id
- **Health gate**: distributed nginx 19851 + BOTH origins 19860/19861 verified listening, X-Worker-Pid on every 200, 0 missing
- **Stickiness**: $request_uri consistency ≥0.90 per URI, X-Worker-Pid distinct ≥2

## 6. New Browser Extension (This Experiment's Scope)

### 6.1 Provisioning Gate (Mandatory — Failure = MEASUREMENT_INVALID)
```python
# Must succeed before any browser metrics are computed
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    # Verify chromium executable exists
    import playwright._impl._path_utils as pu
    assert pu.get_executable_path("chromium").exists()
    browser.close()

# BrowserGym import
import browsergym  # version 0.14.3 required
# agentlab 0.4.2 attempted but not required if BrowserGym works
```

**No synthetic fallback.** If provisioning fails, experiment halts with `status=MEASUREMENT_INVALID`, all browser-dependent metrics = `null`, all browser-dependent controls = `UNKNOWN`.

### 6.2 BrowserGym CDP 1280x720 Capture
- **Viewport**: 1280x720 verified via `page.viewport_size` **AND** `cdp.send("Emulation.setDeviceMetricsOverride", {"width":1280,"height":720,"deviceScaleFactor":1,"mobile":False})`
- **Targets**: 80 pages across endpoints: `/resource_page`, `/resource`, `/api/profile`, `/api/data_list` (20 each)
- **Per page**:
  - `page.goto(url, wait_until="domcontentloaded", timeout=5000)` + `page.wait_for_timeout(100)`
  - DOM count: `page.evaluate("() => document.querySelectorAll('*').length")`
  - AX tree: `cdp_session.send("Accessibility.getFullAXTree", {})` → count nodes
  - Fetch via `page.request.get(url, headers={"Authorization": f"Bearer {valid_token}"})` for body/headers/X-Worker-Pid
- **Health metrics**:
  - `AX_median > 10`
  - `PC_HEALTH = fraction(AX > 10) ≥ 0.80`
  - `DOM_median ∈ [21, 82]`
  - `viewport_ok = true`

### 6.3 Real DOM/AX Feature Vectors (Per Observation)
Computed from **real** CDP AX tree and DOM:
- **Tag histogram**: normalized counts of top 20 HTML tags from `document.querySelectorAll('*')`
- **AX role histogram**: normalized counts of top 15 AX roles from `Accessibility.getFullAXTree` nodes
- **Control counts**: raw counts of `<input>`, `<select>`, `<textarea>`, `<button>` elements
- **Vector dimension**: ~40 features (20 tag + 15 role + 5 control)

### 6.4 TRAIN-only k-means k=20
- **Split**: 60/40 by trajectory_id (first 60% = TRAIN)
- **Fit**: `KMeans(n_clusters=20, random_state=44, n_init=10)` on TRAIN features only
- **Test assignment**: `predict(X_test)` using TRAIN centroids only
- **Leakage check**: refit on combined data, compute `centroid_diff = ||centroids_train - centroids_combined[:20]||`
- **Leakage pass**: `centroid_diff > 1e-6` AND `same_state_J_kmeans == 1.0` (duplicate same-state observations assigned to same cluster)

### 6.5 Writable-Controls Matrix via Playwright
**Target endpoints**: `/api/write/profile`, `/api/write/data_list`, `/api/write/controls_matrix` (via distributed nginx 19851)

**Positive cell (VALID_AUTH_WRITE)**:
```python
# Via Playwright page interactions on /resource_page form
page.goto(f"http://127.0.0.1:19851/resource_page?uid={i}")
page.fill('input[name="name"]', "test_value")
page.select_option('select[name="role"]', "admin")
page.fill('textarea[name="bio"]', "updated bio")
page.click('button[type="submit"]')
# Also direct API POST via page.request.post
resp = page.request.post(f"http://127.0.0.1:19851/api/write/profile", 
                         data={"variant": "B"}, 
                         headers={"Authorization": f"Bearer {valid_token}"})
```
- **Expected**: 200 response, fingerprint discriminates (before≠after), DOM_delta > 0, WAL mutated (writable_state count increases)

**Null cells (all must produce 0.0 discrimination, 0 DOM_delta, WAL not mutated)**:
1. **READONLY_GET**: `page.request.get(...)` with valid auth
2. **INVALID_AUTH_WRITE**: `page.request.post(...)` with invalid token → 401
3. **EXPIRED_AUTH_WRITE**: `page.request.post(...)` with expired token → 401
4. **DELETED_SESSION_WRITE**: DELETE sessions via admin, then valid auth write → 401
5. **SAME_STATE_READ**: repeated GET with same valid auth + same body_variant → fingerprint identical, same_state_J=1.0

**Aggregates required**:
- `pos_rate ≥ 0.5` (fraction of positive cells where fingerprint discriminates)
- `all null_rates == 0.0`
- `nullFP ≤ 0.05`
- `dom_delta_pos_rate == 1.0`
- `wal_pos_mutated_rate == 1.0`
- `all null wal_mutated == false`

### 6.6 Browser Fetch Path Discrimination (C2/C4 via Browser)
- **Header-only Jaccard (C2)**: paired valid vs expired same body_variant via `page.request.get` → compute on filtered headers MINUS body-derived
- **Full-vector fingerprint (C4)**: `SHA256(status||decompressed_body||sorted_filtered_headers_json)` via browser fetch
- Both must meet same thresholds as parent C2/C4

## 7. Baselines and Controls (Stable Identifiers for Downstream Transmission)

| Control ID | Type | Description | Expected |
|------------|------|-------------|----------|
| B-DISTRIBUTED-HTTP-TRIPLE | baseline | Parent canonical C1-C5 replicated without regression | PASS |
| B-BROWSER-DOM-AX-STRUCTURAL | baseline | Real CDP DOM/AX health at 1280x720 | PASS |
| B-WRITABLE-POSITIVE | positive | Valid-auth write via Playwright discriminates, mutates WAL | ≥0.5 disc, DOM_delta>0, WAL+ |
| B-WRITABLE-NULL-READONLY | null | Read-only GET via Playwright | 0.0 disc, 0 DOM_delta, WAL= |
| B-WRITABLE-NULL-INVALID-AUTH | null | Write with invalid auth via Playwright | 0.0 disc, 401, WAL= |
| B-WRITABLE-NULL-EXPIRED-AUTH | null | Write with expired auth via Playwright | 0.0 disc, 401, WAL= |
| B-WRITABLE-NULL-DELETED-SESSION | null | Write after session deletion via Playwright | 0.0 disc, 401, WAL= |
| B-WRITABLE-NULL-SAME-STATE | null | Repeated same-state GET via Playwright | 0.0 disc, J=1.0, WAL= |
| B-TRAIN-ONLY-KMEANS | baseline | k=20 TRAIN-only on real DOM/AX features | leakage_pass |
| B-HEADER-ONLY-JACCARD-STABLE-BROWSER | baseline | C2 orthogonality via browser fetch | \|r\|<0.30 V<0.30 J=1.0 nullFP≤0.05 |
| B-FULL-VECTOR-BROWSER | baseline | C4 compositive discrimination via browser fetch | full>0.5 diff_lo>0 null=0 |
| PC-REAL-BROWSER-PROVISIONED | positive_ctrl | Playwright chromium + BrowserGym 0.14.3 + real capture works | PASS |
| NC-SYNTHETIC-FALLBACK-REJECTED | null_ctrl | No synthetic fallback permitted | FAIL if triggered |

## 8. Measurement Validity Gates (Pre-Commitment)
1. Playwright chromium executable verified at runtime before any capture
2. BrowserGym 0.14.3 import verified
3. CDP `Accessibility.getFullAXTree` called per page
4. DOM count via `document.querySelectorAll('*').length`
5. Viewport 1280x720 verified via both `page.viewport_size` and CDP
6. TRAIN-only k-means: strict 60/40 split by trajectory_id, fit TRAIN only
7. Real DOM/AX feature vectors from real CDP/DOM (not synthetic)
8. Writable matrix via Playwright `page.fill`, `page.select_option`, `page.click`, `page.request.post`
9. WAL mutation via direct SQLite `SELECT COUNT(*) FROM writable_state`
10. Honest-cost B=1000 trajectory-grouped permutation (no jitter)
11. All header filtering/fingerprint identical to parent canonical
12. No post-state leakage in any computation
13. Deterministic SEED=44, numpy/sklearn random_state=44

## 9. Decision Rule (Frozen)
```
status = COMPLETE, outcome = SUPPORTS  IFF all C1-C8 pass
status = MEASUREMENT_INVALID           IFF provisioning fails OR any validity gate fails
status = COMPLETE, outcome = FALSIFIES IFF validity gates pass but any C1-C8 condition fails
```

## 10. Consequences
- **Positive**: C-MEAS-VALID → EXPERIMENTAL with BrowserGym DISTRIBUTED VALIDATED ceiling. Unblocks Graph C-DELTA-REPAIR k>1, Product M_total, Frontier live-site, Physics correlated banks.
- **Negative/Blocked**: C-MEAS-VALID remains EXPERIMENTAL with plain-HTTP only. Browser-dependent lanes stay blocked. Next Runtime experiment must fix provisioning or PARK browser thread.

## 11. Scope Boundaries (Explicitly UNKNOWN)
- TLS/HTTP2/QUIC
- Multi-host Redis
- Production CDN/edge
- Compressed encoding beyond greedy MAX_DEPTH5
- Timing-window header canonicalization
- WAL durability beyond /tmp/single.db (reboot, concurrent multi-host, high write contention)
- agentlab 0.4.2 full integration (import checked only)
- BrowserGym task-level evaluation (only observation substrate tested)

## 12. Artifacts to Preserve
- `raw_freshness_observations.jsonl` — all HTTP observations (parent + browser fetch)
- `raw_browser_observations.jsonl` — CDP AX tree, DOM counts, viewport, fetch responses
- `raw_writable_observations.jsonl` — writable matrix cells with before/after fingerprints, WAL counts
- `raw_kmeans_features.jsonl` — real DOM/AX feature vectors per observation
- `raw_trajectory_costs.jsonl` — honest-cost integer sums
- `run_experiment.py` — exact code (sha256)
- `provenance.json` — commits, versions, seeds, hashes

## 13. No-Drift Commitments
- **No synthetic fallback** for browser metrics — provisioning failure = MEASUREMENT_INVALID
- **No re-testing** of plain HTTP C1-C5 beyond replication gate (must pass but not re-optimized)
- **No weakening** of thresholds after seeing outcomes
- **No post-hoc** addition of browser metrics not declared here
- **Same TESTBED_SECRET**, same DB_PATH, same nginx config, same endpoints as parent

## 14. Random Seeds and Determinism
- `SEED = 44` (Python random)
- `numpy.random.seed(44)` where used
- `sklearn KMeans random_state=44`
- Trajectory IDs deterministic: `fresh_{attempt//10}`, `jaccard_pair_{leg}_{idx}`, etc.
- Honest-cost permutation: block shuffle by trajectory_id with B=1000, seed=44