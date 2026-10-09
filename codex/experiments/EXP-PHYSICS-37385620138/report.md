# EXP-PHYSICS-37385620138 — EXECUTE report

**Lane:** physics  ·  **Claim under test:** C-WEB-DYNAMICS (registry status before this run:
`HYPOTHESIS`)  ·  **Stage:** EXECUTE

**Disposition: `status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`.**
The claim's registry status is unchanged. This run produces no admissible evidence for or
against C-WEB-DYNAMICS. It does produce a large amount of admissible evidence about the frozen
measurement apparatus itself, and that evidence is what the Director and AUDIT should read first.

---

## 1. What was run

The frozen interventional effect-factorization design was executed as written: a frozen
variation-coverage screen over credential-free public HTML documents, a baseline fetch plus 15
parameterised probes per candidate, a frozen four-predictor comparison
(`MECHANISM_CONDITIONED` against `B_COMBINED_NULL`, with `B_CACHE_REVALIDATION` and
`B_SITE_TEMPLATE_MEMORY` as component nulls), a site-clustered bootstrap, the frozen
`NC_PERMUTED_MECHANISM` null, and `PC_KNOWN_PARAMETER_EFFECT` on a local server with known
ground truth.

| | |
|---|---|
| frozen inputs verified | 3 of 3 hash-match `freeze.json`; `master_seed = 445086315` |
| collection requests archived | 2896 (0 transport errors) |
| candidates curated / screened / admitted | 189 / 181 / 6 |
| sites admitted | 6 (frozen requirement: >= 20 admitted sites) |
| positive control | 20 pseudo-sites, 360 requests, 90 held-out instances |
| analysis | deterministic, 10000 site-clustered resamples, 1000 permutations |

## 2. Why the disposition is MEASUREMENT_INVALID

prereg §3 makes the experiment MEASUREMENT_INVALID if **any** of M1–M6 holds, and permits no
inference in either direction when it does. Three hold, and two of them are structural facts about
the freeze that no amount of good execution could repair.

| condition | required | observed | holds |
|---|---|---|---|
| M1 | >= 20 admitted sites | 6 admitted sites | **False** |
| M2 | pilot_data.json and power_calculation.json present and hashed at freeze | both absent, unhashed | **False** |
| M3 | frozen pool hashed into freeze.json | `freeze.json` hashes only `prereg.md`, `request.json`, `spec.json`; no `frozen_pool.json` | **False** |
| M4 | inert rate ≤ 0.20 in test | not decidable as written; the two non-vacuous readings give 0.3333 and 0.3333 on the test set (§5.1) | **not decidable** |
| M5 | cache predictor free of mechanism and parameters | structurally enforced | **True** |
| M6 | site-memory predictor free of bound parameters | structurally enforced | **True** |

M1 is not a bad-luck screen. Its dominant cause is measured: of
905 path-parameter probes only
71 returned 2xx/3xx
(7.85%),
and 151 candidates returned 404 for all five
path values. Frozen criterion C1 requires at least 12 of 15 probes to be 2xx/3xx, and since the
other two intervention types can contribute at most 10, that requires at least two of the five
path values to succeed. On credential-free public HTML documents this criterion is close to
unreachable, and C1 is the single largest screen failure
(167 of 181).

## 3. What the frozen numbers are, and why they are not evidence

These are reported for completeness and for audit. Under prereg §3 they carry no inferential
weight.

| quantity | value (nats) |
|---|---|
| `RESIDUAL_EFFECT_SIZE_NATS`, admitted frozen pool | 1.110778, CI95 [0.871108, 2.548803] |
| `RESIDUAL_EFFECT_SIZE_NATS`, full screened pool (exploratory) | 1.446620, CI95 [1.199098, 1.657227] |
| `PC_KNOWN_PARAMETER_EFFECT` | -1.489497, CI95 [-1.489497, -1.489497] |
| `NC_PERMUTED_MECHANISM` p95 | 1.902384 (treatment percentile 0.487) |

| acceptance condition | A1 metric > 0.05 | A2 CI lower > 0 | A3 > null p95 | A4 PC recovers | A5 >= 15 sites | A6 null non-degenerate |
|---|---|---|---|---|---|---|
| holds | True | True | False | False | False | True |

| falsification condition | F1 <= 0.05 | F2 CI includes 0 | F3 <= null p95 | F4 PC fails | F5 < 15 sites | F6 null degenerate |
|---|---|---|---|---|---|---|
| holds | False | False | True | True | True | False |

An alternative precedence that evaluated F1–F6 first would read FALSIFIES. That reading is recorded
in `derived/decision_readings.json` and **not adopted**, because the same condition set shows the
accept branch is unreachable and two instruments are themselves defective; the packet contract
forbids recording a statement about the instrument as scientific falsification. The Director owns
this precedence choice.

## 4. Substrate facts that are admissible regardless of disposition

These are direct observations of credential-free public HTML documents, not claims about mechanism
semantics. Each is bounded to the curated pool and to a single collection window.

* **Fragment interventions are inert as HTTP requires.** Conditioned on a 2xx/3xx response,
  `M_ANCHOR` returned a byte-identical signature at the same status in
  88.9% of 693 cases.
  Fragments are not transmitted in a request target, so the frozen mechanism's declared effect
  (client-side scrolling) is **definitionally unobservable** by a stdlib HTTP client.
* **Query parameters do produce body variation, above the measured noise floor.** Conditioned on a
  2xx/3xx response, `M_PAGINATION` changed the body at the same status in
  25.5% of 691 cases,
  against a repeat-identical rate of
  87.5%
  (140/160 repeat
  fetches of an unchanged URL were byte-identical). This is the first positive, bounded substrate
  result in this lineage and it contradicts the inherited expectation that public HTML documents
  show no per-identifier variation.
* **Path parameters are mostly absent, and their absence shows up as 404.** `M_SECTION` returned
  2xx/3xx in only 7.8% of probes. Its apparent signature variation is
  dominated by 404-versus-200 status changes, which is a transport effect, not section selection.
* **Revalidation responses are available and were never used.** 59 of
  80 conditional GETs returned 304 (73.8%).
  The frozen collection protocol issues no conditional requests, so component (i) — the
  cache/revalidation component the design is built around — is unmeasurable by the frozen design
  even though the substrate supplies it.
* **The site-dynamism floor is low but non-zero.**
  10 of 80
  candidates changed on at least one repeat fetch, so any signature difference at or below that
  floor cannot be attributed to an intervention.

## 5. The apparatus defects, measured rather than argued

These are the durable outputs of this run. Each is a property of the frozen specification, was
verified directly, and is quantified in `result.json`.

### 5.1 The frozen distance is not a distance

prereg §6.3 uses `+0.3 * Jaccard(cache_headers)` where a distance requires
`0.3 * (1 - Jaccard)`. As written, the term **increases** with header similarity. Consequences,
all measured:

* an identical signature scores exactly `0.3`, so the prereg §8.2 inert test `||delta|| < 0.01`
  can never fire; on the 105-instance held-out test set the
  frozen reading is 0.0000 while the
  signature-identity reading is
  0.3333 and the corrected reading is
  0.3333, both above the 0.20 inert ceiling;
* the positive control's provably inert fragment arm is scored at `0.3`, indistinguishable from a
  real change;
* correcting this one sign moves the positive control from **-1.489497 nats** to
  **7.923085 nats** — same ground truth, same predictors,
  same server. The distance form alone accounts for the positive-control failure.

### 5.2 The frozen strong baseline cannot be exercised

`B_SITE_TEMPLATE_MEMORY` is keyed on `(site, action_template)` while the split is at site level,
so no test site can own a TRAIN memory cell. It fell back to a global constant on
105/
105 frozen-pool test instances and
870/
870 exploratory test instances. The
frozen contrast between component (ii) and the treatment was therefore never tested: the entire
comparison is the treatment against one constant.

### 5.3 The frozen null cannot discriminate

`NC_PERMUTED_MECHANISM` permutes mechanism declarations within an `intervention_type`, and each
frozen `intervention_type` contains exactly one mechanism, so a permutation only reassigns which
instance receives which parameter rank. It is non-degenerate as required
(999 distinct values over 1000 permutations — the
inherited placebo defect is genuinely repaired), but its mean
(1.128741) sits on top of the treatment (1.110778), placing the treatment
at percentile 0.487. As specified it cannot separate the
mechanism declaration from a random rank alignment.

### 5.4 Rank magnitude is not identifiable from an HTTP signature

The executor added `SB_DEGENERATE_ZERO`, a predictor that uses no mechanism, no site, no parameter
and no data, because the frozen control set contains no triviality floor for the 0.05 nats
threshold.

On the positive control, where the mechanism declarations are true by construction, the observed
signature distance takes **at most two** distinct values across the five parameter ranks for
`M_PAGINATION` and **exactly one** for `M_SECTION`, while `MECHANISM_CONDITIONED` emits five
distinct rank-ordered values for both. A single constant is therefore closer to the truth than the
rank-ordered treatment on two of three mechanisms. Under the corrected distance the same positive
control gives 7.923085 nats for the treatment and
6.908598 nats for the
mechanism-free constant — the constant recovers
87%
of the treatment's gain. On the real Web pools under the corrected distance the ordering reverses
outright: the constant scores
12.102727 nats against the treatment's
6.828579.

The mechanism declaration predicts *how much* a parameter changed a document. HTTP exposes only
*whether* the signature changed. A magnitude prior over parameter rank has no observable
counterpart — this is a statement about the observable, not about the mechanisms.

### 5.5 Variance inverts the ordering

Under `TREATMENT_EXPLAINED_VARIANCE` the treatment scores
-0.6177 on the exploratory
pool while `SITE_MEMORY_EXPLAINED_VARIANCE` scores
0.5946, and
`RESIDUAL_SIGN_ACCURACY` is 0.2000.
The frozen log-score metric prefers the treatment only because it is singular at zero error.

## 6. Validity gates

* **V1_TARGET_INTEGRITY** — PASS: null predictors are handed restricted views without the mechanism declaration or bound parameters. Evidence: `exp_37385620138_lib.predict_cache_revalidation / predict_site_template_memory receive {url, baseline_url, baseline_signature} and {site, memory_key} only; MECHANISM_CONDITIONED reads only mechanism_id and value_rank`
* **V2_SPLIT_INTEGRITY** — PASS: site-level 70/30 split; B_SITE_TEMPLATE_MEMORY fitted on TRAIN rows only. Evidence: `train_sites=4, test_sites=2`
* **V3_SAMPLING_INTEGRITY** — PASS: master_seed = int(request_hash[:8],16); permutation and bootstrap seeds derived. Evidence: `master_seed=445086315`
* **V4_UNCERTAINTY_INTEGRITY** — PASS: 10000 site-clustered resamples, no noise injection. Evidence: `n_resamples=10000`
* **V5_REPRESENTATION_INTEGRITY** — PASS: every response archived with status, full response headers, body length, body sha256 and structural hash. DOCUMENTED LOSS: response body bytes are not archived (prereg s14 describes the body as part of this artifact), so a hash cannot be recomputed from the packet without a fresh fetch. Evidence: `raw/collection_log.jsonl`
* **V6_POOL_ADMITTED_GE_20** — FAIL: count of distinct admitted sites after the frozen screen. Evidence: `n_admitted_sites=6, n_screened=181`
* **V7_PILOT_POWER_HASHED** — FAIL: existence and freeze hashing of the two declared pre-freeze artifacts. Evidence: `{"candidate_universe.json": {"exists_on_disk": false, "hashed_by_freeze": false}, "frozen_pool.json": {"exists_on_disk": false, "hashed_by_freeze": false}, "pilot_data.json": {"exists_on_disk": false, "hashed_by_freeze": false}, "power_calculation.json": {"exists_on_disk": false, "hashed_by_freeze": false}}`
* **V8_INTERVENTION_BIT** — FAIL: fraction of HELD-OUT TEST interventions whose signature is unchanged by the intervention. Reported on all three readings because prereg s6.3 makes the frozen distance incapable of registering an inert intervention (identical signatures score 0.3, above the 0.01 ceiling), so the frozen-distance reading cannot fail and its PASS is not informative. Evidence: `TEST n_frozen=105 n_exploratory=870; TEST frozen_distance=0.0; TEST signature_identity=0.3333333333333333; TEST corrected_distance=0.3333333333333333; all-admitted-instances frozen_distance=0.0125`
* **V9_PLACEBO_NONDEGENERATE** — PASS: distinct mean-residual values across 1000 permutations. Evidence: `{"n_permutations": 1000, "n_distinct_values": 999, "degenerate": false, "null_p95": 1.9023843333766466}`
* **V10_PC_ATTAINABLE** — FAIL: PC residual >= frozen 0.10 nats. Evidence: `pc_residual=-1.4894969491411805; constant_zero_predictor_residual=-2.3685798086447933; max_attainable_log_score=-log(1e-10)=23.025850929940457`

V8 **FAILS**. Its frozen-distance reading is vacuous per §5.1 — it reads
0.0000 on the test set only because an inert
intervention cannot be registered by that formula at all. The two non-vacuous readings on the same
105-instance held-out test set are
0.3333 (signature identity) and
0.3333 (corrected distance), both above the
0.20 ceiling. M4 itself is recorded as **not decidable** rather than as pass or fail, because its
frozen definition cannot discriminate; a strict reading under either non-vacuous definition would
make M4 hold as well.

## 7. What this run does and does not establish

Established, at the stated ceiling:

1. Three preregistered pre-freeze artifacts do not exist and were never hashed. The design's power
   and threshold-attainability claims are unverifiable, and the measured positive control
   (-1.489497 ± 0.000000) does not contain the asserted pilot value (0.18 ± 0.03).
2. The frozen distance formula is not a metric, and that single defect accounts for the
   positive-control failure (§5.1).
3. The frozen strong baseline and the frozen null control cannot, as specified, discriminate the
   mechanism-semantics component from a global constant or from a random rank alignment (§5.2,
   §5.3).
4. On credential-free public HTML documents, fragment interventions are inert, query parameters do
   produce body variation above the dynamism floor, path parameters are usually absent, and
   revalidation responses are available but unused (§4).

**Not** established, and explicitly unsafe to assume:

* that C-WEB-DYNAMICS is false, weakly supported, or blocked — this run carries no admissible
  evidence about the claim;
* that the 1.110778 nats figure, or its 5.650872 corrected-distance
  counterpart, indicates mechanism semantics — on both readings a mechanism-free constant is
  competitive or better;
* that query-parameter variation is mechanism-semantic rather than template rotation — that is
  precisely the discrimination the collapsed `B_SITE_TEMPLATE_MEMORY` arm was designed to make;
* that the 87.5% dynamism floor licenses attributing
  the 25.5% pagination variation to the bound
  parameter rather than to host dynamism;
* that anything here generalises beyond one curated pool and one collection window, on one
  credential-free stdlib HTTP client with no JavaScript, no cookies and no rendering.

## 8. Smallest next actions that would unblock a real measurement

1. Fix the distance to `0.3 * (1 - Jaccard)` (or another form with `d = 0` iff signatures are
   equal) and re-freeze. This is a one-line specification repair with a measured effect (§5.1).
2. Re-key `B_SITE_TEMPLATE_MEMORY` on `(site, document_template)` fitted across train sites, or
   hold out documents within sites, so the split can actually exercise component (ii) (§5.2).
3. Re-specify `NC_PERMUTED_MECHANISM` to permute across mechanisms *and* intervention types, or
   to permute the declared effect against the bound parameter independently, so the null can
   separate a mechanism declaration from a rank alignment (§5.3).
4. Register a triviality floor (`SB_DEGENERATE_ZERO`) as a required control and make the acceptance
   threshold relative to it, not an absolute 0.05 nats (§5.4).
5. Lower or restructure C1: the ≥12-of-15 criterion requires path-parameterized content that
   credential-free public HTML documents do not expose, and it dominates screen failure (§2).
6. Decide the branch-precedence question in §3 explicitly in the next preregistration.

## 9. Packet contents

`result.json` (this run's structured output), `provenance.json` (reproducibility, hashes,
environment, scope compliance), `raw/` (every request/response, the screen, the diagnostics, the
positive control), `derived/` (predictions, metrics, null distribution, gate and decision
readings), and the four executor code files under `research/physics/`. Artifact paths and SHA256
hashes for all of them are listed in `result.json.artifacts` and `provenance.json.artifacts`.

No frozen input was modified. No commit, push, branch switch or reset was performed.
`SPIDER_CODEX.md` is unmodified.
