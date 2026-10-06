"""Frozen-design executor for EXP-FRONTIER-37385647440.

Lane: frontier. Frozen inputs (immutable): request.json, spec.json, prereg.md,
freeze.json.

WHAT THIS SCRIPT IS. It executes the frozen design verbatim. It does not
re-design, re-freeze or amend any frozen input. Every implementation choice that
resolves an ambiguity in the frozen text is written to
derived/implementation_choices.json so that AUDIT can recompute or dispute it.

SAFETY. GET only. No browser, no Docker, no model key, no credentials, no write
verb, no third-party state mutation. 0 non-GET requests are issued.

DURABILITY (prereg section 9). Every response body is content-addressed by
SHA256 of the body bytes and cached at raw/responses_cache/<sha256>.json.gz. The
address is sha256 of the raw body bytes exactly as prereg section 9 requires; the
JSON record is gzip-compressed only for storage. Per-item per-session
observations are persisted to raw/observations.jsonl with a non-self-referential
per-line observation_hash, so the run is auditable without re-hitting a live
network.

PHASES.
  0 preflight    constants, environment record, frozen-input hash verification
  1 cold pass    ONE cold unconditional breadth-first crawl per frozen target
                 site (max 2 hops, max 50 pages, no prior map, GET only). This
                 single cold pass serves BOTH prereg section 3 item discovery
                 AND the COLD_REEXPLORATION (re_derivation) cost measurement,
                 because both prereg procedures specify the identical cold BFS
                 from root with no prior map. Charging one cold crawl is the
                 conservative reading: it never charges the cold agent more
                 than the frozen procedure does.
  2 stationarity K=5 independent fresh sessions, disjoint cookie jars per
                 session, global >=60 s barrier between consecutive sessions,
                 2 GETs per URL per session ~1 s apart (the single frozen
                 intra-session repetition).
  3 observations per-item, per-session value / body-hash / token records.
"""

from __future__ import annotations

import gzip
import hashlib
import http.cookiejar
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Any

# --------------------------------------------------------------------------
# 0. FROZEN CONSTANTS. Source: spec.json + prereg.md sections 2, 3, 4, 5, 8.
# --------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-FRONTIER-37385647440"
GITHUB_RUN_ID = "37385647440"
LANE = "frontier"

K_SESSIONS = 5                  # prereg section 2: "Sessions per Target (K) >= 5 (frozen at 5)"
MIN_INTER_SESSION_DELAY_S = 60  # prereg section 2 and 6.3
INTRA_SESSION_REPLICATION_S = 1.0  # prereg section 4: "separated by ~1s"
MAX_HOPS = 2                    # prereg section 3: "max 2 hops"
MAX_PAGES_PER_COLD_CRAWL = 50   # prereg section 5: "max 2 hops, max 50 pages"
MAX_ITEMS_PER_SITE = 6          # declared per-site admission cap (cost bound)
BOOTSTRAP_RESAMPLES = 10000     # spec decision_rule.primary_classification.reporting
BOOTSTRAP_SEED = 37385647440    # prereg section 8.1 "seed = 37385647440"
TOKENIZER_ENCODING = "cl100k_base"

# Frozen target pool, prereg section 3. No post-freeze substitution.
FROZEN_SITES = [
    ("gitlab", "https://gitlab.com"),
    ("wikimedia", "https://auth.wikimedia.org"),
    ("wikipedia", "https://en.wikipedia.org"),
    ("bitbucket", "https://bitbucket.org"),
    ("httpbin", "https://httpbin.org"),
    ("postman_echo", "https://postman-echo.com"),
]

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXP_DIR = os.path.join(ROOT, "research", "experiments", EXPERIMENT_ID)
RAW_DIR = os.path.join(EXP_DIR, "raw")
DERIVED_DIR = os.path.join(EXP_DIR, "derived")
CACHE_DIR = os.path.join(RAW_DIR, "responses_cache")

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

TOKEN_NAME_RE = re.compile(r"(csrf|token|nonce|authenticity|state|session)", re.IGNORECASE)
CACHE_BUSTER_RE = re.compile(r"\{rand16\}")

IMPLEMENTATION_CHOICES: list[dict] = []


def note(choice_id: str, question: str, resolution: str, effect: str) -> None:
    IMPLEMENTATION_CHOICES.append({
        "choice_id": choice_id, "frozen_text_is_ambiguous_about": question,
        "resolution_applied": resolution, "effect_on_result": effect,
    })


note("IC-01",
     "prereg section 4 defines body_hash as 'SHA256 of the full HTTP response body' of "
     "the item's page_url, and rules 2 and 3 disagree about whether within-session "
     "constancy is tested on the VALUE alone (rule 2 operational test) or on VALUE and "
     "body_hash together (rule 2 prose and rule 3 prose).",
     "PRIMARY implements the prose reading: a within-session instance is the PAIR "
     "(value, body_hash) for rules 2 and 3. The value-only reading is computed in "
     "parallel and reported as derived/classification_sensitivity.json; it never "
     "overrides the primary.",
     "Decisive for the class of any item whose page body changes between two requests "
     "1 s apart inside one session.")

note("IC-02",
     "prereg section 4 says 'In each session, we fetch the item's page URL' but the "
     "KNOWN_STATIONARY_CONTROL designates two items that are LINKS DISCOVERED ON THE "
     "ROOT page. Under a literal reading their body_hash is the ROOT page body, which "
     "is not a stationary resource; under a resource reading it is the linked "
     "resource's body.",
     "PRIMARY follows the literal reading: page_url for those two items is the root "
     "page the link was observed on. A secondary resource-level probe of the linked "
     "target is recorded separately in raw/http.jsonl phase=secondary_resource_probe "
     "and summarised as a disclosed sensitivity. It never overrides the primary.",
     "Decisive for the KNOWN_STATIONARY_CONTROL verdict on the two root nav-link items.")

note("IC-03",
     "prereg section 4's tie-break 'the first matching class in the table order applies' "
     "lists session_scoped BEFORE time_scoped and rotating, while rules 4 and 5 are both "
     "defined as refinements of the session-scoped pattern. Rule 2 therefore matches "
     "first and rules 4 and 5 are unreachable.",
     "The frozen order is applied unchanged to the PRIMARY classification. A secondary "
     "post-hoc classification that applies rules 4 and 5 to session-scoped-pattern "
     "items is computed and reported separately, explicitly labelled as NOT part of the "
     "frozen decision rule.",
     "PRIMARY counts for time_scoped and rotating are structurally 0 by construction, "
     "so those two classes carry no primary information in this run.")

note("IC-04",
     "prereg section 4's operational test for time_scoped says 'values cycle with period "
     "approximately K if delay-controlled', which does not define a computable test.",
     "PRIMARY leaves time_scoped unreachable (see IC-03). The secondary classification "
     "implements an explicit, declared periodicity statistic on the value series "
     "(detected exact-value recurrence) and records it as post-hoc only.",
     "Only affects the post-hoc diagnostic, never the frozen decision rule.")

note("IC-05",
     "prereg section 6.2 names https://gitlab.com/users/sign_in for the gitlab CSRF "
     "control item while its own header says 'The 4 server-minted CSRF tokens from "
     "parent packet', and the parent handoff records the gitlab token at "
     "https://gitlab.com/-/trial_registrations/new/.",
     "BOTH URLs are executed live. The REVERIFIED_NON_STATIONARY verdict is computed on "
     "the prereg-named URL only. The parent-cited URL is reported separately and is "
     "never substituted for the prereg-named anchor.",
     "Determines the REVERIFIED_NON_STATIONARY control verdict and therefore the frozen "
     "controls_gate branch.")

note("IC-06",
     "prereg section 3 states a 2-hop crawl but does not state whether the crawl may "
     "leave the starting host, and section 3 also designates two root-page control items "
     "by a nominal root URL that three of the six frozen sites redirect away from.",
     "The crawl is pinned to the host of the page actually served after redirects, and "
     "the effective root is the post-redirect final URL. Redirect facts are recorded per "
     "request in raw/http.jsonl and reported as a validity note. No target was substituted.",
     "Changes which page the two root-page control items are observed on; it does not "
     "change the frozen target pool.")

note("IC-07",
     "prereg section 6.1 makes httpbin.org/sitemap.xml conditional ('if exists, else "
     "skip') and no other control item is marked optional.",
     "sitemap.xml is executed live; a 404 records the item as absent-and-skipped with "
     "n_distinct_values null, never 0.0, and it is excluded from the control verdict by "
     "the frozen conditional rather than by producer choice.",
     "Affects the KNOWN_STATIONARY_CONTROL denominator only.")

note("IC-10",
     "prereg section 6.2 declares two anchors for the same control element "
     "(authenticity_token at the prereg-named /users/sign_in and at the parent-cited "
     "/-/trial_registrations/new/) without stating that they are distinct items.",
     "item identity includes page_url, so the two anchors are distinct items with "
     "distinct per-session records. An earlier pass keyed items by "
     "(ctrl_id, element_type, element_name) only, which collapsed the two anchors and "
     "discarded the prereg-named anchor's observations; that pass was discarded.",
     "Restores the prereg-named REVERIFIED_NON_STATIONARY anchor as an independently "
     "reported control item.")

note("IC-09",
     "prereg section 3 designates link items by the absolute URL they point at, while "
     "real markup writes hrefs in relative form, and prereg section 4 does not say which "
     "form is the item's VALUE.",
     "A link is present if the raw href equals the designated URL OR normalises against "
     "the page URL to the designated URL; the recorded value is the raw href as served. "
     "An earlier pass of this executor compared only raw hrefs to absolute URLs and "
     "reported 8 present links as absent; that pass was discarded, its derived outputs "
     "were deleted, and the whole run was repeated with the corrected extractor.",
     "Moves 8 link items, including one frozen KNOWN_STATIONARY_CONTROL item, from "
     "unclassifiable to classified.")

note("IC-08",
     "prereg section 5 defines re_acquisition_cost as the tokens of 'all response bodies "
     "+ headers observed along the path' without fixing the serialization.",
     "Declared canonical serialization, recorded in every raw observation so any token "
     "number is recomputable from the content-addressed cache: '<final_url>\\n<status>\\n' "
     "followed by every received response header in received order as 'name: value\\n', "
     "followed by the response body decoded utf-8 with replacement.",
     "Determines the absolute token values but not the sign of any frozen comparison, "
     "which is a difference of two measurements taken under the same serialization.")


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def line_hash(record: dict) -> str:
    """Non-self-referential line hash: sha256 of the record WITHOUT its hash field."""
    stripped = {k: v for k, v in record.items() if k != "observation_hash"}
    return sha256_hex(canonical_json(stripped).encode("utf-8"))


class JsonlWriter:
    def __init__(self, path: str, hash_field: str = "observation_hash") -> None:
        self.path = path
        self.hash_field = hash_field
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.fh = open(path, "w", encoding="utf-8")
        self.n = 0

    def write(self, record: dict) -> dict:
        rec = dict(record)
        if self.hash_field:
            rec[self.hash_field] = line_hash(rec)
        self.fh.write(canonical_json(rec) + "\n")
        self.n += 1
        return rec

    def close(self) -> None:
        self.fh.close()


class ResponseCache:
    """Content-addressed durable raw evidence. Address = sha256 of the body bytes."""

    def __init__(self) -> None:
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.written: set[str] = set()
        self.bytes_written = 0

    def put(self, record: dict) -> str:
        digest = record["body_sha256"]
        self.bytes_written += len(record.get("body") or "")
        if digest in self.written:
            return digest
        self.written.add(digest)
        path = os.path.join(CACHE_DIR, f"{digest}.json.gz")
        if not os.path.exists(path):
            with gzip.open(path, "wt", encoding="utf-8") as fh:
                fh.write(canonical_json(record))
        return digest


_ENC = None


def encoder():
    global _ENC
    if _ENC is None:
        import tiktoken  # disclosed build-time dependency; see report.md section 9
        _ENC = tiktoken.get_encoding(TOKENIZER_ENCODING)
    return _ENC


def observation_text(final_url: str, status, headers: list, body_text: str) -> str:
    """Frozen cost representation, declared in IC-08."""
    parts = [f"{final_url}\n{status}\n"]
    parts.extend(f"{k}: {v}\n" for k, v in headers)
    parts.append(body_text)
    return "".join(parts)


def expand_template(url: str, session: int) -> str:
    return CACHE_BUSTER_RE.sub(
        lambda _: sha256_hex(f"{url}|{session}".encode())[:16], url)


# --------------------------------------------------------------------------
# HTTP substrate: stdlib only, GET only, disjoint cookie jar per session.
# --------------------------------------------------------------------------

class Session:
    def __init__(self, label: str) -> None:
        self.label = label
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.jar),
            urllib.request.HTTPRedirectHandler(),
        )
        self.n_get = 0
        self.n_non_get = 0

    def get(self, url: str, timeout: int = 30, attempts: int = 2) -> dict:
        rec = None
        for attempt in range(attempts):
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive",
                },
                method="GET",
            )
            try:
                resp = self.opener.open(req, timeout=timeout)
                raw = resp.read()
                rec = {
                    "url": url, "ok": True, "error": None, "final_url": resp.geturl(),
                    "status": resp.status,
                    "headers": [[k, v] for k, v in resp.headers.items()], "raw": raw,
                }
                break
            except urllib.error.HTTPError as exc:
                raw = b""
                try:
                    raw = exc.read()
                except Exception:  # noqa: BLE001
                    pass
                rec = {
                    "url": url, "ok": True, "error": None,
                    "final_url": exc.geturl() if hasattr(exc, "geturl") else url,
                    "status": exc.code,
                    "headers": [[k, v] for k, v in (exc.headers.items() if exc.headers else [])],
                    "raw": raw,
                }
                break
            except Exception as exc:  # noqa: BLE001
                err = f"{type(exc).__name__}:{exc}"
                if attempt + 1 < attempts:
                    time.sleep(1.0)
                    continue
                rec = {"url": url, "ok": False, "error": err, "final_url": url,
                       "status": None, "headers": [], "raw": b""}
                break
        body_text = rec["raw"].decode("utf-8", "replace")
        ctype = next((v for k, v in rec["headers"] if k.lower() == "content-type"), None)
        out = {
            "url": rec["url"], "ok": rec["ok"], "error": rec["error"],
            "final_url": rec["final_url"], "status": rec["status"],
            "headers": rec["headers"], "body": body_text,
            "body_sha256": sha256_hex(rec["raw"]),
            "body_bytes": len(rec["raw"]),
            "content_type": ctype, "tokens": None,
        }
        if rec["ok"]:
            self.n_get += 1
            out["tokens"] = len(encoder().encode(
                observation_text(rec["final_url"], rec["status"], rec["headers"], body_text)))
        return out

    def cookie_names(self) -> list[str]:
        return sorted({c.name for c in self.jar})


# --------------------------------------------------------------------------
# HTML extraction (stdlib html.parser only; no browser, no JavaScript).
# --------------------------------------------------------------------------

class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.forms: list[dict] = []
        self.inputs: list[dict] = []
        self.metas: list[dict] = []
        self._form: dict | None = None
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "form":
            self._form = {"action": a.get("action", ""),
                          "method": (a.get("method") or "get").lower(),
                          "id": a.get("id", "")}
            self.forms.append(self._form)
        elif tag == "input":
            rec = {"name": a.get("name", ""), "value": a.get("value", ""),
                   "type": a.get("type", "text"), "id": a.get("id", "")}
            self.inputs.append(rec)
            if self._form is not None:
                self._form.setdefault("inputs", []).append(rec)
        elif tag == "meta":
            self.metas.append({
                "name": a.get("name", ""), "property": a.get("property", ""),
                "http_equiv": a.get("http-equiv", ""), "content": a.get("content", ""),
            })
        elif tag in ("script", "style"):
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag == "form":
            self._form = None
        if tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        return


def parse_page(body: str) -> PageParser:
    p = PageParser()
    try:
        p.feed(body)
        p.close()
    except Exception:  # noqa: BLE001 - malformed markup must not abort the run
        pass
    return p


def normalize_href(href: str, base: str) -> str | None:
    try:
        u = urllib.parse.urljoin(base, href.strip())
    except Exception:  # noqa: BLE001
        return None
    p = urllib.parse.urlparse(u)
    if p.scheme not in ("http", "https"):
        return None
    return urllib.parse.urlunparse((p.scheme, p.netloc, p.path or "/", p.params, p.query, ""))


def is_crawlable(url: str) -> bool:
    return not re.search(
        r"\.(png|jpe?g|gif|svg|webp|ico|css|js|json|xml|txt|zip|gz|pdf|mp4|webm|woff2?|ttf|eot)$",
        url.lower())


# --------------------------------------------------------------------------
# per-item admission (prereg section 3: per-item, NO site-level conjunction)
# --------------------------------------------------------------------------

def item_candidates(page_url: str, page: PageParser, depth: int):
    """Return [(priority, element_type, element_name, selector, value, value_kind)].

    Priority 0  token-like or hidden <input> on any crawled page: the class an
                agent must carry to replay an action.
    Priority 1  other hidden inputs.
    Priority 2  meta tags whose name/property/http-equiv is token-like.
    Priority 3  same-host links on the ROOT page only, which is where the frozen
                KNOWN_STATIONARY_CONTROL designates its nav-link items.
    """
    out = []
    page_host = urllib.parse.urlparse(page_url).netloc
    for inp in page.inputs:
        name = inp["name"]
        if not name:
            continue
        hidden = inp["type"].lower() == "hidden"
        if hidden and TOKEN_NAME_RE.search(name):
            prio = 0
        elif hidden:
            prio = 1
        elif TOKEN_NAME_RE.search(name):
            prio = 0
        else:
            continue
        out.append((prio, "input", name, f"//input[@name='{name}']", inp["value"], "value"))
    for m in page.metas:
        key = m["name"] or m["property"] or m["http_equiv"] or ""
        if key and TOKEN_NAME_RE.search(key) and m["content"]:
            out.append((2, "meta", key, f"//meta[@name='{key}']", m["content"], "meta"))
    if depth == 0:
        seen = set()
        for href in page.links[:60]:
            absu = normalize_href(href, page_url)
            if not absu or absu in seen:
                continue
            if urllib.parse.urlparse(absu).netloc != page_host:
                continue
            seen.add(absu)
            out.append((3, "link", absu, f"//a[@href='{absu}']", absu, "href"))
    return out


def extract_value(body: str, headers: list, kind: str, element_name: str,
                  page_url: str | None = None,
                  fallback_kind: str | None = None):
    """Return (value, extract_status) with status in {ok, empty, absent, fallback, error}.

    IC-09. For a link item the prereg designates the item by the URL it points at,
    while real markup writes hrefs in relative form. A link is therefore present if
    the raw href matches the designated URL exactly OR if normalising the raw href
    against the page URL yields the designated URL. An earlier pass of this executor
    matched only exact raw hrefs, which reported 8 present links as absent; that pass
    was discarded and is not shipped.
    """
    if kind == "value":
        for inp in parse_page(body).inputs:
            if inp["name"] == element_name:
                return inp["value"], ("ok" if inp["value"] else "empty")
        return None, "absent"
    if kind == "href":
        for h in parse_page(body).links:
            raw = h.strip()
            if raw == element_name:
                return raw, "ok"
            if page_url:
                norm = normalize_href(raw, page_url)
                if norm and norm == element_name:
                    return raw, "ok"
        return None, "absent"
    if kind == "meta":
        for m in parse_page(body).metas:
            if (m["name"] or m["property"] or m["http_equiv"] or "") == element_name:
                return m["content"], ("ok" if m["content"] else "empty")
        return None, "absent"
    if kind == "body":
        return body, ("ok" if body else "empty")
    if kind.startswith("json:"):
        field = kind.split(":", 1)[1]
        try:
            obj = json.loads(body)
        except Exception:  # noqa: BLE001
            return None, "error"
        if isinstance(obj, dict) and field in obj:
            return str(obj[field]), "ok"
        return None, "absent"
    if kind.startswith("header:"):
        field = kind.split(":", 1)[1]
        for k, v in headers or []:
            if k.lower() == field.lower():
                return v, "ok"
        if fallback_kind == "ua_hash":
            return sha256_hex(USER_AGENT.encode())[:32], "fallback"
        return None, "absent"
    return None, "error"


# --------------------------------------------------------------------------
# FROZEN CONTROL DECLARATIONS (prereg section 6), declared before any run.
# --------------------------------------------------------------------------

def control_declarations() -> list[dict]:
    return [
        # 6.1 KNOWN_STATIONARY_CONTROL
        {"ctrl_id": "KNOWN_STATIONARY_CONTROL", "role": "positive", "site": "httpbin",
         "page_url": "https://httpbin.org/robots.txt", "element_type": "file",
         "element_name": "robots.txt", "selector": "//body", "value_kind": "body",
         "prereg_designated": True, "optional": False},
        {"ctrl_id": "KNOWN_STATIONARY_CONTROL", "role": "positive", "site": "httpbin",
         "page_url": "https://httpbin.org/sitemap.xml", "element_type": "file",
         "element_name": "sitemap.xml", "selector": "//body", "value_kind": "body",
         "prereg_designated": True, "optional": True},  # prereg: "if exists, else skip"
        {"ctrl_id": "KNOWN_STATIONARY_CONTROL", "role": "positive", "site": "gitlab",
         "page_url": "https://gitlab.com/favicon.ico", "element_type": "file",
         "element_name": "favicon.ico", "selector": "//body", "value_kind": "body",
         "prereg_designated": True, "optional": False},
        {"ctrl_id": "KNOWN_STATIONARY_CONTROL", "role": "positive", "site": "wikipedia",
         "page_url": "https://en.wikipedia.org/static/favicon/wikipedia.ico",
         "element_type": "file", "element_name": "wikipedia.ico", "selector": "//body",
         "value_kind": "body", "prereg_designated": True, "optional": False},
        {"ctrl_id": "KNOWN_STATIONARY_CONTROL", "role": "positive", "site": "gitlab",
         "root_of": "https://gitlab.com", "element_type": "link",
         "element_name": "https://gitlab.com/explore",
         "selector": "//a[@href='https://gitlab.com/explore']", "value_kind": "href",
         "prereg_designated": True, "optional": False,
         "resource_probe": "https://gitlab.com/explore"},
        {"ctrl_id": "KNOWN_STATIONARY_CONTROL", "role": "positive", "site": "wikipedia",
         "root_of": "https://en.wikipedia.org", "element_type": "link",
         "element_name": "https://en.wikipedia.org/wiki/Main_Page",
         "selector": "//a[@href='https://en.wikipedia.org/wiki/Main_Page']",
         "value_kind": "href", "prereg_designated": True, "optional": False,
         "resource_probe": "https://en.wikipedia.org/wiki/Main_Page"},
        # 6.2 REVERIFIED_NON_STATIONARY
        {"ctrl_id": "REVERIFIED_NON_STATIONARY", "role": "live_positive", "site": "gitlab",
         "page_url": "https://gitlab.com/users/sign_in", "element_type": "input",
         "element_name": "authenticity_token", "selector": "//input[@name='authenticity_token']",
         "value_kind": "value", "prereg_designated": True, "optional": False,
         "note": "URL literally as named in prereg 6.2. Not substituted."},
        {"ctrl_id": "REVERIFIED_NON_STATIONARY", "role": "live_positive", "site": "wikimedia",
         "page_url": "https://auth.wikimedia.org/enwiki/w/index.php?title=Special:CreateAccount",
         "element_type": "input", "element_name": "wpCreateaccountToken",
         "selector": "//input[@name='wpCreateaccountToken']", "value_kind": "value",
         "prereg_designated": True, "optional": False},
        {"ctrl_id": "REVERIFIED_NON_STATIONARY", "role": "live_positive", "site": "gitlab",
         "page_url": "https://gitlab.com/-/trial_registrations/new/", "element_type": "input",
         "element_name": "authenticity_token", "selector": "//input[@name='authenticity_token']",
         "value_kind": "value", "prereg_designated": False, "optional": False,
         "note": "Parent-cited URL for the same control item "
                 "(EXP-FRONTIER-36306528608 handoff). Executed for information; "
                 "never substituted for the prereg-named URL."},
        # 6.4 NULL_STATIONARITY_ARM
        {"ctrl_id": "NULL_STATIONARITY_ARM", "role": "null", "site": "httpbin",
         "page_url": "https://httpbin.org/uuid", "element_type": "json_field",
         "element_name": "uuid", "selector": "$.uuid", "value_kind": "json:uuid",
         "prereg_designated": True, "optional": False},
        {"ctrl_id": "NULL_STATIONARITY_ARM", "role": "null", "site": "httpbin",
         "page_url": "https://httpbin.org/date", "element_type": "json_field",
         "element_name": "date", "selector": "$.date", "value_kind": "json:date",
         "prereg_designated": True, "optional": False},
        {"ctrl_id": "NULL_STATIONARITY_ARM", "role": "null", "site": "httpbin",
         "page_url": "https://httpbin.org/headers", "element_type": "header",
         "element_name": "X-Request-Id", "selector": "//headers/X-Request-Id",
         "value_kind": "header:X-Request-Id", "fallback_kind": "ua_hash",
         "prereg_designated": True, "optional": False},
        {"ctrl_id": "NULL_STATIONARITY_ARM", "role": "null", "site": "httpbin",
         "page_url": "https://httpbin.org/robots.txt?cache_buster={rand16}",
         "element_type": "file", "element_name": "robots.txt?cache_buster",
         "selector": "//body", "value_kind": "body", "prereg_designated": True,
         "optional": False, "randomize_query": True},
    ]


def main() -> int:
    t0 = time.time()
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DERIVED_DIR, exist_ok=True)

    env = {
        "python": sys.version.split()[0], "platform": sys.platform,
        "tiktoken_version": None, "tokenizer_encoding": TOKENIZER_ENCODING,
        "tiktoken_declared_in_pyproject": False, "network": "UNKNOWN",
        "started_at_unix": t0,
    }
    try:
        import tiktoken
        env["tiktoken_version"] = tiktoken.__version__
    except Exception as exc:  # noqa: BLE001
        env["tiktoken_error"] = f"{type(exc).__name__}:{exc}"
    try:
        socket.gethostbyname("httpbin.org")
        env["network"] = "AVAILABLE"
    except Exception as exc:  # noqa: BLE001
        env["network"] = f"UNAVAILABLE:{type(exc).__name__}:{exc}"

    http_w = JsonlWriter(os.path.join(RAW_DIR, "http.jsonl"), "record_hash")
    obs_w = JsonlWriter(os.path.join(RAW_DIR, "observations.jsonl"), "observation_hash")
    cache = ResponseCache()

    def log_http(**kw):
        http_w.write(kw)

    def store(rec):
        if rec["ok"] and rec["body"]:
            cache.put({"url": rec["url"], "final_url": rec["final_url"],
                       "status": rec["status"], "headers": rec["headers"],
                       "body": rec["body"], "body_sha256": rec["body_sha256"],
                       "body_bytes": rec["body_bytes"], "observation_tokens": rec["tokens"]})
        return rec

    def fetch_record(sess, url, **kw):
        r = sess.get(url)
        store(r)
        log_http(session_label=sess.label, ok=r["ok"], error=r["error"], url=r["url"],
                 final_url=r["final_url"], status=r["status"], content_type=r["content_type"],
                 body_bytes=r["body_bytes"], body_sha256=r["body_sha256"],
                 observation_tokens=r["tokens"],
                 set_cookie_names=[v.split("=", 1)[0] for k, v in r["headers"]
                                   if k.lower() == "set-cookie"],
                 fetched_at=time.time(), **kw)
        return r

    # ---------------- PHASE 1: one cold unconditional BFS crawl per site ----
    cold: dict[str, dict] = {}
    for label, root_url in FROZEN_SITES:
        sess = Session(f"cold-{label}")
        queue = [(root_url, None, 0)]
        visited: set[str] = set()
        pages: list[dict] = []
        parent: dict[str, str | None] = {}
        while queue and len(pages) < MAX_PAGES_PER_COLD_CRAWL:
            url, parent_url, depth = queue.pop(0)
            if url in visited or depth > MAX_HOPS:
                continue
            visited.add(url)
            r = fetch_record(sess, url, phase="cold_crawl", site=label, hop=depth,
                             parent_url=parent_url, fetch_order=len(pages))
            pages.append({"url": url, "final_url": r["final_url"], "status": r["status"],
                          "ok": r["ok"], "tokens": r["tokens"], "body_bytes": r["body_bytes"],
                          "body_sha256": r["body_sha256"], "fetch_order": len(pages),
                          "hop": depth, "parent_url": parent_url})
            parent[url] = parent_url
            if not r["ok"] or r["status"] != 200 or not r["body"]:
                continue
            parsed = parse_page(r["body"])
            final_host = urllib.parse.urlparse(r["final_url"]).netloc
            n_links = 0
            for href in parsed.links:
                absu = normalize_href(href, r["final_url"])
                if not absu or absu in visited or not is_crawlable(absu):
                    continue
                if urllib.parse.urlparse(absu).netloc != final_host:
                    continue
                queue.append((absu, r["final_url"], depth + 1))
                n_links += 1
                if n_links >= 60:
                    break
        cold[label] = {
            "site": label, "root_url": root_url, "pages": pages, "parent": parent,
            "cookie_names": sess.cookie_names(), "n_get": sess.n_get,
            "final_root": pages[0]["final_url"] if pages else None,
            "final_root_host": (urllib.parse.urlparse(pages[0]["final_url"]).netloc
                                if pages else None),
            "root_redirected": bool(pages and pages[0]["final_url"] != root_url),
        }
        print(f"[cold] {label}: {len(pages)} pages root_final={cold[label]['final_root']}",
              flush=True)

    # ---------------- item admission (per item, no site-level conjunction) ----
    admitted: list[dict] = []
    for label, _ in FROZEN_SITES:
        found: list[dict] = []
        seen: set[tuple] = set()
        for pe in cold[label]["pages"]:
            if not pe["ok"] or pe["status"] != 200 or not pe["body_sha256"]:
                continue
            with gzip.open(os.path.join(CACHE_DIR, f"{pe['body_sha256']}.json.gz"),
                           "rt", encoding="utf-8") as fh:
                cached = json.load(fh)
            parsed = parse_page(cached["body"])
            for prio, etype, ename, selector, value, vkind in item_candidates(
                    pe["url"], parsed, pe["hop"]):
                key = (pe["url"], etype, ename)
                if key in seen:
                    continue
                seen.add(key)
                found.append({
                    "item_id": f"{label}|{etype}|{pe['url']}|{ename}",
                    "site": label, "page_url": pe["url"], "element_type": etype,
                    "element_name": ename, "selector": selector,
                    "discovery_value": value, "discovery_value_sha256":
                        sha256_hex((value or "").encode()),
                    "discovery_priority": prio, "value_kind": vkind, "hop": pe["hop"],
                    "is_control": False, "ctrl_id": None, "optional": False,
                    "prereg_designated": None, "role": "primary_pool",
                    "resource_probe": None, "randomize_query": False,
                    "fallback_kind": None,
                })
        found.sort(key=lambda f: (f["discovery_priority"], f["hop"], f["page_url"],
                                  f["element_name"]))
        for f in found[:MAX_ITEMS_PER_SITE]:
            f["admitted"] = True
            f["admission_reason"] = (
                f"per-item admission: priority={f['discovery_priority']} "
                f"element_type={f['element_type']} hop={f['hop']}; "
                f"{len(found)} candidates detected on this site, admitted "
                f"{min(MAX_ITEMS_PER_SITE, len(found))} under declared cap "
                f"MAX_ITEMS_PER_SITE={MAX_ITEMS_PER_SITE}")
            admitted.append(f)
        cold[label]["n_candidates_detected"] = len(found)
    print(f"[admission] {sum(1 for a in admitted if not a['is_control'])} discovered "
          f"items admitted across {len(cold)} sites", flush=True)

    # control items join the same observation set
    for d in control_declarations():
        page_url = cold.get(d["site"], {}).get("final_root") if d.get("root_of") else d["page_url"]
        page_url = page_url or d.get("root_of") or d["page_url"]
        admitted.append({
            # IC-10: the page_url is part of the identity. Two distinct control items
            # (the prereg-named https://gitlab.com/users/sign_in anchor and the
            # parent-cited https://gitlab.com/-/trial_registrations/new/ anchor) declare
            # the same element_name, so an identity without the URL collapses them and
            # silently discards one anchor's observations.
            "item_id": f"{d['ctrl_id']}|{d['element_type']}|{page_url}|{d['element_name']}",
            "site": d["site"], "page_url": page_url,
            "element_type": d["element_type"], "element_name": d["element_name"],
            "selector": d["selector"], "discovery_value": None,
            "discovery_priority": -1, "value_kind": d["value_kind"],
            "hop": None, "admitted": True,
            "admission_reason": "pre-declared frozen control item, prereg section 6",
            "is_control": True, "ctrl_id": d["ctrl_id"], "role": d["role"],
            "optional": d.get("optional", False),
            "prereg_designated": d.get("prereg_designated", True),
            "note": d.get("note"), "resource_probe": d.get("resource_probe"),
            "randomize_query": d.get("randomize_query", False),
            "fallback_kind": d.get("fallback_kind"),
        })

    # fetch set per site = item pages plus their BFS ancestors (paths must be walkable)
    fetch_urls_by_site: dict[str, list[str]] = {}
    for item in admitted:
        by = fetch_urls_by_site.setdefault(item["site"], [])
        u = item["page_url"]
        if u not in by:
            by.append(u)
        p = cold.get(item["site"], {}).get("parent", {}).get(u)
        while p and p not in by:
            by.append(p)
            p = cold.get(item["site"], {}).get("parent", {}).get(p)

    # ---------------- PHASE 2: K independent fresh sessions -------------------
    session_records: list[dict] = []
    obs_index: dict[tuple, dict] = {}
    inter_session_delays: list[dict] = []

    for s in range(K_SESSIONS):
        if s > 0:
            ends = [r["ended_at"] for r in session_records if r["session"] == s - 1]
            if ends:
                wait = MIN_INTER_SESSION_DELAY_S - (time.time() - max(ends))
                if wait > 0:
                    time.sleep(wait)
        barrier_at = time.time()
        for label, _ in FROZEN_SITES:
            sess = Session(f"s{s}-{label}")
            obs_index[(label, s)] = {}
            for tmpl in fetch_urls_by_site.get(label, []):
                url = expand_template(tmpl, s)
                recs = []
                for rep in (0, 1):
                    if rep == 1:
                        time.sleep(INTRA_SESSION_REPLICATION_S)
                    recs.append(fetch_record(sess, url, phase="stationarity", site=label,
                                             session=s, replication=rep,
                                             url_template=tmpl))
                obs_index[(label, s)][url] = recs
            for item in admitted:
                if item["site"] != label or not item.get("resource_probe"):
                    continue
                rp = expand_template(item["resource_probe"], s)
                if rp in obs_index[(label, s)]:
                    continue
                rec = fetch_record(sess, rp, phase="secondary_resource_probe", site=label,
                                   session=s, replication=0, resource_for=item["item_id"])
                obs_index[(label, s)][rp] = [rec]
            session_records.append({
                "session": s, "site": label, "session_label": sess.label,
                "cookie_names": sess.cookie_names(), "n_get": sess.n_get,
                "n_urls": len(fetch_urls_by_site.get(label, [])),
                "barrier_at": barrier_at, "ended_at": time.time(),
            })
        for label, _ in FROZEN_SITES:
            cur = [r["ended_at"] for r in session_records
                   if r["session"] == s and r["site"] == label]
            prev = [r["ended_at"] for r in session_records
                    if r["session"] == s - 1 and r["site"] == label]
            if cur and prev:
                inter_session_delays.append({
                    "site": label, "session_pair": f"{s - 1}->{s}",
                    "delay_seconds": round(min(cur) - max(prev), 2)})
        print(f"[session {s}] complete, barrier at {time.strftime('%H:%M:%S')}", flush=True)

    # ---------------- PHASE 3: per-item per-session observations --------------
    items_out: list[dict] = []
    for item in admitted:
        label = item["site"]
        per_session: list[dict] = []
        for s in range(K_SESSIONS):
            url = expand_template(item["page_url"], s)
            recs = obs_index.get((label, s), {}).get(url)
            entry = {"session": s, "requested_url": url}
            if not recs:
                entry.update({"observed": False, "reason": "url_absent_from_fetch_set"})
                per_session.append(entry)
                continue
            entry["replications"] = []
            for rep, r in enumerate(recs):
                if r.get("resource_for"):
                    entry["replications"].append({"replication": rep, "secondary": True})
                    continue
                if not r["ok"]:
                    entry["replications"].append({
                        "replication": rep, "observed": False, "error": r["error"]})
                    continue
                value, xstatus = extract_value(r["body"], r["headers"], item["value_kind"],
                                               item["element_name"],
                                               page_url=item["page_url"],
                                               fallback_kind=item["fallback_kind"])
                rec = {
                    "replication": rep, "observed": True, "url": r["url"],
                    "final_url": r["final_url"], "http_status": r["status"],
                    "body_sha256": r["body_sha256"], "body_bytes": r["body_bytes"],
                    "observation_tokens": r["tokens"], "value": value,
                    "value_sha256": sha256_hex((value or "").encode()),
                    "value_length": len(value or ""), "value_extract_status": xstatus,
                }
                entry["replications"].append(rec)
                obs_w.write({
                    "item_id": item["item_id"], "site": label, "ctrl_id": item["ctrl_id"],
                    "page_url": item["page_url"], "element_name": item["element_name"],
                    "is_control": item["is_control"], "session": s, "replication": rep,
                    "observed": True, "url": r["url"], "final_url": r["final_url"],
                    "http_status": r["status"], "body_sha256": r["body_sha256"],
                    "observation_tokens": r["tokens"], "value_sha256": rec["value_sha256"],
                    "value_length": rec["value_length"], "value_extract_status": xstatus,
                })
            per_session.append(entry)
        items_out.append({**item, "per_session": per_session})

    with open(os.path.join(DERIVED_DIR, "items.json"), "w", encoding="utf-8") as fh:
        json.dump({
            "experiment_id": EXPERIMENT_ID, "environment": env,
            "constants": {
                "K_SESSIONS": K_SESSIONS,
                "MIN_INTER_SESSION_DELAY_S": MIN_INTER_SESSION_DELAY_S,
                "INTRA_SESSION_REPLICATION_S": INTRA_SESSION_REPLICATION_S,
                "MAX_HOPS": MAX_HOPS, "MAX_PAGES_PER_COLD_CRAWL": MAX_PAGES_PER_COLD_CRAWL,
                "MAX_ITEMS_PER_SITE": MAX_ITEMS_PER_SITE,
                "BOOTSTRAP_RESAMPLES": BOOTSTRAP_RESAMPLES,
                "BOOTSTRAP_SEED": BOOTSTRAP_SEED,
                "TOKENIZER_ENCODING": TOKENIZER_ENCODING,
                "FROZEN_SITES": FROZEN_SITES, "USER_AGENT": USER_AGENT,
            },
            "implementation_choices": IMPLEMENTATION_CHOICES,
            "cold": cold, "inter_session_delays": inter_session_delays,
            "session_records": session_records, "items": items_out,
        }, fh, indent=1)

    with open(os.path.join(RAW_DIR, "session_timing.jsonl"), "w", encoding="utf-8") as fh:
        for d in inter_session_delays:
            d2 = dict(d)
            d2["observation_hash"] = line_hash(d2)
            fh.write(canonical_json(d2) + "\n")

    obs_w.close()
    http_w.close()

    manifest = {
        "experiment_id": EXPERIMENT_ID,
        "wall_clock_seconds": round(time.time() - t0, 1),
        "responses_cached": len(cache.written),
        "cache_bytes_uncompressed": cache.bytes_written,
        "http_log_records": http_w.n, "observation_records": obs_w.n,
        "min_inter_session_delay_s": min((d["delay_seconds"] for d in inter_session_delays),
                                         default=None),
        "n_distinct_cookie_names_per_site": {
            r["site"]: r["cookie_names"] for r in session_records if r["session"] == 0},
    }
    with open(os.path.join(DERIVED_DIR, "run_manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    print(json.dumps(manifest, indent=1), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())