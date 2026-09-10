# EXP-PRODUCT-34195008089 — Report

## Executive Summary

**Verdict: C2-FIX-FALSIFIED**

The `_bind()` prefix-strip fix proposed in the preregistration does **not** fix the C2 double-prefix bug. The C2 condition fails with `binding_accuracy=0.0` — all 3 test cases produce `user-user-4` instead of `user-4`. All 9 other conditions pass with no regressions.

## What Was Tested

The frozen experiment tested whether a minimal modification to `_bind()` in `src/spider/kernel.py` — detecting when a parameter value already starts with the template's literal prefix and stripping it before substitution — would fix C2 full-value binding without breaking any of the 9 conditions that already pass.

## Results

| Condition | Expected | Observed | Binding Accuracy | Status |
|-----------|----------|----------|------------------|--------|
| B1 | slot_count=1 | slot_count=1 | 1.0 (5/5) | PASS |
| B2 | slot_count=2 | slot_count=2 | 1.0 (5/5) | PASS |
| B3 | slot_count=3 | slot_count=3 | 1.0 (5/5) | PASS |
| B4 | slot_count=1 | slot_count=1 | 1.0 (3/3) | PASS |
| B5 | slot_count=1 | slot_count=1 | 1.0 (3/3) | PASS |
| C1 | slot_count=1, no over-strip | slot_count=1 | 1.0 (3/3) | PASS |
| **C2** | **slot_count=1, 'user-4' not 'user-user-4'** | **slot_count=1, 'user-user-4'** | **0.0 (0/3)** | **FAIL** |
| D1 | slot_count=3, metadata excluded | slot_count=3 | 1.0 (3/3) | PASS |
| D2 | slot_count=1, metadata excluded | slot_count=1 | 1.0 (3/3) | PASS |
| D3 | slot_count=1 [url] | slot_count=1 | 1.0 (1/1) | PASS |
| E1 | slot_count=0 | slot_count=0 | N/A | PASS |
| E2 | slot_count=0 | slot_count=0 | N/A | PASS |
| Literal | fail_rate=1.0 | fail_rate=1.0 | N/A | PASS |

**Overall: 31/35 binding correct (88.6%). C2 is the sole failure.**

## Root Cause Analysis

### Why the fix didn't work

The preregistration proposed a fix that checks if the parameter value starts with the template's literal prefix:

```python
prefix_match = re.match(r'^([^$]*)\$\{', value)
if prefix_match:
    template_prefix = prefix_match.group(1)
    for slot, val in params.items():
        if isinstance(val, str) and val.startswith(template_prefix) and len(val) > len(template_prefix):
            params = {k: v[len(template_prefix):] if k == slot else v ...}
```

The prereg assumed the template prefix would be short (e.g., `user-`). But `distill_parameterized()` induces the **full common prefix** from the training data:

- Training URLs: `https://api.example.com/users/user-1`, `user-2`, `user-3`
- Common prefix: `https://api.example.com/users/user-`
- Induced template: `https://api.example.com/users/user-${url}`

When binding with `params={'url': 'user-4'}`:
- Template prefix: `https://api.example.com/users/user-`
- Param value: `user-4`
- `user-4`.startswith(`https://api.example.com/users/user-`) → **False**
- Strip logic never triggers
- Result: `https://api.example.com/users/user-user-4` ❌

### The fix is structurally inert

The fix's condition (`val.startswith(template_prefix) AND len(val) > len(template_prefix)`) is **False for every condition in the experiment**. The fix code executes but does nothing. This is why there are no regressions — the fix is dead code in this context.

### What would actually fix C2

The C2 problem is that the induced template `user-${url}` has a prefix `user-` that overlaps with the full-value param `user-4`. Two possible fix strategies:

1. **Modify `distill_parameterized()`**: Detect when the template prefix matches a common prefix of the param values being bound, and strip the prefix from the template (inducing `${url}` instead of `user-${url}`). This changes template construction, not just binding.

2. **Modify `_bind()` differently**: Instead of checking if the param value starts with the template prefix, check if the param value starts with the **slot name's typical prefix pattern** (e.g., if slot is `url` and the template is `user-${url}`, check if param value starts with `user-`). This requires understanding the relationship between the slot name and the template prefix.

## No Regressions

The fix modification does not break any condition that previously passed. The prefix-strip code only triggers when `val.startswith(template_prefix) AND len(val) > len(template_prefix)`, which is False for all passing conditions. The fix is inert — it exists but does nothing.

## Validity

- All 10 conditions are synthetic deterministic data (no model/network/browser calls)
- C2 tested with full values (`user-4`, `user-5`, `user-6`) per spec
- Binding correctness uses strict JSON comparison
- The fix was applied exactly as proposed in the preregistration
- No deviations from preregistered methodology

## Carry-Forward

### Established (from this experiment)
- B1-B5 regression preserved: slot counts correct, binding_accuracy=1.0
- C1 prefix+suffix binding works (no over-strip)
- D1/D2/D3 noise filtering works
- E1/E2 null controls hold
- Literal baseline fails (fail_rate=1.0)
- The `_bind()` prefix-strip fix is structurally inert (does nothing)

### Rejected
- The `_bind()` prefix-strip approach for C2 — FALSIFIED: fix does not work for induced templates with long prefixes
- C2 full-value binding with prefix-containing params works — still FALSIFIED

### Unknown
- Whether modifying `distill_parameterized()` to handle prefix-only templates would fix C2
- Whether a different `_bind()` approach (checking slot name patterns, not template prefix) would work
- What the correct C2 binding semantics should be for product use

### Do Not Assume
- C-PARAM-INHERIT is product-ready — C2 is still broken
- The C2 bug can be fixed at bind time only — may require template construction changes
- Real browser observations would produce the same induced templates
