# EXP-GRAPH-34170139507 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34170139507
- **Lane**: Graph
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-07
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-GRAPH-33998605047 (PARTIAL_VALIDATION)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does the parameter-slot-count fix, applied temporarily during execution, generalize to actual HTTP execution against a live endpoint — specifically: does the parameterized mechanism resolve correctly, bind to the correct URL, execute a real HTTP GET, and return the expected response for both seen and unseen identifiers, while the literal mechanism fails to generalize?

## 3. Motivation

### What the parent experiment established (EXP-GRAPH-33998605047)

The parent experiment tested the parameter-slot-count fix on synthetic resolution-only conditions (no HTTP execution). It produced:

**Established:**
- Core false-accept hazard elimination: with fix applied, literal (0 parameter_slots) loses to param (1 parameter_slot) at equal confidence 0.95 for all tested ids 2..6 (5/5 param wins). Without fix, literal wins all 5.
- Multi-slot dominance confirmed: param-2slot [id,category] beats param-fetch-posts [id] at equal confidence 0.95, robust to registry order.
- Template-only params (parameter_slots=[] but template has ${id}) lose to declared 1-slot param.
- 6/7 valid baselines preserve (cold, literal-only orig/unseen, param-only orig/unseen, confidence param-higher).

**Rejected:**
- B_CONFIDENCE_LITERAL_HIGHER was correctly measured (misimplemented in experiment).
- Fix is committed to production HEAD (kernel.py L112 remains unfixed).
- Equal-slot ties are lexicographic (they are insertion-order dependent).
- FIX-VALIDATED decision not satisfied (B_CONFIDENCE_LITERAL_HIGHER misimplemented).

**Unknown:**
- Whether the fix generalizes to real-web endpoints with HTTP execution — synthetic substrate only.
- Whether the fix has been committed to production HEAD.
- Whether the fix generalizes to other slot counts, template shapes, or intents.

**Do Not Assume:**
- Fix is committed to production.
- baseline_pass is 7/7 (semantic 6/7).
- Equal-slot ties are lexicographic or deterministic.
- Fix generalizes beyond single tested multi-slot pair.
- verify() works end-to-end with real HTTP responses.

### Why this experiment is different

The parent experiment validated the fix entirely on synthetic resolution-only conditions: `resolve()` returns a `Resolution` object with `bound_action`, but no actual HTTP request is made. The fix sorts candidates by `(confidence, len(parameter_slots))` in `resolve()`, but the production code path includes `_bind()` which substitutes template parameters into the URL, and the actual HTTP execution is external to the kernel.

This experiment adds the execution layer: after `resolve()` returns a bound URL, the test script makes a real HTTP GET request to that URL and verifies the response. This tests:

1. **URL binding correctness**: Does `_bind()` correctly substitute `{id: 7}` into `/posts/${id}` to produce `/posts/7`?
2. **HTTP response correctness**: Does `/posts/7` actually return a post with `id=7`?
3. **Literal failure mode**: Does `/posts/1` (literal bound URL) return `id=1` when we requested `id=7`?
4. **End-to-end generalization**: Does the parameterized mechanism actually produce different outcomes for different identifiers when executed over HTTP?

These are not testable in resolution-only conditions because `_bind()` produces a string either way — the string `/posts/{id}` looks correct for both literal and param until you actually make the HTTP call.

## 4. Hypotheses

### H1: Parameterized mechanism wins in competition under HTTP execution
With fix applied, in the compete-equal condition (literal + param at confidence 0.95), param resolves as winning mechanism for unseen id=7, bound URL is `/posts/7`, and HTTP GET returns status 200 with JSON body containing `id=7`.

### H2: Literal mechanism does not generalize
In the literal-only-unseen condition, HTTP GET to the bound URL `/posts/1` returns JSON body containing `id=1` (not `id=7`). Literal universal matching does not produce the correct response for unseen identifiers.

### H3: Parameterized mechanism generalizes in isolation
In the param-only-unseen condition, HTTP GET to the bound URL `/posts/7` returns JSON body containing `id=7`. Param correctly generalizes to unseen identifiers.

### H4: No baseline regression
All baseline conditions (cold, literal-only-orig, literal-only-unseen, param-only-orig, param-only-unseen, confidence param-higher) match expected resolution status and HTTP response.

### H5: Multi-slot dominance survives HTTP execution
The 2-slot param beats 1-slot param at equal confidence, bound URL is `/posts/1/tech`, and HTTP GET returns status 200.

## 5. Data and Endpoint

### 5.1 Live HTTP Endpoint

All HTTP requests target `https://jsonplaceholder.typicode.com`, a free public REST API that returns deterministic JSON responses. Key endpoints:

- `GET /posts/{id}` → `{"userId": 1, "id": {id}, "title": "...", "body": "..."}`
- `GET /posts/1/tech` → returns a valid JSON response (status 200)

### 5.2 Mechanism Definitions

**Literal mechanism** (`literal-fetch-posts-1`):
- `parameter_slots = []`
- `action_template = {"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/1"}`
- `confidence = 0.95`
- Always binds to `/posts/1` regardless of params.

**Param mechanism** (`param-fetch-posts`):
- `parameter_slots = ["id"]`
- `action_template = {"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/${id}"}`
- `confidence = 0.95`
- Binds to `/posts/{id}` where `{id}` is substituted from params.

**Param-high** (`param-fetch-posts-high`):
- Same as param but `confidence = 0.98`.

**2-slot param** (`param-2slot`):
- `parameter_slots = ["id", "category"]`
- `action_template = {"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/${id}/${category}"}`
- `confidence = 0.95`

### 5.3 Identifier Selection

The experiment uses `id=7` as the primary unseen identifier (not used in parent experiments which tested ids 2..6). This provides an independent test of generalization.

## 6. Conditions

| # | Condition | Registry | Params | Expected Resolution | Expected URL | Expected HTTP id | Role |
|---|-----------|----------|--------|---------------------|--------------|------------------|------|
| 1 | cold | empty | {id:7} | UNKNOWN | — | — | baseline |
| 2 | literal-only-original | literal-only | {id:1} | EXECUTABLE | /posts/1 | 1 | baseline |
| 3 | literal-only-unseen | literal-only | {id:7} | EXECUTABLE | /posts/1 | 1 | baseline |
| 4 | param-only-original | param-only | {id:1} | EXECUTABLE | /posts/1 | 1 | baseline |
| 5 | param-only-unseen | param-only | {id:7} | EXECUTABLE | /posts/7 | 7 | baseline |
| 6 | compete-param-higher | shared-param-higher | {id:7} | EXECUTABLE | /posts/7 | 7 | baseline |
| 7 | compete-equal | shared-equal | {id:7} | EXECUTABLE | /posts/7 | 7 | intervention |
| 8 | multi-slot-beats-1-slot | 2slot-vs-1slot | {id:1,category:tech} | EXECUTABLE | /posts/1/tech | — | positive_control |

## 7. Controls

### 7.1 Positive Control (multi-slot)
2-slot param beats 1-slot param at equal confidence under HTTP execution. Verifies fix sorts by slot count and URL binding handles multiple template parameters.

### 7.2 Null Control (compete-equal)
Literal + param at equal confidence 0.95: param must win. This is the original hazard. Before fix, literal won (false accept); after fix, param must win. Verified both by resolution mechanism and by HTTP response (id=7 not id=1).

### 7.3 Baseline Preservation
All 6 baseline conditions match expected outcomes. No regression from parent experiment (which used the same baseline definitions).

### 7.4 HTTP Execution Validity
Each HTTP call must return status 200 with valid JSON. If jsonplaceholder is unreachable, that condition is MEASUREMENT_INVALID.

## 8. Fix Application

The fix is applied via monkey-patching during execution:

```python
original_resolve = SpiderKernel.resolve
def patched_resolve(self, intent, context, params=None):
    # Temporarily patch candidates.sort
    # ... apply fix ...
    return original_resolve(self, intent, context, params)
```

Same approach as parent EXP-GRAPH-33998605047. Production HEAD `src/spider/kernel.py` L112 remains unfixed. The fix is not committed in this experiment.

## 9. Measurement Procedure

For each condition:
1. Create fresh `SpiderKernel` with fresh `MechanismRegistry` (temp JSONL file).
2. Register mechanisms per condition specification.
3. Call `resolve(intent="fetch-post", context={}, params=condition.params)`.
4. Record resolution status, mechanism_id, bound_action, confidence.
5. If status == EXECUTABLE, extract URL from bound_action.
6. Make HTTP GET request to the URL with 5-second timeout.
7. Parse JSON response. Record HTTP status code and response id field.
8. Compare response id to expected_http_id.

## 10. Decision Rules

### 10.1 HTTP-PARAM-INHERIT-SURVIVES
If ALL of:
1. All 6 baseline conditions match expected resolution status
2. compete-equal: param wins, bound URL = `/posts/7`, HTTP status 200, response id = 7
3. literal-only-unseen: HTTP response id = 1 (literal does not generalize)
4. param-only-unseen: HTTP response id = 7 (param generalizes)
5. multi-slot: HTTP status 200
6. No Python exceptions

### 10.2 HTTP-PARAM-INHERIT-FALSIFIED
If ANY of:
1. compete-equal: literal wins (false accept under HTTP)
2. compete-equal: bound URL != `/posts/7`
3. compete-equal: HTTP response id != 7
4. Any baseline regresses from parent results

### 10.3 MEASUREMENT_INVALID
If:
1. Network unavailable (HTTP timeout or connection error) for any non-cold condition
2. Python exception during resolve or HTTP execution
3. jsonplaceholder returns non-JSON response

## 11. Validity Threats

### 11.1 Network Dependency
 jsonplaceholder.typicode.com is a free public service. It may be slow, rate-limited, or temporarily unavailable. **Mitigation**: 5-second timeout per request; MEASUREMENT_INVALID status for network failures (not scientific falsification).

### 11.2 Endpoint Stability
 jsonplaceholder responses are deterministic and do not change. `/posts/7` always returns `id=7`. **Mitigation**: verified by running multiple GET requests in baseline conditions.

### 11.3 Synthetic-to-Real Gap
 jsonplaceholder is a simple REST API, not a complex Web application with DOM, auth, session state, or drift. **Mitigation**: this experiment tests the *execution path* (resolve → bind → HTTP → response), not full browser interaction. DOM/auth/session/drift are out of scope for this experiment and remain the next generalization gate.

### 11.4 Single Endpoint
 All conditions use the same endpoint. **Mitigation**: the experiment tests kernel logic and URL binding, not site-specific behavior. The endpoint is a vehicle for HTTP execution, not the object of study.

### 11.5 Fix Not Committed
 Production HEAD remains unfixed. **Mitigation**: the fix is applied via monkey-patching (same as parent). The experiment tests fix behavior, not production HEAD behavior. Post-commit re-validation is a separate experiment.

## 12. Expected Outcomes

### 12.1 Positive Result (HTTP-PARAM-INHERIT-SURVIVES)
- Parameterized inheritance works end-to-end with real HTTP execution
- The fix eliminates false accepts in the execution path
- Param mechanisms generalize to unseen identifiers via URL binding
- C-PARAM-INHERIT advances: next gate is real-web with DOM, auth, session, drift
- Product can trust param mechanisms to generalize correctly over HTTP

### 12.2 Negative Result (HTTP-PARAM-INHERIT-FALSIFIED)
- The fix works in resolution-only but fails in the execution path
- A critical bug exists in _bind() or HTTP response handling
- C-PARAM-INHERIT is blocked: param mechanisms cannot be trusted for real-web use
- Alternative approaches must be explored

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Network issues prevent HTTP execution
- Not scientific evidence for or against
- Retry when network is available

## 13. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 14. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
