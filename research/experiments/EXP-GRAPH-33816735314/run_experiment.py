#!/usr/bin/env python3
"""EXP-GRAPH-33816735314: Test parameter-slot-count tie-break fix.

This script executes all 13 conditions from the frozen experiment design.
Each condition uses a fresh kernel instance with explicitly controlled registry contents.
No HTTP execution required - only resolution and bound_action correctness measured.
"""

import json
import hashlib
import tempfile
from pathlib import Path
from dataclasses import asdict

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from spider.kernel import SpiderKernel
from spider.registry import MechanismRegistry
from spider.models import Mechanism, ResolutionStatus


def sha256_file(path: str) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def create_mechanism(
    mechanism_id: str,
    intent: str = "fetch",
    confidence: float = 0.95,
    parameter_slots: list[str] | None = None,
    template: str | None = None,
    fixed_url: str | None = None,
) -> Mechanism:
    """Create a mechanism with specified parameters."""
    if parameter_slots is None:
        parameter_slots = []
    
    if template:
        action_template = {"url": template}
    elif fixed_url:
        action_template = {"url": fixed_url}
    else:
        action_template = {"url": "/posts/1"}
    
    return Mechanism(
        mechanism_id=mechanism_id,
        intent=intent,
        preconditions={},
        action_template=action_template,
        postconditions={},
        parameter_slots=parameter_slots,
        evidence=["test"],
        confidence=confidence,
    )


def run_condition(
    condition_id: str,
    mechanisms: list[Mechanism],
    params: dict,
    expected_resolution: str,
    expected_url: str | None,
    expected_winning_mechanism: str | None = None,
    role: str = "test",
) -> dict:
    """Run a single experimental condition and return raw evidence."""
    # Create fresh kernel with temporary registry
    with tempfile.TemporaryDirectory() as tmpdir:
        registry_path = Path(tmpdir) / "registry.jsonl"
        registry = MechanismRegistry(registry_path)
        
        # Register mechanisms
        for m in mechanisms:
            registry.upsert(m)
        
        kernel = SpiderKernel(registry)
        
        # Run resolution
        result = kernel.resolve("fetch", {}, params)
        
        # Extract observed values
        observed_resolution = result.status.value
        observed_mechanism_id = result.mechanism_id
        observed_url = result.bound_action.get("url") if result.bound_action else None
        
        # Build raw evidence record
        raw_evidence = {
            "condition_id": condition_id,
            "role": role,
            "registry_mechanisms": [m.as_dict() for m in mechanisms],
            "params": params,
            "expected_resolution": expected_resolution,
            "expected_url": expected_url,
            "expected_winning_mechanism": expected_winning_mechanism,
            "observed_resolution": observed_resolution,
            "observed_mechanism_id": observed_mechanism_id,
            "observed_url": observed_url,
            "raw_resolution": asdict(result),
            "matches_resolution": observed_resolution == expected_resolution,
            "matches_url": observed_url == expected_url,
            "matches_winning_mechanism": (
                observed_mechanism_id == expected_winning_mechanism
                if expected_winning_mechanism
                else None
            ),
        }
        
        return raw_evidence


def main():
    """Execute all 13 conditions."""
    raw_evidence_list = []
    
    # Condition 1: cold - No mechanisms registered
    raw_evidence_list.append(run_condition(
        condition_id="cold",
        mechanisms=[],
        params={"id": 2},
        expected_resolution="UNKNOWN",
        expected_url=None,
        role="baseline",
    ))
    
    # Condition 2: literal-only-original - Literal mechanism only, original resource
    raw_evidence_list.append(run_condition(
        condition_id="literal-only-original",
        mechanisms=[create_mechanism(
            mechanism_id="literal-fetch-posts-1",
            confidence=0.95,
            parameter_slots=[],
            fixed_url="https://jsonplaceholder.typicode.com/posts/1",
        )],
        params={"id": 1},
        expected_resolution="EXECUTABLE",
        expected_url="https://jsonplaceholder.typicode.com/posts/1",
        role="baseline",
    ))
    
    # Condition 3: literal-only-unseen - Literal mechanism only, unseen resource
    raw_evidence_list.append(run_condition(
        condition_id="literal-only-unseen",
        mechanisms=[create_mechanism(
            mechanism_id="literal-fetch-posts-1",
            confidence=0.95,
            parameter_slots=[],
            fixed_url="https://jsonplaceholder.typicode.com/posts/1",
        )],
        params={"id": 2},
        expected_resolution="EXECUTABLE",
        expected_url="https://jsonplaceholder.typicode.com/posts/1",
        role="baseline",
    ))
    
    # Condition 4: param-only-original - Parameterized mechanism only, original resource
    raw_evidence_list.append(run_condition(
        condition_id="param-only-original",
        mechanisms=[create_mechanism(
            mechanism_id="param-fetch-posts",
            confidence=0.95,
            parameter_slots=["id"],
            template="https://jsonplaceholder.typicode.com/posts/${id}",
        )],
        params={"id": 1},
        expected_resolution="EXECUTABLE",
        expected_url="https://jsonplaceholder.typicode.com/posts/1",
        role="baseline",
    ))
    
    # Condition 5: param-only-unseen - Parameterized mechanism only, unseen resource
    raw_evidence_list.append(run_condition(
        condition_id="param-only-unseen",
        mechanisms=[create_mechanism(
            mechanism_id="param-fetch-posts",
            confidence=0.95,
            parameter_slots=["id"],
            template="https://jsonplaceholder.typicode.com/posts/${id}",
        )],
        params={"id": 2},
        expected_resolution="EXECUTABLE",
        expected_url="https://jsonplaceholder.typicode.com/posts/2",
        role="baseline",
    ))
    
    # Condition 6-11: compete-equal-id1 through id6 - Shared registry, equal confidence
    shared_equal_mechanisms = [
        create_mechanism(
            mechanism_id="literal-fetch-posts-1",
            confidence=0.95,
            parameter_slots=[],
            fixed_url="https://jsonplaceholder.typicode.com/posts/1",
        ),
        create_mechanism(
            mechanism_id="param-fetch-posts",
            confidence=0.95,
            parameter_slots=["id"],
            template="https://jsonplaceholder.typicode.com/posts/${id}",
        ),
    ]
    
    for id_val in range(1, 7):
        raw_evidence_list.append(run_condition(
            condition_id=f"compete-equal-id{id_val}",
            mechanisms=shared_equal_mechanisms,
            params={"id": id_val},
            expected_resolution="EXECUTABLE",
            expected_url=f"https://jsonplaceholder.typicode.com/posts/{id_val}",
            expected_winning_mechanism="param-fetch-posts",
            role="intervention",
        ))
    
    # Condition 12: compete-param-higher - Shared registry, param higher confidence
    raw_evidence_list.append(run_condition(
        condition_id="compete-param-higher",
        mechanisms=[
            create_mechanism(
                mechanism_id="literal-fetch-posts-1",
                confidence=0.95,
                parameter_slots=[],
                fixed_url="https://jsonplaceholder.typicode.com/posts/1",
            ),
            create_mechanism(
                mechanism_id="param-fetch-posts",
                confidence=0.98,
                parameter_slots=["id"],
                template="https://jsonplaceholder.typicode.com/posts/${id}",
            ),
        ],
        params={"id": 3},
        expected_resolution="EXECUTABLE",
        expected_url="https://jsonplaceholder.typicode.com/posts/3",
        expected_winning_mechanism="param-fetch-posts",
        role="positive_control",
    ))
    
    # Condition 13: compete-literal-higher - Shared registry, literal higher confidence
    raw_evidence_list.append(run_condition(
        condition_id="compete-literal-higher",
        mechanisms=[
            create_mechanism(
                mechanism_id="literal-fetch-posts-1",
                confidence=0.98,
                parameter_slots=[],
                fixed_url="https://jsonplaceholder.typicode.com/posts/1",
            ),
            create_mechanism(
                mechanism_id="param-fetch-posts",
                confidence=0.95,
                parameter_slots=["id"],
                template="https://jsonplaceholder.typicode.com/posts/${id}",
            ),
        ],
        params={"id": 3},
        expected_resolution="EXECUTABLE",
        expected_url="https://jsonplaceholder.typicode.com/posts/1",
        expected_winning_mechanism="literal-fetch-posts-1",
        role="null_control",
    ))
    
    # Write raw evidence
    output_path = Path(__file__).parent / "raw_evidence.json"
    with open(output_path, "w") as f:
        json.dump(raw_evidence_list, f, indent=2)
    
    print(f"Raw evidence written to {output_path}")
    print(f"Total conditions: {len(raw_evidence_list)}")
    
    # Print summary
    all_pass = True
    for ev in raw_evidence_list:
        status = "PASS" if ev["matches_resolution"] and ev["matches_url"] else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"  {ev['condition_id']}: {status}")
    
    print(f"\nOverall: {'ALL PASS' if all_pass else 'SOME FAIL'}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
