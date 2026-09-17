# Preregistration: EXP-PHYSICS-35262258744

## Title

URL-level PMI on real browser-collected SPA transitions: raw vs normalized URL representation

## Lane

Physics

## Claim

C-WEB-DYNAMICS: Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity.

## Question

Does URL-level pointwise mutual information (PMI) between actions and next-states detect predictive dynamical structure on real browser-collected SPA transitions when URL fragments are preserved — and how much information does standard fragment-stripping normalization destroy?

## Background and Motivation

The C-WEB-DYNAMICS research program has accumulated 30+ experiments, all either synthetic or locally-hosted. The dominant bottleneck is the synthetic-to-real gap: no experiment has tested PMI on real browser-collected SPA transitions.

Parent experiment EXP-PHYSICS-35209110569 validated 5 TodoMVC hash-SPA variants as suitable testbeds:
- All 5 variants achieve leakage < 40% (valid-only 0.213–0.285)
- 50 non-leakage transitions achievable at 64–70 raw per variant
- Per-type stratification: link_click leakage 1.00, button_click/form_submit/js_navigate leakage 0.00
- Title variation: 0/5 variants have ≥2 unique titles (entropy 0.0 bits) — title-aware PMI falsified on TodoMVC

A critical finding from the parent analysis: fragment-stripping normalization (`url.split("#")[0]`) collapses all TodoMVC URLs to a single state (unique_urls_norm = 1, url_entropy = 0.0 bits). This means:
- **Normalized URL-only PMI is mathematically 0.0 bits** — not because there is no structure, but because the representation destroys it
- **Raw URLs with fragments have 3+ unique states**: `#/` (all), `#/active`, `#/completed`
- The question is whether these fragment-encoded states carry predictive information

This experiment directly tests whether URL fragments on hash-SPAs encode state information detectable by PMI, and quantifies the information loss from standard normalization.

## Hypothesis

On TodoMVC hash-SPA variants where fragment-stripping normalization collapses all URLs to a single state (normalized URL entropy = 0.0 bits), raw URL PMI with fragments preserved will be significantly positive under cross-trajectory permutation testing, demonstrating that hash-based routing encodes state information in URL fragments that standard normalization destroys.

## Falsifier

The claim is falsified if ANY of:
1. Fewer than 3/5 variants achieve raw URL PMI > 0.05 bits with Bonferroni-corrected permutation p < 0.01
2. The positive control (synthetic deterministic SPA) fails (PMI < 1.0 bits)
3. Fewer than 3/5 variants have ≥ 50 non-leakage transitions after filtering
4. Fewer than 3/5 variants have ≥ 5 unique raw URLs (insufficient state variation)
5. More than 1/5 variants have > 50% singleton state-action pairs (PMI estimator degenerate)

## Experimental Conditions

### Primary Condition: Raw URL PMI

- **State representation**: raw `url_before` (with fragment, e.g., `https://todomvc.com/examples/react/dist/#/active`)
- **Action representation**: `action_primitive` categorical (form_submit, button_click, js_navigate)
- **Next-state**: raw `url_after` (with fragment)
- **Non-leakage filter**: `action_primitive != 'link_click'` (all link_click are leakage on TodoMVC hash-SPAs)
- **Expected**: raw URLs have 3+ unique states (#/, #/active, #/completed); PMI may be > 0 if transitions are not uniformly distributed across states

### Null Control Condition: Normalized URL PMI

- **State representation**: `normalize(url_before)` where normalize = `url.split("#")[0]`, strip trailing slash, unquote
- **Action representation**: same as primary
- **Next-state**: `normalize(url_after)`
- **Expected**: exactly 0.0 bits (mathematically forced: 1 unique state → P(s'|s) = 1.0 for all s' → PMI = 0)

### Positive Control

- Synthetic deterministic SPA with 8 states, 4 actions, known action→next-state mapping (same as EXP-PHYSICS-34149195420)
- **Expected**: PMI ≥ 1.0 bits, permutation p < 0.001
- **Purpose**: validate PMI pipeline detects known structure before testing real data

## Data

### Source

Reuse parent raw transition files from `research/experiments/EXP-PHYSICS-35209110569/`:
- `raw_vanillajs.json`, `raw_vanillajs_topup.json`
- `raw_react.json`, `raw_react_topup.json`
- `raw_vue.json`, `raw_vue_topup.json`
- `raw_angular.json`, `raw_angular_topup.json`
- `raw_svelte.json`, `raw_svelte_topup.json`
- `raw_wikipedia.json`, `raw_wikipedia_s0fix.json` (null control for leakage validation)

No new browser collection required.

### Transition Format

Each record contains:
```json
{
  "site": "vanillajs",
  "session": 0,
  "url_before": "https://todomvc.com/examples/javascript-es6/dist/",
  "url_after": "https://todomvc.com/examples/javascript-es6/dist/#/",
  "title_before": "TodoMVC: JavaScript Es6 Webpack",
  "title_after": "TodoMVC: JavaScript Es6 Webpack",
  "action_primitive": "link_click",
  "action_target": "https://todomvc.com/examples/javascript-es6/dist/#/",
  "timestamp": "2026-09-17T18:25:22.610864+00:00",
  "error": null
}
```

### Sample Sizes (from parent)

| Variant | Raw | Valid | Non-Leakage | Unique Raw URLs |
|---------|-----|-------|-------------|-----------------|
| vanillajs | 168 | 130 | ~83 | 3+ (with fragments) |
| react | 168 | 130 | ~83 | 3+ |
| vue | 168 | 108 | ~85 | 3+ |
| angular | 168 | 130 | ~83 | 3+ |
| svelte | 168 | 130 | ~83 | 3+ |
| wikipedia | 100 | 100 | 0 (all link_click) | N/A |

## Metrics

### Primary Metric

**Raw URL PMI**: Mean pointwise mutual information I(url_before_raw; url_after_raw | action_primitive) across non-leakage transitions, computed with Laplace smoothing (alpha=1.0).

PMI formula:
```
PMI(s, a, s') = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]
```
where s = raw url_before, a = action_primitive, s' = raw url_after.

### Secondary Metrics

1. **Normalized URL PMI**: Same formula with fragment-stripped URLs. Expected: exactly 0.0 bits.
2. **Raw vs Normalized PMI difference**: raw_PMI - normalized_PMI. Quantifies information loss from fragment-stripping.
3. **Unique raw URL count per variant**: Number of distinct raw urls (with fragments). Expected: 3+ (#/, #/active, #/completed).
4. **Unique state-action pair count**: Number of distinct (raw_url, action) pairs. Degenerate if > 50% are singletons.
5. **Singleton fraction**: Fraction of state-action pairs appearing exactly once. If > 50%, PMI estimator is degenerate.
6. **Permutation p-value**: P(shuffled PMI >= observed PMI) from 1000 cross-trajectory shuffles.
7. **Effect size (Cohen's d)**: (observed PMI - null mean) / null std.
8. **Non-leakage transition count**: Must be >= 50 per variant.

## Analysis Plan

### Step 1: Load and Filter

1. Load raw transition files for each variant
2. Combine base + topup files
3. Filter: keep only transitions where `error is None`
4. Filter: keep only non-leakage transitions where `action_primitive != 'link_click'`
5. Count transitions per variant; check >= 50

### Step 2: Extract Triples

For each non-leakage transition:
- Raw triple: `(url_before, action_primitive, url_after)` — fragments preserved
- Normalized triple: `(normalize(url_before), action_primitive, normalize(url_after))` — fragments stripped

Where `normalize(url) = url.split("#")[0].rstrip("/")`.

### Step 3: Compute PMI

For each variant and each condition (raw, normalized):
1. Count states, actions, state-action pairs, triple counts
2. Compute per-transition PMI with Laplace smoothing (alpha=1.0)
3. Compute mean PMI across all transitions
4. Record unique state count, unique SA pair count, singleton fraction

### Step 4: Permutation Test

For each variant and condition:
1. Group transitions by session (trajectory)
2. For 1000 permutations (seed=42):
   - Shuffle action labels within each session
   - Recompute mean PMI on shuffled data
3. Compute p-value: P(shuffled >= observed)
4. Compute effect size d: (observed - null_mean) / null_std

### Step 5: Controls

1. **Positive control**: Run PMI on synthetic deterministic SPA data (same as EXP-PHYSICS-34149195420). Check PMI >= 1.0, p < 0.001.
2. **Null control**: Check normalized URL PMI = 0.0 bits on all 5 variants.

### Step 6: Decision

Apply frozen decision_rule. If ALL conditions pass → SURVIVES_CURRENT_TEST. If raw PMI condition fails → FALSIFIED-IN-SETTING. If controls fail → MEASUREMENT_INVALID.

## Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
1. ≥ 3/5 variants: raw URL PMI > 0.05 bits AND Bonferroni p < 0.01 (5 comparisons, alpha = 0.01)
2. Normalized URL PMI = 0.0 bits on all 5 variants
3. Positive control PMI >= 1.0 bits
4. ≥ 50 non-leakage transitions per variant
5. ≥ 5 unique raw URLs per variant

**FALSIFIED-IN-SETTING** if: fewer than 3/5 variants achieve raw URL PMI > 0.05 bits with Bonferroni p < 0.01.

**MEASUREMENT_INVALID** if: controls fail or data quality insufficient.

## Validity Threats

1. **Low raw URL cardinality**: TodoMVC hash-SPAs may have only 3 raw URLs (#/, #/active, #/completed), limiting PMI sensitivity. With 3 states and 3 actions, maximum possible PMI is log2(3) ≈ 1.585 bits. If transitions are uniformly distributed, observed PMI will be low even if structure exists. Report unique raw URL count and SA pair cardinality.

2. **Singleton SA pairs**: If most (url, action) pairs appear once, Laplace-smoothed PMI is biased toward 0. Report singleton fraction; flag if > 50%.

3. **Action vocabulary limited**: Only 3 action types (form_submit, button_click, js_navigate) after excluding link_click. Limited action diversity reduces PMI sensitivity.

4. **Deterministic transitions**: TodoMVC transitions are mostly deterministic (same (url, action) → same next_url). This makes PMI either high (if state space is rich) or 0 (if collapsed). The raw-vs-normalized comparison is informative regardless.

5. **Laplace smoothing bias**: Alpha=1.0 inflates PMI for sparse counts. Report null mean from permutation test to bound inflation.

6. **No title variation**: All TodoMVC titles are constant (entropy 0.0 bits). Title-aware PMI is not testable; this experiment tests URL-only PMI with fragments.

## Preregistration Timing

This preregistration was written BEFORE any outcome data was inspected. The analysis script will be frozen after this preregistration is written. No modifications to the analysis plan after seeing results.
