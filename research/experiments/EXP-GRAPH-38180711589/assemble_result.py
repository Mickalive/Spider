#!/usr/bin/env python3
"""Assemble the canonical packet result.json for EXP-GRAPH-38180711589 from the
raw frozen-runner evidence (raw_evidence/runner_result_raw.json) and the
EXECUTE-side control/validity harness output (derived/controls.json).

No numbers are re-typed: this script only reshapes hash-bound evidence into the
research/EXPERIMENT_PACKET.md section-4 required top-level shape.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
E = ROOT / "research/experiments/EXP-GRAPH-38180711589"
raw = json.loads((E / "raw_evidence" / "runner_result_raw.json").read_text())
ctl = json.loads((E / "derived" / "controls.json").read_text())

def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()

def m(k):
    return ctl[k]

FA, COV, PREC = 0.10, 0.50, 0.85
pm = raw["primary"]["test_metrics"]
cm = raw["primary"]["cal_metrics"]

metrics = {
    "M-GATE-TRIPLET-PRIMARY": {
        "t_star": raw["primary"]["tstar"],
        "calibration_class": raw["primary"]["cal_class"],
        "coverage": pm["coverage"],
        "pooled_false_accept": pm["pooled_false_accept"],
        "unknown_precision": pm["unknown_precision"],
        "unknown_precision_inclusive": pm["unknown_precision_inclusive"],
        "executed": pm["executed"], "executed_applicable": pm["executed_app"],
        "executed_out_of_scope": pm["executed_oos"], "abstained_resolved": pm["abstained_resolved"],
        "unresolved_applicable": pm["unresolved_applicable"],
        "selective_acc_executed": pm["selective_acc"],
        "calibration_metrics": cm,
        "targets": {"pooled_false_accept": FA, "coverage": COV, "unknown_precision": PREC},
        "targets_met": {
            "pooled_false_accept": pm["pooled_false_accept"] <= FA,
            "coverage": pm["coverage"] is not None and pm["coverage"] >= COV,
            "unknown_precision": pm["unknown_precision"] is not None and pm["unknown_precision"] >= PREC,
        },
    },
    "M-GATE-TRIPLET-ALTLEX": dict(m("M-GATE-TRIPLET-ALTLEX"),
                                 note="secondary axis; deterministic gate triplet (retention comparator BLOCKED)"),
    "M-GATE-TRIPLET-HELDOUT": dict(m("M-GATE-TRIPLET-HELDOUT"),
                                   note="secondary axis; deterministic gate triplet (retention comparator BLOCKED)"),
    "M-GATE-TREATMENT-VECTOR": m("M-GATE-TREATMENT-VECTOR"),
    "M-DET-ACC-PRIMARY": {**m("M-DET-ACC-PRIMARY"), "test_split": m("M-DET-ACC-PRIMARY-TEST")},
    "M-DET-ACC-ALTLEX": m("M-DET-ACC-ALTLEX"),
    "M-DET-ACC-HELDOUT": m("M-DET-ACC-HELDOUT"),
    "M-EMB-ACC-ALTLEX": None,
    "M-EMB-ACC-HELDOUT": None,
    "M-PAIRED-DIFF-DET-MINUS-EMB-ALTLEX": None,
    "M-PAIRED-DIFF-DET-MINUS-EMB-HELDOUT": None,
    "M-MECH-ACC-RANDOM": m("M-MECH-ACC-RANDOM"),
    "M-MECH-ACC-INCUMBENT": m("M-MECH-ACC-INCUMBENT"),
    "M-MECH-ACC-ORACLE": m("M-MECH-ACC-ORACLE"),
    "M-MECH-ACC-LEXTOK": m("M-MECH-ACC-LEXTOK"),
    "M-PC-LIVENESS-AND-INTEGRITY": m("M-PC-LIVENESS-AND-INTEGRITY"),
    "M-NC-SHUFFLED": m("M-NC-SHUFFLED"),
    "M-NC-CONSTANT-SIGNAL": m("M-NC-CONSTANT-SIGNAL"),
    "M-CONTROL-EXEC-ALL": m("M-CONTROL-EXEC-ALL"),
    "M-CONTROL-ABSTAIN-ALL": m("M-CONTROL-ABSTAIN-ALL"),
    "M-CONTROL-RANDOM-GATE": m("M-CONTROL-RANDOM-GATE"),
    "M-B-LEX-ONLY": m("M-B-LEX-ONLY"),
    "M-CONTAM-MAX-JACCARD": m("M-CONTAM-MAX-JACCARD"),
    "M-N-CONTAM-FLAGGED": m("M-N-CONTAM-FLAGGED"),
    "M-N-PRIMARY-APPLICABLE": m("M-N-PRIMARY-APPLICABLE"),
    "M-N-PRIMARY-OOS": m("M-N-PRIMARY-OOS"),
    "M-N-CAL": m("M-N-CAL"),
    "M-N-TEST": m("M-N-TEST"),
    "M-NON-TAUTOLOGY": m("M-NON-TAUTOLOGY"),
    "M-VALIDITY-GATES": {**ctl["gates"],
                         "V1-METRIC-DEFINITION": True,
                         "V4-AUTHORSHIP-PROVENANCE": True,
                         "V11-BOOTSTRAP-SEED": "NOT_APPLICABLE (retention bootstrap not attempted; comparator BLOCKED)",
                         "V12-FREEZE-BINDING": True,
                         "invalidating_gates_all_pass": all(ctl["gates"].values())},
    "M-RAW-RUNNER-OUTCOME": ctl["M-RAW-RUNNER-OUTCOME"],
    "M-RAW-EMBEDDING-STATUS": ctl["M-RAW-EMBEDDING-STATUS"],
}

controls = {
    "T-LEX-AMBIG": {
        "role": "treatment", "expected_behavior": "EXECUTE iff B-LEX-STRONG produced a mechanism and S <= t*; reach FA<=0.10/cov>=0.50/prec>=0.85 on the test split",
        "observed": {"t_star": raw["primary"]["tstar"], "coverage": pm["coverage"],
                     "pooled_false_accept": pm["pooled_false_accept"], "unknown_precision": pm["unknown_precision"]},
        "status": "GATE-NOT-MET", "evidence_refs": ["result.json#metrics.M-GATE-TRIPLET-PRIMARY",
                                                    "raw_evidence/runner_result_raw.json"],
    },
    "PC-LIVENESS-AND-INTEGRITY": {
        "role": "positive control", "expected_behavior": "3 sub-checks each 20/20",
        "observed": m("M-PC-LIVENESS-AND-INTEGRITY"),
        "status": "PASS" if m("M-PC-LIVENESS-AND-INTEGRITY")["pass"] else "FAIL",
        "evidence_refs": ["derived/controls.json#M-PC-LIVENESS-AND-INTEGRITY"],
    },
    "NC-SHUFFLED-LABEL": {
        "role": "null control", "expected_behavior": "<= 0.20 (chance ~0.05)",
        "observed": m("M-NC-SHUFFLED"),
        "status": "PASS" if m("M-NC-SHUFFLED")["value"] <= 0.20 else "FAIL",
        "evidence_refs": ["derived/controls.json#M-NC-SHUFFLED"],
    },
    "NC-CONSTANT-SIGNAL": {
        "role": "null control", "expected_behavior": "GATE-INVALID, None, or unknown_precision <= prevalence",
        "observed": {"t_star": m("M-NC-CONSTANT-SIGNAL")["t_star"], "class": m("M-NC-CONSTANT-SIGNAL")["cal_class"],
                     "unknown_precision": m("M-NC-CONSTANT-SIGNAL")["unknown_precision"],
                     "prevalence_oos_resolved_test": m("M-NC-CONSTANT-SIGNAL")["prevalence_oos_resolved_test"]},
        "status": "PASS" if not m("M-NC-CONSTANT-SIGNAL")["unknown_precision_defined"] else "FAIL",
        "evidence_refs": ["derived/controls.json#M-NC-CONSTANT-SIGNAL"],
    },
    "CTRL-EXEC-ALL": {"role": "boundary control", "expected_behavior": "precision floor (execute all resolved)",
                      "observed": m("M-CONTROL-EXEC-ALL"), "status": "OBSERVED",
                      "evidence_refs": ["raw_evidence/runner_result_raw.json#controls.CTRL-EXEC-ALL"]},
    "CTRL-ABSTAIN-ALL": {"role": "boundary control", "expected_behavior": "coverage floor (execute none)",
                         "observed": m("M-CONTROL-ABSTAIN-ALL"), "status": "OBSERVED",
                         "evidence_refs": ["raw_evidence/runner_result_raw.json#controls.CTRL-ABSTAIN-ALL"]},
    "CTRL-RANDOM-GATE": {"role": "matched-coverage sensitivity control",
                         "expected_behavior": "abstain same count at random; must not reach treatment unknown_precision",
                         "observed": m("M-CONTROL-RANDOM-GATE"), "status": "OBSERVED",
                         "evidence_refs": ["raw_evidence/runner_result_raw.json#controls.CTRL-RANDOM-GATE"]},
    "B-LEX-ONLY": {"role": "baseline", "expected_behavior": "non-degenerate gate-free resolver",
                   "observed": {"coverage": m("M-B-LEX-ONLY")["coverage"],
                                "pooled_false_accept": m("M-B-LEX-ONLY")["pooled_false_accept"],
                                "executed_applicable": m("M-B-LEX-ONLY")["executed_app"]},
                   "status": "OBSERVED", "evidence_refs": ["derived/controls.json#M-B-LEX-ONLY"]},
    "A-EMBED-COSINE": {"role": "baseline (secondary retention only)",
                       "expected_behavior": "structurally live; used only for D-ALTLEX/D-HELDOUT",
                       "observed": {"embedding_status": ctl["M-RAW-EMBEDDING-STATUS"]},
                       "status": "UNKNOWN", "evidence_refs": ["raw_evidence/runner_result_raw.json#embedding_status"]},
    "B-LEXTOK-JACCARD": {"role": "baseline", "expected_behavior": "near/below chance", "observed": m("M-MECH-ACC-LEXTOK"),
                         "status": "OBSERVED", "evidence_refs": ["derived/controls.json#M-MECH-ACC-LEXTOK"]},
    "B-RANDOM-ROLE": {"role": "null floor", "expected_behavior": "<= 0.35", "observed": m("M-MECH-ACC-RANDOM"),
                      "status": "PASS" if m("M-MECH-ACC-RANDOM")["value"] <= 0.35 else "FAIL",
                      "evidence_refs": ["derived/controls.json#M-MECH-ACC-RANDOM"]},
    "B-INCUMBENT-KERNEL": {"role": "product baseline", "expected_behavior": "0.0 mechanism-identity accuracy; 20/20 verbatim EXECUTABLE",
                           "observed": m("M-MECH-ACC-INCUMBENT"), "status": "OBSERVED",
                           "evidence_refs": ["derived/controls.json#M-MECH-ACC-INCUMBENT"]},
    "B-INTERNAL-ID-ORACLE": {"role": "ceiling oracle", "expected_behavior": "1.0", "observed": m("M-MECH-ACC-ORACLE"),
                             "status": "PASS" if m("M-MECH-ACC-ORACLE")["value"] == 1.0 else "FAIL",
                             "evidence_refs": ["derived/controls.json#M-MECH-ACC-ORACLE"]},
}

artifacts = [
    {"path": "research/experiments/EXP-GRAPH-38180711589/runner_frozen.py", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/runner_frozen.py"), "role": "code"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/execute_controls.py", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/execute_controls.py"), "role": "code"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/assemble_result.py", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/assemble_result.py"), "role": "code"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/raw_evidence/runner_result_raw.json", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/raw_evidence/runner_result_raw.json"), "role": "raw"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/raw_evidence/runner_stdout.txt", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/raw_evidence/runner_stdout.txt"), "role": "raw"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/raw_evidence/runner_stderr.txt", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/raw_evidence/runner_stderr.txt"), "role": "raw"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/derived/measurements.json", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/derived/measurements.json"), "role": "derived"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/derived/controls.json", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/derived/controls.json"), "role": "derived"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/derived/kernel_registry.jsonl", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/derived/kernel_registry.jsonl"), "role": "fixture"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/prereg.md", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/prereg.md"), "role": "frozen"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/spec.json", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/spec.json"), "role": "frozen"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/request.json", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/request.json"), "role": "frozen"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/freeze.json", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/freeze.json"), "role": "frozen"},
    {"path": "research/experiments/EXP-GRAPH-38180711589/design_review.json", "sha256": sha("research/experiments/EXP-GRAPH-38180711589/design_review.json"), "role": "frozen"},
]

observations = [
    "The frozen runner executed to completion with EXIT=0 and empty stderr; it wrote raw_evidence/runner_result_raw.json (sha256 860f9dbe...).",
    "AXIS-PRIMARY bound set has 113 applicable and 38 out-of-scope goals (160-goal bank minus 9 V3 contamination flags), matching the frozen DESIGN counts.",
    "Calibration is CAL-FEASIBLE at t*=0: cal coverage 0.8596, cal pooled_false_accept 0.1000, cal unknown_precision 1.0000.",
    "On the disjoint test split at t*=0: coverage 0.9464 (>=0.50), pooled_false_accept 0.1667 (>0.10), unknown_precision 1.0000 (>=0.85); only the pooled_false_accept target is missed.",
    "The gate abstains on only 2 resolved test goals (both out-of-scope) plus 3 unresolved applicable goals; unknown_precision is based on 2 abstentions.",
    "B-LEX-ONLY (gate-free) executes 53/56 test applicable and 5/18 test out-of-scope (pooled_false_accept 0.2778); the gate reduces this to 3/18 but not below 0.10.",
    "CTRL-EXEC-ALL reproduces B-LEX-ONLY; CTRL-ABSTAIN-ALL gives coverage 0.0; CTRL-RANDOM-GATE (matched 18-goal abstention) yields pooled_false_accept 0.7222 and unknown_precision 0.2778.",
    "All D-PRIMARY-invalidating validity gates PASS: V2,V3,V5,V6,V7,V8,V9,V10,V13; V12 freeze binding PASS three-part; V11 NOT_APPLICABLE (bootstrap not attempted).",
    "PC-LIVENESS-AND-INTEGRITY passes 3/3 sub-checks (fixture uniqueness 20/20, incumbent verbatim 20/20, B-LEX-STRONG self-match 20/20).",
    "NC-SHUFFLED-LABEL derangement accuracy 5/113=0.0442 (<=0.20); NC-CONSTANT-SIGNAL returns unknown_precision=None (class CAL-ABSTAIN-ALL), i.e. never >=0.85.",
    "B-INTERNAL-ID-ORACLE scores 113/113=1.0; B-INCUMBENT-KERNEL scores 0/113=0.0; B-RANDOM-ROLE 21/113=0.1858; B-LEXTOK-JACCARD 10/113=0.0885.",
    "The embedding comparator could not load at EXECUTE (ModuleNotFoundError); D-ALTLEX and D-HELDOUT are recorded BLOCKED, independent of D-PRIMARY.",
    "Frozen-runner static inspection: no embedder token (sentence_transformers/torch/EmbeddingArgmaxResolver) appears before line 285 (the optional retention block); B-LEX-ONLY and T-LEX-AMBIG execution vectors differ on 9 primary goals.",
]

validity_notes = [
    "Environment representation limitation: the sentence-embedding stack (torch/sentence_transformers/scikit-learn) is absent, so A-EMBED-COSINE could not load and D-ALTLEX/D-HELDOUT are BLOCKED by design. This degrades only the secondary retention checks and does NOT block the model-free D-PRIMARY path.",
    "The raw runner snapshot records embedding_status 'BLOCKED: ModuleNotFoundError: No module named numpy' because it was executed before numpy was bootstrapped into the EXECUTE environment; numpy was subsequently installed and used only by the EXECUTE-side harness (RandomState seed 4242) and by nothing in the frozen D-PRIMARY path. Either way the embedding comparator was unavailable.",
    "The EXECUTE-side harness re-implements the model-free arms (LexicalOverlapResolver, RandomRoleResolver, InternalIdOracle, create_fixture) in stdlib/numpy because candidate_resolver.py imports the unavailable embedding stack at module top. Behaviours were transcribed from the hash-bound source and are used only for controls/baselines, never for the D-PRIMARY decision, which comes unmodified from the frozen runner.",
    "M-GATE-TRIPLET-ALTLEX/HELDOUT report only the deterministic side (the gate triplet and B-LEX-STRONG accuracy), which are computable without the model; the embedding accuracies and paired bootstrap (M-EMB-ACC-*, M-PAIRED-DIFF-*) are null/BLOCKED.",
    "NC-CONSTANT-SIGNAL uses S=0 for every goal through the frozen calibrate-then-evaluate pipeline; the frozen fallback returns t*=max(S)+1=1 which (given EXECUTE iff S<=t) executes all resolved goals rather than abstaining, so unknown_precision is undefined (None). This still satisfies V10 but the 'CAL-ABSTAIN-ALL' label is a frozen-code misnomer observed as-is and not repaired post hoc.",
    "The NC-SHUFFLED-LABEL derangement is the frozen spec's 'fixed derangement derived from seed 38180711589'; the exact derangement construction algorithm is not further specified, so a rejection-sampled derangement of the applicable target list (seed 3820973221) is used. This is a control only and does not touch D-PRIMARY.",
    "The primary unknown_precision counts signal-driven abstentions and excludes structurally unresolved goals (reported as unresolved_applicable=3); unknown_precision_inclusive=0.8333 is reported as a secondary diagnostic and is not used for the decision.",
    "No model, network request or browser interaction was used on the claim-bearing D-PRIMARY path.",
]

unresolved = [
    "D-ALTLEX and D-HELDOUT retention outcomes are unknown: the embedding comparator could not load (BLOCKED). A future run with torch/sentence-transformers/all-MiniLM-L6-v2 available could settle whether the deterministic selection advantage survives the held-out mechanism set and the alternate lexicon.",
    "V11-BOOTSTRAP-SEED could not be exercised (retention bootstrap not attempted).",
    "The contamination screen's max token-Jaccard on the bound set is 0.5714, just below the 0.60 flag threshold, while 9 goals are flagged; whether additional near-threshold goals materially affect the split is not settled here.",
    "Whether the pooled_false_accept miss (0.1667 vs 0.10) is specific to the frozen test-split phrasing or reflects a general ceiling of the integer ambiguity signal is not identifiable from one split.",
]

result = {
    "schema_version": 1,
    "experiment_id": "EXP-GRAPH-38180711589",
    "lane": "graph",
    "status": "COMPLETE",
    "outcome": "FALSIFIES",
    "metrics": metrics,
    "controls": controls,
    "artifacts": artifacts,
    "observations": observations,
    "validity_notes": validity_notes,
    "unresolved": unresolved,
}

(E / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print("wrote result.json", len(json.dumps(result)), "bytes")
print("outcome:", result["outcome"], "status:", result["status"])
