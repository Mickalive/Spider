# EXP-RUNTIME-38340133174 — EXECUTE report: scaffolding-attributed terminal comparison for delta-repair with B11 certificate

- experiment_id: `EXP-RUNTIME-38340133174`, lane `runtime`, target claim `C-DELTA-REPAIR`
- Frozen inputs executed exactly: `request.json`, `spec.json`, `prereg.md` (§12 v4 driver,
  CANONICAL-RUNNER-V4-SHA256 `4a97d95c…9409357d`, extraction re-verified byte-identical at EXECUTE),
  `freeze.json`, `design_review.json` (PASS). No frozen file was modified.
- Raw evidence preserved verbatim: `raw_evidence/scored_run.json` (driver stdout),
  `raw_evidence/runner_delta_repair_scaffold_v4.py` (extracted driver),
  `raw_evidence/preflight_reachability.json`, `raw_evidence/preflight_liveness.json`.
- Canonical summary: `result.json` (`status=COMPLETE`, `outcome=FALSIFIES` bounded — see §1).
  This report is explanatory only and does not exceed `result.json` or the frozen claim ceiling.

## 1. Headline verdict (text-faithful reading of the frozen decision rule)

**PERMANENT-DROP-BOUNDED → `outcome=FALSIFIES` (bounded product-story drop, explicitly NOT a
mechanism falsification).** Per prereg §8 mapping, reuse-based localized repair is permanently
dropped from the `C-PRODUCT-ECON` product story on this substrate/carrier/classes/counter, with no
further L-sweeps (mandate stop trigger fires). `C-DELTA-REPAIR` mechanism soundness
(functional/locality) is NOT rejected and stays EXPERIMENTAL bounded to functional/locality
soundness: repair works (36/36), it just does not pay end-to-end.

**Mandatory disclosure on the verdict label.** The frozen driver's stdout prints
`decision=MEASUREMENT_INVALID` with 9 `invalid_reasons` strings. Those 9 strings are a
demonstrable code-evaluation artifact, not measurement failures: the driver tests the three
must-pass upper-bound gates as `(metric or 1.0) > 0.10`, and Python maps a legitimately observed
`0.0` to `1.0`, so perfect must-fail-control behavior (literal 0.0, norepair 0.0, contamination 0.0
on all classes) spuriously trips INVALID. The frozen *textual* gates (spec decision_rule,
prereg §6 V4/V6/V8, prereg §8/§14) all hold, the driver's own cost classifier returns
PRICED-DEFICIT ×3 via direct comparisons, and no §8 gate failed — so per prereg §14 the
measurement transaction is COMPLETE with the priced verdict above. Both readings are preserved:
`result.json.metrics.driver_emitted` carries the raw stdout decision verbatim;
`result.json` top-level `status/outcome` carry the text-faithful reading. AUDIT adjudicates.

## 2. What was measured (36 scored trials + certificate bank, all in-runner)

- 36/36 valid trials (12/class × P1-ENDPOINT / P2-STRUCTURE / P3-PERMISSION), all repair
  reason `repaired`, repair_success 36/36, retention_ok 36/36 (V-RETAIN tripwire held — warmups
  did not heal perturbations), 2 warmups/trial, exact 6/6 parity per class, 108/108 episode
  latencies finite and positive, 0 timed-episode errors, base liveness 36/36.
- Functional/locality gates pass on every class: repair 1.0 (Wilson lower 0.7575 ≥ 0.60),
  contamination 0/24 unaffected probes, write_set_max 1, guard_fire 1.0, cold 1.0.
- Drift pins hold exactly: cold shipped 216/228 with http 96/108 per class (V-DRIFT-COLD);
  every repaired trial ships exactly 17 with class http 6/5/6 (V-DRIFT-REUSE, 36/36).
  V-EQUIV: timed episodes match original-function warmup discrete projections 36/36.
- Shipped 4-field premise (V-EQ-HOLDS, deterministic as designed): reuse 204 vs cold 216/228
  → ratios 0.9444 (L2) / 0.8947 (L3); fetch ratios 0.667/0.556/0.667 ≤ 0.90. Zero empirical
  variance by construction (AF-3 lesson honored: premise, not win claim).
- Empirical decider (dual-boundary latency): reuse is strictly SLOWER on all six ratios —
  inclusive 1.246/1.152/1.235 (L2), 1.136/1.037/1.119 (L3); NOARG 1.228/1.137 (L2),
  1.119/1.023/1.105 (L3). All six bootstrap CI95 (B=2000) lie entirely above 1.00 (lowest lower
  bound 1.0233, P2-L3-NOARG). Per-trial signs at L3: 35/36 reuse-slower (12/12, 12/12, 11/12).
  The deficit survives removal of the disclosed S-ARG deepcopy asymmetry, so it is not a
  deepcopy artifact. Class verdicts PRICED-DEFICIT ×3 → aggregate PERMANENT-DROP-BOUNDED.
- 5-field scaffold-inclusive sensitivity (reported, excluded): 1.2857/1.2273 every class —
  consistent with the latency verdict, not gated by design.
- Legacy replication (V13): T-REPAIR-LEGACY shipped ratio 1.1111 > 1.00 at L2 on every class —
  the prior product-counter regression reproduces; no caveat.

## 3. Attribution answer (unknown #1 resolved)

**ATTRIBUTED-S-REGISTRY-BUILD** with closure holding (reuse misc 0.0039–0.0043, cold misc
0.0063–0.0065, far below the 0.20 bar). Median excess 0.75ms (P1) / 0.21ms (P2) / 0.66ms (P3) —
inside the parent 0.2–0.9ms band. S-REGISTRY-BUILD delta (~1.44–1.45ms, reuse builds the registry
from 5 mechanisms while cold builds from `{}`) exceeds half the excess on 3/3 classes. Honest
context: S-PROBE also reaches the share on 3/3 and S-REPAIR-SIGNAL on 2/3 (P1, P3); the frozen
first-match order reports S-REGISTRY-BUILD. Shares exceed 1.0 because the excess is net of
~2.0–2.2ms cold-side savings (discovery/observe/distill/execute negative for reuse) — gross
reuse-side scaffolding (~2.9–3.0ms: registry build + probe + repair-signal + registry write)
minus cold-side re-derivation work the reuse arm skips. The mandate's "which scaffolding
component" question is therefore answered: registry construction dominates, with the fused
first-task probe and the repair-signal evaluation as jointly sufficient co-contributors.

## 4. B11 certificate (second deliverable, V-CERT track)

Complete (`certificate_complete=true`): bank sensitivity 36/36, held-out sensitivity 12/12 on
disjoint fresh seeds (genuinely new information beyond the gated episodes), pooled specificity
38/38 (36 per-trial fresh-silence probes + 2 NCs), 0 false accepts, residual boundary labeled
(BND-REQUIRED-PATHS DERIVED, BND-THRESHOLD DERIVED, BND-PROBE-BUDGET MEASURED at single fused
probe TASK_IDS[0]=14). This packet measures the runtime instance including unseen-perturbation
sensitivity; it does not close product B11. B3 model economics: structurally 0 calls/tokens —
UNSATISFIABLE here, priced in counters only, blocker recorded per mandate.

## 5. Consequences

- Negative (this packet): the SINGLE-SURFACE-MIXED split resolves to **permanent bounded drop**
  from the `C-PRODUCT-ECON` product story — no re-admission, no further L-sweeps, no promotion.
  `C-DELTA-REPAIR` itself stays EXPERIMENTAL (repair works; it does not pay end-to-end).
- Positive counterfactual (not observed): all-six strict latency wins would have re-admitted
  localized repair with honest denominators (shipped counter + dual-boundary latency +
  attribution + B11 certificate), still with the B3 blocker recorded and no code promotion.
- For AUDIT: recompute from `scored_run.json` trials (counters, oplogs, phase timings, V-EQUIV
  fields all present); the single adjudication point is VN-DRIVER-OR-DEFAULT (result.json
  validity_notes), where raw stdout and frozen text diverge for the documented Python-semantics
  reason. A future DESIGN revision should replace `(m or 1.0)` None-defaults with explicit
  `is None` checks; that repair is DIRECTOR business, not an EXECUTE edit.
