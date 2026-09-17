#!/usr/bin/env python3
"""
EXP-PRODUCT-35185290656: Fix3 Redesign for Query-Parameterized URLs

Tests the redesigned _is_protocol_only_prefix (Fix3) that checks for
'?', '/', or '#' in rest after '://' to correctly distinguish:
- Protocol-only prefixes (bare authority, no path/query/fragment) -> REJECT
- Query-parameterized prefixes (host?query) -> ACCEPT
- Path-slash prefixes (host/path) -> ACCEPT (same as before)

Frozen decision rule conditions:
C1: Fix3 redesigned rejects bare authority prefix 'https://api.example.com' (returns True)
C2: Fix3 redesigned accepts query-parameterized prefix 'https://api.example.com?key=' (returns False)
C3: Fix3 redesigned accepts path-slash prefix 'https://jsonplaceholder.typicode.com/' (returns False)
C4: Old Fix3 (before redesign) incorrectly rejects query-parameterized prefix (returns True)
C5: Kernel regression tests pass (3/3) after Fix3 redesign
C6: HTTP binding accuracy >= 1.0 on query-parameterized endpoint
C7: distill_parameterized with Fix3 redesign produces correct Mechanism for query-parameterized observations
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from spider.kernel import (
    SpiderKernel, distill_parameterized, _is_protocol_only_prefix,
    _validate_prefix_boundary, _find_common_prefix_suffix, _bind, _template_slots,
)
from spider.models import Mechanism, Observation, Resolution, ResolutionStatus
from spider.registry import MechanismRegistry


# =============================================================================
# SECTION 1: URL Test Corpus (12 patterns, 4 categories)
# =============================================================================

URL_CORPUS = [
    # Category 1: Protocol-only (Fix3 should REJECT)
    {"prefix": "https://api.example.com", "category": "protocol_only", "expected_fix3": True, "note": "Bare authority, no path/query"},
    {"prefix": "http://localhost:8080", "category": "protocol_only", "expected_fix3": True, "note": "Localhost bare authority"},
    {"prefix": "https://a.com", "category": "protocol_only", "expected_fix3": True, "note": "Minimal bare authority"},
    # Category 2: Query-parameterized (Fix3 should ACCEPT)
    {"prefix": "https://api.example.com?key=", "category": "query_parameterized", "expected_fix3": False, "note": "Query param prefix"},
    {"prefix": "https://example.com?x=", "category": "query_parameterized", "expected_fix3": False, "note": "Different host"},
    {"prefix": "https://api.example.com?foo=bar&baz=", "category": "query_parameterized", "expected_fix3": False, "note": "Multi-query prefix"},
    # Category 3: Path-slash (Fix3 should ACCEPT, same as current)
    {"prefix": "https://jsonplaceholder.typicode.com/", "category": "path_slash", "expected_fix3": False, "note": "Parent test pattern"},
    {"prefix": "https://jsonplaceholder.typicode.com/posts/", "category": "path_slash", "expected_fix3": False, "note": "Deeper path"},
    {"prefix": "https://api.example.com/v1/", "category": "path_slash", "expected_fix3": False, "note": "Versioned path"},
    # Category 4: Mixed/Edge (Fix3 should ACCEPT)
    {"prefix": "https://api.example.com/path?query=", "category": "mixed_edge", "expected_fix3": False, "note": "Path + query"},
    {"prefix": "https://example.com#frag", "category": "mixed_edge", "expected_fix3": False, "note": "Fragment (unusual)"},
    {"prefix": "https://api.example.com:8080/", "category": "mixed_edge", "expected_fix3": False, "note": "Port + path"},
]


# Old Fix3 logic (pre-redesign, overbroad)
def _old_is_protocol_only_prefix(prefix: str) -> bool:
    """OLD Fix3: Reject prefixes where '/' not in rest after '://'.
    
    BUG: This incorrectly rejects valid host?query patterns like
    'https://api.example.com?key=' because rest has no '/'.
    """
    if not prefix:
        return False
    parts = prefix.split("://", 1)
    if len(parts) != 2:
        return False
    scheme, rest = parts
    if not rest:
        return True
    if "/" not in rest:
        return True
    return False


# =============================================================================
# SECTION 2: Training observations for distill_parameterized
# =============================================================================

P1_TRAINING = {
    "fetch_posts": [
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/1"},
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/2"},
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/3"},
        {"method": "PUT", "url": "https://jsonplaceholder.typicode.com/posts/1"},
        {"method": "PUT", "url": "https://jsonplaceholder.typicode.com/posts/2"},
    ],
    "fetch_users": [
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/users/1"},
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/users/2"},
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/users/3"},
    ],
    "fetch_comments": [
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=1"},
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=2"},
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=3"},
    ],
}

# Query-parameterized training for C7
QUERY_PARAM_TRAINING = {
    "fetch_comments": [
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=1"},
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=2"},
        {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=3"},
    ],
}

P1_UNSEEN = {
    "fetch_posts": [{"url": "96"}, {"url": "97"}, {"url": "98"}],
    "fetch_users": [{"url": "8"}, {"url": "9"}, {"url": "10"}],
    "fetch_comments": [{"url": "5"}, {"url": "6"}, {"url": "7"}],
}


def make_observation(intent: str, action: dict, state: dict = None,
                     next_state: dict = None, success: bool = True) -> Observation:
    return Observation(
        intent=intent,
        state=state or {},
        action=action,
        next_state=next_state or {},
        success=success,
        provenance={},
    )


def http_get(url: str, timeout: int = 10) -> dict:
    """Execute HTTP GET and return status, headers, body."""
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", "SPIDER-Experiment/2.0")
        resp = urllib.request.urlopen(req, timeout=timeout)
        body = resp.read().decode("utf-8", errors="replace")
        return {
            "status": resp.status,
            "body": body,
            "content_type": resp.headers.get("Content-Type", ""),
            "error": None,
        }
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return {
            "status": e.code,
            "body": body,
            "content_type": e.headers.get("Content-Type", "") if e.headers else "",
            "error": str(e),
        }
    except Exception as e:
        return {
            "status": 0,
            "body": "",
            "content_type": "",
            "error": str(e),
        }


def validate_comment_body(body_json: Any) -> bool:
    """Comments endpoint returns a list-of-dicts with keys: postId, id, name, email, body."""
    if isinstance(body_json, list):
        if len(body_json) == 0:
            return True
        first = body_json[0]
        if isinstance(first, dict):
            return all(k in first for k in ["postId", "id", "name", "email", "body"])
        return False
    return False


# =============================================================================
# C1: Fix3 redesigned rejects bare authority prefix
# =============================================================================

def test_c1_redesigned_rejects_protocol_only() -> dict:
    """C1: Redesigned Fix3 applied to bare authority prefix 'https://api.example.com'.
    Expected: returns True (rejects)."""
    result = _is_protocol_only_prefix("https://api.example.com")
    return {"condition": "C1", "passed": result is True, "observed": result}


# =============================================================================
# C2: Fix3 redesigned accepts query-parameterized prefix
# =============================================================================

def test_c2_redesigned_accepts_query_param() -> dict:
    """C2: Redesigned Fix3 applied to query-parameterized prefix 'https://api.example.com?key='.
    Expected: returns False (does NOT reject)."""
    result = _is_protocol_only_prefix("https://api.example.com?key=")
    return {"condition": "C2", "passed": result is False, "observed": result}


# =============================================================================
# C3: Fix3 redesigned accepts path-slash prefix
# =============================================================================

def test_c3_redesigned_accepts_path_slash() -> dict:
    """C3: Redesigned Fix3 applied to path-slash prefix 'https://jsonplaceholder.typicode.com/'.
    Expected: returns False (does NOT reject, same as current)."""
    result = _is_protocol_only_prefix("https://jsonplaceholder.typicode.com/")
    return {"condition": "C3", "passed": result is False, "observed": result}


# =============================================================================
# C4: Old Fix3 incorrectly rejects query-parameterized prefix
# =============================================================================

def test_c4_old_fix3_overbroad() -> dict:
    """C4: Old Fix3 (before redesign) incorrectly rejects query-parameterized prefix.
    Expected: returns True (demonstrates the bug being fixed)."""
    result = _old_is_protocol_only_prefix("https://api.example.com?key=")
    return {"condition": "C4", "passed": result is True, "observed": result}


# =============================================================================
# C5: URL Test Corpus (comprehensive 12-pattern test)
# =============================================================================

def test_url_corpus() -> dict:
    """Run all 12 URL patterns through redesigned Fix3."""
    results = []
    all_correct = True
    for entry in URL_CORPUS:
        actual = _is_protocol_only_prefix(entry["prefix"])
        correct = actual == entry["expected_fix3"]
        if not correct:
            all_correct = False
        results.append({
            "prefix": entry["prefix"],
            "category": entry["category"],
            "expected": entry["expected_fix3"],
            "observed": actual,
            "correct": correct,
            "note": entry["note"],
        })
    return {"all_correct": all_correct, "total": len(results), "results": results}


# =============================================================================
# C5: Kernel regression tests
# =============================================================================

def run_existing_kernel_tests() -> dict:
    """Run the existing kernel regression tests."""
    env = {**dict(os.environ), "PYTHONPATH": str(REPO_ROOT / "src")}
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_kernel", "-v"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    all_passed = result.returncode == 0
    tests_run = 0
    failures = 0
    errors = 0
    for line in result.stdout.split("\n"):
        if "Ran" in line and "test" in line:
            parts = line.split()
            if len(parts) >= 2:
                tests_run = int(parts[1])
        if "FAIL" in line:
            failures += 1
        if "ERROR" in line:
            errors += 1

    return {
        "tests_run": tests_run,
        "failures": failures,
        "errors": errors,
        "all_passed": all_passed,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


# =============================================================================
# C6: HTTP binding on query-parameterized endpoint
# =============================================================================

def test_c6_http_binding_query_param() -> dict:
    """C6: HTTP binding accuracy >= 1.0 on query-parameterized endpoint.
    Uses comments?postId=${url} with valid unseen IDs postId 5-7."""
    # Distill parameterized mechanism from query-parameterized observations
    obs_list = []
    for training in QUERY_PARAM_TRAINING["fetch_comments"]:
        obs_list.append(make_observation("fetch_comments", training))

    mech = distill_parameterized(None, obs_list)
    if mech is None:
        return {
            "condition": "C6",
            "passed": False,
            "mechanism_distilled": False,
            "error": "distill_parameterized returned None",
        }

    # Test with unseen IDs
    results = []
    all_correct = True
    for unseen_val in P1_UNSEEN["fetch_comments"]:
        url_val = unseen_val["url"]
        params = {"url": url_val}

        # Construct expected URL
        template_url = mech.action_template.get("url", "")
        expected_url = template_url
        for slot in mech.parameter_slots:
            expected_url = expected_url.replace(f"${{{slot}}}", str(url_val))

        # Make real HTTP request
        http_result = http_get(expected_url)

        # Verify
        status_ok = http_result["status"] == 200
        body_valid = False
        if status_ok:
            try:
                body_json = json.loads(http_result["body"])
                body_valid = validate_comment_body(body_json)
            except (json.JSONDecodeError, ValueError):
                body_valid = False

        http_correct = status_ok and body_valid
        if not http_correct:
            all_correct = False

        results.append({
            "url": expected_url,
            "status": http_result["status"],
            "status_ok": status_ok,
            "body_valid": body_valid,
            "http_correct": http_correct,
            "error": http_result["error"],
        })

    http_accuracy = sum(1 for r in results if r["http_correct"]) / max(len(results), 1)
    return {
        "condition": "C6",
        "passed": all_correct and http_accuracy >= 1.0,
        "mechanism_distilled": True,
        "mechanism_slots": mech.parameter_slots,
        "mechanism_template": mech.action_template,
        "http_accuracy": http_accuracy,
        "total_correct": sum(1 for r in results if r["http_correct"]),
        "total_calls": len(results),
        "results": results,
    }


# =============================================================================
# C7: distill_parameterized produces correct Mechanism for query-parameterized
# =============================================================================

def test_c7_distill_query_param() -> dict:
    """C7: distill_parameterized with Fix3 redesign produces correct Mechanism
    for query-parameterized observations (slot ['url'], template 'comments?postId=${url}')."""
    obs_list = []
    for training in QUERY_PARAM_TRAINING["fetch_comments"]:
        obs_list.append(make_observation("fetch_comments", training))

    mech = distill_parameterized(None, obs_list)

    if mech is None:
        return {
            "condition": "C7",
            "passed": False,
            "mechanism_distilled": False,
            "error": "distill_parameterized returned None",
        }

    # Verify mechanism properties
    has_url_slot = "url" in mech.parameter_slots
    template_str = json.dumps(mech.action_template)
    has_post_id_template = "postId=" in template_str and "${url}" in template_str
    template_is_correct = has_url_slot and has_post_id_template

    # Verify it resolves with params
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        reg = MechanismRegistry(Path(f.name))
    reg.replace([mech])
    kernel = SpiderKernel(reg, min_confidence=0.8)
    resolution = kernel.resolve("fetch_comments", {}, {"url": "5"})
    resolves_executable = resolution.status == ResolutionStatus.EXECUTABLE

    # Verify binding correctness
    if resolves_executable and resolution.bound_action:
        bound_url = resolution.bound_action.get("url", "")
        expected_url = "https://jsonplaceholder.typicode.com/comments?postId=5"
        binding_correct = bound_url == expected_url
    else:
        binding_correct = False
        bound_url = None

    passed = template_is_correct and resolves_executable and binding_correct

    return {
        "condition": "C7",
        "passed": passed,
        "mechanism_distilled": True,
        "parameter_slots": mech.parameter_slots,
        "has_url_slot": has_url_slot,
        "has_post_id_template": has_post_id_template,
        "template": mech.action_template,
        "template_is_correct": template_is_correct,
        "resolves_executable": resolves_executable,
        "binding_correct": binding_correct,
        "bound_url": bound_url,
        "expected_url": "https://jsonplaceholder.typicode.com/comments?postId=5",
        "resolution_status": resolution.status.value,
    }


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_experiment():
    """Run the full EXP-PRODUCT-35185290656 experiment."""
    print("=" * 70)
    print("EXP-PRODUCT-35185290656: Fix3 Redesign for Query-Parameterized URLs")
    print("=" * 70)

    # ─── C1: Fix3 redesigned rejects bare authority ────────────────────
    print("\n--- C1: Fix3 redesigned rejects bare authority ---")
    c1 = test_c1_redesigned_rejects_protocol_only()
    print(f"  _is_protocol_only_prefix('https://api.example.com') = {c1['observed']}")
    print(f"  Expected: True, Passed: {c1['passed']}")

    # ─── C2: Fix3 redesigned accepts query-parameterized ───────────────
    print("\n--- C2: Fix3 redesigned accepts query-parameterized ---")
    c2 = test_c2_redesigned_accepts_query_param()
    print(f"  _is_protocol_only_prefix('https://api.example.com?key=') = {c2['observed']}")
    print(f"  Expected: False, Passed: {c2['passed']}")

    # ─── C3: Fix3 redesigned accepts path-slash ────────────────────────
    print("\n--- C3: Fix3 redesigned accepts path-slash ---")
    c3 = test_c3_redesigned_accepts_path_slash()
    print(f"  _is_protocol_only_prefix('https://jsonplaceholder.typicode.com/') = {c3['observed']}")
    print(f"  Expected: False, Passed: {c3['passed']}")

    # ─── C4: Old Fix3 incorrectly rejects query-parameterized ──────────
    print("\n--- C4: Old Fix3 incorrectly rejects query-parameterized ---")
    c4 = test_c4_old_fix3_overbroad()
    print(f"  OLD _is_protocol_only_prefix('https://api.example.com?key=') = {c4['observed']}")
    print(f"  Expected: True (bug), Passed: {c4['passed']}")

    # ─── URL Corpus (comprehensive 12-pattern test) ────────────────────
    print("\n--- URL Corpus (12 patterns, 4 categories) ---")
    corpus = test_url_corpus()
    print(f"  All correct: {corpus['all_correct']}")
    for r in corpus["results"]:
        status = "OK" if r["correct"] else "FAIL"
        print(f"  [{status}] {r['category']}: '{r['prefix']}' -> {r['observed']} (expected {r['expected']})")

    # ─── C5: Kernel regression tests ───────────────────────────────────
    print("\n--- C5: Kernel regression tests ---")
    c5 = run_existing_kernel_tests()
    print(f"  Tests run: {c5['tests_run']}")
    print(f"  Failures: {c5['failures']}")
    print(f"  Errors: {c5['errors']}")
    print(f"  All passed: {c5['all_passed']}")

    # ─── C6: HTTP binding on query-parameterized endpoint ───────────────
    print("\n--- C6: HTTP binding on query-parameterized endpoint ---")
    c6 = test_c6_http_binding_query_param()
    print(f"  Mechanism distilled: {c6.get('mechanism_distilled', False)}")
    if c6.get("mechanism_template"):
        print(f"  Template: {c6['mechanism_template']}")
        print(f"  Slots: {c6.get('mechanism_slots', [])}")
    print(f"  HTTP accuracy: {c6.get('http_accuracy', 0):.4f}")
    print(f"  Total: {c6.get('total_correct', 0)}/{c6.get('total_calls', 0)}")
    for r in c6.get("results", []):
        print(f"    {r['url']}: status={r['status']} http_correct={r['http_correct']}")
    print(f"  Passed: {c6['passed']}")

    # ─── C7: distill_parameterized for query-parameterized ──────────────
    print("\n--- C7: distill_parameterized for query-parameterized ---")
    c7 = test_c7_distill_query_param()
    print(f"  Mechanism distilled: {c7.get('mechanism_distilled', False)}")
    if c7.get("template"):
        print(f"  Template: {c7['template']}")
        print(f"  Slots: {c7.get('parameter_slots', [])}")
    print(f"  Template correct: {c7.get('template_is_correct', False)}")
    print(f"  Resolves EXECUTABLE: {c7.get('resolves_executable', False)}")
    print(f"  Binding correct: {c7.get('binding_correct', False)}")
    if c7.get("bound_url"):
        print(f"  Bound URL: {c7['bound_url']}")
        print(f"  Expected: {c7.get('expected_url', '')}")
    print(f"  Passed: {c7['passed']}")

    # ─── Overall verdict ────────────────────────────────────────────────
    print("\n" + "=" * 70)
    all_conditions = [c1["passed"], c2["passed"], c3["passed"], c4["passed"],
                      c5["all_passed"], c6["passed"], c7["passed"]]
    condition_names = [
        "C1: Fix3 redesigned rejects bare authority",
        "C2: Fix3 redesigned accepts query-parameterized",
        "C3: Fix3 redesigned accepts path-slash",
        "C4: Old Fix3 incorrectly rejects query-parameterized",
        "C5: Kernel regression tests pass",
        "C6: HTTP binding accuracy >= 1.0 on query-param endpoint",
        "C7: distill_parameterized produces correct Mechanism",
    ]

    for name, passed in zip(condition_names, all_conditions):
        status = "PASS" if passed else "FAIL"
        print(f"  {name} -> {status}")

    all_pass = all(all_conditions)
    verdict = "SURVIVES_CURRENT_TEST" if all_pass else "FALSIFIED-IN-SETTING"
    outcome = "SUPPORTS" if all_pass else "FALSIFIES"
    print(f"\nOVERALL VERDICT: {verdict}")
    print(f"OUTCOME: {outcome}")
    print("=" * 70)

    # Build comprehensive metrics
    metrics = {
        "c1_redesigned_rejects_protocol_only": c1["passed"],
        "c1_observed": c1["observed"],
        "c2_redesigned_accepts_query_param": c2["passed"],
        "c2_observed": c2["observed"],
        "c3_redesigned_accepts_path_slash": c3["passed"],
        "c3_observed": c3["observed"],
        "c4_old_fix3_overbroad": c4["passed"],
        "c4_observed": c4["observed"],
        "c5_kernel_tests_passed": c5["all_passed"],
        "c5_kernel_tests_run": c5["tests_run"],
        "c6_http_binding_accuracy": c6.get("http_accuracy", 0),
        "c6_http_total_correct": c6.get("total_correct", 0),
        "c6_http_total_calls": c6.get("total_calls", 0),
        "c6_mechanism_template": c6.get("mechanism_template"),
        "c6_mechanism_slots": c6.get("mechanism_slots", []),
        "c7_mechanism_distilled": c7.get("mechanism_distilled", False),
        "c7_template_correct": c7.get("template_is_correct", False),
        "c7_resolves_executable": c7.get("resolves_executable", False),
        "c7_binding_correct": c7.get("binding_correct", False),
        "c7_template": c7.get("template"),
        "c7_slots": c7.get("parameter_slots", []),
        "c7_bound_url": c7.get("bound_url"),
        "url_corpus_all_correct": corpus["all_correct"],
        "url_corpus_total": corpus["total"],
        "url_corpus_results": corpus["results"],
        "all_conditions_pass": all_pass,
    }

    controls = {
        "P1_QUERY_PARAM_ACCEPTED": {
            "type": "positive_control",
            "id": "P1_QUERY_PARAM_ACCEPTED",
            "stable_id": "P1_QUERY_PARAM_ACCEPTED",
            "expected": "Redesigned Fix3 returns False for 'https://api.example.com?key='",
            "observed": f"returns {c2['observed']}",
            "passed": c2["passed"],
            "evidence_ref": "test_c2_redesigned_accepts_query_param()",
        },
        "N1_PROTOCOL_ONLY_REJECTED": {
            "type": "null_control",
            "id": "N1_PROTOCOL_ONLY_REJECTED",
            "stable_id": "N1_PROTOCOL_ONLY_REJECTED",
            "expected": "Redesigned Fix3 returns True for 'https://api.example.com'",
            "observed": f"returns {c1['observed']}",
            "passed": c1["passed"],
            "evidence_ref": "test_c1_redesigned_rejects_protocol_only()",
        },
        "B_OLD_FIX3_OVERBROAD": {
            "type": "baseline",
            "id": "B_OLD_FIX3_OVERBROAD",
            "stable_id": "B_OLD_FIX3_OVERBROAD",
            "expected": "Old Fix3 returns True for query-param prefix (demonstrates bug)",
            "observed": f"returns {c4['observed']}",
            "passed": c4["passed"],
            "evidence_ref": "test_c4_old_fix3_overbroad()",
        },
        "B_LITERAL_HTTP_REGRESSION": {
            "type": "baseline",
            "id": "B_LITERAL_HTTP_REGRESSION",
            "stable_id": "B_LITERAL_HTTP_REGRESSION",
            "expected": "Existing kernel regression tests pass (3/3)",
            "observed": f"tests_run={c5['tests_run']}, all_passed={c5['all_passed']}",
            "passed": c5["all_passed"],
            "evidence_ref": "tests/test_kernel.py via unittest",
        },
        "kernel_regression": {
            "type": "regression",
            "id": "kernel_regression",
            "stable_id": "kernel_regression",
            "expected": "All 3 existing kernel tests pass after Fix3 redesign",
            "observed": f"tests_run={c5['tests_run']}, failures={c5['failures']}, errors={c5['errors']}",
            "passed": c5["all_passed"],
            "evidence_ref": "tests/test_kernel.py via unittest",
        },
    }

    return metrics, controls, verdict, outcome, all_conditions, condition_names


if __name__ == "__main__":
    result = run_experiment()
    if result is None:
        print("EXPERIMENT FAILED: Could not complete")
        sys.exit(1)

    metrics, controls, verdict, outcome, all_conditions, condition_names = result

    # Write experiment results
    output = {
        "experiment_id": "EXP-PRODUCT-35185290656",
        "verdict": verdict,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
    }

    output_path = Path(__file__).parent / "experiment_results.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults written to {output_path}")
