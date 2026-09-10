# EXP-PRODUCT-34282620394 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34282620394
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Parent**: EXP-PRODUCT-34195008089 (C2-FIX-FALSIFIED)
- **Date**: 2026-09-08
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can C2 full-value binding be fixed by modifying `distill_parameterized()` to detect prefix-only varying segments and induce shorter templates, such that binding `user-${url}` with `params={'url':'user-4'}` produces `user-4` not `user-user-4`, and all 10 conditions pass?

## 3. Motivation

### 3.1 Prior Work

| Experiment | Attempt | Root Cause | Verdict |
|---|---|---|---|
| EXP-PRODUCT-34015741916 | Kernel integration | `distill_parameterized()` not in kernel.py HEAD | KERNEL-INTEGRATION-PARTIAL (9/10) |
| EXP-PRODUCT-34195008089 | `_bind()` prefix-strip | Template prefix is full path (`https://api.example.com/users/user-`), not short prefix (`user-`); `val.startswith(template_prefix)` always False | C2-FIX-FALSIFIED |

### 3.2 Root Cause Analysis

The parent experiment identified the precise root cause:

1. `distill_parameterized()` computes the longest common prefix of varying values at each path
2. For C2 training data (`user-1`, `user-2`, `user-3`), the common prefix at the URL path is `https://api.example.com/users/user-`
3. The induced template is `https://api.example.com/users/user-${url}`
4. When binding with `params={'url': 'user-4'}`, `_bind()` substitutes: `https://api.example.com/users/user-${url}` → `https://api.example.com/users/user-user-4`
5. The double-prefix occurs because `user-4` already contains the prefix `user-` that is also in the template

### 3.3 Proposed Fix Strategy

**Strategy A (Primary)**: Modify `distill_parameterized()` to detect when the varying segment's common prefix is a **slot-level prefix** (part of the varying values' identity) rather than a **structural prefix** (part of the URL path architecture). When detected, strip the slot-level prefix from the template and store it as a metadata annotation.

**Detection algorithm**:
1. After computing the longest common prefix of varying values at a path, check if the prefix ends with a boundary character (e.g., `-`, `/`, `_`, `.`, space) OR if the prefix is followed by a digit/letter pattern that suggests it's part of an identifier
2. If the prefix is a proper prefix of ALL varying values AND removing it leaves a non-empty segment, the prefix is a slot-level prefix
3. Strip the slot-level prefix from the template: `https://api.example.com/users/user-${url}` → `https://api.example.com/users/${url}`
4. At bind time, the slot value (`user-4`) is inserted directly: `https://api.example.com/users/user-4` ✓

**Strategy B (Fallback)**: If Strategy A introduces regressions, modify `_bind()` to compute slot-specific prefix from the distribution of training values at the path level (not from the full template string) and strip accordingly.

### 3.4 Why This Fix Is Different From Parent

The parent fix modified `_bind()` to check `val.startswith(template_prefix)`. This failed because:
- Template prefix = `https://api.example.com/users/user-` (full path)
- Param value = `user-4`
- `user-4`.startswith(`https://api.example.com/users/user-`) → False

The new fix modifies `distill_parameterized()` to produce a shorter template:
- Template prefix = `https://api.example.com/users/` (structural only)
- Template = `https://api.example.com/users/${url}`
- Param value = `user-4`
- Binding: `https://api.example.com/users/user-4` ✓

## 4. Hypotheses

### H1: C2 Fix Works
C2 full-value binding produces correct URLs (user-4 not user-user-4) with binding_accuracy=1.0.

### H2: No Regression
All 9 previously-passing conditions (B1-B5, C1, D1-D3) maintain correct slot counts and binding_accuracy=1.0.

### H3: Null Controls Hold
E1 (pattern absence) and E2 (single observation) produce slot_count=0.

### H4: Template Induction Correct
For C2, the induced template is `https://api.example.com/users/${url}` (not `https://api.example.com/users/user-${url}`).

## 5. Data and Conditions

### 5.1 Training Data (Identical to Parent)

All 10 conditions use the same synthetic deterministic data as EXP-PRODUCT-34195008089:

| Condition | Training | Unseen | Expected Slot Count |
|---|---|---|---|
| B1 | 3 get-item obs (items A,B,C) | 5 unseen (D-H) | 1 [url] |
| B2 | 3 create-user obs (users A,B,C) | 5 unseen (D-H) | 2 [url, name] |
| B3 | 3 create-post obs (posts A,B,C) | 5 unseen (D-H) | 3 [url, title, X-Request-ID] |
| B4 | 3 set-webhook obs (callbacks a,b,c) | 3 unseen (d-f) | 1 [callback_url] |
| B5 | 3 update-item obs (static user_id=A) | 3 unseen (D-F) | 1 [url] |
| C1 | = B4 training | 3 unseen (d-f) | 1 [callback_url] |
| C2 | 3 get-user obs (user-1/2/3) | 3 unseen (user-4/5/6) | 1 [url] |
| D1 | 3 create-order obs (noisy) | 3 unseen | 3 [url, customer, X-Request-ID] |
| D2 | 3 search obs (noisy GET) | 3 unseen | 1 [url] |
| D3 | 3 place-order obs (static quantity) | 1 unseen | 1 [url] |

### 5.2 Null Controls

| Control | Training | Expected Slot Count |
|---|---|---|
| E1 | 3 unrelated obs (payment, user, session) | 0 |
| E2 | 1 single obs (get-item A) | 0 |

### 5.3 Literal Baseline

Literal mechanism (no parameter slots) from `kernel.distill()` must fail on all unseen combinations (fail_rate=1.0).

## 6. Implementation Plan

### 6.1 Code Changes

Modify `src/spider/kernel.py`:

1. **Add `_compute_slot_prefix()` helper**: Given a list of varying values at a path, compute the longest common prefix. Check if it's a slot-level prefix (ends with boundary char or is followed by identifier pattern). Return the prefix to strip and the stripped template.

2. **Modify `distill_parameterized()`**: After computing common prefix/suffix, call `_compute_slot_prefix()` on the prefix. If a slot-level prefix is detected, strip it from the template and record it in the mechanism's metadata.

3. **No changes to `_bind()`**: The parent's `_bind()` prefix-strip code is inert and should be removed (it was added in the parent experiment but never worked). The new fix works at template construction time, not bind time.

### 6.2 Test Harness

Reuse `research/experiments/EXP-PRODUCT-34195008089/run_experiment.py` with:
- Updated experiment_id to EXP-PRODUCT-34282620394
- Same 10-condition structure
- Same training/unseen/expected data
- C2 uses full values (user-4, user-5, user-6) per spec

### 6.3 Execution

1. Write the fix in `src/spider/kernel.py`
2. Copy and adapt test harness from parent
3. Run all 10 conditions + null controls + literal baseline
4. Record raw evidence, derived metrics, and interpretation

## 7. Controls

### 7.1 Positive Control (C2)
- **Expected**: slot_count=1, binding_accuracy=1.0, bound URLs = `https://api.example.com/users/user-4` etc.
- **Pass condition**: All 3 unseen values produce correct URLs

### 7.2 Regression Controls (B1-B5, C1, D1-D3)
- **Expected**: Slot counts match parent results, binding_accuracy=1.0
- **Pass condition**: No change from parent (all 9 conditions pass)

### 7.3 Null Controls (E1, E2)
- **Expected**: slot_count=0
- **Pass condition**: No parameterization hallucinated

### 7.4 Template Induction Control (C2 diagnostics)
- **Expected**: Induced template prefix does NOT contain the slot-level prefix `user-`
- **Pass condition**: Template = `https://api.example.com/users/${url}` (not `https://api.example.com/users/user-${url}`)

## 8. Validity Threats

### 8.1 Over-Stripping Risk
The slot-level prefix detection might strip too aggressively (e.g., stripping `https://api.example.com/` from all templates). **Mitigation**: The fix only strips when the prefix is a proper prefix of ALL varying values AND ends with a boundary character. Structural URL components (scheme, host, path separators) are not boundary-matched.

### 8.2 Boundary Character Ambiguity
Some URLs may have meaningful `-` or `_` in structural positions. **Mitigation**: The fix only applies to the prefix of VARYING values at a specific path, not to the entire template. Structural components are shared across all observations and thus part of the common prefix, not the slot-level prefix.

### 8.3 C1 Interaction
C1 uses prefix+suffix templates (`https://site-${callback_url}.com/hook`). The fix must not strip the suffix or interfere with suffix-based templates. **Mitigation**: The fix only modifies prefix stripping; suffix logic is unchanged.

### 8.4 D2 Query Parameter Limitation
D2 expected slot_count=1 [url] per architectural limitation (leaf-path cannot split query params). The fix must not change this behavior. **Mitigation**: D2's varying values are full URLs with query params; the slot-level prefix detection applies to the path component only.

## 9. Decision Rules

### 9.1 C2-FIX-SURVIVES
If ALL of:
1. C2 binding_accuracy == 1.0 (3/3 correct)
2. All 9 regression conditions pass (slot_count match AND binding_accuracy=1.0)
3. E1 slot_count == 0
4. E2 slot_count == 0
5. No crashes or unexpected None returns
6. C2 induced template does NOT contain `user-` as slot-level prefix

### 9.2 C2-FIX-FALSIFIED
If ANY of:
1. C2 binding_accuracy < 1.0
2. Any regression condition fails
3. Null control fails (slot_count > 0)

### 9.3 MEASUREMENT_INVALID
If:
1. distill_parameterized() crashes
2. Test harness errors prevent execution
3. Import failures or missing dependencies

## 10. Analysis Plan

1. Run test harness with fix applied
2. Record raw evidence (all condition results, diagnostics)
3. Compute derived metrics (binding accuracy, slot counts, template prefixes)
4. Compare against frozen expected values
5. Apply decision rules
6. Record observations, validity notes, and unresolved questions

## 11. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 12. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
