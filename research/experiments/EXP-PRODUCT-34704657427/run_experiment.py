#!/usr/bin/env python3
"""
EXP-PRODUCT-34704657427: Verify non-empty slot_prefixes computation.

Imports src/spider/kernel.py directly (no monkey-patching).
Runs 7 frozen conditions (5 established + 2 null controls).
Verifies slot_prefixes non-empty for P1/G3/G5 and binding_accuracy=1.0 for all established.

The current kernel.py already contains the new slot_prefixes extraction
algorithm (lines 276-314). This script tests whether it produces the
expected non-empty slot_prefixes for path-prefix patterns.
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

# Force fresh import of kernel module
import src.spider.kernel as kernel_mod
importlib.reload(kernel_mod)
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
    """Run a single test condition against current kernel.py."""
    observations = []
    for action in cond["training"]:
        observations.append(Observation(
            intent="test",
            state={},
            action=action,
            next_state={},
            success=True,
        ))

    # Use committed distill_parameterized (no monkey-patching)
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

    # Check if slot_prefixes matches expected
    slot_prefixes_match = mechanism.slot_prefixes == cond["expected_slot_prefixes"]

    condition_result.update({
        "distill_success": True,
        "mechanism_id": mechanism.mechanism_id,
        "action_template": mechanism.action_template,
        "parameter_slots": mechanism.parameter_slots,
        "slot_count": len(mechanism.parameter_slots),
        "confidence": mechanism.confidence,
        "slot_prefixes": mechanism.slot_prefixes,
        "slot_prefixes_expected": cond["expected_slot_prefixes"],
        "slot_prefixes_match": slot_prefixes_match,
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
            # For null controls: pass if no parameterization induced (slot_count=0)
            passed = slot_count_ok
        else:
            binding_ok = result.get("metrics", {}).get("binding_accuracy", 0.0) == 1.0
            slot_prefixes_ok = result.get("slot_prefixes_match", False)
            passed = slot_count_ok and binding_ok and slot_prefixes_ok
        condition_pass[cond_id] = passed

    # Aggregate metrics
    total_conditions = len(CONDITIONS)
    passed_conditions = sum(1 for v in condition_pass.values() if v)
    condition_pass_rate = passed_conditions / total_conditions

    # Structural generalization rate (G1-G5 only)
    g_conditions = [k for k in condition_pass if k.startswith("G")]
    g_passed = sum(1 for k in g_conditions if condition_pass[k])
    structural_generalization_rate = g_passed / len(g_conditions) if g_conditions else 0.0

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

    # Frozen decision rule: ALL 8 must pass (section 9.1)
    all_eight_pass = all([
        p1_passes, g1_passes, g2_passes, g3_passes, g5_passes,
        n1_original_passes, n1_corrected_passes,
        pipeline_no_errors,
    ])

    # slot_prefixes non-empty check for path-prefix conditions
    p1_slot_prefixes_nonempty = all_results.get("P1_PATH_PREFIX", {}).get("slot_prefixes", {}) != {"url": ""}
    g3_slot_prefixes_nonempty = all_results.get("G3_DEEP_PATH", {}).get("slot_prefixes", {}) != {"url": ""}
    g5_slot_prefixes_nonempty = all_results.get("G5_PATH_QUERY_HYBRID", {}).get("slot_prefixes", {}) != {"url": ""}
    slot_prefixes_computation_works = p1_slot_prefixes_nonempty and g3_slot_prefixes_nonempty and g5_slot_prefixes_nonempty

    if all_eight_pass and slot_prefixes_computation_works:
        verdict = "SURVIVES_CURRENT_TEST"
        outcome = "SUPPORTS"
    elif all_eight_pass and not slot_prefixes_computation_works:
        # Binding works but slot_prefixes still empty — same as parent
        verdict = "MIXED"
        outcome = "MIXED"
    elif not all_eight_pass:
        verdict = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
    else:
        verdict = "INCONCLUSIVE"
        outcome = "INCONCLUSIVE"

    # Raw evidence output
    raw_evidence = {
        "experiment_id": "EXP-PRODUCT-34704657427",
        "conditions": all_results,
        "controls": {
            "P1_PATH_PREFIX": {
                "type": "positive_control",
                "expected": "slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'users/'}",
                "passed": condition_pass["P1_PATH_PREFIX"],
            },
            "N1_ORIGINAL": {
                "type": "fix2_target",
                "expected": "slot_count=0",
                "passed": condition_pass["N1_ORIGINAL"],
            },
            "N1_CORRECTED": {
                "type": "null_control_corrected",
                "expected": "slot_count=0",
                "passed": condition_pass.get("N1_CORRECTED", False),
            },
            "G2_QUERY_STRING_MULTIPARAM": {
                "type": "regression",
                "expected": "slot_count=1, binding_accuracy=1.0",
                "passed": condition_pass["G2_QUERY_STRING_MULTIPARAM"],
            },
            "G3_DEEP_PATH": {
                "type": "regression",
                "expected": "slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'repos/main/issues/'}",
                "passed": condition_pass["G3_DEEP_PATH"],
            },
            "G5_PATH_QUERY_HYBRID": {
                "type": "regression",
                "expected": "slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'users/'}",
                "passed": condition_pass["G5_PATH_QUERY_HYBRID"],
            },
        },
        "aggregate": {
            "total_conditions": total_conditions,
            "passed_conditions": passed_conditions,
            "condition_pass_rate": condition_pass_rate,
            "structural_generalization_rate": structural_generalization_rate,
            "overall_binding_accuracy": overall_binding_accuracy,
            "verdict": verdict,
        },
        "condition_pass": condition_pass,
        "slot_prefixes_verification": {
            "p1_slot_prefixes": all_results.get("P1_PATH_PREFIX", {}).get("slot_prefixes", {}),
            "p1_expected": {"url": "users/"},
            "p1_nonempty": p1_slot_prefixes_nonempty,
            "g3_slot_prefixes": all_results.get("G3_DEEP_PATH", {}).get("slot_prefixes", {}),
            "g3_expected": {"url": "repos/main/issues/"},
            "g3_nonempty": g3_slot_prefixes_nonempty,
            "g5_slot_prefixes": all_results.get("G5_PATH_QUERY_HYBRID", {}).get("slot_prefixes", {}),
            "g5_expected": {"url": "users/"},
            "g5_nonempty": g5_slot_prefixes_nonempty,
            "computation_works": slot_prefixes_computation_works,
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
            "slot_prefixes_computation_works": slot_prefixes_computation_works,
            "verdict": verdict,
        },
        "fixes_inherited": {
            "fix1_suffix_guard": "Exclude single-character suffixes not preceded by structural delimiters (?, =, &)",
            "fix2_delimiter_bound_prefix": "Last-char of prefix in /?=& (validated in EXP-PRODUCT-34642376433)",
            "empty_prefix_guard": "Frozen: reject parameterization when common prefix is empty (truly disjoint URLs)",
            "slot_prefixes_extraction": "New: extract path segment between domain authority and slot position (kernel.py lines 276-314)",
        },
        "substrate": {
            "module": "src.spider.kernel",
            "approach": "committed code (no monkey-patching)",
            "mechanism_model": "slot_prefixes is a proper dataclass field in models.py",
            "bind_function": "actual kernel._bind (template substitution)",
        },
    }

    with open("raw_evidence.json", "w") as f:
        json.dump(raw_evidence, f, indent=2)

    print(f"Experiment complete: {passed_conditions}/{total_conditions} conditions passed")
    print(f"Verdict: {verdict}")
    print(f"Outcome: {outcome}")
    print(f"Overall binding accuracy: {overall_binding_accuracy:.3f}")
    print(f"Structural generalization rate: {structural_generalization_rate:.3f}")
    print(f"P1 (positive control): {'PASS' if p1_passes else 'FAIL'}")
    print(f"G1 (fix1 target): {'PASS' if g1_passes else 'FAIL'}")
    print(f"G2 (regression): {'PASS' if g2_passes else 'FAIL'}")
    print(f"G3 (regression): {'PASS' if g3_passes else 'FAIL'}")
    print(f"G5 (regression): {'PASS' if g5_passes else 'FAIL'}")
    print(f"N1_ORIGINAL (fix2 target): {'PASS' if n1_original_passes else 'FAIL'}")
    print(f"N1_CORRECTED (null control): {'PASS' if n1_corrected_passes else 'FAIL'}")
    print(f"slot_prefixes computation works: {slot_prefixes_computation_works}")
    print(f"P1 slot_prefixes: {all_results.get('P1_PATH_PREFIX', {}).get('slot_prefixes', {})}")
    print(f"G3 slot_prefixes: {all_results.get('G3_DEEP_PATH', {}).get('slot_prefixes', {})}")
    print(f"G5 slot_prefixes: {all_results.get('G5_PATH_QUERY_HYBRID', {}).get('slot_prefixes', {})}")

    return raw_evidence


if __name__ == "__main__":
    main()
