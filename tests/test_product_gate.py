import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from decide_product_gate import decide


CATS = ("model", "browser", "retrieval", "verification", "memory_read_write",
        "training_amortized", "repair", "other")
ARMS = ("COLD", "INSTRUCTIONS", "RETRIEVAL", "SPIDER", "COMPILED",
        "DIRECT_API", "STAGEHAND_V4_SERVER_CACHE")


def example_rows(replications=12, spider_price=0.005):
    rows = []
    for family, identifier in (("pypi", "httpx"), ("github", "astral-sh/ruff")):
        for replicate in range(replications):
            for arm in ARMS:
                cost = spider_price if arm == "SPIDER" else 0.01
                safe_success = True if arm != "COLD" else replicate % 5 != 0
                rows.append({
                    "task_id": f"{family}:{identifier}", "replicate": replicate,
                    "family": family, "phase": "public-heldout-v1", "arm": arm,
                    "success": safe_success, "safe": True, "cost_usd": cost,
                    "cost_components_usd": {k: cost if k == "model" else 0 for k in CATS},
                    "tokens": 100, "latency_ms": 120, "cost_accounting_complete": True,
                })
    return rows


class DecisionGateTests(unittest.TestCase):
    def test_not_enough_tasks_refuses_go(self):
        outcome = decide(example_rows(3))
        self.assertEqual(outcome["decision"], "INCONCLUSIVE_FIX_EVIDENCE")

    def test_no_win_against_direct_api_stops(self):
        outcome = decide(example_rows(spider_price=0.012))
        self.assertEqual(outcome["decision"], "STOP_OR_PIVOT")
        self.assertEqual(outcome["best_comparator"], "INSTRUCTIONS")

    def test_candidate_is_never_scientific_promotion(self):
        outcome = decide(example_rows(spider_price=0.005))
        self.assertEqual(outcome["decision"], "CANDIDATE_GO_PENDING_INDEPENDENT_AUDIT")
        self.assertIn("never auto-promote", outcome["audit_gate"])

    def test_missing_real_stagehand_fails_closed(self):
        rows = [r for r in example_rows() if r["arm"] != "STAGEHAND_V4_SERVER_CACHE"]
        with self.assertRaisesRegex(ValueError, "incomplete paired"):
            decide(rows)


if __name__ == "__main__":
    unittest.main()
