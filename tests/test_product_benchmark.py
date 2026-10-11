import unittest

from scripts.score_product_benchmark import score


class BenchmarkScorerTests(unittest.TestCase):
    def trials(self):
        rows = []
        for arm in ("COLD", "INSTRUCTIONS", "RETRIEVAL", "SPIDER"):
            rows.append(dict(task_id="test", replicate=0, family="portal",
                             phase="repeat", arm=arm, success=True, safe=True,
                             cost_usd=2 if arm != "SPIDER" else 1,
                             latency_ms=100, tokens=100, cost_accounting_complete=True))
        return rows

    def test_descriptive_cost_not_a_claim(self):
        s = score(self.trials())
        self.assertEqual(s["arms"]["SPIDER"]["cost_per_safe_success_usd"], 1)
        self.assertEqual(s["arms"]["COLD"]["cost_per_safe_success_usd"], 2)
        self.assertTrue(s["baseline_ceiling_warning"])
        self.assertIn("DESCRIPTIVE_ONLY", s["status"])

    def test_incomplete_cost_accounting_refused(self):
        rows = self.trials()
        rows[0]["cost_accounting_complete"] = False
        with self.assertRaisesRegex(ValueError, "incomplete cost"):
            score(rows)

    def test_strong_cache_required_when_requested(self):
        with self.assertRaisesRegex(ValueError, "incomplete paired"):
            score(self.trials(), require_cache=True)
        rows = self.trials()
        rows.append(dict(rows[0], arm="CACHE", cost_usd=1.2))
        self.assertTrue(score(rows, require_cache=True)["strong_cache_competitor_included"])

    def test_missing_arm_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "incomplete paired"):
            score(self.trials()[:-1])

    def test_mismatched_task_family_fails_closed(self):
        rows = self.trials()
        rows[-1]["family"] = "different"
        with self.assertRaisesRegex(ValueError, "mismatch"):
            score(rows)

    def test_unsafe_success_not_counted(self):
        rows = self.trials()
        rows[-1]["safe"] = False
        s = score(rows)
        self.assertIsNone(s["arms"]["SPIDER"]["cost_per_safe_success_usd"])


if __name__ == "__main__":
    unittest.main()
