import tempfile
import unittest
from pathlib import Path

from spider import Mechanism, SpiderKernel, ResolutionStatus
from spider.models import Observation
from spider.registry import MechanismRegistry

#: Prereg section 7 declares intent namespaces on both resources.
INTENT_NS = {
    "read-item": ["read-product"],
    "create-item": ["create-product"],
    "list-items": ["list-products"],
    "delete-item": ["delete-product"],
}


def make_observations(prefix, count, path_fmt="/api/v1/items/{}"):
    """Resource-A observations whose only varying field is the identifier."""
    out = []
    for i in range(1, count + 1):
        identifier = f"{prefix}-{i}"
        out.append(
            Observation(
                intent="read-item",
                state={"authenticated": True, "collection": "items"},
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


class ParameterInductionTests(unittest.TestCase):
    """Prereg section 6 T1-T5. All of these go THROUGH distill_parameterized()."""

    def make_kernel(self, intent_namespace_map=None):
        td = tempfile.TemporaryDirectory()
        reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
        return td, reg, SpiderKernel(reg, intent_namespace_map=intent_namespace_map)

    def test_t1_distill_parameterized_induces_slot_and_calibrated_confidence(self):
        """T1: parameter_slots == ["id"], confidence >= 0.8, prefix-preserved path."""
        td, reg, kernel = self.make_kernel()
        try:
            built = kernel.distill_parameterized(make_observations("item", 12))
            self.assertEqual(len(built), 1)
            mech = built[0]
            self.assertEqual(mech.parameter_slots, ["id"])
            self.assertGreaterEqual(mech.confidence, 0.8)
            self.assertEqual(mech.action_template["path"], "/api/v1/items/${id}")
            reg.upsert(mech)
        finally:
            td.cleanup()

    def test_t2_resolve_on_resource_b_binds_and_is_executable(self):
        """T2: EXECUTABLE with bound_action.path == '/api/v1/items/B123'."""
        td, reg, kernel = self.make_kernel(INTENT_NS)
        try:
            for mech in kernel.distill_parameterized(make_observations("item", 12)):
                reg.upsert(mech)
            r = kernel.resolve(
                "read-product",
                {"authenticated": True, "collection": "products"},
                {"id": "B123"},
            )
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action["path"], "/api/v1/items/B123")
        finally:
            td.cleanup()

    def test_t3_verify_accepts_observed_next_state(self):
        """T3: verify() on the observed next_state returns True."""
        td, reg, kernel = self.make_kernel(INTENT_NS)
        try:
            built = kernel.distill_parameterized(make_observations("item", 12))
            for mech in built:
                reg.upsert(mech)
            r = kernel.resolve("read-product", {"authenticated": True}, {"id": "B123"})
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertTrue(kernel.verify(r.mechanism_id, {"status": 200, "exists": True}))
        finally:
            td.cleanup()

    def test_t4_paraphrased_intent_resolves_via_namespace_map(self):
        """T4: read-item mechanism answers to read-product through the alias map."""
        td, reg, kernel = self.make_kernel(INTENT_NS)
        try:
            for mech in kernel.distill_parameterized(make_observations("item", 12)):
                reg.upsert(mech)
            paraphrased = kernel.resolve(
                "read-product", {"authenticated": True, "collection": "products"}, {"id": "SKU-A"}
            )
            self.assertEqual(paraphrased.status, ResolutionStatus.EXECUTABLE)
            # Without the namespace map the same mechanism must NOT transfer.
            td2, reg2, bare = self.make_kernel()
            try:
                for mech in bare.distill_parameterized(make_observations("item", 12)):
                    reg2.upsert(mech)
                self.assertNotEqual(
                    bare.resolve("read-product", {"authenticated": True}, {"id": "SKU-A"}).status,
                    ResolutionStatus.EXECUTABLE,
                )
            finally:
                td2.cleanup()
        finally:
            td.cleanup()

    def test_t5_bound_path_never_regresses_to_prefix_free_placeholder(self):
        """T5: regression guard against the parent packet's path defect.

        Induction must always pin a non-empty URL prefix, and the bound path must
        still contain that prefix after binding.
        """
        td, reg, kernel = self.make_kernel(INTENT_NS)
        try:
            for mech in kernel.distill_parameterized(make_observations("item", 12)):
                self.assertTrue(mech.action_template["path"].startswith("/api/v1/items/"))
                self.assertNotEqual(mech.action_template["path"], "${id}")
                reg.upsert(mech)
            r = kernel.resolve("read-product", {"authenticated": True}, {"id": "B7"})
            self.assertEqual(r.bound_action["path"], "/api/v1/items/B7")
            self.assertTrue(r.bound_action["path"].startswith("/api/v1/items/"))
        finally:
            td.cleanup()

    def test_underdetermined_template_cannot_reach_executable(self):
        """A template pinning no prefix with several free positions must abstain.

        This is the property the parent handoff flagged as missing: a permuted
        intent group induces slots, but must not reach EXECUTABLE.
        """
        td, reg, kernel = self.make_kernel()
        try:
            mixed = [
                Observation(
                    intent="shuffled",
                    state={"authenticated": True},
                    action={"method": "GET", "path": p},
                    next_state={"status": 200},
                    success=True,
                )
                for p in ("/items/item-1", "/products/PROD-100", "/categories/cat1", "/widgets/w-9")
            ]
            built = kernel.distill_parameterized(mixed)
            self.assertEqual(len(built), 1)
            reg.upsert(built[0])
            slots = built[0].parameter_slots
            params = {name: f"v{i}" for i, name in enumerate(slots)}
            r = kernel.resolve("shuffled", {"authenticated": True}, params)
            self.assertNotEqual(r.status, ResolutionStatus.EXECUTABLE)
        finally:
            td.cleanup()

    def test_strip_common_prefix_is_segment_granular(self):
        """Induction must not swallow a stable identifier prefix into the slot."""
        from spider.kernel import _strip_common_prefix, _path_template

        paths = ["/api/v1/items/item-1", "/api/v1/items/item-2", "/api/v1/items/item-300"]
        self.assertEqual(_strip_common_prefix(paths), "/api/v1/items")
        template, slots = _path_template(paths)
        self.assertEqual(template, "/api/v1/items/${id}")
        self.assertEqual(slots, ["id"])


if __name__ == "__main__":
    unittest.main()

