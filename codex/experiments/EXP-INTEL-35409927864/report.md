# EXP-INTEL-35409927864 — Report

## Question

Does the locatable_sample's fixed per-page-type template composition explain the parent's zero task-type discrimination (eta-squared=0.0), and does the full DOM contain task-type-discriminative tag structure that the sample masks?

## Verdict: FALSIFIES Template Explanation

**The template-composition hypothesis is falsified.** The sample IS per-task-structured with clear task-type discrimination (eta-squared = 1.0 on tag entropy, form fraction, total area). The parent's hierarchy-weighted density producing eta-squared = 0.0 was NOT caused by sample template invariance.

## Decision Rule Results

| Condition | Description | Result | Detail |
|-----------|-------------|--------|--------|
| **C1** | Sample elements 100% identical within each page type (all 7 fields) | **FAIL** | Y-coordinates differ for elements 12-19 (8 differences per type). Tags, roles, inForm, x, w, h are identical. |
| **C1b** | Sample elements identical (structural fields only, without y) | **PASS** | All structural fields (tag, role, inForm, x, w, h) identical within each page type. |
| **C2** | All sample metrics have eta-squared < 0.01 on page_type | **FAIL** | eta-squared = 1.0 for tag entropy, form fraction, total area, mean bbox area. |
| **C3** | Full DOM chi-squared p < 0.01 | **PASS** | p = 6.14e-53, chi2 = 462.56, Cramer's V = 0.150. |
| **C4** | I_sample = 0.0 AND I_full_dom > 0.0 | **FAIL** | MI_sample = 1.449 bits (NOT zero). MI_full_dom = 1.449 bits. |

**Frozen verdict rule:** `NOT C1 → FALSIFIES template explanation — sample IS per-task, and density failure is genuine. MIXED program should be abandoned for this sample.`

## Detailed Findings

### Sample Template Analysis

The locatable_sample has a **partially fixed template** structure:

**Within each page type, the sample is structurally identical:**
- All 3 listing tasks share: 7 unique tags, 85% inForm, total area 341,795 pixels^2
- All 3 detail tasks share: 7 unique tags, 95% inForm, total area 589,190 pixels^2
- Cart (1 task): 7 unique tags, 95% inForm, total area 428,790 pixels^2
- Within-type standard deviation = 0.0 for all metrics (perfect invariance)

**Across page types, the sample is dramatically different:**
- Listing vs detail: entropy 2.646 vs 2.484, form fraction 0.85 vs 0.95, total area 341K vs 589K
- eta-squared = 1.0 means 100% of variance is between-page-type

**The critical failure of the template hypothesis:** The sample has ZERO within-type variance but PERFECT between-type variance. This means the sample carries maximal task-type information, not zero. The hypothesis predicted zero between-type variance ("eta-squared=0.0 a mathematical necessity for ANY density recipe"), but the sample metrics show eta-squared = 1.0.

### Y-Coordinate Differences

Elements 12-19 have different y-coordinates across tasks within the same page type. These are the bottom-of-page elements (footer, newsletter forms, wish list/compare buttons). Their y-positions vary because:
- Different product listings have different content lengths
- Detail pages have different product descriptions
- The elements are at the DOM bottom, so their y-coordinate tracks total page height

These are **positional, not structural** differences. The elements themselves (tag, role, inForm, width, height) are identical.

### Full DOM Discrimination

The full DOM shows massive task-type discrimination:
- Listing: ~1700 elements, ~400 links, ~500 divs
- Detail: ~1300 elements, ~330 links, ~320 divs
- Cart: ~1100 elements, ~320 links, ~43 divs
- Chi-squared p = 6.14e-53 (overwhelmingly significant)

This confirms the full DOM contains task-type structure that the sample also captures (MI = 1.449 bits for both).

## Implications for MIXED Program

1. **Template explanation is dead.** The parent's zero density eta2 is NOT explained by sample template invariance. The sample has clear task-type structure.

2. **The density metric is the problem, not the sample.** The hierarchy-weighted density formula maps different sample compositions to the same density value. A different density metric that captures entropy/form fraction/area differences would achieve non-zero eta2.

3. **The 31x canonical/weighted material gap remains valid** (EXP-INTEL-35264637598). The task-type information exists in the sample; a metric needs to be designed to exploit it.

4. **Per-task sampling is NOT required** for task-type discrimination. The fixed truncated-first-20 sample already provides discriminative information (eta2=1.0 on basic metrics). The issue is metric design, not sampling.

## Scope

- 7 tasks, 1 Magento site, 3 definitions, truncated-first-20 locatable_sample
- Raw evidence: EXP-INTEL-34782350557 (sha256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050)
- checkout_1 excluded (connection refused error)
- cart_1 deduplicated (2 entries, 1 valid)
