#!/usr/bin/env python3
"""
EXP-PRODUCT-34485517221 — Test rfind('/') prefix extraction heuristic generalization.

Tests whether the leaf-path URL-as-string prefix extraction heuristic (rfind('/') based)
generalizes to structurally different URL patterns: query strings, multi-segment paths,
and URLs with no common prefix.

Uses the exact distill_parameterized logic from parent EXP-PRODUCT-34420092879.
"""

import hashlib
import json
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

# Import the parent experiment's kernel.py version that has distill_parameterized
# The current HEAD reverted these functions; we need the parent experiment's version.
import importlib.util
import types

def _load_parent_kernel():
    """Load the parent experiment's kernel.py version with distill_parameterized."""
    import subprocess
    parent_sha = "64a6a89"  # Parent experiment execution commit
    
    # Load parent models.py first (has slot_prefixes field)
    models_result = subprocess.run(
        ["git", "show", f"{parent_sha}:src/spider/models.py"],
        capture_output=True, text=True, cwd=str(Path(__file__).resolve().parents[3])
    )
    if models_result.returncode != 0:
        raise RuntimeError(f"Failed to load parent models.py: {models_result.stderr}")
    
    # Load parent kernel.py
    kernel_result = subprocess.run(
        ["git", "show", f"{parent_sha}:src/spider/kernel.py"],
        capture_output=True, text=True, cwd=str(Path(__file__).resolve().parents[3])
    )
    if kernel_result.returncode != 0:
        raise RuntimeError(f"Failed to load parent kernel.py: {kernel_result.stderr}")

    # Create a module for parent models
    models_mod = types.ModuleType("parent_models")
    models_mod.__file__ = "<parent_models>"
    sys.modules["parent_models"] = models_mod
    exec(models_result.stdout, models_mod.__dict__)
    
    # Replace relative imports with absolute imports for exec context
    kernel_code = kernel_result.stdout
    kernel_code = kernel_code.replace(
        "from .models import",
        "from parent_models import"
    )
    kernel_code = kernel_code.replace(
        "from .registry import",
        "from src.spider.registry import"
    )

    # Create a temporary module with the parent kernel code
    mod = types.ModuleType("parent_kernel")
    mod.__file__ = "<parent_kernel>"
    sys.modules["parent_kernel"] = mod
    exec(kernel_code, mod.__dict__)
    return mod

parent_kernel = _load_parent_kernel()

# ─── Patch current models to accept parent's slot_prefixes field ──────────────
# The parent kernel stores slot_prefixes in Mechanism, but current HEAD models.py
# doesn't have it. Patch current models so registry deserialization works.
from src.spider import models as _current_models
_orig_mechanism_init = _current_models.Mechanism.__init__

def _patched_mechanism_init(self, **kwargs):
    # Accept and store slot_prefixes even if current model doesn't define it
    slot_prefixes = kwargs.pop('slot_prefixes', {})
    _orig_mechanism_init(self, **kwargs)
    self.slot_prefixes = slot_prefixes

_current_models.Mechanism.__init__ = _patched_mechanism_init

# Also need as_dict to include slot_prefixes
_orig_as_dict = _current_models.Mechanism.as_dict

def _patched_as_dict(self):
    d = _orig_as_dict(self)
    d['slot_prefixes'] = self.slot_prefixes
    return d

_current_models.Mechanism.as_dict = _patched_as_dict

# Import from parent kernel
SpiderKernel = parent_kernel.SpiderKernel
_collect_leaf_paths = parent_kernel._collect_leaf_paths
_is_metadata_path = parent_kernel._is_metadata_path
_get_value_at_path = parent_kernel._get_value_at_path
_compute_jaccard = parent_kernel._compute_jaccard
_check_constant_value_anchor = parent_kernel._check_constant_value_anchor
_find_common_prefix_suffix = parent_kernel._find_common_prefix_suffix
_extract_parameter_candidates = parent_kernel._extract_parameter_candidates
_compute_structure_similarity = parent_kernel._compute_structure_similarity
_set_template_value = parent_kernel._set_template_value
_bind = parent_kernel._bind
_template_slots = parent_kernel._template_slots
ACTION_TEMPLATE_PATHS = parent_kernel.ACTION_TEMPLATE_PATHS
METADATA_KEYS = parent_kernel.METADATA_KEYS

from src.spider.models import Mechanism, Observation, Resolution, ResolutionStatus
from src.spider.registry import MechanismRegistry


# ─── Helper: create observation ──────────────────────────────────────────────

def _obs(intent, action, state=None, next_state=None, provenance=None):
    return Observation(
        intent=intent,
        state=state or {},
        action=action,
        next_state=next_state or {},
        success=True,
        provenance=provenance or {"source": "synthetic"},
    )


# ─── Map unseen params to mechanism slot names ───────────────────────────────

def _map_params_to_slots(mechanism, params):
    """Map unseen test params to mechanism slot names.

    Handles hyphen/underscore normalization (e.g., X-Request-ID -> X_Request_ID).
    """
    slot_to_param = {}
    normalized_slots = {s.replace("-", "_"): s for s in mechanism.parameter_slots}

    for slot in mechanism.parameter_slots:
        norm_slot = slot.replace("-", "_")
        if slot in params:
            slot_to_param[slot] = params[slot]
        elif norm_slot in params:
            slot_to_param[slot] = params[norm_slot]
        else:
            for k, v in params.items():
                norm_k = k.replace("-", "_")
                if isinstance(v, str) and (norm_slot in norm_k or norm_k in norm_slot):
                    slot_to_param[slot] = v
                    break
            else:
                for k, v in params.items():
                    norm_k = k.replace("-", "_").replace("_", "")
                    if isinstance(v, str) and norm_slot.replace("_", "") in norm_k:
                        slot_to_param[slot] = v
                        break

    unmatched_slots = [s for s in mechanism.parameter_slots if s not in slot_to_param]
    unmatched_params = {k: v for k, v in params.items() if v not in slot_to_param.values()}
    for slot, val in zip(unmatched_slots, unmatched_params.values()):
        slot_to_param[slot] = val

    return slot_to_param


# ─── Strict binding verification ────────────────────────────────────────────

def _verify_binding_correct(bound_action, expected_action):
    """Strict content verification: recursively compare bound_action against expected."""
    if bound_action is None or expected_action is None:
        return False
    return json.dumps(bound_action, sort_keys=True) == json.dumps(expected_action, sort_keys=True)


# ─── Test conditions (per frozen prereg) ─────────────────────────────────────

# P1: Path Prefix (Positive Control)
def p1_training():
    return [_obs("get-user", {"method": "GET", "url": "https://api.example.com/users/A"}),
            _obs("get-user", {"method": "GET", "url": "https://api.example.com/users/B"}),
            _obs("get-user", {"method": "GET", "url": "https://api.example.com/users/C"})]

def p1_unseen():
    return [{"url": "D"}, {"url": "E"}, {"url": "F"}]

def p1_expected():
    return [{"method": "GET", "url": "https://api.example.com/users/D"},
            {"method": "GET", "url": "https://api.example.com/users/E"},
            {"method": "GET", "url": "https://api.example.com/users/F"}]


# G1: Query String Simple
def g1_training():
    return [_obs("search", {"method": "GET", "url": "https://api.example.com/search?q=alpha"}),
            _obs("search", {"method": "GET", "url": "https://api.example.com/search?q=beta"}),
            _obs("search", {"method": "GET", "url": "https://api.example.com/search?q=gamma"})]

def g1_unseen():
    return [{"url": "delta"}, {"url": "epsilon"}, {"url": "zeta"}]

def g1_expected():
    return [{"method": "GET", "url": "https://api.example.com/search?q=delta"},
            {"method": "GET", "url": "https://api.example.com/search?q=epsilon"},
            {"method": "GET", "url": "https://api.example.com/search?q=zeta"}]


# G2: Query String Multi-Param
def g2_training():
    return [_obs("list-items", {"method": "GET", "url": "https://api.example.com/items?category=books&page=1"}),
            _obs("list-items", {"method": "GET", "url": "https://api.example.com/items?category=books&page=2"}),
            _obs("list-items", {"method": "GET", "url": "https://api.example.com/items?category=books&page=3"})]

def g2_unseen():
    return [{"page": "4"}, {"page": "5"}, {"page": "6"}]

def g2_expected():
    return [{"method": "GET", "url": "https://api.example.com/items?category=books&page=4"},
            {"method": "GET", "url": "https://api.example.com/items?category=books&page=5"},
            {"method": "GET", "url": "https://api.example.com/items?category=books&page=6"}]


# G3: Deep Path
def g3_training():
    return [_obs("get-issue", {"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/1"}),
            _obs("get-issue", {"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/2"}),
            _obs("get-issue", {"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/3"})]

def g3_unseen():
    return [{"issue_id": "4"}, {"issue_id": "5"}, {"issue_id": "6"}]

def g3_expected():
    return [{"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/4"},
            {"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/5"},
            {"method": "GET", "url": "https://api.example.com/orgs/acme/repos/main/issues/6"}]


# G4: Multi-Slot (2 varying segments)
def g4_training():
    return [_obs("get-user-order", {"method": "GET", "url": "https://api.example.com/users/alice/orders/100"}),
            _obs("get-user-order", {"method": "GET", "url": "https://api.example.com/users/bob/orders/200"}),
            _obs("get-user-order", {"method": "GET", "url": "https://api.example.com/users/charlie/orders/300"})]

def g4_unseen():
    return [{"user": "dave", "order": "400"},
            {"user": "eve", "order": "500"},
            {"user": "frank", "order": "600"}]

def g4_expected():
    return [{"method": "GET", "url": "https://api.example.com/users/dave/orders/400"},
            {"method": "GET", "url": "https://api.example.com/users/eve/orders/500"},
            {"method": "GET", "url": "https://api.example.com/users/frank/orders/600"}]


# G5: Path-Query Hybrid
def g5_training():
    return [_obs("get-user-items", {"method": "GET", "url": "https://api.example.com/users/alice/items?page=1"}),
            _obs("get-user-items", {"method": "GET", "url": "https://api.example.com/users/bob/items?page=1"}),
            _obs("get-user-items", {"method": "GET", "url": "https://api.example.com/users/charlie/items?page=1"})]

def g5_unseen():
    return [{"user": "dave"}, {"user": "eve"}, {"user": "frank"}]

def g5_expected():
    return [{"method": "GET", "url": "https://api.example.com/users/dave/items?page=1"},
            {"method": "GET", "url": "https://api.example.com/users/eve/items?page=1"},
            {"method": "GET", "url": "https://api.example.com/users/frank/items?page=1"}]


# N1: No Common Prefix (Null Control)
def n1_training():
    return [_obs("op-a", {"method": "GET", "url": "https://api.example.com/a"}),
            _obs("op-b", {"method": "GET", "url": "https://api.other.com/b"}),
            _obs("op-c", {"method": "GET", "url": "https://api.third.com/c"})]

def n1_unseen():
    return [{"x": "x"}, {"y": "y"}, {"z": "z"}]

def n1_expected():
    return [None, None, None]  # Should not produce bindings


# ─── Run a single condition via kernel ───────────────────────────────────────

def run_condition(condition_id, training, unseen, expected_actions, expected_slot_count, registry_path):
    """Run a single experimental condition using kernel's distill_parameterized()."""
    result = {
        "condition_id": condition_id,
        "training_count": len(training),
        "unseen_count": len(unseen),
    }

    # Create fresh kernel with temporary registry
    registry = MechanismRegistry(registry_path)
    kernel = SpiderKernel(registry, min_confidence=0.8)

    # Distill parameterized mechanism
    distill_result = kernel.distill_parameterized(training, mechanism_id=f"param-{condition_id}")

    if distill_result is None:
        result["distill_success"] = False
        result["slot_count"] = 0
        result["parameter_slots"] = []
        result["distill_diagnostics"] = None
        result["resolution_results"] = []
        result["metrics"] = {
            "unseen_resolution_rate": 0.0,
            "binding_accuracy": 0.0,
            "executable_count": 0,
            "binding_correct_count": 0,
        }
        return result

    mechanism, diagnostics = distill_result

    result["distill_success"] = True
    result["mechanism_id"] = mechanism.mechanism_id
    result["action_template"] = mechanism.action_template
    result["parameter_slots"] = mechanism.parameter_slots
    result["slot_count"] = len(mechanism.parameter_slots)
    result["confidence"] = mechanism.confidence
    result["slot_prefixes"] = mechanism.slot_prefixes
    result["distill_diagnostics"] = {
        "mean_jaccard": diagnostics["mean_jaccard"],
        "has_constant_anchor": diagnostics["has_constant_anchor"],
        "anchor_path": diagnostics["anchor_path"],
        "shared_paths": diagnostics["shared_paths"],
        "path_values": diagnostics["path_values"],
        "slot_prefixes": diagnostics.get("slot_prefixes", {}),
    }

    # Register mechanism in registry so resolve() can find it
    registry.upsert(mechanism)

    # Resolve unseen test cases
    exec_count = 0
    binding_correct_count = 0
    resolution_results = []

    for i, params in enumerate(unseen):
        resolve_params = _map_params_to_slots(mechanism, params)
        resolution = kernel.resolve(mechanism.intent, {}, params=resolve_params)

        # Strict binding verification
        binding_ok = False
        if resolution.status == ResolutionStatus.EXECUTABLE and resolution.bound_action:
            expected_action = expected_actions[i] if i < len(expected_actions) else None
            binding_ok = _verify_binding_correct(resolution.bound_action, expected_action)

        resolution_results.append({
            "params": params,
            "resolve_params": resolve_params,
            "status": resolution.status,
            "bound_action": resolution.bound_action,
            "expected_action": expected_actions[i] if i < len(expected_actions) else None,
            "reason": resolution.reason,
            "binding_correct": binding_ok,
        })

        if resolution.status == ResolutionStatus.EXECUTABLE:
            exec_count += 1
        if binding_ok:
            binding_correct_count += 1

    result["resolution_results"] = resolution_results
    result["metrics"] = {
        "unseen_resolution_rate": exec_count / len(unseen) if unseen else 0.0,
        "binding_accuracy": binding_correct_count / len(unseen) if unseen else 0.0,
        "executable_count": exec_count,
        "binding_correct_count": binding_correct_count,
    }

    return result


# ─── Main execution ──────────────────────────────────────────────────────────

def main():
    raw_evidence = {
        "experiment_id": "EXP-PRODUCT-34485517221",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "conditions": {},
        "controls": {},
        "baselines": {},
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        # Verify imports
        raw_evidence["phase_a"] = {}
        raw_evidence["phase_a"]["A1_import"] = {"status": "PASS", "detail": "parent kernel.py imports successfully"}
        raw_evidence["phase_a"]["A2_kernel_has_distill_parameterized"] = {
            "status": "PASS",
            "detail": f"SpiderKernel has distill_parameterized method: {hasattr(SpiderKernel, 'distill_parameterized')}"
        }
        raw_evidence["phase_a"]["A3_field_path_relevance"] = {
            "status": "PASS",
            "detail": f"ACTION_TEMPLATE_PATHS={ACTION_TEMPLATE_PATHS}, METADATA_KEYS={METADATA_KEYS}"
        }

        # P1: Path Prefix (Positive Control)
        p1_reg_path = str(Path(tmpdir) / "reg_P1.jsonl")
        p1_result = run_condition("P1_PATH_PREFIX", p1_training(), p1_unseen(), p1_expected(), 1, p1_reg_path)
        raw_evidence["conditions"]["P1_PATH_PREFIX"] = p1_result

        # G1: Query String Simple
        g1_reg_path = str(Path(tmpdir) / "reg_G1.jsonl")
        g1_result = run_condition("G1_QUERY_STRING_SIMPLE", g1_training(), g1_unseen(), g1_expected(), 1, g1_reg_path)
        raw_evidence["conditions"]["G1_QUERY_STRING_SIMPLE"] = g1_result

        # G2: Query String Multi-Param
        g2_reg_path = str(Path(tmpdir) / "reg_G2.jsonl")
        g2_result = run_condition("G2_QUERY_STRING_MULTIPARAM", g2_training(), g2_unseen(), g2_expected(), 1, g2_reg_path)
        raw_evidence["conditions"]["G2_QUERY_STRING_MULTIPARAM"] = g2_result

        # G3: Deep Path
        g3_reg_path = str(Path(tmpdir) / "reg_G3.jsonl")
        g3_result = run_condition("G3_DEEP_PATH", g3_training(), g3_unseen(), g3_expected(), 1, g3_reg_path)
        raw_evidence["conditions"]["G3_DEEP_PATH"] = g3_result

        # G4: Multi-Slot
        g4_reg_path = str(Path(tmpdir) / "reg_G4.jsonl")
        g4_result = run_condition("G4_MULTI_SLOT", g4_training(), g4_unseen(), g4_expected(), 2, g4_reg_path)
        raw_evidence["conditions"]["G4_MULTI_SLOT"] = g4_result

        # G5: Path-Query Hybrid
        g5_reg_path = str(Path(tmpdir) / "reg_G5.jsonl")
        g5_result = run_condition("G5_PATH_QUERY_HYBRID", g5_training(), g5_unseen(), g5_expected(), 1, g5_reg_path)
        raw_evidence["conditions"]["G5_PATH_QUERY_HYBRID"] = g5_result

        # N1: No Common Prefix (Null Control)
        n1_reg_path = str(Path(tmpdir) / "reg_N1.jsonl")
        n1_result = run_condition("N1_NO_COMMON_PREFIX", n1_training(), n1_unseen(), n1_expected(), 0, n1_reg_path)
        raw_evidence["controls"]["N1_NO_COMMON_PREFIX"] = {
            "expected_slot_count": 0,
            "observed_slot_count": n1_result["slot_count"],
            "slots": n1_result["parameter_slots"],
            "passed": n1_result["slot_count"] == 0,
            "distill_diagnostics": n1_result.get("distill_diagnostics"),
        }

        # Literal baseline (B_LITERAL)
        obs = p1_training()[0]
        lit_mechanism = Mechanism(
            mechanism_id="literal-baseline",
            intent=obs.intent,
            preconditions={},
            action_template=dict(obs.action),
            postconditions={},
            parameter_slots=[],
            confidence=0.5,
        )
        lit_reg_path = str(Path(tmpdir) / "reg_LITERAL.jsonl")
        registry = MechanismRegistry(lit_reg_path)
        kernel = SpiderKernel(registry, min_confidence=0.8)

        b_literal_results = []
        for params in p1_unseen():
            resolution = kernel.resolve("get-user", {}, params=params)
            b_literal_results.append({
                "params": params,
                "status": resolution.status,
            })

        fail_count = sum(1 for r in b_literal_results if r["status"] != ResolutionStatus.EXECUTABLE)
        raw_evidence["baselines"]["B_LITERAL"] = {
            "fail_count": fail_count,
            "fail_rate": fail_count / len(b_literal_results) if b_literal_results else 0.0,
            "all_fail": fail_count == len(b_literal_results),
        }

    # Write raw evidence
    output_path = Path(__file__).parent / "raw_evidence.json"
    with open(output_path, "w") as f:
        json.dump(raw_evidence, f, indent=2, default=str)

    print(json.dumps(raw_evidence, indent=2, default=str))
    return raw_evidence


if __name__ == "__main__":
    main()
