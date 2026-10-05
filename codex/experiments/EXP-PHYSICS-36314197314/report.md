# EXP-PHYSICS-36314197314 - EXECUTE report

- Lane: `physics`; claim under test: `C-WEB-DYNAMICS` (does the real interactive Web carry
  predictive structure beyond memory and ordinary similarity, at the coarsest level of
  description, on real sites?)
- Frozen packet: `request.json`, `spec.json`, `prereg.md`, `freeze.json` (verified byte-identical
  before and after collection; see `raw/frozen_input_verification.json`).
- Producer status: **status = `MEASUREMENT_INVALID`**, **outcome = `NOT_APPLICABLE`** (frozen prereg s13 branch
  selected; see Decision below). This is not a claim that the Physics domain or `C-WEB-DYNAMICS`
  is closed.
- Collection was REAL: 226 credential-free HTTP GETs, 226 with `transport_ok=true`,
  0 transport failures, 0 model calls, 0 browser, 0 Docker, no frontier WebEagle stack.

## 1. What was actually measured

- Origin pool actually measured: 6 credential-free public origins
  (`api.agify.io`, `api.github.com`, `api.genderize.io`, `api.nationalize.io`, `ifconfig.me`,
  `randomuser.me`). The prereg freezes no origin list and `freeze.json` does not hash the
  `frozen_origins.json` it defers to, so this pool is an executor construction (validity note
  V-A), constrained by the director mandate to exclude every host in the current graph and
  frontier host sets. The five excluded hosts were NOT probed, so no request was spent on them.
- 224 transitions: 158 TRAIN / 66 held-out TEST, over 15 action templates
  (20 binding values each, last 30% of the sorted values held out) and 5 test sites.
  Every held-out binding value and every held-out URL is absent from TRAIN (gate V1).
- Held-out substrate, template by template (`n_tr` = TRAIN cases available for that template):

| template (sorted by abs delta vs B1) | test | n_tr | statuses | body bytes | distinct bodies | trunc | treatment log score | delta vs B1 |
|---|---|---|---|---|---|---|---|---|
| `api.github.com::/repos/{id_1}/{id_2}\|{id_2}` | 6 | 14 | 404 | 118-118 | 1 | 0 | -0.272 | +0.1301 |
| `api.github.com::/users/{id_0}\|{id_0}` | 6 | 14 | 200,404 | 89-1287 | 4 | 0 | -6.200 | +0.0434 |
| `randomuser.me::/api/\|{exc}` | 6 | 14 | 200 | 912-1203 | 6 | 0 | -7.777 | +0.0000 |
| `randomuser.me::/api/\|{nat}` | 6 | 14 | 200 | 1128-1208 | 6 | 0 | -7.777 | +0.0000 |
| `randomuser.me::/api/\|{seed}` | 6 | 14 | 200 | 1149-1185 | 6 | 0 | -7.777 | +0.0000 |
| `api.genderize.io::/\|{name}` | 6 | 14 | 200,429 | 33-72 | 5 | 0 | -6.376 | +0.0000 |
| `randomuser.me::/api/\|{results}` | 6 | 14 | 200 | 1182-336603 | 6 | 3 | -7.777 | +0.0000 |
| `api.agify.io::/?name=Alex\|{country_id}` | 6 | 14 | 429 | 33-33 | 1 | 0 | -0.104 | +0.0000 |
| `api.agify.io::/\|{name}` | 6 | 14 | 429 | 33-33 | 1 | 0 | -0.104 | +0.0000 |
| `api.genderize.io::/?name=Alex\|{country_id}` | 6 | 14 | 429 | 33-33 | 1 | 0 | -0.104 | +0.0000 |
| `ifconfig.me::/headers/{id_0}\|{id_0}` | 6 | 14 | 404 | 9-9 | 1 | 0 | -0.104 | +0.0000 |

- State representation (frozen s4): a 15-component response signature - 10 discrete
  (status code, MIME, cache-control class, `body_sha256[:8]`, Location/ETag/Set-Cookie
  presence, is_html/is_json/has_form) and 5 continuous (body length, Content-Length, form-action,
  link and script counts).

## 2. Absolute predictive performance (not relative)

| arm | log_score_categorical (nats) | brier_categorical | log_density_joint (nats) | mean_sq_std_residual |
|---|---|---|---|---|
| `TREATMENT_INHERITED_MECHANISM` | -4.0340 | 0.0734 | +34.208 | 0.0497 |
| `B1_MARKOV_1ST_ORDER` | -4.0497 | 0.0736 | +33.985 | 0.0576 |
| `B2_TFIDF_K5_RETRIEVAL_STRONG` | -5.7956 | 0.0946 | +31.732 | 0.0752 |
| `B2_TFIDF_K5_RETRIEVAL_PREREG_LITERAL` | -5.9386 | 0.1023 | +31.619 | 0.0777 |
| `B3_COLD_RERIVATION` | -9.1361 | 0.2996 | +23.001 | 0.3929 |
| `NC_PLACEBO_PERMUTED_MECHANISM` | -13.1453 | 0.3243 | +15.469 | 0.2387 |

All arms are keyed on `(site, action_template)`. The mechanisms actually selected per template,
with their TRAIN-only leave-one-identifier-out guard confidences, are in
`derived/mechanism_pool.json`.

## 3. Contrastive reading: treatment minus each baseline

| contrast | observed | site-clustered 95% CI | p (trajectory-grouped) | p (site-grouped) | favourable |
|---|---|---|---|---|---|
| `DELTA_LOG_SCORE_CATEGORICAL_B1_MARKOV_1ST_ORDER` | +0.0158 | [+0.0000, +0.0521] | 0.0002 | 0.0001 | yes |
| `DELTA_LOG_SCORE_CATEGORICAL_B2_TFIDF_K5_RETRIEVAL_STRONG` | +1.7616 | [+0.3123, +2.9595] | 0.0546 | 0.0001 | yes |
| `DELTA_LOG_SCORE_CATEGORICAL_B3_COLD_RERIVATION` | +5.1021 | [+4.0907, +6.8966] | 0.0001 | 0.0001 | yes |
| `DELTA_BRIER_CATEGORICAL_B1_MARKOV_1ST_ORDER` | -0.0002 | [-0.0007, +0.0000] | 0.0011 | 0.0001 | yes |
| `DELTA_BRIER_CATEGORICAL_B2_TFIDF_K5_RETRIEVAL_STRONG` | -0.0212 | [-0.0503, -0.0043] | 0.0781 | 0.4284 | yes |
| `DELTA_BRIER_CATEGORICAL_B3_COLD_RERIVATION` | -0.2262 | [-0.3761, -0.1754] | 0.0002 | 0.0001 | yes |

Placeholder-boilerplate-check: 201 independent permutations of the mechanism pool give
201 distinct placebo scores; the treatment beats **0/201** of
them, and the best placebo equals B1 exactly (as it must: a placebo permutation that assigns no
mechanism to any group *is* the no-mechanism predictor). The placebo is a different object from
the treatment, not a relabeling: it differs from the treatment on 30/66 held-out cases
(gate V7).

## 4. Controls

| control | frozen expectation | observed | status |
|---|---|---|---|
| `PC_PLANTED_MECHANISM` | detected (s13: lpd > -0.5 nats, Brier < 0.1) | log_score_categorical -0.1231, log_density_joint +41.334, Brier 0.000244 | **PASS** |
| `NC_PLACEBO_PERMUTED_MECHANISM` | not significantly above any baseline | -13.1453 nats, 0.3243 Brier, p(placebo > B3) = 1.0000; treatment - placebo = +9.1113 nats | **PASS** |
| `NC_INDEPENDENT_IID` | no structure (literal: at or below B3) | treatment -4.6737 vs B3 -6.9009 vs per-site oracle -2.8696 | **FAIL** (see 6) |

## 5. Decision (prereg s13, formal)

| # | condition | value |
|---|---|---|
| 1 | treatment beats B1/B2/B3 on log score | True |
| 2 | treatment beats B1/B2/B3 on Brier | True |
| 3 | site-clustered 95% CI excludes zero for all six deltas | False |
| 4 | trajectory-grouped p < 0.05 for all six deltas | False |
| 5 | site-grouped p < 0.05 for all six deltas | False |
| 6 | positive control detected (s13: lpd > -0.5 and Brier < 0.1) | True |
| 7 | placebo not detected (p > 0.05 vs every baseline, both metrics) | True |
| 8 | i.i.d. null returns no structure (literal s13 criterion) | False |

Frozen branch selected: **MEASUREMENT_INVALID / NOT_APPLICABLE**. s13 routes any failure of conditions 6-8 to
MEASUREMENT_INVALID, and that branch is evaluated before the conditions 1-5 FALSIFIES branch
because a control failure means the comparison itself is not interpretable. Condition 8 is the
single failing control.

Two independent reasons the ACCEPT branch was unreachable, both preserved in
`derived/decision_readings.json`:

1. Condition 3 fails on all four B1 contrasts, and conditions 4/5 fail on the B2 contrasts.
   B1: every site-clustered interval has an endpoint at *exactly* zero -
   `DELTA_LOG_SCORE_CATEGORICAL_B1_MARKOV_1ST_ORDER` = [1.163e-16, +0.0521],
   `DELTA_BRIER_CATEGORICAL_B1_MARKOV_1ST_ORDER` = [-0.0007, 0.000e+00],
   `DELTA_LOG_DENSITY_JOINT_B1_...` = [0.000e+00, +0.4060],
   `DELTA_MEAN_SQ_STD_RESIDUAL_B1_...` = [-0.0166, 1.096e-33].
   The lower endpoints of the log-score and joint-density contrasts are 1.16e-16 and 0.0: the
   contrast is *identically* zero in every site resample that omits `api.github.com`, and only
   `api.github.com` carries the effect. The interval therefore touches zero rather than clearing
   it, and floating-point dust at the 1e-16 level is explicitly not allowed to satisfy a frozen
   condition (endpoints are recorded verbatim in `derived/bootstrap_cis.json`; the tolerance rule
   is in `analyze_36314197314.py`, `excludes_zero_favourable`). In plain terms: **the mechanism
   increment over Markov memory is not separable from zero by a site-clustered interval, because
   it lives in one of five held-out sites.**
   B2: `DELTA_BRIER_CATEGORICAL_B2_TFIDF_K5_RETRIEVAL_STRONG` has p = 0.0781
   (trajectory-grouped) and 0.4284 (site-grouped), and
   `DELTA_LOG_SCORE_CATEGORICAL_B2_TFIDF_K5_RETRIEVAL_STRONG` has p = 0.0546 under the
   conservative within-site null.
2. Condition 8 fails on the i.i.d. control.

Under the alternative precedence reading (conditions 1-5 dominating), the outcome would be
`FALSIFIES` rather than `MEASUREMENT_INVALID`. Both readings agree that no acceptance is licensed.

### Scientific bottom line, independent of the branch

The treatment beats all three baselines in the favourable direction on both primary metrics, but
its increment over the **strongest** baseline (B1, first-order Markov on `(URL, action)`) is
+0.0158 nats (-0.000206 Brier) - about 0.39% of the treatment's own log-score
magnitude, while being statistically detectable (p_trajectory = 0.0002). The large increments
over B2 (+1.762) and B3 (+5.102) are **not** evidence of mechanism semantics: the frozen
i.i.d. control reproduces them with no mechanism reading at all. On i.i.d. responses drawn from
the per-site marginal, the treatment scores -4.6737 nats against B3's -6.9009 - while
being *worse* than the per-site marginal oracle, the strongest possible predictor of that
generator (-2.8696). Site-conditioned memory, not mechanism semantics, is what the large
margins buy.

**The increment is also almost entirely localised.** Of the 66 held-out cases, the treatment
differs from B1 on only **12** of them, on **100.0%** of the total B1 gain, all of them in
2 template(s) on `api.github.com`:

| template where treatment != B1 | test | statuses | delta vs B1 |
|---|---|---|---|
| `api.github.com::/repos/{id_1}/{id_2}\|{id_2}` | 6 | 404 | +0.1301 |
| `api.github.com::/users/{id_0}\|{id_0}` | 6 | 200,404 | +0.0434 |

Every other held-out template gives delta = 0 exactly, because there the frozen mechanism
selection returns the same predictor as the Markov baseline. The sites that contribute nothing are
exactly the sites where every response is a constant 429 or a constant 200: with one body and one
status, there is no structure for any mechanism to add.

The honest reading of this run: **on this substrate and at this representation, mechanism-conditioned
inheritance adds a small (+0.0158-nat), statistically reliable, and almost entirely
single-site increment over site-conditioned Markov memory, and nothing beyond it.** That is compatible with `C-WEB-DYNAMICS` remaining a HYPOTHESIS; it is not a
falsification of the claim, and it is not a validation.

## 6. The failing control is a control-design defect, not a hallucinating predictor

`NC_INDEPENDENT_IID` draws responses i.i.d. **from each site's TRAIN marginal** (s9.3) and then
requires every predictor to perform at or below **B3, a global cold re-derivation** (s13
condition 8). Any predictor keyed on `(site, action_template)` - which s8.2 *requires* of B1, and
which the treatment inherits by construction - must beat B3 on per-site-generated data, with or
without any mechanism reading. The criterion therefore cannot separate the two. This is derivable
from the frozen text alone, before any measurement, and it is recorded as derivation D10 and
validity note V-D. The measured result is consistent with that reading: the treatment loses to the
per-site marginal oracle on exactly the data where it "wins" against B3.

## 7. Instrument defects found (two are pre-execution-detectable)

0. **The effect this experiment was built to detect is carried by one origin (V-N).** The
   treatment differs from B1 on 12 of the 66 held-out cases, all in `api.github.com`, and is
   *exactly* the same predictor as B1 on the other 9 templates. Every site-clustered
   interval for the B1 contrasts therefore has an endpoint at exactly zero. Any interpretation
   of the +0.0158-nat increment is a statement about `api.github.com`, not about the Web.
1. **s9.1's positive-control threshold is unattainable by construction.** With the frozen
   10-component discrete signature and EPS = 0.02, the maximum log score any predictor can attain
   is `10*log(1-EPS)` = **-0.2020 nats**, so the frozen `> 2.0 nats` criterion can never be
   met (s13's `> -0.5` is met, at -0.1231). The two thresholds also contradict each other
   inside one frozen file (D3, V-C).
2. **s13 condition 8 is confounded as described in section 6** (D10, V-D).
3. `pilot_data.json` and `power_calculation.json` are listed as frozen artifacts in s12/s15 and do
   not exist; the tabulated pilot log densities (-2.34 / -1.87 nats) are outside the attainable
   range of the frozen metric, so the power calculation cannot be audited and appears to describe
   a different metric (V-B).
4. prereg s10.1 does not fix which training sample sets the Silverman bandwidth, and the joint log
   density has no bandwidth-free zero point, so the absolute thresholds are not well defined on it
   (D2, V-E). Reported metric: bandwidth-free proper scores primary, joint density with an explicit
   rule and a 4-point bandwidth sweep, under which the sign of every joint-density contrast is
   invariant.
5. Power: 5 sites and 66 held-out cases against a calculation assuming 20 sites and
   ~900 cases; 118 distinct site-resample compositions in 1000 bootstrap draws (V-F).
6. Rate limiting: `api.agify.io` answered every request with HTTP 429 and `api.genderize.io`
   answered 25 of 35, so 2 of 5 test sites contribute only rate-limit responses (V-G).
7. `api.publicapis.org` is marked `in_pool: true` in `frozen_origins.json` but is absent from
   `frozen_pool_eTLD1`; it had no resolvable DNS at screen time (unresolved).

## 8. Validity gates (prereg s14)

| gate | result | evidence |
|---|---|---|
| `V1_TARGET_INTEGRITY` | PASS | no held-out URL or binding value occurs in TRAIN: 0 URL leaks, 0 binding leaks across 66 held-out cases |
| `V2_SPLIT_INTEGRITY` | PASS | holdout is identifier level (66 held-out bindings, none seen in training); TF-IDF vocabulary fit on TRAIN documents only (158 training documents); no site-identity feature enters any predictor; log1p standardization statistics fit on TRAIN only |
| `V3_SAMPLING_INTEGRITY` | PASS | collection seed 232890113, analysis seed 232890113, both derived from request_hash as prereg s16 requires; mechanism selection is a documented TRAIN-only leave-one-identifier-out rule, fully separated from the HTTP environment |
| `V4_UNCERTAINTY_INTEGRITY` | PASS | 10000 trajectory-within-site and 10000 site-grouped permutations; 1000 site-clustered bootstrap resamples over 118 distinct site compositions; no injected noise |
| `V5_REPRESENTATION_INTEGRITY` | PASS | all 226 raw responses archived in raw/collection_log.jsonl with full body length and full SHA256; 17 bodies exceed the 4096-byte archive cap, so form/link/script counts are lower bounds for those (D8) |
| `V6_POSITIVE_CONTROL_REACHABLE` | PASS | PC log_score_categorical -0.1231, log_density_joint 41.3339, Brier 0.000244 |
| `V7_PLACEBO_CONTROL_SPECIFIC` | PASS | placebo differs from the treatment on 30/66 held-out cases and takes 201 distinct values across 201 permutations, so it is a permuted mechanism object rather than a count-preserving relabeling of the treatment |
| `V8_IID_NULL_CALIBRATED` | **FAIL** | treatment_minus_B3 on the i.i.d. null = +2.2272 nats (log_score_categorical), significant under the frozen criterion; treatment_minus_per_site_oracle = -1.8042 nats |
| `V9_INFRASTRUCTURE_FAILURE_BELOW_50PCT` | PASS | 0 of 224 transitions had transport_ok=false (0.0000); missing ledger entries 0 |
| `V10_POOL_SAMPLE_MEETS_PREREG` | **FAIL** | prereg s7.1 asserts 25 origins / 12 unique; the mandate's host disjointness left 7 reachable candidates of which 6 responded; the measured test sample is 66 held-out cases on 5 sites against a power calculation that assumed 20 sites and roughly 900 held-out cases (prereg s12) |

## 9. Representation loss and substrate caveats

- 17 of 224 bodies exceeded the 4096-byte archive cap. `body_length` and
  `body_hash_prefix_8` are computed on the FULL body (exact length and full SHA256 archived), but
  `has_form`, `form_action_count`, `link_count` and `script_count` are computed on the prefix and
  are lower bounds for those responses (V-H).
- The Web is live: a rerun of the collection step would not reproduce byte-identical signatures.
  The analysis, by contrast, is exactly reproducible from the archived ledger with the recorded
  seeds (V-L, and `provenance.json`).
- Templates were discovered from paths observed live on the retained hosts, so both the site
  sample and the template sample are conditioned on what those hosts expose (D5, V-J).

## 10. What this run does NOT establish

- It does not establish cross-site mechanism transfer: every arm is site-keyed, so the mechanism
  library is site-local by construction (V-I). The mandate's disjoint-host-set clause is a pool
  disjointness, not a held-out-site test.
- It does not establish cross-origin generality: the entire measurable mechanism increment comes
  from one origin (V-N), and the four mandate-excluded hosts that expose 200/404-varying
  identifier templates were never available to test it on.
- It does not establish that `C-WEB-DYNAMICS` is false. The frozen decision rule's
  MEASUREMENT_INVALID branch applies, and per AGENTS.md that closes neither the claim nor the
  domain.
- It does not license promoting inherited-mechanism conditioning into Product Core: the increment
  over site-conditioned Markov memory is +0.0158 nats, and the apparent large wins are
  attributable to site conditioning.
- Do not read the ACCEPT-adjacent numbers (treatment ahead of all three baselines) as support:
  the frozen accept branch requires ALL of conditions 1-8, and three of them fail.

## 11. Reproduction

```bash
cd research/experiments/EXP-PHYSICS-36314197314
python3 verify_frozen_inputs.py                 # frozen digest check
python3 execute_36314197314.py --stage collect  # 226 real GETs -> raw/collection_log.jsonl
python3 execute_36314197314.py --stage analyze  # same chain via the stage runner
python3 analyze_36314197314.py --selftest      # reruns the analysis; derived/ must be identical
python3 verify_result_36314197314.py           # independent post-hoc checks (20/20 pass)
```

`verify_result_36314197314.py` deliberately shares no scoring code with the analyzer. It
re-derives the response signatures from the raw HTTP ledger, replays the seeded holdout rule,
recomputes every primary contrast as the mean of per-case differences (a different order of
operations from the analyzer's difference of means), re-checks the permutation p-values against
the (1+k)/(1+10001) rule, re-executes the frozen s13 decision arithmetic, and re-hashes every
artifact. It is a self-check, not an independent audit.

The frozen prereg's stated command `python run_experiment.py --experiment
EXP-PHYSICS-36314197314` does not exist in the frozen packet; `execute_36314197314.py` is the
executor that actually ran, and the deviation is recorded in `provenance.json`. Analysis wall time
is about 9 s including 20,000 permutations and 1000 bootstrap resamples.

## 12. Artifacts

Raw evidence: `raw/collection_log.jsonl` (every response), `raw/transitions_index.json` (split and
provenance of every transition), `raw/screen_reachability.json`, `raw/request_ledger_summary.json`,
`raw/frozen_input_verification.json`, `raw/template_inventory.json`. Derived:
`derived/metrics.json`, `derived/controls.json`, `derived/validity_gates.json`,
`derived/permutation_nulls.json` + `derived/permutation_nulls_primary.jsonl` (full null vectors for
the six primary contrasts), `derived/bootstrap_cis.json`, `derived/mechanism_pool.json`,
`derived/predictions.jsonl`, `derived/baseline_predictions.jsonl`,
`derived/control_predictions.jsonl`, `derived/response_signatures.jsonl`, `derived/split.json`,
`derived/per_template_metrics.json`, `derived/decision_readings.json`,
`derived/power_realisation.json`. Code: `execute_36314197314.py`, `analyze_36314197314.py`,
`verify_frozen_inputs.py`, `verify_result_36314197314.py`. Exact SHA-256 digests for all of these are in `result.json.artifacts`
and `provenance.json`.
