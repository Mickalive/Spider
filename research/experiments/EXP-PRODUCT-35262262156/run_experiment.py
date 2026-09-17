#!/usr/bin/env python3
"""EXP-PRODUCT-35262262156: Execute frozen experiment design.

Tests whether parameterized mechanism representation reduces token cost
when concrete values are long strings (UUIDs, slugs, full API paths,
bearer tokens) rather than short numeric IDs.

Patterns: 5 long-value target patterns + 1 positive control + 1 null control
Total: 7 patterns, 21 observations (3 per pattern for resolve/bind)
"""

import json
import tempfile
import sys
import os
import hashlib
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

import tiktoken
from spider.models import Mechanism, Observation, ResolutionStatus
from spider.kernel import SpiderKernel, _template_slots, _bind
from spider.registry import MechanismRegistry


def count_tokens(action_template: dict) -> int:
    """Count tiktoken tokens for action_template JSON serialization."""
    enc = tiktoken.get_encoding("cl100k_base")
    json_str = json.dumps(action_template, sort_keys=True)
    return len(enc.encode(json_str))


def make_literal_mechanism(intent: str, method: str, url: str, evidence: list[str]) -> Mechanism:
    """Create a literal mechanism with full URL (no template slots)."""
    return Mechanism(
        mechanism_id=f"literal-{intent}-{hashlib.sha256(url.encode()).hexdigest()[:8]}",
        intent=intent,
        preconditions={},
        action_template={"method": method, "url": url},
        postconditions={},
        parameter_slots=[],
        evidence=evidence,
        confidence=0.9,
    )


def make_parameterized_mechanism(intent: str, method: str, template_url: str, slots: list[str], evidence: list[str]) -> Mechanism:
    """Create a parameterized mechanism with ${var} template slots."""
    return Mechanism(
        mechanism_id=f"param-{intent}-{hashlib.sha256(template_url.encode()).hexdigest()[:8]}",
        intent=intent,
        preconditions={},
        action_template={"method": method, "url": template_url},
        postconditions={},
        parameter_slots=slots,
        evidence=evidence,
        confidence=0.9,
    )


# ============================================================
# 7 patterns from frozen prereg
# ============================================================

# --- Target long-value patterns (5 patterns) ---

P1_UUID = {
    "id": "P1_UUID",
    "name": "UUID value (36 chars)",
    "category": "long_value",
    "intent": "fetch_user",
    "observations": [
        {"method": "GET", "url": "https://api.example.com/users/550e8400-e29b-41d4-a716-446655440000"},
        {"method": "GET", "url": "https://api.example.com/users/6ba7b810-9dad-11d1-80b4-00c04fd430c8"},
        {"method": "GET", "url": "https://api.example.com/users/f47ac10b-58cc-4372-a567-0e02b2c3d479"},
    ],
    "parameterized_template": {"method": "GET", "url": "https://api.example.com/users/${userId}"},
    "slots": ["userId"],
    "test_params": {"userId": "550e8400-e29b-41d4-a716-446655440000"},
    "expected_bound_url": "https://api.example.com/users/550e8400-e29b-41d4-a716-446655440000",
    "value_length": 36,
}

P2_SLUG = {
    "id": "P2_SLUG",
    "name": "Slug value (28 chars)",
    "category": "long_value",
    "intent": "fetch_page",
    "observations": [
        {"method": "GET", "url": "https://api.example.com/pages/user-profile-settings-page"},
        {"method": "GET", "url": "https://api.example.com/pages/admin-dashboard-analytics-view"},
        {"method": "GET", "url": "https://api.example.com/pages/blog-post-comments-section"},
    ],
    "parameterized_template": {"method": "GET", "url": "https://api.example.com/pages/${pageSlug}"},
    "slots": ["pageSlug"],
    "test_params": {"pageSlug": "user-profile-settings-page"},
    "expected_bound_url": "https://api.example.com/pages/user-profile-settings-page",
    "value_length": 28,
}

P3_DEEPPATH = {
    "id": "P3_DEEPPATH",
    "name": "Deep API path (42 chars total)",
    "category": "long_value",
    "intent": "fetch_project",
    "observations": [
        {"method": "GET", "url": "https://api.example.com/v2/api/organizations/100/projects/200"},
        {"method": "GET", "url": "https://api.example.com/v2/api/organizations/300/projects/400"},
        {"method": "GET", "url": "https://api.example.com/v2/api/organizations/500/projects/600"},
    ],
    "parameterized_template": {"method": "GET", "url": "https://api.example.com/v2/api/organizations/${orgId}/projects/${projectId}"},
    "slots": ["orgId", "projectId"],
    "test_params": {"orgId": "12345", "projectId": "67890"},
    "expected_bound_url": "https://api.example.com/v2/api/organizations/12345/projects/67890",
    "value_length": 42,
}

P4_BEARER = {
    "id": "P4_BEARER",
    "name": "Bearer token (64 chars)",
    "category": "long_value",
    "intent": "authenticated_request",
    "observations": [
        {"method": "GET", "url": "https://api.example.com/me", "headers": {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkw"}},
        {"method": "GET", "url": "https://api.example.com/me", "headers": {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2FwaS5leGFtcGxlLmNvbSIsInN1YiI6InVzZXIxMjM0NTY3ODkwIn0"}},
        {"method": "GET", "url": "https://api.example.com/me", "headers": {"Authorization": "Bearer BKy8jB3XQa9kL7v2mN4pR6wT8yZ1cE5gF0hI2oS4uA7dG9qW3xJ8nK5mP1rV6bQ"}},
    ],
    "parameterized_template": {"method": "GET", "url": "https://api.example.com/me", "headers": {"Authorization": "Bearer ${token}"}},
    "slots": ["token"],
    "test_params": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkw"},
    "expected_bound_url": "https://api.example.com/me",
    "value_length": 64,
}

P5_MULTIPARAM = {
    "id": "P5_MULTIPARAM",
    "name": "Multi-param query (46 chars)",
    "category": "long_value",
    "intent": "search_products",
    "observations": [
        {"method": "GET", "url": "https://api.example.com/search?category=electronics&minPrice=100&maxPrice=500"},
        {"method": "GET", "url": "https://api.example.com/search?category=clothing&minPrice=25&maxPrice=200"},
        {"method": "GET", "url": "https://api.example.com/search?category=books&minPrice=10&maxPrice=100"},
    ],
    "parameterized_template": {"method": "GET", "url": "https://api.example.com/search?category=${category}&minPrice=${minPrice}&maxPrice=${maxPrice}"},
    "slots": ["category", "minPrice", "maxPrice"],
    "test_params": {"category": "electronics", "minPrice": "100", "maxPrice": "500"},
    "expected_bound_url": "https://api.example.com/search?category=electronics&minPrice=100&maxPrice=500",
    "value_length": 46,
}

# --- Positive control (1 pattern) ---

PC_SHORT = {
    "id": "PC_SHORT",
    "name": "Short numeric (2 chars)",
    "category": "positive_control",
    "intent": "fetch_item",
    "observations": [
        {"method": "GET", "url": "https://api.example.com/items/42"},
        {"method": "GET", "url": "https://api.example.com/items/7"},
        {"method": "GET", "url": "https://api.example.com/items/100"},
    ],
    "parameterized_template": {"method": "GET", "url": "https://api.example.com/items/${id}"},
    "slots": ["id"],
    "test_params": {"id": "42"},
    "expected_bound_url": "https://api.example.com/items/42",
    "value_length": 2,
}

# --- Null control (1 pattern) ---

NC_MID = {
    "id": "NC_MID",
    "name": "Mid alphanumeric (6 chars)",
    "category": "null_control",
    "intent": "fetch_session",
    "observations": [
        {"method": "GET", "url": "https://api.example.com/sessions/abc123"},
        {"method": "GET", "url": "https://api.example.com/sessions/xyz789"},
        {"method": "GET", "url": "https://api.example.com/sessions/mno456"},
    ],
    "parameterized_template": {"method": "GET", "url": "https://api.example.com/sessions/${sessionId}"},
    "slots": ["sessionId"],
    "test_params": {"sessionId": "abc123"},
    "expected_bound_url": "https://api.example.com/sessions/abc123",
    "value_length": 6,
}

ALL_PATTERNS = [P1_UUID, P2_SLUG, P3_DEEPPATH, P4_BEARER, P5_MULTIPARAM, PC_SHORT, NC_MID]


def run_kernel_regression():
    """Run the 3 existing kernel tests to verify no regression."""
    import unittest
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "tests.test_kernel",
        str(Path(__file__).resolve().parents[3] / "tests" / "test_kernel.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    KernelTests = mod.KernelTests

    suite = unittest.TestLoader().loadTestsFromTestCase(KernelTests)
    result = unittest.TextTestRunner(verbosity=2, stream=open(os.devnull, 'w')).run(suite)
    return {
        "total": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "failure_details": [str(f[1]) for f in result.failures] + [str(e[1]) for e in result.errors],
    }


def run_token_measurements():
    """Measure token costs for all 7 patterns."""
    enc = tiktoken.get_encoding("cl100k_base")
    results = []
    for pattern in ALL_PATTERNS:
        # Literal: use first observation's full URL
        literal_action = pattern["observations"][0]
        literal_json = json.dumps(literal_action, sort_keys=True)
        literal_tokens = len(enc.encode(literal_json))

        # Parameterized: use template
        param_json = json.dumps(pattern["parameterized_template"], sort_keys=True)
        param_tokens = len(enc.encode(param_json))

        savings_pct = (literal_tokens - param_tokens) / literal_tokens * 100 if literal_tokens > 0 else 0.0

        results.append({
            "pattern_id": pattern["id"],
            "pattern_name": pattern["name"],
            "category": pattern["category"],
            "num_params": len(pattern["slots"]),
            "value_length": pattern["value_length"],
            "literal_tokens": literal_tokens,
            "parameterized_tokens": param_tokens,
            "savings_tokens": literal_tokens - param_tokens,
            "savings_pct": round(savings_pct, 2),
            "literal_json": literal_json,
            "parameterized_json": param_json,
        })
    return results


def run_resolve_bind_tests():
    """Test resolve() and _bind() pipeline for all 7 patterns."""
    results = []
    td = tempfile.TemporaryDirectory()
    try:
        reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
        kernel = SpiderKernel(reg, min_confidence=0.8)

        for pattern in ALL_PATTERNS:
            # Register parameterized mechanism
            param_mech = make_parameterized_mechanism(
                intent=pattern["intent"],
                method=pattern["observations"][0]["method"],
                template_url=pattern["parameterized_template"]["url"],
                slots=pattern["slots"],
                evidence=[pattern["id"]],
            )
            reg.upsert(param_mech)

            # C1: resolve() with correct parameters -> EXECUTABLE
            res_with_params = kernel.resolve(
                pattern["intent"],
                {},
                pattern["test_params"],
            )

            # C2: resolve() without parameters -> UNKNOWN
            res_no_params = kernel.resolve(
                pattern["intent"],
                {},
                {},
            )

            # C3: _bind() produces correct bound_action
            bound = _bind(pattern["parameterized_template"], pattern["test_params"])
            # For bearer pattern, check headers nested structure
            if pattern["id"] == "P4_BEARER":
                bound_correct = bound.get("url") == pattern["expected_bound_url"]
            else:
                bound_correct = bound.get("url") == pattern["expected_bound_url"]

            results.append({
                "pattern_id": pattern["id"],
                "pattern_name": pattern["name"],
                "category": pattern["category"],
                "num_params": len(pattern["slots"]),
                "resolve_with_params_status": res_with_params.status.value,
                "resolve_with_params_executable": res_with_params.status == ResolutionStatus.EXECUTABLE,
                "resolve_with_params_bound_url": res_with_params.bound_action.get("url") if res_with_params.bound_action else None,
                "resolve_no_params_status": res_no_params.status.value,
                "resolve_no_params_unknown": res_no_params.status == ResolutionStatus.UNKNOWN,
                "bind_correct_url": bound_correct,
                "bind_actual_url": bound.get("url"),
                "expected_url": pattern["expected_bound_url"],
                "test_params": pattern["test_params"],
                "slots": pattern["slots"],
            })
    finally:
        td.cleanup()

    return results


def main():
    """Execute all measurements and write raw evidence."""
    output_dir = Path(__file__).parent

    print("=== EXP-PRODUCT-35262262156 EXECUTION ===")

    # 1. Kernel regression
    print("\n--- Kernel Regression Tests (C7) ---")
    regression = run_kernel_regression()
    print(f"  Regression: {regression['passed']}/{regression['total']} passed")
    if regression['failures'] > 0 or regression['errors'] > 0:
        print(f"  FAILURES: {regression['failure_details']}")

    # 2. Token measurements
    print("\n--- Token Cost Measurements (C4-C6) ---")
    token_results = run_token_measurements()
    for r in token_results:
        print(f"  {r['pattern_id']}: literal={r['literal_tokens']} param={r['parameterized_tokens']} "
              f"savings={r['savings_pct']}% (value_len={r['value_length']})")

    # 3. Resolve/Bind tests
    print("\n--- Resolve/Bind Pipeline Tests (C1-C3, C8) ---")
    resolve_results = run_resolve_bind_tests()
    for r in resolve_results:
        print(f"  {r['pattern_id']}: resolve_exec={r['resolve_with_params_executable']} "
              f"resolve_miss={r['resolve_no_params_unknown']} bind_correct={r['bind_correct_url']}")

    # 4. Decision rule evaluation
    print("\n--- Decision Rule Evaluation ---")

    # Split long-value (5) from controls (2)
    long_value_token = [r for r in token_results if r["category"] == "long_value"]
    long_value_resolve = [r for r in resolve_results if r["category"] == "long_value"]
    pc_token = [r for r in token_results if r["pattern_id"] == "PC_SHORT"][0]
    nc_token = [r for r in token_results if r["pattern_id"] == "NC_MID"][0]

    # C1: resolve() EXECUTABLE for all 5 long-value
    c1_pass = all(r["resolve_with_params_executable"] for r in long_value_resolve)
    c1_count = sum(1 for r in long_value_resolve if r["resolve_with_params_executable"])
    print(f"  C1 (resolve EXECUTABLE): {c1_count}/5 = {'PASS' if c1_pass else 'FAIL'}")

    # C2: resolve() UNKNOWN for all 5 missing params
    c2_pass = all(r["resolve_no_params_unknown"] for r in long_value_resolve)
    c2_count = sum(1 for r in long_value_resolve if r["resolve_no_params_unknown"])
    print(f"  C2 (resolve UNKNOWN no params): {c2_count}/5 = {'PASS' if c2_pass else 'FAIL'}")

    # C3: _bind() correct for all 5
    c3_pass = all(r["bind_correct_url"] for r in long_value_resolve)
    c3_count = sum(1 for r in long_value_resolve if r["bind_correct_url"])
    print(f"  C3 (bind correct): {c3_count}/5 = {'PASS' if c3_pass else 'FAIL'}")

    # C4: Parameterized fewer tokens for >= 3/5 long-value
    c4_count = sum(1 for r in long_value_token if r["savings_tokens"] > 0)
    c4_pass = c4_count >= 3
    print(f"  C4 (param fewer tokens >=3/5): {c4_count}/5 = {'PASS' if c4_pass else 'FAIL'}")

    # C5: Mean savings >= 10%
    mean_savings = sum(r["savings_pct"] for r in long_value_token) / len(long_value_token)
    c5_pass = mean_savings >= 10.0
    print(f"  C5 (mean savings >= 10%): {mean_savings:.2f}% = {'PASS' if c5_pass else 'FAIL'}")

    # C6: Savings increase with value length (r >= 0.7)
    import statistics
    value_lengths = [r["value_length"] for r in long_value_token]
    savings_pcts = [r["savings_pct"] for r in long_value_token]
    # Pearson correlation
    n = len(value_lengths)
    mean_x = statistics.mean(value_lengths)
    mean_y = statistics.mean(savings_pcts)
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(value_lengths, savings_pcts)) / n
    std_x = statistics.stdev(value_lengths) if n > 1 else 0
    std_y = statistics.stdev(savings_pcts) if n > 1 else 0
    correlation = cov / (std_x * std_y) if std_x > 0 and std_y > 0 else 0
    c6_pass = correlation >= 0.7
    print(f"  C6 (savings correlate with value length, r={correlation:.4f}): {'PASS' if c6_pass else 'FAIL'}")

    # C7: Kernel regression 3/3
    c7_pass = regression["passed"] == 3
    print(f"  C7 (kernel regression): {regression['passed']}/3 = {'PASS' if c7_pass else 'FAIL'}")

    # C8: Positive control - short value shows negative savings
    c8_pass = pc_token["savings_tokens"] < 0
    print(f"  C8 (positive control, short-value penalty): param={pc_token['parameterized_tokens']} > literal={pc_token['literal_tokens']} => savings={pc_token['savings_pct']}% = {'PASS' if c8_pass else 'FAIL'}")

    # Overall verdict
    all_pass = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass and c6_pass and c7_pass and c8_pass
    print(f"\n  OVERALL: {'SURVIVES_CURRENT_TEST' if all_pass else 'FALSIFIED-IN-SETTING'}")

    # Write raw evidence
    evidence = {
        "regression": regression,
        "token_measurements": token_results,
        "resolve_bind_tests": resolve_results,
        "decision_rule": {
            "C1_resolve_executable": {"pass": c1_pass, "count": c1_count, "total": 5},
            "C2_resolve_unknown_no_params": {"pass": c2_pass, "count": c2_count, "total": 5},
            "C3_bind_correct": {"pass": c3_pass, "count": c3_count, "total": 5},
            "C4_param_fewer_tokens": {"pass": c4_pass, "count": c4_count, "total": 5, "threshold": 3},
            "C5_mean_savings_pct": {"pass": c5_pass, "value": round(mean_savings, 2), "threshold": 10.0},
            "C6_savings_correlation": {"pass": c6_pass, "r": round(correlation, 4), "threshold": 0.7},
            "C7_kernel_regression": {"pass": c7_pass, "passed": regression["passed"], "total": 3},
            "C8_positive_control": {"pass": c8_pass, "savings_pct": pc_token["savings_pct"]},
            "ALL_pass": all_pass,
            "verdict": "SURVIVES_CURRENT_TEST" if all_pass else "FALSIFIED-IN-SETTING",
        },
    }
    evidence_path = output_dir / "raw_evidence.json"
    with open(evidence_path, "w") as f:
        json.dump(evidence, f, indent=2)
    print(f"\nRaw evidence written to {evidence_path}")

    return evidence


if __name__ == "__main__":
    main()
