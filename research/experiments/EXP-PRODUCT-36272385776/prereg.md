# EXP-PRODUCT-36272385776 Preregistration

## 1. Executive Summary

This experiment tests whether a **durable, kernel-integrated** parameter induction capability (`distill_parameterized` in `src/spider/kernel.py`) enables economically viable transfer from resource-A to never-observed resource-B with **disjoint identifier value sets** on a substrate that imposes **genuine cold-discovery cost** (multi-step auth, pagination, schema discovery).

This is the **decisive economic measurement** for C-PARAM-INHERIT and the entire SPIDER program. The previous experiment (EXP-PRODUCT-36249064252) established the mechanism capability (success_rate 1.0, binding_accuracy 1.0 on disjoint identifiers) but on a substrate where the cold baseline (B-COLD) cost only 1.0 HTTP request per task — leaving zero dynamic range for amortization. The measured break-even was 253.8 transfer tasks on crud-write and never reached on crud-read or query.

The Director's mandate (CONTINUE with cognitive_reset=true on C-PARAM-INHERIT) identifies that:
- The mechanism capability is **established** but its **economics are unmeasured** on a substrate with real discovery cost
- The treatment arm (`distill_parameterized`) exists in the kernel at commit 664bc124 but was **deleted at the verdict commit** (61eb4fb) because the compound gate failed — the same add-at-execute / delete-at-verdict cycle has occurred **at least 13 times** across product packets
- **Durability** is the blocker: a mechanism that cannot survive the promotion gate is not a product capability
- This cycle must deliver **both** a discriminating economic measurement **and** a durability measurement that cannot be asserted in prose

A valid PASS establishes the first durable, kernel-integrated parameterized inheritance mechanism with measured economic viability on a substrate where cold discovery has real cost. A valid FAIL falsifies the core architectural bet and forces a program-level pivot. The durability co-measurement ensures the mechanism survives to the verdict commit. Either outcome changes the claim status and product direction decisively.

## 2. Substrate Specification

### 2.1 HTTP Server (stdlib `http.server` or Flask — verified by self-test before any arm)

**Required capabilities (all must pass automated pre-flight check before freeze):**
- Multi-step authentication: `POST /auth/login` → returns `Bearer <token>` → subsequent requests require `Authorization: Bearer <token>` header; tokens expire after 100 requests or 5 minutes
- Paginated list endpoints: `GET /api/v1/{collection}?page={n}&page_size=10` returns `{items: [...], next_page: n+1 or null, total: N}`
- Schema discovery required: endpoint paths, HTTP methods, request/response body schemas are NOT documented; must be discovered from observations
- Real ETag/304 conditional GET support on item endpoints
- Session-scoped state: token affects response body (e.g., includes user_id, permissions)
- Deterministic responses for given (state, action, identifier) — no RNG in server logic
- Two resource families with **disjoint identifier value sets**:
  - Resource A (training): `/api/v1/items` where `id` ∈ {`item-1` .. `item-200`}
  - Resource B (transfer): `/api/v1/products` where `sku` ∈ {`SKU-A` .. `SKU-Z`, `PROD-100` .. `PROD-199`}

**No browser, no docker, no LLM key, no external network.** All preconditions recorded as observations with explicit smallest-next-action if unavailable.

### 2.2 Resource A — Training Observations

| Intent Family | Intents | Identifiers | Observations per Intent |
|---------------|---------|-------------|-------------------------|
| CRUD-write    | `create-item`, `update-item`, `delete-item` | 20 each | 20 |
| CRUD-read     | `read-item` | 20 | 20 |
| Query/List    | `list-items`, `filter-items` | 10 each (different filters) | 10 |

Total: **100 successful observations** across 7 intents.
Each observation collected by executing real HTTP requests including full auth handshake, pagination traversal where needed, and schema discovery.

### 2.3 Resource B — Transfer Evaluation

| Intent Family | Intents | Identifiers | Transfer Tasks per Intent |
|---------------|---------|-------------|---------------------------|
| CRUD-write    | `create-product`, `update-product`, `delete-product` | 50 each | 50 |
| CRUD-read     | `read-product` | 50 | 50 |
| Query/List    | `list-products`, `filter-products` | 25 each | 25 |

Total: **150 transfer tasks** on **never-observed** resource-B identifiers (disjoint value sets verified: no string overlap between `{item-1..item-200}` and `{SKU-A..SKU-Z, PROD-100..PROD-199}`).

### 2.4 Cost Structure (Why This Substrate Has Dynamic Range)

| Operation | B-COLD Requests (estimated) | PARAM-INHERIT Transfer Requests |
|-----------|-----------------------------|--------------------------------|
| Auth handshake (login) | 1 per task* | 0 (token in mechanism preconditions) |
| Schema discovery (endpoint enumeration) | 3-5 per task | 0 (template in mechanism) |
| Pagination traversal (list) | 2-10 per task | 0 (direct item access via template) |
| Target operation | 1 per task | 1 per task |
| **Total per task** | **7-17** | **1** |

\* B-COLD re-authenticates per task because it has no mechanism to persist tokens. PARAM-INHERIT mechanisms carry `${auth_token}` slot bound from context.

**Key**: B-COLD cost >> 1 request/task. Induction cost ≈ 100 obs × 15 req/obs = 1500 requests. Transfer cost ≈ 1 req/task. Break-even expected at N ≈ 100-150 tasks (vs 253.8 on previous substrate).

## 3. Observations and Induction

### 3.1 Resource-A Training Observations

- Collected by executing real HTTP requests against the server
- Each observation: `Observation(intent, state, action, next_state, success, provenance)`
- State includes: `auth_token`, `session_id`, `content_type`, `base_url`
- Action includes: `method`, `path`, `body`, `query`, `headers` (with identifier in path/body/query)
- Next state includes: `status_code`, `response_body`, `etag`, `headers`, `pagination_info`
- Success = (2xx status AND expected postcondition match via kernel.verify())

### 3.2 Parameter Induction (`distill_parameterized`)

**Implemented in `src/spider/kernel.py`** with unit tests in `tests/test_kernel.py`. **Must survive to verdict commit.**

Algorithm (deterministic, no LLM):
1. Group observations by `intent`
2. For each intent group, compute varying fields across observations using structural comparison
3. For each varying field path (e.g., `action.path`, `action.body.id`, `action.query.page`, `action.headers.Authorization`), induce a parameter slot with structural name (e.g., `id`, `sku`, `page`, `auth_token`)
4. Build `action_template` with `${slot}` placeholders
5. Set `parameter_slots` = list of induced slot names
6. Set `confidence` = calibrated value ≥ 0.8 (not hardcoded 0.5)
   - Confidence = Beta(2, 1) posterior mean × leave-one-out reconstruction consistency
7. Populate `applicability_guards` from common preconditions across group (e.g., `authenticated: true`, `has_token: true`)
8. Populate `verification_rule` from common postconditions (e.g., `status_code: 2xx`, `has_etag: true`)
9. Populate `freshness` with evidence-scope metadata: `observed_distinct_identifiers`, `observed_sessions`, `schema_version`
10. Set `repair_scope` = `{}` (policy: none — delta repair out of scope for this gate)
11. Return `Mechanism` with all fields populated (not empty dicts)

**Key requirements (validated by unit tests):**
- Full-value identifiers (e.g., `/api/v1/items/item-42` → template with `${id}` not double-prefix)
- Integer and string parameter types (query params, path params, body fields)
- Noise fields (top-level metadata like `timestamp`, `request_id`, `server_id` excluded via field-path allowlist)
- Pattern absence (unrelated observations → 0 slots, not hallucinated slots)
- Credential-safe templates: `${auth_token}` placeholder, no live credentials in durable mechanisms
- Pagination parameters (`page`, `page_size`) induced as slots for list intents

### 3.3 Kernel Integration

`SpiderKernel` gains:
```python
def distill_parameterized(self, observations: list[Observation], register: bool = False) -> list[Mechanism]:
    """Induce parameterized mechanisms from observations. Register if requested."""
```

`align_parameters(observations: list[Observation]) -> list[Mechanism]` — standalone function for testing.

Re-exported from `src/spider/__init__.py`.

## 4. Transfer Evaluation (Resource-B)

### 4.1 Arms (Mechanisms Under Test)

| Arm | Mechanism Source | Binding | Expected Behavior |
|-----|-----------------|---------|-------------------|
| **PARAM-INHERIT** (treatment) | `distill_parameterized` on resource-A | Induced slots bound to resource-B identifiers from context | EXECUTABLE on resource-B |
| **B-COLD** | None (no mechanism) | N/A | UNKNOWN → full discovery cost (auth + schema + pagination) |
| **B-LITERAL-REPLAY** | `distill` (literal) on resource-A | None (fixed action_template) | EXPLORE (confidence 0.5 < 0.8) or UNKNOWN |
| **B-RETRIEVAL-K5** | Top-5 retrieved resource-A observations | Heuristic slot matching | EXECUTABLE if match confidence ≥ threshold |

### 4.2 Metrics (Per Task, Per Family)

| Metric | Definition | Target (PARAM-INHERIT) |
|--------|------------|------------------------|
| `success_rate` | Fraction of tasks with HTTP 2xx + verified postcondition | ≥ 0.80 |
| `abstention_precision` | TN / (TN + FP) on unlearned/out-of-support intents | ≥ 0.85 |
| `false_accept_rate` | FP / (FP + TN) on unlearned/out-of-support intents | ≤ 0.10 |
| `ECE` | Expected Calibration Error over confidence bins | ≤ 0.15 |
| `amortized_cost_ratio` | (induction_cost + N×transfer_cost)/N ÷ baseline_cost | ≤ 0.85 vs best baseline |
| `break_even_transfer_tasks` | Smallest N where cumulative treatment ≤ cumulative baseline | ≤ N_MAX (preregistered) |
| `binding_accuracy` | Fraction of bound_actions with correct identifier substitution | ≥ 0.95 |
| `http_requests_per_task` | Total HTTP requests (auth, pagination, target, 304) | Measured |
| `bytes_transferred_per_task` | Total response bytes | Measured |
| `wall_clock_ms_per_task` | End-to-end latency | Measured |

**Cost accounting (measured, not assumed):**
- `induction_cost`: All HTTP requests + kernel calls to collect/process 100 resource-A observations
- `transfer_cost`: HTTP requests + kernel resolve/execute/verify per resource-B task
- `baseline_cost`: Same measurement for each baseline arm (B-COLD, B-LITERAL-REPLAY, B-RETRIEVAL-K5)
- Amortization computed at each N = 10, 25, 50, 100, 150, 200, 250, 300 transfer tasks

### 4.3 Out-of-Support Abstention Probes (Critical for False-Accept Measurement)

**60 negative probes per arm** (20 per intent family):
- 20 unlearned-intent probes: intents never in training (e.g., `archive-product`, `export-product`, `bulk-delete`)
- 20 out-of-support slot probes: valid intents but slot values outside observed range (e.g., `sku: "SKU-AA"`, `sku: "PROD-999"`, `page: 999`)
- 20 prefix-collision probes: identifiers sharing prefix with training but semantically different (e.g., `item-999` vs `item-1..200`)

All probes must resolve to UNKNOWN or EXPLORE. FP = EXECUTABLE on any probe.

## 5. Controls

### 5.1 Positive Control (PC-SAME-RESOURCE)
- Induce from resource-A, test on **held-out resource-A identifiers** (same resource, same schema, disjoint identifier split: 20 held-out ids)
- Expected: `success_rate ≥ 0.95`, `binding_accuracy ≥ 0.95`, `cost_ratio ≤ 0.50` vs B-COLD, `break_even ≤ 10`
- **Pass required**: Validates induction/binding pipeline works when distribution and schema match

### 5.2 Null Control (NC-SHUFFLED-INTENT)
- Shuffle `intent` labels across ALL resource-A observations before induction (not within family)
- Test transfer on resource-B
- Expected: `success_rate ≤ 0.10`, `abstention_precision ≥ 0.90`, `cost_ratio ≥ 1.0` vs B-COLD
- **Pass required**: Confirms transfer requires genuine intent structure, not spurious pattern matching

## 6. Incumbent Reference Curve (Mandatory)

**Measure and report the shipped kernel's behavior exactly as committed at freeze:**
- `distill()` returns `confidence=0.5` (hardcoded)
- `SpiderKernel.__init__` sets `min_confidence=0.8`
- `resolve()` gates on `best.confidence < self.min_confidence` → returns `EXPLORE`
- **Expected result**: 0% EXECUTABLE for any distilled mechanism on any resource
- This quantifies the "kernel cannot execute what it learns" defect into a citable baseline

## 7. Threshold Derivation (Frozen Before Arms Run)

All economic thresholds derived from **measured B-COLD baseline cost** on this substrate:

1. Run B-COLD on 50 sample transfer tasks (stratified across families) **BEFORE FREEZE**
2. Compute `baseline_cost_per_task` = mean(total HTTP requests per task) for B-COLD
3. Compute `induction_cost` = total HTTP requests for 100 resource-A observations
4. Derive `amortized_cost_ratio` threshold: **0.85** (fixed, not derived)
5. Derive `N_MAX` (max break-even): `ceil(induction_cost / (baseline_cost_per_task - treatment_transfer_cost_per_task))`
   - Where `treatment_transfer_cost_per_task` = measured PARAM-INHERIT cost on 10 pilot transfer tasks
   - **N_MAX frozen before main arms run**
6. All thresholds recorded in `freeze.json` and `artifacts/derived/thresholds.json`

**This prevents the previous failure mode where thresholds were assumed constants (0.85, 0.50) on a substrate where B-COLD=1.0 made them unreachable for ANY system.**

## 8. Statistical Rigor

- **Family-stratified bootstrap**: B=5000 resamples per family, stratified by intent family
- **Margin**: Per-family success_rate, cost_ratio, break_even with 95% CI
- **Decision**: ALL families must meet thresholds (not just aggregate)
- **Sample size**: n ≥ 50 transfer tasks per family, ≥ 3 families (powered for family-level inference)
- **Seed**: Fixed random seed for task sampling, bootstrap, server state initialization (recorded in provenance)

## 9. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Identifier leakage (A→B overlap) | Disjoint value sets by construction; automated check in provenance |
| Server non-determinism | Deterministic server; fixed seed; no RNG in response logic |
| Intent contamination in null | Intent labels permuted across ALL observations, not within family |
| Cost measurement omission | All HTTP requests, kernel calls, bytes, latency logged per task per arm |
| Calibration gaming | ECE computed on held-out calibration set; confidence from induction not hardcoded |
| Harness substitute | Implementation in `src/spider/kernel.py` with `tests/test_kernel.py` unit tests |
| Durability theater | Durability measured at verdict commit via git diff; promotion rule pre-declared |
| Threshold assumption | Thresholds derived from MEASURED B-COLD baseline before freeze |
| Single-substrate claim | Scope bounded: valid PASS only establishes economics IN THIS SETTING |

## 10. Falsifier (Pre-declared, Binding)

**Primary Falsifier (Economic + Mechanism):**
If on resource-B transfer tasks (n≥50/family, ≥3 families):
- `success_rate < 0.80` OR
- `abstention_precision < 0.85` OR
- `false_accept_rate > 0.10` OR
- `ECE > 0.15` OR
- `amortized_cost_ratio > 0.85` vs best baseline at matched correctness OR
- `break_even_transfer_tasks > N_MAX`

AND positive control passes AND null control passes
→ **C-PARAM-INHERIT is FALSIFIED-IN-SETTING** as SPIDER's central mechanism. The architecture must change to non-inheriting alternatives.

**Durability Falsifier (Independent, Co-equal):**
If at the verdict-creating commit:
- `distill_parameterized` function is absent from `src/spider/kernel.py` OR
- `SpiderKernel.distill_parameterized` method is absent OR
- `align_parameters` function is absent OR
- Corresponding unit tests are absent from `tests/test_kernel.py` OR
- The promotion rule was not pre-declared before arms ran OR
- The promotion rule was not satisfied
→ **Packet fails regardless of transfer outcomes**. The mechanism is not durable.

## 11. Durability Measurement (Co-equal First-Class Measurement)

**Measured at verdict commit (not at execute commit):**
1. `git diff <freeze_base_commit> <verdict_commit> -- src/spider/kernel.py tests/test_kernel.py`
2. Verify all three kernel symbols present: `distill_parameterized`, `SpiderKernel.distill_parameterized`, `align_parameters`
3. Verify unit tests present and passing (20+ tests covering: single-param, multi-param, integer params, noise filtering, pattern absence, credential-safe templates, pagination params)
4. Verify promotion rule pre-declared in `spec.json` / `prereg.md` and satisfied:
   - Rule: "If PASS (all 9 conditions), then promote_to_product=true and C-PARAM-INHERIT→VALIDATED. If FAIL/MIXED/MEASUREMENT_INVALID, promote_to_product=false."
   - Rule evaluated by Director at verdict; no post-hoc changes

**This directly addresses the 13-cycle add-at-execute / delete-at-verdict pathology.**

## 12. Product Consequences

| Outcome | Claim Status | Product Action |
|---------|--------------|----------------|
| PASS (all 9 conditions) | C-PARAM-INHERIT → VALIDATED | Kernel mechanism promotable; promotion authorized; enables C-FRESHNESS, C-DELTA-REPAIR, C-RESIDUAL-NOVELTY, C-LLM-INHERIT |
| FAIL (any mechanism/economic condition) | C-PARAM-INHERIT → FALSIFIED-IN-SETTING | Pivot to non-inheriting architecture; reallocate to Frontier/Intel |
| FAIL (durability condition only) | C-PARAM-INHERIT → BLOCKED | Mechanism works but cannot be made durable; fix promotion pipeline; re-run |
| MIXED (controls + durability pass, transfer partial) | C-PARAM-INHERIT → EXPERIMENTAL (bounded) | Targeted fixes; re-run with narrowed scope |
| MEASUREMENT_INVALID | C-PARAM-INHERIT unchanged | Fix substrate; re-run |

## 13. Implementation Checklist (for EXECUTE)

- [ ] Implement `distill_parameterized(observations: list[Observation], register: bool=False) -> list[Mechanism]` in `src/spider/kernel.py`
- [ ] Implement `align_parameters(observations: list[Observation]) -> list[Mechanism]` in `src/spider/kernel.py`
- [ ] Add unit tests in `tests/test_kernel.py` covering: single-param, multi-param, integer query params, double-prefix, noise filtering, pattern absence, credential-safe templates, pagination params
- [ ] Implement HTTP test server with: multi-step auth, pagination, schema discovery, ETag/304, session state, disjoint resource A/B
- [ ] Implement observation collection harness (real HTTP calls with full cost accounting)
- [ ] Implement baseline arms (B-COLD, B-LITERAL-REPLAY, B-RETRIEVAL-K5)
- [ ] Implement metrics computation (success, abstention, false-accept, ECE, cost, break-even)
- [ ] Implement family-stratified bootstrap (B=5000)
- [ ] **PRE-FREEZE**: Run B-COLD pilot (50 tasks) to measure baseline cost and derive N_MAX
- [ ] **PRE-FREEZE**: Run PARAM-INHERIT pilot (10 tasks) to measure treatment transfer cost
- [ ] **FREEZE**: Record all thresholds in freeze.json
- [ ] Run incumbent reference curve measurement (shipped kernel)
- [ ] Run positive control (PC-SAME-RESOURCE)
- [ ] Run null control (NC-SHUFFLED-INTENT)
- [ ] Run transfer evaluation (PARAM-INHERIT vs baselines on resource-B)
- [ ] Run out-of-support abstention probes (60 per arm)
- [ ] Produce `result.json`, `report.md`, `provenance.json` per packet contract
- [ ] At verdict: measure durability (git diff, symbol presence, test presence, promotion rule)

## 14. Deviations from Prior Work (EXP-PRODUCT-36249064252)

| Prior Defect | This Experiment |
|--------------|-----------------|
| Substrate: B-COLD = 1.0 req/task (no dynamic range) | **Substrate: B-COLD >> 1 req/task (auth + pagination + schema discovery)** |
| Thresholds: assumed constants (0.85, 0.50) | **Thresholds: derived from MEASURED baseline before freeze** |
| Break-even: measured post-hoc (253.8) | **N_MAX: preregistered and frozen before arms** |
| Durability: asserted in prose, not measured | **Durability: co-equal measurement at verdict commit via git diff** |
| Promotion rule: decided after numbers seen | **Promotion rule: pre-declared in spec/prereg before freeze** |
| Out-of-support abstention: untested (only prefix-collision) | **Out-of-support: explicit slot-value probes (SKU-AA, PROD-999, page=999)** |
| 100 resource-A observations | **200 resource-A observations (better induction coverage)** |
| 5 intents × 20 ids | **7 intents, varied counts (better family coverage)** |
| Flask server (not actually present) | **stdlib http.server verified by self-test (no Flask dependency)** |

## 15. Scope Boundaries (Do Not Assume)

- This experiment does **not** test: cross-site transfer (C-CROSSSITE), LLM distillation (C-LLM-INHERIT), freshness guards (C-FRESHNESS), delta repair (C-DELTA-REPAIR), real-browser economics (C-PRODUCT-ECON)
- Substrate is localhost HTTP only — no WAN latency, no browser rendering, no JavaScript execution
- Identifiers are opaque strings — no semantic generalization tested
- Single-server, single-session — no auth rotation, no schema drift, no multi-tenancy (though token expiry is modeled)
- A valid PASS only establishes parameterized inheritance **in this setting**; broader claims require separate gates
- The mechanism's `repair_scope` is `{}` (policy: none) — delta repair explicitly out of scope

## 16. Dependencies

- **Runtime**: Capability ledger not required (stdlib-only HTTP substrate)
- **Frontier/Intel**: No-memory deterministic executor specification (for B-COLD cost model verification)
- **Graph**: Not required (semantic resolution not tested)
- **Deferred**: C-LLM-INHERIT, real-agent C-PRODUCT-ECON (blocked on LLM key, BrowserGym, Docker — all verified absent)
- **Durability**: Requires that the product-promote workflow (scripts/check_scope.py) does not revert kernel changes for a PASS verdict

## 17. Precedent and Inherited State (from Parent Handoff EXP-PRODUCT-36249064252)

**Established (carried forward):**
- Durable, committed, unit-tested parameter-induction capability design exists (was at commit 664bc124, sha256 ac1cbdd9...)
- Mechanism success 1.0, binding accuracy 1.0 on disjoint identifiers
- Abstention precision 1.0, false_accept_rate 0.0 on negative probes (unlearned-intent + prefix-collision)
- B-LITERAL-REPLAY and B-RETRIEVAL-K5 both mechanism_success_rate 0.0
- NC-SHUFFLED-INTENT transfers at 0.0 with abstention 1.0
- Incumbent reference curve matches expectation (0% EXECUTABLE)
- Three product defects found: string-only slots, credential persistence in literal path, volatile session metadata

**Rejected (carried forward):**
- Literal replay does not transfer to disjoint identifiers (B-LITERAL-REPLAY-FORCED: binding_accuracy 0.0)
- Retrieval with heuristic slots does not transfer (B-RETRIEVAL-K5-SLOT: 0.0)
- The compound FALSIFIES label from previous packet is real but its causal content (architecture must change) is NOT identified — the failing thresholds had zero dynamic range
- D6 positive-control cost criterion was non-discriminating (B-COLD also 1.0 req/task)

**Unknown (carried forward — THIS EXPERIMENT ADDRESSES):**
- Whether parameterized inheritance is economically viable (D5 failure: intrinsic or substrate artifact?)
- Whether thresholds can be discriminating with derived baseline cost
- Whether mechanism abstains on out-of-support slot bindings (previously untested)
- Whether machinery spans schemas with different field names, nested bodies, multi-step flows
- Freshness, staleness, repair (still out of scope)

**Do Not Assume (carried forward):**
- Do not assume C-PARAM-INHERIT is validated or promoted (status: EXPERIMENTAL, bounded)
- Do not assume the prereg's architecture-pivot conclusion in either direction
- Do not read 1.0 HTTP request/task as product economics
- Do not treat collection-slot transfer as interpolation (products was out-of-support extrapolation)
- Do not assume durable templates are credential-safe in general (literal path still persists bearer token)
- Do not treat harness-level cold exploration as product capability

---

**Frozen by DESIGN.** No outcome data inspected. This preregistration commits the hypothesis, substrate, metrics, controls, decision rule, threshold derivation procedure, falsifiers (both), durability measurement, and promotion rule before EXECUTE begins.