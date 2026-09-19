# EXP-INTEL-35434771791 Preregistration

## Status: DESIGN — NOT YET FROZEN

---

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35434771791
- **Lane**: intel
- **Claim IDs**: C-MEAS-VALID
- **Parent Handoff**: EXP-INTEL-35422991016 (MEASUREMENT_INVALID)
- **Parent Question**: Does the OECD/COINr density pipeline preserve discrimination when sample-derived features replace the hierarchy-weighted density formula?

## 2. Scientific Question

Does the OECD/COINr density pipeline — comprising definition-based element filtering, recipe-based definition sampling, and normalization by elements_with_bbox — preserve the task-type discrimination present in sample-derived features (tag_entropy, form_fraction, total_area, all achieving eta2=1.0 on page_type) when these features are used as element-level weights? Or does the pipeline structurally collapse between-type variance regardless of input feature?

## 3. Background and Motivation

### What is established (from parent chain):
- Sample features have perfect task-type discrimination: tag_entropy eta2=1.0, form_fraction eta2=1.0, total_area eta2=1.0, within-type std=0.0 (EXP-INTEL-35409927864 M2, audit PASS; replicated in EXP-INTEL-35422991016 M2-M4)
- Hierarchy-weighted density formula produces eta2=0.0 with normalized formula (EXP-INTEL-35401997918 M7), but eta2=1.0 with binary inForm raw sum (EXP-INTEL-35422991016 compute_output.json) — normalization is the collapse mechanism
- Recipe choice is MATERIAL: 31x canonical/weighted gap (EXP-INTEL-35264637598)
- Linear combinations cannot break OECD/COINr dominance degeneracy (EXP-INTEL-35353016702)
- Within each recipe, definitions are highly correlated Spearman r > 0.98 (EXP-INTEL-3330747199)

### What failed:
- EXP-INTEL-35409927864: Falsified template composition explanation; sample IS discriminative (eta2=1.0)
- EXP-INTEL-35422991016: MEASUREMENT_INVALID — pipeline never executed; only raw feature eta2 computed (already established in parent)

### The critical gap:
The OECD/COINr pipeline (definition filtering × recipe sampling × normalization) has NEVER been tested with feature-based inputs. The raw feature eta2=1.0 was computed directly, bypassing the pipeline entirely. The audit required_fixes #2 explicitly states: "Test alternative metrics THROUGH the OECD/COINr density pipeline as frozen question/spec requires."

## 4. Hypothesis

The hierarchy-weighted density formula's eta2=0.0 was caused by the specific inForm binary weighting combined with normalization collapsing between-type variance. Feature-weighted densities using tag_entropy, form_fraction, or total_area as element weights should preserve discrimination (eta2 >= 0.05) through the full OECD/COINr pipeline because these features capture genuine structural differences between page types that survive definition filtering and normalization.

## 5. Falsifier

The hypothesis is falsified if ANY of:
- (F1) ALL feature-weighted density eta2 values through the pipeline are < 0.05 on page_type across all 3 definitions × 3 features
- (F2) The pipeline reorders page types such that the ranking contradicts the direct-feature ranking for ALL features simultaneously
- (F3) Normalized feature-weighted density produces eta2=0.0 for at least one feature that achieves eta2=1.0 as a direct value AND the normalized hierarchy density also produces eta2=0.0

## 6. Data and Sample

- **Raw evidence**: research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json (sha256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050)
- **Tasks**: 7 tasks (3 listing, 3 detail, 1 cart deduplicated from 8 successful measurements)
- **Sample**: truncated-first-20 locatable_sample per task, fields: tag, role, inForm, x, y, w, h
- **Site**: 1 Magento site (localhost:8080)
- **Within-type invariance**: All tasks of the same page type share identical element tags, roles, inForm flags, and bbox coordinates (template; EXP-INTEL-35409927864 M1)

## 7. OECD/COINr Pipeline Components

### 7.1 Definitions (element filtering by role)

Three definitions from prior experiments (EXP-INTEL-35083033552):

| Definition | INTERACTIVE_ROLES | ROLE_MAP |
|---|---|---|
| DEF-FULL-MAP | {button, link, textbox, checkbox, radio, combobox, listbox, menuitem, tab, slider, spinbutton, searchbox, switch} | {a→link, input→textbox} |
| DEF-FORM-ONLY | {button, textbox, checkbox, radio, combobox, listbox, slider, spinbutton, searchbox, switch} | {} (raw roles) |
| ISOLATED-A-LINK | {link} | {} (raw roles) |

Element matching: for each element in locatable_sample, apply ROLE_MAP to get canonical role, then check if canonical role is in INTERACTIVE_ROLES.

### 7.2 Feature-Weighted Density (replacing element count)

For each definition D and feature F:
```
feature_weighted_density(task, D, F) = sum(F(elem) for elem in locatable_sample if elem matches D) / elements_with_bbox
```

Where F(elem) is:
- **tag_entropy**: Not an element-level feature. Use per-element contribution: H_contribution(elem) = -p(tag) * log2(p(tag)) where p(tag) = count of this tag type / total elements. This gives each element its contribution to the task's tag entropy.
- **form_fraction**: Binary: 1.0 if elem.inForm == true, else 0.0. Sum gives count of inForm elements (same as hierarchy formula's raw input).
- **total_area**: elem.w × elem.h (bounding box area of each element).

### 7.3 Recipes (definition sampling)

Two recipes from prior experiments:

1. **Canonical per-iteration**: For each iteration, sample each role independently with p=0.5. Apply the SAME random subset to ALL tasks. Density = count of matching elements / elements_with_bbox. (From EXP-INTEL-35264637598.)

2. **Per-task weighted**: For each task independently, sample each role with p=0.5, weighted by task density. (From EXP-INTEL-35264637598.)

Note: For this experiment, since elements are identical within page types, recipe sampling affects WHICH definitions are active but not the within-type variance (which is 0 by construction). The recipe test is whether different active definition sets change the between-type ranking.

### 7.4 Normalization

OECD/COINr density normalization: density = feature_weighted_sum / elements_with_bbox.

For hierarchy density specifically:
```
normalized_hierarchy_density = sum(exp(-alpha * depth) * inForm) / total_hierarchy_weight
```
where total_hierarchy_weight = sum(exp(-alpha * depth) for all 20 elements), alpha=0.3.

## 8. Controls

### 8.1 Positive Control: PC1_RAW_FEATURES_REPRODUCE
- **What**: Direct (non-pipeline) eta2 computation for tag_entropy, form_fraction, total_area on page_type
- **Expected**: eta2=1.0 for all three, within-type std=0.0, group means within 0.001 of parent values
- **Purpose**: Confirms raw features retain discrimination before pipeline processing

### 8.2 Null Control: NC1_NORMALIZED_HIERARCHY_REPRODUCES
- **What**: Compute normalized hierarchy-weighted density (exp(-alpha*depth)*inForm / total_weight) for all 7 tasks, compute eta2 on page_type
- **Expected**: eta2 < 0.01, all page type means within 1% of each other
- **Purpose**: Reproduces the parent's eta2=0.0 anchor, establishing the C1 baseline that the parent experiment failed to produce in its own artifact
- **Note**: This requires depth values for the 20 elements. If depth is not available in the locatable_sample (only tag, role, inForm, x, y, w, h), use DOM tree depth from the raw measurement's DOM structure. If DOM depth is unavailable, use y-coordinate as a proxy for depth (higher y = deeper in the page), with the understanding that this is an approximation.

## 9. Metrics

### 9.1 Primary Metrics
- **M1_eta2_by_feature_definition**: For each of 3 features × 3 definitions: compute feature-weighted density for all 7 tasks, compute eta2 on page_type. Total: 9 eta2 values.
- **M2_eta2_by_recipe**: For the canonical recipe (10 seeds × 1000 iterations): compute recipe-sampled feature-weighted density, compute eta2. Report mean and std across seeds.
- **M3_ranking_by_feature**: For each feature: report the ranking of page types by mean feature-weighted density across all definitions. Compare to direct feature ranking.

### 9.2 Derived Metrics
- **M4_best_pipeline_eta2**: Maximum eta2 across all feature × definition × recipe combinations.
- **M5_pipeline_vs_direct_ratio**: best_pipeline_eta2 / direct_feature_eta2 (expected ~1.0 if pipeline preserves discrimination).
- **M6_hierarchy_eta2**: Normalized hierarchy density eta2 (expected ~0.0 from C2).
- **M7_ranking_agreement**: Fraction of definition × recipe combinations where the pipeline ranking matches the direct feature ranking.

## 10. Decision Rule

Conjunctive (see spec.json for full decision rules):

1. **C1**: Raw features reproduce (eta2 >= 0.99 for all three)
2. **C2**: Normalized hierarchy reproduces (eta2 < 0.01)
3. **C3**: Pipeline feature eta2 non-zero (max eta2 >= 0.05)
4. **C4**: Pipeline preserves ranking (>= 1 feature preserves listing-vs-detail ordering across all 6 definition×recipe combinations)
5. **C5**: Feature beats hierarchy (max_feature_eta2 > hierarchy_eta2 + 0.01)

## 11. Consequences

### If SURVIVES (C1 AND C2 AND C3 AND C4 AND C5):
- The hierarchy formula was the bottleneck, not the OECD/COINr pipeline
- Product lane can pursue density-based MIXED handling using feature-weighted density
- The 31x recipe material gap becomes actionable with the correct input feature

### If FALSIFIES (C1 AND C2 AND NOT C3):
- The OECD/COINr pipeline structure itself collapses between-type variance
- Density-based MIXED handling should be abandoned for this sample/site
- Product lane must pivot to non-density-based approaches

### If MIXED (C1 AND C2 AND C3 AND NOT C4):
- Pipeline preserves some discrimination but reverses rankings
- Product must decide which ranking is correct
- Possible: different features are appropriate for different definitions

## 12. Scope Limitations

- 7 tasks (3 listing, 3 detail, 1 cart), 1 Magento site, truncated-first-20 locatable_sample
- Within-type template invariance means eta2=1.0 is trivially achievable for any between-type-discriminative function
- The real test is whether the pipeline changes the RANKING, not whether eta2 is zero
- Cross-site generalization not tested
- Full DOM not tested (blocked by runtime substrate)
- Cart n=1 within-type variance degenerate

## 13. Estimated Cost

VERY LOW — offline computation on existing reconstructed data. No browser/network/model calls.

## 14. Expected Information Gain

HIGH — directly tests the critical untested question from parent EXP-INTEL-35422991016. Either outcome changes a concrete product decision about MIXED handling strategy.
