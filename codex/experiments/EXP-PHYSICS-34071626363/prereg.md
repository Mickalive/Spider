# EXP-PHYSICS-34071626363 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34071626363
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-07
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-PHYSICS-34038570933 (FALSIFIED-IN-SETTING)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does pointwise mutual information (PMI) between actions and next-states, conditioned on current state, remain positive when action-to-destination URL leakage is eliminated (i.e., transitions where action.target_href != state_after.url)?

## 3. Motivation

### What the parent experiment established (EXP-PHYSICS-34038570933)

The parent experiment tested PMI between actions and next-states on live Web transitions using URL-level state representation.

**Established (descriptive):**
- PMI pipeline is computationally correct: positive control detects deterministic synthetic structure (d=50.4, p=0.001); null control correctly does not reject random data (p=1.0)
- PMI > 0 on live data with unblinded actions (all 4 primary tests pass permutation after Bonferroni correction, p_bonf=0.004, d=3.5-14.5)
- Self-loop rates: Wikipedia 17.6%, Python docs 49.5%

**Rejected (measurement invalid):**
- PMI at URL-only representation with unblinded actions as evidence for C-WEB-DYNAMICS: FALSIFIED-IN-SETTING per frozen decision_rule and audit action_leakage critical finding
- The critical audit finding: action_leakage_href_equals_next: 92-98% of actions encode the next URL, meaning PMI collapses to -log P(a|s) for those transitions
- Producer claim that 'PMI detects action-conditioned structure that accuracy cannot': unsupported because PMI inherits the same href-to-next leakage

**Unknown:**
- Whether blinded action representations (hashed href, action_type only) would yield PMI > 0 — the identifiability test for state contribution beyond trivial mapping was not performed
- Whether the non-leakage subset (action.target_href != state_after.url) has positive PMI
- Whether JavaScript-heavy SPA sites or form-heavy sites (where action.target_href != state_after.url by construction) have action-conditioned dynamical structure

**Do Not Assume:**
- That PMI > 0 on live data indicates action-conditioned structure beyond trivial href-to-destination mapping — the signal is confounded by action leakage (92-98% href==next)
- That the shuffled-action null is a strong null for Web dynamics — it does not preserve the action-to-next mapping
- That PMI at URL level generalizes to C-WEB-DYNAMICS for richer representations or different site types

### Why this experiment is different

The parent experiment used **unblinded actions** where action.target_href is the actual destination URL. The audit found that 92-98% of transitions have action.target_href == state_after.url, meaning PMI is confounded by this trivial equality. This experiment isolates the **non-leakage subset** where action.target_href != state_after.url, eliminating the trivial mapping and testing for genuine state-conditioned structure.

**Key insight**: If PMI is positive on non-leakage transitions, it demonstrates that actions and next-states are statistically associated even when actions do not trivially encode the next URL. This would be evidence for genuine Web dynamics beyond mechanical URL mapping.

## 4. Hypotheses

### H1: Positive PMI on Non-Leakage Transitions
Mean PMI between actions and next-states (conditioned on current state) is > 0 on non-leakage transitions (action.target_href != state_after.url) for both live sites, and significantly exceeds the shuffled-action null (permutation test p < 0.05 after Bonferroni correction).

### H2: Positive Control
PMI on synthetic lambda=1.0 data (actions fully determine next-state) is >= 1.0 bit. This verifies the PMI computation detects known structure.

### H3: Null Control
PMI on shuffled action labels on non-leakage transitions is not significantly > 0 (permutation test p > 0.05). This verifies the PMI computation does not detect structure when absent.

### H4: Leakage vs Non-Leakage Comparison
PMI on non-leakage subset is >= PMI on all transitions (excluding leakage does not reduce the signal). This is exploratory.

## 5. Data Sources

### 5.1 Parent Experiment Raw Data

This experiment re-uses raw transition data from the parent experiment (EXP-PHYSICS-33965269281). No new data collection is required.

**Files:**
- `research/experiments/EXP-PHYSICS-33965269281/raw_live_wikipedia.json` (sha256: 87e6d8fcecb436ab9b1067a27c7f5708c393bace5efbb0225bfe1f57aa87bc5e) — 880 transitions, 110 trajectories
- `research/experiments/EXP-PHYSICS-33965269281/raw_live_python_docs.json` (sha256: a7634ca3734360a4d6a2ffdb89d859ae9ff466df710be3323da8ac5c5d2fa648) — 880 transitions, 110 trajectories
- `research/experiments/EXP-PHYSICS-33965269281/raw_positive.json` (sha256: 3eef0bbc382fef44eb63d55481e3d417b2a98478d6f4fa4e1eb06331a99fc73f) — 600 transitions, 60 trajectories, lambda=1.0

### 5.2 Non-Leakage Subset Identification

A transition is classified as **non-leakage** if `action.target_href != state_after.url` after normalization:
- Strip trailing slash, lowercase scheme/host
- For relative URLs, resolve against base URL (state_before.url)
- Non-leakage transitions are those where the action's target href does not match the resulting URL

From preliminary analysis:
- Wikipedia: 67 non-leakage transitions (7.6% of 880)
- Python docs: 13 non-leakage transitions (1.5% of 880)

### 5.3 State Representation for PMI

The parent experiment uses URL as the state identifier for PMI computation. This experiment maintains the same representation for comparability.

## 6. PMI Computation

### 6.1 Pointwise Mutual Information

For a transition (s, a, s'), the PMI is:

```
PMI(s, a, s') = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]
```

### 6.2 Probability Estimation

For a given dataset of transitions {(s_i, a_i, s'_i)}:

**Conditional marginals (conditioned on current state s):**
- P(a | s) = count(s, a) / count(s) + alpha / (count(s) + alpha * |A_s|)
- P(s' | s) = count(s, s') / count(s) + alpha / (count(s) + alpha * |S'_s|)

**Joint conditional:**
- P(a, s' | s) = count(s, a, s') / count(s)

Where:
- count(s) = number of transitions from state s
- count(s, a) = number of transitions from s with action a
- count(s, s') = number of transitions from s to s'
- count(s, a, s') = number of transitions (s, a, s')
- alpha = 1.0 (Laplace smoothing for marginal estimates)
- |A_s| = number of distinct actions from s
- |S'_s| = number of distinct next-states from s

### 6.3 Mean PMI

For a dataset D of N transitions:

```
mean_PMI(D) = (1/N) * sum_i PMI(s_i, a_i, s'_i)
```

### 6.4 Shuffled-Action PMI

For each permutation p (1000 total):
1. Within each trajectory, randomly permute action labels (preserving trajectory structure)
2. Compute mean PMI on the shuffled dataset
3. The shuffled-action PMI distribution provides the null for testing mean_PMI > 0

### 6.5 Trajectory-Grouped Shuffling

Action labels are shuffled **within trajectories**, not across the entire dataset. This preserves:
- Trajectory-level state distributions
- Temporal ordering of states
- The marginal distribution of states

Only the action-state association is destroyed.

## 7. Measures

### 7.1 Primary Metrics
- **mean_pmi_non_leakage_wiki**: Mean PMI across non-leakage transitions on Wikipedia
- **mean_pmi_non_leakage_python**: Mean PMI across non-leakage transitions on Python docs
- **permutation_p_value_non_leakage**: Fraction of shuffled PMI values >= observed PMI (one-sided) for non-leakage subset

### 7.2 Secondary Metrics
- **mean_pmi_all_wiki**: Mean PMI across all transitions (parent baseline)
- **mean_pmi_all_python**: Mean PMI across all transitions (parent baseline)
- **mean_pmi_hashed_wiki**: Mean PMI with hashed action representation (sha256 of target_href)
- **mean_pmi_hashed_python**: Mean PMI with hashed action representation
- **mean_pmi_action_type_wiki**: Mean PMI with action_type categorical only (all 'click')
- **mean_pmi_action_type_python**: Mean PMI with action_type categorical only
- **non_leakage_fraction_wiki**: Fraction of non-leakage transitions on Wikipedia
- **non_leakage_fraction_python**: Fraction of non-leakage transitions on Python docs
- **unique_states_non_leakage**: Number of unique states in non-leakage subset
- **unique_actions_non_leakage**: Number of unique actions in non-leakage subset
- **unique_sa_pairs_non_leakage**: Number of unique (state, action) pairs in non-leakage subset

### 7.3 Comparison Metrics
- **diff_pmi_non_leakage_vs_all**: Mean PMI(non-leakage) - Mean PMI(all)
- **leakage_confounding_estimate**: Estimated contribution of leakage to PMI(all)

## 8. Null Models

### 8.1 Shuffled-Action Null
Permute action labels within trajectories (1000 permutations). PMI on shuffled data should be ~0 when actions carry no information about next-states. This is the primary null for testing H1.

### 8.2 Frequency Null
Under no action-dependence, P(a, s'|s) = P(a|s) * P(s'|s), so PMI = 0. The frequency null is analytically equivalent to the shuffled-action null at the population level; finite-sample deviations are captured by the permutation test.

## 9. Statistical Tests

### 9.1 Primary Test: PMI > 0 on Non-Leakage Subset
- One-sided permutation test: H0: mean_PMI <= 0, H1: mean_PMI > 0
- Test statistic: mean_PMI on observed non-leakage data
- Null distribution: mean_PMI on 1000 shuffled-action datasets
- p-value = (number of shuffled PMI >= observed PMI + 1) / (1000 + 1)
- **Bonferroni correction for 2 comparisons** (2 live sites)
- Significance threshold: p < 0.05 / 2 = 0.025

### 9.2 Secondary Test: PMI > Shuffled PMI
- Paired comparison: mean_PMI(observed) vs mean_PMI(shuffled) across trajectories
- One-sided: observed > shuffled
- Wilcoxon signed-rank test on per-trajectory PMI differences

### 9.3 Effect Size
- Cohen's d for mean_PMI(observed) vs mean_PMI(shuffled)
- Report confidence intervals for mean PMI at each site

### 9.4 Leakage Comparison
- Paired comparison: mean_PMI(non-leakage) vs mean_PMI(all) at each site
- One-sided: non-leakage >= all (excluding leakage does not reduce signal)

## 10. Controls

### 10.1 Positive Control (Synthetic lambda=1.0)
- PMI >= 1.0 bit on synthetic data with deterministic action->next-state mapping
- This verifies: PMI computation is correct, known structure is detectable

### 10.2 Null Control (Shuffled Actions on Non-Leakage)
- PMI not significantly > 0 on shuffled non-leakage data (permutation p > 0.05)
- This verifies: PMI computation does not detect structure when absent

### 10.3 Leakage Prevalence Control
- Report non-leakage fraction per site (expected: wiki ~7.6%, python ~1.5%)
- If non-leakage fraction < 5% at a site, power is limited; interpret results cautiously

## 11. Validity Threats

### 11.1 Small Non-Leakage Sample Size
With only 67 non-leakage transitions on Wikipedia and 13 on Python docs, power is limited for detecting small effects. **Mitigation**: report effect sizes and confidence intervals; focus on Wikipedia where sample is larger; interpret Python docs as supportive/contradictory rather than primary.

### 11.2 Sparse State Spaces in Non-Leakage Subset
Non-leakage transitions are a small subset, potentially with even sparser state spaces. **Mitigation**: Laplace smoothing mitigates log(0); permutation test is robust to sparse estimation.

### 11.3 Selection Bias in Non-Leakage Transitions
Non-leakage transitions may be systematically different from leakage transitions (e.g., form submissions, JavaScript navigation). **Mitigation**: this is intentional — we are testing whether these structurally different transitions have action-conditioned dynamics.

### 11.4 Synthetic-to-Real Gap
Synthetic positive control validates the PMI computation on known structure. Real Web dynamics may be fundamentally different. **Mitigation**: this is a necessary validation step.

### 11.5 Multiple Comparisons
2 primary comparisons (2 sites) with Bonferroni correction. **Mitigation**: correction is conservative; report both corrected and uncorrected p-values.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Mean PMI on non-leakage Wikipedia transitions > 0, permutation p < 0.025 (Bonferroni x2)
2. Mean PMI on non-leakage Python docs transitions > 0, permutation p < 0.025
3. Synthetic positive control PMI >= 1.0 bit
4. Shuffled-action null control: PMI not significantly > 0 (permutation p > 0.05)
5. No pipeline errors

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. PMI not > 0 on non-leakage transitions for both sites after correction
2. Positive control fails (PMI < 1.0 bit)
3. Null control fails (shuffled PMI significantly > 0)

### 12.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. Data loading failure (files missing or corrupted)
3. Fewer than 10 non-leakage transitions per site

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates that action-conditioned structure exists in live Web data beyond trivial action-to-destination mapping
- Validates that PMI can detect genuine Web dynamics when leakage is eliminated
- Justifies: (a) focusing on non-leakage transitions as a clean test bed, (b) designing mechanisms that leverage action-conditioned structure without relying on href-to-URL mapping, (c) investigating SPA/form-heavy sites where non-leakage is more frequent

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- Suggests that the PMI detected in prior experiments was entirely due to trivial action-to-destination leakage
- Does NOT falsify C-WEB-DYNAMICS entirely — only this detection method on these specific sites
- Physics lane should investigate: (a) SPA/form-heavy sites where non-leakage is more frequent, (b) richer state representations, (c) trajectory-level entropy rates

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Data Loading**: Load parent raw data files; verify SHA-256 hashes; extract (state.url, action.target_href, state_after.url) triples
2. **Non-Leakage Identification**: Identify transitions where action.target_href != state_after.url after normalization
3. **PMI Computation**: For each dataset (all, non-leakage), compute PMI using smoothed marginals; aggregate to mean PMI per dataset
4. **Shuffled-Action Null**: For 1000 permutations, shuffle action labels within trajectories, recompute mean PMI
5. **Permutation Test**: Compute p-value = (count shuffled >= observed + 1) / 1001
6. **Bonferroni Correction**: Correct p-values for 2 primary comparisons
7. **Positive Control**: Verify PMI >= 1.0 on synthetic data
8. **Null Control**: Verify shuffled PMI not > 0 on non-leakage data
9. **Leakage Comparison**: Compare PMI on all vs non-leakage subsets
10. **Effect Size**: Compute Cohen's d, confidence intervals
11. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `json` for loading parent raw data files
- `hashlib` for SHA-256 verification
- `math` for log2 computation
- `collections.Counter` for frequency counting
- `random.Random` for deterministic permutation tests (seed=42)
- `numpy` for statistical computations (mean, std, Cohen's d)
- Standard library only (no custom estimators required)

Code will be committed to `research/physics/information_theoretic/` before execution.

## 16. Pre-registered Expectations

From prior work and theoretical reasoning:
- The parent experiment found PMI > 0 but confounded by 92-98% leakage
- Non-leakage transitions are rare (7.6% wiki, 1.5% python) but may have genuine dynamics
- Expected PMI on non-leakage subset: modestly positive (>0) if any action-conditioned structure exists; near 0 if sites are truly unstructured at URL level
- Expected PMI on hashed action representation: similar to unblinded (preserves uniqueness)
- Expected PMI on action-type categorical: near 0 (all actions are 'click')

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.