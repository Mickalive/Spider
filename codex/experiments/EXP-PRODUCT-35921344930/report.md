# EXP-PRODUCT-35921344930 — Execution Report

- **Lane:** product
- **Transaction:** frozen EXECUTE of EXP-PRODUCT-35921344930 (Director REOPEN of claim `C-PRODUCT-ECON`, `cognitive_reset: true`)
- **Status:** MEASUREMENT_INVALID — **outcome: INCONCLUSIVE**
- **Frozen inputs:** request.json `c3bfbb9a…`, spec.json `119615e7…`, prereg.md `90d40e33…` — byte-identical to `freeze.json` hashes (immutable, verified)
- **Environment:** GitHub Actions runner (HEAD `87ff4234`), Python 3.12.14, pip-only stdlib env

## 1. What this transaction was supposed to measure

Per the frozen design, this experiment was authorized to test, on a **distributed HS256 shared-WAL substrate with honest sum counters**, whether the parent file-proxy economics result (`per_hit 1.045`, `rho 0.472`) changes when correlated freshness (`ETag W/body_sha`, ≤10M counter-UDP MTU, 317 inserts/s) and novelty (family-stratified seeds) are closed, with a Docker BrowserGym 0.14.3 (CDP AX, 2000-node, 1280x720) + real gpt-4o-mini 15-step run. Five positive controls (PC1–PC5) and four null controls (NC1–NC4), family-stratified bootstrap 5000 / trajectory-grouped block-permutation 5000, decision rule with explicit precedence.

## 2. What happened instead

The **frozen PRIMARY DEPENDENCY gate** (Director dependencies: *runtime:shared SQLite WAL HS256 sticky nginx + honest sum counters + BrowserGym 1280x720 fixture*) is unsatisfiable in this environment. Raw evidence in `artifacts/substrate_audit.json` (OBS-1..OBS-18):

| Dependency | State |
|---|---|
| Docker daemon | available (0 containers, no BrowserGym/agentlab image) |
| shared SQLite WAL substrate (`shared.db`) | **absent anywhere on filesystem** |
| PyJWT 2.14.0 (HS256) | not installed |
| gunicorn 23.0.0 (2x workers) | not installed (nginx binary-only) |
| numpy / scipy / sklearn / pandas | not installed |
| browsergym / playwright | not installed |
| gpt-4o-mini API key | absent (only GH_TOKEN) |
| repo runtime hardening (`research/runtime/`, `substrates/`) | not landed |

The frozen design anticipates exactly this branch: *"if distributed substrate or rho_proxy_real unavailable → MEASUREMENT_INVALID, not FALSIFIED"*, and **expressly prohibits** the file-proxy fallback for economics claims ("honest counters must be summed via distributed WAL, not file-proxy isolated SQLite"). Therefore no proxy re-run was attempted, no economics numbers were computed, and no claim is made or changed by this transaction.

## 3. What was done, precisely

1. **Substrate audit (raw evidence only)** → `artifacts/substrate_audit.json` (18 command+result observations).
2. **Frozen instrument prep — kernel binding fix (PC2 prerequisite):** re-applied the dot-aware `_PARAMETER` regex to `src/spider/kernel.py` (the exact fix the frozen prereg flags as required before EXECUTE; patched sha256 `d926279d5ee14a044a2f13b8abc09202df9f5adb9e86feaadeb61818a15f4038`, matching the pre-2.0 verified patch), added regression tests (`test_dotted_parameter_slot_binds_fully`, `test_plain_identifier_slot_still_binds`) in `tests/test_kernel.py`; suite **5/5 pass**.
3. **Failure transmission** → `failure.json` (category `substrate-unavailable`, retryable, smallests-next-action recorded).
4. **Result packet** → this `result.json` (mandatory keys all present; scientific controls `unknown`; primaries explicit `null` = unmeasurable, never zero).

No git commit/push/switch/reset was performed; only product-lane roots (`src/`, `tests/`) and the experiment packet directory were touched.

## 4. Interpretation (bounded)

- **This is an infrastructure failure of a frozen dependency, not a scientific negative.** The economics question (`per_hit ≤ 0.85` with correlated freshness; TTL-style proxy vs RAG) remains **OPEN** and untestable until the substrate exists.
- Nothing here updates `C-PRODUCT-ECON`, `C-RESIDUAL-NOVELTY`, or `C-FRESHNESS`; the parent's bounded file-proxy falsification stands as-is and the parent's SUPERSEDE advisory stays non-binding.
- The only durable scientific state produced: PC2's binding-fix prerequisite is now verified in place (kernel tests green), which shortens the retry to pure substrate-dependent measurement.

## 5. Smallest next action for the retry (exact same frozen design, no re-design, no new mandate)

Runtime-lane hardening — deploy `runtime:shared SQLite WAL HS256 sticky nginx + honest sum counters + BrowserGym 1280x720 fixture`:
1. Create `/tmp/spider-runtime/shared.db` (WAL mode) + per-batch SELECT counter service, HS256 PyJWT 2.14.0, 2x gunicorn 23.0.0 behind nginx 1.24.0 round-robin sticky hash; validate 960/960 oracle-free decode TN ≥ 0.85.
2. Provision Docker BrowserGym 0.14.3 (CDP AX, 2000-node, 1280x720, full-DOM) and a real gpt-4o-mini key for 15-step token/browser/latency (`rho_proxy_real ≥ 0.50`).
3. Install numpy/scipy/sklearn/pandas for bootstrap-5000 / block-permutation-5000 statistics.
Then re-run this frozen transaction.