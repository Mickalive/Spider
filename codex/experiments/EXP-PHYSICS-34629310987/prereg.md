# EXP-PHYSICS-34629310987 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34629310987
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Parent**: EXP-PHYSICS-34524411213 (DOM structural features falsified on TodoMVC)
- **Date**: 2026-09-11
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the accessibility tree — a semantically richer structural representation capturing element roles, names, states, and relationships rather than raw DOM counts — provide predictive state information beyond URL on genuine SPA/form-heavy sites where the same URL hosts different states?

## 3. Motivation

Prior Physics work established:
- URL-only PMI is strongly positive on TodoMVC: React 0.670 bits, Vue 0.751 bits (EXP-PHYSICS-34524411213)
- DOM structural features (element_count, tree_depth, interactive_density) are significantly predictive but strictly worse than URL-only on TodoMVC (DOM PMI -0.073 bits worse on React, -0.006 on Vue)
- The rejected hypothesis was that raw DOM counts improve over URL

The accessibility tree is a materially orthogonal level of description:
- DOM structural features: quantitative (how many elements, how deep, how interactive)
- Accessibility tree: semantic (what elements are, what they do, what state they're in)

A multi-step form at step 2 vs step 3 may have identical element counts but very different accessibility trees: different labels ("Shipping" vs "Payment"), different visible/hidden regions, different focused elements, different ARIA states.

The key validity insight from the parent experiment: on TodoMVC, URL perfectly identifies state (URL entropy = 3.7 bits, unique URLs = 13 per site). There is no URL ambiguity to exploit. The test must use sites where the same URL hosts different states — client-side-routed form-heavy SPAs.

## 4. Hypotheses

### H1: Accessibility-Tree Gain
On transitions where the URL does not change (within-URL transitions), accessibility-tree PMI exceeds URL-only PMI by >= 0.1 bits.

### H2: Accessibility-Tree Variability
The accessibility tree varies within the same URL: entropy of accessibility-tree states given URL > 0 on >= 1 site.

### H3: Positive Control
On a synthetic SPA with deterministic accessibility-tree evolution, accessibility-tree PMI >= 0.5 bits (permutation p < 0.001).

### H4: Null Control
Shuffled accessibility-tree labels produce PMI not significantly > 0 (permutation p > 0.01).

### H5: URL-Ambiguity Quantification
URL entropy reduction on the test sites is substantially lower than on TodoMVC (where URL entropy reduction was 3.2-3.4 bits), confirming the sites have genuine URL ambiguity.

## 5. Site Selection

### 5.1 Required Properties
- Client-side routing: same URL hosts multiple form steps
- Form-heavy: multi-step workflows with user input at each step
- Accessibility tree varies across steps: different element roles/names/states
- Genuinely reachable: publicly accessible without authentication

### 5.2 Candidate Sites
- **Tally** (tally.so): Form builder with client-side step routing. Same URL for different form steps. Accessibility tree changes (different labels, input fields, visible regions).
- **Google Forms** (docs.google.com/forms): Multi-step forms with URL parameters. Same base URL, different accessibility tree per section.
- **Typeform** (typeform.com): Multi-step forms with hash/history routing.

### 5.3 Selection Criteria
Each site must satisfy:
1. >= 3 distinct form steps reachable under the same URL (verified by accessibility tree hash variation)
2. At least 10 form submissions or step progressions collectible
3. No authentication wall blocking automated access

### 5.4 Site Limitation
Results apply only to the tested sites. No cross-site universality claim is made.

## 6. Data Collection

### 6.1 Browser Automation
- Playwright Chromium, headless mode
- Navigate to form URL
- At each step: wait for network idle, extract accessibility tree via `page.accessibility.snapshot()`
- Progress through form by interacting with visible elements (click buttons, fill inputs)
- Record: URL, accessibility tree, timestamp, action taken

### 6.2 Accessibility Tree Processing
From raw `page.accessibility.snapshot()`:
1. Recursively extract all nodes
2. Filter: exclude `Presentation`, `None`, `generic` roles; exclude pure text nodes without semantic role
3. For each remaining node: `(role, name, focused, expanded, checked, disabled, selected)` — the semantic tuple
4. Hash: `SHA256(str(sorted(visible_semantic_tuples)))` → discrete state identifier
5. This produces an accessibility-tree state hash at each step

### 6.3 Transition Recording
Each observed transition:
```
{
  "site": "...",
  "url_t": "URL at step t",
  "a11y_hash_t": "accessibility tree hash at step t",
  "url_t1": "URL at step t+1",
  "a11y_hash_t1": "accessibility tree hash at step t+1",
  "action": "action taken at step t",
  "timestamp": "..."
}
```

### 6.4 Leakage Classification
- **Non-leakage**: URL changes via hash (#), history.pushState, or standard link navigation with different path
- **Leakage**: URL remains identical AND no navigation event occurred (client-side state update only)
- Within-URL transitions are a subset of non-leakage transitions where url_t == url_t1

## 7. State Representations

### 7.1 URL-Only State
- State = URL (full string, including hash/query)
- PMI: P(URL_t1 | URL_t) pointwise mutual information
- Same computation as parent experiment

### 7.2 Accessibility-Tree-Only State
- State = accessibility-tree hash (SHA256 of sorted semantic tuples)
- PMI: P(a11y_hash_t1 | a11y_hash_t)

### 7.3 URL + Accessibility-Tree State
- State = (URL, accessibility-tree hash) concatenated
- PMI: P((URL_t1, a11y_hash_t1) | (URL_t, a11y_hash_t))
- Tests whether the combination provides more than URL alone

### 7.4 Discretization
- All state representations are already discrete (URL strings, SHA256 hashes)
- No binning or discretization edges needed (unlike continuous DOM features in parent)
- Laplace smoothing alpha = 1.0 for PMI computation (matching parent)

## 8. Primary Metric

### 8.1 Within-URL Gain
```
gain_within_url = mean over sites of (PMI_a11y - PMI_url) on transitions where url_t == url_t1
```

Primary decision: `gain_within_url >= 0.1 bits`

### 8.2 Overall Gain
```
gain_overall = mean over sites of (PMI_a11y - PMI_url) on all non-leakage transitions
```

Secondary: reported for context but not primary decision (URL and accessibility tree may be confounded on between-URL transitions).

## 9. Statistical Tests

### 9.1 Permutation Test
- For each site: permute accessibility-tree labels (a11y_hash_t) across transitions 1000 times
- Compute permuted PMI for each permutation
- p-value = fraction of permutations with PMI >= observed PMI
- Bonferroni correction: 4 comparisons (2 sites x 2 conditions: within-URL and overall)

### 9.2 Effect Size
- Cohen's d for PMI difference (accessibility-tree vs URL) on within-URL transitions
- Bootstrap 95% CI for gain_within_url (1000 resamples, stratified by site)

### 9.3 Entropy Analysis
- H(URL | site): entropy of URL distribution per site
- H(a11y_hash | site): entropy of accessibility-tree hash distribution per site
- H(a11y_hash | URL, site): entropy of accessibility-tree hash given URL per site
- If H(a11y_hash | URL) = 0, accessibility tree is fully determined by URL (no independent information)

## 10. Controls

### 10.1 Positive Control (Synthetic SPA)
- 8 states, 4 actions, deterministic transitions
- Accessibility tree uniquely identifies each state (different (role, name) tuples per state)
- Expected: PMI >= 0.5 bits, permutation p < 0.001
- Verifies pipeline detects accessibility-tree structure when present

### 10.2 Null Control (Shuffled Labels)
- Permute accessibility-tree hashes across transitions
- Expected: PMI not significantly > 0 (permutation p > 0.01)
- Verifies pipeline does not detect random label associations

### 10.3 URL-Ambiguity Control
- Measure URL entropy reduction on test sites
- Compare to TodoMVC (URL entropy reduction 3.2-3.4 bits)
- If URL entropy reduction is high (>= 3 bits), URL is not ambiguous and the test is uninformative
- Require URL entropy reduction < 2 bits for site to be included in primary analysis

### 10.4 DOM Structural Features Replication
- Compute DOM PMI (element_count, tree_depth, interactive_density) on same data
- Expected to replicate parent: DOM PMI < URL-only PMI
- Verifies consistency with parent experiment

## 11. Validity Threats

### 11.1 URL-Accessibility Tree Confounding
When URL changes, accessibility tree almost certainly changes too. Between-URL PMI differences may reflect URL information, not accessibility-tree information. **Mitigation**: Primary analysis is restricted to within-URL transitions where url_t == url_t1. This is the critical test.

### 11.2 Accessibility Tree Stability
Dynamic content (animations, lazy loading, ads) may cause accessibility tree hash instability across identical states. **Mitigation**: Wait for network idle before snapshotting; use sorted hash to ignore ordering; test reproducibility on 5 repeated navigations to the same step.

### 11.3 Form Interaction Artifacts
Filling in form fields changes the accessibility tree (input values, validation messages). These changes are step-dependent but not step-predictive — they reflect user input, not site state. **Mitigation**: Record form field values; test whether PMI persists when input-dependent elements are excluded from the hash.

### 11.4 Site Selection Bias
Only 2-3 sites tested. Results do not generalize to all SPAs. **Mitigation**: Bounded claim ceiling. No cross-site universality claim.

### 11.5 Sample Size
With 50+ transitions per site and 1000 permutations, power is adequate for large effects (d > 0.8). Smaller effects may be missed. **Mitigation**: Report confidence intervals; do not claim "no effect" for non-significant results — claim "insufficient evidence."

### 11.6 Accessibility Tree Representation Choice
Hashing sorted (role, name, state) tuples is one discretization. Other representations (tree edit distance, embedding) might perform differently. **Mitigation**: This tests the simplest semantic representation; failure does not close the broader semantic-structure hypothesis.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. gain_within_url >= 0.1 bits (mean across sites)
2. Accessibility-tree permutation p < 0.01 after Bonferroni (4 comparisons)
3. Positive control passes (synthetic SPA PMI >= 0.5)
4. Null control passes (shuffled PMI not > 0, p > 0.01)
5. Accessibility tree varies within URL (entropy > 0 on >= 1 site)
6. Data sufficiency (>= 50 non-leakage transitions per site)

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. gain_within_url < 0.1 bits (accessibility-tree <= URL-only on within-URL transitions)
2. Accessibility tree does not vary within URL on any site (entropy = 0 everywhere)
3. Positive control fails
4. Null control fails (pipeline detects structure in random labels)

### 12.3 MEASUREMENT_INVALID
If:
1. < 50 non-leakage transitions per site
2. No sites with genuine URL ambiguity (all have URL entropy reduction >= 2 bits)
3. Pipeline errors prevent PMI computation
4. Accessibility tree extraction fails on all test sites

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- Accessibility-tree structure provides dynamical information beyond URL on form-heavy SPAs
- SPIDER should use accessibility-tree snapshots as state representation for client-side-routed workflows
- State-space representation shifts from location-based (URL) to semantics-based (accessibility tree)
- Product architecture: store accessibility-tree hashes in operational knowledge graph alongside URL

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- Accessibility tree provides no gain over URL-only on tested sites
- Semantic structure (roles, names, states) does not predict transitions better than location
- SPIDER should rely on URL-based state or seek other signals (network requests, cookies, JS state)
- Does NOT falsify C-WEB-DYNAMICS — only this specific semantic representation

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- No suitable sites with URL ambiguity, or pipeline failure
- Not evidence for or against the hypothesis

## 14. Analysis Code

Analysis will be implemented in Python using:
- `playwright` for browser automation and accessibility snapshot extraction
- `hashlib` for SHA256 hashing of accessibility tree states
- `numpy` for PMI computation and permutation testing
- `scipy.stats` for entropy computation
- Standard library only for state discretization

Code will be committed to `research/physics/a11y_tree/` before execution.

## 15. Pre-registered Expectations

From prior work and parent experiment:
- URL-only PMI on TodoMVC was 0.670-0.751 bits with perfect URL-state mapping
- On URL-ambiguous sites, URL-only PMI should be lower (URL does not distinguish states)
- Accessibility tree should have higher entropy than URL on form-heavy sites (more distinct states)
- If accessibility tree provides >= 0.1 bits gain over URL-only, semantic structure carries dynamical information
- If not, the semantic-structure hypothesis is weakened for the tested sites

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Scope Limitations

This experiment tests accessibility-tree state representation on 2-3 form-heavy SPAs. Results:
- Do NOT generalize to all SPAs or all client-side-routed sites
- Do NOT test other semantic representations (component hierarchy, visual layout, network requests)
- Do NOT test cross-site transfer of accessibility-tree representations
- Do NOT establish that accessibility trees are the optimal state representation — only that they test a different level of description than DOM counts
- Apply only to the tested sites, models, and measurement pipeline

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
