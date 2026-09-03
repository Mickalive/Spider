#!/usr/bin/env python3
"""EXP-GRAPH-33718012817 — Execute frozen experiment: literal vs parameterized mechanism competition.

This script creates fresh kernel instances for each condition, registers the specified
mechanisms, resolves with the given params, and records all raw evidence.

No HTTP execution is performed — only kernel resolution and bound_action correctness are measured.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.spider.kernel import SpiderKernel
from src.spider.models import Mechanism
from src.spider.registry import MechanismRegistry

# --- Mechanism definitions (frozen spec) ---

MECHANISMS = {
    "literal-fetch-posts-1": Mechanism(
        mechanism_id="literal-fetch-posts-1",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/1"},
        postconditions={"status": 200, "has_keys": ["userId", "id", "title", "body"]},
        parameter_slots=[],
        confidence=0.95,
    ),
    "param-fetch-posts": Mechanism(
        mechanism_id="param-fetch-posts",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/${id}"},
        postconditions={"status": 200, "has_keys": ["userId", "id", "title", "body"]},
        parameter_slots=["id"],
        confidence=0.95,
    ),
    "param-fetch-posts-higher": Mechanism(
        mechanism_id="param-fetch-posts-higher",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/${id}"},
        postconditions={"status": 200, "has_keys": ["userId", "id", "title", "body"]},
        parameter_slots=["id"],
        confidence=0.98,
    ),
    "literal-fetch-posts-1-higher": Mechanism(
        mechanism_id="literal-fetch-posts-1-higher",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/1"},
        postconditions={"status": 200, "has_keys": ["userId", "id", "title", "body"]},
        parameter_slots=[],
        confidence=0.98,
    ),
}

# --- Registry configurations ---

REGISTRY_CONFIGS = {
    "empty": [],
    "literal-only": ["literal-fetch-posts-1"],
    "param-only": ["param-fetch-posts"],
    "shared-equal": ["literal-fetch-posts-1", "param-fetch-posts"],
    "shared-param-higher": ["literal-fetch-posts-1", "param-fetch-posts-higher"],
    "shared-literal-higher": ["literal-fetch-posts-1-higher", "param-fetch-posts"],
}

# --- Conditions (frozen spec) ---

CONDITIONS = [
    {"id": "cold", "registry": "empty", "params": {"id": 2}, "expected_resolution": "UNKNOWN", "expected_url": None, "expected_winning_mechanism": None},
    {"id": "literal-only-original", "registry": "literal-only", "params": {"id": 1}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1"},
    {"id": "literal-only-unseen", "registry": "literal-only", "params": {"id": 2}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1"},
    {"id": "param-only-original", "registry": "param-only", "params": {"id": 1}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "param-fetch-posts"},
    {"id": "param-only-unseen", "registry": "param-only", "params": {"id": 2}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/2", "expected_winning_mechanism": "param-fetch-posts"},
    {"id": "compete-equal-id1", "registry": "shared-equal", "params": {"id": 1}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1"},
    {"id": "compete-equal-id2", "registry": "shared-equal", "params": {"id": 2}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1"},
    {"id": "compete-equal-id3", "registry": "shared-equal", "params": {"id": 3}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1"},
    {"id": "compete-equal-id4", "registry": "shared-equal", "params": {"id": 4}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1"},
    {"id": "compete-equal-id5", "registry": "shared-equal", "params": {"id": 5}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1"},
    {"id": "compete-equal-id6", "registry": "shared-equal", "params": {"id": 6}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1"},
    {"id": "compete-param-higher", "registry": "shared-param-higher", "params": {"id": 3}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/3", "expected_winning_mechanism": "param-fetch-posts-higher"},
    {"id": "compete-literal-higher", "registry": "shared-literal-higher", "params": {"id": 3}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1-higher"},
]


def run_condition(condition: dict) -> dict:
    """Execute a single condition with a fresh kernel instance."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry_path = os.path.join(tmpdir, "registry.jsonl")
        registry = MechanismRegistry(registry_path)

        # Register mechanisms in specified order
        mech_ids = REGISTRY_CONFIGS[condition["registry"]]
        for mid in mech_ids:
            registry.upsert(MECHANISMS[mid])

        kernel = SpiderKernel(registry, min_confidence=0.8)

        # Resolve
        resolution = kernel.resolve("fetch", {}, params=condition["params"])

        # Extract bound_action URL
        bound_url = None
        if resolution.bound_action is not None:
            bound_url = resolution.bound_action.get("url")

        return {
            "condition_id": condition["id"],
            "resolution_status": resolution.status.value,
            "winning_mechanism_id": resolution.mechanism_id,
            "resolution_reason": resolution.reason,
            "bound_action": resolution.bound_action,
            "bound_url": bound_url,
            "confidence": resolution.confidence,
            "expected_resolution": condition["expected_resolution"],
            "expected_url": condition["expected_url"],
            "expected_winning_mechanism": condition["expected_winning_mechanism"],
            "match_expected_resolution": resolution.status.value == condition["expected_resolution"],
            "match_expected_url": bound_url == condition["expected_url"],
            "match_expected_winner": resolution.mechanism_id == condition["expected_winning_mechanism"],
        }


def main():
    results = []
    for cond in CONDITIONS:
        print(f"Running condition: {cond['id']}...", flush=True)
        result = run_condition(cond)
        results.append(result)
        print(f"  -> {result['resolution_status']} | winner={result['winning_mechanism_id']} | url={result['bound_url']}", flush=True)

    # Write raw results
    output_path = Path(__file__).parent / "raw_evidence.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nRaw evidence written to {output_path}")

    # Print summary
    print("\n=== SUMMARY ===")
    for r in results:
        status = "PASS" if (r["match_expected_resolution"] and r["match_expected_url"] and r["match_expected_winner"]) else "FAIL"
        print(f"  {r['condition_id']:30s} | {r['resolution_status']:12s} | winner={str(r['winning_mechanism_id']):30s} | url={str(r['bound_url']):60s} | {status}")


if __name__ == "__main__":
    main()
