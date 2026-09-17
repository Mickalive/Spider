#!/usr/bin/env python3
"""EXP-PRODUCT-35209109455: Execute frozen experiment design.

Tests:
1. Token cost comparison: parameterized vs literal mechanisms across 5 URL patterns
2. resolve() pipeline: EXECUTABLE with correct bound_action for parameterized mechanisms
3. Null control: UNKNOWN when parameters missing
4. _bind() correctness for all 5 patterns
5. Kernel regression: 3 existing tests pass
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
# 5 URL patterns from frozen prereg
# ============================================================

PATTERNS = [
    {
        "id": "pattern_1",
        "name": "Single path parameter (1 param)",
        "intent": "fetch_user",
        "observations": [
            {"method": "GET", "url": "https://api.example.com/users/1"},
            {"method": "GET", "url": "https://api.example.com/users/2"},
            {"method": "GET", "url": "https://api.example.com/users/3"},
        ],
        "parameterized_template": {"method": "GET", "url": "https://api.example.com/users/${id}"},
        "slots": ["id"],
        "test_params": {"id": "42"},
        "expected_bound_url": "https://api.example.com/users/42",
    },
    {
        "id": "pattern_2",
        "name": "Single query parameter (1 param)",
        "intent": "fetch_comments",
        "observations": [
            {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=1"},
            {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=2"},
            {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=3"},
        ],
        "parameterized_template": {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=${id}"},
        "slots": ["id"],
        "test_params": {"id": "5"},
        "expected_bound_url": "https://jsonplaceholder.typicode.com/comments?postId=5",
    },
    {
        "id": "pattern_3",
        "name": "Two query parameters (2 params)",
        "intent": "search_posts",
        "observations": [
            {"method": "GET", "url": "https://api.example.com/posts?userId=1&limit=10"},
            {"method": "GET", "url": "https://api.example.com/posts?userId=2&limit=20"},
            {"method": "GET", "url": "https://api.example.com/posts?userId=3&limit=30"},
        ],
        "parameterized_template": {"method": "GET", "url": "https://api.example.com/posts?userId=${userId}&limit=${limit}"},
        "slots": ["userId", "limit"],
        "test_params": {"userId": "5", "limit": "25"},
        "expected_bound_url": "https://api.example.com/posts?userId=5&limit=25",
    },
    {
        "id": "pattern_4",
        "name": "Path + query parameter (2 params, mixed)",
        "intent": "fetch_user_posts",
        "observations": [
            {"method": "GET", "url": "https://api.example.com/users/1/posts?page=1"},
            {"method": "GET", "url": "https://api.example.com/users/2/posts?page=2"},
            {"method": "GET", "url": "https://api.example.com/users/3/posts?page=3"},
        ],
        "parameterized_template": {"method": "GET", "url": "https://api.example.com/users/${userId}/posts?page=${page}"},
        "slots": ["userId", "page"],
        "test_params": {"userId": "5", "page": "3"},
        "expected_bound_url": "https://api.example.com/users/5/posts?page=3",
    },
    {
        "id": "pattern_5",
        "name": "Three query parameters (3 params)",
        "intent": "filter_products",
        "observations": [
            {"method": "GET", "url": "https://api.example.com/products?category=books&minPrice=10&maxPrice=50"},
            {"method": "GET", "url": "https://api.example.com/products?category=electronics&minPrice=20&maxPrice=100"},
            {"method": "GET", "url": "https://api.example.com/products?category=clothing&minPrice=5&maxPrice=30"},
        ],
        "parameterized_template": {"method": "GET", "url": "https://api.example.com/products?category=${category}&minPrice=${minPrice}&maxPrice=${maxPrice}"},
        "slots": ["category", "minPrice", "maxPrice"],
        "test_params": {"category": "tools", "minPrice": "15", "maxPrice": "75"},
        "expected_bound_url": "https://api.example.com/products?category=tools&minPrice=15&maxPrice=75",
    },
]


def run_kernel_regression():
    """Run the 3 existing kernel tests to verify no regression."""
    import unittest
    import importlib.util
    
    # Load test module from tests/test_kernel.py
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
    """Measure token costs for all 5 patterns."""
    results = []
    for pattern in PATTERNS:
        # Literal: use first observation's full URL
        literal_action = pattern["observations"][0]
        literal_tokens = count_tokens(literal_action)
        
        # Parameterized: use template
        param_tokens = count_tokens(pattern["parameterized_template"])
        
        savings_pct = (literal_tokens - param_tokens) / literal_tokens * 100
        
        results.append({
            "pattern_id": pattern["id"],
            "pattern_name": pattern["name"],
            "num_params": len(pattern["slots"]),
            "literal_tokens": literal_tokens,
            "parameterized_tokens": param_tokens,
            "savings_tokens": literal_tokens - param_tokens,
            "savings_pct": round(savings_pct, 2),
            "literal_action": literal_action,
            "parameterized_action": pattern["parameterized_template"],
        })
    return results


def run_resolve_bind_tests():
    """Test resolve() and _bind() pipeline for all 5 patterns."""
    results = []
    td = tempfile.TemporaryDirectory()
    try:
        reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
        kernel = SpiderKernel(reg, min_confidence=0.8)
        
        for pattern in PATTERNS:
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
            bound_correct = bound.get("url") == pattern["expected_bound_url"]
            
            results.append({
                "pattern_id": pattern["id"],
                "pattern_name": pattern["name"],
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
    
    print("=== EXP-PRODUCT-35209109455 EXECUTION ===")
    
    # 1. Kernel regression
    print("\n--- Kernel Regression Tests ---")
    regression = run_kernel_regression()
    print(f"  Regression: {regression['passed']}/{regression['total']} passed")
    
    # 2. Token measurements
    print("\n--- Token Cost Measurements ---")
    token_results = run_token_measurements()
    for r in token_results:
        print(f"  {r['pattern_id']}: literal={r['literal_tokens']} param={r['parameterized_tokens']} savings={r['savings_pct']}%")
    
    # 3. Resolve/Bind tests
    print("\n--- Resolve/Bind Pipeline Tests ---")
    resolve_results = run_resolve_bind_tests()
    for r in resolve_results:
        print(f"  {r['pattern_id']}: resolve_exec={r['resolve_with_params_executable']} "
              f"resolve_miss={r['resolve_no_params_unknown']} bind_correct={r['bind_correct_url']}")
    
    # Write raw evidence
    evidence = {
        "regression": regression,
        "token_measurements": token_results,
        "resolve_bind_tests": resolve_results,
    }
    evidence_path = output_dir / "raw_evidence.json"
    with open(evidence_path, "w") as f:
        json.dump(evidence, f, indent=2)
    print(f"\nRaw evidence written to {evidence_path}")
    
    return evidence


if __name__ == "__main__":
    main()
