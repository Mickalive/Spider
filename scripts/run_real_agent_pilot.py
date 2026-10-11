#!/usr/bin/env python3
"""Opt-in live Chromium/LLM agent pilot, NEVER a claim that SPIDER wins.

Requirements: pip install browser-use; uvx browser-use install.
A provider key and --allow-model-charges are required for any agent fallback.
Each run writes raw telemetry, NOT fabricated fully-loaded benchmark costs.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

from spider import Mechanism, SpiderKernel
from spider.agent_bridge import AgentBridge
from spider.pilot_portal import DATA, start_portal, truth
from spider.registry import MechanismRegistry


def task_prompt(base: str, family: str, identifier: str, arm: str) -> str:
    kind = "invoice total" if family == "invoices" else "shipment status"
    prefix = (
        f"Open {base}/ and use the portal UI to find the {kind} for reference {identifier}. "
        "Return the exact answer as plain text. Never use an imagined value."
    )
    if arm == "INSTRUCTIONS":
        prefix += " Use the appropriate portal section, search the reference, open the result, and read the detail."
    if arm == "RETRIEVAL":
        prefix += f" A previous worker reported that the {family} section has a search form at {base}/portal/{family} (unverified hint)."
    return prefix


def normalize(value: str) -> str:
    return " ".join(str(value).strip().casefold().split())


def checked_answer(raw: object, expected: str) -> bool:
    answer = normalize(str(raw))
    expected = normalize(expected)
    # The fixture has short answers; do not accept a number embedded in another.
    return bool(re.search(r"(?<![\w.])" + re.escape(expected) + r"(?![\w.])", answer))


async def execute_browser_use(prompt: str, provider: str, model: str | None) -> dict:
    try:
        from browser_use import Agent, ChatBrowserUse, ChatGoogle
    except ImportError as exc:
        raise RuntimeError("Install optional browser-use and Chromium before running real-agent pilot") from exc

    if provider == "google":
        if not os.environ.get("GOOGLE_API_KEY"):
            raise RuntimeError("GOOGLE_API_KEY missing; no model request attempted")
        llm = ChatGoogle(model=model or "gemini-3-flash-preview")
    elif provider == "browser-use":
        if not os.environ.get("BROWSER_USE_API_KEY"):
            raise RuntimeError("BROWSER_USE_API_KEY missing; no model request attempted")
        llm = ChatBrowserUse(model=model or "bu-2-0")
    else:
        raise ValueError(f"unsupported provider {provider}")

    history = await Agent(task=prompt, llm=llm).run(max_steps=22)
    usage = getattr(history, "usage", None)
    tokens = getattr(usage, "total_tokens", None) if usage is not None else None
    cost = getattr(usage, "total_cost", None) if usage is not None else None
    return {
        "answer": history.final_result(),
        "tokens": tokens,
        "model_cost_usd": cost,
        "steps": len(history.action_names()),
        "agent_errors": history.errors(),
        "model_usage_present": usage is not None,
    }


def seed_fixture_mechanism(registry: MechanismRegistry, family: str, base: str) -> None:
    """EXPERIMENT-ONLY oracle/template seed, not automatic SPIDER learning."""
    registry.upsert(Mechanism(
        mechanism_id=f"MANUAL-fixture-{family}",
        intent=f"read-{family}",
        preconditions={"origin": base, "family": family},
        action_template={"method": "GET", "url": base + f"/api/{family}/\u0024{{id}}"},
        postconditions={"ok": True},
        parameter_slots=["id"],
        verification_rule={"replay_safe": True},
        evidence=["MANUAL_FIXTURE_SCHEMA_NOT_AGENT_DISCOVERY"],
        confidence=0.95,
    ))


def run_trial(arm: str, family: str, identifier: str, provider: str,
              model: str | None, seeded_fixture: bool) -> dict:
    expected = truth(family, identifier)
    if expected is None:
        raise ValueError("unknown local fixture reference")
    server, thread, base = start_portal()
    registry = MechanismRegistry(Path(__file__).resolve().parent / ".spider-pilot-temporary-registry.jsonl")
    # Never leave fixture-derived state in the source tree or another user's run.
    import tempfile
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            registry = MechanismRegistry(Path(tempdir) / "pilot.jsonl")
            if arm == "SPIDER" and seeded_fixture:
                seed_fixture_mechanism(registry, family, base)

            start = time.monotonic()
            request_count = 0
            response_holder = {}
            def read_only_get(action: dict):
                nonlocal request_count
                request_count += 1
                with urllib.request.urlopen(action["url"], timeout=10) as response:
                    data = json.loads(response.read())
                response_holder["value"] = data
                return data

            def observed():
                data = response_holder.get("value", {})
                return {"ok": data.get("ok") is True and
                        data.get("id") == identifier and data.get("family") == family}

            def authorize(action: dict) -> bool:
                # Read-only and exact same-origin fixture endpoint, no traversal.
                return action.get("method") == "GET" and action.get("url") == base + f"/api/{family}/{identifier}"

            def fallback():
                return asyncio.run(execute_browser_use(task_prompt(base, family, identifier, arm), provider, model))

            if arm == "SPIDER":
                bridge = AgentBridge(SpiderKernel(registry))
                outcome = bridge.run(f"read-{family}", {"origin": base, "family": family},
                                     {"id": identifier}, fallback=fallback,
                                     execute=read_only_get, read_state=observed, authorize=authorize)
                path = outcome.path
                value = outcome.value
                reason = outcome.reason
            elif arm in ("COLD", "INSTRUCTIONS", "RETRIEVAL"):
                path = "agent"
                value = fallback()
                reason = "ordinary Browser Use agent"
            else:
                raise ValueError("unsupported arm")

            elapsed = time.monotonic() - start
            answer = value.get("answer") if path == "agent" else (value.get("answer") if isinstance(value, dict) else None)
            usage = value if path == "agent" and isinstance(value, dict) else {}
            return {
                "task_id": f"{family}:{identifier}", "replicate": 0,
                "family": family, "phase": "seeded-repeat" if seeded_fixture else "cold",
                "arm": arm, "success": checked_answer(answer, expected),
                "safe": path != "unknown",
                "path": path, "reason": reason, "answer": answer,
                "latency_ms": int(elapsed * 1000),
                "tokens": usage.get("tokens"),
                "model_cost_usd": usage.get("model_cost_usd"),
                "http_requests_from_spider": request_count,
                "manual_fixture_seed": seeded_fixture,
                "cost_accounting_complete": False,
                "cost_usd": None,
                "note": "Raw pilot only: seeded template is manual; model/browser/storage/seed costs and strongest cache competitor not fully measured.",
            }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=["COLD", "INSTRUCTIONS", "RETRIEVAL", "SPIDER"], required=True)
    ap.add_argument("--family", choices=sorted(DATA), required=True)
    ap.add_argument("--id", required=True, dest="identifier")
    ap.add_argument("--provider", choices=["google", "browser-use"], default="google")
    ap.add_argument("--model")
    ap.add_argument("--seeded-fixture", action="store_true", help="Manually seed known fixture API; not learned inheritance")
    ap.add_argument("--allow-model-charges", action="store_true", help="Explicit opt-in to provider billing, including possible fallback")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if not args.allow_model_charges:
        ap.error("Provider cost permission required; pilot performs no model requests by default")
    result = run_trial(args.arm, args.family, args.identifier, args.provider,
                       args.model, args.seeded_fixture)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(result, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
