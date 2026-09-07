# EXP-PHYSICS-34038570933 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34038570933
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-06
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-PHYSICS-33965269281 (MEASUREMENT_INVALID)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Can pointwise mutual information (PMI) between actions and next-states, conditioned on current state, detect action-conditioned structure on live Web pages that point-prediction accuracy metrics fail to detect due to sparse state spaces and self-loop contamination?

## 3. Motivation

### What the parent experiment established (EXP-PHYSICS-33965269281)

The parent experiment tested action-conditioned predictive accuracy (SA) against action-frequency (AF) and shuffle baselines on live Web transitions using browser-based collection with composite state representation (url, title, link_texts, tag_counts, form_signals).

**Established (descriptive):**
- Browser collection successfully gathered 880 transitions per site (Wikipedia, Python docs), 110 trajectories each, 0 failures
- Synthetic positive control: SA held-out 1.0 vs AF 0.678, permutation p=0.0 — pipeline can learn deterministic transitions
- Trajectory-grouped permutation null correctly fails to reject on random data: SA=0.0, p=0.241
- HTTP fetch + HTMLParser can collect transitions on server-rendered sites (established by prior EXP-PHYSICS-33788037373)

**Rejected (measurement invalid):**
- Predictive accuracy (S,A)->S' as detection method for live Web dynamics: extreme memorization (wiki train 0.998 vs heldout 0.030, ratio 32.9), near-unique SA keys (607 keys for 616 train transitions), self-loop rates 17-49%, SA < AF on both live sites
- Validity gates: trajectory split non-deterministic (PYTHONHASHSEED), Bonferroni 6x not applied (code used 2x), accessibility tree 0% populated, target_href_encoding gate false positive on self-loops
- Browser reveals action-conditioned structure: SA < AF means action alone predicts better than (state, action)

**Unknown:**
- Whether information-theoretic measures (PMI, entropy rate) detect action-conditioned structure that point prediction misses
- Whether excluding self-loops reveals conditional dynamics on non-self transitions
- Whether accessibility tree extraction can be repaired
- Whether JavaScript-heavy SPA sites show different dynamical structure
- Whether richer representations (visual layout, CSS, interaction sequences) reveal structure
- Whether the tested sites are representative of dynamical regimes

**Do Not Assume:**
- Synthetic positive control result applies to live Web (validates pipeline not Web dynamics)
- Nominal p=0.0 for SA vs shuffle is meaningful (SA < AF so effect is wrong direction)
- Accessibility tree was collected (0% populated)
- Trajectory split is deterministic (PYTHONHASHSEED-dependent)
- Self-loop contamination is a bug (may reflect genuine Web structure)
- Fixing validity gates alone would yield positive result (SA < AF is fundamental)

### Why this experiment is different

The parent experiment used **point-prediction accuracy**: train a rule model on (state, action) -> next_state, compare accuracy to action-frequency baseline. This failed because:

1. **Sparse state spaces**: 607 unique (state, action) keys for 616 training transitions means most keys appear once → memorization, not generalization
2. **Self-loop contamination**: 17-49% of transitions are self-loops (page links to itself) → trivial transitions inflate action-frequency baseline
3. **Accuracy metric insensitivity**: Accuracy measures point-prediction correctness, which requires generalization from training to test. In near-unique key regimes, this is impossible regardless of whether structure exists.

This experiment uses **pointwise mutual information (PMI)**: measure whether actions and next-states are statistically associated, conditioned on current state. PMI operates on **distributions** rather than **point predictions**:

- PMI does not require training/testing splits
- PMI naturally handles sparse state spaces (it measures association, not prediction)
- PMI can detect structure even when no classifier can generalize
- PMI is a well-defined information-theoretic quantity with known statistical properties

**Key insight**: A system can have genuine action-conditioned structure (actions constrain next-states in distribution) even if no classifier can predict the exact next-state from (state, action). PMI detects the former; accuracy detects the latter.

## 4. Hypotheses

### H1: Positive PMI on Live Data
Mean PMI between actions and next-states (conditioned on current state) is > 0 on live Web transitions, and significantly exceeds the shuffled-action null (permutation test p < 0.05 after Bonferroni correction).

### H2: Self-Loop Exclusion Improves Signal
PMI on non-self-loop transitions is >= PMI on all transitions (excluding self-loops does not reduce the action-conditioned signal).

### H3: Positive Control
PMI on synthetic lambda=1.0 data (actions fully determine next-state) is >= 1.0 bit. This verifies the PMI computation detects known structure.

### H4: Null Control
PMI on shuffled action labels is not significantly > 0 (permutation test p > 0.05). This verifies the PMI computation does not detect structure when absent.

## 5. Data Sources

### 5.1 Parent Experiment Raw Data

This experiment re-uses raw transition data from the parent experiment (EXP-PHYSICS-33965269281). No new data collection is required.

**Files:**
- `research/experiments/EXP-PHYSICS-33965269281/raw_live_wikipedia.json` (sha256: 87e6d8fcecb436ab9b1067a27c7f5708c393bace5efbb0225bfe1f57aa87bc5e) — 880 transitions, 110 trajectories
- `research/experiments/EXP-PHYSICS-33965269281/raw_live_python_docs.json` (sha256: a7634ca3734360a4d6a2ffdb89d859ae9ff466df710be3323da8ac5c5d2fa648) — 880 transitions, 110 trajectories
- `research/experiments/EXP-PHYSICS-33965269281/raw_positive.json` (sha256: 3eef0bbc382fef44eb63d55481e3d417b2a98478d6f4fa4e1eb06331a99fc73f) — 600 transitions, 60 trajectories, lambda=1.0
- `research/experiments/EXP-PHYSICS-33965269281/raw_null.json` (sha256: 3ae136b4cc36b5f736252af8b819613d1864625fc9647cfbdd649b13c72c713e) — 300 transitions, 30 trajectories, random

### 5.2 State Representation for PMI

The parent experiment uses a composite BrowserState with 6 fields (url, title, link_texts, tag_counts, form_signals, accessibility_roles). For PMI computation, we use **URL only** as the state identifier, consistent with:
- The parent's state discretization (BrowserState.to_key() produces a hash, but URL is the primary discriminator)
- The HTTP fetch baseline (EXP-PHYSICS-33788037373) which used URL-only state
- Avoiding combinatorial explosion of composite state keys (which contributed to the memorization problem)

This is a deliberate representation choice: we test whether URL-level state + action carries mutual information about next-URL, which is the most basic form of action-conditioned structure.

### 5.3 Self-Loop Identification

A transition is classified as a self-loop if `state_before.url == state_after.url` (after normalization: strip trailing slash, lowercase scheme/host). Self-loops represent pages that link to themselves, where clicking a self-referential link produces no URL change.

## 6. PMI Computation

### 6.1 Pointwise Mutual Information

For a transition (s, a, s'), the PMI is:

```
PMI(s, a, s') = log2[ P(s, a, s') / (P(s) * P(a|s) * P(s'|s)) ]
```

which simplifies to:

```
PMI(s, a, s') = log2[ P(a, s' | s) / P(a | s) * P(s' | s) ]
```

This measures how much more likely the joint occurrence (a, s') is under the joint distribution vs. the product of marginals, conditioned on s.

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
- **mean_pmi_live_all**: Mean PMI across all transitions at each live site
- **mean_pmi_live_nonself**: Mean PMI across non-self-loop transitions at each live site
- **mean_pmi_shuffled**: Mean PMI across shuffled-action permutations (null distribution)
- **permutation_p_value**: Fraction of shuffled PMI values >= observed PMI (one-sided)

### 7.2 Secondary Metrics
- **pmi_by_state_frequency**: Mean PMI stratified by state frequency (common vs rare states)
- **pmi_by_action_type**: Mean PMI stratified by action target (if distinguishable)
- **self_loop_fraction**: Fraction of transitions that are self-loops per site
- **unique_state_action_pairs**: Number of unique (state, action) pairs per dataset
- **unique_states**: Number of unique states per dataset
- **entropy_h_a**: Marginal entropy of actions H(A)
- **entropy_h_s_prime_given_s**: Conditional entropy H(S'|S)
- **mutual_information_I_a_s_prime_given_s**: I(A; S' | S) = H(A|S) - H(A|S,S') (information-theoretic mutual information, related to mean PMI)

### 7.3 Comparison Metrics
- **diff_pmi_vs_accuracy**: Qualitative comparison: does PMI detect structure when accuracy shows SA < AF?
- **parent_accuracy_SA_heldout**: From parent result.json (wiki 0.030, python 0.242)
- **parent_accuracy_AF_heldout**: From parent result.json (wiki 0.152, python 0.402)
- **parent_diff_SA_vs_AF**: From parent result.json (wiki -0.121, python -0.159)

## 8. Null Models

### 8.1 Shuffled-Action Null
Permute action labels within trajectories (1000 permutations). PMI on shuffled data should be ~0 when actions carry no information about next-states. This is the primary null for testing H1.

### 8.2 Frequency Null
Under no action-dependence, P(a, s'|s) = P(a|s) * P(s'|s), so PMI = 0. The frequency null is analytically equivalent to the shuffled-action null at the population level; finite-sample deviations are captured by the permutation test.

## 9. Statistical Tests

### 9.1 Primary Test: PMI > 0
- One-sided permutation test: H0: mean_PMI <= 0, H1: mean_PMI > 0
- Test statistic: mean_PMI on observed data
- Null distribution: mean_PMI on 1000 shuffled-action datasets
- p-value = (number of shuffled PMI >= observed PMI + 1) / (1000 + 1)
- **Bonferroni correction for 4 comparisons** (2 live sites x 2 conditions: all, non-self)
- Significance threshold: p < 0.05 / 4 = 0.0125

### 9.2 Secondary Test: PMI > Shuffled PMI
- Paired comparison: mean_PMI(observed) vs mean_PMI(shuffled) across trajectories
- One-sided: observed > shuffled
- Wilcoxon signed-rank test on per-trajectory PMI differences

### 9.3 Effect Size
- Cohen's d for mean_PMI(observed) vs mean_PMI(shuffled)
- Report confidence intervals for mean PMI at each site

### 9.4 Self-Loop Comparison
- Paired comparison: mean_PMI(non-self) vs mean_PMI(all) at each site
- One-sided: non-self >= all (excluding self-loops does not reduce signal)

## 10. Controls

### 10.1 Positive Control (Synthetic lambda=1.0)
- PMI >= 1.0 bit on synthetic data with deterministic action->next-state mapping
- This verifies: PMI computation is correct, known structure is detectable
- Expected: With 10 states and 4 permutation actions, H(S'|S,A) = 0 (deterministic), H(A|S) = log2(4) = 2.0 bits (uniform actions), so I(A;S'|S) = H(S'|S) - H(S'|S,A). Under uniform S: H(S'|S) = H(S') = log2(10) = 3.32 bits. With action-dependence, H(S'|S,A) = 0, so I = 3.32 - 0 = 3.32 bits. Mean PMI ≈ I(A;S'|S) / N ≈ 3.32 bits average.

### 10.2 Null Control (Shuffled Actions)
- PMI not significantly > 0 on shuffled data (permutation p > 0.05)
- This verifies: PMI computation does not detect structure when absent

### 10.3 Self-Loop Control
- Self-loop fraction reported per site (expected: wiki ~17%, python ~49% from parent)
- PMI on self-loops only vs non-self-loops only: decomposition reveals whether structure is in self-loops or non-self transitions

## 11. Validity Threats

### 11.1 Sparse State Spaces
With 607 unique (state, action) keys for 616 transitions, most joint cells have count=1. Laplace smoothing on marginals mitigates log(0) but does not eliminate estimation noise. **Mitigation**: report PMI distribution across transitions, not just mean; use permutation test which is robust to sparse estimation.

### 11.2 Self-Loop Inflation
Self-loops (17-49% of transitions) have P(s'|s,a) = 1.0 for the self-transition, which could inflate PMI if actions are concentrated on self-links. **Mitigation**: test non-self-loop transitions separately (H2); report self-loop PMI decomposition.

### 11.3 URL-Only State Representation
Using URL as state identity ignores page content, structure, and session state. Two different visits to the same URL may have different internal states. **Mitigation**: this is a deliberate choice to test the most basic form of action-conditioned structure (URL transitions). If PMI detects structure at URL level, it is a lower bound on structure detectable with richer representations.

### 11.4 Parent Data Quality
Re-using parent data inherits its validity issues: non-deterministic trajectory split, empty accessibility tree, query-string stripping, Bonferroni 6x not applied. **Mitigation**: these issues affect the parent's accuracy metrics but do not affect PMI computation (which does not use train/test splits). The trajectory-split determinism issue is irrelevant for PMI. Accessibility tree absence limits representation to URL+title+link_texts+tag_counts+form_signals, which is sufficient for URL-level PMI.

### 11.5 Multiple Comparisons
4 primary comparisons (2 sites x 2 conditions) with Bonferroni correction. **Mitigation**: correction is conservative; report both corrected and uncorrected p-values. The primary test is the most conservative; secondary tests are exploratory.

### 11.6 Synthetic-to-Real Gap
Synthetic positive control validates the PMI computation on known structure. Real Web dynamics may be fundamentally different. **Mitigation**: this is a necessary validation step. If PMI cannot detect known structure in synthetic data, it cannot be trusted on real data.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Mean PMI on live Wikipedia all-transitions > 0, permutation p < 0.0125 (Bonferroni x4)
2. Mean PMI on live Python docs all-transitions > 0, permutation p < 0.0125
3. Mean PMI on live Wikipedia non-self-loop > 0, permutation p < 0.0125
4. Mean PMI on live Python docs non-self-loop > 0, permutation p < 0.0125
5. Synthetic positive control PMI >= 1.0 bit
6. Shuffled-action null control: PMI not significantly > 0 (permutation p > 0.05)
7. No pipeline errors

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. PMI not > 0 on any live site after Bonferroni correction
2. PMI does not significantly exceed shuffled-action PMI
3. PMI on non-self-loop < PMI on all transitions at either site
4. Positive control fails (PMI < 1.0 bit)
5. Null control fails (shuffled PMI significantly > 0)

### 12.3 MEASUREMENT_INVALID
If:
1. Pipeline errors prevent computation
2. Data loading failure (files missing or corrupted)
3. Fewer than 100 transitions per live site
4. SHA-256 hash mismatch on parent data files

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates that action-conditioned structure exists in live Web data, detectable by PMI but not by point-prediction accuracy
- Validates information-theoretic measures as a complementary detection paradigm
- Explains why accuracy metrics failed: accuracy requires generalization (impossible with sparse keys); PMI measures association (detectable even with sparse data)
- Justifies: (a) PMI-guided exploration policies, (b) investigating why accuracy fails while PMI succeeds, (c) designing mechanisms that leverage distributional structure without point-prediction

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- Suggests that either (a) PMI is not sensitive to Web-dynamical structure at URL-level representation, or (b) the tested sites genuinely lack action-conditioned dynamics at URL level
- Does NOT falsify C-WEB-DYNAMICS entirely — only this detection method at this representation
- Physics lane should investigate: (a) richer state representations, (b) different site types (SPAs, form-heavy), (c) trajectory-level entropy rates instead of transition-level PMI

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Data Loading**: Load parent raw data files; verify SHA-256 hashes; extract (state.url, action.target_href, state_after.url) triples
2. **Self-Loop Classification**: Identify self-loops (state_before.url == state_after.url after normalization)
3. **PMI Computation**: For each transition, compute PMI using smoothed marginals; aggregate to mean PMI per dataset
4. **Shuffled-Action Null**: For 1000 permutations, shuffle action labels within trajectories, recompute mean PMI
5. **Permutation Test**: Compute p-value = (count shuffled >= observed + 1) / 1001
6. **Bonferroni Correction**: Correct p-values for 4 primary comparisons
7. **Positive Control**: Verify PMI >= 1.0 on synthetic data
8. **Null Control**: Verify shuffled PMI not > 0
9. **Self-Loop Decomposition**: Compare PMI on all vs non-self-loop vs self-loop-only transitions
10. **Effect Size**: Compute Cohen's d, confidence intervals
11. **Comparison**: Qualitative comparison with parent accuracy metrics
12. **Reporting**: Report all outcomes with equal prominence

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
- The parent experiment found SA < AF on live data, suggesting accuracy metrics are uninformative due to sparse keys
- PMI measures distributional association, not point prediction, so it may detect structure that accuracy cannot
- Self-loops (17-49%) are trivial transitions that may inflate or deflate PMI depending on action distribution
- URL-level state representation is the most basic test; if PMI detects structure here, it is a lower bound
- Expected PMI on live data: modestly positive (>0) if any action-conditioned structure exists; near 0 if sites are truly unstructured
- Expected PMI on synthetic lambda=1.0: ~3.3 bits (theoretical maximum for 10 states, 4 actions)

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
