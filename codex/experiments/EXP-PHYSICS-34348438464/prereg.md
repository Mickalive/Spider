# EXP-PHYSICS-34348438464 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34348438464
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-09
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-PHYSICS-34266105229 (FALSIFIED-IN-SETTING)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does title-aware PMI detect dynamical structure on real SPA/form-heavy sites where titles actually vary across routes, using browser-collected action->next-state data with sufficient transition density and title variance?

## 3. Motivation

### What the parent experiment established (EXP-PHYSICS-34266105229)

The parent experiment tested title-aware PMI on real SPA/form-heavy browser transitions (TodoMVC React/Vue). It produced:

**Established:**
- URL-only PMI is strongly positive on TodoMVC hash-SPA transitions: React 1.360 bits, Vue 1.323 bits (permutation p=0.001, d=83-86, 400 transitions over 18 SA pairs). URL-level action->next-state dependency is genuine and strong on these sites
- PMI pipeline works correctly on real browser data: positive control (synthetic SPA PMI=0.693 bits, p=0.001) passes, cross-trajectory permutation null is valid and powerful on real SPA data
- TodoMVC hash-based SPA architecture produces 100% non-leakage transitions by construction (filter/toggle/add actions do not change URL path, so action.target_href never equals state_after.url)

**Rejected:**
- Title-aware PMI > URL-only PMI on TodoMVC SPAs: 0% improvement on both sites, but this is a mathematical consequence of zero title variance (unique_titles=1), not an empirical test of the hypothesis
- Form_signals provide marginal information beyond titles on TodoMVC: zero form_signals variance (all transitions have identical {has_form:false, has_input:true, has_select:false, has_textarea:false}), so H4 had zero power — untested, not rejected

**Unknown:**
- Whether title-aware PMI detects dynamical structure on real SPA/form-heavy sites where titles actually vary across routes (the preregistered population was never tested)
- Whether form_signals provide marginal information beyond titles on sites where titles are ambiguous but form structures differ (multi-step forms with similar titles but different has_form/has_input patterns)
- Whether trajectory-level entropy rates detect structure differences when transition-level PMI is identical due to degenerate representation
- Whether the high URL-only PMI (1.32-1.36 bits vs parent synthetic 0.693 bits) reflects genuinely richer dynamical structure or small-state-space artifact (3 URLs vs 8 synthetic states) combined with smoothing asymmetry
- Whether most production React/Vue SPAs have route-varying titles (via React Helmet, Vue Meta) or constant titles like TodoMVC — a title variance survey across SPA corpus would inform site selection
- Whether 100% non-leakage is specific to TodoMVC hash-navigation or generalizes to form-heavy SPAs with actual form submissions and href-based navigation

**Do Not Assume:**
- That the 0% title improvement on TodoMVC generalizes to sites with varying titles — it is a mathematical consequence of zero title variance (unique_titles=1), not a scientific finding about title informativeness
- That the high URL-only PMI (1.32-1.36 bits) reflects richer dynamical structure than the parent synthetic baseline (0.693 bits) — the comparison is confounded by different state spaces (3 URLs vs 8 states), different smoothing effects, and the PMI smoothing asymmetry (smoothed marginals, unsmoothed joint P(a,s'|s)=ct/cs) inherited from parent spa_pmi.py. Absolute bits are only comparable under same alpha and same state-space cardinality
- That TodoMVC properties (constant titles, 100% non-leakage, 3 URLs, 6 actions) are representative of production SPA sites — TodoMVC is a degenerate demo app
- That this experiment provides evidence for or against title-aware PMI on real sites with varying titles — the test environment had zero title entropy and was uninformative for the preregistered hypothesis
- That the half-spec sample size (400 vs 800 transitions) affected the conclusion — the zero title variance makes sample size moot for the title comparison, but note the deviation for future protocol compliance
- That 100% non-leakage fraction on TodoMVC would appear on form-heavy SPAs with actual form submissions — non-leakage rate depends on action representation (target_href) and site architecture
- That the permutation p=0.001 across all representations and sites indicates equal evidence — it is the resolution floor of 1000 permutations; effect sizes (d=83-86) differ and absolute PMI values differ
- That the PMI smoothing asymmetry (alpha=1.0 on marginals, unsmoothed joint) produces unbiased absolute bit values — reported bits are specific to alpha=1.0, sensitivity analysis at alpha=0,0.5,2.0 was not performed (prereg 11.5)

### Why this experiment is different

The parent experiment used **TodoMVC constant-title SPAs** where title variance was zero (unique_titles=1). This experiment selects **real SPA/form-heavy sites with verified title variance across routes**. The critical differences:

1. **Title variance**: Sites must have at least 3 routes with distinct document.title values (verified via pre-survey before full data collection)
2. **Form-heavy interactions**: Sites should have multi-step forms, checkout flows, survey builders, or dashboards where titles vary per step/page
3. **Non-leakage by construction**: SPA form submissions and client-side routing produce non-leakage transitions where the action does not predict the next state URL/title by simple string matching
4. **Cross-site generalization**: Testing 2-3 sites with different frameworks and content domains
5. **Form signals hypothesis**: Sites where titles may be ambiguous but form structures differ, enabling H4 test

## 4. Hypotheses

### H1: Title-Aware PMI > URL-Only PMI
URL+title PMI is significantly greater than URL-only PMI on real SPA non-leakage transitions where titles vary across routes, with Bonferroni-corrected permutation p < 0.025 for each site.

### H2: Meaningful Structure Detection
URL+title PMI exceeds 0.5 bits on at least one real SPA site, demonstrating non-trivial dynamical structure detectable by title-aware PMI.

### H3: Permutation Null Validation
Cross-trajectory permutation on real SPA data confirms that observed PMI reflects genuine action->next-state dependency (permutation p < 0.001 on at least one site).

### H4: Form Signals Marginal Information
On at least one real SPA site where titles are ambiguous (e.g., multi-step forms with similar page titles), form_signals provide marginal information beyond titles (URL+title+form PMI > URL+title PMI).

### H5: Positive Control
The synthetic SPA pipeline produces PMI >= 0.5 bits on known deterministic structure, verifying pipeline integrity.

## 5. Data Collection

### 5.1 Infrastructure Setup

Before data collection:
1. Install Playwright: `pip install playwright`
2. Download browser binaries: `playwright install chromium`
3. Verify Playwright works: simple page load test on a known URL

### 5.2 Site Selection

Select 2-3 JavaScript-heavy SPA/form-heavy sites meeting these criteria:
- **Title variance**: At least 3 routes with distinct document.title values (verified via pre-survey: navigate to 5+ routes and check document.title)
- Client-side routing (React Router, Vue Router, or equivalent)
- Form interactions (multi-step forms, checkout flows, registration)
- Non-leakage transitions: form submissions that trigger client-side state changes without URL action keywords
- Accessible without authentication (or use demo accounts)
- Known to be stable and not blocking automated access
- Different frameworks and content domains

Candidate sites (to be finalized after title variance verification):
1. **Site A**: A multi-step form wizard or survey builder with step-specific titles (e.g., "Step 1: Personal Info", "Step 2: Preferences", "Review & Submit")
2. **Site B**: A settings/configuration page with section-specific titles (e.g., "Account Settings", "Privacy Settings", "Notification Preferences")
3. **Site C (optional)**: A dashboard or admin panel with page-specific titles via React Helmet/Vue Meta

### 5.3 Title Variance Pre-Survey

Before full data collection, verify title variance:
1. Navigate to 5+ distinct routes on each candidate site
2. Record document.title on each route
3. Confirm at least 3 distinct titles exist
4. If titles are constant (unique_titles=1), reject site and select alternative
5. Record title variance metric: unique_titles / total_routes

### 5.4 Interaction Protocol

For each site:
1. Navigate to the site's entry point
2. Execute random-walk trajectories: 30 trajectories of 8 steps each = 240 total transitions per site
3. At each step:
   a. Extract BrowserState (URL, title, form_signals)
   b. Extract available actions (clickable same-domain links, buttons, form inputs)
   c. Randomly select an action (uniform, seed=42 for reproducibility)
   d. Execute the action (Playwright click/type/submit)
   e. Wait for page load (>= 1.5 second polite delay)
   f. Extract next BrowserState
   g. Record transition (state, action, next_state)
4. Filter out leakage transitions (action.target_href == state.url)
5. Ensure sufficient non-leakage density (>= 30 transitions per site, target 50+)

### 5.5 State Representation

For each transition (S_t, A_t, S_{t+1}):
- **URL**: window.location.href
- **Title**: document.title (truncated to 100 chars)
- **Form signals**: (has_form, has_input, has_select, has_textarea) — 4 booleans from DOM inspection

### 5.6 Non-Leakage Classification

A transition is classified as leakage ONLY if:
- action.target_href == state_after.url (the action's target URL is the current state's URL)

All other transitions are non-leakage. This matches the parent experiment's definition.

### 5.7 Sample Size

- 2-3 sites x 30 trajectories x 8 steps = 480-720 total transitions
- Expected non-leakage: ~60-80% on SPA sites (290-580 transitions)
- Minimum valid: 30 non-leakage transitions per site
- Target: 50+ non-leakage transitions per site

## 6. PMI Computation

### 6.1 PMI Formula

PMI(a, s'|s) = log2[P(a, s'|s) / (P(a|s) * P(s'|s))]

With Laplace smoothing (alpha=1.0) on joint and marginal counts, matching parent experiments.

### 6.2 Representations

Three representations tested per site:
1. **URL-only**: state = URL
2. **URL+title**: state = (URL, title)
3. **URL+title+form**: state = (URL, title, form_signals)

### 6.3 Cross-Trajectory Permutation Null

For each permutation:
1. Shuffle action labels across trajectories (preserving trajectory structure)
2. Recompute PMI on shuffled data
3. Repeat 1000 times

Observed PMI is significant if fewer than 5/1000 shuffled means exceed observed (one-sided p < 0.005, or p < 0.001 if 0/1000 exceed).

### 6.4 Trajectory-Level Entropy Rates (Complementary Measure)

Compute trajectory-level entropy rates as a complementary measure for stochastic transitions:
- H(S_{t+1} | S_t, A_t) = -sum P(s'|s,a) log2 P(s'|s,a)
- Compare with URL-only and URL+title representations
- This is exploratory and does not affect the primary decision rule

## 7. Measures

### 7.1 Primary Metrics
- **url_only_pmi**: PMI using URL-only state representation per site
- **url_title_pmi**: PMI using URL+title state representation per site
- **url_title_form_pmi**: PMI using URL+title+form state representation per site
- **spearman_richness**: Spearman correlation between representation richness (URL < URL+title < URL+title+form) and PMI per site

### 7.2 Secondary Metrics
- **permutation_p**: Cross-trajectory permutation p-value per representation per site
- **effect_size_d**: Cohen's d of observed vs shuffled PMI per representation per site
- **n_non_leakage**: Number of non-leakage transitions per site
- **n_unique_sa_pairs**: Number of unique (state, action) pairs per representation per site
- **form_signals_marginal**: URL+title+form PMI minus URL+title PMI per site (form signals marginal information)
- **title_variance**: unique_titles / total_routes measured in pre-survey per site

### 7.3 Comparison Metrics
- **parent_synthetic_url_only**: 0.693 bits (parent EXP-PHYSICS-34149195420)
- **parent_synthetic_url_title**: 1.970 bits (parent EXP-PHYSICS-34149195420)
- **parent_synthetic_improvement**: +184% (parent EXP-PHYSICS-34149195420)
- **parent_todomvc_url_only**: 1.360 bits (React), 1.323 bits (Vue) (parent EXP-PHYSICS-34266105229)
- **parent_todomvc_title_improvement**: 0% (both sites) (parent EXP-PHYSICS-34266105229)

### 7.4 Exploratory Metrics
- **trajectory_entropy_url_only**: Trajectory-level entropy rate using URL-only representation
- **trajectory_entropy_url_title**: Trajectory-level entropy rate using URL+title representation

## 8. Null Models

### 8.1 Cross-Trajectory Permutation
Shuffle action labels across trajectories. Preserves trajectory structure and marginal frequencies but destroys action->outcome dependency. 1000 permutations per site per representation.

### 8.2 Frequency Null
Predict next state from marginal distribution P(S_{t+1}). Expected PMI under this null is approximately 0 (no action-conditioned structure).

### 8.3 URL-Only Null
URL-only PMI serves as a within-experiment null: if URL+title PMI is not > URL-only PMI, title information provides no additional discrimination.

## 9. Statistical Tests

### 9.1 Primary Test: Representation Comparison
For each site: paired comparison of URL+title PMI vs URL-only PMI using cross-trajectory permutation.
- Bonferroni correction for 2 sites: alpha = 0.05/2 = 0.025
- Decision: URL+title PMI > URL-only PMI with permutation p < 0.025 at each site

### 9.2 Per-Site Significance
For each site and representation: cross-trajectory permutation test (one-sided, 1000 permutations).
- Decision: permutation p < 0.001 (0/1000 shuffled exceed observed)

### 9.3 Cross-Site Consistency
Qualitative comparison: do both sites show the same pattern (URL+title > URL-only)? Report effect direction and magnitude.

### 9.4 Effect Size
Cohen's d of observed vs shuffled PMI per representation per site. Report alongside p-values.

## 10. Controls

### 10.1 Positive Control (Synthetic SPA)
The synthetic SPA pipeline from parent EXP-PHYSICS-34149195420 must produce PMI >= 0.5 bits with p < 0.001. Run as a batch alongside real data to verify pipeline integrity.

### 10.2 Null Control (Permutation)
Cross-trajectory permutation on real SPA data: shuffled PMI must not exceed observed PMI in more than 5% of permutations (one-sided test, alpha=0.05). This verifies observed PMI reflects genuine action->next-state dependency.

### 10.3 Representation Comparison (URL-only vs URL+title)
URL+title PMI must be > URL-only PMI on both sites (Bonferroni-corrected). This is the core test of whether titles resolve structural ambiguity on real data with varying titles.

### 10.4 Minimum Data Threshold
At least 30 non-leakage transitions per site. Fewer than 30 means PMI estimates are unreliable and the result is MEASUREMENT_INVALID.

### 10.5 Title Variance Threshold
Each site must have at least 3 distinct titles across routes (verified via pre-survey). If titles are constant (unique_titles=1), the site is degenerate for title-aware PMI and must be rejected.

## 11. Validity Threats

### 11.1 Title Variance Verification
Even after pre-survey, title variance may be lower than expected during full data collection (e.g., some routes have identical titles).
**Mitigation**: Report actual unique_titles across all collected transitions. If unique_titles=1 for a site, treat as degenerate and note in validity_notes.

### 11.2 Non-Leakage Classification Errors
Conservative non-leakage criteria may exclude genuine transitions or include spurious ones.
**Mitigation**: Manual inspection of 10% of classified transitions if feasible. Report false positive/negative rates.

### 11.3 Sample Size
With 30 trajectories x 8 steps = 240 transitions per site and 60-80% non-leakage, expect 144-192 non-leakage transitions per site. This exceeds the 30-transition minimum.
**Mitigation**: If initial collection yields <30 transitions, extend to 50 trajectories per site.

### 11.4 Site Selection Bias
Two sites may not represent the diversity of SPA architectures.
**Mitigation**: Select sites with different frameworks (React vs Vue), different interaction types (forms vs navigation), and different content domains.

### 11.5 Laplace Smoothing Sensitivity
PMI values are sensitive to alpha. Results are specific to alpha=1.0.
**Mitigation**: Report results at alpha=1.0 matching parent. Sensitivity analysis at alpha=0.5 and alpha=2.0 as secondary exploration if time permits.

### 11.6 Browser State Capture Timing
DOM state may change between action execution and state capture (async loading, animations).
**Mitigation**: Wait 2 seconds after each action before capturing state. Report any capture failures.

### 11.7 Playwright Installation Failure
Playwright or browser binaries may fail to install.
**Mitigation**: If installation fails, experiment is MEASUREMENT_INVALID. Document exact error and retry.

### 11.8 Site Access Failure
Real SPA sites may block automated access (403, CAPTCHA, rate limiting).
**Mitigation**: Use polite delays (>= 1.5 seconds), rotate user agents if needed, select sites known to be accessible. If all sites fail, experiment is MEASUREMENT_INVALID.

### 11.9 Parent Comparison Confounds
Absolute PMI bits are not directly comparable across different state-space cardinalities (TodoMVC 3 URLs vs real sites with many URLs). The comparison is confounded by smoothing asymmetry.
**Mitigation**: Focus on within-site URL vs URL+title comparison, not absolute bit values across experiments.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. URL+title PMI > URL-only PMI on both sites (Bonferroni-corrected permutation p < 0.025)
2. URL+title PMI > 0.5 bits on at least one site
3. Cross-trajectory permutation p < 0.001 on at least one site
4. Positive control passes (synthetic SPA PMI >= 0.5 bits)
5. At least 30 non-leakage transitions obtained from each site

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. URL+title PMI not > URL-only PMI on both sites after Bonferroni correction
2. Both sites show URL+title PMI < 0.1 bits
3. Permutation null fails (p > 0.05 on all sites/representations)
4. Positive control fails (synthetic SPA PMI < 0.5 bits)

### 12.3 MEASUREMENT_INVALID
If:
1. Fewer than 30 non-leakage transitions from either site
2. Pipeline errors prevent computation
3. Playwright fails to access sites or browser state extraction fails
4. Both sites have unique_titles=1 (constant titles) — degenerate for title-aware PMI hypothesis

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- Real SPA sites with varying titles exhibit title-dependent dynamical structure detectable by PMI
- Validates the synthetic-to-real bridge for the PMI pipeline
- Justifies title-aware BrowserState representation in Product
- Opens trajectory-level analysis for stochastic transitions
- Physics lane should investigate form_signals marginal information on real data

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- Real SPA sites with varying titles do not show title-dependent PMI above URL-only baseline
- The synthetic finding (EXP-PHYSICS-34149195420) does not generalize to real browser data
- Physics lane should explore alternative state representations (DOM structure, accessibility tree, visual features) or alternative measures (trajectory-level entropy rates)
- Product lane should not invest in title-aware state representation based on current evidence
- Does NOT falsify C-WEB-DYNAMICS entirely — only this specific representation and detection method

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- Insufficient non-leakage transitions or pipeline errors
- Not scientific evidence for or against
- Requires collection protocol refinement before re-attempt

## 14. Analysis Plan

1. **Infrastructure Setup**: Install Playwright, download browser binaries, verify works
2. **Site Selection & Title Variance Pre-Survey**: Verify at least 3 distinct titles per site
3. **Data Collection**: Browser automation on 2-3 SPA/form-heavy sites, 30 trajectories x 8 steps each, recording (URL, title, form_signals, action) before/after each interaction
4. **Non-Leakage Classification**: Apply parent definition (action.target_href == state.url) to identify non-leakage transitions
5. **PMI Computation**: Compute PMI for URL-only, URL+title, URL+title+form representations per site
6. **Permutation Testing**: Cross-trajectory permutation (1000 iterations) per representation per site
7. **Positive Control**: Run synthetic SPA pipeline alongside real data
8. **Comparison**: Compare real-data PMI with parent synthetic results and TodoMVC results
9. **Form Signals**: Test whether URL+title+form > URL+title on sites with ambiguous titles
10. **Trajectory Entropy**: Compute trajectory-level entropy rates as complementary measure (exploratory)
11. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- PMI computation from `research/physics/information_theoretic/spa_pmi.py` (reused from parent)
- Browser automation via Playwright for state collection
- `numpy` for statistical tests
- `scipy.stats` for permutation tests
- Standard library only for PMI computation

Code will be committed to `research/physics/information_theoretic/real_spa_pmi.py` before execution (replacing parent TodoMVC version with real SPA version).

## 16. Pre-registered Expectations

From parent experiment and theoretical reasoning:
- URL+title PMI should be > URL-only PMI on real SPA data with varying titles (titles resolve structural ambiguity)
- The magnitude of improvement may differ from synthetic +184% (real titles are noisier)
- URL-only PMI should be > 0 on real SPA data (URL-level states are not exchangeable)
- Form signals may provide marginal information on real data where titles are ambiguous
- Non-leakage transitions should be frequent on SPA/form-heavy sites (parent expected ~60-80%)
- Trajectory-level entropy rates may detect structure that transition-level PMI misses

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any data collection code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
