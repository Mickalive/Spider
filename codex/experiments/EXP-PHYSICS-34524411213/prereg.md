# EXP-PHYSICS-34524411213 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34524411213
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-10
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can DOM structural features (element counts by type, tree depth, interactive element density) predict next-state transitions on real SPA/form-heavy sites, providing state representation beyond URL and title?

## 3. Motivation

Prior Physics work established:
- URL-only PMI is strongly positive on TodoMVC hash-SPA transitions: React 1.360 bits, Vue 1.323 bits (EXP-PHYSICS-34266105229)
- Title-aware PMI showed 0% improvement on TodoMVC (zero title variance) and was MEASUREMENT_INVALID on GitHub/MDN (MPA sites with insufficient transition density, EXP-PHYSICS-34348438464)
- The title-aware hypothesis remains untested on genuine SPA sites with varying titles

The parent handoff (EXP-PHYSICS-34348438464) recommended testing DOM structural features as a materially orthogonal level of description. While titles are semantic identifiers, DOM structural features (element counts, tree depth, interactive density) capture the *physical structure* of the page. A SPA with the same URL and title but different DOM state (e.g., a form at step 2 vs step 3) would be indistinguishable at URL/title level but distinguishable at DOM structure level.

This experiment tests whether DOM structural features carry predictive dynamical information that URL and title miss.

## 4. Hypotheses

### H1: DOM-feature PMI > URL-only PMI
On genuine SPA/form-heavy sites, PMI computed with DOM structural features as state representation exceeds URL-only PMI by >= 0.1 bits on >= 2/3 sites.

### H2: DOM-feature PMI significantly > 0
DOM-feature PMI is significantly > 0 under cross-trajectory permutation (p < 0.025 after Bonferroni correction) on >= 2/3 sites.

### H3: Positive Control
On synthetic SPA with deterministic DOM evolution, DOM-feature PMI >= 0.5 bits with permutation p < 0.001.

### H4: Null Control
On synthetic SPA with action-independent (shuffled) transitions, DOM-feature PMI does not significantly exceed 0 (permutation p > 0.05).

## 5. Data Collection

### 5.1 Site Selection

Select 2-3 genuine SPA/form-heavy sites with client-side routing. Pre-survey criteria:
- URL changes without full page reload (history.pushState or hash routing)
- DOM updates on navigation (document.querySelector('[data-reactroot]') or Vue mount point detected)
- Multiple interactive forms or multi-step workflows
- No CAPTCHA/403 blocks under polite crawling (0.5s delay)

Candidate categories:
- Survey builders (Typeform, Google Forms if accessible)
- E-commerce checkouts (multi-step forms)
- Dashboard apps (React/Vue admin panels)
- TodoMVC variants with form interactions (already validated)

### 5.2 Synthetic SPA (Positive Control)

Generate synthetic SPA with 8 states, 4 actions, deterministic transitions, and DOM feature vectors that evolve predictably:
- Each state has a unique DOM feature vector (element_count, tree_depth, interactive_density)
- Actions modify specific features (e.g., "add_item" increments element_count, "navigate" changes tree_depth)
- DOM feature vectors are 3-dimensional: [element_count, tree_depth, interactive_density]
- Element count ranges 10-50, tree depth 2-8, interactive density 0.1-0.5

### 5.3 Data Collection Protocol

For each site:
1. Navigate to entry URL
2. At each step:
   a. Extract state representation: URL, title, DOM features
   b. Discover available actions (Playwright locator API: button:visible, a:visible, input:visible)
   c. Randomly select one action
   d. Execute action, wait for navigation/DOM update (networkidle)
   e. Extract next-state representation
   f. Record transition: (state, action, next_state, raw_features)
3. Collect 30 trajectories x 8 steps = 240 transitions per site (target)
4. Polite delay: 0.5s between actions, 2s between trajectories

### 5.4 DOM Feature Extraction

At each step, extract via Playwright page.evaluate():
```javascript
{
  element_count: document.querySelectorAll('*').length,
  tree_depth: computeMaxDepth(document.body),  // recursive childElementCount
  interactive_density: (
    document.querySelectorAll('button, a, input, select, textarea, [role="button"]').length
    / Math.max(document.querySelectorAll('*').length, 1)
  ),
  form_count: document.querySelectorAll('form').length,
  input_count: document.querySelectorAll('input, select, textarea').length,
  button_count: document.querySelectorAll('button, [role="button"]').length
}
```

Store raw feature vectors for each transition.

## 6. State Representations

### 6.1 URL-only
State = URL path (query params stripped, hash stripped)

### 6.2 URL+title
State = (URL path, document.title)

### 6.3 DOM-feature
State = discretized DOM feature vector:
- Primary features: element_count, tree_depth, interactive_density
- Secondary features: form_count, input_count, button_count (for ablation)
- Discretization: each feature binned into 5 quantile bins (edges fit on TRAIN only)
- State = (element_count_bin, tree_depth_bin, interactive_density_bin)
- 5 x 5 x 5 = 125 possible discrete states

## 7. PMI Computation

### 7.1 Formula
PMI(a, s, s') = log2[ P(s'|s,a) / P(s'|s) ]

Where:
- P(s'|s,a) = count(s,a,s') / count(s,a) (Laplace-smoothed with alpha=1.0)
- P(s'|s) = count(s,s') / count(s) (Laplace-smoothed with alpha=1.0)
- PMI averaged over all observed (s,a,s') triples

### 7.2 Alpha Sensitivity
Compute PMI at alpha = 0, 0.5, 1.0, 2.0 to assess smoothing sensitivity.

## 8. Statistical Tests

### 8.1 Primary: Cross-Trajectory Permutation
- Shuffle action labels across trajectories (preserving trajectory structure)
- 1000 permutations
- p = (count_shuffled_gt_observed + 1) / (1000 + 1)
- One-sided test: observed PMI > shuffled distribution

### 8.2 Representation Comparison
- Paired comparison: DOM-feature PMI vs URL-only PMI per site
- Effect size: Cohen's d of permutation distributions
- Bonferroni correction for 3 representations x 2 tests = 6 comparisons (alpha = 0.025)

### 8.3 Secondary: Trajectory-Level Entropy Rate
- H(S'|S) = -sum P(s'|s) log2 P(s'|s)
- H(S'|S,A) = -sum P(s'|s,a) log2 P(s'|s,a)
- Entropy reduction = H(S'|S) - H(S'|S,A)
- Positive entropy reduction indicates action-conditioned structure

## 9. Null Models

### 9.1 Shuffle Null
Permute action labels across trajectories. Destroys action->outcome dependency while preserving state frequencies.

### 9.2 Frequency Null
Predict next state from marginal distribution P(S_{t+1}). Expected PMI = 0.

### 9.3 URL-only Null
If DOM-feature PMI > URL-only PMI, test whether the improvement is significant via paired permutation on representation differences.

## 10. Controls

### 10.1 Positive Control (Synthetic SPA)
- Synthetic SPA with deterministic DOM evolution
- DOM-feature PMI must be >= 0.5 bits with permutation p < 0.001
- Verifies: DOM feature extraction works, PMI computation correct, pipeline detects known structure

### 10.2 Null Control (Shuffled Synthetic)
- Same synthetic SPA with shuffled actions
- DOM-feature PMI must not significantly exceed 0 (permutation p > 0.05)
- Verifies: pipeline does not detect structure when absent

### 10.3 Baseline Comparison
- URL-only PMI provides lower bound
- URL+title PMI provides semantic baseline
- DOM-feature PMI should exceed both if structural features carry additional information

### 10.4 Data Sufficiency
- >= 30 non-leakage transitions per site (target 50+)
- If < 30, site is excluded and counted toward MEASUREMENT_INVALID threshold

## 11. Validity Threats

### 11.1 SPA vs MPA Site Selection
Prior experiment (EXP-PHYSICS-34348438464) failed because GitHub/MDN are MPAs. Mitigation: pre-survey verifies client-side routing via DOM update detection, not just title variance. Exclude sites where > 80% of transitions are link-navigation leakage.

### 11.2 DOM Feature Representativeness
6 features may not capture relevant structural variation. Mitigation: primary test uses 3 features (element_count, tree_depth, interactive_density); secondary features (form_count, input_count, button_count) available for ablation. Raw feature vectors preserved for downstream analysis.

### 11.3 Discretization Artifacts
5-bin quantile discretization may lose information or create artificial state boundaries. Mitigation: alpha sensitivity analysis; report results at multiple bin counts (3, 5, 10) as exploratory.

### 11.2 Synthetic-to-Real Gap
Synthetic SPA DOM evolution may not reflect real SPA dynamics. Mitigation: synthetic is positive control only; real-data test is the confirmatory claim.

### 11.3 Sample Size
With 30 trajectories x 8 steps = 240 transitions per site, and ~50-100 non-leakage expected, power is moderate for detecting large effects (d > 0.8). Smaller effects may require more data. Report confidence intervals.

### 11.4 Multiple Comparisons
3 sites x 2 tests (PMI > 0, DOM > URL) = 6 comparisons. Bonferroni correction alpha = 0.025. Conservative but appropriate for confirmatory test.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. DOM-feature PMI > URL-only PMI by >= 0.1 bits on >= 2/3 sites (Bonferroni-corrected permutation p < 0.025)
2. DOM-feature PMI significantly > 0 on >= 2/3 sites (permutation p < 0.025)
3. Positive control passes (DOM-feature PMI >= 0.5, p < 0.001)
4. Null control passes (p > 0.05)
5. Data sufficiency met on >= 2/3 sites (>= 30 non-leakage transitions)

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. DOM-feature PMI does not exceed URL-only PMI by >= 0.1 bits on 2+ sites
2. DOM-feature PMI is not significantly > 0 on 2+ sites
3. Positive control fails
4. Null control fails

### 12.3 MEASUREMENT_INVALID
If:
1. Data sufficiency (< 30 non-leakage) on 2+ sites
2. Pipeline errors prevent computation
3. SPA pre-survey fails on all candidate sites

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- DOM structural features capture dynamical structure beyond URL/title
- Product could use DOM-feature hashing for state identity on form-heavy sites
- Justifies further investigation of structural state representation (accessibility tree, visual features)
- Supports C-WEB-DYNAMICS: Web transformations have predictive structure at the structural level

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- DOM structural features do not improve PMI over URL-only on tested sites
- Product should focus on URL/title/semantic representations
- Does NOT falsify C-WEB-DYNAMICS entirely—only this specific structural representation
- Consider alternative representations: accessibility tree, visual features, session state

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- Insufficient SPA sites or transition density
- Pipeline needs debugging
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Pre-survey**: Verify SPA candidate sites via DOM update detection
2. **Positive control**: Generate synthetic SPA, extract DOM features, compute PMI
3. **Data collection**: Playwright browser transitions on 2-3 SPA sites
4. **Feature extraction**: DOM features via page.evaluate() at each step
5. **Discretization**: Quantile bins fit on TRAIN only
6. **PMI computation**: URL-only, URL+title, DOM-feature representations
7. **Permutation tests**: 1000 cross-trajectory permutations per representation per site
8. **Alpha sensitivity**: PMI at alpha = 0, 0.5, 1.0, 2.0
9. **Entropy rates**: H(S'|S), H(S'|S,A), entropy reduction
10. **Decision**: Apply frozen decision rule

## 15. Analysis Code

Analysis will be implemented in Python using:
- `playwright` for browser data collection and DOM feature extraction
- `numpy` for array operations and random generation
- `scipy.stats` for statistical tests
- `collections.Counter` for majority voting and PMI computation
- Standard library only for discretization and feature processing

Code will be committed to `research/physics/dom_features/` before execution.

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
