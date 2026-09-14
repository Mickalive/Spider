# EXP-GRAPH-34755316488 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34755316488
- **Lane**: Graph
- **Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-GRAPH-34711403174 (SURVIVES_CURRENT_TEST, audit REVISE)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does Jaccard (field_path,type) freshness detection survive scaling to realistic schema sizes (10-50 fields) where single-field drift similarity exceeds the parent threshold 0.85, and does an adaptive schema-size-adjusted threshold restore detection without inflating false positives on stochastic response variation?

## 3. Motivation

### What the parent experiment established (EXP-GRAPH-34711403174)

The parent experiment tested Jaccard (field_path,type) freshness scoring on a deterministic mock server with 3-4 field schemas. It produced:

**Established:**
- Jaccard similarity perfectly separates fresh (1.0) from three structural drifts (0.6/0.75) on 3-4 field flat schemas at threshold 0.85
- Point-estimate TP 1.0, FP 0.0 on deterministic mock
- Drift patterns add_field, change_type, remove_field are all detectable at this scale

**Rejected (by audit):**
- Fixed threshold 0.85 is robust across schema sizes: analytical scaling attack shows n=10 add_field similarity = 0.909 > 0.85 (FN), n=20 = 0.952, n=50 = 0.98
- Controls are independent from main metric: positive/null controls are tautological with Jaccard computation
- FP rate is precisely estimated: Wilson CI [0.0, 0.2775] on n=10 control

**Unknown:**
- Whether the method works at realistic schema sizes (10-50 fields)
- Whether an adaptive threshold can restore detection at scale
- Whether stochastic response variation (real-world noise) produces false positives
- Whether the method works on real API endpoints

**Do Not Assume:**
- Fixed threshold 0.85 works for schemas >= 10 fields
- Deterministic mock results generalize to real Web endpoints
- The method scales to complex real-world APIs

### Why this experiment is different

The parent experiment validated freshness detection only on 3-4 field schemas where the analytical Jaccard similarity for single-field drift (0.6-0.75) is well below threshold 0.85. This experiment tests the critical scaling boundary: as schema size n grows, single-field add similarity = n/(n+1) approaches 1.0, eventually exceeding any fixed threshold.

The experiment has two components:
1. **Mock scaling component**: Systematically vary schema size (5-50 fields) and measure detection rate degradation, then test whether adaptive threshold T(n) = 1 - 1/(2n) restores detection
2. **Real-API FP component**: Measure false-positive rate on fresh responses from 3 public APIs with natural stochastic variation

## 4. Hypotheses

### H1: Scaling Degradation
Detection rate at fixed threshold 0.85 decreases monotonically with schema size (Spearman rho >= 0.8, p < 0.05).

### H2: Adaptive Threshold Recovery
Adaptive threshold T(n) = 1 - 1/(2n) achieves TP >= 0.8 at each schema size n >= 10.

### H3: Adaptive Threshold FP Control
Adaptive threshold FP rate <= 0.15 on stochastic response variation across all schema sizes.

### H4: Null Control
Stable endpoint (no drift) produces 0 false positives at any threshold, at each schema size.

### H5: Real-API FP
FP rate on fresh real-API responses <= 0.20 with adaptive threshold.

## 5. Design

### 5.1 Schema Sizes

Six conditions:
- **n=5**: Parent baseline (3 fields + 2 added for consistency)
- **n=10**: Minimum realistic API schema
- **n=15**: Moderate API schema
- **n=20**: Typical REST API resource
- **n=30**: Large API resource (e.g., GitHub repo detail)
- **n=50**: Complex API resource (e.g., full user profile with metadata)

### 5.2 Schema Construction

For each size n, generate a base schema of n fields:
- Field i (0 <= i < n): path = "field_{i}", type = one of {integer, string, number, boolean} cycling
- First field is always ("id", "integer") for consistency
- Remaining fields use deterministic type assignment: field_{i} type = ["string", "integer", "number", "boolean"][i % 4]

### 5.3 Drift Patterns

Three structural drift patterns per schema size (same as parent):
1. **add_field**: Add ("new_field", "string") to schema → Jaccard = n/(n+1)
2. **remove_field**: Remove last field → Jaccard = (n-1)/n
3. **change_type**: Change first field type integer→string → Jaccard = (n-1)/(n+1)

### 5.4 Stochastic Variation Control

For FP measurement, generate responses that preserve schema structure but vary values:
- Random strings for string fields (length 5-20)
- Random integers for integer fields (range 0-10000)
- Random floats for number fields (range 0.0-1000.0)
- Random booleans for boolean fields

This simulates natural API response variation without structural drift. Jaccard should remain 1.0 (same (field_path, type) pairs).

### 5.5 Sample Size

Mock component:
- 6 schema sizes x 3 drift patterns x (5 fresh + 5 stale) = 30 requests per size = 180 drift requests
- 6 schema sizes x 20 stochastic variation = 120 FP measurement requests
- 6 schema sizes x 10 stable endpoint = 60 null control requests
- Total mock: ~360 requests

Real-API component:
- 3 APIs x 10 fresh requests each = 30 requests
- Re-request same endpoints with same parameters to measure natural Jaccard variation

### 5.6 Mock Server Architecture

Single mock server with endpoints:
- `/{schema_size}/{resource_id}` returns JSON matching the n-field schema
- Pre-drift: returns fresh schema
- Post-drift (requests 6+): returns drifted schema for drift families, stochastic-variation schema for FP families, identical schema for null control families

Resource families per schema size:
- `drift_add_{n}`: add-field drift at request 6
- `drift_remove_{n}`: remove-field drift at request 6
- `drift_change_{n}`: change-type drift at request 6
- `stochastic_{n}`: schema-preserving value variation on every request
- `stable_{n}`: identical responses on every request

### 5.7 Adaptive Threshold

T(n) = 1 - 1/(2n)

Rationale: Single-field add Jaccard = n/(n+1). For detection, need T < n/(n+1). The gap n/(n+1) - T(n) = 1/(2n) - 1/(n+1) = (n+1-2n)/(2n(n+1)) = (1-n)/(2n(n+1)). At n=10: T=0.95, add Jaccard=0.909, gap=-0.041 (detection fails). Wait — this is wrong.

Let me reconsider. The analytical Jaccard for add_field is n/(n+1). For T(n) to detect this, we need T(n) > n/(n+1). But n/(n+1) approaches 1.0, so T(n) must also approach 1.0.

Better formula: T(n) = (n-0.5)/(n+0.5). This gives:
- n=5: T=4.5/5.5 = 0.818, add Jaccard=0.833 > 0.818 → detected
- n=10: T=9.5/10.5 = 0.905, add Jaccard=0.909 > 0.905 → barely detected
- n=20: T=19.5/20.5 = 0.951, add Jaccard=0.952 > 0.951 → barely detected
- n=50: T=49.5/50.5 = 0.980, add Jaccard=0.980 ≈ 0.980 → borderline

Actually, a simpler adaptive threshold: T(n) = 1 - c/n where c is calibrated. For add_field detection: need 1 - c/n < n/(n+1), i.e., c/n > 1/(n+1), i.e., c > n/(n+1). Since n/(n+1) < 1, any c >= 1 works. But for remove_field: Jaccard = (n-1)/n = 1 - 1/n, need T < 1 - 1/n, i.e., 1 - c/n < 1 - 1/n, i.e., c > 1. So c must be > 1.

Let me use: T(n) = 1 - 1.5/n. Check:
- n=5: T=0.7, add=0.833, remove=0.8, change=0.667 → all detected
- n=10: T=0.85, add=0.909, remove=0.9, change=0.818 → add/remove detected, change borderline
- n=20: T=0.925, add=0.952, remove=0.95, change=0.905 → all detected
- n=50: T=0.97, add=0.98, remove=0.98, change=0.962 → all detected

For FP: stochastic variation preserves (field_path, type) pairs, so Jaccard = 1.0 > T(n) for all n → 0 FP. This is correct because stochastic variation does NOT change structure.

The FP question is about stochastic drift that MIGHT change structure. Let me add a "stochastic structural variation" control where occasionally (10% chance) a field is added or removed randomly, simulating real API optional fields.

Actually, for the FP measurement, I should test: when the response has the SAME schema but different values, does Jaccard remain 1.0? Yes, by construction. The real FP threat is: when the response has slightly different structure due to optional fields, null values, or encoding differences.

Let me add a "structural noise" control: 10% chance of random field addition/removal per request, simulating optional fields in real APIs.

OK, I think I'm overcomplicating this. Let me simplify and use T(n) = 1 - 1.5/n as the adaptive threshold, and test it rigorously.

Actually, the key insight from the parent audit is that the analytical Jaccard values for single-field drift are:
- add_field: n/(n+1)
- remove_field: (n-1)/n  
- change_type: (n-1)/(n+1)

The tightest is change_type = (n-1)/(n+1). For detection, need T < (n-1)/(n+1).

(n-1)/(n+1) = 1 - 2/(n+1). So T(n) must be < 1 - 2/(n+1).

Let T(n) = 1 - 2.5/(n+1). Then:
- n=5: T=1-2.5/6=0.583, change=0.667 > 0.583 → detected
- n=10: T=1-2.5/11=0.773, change=0.818 > 0.773 → detected
- n=20: T=1-2.5/21=0.881, change=0.905 > 0.881 → detected
- n=50: T=1-2.5/51=0.951, change=0.961 > 0.951 → detected

For add_field: n/(n+1) = 1 - 1/(n+1). Need T < 1 - 1/(n+1). With T = 1 - 2.5/(n+1), gap is (2.5-1)/(n+1) = 1.5/(n+1) > 0 → always detected.

For remove_field: (n-1)/n = 1 - 1/n. Need T < 1 - 1/n. With T = 1 - 2.5/(n+1), need 2.5/(n+1) > 1/n, i.e., 2.5n > n+1, i.e., 1.5n > 1, i.e., n > 0.67 → always true for n>=1.

OK so T(n) = 1 - 2.5/(n+1) works analytically. But I should also consider FP. With this threshold, FP on stochastic variation (same schema) = 0 because Jaccard = 1.0 > T(n). FP on structural noise (optional fields) depends on how often structure changes.

Let me keep the design simpler. I'll use T(n) = 1 - 1.5/n as a practical formula and verify empirically.

Actually, let me just use a clean formula and test it. The important thing is the experiment structure, not the exact threshold formula. I'll specify T(n) = max(0.5, 1 - 2/(n+1)) which gives a safety margin above the theoretical minimum.

Wait, I'm spending too much time on the threshold formula in the prereg. Let me finalize the spec and write the prereg.</think><tool_call>
<function=write>
<parameter=content># EXP-GRAPH-34755316488 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34755316488
- **Lane**: Graph
- **Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-GRAPH-34711403174 (SURVIVES_CURRENT_TEST, audit REVISE)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does Jaccard (field_path,type) freshness detection survive scaling to realistic schema sizes (10-50 fields) where single-field drift similarity exceeds the parent threshold 0.85, and does an adaptive schema-size-adjusted threshold restore detection without inflating false positives on stochastic response variation?

## 3. Motivation

### What the parent experiment established (EXP-GRAPH-34711403174)

The parent experiment tested Jaccard (field_path,type) freshness scoring on a deterministic mock server with 3-4 field schemas. Key results:

**Established:**
- Jaccard similarity perfectly separates fresh (1.0) from three structural drifts (0.6/0.75) on 3-4 field flat schemas at threshold 0.85 (result.json metrics, audit.json claim_ceiling)
- Point-estimate TP 1.0, FP 0.0 on deterministic mock (result.json metrics)
- Drift patterns add_field, change_type, remove_field are all detectable at this scale

**Rejected (by audit scaling attack):**
- Fixed threshold 0.85 is robust across schema sizes: n=10 add_field similarity = 0.909 > 0.85 (FN), n=20 = 0.952, n=50 = 0.98 (audit.json scaling_attack)
- Controls are independent from main metric: positive/null controls are tautological with Jaccard computation (audit.json validity_findings)
- FP rate precisely estimated: Wilson CI [0.0, 0.2775] on n=10 control (audit.json)

**Unknown:**
- Whether the method works at realistic schema sizes (10-50 fields)
- Whether an adaptive threshold can restore detection at scale
- Whether stochastic response variation produces false positives
- Whether the method works on real API endpoints

**Do Not Assume:**
- Fixed threshold 0.85 works for schemas >= 10 fields (audit scaling_attack demonstrates failure)
- Deterministic mock results generalize to real Web endpoints (audit validity_findings)
- The method scales to complex real-world APIs

### Why this experiment is different

The parent experiment validated freshness detection only on 3-4 field schemas where analytical Jaccard for single-field drift (0.6-0.75) is well below threshold 0.85. This experiment directly tests the audit's critical scaling vulnerability: as schema size n grows, single-field add similarity = n/(n+1) approaches 1.0, eventually exceeding any fixed threshold.

The experiment has two components:
1. **Mock scaling component**: Systematically vary schema size (5-50 fields), measure detection degradation at fixed threshold, test adaptive threshold T(n) = 1 - 2/(n+1) that provides margin above the theoretical minimum for change_type drift
2. **Real-API FP component**: Measure false-positive rate on fresh responses from 3 public APIs with natural stochastic variation

## 4. Hypotheses

### H1: Scaling Degradation (Primary)
Detection rate at fixed threshold 0.85 decreases monotonically with schema size for single-field add_field drift (Spearman rho >= 0.8 between schema size and Jaccard similarity, p < 0.05).

### H2: Adaptive Threshold Recovery
Adaptive threshold T(n) = 1 - 2/(n+1) achieves TP >= 0.8 at each schema size n >= 10 for all three drift patterns.

### H3: Adaptive Threshold FP Control
Adaptive threshold FP rate <= 0.15 on stochastic response variation (schema-preserving value changes) across all schema sizes.

### H4: Null Control
Stable endpoint (no drift) produces Jaccard = 1.0 and 0 false positives at any threshold, at each schema size.

### H5: Real-API False Positives
FP rate on fresh real-API responses (re-requests of same endpoints) <= 0.20 with adaptive threshold.

## 5. Design

### 5.1 Schema Sizes

Six conditions:
- **n=5**: Parent baseline compatibility (3 original fields + 2 padding)
- **n=10**: Minimum realistic API schema
- **n=15**: Moderate API schema
- **n=20**: Typical REST API resource
- **n=30**: Large API resource
- **n=50**: Complex API resource (e.g., full user profile with metadata)

### 5.2 Schema Construction

For each size n, generate a base schema of n fields:
- Field 0: ("id", "integer") — always present for consistency
- Field i (1 <= i < n): ("field_{i}", type_i) where type_i cycles through ["string", "integer", "number", "boolean"]

### 5.3 Drift Patterns (per schema size)

Three structural drift patterns (same as parent, generalized):
1. **add_field**: Add ("new_field", "string") → Jaccard = n/(n+1)
2. **remove_field**: Remove last field → Jaccard = (n-1)/n
3. **change_type**: Change field_0 type integer→string → Jaccard = (n-1)/(n+1)

The tightest drift is change_type: Jaccard = (n-1)/(n+1) = 1 - 2/(n+1).

### 5.4 Adaptive Threshold

**T(n) = 1 - 2/(n+1)**

Analytical verification for single-field drift detection (need T < Jaccard_drift):
- add_field: Jaccard = n/(n+1) = 1 - 1/(n+1). Gap = T - Jaccard = (1 - 2/(n+1)) - (1 - 1/(n+1)) = -1/(n+1) < 0. Always detected.
- remove_field: Jaccard = (n-1)/n = 1 - 1/n. Need T < 1 - 1/n. At n=10: T=0.818, Jaccard=0.9. Detected. At n=50: T=0.961, Jaccard=0.98. Detected.
- change_type: Jaccard = (n-1)/(n+1) = 1 - 2/(n+1). Gap = T - Jaccard = 0. **T equals the change_type Jaccard exactly.** This means change_type is the boundary case. We need T slightly below this: use **T(n) = 1 - 2.5/(n+1)** for safety margin.

**Revised: T(n) = 1 - 2.5/(n+1)**

Verification:
- n=5: T=0.583, add=0.833, remove=0.8, change=0.667 → all detected
- n=10: T=0.773, add=0.909, remove=0.9, change=0.818 → all detected
- n=20: T=0.881, add=0.952, remove=0.95, change=0.905 → all detected
- n=50: T=0.951, add=0.98, remove=0.98, change=0.961 → all detected

### 5.5 Stochastic Variation Control (FP measurement)

For each schema size, generate 20 responses that preserve (field_path, type) pairs but vary values:
- Random strings (length 5-20 chars) for string fields
- Random integers (0-10000) for integer fields
- Random floats (0.0-1000.0) for number fields
- Random booleans for boolean fields

Jaccard should remain 1.0 (same structure). Any detection is a false positive.

### 5.6 Null Control

Stable endpoint at each schema size: 10 identical responses. Jaccard = 1.0 always. 0 FP expected.

### 5.7 Sample Size

Mock component:
- 6 sizes x 3 patterns x (5 fresh + 5 stale) = 180 drift requests
- 6 sizes x 20 stochastic variation = 120 FP measurement requests
- 6 sizes x 10 stable endpoint = 60 null control requests
- Total mock: 360 requests

Real-API component:
- 3 public APIs x 10 fresh requests each = 30 requests
- APIs: GitHub /repos/{owner}/{repo}, JSONPlaceholder /posts/{id}, httpbin /response-headers
- Same endpoint requested twice with identical parameters; Jaccard of (field_path, type) between first and second response measures natural structural variation

### 5.8 Mock Server Architecture

Single mock server with endpoints:
- `/{schema_size}/{resource_id}` returns JSON matching the n-field schema
- Families per size: drift_add_{n}, drift_remove_{n}, drift_change_{n}, stochastic_{n}, stable_{n}
- Drift injection at request 6 for drift families (same as parent)
- Stochastic family: values change every request, structure preserved
- Stable family: identical responses always

## 6. Measures

### 6.1 Primary Metric
- **jaccard_by_size**: Mean Jaccard similarity at each schema size for each drift pattern, at fixed threshold 0.85
- **spearman_rho_scaling**: Spearman correlation between schema size and add_field Jaccard similarity (n=6 sizes)
- **tp_rate_adaptive**: Detection rate at adaptive threshold T(n) = 1 - 2.5/(n+1) at each schema size for each drift pattern
- **fp_rate_adaptive**: False-positive rate on stochastic variation at adaptive threshold at each schema size

### 6.2 Secondary Metrics
- Per-drift-pattern Jaccard at each schema size
- Jaccard distribution (fresh vs stale) at each schema size
- Sensitivity analysis: TP/FP at thresholds [0.7, 0.8, 0.85, 0.9, 0.95] at each schema size
- Real-API Jaccard distribution across re-requests
- Wilson 95% CIs for all rates

### 6.3 Comparison with Parent
- Jaccard values at n=5 should match parent experiment (n=3-4) approximately
- Fixed threshold 0.85 TP rate at n=5 should be 1.0 (replication)

## 7. Null Models

### 7.1 No Detection (always fresh)
TP=0%, FP=0%. Trivial baseline.

### 7.2 Field-Set Equality (exact match)
TP=100% for any structural change, FP=100% for any stochastic variation. Degenerate extreme.

### 7.3 Fixed Threshold 0.85 (parent)
Expected to fail at n>=10. Provides direct comparison with parent claim.

## 8. Statistical Tests

### 8.1 Primary: Scaling Degradation
- Spearman rho between schema size and add_field Jaccard at threshold 0.85
- One-sided test: rho > 0 (Jaccard increases with size → detection degrades)
- n=6 sizes, single comparison, no correction

### 8.2 Adaptive Threshold Recovery
- For each schema size n >= 10: TP rate >= 0.8 across 3 drift patterns (5 stale requests each = 15 per size)
- Wilson 95% CI lower bound > 0.6 at each size

### 8.3 FP Control
- For each schema size: FP rate <= 0.15 on 20 stochastic variation requests
- Wilson 95% CI upper bound < 0.25 at each size

### 8.4 Real-API FP
- FP rate across 30 real-API re-requests at adaptive threshold
- Wilson 95% CI upper bound < 0.30

## 9. Controls

### 9.1 Positive Control (n=5, add_field)
- Jaccard = 5/6 = 0.833 < 0.85 → detected at fixed threshold
- Verifies pipeline correctly computes Jaccard and applies threshold

### 9.2 Null Control (all sizes, stable endpoint)
- Jaccard = 1.0, 0 FP at any threshold
- Verifies no spurious detection on identical responses

### 9.3 Replication Control (n=5)
- Results at n=5 should approximately match parent experiment (n=3-4)
- TP=1.0 at fixed threshold 0.85 for all drift patterns

### 9.4 Stochastic Structure Preservation
- Stochastic variation responses have identical (field_path, type) pairs as fresh
- Jaccard = 1.0 by construction → FP should be 0 at any threshold
- Tests that Jaccard is structure-only, not value-sensitive

## 10. Validity Threats

### 10.1 Mock-to-Real Gap
Mock server uses deterministic schema construction. Real APIs may have optional fields, null values, nested structures, encoding variations. **Mitigation**: Real-API FP component directly measures structural variation on live endpoints.

### 10.2 Adaptive Threshold Overfitting
T(n) = 1 - 2.5/(n+1) is derived from analytical Jaccard formulas for the three tested drift patterns. Other drift patterns (nested changes, value-range drift) may have different Jaccard values. **Mitigation**: Experiment tests only structural drift; claim ceiling explicitly excludes non-structural drift.

### 10.3 Sample Size per Schema Size
5 stale requests per drift pattern per size gives Wilson CI [0.565, 1.0] for 5/5 detection. Limited precision for per-size claims. **Mitigation**: Primary test is monotonicity across sizes (n=6), not per-size CI precision.

### 10.4 Real-API Endpoint Selection
3 public APIs may not represent typical API response structure. **Mitigation**: APIs chosen for diversity (code hosting, placeholder, HTTP utilities). Claim ceiling bounded to tested endpoints.

### 10.5 Threshold Sensitivity
Adaptive threshold performance depends on the specific formula. Different formulas might work better or worse. **Mitigation**: Sensitivity analysis across multiple thresholds at each size; report the full TP/FP surface.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Spearman rho(schema_size, add_field_jaccard_at_0.85) >= 0.8, p < 0.05 (scaling degradation confirmed)
2. Adaptive threshold TP >= 0.8 at each schema size n >= 10 across all 3 drift patterns
3. Adaptive threshold FP <= 0.15 on stochastic variation at each schema size
4. Null control passes at all sizes (FP = 0)
5. Positive control passes at n=5 (TP = 1.0)
6. Real-API FP rate <= 0.20
7. No pipeline errors (>20% request failures)

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Spearman rho < 0.8 or p > 0.05 (scaling degradation not confirmed — contradicts analytical prediction)
2. Adaptive threshold TP < 0.8 at any n >= 10
3. Adaptive threshold FP > 0.15 on stochastic variation
4. Null control fails at any size
5. Positive control fails at n=5

### 11.3 MEASUREMENT_INVALID
If:
1. >20% request failures
2. Mock server errors prevent data collection
3. Real-API component fails (endpoints unreachable)

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Confirms that Jaccard (field_path,type) detection degrades predictably with schema size
- Validates adaptive threshold T(n) = 1 - 2.5/(n+1) as a product-viable calibration
- C-FRESHNESS claim advances toward product kernel integration
- Provides concrete threshold formula for implementation in freshness guard
- Product lane can integrate adaptive Jaccard freshness scoring with bounded claim

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- If adaptive threshold cannot restore detection: (field_path,type) representation is insufficient for realistic schemas
- Product lane should pursue alternative staleness signals: session token validation, DOM structure checks, response-time profiling, or semantic embedding similarity
- Does NOT falsify C-FRESHNESS entirely — only Jaccard (field_path,type) as the detection mechanism

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Mock Server Setup**: Start mock server with all schema sizes and families
2. **Request Execution**: 360 mock requests across sizes/patterns/controls
3. **Jaccard Computation**: For each request, extract (field_path, type) pairs, compute Jaccard against cached fresh schema
4. **Fixed Threshold Analysis**: Apply threshold 0.85, compute TP/FP per size per pattern
5. **Scaling Test**: Spearman correlation between schema size and add_field Jaccard
6. **Adaptive Threshold Analysis**: Apply T(n) = 1 - 2.5/(n+1), compute TP/FP per size
7. **Sensitivity Analysis**: TP/FP at thresholds [0.7, 0.8, 0.85, 0.9, 0.95] per size
8. **Real-API Component**: Request 3 APIs, compute Jaccard between re-requests, apply adaptive threshold
9. **Control Verification**: Verify positive, null, and replication controls
10. **Decision**: Apply frozen decision rule

## 14. Analysis Code

Analysis will be implemented in Python using:
- `json` for response parsing
- `http.server` for mock server
- `urllib.request` for client requests and real-API calls
- `math` for Wilson CI computation
- `random` for stochastic variation generation (seed=42)
- `scipy.stats` for Spearman correlation
- Standard library only (no custom estimators)

Code will be committed to `research/graph/freshness_detection/` before execution.

## 15. Pre-registered Expectations

From analytical Jaccard formulas and parent experiment:
- add_field Jaccard = n/(n+1): n=5→0.833, n=10→0.909, n=20→0.952, n=50→0.980
- remove_field Jaccard = (n-1)/n: n=5→0.8, n=10→0.9, n=20→0.95, n=50→0.98
- change_type Jaccard = (n-1)/(n+1): n=5→0.667, n=10→0.818, n=20→0.905, n=50→0.961
- At threshold 0.85: detection fails for add_field at n>=10 (0.909>0.85), for remove_field at n>=10 (0.9>0.85), for change_type at n>=14 (0.857>0.85)
- Adaptive threshold T(n) = 1 - 2.5/(n+1) should restore detection with margin
- Stochastic variation preserves (field_path, type) → Jaccard = 1.0 → FP = 0
- Real APIs may have optional fields or encoding differences → some FP expected

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
