# EXP-INTEL-35209112878 preregistration

## Status: DESIGN ONLY — NOT YET FROZEN

---

## 1. Experiment Identity

- **experiment_id**: EXP-INTEL-35209112878
- **lane**: intel
- **claim_ids**: C-MEAS-VALID
- **parent**: EXP-INTEL-35166505835 (handoff sha256: 2d6841990f57286921184777d179df9ec8de0facb3d855bd95a26edc8044c219)
- **created_at**: 2026-09-17

## 2. Question

Is the page-type density null model sensitive to RNG implementation, seed, conditioning set, role-count mapping, or tie-handling choices — and does the canonical analysis script reproduce the parent chain's truncated-data metrics exactly?

## 3. Hypothesis

The null model's mean pairwise agreement and C2 direction (observed vs null) are robust across RNG implementations and seeds when the recipe is fully specified.

## 4. Falsifier

- **F1**: Mean pairwise agreement across 10 seeds varies by >0.10 (SD > 0.05) across any RNG implementation
- **F2**: C2 direction flips across seeds within any single RNG implementation
- **F3**: Canonical script produces metrics differing by >0.001 from parent chain values on identical truncated input

## 5. C2 Direction Resolution

The parent chain identified a semantic contradiction in the frozen spec (audit V4 of EXP-INTEL-35137036013):

- falsifier F2: "null mean > observed -> metric fails"
- decision_rule C2: "null >= observed -> C2=true -> SURVIVES"

These are logically incompatible. Resolution grounded in EXP-INTEL-35112013458 (null 0.5275 > observed 0.3 -> FALSIFIED):

- **C2 is defined as: observed pairwise agreement > null model mean pairwise agreement**
- If C2 TRUE (observed > null): metric passes
- If C2 FALSE (observed <= null): metric fails
- Frozen decision_rule: SURVIVES requires C1 (ordering change) AND C2 (observed > null)

## 6. Null Model Recipe (Fully Specified)

### 6.1 RNG Implementations

| ID | Import | Seeding |
|----|--------|---------|
| RNG-PY | `random.Random(seed)` | `rng.seed(seed)` per iteration |
| RNG-NP-RS | `np.random.RandomState(seed)` | `rng.seed(seed)` per iteration |
| RNG-NP-DR | `np.random.default_rng(seed)` | new Generator per iteration |

### 6.2 Seeds

10 seeds: [42, 123, 456, 789, 1000, 2000, 3000, 4000, 5000, 99999]

### 6.3 Conditioning Set

- 7 tasks from truncated-first-20 locatable sample (same as parent chain)
- Role set per task: ARIA roles with >= 1 locatable element
- Observed roles: {a:16, button:22, combobox:8, div:50, form:19, input:5, label:13, span:27}; link/menuitem/tab = 0 (excluded)

### 6.4 Role-Count Mapping

For each task, `role_counts = {role: count for role, count in task.role_element_counts.items() if count > 0}`.

### 6.5 Null Draw Procedure (Per Iteration, Per Task)

1. From the task's role set, draw a random subset: for each role, include with probability proportional to its count (normalized to sum to 1 across roles), then sample without replacement a random subset size k drawn from Uniform(1, len(roles)), selecting k roles by weighted sampling without replacement.
2. Density for this null draw = sum(count[r] for r in selected_roles) / total_locatable_elements_in_task.
3. Repeat for all 7 tasks to get a null density vector.

### 6.6 Page-Type Ordering

For each definition (DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK, plus 2 additional from parent chain), compute per-page-type mean density across tasks of that type. Order page types by descending mean density. Break ties by page-type name alphabetically.

### 6.7 Pairwise Agreement

For each pair of definitions (C(5,2)=10 pairs), compare their page-type orderings. Agreement = 1 if identical top-2 ordering, 0 otherwise. Mean pairwise agreement = sum(agreements) / 10.

### 6.8 Iterations

1000 null iterations per seed per RNG. Report mean, SD, min, max of pairwise agreement across iterations.

## 7. Baselines

- **B1**: Parent observed pairwise agreement = 0.3 (EXP-INTEL-35112013458)
- **B2**: Parent null mean pairwise agreement = 0.5275 (EXP-INTEL-35112013458)

## 8. Positive Control

- **PC1**: Canonical script reproduces DEF-FULL-MAP ordering = cart > product_listing > detail
- **PC2**: Canonical script reproduces DEF-FORM-ONLY ordering = product_listing > cart > detail
- **PC3**: C2 direction on truncated data: null (0.5275) > observed (0.3) -> C2 = FALSE (metric fails)

## 9. Null Control

- **NC1**: Seed=42 with RNG-PY reproduces null mean 0.5275 +/- 0.001 on identical truncated input

## 10. Measurement Validity

1. All RNG implementations use deterministic seeding with recorded seed values
2. Canonical script committed at stable repo path before execution
3. C2 direction coherently defined (Section 5)
4. Density denominator = count of elements matching definition's role set / total locatable elements in truncated sample
5. Pairwise agreement = fraction of definition-pairs with identical top-2 page-type ordering

## 11. Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
1. PC1 passes (ordering reproduction +/- 0.001)
2. PC2 passes (C2 direction null > observed confirmed)
3. NC1 passes (seed=42 null mean 0.5275 +/- 0.001)
4. F1 not triggered (SD across seeds < 0.05 for RNG-PY)
5. F2 not triggered (C2 direction consistent across all 10 seeds for RNG-PY)
6. F3 not triggered (script metrics within +/- 0.001 of parent)

**FALSIFIED_IN_SETTING** if F1, F2, or F3 triggered.

**MEASUREMENT_INVALID** if PC1 or PC2 fails due to script bug.

## 12. Product Consequence

- **Positive**: Robust null model unblocks full-DOM enumeration experiment when runtime removes locatableSample cap
- **Negative**: Sensitive null model means recipe choice determines scientific verdict; full-DOM experiment blocked until recipe redesigned or metric replaced

## 13. Stable Metric Identifiers (for downstream transmission)

- `M1_MEAN_PAIRWISE_AGREEMENT`: Mean pairwise agreement across 1000 null iterations
- `M2_SD_PAIRWISE_AGREEMENT`: SD of pairwise agreement across iterations
- `M3_OBSERVED_PAIRWISE_AGREEMENT`: Observed pairwise agreement on actual data (0.3)
- `M4_C2_DIRECTION`: Boolean, True if observed > null_mean
- `M5_C1_ORDERING_CHANGED`: Boolean, True if page-type ordering differs across definitions
- `M6_SCRIPT_REPRODUCTION_ERROR`: Max absolute difference between script output and parent values

## 14. Stable Control Identifiers

- `C_POSITIVE_ORDERING_REPRODUCTION`: PC1
- `C_NULL_MODEL_REGRESSION`: NC1
- `C_RECIPE_SENSITIVITY`: F1/F2
- `C_PROVENANCE_MATCH`: F3
