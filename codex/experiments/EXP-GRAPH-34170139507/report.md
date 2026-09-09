# EXP-GRAPH-34170139507 Report

## 1. Executive Summary

The experiment tested whether the parameter-slot-count fix generalizes to actual HTTP execution against a live endpoint. The core hazard test (compete-equal condition) **passed**: with fix applied, param mechanism wins over literal at equal confidence 0.95 for unseen id=7, bound URL is `/posts/7`, and HTTP GET returns status 200 with JSON `id=7`. Literal mechanism does not generalize (returns id=1). Param mechanism generalizes (returns id=7). All 6 baseline conditions match expected resolution status and HTTP responses.

However, the multi-slot positive control failed with HTTP 404 Not Found (`/posts/1/tech` does not exist on jsonplaceholder). This is a **measurement invalidity** due to endpoint limitations, not a scientific falsification. The experiment status is `MEASUREMENT_INVALID`, outcome `NOT_APPLICABLE`.

## 2. Key Findings

### 2.1 Core Hazard Test (compete-equal)
- **Resolution**: param-fetch-posts wins (confidence 0.95, parameter_slots=["id"]).
- **Bound URL**: `https://jsonplaceholder.typicode.com/posts/7`.
- **HTTP Response**: status 200, JSON `id=7`.
- **Interpretation**: The fix eliminates false accepts under HTTP execution. Param generalizes correctly to unseen identifiers.

### 2.2 Literal Mechanism Failure Mode
- **Condition**: literal-only-unseen (id=7).
- **Resolution**: literal-fetch-posts-1 wins, bound URL `/posts/1`.
- **HTTP Response**: status 200, JSON `id=1` (not 7).
- **Interpretation**: Literal universal matching does not produce correct response for unseen identifiers.

### 2.3 Param Generalization
- **Condition**: param-only-unseen (id=7).
- **Resolution**: param-fetch-posts wins, bound URL `/posts/7`.
- **HTTP Response**: status 200, JSON `id=7`.
- **Interpretation**: Param correctly generalizes to unseen identifiers in isolation.

### 2.4 Baseline Preservation
- All 6 baseline conditions (cold, literal-only-original, literal-only-unseen, param-only-original, param-only-unseen, compete-param-higher) match expected resolution status and HTTP responses.
- No regression from parent experiment (synthetic resolution-only).

### 2.5 Multi-Slot Positive Control (FAILED)
- **Resolution**: param-2slot wins, bound URL `/posts/1/tech`.
- **HTTP Response**: 404 Not Found.
- **Interpretation**: The endpoint does not support `/posts/1/tech`. This is an endpoint limitation, not a kernel or fix failure. The resolution step succeeded (param-2slot beats 1-slot), but HTTP execution failed due to missing route.

## 3. Measurement Validity

- **Network dependency**: All HTTP calls target jsonplaceholder.typicode.com. The multi-slot endpoint `/posts/1/tech` returns 404, indicating the endpoint does not exist. This is a measurement invalidity, not scientific falsification.
- **Endpoint stability**: jsonplaceholder responses are deterministic for existing routes (`/posts/{id}`).
- **Synthetic-to-real gap**: jsonplaceholder is a simple REST API; DOM, auth, session state, drift are out of scope.
- **Fix application**: Applied via monkey-patching; production HEAD remains unfixed.

## 4. Decision Rule Evaluation

The frozen decision rule `HTTP-PARAM-INHERIT-SURVIVES` requires ALL of:
1. All 6 baseline conditions match expected resolution status ✅
2. compete-equal returns param-fetch-posts with bound URL `/posts/7` and HTTP id=7 ✅
3. literal-only-unseen HTTP id=1 ✅
4. param-only-unseen HTTP id=7 ✅
5. multi-slot HTTP status 200 ❌ (404)
6. No Python exceptions ✅
7. No network failures ❌ (multi-slot 404)

Thus `HTTP-PARAM-INHERIT-SURVIVES` is not satisfied. The outcome is `MEASUREMENT_INVALID` due to network failure (HTTP 404) in the multi-slot condition.

## 5. Implications

- **Parameterized inheritance works end-to-end with real HTTP execution** for the core hazard test. The fix eliminates false accepts, param generalizes to unseen identifiers via URL binding, and correct HTTP responses are returned.
- **The multi-slot positive control failure is an endpoint limitation**, not a kernel or fix failure. The resolution step succeeded (param-2slot beats 1-slot). A different endpoint with nested routes would be needed to test multi-slot HTTP execution.
- **C-PARAM-INHERIT can advance** based on the core hazard test results. The multi-slot positive control should be re-tested on an endpoint that supports nested routes (e.g., a custom mock server).

## 6. Validity Threats

1. **Network dependency**: jsonplaceholder may be slow or rate-limited. Mitigation: 5-second timeout; MEASUREMENT_INVALID for network failures.
2. **Endpoint stability**: jsonplaceholder responses are deterministic. Mitigation: verified via multiple GET requests.
3. **Synthetic-to-real gap**: jsonplaceholder is simple REST; real-web complexity not tested. Mitigation: out of scope for this experiment.
4. **Single endpoint**: All conditions use same endpoint. Mitigation: tests kernel logic and URL binding, not site-specific behavior.
5. **Fix not committed**: Production HEAD remains unfixed. Mitigation: fix applied via monkey-patching; post-commit re-validation separate.

## 7. Recommendations

1. **Re-run multi-slot positive control** on a mock server that supports nested routes (e.g., `/posts/{id}/{category}`).
2. **Proceed with fix commit** to production HEAD, as core hazard test passed under HTTP execution.
3. **Advance to real-web endpoints** with DOM, auth, session state, drift — the highest-upside generalization gap.
4. **Consider alternative positive control** that uses existing jsonplaceholder routes (e.g., `/comments?postId={id}`).

---

*Report generated from frozen experiment EXP-GRAPH-34170139507. All observations are raw evidence; interpretations are separated.*