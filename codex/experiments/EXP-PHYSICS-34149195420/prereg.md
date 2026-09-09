# EXP-PHYSICS-34149195420 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34149195420
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-07
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does PMI between actions and next-states detect genuine dynamical structure in non-leakage SPA transitions when the state representation is enriched beyond URL to include title and form signals?

## 3. Motivation

Prior Physics work established:
- WP-002B: rule ~ nearest-neighbor > shuffle on all transitions; rule-shuffle difference +0.0532
- EXP-PHYSICS-34038570933: PMI > 0 on all transitions (URL-level, target_href actions)
- EXP-PHYSICS-34071626363: PMI drops to 0 or near-0 when leakage transitions excluded (Wikipedia 0.0, Python 0.874)

The critical finding from EXP-PHYSICS-34071626363 is that PMI on non-leakage subsets is driven to zero by **sparse unique SA pairs**: on server-rendered sites, non-leakage transitions are rare (7.6% wiki, 2.4% python), producing nearly unique (state, action) combinations where PMI is mathematically forced to zero under Laplace smoothing.

The parent handoff proposed two escape routes:
1. **Denser non-leakage sampling** on SPA/form-heavy sites where non-leakage is frequent by construction
2. **Richer state representations** (title, form_signals, tag_counts) that may capture structure invisible at URL level

This experiment tests both simultaneously using synthetic SPA-like data where:
- action.target_href != state_after.url by construction (non-leakage is 100%)
- A known action→next-state dependency exists
- URL-only representation has structural ambiguity (same URL, different actions, different outcomes)
- Richer representation (URL + title) resolves the ambiguity

This is a controlled validation: if the pipeline cannot detect known structure in synthetic SPA data, it cannot be trusted on real SPA data.

## 4. Hypotheses

### H1: URL-only PMI is indistinguishable from zero
PMI computed with URL-only state representation on the primary SPA dataset will be near zero (mean PMI < 0.1 bits) because repeated URLs with different action-outcome mappings create structural ambiguity that PMI cannot resolve.

### H2: Richer representation PMI is significantly positive
PMI computed with URL + title state representation will be significantly > 0 under cross-trajectory permutation (p < 0.025 after Bonferroni correction), demonstrating that title information resolves the URL-level ambiguity and reveals the action→next-state dependency.

### H3: Form signals add marginal information
PMI with URL + title + form_signals will be >= PMI with URL + title, though the increment may be small since titles already capture most of the structural information in the synthetic data.

### H4: Positive control passes
PMI on the deterministic positive control dataset (separate from primary) will be >= 0.5 bits with permutation p < 0.001, verifying the pipeline detects known structure.

### H5: Null control passes
Cross-trajectory shuffled-action PMI on the primary dataset will not be significantly > observed PMI (permutation p > 0.05), verifying the null model does not reject when actions are permuted.

## 5. Data Generation

### 5.1 Synthetic SPA Model

Generate a synthetic SPA environment with:
- **8 states**: Each has a URL and a title (URLs repeat across states with different titles)
- **4 actions**: form_submit, button_click, link_nav, menu_select
- **Deterministic transitions**: Each (state, action) pair maps to a unique (next_state, next_title)
- **Non-leakage by construction**: action.target_href is set to a dummy value that never equals state_after.url

### 5.2 State Structure

Each state has:
- `url`: One of 3 unique URLs (URLs repeat with different titles)
- `title`: Unique per state (8 unique titles for 8 states)
- `form_signals`: [has_form, has_input, has_submit, has_textarea] — varies by state

The 3 unique URLs are:
- `http://spa.test/form` (states 0, 1, 2 — form page with different contexts)
- `http://spa.test/dashboard` (states 3, 4, 5 — dashboard with different views)
- `http://spa.test/settings` (states 6, 7 — settings with different tabs)

### 5.3 Transition Structure

Each state has 4 actions, each leading to a specific next state:
- State 0 (form, "Checkout Form"): form_submit → State 3, button_click → State 4, link_nav → State 6, menu_select → State 7
- State 1 (form, "Login Form"): form_submit → State 5, button_click → State 3, link_nav → State 4, menu_select → State 6
- ... (similar for all 8 states)

This ensures:
- Same URL (`http://spa.test/form`) appears in states 0, 1, 2 with different titles and different action→next-state mappings
- URL-only representation: same (URL, action) can lead to different next-states → PMI ≈ 0
- Title-aware representation: each (URL, title, action) maps to exactly one next-state → PMI > 0

### 5.4 Sample Size

- 500 total transitions
- 25 trajectories of 20 transitions each
- Each trajectory starts from a random state and follows random actions
- Each state appears ~62.5 times (500/8), each (state, action) pair ~15.6 times (500/32)
- 80/20 train/test split is NOT used (PMI is computed on all triples; permutation test provides inference)

### 5.5 Positive Control Dataset

Separate synthetic dataset:
- 8 states, 4 actions, deterministic action→next-state mapping
- All states have unique URLs (no ambiguity)
- Same format as primary dataset but designed to have maximum PMI
- 200 transitions, 10 trajectories of 20

### 5.6 Random Seed

All data generation uses `random.Random(42)` with `PYTHONHASHSEED=0`.

## 6. State Representations

### 6.1 URL-only (Baseline)
State = URL string. This is the representation used in prior PMI experiments.

### 6.2 URL + title (Primary)
State = (URL, title) tuple. This tests whether title information resolves URL-level ambiguity.

### 6.3 URL + title + form_signals (Extended)
State = (URL, title, tuple(form_signals)) tuple. This tests whether form signals add information beyond title.

## 7. PMI Computation

### 7.1 Formula
PMI(s, a, s') = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]

Using Laplace smoothing (alpha = 1.0) for marginal probability estimates, identical to prior experiments.

### 7.2 Mean PMI
Average PMI across all transitions in the dataset.

## 8. Null Model

### 8.1 Cross-Trajectory Permutation
Shuffle action labels across entire trajectories (not within trajectories). This breaks the action→outcome dependency while preserving:
- Trajectory structure (sequence lengths)
- Marginal action frequencies
- State visitation patterns

This is the primary null model, addressing the parent experiment's finding that within-trajectory permutation is degenerate when trajectory groups are mostly singletons.

### 8.2 Permutation Procedure
1. Collect all trajectories
2. For each permutation: randomly reassign trajectory IDs to action sequences (cross-trajectory shuffle)
3. Compute mean PMI on shuffled data
4. Repeat 1000 times
5. p-value = (count of shuffled means >= observed mean + 1) / (1000 + 1)

## 9. Statistical Tests

### 9.1 Primary Test
For each representation (URL+title, URL+title+form_signals):
- Cross-trajectory permutation test (1000 permutations)
- One-sided: observed PMI > shuffled PMI
- Bonferroni correction for 2 comparisons: p_corrected < 0.05 → p_raw < 0.025

### 9.2 Comparison Test
- Paired comparison: richer representation PMI vs URL-only PMI
- Expected: richer > URL-only (one-sided, exploratory)

### 9.3 Effect Size
- Cohen's d for observed vs shuffled PMI at each representation level

## 10. Controls

### 10.1 Positive Control
- Deterministic synthetic SPA with unique URLs (no ambiguity)
- PMI with any representation must be >= 0.5 bits
- Permutation p < 0.001
- Verifies: PMI pipeline works, data format is correct, known structure is detectable

### 10.2 Null Control
- Cross-trajectory shuffled PMI on primary dataset
- Must not be significantly > observed PMI (p > 0.05)
- Verifies: null model does not reject when actions are permuted

### 10.3 Representation Comparison Control
- URL-only PMI must be < richer representation PMI
- Verifies: the representation change actually affects PMI (not just a constant shift)

## 11. Validity Threats

### 11.1 Synthetic-to-Real Gap
Synthetic SPA data may not reflect real SPA dynamics. Mitigation: this is a controlled validation. If the pipeline cannot detect known structure in synthetic data, it cannot be trusted on real data.

### 11.2 Laplace Smoothing Artifacts
Alpha = 1.0 smoothing affects PMI estimates in sparse regimes. With ~15 transitions per (state, action) pair, smoothing has moderate effect. Mitigation: same alpha as prior experiments; results are comparable.

### 11.3 Permutation Test Power
With 500 transitions and 1000 permutations, the test has high power to detect moderate effects (d > 0.3). Small effects may be missed. Mitigation: report effect sizes alongside p-values.

### 11.4 Deterministic Transition Choice
Single deterministic mapping could be pathological. Mitigation: the mapping is designed to create structural ambiguity at URL level while being detectable at title level. The positive control uses a separate, unambiguous mapping.

### 11.5 Multiple Comparisons
2 primary comparisons (URL+title, URL+title+form_signals) with Bonferroni correction. Conservative but appropriate for confirmatory tests.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Positive control PMI >= 0.5 bits (p < 0.001)
2. Null control p > 0.05
3. At least one of (URL+title, URL+title+form_signals) has mean PMI > 0 with permutation p < 0.025 (Bonferroni corrected)
4. Richer representation PMI > URL-only PMI
5. No pipeline errors

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. Positive control PMI < 0.5 bits OR p >= 0.001
2. Null control p < 0.05
3. No representation achieves Bonferroni-corrected significance
4. Richer representation PMI <= URL-only PMI

### 12.3 MEASUREMENT_INVALID
If:
1. Fewer than 100 transitions generated
2. Pipeline errors prevent computation
3. Fewer than 500 permutations completed

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- URL-only PMI ≈ 0 (structural ambiguity from repeated URLs)
- Title-aware PMI > 0 and significant (ambiguity resolved by title)
- Form signals add marginal information
- **Interpretation**: Richer BrowserState representations capture dynamical structure invisible at URL level in non-leakage SPA regimes
- **Next step**: Collect real SPA/form-heavy browser transitions and apply title-aware PMI

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
Two sub-cases:
- (a) No representation achieves significant PMI → SPA-like structure is not detectable by PMI even with richer representations
- (b) URL-only PMI is already significant → structural ambiguity is not the limiting factor; the parent failure was due to sparsity, not representation
- **Interpretation**: PMI is not the right tool for non-leakage SPA dynamics, or the synthetic structure is insufficient
- **Next step**: Try trajectory-level entropy rates or alternative information-theoretic measures

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Data Generation**: Generate 500 transitions from synthetic SPA model (seed=42)
2. **Positive Control**: Generate 200 transitions from deterministic SPA (separate dataset)
3. **URL-only PMI**: Compute PMI with state = URL on primary dataset
4. **Title-aware PMI**: Compute PMI with state = (URL, title) on primary dataset
5. **Form-signals PMI**: Compute PMI with state = (URL, title, form_signals) on primary dataset
6. **Positive Control PMI**: Compute PMI on positive control dataset
7. **Cross-Trajectory Permutation**: 1000 permutations for each representation on primary dataset
8. **Null Control**: Verify shuffled PMI is not significantly > observed
9. **Bonferroni Correction**: Correct for 2 primary comparisons
10. **Decision**: Apply frozen decision rule
11. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations
- `random` for deterministic data generation and permutation
- `collections.Counter` for counting
- `math` for log2
- Standard library only (no custom estimators required)

Code will be committed to `research/physics/information_theoretic/spa_pmi.py` before execution.

## 16. Pre-registered Expectations

From prior work:
- URL-only PMI on non-leakage subsets is 0.0 (Wikipedia) or 0.874 (Python docs, not significant)
- The parent failure was driven by sparse unique SA pairs
- SPA/form-heavy sites should have denser non-leakage subsets
- Richer representations should resolve URL-level ambiguity

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
