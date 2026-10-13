# EXP-GRAPH-38291080992 — Execute report (graph lane, C-SEMANTIC-RESOLVE liveness repair)

- experiment: `EXP-GRAPH-38291080992` (graph), design_contract_version 2, director mandate PIVOT cycle `38290683955`.
- Frozen inputs executed unchanged: `request.json`, `spec.json`, `prereg.md` (§13 FROZEN-RUNNER), `freeze.json`, `design_review.json` (PASS). All three `freeze.json.artifact_hashes` re-verified byte-identical at EXECUTE time.

## 1. What was run (raw evidence distinguished from interpretation)

1. Extracted `FROZEN-RUNNER` from `prereg.md#13.4` to `raw_evidence/runner_tframe_g3.py` with exactly one trailing newline; sha256 `11fa2467...edc7508` equals `CANONICAL-RUNNER-SHA256`.
2. Two `--mechanics-only` canary runs: byte-identical (`32e3d9cd...`), exit 0 — V2 canary requirement met before the scored run.
3. Scored run: `python3 research/experiments/EXP-GRAPH-38291080992/raw_evidence/runner_tframe_g3.py > raw_evidence/run_output.json`, exit 0, empty stderr (`run_stderr.txt` empty, sha `e3b0c44...`). Verbatim stdout preserved as `raw_evidence/run_output.json` (sha `8b986b96...`); a second scored run was byte-identical.
4. `result.json` metrics below are DERIVED MEASUREMENTS read off the raw evidence with frozen identifiers; §4 is INTERPRETATION. Nothing was refit, no third surface was authored, no frozen file was modified.

## 2. Observations (direct, not interpretations)

- Runner emitted `status=COMPLETE`, `decision=DECIDE_REQUIRE_RETRIEVAL_B`, `invalid_reasons=[]`, `runner_self_sha` = canonical.
- Repaired liveness on AXIS-G3-NEW test: `executed_total=38/56`, `executed_app=36`, `abstained_resolved=7` → `LIVE=True`.
- AXIS-G3-NEW test T-FRAME+: coverage `1.0`, `pooled_false_accept=0.10` (2/20, exactly at the `<=0.10` bar), `unknown_precision=1.0`, `selective_acc=1.0` → gate True.
- AXIS-G2-RETEST test T-FRAME+: coverage `0.925`, `pooled_false_accept=0.0`, `unknown_precision=0.8333 < 0.85`, `selective_acc=1.0` → gate False solely on UP.
- AXIS-G1-PRIMARY: FA `0.0556`, coverage `0.9464`, UP `1.0`, sel `0.9057` → gate True. AXIS-G1-ALTLEX: same FA/coverage/UP, sel `1.0` → gate True (positive control passes). `selection_preserved=True`.
- C7: 0 applicable firings on every axis; 2/4/2/1 OOS firings; test FA `0.20→0.10` (G3), `0.10→0.00` (G2) with C7.
- Arm B measurable (`tau=0.4278, mu=0.0`, feasible): G3 gate-met (FA `0.05`, UP `0.8636`, sel_acc `0.2727`); G2 collapse (FA `0.70`, UP `0.2857`, sel_acc `0.08`). Fork `BOTH_PASS_G3`.
- Controls moved: NC-EXEC-ALL FA `0.45/0.50/0.2778`; random-gate FA `0.65-0.75`; shuffled/random-role `0.03-0.08`; incumbent FA `0.20/0.20/0.1667`.

## 3. Derived measurement vs the frozen decision rule

- No invalidity trigger: liveness passes, UP defined on every axis, PC passes → valid measurement.
- `g3_gate=True, g2_gate=False` → neither BROAD nor SCOPED branch reachable → frozen cascade emits `DECIDE_REQUIRE_RETRIEVAL_B` (valid scientific bound, exactly the predicted informative outcome in `spec.json#decision_rule` / `prereg.md#8.10`).
- H1 (joint G3+G2 gate passage) does not hold as stated: G3 holds, G2 fails solely on UP — the shortfall reproduces deterministically under the frozen no-refit clause set, i.e. it is intrinsic to this clause set on this surface family, not measurement noise. H2 holds: Arm B is measurable and does not strictly dominate (`BOTH_PASS_G3` with selective_acc `1.0 vs 0.2727`, plus opposite G2 asymmetry `FA 0.0 vs 0.70` favouring structure).
- Outcome `MIXED` with `status=COMPLETE`: a valid bound, not a falsification of the architecture and not an infrastructure failure.

## 4. Interpretation (for DIRECTOR; does not promote anything by itself)

- The mandate's validity repair worked: the parent `MEASUREMENT_INVALID` (scope-defective liveness) is now a VALID packet reaching a frozen decision branch. The status confusion around C-SEMANTIC-RESOLVE can be adjudicated from this packet rather than the invalid parent.
- Evidence supports bounding (not shipping) the deterministic resolver: T-FRAME licensed at most on PRIMARY+ALTLEX on current evidence; Product keeps the conservative shipped abstention boundary. The G2 UP gap (10/12 vs 11/12 needed) is one resolved-abstention error from the bar, but under the no-refit constraint it is what the frozen clause set deterministically produces.
- The deterministic-vs-retrieval fork favours structure on this surface family despite `BOTH_PASS_G3`: Arm B pays a steep selectivity price on G3 and collapses on G2, while T-FRAME+ keeps selective_acc `1.0` on all four axes.
- Product consequence (frozen): REQUIRE_RETRIEVAL_B → do not ship the deterministic architecture; keep the conservative abstention boundary. Promotion, if ever, needs an audited verdict plus a separate Product-lane experiment.

## 5. Validity notes and unresolved

See `result.json#validity_notes` / `#unresolved`. Headlines: G3 FA sits exactly on the `0.10` boundary (stable here by determinism + hashes, fragile to perturbation); inherited nonblocking findings (hardcoded abstain-all/incumbent-kernel placeholders; PC-failure spec/runner divergence not triggered; else-branch label must be read with the fork field); stdlib-only, no model/network/browser/credential.
