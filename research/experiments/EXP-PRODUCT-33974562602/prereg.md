# EXP-PRODUCT-33974562602 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-33974562602
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-05
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the multi-parameter induction function survive kernel integration (shipping into src/spider/kernel.py) and still produce correct distinct slot naming, and does it also work when training observations come from noisy multi-step browser sessions with varying preconditions?

## 3. Motivation

The parent experiment (EXP-PRODUCT-33741671686) validated multi-parameter induction at synthetic POC level:
- 21/21 unseen combinations resolved EXECUTABLE with correct bound_action
- All 5 conditions (C1-C5) passed: single-path, path+body, path+body+headers, non-identifier, shared-slot collision
- Audit PASS with all recomputed metrics matching producer

However, the audit identified 8 required_fixes and a narrow claim ceiling:
1. **The induction function lives only in run_experiment.py** — not in src/spider/kernel.py (sha256 46929b3a unchanged)
2. Null control passes via intent mismatch, not pattern absence detection
3. Full-value unseen tests (caller supplies complete URLs) not performed
4. Confidence threshold is tautological (0.8 == min_confidence 0.8)
5. Fragile positional slot-to-param mapping in harness

The parent handoff recommends: "ship distill_parameterized_v2 / _extract_varying_values_multi into src/spider/kernel.py with unit tests, fix null_control, add full-value unseen tests, calibrate confidence."

This experiment addresses fixes #1, #2, and #3 — the three most critical blockers for advancing C-PARAM-INHERIT beyond experiment-script-only POC.

## 4. Hypotheses

### H1: Kernel Integration Faithfulness
The kernel-integrated distill_parameterized() produces identical slot counts, distinct slot naming, and 100% unseen resolution/binding as the experiment-script version on identical synthetic inputs.

### H2: Full-Value Unseen Resolution
The kernel-integrated function correctly handles full-value unseen parameters (caller supplies `https://site-d.com/hook` and `req-4`, not pre-stripped middles `d` and `4`), extracting prefix/suffix correctly from complete values.

### H3: Noisy Browser Compatibility
The kernel-integrated function produces correct distinct slot naming and resolves EXECUTABLE for training observations that contain realistic noise: extra fields (timestamps, request_ids, metadata), varying preconditions, and multi-step action structures.

### H4: Pattern Absence Detection (Null Control)
When training observations share no common prefix/suffix pattern and no shared structural positions for varying fields, the function produces zero parameter slots (slot_count=0), not hallucinated parameters.

## 5. Kernel Integration Plan

### 5.1 Functions to Port

From `research/experiments/EXP-PRODUCT-33741671686/run_experiment.py` into `src/spider/kernel.py`:

**Core induction engine:**
- `_extract_varying_values_multi(observations: list[Observation]) -> dict` — the varying-field detection and prefix/suffix extraction algorithm

**Entry point:**
- `distill_parameterized(observations: list[Observation], mechanism_id: str = "param-multi", intent: str | None = None) -> Mechanism | None` — multi-observation distillation that creates a Mechanism with parameterized template

**Supporting helpers (private functions in kernel.py):**
- `_deep_get(obj, path) -> Any` — navigate nested dicts by path tuple
- `_deep_set(obj, path, value)` — set nested values by path tuple
- `_collect_leaf_paths(obj, prefix) -> list[tuple]` — collect all leaf paths in nested structure
- `_common_prefix_and_suffix(values: list[str]) -> tuple[str, str, list[str]]` — extract common prefix/suffix across string values
- `_is_varying_field(field_values: list[Any]) -> bool` — check if a field genuinely varies
- `_field_path_to_slot_name(field_path: tuple, values: list[str]) -> str` — generate slot name from field path

### 5.2 Integration Target

The functions become methods or module-level helpers in `src/spider/kernel.py`:
- `SpiderKernel.distill_parameterized()` — public method, delegates to the induction engine
- Private helper functions prefixed with `_` in kernel.py module scope
- No changes to existing `_bind()`, `_template_slots()`, `resolve()`, or `Mechanism` model — they already support parameterized mechanisms

### 5.3 Verification

After integration:
- Run existing `tests/test_kernel.py` — must pass (no regressions)
- Run `python -c "from spider.kernel import SpiderKernel; print('import ok')"` — must succeed
- Compute sha256 of modified kernel.py for provenance

## 6. Test Conditions

### Phase A: Kernel Integration Verification

| Step | What | Expected |
|------|------|----------|
| A1 | Import kernel after modification | No ImportError |
| A2 | Run existing tests/test_kernel.py | 3/3 pass |
| A3 | Verify distill_parameterized is callable | Method exists on SpiderKernel |

### Phase B: Regression Baseline (5 conditions from EXP-PRODUCT-33741671686)

Run the identical 5 synthetic conditions through `kernel.distill_parameterized()`:

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
- Expected: slot_count=2 distinct (no collision), unseen_resolution=1.0, binding_accuracy=1.0

### Phase C: Full-Value Unseen Test

**C1: Full-value URLs**
- Training: same as B4 (https://site-{a,b,c}.com/hook)
- Unseen: caller supplies FULL URLs: https://site-d.com/hook, https://site-e.com/hook, https://site-f.com/hook
- Expected: prefix extraction handles complete values correctly (prefix="https://site-", suffix=".com/hook"), slot_count=1, resolution=EXECUTABLE, bound_action contains full correct URL
- This specifically tests whether the function handles non-circular prefix extraction when the caller supplies full values, not pre-stripped middles

**C2: Full-value IDs with prefix**
- Training: GET https://api.example.com/users/{user-1,user-2,user-3}
- Unseen: caller supplies full IDs: user-4, user-5, user-6
- Expected: prefix="user-", slot_count=1, resolution=EXECUTABLE, bound_action contains full correct ID

### Phase D: Noisy Browser-Like Observations

**D1: Noisy POST with path+body+headers**
- Training: 5 observations of POST https://api.example.com/orders/{order-1,order-2,order-3,order-4,order-5} with body={customer: {cust-A,cust-B,cust-C,cust-D,cust-E}} and headers={X-Request-ID: {req-101,...,req-105}} PLUS extra noise fields: timestamp, request_duration_ms, retry_count, user_agent
- Unseen: 5 combinations of (order-id, customer-name, request-id)
- Expected: slot_count=3 distinct (order, customer, request_id), noise fields ignored, unseen_resolution=1.0, binding_accuracy=1.0

**D2: Noisy GET with path+query**
- Training: 5 observations of GET https://api.example.com/search?q={alpha,beta,gamma,delta,epsilon}&page={1,2,3,4,5} with extra fields: response_time_ms, cache_hit, result_count
- Unseen: 5 combinations of (query-term, page-number)
- Expected: slot_count=2 distinct (q, page), noise fields ignored, unseen_resolution=1.0, binding_accuracy=1.0

**D3: Multi-step observation with varying preconditions**
- Training: 3 observations where each observation has a state with different session_id and auth_token, and actions with varying path parameters. The preconditions vary across observations but the action structure is consistent.
- Unseen: new session_id/auth_token + new path parameter
- Expected: slot_count>=1, preconditions taken from last observation (not averaged), resolution=EXECUTABLE with correct bound_action

### Phase E: Null Control (Pattern Absence)

**E1: Unrelated action structures**
- Training: 3 observations with completely different action structures:
  1. POST /api/payments body={amount: 100, currency: "USD"}
  2. GET /api/users/42
  3. DELETE /api/sessions/abc-123
- These share no common prefix/suffix in varying positions, no shared structural fields
- Expected: slot_count=0, mechanism resolves to UNKNOWN for any params
- This tests pattern-ABSENCE detection (not just intent mismatch)

**E2: Single observation (insufficient for induction)**
- Training: 1 observation only
- Expected: slot_count=0 (cannot induce from a single observation — no varying fields)

## 7. Measures

### 7.1 Primary Metrics

- **kernel_regression_pass**: boolean — all 5 regression conditions (B1-B5) produce identical slot counts and 100% unseen resolution/binding as EXP-PRODUCT-33741671686
- **full_value_resolution_rate**: ratio — fraction of full-value unseen tests (C1+C2) that resolve EXECUTABLE with correct bound_action
- **noisy_resolution_rate**: ratio — fraction of noisy browser tests (D1+D2+D3) that resolve EXECUTABLE with correct bound_action
- **null_control_slot_count**: integer — number of parameter slots induced for null control E1 (must be 0)

### 7.2 Secondary Metrics

- **per_condition_slot_count**: integer per condition — number of parameter slots induced
- **per_condition_slot_names**: list of strings per condition — actual slot names (check distinctness)
- **per_condition_unseen_resolution_rate**: ratio per condition — fraction of unseen combinations resolving EXECUTABLE
- **per_condition_binding_accuracy**: ratio per condition — fraction of resolved combinations with correct bound_action
- **kernel_integration_time**: seconds — time to complete kernel modification + verification
- **total_test_combinations**: integer — total unseen test combinations across all conditions

### 7.3 Control Metrics

- **positive_control_regression**: all B1-B5 match EXP-PRODUCT-33741671686 results exactly
- **null_control_pattern_absence**: E1 produces slot_count=0 (pattern absence, not intent mismatch)
- **null_control_single_obs**: E2 produces slot_count=0 (insufficient data)

## 8. Null Models

### 8.1 Pattern Absence Null (E1)
Three unrelated observations with different HTTP methods, endpoints, and body structures. The induction function should find no common prefix/suffix pattern and produce zero slots. This is a stronger null than the parent experiment's null control (which passed via intent mismatch).

### 8.2 Single Observation Null (E2)
One observation only. With no second observation to compare, no field can be identified as "varying." The function should produce zero slots. This tests the minimum-data boundary.

### 8.3 Shuffle Null (implicit)
If slot naming were random, binding_accuracy would be ~0 (since random slot names don't map to the correct params). The B_RANDOM_INDUCTION baseline from the parent experiment showed this: random naming resolves EXECUTABLE but binding_accuracy=0.0. We reuse this insight: correct slot naming is measured by binding_accuracy, not just resolution rate.

## 9. Statistical Tests

### 9.1 Primary: Exact Match Regression
For each of the 5 regression conditions (B1-B5):
- Slot count must equal the value from EXP-PRODUCT-33741671686
- Slot names must be distinct (no collisions)
- Unseen resolution rate must equal 1.0 (21/21 total)
- Binding accuracy must equal 1.0 (21/21 total)
- Test: exact equality (no tolerance — synthetic data, deterministic function)

### 9.2 Resolution Rate Threshold
For each new condition (C1-C2, D1-D3):
- unseen_resolution_rate >= 0.9 (allowing 1 failure per condition with 5 unseen tests)
- binding_accuracy >= 0.9

### 9.3 Null Control
For E1 and E2:
- slot_count must equal 0 (exact, not threshold)
- Resolution must be UNKNOWN for all param combinations

### 9.4 No Multiple Comparisons Correction Needed
All tests are exact-match or threshold-based on deterministic synthetic data. No inferential statistics are required. The "p-value" is 0 or 1: either the function produces the correct output or it doesn't.

## 10. Controls

### 10.1 Positive Control: Regression to EXP-PRODUCT-33741671686
The 5 synthetic conditions (B1-B5) use identical inputs and must produce identical outputs. This is the strongest possible positive control: the function already works on these inputs (in run_experiment.py). Any deviation indicates an integration bug.

### 10.2 Null Control: Pattern Absence (E1)
Three unrelated observations. The parent experiment's null control passed via intent mismatch (hallucinated slots with wrong intent). This experiment's null control is stronger: it tests that the function produces ZERO slots when no pattern exists. This addresses audit finding #2 from EXP-PRODUCT-33741671686.

### 10.3 Sensitivity Control: Single Observation (E2)
One observation only. Tests the minimum-data boundary: the function should not induce any parameters from a single observation (no varying fields to detect).

### 10.4 Baseline: Literal Replay
kernel.distill() (existing literal mechanism) must fail on all unseen multi-parameter combinations. This confirms parameterization is still necessary after integration.

## 11. Validity Threats

### 11.1 Integration Fidelity
Moving code from run_experiment.py to kernel.py could introduce subtle bugs (import paths, type hints, missing helpers). Mitigation: regression baseline (B1-B5) uses identical inputs and must produce identical outputs. Any deviation is immediately detected.

### 11.2 Noisy Observation Design
Noisy observations are synthetic (not real browser data). The noise is realistic (extra fields, varying preconditions) but controlled. Mitigation: this is a stepping stone — if the function fails on designed noise, it will fail on real noise. If it passes, real-browser testing is the next gate.

### 11.3 Full-Value Unseen Circularity
The prefix extraction could be circular if the training data already contains full values. Mitigation: training data uses different values than test data (site-a/b/c vs site-d/e/f), so the function must generalize the prefix pattern, not memorize specific values.

### 11.4 Null Control Strength
The null control (E1) uses 3 observations with different structures. A stronger null would use more observations or more dissimilar structures. Mitigation: 3 observations is the minimum for the induction function (it needs at least 2 to compare). Using 3 with maximally different structures is sufficient.

### 11.5 No Real-Agent Cost Measurement
This experiment does not measure end-to-end cost for a real LLM agent (tokens, browser work, latency). Mitigation: that measurement requires real-browser infrastructure and is the next gate after kernel integration is validated.

## 12. Decision Rules

### 12.1 KERNEL-INTEGRATION-SURVIVES
If ALL of:
1. Kernel integration completes without crashes; existing tests pass
2. Regression baseline: all 5 conditions (B1-B5) produce identical slot counts, distinct naming, and 21/21 EXECUTABLE + 21/21 binding correct
3. Full-value unseen: C1+C2 resolve all 5 unseen combinations with EXECUTABLE and correct bound_action
4. Noisy browser: D1+D2+D3 resolve all 15 unseen combinations with EXECUTABLE and correct bound_action (>=0.9 per condition)
5. Null control: E1+E2 produce slot_count=0 and UNKNOWN resolution
6. No crashes or non-deterministic output

### 12.2 KERNEL-INTEGRATION-FALSIFIED
If ANY of:
1. Any regression condition (B1-B5) produces different slot count or <100% resolution/binding
2. Full-value unseen (C1 or C2) resolution rate <0.9
3. Noisy observation (D1, D2, or D3) resolution rate <0.9
4. Null control E1 produces slot_count > 0
5. Any crash or non-deterministic output

### 12.3 MEASUREMENT_INVALID
If:
1. Kernel integration cannot complete (import errors, type incompatibilities, missing dependencies)
2. The function is not implementable in kernel.py (e.g., requires runtime imports that create circular dependencies)
3. Test infrastructure failures prevent execution

## 13. Expected Outcomes

### 13.1 KERNEL-INTEGRATION-SURVIVES
- C-PIM advances: kernel can now create parameterized mechanisms via distill_parameterized()
- Addresses 3 of 8 audit required_fixes from EXP-PRODUCT-33741671686
- Product can register multi-parameter mechanisms for production use
- Next gate: confidence calibration, real-agent cost measurement, real-browser noisy observations
- The claim ceiling advances from "experiment-script-only synthetic POC" to "kernel-shipped with synthetic validation"

### 13.2 KERNEL-INTEGRATION-FALSIFIED
- C-PARAM-INHERIT remains stuck at experiment-script-only POC
- Identify the exact failure mode:
  - If regression fails: integration bug (type mismatch, import error, helper incompatibility)
  - If full-value fails: prefix extraction is circular (only works with pre-stripped middles)
  - If noisy fails: function is not robust to realistic input variation
  - If null control fails: function hallucinates parameters (still not detecting pattern absence)
- Smallest next action: fix the identified failure mode before attempting further generalization

### 13.3 MEASUREMENT_INVALID
- Infrastructure issue prevents the experiment from running
- Not scientific evidence for or against C-PARAM-INHERIT
- Debug the integration issue and retry

## 14. Analysis Plan

1. **Phase A: Kernel Integration**
   - Port functions from run_experiment.py to kernel.py
   - Verify import, run existing tests
   - Record kernel.py sha256 before and after

2. **Phase B: Regression Baseline**
   - Create fresh MechanismRegistry per condition
   - Call kernel.distill_parameterized() with training observations
   - Record slot_count, slot_names, template
   - Call kernel.resolve() with each unseen param combination
   - Record resolution status, bound_action
   - Compare to EXP-PRODUCT-33741671686 results (exact match)

3. **Phase C: Full-Value Unseen**
   - Use same training data as B4 (non-identifier URLs)
   - Call distill_parameterized() — record induction result
   - Call resolve() with full URLs (https://site-d.com/hook, not 'd')
   - Record resolution status, bound_action
   - Verify prefix extraction is non-circular

4. **Phase D: Noisy Browser**
   - Generate noisy observations with extra fields and varying preconditions
   - Call distill_parameterized() — verify noise fields are ignored
   - Call resolve() with each unseen combination
   - Record resolution status, bound_action

5. **Phase E: Null Control**
   - Call distill_parameterized() with unrelated observations
   - Verify slot_count=0
   - Call resolve() with various params — verify UNKNOWN

6. **Aggregation**
   - Compute all primary and secondary metrics
   - Apply decision rule
   - Write result.json, report.md, provenance.json

## 15. Pre-registered Expectations

From prior work:
- The induction function works on identical synthetic inputs (EXP-PRODUCT-33741671686: 21/21 EXECUTABLE, 21/21 binding)
- Kernel integration should preserve this behavior exactly (deterministic function, same inputs)
- Full-value unseen tests are expected to succeed IF prefix extraction is non-circular (the function extracts common prefix/suffix from training data and applies it to unseen values — if training data uses site-a/b/c with prefix "https://site-" and suffix ".com/hook", unseen site-d should work)
- Noisy observations are expected to succeed IF the noise fields don't share structural positions with the varying fields (extra timestamp/metadata fields are at different paths than the order/customer/request_id fields)
- Null control is expected to produce zero slots IF the function correctly detects that unrelated observations share no common pattern

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

If the kernel integration requires design changes (e.g., the function signature must differ from run_experiment.py), the deviation will be documented in the result.json validity_notes and the regression baseline will verify functional equivalence despite signature changes.

## 17. Freeze Statement

This preregistration is frozen BEFORE any kernel modification or test execution. The experiment will be executed exactly as described here.
