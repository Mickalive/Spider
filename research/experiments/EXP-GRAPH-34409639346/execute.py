#!/usr/bin/env python3
"""
EXP-GRAPH-34409639346: Semantic Aliasing Resolution Test

Tests whether the kernel resolves semantically aliased URL templates
to the correct parametrized mechanism when both are registered with equal confidence.

Frozen design: exactly 4 baselines + 10 aliased pairs x 2 orderings = 24 kernel calls.

Naming convention: mechanism IDs are "a-XX" (always the smaller ID, alphabetically first)
and "z-XX" (always the larger ID). In correct-first ordering, "a-XX" is the correct
mechanism. In aliased-first ordering, "a-XX" is the aliased mechanism. This ensures
the registry's mechanism_id sort order controls which mechanism is tie-break selected.
"""

import json
import os
import sys
import tempfile
import hashlib
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from spider.kernel import SpiderKernel
from spider.registry import MechanismRegistry
from spider.models import Mechanism, ResolutionStatus

EXPERIMENT_DIR = Path(__file__).resolve().parent
RAW_EVIDENCE_DIR = EXPERIMENT_DIR / "raw_evidence"
RAW_EVIDENCE_DIR.mkdir(exist_ok=True)

# ============================================================
# 10 independent intent-template pairs
# ============================================================
PAIRS = [
    {
        "intent": "get-user-profile",
        "correct_template": {"url": "/users/${id}"},
        "aliased_template": {"url": "/accounts/${uid}"},
        "correct_slots": ["id"],
        "aliased_slots": ["uid"],
    },
    {
        "intent": "list-user-posts",
        "correct_template": {"url": "/users/${id}/posts"},
        "aliased_template": {"url": "/profiles/${uid}/entries"},
        "correct_slots": ["id"],
        "aliased_slots": ["uid"],
    },
    {
        "intent": "create-new-comment",
        "correct_template": {"url": "/posts/${id}/comments"},
        "aliased_template": {"url": "/articles/${id}/reviews"},
        "correct_slots": ["id"],
        "aliased_slots": ["id"],
    },
    {
        "intent": "delete-item",
        "correct_template": {"url": "/items/${itemId}"},
        "aliased_template": {"url": "/objects/${objId}"},
        "correct_slots": ["itemId"],
        "aliased_slots": ["objId"],
    },
    {
        "intent": "update-settings",
        "correct_template": {"url": "/users/${id}/settings"},
        "aliased_template": {"url": "/accounts/${id}/preferences"},
        "correct_slots": ["id"],
        "aliased_slots": ["id"],
    },
    {
        "intent": "search-content",
        "correct_template": {"url": "/search/${query}"},
        "aliased_template": {"url": "/find/${term}"},
        "correct_slots": ["query"],
        "aliased_slots": ["term"],
    },
    {
        "intent": "get-order-details",
        "correct_template": {"url": "/orders/${orderId}"},
        "aliased_template": {"url": "/purchases/${purchaseId}"},
        "correct_slots": ["orderId"],
        "aliased_slots": ["purchaseId"],
    },
    {
        "intent": "submit-form",
        "correct_template": {"url": "/forms/${formId}/submit"},
        "aliased_template": {"url": "/surveys/${surveyId}/respond"},
        "correct_slots": ["formId"],
        "aliased_slots": ["surveyId"],
    },
    {
        "intent": "upload-file",
        "correct_template": {"url": "/files/${fileId}/upload"},
        "aliased_template": {"url": "/documents/${docId}/store"},
        "correct_slots": ["fileId"],
        "aliased_slots": ["docId"],
    },
    {
        "intent": "fetch-analytics",
        "correct_template": {"url": "/analytics/${metricId}"},
        "aliased_template": {"url": "/metrics/${indicatorId}"},
        "correct_slots": ["metricId"],
        "aliased_slots": ["indicatorId"],
    },
]

# ============================================================
# Helper functions
# ============================================================

def make_params(pair):
    """Create params dict that satisfies both parameter_slots."""
    params = {}
    for slot in pair["correct_slots"]:
        params[slot] = 42
    for slot in pair["aliased_slots"]:
        params[slot] = 42
    return params


def make_mechanism(mech_id, pair, confidence=0.9, is_correct=True):
    """Create a mechanism for the given pair."""
    template = pair["correct_template"] if is_correct else pair["aliased_template"]
    slots = pair["correct_slots"] if is_correct else pair["aliased_slots"]
    return Mechanism(
        mechanism_id=mech_id,
        intent=pair["intent"],
        preconditions={},
        action_template=template,
        postconditions={},
        parameter_slots=slots,
        confidence=confidence,
    )


def run_condition(kernel, intent, context, params, condition_id):
    """Run a single resolution condition and return the result."""
    try:
        resolution = kernel.resolve(intent, context, params)
        return {
            "condition_id": condition_id,
            "status": resolution.status.value,
            "mechanism_id": resolution.mechanism_id,
            "bound_action": resolution.bound_action,
            "confidence": resolution.confidence,
            "reason": resolution.reason,
            "error": None,
        }
    except Exception as e:
        return {
            "condition_id": condition_id,
            "status": "EXCEPTION",
            "mechanism_id": None,
            "bound_action": None,
            "confidence": 0.0,
            "reason": str(e),
            "error": type(e).__name__,
        }


def create_fresh_kernel(mechanisms):
    """Create a fresh kernel with the given mechanisms in a temp directory."""
    tmpdir = tempfile.mkdtemp(prefix="spider_exp_")
    registry_path = os.path.join(tmpdir, "registry.jsonl")
    registry = MechanismRegistry(registry_path)
    for m in mechanisms:
        registry.upsert(m)
    kernel = SpiderKernel(registry, min_confidence=0.8)
    return kernel, tmpdir


# ============================================================
# Baseline conditions
# ============================================================

def run_baselines():
    """Run all 4 baseline conditions."""
    results = []

    # B-EMPTY-REGISTRY
    kernel, tmpdir = create_fresh_kernel([])
    res = run_condition(kernel, "get-user-profile", {}, {}, "B-EMPTY-REGISTRY")
    expected = "UNKNOWN"
    res["expected_status"] = expected
    res["passed"] = res["status"] == expected
    results.append(res)

    # B-SINGLE-MECHANISM
    m1 = make_mechanism("a-01", PAIRS[0], confidence=0.9, is_correct=True)
    kernel, tmpdir = create_fresh_kernel([m1])
    params = make_params(PAIRS[0])
    res = run_condition(kernel, PAIRS[0]["intent"], {}, params, "B-SINGLE-MECHANISM")
    expected = "EXECUTABLE"
    res["expected_status"] = expected
    res["expected_mechanism_id"] = "a-01"
    res["passed"] = (res["status"] == expected and res["mechanism_id"] == "a-01")
    results.append(res)

    # B-CONFIDENCE-HIGHER: Two mechanisms with DIFFERENT intents, different confidences
    m_high = make_mechanism("a-high", PAIRS[0], confidence=0.95, is_correct=True)
    m_low = make_mechanism("z-low", PAIRS[1], confidence=0.8, is_correct=True)
    kernel, tmpdir = create_fresh_kernel([m_high, m_low])
    res = run_condition(kernel, PAIRS[0]["intent"], {}, make_params(PAIRS[0]), "B-CONFIDENCE-HIGHER")
    expected = "EXECUTABLE"
    res["expected_status"] = expected
    res["expected_mechanism_id"] = "a-high"
    res["passed"] = (res["status"] == expected and res["mechanism_id"] == "a-high")
    results.append(res)

    # B-CONFIDENCE-EQUAL-DIFFERENT-INTENT: Two mechanisms, different intents, equal confidence
    m_a = make_mechanism("a-01", PAIRS[0], confidence=0.9, is_correct=True)
    m_b = make_mechanism("z-01", PAIRS[1], confidence=0.9, is_correct=True)
    kernel, tmpdir = create_fresh_kernel([m_a, m_b])
    res = run_condition(kernel, PAIRS[0]["intent"], {}, make_params(PAIRS[0]), "B-CONFIDENCE-EQUAL-DIFFERENT-INTENT")
    expected = "EXECUTABLE"
    res["expected_status"] = expected
    res["expected_mechanism_id"] = "a-01"
    res["passed"] = (res["status"] == expected and res["mechanism_id"] == "a-01")
    results.append(res)

    return results


# ============================================================
# Aliased pair conditions
# ============================================================

def run_aliased_pairs():
    """Run 10 aliased pairs, each with correct-first and aliased-first orderings.

    Naming convention:
    - "a-XX" is always the mechanism with the smaller ID (alphabetically first)
    - "z-XX" is always the mechanism with the larger ID
    - In correct-first: a-XX = correct mechanism, z-XX = aliased mechanism
    - In aliased-first: a-XX = aliased mechanism, z-XX = correct mechanism

    This ensures the registry's mechanism_id sort order controls tie-breaking.
    """
    results = []

    for i, pair in enumerate(PAIRS):
        pair_num = i + 1
        params = make_params(pair)

        # IDs: a-XX is always the smaller one
        small_id = f"a-{pair_num:02d}"
        large_id = f"z-{pair_num:02d}"

        # ---- Correct-first ordering ----
        # a-XX = correct (smaller ID, tie-break selects it)
        # z-XX = aliased (larger ID, loses tie-break)
        m_correct = make_mechanism(small_id, pair, confidence=0.9, is_correct=True)
        m_aliased = make_mechanism(large_id, pair, confidence=0.9, is_correct=False)

        kernel, tmpdir = create_fresh_kernel([m_correct, m_aliased])
        res_correct = run_condition(
            kernel, pair["intent"], {}, params,
            f"PAIR-{pair_num}-CORRECT-FIRST"
        )
        res_correct["pair_num"] = pair_num
        res_correct["ordering"] = "correct-first"
        res_correct["small_id"] = small_id
        res_correct["large_id"] = large_id
        res_correct["small_is"] = "correct"
        # Expected: kernel selects small_id (tie-breaking picks smaller ID)
        res_correct["expected_mechanism_id"] = small_id
        res_correct["passed"] = (res_correct["mechanism_id"] == small_id)
        results.append(res_correct)

        # ---- Aliased-first ordering ----
        # a-XX = aliased (smaller ID, tie-break selects it)
        # z-XX = correct (larger ID, loses tie-break)
        m_aliased_rev = make_mechanism(small_id, pair, confidence=0.9, is_correct=False)
        m_correct_rev = make_mechanism(large_id, pair, confidence=0.9, is_correct=True)

        kernel, tmpdir = create_fresh_kernel([m_aliased_rev, m_correct_rev])
        res_aliased = run_condition(
            kernel, pair["intent"], {}, params,
            f"PAIR-{pair_num}-ALIASED-FIRST"
        )
        res_aliased["pair_num"] = pair_num
        res_aliased["ordering"] = "aliased-first"
        res_aliased["small_id"] = small_id
        res_aliased["large_id"] = large_id
        res_aliased["small_is"] = "aliased"
        # Expected if NO semantic resolution: kernel selects small_id (aliased)
        # Expected IF semantic resolution: kernel selects large_id (correct)
        res_aliased["expected_tie_breaking"] = small_id
        res_aliased["expected_semantic"] = large_id
        res_aliased["follows_tie_breaking"] = (res_aliased["mechanism_id"] == small_id)
        res_aliased["selects_correct"] = (res_aliased["mechanism_id"] == large_id)
        results.append(res_aliased)

    return results


# ============================================================
# Main execution
# ============================================================

def main():
    print(f"=== EXP-GRAPH-34409639346 Execution ===")
    print(f"Time: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}")
    print()

    # Run baselines
    print("--- Running Baseline Conditions ---")
    baseline_results = run_baselines()
    for r in baseline_results:
        status_icon = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status_icon}] {r['condition_id']}: {r['status']} (expected: {r['expected_status']})")
        if r.get("error"):
            print(f"       ERROR: {r['error']}: {r['reason']}")

    print()

    # Run aliased pairs
    print("--- Running Aliased Pair Conditions ---")
    pair_results = run_aliased_pairs()
    for r in pair_results:
        if r["ordering"] == "aliased-first":
            icon = "TIE" if r["follows_tie_breaking"] else "SEM"
            print(f"  [{icon}] {r['condition_id']}: selected={r['mechanism_id']} "
                  f"(tie_break={r['expected_tie_breaking']}, "
                  f"semantic={r['expected_semantic']})")
        else:
            icon = "OK" if r["passed"] else "UNEXPECTED"
            print(f"  [{icon}] {r['condition_id']}: selected={r['mechanism_id']} "
                  f"(expected: {r['expected_mechanism_id']})")

    print()

    # Compute metrics
    baselines_passed = all(r["passed"] for r in baseline_results)
    exceptions = [r for r in baseline_results + pair_results if r.get("error")]

    # Aliased-first subset
    aliased_first_results = [r for r in pair_results if r["ordering"] == "aliased-first"]
    n_aliased_first = len(aliased_first_results)
    n_selects_correct = sum(1 for r in aliased_first_results if r["selects_correct"])
    aliased_first_correct_selection_rate = n_selects_correct / n_aliased_first if n_aliased_first > 0 else 0.0

    # Correct-first subset
    correct_first_results = [r for r in pair_results if r["ordering"] == "correct-first"]
    n_correct_first = len(correct_first_results)
    n_correct_first_correct = sum(1 for r in correct_first_results if r["passed"])
    correct_first_correct_selection_rate = n_correct_first_correct / n_correct_first if n_correct_first > 0 else 0.0

    # Binomial test
    binomial_p = None
    try:
        from scipy.stats import binomtest
        k = n_selects_correct
        n = n_aliased_first
        result = binomtest(k, n, 0.5, alternative='greater')
        binomial_p = result.pvalue
    except ImportError:
        from math import comb
        n = n_aliased_first
        k = n_selects_correct
        if k == 0:
            binomial_p = 1.0
        else:
            p_value = 0.0
            for i in range(k, n + 1):
                p_value += comb(n, i) * (0.5 ** n)
            binomial_p = p_value

    print("--- Metrics ---")
    print(f"  baselines_passed: {baselines_passed}")
    print(f"  exceptions: {len(exceptions)}")
    print(f"  aliased_first_correct_selection_rate: {aliased_first_correct_selection_rate} ({n_selects_correct}/{n_aliased_first})")
    print(f"  correct_first_correct_selection_rate: {correct_first_correct_selection_rate} ({n_correct_first_correct}/{n_correct_first})")
    print(f"  binomial_p (one-sided, H1: p>0.5): {binomial_p}")
    print()

    # Determine outcome
    if not baselines_passed or len(exceptions) > 0:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        print("  STATUS: MEASUREMENT_INVALID (baseline failure or exceptions)")
    elif aliased_first_correct_selection_rate >= 0.1:
        # >=1/10 correct selections in aliased-first
        status = "COMPLETE"
        outcome = "FALSIFIES"
        print(f"  OUTCOME: FALSIFIES (kernel selects correct mechanism in {n_selects_correct}/{n_aliased_first} aliased-first conditions)")
    else:
        status = "COMPLETE"
        outcome = "SUPPORTS"
        print(f"  OUTCOME: SUPPORTS (kernel follows tie-breaking exactly, 0/{n_aliased_first} correct selections in aliased-first)")

    # Collect all observations
    all_observations = []
    for r in baseline_results:
        all_observations.append({
            "type": "baseline",
            "condition_id": r["condition_id"],
            "status": r["status"],
            "mechanism_id": r["mechanism_id"],
            "passed": r["passed"],
            "expected": r.get("expected_status"),
        })
    for r in pair_results:
        obs = {
            "type": "aliased_pair",
            "condition_id": r["condition_id"],
            "pair_num": r["pair_num"],
            "ordering": r["ordering"],
            "status": r["status"],
            "mechanism_id": r["mechanism_id"],
        }
        if r["ordering"] == "aliased-first":
            obs["follows_tie_breaking"] = r["follows_tie_breaking"]
            obs["selects_correct"] = r["selects_correct"]
        else:
            obs["passed"] = r["passed"]
        all_observations.append(obs)

    # Save raw evidence
    raw_evidence = {
        "experiment_id": "EXP-GRAPH-34409639346",
        "execution_time": time.strftime('%Y-%m-%dT%H:%M:%S%z'),
        "baseline_results": baseline_results,
        "pair_results": pair_results,
        "metrics": {
            "baselines_passed": baselines_passed,
            "exceptions_count": len(exceptions),
            "aliased_first_correct_selection_rate": aliased_first_correct_selection_rate,
            "correct_first_correct_selection_rate": correct_first_correct_selection_rate,
            "binomial_p": binomial_p,
            "n_aliased_first": n_aliased_first,
            "n_selects_correct": n_selects_correct,
            "n_correct_first": n_correct_first,
            "n_correct_first_correct": n_correct_first_correct,
        },
        "status": status,
        "outcome": outcome,
    }

    raw_path = RAW_EVIDENCE_DIR / "execution_results.json"
    with open(raw_path, "w") as f:
        json.dump(raw_evidence, f, indent=2)
    print(f"\n  Raw evidence saved to: {raw_path}")

    # Compute SHA256 of raw evidence
    with open(raw_path, "rb") as f:
        raw_sha256 = hashlib.sha256(f.read()).hexdigest()
    print(f"  Raw evidence SHA256: {raw_sha256}")

    return raw_evidence, raw_sha256


if __name__ == "__main__":
    raw_evidence, raw_sha256 = main()
