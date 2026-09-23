import tempfile
import unittest
from pathlib import Path

from spider import Mechanism, SpiderKernel, ResolutionStatus
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

    def test_dotted_parameter_slot_binds_fully(self):
        """EXP-PRODUCT-35921344930 binding fix: _PARAMETER must accept dots in slot
        names so ${store.id} binds as one slot instead of ${store} + literal '.id}'."""
        td, reg, kernel = self.make_kernel()
        try:
            reg.upsert(Mechanism(
                mechanism_id="get-store",
                intent="fetch",
                preconditions={"authenticated": True},
                action_template={"method": "GET", "url": "https://api.example.com/stores/${store.id}/orders"},
                postconditions={"ok": True},
                parameter_slots=["store.id"],
                confidence=0.95,
            ))
            # _template_slots must return the full dotted name.
            from spider.kernel import _template_slots
            slots = _template_slots({"url": "https://api.example.com/stores/${store.id}/orders"})
            self.assertEqual(slots, {"store.id"})
            # resolve() must require the dotted slot and produce a fully substituted action.
            missing = kernel.resolve("fetch", {"authenticated": True}, {})
            self.assertEqual(missing.status, ResolutionStatus.UNKNOWN)
            r = kernel.resolve("fetch", {"authenticated": True}, {"store.id": "42"})
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action["url"], "https://api.example.com/stores/42/orders")
        finally:
            td.cleanup()

    def test_plain_identifier_slot_still_binds(self):
        """Regression: the dot-tolerant regex must not change plain ${id} behavior."""
        td, reg, kernel = self.make_kernel()
        try:
            reg.upsert(Mechanism(
                mechanism_id="del",
                intent="delete",
                preconditions={"authenticated": True},
                action_template={"method": "DELETE", "path": "/api/items/${id}"},
                postconditions={"exists": False},
                parameter_slots=["id"],
                confidence=0.95,
            ))
            r = kernel.resolve("delete", {"authenticated": True}, {"id": "B"})
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action["path"], "/api/items/B")
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
