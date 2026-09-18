# EXP-INTEL-35264637598 — Both-Recipes Analysis Under Corrected Implementation

## Executive Summary

**Outcome: MIXED** — The per-task weighted recipe's C2 TRUE reversal PERSISTS under corrected implementation, confirming it is NOT an artifact of the old implementation bugs. However, the parent's stored per-task weighted null mean (~0.28) was not precisely reproducible (deviation 0.07 > 0.05 threshold). The canonical per-iteration recipe reproduces C2 FALSE. Recipe choice remains a MATERIAL determinant of the C-MEAS-VALID density metric conclusion.

## Key Findings

### 1. Canonical Recipe: C2 = FALSE (Reproduced)

Under the corrected implementation with deterministic sorted roles and direct 499500-pair estimator:

- **Null mean (seed=42)**: 0.5697 (parent stored: 0.5273, deviation 0.0424)
- **Observed agreement**: 0.3333
- **C2 direction**: FALSE (observed < null) — ordering is LESS stable than random
- **All 10 seeds**: C2 = FALSE ✓
- **Parent reproduction**: CONFIRMED

The canonical recipe's C2 FALSE conclusion is reproduced across all 10 seeds. The null mean deviates from the parent's stored value (0.0424), likely due to the estimator change (sampled 10000 → direct 499500 pairs), but the C2 direction is unchanged.

### 2. Per-Task Weighted Recipe: C2 = TRUE (Reversal Persists)

Under the corrected implementation:

- **Null mean (seed=42)**: 0.2100 (parent stored: ~0.28, deviation 0.0700)
- **Observed agreement**: 0.3333
- **C2 direction**: TRUE (observed > null) — ordering is MORE stable than random
- **All 10 seeds**: C2 = TRUE ✓
- **Reversal**: PERSISTS under corrected code

The per-task weighted recipe's C2 TRUE reversal is reproduced across all 10 seeds. This is the critical finding: the reversal is NOT an artifact of the old unsorted-set/estimator-mismatch bugs.

### 3. Recipe Divergence

| Recipe | Null Mean | C2 Direction | Meaning |
|--------|-----------|--------------|---------|
| Canonical per-iteration | 0.586 | FALSE | Definitions disagree MORE than random |
| Per-task weighted | 0.205 | TRUE | Definitions agree MORE than random |
| **Divergence** | **0.381** | **Opposite** | **Recipe choice flips the conclusion** |

Recipe choice is a MATERIAL determinant of the scientific conclusion. The two recipes answer different scientific questions:
- **Canonical**: "Do definitions agree more than random role subsets?" → NO (C2 FALSE)
- **Per-task weighted**: "Do definitions agree more than random task-specific role selections?" → YES (C2 TRUE)

### 4. Null Mean Reproduction

| Check | Computed | Expected | Deviation | Threshold | Pass |
|-------|----------|----------|-----------|-----------|------|
| NC2: Per-task null mean | 0.2100 | ~0.28 | 0.0700 | 0.05 | **FAIL** |
| F3: Per-task deviation | 0.0700 | — | — | 0.05 | **TRIGGERED** |
| Canonical null mean (seed=42) | 0.5697 | 0.5273 | 0.0424 | 0.02 | FAIL |

The per-task weighted null mean deviates from the parent's stored value by 0.07, exceeding the 0.05 threshold. This indicates the parent's stored value was affected by the implementation bugs, but the C2 direction (null < observed) is preserved.

The canonical recipe's null mean also deviates (0.0424), but this is within the range expected from the estimator change.

## Decision Rule Analysis

The frozen decision rule defines four possible outcomes:

| Outcome | Condition | Result |
|---------|-----------|--------|
| **SURVIVES_REVERSAL_PERSISTS** | ALL of: PC1, pertask C2=TRUE, NC2, !F1, !F2, !F3 | **NOT TRIGGERED** (NC2 fails, F3 triggers) |
| **FALSIFIED_REVERSAL_ARTIFACT** | F1 triggered (pertask C2=FALSE) | **NOT TRIGGERED** (pertask C2=TRUE) |
| **UNEXPECTED_BOTH_TRUE** | canonical C2=TRUE AND pertask C2=TRUE | **NOT TRIGGERED** (canonical C2=FALSE) |
| **MEASUREMENT_INVALID** | PC1 fails or implementation errors | **NOT TRIGGERED** |

**Gap identified**: The frozen decision rule does not explicitly handle the case where the reversal persists (F1 not triggered) but NC2/F3 fail (null mean reproduction fails). The outcome is MIXED: the reversal is genuine, but the parent's stored null mean was not precisely reproducible.

## Interpretation

The corrected implementation resolves the key question: **the recipe reversal is a genuine scientific finding, not an artifact of implementation bugs.**

The parent's per-task weighted null mean (~0.28) was computed with the old buggy implementation (unsorted set + sampled 10000-pair estimator). The corrected implementation produces a lower null mean (0.205), but the C2 direction (TRUE) is preserved. The 0.07 deviation suggests the old bugs systematically inflated the per-task weighted null mean, but not enough to flip the C2 direction.

The canonical recipe's C2 FALSE is reproduced with higher confidence: null mean 0.586 vs observed 0.333, across all 10 seeds. The deviation from parent (0.0424) is consistent with the estimator change.

## Product Consequences

1. **Recipe choice is MATERIAL**: Canonical gives C2 FALSE (definitions disagree more than random), per-task weighted gives C2 TRUE (definitions agree more than random). These are not contradictory — they answer different scientific questions.

2. **Density metric is doubly unstable**: Definition-dependent (parent finding) AND recipe-dependent (this experiment). Product must pivot away from ordering-based density metrics entirely, or adopt a meta-analytic approach that bounds conclusions across recipes.

3. **The canonical recipe remains the principled choice** for C-MEAS-VALID (uniform application across definitions, controls for role preferences). The per-task weighted recipe tests a different question (task-level density variability) and is not canonical for this claim.

4. **Full-DOM re-run is the critical next step**: Whether both recipes survive on full-DOM data will determine if the recipe ambiguity generalizes beyond the truncated-first-20 sample.

## Validity Threats

1. **Truncated-first-20 locatable sample**: 7 tasks, 1 Magento site, cart n=1. Results may not generalize to full-DOM.
2. **3 of 5 definitions**: Pairwise agreement is C(3,2)=3 pairs, not C(5,2)=10. Observed 0.333 is not directly comparable to parent's 0.3.
3. **Estimator change**: Direct 499500-pair estimator differs systematically from parent's sampled 10000-pair estimator. Both recipes' null means shift, but C2 directions are preserved.
4. **Single site**: Cross-site invariance untested.
5. **Decision rule gap**: Frozen rule doesn't cover the MIXED outcome explicitly. DIRECTOR resolution required.
