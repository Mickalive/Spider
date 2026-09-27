#!/usr/bin/env python3
"""Shared extraction/measurement pipeline for EXP-INTEL-36287179392 (lane intel).

Implements the FROZEN prereg.md sections 5-10 of
research/experiments/EXP-INTEL-36287179392/prereg.md:
  6.1 raw observation, 6.2 minimal structural representation, 6.3 baselines,
  6.4 minimal serialization, 7.1 structural signatures, 7.2 cross-site matching,
  7.3 AGF, 8 shuffled-host null, 9 host-level bootstrap, 10 cost metrics.

This module contains NO experiment outcome logic beyond the frozen estimator
definitions. It is imported by exp_36287179392_fetch.py,
exp_36287179392_extract.py and exp_36287179392_analyze.py.

No third-party credentials, registry auth, browser binary or model API key is
used at any point. Only anonymous public HTTP(S) GET.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.robotparser
from urllib.parse import parse_qsl, unquote, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# 0. Frozen constants (prereg section 5.2 / 16 / 6.1)
# ---------------------------------------------------------------------------

USER_AGENT = "SPIDER-Research/1.0"
ACCEPT = "text/html"
MAX_PAGES_PER_SITE = 10          # prereg 5.3
MIN_PAGES_PER_SITE = 2           # prereg 5.3
PER_HOST_MIN_INTERVAL_S = 1.05   # prereg 6.1: <=1 req/sec per host
CONNECT_TIMEOUT_S = 10           # prereg 6.1
READ_TIMEOUT_S = 30              # prereg 6.1
SEED_BOOTSTRAP = 36287179392     # prereg 16
SEED_NULL = 36287179392 + 1       # prereg 16
SEED_POSITIVE_CONTROL = 36287179392 + 2  # prereg 16
N_BOOTSTRAP = 10000              # prereg 9.2
N_NULL_PERMUTATIONS = 1000       # prereg 8.1

# prereg 5.2 - the site sample is FIXED before any measurement. Do not edit.
SITE_SAMPLE = [
    # (ordinal, site_key, base_url, category)
    (1, "github.com", "https://github.com", "developer platform"),
    (2, "docs.python.org", "https://docs.python.org", "documentation"),
    (3, "en.wikipedia.org", "https://en.wikipedia.org", "reference"),
    (4, "news.ycombinator.com", "https://news.ycombinator.com", "news aggregator"),
    (5, "stackoverflow.com", "https://stackoverflow.com", "q&a"),
    (6, "developer.mozilla.org", "https://developer.mozilla.org", "documentation"),
    (7, "pypi.org", "https://pypi.org", "package registry"),
    (8, "npmjs.com", "https://www.npmjs.com", "package registry"),
    (9, "crates.io", "https://crates.io", "package registry"),
    (10, "rubygems.org", "https://rubygems.org", "package registry"),
    (11, "gitlab.com", "https://gitlab.com", "developer platform"),
    (12, "bitbucket.org", "https://bitbucket.org", "developer platform"),
    (13, "sourceforge.net", "https://sourceforge.net", "developer platform"),
    (14, "dockerhub.io", "https://hub.docker.com", "container registry"),
    (15, "readthedocs.io", "https://readthedocs.io", "documentation hosting"),
    (16, "git-scm.com", "https://git-scm.com", "documentation"),
    (17, "linuxfoundation.org", "https://linuxfoundation.org", "organization"),
    (18, "apache.org", "https://apache.org", "organization"),
    (19, "gnu.org", "https://www.gnu.org", "organization"),
    (20, "kernel.org", "https://kernel.org", "reference"),
]

# prereg 5.3 excluded link substrings
EXCLUDE_LINK_TOKENS = (
    "logout", "log-out", "signout", "sign-out", "login", "log-in", "signin",
    "sign-in", "register", "account", "admin", "/api/", "api.", ".json",
)
STATIC_EXTS = (
    ".css", ".js", ".mjs", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
    ".woff", ".woff2", ".ttf", ".eot", ".ico", ".pdf", ".zip", ".tar", ".gz",
    ".mp4", ".mp3", ".webm", ".wasm", ".map", ".rss", ".xml",
)

# prereg 6.2.6 detail-link path patterns
DETAIL_SEGMENTS = (
    "item", "items", "product", "products", "article", "articles", "post",
    "posts", "question", "questions", "issue", "issues", "pr", "package",
    "packages", "crate", "crates", "gem", "gems", "project", "projects",
    "story", "stories", "news", "blog", "doc", "docs", "topic", "topics",
    "tag", "tags", "category", "categories", "user", "users", "repo", "repos",
)
# prereg 6.2.5 pagination indicators
PAGINATION_PARAMS = ("page", "p", "pageno", "offset", "start", "from", "pageindex")
PAGINATION_TEXT_RE = re.compile(r"(?i)\b(next|previous|prev|first|last|page\s*\d+|older|newer|more)\b")
REL_PAGINATION = ("prev", "next", "first", "last")

# prereg 6.2.2 semantic containers
NAV_TAGS = ("nav", "header", "footer")
LANDMARK_ROLES = ("navigation", "banner", "contentinfo", "search", "main", "form")
HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")
A11Y_SEMANTIC_TAGS = (
    "main", "nav", "article", "section", "aside", "header", "footer", "form",
    "button", "table", "ul", "ol", "li", "img", "a", "input", "select",
    "textarea", "label", "dialog", "details", "summary", "iframe",
) + HEADING_TAGS

# prereg 6.2 typed slots. Kept small and explicit; see report.md section on
# representation loss.
QUERY_PARAM_SLOTS = {
    "q": "{query}", "query": "{query}", "s": "{query}", "search": "{query}",
    "keyword": "{query}", "keywords": "{query}", "term": "{query}",
    "terms": "{query}", "searchquery": "{query}", "searchtext": "{query}",
    "find": "{query}", "querytext": "{query}",
    "page": "{page}", "p": "{page}", "pageno": "{page}", "page_number": "{page}",
    "pagenumber": "{page}", "pageindex": "{page}", "offset": "{page}",
    "start": "{page}", "startindex": "{page}", "from": "{page}", "results": "{page}",
    "category": "{category}", "cat": "{category}", "topic": "{category}",
    "tag": "{category}", "tags": "{category}", "section": "{category}",
    "channel": "{category}", "department": "{category}", "type": "{category}",
    "sort": "{sort}", "order": "{sort}", "orderby": "{sort}",
    "token": "{token}", "next_token": "{token}", "continuation": "{token}",
    "cursor": "{token}", "pagetoken": "{token}", "page_token": "{token}",
    "since": "{token}", "after": "{token}", "auth": "{token}",
    "id": "{id}", "itemid": "{id}", "pk": "{id}", "key": "{id}", "name": "{name}",
    "id_": "{id}", "node": "{id}",
}
FIELD_NAME_SLOTS = {
    "q": "{query}", "query": "{query}", "search": "{query}", "s": "{query}",
    "keyword": "{query}", "term": "{query}", "keywords": "{query}",
    "searchtext": "{query}", "find": "{query}", "searchquery": "{query}",
    "page": "{page}", "offset": "{page}", "start": "{page}", "p": "{page}",
    "email": "{email}", "e-mail": "{email}", "mail": "{email}",
    "user": "{user}", "username": "{user}", "login": "{user}", "handle": "{user}",
    "password": "{password}", "passwd": "{password}", "pwd": "{password}",
    "name": "{name}", "id": "{id}", "category": "{category}", "tag": "{category}",
    "token": "{token}", "message": "{text}", "comment": "{text}", "body": "{text}",
    "url": "{url}", "file": "{file}", "code": "{text}", "subject": "{text}",
}
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
HEX_RE = re.compile(r"^[0-9a-f]+$", re.I)
SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._~-]*$")


# ---------------------------------------------------------------------------
# 1. HTTP session with per-host rate limiting (prereg 6.1)
# ---------------------------------------------------------------------------

class RateLimitedSession:
    """Sequential-per-host session enforcing >=1.05s between requests per host.

    Thread-safe: hosts are fetched by different workers, but a given host is
    only ever handled by one worker at a time because each host is a unit of
    work.
    """

    def __init__(self):
        self._last: dict[str, float] = {}
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT, "Accept": ACCEPT})
        self.session.max_redirects = 5

    def _wait(self, host: str):
        now = time.monotonic()
        prev = self._last.get(host)
        if prev is not None:
            delta = now - prev
            if delta < PER_HOST_MIN_INTERVAL_S:
                time.sleep(PER_HOST_MIN_INTERVAL_S - delta)
        self._last[host] = time.monotonic()

    def get(self, url: str, stream_body: bool = True):
        host = urlsplit(url).netloc.lower()
        self._wait(host)
        t0 = time.perf_counter()
        try:
            resp = self.session.get(
                url,
                timeout=(CONNECT_TIMEOUT_S, READ_TIMEOUT_S),
                allow_redirects=True,
            )
            body = resp.content
            latency_ms = round((time.perf_counter() - t0) * 1000.0, 3)
            return {
                "url_requested": url,
                "url_final": resp.url,
                "status": resp.status_code,
                "headers": {k: v for k, v in resp.headers.items()},
                "body": body,
                "bytes": len(body),
                "latency_ms": latency_ms,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "redirects": [
                    {"status": h.status_code, "url": h.url, "location": h.headers.get("Location", "")}
                    for h in resp.history
                ],
                "error": None,
            }
        except Exception as exc:  # transport failure is evidence, not a result
            latency_ms = round((time.perf_counter() - t0) * 1000.0, 3)
            return {
                "url_requested": url,
                "url_final": None,
                "status": None,
                "headers": {},
                "body": b"",
                "bytes": 0,
                "latency_ms": latency_ms,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "redirects": [],
                "error": f"{type(exc).__name__}: {exc}",
            }


def make_robot_parser(session: RateLimitedSession, base_url: str, raw_out: list):
    """prereg 6.1/13: robots.txt is checked once per host before any request."""
    parts = urlsplit(base_url)
    robots_url = urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))
    rec = session.get(robots_url)
    raw_out.append(rec)
    rp = urllib.robotparser.RobotFileParser()
    if rec["status"] == 200 and rec["body"]:
        rp.parse(rec["body"].decode("utf-8", "replace").splitlines())
        rp.set_url(robots_url)
    else:
        rp.parse(["User-agent: *", "Allow: /"])  # 404/absent -> no restrictions
        rp.allow_all = True
        rp.disallow_all = False
    return rp, robots_url


# ---------------------------------------------------------------------------
# 2. URL templating with typed slots (prereg 6.2 parameterization rule, 7.1)
# ---------------------------------------------------------------------------

def slot_for_segment(seg: str) -> str:
    """Type one path segment into a typed slot."""
    if not seg:
        return ""
    if seg.isdigit():
        return "{id}"
    if UUID_RE.match(seg):
        return "{token}"
    if len(seg) >= 6 and HEX_RE.match(seg):
        return "{token}"
    if SLUG_RE.match(seg):
        return "{slug}"
    return "{slug}"  # percent-decoded, arbitrary text is still an identifier slot


def slot_for_query_param(name: str) -> str:
    n = unquote(name).strip().lower()
    return QUERY_PARAM_SLOTS.get(n, "{" + re.sub(r"[^a-z0-9_]+", "_", n) + "}")


def slot_for_field_name(name: str) -> str:
    n = unquote(name or "").strip().lower()
    if not n:
        return "{field}"
    return FIELD_NAME_SLOTS.get(n, "{" + re.sub(r"[^a-z0-9_]+", "_", n) + "}")


def url_template(abs_url: str) -> str | None:
    """Host-relative structural template of a URL with typed slots.

    Fragment, scheme and netloc are dropped: cross-site matching (prereg 7.2)
    must not be able to match on host identity.
    """
    if not abs_url:
        return None
    try:
        parts = urlsplit(abs_url)
    except ValueError:
        return None
    raw_path = parts.path or "/"
    try:
        segs = [unquote(s) for s in raw_path.split("/") if s]
    except Exception:
        segs = [s for s in raw_path.split("/") if s]
    if segs:
        path = "/" + "/".join(slot_for_segment(s) for s in segs)
    else:
        path = "/"
    qs = []
    try:
        pairs = parse_qsl(parts.query, keep_blank_values=True)
    except Exception:
        pairs = []
    for k, _v in pairs:
        qs.append(slot_for_query_param(k))
    query = "?" + "&".join(sorted(qs)) if qs else ""
    return path + query


def is_same_site(abs_url: str, base_url: str) -> bool:
    """Registered-domain match (prereg 13: publicsuffix2-based)."""
    try:
        import publicsuffix2
    except Exception:
        publicsuffix2 = None

    def reg(host: str) -> str:
        host = (host or "").lower().split(":")[0]
        if publicsuffix2 is not None:
            try:
                return publicsuffix2.get_sld(host)
            except Exception:
                pass
        parts = host.split(".")
        return ".".join(parts[-2:]) if len(parts) >= 2 else host

    a = reg(urlsplit(abs_url).netloc)
    b = reg(urlsplit(base_url).netloc)
    return bool(a) and a == b


def etld1(host: str):
    try:
        import publicsuffix2
        return publicsuffix2.get_sld(host)
    except Exception:
        parts = (host or "").lower().split(".")
        return ".".join(parts[-2:]) if len(parts) >= 2 else host


# ---------------------------------------------------------------------------
# 3. Link filtering and page discovery (prereg 5.3)
# ---------------------------------------------------------------------------

def link_candidate_ok(href: str, base_url: str) -> bool:
    if not href or href.startswith(("#", "javascript:", "mailto:", "tel:", "data:")):
        return False
    low = href.lower()
    if any(low.endswith(ext) or ext + "?" in low for ext in STATIC_EXTS):
        return False
    if any(tok in low for tok in EXCLUDE_LINK_TOKENS):
        return False
    try:
        parts = urlsplit(href)
    except ValueError:
        return False
    if parts.netloc and not is_same_site(href, base_url):
        return False
    return True


def absolutize(href: str, base_url: str) -> str | None:
    try:
        from urllib.parse import urljoin
        joined = urljoin(base_url, href)
    except Exception:
        return None
    return joined if joined.startswith(("http://", "https://")) else None


# ---------------------------------------------------------------------------
# 4. Structural representation: minimal (prereg 6.2 / 6.4)
# ---------------------------------------------------------------------------

def _attr(el, name):
    """Attribute accessor that normalizes bs4 multi-valued attribute lists."""
    v = el.get(name)
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        return " ".join(str(x) for x in v).strip()
    return str(v).strip()


def _own_link_templates(el, base_url, limit=200):
    """Ordered, host-restricted, de-duplicated URL templates of an element's links."""
    out, seen = [], set()
    for a in el.find_all("a", href=True):
        href = _attr(a, "href")
        if not link_candidate_ok(href or "", base_url):
            continue
        absu = absolutize(href, base_url)
        if not absu:
            continue
        t = url_template(absu)
        if t and t not in seen:
            seen.add(t)
            out.append(t)
            if len(out) >= limit:
                return out, True
    return out, False


def extract_forms(soup, base_url):
    forms = []
    for f in soup.find_all("form"):
        action = _attr(f, "action") or ""
        method = (_attr(f, "method") or "get").lower()
        abs_action = absolutize(action, base_url) if action else base_url
        tpl = url_template(abs_action) if abs_action else "/"
        fields = []
        for inp in f.find_all(["input", "select", "textarea"]):
            itype = (_attr(inp, "type") or inp.name or "text").lower()
            if itype in ("hidden",):
                continue
            fields.append({
                "name": slot_for_field_name(_attr(inp, "name") or ""),
                "type": itype,
                "required": inp.has_attr("required"),
            })
        fields.sort(key=lambda d: (d["name"], d["type"], d["required"]))
        forms.append({
            "action_template": tpl,
            "method": method,
            "fields": fields,
            "field_slots": sorted({d["name"] for d in fields}),
        })
    return forms


def extract_nav(soup, base_url):
    navs = []
    for tag in NAV_TAGS:
        for el in soup.find_all(tag):
            tpls, trunc = _own_link_templates(el, base_url)
            if not tpls:
                continue
            navs.append({
                "nav_type": tag,
                "link_templates": sorted(tpls),
                "n_links": len(tpls),
                "truncated": trunc,
            })
    for el in soup.find_all(attrs={"role": True}):
        role = (_attr(el, "role") or "").lower()
        if role in ("navigation", "banner", "contentinfo", "search", "menubar", "tablist", "toolbar", "tab"):
            tpls, trunc = _own_link_templates(el, base_url)
            if not tpls:
                continue
            navs.append({
                "nav_type": "role_" + role,
                "link_templates": sorted(tpls),
                "n_links": len(tpls),
                "truncated": trunc,
            })
    for a in soup.find_all("a", rel=True):
        rels = [r.lower() for r in (_attr(a, "rel") or "").split()]
        if not any(r in REL_PAGINATION for r in rels):
            continue
        absu = absolutize(_attr(a, "href") or "", base_url)
        t = url_template(absu) if absu else None
        if t:
            navs.append({
                "nav_type": "rel_" + "+".join(sorted(set(rels))),
                "link_templates": [t],
                "n_links": 1,
                "truncated": False,
            })
    for el in soup.find_all(attrs={"aria-label": True}):
        label = (_attr(el, "aria-label") or "").lower()
        if "breadcrumb" not in label:
            continue
        tpls, trunc = _own_link_templates(el, base_url)
        if tpls:
            navs.append({
                "nav_type": "breadcrumb",
                "link_templates": sorted(tpls),
                "n_links": len(tpls),
                "truncated": trunc,
            })
    return navs


def extract_lists(soup, base_url):
    lists = []
    containers = []
    for tag in ("ul", "ol"):
        containers.extend((tag, el) for el in soup.find_all(tag))
    for el in soup.find_all("table"):
        containers.append(("table", el))
    for el in soup.find_all(class_=True):
        try:
            children = [c for c in el.find_all(recursive=False) if c.name]
        except Exception:
            children = []
        if len(children) > 3:
            tags = [c.name for c in children]
            if len(set(tags)) <= max(1, len(tags) // 3):
                containers.append(("div-children", el))
    seen_ids = set()
    for ctype, el in containers:
        marker = id(el)
        if marker in seen_ids:
            continue
        seen_ids.add(marker)
        if ctype in ("ul", "ol"):
            kids = [li for li in el.find_all("li", recursive=False)]
        elif ctype == "table":
            rows = el.find_all("tr")
            kids = rows
        else:
            kids = [c for c in el.find_all(recursive=False) if c.name]
        kids = kids[:60]
        if len(kids) < 2:
            continue
        tmpl_counter = {}
        for kid in kids:
            t = None
            for a in kid.find_all("a", href=True):
                href = _attr(a, "href") or ""
                if not link_candidate_ok(href, base_url):
                    continue
                absu = absolutize(href, base_url)
                t = url_template(absu) if absu else None
                if t:
                    break
            if t is None:
                t = "<" + (kid.name or "node") + ">"
            tmpl_counter[t] = tmpl_counter.get(t, 0) + 1
        if tmpl_counter:
            best = sorted(tmpl_counter.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        else:
            best = "<" + (kids[0].name or "node") + ">"
        lists.append({
            "container_type": ctype,
            "item_template": best,
            "item_count": len(kids),
        })
    return lists


def extract_search(forms):
    """prereg 6.2.4: a form is a search form if it declares type=search or a
    search-like input name."""
    searches = []
    for f in forms:
        names = {d["name"] for d in f["fields"]}
        has_search_type = any(d["type"] == "search" for d in f["fields"])
        search_slots = {"{query}", "{q}", "{keyword}", "{term}",
                        "{searchtext}", "{find}", "{searchquery}"}
        has_search_name = any(
            n in search_slots or "search" in n or n in ("{q}", "{keyword}")
            for n in names
        )
        if not (has_search_type or has_search_name):
            continue
        typed = sorted(n for n in names if n in search_slots)
        searches.append({
            "action_template": f["action_template"],
            "param_name": typed[0] if typed else "|".join(sorted(names)) or None,
        })
    return searches


def extract_pagination(soup, base_url):
    pages = []
    for a in soup.find_all("a", href=True):
        href = _attr(a, "href") or ""
        rels = [r.lower() for r in ((_attr(a, "rel") or "").split())]
        absu = absolutize(href, base_url)
        if not absu:
            continue
        text = (a.get_text(" ", strip=True) or "").strip()
        is_pag = False
        param = None
        if any(r in REL_PAGINATION for r in rels):
            is_pag = True
        else:
            try:
                qs = dict(parse_qsl(urlsplit(absu).query, keep_blank_values=True))
            except Exception:
                qs = {}
            for k, v in qs.items():
                if k.lower() in PAGINATION_PARAMS:
                    is_pag = True
                    param = slot_for_query_param(k)
                    break
            if not is_pag and text and len(text) <= 12 and PAGINATION_TEXT_RE.fullmatch(text):
                is_pag = True
        if not is_pag:
            continue
        t = url_template(absu)
        if t:
            pages.append({"base_template": t, "param_name": param})
    if not pages:
        return []
    counter = {}
    for p in pages:
        counter[(p["base_template"], p["param_name"])] = counter.get((p["base_template"], p["param_name"]), 0) + 1
    best = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0][0], str(kv[0][1])))[0][0]
    return [{"base_template": best[0], "param_name": best[1]}]


def extract_details(soup, base_url):
    counter = {}
    for a in soup.find_all("a", href=True):
        href = _attr(a, "href") or ""
        if not link_candidate_ok(href, base_url):
            continue
        absu = absolutize(href, base_url)
        if not absu:
            continue
        try:
            segs = [unquote(s).lower() for s in urlsplit(absu).path.split("/") if s]
        except Exception:
            continue
        if not any(s in DETAIL_SEGMENTS for s in segs):
            continue
        t = url_template(absu)
        if t:
            counter[t] = counter.get(t, 0) + 1
    if not counter:
        return []
    # param_name may be None, so the tuple key must be compared component-wise.
    best = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0][0], str(kv[0][1])))[0][0]
    parts = best.split("?")
    segs = parts[0].split("/")
    list_tpl = "/".join(segs[:-1]) or "/"
    if len(parts) > 1:
        list_tpl = list_tpl + "?" + parts[1]
    return [{"list_template": list_tpl, "detail_template": best}]


def extract_actions(soup, base_url):
    actions = []
    for el in soup.find_all(["button", "input", "a"]):
        name = el.name
        if name == "button":
            atype = "button"
        elif name == "input" and (_attr(el, "type") or "").lower() in ("submit", "button", "image", "reset"):
            atype = "submit"
        elif name == "a" and ((_attr(el, "role") or "").lower() == "button" or any("btn" in (c or "").lower() for c in (el.get("class") or []))):
            atype = "a_btn"
        else:
            continue
        target = None
        if name == "button" and el.find_parent("form") is not None:
            form = el.find_parent("form")
            act = _attr(form, "action") or ""
            absu = absolutize(act, base_url) if act else base_url
            target = url_template(absu) if absu else "/"
        elif _attr(el, "formaction"):
            absu = absolutize(_attr(el, "formaction"), base_url)
            target = url_template(absu) if absu else None
        elif name == "a" and _attr(el, "href"):
            href = _attr(el, "href")
            if link_candidate_ok(href, base_url):
                absu = absolutize(href, base_url)
                target = url_template(absu) if absu else None
        actions.append({"action_type": atype, "target_template": target})
    dedup = {}
    for a in actions:
        dedup[(a["action_type"], a["target_template"])] = a
    return list(dedup.values())


# ---------------------------------------------------------------------------
# 5. Baseline representations (prereg 6.3)
# ---------------------------------------------------------------------------

def full_dom_serialized(soup) -> str:
    html = soup.find("html")
    node = html if html is not None else soup
    try:
        return node.decode(formatter="minimal")
    except Exception:
        return str(node)


def a11y_tree(soup) -> dict:
    """Accessibility-tree APPROXIMATION from semantic HTML + ARIA (prereg 6.3)."""
    nodes = []
    for el in soup.find_all(A11Y_SEMANTIC_TAGS):
        role = _attr(el, "role")
        aria = {}
        for k, v in (el.attrs or {}).items():
            if k.startswith("aria-"):
                aria[k] = v
        node = {
            "t": el.name,
            "role": role,
            "aria": aria,
            "href_t": url_template(absolutize(_attr(el, "href"), BASE_URL_HOLDER[0])) if el.name == "a" and _attr(el, "href") else None,
            "alt": _attr(el, "alt") if el.name == "img" else None,
            "lbl": _attr(el, "aria-label") or _attr(el, "title") or _attr(el, "placeholder"),
            "lvl": int(el.name[1]) if el.name in HEADING_TAGS else None,
            "dis": el.has_attr("disabled"),
            "req": el.has_attr("required"),
            "children": len([c for c in el.find_all(recursive=False) if c.name]),
        }
        nodes.append(node)
    return {"n": len(nodes), "nodes": nodes}


BASE_URL_HOLDER = [None]


# ---------------------------------------------------------------------------
# 6. Signatures (prereg 7.1)
# ---------------------------------------------------------------------------

def signatures_for_page(structures: dict) -> list[dict]:
    """Return [{type, key, slots, meta}] with the frozen 7 signature classes."""
    sigs = []
    for f in structures["forms"]:
        key = {
            "action_template": f["action_template"],
            "method": f["method"],
            "field_names": f["field_slots"],
        }
        sigs.append(_mk("form", key, (f["action_template"], f["method"], tuple(f["field_slots"]))))
    for n in structures["navs"]:
        key = {"nav_type": n["nav_type"], "link_templates": n["link_templates"]}
        sigs.append(_mk("nav", key, (n["nav_type"], tuple(n["link_templates"]))))
    for l in structures["lists"]:
        key = {"container_type": l["container_type"], "item_template": l["item_template"], "item_count": l["item_count"]}
        # prereg 7.2 matches on template structure; item_count is not a template
        # component, so it is carried as meta and excluded from matching.
        sigs.append(_mk("list", key, (l["container_type"], l["item_template"]), meta={"item_count": l["item_count"]}))
    for s in structures["searches"]:
        key = {"action_template": s["action_template"], "param_name": s["param_name"]}
        sigs.append(_mk("search", key, (s["action_template"], s["param_name"])))
    for p in structures["paginations"]:
        key = {"base_template": p["base_template"], "param_name": p["param_name"]}
        sigs.append(_mk("pagination", key, (p["base_template"], p["param_name"])))
    for d in structures["details"]:
        key = {"list_template": d["list_template"], "detail_template": d["detail_template"]}
        sigs.append(_mk("detail", key, (d["list_template"], d["detail_template"])))
    for a in structures["actions"]:
        key = {"action_type": a["action_type"], "target_template": a["target_template"]}
        sigs.append(_mk("action", key, (a["action_type"], a["target_template"])))
    return sigs


TYPED_SLOT_RE = re.compile(r"\{[a-z_][a-z0-9_]*\}")


def _mk(stype, key, match_tuple, meta=None):
    flat = json.dumps(key, sort_keys=True)
    slots = sorted(set(TYPED_SLOT_RE.findall(flat)))
    return {
        "type": stype,
        "key": key,
        "match": match_tuple,
        "slots": slots,
        "n_slots": len(slots),
        "meta": meta or {},
    }


def canonical_key(sig) -> str:
    return json.dumps([sig["type"], sig["match"]], sort_keys=True, default=list)


def slot_canonical_key(sig) -> str:
    """Key that additionally requires >=1 typed slot (alias-generalizable subset).

    NOT part of the frozen primary metric. Reported only as a labelled
    sensitivity, because the prereg's own construct (spec.baselines /
    spec.hypothesis: "varying identifiers (IDs, slugs, query params) can be
    parameterized to a common template") is not exercised by a template with
    zero typed slots.
    """
    return canonical_key(sig) if sig["n_slots"] > 0 else None


# ---------------------------------------------------------------------------
# 7. Matching, AGF, Jaccard (prereg 7.2, 7.3)
# ---------------------------------------------------------------------------

def signature_counts(site_sig_keys: list[str], keyfn=canonical_key) -> dict:
    counts = {}
    for s in site_sig_keys:
        k = keyfn(s)
        if k is None:
            continue
        counts[k] = counts.get(k, 0) + 1
    return counts


def agf_from_site_keymaps(site_keymaps: dict, sigs_per_site: dict, keyfn=canonical_key) -> dict:
    """Frozen prereg 7.3 primary metric.

    AGF = (total matched signatures across all eTLD+1 pairs) / (total signatures)
    Pair matches are counted with multiplicity: for signature key K present n_s
    times in site s, the number of matched instances between an unordered site
    pair is n_a * n_b.
    """
    numerator = 0
    for k, per_site in _key_site_counts(site_keymaps, sigs_per_site, keyfn).items():
        vals = list(per_site.values())
        total = sum(vals)
        sq = sum(v * v for v in vals)
        numerator += (total * total - sq) // 2
    denominator = sum(len(v) for v in sigs_per_site.values())
    agf = (numerator / denominator) if denominator else 0.0
    distinct_matched = sum(
        1 for per_site in _key_site_counts(site_keymaps, sigs_per_site, keyfn).values()
        if len(per_site) >= 2
    )
    return {
        "agf": agf,
        "matched_signature_instances": numerator,
        "total_signatures": denominator,
        "matched_distinct_keys": distinct_matched,
    }


def _key_site_counts(site_keymaps, sigs_per_site, keyfn):
    """key -> {site: count} for keys present in >= 2 sites."""
    out = {}
    for site, sigs in sigs_per_site.items():
        for sig in sigs:
            k = keyfn(sig) if not isinstance(sig, str) else keyfn(sig)
            if k is None:
                continue
            d = out.get(k)
            if d is None:
                d = {}
                out[k] = d
            d[site] = d.get(site, 0) + 1
    del site_keymaps
    return out


def pairwise_jaccard(sigs_per_site, keyfn=canonical_key) -> dict:
    """Frozen prereg 7.3 secondary metric: mean pairwise Jaccard of signature sets."""
    sets = {}
    for site, sigs in sigs_per_site.items():
        s = set()
        for sig in sigs:
            k = keyfn(sig) if not isinstance(sig, str) else keyfn(sig)
            if k is not None:
                s.add(k)
        sets[site] = s
    sites = sorted(sets)
    pairs = []
    for i in range(len(sites)):
        for j in range(i + 1, len(sites)):
            a, b = sets[sites[i]], sets[sites[j]]
            union = len(a | b)
            jac = (len(a & b) / union) if union else 0.0
            pairs.append({"a": sites[i], "b": sites[j], "jaccard": jac,
                          "shared": len(a & b), "union": union})
    vals = [p["jaccard"] for p in pairs] or [0.0]
    nonzero = [p for p in pairs if p["shared"] > 0]
    return {
        "n_pairs": len(pairs),
        "mean_jaccard": sum(vals) / len(vals),
        "max_jaccard": max(vals),
        "n_pairs_nonzero": len(nonzero),
        "pairs": pairs,
    }


def singleton_sites(sigs_per_site, keyfn=canonical_key) -> list:
    """NC-SINGLETON-SITE (spec.null_control): sites with no match to any other site."""
    counts = _key_site_counts(None, sigs_per_site, keyfn)
    shared_keys = {k for k, d in counts.items() if len(d) >= 2}
    out = []
    for site, sigs in sigs_per_site.items():
        touched = False
        for sig in sigs:
            k = keyfn(sig) if not isinstance(sig, str) else keyfn(sig)
            if k is not None and k in shared_keys:
                touched = True
                break
        if not touched:
            out.append(site)
    return sorted(out)


# ---------------------------------------------------------------------------
# 8. Tokenization and cost accounting (prereg 10)
# ---------------------------------------------------------------------------

_TOK = None


def tokenizer():
    global _TOK
    if _TOK is None:
        import tiktoken
        _TOK = tiktoken.get_encoding("cl100k_base")
    return _TOK


def ntok(text: str) -> int:
    return len(tokenizer().encode(text, disallowed_special=()))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def compact_json(obj) -> str:
    return json.dumps(obj, separators=(",", ":"), sort_keys=False, default=str)


def percentile(sorted_vals, q):
    if not sorted_vals:
        return None
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    pos = (len(sorted_vals) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = pos - lo
    return float(sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac)


def ci(samples, alpha=0.05):
    """Percentile bootstrap CI (prereg 9.3)."""
    s = sorted(samples)
    lo = percentile(s, alpha / 2.0)
    hi = percentile(s, 1.0 - alpha / 2.0)
    return {
        "ci_lower": lo,
        "ci_upper": hi,
        "ci_width": (hi - lo) if (lo is not None and hi is not None) else None,
        "n_replicates": len(s),
    }
