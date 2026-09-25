# EXP-GRAPH-36118890504 Report — Parameterized Mechanism Transfer Across Disjoint Identifier Spaces

**Lane:** graph | **Claim:** C-PARAM-INHERIT | **Status:** COMPLETE | **Outcome:** FALSIFIES | **Date:** 2026-09-25 | **Run:** 36118890504

---

## 1. Summary

This experiment tested whether a parameterized mechanism induced from resource A observations can transfer to never-observed resource B with disjoint identifier value sets, outperforming cold exploration, literal replay, and retrieval baselines on success rate and honest per-task cost, with false accept rate ≤ 10% on unrelated resource C.

**Result: FALSIFIES.** The parameterized mechanism achieved **0% success rate** on resource B (ids 6–10), while cold exploration achieved **100% success rate**. The mechanism failed to transfer because its induced preconditions and action template are bound to resource A's specific endpoint (`/posts/{id}`) and resource identifier (`resource: "posts"`), preventing resolution on resource B (`/users/{id}`, `resource: "users"`).

**Key finding:** The current parameterized induction (harness-level, since `distill_parameterized` is not in the kernel) captures resource-specific preconditions and base paths, not just the varying identifier. This prevents cross-resource transfer even when action structure is isomorphic.

---

## 2. Experimental Design (Frozen)

### 2.1 Resources (Isomorphic Action Templates)
| Resource | Base Path | Method | Parameter Slot | Response Schema | ID Space |
|----------|-----------|--------|----------------|-----------------|----------|
| **A (Train)** | `/posts` | GET | `id` | `{id, userId, title, body}` | 1,2,3,4,5 |
| **B (Test)** | `/users` | GET | `id` | `{id, name, username, email}` | 6,7,8,9,10 |
| **C (Null)** | `/comments` | POST | `postId, body` | `{id, postId, name, email, body}` | 11,12,13,14,15 |

- **Isomorphic A↔B**: Same HTTP method (GET), single path parameter `{id}`, JSON response with `id` field
- **Disjoint IDs**: A uses 1–5, B uses 6–10, C uses 11–15 (no overlap)
- **Non-isomorphic C**: Different method (POST), two parameters, different schema → null control

### 2.2 Substrate
- **Validated pattern**: Single-node Flask 3.1.3 + PyJWT 2.13.0 HS256 (per Runtime EXP-RUNTIME-33902315583)
- **Endpoints**: Localhost, deterministic responses, 50–150ms uniform jitter
- **Authentication**: Bearer token required (HS256)

### 2.3 Mechanism Induction (Train Phase — Resource A Only)
1. Observe 5 successful trajectories on resource A (ids 1..5)
2. Induce parameterized mechanism via harness-level `distill_parameterized`:
   - Detect varying `id` in URL path → parameter slot `id`
   - Fixed template: `GET /posts/${id}`
   - Preconditions: `{auth: valid_token, resource: "posts"}`
   - Postconditions: `{status: 200}`
   - Confidence: 0.95
3. Register mechanism in registry

### 2.4 Test Phase — Resource B (Never-Observed, Disjoint IDs)
For each test ID in {6,7,8,9,10}:
1. Context: `{auth: valid_token, resource: "users"}`
2. Params: `{id: test_id}`
3. Resolve via kernel
4. Execute if EXECUTABLE
5. Verify against postconditions

### 2.5 Baselines (Same Test IDs on Resource B)
| Baseline | Registry Content | Resolution Strategy |
|----------|------------------|---------------------|
| **B-COLD** | Empty | Try `/users/{id}` directly |
| **B-LITERAL-REPLAY** | Literal mechanisms from A | Exact replay of `/posts/1` etc. |
| **B-RETRIEVAL-KNN** | Raw observations from A | Naive string replace `/posts/`→`/users/` |

### 2.6 Controls
- **PC-A-SEEN**: Param mechanism on resource A seen IDs (1..5) → expected 100% success
- **NC-UNRELATED-RESOURCE**: Param mechanism on resource C → expected 0% false accepts

---

## 3. Results

### 3.1 Raw Observations

| Phase | Resource | IDs | Mechanism | Success Rate | Cost (req/task) |
|-------|----------|-----|-----------|--------------|-----------------|
| Train | A | 1–5 | — | 5/5 (100%) | 1.0 |
| Test | B | 6–10 | Parameterized | **0/5 (0%)** | 0.0 |
| Test | B | 6–10 | Cold | **5/5 (100%)** | 1.0 |
| Test | B | 6–10 | Literal Replay | 0/5 (0%) | 0.0 |
| Test | B | 6–10 | KNN Retrieval | 0/5 (0%) | 1.0 |
| Null | C | 11–15 | Parameterized | 0/5 (0% false accept) | 0.0 |
| Pos Control | A | 1–5 | Parameterized | 5/5 (100%) | 1.0 |

### 3.2 Metrics (Stable Identifiers)

| Metric ID | Value | Unit |
|-----------|-------|------|
| `success_rate_B_param` | 0.00 | [0,1] |
| `success_rate_B_cold` | 1.00 | [0,1] |
| `success_rate_B_literal` | 0.00 | [0,1] |
| `success_rate_B_knn` | 0.00 | [0,1] |
| `cost_per_task_B_param` | 0.00 | count |
| `cost_per_task_B_cold` | 1.00 | count |
| `cost_per_task_B_literal` | 0.00 | count |
| `cost_per_task_B_knn` | 1.00 | count |
| `false_accept_rate_C_param` | 0.00 | [0,1] |
| `success_rate_A_param_seen` | 1.00 | [0,1] |

### 3.3 Decision Rule Evaluation (Conjunctive)

| Condition | Metric | Threshold | Result |
|-----------|--------|-----------|--------|
| **D1_SUCCESS_B** | `success_rate_B_param` | > max(baselines) + 0.10 | **FAIL** (0.00 > 1.00 + 0.10) |
| **D2_COST_B** | `cost_per_task_B_param` | < min(baselines) × 0.80 | **FAIL** (0.00 < 0.00 × 0.80) |
| **D3_FALSE_ACCEPT** | `false_accept_rate_C_param` | ≤ 0.10 | **PASS** (0.00 ≤ 0.10) |
| **D4_POSITIVE_CONTROL** | `success_rate_A_param_seen` | == 1.0 | **PASS** (1.00 == 1.0) |
| **D5_NULL_CONTROL** | `false_accept_rate_C_param` | == 0.0 | **PASS** (0.00 == 0.0) |

**Outcome mapping:** Any FAIL → `FALSIFIES` (D1 and D2 fail)

---

## 4. Controls

### PC-A-SEEN (Positive Control) — **PASS**
- **Expected:** Success rate = 1.0, cost = 1, false accepts = 0
- **Observed:** Success rate = 1.00, cost = 1.00, false accepts = 0
- The parameterized mechanism works perfectly on resource A seen identifiers.

### NC-UNRELATED-RESOURCE (Null Control) — **PASS**
- **Expected:** Resolution = UNKNOWN/EXPLORE, false accept rate = 0.0
- **Observed:** All 5 resolutions = UNKNOWN, false accept rate = 0.00
- The mechanism correctly rejects resource C (different method, params, schema).

---

## 5. Validity Assessment

### 5.1 Measurement Validity Gates (All Checked)

| Gate | Check | Result |
|------|-------|--------|
| **V1_SUBSTRATE** | Flask/JWT substrate per Runtime pattern | Checked (not independently re-validated) |
| **V2_DISJOINT_IDS** | Train {1..5} ∩ Test {6..10} = ∅ | **PASS** |
| **V3_ISOMORPHIC_ACTION** | A/B both GET, single `{id}`, JSON with `id` | **PASS** |
| **V4_HONEST_COST** | All HTTP requests counted | **PASS** |
| **V5_NO_LEAKAGE** | Induction sees only resource A | **PASS** |
| **V6_DETERMINISTIC_EXECUTION** | Same (resource, id) → identical response | **PASS** |
| **V7_VERIFICATION_REAL** | `verify()` checks actual HTTP response | **PASS** |

### 5.2 Design Discrepancy (Not a Measurement Failure)
- **KERNEL_DISTILL_PARAMETERIZED**: `SpiderKernel` has `distill_parameterized = False`
- Frozen spec section 14 claims "No new code required — uses existing kernel/registry" but kernel lacks `distill_parameterized`
- Harness-level induction used per prereg section 5.3
- **This is a design documentation error, not a measurement validity failure for the transfer hypothesis.** The induction logic used is exactly as specified in the prereg (detect varying `id` → parameter slot `id`).

### 5.3 Representation Loss & Validity Threats
1. **Single-node substrate only** — distributed transfer not tested
2. **No LLM-driven distillation** — "learn on A" half of C-PARAM-INHERIT untested
3. **Only 5 IDs per resource** — limited statistical power
4. **Preconditions include resource name** — induction captures `resource: "posts"` which blocks cross-resource resolution (this is the mechanistic finding, not a threat)

---

## 6. Interpretation

### 6.1 Why the Parameterized Mechanism Failed to Transfer

The induced mechanism has:
- **Preconditions:** `{"auth": "valid_token", "resource": "posts"}`
- **Action template:** `{"method": "GET", "url": "/posts/${id}"}`

When resolving for resource B with context `{"auth": "valid_token", "resource": "users"}`:
1. Precondition check fails: `resource: "posts"` ≠ `resource: "users"`
2. Kernel returns `ResolutionStatus.UNKNOWN` (no applicable mechanism)
3. Zero HTTP requests made, zero cost, zero success

**The mechanism binds to the resource identifier in preconditions and the base path in the action template.** It parameterizes only the `id` value, not the resource path or resource precondition.

### 6.2 Baseline Behavior
- **Cold (100% success):** Tries `/users/{id}` directly — knows the correct endpoint for each test ID
- **Literal Replay (0% success):** Replays exact `/posts/1` etc. — wrong base path for resource B
- **KNN Retrieval (0% success):** Naive string replace `/posts/`→`/users/` on `/posts/1` gives `/users/1` — wrong ID for test IDs 6–10

### 6.3 What This Means for C-PARAM-INHERIT

The hypothesis assumed that parameterizing the varying identifier (`id`) would enable transfer across isomorphic resources. However, the induction process also captures:
1. **Resource-specific preconditions** (the `resource` field in state)
2. **Resource-specific base paths** (`/posts/` vs `/users/`)

For true cross-resource transfer, the mechanism would need to either:
- **Abstract the resource identifier** (parameterize the base path: `/${resource}/${id}`)
- **Generalize preconditions** (drop or parameterize the `resource` field)
- **Use semantic matching** rather than exact precondition matching

The current single-parameter induction (varying value in URL path only) is insufficient for cross-resource transfer when resources differ in their base path and precondition identifiers.

---

## 7. Consequences for C-PARAM-INHERIT

### Negative Outcome (FALSIFIES)
- **C-PARAM-INHERIT remains at synthetic POC ceiling (EXPERIMENTAL or BLOCKED)**
- Parameterized transfer across disjoint ID spaces **fails** on validated HTTP substrate
- The mechanism induction/binding logic is fundamentally limited to same-resource parameterization
- **Product must NOT promote parameterized mechanisms** for cross-resource transfer
- **Graph must either:**
  1. Fix induction/binding to support resource abstraction (parameterize base path, generalize preconditions), OR
  2. Pivot to alternative transfer mechanism (e.g., semantic resolution, fragment reuse)

### Comparison to Prior Work
- **EXP-PRODUCT-33528829801** (10/10 single-param): Tested same-resource unseen IDs only, not cross-resource
- **EXP-PRODUCT-33741671686** (21/21 harness multi-param): Same-resource, not kernel-integrated
- **EXP-GRAPH-34170139507**: HTTP execution with param mechanism on same resource only
- **This experiment**: First test of **cross-resource** (A→B) transfer with disjoint IDs — **falsifies** the transfer hypothesis at this scope

---

## 8. Artifacts & Reproducibility

| Artifact | Path | Role |
|----------|------|------|
| Substrate app | `research/experiments/EXP-GRAPH-36118890504/substrate_app.py` | code |
| Experiment runner | `research/experiments/EXP-GRAPH-36118890504/run_experiment.py` | code |
| Raw results | `research/experiments/EXP-GRAPH-36118890504/raw_results.json` | raw |
| Registry | `research/experiments/EXP-GRAPH-36118890504/registry.jsonl` | derived |
| Result packet | `research/experiments/EXP-GRAPH-36118890504/result.json` | canonical |
| Provenance | `research/experiments/EXP-GRAPH-36118890504/provenance.json` | canonical |

**Kernel SHA256:** `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61` (HEAD `d14f4f87`, base `9db3353d`)

**Substrate:** Flask 3.1.3 + PyJWT 2.13.0 HS256, port 18928, 50–150ms jitter

---

## 9. Unresolved Questions

1. **Kernel `distill_parameterized` not durably committed** — harness-level only; kernel integration needed for product promotion
2. **Distributed transfer** — single-node substrate only; multi-worker/WAL transfer untested
3. **LLM-driven distillation** — "learn on A" half of C-PARAM-INHERIT completely untested
4. **Resource abstraction** — can induction be extended to parameterize base paths and generalize preconditions?
5. **Statistical power** — only 5 IDs per resource; needs larger-scale validation

---

*This report is bound to the frozen `spec.json`, `prereg.md`, and `freeze.json`. The `result.json` and `provenance.json` are the canonical machine-readable outputs per EXPERIMENT_PACKET.md.*