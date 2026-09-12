# EXP-GRAPH-34711403174 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34711403174
- **Lane**: Graph
- **Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)
- **Date**: 2026-09-12
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-GRAPH-34586318405 (MIXED - C-SEMANTIC-RESOLVE tested)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does comparing cached mechanism postconditions against live endpoint responses provide reliable staleness detection across resource families with different drift patterns?

## 3. Motivation

### What the parent experiment established (EXP-GRAPH-34586318405)

The parent experiment tested C-SEMANTIC-RESOLVE (semantic aliasing resolution). It established:
- Kernel uses exact intent matching (no URL template analysis)
- HTTP status-code grounding is falsified on tolerant APIs (0/12 status differences)
- Body-based grounding is exploratory and non-autonomous

The parent handoff recommended moving to C-FRESHNESS because:
- It is materially orthogonal to semantic resolution (different product capability)
- It is a priority graph-lane claim
- It is testable with current infrastructure (compare cached mechanism metadata against live endpoint responses)

### Why this experiment is different

This experiment tests a different capability: detecting when cached mechanism knowledge has become stale due to endpoint drift. This is product-critical for knowing when inherited knowledge needs re-validation.

The experiment uses a controlled mock server to simulate endpoint drift across resource families, enabling measurement of true-positive and false-positive rates of staleness detection.

## 4. Hypotheses

### H1: Detection Reliability
A simple postcondition-similarity freshness score can detect endpoint drift with >80% true-positive rate and <5% false-positive rate across resource families.

### H2: Positive Control
Drift that changes response structure (add field) should be detected with 100% true-positive rate when threshold is 0.85.

### H3: Null Control
Stable endpoint should produce 0% false-positive rate.

### H4: Drift Pattern Sensitivity
Different drift patterns (add field, change type, remove field) are detectable with similar reliability (true-positive rate >70% for each pattern).

## 5. Experimental Design

### 5.1 Mock Server

A Python HTTP server that serves three resource families:
- `/users/{id}`: Returns JSON with fields `id`, `name`, `email`
- `/posts/{id}`: Returns JSON with fields `id`, `title`, `body`, `userId`
- `/comments/{id}`: Returns JSON with fields `id`, `postId`, `author`, `text`

The server supports a drift injection mechanism: after N requests to a resource, the response structure changes.

### 5.2 Resource Families and Drift Patterns

| Family | Endpoint | Drift Pattern | Drift Point | Ground Truth |
|--------|----------|---------------|-------------|--------------|
| Users | /users/{id} | Add field: `phone` added at request 6 | request 6-10 | stale |
| Posts | /posts/{id} | Change type: `id` changes from integer to string at request 6 | request 6-10 | stale |
| Comments | /comments/{id} | Remove field: `author` removed at request 6 | request 6-10 | stale |
| Control | /users/{id} (stable) | No drift | none | fresh |

### 5.3 Cached Mechanisms

For each resource family, create a cached mechanism with:
- `intent`: "get_{resource}"
- `postconditions`: Expected response fields as set of (field_path, type) pairs
- `confidence`: 0.9
- `freshness`: Empty (not used in this experiment)

### 5.4 Freshness Detection Algorithm

For each request:
1. Send request to mock server, receive response
2. Extract actual response fields as set of (field_path, type) pairs
3. Compute Jaccard similarity between cached postconditions and actual fields
4. If similarity < threshold (0.85), flag as stale

### 5.5 Threshold

Threshold fixed at 0.85 before execution. This is a design parameter, not a result.

## 6. Measures

### 6.1 Primary Metrics
- **true_positive_rate**: Fraction of drift requests correctly flagged as stale (across all drift families)
- **false_positive_rate**: Fraction of fresh requests incorrectly flagged as stale (on stable control)

### 6.2 Secondary Metrics
- Per-family true-positive rate
- Per-drift-pattern true-positive rate
- Similarity scores distribution for fresh vs stale requests
- Confusion matrix (TP, FP, TN, FN)

### 6.3 Baseline Comparisons
- No freshness detection: TP=0%, FP=0%
- Random detection (50%): TP~50%, FP~50%

## 7. Controls

### 7.1 Positive Control (drift at request 6)
- Drift adds a new field to /users/{id} response
- Expected: similarity drops below 0.85, detection rate 100%

### 7.2 Null Control (stable endpoint)
- /users/{id} (stable version) returns same structure for all 10 requests
- Expected: similarity always 1.0, false-positive rate 0%

### 7.3 Drift Pattern Controls
- Three distinct drift patterns test generalizability
- Each pattern should be detectable (TP >70%)

## 8. Statistical Tests

### 8.1 Primary Test
- Compute true-positive rate and false-positive rate across all resource families
- Apply decision rule: TP >= 0.8 AND FP <= 0.1

### 8.2 Per-Family Tests
- Compute TP per family, require >70% for each (H4)

### 8.3 Confidence Intervals
- Wilson score interval for proportions (TP and FP)
- Report 95% CI alongside point estimates

## 9. Validity Threats

### 9.1 Mock Server Fidelity
Mock server may not reflect real Web drift patterns. **Mitigation**: This is a controlled validation experiment. If freshness detection cannot detect known drift in mock server, it cannot be trusted on real endpoints.

### 9.2 Threshold Sensitivity
Threshold 0.85 is arbitrary. **Mitigation**: Report sensitivity analysis across thresholds 0.7, 0.8, 0.85, 0.9, 0.95 in secondary analysis.

### 9.3 Drift Pattern Diversity
Only three drift patterns tested. **Mitigation**: Patterns cover add/remove/change-type, which are common drift modes. Additional patterns can be tested in future experiments.

### 9.4 Sample Size
10 requests per family, 3 drift families + 1 control = 40 requests total. Limited power for rare events. **Mitigation**: Drift is deterministic (injected at request 6), not random, so sample size is adequate for detection measurement.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST
If ALL of:
1. True-positive rate >= 0.8 across all drift families
2. False-positive rate <= 0.1 on stable control
3. Per-family TP > 0.7 for each drift pattern
4. No mock server failures

### 10.2 FALSIFIED-IN-SETTING
If ANY of:
1. True-positive rate < 0.8 across all drift families
2. False-positive rate > 0.1 on stable control
3. Per-family TP <= 0.7 for any drift pattern

### 10.3 MEASUREMENT_INVALID
If:
1. Mock server fails to start or respond
2. Drift injection fails (no drift occurs at request 6)
3. Request/response logging fails

## 11. Expected Outcomes

### 11.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates freshness scoring can detect endpoint drift
- Validates C-FRESHNESS claim at proof-of-concept level
- Product lane can integrate freshness scoring into kernel to trigger re-validation
- Graph lane can use freshness scoring to prioritize re-validation of cached mechanisms

### 11.2 Negative Result (FALSIFIED-IN-SETTING)
- Simple postcondition similarity is not reliable for staleness detection
- Need alternative staleness signals (session token validation, DOM structure checks, etc.)
- Does NOT falsify C-FRESHNESS entirely - only this specific detection method

### 11.3 Invalid Result (MEASUREMENT_INVALID)
- Mock server infrastructure needs debugging
- Not scientific evidence for or against

## 12. Analysis Plan

1. **Mock Server Setup**: Implement Python HTTP server with drift injection
2. **Mechanism Caching**: Create cached mechanisms for each resource family
3. **Request Execution**: Send 10 requests per family, log responses
4. **Freshness Scoring**: Compute Jaccard similarity for each request
5. **Detection Decision**: Apply threshold 0.85, flag stale if similarity < 0.85
6. **Metric Computation**: TP rate, FP rate, per-family rates
7. **Statistical Tests**: Wilson score CIs, decision rule evaluation
8. **Sensitivity Analysis**: Report TP/FP across thresholds 0.7, 0.8, 0.85, 0.9, 0.95
9. **Reporting**: Report all outcomes with equal prominence

## 13. Analysis Code

Analysis will be implemented in Python using:
- `http.server` or `Flask` for mock server
- `requests` for HTTP client
- `json` for response parsing
- `numpy` for similarity computation
- Standard library only

Code will be committed to `research/graph/freshness_detection/` before execution.

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.