# EXP-PHYSICS-34695057869 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34695057869
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Parent Experiment**: EXP-PHYSICS-34674671762 (FALSIFIED-IN-SETTING: client-side request signatures fail on 2/3 locally-hosted SPAs; only dashboard passes, and its gain is tautological)
- **Parent Handoff**: research/experiments/EXP-PHYSICS-34674671762/handoff.json (sha256: ca491e4b2ac3c6fb4568d3a631261d9e8c6599841d05b02ec1721bd85deef1b1)
- **Date**: 2026-09-12
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Do response-side signals (response content-type, response body digest, response timing, response status sequences) captured via Playwright route interception on locally-hosted SPAs with state-dependent server responses provide predictive PMI on within-URL transitions where client-side request signatures are identical across states?

## 3. Motivation

### 3.1 Parent Experiment Findings

EXP-PHYSICS-34674671762 tested client-side request signatures (endpoint+method+status+body_frag[:200]) on 3 locally-hosted SPAs:

- **Dashboard**: 0.881 bits PMI (passes primary) — but tautological (action→own-request: action target_href directly equals endpoint path /api/tab/{tab})
- **Multistep_form**: 0.0 bits PMI (fails primary) — server hides state in session cookies, client sends identical POST /api/checkout/next for all steps
- **Wizard**: 0.0 bits PMI (fails primary) — server hides state in session cookies, client sends identical POST /api/wizard/next for all steps

Primary condition fails: only 1/3 sites pass (need >=2/3). Verdict: FALSIFIED-IN-SETTING.

### 3.2 Why Response-Side Signals

The parent experiment revealed a fundamental asymmetry between client-observable and server-observable communication:

- **Client-side request signatures** capture what the agent sends (outgoing communication). On session-tracked SPAs, these are invariant across states.
- **Response-side signals** capture what the server sends back (incoming communication). Server responses may encode state-dependent information that client requests do not.

On the multistep_form SPA, the server returns `{ step: N, stepName: STEPS[N], apis: STEP_API_CALLS[stepName] }` — response bodies vary by step. On the wizard SPA, the server returns `{ step: N, stepName: STEPS[N] }` — response bodies also vary by step. These response bodies contain step-specific information that is absent from the client-side request signatures.

This is a materially orthogonal level of description within the network-request domain: server-observable communication (what comes back) vs client-observable communication (what goes out).

### 3.3 Fixes for Parent Validity Issues

This experiment explicitly addresses audit findings from EXP-PHYSICS-34674671762:

1. **sampling_local_not_production** (high): Same 3 locally-hosted SPAs, now explicitly labeled as locally-hosted simulation, not production. Claim ceiling bounded accordingly.
2. **wizard_temporal_split_violation** (high): Proper 80/20 temporal split with n_test >= 30 on held-out test set. If wizard has <30 transitions after split, exclude from primary analysis. No fallback to full-data evaluation.
3. **tautological_dashboard_gain_identifiability** (high): Response-side PMI on dashboard may also be tautological (action→response causality). Explicit identifiability analysis required: if response body is deterministic function of action label, gain is tautological. Report whether response-side gain is orthogonal to action label.
4. **multistep_wizard_api_coarseness** (medium): Response-side signals may encode state that request-side misses — specifically step-specific validation results and step metadata in JSON responses.
5. **null_control_wrong_population** (medium): Null control run on real SPA shuffled labels per spec, not synthetic data.
6. **positive_control_threshold_fragile** (low): Positive control uses synthetic SPA with response-side variation; PMI computed on proper 80/20 test split (not in-sample).

## 4. Hypotheses

### H1: Response-Side Predictive Power (Primary)

Response-side PMI exceeds URL-only PMI by >= 0.1 bits on >= 2/3 of all tested locally-hosted SPAs (dashboard, multistep_form, wizard). On multistep_form and wizard specifically, where request-side PMI was 0.0 bits, response-side PMI > 0 bits demonstrates that server responses encode predictive state information that client requests miss.

### H2: Positive Control

Synthetic SPA with deterministic response-side variation achieves response-side PMI >= 0.5 bits with permutation p < 0.001 on proper 80/20 temporal split.

### H3: Null Control

Shuffled action labels on real SPA data produce permutation p > 0.01 after Bonferroni correction for 3 comparisons.

### H4: Response-Side vs Request-Side Comparison

On multistep_form and wizard, response-side PMI > request-side PMI (which was 0.0 bits). This directly tests whether server responses provide state information that client requests do not.

### H5: Dashboard Tautology Check

Dashboard response-side PMI may be tautological if response body is deterministic function of action label. Explicit test: compute mutual information between action label and response body digest. If I(action; response_body) > 0.5 bits, the response-side gain is largely action→response causality, not orthogonal environmental dynamics.

## 5. Data Collection

### 5.1 Locally-Hosted SPAs

Reuse existing servers from parent experiment:
- **Dashboard**: `research/physics/network_requests/dashboard_spa_server.js` (port 3849)
  - 4 tabs (overview, analytics, users, settings), all at /dashboard URL
  - Response bodies differ by tab: `{ tab: tabName, apis: TAB_APIS[tab], timestamp }`
- **Multistep_form**: `research/physics/network_requests/multistep_form_server.js` (port 3848)
  - 4 steps (shipping, payment, review, confirmation), all at /checkout URL
  - Response bodies differ by step: `{ step: N, stepName, apis: STEP_API_CALLS[stepName] }`
- **Wizard**: `research/physics/network_requests/wizard_spa_server.js` (port 3850)
  - 4 steps (personal_info, address, payment, review), all at /wizard URL
  - Response bodies differ by step: `{ step: N, stepName, apis: [...endpoints] }`

### 5.2 Synthetic SPA (Positive Control)

Modify `research/physics/network_requests/synthetic_spa_server.js` to return distinct response bodies per (state, action) pair:
- Response body: JSON `{state_id: N, action_label: "act_X", data_hash: "<deterministic_hash>", next_state: M}`
- Status codes: 200 for most transitions, 201 for terminal state transitions
- Content-type: application/json for all (controlled)
- 8 states, 4 actions, each (state, action) triggers a unique response body

### 5.3 Capture Script

Create `research/physics/network_requests/capture_response_side.js` based on `capture_all_local_v2.js`:

Key modification: capture response bodies via Playwright's `page.on('response', ...)` event:
```javascript
page.on('response', async (response) => {
  const url = response.url();
  if (isStaticAsset(url)) return;
  try {
    const body = await response.body();
    const bodyStr = body.toString('utf-8').slice(0, 500);
    const bodyHash = crypto.createHash('sha256').update(bodyStr).digest('hex').slice(0, 16);
    capturedResponses.set(url, {
      status: response.status(),
      contentType: response.headers()['content-type'] || 'unknown',
      bodyHash: bodyHash,
      bodyFragment: bodyStr
    });
  } catch(e) { /* streaming or unavailable */ }
});
```

Output format: same structure as `raw_network_captures.json` but with additional response-side fields per network request:
```json
{
  "endpoint_url": "...",
  "http_method": "POST",
  "status_code": 200,
  "content_type": "application/json",
  "request_body": "",
  "response_body_hash": "abc123...",
  "response_body_fragment": "{\"step\":2,...}",
  "response_timing_ms": 15
}
```

### 5.4 Sample Size

- Synthetic: 250 transitions (10 trajectories × 25 steps)
- Dashboard: 160 transitions (10 trajectories × 16 steps)
- Multistep_form: 120 transitions (10 trajectories × 12 steps)
- Wizard: 32+ transitions (10 trajectories × 12 steps, limited by Playwright capture as in parent)
- Total: ~560 transitions

### 5.5 Temporal Split (Critical Fix)

80/20 temporal split per SPA:
- Train: first 80% of transitions (by trajectory order within each SPA)
- Test: last 20% of transitions
- **Minimum test size: 30 transitions per site**
- If n_test < 30 after split, **exclude SPA from primary analysis** (no fallback to full-data evaluation)
- State discretization bins fit on TRAIN only; evaluation on held-out TEST only

## 6. State Representation

### 6.1 Response-Side State Discretization (Primary)

For each network request in a transition:
1. Extract response headers: content-type (from response.headers()['content-type'])
2. Extract response body: first 500 chars, compute SHA-256 digest (response_body_hash)
3. Extract response status code (from response.status())
4. Compute per-request hash: SHA-256(content_type + response_body_hash[:16] + status_code)
5. For transition state: sorted tuple of per-request response hashes, then SHA-256 to single string

### 6.2 URL-Only Baseline

URL-only state: normalized URL path (no query, no hash). Same as parent experiment. Expected: 0 bits (single-path SPAs).

### 6.3 Request-Side Baseline

Request-side state: SHA-256(endpoint_path + method + status + request_body[:200]) per request, sorted tuple, SHA-256 to single string. Same as parent experiment. Used for direct comparison.

## 7. PMI Computation

### 7.1 PMI Formula

PMI(s, a, s') = log2[ P(s' | s, a) / P(s' | s) ]

With Laplace smoothing alpha = 1.0.

### 7.2 Temporal Split

Fit discretization on TRAIN only (80/20 temporal split). Evaluate on held-out TEST. No fallback when test < 10 (fixes parent wizard_temporal_split_violation).

### 7.3 Permutation Test

Shuffle action labels within trajectories (preserving trajectory structure). 1000 permutations per site per state representation.

### 7.4 Alpha Sensitivity

Compute PMI at alpha = 0.0, 0.5, 1.0, 2.0 to test robustness to Laplace smoothing.

## 8. Baselines

### 8.1 Response-Side PMI (Primary)

Response-side state discretization as defined in Section 6.1.

### 8.2 Request-Side PMI (Baseline)

Request-side state discretization from parent experiment (Section 6.3). Allows direct comparison: does response-side capture state that request-side misses?

### 8.3 URL-Only PMI (Baseline)

URL-only state (Section 6.2). Expected: 0 bits (single-path SPAs).

### 8.4 Shuffle Null (Null Control)

Shuffled action labels within trajectories on real SPA data. Expected: permutation p > 0.01.

### 8.5 Frequency Baseline

Marginal next-state distribution. Expected accuracy: 1/|S|.

## 9. Controls

### 9.1 Positive Control (Synthetic SPA)

- Synthetic SPA with deterministic response-side variation (8 states, 4 actions)
- Each (state, action) triggers distinct response body, status code
- Expected: response-side PMI >= 0.5 bits, permutation p < 0.001
- Evaluated on proper 80/20 temporal split (not in-sample)
- Verifies: pipeline correctly detects response-side structure when present

### 9.2 Null Control (Real SPA Shuffled Labels)

- Shuffled action labels on real SPA data (dashboard, multistep_form, wizard)
- Permutation p > 0.01 after Bonferroni correction for 3 comparisons
- Verifies: pipeline does not produce false positives on real SPA data
- Fixes parent audit finding (null_control_wrong_population)

### 9.3 Dashboard Tautology Check

- Compute I(action_label; response_body_hash) for dashboard transitions
- If I(action; response_body) > 0.5 bits, response-side gain is largely tautological
- Report separately: genuine environmental dynamics vs action→response causality

## 10. Statistical Tests

### 10.1 Primary Test

- Response-side PMI exceeds URL-only PMI by >= 0.1 bits on >= 2/3 of all tested locally-hosted SPAs
- Permutation p < 0.0167 (Bonferroni-corrected for 3 comparisons, alpha = 0.05/3)

### 10.2 Paired Comparisons

- At each SPA: response-side PMI vs request-side PMI
- Two-sided, alpha = 0.05

### 10.3 Effect Size

- Cohen's d for response-side vs request-side PMI at each SPA

### 10.4 Tautology Quantification

- For dashboard: mutual information between action label and response body digest
- Report as fraction of response-side PMI that is attributable to action→response causality

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST

If ALL of:
1. Response-side PMI exceeds URL-only PMI by >= 0.1 bits on >= 2/3 of all tested locally-hosted SPAs (primary condition)
2. Permutation p < 0.0167 after Bonferroni correction on >= 2/3 sites
3. Positive control passes (synthetic response-side PMI >= 0.5 bits, p < 0.001 on test split)
4. Null control passes (shuffled real-SPA labels p > 0.01)
5. Data sufficiency met (n_test >= 30 on held-out test per site)
6. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING

If ANY of:
1. Primary condition fails (response-side PMI < 0.1 bits on >= 2/3 sites)
2. Permutation p >= 0.0167 after Bonferroni correction on >= 2/3 sites
3. Positive control fails
4. Null control fails

### 11.3 MEASUREMENT_INVALID

If:
1. Sample sizes insufficient (<30 held-out test transitions per site after temporal split)
2. Pipeline errors prevent computation
3. Response-side data capture fails (Playwright route interception cannot capture response bodies)

## 12. Validity Threats

### 12.1 Sample Size

With 30+ held-out test transitions per SPA, power is limited for detecting small effects. Report confidence intervals alongside p-values. Wizard may have <30 test transitions; if so, exclude from primary analysis.

### 12.2 Synthetic-to-Real Gap

Synthetic positive control may not reflect real SPA response patterns. Mitigation: pipeline validation on known structure is necessary before interpreting real SPA results.

### 12.3 Response-Side Capture Limitations

Playwright route interception may not capture all response-side data (streaming responses, WebSocket messages, Service Worker responses, large binary responses). Mitigation: focus on fetch/XHR JSON responses; document capture limitations in validity_notes.

### 12.4 Response Body Digest Coarseness

SHA-256 of response body[:500] may miss state-relevant information in larger responses or be too sensitive to irrelevant fields (timestamps, nonces). Mitigation: alpha sensitivity analysis; if body digest is too noisy, test with body[:200] and body[:1000] in exploratory analysis.

### 12.5 Response-Side Tautology Risk

Dashboard response bodies are deterministic functions of action label (tab name determines response). Response-side PMI may measure action→response causality, not orthogonal environmental dynamics. Mitigation: explicit tautology check (Section 9.3); report fraction of PMI attributable to action→response.

### 12.6 Temporal Split Risk

Wizard may have <30 transitions after 80/20 split (parent had 32 total, 80/20 gives ~6 test). If wizard test < 30, exclude from primary analysis. This reduces primary condition to 2 sites (dashboard, multistep_form), requiring both to pass.

### 12.7 Server Response Timing

Response timing (latency) may vary due to system load rather than SPA state. Mitigation: focus on response body digest and status code as primary signals; timing is secondary/exploratory.

## 13. Analysis Plan

1. **Data Collection**: Capture response-side data from 3 locally-hosted SPAs + synthetic SPA using modified capture script
2. **Quality Check**: Verify response bodies are captured for >= 90% of API/XHR responses per site
3. **Temporal Split**: 80/20 split per SPA, exclude SPAs with <30 held-out test transitions
4. **State Discretization**: Compute response-side, request-side, and URL-only state hashes on TRAIN, apply to TEST
5. **PMI Computation**: Compute PMI for each state representation on held-out TEST set
6. **Permutation Test**: 1000 permutations per SPA per state representation
7. **Bonferroni Correction**: Correct for 3 comparisons (alpha = 0.0167)
8. **Effect Size**: Compute Cohen's d for response-side vs request-side
9. **Alpha Sensitivity**: Test PMI at alpha = 0.0, 0.5, 1.0, 2.0
10. **Tautology Check**: Compute I(action; response_body) for dashboard
11. **Decision**: Apply frozen decision rules

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration and untouched evidence.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
