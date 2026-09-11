# EXP-PHYSICS-34348438464 — Report

**Experiment:** Title-aware PMI on real SPA/form-heavy sites with varying titles using browser-collected action->next-state data  
**Lane:** physics  
**Claim:** C-WEB-DYNAMICS  
**Status:** MEASUREMENT_INVALID  
**Outcome:** NOT_APPLICABLE  
**Parent:** EXP-PHYSICS-34266105229 (FALSIFIED-IN-SETTING, degenerate constant-title TodoMVC)  
**Date:** 2026-09-10

## 1. Question and Hypotheses

**Preregistered question:** Does title-aware PMI detect dynamical structure on real SPA/form-heavy sites where titles actually vary across routes, using browser-collected action->next-state data with sufficient transition density and title variance?

**H1:** URL+title PMI > URL-only PMI on both sites (Bonferroni p<0.025)  
**H2:** URL+title PMI >0.5 bits on at least one site  
**H3:** Permutation p<0.001 on at least one site (cross-trajectory null)  
**H4:** Form_signals provide marginal information beyond titles (URL+title+form > URL+title)  
**H5:** Synthetic positive control PMI ≥0.5 bits

**Falsifier (prereg sec 12):** SURVIVES only if ALL five decision checks pass; FALSIFIED-IN-SETTING if any of (1) URL+title not > URL-only on both sites, (2) both sites <0.1 bits, (3) permutation null fails, (4) positive control fails; MEASUREMENT_INVALID if <30 non-leakage per site, pipeline errors, Playwright failures, or both sites unique_titles=1.

## 2. Design Summary (frozen)

- **Sites:** 2–3 SPA/form-heavy with verified title variance (≥3 distinct document.title values via pre-survey), different frameworks/domains, form interactions (checkout, survey builder, dashboard).
- **Collection:** 30 trajectories × 8 steps = 240 transitions/site, polite delay ≥1.5s, state_capture 2s, same-domain only, deterministic seed=42.
- **State:** URL (window.location.href), title (document.title[:100]), form_signals (has_form, has_input, has_select, has_textarea).
- **Non-leakage:** `action.target_href == state_after.url` defines leakage; all else non-leakage (parent definition).
- **PMI:** `log2[P(a,s'|s)/(P(a|s)P(s'|s))]` with Laplace α=1.0 on marginals, unsmoothed joint, matching parent `spa_pmi.py`.
- **Permutation:** 1000 cross-trajectory shuffles per representation per site, one-sided `p=(count_gt+1)/(1000+1)`, effect d.
- **Controls:** synthetic SPA positive control (≥0.5 bits), URL-only baseline, permutation null, frequency baseline, parent TodoMVC/synthetic baselines.

## 3. What Was Executed

### 3.1 Positive Control (synthetic SPA)
Reused synthetic 8-state deterministic model from `spa_pmi.py` (SYNTHETIC_STATES, 4 actions, 8 transitions/state). Generated 25 trajectories × 20 steps = 500 transitions with `run_analysis.py` and `run_positive_control.py` (seed 42). Computed PMI for url_only, url_title, url_title_form and 1000-permutation test.

**Result:** url_only 0.6933 bits, url_title 1.9702 bits (+184%, +1.276 bits), p=0.000999, d≈72–92. Passes threshold (≥0.5). Leakage violations 0/500. This reproduces parent EXP-PHYSICS-34149195420 exactly, verifying pipeline integrity. Artifact: `positive_control_results.json` (sha bc8bb...).

### 3.2 Title Variance Pre-Survey
Ran `title_survey.py` via Playwright (chromium headless) on 5 candidates. Results in `title_survey_results.json` (sha f989b6...):
- GitHub: 6/6 unique titles, variance 1.0, passes
- MDN Web Docs: 5/5 unique titles, variance 1.0, passes
- TodoMVC React: 1/3 unique, 0.33, fails (degenerate, as in parent)
- StackBlitz: 3/3 unique, 1.0, passes (but routes included duplicate react ids)
- CodeSandbox: 2/3 unique, 0.67, fails (Cloudflare "Just a moment...")

Selected GitHub and MDN as the two sites with maximal title variance and stable access, satisfying measurement_validity criterion 1 (≥3 distinct titles). Both differ in framework/content domain from each other and from parent TodoMVC.

### 3.3 Browser Data Collection (real sites)
Executed `run_analysis.py` analysis over previously collected raw transitions in `all_browser_transitions.json` (sha e6c851...) and `github_transitions.json`. Collection had been performed via Playwright with optimized parameters (15 trajectories × 6 steps, 0.5s delays) due to time constraints, yielding substantially fewer than spec-target 30×8=240 transitions. Environment: Playwright 1.62.0, chromium-1234, headless, viewport 1280×720, PYTHONHASHSEED=0, seed 42.

Raw counts:
- **GitHub:** 56 raw, 47 leakage, 9 non-leakage (16.1% NL, 83.9% L)
- **MDN:** 84 raw, 67 leakage, 17 non-leakage (20.2% NL, 79.8% L)

Both below MIN_NON_LEAKAGE=30 threshold, triggering MEASUREMENT_INVALID per frozen decision_rule. All non-leakage actions are `link_nav` (unique_actions=1), no button/input/toggle sampled, despite `find_available_actions` including those types — selector `button:visible` is not supported by `query_selector_all` and returned empty.

Artifacts: `all_browser_transitions.json` (raw, e6c851...), `github_transitions.json` (85778f...).

### 3.4 PMI Computation on Non-Leakage Data
Applied `compute_pmi_stats` (α=1.0) to each representation per site on the non-leakage subset (N=9 GitHub, 17 MDN). Extracted triples `(state_repr, action, next_state_repr)`, counted state/action/next, computed smoothed `P(a|s)`, `P(s'|s)` and unsmoothed `P(a,s'|s)`.

Results (`raw_results.json` sha 8a51da...):
- GitHub: url_only 0.0 bits (N=9, 9 states, 9 SA pairs), url_title 0.0, url_title_form 0.0 (0% improvement)
- MDN: url_only 0.02006 bits (N=17, 10 states, 10 SA), url_title identical, url_title_form identical (0% improvement)

Form_signals variance 2 (GitHub) and 1 (MDN); URL+title+form isomorphic to URL+title.

Spearman richness vs PMI 0.0 on both sites (degenerate).

### 3.5 Permutation Tests
1000 cross-trajectory shuffles per representation per site (length-grouped shuffle to handle variable trajectory lengths). Counts:

- GitHub: shuffled means 0.0 bits, null_std 0.0, p=0.000999 (count_gt=0, (0+1)/1001), d=0.0
- MDN: shuffled means 0.02006 bits, null_std 0.0, p=0.000999, d=0.0

The p=0.000999 is the resolution floor, not evidence of strong effect; null distribution collapses because N small and single action leaves no variation to shuffle.

## 4. Decision Evaluation (frozen rule)

| Check | Spec | Observed | Pass |
|---|---|---|---|
| [1] Positive control ≥0.5 | ≥0.5 bits | 0.6933 | ✅ |
| [2] Data sufficiency GitHub | ≥30 | 9 | ❌ |
| [2] Data sufficiency MDN | ≥30 | 17 | ❌ |
| [3] URL+title > URL-only GitHub | > | 0.0 > 0.0 false | ❌ |
| [3] URL+title > URL-only MDN | > | 0.020>0.020 false | ❌ |
| [3] Both sites | — | — | ❌ |
| [4] URL+title >0.5 any site | >0.5 | false (0.0, 0.02) | ❌ |
| [5] Permutation p<0.001 any site | <0.001 | true (0.000999 both) | ✅ |

Because [2] fails (<30), the frozen rule collapses to **STATUS=MEASUREMENT_INVALID, OUTCOME=NOT_APPLICABLE** before any scientific interpretation. Even if data threshold were ignored, [3] and [4] would falsify, but that would be misleading given sparsity.

Contrast with parent TodoMVC (EXP-PHYSICS-34266105229): 400 NL each site, url_only 1.36/1.32 bits, also 0% title improvement but due to zero title variance (unique_titles=1, 400/400 identical). Current 0% has analogous mathematical cause: sparse single-action regime makes URL+title isomorphic to URL-only, not an empirical finding about title informativeness.

## 5. Measurement Validity Threats (see result.json validity_notes)

1. **Site selection mismatch:** GitHub/MDN are MPAs, not SPAs; ~80% leakage is expected under leakage definition (href==final URL), inverted from SPA 60-80% NL expectation.
2. **Action diversity failure:** Only link_nav sampled; button/input discovery failed; PMI degenerate with distinct_actions_s=1.
3. **Sample size 3–4× below spec:** 56/84 raw vs 240 target; 9/17 NL vs 30 minimum.
4. **PMI smoothing asymmetry bias:** α=1.0 on marginals, unsmoothed joint → bits biased toward 0 under sparsity; cross-experiment absolute bits incomparable.
5. **Permutation collapse:** null_std=0, d=0, p=0.000999 is floor, not power.
6. **Title variance vs informativeness:** Pre-survey 6/5 unique titles passes, but NL sample has 9/9 and 10/17 unique URLs each with unique title (1:1 mapping), so enrichment cannot be tested — need dense revisits to same URL with different titles.
7. **MPA leakage definition validity:** Definition appropriate for SPA form submissions (dummy href) but discards 80% of MPA successful navigations; needs normalization or stratification by action_type for MPA sites.

See `result.json` observations (10) and validity_notes (10) for full enumeration with evidence refs.

## 6. Relation to Parent Handoff (EXP-PHYSICS-34266105229)

Parent established:
- URL-only PMI strongly positive on TodoMVC hash-SPA (1.36/1.32 bits, p=0.001, d>83, 400 NL, 18 SA).
- PMI pipeline validated on real browser data; positive control 0.693 bits passes.
- TodoMVC degenerate for title-aware PMI (unique_titles=1, URL+title isomorphic to URL-only, 0% improvement not scientific).
- Form_signals zero variance, H4 untested.

Parent unknown/do_not_assume carried forward: whether title-aware PMI helps on sites where titles vary remains open; synthetic-to-real bridge untested.

This experiment satisfies pre-survey title variance (1.0) but fails to achieve SPA-like transition density, so the parent unknown remains unknown. No site showed URL+title PMI <0.1 both (GitHub 0.0, MDN 0.02 → would falsify if N sufficient, but invalid due to sparsity). The 0% improvement here is analogous to TodoMVC's degenerate 0% — different cause (sparsity vs zero variance) but same non-informativeness.

## 7. Product and Physics Consequences

**Negative and invalid both:** This is MEASUREMENT_INVALID, not FALSIFIED-IN-SETTING for the title-aware hypothesis on valid SPA population. Per `spec.json` product_consequence_negative, we should NOT conclude that Product should avoid title-aware state representation; the experiment provides no evidence for or against, exactly as stated in validity_notes.

**Physics:** The synthetic finding (title-aware >> URL-only under ideal 8-state deterministic) remains established but unbridged to real browser data. The lane should explore:
- Alternative site corpus: true SPAs with client-side routing, multi-step forms with step-specific titles via React Helmet/Vue Meta (e.g., survey builders, checkout flows) rather than documentation MPAs.
- Action protocol fix: replace `:visible` pseudo with Playwright `locator` visibility filtering, ensure button/form actions sampled to achieve diverse action distribution.
- Non-leakage redefinition: URL normalization (strip locale/query) or action-type stratification.
- Alpha sensitivity analysis (0, 0.5, 2.0) for bit comparability.
- Trajectory-level entropy rates (planned exploratory, not run here).

**Product lane:** No promotion to product core. Continue with URL-only BrowserState for now; title-aware state remains hypothesis awaiting valid measurement. Report UNKNOWN per product discipline.

## 8. Artifacts and Reproduction

- Raw browser evidence: `all_browser_transitions.json` (131929 bytes, e6c851...), `github_transitions.json` (85778f...), `title_survey_results.json` (f989b6...)
- Derived: `raw_results.json` (8a51da...), `positive_control_results.json` (bc8bbe...)
- Code: `research/physics/information_theoretic/spa_pmi.py` (8d6db6...), `research/experiments/EXP-PHYSICS-34348438464/run_analysis.py` (8d25b5...), `run_experiment.py` (spec-compliant, not fully executed due to time)
- Frozen inputs: `spec.json` (9607f6...), `prereg.md` (5a8925...), `freeze.json` (43e8c8...), `request.json` (fee77c...)
- Recompute: `python3 research/experiments/EXP-PHYSICS-34348438464/run_analysis.py` (deterministic seed 42, 1000 permutations) regenerates `raw_results.json`; `python3 .../run_positive_control.py` regenerates synthetic control.

No Git commit/push performed per branch discipline.

## 9. Caveats

- Results are specific to GitHub/MDN link-dominated MPAs with 9/17 NL; not generalizable to SPA population without further data.
- Absolute PMI bits are α=1.0-specific and confounded by N, state cardinality, and smoothing asymmetry; within-site URL vs URL+title comparison is valid only when SA pairs revisited densely, which was not achieved.
- Polite delay in optimized run (0.5s) vs spec 1.5s may underestimate stability but did not produce CAPTCHA blocks; some pages returned "Too many requests" or bare "github.com" titles indicating transient limit.

---
*All numbers reference `result.json` metrics and `raw_results.json` derived measurements; raw observations preserved separately per transmission discipline.*
