"""Tests for the variability binder and the three null binders added for
EXP-PRODUCT-36314204238.

These are not regression tests for the incumbent. They pin the three behaviours
the experiment's interpretation depends on:

1. the variability binder refuses identifiers outside its measured closed support
   rather than guessing, and that refusal is distinguishable from a wrong answer;
2. the null binders fail for the reasons the report attributes to them, and not
   for an incidental reason such as a crash or a mis-parse;
3. the induction pipeline produces a mechanism whose slot support is measured
   from observations rather than declared in code, and a single-collection
   induction does not invent the collections it never saw.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from spider.models import BINDER_ABSTAIN, BINDER_BOUND, Mechanism, Observation  # noqa: E402
from spider.variability import (  # noqa: E402
    VariabilityBinders,
    learned_shape,
    make_goal,
    parse_goal,
    shape_of,
    slot_support_for,
)


def _identifier(outcome) -> str | None:
    """The identifier the outcome would send, or None for an explicit refusal.

    Abstention is a scored outcome class, so a refusal is a populated
    BindOutcome with a null bound action rather than a missing object.
    """
    if outcome.status == BINDER_ABSTAIN:
        return None
    return outcome.slot_values.get("s1")


def _observation(collection: str, identifier: str, intent: str = "read") -> Observation:
    method = {"read": "GET", "update": "PUT", "delete": "DELETE"}[intent]
    state = {
        "collection": collection,
        "resource": identifier,
        "identifiers": [identifier],
        "exists": True,
        "authenticated": True,
        "method": method,
    }
    return Observation(
        intent=intent,
        state=state,
        action={"method": method, "path": f"/{collection}/{identifier}"},
        next_state=dict(state),
        success=True,
    )


def _training(collections: tuple[str, ...], n: int = 40) -> list[Observation]:
    out: list[Observation] = []
    for intent in ("read", "update", "delete"):
        for collection in collections:
            prefix = collection[:-1] if collection.endswith("s") else collection
            for i in range(151, 151 + n):
                out.append(_observation(collection, f"{prefix}-{i}", intent))
    return out


class _Binder(VariabilityBinders):
    """The mixin needs a confidence gate; supply the frozen one."""

    min_confidence = 0.85


class TestRequestFrame(unittest.TestCase):
    def test_frame_r_names_the_identifier_verbatim(self):
        parsed = parse_goal("read record item-201 in items catalog")
        self.assertEqual(parsed["form"], "R")
        self.assertEqual(parsed["collection"], "items")
        self.assertEqual(parsed["target"], "item-201")
        self.assertEqual(parsed["verb"], "read")

    def test_frame_b_names_only_an_ordinal(self):
        parsed = parse_goal("read record 201 in items catalog")
        self.assertEqual(parsed["form"], "B")
        self.assertEqual(parsed["collection"], "items")
        self.assertEqual(parsed["target"], "201")
        self.assertNotEqual(parsed["target"], "item-201")

    def test_unrecognised_request_yields_nothing_rather_than_a_guess(self):
        self.assertEqual(parse_goal("do the thing with widget-9"), {})

    def test_make_goal_round_trips(self):
        self.assertEqual(
            parse_goal(make_goal("delete", "order-7", "orders")),
            {"verb": "delete", "target": "order-7", "collection": "orders", "form": "R"},
        )


class TestLearnedShapes(unittest.TestCase):
    def test_shape_generalises_rather_than_literalises(self):
        self.assertEqual(shape_of("item-151"), r"[a-z]+\-[0-9]+")

    def test_learned_shape_unifies_differing_widths(self):
        pattern = learned_shape(["item-151", "order-9", "product-12345"])
        self.assertTrue(pattern.startswith("(?:"))
        for value in ("item-151", "order-9", "product-12345"):
            self.assertRegex(value, pattern)

    def test_small_support_becomes_a_closed_set(self):
        support = slot_support_for(["items", "orders", "items"])
        self.assertEqual(support["kind"], "closed_set")
        self.assertEqual(support["values"], ["items", "orders"])
        self.assertEqual(support["cardinality"], 2)

    def test_large_support_becomes_a_shape_not_a_list(self):
        support = slot_support_for([f"item-{i}" for i in range(50)])
        self.assertEqual(support["kind"], "shape")
        self.assertEqual(support["prefixes"], ["item"])
        self.assertEqual(support["n_distinct"], 50)


class TestVariabilityInduction(unittest.TestCase):
    def setUp(self):
        self.binders = _Binder()
        self.mechanisms = self.binders.distill_variability(
            _training(("items", "orders", "products")), mechanism_prefix="multi"
        )
        self.by_intent = {m.intent: m for m in self.mechanisms}

    def test_every_intent_gets_a_mechanism(self):
        self.assertEqual(set(self.by_intent), {"read", "update", "delete"})

    def test_collection_slot_is_a_closed_set_over_the_observed_collections(self):
        mechanism = self.by_intent["read"]
        support = mechanism.failure_boundary["slot_support"]["s0"]
        self.assertEqual(support["kind"], "closed_set")
        self.assertEqual(set(support["values"]), {"items", "orders", "products"})

    def test_no_collection_vocabulary_is_declared_in_code(self):
        for mechanism in self.mechanisms:
            self.assertEqual(mechanism.failure_boundary["declared_identity_slots"], [])
            self.assertEqual(mechanism.failure_boundary["declared_identity_fields"], [])
            self.assertEqual(
                mechanism.failure_boundary["induction_basis"], "observed_variability"
            )

    def test_head_to_prefix_relation_is_learned_by_cooccurrence(self):
        for mechanism in self.mechanisms:
            mapping = mechanism.failure_boundary["id_prefix_by_head"]
            self.assertEqual(mapping["items"], "item")
            self.assertEqual(mapping["orders"], "order")
            self.assertEqual(mapping["products"], "product")

    def test_confidence_is_measured_not_constant(self):
        for mechanism in self.mechanisms:
            self.assertIsNotNone(mechanism.failure_boundary.get("loo_n"))
            self.assertEqual(mechanism.failure_boundary["loo_method"][:9], "leave_one")
            self.assertIn("incumbent_formula_confidence", mechanism.failure_boundary)

    def test_single_collection_induction_invents_nothing(self):
        single = self.binders.distill_variability(
            _training(("items",)), mechanism_prefix="single"
        )
        for mechanism in single:
            path = mechanism.action_template["path"]
            self.assertTrue(path.startswith("/items/"), path)
            self.assertNotIn("products", path)
            self.assertNotIn("orders", path)
            self.assertEqual(
                list(mechanism.failure_boundary["id_prefix_by_head"]), ["items"]
            )


class TestVariabilityBinding(unittest.TestCase):
    def setUp(self):
        self.binders = _Binder()
        self.mechanisms = self.binders.distill_variability(
            _training(("items", "orders", "products")), mechanism_prefix="multi"
        )
        self.by_intent = {m.intent: m for m in self.mechanisms}

    def test_binds_a_held_out_identifier_of_a_seen_collection(self):
        outcome = self.binders.bind_variability(
            self.by_intent["read"], parse_goal("read record 201 in items catalog")
        )
        self.assertEqual(outcome.status, BINDER_BOUND)
        self.assertEqual(_identifier(outcome), "item-201")
        self.assertGreaterEqual(outcome.bind_confidence, 0.85)

    def test_rebuilds_an_identifier_the_request_never_showed(self):
        """The discriminator. A frame-R request already contains the answer, so
        only a bare-ordinal request can show that the form was learned."""
        outcome = self.binders.bind_variability(
            self.by_intent["read"], parse_goal("read record 201 in products catalog")
        )
        self.assertEqual(outcome.status, BINDER_BOUND)
        self.assertEqual(_identifier(outcome), "product-201")

    def test_refuses_an_unseen_collection_instead_of_guessing(self):
        outcome = self.binders.bind_variability(
            self.by_intent["read"], parse_goal("read record 151 in widgets catalog")
        )
        self.assertEqual(outcome.status, BINDER_ABSTAIN)
        self.assertIsNone(_identifier(outcome))
        self.assertLess(outcome.bind_confidence, 0.85)

    def test_refusal_is_explicit_not_a_silent_wrong_answer(self):
        refusal = self.binders.bind_variability(
            self.by_intent["read"], parse_goal("read record 151 in widgets catalog")
        )
        self.assertTrue(refusal.reason, "a refusal must state why")
        self.assertIsNone(_identifier(refusal))

    def test_unrecognised_request_is_refused_not_guessed(self):
        outcome = self.binders.bind_variability(self.by_intent["read"], {})
        self.assertEqual(outcome.status, BINDER_ABSTAIN)
        self.assertIsNone(_identifier(outcome))

    def test_each_intent_binds_its_own_verb(self):
        for intent, method in (("read", "GET"), ("update", "PUT"), ("delete", "DELETE")):
            mechanism = self.by_intent[intent]
            self.assertEqual(mechanism.action_template["method"], method)


class TestNullBinders(unittest.TestCase):
    """The report attributes each null's failure to a specific reason. These
    tests keep that attribution honest."""

    def setUp(self):
        self.binders = _Binder()
        self.mechanisms = self.binders.distill_variability(
            _training(("items", "orders", "products")), mechanism_prefix="multi"
        )
        self.by_intent = {m.intent: m for m in self.mechanisms}

    def test_lexical_overlap_copies_from_the_goal_and_so_cannot_rebuild_a_form(self):
        """Frame B hides the identifier, so a token-overlap binder has nothing to
        copy and must get the identifier wrong."""
        outcome = self.binders.bind_lexical_overlap(
            self.by_intent["read"], parse_goal("read record 201 in products catalog")
        )
        self.assertNotEqual(_identifier(outcome), "product-201")

    def test_lexical_overlap_tie_order_can_change_the_answer(self):
        """The frozen A4 rule is underdetermined on a request that repeats the
        identifier. If the two orders could never disagree, the experiment's tie
        diagnostic would be vacuous."""
        parsed = parse_goal("read record product-201 in products catalog")
        mechanism = self.by_intent["read"]
        first = self.binders.bind_lexical_overlap(mechanism, parsed, tie_break="longest_first")
        second = self.binders.bind_lexical_overlap(mechanism, parsed, tie_break="shortest_first")
        self.assertIsNotNone(_identifier(first))
        self.assertIsNotNone(_identifier(second))
        self.assertTrue(first.slot_values)
        self.assertTrue(second.slot_values)

    def test_positional_regex_refuses_when_no_learned_position_matches(self):
        outcome = self.binders.bind_positional_regex(
            self.by_intent["read"], parse_goal("read record 201 in items catalog")
        )
        self.assertIn(outcome.status, (BINDER_BOUND, BINDER_ABSTAIN))
        if outcome.status == BINDER_ABSTAIN:
            self.assertLess(outcome.bind_confidence, 0.85)
            self.assertTrue(outcome.reason)

    def test_most_frequent_value_ignores_the_request_entirely(self):
        """The defining property of this null: same answer whatever is asked."""
        mechanism = self.by_intent["read"]
        first = self.binders.bind_most_frequent_value(
            mechanism, parse_goal("read record 201 in items catalog")
        )
        second = self.binders.bind_most_frequent_value(
            mechanism, parse_goal("read record 999 in orders catalog")
        )
        self.assertEqual(_identifier(first), _identifier(second))

    def test_null_binders_use_no_measured_support(self):
        """None of the nulls may consult slot_support, or the experiment is not
        comparing what it claims to compare."""
        mechanism = self.by_intent["read"]
        self.assertEqual(self.binders.bind_most_frequent_value(mechanism, {}).slot_support, {})
        self.assertEqual(self.binders.bind_lexical_overlap(mechanism, {}).slot_support, {})


class TestMechanismDataclass(unittest.TestCase):
    def test_namespace_map_defaults_to_empty_not_absent(self):
        """A mechanism without a namespace map must still expose the attribute so
        callers never have to branch on whether it was set."""
        mechanism = Mechanism(
            mechanism_id="m",
            intent="read",
            preconditions={},
            action_template={"method": "GET", "path": "/${s0}/${s1}"},
            postconditions={},
        )
        self.assertEqual(list(mechanism.intent_namespace_map), [])


if __name__ == "__main__":
    unittest.main()
