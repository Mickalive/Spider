"""Emit provenance.json for EXP-PRODUCT-36293260887 with recomputed digests.

Every digest here is computed at write time. Nothing is hand-typed, and no
placeholder or null stands in for a value that can actually be obtained.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EXP = Path(__file__).resolve().parent
REPO = EXP.parents[2]
RAW = EXP / "raw_evidence"


def sha(rel: str) -> str:
    return hashlib.sha256((REPO / rel).read_bytes()).hexdigest()


def git(*a):
    return subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True).stdout.strip()


FREEZE = json.loads((EXP / "freeze.json").read_text())
DERIVED = json.loads((RAW / "derived.json").read_text())

E = "research/experiments/EXP-PRODUCT-36293260887/"
S = "research/experiments/EXP-PRODUCT-36272385776/substrate.py"

frozen_inputs = [
    {"path": E + n, "frozen_sha256": h, "recomputed_sha256": sha(E + n),
     "verifies": sha(E + n) == h, "mutated_by_this_stage": False}
    for n, h in FREEZE["hashes"].items()
]

code = [
    {"path": "src/spider/kernel.py", "sha256": sha("src/spider/kernel.py"),
     "committed": False, "role": "implementation",
     "change": "Added align_parameters, _build_action_template, _strip_common_prefix; distill_parameterized now calls them, performs segment-granular prefix preservation, resolves intent-namespace aliases, derives confidence from evidence, and supports induce_identity_slots and force_resolve.",
     "in_base_sha_range": bool(git("diff", FREEZE.get("base_sha", "244dd5bdfe5d34bcf74f4d8472db3caa0922b641") + "..HEAD", "--", "src/spider/kernel.py"))},
    {"path": "src/spider/models.py", "sha256": sha("src/spider/models.py"),
     "committed": False, "role": "implementation",
     "change": "Added Mechanism.intent_namespace_map.", "in_base_sha_range": False},
    {"path": "tests/test_kernel.py", "sha256": sha("tests/test_kernel.py"),
     "committed": False, "role": "verification",
     "change": "3 pre-existing tests retained; added T1-T5, a segment-granularity test and an under-determined abstention test. All mechanism tests reach EXECUTABLE through distill_parameterized rather than a hand-built Mechanism.",
     "in_base_sha_range": False},
]

support = [
    {"path": E + "run_experiment.py", "sha256": sha(E + "run_experiment.py"), "role": "measurement_harness"},
    {"path": E + "probe_substrate.py", "sha256": sha(E + "probe_substrate.py"), "role": "measurement_harness"},
    {"path": E + "build_result.py", "sha256": sha(E + "build_result.py"), "role": "packet_builder"},
    {"path": S, "sha256": sha(S), "role": "fixture", "reused_unchanged": True,
     "note": "Frozen substrate. Digest matches prereg.md section 7."},
]

raw = [
    {"path": E + "raw_evidence/substrate_surface_probe.json",
     "sha256": sha(E + "raw_evidence/substrate_surface_probe.json"), "kind": "observation",
     "description": "Empirical probe of the declared and actual substrate surface."},
    {"path": E + "raw_evidence/observations.jsonl", "sha256": sha(E + "raw_evidence/observations.jsonl"),
     "kind": "observation", "records": 150, "description": "Induced resource-A observations, 50 per intent family, over 50 distinct training identifiers."},
    {"path": E + "raw_evidence/task_results.jsonl", "sha256": sha(E + "raw_evidence/task_results.jsonl"),
     "kind": "observation", "records": 1158, "description": "Per-task raw rows across 9 arms."},
    {"path": E + "raw_evidence/probe_results.jsonl", "sha256": sha(E + "raw_evidence/probe_results.jsonl"),
     "kind": "observation", "records": 180, "description": "Negative probes, 60 per arm over 3 arms."},
    {"path": E + "raw_evidence/mechanisms.json", "sha256": sha(E + "raw_evidence/mechanisms.json"),
     "kind": "observation", "description": "Mechanisms emitted by each induction call, with templates and confidences."},
    {"path": E + "raw_evidence/derived.json", "sha256": sha(E + "raw_evidence/derived.json"),
     "kind": "derived_measurement", "description": "Family-stratified B=5000 bootstrap intervals, cost ratios, break-even and n_max, computed from the raw evidence above."},
    {"path": E + "result.json", "sha256": sha(E + "result.json"), "kind": "packet_output",
     "description": "Stage output. Generated before this file, so its digest is recorded here for audit."},
    {"path": E + "report.md", "sha256": sha(E + "report.md"), "kind": "packet_output"},
]

prov = {
    "schema_version": 1,
    "experiment_id": "EXP-PRODUCT-36293260887",
    "lane": "product",
    "stage": "execute",
    "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "status": "MEASUREMENT_INVALID",
    "outcome": "MIXED",

    "git_state": {
        "head_sha": git("rev-parse", "HEAD"),
        "frozen_base_sha": "244dd5bdfe5d34bcf74f4d8472db3caa0922b641",
        "base_range": "244dd5bdfe5d34bcf74f4d8472db3caa0922b641..536e2565f30bedf7f308a62fb08143d65bf24e46",
        "committed_changes_to_src_or_tests_in_base_range": 0,
        "verification": "git diff 244dd5bd..HEAD -- src/ tests/ is empty",
        "working_tree_changes_uncommitted": True,
        "git_actions_taken_by_this_lane": "none; no add, commit, push, checkout, switch, reset or restore was executed",
        "durable_artifact_verified": False,
        "durable_artifact_note": "The mandate's central DURABLE requirement is unmet. The corrected kernel exists in the working tree only. This lane has no authorized commit mechanism, so the precondition could not be satisfied at any stage of this experiment.",
    },

    "frozen_inputs": frozen_inputs,
    "frozen_inputs_all_verify": all(f["verifies"] for f in frozen_inputs),

    "code_artifacts": code,
    "support_artifacts": support,
    "evidence_artifacts": raw,

    "environment": {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "network": "none; stdlib http.client against a local in-process HTTP substrate",
        "model_calls": 0,
        "model_tokens": 0,
        "embedding_service": "unavailable; B-RETRIEVAL-K5 substituted a deterministic hashed character-n-gram bag",
        "api_key_present": False,
        "third_party_packages_used": [],
        "seed": 42,
        "seeds_control": ["label permutation", "probe selection", "bootstrap resampling"],
    },

    "test_evidence": {
        "command": "PYTHONPATH=src python3 -m unittest discover -s tests",
        "result": "OK",
        "tests_run": 10,
        "failures": 0,
        "errors": 0,
        "preregistered_tests": {"T1": "pass", "T2": "pass", "T3": "pass", "T4": "pass", "T5": "pass"},
        "note": "Run at execute against the uncommitted working tree. T1, T2 and T4 are assertion-inverted by the frozen substrate's actual surface: T1 pins /api/v1/items/${id} which serves 404, and T4 expects an index with no collection candidates, which does not exist here. The tests are recorded as passing on the assertions as written and this conflict is recorded in result.json validity_notes rather than resolved by weakening a test.",
    },

    "measurement_transaction": {
        "http_requests_total": DERIVED["http_requests_total"],
        "reauth_requests_total": DERIVED["reauths_total"],
        "induction_cost_total": DERIVED["induction_cost_total"],
        "cost_basis": "counted real HTTP requests observed at the client",
        "task_rows": 1158,
        "probe_rows": 180,
        "arms": 9,
        "substrate_state_reset_between_arms": True,
    },

    "protocol_amendments": [
        {"id": "A1", "trigger": "TOKEN_EXPIRY=100 with no issuance endpoint",
         "amendment": "A 401 clears the request budget instead of re-issuing a token, and the re-authentication is charged as one real HTTP request.",
         "disclosed_before_inspecting_outcomes": True},
        {"id": "A2", "trigger": "null-arm success was spuriously 1.0 because the runner supplied the task family's verb instead of the resolved mechanism's verb",
         "amendment": "Mechanism arms execute the verb carried in the resolved action_template.",
         "disclosed_before_inspecting_outcomes": False,
         "integrity_note": "This defect inflated the null arm to a false pass. It was found during execution and corrected; the reported NC-SHUFFLED-INTENT-FORCED success of 0.3333 is trustworthy only because of that correction."},
    ],

    "frozen_design_defects_found": [
        {"clause": "F2", "defect": "requires /api/v1/<collection>/<slot> on a substrate with no /api/v1 prefix; also contradicts T1 which pins the collection"},
        {"clause": "F6", "defect": "N_MAX and break-even are the same algebraic expression; the clause is an identity and cannot fire"},
        {"clause": "F9", "defect": "requires the null arm's cost ratio to be >= 1.0, penalising correct abstention at zero requests"},
        {"clause": "decision_rule.5", "defect": "requires matched end-to-end success against two baselines whose measured success is 0.0, so the comparison has no referent"},
        {"clause": "F12", "defect": "requires n >= 50 per family for all arms; the frozen substrate supplies only 126 resource-B identifiers"},
        {"clause": "prereg.5", "defect": "orders kernel fixes to be committed before freeze, but check_scope.py:124-126 gives stage 'design' only 4 exact exp paths and freeze_experiment.py:79-82 writes only 3 hashes (request.json, spec.json, prereg.md), so a code-bound precondition is unsatisfiable in every lane"},
        {"clause": "prereg.8.4", "defect": "requires N_MAX frozen pre-experiment; absent from spec.json and freeze.json"},
    ],
    "program_level_recurrence": {
        "finding": "A prereg that requires a committed or hash-verified code artifact before freeze is unsatisfiable in every lane, because scripts/freeze_experiment.py:79-82 binds only request.json, spec.json and prereg.md, and scripts/check_scope.py:124-126 withholds code-writing permission until the execute stage.",
        "verified_at_source_by_this_lane": True,
        "prior_occurrences_in_codex": ["EXP-GRAPH-36287167610", "EXP-INTEL-36293264917"],
        "note": "This lane reached the same defect independently through prereg section 5, a different clause from the graph lane's V9. It is recorded as a program-level control-plane defect rather than as a defect unique to this experiment.",
    },

    "reproduction": {
        "order": [
            "python3 research/experiments/EXP-PRODUCT-36293260887/probe_substrate.py",
            "PYTHONPATH=src python3 -m unittest discover -s tests",
            "python3 research/experiments/EXP-PRODUCT-36293260887/run_experiment.py",
            "python3 research/experiments/EXP-PRODUCT-36293260887/build_result.py",
            "python3 research/experiments/EXP-PRODUCT-36293260887/build_provenance.py",
        ],
        "deterministic": True,
        "caveat": "The substrate contains no RNG, so the measurement itself is deterministic given the fixed seed. The 'deterministic' flag attests only to the absence of unseeded randomness, not to stability across Python versions.",
    },

    "integrity_statement": {
        "frozen_inputs_mutated": False,
        "codex_mutated": False,
        "other_lanes_or_experiments_touched": False,
        "constitutional_files_touched": False,
        "github_workflows_touched": False,
        "placeholders_in_packet": False,
        "claim_self_promotion": False,
        "self_reference_note": "build_provenance.py cannot record its own digest, because writing the digest changes the file. Its digest is therefore absent from this packet by construction rather than by omission; it can be recomputed directly from the working tree.",
        "note": "The only modified paths are the product lane's authorized roots (src, tests) and this experiment's own directory. Everything in src/ and tests/ is uncommitted, which is disclosed above as a validity failure rather than presented as a delivered capability.",
    },
}

(EXP / "provenance.json").write_text(json.dumps(prov, indent=2) + "\n")
print("wrote provenance.json")
print("frozen inputs all verify:", prov["frozen_inputs_all_verify"])
print("durable artifact verified:", prov["git_state"]["durable_artifact_verified"])
print("digests computed:", len(code) + len(support) + len(raw) + len(frozen_inputs))
