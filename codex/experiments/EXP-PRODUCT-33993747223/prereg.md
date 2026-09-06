# EXP-PRODUCT-33993747223 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-33993747223
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-05
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can three algorithmic fixes — double-prefix detection, noise-field filtering, and structure-similarity check — be applied to distill_parameterized() in src/spider/kernel.py without breaking regression on clean synthetic inputs, and do the fixes resolve the three failure modes that blocked realistic-input use?

## 3. Motivation

The parent experiment (EXP-PRODUCT-33974562602) established:
- **Kernel integration is faithful**: distill_parameterized() on SpiderKernel produces identical slot counts, distinct naming, and 100% EXECUTABLE/correct binding as the experiment-script version on clean synthetic inputs (21/21 across B1-B5).
- **Three algorithmic failure modes block all realistic-input use**:
  1. **Double-prefix error** (C1/C2): When caller supplies full values containing the learned prefix/suffix (e.g., `https://site-d.com/hook`), `_bind()` substitutes the full value into `${slot}`, producing `https://site-https://site-d.com/hook.com/hook`. Binding accuracy = 0.0.
  2. **Noise-field over-parametrization** (D1/D2): `_extract_varying_values_multi()` treats every varying field as a slot. Noise fields (timestamps, durations, cache flags) induce spurious parameter slots, causing 0% resolution on D1/D2.
  3. **Pattern-absence hallucination** (E1): Unrelated observations (POST /api/payments, GET /api/users/42, DELETE /api/sessions/abc-123) produce 4 hallucinated slots instead of 0.

The parent verdict was KERNEL-INTEGRATION-FALSIFIED: the integration is faithful but the algorithm has bugs. The code was reverted to the base state (132-line kernel.py without distill_parameterized). This experiment re-integrates the function AND applies the three targeted fixes.

The parent handoff recommends: "Fix the three algorithmic failure modes in src/spider/kernel.py: (1) in _bind, detect when supplied param already contains prefix/suffix and skip re-wrapping; (2) in _extract_varying_values_multi, add noise-filter heuristic; (3) add structure-similarity check to return slot_count=0 when observations share no common pattern."

## 4. Hypotheses

### H1: Regression Preservation
The three fixes do not alter the behavior of distill_parameterized() on clean synthetic inputs. All 5 regression conditions (B1-B5) produce identical slot counts, distinct naming, and 100% unseen resolution/binding as EXP-PRODUCT-33974562602.

### H2: Double-Prefix Fix
After fixing `_bind()` to detect when a supplied param value already contains the template's prefix+suffix, full-value unseen parameters (C1: `https://site-d.com/hook`, C2: `user-4`) resolve EXECUTABLE with correct bound_action and binding_accuracy >= 0.9.

### H3: Noise-Field Filtering
After adding a noise-filter heuristic to `_extract_varying_values_multi()` that ignores fields without common prefix/suffix structure, noisy browser observations (D1: POST with extra fields, D2: GET with extra fields) produce slot_count matching expected signal-only fields and resolution >= 0.9.

### H4: Structure-Similarity Check
After adding a structure-similarity check (Jaccard over leaf paths), unrelated observations (E1) produce slot_count=0 and the resulting mechanism resolves to UNKNOWN.

## 5. Code Changes

### 5.1 Re-integration (Infrastructure)

Re-add to `src/spider/kernel.py` the functions from commit `521fdb2` (parent experiment execution base):
- `_deep_get(obj, path)` — navigate nested dicts by path tuple
- `_deep_set(obj, path, value)` — set nested values by path tuple
- `_collect_leaf_paths(obj, prefix)` — collect all leaf paths in nested structure
- `_common_prefix_and_suffix(values)` — extract common prefix/suffix across string values
- `_is_varying_field(field_values)` — check if a field genuinely varies
- `_field_path_to_slot_name(field_path, values)` — generate slot name from field path
- `_extract_varying_values_multi(observations)` — the varying-field detection and prefix/suffix extraction algorithm
- `SpiderKernel.distill_parameterized(observations, mechanism_id, intent)` — entry point

### 5.2 Fix A: Double-Prefix Detection in `_bind()`

**Bug**: `_bind()` uses `_PARAMETER.sub(replace, value)` which substitutes the full param value into `${slot}`. If the template is `https://site-${callback_url}.com/hook` and `callback_url` = `https://site-d.com/hook`, the result is `https://site-https://site-d.com/hook.com/hook`.

**Fix**: Before substituting, check if the param value already contains the surrounding prefix+suffix context. If the full-match value of the `${slot}` in the template would produce a string that already appears in the param value, return the param value directly instead of substituting.

**Alternative approach** (simpler): In `resolve()`, before calling `_bind()`, check if any param value already contains the template's slot prefix+suffix. If so, use the param value directly as the bound value for that slot, bypassing `_bind()` substitution.

**Pre-registered threshold**: The fix must detect the double-prefix by checking whether `prefix + param_value + suffix` equals `param_value` (i.e., the param value already includes the prefix and suffix). If true, use `param_value` directly. This is a deterministic check, not a heuristic.

### 5.3 Fix B: Noise-Field Filtering in `_extract_varying_values_multi()`

**Bug**: Every varying field across observations becomes a parameter slot. Noise fields (timestamps, durations, cache flags) vary but are not meaningful parameters.

**Fix**: After identifying varying fields, filter out fields whose values lack common prefix/suffix structure. Specifically:
- Compute `_common_prefix_and_suffix(str_values)` for each varying field
- If the common prefix is empty AND the common suffix is empty AND the values are not isomorphic (i.e., they don't share a structural pattern like `order-{N}`), the field is noise — ignore it
- A field is "structural" if it has a non-empty common prefix OR a non-empty common suffix across its values. This captures `https://site-{X}.com/hook` (has prefix and suffix) and `order-{N}` (has prefix) but not timestamps like `2026-09-01T10:00:00Z` vs `2026-09-01T10:01:00Z` (no common prefix/suffix beyond the date format, which is noise).

**Pre-registered criterion**: A field passes the noise filter if and only if `len(common_prefix) > 0 OR len(common_suffix) > 0`. Fields with empty prefix AND empty suffix are treated as noise. This is a deterministic heuristic, not a learned threshold.

### 5.4 Fix C: Structure-Similarity Check for Pattern Absence

**Bug**: Unrelated observations (POST /api/payments, GET /api/users/42, DELETE /api/sessions/abc-123) produce 4 hallucinated slots instead of 0.

**Fix**: Before creating slots, compute the structural similarity across observations. If observations share no common structural pattern, return slot_count=0 (no mechanism induced).

**Pre-registered metric**: Jaccard similarity over the set of leaf paths (as tuples) from each observation's action. Specifically:
- For each observation, collect `_collect_leaf_paths(obs.action)` → set of path tuples
- Compute pairwise Jaccard similarity: `|intersection| / |union|`
- If the mean pairwise Jaccard similarity < 0.3 (pre-registered threshold), observations are "unrelated" → return slot_count=0

**Rationale for threshold 0.3**: Observations with the same intent and action structure (e.g., all GET /api/items/{id}) share 100% of leaf paths (Jaccard = 1.0). Observations with different structures (POST body vs GET path vs DELETE path) share 0% of leaf paths (Jaccard = 0.0). A threshold of 0.3 is conservative: it requires at least some structural overlap before inducing slots.

### 5.5 Existing Code Preservation

The following functions/methods must NOT be altered by the fixes:
- `_matches()` — unchanged
- `_template_slots()` — unchanged
- `SpiderKernel.observe()` — unchanged
- `SpiderKernel.distill()` — unchanged
- `SpiderKernel.resolve()` — may be modified only for Fix A (double-prefix detection)
- `SpiderKernel.verify()` — unchanged
- `SpiderKernel.invalidate()` — unchanged

## 6. Test Conditions

### Phase A: Kernel Integration + Fix Verification

| Step | What | Expected |
|------|------|----------|
| A1 | Import kernel after modification | No ImportError |
| A2 | Run existing tests/test_kernel.py | All pass |
| A3 | Verify distill_parameterized is callable | Method exists on SpiderKernel |

### Phase B: Regression Baseline (5 conditions from EXP-PRODUCT-33741671686)

Identical to parent experiment B1-B5. Run through the FIXED kernel.distill_parameterized():

**B1: Single-path (C1 regression)**
- Training: GET https://api.example.com/items/{A,B,C}
- Unseen: {D,E,F,G,H}
- Expected: slot_count=1, unseen_resolution=1.0, binding_accuracy=1.0

**B2: Path+body (C2)**
- Training: POST https://api.example.com/users/{A,B,C} body={name: {Alice,Bob,Charlie}}
- Unseen: {(D,Diana),(E,Eve),(F,Frank),(G,Grace),(H,Heidi)}
- Expected: slot_count=2 distinct, unseen_resolution=1.0, binding_accuracy=1.0

**B3: Path+body+headers (C3)**
- Training: POST https://api.example.com/posts/{A,B,C} body={title: {First,Second,Third}} headers={X-Request-ID: {req-1,req-2,req-3}}
- Unseen: {(D,Fourth,req-4),(E,Fifth,req-5),(F,Sixth,req-6),(G,Seventh,req-7),(H,Eighth,req-8)}
- Expected: slot_count=3 distinct, unseen_resolution=1.0, binding_accuracy=1.0

**B4: Non-identifier URLs (C4)**
- Training: POST /webhooks body={callback_url: {https://site-a.com/hook, https://site-b.com/hook, https://site-c.com/hook}}
- Unseen: {https://site-d.com/hook, https://site-e.com/hook, https://site-f.com/hook}
- Expected: slot_count=1, unseen_resolution=1.0, binding_accuracy=1.0

**B5: Shared-slot collision (C5)**
- Training: PUT https://api.example.com/items/{A,B,C} body={user_id: {A,B,C}}
- Unseen: {(D,D),(E,E),(F,F)}
- Expected: slot_count=2 distinct, unseen_resolution=1.0, binding_accuracy=1.0

### Phase C: Full-Value Unseen Test (Double-Prefix Fix)

**C1: Full-value URLs**
- Training: same as B4 (https://site-{a,b,c}.com/hook)
- Unseen: caller supplies FULL URLs: https://site-d.com/hook, https://site-e.com/hook, https://site-f.com/hook
- Expected: double-prefix fix detects that supplied values already contain prefix "https://site-" and suffix ".com/hook", returns the full URL directly. slot_count=1, resolution=EXECUTABLE, bound_action = {"callback_url": "https://site-d.com/hook"} (not "https://site-https://site-d.com/hook.com/hook")

**C2: Full-value IDs with prefix**
- Training: GET https://api.example.com/users/{user-1,user-2,user-3}
- Unseen: caller supplies full IDs: user-4, user-5, user-6
- Expected: prefix="user-", slot_count=1, resolution=EXECUTABLE, bound_action contains full correct ID. Since "user-4" starts with prefix "user-" but does NOT end with an empty suffix, the double-prefix fix should pass through (param value "user-4" is the varying middle + prefix, template is `https://api.example.com/users/${url}` → binding produces correct URL).

### Phase D: Noisy Browser-Like Observations (Noise Filter Fix)

**D1: Noisy POST with path+body+headers**
- Training: 3 observations of POST https://api.example.com/orders/{order-1,order-2,order-3} with body={customer: {cust-A,cust-B,cust-C}} and headers={X-Request-ID: {req-101,req-102,req-103}} PLUS noise fields: timestamp, request_duration_ms, retry_count, user_agent
- Unseen: 3 combinations of (order-id, customer-name, request-id)
- Expected: noise filter ignores timestamp/request_duration_ms/retry_count/user_agent (no common prefix/suffix). slot_count=3 distinct (url, customer, X-Request-ID), unseen_resolution >= 0.9, binding_accuracy >= 0.9

**D2: Noisy GET with path+query**
- Training: 3 observations of GET https://api.example.com/search?q={alpha,beta,gamma}&page={1,2,3} with extra fields: response_time_ms, cache_hit, result_count
- Unseen: 3 combinations of (query-term, page-number)
- Expected: noise filter ignores response_time_ms/cache_hit/result_count. slot_count=2 distinct (q, page), unseen_resolution >= 0.9, binding_accuracy >= 0.9

**D3: Varying preconditions (observational only)**
- Training: 3 observations where each observation has different session_id and auth_token in state, and actions with varying path parameters
- Unseen: new session_id/auth_token + new path parameter
- Expected: slot_count >= 2 (url + body amount), resolution is observational (the precondition matching issue is orthogonal to the three fixes)
- NOTE: D3 is retained for completeness but NOT part of the primary decision rule. The precondition matching failure is a known separate issue.

### Phase E: Null Controls (Structure-Similarity Fix)

**E1: Unrelated action structures**
- Training: 3 observations with completely different action structures:
  1. POST /api/payments body={amount: 100, currency: "USD"}
  2. GET /api/users/42
  3. DELETE /api/sessions/abc-123
- Expected: Jaccard similarity over leaf paths < 0.3 (pre-registered threshold). Structure-similarity check returns slot_count=0. Mechanism resolves to UNKNOWN for any params.

**E2: Single observation (insufficient for induction)**
- Training: 1 observation only
- Expected: slot_count=0 (cannot induce from a single observation — no varying fields)

## 7. Measures

### 7.1 Primary Metrics

- **regression_pass**: boolean — all 5 regression conditions (B1-B5) produce identical slot counts and 100% unseen resolution/binding as EXP-PRODUCT-33974562602
- **double_prefix_fix_rate**: ratio — fraction of full-value unseen tests (C1+C2) that resolve EXECUTABLE with correct bound_action (no double-prefix error)
- **noise_filter_effectiveness**: ratio — fraction of noisy browser tests (D1+D2) that achieve slot_count matching expected signal-only count and resolution >= 0.9
- **pattern_absence_slot_count**: integer — number of parameter slots induced for null control E1 (must be 0)

### 7.2 Secondary Metrics

- **per_condition_slot_count**: integer per condition
- **per_condition_slot_names**: list of strings per condition
- **per_condition_unseen_resolution_rate**: ratio per condition
- **per_condition_binding_accuracy**: ratio per condition
- **jaccard_similarity_e1**: float — mean pairwise Jaccard similarity over leaf paths for E1 observations (must be < 0.3)
- **noise_filter_precision**: for D1/D2, fraction of ignored fields that are genuinely noise (should be 1.0)
- **noise_filter_recall**: for D1/D2, fraction of signal fields that are retained (should be 1.0)
- **total_test_combinations**: integer

### 7.3 Control Metrics

- **positive_control_regression**: all B1-B5 match EXP-PRODUCT-33974562602 results exactly
- **null_control_pattern_absence**: E1 produces slot_count=0
- **null_control_single_obs**: E2 produces slot_count=0
- **literal_baseline_fail**: literal mechanism fails on all unseen multi-param combinations

## 8. Null Models

### 8.1 Pattern Absence Null (E1)
Three unrelated observations with different HTTP methods, endpoints, and body structures. The structure-similarity check (Jaccard < 0.3) should detect that these share no common pattern and produce zero slots. This is a stronger null than the parent's (which passed via intent mismatch).

### 8.2 Single Observation Null (E2)
One observation only. With no second observation to compare, no field can be identified as "varying." The function should produce zero slots.

### 8.3 Noise Fields as Negative Controls
In D1 and D2, the noise fields (timestamp, duration, cache) are negative controls: they vary across observations but should be filtered out by the noise-filter heuristic. If they are NOT filtered, the slot count will be inflated (as in the parent experiment).

## 9. Statistical Tests

### 9.1 Primary: Exact Match Regression
For each of the 5 regression conditions (B1-B5):
- Slot count must equal the value from EXP-PRODUCT-33974562602
- Slot names must be distinct
- Unseen resolution rate must equal 1.0
- Binding accuracy must equal 1.0
- Test: exact equality (no tolerance — synthetic data, deterministic function)

### 9.2 Resolution Rate Threshold
For each new condition (C1-C2, D1-D2):
- unseen_resolution_rate >= 0.9
- binding_accuracy >= 0.9

### 9.3 Null Control
For E1:
- slot_count must equal 0 (exact)
- Jaccard similarity must be < 0.3
- Resolution must be UNKNOWN for all param combinations

For E2:
- slot_count must equal 0 (exact)

### 9.4 Noise Filter Precision/Recall
For D1:
- Signal fields (url, customer, X-Request-ID): must be retained (recall = 1.0)
- Noise fields (timestamp, request_duration_ms, retry_count, user_agent): must be ignored (precision = 1.0)

For D2:
- Signal fields (q, page in URL): must be retained
- Noise fields (response_time_ms, cache_hit, result_count): must be ignored

### 9.5 No Multiple Comparisons Correction
All tests are exact-match or threshold-based on deterministic synthetic data.

## 10. Controls

### 10.1 Positive Control: Regression to EXP-PRODUCT-33974562602
The 5 synthetic conditions (B1-B5) use identical inputs and must produce identical outputs. This is the strongest positive control: any deviation indicates a fix introduced regression.

### 10.2 Null Control: Pattern Absence (E1)
Three unrelated observations. The structure-similarity check should detect Jaccard < 0.3 and return slot_count=0. This addresses audit finding from EXP-PRODUCT-33741671686 and EXP-PRODUCT-33974562602.

### 10.3 Sensitivity Control: Single Observation (E2)
One observation only. Tests the minimum-data boundary.

### 10.4 Baseline: Literal Replay
kernel.distill() (existing literal mechanism) must fail on all unseen multi-parameter combinations.

### 10.5 Noise Field Negative Controls
In D1 and D2, noise fields serve as negative controls for the noise filter. If the filter works, these fields are ignored. If it doesn't, slot count is inflated (as in the parent).

## 11. Validity Threats

### 11.1 Fix Regression Risk
The three fixes modify the induction algorithm. Each fix could inadvertently alter behavior on clean synthetic inputs. Mitigation: regression baseline (B1-B5) uses identical inputs and must produce identical outputs. Any deviation is immediately detected.

### 11.2 Noise Filter False Positives
The noise filter heuristic (non-empty prefix OR suffix) could incorrectly filter out a genuine varying field that happens to have no common prefix/suffix. Mitigation: in D1/D2, the signal fields (url, customer, X-Request-ID, q, page) all have non-empty common prefix or suffix. The heuristic should retain them. If it doesn't, the filter is too aggressive and needs refinement.

### 11.3 Noise Filter False Negatives
The noise filter could fail to filter out noise fields that happen to share a prefix/suffix. Mitigation: the noise fields (timestamp, duration, cache) do not share meaningful prefix/suffix across observations. If the filter passes them through, the threshold needs tightening.

### 11.4 Structure-Similarity Threshold
The Jaccard threshold of 0.3 is pre-registered. If it's too high, unrelated observations with slight structural overlap could induce slots. If too low, related observations with minor structural differences could be rejected. Mitigation: 0.3 is conservative — it requires at least 30% path overlap before inducing slots.

### 11.5 Double-Prefix Fix Scope
The double-prefix fix detects when `prefix + param_value + suffix == param_value`. This handles the case where the caller supplies the full URL. But it may not handle edge cases where the param value partially overlaps with the prefix/suffix. Mitigation: the test conditions C1/C2 cover the documented failure modes. Edge cases are tracked as unknowns.

### 11.6 No Real-Agent Cost Measurement
This experiment does not measure end-to-end cost for a real LLM agent. Mitigation: that measurement requires real-browser infrastructure and is the next gate after these fixes are validated.

## 12. Decision Rules

### 12.1 FIXES-SURVIVE-REGRESSION
If ALL of:
1. Kernel integration completes without crashes; existing tests pass
2. Regression baseline: all 5 conditions (B1-B5) produce identical slot counts, distinct naming, and 21/21 EXECUTABLE + 21/21 binding correct
3. Full-value unseen: C1+C2 resolve with EXECUTABLE and binding_accuracy >= 0.9
4. Noisy browser: D1+D2 achieve slot_count matching expected signal-only count and resolution >= 0.9
5. Null control: E1 produces slot_count=0 and E2 produces slot_count=0
6. No crashes or non-deterministic output

### 12.2 FIXES-FALSIFIED
If ANY of:
1. Any regression condition (B1-B5) produces different slot count or <100% resolution/binding
2. Full-value unseen (C1 or C2) binding_accuracy < 0.9
3. Noisy observation (D1 or D2) slot_count != expected signal-only count or resolution < 0.9
4. Null control E1 produces slot_count > 0
5. Any crash or non-deterministic output

### 12.3 MEASUREMENT_INVALID
If:
1. Kernel integration cannot complete (import errors, type incompatibilities)
2. The three fixes cannot be implemented without circular dependencies
3. Test infrastructure failures prevent execution

## 13. Expected Outcomes

### 13.1 FIXES-SURVIVE-REGRESSION
- C-PARAM-INHERIT advances: the function now handles realistic inputs
- The three algorithmic failure modes are resolved
- Product can proceed to real-browser testing and confidence calibration
- The claim ceiling advances from "kernel-shipped, clean-synthetic only" to "kernel-shipped with realistic-synthetic robustness"
- Next gate: real-browser noisy observations, confidence calibration, end-to-end agent cost

### 13.2 FIXES-FALSIFIED
- Identify which fix failed:
  - If regression breaks: one of the fixes inadvertently altered clean-synthetic behavior
  - If double-prefix persists: the detection logic is insufficient (need API contract change)
  - If noise filter fails: the prefix/suffix heuristic is insufficient (need richer features)
  - If pattern-absence still hallucinates: Jaccard threshold is wrong or leaf paths are insufficient
- Smallest next action: fix the identified failure mode before attempting further generalization

### 13.3 MEASUREMENT_INVALID
- Infrastructure issue prevents the experiment from running
- Not scientific evidence for or against C-PARAM-INHERIT
- Debug the integration issue and retry

## 14. Analysis Plan

1. **Phase A: Kernel Integration + Fixes**
   - Re-add distill_parameterized() and helpers to kernel.py from commit 521fdb2
   - Apply Fix A: modify _bind() or resolve() for double-prefix detection
   - Apply Fix B: modify _extract_varying_values_multi() for noise filtering
   - Apply Fix C: add structure-similarity check before slot creation
   - Verify import, run existing tests
   - Record kernel.py sha256 before and after

2. **Phase B: Regression Baseline**
   - Create fresh MechanismRegistry per condition
   - Call kernel.distill_parameterized() with training observations
   - Record slot_count, slot_names, template
   - Call kernel.resolve() with each unseen param combination
   - Record resolution status, bound_action
   - Compare to EXP-PRODUCT-33974562602 results (exact match)

3. **Phase C: Full-Value Unseen**
   - Use same training data as B4
   - Call distill_parameterized() — record induction result
   - Call resolve() with full URLs (https://site-d.com/hook, not 'd')
   - Record resolution status, bound_action
   - Verify no double-prefix in bound_action

4. **Phase D: Noisy Browser**
   - Generate noisy observations with extra fields
   - Call distill_parameterized() — verify noise fields are ignored
   - Record which fields were filtered vs retained
   - Call resolve() with each unseen combination
   - Record resolution status, bound_action

5. **Phase E: Null Control**
   - Call distill_parameterized() with unrelated observations
   - Compute Jaccard similarity over leaf paths
   - Verify slot_count=0 (Jaccard < 0.3)
   - Call resolve() with various params — verify UNKNOWN

6. **Aggregation**
   - Compute all primary and secondary metrics
   - Apply decision rule
   - Write result.json, report.md, provenance.json

## 15. Pre-registered Expectations

From prior work:
- The function works on identical synthetic inputs (EXP-PRODUCT-33974562602: 21/21 EXECUTABLE, 21/21 binding)
- The three fixes are targeted at documented failure modes with clear root causes
- Double-prefix fix: the detection is deterministic (prefix + param + suffix == param → use param directly)
- Noise filter: prefix/suffix heuristic is sufficient because signal fields have structural patterns and noise fields don't
- Structure-similarity: Jaccard < 0.3 is conservative for unrelated observations (Jaccard = 0.0) and permissive for related observations (Jaccard = 1.0)
- Regression risk is low because the fixes are orthogonal to the clean-synthetic path (clean synthetic has no double-prefix, no noise fields, and Jaccard = 1.0)

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

If the three fixes require design changes (e.g., the noise filter needs a different threshold, or the structure-similarity metric needs a different similarity measure), the deviation will be documented in the result.json validity_notes and the regression baseline will verify functional equivalence despite design changes.

## 17. Freeze Statement

This preregistration is frozen BEFORE any code modification or test execution. The experiment will be executed exactly as described here.
