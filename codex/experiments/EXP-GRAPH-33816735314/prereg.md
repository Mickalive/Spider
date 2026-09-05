# EXP-GRAPH-33816735314 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-33816735314
- **Lane**: Graph
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Parent**: EXP-GRAPH-33718012817 (COMPETITION-UNSAFE)
- **Date**: 2026-09-03
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does adding a parameter-slot-count secondary tie-break in `kernel.py resolve()` eliminate false accepts in mixed literal+parameterized registries at equal confidence, without breaking cold, literal-only, or parameter-only baselines?

## 3. Motivation

The parent experiment (EXP-GRAPH-33718012817) established:

- **Literal universal matching**: A literal mechanism with `parameter_slots=[]` yields `required_slots={}` (kernel.py L104-106), making it eligible for ALL parameter values via vacuous `any()` check.
- **False accepts**: In shared registries at equal confidence (0.95), the literal mechanism shadows the parameterized mechanism for 5/5 eligible parameter values (id=2..6), producing `bound_action=/posts/1` instead of `/posts/{id}`.
- **Tie-break is lexicographic**: `registry.py` sorts by `mechanism_id` (L38: `sorted(items)`), not insertion order.
- **Confidence disambiguation works**: 0.98 vs 0.95 correctly produces the higher-confidence winner, but equal confidence is realistic.
- **COMPETITION-UNSAFE verdict**: C-PARAM-INHERIT is BLOCKED until a code fix resolves the hazard.

The parent handoff recommends three possible fixes:
- **Option A**: Tie-break at equal confidence prefer parameterized mechanisms (kernel code change in `resolve()`)
- **Option B**: Literal mechanisms carry value-based constraints that reject params conflicting with fixed resources
- **Option C**: Add a `fixed_resource` field to literal mechanisms

This experiment tests **Option A** — the smallest possible code change: modifying the sort key in `resolve()` from `lambda m: m.confidence` to `lambda m: (m.confidence, len(m.parameter_slots))`.

## 4. Hypotheses

### H1: False-Accept Elimination
After the fix, in shared registries at equal confidence (0.95), the parameterized mechanism wins for all parameter values (id=1..6), producing parameterized `bound_action` URLs (`/posts/{id}`).

### H2: Baseline Preservation
All baseline conditions produce identical results to the parent experiment:
- Cold → UNKNOWN
- Literal-only-original → EXECUTABLE url=/posts/1
- Literal-only-unseen → EXECUTABLE url=/posts/1
- Param-only-original → EXECUTABLE url=/posts/1
- Param-only-unseen → EXECUTABLE url=/posts/2

### H3: Confidence Disambiguation Preservation
Confidence-based disambiguation still works:
- Higher-confidence param (0.98) beats lower-confidence literal (0.95) → param wins
- Higher-confidence literal (0.98) beats lower-confidence param (0.95) → literal wins

### H4: No Regression
No condition produces a Python exception, type error, or unexpected resolution status (e.g., EXPLORE, REPAIRABLE) when EXECUTABLE or UNKNOWN is expected.

## 5. Code Fix

### 5.1 The Change

**File**: `src/spider/kernel.py`, line 112

**Before**:
```python
candidates.sort(key=lambda m: m.confidence, reverse=True)
```

**After**:
```python
candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
```

### 5.2 Rationale

When confidence is equal, `reverse=True` with tuple `(confidence, len(parameter_slots))` means:
- Literal mechanism: `(0.95, 0)` — 0 parameter slots
- Parameterized mechanism: `(0.95, 1)` — 1 parameter slot
- `(0.95, 1) > (0.95, 0)` in descending sort → parameterized wins

This is the minimal change: one line, no new fields, no schema changes, no impact on existing mechanism types.

### 5.3 Why This Works

The false-accept hazard occurs because:
1. Literal's `required_slots={}` makes it universally eligible
2. At equal confidence, the tie-break is arbitrary (lexicographic mechanism_id)
3. The literal mechanism can win and produce incorrect `bound_action`

The fix adds a deterministic, semantically meaningful tie-break: prefer mechanisms that declare they need parameters. This is sound because:
- A mechanism that declares `parameter_slots=['id']` is explicitly designed to handle parameterized requests
- A mechanism with `parameter_slots=[]` is a fixed-resource mechanism that happens to match vacuously
- When both match at equal confidence, the parameterized mechanism is the more specific and correct choice

## 6. Experimental Conditions

### 6.1 Registry Configurations

| Registry | Mechanisms | Notes |
|----------|-----------|-------|
| empty | (none) | Cold null |
| literal-only | literal-fetch-posts-1 (confidence=0.95, parameter_slots=[], template=/posts/1) | Literal baseline |
| param-only | param-fetch-posts (confidence=0.95, parameter_slots=['id'], template=/posts/${id}) | Parameterized baseline |
| shared-equal | Both literal and param at confidence=0.95 | Competition test |
| shared-param-higher | Param at 0.98, literal at 0.95 | Confidence disambiguation |
| shared-literal-higher | Literal at 0.98, param at 0.95 | Confidence disambiguation |

### 6.2 Conditions

13 conditions total:
- 5 baseline conditions (cold, literal-only × 2, param-only × 2)
- 6 intervention conditions (compete-equal-id1 through id6)
- 2 control conditions (compete-param-higher, compete-literal-higher)

### 6.3 Expected Outcomes

| Condition | Expected Resolution | Expected URL | Expected Winner |
|-----------|-------------------|--------------|-----------------|
| cold | UNKNOWN | null | — |
| literal-only-original | EXECUTABLE | /posts/1 | literal |
| literal-only-unseen | EXECUTABLE | /posts/1 | literal |
| param-only-original | EXECUTABLE | /posts/1 | param |
| param-only-unseen | EXECUTABLE | /posts/2 | param |
| compete-equal-id1 | EXECUTABLE | /posts/1 | param |
| compete-equal-id2 | EXECUTABLE | /posts/2 | param |
| compete-equal-id3 | EXECUTABLE | /posts/3 | param |
| compete-equal-id4 | EXECUTABLE | /posts/4 | param |
| compete-equal-id5 | EXECUTABLE | /posts/5 | param |
| compete-equal-id6 | EXECUTABLE | /posts/6 | param |
| compete-param-higher | EXECUTABLE | /posts/3 | param |
| compete-literal-higher | EXECUTABLE | /posts/1 | literal |

## 7. Statistical Analysis

This experiment is fully deterministic (no model calls, no RNG, no sampling). No statistical tests are needed. All conditions produce exact expected values. The analysis is a point-by-point comparison of observed vs. expected resolution status, bound_action URL, and winning mechanism_id.

## 8. Controls

### 8.1 Baseline Replication (B_COLD, B_LITERAL_*, B_PARAM_*)
These replicate the parent experiment's conditions exactly. Any regression indicates the fix broke existing behavior.

### 8.2 Positive Control (compete-param-higher)
Replicates the parent's confidence-disambiguation test. Higher-confidence param wins. Verifies the fix does not disrupt confidence-based sorting.

### 8.3 Null Control (compete-literal-higher)
Replicates the parent's confidence-disambiguation test in the opposite direction. Higher-confidence literal wins. Verifies the fix does not create a blanket preference for parameterized mechanisms regardless of confidence.

### 8.4 Fix Validation (compete-equal-id2 through id6)
These are the new measurements. If the fix works, param wins all 5 conditions with correct parameterized URLs. If any still show literal bound_action, the fix is insufficient.

## 9. Validity Threats

### 9.1 Substrate Limitation
Only jsonplaceholder.typicode.com is tested. Real Web endpoints may have different behavior. **Mitigation**: This is a kernel logic test, not a Web execution test. The fix is in pure Python sorting logic.

### 9.2 Single Parameter Slot
Only one parameter slot (`id`) is tested. Multiple parameter slots might behave differently. **Mitigation**: The sort key `len(m.parameter_slots)` is a total order that generalizes to any number of slots. Multiple-slot mechanisms would always win over zero-slot mechanisms at equal confidence.

### 9.3 mechanism_id Sensitivity
The parent experiment showed that lexicographic mechanism_id ordering affects the tie-break. The fix replaces this with parameter-slot-count ordering. **Mitigation**: Parameter-slot-count is mechanism_id-independent, eliminating the ID-sensitivity hazard.

### 9.4 Single Confidence Level
Only equal confidence (0.95) is tested for the fix. Other equal-confidence values (e.g., 0.90, 0.99) are not tested. **Mitigation**: The fix operates on the sort key tuple, which is independent of the specific confidence value.

### 9.5 No Regression Test for verify()
The parent handoff noted that `verify()` has hardcoded `status=200`. This experiment does not test verify(). **Mitigation**: Out of scope. The fix does not modify verify().

## 10. Decision Rules

### 10.1 COMPETITION-SAFE
If ALL of:
1. cold → UNKNOWN
2. literal-only-original → EXECUTABLE url=/posts/1
3. literal-only-unseen → EXECUTABLE url=/posts/1
4. param-only-original → EXECUTABLE url=/posts/1
5. param-only-unseen → EXECUTABLE url=/posts/2
6. compete-param-higher → EXECUTABLE url=/posts/3 with param
7. compete-literal-higher → EXECUTABLE url=/posts/1 with literal
8. compete-equal-id2 through id6 → EXECUTABLE with param bound_action (/posts/{id}) and param-fetch-posts winning

### 10.2 COMPETITION-UNSAFE
If ANY of:
- Any baseline condition (1-5) regresses (different result than parent)
- Any compete-equal-id condition (id2-id6) still returns literal bound_action
- Any condition produces unexpected resolution status

### 10.3 MEASUREMENT_INVALID
If:
- Code fix causes Python exceptions or import errors
- Kernel cannot be instantiated with the fix
- Unexpected infrastructure failure

## 11. Expected Outcomes

### 11.1 COMPETITION-SAFE (Expected)
- The parameter-slot-count tie-break is validated as the minimal safe fix
- C-PARAM-INHERIT can advance past BLOCKED
- Product registration of mixed literal+parameterized mechanisms becomes safe
- The fix is a single-line change with no schema impact

### 11.2 COMPETITION-UNSAFE
- Option A is insufficient
- Must explore Option B (value-based constraints) or Option C (fixed_resource field)
- C-PARAM-INHERIT remains BLOCKED

### 11.3 MEASUREMENT_INVALID
- Fix has implementation issues
- Not scientific evidence for or against

## 12. Analysis Plan

1. **Apply Fix**: Modify `kernel.py` line 112 from `candidates.sort(key=lambda m: m.confidence, reverse=True)` to `candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)`
2. **Run All Conditions**: Execute 13 conditions with fresh kernel instances
3. **Compare**: Point-by-point comparison of observed vs. expected for each condition
4. **Decision**: Apply frozen decision rule (Section 10)

## 13. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 14. Freeze Statement

This preregistration is frozen BEFORE any code is modified or any outcome data is inspected. The experiment will be executed exactly as described here.
