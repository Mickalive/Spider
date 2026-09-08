# EXP-GRAPH-34222171093 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34222171093
- **Lane**: Graph
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-08
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-GRAPH-34176416673 (BLOCKED)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

After committing the parameter-slot-count fix to production HEAD (candidates.sort key includes len(parameter_slots)): does the literal-vs-param equal-confidence competition resolve to param for all unseen ids 2-7 without monkey-patching, do all 6 baseline conditions pass, and does the corrected B_CONFIDENCE_LITERAL_HIGHER condition (literal 0.98 > param 0.95) remain literal-winning?

## 3. Motivation

### What the parent experiment established (EXP-GRAPH-34176416673)

The parent experiment was BLOCKED because the one-line fix to `src/spider/kernel.py` L112 was not committed to production HEAD.

**Established (under monkey-patched fix):**
- Core false-accept hazard elimination validated: compete-equal (literal 0.95 vs param 0.95, literal registered before param, unseen id=7) resolves to param-fetch-posts, bound URL /posts/7, HTTP 200, id=7
- Without fix: independent replay shows literal wins (/posts/1, id=1) — false accept reproduced
- All 6 baseline conditions preserve under HTTP execution on both monkey-patched and unfixed HEAD
- Param generalization to unseen id=7 confirmed; literal does NOT generalize
- Hazard is systematic across unseen ids: null control (compete-equal on unfixed HEAD) resolves to literal for ALL tested ids (id=7 from parent, ids 2-6 exploratory)

**Rejected:**
- Frozen decision rule HTTP-PARAM-INHERIT-SURVIVES: UNSUPPORTED (multi-slot endpoint 404)
- Multi-slot positive control: UNSUPPORTED (order-dependent without fix)
- This experiment advances C-PARAM-INHERIT beyond parent ceiling: UNSUPPORTED (fix not committed, BLOCKED)

**Unknown:**
- Whether the fix survives commit to production HEAD and re-validation without monkey-patching
- Whether B_CONFIDENCE_LITERAL_HIGHER remains literal-winning after fix commit
- Whether param generalization holds across multiple unseen ids (2-7) in committed HEAD
- Whether fix generalizes to real-web endpoints with DOM, auth, session, drift

**Do Not Assume:**
- The fix is committed to production — HEAD L112 is unfixed (sha256 46929b3a)
- C-PARAM-INHERIT SURVIVES_POST_COMMIT is tested — prerequisite not met
- baseline_pass 6/6 on unfixed HEAD indicates production-readiness
- The hazard being systematic across ids 2-7 without fix means the fix will work for all ids
- Core hazard validation extends beyond patch-only, single endpoint, single intent, preconditions={}, deterministic n=1

### Why this experiment is different

The parent experiment used **monkey-patching** to apply the fix at runtime. This experiment applies the fix by **committing it to production HEAD** and then testing against committed code without any runtime modification.

**Key differences:**
1. No monkey-patching: tests run against committed kernel code directly
2. Fix is permanent: committed to src/spider/kernel.py, not applied at runtime
3. Full unseen-id sweep: tests ids 2-7 (not just id=7)
4. Corrected null control: B-LITERAL-HIGHER-CONF (literal 0.98 > param 0.95) tests that confidence ordering is not broken
5. Verified fix presence: L112 inspected to confirm parameter_slots in sort key

## 4. Hypotheses

### H1: Hazard Elimination
On committed HEAD with the fix, compete-equal (literal 0.95 vs param 0.95, literal registered before param) resolves to param for ALL unseen ids in {2, 3, 4, 5, 6, 7}. Zero literal wins out of 6 tests.

### H2: Baseline Preservation
All 6 baseline conditions pass on committed HEAD with the fix, identical to their behavior on unfixed HEAD and monkey-patched HEAD.

### H3: Confidence Ordering Preserved
B-LITERAL-HIGHER-CONF (literal 0.98 vs param 0.95) resolves to literal for unseen id=7. The fix only affects tie-breaking at equal confidence, not strict confidence ordering.

### H4: Fix Presence
src/spider/kernel.py L112 contains a sort key that includes `len(m.parameter_slots)` or equivalent parameter-slot-count tie-breaking.

## 5. Pre-Commit Verification

Before any test execution, verify:

1. **Fix line inspection**: Read src/spider/kernel.py L112 and confirm the sort key includes parameter_slots
2. **Commit verification**: The commit hash or branch state is recorded
3. **No monkey-patching**: The test harness does not modify kernel.py at runtime

If the fix line is absent from committed HEAD, the experiment is BLOCKED (not a scientific result — an infrastructure prerequisite not met).

## 6. Conditions

### 6.1 Core Hazard Test (H1)

For each unseen id in {2, 3, 4, 5, 6, 7}:

- Register two mechanisms:
  - literal-fetch-posts: action_template="/posts/1", confidence=0.95, parameter_slots=[]
  - param-fetch-posts: action_template="/posts/{id}", confidence=0.95, parameter_slots=["id"]
- Register order: literal FIRST, param SECOND (worst case for param — insertion-order advantage to literal)
- Resolve with params={"id": <unseen_id>}
- Expected: param wins (ResolutionStatus.EXECUTABLE, bound_action="/posts/{id}" with id substituted)
- HTTP verification: GET bound_action -> HTTP 200, response JSON id == unseen_id

**Primary metric**: `hazard_elimination_rate` = number of unseen ids where param wins / 6
**Decision threshold**: hazard_elimination_rate == 1.0 (all 6 param wins)

### 6.2 Baseline Conditions (H2)

| Condition | Mechanisms Registered | Params | Expected Resolution | Expected HTTP |
|-----------|----------------------|--------|-------------------|--------------|
| B-COLD-UNKNOWN | None | {id:1} | UNKNOWN | N/A |
| B-LITERAL-ONLY-ORIG | literal-fetch-posts (id=1) | {id:1} | EXECUTABLE, /posts/1 | 200, id=1 |
| B-LITERAL-ONLY-UNSEEN | literal-fetch-posts (id=1) | {id:7} | EXECUTABLE, /posts/1 | 200, id=1 |
| B-PARAM-ONLY-ORIG | param-fetch-posts | {id:1} | EXECUTABLE, /posts/1 | 200, id=1 |
| B-PARAM-ONLY-UNSEEN | param-fetch-posts | {id:7} | EXECUTABLE, /posts/7 | 200, id=7 |
| B-COMPETE-PARAM-HIGHER | param (0.98) + literal (0.95) | {id:7} | EXECUTABLE, /posts/7 | 200, id=7 |

**Primary metric**: `baseline_pass_count` = number of baselines passing / 6
**Decision threshold**: baseline_pass_count == 1.0 (all 6 pass)

### 6.3 Null Control (H3)

- Register: literal (conf=0.98) + param (conf=0.95), literal FIRST
- Resolve with params={"id":7}
- Expected: literal wins (higher confidence, fix does not override)
- HTTP verification: GET /posts/1 -> 200, id=1

**Primary metric**: `null_control_pass` = literal wins at higher confidence
**Decision threshold**: null_control_pass == true

### 6.4 Fix Verification (H4)

- Read src/spider/kernel.py L112
- Confirm sort key includes `len(m.parameter_slots)` or equivalent
- Record exact line content and commit hash

**Primary metric**: `fix_present` = true/false
**Decision threshold**: fix_present == true

## 7. Execution Order

1. Verify fix is committed (H4) — if absent, BLOCK experiment
2. Run all 6 baseline conditions (H2) — establish no regression
3. Run null control (H3) — confirm confidence ordering preserved
4. Run core hazard test for ids 2-7 (H1) — primary scientific result
5. Record all observations, measurements, and HTTP responses

## 8. Controls Summary

| Control | Type | Expected | Fail Means |
|---------|------|----------|------------|
| B-COLD-UNKNOWN | baseline | UNKNOWN | Resolution logic broken |
| B-LITERAL-ONLY-* | baseline | literal resolves | Registration/resolution broken |
| B-PARAM-ONLY-* | baseline | param resolves | Parameter binding broken |
| B-COMPETE-PARAM-HIGHER | positive control | param wins (0.98>0.95) | Confidence ordering broken |
| B-LITERAL-HIGHER-CONF | null control | literal wins (0.98>0.95) | Fix overrides confidence |
| Core hazard (6 ids) | primary test | param wins all 6 | Hazard persists post-commit |

## 9. Validity Threats

### 9.1 Fix Not Committed
If src/spider/kernel.py L112 lacks the parameter_slots sort key, the experiment cannot proceed. **Mitigation**: pre-verify fix presence; BLOCK status if absent (not a scientific result).

### 9.2 Monkey-Patch Contamination
If the test harness accidentally monkey-patches kernel.py, results reflect patched behavior, not committed behavior. **Mitigation**: explicit no-monkey-patch verification in execution; inspect test code for runtime modifications.

### 9.3 HTTP Endpoint Unavailability
jsonplaceholder /posts/{id} may be unreachable. **Mitigation**: retry with backoff; if persistent, record as infrastructure failure (MEASUREMENT_INVALID), not negative result.

### 9.4 Insertion-Order Assumption
The test registers literal before param to create the worst case for param. If the registry sorting (production) interacts differently than replace() used here, results may differ. **Mitigation**: note this as a scope limitation; do not generalize to production registry sorting without explicit test.

### 9.5 Single Endpoint, Single Intent
Tests use jsonplaceholder /posts/{id} with fetch-post intent only. Generalization to other endpoints, intents, preconditions, and non-deterministic responses is not tested here. **Mitigation**: explicit claim ceiling bounds this experiment to the tested scope.

### 9.6 Deterministic n=1
Each condition is run once (deterministic). No statistical inference needed. **Mitigation**: all conditions are deterministic given frozen registry state; no sampling variability.

## 10. Decision Rules

### 10.1 SURVIVES_POST_COMMIT
If ALL of:
1. hazard_elimination_rate == 1.0 (param wins all 6 unseen ids)
2. baseline_pass_count == 1.0 (all 6 baselines pass)
3. null_control_pass == true (literal wins when confidence higher)
4. fix_present == true (L112 contains parameter_slots)
5. No unsubstituted templates in any param resolution
6. No infrastructure failures

### 10.2 FALSIFIES_POST_COMMIT
If ANY of:
1. hazard_elimination_rate < 1.0 (literal wins any unseen id)
2. baseline_pass_count < 1.0 (any baseline fails)
3. null_control_pass == false (param wins when confidence lower)
4. fix_present == false (fix line absent)

### 10.3 BLOCKED
If:
1. Fix cannot be committed (infrastructure, not scientific)
2. HTTP endpoints unreachable for all conditions (infrastructure)

### 10.4 MEASUREMENT_INVALID
If:
1. Test harness contains monkey-patching (contamination)
2. Registry state cannot be isolated between conditions

## 11. Expected Outcomes

### 11.1 SURVIVES_POST_COMMIT (Positive)
- Core false-accept hazard eliminated in committed HEAD
- C-PARAM-INHERIT advances: the parameter mechanism correctly wins tie-breaks for unseen identifiers
- Product can proceed to real-web generalization testing (highest-upside next gate)
- Claim ceiling: single endpoint (jsonplaceholder), single intent (fetch-post), preconditions={}, deterministic n=1, committed HEAD without monkey-patching

### 11.2 FALSIFIES_POST_COMMIT (Negative)
- Fix is insufficient: parameter_slots tie-breaking does not eliminate the hazard in committed code
- OR commit process altered behavior (regression)
- Product cannot proceed to real-web testing; fix requires revision
- Next action: diagnose whether the failure is in the sort key, the registry, or the commit

### 11.3 BLOCKED (Infrastructure)
- Fix cannot be committed or verified
- Not a scientific result; smallest next action: commit the fix with Director approval

## 12. Claim Ceiling

This experiment establishes (if SURVIVES_POST_COMMIT):

- **Scope**: jsonplaceholder API, /posts/{id} endpoint, fetch-post intent, preconditions={}, deterministic n=1
- **Mechanism**: parameter_slots count as tie-breaker at equal confidence
- **Limitation**: no real-web endpoints, no DOM, no auth, no session state, no drift, no LLM distillation, no multi-intent, no non-empty preconditions
- **Claim level**: PROOF OF CONCEPT in committed HEAD (narrow, single-endpoint)
- **Not established**: generalization, robustness, production-readiness, broad C-PARAM-INHERIT survival

## 13. Analysis Plan

1. **Pre-check**: Verify fix at L112; BLOCK if absent
2. **Baselines**: Run 6 baseline conditions; record pass/fail for each
3. **Null control**: Run B-LITERAL-HIGHER-CONF; verify literal wins
4. **Core hazard**: For each id in {2,3,4,5,6,7}: register mechanisms, resolve, HTTP verify
5. **Compile metrics**: hazard_elimination_rate, baseline_pass_count, null_control_pass, fix_present
6. **Apply decision rule**: SURVIVES_POST_COMMIT / FALSIFIES_POST_COMMIT / BLOCKED / MEASUREMENT_INVALID
7. **Report**: All outcomes with equal prominence; raw observations separate from interpretation

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any execution code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
