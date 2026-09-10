# EXP-PRODUCT-34282620394 Report

## Executive Summary

**Outcome: MIXED** — C2 full-value binding fix works at the kernel level, but introduces regressions in 4 of 9 regression conditions due to a value-contract incompatibility between the distill-time stripping approach and the test harness.

- **C2 (positive control)**: PASS — binding_accuracy=1.0, template correctly shortened
- **Regression conditions**: 5/9 PASS, 4/9 FAIL (B4, C1, D1, D3)
- **Null controls**: PASS (E1, E2)
- **Literal baseline**: PASS (fail_rate=1.0)

## What Was Tested

The frozen spec required modifying `distill_parameterized()` to detect prefix-only varying segments and induce shorter templates by stripping the slot-level prefix at template construction time. This is distinct from the parent's bind-time approach.

### Implementation Changes

1. **`distill_parameterized()`** (lines 439-455): When `_detect_slot_level_prefix()` identifies a slot-level prefix (e.g., `user-` from training values `user-1`, `user-2`, `user-3`), the prefix is now stripped from the template string. Template becomes `https://api.example.com/users/${url}` instead of `https://api.example.com/users/user-${url}`.

2. **`_bind()`** (lines 38-51): Removed the double-prefix detection logic (former lines 44-66). With distill-time stripping, templates no longer contain slot-level prefixes, so direct `${slot}` substitution works without prefix manipulation.

## C2 Fix Verification

The distill-time fix **works correctly for C2**:

| Metric | Value |
|---|---|
| Template before fix | `https://api.example.com/users/user-${url}` |
| Template after fix | `https://api.example.com/users/${url}` |
| Slot-level prefix detected | `user-` |
| Binding with `url='user-4'` | `https://api.example.com/users/user-4` ✓ |
| Binding with `url='user-5'` | `https://api.example.com/users/user-5` ✓ |
| Binding with `url='user-6'` | `https://api.example.com/users/user-6` ✓ |
| binding_accuracy | 1.0 (3/3) |

The template is correctly shortened. The `user-` prefix is stripped from the template, and full values (`user-4`) are inserted directly into `${url}` without double-prefix.

## Regression Analysis

### Why B4, C1, D1, D3 Fail

The distill-time approach changes the **value contract**: when the template is `${slot}` (prefix stripped), callers MUST pass full values containing the prefix. But the test harness passes **short values** for B4, C1, D1, D3:

| Condition | Template (after strip) | Test param | Expected output | Actual output |
|---|---|---|---|---|
| B4 | `https://${callback_url}.com/hook` | `"d"` | `https://site-d.com/hook` | `https://d.com/hook` ✗ |
| C1 | `https://${callback_url}.com/hook` | `"d"` | `https://site-d.com/hook` | `https://d.com/hook` ✗ |
| D1 | `https://api.example.com/orders/${url}` | `"4"` | `https://api.example.com/orders/order-4` | `https://api.example.com/orders/4` ✗ |
| D3 | `https://api.example.com/orders/${url}` | `"4"` | `https://api.example.com/orders/item-4` | `https://api.example.com/orders/4` ✗ |

### Why B1, B2, B3, B5, D2 Pass

These conditions have training values where the common prefix ends at a path boundary (`/`), so `_detect_slot_level_prefix()` returns empty string and no stripping occurs. Templates remain unchanged.

### Why the Parent's Bind-Time Approach Was More Robust

The parent's `_bind()` double-prefix detection handled BOTH value conventions:
- Short value `"d"` into template `site-${slot}` → `site-d` (no stripping triggered, param doesn't start with last segment)
- Full value `"user-4"` into template `user-${slot}` → stripping triggers → `user-4`

This flexibility is lost with distill-time stripping, which mandates a single convention (full values only).

## Scientific Interpretation

The experiment reveals a **fundamental design tension**:

1. **Distill-time stripping** (this experiment): Produces shorter, cleaner templates. But requires callers to adopt a full-value convention. Breaks backward compatibility with existing callers that pass short values.

2. **Bind-time stripping** (parent approach): Handles both value conventions transparently. More robust for mixed-convention callers. But produces longer templates and relies on runtime prefix detection.

For product use, the choice depends on whether the API can mandate a consistent value convention. If all callers pass full values (e.g., `'user-4'` not `'4'`), distill-time stripping is cleaner. If callers use mixed conventions, bind-time stripping is more robust.

## Decision Rule Application

Per the frozen decision rule:

- C2 binding_accuracy == 1.0 ✓
- BUT 4 of 9 regression conditions FAIL ✗
- Therefore: **C2-FIX-FALSIFIED** (regression failure)

The C2 fix itself works, but the distill-time approach is incompatible with the existing test harness value conventions. This is a MIXED result, not a clean pass or fail.

## Next Steps

Two options for the next experiment:

**Option A**: Revert to bind-time stripping (parent approach) which handles both value conventions. This would pass all 10 conditions without changing the test harness.

**Option B**: Update the test harness to use full values for all conditions (B4: `'site-d'` instead of `'d'`, D1: `'order-4'` instead of `'4'`, etc.). This would make distill-time stripping work across all conditions.

Option A is lower-risk and preserves backward compatibility. Option B is cleaner architecturally but requires updating all callers.
