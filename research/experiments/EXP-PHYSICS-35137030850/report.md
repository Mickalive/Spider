# EXP-PHYSICS-35137030850 — Execution Report

## Experiment Summary

**Question**: Can a non-deterministic branching FSM with many-to-one content mapping (where response does NOT uniquely determine state for a subset of states) yield conditional PMI > 0.05 bits at K=3?

**Frozen verdict per decision rule**: FALSIFIED-IN-SETTING (C3 fails: many-to-one BC PMI 0.226 < unique-content BC PMI 0.493 - 0.1 = 0.393)

**Scientific interpretation**: MIXED — PMI persists with many-to-one mapping (0.226 bits), demonstrating genuine predictive dynamics beyond content-state aliasing, but is substantially reduced (54% drop) compared to unique-content mapping.

## 1. Primary Result

| Metric | Many-to-One | Unique-Content | Difference |
|--------|-------------|----------------|------------|
| BC PMI at K=3 | **0.226 bits** | **0.493 bits** | **-0.268 bits** |
| Bonferroni p | 0.0 | 0.0 | — |
| BC PMI at K=1 | 0.247 bits | 0.565 bits | -0.318 bits |
| H(S_next\|URL,H_K=3) | 1.533 bits | 1.537 bits | -0.003 bits |
| Unique response hashes | 2 | 3 | — |
| N transitions | 2000 | 2000 | — |

**Key finding**: BC PMI > 0 on many-to-one condition (0.226 bits, p_bonf=0.0). Response content carries predictive information about state transitions even when content does NOT uniquely determine state for 2 of 3 states.

## 2. Decision Rule Evaluation

| Criterion | Threshold | Observed | Pass? |
|-----------|-----------|----------|-------|
| C1: H > 0.2 bits | > 0.2 | 1.533 | YES |
| C2: BC PMI > 0.05, Bonf p < 0.0125 | > 0.05, < 0.0125 | 0.226, 0.0 | YES |
| C3: mto > uniq - 0.1 | > -0.1 | -0.268 | **NO** |
| C4: Positive control passes | BC ≈ 0 | 0.002 | YES |
| C5: Determinism check | accuracy = 1.0 | 1.0 | YES |
| C6: N >= 500 | >= 500 | 2000 | YES |
| C7: Cardinality < 0.8 | < 0.8 | 0.001 | YES |

**Verdict**: FALSIFIED-IN-SETTING (C3 fails)

## 3. Controls

### 3.1 Positive Control (Content-Shuffled)
- **Design**: Each transition's response replaced with content from a random state, preserving many-to-one hash pool but breaking state→content pairing. Evaluated on H>0 strata only.
- **Result**: BC PMI = 0.002 ≈ 0, perm_std = 0.0064
- **Interpretation**: Pipeline correctly detects that randomizing state→content pairing eliminates PMI. The estimator and pipeline are valid.

### 3.2 Null Control (Shuffled Labels)
- **Design**: Within each (URL, H_K=3, step) stratum, permute response labels. Bias-corrected: subtract permutation mean.
- **Result**: Raw shuffled PMI mean = 0.052 (finite-sample bias), BC shuffled PMI mean = 0.0 (by construction), BC shuffled PMI std = 0.0068
- **Interpretation**: Estimator has ~0.05 bit positive finite-sample bias, correctly removed by BC correction. BC-corrected estimator yields ≈0 under the null.

### 3.3 Determinism Check
- **Result**: P(Response_hash | FSM_state, session, step) = 1.0 on both conditions (571 groups MTO, 582 groups UNIQ, 0 violations)
- **Interpretation**: Content is deterministic per (state, session, step) in both conditions. No content leakage across sessions or steps.

### 3.4 Cardinality
- Many-to-one: all 63 strata at K=3 have exactly 2 unique response hashes (shared S0/S1 + unique S2). Max ratio = 0.001.
- Unique-content: all 63 strata at K=3 have exactly 3 unique response hashes. Max ratio = 0.0015.
- No cardinality degeneracy in either condition.

## 4. Interpretation

### 4.1 What the result means

The frozen decision rule's FALSIFIED-IN-SETTING verdict is triggered by C3: many-to-one BC PMI (0.226) is more than 0.1 bits below unique-content BC PMI (0.493). This is a strict threshold.

However, the scientific picture is more nuanced:

1. **PMI persists with many-to-one mapping**: BC PMI = 0.226 > 0.05 bits, p_bonf = 0.0. This is the critical test for V10 identifiability. The parent's concern that PMI was "trivially constructed from content-state aliasing" is PARTIALLY addressed: PMI survives when content is ambiguous for 2 of 3 states.

2. **Content-state aliasing IS a significant source**: The 54% reduction in PMI (0.226 vs 0.493) quantifies how much of the parent's signal came from content uniquely determining state. Approximately 54% of the unique-content PMI was attributable to content-state aliasing.

3. **Genuine predictive dynamics remain**: The remaining 0.226 bits of PMI on many-to-one condition represents information that CANNOT be explained by content-state aliasing alone. This could be:
   - **Partial state discrimination**: Observing the unique S2 content eliminates 2 states; observing shared S0/S1 content narrows to 2 states. This partial discrimination still carries information about next-state distribution.
   - **Genuine response-context dynamics**: The response content (even when ambiguous between S0/S1) may carry structural information about transition probabilities.

### 4.2 What does NOT follow

- The result does NOT demonstrate fully content-independent predictive dynamics (the many-to-one condition still has 2 unique hashes, allowing partial discrimination).
- The result does NOT close C-WEB-DYNAMICS (PMI>0 persists, even if reduced).
- The result does NOT validate the pipeline for production use (all tests are synthetic).

### 4.3 The C3 threshold question

The frozen decision rule's C3 threshold (mto > uniq - 0.1) is very conservative. A difference of -0.268 bits still leaves many-to-one BC PMI well above the 0.05 significance threshold. The FALSIFIED-IN-SETTING verdict per the frozen rule does not mean PMI=0; it means PMI is substantially reduced by many-to-one mapping.

This raises a question for the DIRECTOR: should C3 be reinterpreted as "content-state aliasing was the SOLE source" (requiring mto BC PMI ≈ 0) rather than "content-state aliasing was a SIGNIFICANT source" (requiring mto < uniq - 0.1)?

## 5. Validity Threats

1. **Partial discrimination**: Many-to-one mapping still allows partial state discrimination (S2 is unique). PMI>0 could partly reflect this rather than pure predictive dynamics. A 3-way shared content condition would resolve this.

2. **Synthetic-to-real gap**: All tests use locally-hosted Express SPA with known FSM structure. Production SPAs have client-side rendering, auth-dependent content, and external data feeds.

3. **Finite-sample bias**: Estimator has ~0.05 bit positive bias, removed by BC correction. Without BC, PMI would be inflated.

4. **Small strata**: Some strata at K=3 have only 18-20 items. PMI estimates on small strata may be noisy, though the BC correction helps.

## 6. Next Steps

The dominant question from this experiment: **Is the remaining 0.226 bits from genuine predictive dynamics or partial state discrimination?**

To resolve this, the next experiment should test a **fully ambiguous content condition** where all 3 states share the same content hash (1 unique hash). If PMI>0 persists, it demonstrates genuine response-context dynamics. If PMI→0, the signal was entirely from partial state discrimination.

Alternatively, the Physics lane could pivot to production SPA infrastructure where transitions are naturally non-deterministic and content varies stochastically, closing the synthetic-to-real gap.
