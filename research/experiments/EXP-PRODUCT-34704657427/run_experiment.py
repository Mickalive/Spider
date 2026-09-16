#!/usr/bin/env python3
"""
EXP-PRODUCT-34704657427: Compute non-empty slot_prefixes for path-prefix patterns.

Tests whether the updated distill_parameterized produces non-empty slot_prefixes
for P1/G3/G5 (path-prefix patterns) without breaking binding_accuracy=1.0 for
any established condition.

Frozen conditions: P1, G1, G2, G3, G5, N1_ORIGINAL, N1_CORRECTED, G4 (reported separately).
Baselines: B_EMPTY_SLOT_PREFIXES (parent behavior), B_UNFIXED (true unfixed heuristic).

All conditions deterministic synthetic, n=3 training + 3 unseen, zero model/network/browser calls.
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


# ─── True Unfixed Heuristic (B_UNFIXED) ────────────────────────────────────

def _unfixed_find_common_prefix_suffix(values: list[str]) -> tuple[str, str]:
    """Original heuristic: common prefix/suffix WITHOUT Fix1 suffix guard."""
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


def distill_unfixed(observations: list[Observation]) -> Mechanism | None:
    """Distill using ORIGINAL unfixed heuristic (no Fix1/Fix2)."""
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
        path_values[path] = {
            "values": values,
            "prefix": prefix,
            "suffix": suffix,
        }

    varying_paths = []
    for path, info in path_values.items():
        if _is_metadata_path(path):
            continue
        unique_vals = set(str(v) for v in info["values"])
        if len(unique_vals) > 1:
            varying_paths.append(path)

    if not varying_paths:
        return None

    # NO Fix2: all varying paths pass
    filtered_varying_paths = list(varying_paths)
    varying_paths = filtered_varying_paths

    if not varying_paths:
        return None

    # Compute slot_prefixes using unfixed rfind('/')
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

    # Build template
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
        json.dumps({
            "intent": intent,
            "action": template,
        }, sort_keys=True).encode()
    ).hexdigest()[:16]

    mechanism = Mechanism(
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
    return mechanism


# ─── Parent action_templates (frozen from EXP-PRODUCT-34685457833) ──────────
# These are the exact templates produced by the parent experiment.
# Used to verify slot_prefixes computation is metadata-only.

PARENT_TEMPLATES = {
    "P1_PATH_PREFIX": {"method": "GET", "url": "https://api.example.com/users/${url}"},
    "G1_QUERY_STRING_SIMPLE": {"method": "GET", "url": "https://api.example.com/search?q=${url}"},
    "G2_QUERY_STRING_MULTIPARAM": {"method": "GET", "url": "https://api.example.com/items?category=books&page=${url}"},
    "G3_DEEP_PATH": {"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/${url}"},
    "G4_MULTI_SLOT": {"method": "GET", "url": "https://api.example.com/users/${url}00"},
    "G5_PATH_QUERY_HYBRID": {"method": "GET", "url": "https://api.example.com/users/${url}/items?page=1"},
}


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
            "distill_diagnostics": None,
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

    # Check slot_prefixes matches expected
    slot_prefixes_match = mechanism.slot_prefixes == cond.get("expected_slot_prefixes", {})

    # Check action_template matches parent (metadata-only invariant)
    parent_template = PARENT_TEMPLATES.get(cond_id)
    template_matches_parent = (mechanism.action_template == parent_template) if parent_template else None

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
            "slot_prefixes_match": slot_prefixes_match,
            "slot_prefixes_observed": mechanism.slot_prefixes,
            "slot_prefixes_expected": cond.get("expected_slot_prefixes", {}),
            "template_matches_parent": template_matches_parent,
        },
    })

    return condition_result


def run_b_empty_slot_prefixes():
    """B_EMPTY_SLOT_PREFIXES: parent behavior — verify old code produced empty slot_prefixes.
    
    The parent used rfind('/') on the full_prefix, which for path-prefix patterns
    gives the text AFTER the last '/', which is empty when the last char is '/'.
    We verify this by computing the old way."""
    b_result = {}
    for cond_id in ["P1_PATH_PREFIX", "G3_DEEP_PATH", "G5_PATH_QUERY_HYBRID"]:
        cond = CONDITIONS[cond_id]
        observations = []
        for action in cond["training"]:
            observations.append(Observation(
                intent="test", state={}, action=action, next_state={}, success=True,
            ))
        successful = [o for o in observations if o.success]
        all_paths_per_obs = [_collect_leaf_paths(o.action) for o in successful]
        path_sets = [set(p) for p in all_paths_per_obs]
        common_paths = path_sets[0]
        for ps in path_sets[1:]:
            common_paths = common_paths & ps

        for path in sorted(common_paths):
            values = [_get_value_at_path(o.action, path) for o in successful]
            str_values = [str(v) for v in values]
            full_prefix, _ = _find_common_prefix_suffix(str_values)
            # OLD code: rfind('/') on full_prefix
            last_slash = full_prefix.rfind('/')
            if last_slash >= 0:
                old_slot_prefix = full_prefix[last_slash + 1:]
            else:
                old_slot_prefix = full_prefix
            slot_name = _field_path_to_slot_name(path)
            b_result[cond_id] = {
                "old_slot_prefix": old_slot_prefix,
                "old_is_empty": old_slot_prefix == "",
                "note": "Parent used rfind('/') on full_prefix; for path-prefix patterns the last char is '/' yielding empty",
            }
    return b_result


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
            slot_prefixes_ok = result.get("metrics", {}).get("slot_prefixes_match", False)
            passed = slot_count_ok and binding_ok and slot_prefixes_ok
        condition_pass[cond_id] = passed

    # B_EMPTY_SLOT_PREFIXES baseline
    b_empty = run_b_empty_slot_prefixes()

    # ─── Frozen Decision Rule ──────────────────────────────────────────────
    # From spec.json decision_rule: ALL of 8 must pass
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

    all_eight_pass = all([
        p1_passes, g1_passes, g2_passes, g3_passes, g5_passes,
        n1_original_passes, n1_corrected_passes, pipeline_no_errors,
    ])

    # Check slot_prefixes non-empty for path-prefix patterns
    p1_slot_prefixes = all_results.get("P1_PATH_PREFIX", {}).get("slot_prefixes", {})
    g3_slot_prefixes = all_results.get("G3_DEEP_PATH", {}).get("slot_prefixes", {})
    g5_slot_prefixes = all_results.get("G5_PATH_QUERY_HYBRID", {}).get("slot_prefixes", {})

    p1_non_empty = p1_slot_prefixes.get("url", "") != ""
    g3_non_empty = g3_slot_prefixes.get("url", "") != ""
    g5_non_empty = g5_slot_prefixes.get("url", "") != ""
    all_path_prefix_non_empty = p1_non_empty and g3_non_empty and g5_non_empty

    # Frozen verdict rules
    if all_eight_pass and all_path_prefix_non_empty:
        verdict = "SURVIVES_CURRENT_TEST"
    elif all_eight_pass and not all_path_prefix_non_empty:
        # Binding works but slot_prefixes still empty for path-prefix patterns
        verdict = "MIXED"
    else:
        verdict = "FALSIFIED-IN-SETTING"

    # G4 separate reporting
    g4_result = all_results.get("G4_MULTI_SLOT", {})
    g4_slot_count = g4_result.get("slot_count", 0)
    g4_binding_accuracy = g4_result.get("metrics", {}).get("binding_accuracy", 0.0)

    # Aggregate metrics
    total_conditions = len(CONDITIONS)
    passed_conditions = sum(1 for v in condition_pass.values() if v)
    condition_pass_rate = passed_conditions / total_conditions

    binding_accuracies = []
    for cond_id, result in all_results.items():
        if result.get("distill_success") and result.get("resolution_results"):
            binding_accuracies.append(result["metrics"]["binding_accuracy"])
    overall_binding_accuracy = sum(binding_accuracies) / len(binding_accuracies) if binding_accuracies else 0.0

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
            "G1_QUERY_STRING_SIMPLE": {
                "type": "fix1_target",
                "expected": "slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'search?q='}",
                "passed": condition_pass["G1_QUERY_STRING_SIMPLE"],
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
        "slot_prefixes_non_empty": {
            "P1": p1_non_empty,
            "G3": g3_non_empty,
            "G5": g5_non_empty,
            "all_path_prefix_non_empty": all_path_prefix_non_empty,
            "P1_observed": p1_slot_prefixes,
            "G3_observed": g3_slot_prefixes,
            "G5_observed": g5_slot_prefixes,
        },
        "g4_separate": {
            "slot_count": g4_slot_count,
            "binding_accuracy": g4_binding_accuracy,
            "architectural_bound": True,
            "note": "G4 reported separately per prereg; not part of frozen decision_rule",
        },
        "b_empty_slot_prefixes": b_empty,
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
            "all_path_prefix_non_empty": all_path_prefix_non_empty,
            "verdict": verdict,
        },
        "metadata_only_check": {
            cond_id: {
                "template_matches_parent": all_results[cond_id].get("metrics", {}).get("template_matches_parent"),
                "parent_template": PARENT_TEMPLATES.get(cond_id),
                "observed_template": all_results[cond_id].get("action_template"),
            }
            for cond_id in PARENT_TEMPLATES
            if cond_id in all_results
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
    print(f"Overall binding accuracy: {overall_binding_accuracy:.3f}")
    print(f"P1 (positive control): {'PASS' if p1_passes else 'FAIL'} slot_prefixes={p1_slot_prefixes}")
    print(f"G1 (fix1 target): {'PASS' if g1_passes else 'FAIL'}")
    print(f"G2 (regression): {'PASS' if g2_passes else 'FAIL'}")
    print(f"G3 (deep path): {'PASS' if g3_passes else 'FAIL'} slot_prefixes={g3_slot_prefixes}")
    print(f"G5 (path+query hybrid): {'PASS' if g5_passes else 'FAIL'} slot_prefixes={g5_slot_prefixes}")
    print(f"N1_ORIGINAL (fix2 target): {'PASS' if n1_original_passes else 'FAIL'}")
    print(f"N1_CORRECTED (null control): {'PASS' if n1_corrected_passes else 'FAIL'}")
    print(f"G4 (architectural): slot_count={g4_slot_count}, binding={g4_binding_accuracy}")
    print(f"slot_prefixes non-empty for path-prefix: P1={p1_non_empty} G3={g3_non_empty} G5={g5_non_empty}")

    return raw_evidence


if __name__ == "__main__":
    main()
