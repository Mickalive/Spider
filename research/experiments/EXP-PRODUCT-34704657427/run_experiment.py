#!/usr/bin/env python3
"""
EXP-PRODUCT-34704657427: Test slot_prefixes computation.

Tests whether slot_prefixes are computed non-empty for path-prefix patterns
(P1/G3/G5) while maintaining binding_accuracy=1.0 for all established conditions.

Frozen inputs: 7 conditions from parent EXP-PRODUCT-34685457833 run_experiment.py.
Code: distill_parameterized from committed kernel.py (no monkey-patching).
"""

import copy
import hashlib
import importlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# ─── Ensure src/spider is importable ────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

# Import committed kernel module (no monkey-patching)
import src.spider.kernel as kernel_mod
from src.spider.kernel import (
    SpiderKernel, _PARAMETER, _matches, _template_slots, _bind,
    distill_parameterized, _find_common_prefix_suffix, _validate_prefix_boundary,
    _collect_leaf_paths, _get_value_at_path, _set_template_value,
    _compute_jaccard, _compute_structure_similarity,
    _check_constant_value_anchor, _field_path_to_slot_name, _is_metadata_path,
)
from src.spider.models import Mechanism, Observation, Resolution, ResolutionStatus
from src.spider.registry import MechanismRegistry


# ─── Test Conditions (frozen spec) ─────────────────────────────────────────

CONDITIONS = {
    "P1_PATH_PREFIX": {
        "type": "positive_control",
        "training": [
            {"method": "GET", "url": "https://api.example.com/users/A"},
            {"method": "GET", "url": "https://api.example.com/users/B"},
            {"method": "GET", "url": "https://api.example.com/users/C"},
        ],
        "unseen_values": [{"url": "D"}, {"url": "E"}, {"url": "F"}],
        "expected_slot_count": 1,
        "expected_slot_prefixes": {"url": "users/"},
        "expected_urls": [
            "https://api.example.com/users/D",
            "https://api.example.com/users/E",
            "https://api.example.com/users/F",
        ],
    },
    "G1_QUERY_STRING_SIMPLE": {
        "type": "fix1_target",
        "training": [
            {"method": "GET", "url": "https://api.example.com/search?q=alpha"},
            {"method": "GET", "url": "https://api.example.com/search?q=beta"},
            {"method": "GET", "url": "https://api.example.com/search?q=delta"},
        ],
        "unseen_values": [{"url": "gamma"}, {"url": "epsilon"}, {"url": "zeta"}],
        "expected_slot_count": 1,
        "expected_slot_prefixes": {"url": "search?q="},
        "expected_urls": [
            "https://api.example.com/search?q=gamma",
            "https://api.example.com/search?q=epsilon",
            "https://api.example.com/search?q=zeta",
        ],
    },
    "G2_QUERY_STRING_MULTIPARAM": {
        "type": "regression",
        "training": [
            {"method": "GET", "url": "https://api.example.com/items?category=books&page=1"},
            {"method": "GET", "url": "https://api.example.com/items?category=books&page=2"},
            {"method": "GET", "url": "https://api.example.com/items?category=books&page=3"},
        ],
        "unseen_values": [{"url": "4"}, {"url": "5"}, {"url": "6"}],
        "expected_slot_count": 1,
        "expected_slot_prefixes": {"url": "items?category=books&page="},
        "expected_urls": [
            "https://api.example.com/items?category=books&page=4",
            "https://api.example.com/items?category=books&page=5",
            "https://api.example.com/items?category=books&page=6",
        ],
    },
    "G3_DEEP_PATH": {
        "type": "regression",
        "training": [
            {"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/1"},
            {"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/2"},
            {"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/3"},
        ],
        "unseen_values": [{"url": "4"}, {"url": "5"}, {"url": "6"}],
        "expected_slot_count": 1,
        "expected_slot_prefixes": {"url": "repos/main/issues/"},
        "expected_urls": [
            "https://api.example.com/orgs/acme/repos/main/issues/4",
            "https://api.example.com/orgs/acme/repos/main/issues/5",
            "https://api.example.com/orgs/acme/repos/main/issues/6",
        ],
    },
    "G5_PATH_QUERY_HYBRID": {
        "type": "regression",
        "training": [
            {"method": "GET", "url": "https://api.example.com/users/alice/items?page=1"},
            {"method": "GET", "url": "https://api.example.com/users/bob/items?page=1"},
            {"method": "GET", "url": "https://api.example.com/users/charlie/items?page=1"},
        ],
        "unseen_values": [{"url": "dave"}, {"url": "eve"}, {"url": "frank"}],
        "expected_slot_count": 1,
        "expected_slot_prefixes": {"url": "users/"},
        "expected_urls": [
            "https://api.example.com/users/dave/items?page=1",
            "https://api.example.com/users/eve/items?page=1",
            "https://api.example.com/users/frank/items?page=1",
        ],
    },
    "N1_ORIGINAL": {
        "type": "fix2_target",
        "training": [
            {"method": "GET", "url": "https://api.example.com/a"},
            {"method": "GET", "url": "https://api.other.com/b"},
            {"method": "GET", "url": "https://api.third.com/c"},
        ],
        "unseen_values": [{"url": "x"}, {"url": "y"}, {"url": "z"}],
        "expected_slot_count": 0,
        "expected_slot_prefixes": {},
        "expected_urls": None,
    },
    "N1_CORRECTED": {
        "type": "null_control_corrected",
        "training": [
            {"method": "GET", "url": "http://a.com/x"},
            {"method": "GET", "url": "ftp://b.org/y"},
            {"method": "GET", "url": "custom://c.net/z"},
        ],
        "unseen_values": [{"url": "x2"}, {"url": "y2"}, {"url": "z2"}],
        "expected_slot_count": 0,
        "expected_slot_prefixes": {},
        "expected_urls": None,
    },
}


# ─── Run conditions ────────────────────────────────────────────────────────

def run_condition(cond_id: str, cond: dict) -> dict:
    """Run a single test condition against committed kernel.py."""
    observations = []
    for action in cond["training"]:
        observations.append(Observation(
            intent="test",
            state={},
            action=action,
            next_state={},
            success=True,
        ))

    # Regular condition: use committed distill_parameterized (no monkey-patching)
    result = distill_parameterized(None, observations)

    condition_result = {
        "condition_id": cond_id,
        "training_count": len(cond["training"]),
        "unseen_count": len(cond["unseen_values"]),
    }

    if result is None:
        condition_result.update({
            "distill_success": False,
            "mechanism_id": None,
            "action_template": None,
            "parameter_slots": [],
            "slot_count": 0,
            "confidence": 0,
            "slot_prefixes": {},
            "resolution_results": [],
            "metrics": {
                "binding_accuracy": 1.0 if cond["expected_slot_count"] == 0 else 0.0,
                "slot_count_correct": cond["expected_slot_count"] == 0,
            },
        })
        return condition_result

    mechanism = result

    # Test binding with unseen values
    resolution_results = []
    for i, unseen in enumerate(cond["unseen_values"]):
        try:
            bound = _bind(mechanism.action_template, unseen)
            binding_correct = False
            if cond["expected_urls"]:
                expected_url = cond["expected_urls"][i]
                binding_correct = bound["url"] == expected_url
            resolution_results.append({
                "params": unseen,
                "bound_action": bound,
                "status": "EXECUTABLE",
                "binding_correct": binding_correct,
                "expected_url": cond["expected_urls"][i] if cond["expected_urls"] else None,
            })
        except Exception as e:
            resolution_results.append({
                "params": unseen,
                "bound_action": None,
                "status": f"ERROR: {e}",
                "binding_correct": False,
                "expected_url": cond["expected_urls"][i] if cond["expected_urls"] else None,
            })

    binding_correct_count = sum(1 for r in resolution_results if r["binding_correct"])
    binding_accuracy = binding_correct_count / len(cond["unseen_values"]) if cond["unseen_values"] else 1.0

    condition_result.update({
        "distill_success": True,
        "mechanism_id": mechanism.mechanism_id,
        "action_template": mechanism.action_template,
        "parameter_slots": mechanism.parameter_slots,
        "slot_count": len(mechanism.parameter_slots),
        "confidence": mechanism.confidence,
        "slot_prefixes": mechanism.slot_prefixes,
        "resolution_results": resolution_results,
        "metrics": {
            "binding_accuracy": binding_accuracy,
            "binding_correct_count": binding_correct_count,
            "executable_count": sum(1 for r in resolution_results if r["status"] == "EXECUTABLE"),
            "slot_count_correct": len(mechanism.parameter_slots) == cond["expected_slot_count"],
        },
    })

    return condition_result


def main():
    """Run all conditions and produce raw evidence."""
    all_results = {}
    condition_pass = {}

    for cond_id, cond in CONDITIONS.items():
        result = run_condition(cond_id, cond)
        all_results[cond_id] = result

        # Determine pass/fail per frozen decision rule
        slot_count_ok = result.get("metrics", {}).get("slot_count_correct", False)
        if cond["expected_slot_count"] == 0:
            passed = slot_count_ok
        else:
            binding_ok = result.get("metrics", {}).get("binding_accuracy", 0.0) == 1.0
            passed = slot_count_ok and binding_ok
        condition_pass[cond_id] = passed

    # Aggregate metrics
    total_conditions = len(CONDITIONS)
    passed_conditions = sum(1 for v in condition_pass.values() if v)
    condition_pass_rate = passed_conditions / total_conditions

    # Overall binding accuracy (for conditions with parameterization)
    binding_accuracies = []
    for cond_id, result in all_results.items():
        if result.get("distill_success") and result.get("resolution_results"):
            binding_accuracies.append(result["metrics"]["binding_accuracy"])
    overall_binding_accuracy = sum(binding_accuracies) / len(binding_accuracies) if binding_accuracies else 0.0

    # Decision per frozen spec.json decision_rule
    p1_passes = condition_pass.get("P1_PATH_PREFIX", False)
    g1_passes = condition_pass.get("G1_QUERY_STRING_SIMPLE", False)
    g2_passes = condition_pass.get("G2_QUERY_STRING_MULTIPARAM", False)
    g3_passes = condition_pass.get("G3_DEEP_PATH", False)
    g5_passes = condition_pass.get("G5_PATH_QUERY_HYBRID", False)
    n1_original_passes = condition_pass.get("N1_ORIGINAL", False)
    n1_corrected_passes = condition_pass.get("N1_CORRECTED", False)

    pipeline_no_errors = all(
        result.get("metrics", {}).get("binding_accuracy") is not None
        for result in all_results.values()
    )

    # Frozen decision rule: ALL 8 must pass
    all_eight_pass = all([
        p1_passes, g1_passes, g2_passes, g3_passes, g5_passes,
        n1_original_passes, n1_corrected_passes, pipeline_no_errors,
    ])

    if all_eight_pass:
        verdict = "SURVIVES_CURRENT_TEST"
    elif (g1_passes or n1_original_passes) and not all([
        p1_passes, g2_passes, g3_passes, g5_passes
    ]):
        verdict = "MIXED"
    else:
        verdict = "FALSIFIED-IN-SETTING"

    # slot_prefixes non-empty check (new for this experiment)
    p1_slot_prefixes = all_results.get("P1_PATH_PREFIX", {}).get("slot_prefixes", {})
    g3_slot_prefixes = all_results.get("G3_DEEP_PATH", {}).get("slot_prefixes", {})
    g5_slot_prefixes = all_results.get("G5_PATH_QUERY_HYBRID", {}).get("slot_prefixes", {})

    p1_prefixes_non_empty = p1_slot_prefixes.get("url", "") != ""
    g3_prefixes_non_empty = g3_slot_prefixes.get("url", "") != ""
    g5_prefixes_non_empty = g5_slot_prefixes.get("url", "") != ""
    all_path_prefixes_non_empty = p1_prefixes_non_empty and g3_prefixes_non_empty and g5_prefixes_non_empty

    # slot_prefixes match expected values
    p1_prefixes_match = p1_slot_prefixes == CONDITIONS["P1_PATH_PREFIX"]["expected_slot_prefixes"]
    g1_prefixes_match = all_results.get("G1_QUERY_STRING_SIMPLE", {}).get("slot_prefixes", {}) == CONDITIONS["G1_QUERY_STRING_SIMPLE"]["expected_slot_prefixes"]
    g2_prefixes_match = all_results.get("G2_QUERY_STRING_MULTIPARAM", {}).get("slot_prefixes", {}) == CONDITIONS["G2_QUERY_STRING_MULTIPARAM"]["expected_slot_prefixes"]
    g3_prefixes_match = g3_slot_prefixes == CONDITIONS["G3_DEEP_PATH"]["expected_slot_prefixes"]
    g5_prefixes_match = g5_slot_prefixes == CONDITIONS["G5_PATH_QUERY_HYBRID"]["expected_slot_prefixes"]

    raw_evidence = {
        "experiment_id": "EXP-PRODUCT-34704657427",
        "conditions": all_results,
        "controls": {
            "P1_PATH_PREFIX": {
                "type": "positive_control",
                "expected": "slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'users/'}",
                "passed": condition_pass.get("P1_PATH_PREFIX", False),
            },
            "N1_ORIGINAL": {
                "type": "fix2_target",
                "expected": "slot_count=0",
                "passed": condition_pass.get("N1_ORIGINAL", False),
            },
            "N1_CORRECTED": {
                "type": "null_control_corrected",
                "expected": "slot_count=0",
                "passed": condition_pass.get("N1_CORRECTED", False),
            },
        },
        "aggregate": {
            "total_conditions": total_conditions,
            "passed_conditions": passed_conditions,
            "condition_pass_rate": condition_pass_rate,
            "overall_binding_accuracy": overall_binding_accuracy,
            "verdict": verdict,
        },
        "condition_pass": condition_pass,
        "slot_prefixes_analysis": {
            "path_prefix_non_empty": {
                "p1": {"observed": p1_slot_prefixes, "non_empty": p1_prefixes_non_empty, "matches_expected": p1_prefixes_match, "expected": CONDITIONS["P1_PATH_PREFIX"]["expected_slot_prefixes"]},
                "g3": {"observed": g3_slot_prefixes, "non_empty": g3_prefixes_non_empty, "matches_expected": g3_prefixes_match, "expected": CONDITIONS["G3_DEEP_PATH"]["expected_slot_prefixes"]},
                "g5": {"observed": g5_slot_prefixes, "non_empty": g5_prefixes_non_empty, "matches_expected": g5_prefixes_match, "expected": CONDITIONS["G5_PATH_QUERY_HYBRID"]["expected_slot_prefixes"]},
                "all_non_empty": all_path_prefixes_non_empty,
            },
            "query_string_correctness": {
                "g1": {"observed": all_results.get("G1_QUERY_STRING_SIMPLE", {}).get("slot_prefixes", {}), "matches_expected": g1_prefixes_match, "expected": CONDITIONS["G1_QUERY_STRING_SIMPLE"]["expected_slot_prefixes"]},
                "g2": {"observed": all_results.get("G2_QUERY_STRING_MULTIPARAM", {}).get("slot_prefixes", {}), "matches_expected": g2_prefixes_match, "expected": CONDITIONS["G2_QUERY_STRING_MULTIPARAM"]["expected_slot_prefixes"]},
            },
        },
        "decision_rule_evaluation": {
            "p1_passes": p1_passes,
            "g1_passes": g1_passes,
            "g2_passes": g2_passes,
            "g3_passes": g3_passes,
            "g5_passes": g5_passes,
            "n1_original_passes": n1_original_passes,
            "n1_corrected_passes": n1_corrected_passes,
            "pipeline_no_errors": pipeline_no_errors,
            "all_eight_pass": all_eight_pass,
            "verdict": verdict,
        },
        "slot_prefixes_metadata_only": {
            "action_template_unchanged": True,  # Will verify below
            "note": "slot_prefixes is metadata-only; action_template and _bind behavior must be identical to parent",
        },
    }

    # Verify action_template unchanged (compare with parent expected templates)
    parent_templates = {
        "P1_PATH_PREFIX": {"method": "GET", "url": "https://api.example.com/users/${url}"},
        "G1_QUERY_STRING_SIMPLE": {"method": "GET", "url": "https://api.example.com/search?q=${url}"},
        "G2_QUERY_STRING_MULTIPARAM": {"method": "GET", "url": "https://api.example.com/items?category=books&page=${url}"},
        "G3_DEEP_PATH": {"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/${url}"},
        "G5_PATH_QUERY_HYBRID": {"method": "GET", "url": "https://api.example.com/users/${url}/items?page=1"},
    }
    template_match = {}
    for cond_id, expected_template in parent_templates.items():
        observed_template = all_results.get(cond_id, {}).get("action_template")
        match = observed_template == expected_template
        template_match[cond_id] = {"observed": observed_template, "expected": expected_template, "match": match}
        if not match:
            raw_evidence["slot_prefixes_metadata_only"]["action_template_unchanged"] = False

    raw_evidence["slot_prefixes_metadata_only"]["template_verification"] = template_match

    # Compute SHA256 of run_experiment.py
    import hashlib
    script_path = Path(__file__).resolve()
    script_hash = hashlib.sha256(script_path.read_bytes()).hexdigest()

    # Compute SHA256 of kernel.py
    kernel_path = REPO_ROOT / "src" / "spider" / "kernel.py"
    kernel_hash = hashlib.sha256(kernel_path.read_bytes()).hexdigest()

    # Compute SHA256 of models.py
    models_path = REPO_ROOT / "src" / "spider" / "models.py"
    models_hash = hashlib.sha256(models_path.read_bytes()).hexdigest()

    raw_evidence["provenance"] = {
        "script_hash": script_hash,
        "kernel_hash": kernel_hash,
        "models_hash": models_hash,
        "substrate": "committed code (no monkey-patching)",
        "environment": {
            "model_network_browser_calls": 0,
            "deterministic_synthetic": True,
            "n_training_per_condition": 3,
            "n_unseen_per_condition": 3,
        },
    }

    output_path = Path(__file__).parent / "raw_evidence.json"
    with open(output_path, "w") as f:
        json.dump(raw_evidence, f, indent=2)

    print(f"Experiment complete: {passed_conditions}/{total_conditions} conditions passed")
    print(f"Verdict: {verdict}")
    print(f"Overall binding accuracy: {overall_binding_accuracy:.3f}")
    print(f"P1 slot_prefixes: {p1_slot_prefixes} (non-empty: {p1_prefixes_non_empty}, match: {p1_prefixes_match})")
    print(f"G3 slot_prefixes: {g3_slot_prefixes} (non-empty: {g3_prefixes_non_empty}, match: {g3_prefixes_match})")
    print(f"G5 slot_prefixes: {g5_slot_prefixes} (non-empty: {g5_prefixes_non_empty}, match: {g5_prefixes_match})")
    print(f"G1 slot_prefixes: {all_results.get('G1_QUERY_STRING_SIMPLE', {}).get('slot_prefixes', {})} (match: {g1_prefixes_match})")
    print(f"G2 slot_prefixes: {all_results.get('G2_QUERY_STRING_MULTIPARAM', {}).get('slot_prefixes', {})} (match: {g2_prefixes_match})")
    print(f"All path-prefix non-empty: {all_path_prefixes_non_empty}")
    print(f"Action templates unchanged: {raw_evidence['slot_prefixes_metadata_only']['action_template_unchanged']}")
    print(f"Raw evidence: {output_path}")

    return raw_evidence


if __name__ == "__main__":
    main()
