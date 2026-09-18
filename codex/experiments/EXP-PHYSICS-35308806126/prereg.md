# Preregistration: EXP-PHYSICS-35308806126

## Background

The parent experiment (EXP-PHYSICS-35290611436) demonstrated that URL-level PMI on TodoMVC hash-SPAs is entirely Markov: conditional PMI at K=3 is exactly 0.0 bits on all 5 variants, meaning the 3-step action history fully determines the next URL on these minimal deterministic SPAs. The parent's carry_forward explicitly states:

- **Established:** URL-level PMI (fragment-preserving) reproduces parent signal exactly: 0.187-0.204 bits unconditional K=0.
- **Rejected:** Beyond-Markov URL-level PMI on TodoMVC hash-SPAs: 0/5 variants achieve K=3 PMI > 0.05 bits.
- **Unknown:** Whether production SPAs with >10 unique URL states, stochastic transitions, and history-based routing exhibit beyond-Markov URL-level PMI at K=3 or higher where H_K=3 does NOT determine next state.
- **Do not assume:** C-WEB-DYNAMICS is globally false based on this TodoMVC falsification. TodoMVC's 3-4 state deterministic ceiling trivially satisfies H_K=3 determination; production SPAs with larger state spaces may not.

The current experiment tests the dominant unknown: whether beyond-Markov URL-level PMI exists on production SPAs where H_K=3 does NOT fully determine the next URL state.

## Hypothesis

**H1 (beyond-Markov):** I(url_after; action | url_before, H_K=3) > 0.05 bits on >=2/3 production SPAs, demonstrating that action provides predictive information about the next URL beyond what the previous 3 actions and current URL determine. This would indicate beyond-Markov structure required by C-WEB-DYNAMICS.

**H0 (Markov-only):** I(url_after; action | url_before, H_K=3) <= 0.05 bits on >=2/3 production SPAs, demonstrating the signal is entirely explained by Markov predictability.

## Methods

### Test Sites

Select 3 production SPAs with:
- >10 unique URL states
- Stochastic transitions (auth, pagination, user-dependent content)
- History-based routing (URL alone is ambiguous)
- Publicly accessible without login

Candidate sites:
1. News site with pagination and user-dependent content (e.g., BBC News)
2. E-commerce site with search filters and session-dependent recommendations (e.g., Amazon product search)
3. Social media site with infinite scroll and user-specific feed (e.g., Twitter/X)

### Data Collection

- Playwright browser collection with cookie/session support
- Collect 500 raw transitions per SPA across multiple sessions
- Action primitives: form_submit, button_click, js_navigate, scroll, search_submit, etc.
- Session grouping: group transitions by session field to form trajectories

### Filtering

- Non-leakage filter: action_primitive != 'link_click' (link clicks are leakage per prior audit)
- Minimum 100 non-leakage transitions per SPA after filtering

### History Construction

For each transition at step t in a trajectory:
- H_K = (action_{t-K}, ..., action_{t-1}) is the sequence of K action labels preceding the current action
- For t < K, pad with START_TOKEN at the beginning

### PMI Estimation

- alpha=0 (no Laplace smoothing) for all PMI computations
- Conditional PMI: for each action-history stratum h = (url_before, H_K), compute PMI between action_t and url_after_t within the stratum, then average across strata weighted by stratum frequency
- Permutation test: 1000 cross-trajectory shuffles of action labels within sessions, seed=42
- Bonferroni correction: 3 primary comparisons (3 SPAs), alpha = 0.05/3 ≈ 0.0167

### Controls

- **Positive control:** Synthetic deterministic SPA with 8 states, 4 actions, known action->next-state mapping. Conditional PMI at K=3 must be >= 1.0 bits with permutation p < 0.001.
- **Null control:** Shuffled-action permutation test within sessions. Expected mean shuffled PMI = 0.0 bits.
- **Normalized URL PMI (fragment-stripped):** Expected to be reduced compared to full URL PMI.

## Analysis Plan

1. Compute unconditional PMI (K=0) for each SPA
2. Compute conditional PMI at K=1 and K=3 for each SPA
3. Run permutation tests for each K level
4. Compute action-history prediction accuracy at each K level
5. Evaluate positive and null controls
6. Apply frozen decision rule

## Decision Rule

If ALL of:
1. >= 2/3 production SPAs achieve conditional PMI at K=3 > 0.05 bits AND Bonferroni-corrected permutation p < 0.0167
2. Positive control conditional PMI at K=3 >= 1.0 bits
3. >= 100 non-leakage transitions per SPA
4. Unconditional PMI at K=0 is positive (> 0.05 bits on >= 2/3 SPAs)

Verdict = SURVIVES_CURRENT_TEST (beyond-Markov structure demonstrated on production SPAs)

If fewer than 2/3 production SPAs achieve conditional PMI at K=3 > 0.05 bits:
Verdict = FALSIFIED-IN-SETTING (signal is entirely Markov on these production SPAs; no beyond-memory structure)

If controls fail or data quality insufficient:
Verdict = MEASUREMENT_INVALID

## Expected Outcomes

**Positive outcome:** Beyond-Markov URL-level PMI on production SPAs. This elevates C-WEB-DYNAMICS from HYPOTHESIS to EXPERIMENTAL and justifies investigation of practical utility for SPIDER exploration.

**Negative outcome:** URL-level PMI is entirely Markov on production SPAs. This narrows the claim ceiling and suggests orthogonal detection methods (DOM, accessibility tree, visual layout) or alternative claims.

**Invalid outcome:** Infrastructure failure or data quality issues. No scientific inference.

## Validity Threats

1. **Site selection bias:** Candidate SPAs may not have genuine history-based routing. Mitigation: select sites with known client-side routing and URL ambiguity.
2. **Action representation loss:** URL-only representation discards DOM, visual, and network information. This is acknowledged and bounded in the claim ceiling.
3. **Leakage misclassification:** Some link clicks may be non-leakage. Mitigation: conservative link_click filter per prior audit.
4. **Sample size:** 500 raw transitions per SPA may yield <100 NL transitions after filtering. Mitigation: collect extra transitions to ensure sufficient NL transitions.
5. **Stochastic transitions:** Production SPAs may have stochastic transitions but H_K=3 may still determine next state. Mitigation: sites selected for history-based routing where URL alone is ambiguous.
6. **Representation loss:** URL-only representation discards DOM, visual, and network information. This is acknowledged and bounded in the claim ceiling.
7. **Model/agent policy dependence:** Action primitives are extracted from Playwright, not from an LLM agent. This is bounded in the claim ceiling.
8. **Non-stationarity:** Production SPAs may change during data collection. Mitigation: collect data within a short time window (1 day).
9. **Session continuity:** Browser sessions may not capture genuine user sessions. Mitigation: use separate browser contexts with distinct cookies.

## Representation Loss

- URL-only representation discards DOM, visual, and network information
- Action primitives are categorical (form_submit, button_click, etc.) and discard action parameters
- Session grouping by cookie may not capture genuine user sessions
- Link click filter may remove non-leakage transitions
- Bonferroni correction for 3 SPAs is conservative

## Parent Handoff Reference

Parent: EXP-PHYSICS-35290611436 (handoff.json sha256 f1d4b4593d2f877220a51a17bf90cde0c7b93db4d4a01f4c9a65f31a23ab3007)

Carry forward from parent:
- **Established:** URL-level PMI (fragment-preserving) reproduces parent signal exactly: 0.187-0.204 bits unconditional K=0.
- **Rejected:** Beyond-Markov URL-level PMI on TodoMVC hash-SPAs: 0/5 variants achieve K=3 PMI > 0.05 bits.
- **Unknown:** Whether production SPAs with >10 unique URL states, stochastic transitions, and history-based routing exhibit beyond-Markov URL-level PMI at K=3 or higher where H_K=3 does NOT determine next state.
- **Do not assume:** C-WEB-DYNAMICS is globally false based on TodoMVC falsification. TodoMVC's 3-4 state deterministic ceiling trivially satisfies H_K=3 determination; production SPAs with larger state spaces may not.

## Stable Metric/Control Identities

- **Primary metric:** conditional_pmi_k3_by_spa (bits)
- **Baseline metrics:** unconditional_pmi_k0_by_spa, conditional_pmi_k1_by_spa, prediction_accuracy_by_k_by_spa
- **Positive control:** POSITIVE_CONTROL_SYNTHETIC_SPA
- **Null control:** NULL_CONTROL_SHUFFLED_ACTIONS
- **Normalized URL control:** NULL_CONTROL_NORMALIZED_URL
- **Decision threshold:** 0.05 bits, Bonferroni alpha = 0.0167
- **Minimum NL transitions:** 100 per SPA
- **Minimum SPA success:** 2/3
