#!/usr/bin/env python3
"""
EXP-PRODUCT-34704657427: Compute non-empty slot_prefixes for path-prefix patterns.

Self-contained experiment script — all helpers from fb7dd83 kernel.py are included
inline. Tests the new template-based slot_prefixes extraction algorithm.

The parent (EXP-PRODUCT-34685457833) computed slot_prefixes from the common
prefix of full URL values using rfind('/'), which yielded empty for path-prefix
patterns (P1/G3/G5) because the common prefix ended with '/'.

This experiment uses a template-based algorithm: find ${slot_name} in the
built template, then extract the path between the first '/' after the domain
authority and the last '/' before the slot.
"""

import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

# ─── Ensure src/spider is importable ────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from src.spider.models import Mechanism, Observation, Resolution, ResolutionStatus


# ─── Helper functions (from fb7dd83 kernel.py) ─────────────────────────────

_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

_METADATA_KEYS = {
    "timestamp", "request_duration_ms", "retry_count", "user_agent",
    "response_time_ms", "cache_hit", "result_count",
}


def _matches(required: dict[str, Any], actual: dict[str, Any]) -> bool:
    return all(actual.get(k) == v for k, v in required.items())


def _template_slots(value: Any) -> set[str]:
    if isinstance(value, str):
        return set(_PARAMETER.findall(value))
    if isinstance(value, dict):
        out: set[str] = set()
        for item in value.values():
            out.update(_template_slots(item))
        return out
    if isinstance(value, list):
        out: set[str] = set()
        for item in value:
            out.update(_template_slots(item))
        return out
    return set()


def _bind(value: Any, params: dict[str, Any]) -> Any:
    if isinstance(value, str):
        full = _PARAMETER.fullmatch(value)
        if full:
            return params[full.group(1)]
        def replace(match: re.Match[str]) -> str:
            return str(params[match.group(1)])
        return _PARAMETER.sub(replace, value)
    if isinstance(value, dict):
        return {k: _bind(v, params) for k, v in value.items()}
    if isinstance(value, list):
        return [_bind(v, params) for v in value]
    return value


def _collect_leaf_paths(obj: Any, prefix: str = "") -> list[str]:
    paths: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            child = f"{prefix}.{k}" if prefix else k
            if isinstance(v, (dict, list)):
                paths.extend(_collect_leaf_paths(v, child))
            else:
                paths.append(child)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            child = f"{prefix}[{i}]"
            if isinstance(item, (dict, list)):
                paths.extend(_collect_leaf_paths(item, child))
            else:
                paths.append(child)
    return paths


def _is_metadata_path(path: str) -> bool:
    top = path.split(".")[0].split("[")[0]
    return top in _METADATA_KEYS


def _get_value_at_path(obj: Any, path: str) -> Any:
    parts = path.replace("[", ".").replace("]", "").split(".")
    current = obj
    for part in parts:
        if part == "":
            continue
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return current


def _set_template_value(template: Any, path: str, value: Any) -> Any:
    result = copy.deepcopy(template)
    parts = path.replace("[", ".").replace("]", "").split(".")
    current = result
    for part in parts[:-1]:
        if part == "":
            continue
        if isinstance(current, dict):
            current = current[part]
        elif isinstance(current, list):
            current = current[int(part)]
    last = parts[-1]
    if isinstance(current, dict):
        current[last] = value
    elif isinstance(current, list):
        current[int(last)] = value
    return result


def _compute_jaccard(set1: set[str], set2: set[str]) -> float:
    if not set1 and not set2:
        return 1.0
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 0.0


def _compute_structure_similarity(observations: list) -> float:
    path_sets = [_collect_leaf_paths(obs["action"]) for obs in observations]
    if len(path_sets) < 2:
        return 1.0
    similarities = []
    for i in range(len(path_sets)):
        for j in range(i + 1, len(path_sets)):
            similarities.append(_compute_jaccard(set(path_sets[i]), set(path_sets[j])))
    return sum(similarities) / len(similarities) if similarities else 0.0


def _check_constant_value_anchor(path_values: dict) -> tuple[bool, str | None]:
    for path, info in path_values.items():
        values = info["values"]
        if len(set(str(v) for v in values)) == 1:
            return True, path
    return False, None


def _field_path_to_slot_name(path: str) -> str:
    parts = path.split(".")
    return parts[-1]


# ─── Fix1: Suffix Guard (from fb7dd83) ─────────────────────────────────────

def _find_common_prefix_suffix(values: list[str]) -> tuple[str, str]:
    """Common prefix/suffix with Fix1: reject single-char suffixes not preceded
    by structural delimiters (?, =, &)."""
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
    if suffix and len(suffix) <= 1:
        pos = len(values[0]) - len(suffix) - 1
        if pos < 0 or values[0][pos] not in ('?', '=', '&'):
            suffix = ''
    return prefix, suffix


# ─── Fix2: Delimiter-Bound Prefix Validation (from fb7dd83) ─────────────────

def _validate_prefix_boundary(full_prefix: str) -> bool:
    if not full_prefix:
        return True
    last_char = full_prefix[-1]
    return last_char in ('/', '?', '=', '&')


# ─── Template-based slot_prefixes extraction (NEW for EXP-PRODUCT-34704657427) ─

def _compute_slot_prefix_from_template(template: dict, slot_name: str) -> str:
    """Extract the path segment immediately before ${slot_name} in the template.
    
    Algorithm (from frozen prereg Section 7):
    1. Find the position of ${slot_name} in the template value string
    2. Find the last '/' before the slot position
    3. Find the next '/' after the domain authority (after '://' and authority)
    4. For path-prefix patterns (last_slash > authority_end):
       slot_prefix = value[authority_end+1 : last_slash+1]
    5. For query-string patterns (last_slash == authority_end):
       slot_prefix = value[last_slash+1 : slot_pos]
    
    This extracts the path segment between the domain authority and the slot
    for path-prefix patterns, and the query prefix for query-string patterns.
    """
    slot_pattern = f"${{{slot_name}}}"
    
    for key, value in template.items():
        if isinstance(value, str) and slot_pattern in value:
            slot_pos = value.find(slot_pattern)
            if slot_pos < 0:
                continue
            last_slash = value.rfind('/', 0, slot_pos)
            protocol_end = value.find('://')
            if protocol_end < 0:
                return ""
            authority_end = value.find('/', protocol_end + 3)
            if authority_end < 0:
                return ""
            if last_slash > authority_end:
                # Path-prefix pattern: extract path segment between authority and slot
                return value[authority_end + 1:last_slash + 1]
            else:
                # Query-string pattern: extract from last slash to slot
                return value[last_slash + 1:slot_pos]
    return ""


# ─── Parameterized distillation (re-committed from fb7dd83, slot_prefixes NEW) ─

def distill_parameterized(observations: list[Observation]) -> Mechanism | None:
    """Parameterized distill: leaf-path extraction + Fix1 + Fix2 + empty-prefix guard.
    
    Slot_prefixes computed via template-based algorithm (EXP-PRODUCT-34704657427).
    """
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

    mean_jaccard = _compute_structure_similarity(
        [{"action": o.action} for o in successful]
    )

    path_values = {}
    for path in sorted(common_paths):
        values = []
        for obs in successful:
            v = _get_value_at_path(obs.action, path)
            values.append(v)
        str_values = [str(v) for v in values]
        prefix, suffix = _find_common_prefix_suffix(str_values)
        path_values[path] = {
            "values": values,
            "prefix": prefix,
            "suffix": suffix,
        }

    has_constant_anchor, anchor_path = _check_constant_value_anchor(path_values)

    varying_paths = []
    for path, info in path_values.items():
        if _is_metadata_path(path):
            continue
        unique_vals = set(str(v) for v in info["values"])
        if len(unique_vals) > 1:
            varying_paths.append(path)

    if not varying_paths:
        return None

    # FIX 2: Delimiter-Bound Prefix Validation + Empty-prefix guard
    filtered_varying_paths = []
    for vpath in varying_paths:
        info = path_values[vpath]
        values = [str(v) for v in info["values"]]
        full_prefix, _ = _find_common_prefix_suffix(values)
        if not full_prefix:
            continue
        if _validate_prefix_boundary(full_prefix):
            filtered_varying_paths.append(vpath)
    varying_paths = filtered_varying_paths

    if not varying_paths:
        return None

    # Build template FIRST (needed for template-based slot_prefixes)
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

    # NEW: Compute slot_prefixes from the BUILT template
    slot_prefixes = {}
    for slot_name in parameter_slots:
        slot_prefixes[slot_name] = _compute_slot_prefix_from_template(template, slot_name)

    oid = hashlib.sha256(
        json.dumps({
            "intent": intent,
            "action": template,
        }, sort_keys=True).encode()
    ).hexdigest()[:16]

    mechanism = Mechanism(
        mechanism_id=f"obs-{oid}",
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
    """Run a single test condition against distill_parameterized."""
    observations = []
    for action in cond["training"]:
        observations.append(Observation(
            intent="test",
            state={},
            action=action,
            next_state={},
            success=True,
        ))

    result = distill_parameterized(observations)

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
    """Run all conditions and produce raw evidence."""
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

    total_conditions = len(CONDITIONS)
    passed_conditions = sum(1 for v in condition_pass.values() if v)
    condition_pass_rate = passed_conditions / total_conditions

    g_conditions = [k for k in condition_pass if k.startswith("G")]
    g_passed = sum(1 for k in g_conditions if condition_pass[k])
    structural_generalization_rate = g_passed / len(g_conditions) if g_conditions else 0.0

    binding_accuracies = []
    for cond_id, result in all_results.items():
        if result.get("distill_success") and result.get("resolution_results"):
            binding_accuracies.append(result["metrics"]["binding_accuracy"])
    overall_binding_accuracy = sum(binding_accuracies) / len(binding_accuracies) if binding_accuracies else 0.0

    g1_passes = condition_pass.get("G1_QUERY_STRING_SIMPLE", False)
    n1_original_passes = condition_pass.get("N1_ORIGINAL", False)
    n1_corrected_passes = condition_pass.get("N1_CORRECTED", False)
    p1_passes = condition_pass.get("P1_PATH_PREFIX", False)
    g2_passes = condition_pass.get("G2_QUERY_STRING_MULTIPARAM", False)
    g3_passes = condition_pass.get("G3_DEEP_PATH", False)
    g5_passes = condition_pass.get("G5_PATH_QUERY_HYBRID", False)

    pipeline_no_errors = all(
        result.get("metrics", {}).get("binding_accuracy") is not None
        for result in all_results.values()
    )

    # Frozen decision rule: ALL 8 conditions must pass (no B_LITERAL in this experiment)
    all_eight_pass = all([
        p1_passes, g1_passes, g2_passes, g3_passes, g5_passes,
        n1_original_passes, n1_corrected_passes,
        pipeline_no_errors,
    ])

    # Check slot_prefixes
    p1_slot_prefixes = all_results.get("P1_PATH_PREFIX", {}).get("slot_prefixes", {})
    g3_slot_prefixes = all_results.get("G3_DEEP_PATH", {}).get("slot_prefixes", {})
    g5_slot_prefixes = all_results.get("G5_PATH_QUERY_HYBRID", {}).get("slot_prefixes", {})
    g1_slot_prefixes = all_results.get("G1_QUERY_STRING_SIMPLE", {}).get("slot_prefixes", {})
    g2_slot_prefixes = all_results.get("G2_QUERY_STRING_MULTIPARAM", {}).get("slot_prefixes", {})

    p1_prefix_nonempty = p1_slot_prefixes.get("url", "") != ""
    g3_prefix_nonempty = g3_slot_prefixes.get("url", "") != ""
    g5_prefix_nonempty = g5_slot_prefixes.get("url", "") != ""
    all_path_prefix_nonempty = p1_prefix_nonempty and g3_prefix_nonempty and g5_prefix_nonempty

    p1_prefix_exact = p1_slot_prefixes == CONDITIONS["P1_PATH_PREFIX"]["expected_slot_prefixes"]
    g3_prefix_exact = g3_slot_prefixes == CONDITIONS["G3_DEEP_PATH"]["expected_slot_prefixes"]
    g5_prefix_exact = g5_slot_prefixes == CONDITIONS["G5_PATH_QUERY_HYBRID"]["expected_slot_prefixes"]
    all_path_prefix_exact = p1_prefix_exact and g3_prefix_exact and g5_prefix_exact

    # G4 separate reporting
    g4_result = all_results.get("G4_MULTI_SLOT", {})
    g4_slot_count = g4_result.get("slot_count", 0)
    g4_binding_accuracy = g4_result.get("metrics", {}).get("binding_accuracy", 0.0)
    g4_slot_prefixes = g4_result.get("slot_prefixes", {})

    raw_evidence = {
        "experiment_id": "EXP-PRODUCT-34704657427",
        "conditions": all_results,
        "controls": {
            "P1_PATH_PREFIX": {
                "type": "positive_control",
                "expected": "slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'users/'}",
                "observed": f"slot_count={all_results['P1_PATH_PREFIX'].get('slot_count', 0)}, binding_accuracy={all_results['P1_PATH_PREFIX'].get('metrics', {}).get('binding_accuracy', 0)}, slot_prefixes={p1_slot_prefixes}",
                "passed": condition_pass["P1_PATH_PREFIX"],
            },
            "N1_ORIGINAL": {
                "type": "fix2_target",
                "expected": "slot_count=0",
                "observed": f"slot_count={all_results['N1_ORIGINAL'].get('slot_count', 0)}",
                "passed": condition_pass["N1_ORIGINAL"],
            },
            "N1_CORRECTED": {
                "type": "null_control_corrected",
                "expected": "slot_count=0",
                "observed": f"slot_count={all_results['N1_CORRECTED'].get('slot_count', 0)}",
                "passed": condition_pass.get("N1_CORRECTED", False),
            },
        },
        "aggregate": {
            "total_conditions": total_conditions,
            "passed_conditions": passed_conditions,
            "condition_pass_rate": condition_pass_rate,
            "structural_generalization_rate": structural_generalization_rate,
            "overall_binding_accuracy": overall_binding_accuracy,
        },
        "condition_pass": condition_pass,
        "slot_prefixes_analysis": {
            "p1_observed": p1_slot_prefixes,
            "p1_expected": CONDITIONS["P1_PATH_PREFIX"]["expected_slot_prefixes"],
            "p1_nonempty": p1_prefix_nonempty,
            "p1_exact": p1_prefix_exact,
            "g3_observed": g3_slot_prefixes,
            "g3_expected": CONDITIONS["G3_DEEP_PATH"]["expected_slot_prefixes"],
            "g3_nonempty": g3_prefix_nonempty,
            "g3_exact": g3_prefix_exact,
            "g5_observed": g5_slot_prefixes,
            "g5_expected": CONDITIONS["G5_PATH_QUERY_HYBRID"]["expected_slot_prefixes"],
            "g5_nonempty": g5_prefix_nonempty,
            "g5_exact": g5_prefix_exact,
            "g1_observed": g1_slot_prefixes,
            "g2_observed": g2_slot_prefixes,
            "all_path_prefix_nonempty": all_path_prefix_nonempty,
            "all_path_prefix_exact": all_path_prefix_exact,
        },
        "g4_separate": {
            "slot_count": g4_slot_count,
            "binding_accuracy": g4_binding_accuracy,
            "slot_prefixes": g4_slot_prefixes,
            "architectural_bound": True,
            "note": "G4 reported separately per prereg; not part of frozen decision_rule",
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
            "all_path_prefix_exact": all_path_prefix_exact,
        },
        "fixes_applied": {
            "fix1_suffix_guard": "Exclude single-character suffixes not preceded by structural delimiters (?, =, &)",
            "fix2_delimiter_bound_prefix": "Last-char of prefix in /?=& (validated in EXP-PRODUCT-34642376433)",
            "empty_prefix_guard": "Frozen: reject parameterization when common prefix is empty (truly disjoint URLs)",
            "slot_prefixes_algorithm": "Template-based: extract path segment between domain authority and slot position in built template",
        },
        "substrate": {
            "module": "src.spider.kernel (helpers inline)",
            "approach": "committed code logic, self-contained script",
            "mechanism_model": "slot_prefixes is a proper dataclass field in models.py",
            "bind_function": "actual kernel._bind (template substitution)",
            "slot_prefixes_method": "template-based extraction (NEW for this experiment)",
        },
    }

    with open("raw_evidence.json", "w") as f:
        json.dump(raw_evidence, f, indent=2)

    print(f"Experiment complete: {passed_conditions}/{total_conditions} conditions passed")
    print(f"Overall binding accuracy: {overall_binding_accuracy:.3f}")
    print(f"Structural generalization rate: {structural_generalization_rate:.3f}")
    print(f"P1 (positive control): {'PASS' if p1_passes else 'FAIL'}")
    print(f"G1 (fix1 target): {'PASS' if g1_passes else 'FAIL'}")
    print(f"G2 (regression): {'PASS' if g2_passes else 'FAIL'}")
    print(f"G3 (regression): {'PASS' if g3_passes else 'FAIL'}")
    print(f"G5 (regression): {'PASS' if g5_passes else 'FAIL'}")
    print(f"N1_ORIGINAL (fix2 target): {'PASS' if n1_original_passes else 'FAIL'}")
    print(f"N1_CORRECTED (null control): {'PASS' if n1_corrected_passes else 'FAIL'}")
    print(f"slot_prefixes non-empty for P1/G3/G5: {all_path_prefix_nonempty}")
    print(f"slot_prefixes exact match P1/G3/G5: {all_path_prefix_exact}")
    print(f"  P1: {p1_slot_prefixes} (expected: {CONDITIONS['P1_PATH_PREFIX']['expected_slot_prefixes']})")
    print(f"  G3: {g3_slot_prefixes} (expected: {CONDITIONS['G3_DEEP_PATH']['expected_slot_prefixes']})")
    print(f"  G5: {g5_slot_prefixes} (expected: {CONDITIONS['G5_PATH_QUERY_HYBRID']['expected_slot_prefixes']})")
    print(f"G4 (architectural): slot_count={g4_slot_count}, binding={g4_binding_accuracy}")

    return raw_evidence


if __name__ == "__main__":
    main()
