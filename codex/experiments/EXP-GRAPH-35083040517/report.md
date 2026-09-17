# EXP-GRAPH-35083040517 — Response-Time Profiling Experiment Report

## Executive Summary

**Decision: FALSIFIED-IN-SETTING**

Response-time profiling fails as a staleness signal for schema drift detection. The KS two-sample test on response-time distributions achieves TP=0.0 (no true drift patterns detected) with FP=0.1875 (nested_object_variation false alarms at 3 of 4 sizes). The experiment fails 3 of 5 frozen decision rule conditions: positive control fails, fewer than 2 of 3 true-drift patterns achieve TP>=0.8, and the Mann-Whitney separation test fails at all sizes.

This is a **valid scientific negative**: the calibration control passes (R²=0.9999), confirming the mock server produces computation-dependent timing. The failure is not due to infrastructure issues — the signal-to-noise ratio is fundamentally insufficient.

## Background

Prior C-FRESHNESS work has falsified two token-based staleness signals:

1. **Jaccard (field_path,type) similarity** (EXP-GRAPH-34788722106): FALSIFIED-IN-SETTING. FP=1.0 at all schema sizes.
2. **TF-IDF bag-of-words semantic similarity** (EXP-GRAPH-35010853847): FALSIFIED-IN-SETTING. FP=1.0 at all sizes, inverted separation direction.

Both failures share a common structure: any token change, whether drift or noise, reduces similarity proportionally. The representational dimension appears insufficient for drift-vs-noise discrimination.

Response-time profiling tests a fundamentally different hypothesis: that the **computation path** on the server differs between true drift (new field = new serialization/validation) and structural noise (optional field churn = same path). This is a temporal signal, orthogonal to both Jaccard and TF-IDF.

## Results

### Calibration Control (PASS)

The mock server produces near-perfect computation-dependent timing:

| Schema Size | Fresh-Copy Mean Response Time |
|-------------|-------------------------------|
| 10 fields   | 104.5 ms                      |
| 20 fields   | 196.9 ms                      |
| 30 fields   | 284.1 ms                      |
| 50 fields   | 462.9 ms                      |

R² = 0.9999. The server is NOT returning in constant time. Each field adds approximately 9.3ms of computation (2000 iterations of json.dumps + sha256 per field).

### Positive Control (FAIL)

add_field at n>=30 should produce a detectable response-time shift (KS D > 0.1, p < 0.05 after Bonferroni correction).

- **n=30**: KS D=0.40, p=0.016 (uncorrected) — **FAILS** Bonferroni correction (α=0.00208)
- **n=50**: KS D=0.30, p=0.135 — **FAILS**

The effect is real (mean difference +9ms to +13ms) but too small relative to jitter (0-50ms uniform) to reach statistical significance at n=30.

### Null Control (PASS)

fresh_copy (same schema, no modification) produces 0 false alarms across all 4 sizes. Natural jitter does not produce false drift signals.

### TP/FP Rates

| Metric | Value | 95% CI |
|--------|-------|--------|
| TP rate | 0.000 | [0.000, 0.243] |
| FP rate | 0.188 | [0.066, 0.430] |
| TP detections | 0/12 | — |
| FP detections | 3/16 | — |

All 3 false alarms come from **nested_object_variation** (a structural noise pattern), which adds 2 fields and produces a detectable timing shift at sizes 10, 20, and 50.

### Per-Pattern Results

**True drift patterns (should be detected):**

| Pattern | TP Rate | Detected At Sizes | Mean KS D |
|---------|---------|-------------------|-----------|
| add_field | 0.00 | none | 0.33 |
| remove_field | 0.00 | none | 0.30 |
| change_type | 0.00 | none | 0.25 |

**Structural noise patterns (should NOT be detected):**

| Pattern | FP Rate | False Alarm Sizes | Mean KS D |
|---------|---------|-------------------|-----------|
| optional_field_churn | 0.00 | none | 0.25 |
| null_valued_fields | 0.00 | none | 0.20 |
| nested_object_variation | 0.75 | 10, 20, 50 | 0.50 |

### Separation Direction (INVERTED)

The Mann-Whitney one-sided test (drift KS D > noise KS D) fails at all 4 sizes:

| Size | Mann-Whitney p | Direction |
|------|----------------|-----------|
| 10 | 0.350 | noise > drift |
| 20 | 0.650 | noise > drift |
| 30 | 0.329 | noise > drift |
| 50 | 0.900 | noise > drift |

At sizes 20 and 50, structural noise patterns produce LARGER KS D values than true drift patterns. This is the **same inverted-direction failure mode** observed in the Jaccard and TF-IDF experiments.

### Effect Sizes

Mean Cohen's d for before/after response-time difference:

| Pattern | Size 10 | Size 20 | Size 30 | Size 50 |
|---------|---------|---------|---------|---------|
| add_field | +0.35 | +0.28 | +0.84 | +0.60 |
| remove_field | -0.73 | -0.94 | -0.60 | -0.17 |
| change_type | +0.30 | -0.34 | -0.16 | +0.30 |
| optional_field_churn | +0.05 | -0.05 | +0.17 | +0.93 |
| null_valued_fields | +0.04 | +0.52 | +0.27 | -0.09 |
| nested_object_variation | +1.14 | +1.47 | +1.00 | +1.47 |
| fresh_copy | +0.47 | -0.08 | +0.00 | +0.31 |

The largest effect sizes are for nested_object_variation (Cohen's d 1.0-1.5), which is structural noise. True drift patterns show smaller, inconsistent effects.

## Interpretation

### Why Response-Time Profiling Fails

1. **Signal-to-noise ratio**: The computation-time difference for adding/removing 1 field (~9ms) is much smaller than the jitter range (0-50ms). At n=30 samples, the KS test lacks power to detect this small difference.

2. **Inverted direction**: nested_object_variation adds 2 fields, producing a larger timing shift than add_field (which adds 1 field). This structural noise pattern is MORE detectable than true drift, creating the inverted separation direction.

3. **Conservative correction**: Bonferroni correction (α=0.00208 for 24 comparisons) is very conservative. Even the largest KS D values (0.40-0.53) fail to reach this threshold.

4. **Fundamental limitation**: The hypothesis assumes structural noise uses the "same computation path" while true drift uses a "different computation path." In the mock server, ALL patterns change the schema structure, so ALL patterns change the computation time. The distinction between "same path" and "different path" does not cleanly map to the drift/noise classification.

### Comparison with Prior Experiments

| Experiment | Signal Type | TP | FP | Direction | Verdict |
|-----------|-------------|-----|-----|-----------|---------|
| Jaccard (34788722106) | Structural | 0.97 | 1.00 | Inverted | FALSIFIED |
| TF-IDF (35010853847) | Semantic | 0.97 | 1.00 | Inverted | FALSIFIED |
| Response-time (35083040517) | Temporal | 0.00 | 0.19 | Inverted | FALSIFIED |

Three orthogonal signal families tested. All three fail. The inverted direction is consistent across representational (Jaccard, TF-IDF) and temporal (response-time) signals.

## Decision Rule Evaluation

| Condition | Required | Observed | Pass/Fail |
|-----------|----------|----------|-----------|
| 1. Positive control | PASS | FAIL | FAIL |
| 2. Null control | PASS | PASS | PASS |
| 3. Drift patterns TP>=0.8 | >=2 of 3 | 0 of 3 | FAIL |
| 4. Separation (Mann-Whitney) | PASS | FAIL | FAIL |
| 5. Noise FP<=0.15 | >=1 of 3 | 2 of 3 | PASS |

**Decision: FALSIFIED-IN-SETTING** (3 of 5 conditions fail)

## Implications for C-FRESHNESS

Two orthogonal signal families have now failed:

1. **Representational signals** (Jaccard, TF-IDF): Fail because any token change reduces similarity proportionally, regardless of whether it is drift or noise.
2. **Temporal signals** (response-time profiling): Fail because the computation-time difference is too small relative to jitter, and structural noise (nested_object_variation) produces larger timing shifts than true drift.

The Graph lane's freshness frontier must shift to:

- **Multi-signal ensembles** combining orthogonal dimensions (structural + temporal + behavioral)
- **Direct schema comparison** (bypassing indirect signals entirely)
- **Schema-specific calibration** rather than universal thresholds
- **Larger sample sizes** (n>=100) with reduced jitter for temporal signals

C-FRESHNESS remains HYPOTHESIS. The problem may require fundamentally different approaches rather than refining indirect signals.

## Validity Threats

1. **Mock server realism**: The mock server uses CPU-bound computation (json.dumps + sha256). Real APIs may have larger timing variance from database, caching, or CDN effects. However, the controlled validation shows the method fails even under favorable conditions.

2. **Jitter magnitude**: The 0-50ms jitter range dominates the ~9ms per-field computation time. Real network jitter may be smaller (e.g., 1-5ms on localhost), which could improve detection. This is an open question.

3. **Sample size**: n=30 per condition is underpowered for the observed effect sizes. Power analysis suggests n>=100 would be needed to detect KS D=0.2 with 80% power.

4. **Pattern classification**: nested_object_variation adds 2 fields, making it structurally similar to add_field. The classification as "structural noise" may need refinement for real-world API drift detection.
