# EXP-GRAPH-35137034388 Preregistration

## Experiment Identity

- **Experiment ID**: EXP-GRAPH-35137034388
- **Lane**: graph
- **Claim**: C-FRESHNESS
- **Parent**: EXP-GRAPH-35130682058 (Linear Fisher LDA ensemble — FALSIFIED-IN-SETTING)

## Motivation

Four orthogonal signal families have been tested and falsified for drift-vs-noise discrimination:

1. **Jaccard structural similarity** (field_path,type) — FP=1.0 at all sizes (EXP-GRAPH-34788722106)
2. **TF-IDF bag-of-words semantic similarity** — TP=0.972, FP=1.0, inverted direction (EXP-GRAPH-35010853847)
3. **Response-time KS two-sample test** — TP=0.0, FP=0.1875, inverted direction (EXP-GRAPH-35083040517)
4. **Linear Fisher LDA ensemble** of (1-Jaccard) and KS D — AUC=0.625, all conditions fail (EXP-GRAPH-35130682058)

All share a common root cause: **magnitude confound** where structural noise patterns (nested_object_variation adding 2 fields, null_valued_fields adding 2 fields) produce larger divergence than true drift patterns (add_field adding 1 field). The confound is in the signal itself, not the classifier.

The parent handoff recommends testing **fundamentally different signal families** — specifically session token validation or field-usage profiling — that measure a dimension orthogonal to structural/temporal similarity.

This experiment tests **field-usage profiling**: tracking which fields different client profiles actually access across response samples, and computing usage-similarity between fresh and stale states.

## Core Insight

Jaccard measures **structural presence** (are fields in the schema?). Field-usage profiling measures **functional access** (are fields used by clients?). These diverge for noise: noise adds fields that no client uses (Jaccard drops, usage unchanged). They converge for drift: drift removes fields that clients depend on (both drop). This creates a separable region in (Jaccard, usage-similarity) space.

## Hypothesis

**H1**: Structural noise patterns reduce Jaccard but NOT usage-similarity (usage-similarity >= 0.95 under noise).

**H2**: True drift patterns reduce BOTH Jaccard and usage-similarity (usage-similarity < 0.90 under drift).

**H3**: Usage-similarity provides information beyond Jaccard (Pearson r < 0.90 across conditions).

## Falsifier

The experiment is FALSIFIED if:

- (F1) No operating point achieves noise usage-similarity >= 0.95 AND drift usage-similarity < 0.90, OR
- (F2) Usage-similarity gap between noise and drift is < 0.05 (insufficient discrimination), OR
- (F3) Pearson r between Jaccard and usage-similarity > 0.95 (redundant signal).

## Experimental Design

### Mock API Server

A local HTTP server serves JSON responses for 4 resource families: `users`, `posts`, `comments`, `items`. Each response contains a fixed set of fields determined by the current schema state (fresh, drifted, or noisy).

The server is **deterministic**: given a (resource, schema_state, resource_id) triple, it returns the same response every time. No timing jitter, no network variation.

### Client Profiles

Three client profiles access different field subsets, simulating real-world heterogeneous API usage:

| Profile | Fields Used | Use Case |
|---------|------------|----------|
| A (light) | id, name | Identity-only consumer |
| B (medium) | id, name, email | Contact consumer |
| C (heavy) | id, name, email, phone | Full-profile consumer |

Each client makes 10 requests per condition, requesting only its designated fields.

### Schema Sizes

4 sizes matching prior experiments: 10, 20, 30, 50 fields. Baseline schemas are generated deterministically with the frozen seed.

### Drift Patterns (True Drift)

| Pattern | Description | Expected Usage Impact |
|---------|-------------|----------------------|
| remove_field | Remove one required field | Client profiles depending on that field fail |
| change_type | Change one field's type (integer→string) | Client profiles expecting old type get type mismatch |
| required_to_optional | Move one required field to optional | Some clients stop receiving the field |

### Noise Patterns (Structural Noise)

| Pattern | Description | Expected Usage Impact |
|---------|-------------|----------------------|
| optional_field_churn | Add ~10% optional fields | No impact — clients don't request optional fields |
| null_valued_fields | Add fields with null values | No impact — clients don't request null fields |
| nested_object_variation | Add nested sub-fields | No impact — clients don't request nested fields |

### Sample Sizes

- **N = 30** fresh samples per condition per schema size
- **N = 30** stale samples per condition per schema size
- **Total**: 4 sizes × 6 patterns × 30 samples × 2 (fresh/stale) = 1440 samples
- **API calls**: 1440 samples × 3 clients × 10 requests = 43,200 local calls

### Controls

| Control | Expected Behavior |
|---------|-------------------|
| Fresh copies (identical schemas) | usage-similarity = 1.0, Jaccard = 1.0 |
| Noise at size 10 | usage-similarity >= 0.95, Jaccard < 1.0 |
| Drift at size 10 | usage-similarity < 0.90, Jaccard < 1.0 |
| Stable resource (users_stable) | usage-similarity = 1.0 across all conditions |

## Metrics

### Primary Metrics

1. **usage_similarity**: Mean per-profile Jaccard(field_used_fresh, field_used_stale) across 3 client profiles. Measures whether client access patterns change.

2. **jaccard_similarity**: Standard Jaccard(field_path, type) between fresh and stale schema field sets. Structural baseline from prior experiments.

3. **per_profile_success_rate**: Fraction of successful requests per client profile per condition. Captures behavioral impact.

### Derived Metrics

4. **usage_jaccard_gap**: jaccard_similarity - usage_similarity per condition. Noise expected to have small gap (usage high, Jaccard low); drift expected to have small or negative gap (both low).

5. **usage_variance**: Variance of usage_similarity across client profiles. Drift may increase variance (some clients affected, others not); noise should not.

6. **pearson_r**: Pearson correlation between jaccard_similarity and usage_similarity across all 24 conditions. Tests orthogonality.

### Decision Metrics

7. **drift_usage_mean**: Mean usage_similarity across all drift patterns and sizes. Must be < 0.90.

8. **noise_usage_mean**: Mean usage_similarity across all noise patterns and sizes. Must be >= 0.95.

9. **discrimination_gap**: noise_usage_mean - drift_usage_mean. Must be >= 0.05.

## Frozen Decision Rule

**SURVIVES_CURRENT_TEST** if and only if ALL THREE conditions hold:

1. **Condition 1** (Drift detection): For EVERY drift pattern (remove_field, change_type, required_to_optional) at EVERY schema size (10, 20, 30, 50), the mean usage_similarity across 30 stale samples is < 0.90.

2. **Condition 2** (Noise tolerance): For EVERY noise pattern (optional_field_churn, null_valued_fields, nested_object_variation) at EVERY schema size (10, 20, 30, 50), the mean usage_similarity across 30 stale samples is >= 0.95.

3. **Condition 3** (Orthogonality): Pearson correlation between jaccard_similarity and usage_similarity across all 24 conditions (4 sizes × 6 patterns) is r < 0.90.

Otherwise **FALSIFIED-IN-SETTING**.

## Information Gain

- **If SURVIVES**: Field-usage profiling is a viable behavioral freshness signal. Changes product decision: behavioral signals can resolve the magnitude confound. Next step: composite signal experiment combining Jaccard + usage-similarity.

- **If FALSIFIED**: Field-usage profiling does not provide orthogonal discrimination. C-FRESHNESS remains HYPOTHESIS pending direct schema comparison (structural diff of schema definitions) or other fundamentally different mechanisms.

## Validity Threats

1. **Deterministic server**: Real APIs have stochastic field availability. Our mock is deterministic, so usage-similarity may be overestimated. Mitigation: report per-profile variance; if variance is zero, note that real-world variability could degrade performance.

2. **Client profiles are hand-designed**: Real clients may use overlapping or unusual field subsets. Mitigation: test 3 profiles covering light/medium/heavy usage; note generalization limit.

3. **Noise patterns are synthetic**: Real-world noise may affect used fields. Mitigation: noise patterns deliberately target unused fields to test the orthogonal signal hypothesis; if noise affects used fields, the signal is not orthogonal by construction.

4. **Sample size N=30**: May be insufficient for stable variance estimates. Mitigation: match parent experiment power; report confidence intervals.

## Infrastructure

- Mock server: Python stdlib http.server (no external dependencies)
- Schema generation: deterministic with seed=20260916
- Execution: single Python script, ~30 minutes runtime
- Artifacts: raw measurements, derived metrics, per-condition analysis
