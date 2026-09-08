# EXP-GRAPH-33998605047 Report

## Executive Summary

**Outcome: SUPPORTS** — The parameter-slot-count fix eliminates all 5 false accepts from the original literal-vs-param equal-confidence hazard, preserves all 7 baselines, generalizes to multi-slot (2 vs 1), and correctly handles template-only params. Status: COMPLETE.

The fix is validated on synthetic substrate for single-slot, multi-slot, and template-only cases. The next gate is real-web endpoints with DOM, auth, session, and drift — but the fix must be committed to production HEAD first.

## 1. Raw Evidence Summary

16 conditions executed, 0 exceptions. All conditions deterministic (no model calls, no RNG, no HTTP). Fix applied temporarily: `candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)`.

## 2. Baseline Conditions (7/7 PASS)

| Condition | Status | Mechanism | URL | Pass |
|-----------|--------|-----------|-----|------|
| cold | UNKNOWN | None | N/A | PASS |
| literal-only-original | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | PASS |
| literal-only-unseen | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | PASS |
| param-only-original | EXECUTABLE | param-fetch-posts | /posts/1 | PASS |
| param-only-unseen | EXECUTABLE | param-fetch-posts | /posts/2 | PASS |
| compete-param-higher | EXECUTABLE | param-fetch-posts-high | /posts/3 | PASS |
| compete-literal-higher | EXECUTABLE | literal-fetch-posts-1-low | /posts/1 | PASS |

All 7 baselines match expected outcomes. No regression from parent experiments.

## 3. False Accept Elimination (5/5 PASS)

The core intervention: at equal confidence (0.95), param must beat literal for all tested id values.

| Condition | Mechanism | URL | Param Wins? |
|-----------|-----------|-----|-------------|
| compete-equal-id2 | param-fetch-posts | /posts/2 | PASS |
| compete-equal-id3 | param-fetch-posts | /posts/3 | PASS |
| compete-equal-id4 | param-fetch-posts | /posts/4 | PASS |
| compete-equal-id5 | param-fetch-posts | /posts/5 | PASS |
| compete-equal-id6 | param-fetch-posts | /posts/6 | PASS |

**0 false accepts remaining.** Before fix: literal won all 5 (false accepts). After fix: param wins all 5.

## 4. Generalization Conditions

### 4.1 Multi-Slot Dominance (PASS)
- 2-slot param `[id, category]` /posts/${id}/${category} beats 1-slot param `[id]` /posts/${id} at equal confidence 0.95
- Winning mechanism: param-2slot
- Bound URL: /posts/3/tech
- Tuple sort: (0.95, 2) > (0.95, 1) — more parameter slots wins

### 4.2 Template-Only vs Param (PASS)
- Template-only (parameter_slots=[], len=0) loses to declared param (parameter_slots=['id'], len=1)
- Winning mechanism: param-fetch-posts
- Bound URL: /posts/3
- Declared slot credit: len=1 > len=0

### 4.3 Template-Only vs Literal (Recorded)
- Template-only-fetch vs literal-fetch-posts-1 at equal confidence 0.95
- Both len=0 → tie → insertion-order
- Winner: template-only-fetch (registered first)
- This is insertion-order dependent, not deterministic across registry orders

### 4.4 Equal-Slot Tie Param vs Param (Recorded)
- param-fetch-posts vs param-fetch-alt at equal confidence 0.95, both len=1
- Tie → insertion-order
- Winner: param-fetch-posts (registered first)
- Consistent with parent finding: equal-slot ties are stable insertion-order

## 5. Interpretation

The parameter-slot-count fix is validated on this synthetic substrate:

1. **False accepts eliminated**: The original hazard (literal winning over param at equal confidence) is fully eliminated across all 5 tested id values.
2. **No baseline regression**: All 7 baselines preserve expected behavior.
3. **Multi-slot generalization**: 2-slot beats 1-slot at equal confidence, as predicted by tuple sort.
4. **Template-only handling**: Declared params beat template-only params, as predicted by len(parameter_slots).

## 6. Claim Ceiling

The fix is validated under these conditions:
- Synthetic substrate only (jsonplaceholder.typicode.com templates)
- Single-slot and one multi-slot pair (2 vs 1)
- Template-only params tested
- All resolution-only (no HTTP execution)
- Fix applied temporarily, not committed to HEAD

**Not validated**: Real-web endpoints, DOM, auth, session, drift, other slot counts (3 vs 2, 5 vs 1), non-fetch-post intents, LLM distillation, non-empty preconditions.

## 7. Product Consequence

If this fix is committed to production HEAD and re-validated post-commit:
- C-PARAM-INHERIT advances from EXPERIMENTAL to validated on synthetic substrate
- The original competition hazard is eliminated
- Next gate: real-web endpoint testing with DOM, auth, session, and drift

## 8. Comparison with Parent Experiment

| Aspect | EXP-GRAPH-33955869291 (Parent) | EXP-GRAPH-33998605047 (This) |
|--------|--------------------------------|------------------------------|
| Original hazard re-tested | No (inherited only) | Yes (5/5 conditions) |
| False accepts eliminated | Not measured | 5/5 confirmed |
| Multi-slot | 1 pair (2 vs 1) | 1 pair (2 vs 1) ✓ |
| Template-only vs param | 1 condition | 1 condition ✓ |
| Baselines | 5 solo | 7 (5 solo + 2 confidence) |
| verify() | 2 conditions | Not tested (out of scope) |
| Fix committed | No | No |

The critical new evidence: the original false-accept hazard is confirmed eliminated in a single integrated run. This was the missing validation from the parent experiment.
