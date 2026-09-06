# EXP-GRAPH-33955869291 Report

## Executive Summary

**Experiment**: Generalization of parameter-slot-count tie-break to multi-slot mechanisms, template-only params, equal-slot ties, and verify() with non-200 HTTP responses.

**Outcome**: SUPPORTS (status=COMPLETE) — decision rule yields GENERALIZATION-SAFE

**Decision**: All 5 required conditions pass. The parameter-slot-count tie-break fix generalizes safely beyond the single-slot case tested in the parent experiment. The fix is ready for production commitment (requires Director approval).

## Key Findings

### 1. Baseline Regression: PASS
All 5 baseline conditions match parent experiment results exactly:
- literal-only-original: EXECUTABLE url=/posts/1
- literal-only-unseen: EXECUTABLE url=/posts/1 (literal universal matching)
- param-only-original: EXECUTABLE url=/posts/1
- param-only-unseen: EXECUTABLE url=/posts/2 (param generalization)
- confidence-disambiguate: EXECUTABLE param-fetch-posts-high (0.98) wins over literal (0.95)

### 2. Multi-Slot Dominance: PASS
A 2-slot param (parameter_slots=['id','category']) beats a 1-slot param (parameter_slots=['id']) at equal confidence (0.95). The tuple sort (confidence, len(parameter_slots)) correctly orders (0.95, 2) > (0.95, 1). Winning mechanism: param-2slot with bound URL /posts/3/tech.

### 3. Template-Only Param Handling: PASS
A template-only param (parameter_slots=[], template=/posts/${id}) loses to a declared 1-slot param (parameter_slots=['id']) at equal confidence. The fix uses len(parameter_slots) not len(required_slots), so template-only params get no slot-count credit. This confirms the parent audit finding V_TIEBREAK_SLOT_COUNT_SCOPE_LIMIT.

### 4. Template-Only vs Literal: INFORMATIVE (not pass/fail)
Template-only-fetch beats literal-fetch-posts-1 at equal confidence. Both have len(parameter_slots)=0 → tie → lexicographic on mechanism_id. Since 'template-only-fetch' < 'literal-fetch-posts-1' lexicographically, template-only wins. This outcome is deterministic but ID-dependent.

### 5. Equal-Slot Ties: INFORMATIVE (not pass/fail)
- param-vs-param tie: param-fetch-posts beats param-fetch-alt (lexicographic)
- lit-vs-lit tie: literal-fetch-posts-1 beats literal-alt (lexicographic)
Both are deterministic but ID-dependent.

### 6. verify() Correctness: PASS
- verify-200-match: True (postconditions={status:200} matches observed status=200)
- verify-404-mismatch: False (postconditions={status:200} does NOT match observed status=404)

The verify() postcondition matching correctly rejects non-matching HTTP responses.

## Interpretation

The parameter-slot-count tie-break fix generalizes safely to multi-slot mechanisms. The critical test was condition (2): template-only params lose to declared params despite needing params. This confirms the fix uses declared parameter_slots only, not required_slots computed from templates. The scope limitation noted in the parent audit (V_TIEBREAK_SLOT_COUNT_SCOPE_LIMIT) is confirmed and bounded.

Template-only params (parameter_slots=[] but template has ${id}) are not reliably preferred over literals. This is an informative finding: if a mechanism needs parameters but declares none, it loses the slot-count tie-break. This does not affect the safety of the fix for mechanisms that correctly declare their parameter_slots.

## Consequences

### For C-PARAM-INHERIT
- The competition hazard is resolved for multi-slot mechanisms on synthetic substrate.
- The fix can be committed to production kernel with Director approval.
- Template-only params remain a known limitation: they lose to literals at equal confidence.
- The claim ceiling extends to multi-slot, single-intent, deterministic synthetic substrate.

### For Product Registration
- Multi-slot mechanisms can be safely registered at equal confidence.
- Template-only params should be avoided alongside literals at equal confidence.
- verify() postcondition matching works for non-200 HTTP responses.

## Validity Threats

1. **Synthetic substrate**: All resolution conditions use jsonplaceholder.typicode.com without HTTP execution. Only verify() conditions make real HTTP requests. Generalizability to real-web endpoints with DOM, auth, session, drift is not tested.

2. **Fix not committed**: The one-line fix is applied temporarily during execution. Production promotion requires Director-approved commit.

3. **Lexicographic tie-breaking**: Equal-slot-count ties fall back to lexicographic ordering on mechanism_id. This is deterministic but ID-dependent. The experiment records actual outcomes but does not claim lexicographic ordering is "correct".

4. **Template-only param semantic ambiguity**: A mechanism with parameter_slots=[] but template ${id} is semantically parameterized but declares no slots. The fix uses len(parameter_slots) not len(required_slots). This means template-only params get no slot-count credit.

5. **verify() postcondition matching**: verify() uses _matches(postconditions, observed_state) which checks dict equality. More complex postcondition matching (partial matching, type coercion) is not tested.

## Next Steps

1. **Director action**: Commit the one-line fix to src/spider/kernel.py L112.
2. **Real-web testing**: Test parameterized mechanisms on real-web endpoints with DOM, auth, session, drift.
3. **LLM distillation**: Test the 'learn on A' half of C-PARAM-INHERIT with model calls.
4. **Template-only param improvement**: Consider using len(required_slots) instead of len(parameter_slots) if template-only params need better handling.

## Appendix: Raw Evidence

Raw evidence and derived measurements are available in:
- `raw_evidence.json` (SHA-256: c6262ebc9435cfc64ddf996b5fecf498cebb4875b6d831962040ac0acf8dc8ed)
- `derived_measurements.json` (SHA-256: 8f5d199684d312d0f81a8b749bacb14bf302e55ad77347c2661b5376af29de96)