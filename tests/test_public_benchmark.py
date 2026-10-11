import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from spider.public_learning import learn_public_route
from spider.public_tasks import PublicTask, TRAIN, HOLDOUT, allowlisted_tasks, parse_page
from spider.registry import MechanismRegistry
from spider.kernel import SpiderKernel

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_public_benchmark import ARMS, STAGEHAND_ARM, plan, trial, confirmed_family_ready


def examples(family):
    out = []
    for name in TRAIN[family]:
        task = PublicTask(family, name)
        url = task.target_url if family == "pypi" else (
            f"https://github.com/{name}/releases/tag/v1.2.3"
        )
        out.append({"identifier": name, "answer": "v1.2.3",
                    "visited_urls": [url],
                    "verified_against_independent_oracle": True})
    return out


class PublicSiteTests(unittest.TestCase):
    def test_readiness_is_family_scoped_and_expires(self):
        import json
        import tempfile
        from datetime import datetime, timedelta, timezone
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "probe.json"
            report = {
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "family_ready": {"github": True, "pypi": False},
            }
            path.write_text(json.dumps(report))
            self.assertTrue(confirmed_family_ready(path, "github"))
            self.assertFalse(confirmed_family_ready(path, "pypi"))
            report["checked_at"] = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
            path.write_text(json.dumps(report))
            self.assertFalse(confirmed_family_ready(path, "github"))

    def test_holdout_and_plan_are_reproducible(self):
        self.assertEqual(plan(8, 2), plan(8, 2))
        self.assertEqual(len(plan(8, 2)), 48)
        self.assertEqual(len(plan(8, 1, True)), 28)
        self.assertTrue(all(set(TRAIN[family]).isdisjoint(HOLDOUT[family]) for family in TRAIN))
        with self.assertRaises(ValueError):
            PublicTask("pypi", "not-in-benchmark")
        with self.assertRaises(ValueError):
            PublicTask("github", "../../etc")

    def test_pypi_html_header_extract(self):
        task = PublicTask("pypi", "httpx")
        body = b'<html><h1 class="package-header__name">httpx 0.28.1</h1></html>'
        self.assertEqual(parse_page(task, body, task.target_url), "0.28.1")
        modern = b'<section><h2>Release files for <span>httpx</span> 0.28.1</h2></section>'
        self.assertEqual(parse_page(task, modern, task.target_url), "0.28.1")
        self.assertIsNone(parse_page(task, body, "http://pypi.org/project/httpx/"))
        self.assertIsNone(parse_page(task, body, "https://pypi.org/project/pytest/"))

    def test_github_redirect_latest_release_extract(self):
        task = PublicTask("github", "astral-sh/ruff")
        self.assertEqual(parse_page(task, b"", task.target_url.replace(
            "/latest", "/tag/0.14.0")), "0.14.0")
        self.assertIsNone(parse_page(task, b"", "https://evil.org/astral-sh/ruff/releases/tag/0.14.0"))
        self.assertIsNone(parse_page(task, b"", "https://github.com/astral-sh/ruff/releases/tag/0.14.0?secret=1"))

    def test_independent_verified_two_record_learning_and_reuse(self):
        import tempfile
        from spider.public_tasks import PublicTask
        for family in TRAIN:
            mechanism = learn_public_route(family, examples(family))
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "mem.jsonl"
                MechanismRegistry(path).upsert(mechanism)
                task = allowlisted_tasks()[0] if family == "pypi" else allowlisted_tasks()[-1]
                resolved = SpiderKernel(MechanismRegistry(path)).resolve(
                    "latest-" + family,
                    {"family": family, "surface": "allowlisted-public-v1", "read_only": True},
                    {"id": task.identifier},
                )
                self.assertEqual(resolved.bound_action["url"], task.target_url)
                val = "0.28.1" if family == "pypi" else "v2.0"
                url = task.target_url if family == "pypi" else task.target_url.replace("/latest", "/tag/v2.0")
                html = f'<h1 class="package-header__name">{task.identifier} {val}</h1>'.encode()
                with patch("run_public_benchmark.http_get", return_value=(html, url)), patch(
                    "run_public_benchmark.oracle", return_value=val
                ):
                    report = trial(task, "SPIDER", 0, path, "google", None)
                self.assertEqual(report["path"], "inheritance")
                self.assertTrue(report["success"])
                self.assertEqual(report["http_requests_from_spider"], 1)
                self.assertIsNone(report["cost_usd"])

    def test_unobserved_or_hallucinated_training_fails_closed(self):
        rows = examples("pypi")
        rows[0]["verified_against_independent_oracle"] = False
        with self.assertRaisesRegex(ValueError, "oracle"):
            learn_public_route("pypi", rows)
        rows = examples("pypi")
        rows[1]["visited_urls"] = ["https://evil.example/"]
        with self.assertRaisesRegex(ValueError, "observed exact"):
            learn_public_route("pypi", rows)
        rows = examples("pypi")
        rows[1]["identifier"] = rows[0]["identifier"]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            learn_public_route("pypi", rows)


if __name__ == "__main__":
    unittest.main()
