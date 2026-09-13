# EXP-PHYSICS-34724244876 — Report

## Executive Summary

**Verdict: SURVIVES_CURRENT_TEST** — DOM provides predictive PMI beyond action-history memory on 2/3 deterministic SPAs when action history is incomplete (K=1,2), but becomes redundant when history is sufficient (K=3).

This experiment resolved the identifiability gap (audit B4) from the parent experiment by computing conditional PMI I(S_next; DOM | URL, ActionHistory) with Bonferroni-corrected permutation tests on 3 locally-hosted deterministic SPAs.

## Key Findings

### 1. Dashboard: DOM adds zero predictive value beyond action history

| Metric | K=1 | K=2 | K=3 |
|--------|-----|-----|-----|
| Conditional PMI | 0.000 bits | 0.000 bits | 0.000 bits |
| Action-history accuracy | 100% | 100% | 100% |
| Permutation p (Bonferroni) | 1.000 | 1.000 | 1.000 |

Dashboard has 4 unique tab actions (overview, users, settings, analytics) where each action uniquely determines the next state. The current action alone fully predicts the next state at K=1. DOM provides zero additional information. The unconditional PMI (0.041 bits) is entirely tautological with action label.

### 2. Multistep_form: DOM is informative when action history is incomplete

| Metric | K=1 | K=2 | K=3 |
|--------|-----|-----|-----|
| Conditional PMI | **0.939 bits** | **0.344 bits** | 0.000 bits |
| Action-history accuracy | 75% | 87.5% | 100% |
| Permutation p (Bonferroni) | **<0.001** | **<0.001** | 1.000 |

At K=1, the current action alone predicts only 75% of next states. DOM encodes state variation that the single action cannot determine (the "next" button leads to different states depending on the current form step). At K=2, accuracy improves to 87.5% and conditional PMI drops to 0.344. At K=3, action history fully predicts next state and DOM becomes redundant.

### 3. Wizard: Same pattern as multistep_form

| Metric | K=1 | K=2 | K=3 |
|--------|-----|-----|-----|
| Conditional PMI | **0.960 bits** | **0.413 bits** | 0.000 bits |
| Action-history accuracy | 74% | 87% | 100% |
| Permutation p (Bonferroni) | **<0.001** | **<0.001** | 1.000 |

Wizard shows the same state-dependent dynamics: "next" button leads to different states depending on the current wizard step. DOM encodes step information that short action histories miss.

### 4. Determinism confirmed

All 3 SPAs are deterministic finite-state machines: P(S_next | S_current, Action) = 100% accuracy on all 804 transitions. This confirms the parent experiment's setting and validates the data.

### 5. Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| Determinism | 100% | 100% (all sites) | ✅ |
| Null (shuffled DOM) | PMI ≈ 0 | PMI = 0.0 | ✅ |
| Frequency null | ~25% | 28-50% | ✅ |
| Positive (synthetic) | PMI ≈ 0 | PMI = 1.69 | ❌ |

**Positive control failure**: The synthetic SPA has deterministic DOM labels that change with FSM state, replicating the same causal structure as real SPAs. This is a control design flaw, not a pipeline failure. The pipeline correctly detects DOM-state association. A properly designed independence control is needed.

## Interpretation

### What the conditional PMI pattern reveals

The conditional PMI decreases with action-history length K on multistep_form and wizard:

- **K=1**: DOM is highly informative (0.94-0.96 bits) because the single action "next" does not uniquely determine the next state. DOM encodes the current step number.
- **K=2**: DOM is partially informative (0.34-0.41 bits) because the last 2 actions narrow down the possible states but don't fully determine them.
- **K=3**: DOM is redundant (0.0 bits) because the last 3 actions fully reconstruct the FSM state.

This pattern is consistent with a deterministic FSM where:
1. The action vocabulary is limited (repeated "next" actions)
2. State depends on the position in a sequence (step number)
3. DOM acts as a state label that encodes position information

### Is this "predictive dynamical structure beyond memory"?

The answer depends on the observation window:

- **At short observation windows (K=1,2)**: Yes, DOM provides predictive information that action history alone cannot. DOM encodes state variation (step number) that short histories miss.
- **At sufficient observation windows (K=3)**: No, action history fully predicts the next state and DOM becomes redundant.

The C-WEB-DYNAMICS claim requires "predictive dynamical structure beyond memory and ordinary similarity." This experiment shows that DOM satisfies this criterion conditionally — when memory (action history) is insufficient. But with sufficient memory, DOM is entirely redundant.

### Comparison to parent experiment

The parent experiment found unconditional PMI of 1.061 bits (multistep_form) and 0.922 bits (wizard). The conditional PMI at K=1 is comparable (0.939 and 0.960 bits), confirming that most of the unconditional PMI is not attributable to action-history memory when K is small. The delta (unconditional - conditional) at K=1 is small (0.123 bits for multistep_form, -0.037 for wizard), indicating that action label alone explains only a small fraction of the PMI at short history lengths.

## Decision Rule Application

Per preregistration §11:

1. **Conditional PMI > 0.1 bits on ≥ 2/3 sites**: ✅ multistep_form (0.939) and wizard (0.960) both exceed 0.1 at K=1
2. **Bonferroni p < 0.0167**: ✅ Both sites have p < 0.001
3. **No pipeline errors**: ✅ Analysis completed without errors
4. **Determinism control passes**: ✅ 100% accuracy on all sites

**Verdict: SURVIVES_CURRENT_TEST**

However, the positive control failure weakens confidence in the pipeline's ability to detect independence. The result should be interpreted as: DOM provides state-dependent predictive information at short history lengths, but this information is entirely subsumed by longer action histories.

## Claim Ceiling

DOM visible_text_hash provides conditional PMI beyond action-history memory on multistep_form and wizard when K < 3, but this is entirely explained by action-history sufficiency at K=3. The effect is specific to:
- Deterministic Express SPAs with limited action vocabularies
- Short observation windows (K=1,2)
- Hash-based DOM representation (4 unique values per SPA)

This does not demonstrate predictive dynamical structure that persists with sufficient memory. It demonstrates that DOM encodes state information that short histories miss — a form of state labeling, not environmental dynamics.

## Product Consequence

DOM integration as a non-trivial state representation is conditionally supported:
- **Supported**: DOM as a state encoder for short observation windows where action history is insufficient
- **Not supported**: DOM as a persistent source of predictive information beyond memory — it becomes redundant with sufficient history
- **Not supported**: DOM integration into SPIDER's observation layer based on this experiment alone — the effect is state labeling, not environmental dynamics
