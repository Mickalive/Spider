import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_pilot_matrix import ARMS, make_plan


class PilotPlanTests(unittest.TestCase):
    def test_plan_is_randomized_but_complete_and_reproducible(self):
        rows = make_plan(101, 2)
        self.assertEqual(rows, make_plan(101, 2))
        self.assertEqual(len(rows), 32)
        buckets = {}
        for row in rows:
            buckets.setdefault((row["task_id"], row["replicate"]), set()).add(row["arm"])
        self.assertEqual(len(buckets), 8)
        self.assertTrue(all(arms == set(ARMS) for arms in buckets.values()))

    def test_invalid_replicate_count(self):
        with self.assertRaises(ValueError):
            make_plan(1, 0)


if __name__ == "__main__":
    unittest.main()
