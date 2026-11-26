import tempfile
import unittest
from pathlib import Path

from spider.agent_bridge import AgentBridge
from spider import Mechanism, SpiderKernel
from spider.registry import MechanismRegistry


class AgentBridgeTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.registry = MechanismRegistry(Path(self.td.name) / "mechanisms.jsonl")
        self.bridge = AgentBridge(SpiderKernel(self.registry))
        self.fallback_calls = 0
        self.executions = 0

    def tearDown(self):
        self.td.cleanup()

    def fallback(self):
        self.fallback_calls += 1
        return "agent-result"

    def execute(self, action):
        self.executions += 1
        return action["path"]

    def add_mechanism(self, **kwargs):
        defaults = dict(mechanism_id="known", intent="read-invoice",
                        preconditions={"authenticated": True},
                        action_template={"method": "GET", "path": "/invoice/${id}"},
                        postconditions={"invoice_loaded": True}, parameter_slots=["id"],
                        confidence=0.95, verification_rule={"replay_safe": True})
        defaults.update(kwargs)
        self.registry.upsert(Mechanism(**defaults))

    def run_bridge(self, **kwargs):
        defaults = dict(intent="read-invoice", context={"authenticated": True},
                        params={"id": "B"}, fallback=self.fallback, execute=self.execute,
                        read_state=lambda: {"invoice_loaded": True},
                        authorize=lambda action: action.get("method") == "GET")
        defaults.update(kwargs)
        return self.bridge.run(**defaults)

    def test_unknown_delegates_to_agent(self):
        result = self.run_bridge()
        self.assertEqual((result.path, result.value), ("agent", "agent-result"))
        self.assertEqual((self.fallback_calls, self.executions), (1, 0))

    def test_verified_parameterized_reuse(self):
        self.add_mechanism()
        result = self.run_bridge()
        self.assertEqual((result.path, result.value), ("inheritance", "/invoice/B"))
        self.assertEqual((self.fallback_calls, self.executions), (0, 1))

    def test_scope_or_freshness_mismatch_delegates(self):
        self.add_mechanism(auth_scope="tenant-A")
        self.assertEqual(self.run_bridge().path, "agent")
        self.add_mechanism(auth_scope=None, freshness={"ttl_seconds": 5})
        self.assertEqual(self.run_bridge().path, "agent")
        self.assertEqual(self.executions, 0)

    def test_non_replay_safe_delegates(self):
        self.add_mechanism(verification_rule={})
        self.assertEqual(self.run_bridge().path, "agent")
        self.assertEqual(self.executions, 0)

    def test_denied_execution_never_falls_back(self):
        self.add_mechanism()
        result = self.run_bridge(authorize=lambda _: False)
        self.assertEqual(result.path, "unknown")
        self.assertEqual((self.fallback_calls, self.executions), (0, 0))

    def test_ambiguous_execution_never_retries(self):
        self.add_mechanism()
        result = self.run_bridge(read_state=lambda: {"invoice_loaded": False})
        self.assertEqual(result.path, "unknown")
        self.assertEqual((self.fallback_calls, self.executions), (0, 1))


if __name__ == "__main__":
    unittest.main()
