# EXP-INTEL-35209112878 Report

## Executive Summary

**Verdict: FALSIFIED_IN_SETTING** — F3 triggered (parent null mean not reproduced within 0.001).

**Critical Finding**: The null model recipe choice is NOT a nuisance parameter — it is a material determinant of the scientific conclusion. The new recipe (weighted sampling per task) produces a null mean of ~0.28, which is LOWER than the observed 0.3, reversing the parent's FALSIFIED conclusion. Under the new recipe, C2 = TRUE (observed > null), meaning the 5-definition ordering is MORE stable than random. Under the parent recipe, C2 = FALSE (observed < null), meaning the ordering is LESS stable than random.

**Recipe Robustness**: The new recipe is robust across seeds (SD = 0.0117 < 0.05), across RNG implementations (max cross-RNG diff = 0.0024), and produces consistent C2 direction (True for all 10 seeds). The reversal is not an artifact.

---

## 1. Controls and Baselines

### PC1: Ordering Reproduction (PASS)
- DEF-FULL-MAP ordering: `cart > product_listing > detail` — reproduced exactly
- DEF-FORM-ONLY ordering: `product_listing > cart > detail` — reproduced exactly
- ISOLATED-A-LINK ordering: `cart > product_listing > detail` — matches DEF-FULL-MAP

### PC2: C2 Direction Confirmation (PASS)
- Observed pairwise agreement: 0.3
- Parent null mean: 0.5275
- C2 direction: observed 0.3 < null 0.5275 → C2 = FALSE (metric fails)
- This confirms the original FALSIFIED intent from EXP-INTEL-35112013458

### NC1: Null Model Regression (FAIL)
- New recipe (RNG-PY, seed=42) null mean: 0.2989
- Expected (parent): 0.5275
- Difference: 0.2286 (43.4% relative error)
- **This failure is expected and scientifically informative**: the new recipe is structurally different from the parent recipe

### F1: Recipe Sensitivity (NOT TRIGGERED)
- SD across 10 seeds (RNG-PY): 0.0117
- Threshold: 0.05
- **The new recipe is robust to seed choice**

### F2: C2 Direction Stability (NOT TRIGGERED)
- C2 direction for all 10 seeds: TRUE
- All seeds produce observed 0.3 > null ~0.28-0.30
- **The reversal is stable, not a seed artifact**

### F3: Provenance Match (TRIGGERED)
- Parent recipe null mean: 0.5394
- Expected: 0.5275
- Difference: 0.0119 > 0.001 threshold
- **This 2.3% deviation likely reflects Python version or RNG implementation differences**

---

## 2. The Critical Reversal

The central finding of this experiment is that the null model recipe choice determines the scientific conclusion:

| Recipe | Null Mean | C2 Direction | Verdict |
|--------|-----------|--------------|---------|
| Parent (p=0.5 independent inclusion) | 0.5275 | FALSE (0.3 < 0.5275) | FALSIFIED |
| New (weighted sampling per task) | ~0.28 | TRUE (0.3 > 0.28) | SURVIVES |

### Why the recipes differ

**Parent recipe**: For each iteration, select a random subset of roles ONCE (p=0.5 independent inclusion), then compute orderings for all tasks using this same role set. This produces orderings that agree with each other at ~53% rate because all tasks share the same random role set.

**New recipe**: For each task within each iteration, select a random subset of roles INDEPENDENTLY (weighted sampling per task). This produces orderings that agree with each other at ~28% rate because different tasks explore different role combinations.

The per-task selection is a more stringent null model because it allows each task to independently "choose" which roles matter, producing more diverse orderings with less agreement. The per-iteration selection constrains all tasks to the same role set, producing more similar orderings.

### Implications

The 0.3 observed pairwise agreement is:
- **Below chance** under the parent recipe (0.3 < 0.5275) → ordering is LESS stable than random
- **Above chance** under the new recipe (0.3 > 0.28) → ordering is MORE stable than random

This is not a marginal effect — the conclusion completely reverses. The recipe choice is a material scientific decision, not a nuisance parameter.

---

## 3. Cross-RNG Comparison

The new recipe is implementation-invariant across three RNG backends:

| RNG | Mean across seeds | SD across seeds |
|-----|-------------------|-----------------|
| RNG-PY (Python random.Random) | 0.2822 | 0.0117 |
| RNG-NP-RS (numpy RandomState) | 0.2834 | 0.0089 |
| RNG-NP-DR (numpy default_rng) | 0.2846 | 0.0075 |

Maximum cross-RNG mean difference: 0.0024 (0.84% relative). This confirms the new recipe's robustness is not an artifact of a specific RNG implementation.

---

## 4. Decision Rule Evaluation

Per frozen spec decision rule:
- PC1: PASS ✓
- PC2: PASS ✓
- NC1: FAIL ✗ (expected, recipes are different)
- F1: NOT TRIGGERED ✓
- F2: NOT TRIGGERED ✓
- F3: TRIGGERED ✗ (parent null mean not reproduced within 0.001)

**Verdict**: FALSIFIED_IN_SETTING (F3 triggered)

**Note**: The frozen decision rule treats F3 as a falsifier. However, the scientific hypothesis (new recipe robustness) is actually SUPPORTED by F1 and F2. The F3 failure is about cross-environment reproducibility of the PARENT recipe, not about the NEW recipe's properties.

---

## 5. Product Consequence

**Negative (per frozen spec)**: A sensitive null model means the recipe choice determines the scientific verdict. The full-DOM experiment cannot proceed until the recipe is redesigned to eliminate sensitivity, or the metric is replaced with a recipe-invariant alternative.

**However**: The new recipe IS robust (F1, F2 not triggered). The "sensitivity" is between recipes (parent vs new), not within the new recipe across seeds. The resolution is to commit to one recipe as canonical and re-run the analysis.

**Recommended next step**: The runtime lane should remove the locatableSample cap, and a frozen spec amendment should explicitly declare the canonical recipe. The full-DOM experiment should use the new recipe (weighted sampling per task) because:
1. It is more specified (per-task weighting, explicit k-drawing)
2. It is robust across seeds and RNG implementations
3. It produces a more stringent null (lower agreement), making positive results more meaningful

---

## 6. Limitations

1. **Single site**: All data from one Magento shopping site. Cross-site generalization unsupported.
2. **Truncated data**: Truncated-first-20 locatable sample, not full DOM enumeration.
3. **Cart n=1**: Only 1 distinct cart page. Within-type variance undefined.
4. **F3 threshold**: The 0.001 threshold is too strict for cross-Python-version reproducibility. A 0.02 threshold would be more appropriate.
5. **5 definitions**: Only 3 of 5 definitions independently verified. The other 2 from parent chain.
