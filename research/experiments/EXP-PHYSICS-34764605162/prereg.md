# EXP-PHYSICS-34764605162 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34764605162
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Parent**: EXP-PHYSICS-34724244876 (FALSIFIED-IN-SETTING on deterministic SPAs)
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

On production SPAs with non-deterministic rendering (React/Vue virtual DOM, auth-dependent content, external data), do DOM structural features encode predictive state variation that persists even with K>=3 sufficient action history?

Specifically:
1. Does conditional PMI I(S_next; DOM | URL, ActionHistory_K=3) exceed zero with Bonferroni-corrected permutation p < 0.0167?
2. Does a richer DOM representation (accessibility tree, computed styles, or multi-feature hash) capture variation invisible to visible_text_hash?

## 3. Motivation

### 3.1 Parent Experiment Findings

EXP-PHYSICS-34724244876 established on 3 deterministic Express SPAs (804 transitions):

| Site | K=1 PMI | K=2 PMI | K=3 PMI | K=3 Accuracy |
|------|---------|---------|---------|--------------|
| dashboard | 0.000 | 0.000 | 0.000 | 100% |
| multistep_form | 0.939 | 0.344 | 0.000 | 100% |
| wizard | 0.960 | 0.413 | 0.000 | 100% |

Key finding: DOM visible_text_hash adds conditional PMI only when action-history is truncated (K=1,2) but becomes fully redundant when history is sufficient (K=3). Effect is state-labeling via FSM state, not predictive dynamics beyond memory.

### 3.2 Why Production SPAs Are Materially Different

Deterministic Express SPAs have P(S_next | S_current, Action) = 1.0 — the same action from the same state always produces the same next state. Action-history memory at K=3 reconstructs the FSM state perfectly, making DOM redundant.

Production SPAs with React/Vue have non-deterministic rendering:
- The same action can lead to different DOM states depending on external factors (API responses, user data, timing, A/B tests, lazy loading)
- Virtual DOM diffing means DOM structure varies even when the logical state is the same
- Auth-dependent content creates user-specific DOM states
- External data feeds (social timelines, news, recommendations) create time-varying DOM

In this setting, action-history memory alone may be insufficient even at K=3, because the same action sequence can produce different outcomes. DOM structural features might encode this non-deterministic variation as predictive state information.

### 3.3 Why This Is the Last High-Setting for DOM-Based C-WEB-DYNAMICS

The parent handoff established:
- Deterministic SPAs: DOM hash is tautological with action history at K=3 (CLOSED)
- Production SPAs: the only remaining setting where DOM could encode genuinely predictive dynamics (OPEN)

A positive result justifies DOM integration. A negative result closes the DOM-hash representation path for C-WEB-DYNAMICS.

## 4. Hypotheses

### H1: Conditional PMI > 0 on Production SPAs
On production SPAs with non-deterministic rendering, conditional PMI I(S_next; DOM | URL, ActionHistory_K=3) > 0 with Bonferroni-corrected permutation p < 0.0167 on >= 2/3 tested SPAs (at least one DOM representation).

### H2: Richer Representations Capture More Variation
At least one of {accessibility_tree_hash, numeric_structural, multi_feature_hash} achieves higher conditional PMI than visible_text_hash on >= 1/3 tested SPAs.

### H3: Positive Control
Random DOM labels (SHA-256(counter), independent of state and action) yield conditional PMI within 3 standard deviations of 0.0.

### H4: Null Control
Shuffled DOM labels (permuted within action-history strata) yield conditional PMI within 3 standard deviations of 0.0.

### H5: Non-Determinism Confirmation
P(S_next | S_current, Action) accuracy < 1.0 on all tested production SPAs, confirming non-deterministic rendering.

## 5. Data Collection

### 5.1 Target Sites

Production SPAs with known non-deterministic rendering. Selection criteria:
- Client-side rendering (React, Vue, Angular)
- Dynamic content (user-specific, time-varying, API-dependent)
- Publicly accessible (no auth required for basic navigation)
- Multiple pages/states reachable via standard actions

Proposed sites (execution agent may substitute equivalent alternatives):
1. A React-based news/aggregation site with dynamic feeds
2. A Vue-based dashboard or tool with user-specific content
3. A React-based e-commerce/catalog site with dynamic product listings

### 5.2 Crawling Protocol

For each site:
1. Navigate to the site and wait for full render
2. Perform a sequence of standard actions (click navigation, scroll, form interactions)
3. Capture DOM snapshot at each step
4. Record action, URL, timestamp
5. Repeat from the same starting point with different timing/session to elicit non-determinism
6. Collect >= 50 trajectories per site, >= 10 transitions per trajectory (>= 500 total transitions)

### 5.3 Data Format

For each transition t:
- `trajectory_id`: unique trajectory identifier
- `step`: integer step within trajectory
- `url`: page URL
- `action`: action performed (type + target)
- `dom_before`: DOM snapshot before action
  - `visible_text_hash`: SHA-256 of visible text content
  - `accessibility_tree_hash`: SHA-256 of accessibility tree structure
  - `numeric_structural`: {element_count, tree_depth, interactive_density, form_count, input_count, button_count}
- `dom_after`: DOM snapshot after action (same fields)
- `s_next`: state label (SHA-256 of dom_after.visible_text_hash)

### 5.4 Filtering

Exclude transitions where:
- Page failed to load (timeout, network error)
- Auth redirect occurred
- DOM capture is incomplete or malformed
- Action was not executed (e.g., click on non-interactive element)

## 6. State and Action Representation

### 6.1 State
S = DOM snapshot after action (one of 4 representations tested independently):
- visible_text_hash: SHA-256(visible_text)
- accessibility_tree_hash: SHA-256(accessibility_tree)
- numeric_structural: (element_count, tree_depth, interactive_density, form_count)
- multi_feature_hash: SHA-256(visible_text + element_count + tree_depth + interactive_density)

### 6.2 Action
A = (action_type, action_target) tuple. Action types: click, scroll, type, navigate, submit.

### 6.3 Action History
H_K = (A_{t-K+1}, ..., A_t) — last K actions. K ∈ {1, 2, 3}.

### 6.4 Strata
Strata are defined by (url, H_K). For large action vocabularies, merge rare strata (< 5 transitions) using the parent's MIN_STRATUM_COUNT=5 threshold.

## 7. Measures

### 7.1 Conditional PMI

For each (site, representation, K):

I(S_next; DOM | URL, H_K) = Σ_{s, d, h} p(s, d, h) * log2[ p(s, d | h) / (p(s | h) * p(d | h)) ]

Where:
- s = S_next (next state)
- d = DOM representation (before action)
- h = (url, H_K) stratum
- p(s, d | h) = joint empirical distribution within stratum
- p(s | h) = marginal over s within stratum
- p(d | h) = marginal over d within stratum

Compute using empirical counts within strata, with MIN_STRATUM_COUNT=5 (same as parent).

### 7.2 Permutation Test

For each (site, representation, K):
1. Compute observed PMI
2. Shuffle DOM labels within action-history strata 1000 times
3. Compute permuted PMI for each shuffle
4. p-value = fraction of permuted PMI >= observed PMI
5. Bonferroni correction across all (site, representation, K) combinations

### 7.3 Action-History Prediction Accuracy

For each K:
- Fit: most frequent S_next per (url, H_K) stratum
- Predict: on each transition, predict most frequent S_next for its stratum
- Report: accuracy = fraction correct

### 7.4 Determinism Check

Compute P(S_next | S_current, Action):
- For each (S_current, Action) pair, check if all transitions yield the same S_next
- Report: accuracy = fraction of deterministic transitions

### 7.5 Primary Metric

conditional_pmi_K3 = mean conditional PMI at K=3 across sites and representations that pass controls.

### 7.6 Secondary Metrics

- PMI by K (K=1,2,3) for each site and representation
- Action-history accuracy by K
- Determinism accuracy per site
- Effect size (Cohen's d) for PMI vs 0
- Number of valid transitions per site
- Strata coverage (fraction of strata with >= 5 transitions)

## 8. Null Models

### 8.1 Shuffle Null (Primary)
Permute DOM labels within action-history strata. Preserves marginal distributions of DOM and action-history while breaking DOM-state correspondence. Expected PMI: 0.0.

### 8.2 Frequency Null
Predict next state from marginal distribution P(S_next). Expected accuracy: 1/n_states.

### 8.3 Action-Only Null
Predict next state from action-history only (no DOM). This is the strong beyond-memory null — if action-history alone achieves high accuracy, DOM cannot add predictive value.

## 9. Statistical Tests

### 9.1 Primary Test
- Permutation test for conditional PMI > 0
- One-sided: PMI > 0
- 1000 permutations per (site, representation, K)
- Bonferroni correction across all combinations (n_sites * n_representations * n_K_values)
- Significance threshold: corrected p < 0.0167 (equivalent to alpha=0.05 across 3 comparisons)

### 9.2 Effect Size
- Cohen's d for observed PMI vs permuted distribution mean
- Report for each (site, representation, K)

### 9.3 Multi-Site Consistency
- Fraction of sites where PMI > 0 and significant
- Decision requires >= 2/3 sites surviving

## 10. Controls

### 10.1 Positive Control (Random Labels)
Generate random DOM labels as SHA-256(counter) where counter increments per transition, independent of state and action. Compute conditional PMI. Expected: approximately 0.0 (within noise). Pass criterion: |PMI| < 3 * std(permuted PMI).

This fixes the parent's positive control failure (synthetic SPA had deterministic FSM-coupled labels, PMI=1.69 bits).

### 10.2 Null Control (Shuffled Labels)
Shuffle DOM labels within action-history strata (1000 shuffles). Expected: mean shuffled PMI approximately 0.0. Pass criterion: |mean shuffled PMI| < 3 * std(shuffled PMI).

### 10.3 Determinism Control
On production SPAs with non-deterministic rendering, P(S_next | S_current, Action) accuracy should be < 1.0. If accuracy = 1.0, the SPA is deterministic and the result is interpretable under the parent's setting, not the production setting.

### 10.4 Data Quality Control
Each surviving SPA must have >= 300 valid transitions after filtering. If a SPA has < 300, it is excluded from the primary analysis but reported.

## 11. Validity Threats

### 11.1 Large State Space
Production SPAs have much larger state spaces than deterministic Express SPAs (10 states). This means:
- More strata, more sparse strata, more excluded transitions
- PMI estimation may be noisy
- Mitigation: MIN_STRATUM_COUNT=5 (same as parent), report effective N per stratum

### 11.2 Representation Loss
Hash-based representations collapse continuous DOM variation. The same visible text with different formatting produces the same hash.
- Mitigation: test multiple representations including accessibility tree and numeric structural features

### 11.3 Non-Determinism Measurement
Non-deterministic rendering may be time-dependent (same action at different times produces different DOM). This is the phenomenon under test, not a validity threat. However, if non-determinism is very low, PMI may be small and hard to detect.
- Mitigation: collect data across multiple sessions/timing to elicit non-determinism

### 11.4 Network and Crawl Failures
Production SPAs may have slow loads, CAPTCHAs, rate limiting, or auth prompts.
- Mitigation: retry failed transitions, exclude auth redirects, set timeout thresholds

### 11.5 Multiple Comparisons
Testing n_sites * n_representations * n_K_values combinations inflates false positive risk.
- Mitigation: Bonferroni correction (conservative), report both corrected and uncorrected p-values

### 11.6 Synthetic-to-Real Gap
This experiment uses real production SPAs, not synthetic data. The findings directly apply to the tested sites but generalization requires replication.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Conditional PMI I(S_next; DOM | URL, ActionHistory_K=3) > 0.0 with Bonferroni-corrected permutation p < 0.0167 on >= 2/3 tested production SPAs (at least one DOM representation per site)
2. Positive control passes (|random-label PMI| < 3 * std(permuted))
3. Null control passes (|shuffled-label PMI| < 3 * std(shuffled))
4. Determinism check confirms non-deterministic rendering (accuracy < 1.0) on all surviving SPAs
5. >= 300 valid transitions per surviving SPA

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. Conditional PMI <= 0.0 or non-significant (Bonferroni p >= 0.0167) on ALL tested SPAs AND ALL representations
2. Positive control fails (|random-label PMI| >= 3 * std(permuted))
3. Null control fails (|shuffled-label PMI| >= 3 * std(shuffled))
4. All SPAs have determinism accuracy = 1.0 (no non-deterministic rendering found)

### 12.3 MEASUREMENT_INVALID
If:
1. < 300 valid transitions per SPA after filtering
2. Pipeline errors prevent PMI computation
3. All SPAs excluded due to data quality

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- DOM integration into SPIDER's observation layer is warranted for production SPAs
- Non-deterministic rendering creates genuine environmental dynamics where DOM encodes predictive state variation beyond action-history memory
- SPIDER should capture and transmit DOM structural features as part of its observation substrate
- C-WEB-DYNAMICS survives at the production SPA level
- Physics lane should investigate what specific DOM features are most predictive and whether the effect is robust across site types

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- DOM hash-based state labeling is not predictive dynamics across all tested settings (deterministic + production SPAs)
- The DOM integration path for C-WEB-DYNAMICS is closed for visible_text_hash and related representations
- SPIDER should focus on action-history-based state tracking and other representations (network responses, API payloads, visual structure)
- Physics lane should try orthogonal approaches (information-theoretic on network data, causal, multi-scale)

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- Production SPA crawling infrastructure needs improvement before this question can be answered
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Data Collection**: Crawl 3 production React/Vue SPAs, collect >= 500 transitions each
2. **Data Filtering**: Exclude failed loads, auth redirects, incomplete DOM captures
3. **DOM Representation**: Compute 4 representations per transition (visible_text_hash, accessibility_tree_hash, numeric_structural, multi_feature_hash)
4. **Action History**: Construct H_K for K=1,2,3 from trajectory step ordering
5. **Strata**: Group by (url, H_K), apply MIN_STRATUM_COUNT=5
6. **Conditional PMI**: Compute for each (site, representation, K)
7. **Permutation Test**: 1000 shuffles per (site, representation, K), Bonferroni correction
8. **Controls**: Positive (random labels), null (shuffled labels), determinism check
9. **Decision**: Apply frozen decision rule
10. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `hashlib` for SHA-256 hashing of DOM representations
- `numpy` for array operations
- `collections.Counter` for empirical distributions
- `scipy.stats` for effect sizes
- Standard library only for PMI computation (no custom estimators required)

Code will be committed to `research/experiments/EXP-PHYSICS-34764605162/` before execution.

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
