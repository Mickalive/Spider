# EXP-GRAPH-34409639346 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34409639346
- **Lane**: Graph
- **Claim**: C-SEMANTIC-RESOLVE (Goals can be resolved to applicable mechanisms without internal ids)
- **Date**: 2026-09-10
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-GRAPH-34395286092 (BLOCKED_CLOSE_AND_PIVOT)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does the kernel resolve semantically aliased URL templates (e.g., /users/{userId} vs /accounts/{id} pointing to the same REST resource) to the correct parametrized mechanism when both are registered with equal confidence, and does it correctly select the mechanism whose template matches the intent structure?

## 3. Motivation

### What the parent experiment established (EXP-GRAPH-34395286092)

The parent experiment was the fourth consecutive BLOCKED result on C-PARAM-INHERIT, due to an unfixed one-line prerequisite in kernel.py L112. The Director pivoted the graph lane to an orthogonal high-upside question: C-SEMANTIC-RESOLVE.

**Established (descriptive):**
- The parameter-slot-count hazard is real and reproducible on unfixed HEAD (kernel sha256 46929b3a)
- Param generalizes to unseen identifiers; literal does not
- All baselines pass on unfixed HEAD
- Confidence ordering works correctly
- HTTP execution against jsonplaceholder works
- Fix is NOT present in committed HEAD across 12+ branches

**Rejected:**
- Post-commit SURVIVES_POST_COMMIT claim (not testable until fix committed)
- Hazard elimination rate of 0/6 on unfixed HEAD is diagnostic only

**Unknown:**
- Whether semantic aliasing (C-SEMANTIC-RESOLVE) works in the current kernel — untested
- Whether the fix will ever be committed

**Do Not Assume:**
- Semantic resolution is guaranteed to work — it is a new untested question
- The kernel performs any fuzzy matching beyond exact intent string equality

### Why this experiment is different

This experiment tests a materially orthogonal question from C-PARAM-INHERIT. It does not depend on the unfixed sort key. The kernel's resolve() function (kernel.py:93-123) uses exact intent matching (line 97: `if m.intent != intent`). It does not analyze URL template structure. Therefore, we hypothesize the kernel does NOT perform semantic aliasing resolution.

The experiment uses deterministic kernel-level testing (no model calls) with controlled registry contents, similar to the C-PARAM-INHERIT experiments but with different mechanisms.

## 4. Hypotheses

### H1: Exact Intent Matching
The kernel selects the mechanism whose intent string exactly matches the provided intent, ignoring URL template structure. When two mechanisms have identical intent strings but different URL templates, selection is determined by confidence ordering and mechanism_id tie-breaking.

### H2: No Semantic Aliasing
The kernel does NOT select the mechanism whose URL template matches the intent structure (as defined by human evaluation) when intent strings are identical. Selection is not based on semantic similarity of URL templates.

### H3: Different Intent Rejection
When intent strings differ (one matches exactly, the other is semantically equivalent but syntactically different), the kernel selects only the exact match, not the semantically equivalent one.

## 5. Conditions

### 5.1 Baseline Conditions

| ID | Description | Expected Outcome |
|----|-------------|------------------|
| B-EXACT-INTENT-MATCH | Two mechanisms with identical intent strings (both contain URL pattern) but different URL templates. Mechanism IDs assigned such that template-matching mechanism has smaller ID. | Kernel selects mechanism with smaller ID (tie-breaking). |
| B-REVERSED-ID | Same as B-EXACT-INTENT-MATCH but mechanism IDs swapped (aliased mechanism has smaller ID). | Kernel selects aliased mechanism (smaller ID). |
| B-DIFFERENT-INTENT | Two mechanisms with different intent strings: one matches intent exactly (contains URL pattern), the other is semantically equivalent but syntactically different. | Kernel selects exact intent match. |
| B-EMPTY-REGISTRY | Empty registry, any intent. | UNKNOWN. |

### 5.2 Mechanism Design

For each of 10 semantically aliased pairs:
- **Intent string**: "GET /users/{userId}" (contains URL pattern)
- **M_correct**: intent="GET /users/{userId}", template="/users/{userId}", parameter_slots=["userId"]
- **M_aliased**: intent="GET /users/{userId}", template="/accounts/{id}", parameter_slots=["id"]
- **Confidence**: 0.9 (equal)
- **Preconditions**: empty dict
- **Applicability_guards**: empty dict
- **Parameter slots satisfied**: params={"userId": 42, "id": 42}

Mechanism IDs assigned as "c-{:02d}".format(i) and "a-{:02d}".format(i) (c < a) for B-EXACT-INTENT-MATCH, swapped for B-REVERSED-ID.

### 5.3 Total Conditions
- 4 baseline conditions x 10 pairs = 40 kernel calls
- All deterministic, no model calls, no RNG

## 6. Measures

### 6.1 Primary Metric
- **selection_rate_correct**: Fraction of pairs where kernel selects M_correct (template matches intent pattern). Expected: 50% (chance) if kernel does NOT perform semantic aliasing; >80% if kernel does.

### 6.2 Secondary Metrics
- Per-condition resolution status, mechanism_id, bound_action, confidence
- Exception/crash count
- Verification that both mechanisms are candidates (intent matches, preconditions match, applicability_guards match, parameter slots satisfied)

## 7. Controls

### 7.1 Positive Control
B-EXACT-INTENT-MATCH: When intents identical, kernel selects mechanism with smaller ID (deterministic). Verifies kernel's tie-breaking works.

### 7.2 Null Control
B-REVERSED-ID: When aliased mechanism has smaller ID, kernel selects aliased mechanism (not template-matching). Verifies kernel does NOT perform semantic aliasing resolution.

### 7.3 Different Intent Control
B-DIFFERENT-INTENT: When intents differ, kernel selects exact match. Verifies kernel does not perform fuzzy matching.

### 7.4 Empty Registry Control
B-EMPTY-REGISTRY: Kernel returns UNKNOWN. Verifies baseline behavior.

## 8. Validity Threats

### 8.1 Small Sample Size
Only 10 pairs may be underpowered for detecting subtle semantic resolution. However, this is a proof-of-concept test; a clear positive result (>80% correct) would be detectable.

### 8.2 Synthetic Aliasing
The aliased templates are synthetic; real-world aliasing may involve more complex mapping (e.g., query parameters, path rewriting). Claim ceiling bounded to simple path aliasing.

### 8.3 Intent String Design
Intent strings contain URL patterns; this may bias toward exact matching. Real-world intents may not contain URL patterns. Claim ceiling bounded to intents containing URL patterns.

### 8.4 Deterministic n=1
All conditions deterministic; single-run exact comparisons valid for kernel-level test.

## 9. Decision Rules

### 9.1 SURVIVES_CURRENT_TEST
If ALL of:
1. B-EXACT-INTENT-MATCH passes (kernel selects mechanism with smaller ID in 100% of pairs)
2. B-REVERSED-ID passes (kernel selects aliased mechanism with smaller ID in 100% of pairs)
3. B-DIFFERENT-INTENT passes (kernel selects exact intent match, not semantic equivalent)
4. B-EMPTY-REGISTRY passes (UNKNOWN)
5. No exceptions or crashes

### 9.2 FALSIFIED-IN-SETTING
If kernel selects template-matching mechanism in >=80% of pairs regardless of ID order (binomial test p<0.05 against chance 50%).

### 9.3 MEASUREMENT_INVALID
If infrastructure failures prevent measurement (e.g., kernel import errors, unexpected exceptions).

## 10. Expected Outcomes

### 10.1 Positive Result (FALSIFIED-IN-SETTING)
- Kernel already possesses semantic aliasing resolution capability
- Claim C-SEMANTIC-RESOLVE validated at proof-of-concept level
- Opens new product path: semantic aliasing for cross-site mechanism reuse
- Graph lane can build on this capability

### 10.2 Negative Result (SURVIVES_CURRENT_TEST)
- Kernel does NOT perform semantic aliasing resolution
- Claim C-SEMANTIC-RESOLVE falsified at current kernel level
- Product must either (a) implement semantic aliasing resolution, or (b) require explicit intent matching
- Graph lane must decide whether to build this capability

### 10.3 Invalid Result (MEASUREMENT_INVALID)
- Infrastructure failure, not scientific result
- Retry after infrastructure repair

## 11. Analysis Plan

1. **Mechanism Creation**: Create 10 pairs of semantically aliased mechanisms with controlled IDs.
2. **Condition Execution**: For each pair, run kernel.resolve() under B-EXACT-INTENT-MATCH and B-REVERSED-ID conditions.
3. **Different Intent Test**: For each pair, create a second mechanism with different intent string, run kernel.resolve().
4. **Empty Registry Test**: Run kernel.resolve() with empty registry.
5. **Metrics Computation**: Compute selection_rate_correct across pairs.
6. **Statistical Test**: Binomial test for selection_rate_correct vs 0.5 chance.
7. **Control Verification**: Check all controls pass/fail.
8. **Reporting**: Report all outcomes with equal prominence.

## 12. Analysis Code

Analysis will be implemented in Python using:
- `spider.kernel.SpiderKernel` for resolution
- `spider.registry.MechanismRegistry` for mechanism storage
- `spider.models.Mechanism`, `Observation`, `Resolution` for data structures
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-GRAPH-34409639346/` before execution.

## 13. Pre-registered Expectations

From kernel code analysis:
- Kernel uses exact intent matching (line 97: `if m.intent != intent`)
- Kernel does not analyze URL template structure
- Kernel sorts candidates by confidence descending (line 112)
- Kernel uses stable sort; tie-breaking determined by original order (mechanism_id order)
- Therefore, selection for identical intents is determined by mechanism_id order, not semantic aliasing
- If intents differ, only exact match passes the filter

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.