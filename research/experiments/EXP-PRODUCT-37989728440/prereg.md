# Preregistration: EXP-PRODUCT-37989728440

## 1. Context and Director Mandate

**Global Research Director allocation**: CONTINUE on C-RESIDUAL-NOVELTY with `cognitive_reset=true`, `parent_handoff_disposition=USE`.

**Binding strategic question** (from `request.json.director_mandate.allocation.question`):
> On a credential-free task bank whose correct action is NOT fully determined by the task specification (multi-step discovery, server-side state that must be read before acting, or parameters not derivable by direct URL construction), can a PRE-FREEZE, arithmetically checkable dynamic-range certificate be produced BEFORE freeze.json exists — B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED success_rate < 0.95 at novelty >= 0.5 on at least one task family, with matched correctness >= 0.80 for all arms — and, if so, does T-SPIDER-PARAM cost_per_success on an honest metric that INCLUDES retrieval_calls (plus http_requests, verification_calls, repair_attempts, latency_ms) show an advantage over BOTH comparators that increases monotonically with residual novelty (Spearman rho > 0.5, permutation p < 0.05), with the emptied-registry null matching cold, and with the treatment carrier either restored to or explicitly bound by git blob hash (audited blob b15ed848 / sha256 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72)? If the certificate is unsatisfiable on every credential-free deterministic substrate tested, record that bounded substrate-class result and route to the external-agent four-arm C-LLM-INHERIT benchmark on a provisioned model endpoint.

**Rationale** (from Director mandate):
- Two consecutive experiments on the deterministic localhost REST substrate (EXP-PRODUCT-37973256064, EXP-PRODUCT-37982016598) failed the dynamic-range certificate because both comparators sat at the 1.0 correctness ceiling by construction (correct action fully determined by task spec).
- The bottleneck is the task bank itself. The mandate must force the dynamic-range certificate to be demonstrated arithmetically BEFORE freeze rather than asserted.
- The same task bank is the enabling artifact for the later external-agent four-arm benchmark, so this work is shared, not duplicated.
- The treatment carrier must be the audited kernel path (blob b15ed848) bound by hash.

**Critical constraint**: `parent_handoff_disposition=USE` — this experiment inherits the parent handoff's four-way distinction (established/rejected/unknown/do_not_assume) as continuity evidence. Its `next_question` is advisory local continuity state, not automatic authorization. The Director's strategic question above is the binding research direction. DESIGN may refine that question into the smallest rigorous falsifiable experiment but may not silently drift back to the parent handoff or substitute a nearby objective.

## 2. Claims Under Test

**Primary: C-RESIDUAL-NOVELTY** — "Later-agent cost tracks residual novelty rather than full task length"
- Registry status: HYPOTHESIS
- Product capability: work compression economics
- Next gate: "matched task families with controlled novelty fraction and end-to-end cost"
- This experiment directly targets the registry next_gate on a real credential-free substrate with a certified dynamic range.

**Dependencies (must be live for this test to be meaningful):**
- **C-PARAM-INHERIT**: "Mechanisms parameterize to unseen identifiers" — EXPERIMENTAL. The treatment arm uses distill_parameterized -> resolve -> execute. Established live on real substrate in EXP-PRODUCT-37973256064 (audit PASS).
- **C-FRESHNESS**: "SPIDER can detect when inherited knowledge is stale" — HYPOTHESIS→EXPERIMENTAL (per EXP-GRAPH-37978902447). The task bank's session-scoped state rotation tests applicability/freshness implicitly.

## 3. Substrate: Real Localhost Stdlib-HTTP Application with Mandatory Discovery

### 3.1 Server Implementation
- **Technology**: Python 3.12+ `http.server` (stdlib only — no Flask, no external dependencies)
- **Port**: Dynamic (ephemeral, chosen at runtime)
- **Determinism**: Fixed seed (`SEED=42`), server state derived from seed + novelty level + task family. No stochastic elements, no jitter, no cache variance.
- **Lifecycle**: Started in-process by test harness, shut down after all arms complete.

### 3.2 Core Design Principle: Correct Action NOT Determined by Task Spec
The task specification provided to the agent is HIGH-LEVEL INTENT ONLY:
> "Update the resource of type {resource_type} with property {target_property} set to {target_value}"

The agent DOES NOT receive:
- The exact resource ID (must be discovered via GET /api/resources)
- The session token (must be obtained via GET /api/session)
- The exact endpoint parameterization (depends on discovered resource schema)

This is the critical difference from prior failed substrates where the task spec contained the full URL.

### 3.3 Server State Model (Per Novelty Level)
The server maintains a session-scoped state that varies by novelty level:

| Novelty Level | Session Token Required? | Valid Resource IDs Known? | Endpoint Parameterization Known? | Discovery Steps Required |
|---------------|------------------------|---------------------------|----------------------------------|-------------------------|
| 0.0 | No (fixed public token) | Yes (fixed public list) | Yes (fixed template) | 0 (direct URL construction works) |
| 0.25 | Yes (fixed per seed) | Yes (fixed per seed) | Yes (fixed template) | 1 (GET /api/session) |
| 0.50 | Yes (rotates per session) | Yes (fixed per seed) | Yes (fixed template) | 2 (GET /api/session, GET /api/resources) |
| 0.75 | Yes (rotates per session) | Rotates per session | Template varies per session | 3 (GET /api/session, GET /api/resources, GET /api/schema) |

**Novelty Definition**: Fraction of action-determining parameters NOT provided in the task spec.
- At novelty=0.0: Task spec fully determines the action (cold re-derivation works perfectly).
- At novelty>=0.5: Mandatory discovery steps required (cold re-derivation fails without discovery).

### 3.4 HTTP API Endpoints
```
GET  /api/session          → 200 {"session_token": "...", "expires": ...}
GET  /api/resources        → 200 {"resources": [{"id": "...", "type": "...", "schema": {...}}, ...]}
GET  /api/schema/{type}    → 200 {"type": "...", "update_endpoint": "/api/{type}/{id}/update", "params": ["property", "value"]}
POST /api/{type}/{id}/update  → 200 {"success": true} (requires valid session_token header, valid id, valid property)
```

All responses include `Content-Type: application/json` and deterministic `X-Request-Id`.

### 3.5 Task Families (for generalization test)
Two task families with different resource types and property schemas:

| Family | Resource Types | Target Properties | Schema Variation |
|--------|---------------|-------------------|------------------|
| F1     | documents, records | status, priority, owner | Flat JSON |
| F2     | widgets, gadgets | config, metadata, tags | Nested JSON |

Each family has 4 novelty levels (0.0, 0.25, 0.5, 0.75) × 5 held-out tasks per level = 20 test tasks per family.

### 3.6 Training Data (for Treatment and Retrieval Arms)
Per family: 10 training tasks at novelty=0.0 (fully specified, direct URLs work).
Observations captured: full trajectory including discovery steps (even though not needed at novelty=0.0), parameterized action templates, session token handling.

### 3.7 Distinction from Prior Failed Substrates
- **EXP-PRODUCT-37973256064 / 37982016598**: Task spec = "GET /api/items/item-006" — action fully determined by spec. Cold re-derivation = direct URL construction = 1.0 success.
- **This substrate**: Task spec = "Update document with status=archived" — action requires discovery. Cold re-derivation MUST perform discovery or fail.

## 4. Arms (Treatment + Three Comparators + Controls)

All arms share:
- Identical task specifications (high-level intent only)
- Identical substrate access: same server, same port, same HTTP client (`urllib.request`)
- Identical tooling budget: max 10 HTTP requests per task, 30 second timeout
- Identical observation format: `Observation(intent, state, action, next_state, success, provenance)`

### 4.1 T-SPIDER-PARAM (Treatment Arm)
**Mechanism**: SpiderKernel with `distill_parameterized` implemented (bound to audited blob b15ed848)
1. **Training phase**: 10 observations per family (novelty=0.0) → `distill_parameterized` induces parameterized mechanisms with `parameter_slots=["session_token", "resource_id", "property", "value"]`, `action_template` with `${slot}` placeholders, `confidence >= 0.85`
2. **Registry**: Mechanisms per family at confidence >= 0.85
3. **Test phase**: For each held-out task (20 per family × 2 families = 40 tasks):
   - `resolve(intent, context={"family": family, "novelty": level}, params={"target_property": ..., "target_value": ...})`
   - Kernel executes discovery steps internally (session → resources → schema) using parameterized sub-mechanisms
   - Expect `ResolutionStatus.EXECUTABLE` with fully bound action
   - Execute HTTP request, verify 200 response matches postconditions
4. **Accounting**: Per-task counters (model_calls=0, model_tokens=0, **retrieval_calls=1** (registry lookup), verification_calls=1, repair_attempts=0-2, http_requests=3-5 (discovery + execute), latency_ms)

### 4.2 B-COLD-RE-DERIVE (Cold Re-derivation Arm)
**Mechanism**: No inheritance, no registry, no retrieval
1. **Training phase**: None (training observations discarded)
2. **Test phase**: For each held-out task (same 40 tasks):
   - Agent receives task spec only: "Update {type} with {property}={value}"
   - Must discover: GET /api/session → extract token, GET /api/resources → find valid ID for type, GET /api/schema/{type} → get update endpoint
   - Construct HTTP request from discovered parameters
   - Execute, verify 200 response
3. **Accounting**: Per-task counters (model_calls=0, model_tokens=0, retrieval_calls=0, verification_calls=1, repair_attempts=0-2, http_requests=4-6 (discovery + execute), latency_ms)

### 4.3 B-RETRIEVAL-SHAPED (Retrieval-Shaped Comparator)
**Mechanism**: Structural similarity retrieval over training observations
1. **Training phase**: Store all 20 training observations (10 per family)
2. **Test phase**: For each held-out task (same 40 tasks):
   - Compute similarity between test task spec and each training observation:
     - Jaccard on action template keys + state keys
     - Exact match on family in state
   - Retrieve top-K=3 most similar training observations
   - **Must also perform discovery requests** (session, resources, schema) because retrieved templates have `${slot}` placeholders needing runtime values
   - Bind parameters: extract slots from retrieved action template, substitute discovered values
   - Execute bound action, verify
3. **Accounting**: Per-task counters (model_calls=0, model_tokens=0, **retrieval_calls=3**, verification_calls=1, repair_attempts=0-2, http_requests=4-6 (discovery + execute), latency_ms)

### 4.4 B-EMPTIED-REGISTRY (Null Control)
**Mechanism**: SpiderKernel with registry initialized empty (zero mechanisms)
1. **Training phase**: Observations provided but `distill_parameterized` returns None (registry stays empty)
2. **Test phase**: For each held-out task:
   - `resolve` returns `UNKNOWN` ("no applicable validated mechanism")
   - Falls back to cold re-derivation behavior (same as B-COLD-RE-DERIVE)
3. **Accounting**: Same as B-COLD-RE-DERIVE (retrieval_calls=0 since registry empty)
4. **Purpose**: Tests whether the registry itself is the carrier of advantage. Expected: cost_per_success matches B-COLD-RE-DERIVE within 10%.

### 4.5 B-LITERAL-KERNEL (Ablation Control)
**Mechanism**: SpiderKernel with ONLY literal `distill()` (confidence 0.5, no `parameter_slots`, no `distill_parameterized`)
1. **Training phase**: Same observations → literal mechanisms with confidence 0.5
2. **Test phase**: Tested on held-out tasks
3. **Expected**: `confidence=0.5 < min_confidence=0.8` → `ResolutionStatus.EXPLORE`/`UNKNOWN` on all parameterized tasks (success_rate < 0.20)
4. **Purpose**: Isolates parameterized path contribution.

### 4.6 PC-EXACT-REPLAY (Positive Control)
- Same as T-SPIDER-PARAM but tested on TRAINING tasks (novelty=0.0, 10 per family = 20 tasks)
- Expected: 100% success, 100% action reuse (zero novel decisions), EXECUTABLE on all
- Validates substrate can measure zero-novelty case and kernel binding works.

## 5. Known-Negative Test Cases (Refusal Detection)

Three categories, 5 test cases each per family = 30 known-negative tasks total:

| Category | Test Case | Expected Refusal Reason |
|----------|-----------|-------------------------|
| Out-of-support identifier | Task references resource_id not in /api/resources | "identifier not in support" or "precondition failed" |
| Out-of-support identifier | Task references resource_type not in training (e.g., "gizmos") | "no applicable validated mechanism" |
| Wrong intent | Use "delete" intent with "update" mechanism | "intent mismatch" or "no applicable validated mechanism" |
| Wrong intent | Use "create" intent with "update" mechanism | "intent mismatch" |
| Missing parameter | `resolve(..., params={})` (no target_property) | "required parameter 'target_property' missing" |
| Missing parameter | `resolve(..., params={"wrong_key": "value"})` | "required parameter 'target_property' missing" |

**Requirement**: All 30 known-negative cases → `bound_action=null`, non-empty `reason` string, status `UNKNOWN` or `EXPLORE` (not `EXECUTABLE`). Refusal reason must correctly categorize the failure type.

## 6. Metrics

### 6.1 Primary Metrics (Per Arm, Per Family, Per Novelty Level)
| Metric | Type | Target (Treatment) |
|--------|------|-------------------|
| `success_rate` | Proportion [0,1] | ≥ 0.80 at all novelty levels |
| `matched_correctness` | Proportion [0,1] | ≥ 0.80 at all novelty levels (same as success_rate for deterministic substrate) |
| `known_negative_refusal_rate` | Proportion [0,1] | ≥ 0.95 |
| `refusal_reason_correctness` | Proportion [0,1] | == 1.00 |
| `model_calls` | Count per task | == 0 (all arms) |
| `model_tokens` | Count per task | == 0 (all arms) |
| `retrieval_calls` | Count per task | Treatment: 1, Cold: 0, Retrieval: 3, Empty: 0 |
| `verification_calls` | Count per task | ≥ 1 (all arms) |
| `repair_attempts` | Count per task | ≥ 0 |
| `http_requests` | Count per task | Measured (3-6) |
| `latency_ms` | Continuous | Measured |

### 6.2 Derived Metrics
- `cost_per_success = (http_requests + retrieval_calls + verification_calls + repair_attempts + latency_ms/1000) / success_rate` — composite units, **includes retrieval_calls**
- `treatment_advantage_vs_cold = cost_per_success_cold - cost_per_success_treatment` (positive = treatment cheaper)
- `treatment_advantage_vs_retrieval = cost_per_success_retrieval - cost_per_success_treatment`
- `residual_novelty` = novelty level (0.0, 0.25, 0.5, 0.75) — the independent variable for monotonicity test
- `full_task_length` = total http_requests for cold arm — control variable (should NOT correlate with advantage)

### 6.3 Dynamic-Range Certificate Metrics (PRE-FREEZE, No Run Data)
Computed from frozen task bank design + frozen arm implementations:
- `cold_success_rate_at_novelty[level]` for each family — arithmetically determined by whether cold arm can succeed without discovery
- `retrieval_success_rate_at_novelty[level]` for each family — arithmetically determined by whether retrieval templates + discovery can succeed
- `certified = (exists family where cold_success_rate_at_novelty[0.5] < 0.95 AND retrieval_success_rate_at_novelty[0.5] < 0.95 AND all arms matched_correctness >= 0.80)`

## 7. Decision Rule (Frozen Before Execution)

### 7.1 C1: PRE-FREEZE Dynamic-Range Certificate (HARD GATE)
```
B-COLD-RE-DERIVE success_rate < 0.95 at novelty >= 0.5 on at least one task family
AND B-RETRIEVAL-SHAPED success_rate < 0.95 at novelty >= 0.5 on at least one task family
AND all arms matched_correctness >= 0.80 at all novelty levels on that family

Certificate computed from FROZEN task bank design + FROZEN arm implementations.
NO outcome data from the actual run.
If certificate=false at freeze time → experiment MUST NOT freeze → MEASUREMENT_INVALID.
```
**This is the critical gate that failed in the two prior experiments. It is enforced by the freeze script reading `spec.json.dynamic_range_certified`.**

### 7.2 C2: Matched Correctness
```
All arms achieve success_rate >= 0.80 on held-out tasks
at ALL novelty levels (0.0, 0.25, 0.5, 0.75)
on at least one task family.
```

### 7.3 C3: Cost Advantage vs Cold
```
Treatment cost_per_success < B-COLD-RE-DERIVE cost_per_success
at novelty >= 0.5 on at least one task family.
```

### 7.4 C4: Cost Advantage vs Retrieval
```
Treatment cost_per_success < B-RETRIEVAL-SHAPED cost_per_success
at novelty >= 0.5 on at least one task family.
```

### 7.5 C5: Novelty Monotonicity (THE C-RESIDUAL-NOVELTY TEST)
```
Spearman rho between residual_novelty and treatment_advantage_vs_cold > 0.5
with permutation p < 0.05 (10,000 permutations)
AND
Spearman rho between residual_novelty and treatment_advantage_vs_retrieval > 0.5
with permutation p < 0.05

Advantage must increase with RESIDUAL NOVELTY, not with full_task_length.
Control check: Spearman rho between full_task_length and advantage must be <= 0.3.
```

### 7.6 C6: Null Carrier (Registry is the Carrier)
```
B-EMPTIED-REGISTRY cost_per_success matches B-COLD-RE-DERIVE cost_per_success
within 10% relative difference across all novelty levels.
```

### 7.7 C7: Known-Negative Refusal
```
known_negative_refusal_rate >= 0.95 across all three categories
AND refusal_reason_correctness == 1.00
AND all_refusals_have_bound_action_null == True
```

### 7.8 C8: Accounting Honesty
```
model_calls == 0 for all arms
AND model_tokens == 0 for all arms
AND no counter event has injected=True
AND retrieval_calls differ between arms as designed (treatment=1, cold=0, retrieval=3, empty=0)
```

### 7.9 C9: Causal Attribution
```
B-LITERAL-KERNEL success_rate < 0.20 on held-out tasks at novelty >= 0.5
AND PC-EXACT-REPLAY success_rate == 1.00 on training tasks
```

### 7.10 C10: Substrate Validity
```
Server uses real HTTP (localhost stdlib)
AND task bank has >= 2 task families with genuine novelty gradient
AND substrate distinct from SYNTH-INDUCTION-BANK-v1 and prior REST substrate
```

### 7.11 C11: Treatment Carrier Bound
```
Treatment arm uses kernel code bound to git blob b15ed848
(sha256 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72)
per provenance.json.
```

### 7.12 OVERALL OUTCOME
| Outcome | Condition |
|---------|-----------|
| `SUPPORTS` | C1 through C11 all PASS |
| `FALSIFIES` | C1 fails (certificate unsatisfiable) OR C2 fails OR C5 fails OR C7 fails |
| `MIXED` | C1 passes but any of C3, C4, C6, C8, C9, C10, C11 fail |
| `MEASUREMENT_INVALID` | C1 fails at freeze time (certificate=false) OR infrastructure failure |

## 8. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Cold arm accidentally succeeds at high novelty without discovery | Server returns 401/404 for requests without valid session_token or resource_id. Cold arm MUST discover or fail. |
| Retrieval arm inadvertently matches treatment performance | Retrieval uses structural similarity ONLY; no parameter induction; top-K=3 fixed; must still do discovery. Retrieval_calls=3 counted honestly. |
| Counter inflation / injection | Counters incremented ONLY at explicit instrumented call sites; model counters hardcoded to 0; retrieval_calls instrumented in registry.resolve() and retrieval comparator. |
| Server non-determinism | Stdlib http.server, no threading, fixed seed, server state = deterministic function of (seed, novelty, family). |
| Parameter binding bugs in kernel | Unit-tested separately; PC-EXACT-REPLAY validates binding on training set. |
| Confounding by family difficulty | Balanced design: 5 held-out per novelty level per family, all arms tested on identical 40 tasks. |
| Support inference boundary collapse (prior 001-009 ceiling) | Training uses 10 examples (001-010) with explicit boundary examples; support regex target widened to `^type-0[0-9]{2}$`; novelty levels defined WITHIN support. |
| Cost metric saturation (prior all arms = 2.0) | Cost_per_success INCLUDES retrieval_calls (treatment=1, retrieval=3) and http_requests (cold=4-6, treatment=3-5). At novelty>=0.5, treatment should have fewer http_requests due to parameterized discovery sub-mechanisms. |
| Shipped kernel regression (blob cfec9866 lacks parameterized path) | Treatment carrier EXPLICITLY bound to audited blob b15ed848. EXECUTE must restore or vendor this exact blob. Provenance records the binding. |
| Dynamic-range certificate gaming | Certificate computed by FREEZE SCRIPT from frozen spec + arm implementations, not by producer. Producer cannot influence it after freeze. |

## 9. Kernel Implementation Requirement (for EXECUTE)

The current `src/spider/kernel.py` at HEAD (blob cfec9866) LACKS the parameterized path.
**EXECUTE MUST**: Restore `src/spider/kernel.py` to git blob `b15ed84865cdd0e91af6337299674d072db3e48121d78a15125a3c797ba2f3ab` (sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`) OR vendor a copy of that exact blob at `research/experiments/EXP-PRODUCT-37989728440/kernel_treatment.py` with its hash recorded in `provenance.json`.

Required kernel capabilities (from audited blob b15ed848):
- `distill_parameterized(observations)` → induces `parameter_slots`, `action_template` with `${slot}`, `confidence >= 0.85`
- `resolve(intent, context, params)` → binds parameters, executes discovery sub-mechanisms, returns `ResolutionStatus.EXECUTABLE` with `bound_action`
- `_support_accepts(mechanism, candidate_params)` → validates parameters against inferred support (widened to `^type-0[0-9]{2}$`)
- `rebind(mechanism, new_params)` → rebinds action template with new parameters
- `TrajectoryCounters` with `retrieval_calls`, `verification_calls`, `repair_attempts`, `http_requests`, `latency_ms`

## 10. Artifacts to Produce

| Artifact | Path | Purpose |
|----------|------|---------|
| Raw evidence | `raw_evidence/task_trajectories.jsonl` | Per-task raw observations, resolutions, executions, verifications, refusals |
| Raw evidence | `raw_evidence/accounting_counters.jsonl` | Per-task counter events with timestamps and arm labels |
| Raw evidence | `raw_evidence/server_log.jsonl` | HTTP request/response log with session/novelty tags |
| Raw evidence | `raw_evidence/known_negatives.jsonl` | 30 known-negative cases with refusal reasons |
| Raw evidence | `raw_evidence/induced_mechanisms.json` | Induced mechanisms with parameter_slots, support regexes, confidence |
| Derived | `derived/arm_metrics.json` | Aggregated metrics per arm per family per novelty level |
| Derived | `derived/dynamic_range_cert.json` | **PRE-FREEZE certificate** with per-family per-novelty success rates for cold/retrieval |
| Derived | `derived/decision_rule_eval.json` | Pass/fail per decision rule clause with evidence refs |
| Derived | `derived/spearman_monotonicity.json` | Spearman rho, permutation p-values, full_task_length control |
| Code | `src/spider/kernel.py` (restored to b15ed848) OR `kernel_treatment.py` (vendored b15ed848) | Treatment carrier bound by hash |
| Code | `run_experiment.py` | Experiment harness |
| Report | `report.md` | Interpretation bounded by measurements |

## 11. Reproducibility

- **Seed**: `SEED=42` for server, harness, all randomization
- **Environment**: Python 3.12+, stdlib only (no pip dependencies beyond spider package)
- **Commit**: Kernel restoration/vendoring recorded in provenance.json before freeze
- **Determinism**: Single-threaded, no async, no external services
- **Freeze enforcement**: Freeze script reads `spec.json` and computes C1 certificate from frozen design. If `dynamic_range_certified=false`, freeze script exits with error and does not create `freeze.json`.

## 12. Carry-Forward from Parent Handoff (EXP-PRODUCT-37982016598)

This experiment explicitly addresses the parent handoff's `unknown` and `do_not_assume` items:

**Unknown → Targeted for Resolution:**
- "Whether ANY credential-free task bank on this architecture/substrate can produce a certified dynamic range" → This substrate design targets YES.
- "Whether T-SPIDER-PARAM would show any cost/novelty advantage if a non-ceiling task bank existed" → C5 tests this directly.
- "What the correct cost-per-success metric should be: include retrieval_calls" → C8 mandates inclusion.
- "Whether the treatment's support-boundary collapse at novelty >= 0.5 is fixable" → Training widened to 001-010, support regex target widened.

**Do Not Assume → Enforced as Constraints:**
- "Do not read this packet as evidence for or against C-RESIDUAL-NOVELTY" → C1 gate prevents measurement without dynamic range.
- "Do not treat cold/retrieval success_rate=1.0 as evidence that cold re-derivation or retrieval substitutes for inheritance" → Substrate designed so cold/retrieval MUST do discovery at novelty>=0.5.
- "Do not assume the shipped kernel contains the audited parameterized path" → C11 requires explicit binding to b15ed848.
- "Do not assume the pre-freeze certificate gate is enforced by the freeze step" → Freeze script enforcement specified in Section 11.
- "Do not re-run this certificate or the parent certificate; redesign the task bank" → This is a redesigned task bank (mandatory discovery, novelty gradient).
- "Do not promote any of this packet's code or scaffolding to product core" → `product_consequence_negative` forbids promotion unless C1-C11 all pass.

## 13. Dependencies for Downstream Work

Per Director mandate and parent handoff, this experiment's success enables:
1. **Four-arm C-LLM-INHERIT benchmark** (cold vs instructions vs retrieval vs SPIDER) on a provisioned model endpoint — requires this task bank with certified dynamic range.
2. **C-PRODUCT-ECON end-to-end amortized economics** — same task bank, honest cost metric.
3. **C-FRESHNESS integration** — session-scoped state rotation in this substrate tests applicability guards.

---

**This preregistration is frozen upon creation of `freeze.json`. No outcome-bearing measurements may be inspected before freeze. The decision rule above is binding. The PRE-FREEZE dynamic-range certificate (C1) is a hard gate: if unsatisfiable, the experiment MUST NOT freeze and MUST record MEASUREMENT_INVALID.**