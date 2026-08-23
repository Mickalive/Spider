import os
import tempfile
import unittest

from graph.store import Store
from physics.run_wp003 import validate_rows


class GraphStoreIntegrityTests(unittest.TestCase):
    def test_new_fragment_counters_and_timestamps_are_valid(self):
        with tempfile.TemporaryDirectory() as td:
            db = os.path.join(td, "store.sqlite")
            s = Store(db)
            s.save_fragment("goal.test", [{"kind": "click", "target_sig": "a"}], "site")
            row = s.db.execute(
                "SELECT success_count,failure_count,created,last_validated FROM fragments"
            ).fetchone()
            self.assertEqual(row[0], 1)
            self.assertEqual(row[1], 0)
            self.assertGreater(row[2], 1_500_000_000)
            self.assertGreaterEqual(row[3], row[2])


class PhysicsLeakageGuardTests(unittest.TestCase):
    def _row(self, step, target, prev, primary=None):
        return {
            "site": "x",
            "trajectory_id": "x-r0",
            "step_id": step,
            "target_action": target,
            "prev_action_label": prev,
            "primary_action": primary or target,
            "pre": {},
            "post": {},
        }

    def test_true_previous_action_sequence_passes(self):
        rows = [
            self._row(0, "click_link", "<START>"),
            self._row(1, "fill_text", "click_link"),
            self._row(2, "click_button", "fill_text"),
        ]
        validate_rows(rows)

    def test_legacy_rows_without_trajectory_identity_fail(self):
        rows = [{
            "site": "x", "step_id": 0, "target_action": "click_link",
            "prev_action_label": "click_link", "primary_action": "click_link",
            "pre": {}, "post": {},
        }]
        with self.assertRaises(AssertionError):
            validate_rows(rows)

    def test_misaligned_previous_action_fails(self):
        rows = [
            self._row(0, "click_link", "<START>"),
            self._row(1, "fill_text", "fill_text"),
        ]
        with self.assertRaises(AssertionError):
            validate_rows(rows)


if __name__ == "__main__":
    unittest.main()
