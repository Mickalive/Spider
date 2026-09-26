import json
import tempfile
import unittest
from pathlib import Path

from spider import Mechanism, SpiderKernel, align_parameters, ResolutionStatus
from spider.registry import MechanismRegistry
from spider.models import Observation


def make_observation(intent, state, action, next_state, success=True, provenance=None):
    return Observation(
        intent=intent,
        state=state,
        action=action,
        next_state=next_state,
        success=success,
        provenance=provenance or {},
    )


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

    def test_distill_parameterized_single_param(self):
        """Single-parameter induction works and produces a mechanism with one slot."""
        td, reg, kernel = self.make_kernel()
        try:
            obs_a1 = make_observation("read-item", {"authenticated": True, "token": "tok-a"}, {"method": "GET", "path": "/api/items/item-1"}, {"status_code": 200, "body": {"id": "item-1"}})
            obs_a2 = make_observation("read-item", {"authenticated": True, "token": "tok-a"}, {"method": "GET", "path": "/api/items/item-2"}, {"status_code": 200, "body": {"id": "item-2"}})
            obs_a3 = make_observation("read-item", {"authenticated": True, "token": "tok-a"}, {"method": "GET", "path": "/api/items/item-3"}, {"status_code": 200, "body": {"id": "item-3"}})

            mechanisms = kernel.distill_parameterized([obs_a1, obs_a2, obs_a3])
            self.assertGreaterEqual(len(mechanisms), 1)
            self.assertEqual(mechanisms[0].intent, "read-item")
            self.assertIn("id", mechanisms[0].parameter_slots)
            self.assertIn("${id}", mechanisms[0].action_template["path"])
            self.assertGreaterEqual(mechanisms[0].confidence, 0.8)
        finally:
            td.cleanup()

    def test_distill_parameterized_multi_param(self):
        """Multi-parameter induction produces distinct slot names for different varying fields."""
        td, reg, kernel = self.make_kernel()
        try:
            obs_list1 = make_observation("list-items", {"authenticated": True, "token": "tok-a"}, {"method": "GET", "path": "/api/items", "query": {"page": 1, "limit": 10}}, {"status_code": 200, "body": {"items": []}})
            obs_list2 = make_observation("list-items", {"authenticated": True, "token": "tok-a"}, {"method": "GET", "path": "/api/items", "query": {"page": 2, "limit": 10}}, {"status_code": 200, "body": {"items": []}})
            obs_list3 = make_observation("list-items", {"authenticated": True, "token": "tok-a"}, {"method": "GET", "path": "/api/items", "query": {"page": 3, "limit": 20}}, {"status_code": 200, "body": {"items": []}})

            obs_crud1 = make_observation("create-item", {"authenticated": True, "token": "tok-a"}, {"method": "POST", "path": "/api/items", "body": {"id": "item-1", "label": "a"}}, {"status_code": 201, "body": {"id": "item-1"}})
            obs_crud2 = make_observation("create-item", {"authenticated": True, "token": "tok-a"}, {"method": "POST", "path": "/api/items", "body": {"id": "item-2", "label": "b"}}, {"status_code": 201, "body": {"id": "item-2"}})

            mechanisms = kernel.distill_parameterized([obs_list1, obs_list2, obs_list3, obs_crud1, obs_crud2])
            # Should have at least one mechanism for list-items and one for create-item
            intents = {m.intent for m in mechanisms}
            self.assertIn("list-items", intents)
            self.assertIn("create-item", intents)

            # List mechanism should have page and limit slots
            list_mech = [m for m in mechanisms if m.intent == "list-items"]
            self.assertGreaterEqual(len(list_mech), 1)
            list_slots = set()
            for m in list_mech:
                list_slots.update(m.parameter_slots)
            self.assertIn("page", list_slots)
            self.assertIn("limit", list_slots)

            # All mechanisms should have confidence >= 0.8
            for m in mechanisms:
                self.assertGreaterEqual(m.confidence, 0.8)
        finally:
            td.cleanup()

    def test_distill_parameterized_integer_params(self):
        """Integer-valued query parameters are correctly aligned as slots."""
        td, reg, kernel = self.make_kernel()
        try:
            obs1 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/items", "query": {"page": 1}}, {"status_code": 200})
            obs2 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/items", "query": {"page": 2}}, {"status_code": 200})
            obs3 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/items", "query": {"page": 3}}, {"status_code": 200})

            mechanisms = kernel.distill_parameterized([obs1, obs2, obs3])
            self.assertGreaterEqual(len(mechanisms), 1)
            m = mechanisms[0]
            self.assertIn("page", m.parameter_slots)
            self.assertGreaterEqual(m.confidence, 0.8)
        finally:
            td.cleanup()

    def test_distill_parameterized_noise_filtering(self):
        """Noise fields (timestamp, request_id, server_id) are excluded from slot induction."""
        td, reg, kernel = self.make_kernel()
        try:
            obs1 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/items/item-1", "headers": {"timestamp": "2024-01-01", "request_id": "abc"}}, {"status_code": 200})
            obs2 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/items/item-2", "headers": {"timestamp": "2024-01-02", "request_id": "def"}}, {"status_code": 200})

            mechanisms = kernel.distill_parameterized([obs1, obs2])
            # Should still find the id slot from the path
            self.assertGreaterEqual(len(mechanisms), 1)
            # No noise fields should be parameter slots
            for m in mechanisms:
                for slot in m.parameter_slots:
                    self.assertNotIn(slot, {"timestamp", "request_id", "server_id"})
        finally:
            td.cleanup()

    def test_distill_parameterized_pattern_absence(self):
        """Unrelated observations produce 0 slots, not hallucinated slots."""
        td, reg, kernel = self.make_kernel()
        try:
            # Observations with no structurally varying action-template fields
            obs1 = make_observation("ping", {"authenticated": True}, {"method": "GET", "path": "/api/ping"}, {"status_code": 200})
            obs2 = make_observation("ping", {"authenticated": True}, {"method": "GET", "path": "/api/ping"}, {"status_code": 200})
            obs3 = make_observation("ping", {"authenticated": True}, {"method": "GET", "path": "/api/ping"}, {"status_code": 200})

            mechanisms = kernel.distill_parameterized([obs1, obs2, obs3])
            # All identical paths - no varying fields, should produce no mechanisms
            # OR mechanisms with the same path (no ${} template)
            for m in mechanisms:
                # The path should not have a ${} slot if it doesn't vary
                self.assertNotIn("${", str(m.action_template.get("path", "")))
        finally:
            td.cleanup()

    def test_distill_parameterized_credential_safe(self):
        """Templates store ${auth_token} placeholder, no live credentials."""
        td, reg, kernel = self.make_kernel()
        try:
            obs1 = make_observation("read-item", {"authenticated": True, "token": "tok-secret-123"}, {"method": "GET", "path": "/api/items/item-1", "headers": {"Authorization": "Bearer tok-secret-123"}}, {"status_code": 200})
            obs2 = make_observation("read-item", {"authenticated": True, "token": "tok-secret-456"}, {"method": "GET", "path": "/api/items/item-2", "headers": {"Authorization": "Bearer tok-secret-456"}}, {"status_code": 200})

            mechanisms = kernel.distill_parameterized([obs1, obs2])
            for m in mechanisms:
                # Check no live token in template
                action_str = json.dumps(m.action_template)
                self.assertNotIn("tok-secret", action_str)
                # Should have auth_token slot
                if "auth_token" in m.parameter_slots:
                    self.assertIn("${auth_token}", action_str)
        finally:
            td.cleanup()

    def test_align_parameters_standalone(self):
        """align_parameters works as a standalone function."""
        obs1 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/items/item-1"}, {"status_code": 200})
        obs2 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/items/item-2"}, {"status_code": 200})

        mechanisms = align_parameters([obs1, obs2])
        self.assertGreaterEqual(len(mechanisms), 1)
        self.assertEqual(mechanisms[0].intent, "read-item")
        self.assertIn("id", mechanisms[0].parameter_slots)

    def test_distill_parameterized_register(self):
        """register=True actually registers mechanisms in the registry."""
        td, reg, kernel = self.make_kernel()
        try:
            obs1 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/items/item-1"}, {"status_code": 200})
            obs2 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/items/item-2"}, {"status_code": 200})

            mechanisms = kernel.distill_parameterized([obs1, obs2], register=True)
            all_mechs = reg.all()
            self.assertGreaterEqual(len(all_mechs), 1)
            self.assertEqual(all_mechs[0].intent, "read-item")
        finally:
            td.cleanup()

    def test_full_parameterized_flow(self):
        """End-to-end test: induce, register, resolve, bind, verify."""
        td, reg, kernel = self.make_kernel()
        try:
            obs1 = make_observation("read-item", {"authenticated": True, "token": "tok-a"}, {"method": "GET", "path": "/api/items/item-1"}, {"status_code": 200, "body": {"id": "item-1"}})
            obs2 = make_observation("read-item", {"authenticated": True, "token": "tok-a"}, {"method": "GET", "path": "/api/items/item-2"}, {"status_code": 200, "body": {"id": "item-2"}})
            obs3 = make_observation("read-item", {"authenticated": True, "token": "tok-a"}, {"method": "GET", "path": "/api/items/item-3"}, {"status_code": 200, "body": {"id": "item-3"}})

            mechanisms = kernel.distill_parameterized([obs1, obs2, obs3], register=True)
            self.assertGreaterEqual(len(mechanisms), 1)

            # Resolve with bound parameters
            m = mechanisms[0]
            params = {slot: "item-42" for slot in m.parameter_slots}
            params["token"] = "tok-a"
            resolution = kernel.resolve(m.intent, {"authenticated": True, "token": "tok-a"}, params)
            self.assertEqual(resolution.status, ResolutionStatus.EXECUTABLE)
            self.assertIsNotNone(resolution.bound_action)

            # Verify the bound action
            self.assertIsNotNone(resolution.bound_action)
        finally:
            td.cleanup()

    def test_no_double_prefix_in_template(self):
        """Full-value identifiers produce ${id} not double-prefixed templates."""
        td, reg, kernel = self.make_kernel()
        try:
            obs1 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/v1/items/item-42"}, {"status_code": 200})
            obs2 = make_observation("read-item", {"authenticated": True}, {"method": "GET", "path": "/api/v1/items/item-99"}, {"status_code": 200})

            mechanisms = kernel.distill_parameterized([obs1, obs2])
            for m in mechanisms:
                path = m.action_template.get("path", "")
                # Should have ${id} not ${item-42} or double-prefix
                self.assertIn("${", path)
                # The path should not contain the full identifier literal
                self.assertNotIn("item-42", path)
                self.assertNotIn("item-99", path)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
