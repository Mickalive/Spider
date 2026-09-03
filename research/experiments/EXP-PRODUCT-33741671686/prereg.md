# EXP-PRODUCT-33741671686 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-33741671686
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-03
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does parameter induction generalize to multi-parameter mechanisms with multiple distinct varying fields (path, body, headers) and distinct slot naming, when training observations come from synthetic but structurally realistic multi-field mechanisms?

## 3. Motivation

Prior experiment EXP-PRODUCT-33528829801 established:
- `distill_parameterized()` with `_extract_varying_values()` correctly induces one parameter slot for isomorphic action paths
- Parameterized mechanism resolves to EXECUTABLE with correct bound_action for all 10 unseen single-char identifiers (10/10)
- Literal mechanism replay fails on all unseen identifiers (0/10 EXECUTABLE)
- Positive control passes (seen identifier resolves correctly)
- Null control passes (mismatched preconditions abstain)

The claim ceiling is narrow: single-parameter, single-field, common-prefix heuristic only. The audit identified multi-parameter collision as a required fix (kernel `_extract_varying_values()` hardcodes `param_name='id'` for every varying leaf, collapsing distinct logical parameters).

The parent handoff explicitly identifies the next question: "Does parameter induction generalize to multi-parameter mechanisms (e.g., POST /api/${resource}/${id} with body {name:${title}}) with distinct slot naming?"

This experiment tests multi-parameter induction on synthetic observations with three distinct varying fields: a path segment, a body value, and a header value. This is the natural next step because it challenges the same kernel mechanism on a materially harder pattern without requiring external infrastructure.

## 4. Hypotheses

### H1: Distinct Slot Induction
Parameter induction identifies >= 3 distinct parameter slots (one per varying field: resource in path, title in body, token in header).

### H2: Unseen Resolution
Unseen parameter combinations resolve to EXECUTABLE with >= 90% rate (9/10 unseen combinations).

### H3: Binding Accuracy
All resolved bound_actions have correct value substitutions in the correct slots (100% accuracy).

### H4: Single-Slot Baseline Failure
A single-slot mechanism (all varying fields collapsed to one param_name='id') fails on all unseen multi-parameter combinations.

### H5: Positive Control
Resolution with all seen training identifiers returns EXECUTABLE with correct bound_action.

### H6: Null Control
Resolution with mismatched preconditions (authenticated=False) returns UNKNOWN (abstains).

## 5. Data Generation

### 5.1 Synthetic Observations

All observations share:
- **Intent**: "create-resource"
- **Preconditions**: `{"authenticated": true, "role": "admin"}`
- **Postconditions**: `{"created": true}`

Each observation differs in three fields:
- **Path**: `/api/${resource}/${id}` (resource and id segments vary)
- **Body**: `{"title": "${title}", "content": "fixed-content"}` (title varies)
- **Headers**: `{"Authorization": "Bearer ${token}"}` (token varies)

### 5.2 Training Set (3 observations)

| # | Resource | ID | Title | Token | Expected Slots |
|---|----------|-----|-------|-------|----------------|
| T1 | books | 101 | Alpha | tok-alpha | resource, id, title, token |
| T2 | users | 202 | Beta | tok-beta | resource, id, title, token |
| T3 | orders | 303 | Gamma | tok-gamma | resource, id, title, token |

### 5.3 Test Set (10 unseen combinations)

Each test combination uses resource/id/title/token values never jointly observed in training:

| # | Resource | ID | Title | Token |
|---|----------|-----|-------|-------|
| U1 | products | 404 | Delta | tok-delta |
| U2 | invoices | 505 | Epsilon | tok-epsilon |
| U3 | articles | 606 | Zeta | tok-zeta |
| U4 | comments | 707 | Eta | tok-eta |
| U5 | reviews | 808 | Theta | tok-theta |
| U6 | tasks | 909 | Iota | tok-iota |
| U7 | events | 111 | Kappa | tok-kappa |
| U8 | messages | 222 | Lambda | tok-lambda |
| U9 | sessions | 333 | Mu | tok-mu |
| U10 | profiles | 444 | Nu | tok-nu |

Note: Individual values may overlap with training (e.g., "products" is new but "101" is reused as a number), but no full combination was seen in training.

### 5.4 Induction Method

The kernel's `distill_parameterized()` method receives the 3 training observations and must:
1. Compare action templates across observations
2. Identify which fields vary and which are constant
3. For each varying field, determine the longest common prefix/suffix
4. Assign distinct parameter slot names per varying field location
5. Produce an action template with `${slot_name}` placeholders

Expected induced template (conceptual):
```json
{
  "method": "POST",
  "path": "/api/${resource}/${id}",
  "body": {"title": "${title}", "content": "fixed-content"},
  "headers": {"Authorization": "Bearer ${token}"}
}
```
With parameter_slots: ["resource", "id", "title", "token"]

### 5.5 Sample Size

- 3 training observations (minimum for cross-observation comparison)
- 10 test combinations (sufficient for clear binary result at >= 90% threshold)
- Total: 13 observations

## 6. Measures

### 6.1 Primary Metric: Distinct Slot Count
Count of distinct parameter slots identified by induction. Must be >= 3.

### 6.2 Primary Metric: Unseen Resolution Rate
Fraction of 10 unseen combinations resolving to EXECUTABLE. Threshold: >= 90%.

### 6.3 Primary Metric: Binding Accuracy
Fraction of resolved combinations where bound_action has correct value substitution in correct slot. Threshold: 100%.

### 6.4 Secondary Metric: Single-Slot Baseline Failure Rate
Fraction of unseen combinations where a single-slot mechanism fails. Expected: 100%.

### 6.5 Control Metrics
- Positive control: EXECUTABLE for seen combination
- Null control: UNKNOWN for mismatched preconditions

## 7. Null Models

### 7.1 Single-Slot Baseline (B3)
Mechanism induced with all varying fields collapsed to one param_name='id' slot. This tests whether the previous experiment's single-slot limitation causes failure on multi-parameter data.

### 7.2 Literal Baseline (B2)
Mechanism with no parameter slots (literal action template). Cannot bind any new identifiers.

### 7.3 Cold Baseline (B1)
No memory; full task re-exploration cost.

## 8. Statistical Tests

This experiment is deterministic and synthetic. All metrics are computed exactly (no sampling uncertainty). The decision rule is threshold-based, not p-value-based.

- Distinct slot count: integer >= 3
- Unseen resolution rate: exact fraction >= 0.9
- Binding accuracy: exact fraction = 1.0
- Literal failure rate: exact fraction = 1.0

## 9. Controls

### 9.1 Positive Control
- Input: Training observation T1 identifiers (resource=A, title=Alpha, token=tok-alpha)
- Expected: EXECUTABLE with correct bound_action
- Verifies: Induction did not break seen-combination resolution

### 9.2 Null Control
- Input: Mismatched preconditions (authenticated=False)
- Expected: UNKNOWN (abstains)
- Verifies: Applicability guards still enforce preconditions

### 9.3 Single-Slot Baseline Control
- Input: Test combinations with single-slot mechanism
- Expected: Fails on all unseen combinations (multiple parameters cannot be expressed in one slot)
- Verifies: Multi-parameter induction is necessary, not merely beneficial

## 10. Validity Threats

### 10.1 Synthetic Data
All observations are perfectly structured. Real web observations have noise, varying schemas, and multi-step actions. The parameter induction heuristic may fail on noisier inputs. **Mitigation**: This is a controlled kernel-level test. If the mechanism cannot handle clean multi-parameter data, it cannot handle noisy data.

### 10.2 Simple Parameter Pattern
Parameters are in distinct fields (path, body, header). Real mechanisms may have parameters in the same field (e.g., two path segments) or nested structures. **Mitigation**: Distinct-field parameters are the minimal multi-parameter case. Same-field parameters are a further generalization for future work.

### 10.3 Small Sample
10 unseen combinations is sufficient for a clear binary result but not for confidence intervals. **Mitigation**: Decision threshold is binary (>= 90%), not a point estimate.

### 10.4 Kernel Implementation Risk
The kernel's `distill_parameterized()` may not currently support multi-parameter induction. If the implementation is missing or incomplete, the experiment will produce a clear negative result (induction fails), which is still informative. **Mitigation**: The experiment measures what exists, not what was promised.

### 10.5 Tautological Construction
Like the previous experiment, training observations are synthetic and the induction heuristic is designed for prefix/suffix patterns. A positive result demonstrates the mechanism works on its designed input class, not that it generalizes to arbitrary patterns. **Mitigation**: Ceiling is explicitly limited to "synthetic multi-parameter common-prefix" level.

## 11. Decision Rules

### 11.1 SURVIVES
If ALL of:
1. Parameter induction identifies >= 3 distinct parameter slots
2. Unseen resolution rate >= 90% (9/10)
3. Binding accuracy = 100% (all resolved bound_actions correct)
4. Single-slot baseline fails on all unseen combinations (literal_fail_rate = 100%)
5. Positive control passes (EXECUTABLE)
6. Null control passes (UNKNOWN)

### 11.2 FALSIFIED
If ANY of:
1. Parameter induction identifies < 3 distinct slots
2. Unseen resolution rate < 90%
3. Binding accuracy < 100%
4. Single-slot baseline succeeds on any unseen combination
5. Positive control fails
6. Null control fails

### 11.3 MEASUREMENT_INVALID
If:
1. Kernel implementation is missing or produces errors
2. Induction produces degenerate output (e.g., no slots at all)
3. Infrastructure failure prevents execution

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES)
- Multi-parameter induction is viable at the kernel level
- C-PARAM-INHERIT claim ceiling extends from single-parameter to multi-parameter
- Product can support mechanisms with multiple independent parameter slots
- Next step: noisy/real-browser observation testing

### 12.2 Negative Result (FALSIFIED)
- Kernel's prefix/suffix heuristic cannot handle multi-parameter patterns
- C-PARAM-INHERIT remains limited to single-field mechanisms
- Kernel design must be reconsidered before further product investment
- Specific failure mode (slot collision, naming failure, binding error) identifies the required fix

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Kernel infrastructure needs repair before this question can be answered
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Observation Generation**: Create 3 training and 10 test observations as specified in §5.2-5.3
2. **Kernel Extension**: Extend `distill_parameterized()` in `src/spider/kernel.py` to support multi-parameter induction with distinct slot naming
3. **Induction**: Run `distill_parameterized()` on training observations
4. **Slot Audit**: Count distinct parameter slots; verify >= 3
5. **Resolution Test**: For each of 10 unseen combinations, call `kernel.resolve()` with the 4 parameter values
6. **Binding Audit**: For each resolved combination, verify bound_action has correct substitutions
7. **Baseline Tests**: Run B1 (cold), B2 (literal), B3 (single-slot) baselines
8. **Controls**: Run positive and null controls
9. **Decision**: Apply frozen decision rule

## 14. Analysis Code

Analysis will be implemented in Python using:
- The existing `spider` kernel module (`src/spider/`)
- Standard library only for test execution
- JSON for raw evidence storage

Code will be committed to `research/experiments/EXP-PRODUCT-33741671686/` before execution.

## 15. Pre-registered Expectations

From prior experiment:
- Single-parameter induction works (10/10 unseen resolution, 100% binding accuracy)
- Kernel uses longest common prefix/suffix heuristic with `is_id_like` regex
- Kernel hardcodes `param_name='id'` for every varying leaf

Expected challenges for multi-parameter:
- Distinct slot naming requires tracking which field location varies, not just that it varies
- Body and header parameters may require different slot naming conventions than path parameters
- The `is_id_like` regex may reject non-identifier values (titles, tokens with special chars)

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
