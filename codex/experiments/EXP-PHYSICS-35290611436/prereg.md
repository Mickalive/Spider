# EXP-PHYSICS-35290611436 — Preregistration

## Experiment

History-conditioned URL PMI on TodoMVC hash-SPAs: testing beyond-Markov structure

## Lane

Physics

## Claim

C-WEB-DYNAMICS: Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity.

## Question

Does URL-level PMI remain significantly positive when conditioned on truncated action-history I(url_after; action | url_before, H_K) for K=1,3 on TodoMVC hash-SPA testbeds, or is the observed 0.188-0.209 bit signal from EXP-PHYSICS-35262258744 entirely explained by memoryless Markov dynamics?

## Hypothesis

**H1 (beyond-Markov):** I(url_after; action | url_before, H_K=3) > 0.05 bits on >=3/5 TodoMVC variants, demonstrating that action provides predictive information about the next URL beyond what the previous 3 actions and current URL determine.

**H0 (Markov-only):** I(url_after; action | url_before, H_K=3) <= 0.05 bits on >=3/5 variants, demonstrating the parent's 0.188-0.209 bit signal is entirely explained by Markov predictability.

## Scientific Rationale

The parent experiment (EXP-PHYSICS-35262258744) demonstrated that URL-level PMI is significantly positive (0.188-0.209 bits, p=0.001, 5/5 variants) when URL fragments are preserved on TodoMVC hash-SPAs. However, audit V7 (identifiability) found that this signal could be entirely explained by Markov dynamics: on deterministic TodoMVC transitions, (url_before, action) -> url_after is a deterministic mapping, so I(url_after; action | url_before) > 0 is trivially true.

To test whether the signal contains beyond-Markov structure, we condition on action history H_K and compute I(url_after; action | url_before, H_K). If the signal is entirely Markov, conditioning on H_K=3 should reduce PMI to 0 (because (url_before, H_K=3) fully determines url_after on deterministic 3-4 state FSMs). If PMI remains > 0 at K=3, there is beyond-Markov structure.

This is the critical identifiability test for C-WEB-DYNAMICS on TodoMVC: it determines whether the URL-level PMI signal demonstrates genuine predictive dynamical structure or merely reflects deterministic state transitions.

## Data

- **Source:** Reuse parent raw transition files from research/experiments/EXP-PHYSICS-35209110569/
- **Files:** raw_{variant}.json and raw_{variant}_topup.json for vanillajs, react, vue, angular, svelte
- **No new browser collection required**
- **Non-leakage filter:** action_primitive != 'link_click' (all link_click are leakage on hash-SPAs)
- **Expected NL per variant:** 85-93 (parent achieved this range)

## Analysis Plan

### 1. Data Loading and Preprocessing

For each variant:
1. Load raw_{variant}.json and raw_{variant}_topup.json
2. Recombine and deduplicate
3. Apply non-leakage filter (action_primitive != 'link_click')
4. Group transitions by session to form trajectories
5. Sort transitions within each trajectory by timestamp

### 2. History Construction

For each transition at step t in a trajectory:
- H_K = (action_{t-K}, ..., action_{t-1}) — the K action labels preceding the current action
- For t < K, pad with START_TOKEN at the beginning
- Action labels: action_primitive categorical (form_submit, button_click, js_navigate)

### 3. Conditional PMI Computation

For K = 0, 1, 3:

For each action-history stratum h = (url_before, H_K):
1. Extract transitions in this stratum
2. If stratum size < 5, skip (insufficient data)
3. Compute joint distribution P(action_t, url_after | h)
4. Compute marginals P(action_t | h) and P(url_after | h)
5. Compute PMI_h = sum_{a,s} P(a,s|h) * log2[P(a,s|h) / (P(a|h) * P(s|h))]
6. Weight by stratum frequency: weight = n_h / N_total

Conditional PMI = sum_h weight_h * PMI_h

**No smoothing (alpha=0):** Both joint and marginal probabilities computed without Laplace smoothing to avoid the artifact that caused parent C2 failure.

### 4. Permutation Test

For each variant and K:
1. Shuffle action labels within each trajectory (preserves action distribution, destroys action->next_url association)
2. Recompute conditional PMI on shuffled data
3. Repeat 1000 times (seed=42)
4. Compute p-value: fraction of shuffled PMIs >= observed PMI
5. Apply Bonferroni correction: p_bonf = min(p * 5, 1.0)

### 5. Action-History Prediction Accuracy

For each K, compute accuracy of predicting url_after from (url_before, H_K) using majority vote within each stratum. This quantifies how much of the next-state is determined by history alone.

### 6. Positive Control

Synthetic deterministic SPA with 8 states, 4 actions, known action->next-state mapping. Conditional PMI at K=3 must be >= 1.0 bits with permutation p < 0.001.

### 7. Null Controls

- **Normalized URL PMI (alpha=0):** Expected = 0.0 bits exactly (fragment-stripping collapses all URLs to 1 state)
- **Shuffled-action permutation:** Expected mean = 0.0 bits (destroys action->next_url association)

## Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:
1. >= 3/5 variants achieve conditional PMI at K=3 > 0.05 bits AND Bonferroni-corrected permutation p < 0.01
2. Positive control conditional PMI at K=3 >= 1.0 bits
3. >= 50 non-leakage transitions per variant
4. Unconditional PMI at K=0 > 0.05 bits on >= 3/5 variants (reproduces parent signal)

**FALSIFIED-IN-SETTING** if fewer than 3/5 variants achieve conditional PMI at K=3 > 0.05 bits (signal is entirely Markov).

**MEASUREMENT_INVALID** if controls fail or data quality insufficient.

## Falsification

The claim is falsified (H0 supported) if:
- Fewer than 3/5 variants achieve conditional PMI at K=3 > 0.05 bits with Bonferroni p < 0.01
- This would demonstrate the parent's 0.188-0.209 bit signal is entirely explained by Markov predictability with no beyond-memory component

## Expected Outcomes

**Positive result (H1 supported):** Beyond-Markov structure exists on TodoMVC hash-SPAs. The URL-level PMI signal contains predictive information beyond what action-history provides. This elevates C-WEB-DYNAMICS from HYPOTHESIS toward EXPERIMENTAL on these testbeds.

**Negative result (H0 supported):** Signal is entirely Markov. The 0.188-0.209 bits reflects deterministic (url, action) -> next_url transitions with no beyond-memory component. C-WEB-DYNAMICS remains HYPOTHESIS with narrowed ceiling: URL-level PMI on TodoMVC is Markov predictability only.

**Either outcome resolves the dominant unknown** from EXP-PHYSICS-35262258744 with minimal cost.

## Validity Threats

1. **TodoMVC determinism ceiling:** If TodoMVC transitions are 100% deterministic and K=3 is sufficient to uniquely determine url_after, PMI at K=3 = 0 by construction. This is a valid negative result, not a measurement failure.
2. **Small state space:** With only 3-4 states, the action history may be redundant with url_before. The experiment tests whether history adds information beyond URL, not whether the effect is practically large.
3. **Data reuse:** No new browser collection. Parent raw files are reused. Integrity relies on parent hashes.
4. **Estimator bias:** alpha=0 may cause issues with empty strata (PMI undefined when P(a,s|h) = 0 for all (a,s)). Empty strata are excluded (stratum size < 5).
5. **Generalization:** Results apply only to TodoMVC hash-SPAs. Production SPAs with history routing, auth, and richer state spaces are untested.
