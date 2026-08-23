# WP-003 PREREGISTRATION — Website-Holdout Universality of Transition Structure

Frozen before data collection and analysis. 2026-08-23, SPIDER Team Physics.
This experiment follows §28 (universality requires TRUE WEBSITE holdout),
§29 (semantic ablation), §31 (strong nulls), §37-39 (verdicts, freezing,
independence levels).

## 1. Hypothesis (H3)

There exists a mechanics-only representation Z of interactive Web states such
that the mapping Z(state) → next-action-class generalizes ACROSS websites:
a predictor trained on K−1 websites predicts held-out-website transitions
better than strong non-memorization nulls.

If no such Z exists at this granularity, universal Web physics (in the
minimal predictive sense) is falsified for this representation family.

## 2. Data (collected AFTER this freeze)

Random-walk interaction traces on 6 distinct live websites (distinct
hosts/apps): books.toscrape.com, quotes.toscrape.com,
the-internet.herokuapp.com, en.wikipedia.org (article-space only),
news.ycombinator.com, openlibrary.org. Uniform-random action selection over
internal actionable elements incl. typed form interactions; event-driven
snapshots (no fixed-cadence segmentation); target ≥90 transitions/site;
fresh anonymous context per site walk.

## 3. Representation Z (frozen, semantics-ablated)

Per-state numeric vector, NO text content, NO site identifiers, NO URL
tokens beyond coarse shape:
link-count bucket [0-9,10-49,50+], button bucket [0,1-3,4+], text-input
bucket [0,1-3,4+], password-field present, select present, checkbox present,
file-input present, textarea present, form-count bucket [0,1,2+],
url-path-depth bucket [0-1,2-3,4+], query-param bucket [0,1,2+],
login-capable (=has password), internal-link-ratio bucket.

Target variable A: next primitive action class ∈ {click_link, click_button,
fill_text, fill_password, select_option, check_box, submit}.
Target variable B (secondary): next-page structural class = tuple bucket
(depth, has-password, link-bucket, input-bucket).

## 4. Unit / holdout level

Unit of analysis: transition. Holdout level: WEBSITE (leave-one-site-out,
6 folds). Transitions never mix across folds. This is website holdout per
§28, not trajectory holdout.

## 5. Models and nulls (frozen)

- M1: multinomial logistic regression (L2, deterministic) on Z, trained on
  K−1 sites.
- N0: global majority-class (action frequency).
- N2: global first-order Markov on previous action class.
- N4: 1-nearest-neighbour in standardized Z against pooled training
  transitions (retrieval/memory baseline per WP-002B lesson).
- S0: label-shuffle within held-out site (500 permutations) → chance
  distribution given site marginals.
- Site-frequency control: report per-site base rates; M1 must beat the
  best null WITHIN each fold, not merely on average (guards against
  frequency artifacts).

## 6. Primary metric & falsification condition (frozen)

Primary: balanced accuracy of target A on held-out site, averaged over 6 LOO
folds (macro over classes, classes weighted equally).

VERDICT RULES (frozen):
- If mean(M1) − mean(best null ∈ {N0,N2,N4}) has bootstrap 95% CI entirely
  above 0 AND M1 beats best null in ≥4/6 individual folds:
  → SURVIVES_CURRENT_TEST (transferable mechanical structure exists at this
    granularity; NOT proof of deeper physics).
- If CI includes 0 or ≤0: → FALSIFIED for representation family Z.
- If <45 usable transitions/site collected: → DATA_INSUFFICIENT (no claim).
- Collection failure of ≥2 sites before freeze-exempt minimum: rerun once;
  else DATA_INSUFFICIENT.

## 7. Secondary (exploratory, cannot rescue primary)

- Target-B prediction (structural next-page class).
- Permutation importance over Z dims (structural concentration expected if
  H3 true).
- Confusion structure: which action classes transfer vs site-locked.
- load_ms distributions per site (descriptive only; characteristic-time
  claims deferred to WP-004).

## 8. Expected direction & honest priors

Prior from WP-001/WP-002B: mechanical signal slightly above shuffle exists
in-distribution (+0.05 dim-acc) but NN retrieval matched rules in-distribution.
Cross-SITE transfer is genuinely untouched; prior probability of clear
survival judged low-to-moderate (~0.35). A FALSIFIED result here is
informative: it would localize all observed predictability to memory +
site-specific regularity.
