#!/usr/bin/env python3
"""
EXP-GRAPH-33528827169: Parameterized Mechanism Resolution End-to-End Test

Tests SpiderKernel's parameterized mechanism resolution on a real HTTP endpoint.
Registered mechanisms:
- literal-fetch-posts-1: Literal (no parameter_slots) for /posts/1
- param-fetch-posts: Parameterized (parameter_slots=["id"]) for /posts/${id}
- param-fetch-posts-guarded: Parameterized with applicability_guards={auth_required: true}

Conditions (11 total):
1. cold: No mechanism registered → UNKNOWN
2. literal-original: Literal on original resource → EXECUTABLE with correct URL
3. literal-unseen: Literal on unseen resource → UNKNOWN
4. missing-params: Parameterized with missing slot → UNKNOWN
5. param-original: Parameterized on original resource → EXECUTABLE with correct URL
6-10. param-unseen-1..5: Parameterized on unseen resources 2-6 → EXECUTABLE with correct URLs
11. guard-blocked: Parameterized with blocking guard → UNKNOWN
"""

import json
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any

import requests

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from spider.models import Mechanism, Resolution, ResolutionStatus
from spider.registry import MechanismRegistry
from spider.kernel import SpiderKernel


BASE_URL = "https://jsonplaceholder.typicode.com"
CONDITIONS = [
    {"id": "cold", "mechanism": "none", "params": {"id": 2}, "expected_resolution": "UNKNOWN"},
    {"id": "literal-original", "mechanism": "literal", "params": {"id": 1}, "expected_resolution": "EXECUTABLE", "expected_url": f"{BASE_URL}/posts/1"},
    {"id": "literal-unseen", "mechanism": "literal", "params": {"id": 2}, "expected_resolution": "UNKNOWN"},
    {"id": "missing-params", "mechanism": "parameterized", "params": {}, "expected_resolution": "UNKNOWN"},
    {"id": "param-original", "mechanism": "parameterized", "params": {"id": 1}, "expected_resolution": "EXECUTABLE", "expected_url": f"{BASE_URL}/posts/1"},
    {"id": "param-unseen-1", "mechanism": "parameterized", "params": {"id": 2}, "expected_resolution": "EXECUTABLE", "expected_url": f"{BASE_URL}/posts/2"},
    {"id": "param-unseen-2", "mechanism": "parameterized", "params": {"id": 3}, "expected_resolution": "EXECUTABLE", "expected_url": f"{BASE_URL}/posts/3"},
    {"id": "param-unseen-3", "mechanism": "parameterized", "params": {"id": 4}, "expected_resolution": "EXECUTABLE", "expected_url": f"{BASE_URL}/posts/4"},
    {"id": "param-unseen-4", "mechanism": "parameterized", "params": {"id": 5}, "expected_resolution": "EXECUTABLE", "expected_url": f"{BASE_URL}/posts/5"},
    {"id": "param-unseen-5", "mechanism": "parameterized", "params": {"id": 6}, "expected_resolution": "EXECUTABLE", "expected_url": f"{BASE_URL}/posts/6"},
    {"id": "guard-blocked", "mechanism": "parameterized-guarded", "params": {"id": 2}, "context_override": {"auth_required": False}, "expected_resolution": "UNKNOWN"},
]

POSTCONDITIONS = {"status": 200, "has_keys": ["userId", "id", "title", "body"]}


def create_mechanisms():
    """Create the three mechanisms for the experiment."""
    literal = Mechanism(
        mechanism_id="literal-fetch-posts-1",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": f"{BASE_URL}/posts/1"},
        postconditions=POSTCONDITIONS,
        parameter_slots=[],
        confidence=0.95,
    )
    param = Mechanism(
        mechanism_id="param-fetch-posts",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": f"{BASE_URL}/posts/${{id}}"},
        postconditions=POSTCONDITIONS,
        parameter_slots=["id"],
        confidence=0.95,
    )
    param_guarded = Mechanism(
        mechanism_id="param-fetch-posts-guarded",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": f"{BASE_URL}/posts/${{id}}"},
        postconditions=POSTCONDITIONS,
        parameter_slots=["id"],
        applicability_guards={"auth_required": True},
        confidence=0.95,
    )
    return [literal, param, param_guarded]


def run_condition(condition: dict, kernel: SpiderKernel, context: dict[str, Any]) -> dict:
    """Run a single condition and return results."""
    result = {
        "condition_id": condition["id"],
        "mechanism_type": condition["mechanism"],
        "params": condition["params"],
        "expected_resolution": condition["expected_resolution"],
        "context": context,
    }

    try:
        # Resolve
        resolution = kernel.resolve("fetch", context, condition["params"])
        result["actual_resolution"] = resolution.status.value
        result["resolution_reason"] = resolution.reason
        result["resolution_mechanism_id"] = resolution.mechanism_id
        result["resolution_confidence"] = resolution.confidence
        result["bound_action"] = resolution.bound_action

        # Check resolution matches expected
        result["resolution_correct"] = resolution.status.value == condition["expected_resolution"]

        # If EXECUTABLE, verify URL and perform HTTP execution
        if resolution.status == ResolutionStatus.EXECUTABLE:
            if "expected_url" in condition:
                result["url_correct"] = resolution.bound_action.get("url") == condition["expected_url"]
            else:
                result["url_correct"] = None

            # HTTP execution
            http_result = execute_http(resolution.bound_action)
            result["http_status"] = http_result["status"]
            result["http_success"] = http_result["success"]
            result["http_response_keys"] = http_result.get("response_keys", [])
            result["http_response_snippet"] = http_result.get("response_snippet", "")

            # Verify postconditions
            if http_result["success"]:
                verify_result = verify_postconditions(
                    resolution.mechanism_id, http_result["response_data"], kernel
                )
                result["verify_result"] = verify_result
            else:
                result["verify_result"] = False
                result["verify_error"] = http_result.get("error", "HTTP execution failed")

        # Overall condition pass
        if condition["expected_resolution"] == "UNKNOWN":
            result["condition_pass"] = resolution.status == ResolutionStatus.UNKNOWN
        elif condition["expected_resolution"] == "EXECUTABLE":
            result["condition_pass"] = (
                resolution.status == ResolutionStatus.EXECUTABLE
                and result.get("url_correct", False)
                and result.get("http_success", False)
                and result.get("verify_result", False)
            )
        else:
            result["condition_pass"] = False

    except Exception as e:
        result["error"] = str(e)
        result["traceback"] = traceback.format_exc()
        result["condition_pass"] = False
        result["actual_resolution"] = "ERROR"

    return result


def execute_http(bound_action: dict[str, Any]) -> dict[str, Any]:
    """Execute an HTTP request based on bound_action."""
    result = {"status": None, "success": False}

    try:
        method = bound_action.get("method", "GET").upper()
        url = bound_action.get("url")
        if not url:
            result["error"] = "No URL in bound_action"
            return result

        response = requests.request(method, url, timeout=10)
        result["status"] = response.status_code

        if response.status_code == 200:
            try:
                data = response.json()
                result["success"] = True
                result["response_data"] = data
                result["response_keys"] = list(data.keys()) if isinstance(data, dict) else []
                result["response_snippet"] = json.dumps(data, indent=2)[:500]
            except json.JSONDecodeError:
                result["error"] = "Response is not valid JSON"
        else:
            result["error"] = f"HTTP {response.status_code}"

    except requests.exceptions.RequestException as e:
        result["error"] = str(e)

    return result


def verify_postconditions(mechanism_id: str, response_data: dict[str, Any], kernel: SpiderKernel) -> bool:
    """Verify postconditions against actual response data."""
    # Construct observed state from response
    observed_state = {"status": 200}
    if isinstance(response_data, dict):
        observed_state["has_keys"] = [k for k in response_data.keys()]
    
    return kernel.verify(mechanism_id, observed_state)


def main():
    """Execute all conditions and collect results."""
    results = []
    start_time = time.time()

    with tempfile.TemporaryDirectory() as td:
        # Create registry and kernel
        reg_path = Path(td) / "mechanisms.jsonl"
        reg = MechanismRegistry(reg_path)
        kernel = SpiderKernel(reg)

        # Register all three mechanisms
        for mechanism in create_mechanisms():
            reg.upsert(mechanism)

        # Verify mechanisms are registered
        all_mechs = reg.all()
        print(f"Registered {len(all_mechs)} mechanisms: {[m.mechanism_id for m in all_mechs]}")

        # Run each condition with a fresh kernel (same registry)
        for condition in CONDITIONS:
            print(f"\nRunning condition: {condition['id']}")
            
            # Determine context
            context = {"base_url": BASE_URL}
            if "context_override" in condition:
                context.update(condition["context_override"])

            # Create fresh kernel for each condition
            kernel = SpiderKernel(reg)

            result = run_condition(condition, kernel, context)
            results.append(result)

            # Print summary
            status_icon = "✓" if result["condition_pass"] else "✗"
            print(f"  {status_icon} Resolution: {result.get('actual_resolution', 'ERROR')} "
                  f"(expected: {condition['expected_resolution']})")
            if result.get("bound_action"):
                print(f"    Bound action: {result['bound_action']}")
            if result.get("http_status"):
                print(f"    HTTP status: {result['http_status']}")
            if result.get("verify_result") is not None:
                print(f"    Verify: {result['verify_result']}")

    # Compute overall verdict
    all_pass = all(r["condition_pass"] for r in results)
    verdict = "PARAM-INHERIT-SUBSTRATE-VALID" if all_pass else "PARAM-INHERIT-SUBSTRATE-BROKEN"
    
    elapsed = time.time() - start_time

    output = {
        "experiment_id": "EXP-GRAPH-33528827169",
        "lane": "graph",
        "claim_id": "C-PARAM-INHERIT",
        "verdict": verdict,
        "elapsed_seconds": round(elapsed, 2),
        "conditions": results,
        "summary": {
            "total_conditions": len(results),
            "passing": sum(1 for r in results if r["condition_pass"]),
            "failing": sum(1 for r in results if not r["condition_pass"]),
        }
    }

    # Write results
    output_path = Path(__file__).parent / "raw_results.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n{'='*60}")
    print(f"EXPERIMENT COMPLETE: {verdict}")
    print(f"Conditions: {output['summary']['passing']}/{output['summary']['total_conditions']} passing")
    print(f"Elapsed: {elapsed:.2f}s")
    print(f"Results written to: {output_path}")

    return output


if __name__ == "__main__":
    main()
