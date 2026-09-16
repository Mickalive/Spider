# EXP-PHYSICS-35040401992 — Report

## Experiment Summary

**Experiment**: EXP-PHYSICS-35040401992  
**Lane**: Physics  
**Claim**: C-WEB-DYNAMICS  
**Date**: 2026-09-16  
**Status**: COMPLETE  
**Outcome**: MEASUREMENT_INVALID  

## Scientific Question

On locally-hosted Express SPAs with session-dependent API responses and a BRANCHING FSM (at least one state with >=2 outgoing actions and session-dependent transition probabilities) so that H(S_next|URL,H_K=3) > 0.2 bits, does network-response payload structure exhibit conditional PMI I(S_next; Response_before | URL, H_K=3) > 0.05 bits with Bonferroni-corrected permutation p < 0.0125 and a discriminating positive control (non-zero perm_null_std)?

## Decision

**MEASUREMENT_INVALID** — The experiment completed successfully with no infrastructure failures, but two frozen control criteria fail:

1. **Determinism check fails** (C5): P(Response_hash | FSM_state, session) accuracy = 0.0 for state-dependent condition (expected 1.0). The frozen response design includes a `step` field that varies within each (FSM_state, session_id) group, making the check unachievable by construction.

2. **Positive control fails** (C4): Session-randomized control yields min_perm_null_std = 0.0, making the pass criterion degenerate (|0.137| < 3 × 0 = 0 is false).

Per the frozen decision rule: "If controls fail ... — verdict = MEASUREMENT_INVALID."

## Key Findings

### Ceiling Elimination: SUCCESS
- H(S_next|URL, H_K=3) = 1.346 bits on the branching FSM (state-dependent condition)
- This far exceeds the 0.2-bit threshold, confirming the branching FSM eliminates the linear FSM's ceiling effect
- The branching FSM design works as intended

### Bias-Corrected PMI: POSITIVE BUT NOT SIGNIFICANT
| Condition | K | BC PMI (bits) | Bonferroni p |
|-----------|---|---------------|--------------|
| State-dependent | 3 | 0.369 | 0.322 |
| State-dependent | 1 | 0.924 | 0.000 |
| State-independent | 3 | 0.000 | 1.000 |
| State-independent | 1 | 0.000 | 1.000 |

- The state-dependent condition shows substantial BC PMI at both K=1 (0.924 bits) and K=3 (0.369 bits)
- K=3 Bonferroni p = 0.322 fails the p < 0.0125 threshold (C2 fails)
- K=1 is highly significant (p < 0.001 after Bonferroni correction)
- State-independent baseline BC PMI = 0.0 at both K values, confirming estimator correctness

### Discrimination Test: HIGHLY SIGNIFICANT
- SD BC PMI − SI BC PMI = 0.369 bits at K=3, paired permutation p = 0.0
- This cleanly demonstrates that response structure carries predictive information
- The within-experiment comparison (same FSM, same sessions, only response content differs) is the strongest possible causal test

### Controls: TWO FAILURES

#### Positive Control (Session-Randomized): FAIL
- BC PMI = 0.1375 (not ≈ 0)
- min_perm_null_std = 0.0 (degenerate)
- The zero perm_null_std indicates the permutation test only exercises deterministic strata after session randomization, or the randomization eliminates all stratum-level variance

#### Null Control (Shuffled Labels): PASS
- Mean shuffled PMI = 0.757, std = 0.506
- |0.757| < 3 × 0.506 = 1.518 ✓
- However, the mean is far from zero, suggesting the shuffled-label null is not fully effective

#### State-Independent Baseline: PASS
- BC PMI = 0.0 at both K=1 and K=3 ✓

#### Determinism Check: FAIL (state-dependent)
- SD accuracy = 0.0 (0/60 groups deterministic)
- SI accuracy = 1.0 (60/60 groups deterministic)
- The SD failure is a frozen design flaw: the response includes `step` which varies within (state, session) groups

### Cardinality: PASS
- Max |R|/N ratio across SD K=3 strata = 0.782 (below 0.8 threshold)
- The branching FSM avoids the parent's cardinality degeneracy

## Interpretation

The experiment successfully eliminates the linear FSM's ceiling effect (H = 1.346 bits at K=3) and demonstrates that network-response payload structure carries substantial conditional PMI (BC PMI = 0.369 bits at K=3, 0.924 bits at K=1). The discrimination test is highly significant (paired permutation p = 0.0), cleanly establishing that response content carries predictive information when action-history is insufficient.

However, the experiment is MEASUREMENT_INVALID because two frozen control criteria fail:

1. **Determinism check**: The frozen spec requires P(Response_hash | FSM_state, session) = 1.0, but the frozen response design includes a `step` field that varies within each (state, session) group. This is a spec-design incompatibility, not a scientific finding about response non-determinism.

2. **Positive control**: The session-randomized control yields perm_null_std = 0.0, making the pass criterion degenerate. This prevents validation that the permutation test can discriminate genuine PMI from noise.

Despite the MEASUREMENT_INVALID verdict, the raw observations are informative:
- The branching FSM design works (ceiling eliminated)
- Response structure carries PMI when action-history is insufficient
- The state-independent baseline correctly gives PMI = 0
- The discrimination test is highly significant

These raw observations are preserved as evidence but cannot support a confirmatory claim for C-WEB-DYNAMICS due to control failures.

## Validity Threats

1. **Spec-design incompatibility**: The determinism check criterion is incompatible with the response design that includes step number. This is a frozen design issue, not an execution failure.

2. **Positive control degeneracy**: The session-randomized control's perm_null_std = 0.0 prevents discrimination. The cause is unclear — it may be a bug in the control implementation or a genuine property of the randomized condition.

3. **Conservative Bonferroni**: The 4-comparison Bonferroni correction includes state-independent comparisons (control baselines), diluting the significance threshold. The state-dependent K=3 comparison alone has p_raw = 0.0805.

4. **Null control non-zero mean**: The shuffled-label null has mean PMI = 0.757, far from zero, suggesting incomplete nullification.

## Raw Evidence

All raw evidence is preserved in:
- `raw_result.json`: Complete numerical results from the frozen analysis pipeline
- `run_experiment.py`: The frozen analysis code (executable, deterministic, seed=42)
- `raw_result_backup.json`: Backup of raw results before re-execution

## Verdict

**MEASUREMENT_INVALID** — Controls fail. The raw PMI values suggest a positive signal (BC PMI = 0.369 bits at K=3, discrimination p = 0.0), but the frozen control criteria are not met. A redesigned experiment with corrected determinism check and positive control is needed to produce a confirmatory result.
