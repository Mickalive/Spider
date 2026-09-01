# EXP-GRAPH-33528827169 — Preregistration

## Experiment Identity

- **ID:** EXP-GRAPH-33528827169
- **Lane:** graph
- **Claim:** C-PARAM-INHERIT — "Mechanisms parameterize to unseen identifiers"
- **Status at design:** EXPERIMENTAL (no direct end-to-end evidence in Research 2.0 codebase)

## Scientific Question

Does the SpiderKernel's parameterized mechanism resolution work end-to-end on a real website?

Specifically: can a mechanism with `${id}` parameter slots, distilled from execution on resource A, be resolved, bound, and executed on resource B (a different identifier) — producing correct bound actions, successful HTTP execution, and verified postconditions?

## Background and Motivation

### What pre2 established
- Fragment reuse reached 69.6% on scripted QUOTES/BOOKS sites (G-H1)
- Blind composition worked on unseen tasks via content-addressed retrieval (G-H2)
- Depth scaling held to depth 4-5 on QUOTES chains (G-H5)
- Generalization to BOOKS inventory failed (G-H6 — bounded negative)

### What is NOT established
- None of the above tested the current Research 2.0 kernel implementation
- The kernel's `_bind()` function is unit-tested in isolation (test_kernel.py) but never executed against a live site
- No experiment has tested whether `resolve() → _bind() → execute → verify()` works end-to-end
- C-PARAM-INHERIT has zero direct evidence in the current codebase

### Why this matters
Parameterized inheritance is the foundational capability for all Graph product claims. If the kernel can't do parameterized resolution on a trivial case, no higher-order experiment (fragment reuse, pagination, cross-task transfer) is testable.

## Hypothesis

A parameterized mechanism with `parameter_slots=["id"]` and `action_template={"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/${id}"}` will:

1. Resolve as EXECUTABLE when `resolve("fetch", context, {"id": <unseen_id>})` is called
2. Produce a correct `bound_action` with the `${id}` slot substituted
3. Execute successfully via HTTP (status 200)
4. Pass `verify()` against the observed post-state

A literal (non-parameterized) mechanism for `/posts/1` will return UNKNOWN for any other resource ID.

## Falsification Criteria

The hypothesis is **FALSIFIED** if any of:

1. `resolve()` returns `UNKNOWN` or `EXPLORE` for a parameterized mechanism when all required slots are provided in `params`
2. `bound_action` contains unsubstituted `${id}` or incorrect URL
3. HTTP execution returns non-200 status
4. `verify()` returns `False` despite successful HTTP execution with valid response
5. The literal baseline returns `EXECUTABLE` for an unseen resource ID (indicates parameter slot checking is broken)

## Experimental Design

### Test Site
- **URL:** `https://jsonplaceholder.typicode.com`
- **Rationale:** Stable public API, no auth required, deterministic responses, no session/drift/DOM complexity
- **Risk:** Site simplicity may overestimate kernel capability for real web navigation. This is acknowledged as a validity limitation — this experiment tests the kernel pipeline, not real-world web complexity.

### Resources Tested
- **Training resource:** `/posts/1` (used to create the literal baseline mechanism)
- **Test resources:** `/posts/2`, `/posts/3`, `/posts/4`, `/posts/5`, `/posts/6` (all unseen by the mechanism)

### Conditions

| Condition | Mechanism Type | Params | Expected Resolution |
|-----------|---------------|--------|-------------------|
| cold | None registered | {id: 2} | UNKNOWN |
| literal-original | Literal (no slots) | {id: 1} | EXECUTABLE |
| literal-unseen | Literal (no slots) | {id: 2} | UNKNOWN |
| param-seen | Parameterized | {id: 1} | EXECUTABLE |
| param-unseen-1 | Parameterized | {id: 2} | EXECUTABLE |
| param-unseen-2 | Parameterized | {id: 3} | EXECUTABLE |
| param-unseen-3 | Parameterized | {id: 4} | EXECUTABLE |
| param-unseen-4 | Parameterized | {id: 5} | EXECUTABLE |
| param-unseen-5 | Parameterized | {id: 6} | EXECUTABLE |
| guard-blocked | Parameterized + guard | {id: 2} (wrong context) | UNKNOWN |

### Measurements

For each EXECUTABLE resolution:
1. `bound_action` correctness (exact URL match)
2. HTTP execution status code
3. Response JSON structure (must contain `userId`, `id`, `title`, `body`)
4. `verify()` result

### Decision Rule

**PARAM-INHERIT-SUBSTRATE-VALID** if ALL of:
- Cold baseline → UNKNOWN ✓
- Literal-original → EXECUTABLE ✓
- Literal-unseen → UNKNOWN ✓
- All 5 param-unseen → EXECUTABLE with correct bound_action ✓
- All 5 HTTP executions → 200 with valid JSON ✓
- All 5 verify() → True ✓
- Guard-blocked → UNKNOWN ✓

**PARAM-INHERIT-SUBSTRATE-BROKEN** otherwise.

## Controls Summary

| Control | Purpose | Type |
|---------|---------|------|
| Cold (no mechanism) | Verify kernel abstains when no knowledge exists | Null |
| Literal-original | Verify basic mechanism resolution works | Positive |
| Literal-unseen | Verify literal mechanisms don't generalize | Null |
| Guard-blocked | Verify applicability guards are enforced | Null |
| Parameterized on original | Verify parameterized mechanisms work on seen data | Positive |
| Parameterized on unseen (×5) | Core test of parameterized inheritance | Experimental |

## Validity Threats

1. **Site simplicity:** JSONPlaceholder is a static API, not a dynamic web app. Success here does not guarantee success on real websites with DOM, auth, session state. **Mitigation:** This is explicitly a substrate validation, not a generalization claim. Real-site testing is the next experiment tier.

2. **API determinism:** Responses are deterministic. No drift, no staleness. **Mitigation:** Accepted for this gate. Freshness/staleness is claim C-FRESHNESS, not C-PARAM-INHERIT.

3. **Single model/API call:** No LLM involvement. This tests the kernel code path, not LLM-driven mechanism discovery. **Mitigation:** C-PARAM-INHERIT's gate is "learn on resource A, succeed on never-observed B." This experiment tests the "succeed on B" half. The "learn on A" half (mechanism distillation from LLM-driven exploration) is a separate experiment.

4. **Small N:** 5 unseen resources. **Mitigation:** Sufficient for a substrate gate. Statistical power is not the goal — binary pass/fail of the kernel pipeline is.

## Consequences

### If PARAM-INHERIT-SUBSTRATE-VALID
- The kernel pipeline is a functional foundation for parameterized inheritance
- Next experiment: test parameterized fragment mechanisms on real web navigation (QUOTES-style pagination with different search terms)
- C-PARAM-INHERIT advances from EXPERIMENTAL to EXPERIMENTAL-with-substrate-validated

### If PARAM-INHERIT-SUBSTRATE-BROKEN
- Identify the exact failure mode (resolution, binding, execution, or verification)
- Write a targeted fix in kernel.py
- Re-run this experiment as a regression test
- C-PARAM-INHERIT remains BLOCKED until the substrate is repaired

## Preregistration Timestamp

This design was created during the DESIGN phase of EXP-GRAPH-33528827169.
No outcome data has been inspected. All measurements are deferred to EXECUTE.
