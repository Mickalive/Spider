# EXP-INTEL-35112013458 Report: Null Models for Truncated-Sample Pairwise Ordering Agreement

## Executive Summary

**Verdict: FALSIFIED-IN-SETTING**

Three preregistered null-model tests on truncated-sample pairwise ordering agreement:

1. **Random ROLE_MAP null (1000 iterations)**: The observed 0.3 pairwise agreement does NOT exceed chance. Null mean = 0.5275, 95th percentile = 1.0. The observed 0.3 is actually BELOW the null mean.

2. **Single-role definitions**: Two single-role definitions (button-only, form-only) produce the same ordering as DEF-FORM-ONLY (product_listing>cart>detail), violating the expectation that no single role drives the metric.

3. **Isolated a→link**: CONFIRMED. A definition with a→link mapping but WITHOUT menuitem/tab produces the same ordering as DEF-FULL-MAP (cart>product_listing>detail). The a→link effect is isolated and sufficient.

**Conclusion**: The truncated-sample ordering stability finding (0.3 pairwise agreement) does not exceed chance-level expectation. The null model reveals that random role assignments produce higher pairwise agreement than the 5-definition family. However, the a→link reversal mechanism is confirmed as isolated and sufficient.

## 1. Test 1: Random ROLE_MAP Null

### Procedure
- 8 raw roles present in data: {a, button, combobox, div, form, input, label, span}
- For each of 1000 iterations (seed=42): randomly assign each role to interactive/not with p=0.5
- Compute ordering for each random assignment
- Compute pairwise agreement across all 1000 orderings

### Results
| Metric | Value |
|--------|-------|
| Null mean pairwise agreement | 0.5275 |
| Null 95th percentile | 1.0 |
| Observed agreement | 0.3 |
| Exceeds null mean | **No** |
| Exceeds null 95th percentile | **No** |
| Unique orderings in null | 5 |
| Top ordering | cart>detail>product_listing (70.2%) |

### Interpretation
The null distribution is dominated by `cart>detail>product_listing` (70.2% of random assignments). The observed 0.3 pairwise agreement is BELOW the null mean (0.5275), meaning the 5-definition family ordering is LESS stable than random. This falsifies the hypothesis that 0.3 exceeds chance.

**Why is the null mean so high?** Random role assignments tend to produce similar orderings because:
- Most roles are evenly distributed across page types
- The `a` role (16 elements) is the only one with strong differential distribution
- Random inclusion/exclusion of most roles doesn't change ordering much
- The 5-definition family is intentionally diverse (spanning form-only to full-map)

## 2. Test 2: Single-Role Definitions

### Results
| Role | Ordering | Total Elements | Matches Parent | Degenerate |
|------|----------|----------------|----------------|------------|
| a | cart>detail>listing | 16 | No | No |
| button | **listing>cart>detail** | 22 | **Yes** | No |
| combobox | cart>detail>listing | 8 | No | No |
| div | detail>cart>listing | 50 | No | No |
| form | **listing>cart>detail** | 19 | **Yes** | No |
| input | cart>detail>listing | 5 | No | No |
| label | cart>detail>listing | 13 | No | No |
| link | listing>detail>cart | 0 | No | **Yes** |
| menuitem | listing>detail>cart | 0 | No | **Yes** |
| span | cart>detail>listing | 27 | No | No |
| tab | listing>detail>cart | 0 | No | **Yes** |

### Key Findings
- **8 non-degenerate roles** produce **3 unique orderings**
- **button-only** and **form-only** both produce `product_listing>cart>detail` (matching DEF-FORM-ONLY)
- This violates the expectation that "no single role drives the metric"
- The `div` role produces a different ordering (`detail>cart>product_listing`), suggesting div density is higher on detail pages

### Interpretation
The button-only and form-only orderings match the parent family, suggesting the `product_listing>cart>detail` ordering may be driven by form elements rather than multi-role interaction. However, the sample is too small (7 tasks, 3 page types) to draw definitive conclusions.

## 3. Test 3: Isolated a→link Definition

### Definition
```
INTERACTIVE_ROLES: {button, link, textbox, checkbox, radio, combobox, listbox, slider, spinbutton, searchbox, switch}
ROLE_MAP: {"a": "link", "input": "textbox"}
(Note: menuitem and tab excluded)
```

### Results
| Definition | Ordering | Means |
|------------|----------|-------|
| DEF-ISOLATED-A-LINK | cart>product_listing>detail | listing=0.00513, detail=0.00428, cart=0.00561 |
| DEF-FULL-MAP | cart>product_listing>detail | listing=0.00513, detail=0.00428, cart=0.00561 |
| DEF-FORM-ONLY | product_listing>cart>detail | listing=0.00385, detail=0.00171, cart=0.00280 |

**Isolated a→link is IDENTICAL to DEF-FULL-MAP** (both ordering and means).

### Interpretation
The a→link mapping alone is sufficient to produce the cart>listing>detail reversal. Menuitem and tab (both = 0 in this sample) do not contribute. The reversal is driven by:
- a→link mapping inflates cart density: cart has 2 `a` elements that get mapped to `link`, while listing has 2 `a` elements but 3x more total elements, diluting the effect
- The differential inflation is: cart +33% (0.00280→0.00561), listing +33% (0.00385→0.00513), but the absolute cart increase (0.00281) exceeds listing increase (0.00128), causing the reversal

## 4. Decision Rule Evaluation

| Condition | Required | Observed | Pass |
|-----------|----------|----------|------|
| 1. Null confirms significance | Null mean < 0.3 AND observed > p95 | Null mean = 0.5275, observed < null mean | **FAIL** |
| 2. No single-role invariant | No single-role matches parent | button and form match parent | **FAIL** |
| 3. Isolated a→link matches DEF-FULL-MAP | Ordering = cart>listing>detail | Ordering = cart>listing>detail | **PASS** |

**Verdict: FALSIFIED-IN-SETTING** (2 of 3 conditions fail)

## 5. Implications

### For Product Lane
- The truncated-sample ordering stability finding (0.3 pairwise agreement) is NOT statistically significant
- The `product_listing>cart>detail` ordering under DEF-FORM-ONLY may be noise, not a robust signal
- The a→link reversal mechanism is confirmed but bounded to this truncated sample
- **Recommendation**: Do not adopt DEF-FORM-ONLY as canonical metric based on this ordering alone

### For Runtime Lane
- The a→link mapping is the dominant sensitivity driver (confirmed)
- The locatableSample cap needs to be fixed before metric validation can proceed
- Full DOM enumeration needed to assess true ordering

### For Intel Lane
- The null model result (0.5275 > 0.3) is surprising and warrants investigation
- The question "does 0.3 exceed chance?" may need reframing to "is the specific ordering stable under constrained definition families?"
- Cross-site validation needed

## 6. Validity Threats

1. **Small sample**: 7 tasks, 3 page types. Low statistical power.
2. **Single site**: All data from one Magento shopping site.
3. **Cart pseudoreplication**: Cart n=1 distinct, within-type variance undefined.
4. **Null model assumptions**: Independent inclusion/exclusion with p=0.5 is more diverse than real definitions.
5. **Truncated sample**: First-20 cap may cause ordering artifacts.
6. **Missing roles**: link=0, menuitem=0, tab=0 in sample; their contributions cannot be assessed.
