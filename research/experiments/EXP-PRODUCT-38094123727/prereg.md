# Preregistration: EXP-PRODUCT-38094123727

## 1. Context and Director Mandate

**Global Research Director allocation**: `CONTINUE` on `C-PARAM-INHERIT` with `cognitive_reset=true`, `parent_handoff_disposition=SUPERSEDE`.

**Binding strategic question** (from `request.json.director_mandate.allocation.question`):
> Can the audited parameterized inherited carrier be landed into the shipped kernel through the sanctioned promotion path - so that after promotion the shipped execution path contains a concrete parameterized mechanism that an inherited procedure visibly instantiates and executes, together with a companion known-negative refusal certificate - such that blocker B1 is satisfied and the pre-freeze executable mechanism required by readiness condition (1) exists, rather than once more running the four-arm economics benchmark on a kernel that still emits literals below the execution threshold?

**Rationale** (from Director mandate):
- **B1 verified at source**: `src/spider/kernel.py` contains only literal `distill()` and a candidate at confidence 0.5 against a default 0.8 execution threshold, while `distill_parameterized()` is absent, so the shipped path has no executable treatment to benchmark.
- **The audited experimental carrier exists**: EXP-PRODUCT-37973256064 demonstrated `distill_parameterized -> resolve -> execute` live and causally attributable (12/15 new identifiers executed, 0/15 for the literal incumbent at its frozen confidence gate, credential-free HTTP substrate outside the synthetic fixture).
- **Centrally, I explicitly do NOT fund the four-arm COLD/INSTRUCTIONS/RETRIEVAL/SPIDER benchmark this cycle**: readiness conditions (2) and (3) do not hold, so Product is funded ONLY to land the carrier and its known-negative refusal path through the sanctioned promotion route.
- **This supersedes the inherited proposal** to run the benchmark on a credential-free endpoint, which is blocked by B2 and B3.

**Critical constraint**: `parent_handoff_disposition=SUPERSEDE` — this experiment MUST NOT silently drift back to the parent handoff's agenda (EXP-PRODUCT-37989728440's `next_question` about the four-arm benchmark). The parent's agenda is explicitly NOT this experiment's question. This experiment's question is the Director's binding strategic question above.

## 2. Claim Under Test

**C-PARAM-INHERIT**: "Mechanisms parameterize to unseen identifiers"
- Registry status: `EXPERIMENTAL`
- Product capability: parameterized inheritance
- Next gate: "learn on resource A, succeed on never-observed B against cold/replay/retrieval baselines"
- This experiment directly targets **blocker B1 removal**: landing the executable parameterized carrier into the shipped kernel. It does NOT test the four-arm C-LLM-INHERIT benchmark (blocked on B2, B3).

## 3. Substrate: Real Localhost Stdlib-HTTP Application (Identical to Audited Carrier)

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
- **Identical to EXP-PRODUCT-37973256064 substrate**: This exact substrate was used to validate the audited carrier.

## 4. Arms (Treatment + Baselines + Controls)

All arms share:
- Identical task specifications: "Read resource {type} with identifier {id}"
- Identical substrate access: same server, same port, same HTTP client (`urllib.request`)
- Identical tooling budget: max 5 HTTP requests per task, 30 second timeout
- Identical observation format: `Observation(intent, state, action, next_state, success, provenance)`

### 4.1 T-PROMOTED-KERNEL (Treatment Arm — THE SHIPPED KERNEL AFTER PROMOTION)
**Mechanism**: `src/spider/kernel.py` AFTER sanctioned promotion of the audited carrier.
1. **Promotion step**: Execute the sanctioned promotion workflow to copy the audited kernel implementation (git blob b15ed848, sha256 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72) into `src/spider/kernel.py`. Verify promotion completes and the module is importable.
2. **Training phase**: 5 observations per resource type (A identifiers) → `distill_parameterized` induces 1 parameterized mechanism per type with `parameter_slots=["id"]`, `action_template.path="/api/{type}/${id}"`, `confidence=0.90`.
3. **Registry**: 3 mechanisms (items, users, orders) at confidence 0.90.
4. **Test phase**: For each held-out B identifier (5 per type × 3 types = 15 tasks):
   - `resolve(intent, context={"resource_type": type}, params={"id": identifier})`
   - Expect `ResolutionStatus.EXECUTABLE` with `bound_action.path="/api/{type}/{identifier}"`
   - Execute HTTP request, verify 200 response matches postconditions
5. **Accounting**: Per-task counters (model_calls=0, model_tokens=0, retrieval_calls=1, verification_calls=1, repair_attempts=0, http_requests=1, latency_ms)

### 4.2 B-LITERAL-KERNEL (Ablation Control — CURRENT SHIPPED KERNEL BEFORE PROMOTION)
**Mechanism**: `src/spider/kernel.py` at `base_sha` (git blob cfec98660b0277ccbf295e8a4119e8d81ddccf50) — ONLY literal `distill()` with confidence 0.5, NO `distill_parameterized`.
1. **Training phase**: Same 5 observations per resource type (A identifiers) → `distill()` creates literal mechanisms with confidence 0.5.
2. **Test phase**: For each held-out B identifier (same 15 tasks):
   - `resolve(intent, context={"resource_type": type}, params={"id": identifier})`
   - Expected: `confidence=0.5 < min_confidence=0.8` → `ResolutionStatus.EXPLORE` or `UNKNOWN` on all parameterized tasks (success_rate < 0.20)
3. **Accounting**: Per-task counters (model_calls=0, model_tokens=0, retrieval_calls=0, verification_calls=0, repair_attempts=0, http_requests=0, latency_ms) — no execution occurs.

### 4.3 B-AUDITED-CARRIER (Positive Control — AUDITED KERNEL IN HARNESS)
**Mechanism**: The exact audited kernel from EXP-PRODUCT-37973256064/EXP-PRODUCT-37989728440 (harness copy at `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`), run in the experiment harness for fidelity comparison.
1. **Training phase**: Same as T-PROMOTED-KERNEL.
2. **Test phase**: Same 15 held-out B tasks.
3. **Expected**: Success rate matching the audited result (12/15 = 0.80), known-negative refusal 15/15.
4. **Purpose**: Verify the promoted kernel (T-PROMOTED-KERNEL) matches the audited behavior exactly (fidelity check).

### 4.4 NC-KNOWN-NEGATIVE (Null Control — Known-Negative Refusal Certificate)
**Mechanism**: T-PROMOTED-KERNEL mechanisms tested on declared negative cases.
Three categories, 5 test cases each = 15 known-negative tasks:

| Category | Test Case | Expected Refusal Reason |
|----------|-----------|-------------------------|
| Out-of-support identifier | `GET /api/items/item-999` | "parameter 'id' outside inferred support" |
| Out-of-support identifier | `GET /api/users/user-xyz` | "parameter 'id' outside inferred support" |
| Wrong intent | Use "delete" intent with "read" mechanism | "no applicable validated mechanism" |
| Wrong intent | Use "create" intent with "read" mechanism | "no applicable validated mechanism" |
| Missing parameter | `resolve(..., params={})` (no `id`) | "missing required parameter 'id'" |
| Missing parameter | `resolve(..., params={"wrong_key": "value"})` | "missing required parameter 'id'" |

**Requirement**: All 15 known-negative cases → `bound_action=null`, non-empty `reason` string, status `EXPLORE` or `UNKNOWN` (not `EXECUTABLE`). Refusal reason must correctly categorize the failure type.

## 5. Metrics

### 5.1 Primary Metrics (Per Arm)
| Metric | Type | Target (T-PROMOTED-KERNEL) |
|--------|------|-------------------|
| `success_rate_heldout_B` | Proportion [0,1] | ≥ 0.80 |
| `known_negative_refusal_rate` | Proportion [0,1] | ≥ 0.95 |
| `refusal_reason_correctness` | Proportion [0,1] | == 1.00 |
| `model_calls` | Count per task | == 0 (all arms) |
| `model_tokens` | Count per task | == 0 (all arms) |
| `retrieval_calls` | Count per task | Treatment: 1, Literal: 0 |
| `verification_calls` | Count per task | ≥ 1 (treatment), 0 (literal) |
| `repair_attempts` | Count per task | ≥ 0 |
| `http_requests` | Count per task | ≥ 1 (treatment), 0 (literal) |
| `latency_ms` | Continuous | Measured |

### 5.2 Derived Metrics
- `fidelity_vs_audited = 1.0 - abs(success_rate_promoted - success_rate_audited)`
- `causal_attribution = success_rate_promoted - success_rate_literal_kernel`
- `promotion_success = boolean` (code landed in src/spider/kernel.py, module imports, validation passes)

## 6. Decision Rule (Frozen Before Execution)

### 6.1 PROMOTION (Sanctioned promotion completes)
```
promoted_kernel_exists_in_src == True
AND src_spider_kernel_imports_without_error == True
AND promotion_validation_passes == True
```

### 6.2 PRIMARY (Treatment separation on held-out)
```
success_rate_promoted >= 0.80
```

### 6.3 KNOWN-NEGATIVE (Refusal correctness)
```
known_negative_refusal_rate >= 0.95
AND refusal_reason_correctness == 1.00
AND all_refusals_have_bound_action_null == True
```

### 6.4 CAUSAL ATTRIBUTION (Parameterized path is necessary)
```
success_rate_literal_kernel < 0.20
```

### 6.5 FIDELITY (Promoted kernel matches audited carrier)
```
abs(success_rate_promoted - success_rate_audited) <= 0.05
AND known_negative_pattern_matches_audited == True
```

### 6.6 OVERALL OUTCOME
- `SUPPORTS`: All five rule groups PASS
- `FALSIFIES`: PROMOTION fails OR PRIMARY fails OR KNOWN-NEGATIVE fails
- `MIXED`: PROMOTION and PRIMARY pass but KNOWN-NEGATIVE or CAUSAL-ATTRIBUTION or FIDELITY fails
- `MEASUREMENT_INVALID`: Substrate fails to start, promotion infrastructure failure, or non-determinism detected

## 7. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Promotion workflow does not exist or is broken | The Director mandate references "sanctioned promotion path" implemented in `scripts/finalize_lane.py` (lines 293-296: `if verdict["promote_to_product"] and req["lane"] != "product": raise...`). The experiment will execute this path. |
| Promoted kernel has subtle differences from audited carrier | FIDELITY check requires behavior match within 0.05 success rate and identical refusal patterns. B-AUDITED-CARRIER runs in same harness for direct comparison. |
| Substrate too simple (trivial parameter binding) | Three resource types, systematic identifier patterns, real HTTP 404 on unknown ids. Identical to audited carrier's substrate. |
| Literal kernel accidentally gets parameterized | B-LITERAL-KERNEL uses the pre-promotion kernel (frozen at base_sha) which has NO distill_parameterized. Verified by git blob hash. |
| Counter inflation / injection | Counters incremented ONLY at explicit instrumented call sites; model counters hardcoded to 0. |
| Server non-determinism | Stdlib http.server, no threading, fixed seed, no cache, no jitter. |
| Parameter binding bugs in promoted kernel | Unit-tested separately; B-AUDITED-CARRIER validates binding on training set. |
| Confounding by resource type difficulty | Balanced design: 5 held-out per type, all arms tested on identical 15 tasks. |

## 8. Kernel Implementation Requirement (for PROMOTION)

The current `src/spider/kernel.py` ONLY has literal `distill()`. The sanctioned promotion must replace it with the audited implementation containing `distill_parameterized`. The audited implementation (from git blob b15ed848) includes:

```python
def distill_parameterized(self, observations: list[Observation]) -> Mechanism | None:
    """Induce one parameterized mechanism from repeated successful observations.
    - Group observations by intent
    - Find varying fields in action_template (e.g., URL path segments)
    - Create parameter_slots for each varying field
    - Build action_template with ${slot} placeholders
    - Infer support descriptors (regex character classes) from observed values
    - Compute confidence: 0.9 if self-verified on induction observations, else 0.5
    - Return Mechanism with parameter_slots, confidence >= 0.8
    """
```

The implementation must:
- Be in `src/spider/kernel.py` (the SHIPPED kernel)
- Produce mechanisms compatible with existing `resolve()` and `_bind()`
- Achieve confidence >= 0.8 on 5 consistent training observations
- Handle the three resource types in this experiment
- Preserve the literal `distill()` path unchanged (for B-LITERAL-KERNEL control)
- Include `TrajectoryCounters` integration for honest accounting
- Include `rebind()` for single repair attempt (C-DELTA-REPAIR precursor)
- Include `verify()` with parameter binding for postcondition checking

## 9. Artifacts to Produce

| Artifact | Path | Purpose |
|----------|------|---------|
| Raw evidence | `raw_evidence/task_trajectories.jsonl` | Per-task raw observations, resolutions, executions, verifications |
| Raw evidence | `raw_evidence/accounting_counters.jsonl` | Per-task counter events with timestamps |
| Raw evidence | `raw_evidence/server_log.jsonl` | HTTP request/response log |
| Raw evidence | `raw_evidence/known_negatives.jsonl` | Known-negative refusal details |
| Derived | `derived/arm_metrics.json` | Aggregated metrics per arm |
| Derived | `derived/decision_rule_eval.json` | Pass/fail per decision rule clause |
| Derived | `derived/fidelity_check.json` | Promoted vs audited carrier comparison |
| Code | `src/spider/kernel.py` (modified by promotion) | Promoted kernel with distill_parameterized |
| Code | `harness/run_experiment.py` | Experiment harness |
| Code | `harness/substrate.py` | HTTP substrate |
| Report | `report.md` | Interpretation bounded by measurements |

## 10. Reproducibility

- **Seed**: `SEED=42` for server, harness, all randomization
- **Environment**: Python 3.12+, stdlib only (no pip dependencies beyond spider package)
- **Commit**: Kernel promotion committed to lab2/product branch before freeze (via sanctioned promotion workflow)
- **Determinism**: Single-threaded, no async, no external services
- **Frozen references**: 
  - Audited carrier: git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` (sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`)
  - Current shipped kernel: git blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50` at `base_sha` `6b4a1f7b18e84015e1765965081f2a8e97d3ba27`
  - Promotion workflow: `scripts/finalize_lane.py` at `base_sha`

## 11. Comparative Reasoning Against Pre-2.0 Legacy

**LEGACY: DISTINCT_EXTENSION** (per Director mandate).
- **P2-REPLAY-COST** (artifact 9687ff787f2d74460bb7006826008852f5b4416b): 1.002x on matched tasks; guard: do not frame scripted replay as real-agent economics. **This experiment does not measure economics**; it lands the executable carrier prerequisite.
- **P2-BLIND-COMPOSITION** (artifact 017a80aeb9a6759c8f6913a37031ff1616ec1bda): G-H2 3/3 vs 0/3 under weak baselines and keyword/oracle dependence. **This experiment uses strong causal-attribution controls (B-LITERAL-KERNEL) and a real HTTP substrate**, not keyword matching.
- **P2-MIND2WEB**: Exact human route 6/176; distinct-and-decomposable structure. **This experiment tests identifier-parameterized mechanisms on a systematic identifier space**, not human-route imitation.
- **None of these landed an identifier-general mechanism into a shipped executable path with a known-negative refusal certificate.** This experiment is a materially distinct extension: promote the audited parameterized carrier via the sanctioned path and prove positive execution plus a known-negative refusal certificate.

## 12. Design Self-Attack (Satisfiability Probes)

Before finalizing, I actively attack this design for the six v2 freeze_eligibility failure modes:

### 12.1 Empty/Unreachable Decision Branches
- **Check**: Can PROMOTION fail while PRIMARY passes? No — if promotion fails, there is no promoted kernel to test, so PRIMARY is undefined. The decision rule correctly makes PROMOTION a gate.
- **Check**: Can KNOWN-NEGATIVE pass while PRIMARY fails? Yes — the kernel could refuse correctly but fail on held-out. This is MIXED, correctly captured.
- **Check**: Are there any arithmetic impossibilities? No — all thresholds are achievable (audited carrier achieved 0.80 and 1.00 refusal).

### 12.2 Missing Prerequisites
- **Audited carrier**: Exists at known git blob (verified).
- **Promotion workflow**: Exists in `scripts/finalize_lane.py` (verified — lines 293-296 enforce Product lane + PASS audit for promotion; this experiment uses the same machinery but with `promote_to_product=false` since it's a prerequisite landing).
- **Substrate**: Implemented and tested in EXP-PRODUCT-37973256064 (harness/substrate.py exists).
- **All prerequisites present**.

### 12.3 Ceiling/Floor Baselines
- **B-LITERAL-KERNEL floor**: Confidence 0.5 < 0.8 is a hard floor. If it ever achieves >= 0.20 success, the confidence gate is broken — correctly detected.
- **B-AUDITED-CARRIER ceiling**: Achieved 0.80. FIDELITY allows 0.05 tolerance. No ceiling problem.
- **NC-KNOWN-NEGATIVE**: 100% refusal is the expected ceiling. < 0.95 is a clear failure signal.

### 12.4 Treatment/Comparator Identity
- **T-PROMOTED-KERNEL** vs **B-LITERAL-KERNEL**: Different code (promoted vs pre-promotion). Verified by git blob hash comparison.
- **T-PROMOTED-KERNEL** vs **B-AUDITED-CARRIER**: Should be behaviorally identical (same source). FIDELITY check enforces this.
- **No identity confusion**.

### 12.5 Insensitive Controls
- **NC-KNOWN-NEGATIVE**: Three distinct categories with specific expected reason strings. A broken support inference will leak as wrong reason or EXECUTABLE. Sensitive.
- **B-LITERAL-KERNEL**: If confidence gate works, 0/15 success. If broken, >0 success. Sensitive.
- **B-AUDITED-CARRIER**: If promoted kernel diverges, FIDELITY catches it. Sensitive.

### 12.6 Unbound Mutable Artifacts
All mutable local dependencies enumerated in `freeze_artifacts`:
- `src/spider/kernel.py` (promotion target)
- `src/spider/models.py`, `src/spider/registry.py` (kernel dependencies)
- `scripts/finalize_lane.py`, `scripts/research2_contract.py` (promotion workflow)
- `harness/substrate.py`, `harness/run_experiment.py` (experiment execution)
All are repository-relative paths. The freezer will hash them.

**All six freeze_eligibility checks: PASS.**

---

**This preregistration is frozen upon creation of `freeze.json`. No outcome-bearing measurements may be inspected before freeze. The decision rule above is binding.**