# EXP-INTEL-35409927864 preregistration

## Status: DESIGN — NOT YET FROZEN

---

## 1. Question

Does the locatable_sample's fixed per-page-type template composition explain the parent's zero task-type discrimination (eta-squared=0.0), and does the full DOM contain task-type-discriminative tag structure that the sample masks?

## 2. Background

The parent experiment (EXP-INTEL-35401997918) tested whether a DOM hierarchy-weighted density recipe could produce task-type structure for MIXED outcome resolution within the OECD/COINr framework. Result: FALSIFIED-IN-SETTING — eta-squared=0.0 at all alpha values (0.1, 0.3, 0.5), meaning the hierarchy-weighted density has identical mean across listing, detail, and cart page types. The hierarchy recipe is a perfect monotonic reparameterization of weighted density (Spearman rho=1.0).

The parent identified the root cause: depth estimation uses inForm (binary flag) rather than actual DOM tree structure, making the depth distribution task-invariant. However, the parent's analysis did not test whether the *entire locatable_sample* is a fixed template per page type.

Preliminary inspection of the raw evidence (EXP-INTEL-34782350557) reveals that the 20-element locatable_sample has **identical** element tags, roles, inForm flags, and bbox coordinates across all tasks within each page type. This means any metric computed from the sample is mathematically constrained to be constant within each page type, making eta-squared=0.0 a necessary consequence of the sampling procedure, not a property of the density metric.

## 3. Hypothesis

The 20-element locatable_sample is a fixed template per page type. All tasks of the same page type share identical element composition. This template invariance forces eta-squared=0.0 for ANY density recipe. The full DOM, by contrast, exhibits genuine task-type variation.

## 4. Falsifier

The template-composition explanation is falsified if:
- (F1) Within at least one page type, locatable_sample elements differ across tasks in tag, role, inForm, or bbox;
- (F2) A sample-derived metric achieves eta-squared >= 0.10 on page_type;
- (F3) The full DOM tag distribution does NOT differ significantly across page types (chi-squared p > 0.05).

## 5. Baselines

| ID | Description | Source |
|----|-------------|--------|
| B1 | Parent hierarchy density eta2 = 0.0 | EXP-INTEL-35401997918 M7 |
| B2 | Parent hierarchy vs weighted rho = 1.0 | EXP-INTEL-35401997918 M6 |
| B3 | Full DOM tag counts vary: listing div 163-171, detail div 98-126, cart div 43 | EXP-INTEL-34782350557 dom_stats |

## 6. Controls

- **PC1 (Positive):** Full DOM tag distribution differs across page types (chi-squared p < 0.01).
- **NC1 (Null):** Locatable_sample tag composition is identical within each page type (within-type std = 0.0 for all metrics).

## 7. Measurements

### Primary metrics

| ID | Metric | Definition |
|----|--------|------------|
| M1 | Sample template identity | For each page type, check if all locatable_sample elements are identical (field-by-field: tag, role, inForm, x, y, w, h) |
| M2 | Sample eta-squared | Eta-squared of sample-derived metrics (tag entropy, form fraction, total_area, mean_bbox_area) on page_type |
| M3 | Full DOM chi-squared | Chi-squared test of tag-type counts across page types |
| M4 | Mutual information | I(tag_composition; page_type) for both locatable_sample and full DOM |
| M5 | Information loss ratio | I_sample / I_full_dom (should be 0.0 if template is invariant) |

### Derived diagnostics

| ID | Metric | Definition |
|----|--------|------------|
| M6 | Within-type sample std | Standard deviation of each sample metric within each page type |
| M7 | Between-type full DOM effect size | Cramér's V for full DOM tag-type chi-squared |
| M8 | Sample element field coverage | Fraction of element fields that are constant within each page type |

## 8. Decision rule

Conjunctive:

- **C1:** Locatable_sample elements are 100% identical within each page type.
- **C2:** All sample-derived metrics have eta-squared < 0.01 on page_type.
- **C3:** Full DOM chi-squared p < 0.01.
- **C4:** I_sample = 0.0 AND I_full_dom > 0.0.

Verdicts:
- C1 AND C2 AND C3 AND C4 → CONFIRMS template explanation
- NOT C1 → FALSIFIES template explanation
- C1 AND C2 AND NOT C3 → Full DOM also lacks structure (page-type homogeneity)
- C1 AND NOT C2 → Sample has task-type structure (unexpected)

## 9. Validity threats

- **V1:** The 7-task, 1-site (Magento), 3-definition sample is small. Cross-site generalization not tested.
- **V2:** cart_1 appears twice in raw data (duplicate entry). Treated as single task.
- **V3:** checkout_1 has empty locatable_sample (total_dom=0). Excluded from sample-based analysis.
- **V4:** Mutual information estimation on small samples may be noisy. Chi-squared is more reliable for the primary test.
- **V5:** Full DOM tag counts are available but full DOM element-level structure (parent-child links, depth) is NOT in the raw evidence. True DOM depth remains untested.

## 10. Consequences

**If CONFIRMED:** The MIXED program's failure is attributed to sampling procedure, not density metric limitation. Product lane should obtain per-task locatable_samples from the runtime lane. The 31x canonical/weighted material gap remains usable with per-task samples. The parent's open question U-1 is resolved: template composition, not depth heuristic, explains zero eta-squared.

**If FALSIFIED (NOT C1):** The sample IS per-task and density failure is genuine. MIXED program should be abandoned for this sample. Pivot to cross-site testing or alternative metrics.

**If full DOM also lacks structure (NOT C3):** The MIXED program is limited by the Magento site's page-type homogeneity. Abandon density-based MIXED for this site; test on sites with more diverse page types.

## 11. Scope

- Bounded to: 7 tasks, 1 Magento site, 3 definitions, truncated-first-20 locatable_sample.
- Raw evidence: EXP-INTEL-34782350557 (sha256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050).
- No new data collection. All computations deterministic from existing artifacts.
- Estimated cost: < 1000 LLM tokens, < 5 minutes compute.
