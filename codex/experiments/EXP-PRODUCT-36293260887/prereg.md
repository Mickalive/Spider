# Preregistration: EXP-PRODUCT-36293260887

## 1. Experiment Identity

- **experiment_id**: EXP-PRODUCT-36293260887
- **lane**: product
- **claim_ids**: C-PARAM-INHERIT, C-RESIDUAL-NOVELTY, C-PRODUCT-ECON
- **request_hash**: 97cc57326645c7f4ff0790f9a4d0fea90e8a8b6ea973b2d98eac78985c8c3452
- **base_sha**: 244dd5bdfe5d34bcf74f4d8472db3caa0922b641
- **director_mandate**: CONTINUE on C-PARAM-INHERIT with cognitive_reset=true

## 2. Strategic Question (from Director Mandate)

> Does a DURABLE, committed, unit-tested parameter-induction capability in the shipped kernel let a mechanism distilled from observations of resource A resolve, bind, execute and verify correctly on never-observed resource B whose identifier value set is disjoint from A, and does that mechanism then reach amortized_cost_ratio at or below 0.85 against B-COLD, B-LITERAL-REPLAY and B-RETRIEVAL-K5 at matched end-to-end success?

## 3. Hypothesis

A corrected parameter-induction pipeline implemented in `src/spider/kernel.py` at HEAD, with tests reaching EXECUTABLE through `distill()`, will produce mechanisms that:
1. Transfer to never-observed resource-B identifiers at success_rate ≥ 0.95 (PC-SAME-RESOURCE)
2. Achieve amortized_cost_ratio ≤ 0.85 against ALL three baselines (B-COLD, B-LITERAL-REPLAY, B-RETRIEVAL-K5) at matched end-to-end success
3. Break even at or before N_MAX derived from measured B-COLD per-task cost (frozen before freeze)

## 4. Falsifier (Pre-declared)

The hypothesis is **FALSIFIED** if ANY of the following conditions hold:

| # | Condition | Threshold |
|---|-----------|-----------|
| F1 | PC-SAME-RESOURCE success_rate | < 0.95 |
| F2 | PC-SAME-RESOURCE bound_path preserves prefix | false (must match `/api/v1/<collection>/<slot>`) |
| F3 | Treatment amortized_cost_ratio vs B-COLD | > 0.85 |
| F4 | Treatment amortized_cost_ratio vs B-LITERAL-REPLAY | > 0.85 |
| F5 | Treatment amortized_cost_ratio vs B-RETRIEVAL-K5 | > 0.85 |
| F6 | Treatment break_even_transfer_tasks | > N_MAX (pre-frozen) |
| F7 | NC-SHUFFLED-INTENT transfer_success | > 0.10 |
| F8 | NC-SHUFFLED-INTENT abstention_precision | < 0.90 |
| F9 | NC-SHUFFLED-INTENT cost_ratio_vs_bcold | < 1.0 |
| F10 | Positive control fails | PC-SAME-RESOURCE fails F1/F2 |
| F11 | Null control fails | NC-SHUFFLED-INTENT fails F7/F8/F9 |
| F12 | Sample size per family | < 50 for ANY arm |
| F13 | Family-stratified bootstrap | Not computed (B=5000) |
| F14 | Negative probes per arm | < 60 executed |
| F15 | Provenance digests | Any placeholder or mismatch |

**Measurement failure** (infrastructure, substrate, code crash) → **MEASUREMENT_INVALID**, not FALSIFIED.

## 5. Kernel Changes Required (Must Be Committed Before Freeze)

The following defects in the committed kernel (132 lines at HEAD 244dd5bd) MUST be fixed and committed with nonempty git diff:

### 5.1 `distill()` Confidence Gate Defect
- **Current**: `distill()` hard-codes `confidence=0.5`
- **Required**: `distill_parameterized()` produces mechanisms with confidence ≥ `min_confidence` (0.8) when induction succeeds
- **Resolution**: Add `distill_parameterized(observations: List[Observation]) -> Mechanism | None` that induces parameter slots and computes calibrated confidence

### 5.2 `resolve()` Exact Intent Equality Defect
- **Current**: `resolve()` requires `m.intent != intent` (exact string match)
- **Required**: Intent namespace mapping between resource-A intents (e.g., `read-item`, `create-item`) and resource-B intents (e.g., `read-product`, `create-product`)
- **Resolution**: Add `intent_namespace_map` to Mechanism or Registry; `resolve()` consults mapping for cross-resource transfer

### 5.3 Missing `_build_action_template` (Path Prefix Preservation)
- **Parent handoff reference**: `src/spider/kernel.py:316-356` — does NOT exist in 132-line file
- **Defect**: Overwrites entire path value with slot placeholder (e.g., `${id}` instead of `/api/v1/items/${id}`)
- **Required**: `_build_action_template(observations) -> dict` that:
  1. Calls `_strip_common_prefix(paths)` to find shared URL prefix
  2. Preserves prefix in action_template: `/api/v1/items/${id}`
  3. Records `parameter_slots = ["id"]`

### 5.4 Dead `_strip_common_prefix` Helper
- **Parent handoff reference**: `src/spider/kernel.py:258` — defined but never called
- **Required**: Call it from `_build_action_template`; or delete if unused (decision recorded)

### 5.5 Missing `align_parameters`
- **Parent handoff reference**: `src/spider/kernel.py:437` — does NOT exist in 132-line file
- **Required**: `align_parameters(observations: List[Observation]) -> dict` that groups observations by intent namespace, computes varying fields, and returns induction context for `distill_parameterized`

### 5.6 Mechanism Field Population
The Mechanism model already carries these fields but they are NEVER populated:
- `parameter_slots: List[str]`
- `freshness: FreshnessPolicy`
- `applicability_guards: dict`
- `verification_rule: str`
- `failure_boundary: str`
- `repair_scope: str`
- **Required**: Populate all fields during `distill_parameterized`

## 6. Test Requirements (Must Pass Before Freeze)

`tests/test_kernel.py` MUST be extended to reach **EXECUTABLE THROUGH `distill()`**:

| Test | Requirement |
|------|-------------|
| T1 | `distill_parameterized()` on resource-A observations → Mechanism with `parameter_slots=["id"]`, `confidence >= 0.8`, `action_template.path == "/api/v1/items/${id}"` |
| T2 | `resolve()` on resource-B context with `params={"id": "B123"}` → `ResolutionStatus.EXECUTABLE`, `bound_action.path == "/api/v1/items/B123"` |
| T3 | `verify()` on observed next_state → `True` |
| T4 | Paraphrased intent (e.g., `read-product` vs `read-item`) resolves via intent_namespace_map |
| T5 | Regression: bound path NEVER regresses to prefix-free `${id}` template |

**Current tests hand-build Mechanism at confidence 0.95 and insert directly — this is NOT sufficient.**

## 7. Substrate (Reused from EXP-PRODUCT-36272385776)

- **Implementation**: `substrate.py` (stdlib `http.server`, sha256 `d3fe358e...` verified)
- **Server-side behavior** (real, not simulated):
  - Multi-step auth: Bearer token issuance → validation
  - Pagination: `?page=N&page_size=K` with Link headers
  - Schema discovery: `GET /api/v1/schema` returns JSON Schema
  - ETag/304 conditional requests
  - Session state: cookie-based, expires
- **Resource-A endpoints**: `/api/v1/items/*`, `/api/v1/collections/*`
- **Resource-B endpoints**: `/api/v1/products/*`, `/api/v1/categories/*` (disjoint identifier value sets)
- **Intent namespace mapping**:
  - `read-item` ↔ `read-product`
  - `create-item` ↔ `create-product`
  - `list-items` ↔ `list-products`
  - `delete-item` ↔ `delete-product`

## 8. Arms and Execution Policy

### 8.1 Treatment Arm (Parameterized Inheritance)
- **Induction**: `distill_parameterized()` on 50 resource-A observations per family (3 families = 150 total)
- **Resolution**: `resolve()` on resource-B with mapped intent + bound params
- **Execution**: HTTP request per resolved action
- **Verification**: `verify()` against actual response state
- **Cost**: Actual HTTP requests executed (counted)

### 8.2 PC-SAME-RESOURCE (Positive Control)
- Same induction as Treatment
- Resolution on resource-A with disjoint identifier values (same endpoint structure)
- Tests prefix preservation and pipeline executability

### 8.3 NC-SHUFFLED-INTENT (Null Control)
- Induction on resource-A observations with **intent labels randomly permuted** (fixed seed)
- Resolution on resource-B
- **Evaluated on transfer_success criterion** (NOT induced-mechanism count):
  - `transfer_success = successful_transfers / attempted_transfers ≤ 0.10`
  - `abstention_precision = true_abstentions / (true_abstentions + false_executions) ≥ 0.90`
  - `cost_ratio_vs_bcold ≥ 1.0`

### 8.4 B-COLD (Executed Cold Baseline) — **MEASURED, NOT CONFIGURED**
- For EACH task: execute multi-step auth + pagination traversal + schema discovery
- Count actual HTTP requests per task
- **Per-task cost measured and recorded**
- N_MAX derived from: `N_MAX = ceil(induction_cost / (mean_bcold_cost - treatment_cost_per_task))`
- **FROZEN BEFORE FREEZE** — N_MAX written to spec.json or freeze.json

### 8.5 B-LITERAL-REPLAY
- Replay resource-A action_template literally on resource-B (no parameter binding)
- Expected to fail on identifier mismatch
- Cost: actual HTTP requests until failure or completion

### 8.6 B-RETRIEVAL-K5
- Embed resource-A observations (intent + state)
- For each resource-B task: retrieve top-5 nearest by cosine similarity
- Execute retrieved action_templates literally
- Cost: actual HTTP requests

## 9. Experimental Design

### 9.1 Families (Stratification)
Three task families with distinct endpoint structures:
1. **Items/Products** — CRUD on collection resources
2. **Collections/Categories** — Hierarchical listing and filtering
3. **Search/Query** — Parameterized search with pagination

Each family: n ≥ 50 tasks per arm (total ≥ 150 per arm)

### 9.2 Resource-B Identifier Sets (Fixed Before Freeze)
- Disjoint from resource-A identifiers
- Fixed sets of 100 identifiers per family per resource
- Seed: 42 (deterministic)

### 9.3 Negative Probes (Abstention/False-Accept)
- 60 probes per arm: out-of-support slot bindings, invalid intents, malformed params
- Measure: `false_accept_rate`, `abstention_precision`, `ece_treatment`

### 9.4 Induction Cost Measurement
- Count actual model/LLM calls if any (currently none — stdlib only)
- Count actual HTTP requests during observation collection
- `induction_cost = total_http_requests_during_observation_collection`

## 10. Metrics (Stable Identifiers for Downstream)

| Metric ID | Definition | Unit |
|-----------|------------|------|
| `pc_same_resource_success_rate` | PC-SAME-RESOURCE successful resolutions / attempted | ratio |
| `pc_same_resource_prefix_preserved` | Bound paths matching `/api/v1/<collection>/<slot>` / attempted | ratio |
| `treatment_success_rate` | Treatment successful executions / attempted on resource-B | ratio |
| `treatment_amortized_cost_ratio_vs_bcold` | (induction_cost + n * treatment_cost_per_task) / (n * bcold_cost_per_task) | ratio |
| `treatment_amortized_cost_ratio_vs_literal_replay` | Same denominator: n * literal_replay_cost_per_task | ratio |
| `treatment_amortized_cost_ratio_vs_retrieval_k5` | Same denominator: n * retrieval_k5_cost_per_task | ratio |
| `treatment_break_even_transfer_tasks` | Smallest n where amortized_cost_ratio ≤ 1.0 | integer |
| `nc_shuffled_transfer_success` | NC-SHUFFLED-INTENT successful transfers / attempted | ratio |
| `nc_shuffled_abstention_precision` | True abstentions / (true abstentions + false executions) | ratio |
| `nc_shuffled_cost_ratio_vs_bcold` | NC cost per task / B-COLD cost per task | ratio |
| `bcold_mean_requests_per_task` | Mean HTTP requests per task (measured) | float |
| `literal_replay_mean_requests_per_task` | Mean HTTP requests per task | float |
| `retrieval_k5_mean_requests_per_task` | Mean HTTP requests per task | float |
| `induction_cost_total` | Total HTTP requests for observation collection | integer |
| `n_max_frozen` | Break-even threshold derived pre-freeze | integer |
| `false_accept_rate` | False executions / negative probes | ratio |
| `abstention_precision` | True abstentions / (true abstentions + false executions) | ratio |
| `ece_treatment` | Expected calibration error (binned) | float |

All ratio metrics: **family-stratified B=5000 bootstrap CIs reported**.

## 11. Decision Rule (Formal)

```
IF (all 9 conditions in spec.json.decision_rule.conditions PASS):
    outcome = "SUPPORTS"
    claim_updates: C-PARAM-INHERIT -> VALIDATED
    promote_to_product = true
ELIF (measurement failure: substrate crash, kernel exception, missing data):
    outcome = "MEASUREMENT_INVALID"
    status = "MEASUREMENT_INVALID"
    claim_updates: none
ELSE:
    outcome = "FALSIFIES"
    claim_updates: C-PARAM-INHERIT -> REJECTED (if mechanism failure) or EXPERIMENTAL (if ambiguous)
    promote_to_product = false
```

**Critical**: The decision rule conditions are evaluated as a CONJUNCTION (all must pass). This avoids the compound-gate pathology where a single non-discriminating threshold voided a decisive mechanism result.

## 12. Validity Threats (Pre-declared)

| Threat | Mitigation |
|--------|------------|
| Intent namespace mapping is hand-authored | Declared as part of mechanism; tested in T4; not learned |
| Substrate is synthetic (stdlib HTTP) | Server-side imposes REAL discovery work; cost dynamic range is measured |
| No browser, no model keys | By design — isolates inheritance mechanism from browser/model variance |
| Single substrate | Substrate validated in parent packet; reuse reduces variance |
| Family stratification may not capture all heterogeneity | Three families chosen to cover distinct endpoint patterns; bootstrap stratified |
| N_MAX depends on B-COLD measurement | B-COLD measured per-task before freeze; N_MAX frozen |
| Null control may not discriminate if induction is fundamentally broken | NC-SHUFFLED-INTENT evaluated on transfer_success, not mechanism count |

## 13. Provenance Requirements

- All artifact digests in `result.json.artifacts` MUST verify (no placeholders)
- `provenance.json.frozen_inputs.freeze.json` digest MUST verify
- Git diff against base_sha MUST be nonempty for `src/` and `tests/`
- Kernel sha256 recorded at freeze
- Substrate sha256 recorded at freeze

## 14. Consequences

### Positive Outcome (SUPPORTS)
- C-PARAM-INHERIT → VALIDATED
- Durable, executable parameter induction in shipped kernel
- C-LLM-INHERIT, C-PRODUCT-ECON, C-CROSSSITE become runnable
- Product promotion gate decidable
- Ends add-at-execute/delete-at-verdict pathology

### Negative Outcome (FALSIFIES with measurement validity)
- C-PARAM-INHERIT → REJECTED (mechanism failure) or stays EXPERIMENTAL (ambiguous)
- Parameter induction not viable on this architecture
- Product lane must pivot architecture or accept no inheritance
- C-RESIDUAL-NOVELTY, C-PRODUCT-ECON remain unmeasurable

### Measurement Invalid
- No claim update
- Experiment must be redesigned with valid substrate/instrumentation
- Does NOT falsify the hypothesis

## 15. Minimal Scope Commitment

This experiment tests **ONE** parameter-induction implementation on **ONE** substrate with **ONE** cost basis (HTTP requests). It does NOT test:
- Cross-model inheritance (C-LLM-INHERIT)
- Real browser interactions
- Cross-site transfer beyond resource-A→resource-B on same substrate
- Freshness, delta repair, semantic resolution
- Model token costs or latency

These remain for future experiments gated on this one's outcome.