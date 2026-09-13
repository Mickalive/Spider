# EXP-PHYSICS-34719136202 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34719136202
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-12
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-PHYSICS-34695057869 (FALSIFIED-IN-SETTING)
- **Request Reason**: continuation (inherited next_question from parent handoff)

## 2. Scientific Question

Do DOM-based state representation (rendered page structural features: element count, tree depth, interactive density, visible text content, attribute patterns) provide predictive PMI on locally-hosted SPAs where both request-side and response-side network-request signals fail (multistep_form, wizard) or are tautological (dashboard)?

## 3. Motivation

### What the parent experiments established

**Network-request-level representation is exhausted on locally-hosted SPAs:**

- Request-side (endpoint+method+status+body_frag): fails on 2/3 sites (0.0 bits on multistep_form and wizard), tautological on 1/3 (dashboard 0.881 bits but action target equals endpoint path) (EXP-PHYSICS-34674671762, EXP-PHYSICS-34695057869)
- Response-side (SHA-256 body digest + content-type + status): fails on 3/3 sites (dashboard 0.034 bits p=1.0, multistep 0.0 p=1.0, wizard 0.0 p=1.0) (EXP-PHYSICS-34695057869)
- URL-only: trivially zero on all 3 SPAs (single-path routing, URL is constant by construction)

**Key lesson from parent audit:**

> "URL is constant by construction (single-path routing), so zero is structural, not empirical"

**Prior DOM result on TodoMVC (EXP-PHYSICS-34524411213):**

- DOM structural features are predictive (React p=0.001, Vue p=0.001) but strictly worse than URL-only: React -0.073 bits, Vue -0.006 bits
- TodoMVC uses hash-routing where URL is informative; locally-hosted SPAs use session tracking where URL is zero
- Therefore DOM may be the only viable non-network state representation on locally-hosted SPAs

**Why this experiment is different:**

The parent experiments tested network-request-level representations (request-side and response-side). This experiment tests a materially orthogonal level of description: rendered-page representation via DOM structural features.

On locally-hosted SPAs where URL is trivially zero and network signals fail, DOM is the last remaining candidate for non-network state representation within the Physics lane's current infrastructure. DOM features capture the visual/structural state of the SPA including elements that may not appear in network traffic (dynamic DOM manipulation, client-side rendering state, hidden form fields, validation messages, step indicators).

On multistep_form and wizard specifically: the server-rendered HTML changes between steps (different form fields, validation messages, step indicators visible in DOM) even though network requests are invariant (same POST endpoints). DOM may encode the state variation that network signals miss.

### carry_forward from parent handoff

**Established:**
- URL-only PMI strongly positive on TodoMVC hash-SPA transitions (React 0.670, Vue 0.751)
- DOM features on TodoMVC hash-SPAs significantly predictive but worse than URL-only
- PMI pipeline validated across multiple experiments
- Request-side tautological on dashboard, 0.0 on multistep/wizard
- Response-side 0.0 on all 3 sites
- Null control on real SPA passes (p~0.57)
- Synthetic positive control detects structure (p=0.001) but magnitude below 0.5 due to HTTP 204 empty responses

**Rejected:**
- Response-side signals (SHA-256 body digest) as predictive on locally-hosted SPAs
- SHA-256 hash aggregation as effective discretization (collapses variation into sparse bins)
- Client-side request signatures as general predictive representation

**Unknown:**
- Whether DOM-based state representation provides predictive PMI on locally-hosted SPAs
- Whether combined request+response network state provides predictive PMI (not tested)
- Whether finer-grained response representations reveal predictive PMI
- Whether the deterministic server logic on these SPAs fundamentally precludes any representation from achieving predictive PMI

**Do Not Assume:**
- That response-side falsification generalizes to production SPAs
- That URL-only zero means URL is uninformative (it is structural, not empirical)
- That the parent DOM-on-TodoMVC result (DOM worse than URL-only) applies to locally-hosted SPAs
- That the deterministic server logic precludes all representations (may be representation-specific)

## 4. Hypotheses

### H1: DOM Predictive Advantage
DOM-feature PMI exceeds URL-only PMI by >= 0.1 bits on >= 2/3 of locally-hosted SPAs (dashboard, multistep_form, wizard). On multistep_form and wizard where network signals are 0.0 bits, DOM may be the only representation that achieves positive PMI.

### H2: Positive Control
At the synthetic SPA with deterministic DOM evolution, DOM-feature PMI >= 0.5 bits with permutation p < 0.001. This verifies DOM feature extraction and PMI computation pipeline work correctly.

### H3: Null Control
On real SPA data with shuffled action labels, DOM-feature PMI is not significantly > 0 (permutation p > 0.01 after Bonferroni correction). This verifies pipeline does not detect structure when absent.

### H4: Tautology Check
On dashboard, MI between action label and DOM state is computed. If MI is large relative to DOM-feature PMI, the gain is tautological (action->DOM causality) rather than orthogonal environmental dynamics. A non-tautological result requires DOM-feature PMI to be a substantial fraction of MI(action; DOM).

## 5. Data Collection

### 5.1 Sites

Same 3 locally-hosted SPAs as parent experiments:
- **dashboard** (port 3849): Tabbed dashboard with 4 tabs, each triggering different API calls. Same URL (/dashboard), different rendered content per tab.
- **multistep_form** (port 3848): 4-step checkout flow. Same URL (/checkout), different form fields per step. Network requests are invariant (same POST endpoints).
- **wizard** (port 3850): 4-step wizard. Same URL (/wizard), different form content per step. Network requests are invariant.

### 5.2 Trajectories

- 25 trajectories per site (same as parent)
- 8 steps per trajectory (same as parent)
- Each trajectory: fresh session cookie, navigate to entry URL, perform 8 random actions
- Actions: click random interactive element (button, link, input, select)
- Polite delay: 300ms between actions
- State capture delay: 500ms after action + waitUntil: 'networkidle' (with 2s timeout)

### 5.3 DOM Feature Extraction

At each transition point (after action execution and page stabilization), extract via Playwright `page.evaluate()`:

```javascript
{
  element_count: document.querySelectorAll('*').length,
  tree_depth: computeMaxDepth(document.body),
  interactive_density: interactiveElements.length / totalElements,
  form_count: document.querySelectorAll('form').length,
  input_count: document.querySelectorAll('input, select, textarea').length,
  button_count: document.querySelectorAll('button, [role="button"]').length,
  visible_text_hash: SHA-256(document.body.innerText.trim().substring(0, 2000)),
  attribute_pattern_hash: SHA-256(sorted attribute names from interactive elements)
}
```

Where `computeMaxDepth` computes maximum DOM tree depth from body.

### 5.4 State Discretization

- Numeric features (element_count, tree_depth, interactive_density, form_count, input_count, button_count): discretized into 5 quantile bins with edges fit on TRAIN only
- Text/attribute hashes: treated as categorical (exact hash match)
- Combined state: tuple of all discretized features

### 5.5 Synthetic Positive Control

8 states, 4 actions. Each (state, action) pair triggers a distinct DOM update:
- Element addition/removal (state-specific element counts)
- Text content changes (state-specific visible text)
- Attribute modifications (state-specific data attributes)
- The synthetic SPA serves HTML with state-specific DOM structure

### 5.6 Sample Size

- ~560 transitions total: synthetic 250, dashboard ~160, multistep ~120, wizard ~32+
- 80/20 temporal split: first 80% train, last 20% test
- Require n_test >= 30 per site

## 6. Measures

### 6.1 Primary Metric
- **dom_pmi**: DOM-feature PMI at each site (action-conditioned PMI using DOM-based state representation)
- **dom_vs_url_bits**: dom_pmi - url_pmi at each site (improvement over URL-only baseline)

### 6.2 Secondary Metrics
- Per-feature PMI contribution (element_count, tree_depth, etc.)
- Number of unique DOM-based states vs URL-only states
- Alpha sensitivity analysis (alpha = 0, 0.5, 1.0, 2.0)
- Entropy reduction for DOM features vs URL-only
- Tautology check: MI(action_label; DOM_state) and fraction_tautological = MI(action; DOM) / dom_pmi

### 6.3 Comparison Metrics
- Request-side PMI from parent (EXP-PHYSICS-34674671762)
- Response-side PMI from parent (EXP-PHYSICS-34695057869)
- URL-only PMI (trivial zero)

## 7. Null Models

### 7.1 Permutation Null
Shuffle action labels across transitions preserving trajectory structure. Repeated 1000 times per site.

### 7.2 Frequency Null
Marginal next-state distribution P(S_{t+1}). Expected accuracy 1/|S|.

## 8. Statistical Tests

### 8.1 Primary Test
For each site: DOM-feature PMI > URL-only PMI by >= 0.1 bits with permutation p < 0.0167 (Bonferroni-corrected for 3 comparisons, alpha = 0.05/3).

### 8.2 Permutation Tests
- At each site: permutation test for DOM-feature PMI > 0 (1000 permutations)
- Permutation p corrected for 3 comparisons

### 8.3 Tautology Check
Compute MI(action_label; DOM_state) using empirical joint distribution. Compare to DOM-feature PMI. If MI >> PMI, gain is tautological.

## 9. Controls

### 9.1 Positive Control (Synthetic SPA)
DOM-feature PMI >= 0.5 bits with permutation p < 0.001. Verifies DOM feature extraction and PMI pipeline.

### 9.2 Null Control (Shuffled Real SPA Labels)
DOM-feature PMI not significantly > 0 (permutation p > 0.01 after Bonferroni correction). Verifies no false-positive pipeline bias.

### 9.3 Data Sufficiency
n_test >= 30 on held-out test per site.

## 10. Validity Threats

### 10.1 Server-Rendered DOM Variation
The locally-hosted SPAs are Express servers that render HTML. DOM variation between steps depends on how much the server-side template changes. If the template is minimal (e.g., only a hidden session field changes), DOM features may not capture step-specific variation. **Mitigation**: the servers are designed to have step-specific content (different form fields, validation messages, step indicators). The positive control verifies DOM capture works.

### 10.2 Discretization Loss
Quantile binning into 5 bins may lose information or create artificial boundaries. **Mitigation**: alpha sensitivity analysis at multiple smoothing levels; text/attribute hashes treated as categorical to preserve exact matches.

### 10.3 Action->DOM Tautology
Actions (clicks, form inputs) directly modify DOM, creating tautological MI between action and DOM state. **Mitigation**: explicit tautology check comparing MI(action; DOM) to DOM-feature PMI. A non-tautological result requires DOM-feature PMI to reflect predictive structure for next-state transitions, not just current-action confirmation.

### 10.4 Playwright DOM Capture Fidelity
page.evaluate() after action execution may capture DOM before server-side rendering completes (SSR). **Mitigation**: waitUntil: 'networkidle' with 500ms additional delay. If DOM is captured pre-render, features will be invariant across steps (degraded to URL-only equivalent), yielding negative result rather than false positive.

### 10.5 Locally-Hosted Not Production
Same 3 Express servers on localhost:3848-3850. Claims bounded to locally-hosted simulation, not production SPAs. **Mitigation**: explicit disclosure (same as parent experiments).

### 10.6 Sample Size at Wizard
Wizard may yield fewer transitions due to 4-step flow. If n_test < 30, wizard excluded from primary analysis. **Mitigation**: 25 trajectories x 8 steps should yield ~32+ within-URL transitions on wizard (same as parent).

### 10.7 Deterministic Server Logic
These SPAs have deterministic server logic (next state depends only on current step + action). This may fundamentally preclude predictive PMI since the state machine is fully determined by action history. **Mitigation**: this is a genuine empirical question — if DOM features cannot achieve PMI even when they visually encode step-specific content, it suggests representation-specific rather than fundamental limitation.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. DOM-feature PMI > URL-only PMI by >= 0.1 bits on >= 2/3 sites (Bonferroni-corrected permutation p < 0.0167)
2. Positive control passes (synthetic DOM-feature PMI >= 0.5 bits, permutation p < 0.001)
3. Null control passes (shuffled real-SPA labels permutation p > 0.01)
4. Data sufficiency met (n_test >= 30 per site)
5. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Primary condition fails on >= 2/3 sites (DOM-feature PMI < 0.1 bits over URL-only)
2. Permutation p >= 0.0167 on >= 2/3 sites
3. Positive control fails (synthetic DOM-feature PMI < 0.5 bits)
4. Null control fails (shuffled labels permutation p <= 0.01)

### 11.3 MEASUREMENT_INVALID
If:
1. Positive or null control fails
2. Data sufficiency fails (n_test < 30 on >= 2/3 sites)
3. Pipeline errors prevent computation
4. DOM capture yields zero feature variation across all steps (Playwright capture failure)

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates that rendered-page structural features provide predictive state information on locally-hosted SPAs where network signals fail
- On multistep_form/wizard specifically: DOM encodes step-specific state that network requests miss (form fields, validation messages, step indicators)
- Justifies integrating DOM-based state into SPIDER's observation layer
- Supports C-WEB-DYNAMICS: Web transformations contain predictive structure at the rendered-page structural level
- Product should use DOM-feature hashing as complementary state representation, especially on session-tracked SPAs

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- DOM features do not improve PMI over URL-only on these SPAs
- Suggests either (a) DOM variation is too minimal on these simple SPAs, (b) feature extraction is too coarse, or (c) deterministic server logic precludes representation-specific PMI
- Does NOT falsify C-WEB-DYNAMICS entirely — only this specific representation on these specific sites
- Physics lane should investigate: combined representations (DOM + timing), more expressive DOM features (accessibility tree, visual layout), or production SPAs with richer rendering

### 12.3 Tautological Positive (Mixed)
- DOM-feature PMI > URL-only but MI(action; DOM) >> DOM-feature PMI
- Gain is driven by action->DOM causality, not orthogonal environmental dynamics
- Not a valid positive for C-WEB-DYNAMICS; would require orthogonal dynamics

### 12.4 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Data Collection**: Start 3 SPA servers, capture DOM features at each transition via Playwright
2. **Feature Extraction**: Compute DOM feature vectors from page.evaluate() output
3. **Discretization**: Quantile binning (5 bins) on train only; text/attribute hashes as categorical
4. **PMI Computation**: Action-conditioned PMI using DOM-based state, URL-only state, and frequency baseline
5. **Permutation Tests**: 1000 permutations per site with trajectory preservation
6. **Alpha Sensitivity**: PMI at alpha = 0, 0.5, 1.0, 2.0
7. **Tautology Check**: MI(action; DOM) vs DOM-feature PMI
8. **Controls**: Verify positive, null, and data sufficiency
9. **Three-way Comparison**: URL-only vs request-side (parent) vs response-side (parent) vs DOM-feature

## 14. Analysis Code

Analysis will be implemented in:
- Node.js (Playwright) for DOM capture: based on `capture_response_side.js` with added `page.evaluate()` DOM extraction
- Python for PMI computation: based on `pmi_response_side.py` adapted for DOM feature vectors

## 15. Pre-registered Expectations

From prior work:
- Network-request representations fail on these SPAs (established)
- DOM features are predictive on TodoMVC but worse than URL-only (TodoMVC has informative URL)
- On locally-hosted SPAs where URL is zero, DOM may be the only viable representation
- If DOM features achieve PMI > 0 on multistep_form/wizard (where network signals are 0.0), this would be the first non-trivial state representation on these sites
- If DOM features also fail, it constrains the state representation hypothesis and suggests fundamental limitation of these simple SPAs

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
