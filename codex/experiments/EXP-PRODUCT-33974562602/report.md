# EXP-PRODUCT-33974562602 — Kernel Integration Test Report

**Experiment ID**: EXP-PRODUCT-33974562602
**Lane**: Product
**Claim**: C-PARAM-INHERIT
**Status**: COMPLETE
**Outcome**: FALSIFIES (KERNEL-INTEGRATION-FALSIFIED)
**Date**: 2026-09-05

## Executive Summary

The multi-parameter induction function **survives kernel integration** (faithful regression: 21/21 EXECUTABLE, 21/21 binding correct on all 5 synthetic conditions) but **fails on three realistic-input conditions**: full-value unseen parameters produce double-prefix errors, noisy browser observations induce extra spurious slots from noise fields, and unrelated observations still produce hallucinated parameter slots. The kernel integration itself is complete and correct; the algorithm's behavior on realistic inputs reveals fundamental limitations.

## Phase A: Kernel Integration Verification

| Check | Result |
|-------|--------|
| A1: Import kernel after modification | PASS — SpiderKernel imported successfully |
| A2: Run existing tests/test_kernel.py | PASS — 3/3 tests pass |
| A3: Verify distill_parameterized callable | PASS — method exists on SpiderKernel |

**Kernel integration is complete.** The `distill_parameterized()` method is a public method on `SpiderKernel` that delegates to `_extract_varying_values_multi()` (module-level helper). The kernel.py sha256 is `f2e8043d`.

## Phase B: Regression Baseline (5 conditions)

All 5 conditions from EXP-PRODUCT-33741671686 produce **identical results** through the kernel-integrated function:

| Condition | Slots | Distinct | Resolution | Binding |
|-----------|-------|----------|------------|---------|
| B1: Single-path | 1 | ✓ | 5/5 (100%) | 5/5 (100%) |
| B2: Path+body | 2 | ✓ | 5/5 (100%) | 5/5 (100%) |
| B3: Path+body+headers | 3 | ✓ | 5/5 (100%) | 5/5 (100%) |
| B4: Non-identifier URLs | 1 | ✓ | 3/3 (100%) | 3/3 (100%) |
| B5: Shared-slot collision | 2 | ✓ | 3/3 (100%) | 3/3 (100%) |

**Total: 21/21 EXECUTABLE, 21/21 binding correct.** This matches EXP-PRODUCT-33741671686 exactly. The kernel integration is faithful.

**Interpretation**: The function behaves identically when called as `kernel.distill_parameterized()` vs the standalone `distill_parameterized_v2()`. The integration introduced no bugs.

## Phase C: Full-Value Unseen Tests

### C1: Full-value URLs

- Training: 3 observations of `POST /webhooks` with `callback_url: https://site-{a,b,c}.com/hook`
- Template: `https://site-${callback_url}.com/hook` (prefix="https://site-", suffix=".com/hook")
- Unseen: caller supplies FULL URLs: `https://site-d.com/hook`, `https://site-e.com/hook`, `https://site-f.com/hook`
- **Result: 0% binding accuracy.** All 3 resolve EXECUTABLE but produce double-prefix: `https://site-https://site-d.com/hook.com/hook`

**Root cause**: The template expects the varying middle (`d`) but the caller supplies the full value (`https://site-d.com/hook`). The `_bind()` function substitutes the full value into `${callback_url}`, producing the double-prefix. This confirms the prefix extraction is circular when the caller supplies full values.

### C2: Full-value IDs with prefix

- Training: 3 observations of `GET /users/user-{1,2,3}`
- Template: `https://api.example.com/users/user-${url}` (prefix="https://api.example.com/users/user-")
- Unseen: caller supplies full IDs: `user-4`, `user-5`, `user-6`
- **Result: 0% binding accuracy.** All 3 resolve EXECUTABLE but produce `https://api.example.com/users/user-user-4` (double prefix)

**Same root cause**: The template expects the varying middle (`4`) but the caller supplies `user-4`.

**Interpretation**: The full-value unseen test reveals a design limitation: the prefix/suffix extraction creates a template that expects the varying middle only, but real callers may supply full values. The function has no mechanism to detect whether the supplied value already contains the prefix/suffix.

## Phase D: Noisy Browser-Like Observations

### D1: Noisy POST with path+body+headers

- Training: 3 observations with extra fields: `timestamp`, `request_duration_ms`, `retry_count`, `user_agent`
- Expected slots: 3 (order, customer, request_id)
- **Observed: 6 slots** (url, customer, x_request_id, timestamp, request_duration_ms, retry_count)
- Resolution: 0% (unseen params don't include noise fields)

### D2: Noisy GET with path+query

- Training: 3 observations with extra fields: `response_time_ms`, `cache_hit`, `result_count`
- Expected slots: 2 (q, page)
- **Observed: 4 slots** (url, cache_hit, response_time_ms, result_count)
- Resolution: 0%

### D3: Multi-step with varying preconditions

- Training: 3 observations with different `session_id` and `auth_token` in state
- Expected slots: 2 (transfer_id, amount)
- **Observed: 2 slots** (url, amount) — correct count
- Resolution: 0% (preconditions vary, resolve() cannot match)

**Root cause**: The induction function treats every varying field as a parameter slot, regardless of whether it's signal (order_id, customer, request_id) or noise (timestamp, retry_count, user_agent). The function has no concept of "this field varies but shouldn't be parameterized."

**Interpretation**: Real browser session data contains many varying fields (timestamps, metadata, session state) that are not part of the action template. The function induces slots from all varying fields, creating an over-parameterized mechanism that fails on unseen data.

## Phase E: Null Controls (Pattern Absence)

### E1: Unrelated action structures

- Training: 3 observations with completely different structures:
  - `POST /api/payments` with `body: {amount: 100, currency: "USD"}`
  - `GET /api/users/42`
  - `DELETE /api/sessions/abc-123`
- Expected: slot_count=0 (no common pattern)
- **Observed: 4 slots** (amount, method, session_id, url)
- Resolution: N/A (hallucinated slots)

**Root cause**: The function detects varying fields by checking if values differ across observations. Since the 3 observations have different structures, many fields appear "varying" (they exist in some observations but not others). The function induces slots from these phantom variations.

### E2: Single observation

- Training: 1 observation only
- Expected: slot_count=0 (cannot induce from single observation)
- **Observed: 0 slots** (no mechanism induced)

**Result: PASS.** The function correctly requires at least 2 observations.

## Baseline: B_LITERAL

Literal mechanism (no parameter slots) from `kernel.distill()`: **5/5 EXPLORE** on unseen multi-param combinations. This confirms parameterization is still necessary after integration.

## Decision Rule Application

| Check | Expected | Observed | Result |
|-------|----------|----------|--------|
| B1 regression (slot≥1, resolution≥0.9, binding≥0.9) | Pass | slot=1, res=1.0, bind=1.0 | ✓ |
| B2 multi-param (slot≥2, distinct, res≥0.9, bind≥0.9) | Pass | slot=2, distinct, res=1.0, bind=1.0 | ✓ |
| B3 three-param (slot≥3, distinct, res≥0.9, bind≥0.9) | Pass | slot=3, distinct, res=1.0, bind=1.0 | ✓ |
| B4 non-identifier (slot≥1, res≥0.9, bind≥0.9) | Pass | slot=1, res=1.0, bind=1.0 | ✓ |
| B5 no-collision (slot≥2, distinct, res≥0.9, bind≥0.9) | Pass | slot=2, distinct, res=1.0, bind=1.0 | ✓ |
| C1 full-value URLs (distill, res≥0.9, bind≥0.9) | Pass | distill=True, res=1.0, bind=0.0 | ✗ |
| C2 full-value IDs (distill, res≥0.9, bind≥0.9) | Pass | distill=True, res=1.0, bind=0.0 | ✗ |
| D1 noisy POST (slot≥3, res≥0.9, bind≥0.9) | Pass | slot=6, res=0.0, bind=0.0 | ✗ |
| D2 noisy GET (slot≥2, res≥0.9, bind≥0.9) | Pass | slot=4, res=0.0, bind=0.0 | ✗ |
| D3 varying preconditions (slot≥2, res≥0.9, bind≥0.9) | Pass | slot=2, res=0.0, bind=0.0 | ✗ |
| E1 pattern absence (slot_count=0) | Pass | slot_count=4 | ✗ |
| E2 single obs (slot_count=0) | Pass | slot_count=0 | ✓ |
| No crashes | Pass | All conditions distilled successfully | ✓ |

**Verdict: KERNEL-INTEGRATION-FALSIFIED** — 6 of 13 checks fail.

## Product Consequence

C-PARAM-INHERIT **does not advance** beyond experiment-script-only POC for realistic inputs. The kernel integration itself is complete and faithful, but the algorithm has three distinct failure modes:

1. **Double-prefix error** (C1/C2): Full-value unseen parameters produce incorrect bindings. The function works correctly only when callers supply the varying middle, not the full value.
2. **Noise sensitivity** (D1/D2/D3): Extra fields in training observations induce spurious parameter slots. The function cannot distinguish signal from noise.
3. **Pattern hallucination** (E1): Unrelated observations produce hallucinated parameter slots. The function has no mechanism for detecting "these observations are unrelated."

**Smallest next action**: Fix the noise sensitivity issue (D1/D2) by adding a heuristic that ignores fields whose values don't follow the prefix/suffix pattern of the majority of varying fields. This is the most impactful fix because it would also address E1 (unrelated observations produce slots with no common prefix/suffix pattern).

**Do NOT promote to Product Core.** The kernel-integrated function produces correct results on clean synthetic data but fails on realistic inputs.
