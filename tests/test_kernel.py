import json
import tempfile
import unittest
from pathlib import Path

from spider import Mechanism, Observation, SpiderKernel, ResolutionStatus, align_parameters, distill_parameterized
from spider.kernel import _bind
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


def _obs(intent, action, *, state=None, identifier=None, success=True, status=200):
    return Observation(
        intent=intent,
        state=state if state is not None else {"auth": "valid_token", "role": "owner", "collection": "items"},
        action=action,
        next_state={"status": status, "ok": True, "resource_present": True},
        success=success,
        provenance={"identifier": identifier, "status": status},
    )


class ParameterInductionTests(unittest.TestCase):
    """Unit tests for the durable C-PARAM-INHERIT induction capability in src/."""

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.reg = MechanismRegistry(Path(self.td.name) / "mechanisms.jsonl")
        self.kernel = SpiderKernel(self.reg)

    def tearDown(self):
        self.td.cleanup()

    def test_single_param_induction(self):
        obs = [_obs("read", {"method": "GET", "path": f"/items/item-{i}"}, identifier=f"item-{i}") for i in range(1, 6)]
        mechs = distill_parameterized(obs)
        self.assertEqual(len(mechs), 1)
        m = mechs[0]
        self.assertEqual(m.action_template["method"], "GET")
        self.assertEqual(m.action_template["path"], "/items/item-${id}")
        self.assertEqual(m.parameter_slots, ["id"])
        self.assertGreaterEqual(m.confidence, 0.8)
        self.assertNotEqual(m.confidence, 0.5)

    def test_multi_param_induction_links_varying_context(self):
        obs = []
        for collection, prefix in (("items", "item"), ("tags", "tag")):
            for i in range(1, 6):
                obs.append(
                    _obs(
                        "read",
                        {"method": "GET", "path": f"/{collection}/{prefix}-{i}"},
                        state={"auth": "valid_token", "role": "owner", "collection": collection},
                        identifier=f"{prefix}-{i}",
                    )
                )
        # A second intent group where role differs makes `role` a group-level
        # applicability guard rather than a global precondition.
        for collection in ("items", "tags"):
            for i in range(1, 6):
                obs.append(
                    _obs(
                        "list",
                        {"method": "GET", "path": f"/{collection}", "query": {"q": f"cat{i}"}},
                        state={"auth": "valid_token", "role": "viewer", "collection": collection},
                        identifier=collection,
                    )
                )
        mechs = {m.intent: m for m in distill_parameterized(obs)}
        self.assertEqual(sorted(mechs), ["list", "read"])
        m = mechs["read"]
        self.assertEqual(m.action_template["path"], "/${collection}/${id}")
        self.assertEqual(sorted(m.parameter_slots), ["collection", "id"])
        self.assertEqual(m.preconditions, {"auth": "valid_token"})
        self.assertEqual(m.applicability_guards, {"role": "owner"})
        self.assertEqual(m.verification_rule["status"], 200)
        self.assertEqual(mechs["list"].action_template["path"], "/${collection}")
        self.assertEqual(mechs["list"].applicability_guards, {"role": "viewer"})

    def test_single_collection_group_refuses_to_generalize_the_collection(self):
        # Only one collection in the evidence: the collection is a group constant,
        # so it is pinned rather than induced, and the mechanism abstains on
        # another collection instead of guessing.
        obs = [
            _obs("list", {"method": "GET", "path": "/items", "query": {"q": f"cat{i}"}}, identifier="items")
            for i in range(1, 6)
        ]
        m = distill_parameterized(obs)[0]
        self.assertNotIn("collection", m.parameter_slots)
        self.assertEqual(m.action_template["path"], "/items")
        self.assertEqual(
            m.preconditions.get("collection", m.applicability_guards.get("collection")), "items"
        )
        with tempfile.TemporaryDirectory() as name:
            reg = MechanismRegistry(Path(name) / "mechanisms.jsonl")
            kernel = SpiderKernel(reg)
            kernel.registry.upsert(m)
            pinned = kernel.resolve(
                "list", {"auth": "valid_token", "role": "owner", "collection": "items"}, {"q": "cat1"}
            )
            other = kernel.resolve(
                "list", {"auth": "valid_token", "role": "owner", "collection": "products"}, {"q": "cat1"}
            )
            self.assertEqual(pinned.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(other.status, ResolutionStatus.UNKNOWN)

    def test_full_value_identifier_is_not_double_prefixed(self):
        # Each identifier is itself a whole URL with no shared structure beyond the
        # scheme: splicing a prefix on would be exactly the double-prefix defect.
        urls = [
            "https://a.example/r/1", "https://b.example/x/2", "https://c.example/y/3",
            "https://d.example/z/4", "https://e.example/w/5",
        ]
        obs = [_obs("read", {"method": "GET", "url": u}, identifier=u) for u in urls]
        m = distill_parameterized(obs)[0]
        self.assertEqual(m.action_template["url"], "${id}")
        params = align_parameters(m.action_template, obs[0].action)
        self.assertEqual(params["id"], "https://a.example/r/1")
        self.assertEqual(_bind(m.action_template, params)["url"], "https://a.example/r/1")
        self.assertEqual(_bind(m.action_template, {"id": "https://z.example/q"})["url"], "https://z.example/q")

    def test_shared_url_prefix_is_spliced_and_reproduces_every_action(self):
        obs = [_obs("read", {"method": "GET", "url": f"https://api.example.com/items/item-{i}"}, identifier=f"item-{i}") for i in range(1, 6)]
        m = distill_parameterized(obs)[0]
        self.assertEqual(m.action_template["url"], "https://api.example.com/items/item-${id}")
        self.assertEqual(m.action_template["url"].count("https://"), 1)
        # The splice is only accepted because it reconstructs every training action.
        for o in obs:
            params = align_parameters(m.action_template, o.action)
            self.assertIsNotNone(params)
            self.assertEqual(_bind(m.action_template, params), o.action)

    def test_noise_fields_are_not_induced(self):
        obs = [
            _obs(
                "read",
                {
                    "method": "GET",
                    "path": f"/items/item-{i}",
                    "timestamp": 1000 + i,
                    "request_id": f"req-{i}",
                    "trace_id": f"trace-{i}",
                },
                identifier=f"item-{i}",
            )
            for i in range(1, 7)
        ]
        m = distill_parameterized(obs)[0]
        self.assertEqual(set(m.action_template), {"method", "path"})
        self.assertNotIn("timestamp", str(m.action_template))
        self.assertNotIn("request_id", str(m.action_template))
        self.assertEqual(m.action_template["path"], "/items/item-${id}")

    def test_unrelated_evidence_yields_no_slots_and_no_mechanism(self):
        # Same intent label, unrelated actions: the structure gate must abstain
        # rather than hallucinate a mechanism.
        obs = [_obs("mixed", {"method": meth, "path": path}, identifier=path) for meth, path in (
            ("GET", "/a/1"), ("POST", "/b/2"), ("PATCH", "/c/3"), ("PUT", "/d/4"), ("TRACE", "/e/5"),
        )]
        self.assertEqual(distill_parameterized(obs), [])

    def test_secret_header_becomes_slot_not_stored_value(self):
        obs = [
            _obs("read", {"method": "GET", "path": "/items/item-1", "headers": {"Authorization": f"Bearer tok-{i}", "Accept": "application/json"}}, identifier="item-1")
            for i in range(1, 6)
        ]
        m = distill_parameterized(obs)[0]
        self.assertEqual(m.action_template["headers"]["Authorization"], "${auth_token}")
        self.assertEqual(m.action_template["headers"]["Accept"], "application/json")
        self.assertIn("auth_token", m.parameter_slots)
        self.assertNotIn("tok-3", str(m.as_dict()))

    def test_unlinked_varying_context_field_is_dropped(self):
        obs = [
            _obs("read", {"method": "GET", "path": f"/items/item-{i}"}, state={"auth": "valid_token", "role": "owner", "collection": "items", "viewport": f"v{i}"}, identifier=f"item-{i}")
            for i in range(1, 6)
        ]
        m = distill_parameterized(obs)[0]
        self.assertNotIn("viewport", m.parameter_slots)
        self.assertEqual(m.action_template["path"], "/items/item-${id}")
        self.assertEqual(m.parameter_slots, ["id"])

    def test_group_with_no_variation_produces_no_transferable_mechanism(self):
        obs = [
            _obs("read", {"method": "GET", "path": "/items/item-1"}, state={"auth": "valid_token", "role": "owner"}, identifier="item-1")
            for _ in range(5)
        ]
        self.assertEqual(distill_parameterized(obs), [])

    def test_failed_observations_are_never_induced(self):
        good = [_obs("read", {"method": "GET", "path": f"/items/item-{i}"}, identifier=f"item-{i}") for i in range(1, 6)]
        bad = [_obs("read", {"method": "GET", "path": f"/items/broken-{i}"}, identifier=f"broken-{i}", success=False, status=404) for i in range(1, 6)]
        m = distill_parameterized(good + bad)[0]
        self.assertEqual(m.action_template["path"], "/items/item-${id}")
        self.assertEqual(len(m.evidence), 5)

    def test_confidence_is_evidence_derived_and_not_hardcoded(self):
        strong = [_obs("read", {"method": "GET", "path": f"/items/item-{i}"}, identifier=f"item-{i}") for i in range(1, 21)]
        self.assertAlmostEqual(distill_parameterized(strong)[0].confidence, 22 / 23, places=5)
        # An unrelated group cannot be induced at all, so there is no mechanism
        # whose confidence could be quoted as evidence.
        self.assertEqual(
            distill_parameterized(
                [_obs("x", {"method": m, "path": p}) for m, p in (("GET", "/a"), ("POST", "/b"), ("PUT", "/c"), ("DELETE", "/d"), ("HEAD", "/e"))]
            ),
            [],
        )

    def test_kernel_method_registers_mechanisms_and_resolves_on_unseen_identifier(self):
        obs = []
        for collection, prefix in (("items", "item"), ("tags", "tag")):
            for i in range(1, 6):
                obs.append(
                    _obs(
                        "read",
                        {"method": "GET", "path": f"/{collection}/{prefix}-{i}"},
                        state={"auth": "valid_token", "role": "owner", "collection": collection},
                        identifier=f"{prefix}-{i}",
                    )
                )
        mechs = self.kernel.distill_parameterized(obs)
        self.assertEqual(len(mechs), 1)
        self.assertEqual(len(self.reg.all()), 1)
        r = self.kernel.resolve("read", {"auth": "valid_token", "role": "owner"}, {"collection": "products", "id": "SKU-A"})
        self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
        self.assertEqual(r.bound_action["path"], "/products/SKU-A")
        # Unbindable context must abstain rather than guess.
        missing = self.kernel.resolve("read", {"auth": "valid_token", "role": "owner"}, {"id": "SKU-A"})
        self.assertEqual(missing.status, ResolutionStatus.UNKNOWN)
        # Wrong guard must abstain.
        denied = self.kernel.resolve("read", {"auth": "valid_token", "role": "viewer"}, {"collection": "products", "id": "SKU-A"})
        self.assertEqual(denied.status, ResolutionStatus.UNKNOWN)

    def test_integer_valued_slot_round_trips_without_stringification(self):
        # Regression: a query parameter observed as an int (limit, offset, page)
        # must align and rebind as an int. String-only alignment made the
        # leave-one-out self-check fail and forced permanent abstention on the
        # whole family.
        obs = [
            _obs(
                "list",
                {
                    "method": "GET",
                    "path": f"/{coll}",
                    "query": {"q": coll[:-1], "limit": n},
                },
                identifier=coll,
                state={"auth": "valid_token", "role": "owner", "collection": coll},
            )
            for coll in ("items", "tags")
            for n in (1, 2, 3)
        ]
        self.kernel.distill_parameterized(obs)
        template = self.kernel.registry.all()[0].action_template
        self.assertEqual(template["query"]["limit"], "${limit}")
        params = align_parameters(template, obs[-1].action)
        self.assertIsNotNone(params)
        self.assertIsInstance(params["limit"], int)
        self.assertEqual(params["limit"], 3)
        r = self.kernel.resolve(
            "list",
            {"auth": "valid_token", "role": "owner", "collection": "products"},
            {"collection": "products", "q": "SKU", "limit": 5},
        )
        self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
        self.assertIsInstance(r.bound_action["query"]["limit"], int)
        self.assertEqual(r.bound_action["query"]["limit"], 5)

    def test_constant_authorization_header_is_still_redacted(self):
        # Regression: the constant fast path used to copy a field verbatim, so an
        # Authorization header that never varied was persisted into the durable
        # template. Constancy is not permission to store a credential.
        token = "Bearer super-secret-token"
        obs = [
            _obs(
                "read",
                {
                    "method": "GET",
                    "path": f"/items/item-{i}",
                    "headers": {"Authorization": token, "Accept": "application/json"},
                },
                identifier=f"item-{i}",
            )
            for i in range(1, 6)
        ]
        mechanisms = self.kernel.distill_parameterized(obs)
        self.assertEqual(len(mechanisms), 1)
        template = mechanisms[0].action_template
        self.assertEqual(template["headers"]["Authorization"], "${auth_token}")
        self.assertEqual(template["headers"]["Accept"], "application/json")
        self.assertNotIn(token, json.dumps(template))

    def test_learned_mechanism_does_not_resolve_unlearned_intent(self):
        obs = [_obs("read", {"method": "GET", "path": f"/items/item-{i}"}, identifier=f"item-{i}") for i in range(1, 6)]
        self.kernel.distill_parameterized(obs)
        for unlearned in ("archive", "merge", "export", "refund", "delete-all", "reindex"):
            r = self.kernel.resolve(unlearned, {"auth": "valid_token", "role": "owner"}, {"id": "SKU-A"})
            self.assertEqual(r.status, ResolutionStatus.UNKNOWN, unlearned)

    def test_parameterized_mechanism_wins_tie_against_literal(self):
        with tempfile.TemporaryDirectory() as name:
            reg = MechanismRegistry(Path(name) / "mechanisms.jsonl")
            kernel = SpiderKernel(reg)
            reg.upsert(Mechanism(mechanism_id="literal", intent="read", preconditions={"auth": "valid_token"}, action_template={"method": "GET", "path": "/items/item-1"}, postconditions={"status": 200}, confidence=0.8))
            reg.upsert(Mechanism(mechanism_id="param", intent="read", preconditions={"auth": "valid_token"}, action_template={"method": "GET", "path": "/items/${id}"}, postconditions={"status": 200}, parameter_slots=["id"], confidence=0.8))
            r = kernel.resolve("read", {"auth": "valid_token"}, {"id": "SKU-A"})
            self.assertEqual(r.mechanism_id, "param")
            self.assertEqual(r.bound_action["path"], "/items/SKU-A")


if __name__ == "__main__":
    unittest.main()
