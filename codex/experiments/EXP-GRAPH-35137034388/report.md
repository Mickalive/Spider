# EXP-GRAPH-35137034388: Field-Usage Profiling for Drift-vs-Noise Discrimination

## Executive Summary

**Decision: FALSIFIED-IN-SETTING**

Field-usage profiling (tracking which fields different client profiles actually access) provides **partial** orthogonal discrimination that structural Jaccard similarity cannot:

- **PASS**: Noise patterns (optional_field_churn, null_valued_fields, nested_object_variation) produce usage_similarity = 1.0 at all schema sizes, well above the 0.95 threshold. Noise adds fields that no client uses, so usage patterns are unaffected.
- **PASS**: Two of three drift patterns (remove_field, required_to_optional) produce usage_similarity < 0.90. These patterns remove or hide fields that clients depend on, reducing usage similarity.
- **FAIL**: change_type produces usage_similarity = 1.0 at all sizes. Type-only changes do not alter field availability — the server still returns the field, and clients count it as "used" regardless of type mismatch.

The experiment is FALSIFIED because the frozen decision rule requires ALL THREE drift patterns to reduce usage_similarity < 0.90 (Condition 1). However, the discrimination gap (0.165) and orthogonality (Pearson r = -0.045) demonstrate that usage-similarity IS a valid orthogonal signal — it just cannot detect type-only changes.

## Motivation

Four signal families have been tested and falsified for C-FRESHNESS drift-vs-noise discrimination:
1. Jaccard structural similarity (FP=1.0 under noise)
2. TF-IDF semantic similarity (FP=1.0, inverted)
3. Response-time KS test (TP=0.0, inverted)
4. Linear Fisher LDA ensemble (AUC=0.625, all conditions fail)

All share the **magnitude confound**: noise patterns (adding 2 fields) produce larger divergence than drift patterns (adding 1 field). This experiment tests whether field-usage profiling provides an orthogonal signal that measures a fundamentally different dimension: functional field access rather than structural presence.

## Results

### Per-Pattern Usage Similarity (across all schema sizes)

| Pattern | Type | Mean Usage-Sim | Std | Jaccard | Detection |
|---------|------|---------------|-----|---------|-----------|
| remove_field | Drift | 0.865 | 0.055 | 0.90-0.98 | ✓ Below 0.90 |
| change_type | Drift | 1.000 | 0.000 | 0.82-0.96 | ✗ Above 0.90 |
| required_to_optional | Drift | 0.639 | 0.000 | 0.82-0.96 | ✓ Below 0.90 |
| optional_field_churn | Noise | 1.000 | 0.000 | 0.909 | ✓ Above 0.95 |
| null_valued_fields | Noise | 1.000 | 0.000 | 0.909 | ✓ Above 0.95 |
| nested_object_variation | Noise | 1.000 | 0.000 | 0.909 | ✓ Above 0.95 |

### Per-Profile Analysis (remove_field at n=10)

| Profile | Fields Used | Usage-Sim | Interpretation |
|---------|------------|-----------|----------------|
| A (light) | id, name | 1.0 | Unaffected: email removal doesn't impact identity-only access |
| B (medium) | id, name, email | 0.856 | Partially affected: loses email access |
| C (heavy) | id, name, email, phone | 0.75 | Most affected: email is 25% of field set |

### Decision Rule Evaluation

| Condition | Requirement | Result | Status |
|-----------|-------------|--------|--------|
| C1: Drift detection | ALL drift patterns < 0.90 | change_type = 1.0 | FAIL |
| C2: Noise tolerance | ALL noise patterns >= 0.95 | All noise = 1.0 | PASS |
| C3: Orthogonality | Pearson r < 0.90 | r = -0.045 | PASS |

### Key Metrics

- **Drift usage mean**: 0.835 (below 0.90 threshold — aggregate passes)
- **Noise usage mean**: 1.0 (above 0.95 threshold — passes)
- **Discrimination gap**: 0.165 (above 0.05 threshold — strong separation)
- **Pearson r**: -0.045 (near zero — signals are orthogonal)

## Interpretation

### What Works

Field-usage profiling successfully separates **field-availability drift** from **structural noise**:

1. **remove_field** (usage_sim ~0.865): When a field clients depend on is removed, usage-similarity drops below 0.90. Profile A (using only id, name) is unaffected because the removed field (email) is not in its access set. Profiles B and C lose access to email, reducing their usage-similarity.

2. **required_to_optional** (usage_sim ~0.639): When a field becomes optional (present ~50% of the time), usage-similarity drops dramatically. Profile A loses name access ~50% of the time, reducing its usage_sim to 0.5 (Jaccard of {id,name} vs {id} = 0.5).

3. **All noise patterns** (usage_sim = 1.0): Structural noise (adding churn fields, null fields, nested sub-fields) does not affect any client's access patterns because the added fields are not in any client's requested set.

### What Doesn't Work

**change_type** (usage_sim = 1.0): When a field's type changes (e.g., integer → string), the server still returns the field. Clients count it as "used" because the field exists and is non-null. Type mismatch is invisible to the usage-similarity metric, which measures field availability, not type compatibility.

This is a genuine limitation of field-usage profiling as modeled in this experiment. In practice, a client expecting an integer might fail to parse a string, effectively losing access to the field. However, our mock server does not model type validation — it returns whatever the server produces, and the client records the field as "used" if it exists.

### Orthogonality Confirmed

The near-zero Pearson correlation (r = -0.045) between Jaccard and usage-similarity confirms these are genuinely different signals:

- **Noise**: Jaccard drops to ~0.91 (new fields dilute the union), but usage_sim stays at 1.0 (clients don't use the new fields). This creates a separable region: (Jaccard ~0.91, usage_sim 1.0).
- **required_to_optional**: Jaccard drops to ~0.82-0.96 (field renamed), and usage_sim drops further to ~0.64 (field unavailable to clients). This creates a distinct region: (Jaccard ~0.82-0.96, usage_sim ~0.64).
- **remove_field**: Jaccard drops to ~0.90-0.98 (field removed from union), and usage_sim drops to ~0.865 (field unavailable to some clients). This creates a third region: (Jaccard ~0.90-0.98, usage_sim ~0.865).

These three regions are well-separated in (Jaccard, usage_sim) space, demonstrating that usage-similarity provides independent information from Jaccard.

## Claim Ceiling

The experiment falsifies the specific frozen decision rule (all three drift patterns must reduce usage_similarity < 0.90) but establishes a narrower valid ceiling:

**Field-usage profiling provides orthogonal discrimination for field-availability drift (remove_field, required_to_optional) but NOT for type-compatibility drift (change_type).** The discrimination gap of 0.165 and Pearson r of -0.045 confirm the signal is genuinely orthogonal to Jaccard.

Bounded to:
- Deterministic mock server (no timing/network variation)
- 3 hand-designed client profiles (light/medium/heavy)
- 4 schema sizes (10, 20, 30, 50 fields)
- Noise patterns that only add unused fields
- N=30 samples per condition
- Type changes that don't affect field availability

Does NOT establish:
- Detection of type-compatibility drift without client-side type validation
- Robustness when noise affects fields clients actually use
- Generalization to real APIs with stochastic field availability
- Optimal client profile design for real-world heterogeneous consumers
