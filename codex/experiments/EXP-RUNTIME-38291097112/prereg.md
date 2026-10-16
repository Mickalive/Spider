# EXP-RUNTIME-38291097112 preregistration (runtime, design_contract_version 2)

**Status:** frozen design (design_contract_version 2). Do not edit after freeze.

| identity | value |
| --- | --- |
| experiment_id | `EXP-RUNTIME-38291097112` |
| lane | `runtime` |
| design_contract_version | `2` |
| target claim | `C-DELTA-REPAIR` (CONTINUE; parent-handoff disposition **USE**) |
| dependency claims | `C-PRODUCT-ECON`, `C-MEAS-VALID`, `C-PARAM-INHERIT`, `C-FRESHNESS` |
| request `base_sha` | `0c2f8f3bd69383aa51599ba9b085e7979eaf429e` |
| claim_registry_sha256 | `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b` |
| origin_github_run_id | `38291097112` |
| parent_handoff | `EXP-RUNTIME-38244432934` (`sha256 66aaa0097910fd64d40f67770c8a55fd777d8e6b0944973fba573ae29c1309c4`), disposition **USE** |
| parent audit | `EXP-RUNTIME-38244432934/audit.json` status `PASS`, `producer_claim_supported=true` |
| origin of the target question | `request.json.director_mandate` (CONTINUE, `cognitive_reset=true`, IDLE reactivation) |
| CANONICAL-RUNNER-V3-SHA256 | `ec480f38c3c5c2f2bfff282aea3ef75654b0c6d2f4453dbca6d0321f03002229` (filled at end of DESIGN by byte-exact extraction; placeholder replaced before freeze) |
| frozen runner file | `raw_evidence/runner_delta_repair_calibrated_v3.py` (extracted from section 12) |
| immutable substrate reference | `research/experiments/EXP-RUNTIME-38244432934/raw_evidence/runner_delta_repair_reuse_v2.py` (`sha256 d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608`, 60855 bytes; V0 pin gate) |

The Global Research Director mandate (`request.json.director_mandate`, action `CONTINUE`,
claim `C-DELTA-REPAIR`, `parent_handoff_disposition=USE`) is BINDING. Runtime is reactivated
from IDLE on the shared validity blocker both Runtime and Graph handoffs converged on. The
parent packet `EXP-RUNTIME-38244432934` ended `SUPPORTS-COUNTER-DEPENDENT / MIXED` (audit PASS):
the strict equal-weight win reproduces (reuse 17 vs cold 18/19) with a live contamination
instrument (overbroad 4/4 every trial), but the win is NOT sign-invariant across the
predeclared `{1,2,3}^4` weight grid (`M-WEIGHT-ROBUST-BOTH` 0.78/0.67 < 1.0). The mandate's
decision counterfactual therefore lands on the open fork: an independently justified counter
showing strict reuse win at L=2/L=3 re-admits localized repair to the product story with a
stated counter; failure to construct one, or a measured loss under justifiable accounting,
permanently drops local repair from `C-PRODUCT-ECON`. The mandate's stop trigger is honored:
this is NOT another equal-weight-only rerun — the primary surfaces (time-calibrated counter,
measured episode latency) and the decision rule are new.

This experiment does NOT repeat the parent design and does NOT repeat pre-2.0 work (see
section 0, legacy comparison). It holds the substrate, carrier, perturbation classes,
identifier banks, arms and controls fixed and changes only the accounting surface and the
decision rule.

## 0. Preserved parent-handoff distinctions (USE) and legacy comparison

From `EXP-RUNTIME-38244432934/handoff.json` (`carry_forward`), inherited as scientific state:

- **established.** (e1) Measurement-valid transaction at the audited ceiling: `status=COMPLETE /
  outcome=MIXED`, audit `PASS`, V1–V15 all PASS; frozen-input integrity confirmed
  (runner `d4871091...`, carrier `3a6caf97... / 338aaf4d... / 51fb440d...`). (e2) The F1
  instrument defect is corrected: in-support probe id=14, `M-CONTAMINATION-RATE=0.0` (0/144)
  LIVE, overbroad rewrite detected 4/4 every trial. (e3) Functional/locality bars hold:
  repair success 1.0 (Wilson lower 0.7575), guard 1.0, `M-WRITE-SET-MAX=1`, literal-replay 0.0,
  no-repair 0.0, NCs fresh. (e4) Strict equal-weight win reproduces: ratios 0.9444 (L=2) /
  0.8947 (L=3) / 0.85 (L=4); fetch ratio 0.667/0.556 at L=3. (e5) The win is
  counter-dependent: grid fractions 0.7778 (P1/P3) / 0.6667 (P2) < 1.0; critical repair
  weight 2.0 (L=2) / 3.0 (L=3); conservative L=3 ratio 0.9474. (e6) Legacy regression
  reproduced (1.1111 at L=2). (e7) `C-DELTA-REPAIR` remains EXPERIMENTAL; localized repair
  dropped from the product story pending a justified counter.
- **rejected.** (r1) The claim that the strict win is ROBUST (`M-WEIGHT-ROBUST-BOTH == 1.0`)
  is rejected on the registered counter and `{1,2,3}^4` grid. (r2) The reading that the
  ~5.3% regression is removable accounting overhead is NOT supported at the strict level.
  (r3) `SUPPORTS` / `STRICT-WIN-ROBUST` / VALIDATED / PRODUCT_CORE are not licensed for
  this evidence. (r4) None of this closes the repair domain, `C-DELTA-REPAIR`,
  `C-PRODUCT-ECON`, or the possibility that a product-correct counter changes the sign.
- **unknown.** (u1) Is the equal-weight counter the product-correct surface? (u2) Transfer
  to real web / production carrier / external agents? (u3) Fidelity of the legacy
  reconstruction beyond its counter? (u4) B3 (capable credential-free agent endpoint) still
  NOT SATISFIED — no model-call/token economics measurable. (u5) Orthogonal repair
  mechanisms untested.
- **do_not_assume** (preserved in intent). Do NOT report SUPPORTS/ROBUST/VALIDATED for the
  parent; do NOT read the overbroad metric name as a 0–1 fraction (it is a per-trial count
  0–4; substance is 4/4 vs parent 0/4); do NOT generalize ratios beyond this
  substrate/carrier/counter/grid; do NOT treat the packet as failure or falsification; do
  NOT promote to product from runtime; do NOT mutate frozen upstream files; do NOT mutate
  cross-lane claim statuses; do NOT treat counter-dependence as closing the domain; do NOT
  treat this handoff as authorizing a successor without a Director mandate.

**Legacy comparison (binding POLICY.md historical non-duplication check).** Targeted
`codex/legacy_artifact_index.json` search (1401 artifacts): narrow counter-query
(equal-weight / per-operation / product-counter / weight-grid / end-to-end-cost /
amortize) returns **0 hits**; broad repair-query hits are operational recounts and
provenance notes with no cost-counter content. The Director's `comparative_reasoning`
records `LEGACY: NO_MATCH` (only `P2-AUTOMATION`, an operational lesson on request
identity/write sets with no counter content). The guards of `P2-REPLAY-COST` (matched
tasks, fully loaded counterfactuals; never frame scripted replay as agent economics) and
`P2-AUTOMATION` (immutable identity, hash-pinned inheritance, validity/completion
separation) are honored by this design (matched L-budgets, measured counter, V0 pin,
validity-gated verdicts). **Material difference from pre-2.0:** no pre-2.0 artifact
constructed a measured per-operation end-to-end counter or a timed episode-latency
comparison; this design introduces both, so it is a `DISTINCT_EXTENSION`, never a
duplicate — and it never repeats an identical invalid/degenerate design (the one
degenerate ancestor, the parent's out-of-support helper, was already superseded by the
parent itself and is re-verified degenerate at this DESIGN).

## 1. Question

On the same fetch-scarce, credential-free, locally served substrate and the same SHIPPED
carrier held fixed (`src/spider/kernel.py`: `distill_parameterized -> resolve -> execute ->
verify`), with the corrected in-support contamination instrument retained: can an
independently justified end-to-end product-economics counter — time-calibrated
per-operation weights (numeraire: measured fetch cost) plus measured end-to-end episode
latency, with model calls/tokens structurally 0 (B3 NOT SATISFIED, carried as unknown) — be
constructed and measured so that reuse-based localized repair is or is not strictly cheaper
than cold re-derivation at L=2 and L=3, i.e. is the observed equal-weight
counter-dependence a genuine product-economics boundary or an artifact of an equal-weight
counter no external agent actually uses — and should localized repair therefore be
permanently dropped from the `C-PRODUCT-ECON` product story?

## 2. Hypotheses

- `H1 (functional/locality gates, re-attested).` After a single LOCAL perturbation, reuse
  repair restores success on ALL FIVE `TASK_IDS=[14,15,16,17,18]` at rate >= 0.80 per class
  (Wilson 95% lower >= 0.60), guard fires >= 0.80, write set <= 1, same-target contamination
  <= 0.10 (in-support probe), overbroad rewrite detected > 0.10 — for `P1-ENDPOINT`,
  `P2-STRUCTURE`, `P3-PERMISSION`.
- `H2 (calibrated counter).` Under the independently time-calibrated per-operation counter
  (Stage-A calibration medians; weights `w=(1, m_resolve/m_fetch, m_verify/m_fetch,
  m_repair/m_fetch)`, fetch numeraire), the reuse weighted product is STRICTLY below cold
  at BOTH L=2 and L=3 (`M-CALIBRATED-WIN=true`).
- `H3 (end-to-end latency).` The median timed-episode latency ratio (reuse/cold) is
  STRICTLY below 1.00 at BOTH L=2 and L=3 (`M-LATENCY-WIN=true`).
- `H4 (construction).` Stage-A calibration is live (`calib_ok=true`): server live,
  N=300/class, all medians finite > 0, `perf_counter` resolution <= 1us, bootstrap RSE <=
  0.30 per class. Model calls/tokens are structurally 0 on this substrate (measured, not
  asserted); real model economics is NOT constructed (B3 unknown, out of scope).
- `H5 (replication premise).` `T-REPAIR-LEGACY` still reproduces the prior regression
  (ratio > 1.00 at L=2) and the equal-weight strict win reproduces (reuse 17 vs 18/19).

## 3. Falsifier

With `H1` and a LIVE instrument established on every class:

- re-admission FAILS if `M-CALIBRATED-WIN` is false (reuse >= cold under measured weights
  at L=2 or L=3) or `M-LATENCY-WIN` is false (median latency ratio >= 1.00 at L=2 or L=3):
  `EQUAL-ONLY-MIXED` / measured-loss reading — the counter-dependence is a genuine
  product-economics boundary; drop from the product story;
- it FAILS a fortiori if the equal-weight strict win itself does not reproduce
  (`BOUNDED-WIN` or worse);
- construction failure (`calib_ok=false`) yields NO scientific verdict
  (`MEASUREMENT_INVALID` / `INCONCLUSIVE`, mandate maps to drop-pending-counter), never
  falsification;
- any insensitive control, pin mismatch, or order/warmup violation is
  `MEASUREMENT_INVALID`, never a negative.

## 4. Substrate, banks, perturbation classes, and Stage-A calibration

**Substrate / banks / classes (held fixed from the parent, credential-free, stdlib only).**
In-process `ThreadingHTTPServer` JSON API `/api/<resource>/<id>` over 127.0.0.1, ephemeral
port; five resources; `TASK_IDS=[14,15,16,17,18]`; `LEARN_IDS=[11,12,13]` (L=3),
`LEARN_IDS_MIN=[11,12]` (L=2), `LEARN_IDS_DEEP=[10,11,12,13]` (L=4); support
`^1[0-9]{1}$`; contamination probe `IN_SUPPORT_PROBE_ID=14`; classes P1 (301+Location
rebind), P2 (`kind`->`entity_type` schema re-adoption), P3 (`X-Consent` attach); targets
rotate over users/posts/comments; deterministic guard (`JACCARD_THRESHOLD=0.85`); reuse /
conservative / legacy semantics unchanged (fused probe, +1 retrieval bound, separate-probe
+ full re-execution); physical accounting per fetch/resolve/verify/repair op. No LLM,
credential, external network, browser — hence `model_calls/model_tokens` are structurally
0 (measured per trial from kernel counters, not asserted).

**Stage-A calibration (independent of arm outcomes).** On a fresh UNPERTURBED app, before
any scored trial: `N_CAL=300` timed single ops per class — HTTP fetch (ids cycling
10..18), carrier resolve, carrier verify (on the matching fetched body), and repair
bookkeeping (`charge_repair_attempt`) — via `perf_counter`; plus response bytes per fetch.
Medians `m_fetch/m_resolve/m_verify/m_repair`; bootstrap RSE (`B_CAL=1000`, fixed seed);
weights `w_http=1.0`, `w_ret=m_resolve/m_fetch`, `w_ver=m_verify/m_fetch`,
`w_rep=m_repair/m_fetch` (6dp). Construction bars (V-CALIB): server live, N==300/class,
all medians finite > 0, resolution <= 1us, RSE <= 0.30 each. On failure the scored run
fast-fails (no 15–50 min spent on an undecidable run). Bytes are diagnostic only: no
byte<->time exchange rate is invented.

## 5. Timing protocol and arms

Per scored trial (same app lifecycle/order as the parent, then): 2 excluded warmup
episodes on the PERTURBED substrate (1 reuse + 1 cold-L3, discarded, counted); then the
three decision episodes timed individually with `perf_counter` — treatment
(`t_reuse_s`), cold-L2 (`t_cold_min_s`), cold-L3 (`t_cold_s`) — in predeclared parity
order (even trial index: reuse first; odd: cold first; exactly 6/6 per class); remaining
arms (conservative, legacy, literal, no-repair) untimed in fixed slots; write-set,
contamination and overbroad computed from the timed treatment arm exactly as the parent.
Any timed-episode exception invalidates the trial (`timed-episode-error`). The equal-weight
vectors come from the same calls, so the parent's ratios reproduce in expectation while
timing adds no accounting change.

## 6. Baselines and controls

| id | type | description |
| --- | --- | --- |
| `B-COLD` / `B-COLD-MIN` / `B-COLD-DEEP` | cost baselines | as parent; L=3/L=2 timed (decision denominators), L=4 untimed sensitivity |
| `B-LITERAL-REPLAY` / `B-NO-REPAIR` | must-fail controls | perturbation bites / abstention inert; never denominators |
| `T-REPAIR-REUSE` | treatment | timed; fused-probe reuse semantics |
| `T-REPAIR-CONSERVATIVE` | sensitivity | untimed upper bound; excluded from classifier |
| `T-REPAIR-LEGACY` | replication control | must reproduce prior regression (V13) |
| `PC-BASE-LIVENESS` | positive control | scored in every trial (V12) |
| `NC-NO-PERTURBATION` / `NC-NOISE` | negative controls | must stay fresh (V7) |
| `NC-OVERBROAD-REPAIR` | must-fire control | in-support probe, 4 unaffected resources (V15) |
| `V0-SUBSTRATE-PIN` | provenance gate | parent v2 file hash+size verified before import; mismatch aborts |
| `V-CALIB` | construction gate | Stage-A bars; fast-fail to INCONCLUSIVE on breach |
| `V-TIMING` | timing-integrity gate | 72 warmups, exact 6/6 parity per class, 0 errors, finite timings |

## 7. Decision rule

Per class, on the FROZEN pure classifier:

```
functional_ok := repair_success >= 0.80 AND wilson_lower >= 0.60
             AND contamination_rate <= 0.10 AND write_set_max <= 1
             AND guard_fire_rate >= 0.80          (v2.functional_ok, reused verbatim)
eq := pr_L2 < 1.00 AND pr_L3 < 1.00 AND fetch_L3 <= 0.90     (parent strict win)
cw := M-CALIBRATED-WIN is True    (measured weights, both budgets)
lw := R_L2 < 1.00 AND R_L3 < 1.00 (median latency ratios, both budgets)
cost_verdict := FUNCTIONAL-FAIL            if not functional_ok
              | STRICT-WIN-MEASURED        if eq AND cw AND lw
              | SINGLE-SURFACE-MIXED       if eq AND (cw XOR lw)
              | EQUAL-ONLY-MIXED           if eq
              | BOUNDED-WIN                if pr_L2 <= 1.00 AND pr_L3 <= 1.00 AND fetch_L3 <= 0.90
              | MIXED-TRADEOFF             if max(pr_L2,pr_L3) <= 1.15 AND fetch_L3 <= 0.90
              | COST-FAIL                  otherwise
              | COST-UNKNOWN               if pr_L2/pr_L3/fetch_L3 is None
```

Aggregate (classes P1/P2/P3):

- any validity gate fails -> `MEASUREMENT_INVALID`, `INCONCLUSIVE`;
- all `STRICT-WIN-MEASURED` -> `SUPPORTS` (`SUPPORTS`);
- all in `{STRICT-WIN-MEASURED, SINGLE-SURFACE-MIXED}` -> `MIXED-PARTIAL` (`MIXED`);
- all in the positive/neutral tiers -> `MIXED-COUNTER-DEPENDENT` (`MIXED`);
- some positive/neutral -> `MIXED` (`MIXED`);
- otherwise -> `FALSIFIES` (`FALSIFIES`).

`T-REPAIR-CONSERVATIVE`/`T-REPAIR-LEGACY` never enter the classifier (legacy only via the
V13 premise). The 81-combo measured-weight band (`{0.5,1,2}^4` scale factors around the
measured weights) is reported (`M-CALIBRATED-ROBUST-BOTH`) but is informational, not a
gate — so no bar can sit at/below a structural floor.

## 8. Design satisfiability probes (non-scored, DESIGN-time)

All probes are non-outcome-bearing: no scored reuse-vs-cold comparison was run or read to
choose any threshold, bar, weight or rule; the scored run re-measures everything
independently at n=12/class (calibration included).

**8.1 Decision-branch reachability (synthetic, non-substrate).** The frozen pure
`cost_verdict_v3` + `aggregate_v3` were driven with synthetic rows: all 8 class branches
`{STRICT-WIN-MEASURED, SINGLE-SURFACE-MIXED, EQUAL-ONLY-MIXED, BOUNDED-WIN,
MIXED-TRADEOFF, COST-FAIL, FUNCTIONAL-FAIL, COST-UNKNOWN}` produced
(`all_class_branches_reachable=True`) and all 6 aggregates `{SUPPORTS, MIXED-PARTIAL,
MIXED-COUNTER-DEPENDENT, MIXED, FALSIFIES, INCONCLUSIVE}` produced
(`all_aggregate_branches_reachable=True`). `SINGLE-SURFACE-MIXED` is reachable from either
surface alone (calibrated-only and latency-only rows both map to it).

**8.2 Calibrated-arithmetic sanity (synthetic).** Parent P1 vectors reuse `(6,5,5,1)` vs
cold `(8,5,5,0)/(9,5,5,0)`: under illustrative time-order weights `(1, 0.005, 0.005,
0.002)` reuse wins both budgets (True, True); under repair-heavy weights `(1,1,1,5)`
reuse loses both (False, False) — `both_sides_exist=True`. The calibrated surface is
capable of placing the verdict on either side; which side it lands on is decided by the
scored-run calibration, not by DESIGN.

**8.3 Substrate/carrier liveness (non-outcome-bearing).** Imports the hash-pinned v2
module, boots the substrate, distills via the shipped carrier: `server_ready=true`,
`distill_live=true`, in-support probe (id=14) `(200, verified True)` on all 5 resources
(`contamination_instrument_live=true`), out-of-support id=`1` `NO-RESOLVE` everywhere
(`out_of_support_probe_degenerate=true`, F1 re-verified), `perf_counter` resolution 1ns.

**8.4 Mini-calibration feasibility (N=60, non-scored).** All four per-op medians resolve
finite > 0: fetch ~388us, resolve ~45us, verify ~40us, repair-bookkeeping ~0.25us; median
78 bytes/fetch. Timer granularity (1ns) is >2 orders of magnitude below the smallest
median, so RSE<=0.30 at N=300 is feasible; no threshold was fitted from these numbers
(the scored calibration re-measures at N=300 with fixed seeds).

**8.5 Trial-pattern smoke test (1 P1 trial, non-scored).** The exact v3 pattern — perturb,
2 warmups, parity-order timed episodes, untimed arms, write-set/contamination/overbroad
from the timed arm — runs valid end-to-end: `smoke_valid=true`, `warmups_done=2`,
`order_rep_first=true`, timings finite > 0, `base_liveness=true`, `write_set_n=1`,
`contamination_n=0`, `overbroad_n=4`, oplogs present. No cost ratio or success rate was
read from this trial (only shape/validity flags); the scored run re-measures all of it.

**8.6 Non-fitted thresholds.** `PRODUCT_COST_BAR=1.00`, `FETCH_COST_BAR=0.90`,
`PRODUCT_COST_MAX=1.15`, `LEGACY_REGRESSION_FLOOR=1.00` inherited unchanged;
`N_CAL=300`, `B_CAL=1000`, `B_LAT=2000`, `RSE_BAR=0.30`, `TIMER_RES_BAR=1us`, parity
order, median statistic and the weight-derivation rule declared before any scored run.

**8.7 DESIGN self-attack (satisfiability).** (i) Empty branches: none — §8.1 proves all 14
reachable; the two-surface conjunction keeps both SUPPORTS and MIXED genuinely reachable
(latency effect ~5–15% vs comparable per-episode noise is flippable either way; the
calibrated surface is decided by scored data per §8.2). (ii) Treatment/comparator
identity: same carrier/substrate/seeds/perturbations; physical op-count difference only;
oplogs emitted (V14). (iii) Ceiling: success rates at 1.0 are gates, not the advantage;
cost range live (17/18/19/20) plus continuous latency. (iv) Floor: no gate sits on a
structural floor (bars are strict inequalities on live quantities; the band is
informational). (v) Insensitive controls: every control verified live at DESIGN (§8.3,
§8.5). (vi) Missing prerequisites: none — no external bank/dataset/model needed; B3
remains an explicit unknown, not an assumed prerequisite. (vii) Mutable dependencies: all
three carrier files bound (re-verified hashes §10); v3 driver embedded (§12) and
hash-bound; v2 reference immutable and pin-gated.

## 9. Measurement validity gates

- `V0-SUBSTRATE-PIN`: v2 file bytes/Hash equal the pin before import; else abort.
- `V1-FREEZE_BINDING`: extracted v3 driver hashes to `CANONICAL-RUNNER-V3-SHA256`;
  request/spec/prereg/carrier hashes match `freeze.json`.
- `V2-SUBSTRATE_ISOLATION`: stdlib only; fresh per-trial app; no cross-arm leakage
  (fresh Arms/registries per call); no LLM/network/credential/browser.
- `V3'-DETERMINISM-PROJECTION`: fixed seeds everywhere (bootstrap included); discrete
  projection recorded for audit; wall-clock quantities excluded from identity by
  construction.
- `V4-PERTURBATION_BITES`: literal-replay <= 0.10 every class.
- `V5-COLD_BASELINE_LIVE`: cold success >= 0.90 every class.
- `V6-NO_REPAIR_INERT`: no-repair success <= 0.10; never a denominator.
- `V7-GUARD_LIVENESS`: guard >= 0.80 perturbed AND fresh on both NCs.
- `V8-NO_TARGET_LEAKAGE`: write_set_max <= 1; contamination only on unaffected resources.
- `V9-INTEGER_COUNTERS`: integer carrier counters; latency in seconds; model counts
  measured from kernel counters (expected structurally 0).
- `V10-THRESHOLD_NOT_FITTED`: preregistered bars/grids/seeds/weight rule; calibration
  independent of arm outcomes.
- `V11-N_CONTROLLED`: 12 trials/class rotating targets; N_CAL=300; 2 warmups/trial.
- `V12-POSITIVE_CONTROL`: base-liveness true in EVERY valid scored trial.
- `V13-LEGACY_REPRODUCTION`: legacy L=2 ratio > 1.00 (reported caveat on failure).
- `V14-REUSE_IDENTITY`: shared seeds/substrate/baseline; oplogs present every trial.
- `V15-CONTAMINATION-INSTRUMENT-LIVE`: probes > 0 AND overbroad rate > 0.10.
- `V-CALIB-CONSTRUCTION`: §4 bars; breach fast-fails to `MEASUREMENT_INVALID` /
  `INCONCLUSIVE` (mandate: drop-pending-counter), never falsification.
- `V-TIMING`: warmups == 72; per-class parity exactly 6/6; timed errors == 0; all
  latencies finite > 0.

## 10. Freeze artifacts and canonical hashes

Mutable local interpretation dependencies (hashed into `freeze.json.artifact_hashes`):

- `src/spider/kernel.py` (`sha256 3a6caf970f5c86db19419f7ae57c7125f409eceba922eb2d5a9f5964140bb1b3`)
- `src/spider/models.py` (`sha256 338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78`)
- `src/spider/registry.py` (`sha256 51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c`)

Executable decision path: embedded verbatim in section 12, bound by
`CANONICAL-RUNNER-V3-SHA256 = ec480f38c3c5c2f2bfff282aea3ef75654b0c6d2f4453dbca6d0321f03002229` and by `freeze.json.hashes.prereg.md`.
Immutable reference (NOT a freeze artifact): the parent v2 runner, pinned by path + hash
+ 60855 bytes and enforced by the V0 gate. No external task bank, dataset or fixture is
read; substrate and calibration are constructed inside the runner.

## 11. Environment and EXECUTE command

Python 3.12, stdlib only. After freeze, EXECUTE extracts the runner by the literal marker
split `content.split("<!-- BEGIN FROZEN-RUNNER -->\n", 1)[1].split("<!-- END FROZEN-RUNNER -->", 1)[0]`
(preserving the runner's trailing newline), writes those exact bytes to
`raw_evidence/runner_delta_repair_calibrated_v3.py`, verifies sha256 equals
`CANONICAL-RUNNER-V3-SHA256 = ec480f38c3c5c2f2bfff282aea3ef75654b0c6d2f4453dbca6d0321f03002229`, then runs pre-flight gates
(non-outcome-bearing; abort on failure) followed by the scored run:

```
python raw_evidence/runner_delta_repair_calibrated_v3.py --reachability-probe | tee raw_evidence/preflight_reachability.json
python raw_evidence/runner_delta_repair_calibrated_v3.py --liveness-only | tee raw_evidence/preflight_liveness.json
python raw_evidence/runner_delta_repair_calibrated_v3.py | tee raw_evidence/runner_result_raw.json
```

The runner prints a single JSON object on stdout per invocation. `--mechanics-only` is the
non-scored determinism-projection canary (discrete projection only; wall-clock quantities
excluded by construction). `result.json` MUST transcribe the frozen raw values exactly, in
particular `M-REPAIR-SUCCESS-WILSON-LOWER` and the latency CIs, and MUST NOT restate the
parent packet's established/rejected distinctions as its own. `model_calls/model_tokens`
MUST be transcribed as measured (expected 0) with the B3 unknown preserved.

## 12. FROZEN-RUNNER
<!-- BEGIN FROZEN-RUNNER -->
#!/usr/bin/env python3
# FROZEN RUNNER v3 for EXP-RUNTIME-38291097112 (runtime, design_contract_version 2).
# C-DELTA-REPAIR, CONTINUE of EXP-RUNTIME-38244432934 (audit PASS, SUPPORTS-COUNTER-DEPENDENT).
#
# Question (Director mandate): with substrate/carrier/classes/banks/arms held fixed,
# can an INDEPENDENTLY JUSTIFIED end-to-end product-economics counter be constructed
# and measured so that reuse-based localized repair is or is not strictly cheaper
# than cold re-derivation at L=2 and L=3?
#
# Two new accounting surfaces (neither re-tuned; both preregistered):
#   (A) CALIBRATED counter: Stage-A calibration workload (N_CAL=300 timed single ops
#       per class on an UNPERTURBED substrate: HTTP fetch, carrier resolve, carrier
#       verify, repair bookkeeping) yields medians m_*; weights w=(1,
#       m_resolve/m_fetch, m_verify/m_fetch, m_repair/m_fetch) with fetch numeraire.
#       The weights come from an INDEPENDENT workload, never from arm outcomes.
#   (B) LATENCY surface: per-trial timed episodes (perf_counter) for the treatment
#       and both cold budgets, in predeclared parity order after 2 excluded warmups.
# Model calls/tokens are MEASURED from kernel counters (structurally 0: no LLM exists
# on this substrate; B3-gated real model economics is out of scope, carried unknown).
#
# Substrate/arms/controls reuse the IMMUTABLE parent v2 module, imported by exact
# path ONLY after the V0 pin check (sha256 + byte size) refuses on mismatch.
# Stdlib only. No credentials, no external network, no LLM, no browser.
# Usage (stdout is always a single JSON object):
#   python runner_delta_repair_calibrated_v3.py                      # scored run
#   python runner_delta_repair_calibrated_v3.py --mechanics-only     # canary (discrete projection)
#   python runner_delta_repair_calibrated_v3.py --reachability-probe # synthetic classifier probes
#   python runner_delta_repair_calibrated_v3.py --liveness-only      # non-outcome-bearing liveness
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import random
import statistics
import sys
import time
from pathlib import Path

EXP_ID3 = "EXP-RUNTIME-38291097112"
SEED3 = 3931358744  # 38291097112 % 2**32
V2_PIN_SHA = "d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608"
V2_PIN_BYTES = 60855
N_CAL = 300
B_CAL = 1000
B_LAT = 2000
RSE_BAR = 0.30
TIMER_RES_BAR = 1e-6


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in (here.parent, *here.parents):
        if (p / "src" / "spider" / "kernel.py").is_file():
            return p
    return Path("/home/runner/work/Spider/Spider")


REPO = _repo_root()
V2_PATH = REPO / "research/experiments/EXP-RUNTIME-38244432934/raw_evidence/runner_delta_repair_reuse_v2.py"


def _load_v2():
    raw = V2_PATH.read_bytes()
    if len(raw) != V2_PIN_BYTES or hashlib.sha256(raw).hexdigest() != V2_PIN_SHA:
        raise SystemExit("V0-SUBSTRATE-PIN failure: parent v2 runner mismatch; refusing to run.")
    spec = importlib.util.spec_from_file_location("v2frozen", str(V2_PATH))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v2 = _load_v2()

CLASSES = v2.CLASSES
TARGETS = v2.TARGETS
TRIALS_PER_CLASS = v2.TRIALS_PER_CLASS


# ------------------------------------------------------------- pure helpers --
def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return None
    m = n // 2
    return float(xs[m]) if n % 2 else (xs[m - 1] + xs[m]) / 2.0


def _bootstrap_median_rse(samples, seed, B):
    rng = random.Random(seed)
    n = len(samples)
    meds = [_median([samples[rng.randrange(n)] for _ in range(n)]) for _ in range(B)]
    mu = sum(meds) / len(meds)
    if not mu:
        return None
    var = sum((x - mu) ** 2 for x in meds) / len(meds)
    return math.sqrt(var) / mu


def _median_ratio_ci(rs, cs, seed, B):
    rng = random.Random(seed)
    n = len(rs)
    out = []
    for _ in range(B):
        r = _median([rs[rng.randrange(n)] for _ in range(n)])
        c = _median([cs[rng.randrange(n)] for _ in range(n)])
        out.append(r / c)
    out.sort()
    return out[int(0.025 * B)], out[int(0.975 * B) - 1]


def _dot(w, v):
    return sum(a * b for a, b in zip(w, v))


def _calibrated_band_fraction(rep_vec, c2_vec, c3_vec, w):
    scales = (0.5, 1.0, 2.0)
    wins = total = 0
    for s1 in scales:
        for s2 in scales:
            for s3 in scales:
                for s4 in scales:
                    ww = (w[0] * s1, w[1] * s2, w[2] * s3, w[3] * s4)
                    total += 1
                    if _dot(ww, rep_vec) < _dot(ww, c2_vec) and _dot(ww, rep_vec) < _dot(ww, c3_vec):
                        wins += 1
    return wins / total if total else None


# ------------------------------------------------------- Stage-A calibration --
def calibrate(n=N_CAL):
    reasons = []
    app = v2.LocalApp()
    try:
        ready = v2.wait_ready(app)
        if not ready:
            return {"calib_ok": False, "reasons": ["server-not-ready"], "n_cal": n}
        mechs, cached = v2.make_mech_dicts(app.origin, v2.Counters())
        if mechs is None:
            return {"calib_ok": False, "reasons": ["learn-failed"], "n_cal": n}
        arm = v2.Arm(mechs, Path("/tmp"), "calib")
        mech = arm.target_mech("users")
        slot = mech.parameter_slots[0]
        intent, ctx = mech.intent, {"resource_type": "users"}
        bodies = {}
        fts, rts, vts, pts, byts = [], [], [], [], []
        for k in range(n):
            rid = 10 + (k % 9)
            t0 = time.perf_counter()
            res = arm.netfetch(f"{app.origin}/api/users/{rid}", {}, origin=app.origin)
            fts.append(time.perf_counter() - t0)
            if res.body is not None:
                bodies[rid] = res.body
                byts.append(len(json.dumps(res.body)))
        for k in range(n):
            rid = 10 + (k % 9)
            t0 = time.perf_counter()
            arm.resolve(intent, ctx, {slot: str(rid)})
            rts.append(time.perf_counter() - t0)
        for k in range(n):
            rid = 10 + (k % 9)
            body = bodies.get(rid)
            if body is None:
                return {"calib_ok": False, "reasons": ["calibration-body-missing"], "n_cal": n}
            t0 = time.perf_counter()
            arm.verify(mech.mechanism_id, body, {slot: str(rid)})
            vts.append(time.perf_counter() - t0)
        for _ in range(n):
            t0 = time.perf_counter()
            arm.charge_repair_attempt()
            pts.append(time.perf_counter() - t0)
        meds = {"fetch": _median(fts), "resolve": _median(rts),
                "verify": _median(vts), "repair": _median(pts)}
        if any(m is None for m in meds.values()):
            reasons.append("empty-sample")
        elif not all(math.isfinite(m) and m > 0 for m in meds.values()):
            reasons.append("non-positive-median")
        rses = {k: _bootstrap_median_rse(v, SEED3 + 11 + i, B_CAL)
                for i, (k, v) in enumerate((("fetch", fts), ("resolve", rts),
                                            ("verify", vts), ("repair", pts)))}
        if any(r is None or not math.isfinite(r) for r in rses.values()):
            reasons.append("rse-indeterminate")
        elif any(r > RSE_BAR for r in rses.values()):
            reasons.append("rse-above-bar")
        resolution = time.get_clock_info("perf_counter").resolution
        if not (math.isfinite(resolution) and resolution <= TIMER_RES_BAR):
            reasons.append("timer-insufficient")
        ok = not reasons
        weights = [1.0,
                   round(meds["resolve"] / meds["fetch"], 6),
                   round(meds["verify"] / meds["fetch"], 6),
                   round(meds["repair"] / meds["fetch"], 6)] if ok else [None, None, None, None]
        return {"calib_ok": bool(ok), "reasons": reasons, "n_cal": n,
                "medians_s": meds, "rse": rses, "weights": weights,
                "bytes_median": _median(byts), "timer_resolution_s": resolution}
    finally:
        app.stop()


# ------------------------------------------------------------- timed trial ---
def _timed(fn, *a, **k):
    t0 = time.perf_counter()
    out = fn(*a, **k)
    return out, time.perf_counter() - t0


def run_trial_v3(cls, target, seed, j):
    app = v2.LocalApp()
    try:
        if not v2.wait_ready(app):
            return {"valid": False, "reason": "server-not-ready"}
        mechs, cached = v2.make_mech_dicts(app.origin, v2.Counters())
        if mechs is None:
            return {"valid": False, "reason": "learn-failed"}
        base_live = {"mech_dicts": {m["mechanism_id"]: m for m in mechs.values()}}
        for r in v2.RESOURCES:
            base_live[r] = v2.unaffected_behavior(mechs, app.origin, r, "base", v2.IN_SUPPORT_PROBE_ID)
        pre_unaffected = {r: base_live[r] for r in v2.RESOURCES}
        app.state.set_perturb(cls, target, seed)
        try:
            v2.run_repair_reuse(app, app.origin, copy.deepcopy(mechs), cached[target], target, "reuse")
            v2.run_cold(app, app.origin, target, v2.LEARN_IDS, "warmcold")
            warmups = 2
            rep_first = (j % 2 == 0)
            if rep_first:
                rep, t_rep = _timed(v2.run_repair_reuse, app, app.origin,
                                    copy.deepcopy(mechs), cached[target], target, "reuse")
                c2, t_c2 = _timed(v2.run_cold, app, app.origin, target, v2.LEARN_IDS_MIN, "coldmin")
                c3, t_c3 = _timed(v2.run_cold, app, app.origin, target, v2.LEARN_IDS, "cold")
            else:
                c3, t_c3 = _timed(v2.run_cold, app, app.origin, target, v2.LEARN_IDS, "cold")
                c2, t_c2 = _timed(v2.run_cold, app, app.origin, target, v2.LEARN_IDS_MIN, "coldmin")
                rep, t_rep = _timed(v2.run_repair_reuse, app, app.origin,
                                    copy.deepcopy(mechs), cached[target], target, "reuse")
            cons = v2.run_repair_reuse(app, app.origin, copy.deepcopy(mechs), cached[target], target, "conservative")
            leg = v2.run_repair_legacy(app, app.origin, copy.deepcopy(mechs), cached[target], target)
            lit = v2.run_literal(app, app.origin, copy.deepcopy(mechs), target)
            nor = v2.run_norepair(app, app.origin, copy.deepcopy(mechs), cached[target], target)
        except Exception as exc:
            return {"valid": False, "reason": "timed-episode-error",
                    "error": type(exc).__name__}
        post_dicts = {m.mechanism_id: m.as_dict() for m in rep["arm"].registry.all()}
        base_dicts = base_live["mech_dicts"]
        write_set = sorted(mid for mid in set(base_dicts) | set(post_dicts)
                           if base_dicts.get(mid) != post_dicts.get(mid))
        contam = 0
        for r in v2.RESOURCES:
            if r == target:
                continue
            post = v2.unaffected_behavior(post_dicts, app.origin, r, "post", v2.IN_SUPPORT_PROBE_ID)
            if post != pre_unaffected[r]:
                contam += 1
        n_unaff = len(v2.RESOURCES) - 1
        patched_mech = rep["arm"].target_mech(target)
        overbroad = None
        if patched_mech is not None:
            overbroad = v2.overbroad_contamination(
                base_live, app.origin, target, patched_mech.as_dict(), v2.IN_SUPPORT_PROBE_ID)
        mcalls = sum(int(getattr(a["arm"].kernel.counters, "model_calls", 0) or 0)
                     for a in (rep, cons, leg, c3, c2) if "arm" in a)
        mtokens = sum(int(getattr(a["arm"].kernel.counters, "model_tokens", 0) or 0)
                      for a in (rep, cons, leg, c3, c2) if "arm" in a)
        return {
            "valid": True, "class": cls, "target": target,
            "repair_success": bool(rep["success"]),
            "repair_guard_fired": bool(rep.get("guard_fired")),
            "repair_reason": rep.get("reason"),
            "conservative_success": bool(cons["success"]),
            "legacy_success": bool(leg["success"]),
            "cold_success": bool(c3["success"]),
            "cold_min_success": bool(c2["success"]),
            "cold_deep_success": None,
            "literal_success": bool(lit["success"]),
            "norepair_success": bool(nor["success"]),
            "norepair_guard_fired": bool(nor.get("guard_fired")),
            "repair_cost": rep["arm"].counters.as_dict(),
            "conservative_cost": cons["arm"].counters.as_dict(),
            "legacy_cost": leg["arm"].counters.as_dict(),
            "cold_cost": c3["arm"].counters.as_dict(),
            "cold_min_cost": c2["arm"].counters.as_dict(),
            "literal_cost": lit["arm"].counters.as_dict(),
            "repair_oplog": list(rep["arm"].oplog),
            "conservative_oplog": list(cons["arm"].oplog),
            "legacy_oplog": list(leg["arm"].oplog),
            "contamination_n": contam,
            "overbroad_contamination_n": overbroad,
            "write_set_n": len(write_set),
            "unaffected_n": n_unaff,
            "base_liveness": all(v and v[0] == 200 and v[2] for v in
                                 (pre_unaffected[r] for r in v2.RESOURCES)),
            "t_reuse_s": t_rep, "t_cold_min_s": t_c2, "t_cold_s": t_c3,
            "order_rep_first": bool(rep_first), "warmups_done": warmups,
            "timed_error": None, "model_calls": mcalls, "model_tokens": mtokens,
        }
    finally:
        app.stop()


# ------------------------------------------------------- decision (pure) ----
def cost_verdict_v3(m):
    if not v2.functional_ok(m):
        return "FUNCTIONAL-FAIL"
    pr2, pr3 = m["M-PRODUCT-RATIO-REUSE-L2"], m["M-PRODUCT-RATIO-REUSE-L3"]
    fr = m["M-COST-FETCH-RATIO-L3"]
    if pr2 is None or pr3 is None or fr is None:
        return "COST-UNKNOWN"
    eq = pr2 < 1.0 and pr3 < 1.0 and fr <= 0.90
    cw = m.get("M-CALIBRATED-WIN") is True
    lw = (m.get("M-LATENCY-R-L2") is not None and m.get("M-LATENCY-R-L3") is not None
          and m["M-LATENCY-R-L2"] < 1.0 and m["M-LATENCY-R-L3"] < 1.0)
    if eq and cw and lw:
        return "STRICT-WIN-MEASURED"
    if eq and (cw ^ lw):
        return "SINGLE-SURFACE-MIXED"
    if eq:
        return "EQUAL-ONLY-MIXED"
    if pr2 <= 1.0 and pr3 <= 1.0 and fr <= 0.90:
        return "BOUNDED-WIN"
    if max(pr2, pr3) <= 1.15 and fr <= 0.90:
        return "MIXED-TRADEOFF"
    return "COST-FAIL"


def aggregate_v3(cvs):
    if any(v == "COST-UNKNOWN" for v in cvs):
        return "INCONCLUSIVE"
    if all(v == "STRICT-WIN-MEASURED" for v in cvs):
        return "SUPPORTS"
    if all(v in ("STRICT-WIN-MEASURED", "SINGLE-SURFACE-MIXED") for v in cvs):
        return "MIXED-PARTIAL"
    winish = ("STRICT-WIN-MEASURED", "SINGLE-SURFACE-MIXED", "EQUAL-ONLY-MIXED",
              "BOUNDED-WIN", "MIXED-TRADEOFF")
    if all(v in winish for v in cvs):
        return "MIXED-COUNTER-DEPENDENT"
    if any(v in winish for v in cvs):
        return "MIXED"
    return "FALSIFIES"


def synthetic_reachability_probe_v3():
    def row(pr2=0.94, pr3=0.89, fr=0.67, ok=True, cw=True, lr2=0.93, lr3=0.90):
        return {"M-REPAIR-SUCCESS": 1.0 if ok else 0.0,
                "M-REPAIR-SUCCESS-WILSON-LOWER": 0.7575 if ok else 0.0,
                "M-CONTAMINATION-RATE": 0.0, "M-WRITE-SET-MAX": 1,
                "M-GUARD-FIRE-RATE": 1.0,
                "M-PRODUCT-RATIO-REUSE-L2": pr2, "M-PRODUCT-RATIO-REUSE-L3": pr3,
                "M-COST-FETCH-RATIO-L3": fr, "M-CALIBRATED-WIN": cw,
                "M-LATENCY-R-L2": lr2, "M-LATENCY-R-L3": lr3}
    cases = {
        "STRICT-WIN-MEASURED": row(),
        "SINGLE-SURFACE-CALIB": row(lr2=1.02),
        "SINGLE-SURFACE-LAT": row(cw=False),
        "EQUAL-ONLY-MIXED": row(cw=False, lr2=1.02, lr3=1.01),
        "BOUNDED-WIN": row(pr2=1.00, pr3=0.95),
        "MIXED-TRADEOFF": row(pr2=1.11, pr3=1.05),
        "COST-FAIL": row(pr2=1.30, pr3=1.25, fr=0.95),
        "FUNCTIONAL-FAIL": row(ok=False),
        "COST-UNKNOWN": row(pr2=None, pr3=None, fr=None),
    }
    verdicts = {k: cost_verdict_v3(v) for k, v in cases.items()}
    aggregates = {
        "SUPPORTS": aggregate_v3(["STRICT-WIN-MEASURED"] * 3),
        "MIXED-PARTIAL": aggregate_v3(["STRICT-WIN-MEASURED", "SINGLE-SURFACE-MIXED",
                                       "SINGLE-SURFACE-MIXED"]),
        "MIXED-COUNTER-DEPENDENT": aggregate_v3(["STRICT-WIN-MEASURED", "EQUAL-ONLY-MIXED",
                                                 "MIXED-TRADEOFF"]),
        "MIXED": aggregate_v3(["STRICT-WIN-MEASURED", "MIXED-TRADEOFF", "COST-FAIL"]),
        "FALSIFIES": aggregate_v3(["COST-FAIL", "COST-FAIL", "FUNCTIONAL-FAIL"]),
        "INCONCLUSIVE": aggregate_v3(["STRICT-WIN-MEASURED", "COST-UNKNOWN", "MIXED-TRADEOFF"]),
    }
    all_class = {"STRICT-WIN-MEASURED", "SINGLE-SURFACE-MIXED", "EQUAL-ONLY-MIXED",
                 "BOUNDED-WIN", "MIXED-TRADEOFF", "COST-FAIL", "FUNCTIONAL-FAIL", "COST-UNKNOWN"}
    all_agg = {"SUPPORTS", "MIXED-PARTIAL", "MIXED-COUNTER-DEPENDENT", "MIXED",
               "FALSIFIES", "INCONCLUSIVE"}
    rep, c2, c3 = (6, 5, 5, 1), (8, 5, 5, 0), (9, 5, 5, 0)
    wt, wh = (1.0, 0.005, 0.005, 0.002), (1.0, 1.0, 1.0, 5.0)
    return {
        "class_cost_verdicts": verdicts,
        "aggregate_decisions": aggregates,
        "all_class_branches_reachable": set(verdicts.values()) == all_class,
        "all_aggregate_branches_reachable": set(aggregates.values()) == all_agg,
        "calibrated_arithmetic": {
            "parent_P1_vectors": {"reuse": list(rep), "cold_L2": list(c2), "cold_L3": list(c3)},
            "time_order_weights_win_L2_L3": [_dot(wt, rep) < _dot(wt, c2),
                                             _dot(wt, rep) < _dot(wt, c3)],
            "repair_heavy_weights_win_L2_L3": [_dot(wh, rep) < _dot(wh, c2),
                                               _dot(wh, rep) < _dot(wh, c3)],
            "both_sides_exist": bool(_dot(wt, rep) < _dot(wt, c2))
            and bool(_dot(wh, rep) >= _dot(wh, c2)),
        },
    }


# ------------------------------------------------------------------ main ----
def _carrier():
    return {
        "kernel_sha256": hashlib.sha256((REPO / "src/spider/kernel.py").read_bytes()).hexdigest(),
        "models_sha256": hashlib.sha256((REPO / "src/spider/models.py").read_bytes()).hexdigest(),
        "registry_sha256": hashlib.sha256((REPO / "src/spider/registry.py").read_bytes()).hexdigest(),
        "v2_runner_sha256": V2_PIN_SHA,
        "v2_runner_bytes": V2_PIN_BYTES,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mechanics-only", action="store_true")
    ap.add_argument("--reachability-probe", action="store_true")
    ap.add_argument("--liveness-only", action="store_true")
    args = ap.parse_args()

    runner_self_sha = "UNKNOWN"
    try:
        runner_self_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        pass
    carrier = _carrier()

    if args.reachability_probe:
        out = {"status": "V3-REACHABILITY-PROBE", "experiment_id": EXP_ID3,
               "lane": "runtime", "runner_self_sha": runner_self_sha,
               "decision_rule": synthetic_reachability_probe_v3(),
               "repair_signal_probe": v2.synthetic_repair_signal_probe()}
        print(json.dumps(out, indent=2))
        return

    if args.liveness_only:
        app = v2.LocalApp()
        try:
            ready = v2.wait_ready(app)
            c = v2.Counters()
            mechs, cached = v2.make_mech_dicts(app.origin, c) if ready else (None, None)
            live = bool(mechs)
            one_ok = in_support_ok = out_deg = None
            if live:
                arm = v2.Arm(mechs, Path("/tmp"), "live3")
                mech = arm.target_mech("users")
                slot = mech.parameter_slots[0]
                r = arm.resolve(mech.intent, {"resource_type": "users"}, {slot: str(v2.TASK_IDS[0])})
                if r.status.name == "EXECUTABLE" and r.bound_action is not None:
                    res = arm.netfetch(r.bound_action["url"], r.bound_action.get("headers", {}))
                    one_ok = res.status == 200 and res.body is not None and arm.verify(
                        r.mechanism_id, res.body, {slot: str(v2.TASK_IDS[0])})
                in_support = {rr: v2.unaffected_behavior(mechs, app.origin, rr, "liveinst",
                                                         v2.IN_SUPPORT_PROBE_ID) for rr in v2.RESOURCES}
                out_support = {rr: v2.unaffected_behavior(mechs, app.origin, rr, "liveold", "1")
                               for rr in v2.RESOURCES}
                in_support_ok = all(v is not None and v[0] == 200 and v[2] is True
                                    for v in in_support.values())
                out_deg = all(v is not None and v[0] == "NO-RESOLVE" for v in out_support.values())
            np_t = v2.no_perturbation_trial(SEED3 + 1) if ready else {"stale": None}
            nz_t = v2.noise_trial(SEED3 + 2) if ready else {"stale": None}
            mini = calibrate(n=60) if ready else {"calib_ok": False, "reasons": ["server-not-ready"]}
        finally:
            app.stop()
        print(json.dumps({"status": "V3-LIVENESS-ONLY", "experiment_id": EXP_ID3,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "server_ready": ready, "distill_live": live,
                          "task_read_verified": bool(one_ok),
                          "in_support_probe_id": v2.IN_SUPPORT_PROBE_ID,
                          "contamination_instrument_live": in_support_ok,
                          "out_of_support_probe_degenerate": out_deg,
                          "nc_no_perturbation_stale": np_t.get("stale"),
                          "nc_noise_stale": nz_t.get("stale"),
                          "timer_resolution_s": time.get_clock_info("perf_counter").resolution,
                          "mini_calibration": mini, "carrier": carrier}, indent=2))
        return

    if args.mechanics_only:
        calib = calibrate()
        canary = []
        for ci, cls in enumerate(CLASSES):
            r = run_trial_v3(cls, TARGETS[ci % len(TARGETS)], SEED3 + 900 + ci, ci)
            canary.append({k: r.get(k) for k in (
                "valid", "class", "target", "order_rep_first", "repair_success",
                "conservative_success", "legacy_success", "cold_success",
                "cold_min_success", "literal_success", "norepair_success",
                "repair_guard_fired", "contamination_n", "overbroad_contamination_n",
                "unaffected_n", "base_liveness", "write_set_n", "repair_cost",
                "conservative_cost", "legacy_cost", "cold_cost", "cold_min_cost",
                "repair_oplog", "legacy_oplog", "warmups_done", "model_calls",
                "timed_error")})
        np_t = v2.no_perturbation_trial(SEED3 + 1)
        nz_t = v2.noise_trial(SEED3 + 2)
        print(json.dumps({"status": "V3-MECHANICS-ONLY", "experiment_id": EXP_ID3,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "seed": SEED3, "carrier": carrier,
                          "calib_ok": calib.get("calib_ok"),
                          "calib_reasons": calib.get("reasons"),
                          "canary": canary, "nc_no_perturbation": np_t,
                          "nc_noise": nz_t}, indent=2))
        return

    calib = calibrate()
    if not calib.get("calib_ok"):
        print(json.dumps({"status": "MEASUREMENT_INVALID", "outcome": "INCONCLUSIVE",
                          "experiment_id": EXP_ID3, "lane": "runtime",
                          "runner_self_sha": runner_self_sha, "seed": SEED3,
                          "invalid_reasons": ["calibration-construction-failed:"
                                              + ",".join(calib.get("reasons", []))],
                          "decision": None, "calibration": calib, "trials": [],
                          "carrier": carrier}, indent=2))
        return
    w = calib["weights"]

    trials = []
    for ci, cls in enumerate(CLASSES):
        for j in range(TRIALS_PER_CLASS):
            target = TARGETS[(ci + j) % len(TARGETS)]
            trials.append(run_trial_v3(cls, target, SEED3 + 1000 * (ci + 1) + j, j))
    np_t = v2.no_perturbation_trial(SEED3 + 1)
    nz_t = v2.noise_trial(SEED3 + 2)

    per_class = {}
    for ci, cls in enumerate(CLASSES):
        rows = [r for r in trials if r.get("valid") and r["class"] == cls]
        n = len(rows)
        rep_ok = sum(1 for r in rows if r["repair_success"])
        cold_ok = sum(1 for r in rows if r["cold_success"])
        cold_min_ok = sum(1 for r in rows if r["cold_min_success"])
        lit_ok = sum(1 for r in rows if r["literal_success"])
        nor_ok = sum(1 for r in rows if r["norepair_success"])
        guard_ok = sum(1 for r in rows if r["repair_guard_fired"])
        contam = sum(r["contamination_n"] for r in rows)
        unaff = sum(r["unaffected_n"] for r in rows)
        overbroad = v2.mean([r["overbroad_contamination_n"] for r in rows
                             if r.get("overbroad_contamination_n") is not None])
        write_ws = [r.get("write_set_n") for r in rows if r.get("write_set_n") is not None]
        rep_prod = v2.mean([r["repair_cost"]["product"] for r in rows])
        cons_prod = v2.mean([r["conservative_cost"]["product"] for r in rows])
        leg_prod = v2.mean([r["legacy_cost"]["product"] for r in rows])
        cold_prod = v2.mean([r["cold_cost"]["product"] for r in rows])
        cold_min_prod = v2.mean([r["cold_min_cost"]["product"] for r in rows])
        rep_http = v2.mean([r["repair_cost"]["http"] for r in rows])
        cold_http = v2.mean([r["cold_cost"]["http"] for r in rows])
        base_live_true = sum(1 for r in rows if r.get("base_liveness"))

        def cvec(arm_key):
            return [v2.mean([r[arm_key]["http"] for r in rows]),
                    v2.mean([r[arm_key]["retrieval"] for r in rows]),
                    v2.mean([r[arm_key]["verification"] for r in rows]),
                    v2.mean([r[arm_key]["repair"] for r in rows])]

        rep_vec = cvec("repair_cost")
        cons_vec = cvec("conservative_cost")
        leg_vec = cvec("legacy_cost")
        cold_vec = cvec("cold_cost")
        cold_min_vec = cvec("cold_min_cost")

        def ratio(a, b):
            return (a / b) if (a is not None and b) else None

        t_rep = [r["t_reuse_s"] for r in rows]
        t_c2 = [r["t_cold_min_s"] for r in rows]
        t_c3 = [r["t_cold_s"] for r in rows]
        med_rep, med_c2, med_c3 = _median(t_rep), _median(t_c2), _median(t_c3)
        r_l2 = (med_rep / med_c2) if (med_rep is not None and med_c2) else None
        r_l3 = (med_rep / med_c3) if (med_rep is not None and med_c3) else None
        ci_l2 = _median_ratio_ci(t_rep, t_c2, SEED3 + 77 + ci, B_LAT)
        ci_l3 = _median_ratio_ci(t_rep, t_c3, SEED3 + 79 + ci, B_LAT)
        cal_rep, cal_c2, cal_c3 = _dot(w, rep_vec), _dot(w, cold_min_vec), _dot(w, cold_vec)
        calibrated_win = bool(cal_rep < cal_c2 and cal_rep < cal_c3)

        order_first = sum(1 for r in rows if r.get("order_rep_first"))
        warmups = sum(r.get("warmups_done", 0) for r in rows)
        timed_errs = sum(1 for r in rows if r.get("timed_error"))
        finite_lat = all(math.isfinite(t) and t > 0 for t in (t_rep + t_c2 + t_c3))

        per_class[cls] = {
            "n": n,
            "M-REPAIR-SUCCESS": rep_ok / n if n else None,
            "M-REPAIR-SUCCESS-WILSON-LOWER": v2.wilson_lower(rep_ok, n),
            "M-COLD-SUCCESS": cold_ok / n if n else None,
            "M-COLD-MIN-SUCCESS": cold_min_ok / n if n else None,
            "M-LITERAL-REPLAY-SUCCESS": lit_ok / n if n else None,
            "M-NO-REPAIR-SUCCESS": nor_ok / n if n else None,
            "M-GUARD-FIRE-RATE": guard_ok / n if n else None,
            "M-CONTAMINATION-RATE": contam / unaff if unaff else None,
            "M-CONTAMINATION-PROBES": unaff,
            "M-OVERBROAD-CONTAMINATION-RATE": overbroad,
            "M-BASE-LIVENESS-TRUE-TRIALS": base_live_true,
            "M-WRITE-SET-MEAN": v2.mean(write_ws),
            "M-WRITE-SET-MAX": max(write_ws) if write_ws else None,
            "M-COST-REPAIR-REUSE-PRODUCT": rep_prod,
            "M-COST-REPAIR-CONSERVATIVE-PRODUCT": cons_prod,
            "M-COST-REPAIR-LEGACY-PRODUCT": leg_prod,
            "M-COST-COLD-PRODUCT": cold_prod,
            "M-COST-COLD-MIN-PRODUCT": cold_min_prod,
            "M-COST-REPAIR-REUSE-VECTOR": rep_vec,
            "M-COST-REPAIR-CONSERVATIVE-VECTOR": cons_vec,
            "M-COST-REPAIR-LEGACY-VECTOR": leg_vec,
            "M-COST-COLD-MIN-VECTOR": cold_min_vec,
            "M-COST-COLD-VECTOR": cold_vec,
            "M-PRODUCT-RATIO-REUSE-L3": ratio(rep_prod, cold_prod),
            "M-PRODUCT-RATIO-REUSE-L2": ratio(rep_prod, cold_min_prod),
            "M-PRODUCT-RATIO-CONSERVATIVE-L3": ratio(cons_prod, cold_prod),
            "M-PRODUCT-RATIO-CONSERVATIVE-L2": ratio(cons_prod, cold_min_prod),
            "M-PRODUCT-RATIO-LEGACY-L3": ratio(leg_prod, cold_prod),
            "M-PRODUCT-RATIO-LEGACY-L2": ratio(leg_prod, cold_min_prod),
            "M-COST-REPAIR-FETCH": rep_http,
            "M-COST-COLD-FETCH": cold_http,
            "M-COST-FETCH-RATIO-L3": ratio(rep_http, cold_http),
            "M-WEIGHT-ROBUST-L2": v2.grid_robust(rep_vec, cold_min_vec),
            "M-WEIGHT-ROBUST-L3": v2.grid_robust(rep_vec, cold_vec),
            "M-WEIGHT-ROBUST-BOTH": v2.grid_robust_both(rep_vec, cold_min_vec, cold_vec),
            "M-WEIGHT-CRITICAL-REPAIR-WEIGHT-L2": v2.critical_repair_weight(rep_vec, cold_min_vec),
            "M-WEIGHT-CRITICAL-REPAIR-WEIGHT-L3": v2.critical_repair_weight(rep_vec, cold_vec),
            "M-CALIBRATED-RATIO-REUSE-L2": ratio(cal_rep, cal_c2),
            "M-CALIBRATED-RATIO-REUSE-L3": ratio(cal_rep, cal_c3),
            "M-CALIBRATED-WIN": calibrated_win,
            "M-CALIBRATED-ROBUST-BOTH": _calibrated_band_fraction(rep_vec, cold_min_vec, cold_vec, w),
            "M-LATENCY-MEDIAN-MS-REUSE": med_rep * 1000.0 if med_rep is not None else None,
            "M-LATENCY-MEDIAN-MS-COLD-L2": med_c2 * 1000.0 if med_c2 is not None else None,
            "M-LATENCY-MEDIAN-MS-COLD-L3": med_c3 * 1000.0 if med_c3 is not None else None,
            "M-LATENCY-R-L2": r_l2, "M-LATENCY-R-L3": r_l3,
            "M-LATENCY-R-L2-CI95": list(ci_l2), "M-LATENCY-R-L3-CI95": list(ci_l3),
            "M-LATENCY-WIN": bool(r_l2 is not None and r_l3 is not None and r_l2 < 1.0 and r_l3 < 1.0),
            "M-LATENCY-ORDER-REP-FIRST": order_first,
            "M-LATENCY-N": n,
            "M-WARMUP-EPISODES": warmups,
            "M-TIMED-EPISODE-ERRORS": timed_errs,
            "M-TIMED-LATENCIES-FINITE": bool(finite_lat),
            "M-MODEL-CALLS": sum(r.get("model_calls", 0) for r in rows),
            "M-MODEL-TOKENS": sum(r.get("model_tokens", 0) for r in rows),
            "M-OPLOG-REPAIR-LEN-MEAN": v2.mean([len(r.get("repair_oplog", [])) for r in rows]),
            "M-OPLOG-LEGACY-LEN-MEAN": v2.mean([len(r.get("legacy_oplog", [])) for r in rows]),
            "M-OPLOG-PRESENT": all(bool(r.get("repair_oplog")) and bool(r.get("legacy_oplog"))
                                   for r in rows),
        }

    overbroad_rate = v2.mean([per_class[c]["M-OVERBROAD-CONTAMINATION-RATE"] for c in CLASSES
                              if per_class[c]["M-OVERBROAD-CONTAMINATION-RATE"] is not None])
    contam_probes_total = sum(per_class[c]["M-CONTAMINATION-PROBES"] for c in CLASSES)
    base_live_true_total = sum(per_class[c]["M-BASE-LIVENESS-TRUE-TRIALS"] for c in CLASSES)
    base_live_total = sum(per_class[c]["n"] for c in CLASSES)

    metrics = {"M-CLASSES": per_class,
               "M-IN-SUPPORT-PROBE-ID": v2.IN_SUPPORT_PROBE_ID,
               "M-CONTAMINATION-PROBES-TOTAL": contam_probes_total,
               "M-OVERBROAD-CONTAMINATION-RATE-MEAN": overbroad_rate,
               "M-BASE-LIVENESS-TRUE-TRIALS-TOTAL": base_live_true_total,
               "M-BASE-LIVENESS-TRIALS-TOTAL": base_live_total,
               "M-NOISE-FALSE-TRIGGER-RATE": (None if nz_t.get("stale") is None
                                              else (1.0 if nz_t["stale"] else 0.0)),
               "M-NO-PERTURBATION-FALSE-TRIGGER-RATE": (None if np_t.get("stale") is None
                                                        else (1.0 if np_t["stale"] else 0.0)),
               "M-LEGACY-REGRESSION-REPRODUCED": all(
                   (per_class[c]["M-PRODUCT-RATIO-LEGACY-L2"] or 0) > v2.LEGACY_REGRESSION_FLOOR
                   for c in CLASSES),
               "M-TRIALS-TOTAL": len(trials),
               "M-CALIB-OK": calib.get("calib_ok"),
               "M-CALIB-N": calib.get("n_cal"),
               "M-CALIB-MEDIANS-S": calib.get("medians_s"),
               "M-CALIB-RSE": calib.get("rse"),
               "M-MEASURED-WEIGHTS": calib.get("weights"),
               "M-CALIB-BYTES-PER-FETCH-MEDIAN": calib.get("bytes_median"),
               "M-WARMUP-EPISODES-TOTAL": sum(per_class[c]["M-WARMUP-EPISODES"] for c in CLASSES),
               "M-TIMED-EPISODE-ERRORS-TOTAL": sum(per_class[c]["M-TIMED-EPISODE-ERRORS"] for c in CLASSES),
               "M-MODEL-CALLS-TOTAL": sum(per_class[c]["M-MODEL-CALLS"] for c in CLASSES),
               "M-MODEL-TOKENS-TOTAL": sum(per_class[c]["M-MODEL-TOKENS"] for c in CLASSES)}

    invalid = []
    if any(not r.get("valid") for r in trials):
        invalid.append("trial-invalid")
    if base_live_total == 0 or base_live_true_total < base_live_total:
        invalid.append("positive-control-base-liveness")
    if contam_probes_total <= 0:
        invalid.append("contamination-instrument-degenerate")
    if overbroad_rate is None or overbroad_rate <= v2.CONTAMINATION_BAR:
        invalid.append("nc-overbroad-not-sensitive")
    for cls, m in per_class.items():
        if m["n"] < TRIALS_PER_CLASS:
            invalid.append(f"{cls}:n<{TRIALS_PER_CLASS}")
        if m["M-COLD-SUCCESS"] is None or m["M-COLD-SUCCESS"] < v2.COLD_SUCCESS_BAR:
            invalid.append(f"{cls}:cold-baseline-not-live")
        if m["M-LITERAL-REPLAY-SUCCESS"] is None or m["M-LITERAL-REPLAY-SUCCESS"] > v2.LITERAL_SUCCESS_BAR:
            invalid.append(f"{cls}:perturbation-does-not-bite")
        if m["M-NO-REPAIR-SUCCESS"] is None or m["M-NO-REPAIR-SUCCESS"] > v2.LITERAL_SUCCESS_BAR:
            invalid.append(f"{cls}:no-repair-not-inert")
        if m["M-LATENCY-ORDER-REP-FIRST"] != TRIALS_PER_CLASS // 2:
            invalid.append(f"{cls}:timing-order-imbalance")
        if m["M-WARMUP-EPISODES"] != 2 * TRIALS_PER_CLASS:
            invalid.append(f"{cls}:warmup-incomplete")
        if m["M-TIMED-EPISODE-ERRORS"]:
            invalid.append(f"{cls}:timed-episode-error")
        if not m["M-TIMED-LATENCIES-FINITE"]:
            invalid.append(f"{cls}:timed-latency-nonfinite")
    if nz_t.get("stale") is not False or np_t.get("stale") is not False:
        invalid.append("negative-control-not-fresh")

    cvs = {cls: cost_verdict_v3(per_class[cls]) for cls in CLASSES}
    if invalid:
        decision, status, outcome = None, "MEASUREMENT_INVALID", "INCONCLUSIVE"
    else:
        decision = aggregate_v3(list(cvs.values()))
        status = "COMPLETE"
        outcome = {"SUPPORTS": "SUPPORTS", "MIXED-PARTIAL": "MIXED",
                   "MIXED-COUNTER-DEPENDENT": "MIXED", "MIXED": "MIXED",
                   "FALSIFIES": "FALSIFIES"}.get(decision, "INCONCLUSIVE")

    out = {"status": status, "experiment_id": EXP_ID3, "lane": "runtime",
           "runner_self_sha": runner_self_sha, "seed": SEED3,
           "measured_weights": calib.get("weights"),
           "in_support_probe_id": v2.IN_SUPPORT_PROBE_ID,
           "invalid_reasons": invalid, "decision": decision, "outcome": outcome,
           "class_cost_verdicts": cvs, "metrics": metrics, "trials": trials,
           "calibration": calib, "nc_no_perturbation": np_t, "nc_noise": nz_t,
           "carrier": carrier}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
<!-- END FROZEN-RUNNER -->
