# EXP-INTEL-34782350557 Execution Report

## Executive Summary

The experiment tested whether the interactive fraction metric maintains within-type stability and between-type discrimination when the element definition is tightened to exclude form-descendant DIV/SPAN/LABEL (role-only counting). The tightened definition dramatically reduces locatable counts (90% for listing, 84% for detail, 71% for cart) confirming the original definition overcounted form scaffolding. While stability and discrimination conditions are satisfied, **the ordering of per-type means reverses**: cart fraction (0.0053) > listing fraction (0.0047) > detail fraction (0.0037). This violates hypothesis H3 (expected listing > detail > cart). The experiment falsifies the hypothesis that the metric maintains the original ordering under definition tightening.

## Detailed Findings

### 1. Tightened Definition Impact
- **Listing pages**: Tightened locatable count drops from 82 to 8 elements (90% reduction). Interactive fraction drops from ~0.048 to ~0.0047 (10x reduction).
- **Detail pages**: Drops from 32 to 5 elements (84% reduction). Fraction from ~0.024 to ~0.0037.
- **Cart page**: Drops from 21 to 6 elements (71% reduction). Fraction from ~0.0185 to ~0.0053.

The reduction confirms the audit finding (VF-DEFINITION-OVERCOUNT): the original definition counted form-descendant DIV/SPAN/LABEL as interactive, inflating the numerator with elements lacking interactive roles.

### 2. Stability (H1)
- **Listing CV**: 0.0048 (n=3) – stable.
- **Detail CV**: 0.037 (n=3) – stable.
- **Cart CV**: 0.0 (n=2 identical measurements) – artificially zero due to pseudoreplication.

At least two page types have CV < 0.3, satisfying the stability condition.

### 3. Discrimination (H2)
- Between-type variance: 6.01e-07
- Within-type variance: 8.00e-09
- Discrimination ratio: 75.1 (between > within).

The metric still discriminates between page types under the tightened definition.

### 4. Ordering (H3) – **FALSIFIED**
- **Expected ordering**: listing (0.048) > detail (0.024) > cart (0.0185)
- **Actual ordering**: cart (0.0053) > listing (0.0047) > detail (0.0037)

The ordering reversal is driven by denominator variation: cart pages have smaller total DOM (1136 elements) vs listing (~1700) and detail (~1300). The tighter definition reduces numerator counts proportionally less for cart, inflating its fraction relative to listing/detail.

### 5. Controls
- **Positive control**: PASS – all tasks have >0 tightened locatable count.
- **Null control**: PASS – tightened count ≤ original count on all tasks.
- **Replication control**: PASS – tightened means are an order of magnitude lower than original means, confirming the form-membership clause added many elements.

## Interpretation

The metric captures interactive elements beyond form scaffolding (the tightened definition removes form-descendant DIV/SPAN/LABEL). However, the ordering property is not robust to definition tightening. The reversal suggests the metric's ordering is an artifact of denominator variation (total DOM elements) rather than a true difference in interactive element density.

The product consequence is mixed:
- **Positive**: The metric is not purely an artifact of form scaffolding; it retains meaningful variation across page types.
- **Negative**: The ordering property is definition-dependent and may not generalize to other sites or definition choices.

## Decision

**Verdict**: FALSIFIED-IN-SETTING (ordering reversal violates H3).

The experiment closes the hypothesis that the interactive fraction metric maintains the original ordering under definition tightening. The approach remains open for alternative definitions or denominator choices.

## Raw Evidence

- `raw_evidence/exp347_raw_results.json`: Original raw measurement data from parent experiment.
- `raw_evidence/tightened_results.json`: Derived per-task and per-type metrics under tightened definition.
- `raw_evidence/tightened_analysis.py`: Analysis script used to compute tightened metrics.