# EXP-PHYSICS-35651906573 preregistration

## Status

DESIGN ONLY — not yet frozen.

## Experiment Identity

- **experiment_id**: EXP-PHYSICS-35651906573
- **lane**: physics
- **claim_ids**: ["C-WEB-DYNAMICS"]
- **parent_handoff**: EXP-PHYSICS-35578258358 (Bayesian DM SURVIVES_CURRENT_TEST on synthetic 12-state SPA)
- **director_mandate**: CONTINUE on C-WEB-DYNAMICS, cognitive_reset=true

## Question

Does the Bayesian Dirichlet-Multinomial model comparison maintain valid null centering (C1: null median < 0) and detection sensitivity (C3: p < 0.001) on real TodoMVC hash-SPA transitions at URL-level, where state representation is fragment-aware (not synthetic state_id) and transitions are genuine browser interactions?

## Hypothesis (H1)

The Bayesian DM model comparison with K=12 passes both C1 (null median < 0 nats) and C3 (permutation p < 0.001) on at least 2/5 TodoMVC hash-SPA variants using URL-level state representation with fragment-aware normalization.

## Falsifier (H0)

The hypothesis is falsified if ANY of:
1. ALL 5 TodoMVC variants fail either C1 or C3
2. Fewer than 2/5 variants achieve >=50 non-leakage transitions
3. Positive control (synthetic 12-state SPA) fails C1 or C3
4. Measurement validity fails on all variants

## State Representation

**State**: URL with fragment-aware normalization. Same as parent EXP-PHYSICS-35209110569:
- Strip trailing slash
- Decode percent-encoding
- Preserve fragment (e.g., `#/active`, `#/completed` are distinct states)
- Example: `todomvc.com/examples/vanillajs/#/active` ≠ `todomvc.com/examples/vanillajs/#/completed`

**History**: State-history K2 = (url_before + 2 previous URLs). Same as parent EXP-PHYSICS-35578258358.

**Action**: URL of the action target (action.target_href). Same as parent.

## Model Specification

**Bayesian Dirichlet-Multinomial** with:
- K = n_states = 12 (maximum number of distinct next-states per (state, action) pair)
- alpha_prior ∈ {0.5, 1.0, 2.0}
- State-history K2 = (url_before + 2 previous URLs)
- Log Bayes Factor: log BF = log P(M1|data) - log P(M0|data)
  - M1: P(url_after | url_before, H_K2) varies across actions (action-conditioned)
  - M0: P(url_after | url_before, H_K2) is action-independent (memory only)

**Implementation**: Same run_experiment.py as parent EXP-PHYSICS-35578258358, with corrected K=12 (not K=len(counts)).

## Data Collection

### Target Sites

5 TodoMVC hash-SPA variants:
1. vanilla JS (ES6): `todomvc.com/examples/vanillajs/`
2. React: `todomvc.com/examples/react/`
3. Vue: `todomvc.com/examples/vue/`
4. Angular: `todomvc.com/examples/angular/`
5. Svelte: `todomvc.com/examples/svelte/`

All use hash-based client-side routing (`#/active`, `#/completed`, `#/`).

### Collection Protocol

- Playwright headless Chrome
- Per-transition record: URL (before), URL (after), action target (href or element), action primitive (click, submit, type, keypress, js_navigate), timestamp
- At least 5 distinct sessions per variant (different starting points, action sequences)
- Target N=5000 raw transitions per variant (matching parent sample size)
- No authentication required

### Leakage Definition

Same as parent: `action.target_href == state_after.url` (same URL after normalization).

Link-click transitions have 100% leakage by design (the href IS the next URL). Non-link transitions (button_click, form_submit, js_navigate) have 0% leakage.

From EXP-PHYSICS-35209110569: all 5 variants have leakage 21-28%, achievable NL 357-394 at 500 raw.

## Analysis Plan

### Primary Analysis

For each variant:
1. Filter to non-leakage transitions (action.target_href ≠ state_after.url)
2. Compute within-session shuffled-action null distribution (N_SHUFFLE=1999)
3. Compute Bayesian DM log BF on real data
4. Test C1: null median < 0 nats
5. Test C3: permutation p < 0.001 (fraction of null BF ≥ observed BF)

### Baselines

1. **URL-only PMI**: I(url_after; action | url_before) without history conditioning
2. **Action-history accuracy**: P(determine url_after | url_before, H_K=3)
3. **State-history K=2 PMI**: I(url_after; url_before, H_K=2) using plug-in estimator

### Positive Control

Synthetic 12-state stochastic hash-routed SPA with N=5000, seed=42. Same as parent.

### Null Control

Within-session shuffled-action permutation (N_SHUFFLE=1999). Same framework as parent.

## Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:
- C1: null median < 0 nats on >=2/5 variants
- C3: permutation p < 0.001 on >=2/5 variants
- C5: >=50 non-leakage transitions on >=2/5 variants
- C6: positive control passes (C1+C3 on synthetic SPA)
- C7: no measurement validity violations

**FALSIFIED-IN-SETTING** if C1 or C3 fails on all 5 variants.

**MEASUREMENT_INVALID** if C6 fails (positive control broken) or C5 fails (insufficient data).

**MIXED** if some variants pass and others fail. Claim ceiling bounded to passing variants only.

## Validity Threats

1. **Title degeneracy**: TodoMVC variants have constant document.title (unique_titles=1, from EXP-PHYSICS-35209110569). This means URL+title is isomorphic to URL-only. Title-aware PMI is NOT tested in this experiment — only URL-level PMI.

2. **Deterministic FSM**: TodoMVC is a deterministic finite-state machine (3-4 states). Action-history K=3 fully determines next state (accuracy 1.0 from parent EXP-PHYSICS-35290611436). This means I(url_after; action | url_before, H_K=3) = 0 by mathematical identity for K=3. The Bayesian test uses K=2 (state-history), not K=3, so this is not a direct confound — but the environment has limited stochasticity.

3. **Synthetic→real gap**: TodoMVC is a minimal SPA, not a production application with high-cardinality state spaces, stochastic transitions, or complex DOM evolution. Success on TodoMVC does NOT establish C-WEB-DYNAMICS for production SPAs.

4. **Leakage filtering**: Link-click transitions (27% of all transitions from EXP-PHYSICS-35209110569) are removed by the NL filter. This reduces effective sample size and may introduce selection bias if non-link transitions are not representative.

5. **Null framework limitation**: The within-session shuffled-action null has known limitations for hash-routed SPA (parent EXP-PHYSICS-35389142077 found null_mean=0.417 bits for plug-in PMI). The Bayesian DM bypasses the Laplace smoothing bias but the null centering on real data is untested.

## Scope Limitations

This experiment tests:
- URL-level state representation (not DOM, accessibility tree, or visual)
- TodoMVC hash-SPAs (3-4 states, deterministic FSM)
- Bayesian DM with K=12 (not other estimator families)
- Non-leakage transitions only (link-clicks excluded)

This experiment does NOT test:
- Production SPAs with high-cardinality state spaces
- Stochastic transitions (e.g., user-dependent content)
- Richer state representations
- Title-aware PMI (TodoMVC has constant title)
- Beyond-Markov dynamics (K3-K2 comparison is exploratory only)

## Expected Outcomes and Consequences

**Positive (>=2/5 variants pass C1+C3)**:
- Bayesian estimator validated on real browser transitions
- Opens path to production SPA testing
- Synthetic→real gap bridged for URL-level state representation
- Claim ceiling: TodoMVC hash-SPAs with URL-level state

**Negative (all variants fail C1 or C3)**:
- Synthetic→real gap is the binding bottleneck
- Physics lane should consider:
  - Continuous-state estimators (KDE/kNN on embeddings)
  - Richer state representations (DOM, accessibility tree)
  - Abandoning URL-level PMI for production SPAs
- Claim ceiling unchanged: Bayesian DM validated on synthetic SPA only

**Mixed (some pass, some fail)**:
- Claim ceiling bounded to passing variants only
- Identify what distinguishes passing vs failing variants
- Consider variant-specific analysis
