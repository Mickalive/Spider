# EXP-RUNTIME-38244432934 preregistration (runtime, design_contract_version 2)

**Status:** frozen design (design_contract_version 2). Do not edit after freeze.

| identity | value |
| --- | --- |
| experiment_id | `EXP-RUNTIME-38244432934` |
| lane | `runtime` |
| design_contract_version | `2` |
| target claim | `C-DELTA-REPAIR` (CONTINUE; parent-handoff disposition **USE**) |
| dependency claims | `C-PRODUCT-ECON`, `C-MEAS-VALID`, `C-PARAM-INHERIT`, `C-FRESHNESS` |
| request `base_sha` | `922eee8638c6fed694076d611433d41a5ef75b21` |
| claim_registry_sha256 | `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b` |
| origin_github_run_id | `38244432934` |
| parent_handoff | `EXP-RUNTIME-38212966040` (`sha256 994971376da89ef3547eb4a72a5f0ad5aba4aa4eb7c4447f286a912e96b08d7b`), disposition **USE** (not SUPERSEDE/PIVOT/REOPEN) |
| parent audit | `EXP-RUNTIME-38212966040/audit.json` status `REVISE`, F1/F2 `blocks_claim=true` |
| origin of the target question | `request.json.director_mandate` (CONTINUE, `cognitive_reset=true`) |
| CANONICAL-RUNNER-SHA256 | `d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608` (60855 bytes) |
| frozen runner file | `raw_evidence/runner_delta_repair_reuse_v2.py` |

The Global Research Director mandate (`request.json.director_mandate`, action `CONTINUE`,
claim `C-DELTA-REPAIR`, `parent_handoff_disposition=USE`) is BINDING. Runtime is reactivated
from IDLE. The parent packet `EXP-RUNTIME-38212966040` ended
`PARTIAL_MEASUREMENT_INVALID` with only a bounded cost sub-result retained because its
contamination helper used an OUT-OF-SUPPORT literal `id="1"`, which the carrier's inferred
support `^1[0-9]{1}$` rejects, pinning `M-CONTAMINATION-RATE` and
`M-OVERBROAD-CONTAMINATION-RATE` at 0.0 by construction and making `NC-OVERBROAD-REPAIR`
structurally unable to fire. That is a one-line instrument defect, not a scientific
negative. This packet repairs that exact prerequisite ONCE in a NEW frozen design (the
parent frozen runner/prereg are immutable and are NOT touched), re-attests the positive
control inside the scored transaction, and adds an independent counter-weighting
robustness test that did not previously exist.

This experiment does NOT re-run the parent design and does NOT merely repeat pre-2.0 work.
It changes three things: (1) the contamination/`NC-OVERBROAD-REPAIR` instrument is corrected
to in-support identifiers; (2) the repair-success denominator (F6) now includes the fused
first task; (3) a predeclared weight grid tests whether the strict win is a counter artifact.
The registered equal-weight product counter is NOT re-tuned. It does NOT execute the gated
`C-PRODUCT-ECON` flagship benchmark and does not mutate any cross-lane claim status.

## 0. Preserved parent-handoff distinctions (USE)

From `EXP-RUNTIME-38212966040/handoff.json` (`carry_forward`), inherited as scientific state
and preserved here:

- **established.** (e1) Bounded COST result on this substrate/carrier under the reuse
  semantics: `T-REPAIR-REUSE` product 17 vs `B-COLD` 18 (L=2) / 19 (L=3), ratios 0.9444 /
  0.8947, fetch ratio 0.556-0.667. (e2) Replication premise: `T-REPAIR-LEGACY` product 20 ->
  ratios 1.1111 / 1.0526, exactly reproducing the prior `EXP-GRAPH-38197849043` regression.
  (e3) Baseline/control liveness: cold success 1.0 (18/19/20 at L=2/3/4), literal-replay
  success 0.0, no-repair success 0.0, `NC-NO-PERTURBATION`/`NC-NOISE` stale=false.
  (e4) Treatment functional liveness: repair success 1.0, guard fire 1.0. (e5) Structural
  locality: `M-WRITE-SET-MAX=1`. (e6) The parent audit is REVISE/`producer_claim_supported`
  false; the settled claim ceiling excludes behavioural locality, counter-robustness and
  transfer.
- **rejected.** (r1) The parent's headline bundle (`outcome=SUPPORTS`, "STRICT-WIN on all
  three classes", "H1-H4 all CONFIRMED", "all 14 gates pass") is NOT adopted. (r2) The
  parent's H2 locality assertion is rejected FOR THAT PACKET because the contamination
  instrument was degenerate. (r3) The hypothesis that the prior ~5.3% product-counter
  regression is intrinsic is provisionally not supported on this substrate/counter, but the
  strict-win classification was not measurement-valid end to end and `T-REPAIR-CONSERVATIVE`
  is exactly 1.00 at L=2, so this is a bounded disconfirmation, not a validated positive.
  (r4) none of these closes the localized-repair product-economics domain, `C-DELTA-REPAIR`
  as a whole, `C-PRODUCT-ECON`, or the flagship benchmark.
- **unknown.** (u1) Would `M-CONTAMINATION-RATE` be 0.0 under a corrected instrument?
  (u2) Does the strict win survive counter reweighting and the conservative bound, given
  `T-REPAIR-CONSERVATIVE` is exactly 1.00 at L=2? (u3) Is `T-REPAIR-LEGACY` a faithful
  operation-sequence reconstruction or only a product-counter reconstruction? (u4) Does the
  reuse semantics transfer to a production carrier? (u5) Does STRICT-WIN transfer to real
  web tasks / external agents / the gated flagship? (u6) The parent scored run's positive
  control was not directly evidenced (base_liveness=false on all 36 trials, same id defect).
- **do_not_assume** (preserved verbatim in intent). Do NOT report SUPPORTS / STRICT-WIN /
  "H2 confirmed" / "all gates pass" for the PARENT packet; do NOT read the parent's
  contamination 0.0 as non-contamination; do NOT promote localized repair to product on the
  parent; do NOT generalize the 0.9444/0.8947 numbers beyond this substrate/carrier/counter;
  do NOT treat `C-DELTA-REPAIR` as advanced or downgraded (it remains EXPERIMENTAL); do NOT
  mutate any frozen parent file; do NOT read the parent's measurement invalidity as a
  scientific falsification; do NOT dispatch a Runtime successor without a new mandate.

This packet is the NEW design the mandate authorizes. Its own claim ceiling (section 7 and
the EXECUTE/AUDIT packet) is bounded to this credential-free stdlib substrate, the shipped
parameterized carrier, the preregistered counters, and the three declared perturbation
classes.

## 1. Question

On the same fetch-scarce, credential-free, locally served substrate and the same SHIPPED
carrier held fixed (`src/spider/kernel.py`: `distill_parameterized -> resolve -> execute ->
verify`), with the F1 degenerate contamination helper CORRECTED to an IN-SUPPORT probe id
(`^1[0-9]{1}$`; `TASK_IDS[0]=14`) so that the baseline/post-repair and over-broad comparisons
are no longer structurally equal: does signal-driven local repair, under the preregistered
reuse accounting, reproduce BOTH (a) the strict product-counter win (reuse ratio < 1.00 at
L=2 and L=3, fetch ratio <= 0.90) AND (b) a sensitive `NC-OVERBROAD-REPAIR`
(over-broad contamination rate > 0.10), and (c) does that strict win survive an independent
counter-weighting robustness test over a predeclared weight grid, given that
`T-REPAIR-CONSERVATIVE` is exactly 1.00 at L=2 - thereby deciding whether localized repair
enters the product story or its ~5.3% product-counter regression is intrinsic to localized
repair?

## 2. Hypotheses

- `H1 (functional, re-attested in-artifact).` After a single LOCAL perturbation of one
  resource segment, reuse-based signal-driven local repair restores correct end-to-end
  success on ALL FIVE `TASK_IDS=[14,15,16,17,18]` (F6 fix: the fused first task's verify is
  counted) at rate >= 0.80 per class (Wilson 95% lower bound >= 0.60), with the deterministic
  guard firing on >= 0.80 of perturbed trials, for `P1-ENDPOINT`, `P2-STRUCTURE`,
  `P3-PERMISSION`.
- `H2 (locality, now measurable).` The repair write set is localized to the single perturbed
  mechanism (`M-WRITE-SET-MAX <= 1`); behavioural contamination of the four unaffected
  resources, measured with the IN-SUPPORT probe, is <= 0.10, AND the instrument is provably
  live because the deliberately over-broad all-mechanism rewrite (`NC-OVERBROAD-REPAIR`) is
  detected at rate > 0.10.
- `H3 (cost, the mandate's strict claim).` Under the preregistered reuse semantics the repair
  product-counter ratio is STRICTLY below 1.00 at BOTH L=2 and L=3 and the network-fetch
  ratio at L=3 is <= 0.90.
- `H4 (counter-robustness, the new mandate question).` The strict win is not an artifact of
  the equal-weight counter choice: over the predeclared weight grid `{1,2,3}^4` applied to
  the four registered counter components, repair beats cold at BOTH L=2 and L=3 on EVERY
  counter in the grid (`M-WEIGHT-ROBUST-BOTH == 1.0`, `ROBUST_FRACTION_BAR = 1.0`, i.e. the
  sign is invariant to the reweighting), and the conservative re-resolve ratio at L=3
  remains < 1.00.
- `H5 (replication premise).` `T-REPAIR-LEGACY`, on the SAME substrate and cold baseline,
  still reproduces the prior product-counter regression (ratio > 1.00 at L=2), so any
  difference is attributable to the repair system's accounting.

## 3. Falsifier

With `H1` and a LIVE `H2` instrument established on every class (guard fires, over-broad
contamination > 0.10, same-target contamination <= 0.10, write set <= 1):

- the mandate's strict claim is validly NEGATIVE if the reuse product-counter ratio is
  >= 1.00 at L=2 OR at L=3, or the L=3 fetch ratio exceeds 0.90 (`MIXED`/`COST-FAIL`, not a
  strict support); and
- it is COUNTER-DEPENDENT rather than ROBUST if the strict inequalities hold but
  `M-WEIGHT-ROBUST-BOTH < 1.0` or the conservative L=3 ratio is >= 1.00 - i.e. the win
  exists only under the registered equal-weight counter and is reversed by at least one
  permitted monotone reweighting, or reversed by the re-resolve upper bound.

A run whose corrected over-broad control is not sensitive (`M-OVERBROAD-CONTAMINATION-RATE`
<= 0.10), whose contamination probe set is empty, whose guard false-fires, whose in-scored
positive control is not true, or whose cold / literal-replay / no-repair baselines are not
live is `MEASUREMENT_INVALID`, NEVER a scientific negative. An instrument failure must not be
transcribed as falsification.

## 4. Substrate, banks, and perturbation classes

**Substrate (unchanged from the parent, credential-free, local, stdlib only; no model call).**
An in-process `ThreadingHTTPServer` serves a small JSON API `/api/<resource>/<id>` over
127.0.0.1 on an ephemeral port. Records return `id` as a **string** plus a stable anchor
field `kind` and per-id data fields. Five resources exist: `users`, `posts`, `comments`,
`albums`, `photos`. The METERED work is the live network fetch; `resolve`/`verify` are the
carrier's local operations and are metered by the registered counter. There is NO LLM,
credential, external network, browser, nginx, gunicorn, Redis or WAL, so no model call exists
and fetches are the scarce accounting resource.

**Identifier banks (disjoint by design).** `TASK_IDS=[14,15,16,17,18]` are the executed task
ids; `LEARN_IDS=[11,12,13]` are the re-derivation observation ids; `LEARN_IDS_MIN=[11,12]`
(L=2) and `LEARN_IDS_DEEP=[10,11,12,13]` (L=4) are the cold-budget sensitivities. The learned
support is the carrier-inferred anchored grammar `^1[0-9]{1}$`, which accepts BOTH banks.
LEARN and TASK ids are DISJOINT so re-derivation reads are genuine acquisition reads. The
corrected contamination probe uses `IN_SUPPORT_PROBE_ID = TASK_IDS[0] = 14`, which the
support accepts (the parent's `id="1"` was rejected by it: audit F1).

**Perturbation classes (one per trial, applied in-process to the single target).**

| class | perturbation | required repair signal |
| --- | --- | --- |
| `P1-ENDPOINT` | old path segment becomes `301` with `Location: /api/<new_segment>/<id>`; redirects are NOT auto-followed | rebind the endpoint segment from `Location` |
| `P2-STRUCTURE` | anchor `kind` renamed to `entity_type` and `schema_version:"2"` added; HTTP 200 | re-adopt the live postcondition schema, relocating the renamed anchor |
| `P3-PERMISSION` | target requires header `X-Consent: granted`, else `403` + `X-Required-Consent: granted` | attach the server-advertised required header |

Targets rotate over `users`/`posts`/`comments`; the other four resources are the
contamination probes. The repair routine branches purely on the observed response signature
and is never told the perturbation class.

## 5. Freshness guard, the three repair systems, and the reuse semantics

**Deterministic freshness guard (unchanged).** The guard declares the live probe STALE iff
any of: (1) the probe is non-200 or errored; or (2) the inherited mechanism's own
postconditions no longer `verify` on the live body; or (3) the Jaccard similarity of the
mechanism's own required-field-filtered structural token set falls below
`JACCARD_THRESHOLD = 0.85`. Fields outside the mechanism's postcondition paths cannot trigger
it. The guard has no fitted parameters.

**The reuse semantics.** The three systems differ only in how the repair path charges work;
all use the SHIPPED carrier and the same guard.

- `T-REPAIR-REUSE` (TREATMENT): the freshness check is FUSED into the first task read (the
  first task attempt is the probe, so no separate guard read is issued), and after the repair
  the reused probe observation is charged ONCE: exactly one `repair_attempts`, one repair
  probe fetch, and one post-repair `verify` of the live probe body; the first task id is NOT
  re-resolved, re-fetched or re-verified. **F6 fix:** the fused first task's verify result
  now counts toward `M-REPAIR-SUCCESS` (the parent discarded it and scored only
  `TASK_IDS[1:]`).
- `T-REPAIR-CONSERVATIVE` (SYSTEM SENSITIVITY): identical, except the repair also re-resolves
  through the carrier's `rebind` (which charges one `retrieval_calls`); this is an upper bound
  on the repair cost and bounds how much of the result depends on not re-resolving.
- `T-REPAIR-LEGACY` (REPLICATION CONTROL): the PRIOR system - a separate guard probe read is
  issued before the batch, and after repair the FULL task batch is re-executed (so the first
  task id is read twice more). Must reproduce the prior product-counter regression.

**Accounting is physical, not summed post hoc.** Every `fetch` increments `http_requests`;
every carrier `resolve` (`rebind` calls `resolve`) increments `retrieval_calls`; every
`verify` increments `verification_calls`; `repair_attempts` is charged exactly once per
repair. The registered product counter is their equal-weight sum. The ONLY difference between
the treatment and the legacy control is the number of physical resolve/fetch/verify
operations for the first task id. **A6 fix:** each arm emits an explicit per-operation log
(`repair_oplog`, `conservative_oplog`, `legacy_oplog` in every trial) so the reuse identity is
directly evidenced, not merely asserted.

**The corrected contamination instrument (F1/F2 fix).** `unaffected_behavior(...)` now takes
an explicit in-support `probe_id` (defaulted by all callers to `IN_SUPPORT_PROBE_ID=14`) and
`overbroad_contamination(...)` threads it through. Consequence (verified at DESIGN):
baseline and post-repair probes return a real verified `(200, id, True)`, so
`M-CONTAMINATION-RATE` is a live measurement (not pinned at 0.0), and the over-broad rewrite
breaks 4/4 unaffected resources (rate 1.0 > 0.10). If `M-OVERBROAD-CONTAMINATION-RATE` were
ever <= 0.10 or the probe set empty, the run is `MEASUREMENT_INVALID` (gate V15).

## 6. Baselines and controls

| id | type | description |
| --- | --- | --- |
| `B-COLD` | cost baseline (primary) | cold re-derivation: discovery probe + `LEARN_IDS` (L=3) fresh observations, `distill_parameterized`, then execute the 5 tasks. The mandate's strong comparator and the ONLY cost denominator. |
| `B-COLD-MIN` | cost sensitivity | identical but L=2 (the carrier's minimum viable re-derivation). |
| `B-COLD-DEEP` | cost sensitivity | identical but L=4. |
| `B-LITERAL-REPLAY` | mechanism control (must fail) | replay the inherited (unrepaired) mechanism on the perturbed resource. |
| `B-NO-REPAIR` | abstention control (must fail) | guard detects staleness but the system abstains; non-executing, NEVER the cost denominator. |
| `T-REPAIR-REUSE` | treatment | see section 5. |
| `T-REPAIR-CONSERVATIVE` | system sensitivity | see section 5; upper bound on repair cost; L=3 ratio enters the ROBUST tier test. |
| `T-REPAIR-LEGACY` | replication control | see section 5; must reproduce the prior regression (>1.00 at L=2). |
| `PC-BASE-LIVENESS` | positive control | scored inside EVERY trial: pre-perturbation, every learned mechanism resolves EXECUTABLE and its in-support first read verifies. |
| `NC-NO-PERTURBATION` | negative control | with no perturbation the guard must NOT fire (stale=false). |
| `NC-NOISE` | negative control | non-semantic `observed_at` churn must NOT fire the guard. |
| `NC-OVERBROAD-REPAIR` | negative control (must be detected) | apply the target's repaired postconditions to ALL mechanisms; with the corrected in-support probe the contamination metric must detect the breakage (>0.10). |

## 7. Decision rule

Per class, on the FROZEN classifier, using the REUSE surface (the mandate's semantics):

```
functional_ok := repair_success >= 0.80
             AND repair_success_wilson_lower >= 0.60
             AND contamination_rate <= 0.10
             AND write_set_max <= 1
             AND guard_fire_rate >= 0.80
strict_win_robust := (M-WEIGHT-ROBUST-BOTH >= 1.0)
             AND (M-PRODUCT-RATIO-CONSERVATIVE-L3 < 1.00)
cost_verdict := FUNCTIONAL-FAIL            if not functional_ok
              | STRICT-WIN-ROBUST          if pr_L2 < 1.00 AND pr_L3 < 1.00 AND fetch_L3 <= 0.90 AND strict_win_robust
              | STRICT-WIN-COUNTER-DEPENDENT if pr_L2 < 1.00 AND pr_L3 < 1.00 AND fetch_L3 <= 0.90
              | BOUNDED-WIN                if pr_L2 <= 1.00 AND pr_L3 <= 1.00 AND fetch_L3 <= 0.90
              | MIXED-TRADEOFF             if max(pr_L2,pr_L3) <= 1.15 AND fetch_L3 <= 0.90
              | COST-FAIL                  otherwise
              | COST-UNKNOWN               if pr_L2/pr_L3/fetch_L3 is None
```

where `pr_L2 = mean(repair reuse product)/mean(cold L=2 product)`,
`pr_L3 = mean(repair reuse product)/mean(cold L=3 product)`,
`fetch_L3 = mean(repair http)/mean(cold http)` at L=3, all over the equal-weight registered
`TrajectoryCounters` components, and `M-WEIGHT-ROBUST-BOTH` is the fraction of the
predeclared `WEIGHT_GRID = {1,2,3}^4` (81 vectors) on which the repair arm's WEIGHTED product
counter is strictly below cold at BOTH L=2 and L=3; `ROBUST` requires this fraction to be
`1.0`, i.e. NO permitted reweighting reverses the sign. The registered equal-weight counter is
NOT re-tuned; the grid only reports how the SIGN changes under monotone reweightings.

Aggregate decision (classes `P1-ENDPOINT`, `P2-STRUCTURE`, `P3-PERMISSION`):

- any validity gate fails -> `status=MEASUREMENT_INVALID`, `outcome=INCONCLUSIVE`;
- all classes `STRICT-WIN-ROBUST` -> `SUPPORTS`, `outcome=SUPPORTS`;
- all classes in `{STRICT-WIN-ROBUST, STRICT-WIN-COUNTER-DEPENDENT}` ->
  `SUPPORTS-COUNTER-DEPENDENT`, `outcome=MIXED`;
- all classes in the positive/neutral tiers -> `MIXED-TRADEOFF`, `outcome=MIXED`;
- some class positive/neutral -> `MIXED`, `outcome=MIXED`;
- otherwise -> `FALSIFIES`, `outcome=FALSIFIES`.

`T-REPAIR-CONSERVATIVE` (`M-PRODUCT-RATIO-CONSERVATIVE-L2/L3`) and `T-REPAIR-LEGACY`
(`M-PRODUCT-RATIO-LEGACY-L2/L3`) are reported as system controls and sensitivities; they do
NOT enter the classifier as comparators (only the conservative L=3 value enters the ROBUST
bound test).

## 8. Design satisfiability probes (non-scored, DESIGN-time)

All probes are non-outcome-bearing; no scored cost was read to choose any threshold, and the
scored run re-measures everything independently at n=12 per class.

**8.1 Decision-branch reachability (synthetic, non-substrate).** The frozen pure
`cost_verdict` and `aggregate` were driven with synthetic rows (`--reachability-probe`):
every class branch `{STRICT-WIN-ROBUST, STRICT-WIN-COUNTER-DEPENDENT, BOUNDED-WIN,
MIXED-TRADEOFF, COST-FAIL, FUNCTIONAL-FAIL, COST-UNKNOWN}` and every aggregate decision
`{SUPPORTS, SUPPORTS-COUNTER-DEPENDENT, MIXED-TRADEOFF, MIXED, FALSIFIES, INCONCLUSIVE}` was
produced (`all_class_branches_reachable=true`, `all_aggregate_branches_reachable=true`).
The rule is satisfiable and not a tautology. `STRICT-WIN-COUNTER-DEPENDENT` is reachable both
by a robust fraction below `1.0` (the probe uses the realizable measured-shape value `0.7778`)
and by conservative L=3 = 1.00.

**8.2 Counter-weighting grid reachability (synthetic).** `--reachability-probe.weight_grid_probe`
reports `grid_size=81`, the measured-shape reuse vector `(6,5,5,1)` against cold
`(8,5,5,0)/(9,5,5,0)` with `knife_edge_fraction=0.7778`, an http-dominated robust vector with
fraction `1.0`, `critical_repair_weight_L2=2.0`, `critical_repair_weight_L3=3.0`, and
`both_sides_reachable=true`. DESIGN self-attack then searched the structural floor: among ALL
integer difference vectors that already win at equal weight, the minimum grid fraction is
`structural_min_fraction_for_equal_weight_win=0.5556`. Consequently a sub-`0.50` bar (as
originally sketched) would have been structurally NON-discriminating - the grid could never
have selected `COUNTER-DEPENDENT`. The declared bar was corrected to `ROBUST_FRACTION_BAR=1.0`
(sign-invariance across the whole grid), which sits above the `0.5556` floor
(`bar_is_discriminating=true`) and is reachable on both sides (`both_sides_reachable=true`).

**8.3 Repair-signal unit probe (synthetic).** `local_repair` was driven with synthetic live
signal signatures for all three classes (`301+Location`, `403+X-Required-*`, `200+schema
drift`); each produced `patched=true` and a probe body (`probe_body_present=true`).

**8.4 Corrected-instrument liveness (non-outcome-bearing).** Independently reproduced at
DESIGN: the carrier-inferred support is `^1[0-9]{1}$`, which `_support_accepts` rejects `"1"`
and accepts `14/15/19/10`; with the old `id="1"` every resource returns `NO-RESOLVE`
(degenerate, audit F1 reproduced); with `IN_SUPPORT_PROBE_ID=14` every resource returns
`(200, "14", True)`; and an over-broad postcondition rewrite flips 3/4 synthetic and 4/4
runner unaffected probes to unverified, so `NC-OVERBROAD-REPAIR` fires.

**8.5 Carrier-liveness probe (non-outcome-bearing).** `--liveness-only` boots the substrate,
distills from `LEARN_IDS`, executes and verifies one in-support task read, checks the two
negative controls, and compares the corrected vs degenerate instruments. Observed:
`server_ready=true`, `distill_live=true`, `task_read_verified=true`,
`contamination_instrument_live=true`, `out_of_support_probe_degenerate=true`,
`nc_no_perturbation_stale=false`, `nc_noise_stale=false`; carrier hashes equal the parent
freeze (`3a6caf97...` / `338aaf4d...` / `51fb440d...`).

**8.6 Mechanics canary determinism (non-scored).** Two independent `--mechanics-only` runs
were byte-identical on the canary projection (valid, control liveness, guard firing, oplogs);
all trials `valid=true`, `base_liveness=true`, cold success true, literal-replay success
false, repair success true, `unaffected_n=4`, `contamination_n=0`.

**8.7 Non-fitted thresholds.** `PRODUCT_COST_BAR=1.00`, `FETCH_COST_BAR=0.90` are the
mandate's semantics; `PRODUCT_COST_MAX=1.15` is an a priori 15% materiality band;
`LEGACY_REGRESSION_FLOOR=1.00` is the prior verdict's sign; `ROBUST_FRACTION_BAR=1.0`
(sign-invariance across the whole predeclared grid) and `WEIGHT_GRID={1,2,3}^4` were declared
before any scored run, and the `1.0` bar was fixed by the structural-floor self-attack in
section 8.2, not by any scored cost. None was tuned against a scored cost.

## 9. Measurement validity gates

- `V1-FREEZE_BINDING`: the runner extracted by splitting the section-12 markers (preserving
  the runner's own trailing newline - the audit F5 defect) hashes to
  `CANONICAL-RUNNER-SHA256`; request/prereg/artifact hashes match `freeze.json`.
- `V2-SUBSTRATE_ISOLATION`: stdlib only; no LLM/network/credential/browser; fresh per-run
  registry directory (no cross-run mechanism leakage).
- `V3-DETERMINISM`: fixed seeds; two independent `--mechanics-only` runs byte-identical.
- `V4-PERTURBATION_BITES`: `B-LITERAL-REPLAY` success <= 0.10 on every class.
- `V5-COLD_BASELINE_LIVE`: `B-COLD` success >= 0.90 on every class.
- `V6-NO_REPAIR_INERT`: `B-NO-REPAIR` success <= 0.10.
- `V7-GUARD_LIVENESS`: guard fires >= 0.80 on perturbed trials AND NOT on
  `NC-NO-PERTURBATION`/`NC-NOISE`.
- `V8-NO_TARGET_LEAKAGE`: the repair writes exactly one mechanism (`M-WRITE-SET-MAX <= 1`);
  contamination measured only on genuinely unaffected resources.
- `V9-INTEGER_COUNTERS`: all cost counters are integer counts from the shipped
  `TrajectoryCounters` surface; no estimated or model-token quantities.
- `V10-THRESHOLD_NOT_FITTED`: all decision bars and the weight grid are preregistered and were
  not tuned against any scored run.
- `V11-N_CONTROLLED`: `TRIALS_PER_CLASS = 12` with rotating targets.
- `V12-POSITIVE_CONTROL`: `PC-BASE-LIVENESS` true inside EVERY valid scored trial (audit F4).
- `V13-LEGACY_REPRODUCTION`: `T-REPAIR-LEGACY` product ratio > 1.00 at L=2
  (`M-LEGACY-REGRESSION-REPRODUCED`). A failure is reported as a validity caveat, not hidden.
- `V14-REUSE_IDENTITY`: `T-REPAIR-REUSE` and `T-REPAIR-LEGACY` share the same seeds,
  perturbations, substrate and cold baseline; their emitted per-operation logs differ only in
  the extra first-task resolve/fetch/verify of the legacy system (A6 fix: logs are present in
  every trial; `M-OPLOG-PRESENT=true`).
- `V15-CONTAMINATION-INSTRUMENT-LIVE` (NEW, the F1 fix): `M-CONTAMINATION-PROBES-TOTAL > 0`
  AND `M-OVERBROAD-CONTAMINATION-RATE-MEAN > 0.10`. Failure -> `MEASUREMENT_INVALID`; the
  parent's degenerate 0.0 must be structurally impossible here.

## 10. Freeze artifacts and canonical hashes

Mutable local interpretation dependencies (hashed into `freeze.json.artifact_hashes`):

- `src/spider/kernel.py` (the shipped carrier; treatment identity, support inference and
  counter semantics)
- `src/spider/models.py` (Mechanism/Observation/Resolution semantics)
- `src/spider/registry.py` (registry read/upsert/invalidate semantics; locality)

The executable decision path is embedded verbatim in section 12 and bound by
`CANONICAL-RUNNER-SHA256` and by `freeze.json.hashes.prereg.md`. No external task bank,
dataset or fixture is read: the substrate is constructed inside the runner.

## 11. Environment and EXECUTE command

Python 3.12, stdlib only. After freeze, EXECUTE extracts the runner by falling back to the
literal marker split
`content.split("<!-- BEGIN FROZEN-RUNNER -->\n", 1)[1].split("<!-- END FROZEN-RUNNER -->", 1)[0]`,
which preserves the runner's own trailing newline, writes those exact bytes to
`raw_evidence/runner_delta_repair_reuse_v2.py`, verifies its sha256 equals
`CANONICAL-RUNNER-SHA256 = d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608`
(60855 bytes), and runs:

```
python raw_evidence/runner_delta_repair_reuse_v2.py | tee raw_evidence/runner_result_raw.json
```

The runner prints a single JSON object on stdout. `--mechanics-only` is the non-scored
determinism canary; `--reachability-probe` and `--liveness-only` are non-scored DESIGN
satisfiability probes. `result.json` MUST transcribe the frozen raw values exactly (audit F3),
in particular `M-REPAIR-SUCCESS-WILSON-LOWER`, and MUST NOT restate the parent packet's
established/rejected distinctions as its own.

## 12. FROZEN-RUNNER
<!-- BEGIN FROZEN-RUNNER -->
#!/usr/bin/env python3
# FROZEN RUNNER for EXP-RUNTIME-38244432934 (runtime, design_contract_version 2).
# C-DELTA-REPAIR, CONTINUE of EXP-RUNTIME-38212966040 (audit REVISE: F1-F6).
#
# Question (Director mandate): with the F1 contamination instrument CORRECTED
# (an IN-SUPPORT probe id replacing the degenerate hardcoded id="1" which the
# carrier rejects, pinning both contamination metrics at 0.0 by construction),
# does signal-driven local repair reproduce BOTH a strict product-counter win
# (reuse ratio < 1.00 at L=2 and L=3) AND a sensitive NC-OVERBROAD-REPAIR
# (over-broad contamination rate > 0.10), and does that strict win survive an
# independent counter-weighting robustness test given that T-REPAIR-CONSERVATIVE
# is exactly 1.00 at L=2 - deciding whether localized repair enters the product
# story or its ~5.3% regression is intrinsic?
#
# The registered product counter is NOT re-tuned: it remains the equal-weight
# sum {http_requests, retrieval_calls, verification_calls, repair_attempts}. The
# robustness test only reports how the sign of the comparison changes under a
# predeclared weight grid.
#
# Arms (stable ids reused from the parent packet):
#   T-REPAIR-REUSE        treatment: guard fused into the first task read; the
#                         repair reuses the probe observation (no duplicate
#                         resolve/fetch/verify for the first task id).
#   T-REPAIR-CONSERVATIVE sensitivity: same reuse, but the repair also re-resolves
#                         (charges the rebind's retrieval) -> upper bound on cost.
#   T-REPAIR-LEGACY       replication control: the prior separate-guard-probe plus
#                         full-batch re-execution system; must reproduce the prior
#                         product-counter regression (>1.00).
#   B-COLD / B-COLD-MIN / B-COLD-DEEP / B-LITERAL-REPLAY / B-NO-REPAIR baselines.
#   PC-BASE-LIVENESS      positive control scored inside the artifact (in-support).
#   NC-NO-PERTURBATION / NC-NOISE / NC-OVERBROAD-REPAIR null controls.
#
# Stdlib only. No credentials, no external network, no LLM, no browser.
# Usage:
#   python runner_delta_repair_reuse_v2.py              # scored run
#   python runner_delta_repair_reuse_v2.py --mechanics-only
#   python runner_delta_repair_reuse_v2.py --reachability-probe
#   python runner_delta_repair_reuse_v2.py --liveness-only   # no repair, no cost ratio
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import random
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-RUNTIME-38244432934"
SEED = 38244432934 % (2 ** 32)

# Fresh per-process registry directory: MechanismRegistry.all() loads existing
# JSONL and upsert() merges by mechanism_id, so a reused path would resurrect
# stale mechanisms whose embedded endpoint port no longer exists.
_RUN_DIR = Path(tempfile.mkdtemp(prefix=f"exprun382-{os.getpid()}-"))

sys.path.insert(0, str(ROOT / "src"))
from spider.kernel import SpiderKernel, TrajectoryCounters  # noqa: E402
from spider.models import Mechanism, Observation  # noqa: E402
from spider.registry import MechanismRegistry  # noqa: E402

# ---------------------------------------------------------------- constants --
RESOURCES = ["users", "posts", "comments", "albums", "photos"]
TARGETS = ["users", "posts", "comments"]
TASK_IDS = [14, 15, 16, 17, 18]
# Learning ids are DISJOINT from task ids so re-derivation's observation reads
# are genuine acquisition reads, never a double-charge of a task read.
LEARN_IDS = [11, 12, 13]
LEARN_IDS_MIN = [11, 12]
LEARN_IDS_DEEP = [10, 11, 12, 13]
CLASSES = ["P1-ENDPOINT", "P2-STRUCTURE", "P3-PERMISSION"]
NEW_SEGMENTS = ["people", "articles", "notes", "collections", "media"]
ANCHOR = "kind"
ANCHOR_RENAMED = "entity_type"
CONSENT_HEADER = "X-Consent"
CONSENT_VALUE = "granted"
JACCARD_THRESHOLD = 0.85
MIN_CONFIDENCE = 0.8

REPAIR_SUCCESS_BAR = 0.80
WILSON_SUCCESS_LOWER_BAR = 0.60
CONTAMINATION_BAR = 0.10
GUARD_FIRE_BAR = 0.80
PRODUCT_COST_BAR = 1.00      # mandate: strictly below cold on the registered counter
PRODUCT_COST_MAX = 1.15      # a priori materiality bound separating neutral from regression
FETCH_COST_BAR = 0.90        # strictly below cold on live fetches
COLD_SUCCESS_BAR = 0.90
LITERAL_SUCCESS_BAR = 0.10
LEGACY_REGRESSION_FLOOR = 1.00   # legacy control must exceed this at L=2
WILSON_Z = 1.96
TRIALS_PER_CLASS = 12

# F1 fix: the freshness/contamination probe MUST use an id the carrier's inferred
# support accepts (support is ^1[0-9]{1}$ from LEARN_IDS=[11,12,13]). TASK_IDS[0]=14
# is in support and yields a verified baseline on every resource.
IN_SUPPORT_PROBE_ID = TASK_IDS[0]

# Counter-weighting robustness (a priori, declared before any scored run). The
# registered equal-weight counter is preserved; the grid reports whether the
# SIGN of repair-vs-cold is INVARIANT to a monotone reweighting of the four
# components over {1,2,3}^4 (81 vectors). Self-attack (DESIGN): among all integer
# difference vectors that already win at equal weight, the MINIMUM grid fraction
# is 5/9 ~= 0.5556, so any bar <= 0.50 would be non-discriminating (it could
# never select COUNTER-DEPENDENT from the grid). The principled test is therefore
# sign-invariance across the ENTIRE grid: ROBUST requires fraction == 1.0 (no
# permitted reweighting reverses the sign) at both L=2 and L=3, and the
# conservative no-reuse-resolve ratio at L=3 remains < 1.00.
WEIGHT_GRID = (1, 2, 3)
ROBUST_FRACTION_BAR = 1.0

# ---------------------------------------------------------------- substrate --
def build_record(resource: str, rid: int) -> dict:
    s = str(rid)
    if resource == "users":
        return {"id": s, "kind": "user", "name": f"User {rid}", "email": f"user{rid}@example.com"}
    if resource == "posts":
        return {"id": s, "kind": "post", "title": f"Post {rid}", "body": f"Body {rid}"}
    if resource == "comments":
        return {"id": s, "kind": "comment", "author": f"Author {rid}", "text": f"Text {rid}"}
    if resource == "albums":
        return {"id": s, "kind": "album", "title": f"Album {rid}", "owner": f"Owner {rid}"}
    if resource == "photos":
        return {"id": s, "kind": "photo", "caption": f"Caption {rid}", "url": f"img://{rid}"}
    raise KeyError(resource)


class AppState:
    def __init__(self):
        self.perturb = None
        self.noise = False
        self.nonce = 0

    def reset(self):
        self.perturb = None
        self.noise = False
        self.nonce = 0

    def set_perturb(self, cls: str, resource: str, seed: int):
        rng = random.Random(seed)
        cfg = {"class": cls, "resource": resource}
        if cls == "P1-ENDPOINT":
            cfg["new_segment"] = rng.choice(NEW_SEGMENTS)
        self.perturb = cfg


class Handler(BaseHTTPRequestHandler):
    state: AppState = None

    def log_message(self, *args):
        pass

    def _json(self, code: int, body: dict):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_GET(self):
        parts = [p for p in self.path.split("/") if p]
        if len(parts) != 3 or parts[0] != "api":
            self._json(404, {"error": "not found"})
            return
        segment, rid_raw = parts[1], parts[2]
        try:
            rid = int(rid_raw)
        except ValueError:
            self._json(400, {"error": "bad id"})
            return
        cfg = self.state.perturb
        logical = segment
        if cfg and cfg["class"] == "P1-ENDPOINT" and segment == cfg["resource"]:
            self.send_response(301)
            self.send_header("Location", f"/api/{cfg['new_segment']}/{rid}")
            self.end_headers()
            return
        if cfg and cfg["class"] == "P1-ENDPOINT" and segment == cfg["new_segment"]:
            logical = cfg["resource"]
        if logical not in RESOURCES:
            self._json(404, {"error": "unknown resource"})
            return
        if cfg and cfg["class"] == "P3-PERMISSION" and logical == cfg["resource"]:
            if self.headers.get(CONSENT_HEADER) != CONSENT_VALUE:
                self.send_response(403)
                self.send_header("X-Required-Consent", CONSENT_VALUE)
                self.end_headers()
                return
        body = build_record(logical, rid)
        if cfg and cfg["class"] == "P2-STRUCTURE" and logical == cfg["resource"]:
            renamed = {ANCHOR_RENAMED if k == ANCHOR else k: v for k, v in body.items()}
            renamed["schema_version"] = "2"
            body = renamed
        if self.state.noise:
            self.state.nonce += 1
            body = dict(body)
            body["observed_at"] = f"t{self.state.nonce}"
        self._json(200, body)


class LocalApp:
    def __init__(self):
        self.state = AppState()
        Handler.state = self.state
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    @property
    def origin(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


def wait_ready(app: "LocalApp", attempts: int = 100) -> bool:
    for _ in range(attempts):
        r = fetch(app.origin + "/api/albums/1")
        if r.status is not None:
            return True
        time.sleep(0.05)
    return False


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


_OPENER = build_opener(NoRedirect)


class Counters:
    def __init__(self):
        self.http = 0
        self.retrieval = 0
        self.verification = 0
        self.repair = 0

    def product(self) -> int:
        return self.http + self.retrieval + self.verification + self.repair

    def as_dict(self):
        return {"http": self.http, "retrieval": self.retrieval,
                "verification": self.verification, "repair": self.repair,
                "product": self.product()}


class HTTPResult:
    def __init__(self, status, headers, body, error=None):
        self.status = status
        self.headers = headers or {}
        self.body = body
        self.error = error


def fetch(url: str, headers: dict | None = None, counters: Counters | None = None,
          origin: str | None = None) -> HTTPResult:
    if counters is not None:
        counters.http += 1
    req = Request(url, headers=headers or {})
    try:
        with _OPENER.open(req, timeout=5) as resp:
            raw = resp.read().decode()
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                body = None
            return HTTPResult(resp.status, dict(resp.headers), body)
    except HTTPError as exc:
        raw = exc.read().decode() if exc.fp else ""
        try:
            body = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            body = None
        hdrs = dict(exc.headers)
        if origin is not None:
            hdrs["_origin"] = origin
        return HTTPResult(exc.code, hdrs, body, error="HTTPError")
    except URLError as exc:
        return HTTPResult(None, {}, None, error=str(exc))


# ----------------------------------------------------- deterministic guard --
TYPE_MAP = {"str": "string", "int": "integer", "float": "number", "bool": "boolean",
            "NoneType": "null", "list": "array", "dict": "object"}


def flatten(obj, prefix=""):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, list):
        out[prefix] = obj
    else:
        out[prefix] = obj
    return out


def field_type_tokens(obj, prefix=""):
    pairs = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, dict):
                pairs.update(field_type_tokens(v, path))
            elif isinstance(v, list):
                pairs.add((path, "array"))
            else:
                pairs.add((path, TYPE_MAP.get(type(v).__name__, type(v).__name__)))
    elif isinstance(obj, list):
        pairs.add((prefix, "array"))
    else:
        pairs.add((prefix, TYPE_MAP.get(type(obj).__name__, type(obj).__name__)))
    return pairs


def required_token_set(body, required_paths):
    return {(p, t) for (p, t) in field_type_tokens(body) if p in required_paths}


def jaccard(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


class Arm:
    """A fresh kernel + registry + honest counters for one arm on one trial."""

    _seq = 0

    def __init__(self, mech_dicts, reg_dir: Path, tag: str):
        Arm._seq += 1
        self.path = _RUN_DIR / f"reg-{tag}-{Arm._seq:06d}.jsonl"
        self.registry = MechanismRegistry(self.path)
        for m in mech_dicts.values():
            self.registry.upsert(Mechanism(**m))
        self.kernel = SpiderKernel(self.registry, min_confidence=MIN_CONFIDENCE,
                                   counters=TrajectoryCounters())
        self.counters = Counters()
        self.oplog = []

    def note(self, kind: str):
        self.oplog.append(kind)

    def netfetch(self, url, headers=None, origin=None):
        self.note("fetch")
        return fetch(url, headers, self.counters, origin=origin)

    def sync(self):
        c = self.kernel.counters
        self.counters.retrieval = c.retrieval_calls
        self.counters.verification = c.verification_calls
        self.counters.repair = c.repair_attempts

    def target_mech(self, resource):
        for m in self.registry.all():
            if m.intent == f"read_{resource}":
                return m
        return None

    def resolve(self, intent, context, params):
        r = self.kernel.resolve(intent, context, params)
        self.note("resolve")
        self.sync()
        return r

    def verify(self, mid, body, params):
        v = self.kernel.verify(mid, body, params)
        self.note("verify")
        self.sync()
        return v

    def rebind(self, intent, context, params):
        r = self.kernel.rebind(intent, context, params)
        self.note("rebind+resolve")
        self.sync()
        return r

    def charge_repair_attempt(self):
        """Charge exactly one repair attempt WITHOUT the redundant re-resolve.

        The reused probe observation already carries the corrected binding, so
        the repair does not re-derive it (this is the mandate's 'reuse the
        freshness-guard probe observation so retrieval/verification are not
        double-charged')."""
        self.kernel.counters.add("repair_attempts")
        self.note("repair_attempt")
        self.sync()


def make_mech_dicts(origin, counters):
    """Learn all resources from LEARN_IDS with the shipped carrier."""
    k = SpiderKernel(MechanismRegistry(_RUN_DIR / "unused.jsonl"),
                     min_confidence=MIN_CONFIDENCE, counters=TrajectoryCounters())
    mechs, cached = {}, {}
    for r in RESOURCES:
        obs = []
        for rid in LEARN_IDS:
            res = fetch(f"{origin}/api/{r}/{rid}", {}, counters)
            obs.append(Observation(intent=f"read_{r}", state={"resource_type": r},
                                   action={"method": "GET", "url": f"{origin}/api/{r}/{rid}",
                                           "headers": {}},
                                   next_state=res.body or {}, success=(res.status == 200)))
        m = k.distill_parameterized(obs)
        if m is None:
            return None, None
        mechs[r] = m.as_dict()
        cached[r] = field_type_tokens(obs[0].next_state)
    return mechs, cached


def execute_batch(arm: Arm, intent, context, slot, ids, extra_header=None):
    ok = True
    values = []
    for t in ids:
        pid = str(t)
        r = arm.resolve(intent, context, {slot: pid})
        if r.status.name != "EXECUTABLE" or r.bound_action is None:
            ok = False
            values.append(None)
            continue
        headers = dict(r.bound_action.get("headers", {}))
        if extra_header:
            headers.update(extra_header)
        res = arm.netfetch(r.bound_action["url"], headers)
        if res.status != 200 or res.body is None:
            ok = False
            values.append(None)
            continue
        if not arm.verify(r.mechanism_id, res.body, {slot: pid}):
            ok = False
        values.append(res.body.get("id"))
    return ok, values


# ------------------------------------------------------------------ repair --
def guard(cached_tokens, required_paths, failed, arm: Arm, mech, params):
    """Deterministic structural + postcondition freshness guard.

    Fires (stale) iff the live probe is non-200/errored, OR the mechanism's own
    postconditions no longer verify, OR the required-field-filtered structural
    token set has drifted below JACCARD_THRESHOLD. Fields outside the
    mechanism's postcondition paths cannot trigger it.
    """
    if failed.error is not None or failed.status != 200 or failed.body is None:
        return True, {"reason": "non-200", "status": failed.status, "jaccard": None}
    live = required_token_set(failed.body, required_paths)
    cached = {(p, t) for (p, t) in cached_tokens if p in required_paths}
    j = jaccard(cached, live)
    ok = arm.verify(mech.mechanism_id, failed.body, params)
    if (not ok) or j < JACCARD_THRESHOLD:
        return True, {"reason": "postcondition" if not ok else "structure",
                      "status": failed.status, "jaccard": j}
    return False, {"reason": "fresh", "status": failed.status, "jaccard": j}


def local_repair(arm: Arm, mech, resource, slot, probe_id, failed, origin):
    """Class-agnostic local repair driven only by live response signals.

    Branches purely on the observed failure signature:
      * redirect       -> rebind the endpoint segment from ``Location``
      * 403 permission -> attach the server-advertised required header
      * 200 drift      -> re-adopt the live postcondition schema, relocating
                          renamed anchor paths (old literal value -> new key)

    Returns (patched_mechanism, probe_body, probe_header); probe_body is the
    live post-repair observation that the caller reuses (verifies once) as the
    first task read instead of issuing a duplicate request. Never touches
    another resource's mechanism.
    """
    import re as _re

    template_re = _re.compile(r"^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$")
    probe_body = None
    probe_header = {}
    new_template = mech.action_template["url"]
    if failed.status in (301, 302, 303, 307, 308) and failed.headers.get("Location"):
        loc = failed.headers["Location"]
        hop_origin = failed.headers.get("_origin", origin)
        probe = arm.netfetch(hop_origin + loc, {})
        if probe.status != 200 or probe.body is None:
            return None, None, None
        probe_body = probe.body
        new_template = hop_origin + "/".join(loc.split("/")[:-1]) + "/${" + slot + "}"
    elif failed.status == 403:
        req_header = req_value = None
        for k, v in failed.headers.items():
            if k.lower().startswith("x-required-"):
                req_header = "X-" + k[len("x-required-"):]
                req_value = v
        if req_header is None:
            return None, None, None
        probe_header = {req_header: req_value}
        probe = arm.netfetch(new_template.replace("${" + slot + "}", str(probe_id)),
                             probe_header)
        if probe.status != 200 or probe.body is None:
            return None, None, None
        probe_body = probe.body
    elif failed.status == 200 and failed.body is not None:
        probe_body = failed.body
    else:
        return None, None, None

    new_post: dict = {}
    for k, v in mech.postconditions.items():
        if isinstance(v, str) and template_re.match(v):
            new_post[k] = v
        elif probe_body.get(k) == v:
            new_post[k] = v
        else:
            cands = [nk for nk, nv in probe_body.items()
                     if nv == v and nk not in new_post]
            new_post[cands[0] if cands else k] = v

    patched = copy.deepcopy(mech)
    patched.action_template["url"] = new_template
    if probe_header:
        patched.action_template["headers"] = dict(probe_header)
    patched.postconditions = new_post
    return patched, probe_body, probe_header


def run_repair_reuse(app, origin, mechs, cached, resource, mode="reuse"):
    """Treatment. Freshness check is FUSED into the first task read; the repair
    reuses the probe observation and does not issue a duplicate resolve/fetch/
    verify for the first task id.

    mode="reuse":        charge one repair attempt, no redundant re-resolve.
    mode="conservative": also re-resolve through the carrier's rebind (charges
                         the rebind retrieval) -> upper bound on repair cost.
    """
    arm = Arm(mechs, Path("/tmp"), "reuse" if mode == "reuse" else "cons")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    intent = mech.intent
    context = {"resource_type": resource}
    required_paths = set(flatten(mech.postconditions).keys())
    # first task read doubles as the freshness probe (fused: no extra read)
    r0 = arm.resolve(intent, context, {slot: str(TASK_IDS[0])})
    if r0.status.name != "EXECUTABLE" or r0.bound_action is None:
        return {"success": False, "guard_fired": False, "arm": arm, "reason": "not-executable"}
    failed = arm.netfetch(r0.bound_action["url"], r0.bound_action.get("headers", {}),
                          origin=origin)
    stale, ginfo = guard(cached, required_paths, failed, arm, mech, {slot: str(TASK_IDS[0])})
    if not stale:
        # the fused guard probe already resolved, fetched AND verified task 0;
        # it therefore counts toward this arm's success denominator (F6).
        ok, _ = execute_batch(arm, intent, context, slot, TASK_IDS[1:])
        return {"success": bool(ok), "guard_fired": False, "arm": arm, "reason": "fresh"}
    patched, probe_body, probe_header = local_repair(
        arm, mech, resource, slot, TASK_IDS[0], failed, origin)
    if patched is None:
        return {"success": False, "guard_fired": True, "arm": arm, "reason": "repair-failed",
                "guard_info": ginfo}
    arm.registry.upsert(patched)
    if mode == "conservative":
        arm.rebind(intent, context, {slot: str(TASK_IDS[0])})  # charges repair + retrieval
    else:
        arm.charge_repair_attempt()                            # one repair attempt only
    # The reused probe observation is this arm's first task read; verify it so
    # the first task enters the success denominator (F6 fix: the prior runner
    # discarded the fused first task and scored only TASK_IDS[1:]).
    first_ok = False
    if probe_body is not None:
        first_ok = bool(arm.verify(patched.mechanism_id, probe_body,
                                   {slot: str(TASK_IDS[0])}))
    ok, _ = execute_batch(arm, intent, context, slot, TASK_IDS[1:])
    return {"success": bool(first_ok and ok), "guard_fired": True, "arm": arm,
            "reason": "repaired", "guard_info": ginfo}


def run_repair_legacy(app, origin, mechs, cached, resource):
    """Replication control: the PRIOR system. A separate guard probe read is
    issued before the batch, and after repair the full task batch is
    re-executed (the first task id is therefore read twice more)."""
    arm = Arm(mechs, Path("/tmp"), "legacy")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    intent = mech.intent
    context = {"resource_type": resource}
    required_paths = set(flatten(mech.postconditions).keys())
    r0 = arm.resolve(intent, context, {slot: str(TASK_IDS[0])})
    if r0.status.name != "EXECUTABLE" or r0.bound_action is None:
        return {"success": False, "guard_fired": False, "arm": arm, "reason": "not-executable"}
    failed = arm.netfetch(r0.bound_action["url"], r0.bound_action.get("headers", {}),
                          origin=origin)
    stale, ginfo = guard(cached, required_paths, failed, arm, mech, {slot: str(TASK_IDS[0])})
    if stale:
        patched, _pb, _ph = local_repair(arm, mech, resource, slot, TASK_IDS[0], failed, origin)
        if patched is None:
            return {"success": False, "guard_fired": True, "arm": arm, "reason": "repair-failed"}
        arm.registry.upsert(patched)
        arm.rebind(intent, context, {slot: str(TASK_IDS[0])})
    ok, _ = execute_batch(arm, intent, context, slot, TASK_IDS)
    return {"success": ok, "guard_fired": stale, "arm": arm, "reason": "legacy",
            "guard_info": ginfo}


def run_cold(app, origin, resource, ids=None, tag="cold"):
    ids = ids or LEARN_IDS
    arm = Arm({}, Path("/tmp"), tag)
    base = f"{origin}/api/{resource}"
    extra_header = {}
    probe = arm.netfetch(f"{base}/{ids[0]}", {}, origin=origin)
    if probe.status in (301, 302, 303, 307, 308) and probe.headers.get("Location"):
        loc = probe.headers["Location"]
        base = origin + "/".join(loc.split("/")[:-1])
    elif probe.status == 403:
        for k, v in probe.headers.items():
            if k.lower().startswith("x-required-"):
                extra_header["X-" + k[len("x-required-"):]] = v
    elif probe.status != 200:
        return {"success": False, "arm": arm, "reason": "discovery-failed"}
    obs = []
    for rid in ids:
        res = arm.netfetch(f"{base}/{rid}", extra_header)
        if res.status != 200 or res.body is None:
            return {"success": False, "arm": arm, "reason": "observation-failed"}
        obs.append(Observation(intent=f"read_{resource}", state={"resource_type": resource},
                               action={"method": "GET", "url": f"{base}/{rid}",
                                       "headers": dict(extra_header)},
                               next_state=res.body, success=True))
    mech = arm.kernel.distill_parameterized(obs)
    if mech is None:
        return {"success": False, "arm": arm, "reason": "distill-failed"}
    arm.registry.upsert(mech)
    slot = mech.parameter_slots[0]
    ok, _ = execute_batch(arm, mech.intent, {"resource_type": resource}, slot, TASK_IDS)
    return {"success": ok, "arm": arm, "reason": "cold"}


def run_literal(app, origin, mechs, resource):
    arm = Arm(mechs, Path("/tmp"), "literal")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    ok, _ = execute_batch(arm, mech.intent, {"resource_type": resource}, slot, TASK_IDS)
    return {"success": ok, "arm": arm}


def run_norepair(app, origin, mechs, cached, resource):
    arm = Arm(mechs, Path("/tmp"), "norepair")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    required_paths = set(flatten(mech.postconditions).keys())
    r0 = arm.resolve(mech.intent, {"resource_type": resource}, {slot: str(TASK_IDS[0])})
    failed = arm.netfetch(r0.bound_action["url"], r0.bound_action.get("headers", {}),
                          origin=origin) if r0.bound_action else HTTPResult(None, {}, None)
    stale, _ = guard(cached, required_paths, failed, arm, mech, {slot: str(TASK_IDS[0])})
    return {"success": False, "guard_fired": stale, "arm": arm}


def unaffected_behavior(mechs, origin, resource, tag, probe_id):
    """Live behavior of an UNTOUCHED resource under a fixed IN-SUPPORT probe id.

    F1 fix: probe_id must be accepted by the carrier's inferred support. Passing
    the out-of-support literal "1" makes resolve return NO-RESOLVE on every
    resource, so the returned tuple never changes and both contamination metrics
    are pinned at 0.0 by construction. Callers must pass IN_SUPPORT_PROBE_ID.
    """
    arm = Arm(mechs, Path("/tmp"), tag)
    mech = arm.target_mech(resource)
    if mech is None:
        return None
    slot = mech.parameter_slots[0]
    r = arm.resolve(mech.intent, {"resource_type": resource}, {slot: str(probe_id)})
    if r.status.name != "EXECUTABLE" or r.bound_action is None:
        return ("NO-RESOLVE", None, False)
    res = arm.netfetch(r.bound_action["url"], r.bound_action.get("headers", {}))
    if res.status != 200 or res.body is None:
        return (res.status, None, False)
    try:
        verified = arm.verify(r.mechanism_id, res.body, {slot: str(probe_id)})
    except (KeyError, TypeError):
        verified = False
    return (200, res.body.get("id"), verified)


def overbroad_contamination(base_live, origin, resource, patched_mech_dict, probe_id):
    bad = {}
    for rid, md in base_live["mech_dicts"].items():
        md2 = copy.deepcopy(md)
        if md2["intent"] != patched_mech_dict["intent"]:
            md2["postconditions"] = copy.deepcopy(patched_mech_dict["postconditions"])
        bad[rid] = md2
    contam = 0
    for r in RESOURCES:
        if r == resource:
            continue
        post = unaffected_behavior(bad, origin, r, "overbroad", probe_id)
        if post != base_live[r]:
            contam += 1
    return contam


# ------------------------------------------------------------------ trial ---
def run_trial(cls, target, seed, reg_dir):
    app = LocalApp()
    try:
        if not wait_ready(app):
            return {"valid": False, "reason": "server-not-ready"}
        base_counters = Counters()
        mechs, cached = make_mech_dicts(app.origin, base_counters)
        if mechs is None:
            return {"valid": False, "reason": "learn-failed"}
        base_live = {"mech_dicts": {m["mechanism_id"]: m for m in mechs.values()}}
        for r in RESOURCES:
            base_live[r] = unaffected_behavior(mechs, app.origin, r, "base", IN_SUPPORT_PROBE_ID)
        pre_unaffected = {r: base_live[r] for r in RESOURCES}
        app.state.set_perturb(cls, target, seed)
        rep = run_repair_reuse(app, app.origin, copy.deepcopy(mechs), cached[target], target, "reuse")
        cons = run_repair_reuse(app, app.origin, copy.deepcopy(mechs), cached[target], target, "conservative")
        leg = run_repair_legacy(app, app.origin, copy.deepcopy(mechs), cached[target], target)
        cold = run_cold(app, app.origin, target, LEARN_IDS, "cold")
        cold_min = run_cold(app, app.origin, target, LEARN_IDS_MIN, "coldmin")
        cold_deep = run_cold(app, app.origin, target, LEARN_IDS_DEEP, "colddeep")
        lit = run_literal(app, app.origin, copy.deepcopy(mechs), target)
        nor = run_norepair(app, app.origin, copy.deepcopy(mechs), cached[target], target)
        post_dicts = {m.mechanism_id: m.as_dict() for m in rep["arm"].registry.all()}
        base_dicts = base_live["mech_dicts"]
        write_set = sorted(
            mid for mid in set(base_dicts) | set(post_dicts)
            if base_dicts.get(mid) != post_dicts.get(mid))
        contam = 0
        for r in RESOURCES:
            if r == target:
                continue
            post = unaffected_behavior(post_dicts, app.origin, r, "post", IN_SUPPORT_PROBE_ID)
            if post != pre_unaffected[r]:
                contam += 1
        n_unaff = len(RESOURCES) - 1
        patched_mech = rep["arm"].target_mech(target)
        overbroad = None
        if patched_mech is not None:
            overbroad = overbroad_contamination(
                base_live, app.origin, target, patched_mech.as_dict(), IN_SUPPORT_PROBE_ID)
        return {
            "valid": True,
            "class": cls,
            "target": target,
            "repair_success": bool(rep["success"]),
            "repair_guard_fired": bool(rep.get("guard_fired")),
            "repair_reason": rep.get("reason"),
            "conservative_success": bool(cons["success"]),
            "legacy_success": bool(leg["success"]),
            "cold_success": bool(cold["success"]),
            "cold_min_success": bool(cold_min["success"]),
            "cold_deep_success": bool(cold_deep["success"]),
            "literal_success": bool(lit["success"]),
            "norepair_success": bool(nor["success"]),
            "norepair_guard_fired": bool(nor.get("guard_fired")),
            "repair_cost": rep["arm"].counters.as_dict(),
            "conservative_cost": cons["arm"].counters.as_dict(),
            "legacy_cost": leg["arm"].counters.as_dict(),
            "cold_cost": cold["arm"].counters.as_dict(),
            "cold_min_cost": cold_min["arm"].counters.as_dict(),
            "cold_deep_cost": cold_deep["arm"].counters.as_dict(),
            "literal_cost": lit["arm"].counters.as_dict(),
            "repair_oplog": list(rep["arm"].oplog),
            "conservative_oplog": list(cons["arm"].oplog),
            "legacy_oplog": list(leg["arm"].oplog),
            "contamination_n": contam,
            "overbroad_contamination_n": overbroad,
            "write_set_n": len(write_set),
            "unaffected_n": n_unaff,
            "base_liveness": all(v and v[0] == 200 and v[2] for v in
                                 (pre_unaffected[r] for r in RESOURCES)),
        }
    finally:
        app.stop()


def noise_trial(seed):
    app = LocalApp()
    try:
        if not wait_ready(app):
            return {"stale": None, "info": {"error": "server-not-ready"}}
        c = Counters()
        mechs, cached = make_mech_dicts(app.origin, c)
        app.state.noise = True
        arm = Arm(mechs, Path("/tmp"), "noise")
        mech = arm.target_mech("users")
        slot = mech.parameter_slots[0]
        required_paths = set(flatten(mech.postconditions).keys())
        failed = arm.netfetch(f"{app.origin}/api/users/11", {}, origin=app.origin)
        stale, info = guard(cached["users"], required_paths, failed, arm, mech, {slot: "11"})
        return {"stale": stale, "info": info}
    finally:
        app.stop()


def no_perturbation_trial(seed):
    app = LocalApp()
    try:
        if not wait_ready(app):
            return {"stale": None, "info": {"error": "server-not-ready"}}
        c = Counters()
        mechs, cached = make_mech_dicts(app.origin, c)
        arm = Arm(mechs, Path("/tmp"), "nopert")
        mech = arm.target_mech("users")
        slot = mech.parameter_slots[0]
        required_paths = set(flatten(mech.postconditions).keys())
        failed = arm.netfetch(f"{app.origin}/api/users/11", {}, origin=app.origin)
        stale, info = guard(cached["users"], required_paths, failed, arm, mech, {slot: "11"})
        return {"stale": stale, "info": info}
    finally:
        app.stop()


# ---------------------------------------------------------------- wilson ----
def wilson_lower(k, n, z=WILSON_Z):
    if n == 0:
        return 0.0
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, center - margin)


def mean(xs):
    return sum(xs) / len(xs) if xs else None


# ------------------------------------------------- counter-weighting robustness --
def _iter_weight_vectors(grid=WEIGHT_GRID):
    for w1 in grid:
        for w2 in grid:
            for w3 in grid:
                for w4 in grid:
                    yield (w1, w2, w3, w4)


def _dot(weights, vec):
    return sum(w * v for w, v in zip(weights, vec))


def grid_robust(repair_vec, cold_vec, grid=WEIGHT_GRID):
    """Fraction of the predeclared weight grid on which the repair arm's weighted
    product counter is STRICTLY below the cold arm's, given their mean component
    vectors [http, retrieval, verification, repair_attempts]."""
    if repair_vec is None or cold_vec is None or len(repair_vec) != 4 or len(cold_vec) != 4:
        return None
    wins = total = 0
    for w in _iter_weight_vectors(grid):
        total += 1
        if _dot(w, repair_vec) < _dot(w, cold_vec):
            wins += 1
    return wins / total if total else None


def grid_robust_both(repair_vec, cold2_vec, cold3_vec, grid=WEIGHT_GRID):
    """Fraction of the grid on which repair beats cold at BOTH L=2 and L=3."""
    if any(v is None for v in (repair_vec, cold2_vec, cold3_vec)):
        return None
    wins = total = 0
    for w in _iter_weight_vectors(grid):
        total += 1
        r = _dot(w, repair_vec)
        if r < _dot(w, cold2_vec) and r < _dot(w, cold3_vec):
            wins += 1
    return wins / total if total else None


def critical_repair_weight(repair_vec, cold_vec):
    """Smallest repair-attempt weight at which the repair arm stops beating cold,
    holding the other three weights at 1. Reported as the fine-grained analog of
    the coarse grid; > 1.00 means the win tolerates repair_attempts being weighted
    above a single fetch/retrieval/verify call."""
    if repair_vec is None or cold_vec is None:
        return None
    if repair_vec[3] == 0:
        return None
    r0 = repair_vec[0] + repair_vec[1] + repair_vec[2]
    c0 = cold_vec[0] + cold_vec[1] + cold_vec[2]
    return (c0 - r0) / repair_vec[3]


# ------------------------------------------------------- decision (pure) ----
def functional_ok(m):
    return bool(m["M-REPAIR-SUCCESS"] is not None and m["M-REPAIR-SUCCESS"] >= REPAIR_SUCCESS_BAR
                and m["M-REPAIR-SUCCESS-WILSON-LOWER"] >= WILSON_SUCCESS_LOWER_BAR
                and m["M-CONTAMINATION-RATE"] is not None and m["M-CONTAMINATION-RATE"] <= CONTAMINATION_BAR
                and m["M-WRITE-SET-MAX"] is not None and m["M-WRITE-SET-MAX"] <= 1
                and m["M-GUARD-FIRE-RATE"] is not None and m["M-GUARD-FIRE-RATE"] >= GUARD_FIRE_BAR)


def strict_win_robust(m):
    """Does the equal-weight strict win survive the counter-weighting test?"""
    rf = m.get("M-WEIGHT-ROBUST-BOTH")
    cons3 = m.get("M-PRODUCT-RATIO-CONSERVATIVE-L3")
    return bool(rf is not None and rf >= ROBUST_FRACTION_BAR
                and cons3 is not None and cons3 < PRODUCT_COST_BAR)


def cost_verdict(m):
    """Registered staged cost verdict on the equal-weight product counter under
    the mandate's reuse semantics (primary), with the network-fetch counter as
    the operational driver. STRICT-WIN is split by the predeclared
    counter-weighting robustness test (mandate: does the strict win survive?)."""
    if not functional_ok(m):
        return "FUNCTIONAL-FAIL"
    pr2, pr3 = m["M-PRODUCT-RATIO-REUSE-L2"], m["M-PRODUCT-RATIO-REUSE-L3"]
    fr = m["M-COST-FETCH-RATIO-L3"]
    if pr2 is None or pr3 is None or fr is None:
        return "COST-UNKNOWN"
    if pr3 < PRODUCT_COST_BAR and pr2 < PRODUCT_COST_BAR and fr <= FETCH_COST_BAR:
        return "STRICT-WIN-ROBUST" if strict_win_robust(m) else "STRICT-WIN-COUNTER-DEPENDENT"
    if pr3 <= PRODUCT_COST_BAR and pr2 <= PRODUCT_COST_BAR and fr <= FETCH_COST_BAR:
        return "BOUNDED-WIN"
    if max(pr2, pr3) <= PRODUCT_COST_MAX and fr <= FETCH_COST_BAR:
        return "MIXED-TRADEOFF"
    return "COST-FAIL"


def aggregate(cvs):
    """Pure aggregation used both by the scored run and by the synthetic
    decision-branch reachability probe. Only a ROBUST strict win aggregates to
    SUPPORTS; a strict win that is counter-dependent aggregates to MIXED."""
    if any(v == "COST-UNKNOWN" for v in cvs):
        return "INCONCLUSIVE"
    if all(v == "STRICT-WIN-ROBUST" for v in cvs):
        return "SUPPORTS"
    if all(v in ("STRICT-WIN-ROBUST", "STRICT-WIN-COUNTER-DEPENDENT") for v in cvs):
        return "SUPPORTS-COUNTER-DEPENDENT"
    winish = ("STRICT-WIN-ROBUST", "STRICT-WIN-COUNTER-DEPENDENT",
              "BOUNDED-WIN", "MIXED-TRADEOFF")
    if all(v in winish for v in cvs):
        return "MIXED-TRADEOFF"
    if any(v in winish for v in cvs):
        return "MIXED"
    return "FALSIFIES"


# ---------------------------------------------------------------- probes ----
def synthetic_reachability_probe():
    def row(name, reuse_success=True, pr2=0.94, pr3=0.89, fr=0.67, contam=0.0,
            ws=1, guard=1.0, rf=1.0, cons3=0.947):
        return {
            "M-REPAIR-SUCCESS": reuse_success,
            "M-REPAIR-SUCCESS-WILSON-LOWER": 0.7575 if reuse_success else 0.0,
            "M-CONTAMINATION-RATE": contam,
            "M-WRITE-SET-MAX": ws,
            "M-GUARD-FIRE-RATE": guard,
            "M-PRODUCT-RATIO-REUSE-L2": pr2,
            "M-PRODUCT-RATIO-REUSE-L3": pr3,
            "M-COST-FETCH-RATIO-L3": fr,
            "M-WEIGHT-ROBUST-BOTH": rf,
            "M-PRODUCT-RATIO-CONSERVATIVE-L3": cons3,
        }
    cases = {
        "STRICT-WIN-ROBUST": row("robust"),
        "STRICT-WIN-COUNTER-DEPENDENT": row("counter", rf=0.7778),
        "STRICT-WIN-COUNTER-DEPENDENT-CONS": row("countercons", rf=1.0, cons3=1.00),
        "BOUNDED-WIN": row("bounded", pr2=1.00, pr3=0.95),
        "MIXED-TRADEOFF": row("mixed", pr2=1.11, pr3=1.05),
        "COST-FAIL": row("fail", pr2=1.30, pr3=1.25, fr=0.95),
        "FUNCTIONAL-FAIL": row("fnfail", reuse_success=False),
        "COST-UNKNOWN": row("unknown", pr2=None, pr3=None, fr=None),
    }
    verdicts = {k: cost_verdict(v) for k, v in cases.items()}
    aggregates = {
        "SUPPORTS": aggregate(["STRICT-WIN-ROBUST"] * 3),
        "SUPPORTS-COUNTER-DEPENDENT": aggregate(
            ["STRICT-WIN-ROBUST", "STRICT-WIN-COUNTER-DEPENDENT",
             "STRICT-WIN-COUNTER-DEPENDENT"]),
        "MIXED-TRADEOFF": aggregate(["STRICT-WIN-ROBUST", "MIXED-TRADEOFF", "MIXED-TRADEOFF"]),
        "MIXED": aggregate(["STRICT-WIN-ROBUST", "MIXED-TRADEOFF", "COST-FAIL"]),
        "FALSIFIES": aggregate(["COST-FAIL", "COST-FAIL", "FUNCTIONAL-FAIL"]),
        "INCONCLUSIVE": aggregate(["STRICT-WIN-ROBUST", "COST-UNKNOWN", "MIXED-TRADEOFF"]),
    }
    all_verdicts = {"STRICT-WIN-ROBUST", "STRICT-WIN-COUNTER-DEPENDENT", "BOUNDED-WIN",
                    "MIXED-TRADEOFF", "COST-FAIL", "FUNCTIONAL-FAIL", "COST-UNKNOWN"}
    all_aggregates = {"SUPPORTS", "SUPPORTS-COUNTER-DEPENDENT", "MIXED-TRADEOFF", "MIXED",
                      "FALSIFIES", "INCONCLUSIVE"}
    return {
        "class_cost_verdicts": verdicts,
        "aggregate_decisions": aggregates,
        "all_class_branches_reachable": set(verdicts.values()) == all_verdicts,
        "all_aggregate_branches_reachable": set(aggregates.values()) == all_aggregates,
    }


def synthetic_weight_grid_probe():
    """Non-outcome-bearing probe: the weight grid must be able to place the
    sign of repair-vs-cold on BOTH sides of the chosen bar, and the bar itself
    must be above the structural floor (else it could never be discriminating)."""
    # actual measured reuse vector is (http,ret,ver,repair)=(6,5,5,1) for P1/P3;
    # its grid fraction is < 1.0, so the grid CAN select COUNTER-DEPENDENT.
    knife = ([6, 5, 5, 1], [8, 5, 5, 0], [9, 5, 5, 0])
    robust = ([4, 5, 5, 1], [8, 5, 5, 0], [9, 5, 5, 0])
    kb = grid_robust_both(*knife)
    rb = grid_robust_both(*robust)
    # Structural floor: minimum grid fraction among ALL integer difference
    # vectors that already win at equal weight. A bar at or below this floor
    # would be non-discriminating (COUNTER-DEPENDENT unreachable from the grid).
    min_fr = None
    for d1 in range(-6, 7):
        for d2 in range(-6, 7):
            for d3 in range(-6, 7):
                for d4 in range(-6, 7):
                    if d1 + d2 + d3 + d4 >= 0:
                        continue
                    fr = tot = 0
                    for w in _iter_weight_vectors(WEIGHT_GRID):
                        tot += 1
                        if _dot(w, (d1, d2, d3, d4)) < 0:
                            fr += 1
                    f = fr / tot
                    if min_fr is None or f < min_fr:
                        min_fr = f
    return {
        "grid_size": 81,
        "knife_edge_fraction": kb,
        "robust_fraction": rb,
        "robust_fraction_required": ROBUST_FRACTION_BAR,
        "structural_min_fraction_for_equal_weight_win": min_fr,
        "bar_is_discriminating": bool(min_fr is not None and min_fr < ROBUST_FRACTION_BAR),
        "critical_repair_weight_L2": critical_repair_weight(knife[0], knife[1]),
        "critical_repair_weight_L3": critical_repair_weight(knife[0], knife[2]),
        "both_sides_reachable": bool(kb is not None and rb is not None and kb < 1.0 and rb == 1.0),
    }


def synthetic_repair_signal_probe():
    """Non-substrate unit probe: local_repair must produce a patched mechanism
    on each of the three live signal signatures."""
    mech_dict = {
        "mechanism_id": "m-probe", "intent": "read_users",
        "preconditions": {"resource_type": "users"},
        "action_template": {"method": "GET", "url": "http://127.0.0.1:1/api/users/${id}",
                            "headers": {}},
        "postconditions": {"kind": "user", "id": "${id}"},
        "parameter_slots": ["id"], "confidence": 0.95,
    }
    out = {}
    for tag in ("P1", "P3", "P2"):
        app = LocalApp()
        try:
            wait_ready(app)
            md = dict(mech_dict)
            md["action_template"] = {"method": "GET",
                                     "url": f"{app.origin}/api/users/${{id}}", "headers": {}}
            mech = Mechanism(**md)
            arm = Arm({}, Path("/tmp"), "probe")
            arm.registry.upsert(mech)
            if tag == "P1":
                app.state.set_perturb("P1-ENDPOINT", "users", 7)
                seg = app.state.perturb["new_segment"]
                ff = HTTPResult(301, {"Location": f"/api/{seg}/1", "_origin": app.origin}, None)
            elif tag == "P3":
                app.state.set_perturb("P3-PERMISSION", "users", 7)
                ff = HTTPResult(403, {"X-Required-Consent": "granted"}, None)
            else:
                app.state.set_perturb("P2-STRUCTURE", "users", 7)
                ff = HTTPResult(200, {}, {"id": "1", "entity_type": "user", "schema_version": "2"})
            patched, pb, ph = local_repair(arm, mech, "users", "id", 1, ff, app.origin)
            out[tag] = {"patched": patched is not None,
                        "probe_body_present": pb is not None,
                        "probe_header_present": bool(ph)}
        finally:
            app.stop()
    return out


# ---------------------------------------------------------------- main ------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mechanics-only", action="store_true")
    ap.add_argument("--reachability-probe", action="store_true")
    ap.add_argument("--liveness-only", action="store_true")
    args = ap.parse_args()
    reg_dir = Path("/tmp/opencode/exprun382-reg")
    reg_dir.mkdir(parents=True, exist_ok=True)

    runner_self_sha = "UNKNOWN"
    try:
        runner_self_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        pass

    carrier = {
        "kernel_sha256": hashlib.sha256((ROOT / "src/spider/kernel.py").read_bytes()).hexdigest(),
        "models_sha256": hashlib.sha256((ROOT / "src/spider/models.py").read_bytes()).hexdigest(),
        "registry_sha256": hashlib.sha256((ROOT / "src/spider/registry.py").read_bytes()).hexdigest(),
    }

    if args.reachability_probe:
        out = {"status": "DESIGN-REACHABILITY-PROBE", "experiment_id": EXP_ID,
               "lane": "runtime", "runner_self_sha": runner_self_sha,
               "decision_rule": synthetic_reachability_probe(),
               "weight_grid_probe": synthetic_weight_grid_probe(),
               "repair_signal_probe": synthetic_repair_signal_probe()}
        print(json.dumps(out, indent=2))
        return

    if args.mechanics_only:
        canary = []
        for ci, cls in enumerate(CLASSES):
            r = run_trial(cls, TARGETS[ci % len(TARGETS)], SEED + 900 + ci, reg_dir)
            canary.append({k: r[k] for k in (
                "valid", "class", "target", "repair_success", "conservative_success",
                "legacy_success", "cold_success", "literal_success", "repair_guard_fired",
                "contamination_n", "overbroad_contamination_n", "unaffected_n", "base_liveness",
                "repair_cost", "conservative_cost", "legacy_cost", "cold_cost",
                "repair_oplog", "legacy_oplog") if k in r})
        np_t = no_perturbation_trial(SEED + 1)
        nz_t = noise_trial(SEED + 2)
        out = {"status": "DESIGN-MECHANICS-ONLY", "experiment_id": EXP_ID, "lane": "runtime",
               "runner_self_sha": runner_self_sha, "seed": SEED, "carrier": carrier,
               "canary": canary, "nc_no_perturbation": np_t, "nc_noise": nz_t}
        print(json.dumps(out, indent=2))
        return

    if args.liveness_only:
        app = LocalApp()
        try:
            ready = wait_ready(app)
            c = Counters()
            mechs, cached = make_mech_dicts(app.origin, c) if ready else (None, None)
            live = bool(mechs)
            one_ok = False
            in_support_ok = None
            out_of_support_degenerate = None
            if live:
                arm = Arm(mechs, Path("/tmp"), "live")
                mech = arm.target_mech("users")
                slot = mech.parameter_slots[0]
                r = arm.resolve(mech.intent, {"resource_type": "users"}, {slot: str(TASK_IDS[0])})
                if r.status.name == "EXECUTABLE" and r.bound_action is not None:
                    res = arm.netfetch(r.bound_action["url"], r.bound_action.get("headers", {}))
                    one_ok = res.status == 200 and res.body is not None and arm.verify(
                        r.mechanism_id, res.body, {slot: str(TASK_IDS[0])})
                # F1 instrument liveness: in-support baseline is live, the old
                # out-of-support literal "1" is degenerate on every resource.
                in_support = {rr: unaffected_behavior(mechs, app.origin, rr, "liveinst",
                                                      IN_SUPPORT_PROBE_ID) for rr in RESOURCES}
                out_support = {rr: unaffected_behavior(mechs, app.origin, rr, "liveold", "1")
                               for rr in RESOURCES}
                in_support_ok = all(v is not None and v[0] == 200 and v[2] is True
                                    for v in in_support.values())
                out_of_support_degenerate = all(v is not None and v[0] == "NO-RESOLVE"
                                                for v in out_support.values())
            np_t = no_perturbation_trial(SEED + 1) if ready else {"stale": None}
            nz_t = noise_trial(SEED + 2) if ready else {"stale": None}
        finally:
            app.stop()
        print(json.dumps({"status": "DESIGN-LIVENESS-ONLY", "experiment_id": EXP_ID,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "server_ready": ready,
                          "distill_live": bool(mechs),
                          "task_read_verified": bool(one_ok),
                          "in_support_probe_id": IN_SUPPORT_PROBE_ID,
                          "contamination_instrument_live": in_support_ok,
                          "out_of_support_probe_degenerate": out_of_support_degenerate,
                          "nc_no_perturbation_stale": np_t.get("stale"),
                          "nc_noise_stale": nz_t.get("stale"),
                          "carrier": carrier}, indent=2))
        return

    trials = []
    for ci, cls in enumerate(CLASSES):
        for j in range(TRIALS_PER_CLASS):
            target = TARGETS[(ci + j) % len(TARGETS)]
            trials.append(run_trial(cls, target, SEED + 1000 * (ci + 1) + j, reg_dir))
    np_t = no_perturbation_trial(SEED + 1)
    nz_t = noise_trial(SEED + 2)

    per_class = {}
    for cls in CLASSES:
        rows = [r for r in trials if r.get("valid") and r["class"] == cls]
        n = len(rows)
        rep_ok = sum(1 for r in rows if r["repair_success"])
        cold_ok = sum(1 for r in rows if r["cold_success"])
        cold_min_ok = sum(1 for r in rows if r["cold_min_success"])
        cold_deep_ok = sum(1 for r in rows if r["cold_deep_success"])
        lit_ok = sum(1 for r in rows if r["literal_success"])
        nor_ok = sum(1 for r in rows if r["norepair_success"])
        guard_ok = sum(1 for r in rows if r["repair_guard_fired"])
        contam = sum(r["contamination_n"] for r in rows)
        unaff = sum(r["unaffected_n"] for r in rows)
        overbroad = mean([r["overbroad_contamination_n"] for r in rows
                          if r.get("overbroad_contamination_n") is not None])
        write_ws = [r.get("write_set_n") for r in rows if r.get("write_set_n") is not None]
        rep_prod = mean([r["repair_cost"]["product"] for r in rows])
        cons_prod = mean([r["conservative_cost"]["product"] for r in rows])
        leg_prod = mean([r["legacy_cost"]["product"] for r in rows])
        cold_prod = mean([r["cold_cost"]["product"] for r in rows])
        cold_min_prod = mean([r["cold_min_cost"]["product"] for r in rows])
        cold_deep_prod = mean([r["cold_deep_cost"]["product"] for r in rows])
        rep_http = mean([r["repair_cost"]["http"] for r in rows])
        cold_http = mean([r["cold_cost"]["http"] for r in rows])
        base_live_true = sum(1 for r in rows if r.get("base_liveness"))

        def cvec(arm_key):
            return [mean([r[arm_key]["http"] for r in rows]),
                    mean([r[arm_key]["retrieval"] for r in rows]),
                    mean([r[arm_key]["verification"] for r in rows]),
                    mean([r[arm_key]["repair"] for r in rows])]

        rep_vec = cvec("repair_cost")
        cons_vec = cvec("conservative_cost")
        cold_vec = cvec("cold_cost")
        cold_min_vec = cvec("cold_min_cost")
        cold_deep_vec = cvec("cold_deep_cost")

        def ratio(a, b):
            return (a / b) if (a is not None and b) else None

        per_class[cls] = {
            "n": n,
            "M-REPAIR-SUCCESS": rep_ok / n if n else None,
            "M-REPAIR-SUCCESS-WILSON-LOWER": wilson_lower(rep_ok, n),
            "M-COLD-SUCCESS": cold_ok / n if n else None,
            "M-COLD-MIN-SUCCESS": cold_min_ok / n if n else None,
            "M-COLD-DEEP-SUCCESS": cold_deep_ok / n if n else None,
            "M-LITERAL-REPLAY-SUCCESS": lit_ok / n if n else None,
            "M-NO-REPAIR-SUCCESS": nor_ok / n if n else None,
            "M-GUARD-FIRE-RATE": guard_ok / n if n else None,
            "M-CONTAMINATION-RATE": contam / unaff if unaff else None,
            "M-CONTAMINATION-PROBES": unaff,
            "M-OVERBROAD-CONTAMINATION-RATE": overbroad,
            "M-BASE-LIVENESS-TRUE-TRIALS": base_live_true,
            "M-WRITE-SET-MEAN": mean(write_ws),
            "M-WRITE-SET-MAX": max(write_ws) if write_ws else None,
            "M-COST-REPAIR-REUSE-PRODUCT": rep_prod,
            "M-COST-REPAIR-CONSERVATIVE-PRODUCT": cons_prod,
            "M-COST-REPAIR-LEGACY-PRODUCT": leg_prod,
            "M-COST-COLD-PRODUCT": cold_prod,
            "M-COST-COLD-MIN-PRODUCT": cold_min_prod,
            "M-COST-COLD-DEEP-PRODUCT": cold_deep_prod,
            "M-COST-REPAIR-REUSE-VECTOR": rep_vec,
            "M-COST-REPAIR-CONSERVATIVE-VECTOR": cons_vec,
            "M-COST-COLD-MIN-VECTOR": cold_min_vec,
            "M-COST-COLD-VECTOR": cold_vec,
            "M-COST-COLD-DEEP-VECTOR": cold_deep_vec,
            "M-PRODUCT-RATIO-REUSE-L3": ratio(rep_prod, cold_prod),
            "M-PRODUCT-RATIO-REUSE-L2": ratio(rep_prod, cold_min_prod),
            "M-PRODUCT-RATIO-REUSE-L4": ratio(rep_prod, cold_deep_prod),
            "M-PRODUCT-RATIO-CONSERVATIVE-L3": ratio(cons_prod, cold_prod),
            "M-PRODUCT-RATIO-CONSERVATIVE-L2": ratio(cons_prod, cold_min_prod),
            "M-PRODUCT-RATIO-LEGACY-L3": ratio(leg_prod, cold_prod),
            "M-PRODUCT-RATIO-LEGACY-L2": ratio(leg_prod, cold_min_prod),
            "M-COST-REPAIR-FETCH": rep_http,
            "M-COST-COLD-FETCH": cold_http,
            "M-COST-FETCH-RATIO-L3": ratio(rep_http, cold_http),
            "M-WEIGHT-ROBUST-L2": grid_robust(rep_vec, cold_min_vec),
            "M-WEIGHT-ROBUST-L3": grid_robust(rep_vec, cold_vec),
            "M-WEIGHT-ROBUST-BOTH": grid_robust_both(rep_vec, cold_min_vec, cold_vec),
            "M-WEIGHT-CRITICAL-REPAIR-WEIGHT-L2": critical_repair_weight(rep_vec, cold_min_vec),
            "M-WEIGHT-CRITICAL-REPAIR-WEIGHT-L3": critical_repair_weight(rep_vec, cold_vec),
            "M-OPLOG-REPAIR-LEN-MEAN": mean([len(r.get("repair_oplog", [])) for r in rows]),
            "M-OPLOG-LEGACY-LEN-MEAN": mean([len(r.get("legacy_oplog", [])) for r in rows]),
            "M-OPLOG-PRESENT": all(bool(r.get("repair_oplog")) and bool(r.get("legacy_oplog"))
                                   for r in rows),
        }

    overbroad_rate = mean([per_class[c]["M-OVERBROAD-CONTAMINATION-RATE"] for c in CLASSES
                           if per_class[c]["M-OVERBROAD-CONTAMINATION-RATE"] is not None])
    contam_probes_total = sum(per_class[c]["M-CONTAMINATION-PROBES"] for c in CLASSES)
    base_live_true_total = sum(per_class[c]["M-BASE-LIVENESS-TRUE-TRIALS"] for c in CLASSES)
    base_live_total = sum(per_class[c]["n"] for c in CLASSES)

    metrics = {"M-CLASSES": per_class,
               "M-IN-SUPPORT-PROBE-ID": IN_SUPPORT_PROBE_ID,
               "M-CONTAMINATION-PROBES-TOTAL": contam_probes_total,
               "M-OVERBROAD-CONTAMINATION-RATE-MEAN": overbroad_rate,
               "M-BASE-LIVENESS-TRUE-TRIALS-TOTAL": base_live_true_total,
               "M-BASE-LIVENESS-TRIALS-TOTAL": base_live_total,
               "M-NOISE-FALSE-TRIGGER-RATE": (None if nz_t.get("stale") is None
                                              else (1.0 if nz_t["stale"] else 0.0)),
               "M-NO-PERTURBATION-FALSE-TRIGGER-RATE": (None if np_t.get("stale") is None
                                                        else (1.0 if np_t["stale"] else 0.0)),
               "M-LEGACY-REGRESSION-REPRODUCED": all(
                   (per_class[c]["M-PRODUCT-RATIO-LEGACY-L2"] or 0) > LEGACY_REGRESSION_FLOOR
                   for c in CLASSES),
               "M-TRIALS-TOTAL": len(trials)}

    invalid = []
    if any(not r.get("valid") for r in trials):
        invalid.append("trial-invalid")
    if base_live_total == 0 or base_live_true_total < base_live_total:
        invalid.append("positive-control-base-liveness")
    if contam_probes_total <= 0:
        invalid.append("contamination-instrument-degenerate")
    if overbroad_rate is None or overbroad_rate <= CONTAMINATION_BAR:
        invalid.append("nc-overbroad-not-sensitive")
    for cls, m in per_class.items():
        if m["n"] < TRIALS_PER_CLASS:
            invalid.append(f"{cls}:n<{TRIALS_PER_CLASS}")
        if m["M-COLD-SUCCESS"] is None or m["M-COLD-SUCCESS"] < COLD_SUCCESS_BAR:
            invalid.append(f"{cls}:cold-baseline-not-live")
        if m["M-LITERAL-REPLAY-SUCCESS"] is None or m["M-LITERAL-REPLAY-SUCCESS"] > LITERAL_SUCCESS_BAR:
            invalid.append(f"{cls}:perturbation-does-not-bite")
        if m["M-NO-REPAIR-SUCCESS"] is None or m["M-NO-REPAIR-SUCCESS"] > LITERAL_SUCCESS_BAR:
            invalid.append(f"{cls}:no-repair-not-inert")
    if nz_t.get("stale") is not False or np_t.get("stale") is not False:
        invalid.append("negative-control-not-fresh")

    cvs = {cls: cost_verdict(per_class[cls]) for cls in CLASSES}
    if invalid:
        decision, status, outcome = None, "MEASUREMENT_INVALID", "INCONCLUSIVE"
    else:
        decision = aggregate(list(cvs.values()))
        status = "COMPLETE"
        # Only a ROBUST strict win aggregates to SUPPORTS; a counter-dependent
        # strict win is reported as MIXED (decision preserves the finer tier).
        outcome = {"SUPPORTS": "SUPPORTS", "SUPPORTS-COUNTER-DEPENDENT": "MIXED",
                   "MIXED-TRADEOFF": "MIXED", "MIXED": "MIXED",
                   "FALSIFIES": "FALSIFIES"}.get(decision, "INCONCLUSIVE")

    out = {"status": status, "experiment_id": EXP_ID, "lane": "runtime",
           "runner_self_sha": runner_self_sha, "seed": SEED,
           "weight_grid": list(WEIGHT_GRID),
           "robust_fraction_bar": ROBUST_FRACTION_BAR,
           "in_support_probe_id": IN_SUPPORT_PROBE_ID,
           "invalid_reasons": invalid, "decision": decision, "outcome": outcome,
           "class_cost_verdicts": cvs, "metrics": metrics, "trials": trials,
           "nc_no_perturbation": np_t, "nc_noise": nz_t, "carrier": carrier}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
<!-- END FROZEN-RUNNER -->
