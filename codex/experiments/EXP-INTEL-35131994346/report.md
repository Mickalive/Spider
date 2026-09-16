# EXP-INTEL-35131994346: Reconstruction of 3-Definition Per-Role-Filtered Analysis

## Executive Summary

This experiment resolves the provenance mismatch between the committed `analyze.py` and stored `analysis_results.json` from EXP-INTEL-35124660457. The reconstruction succeeds partially:

- **DEF-FULL-MAP**: ✅ Perfect reconstruction (all metrics match stored results)
- **DEF-FORM-ONLY**: ✅ Perfect reconstruction (all metrics match stored results)  
- **ISOLATED-A-LINK**: ❌ **Bug found** — stored results are identical to DEF-FULL-MAP (copy-paste error)

**Verdict**: MIXED — provenance partially resolved, but stored ISOLATED-A-LINK results are invalid.

## Key Findings

### 1. The Uncommitted Script Was Successfully Reconstructed

The uncommitted script that produced the stored `analysis_results.json` can be reconstructed from the raw evidence using:

1. **Deduplication**: Remove duplicate `cart_1` (8→7 tasks)
2. **Per-definition role filtering**: 
   - DEF-FULL-MAP: a + button + input + combobox
   - DEF-FORM-ONLY: button + combobox
   - ISOLATED-A-LINK: a only
3. **Density calculation**: Count roles matching definition in truncated sample, divide by `elements_with_bbox`
4. **Full-DOM estimation**: Use DOM tag counts for a/button/form/input, scale sample counts for other roles

The reconstruction is exact for DEF-FULL-MAP and DEF-FORM-ONLY (densities match within floating-point tolerance).

### 2. ISOLATED-A-LINK Has a Critical Bug

The stored `analysis_results.json` contains identical values for DEF-FULL-MAP and ISOLATED-A-LINK:

| Task | DEF-FULL-MAP truncated_count | ISOLATED-A-LINK truncated_count |
|------|------------------------------|--------------------------------|
| listing_clothing | 8 | 8 (should be 2) |
| listing_beauty | 8 | 8 (should be 2) |
| detail_camera | 5 | 5 (should be 2) |

ISOLATED-A-LINK should count only `a` elements (truncated_count=2 for listing tasks), but stored results count all DEF-FULL-MAP roles (truncated_count=8). This is a copy-paste error.

### 3. Committed Script vs Stored Results

| Metric | Committed `analyze.py` | Stored `analysis_results.json` |
|--------|------------------------|--------------------------------|
| Tasks | 8 (cart_1 duplicated) | 7 (deduplicated) |
| Density | All roles | Per-definition filtered |
| C1 (ordering changed) | True | True |
| C2 (≥2 tasks >20% bias) | 8/8 | 7/7 |
| C3 (random baseline lower) | False | True (DEF-FULL-MAP) |
| Decision | FALSIFIED-IN-SETTING | SURVIVES_CURRENT_TEST |

The committed script uses all-role density (denominator includes all interactive elements), while the uncommitted script filters by definition. This changes C3: all-role density makes random and truncation biases similar, while per-definition filtering shows truncation bias exceeds random for DEF-FULL-MAP.

### 4. Root Cause of Verdict Difference

The committed script's `C3=false` occurs because:
- All-role density sums a+button+form+input+combobox+div+label+span
- This inflates the denominator, making random and truncation biases similar
- Per-definition filtering (e.g., DEF-FULL-MAP) excludes non-target roles, revealing that truncation bias exceeds random sampling bias

## Implications for Parent Experiment

### If Provenance Partially Resolved (Current State)

- The committed script is **not** the correct analysis — it uses a different algorithm
- The stored results have a bug in ISOLATED-A-LINK but are correct for DEF-FULL-MAP and DEF-FORM-ONLY
- The parent experiment's FALSIFIED verdict from EXP-INTEL-35112013458 should be re-evaluated using:
  - 7 deduplicated tasks (not 8)
  - Per-definition role filtering
  - The correct ISOLATED-A-LINK values (a-only, not all-role)

### Recommended Actions

1. **Update committed `analyze.py`** to:
   - Deduplicate cart_1 (keep first occurrence)
   - Implement 3-definition role filtering
   - Run all definitions and report per-definition verdicts
   - This eliminates the provenance mismatch permanently

2. **Mark stored ISOLATED-A-LINK results as exploratory** — the bug means those specific values are unreliable

3. **Re-run parent experiment** with corrected script to get valid FALSIFIED/SURVIVES verdicts per definition

## Measurement Validity

- ✅ Raw evidence from EXP-INTEL-34782350557 is accessible and intact
- ✅ Committed `analyze.py` is runnable and produces stable output
- ✅ Stored `analysis_results.json` is structurally valid (3 definitions, 7 tasks)
- ✅ Reconstruction is documented step-by-step with intermediate artifacts
- ⚠️ ISOLATED-A-LINK in stored results is invalid (identical to DEF-FULL-MAP)

## Scope and Limitations

This experiment:
- ✅ Resolves the provenance mismatch for DEF-FULL-MAP and DEF-FORM-ONLY
- ✅ Identifies the bug in ISOLATED-A-LINK
- ✅ Confirms the uncommitted script's algorithm can be reconstructed
- ❌ Does not resolve the substrate fix needed for full DOM enumeration
- ❌ Does not change the claim status of C-CROSSSITE or C-LLM-INHERIT
