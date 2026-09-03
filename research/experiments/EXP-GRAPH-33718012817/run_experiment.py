#!/usr/bin/env python3
"""
EXP-GRAPH-33718012817 — Execute frozen experiment.
Tests whether literal universal matching causes false accepts
when literal and parameterized mechanisms coexist in a shared registry.
"""

import json
import hashlib
import sys
import os
import traceback
from pathlib import Path
from datetime import datetime, timezone

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from spider.models import Mechanism, Observation, ResolutionStatus
from spider.registry import MechanismRegistry
from spider.kernel import SpiderKernel

EXPERIMENT_DIR = Path(__file__).parent
RAW_EVIDENCE_PATH = EXPERIMENT_DIR / "raw_evidence.jsonl"

def make_mechanisms():
    """Create the four mechanism definitions used across conditions."""
    literal = Mechanism(
        mechanism_id="literal-fetch-posts-1",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/1"},
        postconditions={"status": 200, "has_keys": ["userId", "id", "title", "body"]},
        parameter_slots=[],
        confidence=0.95,
    )
    param = Mechanism(
        mechanism_id="param-fetch-posts",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/${id}"},
        postconditions={"status": 200, "has_keys": ["userId", "id", "title", "body"]},
        parameter_slots=["id"],
        confidence=0.95,
    )
    param_higher = Mechanism(
        mechanism_id="param-fetch-posts-higher",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/${id}"},
        postconditions={"status": 200, "has_keys": ["userId", "id", "title", "body"]},
        parameter_slots=["id"],
        confidence=0.98,
    )
    literal_higher = Mechanism(
        mechanism_id="literal-fetch-posts-1-higher",
        intent="fetch",
        preconditions={},
        action_template={"method": "GET", "url": "https://jsonplaceholder.typicode.com/posts/1"},
        postconditions={"status": 200, "has_keys": ["userId", "id", "title", "body"]},
        parameter_slots=[],
        confidence=0.98,
    )
    return {
        "literal": literal,
        "param": param,
        "param_higher": param_higher,
        "literal_higher": literal_higher,
    }

def make_registry_configs(mechs):
    """Define which mechanisms go into each registry configuration."""
    return {
        "empty": [],
        "literal-only": [mechs["literal"]],
        "param-only": [mechs["param"]],
        "shared-equal": [mechs["literal"], mechs["param"]],
        "shared-param-higher": [mechs["literal"], mechs["param_higher"]],
        "shared-literal-higher": [mechs["literal_higher"], mechs["param"]],
    }

def make_conditions():
    """Define all 13 experimental conditions."""
    return [
        {"id": "cold", "registry": "empty", "params": {"id": 2},
         "expected_resolution": "UNKNOWN", "expected_url": None,
         "expected_winning_mechanism": None},
        {"id": "literal-only-original", "registry": "literal-only", "params": {"id": 1},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
         "expected_winning_mechanism": "literal-fetch-posts-1"},
        {"id": "literal-only-unseen", "registry": "literal-only", "params": {"id": 2},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
         "expected_winning_mechanism": "literal-fetch-posts-1"},
        {"id": "param-only-original", "registry": "param-only", "params": {"id": 1},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
         "expected_winning_mechanism": "param-fetch-posts"},
        {"id": "param-only-unseen", "registry": "param-only", "params": {"id": 2},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/2",
         "expected_winning_mechanism": "param-fetch-posts"},
        {"id": "compete-equal-id1", "registry": "shared-equal", "params": {"id": 1},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
         "expected_winning_mechanism": "literal-fetch-posts-1"},
        {"id": "compete-equal-id2", "registry": "shared-equal", "params": {"id": 2},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
         "expected_winning_mechanism": "literal-fetch-posts-1"},
        {"id": "compete-equal-id3", "registry": "shared-equal", "params": {"id": 3},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
         "expected_winning_mechanism": "literal-fetch-posts-1"},
        {"id": "compete-equal-id4", "registry": "shared-equal", "params": {"id": 4},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
         "expected_winning_mechanism": "literal-fetch-posts-1"},
        {"id": "compete-equal-id5", "registry": "shared-equal", "params": {"id": 5},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
         "expected_winning_mechanism": "literal-fetch-posts-1"},
        {"id": "compete-equal-id6", "registry": "shared-equal", "params": {"id": 6},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
         "expected_winning_mechanism": "literal-fetch-posts-1"},
        {"id": "compete-param-higher", "registry": "shared-param-higher", "params": {"id": 3},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/3",
         "expected_winning_mechanism": "param-fetch-posts-higher"},
        {"id": "compete-literal-higher", "registry": "shared-literal-higher", "params": {"id": 3},
         "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
         "expected_winning_mechanism": "literal-fetch-posts-1-higher"},
    ]

def run_condition(condition, registry_configs, mechs):
    """Run a single experimental condition and return raw evidence."""
    config_name = condition["registry"]
    mechanism_list = registry_configs[config_name]

    # Create a fresh temporary registry file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        reg_path = f.name
        for m in mechanism_list:
            f.write(json.dumps(m.as_dict(), sort_keys=True) + "\n")

    try:
        registry = MechanismRegistry(reg_path)
        kernel = SpiderKernel(registry)

        # Run resolution
        resolution = kernel.resolve("fetch", {}, condition["params"])

        # Collect raw evidence
        raw = {
            "condition_id": condition["id"],
            "registry_config": config_name,
            "mechanisms_registered": [m.mechanism_id for m in mechanism_list],
            "mechanism_insertion_order": [m.mechanism_id for m in mechanism_list],
            "params": condition["params"],
            "resolution_status": resolution.status.value,
            "resolution_mechanism_id": resolution.mechanism_id,
            "resolution_reason": resolution.reason,
            "bound_action": resolution.bound_action,
            "confidence": resolution.confidence,
            "expected_resolution": condition["expected_resolution"],
            "expected_url": condition["expected_url"],
            "expected_winning_mechanism": condition["expected_winning_mechanism"],
        }
        return raw
    finally:
        os.unlink(reg_path)

def main():
    mechs = make_mechanisms()
    registry_configs = make_registry_configs(mechs)
    conditions = make_conditions()

    results = []
    raw_evidence_lines = []

    for cond in conditions:
        raw = run_condition(cond, registry_configs, mechs)
        results.append(raw)
        raw_evidence_lines.append(json.dumps(raw, sort_keys=True))

        # Write raw evidence line immediately
        with open(RAW_EVIDENCE_PATH, "a") as f:
            f.write(json.dumps(raw, sort_keys=True) + "\n")

        # Print progress
        status_match = "PASS" if raw["resolution_status"] == raw["expected_resolution"] else "FAIL"
        url_match = "PASS" if raw["bound_action"] and raw["bound_action"].get("url") == raw["expected_url"] else (
            "PASS" if raw["expected_url"] is None and raw["bound_action"] is None else "FAIL"
        )
        mech_match = "PASS" if raw["resolution_mechanism_id"] == raw["expected_winning_mechanism"] else "FAIL"
        print(f"  [{status_match}] {raw['condition_id']}: status={raw['resolution_status']} "
              f"mech={raw['resolution_mechanism_id']} url={raw['bound_action'] and raw['bound_action'].get('url')}")

    # Summary
    print("\n=== Summary ===")
    print(f"Total conditions: {len(results)}")

    # Evaluate decision rule
    cold_ok = results[0]["resolution_status"] == "UNKNOWN"
    lit_orig_ok = results[1]["resolution_status"] == "EXECUTABLE" and results[1]["bound_action"]["url"] == "https://jsonplaceholder.typicode.com/posts/1"
    lit_unseen_ok = results[2]["resolution_status"] == "EXECUTABLE" and results[2]["bound_action"]["url"] == "https://jsonplaceholder.typicode.com/posts/1"
    param_orig_ok = results[3]["resolution_status"] == "EXECUTABLE" and results[3]["bound_action"]["url"] == "https://jsonplaceholder.typicode.com/posts/1"
    param_unseen_ok = results[4]["resolution_status"] == "EXECUTABLE" and results[4]["bound_action"]["url"] == "https://jsonplaceholder.typicode.com/posts/2"

    # Competition conditions: id2..id6
    compete_ids = [5, 6, 7, 8, 9]  # indices for compete-equal-id2 through id6
    literal_wins_all = all(results[i]["resolution_mechanism_id"] == "literal-fetch-posts-1" for i in compete_ids)
    literal_wrong_url = all(
        results[i]["bound_action"]["url"] == "https://jsonplaceholder.typicode.com/posts/1"
        for i in compete_ids
    )

    param_higher_ok = results[11]["resolution_mechanism_id"] == "param-fetch-posts-higher"
    literal_higher_ok = results[12]["resolution_mechanism_id"] == "literal-fetch-posts-1-higher"

    baselines_pass = cold_ok and lit_orig_ok and lit_unseen_ok and param_orig_ok and param_unseen_ok
    disambig_pass = param_higher_ok and literal_higher_ok

    # COMPETITION-SAFE: parameterized wins at equal confidence OR literal doesn't win
    # COMPETITION-UNSAFE: literal wins AND produces wrong URL
    competition_unsafe = literal_wins_all and literal_wrong_url
    competition_safe = not competition_unsafe

    print(f"Cold baseline: {'PASS' if cold_ok else 'FAIL'}")
    print(f"Literal standalone: {'PASS' if lit_orig_ok else 'FAIL'}")
    print(f"Param standalone: {'PASS' if param_orig_ok and param_unseen_ok else 'FAIL'}")
    print(f"Baselines all pass: {'PASS' if baselines_pass else 'FAIL'}")
    print(f"Competition equal (literal wins all id2-6): {literal_wins_all}")
    print(f"Competition equal (literal wrong URL all): {literal_wrong_url}")
    print(f"Disambiguation (param higher): {'PASS' if param_higher_ok else 'FAIL'}")
    print(f"Disambiguation (literal higher): {'PASS' if literal_higher_ok else 'FAIL'}")
    print(f"COMPETITION-UNSAFE (literal false accepts): {competition_unsafe}")
    print(f"COMPETITION-SAFE: {competition_safe}")

    # Write full summary to stdout for capture
    print("\n=== Full Results JSON ===")
    print(json.dumps(results, indent=2))

    # Write structured results to file
    summary_path = EXPERIMENT_DIR / "run_summary.json"
    with open(summary_path, "w") as f:
        json.dump({
            "results": results,
            "evaluation": {
                "cold_ok": cold_ok,
                "lit_orig_ok": lit_orig_ok,
                "lit_unseen_ok": lit_unseen_ok,
                "param_orig_ok": param_orig_ok,
                "param_unseen_ok": param_unseen_ok,
                "baselines_pass": baselines_pass,
                "literal_wins_all_competition": literal_wins_all,
                "literal_wrong_url_all_competition": literal_wrong_url,
                "param_higher_ok": param_higher_ok,
                "literal_higher_ok": literal_higher_ok,
                "disambig_pass": disambig_pass,
                "competition_unsafe": competition_unsafe,
                "competition_safe": competition_safe,
            }
        }, f, indent=2)

    print(f"\nRaw evidence written to: {RAW_EVIDENCE_PATH}")
    print(f"Summary written to: {summary_path}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
