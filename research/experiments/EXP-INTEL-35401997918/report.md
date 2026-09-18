# EXP-INTEL-35401997918 Report

## Experiment Summary

**Question**: Does a structurally non-linear third recipe (DOM hierarchy-depth weighting with exponential decay) produce density rankings outside the canonical-weighted convex hull, thereby breaking the 2-recipe degeneracy that blocks MIXED outcome resolution?

**Verdict**: FALSIFIED-IN-SETTING — The hierarchy-weighted density recipe fails on C4 (task-type structure: eta²=0.000 < 0.10). While C1-C3 pass, the recipe produces zero discrimination across page types, making it useless for the MIXED decision rule.

## Decision Rule Evaluation

| Condition | Criterion | Value | Threshold | Pass? |
|-----------|-----------|-------|-----------|-------|
| C1 | CV(hierarchy_density) ≥ 0.10 | 0.584 | 0.10 | ✅ |
| C2 | ≥3 pairs outside convex hull | 7/21 | 3 | ✅ |
| C3 | \|ρ(hier, canon)\| < 0.90 OR \|ρ(hier, weight)\| < 0.90 | 0.879 | 0.90 | ✅ |
| C4 | η²(hierarchy_density, page_type) ≥ 0.10 | 0.000 | 0.10 | ❌ |

**Verdict rule**: C1 AND C2 AND C3 AND NOT C4 → **FALSIFIED-IN-SETTING**

## Key Findings

### 1. The Hierarchy Recipe Is a Monotonic Reparameterization of Weighted Density

The most important finding is that the hierarchy-weighted density produces a **perfect monotonic transformation** of the weighted density (Spearman ρ = 1.0 at α=0.3). This means:

- The hierarchy recipe does NOT introduce a structurally different ranking
- It reparameterizes the existing weighted ranking by shifting absolute values
- All hull-breaking pairs (7/21) are ISOLATED-A-LINK, where hierarchy upweights shallow non-form elements

The mechanism is straightforward: the depth estimation heuristic uses `inForm` (a binary attribute) as the primary depth proxy. Since all 20 locatable_sample elements have the same `inForm` distribution across all tasks, the depth distribution is task-invariant. The hierarchy recipe therefore preserves the weighted ranking while adding noise from the binary depth signal.

### 2. Hull-Breaking Is Definition-Dependent, Not Task-Type-Dependent

All 7 hull-breaking pairs are ISOLATED-A-LINK (the most restrictive definition, 1-3 matching elements). For DEF-FULL-MAP (20 elements) and DEF-FORM-ONLY (17-19 elements), hierarchy density is always between canonical and weighted.

The hull-breaking occurs because hierarchy upweights shallow non-form elements (nav links, action buttons at depth 1-2) that have minimal area in the weighted recipe. For ISOLATED-A-LINK, these shallow elements constitute a larger fraction of the matching set, amplifying the hierarchy weighting effect.

### 3. Zero Task-Type Structure at All Alpha Values

η²(hierarchy_density, page_type) = 0.0 at ALL tested alpha values (0.1, 0.3, 0.5). The three page types have identical mean hierarchy density (listing = detail = cart = 0.667).

This is because:
- The locatable_sample contains a fixed set of 20 elements per task
- The element composition (tag distribution, inForm distribution) is nearly identical across tasks
- The depth estimation is based on inForm (binary), not on actual DOM nesting structure
- Therefore, the hierarchy weighting is task-invariant

### 4. Random Weights Show Equivalent Structure

The NC1 null control shows that random [0,1] weights produce nearly identical correlation structure to hierarchy weights:
- Random mean|ρ(rand, canon)| = 0.877 vs |ρ(hier, canon)| = 0.879
- Random mean|ρ(rand, weight)| = 0.978 vs |ρ(hier, weight)| = 1.000

The hierarchy recipe does not produce more systematic structure than random weights.

## Comparison with Prior Work

| Recipe | Mean density | η²(page_type) | Hull breaks | ρ(weighted) |
|--------|-------------|---------------|-------------|-------------|
| B1: Canonical | 0.005 | — | — | — |
| B2: Weighted | 0.667 | 0.000 | 0 | 1.0 |
| B3: Linear mean | 0.336 | 0.000 | 0 | 0.984 |
| B4: Density ratio | — | 0.144 | — | — |
| Hierarchy (α=0.3) | 0.667 | **0.000** | **7** | **1.0** |

The hierarchy recipe adds hull-breaking capability (7 pairs vs 0 for linear mean) but provides zero task-type discrimination (η²=0.0 vs 0.144 for density ratio). The density ratio from EXP-INTEL-35375593989 had the best task-type structure (η²=0.144) but was falsified for other reasons (definition-driven variation, non-significant task-type correlation).

## Product Consequence

**Negative**: The MIXED outcome program cannot use DOM hierarchy-weighted density as a third recipe. The recipe breaks the convex hull (C2 passes) but provides no task-type discrimination (C4 fails). The remaining options for the MIXED program are:

1. **Abandon density-based MIXED handling entirely** — restrict to recipe-insensitive task-definition pairs only
2. **Accept that density metric recipe sensitivity is irreducible** — the 31x canonical/weighted gap makes dominance-based approaches fundamentally unworkable within the OECD/COINr framework
3. **Test with TRUE DOM tree depth** — the current negative result applies to the heuristic depth estimation (inForm-based), not to genuine DOM tree structure. A future experiment could use complete DOM tree data with parent-child links to compute actual depth values.

## Validity Threats

1. **Depth estimation is heuristic, not structural**: The locatable_sample is a flattened list without parent-child links. Depth is inferred from tag type and inForm flag, providing at most 4 distinct levels. True DOM depth could range from 2 to 20+.

2. **Fixed sample size eliminates depth variation**: All tasks have exactly 20 elements in the locatable_sample, so any depth-distribution variation from different DOM sizes is suppressed.

3. **Single site, single sample**: Results are bounded to 1 Magento site with truncated-first-20 sampling. Full DOM enumeration might change density values.

4. **The negative result is bounded to the heuristic depth estimation**: The theoretical possibility that genuine DOM depth information could break the degeneracy remains untested.

## Conclusion

The hierarchy-weighted density recipe fails to produce a viable third recipe for the MIXED decision rule. While it breaks the convex hull (a mathematical consequence of upweighting shallow non-form elements), it provides zero task-type discrimination (η²=0.0 at all alpha values). The recipe is effectively a monotonic reparameterization of weighted density (Spearman ρ=1.0), not a structurally different recipe.

This experiment, combined with prior failures of linear combinations (EXP-INTEL-35353016702) and density ratios (EXP-INTEL-35375593989), demonstrates that **no tested density-based recipe can resolve the MIXED outcome decision rule** within the OECD/COINr framework. The 31x canonical/weighted gap makes all recipes either degenerate (linear combinations), definition-driven (density ratio), or task-invariant (hierarchy weighting).

The MIXED outcome program should either be abandoned or restricted to recipe-insensitive task-definition pairs.
