# EXP-PHYSICS-34724244876 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34724244876
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-PHYSICS-34719136202 (FALSIFIED-IN-SETTING, audit REVISE)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

On locally-hosted deterministic SPAs, does any state representation achieve predictive PMI beyond what action-history memory alone determines? Specifically: (1) what PMI does a history-conditioned baseline P(s'|action_history) achieve, and does DOM or network representation exceed it? (2) does conditional mutual information MI(S_next; DOM | action_history) indicate DOM encodes predictive state variation not already captured by the action history?

## 3. Motivation

### What the parent experiment established

**DOM visible_text_hash provides PMI over URL-only structural zero on all 3 SPAs:**
- dashboard +1.006 bits, multistep_form +0.286 bits, wizard +0.438 bits
- All Bonferroni p=0.003, n_test 40/40/31

**But the effect is entirely tautological with action (type+target) label:**
- MI(action; DOM_state) = 1.989 bits (dashboard), 0.467 bits (multistep), 0.468 bits (wizard)
- Fraction tautological: dashboard 198%, multistep 163%, wizard 107%
- All sites: MI(action; DOM) > DOM PMI — gain is action->DOM causality

**Numeric DOM features are degenerate:**
- element_count, tree_depth, interactive_density, form_count, input_count, button_count are invariant across all transitions
- All PMI driven by visible_text_hash categorical

**Network signals exhausted:**
- Request-side: dashboard 0.881 (tautological), multistep 0.0, wizard 0.0
- Response-side: dashboard 0.034, multistep 0.0, wizard 0.0
- URL-only: 0.0 on all (structural, single-path routing)

### What the audit required (B4)

> "No history/memory baseline (e.g., predict next state from action sequence or previous DOM state alone without current action) despite C-WEB-DYNAMICS definition requiring 'beyond memory'. Deterministic FSA predicts perfectly from (state,action); PMI over URL-only conflates memory with dynamics. Required for physics identifiability."

### Why this experiment is different

The parent experiment measured DOM PMI against URL-only (structural zero). This experiment measures DOM PMI against action-type+target PMI — the natural baseline on deterministic servers where next state = f(current state, action).

If action labels already fully determine next state, then DOM features merely recover the FSM state label that action labels encode. PMI over URL-only is guaranteed if DOM varies, but does not demonstrate predictive structure beyond memory.

This experiment directly tests the 'beyond memory' requirement by comparing representations against the action-label baseline rather than the URL-only structural zero.

### carry_forward from parent handoff

**Established:**
- DOM visible_text_hash provides PMI over URL-only on 3/3 deterministic SPAs (dashboard +1.006, multistep +0.286, wizard +0.438, all Bonferroni p=0.003)
- Numeric DOM features are invariant — hash-only drives all PMI
- MI(action; DOM) > DOM PMI on all sites — tautological with action label
- PMI pipeline validated: positive control synthetic DOM PMI=0.577 p=0.001; null control shuffled labels p=0.302
- URL-only PMI structurally zero (single-path routing)
- All 3 SPAs are deterministic Express servers on localhost:3848-3850

**Rejected:**
- Numeric DOM structural features (element counts, tree depth, interactive density) as predictive representation — invariant on these SPAs
- Visible_text_hash as non-tautological predictive dynamics on deterministic SPAs — MI(action;DOM) > PMI on all sites
- Response-side signals (SHA-256 body digest) as predictive on locally-hosted SPAs
- Client-side request signatures as general predictive representation
- DOM as "last viable non-network representation" on these SPAs — works only as hash-based FSM state label

**Unknown:**
- What PMI an action-label baseline achieves on these SPAs and whether DOM exceeds it
- Whether DOM provides predictive PMI on production SPAs with non-deterministic rendering
- Whether finer-grained DOM features (accessibility tree, CSS styles) capture additional variation
- Whether combined DOM+network exceeds hash-only PMI
- Whether response timing provides predictive PMI

**Do Not Assume:**
- That DOM visible_text_hash PMI demonstrates predictive dynamical structure beyond memory — it is tautological with action label on deterministic SPAs
- That these results generalize to production SPAs
- That numeric DOM structural features provide any predictive signal on these SPAs
- That URL-only zero means URL is uninformative (structural, not empirical)
- That deterministic server logic precludes ALL non-tautological predictive dynamics
- That network representations are fundamentally uninformative
- That DOM integration into SPIDER is warranted based on tautological PMI

## 4. Hypotheses

### H1: Action-Label Dominance
On deterministic SPAs, action-type+target PMI MI(S_next; A) equals or exceeds DOM PMI MI(S_next; DOM) on >= 2/3 of tested sites. Action (type+target) labels are a sufficient statistic for next-state prediction when the server state machine is deterministic.

### H2: DOM Adds Nothing Beyond Action
Conditional mutual information MI(S_next; DOM | A) is negligible (< 0.1 bits) on >= 2/3 of tested sites. DOM features do not encode predictive state variation not already captured by the action label.

### H3: Positive Control
On synthetic SPA with independent environmental counter (genuine environmental dynamics), MI(S_next; DOM | A) > 0.1 bits with permutation p < 0.0167. Verifies pipeline detects real environmental dynamics when present.

### H4: Null Control
On real SPA data with shuffled action labels, MI(S_next; DOM | A_shuffled) is not significantly > 0 (permutation p > 0.0167 after Bonferroni correction). Verifies no false-positive environmental dynamics detection.

## 5. Data Sources

### 5.1 Existing Data (No New Collection)

Reuse raw_dom_captures.json from EXP-PHYSICS-34719136202:
- 804 transitions across 3 SPAs + synthetic
- sha256: 85efd4675f1fcbe841200cbd406338f1b81aaf923e9f2005982f92ee24a7d7a1
- Includes per-transition: DOM features (visible_text_hash, numeric features), URL, action type and target

Action labels extracted from trajectory metadata:
- action_type: one of {click, fill, submit, navigate}
- action_target: target_href (specific element identifier)
- action label = action_type:action_target combined as categorical

### 5.2 Synthetic Positive Control (New Collection)

Small new dataset: ~50 transitions on synthetic SPA with independent environmental counter.

The synthetic SPA has:
- 8 states, 4 actions (same as parent positive control)
- An independent counter that increments every transition regardless of action
- DOM features encode both action-determined state AND counter value
- Counter varies independently of action → MI(S_next; DOM | A) should be > 0

### 5.3 Sites

Same 3 locally-hosted SPAs as parent experiments:
- **dashboard** (port 3849): Tabbed dashboard with 4 tabs
- **multistep_form** (port 3848): 4-step checkout flow
- **wizard** (port 3850): 4-step wizard

All are deterministic Express servers on localhost with session-cookie state.

## 6. Measures

### 6.1 Primary Metrics

- **mi_action_next**: MI(S_next; A) — action-type+target PMI. How much does the action (type+target) predict the next state?
- **mi_dom_next**: MI(S_next; DOM) — DOM-feature PMI. How much does the DOM representation predict the next state?
- **mi_action_dom_next**: MI(S_next; A, DOM) — combined PMI. How much do action + DOM together predict the next state?
- **mi_dom_given_action**: MI(S_next; DOM | A) = MI(S_next; A, DOM) - MI(S_next; A) — conditional MI. How much does DOM add beyond action label?
- **mi_action_given_dom**: MI(S_next; A | DOM) = MI(S_next; A, DOM) - MI(S_next; DOM) — conditional MI. How much does action add beyond DOM?
- **dom_exceeds_action**: boolean — does MI(S_next; DOM) > MI(S_next; A) on each site?

### 6.2 Secondary Metrics

- Per-site unique states (action-label based vs DOM-based)
- Permutation p-values for each MI computation (1000 permutations)
- Effect sizes (Cohen's d for MI vs null distribution)
- Alpha sensitivity (smoothing alpha = 0.0, 0.5, 1.0, 2.0)
- Entropy of next-state distribution H(S_next)

### 6.3 Comparison Metrics

- URL-only PMI (structural zero, inherited)
- Network-request PMI (inherited from parent experiments, not re-measured)
- Parent DOM PMI (inherited: dashboard 1.006, multistep 0.286, wizard 0.438)
- Parent MI(action; DOM) (inherited: dashboard 1.989, multistep 0.467, wizard 0.468)

## 7. Null Models

### 7.1 Permutation Null (Action Labels)
Shuffle action labels across transitions preserving trajectory structure. Repeated 1000 times per site. Tests whether MI(S_next; A) is significant.

### 7.2 Permutation Null (DOM)
Shuffle DOM state labels across transitions preserving trajectory structure. Repeated 1000 times per site. Tests whether MI(S_next; DOM) is significant.

### 7.3 Permutation Null (Conditional MI)
Shuffle DOM labels while holding action labels fixed. Tests whether MI(S_next; DOM | A) is significant.

### 7.4 Frequency Null
Marginal next-state distribution P(S_next). Expected accuracy 1/|S|.

## 8. Statistical Tests

### 8.1 Primary Comparison
For each site: MI(S_next; DOM) vs MI(S_next; A). If MI(S_next; A) >= MI(S_next; DOM), action labels dominate.

### 8.2 Conditional MI Test
For each site: MI(S_next; DOM | A) with permutation test. If MI(S_next; DOM | A) < 0.1 bits, DOM adds nothing beyond action.

### 8.3 Bonferroni Correction
Alpha = 0.05 / 3 = 0.0167 for 3 site comparisons.

### 8.4 Paired Comparisons
At each site: paired permutation test for MI(S_next; DOM) vs MI(S_next; A).

## 9. Controls

### 9.1 Positive Control (Synthetic SPA with Environmental Counter)
- Synthetic SPA has independent counter varying regardless of action
- DOM encodes both action-determined state AND counter value
- Expected: MI(S_next; DOM | A) > 0.1 bits (counter is genuine environmental dynamics)
- Permutation p < 0.0167
- Verifies pipeline detects real environmental dynamics when present

### 9.2 Null Control (Shuffled Action Labels)
- Real SPA data with action labels permuted within trajectories
- Expected: MI(S_next; DOM | A_shuffled) permutation p > 0.0167
- Verifies no false-positive environmental dynamics detection

### 9.3 Data Sufficiency
- n_test >= 30 on held-out test per site
- Same as parent: dashboard 40, multistep 40, wizard 31

### 9.4 Pipeline Validation
- Reuse parent positive control (synthetic DOM PMI=0.577, p=0.001) as regression check
- Verify MI computations are consistent with parent PMI computations

## 10. Validity Threats

### 10.1 Action Label Definition
Action type (click/fill/submit/navigate) without target element. On deterministic servers, the next state depends on both action type AND target. If action type alone is insufficient to predict next state (because target matters), DOM might capture target information that action type misses. **Mitigation**: this is the correct comparison — we test whether DOM adds value beyond what action TYPE provides. If DOM captures target-specific information, that IS additional predictive structure.

### 10.2 Discretization of DOM State
DOM state is represented as visible_text_hash (SHA-16). Hash collisions could collapse distinct states, underestimating DOM PMI. **Mitigation**: alpha sensitivity analysis at multiple smoothing levels; SHA-16 has 2^16 possible values, sufficient for ~8 unique states per SPA.

### 10.3 Finite Sample Bias
With n_test = 30-40 per site, MI estimates may be noisy. **Mitigation**: permutation tests with 1000 permutations provide non-parametric significance; report confidence intervals.

### 10.4 Deterministic Server Logic
These SPAs have deterministic server logic (next state depends only on current step + action). This may make action-label dominance trivially true. **Mitigation**: this IS the hypothesis being tested. If action labels dominate, it confirms C-WEB-DYNAMICS is not supported on deterministic SPAs. The positive control (synthetic SPA with independent counter) verifies the pipeline can detect genuine dynamics when present.

### 10.5 Reuse of Parent Data
Using existing raw_dom_captures.json means no new DOM data collection. If the parent capture had quality issues (wizard 23% missingness), those propagate. **Mitigation**: wizard missingness is documented; n_test=31 still meets threshold. No new collection means no new missingness.

### 10.6 Conditional MI Estimation
MI(S_next; DOM | A) requires estimating joint distributions in higher-dimensional space. With limited data, conditional MI may be noisy. **Mitigation**: use the same PMI framework as parent (quantile binning, alpha smoothing); report results at multiple alpha levels.

## 11. Decision Rules

### 11.1 FALSIFIED-IN-SETTING
If ALL of:
1. Action-label PMI >= DOM PMI on >= 2/3 sites (action labels dominate)
2. MI(S_next; DOM | A) < 0.1 bits on >= 2/3 sites (DOM adds nothing beyond action)
3. Positive control passes (synthetic MI(S_next; DOM | A) > 0.1 bits)
4. Null control passes (shuffled MI(S_next; DOM | A) permutation p > 0.0167)
5. Data sufficiency met (n_test >= 30 per site)
6. No pipeline errors

This confirms DOM PMI is tautological FSM state recovery on deterministic SPAs. C-WEB-DYNAMICS 'beyond memory' not supported in this setting.

### 11.2 SURVIVES_CURRENT_TEST
If ANY of:
1. DOM exceeds action-type+target PMI on >= 1/3 sites (MI(S_next; DOM) > MI(S_next; A) by >= 0.05 bits)
2. MI(S_next; DOM | A) > 0.1 bits on >= 1/3 sites (DOM adds substantial predictive power beyond action)

This would indicate hidden session dynamics or non-trivial environmental structure on deterministic SPAs.

### 11.3 MEASUREMENT_INVALID
If:
1. Positive or null control fails
2. Data sufficiency fails (n_test < 30 on >= 2/3 sites)
3. Pipeline errors prevent computation
4. MI computations produce negative values (should not occur for MI but indicates implementation error)

## 12. Expected Outcomes

### 12.1 FALSIFIED-IN-SETTING (Expected)
- Action-label PMI dominates on all 3 deterministic SPAs
- DOM PMI does not exceed action-type+target PMI
- MI(S_next; DOM | A) is negligible
- Confirms that DOM visible_text_hash PMI is tautological FSM state recovery
- C-WEB-DYNAMICS 'beyond memory' is not supported on deterministic SPAs
- **Consequence**: Physics lane must investigate production SPAs with non-deterministic rendering where action labels may not be sufficient statistics

### 12.2 SURVIVES_CURRENT_TEST (Surprising)
- DOM exceeds action-type+target PMI on some sites
- MI(S_next; DOM | A) is substantial
- Would indicate hidden session dynamics not captured by action labels
- Would justify DOM integration as non-trivial physics
- **Consequence**: Investigate mechanism (server session state, hidden form fields, dynamic rendering)

### 12.3 MEASUREMENT_INVALID
- Pipeline or data issues prevent valid comparison
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Load existing data**: Read raw_dom_captures.json from EXP-PHYSICS-34719136202
2. **Extract action labels**: From trajectory metadata, extract action_type (click/fill/submit/navigate) and action_target (target_href), combine as categorical label
3. **Compute MI(S_next; A)**: Action-label PMI using same framework as parent (quantile bins, alpha smoothing, 80/20 temporal split)
4. **Compute MI(S_next; DOM)**: DOM-feature PMI (reuse parent DOM PMI values as regression check)
5. **Compute MI(S_next; A, DOM)**: Combined PMI
6. **Compute MI(S_next; DOM | A)**: Conditional MI = MI(S_next; A, DOM) - MI(S_next; A)
7. **Compute MI(S_next; A | DOM)**: Conditional MI = MI(S_next; A, DOM) - MI(S_next; DOM)
8. **Permutation tests**: 1000 permutations for each MI computation
9. **Alpha sensitivity**: Repeat at alpha = 0.0, 0.5, 1.0, 2.0
10. **Controls**: Verify positive control (synthetic with counter) and null control (shuffled labels)
11. **Decision**: Apply frozen decision rule

## 14. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations
- `scipy.stats` for permutation tests
- `hashlib` for SHA-16 hash computation (matching parent)
- PMI computation framework from parent experiment pmi_dom_features.py

Code will be committed to `research/experiments/EXP-PHYSICS-34724244876/` before execution.

## 15. Pre-registered Expectations

From prior work:
- DOM visible_text_hash PMI: dashboard 1.006, multistep 0.286, wizard 0.438 (parent)
- MI(action; DOM): dashboard 1.989, multistep 0.467, wizard 0.468 (parent audit recomputation)
- Action-label PMI MI(S_next; A) is expected to be high on deterministic SPAs (action type determines next state)
- DOM PMI MI(S_next; DOM) is expected to be similar to or lower than action-type+target PMI
- MI(S_next; DOM | A) is expected to be near zero (DOM adds nothing beyond action)
- This would confirm the tautology finding from parent audit

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.