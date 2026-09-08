# EXP-PRODUCT-34195008089 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34195008089
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Parent**: EXP-PRODUCT-34015741916 (KERNEL-INTEGRATION-PARTIAL)
- **Date**: 2026-09-08
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can the C2 double-prefix bug be fixed by modifying `_bind()` in `src/spider/kernel.py` to detect when a full-value parameter already contains the template prefix and strip it before substitution, such that binding `user-${url}` with `params={'url':'user-4'}` produces `user-4` (not `user-user-4`), and all 10 test conditions continue to pass?

## 3. Motivation

EXP-PRODUCT-34015741916 achieved KERNEL-INTEGRATION-PARTIAL: 9/10 synthetic conditions pass, C2 fails the spec-required full-value binding test.

**Root cause**: Template `user-${url}` with `params={'url':'user-4'}` produces `user-user-4` because `_bind()` unconditionally substitutes `${url}` → `user-4` without detecting the prefix duplication. The `_detect_double_prefix` function exists in kernel.py (lines 223-244) but is dead code — the guard `if not _PARAMETER.search(url_template)` in Step 4 (lines 404-414) is always False because the template already contains `${url}`.

**Parent audit recomputation**: `kernel.resolve('get-user', {}, params={'url':'user-4'})` → `'https://api.example.com/users/user-user-4'` (binding_correct false).

**Why this is the highest-upside next step**: C2 is the sole blocker preventing KERNEL-INTEGRATION-SURVIVES. Fixing it completes the kernel integration gate and enables product economics testing.

## 4. Proposed Fix

### 4.1 Approach: Prefix-strip in `_bind()`

Modify `_bind()` in `src/spider/kernel.py` to detect when a full-match parameter value already starts with the template's literal prefix and strip it before substitution.

**Current `_bind()` behavior** (lines 35-49):
```python
def _bind(value: Any, params: dict[str, Any]) -> Any:
    if isinstance(value, str):
        full = _PARAMETER.fullmatch(value)
        if full:
            return params[full.group(1)]
        def replace(match: re.Match[str]) -> str:
            return str(params[match.group(1)])
        return _PARAMETER.sub(replace, value)
    ...
```

For template `user-${url}` with `params={'url': 'user-4'}`:
- `_PARAMETER.fullmatch('user-${url}')` → None (not a pure template)
- `_PARAMETER.sub(replace, 'user-${url}')` → `'user-' + 'user-4'` = `'user-user-4'` ← BUG

**Proposed fix**: Before substitution, detect the template's literal prefix (text before `${...}`), check if the param value starts with that prefix, and strip it.

```python
def _bind(value: Any, params: dict[str, Any]) -> Any:
    if isinstance(value, str):
        full = _PARAMETER.fullmatch(value)
        if full:
            return params[full.group(1)]

        # Detect prefix overlap: if template has prefix before ${slot}
        # and param value starts with that prefix, strip it to avoid
        # double-prefix (e.g., user-${url} + url='user-4' → user-4)
        prefix_match = re.match(r'^([^$]*)\$\{', value)
        if prefix_match:
            template_prefix = prefix_match.group(1)
            # Check if any param value starts with template prefix
            for slot, val in params.items():
                if isinstance(val, str) and val.startswith(template_prefix) and len(val) > len(template_prefix):
                    params = {k: v[len(template_prefix):] if k == slot else v
                              for k, v in params.items()}
                    break

        def replace(match: re.Match[str]) -> str:
            return str(params[match.group(1)])
        return _PARAMETER.sub(replace, value)
    ...
```

### 4.2 Why this approach

1. **Minimal**: Only modifies `_bind()`, ~8 lines of new code
2. **Localized**: No changes to `distill_parameterized()` template construction
3. **Testable**: C2 is the discriminating test case
4. **Reversible**: If it causes regressions, revert is trivial

### 4.3 Why NOT fix `_detect_double_prefix` wiring

The parent audit identified that `_detect_double_prefix` is dead code. However, wiring it into `_bind()` or `resolve()` requires understanding its intended semantics (which are unclear from the code: it returns `(stripped, detected_slot)` but the caller never uses it). The prefix-strip approach in `_bind()` is simpler and more directly addresses the product requirement.

## 5. Test Harness Correction

The parent test harness `c2_unseen()` returns `[{'url':'4'}]` (stripped), not `[{'url':'user-4'}]` (full value) per spec. The corrected harness must use full values:

```python
def c2_unseen():
    """C2: pass full values per spec (not stripped)."""
    return [{"url": "user-4"},
            {"url": "user-5"},
            {"url": "user-6"}]
```

The `c2_expected()` function remains unchanged (expects `user-4`, `user-5`, `user-6` in the URL).

## 6. Hypotheses

### H1: C2 Fix Works
After the `_bind()` prefix-strip modification, `kernel.resolve('get-user', {}, params={'url':'user-4'})` produces `{'url': 'https://api.example.com/users/user-4'}` with `binding_correct=true`.

### H2: No Regression
All 9 conditions that passed in EXP-PRODUCT-34015741916 continue to pass with identical slot counts and binding_accuracy=1.0.

### H3: No Over-Strip
C1 (prefix+suffix template `https://site-${url}.com/hook`) is not affected by the prefix-strip logic. The param value `d` does not start with `https://site-`, so no stripping occurs. C1 continues to pass.

## 7. Conditions

### Phase B: Regression Baseline (must all pass)
- B1: single-path URL (slot_count=1, binding_accuracy=1.0)
- B2: path+body (slot_count=2, binding_accuracy=1.0)
- B3: path+body+headers with hyphen param (slot_count=3, binding_accuracy=1.0)
- B4: non-identifier values (slot_count=1, binding_accuracy=1.0)
- B5: shared slot name, static A,A,A (slot_count=1 [url], binding_accuracy=1.0)

### Phase C: Full-Value Binding (C2 is discriminating)
- C1: prefix+suffix URLs (slot_count=1, binding_accuracy=1.0, no over-strip)
- C2: prefix-only IDs with full values (slot_count=1, binding_accuracy=1.0, bound='user-4' not 'user-user-4')

### Phase D: Noisy Browser (must all pass)
- D1: noisy POST with metadata (slot_count=3, metadata excluded)
- D2: noisy GET with metadata (slot_count=1 [url], metadata excluded)
- D3: varying preconditions, static quantity (slot_count=1 [url])

### Phase E: Null Controls (must all pass)
- E1: pattern absence (slot_count=0)
- E2: single observation (slot_count=0)

### Baseline: Literal replay (must fail)
- B_LITERAL: literal mechanism fails on all unseen combinations

## 8. Decision Rules

### C2-FIX-SURVIVES
If ALL of:
1. B1-B5 correct slot counts with binding_accuracy=1.0
2. C1 slot_count=1, binding_accuracy=1.0
3. C2 slot_count=1, binding_accuracy=1.0, bound URL contains 'user-4' (not 'user-user-4')
4. D1 slot_count=3, metadata excluded
5. D2 slot_count=1 [url], metadata excluded
6. D3 slot_count=1 [url]
7. E1 slot_count=0
8. E2 slot_count=0
9. Literal baseline fail_rate=1.0

### C2-FIX-FALSIFIED
If C2 fails (binding_accuracy < 1.0 or bound URL contains 'user-user-4') but all other 9 conditions pass.

### C2-FIX-REGRESSED
If any condition other than C2 regresses from parent results.

### MEASUREMENT_INVALID
If infrastructure prevents execution or distill_parameterized() crashes.

## 9. Validity Threats

### 9.1 Over-Strip Risk
The prefix-strip logic might incorrectly strip a legitimate prefix from C1 or other conditions. Mitigation: C1 template `https://site-${url}.com/hook` has param value `d` which does not start with `https://site-`, so no strip occurs. The fix is gated on `val.startswith(template_prefix) and len(val) > len(template_prefix)`.

### 9.2 Synthetic Only
All 10 conditions use deterministic synthetic data. No external validity to real browser observations. This is by design — kernel integration is validated synthetically first.

### 9.3 Minimal Fix Scope
Only `_bind()` is modified. If the fix works, it does not prove the approach generalizes to other double-prefix patterns (e.g., suffix-only templates, multi-parameter templates). Those are separate follow-ups.

### 9.4 Test Harness Change
The harness correction (c2_unseen returning full values) is a spec-compliance fix, not a scientific variable change. The parent harness was wrong per spec; this corrects it.

## 10. Carry-Forward from Parent

### Established (inherited from EXP-PRODUCT-34015741916)
- B1-B5 regression preserved in kernel: slot counts correct, binding_accuracy=1.0
- C1 prefix+suffix full-value URL binding works
- D1/D2/D3 noise filtering works for top-level metadata
- E1/E2 null controls hold
- Literal mechanism replay fails (fail_rate=1.0)
- _PARAMETER regex hyphen fix is genuine and necessary

### Rejected (inherited)
- C2 full-value binding with prefix-containing params works — FALSIFIED (parent audit)
- _detect_double_prefix is functional code — REJECTED (dead code)
- Test harness tests full-value binding as spec requires — FALSIFIED (uses stripped parts)

### Unknown (inherited)
- Whether nested metadata filtering requires recursive allowlist/denylist
- Whether constant-value anchor is independently necessary
- What full-value C2 binding semantics should be for product use

### Do Not Assume (inherited)
- C-PARAM-INHERIT is product-ready (C2 was broken, this experiment tests the fix)
- Nested metadata inside body/headers is excluded
- Result transfers to real browser observations

## 11. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 12. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
