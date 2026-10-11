"""Fixed, public, read-only site benchmark with independent truth sources.

No account access, no writes, no broad crawling. Targets are intentionally
enumerated; the user can extend them after auditing a new site's terms.
Two holdout families: PyPI package versions and GitHub latest release tags.
This is a capability benchmark, not proof of non-degenerate economic value.
"""
from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import quote, unquote, urlsplit

USER_AGENT = "SpiderResearchReadOnly/0.1 (public metadata benchmark)"
TRAIN = {
    "pypi": ("requests", "pytest"),
    "github": ("pallets/flask", "psf/requests"),
}
HOLDOUT = {
    "pypi": ("httpx", "pydantic"),
    "github": ("astral-sh/ruff", "pydantic/pydantic"),
}
VERS = re.compile(r"[A-Za-z0-9][A-Za-z0-9.+_-]{0,99}\Z")


@dataclass(frozen=True)
class PublicTask:
    family: str
    identifier: str

    def __post_init__(self):
        if self.family not in TRAIN:
            raise ValueError("unsupported family")
        if self.identifier not in TRAIN[self.family] + HOLDOUT[self.family]:
            raise ValueError("identifier outside curated read-only benchmark allowlist")

    @property
    def start_url(self) -> str:
        if self.family == "pypi":
            return "https://pypi.org/"
        return "https://github.com/"

    @property
    def target_url(self) -> str:
        if self.family == "pypi":
            return f"https://pypi.org/project/{self.identifier}/"
        return f"https://github.com/{self.identifier}/releases/latest"

    @property
    def oracle_url(self) -> str:
        if self.family == "pypi":
            return f"https://pypi.org/pypi/{self.identifier}/json"
        return f"https://api.github.com/repos/{self.identifier}/releases/latest"

    @property
    def prompt(self) -> str:
        if self.family == "pypi":
            return (f"Start at {self.start_url} and find the latest released "
                    f"version of the PyPI package {self.identifier}. "
                    "Read it from the public project page, not from an API. "
                    "Return only the exact version string.")
        return (f"Start at {self.start_url} and find the latest published "
                f"GitHub Release tag of the repository {self.identifier}. "
                "Read it from the public release page. Return only the tag.")


def http_get(url: str) -> tuple[bytes, str]:
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/html;q=0.9",
        }), timeout=12,
    ) as response:
        if response.status != 200:
            raise RuntimeError(f"bad HTTP status {response.status}")
        if len(response.headers.get("Content-Length", "0")) > 4_000_000:
            raise RuntimeError("excessive response size")
        content = response.read(4_000_001)
        if len(content) > 4_000_000:
            raise RuntimeError("response too large")
        return content, response.geturl()


def oracle(task: PublicTask) -> str:
    raw, final_url = http_get(task.oracle_url)
    if urlsplit(final_url).hostname not in {"pypi.org", "api.github.com"}:
        raise ValueError("oracle redirect crossed expected host")
    data = json.loads(raw)
    value = data["info"]["version"] if task.family == "pypi" else data["tag_name"]
    if not isinstance(value, str) or not VERS.fullmatch(value):
        raise ValueError("oracle value invalid")
    return value


class _PyPIHeader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        if self.depth:
            self.depth += 1
        elif tag == "h1" and "package-header__name" in dict(attrs).get("class", "").split():
            self.depth = 1

    def handle_endtag(self, tag):
        if self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.text.append(data)


def parse_page(task: PublicTask, raw: bytes, final_url: str) -> str | None:
    url = urlsplit(final_url)
    if task.family == "github":
        if url.scheme != "https" or url.hostname != "github.com":
            return None
        prefix = f"/{task.identifier}/releases/tag/"
        if not url.path.startswith(prefix) or url.query or url.fragment:
            return None
        tag = unquote(url.path[len(prefix):])
        return tag if VERS.fullmatch(tag) else None
    if url.scheme != "https" or url.hostname != "pypi.org" or url.path != f"/project/{task.identifier}/":
        return None
    parser = _PyPIHeader()
    parser.feed(raw.decode("utf-8", errors="replace"))
    text = " ".join(" ".join(parser.text).split())
    # The page title must contain the exact package name, followed by the version.
    match = re.fullmatch(rf"{re.escape(task.identifier)}\s+([A-Za-z0-9][A-Za-z0-9.+_-]{{0,99}})", text)
    return match.group(1) if match else None


def direct_result(task: PublicTask) -> str:
    """Strong direct API comparator; never call this a Spider result."""
    return oracle(task)


def compiled_result(task: PublicTask) -> str:
    """Read-only compiled public page route with no LLM. Same page as Spider replay."""
    raw, final_url = http_get(task.target_url)
    version = parse_page(task, raw, final_url)
    if version is None:
        raise ValueError("unreadable public page (abstain)")
    return version


def verify(task: PublicTask, candidate: str) -> dict:
    try:
        expected = oracle(task)
    except Exception as exc:
        return {"verified": False, "oracle_valid": False, "reason": str(exc)}
    return {"verified": candidate == expected, "oracle_valid": True, "expected": expected}


def allowlisted_tasks(phase: str = "holdout") -> list[PublicTask]:
    source = HOLDOUT if phase == "holdout" else TRAIN if phase == "train" else None
    if source is None:
        raise ValueError("unknown phase")
    return [PublicTask(family, name) for family, names in source.items() for name in names]
