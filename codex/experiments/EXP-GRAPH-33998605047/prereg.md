# EXP-GRAPH-33998605047 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-33998605047
- **Lane**: Graph
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Parent**: EXP-GRAPH-33955869291 (handoff sha256: 423be67d7374d5c7fb271c44146735e754ab46708b396bdaedb8dd99d93354d4)
- **Date**: 2026-09-05
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the parameter-slot-count fix, applied temporarily during execution, eliminate the original 5/5 false accepts from the literal-vs-param equal-confidence hazard (EXP-GRAPH-33718012817) without regressing any baseline conditions, and does it generalize to multi-slot (2 vs 1) and template-only parameter scenarios?

## 3. Motivation

The parameter-slot-count fix (`candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)`) was validated on synthetic substrate for single-slot and single multi-slot pair (EXP-GRAPH-33955869291). However:

1. **The original hazard was not directly re-tested**: EXP-GRAPH-33955869291 tested multi-slot dominance and template-only conditions but did not re-run the original compete-equal-id2 through id6 conditions from EXP-GRAPH-33718012817 that demonstrated the false accepts.

2. **The fix is NOT committed to production HEAD**: `src/spider/kernel.py` L112 still uses `candidates.sort(key=lambda m: m.confidence, reverse=True)`. Real-web testing requires the fix to be committed first (parent handoff).

3. **The parent recommended**: commit fix → re-validate in committed HEAD → advance to real-web testing. This experiment is the "re-validate" step before commit.

The highest-upside next question is real-web endpoints with DOM, auth, session state, and drift. But that requires the fix to be committed first. This experiment validates the fix on the original hazard before committing.

## 4. Inherited State (from parent handoff)

### Established
- Multi-slot dominance confirmed for single tested pair (2 vs 1)
- Template-only params (parameter_slots=[] but template ${id}) lose to declared 1-slot param at equal confidence
- verify() dict equality works for matching/non-matching postconditions
- 5/5 solo baselines preserved
- Confidence dominates slot count: (0.98,1) > (0.95,0)
- All 12 observations independently recomputed and match

### Rejected
- Equal-slot-count ties are insertion-order (not lexicographic)
- Template-only params are reliably handled (they lose to literals by insertion order at equal confidence)

### Unknown
- Whether the fix generalizes to real-web endpoints with DOM, auth, session state, and drift
- Whether the literal-vs-param equal-confidence competition remains param-winning after fix commit
- Whether the fix generalizes to other slot counts (3 vs 2, 5 vs 1)

### Do NOT Assume
- Fix is committed to production HEAD (it is NOT)
- Template-only params work correctly in production
- verify() works end-to-end with HTTP
- Fix generalizes beyond single tested multi-slot pair

## 5. Hypotheses

### H1: False Accept Elimination
The fix eliminates all 5 false accepts in compete-equal-id2 through id6: param wins over literal at equal confidence for all tested id values.

### H2: Baseline Preservation
All 7 baseline conditions (cold, literal-only-original, literal-only-unseen, param-only-original, param-only-unseen, compete-param-higher, compete-literal-higher) match expected outcomes with no regression.

### H3: Multi-Slot Generalization
2-slot param beats 1-slot param at equal confidence (multi-slot dominance).

### H4: Template-Only Handling
Declared param (parameter_slots=['id']) beats template-only (parameter_slots=[]) at equal confidence.

## 6. Conditions

### Baselines (7 conditions)
| ID | Registry | Params | Expected | Role |
|----|----------|--------|----------|------|
| cold | empty | {id:2} | UNKNOWN | baseline |
| literal-only-original | literal-only | {id:1} | EXECUTABLE url=/posts/1 | baseline |
| literal-only-unseen | literal-only | {id:2} | EXECUTABLE url=/posts/1 | baseline |
| param-only-original | param-only | {id:1} | EXECUTABLE url=/posts/1 | baseline |
| param-only-unseen | param-only | {id:2} | EXECUTABLE url=/posts/2 | baseline |
| compete-param-higher | shared-param-higher | {id:3} | EXECUTABLE param wins | baseline |
| compete-literal-higher | shared-literal-higher | {id:3} | EXECUTABLE literal wins | baseline |

### Interventions (9 conditions)
| ID | Registry | Params | Expected | Role |
|----|----------|--------|----------|------|
| compete-equal-id2 | shared-equal | {id:2} | EXECUTABLE param wins | intervention |
| compete-equal-id3 | shared-equal | {id:3} | EXECUTABLE param wins | intervention |
| compete-equal-id4 | shared-equal | {id:4} | EXECUTABLE param wins | intervention |
| compete-equal-id5 | shared-equal | {id:5} | EXECUTABLE param wins | intervention |
| compete-equal-id6 | shared-equal | {id:6} | EXECUTABLE param wins | intervention |
| multi-slot-beats-1-slot | 2slot-vs-1slot | {id:3, category:tech} | EXECUTABLE 2slot wins | intervention |
| template-only-vs-param | template-only-vs-param | {id:3} | EXECUTABLE param wins | intervention |
| template-only-vs-literal | template-only-vs-literal | {id:3} | EXECUTABLE (record winner) | intervention |
| equal-slot-tie | equal-slot-param-vs-param | {id:3} | EXECUTABLE (record winner) | intervention |

## 7. Controls

### Positive Control (multi-slot-beats-1-slot)
2-slot param (len=2) must beat 1-slot param (len=1) at equal confidence via tuple sort. Verifies multi-slot dominance works.

### Null Control (compete-equal-id conditions)
Before fix: literal won at equal confidence (false accepts). After fix: param must win. If literal still wins, fix is insufficient.

### Sensitivity Control (baseline conditions)
All 7 baselines must match parent results. Any regression indicates fix introduces new problems.

## 8. Decision Rules

### FIX-VALIDATED
If ALL of:
1. All 7 baselines match expected outcomes
2. compete-equal-id2 through id6 ALL return param-fetch-posts as winning mechanism
3. multi-slot-beats-1-slot returns param-2slot winning
4. template-only-vs-param returns param-declared-slots winning
5. No exceptions or unexpected statuses

### PARTIAL-VALIDATION
If baselines pass but some compete-equal-id conditions still return literal (partial false accept elimination).

### FIX-INSUFFICIENT
If baselines pass but majority of compete-equal-id conditions still return literal.

### COMPETITION-UNSAFE
If any baseline regresses.

### MEASUREMENT_INVALID
If fix causes exceptions or unexpected statuses.

## 9. Validity Threats

### 9.1 Synthetic Substrate
All conditions use jsonplaceholder.typicode.com — generalizability to real-web endpoints not tested here. Mitigation: this is prerequisite validation; real-web testing is the next gate.

### 9.2 Fix Applied Temporarily
Fix is not committed to HEAD. Production remains unfixed. Mitigation: same approach as parent experiment; commit requires Director approval after this validation.

### 9.3 No HTTP Execution
Resolution conditions are logic-only. Network availability not tested. Mitigation: HTTP execution is out of scope for this experiment; real-web testing is the next gate.

### 9.4 Single-Run Determinism
All conditions deterministic: no model calls, no RNG, no sampling. Single-run exact point comparisons. No statistical uncertainty.

### 9.5 Registry Insertion Order
Literal registered before param in competition conditions. Different insertion order could change tie-break behavior. Mitigation: insertion order is controlled and documented; equal-slot ties are known to be insertion-order dependent (established in parent).

## 10. Analysis Plan

1. Execute all 16 conditions with fix applied temporarily
2. Record resolution status, winning mechanism, and bound_action URL for each
3. Check baselines: all 7 must match expected outcomes
4. Check false accepts: compete-equal-id2 through id6 must all return param-fetch-posts
5. Check multi-slot: 2-slot must beat 1-slot
6. Check template-only: declared param must beat template-only
7. Apply decision rule
8. Report all outcomes with equal prominence

## 11. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 12. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
