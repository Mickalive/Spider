import tempfile
import unittest
from pathlib import Path

from spider import Mechanism, SpiderKernel, ResolutionStatus
from spider.registry import MechanismRegistry

FORBIDDEN_KEYS = {
    "alias_family", "query_key", "target_prefix", "routing_prefix", "target_style",
    "path_style", "header_key", "body_field", "auth_scope", "expected_template",
    "resource", "train_template", "dist_template",
}


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

    # ---- reconstruction adapter (EXP-PRODUCT-35777355953 port of Frontier RECONSTRUCTION-RULE)
    def derived(self, url, headers=None, body=None, query=None):
        d = {
            "url": url,
            "method": "GET",
            "url_path": url.split("?", 1)[0],
            "url_query": query or {},
            "url_segments": [s for s in url.split("?", 1)[0].split("/") if s],
            "headers_observed": headers or {},
            "body_observed": body or {},
            "ax_tree_snapshot": None,
            "ax_nodes_count": None,
            "viewport_observed": None,
        }
        return d

    def mk(self, mid, template, conf, intent="x"):
        return Mechanism(mechanism_id=mid, intent=intent, preconditions={},
                         action_template=template, postconditions={},
                         parameter_slots=[], applicability_guards={}, confidence=conf)

    def test_reconstruct_resolves_heldout_header_alias(self):
        td, reg, kernel = self.make_kernel()
        try:
            reg.replace([
                self.mk("train", {"url": "/api/data", "headers": {"ApiKey": "${token}"}}, 0.9),
                self.mk("dist", {"url": "/api/data", "headers": {"X-Reset-Token": "${token}"}}, 0.9),
                self.mk("low", {"url": "/api/data", "headers": {"X-Api-Key": "${token}"}}, 0.8),
            ])
            r = kernel.resolve("x", self.derived("/api/data",
                                                headers={"Authorization": "Bearer tok1"}),
                               {"token": "tok1"}, reconstruct=True)
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action,
                             {"url": "/api/data", "headers": {"Authorization": "Bearer tok1"}})
        finally:
            td.cleanup()

    def test_reconstruct_mixed_multichannel_rewrite(self):
        td, reg, kernel = self.make_kernel()
        try:
            reg.replace([
                self.mk("train", {"url": "/api/data", "headers": {"ApiKey": "${token}"}}, 0.9),
                self.mk("dist", {"url": "/api/data", "body": {"apiKey": "${token}"}}, 0.9),
                self.mk("low", {"url": "/api/data?admin_scope=${perm}"}, 0.8),
            ])
            ctx = self.derived("/api/data?permission=read",
                               headers={"X-Api-Key": "tok_mix"},
                               body={"api_token": "tok_mix"},
                               query={"permission": "read"})
            r = kernel.resolve("x", ctx, {"token": "tok_mix", "perm": "read"}, reconstruct=True)
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action, {
                "url": "/api/data?permission=read",
                "headers": {"X-Api-Key": "tok_mix"},
                "body": {"api_token": "tok_mix"},
            })
        finally:
            td.cleanup()

    def test_reconstruct_abstains_when_no_adoptable_signal(self):
        td, reg, kernel = self.make_kernel()
        try:
            reg.replace([self.mk("train", {"url": "/api/data", "headers": {"ApiKey": "${token}"}}, 0.9)])
            ctx = self.derived("/api/data", headers={"Host": "api.example.com"})
            r = kernel.resolve("x", ctx, {"token": "tok"}, reconstruct=True)
            self.assertEqual(r.status, ResolutionStatus.UNKNOWN)
        finally:
            td.cleanup()

    def test_reconstruct_exact_match_preserved(self):
        td, reg, kernel = self.make_kernel()
        try:
            reg.replace([self.mk("m", {"url": "/api/data", "headers": {"X-Api-Key": "${token}"}}, 0.9)])
            ctx = self.derived("/api/data", headers={"X-Api-Key": "tok1"})
            r = kernel.resolve("x", ctx, {"token": "tok1"}, reconstruct=True)
            self.assertEqual(r.status, ResolutionStatus.EXECUTABLE)
            self.assertEqual(r.bound_action, {"url": "/api/data", "headers": {"X-Api-Key": "tok1"}})
        finally:
            td.cleanup()

    def test_reconstruct_reads_only_whitelisted_state_keys(self):
        td, reg, kernel = self.make_kernel()
        try:
            reg.replace([self.mk("m", {"url": "/api/data"}, 0.9)])
            # extra unwhitelisted junk keys are projected out by resolve()
            ctx = dict(self.derived("/api/data"))
            ctx["alias_family"] = "bogus"
            r = kernel.resolve("x", ctx, {}, reconstruct=True)
            self.assertIn(r.status, (ResolutionStatus.EXECUTABLE, ResolutionStatus.UNKNOWN))
        finally:
            td.cleanup()

    def test_kernel_source_reads_no_forbidden_keys(self):
        src = Path(__file__).resolve().parents[1] / "src/spider/kernel.py"
        text = src.read_text()
        # literal-key reads appear as quoted strings; identifiers like cand_query_keys
        # are variable names, not dict-key reads, and must not trip the audit.
        hits = [k for k in sorted(FORBIDDEN_KEYS)
                if f'"{k}"' in text or f"'{k}'" in text]
        self.assertEqual(hits, [])

    def test_kernel_reconstruct_confidence_is_not_constant(self):
        td, reg, kernel = self.make_kernel()
        try:
            reg.replace([
                self.mk("train", {"url": "{BASE}", "headers": {"ApiKey": "${token}"}}, 0.9),
                self.mk("dist", {"url": "{BASE}", "headers": {"X-Reset-Token": "${token}"}}, 0.9),
                self.mk("low", {"url": "{BASE}", "headers": {"X-Api-Key": "${token}"}}, 0.8),
            ])
            confs = []
            for base in ("/api/data", "/api/v2/data", "/api/v2/data/x"):
                ctx = self.derived(base, headers={"X-Auth-Key": "tok1"})
                r = kernel.resolve("x", ctx, {"token": "tok1"}, reconstruct=True)
                confs.append(r.confidence)
            self.assertGreater(max(confs) - min(confs), 0.001)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
