# EXP-PHYSICS-35209110569 — SPA Corpus Survey for C-WEB-DYNAMICS

**Status:** DESIGN NOT YET FROZEN  
**Lane:** physics  
**Claim:** C-WEB-DYNAMICS  
**Parent:** EXP-PHYSICS-35185288822 (MEASUREMENT_INVALID, structural leakage 78-92% on server-rendered MPAs)

---

## 1. Question

Which TodoMVC hash-SPA variants exhibit URL-level leakage below 40% and sufficient title variation, enabling >=50 non-leakage transitions for PMI analysis — thereby identifying suitable production-like testbeds to bridge the synthetic-to-real gap in the C-WEB-DYNAMICS research program?

## 2. Hypothesis

TodoMVC hash-SPA variants with client-side routing (where multiple views share the same URL path, e.g., `#/active`, `#/completed`) exhibit lower URL-level leakage than server-rendered MPAs (78-92%), because:

- Hash-based navigation allows multiple states per URL
- Client-side transitions (button clicks, form submissions, JavaScript-triggered) produce non-link-leakage transitions
- At least 1 of 5 variants achieves <40% leakage, enabling >=50 NL transitions at manageable raw collection sizes (~83 raw at 40% leakage)

## 3. Falsifier

The claim is falsified if ANY of:

1. ALL 5 TodoMVC variants exhibit leakage >=40%
2. ALL variants have <2 unique `document.title` values
3. ALL variants have achievable NL count <50 at 500 raw collection limit (`achievable_NL = 500 * (1 - leakage_rate)`)
4. Positive control (Wikipedia) leakage <80% (confirming measurement validity)
5. Data quality insufficient (<100 raw transitions per variant)

## 4. Sites

| Variant | Framework | URL | Expected Leakage |
|---------|-----------|-----|------------------|
| Vanilla JS (ES6) | None | todomvc.com/examples/vanillajs/ | <60% |
| React | React | todomvc.com/examples/react/ | <60% |
| Vue | Vue.js | todomvc.com/examples/vue/ | <60% |
| Angular | Angular | todomvc.com/examples/angular/ | <60% |
| Svelte | Svelte | todomvc.com/examples/svelte/ | <60% |

**Positive control:** Wikipedia (server-rendered MPA, expected leakage >80%)  
**Null control:** TodoMVC vanilla JS (known SPA structure, expected leakage <60%)

## 5. Actions

For each variant, perform these actions across 5+ sessions:

- **Link clicks:** Click filter links (All, Active, Completed)
- **Button clicks:** Toggle todo completion, destroy todo, clear completed
- **Form submissions:** Add new todo (type text + Enter)
- **JavaScript-triggered:** Navigate via browser back/forward, refresh page

Record per transition:
- URL (before and after)
- `document.title` (before and after)
- Action target (href or element selector)
- Action primitive (click, submit, keypress, navigate)
- Timestamp

## 6. Measurements

### Primary Metrics

| Metric | Definition | Threshold |
|--------|-----------|-----------|
| Leakage rate | `action.target_href == state_after.url` fraction | <40% for viability |
| Unique titles | Distinct `document.title` values across transitions | >=2 per variant |
| Achievable NL | `500 * (1 - leakage_rate)` | >=50 per variant |
| Raw transitions | Total collected per variant | >=100 per variant |

### Secondary Metrics

- Per-action-type leakage rate (link_click, button_click, form_submit, keypress)
- Title entropy: `H(document.title)` across transitions
- URL entropy: `H(URL)` across transitions
- Action type distribution: `P(action_primitive)`

## 7. Controls

### Positive Control: TodoMVC Vanilla JS

- **Expected:** Leakage <60%, unique_titles >=2, raw_transitions >=100
- **Pass criterion:** leakage <60% AND unique_titles >=2 AND raw_transitions >=100
- **Purpose:** Validates measurement pipeline on known SPA structure

### Null Control: Wikipedia

- **Expected:** Leakage >80%, unique_titles >=2, raw_transitions >=100
- **Pass criterion:** leakage >80% AND unique_titles >=2 AND raw_transitions >=100
- **Purpose:** Confirms measurement pipeline correctly identifies high leakage on known MPAs

## 8. Data Collection Protocol

### Setup

1. Install Playwright with headless Chrome
2. Create collection script: `collect_spa_survey.py`
3. For each variant:
   - Navigate to variant URL
   - Wait for page load (network idle)
   - Record initial state (URL, title, DOM hash)
   - Perform action (click, submit, navigate)
   - Record resulting state
   - Repeat for 20+ actions per session
   - Run 5+ sessions per variant

### EPIPE Mitigation

- Use single-page context per session
- Close browser between sessions (not context)
- Do not close context before page load complete
- Add 1.5s delay between actions (polite crawling)
- Add 2.0s delay for page capture after action

### Leakage Classification

```python
def is_leakage(action_target, state_after_url):
    """Check if action.target_href == state_after.url"""
    # Normalize URLs
    target = normalize_url(action_target)
    state = normalize_url(state_after_url)
    return target == state

def normalize_url(url):
    """Strip trailing slash, decode percent-encoding, ignore fragment"""
    # Remove fragment
    url = url.split('#')[0]
    # Remove trailing slash
    url = url.rstrip('/')
    # Decode percent-encoding
    url = urllib.parse.unquote(url)
    return url
```

## 9. Analysis Plan

### Step 1: Compute Leakage Rates

For each variant:
- Count total transitions (N_raw)
- Count leakage transitions (N_leakage) where `action.target_href == state_after.url`
- Compute leakage_rate = N_leakage / N_raw
- Compute achievable_NL = 500 * (1 - leakage_rate)

### Step 2: Compute Title Variation

For each variant:
- Count unique `document.title` values (unique_titles)
- Compute title entropy: `H(title) = -sum(p_i * log2(p_i))`

### Step 3: Compute Per-Type Leakage

For each variant and action type:
- Count transitions per type
- Compute per-type leakage rate
- Identify which action types produce non-leakage transitions

### Step 4: Decision

Apply frozen decision rule:
- If >=1 variant achieves leakage <40% AND achievable_NL >=50: SURVIVES
- If 0 variants achieve these thresholds: FALSIFIED-IN-SETTING
- If controls fail or data quality insufficient: MEASUREMENT_INVALID

## 10. Product Consequences

### Positive Outcome

If >=1 variant achieves <40% leakage:
- That variant becomes priority target for next PMI experiment
- SPIDER should collect 500+ raw transitions on that variant
- Title-aware PMI pipeline should be applied to the NL subset
- The synthetic-to-real gap is bridged (first production-like SPA testbed)

### Negative Outcome

If all variants >=40% leakage:
- URL-level PMI approach is not viable for these SPAs
- SPIDER should reconsider state representation:
  - DOM visible_text_hash (tested on locally-hosted SPAs, mixed results)
  - Accessibility tree (not tested on production SPAs)
  - Visual layout / computed styles (not tested)
  - Learned state abstractions (not tested)
- The dominant synthetic-to-real gap persists

## 11. Validity Threats

1. **TodoMVC is not "production":** TodoMVC is a demonstration app, not a production SPA with real users. Leakage rates on TodoMVC may not generalize to production SPAs (Gmail, Twitter, Notion). However, TodoMVC provides a controlled testbed with known structure, which is appropriate for a feasibility survey.

2. **Hash-based routing only:** The survey tests hash-based routing (`#/active`), not history-based routing (`/active`). Production SPAs often use history-based routing. However, hash-based routing is the simplest case and should have lowest leakage.

3. **No authentication:** TodoMVC has no authentication, so the survey cannot test auth-gated transitions. However, the parent handoff identifies URL-level leakage as the primary bottleneck, not auth.

4. **Playwright EPIPE:** EPIPE errors in CI may limit data collection. The EPIPE mitigation protocol should handle this, but if it fails, the experiment may be MEASUREMENT_INVALID.

5. **Leakage definition:** The leakage definition (`action.target_href == state_after.url`) may over-classify redirect/normalized URLs. The URL normalization should handle this, but edge cases may remain.

## 12. Expected Outcomes

Based on prior knowledge:

- **TodoMVC vanilla JS:** Expected low leakage (<40%) because:
  - Filter links use hash-based URLs (`#/active`, `#/completed`)
  - Button clicks (toggle, destroy, clear) have no href
  - Form submissions (add todo) have no href
  - Only filter links produce leakage transitions

- **TodoMVC React/Vue/Angular/Svelte:** Expected similar low leakage because:
  - Same TodoMVC structure across frameworks
  - Same hash-based routing
  - Same action types (click, submit, keypress)

- **Wikipedia:** Expected high leakage (>80%) because:
  - Server-rendered links encode full destination URLs
  - Link clicks dominate navigation
  - Button/form transitions are rare

If the expected outcomes hold, the survey will identify TodoMVC variants as suitable testbeds for PMI analysis, justifying the SPA pivot.

---

**Next steps after this survey:**
1. If SURVIVES: Design PMI experiment on lowest-leakage variant
2. If FALSIFIED: Reconsider state representation or abandon URL-level PMI
3. If MEASUREMENT_INVALID: Fix infrastructure and re-run survey
