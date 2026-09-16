# EXP-GRAPH-35154724244 Preregistration

## Experiment Identity

- **Experiment ID**: EXP-GRAPH-35154724244
- **Lane**: graph
- **Claim**: C-FRESHNESS
- **Parent**: EXP-GRAPH-35137034388 (Field-usage profiling — FALSIFIED-IN-SETTING)

## Motivation

Five orthogonal signal families have been tested and falsified for drift-vs-noise discrimination:

1. **Jaccard structural similarity** (field_path,type) — FP=1.0 at all sizes (EXP-GRAPH-34788722106)
2. **TF-IDF bag-of-words semantic similarity** — FP=1.0, inverted direction (EXP-GRAPH-35010853847)
3. **Response-time KS two-sample test** — TP=0.0, FP=0.1875, inverted direction (EXP-GRAPH-35083040517)
4. **Linear Fisher LDA ensemble** of (1-Jaccard) and KS D — AUC=0.625, all conditions fail (EXP-GRAPH-35130682058)
5. **Field-usage profiling** — orthogonal (r=-0.045) but fails on change_type (usage_similarity=1.0) (EXP-GRAPH-35137034388)

All share a common root cause: **magnitude confound** where structural noise patterns produce larger divergence than true drift patterns, OR the signal measures an indirect proxy that doesn't capture the drift dimension.

The parent handoff recommends testing **direct schema comparison** — structural diff of schema definitions themselves, bypassing behavioral proxies entirely. This measures structural change at the schema level (field names, types, nesting depth, required/optional status, enum constraints) rather than via response timing, field usage, or semantic similarity.

This experiment tests whether direct schema comparison provides reliable drift-vs-noise discrimination.

## Core Insight

Indirect signals (Jaccard, TF-IDF, response-time, field-usage) measure behavioral proxies of structural change. Direct schema comparison measures the structural change itself. The magnitude confound arises because noise patterns (adding unused fields) produce larger behavioral divergence than drift patterns (changing one field's type). But at the schema level, drift patterns produce clear structural diffs (type change, required→optional) while noise patterns produce diffs only in optional/description fields that don't affect functional semantics.

## Hypothesis

**H1**: Direct schema comparison detects drift patterns (add_field, remove_field, change_type, required_to_optional, rename_field) as non-zero diff magnitude.

**H2**: Noise patterns (description_change, default_value_change, optional_field_addition, nested_property_addition, enum_expansion) produce diff magnitude below a separable threshold.

**H3**: Schema diff magnitude provides information beyond Jaccard structural similarity (Pearson r < 0.90).

**H4**: Type-aware client validation detects change_type drift (validation failure rate > 0.8) while noise patterns produce validation failure rate < 0.1.

## Falsifier

The experiment is FALSIFIED if:

- (F1) No threshold on schema diff magnitude achieves TP >= 0.9 for drift AND FP <= 0.15 for noise across all schema sizes, OR
- (F2) Pearson r between schema diff magnitude and Jaccard > 0.95 (redundant signal), OR
- (F3) Type-aware client validation fails to detect change_type drift (validation failure rate < 0.8) OR falsely triggers on noise (validation failure rate > 0.1).

## Experimental Design

### Mock API Server

A local HTTP server serves JSON responses **and JSON Schema definitions** for 4 resource families: `users`, `posts`, `comments`, `items`. Each response contains a fixed set of fields determined by the current schema state (fresh, drifted, or noisy).

The server is **deterministic**: given a (resource, schema_state, resource_id) triple, it returns the same response and schema every time. No timing jitter, no network variation.

### Schema Representation

Each resource has a JSON Schema definition describing:
- Field names and types (string, integer, boolean, array, object)
- Required/optional status
- Enum constraints (where applicable)
- Nesting depth (one level of nested objects allowed)

### Client Profiles

Three client profiles with increasing validation strictness:

| Profile | Validation | Use Case |
|---------|-----------|----------|
| A (light) | No validation, just requests fields | Simple consumer |
| B (medium) | Type checking only | Type-sensitive consumer |
| C (heavy) | Type + required + enum validation | Full schema validator |

Each client makes 10 requests per condition, requesting only its designated fields.

### Schema Sizes

4 sizes matching prior experiments: 10, 20, 30, 50 fields. Baseline schemas are generated deterministically with the frozen seed.

### Drift Patterns (True Drift)

| Pattern | Description | Expected Schema Diff |
|---------|-------------|---------------------|
| add_field | Add one required field | +1 field, diff magnitude >= 1.0 |
| remove_field | Remove one required field | -1 field, diff magnitude >= 1.0 |
| change_type | Change one field's type (integer→string) | Type change, diff magnitude >= 0.5 |
| required_to_optional | Move one required field to optional | Required change, diff magnitude >= 0.3 |
| rename_field | Rename one field (keeping type) | Name change, diff magnitude >= 1.0 |

### Noise Patterns (Structural Noise) — Redesigned to overlap with client-requested fields

| Pattern | Description | Expected Schema Diff |
|---------|-------------|---------------------|
| description_change | Change description of a used field | Description change, diff magnitude <= 0.1 |
| default_value_change | Change default value of a used field | Default change, diff magnitude <= 0.1 |
| optional_field_addition | Add optional field (may be used by heavy client) | +1 optional field, diff magnitude <= 0.5 |
| nested_property_addition | Add nested property to a used field | +1 nested property, diff magnitude <= 0.3 |
| enum_expansion | Add extra enum values to a used field | Enum change, diff magnitude <= 0.2 |

### Sample Sizes

- **N = 30** fresh samples per condition per schema size
- **N = 30** stale samples per condition per schema size
- **Total**: 4 sizes × 10 patterns × 30 samples × 2 (fresh/stale) = 2400 samples
- **API calls**: 2400 samples × 3 clients × 10 requests = 72,000 local calls

### Controls

| Control | Expected Behavior |
|---------|-------------------|
| Fresh copies (identical schemas) | diff magnitude = 0, validation failure = 0 |
| Drift at size 10 | diff magnitude > 0, validation failure > 0 for type-aware |
| Noise at size 10 | diff magnitude <= 0.5, validation failure < 0.1 |
| Stable resource (users_stable) | diff magnitude = 0 across all conditions |

## Metrics

### Primary Metrics

1. **schema_diff_magnitude**: Weighted sum of structural changes: 1.0 per added/removed field, 0.5 per type change, 0.3 per required→optional change, 0.2 per enum change. Computed per sample pair (fresh vs stale schema).

2. **validation_failure_rate**: Fraction of requests failing validation per client profile per condition. For profile C (heavy): type + required + enum validation.

### Derived Metrics

3. **diff_jaccard_gap**: schema_diff_magnitude - (1 - Jaccard) per condition. Positive means schema diff captures more change than Jaccard.

4. **pearson_r**: Pearson correlation between schema_diff_magnitude and Jaccard across all 40 conditions. Tests orthogonality.

5. **per_pattern_discrimination**: For each pattern, compute separation between drift and noise distributions.

### Decision Metrics

6. **drift_diff_mean**: Mean schema_diff_magnitude across all drift patterns and sizes. Must be > 0.0.

7. **noise_diff_mean**: Mean schema_diff_magnitude across all noise patterns and sizes. Must be <= 0.5.

8. **discrimination_gap**: drift_diff_mean - noise_diff_mean. Must be > 0.0.

9. **type_aware_detection**: Profile C validation failure rate for change_type drift must be > 0.8.

10. **type_aware_false_positive**: Profile C validation failure rate for noise patterns must be < 0.1.

## Frozen Decision Rule

**SURVIVES_CURRENT_TEST** if and only if ALL FOUR conditions hold:

1. **Condition 1** (Drift detection): For EVERY drift pattern (add_field, remove_field, change_type, required_to_optional, rename_field) at EVERY schema size (10, 20, 30, 50), the mean schema_diff_magnitude across 30 stale samples is > 0.0.

2. **Condition 2** (Noise tolerance): For EVERY noise pattern (description_change, default_value_change, optional_field_addition, nested_property_addition, enum_expansion) at EVERY schema size (10, 20, 30, 50), the mean schema_diff_magnitude across 30 stale samples is <= 0.5.

3. **Condition 3** (Orthogonality): Pearson correlation between schema_diff_magnitude and Jaccard across all 40 conditions is r < 0.90.

4. **Condition 4** (Type-aware validation): Profile C validation failure rate for change_type drift is > 0.8, AND validation failure rate for all noise patterns is < 0.1.

Otherwise **FALSIFIED-IN-SETTING**.

## Information Gain

- **If SURVIVES**: Direct schema comparison is a viable structural freshness signal. Changes product decision: structural signals can detect drift without behavioral proxies. Next step: integrate into freshness guards, test on real API schemas.

- **If FALSIFIED**: Direct schema comparison does not provide discrimination beyond Jaccard. C-FRESHNESS remains HYPOTHESIS pending session-level behavioral signals (token validation, cookie state inspection) which test a fundamentally different dimension.

## Validity Threats

1. **Deterministic server**: Real APIs have stochastic field availability. Our mock is deterministic, so schema diff may be overestimated. Mitigation: report per-condition variance; note that real-world variability could degrade performance.

2. **Client profiles are hand-designed**: Real clients may have different validation logic. Mitigation: test 3 profiles covering none/type/full validation; note generalization limit.

3. **Noise patterns are synthetic**: Real-world noise may affect required fields or types. Mitigation: noise patterns deliberately target used fields (descriptions, defaults, enums) to test schema-level discrimination; if noise affects types/required status, it becomes drift by definition.

4. **Sample size N=30**: May be insufficient for stable variance estimates. Mitigation: match parent experiment power; report confidence intervals.

5. **Schema diff weighting**: The weights (1.0, 0.5, 0.3, 0.2) are arbitrary. Mitigation: sensitivity analysis across weight sets; report raw counts of each change type.

## Infrastructure

- Mock server: Python stdlib http.server (no external dependencies)
- Schema generation: deterministic with seed=20260917
- Execution: single Python script, ~45 minutes runtime
- Artifacts: raw measurements, derived metrics, per-condition analysis
