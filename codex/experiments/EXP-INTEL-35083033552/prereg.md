# EXP-INTEL-35083033552 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35083033552
- **Lane**: Intel
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-16
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the ordering sensitivity of the interactive element metric stem primarily from the ROLE_MAP ambiguity (how 'a' elements are classified) or from the sample truncation (first-20 cap), and can a canonical interactive definition be established that is invariant to both?

## 3. Motivation

Prior Intel work established:
- EXP-INTEL-34782350557: Tightened role-only definition produces ordering sensitive to ROLE_MAP variant (with_map: cart>listing>detail; no_map: listing>cart>detail)
- EXP-INTEL-34956989900: elements_with_bbox denominator does NOT resolve ordering sensitivity; the issue is two-factor: (1) denominator variation and (2) ROLE_MAP-dependent count inflation
- The ROLE_MAP ('a'→'link', 'input'→'textbox') inflates counts differentially: cart +100%, detail +150%, listing +33%
- First-20 truncation produces differential undercount: listing 4.1x, detail 1.6x, cart 1.05x

The parent handoff asks: is the ordering sensitivity primarily from ROLE_MAP ambiguity or sample truncation? This experiment tests whether ANY granular ROLE_MAP definition can stabilize ordering under the existing truncated data.

## 4. Hypotheses

### H1: Canonical Definition Exists
At least 2 semantically adjacent ROLE_MAP definitions (differing by ≤1 role category) produce the same ordering across all 3 page types.

### H2: Link-Inclusion Drives Sensitivity
Definitions that include 'link' (from 'a' elements) produce different orderings than those that exclude it, confirming ROLE_MAP as the dominant driver.

### H3: Truncation Is Not the Only Driver
If H1 is true, truncation is not the sole confound — a canonical definition can stabilize ordering even under truncation.

### H4: Form-Only Definition Is Stable
The most restrictive definition (DEF-FORM-ONLY: form elements only, no links) produces ordering consistent with the no_map variant (listing>cart>detail), because it excludes the ambiguous 'a'→'link' mapping entirely.

## 5. ROLE_MAP Definitions

Five definitions ordered by semantic restrictiveness:

### DEF-FORM-ONLY (Most Restrictive)
Canonical roles: {button, textbox, checkbox, radio, combobox, listbox, slider, spinbutton, searchbox, switch}
Mapping: raw→canonical as-is (no 'a'→'link' mapping)
Rationale: Form elements are unambiguously interactive; links are navigation, not action.

### DEF-FORM-AND-BUTTON-LINK
Canonical roles: {button, link, textbox, checkbox, radio, combobox, listbox, slider, spinbutton, searchbox, switch}
Mapping: raw→canonical as-is (semantic 'link' role only)
Rationale: Includes semantic link role but not 'a' elements with raw role='a'.

### DEF-FORM-AND-A-TEXTBOX
Canonical roles: {button, link, textbox, checkbox, radio, combobox, listbox, slider, spinbutton, searchbox, switch}
Mapping: input→textbox (but NOT a→link)
Rationale: Tests whether the 'input'→'textbox' mapping alone affects ordering.

### DEF-FULL-MAP (Parent with_map)
Canonical roles: {button, link, textbox, checkbox, radio, combobox, listbox, menuitem, tab, slider, spinbutton, searchbox, switch}
Mapping: a→link, input→textbox
Rationale: Parent's with_map definition; includes menuitem, tab.

### DEF-ALL-LOCATABLE (Least Restrictive)
All elements in locatable_sample regardless of role.
Rationale: Upper bound; should equal locatable_sample size.

## 6. Data Source

Reuses existing raw measurement data:
- Source: `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json`
- SHA256: `da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050`
- 7 successful tasks from Magento shopping site (Docker: am1n3e/webarena-verified-shopping:latest)
- Truncated-first-20 locatable_sample per task (listing: 82 total, 20 sampled; detail: 32 total, 20 sampled; cart: 21 total, 20 sampled)

## 7. Measures

### 7.1 Per-Definition Tightened Count
For each task and each definition: count elements in locatable_sample whose canonical role is in the definition's INTERACTIVE_ROLES set.

### 7.2 Per-Definition Density
density = tightened_count / elements_with_bbox (consistent with parent)

### 7.3 Per-Definition Ordering
Sort page types by mean density (descending). Record the ordering tuple.

### 7.4 Ordering Stability Metrics
- **Pairwise agreement**: Number of definition pairs (out of 10) that produce the same ordering
- **Adjacent agreement**: Number of adjacent definitions (out of 4) that produce the same ordering
- **Max stable family**: Largest set of semantically adjacent definitions that agree on ordering
- **Link sensitivity**: Absolute difference in ordering between definitions that include vs exclude 'link'

### 7.5 Discrimination Ratio
Between-type variance / within-type variance for each definition.

## 8. Null Models

### 8.1 Random ROLE_MAP
Randomly assign each raw role to 'interactive' or 'not' with probability 0.5. Expected: ordering varies randomly across assignments. This tests whether the observed ordering sensitivity is above chance.

### 8.2 Single-Role Definitions
Test each individual role in isolation (button-only, link-only, textbox-only, etc.). Expected: single-role orderings vary, confirming that no single role drives the metric.

## 9. Statistical Tests

### 9.1 Primary: Pairwise Ordering Agreement
For each pair of definitions (10 pairs), compute whether ordering is identical. Report the fraction of agreeing pairs.

### 9.2 Secondary: Adjacency Agreement
For each adjacent pair (DEF-FORM-ONLY↔DEF-FORM-AND-BUTTON-LINK, etc.), test ordering agreement. Report the fraction.

### 9.3 Effect Size: Ordering Reversal Magnitude
For each pair that disagrees, measure the number of position swaps (Kendall tau distance) between the orderings.

### 9.4 Link Sensitivity
Compute |density(def_with_link) - density(def_without_link)| for each page type. Average across page types.

## 10. Controls

### 10.1 Positive Control
All 5 definitions produce tightened_count > 0 on all 7 tasks. This verifies definitions are non-degenerate.

### 10.2 Null Control
DEF-ALL-LOCATABLE yields tightened_count = locatable_sample length on all tasks. This verifies counting pipeline correctness.

### 10.3 Baseline Comparison
Orderings under DEF-FULL-MAP should match parent with_map ordering (cart>listing>detail). Orderings under DEF-FORM-ONLY should match parent no_map ordering (listing>cart>detail) if 'a'→'link' is the dominant sensitivity driver.

### 10.4 Extrapolation Consistency
If ordering under any definition matches the expected full-DOM ordering (listing>detail>cart from parent audit extrapolation), report as supporting evidence for that definition.

## 11. Validity Threats

### 11.1 Truncation Confound
All measurements use truncated-first-20 samples. Undercount factors (listing 4.1x, detail 1.6x, cart 1.05x) may cause ordering reversals that are truncation artifacts, not ROLE_MAP artifacts. Mitigation: report truncation-adjusted estimates alongside raw densities; acknowledge ceiling.

### 11.2 Single Site
All data from one Magento shopping site. Cross-site generalization unsupported. Mitigation: bound claim to this site.

### 11.3 Cart Pseudoreplication
Cart n=2 identical entries (same URL); deduped n=1 distinct. Within-type CV for cart undefined. Mitigation: report deduped statistics separately.

### 11.4 Definition Granularity
Only 5 definitions tested. Other definitions (e.g., including 'menuitem', 'tab') may produce different results. Mitigation: definitions span the full range from most to least restrictive; adjacent pairs differ by ≤1 role category.

### 11.5 Sample Size
7 tasks (3 listing, 3 detail, 1 cart). Low statistical power for detecting small ordering differences. Mitigation: report effect sizes alongside binary agreement; focus on large reversals.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ANY of:
1. At least 2 semantically adjacent definitions produce the same ordering across all 3 page types
2. The ordering is invariant to the link-inclusion decision (definitions with and without 'link' agree)

### 12.2 FALSIFIED-IN-SETTING
If ALL of:
1. All 5 definitions produce different orderings
2. No adjacent pair agrees on ordering
3. No definition matches the expected full-DOM ordering (listing>detail>cart)

### 12.3 MEASUREMENT_INVALID
If:
1. Raw data extraction fails or locatable_sample is missing for any task
2. Definitions produce degenerate results (zero counts everywhere)
3. Pipeline errors prevent computation

## 13. Expected Outcomes

### 13.1 SURVIVES_CURRENT_TEST (Canonical Definition Found)
- A specific ROLE_MAP definition stabilizes ordering under truncated sampling
- Product lane can adopt this definition for yield estimation
- Runtime lane should still fix the locatableSample cap for full-DOM validation, but the metric is usable now
- Claim C-MEAS-VALID advances toward VALIDATED for this metric

### 13.2 FALSIFIED-IN-SETTING (No Canonical Definition)
- No definition stabilizes ordering under truncation
- Truncation is the dominant confound; ROLE_MAP resolution alone is insufficient
- Runtime lane must fix the locatableSample cap before further metric validation
- Product lane cannot use fraction-based yield metrics until truncation is resolved
- Claim C-MEAS-VALID remains EXPERIMENTAL

### 13.3 MEASUREMENT_INVALID
- Pipeline error; not scientific evidence
- Retry with fixed pipeline

## 14. Analysis Plan

1. Load raw data from exp347_raw_results.json
2. For each of 5 definitions:
   a. Apply ROLE_MAP to each element's raw role
   b. Count elements whose canonical role is in INTERACTIVE_ROLES
   c. Compute density = count / elements_with_bbox
   d. Compute per-type mean density and ordering
   e. Compute between/within variance and discrimination ratio
3. Compute pairwise ordering agreement (10 pairs)
4. Compute adjacency agreement (4 adjacent pairs)
5. Compute Kendall tau distance for disagreeing pairs
6. Compute link sensitivity (with vs without 'link')
7. Run null models (random ROLE_MAP, single-role)
8. Compare with parent orderings
9. Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `json` for data loading
- `collections.Counter` for role counting
- `math` for variance/CV computation
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-INTEL-35083033552/analyze.py` before execution.

## 16. Pre-registered Expectations

From prior work:
- The 'a'→'link' mapping inflates counts 33-150% differentially across page types
- Without mapping, ordering partially matches expectations (listing>cart>detail)
- With mapping, ordering reverses (cart>listing>detail)
- If 'a'→'link' is the dominant driver, definitions excluding 'link' should agree (listing>cart>detail)
- If truncation is also a driver, even 'link'-excluded definitions may show instability

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
