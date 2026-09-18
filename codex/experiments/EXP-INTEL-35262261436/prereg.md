# EXP-INTEL-35262261436 Preregistration

## Status: DESIGN — NOT YET FROZEN

---

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35262261436
- **Lane**: intel
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Parent**: EXP-INTEL-35209112878 (MEASUREMENT_INVALID — decision rule incoherent)
- **Parent Handoff**: `research/experiments/EXP-INTEL-35209112878/handoff.json`

## 2. Scientific Question

With a corrected implementation (deterministic sorted roles, aligned estimator, coherent decision rule), does the canonical per-iteration p=0.5 null recipe reproduce the parent FALSIFIED result (C2 FALSE: observed 0.3 < null ~0.53) on truncated-first-20 data?

This converts the MEASUREMENT_INVALID verdict (design failure) into a coherent scientific verdict.

## 3. Background and Motivation

The page-type density metric measures whether different definitions of "interactive element" produce consistent orderings of page types by density. Four parent experiments (EXP-INTEL-35112013458 through EXP-INTEL-35209112878) have produced contradictory results due to:

1. **Recipe sensitivity** (EXP-INTEL-35209112878): The null model recipe choice reverses C2 direction — parent recipe yields C2 FALSE (FALSIFIED), new recipe yields C2 TRUE (SURVIVES). The recipe is material, not a nuisance parameter.

2. **Decision rule incoherence** (audit V2): NC1 requires cross-recipe equivalence that is structurally impossible, making SURVIVES logically unachievable.

3. **Implementation bugs** (audit V1): Unsorted set iteration + PYTHONHASHSEED + estimator mismatch prevent reproducible parent null mean reproduction (0.0119 deviation > 0.001 threshold).

The parent handoff recommends: "prepare a frozen spec amendment that specifies the canonical null recipe with principled justification, fixes the decision rule incoherence, commits deterministic role sorting and aligned metric definitions."

## 4. Canonical Null Recipe Selection

**Adopted: Per-iteration p=0.5 independent inclusion with deterministic sorted roles.**

### Justification

The two candidate recipes test different scientific questions:

| Recipe | Null Question | Null Mean | C2 Direction |
|--------|--------------|-----------|--------------|
| Per-iteration p=0.5 (parent) | Do definitions agree more than random role subsets applied uniformly? | 0.5275 | FALSE (0.3 < 0.5275) |
| Per-task weighted (new) | Do definitions agree more than random task-specific role selections? | ~0.28 | TRUE (0.3 > 0.28) |

**The per-iteration recipe is scientifically canonical for this claim because:**

1. **Uniform application**: The 5 definitions (DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK, etc.) are fixed properties applied uniformly across all tasks. The null should reflect this uniformity — random role subsets applied once per iteration to all tasks.

2. **Controls for role preferences**: Definitions have inherent role preferences (DEF-FULL-MAP includes link/menuitem/tab; DEF-FORM-ONLY excludes them). The per-iteration null controls for these preferences by randomizing the role subset while keeping it shared.

3. **Tests the right question**: "Is the observed agreement (0.3) higher than what random role subsets produce?" is the question for C-MEAS-VALID. The per-iteration null answers this directly.

4. **The per-task recipe tests a different question**: "Is the observed agreement higher than random task-specific role selections?" This is a valid question but not the one for C-MEAS-VALID. The per-task recipe introduces task-level variation that conflates definition stability with task heterogeneity.

5. **The per-iteration null's higher agreement (0.5275) is informative**: It reveals that random role subsets applied uniformly produce MORE agreement than the observed 0.3, meaning the definitions actually disagree more than random. This is a genuine scientific finding, not a measurement artifact.

### Implementation Fix

The parent recipe's implementation had two bugs:
- `get_all_raw_roles()` returns a `set` and iterates without sorting → PYTHONHASHSEED nondeterminism
- Parent stored value used sampled 10000-pair estimator; canonical uses direct 499500-pair estimator

**Fix**: `sorted(raw_roles)` before sampling, and direct estimator consistently.

## 5. Hypothesis

**H1 (primary)**: Under the canonical per-iteration recipe with corrected implementation, C2 = FALSE (observed 0.3 < null mean), reproducing the parent's FALSIFIED conclusion.

**H0 (null)**: C2 = TRUE (observed 0.3 > null mean), reversing the parent's conclusion.

## 6. Falsification Criteria

| ID | Condition | Threshold | Meaning |
|----|-----------|-----------|---------|
| F1 | C2 direction | C2 = TRUE | Original FALSIFIED was wrong — ordering IS more stable than random |
| F2 | Parent null mean reproduction | >0.02 deviation from 0.5275 | Parent's stored value unreliable even after fixes |
| F3 | Seed robustness | SD across 10 seeds >0.05 | Recipe too sensitive for reproducible conclusions |

## 7. Controls

### Positive Controls

| ID | Test | Expected |
|----|------|----------|
| PC1a | DEF-FULL-MAP ordering | cart > product_listing > detail |
| PC1b | DEF-FORM-ONLY ordering | product_listing > cart > detail |
| PC2 | C2 direction under canonical recipe | FALSE (observed 0.3 < null >0.5) |

### Null Controls

| ID | Test | Expected |
|----|------|----------|
| NC1 | Parent null mean reproduction | Within 0.02 of stored 0.5275 |

### Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B1 | Parent orderings reproduced exactly | Deterministic match |
| B2 | Corrected null mean | Within 0.02 of 0.5275 |
| B3 | Seed SD | <0.05 |

## 8. Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
1. PC1a AND PC1b pass (orderings reproduced exactly)
2. PC2 passes (C2 = FALSE under canonical recipe)
3. NC1 passes (parent null mean within 0.02 of stored 0.5275)
4. F1 not triggered (C2 is FALSE, not TRUE)
5. F2 not triggered (null mean within 0.02)
6. F3 not triggered (SD <0.05)

**FALSIFIED_IN_SETTING** if F1 triggered (C2 reverses to TRUE).

**MEASUREMENT_INVALID** if PC1 or PC2 fails due to implementation bug.

## 9. Metrics

| Metric ID | Description | Unit |
|-----------|-------------|------|
| M1 | Corrected parent null mean (direct estimator, sorted roles) | pairwise agreement |
| M2 | Difference from stored 0.5275 | absolute |
| M3 | C2 direction under canonical recipe | TRUE/FALSE |
| M4 | Mean pairwise agreement across 10 seeds (canonical recipe) | pairwise agreement |
| M5 | SD across 10 seeds | pairwise agreement |
| M6 | DEF-FULL-MAP ordering | list |
| M7 | DEF-FORM-ONLY ordering | list |
| M8 | ISOLATED-A-LINK ordering | list |
| M9 | C2 direction per seed | list of bool |

## 10. Data

- **Source**: `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json`
- **Scope**: Truncated-first-20 locatable sample, 7 tasks, 1 Magento site, cart n=1
- **Definitions**: DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK (3 of 5 planned)
- **No new data collection**: Re-analysis of existing raw evidence only

## 11. Validity Threats

1. **Truncated data**: Results apply only to truncated-first-20 locatable sample, not full DOM. Full-DOM re-run blocked by substrate cap (locatableSample at measure_fullpage_yield.py:89).
2. **Single site**: All data from one Magento site. Cross-site invariance untested.
3. **Cart n=1**: Only 1 distinct cart page. Within-type variance undefined for cart.
4. **3 of 5 definitions**: Only 3 definitions independently verified. Pairwise agreement is C(3,2)=3 pairs, not C(5,2)=10.
5. **Estimator alignment**: Direct 499500-pair estimator may still differ from parent's sampled 10000-pair estimator by ~0.007 (audit V1). The 0.02 threshold accommodates this.

## 12. Expected Outcomes and Consequences

### If SURVIVES (C2 = FALSE confirmed)
- The FALSIFIED conclusion is scientifically valid: density ordering is definition-dependent
- C-MEAS-VALID density metric program should pivot or abandon ordering-based approach
- Corrected canonical script + frozen recipe unblocks full-DOM re-run with coherent decision rule
- Product consequence: density metric is not reliable for page-type discrimination

### If FALSIFIED_IN_SETTING (C2 reverses to TRUE)
- The original FALSIFIED was an implementation artifact, not a scientific finding
- Density ordering IS more stable than random under corrected implementation
- Full-DOM re-run becomes high-priority to confirm on non-truncated data
- Product consequence: density metric may be viable after all

### If MEASUREMENT_INVALID
- Implementation bugs persist despite corrections
- Need further debugging before scientific conclusion possible
- Not a scientific result — infrastructure failure

## 13. Estimated Cost

<1 GPU-hour. Re-analysis of existing data. No browser/network/model calls.

## 14. Preregistration Amendments

This preregistration amends the parent chain (EXP-INTEL-35112013458 through EXP-INTEL-35209112878) as follows:

1. **NC1 removed**: The parent's NC1 (cross-recipe equivalence) is logically incoherent and removed entirely. NC1 in this experiment tests parent null mean reproduction within 0.02, a different test.
2. **F3 threshold relaxed**: From 0.001 to 0.02, to accommodate cross-environment estimator and Python version variation (audit V1).
3. **Recipe canonically specified**: Per-iteration p=0.5 with sorted roles is the canonical null recipe, resolving the parent's recipe ambiguity.
4. **Pairwise agreement aligned**: Spec text aligned with code implementation — fraction of C(n,2) definition-pairs with identical ordering.
5. **Density denominator frozen**: elements_with_bbox (matching parent chain for ordering reproducibility).

These amendments are justified by the parent's MEASUREMENT_INVALID verdict and audit findings. No amendments will be made after outcome observation.
