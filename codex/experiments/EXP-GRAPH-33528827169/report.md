# EXP-GRAPH-33528827169 — Execution Report

## Experiment Identity

- **ID:** EXP-GRAPH-33528827169
- **Lane:** graph
- **Claim:** C-PARAM-INHERIT — "Mechanisms parameterize to unseen identifiers"
- **Status:** COMPLETE
- **Outcome:** MIXED

## Verdict

**PARAM-INHERIT-SUBSTRATE-BROKEN** (per frozen decision rule: 10/11 conditions passing, 1 failing)

The parameterized mechanism pipeline works correctly end-to-end. The failure is in the literal mechanism baseline: it matches unseen resources, violating the spec's falsification criterion #5. This reveals a design clarification about how the kernel enforces parameter constraints.

## Summary

| Condition | Expected | Observed | Pass |
|---|---|---|---|
| cold | UNKNOWN | UNKNOWN | ✅ |
| literal-original | EXECUTABLE | EXECUTABLE | ✅ |
| **literal-unseen** | **UNKNOWN** | **EXECUTABLE** | ❌ |
| missing-params | UNKNOWN | UNKNOWN | ✅ |
| param-original | EXECUTABLE | EXECUTABLE | ✅ |
| param-unseen-1 (id=2) | EXECUTABLE | EXECUTABLE | ✅ |
| param-unseen-2 (id=3) | EXECUTABLE | EXECUTABLE | ✅ |
| param-unseen-3 (id=4) | EXECUTABLE | EXECUTABLE | ✅ |
| param-unseen-4 (id=5) | EXECUTABLE | EXECUTABLE | ✅ |
| param-unseen-5 (id=6) | EXECUTABLE | EXECUTABLE | ✅ |
| guard-blocked | UNKNOWN | UNKNOWN | ✅ |

## Key Findings

### 1. Parameterized Pipeline: Validated ✅

All 5 unseen resource IDs (2–6) resolved correctly through the complete pipeline:

1. **resolve()** returned EXECUTABLE for parameterized mechanism `param-fetch-posts`
2. **_bind()** correctly substituted `${id}` in the action_template URL
3. **HTTP execution** returned status 200 with valid JSON containing `userId`, `id`, `title`, `body`
4. **verify()** returned True against observed post-state

The `resolve() → _bind() → execute → verify()` pipeline is a functional substrate for parameterized inheritance.

### 2. Literal Mechanism Universal Matching: The Failure ❌

The literal mechanism (no `parameter_slots`, action_template is a fixed URL `.../posts/1`) returned EXECUTABLE for resource ID 2, with bound_action url still pointing to `/posts/1`.

**Root Cause (from `kernel.py` line 104–106):**

```python
required_slots = set(m.parameter_slots) | _template_slots(m.action_template)
if any(slot not in params for slot in required_slots):
    continue
```

For the literal mechanism:
- `m.parameter_slots = []`
- `_template_slots(action_template) = set()` (no `${}` templates in a literal URL)
- `required_slots = set()`
- `any(slot not in params for slot in set())` → `False` (empty iteration)

The required_slots check is **presence-based**, not **value-based**. A mechanism with zero required slots has no constraints and matches any params for its intent and preconditions. The literal mechanism is therefore a universal "catch-all" for the `fetch` intent with matching preconditions.

### 3. Guards and Completeness: Enforced ✅

- Missing-params condition correctly returned UNKNOWN (required slot `id` absent)
- Guard-blocked condition correctly returned UNKNOWN (auth_required guard mismatch)
- These work independently of the parameter binding pipeline

## Interpretation

The frozen decision rule requires ALL 11 conditions to pass for PARAM-INHERIT-SUBSTRATE-VALID. Condition 3 (literal-unseen) fails, so the verdict is BROKEN per the spec.

However, the scientific substance is more nuanced:

1. **The parameterized mechanism pipeline is validated.** All 5 unseen-resource tests passed. The kernel correctly resolves parameterized mechanisms, binds slots, executes HTTP, and verifies postconditions. This is the core capability under test.

2. **The literal-unseen failure reveals a design clarification, not a kernel bug.** The kernel's parameter slot enforcement is presence-based: "are all required slots provided?" It does not enforce value constraints: "do the slot values match expected resources?" This is correct for parameterized mechanisms (the template handles resource substitution), but means literal mechanisms (zero required slots) are universally applicable.

3. **The spec's falsification criterion #5 assumed value-based matching.** The kernel was designed with presence-based matching. This is a spec-kernel design mismatch that needs DIRECTOR resolution.

## Consequences for C-PARAM-INHERIT

- **Positive:** The parameterized pipeline works. The "succeed on never-observed B" half of the gate is passed for parameterized mechanisms.
- **Blocker:** The literal mechanism's universal matching means the kernel cannot distinguish between "this mechanism was designed for this specific resource" and "this mechanism can handle any resource with the right slots." Whether this is acceptable depends on the intended use case.
- **Next decision needed:** DIRECTOR must determine whether the literal-unseen failure is:
  - (a) A genuine bug requiring a kernel fix (add value-based matching for literal mechanisms), or
  - (b) An acceptable design choice (literal mechanisms are intentionally universal), requiring a spec update.

## Validity Threats

1. **Substrate simplicity:** JSONPlaceholder is a static REST API. Success here is necessary but not sufficient for real-web parameterized inheritance. Real-site testing is the next experiment tier.
2. **No LLM involvement:** This tests kernel code paths, not LLM-driven mechanism discovery. The "learn on A" half of C-PARAM-INHERIT is untested.
3. **Small N:** 5 unseen resources. Sufficient for a substrate gate; statistical power is not the goal.
4. **Previous execution failure:** The prior attempt (failure.json exit code 66) was a validation failure (missing status field), not a scientific failure. The current run completes the measurement.
