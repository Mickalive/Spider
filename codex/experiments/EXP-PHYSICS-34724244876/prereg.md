# EXP-PHYSICS-34724244876 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34724244876
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

On locally-hosted deterministic SPAs, does DOM representation achieve predictive PMI beyond what is explained by action-history memory alone? Specifically: (1) what conditional PMI I(S_next; DOM | URL, ActionHistory) achieves, and does it exceed zero? (2) does action-history memory alone predict next state perfectly on these deterministic SPAs?

## 3. Motivation

Prior Physics work established:
- DOM visible_text_hash provides statistically significant PMI over URL-only structural zero on 3/3 deterministic SPAs (EXP-PHYSICS-34719136202)
- Effect is entirely tautological with action label: MI(action;DOM) > PMI on all sites (audit V1)
- Numeric DOM structural features are degenerate/invariant (audit V2)
- No history-conditioned baseline exists (audit B4)

The core Physics claim C-WEB-DYNAMICS requires 'predictive dynamical structure beyond memory and ordinary similarity'. Without a history-conditioned baseline, observed PMI cannot be distinguished from trivial memorization of the deterministic finite-state machine (next step = f(current step, action)).

This experiment resolves the identifiability gap by computing conditional PMI conditioned on action history. If DOM adds no predictive value beyond action history, the observed PMI is tautological. If DOM adds predictive value, it suggests DOM captures environmental state variation beyond what action labels determine.

## 4. Hypotheses

### H1: Conditional PMI is zero
I(S_next; DOM | URL, ActionHistory) = 0 on all 3 deterministic SPAs. DOM provides no predictive value beyond action-history memory.

### H2: Action-history memory predicts perfectly
On deterministic SPAs, P(S_next | S_current, Action) is deterministic (next state = f(current state, action)). Action-history memory alone achieves perfect prediction when current state is known.

### H3: Unconditional PMI exceeds conditional PMI
I(S_next; DOM | URL) > I(S_next; DOM | URL, ActionHistory) on all sites. The difference equals the tautological component attributable to action->DOM causality.

## 5. Data Source

### 5.1 Existing Raw Data
Reuse `raw_dom_captures.json` from EXP-PHYSICS-34719136202:
- 804 transitions across 3 SPAs (dashboard 200, multistep_form 200, wizard 154)
- Each transition contains: trajectory_id, step_index, action, DOM features (visible_text_hash, attribute_pattern_hash, element_count, tree_depth, interactive_density, form_count, input_count, button_count), URL
- No new data collection required

### 5.2 Action History Construction
For each transition at step t in trajectory i:
- ActionHistory_1 = [action_t] (current action only)
- ActionHistory_2 = [action_{t-1}, action_t] (last 2 actions)
- ActionHistory_3 = [action_{t-2}, action_{t-1}, action_t] (last 3 actions)
- For t=0, pad with <START> token

### 5.3 State Representation
- S_next = visible_text_hash of DOM after transition (4 unique values per SPA)
- Representation = visible_text_hash of DOM before transition (current state)
- URL = single path per SPA (structural zero)

## 6. Measures

### 6.1 Conditional PMI (Primary Metric)
Compute I(S_next; Representation | URL, ActionHistory) via:
1. For each action-history stratum h, compute joint distribution P(Representation, S_next | ActionHistory=h)
2. Compute conditional PMI = sum_{r,s,h} P(r,s|h) log2[ P(r,s|h) / (P(r|h) P(s|h)) ]
3. Average across action-history strata weighted by stratum frequency

### 6.2 Unconditional PMI (Comparison)
I(S_next; Representation | URL) from parent experiment (recomputed for consistency).

### 6.3 PMI Difference
Delta = unconditional PMI - conditional PMI. This equals the tautological component attributable to action->DOM causality.

### 6.4 Action-History Prediction Accuracy
Accuracy of predicting S_next from ActionHistory alone (most frequent next state given action history).

### 6.5 Current-State Prediction Accuracy
Accuracy of predicting S_next from (S_current, Action) — should be 100% on deterministic SPAs.

## 7. Null Models

### 7.1 Shuffled DOM Labels
Permute DOM labels within action-history strata. Preserves action-history distribution, destroys DOM-S_next association. Conditional PMI should be zero.

### 7.2 Shuffled Action History
Permute action-history labels across transitions. Preserves DOM distribution, destroys action-history-S_next association. Tests whether action history is informative.

### 7.3 Frequency Null
Predict S_next from marginal P(S_next). Expected accuracy: 1/|S| (25% for 4 states).

## 8. Statistical Tests

### 8.1 Primary Test
- Permutation test: shuffle DOM labels within action-history strata, N=1000 permutations
- Compute conditional PMI on shuffled data, compare to observed
- One-sided test: conditional PMI > 0
- Bonferroni correction for 3 sites (alpha 0.05/3 = 0.0167)

### 8.2 Paired Comparison
- Paired t-test: unconditional PMI vs conditional PMI across trajectories
- Two-sided, alpha=0.05
- Tests whether unconditional > conditional (tautology detection)

### 8.3 Effect Size
- Cohen's d for conditional PMI vs zero across trajectories

## 9. Controls

### 9.1 Positive Control (Synthetic SPA)
- Synthetic SPA with random DOM labels independent of action history
- Conditional PMI should be zero (pipeline correctly detects independence)
- Verified in parent experiment: synthetic DOM PMI > 0 but conditional should be 0

### 9.2 Null Control (Shuffled Labels)
- Shuffled DOM labels within action-history strata
- Conditional PMI should be zero (pipeline does not detect structure when absent)

### 9.3 Determinism Control
- Current-state prediction accuracy should be 100% on all SPAs (deterministic FSM)
- If not 100%, data or representation is flawed

### 9.4 Action-History Sufficiency Control
- Action-history prediction accuracy should be high (>80%) on deterministic SPAs
- If low, action history is insufficient to explain observed PMI

## 10. Validity Threats

### 10.1 Sample Size
With 804 transitions across 3 SPAs (200/200/154), action-history strata may have small counts. Mitigation: report stratum frequencies; combine rare strata (count < 5) into 'other' category.

### 10.2 Action History Length
K=1,2,3 actions may not capture full state dependency. Mitigation: test all three lengths; if conditional PMI decreases with K, longer history captures more dependency.

### 10.3 Representation Collapse
DOM representation is hash-based (4 unique values per SPA). Discrete representation may miss continuous variation. Mitigation: acknowledge limitation; hash-based representation is what prior experiments used.

### 10.4 Deterministic SPA Specificity
Results apply only to deterministic Express SPAs on localhost. Generalization to production SPAs is explicitly out of scope. Mitigation: bound claim ceiling.

### 10.5 Wizard Data Loss
Wizard has 154/200 transitions (23% loss). Missingness mechanism unknown. Mitigation: report sensitivity analysis excluding wizard.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Conditional PMI > 0.1 bits on >= 2/3 sites
2. Bonferroni-corrected permutation p < 0.0167 on those sites
3. No pipeline errors
4. Determinism control passes (current-state accuracy 100%)

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Conditional PMI <= 0.1 bits on >= 2/3 sites
2. Fails significance on < 2/3 sites
3. Determinism control fails

### 11.3 MEASUREMENT_INVALID
If:
1. Sample sizes insufficient (<10 transitions per action-history stratum)
2. Pipeline errors prevent computation
3. Data corruption detected

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- DOM adds predictive value beyond action history
- Suggests DOM captures environmental state variation not determined by action labels
- Supports DOM as non-trivial state representation for SPIDER observation layer
- Physics lane should investigate production SPAs with richer rendering

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- DOM adds no predictive value beyond action history
- Confirms tautology: observed PMI is entirely action->DOM causality
- DOM integration as non-trivial physics not warranted on deterministic SPAs
- Physics lane should focus on production SPAs where deterministic server logic is absent

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Data Loading**: Load raw_dom_captures.json from EXP-PHYSICS-34719136202
2. **Action History Construction**: Build ActionHistory_1, ActionHistory_2, ActionHistory_3 from trajectory indices
3. **Conditional PMI Computation**: For each SPA, for each action-history length K, compute conditional PMI via empirical conditional probability tables
4. **Permutation Test**: Shuffle DOM labels within action-history strata, N=1000, compute conditional PMI on shuffled data
5. **Unconditional PMI Recomputation**: Recompute unconditional PMI from same data for comparison
6. **Delta Computation**: Compute unconditional - conditional PMI (tautological component)
7. **Action-History Prediction**: Compute prediction accuracy from action history alone
8. **Determinism Check**: Compute prediction accuracy from (S_current, Action) — should be 100%
9. **Controls**: Verify positive control (synthetic), null control (shuffled), determinism control
10. **Reporting**: Report all outcomes with equal prominence

## 14. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations
- `collections.Counter` for empirical distributions
- `scipy.stats` for permutation tests
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-PHYSICS-34724244876/` before execution.

## 15. Pre-registered Expectations

From prior Physics work:
- DOM PMI is tautological with action label on all sites (MI > PMI)
- Action-history memory should explain most/all of DOM PMI
- Conditional PMI should be near zero on dashboard (action alone determines next state)
- Conditional PMI may be non-zero on multistep_form/wizard (action alone insufficient, current step needed)
- If conditional PMI > 0 on any site, DOM captures non-trivial state variation

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.