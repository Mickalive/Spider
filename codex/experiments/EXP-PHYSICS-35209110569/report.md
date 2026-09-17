# EXP-PHYSICS-35209110569 — SPA Corpus Survey for C-WEB-DYNAMICS (EXECUTE report)

**Status:** COMPLETE / **Outcome:** MIXED
**Lane:** physics — **Claim:** C-WEB-DYNAMICS
**Parent:** EXP-PHYSICS-35185288822 (MEASUREMENT_INVALID; structural MPA leakage 78–92%)

Canonical measurements: `result.json` (145 metrics, 5 controls, 15 artifacts).
Derived table: `analysis_results.json`. Raw evidence: `raw_{vanillajs,react,vue,angular,svelte}[_topup].json`,
`raw_wikipedia.json` (+ superseded session 0), `raw_wikipedia_s0fix.json`.
Code: `collect_spa_survey.py`, `analyze_spa_survey.py`.

## 1. What was executed

Frozen design, 5 TodoMVC hash-SPA variants + Wikipedia MPA control, Playwright headless
Chrome, per-transition (url_before/after, title_before/after, action_primitive, resolved
action_target, timestamp). Leakage per frozen definition:
`normalize(target_href) == normalize(url_after)`, normalize = strip fragment,
strip trailing slash, unquote. 7 sessions × 24 actions per SPA (168 raw; exceeds frozen
≥5 sessions / ≥100 minimums to reach validity minimums with executed actions); 5 × 20
link clicks on Wikipedia (100 raw). Zero EPIPE crashes across 40 sessions.

Two documented operational repairs (thresholds/decision rule unchanged):
- Spec URL shorthand mapped to live dist URLs (e.g. `vanillajs` →
  `todomvc.com/examples/javascript-es6/dist/`); same 5 framework variants.
- Wikipedia session-0 hub Main_Page yielded 0/20 successful link clicks (element-discovery
  failure, preserved in `raw_wikipedia.json`); re-ran session 0 on the HTML article hub
  (20/20 success, `raw_wikipedia_s0fix.json`).

## 2. Results vs frozen decision rule

| Check | Frozen threshold | Observed | Pass |
|---|---|---|---|
| ≥1/5 variants leakage <40% + achievable_NL ≥50 | <0.40, ≥50 | **5/5**: 0.213–0.285 valid (0.25 all-raw); NL@500 = 358–394 | YES |
| ≥1/5 variants ≥2 unique titles | ≥2 | **0/5**: all variants unique_titles=1, entropy 0.0 bits | NO |
| Wikipedia leakage >80% | >0.80 | 1.00 (100/100), 5 titles, 100 raw | YES |
| Vanilla JS leakage <60% | <0.60 | 0.2846 valid, 168 raw (130 valid) | YES (titles 1 → control PARTIAL) |
| ≥100 raw per variant | ≥100 | 168 SPAs / 100 wiki | YES |
| ≥5 sessions per variant | ≥5 | 7 SPAs / 5 wiki | YES |

SURVIVES requires all six → **not SURVIVES** (title clause fails 0/5).
FALSIFIED-IN-SETTING's literal clause (0/5 reach <40%) → **not triggered** (5/5 reach it).
Falsifier clause (2) (ALL variants <2 titles) **triggers**. Control/data-quality gating is
satisfied. Verdict: `status=COMPLETE, outcome=MIXED`.

## 3. Mechanism (per-type stratification, mix-free)

On every SPA: `link_click` leakage = 1.00 (170/170 valid; filter links `#/active` etc.
normalize to the same path, so they leak *by the frozen definition*), while
`button_click` / `form_submit` / `js_navigate` = 0.00 (548/548). Leakage is entirely
determined by action type; the 21–28% headline rate reflects the protocol's 27% link
share, not a site constant. Wikipedia: 100% link clicks → 1.00 leakage, consistent with
(and above) the parent's 91.2% on mixed navigation.

## 4. Interpretation (kept separate from observations)

- **Leakage half SUPPORTED:** hash-SPAs with a realistic non-link action mix achieve
  21–28% leakage; 50 NL transitions need only ~64–70 raw transitions (vs 625 at 92% MPA
  leakage). The SPA pivot is justified **for URL-level NL collection**.
- **Title half FALSIFIED in this setting:** `document.title` is constant on all 5
  variants (840 SPA transitions, one title each), so title-aware PMI is untestable on
  TodoMVC — replicating the EXP-PHYSICS-34266105229 degeneracy. The pipeline is not at
  fault (same code records 5 distinct Wikipedia titles).
- Product consequence: target these TodoMVC variants for URL-level PMI at NL scale, but
  do **not** expect title information there; title-aware PMI needs title-varying
  production SPAs (still unidentified) or a non-title state representation.

## 5. Validity threats / limits

Action-mix dependence (above); TodoMVC demos ≠ production (no auth, single input, hash
routing only; history routing untested); error-transition exclusion documented with
all-raw sensitivity (never crosses 0.40); control-label swap between prereg §4 and
spec.json/decision_rule (packet follows spec.json keys); single-day collection, no
model calls.

## 6. Unresolved

Title-varying production SPA not identified; history-routed SPA leakage untested;
per-URL title variance untested. Next: survey production SPAs (e.g. React-Router
history SPAs) for joint (low-leakage, varying-title) sites before any title-PMI design.
