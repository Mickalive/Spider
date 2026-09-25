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

    def test_dotted_slots_bind_and_gate(self):
        """Frozen C-LLM-INHERIT dot-regex (MV3): dotted keys like item.id,
        family.id, user.profile.id must be captured, bound and family-gated."""
        from spider.kernel import _PARAMETER
        self.assertEqual(
            _PARAMETER.pattern,
            r"\$\{([A-Za-z_][A-Za-z0-9_\.]*)\}",
            "kernel must use the frozen dotted-parameter regex")
        td, reg, kernel = self.make_kernel()
        try:
            cases = [
                ("family_00", "/api/items/${item.id}", "IT-77", "item.id"),
                ("family_01", "/api/families/${family.id}/items", "fam_03", "family.id"),
                ("family_02", "https://${site.name}/catalog", "shop07.example.com", "site.name"),
                ("family_03", "/api/users/${user.profile.id}/profile", "u-9182", "user.profile.id"),
                ("family_04", "/orders/${order.item.sku}/status", "SKU-42A", "order.item.sku"),
            ]
            for fid, template, value, slot in cases:
                reg.upsert(Mechanism(
                    mechanism_id=f"m-{fid}", intent="browse",
                    preconditions={"family_id": fid},
                    applicability_guards={"family_id": fid},
                    action_template={"url": template},
                    postconditions={"url": template.replace("${" + slot + "}", value)},
                    parameter_slots=[slot], confidence=0.85))
                r = kernel.resolve("browse", {"family_id": fid}, {slot: value})
                self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
                self.assertEqual(r.bound_action["url"], template.replace("${" + slot + "}", value))
                wrong = kernel.resolve("browse", {"family_id": "family_99"}, {slot: value})
                self.assertEqual(wrong.status, ResolutionStatus.UNKNOWN)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
