# Preregistration: EXP-GRAPH-36132150213

**Lane:** graph | **Claim:** C-FRESHNESS | **Status:** DESIGN (pre-freeze)

---

## 1. Executive Summary

This experiment tests the **deterministic response-derived freshness guard** on the **certified distributed shared-WAL HTTP substrate** that Runtime has independently validated (EXP-RUNTIME-36100549580, EXP-RUNTIME-36094450333). The freshness guard combines four signals: Jaccard similarity (threshold 0.85) over required DOM fields, endpoint `_template` drift, `X-Csrf-Token` drift, and `ETag` change with `Cache-Control: max-age=0`.

This is the **first valid measurement** of C-FRESHNESS in the Research 2.0 program — the claim has had **zero recent experiments** across all owner lanes. It is the safety gate beneath C-DELTA-REPAIR, C-SEMANTIC-RESOLVE, C-PARAM-INHERIT, C-LLM-INHERIT, and C-PRODUCT-ECON. A false accept silently applies a stale mechanism, contaminating every downstream success margin, abstention calibration, and cost comparison.

---

## 2. Substrate and Preconditions

### 2.1 Certified Distributed Substrate (Mandatory)

The experiment **requires** the following substrate, already certified DISTRIBUTED VALIDATED by Runtime in bounded plain-HTTP scope:

- **nginx 1.24.0** with `$request_uri consistent` sticky routing
- **4x gunicorn 23.0.0** workers running **Flask 3.1.3** / **PyJWT 2.x HS256**
- **Shared SQLite WAL** at `/tmp/spider-runtime/shared.db` (cross-process WAL propagation: harness writes, app reads, immediate visibility)
- **Real `If-None-Match` / `ETag` → 304** revalidation (only when fresh and `max-age=60`)
- **`X-Worker-Pid`** header exposing upstream worker PID (for sticky verification)
- **JWT authentication** required on every request (`Authorization: Bearer <HS256 token>`)

### 2.2 Runtime One-Command Bring-Up Contract (Mandatory Precondition)

Runtime must provide a **machine-readable capability ledger** and **one-command bring-up contract** that:
- Starts the full distributed stack (nginx + 4 workers + shared WAL) with a single command
- Exposes health gate endpoints and success criteria
- Certifies `substrate_started=true` and `health_gate_pass=true` as observable preconditions
- **If the substrate does not start, the experiment is MEASUREMENT_INVALID with the exact blocking artifact recorded — never a scientific negative.**

### 2.3 Browser Channel (Conditional)

**ONLY IF** Runtime's capability ledger certifies a launchable real Chromium at 1280×720 with CDP `Accessibility.getFullAXTree`:
- Browser-observed DOM and accessibility tree tokens are collected alongside HTTP signals
- Freshness guard validated on both HTTP-layer and browser-observed channels
- If not certified: browser quantities reported `UNKNOWN` with explicit reason

---

## 3. Freshness Guard Specification

### 3.1 Signal Definitions (Frozen)

| Signal | Computation | Threshold |
|--------|-------------|-----------|
| **Jaccard DOM** | `jaccard(cached_required_dom, live_required_dom)` over paths `{"id","name","email"}` | `< 0.85` → stale |
| **Endpoint Template** | `cached_template != live_template` (query_params, header_names) | changed → stale |
| **X-Csrf-Token** | `cached_csrf != live_csrf` | changed → stale |
| **ETag + Cache-Control** | `cached_etag != live_etag AND live_cc == "max-age=0"` | both true → stale |

### 3.2 Composite Decision Rule (Frozen)

```python
spider_stale = (jaccard < 0.85) \
    or param_changed \
    or csrf_changed \
    or (etag_changed and cache_expiry)

spider_status = "UNKNOWN" if spider_stale else "EXECUTABLE"
spider_confidence = 0.85 if spider_stale else 0.95
```

**304 responses:** Always treated as FRESH (`spider_stale=False`, `jaccard=1.0`). This is correct because 304 only occurs when `ETag` matches AND `Cache-Control: max-age=60` AND ground truth is fresh.

### 3.3 Required DOM Fields (Frozen)

```python
REQUIRED_PATHS = {"id", "name", "email"}
```

Only these three field paths contribute to the Jaccard calculation. Optional/noise fields (`phone`, `nickname`, etc.) are excluded.

---

## 4. Workload Design

### 4.1 Drift Families (Staleness Modalities)

| Family | Mechanism | Ground Truth Transition |
|--------|-----------|------------------------|
| **dom_drift** | `id` type flips `int→str`, adds `phone` field | Fresh (req 1–5) → Stale (req 6–10) |
| **param_header_mutation** | Query param `detail→uid`, `X-Csrf-Token` value flips | Fresh (req 1–5) → Stale (req 6–10) |
| **cache_expiry** | Email value changes, `Cache-Control: max-age=60 → max-age=0` | Fresh (req 1–5) → Stale (req 6–10) |

**DRIFT_POINT = 6** (requests 1–5 fresh, 6–10 stale per trajectory)

### 4.2 Noise Families (Benign Variation, Must Stay Fresh)

| Family | Variation |
|--------|-----------|
| **noise_A_phone** | Intermittent `phone` field (30% probability) |
| **noise_B_nickname** | Intermittent `nickname` field (30% probability) |
| **noise_C_null** | Intermittent `email=null` (20%), `phone` (30%) |

All noise families: **always fresh**, all request numbers.

### 4.3 Stable/Control Families (Always Fresh)

| Family | Purpose |
|--------|---------|
| **stable** | Clean baseline trajectories (15 requests each) |
| **fresh_pool** | Auxiliary fresh trajectories for cache building |

### 4.4 Workload Scale (Distributed Primary)

| Component | Trajectories | Requests/Trajectory | Total Requests |
|-----------|--------------|---------------------|----------------|
| Fresh (stable) | 20 | 15 | 300 |
| Fresh (aux) | 2 | 15 | 30 |
| Stale K=1 | 30 (10/family) | 1 (eval at req 6) | 30 |
| Stale K=2 | 10 | 2 (eval at req 6,7) | 20 |
| Stale K=3 | 10 | 3 (eval at req 6,7,8) | 30 |
| Noise | 15 (5/variant) | 10 | 150 |
| **Total (fresh+stale)** | | | **~560** |
| **Stale prevalence** | | | **~15%** (80 stale / 560) |

### 4.5 Controls and Baselines (Embedded in Workload)

- **PC-FRESH-EXECUTION**: `pc1_ids` = 12 fresh trajectories, verify EXECUTABLE + postconditions
- **NC-NOISE-IMMUNITY**: `nc1_ids` = 10 noise trajectories, verify no stale detection
- **B-COLD**: `cold_ids` = 12 cold exploration baselines (full re-discovery cost)
- **B-NO-GUARD**: Always EXECUTABLE (computed from logs, no separate execution)
- **B-JACCARD-ONLY**: Jaccard-only stale decision (computed from logs)
- **B-HEADER-ONLY**: Header-only stale decision (computed from logs)
- **Unrelated/Contamination**: `unrelated_ids` = 20 disjoint IDs, verify no false stale

---

## 5. Metrics (Stable Identifiers for Downstream Transmission)

### 5.1 Primary Metrics (Decision Rule)

| Metric ID | Definition | Target |
|-----------|------------|--------|
| `M-TN-POOLED-WILSON-LOWER` | Wilson lower bound (95%) on pooled true-negative rate (fresh→EXECUTABLE) | > 0.75 (point ≥ 0.85) |
| `M-FALSE-ACCEPT-POOLED-WILSON-UPPER` | Wilson upper bound (95%) on pooled false-accept rate (stale→EXECUTABLE) | ≤ 0.10 |
| `M-UNKNOWN-PRECISION-POOLED` | TP / (TP + FP) on stale: correctly UNKNOWN / all UNKNOWN | ≥ 0.85 |
| `M-ECE-GLOBAL` | Expected Calibration Error (10 bins, confidence vs accuracy) | ≤ 0.15 |
| `M-ECE-GLOBAL-BOOTSTRAP-97.5` | 97.5th percentile of bootstrap ECE distribution (5000 iter) | ≤ 0.18 |
| `M-ECE-PER-CLASS-MAX` | max(ECE_fresh, ECE_stale) | ≤ 0.15 |
| `M-MAX-ABS-RHO` | max |ρ| under 1000 trajectory-grouped shuffles (cost vs outcome) | < 0.20 |

### 5.2 Control Metrics

| Metric ID | Definition | Target |
|-----------|------------|--------|
| `M-PC-FRESH-SUCCESS-RATE` | Fresh execution success rate on PC1 | == 1.0 |
| `M-NC-NOISE-FA-WILSON-UPPER` | Noise family false-accept Wilson upper | ≤ 0.05 |

### 5.3 Per-Family/Per-Class Metrics (Reported, Not Gating)

- `M-TN-PER-FAMILY-K`: TN Wilson lower per (family, blast_radius)
- `M-FA-PER-FAMILY-K`: FA point + Wilson upper per (family, blast_radius)
- `M-ECE-PER-CLASS`: ECE_fresh, ECE_stale separately

### 5.4 Substrate Observations (Logged Before Any Metric)

- `substrate_started`: boolean
- `health_gate_pass`: boolean
- `n_non304`: integer (must be ≥ 800)
- `n_distinct_workers`: integer (must be ≥ 2)
- `health_gate_details`: full JSON of D1–D13 checks

---

## 6. Statistical Methodology

### 6.1 Confidence Intervals

- **Wilson score intervals** (95%, z=1.96) for all binomial proportions (TN, FA, UNKNOWN precision)
- **No Gaussian approximation** — Wilson exact for all decision thresholds

### 6.2 Bootstrap (Trajectory-Grouped, Family-Stratified)

- **5000 iterations**
- Resample trajectories **within each family** (preserves family structure)
- Each bootstrap sample computes all primary metrics
- Report 2.5th and 97.5th percentiles
- **Trajectory IDs are the unit of dependence** — requests within a trajectory are correlated

### 6.3 Permutation Test (Trajectory-Grouped)

- **1000 permutations**
- Shuffle trajectory IDs (not individual requests) between cost and outcome vectors
- Compute max |ρ| (Pearson) between shuffled cost and original outcome
- **max |ρ| < 0.20** required for non-degenerate uncertainty

### 6.4 ECE Computation

- **10 equal-width bins**: [0.0,0.1), [0.1,0.2), ..., [0.9,1.0]
- Confidence values: 0.95 (fresh/EXECUTABLE), 0.85 (stale/UNKNOWN)
- Accuracy per bin: fraction where (status=="EXECUTABLE" & truth=="fresh") OR (status=="UNKNOWN" & truth=="stale")
- ECE = Σ |accuracy_bin - avg_confidence_bin| × (n_bin / n_total)

---

## 7. Validity Gates (Must All Pass for Scientific Validity)

| Gate | Check | Failure Consequence |
|------|-------|---------------------|
| **V1** | `substrate_started == true` | MEASUREMENT_INVALID (exact artifact logged) |
| **V2** | `health_gate_pass == true` | MEASUREMENT_INVALID (exact artifact logged) |
| **V3** | `n_non304 >= 800` | MEASUREMENT_INVALID |
| **V4** | `n_distinct_workers >= 2` | MEASUREMENT_INVALID |
| **V5** | Stale prevalence ≈ 15% (no rebalancing without disclosure) | Validity note, not invalidating |
| **V6** | All costs integer, trajectory-reset, no jitter/proxy | MEASUREMENT_INVALID if violated |
| **V7** | `M-MAX-ABS-RHO < 0.20` | MEASUREMENT_INVALID if violated |
| **V8** | Verification via `_matches()` exact equality | MEASUREMENT_INVALID if violated |
| **V9** | No synthetic fixtures, no default-filled metrics | MEASUREMENT_INVALID if violated |
| **V10** | Browser channel conditional on Runtime certification | `UNKNOWN` with reason if not certified |
| **V11** | 304 responses correctly handled as fresh | MEASUREMENT_INVALID if violated |
| **V12** | Stale ground truth defined by drift_point=6, no label leakage | MEASUREMENT_INVALID if violated |

---

## 8. Decision Rule (Conjunctive — All Must Pass)

The experiment **SUPPORTS** C-FRESHNESS **iff** ALL of D1–D9 pass **AND** substrate/health gates pass.

| Condition | Metric | Threshold |
|-----------|--------|-----------|
| **D1** | `M-TN-POOLED-WILSON-LOWER` | > 0.75 |
| **D2** | `M-FALSE-ACCEPT-POOLED-WILSON-UPPER` | ≤ 0.10 |
| **D3** | `M-UNKNOWN-PRECISION-POOLED` | ≥ 0.85 |
| **D4** | `M-ECE-GLOBAL` | ≤ 0.15 |
| **D5** | `M-ECE-GLOBAL-BOOTSTRAP-97.5` | ≤ 0.18 |
| **D6** | `M-ECE-PER-CLASS-MAX` | ≤ 0.15 |
| **D7** | `M-MAX-ABS-RHO` | < 0.20 |
| **D8** | `M-PC-FRESH-SUCCESS-RATE` | == 1.0 |
| **D9** | `M-NC-NOISE-FA-WILSON-UPPER` | ≤ 0.05 |

**Outcome Mapping:**
- All pass + substrate up → `SUPPORTS`
- Any D1–D9 fail → `FALSIFIES`
- Positive control fail → `MEASUREMENT_INVALID`
- Null control fail → `FALSIFIES`
- Substrate not started → `MEASUREMENT_INVALID`
- Health gate fail → `MEASUREMENT_INVALID`
- Incomplete data → `INCONCLUSIVE`

---

## 9. Baselines (Computed from Same Raw Evidence)

| Baseline | Computation | Expected Behavior |
|----------|-------------|-------------------|
| **B-NO-GUARD** | `spider_stale = False` always | TN=1.0, FA=1.0, UNKNOWN_prec=0.0 |
| **B-JACCARD-ONLY** | `spider_stale = (jaccard < 0.85)` | Good on dom_drift, FA≈1.0 on param_header_mutation & cache_expiry |
| **B-HEADER-ONLY** | `spider_stale = param or csrf or (etag_changed and cache_expiry)` | Good on param_header_mutation & cache_expiry, FA≈1.0 on dom_drift |

**No separate execution** — all baselines derived from the same logged responses to ensure matched comparison.

---

## 10. Representation Loss Disclosure

The following information is **discarded** by the freshness guard representation:

| Discarded | Could Matter? | Mitigation |
|-----------|---------------|------------|
| Field **magnitudes/values** (only types retained) | Yes — semantic drift without type change | Required paths are identifier-like; type change = structural |
| **Nested depth** beyond path | Partially | Path includes nesting (e.g., `user.email`) |
| **Array lengths/order** | Yes — list reordering invisible | Not in required paths for this experiment |
| **ETag truncated to 16 hex** | Collision probability ~2⁻⁶⁴ | Negligible for n<10⁶ |
| **Endpoint template ignores param semantics** | Yes — `detail` vs `uid` same structure | Template drift detected by key change |
| **No timing/latency signals** | Yes — slow responses may indicate stale cache | Deferred to future browser-observed channel |
| **No visual/rendered signals** | Yes — DOM same but CSS/JS changed | Deferred to browser channel |

**This disclosure is mandatory.** The result survives only if the claim is bounded to "HTTP-layer response-derived freshness on this substrate with these signal definitions."

---

## 11. Validity Threats and Mitigations

| Threat | Likelihood | Mitigation |
|--------|------------|------------|
| Substrate fails to start | Medium (historical) | V1/V2 gates: MEASUREMENT_INVALID with artifact, not scientific negative |
| Health gate passes but n_non304 < 800 | Low (certified substrate) | V3 gate: explicit floor, MEASUREMENT_INVALID |
| Stale prevalence far from 15% | Low (fixed workload) | Exact prevalence logged; no rebalancing |
| Trajectory correlation inflates precision | Medium | V7: trajectory-grouped permutations + bootstrap |
| Noise families accidentally trigger stale | Low (validated in prior single-node) | V9 null control gate |
| Browser channel unavailable | High (current state) | V10: conditional, reports UNKNOWN not failure |
| 304 responses misclassified | Low (logic frozen) | V11: explicit 304 handling, health gate verification |

---

## 12. Consequences

### 12.1 Positive Outcome (SUPPORTS)

- **C-FRESHNESS**: HYPOTHESIS → EXPERIMENTAL (distributed HTTP-layer validated)
- **Unblocks**: C-DELTA-REPAIR (repair now has detection), C-SEMANTIC-RESOLVE (abstention calibratable), C-PARAM-INHERIT/C-LLM-INHERIT (safe inheritance), C-PRODUCT-ECON (honest cost)
- **Next gate**: Browser DOM/AX validation (conditional on Runtime), session/auth drift, cross-site holdout

### 12.2 Negative Outcome (FALSIFIES)

- **C-FRESHNESS**: Remains HYPOTHESIS or BLOCKED
- **Graph must**: Redesign signal set (add DOM structural, timing, visual), accept browser channel as mandatory, or pivot approach
- **Downstream**: C-DELTA-REPAIR, C-SEMANTIC-RESOLVE, C-PARAM-INHERIT, C-LLM-INHERIT, C-PRODUCT-ECON remain dependency-gated
- **No promotion** of any freshness-dependent capability to Product Core

### 12.3 MEASUREMENT_INVALID (Substrate/Health Failure)

- **No scientific conclusion** — the experiment could not measure
- **Exact blocking artifact** recorded in `validity_notes` and `unresolved`
- **Prior single-node SURVIVES** (EXP-GRAPH-35949562506) remains the ceiling
- **Retry** with hardened substrate, not a new design

---

## 13. Reproducibility Anchors

- **Code paths** (frozen at freeze.json):
  - `research/graph/delta_repair/flask_app_distributed_36106653880.py` (substrate app, single source of truth via `resource_for()`)
  - `research/graph/delta_repair/nginx_distributed.conf` (nginx sticky config)
  - `src/spider/kernel.py` (verification via `_matches()`)
  - Experiment execution script (to be created at EXECUTE stage)
- **Seeds**: Deterministic trajectory IDs, request numbers, family assignments; bootstrap seed=42, permutation seed=123
- **Environment**: Python 3.12, Flask 3.1.3, PyJWT 2.x, gunicorn 23.0.0, nginx 1.24.0, SQLite 3.x WAL
- **Data**: No external datasets — all responses generated by deterministic `resource_for()` function shared between harness and app

---

## 14. Frozen References

- **Director Mandate**: `request.json.director_mandate.allocation.question`
- **Parent Handoff**: `EXP-GRAPH-36118890504` (SUPERSEDE disposition)
- **Prior Single-Node Freshness**: `EXP-GRAPH-35949562506` (SURVIVES_CURRENT_TEST on stdlib http.server)
- **Certified Substrate**: `EXP-RUNTIME-36100549580`, `EXP-RUNTIME-36094450333` (DISTRIBUTED VALIDATED plain-HTTP)
- **Runtime Dependency**: Capability ledger + one-command bring-up contract (in-flight)

---

## 15. No-Go Rules (Explicitly Forbidden)

1. **No synthetic alias fixtures** — all data from live distributed substrate
2. **No jittered or proxy cost counters** — integer sum-counter only
3. **No prevalence rebalancing without disclosure** — exact prevalence logged
4. **No default-filled metrics** — if a metric cannot be computed, report `null` with reason in `validity_notes`
5. **No browser metrics without Runtime certification** — report `UNKNOWN` explicitly
6. **No substrate-start substitution** — if substrate fails, record exact failure and stop
7. **No post-hoc threshold adjustment** — all thresholds frozen in this preregistration

---

## 16. Artifact Specification

**Raw Evidence (JSONL, one entry per request):**
```
raw_evidence/raw_evidence_distributed.jsonl
```

**Derived Artifacts:**
- `result.json` — canonical machine handoff
- `report.md` — human-readable interpretation
- `provenance.json` — commits, environment, hashes
- `raw_evidence/summary.json` — aggregated counts
- `raw_evidence/health_gate.json` — health gate results
- `raw_evidence/decision.json` — decision rule evaluation

All artifacts written to `research/experiments/EXP-GRAPH-36132150213/`

---

**End of Preregistration.** This document is frozen at `freeze.json` creation. No modifications after freeze.