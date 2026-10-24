import unittest

from scripts.score_product_benchmark import score


class BenchmarkScorerTests(unittest.TestCase):
    def trials(self):
        rows = []
        for arm in ("COLD", "INSTRUCTIONS", "RETRIEVAL", "SPIDER"):
            cost = 2 if arm != "SPIDER" else 1
            rows.append(dict(task_id="test", replicate=0, family="portal",
                             phase="repeat", arm=arm, success=True, safe=True,
                             cost_usd=cost, cost_components_usd={
                                 "model": cost, "browser": 0, "retrieval": 0,
                                 "verification": 0, "memory_read_write": 0,
                                 "training_amortized": 0, "repair": 0, "other": 0,
                             },
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
        rows.append(dict(rows[0], arm="CACHE", cost_usd=1.2,
                         cost_components_usd={**rows[0]["cost_components_usd"], "model": 1.2}))
        self.assertTrue(score(rows, require_cache=True)["strong_cache_competitor_included"])

    def test_refuse_manual_seed_or_missing_itemization(self):
        rows = self.trials()
        rows[-1]["manual_fixture_seed"] = True
        with self.assertRaisesRegex(ValueError, "manual fixture"):
            score(rows)
        rows = self.trials()
        del rows[-1]["cost_components_usd"]
        with self.assertRaisesRegex(ValueError, "cost components"):
            score(rows)
        rows = self.trials()
        rows[-1]["cost_components_usd"]["model"] = 100
        with self.assertRaisesRegex(ValueError, "reconcile"):
            score(rows)

    def test_public_benchmark_requires_direct_api_and_native_cache_when_requested(self):
        rows = []
        arms = ("COLD", "INSTRUCTIONS", "RETRIEVAL", "SPIDER", "COMPILED", "DIRECT_API")
        for arm in arms:
            rows.append(dict(self.trials()[0],
                             task_id="pypi:httpx", family="pypi",
                             phase="public-heldout-v1", arm=arm,
                             manual_fixture_seed=False))
        result = score(rows, public=True)
        self.assertTrue(result["direct_api_comparator_included"])
        with self.assertRaisesRegex(ValueError, "incomplete paired"):
            score(rows[:-1], public=True)
        with self.assertRaisesRegex(ValueError, "incomplete paired"):
            score(rows, public=True, require_native_cache=True)
        rows.append(dict(rows[0], arm="STAGEHAND_V4_SERVER_CACHE"))
        self.assertTrue(score(rows, public=True, require_native_cache=True)["native_stagehand_cache_included"])

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
