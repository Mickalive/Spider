# EXP-PHYSICS-33788037373 — Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-33788037373
- **Lane**: Physics
- **Claims**: C-WEB-DYNAMICS ("Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity"), C-MEAS-VALID ("Measurement substrate is intervention-valid")
- **Date**: 2026-09-03
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Handoff**: EXP-PHYSICS-33528829431 ( REVISE — infrastructure defects prevent conclusion)

## 2. Scientific Question

Can trajectory-grouped holdout evaluation with richer state representation (DOM tree structure with element roles) and semantic action selectors reveal genuine action-conditioned transition structure on live Web pages with navigational density, replacing the coarse URL+hash representation that produced entropy inversion in EXP-PHYSICS-33528829431?

## 3. Background and Motivation

### What prior Physics work established

- **WP-001**: Weak mechanics-only signal above shuffle but imperfect post-state proxy
- **WP-002B**: 300 trajectories, 901 transitions; rule ~0.624, nearest-neighbour ~0.630, shuffle ~0.571; rule-shuffle +0.053; no website holdout
- **WP-003**: MEASUREMENT_INVALID (target leakage, invalid bootstrap, process-randomized hash)
- **EXP-PHYSICS-33528829431**: REVISE — four infrastructure defects identified by audit:
  1. In-sample evaluation (fit+evaluate on same data → memorization)
  2. Invalid bootstrap (resamples transitions not trajectories; declares significance on random null data)
  3. Non-discriminating positive control (9 globally unique actions → action_frequency_accuracy=1.0 trivially)
  4. Coarse state representation (URL+structure_hash+element_hash → entropy inversion artifact)
- **EXP-FRONTIER-33528827909**: Synthetic regime detection — monotonic rule-memory scaling with lambda (rho=1.0) but MEASUREMENT_INVALID (Bonferroni mismatch, saturated ANOVA)

### What this experiment addresses

The parent handoff identified four mandatory infrastructure fixes:

1. **Trajectory-grouped holdout evaluation** — entire trajectories in train or test, never split
2. **Trajectory-grouped permutation null** — permute action labels within trajectories, resample trajectories not transitions
3. **Positive control with overlapping actions** — same action types across states to discriminate (S,A) from A alone
4. **Richer state representation** — DOM tree structure with element roles, not URL+hash

Additionally:
5. **Semantic action selectors** — CSS selectors or ARIA roles, not link_N indices
6. **Navigational-density test sites** — sites with >10 internal links per page

This experiment implements all six fixes and re-tests C-WEB-DYNAMICS and C-MEAS-VALID on live Web.

### Why this matters

If the prior entropy inversion (-250%) was a state representation artifact (as the audit concluded), then richer representation should change the observed dynamics. If entropy inversion persists with DOM-tree representation, the claim is substantially weakened. If action-conditioned structure appears, the Physics lane has a validated substrate and a genuine signal to investigate.

## 4. Hypotheses

### H1: Action-conditioned structure exists on live Web (primary)
The action-conditioned predictor accuracy on held-out trajectories exceeds the trajectory-grouped permutation null distribution at Bonferroni-corrected p < 0.05 on at least 1 of 3 test sites.

### H2: Entropy reduction (directional)
H(S'|S,A) < H(S'|S) on held-out trajectories for at least 2 of 3 test sites, indicating action provides information about next state beyond current state alone.

### H3: Positive control passes
Action-conditioned predictor achieves >90% accuracy on held-out trajectories from the synthetic deterministic graph. Verifies pipeline captures deterministic transitions.

### H4: Null control passes
Null control entropy reduction < 15% on held-out trajectories. Verifies pipeline does not detect structure when absent.

### H5: Representation matters
The coarse URL+hash representation (B_PRIOR_COARSE baseline) shows different dynamics than the DOM-tree representation — specifically, the entropy inversion observed in EXP-PHYSICS-33528829431 does not persist with DOM-tree representation under trajectory-grouped holdout.

## 5. Data Collection

### 5.1 Test Sites

Three sites with navigational density:

| Site | URL | Rationale |
|------|-----|-----------|
| Wikipedia Main Page | https://en.wikipedia.org/wiki/Main_Page | Dense internal linking, predictable structure, ~50+ links per page |
| Wikipedia Category | https://en.wikipedia.org/wiki/Category:Featured_articles | List-based navigation, many internal links, structured content |
| example.com | https://www.example.com | Simple control site, few links, tests substrate on minimal site |

If a site fails to provide >=10 steps per trajectory, it is replaced with:
- https://www.iana.org/domains/example
- https://www.rfc-editor.org/rfc/rfc2606

### 5.2 State Representation

**DOM-tree state** (new, replaces coarse URL+hash):
- `url`: the page URL
- `dom_tree_hash`: SHA-256 hash of the element tag hierarchy (tags, attributes, nesting structure) extracted from raw HTML via HTMLParser. Captures page structure without full DOM.
- `element_roles_hash`: SHA-256 hash of interactive element roles (element tag + role inferred from tag: `<a>` → link, `<button>` → button, `<input>` → input, `<select>` → select, `<form>` → form, `<textarea>` → textarea). Captures what interactive elements exist.
- `text_structure_hash`: SHA-256 hash of text content structure (text node count, heading count, paragraph count). Captures content structure.

State key: `url|dom_tree_hash|element_roles_hash|text_structure_hash`

**Coarse state** (replication baseline B_PRIOR_COARSE):
- `url`: the page URL
- `structure_hash`: SHA-256 of tag count + element count + link count
- `element_hash`: SHA-256 of sorted link URLs (top 20)

State key: `url|structure_hash|element_hash` (same as EXP-PHYSICS-33528829431)

### 5.3 Action Representation

**Semantic actions** (new, replaces link_N indices):
- `action_type`: "click" for `<a>` tags, "submit" for `<form>` tags, "input" for `<input>`/`<textarea>`/`<select>` tags
- `selector`: CSS selector path to the element (e.g., `#content > ul > li:nth-child(3) > a`). If CSS selector is not computable from HTMLParser, use element tag + position within parent + nearest ancestor ID/class.
- `text`: visible text content of the element (truncated to 50 chars). Provides semantic identification.

Action key: `action_type|selector|text`

**Coarse actions** (replication baseline):
- `action_type`: "click"
- `target_id`: `link_N` (index in the link list)
- `parameters`: `link_text_N`

Action key: `action_type|target_id|parameters` (same as EXP-PHYSICS-33528829431)

### 5.4 Trajectory Collection

For each test site:
1. Start at the test URL
2. Extract state representation (DOM-tree or coarse)
3. Identify available actions (semantic or coarse)
4. Randomly select one action
5. Follow the action (HTTP fetch the target URL)
6. Record transition: (S, A, S')
7. Repeat from step 2 for max 10 steps
8. Collect 10 trajectories per site (30 total)

Total target: 30 trajectories x 10 steps = 300 transitions

### 5.5 Positive Control

Synthetic deterministic navigation graph (5 states, 3 action types, 9 transitions):
- States: A (home), B (products), C (about), D (contact), E (detail)
- Action types: click, navigate, scroll (overlapping across states)
- Deterministic transitions: A-click→B, A-navigate→C, A-scroll→D, B-click→E, B-navigate→A, C-click→A, D-click→A, E-click→B, E-navigate→A
- Invalid actions from a state → fallback to A

Collection: 50 trajectories x 10 steps = 500 transitions. Seed=42.

### 5.6 Null Control

Synthetic random-click transitions (20 page states, 3 action types, 5 target IDs):
- Next state is uniformly random, independent of action
- Actions are reused across states (same action types and targets)
- Same representation as live test (DOM-tree or coarse)

Collection: 20 trajectories x 10 steps = 200 transitions. Seed=44.

## 6. Evaluation Method

### 6.1 Trajectory-Grouped Holdout

For each test site:
1. Collect N trajectories
2. Assign trajectories to train (80%) or test (20%) using deterministic shuffle (seed=42)
3. ALL transitions from a trajectory stay in the same split
4. Fit predictors on train trajectories only
5. Evaluate on test trajectories only

This prevents information leakage between trajectories. Prior experiment used in-sample evaluation (fit+evaluate on same transitions), which produced memorization artifacts.

### 6.2 Action-Conditioned Predictor

Fit: For each (state_key, action_key) pair in train, compute majority-vote next_state.
Predict: On test, look up (state_key, action_key) and predict majority-vote next_state.
Cold start: For unseen (state_key, action_key) pairs, predict the most common next_state across all train data.

### 6.3 State-Only Predictor (B_STATE_ONLY)

Fit: For each state_key in train, compute majority-vote next_state (ignoring action).
Predict: On test, look up state_key and predict majority-vote next_state.

### 6.4 Trajectory-Grouped Permutation Null (B_PERM_NULL)

For each permutation i in 1..n_perm (n_perm=1000):
1. Within each trajectory, randomly permute action labels (preserve trajectory structure)
2. Fit action-conditioned predictor on permuted train
3. Evaluate on permuted test
4. Record accuracy_i

Null distribution: {accuracy_1, ..., accuracy_1000}
p-value: fraction of null accuracies >= observed accuracy

### 6.5 Entropy Metrics

- H(S'|S,A): conditional entropy of next state given (state, action), computed on held-out test trajectories
- H(S'|S): conditional entropy of next state given state only, computed on held-out test trajectories
- Entropy reduction: (H(S'|S) - H(S'|S,A)) / H(S'|S) * 100%

## 7. Controls

### 7.1 Positive Control (Synthetic Deterministic Graph)
- **Expected**: action-conditioned accuracy > 90% on held-out trajectories
- **Purpose**: Pipeline correctly captures deterministic transitions when they exist
- **Pass criterion**: accuracy > 0.90

### 7.2 Null Control (Random Clicks)
- **Expected**: entropy reduction < 15% on held-out trajectories
- **Purpose**: Pipeline does not detect action-conditioned structure when absent
- **Pass criterion**: entropy_reduction < 0.15

### 7.3 Representation Comparison (B_PRIOR_COARSE)
- **Expected**: Coarse URL+hash representation shows different dynamics than DOM-tree
- **Purpose**: Tests whether representation upgrade changes observed dynamics
- **Report**: Entropy reduction and permutation null p-value for both representations

## 8. Statistical Tests

### 8.1 Primary Test
- Permutation test: p-value = (number of null accuracies >= observed accuracy) / n_perm
- Bonferroni correction across test sites (3 sites → alpha_corrected = 0.05/3 = 0.0167)
- Significant if corrected p < 0.05 at any test site

### 8.2 Directional Test
- H(S'|S,A) < H(S'|S) on held-out test trajectories
- Report entropy reduction percentage per site
- Qualitative assessment: >5% reduction = meaningful, 0-5% = marginal, <0% = inversion

### 8.3 Effect Size
- Cohen's d for action-conditioned vs. permutation null accuracy (across n_perm permutations)
- Report per site

## 9. Decision Rules

### SURVIVES_CURRENT_TEST
If ALL of:
1. Action-conditioned predictor exceeds permutation null at Bonferroni-corrected p < 0.05 at >=1 test site
2. Positive control accuracy > 90% on held-out trajectories
3. Null control entropy reduction < 15%
4. >=200 valid transitions collected
5. No validity gate failures

### FALSIFIED-IN-SETTING
If ANY of:
1. Action-conditioned predictor does not exceed permutation null at any test site after correction
2. Entropy inversion persists (H(S'|S,A) >= H(S'|S) for all test sites)
3. Positive control accuracy < 90%
4. Null control entropy reduction >= 15%

### MEASUREMENT_INVALID
If:
1. <200 transitions collected
2. Validity gates fail
3. Infrastructure prevents execution

## 10. Validity Threats

### 10.1 HTTP Fetch Limitation
HTTP fetch + HTMLParser does not execute JavaScript. Dynamic pages may have incomplete state representation. **Mitigation:** Test sites are chosen for server-rendered content (Wikipedia, example.com). Documented limitation — results apply to server-rendered Web, not JavaScript-heavy SPAs.

### 10.2 DOM Tree Hash Coarseness
Hashing the DOM tree structure loses fine-grained detail. Two structurally similar pages may have different hashes or vice versa. **Mitigation:** Multiple hashes (tree structure, element roles, text structure) provide complementary views. This is still coarser than full DOM but richer than URL+tag counts.

### 10.3 CSS Selector Instability
CSS selectors based on position (nth-child) may be unstable across page loads. **Mitigation:** Use nearest ancestor ID/class when available; fall back to positional only when necessary. Report selector stability as a validity note.

### 10.4 Sample Size
Target 300 transitions (30 trajectories x 10 steps). Some trajectories may terminate early (<10 steps). Minimum viable: 200 transitions. **Mitigation:** Report actual sample size; MEASUREMENT_INVALID if <200.

### 10.5 Site Selection
Only 3 test sites. Results may not generalize. **Mitigation:** This is a substrate validation, not a universality claim. Wikipedia has high navigational density; example.com is a minimal control. Future experiments expand coverage.

### 10.6 Multiple Comparisons
3 test sites → Bonferroni correction factor 3. Conservative but appropriate for confirmatory test.

### 10.7 Cold-Start Bias
Unseen (state, action) pairs in test use a global most-common fallback. This may inflate accuracy if most transitions share a common next state. **Mitigation:** Report frequency of cold-start predictions separately.

## 11. Expected Outcomes

### 11.1 Positive Result (SURVIVES_CURRENT_TEST)
- Action-conditioned structure exists in live Web transitions under richer representation
- C-WEB-DYNAMICS advances from HYPOTHESIS
- C-MEAS-VALID substrate is validated for live Web
- Physics lane investigates the nature and scope of the structure
- Product lane considers action-conditioned prediction mechanisms

### 11.2 Negative Result (FALSIFIED-IN-SETTING)
- Action-conditioned structure is not detectable with DOM-tree representation and trajectory-grouped evaluation
- C-WEB-DYNAMICS is weakened: the claim requires either (a) even richer representation (accessibility tree, rendered DOM, network responses), or (b) the claim is false
- Physics lane pivots to: (1) Playwright-based accessibility tree collection, or (2) alternative mechanisms (information-theoretic, causal, multi-scale)
- C-MEAS-VALID may still be validated even if C-WEB-DYNAMICS is falsified

### 11.3 Inconclusive (MEASUREMENT_INVALID)
- Infrastructure cannot support the measurement
- Not scientific evidence for or against
- Debug and retry

## 12. Analysis Plan

1. **Collection**: HTTP fetch from 3 test sites, 10 trajectories each, 10 steps max. Positive control: 50 trajectories from synthetic graph. Null control: 20 trajectories from random clicks.
2. **State/Action Extraction**: DOM-tree hashes and semantic selectors from raw HTML. Coarse hashes for replication baseline.
3. **Trajectory-Grouped Split**: 80/20 by trajectory, seed=42.
4. **Predictor Fit**: Action-conditioned majority vote on train trajectories only.
5. **Evaluation**: Accuracy on held-out test trajectories.
6. **Permutation Null**: 1000 permutations of action labels within trajectories, independent RNG per permutation.
7. **Entropy Metrics**: H(S'|S,A), H(S'|S), entropy reduction on test trajectories.
8. **Controls**: Verify positive control >90%, null control <15% entropy reduction.
9. **Statistical Tests**: Permutation p-value, Bonferroni correction, Cohen's d.
10. **Reporting**: All outcomes reported with equal prominence.

## 13. Inherited State from Parent Handoff

### Established
- Synthetic feasibility with coarse representation
- HTTP fetch + HTMLParser can collect transitions
- Validity gates pass narrowly (no URL leakage, numpy seeds deterministic)

### Rejected
- C-MEAS-VALID not established (in-sample evaluation, invalid bootstrap)
- C-WEB-DYNAMICS not testable from prior experiment (entropy inversion is artifact)
- Producer SUPPORTS verdict rejected

### Unknown
- Whether richer state representation reveals action-conditioned structure
- Whether navigational-density sites support trajectory completion
- Whether trajectory-grouped holdout changes accuracy gaps
- Whether proper permutation nulls reject shuffle null
- Whether semantic actions capture invisible structure

### Do NOT Assume
- Do not assume live entropy inversion reflects real dynamics (artifact confirmed)
- Do not assume synthetic positive control discriminates (S,A) from A alone (trivial with unique actions)
- Do not assume bootstrap p-values from prior experiment are valid
- Do not assume in-sample accuracies generalize to held-out data
- Do not assume C-MEAS-VALID or C-WEB-DYNAMICS have been advanced by prior experiment

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
