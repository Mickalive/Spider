# EXP-PHYSICS-35185288822 — Preregistration

**Experiment ID:** EXP-PHYSICS-35185288822  
**Lane:** physics  
**Claim:** C-WEB-DYNAMICS  
**Date:** 2026-09-17  
**Status:** DESIGN — NOT YET FROZEN

---

## 1. Research Question

Can the PMI pipeline detect title-aware conditional PMI I(S_next; Title_before | URL, H_K=3) > 0.05 bits on production server-rendered websites with genuine title variation and navigational density, beyond what URL-only representation provides — thereby bridging the dominant synthetic-to-real gap in the C-WEB-DYNAMICS research program?

## 2. Hypothesis

The 30+ C-WEB-DYNAMICS experiments have all been synthetic or locally-hosted. Production server-rendered websites have genuine title variation (different page titles for different content states), stochastic navigation (user-driven action sequences), and real-world content diversity. If title-aware PMI > 0 on production sites after controlling for URL and action-history, this demonstrates that richer state representations capture predictive dynamical structure on the real Web. If title-aware PMI = 0 (despite URL-only PMI > 0), title is not a useful state representation and the PMI signal is limited to URL-level structure.

## 3. State Representation

- **Primary:** `Title_before` = document.title of the page BEFORE the transition (string)
- **Control:** `URL` = URL of the page BEFORE the transition (string)
- **Combined:** `(URL, Title_before)` as joint state representation
- **History:** ActionHistory_K = last K actions (action_target, action_primitive) with START padding, K ∈ {1, 3}

## 4. Action Representation

- **Action target:** clicked element href or button identifier (string)
- **Action primitive:** click, type, scroll, back, refresh (categorical)
- Collected from browser automation (Playwright/Puppetwright headless Chrome)

## 5. Target

Next-state URL after action: S_next = URL of the page AFTER the transition

## 6. Sites

Three production server-rendered websites with genuine title variation:

1. **Wikipedia** (en.wikipedia.org): article pages with unique titles, internal links, back-button navigation. Known to have stochastic transitions (user-driven). Prior experiments: EXP-PHYSICS-34071626363 showed URL-only PMI = 0.0 with leakage removed (unique SA pairs). EXP-PHYSICS-34348438464 showed insufficient non-leakage transitions (N=9). This experiment uses browser automation (not HTTP fetch) to collect richer transition data.

2. **MDN Web Docs** (developer.mozilla.org): documentation pages with topic-specific titles, sidebar navigation, search functionality. Prior experiment: EXP-PHYSICS-34348438464 showed insufficient non-leakage transitions (N=17). Browser automation should yield higher transition density.

3. **GitHub** (github.com): repository pages with project-specific titles, file tree navigation, issue/PR pages. Prior experiment: EXP-PHYSICS-34348438464 showed insufficient non-leakage transitions (N=9). Browser automation should yield higher transition density.

**Exclusion criteria:** Sites with < 2 unique document.title values across collected transitions are excluded as degenerate (title variation insufficient).

## 7. Sampling Policy

- **Browsing sessions:** 5+ distinct sessions per site (different starting pages, different action sequences)
- **Actions per session:** 20-50 actions (clicks, navigation, back-button)
- **Total transitions:** >= 100 per site after filtering
- **Non-leakage requirement:** >= 50% of transitions must be non-leakage (action.target_href != state_after.url)
- **Session generation:** seeded random walk over linked pages (seed=42 for reproducibility)

## 8. Unit of Analysis

Each transition: (URL_before, Title_before, ActionHistory_K, Action, S_next)  
Grouped by (site, URL, ActionHistory_K, step) for within-strata permutation.

## 9. Holdout

- **Site-level:** Each site is analyzed independently; no cross-site pooling for primary test
- **Within-site:** Strata with < 5 transitions are excluded (insufficient for permutation test)
- **Temporal:** First 70% of transitions per session = train (for BC correction); last 30% = test (for PMI evaluation). NOTE: since PMI is computed on the full dataset with permutation null, this train/test split is for bias correction only, not for confirmatory inference.

## 10. Null Models / Baselines

1. **Frequency baseline:** P(S_next) = marginal next-state distribution. Expected accuracy varies.
2. **URL-only baseline:** BC PMI I(S_next; URL | URL, H_K=3). Expected > 0.05 bits on >= 2/3 sites.
3. **Title-shuffled null:** Title_before labels permuted within (URL, H_K=3, step) strata (1000 permutations per stratum). Expected BC PMI ≈ 0.
4. **Synthetic positive control:** 8-state linear SPA with unique deterministic titles. Expected BC PMI > 0.5 bits.

## 11. Primary Metric

**Title-aware BC PMI at K=3:** Bias-corrected pointwise mutual information I(S_next; Title_before | URL, H_K=3) computed on collected production site transitions.

Formula:  
BC_PMI = observed_PMI - perm_mean_PMI  
where perm_mean_PMI = mean PMI over 1000 within-strata label permutations.

**Significance:** Permutation test, 1000 permutations per (site, K) stratum. Bonferroni correction across 6 comparisons (3 sites × 2 K values: K=1, K=3). Corrected threshold: p < 0.0125 (α/4).

**Effect size:** Cohen's d = (observed_PMI - perm_mean_PMI) / perm_std_PMI. Report for each site.

## 12. Expected Direction

If title carries predictive information: title-aware BC PMI > 0 (positive direction).  
If title is redundant with URL: title-aware BC PMI ≈ 0 (null direction).  
If title is anti-predictive: title-aware BC PMI < 0 (negative direction, unusual).

## 13. Uncertainty Method

- Bootstrap 95% CI on BC PMI (1000 bootstrap resamples of trajectories, not transitions, to preserve within-trajectory dependence)
- Permutation p-value (1000 permutations)
- Bonferroni correction for multiple comparisons

## 14. Adequacy Rule

The experiment is adequately powered if:
- >= 50 non-leakage transitions per site (after filtering)
- >= 2 unique titles per site (title variation check)
- H(S_next | URL, H_K=3) > 0.2 bits on >= 2/3 sites (ceiling eliminated)
- Permutation test converges (p-value stabilizes within ±0.005 across last 200 permutations)

## 15. Falsification / Survival Rule

**SURVIVES_CURRENT_TEST** if ALL of:
1. URL-only BC PMI at K=3 > 0.05 bits with Bonferroni p < 0.0125 on >= 2/3 sites
2. Title-aware BC PMI at K=3 > 0.05 bits with Bonferroni p < 0.0125 on >= 2/3 sites
3. Title variation check passes (>= 2 unique titles per site)
4. Positive control BC PMI > 0.5 bits with Bonferroni p < 0.0125
5. Negative control BC PMI < 0.05 bits with p >= 0.0125
6. Determinism check passes on positive control (accuracy = 1.0)
7. >= 50 non-leakage transitions per site
8. H(S_next | URL, H_K=3) > 0.2 bits on >= 2/3 sites

**FALSIFIED-IN-SETTING** if:
- Title-aware BC PMI <= 0.05 bits OR Bonferroni p >= 0.0125 on >= 2/3 sites, while URL-only passes (condition 1 satisfied)

**INCONCLUSIVE** if:
- URL-only BC PMI <= 0.05 bits on all 3 sites (pipeline cannot detect basic structure)

**MEASUREMENT_INVALID** if:
- Controls fail (positive or negative)
- Title variation insufficient (< 2 unique titles per site)
- Data quality insufficient (< 50 non-leakage transitions per site)
- Determinism check fails on positive control

## 16. Controls Summary

| Control | Identifier | Expected | Pass Criterion |
|---------|-----------|----------|----------------|
| Synthetic positive control | `POS_CTRL_SYNTHETIC_8STATE` | BC PMI > 0.5 bits | BC_PMI > 0.5 AND perm_std > 0 AND p_bonf < 0.0125 |
| Title-shuffled negative control | `NEG_CTRL_TITLE_SHUFFLED` | BC PMI ≈ 0 | |BC_PMI| < 3 * perm_std AND perm_std > 0 |
| URL-only baseline | `BASELINE_URL_ONLY` | BC PMI > 0.05 bits | BC_PMI > 0.05 AND p_bonf < 0.0125 |
| Frequency baseline | `BASELINE_FREQUENCY` | Accuracy ~1/N_states | Report only, no pass/fail |

## 17. Metrics Registry (Stable Identifiers)

| Metric ID | Description | Unit |
|-----------|-------------|------|
| `BC_PMI_TITLE_K3` | Title-aware BC PMI at K=3 (primary) | bits |
| `BC_PMI_TITLE_K1` | Title-aware BC PMI at K=1 | bits |
| `BC_PMI_URL_K3` | URL-only BC PMI at K=3 | bits |
| `BC_PMI_URL_K1` | URL-only BC PMI at K=1 | bits |
| `PERM_P_TITLE_K3` | Permutation p-value for title-aware PMI at K=3 | — |
| `PERM_P_URL_K3` | Permutation p-value for URL-only PMI at K=3 | — |
| `COHEN_D_TITLE_K3` | Effect size for title-aware PMI at K=3 | — |
| `H_SNEXT_URL_HK3` | Conditional entropy H(S_next \| URL, H_K=3) | bits |
| `N_TRANSITIONS` | Total collected transitions per site | count |
| `N_NON_LEAKAGE` | Non-leakage transitions per site | count |
| `N_UNIQUE_TITLES` | Unique document.title values per site | count |
| `DETERMINISM_ACC` | Determinism accuracy on positive control | — |
| `POS_CTRL_BC_PMI` | Positive control BC PMI | bits |
| `NEG_CTRL_BC_PMI` | Negative control BC PMI | bits |

## 18. Data Collection Protocol

1. Launch headless Chrome via Playwright
2. For each site, navigate to a random starting page (seeded)
3. For each action:
   a. Record pre-transition state: URL, document.title, DOM hash, timestamp
   b. Identify clickable elements (links, buttons)
   c. Execute action (random choice from available elements, seeded)
   d. Record post-transition state: URL, document.title, DOM hash, timestamp
   e. Record action details: target href/identifier, primitive type
4. Repeat for 20-50 actions per session, 5+ sessions per site
5. Filter non-leakage transitions (action.target_href != state_after.url)
6. Export transition records to JSON

## 19. Analysis Pipeline

1. Load transitions, apply non-leakage filter
2. Construct action history (K=1, K=3)
3. Compute conditional entropy H(S_next | URL, H_K=3)
4. For each (site, K):
   a. Compute observed PMI for title-aware representation
   b. Run 1000 within-strata permutations
   c. Compute BC PMI = observed - perm_mean
   d. Compute permutation p-value
   e. Apply Bonferroni correction
5. Repeat for URL-only representation
6. Compute positive and negative controls
7. Generate report with metrics, controls, and observations

## 20. Validity Threats

1. **Title redundancy with URL:** On some SPAs, document.title may be isomorphic to URL (e.g., hash-SPAs where title reflects hash). If title adds zero marginal information beyond URL, the test is degenerate. Mitigation: include title variation check; report URL-only PMI separately.

2. **Server-rendered vs client-side:** Production server-rendered sites (Wikipedia, MDN, GitHub) may not exhibit the same state-transition dynamics as client-side SPAs. The C-WEB-DYNAMICS claim concerns "interactive Web transformations" broadly, but the tested sites are server-rendered. Claim ceiling bounded accordingly.

3. **Non-leakage filtering:** Aggressive filtering (excluding transitions where action.target_href == state_after.url) may reduce sample size below power threshold. Mitigation: report both pre- and post-filter sample sizes; if post-filter N < 50, experiment is MEASUREMENT_INVALID.

4. **Browser automation artifacts:** Playwright/Puppeteer may introduce timing or rendering artifacts not present in real user interaction. Mitigation: use realistic delays between actions; record timing for audit.

5. **Session diversity:** Insufficient session diversity (same starting points, same action sequences) may inflate PMI through trajectory clustering. Mitigation: use seeded random walk with different starting pages; report per-session PMI variance.

6. **Bonferroni conservatism:** 6 comparisons (3 sites × 2 K values) with Bonferroni correction is conservative. If title-aware PMI is marginally significant (raw p < 0.05 but corrected p >= 0.0125), this is reported as descriptive, not confirmatory.

---

*This preregistration is frozen before outcome inspection. Any changes after seeing results are exploratory and must be labelled as such.*
