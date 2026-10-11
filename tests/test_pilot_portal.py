import asyncio
import json
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from run_real_agent_pilot import checked_answer, run_trial, seed_fixture_mechanism
from spider.pilot_portal import start_portal
from spider.registry import MechanismRegistry
from spider.kernel import SpiderKernel


class PortalFixtureTests(unittest.TestCase):
    def test_http_browser_workflow_has_three_real_steps(self):
        server, thread, base = start_portal()
        try:
            with urllib.request.urlopen(base) as r:
                self.assertIn(b"/portal/invoices", r.read())
            with urllib.request.urlopen(base + "/portal/invoices") as r:
                self.assertIn(b"Reference ID", r.read())
            with urllib.request.urlopen(base + "/portal/invoices/search?id=A-101") as r:
                self.assertIn(b"Open matching record", r.read())
            with urllib.request.urlopen(base + "/portal/invoices/view?id=A-101") as r:
                self.assertIn(b"CHF 138.45", r.read())
            with urllib.request.urlopen(base + "/api/invoices/A-101") as r:
                payload = json.loads(r.read())
                self.assertEqual(payload["answer"], "CHF 138.45")
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                urllib.request.urlopen(base + "/api/shipments/A-101")
            self.assertEqual(ctx.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_bounded_seed_parameterizes_new_id(self):
        with tempfile.TemporaryDirectory() as td:
            registry = MechanismRegistry(Path(td) / "store.jsonl")
            seed_fixture_mechanism(registry, "shipments", "http://127.0.0.1:41111")
            resolution = SpiderKernel(registry).resolve(
                "read-shipments",
                {"origin": "http://127.0.0.1:41111", "family": "shipments"},
                {"id": "S-902"},
            )
            self.assertEqual(resolution.bound_action["url"], "http://127.0.0.1:41111/api/shipments/S-902")

    def test_seeded_spider_executes_without_model_and_reports_unpriced_cost(self):
        def no_agent(*_args, **_kwargs):
            raise AssertionError("no model calls should be necessary for verified fixture mechanism")
        with patch("run_real_agent_pilot.execute_browser_use", side_effect=no_agent):
            for family, identifier in [("invoices", "A-202"), ("shipments", "S-902")]:
                report = run_trial("SPIDER", family, identifier, "google", None, True)
                self.assertEqual(report["path"], "inheritance")
                self.assertTrue(report["success"])
                self.assertFalse(report["cost_accounting_complete"])
                self.assertIsNone(report["cost_usd"])
                self.assertEqual(report["http_requests_from_spider"], 1)

    def test_unseeded_spider_uses_actual_agent_callback_contract(self):
        async def fake_agent(*_args, **_kwargs):
            return {"answer": "Delivered", "tokens": 11, "model_cost_usd": 0.01}
        with patch("run_real_agent_pilot.execute_browser_use", side_effect=fake_agent):
            report = run_trial("SPIDER", "shipments", "S-501", "google", None, False)
            self.assertEqual(report["path"], "agent")
            self.assertTrue(report["success"])
            self.assertEqual(report["tokens"], 11)

    def test_answers_not_substrings_of_other_values(self):
        self.assertTrue(checked_answer("Final: CHF 138.45", "CHF 138.45"))
        self.assertFalse(checked_answer("CHF 138.450", "CHF 138.45"))
        self.assertFalse(checked_answer("In transit", "Delivered"))


if __name__ == "__main__":
    unittest.main()
