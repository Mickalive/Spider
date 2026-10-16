# EXP-GRAPH-38530149021 report — Graph sensitivity packet: screen re-inclusion + cross-surface lexicon (EXECUTE)

Lane: graph. Claim: C-SEMANTIC-RESOLVE. Status: COMPLETE. Outcome: SUPPORTS (decision BOUND_ROBUST).

## Binding question

Does the DECIDE_REQUIRE_RETRIEVAL_B bound survive a pre-registered sensitivity packet that (a) re-includes the frozen-screen-dropped TEST rows and (b) removes the gold-lexicon asymmetry via a blind/cross-surface lexicon arm — isolating whether the G2 one-row margin and the TFRAME_DOMINATES_G3 fork are robust or artifacts?

## What was run (frozen design, no deviation)

- Extracted the FROZEN-RUNNER (§13 of prereg.md) to `raw_evidence/runner_tframe_sensitivity.py` (block bytes + one trailing newline). sha256 `89baf53026da8b33d80bf891a7c116b69b5bec8f60c9ae55a3ef8c484984ce29` equals CANONICAL-RUNNER-SHA256 and the run's `runner_self_sha`.
- `--mechanics-only` twice: rc=0 both, byte-identical stdout (sha `9251f48e0212196b2d0f4a51d54bb0a7ae5f3e59c6fc0b8b384f78457393dfc2`, matching the DESIGN probe), `test_not_scored=true`, empty stderr.
- Single scored run to `raw_evidence/run_output.json` (sha `c5a1786f0f89da9e872466fb7eb351244221bcd0456e5e7ae410f5063723ef54`).
- Freeze artifact hashes re-verified unchanged (all four match `freeze.json`).
- No clause refit, no resubstitution, no mu==0 gate, no TEST-row use in fit/select.

## RAW EVIDENCE vs observations vs measurements vs interpretation

- RAW EVIDENCE: `raw_evidence/run_output.json` (+ runner, mech probes). Nothing else carries scientific state.
- OBSERVATIONS: see `result.json#observations` (direct run outputs, no interpretation).
- DERIVED MEASUREMENTS: `result.json#metrics` (gates, forks, SELECT gate, fit bars, selective_acc, C7 counts, controls summary).
- INTERPRETATION (this report + `result.json` outcome/decision): the bound is screen- and fork-stable AND gold-lexicon-conditional.

## Results

Screened reproduction (validity tripwire, disclosed non-evidence): gold-screened gate vector {G3 met, G1 met, ALTLEX met, G2 false-solely-on-UP with FA 0.0<=0.10 and coverage 0.925} exactly as parent-published; screened fork TFRAME_DOMINATES_G3; screened retrieval fails all four TEST gates; cross flagged-gid sets equal gold (xdiv empty). All §7 invalidity triggers clear.

NEW evidence 1 — screen re-inclusion: `screen_stable=true`. G3 gate stays met (executed 38->42, abstR 7 unchanged, UP-excl 1.0); G1-PRIMARY/ALTLEX stay met (FA 0.0556->0.05, UP-excl 1.0, coverage 0.9464->0.9333); G2 byte-identical (0 flagged TEST rows, `g2_reincl_identical=true`, UP-excl 0.8333 both); `selection_reincl == selection_preserved` (all axes >=0.80 both supersets).

NEW evidence 2 — reincluded fork: `fork_stable=true`. Retrieval-OOS (SELECT tau=0.4156, mu=0.0005, mu_active, feasible) fails every TEST gate on both supersets (screened G3 UP 0.7037; reincluded G3 UP 0.6786; G2/G1 coverage-bound both). Fork TFRAME_DOMINATES_G3 on both.

NEW evidence 3 — lexicon asymmetry: `gold_dependent=true`. Under the fixed foreign-surface derangement every gold-met axis fails on screened AND reincluded sets (xgates all false; xcoverage 0.0 all axes; xresolved G3 2, G2 0, G1 2, ALTLEX 2). Pre-declared VALID floor collapse, never invalidity.

Controls all pass: PC-AXIS-G1-ALTLEX met; NC-EXEC-ALL headroom on all three set families (screened FA 0.2778–0.50 vs Arm A 0.0–0.10; reincluded and cross re-reported); NC-ABSTAIN-ALL executed on both supersets (coverage 0.0, informative UP); shuffled/random-role near chance both supersets; random-gate FA in the 0.60–0.75 band both supersets; incumbent lexical reference recorded.

## Interpretation and product consequence

- H1 (screen-robustness) SUPPORTED; H2 (fork robustness) SUPPORTED: `BOUND_ROBUST` (screen_artifact=false, fork_artifact=false).
- The published G2 one-row margin is screen-invariant (analytic + runtime-verified), and the TFRAME_DOMINATES_G3 fork persists under symmetric screen handling.
- The ceiling is gold-lexicon-conditional (`gold_dependent=true`): the bound holds with surface lexicons and collapses without them. Per the frozen consequence: keep the conservative shipped abstention boundary, keep the fork resolved toward REQUIRE_RETRIEVAL_B (vacated as specified), reopen blind/cross-surface resolver work without promotion. This packet promotes nothing itself.
- Gating on `unknown_precision_inclusive` was and remains invalid; all decisions use the exclusive denominator.

## Validity notes and unresolved

See `result.json#validity_notes` (reproduction-as-validity-leg, pooled-dilution bias against retrieval, G1 text-identity across three surfaces, G3 applicable-bank simplicity, inclusive-denominator quarantine, cross-G2 UP-null pre-handling, per-row vector preservation) and `result.json#unresolved` (full-blind-resolver survival; alternative SELECT selection rules with SELECT selective_acc 0.0 noted).
