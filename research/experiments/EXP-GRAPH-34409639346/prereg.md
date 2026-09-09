# EXP-GRAPH-34409639346 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34409639346
- **Lane**: Graph
- **Claim**: C-SEMANTIC-RESOLVE (Goals can be resolved to applicable mechanisms without internal ids)
- **Date**: 2026-09-09
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the kernel resolve a URL template with semantic aliasing (e.g., /users/{userId} vs /accounts/{id} pointing to the same REST resource) to the correct parametrized mechanism when both are registered with equal confidence, and does it correctly select the mechanism whose template matches the intent structure?

## 3. Motivation

The graph lane has been BLOCKED on C-PARAM-INHERIT for four consecutive experiments due to an unfixed sort key in kernel.py L112. The Director pivoted to C-SEMANTIC-RESOLVE as a materially orthogonal question within the graph lane charter (priority_claims includes C-SEMANTIC-RESOLVE).

The kernel's `resolve()` function (kernel.py L93-123) filters candidates by:
1. Exact intent string match (`m.intent != intent`)
2. Preconditions match (`_matches(m.preconditions, context)`)
3. Applicability guards match (`_matches(m.applicability_guards, context)`)
4. Required parameter slots available in params

Then sorts by confidence descending and returns the first candidate.

When two mechanisms share the same intent string and confidence, the kernel has no template-matching or intent-structure-matching logic. It returns whichever candidate sorts first by mechanism_id. This experiment tests whether this is the case, and whether preconditions can serve as a disambiguation signal.

## 4. Hypotheses

### H1: Core Falsification (Arbitrary Selection)
When two mechanisms have identical intent strings, confidence, preconditions, and applicability_guards, but different URL templates (e.g., /users/{userId} vs /accounts/{id}), the kernel selects whichever mechanism sorts first by mechanism_id. Selection is NOT based on template structure or intent structure.

### H2: Preconditions Disambiguation
When two mechanisms have identical intent strings and confidence but different preconditions (e.g., resource_type="user" vs resource_type="account"), the kernel correctly filters to the mechanism whose preconditions match the context. Preconditions serve as a viable semantic resolution signal.

### H3: Intent Exact Match
When two mechanisms have different intent strings, the kernel correctly selects the mechanism whose intent matches the query intent. Exact intent matching works correctly.

### H4: Baseline Integrity
All baseline conditions (B-COLD, B-SINGLE-USER, B-SINGLE-USER-EXECUTE, B-INTENT-DIFFERENT) pass as specified.

## 5. Mechanism Definitions

### 5.1 Mechanism Alpha (user-retrieval)
```
mechanism_id: "mechanism-alpha"
intent: "get-user"
preconditions: {} (empty, or resource_type="user" in PRECONDITIONS-DISAMBIGUATE)
action_template: {"method": "GET", "url": "/users/${userId}"}
postconditions: {"resource_type": "user"}
parameter_slots: ["userId"]
confidence: 0.95
```

### 5.2 Mechanism Beta (account-retrieval)
```
mechanism_id: "mechanism-beta"
intent: "get-user"  (SAME as alpha — semantic aliasing)
preconditions: {} (empty, or resource_type="account" in PRECONDITIONS-DISAMBIGUATE)
action_template: {"method": "GET", "url": "/accounts/${id}"}
postconditions: {"resource_type": "account"}
parameter_slots: ["id"]
confidence: 0.95  (SAME as alpha — equal confidence)
```

### 5.3 Sort Order
mechanism-alpha < mechanism-beta alphabetically. When both are candidates, the kernel returns mechanism-alpha (first in sorted order).

## 6. Conditions

### 6.1 B-COLD (Baseline: Empty Registry)
- Registry: empty
- Intent: "get-user"
- Context: {resource_type: "user", id: 7}
- Params: {userId: 7, id: 7}
- Expected: UNKNOWN (no applicable mechanism)
- Purpose: Verifies kernel does not fabricate mechanisms

### 6.2 B-SINGLE-USER (Baseline: Single Mechanism)
- Registry: mechanism-alpha only
- Intent: "get-user"
- Context: {resource_type: "user", id: 7}
- Params: {userId: 7, id: 7}
- Expected: EXECUTABLE, mechanism_id="mechanism-alpha", bound_action={"method": "GET", "url": "/users/7"}
- Purpose: Verifies basic template binding works

### 6.3 B-SINGLE-USER-EXECUTE (Baseline: HTTP Execution)
- Same as B-SINGLE-USER
- Additional: HTTP GET to jsonplaceholder.typicode.com/users/7
- Expected: HTTP 200, response contains id=7
- Purpose: Verifies HTTP execution against live endpoint

### 6.4 B-INTENT-DIFFERENT (Baseline: Different Intent Strings)
- Registry: mechanism-alpha (intent="get-user") and mechanism-gamma (intent="get-account", same template as alpha)
- Intent: "get-user"
- Context: {resource_type: "user", id: 7}
- Params: {userId: 7, id: 7}
- Expected: EXECUTABLE, mechanism_id="mechanism-alpha" (exact intent match filters out gamma)
- Purpose: Verifies exact intent matching works correctly

### 6.5 CORE-DUAL-TEMPLATE (Core Test: Semantic Aliasing)
- Registry: mechanism-beta registered FIRST, then mechanism-alpha (via sequential upsert; final sorted order: alpha, beta)
- Both mechanisms: intent="get-user", confidence=0.95, preconditions={}, applicability_guards={}
- Intent: "get-user"
- Context: {resource_type: "user", id: 7}
- Params: {userId: 7, id: 7}
- Expected: EXECUTABLE, mechanism_id="mechanism-alpha" (sort order, NOT template matching)
- Purpose: Tests whether selection is based on template structure or arbitrary sort order
- Note: Both mechanisms have all parameter slots satisfied (userId and id both provided). The kernel cannot distinguish them by preconditions, applicability_guards, or parameter availability. Selection depends solely on sort order.

### 6.6 PRECONDITIONS-DISAMBIGUATE (Test: Preconditions as Semantic Signal)
- Registry: mechanism-beta registered FIRST, then mechanism-alpha
- mechanism-alpha: preconditions={"resource_type": "user"}
- mechanism-beta: preconditions={"resource_type": "account"}
- Intent: "get-user"
- Context: {resource_type: "user", id: 7}
- Params: {userId: 7, id: 7}
- Expected: EXECUTABLE, mechanism_id="mechanism-alpha" (preconditions filter out beta)
- Purpose: Tests whether preconditions can disambiguate semantically aliased templates

### 6.7 NULL-ARBITRARY (Null Control: Identical Mechanisms)
- Registry: mechanism-delta (mechanism_id="mechanism-delta") and mechanism-epsilon (mechanism_id="mechanism-epsilon")
- Both: identical intent, confidence, preconditions, applicability_guards, parameter_slots
- Intent: "get-user"
- Context: {resource_type: "user", id: 7}
- Params: {userId: 7, id: 7}
- Expected: EXECUTABLE, mechanism_id="mechanism-delta" (sort order: delta < epsilon)
- Purpose: Confirms arbitrary selection when mechanisms are identical except for ID

### 6.8 CORE-DUAL-TEMPLATE-RUN2 (Reproducibility Check)
- Identical to CORE-DUAL-TEMPLATE
- Purpose: Verify selection is deterministic across runs

## 7. Controls

### 7.1 Positive Control (B-SINGLE-USER)
- Single mechanism resolves correctly with template binding
- Verifies: basic kernel functionality works

### 7.2 Null Control (B-COLD)
- Empty registry returns UNKNOWN
- Verifies: kernel does not fabricate mechanisms

### 7.3 Null Control (NULL-ARBITRARY)
- Two identical mechanisms, selection by sort order
- Verifies: kernel has no hidden disambiguation logic

### 7.4 Intent Match Control (B-INTENT-DIFFERENT)
- Different intent strings correctly filter candidates
- Verifies: exact intent matching works

### 7.5 Reproducibility Control (CORE-DUAL-TEMPLATE-RUN2)
- Same result across two independent runs
- Verifies: selection is deterministic

## 8. Decision Rules

### 8.1 SURVIVES_CURRENT_TEST
If ALL of:
1. B-COLD returns UNKNOWN
2. B-SINGLE-USER returns EXECUTABLE with correct bound_action
3. B-SINGLE-USER-EXECUTE returns HTTP 200 with correct id
4. B-INTENT-DIFFERENT resolves to mechanism-alpha
5. CORE-DUAL-TEMPLATE selection is deterministic (same result in RUN1 and RUN2)
6. PRECONDITIONS-DISAMBIGUATE resolves to mechanism-alpha (preconditions filter out beta)
7. NULL-ARBITRARY resolves to mechanism-delta (sort order)
8. No exceptions or crashes
9. No monkey-patching

### 8.2 FALSIFIED-IN-SETTING
If ANY of:
1. CORE-DUAL-TEMPLATE selection depends on registration order (not mechanism_id sort order) — demonstrates instability
2. PRECONDITIONS-DISAMBIGUATE fails to filter by preconditions (both mechanisms remain candidates)
3. Any baseline regresses (B-COLD returns non-UNKNOWN, B-SINGLE-USER fails, B-SINGLE-USER-EXECUTE fails HTTP, B-INTENT-DIFFERENT resolves to wrong mechanism)
4. The kernel selects the mechanism whose template does NOT match the context parameters when preconditions could disambiguate

### 8.3 MEASUREMENT_INVALID
If:
1. HTTP failures prevent execution for conditions that reach EXECUTABLE status
2. Exceptions or crashes prevent measurement
3. Infrastructure issues prevent kernel instantiation

## 9. Validity Threats

### 9.1 Kernel Code Limitation
The kernel's resolve() function (kernel.py L93-123) has no template-matching or intent-structure-matching logic. A negative result (arbitrary selection in CORE-DUAL-TEMPLATE) is expected from code inspection. However, this is still valuable: it definitively characterizes the kernel's limitation and identifies the extension point (preconditions or new matching logic).

### 9.2 Parameter Name Bias
The templates use different parameter names (userId vs id). If the kernel were to match templates against context keys, this could introduce bias. However, the current kernel does not perform template-context matching, so this is not a confound.

### 9.3 HTTP Endpoint Limitations
jsonplaceholder.typicode.com is a simple REST API with no DOM, auth, session state, or drift. Results apply only to this endpoint type. Production OAuth/OIDC, CDN, load-balancer, or rate-limit environments may behave differently.

### 9.4 Registration Order Confound
In CORE-DUAL-TEMPLATE, mechanism-beta is registered before mechanism-alpha (via sequential upsert). The final sorted order is alpha, beta (alpha sorts first). If the kernel's selection depends on registration order rather than sorted order, this would be a different failure mode. The experiment controls for this by documenting the registration order and verifying the sorted order.

### 9.5 Single-Intent Scope
The experiment tests a single intent ("get-user") with a single endpoint pattern (/users/{id} or /accounts/{id}). Generalization to multiple intents, complex URL patterns, or nested resources is not tested.

### 9.6 Synthetic Mechanisms
The mechanisms are hand-authored, not distilled from observations. Real mechanisms produced by distill() may have different characteristics (e.g., different preconditions, evidence, confidence). The experiment tests the kernel's resolution logic, not the distillation pipeline.

## 10. Analysis Plan

1. **Kernel Inspection**: Before execution, verify kernel.py L112 sort key (should be `m.confidence` only, per unfixed HEAD).
2. **Registry Setup**: For each condition, create a fresh kernel with explicitly controlled registry contents.
3. **Resolution**: Call resolve() with specified intent, context, and params.
4. **HTTP Execution**: For EXECUTABLE results, execute bound_action against jsonplaceholder.typicode.com.
5. **Verification**: Check resolution status, mechanism_id, bound_action, and HTTP response.
6. **Reproducibility**: Run CORE-DUAL-TEMPLATE twice to verify deterministic selection.
7. **Reporting**: Report all outcomes with equal prominence.

## 11. Expected Outcomes

### 11.1 SURVIVES_CURRENT_TEST (Preconditions Disambiguate)
- PRECONDITIONS-DISAMBIGUATE resolves to mechanism-alpha (preconditions filter out beta)
- CORE-DUAL-TEMPLATE resolves to mechanism-alpha (sort order, both candidates)
- All baselines pass
- Interpretation: Preconditions-based filtering is a viable mechanism for semantic resolution. The product can encode intent structure in preconditions to guide template selection. C-SEMANTIC-RESOLVE can advance without kernel modification.

### 11.2 FALSIFIED-IN-SETTING (Arbitrary Selection or Preconditions Fail)
- CORE-DUAL-TEMPLATE resolves to mechanism-alpha (sort order) — expected, but if PRECONDITIONS-DISAMBIGUATE also fails, the kernel lacks any semantic resolution capability
- If PRECONDITIONS-DISAMBIGUATE fails: The kernel cannot use preconditions to disambiguate. C-SEMANTIC-RESOLVE requires kernel modification (e.g., template-structure matching, intent-classification, or precondition-based filtering enhancement).
- If CORE-DUAL-TEMPLATE selection depends on registration order: The kernel's selection is unstable, not just arbitrary. This is a stronger negative result.

### 11.3 MEASUREMENT_INVALID
- HTTP failures, exceptions, or infrastructure issues prevent measurement
- Not scientific evidence for or against

## 12. Analysis Code

Analysis will be implemented in Python using:
- `spider.kernel.SpiderKernel` for kernel instantiation and resolution
- `spider.registry.MechanismRegistry` for registry management
- `spider.models.Mechanism` for mechanism construction
- `urllib.request` for HTTP execution against jsonplaceholder.typicode.com
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-GRAPH-34409639346/` before execution.

## 13. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 14. Parent Handoff Carry-Forward

This experiment inherits from EXP-GRAPH-34395286092 (BLOCKED_CLOSE_AND_PIVOT on C-PARAM-INHERIT). The following distinctions are preserved:

### Established
- Parameter-slot-count hazard is real and reproducible on unfixed HEAD (kernel sha256 46929b3a)
- Param mechanism generalizes to unseen identifiers
- Literal mechanism does not generalize
- All 6 baselines pass on unfixed HEAD
- Confidence ordering works correctly
- HTTP execution against jsonplaceholder.typicode.com works (13/13 HTTP 200)
- Fix is NOT present in committed HEAD

### Rejected
- Post-commit SURVIVES_POST_COMMIT claim for C-PARAM-INHERIT (not testable until fix committed)
- Hazard elimination rate of 0/6 on unfixed HEAD is diagnostic, not evidence against the fix

### Unknown
- Whether the fix will ever be committed
- Whether all baselines remain passing after fix commit
- Whether LLM-driven mechanism distillation works (no model calls in BLOCKED experiments)
- Whether semantic aliasing (C-SEMANTIC-RESOLVE) works in the current kernel — **this experiment tests this**

### Do Not Assume
- The fix is committed or will be committed
- Post-commit behavior matches monkey-patched behavior
- Production-readiness of jsonplaceholder results
- Generalization beyond single intent/endpoint
- The hazard is permanently closed
- C-PARAM-INHERIT is scientifically falsified (it is blocked, not rejected)
- Re-running the same BLOCKED spec yields new information
- Semantic resolution (C-SEMANTIC-RESOLVE) is guaranteed to work — **it has its own falsification risk**

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
