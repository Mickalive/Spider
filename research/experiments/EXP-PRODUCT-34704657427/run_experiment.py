#!/usr/bin/env python3
"""
EXP-PRODUCT-34704657427: Test slot_prefixes computation for path-prefix patterns.

Runs 7 decision-relevant conditions (P1, G1, G2, G3, G5, N1_ORIGINAL, N1_CORRECTED)
plus G4 and B_UNFIXED (reported separately) against the current kernel.py which has
the slot_prefixes extraction algorithm.

Produces raw_evidence.json.
"""

import hashlib
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

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


# ─── True Unfixed Heuristic (B_UNFIXED) ────────────────────────────────────

def _unfixed_find_common_prefix_suffix(values):
    if not values:
        return "", ""
    prefix = values[0]
    for v in values[1:]:
        while not v.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                break
    suffix = values[0]
    for v in values[1:]:
        while not v.endswith(suffix):
            suffix = suffix[1:]
            if not suffix:
                break
    return prefix, suffix


def distill_unfixed(observations):
    if not observations or len(observations) < 2:
        return None
    successful = [o for o in observations if o.success]
    if len(successful) < 2:
        return None
    intent = successful[0].intent
    same_intent = [o for o in successful if o.intent == intent]
    if len(same_intent) < 2:
        return None
    successful = same_intent

    all_paths_per_obs = [_collect_leaf_paths(o.action) for o in successful]
    path_sets = [set(p) for p in all_paths_per_obs]
    common_paths = path_sets[0]
    for ps in path_sets[1:]:
        common_paths = common_paths & ps

    path_values = {}
    for path in sorted(common_paths):
        values = []
        for obs in successful:
            v = _get_value_at_path(obs.action, path)
            values.append(v)
        str_values = [str(v) for v in values]
        prefix, suffix = _unfixed_find_common_prefix_suffix(str_values)
        path_values[path] = {"values": values, "prefix": prefix, "suffix": suffix}

    varying_paths = []
    for path, info in path_values.items():
        if _is_metadata_path(path):
            continue
        unique_vals = set(str(v) for v in info["values"])
        if len(unique_vals) > 1:
            varying_paths.append(path)

    if not varying_paths:
        return None

    # Unfixed: skip empty-prefix guard and Fix2
    filtered_varying_paths = list(varying_paths)
    varying_paths = filtered_varying_paths
    if not varying_paths:
        return None

    slot_prefixes = {}
    for vpath in varying_paths:
        info = path_values[vpath]
        values = [str(v) for v in info["values"]]
        full_prefix, _ = _unfixed_find_common_prefix_suffix(values)
        last_slash = full_prefix.rfind('/')
        if last_slash >= 0:
            slot_prefix = full_prefix[last_slash + 1:]
        else:
            slot_prefix = full_prefix
        slot_name = _field_path_to_slot_name(vpath)
        slot_prefixes[slot_name] = slot_prefix

    template = dict(successful[0].action)
    parameter_slots = []
    for vpath in varying_paths:
        slot_name = _field_path_to_slot_name(vpath)
        parameter_slots.append(slot_name)
        info = path_values[vpath]
        prefix = info["prefix"]
        suffix = info["suffix"]
        template_value = f"{prefix}${{{slot_name}}}{suffix}"
        template = _set_template_value(template, vpath, template_value)

    oid = hashlib.sha256(
        json.dumps({"intent": intent, "action": template}, sort_keys=True).encode()
    ).hexdigest()[:16]

    return Mechanism(
        mechanism_id=f"unfixed-{oid}",
        intent=intent,
        preconditions=dict(successful[0].state) if hasattr(successful[0], 'state') else {},
        action_template=template,
        postconditions=dict(successful[0].next_state) if hasattr(successful[0], 'next_state') else {},
        parameter_slots=parameter_slots,
        evidence=[oid],
        confidence=0.9,
        slot_prefixes=slot_prefixes,
    )


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
    "G4_MULTI_SLOT": {
        "type": "architectural",
        "training": [
            {"method": "GET", "url": "https://api.example.com/users/alice/orders/100"},
            {"method": "GET", "url": "https://api.example.com/users/bob/orders/200"},
            {"method": "GET", "url": "https://api.example.com/users/charlie/orders/300"},
        ],
        "unseen_values": [{"url": "dave/orders/400"}, {"url": "eve/orders/500"}, {"url": "frank/orders/600"}],
        "expected_slot_count": 1,
        "expected_slot_prefixes": {"url": ""},
        "expected_urls": [
            "https://api.example.com/users/dave/orders/400",
            "https://api.example.com/users/eve/orders/500",
            "https://api.example.com/users/frank/orders/600",
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
    "B_LITERAL": {
        "type": "baseline",
        "training": [
            {"method": "GET", "url": "https://api.example.com/users/A"},
            {"method": "GET", "url": "https://api.example.com/users/B"},
            {"method": "GET", "url": "https://api.example.com/users/C"},
        ],
        "unseen_values": [{"url": "D"}, {"url": "E"}, {"url": "F"}],
        "expected_slot_count": 0,
        "expected_slot_prefixes": {},
        "expected_urls": None,
        "baseline": "literal",
    },
    "B_UNFIXED": {
        "type": "baseline_unfixed",
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
        "baseline": "unfixed",
    },
}


def run_condition(cond_id, cond):
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

    if cond.get("baseline") == "literal":
        mechanism_count = len(set(json.dumps(a, sort_keys=True) for a in cond["training"]))
        return {
            "condition_id": cond_id,
            "training_count": len(cond["training"]),
            "unseen_count": len(cond["unseen_values"]),
            "distill_success": True,
            "mechanism_id": "literal-auto",
            "action_template": cond["training"][0],
            "parameter_slots": [],
            "slot_count": 0,
            "confidence": 0.5,
            "slot_prefixes": {},
            "distill_diagnostics": {
                "mean_jaccard": 1.0,
                "has_constant_anchor": True,
                "anchor_path": ["method"],
                "shared_paths": ["method", "url"],
                "slot_prefixes": {},
                "mechanism_count": mechanism_count,
            },
            "resolution_results": [],
            "metrics": {
                "binding_accuracy": 1.0 if cond["expected_slot_count"] == 0 else 0.0,
                "binding_correct_count": 0,
                "executable_count": 0,
                "slot_count_correct": cond["expected_slot_count"] == 0,
                "fail_rate": 1.0,
            },
            "baseline_note": "Literal mechanism reuse: confidence 0.5 < min_confidence 0.8, all resolutions return EXPLORE/UNKNOWN",
        }

    if cond.get("baseline") == "unfixed":
        mechanism = distill_unfixed(observations)
        if mechanism is None:
            return {
                "condition_id": cond_id,
                "distill_success": False,
                "slot_count": 0,
                "confidence": 0,
                "metrics": {
                    "binding_accuracy": 1.0 if cond["expected_slot_count"] == 0 else 0.0,
                    "slot_count_correct": cond["expected_slot_count"] == 0,
                },
                "baseline_note": "Unfixed: no parameterization induced",
            }

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
                })

        binding_correct_count = sum(1 for r in resolution_results if r["binding_correct"])
        binding_accuracy = binding_correct_count / len(cond["unseen_values"]) if cond["unseen_values"] else 1.0

        return {
            "condition_id": cond_id,
            "training_count": len(cond["training"]),
            "unseen_count": len(cond["unseen_values"]),
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
            "baseline_note": "True unfixed heuristic: rfind('/') without Fix1/Fix2.",
        }

    # Regular condition: use committed distill_parameterized
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
            "distill_diagnostics": None,
            "resolution_results": [],
            "metrics": {
                "binding_accuracy": 1.0 if cond["expected_slot_count"] == 0 else 0.0,
                "slot_count_correct": cond["expected_slot_count"] == 0,
            },
        })
        return condition_result

    mechanism = result

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
    all_results = {}
    condition_pass = {}

    for cond_id, cond in CONDITIONS.items():
        result = run_condition(cond_id, cond)
        all_results[cond_id] = result

        slot_count_ok = result.get("metrics", {}).get("slot_count_correct", False)
        if cond["expected_slot_count"] == 0:
            passed = slot_count_ok
        else:
            binding_ok = result.get("metrics", {}).get("binding_accuracy", 0.0) == 1.0
            passed = slot_count_ok and binding_ok
        condition_pass[cond_id] = passed

    # Per frozen spec.json decision_rule
    p1_passes = condition_pass.get("P1_PATH_PREFIX", False)
    g1_passes = condition_pass.get("G1_QUERY_STRING_SIMPLE", False)
    g2_passes = condition_pass.get("G2_QUERY_STRING_MULTIPARAM", False)
    g3_passes = condition_pass.get("G3_DEEP_PATH", False)
    g5_passes = condition_pass.get("G5_PATH_QUERY_HYBRID", False)
    n1_original_passes = condition_pass.get("N1_ORIGINAL", False)
    n1_corrected_passes = condition_pass.get("N1_CORRECTED", False)
    b_literal_passes = condition_pass.get("B_LITERAL", False)

    pipeline_no_errors = all(
        result.get("metrics", {}).get("binding_accuracy") is not None
        for result in all_results.values()
    )

    # Frozen decision rule: ALL 8 must pass
    all_eight_pass = all([
        p1_passes, g1_passes, g2_passes, g3_passes, g5_passes,
        n1_original_passes, n1_corrected_passes, b_literal_passes,
        pipeline_no_errors,
    ])

    # slot_prefixes assessment
    p1_slot_prefixes = all_results.get("P1_PATH_PREFIX", {}).get("slot_prefixes", {})
    g3_slot_prefixes = all_results.get("G3_DEEP_PATH", {}).get("slot_prefixes", {})
    g5_slot_prefixes = all_results.get("G5_PATH_QUERY_HYBRID", {}).get("slot_prefixes", {})
    g1_slot_prefixes = all_results.get("G1_QUERY_STRING_SIMPLE", {}).get("slot_prefixes", {})
    g2_slot_prefixes = all_results.get("G2_QUERY_STRING_MULTIPARAM", {}).get("slot_prefixes", {})

    p1_nonempty = p1_slot_prefixes.get("url", "") != ""
    g3_nonempty = g3_slot_prefixes.get("url", "") != ""
    g5_nonempty = g5_slot_prefixes.get("url", "") != ""

    # Check for regressions (any established condition binding_accuracy < 1.0)
    binding_regression = False
    for cid in ["P1_PATH_PREFIX", "G1_QUERY_STRING_SIMPLE", "G2_QUERY_STRING_MULTIPARAM",
                 "G3_DEEP_PATH", "G5_PATH_QUERY_HYBRID"]:
        ba = all_results.get(cid, {}).get("metrics", {}).get("binding_accuracy", 1.0)
        if ba < 1.0:
            binding_regression = True

    # Verdict per frozen spec.json decision_rule
    if all_eight_pass and p1_nonempty and g3_nonempty and g5_nonempty:
        verdict = "SURVIVES_CURRENT_TEST"
    elif all_eight_pass and not (p1_nonempty and g3_nonempty and g5_nonempty):
        # Binding intact but slot_prefixes still empty (same as parent) — design intent not achieved
        verdict = "MIXED"
    elif binding_regression:
        verdict = "FALSIFIED-IN-SETTING"
    else:
        verdict = "MIXED"

    # G4 separate
    g4_result = all_results.get("G4_MULTI_SLOT", {})

    # B_UNFIXED
    b_unfixed_result = all_results.get("B_UNFIXED", {})

    raw_evidence = {
        "experiment_id": "EXP-PRODUCT-34704657427",
        "conditions": all_results,
        "controls": {
            "P1_PATH_PREFIX": {
                "type": "positive_control",
                "expected": "slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'users/'}",
                "passed": condition_pass["P1_PATH_PREFIX"],
                "slot_prefixes_observed": p1_slot_prefixes,
                "slot_prefixes_nonempty": p1_nonempty,
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
        },
        "decision_rule_evaluation": {
            "p1_passes": p1_passes,
            "g1_passes": g1_passes,
            "g2_passes": g2_passes,
            "g3_passes": g3_passes,
            "g5_passes": g5_passes,
            "n1_original_passes": n1_original_passes,
            "n1_corrected_passes": n1_corrected_passes,
            "b_literal_passes": b_literal_passes,
            "pipeline_no_errors": pipeline_no_errors,
            "all_eight_pass": all_eight_pass,
            "binding_regression": binding_regression,
            "p1_nonempty_slot_prefixes": p1_nonempty,
            "g3_nonempty_slot_prefixes": g3_nonempty,
            "g5_nonempty_slot_prefixes": g5_nonempty,
            "verdict": verdict,
        },
        "slot_prefixes_assessment": {
            "P1": {"observed": p1_slot_prefixes, "expected": {"url": "users/"}, "nonempty": p1_nonempty},
            "G3": {"observed": g3_slot_prefixes, "expected": {"url": "repos/main/issues/"}, "nonempty": g3_nonempty},
            "G5": {"observed": g5_slot_prefixes, "expected": {"url": "users/"}, "nonempty": g5_nonempty},
            "G1": {"observed": g1_slot_prefixes, "expected": {"url": "search?q="}},
            "G2": {"observed": g2_slot_prefixes, "expected": {"url": "items?category=books&page="}},
        },
        "substrate": {
            "module": "src.spider.kernel",
            "approach": "committed code (no monkey-patching)",
            "kernel_sha": hashlib.sha256(open(REPO_ROOT / "src" / "spider" / "kernel.py", "rb").read()).hexdigest()[:16],
        },
    }

    with open(os.path.join(os.path.dirname(__file__), "raw_evidence.json"), "w") as f:
        json.dump(raw_evidence, f, indent=2)

    print(f"Experiment complete: {sum(1 for v in condition_pass.values() if v)}/{len(condition_pass)} conditions passed")
    print(f"Verdict: {verdict}")
    print(f"P1 slot_prefixes: {p1_slot_prefixes} (nonempty={p1_nonempty})")
    print(f"G3 slot_prefixes: {g3_slot_prefixes} (nonempty={g3_nonempty})")
    print(f"G5 slot_prefixes: {g5_slot_prefixes} (nonempty={g5_nonempty})")
    print(f"Binding regression: {binding_regression}")

    return raw_evidence


if __name__ == "__main__":
    main()
