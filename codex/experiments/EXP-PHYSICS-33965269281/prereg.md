# EXP-PHYSICS-33965269281 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-33965269281
- **Lane**: Physics
- **Claims**: C-MEAS-VALID (Measurement substrate is intervention-valid), C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-05
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does a browser-based collection substrate with full DOM and accessibility tree state representation reveal action-conditioned transition structure on live Web pages with navigational density, beyond what HTTP fetch with URL-only representation can detect?

## 3. Motivation

### 3.1 Prior Art

- **WP-001**: Weak mechanics-only signal above shuffle (imperfect post-state proxy)
- **WP-002B**: 300 trajectories, 901 transitions, rule ~0.62, NN ~0.63, shuffle ~0.57, rule-shuffle +0.053
- **WP-003**: MEASUREMENT_INVALID (target leakage, bootstrap invalid, hash seed)
- **EXP-PHYSICS-33528829431**: First live-Web attempt with methodology defects (in-sample evaluation, invalid bootstrap, non-discriminating positive control)
- **EXP-PHYSICS-33788037373**: Corrected methodology with trajectory-grouped holdout, permutation null, overlapping-action positive control. Synthetic controls validated. Live results: Wikipedia 0.0 accuracy, Python docs 0.033 accuracy (SA == AF, diff ~0.0). MEASUREMENT_INVALID due to: (1) state representation degraded to URL-only (composite state not stored), (2) target_href encoding bug (source URL not destination), (3) Bonferroni correction not applied as specified (2x not 6x), (4) artifact hashes missing.

### 3.2 Why This Experiment

The prior MEASUREMENT_INVALID result cannot be interpreted as evidence for or against Web dynamics because the measurement substrate was defective. The handoff identified four mandatory fixes and recommended browser-based collection for richer state representation.

Playwright is now available in the execution environment (playwright 1.62.0, Chromium headless shell 151.0.7922.34). This enables:
- Full DOM parsing via `page.content()`
- Accessibility tree extraction via `page.accessibility.snapshot()`
- JavaScript execution (handling SPAs and dynamic content)
- Reliable link extraction with rendered text

This experiment directly tests whether the representation was the limiting factor in the prior measurement failure, with adequate sample size (>100 trajectories/site as recommended by parent handoff) to detect small effects after trajectory-grouped holdout.

### 3.3 What Changed from EXP-PHYSICS-33788037373

1. **State representation**: URL + title + link_texts + tag_counts + form_signals + accessibility tree roles/states (stored in raw data, not just hashed)
2. **Collection substrate**: Playwright (browser-based) instead of HTTP fetch + HTMLParser
3. **Target_href encoding**: Set to destination URL (not source URL)
4. **Bonferroni correction**: Applied for 6 comparisons (3 null tests × 2 live sites) as specified
5. **Artifact integrity**: All raw/derived files have sha256 hashes in result.json

## 4. Hypotheses

### H1: Positive Control Discrimination
The synthetic positive control with overlapping actions will show action-conditioned accuracy significantly > action-frequency accuracy on held-out data (permutation test p < 0.05).

### H2: Positive Control Accuracy
The synthetic positive control will achieve > 90% held-out action-conditioned accuracy, demonstrating the pipeline can learn deterministic transitions.

### H3: Null Control Passes
The random-policy null control will show no significant action-conditioned structure (permutation test p > 0.05), demonstrating no false positives.

### H4: Live Action-Conditioned Structure
At least one live site (Wikipedia or Python docs) will show action-conditioned structure above shuffle after Bonferroni correction for 6 comparisons (p_corr < 0.05), with effect size (diff_SA_vs_shuffle) > 0.03.

### H5: Representation Improves Detection
Browser-collected data will show higher diff_SA_vs_shuffle than the HTTP fetch baseline (0.03 for Python docs, 0.0 for Wikipedia) on the same sites, with adequate power (>= 100 trajectories/site), demonstrating that richer state representation reveals structure hidden by URL-only identity.

## 5. Data Collection

### 5.1 Synthetic Positive Control

- 8 states, 3 action types with overlapping actions
- Actions: click (shared across states), navigate (shared), submit (shared)
- 60 trajectories of 10 steps each = 600 transitions
- Deterministic transitions from synthetic graph
- State representation: synthetic state ID (no browser needed)

### 5.2 Null Control

- 30 states, 5 action types, 8 target_ids shared across states
- Next-states uniformly random, independent of action
- 30 trajectories of 10 steps each = 300 transitions
- State representation: synthetic state ID

### 5.3 Live Web Sites

**Site 1: en.wikipedia.org**
- Start URL: https://en.wikipedia.org/wiki/Web_browser
- Collection: Follow internal links (same domain only)
- Target: 100+ trajectories, 8 steps each
- Navigational density: high (dense internal link structure)

**Site 2: docs.python.org**
- Start URL: https://docs.python.org/3/library/index.html
- Collection: Follow internal links (same domain only)
- Target: 100+ trajectories, 8 steps each
- Navigational density: high (dense documentation links)

### 5.4 Browser-Based Collection Protocol

For each trajectory (target: 100+ trajectories per site):
1. Navigate to start URL using Playwright
2. Wait for page load (networkidle)
3. Extract state representation:
   - URL (page.url)
   - Title (page.title())
   - Link texts (first 30 visible <a> text contents)
   - Tag counts (11 categories: h1,h2,h3,form,input,button,select,textarea,nav,main,aside)
   - Form signals (4 booleans: has_form, has_input, has_select, has_textarea)
   - Accessibility tree snapshot (page.accessibility.snapshot())
4. Extract available actions: all clickable <a> elements with href (same domain) and text
5. Randomly select one action (uniform random over available links)
6. Execute action (page.click or page.goto)
7. Wait for navigation
8. Record transition: (state_before, action, state_after, trajectory_id, step_index)
9. Repeat for 8-10 steps per trajectory
10. Restart at new start URL for next trajectory

### 5.5 Sample Size

- Synthetic positive control: 600 transitions (60 trajectories x 10 steps)
- Null control: 300 transitions (30 trajectories x 10 steps)
- Live Wikipedia: >= 800 transitions (100 trajectories x 8 steps)
- Live Python docs: >= 800 transitions (100 trajectories x 8 steps)
- Total: >= 2500 transitions

## 6. State and Action Representation

### 6.1 State (Browser-Collected)

```python
@dataclass(frozen=True)
class State:
    url: str                          # page URL
    title: str                        # page title
    link_texts: tuple                 # sorted tuple of first 30 visible link texts
    tag_counts: tuple                 # 11 integers: h1,h2,h3,form,input,button,select,textarea,nav,main,aside
    form_signals: tuple               # 4 booleans: has_form, has_input, has_select, has_textarea
    accessibility_roles: tuple        # sorted tuple of (role, name) from accessibility tree
```

State key: SHA-256 hash of all fields, truncated to 16 hex characters.

### 6.2 Action

```python
@dataclass(frozen=True)
class Action:
    action_type: str                  # "click" (all actions are link clicks)
    target_text: str                  # visible text of clicked link
    target_href: str                  # destination URL (NOT source URL)
```

Action key: `action_type|target_text|target_href`

### 6.3 Raw Data Storage

Every transition stores the FULL state representation (not just the key hash):
```json
{
    "trajectory_id": "...",
    "step_index": 0,
    "state_before": {
        "url": "...",
        "title": "...",
        "link_texts": ["...", "..."],
        "tag_counts": [1, 2, ...],
        "form_signals": [true, false, ...],
        "accessibility_roles": [("link", "Home"), ...]
    },
    "action": {
        "action_type": "click",
        "target_text": "...",
        "target_href": "..."
    },
    "state_after": {
        "... same structure ..."
    }
}
```

## 7. Measures

### 7.1 Primary Metric
- **diff_SA_vs_shuffle**: accuracy(SA_heldout) - accuracy(shuffle_heldout)
- **diff_SA_vs_AF**: accuracy(SA_heldout) - accuracy(AF_heldout)

### 7.2 Statistical Tests
- Permutation test (1000 permutations) for SA vs shuffle at each site
- Permutation test for SA vs AF at positive control and each site
- Bonferroni correction: 6 comparisons (2 live sites × 3 tests)
- Paired comparison: browser-collected diff_SA_vs_shuffle vs HTTP fetch baseline

### 7.3 Secondary Metrics
- accuracy_SA_train, accuracy_SA_heldout, accuracy_AF_heldout, accuracy_state_heldout
- memorization ratio (in-sample / held-out)
- Effect sizes (Cohen's d where applicable)
- Collection time per trajectory

## 8. Null Models

### 8.1 Shuffle Null
Permute next_state labels within each trajectory (trajectory-grouped). Rules trained on shuffled data should perform like action-frequency (no state advantage).

### 8.2 Action-Frequency Null
Predict most common next_state per action type, ignoring current state. Tests whether action alone predicts next state without state context.

### 8.3 First-Order Markov Null
Predict next_state from current state only, ignoring action. Tests whether action adds predictive power beyond state identity.

## 9. Controls

### 9.1 Positive Control (Synthetic Graph)
- **Expected**: SA_heldout > 90%, SA >> AF, p < 0.05
- **Purpose**: Verifies pipeline can learn deterministic transitions with overlapping actions

### 9.2 Null Control (Random Policy)
- **Expected**: SA ≈ AF ≈ chance, p > 0.05
- **Purpose**: Verifies no false positives on unstructured data

### 9.3 HTTP Fetch Comparison
- **Expected**: Browser-collected diff_SA_vs_shuffle > HTTP fetch diff (0.03 max)
- **Purpose**: Tests whether representation improvement changes detection outcome

## 10. Validity Gates

All of the following must pass or verdict is MEASUREMENT_INVALID:

1. **Trajectory-grouped holdout**: No trajectory appears in both train and test
2. **Trajectory-grouped permutation null**: Permutations within trajectories only
3. **Positive control discrimination**: SA > AF on held-out data (p < 0.05)
4. **No target leakage**: Action features do not contain next-state information
5. **Target_href encoding**: target_href = destination URL (not source)
6. **Full state representation**: Raw data contains url, title, link_texts, tag_counts, form_signals for every transition
7. **Deterministic seeds**: All RNG uses random.Random(seed), not hash()
8. **Temporal ordering**: Step indices monotonically increasing within trajectories
9. **Artifact integrity**: result.json artifacts populated with sha256 hashes
10. **Sample size**: >= 100 live transitions per site

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Positive control discriminates (SA > AF, p < 0.05)
2. Positive control accuracy > 90% held-out
3. Null control passes (p > 0.05)
4. At least one live site shows SA vs shuffle p < 0.05 after 6x Bonferroni correction
5. All validity gates pass
6. >= 100 live transitions per site (>= 800 total live)
7. diff_SA_vs_shuffle on at least one site > 0.03

### 11.2 FALSIFIED-IN-SETTING
If (1)-(3) pass but:
- No live site shows significant structure after correction (all p_corr > 0.05)
- AND effect sizes are < 0.05 on all sites

### 11.3 MEASUREMENT_INVALID
If any validity gate fails or infrastructure prevents collection.

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- First measurement-valid positive signal for Web dynamics on live Web
- Validates browser-based collection as necessary for Physics measurement
- Justifies investment in Playwright-based measurement substrates
- C-WEB-DYNAMICS moves from HYPOTHESIS toward EXPERIMENTAL
- C-MEAS-VALID strengthened (browser-based validation, adequate sample size)

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Browser-based collection with full state does NOT reveal structure on these sites (with adequate power: >= 100 trajectories/site)
- Constrains C-WEB-DYNAMICS to richer representations (visual layout, interaction sequences) or different site types
- Does NOT close Physics domain -- only this detection method on these sites
- C-MEAS-VALID partially supported (pipeline validated, null control passes)

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging or infrastructure improvement
- Not scientific evidence for or against
- Prior MEASUREMENT_INVALID streak continues -- consider fundamental redesign

## 13. Analysis Plan

1. **Collect**: Playwright-based transitions on synthetic controls and 2 live sites (>100 trajectories/site)
2. **Split**: Trajectory-grouped 70/30 train/test (seed=42)
3. **Fit**: Rule baseline (majority vote per (state, action)) on train
4. **Evaluate**: Accuracy on test for rule, action-frequency, state-only, shuffle
5. **Permutation test**: 1000 trajectory-grouped permutations (seeds 1000-1005)
6. **Bonferroni**: Correct for 6 comparisons
7. **Compare**: Browser-collected results vs HTTP fetch baseline from EXP-PHYSICS-33788037373
8. **Report**: All outcomes with equal prominence

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
