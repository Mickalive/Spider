# EXP-GRAPH-38816768796 execution report — Graph tau-rule-sensitivity packet (max-slack feasible-tau)

## Question and design (frozen)

Binding direction: `request.json#director_mandate` (cycle 38816465757, Graph REOPEN on C-SEMANTIC-RESOLVE).
Director question: under a pre-registered feasible-tau selection rule that is not lowest-tau-wins,
does the word-unigram Jaccard 1-NN blind resolver survive the frozen AXIS-G3-NEW reincluded G3 gate,
or does BLIND_FAILS persist independent of the ascending-tau tie-break?

Single-variable ablation vs parent EXP-GRAPH-38666634300: the blind SELECT rule changes from
ascending-tau first-max to feasibility-plus-maximum-FA-slack
(`tau* = argmax (FA_TARGET − SELECT pooled_false_accept)`, tie-break higher tau wins).
Every other byte of analysis logic is identical. Decision gate (exclusive denominator only):
`pooled_false_accept<=0.10 AND coverage>=0.50 AND unknown_precision_exclusive>=0.85`
on AXIS-G3-NEW reincluded TEST at the frozen `tau*`.

## Execution (exactly the frozen design)

1. Re-verified all four `freeze.json#artifact_hashes` — all match (see `provenance.json`).
2. Extracted the `FROZEN-RUNNER` block (prereg §13) to
   `raw_evidence/runner_blind_resolver.py` (+ one trailing newline);
   sha256 `d4356386…f536f` equals `CANONICAL-RUNNER-SHA256`.
3. Ran `--mechanics-only` twice before any TEST scoring: byte-identical
   (sha `5dc12049…4450`), `test_not_scored=true` in both. Saved as
   `raw_evidence/mechanics_only_run1/2.json`.
4. Ran the full frozen runner once; output saved to `raw_evidence/run_output.json`
   (sha `9116cd3f…93212`). No frozen file was modified; no refit, no new surface.

## Raw outcome (no interpretation)

- Runner status `COMPLETE`, `invalid_reasons=[]`, `decision=BLIND_FAILS`.
- Blind SELECT rule emitted `tau*=0.6`, `select_slack=0.1`
  (SELECT: FA 0.0, coverage 0.7941, UP_excl 0.8955, selective_acc 0.0; feasible=true).
  `tau* != 0.2727`, so the tie-break factor was genuinely varied.
- Blind AXIS-G3-NEW **reincluded** TEST at `tau*=0.6`:
  coverage 0.10, pooled FA 0.0, UP_excl 0.3571, selective_acc 0.0
  (4 executed: 4 app / 0 oos; 56 abstained) → gate **false**. `blind_inert=false`.
- Blind fails all four TEST gates on screened AND reincluded sets;
  reincluded fork `GOLD_DOMINATES_BLIND_G3`.
- Retrieval OOS reproduced exactly: tau=0.4156, mu=0.0005, mu_active=true;
  fork `TFRAME_DOMINATES_G3` both supersets; no TEST gate met either superset.
- Gold continuity tripwires all hold: screened gates {G3 met, G2 false, G1 met, ALTLEX met};
  reincluded gates identical; flagged TEST gids exactly parent-published;
  gold G3 reincluded live (cov 1.0, FA 0.10, UP 1.0, selective 1.0).
- Permuted blind at frozen `tau*=0.6`: SELECT selective 0.0 = real blind 0.0;
  G3 reincluded vector identical to real blind; `permuted_g3_met=false`
  (scoped to the selection reading per prereg §6, as designed).
- All controls live on both supersets: execute-all FA headroom
  (G3 0.45 vs gold 0.10; G2 0.50 vs gold 0.0); abstain-all coverage 0.0 with
  informative UP; shuffled/random-role near chance (0.0–0.10);
  random-gate FA 0.55–0.72.

## Interpretation (bounded)

Per the frozen transcription rule, `BLIND_FAILS` maps to
`result.json{status=COMPLETE, outcome=FALSIFIES}` — a valid scientific negative,
not an infrastructure failure. The word-unigram Jaccard 1-NN blind path now fails the
frozen G3 reincluded gate under **both** the lowest-tau rule (parent, FA 0.20 at tau=0.2727)
and the max-slack rule (this packet, coverage/UP collapse at tau*=0.6), while G1/G2
negatives are tau-robust across both packets. The tie-break confound is closed:
the failure travels with the mechanism, not the calibration rule.

Note the failure mode moved, as the packet predicted: at the conservative `tau*=0.6`
the blind arm over-abstains (coverage 0.10, UP 0.3571) rather than over-accepting
(parent FA 0.20). Resolution quality is absent in both regimes (selective 0.0 here,
0.05 parent; permuted identical). No ship-grade reading is available on any branch.

## Product consequence (frozen negative leg)

Park the blind thread at the PRIMARY+ALTLEX gold-lexicon-conditional bound; keep the
conservative shipped abstention boundary with the retrieval-B requirement vacated in the
gold-conditional sense; no further Jaccard-1NN blind work without a new mechanism class
(structural-heuristic blind held as explicit follow-up). HYPOTHESIS retained with
hardened ceiling. This packet promotes nothing itself.

## Validity notes and unresolved

See `result.json#validity_notes` (screened legs are reproduction tripwires; SELECT-only
tau* computation before TEST scoring; disclosed post-hoc-knowledge mitigation;
exclusive-denominator gating; no model/network/browser/packages; G1 text-identity and
G3 zero-slack fragility carried as ceilings; ancestor arms as identities only)
and `result.json#unresolved` (other blind mechanism classes; pooled-dilution vs
intrinsic weakness; no powered OOS-denominator margin reading).
