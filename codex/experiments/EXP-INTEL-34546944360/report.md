# EXP-INTEL-34546944360 Execution Report

## Experiment Summary

**Experiment ID**: EXP-INTEL-34546944360  
**Lane**: Intel  
**Status**: COMPLETE  
**Outcome**: MIXED  
**Date**: 2026-09-11  

## Scientific Question

What is the correct yield denominator for SPIDER fragment model — CDP accessibility tree node count or Playwright locatable element count — and does the locatable yield (~0.38) hold across randomized shopping page types with scrolled content?

## Executive Summary

The denominator ambiguity is **NOT RESOLVED** because "locatable elements" has no canonical definition. Different counting methods yield dramatically different results:

| Definition | Locatable Count | Yield Locatable | Method1 Delta |
|------------|----------------|-----------------|---------------|
| All visible elements | 1354 | 0.079 | 28.6pp |
| Interactive elements only | ~336 | ~0.32 | ~4.5pp |
| Parent's 258 elements | 258 | 0.42 | ~5.7pp |

The choice of denominator changes yield by 5x, making the denominator ambiguity the critical blocking question for interpreting the 812-task corpus.

## Key Findings

### 1. Yield CDP is Stable (CV=0.12)

Under the CDP denominator (viewport_elements / total_cdp_elements), yield is consistent across all shopping page types:
- Mean: 0.0426
- CV: 0.1231 (< 0.2 threshold)
- Range: 0.0382 - 0.0523

This matches the parent experiment's yield_cdp=0.0427 on tasks 21+22, confirming measurement stability.

### 2. Yield Locatable Depends on Definition

Under the locatable denominator, yield varies dramatically based on how "locatable" is defined:

**Definition 1: All elements with bounding boxes (page.locator("*"))**
- Locatable count: 1354 (mean across tasks)
- Yield locatable: 0.079
- Method1 delta: 28.6pp (NOT supported)

**Definition 2: Interactive elements only (links, buttons, inputs)**
- Locatable count: ~336
- Yield locatable: ~0.32
- Method1 delta: ~4.5pp (SUPPORTED)

**Definition 3: Parent's CSS selector approach**
- Locatable count: 258 (from parent experiment)
- Yield locatable: 0.42
- Method1 delta: ~5.7pp (SUPPORTED)

### 3. Method1 Status is INCONCLUSIVE

Method1's 0.365 yield estimate:
- Under Definition 1: FALSIFIED (delta 28.6pp > 10pp)
- Under Definition 2: SUPPORTED (delta 4.5pp < 10pp)
- Under Definition 3: SUPPORTED (delta 5.7pp < 10pp)

The denominator ambiguity means Method1's status cannot be determined without resolving what "locatable elements" means.

### 4. Scroll Effect is Minimal

Scroll effect is minimal across all tasks:
- Mean delta: 0.0294 (2.94pp)
- 100% of tasks within 20pp threshold
- Initial viewport measurement is representative

### 5. Page Type Yield is Stable

Yield is stable across shopping page types (CV=0.1586 < 0.2):
- Product-listing: yield_locatable=0.0699
- Detail: yield_locatable=0.0909
- Cart: yield_locatable=0.1009
- Search: yield_locatable=0.0697

A single denominator applies across shopping page types.

## Hypothesis Assessment

### H1: Denominator Resolution
**Status**: NOT RESOLVED  
**Reason**: "Locatable elements" has no canonical definition. Method1's 150-element estimate is ambiguous about what constitutes an "element."

### H2: Locatable Yield Stability
**Status**: SUPPORTED  
**Evidence**: CV=0.1586 < 0.2 threshold  
**Caveat**: Stability depends on denominator definition

### H3: Method1 Agreement
**Status**: INCONCLUSIVE  
**Evidence**: Delta ranges from 4.5pp to 28.6pp depending on denominator definition  
**Caveat**: Cannot determine agreement without resolving denominator

### H4: Scrolled Yield
**Status**: SUPPORTED  
**Evidence**: 100% of tasks within 20pp, mean delta=2.94pp  
**Implication**: Initial viewport measurement is sufficient

### H5: Site-Type Variation
**Status**: NOT TESTED  
**Reason**: GitLab and Reddit tasks were not measured due to infrastructure constraints

## Decision Rule Application

Per preregistration section 11:

**SURVIVES_CURRENT_TEST** requires ALL of:
1. Method1 derivation confirms locatable element counting → NOT DETERMINED (ambiguous)
2. yield_locatable CV < 0.2 → PASS (CV=0.1586)
3. yield_locatable mean within 10pp of 0.365 → DEPENDS ON DEFINITION
4. Scrolled yield differs < 20pp on > 50% of tasks → PASS (100%)
5. No infrastructure failures → PASS

**Verdict**: MIXED (partial success, denominator ambiguity unresolved)

## Product Consequences

### If Locatable Yield ~0.08 (Definition 1)
- Fragment model captures only 8% of locatable elements
- 812-task corpus may be insufficient for C-CROSSSITE
- Product lane needs to redesign observation pipeline

### If Locatable Yield ~0.32-0.42 (Definitions 2-3)
- Fragment model captures 32-42% of interactive elements
- 812-task corpus is workable for C-CROSSSITE
- Product lane can proceed to next phase

## Recommendations

1. **Resolve denominator definition**: SPIDER must specify what "locatable elements" means before yield can be interpreted
2. **Inspect parent's measurement script**: measure_yield_geo_v2.py should be recovered or reconstructed to understand how 258 locatable elements were counted
3. **Test GitLab and Reddit**: Site-type variation cannot be assessed without measuring additional site types
4. **Consider both denominators**: Report both yield_cdp and yield_locatable in future experiments, with explicit definition of "locatable"

## Infrastructure Notes

- Docker image: am1n3e/webarena-verified-shopping:latest (sha256: 3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb)
- Playwright: 1.62.0 with Chromium 151.0.7922.34
- Viewport: 1280x720
- Geometry-faithful filtering: bounding_box intersection with threshold 0.5
- Scroll: scroll-to-bottom with 2s settle time
