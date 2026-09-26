# Preregistration: EXP-GRAPH-36118890504

## 1. Experiment Identity
- **Experiment ID**: EXP-GRAPH-36118890504
- **Lane**: graph
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Director Mandate**: PIVOT from C-DELTA-REPAIR to C-PARAM-INHERIT (Global Research Director cycle 36118077218)
- **Parent Handoff**: EXP-GRAPH-36106653880 (MEASUREMENT_INVALID, distributed substrate failed)

## 2. Strategic Question (Director Mandate)
> Using the already audited distributed plain-HTTP shared-WAL substrate, can a mechanism distilled from resource-A observations resolve, bind, execute, and verify correctly on never-observed resource B with disjoint identifier value sets, while outperforming cold exploration, literal replay, and retrieval baselines on success and honest per-task cost without converting false accepts into executable mechanisms?

**Refined for this DESIGN**: Using a **validated single-node plain-HTTP substrate** (Flask/JWT, Runtime EXP-RUNTIME-33902315583 ceiling), can a parameterized mechanism induced from resource A transfer to resource B with disjoint IDs, beating cold/literal/retrieval baselines on success and cost, with false accepts < 10%?

*Dependency*: Runtime must provide the distributed shared-WAL substrate for future transfer testing. This experiment uses the validated single-node substrate to isolate the mechanism transfer question from the substrate blocker.

## 3. Hypothesis
A parameterized mechanism induced from successful observations on resource A (e.g., `GET /posts/{id}` for ids 1..5) will transfer to resource B (e.g., `GET /users/{id}` for ids 6..10, disjoint ID space) achieving:
- Higher success rate than cold exploration, literal replay, and KNN retrieval baselines
- Lower honest per-task cost (HTTP requests) than the best baseline
- False accept rate ≤ 10% on unrelated resource C

## 4. Falsifier
The experiment **FALSIFIES** the hypothesis if ANY of:
1. Parameterized mechanism success rate on resource B does NOT exceed ALL THREE baselines by ≥10 pp
2. Parameterized mechanism honest cost on resource B is NOT ≥20% lower than the best baseline
3. Parameterized mechanism false accept rate on resource C exceeds 10%
4. Positive control fails (mechanism doesn't work on resource A seen IDs)
5. Null control fails (mechanism falsely accepts on resource C)

## 5. Experimental Design

### 5.1 Resources (Isomorphic Action Templates)
| Resource | Base Path | Method | Parameter Slot | Response Schema | ID Space |
|----------|-----------|--------|----------------|-----------------|----------|
| **A (Train)** | `/posts` | GET | `id` | `{id, userId, title, body}` | 1,2,3,4,5 |
| **B (Test)** | `/users` | GET | `id` | `{id, name, username, email}` | 6,7,8,9,10 |
| **C (Null)** | `/comments` | POST | `postId, body` | `{id, postId, name, email, body}` | 11,12,13,14,15 |

- **Isomorphic A↔B**: Same HTTP method (GET), single path parameter `{id}`, JSON response with `id` field
- **Disjoint IDs**: A uses 1-5, B uses 6-10, C uses 11-15 (no overlap)
- **Non-isomorphic C**: Different method (POST), two parameters, different schema → null control

### 5.2 Substrate
- **Validated**: Single-node Flask 3.1.3 + PyJWT 2.13.0 HS256 (Runtime EXP-RUNTIME-33902315583, EXP-RUNTIME-34015740602)
- **Endpoints**: Localhost, deterministic responses, 50-150ms jitter
- **Authentication**: Bearer token required (valid/expired/invalid states tested by Runtime)
- **No browser, no Playwright, no LLM policy** — pure HTTP observation/execution

### 5.3 Mechanism Induction (Train Phase — Resource A Only)
1. **Observe** 5 successful trajectories on resource A (ids 1..5):
   - Intent: "fetch resource by id"
   - State: `{auth: valid_token, resource: "posts"}`
   - Action: `{method: "GET", url: "/posts/{id}", params: {id: N}}`
   - Next State: `{status: 200, body: {...}}`
2. **Distill** parameterized mechanism via `distill_parameterized()`:
   - Detect varying `id` in URL path → parameter slot `id`
   - Fixed template: `GET /posts/${id}`
   - Preconditions: `{auth: valid_token, resource: "posts"}`
   - Postconditions: `{status: 200}`
   - Confidence: 0.95
3. **Register** mechanism in registry

### 5.4 Test Phase — Resource B (Never-Observed, Disjoint IDs)
For each test ID in {6,7,8,9,10}:
1. **Context**: `{auth: valid_token, resource: "users"}` (different resource name)
2. **Params**: `{id: test_id}`
3. **Resolve**: `kernel.resolve("fetch resource by id", context, params)`
4. **Execute**: If EXECUTABLE, perform HTTP request with bound action
5. **Verify**: Check response matches postconditions
6. **Record**: Success/failure, HTTP requests made, resolution status

### 5.5 Baseline Conditions (Same Test IDs on Resource B)
| Baseline | Registry Content | Resolution Strategy |
|----------|------------------|---------------------|
| **B-COLD** | Empty | Agent must explore: try common patterns until success |
| **B-LITERAL-REPLAY** | Literal mechanisms from resource A (no params) | Exact replay: `GET /posts/1` → fails on `/users/6` |
| **B-RETRIEVAL-KNN** | Raw observations from resource A | Embed context, retrieve nearest, naive string replace `/posts/`→`/users/` |

### 5.6 Null Control — Resource C
- Same parameterized mechanism from resource A
- Test contexts: `{auth: valid_token, resource: "comments"}` with params `{postId: N, body: "test"}`
- Expect: Resolution = UNKNOWN/EXPLORE (preconditions don't match, wrong method, wrong params)

## 6. Metrics (Stable Identities for Downstream Transmission)

| Metric ID | Definition | Unit |
|-----------|------------|------|
| `success_rate_B_param` | Fraction of resource B test IDs where param mechanism resolves EXECUTABLE, executes, and verifies | [0,1] |
| `success_rate_B_cold` | Same for cold baseline | [0,1] |
| `success_rate_B_literal` | Same for literal replay baseline | [0,1] |
| `success_rate_B_knn` | Same for KNN retrieval baseline | [0,1] |
| `cost_per_task_B_param` | Mean HTTP requests per resource B task (including failed/exploratory) | count |
| `cost_per_task_B_cold` | Same for cold baseline | count |
| `cost_per_task_B_literal` | Same for literal replay baseline | count |
| `cost_per_task_B_knn` | Same for KNN retrieval baseline | count |
| `false_accept_rate_C_param` | Fraction of resource C tests where param mechanism resolves EXECUTABLE | [0,1] |
| `success_rate_A_param_seen` | Positive control: param mechanism on resource A seen IDs (1..5) | [0,1] |

## 7. Controls (Stable Identifiers)

| Control ID | Type | Expected | Pass Criterion |
|------------|------|----------|----------------|
| `PC-A-SEEN` | Positive | Success rate = 1.0 on resource A ids 1..5 | `success_rate_A_param_seen == 1.0` |
| `NC-UNRELATED-RESOURCE` | Null | Zero false accepts on resource C | `false_accept_rate_C_param == 0.0` |

## 8. Measurement Validity Gates (Must All Pass)

| Gate | Check | Failure → |
|------|-------|-----------|
| V1_SUBSTRATE | Substrate matches Runtime validated config (Flask/JWT, deterministic fingerprint) | MEASUREMENT_INVALID |
| V2_DISJOINT_IDS | Train IDs ∩ Test IDs = ∅ | MEASUREMENT_INVALID |
| V3_ISOMORPHIC_ACTION | A and B share method/param-slot/response-shape | MEASUREMENT_INVALID |
| V4_HONEST_COST | All HTTP requests counted, no hidden caching | MEASUREMENT_INVALID |
| V5_NO_LEAKAGE | Induction sees only resource A; test contexts don't reveal B structure | MEASUREMENT_INVALID |
| V6_DETERMINISTIC_EXECUTION | Same (resource, id) → identical response | MEASUREMENT_INVALID |
| V7_VERIFICATION_REAL | verify() checks actual HTTP response vs postconditions | MEASUREMENT_INVALID |

## 9. Decision Rule (Conjunctive)

| Condition | Metric | Threshold |
|-----------|--------|-----------|
| D1_SUCCESS_B | `success_rate_B_param` | > max(baselines) + 0.10 |
| D2_COST_B | `cost_per_task_B_param` | < min(baselines) × 0.80 |
| D3_FALSE_ACCEPT | `false_accept_rate_C_param` | ≤ 0.10 |
| D4_POSITIVE_CONTROL | `success_rate_A_param_seen` | == 1.0 |
| D5_NULL_CONTROL | `false_accept_rate_C_param` | == 0.0 |

**Outcome Mapping**:
- All 5 pass → `SUPPORTS`
- Any fail → `FALSIFIES`
- D4 fails → `MEASUREMENT_INVALID` (substrate/induction broken)
- D5 fails → `FALSIFIES` (safety gate)
- Incomplete data → `INCONCLUSIVE`

## 10. Product Consequences

### Positive (SUPPORTS)
- C-PARAM-INHERIT advances toward **VALIDATED**: parameterized transfer across disjoint ID spaces demonstrated on validated HTTP substrate
- Product may integrate parameterized inheritance into external-agent kernel
- Next gates: real-web DOM/auth/session/drift transfer; LLM distillation half of C-PARAM-INHERIT

### Negative (FALSIFIES or MEASUREMENT_INVALID)
- C-PARAM-INHERIT remains at **synthetic POC ceiling** (EXPERIMENTAL or BLOCKED)
- Parameterized transfer fails on validated HTTP substrate → induction/binding logic fundamentally limited
- Product must NOT promote parameterized mechanisms
- Graph must fix induction/binding OR pivot to alternative transfer mechanism

## 11. Validity Threats & Mitigations

| Threat | Mitigation |
|--------|------------|
| Substrate not yet distributed | Design uses validated single-node; distributed transfer is separate future experiment |
| jsonplaceholder not "real web" | Substrate is validated Flask/JWT; resources are isomorphic test fixtures — the claim is about mechanism transfer, not site realism |
| KNN retrieval baseline weak | Baseline is intentionally weak (naive string replace); stronger retrieval is future work |
| Cost accounting honesty | Explicit V4_HONEST_COST gate; all requests logged |
| False accept definition | Null control uses structurally different resource (POST vs GET, 2 params vs 1) |

## 12. Independence from Pre-2.0 Work
- Does NOT repeat: synthetic single-param POC (EXP-PRODUCT-33528829801), multi-param POC (EXP-PRODUCT-33741671686), competition fix (EXP-GRAPH-33816735314), kernel integration attempts (EXP-PRODUCT-33974562602+)
- **Novel**: First experiment testing **disjoint identifier space transfer** (A→B with zero ID overlap) on **validated HTTP substrate** with **honest cost accounting** against **strong baselines** (cold, literal, retrieval)
- Pre-2.0 work tested same-ID or overlapping-ID transfer; this tests the registry's explicit next_gate: "learn on resource A, succeed on never-observed B"

## 13. Execution Plan (For EXECUTE Stage)
1. Provision validated Flask/JWT substrate (reuse Runtime EXP-RUNTIME-33902315583 code/config)
2. Implement 3 resources (/posts, /users, /comments) with isomorphic A/B, distinct C
3. Run train phase: 5 observations on resource A → induce parameterized mechanism
4. Run test phase: 5 test IDs on resource B for param mechanism + 3 baselines
5. Run null control: 5 test IDs on resource C for param mechanism
6. Run positive control: 5 seen IDs on resource A for param mechanism
7. Compute all metrics, check validity gates, apply decision rule
8. Emit result.json, report.md, provenance.json per EXPERIMENT_PACKET.md

## 14. Dependencies & Blockers
- **Runtime**: Must provide validated single-node Flask/JWT substrate config (already done in EXP-RUNTIME-33902315583)
- **Kernel**: `distill_parameterized()` and `resolve()` in `src/spider/kernel.py` (current HEAD)
- **Registry**: `MechanismRegistry` in `src/spider/registry.py`
- **No new code required** — uses existing kernel/registry; experiment is a harness

## 15. Carried-Forward State from Parent Handoff (EXP-GRAPH-36106653880)

| Category | Items Preserved |
|----------|-----------------|
| **Established** | Single-node C-DELTA-REPAIR health-gated result is EXPERIMENTAL (EXP-GRAPH-36018188168); synthetic ceilings only |
| **Rejected** | Single-channel guard insufficient; always-EXECUTABLE unsafe; retrieval ≠ repair |
| **Unknown** | Whether C-PARAM-INHERIT works on validated HTTP substrate with disjoint IDs (THIS EXPERIMENT) |
| **Do Not Assume** | Producer's COMPLETE/MIXED ≠ scientific result; zero metrics ≠ observations; n_non304=0 ≠ falsification; C-DELTA-REPAIR not promoted |

---
*This preregistration is frozen at DESIGN. EXECUTE must not modify any field above. Any deviation requires new DESIGN+FREEZE.*