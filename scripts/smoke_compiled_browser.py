#!/usr/bin/env python3
"""Real headless Chromium smoke test, no model calls and no secrets."""
from run_real_agent_pilot import execute_compiled_playwright
from spider.pilot_portal import start_portal, truth


def main():
    server, thread, base = start_portal()
    try:
        for family, reference in (("invoices", "A-101"), ("shipments", "S-902")):
            result = execute_compiled_playwright(base, family, reference)
            if result["answer"] != truth(family, reference):
                raise AssertionError(f"wrong browser result for {family}:{reference}: {result}")
        print("SPIDER_REAL_CHROMIUM_COMPILED_BASELINE_OK")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
