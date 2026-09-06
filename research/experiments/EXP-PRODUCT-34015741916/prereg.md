# EXP-PRODUCT-34015741916 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34015741916
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-06
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-PRODUCT-34003641840 (FIXES-FALSIFIED per audit ceiling)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Do the field-path relevance noise filter, two-part structure-similarity check, and double-prefix detection — validated in isolation in EXP-PRODUCT-34003641840 — transfer correctly when ported into src/spider/kernel.py?

## 3. Motivation

### What the parent experiment established (EXP-PRODUCT-34003641840)

The parent experiment validated two algorithmic concepts in an isolated implementation (run_experiment.py):

**Established (carried forward):**
- Field-path relevance noise filter correctly excludes metadata from D1 (timestamp, request_duration_ms, retry_count, user_agent excluded; slot count 4->3) and D2 (response_time_ms, cache_hit, result_count excluded; slot count 2->1)
- Structure-similarity two-part check (Jaccard>=0.75 + constant-value anchor) prevents E1 hallucination: unrelated observations have Jaccard=0.667 (below 0.75) AND constant-anchor fails
- B1/B4 clean-synthetic regression preserved: slot_count=1, binding_correct=1.0
- C1 full-value URL binding passes: slot_count=1, 3/3 EXECUTABLE
- E2 single-observation null control passes: slot_count=0
- B2/B3 improvements: body.name (B2 slot 1->2) and body.title (B3 slot 2->3) correctly parameterized
- Base distill_parameterized algorithm remains sound for path-only and URL-value parameterization

**Rejected (carried forward):**
- Noise-filter heuristic len(common_prefix)>0 OR len(common_suffix)>0 — provably insufficient
- Structure-similarity Jaccard threshold 0.3 — too low
- Producer's broad claim FIXES-SURVIVE-REGRESSION — NOT SUPPORTED per audit ceiling (audit status=REVISE producer_claim_supported=false)

**Unknown (carried forward — these are the questions this experiment answers):**
- Whether field-path relevance + structure-similarity survive kernel integration into src/spider/kernel.py
- Whether B5/D3 pass with correct prereg training data
- Whether C2 double-prefix can be fixed for suffix-empty templates
- Whether D2 query-string parameterization requires architectural change
- Whether nested metadata (body.timestamp) leaks through top-level-only allowlist

**Do Not Assume (carried forward):**
- Do not assume this result transfers to kernel-integrated code
- Do not assume B5/D3 results are valid regression anchors (prereg was violated in parent)
- Do not assume C2 double-prefix is fixed (dead code in parent)
- Do not assume D2 slot_count=1 means D2 passes (post-hoc redefinition in parent)
- Do not assume nested metadata inside body/headers is excluded
- Do not assume real browser observations match synthetic patterns

### Why this experiment is different

The parent experiment validated the algorithm in a self-contained run_experiment.py that never modified kernel.py. The audit explicitly identified KERNEL_INTEGRATION_GAP as a blocking issue: the entire implementation is isolated and never touches the production code path.

This experiment ports the validated components into the actual kernel:
1. Adds distill_parameterized() to SpiderKernel in kernel.py
2. Wires double-prefix detection into _bind()
3. Uses the same field-path relevance and structure-similarity logic
4. Runs all 10 conditions through the kernel's data model (Observation, Mechanism, Resolution)
5. Restores correct prereg training data (B5: static A,A,A; D3: static 1,1,1)

The question is NOT whether the algorithm works (it does, in isolation). The question is whether it works when integrated into the kernel's code path, data model, and method interfaces.

## 4. Hypotheses

### H1: Kernel Integration Preserves Base Algorithm
B1 slot_count=1 and B4 slot_count=1, with all binding_correct=true under strict content verification, when distill_parameterized runs inside kernel.py. The port does not break clean-synthetic parameterized induction.

### H2: Noise Filter Transfers to Kernel
D1 slot_count=3 (customer, url, x_request_id) with metadata excluded. D2 slot_count=1 (url) with metadata excluded. The field-path relevance filter works identically in the kernel's Observation data model.

### H3: Structure-Similarity Transfers to Kernel
E1 slot_count=0 for unrelated observations. The two-part check (Jaccard>=0.75 + constant-value anchor) works identically in the kernel.

### H4: Double-Prefix Bug Fixed in Kernel
C2 slot_count=1 with all 3 binding_correct=true using true unseen full values (user-4, user-5, user-6). No double-prefix (user-user-4) occurs. Double-prefix detection is wired into the kernel's _bind() path.

### H5: Prereg Training Data Restored
B5 slot_count=1 with static A,A,A training (user_id is constant, correctly excluded). D3 slot_count=1 with static quantity 1,1,1 training (quantity is constant, correctly excluded). These match the preregistered expectations from EXP-PRODUCT-33993747223.

### H6: No Regression
All conditions that passed in EXP-PRODUCT-34003641840 pass identically in the kernel. No condition regresses.

## 5. Test Conditions

All conditions use identical observation data as EXP-PRODUCT-34003641840 (raw_evidence.json). The only change is that distill_parameterized runs inside kernel.py instead of run_experiment.py.

### 5.1 Regression Conditions (B1-B5)

**B1 (single-path url parameter):**
- Training: GET /api/items/{A,B,C} (3 observations)
- Expected: slot_count=1 [url], all 5 unseen bindings correct

**B2 (path and body):**
- Training: POST /api/users/{D,E,F} with body.name={Alice,Bob,Charlie} (3 observations)
- Expected: slot_count=2 [url, name], all 5 unseen bindings correct

**B3 (path, body, headers):**
- Training: POST /api/posts/{D,E,F} with body.title={First,Second,Third} and X-Request-ID=req-{4,5,6} (3 observations)
- Expected: slot_count=3 [url, title, x_request_id], all 5 unseen bindings correct

**B4 (non-identifier URL values):**
- Training: POST /api/webhooks with body.callback_url=https://site-{d,e,f}.com/hook (3 observations)
- Expected: slot_count=1 [callback_url], all 3 unseen bindings correct

**B5 (shared slot name — CORRECT PREREG DATA):**
- Training: PUT /api/items/{D,E,F} with body.user_id={A,A,A} (3 observations, ALL SAME VALUE)
- Expected: slot_count=1 [url] — user_id is static (same value A), correctly excluded
- Note: Parent used varying A,B,C (slot_count=2). This experiment uses correct prereg: static A,A,A.

### 5.2 Full-Value Conditions (C1-C2)

**C1 (full-value URL binding):**
- Training: POST /api/webhooks with body.callback_url=https://site-{d,e,f}.com/hook (3 observations)
- Expected: slot_count=1 [callback_url], all 3 bindings correct

**C2 (full-value IDs with double-prefix fix):**
- Training: GET /api/users/user-{4,5,6} (3 observations)
- Expected: slot_count=1 [url], all 3 bindings correct — true unseen values are user-4, user-5, user-6
- Double-prefix detection: template is user-${url}, unseen param is user-4, detection strips prefix to get url=4

### 5.3 Noisy Observation Conditions (D1-D3)

**D1 (noisy POST with metadata):**
- Training: POST /api/orders/order-{4,5,6} with body.customer=cust-{D,E,F}, headers.X-Request-ID=req-10{4,5,6}, plus metadata: timestamp, request_duration_ms, retry_count, user_agent (3 observations)
- Expected: slot_count=3 [customer, url, x_request_id] — metadata excluded

**D2 (noisy GET with query string — HONEST LIMITATION):**
- Training: GET /api/search?q={delta,epsilon,zeta}&page={4,5,6} with metadata: response_time_ms, cache_hit, result_count (3 observations)
- Expected: slot_count=1 [url] — metadata excluded, but leaf-path model cannot extract query parameters
- This documents the architectural limitation honestly, not redefined post-hoc

**D3 (varying preconditions — CORRECT PREREG DATA):**
- Training: POST /api/orders/item-{4,5,6} with body.quantity={1,1,1} and varying session_id/auth_token (3 observations, ALL SAME QUANTITY)
- Expected: slot_count=1 [url] — quantity is static (1,1,1), correctly excluded
- Note: Parent used varying 1,2,3 (slot_count=2). This experiment uses correct prereg: static 1,1,1.

### 5.4 Null Control Conditions (E1-E2)

**E1 (pattern-absence / unrelated observations):**
- Training: POST /api/payments, GET /api/users/42, DELETE /api/sessions/abc-123 (3 unrelated observations)
- Expected: slot_count=0 — no common parameterizable structure

**E2 (single observation null control):**
- Training: 1 observation only
- Expected: slot_count=0 — function requires >=2 observations

## 6. Kernel Integration Design

### 6.1 New Method: distill_parameterized()

Added to SpiderKernel class in kernel.py:
- Input: list[Observation] (multiple observations of the same intent)
- Output: Mechanism with parameter_slots populated
- Logic:
  1. Collect leaf paths from all observations' action dicts
  2. Apply field-path relevance filter (allowlist: method, url, body, headers, query)
  3. For each filtered path, collect values across observations
  4. If path has varying values across observations → candidate parameter slot
  5. Apply structure-similarity check: Jaccard(leaf_path_sets) >= 0.75 AND constant-value anchor
  6. If check fails → return None (observations are unrelated)
  7. Build action_template with ${slot} substitution for varying paths
  8. Build Mechanism with parameter_slots list

### 6.2 Modified: _bind() with Double-Prefix Detection

Extended to handle suffix-empty templates:
- When template has prefix but no suffix (e.g., user-${url})
- If param starts with prefix: strip prefix, use remainder as parameter value
- If param does NOT start with prefix: proceed with normal substitution

### 6.3 Data Model Compatibility

The ported code must work with kernel.py's existing data models:
- Observation: intent, state, action, next_state, success, provenance
- Mechanism: mechanism_id, intent, preconditions, action_template, postconditions, parameter_slots, ...
- Resolution: status, mechanism_id, reason, bound_action, confidence

No model changes required — parameter_slots already exists on Mechanism.

## 7. Binding Correctness Verification

### 7.1 Strict Content Check

For each unseen test case:
1. Resolve the mechanism with test params via kernel.resolve()
2. Compare bound_action content recursively against expected_action
3. binding_correct = (resolution.status == EXECUTABLE) AND (bound_action == expected_action)

### 7.2 Double-Prefix Verification

For C2 specifically:
- Template: user-${url}
- Unseen param: user-4 (full value)
- Expected bound_action url field: user-4 (the full value, not user-user-4)
- Double-prefix detection must strip the user- prefix from user-4 to get url=4, then substitute to get user-${url} → user-4

## 8. Measures

### 8.1 Primary Metrics
- **slot_count** per condition: number of parameter slots induced by kernel.distill_parameterized()
- **binding_correct_count** per condition: number of unseen test cases with correct bound_action (strict)
- **binding_accuracy** per condition: binding_correct_count / unseen_count

### 8.2 Secondary Metrics
- **parameter_slots** per condition: list of slot names induced
- **metadata_excluded** for D1/D2: boolean — are metadata fields excluded?
- **double_prefix_detected** for C2: boolean — was the double-prefix correctly handled?
- **prereg_compliant** for B5/D3: boolean — does slot_count match correct prereg expectation?

### 8.3 Control Metrics
- **B1/B4_regression_pass**: boolean — slot_count and binding unchanged
- **E2_null_pass**: boolean — slot_count=0
- **C1/C2_pass**: boolean — full-value binding correct
- **D1/D2_noise_filtered**: boolean — metadata excluded
- **E1_hallucination_prevented**: boolean — slot_count=0

## 9. Decision Rules

### 9.1 KERNEL-INTEGRATION-SURVIVES
If ALL of:
1. B1 slot_count=1 AND all 5 binding_correct=true
2. B4 slot_count=1 AND all 3 binding_correct=true
3. D1 slot_count=3 AND slots ⊆ {customer, url, x_request_id}
4. E1 slot_count=0
5. C1 slot_count=1 AND all 3 binding_correct=true
6. C2 slot_count=1 AND all 3 binding_correct=true (no double-prefix)
7. E2 slot_count=0
8. B5 slot_count=1 with static A,A,A training (prereg correct)
9. D3 slot_count=1 with static 1,1,1 training (prereg correct)
10. No condition regresses vs EXP-PRODUCT-34003641840

### 9.2 KERNEL-INTEGRATION-FALSIFIED
If ANY of conditions (1)-(10) fail.

### 9.3 MEASUREMENT_INVALID
If kernel cannot execute in test mode, or binding_correct verification cannot be performed.

## 10. Validity Threats

### 10.1 Kernel Data Model Mismatch
The ported code assumes Observation.action is a dict with leaf paths matching the synthetic test data structure. If the kernel's Observation model handles action dicts differently (e.g., different key traversal, different None handling), results may differ from the isolated implementation. **Mitigation:** Test identical observation data; compare slot_count and binding_correct against parent results.

### 10.2 _bind() Interface Change
Extending _bind() with double-prefix detection changes a shared function. If other kernel code paths depend on _bind() behavior, this could introduce regressions. **Mitigation:** Double-prefix detection only triggers when template has prefix and no suffix — a narrow condition that does not affect normal ${slot} substitution.

### 10.3 Regex Pattern for Slot Names
The parent experiment fixed a regex bug: [A-Za-z0-9_]* → [A-Za-z0-9_-]* to match hyphenated slot names (X-Request-ID). The kernel's existing _PARAMETER regex must also support hyphens. **Mitigation:** Verify kernel regex matches [A-Za-z0-9_-] before running conditions.

### 10.4 D2 Query-String Limitation
The leaf-path model treats URL as a single leaf node. D2 will produce slot_count=1 [url] rather than slot_count=2 [q, page]. This is a known architectural limitation, not a noise-filter failure. **Mitigation:** D2 documents the limitation honestly (slot_count=1, not redefined to pass).

### 10.5 Synthetic-to-Real Gap
All test conditions use synthetic observations. Real browser observations may have different noise patterns, nested structures, or None values. **Mitigation:** This is a kernel integration test, not a real-browser test. Real-browser testing is a later gate.

## 11. Expected Outcomes

### 11.1 All Conditions Pass (KERNEL-INTEGRATION-SURVIVES)
- Algorithmic gains transfer from isolated POC to production kernel
- C-PARAM-INHERIT advances to kernel-validated level
- Product can expose distill_parameterized() as a kernel capability
- Next gate: real-browser observation testing
- Product consequence: parameterized induction becomes a credible product capability

### 11.2 Kernel Integration Breaks (KERNEL-INTEGRATION-FALSIFIED)
- The ported code does not work correctly in the kernel's code path
- Diagnosis: which condition fails identifies the exact integration gap
- Possible causes: data model mismatch, _bind() interface change, regex incompatibility
- Product consequence: parameterized induction remains at isolated-POC level

### 11.3 Kernel Cannot Execute (MEASUREMENT_INVALID)
- The kernel cannot run distill_parameterized in test mode
- Not scientific evidence for or against
- Requires infrastructure fix before this question can be answered

## 12. Analysis Plan

1. **Port distill_parameterized()** from run_experiment.py into kernel.py SpiderKernel class
2. **Extend _bind()** with double-prefix detection for suffix-empty templates
3. **Fix _PARAMETER regex** to support hyphens: [A-Za-z0-9_-]
4. **Restore prereg training data**: B5 static A,A,A; D3 static 1,1,1
5. **Run all 10 conditions** through kernel.distill_parameterized()
6. **Record slot_count, parameter_slots, binding_correct for each condition**
7. **Compare with parent results** (EXP-PRODUCT-34003641840): direct before/after
8. **Apply decision rule**: KERNEL-INTEGRATION-SURVIVES / FALSIFIED / MEASUREMENT_INVALID
9. **Report all outcomes with equal prominence**

## 13. Analysis Code

Analysis will be implemented in Python using:
- Standard library only (no external dependencies)
- kernel.py's existing SpiderKernel class with new distill_parameterized method
- Same observation data as EXP-PRODUCT-34003641840 (raw_evidence.json)
- Recursive dict comparison for binding_correct verification
- Set operations for Jaccard similarity

Code will be committed to `research/experiments/EXP-PRODUCT-34015741916/` before execution.

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
