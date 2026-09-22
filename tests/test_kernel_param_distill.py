"""Unit tests for the frozen EXP-PRODUCT-35793576245 SUT surface:

* SpiderKernel.distill_parameterized: family-specific slot induction (Jaccard>=0.75 structure
  similarity, constant anchors, field-path relevance) — never a generic ['path','store'].
* Runtime evidence-derived confidence (softmax temp 0.15 + seeded jitter), UNKNOWN < 0.80.
* Freshness gating (>= 0.25) and required-slot gating.
* Deterministic confidence for identical (mechanism, params) pairs.
"""

import tempfile
import unittest
from pathlib import Path

from spider import Mechanism, Observation, SpiderKernel, ResolutionStatus
from spider.registry import MechanismRegistry

INTENT = "shopping_checkout"
FAMILY = "family_00"


def step_action(step_index: int, sku: str):
    if step_index == 0:
        return {"method": "GET", "url": "https://shop00.example.com/", "headers": {"auth": "Bearer tok_00"}, "body": {}}
    if step_index == 1:
        return {"method": "GET", "url": "https://shop00.example.com/catalog", "headers": {}, "body": {"sku": sku}}
    return {"method": "POST", "url": "https://shop00.example.com/checkout", "headers": {"auth": "Bearer tok_00"}, "body": {"cart": "cart_00", "done": "true"}}


def demo_observation(step_index: int, sku: str, success: bool = True):
    return Observation(
        intent=INTENT,
        state={"family": FAMILY, "authenticated": True, "step_index": step_index},
        action=step_action(step_index, sku),
        next_state={"status": 200, "done": True},
        success=success,
        provenance={"family": FAMILY, "demo": int(sku[-1]), "step": step_index},
    )


def five_demos():
    obs = []
    for d in range(5):
        for i in range(3):
            obs.append(demo_observation(i, f"A-SKU-00-{d}"))
    return obs


class ParamDistillTests(unittest.TestCase):
    def make_kernel(self):
        td = tempfile.TemporaryDirectory()
        reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
        return td, reg, SpiderKernel(reg)

    def test_distills_family_specific_slots_not_generic(self):
        td, reg, kernel = self.make_kernel()
        try:
            m = kernel.distill_parameterized(five_demos(), INTENT, FAMILY)
            self.assertIsNotNone(m)
            self.assertEqual(m.parameter_slots, ["sku"])
            self.assertNotEqual(m.parameter_slots, ["path", "store"])
            self.assertEqual(m.action_template["steps"][1]["body"], {"sku": "${sku}"})
            # constant anchors preserved
            self.assertEqual(m.action_template["steps"][0]["url"], "https://shop00.example.com/")
            self.assertEqual(m.action_template["steps"][0]["headers"], {"auth": "Bearer tok_00"})
            self.assertEqual(m.action_template["steps"][2]["body"]["done"], "true")
            self.assertEqual(m.evidence_values["sku"], [f"A-SKU-00-{d}" for d in range(5)])
            self.assertGreaterEqual(m.verification_rule["induction"]["pairwise_structure_jaccard"], 0.75)
        finally:
            td.cleanup()

    def test_resolve_binds_seen_params_and_abstains_on_novel(self):
        td, reg, kernel = self.make_kernel()
        try:
            m = kernel.distill_parameterized(five_demos(), INTENT, FAMILY)
            reg.upsert(m)
            r = kernel.resolve(INTENT, {"family": FAMILY, "authenticated": True}, {"sku": "A-SKU-00-3"})
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action["steps"][1]["body"]["sku"], "A-SKU-00-3")
            self.assertGreaterEqual(r.confidence, 0.8)
            novel = kernel.resolve(INTENT, {"family": FAMILY, "authenticated": True}, {"sku": "B-SKU-00-0"})
            self.assertEqual(novel.status, ResolutionStatus.UNKNOWN)
            self.assertLess(novel.confidence, 0.8)
        finally:
            td.cleanup()

    def test_freshness_gate_blocks_stale_mechanism(self):
        td, reg, kernel = self.make_kernel()
        try:
            m = kernel.distill_parameterized(five_demos(), INTENT, FAMILY)
            m.freshness = {"behavioral_score": 0.1, "probe_url": "file://mock/family_00"}
            reg.upsert(m)
            r = kernel.resolve(INTENT, {"family": FAMILY, "authenticated": True}, {"sku": "A-SKU-00-0"})
            self.assertEqual(r.status, ResolutionStatus.UNKNOWN)
        finally:
            td.cleanup()

    def test_missing_required_slot_is_unknown(self):
        td, reg, kernel = self.make_kernel()
        try:
            m = kernel.distill_parameterized(five_demos(), INTENT, FAMILY)
            reg.upsert(m)
            r = kernel.resolve(INTENT, {"family": FAMILY, "authenticated": True}, {})
            self.assertEqual(r.status, ResolutionStatus.UNKNOWN)
        finally:
            td.cleanup()

    def test_structure_mismatch_blocks_induction(self):
        td, reg, kernel = self.make_kernel()
        try:
            obs = five_demos()
            # Corrupt one demo step so its field-path set mismatches (structure jaccard < 0.75).
            bad = demo_observation(1, "A-SKU-00-0")
            bad = Observation(intent=INTENT, state=bad.state, action={"method": "POST", "body": {"price": "1"}}, next_state=bad.next_state, success=True, provenance=bad.provenance)
            obs[1] = bad
            m = kernel.distill_parameterized(obs, INTENT, FAMILY)
            self.assertIsNone(m)
        finally:
            td.cleanup()

    def test_confidence_deterministic_with_seeded_jitter_bounded(self):
        td, reg, kernel = self.make_kernel()
        try:
            m = kernel.distill_parameterized(five_demos(), INTENT, FAMILY)
            reg.upsert(m)
            ctx = {"family": FAMILY, "authenticated": True}
            c1 = kernel.resolve(INTENT, ctx, {"sku": "B-SKU-00-0"}).confidence
            c2 = kernel.resolve(INTENT, ctx, {"sku": "B-SKU-00-0"}).confidence
            self.assertEqual(c1, c2)
            self.assertGreaterEqual(m.evidence_values["sku"], ["A-SKU-00-0"])
            self.assertLess(abs(c1 - 0.0013), 0.06)  # near-0 consistency + [-0.05, 0.05] jitter
            seen = kernel.resolve(INTENT, ctx, {"sku": "A-SKU-00-4"}).confidence
            self.assertGreaterEqual(seen, 0.8)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()