#!/usr/bin/env python3
"""EXP-GRAPH-34170139507 — Execute frozen experiment.

Tests parameter-slot-count fix with actual HTTP execution against live endpoint.
8 conditions: 6 baselines + compete-equal (intervention) + multi-slot (positive control).
Deterministic, no model calls, network required.
"""

import json
import sys
import tempfile
import hashlib
import urllib.request
import urllib.error
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
    "param-2slot": Mechanism(
        mechanism_id="param-2slot",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}/${category}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=["id", "category"],
        confidence=0.95,
    ),
}

# =============================================================================
# REGISTRY CONFIGURATIONS (from frozen spec.json)
# =============================================================================

REGISTRIES = {
    "empty": [],
    "literal-only": ["literal-fetch-posts-1"],
    "param-only": ["param-fetch-posts"],
    "shared-param-higher": ["param-fetch-posts-high", "literal-fetch-posts-1"],  # param higher confidence
    "shared-equal": ["literal-fetch-posts-1", "param-fetch-posts"],  # equal confidence
    "2slot-vs-1slot-equal-conf": ["param-2slot", "param-fetch-posts"],  # 2-slot vs 1-slot equal confidence
}

# =============================================================================
# CONDITION DEFINITIONS (from frozen spec.json)
# =============================================================================

CONDITIONS = [
    # Baselines
    {"id": "cold", "registry": "empty", "params": {"id": 7}, "expected_resolution": "UNKNOWN",
     "expected_url": None, "expected_http_id": None, "role": "baseline"},
    {"id": "literal-only-original", "registry": "literal-only", "params": {"id": 1},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
     "expected_http_id": 1, "role": "baseline"},
    {"id": "literal-only-unseen", "registry": "literal-only", "params": {"id": 7},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
     "expected_http_id": 1, "role": "baseline"},
    {"id": "param-only-original", "registry": "param-only", "params": {"id": 1},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
     "expected_http_id": 1, "role": "baseline"},
    {"id": "param-only-unseen", "registry": "param-only", "params": {"id": 7},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/7",
     "expected_http_id": 7, "role": "baseline"},
    {"id": "compete-param-higher", "registry": "shared-param-higher", "params": {"id": 7},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/7",
     "expected_http_id": 7, "role": "baseline"},
    # Intervention: core hazard test under HTTP execution
    {"id": "compete-equal", "registry": "shared-equal", "params": {"id": 7},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/7",
     "expected_http_id": 7, "role": "intervention"},
    # Positive control: multi-slot dominance
    {"id": "multi-slot-beats-1-slot", "registry": "2slot-vs-1slot-equal-conf", "params": {"id": 1, "category": "tech"},
     "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1/tech",
     "expected_http_id": None, "role": "positive_control"},
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
# HTTP EXECUTION
# =============================================================================

def http_get(url: str, timeout: int = 5) -> dict:
    """Make HTTP GET request and return response details."""
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status_code = resp.getcode()
            body = resp.read().decode("utf-8")
            try:
                json_body = json.loads(body)
            except json.JSONDecodeError:
                json_body = None
            return {
                "status_code": status_code,
                "body": body,
                "json_body": json_body,
                "error": None,
            }
    except urllib.error.URLError as e:
        return {
            "status_code": None,
            "body": None,
            "json_body": None,
            "error": f"URLError: {e}",
        }
    except urllib.error.HTTPError as e:
        return {
            "status_code": e.code,
            "body": None,
            "json_body": None,
            "error": f"HTTPError: {e}",
        }
    except Exception as e:
        return {
            "status_code": None,
            "body": None,
            "json_body": None,
            "error": f"Exception: {e}",
        }

# =============================================================================
# EXECUTION
# =============================================================================

def create_kernel(registry_name: str) -> SpiderKernel:
    """Create a fresh kernel with specified registry mechanisms."""
    tmp = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False, prefix=f"exp3417_{registry_name}_")
    tmp.close()
    registry = MechanismRegistry(tmp.name)
    mech_ids = REGISTRIES[registry_name]
    mechanisms = [MECHANISMS[mid] for mid in mech_ids]
    registry.replace(mechanisms)
    return SpiderKernel(registry, min_confidence=0.8)


def run_condition(cond: dict) -> dict:
    """Run a single condition: resolve + HTTP GET."""
    kernel = create_kernel(cond["registry"])
    resolution = kernel.resolve("fetch-post", {}, cond["params"])

    obs = {
        "condition_id": cond["id"],
        "type": "resolution+http",
        "status": resolution.status.value if hasattr(resolution.status, 'value') else str(resolution.status),
        "mechanism_id": resolution.mechanism_id,
        "bound_action": resolution.bound_action,
        "confidence": resolution.confidence,
        "reason": resolution.reason,
        "expected_status": cond["expected_resolution"],
        "expected_url": cond["expected_url"],
        "expected_http_id": cond["expected_http_id"],
        "match_expected_status": (resolution.status.value if hasattr(resolution.status, 'value') else str(resolution.status)) == cond["expected_resolution"],
        "match_expected_url": resolution.bound_action.get("url") == cond["expected_url"] if cond["expected_url"] is not None and resolution.bound_action else None,
        "role": cond["role"],
    }

    # HTTP execution if resolution is EXECUTABLE
    if obs["status"] == "EXECUTABLE" and obs["bound_action"] and "url" in obs["bound_action"]:
        url = obs["bound_action"]["url"]
        http_response = http_get(url, timeout=5)
        obs["http_status_code"] = http_response["status_code"]
        obs["http_json_body"] = http_response["json_body"]
        obs["http_error"] = http_response["error"]
        
        # Extract id from JSON response if present
        if http_response["json_body"] and isinstance(http_response["json_body"], dict):
            obs["http_response_id"] = http_response["json_body"].get("id")
        else:
            obs["http_response_id"] = None
        
        # Check HTTP validity
        obs["http_valid"] = (
            http_response["status_code"] == 200
            and http_response["json_body"] is not None
            and http_response["error"] is None
        )
        
        # Check if HTTP response matches expected
        if cond["expected_http_id"] is not None:
            obs["match_expected_http_id"] = obs["http_response_id"] == cond["expected_http_id"]
        else:
            obs["match_expected_http_id"] = None  # not expected (multi-slot path)
    else:
        obs["http_status_code"] = None
        obs["http_json_body"] = None
        obs["http_error"] = None
        obs["http_response_id"] = None
        obs["http_valid"] = None
        obs["match_expected_http_id"] = None

    return obs


def main():
    apply_fix()

    raw_observations = []
    errors = []

    # Run all 8 conditions
    for cond in CONDITIONS:
        try:
            obs = run_condition(cond)
            raw_observations.append(obs)
        except Exception as e:
            errors.append({"condition_id": cond["id"], "error": str(e), "type": "exception"})
            raw_observations.append({
                "condition_id": cond["id"],
                "type": "resolution+http",
                "status": "EXCEPTION",
                "mechanism_id": None,
                "bound_action": None,
                "confidence": None,
                "reason": str(e),
                "expected_status": cond["expected_resolution"],
                "expected_url": cond["expected_url"],
                "expected_http_id": cond["expected_http_id"],
                "match_expected_status": False,
                "match_expected_url": None,
                "http_status_code": None,
                "http_json_body": None,
                "http_error": str(e),
                "http_response_id": None,
                "http_valid": False,
                "match_expected_http_id": None,
                "role": cond["role"],
            })

    # =============================================================================
    # DERIVED MEASUREMENTS
    # =============================================================================

    resolution_obs = [o for o in raw_observations]

    # Baseline observations (6 conditions)
    baseline_ids = ["cold", "literal-only-original", "literal-only-unseen",
                    "param-only-original", "param-only-unseen",
                    "compete-param-higher"]
    baseline_obs = [o for o in resolution_obs if o["condition_id"] in baseline_ids]
    baseline_pass = all(o["match_expected_status"] for o in baseline_obs)

    # Cold baseline specifically
    cold_obs = next((o for o in resolution_obs if o["condition_id"] == "cold"), None)
    cold_pass = cold_obs["status"] == "UNKNOWN" if cold_obs else False

    # Compete-equal (core hazard test)
    compete_equal = next((o for o in resolution_obs if o["condition_id"] == "compete-equal"), None)
    compete_equal_param_wins = (
        compete_equal["status"] == "EXECUTABLE"
        and compete_equal["mechanism_id"] == "param-fetch-posts"
        and compete_equal["match_expected_url"] is True
        and compete_equal["match_expected_http_id"] is True
    ) if compete_equal else False

    # Multi-slot dominance
    multi_slot = next((o for o in resolution_obs if o["condition_id"] == "multi-slot-beats-1-slot"), None)
    multi_slot_dominance = (
        multi_slot["status"] == "EXECUTABLE"
        and multi_slot["mechanism_id"] == "param-2slot"
        and multi_slot["match_expected_url"] is True
        and multi_slot["http_valid"] is True
    ) if multi_slot else False

    # Literal-only-unseen: literal does not generalize
    literal_unseen = next((o for o in resolution_obs if o["condition_id"] == "literal-only-unseen"), None)
    literal_does_not_generalize = (
        literal_unseen["status"] == "EXECUTABLE"
        and literal_unseen["mechanism_id"] == "literal-fetch-posts-1"
        and literal_unseen["match_expected_http_id"] is True
        and literal_unseen["http_response_id"] == 1
    ) if literal_unseen else False

    # Param-only-unseen: param generalizes
    param_unseen = next((o for o in resolution_obs if o["condition_id"] == "param-only-unseen"), None)
    param_generalizes = (
        param_unseen["status"] == "EXECUTABLE"
        and param_unseen["mechanism_id"] == "param-fetch-posts"
        and param_unseen["match_expected_http_id"] is True
        and param_unseen["http_response_id"] == 7
    ) if param_unseen else False

    # =============================================================================
    # DECISION RULE (from frozen spec.json)
    # =============================================================================

    has_exceptions = len(errors) > 0
    has_unexpected_status = any(o["status"] not in ("EXECUTABLE", "UNKNOWN", "EXCEPTION") for o in resolution_obs)

    # Check network failures (MEASUREMENT_INVALID)
    network_failures = []
    for o in resolution_obs:
        if o["status"] == "EXECUTABLE" and o.get("http_error") is not None:
            network_failures.append(o["condition_id"])
    has_network_failure = len(network_failures) > 0

    # HTTP-PARAM-INHERIT-SURVIVES: all 6 criteria
    http_param_inherit_survives = (
        baseline_pass
        and compete_equal_param_wins
        and literal_does_not_generalize
        and param_generalizes
        and multi_slot_dominance
        and not has_exceptions
        and not has_network_failure
    )

    # HTTP-PARAM-INHERIT-FALSIFIED: any of the failure conditions
    http_param_inherit_falsified = (
        (compete_equal is not None and not compete_equal_param_wins)
        or (compete_equal is not None and compete_equal.get("match_expected_url") is False)
        or (compete_equal is not None and compete_equal.get("match_expected_http_id") is False)
    )

    if has_exceptions or has_unexpected_status or has_network_failure:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    elif http_param_inherit_survives:
        status = "COMPLETE"
        outcome = "SUPPORTS"
    elif http_param_inherit_falsified:
        status = "COMPLETE"
        outcome = "FALSIFIES"
    else:
        status = "COMPLETE"
        outcome = "MIXED"

    # =============================================================================
    # METRICS
    # =============================================================================

    metrics = {
        "baseline_pass": baseline_pass,
        "baseline_pass_count": sum(1 for o in baseline_obs if o["match_expected_status"]),
        "baseline_total": len(baseline_obs),
        "cold_baseline_pass": cold_pass,
        "compete_equal_param_wins": compete_equal_param_wins,
        "compete_equal_http_response_id": compete_equal.get("http_response_id") if compete_equal else None,
        "literal_does_not_generalize": literal_does_not_generalize,
        "literal_unseen_http_response_id": literal_unseen.get("http_response_id") if literal_unseen else None,
        "param_generalizes": param_generalizes,
        "param_unseen_http_response_id": param_unseen.get("http_response_id") if param_unseen else None,
        "multi_slot_dominance": multi_slot_dominance,
        "multi_slot_http_valid": multi_slot.get("http_valid") if multi_slot else None,
        "exceptions_count": len(errors),
        "network_failure_count": len(network_failures),
        "network_failure_conditions": network_failures,
        "total_conditions": len(CONDITIONS),
        "conditions_with_correct_status": sum(1 for o in resolution_obs if o["match_expected_status"]),
        "http_status_codes": {o["condition_id"]: o.get("http_status_code") for o in resolution_obs if o["status"] == "EXECUTABLE"},
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
            "expected": "EXECUTABLE url=/posts/1, HTTP id=1",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "literal-only-original"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "literal-only-original" and o.get("bound_action")), None),
            "observed_http_id": next((o["http_response_id"] for o in baseline_obs if o["condition_id"] == "literal-only-original"), None),
            "pass": next((o["match_expected_status"] and o.get("match_expected_http_id") for o in baseline_obs if o["condition_id"] == "literal-only-original"), None),
        },
        "B_LITERAL_ONLY_UNSEEN": {
            "expected": "EXECUTABLE url=/posts/1 (literal universal), HTTP id=1",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "literal-only-unseen"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "literal-only-unseen" and o.get("bound_action")), None),
            "observed_http_id": next((o["http_response_id"] for o in baseline_obs if o["condition_id"] == "literal-only-unseen"), None),
            "pass": next((o["match_expected_status"] and o.get("match_expected_http_id") for o in baseline_obs if o["condition_id"] == "literal-only-unseen"), None),
            "interpretation": "Literal does not generalize: id=7 resolves to /posts/1, HTTP returns id=1 (not 7)",
        },
        "B_PARAM_ONLY_ORIG": {
            "expected": "EXECUTABLE url=/posts/1, HTTP id=1",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "param-only-original"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "param-only-original" and o.get("bound_action")), None),
            "observed_http_id": next((o["http_response_id"] for o in baseline_obs if o["condition_id"] == "param-only-original"), None),
            "pass": next((o["match_expected_status"] and o.get("match_expected_http_id") for o in baseline_obs if o["condition_id"] == "param-only-original"), None),
        },
        "B_PARAM_ONLY_UNSEEN": {
            "expected": "EXECUTABLE url=/posts/7 (param generalizes), HTTP id=7",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "param-only-unseen"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "param-only-unseen" and o.get("bound_action")), None),
            "observed_http_id": next((o["http_response_id"] for o in baseline_obs if o["condition_id"] == "param-only-unseen"), None),
            "pass": next((o["match_expected_status"] and o.get("match_expected_http_id") for o in baseline_obs if o["condition_id"] == "param-only-unseen"), None),
            "interpretation": "Param generalizes: id=7 resolves to /posts/7, HTTP returns id=7",
        },
        "B_CONFIDENCE_PARAM_HIGHER": {
            "expected": "EXECUTABLE param (0.98) wins, HTTP id=7",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "compete-param-higher"), None),
            "observed_mechanism": next((o["mechanism_id"] for o in baseline_obs if o["condition_id"] == "compete-param-higher"), None),
            "observed_http_id": next((o["http_response_id"] for o in baseline_obs if o["condition_id"] == "compete-param-higher"), None),
            "pass": next((o["match_expected_status"] and o.get("match_expected_http_id") for o in baseline_obs if o["condition_id"] == "compete-param-higher"), None),
        },
        "NULL_FALSE_ACCEPT_ELIMINATION": {
            "expected": "compete-equal returns param-fetch-posts (not literal), bound URL /posts/7, HTTP id=7",
            "observed_mechanism": compete_equal["mechanism_id"] if compete_equal else None,
            "observed_url": compete_equal["bound_action"].get("url") if compete_equal and compete_equal.get("bound_action") else None,
            "observed_http_id": compete_equal.get("http_response_id") if compete_equal else None,
            "pass": compete_equal_param_wins,
        },
        "POS_MULTI_SLOT": {
            "expected": "EXECUTABLE param-2slot wins, bound URL /posts/1/tech, HTTP status 200",
            "observed_status": multi_slot["status"] if multi_slot else None,
            "observed_mechanism": multi_slot["mechanism_id"] if multi_slot else None,
            "observed_url": multi_slot["bound_action"].get("url") if multi_slot and multi_slot.get("bound_action") else None,
            "observed_http_valid": multi_slot.get("http_valid") if multi_slot else None,
            "pass": multi_slot_dominance,
        },
    }

    # =============================================================================
    # ARTIFACTS
    # =============================================================================

    artifacts = [
        {"path": "research/experiments/EXP-GRAPH-34170139507/run_experiment.py", "sha256": None, "role": "code"},
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
        "network_failures": network_failures,
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
                              "status": o["status"], "url": o["bound_action"].get("url") if o.get("bound_action") else None,
                              "http_id": o.get("http_response_id")}
                             for o in baseline_obs],
        "cold_baseline_pass": cold_pass,
        "compete_equal_param_wins": compete_equal_param_wins,
        "compete_equal_details": {
            "mechanism": compete_equal["mechanism_id"] if compete_equal else None,
            "url": compete_equal["bound_action"].get("url") if compete_equal and compete_equal.get("bound_action") else None,
            "http_id": compete_equal.get("http_response_id") if compete_equal else None,
            "http_status": compete_equal.get("http_status_code") if compete_equal else None,
        },
        "literal_does_not_generalize": literal_does_not_generalize,
        "literal_unseen_details": {
            "mechanism": literal_unseen["mechanism_id"] if literal_unseen else None,
            "url": literal_unseen["bound_action"].get("url") if literal_unseen and literal_unseen.get("bound_action") else None,
            "http_id": literal_unseen.get("http_response_id") if literal_unseen else None,
        },
        "param_generalizes": param_generalizes,
        "param_unseen_details": {
            "mechanism": param_unseen["mechanism_id"] if param_unseen else None,
            "url": param_unseen["bound_action"].get("url") if param_unseen and param_unseen.get("bound_action") else None,
            "http_id": param_unseen.get("http_response_id") if param_unseen else None,
        },
        "multi_slot_dominance": multi_slot_dominance,
        "multi_slot_details": {
            "mechanism": multi_slot["mechanism_id"] if multi_slot else None,
            "url": multi_slot["bound_action"].get("url") if multi_slot and multi_slot.get("bound_action") else None,
            "http_valid": multi_slot.get("http_valid") if multi_slot else None,
            "http_status": multi_slot.get("http_status_code") if multi_slot else None,
        },
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
        if o["type"] == "resolution+http":
            obs_text += f" status={o['status']} mechanism={o['mechanism_id']}"
            if o.get("bound_action"):
                obs_text += f" bound_url={o['bound_action'].get('url', 'N/A')}"
            obs_text += f" confidence={o['confidence']}"
            if o.get("http_status_code") is not None:
                obs_text += f" http_status={o['http_status_code']}"
            if o.get("http_response_id") is not None:
                obs_text += f" http_id={o['http_response_id']}"
            if o.get("http_error"):
                obs_text += f" http_error={o['http_error']}"
        observations.append(obs_text)

    # =============================================================================
    # VALIDITY NOTES
    # =============================================================================

    validity_notes = [
        "Fix applied temporarily during execution — current HEAD src/spider/kernel.py L112 still has unfixed sort key (m.confidence only). Production commit requires Director approval.",
        "All conditions deterministic: no model calls, no RNG, no sampling. Single-run exact point comparisons. No statistical uncertainty.",
        "HTTP execution against live endpoint jsonplaceholder.typicode.com. Network availability required; if unreachable, condition is MEASUREMENT_INVALID.",
        "5-second timeout per HTTP request to avoid hanging on network issues.",
        "jsonplaceholder is a simple REST API, not a complex Web application with DOM, auth, session state, or drift. This experiment tests the execution path (resolve -> bind -> HTTP -> response), not full browser interaction.",
        "Each condition uses a fresh kernel instance with explicitly controlled registry contents. No cross-contamination.",
        "Registry insertion order controlled: literal registered before param in shared-equal conditions to test tie-break under fix.",
        "The fix was not committed to HEAD — sha256 of unfixed kernel.py confirmed in artifacts.",
        "Network failures recorded as MEASUREMENT_INVALID, not scientific falsification.",
    ]

    # =============================================================================
    # UNRESOLVED
    # =============================================================================

    unresolved = [
        "Whether the fix generalizes to real-web endpoints with DOM, auth, session state, drift (jsonplaceholder is simple REST).",
        "Whether the fix has been committed to production HEAD (current HEAD unfixed, requires Director action).",
        "Whether the literal-vs-param equal-confidence competition remains param-winning after fix is committed to production HEAD.",
        "Whether LLM-driven mechanism distillation ('learn on A' half of C-PARAM-INHERIT) works (no model calls).",
        "Whether _matches() discriminates beyond empty dict preconditions (all mechanisms tested with preconditions={}).",
        "Whether _bind() preserves type for full-match template strings (int -> int) (only URL-embedded partial match tested).",
        "Whether the fix generalizes to other slot counts (3 vs 2, 5 vs 1), other template shapes, or other intents beyond fetch-post.",
    ]

    # =============================================================================
    # RESULT.JSON
    # =============================================================================

    result = {
        "schema_version": 1,
        "experiment_id": "EXP-GRAPH-34170139507",
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
    print(f"Compete-equal param wins: {'PASS' if compete_equal_param_wins else 'FAIL'}")
    if compete_equal:
        print(f"  mechanism={compete_equal['mechanism_id']} url={compete_equal.get('bound_action', {}).get('url') if compete_equal.get('bound_action') else 'N/A'} http_id={compete_equal.get('http_response_id')}")
    print(f"Literal does not generalize: {'PASS' if literal_does_not_generalize else 'FAIL'}")
    if literal_unseen:
        print(f"  http_id={literal_unseen.get('http_response_id')}")
    print(f"Param generalizes: {'PASS' if param_generalizes else 'FAIL'}")
    if param_unseen:
        print(f"  http_id={param_unseen.get('http_response_id')}")
    print(f"Multi-slot dominance: {'PASS' if multi_slot_dominance else 'FAIL'}")
    if multi_slot:
        print(f"  http_valid={multi_slot.get('http_valid')}")
    print(f"Network failures: {len(network_failures)}")
    if network_failures:
        print(f"  Conditions: {network_failures}")

    return result


if __name__ == "__main__":
    main()