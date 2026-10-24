#!/usr/bin/env python3
"""End-to-end Chromium smoke: observe two routes, compile, reuse held-out URLs.

No LLM/provider access; reports no economic product advantage.
"""
import tempfile
from pathlib import Path

from run_real_agent_pilot import execute_compiled_playwright, run_trial
from train_pilot_memory import train
from spider.pilot_portal import TRAIN_IDS, EVAL_IDS, start_portal, truth


def main():
    server, thread, base = start_portal()
    try:
        for family, ids in TRAIN_IDS.items():
            first = ids[0]
            result = execute_compiled_playwright(base, family, first)
            if result["answer"] != truth(family, first):
                raise AssertionError(f"Chromium wrong: {family}:{first}")
            if "/view?id=" not in result["final_url"] or "id=\"answer\"" not in result["page_html"]:
                raise AssertionError("browser trace absent")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    with tempfile.TemporaryDirectory() as tmp:
        memory_path = Path(tmp) / "memory.jsonl"
        for family in TRAIN_IDS:
            manifest = train(memory_path, family)  # real Chromium, two training IDs
            if manifest["browser_training_runs"] != 2:
                raise AssertionError("insufficient browser evidence")
            for identifier in EVAL_IDS[family]:
                report = run_trial("SPIDER", family, identifier, "google",
                                   None, False, memory_path=memory_path)
                if report["path"] != "inheritance" or not report["success"]:
                    raise AssertionError(f"held-out inherited route failed: {report}")
                if report["http_requests_from_spider"] != 1:
                    raise AssertionError("replay must use a single read-only HTTP request")
                if report["cost_accounting_complete"]:
                    raise AssertionError("unsupported economic claim")
    print("SPIDER_CHROMIUM_LEARN_AND_INHERIT_HELDOUT_OK")


if __name__ == "__main__":
    main()
