# EXP-PRODUCT-33741671686 — Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-33741671686
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT — "Mechanisms parameterize to unseen identifiers"
- **Date**: 2026-09-03
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-PRODUCT-33528829801 (C-PARAM-INHERIT SURVIVES at single-parameter synthetic POC)

## 2. Scientific Question

Does parameter induction generalize to multi-parameter mechanisms with multiple distinct varying fields (path + body + headers), each receiving a distinct slot name, such that the induced mechanism resolves EXECUTABLE with correct bound_action for unseen multi-parameter combinations?

## 3. Background and Motivation

### What the parent experiment established (EXP-PRODUCT-33528829801)

- `distill_parameterized()` with `_extract_varying_values()` correctly induces one parameter slot for isomorphic action paths sharing common prefix/suffix (e.g., `/api/items/A`, `/api/items/B`, `/api/items/C` → `/api/items/${id}`)
- Parameterized mechanism resolves EXECUTABLE with correct bound_action for all 10 unseen single-char identifiers (D–M)
- Literal mechanism replay fails on all unseen identifiers (0/10 EXECUTABLE)
- Positive control passes: seen identifier resolves correctly
- Null control passes: mismatched preconditions → UNKNOWN

### What the audit identified as required fixes

The audit from EXP-PRODUCT-33528829801 explicitly identified:

> "Fix multi-field parameterization collision: `_extract_varying_values()` hardcodes `param_name='id'` for every varying leaf. With >1 varying leaf (e.g., path and headers.Authorization both varying) the mechanism collapses distinct logical parameters into one slot 'id' → bound_action forces token == resource_id. Requires distinct slot naming per path before claiming multi-parameter induction."

Additionally, the handoff carried forward:

> "Do not assume the kernel's `_extract_varying_values()` heuristic handles non-prefix/suffix variation — it uses longest common prefix/suffix with `is_id_like` regex that rejects spaces, slashes, punctuation"

### Why this matters

Real API patterns are multi-parameter:
- `POST /api/users/${user_id}` with body `{name: ${name}}`
- `PUT /api/posts/${post_id}` with body `{title: ${title}}` and headers `{X-Request-ID: ${request_id}}`

If the kernel cannot induce distinct parameter slots from multi-field variation, C-PARAM-INHERIT cannot advance beyond the single-parameter POC. Product cannot register multi-parameter mechanisms for external-agent consumption.

## 4. Hypothesis

A multi-parameter induction function that:
1. Compares field values across training observations
2. Identifies which fields vary (not hardcoded to one field)
3. Extracts common prefix/suffix per varying field
4. Names slots distinctly based on structural position (not hardcoded 'id')

will:

1. Induce multiple distinct parameter slots when multiple fields vary across observations
2. Produce correct bound_action substitution for all slots simultaneously
3. Resolve EXECUTABLE for unseen combinations of parameter values
4. Correctly abstain (UNKNOWN) when required slots are missing
5. Handle non-identifier values (URLs, timestamps) that the previous `is_id_like` regex rejected

## 5. Falsification Criteria

The hypothesis is **FALSIFIED** if ANY of:

1. The induction function produces zero parameter slots when multiple fields genuinely vary (slot_count < true_slot_count for any condition)
2. Slot naming collisions occur — two distinct varying fields receive the same slot name (e.g., both `path.user_id` and `body.user_id` become `${id}`)
3. Resolution fails (status != EXECUTABLE) for any unseen combination where all required slots are provided
4. `bound_action` contains unsubstituted `${...}` template literals for any resolved slot
5. The function crashes or produces non-deterministic output for any condition
6. The positive control fails — single-parameter induction no longer works after the multi-parameter extension (regression)

## 6. Experimental Conditions

### C1: Single-Path Parameter (Regression Baseline)

- **Purpose**: Verify single-parameter induction still works after multi-parameter extension
- **Training observations**: 3 observations with path-only variation (`/api/items/A`, `/api/items/B`, `/api/items/C`)
- **Unseen test**: 5 new identifiers (D–H)
- **Expected**: slot_count ≥ 1, unseen_resolution_rate ≥ 0.9, binding_accuracy ≥ 0.9

### C2: Path + Body (Core Multi-Parameter Test)

- **Purpose**: Test two-field parameter induction
- **Training observations**: 3 observations with path and body varying:
  - `POST /api/users/A` with body `{name: "Alice"}`
  - `POST /api/users/B` with body `{name: "Bob"}`
  - `POST /api/users/C` with body `{name: "Charlie"}`
- **Unseen test**: 5 combinations (user_id=D/E/F/G/H, name=Diana/Eve/Frank/Grace/Heidi)
- **Expected**: slot_count ≥ 2, distinct slot names, all 5 unseen resolve EXECUTABLE with correct bound_action

### C3: Path + Body + Headers (Maximum Complexity)

- **Purpose**: Test three-field parameter induction across different structural locations
- **Training observations**: 3 observations with path, body, and headers varying:
  - `POST /api/posts/A` with body `{title: "First"}`, headers `{X-Request-ID: "req-1"}`
  - `POST /api/posts/B` with body `{title: "Second"}`, headers `{X-Request-ID: "req-2"}`
  - `POST /api/posts/C` with body `{title: "Third"}`, headers `{X-Request-ID: "req-3"}`
- **Unseen test**: 5 combinations
- **Expected**: slot_count ≥ 3, distinct slot names, all 5 unseen resolve

### C4: Non-Identifier Values

- **Purpose**: Test that non-identifier values (URLs) are handled — the old `is_id_like` regex (`^[A-Za-z0-9_-]+$`) would reject URLs
- **Training observations**: 3 observations with body.callback_url varying (`https://site-a.com/hook`, etc.)
- **Unseen test**: 3 new URLs
- **Expected**: slot_count ≥ 1, all 3 unseen resolve with correct bound_action

### C5: Shared Slot Name Collision

- **Purpose**: Test that two fields with identical value patterns receive distinct slot names
- **Training observations**: 3 observations where path.id and body.user_id both vary with the same values (A, B, C)
- **Unseen test**: 3 combinations
- **Expected**: slot_count ≥ 2, slot names must be distinct (collision = falsification)

## 7. Controls

### Positive Control (C1 Regression)

- C1 conditions must replicate the parent experiment's results
- Single-parameter induction must still produce ≥ 1 slot with ≥ 90% unseen resolution
- This is the regression gate: if the multi-parameter extension breaks single-parameter, the extension is flawed

### Null Control

- Three training observations with completely random, non-shared action templates
- No common prefix/suffix, no varying fields in the same structural position
- Expected: zero parameter slots induced, or mechanism resolves to UNKNOWN
- This verifies the function does not hallucinate parameters when no pattern exists

### Negative Baselines

- **B_LITERAL**: Literal mechanism (no parameter_slots) must fail on all unseen multi-parameter combinations
- **B_COLD**: Cold exploration cost (simulated) for reference
- **B_RANDOM_INDUCTION**: Random slot assignment — tests whether structural naming outperforms chance

## 8. Decision Rule

**MULTI-PARAM-SURVIVES** if ALL of:
1. C1 single-parameter regression passes (slot_count ≥ 1, unseen_resolution_rate ≥ 0.9, binding_accuracy ≥ 0.9)
2. C2 multi-parameter induces ≥ 2 distinct slots and resolves all 5 unseen combos with correct bound_action
3. C3 three-parameter induces ≥ 3 distinct slots and resolves all 5 unseen combos
4. C4 non-identifier induces ≥ 1 slot and resolves all 3 unseen combos
5. C5 shared-slot induces ≥ 2 distinct slots (no collision) and resolves all 3 unseen combos
6. Null_control produces zero slots or UNKNOWN resolution
7. No crashes or non-deterministic output

**MULTI-PARAM-FALSIFIED** if any condition fails its expected_slot_count or resolution rate < 0.9.

**MEASUREMENT_INVALID** if the induction function is not implementable or crashes on all conditions.

## 9. Validity Threats

1. **Induction function implementation**: The multi-parameter induction function does not exist yet — it must be implemented during EXECUTE. If the implementation is flawed, the experiment tests the implementation bug, not the scientific question. **Mitigation**: The spec defines the function's interface and expected behavior independently of implementation; the audit can verify the implementation matches the spec.

2. **Synthetic-to-real gap**: All observations are synthetic with deterministic structure. Real browser observations would have noise, varying schemas, and multi-step actions. **Mitigation**: This is explicitly a POC gate. Success here is necessary but not sufficient for real-browser parameterized inheritance.

3. **Small sample**: 3 training observations per condition, 3–5 unseen test combinations. **Mitigation**: Sufficient for a clear binary result. Ambiguous results (e.g., 3/5) would require replication.

4. **Slot naming subjectivity**: The expected slot names in the spec are illustrative; the actual names may differ (e.g., `param_0` vs `user_id`). **Mitigation**: The decision rule requires distinct slot names, not specific names. Any naming scheme that produces distinct slots for distinct fields satisfies the claim.

5. **No model calls**: This tests kernel code paths, not LLM-driven mechanism discovery. **Mitigation**: C-PARAM-INHERIT's current gate is "induce from observations, succeed on unseen." LLM-driven discovery is a separate experiment tier.

## 10. Consequences

### If MULTI-PARAM-SURVIVES

- C-PARAM-INHERIT advances: the kernel can induce distinct parameter slots from structured observations with multiple varying fields
- Product can register multi-parameter mechanisms (path + body + header patterns) for external-agent consumption
- Next gate: test with noisy observations from real browser sessions (C-PARAM-INHERIT's "learn on A" half)
- The handoff-identified blocker (multi-parameter collision) is resolved

### If MULTI-PARAM-FALSIFIED

- C-PARAM-INHERIT remains stuck at single-parameter POC
- The kernel cannot handle real API patterns (POST with body, multi-field variation)
- Product cannot register multi-parameter mechanisms
- The smallest next action: identify which induction step fails (slot discovery, naming, or binding) and redesign the heuristic

### If MEASUREMENT_INVALID

- The induction function cannot be implemented with the required properties
- The approach needs fundamental redesign (not just parameter tuning)
- Consider alternative: LLM-driven slot discovery instead of heuristic comparison

## 11. Analysis Plan

1. **Implement** `distill_parameterized()` with multi-parameter support in the experiment script (not modifying kernel.py during DESIGN)
2. **Run** each condition: distill from training observations, resolve on unseen combinations
3. **Measure**: slot_count, slot_names, unseen_resolution_rate, binding_accuracy, collision detection
4. **Compare** against baselines (B_LITERAL, B_COLD, B_RANDOM_INDUCTION)
5. **Apply** decision rule: all conditions must pass for SURVIVES
6. **Report** all outcomes with equal prominence

## 12. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 13. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
