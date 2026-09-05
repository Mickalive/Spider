#!/usr/bin/env python3
"""EXP-PRODUCT-33974562602: Kernel Integration of Multi-Parameter Induction.

Phase B: Regression baseline (5 conditions from EXP-PRODUCT-33741671686)
Phase C: Full-value unseen tests
Phase D: Noisy browser-like observations
Phase E: Null control (pattern absence)
Baselines: B_LITERAL, B_RANDOM_INDUCTION
"""

import json
import hashlib
import tempfile
import time
import re
import random
from pathlib import Path
from typing import Any

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from spider import SpiderKernel, Observation, Resolution, ResolutionStatus
from spider.registry import MechanismRegistry
from spider.models import Mechanism

random.seed(42)  # Deterministic for B_RANDOM_INDUCTION


# ═══════════════════════════════════════════════════════════════════════════════
# Shared helpers
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


def _check_bound_action(expected: dict, actual: dict) -> tuple[bool, str]:
    """Check if bound_action matches expected, with detailed mismatch info."""
    if actual is None:
        return False, "bound_action is None"

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


def _has_unsubstituted(bound_action: dict) -> bool:
    if bound_action is None:
        return False
    return "${" in json.dumps(bound_action)


def _make_kernel_and_reg():
    tmpdir = tempfile.mkdtemp()
    reg = MechanismRegistry(Path(tmpdir) / "mechanisms.jsonl")
    kernel = SpiderKernel(reg)
    return tmpdir, reg, kernel


# ═══════════════════════════════════════════════════════════════════════════════
# Phase B: Regression Baseline Conditions (B1-B5)
# Identical to EXP-PRODUCT-33741671686 C1-C5
# ═══════════════════════════════════════════════════════════════════════════════

# B1: Single-path
def b1_training():
    return [_obs("get-item", {"method": "GET", "url": "https://api.example.com/items/A"}),
            _obs("get-item", {"method": "GET", "url": "https://api.example.com/items/B"}),
            _obs("get-item", {"method": "GET", "url": "https://api.example.com/items/C"})]

def b1_unseen():
    return [{"id": "D"}, {"id": "E"}, {"id": "F"}, {"id": "G"}, {"id": "H"}]

def b1_expected(params):
    return {"method": "GET", "url": f"https://api.example.com/items/{params['id']}"}

# B2: Path+body
def b2_training():
    return [_obs("create-user", {"method": "POST", "url": "https://api.example.com/users/A",
                                  "body": {"name": "Alice"}}),
            _obs("create-user", {"method": "POST", "url": "https://api.example.com/users/B",
                                  "body": {"name": "Bob"}}),
            _obs("create-user", {"method": "POST", "url": "https://api.example.com/users/C",
                                  "body": {"name": "Charlie"}})]

def b2_unseen():
    return [{"user_id": "D", "name": "Diana"},
            {"user_id": "E", "name": "Eve"},
            {"user_id": "F", "name": "Frank"},
            {"user_id": "G", "name": "Grace"},
            {"user_id": "H", "name": "Heidi"}]

def b2_expected(params):
    return {"method": "POST",
            "url": f"https://api.example.com/users/{params['user_id']}",
            "body": {"name": params['name']}}

# B3: Path+body+headers
def b3_training():
    return [_obs("create-post", {"method": "POST", "url": "https://api.example.com/posts/A",
                                  "body": {"title": "First"},
                                  "headers": {"X-Request-ID": "req-1"}}),
            _obs("create-post", {"method": "POST", "url": "https://api.example.com/posts/B",
                                  "body": {"title": "Second"},
                                  "headers": {"X-Request-ID": "req-2"}}),
            _obs("create-post", {"method": "POST", "url": "https://api.example.com/posts/C",
                                  "body": {"title": "Third"},
                                  "headers": {"X-Request-ID": "req-3"}})]

def b3_unseen():
    return [{"post_id": "D", "title": "Fourth", "request_id": "4"},
            {"post_id": "E", "title": "Fifth", "request_id": "5"},
            {"post_id": "F", "title": "Sixth", "request_id": "6"},
            {"post_id": "G", "title": "Seventh", "request_id": "7"},
            {"post_id": "H", "title": "Eighth", "request_id": "8"}]

def b3_expected(params):
    return {"method": "POST",
            "url": f"https://api.example.com/posts/{params['post_id']}",
            "body": {"title": params['title']},
            "headers": {"X-Request-ID": f"req-{params['request_id']}"}}

# B4: Non-identifier values
def b4_training():
    return [_obs("set-webhook", {"method": "POST", "url": "https://api.example.com/webhooks",
                                  "body": {"callback_url": "https://site-a.com/hook"}}),
            _obs("set-webhook", {"method": "POST", "url": "https://api.example.com/webhooks",
                                  "body": {"callback_url": "https://site-b.com/hook"}}),
            _obs("set-webhook", {"method": "POST", "url": "https://api.example.com/webhooks",
                                  "body": {"callback_url": "https://site-c.com/hook"}})]

def b4_unseen():
    return [{"webhook_url": "d"},
            {"webhook_url": "e"},
            {"webhook_url": "f"}]

def b4_expected(params):
    return {"method": "POST",
            "url": "https://api.example.com/webhooks",
            "body": {"callback_url": f"https://site-{params['webhook_url']}.com/hook"}}

# B5: Shared-slot collision
def b5_training():
    return [_obs("update-item", {"method": "PUT", "url": "https://api.example.com/items/A",
                                  "body": {"user_id": "A"}}),
            _obs("update-item", {"method": "PUT", "url": "https://api.example.com/items/B",
                                  "body": {"user_id": "B"}}),
            _obs("update-item", {"method": "PUT", "url": "https://api.example.com/items/C",
                                  "body": {"user_id": "C"}})]

def b5_unseen():
    return [{"item_id": "D", "owner_id": "D"},
            {"item_id": "E", "owner_id": "E"},
            {"item_id": "F", "owner_id": "F"}]

def b5_expected(params):
    return {"method": "PUT",
            "url": f"https://api.example.com/items/{params['item_id']}",
            "body": {"user_id": params['owner_id']}}


# ═══════════════════════════════════════════════════════════════════════════════
# Phase C: Full-Value Unseen Tests
# ═══════════════════════════════════════════════════════════════════════════════

# C1: Full-value URLs (same training as B4)
def c1_full_value_unseen():
    """Caller supplies FULL URLs, not pre-stripped middles."""
    return [{"webhook_url": "https://site-d.com/hook"},
            {"webhook_url": "https://site-e.com/hook"},
            {"webhook_url": "https://site-f.com/hook"}]

def c1_full_value_expected(params):
    return {"method": "POST",
            "url": "https://api.example.com/webhooks",
            "body": {"callback_url": params['webhook_url']}}

# C2: Full-value IDs with prefix
def c2_full_value_training():
    return [_obs("get-user", {"method": "GET", "url": "https://api.example.com/users/user-1"}),
            _obs("get-user", {"method": "GET", "url": "https://api.example.com/users/user-2"}),
            _obs("get-user", {"method": "GET", "url": "https://api.example.com/users/user-3"})]

def c2_full_value_unseen():
    return [{"user_id": "user-4"},
            {"user_id": "user-5"},
            {"user_id": "user-6"}]

def c2_full_value_expected(params):
    return {"method": "GET",
            "url": f"https://api.example.com/users/{params['user_id']}"}


# ═══════════════════════════════════════════════════════════════════════════════
# Phase D: Noisy Browser-Like Observations
# ═══════════════════════════════════════════════════════════════════════════════

# D1: Noisy POST with path+body+headers
def d1_noisy_training():
    return [_obs("create-order", {
        "method": "POST",
        "url": "https://api.example.com/orders/order-1",
        "body": {"customer": "cust-A"},
        "headers": {"X-Request-ID": "req-101"},
        "timestamp": "2026-09-05T10:00:00Z",
        "request_duration_ms": 150,
        "retry_count": 0,
        "user_agent": "Mozilla/5.0"
    }, state={"session_id": "sess-1", "authenticated": True}),
    _obs("create-order", {
        "method": "POST",
        "url": "https://api.example.com/orders/order-2",
        "body": {"customer": "cust-B"},
        "headers": {"X-Request-ID": "req-102"},
        "timestamp": "2026-09-05T10:01:00Z",
        "request_duration_ms": 200,
        "retry_count": 1,
        "user_agent": "Mozilla/5.0"
    }, state={"session_id": "sess-2", "authenticated": True}),
    _obs("create-order", {
        "method": "POST",
        "url": "https://api.example.com/orders/order-3",
        "body": {"customer": "cust-C"},
        "headers": {"X-Request-ID": "req-103"},
        "timestamp": "2026-09-05T10:02:00Z",
        "request_duration_ms": 180,
        "retry_count": 0,
        "user_agent": "Mozilla/5.0"
    }, state={"session_id": "sess-3", "authenticated": True})]

def d1_noisy_unseen():
    return [{"order_id": "order-4", "customer": "cust-D", "request_id": "104"},
            {"order_id": "order-5", "customer": "cust-E", "request_id": "105"},
            {"order_id": "order-6", "customer": "cust-F", "request_id": "106"},
            {"order_id": "order-7", "customer": "cust-G", "request_id": "107"},
            {"order_id": "order-8", "customer": "cust-H", "request_id": "108"}]

def d1_noisy_expected(params):
    return {"method": "POST",
            "url": f"https://api.example.com/orders/{params['order_id']}",
            "body": {"customer": params['customer']},
            "headers": {"X-Request-ID": f"req-{params['request_id']}",
                        "timestamp": "2026-09-05T10:00:00Z",
                        "request_duration_ms": 150,
                        "retry_count": 0,
                        "user_agent": "Mozilla/5.0"}}


# D2: Noisy GET with path+query
def d2_noisy_training():
    return [_obs("search", {
        "method": "GET",
        "url": "https://api.example.com/search",
        "query": {"q": "alpha", "page": "1"},
        "response_time_ms": 50,
        "cache_hit": False,
        "result_count": 20
    }),
    _obs("search", {
        "method": "GET",
        "url": "https://api.example.com/search",
        "query": {"q": "beta", "page": "2"},
        "response_time_ms": 75,
        "cache_hit": True,
        "result_count": 15
    }),
    _obs("search", {
        "method": "GET",
        "url": "https://api.example.com/search",
        "query": {"q": "gamma", "page": "3"},
        "response_time_ms": 60,
        "cache_hit": False,
        "result_count": 25
    })]

def d2_noisy_unseen():
    return [{"search_term": "delta", "page_num": "4"},
            {"search_term": "epsilon", "page_num": "5"},
            {"search_term": "zeta", "page_num": "6"},
            {"search_term": "eta", "page_num": "7"},
            {"search_term": "theta", "page_num": "8"}]

def d2_noisy_expected(params):
    return {"method": "GET",
            "url": "https://api.example.com/search",
            "query": {"q": params['search_term'], "page": params['page_num']},
            "response_time_ms": 50,
            "cache_hit": False,
            "result_count": 20}


# D3: Multi-step observation with varying preconditions
def d3_noisy_training():
    return [_obs("place-order", {
        "method": "POST",
        "url": "https://api.example.com/orders/item-1"
    }, state={"session_id": "s-A", "auth_token": "tok-1", "authenticated": True}),
    _obs("place-order", {
        "method": "POST",
        "url": "https://api.example.com/orders/item-2"
    }, state={"session_id": "s-B", "auth_token": "tok-2", "authenticated": True}),
    _obs("place-order", {
        "method": "POST",
        "url": "https://api.example.com/orders/item-3"
    }, state={"session_id": "s-C", "auth_token": "tok-3", "authenticated": True})]

def d3_noisy_unseen():
    return [{"order_item": "item-4"},
            {"order_item": "item-5"},
            {"order_item": "item-6"},
            {"order_item": "item-7"},
            {"order_item": "item-8"}]

def d3_noisy_expected(params):
    return {"method": "POST",
            "url": f"https://api.example.com/orders/{params['order_item']}"}


# ═══════════════════════════════════════════════════════════════════════════════
# Phase E: Null Control (Pattern Absence)
# ═══════════════════════════════════════════════════════════════════════════════

# E1: Unrelated action structures
def e1_null_training():
    return [_obs("make-payment", {"method": "POST", "url": "/api/payments", "body": {"amount": 100, "currency": "USD"}}),
            _obs("get-user", {"method": "GET", "url": "/api/users/42"}),
            _obs("delete-session", {"method": "DELETE", "url": "/api/sessions/abc-123"})]

def e1_null_unseen():
    return [{"x": "1"}, {"y": "2"}, {"z": "3"}]


# E2: Single observation (insufficient for induction)
def e2_single_obs():
    return [_obs("get-item", {"method": "GET", "url": "https://api.example.com/items/A"})]

def e2_unseen():
    return [{"id": "X"}, {"id": "Y"}]


# ═══════════════════════════════════════════════════════════════════════════════
# Run a single condition
# ═══════════════════════════════════════════════════════════════════════════════

def run_condition(condition_id, training, unseen, expected_fn, expected_slot_count, kernel, reg):
    """Run a single experimental condition using kernel.distill_parameterized()."""
    result = {
        "condition_id": condition_id,
        "training_count": len(training),
        "unseen_count": len(unseen),
        "timestamps": {"start": time.time()},
    }

    mech = kernel.distill_parameterized(training, mechanism_id=f"param-{condition_id}")

    if mech is None:
        result["distill_success"] = False
        result["error"] = "distill_parameterized returned None"
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

    result["slot_count_expected"] = expected_slot_count
    result["slot_count_met"] = result["slot_count"] >= expected_slot_count
    result["slot_names_distinct"] = len(mech.parameter_slots) == len(set(mech.parameter_slots))

    reg.upsert(mech)

    resolution_results = []
    for params in unseen:
        # Map spec param names to slot names
        slot_to_param = {}
        for slot in mech.parameter_slots:
            for k, v in params.items():
                if k == slot or slot in k or k in slot:
                    slot_to_param[slot] = v
                    break

        if len(slot_to_param) < len(mech.parameter_slots):
            unmatched_slots = [s for s in mech.parameter_slots if s not in slot_to_param]
            unmatched_params = {k: v for k, v in params.items() if v not in slot_to_param.values()}
            for slot, val in zip(unmatched_slots, unmatched_params.values()):
                slot_to_param[slot] = val

        start = time.perf_counter()
        resolution = kernel.resolve(
            mech.intent,
            dict(SHARED_STATE),
            params=slot_to_param,
        )
        elapsed = time.perf_counter() - start

        expected_binding = expected_fn(params)
        binding_ok, binding_msg = _check_bound_action(expected_binding, resolution.bound_action)

        resolution_results.append({
            "params": params,
            "resolve_params": slot_to_param,
            "status": resolution.status.value,
            "mechanism_id": resolution.mechanism_id,
            "bound_action": resolution.bound_action,
            "reason": resolution.reason,
            "confidence": resolution.confidence,
            "elapsed_seconds": elapsed,
            "binding_correct": binding_ok,
            "binding_detail": binding_msg if not binding_ok else "ok",
            "has_unsubstituted_template": _has_unsubstituted(resolution.bound_action),
        })

    result["resolution_results"] = resolution_results

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


# ═══════════════════════════════════════════════════════════════════════════════
# Main experiment
# ═══════════════════════════════════════════════════════════════════════════════

def run_experiment():
    print("=" * 70)
    print("EXP-PRODUCT-33974562602: Kernel Integration of Multi-Parameter Induction")
    print("=" * 70)

    raw_evidence = {
        "experiment_id": "EXP-PRODUCT-33974562602",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "phase_a": {},
        "conditions": {},
        "controls": {},
        "baselines": {},
        "induction_audit": {},
        "decision": {},
    }

    # ─── Phase A: Kernel Integration Verification ────────────────────────
    print(f"\n{'─'*60}")
    print("  Phase A: Kernel Integration Verification")
    print(f"{'─'*60}")

    try:
        from spider.kernel import SpiderKernel as SK, _extract_varying_values_multi, _deep_get, _deep_set
        raw_evidence["phase_a"]["import_ok"] = True
        print("  [✓] Import successful")
    except Exception as e:
        raw_evidence["phase_a"]["import_ok"] = False
        raw_evidence["phase_a"]["import_error"] = str(e)
        print(f"  [✗] Import failed: {e}")
        return raw_evidence

    # Check method exists
    has_method = hasattr(SK, 'distill_parameterized')
    raw_evidence["phase_a"]["method_exists"] = has_method
    print(f"  [{'✓' if has_method else '✗'}] distill_parameterized method exists")

    # Run existing unit tests
    import subprocess
    test_result = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_kernel", "-v"],
        capture_output=True, text=True,
        cwd=str(Path(__file__).parent.parent.parent.parent)
    )
    raw_evidence["phase_a"]["existing_tests_exit_code"] = test_result.returncode
    raw_evidence["phase_a"]["existing_tests_passed"] = test_result.returncode == 0
    print(f"  [{'✓' if test_result.returncode == 0 else '✗'}] Existing tests exit code: {test_result.returncode}")

    # ─── Phase B: Regression Baseline (B1-B5) ───────────────────────────
    print(f"\n{'='*70}")
    print("  Phase B: Regression Baseline (5 conditions)")
    print(f"{'='*70}")

    regression_conditions = [
        ("B1-single-path", b1_training, b1_unseen, b1_expected, 1),
        ("B2-path-and-body", b2_training, b2_unseen, b2_expected, 2),
        ("B3-path-body-headers", b3_training, b3_unseen, b3_expected, 3),
        ("B4-non-identifier-values", b4_training, b4_unseen, b4_expected, 1),
        ("B5-shared-slot-name", b5_training, b5_unseen, b5_expected, 2),
    ]

    for cond_id, train_fn, unseen_fn, expected_fn, exp_slots in regression_conditions:
        print(f"\n  Condition: {cond_id}")
        tmpdir, reg, kernel = _make_kernel_and_reg()
        training = train_fn()
        unseen = unseen_fn()
        result = run_condition(cond_id, training, unseen, expected_fn, exp_slots, kernel, reg)
        raw_evidence["conditions"][cond_id] = result

        if result.get("distill_success"):
            m = result["metrics"]
            print(f"    Slots: {result['slot_count']} (expected >= {exp_slots})")
            print(f"    Slot names: {result['parameter_slots']}")
            print(f"    Template: {json.dumps(result['action_template'])}")
            print(f"    Unseen resolution: {m['unseen_resolution_rate']:.1%} ({m['executable_count']}/{unseen.__len__()})")
            print(f"    Binding accuracy: {m['binding_accuracy']:.1%} ({m['binding_correct_count']}/{unseen.__len__()})")
        else:
            print(f"    FAILED: {result.get('error', 'unknown')}")

    # ─── Phase C: Full-Value Unseen Tests ────────────────────────────────
    print(f"\n{'='*70}")
    print("  Phase C: Full-Value Unseen Tests")
    print(f"{'='*70}")

    # C1: Full-value URLs (same training as B4)
    print(f"\n  Condition: C1-full-value-urls")
    tmpdir, reg, kernel = _make_kernel_and_reg()
    c1_training = b4_training()
    mech = kernel.distill_parameterized(c1_training, mechanism_id="param-C1-full-value")
    if mech:
        reg.upsert(mech)
        c1_results = []
        for params in c1_full_value_unseen():
            slot_to_param = {}
            for slot in mech.parameter_slots:
                for k, v in params.items():
                    if k == slot or slot in k or k in slot:
                        slot_to_param[slot] = v
                        break
            if len(slot_to_param) < len(mech.parameter_slots):
                unmatched_slots = [s for s in mech.parameter_slots if s not in slot_to_param]
                unmatched_params = {k: v for k, v in params.items() if v not in slot_to_param.values()}
                for slot, val in zip(unmatched_slots, unmatched_params.values()):
                    slot_to_param[slot] = val

            resolution = kernel.resolve(mech.intent, dict(SHARED_STATE), params=slot_to_param)
            expected_binding = c1_full_value_expected(params)
            binding_ok, binding_msg = _check_bound_action(expected_binding, resolution.bound_action)
            c1_results.append({
                "params": params,
                "resolve_params": slot_to_param,
                "status": resolution.status.value,
                "bound_action": resolution.bound_action,
                "binding_correct": binding_ok,
                "binding_detail": binding_msg if not binding_ok else "ok",
                "has_unsubstituted_template": _has_unsubstituted(resolution.bound_action),
            })

        exec_count = sum(1 for r in c1_results if r["status"] == "EXECUTABLE")
        bind_count = sum(1 for r in c1_results if r["binding_correct"])
        raw_evidence["conditions"]["C1-full-value-urls"] = {
            "condition_id": "C1-full-value-urls",
            "distill_success": True,
            "slot_count": len(mech.parameter_slots),
            "parameter_slots": mech.parameter_slots,
            "action_template": mech.action_template,
            "resolution_results": c1_results,
            "metrics": {
                "unseen_resolution_rate": exec_count / len(c1_results),
                "binding_accuracy": bind_count / len(c1_results),
                "executable_count": exec_count,
                "binding_correct_count": bind_count,
            },
        }
        print(f"    Slots: {mech.parameter_slots}")
        print(f"    Template: {json.dumps(mech.action_template)}")
        print(f"    Resolution: {exec_count}/{len(c1_results)}, Binding: {bind_count}/{len(c1_results)}")
        for r in c1_results:
            sym = "✓" if r["status"] == "EXECUTABLE" and r["binding_correct"] else "✗"
            print(f"      [{sym}] {r['params']} -> {r['status']} binding={'ok' if r['binding_correct'] else r['binding_detail']}")
            print(f"          bound_action: {r['bound_action']}")
    else:
        raw_evidence["conditions"]["C1-full-value-urls"] = {"distill_success": False, "error": "distill returned None"}
        print("    FAILED: distill returned None")

    # C2: Full-value IDs with prefix
    print(f"\n  Condition: C2-full-value-ids")
    tmpdir, reg, kernel = _make_kernel_and_reg()
    c2_train = c2_full_value_training()
    mech = kernel.distill_parameterized(c2_train, mechanism_id="param-C2-full-value")
    if mech:
        reg.upsert(mech)
        c2_results = []
        for params in c2_full_value_unseen():
            slot_to_param = {}
            for slot in mech.parameter_slots:
                for k, v in params.items():
                    if k == slot or slot in k or k in slot:
                        slot_to_param[slot] = v
                        break
            if len(slot_to_param) < len(mech.parameter_slots):
                unmatched_slots = [s for s in mech.parameter_slots if s not in slot_to_param]
                unmatched_params = {k: v for k, v in params.items() if v not in slot_to_param.values()}
                for slot, val in zip(unmatched_slots, unmatched_params.values()):
                    slot_to_param[slot] = val

            resolution = kernel.resolve(mech.intent, dict(SHARED_STATE), params=slot_to_param)
            expected_binding = c2_full_value_expected(params)
            binding_ok, binding_msg = _check_bound_action(expected_binding, resolution.bound_action)
            c2_results.append({
                "params": params,
                "resolve_params": slot_to_param,
                "status": resolution.status.value,
                "bound_action": resolution.bound_action,
                "binding_correct": binding_ok,
                "binding_detail": binding_msg if not binding_ok else "ok",
                "has_unsubstituted_template": _has_unsubstituted(resolution.bound_action),
            })

        exec_count = sum(1 for r in c2_results if r["status"] == "EXECUTABLE")
        bind_count = sum(1 for r in c2_results if r["binding_correct"])
        raw_evidence["conditions"]["C2-full-value-ids"] = {
            "condition_id": "C2-full-value-ids",
            "distill_success": True,
            "slot_count": len(mech.parameter_slots),
            "parameter_slots": mech.parameter_slots,
            "action_template": mech.action_template,
            "resolution_results": c2_results,
            "metrics": {
                "unseen_resolution_rate": exec_count / len(c2_results),
                "binding_accuracy": bind_count / len(c2_results),
                "executable_count": exec_count,
                "binding_correct_count": bind_count,
            },
        }
        print(f"    Slots: {mech.parameter_slots}")
        print(f"    Template: {json.dumps(mech.action_template)}")
        print(f"    Resolution: {exec_count}/{len(c2_results)}, Binding: {bind_count}/{len(c2_results)}")
        for r in c2_results:
            sym = "✓" if r["status"] == "EXECUTABLE" and r["binding_correct"] else "✗"
            print(f"      [{sym}] {r['params']} -> {r['status']} binding={'ok' if r['binding_correct'] else r['binding_detail']}")
            print(f"          bound_action: {r['bound_action']}")
    else:
        raw_evidence["conditions"]["C2-full-value-ids"] = {"distill_success": False, "error": "distill returned None"}
        print("    FAILED: distill returned None")

    # ─── Phase D: Noisy Browser-Like Observations ────────────────────────
    print(f"\n{'='*70}")
    print("  Phase D: Noisy Browser-Like Observations")
    print(f"{'='*70}")

    noisy_conditions = [
        ("D1-noisy-post", d1_noisy_training, d1_noisy_unseen, d1_noisy_expected, 3),
        ("D2-noisy-get", d2_noisy_training, d2_noisy_unseen, d2_noisy_expected, 2),
        ("D3-noisy-multi-step", d3_noisy_training, d3_noisy_unseen, d3_noisy_expected, 1),
    ]

    for cond_id, train_fn, unseen_fn, expected_fn, exp_slots in noisy_conditions:
        print(f"\n  Condition: {cond_id}")
        tmpdir, reg, kernel = _make_kernel_and_reg()
        training = train_fn()
        unseen = unseen_fn()
        result = run_condition(cond_id, training, unseen, expected_fn, exp_slots, kernel, reg)
        raw_evidence["conditions"][cond_id] = result

        if result.get("distill_success"):
            m = result["metrics"]
            print(f"    Slots: {result['slot_count']} (expected >= {exp_slots})")
            print(f"    Slot names: {result['parameter_slots']}")
            print(f"    Template: {json.dumps(result['action_template'])}")
            print(f"    Unseen resolution: {m['unseen_resolution_rate']:.1%} ({m['executable_count']}/{len(unseen)})")
            print(f"    Binding accuracy: {m['binding_accuracy']:.1%} ({m['binding_correct_count']}/{len(unseen)})")
            for r in result["resolution_results"]:
                sym = "✓" if r["status"] == "EXECUTABLE" and r["binding_correct"] else "✗"
                print(f"      [{sym}] {r['params']} -> {r['status']} binding={'ok' if r['binding_correct'] else r['binding_detail']}")
        else:
            print(f"    FAILED: {result.get('error', 'unknown')}")

    # ─── Phase E: Null Control (Pattern Absence) ─────────────────────────
    print(f"\n{'='*70}")
    print("  Phase E: Null Control (Pattern Absence)")
    print(f"{'='*70}")

    # E1: Unrelated observations
    print(f"\n  Condition: E1-unrelated-structures")
    tmpdir, reg, kernel = _make_kernel_and_reg()
    e1_training = e1_null_training()
    e1_mech = kernel.distill_parameterized(e1_training, mechanism_id="param-E1-null")

    if e1_mech is None:
        raw_evidence["controls"]["E1_pattern_absence"] = {
            "description": "Unrelated observations produce no parameterized mechanism",
            "expected": "no mechanism (None)",
            "observed": "None",
            "passed": True,
            "slot_count": 0,
        }
        print("  [✓] No mechanism induced (correct: no pattern to find)")
    else:
        # Check slot count
        resolution = kernel.resolve(e1_mech.intent, dict(SHARED_STATE), params={})
        raw_evidence["controls"]["E1_pattern_absence"] = {
            "description": "Unrelated observations produce no parameterized mechanism",
            "expected": "slot_count=0",
            "observed": f"slot_count={len(e1_mech.parameter_slots)}",
            "slots": e1_mech.parameter_slots,
            "template": e1_mech.action_template,
            "resolution_status": resolution.status.value,
            "passed": len(e1_mech.parameter_slots) == 0,
        }
        sym = "✓" if len(e1_mech.parameter_slots) == 0 else "✗"
        print(f"  [{sym}] Mechanism induced with {len(e1_mech.parameter_slots)} slots (expected 0)")
        print(f"    Slots: {e1_mech.parameter_slots}")

    # E2: Single observation
    print(f"\n  Condition: E2-single-observation")
    tmpdir, reg, kernel = _make_kernel_and_reg()
    e2_training = e2_single_obs()
    e2_mech = kernel.distill_parameterized(e2_training, mechanism_id="param-E2-single")

    if e2_mech is None:
        raw_evidence["controls"]["E2_single_obs"] = {
            "description": "Single observation produces no parameterized mechanism",
            "expected": "no mechanism (None)",
            "observed": "None",
            "passed": True,
            "slot_count": 0,
        }
        print("  [✓] No mechanism induced (correct: need at least 2 observations)")
    else:
        raw_evidence["controls"]["E2_single_obs"] = {
            "description": "Single observation produces no parameterized mechanism",
            "expected": "slot_count=0",
            "observed": f"slot_count={len(e2_mech.parameter_slots)}",
            "slots": e2_mech.parameter_slots,
            "passed": len(e2_mech.parameter_slots) == 0,
        }
        sym = "✓" if len(e2_mech.parameter_slots) == 0 else "✗"
        print(f"  [{sym}] Mechanism induced with {len(e2_mech.parameter_slots)} slots (expected 0)")

    # ─── Baseline: B_LITERAL ─────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print("  Baseline B_LITERAL: Literal replay on unseen")
    print(f"{'─'*60}")

    tmpdir, reg, kernel = _make_kernel_and_reg()
    obs = b2_training()[0]
    lit_mech = kernel.distill(obs)
    if lit_mech:
        lit_mech.mechanism_id = "literal-baseline"
        reg.upsert(lit_mech)

        b_literal_results = []
        for params in b2_unseen():
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
        raw_evidence["baselines"]["B_LITERAL"] = {"description": "Literal distillation failed"}

    # ─── Baseline: B_RANDOM_INDUCTION ────────────────────────────────────
    print(f"\n{'─'*60}")
    print("  Baseline B_RANDOM_INDUCTION: Random slot naming")
    print(f"{'─'*60}")

    tmpdir, reg, kernel = _make_kernel_and_reg()
    training = b2_training()
    mech = kernel.distill_parameterized(training, mechanism_id="param-random")
    if mech:
        original_slots = list(mech.parameter_slots)
        randomized_slots = [f"rand_{i}" for i in range(len(original_slots))]

        template_str = json.dumps(mech.action_template)
        for orig, rand in zip(original_slots, randomized_slots):
            template_str = template_str.replace(f"${{{orig}}}", f"${{{rand}}}")
        mech.action_template = json.loads(template_str)
        mech.parameter_slots = randomized_slots

        reg.upsert(mech)

        b_random_results = []
        for params in b2_unseen():
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
        raw_evidence["baselines"]["B_RANDOM_INDUCTION"] = {"description": "Induction failed"}

    # ─── Induction Audit ─────────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print("  Induction Audit")
    print(f"{'─'*60}")

    audit_conditions = [
        ("B1-single-path", b1_training, 1),
        ("B2-path-and-body", b2_training, 2),
        ("B3-path-body-headers", b3_training, 3),
        ("B4-non-identifier-values", b4_training, 1),
        ("B5-shared-slot-name", b5_training, 2),
    ]

    audit_results = {}
    for cond_id, train_fn, exp_slots in audit_conditions:
        training = train_fn()
        tmpdir, reg, kernel = _make_kernel_and_reg()
        mech = kernel.distill_parameterized(training, mechanism_id=f"audit-{cond_id}")
        if mech:
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
            audit_results[cond_id] = {"slot_count": 0, "error": "induction failed"}

    raw_evidence["induction_audit"] = audit_results

    # ─── Decision Rule ───────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("DECISION")
    print(f"{'='*70}")

    decision_checks = {}

    # Check 1: Kernel integration completed
    decision_checks["A1_kernel_integration"] = (
        raw_evidence["phase_a"].get("import_ok", False)
        and raw_evidence["phase_a"].get("method_exists", False)
        and raw_evidence["phase_a"].get("existing_tests_passed", False)
    )

    # Check 2: B1 regression
    b1r = raw_evidence["conditions"].get("B1-single-path", {})
    b1m = b1r.get("metrics", {})
    decision_checks["B1_regression"] = (
        b1r.get("slot_count", 0) >= 1
        and b1r.get("slot_names_distinct", False)
        and b1m.get("unseen_resolution_rate", 0) == 1.0
        and b1m.get("binding_accuracy", 0) == 1.0
    )

    # Check 3: B2 multi-param
    b2r = raw_evidence["conditions"].get("B2-path-and-body", {})
    b2m = b2r.get("metrics", {})
    decision_checks["B2_multi_param"] = (
        b2r.get("slot_count", 0) >= 2
        and b2r.get("slot_names_distinct", False)
        and b2m.get("unseen_resolution_rate", 0) == 1.0
        and b2m.get("binding_accuracy", 0) == 1.0
    )

    # Check 4: B3 three-param
    b3r = raw_evidence["conditions"].get("B3-path-body-headers", {})
    b3m = b3r.get("metrics", {})
    decision_checks["B3_three_param"] = (
        b3r.get("slot_count", 0) >= 3
        and b3r.get("slot_names_distinct", False)
        and b3m.get("unseen_resolution_rate", 0) == 1.0
        and b3m.get("binding_accuracy", 0) == 1.0
    )

    # Check 5: B4 non-identifier
    b4r = raw_evidence["conditions"].get("B4-non-identifier-values", {})
    b4m = b4r.get("metrics", {})
    decision_checks["B4_non_identifier"] = (
        b4r.get("slot_count", 0) >= 1
        and b4m.get("unseen_resolution_rate", 0) == 1.0
        and b4m.get("binding_accuracy", 0) == 1.0
    )

    # Check 6: B5 shared-slot collision
    b5r = raw_evidence["conditions"].get("B5-shared-slot-name", {})
    b5m = b5r.get("metrics", {})
    decision_checks["B5_no_collision"] = (
        b5r.get("slot_count", 0) >= 2
        and b5r.get("slot_names_distinct", False)
        and b5m.get("unseen_resolution_rate", 0) == 1.0
        and b5m.get("binding_accuracy", 0) == 1.0
    )

    # Check 7: Full-value C1
    c1r = raw_evidence["conditions"].get("C1-full-value-urls", {})
    c1m = c1r.get("metrics", {})
    decision_checks["C1_full_value_resolution"] = (
        c1m.get("unseen_resolution_rate", 0) >= 0.9
        and c1m.get("binding_accuracy", 0) >= 0.9
    )

    # Check 8: Full-value C2
    c2r = raw_evidence["conditions"].get("C2-full-value-ids", {})
    c2m = c2r.get("metrics", {})
    decision_checks["C2_full_value_resolution"] = (
        c2m.get("unseen_resolution_rate", 0) >= 0.9
        and c2m.get("binding_accuracy", 0) >= 0.9
    )

    # Check 9-11: Noisy D1-D3
    for d_id in ["D1-noisy-post", "D2-noisy-get", "D3-noisy-multi-step"]:
        dr = raw_evidence["conditions"].get(d_id, {})
        dm = dr.get("metrics", {})
        decision_checks[f"{d_id}_resolution"] = (
            dm.get("unseen_resolution_rate", 0) >= 0.9
            and dm.get("binding_accuracy", 0) >= 0.9
        )

    # Check 12: Null control E1
    e1_ctrl = raw_evidence["controls"].get("E1_pattern_absence", {})
    decision_checks["E1_null_control"] = e1_ctrl.get("passed", False)

    # Check 13: Null control E2
    e2_ctrl = raw_evidence["controls"].get("E2_single_obs", {})
    decision_checks["E2_single_obs"] = e2_ctrl.get("passed", False)

    # Check 14: No crashes
    all_distilled = all(
        raw_evidence["conditions"][c].get("distill_success", False)
        for c in raw_evidence["conditions"]
        if "distill_success" in raw_evidence["conditions"][c]
    )
    decision_checks["no_crashes"] = all_distilled

    all_pass = all(decision_checks.values())
    verdict = "KERNEL-INTEGRATION-SURVIVES" if all_pass else "KERNEL-INTEGRATION-FALSIFIED"

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

    output_path = Path(__file__).parent / "raw_evidence.json"
    with open(output_path, "w") as f:
        json.dump(evidence, f, indent=2, default=str)

    print(f"\nRaw evidence written to: {output_path}")
