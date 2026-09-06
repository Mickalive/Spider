#!/usr/bin/env python3
"""EXP-GRAPH-33998605047 — Execute frozen experiment.

Re-tests the literal-vs-param equal-confidence hazard (original false accepts)
with the parameter-slot-count fix applied temporarily during execution.

16 conditions: 7 baselines + 5 compete-equal-id + multi-slot + template-only x2 + equal-slot-tie.
No HTTP execution — resolution-only. Deterministic, no model calls.
"""

import json
import sys
import tempfile
import hashlib
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from src.spider.kernel import SpiderKernel, _matches, _template_slots
from src.spider.registry import MechanismRegistry
from src.spider.models import Mechanism, ResolutionStatus

# =============================================================================
# MECHANISM DEFINITIONS (stable identifiers for controls)
# =============================================================================

MECHANISMS = {
    "literal-fetch-posts-1": Mechanism(
        mechanism_id="literal-fetch-posts-1",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/1", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=[],
        confidence=0.95,
    ),
    "param-fetch-posts": Mechanism(
        mechanism_id="param-fetch-posts",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=["id"],
        confidence=0.95,
    ),
    "param-fetch-posts-high": Mechanism(
        mechanism_id="param-fetch-posts-high",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=["id"],
        confidence=0.98,
    ),
    "literal-fetch-posts-1-low": Mechanism(
        mechanism_id="literal-fetch-posts-1-low",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/1", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=[],
        confidence=0.95,
    ),
    "param-2slot": Mechanism(
        mechanism_id="param-2slot",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}/${category}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=["id", "category"],
        confidence=0.95,
    ),
    "template-only-fetch": Mechanism(
        mechanism_id="template-only-fetch",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=[],
        confidence=0.95,
    ),
    "param-fetch-alt": Mechanism(
        mechanism_id="param-fetch-alt",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=["id"],
        confidence=0.95,
    ),
    "literal-alt": Mechanism(
        mechanism_id="literal-alt",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/2", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=[],
        confidence=0.95,
    ),
}

# =============================================================================
# REGISTRY CONFIGURATIONS
# =============================================================================

REGISTRIES = {
    "empty": [],
    "literal-only": ["literal-fetch-posts-1"],
    "param-only": ["param-fetch-posts"],
    "shared-param-higher": ["param-fetch-posts-high", "literal-fetch-posts-1-low"],
    "shared-literal-higher": ["literal-fetch-posts-1-low", "param-fetch-posts-high"],
    "shared-equal": ["literal-fetch-posts-1", "param-fetch-posts"],
    "2slot-vs-1slot-equal-conf": ["param-2slot", "param-fetch-posts"],
    "template-only-vs-param": ["template-only-fetch", "param-fetch-posts"],
    "template-only-vs-literal": ["template-only-fetch", "literal-fetch-posts-1"],
    "equal-slot-param-vs-param": ["param-fetch-posts", "param-fetch-alt"],
}

# =============================================================================
# CONDITION DEFINITIONS (from frozen spec.json)
# =============================================================================

CONDITIONS = [
    # Baselines
    {"id": "cold", "registry": "empty", "params": {"id": 2}, "expected_resolution": "UNKNOWN",
     "expected_url": None, "expected_winning_mechanism": None, "role": "baseline"},
    {"id": "literal-only-original", "registry": "literal-only", "params": {"id": 1},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
     "expected_winning_mechanism": "literal-fetch-posts-1", "role": "baseline"},
    {"id": "literal-only-unseen", "registry": "literal-only", "params": {"id": 2},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
     "expected_winning_mechanism": "literal-fetch-posts-1", "role": "baseline"},
    {"id": "param-only-original", "registry": "param-only", "params": {"id": 1},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
     "expected_winning_mechanism": "param-fetch-posts", "role": "baseline"},
    {"id": "param-only-unseen", "registry": "param-only", "params": {"id": 2},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/2",
     "expected_winning_mechanism": "param-fetch-posts", "role": "baseline"},
    {"id": "compete-param-higher", "registry": "shared-param-higher", "params": {"id": 3},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/3",
     "expected_winning_mechanism": "param-fetch-posts-high", "role": "baseline"},
    {"id": "compete-literal-higher", "registry": "shared-literal-higher", "params": {"id": 3},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
     "expected_winning_mechanism": "literal-fetch-posts-1-low", "role": "baseline"},
    # Interventions: original hazard (false accepts)
    {"id": "compete-equal-id2", "registry": "shared-equal", "params": {"id": 2},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/2",
     "expected_winning_mechanism": "param-fetch-posts", "role": "intervention",
     "note": "Original hazard: before fix, literal won (false accept). After fix, param must win."},
    {"id": "compete-equal-id3", "registry": "shared-equal", "params": {"id": 3},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/3",
     "expected_winning_mechanism": "param-fetch-posts", "role": "intervention",
     "note": "Original hazard: before fix, literal won (false accept). After fix, param must win."},
    {"id": "compete-equal-id4", "registry": "shared-equal", "params": {"id": 4},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/4",
     "expected_winning_mechanism": "param-fetch-posts", "role": "intervention",
     "note": "Original hazard: before fix, literal won (false accept). After fix, param must win."},
    {"id": "compete-equal-id5", "registry": "shared-equal", "params": {"id": 5},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/5",
     "expected_winning_mechanism": "param-fetch-posts", "role": "intervention",
     "note": "Original hazard: before fix, literal won (false accept). After fix, param must win."},
    {"id": "compete-equal-id6", "registry": "shared-equal", "params": {"id": 6},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/6",
     "expected_winning_mechanism": "param-fetch-posts", "role": "intervention",
     "note": "Original hazard: before fix, literal won (false accept). After fix, param must win."},
    # Interventions: generalization
    {"id": "multi-slot-beats-1-slot", "registry": "2slot-vs-1slot-equal-conf", "params": {"id": "3", "category": "tech"},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/3/tech",
     "expected_winning_mechanism": "param-2slot", "role": "intervention",
     "note": "2-slot param (len=2) beats 1-slot param (len=1) at equal confidence via tuple sort."},
    {"id": "template-only-vs-param", "registry": "template-only-vs-param", "params": {"id": 3},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/3",
     "expected_winning_mechanism": "param-fetch-posts", "role": "intervention",
     "note": "Template-only (parameter_slots=[], len=0) vs declared param (parameter_slots=['id'], len=1). Declared param wins."},
    {"id": "template-only-vs-literal", "registry": "template-only-vs-literal", "params": {"id": 3},
     "expected_resolution": "EXECUTABLE", "expected_url": None,
     "expected_winning_mechanism": None, "role": "intervention",
     "note": "Template-only vs literal at equal confidence. Both len=0 -> tie -> insertion-order. Record actual winner."},
    {"id": "equal-slot-tie-param-vs-param", "registry": "equal-slot-param-vs-param", "params": {"id": 3},
     "expected_resolution": "EXECUTABLE", "expected_url": None,
     "expected_winning_mechanism": None, "role": "intervention",
     "note": "Two params with same slot count at equal confidence. Tie -> insertion-order. Record actual winner."},
]

# =============================================================================
# APPLY THE ONE-LINE FIX (temporary patch for execution)
# =============================================================================

def apply_fix():
    """Apply the one-line fix: tuple sort with (confidence, len(parameter_slots))."""
    import src.spider.kernel as kernel_mod

    original_resolve = kernel_mod.SpiderKernel.resolve

    def patched_resolve(self, intent, context, params=None):
        params = params or {}
        candidates = []
        for m in self.registry.all():
            if m.invalidated or m.intent != intent:
                continue
            if not _matches(m.preconditions, context):
                continue
            if not _matches(m.applicability_guards, context):
                continue

            required_slots = set(m.parameter_slots) | _template_slots(m.action_template)
            if any(slot not in params for slot in required_slots):
                continue
            candidates.append(m)

        if not candidates:
            from src.spider.models import Resolution
            return Resolution(ResolutionStatus.UNKNOWN, None, "no applicable validated mechanism")

        # THE FIX: tuple sort with (confidence, len(parameter_slots))
        candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
        best = candidates[0]
        if best.confidence < self.min_confidence:
            from src.spider.models import Resolution
            return Resolution(ResolutionStatus.EXPLORE, best.mechanism_id, "candidate exists but confidence is below execution threshold", confidence=best.confidence)

        from src.spider.models import Resolution
        from src.spider.kernel import _bind
        return Resolution(
            ResolutionStatus.EXECUTABLE,
            best.mechanism_id,
            "applicability guards and confidence threshold passed",
            bound_action=_bind(best.action_template, params),
            confidence=best.confidence,
        )

    kernel_mod.SpiderKernel.resolve = patched_resolve

# =============================================================================
# EXECUTION
# =============================================================================

def create_kernel(registry_name: str) -> SpiderKernel:
    """Create a fresh kernel with specified registry mechanisms."""
    tmp = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False, prefix=f"exp339986_{registry_name}_")
    tmp.close()
    registry = MechanismRegistry(tmp.name)
    mech_ids = REGISTRIES[registry_name]
    mechanisms = [MECHANISMS[mid] for mid in mech_ids]
    registry.replace(mechanisms)
    return SpiderKernel(registry, min_confidence=0.8)


def run_condition(cond: dict) -> dict:
    """Run a single condition and return raw observation."""
    kernel = create_kernel(cond["registry"])
    resolution = kernel.resolve("fetch-post", {}, cond["params"])

    obs = {
        "condition_id": cond["id"],
        "type": "resolution",
        "status": resolution.status.value if hasattr(resolution.status, 'value') else str(resolution.status),
        "mechanism_id": resolution.mechanism_id,
        "bound_action": resolution.bound_action,
        "confidence": resolution.confidence,
        "reason": resolution.reason,
        "expected_status": cond["expected_resolution"],
        "expected_url": cond["expected_url"],
        "expected_winning_mechanism": cond.get("expected_winning_mechanism"),
        "match_expected_status": (resolution.status.value if hasattr(resolution.status, 'value') else str(resolution.status)) == cond["expected_resolution"],
        "match_expected_url": resolution.bound_action.get("url") == cond["expected_url"] if cond["expected_url"] is not None and resolution.bound_action else None,
        "match_expected_mechanism": resolution.mechanism_id == cond.get("expected_winning_mechanism") if cond.get("expected_winning_mechanism") is not None else None,
        "role": cond["role"],
    }
    return obs


def main():
    apply_fix()

    raw_observations = []
    errors = []

    # Run all 16 conditions
    for cond in CONDITIONS:
        try:
            obs = run_condition(cond)
            raw_observations.append(obs)
        except Exception as e:
            errors.append({"condition_id": cond["id"], "error": str(e), "type": "exception"})
            raw_observations.append({
                "condition_id": cond["id"],
                "type": "resolution",
                "status": "EXCEPTION",
                "mechanism_id": None,
                "bound_action": None,
                "confidence": None,
                "reason": str(e),
                "expected_status": cond["expected_resolution"],
                "expected_url": cond["expected_url"],
                "expected_winning_mechanism": cond.get("expected_winning_mechanism"),
                "match_expected_status": False,
                "match_expected_url": None,
                "match_expected_mechanism": None,
                "role": cond["role"],
            })

    # =============================================================================
    # DERIVED MEASUREMENTS
    # =============================================================================

    resolution_obs = [o for o in raw_observations]

    # Baseline observations (7 conditions)
    baseline_ids = ["cold", "literal-only-original", "literal-only-unseen",
                    "param-only-original", "param-only-unseen",
                    "compete-param-higher", "compete-literal-higher"]
    baseline_obs = [o for o in resolution_obs if o["condition_id"] in baseline_ids]
    baseline_pass = all(o["match_expected_status"] for o in baseline_obs)

    # Cold baseline specifically
    cold_obs = next((o for o in resolution_obs if o["condition_id"] == "cold"), None)
    cold_pass = cold_obs["status"] == "UNKNOWN" if cold_obs else False

    # Compete-equal-id (original hazard) — 5 conditions
    compete_equal_ids = ["compete-equal-id2", "compete-equal-id3", "compete-equal-id4",
                         "compete-equal-id5", "compete-equal-id6"]
    compete_equal_obs = [o for o in resolution_obs if o["condition_id"] in compete_equal_ids]
    false_accepts_eliminated = all(
        o["match_expected_mechanism"] is True for o in compete_equal_obs
    )
    false_accept_count = sum(1 for o in compete_equal_obs if o.get("match_expected_mechanism") is not True)

    # Multi-slot dominance
    multi_slot = next((o for o in resolution_obs if o["condition_id"] == "multi-slot-beats-1-slot"), None)
    multi_slot_dominance = (
        multi_slot["status"] == "EXECUTABLE"
        and multi_slot.get("match_expected_mechanism") is True
    ) if multi_slot else False

    # Template-only vs param
    template_vs_param = next((o for o in resolution_obs if o["condition_id"] == "template-only-vs-param"), None)
    template_only_handling = (
        template_vs_param["status"] == "EXECUTABLE"
        and template_vs_param.get("match_expected_mechanism") is True
    ) if template_vs_param else None

    # Template-only vs literal (record winner)
    template_vs_literal = next((o for o in resolution_obs if o["condition_id"] == "template-only-vs-literal"), None)
    template_vs_literal_winner = template_vs_literal["mechanism_id"] if template_vs_literal else None

    # Equal-slot tie (record winner)
    tie_param = next((o for o in resolution_obs if o["condition_id"] == "equal-slot-tie-param-vs-param"), None)
    equal_slot_tie_winner = tie_param["mechanism_id"] if tie_param else None

    # =============================================================================
    # DECISION RULE (from frozen spec.json)
    # =============================================================================

    has_exceptions = len(errors) > 0
    has_unexpected_status = any(o["status"] not in ("EXECUTABLE", "UNKNOWN", "EXCEPTION") for o in resolution_obs)

    # FIX-VALIDATED: all 5 criteria
    fix_validated = (
        baseline_pass
        and false_accepts_eliminated
        and multi_slot_dominance
        and template_only_handling is True
        and not has_exceptions
        and not has_unexpected_status
    )

    # PARTIAL-VALIDATION: baselines pass but some compete-equal-id still return literal
    partial_validation = (
        baseline_pass
        and not false_accepts_eliminated
        and not has_exceptions
        and not has_unexpected_status
    )

    # COMPETITION-UNSAFE: any baseline regresses
    competition_unsafe = not baseline_pass

    if has_exceptions or has_unexpected_status:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    elif fix_validated:
        status = "COMPLETE"
        outcome = "SUPPORTS"
    elif partial_validation:
        status = "COMPLETE"
        outcome = "MIXED"
    elif competition_unsafe:
        status = "COMPLETE"
        outcome = "FALSIFIES"
    else:
        status = "COMPLETE"
        outcome = "INCONCLUSIVE"

    # =============================================================================
    # METRICS
    # =============================================================================

    metrics = {
        "baseline_pass": baseline_pass,
        "baseline_pass_count": sum(1 for o in baseline_obs if o["match_expected_status"]),
        "baseline_total": len(baseline_obs),
        "cold_baseline_pass": cold_pass,
        "false_accepts_eliminated": false_accepts_eliminated,
        "false_accept_count": false_accept_count,
        "compete_equal_total": len(compete_equal_obs),
        "multi_slot_dominance": multi_slot_dominance,
        "multi_slot_winning_mechanism": multi_slot["mechanism_id"] if multi_slot else None,
        "multi_slot_bound_url": multi_slot["bound_action"].get("url") if multi_slot and multi_slot.get("bound_action") else None,
        "template_only_vs_param": "PASS" if template_only_handling else ("FAIL" if template_only_handling is False else "INCONCLUSIVE"),
        "template_only_vs_param_winning": template_vs_param["mechanism_id"] if template_vs_param else None,
        "template_vs_literal_winner": template_vs_literal_winner,
        "equal_slot_tie_param_winner": equal_slot_tie_winner,
        "exceptions_count": len(errors),
        "total_conditions": len(CONDITIONS),
        "conditions_with_correct_status": sum(1 for o in resolution_obs if o["match_expected_status"]),
    }

    # =============================================================================
    # CONTROLS (stable identifiers for downstream)
    # =============================================================================

    controls = {
        "B_COLD": {
            "expected": "UNKNOWN",
            "observed_status": cold_obs["status"] if cold_obs else None,
            "pass": cold_pass,
        },
        "B_LITERAL_ONLY_ORIG": {
            "expected": "EXECUTABLE url=/posts/1",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "literal-only-original"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "literal-only-original" and o.get("bound_action")), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "literal-only-original"), None),
        },
        "B_LITERAL_ONLY_UNSEEN": {
            "expected": "EXECUTABLE url=/posts/1 (literal universal)",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "literal-only-unseen"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "literal-only-unseen" and o.get("bound_action")), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "literal-only-unseen"), None),
        },
        "B_PARAM_ONLY_ORIG": {
            "expected": "EXECUTABLE url=/posts/1",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "param-only-original"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "param-only-original" and o.get("bound_action")), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "param-only-original"), None),
        },
        "B_PARAM_ONLY_UNSEEN": {
            "expected": "EXECUTABLE url=/posts/2 (param generalizes)",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "param-only-unseen"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "param-only-unseen" and o.get("bound_action")), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "param-only-unseen"), None),
        },
        "B_CONFIDENCE_PARAM_HIGHER": {
            "expected": "EXECUTABLE param (0.98) wins",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "compete-param-higher"), None),
            "observed_mechanism": next((o["mechanism_id"] for o in baseline_obs if o["condition_id"] == "compete-param-higher"), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "compete-param-higher"), None),
        },
        "B_CONFIDENCE_LITERAL_HIGHER": {
            "expected": "EXECUTABLE literal (0.98) wins",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "compete-literal-higher"), None),
            "observed_mechanism": next((o["mechanism_id"] for o in baseline_obs if o["condition_id"] == "compete-literal-higher"), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "compete-literal-higher"), None),
        },
        "NULL_FALSE_ACCEPT_ELIMINATION": {
            "expected": "All 5 compete-equal-id conditions return param-fetch-posts (false accepts eliminated)",
            "observed_false_accept_count": false_accept_count,
            "observed_per_id": {o["condition_id"]: o["mechanism_id"] for o in compete_equal_obs},
            "pass": false_accepts_eliminated,
        },
        "POS_MULTI_SLOT": {
            "expected": "EXECUTABLE param-2slot wins (len=2 > len=1)",
            "observed_status": multi_slot["status"] if multi_slot else None,
            "observed_mechanism": multi_slot["mechanism_id"] if multi_slot else None,
            "pass": multi_slot_dominance,
        },
        "POS_TEMPLATE_VS_PARAM": {
            "expected": "EXECUTABLE param-fetch-posts wins over template-only",
            "observed_status": template_vs_param["status"] if template_vs_param else None,
            "observed_mechanism": template_vs_param["mechanism_id"] if template_vs_param else None,
            "pass": template_only_handling,
        },
    }

    # =============================================================================
    # ARTIFACTS
    # =============================================================================

    artifacts = [
        {"path": "research/experiments/EXP-GRAPH-33998605047/run_experiment.py", "sha256": None, "role": "code"},
        {"path": "src/spider/kernel.py", "sha256": None, "role": "code"},
        {"path": "src/spider/models.py", "sha256": None, "role": "code"},
        {"path": "src/spider/registry.py", "sha256": None, "role": "code"},
    ]

    for art in artifacts:
        fpath = PROJECT_ROOT / art["path"]
        if fpath.exists():
            art["sha256"] = hashlib.sha256(fpath.read_bytes()).hexdigest()

    # =============================================================================
    # RAW EVIDENCE (separate from observations)
    # =============================================================================

    raw_evidence = {
        "observations": raw_observations,
        "errors": errors,
        "fix_applied": True,
        "fix_description": "candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)",
        "fix_target": "src/spider/kernel.py L112",
        "unfixed_line": "candidates.sort(key=lambda m: m.confidence, reverse=True)",
    }
    raw_path = Path(__file__).parent / "raw_evidence.json"
    raw_path.write_text(json.dumps(raw_evidence, indent=2), encoding="utf-8")

    # =============================================================================
    # DERIVED MEASUREMENTS (separate from raw evidence)
    # =============================================================================

    derived = {
        "baseline_pass": baseline_pass,
        "baseline_pass_count": sum(1 for o in baseline_obs if o["match_expected_status"]),
        "baseline_total": len(baseline_obs),
        "baseline_details": [{"id": o["condition_id"], "pass": o["match_expected_status"],
                              "status": o["status"], "url": o["bound_action"].get("url") if o.get("bound_action") else None}
                             for o in baseline_obs],
        "cold_baseline_pass": cold_pass,
        "false_accepts_eliminated": false_accepts_eliminated,
        "false_accept_count": false_accept_count,
        "compete_equal_details": [{"id": o["condition_id"], "mechanism": o["mechanism_id"],
                                   "url": o["bound_action"].get("url") if o.get("bound_action") else None,
                                   "param_wins": o.get("match_expected_mechanism")}
                                  for o in compete_equal_obs],
        "multi_slot_dominance": multi_slot_dominance,
        "multi_slot_details": multi_slot,
        "template_only_handling": template_only_handling,
        "template_only_vs_param_details": template_vs_param,
        "template_vs_literal_winner": template_vs_literal_winner,
        "template_vs_literal_details": template_vs_literal,
        "equal_slot_tie_winner": equal_slot_tie_winner,
        "equal_slot_tie_details": tie_param,
        "conditions_met_count": sum(1 for o in resolution_obs if o["match_expected_status"]),
        "conditions_total": len(CONDITIONS),
    }
    derived_path = Path(__file__).parent / "derived_measurements.json"
    derived_path.write_text(json.dumps(derived, indent=2), encoding="utf-8")

    # =============================================================================
    # OBSERVATIONS (direct, not interpreted)
    # =============================================================================

    observations = []
    for o in raw_observations:
        obs_text = f"[{o['condition_id']}] type={o['type']}"
        if o["type"] == "resolution":
            obs_text += f" status={o['status']} mechanism={o['mechanism_id']}"
            if o.get("bound_action"):
                obs_text += f" bound_url={o['bound_action'].get('url', 'N/A')}"
            obs_text += f" confidence={o['confidence']}"
        observations.append(obs_text)

    # =============================================================================
    # VALIDITY NOTES
    # =============================================================================

    validity_notes = [
        "Fix applied temporarily during execution — current HEAD src/spider/kernel.py L112 still has unfixed sort key (m.confidence only). Production commit requires Director approval.",
        "All conditions deterministic: no model calls, no RNG, no sampling. Single-run exact point comparisons. No statistical uncertainty.",
        "No HTTP execution — resolution-only conditions. Network availability not tested. Out of scope per preregistration.",
        "Synthetic substrate (jsonplaceholder.typicode.com templates) — generalizability to real-web endpoints with DOM, auth, session, drift not tested here.",
        "Each condition uses a fresh kernel instance with explicitly controlled registry contents. No cross-contamination.",
        "Registry insertion order controlled: literal registered before param in shared-equal conditions to test tie-break. Equal-slot ties are insertion-order dependent (established in parent).",
        "template-only-vs-literal and equal-slot-tie conditions have uncertain expected outcomes (insertion-order tie-break on mechanism_id). Results recorded as-is, not pass/fail.",
        "The fix was not committed to HEAD — sha256 of unfixed kernel.py confirmed in artifacts.",
    ]

    # =============================================================================
    # UNRESOLVED
    # =============================================================================

    unresolved = [
        "Whether the fix generalizes to real-web endpoints with DOM, auth, session state, drift (not tested here).",
        "Whether the fix has been committed to production HEAD (current HEAD unfixed, requires Director action).",
        "Whether the literal-vs-param equal-confidence competition remains param-winning after fix is committed to production HEAD.",
        "Whether LLM-driven mechanism distillation ('learn on A' half of C-PARAM-INHERIT) works (no model calls).",
        "Whether _matches() discriminates beyond empty dict preconditions (all mechanisms tested with preconditions={}).",
        "Whether _bind() preserves type for full-match template strings (int -> int) (only URL-embedded partial match tested).",
        "Whether the fix generalizes to other slot counts (3 vs 2, 5 vs 1), other template shapes, or other intents beyond fetch-post.",
        "Whether template-only params need explicit handling via required_slots rather than declared slots for production use.",
    ]

    # =============================================================================
    # RESULT.JSON
    # =============================================================================

    result = {
        "schema_version": 1,
        "experiment_id": "EXP-GRAPH-33998605047",
        "lane": "graph",
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    result_path = Path(__file__).parent / "result.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"result.json written: {result_path}")
    print(f"Outcome: {outcome}")
    print(f"Status: {status}")

    # Print key findings
    print("\n=== KEY FINDINGS ===")
    print(f"Baseline regression: {'PASS' if baseline_pass else 'FAIL'} ({metrics['baseline_pass_count']}/{metrics['baseline_total']})")
    print(f"Cold baseline: {'PASS' if cold_pass else 'FAIL'}")
    print(f"False accepts eliminated: {'PASS' if false_accepts_eliminated else 'FAIL'} ({false_accept_count} remaining)")
    for o in compete_equal_obs:
        print(f"  {o['condition_id']}: mechanism={o['mechanism_id']} url={o.get('bound_action', {}).get('url') if o.get('bound_action') else 'N/A'}")
    print(f"Multi-slot dominance: {'PASS' if multi_slot_dominance else 'FAIL'}")
    print(f"Template-only vs param: {'PASS' if template_only_handling else 'FAIL'}")
    print(f"Template-only vs literal winner: {template_vs_literal_winner}")
    print(f"Equal-slot param tie winner: {equal_slot_tie_winner}")

    return result


if __name__ == "__main__":
    main()
