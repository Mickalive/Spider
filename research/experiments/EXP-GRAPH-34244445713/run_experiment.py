#!/usr/bin/env python3
"""
EXP-GRAPH-34244445713 — Execute frozen experiment.

Tests whether the parameter-slot-count tie-break fix is present in committed HEAD
and whether it resolves the literal-vs-param equal-confidence hazard for unseen ids 2-7.
"""

import json
import hashlib
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Add src to path (spider package is under src/)
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from spider.kernel import SpiderKernel
from spider.models import Mechanism, Observation
from spider.registry import MechanismRegistry


EXPERIMENT_ID = "EXP-GRAPH-34244445713"
KERNEL_PATH = Path(__file__).resolve().parents[3] / "src" / "spider" / "kernel.py"
ENDPOINT = "https://jsonplaceholder.typicode.com"


def verify_fix() -> dict:
    """Read kernel.py L112 and check if fix is present."""
    lines = KERNEL_PATH.read_text().splitlines()
    line_112 = lines[111]  # 0-indexed
    fix_present = "len(m.parameter_slots)" in line_112 or "len(parameter_slots)" in line_112
    kernel_sha256 = hashlib.sha256(KERNEL_PATH.read_bytes()).hexdigest()
    return {
        "line_112_content": line_112.strip(),
        "fix_present": fix_present,
        "kernel_sha256": kernel_sha256,
    }


def make_literal_mechanism(confidence: float = 0.95) -> Mechanism:
    """Create a literal mechanism for /posts/1."""
    return Mechanism(
        mechanism_id="literal-posts-1",
        intent="fetch-post",
        preconditions={},
        action_template={"method": "GET", "url": "/posts/1"},
        postconditions={"id": 1},
        parameter_slots=[],
        evidence=["test-literal"],
        confidence=confidence,
    )


def make_param_mechanism(confidence: float = 0.95) -> Mechanism:
    """Create a parametrized mechanism for /posts/{id}."""
    return Mechanism(
        mechanism_id="param-posts-id",
        intent="fetch-post",
        preconditions={},
        action_template={"method": "GET", "url": "/posts/${id}"},
        postconditions={"id": "${id}"},
        parameter_slots=["id"],
        evidence=["test-param"],
        confidence=confidence,
    )


def http_execute(url: str, timeout: int = 5) -> dict:
    """Execute HTTP GET and return status code and parsed JSON."""
    import urllib.request
    import urllib.error
    full_url = f"{ENDPOINT}{url}"
    try:
        req = urllib.request.Request(full_url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status_code = resp.getcode()
            body = json.loads(resp.read().decode())
            return {"status_code": status_code, "body": body, "error": None}
    except urllib.error.HTTPError as e:
        return {"status_code": e.code, "body": None, "error": str(e)}
    except Exception as e:
        return {"status_code": None, "body": None, "error": str(e)}


def run_condition(registry_path: str, context_id: int, params: dict, label: str) -> dict:
    """Run a single resolution condition and record raw evidence."""
    reg = MechanismRegistry(registry_path)
    kernel = SpiderKernel(reg, min_confidence=0.8)
    
    t0 = time.time()
    resolution = kernel.resolve("fetch-post", {"id": context_id}, params)
    t1 = time.time()
    
    result = {
        "label": label,
        "status": resolution.status.value,
        "mechanism_id": resolution.mechanism_id,
        "bound_action": resolution.bound_action,
        "confidence": resolution.confidence,
        "reason": resolution.reason,
        "resolution_time_ms": round((t1 - t0) * 1000, 2),
    }
    
    # If EXECUTABLE, execute HTTP
    if resolution.status.value == "EXECUTABLE" and resolution.bound_action:
        url = resolution.bound_action.get("url", "")
        http = http_execute(url)
        result["http_status_code"] = http["status_code"]
        result["http_body"] = http["body"]
        result["http_error"] = http["error"]
    else:
        result["http_status_code"] = None
        result["http_body"] = None
        result["http_error"] = None
    
    return result


def main():
    evidence_dir = Path(__file__).parent
    raw_evidence = []
    
    # Step 1: Fix verification
    fix_info = verify_fix()
    print(f"Fix verification: {fix_info}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        reg_path = str(Path(tmpdir) / "registry.jsonl")
        
        # === BASELINE CONDITIONS (6) ===
        
        # B-COLD: Empty registry
        raw_evidence.append(run_condition(reg_path, 7, {"id": "7"}, "B-COLD"))
        
        # B-LITERAL-ONLY-ORIG: Literal /posts/1, context id=1
        reg = MechanismRegistry(reg_path)
        reg.replace([make_literal_mechanism()])
        raw_evidence.append(run_condition(reg_path, 1, {"id": "1"}, "B-LITERAL-ONLY-ORIG"))
        
        # B-LITERAL-ONLY-UNSEEN: Literal /posts/1, context id=7
        raw_evidence.append(run_condition(reg_path, 7, {"id": "7"}, "B-LITERAL-ONLY-UNSEEN"))
        
        # B-PARAM-ONLY-ORIG: Param /posts/{id}, context id=1
        reg.replace([make_param_mechanism()])
        raw_evidence.append(run_condition(reg_path, 1, {"id": "1"}, "B-PARAM-ONLY-ORIG"))
        
        # B-PARAM-ONLY-UNSEEN: Param /posts/{id}, context id=7
        raw_evidence.append(run_condition(reg_path, 7, {"id": "7"}, "B-PARAM-ONLY-UNSEEN"))
        
        # B-COMPETE-PARAM-HIGHER: Param (0.98) vs literal (0.95), context id=7
        reg.replace([make_literal_mechanism(0.95), make_param_mechanism(0.98)])
        raw_evidence.append(run_condition(reg_path, 7, {"id": "7"}, "B-COMPETE-PARAM-HIGHER"))
        
        # === CORE HAZARD CONDITIONS (6): equal confidence 0.95, literal registered first ===
        
        for ctx_id in range(2, 8):
            # Reset registry: literal first, then param (worst-case insertion order)
            reg.replace([make_literal_mechanism(0.95), make_param_mechanism(0.95)])
            raw_evidence.append(run_condition(reg_path, ctx_id, {"id": str(ctx_id)}, f"C-EQUAL-ID{ctx_id}"))
        
        # === NULL CONTROL (1) ===
        
        # B-CONFIDENCE-LITERAL-HIGHER: literal (0.98) vs param (0.95), context id=7
        reg.replace([make_literal_mechanism(0.98), make_param_mechanism(0.95)])
        raw_evidence.append(run_condition(reg_path, 7, {"id": "7"}, "B-CONFIDENCE-LITERAL-HIGHER"))
    
    # Write raw evidence
    raw_path = evidence_dir / "raw_evidence.json"
    raw_path.write_text(json.dumps({
        "experiment_id": EXPERIMENT_ID,
        "fix_verification": fix_info,
        "conditions": raw_evidence,
    }, indent=2))
    
    print(f"\nRaw evidence written to {raw_path}")
    print(f"Total conditions: {len(raw_evidence)}")
    
    # Print summary
    for obs in raw_evidence:
        print(f"  {obs['label']}: status={obs['status']}, mechanism={obs['mechanism_id']}, "
              f"url={obs['bound_action'].get('url') if obs['bound_action'] else 'N/A'}, "
              f"http={obs['http_status_code']}")


if __name__ == "__main__":
    main()
