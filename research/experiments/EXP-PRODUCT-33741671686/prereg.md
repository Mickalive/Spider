# EXP-PRODUCT-33741671686 — Preregistration

## Experiment Identity

- **ID:** EXP-PRODUCT-33741671686
- **Lane:** product
- **Claim:** C-PARAM-INHERIT — "Mechanisms parameterize to unseen identifiers"
- **Parent:** EXP-PRODUCT-33528829801 (SURVIVES at single-parameter synthetic POC level)
- **Status at design:** EXPERIMENTAL (single-parameter POC survived; multi-parameter untested)
- **Request hash:** d28509c479ff5e4daaa8a41130f06d312f6e1b0ec94d28a62d6cf353cae4b26e

## Scientific Question

Does parameter induction generalize to multi-parameter mechanisms with distinct slot naming across path, body, and headers fields?

## Background and Motivation

### What the parent experiment (EXP-PRODUCT-33528829801) established

- `distill_parameterized()` with `_extract_varying_values()` correctly induces one parameter slot for isomorphic action paths sharing common prefix/suffix (e.g., `/api/items/A`, `/api/items/B`, `/api/items/C` → `/api/items/${id}`)
- Parameterized mechanism resolves to EXECUTABLE with correct `bound_action` for all 10 unseen single-char identifiers (10/10)
- Literal mechanism replay fails on all unseen identifiers (0/10 EXECUTABLE)
- Positive and null controls pass

### What the parent audit identified as the critical limitation

The audit (V_MULTI_FIELD_COLLISION) found:

> `_extract_varying_values()` hardcodes `param_name='id'` for every varying leaf. With >1 varying leaf (e.g., path and headers.Authorization both varying) the mechanism collapses distinct logical parameters into one slot `'id'` → `bound_action` forces `token == resource_id`. Requires distinct slot naming per path before claiming multi-parameter induction.

This is the exact gate this experiment addresses.

### What is NOT established

- Whether distinct slot names can be induced from structural position (path vs body vs headers) when values are structurally identical
- Whether `_bind()` correctly substitutes multiple distinct slots in a single resolution
- Whether slot completeness enforcement works for multi-slot mechanisms
- Whether the heuristic approach generalizes beyond prefix/suffix variation

## Hypothesis

Extending `_extract_varying_values()` to produce distinct parameter slot names per varying field enables multi-parameter inheritance.

Concretely, given training observations:

| resource_id | path | body.title | headers.Authorization |
|---|---|---|---|
| A | `/api/items/A` | `Title A` | `Bearer token-A` |
| B | `/api/items/B` | `Title B` | `Bearer token-B` |
| C | `/api/items/C` | `Title C` | `Bearer token-C` |

The extended `distill_parameterized()` will produce:

```json
{
  "parameter_slots": ["resource_id", "title", "token"],
  "action_template": {
    "method": "POST",
    "path": "/api/items/${resource_id}",
    "body": {"title": "${title}"},
    "headers": {"Authorization": "Bearer ${token}"}
  }
}
```

And this mechanism will resolve EXECUTABLE for unseen combinations where all three fields vary simultaneously, with correct `bound_action` for each slot independently.

## Kernel Code Path Being Tested

### Current state (frozen kernel.py)

`_extract_varying_values()` does not exist in the current `src/spider/kernel.py`. The parent experiment added it during execution. The current kernel's `distill()` method creates only literal mechanisms with no parameter induction.

### Required extension (within Product lane code roots: src/spider/)

1. Add `_extract_varying_values(observations: list[Observation]) -> dict` that:
   - Collects all values at each structural position across observations
   - Identifies positions where values differ across observations
   - Assigns DISTINCT parameter slot names based on structural path (e.g., `resource_id` for path leaf, `title` for body.title, `token` for headers.Authorization)
   - Returns a mapping from structural position to slot name

2. Add `distill_parameterized(observations, mechanism_id) -> Mechanism` that:
   - Calls `_extract_varying_values()` to identify varying fields
   - Creates an `action_template` with `${slot_name}` placeholders at varying positions
   - Sets `parameter_slots` to the list of distinct slot names
   - Sets `confidence=0.9` (matching parent experiment convention)

### What is NOT changed

- `resolve()` — unchanged; its `required_slots` check already works for arbitrary slot lists
- `_bind()` — unchanged; its recursive dict/list/string substitution already handles multiple `${...}` patterns
- `_template_slots()` — unchanged; already finds all `${...}` patterns in a template
- `Mechanism` model — unchanged; `parameter_slots: list[str]` already supports multiple slots

The experiment tests whether the INDUCTION (naming) is the binding constraint, not whether the EXECUTION pipeline can handle multiple slots.

## Experimental Design

### Training Observations

3 observations for intent `"create-item"` with state `{"authenticated": true, "role": "admin"}`:

| Obs | action.path | action.body.title | action.headers.Authorization |
|---|---|---|---|
| train-A | `/api/items/A` | `Title A` | `Bearer token-A` |
| train-B | `/api/items/B` | `Title B` | `Bearer token-B` |
| train-C | `/api/items/C` | `Title C` | `Bearer token-C` |

All observations share: `method=POST`, `state={authenticated: true, role: admin}`, `next_state={created: true}`, `success=True`.

### Test Conditions

| # | Condition | Description | Params | Expected Resolution | Expected bound_action |
|---|---|---|---|---|---|
| 1 | cold | No mechanism registered | {resource_id: X, title: Title X, token: token-X} | UNKNOWN | — |
| 2 | positive-control | Multi-slot on seen resource A | {resource_id: A, title: Title A, token: token-A} | EXECUTABLE | path=/api/items/A, body.title=Title A, headers.Authorization=Bearer token-A |
| 3 | unseen-X | Multi-slot on unseen combination X | {resource_id: X, title: Title X, token: token-X} | EXECUTABLE | path=/api/items/X, body.title=Title X, headers.Authorization=Bearer token-X |
| 4 | unseen-Y | Multi-slot on unseen combination Y | {resource_id: Y, title: Title Y, token: token-Y} | EXECUTABLE | path=/api/items/Y, body.title=Title Y, headers.Authorization=Bearer token-Y |
| 5 | unseen-Z | Multi-slot on unseen combination Z | {resource_id: Z, title: Title Z, token: token-Z} | EXECUTABLE | path=/api/items/Z, body.title=Title Z, headers.Authorization=Bearer token-Z |
| 6 | partial-missing-title | Multi-slot with title missing | {resource_id: X, token: token-X} | UNKNOWN | — |
| 7 | partial-missing-token | Multi-slot with token missing | {resource_id: X, title: Title X} | UNKNOWN | — |
| 8 | null-control | Multi-slot with wrong preconditions | {resource_id: A, title: Title A, token: token-A}, context.authenticated=False | UNKNOWN | — |
| 9 | single-slot-baseline | Single-slot mechanism on multi-param data | {id: X} | EXECUTABLE | path=/api/items/X, body=literal (Title A), headers=literal (Bearer token-A) |
| 10 | literal-replay | Literal mechanism on unseen | {} | EXECUTABLE | path=/api/items/A (training resource), body=literal, headers=literal |

### Measurements (for each EXECUTABLE resolution)

1. `bound_action.path` correctness (exact match)
2. `bound_action.body.title` correctness (exact match)
3. `bound_action.headers.Authorization` correctness (exact match)
4. `parameter_slots` count and names (must be >= 3 distinct names)
5. Resolution reason string (for debugging)

### Execution Order

Conditions executed in order 1→10. Each condition uses a fresh registry (isolated). No cross-condition contamination.

## Decision Rule

**C-PARAM-INHERIT-ADVANCES** if ALL of:
- Condition 1 (cold) → UNKNOWN ✓
- Condition 2 (positive-control) → EXECUTABLE with all 3 fields correct ✓
- Conditions 3-5 (unseen-X/Y/Z) → EXECUTABLE with all 3 fields correct ✓
- Condition 6 (partial-missing-title) → UNKNOWN ✓
- Condition 7 (partial-missing-token) → UNKNOWN ✓
- Condition 8 (null-control) → UNKNOWN ✓
- `parameter_slots` has >= 3 distinct names ✓

**C-PARAM-INHERIT-BLOCKED** otherwise. The report must identify the exact failing condition and whether the failure is in induction (slot naming), binding (slot substitution), or enforcement (slot completeness).

## Controls Summary

| Control | Condition # | Purpose | Type |
|---|---|---|---|
| Cold (no mechanism) | 1 | Kernel abstains when no knowledge exists | Null |
| Positive control (seen) | 2 | Extended mechanism works on training data | Positive |
| Unseen full-combination (×3) | 3-5 | Core test: multi-parameter inheritance | Experimental |
| Partial-missing (×2) | 6-7 | Slot completeness enforcement for multi-slot | Null |
| Null control (guard) | 8 | Precondition guards work with multi-slot | Null |
| Single-slot baseline | 9 | Demonstrates parent limitation: single-slot can't parameterize body/headers | Baseline |
| Literal replay | 10 | Literal mechanisms are universal catch-all but incorrect for unseen | Baseline |

## Validity Threats

1. **Synthetic data with correlated variation:** All three varying fields (path, title, token) use the same base value (resource_id). A clever algorithm could detect this correlation and infer a single underlying parameter. **Mitigation:** The experiment tests whether the algorithm produces DISTINCT slots regardless of value correlation. The key is structural position, not value independence. If the algorithm collapses correlated-but-structurally-distinct fields, that IS the failure mode we want to detect.

2. **is_id_like regex match on all values:** The values A/B/C/X/Y/Z and Title A/Title X and token-A/token-X all match `^[A-Za-z0-9_\\-]+$`. The algorithm cannot distinguish them by value properties. **Mitigation:** This is intentional — it forces the algorithm to use structural position (path vs body vs headers) for naming, which is the actual capability under test.

3. **Single code change scope:** Only `_extract_varying_values()` and `distill_parameterized()` are modified. If the failure is in `resolve()`, `_bind()`, or `_template_slots()`, those are pre-existing bugs, not induction failures. **Mitigation:** The experiment instrument separately reports induction results (slot names produced) vs execution results (resolution + binding), so failures can be attributed.

4. **Small N:** 3 training observations, 3 unseen test combinations. **Mitigation:** Sufficient for a mechanism gate. Statistical power is not the goal — correct slot naming and binding on a representative multi-parameter pattern is.

5. **Single-value-type variation:** All varying values are short alphanumeric strings. URL paths, timestamps, JSON, or arbitrary strings are not tested. **Mitigation:** Accepted for this gate. Non-identifier values are a separate experiment (identified as unknown in parent handoff).

6. **No real-browser observations:** All observations are synthetic. The parent handoff identifies real-browser testing as a future gate. **Mitigation:** This experiment stays within the synthetic-data dependency. Real-browser testing requires the runtime substrate (not yet available for multi-parameter observations).

## Consequences

### If C-PARAM-INHERIT-ADVANCES

- Multi-parameter inheritance is viable at the kernel level
- C-PARAM-INHERIT claim ceiling raises from single-parameter to multi-parameter synthetic POC
- Product lane can proceed to test parameterized mechanisms on real-browser observations with multiple varying fields
- Next experiment: test parameterized mechanisms with non-correlated variation (different value types per field) or with noisy/real-browser observations
- Promotion readiness increases but remains gated on real-browser and cost measurements

### If C-PARAM-INHERIT-BLOCKED

- The `_extract_varying_values()` heuristic approach cannot produce distinct slot names from structural position alone
- C-PARAM-INHERIT is blocked at single-parameter until a fundamentally different induction approach is found
- Product architecture must reconsider: either (a) invest in LLM-based slot naming, (b) require human-authored parameter annotations, or (c) limit parameterized inheritance to single-parameter mechanisms
- The single-parameter POC result remains valid but the generalization path is closed at this level

## Preregistration Timestamp

This design was created during the DESIGN phase of EXP-PRODUCT-33741671686.
No outcome data has been inspected. All measurements are deferred to EXECUTE.
The design follows the parent handoff's recommended action and preserves all inherited established/rejected/unknown/do_not_assume distinctions.
