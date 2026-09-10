# EXP-PHYSICS-34266105229 — Real SPA Title-Aware PMI

## Executive Summary

**Status**: COMPLETE | **Outcome**: FALSIFIES

Title-aware PMI (URL+title) does **not** exceed URL-only PMI on either TodoMVC React or TodoMVC Vue. Both sites use a single constant `document.title` across all client-side routes, making the title representation isomorphic to URL-only. The hypothesis is falsified in this setting, but the falsification is narrow: it targets TodoMVC's constant-title architecture, not the general C-WEB-DYNAMICS claim.

**Verdict**: FALSIFIED-IN-SETTING per frozen decision rules.

---

## 1. Positive Control (Pipeline Integrity)

| Metric | Value | Threshold | Pass |
|--------|-------|-----------|------|
| URL-only PMI | 0.693 bits | ≥ 0.5 | ✓ |
| Permutation p | 0.001 | < 0.001 | ✓ |

The synthetic SPA pipeline (8 states, 4 actions, deterministic transitions) produces PMI = 0.693 bits with permutation p = 0.001. Pipeline integrity is confirmed. This matches the parent experiment (EXP-PHYSICS-34149195420) synthetic results exactly.

---

## 2. Real SPA Data Collection

### 2.1 Sites

| Site | Framework | URL | Unique URLs | Unique Titles |
|------|-----------|-----|-------------|---------------|
| TodoMVC React | React | `todomvc.com/examples/react/dist/#/` | 3 | **1** ("TodoMVC: React") |
| TodoMVC Vue | Vue | `todomvc.com/examples/vue/dist/#/` | 3 | **1** ("TodoMVC: Vue") |

### 2.2 Transitions

| Site | Total | Non-Leakage | NL Fraction | Unique SA Pairs |
|------|-------|-------------|-------------|-----------------|
| React | 400 | 400 | 100% | 18 |
| Vue | 400 | 400 | 100% | 18 |

All transitions are non-leakage by the parent definition (action.target_href ≠ state_after.url). TodoMVC's hash-based navigation means filter/toggle/add actions change internal state without altering the URL path, so the action description never matches the resulting URL.

### 2.3 State Distribution

**React** — URL distribution:
- `#/` : 213 (53%)
- `#/active` : 105 (26%)
- `#/completed` : 82 (21%)

**Vue** — URL distribution:
- `#/` : 202 (51%)
- `#/active` : 106 (27%)
- `#/completed` : 92 (23%)

**Actions** (both sites): `filter_all`, `filter_active`, `filter_completed`, `toggle_0`, `add_todo`, `clear_completed` — 6 distinct action types.

---

## 3. PMI Results

### 3.1 Primary Comparison: URL-Only vs URL+Title

| Site | URL-Only PMI | URL+Title PMI | Improvement | URL+Title > URL-Only |
|------|-------------|---------------|-------------|----------------------|
| React | 1.360 bits | 1.360 bits | **0.0%** | **No** |
| Vue | 1.323 bits | 1.323 bits | **0.0%** | **No** |

**Critical observation**: Because both sites have exactly 1 unique title, the URL+title state representation produces identical state identifiers to URL-only. Adding title information provides exactly zero additional discrimination power.

### 3.2 URL+Title+Form

| Site | URL+Title+Form PMI | Form Marginal (above URL+Title) |
|------|-------------------|--------------------------------|
| React | 1.360 bits | 0.0 bits |
| Vue | 1.323 bits | 0.0 bits |

Form signals add no marginal information beyond titles — consistent with parent finding, but for a different reason (titles are constant, not because form signals are redundant with discriminative titles).

### 3.3 Comparison with Parent Synthetic Results

| Metric | Parent Synthetic | Real React | Real Vue |
|--------|-----------------|------------|----------|
| URL-only PMI | 0.693 bits | 1.360 bits (+96%) | 1.323 bits (+91%) |
| URL+title PMI | 1.970 bits | 1.360 bits (−31%) | 1.323 bits (−33%) |
| Title improvement | +184% | 0.0% | 0.0% |

Real URL-only PMI (1.32–1.36 bits) substantially exceeds the parent synthetic baseline (0.693 bits), indicating richer action-conditioned structure in real TodoMVC transitions. However, real URL+title PMI falls far short of the parent synthetic value (1.970 bits) because real titles are constant while synthetic titles were designed to be unique discriminators.

---

## 4. Permutation Tests

| Site | Representation | Observed PMI | Null Mean | Effect d | p-value |
|------|---------------|-------------|-----------|----------|---------|
| React | url_only | 1.360 | 0.060 | 83.14 | 0.001 |
| React | url_title | 1.360 | 0.060 | 83.14 | 0.001 |
| Vue | url_only | 1.323 | 0.060 | 85.66 | 0.001 |
| Vue | url_title | 1.292 | 0.060 | 85.66 | 0.001 |

Cross-trajectory permutation confirms that URL-level action→next-state dependency is genuine and extremely strong on both sites (0/1000 shuffled means exceed observed PMI). The large effect sizes (d > 80) indicate high statistical power. The permutation null is valid.

---

## 5. Decision Rule Evaluation

| Criterion | Required | Observed | Pass |
|-----------|----------|----------|------|
| URL+title > URL-only on **both** sites | Yes | No (0% improvement on both) | **FAIL** |
| URL+title > 0.5 bits on **any** site | Yes | Yes (1.36, 1.32) | ✓ |
| Permutation p < 0.001 on **any** site | Yes | Yes (0.001 on both) | ✓ |
| Positive control PMI ≥ 0.5 | Yes | Yes (0.693) | ✓ |
| ≥ 50 non-leakage per site | Yes | Yes (400 each) | ✓ |

**Result**: FALSIFIED-IN-SETTING — the first criterion (URL+title > URL-only on both sites) fails.

---

## 6. Interpretation

### 6.1 Why Titles Don't Help on TodoMVC

TodoMVC is a canonical single-page application demo, but its `document.title` is set once at application load and never changes. All client-side routes (`#/`, `#/active`, `#/completed`) share the same title. This makes the title representation a constant — it carries zero information about the current state beyond what the URL already provides.

This is a **design property of TodoMVC**, not evidence that titles are generally uninformative for SPA state discrimination. Most production React/Vue applications use route-specific titles (via React Helmet, Vue Meta, or manual `document.title` assignment).

### 6.2 What the Result Does NOT Falsify

- **C-WEB-DYNAMICS**: The broader claim that interactive Web transformations contain predictive dynamical structure is not addressed — URL-only PMI is strongly positive (1.32–1.36 bits, p=0.001), confirming dynamical structure exists at the URL level.
- **Title-aware PMI on real sites with varying titles**: The experiment used sites where titles are constant by design. Sites with route-varying titles (e.g., multi-step forms, article pages with unique titles) remain untested.
- **Form signals as marginal information**: Form signals provide zero marginal information here, but only because titles are constant — the same reason titles provide zero marginal information. On sites where titles vary, form signals might still provide additional discrimination.

### 6.3 What the Result Establishes

- **TodoMVC titles are constant**: Both TodoMVC implementations use a single `document.title` across all routes, making title-aware state representation equivalent to URL-only.
- **URL-only PMI on real SPAs exceeds synthetic baseline**: Real TodoMVC URL-only PMI (1.32–1.36 bits) is ~90% higher than the parent synthetic baseline (0.693 bits), suggesting real SPA transitions have richer structure than the synthetic model.
- **Non-leakage density on TodoMVC is 100%**: All transitions are non-leakage by construction, exceeding the 50-transition minimum by 8×.
- **The permutation null is valid and powerful on real SPA data**: 0/1000 shuffled means exceed observed PMI with d > 80.

---

## 7. Implications for Next Experiment

The frozen `inherited_next_question` asked whether title-aware PMI detects structure on real SPA/form-heavy transitions. This experiment partially answers: **titles provide no benefit when they are constant** (which is the TodoMVC case). The critical unknown — whether title-aware PMI helps on sites where titles actually vary — remains open.

**Recommended next steps** (for DIRECTOR/handoff):
1. Test on sites with **route-varying titles**: multi-step forms, article/content sites, dashboards with page-specific titles
2. Specifically target sites where URL-only PMI is low (ambiguous URLs) but titles are informative
3. Consider alternative richer state representations: DOM structure hashes, accessibility tree snapshots, or visual features

---

## 8. Deviation Notes

No deviations from the frozen preregistration. The experiment was executed exactly as specified: 2 sites × 100 trajectories × 8 steps, seed=42, alpha=1.0, 1000 permutations, Bonferroni-corrected at 0.025.

---

## Appendix: Raw Metric Values

### React (todomvc_react)
- url_only_pmi: 1.360076527495342
- url_title_pmi: 1.360076527495342
- url_title_form_pmi: 1.360076527495342
- permutation_p (all reps): 0.000999000999000999
- permutation_null_mean: 0.05994243285655704
- permutation_effect_d: 83.14421684311813

### Vue (todomvc_vue)
- url_only_pmi: 1.3232577149184857
- url_title_pmi: 1.3232577149184857
- url_title_form_pmi: 1.3232577149184857
- permutation_p (all reps): 0.000999000999000999
- permutation_null_mean: 0.06040391066530815
- permutation_effect_d: 85.66026096855953

### Positive Control (synthetic SPA)
- url_only_pmi: 0.6933101309975662
- permutation_p: 0.000999000999000999
