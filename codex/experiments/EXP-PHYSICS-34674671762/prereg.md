# EXP-PHYSICS-34674671762 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34674671762
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-12
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Do network requests and API calls (XHR/fetch payloads, endpoint sequences, response content-types) captured via Playwright route interception on genuine client-side-routed SPAs provide predictive state information beyond URL — specifically, does the network-request signature on within-URL transitions carry PMI exceeding URL-only by >= 0.1 bits on sites where URL is ambiguous?

## 3. Motivation

Prior Physics work established:
- URL-only PMI is strongly positive on TodoMVC hash-SPA transitions: React 0.670 bits, Vue 0.751 bits (EXP-PHYSICS-34524411213)
- DOM structural features (element_count, tree_depth, interactive_density) are significantly predictive but strictly worse than URL-only on TodoMVC: React -0.073 bits, Vue -0.006 bits (EXP-PHYSICS-34524411213)
- Accessibility-tree hashes showed strong synthetic PMI (0.972 bits) but real-site Playwright automation failed; the hypothesis remains UNTESTED on genuine SPAs (EXP-PHYSICS-34629310987 MEASUREMENT_INVALID)

The parent handoff (EXP-PHYSICS-34629310987) recommended testing network-request signals as a **materially orthogonal level of description**: communication structure (what endpoints the SPA calls, what data it sends/receives) rather than page structure (DOM counts, element roles).

Network requests are independently observable via Playwright `page.route()` interception without needing accessibility snapshot extraction. This addresses the Playwright timing issues that blocked the accessibility-tree experiment.

On client-side-routed SPAs, the same URL may trigger different API calls at different form steps (e.g., `/checkout` with shipping vs payment step calls different endpoints). This is the hypothesized source of within-URL predictive structure.

## 4. Hypotheses

### H1: Network-Request PMI Exceeds URL-Only
On genuine client-side-routed SPAs with verified URL ambiguity, network-request PMI exceeds URL-only PMI by >= 0.1 bits on within-URL transitions on >= 2/3 tested sites.

### H2: Positive Control
On a synthetic SPA with deterministic network-request evolution (8 states, 4 actions, each (state, action) triggers distinct endpoint+method+status), network-request PMI >= 0.5 bits with permutation p < 0.001.

### H3: Null Control
On shuffled network-request labels (action labels permuted across transitions), network-request PMI does not significantly exceed 0 (permutation p > 0.01).

### H4: Data Sufficiency
>=30 non-leakage within-URL transitions per site after 80/20 temporal split.

## 5. Site Selection

### 5.1 Selection Criteria
Select 2-3 genuine client-side-routed production SPAs that satisfy:
1. **Client-side routing**: URL changes without full page reload (history.pushState or hash routing)
2. **Verified URL ambiguity**: Manual inspection confirms same URL hosts different states at different form steps (e.g., `/checkout` with shipping vs payment, `/survey` with question 1 vs question 5, `/dashboard` with different tabs)
3. **Network-request variation**: Different states at same URL trigger different API calls (different endpoints, methods, payloads, or response content-types)
4. **Accessibility**: Publicly accessible without login, or with pre-authenticated session
5. **Form-heavy**: Multi-step forms, wizards, or tabbed interfaces where same URL hosts multiple states

### 5.2 Candidate Sites (to be validated during execution)
- Multi-step checkout flows (e.g., shipping → payment → confirmation on same `/checkout` URL)
- Survey/form builders (e.g., multi-page forms on same URL)
- Dashboard apps with tab navigation (same URL, different data loaded)

### 5.3 Excluded Sites
- TodoMVC (degenerate demo app, results from EXP-PHYSICS-34524411213 already available)
- Server-side rendered sites (no client-side routing)
- Sites requiring login without pre-authenticated session

## 6. Data Collection

### 6.1 Network-Request Capture
Use Playwright `page.route('**/*', route => {...})` to intercept all network requests at each navigation/interaction step. For each request, record:
- `endpoint_url`: The requested URL (path + query, without fragment)
- `http_method`: GET, POST, PUT, DELETE, etc.
- `status_code`: HTTP response status
- `content_type`: Response Content-Type header (if available)
- `timestamp`: Request timestamp for temporal ordering

### 6.2 State Discretization
Discretize network-request state as:
1. Per-request hash: `SHA-256(endpoint_url + http_method + status_code)`
2. Per-transition state: Sorted tuple of per-request hashes for all requests triggered by a single user action
3. State representation: The sorted tuple hash (deterministic, order-invariant)

### 6.3 Transition Recording
For each user interaction (button click, form submission, navigation):
1. Record pre-interaction URL
2. Execute interaction
3. Record post-interaction URL
4. Record all network requests triggered by the interaction
5. Classify transition as within-URL (pre_url == post_url) or cross-URL (pre_url != post_url)

### 6.4 SPA-Aware Leakage Classification
Use corrected hash-based URL change detection (not action-label based):
- **Non-leakage**: URL changes without corresponding network-request variation (navigation without state change)
- **Within-URL**: URL constant, network-request state varies (the target signal)
- **Cross-URL leakage**: URL changes AND network-request state changes (excluded from within-URL analysis)

## 7. Analysis Plan

### 7.1 Train/Test Split
- Temporal split: first 80% of transitions as TRAIN, last 20% as TEST
- Fit discretization bins on TRAIN only
- Evaluate PMI on TEST only
- This avoids within-trajectory correlation leakage

### 7.2 PMI Computation
Compute Pointwise Mutual Information:
```
PMI(s, a) = log2(P(s_next | s, a) / P(s_next))
```
where:
- `s` = network-request state (or URL-only state)
- `a` = user action
- `s_next` = next network-request state (or next URL)
- Laplace smoothing alpha=1.0

Aggregate PMI across all (state, action) pairs weighted by frequency.

### 7.3 Statistical Testing
- Permutation test: 1000 permutations of action labels within trajectories
- Bonferroni correction for 2-3 sites (alpha = 0.05 / 3 = 0.0167)
- One-sided test: network-request PMI > URL-only PMI

### 7.4 Alpha Sensitivity Analysis
Compute PMI at alpha = 0.0, 0.5, 1.0, 2.0 to verify robustness to smoothing parameter.

## 8. Controls

### 8.1 Positive Control (Synthetic SPA)
- 8 states, 4 actions, deterministic network-request evolution
- Each (state, action) triggers distinct endpoint+method+status
- Network-request PMI must be >= 0.5 bits with permutation p < 0.001
- This verifies the PMI computation pipeline correctly detects network-request structure

### 8.2 Null Control (Shuffled Labels)
- Real SPA data with action labels permuted across transitions
- Network-request PMI must not significantly exceed 0 (permutation p > 0.01)
- This verifies the pipeline does not detect structure when absent

### 8.3 URL-Only Baseline
- URL path as state representation
- Established from EXP-PHYSICS-34524411213: React 0.670 bits, Vue 0.751 bits on TodoMVC
- Re-computed on each new site for comparison

## 9. Decision Rules

### 9.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Network-request PMI exceeds URL-only PMI by >= 0.1 bits on >= 2/3 tested sites
2. Positive control passes (synthetic SPA network-request PMI >= 0.5, permutation p < 0.001)
3. Null control passes (shuffled permutation p > 0.01)
4. Data sufficiency met (>=30 non-leakage transitions per site)
5. Permutation p < 0.01 after Bonferroni correction on >= 2/3 sites

### 9.2 FALSIFIED-IN-SETTING
If ANY of:
1. Network-request PMI does NOT exceed URL-only PMI by >= 0.1 bits on >= 2/3 sites (primary condition fails)
2. Permutation p >= 0.01 after Bonferroni correction on >= 2/3 sites

### 9.3 MEASUREMENT_INVALID
If:
1. Positive control fails
2. Null control fails
3. Data sufficiency fails (<30 transitions per site)
4. Playwright automation fails on all sites
5. Pipeline errors prevent computation

## 10. Validity Threats

### 10.1 Site Selection Bias
Selected sites may have unusually strong or weak network-request variation. Mitigation: select 2-3 sites with verified URL ambiguity through manual inspection.

### 10.2 Network-Request Coarseness
SHA-256(endpoint+method+status) may be too coarse to capture state variation. Mitigation: this is the minimal representation; if it fails, more expressive representations (payload hashes, content-type sequences) may be tested in future work.

### 10.3 Temporal Split Limitations
80/20 temporal split may not fully decorrelate within-trajectory transitions. Mitigation: report sensitivity to split ratio (70/30, 80/20, 90/10).

### 10.4 Playwright Automation
Route interception may miss some requests (e.g., Service Worker requests, cached responses). Mitigation: log all intercepted requests and report coverage.

### 10.5 Synthetic-to-Real Gap
Positive control uses synthetic data. If it passes but real-site results fail, this is evidence against the hypothesis, not a pipeline failure.

## 11. Expected Outcomes

### 11.1 Positive Result (SURVIVES_CURRENT_TEST)
- Demonstrates that network-request signatures capture predictive dynamical structure beyond URL on genuine SPAs
- Network-request interception is more reliable than accessibility snapshot extraction (no Playwright timing issues)
- Product architecture could use network-request signatures as a complementary state representation
- Physics lane should investigate network-request-aware dynamics on larger site collections

### 11.2 Negative Result (FALSIFIED-IN-SETTING)
- Suggests that network-request structure is redundant with URL on tested sites, or too coarse to capture state variation
- Does NOT falsify C-WEB-DYNAMICS entirely — only this specific representation
- Physics lane should investigate other mechanisms or accept URL-only dynamics for simple SPAs

### 11.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 12. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 13. Parent Handoff Constraints

This experiment inherits from EXP-PHYSICS-34629310987 (MEASUREMENT_INVALID). Key constraints:
- **established**: URL-only PMI is strongly positive on TodoMVC (React 0.670, Vue 0.751 bits)
- **rejected**: DOM structural features on TodoMVC; synthetic-only evidence for C-WEB-DYNAMICS
- **unknown**: Whether network-request signatures on genuine SPAs provide predictive information
- **do_not_assume**: That synthetic results translate to real sites; that TodoMVC generalizes to production

This experiment tests a materially orthogonal mechanism (communication structure) rather than repeating failed page-structure representations. It uses Playwright route interception (more reliable than accessibility snapshot extraction) on genuine sites with verified URL ambiguity.
