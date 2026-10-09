import tempfile
import unittest
from pathlib import Path

from spider import (
    Mechanism,
    Observation,
    SpiderKernel,
    ResolutionStatus,
    TrajectoryCounters,
)
from spider.registry import MechanismRegistry


class KernelTests(unittest.TestCase):
    def make_kernel(self):
        td = tempfile.TemporaryDirectory()
        reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
        return td, reg, SpiderKernel(reg)

    def test_unknown_is_default(self):
        td, reg, kernel = self.make_kernel()
        try:
            r = kernel.resolve("delete", {"authenticated": True})
            self.assertEqual(r.status, ResolutionStatus.UNKNOWN)
        finally:
            td.cleanup()

    def test_parameterized_mechanism_binds_only_when_guarded(self):
        td, reg, kernel = self.make_kernel()
        try:
            reg.upsert(Mechanism(mechanism_id="delete-item", intent="delete", preconditions={"authenticated": True}, applicability_guards={"role": "owner"}, action_template={"method": "DELETE", "path": "/api/items/${id}"}, postconditions={"exists": False}, parameter_slots=["id"], confidence=0.95))
            r = kernel.resolve("delete", {"authenticated": True, "role": "owner"}, {"id": "B"})
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action["path"], "/api/items/B")
            denied = kernel.resolve("delete", {"authenticated": True, "role": "viewer"}, {"id": "B"})
            self.assertEqual(denied.status, ResolutionStatus.UNKNOWN)
        finally:
            td.cleanup()

    def test_invalidation_forces_abstention(self):
        td, reg, kernel = self.make_kernel()
        try:
            reg.upsert(Mechanism(mechanism_id="m", intent="x", preconditions={}, action_template={"op": "x"}, postconditions={"ok": True}, confidence=1.0))
            self.assertEqual(kernel.resolve("x", {}).status, ResolutionStatus.EXECUTABLE)
            self.assertTrue(kernel.invalidate("m"))
            self.assertEqual(kernel.resolve("x", {}).status, ResolutionStatus.UNKNOWN)
        finally:
            td.cleanup()


class ParameterizedDistillTests(unittest.TestCase):
    """Contract tests for the parameterized distillation path added for
    EXP-PRODUCT-37950607128. These exercise the exact mechanism used by the
    arm-differentiation certificate: distill_parameterized -> resolve -> execute
    -> verify, with refusals on out-of-support / missing parameters."""

    def make_kernel(self, counters=None):
        td = tempfile.TemporaryDirectory()
        reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
        return td, reg, SpiderKernel(reg, counters=counters)

    @staticmethod
    def url_observations():
        return [
            Observation(
                intent="fetch",
                state={"site": "x"},
                action={"method": "GET", "url": "https://e.invalid/items/a1"},
                next_state={"status": 200, "echo": "a1"},
                success=True,
            ),
            Observation(
                intent="fetch",
                state={"site": "x"},
                action={"method": "GET", "url": "https://e.invalid/items/a2"},
                next_state={"status": 200, "echo": "a2"},
                success=True,
            ),
            Observation(
                intent="fetch",
                state={"site": "x"},
                action={"method": "GET", "url": "https://e.invalid/items/a3"},
                next_state={"status": 200, "echo": "a3"},
                success=True,
            ),
        ]

    def test_distill_parameterized_infers_single_path_slot(self):
        td, reg, kernel = self.make_kernel()
        try:
            m = kernel.distill_parameterized(self.url_observations())
            self.assertIsNotNone(m)
            self.assertEqual(len(m.parameter_slots), 1)
            slot = m.parameter_slots[0]
            self.assertIn("${" + slot + "}", m.action_template["url"])
            self.assertIn(slot, m.verification_rule["parameter_supports"])
            self.assertGreaterEqual(m.confidence, 0.8)
        finally:
            td.cleanup()

    def test_parameterized_roundtrip_and_verify(self):
        td, reg, kernel = self.make_kernel()
        try:
            m = kernel.distill_parameterized(self.url_observations())
            reg.upsert(m)
            slot = m.parameter_slots[0]
            r = kernel.resolve("fetch", {"site": "x"}, {slot: "a9"})
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action["url"], "https://e.invalid/items/a9")
            self.assertTrue(
                kernel.verify(
                    m.mechanism_id,
                    {"status": 200, "echo": "a9"},
                    {slot: "a9"},
                )
            )
            self.assertFalse(
                kernel.verify(
                    m.mechanism_id,
                    {"status": 200, "echo": "wrong"},
                    {slot: "a9"},
                )
            )
        finally:
            td.cleanup()

    def test_out_of_support_and_missing_params_refuse(self):
        td, reg, kernel = self.make_kernel()
        try:
            m = kernel.distill_parameterized(self.url_observations())
            reg.upsert(m)
            slot = m.parameter_slots[0]
            bad = kernel.resolve("fetch", {"site": "x"}, {slot: "not a valid token"})
            self.assertNotEqual(bad.status, ResolutionStatus.EXECUTABLE)
            self.assertIsNone(bad.bound_action)
            self.assertTrue(bad.reason)
            missing = kernel.resolve("fetch", {"site": "x"}, {})
            self.assertNotEqual(missing.status, ResolutionStatus.EXECUTABLE)
            self.assertIsNone(missing.bound_action)
        finally:
            td.cleanup()

    def test_wrong_intent_refuses(self):
        td, reg, kernel = self.make_kernel()
        try:
            m = kernel.distill_parameterized(self.url_observations())
            reg.upsert(m)
            slot = m.parameter_slots[0]
            r = kernel.resolve("delete", {"site": "x"}, {slot: "a9"})
            self.assertNotEqual(r.status, ResolutionStatus.EXECUTABLE)
        finally:
            td.cleanup()

    def test_counters_record_inherited_path_increments(self):
        counters = TrajectoryCounters()
        td, reg, kernel = self.make_kernel(counters=counters)
        try:
            m = kernel.distill_parameterized(self.url_observations())
            reg.upsert(m)
            slot = m.parameter_slots[0]
            kernel.resolve("fetch", {"site": "x"}, {slot: "a9"})
            self.assertEqual(counters.retrieval_calls, 1)
            kernel.verify(m.mechanism_id, {"status": 200, "echo": "a9"}, {slot: "a9"})
            self.assertEqual(counters.verification_calls, 1)
            kernel.rebind(m.mechanism_id, {"site": "x"}, {slot: "a9"})
            self.assertEqual(counters.repair_attempts, 1)
        finally:
            td.cleanup()

    def test_literal_distill_stays_below_execution_confidence(self):
        td, reg, kernel = self.make_kernel()
        try:
            m = kernel.distill(self.url_observations()[0])
            reg.upsert(m)
            self.assertEqual(m.confidence, 0.5)
            r = kernel.resolve("fetch", {"site": "x"})
            self.assertEqual(r.status, ResolutionStatus.EXPLORE)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
