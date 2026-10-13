# EXP-RUNTIME-38291097112 — EXECUTE report (runtime)

**Status:** `COMPLETE` / **Outcome:** `MIXED` (runner decision `MIXED-PARTIAL`).
Canonical machine handoff is `result.json`; raw evidence is
`raw_evidence/runner_result_raw.json`. This report explains and interprets
those fields and does not add measurements beyond them.

## 1. Question (frozen)

On the same fetch-scarce, credential-free, locally served substrate and the
same shipped carrier held fixed, with the corrected in-support contamination
instrument retained: can an independently justified end-to-end
product-economics counter — time-calibrated per-operation weights (fetch
numeraire) plus measured end-to-end episode latency, model calls/tokens
structurally 0 (B3 NOT SATISFIED, carried as unknown) — be constructed and
measured so that reuse-based localized repair is or is not strictly cheaper
than cold re-derivation at L=2 and L=3, and should localized repair therefore
be re-admitted to or permanently dropped from the `C-PRODUCT-ECON` product
story?

## 2. What was executed (exactly the frozen design)

1. Extracted the frozen runner from `prereg.md` §12 by the literal marker
   split, wrote `raw_evidence/runner_delta_repair_calibrated_v3.py`, verified
   sha256 `ec480f38…002229` == `CANONICAL-RUNNER-V3-SHA256`.
2. Re-verified the three carrier hashes against `freeze.json.artifact_hashes`
   (all match) and the parent v2 pin (60855 bytes / `d4871091…`; the runner's
   V0 gate imported it without refusal).
3. Pre-flight (non-outcome-bearing): `--reachability-probe` (all 8 class + 6
   aggregate branches reachable) and `--liveness-only` (server, distill,
   verify, in-support instrument, both NCs fresh, 1ns timer, N=60
   mini-calibration live).
4. Scored run: Stage-A calibration (N=300/class) then 36 timed trials
   (12/class × P1/P2/P3, rotating targets, 2 excluded warmups + parity-ordered
   timed reuse/cold-L2/cold-L3 per trial, untimed conservative/legacy/literal/
   no-repair arms, both NC trials). No frozen file was modified; only
   `raw_evidence/` outputs plus this packet's `result.json`/`report.md`/
   `provenance.json` were added.

## 3. Raw evidence → observations (no interpretation here)

- Runner output: `status=COMPLETE`, `outcome=MIXED`, `decision=MIXED-PARTIAL`,
  `invalid_reasons=[]`; 36/36 trials valid; class verdicts
  `SINGLE-SURFACE-MIXED` on all three classes.
- Functional gates hold everywhere: repair 1.0 (Wilson lower
  `0.7574992425007574`), guard 1.0, contamination 0.0/144, write-set max 1,
  literal-replay 0.0, no-repair 0.0.
- Equal-weight strict win reproduced: 0.9444 (L=2) / 0.8947 (L=3), fetch
  0.6667 (P1/P3) / 0.5556 (P2); vectors P1/P3 `(6,5,5,1)`, P2 `(5,5,6,1)` vs
  cold `(8,5,5,0)/(9,5,5,0)`.
- Construction live: `calib_ok=true`; medians fetch 362.4µs / resolve 42.0µs /
  verify 37.8µs / repair 0.21µs; RSEs ≤ 0.012 (bar 0.30); timer 1ns;
  weights `[1.0, 0.116023, 0.104291, 0.000582]`.
- Calibrated surface: reuse strictly cheaper both budgets all classes (P1
  0.7803/0.7031; P2 0.6819/0.6144; P3 0.7803/0.7031); band 1.0.
- Latency surface: reuse strictly slower both budgets all classes (P1
  1.2118/1.0976; P2 1.1407/1.0459; P3 1.2513/1.1451); every 95% CI excludes
  1.0 from above.
- Replication: legacy L=2 1.1111 all classes; equal-weight grid 0.78/0.67,
  critical weights 2.0/3.0 — the parent's numbers reproduced.
- Controls all PASS: base-liveness 36/36, overbroad 4/4 every trial, NCs
  fresh, 72/72 warmups, exact 6/6 parity, 0 timed errors, model calls/tokens 0
  (measured).

## 4. Derived measurements (frozen classifier)

Per class: `functional_ok=true`, `eq=true` (0.9444 < 1, 0.8947 < 1,
fetch ≤ 0.90), `cw=true`, `lw=false` → `SINGLE-SURFACE-MIXED` (eq AND
exactly one of cw/lw). Aggregate: all three in
`{STRICT-WIN-MEASURED, SINGLE-SURFACE-MIXED}` with zero all-strict →
`MIXED-PARTIAL` → outcome `MIXED`.

## 5. Interpretation

- **H1 (functional/locality):** holds — re-attested at the same ceiling.
- **H2 (calibrated counter):** holds — under the independently measured
  fetch-numeraire weights, reuse is strictly cheaper at L=2 and L=3 on every
  class, robust across the 81-combo band (1.0). The parent's
  counter-dependence does NOT reproduce on this surface: the measured weights
  sit deep in reuse-wins territory.
- **H3 (latency):** fails — median timed-episode reuse is slower than cold at
  both budgets on every class, decisively (no CI touches 1.0).
- **H4 (construction):** holds — the counter was constructed live with large
  margins on every bar; B3 model economics remains unknown, not measured.
- **H5 (replication premise):** holds — legacy regression and equal-weight
  strict win both reproduced.

The two new surfaces diverge, and the divergence is the finding:
the counted-op model (4 op classes) says reuse wins; the wall clock says
reuse loses by ~0.2–0.9ms/episode. The calibrated counter is therefore an
*incomplete* end-to-end model on this substrate — episode scaffolding
(guard/signal/registry/copy/dispatch work the calibration workload does not
time) evidently favors cold. This packet does not decompose that scaffolding
(see `unresolved`); it establishes the sign split with both sides measured
live under parity-controlled timing.

## 6. Product consequence (preregistered)

Re-admission required `SUPPORTS` (all `STRICT-WIN-MIXED`… precisely all
`STRICT-WIN-MEASURED`); the observed `MIXED-PARTIAL` does not meet it, so
**localized repair is not re-admitted to the `C-PRODUCT-ECON` product story
by this evidence**. This is not `EQUAL-ONLY-MIXED` (the calibrated surface
did win) and not falsification of repair as a mechanism — it is the
preregistered intermediate: one product-correct surface wins, the other
decisively loses. Whether the Director reads this as drop-permanently or
drop-pending-a-scaffolding-complete-counter is an adjudication matter for
DIRECTOR; the producer records that a fetch-numeraire counted-op counter
alone is insufficient end-to-end evidence for re-admission, and no promotion
is requested or licensed (`promote_to_product=false` by lane discipline).

Had the outcome been `SUPPORTS`, the consequence would have been re-admission
with the stated measured counter and explicit scope bounds (B3 still gating
the flagship). Had calibration failed, there would be no scientific verdict
(drop-pending-counter), not falsification.

## 7. Caveats and scope

See `result.json#validity_notes` (B3 unknown; calibration covers 4 op classes
only; localhost ~4ms-episode timing scope; L=4 not re-run; NB-1 moot with
V13 satisfied; NB-2 enforced at pre-flight) and `#unresolved` (scaffolding
decomposition; space of other justifiable counters; real-web transfer; B3).
No claim is made beyond this substrate/carrier/classes/counter/grid, and no
parent-packet distinction is restated as this packet's own result.
