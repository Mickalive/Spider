# EXP-INTEL-35462974425 Preregistration

## Experiment Metadata

- **Experiment ID**: EXP-INTEL-35462974425
- **Lane**: intel
- **Claim IDs**: C-MEAS-VALID
- **Parent**: EXP-INTEL-35445596324 (MIXED verdict, C6 FAIL: canonical recipe agreement 55.95% at truncated-first-20)

## 1. Question

Does the OECD/COINr pipeline preserve feature-weighted density ranking on full DOM elements (n=21-82 per task, not truncated-first-20) with richer element diversity — specifically, does canonical recipe ranking agreement reach the 80% threshold when the effective element count exceeds the 20-element truncation ceiling?

## 2. Background and Motivation

The parent experiment (EXP-INTEL-35445596324) tested whether ranking instability under recipe sampling is a sample-size artifact within the truncated-first-20 range. Key findings:

- **Sample-size effect is REAL and MONOTONIC**: canonical recipe agreement improves from 0% at n=5 to 55.95% at n=20 (Spearman=1.0, +55.95pp, C5 PASS).
- **But plateaus below 80%**: agreement at n=20 is only 55.95% — well below the 80% stability threshold (C6 FAIL).
- **Per-task recipe is closer**: 78.65% at n=20 — tantalizingly close to 80% but not tested by frozen C6.
- **Bootstrap CI is extremely wide**: 57.1% ± 49.5% (571/1000 bootstrap samples agree), confirming ranking is not a stable property at truncated-first-20.

The parent handoff identified full DOM testing as the single highest-information next step:

> "Full DOM samples (n=21-82, elements_with_bbox 1070-1564 full count) would contain richer element diversity with more discriminative elements per definition, potentially crossing the 80% threshold that the truncated-first-20 ceiling cannot reach."

The raw data from EXP-INTEL-34782350557 contains locatable_sample per task. Prior experiments truncated to first-20 elements by DOM position. This experiment uses ALL elements with bbox.

## 3. Hypothesis

The ranking instability at truncated-first-20 is a truncation artifact. Full DOM samples contain richer element diversity with more discriminative elements per definition, enabling canonical recipe sampling to capture a more representative subset.

Specifically:
- **H1**: Canonical recipe ranking agreement for tag_entropy × DEF-FULL-MAP will be ≥80% on full DOM
- **H2**: Full-DOM agreement will exceed truncated-first-20 agreement (55.95%) by ≥10 percentage points
- **H3**: Per-task recipe ranking agreement will be ≥85% on full DOM

## 4. Falsifier

The hypothesis is falsified if ANY of:
- **F1**: Canonical recipe agreement on full DOM < 75% — instability is structural regardless of element count
- **F2**: Full-DOM agreement does NOT exceed truncated-first-20 (55.95%) by ≥5pp — additional elements don't help
- **F3**: Per-task recipe agreement on full DOM < 75% — even independent sampling can't stabilize
- **F4**: Pipeline eta2 on full DOM drops below 0.90 — full-DOM elements introduce noise that degrades discrimination

## 5. Baselines

| ID | Description | Source |
|---|---|---|
| B1 | Truncated-first-20 canonical agreement: 55.95% (tag_entropy × DEF-FULL-MAP) | EXP-INTEL-35445596324 M4 |
| B2 | Truncated-first-20 per-task agreement: 78.65% (tag_entropy × DEF-FULL-MAP) | EXP-INTEL-35445596324 M5 |
| B3 | Non-recipe pipeline ranking agreement: 100% (tag_entropy both definitions) | EXP-INTEL-35445596324 B2 controls |
| B4 | Non-recipe pipeline eta2: 0.9996 (DEF-FORM-ONLY), 0.9958 (DEF-FULL-MAP) at n=20 | EXP-INTEL-35445596324 M3 |

## 6. Controls

### Positive Control: PC1_RAW_FEATURE_REPRODUCES_FULL_DOM

Direct (non-pipeline) computation of tag_entropy, form_fraction, and total_area eta2 on page_type reproduces eta2 ≥ 0.99 on full DOM locatable_sample.

**Expected**: All three features: eta2 ≥ 0.99, within-type std < 0.001. Feature values will differ from truncated-first-20 (more elements contribute), but within-type template invariance preserves perfect discrimination.

### Null Control: NC1_HIERARCHY_NORMALIZED_FULL_DOM

Normalized hierarchy-weighted density formula produces eta2 < 0.01 on page_type with full DOM elements.

**Expected**: eta2 < 0.01, all page type means within 1% of each other.

## 7. Data Availability Gate (C3)

**CRITICAL**: Before any analysis, the script must verify that locatable_sample contains >20 elements for at least 5 of 7 tasks. If ALL tasks have exactly 20 elements (confirming the raw data itself is truncated at collection time), the experiment is BLOCKED — full DOM re-collection from the Magento Docker container would be required.

Expected full element counts (from EXP-INTEL-34782350557 metadata):
- Listing tasks: 1550-1564 elements_with_bbox
- Detail tasks: 1149-1215
- Cart: 1070

## 8. Analysis Protocol

### 8.1 Feature Computation (Full DOM)

For each task, use the ENTIRE locatable_sample (all elements with bbox):
- **tag_entropy**: -sum(p(tag) * log2(p(tag))) per element
- **form_fraction**: 1.0 if inForm else 0.0 per element
- **total_area**: w * h per element

### 8.2 Non-Recipe Pipeline

Compute feature-weighted density = sum(feature_value for matching elements) / elements_with_bbox for each feature × definition × task. Compute eta2 on page_type.

### 8.3 Recipe Sampling

At full DOM:
- **Canonical recipe**: shared subset p=0.5 (same roles sampled for all tasks), 10 seeds × 1000 iterations
- **Per-task recipe**: independent p=0.5 per task, 10 seeds × 1000 iterations
- Compute ranking agreement (listing > detail preserved) per iteration
- Aggregate: mean ± std across seeds

### 8.4 Bootstrap Resampling

B=1000 bootstrap resamples of tasks within each page_type (with replacement). Compute canonical recipe ranking agreement per bootstrap. Report mean ± std. Compare CI width against parent (49.5% std).

### 8.5 Comparison Metrics

- **M1**: Full-DOM canonical agreement (tag_entropy × DEF-FULL-MAP)
- **M2**: Full-DOM per-task agreement (tag_entropy × DEF-FULL-MAP)
- **M3**: Delta = M1 - 55.95% (parent truncated-first-20)
- **M4**: Full-DOM bootstrap CI width
- **M5**: Full-DOM pipeline eta2 (max across features × definitions)

## 9. Decision Rules

C1: PC1 passes (all three features eta2 ≥ 0.99 on full DOM)
C2: NC1 passes (hierarchy eta2 < 0.01 on full DOM)
C3: ≥5 of 7 tasks have locatable_count > 20 (full DOM data available)
C4: Pipeline max eta2 ≥ 0.05 on full DOM
C5: Full-DOM canonical agreement > 60.95% (exceeds truncated-first-20 by ≥5pp)
C6: Full-DOM canonical agreement ≥ 75%
C7: Full-DOM per-task agreement ≥ 85%

**Verdict mapping**:
- NOT C1 → MEASUREMENT_INVALID
- NOT C2 → MEASUREMENT_INVALID
- NOT C3 → BLOCKED (data unavailable)
- C1 ∧ C2 ∧ C3 ∧ NOT C4 → FALSIFIES (pipeline collapses)
- C1 ∧ C2 ∧ C3 ∧ C4 ∧ NOT C5 → FALSIFIES (no improvement over truncated)
- C1 ∧ C2 ∧ C3 ∧ C4 ∧ C5 ∧ NOT C6 → MIXED (improves but <75%)
- C1 ∧ C2 ∧ C3 ∧ C4 ∧ C5 ∧ C6 ∧ NOT C7 → SURVIVES_PARTIALLY (canonical viable, per-task untested)
- C1 ∧ C2 ∧ C3 ∧ C4 ∧ C5 ∧ C6 ∧ C7 → SURVIVES (both viable)

## 10. Product Consequences

### If SURVIVES (C5 ∧ C6 ∧ C7 PASS):
- Recipe density is viable for MIXED handling
- Product lane can use tag_entropy-weighted density with canonical or per-task recipe
- The 31x recipe material gap (EXP-INTEL-35264637598) becomes actionable
- MIXED program is unblocked

### If FALSIFIES (C5 FAILS):
- Ranking instability is structural, not a truncation artifact
- Product lane must use non-recipe density only (100% ranking agreement, lower eta2)
- Recipe density design path is closed for this definition×recipe framework
- No further full-DOM testing needed on this site

### If MIXED (C5 passes, C6 fails):
- Full DOM improves but doesn't reach threshold
- Product lane must evaluate whether 60-75% agreement is sufficient for use case
- May warrant testing on additional sites or with different definitions

## 11. Validity Threats

1. **Template invariance at full DOM**: Within-type template invariance may persist in full DOM, making eta2 trivially achievable. Ranking preservation remains the only discriminating check (inherited from parent audit VF1).

2. **Cart n=1 degeneracy**: Cart page_type has n=1, making within-type variance degenerate. Comparison focuses on listing vs detail (n=3 each).

3. **Element count heterogeneity**: Full DOM samples vary widely (1070-1564 elements_with_bbox). The normalization by elements_with_bbox should handle this, but extreme variance may affect recipe sampling.

4. **Definition degeneracy**: ISOLATED-A-LINK is expected degenerate (zero elements match). Analysis focuses on DEF-FULL-MAP and DEF-FORM-ONLY.

5. **Single site**: Magento localhost only. Cross-site generalization not tested.

6. **Data truncation risk**: If locatable_sample is truncated at collection time (all tasks have exactly 20 elements), the experiment is BLOCKED. The data availability gate (C3) explicitly checks for this.

## 12. Estimated Cost

Very low — offline computation on existing data. No browser/network/model calls.
- ~168 density values (3 features × 2 definitions × 7 tasks × 1 full-DOM)
- ~120,000 recipe iterations (2 recipes × 10 seeds × 1000 iters × 2 definitions × 3 features)
- ~4000 bootstrap iterations
- Estimated < 5000 LLM tokens for analysis code, < 60 seconds compute
