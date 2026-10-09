# Preregistration: Stationarity Classification and Re-acquisition Economics on Credential-Free Public HTTP

**Experiment ID:** EXP-FRONTIER-37385647440
**Lane:** frontier
**Claim IDs:** C-WEB-DYNAMICS, C-FRESHNESS, C-CROSSSITE
**Created:** 2026-10-05
**Status:** PRE-FREEZE (this document is frozen before any outcome measurement)

---

## 1. Executive Summary

This experiment measures the **stationarity class distribution** and **re-acquisition cost economics** of interface-state items on credential-free public HTTP sites. It replaces the unmeasurable "static re-derivable fraction" from the parent packet (EXP-FRONTIER-36306528608) with a dynamical measurement that is answerable on the actually-available substrate (stdlib HTTP, GET only, no browser, no credentials, no write verbs).

**Core Question:** For every candidate item of interface state a persistent agent would carry between episodes, which stationarity class does it belong to, and what does it cost to re-acquire a fresh valid instance?

**Falsifier (arithmetically checkable before freeze):** If the majority of detected state items are non-stationary (request_scoped, time_scoped, rotating) AND re-acquiring a fresh instance is not cheaper than unconditional re-derivation, then persistent cross-episode handle state has no amortization surface on this substrate class.

---

## 2. Substrate and Constraints

| Constraint | Value |
|------------|-------|
| HTTP Client | Python stdlib (`urllib.request`) or `requests` (stdlib-only if possible) |
| Verbs | GET only |
| Browser | None |
| Docker | None |
| Model Key | None |
| Credentials | None |
| Write Verbs | None |
| Tokenizer | `tiktoken` (must be declared in `pyproject.toml` or provisioned in workflow image) |
| Token Encoding | `cl100k_base` |
| Session Isolation | Disjoint cookie jars per session (`http.cookiejar.CookieJar` per session) |
| Inter-Session Delay | Minimum 60 seconds (configurable, declared before freeze) |
| Sessions per Target (K) | ≥ 5 (frozen at 5) |
| Target Sites | ≥ 4 hand-picked credential-free public HTTP sites |
| Target Items | ≥ 20 classified state items total |

**Ethical/Methodological Note:** 0 non-GET requests will be issued. No third-party state will be mutated. This is deliberate and correct; it means authorization semantics of observed gates are not measured.

---

## 3. Frozen Target Pool

Sites are hand-picked for credential-free accessibility, diversity of interaction patterns, and prior evidence of action-gating structure (from parent packet EXP-FRONTIER-36306528608 and Codex evidence). The pool is **explicitly not a prevalence sample** of the Web.

| Site | Root URL | Rationale |
|------|----------|-----------|
| GitLab | `https://gitlab.com` | Parent packet: 3 distinct `authenticity_token` values in 3 sessions; 3 action-gating objects |
| Wikimedia | `https://auth.wikimedia.org` | Parent packet: 3 distinct `wpCreateaccountToken` values in 3 sessions; 1 action-gating object |
| Wikipedia | `https://en.wikipedia.org` | Parent packet: 8 action-gating objects detected; C3-passing (token-gated forms) |
| Bitbucket | `https://bitbucket.org` | Parent packet: 9 action-gating objects detected; C3-passing, C5-passing |
| HTTPBin | `https://httpbin.org` | Calibration/control site; static endpoints, known-stationary controls |
| Postman Echo | `https://postman-echo.com` | Parent packet: 1 re-derivable object (off-host redirect noted); simple echo endpoints |

**Frozen at preregistration:** The exact list of 6 sites above. No post-freeze substitution allowed (control: `NO_POST_FREEZE_SITE_SUBSTITUTION`).

**Item Discovery:** For each site, we crawl from root (max 2 hops) via GET only, extracting:
- Links (`<a href>`)
- Forms (`<form>` with `method="GET"` or `method="POST"` — we only GET the form page, not submit)
- Input fields (`<input>`, `<select>`, `<textarea>`) with `name` attributes
- Meta tags with state-like content (CSRF tokens, nonces, etc.)
- JSON API endpoints discoverable from root (e.g., `/api/`, `/graphql` — GET only)

Each discovered **state item** is a tuple: `(site, page_url, element_type, element_name, selector_or_xpath)`. Example: `(gitlab.com, /users/sign_in, input, authenticity_token, //input[@name='authenticity_token'])`.

---

## 4. Stationarity Classification Scheme

Each detected state item is observed across **K = 5 independent fresh sessions** (disjoint cookie jars, ≥60s delay between sessions). In each session, we fetch the item's page URL and record:
- `value`: The extracted value (for inputs: `value` attribute; for meta: `content`; for links: `href`; for JSON: the parsed field)
- `body_hash`: SHA256 of the full HTTP response body
- `status_code`: HTTP status
- `response_headers`: Selected headers (Content-Type, Set-Cookie, ETag, Cache-Control)

**Classification Rules (mutually exclusive, evaluated in order):**

| Class | Definition | Operational Test |
|-------|------------|------------------|
| `session_invariant` | Value and body_hash identical across **all K sessions** | `len(set(values)) == 1 and len(set(body_hashes)) == 1` |
| `session_scoped` | Value and body_hash identical **within each session** but differ **across sessions** | `all(len(set(v)) == 1 for v in per_session_values) and len(set(across_session_values)) > 1` |
| `request_scoped` | Value or body_hash differs **across requests within the same session** | `any(len(set(v)) > 1 for v in per_session_values)` |
| `time_scoped` | Value differs across sessions with **periodicity consistent with inter-session delay** | Session-scoped pattern + Fourier/autocorrelation peak at declared delay frequency (simplified: values cycle with period ≈ K if delay-controlled) |
| `rotating` | Value differs across sessions with **no detectable periodicity** | Session-scoped pattern + no periodicity detected (residual class) |

**Tie-breaking:** If an item meets multiple criteria, the **first matching class in the table order** applies. This order is frozen.

**Per-Session Replication:** Within each session, we may issue 2 requests to the same URL (separated by ~1s) to detect `request_scoped` variance. This is the only intra-session repetition.

---

## 5. Re-acquisition Cost Measurement

For each classified item, we measure the cost to obtain **one fresh valid instance** from a cold start (no prior knowledge, no cached cookies, no cached responses).

**Procedure:**
1. Start new session (fresh cookie jar)
2. From site root, follow the **shortest unconditional path** (sequence of GET requests) to reach a page containing the item in a valid state (status 200, item present with extractable value)
3. Record:
   - `request_count`: Number of GET requests issued (including root)
   - `total_tokens`: Sum of `cl100k_base` token counts for all response bodies + headers observed along the path (using `tiktoken`)
   - `path_urls`: The sequence of URLs visited
   - `success`: Boolean (item found in valid state)

**Unconditional Re-derivation Baseline (COLD_REEXPLORATION):** Same procedure but the agent has **no prior map** — it must discover the path by crawling from root (breadth-first, max 2 hops, max 50 pages). This measures the cost of "starting from scratch" vs. "following a known path."

**Cost Metrics (per item, per class):**
- `re_acquisition_tokens`: Median tokens over K sessions
- `re_acquisition_requests`: Median requests over K sessions
- `re_derivation_tokens`: Median tokens for unconditional re-derivation (measured once per item)
- `re_derivation_requests`: Median requests for unconditional re-derivation
- `break_even_reuse_count`: `ceil(re_acquisition_cost / (re_derivation_cost - re_acquisition_cost))` if `re_derivation_cost > re_acquisition_cost`, else `null` (infinite)

**Token-to-latency and token-to-dollar:** Explicitly **UNKNOWN**. No imputation. Reported as `null` in all outputs.

---

## 6. Controls (Must Pass LIVE Before Freeze)

### 6.1 KNOWN_STATIONARY_CONTROL (Positive Control)
**Items:** Pre-declared static elements expected to be `session_invariant`:
- `https://httpbin.org/robots.txt` (static file)
- `https://httpbin.org/sitemap.xml` (if exists, else skip)
- `https://gitlab.com/favicon.ico` (or root page logo/link)
- `https://en.wikipedia.org/static/favicon/wikipedia.ico`
- Root page `href` to `https://gitlab.com/explore` (static nav link)
- Root page `href` to `https://en.wikipedia.org/wiki/Main_Page` (self-link)

**Pass Criterion:** ALL designated items classified as `session_invariant` with exact-value and body-hash equality across all 5 sessions. **If any fails → MEASUREMENT_INVALID.**

### 6.2 REVERIFIED_NON_STATIONARY (Live Positive Control)
**Items:** The 4 server-minted CSRF tokens from parent packet, re-verified live:
- `gitlab.com` → `/users/sign_in` → `input[name=authenticity_token]`
- `auth.wikimedia.org` → `/enwiki/w/index.php?title=Special:CreateAccount` → `input[name=wpCreateaccountToken]`
- (Plus any additional token-gated forms discovered in this run's crawl)

**Pass Criterion:** ALL designated items classified as `session_scoped` (identical within session, different across sessions) OR `rotating` (different across sessions, no periodicity). At least 2 distinct values across 5 sessions. **If any classified as `session_invariant` → MEASUREMENT_INVALID.**

### 6.3 INTER_SESSION_DELAY (Timing Control)
**Protocol:** Minimum 60 seconds wall-clock delay between consecutive sessions for the same target.
**Verification:** Log timestamps of session start/end. Compute actual delays.
**Pass Criterion:** All inter-session delays ≥ 60 seconds. **If any < 60s → MEASUREMENT_INVALID.**
**Purpose:** Ensures `time_scoped` (periodic with delay) is separable from `session_scoped` (changes per session regardless of time).

### 6.4 NULL_STATIONARITY_ARM (Null Control)
**Items:** Synthetic probes with **no stable identity**:
- Per-request timestamp: `https://httpbin.org/uuid` (returns new UUID per request)
- Per-request timestamp: `https://httpbin.org/date` (returns current time)
- Server-generated request ID: `https://httpbin.org/headers` (extract `X-Request-Id` if present, else `User-Agent` hash)
- Custom: Add `?cache_buster=<random>` to a static URL and observe response variance

**Pass Criterion:** At least 1 designated item classified as `request_scoped` or `rotating` (i.e., the arm **fires** and detects non-stationarity). **If all classified as `session_invariant` or `session_scoped` → MEASUREMENT_INVALID** (classifier not discriminating).

---

## 7. Measurement Validity Gates (Pre-Freeze)

All four controls above **must be verified LIVE and PASS** before `freeze.json` is created. The verification results (timestamp, evidence reference) are recorded in `spec.json.controls_pre_freeze_verification`.

If any control fails:
- The experiment is **not frozen**
- The design is revised
- A new preregistration is written
- No outcome data from the failed run is used

This prevents the "frozen calibration anchor wrong at freeze" failure mode from the parent packet.

---

## 8. Decision Rule (Frozen)

### 8.1 Primary Classification Output
- `class_distribution`: Counts and proportions of items in each of the 5 classes.
- Site-clustered bootstrap CI95 (10,000 resamples, seed = 37385647440).
- Reported as: `{class: {count, proportion, ci95_low, ci95_high}}`

### 8.2 Re-acquisition Economics Output
For each class with count > 0:
- `median_re_acquisition_tokens`, `median_re_acquisition_requests`
- `median_re_derivation_tokens`, `median_re_derivation_requests`
- `break_even_reuse_count` (or `null` if infinite)
- Site-clustered CI95 for break-even (resample sites, not items)

### 8.3 Falsifier Evaluation
```
majority_non_stationary = (count_request_scoped + count_time_scoped + count_rotating) > 
                          (count_session_invariant + count_session_scoped)

cost_condition = median_re_acquisition_tokens_non_stationary >= 
                 median_re_derivation_tokens_non_stationary
                 (using the majority non-stationary class's medians)

falsifier_triggered = majority_non_stationary AND cost_condition
```

### 8.4 Outcome Mapping

| Condition | Status | Outcome |
|-----------|--------|---------|
| Any control FAIL | MEASUREMENT_INVALID | INCONCLUSIVE |
| All controls PASS, falsifier_triggered = TRUE | COMPLETE | FALSIFIES (bounded: HANDLE PERSISTENCE on credential-free HTTP substrate) |
| All controls PASS, falsifier_triggered = FALSE, at least one class has finite break_even | COMPLETE | SUPPORTS |
| All controls PASS, falsifier_triggered = FALSE, no class has finite break_even | COMPLETE | MIXED |
| Controls PASS but classification ambiguous (e.g., items unclassifiable) | COMPLETE | MIXED |

**Critical:** Metrics for unexecuted arms (e.g., `ORACLE_PERFECT_TRANSFER` for non-session_invariant classes) are reported as `null`, never `0.0`.

---

## 9. Durable Evidence Requirements

All raw evidence persisted with **non-self-referential SHA256 hashes** (content-addressed):

| Artifact | Format | Hashing |
|----------|--------|---------|
| Raw HTTP responses | `raw/responses_cache/{sha256}.json` | SHA256 of response body |
| Per-session item observations | `raw/observations.jsonl` | Per-line SHA256 in `observation_hash` field |
| Classification results | `derived/classification.json` | SHA256 of file |
| Cost measurements | `derived/costs.json` | SHA256 of file |
| Control verification logs | `raw/controls_verification.jsonl` | Per-line SHA256 |
| Session timing logs | `raw/session_timing.jsonl` | Per-line SHA256 |

**Auditability:** The full run is reproducible from durable evidence without re-hitting live network.

---

## 10. Validity Threats and Disclosures

| Threat | Mitigation / Disclosure |
|--------|-------------------------|
| Hand-picked site pool (not prevalence) | Explicitly labelled; class distribution is a **sample of this pool**, not Web prevalence |
| No browser / no JavaScript execution | Items existing only in JS-rendered DOM are **invisible by construction**; disclosed as substrate limit |
| No write verbs / no credentials | Authorization semantics of token-gated forms **not measured**; `ORACLE_PERFECT_TRANSFER` null for non-session_invariant |
| Token cost ≠ latency/dollar | Explicitly `UNKNOWN`; no economic claim beyond token/request counts |
| Inter-session delay (60s) may not capture all time_scoped periods | Declared limitation; longer periods would be misclassified as `rotating` |
| Single unconditional path per item | May not be globally optimal; measures *a* valid path, not *the* minimal path |
| Parent packet's httpbin calibration anchor was wrong | This experiment uses httpbin only for controls (static files, UUID/date), not as primary target |
| Tiktoken installed at runtime | Must be declared in `pyproject.toml` or provisioned; disclosed as build-time dependency |

---

## 11. Product and Claim Consequences

### If FALSIFIES (falsifier triggered):
- **Bounded Negative:** Persistent cross-episode **handle state** has no amortization surface on credential-free public HTTP substrate.
- **Architecture Redirect:** SPIDER should not invest in cross-episode handle persistence for this substrate. Effort shifts to: procedure re-execution caching, semantic resolution of re-derivation paths, or substrate expansion (browser, credentials, write).
- **Claims:** C-FRESHNESS (staleness detection) scope narrowed — no handle to go stale. C-CROSSSITE (transfer) not closed — mechanism transfer may still work. C-WEB-DYNAMICS (timescales) receives evidence that stationarity is predominantly non-stationary on this substrate.

### If SUPPORTS (falsifier not triggered, finite break-even exists):
- **Measurable Amortization Surface:** Persistent state is economically justified for `session_invariant` and/or `session_scoped` classes.
- **Architecture Investment:** Persist handles for these classes; implement staleness guards (C-FRESHNESS) keyed to session boundary.
- **Break-even Counts:** Become the economic guard — only persist if expected reuse > break_even.
- **Claims:** C-FRESHNESS advances (staleness detectable for session_scoped). C-CROSSSITE receives evidence that some state transfers. C-WEB-DYNAMICS receives stationarity distribution evidence.

### If MIXED:
- Per-class architecture: persist for session_invariant, re-derive for rotating.
- Product kernel must support class-conditional persistence.

---

## 12. Dependencies on Other Lanes

| Dependency | Owner | Status |
|------------|-------|--------|
| Runtime capability ledger (token→latency/dollar) | Runtime | **UNKNOWN** — not required for this experiment; token counts reported without conversion |
| Screen/calibration repair (C3 executability, C7 403 false-positive, host-root rooting) | Runtime (C-MEAS-VALID) | **Not required** — this experiment uses per-item admission, not site-level conjunction screen |
| Executable induced mechanism in kernel (distill_parameterized) | Product/Graph (C-PARAM-INHERIT) | **Not required** — this experiment measures substrate properties, not kernel mechanisms |
| Self-hosted credentialed substrate for write-leg | Runtime/Program | **Not required** — 0 non-GET requests by design |

---

## 13. What This Experiment Does NOT Do

- ❌ Measure Web prevalence (hand-picked pool only)
- ❌ Test cross-episode transfer (no prior episodes)
- ❌ Test LLM agent inheritance (no model calls)
- ❌ Measure authorization semantics (no form submission)
- ❌ Measure JavaScript-rendered state (stdlib HTTP only)
- ❌ Promote to Product Core (Frontier lane, no src/ changes)
- ❌ Close C-CROSSSITE, C-FRESHNESS, or C-WEB-DYNAMICS broadly (bounded to this substrate class)

---

## 14. Success Criteria for Freeze

Before `freeze.json` is created, the following must be verified and recorded in `spec.json.controls_pre_freeze_verification`:

1. `KNOWN_STATIONARY_CONTROL`: PASS (all items session_invariant)
2. `REVERIFIED_NON_STATIONARY`: PASS (all items session_scoped or rotating, ≥2 distinct values)
3. `INTER_SESSION_DELAY`: PASS (all delays ≥ 60s)
4. `NULL_STATIONARITY_ARM`: PASS (at least 1 item request_scoped or rotating)

Only when all four are `{"status": "PASS", "verified_at": "<ISO8601>", "evidence_ref": "<path>"}` may the experiment proceed to freeze.

---

## 15. Frozen Hashes (To Be Filled at Freeze)

| File | SHA256 |
|------|--------|
| `request.json` | (filled by freezer) |
| `spec.json` | (filled by freezer) |
| `prereg.md` | (filled by freezer) |

---

**End of Preregistration.** This document is immutable after freeze. Any design change requires a new experiment ID.