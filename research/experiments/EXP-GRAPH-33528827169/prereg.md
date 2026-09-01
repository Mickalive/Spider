# EXP-GRAPH-33528827169 — Preregistration

## Experiment Identity

- **ID:** EXP-GRAPH-33528827169
- **Lane:** graph
- **Claim:** C-PARAM-INHERIT — "Mechanisms parameterize to unseen identifiers"
- **Status at design:** EXPERIMENTAL (no direct end-to-end evidence in Research 2.0 codebase)
- **Request hash:** fc823b0ef78b1a62c61007c0f4234738351c955bf2a39504bc4a2693702e19ce

## Scientific Question

Does SpiderKernel's parameterized mechanism resolution work end-to-end on a real HTTP endpoint?

Can a mechanism with `${id}` parameter slots, registered in the MechanismRegistry, be resolved via `resolve()`, bound via `_bind()`, executed over HTTP, and verified via `verify()` against actual response state — on resource identifiers never seen during mechanism registration?

## Background and Motivation

### What pre2 established (from SPIDER_CODEX_ULTIME.md)
- Fragment reuse reached 69.6% on scripted QUOTES/BOOKS sites (G-H1)
- Blind composition worked on unseen tasks via content-addressed retrieval (G-H2)
- Depth scaling held to depth 4-5 on QUOTES chains (G-H5)
- Generalization to BOOKS inventory failed (G-H6 — bounded negative)

### What Research 2.0 has NOT established
- None of the above tested the current Research 2.0 kernel implementation
- The kernel's `_bind()` function has unit tests in `test_kernel.py` but only for string substitution and guard enforcement — never executed against a live endpoint
- `resolve()` has never been tested end-to-end with HTTP execution and `verify()` against real response state
- C-PARAM-INHERIT has zero direct evidence in the current codebase

### Why this matters
Parameterized inheritance is the foundational capability for all Graph product claims. The claim "learn on resource A, succeed on never-observed B" requires the kernel pipeline to work end-to-end. If it fails on a trivial API, no higher-order experiment (fragment reuse, pagination, cross-task transfer) is testable.

## Hypothesis

A parameterized mechanism with:
- `parameter_slots=["id"]`
- `action_template={"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/${id}"}`
- `postconditions={"status": 200, "has_keys": ["userId", "id", "title", "body"]}`
- `confidence=0.95`

will:

1. Resolve as EXECUTABLE when `resolve("fetch", context, {"id": <unseen_id>})` is called
2. Produce a correct `bound_action` with the `${id}` slot substituted to the actual parameter value
3. Execute successfully via HTTP (status 200 with valid JSON)
4. Pass `verify()` against the observed post-state

Additionally:
- A literal (non-parameterized) mechanism will NOT generalize to unseen resource IDs
- A parameterized mechanism with missing required params will NOT resolve
- A parameterized mechanism with blocking applicability_guards will NOT resolve

## Kernel Code Path Being Tested

From `src/spider/kernel.py`, the `resolve()` method:

1. Iterates `self.registry.all()` looking for mechanisms matching `intent`
2. Checks `m.preconditions` against `context` via `_matches()`
3. Checks `m.applicability_guards` against `context` via `_matches()`
4. Computes `required_slots = set(m.parameter_slots) | _template_slots(m.action_template)`
5. Skips mechanism if any `slot not in params`
6. Sorts candidates by confidence (descending)
7. Returns EXECUTABLE with `bound_action=_bind(best.action_template, params)`

The `_bind()` function:
- For string `"${id}"` (full match): returns `params["id"]` directly (type-preserving)
- For string `"prefix/${id}/suffix"` (partial match): returns substituted string
- Recursively processes dicts and lists

This experiment tests the complete path from step 1 through `_bind()` return, plus HTTP execution and `verify()`.

## Falsification Criteria

The hypothesis is **FALSIFIED** if ANY of:

1. `resolve()` returns `UNKNOWN` or `EXPLORE` for a parameterized mechanism when all required slots ARE present in `params` — the kernel's slot-checking logic is broken
2. `bound_action` contains unsubstituted `${id}` literal or incorrect URL — `_bind()` failed
3. HTTP execution returns non-200 for a valid resource (posts/1 through posts/6 are stable) — bound_action is wrong
4. `verify()` returns `False` despite 200 response with valid JSON containing userId/id/title/body — verify() logic is broken
5. A literal mechanism returns `EXECUTABLE` for resource ID 2 — parameter slot enforcement is absent (mechanism should only match ID 1)
6. A parameterized mechanism with empty params returns `EXECUTABLE` — required_slots check is bypassed
7. A parameterized mechanism with blocking guards returns `EXECUTABLE` — applicability_guards are not enforced

## Experimental Design

### Test Endpoint
- **URL:** `https://jsonplaceholder.typicode.com`
- **Resources:** `/posts/1` through `/posts/6`
- **Rationale:** Stable public REST API, no auth, deterministic JSON responses, no session/drift/DOM complexity. This is a substrate validation — testing the kernel pipeline, not real-world web complexity.

### Resources
- **Training resource:** `/posts/1` (used to create the literal baseline mechanism)
- **Test resources:** `/posts/2`, `/posts/3`, `/posts/4`, `/posts/5`, `/posts/6` (all unseen by the mechanism)

### Mechanisms Registered

| Mechanism ID | Type | parameter_slots | action_template | applicability_guards |
|---|---|---|---|---|
| `literal-fetch-posts-1` | Literal | [] | {method: GET, url: https://jsonplaceholder.typicode.com/posts/1} | {} |
| `param-fetch-posts` | Parameterized | ["id"] | {method: GET, url: https://jsonplaceholder.typicode.com/posts/${id}} | {} |
| `param-fetch-posts-guarded` | Parameterized | ["id"] | {method: GET, url: https://jsonplaceholder.typicode.com/posts/${id}} | {auth_required: true} |

All mechanisms: intent="fetch", confidence=0.95, postconditions={status: 200, has_keys: [userId, id, title, body]}

### Conditions Matrix

| # | Condition | Mechanism | Context | Params | Expected Resolution | Expected URL |
|---|---|---|---|---|---|---|
| 1 | cold | none registered | {base_url: ...} | {id: 2} | UNKNOWN | — |
| 2 | literal-original | literal | {base_url: ...} | {id: 1} | EXECUTABLE | .../posts/1 |
| 3 | literal-unseen | literal | {base_url: ...} | {id: 2} | UNKNOWN | — |
| 4 | missing-params | parameterized | {base_url: ...} | {} | UNKNOWN | — |
| 5 | param-original | parameterized | {base_url: ...} | {id: 1} | EXECUTABLE | .../posts/1 |
| 6 | param-unseen-1 | parameterized | {base_url: ...} | {id: 2} | EXECUTABLE | .../posts/2 |
| 7 | param-unseen-2 | parameterized | {base_url: ...} | {id: 3} | EXECUTABLE | .../posts/3 |
| 8 | param-unseen-3 | parameterized | {base_url: ...} | {id: 4} | EXECUTABLE | .../posts/4 |
| 9 | param-unseen-4 | parameterized | {base_url: ...} | {id: 5} | EXECUTABLE | .../posts/5 |
| 10 | param-unseen-5 | parameterized | {base_url: ...} | {id: 6} | EXECUTABLE | .../posts/6 |
| 11 | guard-blocked | parameterized-guarded | {base_url: ..., auth_required: false} | {id: 2} | UNKNOWN | — |

### Measurements (for each EXECUTABLE resolution)

1. `bound_action` correctness (exact URL match against expected_url)
2. HTTP execution status code (must be 200)
3. Response JSON structure (must contain userId, id, title, body keys)
4. `verify()` result (must be True)
5. Resolution reason string (for debugging)

### Execution Order

Conditions executed in order 1→11. Each condition is independent (fresh kernel instance with same registry state). No cross-condition contamination.

## Decision Rule

**PARAM-INHERIT-SUBSTRATE-VALID** if ALL of:
- Condition 1 (cold) → UNKNOWN ✓
- Condition 2 (literal-original) → EXECUTABLE with correct URL ✓
- Condition 3 (literal-unseen) → UNKNOWN ✓
- Condition 4 (missing-params) → UNKNOWN ✓
- Condition 5 (param-original) → EXECUTABLE with correct URL ✓
- Conditions 6-10 (param-unseen ×5) → EXECUTABLE with correct URL ✓
- Condition 11 (guard-blocked) → UNKNOWN ✓
- For all EXECUTABLE conditions: HTTP 200 + valid JSON + verify()=True ✓

**PARAM-INHERIT-SUBSTRATE-BROKEN** otherwise. The report must identify the exact failing condition and failure mode (resolution, binding, execution, or verification).

## Controls Summary

| Control | Condition # | Purpose | Type |
|---|---|---|---|
| Cold (no mechanism) | 1 | Kernel abstains when no knowledge exists | Null |
| Literal on original | 2 | Basic mechanism resolution works | Positive |
| Literal on unseen | 3 | Literal mechanisms don't generalize | Null |
| Missing params | 4 | Parameter completeness is enforced | Null |
| Param on original | 5 | Parameterized mechanism works on seen data | Positive |
| Param on unseen (×5) | 6-10 | Core test of parameterized inheritance | Experimental |
| Guard-blocked | 11 | Applicability guards enforced independently of params | Null |

## Validity Threats

1. **Site simplicity:** JSONPlaceholder is a static REST API, not a dynamic web app with DOM, auth, or session state. **Mitigation:** This is explicitly a substrate validation, not a generalization claim. Success here is necessary but not sufficient for real-web parameterized inheritance. Real-site testing is the next experiment tier.

2. **API determinism:** Responses are deterministic. No drift, no staleness. **Mitigation:** Accepted for this gate. Freshness/staleness is claim C-FRESHNESS, not C-PARAM-INHERIT.

3. **No LLM involvement:** No model calls. This tests the kernel code path, not LLM-driven mechanism discovery. **Mitigation:** C-PARAM-INHERIT's gate is "learn on resource A, succeed on never-observed B." This experiment tests the "succeed on B" half. The "learn on A" half (mechanism distillation from LLM-driven exploration) is a separate experiment.

4. **Small N:** 5 unseen resources. **Mitigation:** Sufficient for a substrate gate. Statistical power is not the goal — binary pass/fail of the kernel pipeline is. All 5 must pass for VALID verdict.

5. **Type coercion in _bind():** When `action_template` contains `"${id}"` as a full-match string, `_bind()` returns the parameter value directly (preserving its Python type, e.g., int). When embedded in a URL string, it returns a substituted string. The experiment uses the URL-embedded form, so this edge case does not affect results. **Mitigation:** Documented; type-preservation edge case is a separate concern.

6. **Previous design failure:** The previous design attempt failed with exit code 66 (DESIGN_FAILURE). The failure was in the stage execution, not the scientific design. The refined design addresses this by being more explicit about conditions and measurements.

## Consequences

### If PARAM-INHERIT-SUBSTRATE-VALID
- The kernel pipeline is a validated functional foundation for parameterized inheritance
- Next experiment: test parameterized fragment mechanisms on real web navigation (e.g., QUOTES-style pagination with different page numbers, BOOKS-style category browsing with different categories)
- C-PARAM-INHERIT claim status advances: the "succeed on B" half of the gate is passed
- Product can begin registering parameterized mechanisms for external-agent consumption testing

### If PARAM-INHERIT-SUBSTRATE-BROKEN
- Identify the exact failure mode from the condition matrix:
  - Resolution failure → bug in `resolve()` slot-checking or preconditions logic
  - Binding failure → bug in `_bind()` substitution
  - Execution failure → bound_action is incorrect
  - Verification failure → bug in `verify()` postcondition checking
- Write a targeted fix in `kernel.py`
- Re-run this experiment as a regression test
- C-PARAM-INHERIT remains BLOCKED until the substrate is repaired

## Preregistration Timestamp

This design was created during the DESIGN phase of EXP-GRAPH-33528827169.
No outcome data has been inspected. All measurements are deferred to EXECUTE.
The spec and prereg were refined from an earlier design attempt (failure.json exit code 66) to strengthen baselines and tighten falsification criteria.
