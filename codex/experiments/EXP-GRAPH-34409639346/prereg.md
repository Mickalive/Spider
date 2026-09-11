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

**Critical design revision from prior attempt:** The prior spec (same experiment_id) used 10 "pairs" with identical intent strings and identical mechanism IDs, making the binomial test degenerate (all 10 pairs yield the same deterministic outcome). This revision uses 10 independent intent-template pairs with distinct intent strings, each tested under both ID orderings (correct-first and aliased-first), yielding 20 independent aliased-pair conditions. The falsification test is applied to the aliased-first subset only, where tie-breaking would select the aliased mechanism — if the kernel instead selects the template-matching mechanism, that is evidence of semantic resolution.

## 4. Hypotheses

### H1: Exact Intent Matching (primary)
The kernel selects mechanisms based on exact intent string equality. When two mechanisms have identical intent strings but different URL templates, both qualify as candidates and selection is determined by confidence ordering then mechanism_id tie-breaking. The kernel does not analyze URL template structure.

### H2: No Semantic Aliasing
The kernel does NOT select the mechanism whose URL template matches the intent structure when doing so would require overriding tie-breaking. In the aliased-first subset (aliased mechanism has smaller ID), the kernel selects the aliased mechanism in 100% of cases.

### H3: Intent Filtering Works
When intent strings differ (one exact match, one syntactically different), only the exact match qualifies as a candidate. The kernel does not perform fuzzy or semantic intent matching.

## 5. Conditions

### 5.1 Baseline Conditions

| ID | Description | Expected Outcome |
|----|-------------|------------------|
| B-EMPTY-REGISTRY | Empty registry, intent "get-user-profile" | UNKNOWN |
| B-SINGLE-MECHANISM | One mechanism registered: intent="get-user-profile", template="/users/{id}", parameter_slots=["id"], confidence=0.9. Params={"id": 42}. | EXECUTABLE, mechanism_id=registered_id, bound_action={"url": "/users/42"} |
| B-CONFIDENCE-HIGHER | Two mechanisms with DIFFERENT intents: M_high intent="get-user-profile" confidence=0.95, M_low intent="list-user-posts" confidence=0.8. Resolve with intent="get-user-profile". | EXECUTABLE, mechanism_id=M_high |
| B-CONFIDENCE-EQUAL-DIFFERENT-INTENT | Two mechanisms with DIFFERENT intents, equal confidence (0.9): M_a intent="get-user-profile", M_b intent="list-user-posts". Resolve with intent="get-user-profile". | EXECUTABLE, mechanism_id=M_a (only exact intent match qualifies) |

### 5.2 Aliased Pair Conditions

For each of 10 independent intent-template pairs:

**Pair structure:**
- **Intent**: A pure semantic intent string (NO URL pattern) — e.g., "get-user-profile", "list-user-posts", "create-new-comment", etc.
- **M_correct**: intent=I, template matches intent structure (e.g., "/users/{id}" for "get-user-profile"), parameter_slots=[slot], confidence=0.9
- **M_aliased**: intent=I (same string), template is a DIFFERENT URL path (e.g., "/accounts/{uid}" for "get-user-profile"), parameter_slots=[different_slot], confidence=0.9
- **Params**: Satisfy both parameter_slots (e.g., {"id": 42, "uid": 42})

**Two ID orderings per pair:**
- **Correct-first**: M_correct.mechanism_id < M_aliased.mechanism_id (e.g., "c-01" vs "a-01"). Tie-breaking selects M_correct. Expected: kernel selects M_correct (but this is tie-breaking, not semantic resolution).
- **Aliased-first**: M_aliased.mechanism_id < M_correct.mechanism_id (e.g., "a-01" vs "c-01"). Tie-breaking selects M_aliased. Expected: if kernel does NOT perform semantic aliasing, selects M_aliased. If kernel DOES perform semantic aliasing, selects M_correct.

**10 independent pairs (distinct intent strings):**

| # | Intent | M_correct template | M_aliased template |
|---|--------|-------------------|-------------------|
| 1 | get-user-profile | /users/{id} | /accounts/{uid} |
| 2 | list-user-posts | /users/{id}/posts | /profiles/{uid}/entries |
| 3 | create-new-comment | /posts/{id}/comments | /articles/{id}/reviews |
| 4 | delete-item | /items/{itemId} | /objects/{objId} |
| 5 | update-settings | /users/{id}/settings | /accounts/{id}/preferences |
| 6 | search-content | /search/{query} | /find/{term} |
| 7 | get-order-details | /orders/{orderId} | /purchases/{purchaseId} |
| 8 | submit-form | /forms/{formId}/submit | /surveys/{surveyId}/respond |
| 9 | upload-file | /files/{fileId}/upload | /documents/{docId}/store |
| 10 | fetch-analytics | /analytics/{metricId} | /metrics/{indicatorId} |

**Total conditions:** 4 baselines + (10 pairs × 2 orderings) = 24 kernel calls.

### 5.3 Falsification Test

The falsification test applies to the **aliased-first subset** (10 conditions where aliased mechanism has smaller ID):

- If kernel does NOT perform semantic aliasing: selects M_aliased in 10/10 cases (tie-breaking always favors smaller ID)
- If kernel DOES perform semantic aliasing: selects M_correct in >=1/10 cases (overrides tie-breaking for semantic reasons)

Binomial test: H0: p=0.5 (chance), H1: p>0.5 (semantic aliasing). With n=10, 0/10 supports H0 (p=1.0), 1/10 gives p=0.011 (significant at alpha=0.05), >=2/10 gives p<=0.055 (marginally significant).

## 6. Measures

### 6.1 Primary Metric
- **aliased_first_correct_selection_rate**: Fraction of aliased-first conditions (n=10) where kernel selects M_correct (template matches intent structure). Expected: 0% if hypothesis is correct (kernel follows tie-breaking). >0% if semantic aliasing works.

### 6.2 Secondary Metrics
- Per-condition: resolution status, mechanism_id, bound_action, confidence
- correct_first_correct_selection_rate: Fraction of correct-first conditions where kernel selects M_correct. Expected: 100% (tie-breaking selects smaller ID, which is M_correct).
- Baseline pass rates
- Exception/crash count
- Verification that both mechanisms in each pair are candidates (intent matches, preconditions match, applicability_guards match, parameter_slots satisfied)

## 7. Controls

### 7.1 Positive Control
B-SINGLE-MECHANISM: When exactly one mechanism matches all filters, kernel returns EXECUTABLE. Verifies basic resolution pipeline works.

### 7.2 Null Control
B-EMPTY-REGISTRY: Empty registry returns UNKNOWN. Verifies kernel does not hallucinate candidates.

### 7.3 Confidence Ordering Control
B-CONFIDENCE-HIGHER: Higher confidence mechanism wins when intents differ. Validates confidence ordering is functional.

### 7.4 Intent Filtering Control
B-CONFIDENCE-EQUAL-DIFFERENT-INTENT: Only exact intent match qualifies when intents differ. Validates intent matching is exact, not fuzzy.

### 7.5 Tie-Breaking Consistency Control
correct-first subset (10 conditions): Kernel should select M_correct in 100% of cases (tie-breaking selects smaller ID). If kernel selects M_aliased in any correct-first condition, there is an unexpected tie-breaking behavior.

## 8. Validity Threats

### 8.1 Limited Power
With n=10 aliased-first conditions, the binomial test has limited power. 0/10 supports the hypothesis but does not prove it (Type II risk). 1/10 is significant at alpha=0.05. The test is designed as a proof-of-concept screen, not a definitive test. If 0/10, a larger follow-up (n=50+) would be needed for strong confirmation.

### 8.2 Synthetic Aliasing
The aliased templates are synthetic; real-world aliasing may involve more complex mapping (query parameters, path rewriting, server-side rewriting). Claim ceiling bounded to simple path aliasing with distinct parameter slot names.

### 8.3 Intent String as Semantic Intent
Intent strings are crafted as human-readable semantic intents (e.g., "get-user-profile") rather than URL patterns. This tests whether the kernel considers template structure beyond intent matching. However, the kernel's intent matching is exact string equality, so the intent string design does not affect the kernel's behavior — only the mechanism design does.

### 8.4 Deterministic n=1
All conditions deterministic; single-run exact comparisons valid for kernel-level test. No sampling variance.

### 8.5 Parameter Slot Naming
M_correct and M_aliased use different parameter slot names (e.g., "id" vs "uid"). Both are satisfied by the provided params. The kernel does not analyze parameter slot names — it only checks that all required slots are present in params. This is valid for testing template structure consideration.

## 9. Decision Rules

### 9.1 SURVIVES_CURRENT_TEST
If ALL of:
1. B-EMPTY-REGISTRY passes (UNKNOWN)
2. B-SINGLE-MECHANISM passes (EXECUTABLE)
3. B-CONFIDENCE-HIGHER passes (higher confidence wins)
4. B-CONFIDENCE-EQUAL-DIFFERENT-INTENT passes (single candidate)
5. No exceptions or crashes

ADDITIONALLY: hypothesis SUPPORTED if aliased_first_correct_selection_rate == 0% (kernel always follows tie-breaking, 0/10 correct selections in aliased-first subset).

### 9.2 FALSIFIED-IN-SETTING
If aliased_first_correct_selection_rate >= 10% (kernel selects template-matching mechanism in >=1/10 aliased-first conditions, binomial p<0.05 against chance 50%).

OR if any baseline fails (indicating infrastructure or kernel malfunction).

### 9.3 MEASUREMENT_INVALID
If infrastructure failures prevent measurement (kernel import errors, unexpected exceptions, registry corruption).

## 10. Expected Outcomes

### 10.1 Most Likely: SUPPORTED (kernel does NOT perform semantic aliasing)
- aliased_first_correct_selection_rate = 0% (kernel follows tie-breaking exactly)
- All baselines pass
- Claim C-SEMANTIC-RESOLVE falsified at current kernel level
- Product must either implement semantic aliasing resolution or require exact intent matching
- Graph lane should estimate engineering cost of building semantic resolution and weigh against other priority claims (C-FRESHNESS, C-DELTA-REPAIR, etc.)

### 10.2 Surprise: FALSIFIED-IN-SETTING (kernel DOES perform semantic aliasing)
- aliased_first_correct_selection_rate >= 10% (kernel overrides tie-breaking for semantic reasons)
- This would be unexpected given code analysis (line 97: exact intent matching)
- Would require explanation: is there hidden template analysis? Is the kernel doing something beyond what code inspection suggests?
- C-SEMANTIC-RESOLVE validated at proof-of-concept level
- Opens new product path: semantic aliasing for cross-site mechanism reuse

### 10.3 MEASUREMENT_INVALID
- Infrastructure failure, not scientific result
- Retry after infrastructure repair

## 11. Analysis Plan

1. **Mechanism Creation**: Create 10 pairs of semantically aliased mechanisms with controlled IDs (correct-first and aliased-first orderings).
2. **Baseline Execution**: Run 4 baseline conditions against fresh kernel instances.
3. **Aliased Pair Execution**: For each of 10 pairs, run resolve() under both correct-first and aliased-first orderings (20 conditions total).
4. **Metrics Computation**: Compute aliased_first_correct_selection_rate across 10 aliased-first conditions.
5. **Statistical Test**: Binomial test for aliased_first_correct_selection_rate vs 0.5 chance (one-sided, H1: p>0.5).
6. **Control Verification**: Check all baselines pass/fail.
7. **Tie-Breaking Verification**: Check correct-first subset yields 100% correct selection (tie-breaking consistency).
8. **Reporting**: Report all outcomes with equal prominence.

## 12. Analysis Code

Analysis will be implemented in Python using:
- `spider.kernel.SpiderKernel` for resolution
- `spider.registry.MechanismRegistry` for mechanism storage
- `spider.models.Mechanism`, `Resolution` for data structures
- `scipy.stats.binomtest` for binomial test
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-GRAPH-34409639346/` before execution.

## 13. Pre-registered Expectations

From kernel code analysis (kernel.py:93-123):
- Line 97: `if m.intent != intent` — exact intent matching, no fuzzy/semantic matching
- Line 99: `if not _matches(m.preconditions, context)` — exact precondition matching
- Line 101: `if not _matches(m.applicability_guards, context)` — exact guard matching
- Line 104-106: parameter_slots check — all required slots must be in params
- Line 112: `candidates.sort(key=lambda m: m.confidence, reverse=True)` — sort by confidence descending; stable sort preserves original order for equal confidence
- Original order is determined by `self.registry.all()` which reads from JSONL file in mechanism_id sorted order (registry.py:38: `sorted(items)`)

Therefore: for equal confidence, selection is determined by mechanism_id ordering (smaller ID wins). The kernel does NOT analyze URL template structure. Expected: aliased_first_correct_selection_rate = 0%.

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
