# EXP-PRODUCT-36249064252 Preregistration

## 1. Executive Summary

This experiment tests whether a **durable, kernel-integrated** parameter induction capability (`distill_parameterized` in `src/spider/kernel.py`) enables transfer from resource-A to never-observed resource-B with **disjoint identifier value sets**, beating cold exploration, literal replay, and retrieval baselines on success rate and honest per-task cost.

This is the **hinge experiment** for C-PARAM-INHERIT and the entire SPIDER program. The Director's mandate (PIVOT with cognitive_reset=true) identifies that:
- All prior parameter induction existed only as harness substitutes, not in `src/spider/kernel.py`
- The shipped kernel cannot execute anything it learns (`distill` confidence=0.5 < `min_confidence`=0.8)
- No `distill_parameterized` exists in the kernel
- A valid PASS establishes the first real mechanism; a valid FAIL falsifies the core architectural bet

## 2. Substrate Specification

**HTTP Server**: Locally-served Flask (or stdlib `http.server`) with:
- Real ETag/304 conditional GET support
- Session-scoped responses via Bearer token (Authorization header) or cookie
- Two resource families with **disjoint identifier value sets**:
  - Resource A (training): `/items/{id}` where `id` ∈ {`item-1`..`item-100`}
  - Resource B (transfer): `/products/{sku}` where `sku` ∈ {`SKU-A`..`SKU-Z`, `PROD-100`..`PROD-199`}
- State: authentication required (401 without valid token), session state affects response body
- Deterministic responses for given (state, action, identifier) — no RNG in server logic

**No browser, no docker, no LLM key, no external network**. All preconditions recorded as observations with explicit smallest-next-action if unavailable.

## 3. Observations and Induction

### 3.1 Resource-A Training Observations
- Collected by executing real HTTP requests against the server
- Each observation: `Observation(intent, state, action, next_state, success, provenance)`
- Intents: `create-item`, `read-item`, `update-item`, `delete-item`, `list-items` (5 intents × 20 identifiers = 100 observations)
- State includes: `auth_token`, `session_id`, `content_type`
- Action includes: `method`, `path`, `body` (with identifier in path/body)
- Next state includes: `status_code`, `response_body`, `etag`, `headers`
- Success = (2xx status AND expected postcondition match)

### 3.2 Parameter Induction (`distill_parameterized`)
**Implemented in `src/spider/kernel.py`** with unit tests in `tests/test_kernel.py`.

Algorithm (deterministic, no LLM):
1. Group observations by `intent`
2. For each intent group, compute varying fields across observations using structural comparison
3. For each varying field path (e.g., `action.path`, `action.body.id`), induce a parameter slot with structural name (e.g., `id`, `sku`)
4. Build `action_template` with `${slot}` placeholders
5. Set `parameter_slots` = list of induced slot names
6. Set `confidence` = calibrated value ≥ 0.8 (not hardcoded 0.5)
7. Populate `applicability_guards` from common preconditions across group
8. Populate `verification_rule` from common postconditions
9. Return `Mechanism` with all fields populated (not empty dicts)

**Key requirement**: The induction must correctly handle:
- Full-value identifiers (e.g., `https://api.example.com/items/item-42` → template with `${id}` not double-prefix)
- Noise fields (top-level metadata like `timestamp`, `request_id` excluded via field-path allowlist)
- Pattern absence (unrelated observations → 0 slots, not hallucinated slots)

## 4. Transfer Evaluation (Resource-B)

### 4.1 Transfer Tasks
- 3 intent families: `CRUD-item` (create/read/update/delete), `CRUD-product`, `query` (list/filter)
- Per family: 50 transfer tasks on resource-B identifiers **never seen during induction**
- Disjoint value sets verified: no string overlap between `{item-1..item-100}` and `{SKU-A..SKU-Z, PROD-100..PROD-199}`

### 4.2 Arms (Mechanisms Under Test)
| Arm | Mechanism Source | Binding | Expected Behavior |
|-----|-----------------|---------|-------------------|
| **PARAM-INHERIT** (treatment) | `distill_parameterized` on resource-A | Induced slots bound to resource-B identifiers | EXECUTABLE on resource-B |
| **B-COLD** | None (no mechanism) | N/A | UNKNOWN → full discovery cost |
| **B-LITERAL-REPLAY** | `distill` (literal) on resource-A | None (fixed action_template) | EXPLORE (confidence 0.5 < 0.8) or UNKNOWN |
| **B-RETRIEVAL-K5** | Top-5 retrieved resource-A observations | Heuristic slot matching | EXECUTABLE if match confidence ≥ threshold |

### 4.3 Metrics (Per Task, Per Family)
| Metric | Definition | Target (PARAM-INHERIT) |
|--------|------------|------------------------|
| `success_rate` | Fraction of tasks with HTTP 2xx + verified postcondition | ≥ 0.80 |
| `abstention_precision` | TN / (TN + FP) on unlearned intents | ≥ 0.85 |
| `false_accept_rate` | FP / (FP + TN) on unlearned intents | ≤ 0.10 |
| `ECE` | Expected Calibration Error over confidence bins | ≤ 0.15 |
| `amortized_cost_ratio` | (induction_cost + N×transfer_cost)/N ÷ baseline_cost | ≤ 0.85 vs best baseline |
| `binding_accuracy` | Fraction of bound_actions with correct identifier substitution | ≥ 0.95 |
| `http_requests_per_task` | Total HTTP requests (including 304 revalidation) | Measured |
| `bytes_transferred_per_task` | Total response bytes | Measured |
| `wall_clock_ms_per_task` | End-to-end latency | Measured |

**Cost accounting**:
- `induction_cost`: HTTP requests + kernel calls to collect/process resource-A observations
- `transfer_cost`: HTTP requests + kernel resolve/execute/verify per resource-B task
- `baseline_cost`: Same measurement for each baseline arm
- Amortization over N=50 transfer tasks per family

## 5. Controls

### 5.1 Positive Control (PC-SAME-RESOURCE)
- Induce from resource-A, test on **held-out resource-A identifiers** (same resource, disjoint identifier split)
- Expected: `success_rate ≥ 0.95`, `binding_accuracy ≥ 0.95`, `cost_ratio ≤ 0.50` vs B-COLD
- **Pass required**: Validates induction/binding pipeline works when distribution matches

### 5.2 Null Control (NC-SHUFFLED-INTENT)
- Shuffle `intent` labels across resource-A observations before induction
- Test transfer on resource-B
- Expected: `success_rate ≤ 0.10`, `abstention_precision ≥ 0.90`, `cost_ratio ≥ 1.0` vs B-COLD
- **Pass required**: Confirms transfer requires genuine intent structure

## 6. Incumbent Reference Curve (Mandatory)

**Measure and report the shipped kernel's behavior exactly as committed**:
- `distill()` returns `confidence=0.5` (hardcoded)
- `SpiderKernel.__init__` sets `min_confidence=0.8`
- `resolve()` gates on `best.confidence < self.min_confidence` → returns `EXPLORE`
- **Expected result**: 0% EXECUTABLE for any distilled mechanism on any resource
- This quantifies the "vague sense that SPIDER doesn't work" into a citable baseline

## 7. Statistical Rigor

- **Family-stratified bootstrap**: B=5000 resamples per family, stratified by intent family
- **Margin**: Per-family success_rate and cost_ratio with 95% CI
- **Decision**: ALL families must meet thresholds (not just aggregate)
- **Sample size**: n ≥ 50 transfer tasks per family, ≥ 3 families (powered for family-level inference)
- **Seed**: Fixed random seed for task sampling, bootstrap, server state initialization

## 8. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Identifier leakage (A→B overlap) | Disjoint value sets by construction; automated check |
| Server non-determinism | Deterministic Flask server; fixed seed; no RNG in response logic |
| Intent contamination in null | Intent labels permuted across ALL observations, not within family |
| Cost measurement omission | All HTTP requests, kernel calls, bytes, latency logged per task |
| Calibration gaming | ECE computed on held-out calibration set; confidence from induction not hardcoded |
| Harness substitute | Implementation in `src/spider/kernel.py` with `tests/test_kernel.py` unit tests |

## 9. Falsifier (Pre-declared, Binding)

**If on resource-B transfer tasks (n≥50/family, ≥3 families):**
- `success_rate < 0.80` OR
- `abstention_precision < 0.85` OR
- `false_accept_rate > 0.10` OR
- `ECE > 0.15` OR
- `amortized_cost_ratio > 0.85` vs best baseline at matched correctness

**AND positive control passes AND null control passes**

→ **C-PARAM-INHERIT is FALSIFIED-IN-SETTING** as SPIDER's central mechanism. The architecture must change to non-inheriting alternatives.

## 10. Product Consequences

| Outcome | Claim Status | Product Action |
|---------|--------------|----------------|
| PASS (all conditions) | C-PARAM-INHERIT → VALIDATED | Kernel mechanism promotable; enables C-FRESHNESS, C-DELTA-REPAIR, C-RESIDUAL-NOVELTY, C-LLM-INHERIT |
| FAIL (any condition) | C-PARAM-INHERIT → FALSIFIED-IN-SETTING | Pivot to non-inheriting architecture; reallocate to Frontier/Intel |
| MIXED (controls pass, transfer partial) | C-PARAM-INHERIT → EXPERIMENTAL (bounded) | Targeted fixes; re-run with narrowed scope |
| MEASUREMENT_INVALID | C-PARAM-INHERIT unchanged | Fix substrate; re-run |

## 11. Implementation Checklist (for EXECUTE)

- [ ] Implement `distill_parameterized(observations: list[Observation]) -> list[Mechanism]` in `src/spider/kernel.py`
- [ ] Add unit tests in `tests/test_kernel.py` covering: single-param, multi-param, double-prefix, noise filtering, pattern absence
- [ ] Implement Flask test server with ETag/304, session auth, disjoint resource A/B
- [ ] Implement observation collection harness (real HTTP calls)
- [ ] Implement baseline arms (B-COLD, B-LITERAL-REPLAY, B-RETRIEVAL-K5)
- [ ] Implement metrics computation (success, abstention, false-accept, ECE, cost)
- [ ] Implement family-stratified bootstrap (B=5000)
- [ ] Run incumbent reference curve measurement (shipped kernel)
- [ ] Run positive control (PC-SAME-RESOURCE)
- [ ] Run null control (NC-SHUFFLED-INTENT)
- [ ] Run transfer evaluation (PARAM-INHERIT vs baselines on resource-B)
- [ ] Produce `result.json`, `report.md`, `provenance.json` per packet contract

## 12. Deviations from Prior Work

| Prior Defect | This Experiment |
|--------------|-----------------|
| Harness-only induction (EXP-GRAPH-36118890504) | **Kernel-integrated** in `src/spider/kernel.py` |
| No unit tests for induction | **Unit tests in `tests/test_kernel.py`** |
| Hardcoded confidence=0.5 | **Calibrated confidence ≥ 0.8** |
| Double-prefix bug (C2) | **Fixed via field-path allowlist + template construction** |
| Noise field over-parametrization (D1/D2) | **Top-level allowlist {method,url,body,headers,query}** |
| Pattern absence hallucination (E1) | **Two-part structure check (Jaccard≥0.75 + constant-value anchor)** |
| Literal vs param competition | **Parameter-slot-count tie-break committed to HEAD** |
| No incumbent measurement | **Mandatory reference curve on shipped kernel** |
| No declared falsifier | **Pre-declared 5-condition falsifier with thresholds** |
| Synthetic substrate only | **Real HTTP with ETag/304, session auth** |

## 13. Scope Boundaries (Do Not Assume)

- This experiment does **not** test: cross-site transfer (C-CROSSSITE), LLM distillation (C-LLM-INHERIT), freshness guards (C-FRESHNESS), delta repair (C-DELTA-REPAIR), real-browser economics (C-PRODUCT-ECON)
- Substrate is localhost HTTP only — no WAN latency, no browser rendering, no JavaScript execution
- Identifiers are opaque strings — no semantic generalization tested
- Single-server, single-session — no auth rotation, no schema drift, no multi-tenancy
- A valid PASS only establishes parameterized inheritance **in this setting**; broader claims require separate gates

## 14. Dependencies

- **Runtime**: Capability ledger not required (stdlib-only HTTP substrate)
- **Frontier/Intel**: No-memory deterministic executor specification (for B-COLD cost model)
- **Graph**: Not required (semantic resolution not tested)
- **Deferred**: C-LLM-INHERIT, real-agent C-PRODUCT-ECON (blocked on LLM key, BrowserGym, Docker — all verified absent)

---

**Frozen by DESIGN.** No outcome data inspected. This preregistration commits the hypothesis, substrate, metrics, controls, decision rule, and falsifier before EXECUTE begins.