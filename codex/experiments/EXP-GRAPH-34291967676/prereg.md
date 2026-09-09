# EXP-GRAPH-34291967676 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34291967676
- **Lane**: Graph
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-09
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-GRAPH-34244445713 (BLOCKED)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

After committing the parameter-slot-count tie-break fix to src/spider/kernel.py L112 (sort key includes len(parameter_slots)), does the literal-vs-param equal-confidence competition resolve to param for all unseen ids 2-7 without monkey-patching, do all 6 baseline conditions pass on committed HEAD, does the corrected B_CONFIDENCE_LITERAL_HIGHER condition (literal 0.98 > param 0.95) remain literal-winning, and does the fix interact correctly with registry upsert sorting (production-like ordering)?

## 3. Motivation

### What the parent experiment established (EXP-GRAPH-34244445713)

The parent experiment tested the core false-accept hazard and baseline behavior on UNFIXED production HEAD. It produced:

**Established (descriptive):**
- Core hazard validated: at equal confidence (0.95), literal beats param for ALL unseen ids 2-7 (6/6 literal wins, 0/6 hazard elimination) when literal is registered before param
- Param generalizes: param-only-unseen resolves to /posts/7, HTTP 200, id=7
- Literal does not generalize: literal-only-unseen resolves to /posts/1, HTTP 200, id=1
- All 6 baselines pass on unfixed HEAD (cold, literal-only orig/unseen, param-only orig/unseen, compete-param-higher)
- Confidence ordering preserved: B-CONFIDENCE-LITERAL-HIGHER literal 0.98 beats param 0.95
- Fix NOT present in committed HEAD (kernel sha256 46929b3a, line 112 'candidates.sort(key=lambda m: m.confidence, reverse=True)')

**Rejected (measurement invalid for post-commit):**
- Post-commit claim (fix not committed — prerequisite unmet)
- Core hazard results (0/6 param wins) are diagnostic on unfixed HEAD, not evidence against fix effectiveness

**Unknown:**
- Whether fix survives commitment to production HEAD
- Whether param wins at equal confidence for ALL unseen ids after fix commit
- Whether baselines regress after fix commit
- Whether B_CONFIDENCE_LITERAL_HIGHER remains literal-winning after fix commit
- Whether fix interacts correctly with registry upsert sorting (production-like ordering)

**Do Not Assume:**
- Fix is committed (verified unfixed at parent experiment time — kernel sha256 46929b3a)
- Post-commit behavior matches monkey-patched behavior
- Production-readiness (jsonplaceholder is simple REST)
- Generalization beyond single intent, single endpoint, preconditions={}, deterministic n=1
- Fix works under upsert sorting (replace() used in parent experiment)

### Why this experiment is different

This experiment is identical in structure to the parent but differs in two critical dimensions:

**Parent**: Tested on UNFIXED HEAD (fix absent, no monkey-patching — experiment ran exactly as committed)
**This experiment**: Tests on COMMITTED HEAD (fix present, no monkey-patching)

Additionally, this experiment adds a validity check for production-like registry ordering (upsert) that was not present in the parent.

The fix is a one-line change to src/spider/kernel.py L112:
```python
# BEFORE (unfixed):
candidates.sort(key=lambda m: m.confidence, reverse=True)
# AFTER (fixed):
candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
```

The fix adds `len(parameter_slots)` as a secondary sort key. When confidences are equal, mechanisms with more parameter slots (param, slots >= 1) sort higher than mechanisms with zero parameter slots (literal, slots = 0).

**Key difference from parent**: No monkey-patching. The fix must be committed to production HEAD before execution. If the fix is not present, the experiment is BLOCKED (not FALSIFIED).

## 4. Hypotheses

### H1: Post-Commit Hazard Elimination
With the fix committed, compete-equal (literal 0.95 vs param 0.95, literal registered first) resolves to param for ALL unseen ids 2-7 (6/6 param wins).

### H2: Baseline Preservation
All 6 baseline conditions pass on committed HEAD with the fix present. No regression from parent experiment baseline behavior.

### H3: Confidence Ordering Preservation
B_CONFIDENCE_LITERAL_HIGHER (literal 0.98 vs param 0.95) remains literal-winning. The fix does not override strict confidence ordering.

### H4: Fix Presence
The fix is verified present in committed HEAD: src/spider/kernel.py L112 sort key includes `len(parameter_slots)`.

### H5: Upsert Compatibility
The fix remains effective under registry upsert sorting (production-like ordering by mechanism_id). C-EQUAL-UPSERT-ID7 resolves to param.

## 5. Conditions

### 5.1 Fix Verification (gate)
- Read src/spider/kernel.py L112
- Verify sort key includes `len(parameter_slots)`
- If absent: status=BLOCKED, skip all conditions

### 5.2 Baseline Conditions (6)

| ID | Registry | Context ID | Expected Status | Expected URL | Expected HTTP ID |
|----|----------|------------|-----------------|--------------|------------------|
| B-COLD | Empty | any | UNKNOWN | N/A | N/A |
| B-LITERAL-ONLY-ORIG | literal /posts/1 | 1 | EXECUTABLE | /posts/1 | 1 |
| B-LITERAL-ONLY-UNSEEN | literal /posts/1 | 7 | EXECUTABLE | /posts/1 | 1 |
| B-PARAM-ONLY-ORIG | param /posts/{id} | 1 | EXECUTABLE | /posts/1 | 1 |
| B-PARAM-ONLY-UNSEEN | param /posts/{id} | 7 | EXECUTABLE | /posts/7 | 7 |
| B-COMPETE-PARAM-HIGHER | literal (0.95) + param (0.98) | 7 | EXECUTABLE | /posts/7 | 7 |

### 5.3 Core Hazard Conditions (6)

| ID | Registry | Context ID | Expected Mechanism | Expected URL | Expected HTTP ID |
|----|----------|------------|--------------------|--------------|------------------|
| C-EQUAL-ID2 | literal (0.95) + param (0.95) | 2 | param | /posts/2 | 2 |
| C-EQUAL-ID3 | literal (0.95) + param (0.95) | 3 | param | /posts/3 | 3 |
| C-EQUAL-ID4 | literal (0.95) + param (0.95) | 4 | param | /posts/4 | 4 |
| C-EQUAL-ID5 | literal (0.95) + param (0.95) | 5 | param | /posts/5 | 5 |
| C-EQUAL-ID6 | literal (0.95) + param (0.95) | 6 | param | /posts/6 | 6 |
| C-EQUAL-ID7 | literal (0.95) + param (0.95) | 7 | param | /posts/7 | 7 |

**Registry order**: literal registered BEFORE param (worst-case insertion order, same as parent).

### 5.4 Null Control Condition (1)

| ID | Registry | Context ID | Expected Mechanism | Expected URL | Expected HTTP ID |
|----|----------|------------|--------------------|--------------|------------------|
| B-CONFIDENCE-LITERAL-HIGHER | literal (0.98) + param (0.95) | 7 | literal | /posts/1 | 1 |

**Purpose**: Verify fix does not override strict confidence ordering.

### 5.5 Upsert Compatibility Condition (1)

| ID | Registry | Context ID | Expected Mechanism | Expected URL | Expected HTTP ID |
|----|----------|------------|--------------------|--------------|------------------|
| C-EQUAL-UPSERT-ID7 | literal (0.95) + param (0.95) via upsert | 7 | param | /posts/7 | 7 |

**Registry order**: mechanisms inserted sequentially via upsert; final ordering determined by mechanism_id sorting (literal-posts-1 sorts before param-posts-id). This tests production-like ordering where the registry uses upsert rather than explicit replace().

### 5.6 Total Conditions
- 6 baselines (B-COLD, B-LITERAL-ONLY-ORIG, B-LITERAL-ONLY-UNSEEN, B-PARAM-ONLY-ORIG, B-PARAM-ONLY-UNSEEN, B-COMPETE-PARAM-HIGHER)
- 6 core hazard (C-EQUAL-ID2 through C-EQUAL-ID7, equal confidence 0.95)
- 1 null control (B-CONFIDENCE-LITERAL-HIGHER, literal higher confidence)
- 1 upsert compatibility (C-EQUAL-UPSERT-ID7, equal confidence 0.95 via upsert)
= **14 conditions total**

Note: B-COMPETE-PARAM-HIGHER (param 0.98 > literal 0.95) and C-EQUAL-ID7 (param 0.95 == literal 0.95) are different conditions with different confidence configurations.

## 6. Measures

### 6.1 Primary Metric
- **hazard_elimination_rate**: Fraction of core hazard conditions (ids 2-7) where param wins at equal confidence. Target: 6/6 = 1.0.
- **baseline_pass_rate**: Fraction of baseline conditions matching expected outcome. Target: 6/6 = 1.0.

### 6.2 Secondary Metrics
- Per-condition resolution status, mechanism_id, bound_url, confidence
- HTTP status code and response id field for each EXECUTABLE condition
- Fix verification: L112 content, kernel.py sha256
- Exception/crash count
- Network failure count
- Upsert condition outcome (C-EQUAL-UPSERT-ID7)

## 7. Controls

### 7.1 Fix Presence Control (prerequisite gate)
- Read src/spider/kernel.py L112
- Verify sort key includes `len(parameter_slots)`
- If absent: status=BLOCKED, outcome=NOT_APPLICABLE
- If present: proceed to all conditions

### 7.2 Baseline Preservation Controls (6 conditions)
Same as parent experiment. All 6 must pass to confirm no regression.

### 7.3 Core Hazard Test (6 conditions)
Same as parent experiment's core hazard test but with fix committed. All 6 must resolve to param.

### 7.4 Confidence Ordering Null Control (1 condition)
Same as parent experiment's B-CONFIDENCE-LITERAL-HIGHER. Must remain literal-winning.

### 7.5 Upsert Compatibility Control (1 condition)
New condition not present in parent. Tests fix under production-like registry ordering (upsert). Must resolve to param.

### 7.6 No-Monkey-Patch Attestation
The experiment script must not modify kernel.py at runtime. Fix must be in committed code. Script must verify no runtime modifications occurred.

## 8. Validity Threats

### 8.1 Fix Not Committed
If src/spider/kernel.py L112 is still unfixed, the experiment is BLOCKED. This is the correct outcome per the parent handoff's first gate. The experiment must not weaken the design to work around an unfixed codebase.

### 8.2 HTTP Endpoint Availability
jsonplaceholder.typicode.com must be reachable. Network failures are infrastructure issues, not scientific results. Record and report but do not classify as FALSIFIES.

### 8.3 Insertion Order Sensitivity
Literal is registered before param in all equal-confidence conditions (worst case). If the fix works under worst-case insertion order, it works under all insertion orders.

### 8.4 Simple REST Limitation
jsonplaceholder is not real Web (no DOM, no auth, no session state, no drift). Claim ceiling is bounded to simple REST parameterized inheritance. Real-web generalization is a separate future experiment.

### 8.5 Deterministic n=1
All conditions are deterministic (no model calls, no RNG). Single-run exact comparisons are valid for this kernel-level test. No statistical inference needed.

### 8.6 Single Endpoint
Only /posts/{id} is tested. Generalization to other endpoints, multi-parameter templates, nested routes, and non-empty preconditions is not tested here.

### 8.7 Upsert Ordering Assumption
Upsert sorts by mechanism_id. The assumption is that literal-posts-1 sorts before param-posts-id (lexicographic 'l' < 'p'). If mechanism_ids differ, ordering may change. This is a minor threat because the worst-case insertion order (literal before param) is already tested in core hazard conditions.

## 9. Decision Rules

### 9.1 SURVIVES_POST_COMMIT
If ALL of:
1. Fix is present in committed HEAD (L112 sort key includes len(parameter_slots))
2. compete-equal resolves to param for ALL unseen ids 2-7 (6/6 param wins)
3. All 6 baselines pass (6/6)
4. B_CONFIDENCE_LITERAL_HIGHER resolves to literal (literal 0.98 wins)
5. No exceptions or crashes
6. No monkey-patching
7. C-EQUAL-UPSERT-ID7 resolves to param (fix works under upsert)

### 9.2 FALSIFIED-POST-COMMIT
If fix is present but ANY of:
1. compete-equal resolves to literal for any unseen id (hazard persists)
2. Any baseline regresses (fails to match expected outcome)
3. B_CONFIDENCE_LITERAL_HIGHER resolves to param (fix overrides confidence)
4. C-EQUAL-UPSERT-ID7 resolves to literal (fix fails under upsert)

### 9.3 BLOCKED
If fix is NOT present in committed HEAD (L112 sort key does not include len(parameter_slots))

### 9.4 MEASUREMENT_INVALID
If:
1. HTTP failures prevent measurement for any condition
2. Exceptions or crashes prevent resolution
3. Infrastructure issues (timeout, DNS, etc.)

## 10. Expected Outcomes

### 10.1 Positive Result (SURVIVES_POST_COMMIT)
- Core false-accept hazard eliminated in committed production code
- Parameter-slot-count tie-break works correctly for all tested unseen ids
- No baseline regressions
- Confidence ordering preserved
- Fix works under production-like upsert ordering
- C-PARAM-INHERIT advances to: real-web endpoint testing with DOM, auth, session state, drift (highest-upside generalization gap)
- Claim ceiling: narrow (single intent, single endpoint, preconditions={}, deterministic n=1, jsonplaceholder REST)

### 10.2 Negative Result (FALSIFIED-POST-COMMIT)
- Fix does not work as intended in committed code, or fails under upsert
- Root cause analysis required:
  - Is the sort key incorrect?
  - Does registry upsert sorting interact differently with tie-break than replace()?
  - Is there a code path that bypasses the sort?
- Product cannot advance to real-web testing
- Possible: different fix approach needed, or different tie-breaking mechanism

### 10.3 Blocked Result (BLOCKED)
- Fix not committed to production HEAD
- First gate from parent handoff not met
- Cannot test post-commit behavior
- Next action: commit fix with Director approval, then re-run this exact spec

### 10.4 Invalid Result (MEASUREMENT_INVALID)
- Infrastructure failure, not scientific result
- Retry after infrastructure repair

## 11. Analysis Plan

1. **Fix Verification**: Read src/spider/kernel.py L112, verify sort key includes len(parameter_slots). If absent → BLOCKED.
2. **Baseline Execution**: Run 6 baseline conditions, verify each matches expected outcome.
3. **Core Hazard Execution**: Run 6 core hazard conditions (ids 2-7), verify param wins for all.
4. **Null Control Execution**: Run B_CONFIDENCE_LITERAL_HIGHER, verify literal wins.
5. **Upsert Condition Execution**: Run C-EQUAL-UPSERT-ID7, verify param wins under upsert ordering.
6. **Metrics Computation**: Compute hazard_elimination_rate and baseline_pass_rate.
7. **Control Verification**: Check all controls pass/fail.
8. **Reporting**: Report all outcomes with equal prominence.

## 12. Analysis Code

Analysis will be implemented in Python using:
- `spider.kernel.SpiderKernel` for resolution
- `spider.registry.MechanismRegistry` for mechanism storage
- `spider.models.Mechanism`, `Observation`, `Resolution` for data structures
- `urllib.request` for HTTP execution against jsonplaceholder.typicode.com
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-GRAPH-34291967676/` before execution.

## 13. Pre-registered Expectations

From parent experiment and theoretical derivation:
- Fix adds len(parameter_slots) as secondary sort key
- Param mechanisms have parameter_slots >= 1 (e.g., ['id'])
- Literal mechanisms have parameter_slots = [] (empty)
- len([]) = 0 < len(['id']) = 1
- At equal confidence, param sorts higher than literal with the fix
- Without the fix, literal wins (insertion-order tie-break)
- Confidence ordering is primary: 0.98 > 0.95 regardless of parameter_slots
- Baseline behavior is independent of the fix (fix only affects tie-breaking at equal confidence)
- Upsert sorting by mechanism_id may reorder mechanisms but should not affect tie-break when fix is present

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
