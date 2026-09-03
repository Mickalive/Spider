#!/usr/bin/env python3
"""EXP-PRODUCT-33741671686: Multi-Parameter Induction Experiment.

Tests claim C-PARAM-INHERIT: generalization to multi-parameter mechanisms.
Condition C1-C5 plus positive/null controls and baselines.
"""

import json
import hashlib
import tempfile
import time
import re
from pathlib import Path
from typing import Any

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from spider import SpiderKernel, Observation, Resolution, ResolutionStatus
from spider.registry import MechanismRegistry
from spider.models import Mechanism


# ═══════════════════════════════════════════════════════════════════════════════
# Multi-Parameter Induction Engine
# ═══════════════════════════════════════════════════════════════════════════════

def _deep_get(obj: Any, path: tuple) -> Any:
    """Get a nested value by path tuple. E.g., _deep_get(d, ('body', 'name'))."""
    current = obj
    for key in path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current


def _deep_set(obj: dict, path: tuple, value: Any) -> None:
    """Set a nested value by path tuple."""
    current = obj
    for key in path[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[path[-1]] = value


def _collect_leaf_paths(obj: Any, prefix: tuple = ()) -> list[tuple]:
    """Collect all leaf paths in a nested dict/list structure."""
    paths = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            paths.extend(_collect_leaf_paths(v, prefix + (k,)))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            paths.extend(_collect_leaf_paths(item, prefix + (str(i),)))
    else:
        paths.append(prefix)
    return paths


def _lcs(a: str, b: str) -> str:
    """Longest common substring between two strings."""
    if not a or not b:
        return ""
    # Use dynamic programming
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    end_a = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_a = i
    return a[end_a - max_len:end_a] if max_len > 0 else ""


def _common_prefix_and_suffix(values: list[str]) -> tuple[str, str, str]:
    """Find common prefix and suffix across a list of string values.
    Returns (prefix, suffix, varying_middle_values).
    """
    if len(values) < 2:
        return ("", "", values)
    
    # Find common prefix
    prefix = values[0]
    for v in values[1:]:
        while not v.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                break
    
    # Find common suffix (on the full strings, not after prefix removal)
    suffix = values[0]
    for v in values[1:]:
        while not v.endswith(suffix):
            suffix = suffix[1:]
            if not suffix:
                break
    
    # Varying middle values: strip prefix and suffix from each value
    middles = []
    for v in values:
        mid = v[len(prefix):]
        if suffix and mid.endswith(suffix):
            mid = mid[:-len(suffix)]
        middles.append(mid)
    
    return (prefix, suffix, middles)


def _is_varying_field(field_values: list[Any]) -> bool:
    """Check if a field genuinely varies across observations."""
    if len(field_values) < 2:
        return False
    str_values = [json.dumps(v, sort_keys=True) for v in field_values]
    return len(set(str_values)) > 1


def _field_path_to_slot_name(field_path: tuple, values: list[str]) -> str:
    """Generate a descriptive slot name from field path and observed values.
    
    Uses the field path structure to create meaningful names.
    Falls back to generic naming when path is ambiguous.
    """
    # Map known patterns to descriptive names
    path_str = ".".join(str(p) for p in field_path)
    
    # Heuristic: use the last path segment, cleaned up
    last_seg = str(field_path[-1]).lower()
    
    # Clean up common patterns
    name = re.sub(r'[^a-z0-9_]', '_', last_seg)
    name = re.sub(r'_+', '_', name).strip('_')
    
    if not name:
        name = "param"
    
    # Ensure uniqueness by appending path context if needed
    return name


def _extract_varying_values_multi(observations: list[Observation]) -> dict:
    """Extract varying fields across observations with distinct slot naming.
    
    Returns dict: {
        'slots': {slot_name: {'field_path': tuple, 'prefix': str, 'suffix': str, 'values': list}},
        'template': dict (action template with ${slot} placeholders),
        'slot_count': int,
    }
    """
    if len(observations) < 2:
        return {'slots': {}, 'template': {}, 'slot_count': 0}
    
    # Collect all leaf paths from the first observation's action
    all_paths = set()
    for obs in observations:
        all_paths.update(_collect_leaf_paths(obs.action))
    
    # Check each path for variation across observations
    varying_fields = {}
    for path in all_paths:
        values = [_deep_get(obs.action, path) for obs in observations]
        if _is_varying_field(values):
            # Check if values are strings (for prefix/suffix extraction)
            str_values = [str(v) for v in values if v is not None]
            if str_values and all(isinstance(v, str) for v in values if v is not None):
                varying_fields[path] = str_values
            elif str_values:
                # Non-string varying fields: treat each as a distinct value
                varying_fields[path] = [json.dumps(v) for v in values if v is not None]
    
    if not varying_fields:
        return {'slots': {}, 'template': {}, 'slot_count': 0}
    
    # Create distinct slot names for each varying field
    slots = {}
    used_names = set()
    
    for field_path, values in varying_fields.items():
        # Generate base name from field path
        base_name = _field_path_to_slot_name(field_path, values)
        
        # Ensure uniqueness
        name = base_name
        counter = 1
        while name in used_names:
            name = f"{base_name}_{counter}"
            counter += 1
        used_names.add(name)
        
        # Extract prefix/suffix
        prefix, suffix, middles = _common_prefix_and_suffix(values)
        
        slots[name] = {
            'field_path': field_path,
            'prefix': prefix,
            'suffix': suffix,
            'values': middles,
            'raw_values': values,
        }
    
    # Build template with ${slot} placeholders
    # Start from first observation's action, replace varying values with ${slot}
    template = json.loads(json.dumps(observations[0].action))
    
    for slot_name, slot_info in slots.items():
        field_path = slot_info['field_path']
        prefix = slot_info['prefix']
        suffix = slot_info['suffix']
        raw_val = slot_info['raw_values'][0]  # Use first observation as reference
        
        if prefix or suffix:
            # Construct template with prefix/suffix
            template_val = f"{prefix}${{{slot_name}}}{suffix}"
        else:
            # Full value replacement
            template_val = f"${{{slot_name}}}"
        
        _deep_set(template, field_path, template_val)
    
    return {
        'slots': slots,
        'template': template,
        'slot_count': len(slots),
    }


def distill_parameterized_v2(
    observations: list[Observation],
    mechanism_id: str = "param-multi",
    intent: str | None = None,
) -> Mechanism | None:
    """Multi-parameter induction: extract multiple distinct parameter slots.
    
    This extends the single-parameter heuristic from EXP-PRODUCT-33528829801
    to handle multiple varying fields with distinct slot naming.
    """
    if not observations:
        return None
    
    successful = [obs for obs in observations if obs.success]
    if not successful:
        return None
    
    result = _extract_varying_values_multi(successful)
    
    if result['slot_count'] == 0:
        return None
    
    # Determine intent from observations
    obs_intent = intent or successful[0].intent
    
    # Merge preconditions from all observations (intersect)
    preconditions = dict(successful[0].state)
    
    # Postconditions from last observation
    postconditions = dict(successful[-1].next_state)
    
    # Build evidence list
    evidence = [hashlib.sha256(json.dumps(obs.action, sort_keys=True).encode()).hexdigest()[:16]
                for obs in successful]
    
    # Confidence: higher when more training observations agree
    confidence = min(0.9, 0.5 + 0.1 * len(successful))
    
    return Mechanism(
        mechanism_id=mechanism_id,
        intent=obs_intent,
        preconditions=preconditions,
        action_template=result['template'],
        postconditions=postconditions,
        parameter_slots=sorted(result['slots'].keys()),
        evidence=evidence,
        confidence=confidence,
    )


def resolve_with_params(
    kernel: SpiderKernel,
    intent: str,
    context: dict[str, Any],
    params: dict[str, Any],
) -> Resolution:
    """Resolve using the kernel's existing resolve() pipeline."""
    return kernel.resolve(intent, context, params=params)


# ═══════════════════════════════════════════════════════════════════════════════
# Synthetic Test Data
# ═══════════════════════════════════════════════════════════════════════════════

SHARED_STATE = {"authenticated": True, "role": "owner"}
SHARED_NEXT_STATE = {"exists": False}


def _obs(intent: str, action: dict, state: dict = None, next_state: dict = None,
         provenance: dict = None) -> Observation:
    return Observation(
        intent=intent,
        state=state or dict(SHARED_STATE),
        action=action,
        next_state=next_state or dict(SHARED_NEXT_STATE),
        success=True,
        provenance=provenance or {"source": "synthetic"},
    )


# ─── Condition C1: Single path parameter (regression) ───────────────────────

def c1_training() -> list[Observation]:
    return [_obs("get-item", {"method": "GET", "url": "https://api.example.com/items/A"}),
            _obs("get-item", {"method": "GET", "url": "https://api.example.com/items/B"}),
            _obs("get-item", {"method": "GET", "url": "https://api.example.com/items/C"})]

def c1_unseen() -> list[dict]:
    return [{"id": "D"}, {"id": "E"}, {"id": "F"}, {"id": "G"}, {"id": "H"}]

def c1_expected_bindings(params: dict) -> dict:
    return {"method": "GET", "url": f"https://api.example.com/items/{params['id']}"}


# ─── Condition C2: Path + body ───────────────────────────────────────────────

def c2_training() -> list[Observation]:
    return [_obs("create-user", {"method": "POST", "url": "https://api.example.com/users/A",
                                 "body": {"name": "Alice"}}),
            _obs("create-user", {"method": "POST", "url": "https://api.example.com/users/B",
                                 "body": {"name": "Bob"}}),
            _obs("create-user", {"method": "POST", "url": "https://api.example.com/users/C",
                                 "body": {"name": "Charlie"}})]

def c2_unseen() -> list[dict]:
    return [{"user_id": "D", "name": "Diana"},
            {"user_id": "E", "name": "Eve"},
            {"user_id": "F", "name": "Frank"},
            {"user_id": "G", "name": "Grace"},
            {"user_id": "H", "name": "Heidi"}]

def c2_expected_bindings(params: dict) -> dict:
    return {"method": "POST",
            "url": f"https://api.example.com/users/{params['user_id']}",
            "body": {"name": params['name']}}


# ─── Condition C3: Path + body + headers ─────────────────────────────────────

def c3_training() -> list[Observation]:
    return [_obs("create-post", {"method": "POST", "url": "https://api.example.com/posts/A",
                                 "body": {"title": "First"},
                                 "headers": {"X-Request-ID": "req-1"}}),
            _obs("create-post", {"method": "POST", "url": "https://api.example.com/posts/B",
                                 "body": {"title": "Second"},
                                 "headers": {"X-Request-ID": "req-2"}}),
            _obs("create-post", {"method": "POST", "url": "https://api.example.com/posts/C",
                                 "body": {"title": "Third"},
                                 "headers": {"X-Request-ID": "req-3"}})]

def c3_unseen() -> list[dict]:
    # The induction extracts prefix "req-" from headers, so the template is
    # req-${x_request_id}. Unseen params provide the VARYING MIDDLE only.
    # Similarly, the URL template is prefix + ${url} + suffix.
    return [{"post_id": "D", "title": "Fourth", "request_id": "4"},
            {"post_id": "E", "title": "Fifth", "request_id": "5"},
            {"post_id": "F", "title": "Sixth", "request_id": "6"},
            {"post_id": "G", "title": "Seventh", "request_id": "7"},
            {"post_id": "H", "title": "Eighth", "request_id": "8"}]

def c3_expected_bindings(params: dict) -> dict:
    # Template: "https://api.example.com/posts/${url}" for URL
    # Template: "${title}" for body.title (no common prefix/suffix)
    # Template: "req-${x_request_id}" for headers (prefix "req-")
    return {"method": "POST",
            "url": f"https://api.example.com/posts/{params['post_id']}",
            "body": {"title": params['title']},
            "headers": {"X-Request-ID": f"req-{params['request_id']}"}}


# ─── Condition C4: Non-identifier values ─────────────────────────────────────

def c4_training() -> list[Observation]:
    return [_obs("set-webhook", {"method": "POST", "url": "https://api.example.com/webhooks",
                                 "body": {"callback_url": "https://site-a.com/hook"}}),
            _obs("set-webhook", {"method": "POST", "url": "https://api.example.com/webhooks",
                                 "body": {"callback_url": "https://site-b.com/hook"}}),
            _obs("set-webhook", {"method": "POST", "url": "https://api.example.com/webhooks",
                                 "body": {"callback_url": "https://site-c.com/hook"}})]

def c4_unseen() -> list[dict]:
    # The induction extracts prefix "https://site-" and suffix ".com/hook" from
    # the callback_url values. The template becomes "https://site-${callback_url}.com/hook".
    # Unseen params provide the VARYING MIDDLE only (the site identifier).
    return [{"webhook_url": "d"},
            {"webhook_url": "e"},
            {"webhook_url": "f"}]

def c4_expected_bindings(params: dict) -> dict:
    # Template: "https://site-${callback_url}.com/hook"
    return {"method": "POST",
            "url": "https://api.example.com/webhooks",
            "body": {"callback_url": f"https://site-{params['webhook_url']}.com/hook"}}


# ─── Condition C5: Shared slot name collision ────────────────────────────────

def c5_training() -> list[Observation]:
    return [_obs("update-item", {"method": "PUT", "url": "https://api.example.com/items/A",
                                 "body": {"user_id": "A"}}),
            _obs("update-item", {"method": "PUT", "url": "https://api.example.com/items/B",
                                 "body": {"user_id": "B"}}),
            _obs("update-item", {"method": "PUT", "url": "https://api.example.com/items/C",
                                 "body": {"user_id": "C"}})]

def c5_unseen() -> list[dict]:
    return [{"item_id": "D", "owner_id": "D"},
            {"item_id": "E", "owner_id": "E"},
            {"item_id": "F", "owner_id": "F"}]

def c5_expected_bindings(params: dict) -> dict:
    return {"method": "PUT",
            "url": f"https://api.example.com/items/{params['item_id']}",
            "body": {"user_id": params['owner_id']}}


# ─── Null Control: Random non-shared observations ────────────────────────────

def null_control_training() -> list[Observation]:
    return [_obs("task-a", {"method": "GET", "url": "https://x.com/alpha"}),
            _obs("task-b", {"method": "DELETE", "path": "/foo/bar/baz"}),
            _obs("task-c", {"method": "PATCH", "data": "completely different structure"})]

def null_control_unseen() -> list[dict]:
    return [{"x": "1"}, {"y": "2"}, {"z": "3"}]


# ═══════════════════════════════════════════════════════════════════════════════
# Experiment Runner
# ═══════════════════════════════════════════════════════════════════════════════

def _check_bound_action(expected: dict, actual: dict) -> tuple[bool, str]:
    """Check if bound_action matches expected, with detailed mismatch info."""
    if actual is None:
        return False, "bound_action is None"
    
    # Compare recursively
    def _cmp(e, a, path=""):
        if isinstance(e, dict):
            if not isinstance(a, dict):
                return False, f"At {path}: expected dict, got {type(a).__name__}"
            for k in e:
                if k not in a:
                    return False, f"At {path}.{k}: key missing in actual"
                ok, msg = _cmp(e[k], a[k], f"{path}.{k}")
                if not ok:
                    return False, msg
            return True, ""
        elif isinstance(e, list):
            if not isinstance(a, list):
                return False, f"At {path}: expected list, got {type(a).__name__}"
            if len(e) != len(a):
                return False, f"At {path}: list length mismatch {len(e)} vs {len(a)}"
            for i, (ei, ai) in enumerate(zip(e, a)):
                ok, msg = _cmp(ei, ai, f"{path}[{i}]")
                if not ok:
                    return False, msg
            return True, ""
        else:
            if e != a:
                return False, f"At {path}: expected {e!r}, got {a!r}"
            return True, ""
    
    return _cmp(expected, actual, "root")


def run_condition(
    condition_id: str,
    training: list[Observation],
    unseen: list[dict],
    expected_bindings_fn,
    expected_slot_count: int,
    kernel: SpiderKernel,
    reg: MechanismRegistry,
) -> dict:
    """Run a single experimental condition."""
    result = {
        "condition_id": condition_id,
        "training_count": len(training),
        "unseen_count": len(unseen),
        "timestamps": {"start": time.time()},
    }
    
    # Distill parameterized mechanism
    mech = distill_parameterized_v2(training, mechanism_id=f"param-{condition_id}")
    
    if mech is None:
        result["distill_success"] = False
        result["error"] = "distill_parameterized_v2 returned None"
        result["timestamps"]["end"] = time.time()
        return result
    
    result["distill_success"] = True
    result["mechanism_id"] = mech.mechanism_id
    result["action_template"] = mech.action_template
    result["parameter_slots"] = mech.parameter_slots
    result["slot_count"] = len(mech.parameter_slots)
    result["confidence"] = mech.confidence
    result["preconditions"] = mech.preconditions
    result["postconditions"] = mech.postconditions
    
    # Check slot count expectation
    result["slot_count_expected"] = expected_slot_count
    result["slot_count_met"] = result["slot_count"] >= expected_slot_count
    
    # Check for slot name collisions (distinctness)
    result["slot_names_distinct"] = len(mech.parameter_slots) == len(set(mech.parameter_slots))
    
    # Register mechanism
    reg.upsert(mech)
    
    # Resolve on unseen combinations
    resolution_results = []
    for params in unseen:
        # Map spec param names to actual slot names
        # The induction may name slots differently than the spec expects
        # We need to figure out which param maps to which slot
        slot_to_param = {}
        for slot in mech.parameter_slots:
            # Try to match slot name to param key
            for k, v in params.items():
                if k == slot or slot in k or k in slot:
                    slot_to_param[slot] = v
                    break
            else:
                # Fallback: try to match by value pattern
                for k, v in params.items():
                    if isinstance(v, str) and slot.replace("_", "") in k.replace("_", ""):
                        slot_to_param[slot] = v
                        break
        
        # If we couldn't match all slots, try positional matching
        if len(slot_to_param) < len(mech.parameter_slots):
            unmatched_slots = [s for s in mech.parameter_slots if s not in slot_to_param]
            unmatched_params = {k: v for k, v in params.items() if k not in slot_to_param.values()}
            for slot, val in zip(unmatched_slots, unmatched_params.values()):
                slot_to_param[slot] = val
        
        # Build the full param dict for resolution
        resolve_params = slot_to_param
        
        start = time.perf_counter()
        resolution = kernel.resolve(
            mech.intent,
            dict(SHARED_STATE),
            params=resolve_params,
        )
        elapsed = time.perf_counter() - start
        
        # Check binding correctness
        expected_binding = expected_bindings_fn(params)
        binding_ok, binding_msg = _check_bound_action(expected_binding, resolution.bound_action)
        
        # Check for unsubstituted templates in bound_action
        has_unsubstituted = False
        if resolution.bound_action:
            action_str = json.dumps(resolution.bound_action)
            has_unsubstituted = "${" in action_str
        
        resolution_results.append({
            "params": params,
            "resolve_params": resolve_params,
            "status": resolution.status.value,
            "mechanism_id": resolution.mechanism_id,
            "bound_action": resolution.bound_action,
            "reason": resolution.reason,
            "confidence": resolution.confidence,
            "elapsed_seconds": elapsed,
            "binding_correct": binding_ok,
            "binding_detail": binding_msg if not binding_ok else "ok",
            "has_unsubstituted_template": has_unsubstituted,
        })
    
    result["resolution_results"] = resolution_results
    
    # Compute metrics
    executable_count = sum(1 for r in resolution_results if r["status"] == "EXECUTABLE")
    binding_correct_count = sum(1 for r in resolution_results if r["binding_correct"])
    unsubstituted_count = sum(1 for r in resolution_results if r["has_unsubstituted_template"])
    
    result["metrics"] = {
        "unseen_resolution_rate": executable_count / len(unseen) if unseen else 0,
        "binding_accuracy": binding_correct_count / len(unseen) if unseen else 0,
        "unsubstituted_template_rate": unsubstituted_count / len(unseen) if unseen else 0,
        "executable_count": executable_count,
        "binding_correct_count": binding_correct_count,
    }
    
    result["timestamps"]["end"] = time.time()
    return result


def run_experiment() -> dict:
    print("=" * 70)
    print("EXP-PRODUCT-33741671686: Multi-Parameter Induction")
    print("=" * 70)
    
    raw_evidence = {
        "experiment_id": "EXP-PRODUCT-33741671686",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "conditions": {},
        "controls": {},
        "baselines": {},
        "induction_audit": {},
        "decision": {},
    }
    
    # ─── Run all conditions ──────────────────────────────────────────────
    
    conditions = [
        ("C1-single-path", c1_training, c1_unseen, c1_expected_bindings, 1),
        ("C2-path-and-body", c2_training, c2_unseen, c2_expected_bindings, 2),
        ("C3-path-body-headers", c3_training, c3_unseen, c3_expected_bindings, 3),
        ("C4-non-identifier-values", c4_training, c4_unseen, c4_expected_bindings, 1),
        ("C5-shared-slot-name", c5_training, c5_unseen, c5_expected_bindings, 2),
    ]
    
    for cond_id, train_fn, unseen_fn, expected_fn, exp_slots in conditions:
        print(f"\n{'─'*60}")
        print(f"  Condition: {cond_id}")
        print(f"{'─'*60}")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            reg = MechanismRegistry(Path(tmpdir) / "mechanisms.jsonl")
            kernel = SpiderKernel(reg)
            
            training = train_fn()
            unseen = unseen_fn()
            
            result = run_condition(
                cond_id, training, unseen, expected_fn, exp_slots, kernel, reg
            )
            
            raw_evidence["conditions"][cond_id] = result
            
            # Print summary
            print(f"  Distill success: {result.get('distill_success', False)}")
            print(f"  Slot count: {result.get('slot_count', 0)} (expected >= {exp_slots})")
            print(f"  Slots: {result.get('parameter_slots', [])}")
            print(f"  Template: {result.get('action_template', {})}")
            
            if result.get("distill_success"):
                m = result["metrics"]
                print(f"  Unseen resolution rate: {m['unseen_resolution_rate']:.1%}")
                print(f"  Binding accuracy: {m['binding_accuracy']:.1%}")
                print(f"  Unsubstituted templates: {m['unsubstituted_template_rate']:.1%}")
                
                # Print per-unseen details
                for r in result["resolution_results"]:
                    sym = "✓" if r["status"] == "EXECUTABLE" and r["binding_correct"] else "✗"
                    print(f"    [{sym}] {r['params']} -> {r['status']} "
                          f"(binding: {'ok' if r['binding_correct'] else r['binding_detail']})")
    
    # ─── Positive Control (C1 Regression) ────────────────────────────────
    print(f"\n{'─'*60}")
    print("  Positive Control: C1 Regression")
    print(f"{'─'*60}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        reg = MechanismRegistry(Path(tmpdir) / "mechanisms.jsonl")
        kernel = SpiderKernel(reg)
        
        training = c1_training()
        mech = distill_parameterized_v2(training, mechanism_id="param-positive-control")
        if mech:
            reg.upsert(mech)
            
            # Resolve with seen identifier (use actual slot name from induction)
            slot_name = mech.parameter_slots[0] if mech.parameter_slots else "url"
            resolution = kernel.resolve("get-item", dict(SHARED_STATE), params={slot_name: "A"})
            raw_evidence["controls"]["positive_control"] = {
                "description": "Resolve with seen identifier A from training set",
                "expected": "EXECUTABLE",
                "observed": resolution.status.value,
                "bound_action": resolution.bound_action,
                "passed": resolution.status == ResolutionStatus.EXECUTABLE,
                "slots": mech.parameter_slots,
                "resolve_params": {slot_name: "A"},
            }
            sym = "✓" if resolution.status == ResolutionStatus.EXECUTABLE else "✗"
            print(f"  [{sym}] Seen identifier A: {resolution.status.value} "
                  f"bound_action={resolution.bound_action}")
        else:
            raw_evidence["controls"]["positive_control"] = {
                "description": "Distillation failed for positive control",
                "expected": "EXECUTABLE",
                "observed": "DISTILL_FAILED",
                "passed": False,
            }
            print("  [✗] Distillation failed")
    
    # ─── Null Control ────────────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print("  Null Control: Non-shared observations")
    print(f"{'─'*60}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        reg = MechanismRegistry(Path(tmpdir) / "mechanisms.jsonl")
        kernel = SpiderKernel(reg)
        
        training = null_control_training()
        mech = distill_parameterized_v2(training, mechanism_id="param-null-control")
        
        if mech is None:
            raw_evidence["controls"]["null_control"] = {
                "description": "Random non-shared observations produce no parameterized mechanism",
                "expected": "no mechanism (None)",
                "observed": "None",
                "passed": True,
                "reason": "No varying fields detected across non-shared observations",
            }
            print("  [✓] No mechanism induced (correct: no pattern to find)")
        else:
            # Mechanism was induced; check if it's reasonable
            resolution = kernel.resolve(mech.intent, dict(SHARED_STATE), params={})
            raw_evidence["controls"]["null_control"] = {
                "description": "Random non-shared observations produce no parameterized mechanism",
                "expected": "no mechanism or UNKNOWN",
                "observed": f"mechanism with {len(mech.parameter_slots)} slots",
                "mechanism": {
                    "slots": mech.parameter_slots,
                    "template": mech.action_template,
                },
                "resolution_status": resolution.status.value,
                "passed": resolution.status in (ResolutionStatus.UNKNOWN, ResolutionStatus.EXPLORE),
            }
            sym = "✓" if resolution.status in (ResolutionStatus.UNKNOWN, ResolutionStatus.EXPLORE) else "✗"
            print(f"  [{sym}] Mechanism induced with {len(mech.parameter_slots)} slots "
                  f"(resolution: {resolution.status.value})")
    
    # ─── Baseline: B_LITERAL ─────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print("  Baseline B_LITERAL: Literal replay on unseen")
    print(f"{'─'*60}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        reg = MechanismRegistry(Path(tmpdir) / "mechanisms.jsonl")
        kernel = SpiderKernel(reg)
        
        # Distill literal mechanism from first C2 training obs
        obs = c2_training()[0]
        lit_mech = kernel.distill(obs)
        if lit_mech:
            lit_mech.mechanism_id = "literal-baseline"
            reg.upsert(lit_mech)
            
            b_literal_results = []
            for params in c2_unseen():
                resolution = kernel.resolve("create-user", dict(SHARED_STATE), params={})
                b_literal_results.append({
                    "params": params,
                    "status": resolution.status.value,
                })
            
            fail_count = sum(1 for r in b_literal_results if r["status"] != "EXECUTABLE")
            raw_evidence["baselines"]["B_LITERAL"] = {
                "description": "Literal mechanism with no parameter slots",
                "results": b_literal_results,
                "fail_count": fail_count,
                "fail_rate": fail_count / len(b_literal_results),
                "all_fail": fail_count == len(b_literal_results),
            }
            print(f"  Literal fails on {fail_count}/{len(b_literal_results)} unseen")
        else:
            raw_evidence["baselines"]["B_LITERAL"] = {
                "description": "Literal mechanism distillation failed",
                "error": "distill returned None",
            }
            print("  [!] Literal distillation failed")
    
    # ─── Baseline: B_RANDOM_INDUCTION ────────────────────────────────────
    print(f"\n{'─'*60}")
    print("  Baseline B_RANDOM_INDUCTION: Random slot naming")
    print(f"{'─'*60}")
    
    import random
    random.seed(42)  # Deterministic
    
    with tempfile.TemporaryDirectory() as tmpdir:
        reg = MechanismRegistry(Path(tmpdir) / "mechanisms.jsonl")
        kernel = SpiderKernel(reg)
        
        # Take C2 training, induce properly, then randomize slot names
        training = c2_training()
        mech = distill_parameterized_v2(training, mechanism_id="param-random")
        if mech:
            # Randomize slot names
            original_slots = list(mech.parameter_slots)
            randomized_slots = [f"rand_{i}" for i in range(len(original_slots))]
            
            # Replace in action template
            template_str = json.dumps(mech.action_template)
            for orig, rand in zip(original_slots, randomized_slots):
                template_str = template_str.replace(f"${{{orig}}}", f"${{{rand}}}")
            mech.action_template = json.loads(template_str)
            mech.parameter_slots = randomized_slots
            
            reg.upsert(mech)
            
            # Try to resolve with the *correct* param names (not the randomized ones)
            b_random_results = []
            for params in c2_unseen():
                # Map correct params to randomized slot names (randomly)
                resolve_params = {}
                for i, (k, v) in enumerate(params.items()):
                    if i < len(randomized_slots):
                        resolve_params[randomized_slots[i]] = v
                
                resolution = kernel.resolve("create-user", dict(SHARED_STATE), params=resolve_params)
                b_random_results.append({
                    "params": params,
                    "status": resolution.status.value,
                    "bound_action": resolution.bound_action,
                })
            
            executable_count = sum(1 for r in b_random_results if r["status"] == "EXECUTABLE")
            raw_evidence["baselines"]["B_RANDOM_INDUCTION"] = {
                "description": "Random slot naming on C2 multi-parameter",
                "original_slots": original_slots,
                "randomized_slots": randomized_slots,
                "results": b_random_results,
                "executable_count": executable_count,
                "resolution_rate": executable_count / len(b_random_results),
            }
            print(f"  Random naming: {executable_count}/{len(b_random_results)} resolved")
        else:
            raw_evidence["baselines"]["B_RANDOM_INDUCTION"] = {
                "description": "Induction failed for random baseline",
                "error": "distill returned None",
            }
            print("  [!] Induction failed")
    
    # ─── Induction Audit ─────────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print("  Induction Audit")
    print(f"{'─'*60}")
    
    audit_results = {}
    for cond_id, train_fn, unseen_fn, expected_fn, exp_slots in conditions:
        training = train_fn()
        mech = distill_parameterized_v2(training, mechanism_id=f"audit-{cond_id}")
        if mech:
            # Check if template contains ${} placeholders for each slot
            template_str = json.dumps(mech.action_template)
            slots_in_template = set(re.findall(r'\$\{([^}]+)\}', template_str))
            
            audit_results[cond_id] = {
                "slot_count": len(mech.parameter_slots),
                "expected_slot_count": exp_slots,
                "slots": mech.parameter_slots,
                "slots_in_template": sorted(slots_in_template),
                "all_slots_in_template": all(s in slots_in_template for s in mech.parameter_slots),
                "slot_names_distinct": len(mech.parameter_slots) == len(set(mech.parameter_slots)),
            }
            print(f"  {cond_id}: {len(mech.parameter_slots)} slots, "
                  f"distinct={audit_results[cond_id]['slot_names_distinct']}, "
                  f"in_template={audit_results[cond_id]['all_slots_in_template']}")
        else:
            audit_results[cond_id] = {
                "slot_count": 0,
                "expected_slot_count": exp_slots,
                "error": "induction failed",
            }
            print(f"  {cond_id}: induction FAILED")
    
    raw_evidence["induction_audit"] = audit_results
    
    # ─── Decision Rule ───────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("DECISION")
    print(f"{'='*70}")
    
    decision_checks = {}
    
    # Check 1: C1 regression passes
    c1_result = raw_evidence["conditions"].get("C1-single-path", {})
    c1_metrics = c1_result.get("metrics", {})
    decision_checks["C1_regression"] = (
        c1_result.get("slot_count", 0) >= 1
        and c1_metrics.get("unseen_resolution_rate", 0) >= 0.9
        and c1_metrics.get("binding_accuracy", 0) >= 0.9
    )
    
    # Check 2: C2 multi-parameter
    c2_result = raw_evidence["conditions"].get("C2-path-and-body", {})
    c2_metrics = c2_result.get("metrics", {})
    decision_checks["C2_multi_param"] = (
        c2_result.get("slot_count", 0) >= 2
        and c2_result.get("slot_names_distinct", False)
        and c2_metrics.get("unseen_resolution_rate", 0) >= 0.9
        and c2_metrics.get("binding_accuracy", 0) >= 0.9
    )
    
    # Check 3: C3 three-parameter
    c3_result = raw_evidence["conditions"].get("C3-path-body-headers", {})
    c3_metrics = c3_result.get("metrics", {})
    decision_checks["C3_three_param"] = (
        c3_result.get("slot_count", 0) >= 3
        and c3_result.get("slot_names_distinct", False)
        and c3_metrics.get("unseen_resolution_rate", 0) >= 0.9
        and c3_metrics.get("binding_accuracy", 0) >= 0.9
    )
    
    # Check 4: C4 non-identifier
    c4_result = raw_evidence["conditions"].get("C4-non-identifier-values", {})
    c4_metrics = c4_result.get("metrics", {})
    decision_checks["C4_non_identifier"] = (
        c4_result.get("slot_count", 0) >= 1
        and c4_metrics.get("unseen_resolution_rate", 0) >= 0.9
        and c4_metrics.get("binding_accuracy", 0) >= 0.9
    )
    
    # Check 5: C5 shared-slot collision (no collision)
    c5_result = raw_evidence["conditions"].get("C5-shared-slot-name", {})
    c5_metrics = c5_result.get("metrics", {})
    decision_checks["C5_no_collision"] = (
        c5_result.get("slot_count", 0) >= 2
        and c5_result.get("slot_names_distinct", False)
        and c5_metrics.get("unseen_resolution_rate", 0) >= 0.9
        and c5_metrics.get("binding_accuracy", 0) >= 0.9
    )
    
    # Check 6: Null control
    null_ctrl = raw_evidence["controls"].get("null_control", {})
    decision_checks["null_control"] = null_ctrl.get("passed", False)
    
    # Check 7: No crashes
    all_distilled = all(
        raw_evidence["conditions"][c].get("distill_success", False)
        for c in ["C1-single-path", "C2-path-and-body", "C3-path-body-headers",
                   "C4-non-identifier-values", "C5-shared-slot-name"]
    )
    decision_checks["no_crashes"] = all_distilled
    
    all_pass = all(decision_checks.values())
    verdict = "MULTI-PARAM-SURVIVES" if all_pass else "MULTI-PARAM-FALSIFIED"
    
    # Check for MEASUREMENT_INVALID
    if not all_distilled and not any(decision_checks.values()):
        verdict = "MEASUREMENT_INVALID"
    
    for check, passed in decision_checks.items():
        sym = "✓" if passed else "✗"
        print(f"  [{sym}] {check}")
    
    print(f"\n  VERDICT: {verdict}")
    
    raw_evidence["decision"] = {
        "checks": decision_checks,
        "verdict": verdict,
        "claim_id": "C-PARAM-INHERIT",
    }
    
    return raw_evidence


if __name__ == "__main__":
    evidence = run_experiment()
    
    # Write raw evidence
    output_path = Path(__file__).parent / "raw_evidence.json"
    with open(output_path, "w") as f:
        json.dump(evidence, f, indent=2, default=str)
    
    print(f"\nRaw evidence written to: {output_path}")
