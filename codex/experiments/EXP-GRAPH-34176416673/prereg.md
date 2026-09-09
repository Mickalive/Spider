# EXP-GRAPH-34176416673 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34176416673
- **Lane**: Graph
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-08
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-GRAPH-34170139507 (MEASUREMENT_INVALID)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does the parameter-slot-count fix survive commitment to production HEAD and re-validation without monkey-patching, and does param generalization hold across multiple unseen identifiers in committed HEAD?

## 3. Motivation

### What the parent experiment established (EXP-GRAPH-34170139507)

The parent experiment tested the core false-accept hazard under HTTP execution with a monkey-patched fix. It produced:

**Established (with monkey-patched fix):**
- Core hazard eliminated: compete-equal (literal 0.95 vs param 0.95, literal registered before param) resolves to param-fetch-posts for unseen id=7, HTTP 200, id=7
- Without fix, independent replay shows literal wins (false accept reproduced)
- All 6 baselines preserve under HTTP execution
- Param generalizes to unseen id=7 in isolation

**Rejected (measurement invalid):**
- Frozen decision rule HTTP-PARAM-INHERIT-SURVIVES unsatisfied: multi-slot condition requires HTTP 200 from /posts/1/tech which returns 404 (endpoint assumption error)
- Multi-slot control does not discriminate fix: order-dependent without fix
- Fix NOT committed to production HEAD: all measurements monkey-patched

**Unknown:**
- Whether fix survives commit to production HEAD
- Whether param generalization holds across multiple unseen ids (beyond single id=7)
- Whether fix generalizes to real-web endpoints with DOM, auth, session state, drift

**Do Not Assume:**
- Fix is committed to production (HEAD unfixed, sha256 46929b3a)
- Multi-slot dominance is validated under HTTP (HTTP 404, order-dependent)
- Core hazard validation applies beyond patch-only, single id=7, single endpoint
- Production-readiness (measurements monkey-patched)

### Why this experiment is different

The parent experiment used **monkey-patching** to apply the fix temporarily. All measurements were patch-only, not post-commit. This experiment tests whether the fix **survives commitment to production HEAD** and re-validates in committed code without monkey-patching.

**Key differences from parent:**
1. **No monkey-patching**: all measurements use committed HEAD code only
2. **Multiple unseen ids**: ids 2-7 (6 unseen ids, not just single id=7)
3. **Fix verification**: sha256 of kernel.py L112 confirms fix is committed
4. **Narrower scope**: no multi-slot testing (endpoint assumption error), no real-web testing (separate gate)

## 4. Hypotheses

### H1: Fix Survives Commitment
The parameter-slot-count fix (candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)) is committed to production HEAD src/spider/kernel.py L112.

### H2: Core Hazard Eliminated in Committed HEAD
In compete-equal conditions (literal 0.95 vs param 0.95, literal registered before param), param beats literal for ALL unseen ids 2-7 in committed HEAD without monkey-patching.

### H3: Baselines Preserve
All 6 baseline conditions pass with no regression in committed HEAD vs monkey-patched behavior.

### H4: Param Generalization Across Multiple Unseen Ids
Param generalizes to unseen ids 2-7 in committed HEAD (not just single id=7).

## 5. Data Generation

### 5.1 Fix Verification

Read src/spider/kernel.py L112 and verify:
- Line contains `candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)`
- sha256 of kernel.py matches expected post-commit hash

### 5.2 Test Conditions

For each unseen id in {2, 3, 4, 5, 6, 7}:
1. **compete-equal**: Register literal-fetch-posts-{id} (0 slots, confidence 0.95) and param-fetch-posts (1 slot, confidence 0.95). Literal registered before param. Resolve with params={id: <unseen_id>}.
2. **param-only-unseen**: Register param-fetch-posts only. Resolve with params={id: <unseen_id>}.

### 5.3 Baseline Conditions

Same as parent:
1. B_COLD: empty registry
2. B_LITERAL_ONLY_ORIG: literal-only, seen id=1
3. B_LITERAL_ONLY_UNSEEN: literal-only, unseen id=7
4. B_PARAM_ONLY_ORIG: param-only, seen id=1
5. B_PARAM_ONLY_UNSEEN: param-only, unseen id=7
6. B_CONFIDENCE_PARAM_HIGHER: param 0.98 vs literal 0.95, unseen id=7

### 5.4 Sample Size

- 6 unseen ids x 2 conditions = 12 test conditions
- 6 baseline conditions
- Total: 18 conditions
- Each condition is a deterministic point comparison (no sampling, no statistics)

## 6. Measures

### 6.1 Primary Metric
- **fix_committed**: boolean — is fix committed to production HEAD?
- **compete_equal_param_wins_all_ids**: boolean — does param win compete-equal for ALL unseen ids 2-7?
- **baselines_pass_all**: boolean — do all 6 baselines pass?

### 6.2 Secondary Metrics
- Per-id compete-equal result (mechanism_id, bound_url, http_status, http_response_id)
- Per-baseline result (status, mechanism_id, bound_url, http_status, http_response_id)
- Fix verification (line content, sha256)
- Network failure count
- Exception count

## 7. Null Models

### 7.1 Without-Fix Null
Independent replay of unfixed HEAD (sha256 46929b3a) shows literal wins in compete-equal. This verifies the hazard exists without the fix.

### 7.2 Endpoint Null
HTTP 200 confirms jsonplaceholder route exists. HTTP 404 indicates endpoint assumption error (not measured in this experiment — multi-slot excluded).

## 8. Statistical Tests

No statistical tests required. All conditions are deterministic point comparisons with no sampling, no RNG, no model calls. Results are exact.

## 9. Controls

### 9.1 Positive Control (C_COMPETE_EQUAL)
- compete-equal resolves to param for ALL unseen ids 2-7
- This verifies: fix works in committed HEAD, hazard eliminated

### 9.2 Null Control (C_COMPETE_EQUAL_HEAD)
- Without fix (unfixed HEAD), compete-equal resolves to literal (false accept)
- This verifies: hazard exists without fix (independent replay, not live measurement)

### 9.3 Baseline Preservation
- All 6 baselines pass with no regression
- This verifies: fix does not break existing behavior

## 10. Validity Threats

### 10.1 Endpoint Assumptions
jsonplaceholder.typicode.com must be reachable and /posts/{id} routes must exist for ids 1-7. Mitigation: verify HTTP 200 before recording result.

### 10.2 Registry Insertion Order
Literal registered before param in shared-equal conditions to test tie-break under fix. Mitigation: controlled explicitly in experiment code.

### 10.3 Single Endpoint
jsonplaceholder is simple REST, not complex Web with DOM/auth/session/drift. Mitigation: explicitly bounded claim ceiling; real-web testing is separate gate.

### 10.4 Fix Commitment Timing
Fix must be committed before experiment execution. Mitigation: experiment checks fix status and reports BLOCKED if not committed.

## 11. Decision Rules

### 11.1 SURVIVES_POST_COMMIT
If ALL of:
1. Fix committed: src/spider/kernel.py L112 matches expected fixed line
2. Core hazard eliminated: compete-equal resolves to param for ALL unseen ids 2-7
3. All 6 baselines pass
4. No network failures (all HTTP 200 for valid endpoints)
5. No exceptions

### 11.2 FALSIFIED_POST_COMMIT
If ANY of:
1. Fix not committed or reverted
2. Param loses to literal in compete-equal for any id
3. Any baseline regresses

### 11.3 MEASUREMENT_INVALID
If:
1. jsonplaceholder unreachable
2. Pipeline errors
3. Fix committed but sort key does not match expected

### 11.4 BLOCKED
If:
1. Fix not committed to production HEAD (prerequisite not met)

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_POST_COMMIT)
- Fix survives commitment to production HEAD
- Claim ceiling upgrades from monkey-patched to committed HEAD
- Product promotion unblocked for next gate (real-web testing)
- Param inheritance validated on committed code for multiple unseen ids

### 12.2 Negative Result (FALSIFIED_POST_COMMIT)
- Fix does not survive commitment or regresses in committed HEAD
- Product promotion blocked
- Root cause analysis required before retry

### 12.3 Blocked Result (BLOCKED)
- Fix not committed to production HEAD
- Experiment cannot proceed
- Prerequisite action required: commit fix to HEAD

## 13. Analysis Plan

1. **Fix Verification**: Read src/spider/kernel.py L112, verify line content and sha256
2. **If fix not committed**: Report BLOCKED with diagnostic
3. **If fix committed**: Execute all 18 conditions (12 test + 6 baseline)
4. **Record results**: Per-condition mechanism_id, bound_url, http_status, http_response_id
5. **Check decision rules**: Apply SURVIVES_POST_COMMIT / FALSIFIED_POST_COMMIT / MEASUREMENT_INVALID
6. **Report**: All outcomes with equal prominence

## 14. Analysis Code

Analysis will be implemented in Python using:
- `hashlib` for sha256 verification
- `json` for HTTP response parsing
- `urllib.request` for HTTP execution
- Standard library only (no external dependencies)

Code will be committed to `research/experiments/EXP-GRAPH-34176416673/` before execution.

## 15. Pre-registered Expectations

From parent experiment:
- With monkey-patched fix, compete-equal resolves to param for id=7
- Without fix, compete-equal resolves to literal (false accept)
- Expect same behavior in committed HEAD (fix should survive commitment)
- Expect generalization to multiple unseen ids (param template should work for any id)

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
