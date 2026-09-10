# EXP-PHYSICS-34266105229 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34266105229
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-08
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-PHYSICS-34149195420 (SURVIVES_CURRENT_TEST)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Does title-aware PMI detect dynamical structure on real SPA/form-heavy browser transitions (React/Vue apps, form-heavy pages) where non-leakage transitions are frequent by construction and titles may be noisy or ambiguous, using browser-collected action->next-state data with sufficient transition density?

## 3. Motivation

### What the parent experiment established (EXP-PHYSICS-34149195420)

The parent experiment validated the PMI pipeline on synthetic SPA data with deterministic transitions and non-leakage by construction. It produced:

**Established:**
- PMI pipeline detects known deterministic action->next-state structure in SPA-like data when richer state representation (URL+title) resolves URL-level ambiguity (title PMI 1.970 bits, p=0.001, d=80.3)
- Title-aware PMI is significantly > URL-only PMI on synthetic SPA data: 1.970 vs 0.693 bits (+184%), confirming titles resolve within-URL structural ambiguity
- Cross-trajectory permutation null is valid and powerful: 0/1000 shuffled means exceed observed PMI, destroying 93.8% of signal
- Sampling 500 transitions over 32 SA pairs (~15.6 each) avoids the unique-SA forced-zero regime that falsified the parent experiment on server-rendered sites
- URL-only PMI is significantly > 0 (0.693 bits) even when structural ambiguity exists — URL-level states are not exchangeable due to heterogeneous marginal distributions
- Form signals add zero marginal information beyond titles when titles uniquely identify states — this is a design artifact, not evidence about form signals

**Rejected:**
- Pre-registered H1 that URL-only PMI would be "near zero (mean PMI < 0.1 bits)" due to structural ambiguity: URL-only PMI is 0.693 bits, significantly > 0
- That title information reveals structure "invisible at URL level": URL-only PMI is already significantly positive; titles provide additional (+184%), not exclusive, information
- That form_signals provide marginal information beyond titles: untested in this design because form_signals are redundant with unique titles in the synthetic data

**Unknown:**
- Whether title-aware PMI detects dynamical structure on real SPA/form-heavy browser transitions where titles may be noisy or ambiguous
- Whether form_signals provide marginal information beyond titles on real web pages where titles may be less discriminative than in synthetic data
- Whether URL-only PMI > 0 generalizes to real SPA sites where URL-level states may be more or less homogeneous than the synthetic 209/178/113 distribution
- Sensitivity of PMI absolute bit values to Laplace alpha (0, 0.5, 2.0)
- Whether trajectory-level entropy rates detect structure that transition-level PMI misses in sparse or stochastic regimes
- Statistical power with real noisy titles and stochastic transitions vs deterministic synthetic perfect-discriminator titles

**Do Not Assume:**
- That titles will be perfect state discriminators on real web pages — synthetic design guaranteed 8 unique titles for 8 states; real pages may have duplicate or missing titles
- That the +184% PMI improvement from URL-only to URL+title on synthetic data predicts the same magnitude on real data
- That deterministic synthetic structure is representative of real SPA dynamics
- That this experiment closes C-WEB-DYNAMICS or justifies product promotion — it is a narrow synthetic-to-real bridge requiring further validation

### Why this experiment is different

The parent experiment used **synthetic deterministic SPA data** with known structure. This experiment collects **real browser transitions** on JavaScript-heavy SPA/form-heavy sites. The critical differences:

1. **Real browser state**: DOM, title, URL are actual browser state, not synthetic constructs
2. **Stochastic transitions**: Real SPA transitions may be non-deterministic (async loading, user-dependent paths, A/B tests)
3. **Noisy titles**: Real page titles may be ambiguous, duplicate, or missing
4. **Non-leakage by construction**: SPA form submissions and client-side routing produce non-leakage transitions where the action does not predict the next state URL/title by simple string matching
5. **Cross-site generalization**: Testing 2+ sites assesses whether the finding is site-specific or general

## 4. Hypotheses

### H1: Title-Aware PMI > URL-Only PMI
URL+title PMI is significantly greater than URL-only PMI on real SPA non-leakage transitions, with Bonferroni-corrected permutation p < 0.025 for each site.

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
3. Verify Playwright works: simple page load test

### 5.2 Site Selection

Select 2 JavaScript-heavy SPA/form-heavy sites meeting these criteria:
- Client-side routing (React Router, Vue Router, or equivalent)
- Form interactions (multi-step forms, checkout flows, registration)
- Non-leakage transitions: form submissions that trigger client-side state changes without URL action keywords
- Accessible without authentication (or use demo accounts)
- Known to be stable and not blocking automated access

Candidate sites (to be finalized at execution):
1. **Site A**: A React/Vue multi-step form application (e.g., demo e-commerce checkout, survey builder)
2. **Site B**: A form-heavy SPA dashboard (e.g., project management tool, analytics dashboard)

### 5.3 Interaction Protocol

For each site:
1. Navigate to the site's entry point
2. Execute random-walk trajectories: 100 trajectories of 8 steps each = 800 total transitions per site
3. At each step:
   a. Extract BrowserState (URL, title, form_signals)
   b. Extract available actions (clickable same-domain links)
   c. Randomly select an action (uniform, seed=42 for reproducibility)
   d. Execute the action (Playwright click)
   e. Wait for page load (>= 1 second polite delay)
   f. Extract next BrowserState
   g. Record transition (state, action, next_state)
4. Filter out leakage transitions (action.target_href == state.url)
5. Ensure sufficient non-leakage density (>= 50 transitions per site, target 100+)

### 5.4 State Representation

For each transition (S_t, A_t, S_{t+1}):
- **URL**: window.location.href
- **Title**: document.title (truncated to 100 chars)
- **Form signals**: (has_form, has_input, has_select, has_textarea) — 4 booleans from DOM inspection

### 5.5 Non-Leakage Classification

A transition is classified as leakage ONLY if:
- action.target_href == state_after.url (the action's target URL is the current state's URL)

All other transitions are non-leakage. This matches the parent experiment's definition.

### 5.6 Sample Size

- 2 sites x 100 trajectories x 8 steps = 1600 total transitions
- Expected non-leakage: ~60-80% on SPA sites (960-1280 transitions)
- Minimum valid: 50 non-leakage transitions per site
- Target: 100+ non-leakage transitions per site

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

### 7.3 Comparison Metrics
- **parent_synthetic_url_only**: 0.693 bits (parent EXP-PHYSICS-34149195420)
- **parent_synthetic_url_title**: 1.970 bits (parent EXP-PHYSICS-34149195420)
- **parent_synthetic_improvement**: +184% (parent EXP-PHYSICS-34149195420)

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
URL+title PMI must be > URL-only PMI on both sites (Bonferroni-corrected). This is the core test of whether titles resolve structural ambiguity on real data.

### 10.4 Minimum Data Threshold
At least 50 non-leakage transitions per site. Fewer than 50 means PMI estimates are unreliable and the result is MEASUREMENT_INVALID.

## 11. Validity Threats

### 11.1 Title Ambiguity on Real Pages
Real web pages may have duplicate, missing, or generic titles (e.g., "Dashboard", "Settings"). This reduces the discriminative power of titles.
**Mitigation**: Report per-site title uniqueness. If titles are largely unique, the test is well-powered. If titles are ambiguous, the result is informative (titles don't help on real data).

### 11.2 Non-Leakage Classification Errors
Conservative non-leakage criteria may exclude genuine transitions or include spurious ones.
**Mitigation**: Manual inspection of 10% of classified transitions. Report false positive/negative rates.

### 11.3 Sample Size
With 100 trajectories x 8 steps = 800 transitions per site and 60-80% non-leakage, expect 480-640 non-leakage transitions per site. This exceeds the 50-transition minimum.
**Mitigation**: If initial collection yields <50 transitions, extend to 200 trajectories per site.

### 11.4 Site Selection Bias
Two sites may not represent the diversity of SPA architectures.
**Mitigation**: Select sites with different frameworks (React vs Vue), different interaction types (forms vs navigation), and different content domains.

### 11.5 Laplace Smoothing Sensitivity
PMI values are sensitive to alpha. Results are specific to alpha=1.0.
**Mitigation**: Report results at alpha=1.0 matching parent. Sensitivity analysis at alpha=0.5 and alpha=2.0 as secondary exploration.

### 11.6 Browser State Capture Timing
DOM state may change between action execution and state capture (async loading, animations).
**Mitigation**: Wait 2 seconds after each action before capturing state. Report any capture failures.

### 11.7 Playwright Installation Failure
Playwright or browser binaries may fail to install.
**Mitigation**: If installation fails, experiment is MEASUREMENT_INVALID. Document exact error and retry.

### 11.8 Site Access Failure
Real SPA sites may block automated access (403, CAPTCHA, rate limiting).
**Mitigation**: Use polite delays (>= 1 second), rotate user agents if needed, select sites known to be accessible. If all sites fail, experiment is MEASUREMENT_INVALID.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. URL+title PMI > URL-only PMI on both sites (Bonferroni-corrected permutation p < 0.025)
2. URL+title PMI > 0.5 bits on at least one site
3. Cross-trajectory permutation p < 0.001 on at least one site
4. Positive control passes (synthetic SPA PMI >= 0.5 bits)
5. At least 50 non-leakage transitions obtained from each site

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. URL+title PMI not > URL-only PMI on both sites after Bonferroni correction
2. Both sites show URL+title PMI < 0.1 bits
3. Permutation null fails (p > 0.05 on all sites/representations)
4. Positive control fails (synthetic SPA PMI < 0.5 bits)

### 12.3 MEASUREMENT_INVALID
If:
1. Fewer than 50 non-leakage transitions from either site
2. Pipeline errors prevent computation
3. Playwright fails to access sites or browser state extraction fails
4. Non-leakage classification reveals systematic leakage in collected data (manual inspection finds >10% misclassification)

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- Real SPA sites exhibit title-dependent dynamical structure detectable by PMI
- Validates the synthetic-to-real bridge for the PMI pipeline
- Justifies title-aware BrowserState representation in Product
- Opens trajectory-level analysis for stochastic transitions
- Physics lane should investigate form_signals marginal information on real data

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- Real SPA sites do not show title-dependent PMI above URL-only baseline
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
2. **Data Collection**: Browser automation on 2 SPA/form-heavy sites, 100 trajectories x 8 steps each, recording (URL, title, form_signals, action) before/after each interaction
3. **Non-Leakage Classification**: Apply parent definition (action.target_href == state.url) to identify non-leakage transitions
4. **PMI Computation**: Compute PMI for URL-only, URL+title, URL+title+form representations per site
5. **Permutation Testing**: Cross-trajectory permutation (1000 iterations) per representation per site
6. **Positive Control**: Run synthetic SPA pipeline alongside real data
7. **Comparison**: Compare real-data PMI with parent synthetic results
8. **Form Signals**: Test whether URL+title+form > URL+title on sites with ambiguous titles
9. **Trajectory Entropy**: Compute trajectory-level entropy rates as complementary measure (exploratory)
10. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- PMI computation from `research/physics/information_theoretic/spa_pmi.py` (reused from parent)
- Browser automation via Playwright for state collection
- `numpy` for statistical tests
- `scipy.stats` for permutation tests
- Standard library only for PMI computation

Code will be committed to `research/physics/information_theoretic/real_spa_pmi.py` before execution.

## 16. Pre-registered Expectations

From parent experiment and theoretical reasoning:
- URL+title PMI should be > URL-only PMI on real SPA data (titles resolve structural ambiguity)
- The magnitude of improvement may differ from synthetic +184% (real titles are noisier)
- URL-only PMI should be > 0 on real SPA data (URL-level states are not exchangeable)
- Form signals may provide marginal information on real data where titles are ambiguous
- Non-leakage transitions should be frequent on SPA/form-heavy sites (parent expected ~60-80%)
- Trajectory-level entropy rates may detect structure that transition-level PMI misses

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any data collection code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
