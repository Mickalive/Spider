# WP-003 REPORT — Website-Holdout Universality of Transition Structure

**Verdict: FALSIFIED** (for the preregistered representation family Z and
target A). Date: 2026-08-23. Data: `data/manifests/wp003_dataset_manifest.json`,
results: `results/physics/wp003_results.json`.

## What was tested

H3: a mechanics-only state representation Z (13 bucketed structural features,
no text/site identity) lets a model trained on K−1 websites predict
next-action-class on a held-out website better than strong non-memorization
nulls. Frozen protocol: `reports/physics/wp003_preregistration.md`
(written before data collection; seed-frozen collector).

## Data

Random-walk interactions (uniform over internal actionable classes incl.
typed forms), event-driven snapshots, 7 distinct hosts:
books.toscrape(90), quotes.toscrape(90), the-internet(48),
wikipedia(90), news.ycombinator(90), openlibrary(59), gutenberg(90).
557 usable transitions; every site ≥45 usable (frozen minimum).

## Result (primary metric: balanced accuracy, LOO website holdout)

| fold | M1 | N0 freq | N2 Markov | N4 NN | shuffle μ |
|---|---|---|---|---|---|
| books | 0.500 | 0.500 | **1.000** | 0.475 | 0.500 |
| gutenberg | 0.384 | 0.333 | **0.833** | 0.346 | 0.335 |
| hackernews | 0.345 | 0.333 | **0.967** | 0.313 | 0.333 |
| internet | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| openlibrary | 0.474 | 0.500 | **1.000** | 0.441 | 0.500 |
| quotes | 0.494 | 0.250 | **0.500** | 0.216 | 0.250 |
| wikipedia | 0.333 | 0.333 | 0.667 | 0.652 | 0.333 |

- mean(M1 − best null) = **−0.348**, bootstrap CI [−0.363, −0.333]
- fold wins: **0/7** (frozen requirement was ≥4/7-equivalent wins + CI>0)
- → frozen verdict rule fires **FALSIFIED**, not merely inconclusive.

## Interpretation (narrow, per §30 red-flag discipline)

1. The interactive Web's next-ACTION-class dynamics, under an unbiased
   interaction policy, are almost fully captured by a ONE-SYMBOL memory
   (previous action class) that is itself UNIVERSAL across sites. This is a
   real cross-site regularity — but it is shallow sequence statistics, not
   state-driven mechanics: adding 26 structural state dims contributed zero
   transferable information (in fact hurt via overfitting to train-site
   quirks).
2. Consistent with prior WP-002B: whatever mechanical signal exists
   in-distribution does NOT survive website holdout against even trivial
   nulls. The burden of proof for "Web physics" shifts to phenomena that
   beat BOTH memory AND trivial Markov structure under true site holdout.
3. Quotes fold nuance: M1 (0.494) beat N0/N4 there — form-flow states carry
   some genuine structural signal locally — but still lost to the global
   bigram null. No fold rescue.

## Scope limits (what this does NOT falsify)

- Falsified claim is specific: transferable structure of
  Z→next-action-class at transition granularity under unbiased policy.
- NOT falsified: attractors/barriers/metastability (state-region phenomena),
  timing physics (load_ms data collected, unanalyzed), goal-directed-policy
  dynamics (a purposive agent breaks the uniformity that made N2 dominant —
  its dominance is partly a property of OUR sampler, and this is stated as
  a policy-sensitivity threat, not hidden), coarser/finer representations,
  next-PAGE-structure prediction (secondary target B, unanalyzed this run).

## Measurement validity log (§37 honesty)

- Run 1 dataset INVALIDATED pre-analysis: collector emitted semantic action
  kinds unknown to the browser driver ⇒ every recorded "transition" was a
  failed no-op. Detected by invariant check (100% ok=False); discarded;
  fixed; recollected. Kept on disk as *_INVALID_run1 for provenance.
- Hackernews walk degraded twice (auth-walled dead ends yielding empty
  snapshots) → dead-state hop-to-home recovery added; final HN sample clean.
- One infrastructure hang (blocking dialog) → browser-level timeouts +
  dialog auto-dismiss + per-site subprocess isolation with hard caps.
- Deviation from frozen plan: 6 sites planned, 7 collected (gutenberg
  substituted when HN initially degraded; both retained). No analysis-side
  deviations; verdict rule applied exactly as frozen.

## Next discriminating tests (Team Physics queue)

1. WP-004: committor/barrier analysis on authenticated-regime transitions
   (quotes/the-internet login walls): q(x)=P(reach authenticated region
   before anonymous home) via Monte-Carlo restarts; barrier signature =
   sharp q-gradient vs degree-preserving graph null. (Data partially in hand.)
2. Target B (next-page structural class) with SAME corpus — checks whether
   STATE change is predictable even though ACTION choice isn't.
3. Policy-sensitivity control: repeat WP-003 under goal-directed sampling;
   if N2 dominance collapses, rerun primary test.
