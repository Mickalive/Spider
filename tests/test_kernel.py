import tempfile
import unittest
from pathlib import Path

from spider import Mechanism, SpiderKernel, ResolutionStatus
from spider.models import Observation
from spider.registry import MechanismRegistry

#: Intent namespaces on both resources (prereg section 5.1).
INTENT_NS = {
    "read-item": ["read-product"],
    "update-item": ["update-product"],
    "delete-item": ["delete-product"],
}


def make_observations(prefix, count, path_fmt="/items/{}"):
    """Resource-A observations whose only varying field is the identifier."""
    out = []
    for i in range(1, count + 1):
        identifier = f"{prefix}-{i}"
        out.append(
            Observation(
                intent="read-item",
                state={"collection": "items"},
                action={"method": "GET", "path": path_fmt.format(identifier)},
                next_state={"status": 200, "exists": True, "id": identifier},
                success=True,
            )
        )
    return out


class KernelTests(unittest.TestCase):
    def make_kernel(self, intent_namespace_map=None):
        td = tempfile.TemporaryDirectory()
        reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
        return td, reg, SpiderKernel(reg, intent_namespace_map=intent_namespace_map)

    def test_unknown_is_default(self):
        td, reg, kernel = self.make_kernel()
        try:
            r = kernel.resolve("delete", {"collection": "items"})
            self.assertEqual(r.status, ResolutionStatus.UNKNOWN)
        finally:
            td.cleanup()

    def test_parameterized_mechanism_binds_only_when_guarded(self):
        td, reg, kernel = self.make_kernel()
        try:
            reg.upsert(Mechanism(mechanism_id="delete-item", intent="delete", preconditions={"collection": "items"}, applicability_guards={"role": "owner"}, action_template={"method": "DELETE", "path": "/items/${id}"}, postconditions={"exists": False}, parameter_slots=["id"], confidence=0.95))
            r = kernel.resolve("delete", {"collection": "items", "role": "owner"}, {"id": "B"})
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action["path"], "/items/B")
            denied = kernel.resolve("delete", {"collection": "items", "role": "viewer"}, {"id": "B"})
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


class ParameterInductionTests(unittest.TestCase):
    """All of these go THROUGH distill_parameterized()."""

    def make_kernel(self, intent_namespace_map=None):
        td = tempfile.TemporaryDirectory()
        reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
        return td, reg, SpiderKernel(reg, intent_namespace_map=intent_namespace_map)

    def test_t1_distill_parameterized_induces_slots_and_calibrated_confidence(self):
        """T1: parameter_slots induced, confidence >= 0.8, prefix-preserved path."""
        td, reg, kernel = self.make_kernel()
        try:
            built = kernel.distill_parameterized(make_observations("item", 12))
            self.assertEqual(len(built), 1)
            mech = built[0]
            self.assertIn("id", mech.parameter_slots)
            self.assertGreaterEqual(mech.confidence, 0.8)
            # Prefix preserved: the template has the collection slot and id slot
            self.assertEqual(mech.action_template["path"], "/${collection}/${id}")
            reg.upsert(mech)
        finally:
            td.cleanup()

    def test_t2_resolve_on_resource_b_binds_and_is_executable(self):
        """T2: EXECUTABLE with bound_action.path == '/items/B123' via namespace map."""
        td, reg, kernel = self.make_kernel(INTENT_NS)
        try:
            for mech in kernel.distill_parameterized(make_observations("item", 12)):
                reg.upsert(mech)
            r = kernel.resolve(
                "read-product",
                {"collection": "products"},
                {"id": "B123", "collection": "products"},
            )
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action["path"], "/products/B123")
        finally:
            td.cleanup()

    def test_t3_verify_accepts_observed_next_state(self):
        """T3: verify() on the observed next_state returns True."""
        td, reg, kernel = self.make_kernel(INTENT_NS)
        try:
            built = kernel.distill_parameterized(make_observations("item", 12))
            for mech in built:
                reg.upsert(mech)
            r = kernel.resolve("read-product", {"collection": "products"}, {"id": "B123", "collection": "products"})
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertTrue(kernel.verify(r.mechanism_id, {"status": 200, "exists": True}))
        finally:
            td.cleanup()

    def test_t4_shuffled_labels_reduce_confidence_below_threshold(self):
        """T4: permuted intent labels induce low confidence (null control)."""
        td, reg, kernel = self.make_kernel()
        try:
            # Build observations where each intent group mixes verbs, so the
            # modal method agrees with only a fraction of observations.
            methods = ["GET", "PUT", "DELETE"]
            intents = ["read-item", "update-item", "delete-item"]
            mixed = []
            for i in range(12):
                identifier = f"item-{i + 1}"
                intent = intents[i % 3]
                method = methods[(i // 3 + i % 3) % 3]
                mixed.append(Observation(
                    intent=intent,
                    state={"collection": "items"},
                    action={"method": method, "path": f"/items/{identifier}"},
                    next_state={"status": 200, "id": identifier},
                    success=True,
                ))
            built = kernel.distill_parameterized(mixed)
            for mech in built:
                self.assertLess(mech.confidence, 0.8)
        finally:
            td.cleanup()

    def test_t5_slot_value_guard_rejects_empty_and_malformed(self):
        """T5: slot-value guard abstains on empty and punctuation-laden values."""
        td, reg, kernel = self.make_kernel(INTENT_NS)
        try:
            for mech in kernel.distill_parameterized(make_observations("item", 12)):
                reg.upsert(mech)
            # Empty string binding -> UNKNOWN
            r = kernel.resolve("read-product", {"collection": "products"}, {"id": "", "collection": "products"})
            self.assertEqual(r.status, ResolutionStatus.UNKNOWN)
            # Punctuation-laden binding -> UNKNOWN
            r = kernel.resolve("read-product", {"collection": "products"}, {"id": "SKU-X!!unsupported!!", "collection": "products"})
            self.assertEqual(r.status, ResolutionStatus.UNKNOWN)
            # Valid binding -> EXECUTABLE
            r = kernel.resolve("read-product", {"collection": "products"}, {"id": "PROD-100", "collection": "products"})
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
        finally:
            td.cleanup()

    def test_t6_identity_slot_induced_not_pinned(self):
        """T6: collection segment is induced as a slot, not pinned."""
        td, reg, kernel = self.make_kernel()
        try:
            built = kernel.distill_parameterized(make_observations("item", 12))
            self.assertEqual(len(built), 1)
            mech = built[0]
            self.assertIn("collection", mech.parameter_slots)
            self.assertEqual(mech.action_template["path"], "/${collection}/${id}")
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
