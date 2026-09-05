# EXP-GRAPH-33955869291 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-33955869291
- **Lane**: Graph
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Parent**: EXP-GRAPH-33816735314 (COMPETITION-SAFE, parameter-slot-count tie-break validated on 0-vs-1 slot)
- **Date**: 2026-09-05
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the parameter-slot-count tie-break generalize safely to multi-slot mechanisms (2 vs 1 slot), template-only params with parameter_slots=[] but template ${id}, equal-slot-count ties (0 vs 0 or 1 vs 1), and verify() postcondition checking for non-200 HTTP responses?

## 3. Motivation

The parent experiment (EXP-GRAPH-33816735314) established that the parameter-slot-count tie-break (Option A) eliminates 5/5 eligible false accepts in mixed literal+parameterized registries at equal confidence on deterministic synthetic substrate. However, the claim ceiling is limited to single-slot, single-intent, deterministic synthetic substrate.

The parent handoff identifies these specific unknowns:
- Whether the fix generalizes safely to multi-slot mechanisms (2 vs 1 slot tie)
- Whether template-only params (parameter_slots=[] but template has ${id}) are handled correctly
- Whether equal-slot-count ties (0 vs 0 or 1 vs 1) remain deterministic
- Whether verify() postcondition checking works for non-200 HTTP responses (hardcoded status=200 per parent audit V_VERIFY_HARDCODED_STATUS)

This experiment directly tests all four unknowns. The `required_slots` vs `parameter_slots` divergence is a design issue that the template-only param condition will expose.

## 4. Hypotheses

### H1: Multi-Slot Tie-Break
At equal confidence, a 2-slot mechanism (parameter_slots=['user_id', 'post_id']) wins over a 1-slot mechanism (parameter_slots=['id']) because len(parameter_slots)=2 > 1 under the fix.

### H2: Template-Only Param Subordination
At equal confidence, a 1-slot param mechanism wins over a template-only param mechanism (parameter_slots=[] but template has ${id}) because len(parameter_slots)=1 > 0 under the fix. The template-only param mechanism requires the parameter for binding but declares no slots; the tie-break correctly subordinates it.

### H3: Equal-Slot-Count Degeneracy
Equal-slot-count ties (0 vs 0, 1 vs 1) are degenerate: the winner depends on insertion order (Python's stable sort), not on slot count. This is an expected limitation, not a regression.

### H4: No Regression
All baseline conditions (cold, literal-only, 1-slot param-only, 2-slot param-only) produce the expected results on the unfixed kernel. Confidence-based disambiguation (higher confidence wins regardless of slot count) remains intact under the fix.

### H5: verify() Correctness
verify() correctly rejects when postconditions do not match observed state, including non-200 HTTP status codes. Empty postconditions match any state (True). Partial matches (status matches but content_type does not) correctly reject (False).

### H6: verify() Fix Idempotence
The fix (adding len(parameter_slots) to the sort key) does not alter verify() behavior. verify() results are identical for the same mechanism/state pairs under both fixed and unfixed kernels.

## 5. Design

### 5.1 Code Fix

The same single-line fix from EXP-GRAPH-33816735314 is applied in the test script for fix conditions:
```python
# Before fix (current HEAD — used for unfixed conditions):
candidates.sort(key=lambda m: m.confidence, reverse=True)
# After fix (applied in test script for fix conditions):
candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
```

The fix is NOT committed to production HEAD. This experiment tests the fix's behavior on edge cases and verify() correctness, not its production deployment.

### 5.2 Conditions

15 conditions total, all deterministic, no HTTP execution, no model calls.

**Baselines on unfixed kernel (5 conditions):**
- B_COLD: No mechanisms registered
- B_LITERAL: Literal mechanism only (parameter_slots=[], fixed URL)
- B_PARAM_1SLOT: 1-slot param only (parameter_slots=['id'], template /posts/${id})
- B_PARAM_2SLOT: 2-slot param only (parameter_slots=['user_id', 'post_id'], template /users/${user_id}/posts/${post_id})
- B_UNFIXED_2VS1: 2-slot vs 1-slot at equal confidence on unfixed kernel — documents the problem

**Interventions on fixed kernel (5 conditions):**
- COMPETE_2VS1: 2-slot vs 1-slot at equal confidence (0.95)
- COMPETE_TEMPLATE_VS_PARAM: Template-only param vs 1-slot param at equal confidence (0.95)
- COMPETE_TEMPLATE_VS_LITERAL: Template-only param vs literal at equal confidence (0.95) — degenerate
- COMPETE_1VS1_EQUAL: Two 1-slot params at equal confidence — degenerate
- COMPETE_0VS0_EQUAL: Two literals at equal confidence — degenerate

**Controls on fixed kernel (2 conditions):**
- POS_CONTROL: 2-slot higher confidence (0.98) vs 1-slot lower (0.95)
- NULL_CONTROL: 1-slot higher confidence (0.98) vs 2-slot lower (0.95)

**verify() tests on unfixed kernel (3 conditions):**
- VERIFY_EMPTY_POSTCONDITIONS: Empty postconditions always return True
- VERIFY_STATUS_MISMATCH: Status 200 postcondition vs 404 observed → False
- VERIFY_MULTI_FIELD_MISMATCH: status=200 + content_type=json postcondition vs status=200 + content_type=html → False

**verify() idempotence test (1 condition):**
- VERIFY_FIX_NO_EFFECT: verify() results identical under fixed and unfixed kernels

### 5.3 Mechanism Definitions

All mechanisms use jsonplaceholder.typicode.com URLs (consistent with parent experiment). No HTTP execution — only resolution, bound_action correctness, and verify() boolean measured.

| Mechanism ID | parameter_slots | action_template | confidence |
|---|---|---|---|
| literal-fetch-posts | [] | {url: /posts/1} | varies |
| param-fetch-posts | ['id'] | {url: /posts/${id}} | varies |
| param-fetch-user-posts | ['user_id', 'post_id'] | {url: /users/${user_id}/posts/${post_id}} | varies |
| template-only-fetch | [] | {url: /users/${id}/posts} | 0.95 |
| literal-fetch-alt | [] | {url: /posts/1/comments} | 0.95 |
| param-fetch-alt | ['id'] | {url: /posts/${id}/comments} | 0.95 |

### 5.4 Registry Configurations

| Registry | Mechanisms | Purpose |
|---|---|---|
| empty | (none) | Cold baseline |
| literal-only | literal-fetch-posts (0.95) | Literal baseline |
| param-1slot-only | param-fetch-posts (0.95) | 1-slot baseline |
| param-2slot-only | param-fetch-user-posts (0.95) | 2-slot baseline |
| shared-2v1 | param-fetch-user-posts (0.95) + param-fetch-posts (0.95) | Multi-slot tie-break |
| shared-template-v-param | template-only-fetch (0.95) + param-fetch-posts (0.95) | Template vs param |
| shared-template-v-literal | template-only-fetch (0.95) + literal-fetch-posts (0.95) | Template vs literal (degenerate) |
| shared-1v1 | param-fetch-posts (0.95) + param-fetch-alt (0.95) | Equal-slot degenerate |
| shared-0v0 | literal-fetch-posts (0.95) + literal-fetch-alt (0.95) | Equal-slot degenerate |
| shared-pos | param-fetch-user-posts (0.98) + param-fetch-posts (0.95) | Positive control |
| shared-null | param-fetch-posts (0.98) + param-fetch-user-posts (0.95) | Null control |

### 5.5 verify() Test Setup

For verify() conditions, a mechanism is registered with specified postconditions. verify() is then called with an observed_state dict. The verify() function checks `_matches(mechanism.postconditions, observed_state)` — a dict-equality check that returns True if and only if every key in postconditions has the corresponding value in observed_state.

Key code path: `src/spider/kernel.py:125-129`:
```python
def verify(self, mechanism_id: str, observed_state: dict[str, Any]) -> bool:
    mechanism = next((m for m in self.registry.all() if m.mechanism_id == mechanism_id), None)
    if mechanism is None or mechanism.invalidated:
        return False
    return _matches(mechanism.postconditions, observed_state)
```

And `_matches` at `src/spider/kernel.py:15-16`:
```python
def _matches(required: dict[str, Any], actual: dict[str, Any]) -> bool:
    return all(actual.get(k) == v for k, v in required.items())
```

This means:
- Empty postconditions → `all()` over empty iterable → True (always passes)
- Non-empty postconditions → every key must match exactly
- Partial matches fail (e.g., status matches but content_type does not)
- The fix (sort key change) does not touch verify() or _matches

## 6. Measures

### 6.1 Primary Metric
- **tie_break_generalizes**: Boolean — COMPETE_2VS1 returns 2-slot AND COMPETE_TEMPLATE_VS_PARAM returns 1-slot

### 6.2 Secondary Metrics
- Baseline pass rate on unfixed kernel (expected: 5/5)
- Intervention pass rate on fixed kernel (expected: 2/2 non-degenerate)
- Degenerate condition count (expected: 3, all ID-dependent)
- Control pass rate (expected: 2/2)
- verify() pass rate (expected: 4/4)
- Resolution status consistency (no exceptions, no unexpected statuses)
- B_UNFIXED_2VS1 winner documentation (insertion-order-dependent)

## 7. Null Models

### 7.1 Insertion-Order Null
For degenerate conditions (equal slot count), the winner is determined by insertion order in the registry, not by any mechanism property. This is the expected behavior when the tie-break cannot discriminate.

### 7.2 Confidence-Dominance Null
When confidence differs, the higher-confidence mechanism wins regardless of slot count. The tie-break only applies at equal confidence.

### 7.3 Unfixed-Baseline Null
On the unfixed kernel (confidence-only sort), the winner at equal confidence is determined by insertion order. B_UNFIXED_2VS1 documents this baseline behavior.

## 8. Statistical Tests

All conditions are deterministic. No statistical tests required. Pass/fail is binary.

## 9. Controls

### 9.1 Positive Control (POS_CONTROL)
2-slot param with higher confidence (0.98) vs 1-slot param (0.95) under the fix. Must return 2-slot mechanism. Verifies confidence dominance works for multi-slot mechanisms.

### 9.2 Null Control (NULL_CONTROL)
1-slot param with higher confidence (0.98) vs 2-slot param (0.95) under the fix. Must return 1-slot mechanism. Verifies confidence dominance works in reverse.

### 9.3 Baseline Controls (B_COLD, B_LITERAL, B_PARAM_1SLOT, B_PARAM_2SLOT)
Replicate parent experiment baselines on the unfixed kernel to verify no regression.

### 9.4 Unfixed Baseline Control (B_UNFIXED_2VS1)
Documents the unfixed kernel's behavior at equal confidence: insertion order determines the winner. This establishes the problem the fix solves.

### 9.5 verify() Controls
Three verify() conditions test the postcondition matching logic:
- Empty postconditions (always True) — verifies _matches handles empty dict
- Status mismatch (False) — verifies non-200 responses are correctly rejected
- Multi-field mismatch (False) — verifies partial matches correctly reject

## 10. Validity Threats

### 10.1 Fix Not Committed
The code fix is applied in the test script, not committed to production HEAD. This is intentional: the experiment tests the fix's behavior on edge cases, not its production deployment. The commit question is a separate product/promotion decision.

### 10.2 Template-Only Param Design Issue
Template-only params (parameter_slots=[] but template has ${id}) expose a divergence: `required_slots` = parameter_slots | template_slots = {'id'}, but `parameter_slots` = []. The tie-break uses `parameter_slots`, so template-only params are treated as 0-slot mechanisms. This is a known design limitation that the experiment will expose. The fix correctly subordinates template-only params to declared-slot params, but the design question of whether template slots should inform the tie-break remains open.

### 10.3 Degenerate Equal-Slot-Count Ties
Equal-slot-count ties (0 vs 0, 1 vs 1) are expected to be ID-dependent. This is a known limitation, not a regression. The experiment records this but does not gate on it.

### 10.4 Synthetic Substrate
All conditions use jsonplaceholder.typicode.com URLs. No HTTP execution. Findings apply to kernel resolution logic and verify() boolean checks only, not to real-web endpoints with DOM, auth, session, or drift.

### 10.5 Single Fix Variant
Only the Option A fix (parameter_slots count) is tested. Alternative fixes (required_slots count, template_slots count) are not tested. If Option A fails, alternatives remain unexplored.

### 10.6 verify() Test Scope
verify() conditions test dict-matching logic, not actual HTTP response handling. The question "does verify() work for non-200 HTTP responses" is answered at the kernel level: verify() rejects any observed_state that doesn't match postconditions, regardless of HTTP status code. The product-level question of whether mechanisms should be registered with status-specific postconditions is out of scope.

## 11. Decision Rules

### 11.1 MULTI-SLOT-SAFE
If ALL of:
1. B_COLD → UNKNOWN
2. B_LITERAL → EXECUTABLE url=/posts/1
3. B_PARAM_1SLOT → EXECUTABLE url=/posts/1
4. B_PARAM_2SLOT → EXECUTABLE url=/users/1/posts/1
5. COMPETE_2VS1 → EXECUTABLE with param-fetch-user-posts as winning mechanism
6. COMPETE_TEMPLATE_VS_PARAM → EXECUTABLE with param-fetch-posts as winning mechanism
7. POS_CONTROL → EXECUTABLE with param-fetch-user-posts as winning mechanism
8. NULL_CONTROL → EXECUTABLE with param-fetch-posts as winning mechanism
9. VERIFY_EMPTY_POSTCONDITIONS → True
10. VERIFY_STATUS_MISMATCH → False
11. VERIFY_MULTI_FIELD_MISMATCH → False
12. VERIFY_FIX_NO_EFFECT → both match and mismatch results correct

### 11.2 MULTI-SLOT-UNSAFE
If ANY of:
1. Any baseline condition (B_COLD, B_LITERAL, B_PARAM_1SLOT, B_PARAM_2SLOT) produces a different result than specified
2. COMPETE_2VS1 returns param-fetch-posts (1-slot) instead of param-fetch-user-posts (2-slot)
3. COMPETE_TEMPLATE_VS_PARAM returns template-only-fetch instead of param-fetch-posts
4. POS_CONTROL or NULL_CONTROL fails

### 11.3 VERIFY_BROKEN
If ANY of:
1. VERIFY_EMPTY_POSTCONDITIONS returns False
2. VERIFY_STATUS_MISMATCH returns True
3. VERIFY_MULTI_FIELD_MISMATCH returns True
4. VERIFY_FIX_NO_EFFECT shows different results between fixed and unfixed kernels

### 11.4 DEGENERATE
If conditions COMPETE_TEMPLATE_VS_LITERAL, COMPETE_1VS1_EQUAL, COMPETE_0VS0_EQUAL show ID-dependent behavior. This is expected and recorded but not gate-failing.

### 11.5 MEASUREMENT_INVALID
If code fix causes Python exceptions, type errors, or unexpected resolution statuses in any condition.

## 12. Expected Outcomes

### 12.1 MULTI-SLOT-SAFE
The tie-break generalizes to multi-slot mechanisms. C-PARAM-INHERIT advances further. Product registration of multi-slot mechanisms becomes safe at equal confidence. Template-only params are correctly subordinated to declared-slot params. The kernel can handle mechanisms with arbitrary slot counts. verify() correctly handles non-200 responses.

### 12.2 MULTI-SLOT-UNSAFE
The tie-break does not generalize. The `required_slots` vs `parameter_slots` divergence issue needs to be addressed. C-PARAM-INHERIT remains limited to single-slot mechanisms. Alternative tie-break strategies (e.g., len(required_slots) instead of len(parameter_slots)) must be explored.

### 12.3 VERIFY_BROKEN
verify() has a correctness issue. This is a separate finding from the tie-break generalization. If verify() fails on empty postconditions or mismatched states, the kernel's postcondition checking needs repair.

### 12.4 DEGENERATE (Expected)
Equal-slot-count ties are ID-dependent. This is a known limitation. The fix does not resolve degenerate cases, and this is acceptable because:
- Degenerate cases only occur when two mechanisms have identical slot counts
- In practice, mechanisms with identical slot counts but different templates are unlikely to coexist at equal confidence
- If they do coexist, the confidence-based disambiguation or intent matching should distinguish them

## 13. Analysis Plan

1. Apply the one-line fix in the test script for fix conditions; use unfixed kernel for unfixed conditions
2. Run all 15 conditions with fresh kernel instances
3. Record resolution status, winning mechanism, and bound_action for resolution conditions
4. Record verify() boolean for verify conditions
5. Check baselines on unfixed kernel: all 5 must pass
6. Check interventions on fixed kernel: COMPETE_2VS1 and COMPETE_TEMPLATE_VS_PARAM must pass
7. Check degenerate conditions: record ID-dependent behavior
8. Check controls on fixed kernel: both must pass
9. Check verify() conditions: all 4 must pass
10. Determine verdict: MULTI-SLOT-SAFE, MULTI-SLOT-UNSAFE, VERIFY_BROKEN, DEGENERATE, or MEASUREMENT_INVALID

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
