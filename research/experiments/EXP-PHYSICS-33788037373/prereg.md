# EXP-PHYSICS-33788037373 Preregistration

## Status: DESIGN — NOT YET FROZEN

---

## 1. Hypothesis

After correcting three methodology defects identified in EXP-PHYSICS-33528829431 (in-sample evaluation, invalid bootstrap, non-discriminating positive control), does the measurement substrate reveal genuine action-conditioned transition structure on live Web pages with navigational density?

### 1.1 Sub-hypotheses

**H1: Memorization Artifact**
The previous 100% live-test action-conditioned accuracy was an artifact of in-sample evaluation. Corrected held-out accuracy will be substantially lower than in-sample accuracy on the same data.

**H2: Positive Control Discrimination**
With overlapping actions across states, the action-conditioned predictor will significantly outperform the action-frequency predictor on held-out data (permutation test p < 0.05), demonstrating that the positive control can detect state-dependent structure.

**H3: Live Action-Conditioned Structure**
On at least one of 2 live test sites with navigational density, the action-conditioned predictor will significantly outperform the shuffle null on held-out data (permutation test p < 0.05 after correction).

---

## 2. State Representation

### 2.1 Design

**S (state)**: A composite representation derived from HTTP fetch + HTML parsing:
- `url`: full page URL (normalized, query string stripped for deduplication)
- `title`: page `<title>` text (lowercased, stripped, max 100 chars; empty string if absent)
- `link_texts`: sorted set of first 30 visible link text contents from `<a>` tags (lowercased, stripped; empty strings excluded)
- `tag_counts`: tuple of 11 integers — counts of h1, h2, h3, form, input, button, select, textarea, nav, main, aside tags
- `form_signals`: tuple of 4 booleans — has_form, has_input, has_select, has_textarea

State key: `SHA256(url + "|" + title + "|" + "|".join(link_texts) + "|" + str(tag_counts) + "|" + str(form_signals))[:16]`

### 2.2 Comparison to Prior

Prior: `State(url, SHA256("tags:{n}|elements:{n}|links:{n}")[:16], SHA256(sorted_links[:20])[:16])`. Lost all fine-grained structure — tag distribution, form presence, link text content.

New: Preserves explicit link texts (semantic action targets), tag distribution (page structure), and form signals (interactive elements). Still no JavaScript, accessibility tree, or visual structure.

### 2.3 Representation Loss

- No JavaScript execution (HTTP fetch only) — SPA pages may appear structurally identical across navigations
- No accessibility tree (ARIA roles, states)
- No visual structure (CSS, layout, images)
- No dynamic form values (auto-fill, session state)
- Link texts may be empty (image links, aria-hidden)
- Tag counts are aggregate, not hierarchical
- Query string stripped from URL — dynamic parameters lost

---

## 3. Action Representation

### 3.1 Design

- `action_type`: one of {click, navigate, type_text}
- `target_text`: visible text of clicked element (from `<a>` text content), lowercased/stripped; empty for navigate
- `target_href`: destination URL for click/navigate; empty for type_text

Action key: `action_type + "|" + target_text + "|" + target_href`

### 3.2 Comparison to Prior

Prior: `Action("click", "link_{idx}", "link_text_{idx}")` — positional index, no semantic content.

New: Preserves visible text and destination URL. Enables analysis of which link texts are predictive.

### 3.3 No-Target-Leakage Guarantee

Action features describe the action target, NOT the next state. `target_href` is the URL the user clicked ON, not the URL they arrived AT (which may differ due to redirects). `target_text` is the visible link text, not the destination page content. The next state is observed AFTER action execution.

---

## 4. Target

Primary: Can we predict S' given (S, A) better than null models on HELD-OUT trajectories?

Secondary: Does corrected evaluation produce different results than prior in-sample methodology?

---

## 5. Sampling Policy

### 5.1 Positive Control (Synthetic)

- 8 states, 3 action types, actions overlap across states
- 60 trajectories × 10 steps = 600 transitions
- Seed: 42
- Deterministic transition table (pre-defined graph)

### 5.2 Null Control (Synthetic)

- 30 states, 5 action types, 8 target_ids shared across states
- Random transitions (next-state independent of action)
- 30 trajectories × 10 steps = 300 transitions
- Seed: 44

### 5.3 Live Test

- **Site 1**: `https://en.wikipedia.org/wiki/Main_Page` — high link density, server-rendered
- **Site 2**: `https://docs.python.org/3/` — medium link density, server-rendered
- 20 trajectories per site, max 10 steps each = up to 400 transitions
- Seeds: 43 (site 1), 45 (site 2)
- HTTP fetch via `urllib.request`, timeout 10s, User-Agent: SPIDER-Physics/2.0
- Polite delay: 0.5s between requests
- Trajectory start: random internal link from homepage

### 5.4 Total Sample

- Positive: 600, Null: 300, Live: up to 400 = up to 1300 total

---

## 6. Unit of Analysis

Each `(trajectory_id, step_index)` is one transition. **Trajectories are the dependency unit.** Train/test splits are at trajectory level.

---

## 7. Holdout

### 7.1 Trajectory-Grouped Split

For each condition:
1. Collect all trajectories
2. Assign 70% to train, 30% to test (random assignment, seed=42 for split)
3. Fit predictors on train trajectories only
4. Evaluate on test trajectories only
5. No trajectory in both train and test

### 7.2 Site-Level Independence (Live)

Each site's trajectories are split independently. No cross-site data sharing.

---

## 8. Nulls/Baselines

### 8.1 Shuffle Null (Primary)

Permute next-state labels within each trajectory. Evaluate action-conditioned predictor on permuted data. Breaks action-conditioning while preserving trajectory-level state distribution.

### 8.2 Action-Frequency Null

For each action type (by `target_text`), predict most common next-state in training, ignoring current state. Tests: does action alone predict next-state?

### 8.3 First-Order Markov Null

Predict next-state from current state only, ignoring action. Tests: does state alone provide same information as (state, action)?

### 8.4 In-Sample Memorization Baseline

Fit and evaluate on SAME transitions (no holdout). Included for direct comparison with prior experiment.

---

## 9. Primary Metrics

### 9.1 Held-Out Accuracy Difference

`diff = accuracy_SA_heldout - accuracy_shuffle_heldout`

per condition (positive, null, live-site-1, live-site-2).

### 9.2 Permutation p-value

One-sided permutation test per condition:
1. Observed diff on held-out data
2. 1000 permutations: permute next-state labels within trajectories
3. For each permutation: recompute diff on same train/test split
4. p = fraction of permuted diffs >= observed diff

### 9.3 Memorization Ratio

`memorization_ratio = accuracy_SA_insample / accuracy_SA_heldout`

Values >> 1 indicate memorization artifact.

---

## 10. Expected Direction

- **Positive control**: diff > 0, p < 0.05
- **Null control**: diff ≈ 0, p > 0.05
- **Live test**: diff > 0, p < 0.05 after correction — OR — diff ≈ 0, p > 0.05
- **Memorization ratio**: >> 1 for all conditions

---

## 11. Uncertainty Method

### 11.1 Permutation Test

- 1000 permutations per condition
- Independent RNG per permutation (fresh `random.Random(seed)` instance)
- Resample unit: trajectory (permute labels within trajectory)
- One-sided: H1: diff > 0

### 11.2 Multiple Comparison Correction

Bonferroni correction for 3 null tests × 2 live sites = 6 comparisons.
Threshold: p_corrected < 0.05.

---

## 12. Adequacy Rule

Substrate is measurement-valid if and only if:
1. Positive control discriminates: action-conditioned > action-frequency, p < 0.05
2. Positive control accuracy > 90% held-out
3. Null control passes: p > 0.05
4. All validity gates pass
5. >= 100 live transitions from >= 2 sites

---

## 13. Falsification/Survival Rule

### SURVIVES_CURRENT_TEST
ALL of:
1. Positive control discriminates (p < 0.05)
2. Positive control accuracy > 90%
3. Null control passes (p > 0.05)
4. >= 1 live site shows action-conditioned structure above shuffle (p < 0.05 after Bonferroni × 6)
5. All validity gates pass
6. >= 100 live transitions from >= 2 sites

### FALSIFIED-IN-SETTING
(1)-(3) pass but (4) fails on all live sites.

### MEASUREMENT_INVALID
Any validity gate fails, or infrastructure prevents data collection, or (1)-(3) fail.

---

## 14. Claim Scope

### Tests:
- C-MEAS-VALID: Can corrected substrate produce measurement-valid results?
- C-WEB-DYNAMICS (preliminary): Action-conditioned structure in live Web transitions at tested representation?

### Does NOT test:
- Cross-site transfer (C-CROSSSITE)
- Universal physical laws
- Attractors, barriers, committors
- Generalization beyond tested sites
- Richer state representations
- Browser-based interaction

---

## 15. Validity Threats

### 15.1 State Representation Coarseness
HTTP fetch cannot execute JS or render dynamic content. SPA pages may appear structurally identical across navigations. **Mitigation:** Select server-rendered sites (Wikipedia, Python docs). Acknowledged.

### 15.2 Action Inference Limitations
Only `<a>` links and `<form>` elements captured. Button clicks, custom elements missed. **Mitigation:** Acknowledged. Focus on link-following transitions.

### 15.3 Sample Size
20 trajectories × 10 steps = 200 per site. Early trajectory termination possible. **Mitigation:** Target dense-navigation sites. Accept partial trajectories.

### 15.4 Multiple Comparisons
6 comparisons, Bonferroni conservative. **Mitigation:** Report raw + corrected p-values. Focus on effect sizes.

### 15.5 Permutation Test Power
~6 held-out trajectories per site. Limited power for small effects. **Mitigation:** Report effect sizes. Large effects (d > 0.8) detectable.

### 15.6 Synthetic-to-Real Gap
Positive control validates pipeline, not Web dynamics. **Mitigation:** Live test provides substantive test.

### 15.7 Infrastructure Constraint
No numpy/scipy/playwright. Stdlib only. **Mitigation:** Permutation test implementable in stdlib. Reproducible with fixed seeds.

---

## 16. Analysis Plan

### Phase 1: Synthetic Validation
1. Generate positive control (8 states, 3 actions, 60×10=600 transitions, seed=42)
2. Generate null control (30 states, 5 actions, 30×10=300 transitions, seed=44)
3. Split 70/30 train/test by trajectory (seed=42)
4. Fit predictors on train, evaluate on test
5. Run permutation test (1000 permutations)
6. Verify: positive discriminates, null passes

### Phase 2: Live Web Collection
7. Fetch Site 1 (Wikipedia): collect trajectories via internal link following
8. Fetch Site 2 (Python docs): collect trajectories via internal link following
9. Record (S, A, S') at each step
10. Verify: >= 100 live transitions from >= 2 sites

### Phase 3: Live Evaluation
11. Split live trajectories 70/30 by trajectory
12. Fit predictors on train, evaluate on test
13. Permutation test (1000 per site)
14. Bonferroni correction (× 6)
15. Compute memorization ratio

### Phase 4: Reporting
16. Report all metrics with equal prominence
17. Report effect sizes alongside p-values
18. Document validity threats and representation losses
19. Determine verdict per decision rule

---

## 17. Analysis Code

Python stdlib only:
- `random.Random(seed)` for RNG
- `math.log2` for entropy
- `collections.Counter` for majority voting
- `urllib.request` for HTTP
- `html.parser.HTMLParser` for parsing
- `json` for serialization
- `hashlib` for state hashing

No numpy, scipy, or external packages.

Code committed to `research/physics/` before execution.

---

## 18. Pre-registered Expectations

From prior work:
- WP-002B: rule-shuffle diff +0.0532 (in-distribution)
- EXP-PHYSICS-33528829431: in-sample 100% (known artifact), entropy -250% (representation artifact)

Expected outcomes:
- Held-out accuracy << 100% on live data (memorization artifact confirmed)
- Positive control: action-conditioned > action-frequency (discrimination succeeds)
- Live test: either diff > 0 (structure exists) or diff ≈ 0 (no structure at this level)
- If diff > 0: magnitude likely small (< 20%) given coarse representation
- If diff ≈ 0: either no Web dynamics or HTTP fetch insufficient — pivot to richer representation

---

## 19. Deviation Policy

Any deviation from this preregistration labeled EXPLORATORY. Confirmatory claims require new preregistration.

---

## 20. Freeze Statement

Frozen BEFORE analysis code written or outcome data inspected. Experiment executed exactly as described.
