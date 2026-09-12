# EXP-PHYSICS-34695057869 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34695057869
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Parent Experiment**: EXP-PHYSICS-34674671762 (FALSIFIED-IN-SETTING: client-side request signatures fail on 2/3 locally-hosted SPAs)
- **Date**: 2026-09-12
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Do response-side signals (response content-type, response body digest, response timing, response status sequences) captured via Playwright route interception on locally-hosted SPAs with state-dependent server responses provide predictive PMI on within-URL transitions where client-side request signatures are identical across states?

## 3. Motivation

### 3.1 Parent Experiment Findings

EXP-PHYSICS-34674671762 tested client-side request signatures (endpoint+method+status+body_frag[:200]) on 3 locally-hosted SPAs:
- **Dashboard**: 0.881 bits PMI (passes primary) — but tautological (action→own-request)
- **Multistep_form**: 0.0 bits PMI (fails primary) — server hides state in session cookies
- **Wizard**: 0.0 bits PMI (fails primary) — server hides state in session cookies

Primary condition fails: only 1/3 sites pass (need >=2/3). Verdict: FALSIFIED-IN-SETTING.

### 3.2 Why Response-Side Signals

The parent experiment revealed a fundamental asymmetry:
- **Client-side request signatures** capture what the agent sends (outgoing communication)
- **Response-side signals** capture what the server sends back (incoming communication)

On session-tracked SPAs, client requests are identical across states (POST /api/checkout/next for all steps), but server responses may differ:
- Response bodies contain step-specific information (step number, step name, validation results)
- Response status codes vary by step (200 vs 201 vs 400)
- Response timing may correlate with step complexity
- Response content-types may vary (application/json vs text/html)

This is a materially orthogonal level of description within the network-request domain. Testing response-side signals can determine whether server-observable communication provides predictive state information that client-observable communication misses.

### 3.3 Fixes for Parent Validity Issues

This experiment addresses 6 audit findings from EXP-PHYSICS-34674671762:

1. **sampling_local_not_production** (high): Same 3 locally-hosted SPAs, but now explicitly labeled as locally-hosted simulation, not production.
2. **wizard_temporal_split_violation** (high): Proper 80/20 temporal split with n_test >= 30 on held-out test set. If wizard has <30 transitions after split, exclude from primary analysis.
3. **tautological_dashboard_gain_identifiability** (high): Response-side PMI on dashboard measures server response variation, not action→own-request causality. If dashboard response-side PMI > 0, it demonstrates genuine server-side state encoding.
4. **multistep_wizard_api_coarseness** (medium): Response-side signals may encode state that request-side misses (step-specific validation results in JSON responses).
5. **null_control_wrong_population** (medium): Null control run on real SPA shuffled labels per spec, not synthetic data.
6. **positive_control_threshold_fragile** (low): Positive control uses synthetic SPA with response-side variation, not request-side variation.

## 4. Hypotheses

### H1: Response-Side Predictive Power
Response-side PMI >= 0.1 bits on >= 2/3 of locally-hosted SPAs where request-side PMI was 0.0 bits (multistep_form, wizard).

### H2: Positive Control
Synthetic SPA with deterministic response-side variation achieves response-side PMI >= 0.5 bits with permutation p < 0.001.

### H3: Null Control
Shuffled action labels on real SPA data produce permutation p > 0.01 after Bonferroni correction.

### H4: Dashboard Non-Tautology
Dashboard response-side PMI measures genuine server response variation, not action→own-request causality. Response bodies differ by tab (different APIs, different data), providing independent predictive information.

## 5. Data Collection

### 5.1 Locally-Hosted SPAs

Reuse existing servers from parent experiment:
- **Dashboard**: `research/physics/network_requests/dashboard_spa_server.js` (port 3849)
- **Multistep_form**: `research/physics/network_requests/multistep_form_server.js` (port 3848)
- **Wizard**: `research/physics/network_requests/wizard_spa_server.js` (port 3850)

### 5.2 Synthetic SPA

Modify `research/physics/network_requests/synthetic_spa_server.js` to return distinct response bodies per (state, action) pair:
- Response body: JSON with state-specific data (e.g., `{state: N, action: "act_X", data: "..."}`)
- Status codes: 200 for most, 201 for certain transitions
- Content-type: application/json for all (controlled)

### 5.3 Capture Script

Create `research/physics/network_requests/capture_response_side.js` based on `capture_all_local_v2.js`:
- Use Playwright route interception to capture both request and response
- For each transition, capture:
  - Request: endpoint_url, http_method, request_body, status_code (as before)
  - Response: status_code, content_type (from response.headers()), response_body_digest (SHA-256 of response.body()[:500]), response_timing (response.timing() if available)
- Filter static assets (CSS, JS, images) as before
- Output format: same structure as `raw_network_captures.json` but with additional response-side fields

### 5.4 Sample Size

- Synthetic: 250 transitions (10 trajectories × 25 steps)
- Dashboard: 160 transitions (10 trajectories × 16 steps)
- Multistep_form: 120 transitions (10 trajectories × 12 steps)
- Wizard: 32+ transitions (10 trajectories × 12 steps, may be limited by Playwright capture)
- Total: ~560 transitions

### 5.5 Temporal Split

80/20 temporal split per SPA:
- Train: first 80% of transitions (by trajectory order)
- Test: last 20% of transitions
- Minimum test size: 30 transitions (if <30, exclude SPA from primary analysis)

## 6. State Representation

### 6.1 Response-Side State Discretization

For each network request in a transition:
1. Extract response headers: content-type, any custom headers
2. Extract response body: first 500 chars, compute SHA-256 digest
3. Extract response status code
4. Compute per-request hash: SHA-256(content_type + response_body_digest[:16] + status)
5. For transition state: sorted tuple of per-request hashes, then SHA-256 to single string

### 6.2 URL-Only Baseline

URL-only state: normalized URL path (no query, no hash). Same as parent experiment.

### 6.3 Request-Side Baseline

Request-side state: SHA-256(endpoint_path + method + status + request_body[:200]) per request, sorted tuple, SHA-256 to single string. Same as parent experiment.

## 7. PMI Computation

### 7.1 PMI Formula

PMI(s, a, s') = log2[ P(s' | s, a) / P(s' | s) ]

With Laplace smoothing alpha = 1.0.

### 7.2 Temporal Split

Fit discretization bins on TRAIN only (80/20 temporal split). Evaluate on held-out TEST.

### 7.3 Permutation Test

Shuffle action labels within trajectories (preserving trajectory structure). 1000 permutations per site.

## 8. Baselines

### 8.1 Response-Side PMI (Primary)
Response-side state discretization as defined in Section 6.1.

### 8.2 Request-Side PMI (Baseline)
Request-side state discretization from parent experiment (Section 6.3).

### 8.3 URL-Only PMI (Baseline)
URL-only state (Section 6.2). Expected: 0 bits (single-path SPAs).

### 8.4 Shuffle Null (Null Control)
Shuffled action labels within trajectories. Expected: permutation p > 0.01.

### 8.5 Frequency Baseline (Optional)
Marginal next-state distribution. Expected accuracy: 1/|S|.

## 9. Controls

### 9.1 Positive Control (Synthetic SPA)
- Synthetic SPA with deterministic response-side variation
- 8 states, 4 actions, each (state, action) triggers distinct response body
- Expected: response-side PMI >= 0.5 bits, permutation p < 0.001
- Verifies: pipeline correctly detects response-side structure when present

### 9.2 Null Control (Real SPA Shuffled Labels)
- Shuffled action labels on real SPA data (dashboard, multistep_form, wizard)
- Expected: permutation p > 0.01 after Bonferroni correction
- Verifies: pipeline does not produce false positives on real SPA data

### 9.3 Dashboard Non-Tautology Check
- Dashboard response-side PMI measures server response variation, not action→own-request causality
- Response bodies differ by tab (different APIs, different data)
- If response-side PMI > 0, it demonstrates genuine server-side state encoding

## 10. Statistical Tests

### 10.1 Primary Test
- Response-side PMI >= 0.1 bits on >= 2/3 of locally-hosted SPAs where request-side PMI was 0.0 bits
- Permutation p < 0.05 after Bonferroni correction (3 comparisons, alpha = 0.0167)

### 10.2 Paired Comparisons
- At each SPA: response-side PMI vs request-side PMI
- Two-sided, alpha = 0.05

### 10.3 Effect Size
- Cohen's d for response-side vs request-side PMI at each SPA

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Response-side PMI >= 0.1 bits on >= 2/3 of SPAs where request-side PMI was 0.0 bits
2. Permutation p < 0.05 after Bonferroni correction
3. Positive control passes (synthetic response-side PMI >= 0.5 bits, p < 0.001)
4. Null control passes (shuffled-label p > 0.01)
5. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Response-side PMI < 0.1 bits on >= 2/3 of SPAs where request-side PMI was 0.0 bits
2. Permutation p > 0.05 after Bonferroni correction
3. Positive control fails
4. Null control fails

### 11.3 MEASUREMENT_INVALID
If:
1. Sample sizes insufficient (<30 test transitions per SPA after temporal split)
2. Pipeline errors prevent computation
3. Response-side data capture fails (Playwright route interception issues)

## 12. Validity Threats

### 12.1 Sample Size
With 30+ test transitions per SPA, power is limited for detecting small effects. Report confidence intervals alongside p-values.

### 12.2 Synthetic-to-Real Gap
Synthetic positive control may not reflect real SPA response patterns. Mitigation: pipeline validation on known structure is necessary before interpreting real SPA results.

### 12.3 Response-Side Capture Limitations
Playwright route interception may not capture all response-side data (e.g., streaming responses, WebSocket messages, Service Worker responses). Mitigation: focus on fetch/XHR responses, document capture limitations.

### 12.4 Response Body Digest Coarseness
SHA-256 of response body[:500] may miss state-relevant information in larger responses. Mitigation: test with different body fragment lengths (200, 500, 1000) in sensitivity analysis.

### 12.5 Temporal Split Violation Risk
If wizard has <30 transitions after 80/20 split, exclude from primary analysis (do not use fallback like parent experiment).

## 13. Analysis Plan

1. **Data Collection**: Capture response-side data from 3 locally-hosted SPAs + synthetic SPA
2. **Temporal Split**: 80/20 split per SPA, exclude SPAs with <30 test transitions
3. **State Discretization**: Compute response-side, request-side, and URL-only state hashes
4. **PMI Computation**: Compute PMI for each state representation on test set
5. **Permutation Test**: 1000 permutations per SPA per state representation
6. **Bonferroni Correction**: Correct for 3 comparisons (alpha = 0.0167)
7. **Effect Size**: Compute Cohen's d for response-side vs request-side
8. **Alpha Sensitivity**: Test PMI at alpha = 0.0, 0.5, 1.0, 2.0
9. **Decision**: Apply frozen decision rules

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
