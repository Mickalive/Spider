# EXP-GRAPH-33955869291 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-33955869291
- **Lane**: Graph
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-05
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-GRAPH-33816735314 (COMPETITION-SAFE)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does the parameter-slot-count tie-break generalize safely to multi-slot mechanisms (2 vs 1 slot), template-only params with parameter_slots=[] but template ${id}, equal-slot-count ties (0 vs 0 or 1 vs 1), and does verify() correctly reject non-matching postconditions for non-200 HTTP responses?

## 3. Motivation

### What the parent experiment established (EXP-GRAPH-33816735314)

The parent experiment tested whether a parameter-slot-count secondary tie-break resolves false accepts in mixed literal+parameterized registries at equal confidence. It produced:

**Established:**
- Parameter-slot-count tie-break (Option A) eliminates 5/5 eligible false accepts in mixed literal+parameterized registries at equal confidence on deterministic synthetic substrate
- All baseline conditions preserved: cold UNKNOWN, literal-only orig/unseen EXECUTABLE, param-only orig/unseen EXECUTABLE
- Confidence-based disambiguation preserved: higher confidence wins regardless of slot count
- Fix makes tie-break ID-independent for 0-vs-1 slot case (audit V_ID_INDEPENDENCE_WITH_FIX)
- Competition is COMPETITION-SAFE on tested substrate (13/13 conditions pass)

**Rejected:**
- The tie-break is universally safe: ceiling limited to single-slot, single-intent, deterministic synthetic substrate (audit V_TIEBREAK_SLOT_COUNT_SCOPE_LIMIT)
- The literal universal matching hazard is root-fixed: hazard mitigated by tie-break, not eliminated (audit V_LIT_UNIVERSAL_STILL_EXISTS)

**Unknown (from parent handoff):**
- Whether verify() postcondition checking works for non-200 HTTP responses (hardcoded status=200 per parent audit V_VERIFY_HARDCODED_STATUS)
- Whether kernel preconditions matching (_matches) discriminates beyond empty dict
- Whether _bind() preserves type for full-match template strings
- Whether parameterized mechanisms work on real-web endpoints with DOM, auth, session state, drift
- Whether the fix generalizes safely to multi-slot mechanisms (2 vs 1 slot), template-only params with parameter_slots=[] but template ${id}, and equal-slot-count ties (0 vs 0 or 1 vs 1)
- Whether the fix has been committed to production kernel

**Do Not Assume:**
- The fix is committed to production (current HEAD still unfixed)
- The tie-break is safe for multi-slot mechanisms (only single-slot tested)
- Template-only params are handled correctly (len(parameter_slots) would be 0)
- Equal-slot-count ties are deterministic (expected lexicographic/ID-dependent)
- The literal universal eligibility is removed (mitigated, not eliminated)
- C-PARAM-INHERIT is fully validated (competition hazard resolved, but learn-on-A and real-web untested)

### Why this experiment is different

The parent experiment tested a **single binary competition**: literal (0 slots) vs single-slot param (1 slot) at equal confidence. This experiment tests **boundary conditions** of the fix:

1. **Multi-slot dominance**: Does 2-slot param beat 1-slot param at equal confidence? The tuple sort (confidence, len(parameter_slots)) predicts yes: (0.95, 2) > (0.95, 1). This is the most natural generalization of the fix.

2. **Template-only params**: A mechanism with parameter_slots=[] but template ${id} has required_slots={id} (computed by _template_slots) but len(parameter_slots)=0. The fix uses len(parameter_slots) not len(required_slots). This means template-only params would lose to declared 1-slot params despite needing params. This is the parent audit finding V_TIEBREAK_SLOT_COUNT_SCOPE_LIMIT. Testing this directly determines whether the fix needs modification.

3. **Equal-slot-count ties**: When both mechanisms have the same parameter_slots length (0 vs 0 or 1 vs 1), the fix does not break the tie — lexicographic ordering on mechanism_id determines the winner. This is deterministic but ID-dependent. Testing confirms this behavior.

4. **verify() with non-200 responses**: The parent audit flagged that verify() postcondition checking was only tested with status=200 (V_VERIFY_HARDCODED_STATUS). This experiment tests verify() with both matching (200) and non-matching (404) postconditions using real HTTP responses.

## 4. Hypotheses

### H1: Multi-Slot Dominance
A 2-slot param beats a 1-slot param at equal confidence. Condition multi-slot-beats-1-slot returns EXECUTABLE with param-2slot as winning mechanism.

### H2: Template-Only Param Handling
A template-only param (parameter_slots=[], template=/posts/${id}) loses to a declared 1-slot param at equal confidence. Condition template-only-vs-param returns EXECUTABLE with declared param winning (len=1 > len=0). This confirms the fix uses declared slots only.

### H3: Template-Only vs Literal
A template-only param vs a literal at equal confidence produces a deterministic but ID-dependent outcome. Condition template-only-vs-literal returns EXECUTABLE with the lexicographically smaller mechanism_id winning. The outcome is informative about whether template-only params can compete with literals.

### H4: Equal-Slot Ties
Equal-slot-count ties (0 vs 0 or 1 vs 1) are resolved by lexicographic ordering on mechanism_id. Conditions equal-slot-tie-param-vs-param and equal-slot-tie-lit-vs-lit return EXECUTABLE with deterministic but ID-dependent winners.

### H5: verify() Correctness
verify() correctly accepts matching postconditions (status=200) and rejects non-matching postconditions (status=404). Condition verify-200-match returns True; verify-404-mismatch returns False.

### H6: Baseline Regression
All 5 baseline conditions match parent experiment results. No regression.

## 5. Mechanism Definitions

### 5.1 Literal Mechanism
- mechanism_id: "literal-fetch-posts-1"
- intent: "fetch-post"
- parameter_slots: []
- action_template: {"url": "https://jsonplaceholder.typicode.com/posts/1", "method": "GET"}
- postconditions: {"status": 200}
- confidence: 0.95 (or 0.98 in confidence-disambiguate)

### 5.2 Single-Slot Param Mechanism
- mechanism_id: "param-fetch-posts"
- intent: "fetch-post"
- parameter_slots: ["id"]
- action_template: {"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"}
- postconditions: {"status": 200}
- confidence: 0.95 (or 0.98 in confidence-disambiguate)

### 5.3 Two-Slot Param Mechanism
- mechanism_id: "param-2slot"
- intent: "fetch-post"
- parameter_slots: ["id", "category"]
- action_template: {"url": "https://jsonplaceholder.typicode.com/posts/${id}/${category}", "method": "GET"}
- postconditions: {"status": 200}
- confidence: 0.95

### 5.4 Template-Only Mechanism (No Declared Slots)
- mechanism_id: "template-only-fetch"
- intent: "fetch-post"
- parameter_slots: []
- action_template: {"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"}
- postconditions: {"status": 200}
- confidence: 0.95

### 5.5 Equal-Slot Param Mechanism (for tie testing)
- mechanism_id: "param-fetch-alt"
- intent: "fetch-post"
- parameter_slots: ["id"]
- action_template: {"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"}
- postconditions: {"status": 200}
- confidence: 0.95

### 5.6 Equal-Slot Literal Mechanism (for tie testing)
- mechanism_id: "literal-alt"
- intent: "fetch-post"
- parameter_slots: []
- action_template: {"url": "https://jsonplaceholder.typicode.com/posts/2", "method": "GET"}
- postconditions: {"status": 200}
- confidence: 0.95

## 6. Registry Configurations

Each condition uses a fresh kernel with a specific registry:

- **literal-only**: [literal-fetch-posts-1]
- **param-only**: [param-fetch-posts]
- **confidence-param-higher**: [param-fetch-posts (0.98), literal-fetch-posts-1 (0.95)]
- **2slot-vs-1slot-equal-conf**: [param-2slot (0.95), param-fetch-posts (0.95)]
- **template-only-vs-literal**: [template-only-fetch (0.95), literal-fetch-posts-1 (0.95)]
- **template-only-vs-param**: [template-only-fetch (0.95), param-fetch-posts (0.95)]
- **equal-slot-param-vs-param**: [param-fetch-posts (0.95), param-fetch-alt (0.95)]
- **equal-slot-lit-vs-lit**: [literal-fetch-posts-1 (0.95), literal-alt (0.95)]

## 7. Measures

### 7.1 Primary Metrics
- **resolution_status**: EXECUTABLE or UNKNOWN for each condition
- **winning_mechanism_id**: Which mechanism won the competition
- **bound_action_url**: The resolved URL after parameter binding
- **verify_result**: True or False for verify() conditions

### 7.2 Secondary Metrics
- **baseline_regression**: All 5 baseline conditions match parent (yes/no)
- **multi_slot_dominance**: 2-slot beats 1-slot (yes/no)
- **template_only_handling**: Template-only vs param outcome (param-wins / template-wins / lexicographic)
- **equal_slot_tie_behavior**: Lexicographic ordering confirmed (yes/no)
- **verify_correctness**: verify() accepts matching and rejects non-matching (yes/no)

## 8. Controls

### 8.1 Baseline Regression Controls (5 conditions)
- literal-only-original, literal-only-unseen, param-only-original, param-only-unseen, confidence-disambiguate
- All must match parent experiment results exactly
- If any regresses → COMPETITION-UNSAFE

### 8.2 Positive Control: Multi-Slot Dominance (1 condition)
- multi-slot-beats-1-slot: 2-slot param (len=2) vs 1-slot param (len=1) at equal confidence
- 2-slot must win: (0.95, 2) > (0.95, 1) in tuple sort
- If fails → fix does not generalize to multi-slot → COMPETITION-UNSAFE

### 8.3 Null Control: Confidence Dominance (1 condition)
- confidence-disambiguate: param (0.98) vs literal (0.95) at different slot counts
- Higher confidence must win regardless of slot count
- If fails → fix disrupts confidence-based sorting → COMPETITION-UNSAFE

### 8.4 Intervention: Template-Only Param (2 conditions)
- template-only-vs-literal: tests whether template-only can compete with literal
- template-only-vs-param: tests whether template-only loses to declared param
- Both outcomes are informative; neither is a failure unless unexpected exception occurs

### 8.5 Intervention: Equal-Slot Ties (2 conditions)
- equal-slot-tie-param-vs-param: 1-slot vs 1-slot → lexicographic
- equal-slot-tie-lit-vs-lit: 0-slot vs 0-slot → lexicographic
- Both should be deterministic; record actual winner

### 8.6 Intervention: verify() Correctness (2 conditions)
- verify-200-match: postconditions={status:200}, observed={status:200} → True
- verify-404-mismatch: postconditions={status:200}, observed={status:404} → False
- If either fails → verify() postcondition matching is broken

## 9. Validity Threats

### 9.1 Fix Not Committed to Production
Current HEAD src/spider/kernel.py still has simple sort key (no tuple). The experiment applies the fix temporarily during execution. This is consistent with parent experiment methodology. Production promotion requires Director-approved commit (separate from this experiment).

### 9.2 Synthetic Substrate
All resolution conditions use jsonplaceholder.typicode.com URL templates without HTTP execution. Only verify() conditions make real HTTP requests. This limits generalizability to real-web endpoints but eliminates network variability for core tie-break tests.

### 9.3 Lexicographic Tie-Breaking
Equal-slot-count ties fall back to lexicographic ordering on mechanism_id. This is deterministic but ID-dependent. The experiment records actual outcomes but does not claim lexicographic ordering is "correct" — it is the observed behavior of the fix.

### 9.4 Template-Only Param Semantic Ambiguity
A mechanism with parameter_slots=[] but template ${id} is semantically parameterized but declares no slots. The fix uses len(parameter_slots) not len(required_slots). This means template-only params get no slot-count credit. The experiment tests this directly and records the outcome. If the outcome is suboptimal (template-only loses to literal), the fix may need modification (e.g., use len(required_slots) instead).

### 9.5 verify() Postcondition Matching
verify() uses _matches(postconditions, observed_state) which checks dict equality. The experiment tests status=200 match and status=404 mismatch. More complex postcondition matching (e.g., partial matching, type coercion) is not tested here.

### 9.6 Sample Size
Each condition is a single deterministic run. No sampling, no confidence intervals. Results are exact point comparisons. Replication is trivial (same code, same inputs → same outputs).

## 10. Decision Rules

### 10.1 GENERALIZATION-SAFE
If ALL of:
1. All 5 baseline conditions match parent results (no regression)
2. multi-slot-beats-1-slot returns EXECUTABLE with param-2slot winning
3. template-only-vs-param returns EXECUTABLE with param-fetch-posts (declared slots) winning
4. verify-200-match returns True
5. verify-404-mismatch returns False
6. No Python exceptions or unexpected resolution statuses

### 10.2 SCOPE-LIMITED
If baselines pass and multi-slot works, but:
- template-only-vs-literal shows lexicographic dependence (informative but not safe for production)
- Equal-slot ties show lexicographic dependence (expected, not a failure)

### 10.3 COMPETITION-UNSAFE
If ANY of:
1. Any baseline condition regresses from parent results
2. Multi-slot-beats-1-slot fails (2-slot does not win)
3. verify() accepts non-matching postconditions or rejects matching ones
4. Fix causes Python exception or unexpected status

### 10.4 MEASUREMENT_INVALID
If:
1. HTTP requests fail for verify() conditions (network error, not matching error)
2. Code fix causes import errors or type mismatches
3. Registry setup produces degenerate conditions

## 11. Expected Outcomes

### 11.1 GENERALIZATION-SAFE (best case)
- Multi-slot dominance works: 2-slot beats 1-slot at equal confidence
- Template-only params correctly handled: declared param preferred over template-only
- verify() works with non-200 responses
- C-PARAM-INHERIT advances with broader safe scope
- Product can register multi-slot mechanisms safely

### 11.2 SCOPE-LIMITED (likely case)
- Multi-slot works, baselines pass
- Template-only vs literal shows lexicographic dependence (informative)
- Equal-slot ties show lexicographic dependence (expected)
- C-PARAM-INHERIT advances but with noted limitations
- Product should avoid registering template-only params alongside literals at equal confidence

### 11.3 COMPETITION-UNSAFE (negative case)
- Multi-slot fails or baseline regresses
- C-PARAM-INHERIT remains limited to single-slot case
- Alternative approaches (Option B: value-based constraints, Option C: required_slots-based sort) must be explored

### 11.4 MEASUREMENT_INVALID (infrastructure case)
- HTTP failures or code errors
- Not scientific evidence; needs infrastructure fix

## 12. Analysis Plan

1. **Setup**: Create fresh kernel instances per condition with specified registries
2. **Resolution**: Call resolve() with specified params, record status + winning_mechanism + bound_action
3. **Competition**: For competitive conditions, verify which mechanism won and whether bound_action is correct
4. **verify()**: For verify conditions, call verify() with specified observed_state, record True/False
5. **Baseline Check**: Compare all baseline results to parent experiment results
6. **Decision**: Apply frozen decision rule to determine verdict
7. **Reporting**: Report all outcomes with equal prominence

## 13. Analysis Code

Analysis will be implemented in Python using:
- src/spider/kernel.py (SpiderKernel, resolve, verify)
- src/spider/registry.py (MechanismRegistry)
- src/spider/models.py (Mechanism, Resolution)
- Standard library only (json, tempfile, urllib.request for HTTP)

Code will be committed to research/experiments/EXP-GRAPH-33955869291/ before execution.

## 14. Pre-registered Expectations

From the parent experiment and code analysis:
- Multi-slot dominance: EXPECTED to work (tuple sort ordering is clear: (0.95,2) > (0.95,1))
- Template-only vs param: EXPECT param to win (len(parameter_slots)=1 > len(parameter_slots)=0)
- Template-only vs literal: UNCERTAIN — both have len=0, lexicographic decides
- Equal-slot ties: EXPECT lexicographic ordering (deterministic but ID-dependent)
- verify(): EXPECT correct behavior (postcondition matching is simple dict equality)

## 15. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 16. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
