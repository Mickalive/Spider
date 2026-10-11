import json
import sys
import tempfile
import unittest
from pathlib import Path

from spider.pilot_learning import compile_browser_traces, parse_verified_detail
from spider.pilot_portal import EVAL_IDS, TRAIN_IDS
from spider.registry import MechanismRegistry
from spider.kernel import SpiderKernel

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_real_agent_pilot import run_trial


def traces(family="invoices"):
    ids = TRAIN_IDS[family]
    return [
        {
            "identifier": reference,
            "final_url": "http://127.0.0.1:3111/portal/" + family + "/view?id=" + reference,
            "answer": "value-" + reference,
            "page_html": "<h1>Record details</h1><p>Reference: " + reference +
                         "</p><strong id='answer'>value-" + reference + "</strong>",
        }
        for reference in ids
    ]


class BrowserTraceCompilerTests(unittest.TestCase):
    def test_disjoint_training_evaluation(self):
        for family in TRAIN_IDS:
            self.assertFalse(set(TRAIN_IDS[family]) & set(EVAL_IDS[family]))

    def test_bounded_learning_compiles_parameterized_heldout_id(self):
        m = compile_browser_traces("invoices", traces())
        with tempfile.TemporaryDirectory() as tmp:
            reg = MechanismRegistry(Path(tmp) / "learning.jsonl")
            reg.upsert(m)
            new_id = EVAL_IDS["invoices"][0]
            r = SpiderKernel(reg).resolve(
                "read-invoices",
                {"family": "invoices", "portal_schema": "local-fixture-v1",
                 "execution_surface": "loopback-fixture"},
                {"id": new_id})
            self.assertEqual(r.bound_action["path"], "/portal/invoices/view?id=" + new_id)
            actual = run_trial("SPIDER", "invoices", new_id, "google", None,
                               False, memory_path=Path(tmp) / "learning.jsonl")
            self.assertTrue(actual["success"])
            self.assertEqual(actual["path"], "inheritance")
            self.assertEqual(actual["http_requests_from_spider"], 1)
            self.assertTrue(actual["learned_browser_trace_available"])
            self.assertFalse(actual["cost_accounting_complete"])

    def test_rejects_different_origin_or_route_or_ids(self):
        examples = traces()
        examples[1]["final_url"] = examples[1]["final_url"].replace("127.0.0.1:3111", "evil.example")
        with self.assertRaises(ValueError):
            compile_browser_traces("invoices", examples)
        examples = traces()
        examples[1]["final_url"] += "&secret=1"
        with self.assertRaises(ValueError):
            compile_browser_traces("invoices", examples)
        examples = traces()
        examples[1]["identifier"] = examples[0]["identifier"]
        with self.assertRaises(ValueError):
            compile_browser_traces("invoices", examples)
        examples = traces()
        examples[0]["answer"] = "fake answer"
        with self.assertRaises(ValueError):
            compile_browser_traces("invoices", examples)

    def test_verification_requires_matching_record_and_id(self):
        html = '<p>Reference: A-303</p><strong id="answer">CHF 875.00</strong>'
        self.assertEqual(parse_verified_detail(html, "A-303"), "CHF 875.00")
        self.assertIsNone(parse_verified_detail(html, "A-404"))
        self.assertIsNone(parse_verified_detail("<strong id='answer'>CHF 875.00</strong>", "A-303"))
        self.assertIsNone(parse_verified_detail(html, "../../evil"))


if __name__ == "__main__":
    unittest.main()
