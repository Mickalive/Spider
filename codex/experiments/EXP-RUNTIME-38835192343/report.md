# EXP-RUNTIME-38835192343 execution report — larger-N L2 resolution (runtime)

Binding mandate: Global Research Director CONTINUE on C-DELTA-REPAIR — at larger N,
do the four L2 MARGINAL cells resolve to robust reuse WINs (completing the 12-cell
re-admission bar) or does any cell show a robust LOSS (bounded permanent drop)?
Stop trigger: this N is the last budgeted resolution attempt; a second consecutive
straddle PARKs the thread.

## Execution

Executed exactly the frozen v6 driver (extracted verbatim from `prereg.md`
section-12 between the line-exact markers; canonical digest `fe053ea6…924c245`
verified MATCH before the scored run; V0 substrate pin `d4871091` verified).
Preflight (non-outcome-bearing): `--liveness-only` all booleans true
(server/distill/resolve/fetch/verify/guard-silent/registry-RW, BulkArm-vs-upsert
byte-equality, NCs silent) and `--reachability-probe` all 5 class + 4 aggregate
branches reachable with N=36 gate coverage exact. Full run: 108 trials
(TRIALS_PER_CLASS=36, SEED6=180486679, rotating targets 12x each), 2 warmups +
3 timed episodes (bulk-reuse R5, cold-L2 C2, cold-L3 C3) in 18/18 parity per class
plus literal/norepair controls, NC trials, and B=2000/B=10000 bootstraps.
`invalid_reasons=[]`; status COMPLETE.

## Results (RAW -> OBSERVATION; interpretation follows separately)

- Functional/locality (H1) re-attested a fourth time at N=36: repair_success 1.0,
  Wilson lower 0.9036 ≥ 0.60, guard_fire 1.0 ≥ 0.80, write_set_max 1,
  contamination 0/144 per class (0/432), literal-replay 0.0 ≤ 0.10, cold 1.0.
- Shipped counter (H2 premise, drift-checked): reuse 612/class vs cold-L2 648 vs
  cold-L3 684; reuse http 216/180/216 (P1/P2/P3); V-DRIFT-COLD, V-DRIFT-REUSE,
  V-REG-EQUIV (108/108 byte-equal), V-EQ-HOLDS all pass.
- Latency decider (H3, Bonferroni family-wise CIs, B=10000):
  - P1 L2: R=0.9893 CIBF [0.9724, 1.0044] → MARGINAL (still straddles 1.00).
  - P1 L2-NOARG: R=0.9735 CIBF [0.9576, 0.9878] → WIN (resolved).
  - P1 L3 / L3-NOARG: R=0.8964 / 0.8820, uppers 0.9074 / 0.8919 → WIN, WIN.
  - P2 all four cells WIN (L2 R=0.8998 [0.8801, 0.9174]; L3 R=0.8120 [0.7961, 0.8271]).
  - P3 L2: R=0.9902 CIBF [0.9775, 1.0044] → MARGINAL (still straddles 1.00).
  - P3 L2-NOARG: R=0.9742 CIBF [0.9614, 0.9887] → WIN (resolved).
  - P3 L3 / L3-NOARG: R=0.8908 / 0.8763 → WIN, WIN.
- Tally: 10 WIN / 2 MARGINAL (P1-L2-inclusive, P3-L2-inclusive) / 0 LOSS / 0 UNKNOWN.
- Frozen rule: P1 PRICED-MARGINAL, P2 PRICED-WIN, P3 PRICED-MARGINAL →
  aggregate **INCONCLUSIVE (marginal straddle)** → outcome INCONCLUSIVE.
- Attribution (diagnostic tie set): excess negative all classes; closure_ok true;
  answer ATTRIBUTION-MOOT. Recurrence N* finite positive everywhere (diagnostic).
  Model calls/tokens 0 (B3 UNSATISFIABLE by construction).

## Interpretation (bounded by the frozen decision rule)

The larger-N power increase worked as projected — family-wise half-widths
narrowed from ~±6% to ~±1.6% on the straddling cells — and resolved two of the
four MARGINAL cells (both L2-NOARG) into robust WINs. But the two L2-inclusive
cells (P1 R=0.9893, P3 R=0.9902, uppers ~1.004) still straddle 1.00: a true effect
of ~1% sits below even the narrowed resolution, exactly the preregistered
sub-3% non-resolution path. No robust LOSS exists anywhere, so the bounded
permanent drop is NOT triggered; the 12-cell bar is NOT completed (10/12), so no
re-admission. Per the mandate stop trigger this second consecutive straddle
PARKs the thread: no re-admit, no drop, no promotion, no third funding request.
C-DELTA-REPAIR stays EXPERIMENTAL bounded to functional/locality soundness
(DIRECTOR decides; this producer claims no status change).

## Validity / representation loss

See `result.json#validity_notes`: localhost-only wall-clock ratios do not transfer
to real web economics; absolute L2 gaps (~0.05ms) are sub-one-local-GET;
B-NO-REPAIR vacuity disclosed (must-fail role held by literal-replay 0.0);
S-ARG asymmetry neutralized by the dual-boundary requirement; scaffold-unit ratio
informational only and excluded from the classifier.

## Evidence

Raw: `raw_evidence/run_v6_output.json` (108 trials, per-class metrics, attribution,
carrier pins). Code: `raw_evidence/runner_v6.py` (extracted frozen driver).
Canonical: `result.json` (machine handoff), `provenance.json` (reproduction).
