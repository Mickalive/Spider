#!/usr/bin/env python3
"""Two observed successful browser routes -> scoped parameterized memory.

Default: scripted local Chromium (zero LLM calls). With explicit consent,
Browser Use agents can instead explore the page and furnish their actual
visited URLs. Re-fetch only an exact same-origin, read-only observed detail URL
for independently verifiable evidence before accepting any mechanism.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import time
import urllib.request
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

from spider.pilot_learning import compile_browser_traces, parse_verified_detail
from spider.pilot_portal import TRAIN_IDS, start_portal
from spider.registry import MechanismRegistry
from run_real_agent_pilot import (
    checked_answer, execute_browser_use, execute_compiled_playwright, task_prompt,
)


def observed_agent_example(base: str, family: str, identifier: str,
                           provider: str, model: str | None) -> tuple[dict, dict]:
    result = asyncio.run(execute_browser_use(
        task_prompt(base, family, identifier, "COLD"), provider, model
    ))
    expected_origin = urlsplit(base).netloc
    selected = None
    for url in reversed(result.get("visited_urls") or []):
        if not isinstance(url, str):
            continue
        parsed = urlsplit(url)
        if (parsed.scheme == "http" and parsed.netloc == expected_origin
                and parsed.path == f"/portal/{family}/view"
                and not parsed.fragment and parse_qsl(parsed.query, keep_blank_values=True) == [("id", identifier)]):
            selected = url
            break
    if selected is None:
        raise ValueError("Agent never visited the exact training record detail page")
    # Local test portal only. No arbitrary agent-supplied network URLs are fetched.
    with urllib.request.urlopen(selected, timeout=10) as response:
        html = response.read().decode("utf-8")
    answer = parse_verified_detail(html, identifier)
    if answer is None or not checked_answer(result.get("answer"), answer):
        raise ValueError("Agent final answer not corroborated by the observed record")
    return {
        "identifier": identifier, "answer": answer,
        "final_url": selected, "page_html": html,
    }, result


def train(memory_path: Path, family: str, source: str = "playwright",
          provider: str = "google", model: str | None = None,
          allow_model_charges: bool = False) -> dict:
    if family not in TRAIN_IDS:
        raise ValueError("unknown family")
    if source not in ("playwright", "browser-use"):
        raise ValueError("unsupported training source")
    if source == "browser-use" and not allow_model_charges:
        raise ValueError("browser-use training requires explicit model charge permission")
    server, thread, base = start_portal()
    try:
        start = time.monotonic()
        examples = []
        llm_total = 0
        model_cost_total = 0.0
        cost_measured = True
        steps = 0
        for identifier in TRAIN_IDS[family]:
            if source == "playwright":
                result = execute_compiled_playwright(base, family, identifier)
                example = {
                    "identifier": identifier,
                    "answer": result["answer"],
                    "final_url": result["final_url"],
                    "page_html": result["page_html"],
                }
            else:
                example, result = observed_agent_example(base, family, identifier, provider, model)
            examples.append(example)
            steps += result.get("steps") or 0
            if result.get("tokens") is None or result.get("model_cost_usd") is None:
                cost_measured = False
            else:
                llm_total += result["tokens"]
                model_cost_total += result["model_cost_usd"]

        mechanism = compile_browser_traces(family, examples)
        registry = MechanismRegistry(memory_path)
        registry.upsert(mechanism)
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return {
            "family": family,
            "mechanism_id": mechanism.mechanism_id,
            "training_identifiers": list(TRAIN_IDS[family]),
            "browser_training_runs": len(examples),
            "browser_training_ms": elapsed_ms,
            "browser_training_steps": steps,
            "learning_source": "OBSERVED_COMPILED_PLAYWRIGHT_TRACES" if source == "playwright" else "OBSERVED_BROWSER_USE_AGENT_TRACES",
            "llm_tokens": llm_total if cost_measured else None,
            "llm_model_cost_usd": model_cost_total if cost_measured else None,
            "cost_accounting_complete": False,
            "product_claim": "ENGINEERING_FIXTURE_ONLY",
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-path", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--source", choices=("playwright", "browser-use"), default="playwright")
    parser.add_argument("--provider", choices=("google", "browser-use"), default="google")
    parser.add_argument("--model")
    parser.add_argument("--allow-model-charges", action="store_true")
    args = parser.parse_args()
    if args.source == "browser-use" and not args.allow_model_charges:
        parser.error("explicit --allow-model-charges required for LLM training")
    results = [
        train(args.memory_path, family, source=args.source, provider=args.provider,
              model=args.model, allow_model_charges=args.allow_model_charges)
        for family in TRAIN_IDS
    ]
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print("SPIDER_BROWSER_TRACE_TRAINING_OK " + json.dumps(results))


if __name__ == "__main__":
    main()
