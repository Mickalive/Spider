# EXP-INTEL-34956989900 Report

## Executive Summary

**Outcome: FALSIFIES** — Element density normalized by `elements_with_bbox` does NOT resolve the denominator sensitivity that confounded the ordering test under the tightened role-only definition.

The hypothesis that `tightened_locatable_count / elements_with_bbox` would yield ordering listing > detail > cart is **falsified** in both ROLE_MAP variants:

- **With ROLE_MAP** (a→link, input→textbox): ordering is cart (0.005607) > listing (0.005135) > detail (0.004280)
- **Without ROLE_MAP**: ordering is listing (0.003851) > cart (0.002804) > detail (0.001712)

Neither variant achieves listing > detail > cart. The ordering is highly sensitive to the ROLE_MAP variant, with cart density inflating 99.9% under the mapping relative to the no-map variant.

## Detailed Results

### Per-Type Element Density (elements_with_bbox denominator)

| Page Type | With Map Mean | With Map CV | No Map Mean | No Map CV |
|-----------|---------------|-------------|-------------|-----------|
| Listing (n=3) | 0.005135 | 0.0046 | 0.003851 | 0.0046 |
| Detail (n=3) | 0.004280 | 0.0335 | 0.001712 | 0.0335 |
| Cart (n=1) | 0.005607 | N/A | 0.002804 | N/A |

### Ordering Comparison

| Denominator | With Map | No Map |
|-------------|----------|--------|
| elements_with_bbox | cart > listing > detail | listing > cart > detail |
| total_dom | cart > listing > detail | listing > cart > detail |

The ordering is identical between denominators for a given ROLE_MAP variant, indicating the denominator change does not alter the fundamental ordering pattern.

### Discrimination Ratio

| Denominator | With Map | No Map |
|-------------|----------|--------|
| elements_with_bbox | 42.75 | 632.93 |
| total_dom | 60.08 | 603.19 |

Discrimination remains strong (>1.0) in all cases. The elements_with_bbox denominator slightly reduces discrimination with mapping but slightly increases it without mapping.

### Controls

| Control | Status | Notes |
|---------|--------|-------|
| Positive (all > 0) | ✅ PASS | All tasks have tightened count > 0 |
| Null (tightened ≤ original) | ✅ PASS | Tightened counts ≤ original on all tasks |
| Denominator sensitivity (bbox/total > 0.8) | ✅ PASS | All ratios > 0.87 |
| Extrapolation consistency (listing > detail > cart) | ❌ FAIL | Orderings do not match |

## Interpretation

### Why elements_with_bbox Fails to Resolve Sensitivity

The denominator sensitivity confound is not primarily about DOM size variation — it is about **differential count inflation from the ROLE_MAP**. When 'a'→'link' mapping is applied:

- Cart's tightened count: 6 (from 3 without map) — 100% increase
- Listing's tightened count: 8 (from 6 without map) — 33% increase
- Detail's tightened count: 5 (from 2 without map) — 150% increase

The cart and detail pages have proportionally more `<a>` elements with implicit link roles than listing pages. The mapping differentially inflates their counts, which combined with their smaller denominators (elements_with_bbox), pushes cart above listing in density.

### Key Insight

The ordering sensitivity is a **two-factor problem**:
1. **Denominator variation** (partially addressed by elements_with_bbox)
2. **ROLE_MAP-dependent count inflation** (not addressed by denominator choice)

elements_with_bbox reduces factor (1) but not factor (2). The remaining denominator variation (listing 0.914, detail 0.871-0.877, cart 0.942 of total_dom) is insufficient to overcome the count inflation effect.

### Product Consequence

The interactive fraction metric remains denominator-confounded AND definition-confounded. Product lane cannot use this metric for yield estimation without:
1. Resolving the ROLE_MAP ambiguity (frozen spec does not mandate a mapping)
2. Full DOM enumeration (not truncated to 20) to eliminate sample truncation effects
3. Either: abandoning role-only counting, or finding a definition that is invariant to the a→link mapping

## Validity Threats

1. **Sample truncation (inherited)**: Tightened counts from first-20 sample. Listing undercounted 4.1x, detail 1.6x, cart 1.05x. Differential truncation may affect ordering.

2. **ROLE_MAP deviation (inherited)**: The 'a'→'link' mapping is undocumented and inflates counts 33-150%. The spec does not resolve this ambiguity.

3. **Cart pseudoreplication (inherited)**: Cart n=2 identical entries, n=1 distinct after deduplication.

4. **Single-site generalization**: All data from one Magento shopping site.

## Recommendations

1. **Do not promote** elements_with_bbox as a resolution to the denominator sensitivity confound.
2. **Resolve the ROLE_MAP ambiguity** before further metric validation. The frozen spec must mandate whether 'a' elements count as 'link'.
3. **Full DOM enumeration** is required to eliminate sample truncation effects.
4. **Consider alternative approaches**: Instead of fraction-based metrics, explore absolute counts or page-type-specific baselines that do not require normalization.
