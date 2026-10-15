# EXP-RUNTIME-38340133174 preregistration — scaffolding-attributed terminal comparison with B11 certificate

- experiment_id: `EXP-RUNTIME-38340133174`
- lane: `runtime` (design_contract_version 2)
- target claim: `C-DELTA-REPAIR` (effective status EXPERIMENTAL; retain-or-bound only)
- director action: REOPEN (runtime IDLE reactivation on the single shared validity blocker)
- design status: PRE-FREEZE (DESIGN ONLY; no outcome-bearing measurement has been run)

## 1. Strategic question (binding director mandate, refined)

Which uncounted episode-scaffolding component accounts for the ~0.2–0.9ms reuse
latency excess, and under a shipped scaffolding-priced end-to-end counter
(`http_requests` + `retrieval_calls` + `verification_calls` + `repair_attempts`,
plus a measured probe-coverage certificate or runtime observation guard for the
B11 budget-sparse boundary as the second deliverable), is reuse-based localized
repair strictly cheaper than cold re-derivation at L=2 and L=3 — i.e. does the
SINGLE-SURFACE-MIXED split resolve toward re-admission or permanent drop from
the C-PRODUCT-ECON product story? If real model-call/token economics (B3)
remain unsatisfiable, price in counters only and record the blocker.

Refinement (no drift): the mandate names the counter fields and the two
deliverables. This design fixes them as: (D1) the shipped 4-field unit counter
(zero fitted quantities) framed honestly as a drift-checked deterministic
premise (V-DRIFT-COLD pins the repair-independent cold nominals 18/19 exactly;
V-EQ-HOLDS records the 17-vs-18/19 inequality with zero empirical variance by
construction, per audit AF-3) plus the parity-controlled latency surface that
prices all scaffolding in wall-clock as the empirical decider, plus an honest
preregistered 5-field scaffolding-inclusive sensitivity; (D2) a measured guard
probe-coverage certificate over the frozen perturbation bank with independent
information beyond the gated episodes (36 per-trial fresh-silence probes plus
12 held-out guard-only perturbations on fresh seeds). "Scaffolding-priced" is
honored by the pair: latency prices every scaffolding operation in time, the
5-field sensitivity prices it in ops, and the phase attribution locates it. The
classifier decides on the shipped premise plus latency, for the reachability
reason recorded in §9 (the 5-field unit counter is deterministically
reuse-negative on nominal vectors, so deciding on it would make SUPPORTS
arithmetically unreachable — a degenerate design; it is reported, not decided).
An sp deficit without cold drift routes to PRICED-DEFICIT/DROP, never INVALID.

Non-degeneracy dilemma (stated explicitly so the structure cannot be misread
as hiding a choice): the shipped 4-field counter is deterministic 17 vs 18/19
by arm protocol — deciding on it alone would make PRICED-DEFICIT-via-shipped
unreachable (structurally reuse-positive); the 5-field unit counter with
preregistered 1:1 scaffold weights is deterministic ≈27 vs ≈21–22 — deciding
on it would make SUPPORTS unreachable (structurally reuse-negative under an
arbitrary weight choice). Both single-counter rules are degenerate in opposite
directions, so neither is the decider. The only non-arbitrary
scaffolding-inclusive measure is wall-clock latency under the inclusive timed
boundary (every scaffolding operation consumes time by construction, with no
weight choice anywhere), which is therefore the empirical decider; the shipped
counter is retained as the mandate-named drift-checked premise (V-DRIFT-COLD +
V-DRIFT-REUSE + V-EQ-HOLDS) and the 5-field form as reported sensitivity. The
pair (premise + latency) jointly omits no cost dimension used by either
comparator: auditable op dimensions in the counter, all residual scaffolding
in time.

## 2. Inherited state (parent handoff EXP-RUNTIME-38291097112, sha 3139aa3b...)

Established (preserved, not re-litigated): measurement-valid MIXED-PARTIAL
transaction (audit PASS); functional/locality soundness 36/36; equal-weight
strict win reproduces (0.9444 L2 / 0.8947 L3); calibrated counted-op surface
favors reuse (0.61–0.78) while the only true end-to-end surface (latency)
disfavors it (R 1.05–1.25, 36/36 per-trial signs); surface divergence held open
as the finding; NOT re-admitted; permanent drop NOT self-executing (parent
AF-7 ambiguity adjudicated as drop-pending-scaffolding-complete-counter).

Rejected (bounded): STRICT-WIN-MEASURED on this substrate/carrier/classes;
the 4-op calibrated counter as a complete end-to-end model; dissolution of
counter-dependence under product-correct accounting.

Unknown (this packet answers #1 fully, #2 terminally): (#1) which scaffolding
component accounts for the excess → §5 attribution; (#2) whether any justifiable
scaffolding-priced counter shows strict reuse win at L=2 AND L=3 → §8 terminal
rule; (#3) transfer off-substrate ( untouched, out of scope); (#4) B3 model
economics (unsatisfiable here → counters-only + recorded blocker, §7).

Do-not-assume (preserved): no end-to-end product win reading of any counted-op
win; no transfer beyond localhost; model zeros are structural, not findings;
P2-L3 CI margin carried, not overstated; contamination count, not rate; no L=4
claim; no conservative-arm superiority claim.

## 3. Substrate, carrier, pins (all verified at DESIGN, §10)

- Python 3.12 stdlib only; `ThreadingHTTPServer` on localhost ephemeral port.
- Carrier (byte-identical to parent freeze, re-verified 2026-10-14):
  `src/spider/kernel.py` 3a6caf970f5c86db19419f7ae57c7125f409eceba922eb2d5a9f5964140bb1b3,
  `src/spider/models.py` 338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78,
  `src/spider/registry.py` 51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c.
- Immutable substrate reference: parent v2 runner
  `research/experiments/EXP-RUNTIME-38244432934/raw_evidence/runner_delta_repair_reuse_v2.py`
  (60855 bytes, sha256 d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608;
  V0 gate refuses on mismatch). The v4 driver calls its arm/substrate functions;
  it never reimplements them.
- Classes/targets/seeds: P1-ENDPOINT, P2-STRUCTURE, P3-PERMISSION × rotating
  TARGETS=[users,posts,comments], TRIALS_PER_CLASS=12, SEED4=3980394806
  (38340133174 mod 2**32), per-trial seed SEED4+1000*(ci+1)+j, parity
  rep_first=(j%2==0) → exactly 6/6 per class.
- No external task bank/dataset/fixture/model endpoint is read. B3 endpoint
  absent by construction.

## 4. Arms, shipped counter, scaffold units

Timed episodes (v4 inclusive boundary: arg deepcopy materialization + arm
execution; placement symmetric, operand asymmetric by construction — reuse
deepcopies the full mech dict, cold deepcopies `{}`; v3-exact boundary via
S-ARG subtraction as sensitivity): T-REPAIR-REUSE vs B-COLD (L=3) vs B-COLD-MIN (L=2), 2 excluded
warmups per trial, predeclared parity order. The 2 warmups call the ORIGINAL
pinned v2 episode functions (`v2.run_repair_reuse`, `v2.run_cold`) and their
discrete projections (success + shipped sums) are captured per trial as the
V-EQUIV diagnostic: audit can compare original-function vs instrumented-episode
discrete outcomes on identical trial state. V-EQUIV is recorded, never gated. Untimed in-trial: T-REPAIR-CONSERVATIVE
and T-REPAIR-LEGACY sensitivities, B-LITERAL-REPLAY / B-NO-REPAIR mechanism
controls, contamination and write-set probes (outside timed sections, exactly as
parent v3). Baseline/treatment identifiers are frozen as in spec.json and reused
verbatim in result/audit transmission.

D1 decision counter (shipped, unit weights, zero fitted quantities): per-episode
sums of `http_requests + retrieval_calls + verification_calls + repair_attempts`
from the shipped `TrajectoryCounters` surface via the pinned `Arm` counters.
Per-class M-SHIPPED-RATIO-L2/L3 = reuse-sum / cold-sum (exact integer ratios).

Preregistered scaffold units (each = 1 `scaffold_op`, integer-counted at
instrumentation points in the v4 driver, never double-counted against shipped
fields): (S1) one arg-deepcopy materialization per timed episode; (S2) one per
`MechanismRegistry.upsert` in episode scope (reuse build = 5, cold build = 0,
post-repair/distill writes = 1); (S3) one per `registry.all()` full scan
(`target_mech`); (S4) one per `guard()` evaluation; (S5) one per
`local_repair()` signal evaluation; (S6) one per `distill_parameterized()`
invocation. Kernel resolve/verify/fetch/repair charges stay in shipped fields
only. The 5-field sensitivity M-SP5-RATIO-* = (shipped + scaffold) ratios,
informational, excluded from the classifier (§9 reason).

Untimed read-only instrumentation (never inside timed sections, never touching
timed arms' counters): per-trial fresh-silence probes (one guard evaluation on
the unperturbed body per trial, pre-perturbation, recorded as `fresh_silent`)
and, after the scored bank, 12 held-out guard-only probes
(`_heldout_guard_probes`: fresh app, `HELDOUT_N_PER_CLASS=4` per class, seeds
`SEED4+50000+1000*(ci+1)+k` disjoint from the scored bank, resolve+fetch+guard
only). Both reuse only already-exercised v2 calls with identical signatures.

## 5. Attribution method (answers unknown #1; never gates the priced decision)

Preregistered phases (perf_counter deltas per timed episode; keys accumulate):
S-ARG, S-REGISTRY-BUILD, S-REGISTRY-SCAN, S-PROBE (fused first-task
resolve+fetch), S-GUARD (includes its verify), S-REPAIR-SIGNAL, S-REGISTRY-WRITE,
S-CHARGE, S-POST-VERIFY, S-EXECUTE, S-DISCOVERY, S-OBSERVE, S-DISTILL,
S-MISC (= episode − Σrecorded, residual). Components: REGISTRY =
BUILD+SCAN+WRITE; GUARD = PROBE+GUARD; plus REPAIR-SIGNAL, ARG, EXECUTE,
DISTILL/DISCOVERY/OBSERVE (cold-side), OTHER. Per class: phase-median deltas
reuse−coldL3; excess E = median episode gap. Closure gate V-CLOSURE: median
|S-MISC|/episode ≤ 0.20 per class. Component X ATTRIBUTED iff its median delta
≥ 0.50×E on ≥ 2/3 classes with closure holding; E ≤ 0 → ATTRIBUTION-MOOT;
closure failure → ATTRIBUTION-INVALID; else UNATTRIBUTED (honest unknown carried
forward). DESIGN liveness (fresh path only, discarded, booleans recorded and no
timings kept): server ready, distill live, resolve EXECUTABLE, fetch 200,
verify True, guard silent on unperturbed body, registry read/write executes —
no perturbation, no repair, no treatment-vs-baseline comparison, no outcome
recorded. Phase-timer/closure liveness on scored episodes is EXECUTE's to
demonstrate under V-CLOSURE, not DESIGN's to pre-measure.

## 6. Controls and validity gates

PC-BASE-LIVENESS in every scored trial (V12); B-LITERAL-REPLAY/B-NO-REPAIR
must-fail (V4/V6); NC-NO-PERTURBATION/NC-NOISE must-silent (V7);
NC-OVERBROAD-REPAIR live > 0.10 (V15); V0 pin; V1 freeze binding (v4 driver hash);
V2 isolation; V3 determinism-projection (counters/oplogs/flags deterministic;
latency wall-clock, not projected); V5 cold live; V8 leakage (write_set_max 1,
in-support contamination probe id 14); V9 integer counters; V10 not-fitted (no
calibration workload exists in v4 — the parent Stage-A fitter is deliberately
removed because its repair weight 0.000582 predetermined the win direction,
audit AF-3); V11 n=12 + 72 warmups; V13 legacy-regression premise (reported
caveat); V14 reuse identity (oplogs + phases); V-DRIFT-COLD gate (per-class
cold shipped sums exactly 216/228 with cold http sums 96/108; cold path is
repair-independent so the pin cannot mask a repair effect; break = drift →
MEASUREMENT_INVALID, never a negative); V-DRIFT-REUSE gate (every valid trial
with repair reason `repaired` and repair success must show shipped reuse sum
exactly 17 with class-expected http P1 6 / P2 5 / P3 6 — the parent accepted
vectors (6,5,5,1)/(5,5,6,1) on the byte-identical carrier; break = reuse-side
driver/substrate drift → MEASUREMENT_INVALID, never a negative; genuine repair
failures can never trip it because the pin constrains only successful-repaired
trials, and charging semantics live entirely in pinned v2 code the driver
calls but never reimplements); V-EQUIV diagnostic (per-trial warmup
original-function vs timed instrumented-episode discrete projections recorded
for audit recomputation; not gated); V-EQ-HOLDS reported premise
(deterministic 17/18, 17/19 inequality, zero empirical variance by
construction — AF-3 lesson; an sp deficit without cold drift routes to
PRICED-DEFICIT/DROP, never INVALID); V-TIMING parity/finite (S-ARG operand
asymmetric by construction, isolated via M-LATENCY-R-L3-NOARG); V-CLOSURE and
V-CERT on independent tracks (§8).

## 7. B11 second deliverable: probe-coverage certificate (V-CERT track)

Bank (frozen, enumerated pre-run): the exact 36 scored perturbations
(class,target,seed) with ground truth stale=True by construction (perturbation
applied by the runner before the guard runs — independent of the guard verdict,
so not circular); guard verdict recorded from each reuse episode. Fresh-silence
set: one read-only guard evaluation on the unperturbed body per trial
(pre-perturbation, untimed), ground truth stale=False, n=36. Held-out set: 12
guard-only probes on fresh perturbations (4/class, seeds disjoint from the
scored bank), ground truth stale=True by construction, untimed, unscored for
pricing — this set contributes genuinely new information beyond the gated
episodes (guard generalization to unseen perturbations). NC set:
NC-NO-PERTURBATION and NC-NOISE with ground truth stale=False. Metrics:
M-CERT-SENSITIVITY (fire rate on the 36-episode bank),
M-CERT-HELDOUT-SENSITIVITY (fire rate on the 12 unseen perturbations),
M-CERT-SPECIFICITY (pooled silence rate over 36 fresh-silence + 2 NC probes,
with M-CERT-SPECIFICITY-BANK/NC reported separately), M-CERT-FALSE-ACCEPTS
(exact bank stale-but-silent count) + M-CERT-HELDOUT-FALSE-ACCEPTS. Residual
boundary, explicitly labeled: BND-REQUIRED-PATHS (DERIVED — perturbations
outside required_paths cannot fire the Jaccard guard by construction);
BND-THRESHOLD (DERIVED — within-envelope perturbations holding Jaccard ≥ 0.85
with verify-True cannot fire by construction); BND-PROBE-BUDGET (MEASURED —
single fused probe at TASK_IDS[0]=14 per episode; detection measured only
there). V-CERT: bank fully enumerated, each of the 36+36+12+2 items scored
exactly once with verdict+truth recorded, boundary enumerated with
measured-vs-derived labels; failure invalidates only the certificate, never
the priced decision. Census vs new information (no circularity claim): bank
sensitivity is a completeness census over the same episodes the functional
gate already scores — reported, not discovered; the certificate's NEW
information is the 36 per-trial fresh-silence specificity probes, the 12
held-out unseen-perturbation sensitivity probes, and the labeled residual
boundary. Schema co-owned with product for B11; this packet measures
the runtime instance (including unseen-perturbation sensitivity), it does not
close product B11. B3: model_calls/model_tokens structurally 0 —
counters-only pricing with the blocker recorded (H5).

## 8. Decision rule (frozen pure classifier; synthetic reachability verified)

Per class (n=12): functional_ok (parent bars); V-DRIFT-COLD gate (cold sums
exactly 216/228, cold http exactly 96/108 — repair-independent drift pin);
V-DRIFT-REUSE gate (every successful-repaired trial ships exactly 17 with
class-expected http — reuse-side drift pin; genuine repair failures cannot
trip it); sp := M-SHIPPED-RATIO-L2<1.00 AND M-SHIPPED-RATIO-L3<1.00 (reported premise
V-EQ-HOLDS: deterministic 17/18, 17/19 by protocol, zero empirical variance);
lw := M-LATENCY-R-L2<1.00 AND M-LATENCY-R-L3<1.00 (medians; B_LAT=2000 bootstrap
CIs reported alongside per-trial 12/12 sign patterns; the empirical decider).
Class first match: FUNCTIONAL-FAIL / COST-UNKNOWN (any ratio None) /
PRICED-WIN (sp AND lw) / PRICED-DEFICIT (an sp deficit without cold drift
lands here, never INVALID). Aggregate first match: gate failure (incl.
V-DRIFT-COLD and V-DRIFT-REUSE) → MEASUREMENT_INVALID; any FUNCTIONAL-FAIL →
FALSIFIES-FUNCTIONAL; any COST-UNKNOWN → INCONCLUSIVE; all
PRICED-WIN → SUPPORTS (re-admit localized repair to C-PRODUCT-ECON with honest
denominators; no promotion; B3 blocker recorded); else → PERMANENT-DROP-BOUNDED
(mandate stop trigger: persistent split converts to permanent bounded drop from
the C-PRODUCT-ECON story, no further L-sweeps; C-DELTA-REPAIR stays
EXPERIMENTAL bounded to functional/locality soundness). Outcome mapping:
SUPPORTS→SUPPORTS, PERMANENT-DROP-BOUNDED→FALSIFIES (bounded product-story
drop, explicitly NOT a mechanism falsification), FALSIFIES-FUNCTIONAL→FALSIFIES
(bounded functional), MEASUREMENT_INVALID/INCONCLUSIVE→INCONCLUSIVE.
Attribution and certificate tracks resolve independently and never flip the
priced decision.

## 9. Satisfiability self-attack (DESIGN, pre-freeze; all branches live)

- Empty/unreachable branches: frozen pure classifier driven with synthetic rows
  at DESIGN — all 4 class branches and all 4 aggregates produced (all True);
  strict-inequality boundary tested (1.00 is NOT a win); aggregate checks
  FUNCTIONAL-FAIL before COST-UNKNOWN, matching class order, so no functional
  failure is masked by an unknown. Reachability probe re-runs inside the
  frozen driver (`--reachability-probe`, pure, no substrate). The one
  defensive-unreachable path (sp deficit without cold drift) is retained
  deliberately so the classifier is total under drift the pins did not catch;
  it routes to PRICED-DEFICIT/DROP, and PRICED-DEFICIT itself is reachable via
  the latency surface, so no DECISION branch is empty. The gates
  (V-DRIFT-COLD, V-DRIFT-REUSE, V-TIMING, V-CLOSURE-track, V-CERT-track) are
  fail-safe INVALID by construction — reachable trivially, and their firing
  is a measurement verdict, not a shadowed decision.
- Arithmetic impossibility and the AF-3 lesson: nominal-vector arithmetic at
  DESIGN confirms the shipped 4-field comparison is deterministic (17 vs 18/19
  on every functional_ok trial) — it is therefore framed as a drift-checked
  premise (V-DRIFT-COLD + V-EQ-HOLDS), never as an empirical win claim, so the
  parent AF-3 quasi-structural flaw is removed rather than repeated with unit
  weights. The 5-field unit counter (deterministic ≈27–28 vs 21–22 reuse
  deficit) stays excluded from the classifier as reported sensitivity. The
  empirical decider is latency: strict inequalities on live wall-clock medians
  with no floor/ceiling — arithmetically attainable in both directions.
- Honest prior predictive distribution: under the parent evidence (36/36
  per-trial latency signs against reuse, gaps 5–25%, narrowest P2-L3 CI95
  lower bound 1.0022) PERMANENT-DROP-BOUNDED with attribution is the expected
  decision-changing outcome and SUPPORTS is the low-prior branch. SUPPORTS is
  retained (not assumed away): if the world surprises us, re-admission is the
  correct consequence, and the packet is decision-changing via DROP either way
  under the mandate stop trigger. The v4 boundary change (symmetric placement)
  attenuates ratios toward 1.0 but preserves order, so it is not claimed as a
  flip mechanism; the v3-exact NOARG sensitivity would expose any
  boundary-artifact dependence as a diagnostic.
- Precedence (no swallow): V-DRIFT-COLD gates only repair-independent cold
  nominals, so it cannot mask a repair effect; an sp deficit without cold drift
  is arithmetically impossible on functional_ok trials, and if ever observed it
  routes to PRICED-DEFICIT/DROP, never INVALID. Functional gates precede
  cost-unknown at both levels.
- Ceiling baselines: success-rate 1.0 ceilings are functional gates, never
  deciders; the deciders (integer cost ratios, continuous latency) have live
  dynamic range.
- Treatment/comparator identity (honest reimplementation disclosure): the v4
  timed episodes are NOT thin wrappers — they reimplement the v2 episode
  sequencing with per-phase timers and integer scaffold units, calling the
  identical pinned v2 primitives in the identical order. Sequence-equivalence
  map (v2 `run_repair_reuse`/`run_cold` → v4 `run_reuse_episode`/
  `run_cold_episode`): Arm-construct → target_mech → resolve → netfetch →
  guard → local_repair → registry.upsert → charge_repair_attempt →
  verify → execute_batch(TASK_IDS[1:]) for repair (fresh path omits
  repair/upsert/charge/verify exactly as v2 does); discovery → observes →
  distill_parameterized → upsert → execute_batch(TASK_IDS) for cold. All
  charging semantics (fetch http+1, kernel counter sync, repair +1, rebind
  excluded from reuse mode) live entirely in pinned v2/carrier code the driver
  calls but never reimplements, so counter divergence requires a sequencing
  error, not a semantic one. Residual sequencing risk is fail-safe three
  ways: (i) V-DRIFT-COLD pins cold nominals exactly (repair-independent);
  (ii) new V-DRIFT-REUSE pins successful-repaired reuse trials to exactly 17
  with class-expected http (parent accepted vectors on the byte-identical
  carrier) — any reuse-side sequencing error routes to MEASUREMENT_INVALID,
  never to a spurious priced verdict; genuine repair failures cannot trip it;
  (iii) per-trial V-EQUIV fields record original-function warmup vs
  instrumented-episode discrete projections on identical trial state for audit
  recomputation. Arms share substrate/seeds/perturbations and differ only in
  preregistered physical/scaffold counts, evidenced by oplogs + phase timings
  + scaffold counts (V14); S-ARG operand asymmetric by construction (full
  mech-dict vs `{}`), disclosed and isolated via the NOARG sensitivity rather
  than mislabeled symmetric.
- Insensitive controls: overbroad instrument live in parent (4/4 every trial
  on the byte-identical carrier; DESIGN verified the function present and
  callable, live-fire basis inherited, not re-fired); must-fail/must-silent controls retained
  with INVALID (not negative) failure policy; specificity pooled over 36
  per-trial fresh-silence probes + 2 NCs; sensitivity over the 36-episode bank
  plus 12 held-out unseen perturbations (independent information, not a relabel).
- Missing prerequisites: none — imports, pins, hashes, timer, bank
  enumerability, all 31 used v2-module attributes (static name check), and cold-nominal
  arithmetic all verified at DESIGN (§10 PASS, §15).
- Unbound mutable artifacts: exactly 4 tracked files, hashes verified,
  listed in spec.freeze_artifacts (3 carrier + the runtime-imported v2 runner,
  additionally fail-closed by the V0 runtime pin); v4 driver embedded below and
  hash-bound by the exact algorithm in §10; no external banks/fixtures (banks,
  fresh-silence, held-out all built in-runner from pinned seeds).

## 10. Freeze binding

freeze_artifacts = [`src/spider/kernel.py`, `src/spider/models.py`,
`src/spider/registry.py`,
`research/experiments/EXP-RUNTIME-38244432934/raw_evidence/runner_delta_repair_reuse_v2.py`].
The v4 driver is the exact text between the two standalone marker lines in §12
(`V4-RUNNER-BEGIN` and `V4-RUNNER-END`, each the unique occurrence of its kind
in this file). CANONICAL-RUNNER-V4-SHA256 = `dcfbad8ac8f3b028798bbcba7248be279777eac4ad9d73f6258aa75cdcacd8ee`
(computed 2026-10-15 from the §12 text by the exact algorithm EXECUTE must
repeat verbatim: split this file on the line exactly equal to
`V4-RUNNER-BEGIN` and the line exactly equal to `V4-RUNNER-END`; take the
middle span; split that span into lines; find the first line whose stripped
form is exactly ```` ```python ```` and the last line whose stripped form is
exactly ```` ``` ````; take the lines strictly between them; join with a
single `\n` (no trailing newline); sha256 the UTF-8 bytes. The ```python
fence-line is unique to §12 in this file, verified at DESIGN.)
EXECUTE extracts by that algorithm and refuses on mismatch (V1).
Request/spec/prereg/carrier hashes verified against freeze.json (V1).

## 11. Legacy differentiation (pre-2.0 precedents; targeted comparison)

- P2-REPLAY-COST (sha 9687ff787f2d74460bb7006826008852f5b4416b): withdrawn 8.5x
  for unmatched/uncounted replay economics. This design honors its guard
  exactly: matched tasks (identical TASK_IDS both arms), fully-loaded
  counterfactual (inclusive timed boundary + scaffold accounting), no
  scripted-replay-as-economics framing. Comparative: DISTINCT_EXTENSION
  (scaffolding-complete counter + attribution, which P2 never priced).
- P2-AUTOMATION (operational lesson, no sha): immutable identity, explicit
  write sets, hash-pinned inheritance, per-item recovery — licensed as method
  (V0/V1/V8/per-trial recovery semantics inherited from v2/v3).
- P2-WP003 (sha 292e3243d9bc7a3b88712788a7cb05709eb74eb9, leakage-invalid):
  guard is leakage containment here — no post-state features enter the guard
  beyond the live probe both arms could observe; repair writes exactly one
  mechanism (V8); no jitter-CIs (exact integer ratios + empirical bootstrap on
  wall-clock only).
- Calibrated-counter lineage (parent v3, not pre-2.0): the time-fitted surface
  is REMOVED, not repeated, per audit AF-3 (quasi-structural win direction).
  No identical invalid/degenerate design is repeated: equal-weight-only reruns
  are excluded by the terminating rule; the priced comparison is continuity
  with new instruments (attribution + certificate) and a terminal decision.
- LEGACY verdict: NO_MATCH for scaffolding attribution/pricing (per mandate
  comparative_reasoning); DISTINCT_EXTENSION on replay-cost guards.
- AF-3 application (parent audit, not pre-2.0): the calibrated counter's
  quasi-structural win direction is not repeated with unit weights — the
  shipped 4-field comparison is disclosed as a zero-variance deterministic
  premise (V-DRIFT-COLD + V-EQ-HOLDS) and the empirical burden is carried
  entirely by the inclusive-boundary latency surface plus attribution.

## 12. Frozen executable driver v4 (extract between markers; sha-bound)

V4-RUNNER-BEGIN
```python
#!/usr/bin/env python3
# FROZEN RUNNER v4 for EXP-RUNTIME-38340133174 (runtime, design_contract_version 2).
# C-DELTA-REPAIR terminal comparison: shipped 4-field unit counter + inclusive
# episode latency + scaffolding attribution + B11 probe-coverage certificate
# + V-DRIFT-REUSE fail-safe pin + V-EQUIV warmup-vs-timed diagnostic.
# Reuses the IMMUTABLE parent v2 module by pin-checked import ONLY. Stdlib only.
# Usage (stdout is always a single JSON object):
#   python runner_delta_repair_scaffold_v4.py                      # scored run
#   python runner_delta_repair_scaffold_v4.py --mechanics-only     # canary (discrete projection)
#   python runner_delta_repair_scaffold_v4.py --reachability-probe # synthetic classifier probes (pure)
#   python runner_delta_repair_scaffold_v4.py --liveness-only      # non-outcome-bearing liveness
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import random
import sys
import time
from pathlib import Path

EXP_ID4 = "EXP-RUNTIME-38340133174"
SEED4 = 3980394806  # 38340133174 % 2**32
V2_PIN_SHA = "d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608"
V2_PIN_BYTES = 60855
B_LAT = 2000
CLOSURE_BAR = 0.20
ATTRIB_SHARE = 0.50
FETCH_BAR = 0.90
NOMINAL = {"reuse_sum": 17, "cold_l2_sum": 18, "cold_l3_sum": 19,
           "cold_l2_http": 8, "cold_l3_http": 9}
REUSE_HTTP_EXPECTED = {"P1-ENDPOINT": 6, "P2-STRUCTURE": 5, "P3-PERMISSION": 6}
HELDOUT_N_PER_CLASS = 4
HELDOUT_SEED_BASE = SEED4 + 50000


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
PHASE_KEYS = ["S-ARG", "S-REGISTRY-BUILD", "S-REGISTRY-SCAN", "S-PROBE", "S-GUARD",
              "S-REPAIR-SIGNAL", "S-REGISTRY-WRITE", "S-CHARGE", "S-POST-VERIFY",
              "S-EXECUTE", "S-DISCOVERY", "S-OBSERVE", "S-DISTILL"]
REGISTRY_PHASES = ["S-REGISTRY-BUILD", "S-REGISTRY-SCAN", "S-REGISTRY-WRITE"]
GUARD_PHASES = ["S-PROBE", "S-GUARD"]
COLD_FETCH_PHASES = ["S-DISCOVERY", "S-OBSERVE"]


def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return None
    m = n // 2
    return float(xs[m]) if n % 2 else (xs[m - 1] + xs[m]) / 2.0


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


class ScafLog:
    """Phase timers + preregistered integer scaffold units for one episode."""

    def __init__(self):
        self.t = {}
        self.scaf = 0

    def timed(self, key, fn, *a, **k):
        t0 = time.perf_counter()
        out = fn(*a, **k)
        self.t[key] = self.t.get(key, 0.0) + (time.perf_counter() - t0)
        return out

    def add_scaf(self, n=1):
        self.scaf += n


def _arm_counters(arm):
    return arm.counters.as_dict()


def run_reuse_episode(app, origin, mechs, cached, resource):
    """Instrumented treatment episode. Mirrors v2.run_repair_reuse semantics."""
    log = ScafLog()
    t0 = time.perf_counter()
    md = log.timed("S-ARG", copy.deepcopy, mechs)
    log.add_scaf(1)
    arm = log.timed("S-REGISTRY-BUILD", v2.Arm, md, Path("/tmp"), "reuse4")
    log.add_scaf(len(md))
    mech = log.timed("S-REGISTRY-SCAN", arm.target_mech, resource)
    log.add_scaf(1)
    if mech is None:
        return {"ok": False, "reason": "not-executable", "arm": arm,
                "phases": dict(log.t), "scaffold": log.scaf,
                "episode_s": time.perf_counter() - t0}
    slot = mech.parameter_slots[0]
    intent = mech.intent
    context = {"resource_type": resource}
    required_paths = set(v2.flatten(mech.postconditions))
    r0 = log.timed("S-PROBE", arm.resolve, intent, context, {slot: str(v2.TASK_IDS[0])})
    if r0.status.name != "EXECUTABLE" or r0.bound_action is None:
        return {"ok": False, "reason": "not-executable", "arm": arm,
                "phases": dict(log.t), "scaffold": log.scaf,
                "episode_s": time.perf_counter() - t0}
    failed = log.timed("S-PROBE", arm.netfetch, r0.bound_action["url"],
                       r0.bound_action.get("headers", {}), origin=origin)
    stale, ginfo = log.timed("S-GUARD", v2.guard, cached, required_paths, failed,
                             arm, mech, {slot: str(v2.TASK_IDS[0])})
    log.add_scaf(1)
    if not stale:
        ok, _ = log.timed("S-EXECUTE", v2.execute_batch, arm, intent, context,
                          slot, v2.TASK_IDS[1:])
        ep = time.perf_counter() - t0
        return {"ok": bool(ok), "reason": "fresh", "arm": arm, "guard_fired": False,
                "guard_info": ginfo, "phases": dict(log.t), "scaffold": log.scaf,
                "episode_s": ep, "misc_s": ep - sum(log.t.values())}
    patched, probe_body, probe_header = log.timed(
        "S-REPAIR-SIGNAL", v2.local_repair, arm, mech, resource, slot,
        v2.TASK_IDS[0], failed, origin)
    log.add_scaf(1)
    if patched is None:
        ep = time.perf_counter() - t0
        return {"ok": False, "reason": "repair-failed", "arm": arm, "guard_fired": True,
                "guard_info": ginfo, "phases": dict(log.t), "scaffold": log.scaf,
                "episode_s": ep, "misc_s": ep - sum(log.t.values())}
    log.timed("S-REGISTRY-WRITE", arm.registry.upsert, patched)
    log.add_scaf(1)
    log.timed("S-CHARGE", arm.charge_repair_attempt)
    first_ok = False
    if probe_body is not None:
        first_ok = bool(log.timed("S-POST-VERIFY", arm.verify, patched.mechanism_id,
                                  probe_body, {slot: str(v2.TASK_IDS[0])}))
    ok, _ = log.timed("S-EXECUTE", v2.execute_batch, arm, intent, context,
                      slot, v2.TASK_IDS[1:])
    ep = time.perf_counter() - t0
    return {"ok": bool(first_ok and ok), "reason": "repaired", "arm": arm,
            "guard_fired": True, "guard_info": ginfo, "phases": dict(log.t),
            "scaffold": log.scaf, "episode_s": ep,
            "misc_s": ep - sum(log.t.values())}


def run_cold_episode(app, origin, resource, ids, tag):
    """Instrumented cold episode. Mirrors v2.run_cold semantics exactly."""
    ids = list(ids)
    log = ScafLog()
    t0 = time.perf_counter()
    log.timed("S-ARG", copy.deepcopy, {})
    log.add_scaf(1)
    arm = log.timed("S-REGISTRY-BUILD", v2.Arm, {}, Path("/tmp"), tag)
    base = f"{origin}/api/{resource}"
    extra_header = {}
    probe = log.timed("S-DISCOVERY", arm.netfetch, f"{base}/{ids[0]}", {},
                      origin=origin)
    if probe.status in (301, 302, 303, 307, 308) and probe.headers.get("Location"):
        loc = probe.headers["Location"]
        base = origin + "/".join(loc.split("/")[:-1])
    elif probe.status == 403:
        for k, vv in probe.headers.items():
            if k.lower().startswith("x-required-"):
                extra_header["X-" + k[len("x-required-"):]] = vv
    elif probe.status != 200:
        ep = time.perf_counter() - t0
        return {"ok": False, "reason": "discovery-failed", "arm": arm,
                "phases": dict(log.t), "scaffold": log.scaf, "episode_s": ep,
                "misc_s": ep - sum(log.t.values())}
    obs = []
    for rid in ids:
        res = log.timed("S-OBSERVE", arm.netfetch, f"{base}/{rid}", extra_header)
        if res.status != 200 or res.body is None:
            ep = time.perf_counter() - t0
            return {"ok": False, "reason": "observation-failed", "arm": arm,
                    "phases": dict(log.t), "scaffold": log.scaf, "episode_s": ep,
                    "misc_s": ep - sum(log.t.values())}
        obs.append(v2.Observation(intent=f"read_{resource}",
                                  state={"resource_type": resource},
                                  action={"method": "GET",
                                          "url": f"{base}/{rid}",
                                          "headers": dict(extra_header)},
                                  next_state=res.body, success=True))
    mech = log.timed("S-DISTILL", arm.kernel.distill_parameterized, obs)
    log.add_scaf(1)
    if mech is None:
        ep = time.perf_counter() - t0
        return {"ok": False, "reason": "distill-failed", "arm": arm,
                "phases": dict(log.t), "scaffold": log.scaf, "episode_s": ep,
                "misc_s": ep - sum(log.t.values())}
    log.timed("S-REGISTRY-WRITE", arm.registry.upsert, mech)
    log.add_scaf(1)
    slot = mech.parameter_slots[0]
    ok, _ = log.timed("S-EXECUTE", v2.execute_batch, arm, mech.intent,
                      {"resource_type": resource}, slot, v2.TASK_IDS)
    ep = time.perf_counter() - t0
    return {"ok": bool(ok), "reason": "cold", "arm": arm,
            "phases": dict(log.t), "scaffold": log.scaf, "episode_s": ep,
            "misc_s": ep - sum(log.t.values())}


def _timed_episode(fn, *a, **k):
    return fn(*a, **k)


def run_trial_v4(cls, target, seed, j):
    app = v2.LocalApp()
    try:
        if not v2.wait_ready(app):
            return {"valid": False, "reason": "server-not-ready"}
        mechs, cached = v2.make_mech_dicts(app.origin, v2.Counters())
        if mechs is None:
            return {"valid": False, "reason": "learn-failed"}
        base_live = {"mech_dicts": {m["mechanism_id"]: m for m in mechs.values()}}
        for r in v2.RESOURCES:
            base_live[r] = v2.unaffected_behavior(mechs, app.origin, r, "base",
                                                 v2.IN_SUPPORT_PROBE_ID)
        pre_unaffected = {r: base_live[r] for r in v2.RESOURCES}
        fresh_silent = None
        try:
            farm = v2.Arm(copy.deepcopy(mechs), Path("/tmp"), "fresh4")
            fmech = farm.target_mech(target)
            if fmech is not None:
                fslot = fmech.parameter_slots[0]
                fr0 = farm.resolve(fmech.intent, {"resource_type": target},
                                   {fslot: str(v2.TASK_IDS[0])})
                if fr0.status.name == "EXECUTABLE" and fr0.bound_action is not None:
                    ffailed = farm.netfetch(fr0.bound_action["url"],
                                            fr0.bound_action.get("headers", {}),
                                            origin=app.origin)
                    fstale, _ = v2.guard(cached[target],
                                         set(v2.flatten(fmech.postconditions)),
                                         ffailed, farm, fmech,
                                         {fslot: str(v2.TASK_IDS[0])})
                    fresh_silent = (not bool(fstale))
        except Exception:
            fresh_silent = None
        app.state.set_perturb(cls, target, seed)
        try:
            wu_reuse = v2.run_repair_reuse(app, app.origin, copy.deepcopy(mechs),
                                           cached[target], target, "reuse")
            wu_cold = v2.run_cold(app, app.origin, target, v2.LEARN_IDS, "warmcold")
            warmups = 2
            wu_reuse_arm = (wu_reuse or {}).get("arm")
            wu_cold_arm = (wu_cold or {}).get("arm")
            rep_first = (j % 2 == 0)
            if rep_first:
                rep = _timed_episode(run_reuse_episode, app, app.origin,
                                     copy.deepcopy(mechs), cached[target], target)
                c2 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS_MIN, "coldmin")
                c3 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS, "cold")
            else:
                c3 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS, "cold")
                c2 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS_MIN, "coldmin")
                rep = _timed_episode(run_reuse_episode, app, app.origin,
                                     copy.deepcopy(mechs), cached[target], target)
            cons = v2.run_repair_reuse(app, app.origin, copy.deepcopy(mechs),
                                       cached[target], target, "conservative")
            leg = v2.run_repair_legacy(app, app.origin, copy.deepcopy(mechs),
                                       cached[target], target)
            lit = v2.run_literal(app, app.origin, copy.deepcopy(mechs), target)
            nor = v2.run_norepair(app, app.origin, copy.deepcopy(mechs),
                                  cached[target], target)
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
            post = v2.unaffected_behavior(post_dicts, app.origin, r, "post",
                                          v2.IN_SUPPORT_PROBE_ID)
            if post != pre_unaffected[r]:
                contam += 1
        n_unaff = len(v2.RESOURCES) - 1
        patched_mech = rep["arm"].target_mech(target)
        overbroad = None
        if patched_mech is not None:
            overbroad = v2.overbroad_contamination(
                base_live, app.origin, target, patched_mech.as_dict(),
                v2.IN_SUPPORT_PROBE_ID)
        mcalls = sum(int(getattr(a["arm"].kernel.counters, "model_calls", 0) or 0)
                     for a in (rep, cons, leg, c3, c2) if "arm" in a)
        mtokens = sum(int(getattr(a["arm"].kernel.counters, "model_tokens", 0) or 0)
                      for a in (rep, cons, leg, c3, c2) if "arm" in a)
        return {
            "valid": True, "class": cls, "target": target,
            "repair_success": bool(rep.get("ok")),
            "repair_guard_fired": bool(rep.get("guard_fired")),
            "repair_reason": rep.get("reason"),
            "conservative_success": bool(cons["success"]),
            "legacy_success": bool(leg["success"]),
            "cold_success": bool(c3.get("ok")),
            "cold_min_success": bool(c2.get("ok")),
            "cold_deep_success": None,
            "literal_success": bool(lit["success"]),
            "norepair_success": bool(nor["success"]),
            "norepair_guard_fired": bool(nor.get("guard_fired")),
            "repair_cost": _arm_counters(rep["arm"]),
            "conservative_cost": _arm_counters(cons["arm"]),
            "legacy_cost": _arm_counters(leg["arm"]),
            "cold_cost": _arm_counters(c3["arm"]),
            "cold_min_cost": _arm_counters(c2["arm"]),
            "literal_cost": _arm_counters(lit["arm"]),
            "repair_oplog": list(rep["arm"].oplog),
            "conservative_oplog": list(cons["arm"].oplog),
            "legacy_oplog": list(leg["arm"].oplog),
            "repair_scaffold": rep.get("scaffold"),
            "cold_scaffold": c3.get("scaffold"),
            "cold_min_scaffold": c2.get("scaffold"),
            "repair_phases": rep.get("phases"),
            "cold_phases": c3.get("phases"),
            "cold_min_phases": c2.get("phases"),
            "repair_misc_s": rep.get("misc_s"),
            "cold_misc_s": c3.get("misc_s"),
            "contamination_n": contam,
            "overbroad_contamination_n": overbroad,
            "write_set_n": len(write_set),
            "fresh_silent": fresh_silent,
            "unaffected_n": n_unaff,
            "base_liveness": all(v and v[0] == 200 and v[2] for v in
                                 (pre_unaffected[r] for r in v2.RESOURCES)),
            "t_reuse_s": rep.get("episode_s"), "t_cold_min_s": c2.get("episode_s"),
            "t_cold_s": c3.get("episode_s"),
            "order_rep_first": bool(rep_first), "warmups_done": warmups,
            "warmup_reuse_success": bool((wu_reuse or {}).get("success")),
            "warmup_reuse_shipped": (_shipped_sum(_arm_counters(wu_reuse_arm))
                                     if wu_reuse_arm is not None else None),
            "warmup_cold_success": bool((wu_cold or {}).get("success")),
            "warmup_cold_shipped": (_shipped_sum(_arm_counters(wu_cold_arm))
                                    if wu_cold_arm is not None else None),
            "timed_error": None, "model_calls": mcalls, "model_tokens": mtokens,
        }
    finally:
        app.stop()


def _heldout_guard_probes():
    """Guard-only probes on fresh perturbations (untimed, unscored for pricing).

    Fresh app, fresh seeds disjoint from the scored bank; resolve+fetch+guard
    only, mirroring the exercised timed-path calls exactly. Ground truth
    stale=True by construction (set_perturb replaces state, verified
    non-accumulating in the pinned v2 module).
    """
    items = []
    try:
        app = v2.LocalApp()
    except Exception:
        return {"transport_ok": False, "items": items}
    try:
        if not v2.wait_ready(app):
            return {"transport_ok": False, "items": items}
        mechs, cached = v2.make_mech_dicts(app.origin, v2.Counters())
        if mechs is None:
            return {"transport_ok": False, "items": items}
        for ci, cls in enumerate(CLASSES):
            for k in range(HELDOUT_N_PER_CLASS):
                target = TARGETS[(ci + k + 1) % len(TARGETS)]
                seed = HELDOUT_SEED_BASE + 1000 * (ci + 1) + k
                app.state.set_perturb(cls, target, seed)
                fired = None
                try:
                    arm = v2.Arm(copy.deepcopy(mechs), Path("/tmp"), "heldout4")
                    mech = arm.target_mech(target)
                    if mech is not None:
                        slot = mech.parameter_slots[0]
                        r0 = arm.resolve(mech.intent, {"resource_type": target},
                                         {slot: str(v2.TASK_IDS[0])})
                        if r0.status.name == "EXECUTABLE" and r0.bound_action is not None:
                            failed = arm.netfetch(r0.bound_action["url"],
                                                  r0.bound_action.get("headers", {}),
                                                  origin=app.origin)
                            stale, _ = v2.guard(
                                cached[target],
                                set(v2.flatten(mech.postconditions)),
                                failed, arm, mech,
                                {slot: str(v2.TASK_IDS[0])})
                            fired = bool(stale)
                except Exception:
                    fired = None
                items.append({"class": cls, "target": target, "seed": seed,
                              "ground_truth_stale": True, "guard_fired": fired})
    finally:
        app.stop()
    return {"transport_ok": True, "items": items}


def _shipped_sum(cost):
    return (cost["http_requests"] if "http_requests" in cost else cost["http"]) + \
           (cost["retrieval_calls"] if "retrieval_calls" in cost else cost["retrieval"]) + \
           (cost["verification_calls"] if "verification_calls" in cost else cost["verification"]) + \
           (cost["repair_attempts"] if "repair_attempts" in cost else cost["repair"])


def _http_of(cost):
    return cost["http_requests"] if "http_requests" in cost else cost["http"]


def cost_verdict_v4(m):
    if not v2.functional_ok(m):
        return "FUNCTIONAL-FAIL"
    sp2, sp3 = m.get("M-SHIPPED-RATIO-L2"), m.get("M-SHIPPED-RATIO-L3")
    lw2, lw3 = m.get("M-LATENCY-R-L2"), m.get("M-LATENCY-R-L3")
    if sp2 is None or sp3 is None or lw2 is None or lw3 is None:
        return "COST-UNKNOWN"
    if sp2 < 1.0 and sp3 < 1.0 and lw2 < 1.0 and lw3 < 1.0:
        return "PRICED-WIN"
    return "PRICED-DEFICIT"


def aggregate_v4(cvs):
    if any(v == "FUNCTIONAL-FAIL" for v in cvs):
        return "FALSIFIES-FUNCTIONAL"
    if any(v == "COST-UNKNOWN" for v in cvs):
        return "INCONCLUSIVE"
    if all(v == "PRICED-WIN" for v in cvs):
        return "SUPPORTS"
    return "PERMANENT-DROP-BOUNDED"


def synthetic_reachability_probe_v4():
    def row(ok=True, sp2=0.9, sp3=0.85, lw2=0.95, lw3=0.93):
        return {"M-REPAIR-SUCCESS": 1.0 if ok else 0.0,
                "M-REPAIR-SUCCESS-WILSON-LOWER": 0.7575 if ok else 0.0,
                "M-CONTAMINATION-RATE": 0.0, "M-WRITE-SET-MAX": 1,
                "M-GUARD-FIRE-RATE": 1.0,
                "M-SHIPPED-RATIO-L2": sp2, "M-SHIPPED-RATIO-L3": sp3,
                "M-LATENCY-R-L2": lw2, "M-LATENCY-R-L3": lw3}
    cases = {
        "PRICED-WIN": row(),
        "PRICED-DEFICIT-shipped": row(sp2=1.05),
        "PRICED-DEFICIT-latency": row(lw3=1.10),
        "PRICED-DEFICIT-boundary": row(sp2=1.0),
        "FUNCTIONAL-FAIL": row(ok=False),
        "COST-UNKNOWN": row(sp2=None, sp3=None, lw2=None, lw3=None),
    }
    verdicts = {k: cost_verdict_v4(v) for k, v in cases.items()}
    aggregates = {
        "SUPPORTS": aggregate_v4(["PRICED-WIN"] * 3),
        "PERMANENT-DROP-BOUNDED": aggregate_v4(["PRICED-WIN", "PRICED-DEFICIT",
                                                "PRICED-WIN"]),
        "FALSIFIES-FUNCTIONAL": aggregate_v4(["PRICED-WIN", "FUNCTIONAL-FAIL",
                                              "PRICED-WIN"]),
        "INCONCLUSIVE": aggregate_v4(["PRICED-WIN", "COST-UNKNOWN",
                                      "PRICED-DEFICIT"]),
    }
    all_class = {"PRICED-WIN", "PRICED-DEFICIT", "FUNCTIONAL-FAIL", "COST-UNKNOWN"}
    all_agg = {"SUPPORTS", "PERMANENT-DROP-BOUNDED", "FALSIFIES-FUNCTIONAL",
               "INCONCLUSIVE"}
    return {
        "class_cost_verdicts": verdicts,
        "aggregate_decisions": aggregates,
        "all_class_branches_reachable": set(verdicts.values()) == all_class,
        "all_aggregate_branches_reachable": set(aggregates.values()) == all_agg,
    }


def _carrier():
    return {
        "kernel_sha256": hashlib.sha256((REPO / "src/spider/kernel.py").read_bytes()).hexdigest(),
        "models_sha256": hashlib.sha256((REPO / "src/spider/models.py").read_bytes()).hexdigest(),
        "registry_sha256": hashlib.sha256((REPO / "src/spider/registry.py").read_bytes()).hexdigest(),
        "v2_runner_sha256": V2_PIN_SHA,
        "v2_runner_bytes": V2_PIN_BYTES,
    }


def _per_class_metrics(cls, rows, seed_base):
    n = len(rows)
    rep_ok = sum(1 for r in rows if r["repair_success"])
    guard_ok = sum(1 for r in rows if r["repair_guard_fired"])
    contam = sum(r["contamination_n"] for r in rows)
    unaff = sum(r["unaffected_n"] for r in rows)
    write_max = max([r.get("write_set_n") for r in rows if r.get("write_set_n") is not None]
                    or [None])
    base_live_true = sum(1 for r in rows if r.get("base_liveness"))
    overbroad = v2.mean([r["overbroad_contamination_n"] for r in rows
                         if r.get("overbroad_contamination_n") is not None])
    m = {
        "M-REPAIR-SUCCESS": rep_ok / n if n else None,
        "M-REPAIR-SUCCESS-WILSON-LOWER": v2.wilson_lower(rep_ok, n) if n else None,
        "M-CONTAMINATION-RATE": (contam / unaff) if unaff else None,
        "M-WRITE-SET-MAX": write_max,
        "M-GUARD-FIRE-RATE": guard_ok / n if n else None,
        "M-COLD-SUCCESS": sum(1 for r in rows if r["cold_success"]) / n if n else None,
        "M-LITERAL-SUCCESS": sum(1 for r in rows if r["literal_success"]) / n if n else None,
        "M-NOREPAIR-SUCCESS": sum(1 for r in rows if r["norepair_success"]) / n if n else None,
        "M-BASE-LIVENESS": base_live_true / n if n else None,
        "M-OVERBROAD-CONTAMINATION-N": overbroad,
    }
    sh_re = sum(_shipped_sum(r["repair_cost"]) for r in rows)
    sh_c2 = sum(_shipped_sum(r["cold_min_cost"]) for r in rows)
    sh_c3 = sum(_shipped_sum(r["cold_cost"]) for r in rows)
    sc_re = sum(r["repair_scaffold"] for r in rows if r.get("repair_scaffold") is not None)
    sc_c2 = sum(r["cold_min_scaffold"] for r in rows if r.get("cold_min_scaffold") is not None)
    sc_c3 = sum(r["cold_scaffold"] for r in rows if r.get("cold_scaffold") is not None)
    h_re = sum(_http_of(r["repair_cost"]) for r in rows)
    h_c2 = sum(_http_of(r["cold_min_cost"]) for r in rows)
    h_c3 = sum(_http_of(r["cold_cost"]) for r in rows)
    m["M-SHIPPED-REUSE"] = sh_re
    m["M-SHIPPED-COLD-L2"] = sh_c2
    m["M-SHIPPED-COLD-L3"] = sh_c3
    m["M-SHIPPED-RATIO-L2"] = (sh_re / sh_c2) if sh_c2 else None
    m["M-SHIPPED-RATIO-L3"] = (sh_re / sh_c3) if sh_c3 else None
    m["M-COST-FETCH-RATIO-L3"] = (h_re / h_c3) if h_c3 else None
    m["M-COLD-HTTP-L2"] = h_c2
    m["M-COLD-HTTP-L3"] = h_c3
    m["M-REUSE-HTTP"] = h_re
    equiv = [r for r in rows if r.get("repair_reason") == "repaired"
             and r.get("repair_success")
             and r.get("warmup_reuse_shipped") is not None]
    m["M-EQUIV-MATCH-N"] = sum(1 for r in equiv if r["warmup_reuse_shipped"]
                               == _shipped_sum(r["repair_cost"]))
    m["M-EQUIV-MATCH-DEN"] = len(equiv)
    m["M-SCAFFOLD-REUSE"] = sc_re
    m["M-SCAFFOLD-COLD-L3"] = sc_c3
    m["M-SP5-RATIO-L2"] = ((sh_re + sc_re) / (sh_c2 + sc_c2)) if (sh_c2 + sc_c2) else None
    m["M-SP5-RATIO-L3"] = ((sh_re + sc_re) / (sh_c3 + sc_c3)) if (sh_c3 + sc_c3) else None
    leg_re = sum(_shipped_sum(r["legacy_cost"]) for r in rows)
    m["M-LEGACY-RATIO-L2"] = (leg_re / sh_c2) if sh_c2 else None
    t_rep = [r["t_reuse_s"] for r in rows]
    t_c2 = [r["t_cold_min_s"] for r in rows]
    t_c3 = [r["t_cold_s"] for r in rows]
    med_rep, med_c2, med_c3 = _median(t_rep), _median(t_c2), _median(t_c3)
    m["M-LATENCY-REUSE-MED-S"] = med_rep
    m["M-LATENCY-COLD-L2-MED-S"] = med_c2
    m["M-LATENCY-COLD-L3-MED-S"] = med_c3
    m["M-LATENCY-R-L2"] = (med_rep / med_c2) if (med_rep is not None and med_c2) else None
    m["M-LATENCY-R-L3"] = (med_rep / med_c3) if (med_rep is not None and med_c3) else None
    if all(v is not None for v in (t_rep, t_c2, t_c3)) and n >= 2:
        lo2, hi2 = _median_ratio_ci(t_rep, t_c2, seed_base + 1, B_LAT)
        lo3, hi3 = _median_ratio_ci(t_rep, t_c3, seed_base + 2, B_LAT)
        m["M-LATENCY-R-L2-CI95"] = [lo2, hi2]
        m["M-LATENCY-R-L3-CI95"] = [lo3, hi3]
    else:
        m["M-LATENCY-R-L2-CI95"] = None
        m["M-LATENCY-R-L3-CI95"] = None
    m["M-LATENCY-SIGN-REUSE-SLOWER-L3"] = sum(1 for a, b in zip(t_rep, t_c3) if a > b)
    no_arg_rep = [r["t_reuse_s"] - (r.get("repair_phases") or {}).get("S-ARG", 0.0)
                  for r in rows]
    no_arg_c3 = [r["t_cold_s"] - (r.get("cold_phases") or {}).get("S-ARG", 0.0)
                 for r in rows]
    m["M-LATENCY-R-L3-NOARG"] = ((_median(no_arg_rep) / _median(no_arg_c3))
        if (_median(no_arg_rep) is not None and _median(no_arg_c3)) else None)
    comp = {}
    for key in PHASE_KEYS:
        mr = _median([(r.get("repair_phases") or {}).get(key, 0.0) for r in rows])
        mc = _median([(r.get("cold_phases") or {}).get(key, 0.0) for r in rows])
        comp[key] = {"reuse_med_s": mr, "cold_med_s": mc, "delta_med_s": mr - mc}
    m["M-PHASE-DELTAS"] = comp
    clos = []
    for r in rows:
        ep = r.get("t_reuse_s")
        ms = r.get("repair_misc_s")
        if ep:
            clos.append(abs(ms or 0.0) / ep)
    m["M-CLOSURE-REUSE-MED"] = _median(clos)
    clos_c = []
    for r in rows:
        ep = r.get("t_cold_s")
        ms = r.get("cold_misc_s")
        if ep:
            clos_c.append(abs(ms or 0.0) / ep)
    m["M-CLOSURE-COLD-MED"] = _median(clos_c)
    m["M-MODEL-CALLS"] = sum(r.get("model_calls", 0) or 0 for r in rows)
    m["M-MODEL-TOKENS"] = sum(r.get("model_tokens", 0) or 0 for r in rows)
    m["M-N"] = n
    return m


def _attribution(per_class):
    excess = {}
    for cls, m in per_class.items():
        mr = m.get("M-LATENCY-REUSE-MED-S")
        mc = m.get("M-LATENCY-COLD-L3-MED-S")
        excess[cls] = (mr - mc) if (mr is not None and mc is not None) else None
    comps = {}
    for key in PHASE_KEYS + ["REGISTRY", "GUARD", "COLD-FETCH"]:
        for cls, m in per_class.items():
            d = m.get("M-PHASE-DELTAS", {})
            if key == "REGISTRY":
                delta = sum(d.get(k, {}).get("delta_med_s", 0.0) for k in REGISTRY_PHASES)
            elif key == "GUARD":
                delta = sum(d.get(k, {}).get("delta_med_s", 0.0) for k in GUARD_PHASES)
            elif key == "COLD-FETCH":
                delta = -sum(d.get(k, {}).get("delta_med_s", 0.0)
                             for k in COLD_FETCH_PHASES + ["S-DISTILL"])
            else:
                delta = d.get(key, {}).get("delta_med_s", 0.0)
            comps.setdefault(key, {})[cls] = delta
    shares = {}
    for key, per_cls in comps.items():
        for cls, delta in per_cls.items():
            e = excess.get(cls)
            shares.setdefault(key, {})[cls] = (delta / e) if e else None
    attributed = None
    votes = {}
    for key, per_cls in shares.items():
        votes[key] = sum(1 for cls in per_class
                         if per_cls.get(cls) is not None and per_cls[cls] >= ATTRIB_SHARE)
        if votes[key] >= 2 and attributed is None:
            attributed = "ATTRIBUTED-" + key
    closure_ok = all(
        (per_class[cls].get("M-CLOSURE-REUSE-MED") is not None
         and per_class[cls]["M-CLOSURE-REUSE-MED"] <= CLOSURE_BAR)
        for cls in per_class)
    if not closure_ok:
        answer = "ATTRIBUTION-INVALID"
    elif all((e or 0.0) <= 0 for e in excess.values() if e is not None):
        answer = "ATTRIBUTION-MOOT"
    elif attributed is None:
        answer = "UNATTRIBUTED"
    else:
        answer = attributed
    return {"excess_med_s": excess, "phase_deltas_med_s": comps,
            "shares_of_excess": shares, "votes_ge_half": votes,
            "closure_ok": closure_ok, "answer": answer}


def _certificate(trials, np_t, nz_t, heldout):
    bank = []
    for r in trials:
        if not r.get("valid"):
            continue
        bank.append({"class": r["class"], "target": r["target"],
                     "ground_truth_stale": True,
                     "guard_fired": bool(r.get("repair_guard_fired"))})
    fresh = [r.get("fresh_silent") for r in trials if r.get("valid")]
    fresh_known = [f for f in fresh if f is not None]
    spec_bank = (sum(1 for f in fresh_known if f) / len(fresh_known)
                 if fresh_known else None)
    nc_items = [
        {"probe": "NC-NO-PERTURBATION", "ground_truth_stale": False,
         "guard_fired": bool(np_t.get("stale")) if np_t.get("stale") is not None else None},
        {"probe": "NC-NOISE", "ground_truth_stale": False,
         "guard_fired": bool(nz_t.get("stale")) if nz_t.get("stale") is not None else None},
    ]
    stale_items = [b for b in bank if b["ground_truth_stale"]]
    sens = (sum(1 for b in stale_items if b["guard_fired"]) / len(stale_items)
            if stale_items else None)
    nc_known = [n for n in nc_items if n["guard_fired"] is not None]
    spec_nc = (sum(1 for n in nc_known if not n["guard_fired"]) / len(nc_known)
               if nc_known else None)
    if fresh_known and nc_known:
        spec = ((sum(1 for f in fresh_known if f)
                 + sum(1 for n in nc_known if not n["guard_fired"]))
                / (len(fresh_known) + len(nc_known)))
    else:
        spec = None
    fa = sum(1 for b in stale_items if not b["guard_fired"])
    h_items = ((heldout or {}).get("items") or [])
    h_known = [h for h in h_items if h.get("guard_fired") is not None]
    h_sens = (sum(1 for h in h_known if h["guard_fired"]) / len(h_known)
              if h_known else None)
    h_fa = sum(1 for h in h_known if not h["guard_fired"])
    complete = (len(bank) == len(CLASSES) * TRIALS_PER_CLASS
                and len(fresh_known) == len(CLASSES) * TRIALS_PER_CLASS
                and len(h_known) == len(CLASSES) * HELDOUT_N_PER_CLASS
                and len(nc_known) == 2
                and sens is not None and spec is not None and h_sens is not None)
    return {
        "bank_n": len(bank), "bank_expected": len(CLASSES) * TRIALS_PER_CLASS,
        "M-CERT-SENSITIVITY": sens, "M-CERT-SPECIFICITY": spec,
        "M-CERT-SPECIFICITY-BANK": spec_bank, "M-CERT-SPECIFICITY-NC": spec_nc,
        "M-CERT-FALSE-ACCEPTS": fa, "M-CERT-FRESH-N": len(fresh_known),
        "M-CERT-HELDOUT-N": len(h_known),
        "M-CERT-HELDOUT-EXPECTED": len(CLASSES) * HELDOUT_N_PER_CLASS,
        "M-CERT-HELDOUT-SENSITIVITY": h_sens,
        "M-CERT-HELDOUT-FALSE-ACCEPTS": h_fa,
        "heldout_transport_ok": bool((heldout or {}).get("transport_ok")),
        "M-CERT-BOUNDARY": [
            {"id": "BND-REQUIRED-PATHS", "kind": "DERIVED",
             "statement": "Perturbations outside the mechanism required_paths cannot fire the Jaccard guard by construction (filtered token sets)."},
            {"id": "BND-THRESHOLD", "kind": "DERIVED",
             "statement": "Within-envelope perturbations holding required-path Jaccard >= 0.85 with verify-True cannot fire by construction."},
            {"id": "BND-PROBE-BUDGET", "kind": "MEASURED",
             "statement": "Single fused probe at TASK_IDS[0]=14 per episode; detection measured only at that probe.",
             "coverage_measured": sens, "false_accepts_measured": fa},
        ],
        "certificate_complete": bool(complete),
        "nc_detail": nc_items,
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
        out = {"status": "V4-REACHABILITY-PROBE", "experiment_id": EXP_ID4,
               "lane": "runtime", "runner_self_sha": runner_self_sha,
               "decision_rule": synthetic_reachability_probe_v4(),
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
            phase_keys = None
            closure_finite = None
            if live:
                arm = v2.Arm(mechs, Path("/tmp"), "live4")
                mech = arm.target_mech("users")
                slot = mech.parameter_slots[0]
                r = arm.resolve(mech.intent, {"resource_type": "users"},
                                {slot: str(v2.TASK_IDS[0])})
                if r.status.name == "EXECUTABLE" and r.bound_action is not None:
                    res = arm.netfetch(r.bound_action["url"],
                                       r.bound_action.get("headers", {}))
                    one_ok = res.status == 200 and res.body is not None and arm.verify(
                        r.mechanism_id, res.body, {slot: str(v2.TASK_IDS[0])})
                in_support = {rr: v2.unaffected_behavior(mechs, app.origin, rr, "liveinst",
                                                         v2.IN_SUPPORT_PROBE_ID)
                              for rr in v2.RESOURCES}
                out_support = {rr: v2.unaffected_behavior(mechs, app.origin, rr, "liveold", "1")
                               for rr in v2.RESOURCES}
                in_support_ok = all(v is not None and v[0] == 200 and v[2] is True
                                    for v in in_support.values())
                out_deg = all(v is not None and v[0] == "NO-RESOLVE"
                              for v in out_support.values())
                ep = run_cold_episode(app, app.origin, "users", v2.LEARN_IDS_MIN,
                                      "livecold")
                phase_keys = sorted((ep.get("phases") or {}).keys())
                ep_s = ep.get("episode_s") or 0.0
                closure_finite = (math.isfinite(ep_s) and ep_s > 0
                                  and math.isfinite(ep.get("misc_s") or float("nan")))
            np_t = v2.no_perturbation_trial(SEED4 + 1) if ready else {"stale": None}
            nz_t = v2.noise_trial(SEED4 + 2) if ready else {"stale": None}
        finally:
            app.stop()
        print(json.dumps({"status": "V4-LIVENESS-ONLY", "experiment_id": EXP_ID4,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "server_ready": ready, "distill_live": live,
                          "task_read_verified": bool(one_ok),
                          "in_support_probe_id": v2.IN_SUPPORT_PROBE_ID,
                          "contamination_instrument_live": in_support_ok,
                          "out_of_support_probe_degenerate": out_deg,
                          "nc_no_perturbation_stale": np_t.get("stale"),
                          "nc_noise_stale": nz_t.get("stale"),
                          "timer_resolution_s": time.get_clock_info("perf_counter").resolution,
                          "instrumented_episode_phase_keys": phase_keys,
                          "instrumented_episode_closure_finite": closure_finite,
                          "carrier": carrier}, indent=2))
        return

    if args.mechanics_only:
        canary = []
        for ci, cls in enumerate(CLASSES):
            r = run_trial_v4(cls, TARGETS[ci % len(TARGETS)], SEED4 + 900 + ci, ci)
            canary.append({k: r.get(k) for k in (
                "valid", "class", "target", "order_rep_first", "repair_success",
                "conservative_success", "legacy_success", "cold_success",
                "cold_min_success", "literal_success", "norepair_success",
                "repair_guard_fired", "contamination_n", "overbroad_contamination_n",
                "unaffected_n", "base_liveness", "write_set_n", "repair_cost",
                "conservative_cost", "legacy_cost", "cold_cost", "cold_min_cost",
                "repair_oplog", "legacy_oplog", "warmups_done", "model_calls",
                "repair_scaffold", "cold_scaffold", "t_reuse_s", "t_cold_s",
                "repair_misc_s", "timed_error")})
        np_t = v2.no_perturbation_trial(SEED4 + 1)
        nz_t = v2.noise_trial(SEED4 + 2)
        print(json.dumps({"status": "V4-MECHANICS-ONLY", "experiment_id": EXP_ID4,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "seed": SEED4, "carrier": carrier,
                          "canary": canary, "nc_no_perturbation": np_t,
                          "nc_noise": nz_t}, indent=2))
        return

    trials = []
    for ci, cls in enumerate(CLASSES):
        for j in range(TRIALS_PER_CLASS):
            target = TARGETS[(ci + j) % len(TARGETS)]
            trials.append(run_trial_v4(cls, target, SEED4 + 1000 * (ci + 1) + j, j))
    np_t = v2.no_perturbation_trial(SEED4 + 1)
    nz_t = v2.noise_trial(SEED4 + 2)
    heldout = _heldout_guard_probes()

    invalid = []
    legacy_caveats = []
    for r in trials:
        if not r.get("valid"):
            invalid.append(f"{r.get('class')}:{r.get('reason')}")
        if r.get("timed_error"):
            invalid.append(f"{r.get('class')}:timed-episode-error")
    per_class = {}
    for ci, cls in enumerate(CLASSES):
        rows = [r for r in trials if r.get("valid") and r["class"] == cls]
        if len(rows) != TRIALS_PER_CLASS:
            invalid.append(f"{cls}:n-control-{len(rows)}!={TRIALS_PER_CLASS}")
            continue
        m = _per_class_metrics(cls, rows, SEED4 + 7000 * (ci + 1))
        if not all(r.get("base_liveness") for r in rows):
            invalid.append(f"{cls}:base-liveness-miss")
        if (m["M-LITERAL-SUCCESS"] or 1.0) > 0.10:
            invalid.append(f"{cls}:perturbation-does-not-bite")
        if (m["M-COLD-SUCCESS"] or 0.0) < 0.90:
            invalid.append(f"{cls}:cold-baseline-not-live")
        if (m["M-NOREPAIR-SUCCESS"] or 1.0) > 0.10:
            invalid.append(f"{cls}:abstention-control-fired")
        if (m["M-GUARD-FIRE-RATE"] or 0.0) < 0.80:
            invalid.append(f"{cls}:guard-not-live")
        if (m["M-CONTAMINATION-RATE"] or 1.0) > 0.10:
            invalid.append(f"{cls}:contamination-above-bar")
        if (m["M-WRITE-SET-MAX"] or 99) > 1:
            invalid.append(f"{cls}:write-set-leakage")
        if not (m["M-OVERBROAD-CONTAMINATION-N"] is not None
                and m["M-OVERBROAD-CONTAMINATION-N"] > 0.10):
            invalid.append(f"{cls}:overbroad-instrument-insensitive")
        if sum(1 for r in rows if r.get("order_rep_first")) != TRIALS_PER_CLASS // 2:
            invalid.append(f"{cls}:parity-order-broken")
        if any(not r.get("warmups_done") == 2 for r in rows):
            invalid.append(f"{cls}:warmup-violation")
        if any(not (math.isfinite(r.get("t_reuse_s") or float("nan"))
                   and math.isfinite(r.get("t_cold_s") or float("nan"))
                   and math.isfinite(r.get("t_cold_min_s") or float("nan"))
                   and (r.get("t_reuse_s") or 0) > 0) for r in rows):
            invalid.append(f"{cls}:nonfinite-latency")
        drift_cold = (m["M-SHIPPED-COLD-L2"] != TRIALS_PER_CLASS * NOMINAL["cold_l2_sum"]
                      or m["M-SHIPPED-COLD-L3"] != TRIALS_PER_CLASS * NOMINAL["cold_l3_sum"]
                      or m.get("M-COLD-HTTP-L2") != TRIALS_PER_CLASS * NOMINAL["cold_l2_http"]
                      or m.get("M-COLD-HTTP-L3") != TRIALS_PER_CLASS * NOMINAL["cold_l3_http"])
        if drift_cold:
            invalid.append(f"{cls}:V-DRIFT-COLD-nominal-mismatch")
        m["V-DRIFT-COLD-HOLDS"] = not drift_cold
        drift_reuse = False
        for r in rows:
            if r.get("repair_reason") == "repaired" and r.get("repair_success"):
                if (_shipped_sum(r["repair_cost"]) != NOMINAL["reuse_sum"]
                        or _http_of(r["repair_cost"]) != REUSE_HTTP_EXPECTED[cls]):
                    drift_reuse = True
                    break
        if drift_reuse:
            invalid.append(f"{cls}:V-DRIFT-REUSE-nominal-mismatch")
        m["V-DRIFT-REUSE-HOLDS"] = not drift_reuse
        eq = (m["M-SHIPPED-RATIO-L2"] is not None and m["M-SHIPPED-RATIO-L3"] is not None
              and m["M-SHIPPED-RATIO-L2"] < 1.0 and m["M-SHIPPED-RATIO-L3"] < 1.0
              and (m["M-COST-FETCH-RATIO-L3"] or 1.0) <= FETCH_BAR)
        if not (m["M-LEGACY-RATIO-L2"] is not None and m["M-LEGACY-RATIO-L2"] > 1.00):
            legacy_caveats.append(f"{cls}:V13-legacy-regression-not-reproduced")
        m["V-EQ-HOLDS"] = bool(eq)
        per_class[cls] = m

    cert = _certificate(trials, np_t, nz_t, heldout)
    attribution = _attribution(per_class) if per_class else {"answer": "ATTRIBUTION-INVALID",
                                                             "closure_ok": False}
    class_verdicts = {cls: cost_verdict_v4(m) for cls, m in per_class.items()}
    if invalid:
        decision, outcome, status = "MEASUREMENT_INVALID", "INCONCLUSIVE", "MEASUREMENT_INVALID"
    elif any(v == "FUNCTIONAL-FAIL" for v in class_verdicts.values()):
        decision, outcome, status = "FALSIFIES-FUNCTIONAL", "FALSIFIES", "COMPLETE"
    elif any(v == "COST-UNKNOWN" for v in class_verdicts.values()):
        decision, outcome, status = "INCONCLUSIVE", "INCONCLUSIVE", "COMPLETE"
    else:
        agg = aggregate_v4(list(class_verdicts.values()))
        decision = agg
        outcome = "SUPPORTS" if agg == "SUPPORTS" else ("INCONCLUSIVE" if agg == "INCONCLUSIVE"
                                                        else "FALSIFIES")
        status = "COMPLETE"
    if decision in ("SUPPORTS", "PERMANENT-DROP-BOUNDED", "FALSIFIES-FUNCTIONAL"):
        product_note = ("re-admit" if decision == "SUPPORTS"
                        else "permanent-bounded-drop-no-further-L-sweeps")
    else:
        product_note = "no-decision-no-drop-no-readmit"
    out = {"status": status, "outcome": outcome, "decision": decision,
           "experiment_id": EXP_ID4, "lane": "runtime",
           "runner_self_sha": runner_self_sha, "seed": SEED4,
           "invalid_reasons": invalid, "legacy_caveats": legacy_caveats,
           "class_verdicts": class_verdicts, "per_class": per_class,
           "attribution": attribution, "certificate": cert,
           "nc_no_perturbation_stale": np_t.get("stale"),
           "nc_noise_stale": nz_t.get("stale"),
           "product_note": product_note,
           "b3_model_economics": "UNSATISFIABLE-no-endpoint-counters-only-blocker-recorded",
           "model_calls_total": sum(r.get("model_calls", 0) or 0 for r in trials),
           "model_tokens_total": sum(r.get("model_tokens", 0) or 0 for r in trials),
           "carrier": carrier, "trials": trials}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
```
V4-RUNNER-END

## 13. Stable metric/control identities for downstream transmission

Priced metrics (per class): `M-SHIPPED-REUSE`, `M-SHIPPED-COLD-L2/L3`,
`M-SHIPPED-RATIO-L2/L3`, `M-COST-FETCH-RATIO-L3`, `M-COLD-HTTP-L2/L3`,
`M-REUSE-HTTP` (per-class reuse http sum; pin expects P1 72 / P2 60 / P3 72),
`V-DRIFT-COLD-HOLDS`, `V-DRIFT-REUSE-HOLDS`, `V-EQ-HOLDS` (reported premise), `M-LATENCY-REUSE-MED-S`,
`M-LATENCY-COLD-L2/L3-MED-S`, `M-LATENCY-R-L2/L3` (+ `M-LATENCY-R-L2/L3-CI95`
with `B_LAT=2000`, `M-LATENCY-SIGN-REUSE-SLOWER-L3`, `M-LATENCY-R-L3-NOARG`
sensitivity). Functional/locality: `M-REPAIR-SUCCESS`,
`M-REPAIR-SUCCESS-WILSON-LOWER`, `M-CONTAMINATION-RATE` (count-derived),
`M-WRITE-SET-MAX`, `M-GUARD-FIRE-RATE`, `M-COLD-SUCCESS`, `M-LITERAL-SUCCESS`,
`M-NOREPAIR-SUCCESS`, `M-BASE-LIVENESS`, `M-OVERBROAD-CONTAMINATION-N`
(count 0–4, not a 0–1 rate). Sensitivity-only: `M-SCAFFOLD-*`,
`M-SP5-RATIO-L2/L3`, `M-LEGACY-RATIO-L2`. Attribution: `M-PHASE-DELTAS`
(12 keys), `M-CLOSURE-REUSE/COLD-MED`, excess/shares/votes/answer object.
Certificate: `M-CERT-SENSITIVITY` (bank n=36), `M-CERT-HELDOUT-SENSITIVITY`
(held-out n=12), `M-CERT-SPECIFICITY` (pooled 36 fresh-silence + 2 NC, with
`M-CERT-SPECIFICITY-BANK/NC` separately), `M-CERT-FALSE-ACCEPTS`,
`M-CERT-HELDOUT-FALSE-ACCEPTS`, `M-CERT-FRESH-N`, `M-CERT-HELDOUT-N`,
`M-CERT-BOUNDARY` (3 labeled entries). V-EQUIV diagnostics (per trial):
`warmup_reuse_success`, `warmup_reuse_shipped`, `warmup_cold_success`,
`warmup_cold_shipped` (original-function discrete projections); per class
`M-EQUIV-MATCH-N`/`M-EQUIV-MATCH-DEN` (timed-vs-warmup reuse-shipped agreement
among repaired-success trials). Model economics: `M-MODEL-CALLS`,
`M-MODEL-TOKENS` (expected structural 0). Controls in `result.json`
keyed by frozen baseline/control ids (`B-COLD`, `B-COLD-MIN`,
`B-LITERAL-REPLAY`, `B-NO-REPAIR`, `T-REPAIR-REUSE`, `T-REPAIR-CONSERVATIVE`,
`T-REPAIR-LEGACY`, `PC-BASE-LIVENESS`, `NC-NO-PERTURBATION`, `NC-NOISE`,
`NC-OVERBROAD-REPAIR`, `V-CLOSURE`, `V-CERT`); each records expected vs
observed behavior and pass/fail with evidence refs. No metric/control may be
renamed by EXECUTE or AUDIT.

## 14. EXECUTE obligations (frozen design, no redesign)

Run the §12 driver verbatim (V1 hash-checked by the §10 algorithm): scored run writes
`result.json` (schema_version 1 with all 11 mandatory top-level keys;
`status` = measurement validity, `outcome` per §8 mapping;
`PERMANENT-DROP-BOUNDED` → `FALSIFIES` is a bounded product-story drop,
explicitly NOT a mechanism falsification), `report.md` (bounded by
`result.json`, no claim beyond the frozen ceiling), `provenance.json`
(run id, commits, carrier/v2 hashes, runner self-sha, environment).
Controls in `result.json` keyed by the frozen ids in §13 (including
`V-DRIFT-COLD-HOLDS`/`V-DRIFT-REUSE-HOLDS`/`V-EQ-HOLDS` and the certificate metrics). Preserve raw
evidence: driver stdout JSON, the extracted driver file,
liveness/reachability preflight outputs. Measurement failure (any gate in
§8) is `MEASUREMENT_INVALID`/`INCONCLUSIVE`, never a negative. B3 stays a
recorded blocker; B11 certificate is measured (bank + fresh-silence +
held-out), not closed.

## 15. DESIGN probe record 2026-10-14/15 (non-outcome-bearing only)

Prior-revision transparency: an earlier DESIGN submission of this packet
received `design_review` status REVISE (factory exit 65); the review artifact
was discarded by the factory's failed-stage cleanup before this revision, so
its specific findings are unavailable to DESIGN. This revision therefore
hardens all six satisfiability fronts preemptively rather than answering
unknown findings: (i) new fail-safe V-DRIFT-REUSE pin (§6/§8/§12) protecting
the priced DROP integrity against reuse-side sequencing drift; (ii) honest
reimplementation disclosure with the sequence-equivalence map (§9) replacing
any "wrapping only" reading; (iii) explicit non-degeneracy dilemma (§1) showing
why shipped-premise-plus-latency is the unique non-degenerate decision
structure; (iv) census-vs-new labeling for the certificate (§7); (v) V-EQUIV
warmup-vs-timed diagnostic capture (§4/§12/§13); (vi) defensive-branch
totality argument (§9). No scored trial and no confirmatory measurement was
run in either revision.

No scored trial and no confirmatory measurement was run. Probes: (a) v2 pin
re-verified (60855 bytes, d4871091…4962bc608) and carrier hashes byte-identical
to the parent freeze (kernel 3a6caf97…, models 338aaf4d…, registry
51fb440d…); Python 3.12.15 stdlib. (b) Pure synthetic reachability probe
(re-run at DESIGN on the frozen classifier: cost_verdict_v4 + aggregate_v4
with FUNCTIONAL-FAIL-first order at both levels): all 4 class branches and
all 4 aggregates reachable (all True); strict-inequality boundary verified
(1.00 is NOT a win). No substrate, no perturbation, no outcome.
Repair-signal liveness verified separately via the pinned module's own
synthetic probe (patched True on P1/P2/P3 synthetic inputs, non-bank
seed 7, discarded). (c) Fresh-path liveness (unperturbed, discarded,
booleans only, no timings recorded): server_ready true, distill_live true,
resolve EXECUTABLE, fetch 200, verify True, guard silent on the unperturbed
body, registry read/write executes, timer 1ns. No perturbation, no repair,
no scored seeds, no treatment-vs-baseline comparison. Contamination,
out-of-support-degenerate, and phase-key/closure liveness basis is inherited
from the parent PASS packet on the byte-identical carrier, not re-fired at
DESIGN. (d) Legacy: compact `codex/legacy_artifact_index.json` scan yields
0 hits for 'scaffolding'; full-archive grep of the mounted
`.spider-runtime/pre2/SPIDER_CODEX_ULTIME.md` yields 30 hits, all inspected
and all unrelated senses (repo/workflow scaffolding, retrieval scaffolding,
accessibility scaffolding, non-stimulus scaffolding deltas) with zero
episode-cost or scaffolding-pricing content → NO_MATCH for
attribution/pricing stands on primary-source inspection, not on
absence-of-hit; DISTINCT_EXTENSION
on P2-REPLAY-COST guards; P2-AUTOMATION licensed as method; P2-WP003
leakage guard honored. (e) Claim state: C-DELTA-REPAIR effective EXPERIMENTAL
(parent packet); B3 endpoint absent by construction (counters-only + blocker).
(f) Static checks on the frozen v4 driver (no execution of scored paths):
all 31 v2-module attributes referenced as `v2.X` in the §12 body (Arm,
CLASSES, Counters, IN_SUPPORT_PROBE_ID, LEARN_IDS, LEARN_IDS_MIN, LocalApp,
Observation, RESOURCES, TARGETS, TASK_IDS, TRIALS_PER_CLASS, execute_batch,
flatten, functional_ok, guard, local_repair, make_mech_dicts, mean,
no_perturbation_trial, noise_trial, overbroad_contamination, run_cold,
run_literal, run_norepair, run_repair_legacy, run_repair_reuse,
synthetic_repair_signal_probe, unaffected_behavior, wait_ready,
wilson_lower) verified present in the pinned v2 module by AST (defs, assigns
and imports); AppState.set_perturb verified replacing (non-accumulating), so
one held-out app serves all 12 probes; cold-nominal arithmetic verified
(12x18=216, 12x19=228, 12x8=96, 12x9=108); extraction algorithm of §10
verified to reproduce the §12 driver body byte-identically (CANONICAL hash
recomputed, not carried over).

## 16. Sign-off

This preregistration is PRE-FREEZE and complete. The decision rule is
reachable, prerequisites verified, baselines discriminating, controls
sensitive, treatment live, and all mutable local dependencies bound (§9).
Scored execution is deferred to EXECUTE under `freeze.json`.
No outcome data was inspected at DESIGN.

2026-10-15 re-verification of the hardened driver (extraction by the §10
algorithm reproduces the §12 body byte-identically under the new
CANONICAL-RUNNER-V4-SHA256; pure synthetic `--reachability-probe`: all 4
class + all 4 aggregate branches reachable, repair-signal patched True on
P1/P2/P3; fresh-path `--liveness-only`: server/distill/resolve/fetch/verify
live, guard silent, contamination instrument live, NCs silent, timer 1ns,
instrumented-episode closure finite; static checks: all 31 `v2.X` attributes
present in the pinned module, `REUSE_HTTP_EXPECTED` keys match v2 `CLASSES`,
`NOMINAL` arithmetic 12x17=204/12x18=216/12x19=228/12x8=96/12x9=108 verified,
reuse per-trial pin 17 with http 6/5/6 grounded in the parent accepted vectors
(6,5,5,1)/(5,5,6,1) on the byte-identical carrier). No scored seeds, no
perturbations, no repair-vs-cold comparison were executed or inspected.