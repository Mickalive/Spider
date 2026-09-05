# EXP-GRAPH-33816735314 Report

## Executive Summary

**Outcome**: COMPETITION-SAFE

The parameter-slot-count secondary tie-break in `kernel.py resolve()` eliminates all false accepts in mixed literal+parameterized registries at equal confidence, without breaking cold, literal-only, or parameter-only baselines. All 13 conditions passed. The fix is a single-line change with no new fields, no schema changes, and no impact on existing mechanism types.

## Background

The parent experiment (EXP-GRAPH-33718012817) established that:
1. Literal mechanisms with `parameter_slots=[]` yield `required_slots={}`, making them universally eligible for all parameter values via vacuous `any()` check.
2. In shared registries at equal confidence (0.95), the literal mechanism shadows the parameterized mechanism for 5/5 eligible parameter values (id=2..6), producing `bound_action=/posts/1` instead of `/posts/{id}`.
3. The tie-break is lexicographic mechanism_id ordering, not insertion order.
4. Confidence-based disambiguation works (0.98 vs 0.95) but is insufficient alone because equal confidence is realistic.

The parent handoff recommended three possible fixes:
- **Option A**: Tie-break at equal confidence prefer parameterized mechanisms (kernel code change in `resolve()`)
- **Option B**: Literal mechanisms carry value-based constraints that reject params conflicting with fixed resources
- **Option C**: Add a `fixed_resource` field to literal mechanisms

This experiment tests **Option A** — the smallest possible code change.

## Code Fix

**File**: `src/spider/kernel.py`, line 112

**Before**:
```python
candidates.sort(key=lambda m: m.confidence, reverse=True)
```

**After**:
```python
candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
```

When confidence is equal, `reverse=True` with tuple `(confidence, len(parameter_slots))` means:
- Literal mechanism: `(0.95, 0)` — 0 parameter slots
- Parameterized mechanism: `(0.95, 1)` — 1 parameter slot
- `(0.95, 1) > (0.95, 0)` in descending sort → parameterized wins

## Results

### Baseline Conditions (5/5 PASS)

| Condition | Expected | Observed | Status |
|-----------|----------|----------|--------|
| cold | UNKNOWN | UNKNOWN | PASS |
| literal-only-original | EXECUTABLE url=/posts/1 | EXECUTABLE url=/posts/1 | PASS |
| literal-only-unseen | EXECUTABLE url=/posts/1 | EXECUTABLE url=/posts/1 | PASS |
| param-only-original | EXECUTABLE url=/posts/1 | EXECUTABLE url=/posts/1 | PASS |
| param-only-unseen | EXECUTABLE url=/posts/2 | EXECUTABLE url=/posts/2 | PASS |

### Intervention Conditions (6/6 PASS)

| Condition | Expected | Observed | Status |
|-----------|----------|----------|--------|
| compete-equal-id1 | EXECUTABLE url=/posts/1 param | EXECUTABLE url=/posts/1 param | PASS |
| compete-equal-id2 | EXECUTABLE url=/posts/2 param | EXECUTABLE url=/posts/2 param | PASS |
| compete-equal-id3 | EXECUTABLE url=/posts/3 param | EXECUTABLE url=/posts/3 param | PASS |
| compete-equal-id4 | EXECUTABLE url=/posts/4 param | EXECUTABLE url=/posts/4 param | PASS |
| compete-equal-id5 | EXECUTABLE url=/posts/5 param | EXECUTABLE url=/posts/5 param | PASS |
| compete-equal-id6 | EXECUTABLE url=/posts/6 param | EXECUTABLE url=/posts/6 param | PASS |

### Control Conditions (2/2 PASS)

| Condition | Expected | Observed | Status |
|-----------|----------|----------|--------|
| compete-param-higher | EXECUTABLE url=/posts/3 param | EXECUTABLE url=/posts/3 param | PASS |
| compete-literal-higher | EXECUTABLE url=/posts/1 literal | EXECUTABLE url=/posts/1 literal | PASS |

## Interpretation

### False-Accept Elimination

The fix eliminates all 5 false accepts (compete-equal-id2 through id6). Before the fix, these conditions returned `bound_action=/posts/1` (literal's fixed URL). After the fix, they return `bound_action=/posts/{id}` (parameterized's template URL).

### Baseline Preservation

All 5 baseline conditions produce identical results to the parent experiment:
- Cold registry correctly returns UNKNOWN (strong null validated).
- Literal mechanism standalone works correctly: EXECUTABLE on original resource (id=1) and universal on unseen (id=2) with correct literal bound_action.
- Parameterized mechanism standalone works correctly: EXECUTABLE with correct `_bind()` URL substitution on original (id=1) and unseen (id=2).

### Confidence Disambiguation Preservation

Confidence-based disambiguation remains intact:
- Higher-confidence param (0.98) beats lower-confidence literal (0.95) → param wins
- Higher-confidence literal (0.98) beats lower-confidence param (0.95) → literal wins

The fix does not create a blanket preference for parameterized mechanisms regardless of confidence. The confidence difference dominates the sort key.

### No Regression

No condition produces a Python exception, type error, or unexpected resolution status (e.g., EXPLORE, REPAIRABLE) when EXECUTABLE or UNKNOWN is expected.

## Decision

Apply frozen decision rule from `spec.json`:

**COMPETITION-SAFE** if ALL of:
1. cold → UNKNOWN ✓
2. literal-only-original → EXECUTABLE url=/posts/1 ✓
3. literal-only-unseen → EXECUTABLE url=/posts/1 ✓
4. param-only-original → EXECUTABLE url=/posts/1 ✓
5. param-only-unseen → EXECUTABLE url=/posts/2 ✓
6. compete-param-higher → EXECUTABLE url=/posts/3 with param ✓
7. compete-literal-higher → EXECUTABLE url=/posts/1 with literal ✓
8. compete-equal-id2 through id6 → EXECUTABLE with param bound_action (/posts/{id}) and param-fetch-posts winning ✓

**Result**: COMPETITION-SAFE

## Product Consequences

If COMPETITION-SAFE (as observed):
- The parameter-slot-count tie-break is validated as the minimal safe fix for the false-accept hazard.
- C-PARAM-INHERIT can advance past the BLOCKED state.
- Product registration of mixed literal+parameterized mechanisms becomes safe at equal confidence.
- The fix is a single-line change with no new fields, no schema changes, and no impact on existing mechanism types.

## Validity Threats

### Substrate Limitation
Only jsonplaceholder.typicode.com is tested. Real Web endpoints may have different behavior. **Mitigation**: This is a kernel logic test, not a Web execution test. The fix is in pure Python sorting logic.

### Single Parameter Slot
Only one parameter slot (`id`) is tested. Multiple parameter slots might behave differently. **Mitigation**: The sort key `len(m.parameter_slots)` is a total order that generalizes to any number of slots. Multiple-slot mechanisms would always win over zero-slot mechanisms at equal confidence.

### mechanism_id Sensitivity
The parent experiment showed that lexicographic mechanism_id ordering affects the tie-break. The fix replaces this with parameter-slot-count ordering. **Mitigation**: Parameter-slot-count is mechanism_id-independent, eliminating the ID-sensitivity hazard.

### Single Confidence Level
Only equal confidence (0.95) is tested for the fix. Other equal-confidence values (e.g., 0.90, 0.99) are not tested. **Mitigation**: The fix operates on the sort key tuple, which is independent of the specific confidence value.

### No Regression Test for verify()
The parent handoff noted that `verify()` has hardcoded `status=200`. This experiment does not test verify(). **Mitigation**: Out of scope. The fix does not modify verify().

## Next Steps

1. **Revert the code fix** — the experiment script applied the fix temporarily; the actual kernel.py should be reverted or the fix should be committed separately after DIRECTOR approval.
2. **Re-test with counterbalanced IDs** — confirm the fix is not ID-dependent (the parent showed sensitivity to ID ordering).
3. **Test verify() postcondition checking** — the parent handoff noted hardcoded `status=200` in verify().
4. **Advance C-PARAM-INHERIT** — the claim can move past BLOCKED with appropriate claim_updates.
