#!/usr/bin/env python3
"""Public-site benchmark: two real sites, no model or cloud cost by default.

Six arms: COLD/INSTRUCTIONS/RETRIEVAL/SPIDER/COMPILED/DIRECT_API.
Optional seventh: STAGEHAND_V4_SERVER_CACHE (real Browserbase remote cache).
Public read-only task results and independent oracle are checked online.
Every raw row is unpriced (full costs unknown): never feed directly to scorer.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path

from spider.agent_bridge import AgentBridge
from spider.kernel import SpiderKernel
from spider.public_tasks import PublicTask, TRAIN, HOLDOUT, allowlisted_tasks, compiled_result, direct_result, http_get, oracle, parse_page
from spider.public_learning import learn_public_route
from spider.registry import MechanismRegistry
from run_real_agent_pilot import execute_browser_use

ARMS = ("COLD", "INSTRUCTIONS", "RETRIEVAL", "SPIDER", "COMPILED", "DIRECT_API")
STAGEHAND_ARM = "STAGEHAND_V4_SERVER_CACHE"


def plan(seed: int = 20261011, replicates: int = 1, include_stagehand: bool = False) -> list[dict]:
    if replicates < 1:
        raise ValueError("replicates must be positive")
    rng = random.Random(seed)
    rows = []
    for i in range(replicates):
        for task in allowlisted_tasks("holdout"):
            arms = list(ARMS + ((STAGEHAND_ARM,) if include_stagehand else ()))
            rng.shuffle(arms)
            rows.extend({
                "task_id": f"{task.family}:{task.identifier}", "replicate": i,
                "family": task.family, "identifier": task.identifier, "arm": arm,
                "phase": "public-heldout-v1",
            } for arm in arms)
    return rows


def prompt(task: PublicTask, arm: str) -> str:
    out = task.prompt
    if arm == "INSTRUCTIONS":
        out += f" Navigate to the public page for {task.identifier}, read the version or tag and verify its identity."
    if arm == "RETRIEVAL":
        out += " A previous browser found a public detail page on this host (hint unverified)."
    return out


async def stagehand_cached(task: PublicTask) -> dict:
    """Stagehand v4 SERVER-SIDE cache. Local Stagehand is not cache-equivalent."""
    import os
    if not os.environ.get("BROWSERBASE_API_KEY"):
        raise RuntimeError("BROWSERBASE_API_KEY required for real remote cache")
    try:
        from stagehand import Stagehand, browserbase
        from pydantic import BaseModel
    except ImportError as e:
        raise RuntimeError("pip install stagehand pydantic before Stagehand evaluation") from e

    class Extracted(BaseModel):
        answer: str

    browser = await browserbase.launch(api_key=os.environ["BROWSERBASE_API_KEY"])
    try:
        sh = await Stagehand.create(browser=browser, cache={"threshold": 1})
        try:
            page = await browser.context.active_page()
            await page.goto(task.target_url)
            result = await sh.extract(
                "Extract exactly the latest public version/tag shown here for the requested package or repository. Return the answer field.",
                Extracted,
            )
            data = result.data
            value = data.answer if hasattr(data, "answer") else data["answer"]
            metadata = getattr(result, "metadata", None)
            return {"answer": value, "metadata": metadata.model_dump(mode="json") if hasattr(metadata, "model_dump") else str(metadata),
                    "model_cost_usd": None, "tokens": None,
                    "cache_mode": "REAL_BROWSERBASE_SERVER_CACHE"}
        finally:
            await sh.close()
    finally:
        await browser.close()


def learn(family: str, memory: Path, provider: str, model: str | None) -> dict:
    examples = []
    token_total = 0
    known_cost = 0.0
    full_usage = True
    started = time.monotonic()
    for identifier in TRAIN[family]:
        task = PublicTask(family, identifier)
        report = asyncio.run(execute_browser_use(task.prompt, provider, model))
        if report.get("tokens") is None or report.get("model_cost_usd") is None:
            full_usage = False
        else:
            token_total += report["tokens"]
            known_cost += report["model_cost_usd"]
        expected = oracle(task)
        if report.get("answer") != expected:
            raise ValueError(f"agent failed independent oracle for {family}/{identifier}")
        history = report.get("visited_urls") or []
        # Never serialize arbitrary visited URLs: they might contain credentials.
        examples.append({
            "identifier": identifier, "answer": expected,
            "visited_urls": history,
            "verified_against_independent_oracle": True,
        })
    mechanism = learn_public_route(family, examples)
    MechanismRegistry(memory).upsert(mechanism)
    return {
        "family": family, "training_identifiers": list(TRAIN[family]),
        "source": "OBSERVED_BROWSER_USE_AGENT_PUBLIC_NAVIGATION",
        "training_runs": len(examples), "elapsed_ms": int(1000 * (time.monotonic() - started)),
        "tokens": token_total if full_usage else None,
        "reported_model_cost_usd": known_cost if full_usage else None,
        "cost_accounting_complete": False,
        "reused_training_data_on_holdouts": False,
        "observed_pattern_sha256": mechanism.evidence,
    }


def trial(task: PublicTask, arm: str, replicate: int, memory: Path | None,
          provider: str, model: str | None) -> dict:
    if arm not in ARMS + (STAGEHAND_ARM,):
        raise ValueError("unsupported arm")
    if arm == "SPIDER" and memory is None:
        raise ValueError("Spider needs independently trained persistent memory")
    start = time.monotonic()
    http_counter = 0
    observed = {}
    def execute(action):
        nonlocal http_counter
        if not authorized(action):
            raise ValueError("action outside strict page-only allowlist")
        http_counter += 1
        raw, url = http_get(action["url"])
        answer = parse_page(task, raw, url)
        observed["verified"] = answer is not None and answer == oracle(task)
        return {"answer": answer}

    def authorized(action):
        return action.get("method") == "GET" and action.get("url") == task.target_url

    def agent(variant=arm):
        return asyncio.run(execute_browser_use(prompt(task, variant), provider, model))

    if arm == "DIRECT_API":
        value = {"answer": direct_result(task), "model_cost_usd": 0.0, "tokens": 0}
        execution_path = "direct-api"
    elif arm == "COMPILED":
        value = {"answer": compiled_result(task), "model_cost_usd": 0.0, "tokens": 0}
        execution_path = "compiled-public-route"
    elif arm == STAGEHAND_ARM:
        value = asyncio.run(stagehand_cached(task))
        execution_path = "browserbase-stagehand-real-cache"
    elif arm == "SPIDER":
        outcome = AgentBridge(SpiderKernel(MechanismRegistry(memory))).run(
            f"latest-{task.family}",
            {"family": task.family, "surface": "allowlisted-public-v1", "read_only": True},
            {"id": task.identifier}, fallback=agent, execute=execute,
            read_state=lambda: dict(observed), authorize=authorized,
        )
        execution_path = outcome.path
        value = outcome.value if isinstance(outcome.value, dict) else {"answer": None}
    else:
        value = agent()
        execution_path = "browser-use-agent"

    check = oracle(task)
    result = value.get("answer")
    return {
        "task_id": f"{task.family}:{task.identifier}", "replicate": replicate,
        "family": task.family, "phase": "public-heldout-v1", "arm": arm,
        "path": execution_path, "safe": execution_path != "unknown",
        "success": result == check, "answer": result,
        "oracle": {"valid": True, "expected": check},
        "latency_ms": round((time.monotonic() - start) * 1000),
        "tokens": value.get("tokens"),
        "model_cost_usd": value.get("model_cost_usd"),
        "http_requests_from_spider": http_counter,
        "cache_evidence": value.get("metadata"),
        "cost_accounting_complete": False,
        "cost_usd": None,
        "manual_fixture_seed": False,
        "warning": "Unpriced engineering trace. Reported model usage excludes browser service, training, retrieval, failures, storage and verification.",
    }


def confirmed_family_ready(path: Path, family: str) -> bool:
    """Never spend model/browser money against an unsupported public substrate."""
    data = json.loads(path.read_text(encoding="utf-8"))
    try:
        checked = datetime.fromisoformat(data["checked_at"]).astimezone(timezone.utc)
    except (KeyError, TypeError, ValueError):
        return False
    age = (datetime.now(timezone.utc) - checked).total_seconds()
    return 0 <= age <= 86400 and data.get("family_ready", {}).get(family) is True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["plan", "probe", "learn", "trial"], default="plan")
    ap.add_argument("--family", choices=tuple(TRAIN))
    ap.add_argument("--id", dest="identifier")
    ap.add_argument("--arm", choices=ARMS + (STAGEHAND_ARM,))
    ap.add_argument("--memory-path", type=Path)
    ap.add_argument("--readiness-file", type=Path, help="required live per-family readiness probe for all paid workflows")
    ap.add_argument("--provider", choices=["google", "browser-use"], default="google")
    ap.add_argument("--model")
    ap.add_argument("--replicate", type=int, default=0)
    ap.add_argument("--seed", type=int, default=20261011)
    ap.add_argument("--replicates", type=int, default=1)
    ap.add_argument("--include-stagehand", action="store_true")
    ap.add_argument("--allow-model-charges", action="store_true")
    ap.add_argument("--allow-browserbase-charges", action="store_true")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.mode == "plan":
        rows = plan(args.seed, args.replicates, args.include_stagehand)
        payload = {"status": "PLAN_ONLY_NO_COST", "trials": rows,
                   "count": len(rows), "strongest_baseline": "DIRECT_API"}
    elif args.mode == "probe":
        payload = {"status": "EXTERNAL_READ_ONLY_NO_MODEL", "results": [],
                   "checked_at": datetime.now(timezone.utc).isoformat()}
        for task in allowlisted_tasks("holdout"):
            try:
                value = compiled_result(task)
                verdict = oracle(task)
                payload["results"].append({"id": f"{task.family}:{task.identifier}",
                                           "match": value == verdict, "page_value": value,
                                           "independent_oracle": verdict})
            except Exception as exc:
                payload["results"].append({"id": f"{task.family}:{task.identifier}",
                                           "match": False, "error": type(exc).__name__ + ": " + str(exc)})
        payload["family_ready"] = {
            family: all(item["match"] for item in payload["results"] if item["id"].startswith(family + ":"))
            for family in TRAIN
        }
        payload["all_match"] = all(payload["family_ready"].values())
    elif args.mode == "learn":
        if not args.memory_path or not args.family:
            ap.error("learn requires --family and --memory-path")
        if not args.allow_model_charges:
            ap.error("live Browser Use learning requires --allow-model-charges")
        if not args.readiness_file or not confirmed_family_ready(args.readiness_file, args.family):
            ap.error("paid learning requires fresh PASS readiness for this family; run --mode probe first")
        payload = learn(args.family, args.memory_path, args.provider, args.model)
    else:
        if not args.family or not args.identifier or not args.arm:
            ap.error("trial requires --family, --id and --arm")
        task = PublicTask(args.family, args.identifier)
        if task.identifier not in HOLDOUT[task.family]:
            ap.error("trial must use a held-out identifier")
        if args.arm not in ("COMPILED", "DIRECT_API"):
            if not args.readiness_file or not confirmed_family_ready(args.readiness_file, args.family):
                ap.error("paid trial requires fresh PASS readiness for the family; run --mode probe first")
        if args.arm not in ("COMPILED", "DIRECT_API") and not args.allow_model_charges:
            ap.error("a live model or fallback requires --allow-model-charges")
        if args.arm == STAGEHAND_ARM and not args.allow_browserbase_charges:
            ap.error("Stagehand browser cloud requires --allow-browserbase-charges")
        payload = trial(task, args.arm, args.replicate, args.memory_path, args.provider, args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.mode == "trial":
        with args.output.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, sort_keys=True) + "\n")
    else:
        args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
