# EXP-GRAPH-38666634300 report — Graph blind-resolver packet (EXECUTE)

## Question and frozen decision

Director question: does the gold-lexicon-conditional bound survive a genuinely
blind resolver (no surface lexicon at all) on the frozen banks?
Frozen rule: `BLIND_SURVIVES` iff blind `AXIS-G3-NEW` reincluded gate-met
(`pooled_false_accept<=0.10 AND coverage>=0.50 AND
unknown_precision_exclusive>=0.85`); else `BLIND_FAILS`. Blind degeneracy
(`BLIND_INERT`) was pre-handled as VALID collapse, never invalidity. Gating on
inclusive precision was pre-declared invalid.

## What was run (exactly the frozen design)

- Extracted `prereg.md#13` FROZEN-RUNNER to
  `raw_evidence/runner_blind_resolver.py` (sha256
  `296fcf26…38615a` == `CANONICAL-RUNNER-SHA256`); no frozen file modified.
- Two `--mechanics-only` canaries: rc=0, byte-identical stdout (sha256
  `43495829…87db8f3f9`), empty stderr, `test_not_scored=true`.
- One scored run -> `raw_evidence/run_output.json` (sha256
  `212b51f0…e79d11`), `status=COMPLETE`, `decision=BLIND_FAILS`,
  `invalid_reasons=[]`.
- `result.json`/`provenance.json` derive from `run_output.json` only, keeping
  frozen metric/control identifiers.

## RAW EVIDENCE -> OBSERVATION -> MEASUREMENT -> INTERPRETATION

- RAW: `run_output.json` (runner_self_sha matches canonical), two canary
  outputs, extracted runner. Hashes in `result.json#artifacts`.
- OBSERVATION: blind SELECT fitted `tau=0.2727` (feasible; FA 0.0833, COV 1.0,
  UP_excl 1.0, selective 0.0). Blind G3 reincluded: 44 executed (40 app +
  4 oos), 16 abstained, FA **0.20**, COV 1.0, UP_excl 1.0, selective **0.05**.
  Blind fails all four TEST gates on both supersets. Retrieval re-fits
  `(0.4156, 0.0005)` with fork `TFRAME_DOMINATES_G3` both supersets and no TEST
  gate met. Gold vectors reproduce the audited parent on both supersets.
  Permuted null at frozen tau reproduces the blind partition exactly
  (G3 reincl FA 0.20/COV 1.0/UP 1.0, selective 0.025 vs real 0.05).
- MEASUREMENT: `blind_g3_met=false`, `blind_inert=false`,
  `blind_fork_reincl=GOLD_DOMINATES_BLIND_G3`; continuity tripwires all pass
  (fit bars 102/34/60, flagged-gid equality, gold vectors, retrieval forks).
- INTERPRETATION: H1 (full-blind viability for BLIND-JAC-1NN) is retired on
  these banks — `outcome=FALSIFIES`, a valid scientific negative
  (`status=COMPLETE`, not an infrastructure failure). The failure mode is
  false-accept excess (0.20 > 0.10), not degeneracy and not abstention
  precision (UP 1.0). Selection quality is resolution-deficient throughout
  (blind TEST selective 0.0–0.095 vs permuted ~chance), consistent with the
  DESIGN expectation, but no grading is applied since the gate is false.

## Controls (all live, all pass)

- `PC-AXIS-G1-ALTLEX` gold-reincluded gate-met (FA 0.05/COV 0.9333/UP 1.0).
- `NC-EXEC-ALL` headroom on every axis/superset (e.g. G3 0.45 vs gold 0.10).
- `NC-ABSTAIN-ALL` executed both supersets (coverage 0.0 floor, UP
  informative). Shuffled/random-role near chance; random-gate FA 0.60–0.80.
- `CTRL-BLIND-PERMUTED` scoped to selection as pre-registered (label-invariant
  partition confirmed empirically); guards selective_acc only.
- Baselines: gold-T-FRAME+ reproduces parent vectors; tframe_frozen shows C7
  carrying G3 0.20->0.10; B-RETRIEVAL-OOS reproduces exactly
  (SELECT selective 0.0); ancestor resub/embedding arms identity-only.

## Product consequence (frozen negative branch)

BLIND_FAILS: full-blind ambitions retired on the frozen banks — two
lexicon-free memory statistics (TF-IDF centroid AND Jaccard 1-NN) fail all
TEST gates while the deterministic bound holds gold-conditionally and
collapses under foreign lexicons (parent XSURF, quoted not re-run). Park the
thread at PRIMARY+ALTLEX gold-lexicon-conditional bound; keep the conservative
shipped abstention boundary with the retrieval-B requirement vacated in the
gold-conditional sense; no further blind work without a new mechanism class
(structural-heuristic blind reserved as explicit follow-up, not spent here).
This packet promotes nothing itself.

## Validity notes and unresolved

See `result.json#validity_notes` (exclusive-denominator gating, tripwire vs new
evidence, stdlib-only/blindness contract, frozen-banks scope) and
`result.json#unresolved` (other blind mechanism classes, dilution-vs-weakness
cause, carried G1-identity/G3-slack caveats). Consistent with `result.json`;
no claim beyond the frozen `C-SEMANTIC-RESOLVE` scope is made here.
