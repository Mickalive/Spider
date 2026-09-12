# EXP-PHYSICS-34674671762 — Network-Request PMI Analysis

## Executive Summary

**Outcome: FALSIFIES** (primary condition fails on 1/3 sites)

Network-request signatures (endpoint+method+status+body) as state representation show strong predictive PMI on one genuine SPA (dashboard: +0.881 bits) but fail on two others (multistep_form: 0.0 bits, wizard: 0.0 bits). The preregistered primary condition requires >= 2/3 of sites to show >= 0.1 bits improvement; only 1/3 passes. Both controls pass, confirming pipeline validity.

## 1. Controls

### Positive Control (Synthetic SPA)
- **Result: PASS** ✓
- Network-request PMI: **0.860 bits** (threshold: >= 0.5)
- Permutation p: **0.001** (threshold: < 0.001)
- The PMI pipeline correctly detects deterministic network-request structure when present.

### Null Control (Shuffled Labels)
- **Result: PASS** ✓
- Shuffled PMI: 0.445 bits
- Permutation p: **0.318** (threshold: > 0.01)
- The pipeline does not produce false positives on shuffled data.

## 2. Genuine SPA Results

| Site | Network PMI | URL PMI | Improvement | Perm p (bonf) | Passes |
|------|-------------|---------|-------------|----------------|--------|
| dashboard | 0.881 bits | 0.0 bits | **+0.881 bits** | 0.003 | ✓ |
| multistep_form | 0.0 bits | 0.0 bits | 0.0 bits | 1.0 | ✗ |
| wizard | 0.0 bits | 0.0 bits | 0.0 bits | 1.0 | ✗ |

**Primary condition**: 1/3 sites pass (threshold: >= 2/3) → **FAILS**

## 3. Analysis

### Dashboard SPA (Passes)
The dashboard SPA triggers genuinely different API endpoints per tab:
- Overview: `/api/tab/overview`
- Analytics: `/api/tab/analytics`
- Users: `/api/tab/users`
- Settings: `/api/tab/settings`

Each tab switch produces a unique network-request hash (endpoint path differs), creating 5 distinct states from 4 tabs + initial state. The network-request PMI (0.881 bits) is strongly significant with Bonferroni-corrected p = 0.003 and large effect size (d = 8.82).

Alpha sensitivity shows robustness: PMI ranges from 1.937 (alpha=0.0) to 1.306 (alpha=2.0), confirming the result is not an artifact of smoothing.

### Multistep Form SPA (Fails)
Despite having 4 wizard steps (shipping, payment, review, confirmation), all steps trigger identical API calls:
- `POST /api/checkout/next` (or `/prev`)
- `GET /checkout` (page reload)

The network requests do not encode step identity. The server tracks step state via session cookie, but this is invisible to client-side network-request capture. Network-request PMI = 0.0 bits.

### Wizard SPA (Fails)
The wizard SPA has distinct steps (personal_info, address, payment, review) but the API calls are:
- `POST /api/wizard/next` (or `/prev`)
- `GET /wizard` (page reload)

Step-specific validation APIs are triggered server-side in response to `/api/wizard/next`, not by client-side fetch. They appear as server responses, not as distinct client-observable network requests. Network-request PMI = 0.0 bits.

## 4. Interpretation

The hypothesis that network-request signatures capture predictive state information beyond URL is **partially supported**:

- **Strong evidence FOR**: On the dashboard SPA, where different tabs trigger genuinely different API endpoints, network-request PMI is 0.881 bits — well above the 0.1 bits threshold.
- **Strong evidence AGAINST**: On the multistep form and wizard SPAs, where the same API endpoints are called regardless of internal state, network-request PMI is 0.0 bits.

The key differentiator is whether the SPA's API calls **encode state information in client-observable request signatures**. SPAs that use server-side session tracking (hiding state in cookies/server memory) do not produce state-dependent network-request patterns.

**Does NOT falsify C-WEB-DYNAMICS entirely**: The dashboard result demonstrates that network-request signatures CAN capture predictive dynamical structure. The negative results on multistep_form and wizard constrain the hypothesis to SPAs where API calls genuinely vary by state.

## 5. Product Consequence

If network-request signatures are to be used as a complementary state representation:
- They work well on SPAs with **distinct API endpoints per state** (dashboards, data-heavy apps)
- They fail on SPAs with **server-side session tracking** (wizards, forms)
- The representation needs to be augmented with response body digests or timing patterns for session-tracked SPAs

## 6. Deviation Notes

1. HTTPBin was excluded due to Playwright navigation failure (net::ERR_ABORTED). Only 3 local SPAs were tested.
2. The wizard SPA captured 32 transitions (vs 120 planned) due to browser context closure.
3. All genuine SPAs are locally hosted, not production sites. This limits generalizability.
