# EXP-GRAPH-35154724244 — Direct Schema Comparison Experiment

**Status:** COMPLETE | **Outcome:** FALSIFIES

**Claim:** C-FRESHNESS (API endpoint freshness detection)

**Hypothesis:** Direct schema comparison (structural diff of schema definitions) provides reliable drift-vs-noise discrimination that all five tested indirect signal families cannot achieve.

---

## Summary

The hypothesis is **FALSIFIED**. Direct schema comparison produces a discrimination gap of only 0.37 between drift (mean=0.96) and noise (mean=0.59), which is insufficient for reliable thresholding. The mechanism fails on two of four frozen decision conditions:

1. **C2 Noise Tolerance (FAIL):** The `optional_field_addition` noise pattern produces schema diff magnitudes that scale with schema size (1.0 at n=10, 2.0 at n=20, 3.0 at n=30, 5.0 at n=50), exceeding the 0.5 threshold at all sizes.

2. **C4 Type-Aware Validation (FAIL):** Profile C (heavy validation: type+required+enum) achieves only a 4.7% validation failure rate for `change_type` drift, far below the 80% threshold required. The mock server always returns data matching schema types, making type drift invisible to client validation.

**C1 Drift Detection (PASS):** All five drift patterns produce nonzero schema diff magnitudes (0.3 to 2.0).

**C3 Orthogonality (PASS):** Pearson correlation between schema diff and Jaccard is -0.590, well below the 0.90 threshold, confirming schema diff captures complementary structural information.

---

## Key Findings

### 1. The Magnitude Confound Persists

The central insight from the parent experiment — that signal magnitude correlates with structural change magnitude rather than drift-vs-noise identity — remains true for direct schema comparison. The `optional_field_addition` noise pattern (adding ~10% optional fields) produces larger schema diffs than the `required_to_optional` drift pattern (changing one field's required status), making thresholding impossible without losing sensitivity to subtle but real drift.

### 2. Schema Diff vs. Jaccard Complementarity

Schema diff and Jaccard structural similarity measure complementary things:
- **Jaccard** is unchanged by `required_to_optional` (same field name + type pair) but degrades with `optional_field_addition`
- **Schema diff** detects `required_to_optional` (diff=0.3) but also detects `optional_field_addition` (diff=1.0-5.0)

The negative correlation (r=-0.590) confirms they capture different structural aspects, but neither alone — nor in combination — resolves the magnitude confound.

### 3. 3 of 5 Noise Patterns Are Invisible to Schema Diff

`description_change`, `default_value_change`, and `nested_property_addition` produce schema diff = 0.0. This is because schema diff compares field names, types, required status, and enums — it does not compare descriptions, default values, or nested property details. These noise patterns are structurally invisible to the metric.

### 4. Rename Drift Has No Behavioral Impact

`rename_field` produces the highest schema diff magnitude (2.0 = add 1 + remove 1) but zero client validation failures across all profiles. Clients validate field content, not field names. This confirms that schema diff measures structural change, not behavioral impact.

---

## Comparison with Baselines

| Signal | Drift Mean | Noise Mean | Discrimination Gap | Passes All Conditions? |
|--------|-----------|------------|-------------------|----------------------|
| Schema Diff | 0.96 | 0.59 | 0.37 | **NO** (C2, C4 fail) |
| Jaccard Structural | 0.818-1.0 | 0.909-1.0 | < 0.19 | **NO** (cannot threshold) |
| Response-Time KS | N/A | N/A | N/A | **NO** (falsified in parent) |
| Field-Usage Profiling | N/A | N/A | N/A | **NO** (falsified in parent) |

Schema diff provides marginal improvement over Jaccard in detecting `required_to_optional` drift, but cannot solve the fundamental magnitude confound.

---

## Decision

The hypothesis is **falsified in this setting**. Direct schema comparison is not a reliable drift-vs-noise discriminator because:

1. Structural noise (optional field additions) produces larger diffs than subtle structural drift (required-to-optional)
2. Type-aware client validation fails to detect type drift in a mock-conformant server environment
3. The discrimination gap (0.37) is insufficient for reliable thresholding

This does not close the C-FRESHNESS domain — it eliminates direct schema comparison as a standalone mechanism. The magnitude confound root cause identified in the parent experiment remains the fundamental barrier.

---

## Recommendations

1. **For DIRECTOR:** Mark schema diff as FALSIFIED as standalone drift-vs-noise discriminator; consider it as a weak supplementary signal alongside Jaccard
2. **For next experiment:** Test bounded noise scenarios (e.g., max 2 optional fields per update) to determine if the mechanism works in constrained settings
3. **For product:** Do not ship schema-diff-based freshness detection; the 0.37 discrimination gap would produce high false-positive rates in production

---

## Artifact References

| File | SHA256 | Role |
|------|--------|------|
| `raw_evidence/experiment_data.json` | `82ad397...` | Raw experiment data |
| `raw_evidence/derived_measurements.json` | `a585dc0...` | Derived measurements |
| `raw_evidence/decision_evaluation.json` | `a9a9773...` | Decision evaluation |
| `execute_schema_diff.py` | — | Experiment code |
