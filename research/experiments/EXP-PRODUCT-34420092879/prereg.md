# EXP-PRODUCT-34420092879 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34420092879
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Parent**: EXP-PRODUCT-34282620394 (C2-FIX-FALSIFIED, distill-time stripping rejected)
- **Date**: 2026-09-10
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can C2 be resolved without regressions by implementing bind-time slot-level prefix extraction in `_bind()`, such that all 10 conditions pass and the product API supports both short and full value calling conventions?

## 3. Motivation

### 3.1 Prior Art and Failure Modes

**EXP-PRODUCT-34015741916 (grandparent)**: KERNEL-INTEGRATION-PARTIAL 9/10. Ported `distill_parameterized()` into kernel.py. B1-B5 regression holds (21/21), D1-D3 noise filtering holds, E1/E2 null controls hold. C2 fails: double-prefix bug (`user-user-4` instead of `user-4`). `_detect_double_prefix` is dead code.

**EXP-PRODUCT-34195008089 (parent)**: C2-FIX-FALSIFIED. Tried `_bind()` prefix-strip approach (`val.startswith(template_prefix)`). FALSIFIED because template prefix is full path (e.g., `https://api.example.com/users/user-`), not short prefix. Value `user-4` doesn't start with full path prefix.

**EXP-PRODUCT-34282620394 (parent)**: C2-FIX-FALSIFIED. Tried distill-time prefix stripping. Works for C2 in isolation (binding_accuracy=1.0). But introduces 4 regressions (B4, C1, D1, D3) because it mandates full-value-only calling convention. Root cause: distill-time stripping changes VALUE CONTRACT. When template is `prefix-${slot}`, callers can pass short values. When template is `${slot}` (prefix stripped), callers MUST pass full values. Test harness uses mixed conventions.

### 3.2 Key Insight from Parent Handoff

The parent handoff identifies that the parent's bind-time approach handled BOTH conventions:
- Short value `d` into `site-${slot}` produced `site-d` (template adds prefix)
- Full value `user-4` triggered prefix stripping (avoid double-prefix)

This flexibility was lost with distill-time stripping because the template was modified at distill time, forcing callers to adapt.

### 3.3 Strategy (a): Bind-Time Slot-Level Prefix Extraction

The parent handoff recommends strategy (a) as lower-risk:
- **Template retains prefix**: no stripping at distill time. Template stays `https://site-${callback_url}.com/hook`, `https://api.example.com/users/user-${url}`, etc.
- **Slot prefix stored in metadata**: `slot_prefixes = {'callback_url': 'site-', 'url': 'user-'}`
- **Bind-time handling**: `_bind()` checks if value starts with stored prefix:
  - If yes: strip prefix from value, then substitute (avoids double-prefix)
  - If no: substitute directly (template adds prefix)

This handles both conventions:
- Short value `d`: doesn't start with `site-`, so substitute directly → `site-d` ✓
- Full value `site-d`: starts with `site-`, strip prefix → `d`, substitute → `site-d` ✓

### 3.4 Why This Approach

1. **Preserves VALUE CONTRACT**: callers can pass either short or full values without API change
2. **Simpler than hybrid**: no distill-time template modification, only bind-time prefix handling
3. **Lower-risk**: restores proven bind-time flexibility without complex two-phase logic
4. **Directly tests the key unknown**: "Whether bind-time detection with slot-level prefix extraction would handle both conventions"

## 4. Hypotheses

### H1: C2 Resolution
Bind-time slot-level prefix extraction resolves C2: `distill_parameterized()` induces template `https://api.example.com/users/user-${url}` with `slot_prefixes={'url': 'user-'}`. `_bind()` strips `user-` from full values (`user-4` → `4`) before substitution. All 3 unseen values (`user-4`, `user-5`, `user-6`) bind correctly (binding_accuracy=1.0).

### H2: No Regressions
All 9 regression conditions (B1-B5, C1, D1-D3) pass with correct slot counts and binding_accuracy=1.0. The bind-time approach does not break existing functionality.

### H3: Mixed Convention Support
The same mechanism handles both short values (`d`, `4`) and full values (`user-4`, `site-d`) without requiring callers to change their parameter passing style.

### H4: Null Controls
E1 (pattern absence) and E2 (single observation) produce slot_count=0. No hallucination.

## 5. Implementation Approach

### 5.1 Model Change
Add `slot_prefixes: dict[str, str] = field(default_factory=dict)` to `Mechanism` in `src/spider/models.py`. This stores the slot-level prefix for each parameter slot (e.g., `{'url': 'user-'}`).

### 5.2 distill_parameterized() in SpiderKernel
Port the induction logic from previous experiments into `src/spider/kernel.py`:
1. Extract varying fields by comparing action templates across observations
2. For each varying field, compute the slot-level prefix from training values
3. Create template by replacing varying parts with `${slot_name}` placeholders
4. Store `slot_prefixes` in mechanism metadata
5. Return mechanism with `confidence=0.9` (matching prior experiments)

### 5.3 _bind() Modification
Modify `_bind()` to accept optional `prefixes: dict[str, str] | None = None` parameter:
1. For each slot substitution, check if `prefixes` contains a prefix for this slot
2. If prefix exists and value starts with prefix: strip prefix from value, then substitute
3. If prefix exists but value doesn't start with prefix: substitute directly (template adds prefix)
4. If no prefix: substitute directly (existing behavior)

### 5.4 resolve() Update
Update `resolve()` to pass `best.slot_prefixes` to `_bind()`:
```python
bound_action=_bind(best.action_template, params, prefixes=best.slot_prefixes),
```

### 5.5 Helper Functions
Port the following helper functions from previous experiment scripts:
- `_collect_leaf_paths(action)` — enumerate leaf paths in action dict
- `_is_metadata_path(path, metadata_keys)` — check if path is metadata
- `_get_value_at_path(action, path)` — extract value at dotted path
- `_compute_jaccard(set1, set2)` — Jaccard similarity
- `_check_constant_value_anchor(path_values)` — check if path has constant anchor
- `_find_common_prefix_suffix(values)` — compute common prefix/suffix
- `_extract_parameter_candidates(action, template_paths)` — identify varying fields
- `_compute_structure_similarity(observations)` — pairwise Jaccard
- `_set_template_value(template, path, value)` — set value at dotted path
- `_field_path_to_slot_name(path)` — convert dotted path to slot name

### 5.6 Test Harness
Reuse the identical 10-condition test harness from parent EXP-PRODUCT-34282620394:
- B1: single-path (url varies)
- B2: path-and-body (url + name vary)
- B3: path-body-headers (url + title + X-Request-ID vary)
- B4: non-identifier-values (callback_url varies, short values 'd','e','f')
- B5: shared-slot-name (url varies, user_id static)
- C1: prefix+Suffix URL binding (same as B4, short values)
- C2: full-value IDs (user-4, user-5, user-6)
- D1: noisy POST with metadata
- D2: noisy GET with metadata
- D3: varying preconditions
- E1: pattern absence (null control)
- E2: single observation (null control)

## 6. Data

### 6.1 Training Data
Identical to parent EXP-PRODUCT-34282620394. Each condition uses 3 training observations with deterministic synthetic data.

### 6.2 Unseen Test Data
Identical to parent. B4/C1/D1/D3 use SHORT values ('d', '4'). C2 uses FULL values ('user-4'). This mixed convention is the core test.

### 6.3 Expected Outputs
Identical to parent. Strict JSON comparison: bound_action must exactly match expected_action.

## 7. Measures

### 7.1 Primary Metric
- **binding_accuracy**: fraction of unseen test cases where bound_action exactly matches expected_action
- **slot_count**: number of parameter slots induced by distill_parameterized()

### 7.2 Per-Condition Metrics
- binding_accuracy per condition (B1-B5, C1-C2, D1-D3)
- slot_count per condition
- resolution_status (EXECUTABLE, EXPLORE, UNKNOWN)

### 7.3 Aggregate Metrics
- overall_binding_accuracy: across all 10 conditions
- regression_pass_count: number of conditions passing
- regression_fail_count: number of conditions failing

### 7.4 Diagnostic Metrics
- slot_prefixes_detected: prefix extracted for each slot
- template_induced: the parameterized template produced
- prefix_strip_count: number of values where prefix was stripped at bind time

## 8. Controls

### 8.1 Positive Control: C2
- Training: user-1, user-2, user-3
- Unseen: user-4, user-5, user-6 (FULL values)
- Expected: binding_accuracy=1.0, no double-prefix
- Verifies: prefix extraction and bind-time stripping work correctly

### 8.2 Regression Baseline: B1-B5
- B1: slot_count=1, binding_accuracy=1.0
- B2: slot_count=2, binding_accuracy=1.0
- B3: slot_count=3, binding_accuracy=1.0
- B4: slot_count=1, binding_accuracy=1.0 (SHORT values 'd','e','f')
- B5: slot_count=1, binding_accuracy=1.0
- Verifies: existing functionality not broken

### 8.3 Mixed Convention Test: B4 vs C2
- B4: short values 'd','e','f' → should bind correctly via template prefix
- C2: full values 'user-4','user-5','user-6' → should bind correctly via prefix stripping
- Verifies: both calling conventions work with same mechanism

### 8.4 Null Controls: E1, E2
- E1: unrelated observations → slot_count=0
- E2: single observation → slot_count=0
- Verifies: no hallucination of parameterization

### 8.5 Literal Baseline: B_LITERAL
- Literal mechanisms (no parameterization) → fail_rate=1.0 on unseen
- Verifies: parameterized induction is necessary

## 9. Statistical Tests

Not applicable. This is a deterministic synthetic experiment with exact matching. No statistical inference required. All conditions must pass exactly (binding_accuracy=1.0, slot_count=expected).

## 10. Validity Threats

### 10.1 Synthetic-to-Real Gap
All conditions use deterministic synthetic data. Findings do not directly demonstrate real-browser behavior. Mitigation: this is a kernel correctness test, not a product economics test. Real-browser testing is a separate gate.

### 10.2 Prefix Extraction Robustness
The slot-level prefix extraction depends on the training values having a consistent prefix. Edge cases (e.g., values with no common prefix, values with multiple candidate prefixes) are not tested. Mitigation: E1 null control tests pattern absence; future experiments should test more diverse prefix patterns.

### 10.3 Template Derivation Accuracy
The template derivation logic must correctly identify varying vs constant fields. Incorrect derivation could produce wrong templates. Mitigation: B1-B5 regression baseline verifies template derivation on known inputs.

### 10.4 Bind-Time Prefix Matching
The prefix matching logic (`value.startswith(prefix)`) could false-match on values that coincidentally start with the prefix. Mitigation: test harness uses distinct prefixes ('user-', 'site-', 'order-', 'item-') that don't appear as prefixes of unrelated values.

### 10.5 No Model/Network/Browser
Pure offline computation. No external validity for real-world deployment. Mitigation: this is a necessary-but-not-sufficient gate. Product economics measurement is a separate experiment.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. C2 binding_accuracy == 1.0 (all 3 unseen values bind correctly)
2. B1-B5 all pass (slot_count match AND binding_accuracy=1.0)
3. C1 passes (slot_count=1, binding_accuracy=1.0)
4. D1-D3 all pass (slot_count match AND binding_accuracy=1.0)
5. E1 slot_count == 0
6. E2 slot_count == 0
7. No crashes or errors in distill_parameterized or _bind

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. C2 binding_accuracy < 1.0
2. Any regression in B1-B5, C1, D1-D3
3. E1 or E2 slot_count > 0
4. Crashes or errors

### 11.3 MEASUREMENT_INVALID
If:
1. Infrastructure failure prevents execution
2. distill_parameterized crashes for unexpected reasons
3. Test harness cannot be loaded

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- C2 resolved without regressions
- C-PARAM-INHERIT advances: parameterized mechanisms handle mixed conventions
- Kernel integration advances from PARTIAL to near-complete
- Unblocks end-to-end product economics measurement (C-PRODUCT-ECON)
- Product API can support both short and full value calling conventions

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Bind-time slot-level prefix extraction fails to resolve C2 or introduces regressions
- Identify specific failure mode (which condition fails, how it fails)
- Narrow remaining options: hybrid distill+bind, or contract change to full-value-only
- Kernel integration remains PARTIAL

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Infrastructure failure, not scientific evidence
- Debug and retry

## 13. Analysis Plan

1. **Implement**: Add `slot_prefixes` to Mechanism model, implement `distill_parameterized()` with prefix detection, modify `_bind()` with prefix handling, port helper functions from parent test harness
2. **Run**: Execute all 10 conditions + E1/E2 null controls + B_LITERAL baseline
3. **Verify**: Check binding_accuracy and slot_count for each condition
4. **Diagnose**: If any condition fails, inspect slot_prefixes_detected, template_induced, and prefix_strip_count
5. **Report**: All outcomes with equal prominence

## 14. Analysis Code

Implementation will be in `src/spider/kernel.py` (distill_parameterized, _bind modifications) and `src/spider/models.py` (slot_prefixes field). Test harness in `research/experiments/EXP-PRODUCT-34420092879/run_experiment.py`.

## 15. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 16. Freeze Statement

This preregistration is frozen BEFORE any implementation code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
