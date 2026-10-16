# EXP-GRAPH-38835183404 report — Graph terminal tau-rule packet (EXECUTE)

Lane `graph`, claim `C-SEMANTIC-RESOLVE`. Frozen design-contract v2 transaction executed exactly as frozen; no redesign after outcomes.

## Question and rule

Director question: which pre-registrable SELECT-only calibration rule fixed before any TEST scoring selects tau=0.3333 rather than an FA-extremal tau, and does BLIND-JAC-1NN survive the frozen AXIS-G3-NEW reincluded G3 gate under that rule with resolution quality above permuted levels?

Frozen rule (`heldout-g3-covup-median`): pooled-feasible taus under the unchanged predicate (FA<=0.10 AND COV>=0.50 AND UP_excl>=0.85), ranked on the G3-origin held-out SELECT slice under the same bars; tau* = lower median of slice-passing taus, else lower median of pooled-feasible (pre-registered fallback).

## Execution (frozen procedure)

1. Extracted the FROZEN-RUNNER block from frozen `prereg.md` §13 to `raw_evidence/runner_blind_resolver.py` (block bytes + one trailing newline); sha256 `e9555d9e…dfffa` equals `CANONICAL-RUNNER-SHA256`.
2. Ran two `--mechanics-only` canaries: byte-identical, `test_not_scored=true`, blind_select tau=0.4286.
3. Ran the scored run to `raw_evidence/run_output.json` (sha256 `b85b9db5…89156b`). `result.json`/`report.md`/`provenance.json` derive from `run_output.json` only.

## Raw outcome (observation, not interpretation)

- `status=COMPLETE`, `invalid_reasons=[]`, `decision=BLIND_FAILS` → transcribed `result.json{status=COMPLETE, outcome=FALSIFIES}` (a valid scientific negative).
- tau* emission (NEW evidence, unpublished at freeze): pooled feasible set holds 9 taus (`0.2727/0.3333/0.375/0.4/0.4286/0.5/0.5556/0.5714/0.6`); the G3-origin held-out SELECT slice (n=30) passes 8 of them — every feasible tau except `0.2727`. tau* = lower median of the 8-element H list = `0.4286`; `select_fallback=false`.
- Blind AXIS-G3-NEW reincluded gate at tau*=0.4286: FA 0.0 / coverage 0.375 / UP_excl 0.4444 / selective_acc 0.1333 (15 executed, 45 abstained) → gate-met=false (coverage and UP bars fail). `blind_inert=false`.
- Blind gates false on all four axes on both screened and reincluded supersets. Fork `GOLD_DOMINATES_BLIND_G3`.
- Resolution quality: blind SELECT selective_acc=0.0; blind G3 reincluded selective_acc=0.1333 vs CTRL-BLIND-PERMUTED 0.0 at the same frozen tau (real slightly above permuted, still far below the 0.80 ship bar; gate-false regardless).

## Controls and baselines (all live)

- PC-AXIS-G1-ALTLEX gold-reincluded gate-met (no invalidity). NC-EXEC-ALL headroom confirmed on both supersets (reincluded FA 0.30–0.50 vs gold 0.05–0.20). NC-ABSTAIN-ALL coverage 0.0 both supersets with informative UP. Shuffled/random-role near chance; random-gate FA 0.50–0.75.
- Gold continuity reproduced exactly: screened `{G3 met, G1 met, ALTLEX met, G2 false}`; reincluded identical; G3 reincluded gold FA 0.10/cov 1.0/UP 1.0/selective 1.0 (42/60 executed).
- B-RETRIEVAL-OOS refit `tau=0.4156, mu=0.0005, mu_active=true`; fork `TFRAME_DOMINATES_G3` both supersets; no retrieval TEST gate met anywhere.
- Fit-pool bars exact (102/34/60, disjointness holds); flagged TEST gids match parent-published lists; no forbidden fallback taken.

## Interpretation (bounded)

H1 (held-out-axis blind viability) is retired for this mechanism-plus-calibration class at the frozen held-out rule: BLIND_FAILS persists under a third, non-extremal, held-out-axis calibration rule (tau*=0.4286, non-fallback emission) while G1/G2 negatives are tau-robust. The Director's which-rule question is answered negatively for the held-out slice: the frozen `heldout-g3-covup-median` rule selects 0.4286, not the knife-edge 0.3333 (the sole feasible-and-passing tau), because the slice passes 8 of 9 feasible taus and the median of that set lands mid-list.

Scope guards (carried, not new claims): this closes the blind Jaccard-1NN thread per the mandate stop trigger (retrieval-B or structured architecture only; Graph freed for first-party product-econ work) but does NOT establish calibration-robust gate-incapability of all lexicon-free mechanisms, does NOT retire the mechanism class beyond the tested calibration family, and promotes nothing to Product Core. The knife-edge 0.3333 pass remains a post-hoc observation, not a pre-registered survival. Claim status itself is the lane Director's verdict, not this packet's.

## Validity notes and unresolved

See `result.json#validity_notes` (screened legs as reproduction; post-hoc-knowledge structural mitigation; conditional-entailment disclosure; inclusive-precision sensitivity-only; pooled-dilution continuity; zero model/network/browser cost) and `result.json#unresolved` (non-pre-registered rules out of scope; 0.2727 slice-exclusion cause not separated; selective_acc hardening unmeasured).
