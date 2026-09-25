# Preregistration — EXP-GRAPH-36106653880 (Graph Lane)

**Experiment ID**: EXP-GRAPH-36106653880
**Lane**: graph
**Claim**: C-DELTA-REPAIR
**Status**: FROZEN — Do not modify after freeze.json exists
**Parent Handoff**: EXP-GRAPH-36018188168 (sha256: 581308f6c8dc174e6f7ec2a4835d2268599c5c99f605e4a7b1faf1ebde91b80f)
**Director Mandate**: CONTINUE on C-DELTA-REPAIR with distributed transfer test

---

## 1. Scientific Question

On the bounded-valid distributed shared-WAL HTTP substrate (validated in EXP-RUNTIME-36100549580: nginx 1.24.0 `$request_uri` sticky, 4× gunicorn 23.0.0 workers, Flask 3.1.3, PyJWT 2.13.0 HS256, shared WAL SQLite at `/tmp/spider-runtime/shared.db`, `n_non304 ≥ 800`, If-None-Match/ETag→304 operational), does the **deterministic freshness-gated localized repair mechanism** from EXP-GRAPH-36018188168 retain:

- True Negative rate **TN ≥ 0.85** (Wilson lower bound) on fresh requests
- False Accept rate **FA ≤ 0.10** (Wilson upper bound) on stale requests
- Pooled repair success **≥ 0.70** (Wilson lower bound) across blast radii K1/K2/K3
- Per-family repair **≥ 0.70** (Wilson lower bound) for each drift family
- Same-resource contamination **< 0.10** (Wilson upper bound) per family
- **Lower token and browser cost than cold re-exploration** at amortization factor `f=10`

under trajectory-grouped uncertainty controls (1000 whole-block permutations, 5000 family-stratified bootstraps, registry-clone re-verification)?

---

## 2. Hypothesis

The single-node `SURVIVES_CURRENT_TEST` result (EXP-GRAPH-36018188168) transfers to the distributed substrate with equivalent thresholds because:

1. The **combined freshness guard** (Jaccard 0.85 on required-filtered `{id,name,email}` + `_template`/`X-Csrf-Token` header + ETag SHA256[:16] + `max-age=0`, recalibrated confidences 0.95 fresh / 0.85 stale) is a deterministic function of observable response headers/body — it does not depend on single-process memory.
2. The **k-probe re-observe patch** via `_matches` exact equality on `required_slots` per mutated `id` is a deterministic local overwrite of live response bytes — it does not require cross-worker coordination.
3. Concurrent WAL propagation and multi-worker sticky routing (`$request_uri` with `X-Worker-Pid ≥ 2` distinct) do not degrade the guard/repair signals beyond the single-node operational envelope established at `n_non304 = 500`.

---

## 3. Falsifier

The hypothesis is **falsified** if **ANY** of the following holds (measured on the frozen TEST split with honest instrumentation):

| # | Condition | Threshold | Evidence |
|---|-----------|-----------|----------|
| F1 | Freshness TN (Wilson lower) | < 0.85 | Fresh requests per family per blast radius |
| F2 | Freshness FA (Wilson upper) | > 0.10 | Stale requests per family per blast radius |
| F3 | Pooled repair (Wilson lower) | < 0.70 | All blast radii K1/K2/K3 combined |
| F4 | Per-family repair (Wilson lower) | < 0.70 | Any family at any blast radius |
| F5 | Same-resource contamination (Wilson upper) | ≥ 0.10 | Disjoint-id (20 IDs) + same-resource co-bound |
| F6 | Verification AUROC (TEST12) | < 0.75 | Frozen TRAIN18/TEST12 split |
| F7 | Verification precision (TEST12) | < 0.80 | Frozen TRAIN18/TEST12 split |
| F8 | Token cost at f=10 | ≥ cold_k | K1: 16, K2: 32, K3: 48 |
| F9 | Browser cost at f=10 | ≥ cold_browser | K1: 3, K2: 6, K3: 9 |
| F10 | Permutation max\|ρ\| | ≥ 0.20 | 1000 trajectory-grouped perms (non-vacuous: cost variance > 0) |
| F11 | Bootstrap CI degenerate | [1.0, 1.0] | Without stochastic threshold — flagged as ceiling not precision |

**Measurement validity failure** (any V1–V12 violated) → `MEASUREMENT_INVALID`, not falsification.

---

## 4. State Representation

### 4.1 Raw Observables (Preserved)
Per-request raw evidence recorded in `raw_evidence.jsonl`:
- Full HTTP response: status, headers (all), body (canonical JSON)
- Request: method, URL, headers, body
- `X-Worker-Pid` header (proves sticky routing)
- `ETag` header (SHA256(canonical_json_without_template)[:16])
- `Cache-Control` header (must include `max-age=0` for stale)
- Timing: `request_ts`, `response_ts`, `latency_ms`
- Auth state: JWT `Authorization` header (HS256 verified)
- WAL state: SQLite `journal_mode=WAL`, `synchronous=NORMAL` verified

### 4.2 Derived State (Frozen from Parent)
**Freshness Guard Signal** (exact equality to EXP-GRAPH-36018188168):
```
stale = (jaccard < 0.85) OR (param_template_changed) OR (etag_changed AND max_age_0)
```
- **Jaccard**: on `required_slots = {id, name, email}` only — ignores `phone`, `nickname`, `detail`, nested depth, magnitudes
- **param_template_changed**: `_template` field (endpoint path template) differs from registry
- **etag_changed**: `ETag` header differs from registry AND `Cache-Control: max-age=0` present
- **Recalibrated confidences**: fresh=0.95, stale=0.85 (frozen from single-node calibration)

**Repair Signal**:
- `k-probe re-observe`: for each mutated `id`, execute `k` probe requests (GET `/resource/{id}`) and apply `_matches` exact equality on `required_slots` to overwrite registry
- **Blast radii**: K1=1 probe, K2=2 probes, K3=3 probes per stale detection
- **Token cost**: `k * 5` tokens per repair (5 tokens per probe — synthetic proxy)
- **Browser cost**: `k` browser steps per repair (1 step per probe — synthetic proxy)
- **Verify cost**: 1 verify call per probe (synthetic proxy)

### 4.3 Drift Families (Frozen from Parent)
| Family | Drift Type | Affected Fields | Guard Channel Triggered |
|--------|------------|-----------------|------------------------|
| `dom` | DOM structure | `detail` (0.60–0.75 Jaccard drop) | Jaccard on required_slots |
| `param_header` | Param + header | `uid` → `id` + `X-Csrf-Token` xyz | template/header + Jaccard |
| `cache` | Cache/ETag | `ETag` change + `max-age=0` | ETag+max-age0 |

**Noise Family (Null Control)**: `noise` — independent random perturbation on `phone` (p=0.3) and `nickname` (p=0.3), NOT in required_slots, no template/header/ETag change.

---

## 5. Action Representation

| Action Type | Description | Cost Model |
|-------------|-------------|------------|
| `GUARD_CHECK` | Evaluate freshness guard on response | 0 tokens, 0 browser |
| `K_PROBE` | GET `/resource/{id}` + `_matches` overwrite | 5 tokens, 1 browser, 1 verify |
| `COLD_EXPLORE` | Full re-exploration from scratch | `k*5` tokens, `k` browser (K1=16/3, K2=32/6, K3=48/9) |
| `VERIFY` | Post-repair `_matches` re-check | 1 token, 0 browser |

**Honest Cost Counters** (per-trajectory-reset integer sums, no jitter):
- `tokens_total = sum(k_probe * 5) + verify_calls`
- `browser_total = sum(k_probe)`
- `verify_total = sum(k_probe)`

---

## 6. Sampling Policy

### 6.1 Substrate Precondition (Runtime Gate)
Before Graph repair test begins, **ALL** EXP-RUNTIME-36100549580 health gate criteria (D1–D13) must PASS on the distributed substrate:
- nginx 1.24.0 `$request_uri` sticky with `X-Worker-Pid ≥ 2` distinct
- 4× gunicorn workers sharing single WAL SQLite
- `If-None-Match` / `ETag` → 304 operational
- Header-only Jaccard (filtered minus `{content-length,etag,w-etag,range}`) non-zero variance, `|r| < 0.30`, `V < 0.30`
- Full-vector discrimination > `max(body, status) + 0.05`
- HMAC-SHA256 per auth_state stable-header mutation
- Greedy brotli→gzip `MAX_DEPTH5` oracle-free decompression byte-identical

### 6.2 Data Collection
- **Target**: `n_non304 ≥ 800` (non-304 responses) before `f=100` (deferred)
- **Stratification**: ≥ 10 fresh + ≥ 10 stale per family per blast radius (K1/K2/K3)
- **Split**: TRAIN 18 trajectories / TEST 12 trajectories (frozen from parent)
- **Trajectory grouping**: Whole trajectories kept together for permutation/block bootstrap
- **Seeds**: Deterministic per-trajectory integer seeds (no Python `hash()` randomization)

### 6.3 Blast Radius Design
| Blast Radius | Probes (k) | Cold Tokens | Cold Browser | Fresh Target | Stale Target |
|--------------|------------|-------------|--------------|--------------|--------------|
| K1 | 1 | 16 | 3 | ≥ 30/family | ≥ 10/family |
| K2 | 2 | 32 | 6 | ≥ 20/family | ≥ 10/family |
| K3 | 3 | 48 | 9 | ≥ 20/family | ≥ 10/family |

Total trajectories: ~150 fresh + ~50 stale per blast radius across 3 families = ~600 trajectories minimum.

---

## 7. Baselines and Controls

### 7.1 Baselines (Stable Identifiers for Downstream)

| ID | Name | Description | Frozen Expected |
|----|------|-------------|-----------------|
| `B-COLD` | Cold Re-exploration | Full k×5 probe tokens, k browser steps, no guard, no repair | `repair=0.0, TN=0.0, FA=1.0, cost=cold` |
| `B-NO-GUARD` | Always Executable | k-probe repair on ALL requests regardless of staleness | `repair≈1.0, FA=1.0 on stale, cost=k*5` |
| `B-ORACLE` | Perfect Oracle | Ground-truth stale/fresh labels + perfect k-probe repair | `TN=1.0, FA=0.0, repair=1.0, cost=k*5` (ceiling) |
| `B-VERBATIM` | Literal Replay | Exact cached action sequence replay | `repair=0.0 on drift, FA=0.0` |
| `B-RETRIEVAL` | Retrieval/RAG | TF-IDF Jaccard 0.30 retrieval, no k-probe patch | `repair_delta_vs_SPIDER ≥ 0.30` |

### 7.2 Positive Control
**`PC-DISTRIBUTED-HEALTH-GATE`** — EXP-RUNTIME-36100549580 distributed substrate validation.
- **Must PASS** before Graph test begins.
- If Runtime gate fails → `BLOCKED` (infrastructure), not `MEASUREMENT_INVALID`.

### 7.3 Null Control
**`NC-NOISE`** — Noise-only drift family.
- Independent random perturbation on `phone` (p=0.3), `nickname` (p=0.3)
- NOT in `required_slots`, no template/header/ETag change
- **Expected**: `FA ≤ 0.05` (Wilson upper), `repair ≈ 0.0`, `contamination ≈ 0.0`

### 7.4 Uncertainty Controls (Trajectory-Grouped)
| Control | Method | Threshold | Purpose |
|---------|--------|-----------|---------|
| `UC-PERM` | 1000 whole-trajectory-block permutations | `max\|ρ\| < 0.20` | Tests graded cost correlation (non-vacuous: cost variance > 0) |
| `UC-BOOT` | 5000 family-stratified trajectory-grouped bootstraps | Wilson CI width > 0 | Binomial CIs for repair/FA/TN; percentile for continuous |
| `UC-CLONE` | Registry clone snapshot + `_matches` re-verify | Contamination < 0.10 | Disjoint-id (20 IDs 9000–9019) + same-resource co-bound |

---

## 8. Decision Rule (Frozen)

### 8.1 Primary (ALL must PASS for `SURVIVES_CURRENT_TEST`)

| Rule | Metric | Threshold | Split |
|------|--------|-----------|-------|
| D1 | Freshness TN (Wilson lower) | ≥ 0.85 | Fresh requests |
| D2 | Freshness FA (Wilson upper) | ≤ 0.10 | Stale requests |
| D3 | Pooled repair (Wilson lower) | ≥ 0.70 | All K1/K2/K3 |
| D4 | Per-family repair (Wilson lower) | ≥ 0.70 | Each family × blast radius |
| D5 | Same-resource contamination (Wilson upper) | < 0.10 | Disjoint-id + co-bound |
| D6 | Verification AUROC | ≥ 0.75 | Frozen TEST12 |
| D6 | Verification precision | ≥ 0.80 | Frozen TEST12 |
| D6 | Permutation null AUROC | ∈ [0.40, 0.60] | Shuffled TRAIN |
| D7 | Token cost at f=10 | < cold_k (16/32/48) | K1/K2/K3 |
| D7 | Browser cost at f=10 | < cold_browser (3/6/9) | K1/K2/K3 |

**Outcome mapping**:
- All D1–D7 PASS → `SURVIVES_CURRENT_TEST`
- Any D1–D7 FAIL → `FALSIFIES`
- Measurement validity (V1–V12) failure → `MEASUREMENT_INVALID`
- Infrastructure failure (Runtime gate, substrate) → `BLOCKED`

### 8.2 Secondary (Reported, Not Gating)
- Global ECE ≤ 0.15, fresh ECE ≤ 0.05, stale ECE ≤ 0.15
- Ablation: `B-JACCARD-ONLY` FAILS ≥ 2 families, `B-HEADER-ONLY` FAILS ≥ 2 families
- Cost scaling: k×5 tokens and k browser steps verified per blast radius
- Per-family Wilson lower bounds reported (K2/K3 n=3–4 limited power disclosed)

---

## 9. Uncertainty Quantification

### 9.1 Permutation Test (Cost Correlation)
- **Unit**: Whole trajectory blocks (preserves within-trajectory correlation)
- **Iterations**: 1000
- **Statistic**: Pearson ρ between `novelty_fraction` and `M_total_f10` (tokens + browser weighted)
- **Null**: Shuffled trajectory blocks (breaks novelty↔cost link)
- **Threshold**: `max\|ρ\| < 0.20` (non-vacuous: requires cost variance > 0; parent had zero variance → vacuous pass)

### 9.2 Bootstrap (Repair/FA/TN CIs)
- **Method**: 5000 family-stratified trajectory-grouped bootstrap resamples
- **Binomial**: Wilson score intervals (preferred for proportions)
- **Continuous**: Percentile intervals (tokens, browser)
- **Degenerate CI handling**: `[1.0, 1.0]` or `[5.0, 5.0]` → flagged as deterministic ceiling, Wilson lower bound reported instead

### 9.3 Verification Discrimination
- **Split**: TRAIN 18 / TEST 12 (frozen from parent, indices fixed)
- **Metric**: AUROC and precision on TEST
- **Null**: Permutation-shuffled TRAIN labels (trajectory-grouped), AUROC expected ∈ [0.40, 0.60]

---

## 10. Validity Threats and Representation Loss (Disclosed)

| Threat | Description | Mitigation / Disclosure |
|--------|-------------|-------------------------|
| **V1: Deterministic flat-JSON only** | No SPA, no DOM, no visual, no auth/session drift beyond JWT | Disclosed: claim ceiling = deterministic flat-JSON /resource/{id} only |
| **V2: ETag truncated 16 hex** | SHA256[:16] loses collision resistance | Disclosed: 16 hex = 64 bits, collision probability negligible at n=800 |
| **V3: Required-slots only** | Jaccard ignores `phone`, `nickname`, `detail`, nested structure | Disclosed: guard blind to non-required fields; ablation tests this |
| **V4: Per-trajectory cache = 3 obs** | May miss rare fields appearing < 3 times | Disclosed: limited observation window |
| **V5: Single-node → distributed gap** | WAL propagation latency, sticky routing imperfect, concurrent writes | Tested: this experiment IS the transfer test; failure bounds locality |
| **V6: Synthetic cost proxy** | 5 tokens/probe, 1 browser/probe — no real LLM/Playwright | Disclosed: f=100 real LLM/Playwright deferred per Director mandate |
| **V7: Degenerate bootstrap at ceiling** | Perfect repair → [1.0,1.0] CI not high precision | Wilson lower bounds reported (e.g., 30/30 → 0.886) |
| **V8: Vacuous permutation ρ** | Zero cost variance → Pearson undefined → 0 | Require cost variance > 0; parent had zero variance |
| **V9: Limited per-family power** | K2/K3 n=3–4 per family → Wilson upper 0.277–0.390 | Pooled n=10 lower 0.722 is informative bound; disclosed |
| **V10: No cross-site holdout** | Single endpoint `/resource/{id}` only | Claim ceiling = single-resource distributed; not cross-site |
| **V11: nginx config not archived** | Parent provenance gap: nginx version captured but config not archived | This run: nginx conf archived, version captured in provenance |
| **V12: Target leakage prevention** | Stale/fresh labels from guard only, never ground-truth drift | Enforced: guard signals computed before drift label known |

---

## 11. Artifacts to Produce

| Artifact | Path | Role |
|----------|------|------|
| Raw evidence (JSONL) | `raw_evidence/raw_evidence_distributed.jsonl` | raw |
| Health gate verification | `raw_evidence/health_gate_distributed.json` | fixture |
| Summary metrics | `raw_evidence/summary_distributed.json` | derived |
| Decision outcome | `raw_evidence/decision_distributed.json` | derived |
| Spec (frozen) | `spec.json` | fixture |
| Prereg (frozen) | `prereg.md` | fixture |
| Freeze hashes | `freeze.json` | fixture |
| Result (EXECUTE output) | `result.json` | derived |
| Report (EXECUTE output) | `report.md` | derived |
| Provenance (EXECUTE output) | `provenance.json` | derived |

---

## 12. Code and Implementation References (Frozen)

- **Kernel repair**: `src/spider/kernel.py` → `_matches` (sha256: 46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61)
- **Single-node execution**: `research/graph/delta_repair/execute_delta_repair_single_node_36018188168.py` (sha256: 1bdec6bc)
- **Single-node Flask app**: `research/graph/delta_repair/flask_app_36018188168.py` (sha256: 727f68f)
- **Distributed Flask app**: `research/graph/delta_repair/flask_app_distributed_36106653880.py` (new, extends single-node for 4-worker WAL)
- **Nginx config**: `research/graph/delta_repair/nginx_distributed.conf` (new, `$request_uri` sticky, 4 upstream)
- **Execution script**: `research/graph/delta_repair/execute_delta_repair_distributed_36106653880.py` (new)

---

## 13. Consequences

### If Positive (`SURVIVES_CURRENT_TEST`)
- C-DELTA-REPAIR upgraded from **single-node EXPERIMENTAL** → **distributed EXPERIMENTAL** (VALIDATED candidacy)
- Product lane may integrate distributed delta-repair into kernel with confidence
- **Does NOT authorize**: PRODUCT_CORE, SHIPPED, cross-site generalization, real LLM/Playwright at f=100
- Next gate: real LLM/Playwright instrumentation at f=100 + cross-site holdout

### If Negative (`FALSIFIES`)
- C-DELTA-REPAIR **bounded to single-node health-gated substrate only**
- Distributed WAL propagation, concurrent multi-worker sticky routing, or nginx load balancing degrades guard/repair below thresholds
- Graph lane **parks C-DELTA-REPAIR** at single-node EXPERIMENTAL
- Per Director mandate: reassess C-PARAM-INHERIT rather than deepen C-DELTA-REPAIR indefinitely

### If `MEASUREMENT_INVALID` or `BLOCKED`
- No scientific conclusion
- Exact failure mode documented in `validity_notes` / `unresolved`
- Retry with fixed substrate or measurement only (no design change post-freeze)

---

## 14. Dependencies (Exact Immutable References)

1. **Runtime substrate**: EXP-RUNTIME-36100549580 (distributed shared-WAL HTTP DISTRIBUTED VALIDATED)
   - `handoff.json` sha256: `2315367865a2d9d4f2f9acad3f02cb04f0f262b7d8e541281285c0e818f202a3`
2. **Single-node repair mechanism**: EXP-GRAPH-36018188168 (SURVIVES_CURRENT_TEST)
   - `handoff.json` sha256: `581308f6c8dc174e6f7ec2a4835d2268599c5c99f605e4a7b1faf1ebde91b80f`
3. **Prior synthetic ceiling**: EXP-GRAPH-35952148696 (audit PASS D1–D10)
4. **Parent MEASUREMENT_INVALID (operational, not scientific)**: EXP-GRAPH-35999336958 (9 fixes now addressed)

---

## 15. Estimated Cost and Timeline

| Phase | Duration | Resources |
|-------|----------|-----------|
| Substrate startup (nginx + 4× gunicorn + WAL) | ~20 min | 4 workers, nginx, SQLite WAL |
| Health gate verification (D1–D13) | ~10 min | Same |
| Graph repair test (n_non304 ≥ 800) | ~30 min | Same + Graph execution |
| Analysis (perms, bootstraps, Wilson) | ~5 min | Single process |
| **Total wall-clock** | **~65 min** | — |

**No LLM/API calls** (synthetic token/browser proxy only). Real LLM/Playwright at f=100 deferred per Director mandate.

---

## 16. Expected Information Gain

**High**. This is a **binary discriminating gate** for the C-DELTA-REPAIR claim ceiling:

- **Positive**: Mechanism is substrate-portable → distributed EXPERIMENTAL → Product integration path open
- **Negative**: Mechanism is single-node artifact → claim bounded → lane reassesses C-PARAM-INHERIT

Controls isolate **WAL propagation** vs **sticky routing** vs **guard signal degradation** — not merely "does it work." The honest cost accounting (per-trajectory-reset integers, no jitter) and trajectory-grouped uncertainty (permutations + stratified bootstraps) directly address the parent's `do_not_assume` items about vacuous correlation and degenerate CIs.

This experiment **cannot** establish real-site generalization, cross-site transfer, or LLM-heuristic robustness. Those remain UNKNOWN per parent handoff and Director mandate.

---

**FROZEN** — This preregistration must not change after `freeze.json` is created. Any design change requires a new experiment ID.