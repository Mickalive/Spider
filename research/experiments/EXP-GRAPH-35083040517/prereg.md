# EXP-GRAPH-35083040517 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-35083040517
- **Lane**: Graph
- **Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)
- **Parent**: EXP-GRAPH-35010853847 (TF-IDF semantic similarity — FALSIFIED-IN-SETTING)
- **Date**: 2026-09-16
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can response-time profiling (measuring endpoint response-time distribution shifts before/after schema modification) distinguish true schema drift from structural noise with TP>=0.8 and FP<=0.15?

## 3. Motivation

Prior C-FRESHNESS work has falsified two token-based staleness signals:

1. **Jaccard (field_path,type) similarity** (EXP-GRAPH-34788722106): FALSIFIED-IN-SETTING. FP=1.0 at all schema sizes. Structural noise produces lower Jaccard than true drift (inverted direction).

2. **TF-IDF bag-of-words semantic similarity** (EXP-GRAPH-35010853847): FALSIFIED-IN-SETTING. FP=1.0 at all sizes. Inverted separation: structural noise more divergent than drift (Cohen's d 1.2–1.9 wrong direction, Mann-Whitney p=1.0).

Both failures share a common structure: **any token change, whether drift or noise, reduces similarity proportionally.** The representational dimension itself appears insufficient for drift-vs-noise discrimination because it cannot distinguish "meaningful" from "meaningless" token changes.

Response-time profiling tests a fundamentally different hypothesis: that the **computation path** on the server differs between true drift (new field = new serialization/validation) and structural noise (optional field churn = same path, optional branches). This is a temporal signal, not a representational one, and is therefore orthogonal to both Jaccard and TF-IDF.

If response-time profiling also fails, the Graph lane will have tested two orthogonal signal families (representational + temporal) and both failed. This would strongly suggest the drift-vs-noise discrimination problem requires either:
- Multi-signal ensembles combining multiple orthogonal dimensions
- Direct schema comparison (bypassing indirect signals entirely)
- Schema-specific calibration rather than universal thresholds

## 4. Hypotheses

### H1: Response-Time Discrimination
KS two-sample test on response-time distributions can distinguish true drift from structural noise with TP>=0.8 and FP<=0.15 at n>=30 fields.

### H2: Positive Control
add_field pattern at n>=30: response-time distribution shifts are detectable (KS D > 0.1, p < 0.05). This verifies the mock server produces real computation-dependent timing variation.

### H3: Null Control
Fresh copies (same schema, no modification): KS test does not detect a shift (FP <= 0.15). This verifies natural jitter does not produce false signals.

### H4: Directional Consistency
True drift patterns (add_field, remove_field, change_type) produce LARGER response-time shifts than structural noise patterns (optional_field_churn, null_valued_fields, nested_object_variation) at matched schema sizes.

### H5: Noise Irrelevance
Structural noise patterns produce response-time distributions indistinguishable from fresh copies (KS p > 0.05), because the computation path is unchanged.

## 5. Data Generation

### 5.1 Mock Server Design

A Python `http.server` serves JSON responses with controlled computation paths:

- **Field-count-proportional serialization**: Each field requires an explicit `json.dumps()` call, making response time proportional to field count.
- **Controlled jitter**: Uniform 0-50ms artificial jitter per request to simulate network noise.
- **Drift injection**: After DRIFT_POINT requests, the server switches to a modified schema.
- **Schema size control**: The number of fields is controlled by generating field dictionaries of size n.

### 5.2 Schema Modification Patterns

**True drift patterns** (should change response time):
1. `add_field`: Add a new field to the response (increases serialization time)
2. `remove_field`: Remove a field from the response (decreases serialization time)
3. `change_type`: Change a field type from integer to string (may change serialization time)

**Structural noise patterns** (should NOT change response time meaningfully):
4. `optional_field_churn`: Randomly add/remove optional nullable fields (same computation path)
5. `null_valued_fields`: Replace field values with null (same serialization path)
6. `nested_object_variation`: Add/remove nested object fields (increases complexity but same base path)

**Null control**:
7. `fresh_copy`: Same schema, no modification (baseline timing)

### 5.3 Schema Sizes

Four conditions: n = 10, 20, 30, 50 fields.

### 5.4 Sample Size

- 30 requests per condition (before drift, after drift) x 6 patterns x 4 sizes = 1440 total requests per before/after pair
- 30 fresh-copy control requests per size = 120 total control requests
- Total: ~1560 client requests, each with controlled jitter

### 5.5 Seeds

- `seed=20260916` for field generation and jitter injection
- `seed=20260917` for pattern variation (which optional fields to churn)
- Both frozen before execution

## 6. Measures

### 6.1 Primary Metric: KS Two-Sample Test
- For each pattern at each size: compute KS two-sample test between before-drift and after-drift response-time distributions
- D statistic and p-value
- Detection: p < 0.05 (after Bonferroni correction across 4 sizes x 6 patterns = 24 comparisons)

### 6.2 TP/FP Rates
- **TP**: KS test detects a shift for true drift patterns (add_field, remove_field, change_type)
- **FP**: KS test detects a shift for structural noise patterns (optional_field_churn, null_valued_fields, nested_object_variation) and fresh copies
- Wilson 95% confidence intervals

### 6.3 Separation Direction
- Mann-Whitney U test: is response-time variance larger for true drift than structural noise?
- One-sided test: drift > noise, p < 0.05

### 6.4 Effect Size
- KS D statistic (0 = identical distributions, 1 = completely separated)
- Cohen's d for mean response-time difference

### 6.5 Response Time Calibration
- Verify that response time is proportional to field count (regression R² > 0.7)
- Verify jitter distribution matches specification (uniform 0-50ms)

## 7. Null Models

### 7.1 Fresh-Copy Null
Same schema, no modification. KS test should not detect a shift. FP <= 0.15.

### 7.2 Shuffle Null
Permute before/after labels. KS test should produce uniform p-values (no systematic detection).

### 7.3 Random Classifier
50% detection rate. Expected to fail TP >= 0.8 and FP <= 0.15.

## 8. Statistical Tests

### 8.1 Primary: KS Two-Sample Test
- For each pattern x size: KS D statistic and p-value
- Bonferroni correction: alpha = 0.05 / 24 = 0.00208
- One-sided test for direction consistency

### 8.2 Secondary: Mann-Whitney U Test
- Compare response-time distributions: true drift patterns vs structural noise patterns
- One-sided alternative: drift variance > noise variance

### 8.3 Calibration Check
- Linear regression: response_time ~ field_count
- R² > 0.7 confirms computation-dependent timing

### 8.4 Effect Size
- Cohen's d for before/after response-time difference at each pattern x size

## 9. Controls

### 9.1 Positive Control (add_field, n>=30)
- KS D > 0.1, p < 0.05 (after correction)
- Verifies: mock server produces real timing variation when schema changes

### 9.2 Null Control (fresh_copy, all sizes)
- KS p > 0.05 (no detection), FP <= 0.15
- Verifies: jitter alone does not produce false signals

### 9.3 Separation Control (Mann-Whitney)
- One-sided p < 0.05: drift response-time shifts > noise response-time shifts
- Verifies: the signal is directional, not random

### 9.4 Calibration Control
- Response time proportional to field count (R² > 0.7)
- Verifies: the mock server is not returning in constant time

## 10. Validity Threats

### 10.1 Mock Server Realism
The mock server is artificial. Real APIs may have response times dominated by network, database, or CDN effects rather than schema computation. Mitigation: this is a controlled validation experiment. If the pipeline cannot detect known timing structure in a controlled environment, it cannot be trusted on real servers.

### 10.2 Computation-Dependent Timing Assumption
The hypothesis assumes response time depends on schema computation. If the server returns in constant time (e.g., caching, pre-computed responses), the signal is zero by construction. Mitigation: calibration control (R² > 0.7) will detect this.

### 10.3 Jitter Masking
Artificial jitter 0-50ms may mask real signal if the computation-time difference is smaller than the jitter. Mitigation: computation time is expected to scale linearly with field count, and at n=50 fields the serialization difference should exceed jitter range.

### 10.4 Client-Side Measurement
Response times are measured client-side (HTTP round-trip), not server-side. Client-side includes network overhead. Mitigation: localhost testing eliminates network variability; jitter is the dominant noise source.

### 10.5 Multiple Comparisons
24 primary comparisons (4 sizes x 6 patterns). Bonferroni correction is conservative. Mitigation: report both corrected and uncorrected p-values; focus on effect sizes.

### 10.6 Sample Size
30 requests per condition may be insufficient for stable distribution estimation. Power analysis: KS test with n=30 per group has ~80% power to detect D=0.4 (medium effect). Smaller effects may be missed.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Positive control passes (add_field TP >= 0.8 at n>=30)
2. Null control passes (fresh_copy FP <= 0.15)
3. At least 2 of 3 true-drift patterns achieve TP >= 0.8 at n>=30
4. Mann-Whitney one-sided p < 0.05 (drift > noise)
5. At least 1 structural noise pattern achieves FP <= 0.15 at n>=30

### 11.2 FALSIFIED-IN-SETTING
If ANY of (1)-(5) fails.

### 11.3 MEASUREMENT_INVALID
If:
1. Calibration control fails (R² < 0.7, server returns in constant time)
2. Pipeline errors prevent computation
3. Jitter injection fails to produce measurable variance

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Response-time profiling is a viable orthogonal staleness signal
- Opens multi-signal ensemble opportunity (temporal + representational)
- Product could deploy response-time monitoring as a lightweight freshness probe
- C-FRESHNESS advances from HYPOTHESIS toward EXPERIMENTAL

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Response-time profiling fails as a staleness signal
- Two orthogonal signal families (representational + temporal) both fail
- Graph lane must shift to multi-signal ensembles or direct schema comparison
- C-FRESHNESS remains HYPOTHESIS
- Strong constraint on future freshness research direction

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Mock server does not produce computation-dependent timing
- Pipeline needs redesign before this question can be answered
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Server Setup**: Launch mock server with controlled computation paths and jitter
2. **Data Collection**: For each pattern x size, collect 30 before-drift and 30 after-drift response times
3. **Calibration Check**: Verify response time ~ field_count regression R² > 0.7
4. **KS Tests**: Compute KS two-sample test for each pattern x size
5. **TP/FP Rates**: Classify detections using Bonferroni-corrected alpha
6. **Separation Test**: Mann-Whitney U test for drift vs noise direction
7. **Controls**: Verify positive, null, separation, and calibration controls
8. **Reporting**: Report all outcomes with equal prominence

## 14. Analysis Code

Analysis will be implemented in Python using:
- `http.server` for mock server
- `urllib.request` for client-side HTTP
- `scipy.stats` for KS test and Mann-Whitney U
- `numpy` for array operations
- `time.perf_counter()` for response-time measurement
- Standard library only (no custom timing libraries)

Code will be committed to `research/graph/freshness_detection/` before execution.

## 15. Pre-registered Expectations

From the hypothesis:
- add_field and remove_field should produce the largest response-time shifts (schema computation changes)
- change_type may produce smaller shifts (same field count, different serialization)
- optional_field_churn should produce negligible shifts (same computation path)
- null_valued_fields and nested_object_variation should produce small shifts (minor serialization changes)
- Fresh copies should produce no systematic shift

From the mock server design:
- Response time should be proportional to field count (R² > 0.7)
- Jitter should add 0-50ms uniform noise without masking the signal
- At n=50 fields, the serialization difference should be measurable

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
