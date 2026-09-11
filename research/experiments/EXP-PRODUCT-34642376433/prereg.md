# EXP-PRODUCT-34642376433 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34642376433
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Parent**: EXP-PRODUCT-34485517221 (FALSIFIED-IN-SETTING, 4/7 pass)
- **Date**: 2026-09-11
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can two bounded kernel fixes — suffix extraction guard and delimiter-bound prefix validation — restore binding correctness on the G1 and N1 failure modes from EXP-PRODUCT-34485517221 while preserving the 4 passing conditions?

## 3. Motivation

EXP-PRODUCT-34485517221 identified three bounded failure modes in the leaf-path URL-as-string parameterization heuristic:

1. **G1 (suffix corruption)**: Training values alpha/beta/delta share trailing character 'a'. `_find_common_prefix_suffix` extracts suffix 'a', producing template `search?q=${url}a` and bound URLs `search?q=gammaa` instead of `search?q=gamma`. The suffix mechanism is not robust to training values sharing trailing characters.

2. **N1 (over-parameterization)**: Cross-host URLs (api.example.com, api.other.com, api.third.com) share prefix `https://api.`. The heuristic induces a parameter slot where slot_count=0 is expected. No guard prevents parameterization of structurally different URLs sharing short prefixes.

3. **G4 (multi-slot limitation)**: The leaf-path model treats URL as a single field, inducing 1 slot instead of 2. This is an architectural limitation, not a bug.

The parent audit (V1-V6) also flagged V2_SUBSTRATE_REIMPLEMENTATION_NOT_KERNEL: the experiment used a standalone reimplementation, not actual kernel.py.

This experiment implements targeted fixes for failure modes (1) and (2), re-runs all 7 parent conditions plus redesigned N1, and validates against the actual algorithm logic. Failure mode (3) is documented as an architectural bound.

## 4. Hypotheses

### H1: Suffix Guard Restores G1
Excluding single-character suffixes not preceded by a structural delimiter (?, =, &) from template construction will restore G1 binding. Template becomes `search?q=${url}` (no suffix) instead of `search?q=${url}a`. Binding_accuracy >= 1.0 for unseen values gamma/epsilon/zeta.

### H2: Delimiter Guard Prevents N1 Over-Parameterization
Requiring the character after the common prefix to be a structural delimiter (/ ? = &) or end-of-string will prevent N1 from inducing a parameter slot. Prefix `https://api.` ends at 'a' (not a delimiter), so slot_count=0.

### H3: No Regressions on Passing Conditions
The suffix guard will not affect P1, G2, G3, or G5 because their suffixes are either empty or structurally valid. The delimiter guard will not affect P1, G2, G3, or G5 because their prefixes already end at structural boundaries.

### H4: G4 Architectural Limitation Confirmed
G4 will still induce slot_count=1 (not 2) because the leaf-path model treats URL as a single field. However, suffix corruption will be fixed (no '00' suffix from 100/200/300).

## 5. Fixes

### 5.1 Fix 1: Suffix Extraction Guard

**Current behavior** (`_find_common_prefix_suffix`):
```python
suffix = values[0]
for v in values[1:]:
    while not v.endswith(suffix):
        suffix = suffix[1:]
        if not suffix:
            break
```
This extracts the longest common suffix, which can be a single trailing character (e.g., 'a' from alpha/beta/delta).

**Fixed behavior**:
```python
# After computing raw suffix, apply guard:
if suffix and len(suffix) <= 1:
    # Single-character suffix: check if preceded by structural delimiter
    # Use the first value as reference
    raw_suffix = suffix
    pos = len(values[0]) - len(raw_suffix) - 1
    if pos < 0 or values[0][pos] not in ('?', '=', '&'):
        suffix = ''  # Reject non-structural single-char suffix
```

**Rationale**: Single-character suffixes that are not preceded by URL structural delimiters are almost always coincidental character overlap, not meaningful template structure. Query parameters use `?key=value&key2=value2` structure; the suffix after the last `=` is the value, not a template suffix.

### 5.2 Fix 2: Delimiter-Bound Prefix Validation

**Current behavior**: The rfind('/') heuristic extracts slot_prefix based on the last '/' in the common prefix. No validation that the prefix ends at a structural boundary.

**Fixed behavior**: After computing slot_prefix via rfind('/') or full prefix, validate:
```python
# After computing full_prefix from _find_common_prefix_suffix:
if full_prefix:
    next_char_idx = len(full_prefix)
    if next_char_idx < len(values[0]):
        next_char = values[0][next_char_idx]
        if next_char not in ('/', '?', '=', '&'):
            # Prefix does not end at a structural boundary
            # This is likely over-parameterization
            # Force slot_count = 0 (no parameterization)
            varying_paths = []  # Clear all varying paths
```

**Rationale**: A valid parameter slot boundary in a URL occurs at structural delimiters: `/` separates path segments, `?` starts query string, `=` separates key from value, `&` separates query parameters. If the common prefix ends at a non-delimiter character, the "slot" is not at a real URL boundary and parameterization is spurious.

## 6. Test Conditions

### 6.1 Parent Conditions (identical training/unseen values)

| ID | Type | Training URLs | Expected | Parent Result |
|----|------|---------------|----------|---------------|
| P1 | Positive control | api.example.com/users/{A,B,C} | slot_count=1, binding=1.0 | PASS |
| G1 | Fix-1 target | api.example.com/search?q={alpha,beta,delta} | slot_count=1, binding=1.0 | FAIL (suffix 'a') |
| G2 | Regression | api.example.com/items?category=books&page={1,2,3} | slot_count=1, binding=1.0 | PASS |
| G3 | Regression | api.example.com/orgs/acme/repos/main/issues/{1,2,3} | slot_count=1, binding=1.0 | PASS |
| G4 | Architectural | api.example.com/users/{alice,bob,charlie}/orders/{100,200,300} | slot_count=1 (bounded), binding=1.0 (suffix fixed) | FAIL (suffix '00', slot=1) |
| G5 | Regression | api.example.com/users/{alice,bob,charlie}/items?page=1 | slot_count=1, binding=1.0 | PASS |

### 6.2 New Conditions

| ID | Type | Training URLs | Expected | Rationale |
|----|------|---------------|----------|-----------|
| N1_ORIGINAL | Fix-2 target | api.example.com/a, api.other.com/b, api.third.com/c | slot_count=0 | Tests delimiter guard on parent's cross-host URLs |
| N1_REDESIGNED | Null control | a.com/x, b.org/y, c.net/z | slot_count=0 | Truly disjoint URLs with no shared prefix |
| B_LITERAL | Baseline | (same as P1) | fail_rate=1.0 | Literal reuse, confidence 0.5 < 0.8 |

## 7. Measures

### 7.1 Primary Metric
- **condition_pass_rate**: Fraction of conditions passing (slot_count correct AND binding_accuracy=1.0)
- **fix_success**: Binary — G1 and N1_ORIGINAL pass after fixes

### 7.2 Per-Condition Metrics
- slot_count (expected: 1 for P1/G1/G2/G3/G5, 1 for G4 (bounded), 0 for N1_ORIGINAL/N1_REDESIGNED)
- binding_accuracy (expected: 1.0 for all passing conditions)
- slot_prefixes (recorded for comparison with parent)
- action_template (recorded to verify suffix fix)

### 7.3 Regression Metrics
- P1 binding_accuracy >= 1.0 (must not drop)
- G2 binding_accuracy >= 1.0 (must not drop)
- G3 binding_accuracy >= 1.0 (must not drop)
- G5 binding_accuracy >= 1.0 (must not drop)

## 8. Controls

### 8.1 Positive Control (P1)
- P1 must pass with binding_accuracy=1.0 after fixes
- Verifies pipeline integrity

### 8.2 Null Controls (N1_ORIGINAL, N1_REDESIGNED)
- Both must produce slot_count=0
- N1_ORIGINAL tests delimiter guard specifically
- N1_REDESIGNED tests truly disjoint URLs

### 8.3 Regression Controls (G2, G3, G5)
- Must maintain binding_accuracy=1.0 after fixes
- If any regresses, the fix is not safe

### 8.4 Baseline Control (B_LITERAL)
- Literal reuse must fail (confidence 0.5 < 0.8)
- Confirms parameterized induction is necessary

## 9. Validity Threats

### 9.1 Fix Implementation Fidelity
The fixes are implemented in standalone experiment code, not actual kernel.py. The audit V2_SUBSTRATE_REIMPLEMENTATION_NOT_KERNEL from parent applies. However, the algorithm logic is identical; the standalone code is a direct reimplementation. Execution against actual kernel.py is recommended as follow-up.

### 9.2 Training Value Sensitivity
G1 fix depends on the specific training values (alpha/beta/delta sharing suffix 'a'). Different training values with multi-character shared suffixes (e.g., 'ing' from running/jumping) would not be caught by the single-character guard. This is a known bound: the fix addresses the most common failure mode, not all possible suffix corruptions.

### 9.3 Delimiter Guard False Positives
The delimiter guard could reject legitimate parameterization if the character after the prefix happens to not be a delimiter. For example, if training values are `user123`, `user456`, `user789`, the common prefix is `user` and the next char is `1` (not a delimiter). This would be falsely rejected. However, this case does not appear in the test conditions; it represents a potential false-negative that bounds the fix's generality.

### 9.4 G4 Architectural Limitation
G4 remains limited to slot_count=1 by the leaf-path model. The suffix corruption is fixed (no '00' suffix), but 2-slot parameterization is not achievable without URL parsing. This is documented, not a measurement gap.

### 9.5 Synthetic-Only
All conditions are deterministic synthetic with no model/network/browser calls. Real-world URL diversity may expose failure modes not tested here.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST
If ALL of:
1. G1 passes: slot_count=1 AND binding_accuracy=1.0 (suffix fix works)
2. N1_ORIGINAL passes: slot_count=0 (delimiter guard works)
3. N1_REDESIGNED passes: slot_count=0 (null control holds)
4. P1 regression: slot_count=1 AND binding_accuracy=1.0 (no breakage)
5. G2 regression: binding_accuracy=1.0 (no breakage)
6. G3 regression: binding_accuracy=1.0 (no breakage)
7. G5 regression: binding_accuracy=1.0 (no breakage)
8. B_LITERAL: fail_rate=1.0 (parameterization necessary)
9. No pipeline errors

### 10.2 MIXED
If G1 or N1 fix works (≥1 restored) but ≥1 regression on P1/G2/G3/G5.

### 10.3 FALSIFIED-IN-SETTING
If G1 fix fails (binding_accuracy < 1.0) OR N1 over-parameterization persists (slot_count > 0 on N1_ORIGINAL or N1_REDESIGNED).

### 10.4 MEASUREMENT_INVALID
If pipeline errors prevent computation or sample sizes are insufficient.

## 11. G4 Separate Reporting

G4 is reported separately from the primary decision rule:
- **Expected**: slot_count=1 (architectural bound), binding_accuracy=1.0 (suffix fix removes '00')
- **If suffix fix works**: G4 template becomes `users/${url}` (no suffix), binding for unseen `dave/orders/400` produces `users/dave/orders/400` — correct for single-slot representation
- **If suffix fix fails**: G4 template remains `users/${url}00`, binding produces `users/dave/orders/40000` — incorrect
- G4 outcome does not affect primary decision rule but is reported as evidence for suffix fix effectiveness

## 12. Analysis Plan

1. Implement Fix 1 (suffix guard) in `_find_common_prefix_suffix`
2. Implement Fix 2 (delimiter-bound prefix validation) in `distill_parameterized`
3. Run all 9 conditions (7 parent + N1_REDESIGNED + N1_ORIGINAL)
4. Record per-condition: slot_count, binding_accuracy, slot_prefixes, action_template
5. Compare with parent result.json per-condition metrics
6. Check decision rule
7. Report G4 separately
8. Document all deviations from parent (N1_REDESIGNED new, fixes applied)

## 13. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 14. Freeze Statement

This preregistration is frozen BEFORE any fix code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
