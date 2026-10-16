"""Minimal end-to-end PRODUCT demonstration, zero LLM or browser-cloud charges.

Observe two independently checked public GitHub release pages, learn a route,
store it in Spider's existing registry, resolve it for unseen repositories and
VERIFY results against an independent official GitHub API.

This is a narrow deterministic read-only mechanism demo, NOT proof of savings
over direct API, generic LLM skill transfer, or browsing-agent integration.
"""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from time import perf_counter
from urllib.parse import urlsplit

from spider.kernel import SpiderKernel
from spider.models import ResolutionStatus
from spider.public_learning import learn_public_route
from spider.public_tasks import HOLDOUT, TRAIN, PublicTask, http_get, parse_page
from spider.registry import MechanismRegistry


def run_github_demo(fetch=http_get, *, memory_path=None):
    began = perf_counter()
    recorded = []
    calls = {"public_pages": 0, "official_api": 0}
    def fetch_public(task):
        calls["public_pages"] += 1
        raw, url = fetch(task.target_url)
        value = parse_page(task, raw, url)
        if value is None:
            raise RuntimeError(f"unreadable public GitHub release page for {task.identifier}")
        return value, url

    def fetch_oracle(task):
        calls["official_api"] += 1
        raw, final = fetch(task.oracle_url)
        if urlsplit(final).hostname != "api.github.com":
            raise RuntimeError("official API redirected to unexpected host")
        value = json.loads(raw)["tag_name"]
        if not isinstance(value, str) or len(value) > 100 or not value:
            raise RuntimeError("invalid official API response")
        return value

    for name in TRAIN["github"]:
        task = PublicTask("github", name)
        answer, url = fetch_public(task)
        oracle = fetch_oracle(task)
        if answer != oracle:
            raise RuntimeError(f"training observation does not match independent truth for {name}")
        recorded.append({
            "identifier": name, "answer": answer,
            "visited_urls": [task.target_url, url],
            "verified_against_independent_oracle": True,
        })

    mechanism = learn_public_route("github", recorded)
    def exercise(registry):
        registry.upsert(mechanism)
        kernel = SpiderKernel(registry)
        outcomes = []
        for name in HOLDOUT["github"]:
            task = PublicTask("github", name)
            resolution = kernel.resolve(
                "latest-github",
                {"family": "github", "surface": "allowlisted-public-v1", "read_only": True},
                {"id": name},
            )
            if (resolution.status != ResolutionStatus.EXECUTABLE
                    or resolution.bound_action != {"method": "GET", "url": task.target_url}):
                raise RuntimeError(f"Spider did not resolve a safe inherited route for {name}")
            observed, _ = fetch_public(task)
            verified = observed == fetch_oracle(task)
            if not verified or not kernel.verify(mechanism.mechanism_id, {"verified": verified}):
                registry.invalidate(mechanism.mechanism_id)
                raise RuntimeError(f"inherited release tag failed independent verification for {name}")
            outcomes.append({"identifier": name, "verified": True, "inherited": True})
        # A learned route may not run outside an explicit allowlisted read-only context.
        denied = kernel.resolve("latest-github", {"family": "github"}, {"id": HOLDOUT["github"][0]})
        if denied.status == ResolutionStatus.EXECUTABLE:
            raise RuntimeError("unsafe inherited route escaped scope guards")
        return outcomes

    if memory_path is not None:
        outcomes = exercise(MechanismRegistry(memory_path))
    else:
        with tempfile.TemporaryDirectory(prefix="spider-product-demo-") as tmp:
            outcomes = exercise(MechanismRegistry(Path(tmp) / "mechanisms.jsonl"))

    return {
        "schema_version": 1, "mode": "live_readonly_no_llm",
        "scope": "two curated GitHub Releases training identifiers, two unseen holdouts",
        "training_examples": len(recorded),
        "holdout": outcomes,
        "success": len(outcomes) == len(HOLDOUT["github"]),
        "calls": calls, "elapsed_seconds": round(perf_counter() - began, 3),
        "claims": {
            "route_reuse_demonstrated": True,
            "generic_web_agent_learning_demonstrated": False,
            "llm_cost_savings_demonstrated": False,
            "beats_direct_api": False,
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--memory", type=Path, default=None)
    args = parser.parse_args()
    report = run_github_demo(memory_path=args.memory)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    if not report["success"]:
        raise SystemExit(1)
