import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from demo_public_reuse import run_github_demo
from spider.kernel import SpiderKernel
from spider.models import ResolutionStatus
from spider.public_learning import learn_public_route
from spider.public_tasks import HOLDOUT, TRAIN, PublicTask
from spider.registry import MechanismRegistry


def fake_get(url, *, fail=None):
    if url.startswith("https://api.github.com/repos/"):
        repo = url[len("https://api.github.com/repos/"):].removesuffix("/releases/latest")
        tag = "v999" if repo == fail else "v1.2.3"
        return json.dumps({"tag_name": tag}).encode(), url
    if url.startswith("https://github.com/") and url.endswith("/releases/latest"):
        repo = url[len("https://github.com/"):].removesuffix("/releases/latest")
        return b"<html>public release</html>", f"https://github.com/{repo}/releases/tag/v1.2.3"
    raise AssertionError("unexpected network address: " + url)


class ProductReuseTests(unittest.TestCase):
    def test_end_to_end_real_kernel_reuses_two_verified_unseen_tasks(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "storage.jsonl"
            report = run_github_demo(fake_get, memory_path=path)
            self.assertTrue(report["success"])
            self.assertEqual(report["calls"], {"public_pages": 4, "official_api": 4})
            self.assertEqual(report["training_examples"], 2)
            self.assertEqual(len(report["holdout"]), 2)
            self.assertEqual(len(MechanismRegistry(path).all()), 1)
            self.assertFalse(report["claims"]["llm_cost_savings_demonstrated"])
            self.assertFalse(report["claims"]["generic_web_agent_learning_demonstrated"])

    def test_training_mismatch_never_creates_learned_memory(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "storage.jsonl"
            with self.assertRaisesRegex(RuntimeError, "training observation"):
                run_github_demo(
                    lambda url: fake_get(url, fail=TRAIN["github"][0]),
                    memory_path=path,
                )
            self.assertFalse(path.exists())

    def test_unseen_holdout_verification_failure_invalidates_memory(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "storage.jsonl"
            with self.assertRaisesRegex(RuntimeError, "failed independent verification"):
                run_github_demo(
                    lambda url: fake_get(url, fail=HOLDOUT["github"][0]),
                    memory_path=path,
                )
            all_mechanisms = MechanismRegistry(path).all()
            self.assertEqual(len(all_mechanisms), 1)
            self.assertTrue(all_mechanisms[0].invalidated)
            self.assertEqual(
                SpiderKernel(MechanismRegistry(path)).resolve(
                    "latest-github",
                    {"family": "github", "surface": "allowlisted-public-v1", "read_only": True},
                    {"id": HOLDOUT["github"][1]},
                ).status,
                ResolutionStatus.UNKNOWN,
            )

    def test_unverified_or_unseen_learning_is_rejected(self):
        examples = [{
            "identifier": name,
            "answer": "v1.2.3",
            "visited_urls": [PublicTask("github", name).target_url],
            "verified_against_independent_oracle": True,
        } for name in TRAIN["github"]]
        bad = [dict(ex) for ex in examples]
        bad[0]["verified_against_independent_oracle"] = False
        with self.assertRaises(ValueError):
            learn_public_route("github", bad)
        bad = [dict(ex) for ex in examples]
        bad[1]["identifier"] = bad[0]["identifier"]
        with self.assertRaises(ValueError):
            learn_public_route("github", bad)


if __name__ == "__main__":
    unittest.main()
