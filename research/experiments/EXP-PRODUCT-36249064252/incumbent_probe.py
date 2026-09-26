"""Incumbent reference curve for EXP-PRODUCT-36249064252 (frozen prereg section 6).

Runs in its own interpreter so that it imports the *pristine committed* kernel
extracted from git, never the modified working tree. Records exactly what the
shipped kernel does with a distilled mechanism on a never-observed resource.

Usage: python3 incumbent_probe.py <output.json>
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

COMMIT = "43fdfa9c39f3f97989c4f446c33183ff779eb9b3"
PACKET = Path(__file__).resolve().parent
FILES = ("__init__.py", "kernel.py", "models.py", "registry.py")


def extract(target: Path) -> dict[str, str]:
    digests = {}
    package = target / "spider"
    package.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        blob = subprocess.run(
            ["git", "show", f"{COMMIT}:src/spider/{name}"],
            cwd=PACKET.parents[2],
            capture_output=True,
            check=True,
        ).stdout
        (package / name).write_bytes(blob)
        digests[f"src/spider/{name}"] = hashlib.sha256(blob).hexdigest()
    return digests


def main() -> None:
    out = Path(sys.argv[1])
    workdir = Path(tempfile.mkdtemp())
    digests = extract(workdir)

    sys.path.insert(0, str(workdir))
    sys.path.insert(0, str(PACKET))
    import spider  # noqa: E402  (import must follow sys.path setup)

    assert Path(spider.__file__).resolve().parent == (workdir / "spider"), spider.__file__

    from spider.registry import MechanismRegistry  # noqa: E402

    from arms import Client, OWNER_TOKEN  # noqa: E402
    from substrate import (  # noqa: E402
        RESOURCE_B_COLLECTION,
        RESOURCE_B_IDS,
        Substrate,
        label_for,
    )

    registry = MechanismRegistry(workdir / "mechanisms.jsonl")
    kernel = spider.SpiderKernel(registry)

    has_distill_parameterized = hasattr(kernel, "distill_parameterized")
    module = __import__("spider.kernel", fromlist=["x"])
    has_module_level = hasattr(module, "distill_parameterized")

    # One literal mechanism exactly as the shipped distill() builds it.
    sample = spider.Observation(
        intent="read",
        state={"auth": "valid_token", "role": "owner", "collection": "items"},
        action={"method": "GET", "path": "/items/item-1"},
        next_state={"status": 200, "ok": True, "resource_present": True},
        success=True,
        provenance={"identifier": "item-1"},
    )
    literal = kernel.distill(sample)
    registry.upsert(literal)

    same = kernel.resolve("read", {"auth": "valid_token", "role": "owner", "collection": "items"})
    paraphrased = kernel.resolve("read-product", {"auth": "valid_token", "role": "owner", "collection": "products"})

    # Full incumbent run over a sample of never-observed resource-B identifiers.
    substrate = Substrate()
    substrate.reset()
    seeded = RESOURCE_B_IDS[18:]
    substrate.seed_many(RESOURCE_B_COLLECTION, seeded)
    client = Client(substrate.base_url)

    per_task = []
    for identifier in seeded[:20]:
        context = {"auth": "valid_token", "role": "owner", "collection": RESOURCE_B_COLLECTION}
        params = {"collection": RESOURCE_B_COLLECTION, "id": identifier, "auth_token": OWNER_TOKEN}
        before = len(client.total.statuses)
        resolution = kernel.resolve("read", context, params)
        issued = len(client.total.statuses) - before
        per_task.append(
            {
                "identifier": identifier,
                "status": resolution.status.value,
                "reason": resolution.reason,
                "mechanism_id": resolution.mechanism_id,
                "confidence": resolution.confidence,
                "http_requests_issued": issued,
                "bound_action": resolution.bound_action,
            }
        )
    substrate.stop()

    executable = sum(1 for row in per_task if row["status"] == "EXECUTABLE")
    payload = {
        "probe": "incumbent-reference-curve",
        "prereg_section": 6,
        "commit": COMMIT,
        "extracted_file_sha256": digests,
        "incumbent_kernel_sha256": digests["src/spider/kernel.py"],
        "has_kernel_distill_parameterized": has_distill_parameterized,
        "has_module_level_distill_parameterized": has_module_level,
        "distill_confidence": literal.confidence,
        "min_confidence": kernel.min_confidence,
        "same_intent_resolution": {
            "status": same.status.value,
            "reason": same.reason,
            "confidence": same.confidence,
        },
        "paraphrased_intent_resolution": {
            "status": paraphrased.status.value,
            "reason": paraphrased.reason,
        },
        "mechanism_unpopulated_fields": {
            key: getattr(literal, key)
            for key in ("freshness", "repair_scope", "applicability_guards", "verification_rule", "failure_boundary")
        },
        "resource_b_probe": {
            "n_tasks": len(per_task),
            "n_executable": executable,
            "executable_fraction": executable / len(per_task) if per_task else None,
            "total_http_requests": sum(row["http_requests_issued"] for row in per_task),
            "per_task": per_task,
        },
        "expected_by_prereg": "0% EXECUTABLE for any distilled mechanism on any resource",
    }
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in payload.items() if k != "resource_b_probe"}, indent=2, sort_keys=True))
    print("executable_fraction:", payload["resource_b_probe"]["executable_fraction"])


if __name__ == "__main__":
    main()
