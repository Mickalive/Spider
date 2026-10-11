"""Fixture-scoped browser-trace compiler: real URLs -> guarded reusable mechanism.

This is engineering proof of the browser-trace -> procedural inheritance chain.
It does not use Spider's production distill() or claim cross-site generalization.
Two separate successful browser observations, a known local schema and strict
URL/ID constraints are required before a candidate is admitted.
"""
from __future__ import annotations

import hashlib
import re
from html.parser import HTMLParser
from urllib.parse import parse_qsl, urlsplit

from .models import Mechanism

_ID = re.compile(r"[A-Z][A-Z0-9-]{2,39}\Z")
_SUPPORTED = {"invoices", "shipments"}


class _AnswerParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.answer_depth = 0
        self.answers: list[str] = []
        self.body: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        if self.answer_depth:
            self.answer_depth += 1
        elif dict(attrs).get("id") == "answer":
            self.answer_depth = 1

    def handle_endtag(self, tag: str):
        if self.answer_depth:
            self.answer_depth -= 1

    def handle_data(self, data: str):
        self.body.append(data)
        if self.answer_depth:
            self.answers.append(data)


def parse_verified_detail(html: str, identifier: str) -> str | None:
    if not isinstance(identifier, str) or not _ID.fullmatch(identifier):
        return None
    doc = _AnswerParser()
    doc.feed(html)
    text = " ".join(" ".join(doc.body).split())
    # A value alone is insufficient: identify the requested record, too.
    if re.search(r"(?<!\w)Reference:\s*" + re.escape(identifier) + r"(?![\w-])", text) is None:
        return None
    value = " ".join(" ".join(doc.answers).split())
    return value if value else None


def compile_browser_traces(family: str, examples: list[dict]) -> Mechanism:
    if family not in _SUPPORTED:
        raise ValueError("unsupported fixture family")
    if len(examples) != 2:
        raise ValueError("two independent browser examples required")
    ids = [e.get("identifier") for e in examples]
    if len(set(ids)) != 2 or any(not isinstance(x, str) or not _ID.fullmatch(x) for x in ids):
        raise ValueError("distinct supported IDs required")
    origins = set()
    evidence = []
    for example in examples:
        identifier = example["identifier"]
        url = urlsplit(example.get("final_url", ""))
        if url.scheme != "http" or url.hostname != "127.0.0.1" or url.username or url.password or url.fragment:
            raise ValueError("only local recorded fixture URLs are accepted")
        if url.path != f"/portal/{family}/view":
            raise ValueError("not a verified detail-route trace")
        if parse_qsl(url.query, keep_blank_values=True, strict_parsing=True) != [("id", identifier)]:
            raise ValueError("detail URL does not bind the exact observed ID")
        if example.get("answer") != parse_verified_detail(example.get("page_html", ""), identifier):
            raise ValueError("page trace does not verify the same record and answer")
        origins.add((url.scheme, url.netloc))
        evidence.append(hashlib.sha256((identifier + "|" + url.path + "?" + url.query).encode()).hexdigest())
    if len(origins) != 1:
        raise ValueError("examples must originate in one observed fixture origin")
    return Mechanism(
        mechanism_id=f"BROWSER-TRACE-{family}-2SAMPLE",
        intent=f"read-{family}",
        preconditions={"family": family, "portal_schema": "local-fixture-v1"},
        applicability_guards={"execution_surface": "loopback-fixture"},
        action_template={"method": "GET", "path": f"/portal/{family}/view?id=${{id}}", "format": "html"},
        postconditions={"verified": True},
        parameter_slots=["id"],
        verification_rule={"replay_safe": True, "provenance": "two_observed_chromium_routes"},
        evidence=evidence,
        confidence=0.85,
    )
