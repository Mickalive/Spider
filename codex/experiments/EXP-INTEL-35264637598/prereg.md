# EXP-INTEL-35264637598 Preregistration

## Status: DESIGN — NOT YET FROZEN

---

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35264637598
- **Lane**: intel
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid) — density metric sub-problem
- **Parent**: EXP-INTEL-35262261436 (SURVIVES_CURRENT_TEST — canonical recipe C2 FALSE validated)
- **Parent Handoff**: `research/experiments/EXP-INTEL-35262261436/handoff.json`

## 2. Scientific Question

Does the per-task weighted recipe's C2 TRUE reversal (established under buggy implementation in EXP-INTEL-35209112878) persist under the corrected implementation with deterministic sorted roles and aligned estimator — or does the corrected implementation eliminate the reversal, revealing it as an artifact of the same bugs that caused the parent MEASUREMENT_INVALID?

## 3. Background and Motivation

The parent EXP-INTEL-35262261436 validated the canonical per-iteration p=0.5 recipe's C2 FALSE conclusion under corrected implementation: observed 0.3 < null 0.5273, density ordering is LESS stable than random role subsets. This was a genuine scientific finding, not an implementation artifact.

However, the parent handoff explicitly notes:

> "Per-task weighted recipe C2 TRUE reversal remains established from parent (EXP-INTEL-35209112878): null ~0.28 < observed 0.3, ordering MORE stable than random. This reversal is robust (SD=0.0117, cross-RNG diff 0.0024) but was NOT retested in this experiment — only the canonical recipe was tested."

The critical question is whether this reversal was **also affected by the same implementation bugs** that caused the parent MEASUREMENT_INVALID:

1. **Unsorted set iteration**: `get_all_raw_roles()` returns a `set` and iterates without sorting → PYTHONHASHSEED nondeterminism
2. **Estimator mismatch**: Parent stored value used sampled 10000-pair estimator; canonical uses direct 499500-pair estimator

Both bugs would affect ANY recipe analysis using the same code — including the per-task weighted recipe analysis in EXP-INTEL-35209112878. The corrected implementation (sorted roles + aligned estimator) provides the first opportunity to determine whether the reversal is genuine or artifact.

### Why this matters

If the reversal persists under corrected code: Recipe choice is a MATERIAL determinant of the C-MEAS-VALID density metric conclusion. The density metric is doubly unstable — definition-dependent AND recipe-dependent. Product must abandon ordering-based density metrics.

If the reversal is eliminated: The canonical per-iteration recipe is the sole valid recipe. C2 FALSE is the unambiguous conclusion. Recipe choice is resolved.

Either outcome changes the product decision. The full-DOM re-run (blocked by substrate cap) would be the next step, but this experiment resolves the recipe question on existing data first.

## 4. Canonical Null Recipe Selection (Unchanged from Parent)

**Adopted: Per-iteration p=0.5 independent inclusion with deterministic sorted roles.**

The per-iteration recipe is canonically justified for C-MEAS-VALID because:
1. Uniform application across definitions (matches how definitions are used)
2. Controls for role preferences (randomizes role subset while keeping it shared)
3. Tests the right question: "Do definitions agree more than random role subsets?"

The per-task weighted recipe tests a different scientific question: "Do definitions agree more than random task-specific role selections?" This is a valid question but not the one for C-MEAS-VALID.

### Implementation Fix (Applied to Both Recipes)

Both recipes now use:
- `sorted(raw_roles)` before sampling → deterministic, no PYTHONHASHSEED nondeterminism
- Direct 499500-pair estimator for both null and observed → no estimator mismatch

## 5. Hypothesis

**H1 (primary)**: Under the corrected implementation, the per-task weighted recipe's C2 TRUE reversal persists: per-task weighted null mean < observed 0.3, while canonical per-iteration null mean > observed 0.3.

**H0 (null)**: Under the corrected implementation, the per-task weighted recipe also produces C2 FALSE (observed ≤ null mean), eliminating the reversal. The reversal was an artifact of implementation bugs.

## 6. Falsification Criteria

| ID | Condition | Threshold | Meaning |
|----|-----------|-----------|---------|
| F1 | Per-task weighted C2 direction | C2 = FALSE (observed ≤ null mean) | Reversal eliminated — was an artifact of implementation bugs |
| F2 | Canonical C2 direction | C2 = TRUE (observed > null mean) | Parent's canonical FALSIFIED result fails to reproduce |
| F3 | Per-task weighted null mean | >0.05 deviation from parent's ~0.28 | Parent's per-task weighted stored value unreliable |

## 7. Controls

### Positive Controls

| ID | Test | Expected |
|----|------|----------|
| PC1 | Canonical recipe reproduces C2 FALSE | Observed 0.3 < null >0.5, matching parent EXP-INTEL-35262261436 |
| PC2 | Recipes produce materially different null distributions | Per-task weighted null mean significantly < canonical null mean |

### Null Controls

| ID | Test | Expected |
|----|------|----------|
| NC1 | Both recipes agree on C2 direction | Both FALSE (reversal artifact) or both TRUE (canonical wrong) |
| NC2 | Per-task weighted null mean reproduction | Within 0.05 of parent's stored ~0.28 |

### Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B1 | Canonical C2 FALSE reproduced | Null mean within 0.02 of 0.5273 |
| B2 | Per-task weighted reversal direction | Either C2 TRUE (genuine) or C2 FALSE (artifact) |
| B3 | Recipe divergence magnitude | Quantifiable and reproducible across seeds |

## 8. Decision Rule

**SURVIVES_REVERSAL_PERSISTS** requires ALL of:
1. PC1 passes (canonical C2 FALSE reproduced)
2. Per-task weighted C2 = TRUE (reversal persists under corrected implementation)
3. NC2 passes (per-task weighted null mean within 0.05 of 0.28)
4. F1 not triggered (per-task weighted C2 is TRUE, not FALSE)
5. F2 not triggered (canonical C2 is FALSE, not TRUE)
6. F3 not triggered (per-task weighted null mean within 0.05 of 0.28)

**FALSIFIED_REVERSAL_ARTIFACT** if F1 triggered: per-task weighted recipe also gives C2 FALSE under corrected implementation, eliminating the reversal.

**UNEXPECTED_BOTH_TRUE** if: canonical C2 = TRUE AND per-task weighted C2 = TRUE.

**MEASUREMENT_INVALID** if: PC1 fails or either recipe's implementation produces errors.

## 9. Metrics

| Metric ID | Description | Unit |
|-----------|-------------|------|
| M1 | Canonical recipe null mean (corrected implementation) | pairwise agreement |
| M2 | Canonical recipe C2 direction | TRUE/FALSE |
| M3 | Per-task weighted recipe null mean (corrected implementation) | pairwise agreement |
| M4 | Per-task weighted recipe C2 direction | TRUE/FALSE |
| M5 | Recipe divergence (canonical null - per-task weighted null) | absolute |
| M6 | Canonical recipe SD across 10 seeds | pairwise agreement |
| M7 | Per-task weighted recipe SD across 10 seeds | pairwise agreement |
| M8 | Per-task weighted null mean deviation from parent ~0.28 | absolute |
| M9 | Canonical recipe C2 direction per seed | list of bool |
| M10 | Per-task weighted recipe C2 direction per seed | list of bool |

## 10. Data

- **Source**: `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json`
- **Scope**: Truncated-first-20 locatable sample, 7 tasks, 1 Magento site, cart n=1
- **Definitions**: DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK (3 of 5 planned)
- **No new data collection**: Re-analysis of existing raw evidence only
- **Both recipes computed on identical raw data**

## 11. Validity Threats

1. **Truncated data**: Results apply only to truncated-first-20 locatable sample, not full DOM. Full-DOM re-run blocked by substrate cap (locatableSample at measure_fullpage_yield.py:89).
2. **Single site**: All data from one Magento site. Cross-site invariance untested.
3. **Cart n=1**: Only 1 distinct cart page. Within-type variance undefined for cart.
4. **3 of 5 definitions**: Only 3 definitions independently verified. Pairwise agreement is C(3,2)=3 pairs, not C(5,2)=10.
5. **Per-task weighted recipe implementation**: The per-task weighted recipe was previously implemented in the parent chain (EXP-INTEL-35209112878) with buggy code. The corrected implementation must faithfully reproduce the recipe's intended behavior: independent random role subset per task, weighted by task density.
6. **Estimator alignment**: Both recipes now use the direct 499500-pair estimator. The parent's per-task weighted result used the sampled 10000-pair estimator, which may differ by ~0.007. The 0.05 threshold accommodates this.

## 12. Expected Outcomes and Consequences

### If SURVIVES_REVERSAL_PERSISTS (reversal genuine)
- Recipe choice is a MATERIAL determinant of C-MEAS-VALID density metric conclusion
- Density metric is doubly unstable: definition-dependent AND recipe-dependent
- Product must pivot away from ordering-based density metrics entirely
- Full-DOM re-run becomes even more critical: must test both recipes on full data
- The canonical recipe's C2 FALSE and the per-task weighted recipe's C2 TRUE are both valid — they answer different scientific questions

### If FALSIFIED_REVERSAL_ARTIFACT (reversal eliminated)
- Recipe reversal was caused by implementation bugs (unsorted set, estimator mismatch)
- Corrected implementation leaves only canonical recipe's C2 FALSE as valid
- Recipe choice is NOT material — only canonical recipe produces valid results
- Product decision simplifies: adopt canonical recipe, pivot away from ordering-based density metrics
- Full-DOM re-run can proceed with single canonical recipe (no recipe ambiguity)

### If UNEXPECTED_BOTH_TRUE
- Both recipes agree ordering IS more stable than random
- Parent's canonical FALSIFIED was wrong — needs investigation
- Possible explanation: corrected implementation changed the canonical result too
- Requires immediate re-examination of the canonical recipe's corrected implementation

### If MEASUREMENT_INVALID
- Implementation bugs persist despite corrections
- Need further debugging before scientific conclusion possible
- Not a scientific result — infrastructure failure

## 13. Estimated Cost

<1 GPU-hour. Re-analysis of existing truncated-first-20 raw evidence (7 tasks, 3 definitions, 2 recipes × 10 seeds × 1000 null iterations = 20,000 null draws). No browser/network/model calls. Code changes: add per-task weighted recipe implementation to the corrected analysis script.

## 14. Preregistration Amendments

This preregistration amends the parent chain as follows:

1. **Both recipes tested**: Parent (EXP-INTEL-35262261436) tested only the canonical per-iteration recipe. This experiment tests BOTH recipes (canonical + per-task weighted) as co-primary analyses.
2. **Reversal verification**: Parent carried forward the per-task weighted reversal as "established" from EXP-INTEL-35209112878, but that analysis used buggy implementation. This experiment verifies the reversal under corrected implementation.
3. **Recipe divergence quantification**: Parent noted recipe choice was "material" but did not formally quantify the divergence under corrected code. This experiment provides the precise divergence estimate.
4. **Decision rule extended**: Parent's decision rule was single-recipe (canonical only). This experiment's decision rule covers both recipes and their interaction.

These amendments are justified by the parent's establishment of recipe sensitivity and the corrected implementation's availability. No amendments will be made after outcome observation.
