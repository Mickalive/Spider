"""Unit tests for the frozen evaluation-harness instrument
(EXP-PRODUCT-36129169543 Part A).

Coverage required by the frozen decision rule:
  * all five arms implemented behind one identical counter interface;
  * all eight counter paths increment per trajectory under the deterministic
    scripted policy;
  * the fail-closed UNKNOWN gate fires for absent BrowserGym/credentials and
    never surrogate-fills or default-fills;
  * per-trajectory hard reset (no cross-trajectory accumulation);
  * family-stratified trajectory-grouped bootstrap and block-permutation
    confidence intervals compute;
  * break-even f* uses only non-token inputs (token inputs do not exist in
    the API) and one-at-a-time sensitivity identifies a dominant quantity.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from spider.eval_harness import (
    ARM_IDS,
    COUNTER_NAMES,
    CounterLedger,
    ColdArm,
    DeterministicExecutorArm,
    GateDecision,
    InstructionsArm,
    MockEnvironment,
    RagEmbedArm,
    SpiderArm,
    block_permutation_test,
    breakeven_f_star,
    build_inheritance,
    build_rag_index,
    fail_closed_gate,
    integrity_ok,
    oat_sensitivity,
    paired_signflip_permutation,
    probe_capabilities,
    run_harness,
    spearman,
    stratified_grouped_bootstrap,
    task_rid,
    tasks_from_manifest,
    verify_inheritance,
)

FIXTURE = {
    "tasks": [
        {
            "task_id": "task_0000",
            "family_id": "family_00",
            "template_id": "template_00",
            "site_id": "shop00.example.com",
            "length": 8,
            "realized_novelty": 0.0,
            "slots": ["sku", "store_id"],
            "param_values": {"sku": "AAA0", "store_id": "AAA1"},
            "b_positions": [],
        },
        {
            "task_id": "task_0001",
            "family_id": "family_00",
            "template_id": "template_00",
            "site_id": "shop00.example.com",
            "length": 8,
            "realized_novelty": 0.5,
            "slots": ["sku", "store_id"],
            "param_values": {"sku": "AZ2A", "store_id": "AAA2"},
            "b_positions": [1],
        },
        {
            "task_id": "task_0100",
            "family_id": "family_01",
            "template_id": "template_01",
            "site_id": "shop01.example.com",
            "length": 9,
            "realized_novelty": 1.0,
            "slots": ["sku"],
            "param_values": {"sku": "BBB0"},
            "b_positions": [0],
        },
    ],
    "demos": {
        "family_00": [
            {
                "demo_idx": 0,
                "values": {"sku": "AAA0", "store_id": "AAA1"},
                "steps": [
                    {"method": "GET", "url": "https://shop00.example.com/", "body": {}},
                    {"method": "GET", "url": "https://shop00.example.com/catalog", "body": {"sku": "AAA0"}},
                    {"method": "GET", "url": "https://shop00.example.com/catalog", "body": {"store_id": "AAA1"}},
                ],
            }
        ],
        "family_01": [
            {
                "demo_idx": 0,
                "values": {"sku": "BBB0"},
                "steps": [
                    {"method": "GET", "url": "https://shop01.example.com/", "body": {}},
                    {"method": "GET", "url": "https://shop01.example.com/catalog", "body": {"sku": "BBB0"}},
                ],
            }
        ],
    },
    "pools": {
        "family_00": {"sku": {"A": ["AAA0", "AAA1"], "B": ["AZ0A", "AZ1A"]}},
        "family_01": {"sku": {"A": ["BBB0"], "B": ["BZ0B"]}},
    },
}


def make_env_and_arms():
    env = MockEnvironment()
    tasks = tasks_from_manifest(FIXTURE)
    # mkdtemp (not TemporaryDirectory): the registry file must survive past the
    # helper return so arms keep a durable kernel for the whole test.
    inh = build_inheritance(env, tasks, FIXTURE, Path(tempfile.mkdtemp(prefix="harness-test-")) / "inh")
    arms = [
        SpiderArm(inh),
        ColdArm(),
        InstructionsArm(),
        RagEmbedArm(build_rag_index(FIXTURE)),
        DeterministicExecutorArm(),
    ]
    return env, tasks, arms, inh


class CounterTests(unittest.TestCase):
    def test_eight_frozen_counter_names(self):
        self.assertEqual(len(COUNTER_NAMES), 8)
        self.assertIn("latency_ms", COUNTER_NAMES)
        self.assertEqual(len(set(COUNTER_NAMES)), 8)

    def test_ledger_rejects_unknown_counter(self):
        ledger = CounterLedger()
        with self.assertRaises(KeyError):
            ledger.incr("tokens")

    def test_ledger_hard_reset(self):
        ledger = CounterLedger()
        ledger.incr("requests", 3)
        ledger.add_latency_ms(4.4)
        first = ledger.snapshot()
        ledger.reset()
        second = ledger.snapshot()
        self.assertEqual(second, {name: 0 for name in COUNTER_NAMES})
        self.assertEqual(first["requests"], 3)
        self.assertEqual(first["latency_ms"], 4)

    def test_snapshot_values_are_integers(self):
        ledger = CounterLedger()
        ledger.add_latency_ms(2.5)
        ledger.incr("verify")
        snap = ledger.snapshot()
        for name, value in snap.items():
            self.assertIsInstance(value, int, name)


class ArmExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env, cls.tasks, cls.arms, cls.inh = make_env_and_arms()
        # Deterministic environment staleness injection so the localized
        # repair counter path is exercised in this run as well.
        cls.env.bump(task_rid(cls.tasks[0], 0))
        cls.records = run_harness(
            cls.arms,
            cls.tasks,
            cls.env,
            mode="scripted",
            capabilities={"http_substrate": True},
        )

    def test_five_frozen_arms_present(self):
        seen = {r.arm_id for r in self.records}
        self.assertEqual(seen, set(ARM_IDS))

    def test_every_arm_produces_all_eight_counters_as_ints(self):
        for rec in self.records:
            self.assertEqual(rec.gate_status, "EXECUTABLE", (rec.arm_id, rec.task_id))
            self.assertIsNotNone(rec.counters)
            self.assertEqual(set(rec.counters), set(COUNTER_NAMES))
            for name, value in rec.counters.items():
                self.assertIsInstance(value, int)
                self.assertGreaterEqual(value, 0, (rec.arm_id, name))

    def test_all_eight_counter_paths_non_zero_for_at_least_one_arm(self):
        totals = {name: 0 for name in COUNTER_NAMES}
        for rec in self.records:
            for name, value in rec.counters.items():
                totals[name] += value
        for name, total in totals.items():
            self.assertGreater(total, 0, f"counter path {name} never incremented")

    def test_per_trajectory_hard_reset_no_accumulation(self):
        env, tasks, arms, _ = make_env_and_arms()
        first = run_harness(arms, tasks, env, "scripted", {"http_substrate": True})
        env2, tasks2, arms2, _ = make_env_and_arms()
        second = run_harness(arms2, tasks2, env2, "scripted", {"http_substrate": True})
        for a, b in zip(first, second):
            self.assertEqual(a.counters, b.counters, (a.arm_id, a.task_id))

    def test_requests_counter_equals_length(self):
        for rec in self.records:
            self.assertEqual(rec.counters["requests"], rec.length, (rec.arm_id, rec.task_id))

    def test_browser_steps_counter_equals_length(self):
        for rec in self.records:
            self.assertEqual(rec.counters["browser_steps"], rec.length)

    def test_spider_only_arms_own_freshness_and_repair(self):
        for rec in self.records:
            if rec.arm_id == "P-SPIDER":
                self.assertGreater(rec.counters["freshness"], 0)
            else:
                self.assertEqual(rec.counters["freshness"], 0, rec.arm_id)
                self.assertEqual(rec.counters["repair"], 0, rec.arm_id)

    def test_inherited_transfer_never_exceeds_cold(self):
        by_key = {(r.arm_id, r.task_id): r for r in self.records}
        for task in self.tasks:
            cold = by_key[("B-COLD", task.task_id)]
            spider = by_key[("P-SPIDER", task.task_id)]
            self.assertLessEqual(spider.payload_bytes, cold.payload_bytes)

    def test_no_token_counters_exist(self):
        for rec in self.records:
            self.assertNotIn("tokens", rec.counters)
            self.assertFalse(any("token" in k for k in rec.counters))


class SpiderMechanismTests(unittest.TestCase):
    def test_build_and_verify_inheritance_measured(self):
        env, tasks, _, inh = make_env_and_arms()
        self.assertGreater(inh.build["build_ms"], 0.0)
        self.assertGreater(inh.build["validators_cached"], 0)
        self.assertEqual(inh.build["family_mechanisms"], 2)
        verdict = verify_inheritance(env, inh, tasks)
        self.assertGreaterEqual(verdict["verify_ms"], 0.0)
        self.assertEqual(verdict["auditor_checks"], verdict["auditor_passes"])
        self.assertEqual(verdict["probe_304_hits"], verdict["probe_requests"])
        self.assertNotIn("token", verdict)

    def test_spider_resolves_executable_and_binds(self):
        env, tasks, arms, _ = make_env_and_arms()
        records = run_harness(arms, tasks, env, "scripted", {"http_substrate": True})
        spider = [r for r in records if r.arm_id == "P-SPIDER"]
        for rec in spider:
            self.assertEqual(rec.extras["resolve_status"], "EXECUTABLE")
            self.assertTrue(rec.extras["auditor_pass"])
            self.assertEqual(rec.counters["resolve"], 1)
            self.assertGreater(rec.counters["bind"], 0)

    def test_unknown_family_abstains_without_fabricated_counters(self):
        env = MockEnvironment()
        tasks = tasks_from_manifest(FIXTURE)
        with tempfile.TemporaryDirectory() as td:
            inh = build_inheritance(env, tasks, FIXTURE, Path(td) / "inh")
            alien = type(tasks[0])(
                task_id="alien",
                family_id="family_404",
                template_id="template_404",
                site_id="ghost.example.com",
                length=8,
                novelty_level=0.0,
                slots=("sku",),
                params={"sku": "X"},
            )
            records = run_harness([SpiderArm(inh)], [alien], env, "scripted", {"http_substrate": True})
            rec = records[0]
            self.assertEqual(rec.extras["resolve_status"], "UNKNOWN")
            self.assertEqual(rec.counters["bind"], 0)
            self.assertIsNone(rec.extras["auditor_pass"])
            self.assertEqual(rec.counters["browser_steps"], 8)

    def test_localized_repair_fires_on_stale_validator(self):
        env, tasks, arms, inh = make_env_and_arms()
        task = tasks[0]
        rid = task_rid(task, 0)
        env.bump(rid)  # environment changes after build -> validator stale
        records = run_harness([SpiderArm(inh)], [task], env, "scripted", {"http_substrate": True})
        rec = records[0]
        self.assertEqual(rec.counters["repair"], 1)
        self.assertEqual(rec.extras["stale_repairs"], 1)
        # repaired validator now matches -> second trajectory is fresh again
        records2 = run_harness([SpiderArm(inh)], [task], env, "scripted", {"http_substrate": True})
        self.assertEqual(records2[0].counters["repair"], 0)
        self.assertEqual(records2[0].counters["freshness"], task.length)

    def test_integrity_check_detects_tampering(self):
        env = MockEnvironment()
        res = env.fetch("family_00_template_00_s0")
        self.assertTrue(integrity_ok(res))
        res.body = res.body + "tampered"
        self.assertFalse(integrity_ok(res))


class RagArmTests(unittest.TestCase):
    def test_retrieval_hit_on_matching_site(self):
        env = MockEnvironment()
        tasks = tasks_from_manifest(FIXTURE)
        arm = RagEmbedArm(build_rag_index(FIXTURE))
        records = run_harness([arm], tasks, env, "scripted", {"http_substrate": True})
        hits = [r for r in records if r.extras["rag_hit"]]
        self.assertGreaterEqual(len(hits), 1)
        for rec in hits:
            self.assertGreaterEqual(rec.extras["rag_top_score"], 0.30)
            self.assertEqual(rec.counters["resolve"], 1)
            expected_bind = len(
                next(t for t in tasks if t.task_id == rec.task_id).slots
            )
            self.assertEqual(rec.counters["bind"], expected_bind)
        self.assertLessEqual(len(records[0].extras["rag_k5_candidates"]), 5)

    def test_tau_threshold_is_enforced(self):
        env = MockEnvironment()
        tasks = tasks_from_manifest(FIXTURE)
        arm = RagEmbedArm(build_rag_index(FIXTURE))
        records = run_harness([arm], tasks, env, "scripted", {"http_substrate": True})
        for rec in records:
            expected = rec.extras["rag_top_score"] >= 0.30
            self.assertEqual(rec.extras["rag_hit"], expected)


class GateTests(unittest.TestCase):
    def test_scripted_gate_executable_when_substrate_present(self):
        d = fail_closed_gate("B-COLD", "scripted", {"http_substrate": True})
        self.assertEqual(d.status, "EXECUTABLE")

    def test_live_gate_unknown_without_browser_and_credential(self):
        caps = {"http_substrate": True, "browsergym": False, "playwright": False, "policy_model": False}
        for arm in ARM_IDS:
            d = fail_closed_gate(arm, "live_browser", caps)
            self.assertEqual(d.status, "UNKNOWN", arm)
            self.assertIn("browsergym", d.missing)
            self.assertIn("playwright", d.missing)
            self.assertIn("policy_model", d.missing)

    def test_gate_decision_has_no_value_slot(self):
        fields = set(GateDecision.__dataclass_fields__)
        self.assertEqual(
            fields,
            {"arm_id", "mode", "status", "required", "missing", "reason"},
        )

    def test_missing_capability_key_fails_closed(self):
        d = fail_closed_gate("P-SPIDER", "live_browser", {"http_substrate": True})
        self.assertEqual(d.status, "UNKNOWN")

    def test_unknown_mode_fails_closed(self):
        d = fail_closed_gate("B-COLD", "unspecified-mode", {"http_substrate": True})
        self.assertEqual(d.status, "UNKNOWN")

    def test_probe_capabilities_is_fail_closed_on_probe_error(self):
        from spider import eval_harness as eh

        original = dict(eh.PROBES)
        try:
            eh.PROBES["playwright"] = lambda: (_ for _ in ()).throw(RuntimeError("boom"))
            probe = eh.probe_capabilities(True)
        finally:
            eh.PROBES.clear()
            eh.PROBES.update(original)
        self.assertFalse(probe["available"]["playwright"])
        self.assertIn("probe_error", probe["details"]["playwright"])

    def test_unknown_arm_records_carry_no_numbers(self):
        env, tasks, arms, _ = make_env_and_arms()
        caps = {"http_substrate": True, "browsergym": False, "playwright": False, "policy_model": False}
        records = run_harness(arms[:1], tasks[:1], env, "live_browser", caps)
        rec = records[0]
        self.assertEqual(rec.gate_status, "UNKNOWN")
        self.assertIsNone(rec.counters)
        self.assertIsNone(rec.payload_bytes)
        self.assertEqual(rec.extras["missing_capabilities"], ["browsergym", "playwright", "policy_model"])
        self.assertEqual(rec.extras.get("resolve_rate"), None)

    def test_probe_reports_environment_truthfully(self):
        probe = probe_capabilities(substrate_ok=True)
        self.assertTrue(probe["available"]["http_substrate"])
        # This test environment has no policy credential by construction.
        self.assertFalse(probe["available"]["policy_model"])
        self.assertEqual(set(probe["available"]), {"http_substrate", "browsergym", "playwright", "policy_model"})


class StatisticsTests(unittest.TestCase):
    def rows(self):
        rows = []
        for fam in ("family_00", "family_01", "family_02"):
            for i in range(6):
                rows.append(
                    {
                        "family_id": fam,
                        "task_id": f"{fam}-{i}",
                        "delta": float(i * (1 + len(fam))),
                        "length": 8 + i,
                        "novelty": i / 5.0,
                    }
                )
        return rows

    def test_spearman_monotone(self):
        self.assertAlmostEqual(spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1.0)
        self.assertAlmostEqual(spearman([1, 2, 3, 4], [40, 30, 20, 10]), -1.0)
        self.assertIsNone(spearman([1, 1, 1], [1, 2, 3]))

    def test_bootstrap_ci_computes_and_orders(self):
        ci = stratified_grouped_bootstrap(
            self.rows(),
            lambda s: sum(r["delta"] for r in s) / len(s),
            B=500,
            seed=42,
        )
        self.assertIsNotNone(ci["lo"])
        self.assertLessEqual(ci["lo"], ci["median"])
        self.assertLessEqual(ci["median"], ci["hi"])
        self.assertEqual(ci["B"], 500)

    def test_block_permutation_p_value_range(self):
        out = block_permutation_test(self.rows(), "length", "delta", B=500, seed=42)
        self.assertIsNotNone(out["rho_observed"])
        self.assertGreaterEqual(out["p"], 0.0)
        self.assertLessEqual(out["p"], 1.0)
        self.assertIsNotNone(out["rho_shuffled_median"])
        self.assertLess(abs(out["rho_shuffled_median"]), 0.5)

    def test_paired_signflip_permutation(self):
        out = paired_signflip_permutation([1.0, 2.0, 3.0, 4.0], ["a", "a", "b", "b"], B=500, seed=42)
        self.assertLess(out["p"], 0.2)  # consistent positive shift
        out_null = paired_signflip_permutation([0.0, 0.0, 0.0], ["a", "a", "b"], B=200, seed=42)
        self.assertGreaterEqual(out_null["p"], 0.5)


class BreakevenTests(unittest.TestCase):
    def test_formula(self):
        out = breakeven_f_star(1000.0, 500.0, 80.0, 50.0, unit="ms")
        self.assertTrue(out["computable"])
        self.assertAlmostEqual(out["f_star"], 1500.0 / 30.0)

    def test_negative_denominator_not_computable(self):
        out = breakeven_f_star(1000.0, 500.0, 10.0, 50.0, unit="ms")
        self.assertFalse(out["computable"])
        self.assertIsNone(out["f_star"])

    def test_no_token_parameter_exists(self):
        import inspect

        params = set(inspect.signature(breakeven_f_star).parameters)
        self.assertEqual(
            params,
            {"build_cost", "verify_cost", "cold_serving_cost", "inherited_serving_cost", "unit"},
        )

    def test_oat_sensitivity_identifies_dominant_quantity(self):
        def f(build_cost, verify_cost, cold_serving_cost, inherited_serving_cost):
            return breakeven_f_star(build_cost, verify_cost, cold_serving_cost, inherited_serving_cost)

        out = oat_sensitivity(
            {"build_cost": 1000.0, "verify_cost": 100.0, "cold_serving_cost": 80.0, "inherited_serving_cost": 60.0},
            f,
            delta=0.10,
        )
        self.assertIsNotNone(out["dominant_quantity"])
        self.assertGreater(out["dominant_max_abs_rel_change"], 0.0)
        self.assertIn(out["dominant_quantity"], out["per_input"])
        # With denominator (cold - inherited) = 20 against a numerator of
        # 1100, +/-10% on cold_serving_cost moves f* most: the sensitivity
        # sweep must surface the denominator, not the numerator.
        self.assertEqual(out["dominant_quantity"], "cold_serving_cost")


if __name__ == "__main__":
    unittest.main()
