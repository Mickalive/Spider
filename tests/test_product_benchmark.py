import unittest

from scripts.score_product_benchmark import score


class BenchmarkScorerTests(unittest.TestCase):
    def trials(self):
        rows = []
        for arm in ("COLD", "INSTRUCTIONS", "RETRIEVAL", "SPIDER"):
            rows.append(dict(task_id="test", replicate=0, family="portal",
                             phase="repeat", arm=arm, success=True, safe=True,
                             cost_usd=2 if arm != "SPIDER" else 1,
                             latency_ms=100, tokens=100))
        return rows

    def test_descriptive_cost_not_a_claim(self):
        s = score(self.trials())
        self.assertEqual(s["arms"]["SPIDER"]["cost_per_safe_success_usd"], 1)
        self.assertEqual(s["arms"]["COLD"]["cost_per_safe_success_usd"], 2)
        self.assertTrue(s["baseline_ceiling_warning"])
        self.assertIn("DESCRIPTIVE_ONLY", s["status"])

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
