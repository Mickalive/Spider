# Preregistration — EXP-GRAPH-38188798583 (DESIGN ONLY, v2)

## Experiment
- Experiment ID: EXP-GRAPH-38188798583
- Lane: graph
- Design contract: v2
- Claim(s): [C-SEMANTIC-RESOLVE]
- Request: research/experiments/EXP-GRAPH-38188798583/request.json (immutable)
- Parent handoff: research/experiments/EXP-GRAPH-38180711589/handoff.json (continuity evidence only; does not override Director mandate)

## Research question (binding)
The Director’s strategic question (binding): see spec.json.question.

## Hypothesis
See spec.json.hypothesis.

## Falsifier
See spec.json.falsifier.

## Arms
- Arm A (primary, feasible now): model-free structured slot/parameter binding with an explicit, independently checkable abstention condition (stdlib-only). No embedding stack required.
- Arm B (comparator): retrieval/embedding resolver trained on independently authored goals. BLOCKED by default unless embedding stack (numpy/scipy/scikit-learn/torch/sentence-transformers) is provisioned with a resolvable pinned model revision.

## Splits and generalization
- Calibration/test splits are disjoint. Threshold selection on calibration ONLY (V4).
- Generalization: held-out mechanism set and independently curated synonym lexicon. Selection advantage must be preserved on both (SELECTION_PRESERVED).

## Metrics (stable identifiers)
Primary gate triplet (test split):
- pooled_false_accept_test (target <= 0.10)
- coverage_test (target >= 0.50)
- unknown_precision_test (target >= 0.85)
- unknown_precision_inclusive_test (diagnostic >= 0.80)

Selection (must preserve):
- B-LEX-STRONG selection accuracy on held-out mechanism set (>= 0.80) and synonym lexicon (>= 0.80), >= baseline 0.8584 where applicable.

Controls: CTRL-RANDOM-GATE, NC-SHUFFLED-LABEL, B-LEX-ONLY, B-INCUMBENT-KERNEL, B-RANDOM-ROLE, PC-LIVENESS-AND-INTEGRITY.

## Measurement validity gates (V1–V13)
V1-FREEZE_BINDING, V2-SPLIT_DISJOINT, V3-CONTAMINATION_BOUNDS (max_token_jaccard<0.60, max_trigram_jaccard<0.75), V4-THRESHOLD_ON_CAL_ONLY, V5-PREREQ_ARM_B_BLOCKED_HANDLED, V6-TAUTOLOGY_CHECK, V7-NON_CEILING_FLOOR, V8-ARMS_INDEPENDENT, V9-EMBEDDER_PATH_ISOLATED, V10-UNKNOWN_PRECISION_N_SENSITIVITY (effective n tracked), V11-BOOTSTRAP_SEED_IF_ATTEMPTED, V12-FREEZE_ARTIFACTS_HASHED, V13-DECISION_BRANCH_REACHABLE.

## Decision rule
Primary: GATE_MET if pooled_false_accept_test <= 0.10 AND coverage_test >= 0.50 AND unknown_precision_test >= 0.85. SELECTION_PRESERVED if selection acc on held-out mech >= 0.80 AND on synonym lex >= 0.80 AND B-LEX-STRONG preserved/exceeded. Outcomes: DECIDE_SHIP_A, DECIDE_REQUIRE_B, DECIDE_BLOCK. Tie-break: prefer model-free if meets gate+selection.

## Product consequences
Positive: license shipping deterministic resolver + calibrated abstention gate (Arm A). Negative: do not ship; require architectural change; keep resolve() UNKNOWN for low-confidence unseen goals.

## Epistemic posture
This is DESIGN ONLY (no outcome-bearing measurements). Cheap satisfiability probes allowed. We do not re-tune the frozen integer signal family; we test a materially different architectural abstention approach (Arm A). Parent handoff carry-forward preserved (established/rejected/unknown/do_not_assume). For v2, all freeze_eligibility checks filled per contract.

## Design attack (self-critique)
Checked: empty/unreachable branches (covered by V13, explicit decision branches), missing prerequisites (Arm B blocked with V5), treatment/comparator identity (V8), ceiling baselines (V7), insensitive controls (random-gate, shuffled-label), mutable dependencies (freeze_artifacts empty with NOT_APPLICABLE justification). No outcome measurements planned in DESIGN.
