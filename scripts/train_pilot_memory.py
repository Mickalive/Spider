#!/usr/bin/env python3
"""Learn a fixture-scoped parameterized GET from two actual Chromium traces.

The first agent here is a deterministic compiled Playwright workflow, NOT an
autonomous LLM browser agent. Costs and provenance of training are recorded;
they are not hidden from a competitive benchmark.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from spider.pilot_learning import compile_browser_traces
from spider.pilot_portal import TRAIN_IDS, start_portal
from spider.registry import MechanismRegistry
from run_real_agent_pilot import execute_compiled_playwright


def train(memory_path: Path, family: str) -> dict:
    if family not in TRAIN_IDS:
        raise ValueError("unknown family")
    server, thread, base = start_portal()
    try:
        start = time.monotonic()
        examples = []
        for identifier in TRAIN_IDS[family]:
            result = execute_compiled_playwright(base, family, identifier)
            examples.append({
                "identifier": identifier,
                "answer": result["answer"],
                "final_url": result["final_url"],
                "page_html": result["page_html"],
            })
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
            "learning_source": "OBSERVED_COMPILED_PLAYWRIGHT_BROWSER_TRACES",
            "llm_model_calls": 0,
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
    args = parser.parse_args()
    results = [train(args.memory_path, family) for family in TRAIN_IDS]
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print("SPIDER_BROWSER_TRACE_TRAINING_OK " + json.dumps(results))


if __name__ == "__main__":
    main()
