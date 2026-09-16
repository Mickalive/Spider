# EXP-INTEL-35112013458 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35112013458
- **Lane**: Intel
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-16
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the truncated-sample pairwise ordering agreement of 0.3 (and adjacency 0.5) exceed chance-level expectation, and can the isolated a→link contribution be separated from menuitem/tab effects in the ordering reversal?

## 3. Motivation

Prior Intel work established:
- EXP-INTEL-35083033552: Three semantically adjacent definitions (DEF-FORM-ONLY, DEF-FORM-AND-BUTTON-LINK, DEF-FORM-AND-A-TEXTBOX) produce stable ordering: product_listing > cart > detail. DEF-FULL-MAP reverses to cart > product_listing > detail.
- The pairwise agreement is 0.3 (3/10 pairs agree) and adjacency agreement is 0.5 (2/4 adjacent pairs agree).
- The audit (VF-MISSING-NULL-MODELS) identified that the null models promised in prereg 8.1 and 8.2 were NOT executed, so the observed 0.3 cannot be assessed against chance.
- The isolated a→link effect is conflated with menuitem/tab inclusion (VF-LINK-SENSITIVITY-DILUTED): DEF-FULL-MAP bundles a→link with menuitem+tab.

This experiment addresses both gaps: (1) statistical significance of the observed agreement, and (2) isolation of the a→link effect.

## 4. Hypotheses

### H1: Random ROLE_MAP Null
The observed 0.3 pairwise agreement exceeds chance-level expectation. Specifically: the mean pairwise agreement across 1000 random ROLE_MAP assignments is < 0.3, AND the observed 0.3 exceeds the 95th percentile of the null distribution.

### H2: Single-Role Definitions
No individual role (button-only, a-only, input-only, etc.) produces stable ordering across all page types. Single-role orderings vary, confirming that the metric is multi-role, not driven by a single dominant role.

### H3: Isolated a→link Effect
A definition with a→link mapping but WITHOUT menuitem/tab produces the same ordering as DEF-FULL-MAP (cart > product_listing > detail). This isolates the a→link effect from menuitem/tab effects.

## 5. Data Source

Reuses existing raw measurement data:
- Source: `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json`
- SHA256: `da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050`
- 7 successful tasks from Magento shopping site
- Truncated-first-20 locatable_sample per task

## 6. Null Models

### 6.1 Random ROLE_MAP Null (Prereg 8.1)

**Procedure:**
1. For each of 1000 iterations (seed=42):
   a. For each raw role present in the data {a, button, combobox, div, form, input, label, link, menuitem, span, tab}, randomly assign it to INTERACTIVE_ROLES (included) or not, with probability 0.5 each.
   b. Apply this random definition to all 7 tasks.
   c. Compute density = count / elements_with_bbox for each task.
   d. Compute per-type mean density and ordering.
   e. Record the ordering tuple.

2. Compute pairwise agreement across all 1000 random orderings (comparing each pair's ordering to every other pair's ordering).

3. Compute the distribution of pairwise agreement fractions.

4. Test whether observed 0.3 exceeds the 95th percentile of this distribution.

**Expected under null:** Random assignments produce diverse orderings with pairwise agreement centered around the base rate of identical random orderings. With 3 page types and 3! = 6 possible orderings, random assignments should produce agreement ~1/6 ≈ 0.167 by chance.

### 6.2 Single-Role Definitions (Prereg 8.2)

**Procedure:**
1. For each raw role present in the data:
   - Create a definition that counts ONLY elements with that specific raw role as interactive.
   - Roles to test: {a, button, combobox, div, form, input, label, link, menuitem, span, tab}

2. For each single-role definition:
   a. Apply to all 7 tasks.
   b. Compute density = count / elements_with_bbox for each task.
   c. Compute per-type mean density and ordering.
   d. Record the ordering tuple.
   e. Record whether any tasks have zero count (degenerate definition).

3. Compare orderings across all single-role definitions.

**Expected under null:** Single-role orderings vary. No single role drives the metric. Some roles may be too rare to produce meaningful ordering (e.g., menuitem, tab have very few occurrences).

### 6.3 Isolated a→link Definition

**Procedure:**
1. Create DEF-ISOLATED-A-LINK:
   - INTERACTIVE_ROLES: {button, link, textbox, checkbox, radio, combobox, listbox, slider, spinbutton, searchbox, switch} (same as DEF-FORM-AND-A-TEXTBOX but adding a→link)
   - ROLE_MAP: {"a": "link", "input": "textbox"} (same as DEF-FULL-MAP)
   - BUT: exclude menuitem and tab from INTERACTIVE_ROLES

2. Apply to all 7 tasks.
3. Compute density = count / elements_with_bbox for each task.
4. Compute per-type mean density and ordering.
5. Record the ordering tuple.

**Expected under null:** If a→link alone drives the reversal, DEF-ISOLATED-A-LINK produces cart > product_listing > detail (same as DEF-FULL-MAP). If menuitem/tab are necessary, ordering differs.

## 7. Statistical Tests

### 7.1 Primary: Random Null Significance
- **Test:** Is observed 0.3 pairwise agreement > 95th percentile of null distribution?
- **One-sided:** Observed agreement exceeds chance.
- **Correction:** Single test (1 comparison), no Bonferroni needed.

### 7.2 Secondary: Single-Role Stability
- **Test:** How many single-role definitions produce the same ordering as any of the 5-definition family?
- **Expected:** 0 (no single-role definition matches any family member).

### 7.3 Effect Size: a→link Isolation
- **Test:** Does DEF-ISOLATED-A-LINK ordering match DEF-FULL-MAP?
- **Expected:** Yes (cart > product_listing > detail).

## 8. Controls

### 8.1 Positive Control
The isolated a→link definition (DEF-ISOLATED-A-LINK) produces ordering cart > product_listing > detail, matching DEF-FULL-MAP. This confirms a→link alone drives the reversal.

### 8.2 Null Control
Random ROLE_MAP null produces mean pairwise agreement < 0.3 with 95% CI excluding 0.3. This confirms observed agreement exceeds chance.

### 8.3 Baseline Comparison
Random null distribution mean should be approximately 1/6 ≈ 0.167 (base rate of identical random orderings with 3 types).

### 8.4 Single-Role Degeneracy Control
Single-role definitions with very few elements (count < 2 across all tasks) are flagged as degenerate and excluded from ordering comparison.

## 9. Validity Threats

### 9.1 Small Sample Size
7 tasks (3 listing, 3 detail, 1 cart). Low statistical power for detecting small ordering differences. Mitigation: focus on large effects (ordering reversals, not minor rank swaps).

### 9.2 Single Site
All data from one Magento shopping site. Cross-site generalization unsupported. Mitigation: bound claim to this site.

### 9.3 Cart Pseudoreplication
Cart n=2 identical entries (same URL); deduped n=1 distinct. Within-type CV for cart undefined. Mitigation: report deduped statistics separately.

### 9.4 Random Null Assumptions
The random null assumes each role is independently included/excluded with p=0.5. Real ROLE_MAP definitions have correlated role choices. Mitigation: this is a conservative null (independent inclusion is more diverse than real definitions).

### 9.5 Single-Role Sparsity
Some roles (menuitem, tab) may have very few occurrences, making their orderings unstable. Mitigation: report element counts alongside orderings; flag degenerate definitions.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Random null mean pairwise agreement < 0.3 AND observed 0.3 > 95th percentile of null distribution
2. No single-role definition produces invariant ordering (all single-role orderings differ from each other AND from the 5-definition family)
3. Isolated a→link definition produces same ordering as DEF-FULL-MAP (cart > product_listing > detail)

### 10.2 FALSIFIED-IN-SETTING
If ANY of:
1. Random null mean >= 0.3 OR observed 0.3 within 95% CI of null
2. Any single-role definition produces stable ordering
3. Isolated a→link produces different ordering than DEF-FULL-MAP

### 10.3 MEASUREMENT_INVALID
If:
1. Raw data extraction fails or locatable_sample is missing for any task
2. Pipeline errors prevent computation
3. Random null seed produces degenerate results

## 11. Expected Outcomes

### 11.1 SURVIVES_CURRENT_TEST (Null Models Confirm Significance)
- The observed 0.3 pairwise agreement is statistically significant (exceeds chance)
- The a→link effect is isolated as the driver (menuitem/tab not necessary)
- Product lane can adopt DEF-FORM-ONLY as canonical metric with statistical backing
- Claim C-MEAS-VALID advances toward VALIDATED for this metric

### 11.2 FALSIFIED-IN-SETTING (Null Models Fail)
- The observed 0.3 does not exceed chance
- OR the a→link effect requires menuitem/tab
- The truncated-sample ordering is noise
- Product lane cannot use fraction-based yield metrics until truncation is resolved
- Claim C-MEAS-VALID remains EXPERIMENTAL

### 11.3 MEASUREMENT_INVALID
- Pipeline error; not scientific evidence
- Retry with fixed pipeline

## 12. Analysis Plan

1. Load raw data from exp347_raw_results.json
2. Implement random ROLE_MAP null (1000 iterations, seed=42)
   a. For each iteration, randomly assign each raw role to interactive/not with p=0.5
   b. Compute ordering for each random assignment
   c. Compute pairwise agreement distribution
   d. Compare observed 0.3 to null distribution
3. Implement single-role definitions (11 roles)
   a. For each role, count only elements with that raw role
   b. Compute ordering for each single-role definition
   c. Compare orderings across all single-role definitions
4. Implement isolated a→link definition
   a. Create DEF-ISOLATED-A-LINK (a→link, input→textbox, no menuitem/tab)
   b. Compute ordering
   c. Compare with DEF-FULL-MAP ordering
5. Check controls (positive, null, baseline, degeneracy)
6. Apply decision rules
7. Report all outcomes with equal prominence

## 13. Analysis Code

Analysis will be implemented in Python using:
- `json` for data loading
- `random` for random ROLE_MAP generation (seeded)
- `collections.Counter` for role counting
- `math` for percentile computation
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-INTEL-35112013458/analyze.py` before execution.

## 14. Pre-registered Expectations

From prior work:
- The observed 0.3 pairwise agreement is based on 3 agreeing pairs out of 10 total
- With 3 page types and 6 possible orderings, random agreement should be ~1/6 ≈ 0.167
- The 'a'→'link' mapping inflates counts 33-150% differentially across page types
- DEF-FULL-MAP (a→link, menuitem, tab) produces cart>listing>detail
- DEF-FORM-AND-A-TEXTBOX (input→textbox only) produces listing>cart>detail
- The difference between these two is attributed to a→link + menuitem/tab

## 15. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 16. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
