# EXP-PHYSICS-34764605162 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34764605162
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Parent**: EXP-PHYSICS-34724244876 (FALSIFIED-IN-SETTING on deterministic SPAs)
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

On locally-hosted Express SPAs with controlled non-deterministic server responses, do DOM structural features encode predictive state variation that persists even with K>=3 sufficient action history?

Specifically:
1. Does conditional PMI I(S_next; DOM | URL, ActionHistory_K=3) exceed zero with Bonferroni-corrected permutation p < 0.0167 on non-deterministic SPAs?
2. Does the non-determinism level (deterministic vs random-API vs timing-dependent) modulate the PMI pattern?
3. Does a richer DOM representation (accessibility tree hash, multi-feature hash) capture variation invisible to visible_text_hash?

## 3. Motivation

### 3.1 Parent Experiment Findings

EXP-PHYSICS-34724244876 established on 3 deterministic Express SPAs (804 transitions):

| Site | K=1 PMI | K=2 PMI | K=3 PMI | K=3 Accuracy |
|------|---------|---------|---------|--------------|
| dashboard | 0.000 | 0.000 | 0.000 | 100% |
| multistep_form | 0.939 | 0.344 | 0.000 | 100% |
| wizard | 0.960 | 0.413 | 0.000 | 100% |

Key finding: DOM visible_text_hash adds conditional PMI only when action-history is truncated (K=1,2) but becomes fully redundant when history is sufficient (K=3). Effect is state-labeling via FSM state, not predictive dynamics beyond memory.

### 3.2 Why Non-Deterministic SPAs Are Materially Different

Deterministic Express SPAs have P(S_next | S_current, Action) = 1.0 — the same action from the same state always produces the same next state. Action-history memory at K=3 reconstructs the FSM state perfectly, making DOM redundant.

Non-deterministic SPAs (random API responses, timing-dependent rendering) break this deterministic mapping:
- The same action can lead to different DOM states depending on server responses
- Random API payloads create DOM variation invisible to action labels
- Timing-dependent rendering creates race conditions that produce different DOM structures
- Action-history memory alone cannot predict which variant will occur

In this setting, action-history memory alone may be insufficient even at K=3, because the same action sequence can produce different outcomes. DOM structural features might encode this non-deterministic variation as predictive state information.

### 3.3 Why Locally-Hosted SPAs (Not Production)

The parent handoff recommended testing "production SPAs with non-deterministic rendering." However:
- Production SPAs require browser automation, anti-bot handling, auth management
- Network variability introduces uncontrolled confounds
- CAPTCHA, rate-limiting, and content changes break reproducibility
- The scientific question is about non-determinism, not about specific production sites

Locally-hosted Express SPAs with controlled non-determinism:
- Isolate the causal variable (non-determinism) without uncontrolled confounds
- Enable exact reproducibility via frozen random seeds
- Allow direct within-experiment comparison (deterministic vs non-deterministic)
- Use the same Express infrastructure as the parent, enabling direct comparison
- Can be crawled 50 times per SPA type with deterministic server-side RNG

### 3.4 Why This Is the Discriminating Test for DOM-Based C-WEB-DYNAMICS

The parent established that DOM hash is tautological with action history at K=3 on deterministic SPAs. The question is whether non-determinism breaks this tautology. This experiment directly tests that by:
- Including a deterministic baseline (Level 0) that should replicate the parent's PMI=0 at K=3
- Including two non-determinism levels (random-API, timing-dependent) that should show PMI>0 at K=3 if non-determinism creates predictive DOM variation
- Using the same analysis pipeline as the parent for direct comparability

## 4. Hypotheses

### H1: Non-Determinism Creates Predictive DOM Variation
On non-deterministic SPAs, conditional PMI I(S_next; DOM | URL, ActionHistory_K=3) > 0 with Bonferroni-corrected permutation p < 0.00208 on >= 2/2 non-deterministic SPA types (at least one DOM representation per type).

### H2: Non-Determinism Level Modulates PMI
The conditional PMI at K=3 increases with non-determinism level: PMI(deterministic) ≤ PMI(random-API) ≤ PMI(timing-dependent). The deterministic baseline should have PMI ≈ 0 (replicating parent).

### H3: Richer Representations Capture More Variation
At least one of {accessibility_tree_hash, multi_feature_hash} achieves higher conditional PMI than visible_text_hash on >= 1/3 non-deterministic SPA types.

### H4: Positive Control
Random DOM labels (SHA-256(random_counter), independent of state and action) yield conditional PMI within 3 standard deviations of 0.0.

### H5: Null Control
Shuffled DOM labels (permuted within action-history strata) yield conditional PMI within 3 standard deviations of 0.0.

### H6: Non-Determinism Confirmation
P(S_next | S_current, Action) accuracy = 1.0 on deterministic SPA (Level 0) and < 1.0 on non-deterministic SPAs (Levels 1, 2), confirming non-determinism was introduced.

## 5. Data Generation

### 5.1 SPA Architecture

All SPAs use Express.js server-side rendering with the same page structure as the parent (dashboard, multistep_form, wizard). The SPA architecture is:
- Single-page Express app with client-side routing
- Server returns HTML with embedded DOM structure
- DOM variations are server-side (not client-side JavaScript)
- Same action vocabulary as parent: click, fill, submit, navigate

### 5.2 Three Non-Determinism Levels

**Level 0: Deterministic (Baseline)**
- Same as parent: deterministic server logic, same action from same state always produces same DOM
- Expected: PMI=0 at K=3 (replicating parent)
- Purpose: within-experiment baseline for direct comparison

**Level 1: Random API Responses**
- Server serves random API payloads from a seeded RNG
- Same action from same state can produce different DOM depending on random payload
- Random seed is fixed (seed=42) for reproducibility, but varies across transitions
- DOM text content varies by inserting random elements (e.g., random notification count, random item list)
- Expected: PMI > 0 at K=3 (non-determinism creates predictive DOM variation)

**Level 2: Timing-Dependent Rendering**
- Server introduces variable response delays (1-50ms) via seeded RNG
- Client renders different DOM elements depending on response timing
- Race conditions between concurrent requests create different DOM structures
- Same action from same state can produce different DOM depending on timing
- Expected: PMI > 0 at K=3 (timing variation creates predictive DOM variation)

### 5.3 Sample Size

For each SPA type:
- 50 trajectories, 10 transitions per trajectory = 500 total transitions
- After filtering (failed loads, incomplete DOM): target >= 300 valid transitions
- 3 SPA types × 300+ = 900+ total transitions

### 5.4 Data Format

Same format as parent (raw_dom_captures.json):
```json
{
  "SPA_TYPE": [
    {
      "trajectory_id": "int",
      "step": "int",
      "url": "string",
      "action": {"type": "string", "target_href": "string"},
      "state_before": {
        "dom_features": {
          "visible_text_hash": "SHA-256 hex",
          "accessibility_tree_hash": "SHA-256 hex",
          "numeric_structural": {
            "element_count": "int",
            "tree_depth": "int",
            "interactive_density": "float",
            "form_count": "int"
          }
        }
      },
      "state_after": {
        "dom_features": { /* same fields */ }
      }
    }
  ]
}
```

### 5.5 Filtering

Exclude transitions where:
- Page failed to load (timeout, server error)
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

For each (SPA_type, representation, K):

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

For each (SPA_type, representation, K):
1. Compute observed PMI
2. Shuffle DOM labels within action-history strata 1000 times
3. Compute permuted PMI for each shuffle
4. p-value = fraction of permuted PMI >= observed PMI
5. Bonferroni correction across all (SPA_type, representation, K) combinations

### 7.3 Action-History Prediction Accuracy

For each (SPA_type, K):
- Fit: most frequent S_next per (url, H_K) stratum
- Predict: on each transition, predict most frequent S_next for its stratum
- Report: accuracy = fraction correct

### 7.4 Determinism Check

Compute P(S_next | S_current, Action):
- For each (S_current, Action) pair, check if all transitions yield the same S_next
- Report: accuracy = fraction of deterministic transitions
- Level 0: expected accuracy = 1.0
- Levels 1, 2: expected accuracy < 1.0

### 7.5 Non-Determinism Modulation

For each K, compare PMI across SPA types:
- PMI(deterministic) vs PMI(random-API) vs PMI(timing-dependent)
- Expected: PMI(deterministic) ≈ 0, PMI(random-API) > 0, PMI(timing-dependent) > 0
- Test: paired comparison within each representation

### 7.6 Primary Metric

conditional_pmi_K3_nonDeterministic = mean conditional PMI at K=3 across non-deterministic SPA types and representations that pass controls.

### 7.7 Secondary Metrics

- PMI by K (K=1,2,3) for each SPA type and representation
- Action-history accuracy by K
- Determinism accuracy per SPA type
- Effect size (Cohen's d) for PMI vs 0
- Number of valid transitions per SPA type
- Strata coverage (fraction of strata with >= 5 transitions)
- PMI difference: PMI(non-deterministic) - PMI(deterministic) at K=3

## 8. Null Models

### 8.1 Shuffle Null (Primary)
Permute DOM labels within action-history strata. Preserves marginal distributions of DOM and action-history while breaking DOM-state correspondence. Expected PMI: 0.0.

### 8.2 Frequency Null
Predict next state from marginal distribution P(S_next). Expected accuracy: 1/n_states.

### 8.3 Action-Only Null
Predict next state from action-history only (no DOM). This is the strong beyond-memory null — if action-history alone achieves high accuracy, DOM cannot add predictive value.

### 8.4 Deterministic Baseline Null
The deterministic SPA (Level 0) serves as a within-experiment null: PMI should be ≈ 0 at K=3, replicating the parent's finding.

## 9. Statistical Tests

### 9.1 Primary Test
- Permutation test for conditional PMI > 0
- One-sided: PMI > 0
- 1000 permutations per (SPA_type, representation, K)
- Bonferroni correction across all combinations (n_spa_types * n_representations * n_K_values)
- n_spa_types = 2 (non-deterministic types only, for primary test)
- n_representations = 4
- n_K_values = 3 (K=1,2,3)
- Total comparisons = 2 × 4 × 3 = 24
- Significance threshold: corrected p < 0.05/24 ≈ 0.00208

### 9.2 Effect Size
- Cohen's d for observed PMI vs permuted distribution mean
- Report for each (SPA_type, representation, K)

### 9.3 Multi-Site Consistency
- Fraction of non-deterministic SPA types where PMI > 0 and significant
- Decision requires >= 2/3 types surviving (i.e., 2/2 non-deterministic types)

### 9.4 Non-Determinism Modulation Test
- Compare PMI at K=3 across SPA types using paired wilcoxon test (non-parametric)
- Report effect size and p-value for each pair

## 10. Controls

### 10.1 Positive Control (Random Labels)
Generate random DOM labels as SHA-256(random_counter) where counter increments with a random integer per transition, independent of state and action. Compute conditional PMI. Expected: approximately 0.0 (within noise). Pass criterion: |PMI| < 3 * std(permuted PMI).

This tests the pipeline's ability to detect independence (which the parent's positive control failed to do).

### 10.2 Null Control (Shuffled Labels)
Shuffle DOM labels within action-history strata (1000 shuffles). Expected: mean shuffled PMI approximately 0.0. Pass criterion: |mean shuffled PMI| < 3 * std(shuffled PMI).

### 10.3 Determinism Control
- Level 0 (deterministic): P(S_next | S_current, Action) accuracy = 1.0
- Levels 1, 2 (non-deterministic): accuracy < 1.0
- If Level 0 accuracy < 1.0: infrastructure failure, MEASUREMENT_INVALID
- If Levels 1, 2 accuracy = 1.0: non-determinism not introduced, interpret under parent's setting

### 10.4 Data Quality Control
Each SPA type must have >= 300 valid transitions after filtering. If a type has < 300, it is excluded from the primary analysis but reported.

### 10.5 Deterministic Baseline Control
The deterministic SPA (Level 0) must show PMI ≈ 0 at K=3 (replicating parent). If Level 0 shows PMI > 0 at K=3: pipeline confound, MEASUREMENT_INVALID.

## 11. Validity Threats

### 11.1 Synthetic-to-Real Gap
Locally-hosted Express SPAs may not reflect real production SPAs with React/Vue virtual DOM, auth-dependent content, or external data feeds.
- Mitigation: this is a controlled experiment isolating the causal variable (non-determinism). If the pipeline cannot detect non-determinism-induced DOM variation in a controlled setting, it cannot be trusted on noisier production data.

### 11.2 DOM Representation Loss
Hash-based representations collapse continuous DOM variation. The same visible text with different formatting produces the same hash.
- Mitigation: test multiple representations including accessibility tree and numeric structural features.

### 11.3 Server-Side Non-Determinism vs Client-Side
Server-side random payloads may produce different DOM variation patterns than client-side virtual DOM diffing.
- Mitigation: server-side non-determinism is the controlled variable. Client-side rendering effects (React virtual DOM) would add additional variation, making this a conservative test.

### 11.4 Action Vocabulary Limitation
Limited action types (click, fill, submit, navigate) may not capture all Web interaction patterns.
- Mitigation: same action vocabulary as parent, enabling direct comparison. Generalization to broader action types is outside scope.

### 11.5 Multiple Comparisons
Testing n_spa_types × n_representations × n_K_values combinations inflates false positive risk.
- Mitigation: Bonferroni correction (conservative), report both corrected and uncorrected p-values.

### 11.6 Strata Sparsity
Large state spaces (non-deterministic SPAs produce more unique DOM states) lead to more sparse strata.
- Mitigation: MIN_STRATUM_COUNT=5 (same as parent), report effective N per stratum.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Conditional PMI I(S_next; DOM | URL, ActionHistory_K=3) > 0.0 with Bonferroni-corrected permutation p < 0.00208 on >= 2/2 non-deterministic SPA types (at least one DOM representation per type)
2. Positive control passes (|random-label PMI| < 3 * std(permuted))
3. Null control passes (|shuffled-label PMI| < 3 * std(shuffled))
4. Determinism check: Level 0 accuracy = 1.0, Levels 1,2 accuracy < 1.0
5. Deterministic baseline: Level 0 PMI at K=3 ≈ 0.0 (within noise)
6. >= 300 valid transitions per surviving SPA type

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. Conditional PMI <= 0.0 or non-significant (Bonferroni p >= 0.00208) on ALL non-deterministic SPA types AND ALL representations
2. Positive control fails (|random-label PMI| >= 3 * std(permuted))
3. Null control fails (|shuffled-label PMI| >= 3 * std(shuffled))
4. Deterministic baseline (Level 0) PMI at K=3 > 0.0 and significant (pipeline confound)
5. Non-deterministic SPAs have accuracy = 1.0 (non-determinism not introduced)

### 12.3 MEASUREMENT_INVALID
If:
1. < 300 valid transitions per SPA type after filtering
2. Pipeline errors prevent PMI computation
3. Level 0 accuracy < 1.0 (deterministic SPA is not actually deterministic)
4. All SPA types excluded due to data quality

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- Non-deterministic server responses create genuine environmental dynamics where DOM encodes predictive state variation beyond action-history memory
- DOM integration into SPIDER's observation layer is warranted for SPAs with non-deterministic rendering
- The non-determinism level modulates the benefit: more non-deterministic → more DOM value
- C-WEB-DYNAMICS survives at the non-deterministic SPA level
- Physics lane should investigate what specific DOM features are most predictive and whether the effect is robust across non-determinism types

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- DOM hash-based state labeling is not predictive dynamics even when non-determinism is introduced
- The DOM integration path for C-WEB-DYNAMICS is closed across ALL tested settings (deterministic + non-deterministic)
- SPIDER should focus on action-history-based state tracking and other representations (network responses, API payloads, visual structure)
- Physics lane should try orthogonal approaches (information-theoretic on network data, causal, multi-scale)

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- The non-determinism infrastructure needs improvement before this question can be answered
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Data Generation**: Build 3 Express SPAs (deterministic, random-API, timing-dependent), crawl 50 trajectories each, collect 500 transitions each
2. **Data Filtering**: Exclude failed loads, incomplete DOM captures
3. **DOM Representation**: Compute 4 representations per transition (visible_text_hash, accessibility_tree_hash, numeric_structural, multi_feature_hash)
4. **Action History**: Construct H_K for K=1,2,3 from trajectory step ordering
5. **Strata**: Group by (url, H_K), apply MIN_STRATUM_COUNT=5
6. **Conditional PMI**: Compute for each (SPA_type, representation, K)
7. **Permutation Test**: 1000 shuffles per (SPA_type, representation, K), Bonferroni correction
8. **Controls**: Positive (random labels), null (shuffled labels), determinism check, deterministic baseline
9. **Non-Determinism Modulation**: Compare PMI across SPA types at K=3
10. **Decision**: Apply frozen decision rule
11. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `hashlib` for SHA-256 hashing of DOM representations
- `numpy` for array operations
- `collections.Counter` for empirical distributions
- `scipy.stats` for effect sizes and Wilcoxon test
- Standard library only for PMI computation (no custom estimators required)

Code will be committed to `research/experiments/EXP-PHYSICS-34764605162/` before execution.

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
