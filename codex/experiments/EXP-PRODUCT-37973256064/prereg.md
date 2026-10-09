# Preregistration: EXP-PRODUCT-37973256064

## 1. Context and Director Mandate

**Global Research Director allocation**: CONTINUE on C-PARAM-INHERIT with `cognitive_reset=true`, `parent_handoff_disposition=SUPERSEDE`.

**Binding strategic question** (from `request.json.director_mandate.allocation.question`):
> On a credential-free substrate that is NOT the synthetic fixture already used for the arm-differentiation certificate (ideally a real localhost or public stdlib-HTTP application with genuinely distinct resource instances and parameterizable identifiers), does the SHIPPED kernel's real distill -> resolve -> execute parameterized round trip (src/spider, the committed kernel repair) produce a measurable, causally attributable treatment-arm behavioral difference versus a matched cold re-derivation arm and a matched retrieval-shaped comparator at equal tooling, with honest unit accounting of model calls, tokens, retrieval, verification and repair, and with a known-negative (out-of-support / wrong-intent / missing-parameter) round trip refused for the right reason with a recorded reason and a null action — thereby establishing that the treatment arm is live and separable outside the synthetic fixture before any four-arm external-LLM benchmark is attempted?

**Rationale** (from Director mandate):
- Parent EXP-PRODUCT-37950607128 established arm differentiation ONLY on synthetic SYNTH-INDUCTION-BANK-v1 fixture
- The four-arm C-LLM-INHERIT benchmark is blocked on a programmatic model credential the factory does not control
- Highest-value next step NOT depending on unavailable credential: show same liveness and causal attribution on a REAL credential-free substrate with honest accounting
- This is a genuine strengthening, not a duplicate of the synthetic certificate

**Critical constraint**: `parent_handoff_disposition=SUPERSEDE` — this experiment MUST NOT silently drift back to the parent handoff's agenda. The parent's `next_question` (four-arm benchmark pending credential) is explicitly NOT this experiment's question. This experiment's question is the Director's binding strategic question above.

## 2. Claim Under Test

**C-PARAM-INHERIT**: "Mechanisms parameterize to unseen identifiers"
- Registry status: EXPERIMENTAL
- Product capability: parameterized inheritance
- Next gate: "learn on resource A, succeed on never-observed B against cold/replay/retrieval baselines"
- This experiment directly targets the registry next_gate on a real credential-free substrate

## 3. Substrate: Real Localhost Stdlib-HTTP Application

### 3.1 Server Implementation
- **Technology**: Python 3.12+ `http.server` (stdlib only — no Flask, no external dependencies)
- **Port**: Dynamic (ephemeral, chosen at runtime)
- **Determinism**: Fixed seed (`SEED=42`), no stochastic elements, no jitter, no cache variance
- **Lifecycle**: Started in-process by test harness, shut down after all arms complete

### 3.2 Resource Model
Three resource types with parameterizable identifiers:

| Resource Type | Path Template | Training Identifiers (A) | Held-Out Identifiers (B) | Out-of-Support (C) |
|--------------|---------------|--------------------------|--------------------------|-------------------|
| items        | `/api/items/${id}` | item-001..item-005 | item-006..item-010 | item-999, item-xyz |
| users        | `/api/users/${id}` | user-001..user-005 | user-006..user-010 | user-999, user-xyz |
| orders       | `/api/orders/${id}` | order-001..order-005 | order-006..order-010 | order-999, order-xyz |

### 3.3 HTTP Semantics
- **GET** `/api/{type}/${id}` → 200 with JSON `{"type": "...", "id": "...", "data": "..."}` if id exists; 404 otherwise
- **POST** `/api/{type}` with body `{"id": "...", ...}` → 201 created
- **PUT** `/api/{type}/${id}` → 200 updated
- **DELETE** `/api/{type}/${id}` → 204 no content
- All responses include `Content-Type: application/json` and `X-Request-Id` (deterministic hash of request)

### 3.4 Parameterizable Action Templates
Each resource type supports a canonical "read" action:
```json
{
  "method": "GET",
  "path": "/api/items/${id}",
  "headers": {"Accept": "application/json"}
}
```
The `${id}` slot is the single parameter. Training observations vary only the `id` value.

### 3.5 Distinction from Synthetic Fixture
- **EXP-PRODUCT-37950607128 fixture**: SYNTH-INDUCTION-BANK-v1 — hardcoded JSON observations, no real HTTP, no server, identifiers like `itm-0009`, `epsilon`, `tok-99`
- **This substrate**: Real HTTP request/response cycles, real parameter binding in URLs, real 200/404 responses, identifiers follow systematic patterns (`item-001`, `user-006`, etc.)

## 4. Arms (Treatment + Two Comparators + Controls)

All arms share:
- Identical task specifications: "Read resource {type} with identifier {id}"
- Identical substrate access: same server, same port, same HTTP client (`urllib.request`)
- Identical tooling budget: max 5 HTTP requests per task, 30 second timeout
- Identical observation format: `Observation(intent, state, action, next_state, success, provenance)`

### 4.1 T-SPIDER-PARAM (Treatment Arm)
**Mechanism**: SpiderKernel with `distill_parameterized` implemented
1. **Training phase**: 5 observations per resource type (A identifiers) → `distill_parameterized` induces 1 parameterized mechanism per type with `parameter_slots=["id"]`, `action_template.path="/api/{type}/${id}"`, `confidence=0.90`
2. **Registry**: 3 mechanisms (items, users, orders) at confidence 0.90
3. **Test phase**: For each held-out B identifier (5 per type × 3 types = 15 tasks):
   - `resolve(intent, context={"resource_type": type}, params={"id": identifier})`
   - Expect `ResolutionStatus.EXECUTABLE` with `bound_action.path="/api/{type}/{identifier}"`
   - Execute HTTP request, verify 200 response matches postconditions
4. **Accounting**: Per-task counters (model_calls=0, model_tokens=0, retrieval_calls=1, verification_calls=1, repair_attempts=0, http_requests=1, latency_ms)

### 4.2 B-COLD-RE-DERIVE (Cold Re-derivation Arm)
**Mechanism**: No inheritance, no registry, no retrieval
1. **Training phase**: None (observations discarded)
2. **Test phase**: For each held-out B identifier (same 15 tasks):
   - Agent receives task spec: "Read {type} {identifier}"
   - Constructs HTTP request from scratch: `GET /api/{type}/{identifier}`
   - Executes, verifies 200 response
3. **Accounting**: Per-task counters (model_calls=0, model_tokens=0, retrieval_calls=0, verification_calls=1, repair_attempts=0, http_requests=1, latency_ms)

### 4.3 B-RETRIEVAL-SHAPED (Retrieval-Shaped Comparator)
**Mechanism**: Structural similarity retrieval over training observations
1. **Training phase**: Store all 15 training observations (5 per type × 3 types)
2. **Test phase**: For each held-out B identifier (same 15 tasks):
   - Compute similarity between test task spec and each training observation:
     - Jaccard on action template keys + state keys
     - Exact match on resource_type in state
   - Retrieve top-K=3 most similar training observations
   - Bind parameters: extract `${id}` slot from retrieved action template, substitute test identifier
   - Execute bound action, verify
3. **Accounting**: Per-task counters (model_calls=0, model_tokens=0, retrieval_calls=3, verification_calls=1, repair_attempts=0, http_requests=1, latency_ms)

### 4.4 PC-EXACT-REPLAY (Positive Control)
- Same as T-SPIDER-PARAM but tested on TRAINING identifiers (A set: 5 per type × 3 types = 15 tasks)
- Expected: 100% success, 100% action reuse (zero novel decisions), EXECUTABLE on all

### 4.5 B-LITERAL-KERNEL (Ablation Control)
- SpiderKernel with ONLY literal `distill()` (confidence 0.5, no `distill_parameterized`, no `parameter_slots`)
- Trained on same A observations → literal mechanisms with confidence 0.5
- Tested on held-out B identifiers
- Expected: `confidence=0.5 < min_confidence=0.8` → `ResolutionStatus.EXPLORE` or `UNKNOWN` on all parameterized tasks (success_rate < 0.20)

### 4.6 NC-OUT-OF-SUPPORT-TYPE (Null Control)
- T-SPIDER-PARAM mechanisms (trained on items/users/orders) tested on NEW resource type "products" (completely unseen, no training observations)
- Expected: `resolve` returns `UNKNOWN` ("no applicable validated mechanism"), `bound_action=null`, reason recorded

## 5. Known-Negative Test Cases (Refusal Detection)

Three categories, 5 test cases each = 15 known-negative tasks:

| Category | Test Case | Expected Refusal Reason |
|----------|-----------|-------------------------|
| Out-of-support identifier | `GET /api/items/item-999` | "identifier not in support" or "precondition failed" |
| Out-of-support identifier | `GET /api/users/user-xyz` | "identifier not in support" |
| Wrong intent | Use "delete" intent with "read" mechanism | "intent mismatch" or "no applicable validated mechanism" |
| Wrong intent | Use "create" intent with "read" mechanism | "intent mismatch" |
| Missing parameter | `resolve(..., params={})` (no `id`) | "required parameter 'id' missing" |
| Missing parameter | `resolve(..., params={"wrong_key": "value"})` | "required parameter 'id' missing" |

**Requirement**: All 15 known-negative cases → `bound_action=null`, non-empty `reason` string, status `UNKNOWN` or `EXPLORE` (not `EXECUTABLE`). Refusal reason must correctly categorize the failure type.

## 6. Metrics

### 6.1 Primary Metrics (Per Arm)
| Metric | Type | Target (Treatment) |
|--------|------|-------------------|
| `success_rate_heldout_B` | Proportion [0,1] | ≥ 0.80 |
| `success_rate_training_A` | Proportion [0,1] | == 1.00 (PC-EXACT-REPLAY) |
| `known_negative_refusal_rate` | Proportion [0,1] | ≥ 0.95 |
| `refusal_reason_correctness` | Proportion [0,1] | == 1.00 |
| `model_calls` | Count per task | == 0 (all arms) |
| `model_tokens` | Count per task | == 0 (all arms) |
| `retrieval_calls` | Count per task | Treatment: 1, Cold: 0, Retrieval: 3 |
| `verification_calls` | Count per task | ≥ 1 (all arms) |
| `repair_attempts` | Count per task | ≥ 0 |
| `http_requests` | Count per task | ≥ 1 |
| `latency_ms` | Continuous | Measured |

### 6.2 Derived Metrics
- `treatment_advantage_vs_cold = success_rate_treatment - success_rate_cold`
- `treatment_advantage_vs_retrieval = success_rate_treatment - success_rate_retrieval`
- `causal_attribution = success_rate_treatment - success_rate_literal_kernel`
- `accounting_honesty = (model_calls == 0) AND (model_tokens == 0) AND (no_injected_counters)`

## 7. Decision Rule (Frozen Before Execution)

**PRIMARY (treatment separation)**:
```
success_rate_treatment >= 0.80
AND treatment_advantage_vs_cold > 0.15
AND treatment_advantage_vs_retrieval > 0.15
```

**KNOWN-NEGATIVE (refusal correctness)**:
```
known_negative_refusal_rate >= 0.95
AND refusal_reason_correctness == 1.00
AND all_refusals_have_bound_action_null == True
```

**ACCOUNTING HONESTY**:
```
model_calls == 0 for all arms
AND model_tokens == 0 for all arms
AND no counter event has injected=True
```

**CAUSAL ATTRIBUTION**:
```
success_rate_literal_kernel < 0.20
AND success_rate_training_A == 1.00 (PC-EXACT-REPLAY)
```

**SUBSTRATE VALIDITY**:
```
server_uses_real_http == True
AND num_resource_types >= 3
AND num_identifiers_per_type >= 10
AND substrate != SYNTH-INDUCTION-BANK-v1
```

**OVERALL OUTCOME**:
- `SUPPORTS`: All five rule groups PASS
- `FALSIFIES`: PRIMARY fails OR KNOWN-NEGATIVE fails
- `MIXED`: PRIMARY passes but KNOWN-NEGATIVE or ACCOUNTING or CAUSAL fails
- `MEASUREMENT_INVALID`: SUBSTRATE_VALIDITY fails OR infrastructure failure (server won't start, port conflict, etc.)

## 8. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Substrate too simple (trivial parameter binding) | Three resource types, systematic identifier patterns, real HTTP 404 on unknown ids |
| Cold arm accidentally benefits from training | Cold arm receives NO training observations; task spec only |
| Retrieval arm inadvertently matches treatment | Retrieval uses structural similarity ONLY; no parameter induction; top-K=3 fixed |
| Counter inflation / injection | Counters incremented ONLY at explicit instrumented call sites; model counters hardcoded to 0 |
| Server non-determinism | Stdlib http.server, no threading, fixed seed, no cache, no jitter |
| Parameter binding bugs in kernel | Unit-tested separately; PC-EXACT-REPLAY validates binding on training set |
| Confounding by resource type difficulty | Balanced design: 5 held-out per type, all arms tested on identical 15 tasks |

## 9. Kernel Implementation Requirement (for EXECUTE)

The current `src/spider/kernel.py` ONLY has literal `distill()`. EXECUTE must implement `distill_parameterized` in the kernel before running. Minimal required signature:

```python
def distill_parameterized(self, observations: list[Observation]) -> Mechanism | None:
    """
    Induce a parameterized mechanism from multiple observations of the same intent.
    - Group observations by intent
    - Find varying fields in action_template (e.g., URL path segments)
    - Create parameter_slots for each varying field
    - Build action_template with ${slot} placeholders
    - Compute confidence from evidence count and consistency
    - Return Mechanism with parameter_slots, confidence >= 0.8
    """
```

The implementation must:
- Be in `src/spider/kernel.py` (the SHIPPED kernel)
- Produce mechanisms compatible with existing `resolve()` and `_bind()`
- Achieve confidence >= 0.8 on 5 consistent training observations
- Handle the three resource types in this experiment

## 10. Artifacts to Produce

| Artifact | Path | Purpose |
|----------|------|---------|
| Raw evidence | `raw_evidence/task_trajectories.jsonl` | Per-task raw observations, resolutions, executions, verifications |
| Raw evidence | `raw_evidence/accounting_counters.jsonl` | Per-task counter events with timestamps |
| Raw evidence | `raw_evidence/server_log.jsonl` | HTTP request/response log |
| Derived | `derived/arm_metrics.json` | Aggregated metrics per arm |
| Derived | `derived/decision_rule_eval.json` | Pass/fail per decision rule clause |
| Code | `src/spider/kernel.py` (modified) | Kernel with distill_parameterized |
| Code | `run_experiment.py` | Experiment harness |
| Report | `report.md` | Interpretation bounded by measurements |

## 11. Reproducibility

- **Seed**: `SEED=42` for server, harness, all randomization
- **Environment**: Python 3.12+, stdlib only (no pip dependencies beyond spider package)
- **Commit**: Kernel modification committed to lab2/product branch before freeze
- **Determinism**: Single-threaded, no async, no external services

---

**This preregistration is frozen upon creation of `freeze.json`. No outcome-bearing measurements may be inspected before freeze. The decision rule above is binding.**