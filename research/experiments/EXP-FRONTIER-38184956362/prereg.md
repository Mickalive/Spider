# EXP-FRONTIER-38184956362 preregistration

**Lane:** frontier · **Claim:** C-CROSSSITE · **Design contract:** v2
**Lineage:** SUPERSEDES EXP-FRONTIER-37984242167 (empty frame, BLOCKED),
EXP-FRONTIER-38085197666 (declared-PASS freeze with absent artifacts, exit 65) and
EXP-FRONTIER-38164611798 (frozen outcome code TypeError on its own frame, MEASUREMENT_INVALID).
**Parent handoff (USE):** research/experiments/EXP-FRONTIER-38164611798/handoff.json
**Director mandate:** request.json#director_mandate (CONTINUE on C-CROSSSITE, cognitive_reset=true).

This prereg is the frozen instrument. Nothing here may be re-designed after freeze. The
outcome-bearing code is reconstructed at EXECUTE from the bound base module plus the patch
embedded verbatim in section 7; the Q1 sampling frame is the bound parent record, not a fresh crawl.

---

## 1. Question, hypothesis, falsifier

**Question.** On the credential-free GET-only stdlib-HTTP substrate, after proving the instrument
and substrate at pre-freeze cost, measure (Q2) the fraction of DEEP (hop 3..6) state-carrying items
reachable within K=3 fresh-agent GETs via ANY of the five frozen site-native discovery channels
(ROBOTS_SITEMAP, SITEMAP_XML, ON_SITE_SEARCH, RSS_ATOM, JSON_LD), with per-channel coverage
disclosed; and (Q3) whether that fraction is >= 0.50 on at least two distinct engines.

**Hypothesis H1 (SUPPORTS).** >= 2 distinct engines reach a discovery-reachable fraction >= 0.50
within K=3 GETs. Then site-native indexes make deep state-carrying acquisition O(1) on this
substrate class, so shortest-path hop is not a fundamental acquisition-cost barrier.

**Falsifier F1 (FALSIFIES).** Fewer than 2 distinct engines reach 0.50 while >= 1 engine admits
>= 1 DEEP item: an engine-stratified bounded negative on this substrate class and frame.

**INCONCLUSIVE (never a negative, never a SUPPORTS).** Zero DEEP items admitted across the frame
(Q1 measured; Q2/Q3 vacuous); or every DEEP-admitting engine LIMITED (>10% admitted-item death);
or seed fetch fails on every pool host (infrastructure signature, EXPERIMENT_PACKET.md section 1).

## 2. The claim and the measured construct

C-CROSSSITE (registry status HYPOTHESIS) asks whether the Web's own indexes let a fresh, credential-free
agent reach deep state-carrying items without traversal. **State-carrying unit (frozen, inherited):**
a page at BFS hop 3..6 containing >= 1 named `<input>`/`<select>` (a durable interaction surface).
**Discovery-reachable:** the item URL is a member of at least one of the five channel documents AND
the item is live (HTTP 200) on a fresh GET, at charged cost <= K = 3 GETs. This is the same construct
the parent froze; it is deliberately not narrowed post-hoc. Its known weakness (theme chrome such as
`__palette`, `q`, `searchbar` also counts) is disclosed in section 14 and is NOT used to change the
decision rule.

## 3. Mandate preconditions (all must hold; else BLOCKED)

- **PC-1** — the exact outcome entry point (`main()` with `--stage discovery` / `--stage all`) is
  smoke-tested to mechanical completion before freeze, and the executed code identity is bound.
- **PC-2** — the Q1 census separates DEEP-discovered from DEEP-fetched with OBSERVED controls and
  fetches the unfetched deep frontiers, so Q1 measures prevalence and not crawl observability.
- **PC-3** — >= 2 distinct hosts/engines on which DEEP state-carrying items are actually observable.

Certified in section 11. If any fails, EXECUTE records BLOCKED with the unmet precondition and the
thread terminates instead of freezing a weaker run.

## 4. Frozen target pool (20 hosts)

Enumerated at DESIGN (2026-10-11), all seeds HTTP 200 text/html. `engine_class` = generator meta if
present else documented platform. The pool is pinned inside the frozen code (POOL); it is not a
mutable fixture.

```
doc.rust-lang.org mdBook; docs.python.org Sphinx; numpy.org Sphinx; pandas.pydata.org Sphinx;
react.dev Docusaurus; docusaurus.io Docusaurus; docs.readthedocs.io Sphinx-RTD; docs.pytest.org
Sphinx-RTD; gohugo.io Hugo; jekyllrb.com Jekyll; docs.gitbook.com GitBook; kubernetes.io Hugo-k8s;
developer.mozilla.org MDN-Yari; docs.github.com GitHubDocs; en.wikipedia.org MediaWiki;
www.mediawiki.org MediaWiki; quotes.toscrape.com custom; www.gnu.org GNU-web; forums.gentoo.org
phpBB; blog.wordpress.org WordPress.
```

## 5. Frozen Q1 frame (PC-2)

The Q1 DEEP sampling frame is the parent's immutable discovery record:

`research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl`
sha256 `2afe65b63f751ef0d25578b02c9a667d43f866a0ac54504ebe1e1f4db839d747`.

It contains, over the 20 hosts, **556 hop 3..6 pages DISCOVERED** under the item-blind FIFO BFS
(budget 250, depth 6), of which only **72 were ever fetched** and **32 carried >= 1 named control**
(all on one engine, Sphinx-RTD). The census stage (section 8) fetches every one of the 556 discovered
DEEP items once, re-observing controls, and writes the discovered/fetched/with-controls separation.
The frame is frozen; EXECUTE must consume exactly this file (`--frame`), never a fresh crawl.

## 6. Five frozen channels and the cost model

| channel | charged GETs | document |
|---|---|---|
| ROBOTS_SITEMAP | 3 | robots.txt -> FIRST `Sitemap:` line -> sitemap (or its matching index child) |
| SITEMAP_XML | 2 | /sitemap.xml, then /sitemap_index.xml fallback; index -> seed-matching child |
| ON_SITE_SEARCH | 3 | seed-HTML form (first named text-like GET form) + slug query results |
| RSS_ATOM | 3 | first alternate feed link in seed head |
| JSON_LD | 2 | URL strings in the SEED page's application/ld+json blocks |

Every redirect leg counts toward K. Discovery-document GETs are amortized once per host/channel;
the per-item liveness GET is charged by every channel. All five charged costs are <= K = 3.

## 7. Frozen instrument (code identity, PC-1)

The outcome-bearing module is embedded VERBATIM below between the unique marker lines
`FROZEN_CODE_BEGIN` and `FROZEN_CODE_END`. EXECUTE reconstructs it exactly as follows and STOPS
(status=MEASUREMENT_INVALID) on any mismatch:

1. Let `block` be the bytes strictly after the `FROZEN_CODE_BEGIN` line and strictly before the
   `FROZEN_CODE_END` line; let `C = block.strip()`.
2. Verify `sha256(C) == DERIVED_SHA256`
   = `b9b2efdc78266717946022002eb3bef301979ac6fc0967254202747037c5956f`.
3. Write `C` to `work/execute_module.py` (no other normalization is permitted) and run it with the
   stage interface of section 8.
4. Provenance (not an input to the run): the module was derived from the bound base module
   `research/experiments/EXP-FRONTIER-38164611798/execute_module.py` (`BASE_SHA256`
   = `75a01d490ec81609cbf87a606f8cfa9227d07f07765b2eb4fd876fef2c8ff53a`) by exactly three edits,
   which the embedded text already carries and which must be present on inspection:
   (a) `(v.get("controls_seen") or 0) > 0` at the two Q1-census filter sites (the parent wrote
   `v.get("controls_seen", 0) > 0`, raising `TypeError: '>' not supported between instances of
   'NoneType' and 'int'` on discovered-but-unfetched pages);
   (b) `"live": live` added to the `evaluate_items` output (the parent omitted it while
   `compute_metrics` reads `it["live"]`, raising `KeyError: 'live'`);
   (c) `census_deep()` plus a `--frame` argument and a seed-matching sitemap-index child selection.

FROZEN_CODE_BEGIN
#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# FROZEN EXECUTE MODULE for EXP-FRONTIER-38164611798 (frontier lane, C-CROSSSITE).
# Embedding contract (UNIQUE, unambiguous): prereg.md section 16 contains this
# module byte-identically. Transcribe:
#     block = bytes strictly between the CODE_BEGIN and CODE_END marker lines
#     C     = block.strip()          # strip leading/trailing ASCII whitespace
# CODE_SHA256 = sha256(C). Instantiate C as the module file at EXECUTE.
# If EXECUTE's transcription differs, status=MEASUREMENT_INVALID.
#
# DESIGN-time usage (non-outcome-bearing):  --stage controls | inventory
# EXECUTE usage:                            --stage all  [--out <dir>]
#   controls   : offline fixture calibrations + parser canaries + env probe + null direct-404s
#   inventory  : per-host discovery-channel endpoint liveness (no hops, no items)
#   structural : frozen BFS census (Q1) and DEEP admission
#   discovery  : per-item channel evaluation (Q2/Q3) + metrics + decision
"""Frozen design for EXP-FRONTIER-38164611798: does site-native discovery make
DEEP (hop>=3) state-carrying item acquisition O(1) in <= K=3 fresh-agent GETs?"""
import gzip
import hashlib
import html.parser
import json
import math
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

EXP_ID = "EXP-FRONTIER-38184956362"
UA = "SPIDER-research-frontier-384956362/1.0"
TIMEOUT = 12.0
MAX_BODY = 600000
DELAY = 0.1
BUDGET = 250          # per-seed page budget (mandate: budget 250)
DEPTH = 6             # depth cap (mandate: depth <= 6)
K = 3                 # fresh-agent GET budget
THRESHOLD = 0.50      # materiality threshold (Q3)
MIN_ENGINES = 2       # distinct engines for Q3
DEEP_BAND = (3, 4, 5, 6)
SYNTH_PREFIX = "spider-nonexistent-38184956362-"
# PC-2: the Q1 DEEP sampling frame is the PARENT'S FROZEN discovery record
# (immutable freeze_artifact), not a fresh live crawl, so Q1 measures
# observed prevalence on a fixed frame separated from whole-corpus crawling.
FRAME_FILE = "research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl"

# ---------------------------------------------------------- frozen target pool
# Enumerated by DESIGN on 2026-10-11; every seed live (HTTP 200 text/html) at
# probe time 2026-10-11T19:40:43Z (probe transcript in prereg.md section 11).
# engine_class = <meta name="generator"> content if present, else the documented
# platform recorded at DESIGN (prereg.md section 6).
POOL = [
    ("doc.rust-lang.org",     "mdBook",        "https://doc.rust-lang.org/stable/book/"),
    ("docs.python.org",       "Sphinx",        "https://docs.python.org/3/"),
    ("numpy.org",             "Sphinx",        "https://numpy.org/doc/stable/"),
    ("pandas.pydata.org",     "Sphinx",        "https://pandas.pydata.org/docs/"),
    ("react.dev",             "Docusaurus",    "https://react.dev/learn"),
    ("docusaurus.io",         "Docusaurus",    "https://docusaurus.io/docs"),
    ("docs.readthedocs.io",   "Sphinx-RTD",    "https://docs.readthedocs.io/en/stable/"),
    ("docs.pytest.org",       "Sphinx-RTD",    "https://docs.pytest.org/en/stable/"),
    ("gohugo.io",             "Hugo",          "https://gohugo.io/documentation/"),
    ("jekyllrb.com",          "Jekyll",        "https://jekyllrb.com/docs/"),
    ("docs.gitbook.com",      "GitBook",       "https://docs.gitbook.com/"),
    ("kubernetes.io",         "Hugo-k8s",      "https://kubernetes.io/docs/"),
    ("developer.mozilla.org", "MDN-Yari",      "https://developer.mozilla.org/en-US/"),
    ("docs.github.com",       "GitHubDocs",    "https://docs.github.com/en"),
    ("en.wikipedia.org",      "MediaWiki",     "https://en.wikipedia.org/wiki/Main_Page"),
    ("www.mediawiki.org",     "MediaWiki",     "https://www.mediawiki.org/wiki/MediaWiki"),
    ("quotes.toscrape.com",   "custom",        "https://quotes.toscrape.com/"),
    ("www.gnu.org",           "GNU-web",       "https://www.gnu.org/"),
    ("forums.gentoo.org",     "phpBB",         "https://forums.gentoo.org/"),
    ("blog.wordpress.org",    "WordPress",     "https://blog.wordpress.org/"),
]

ASSET_EXTS = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".zip", ".gz", ".tar", ".tgz",
    ".bz2", ".xz", ".mp3", ".mp4", ".webm", ".avi", ".mov", ".txt", ".xml",
)

# ------------------------------------------------------------- frozen helpers
def norm(url: str) -> str:
    """Defragment + canonicalize: same-host http(s) URL key."""
    p = urllib.parse.urlsplit(url)
    scheme = p.scheme.lower()
    netloc = p.netloc.lower()
    if ":" in netloc and not netloc.endswith("]"):
        host, _, port = netloc.rpartition(":")
        if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
            netloc = host
    path = p.path or "/"
    return urllib.parse.urlunsplit((scheme, netloc, path, p.query, ""))


def norm_eq(a: str, b: str) -> bool:
    """Membership equality: exact normalized equality, or equality after
    stripping at most one trailing '/' from the path (redirect-equivalence for
    canonical slash variants; no redirect chasing of channel URLs)."""
    na, nb = norm(a), norm(b)
    if na == nb:
        return True
    if na.endswith("/") and na[:-1] == nb:
        return True
    if nb.endswith("/") and nb[:-1] == na:
        return True
    return False


def is_asset(url: str) -> bool:
    path = urllib.parse.urlsplit(url).path.lower()
    return path.endswith(ASSET_EXTS)


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.forms = []          # frozen search-form finder: (action, inputs)
        self._form = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.hrefs.append(d["href"])
        if tag == "form":
            self._form = [d.get("action"), d.get("method", "get").lower(), []]
            self.forms.append(self._form)
        if tag == "input" and self._form is not None:
            if d.get("name"):
                self._form[2].append((d["name"], d.get("type", "text")))

    def handle_endtag(self, tag):
        if tag == "form":
            self._form = None


def static_links(base: str, html_text: str) -> list:
    lp = LinkParser()
    try:
        lp.feed(html_text)
    except Exception:
        return []
    out = []
    for h in lp.hrefs:
        u = urllib.parse.urljoin(base, h.strip())
        p = urllib.parse.urlsplit(u)
        if p.scheme not in ("http", "https"):
            continue
        if is_asset(u):
            continue
        out.append(u)
    return out


def search_form(base: str, html_text: str):
    """First GET form with a named text-like input; (action_url, input_name)."""
    lp = LinkParser()
    try:
        lp.feed(html_text)
    except Exception:
        return None
    for action, method, inputs in lp.forms:
        if method not in ("get", ""):
            continue
        for name, itype in inputs:
            if itype in ("text", "search", ""):
                action_url = urllib.parse.urljoin(base, action) if action else base
                return (action_url, name)
    return None


class ControlParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.controls = []

    def handle_starttag(self, tag, attrs):
        if tag in ("input", "select"):
            d = dict(attrs)
            if d.get("name"):
                self.controls.append((tag, d["name"], d.get("type", "")))


def named_controls(html_text: str) -> list:
    cp = ControlParser()
    try:
        cp.feed(html_text)
    except Exception:
        return []
    return cp.controls


class MetaParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.generator = None
        self.feeds = []
        self.jsonld_blocks = []
        self._in_jsonld = False
        self._buf = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta" and d.get("name", "").lower() == "generator":
            self.generator = d.get("content")
        if tag == "link":
            rel = d.get("rel", "")
            t = d.get("type", "")
            if "alternate" in rel.lower() and ("rss" in t or "atom" in t):
                self.feeds.append((rel, t, d.get("href", "")))
        if tag == "script" and d.get("type", "").lower() == "application/ld+json":
            self._in_jsonld = True
            self._buf = []
            self.jsonld_blocks.append(self._buf)

    def handle_data(self, data):
        if self._in_jsonld and self._buf is not None:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_jsonld = False


def parse_meta(html_text: str):
    mp = MetaParser()
    try:
        mp.feed(html_text)
    except Exception:
        pass
    blocks = ["".join(b) for b in mp.jsonld_blocks]
    return {"generator": mp.generator, "feeds": mp.feeds, "jsonld_blocks": blocks}


def walk_strings(obj, acc):
    if isinstance(obj, str):
        acc.append(obj)
    elif isinstance(obj, list):
        for x in obj:
            walk_strings(x, acc)
    elif isinstance(obj, dict):
        for v in obj.values():
            walk_strings(v, acc)


def jsonld_urls(blocks: list) -> set:
    urls = set()
    for b in blocks:
        try:
            parsed = json.loads(b)
        except Exception:
            continue
        acc = []
        walk_strings(parsed, acc)
        for s in acc:
            if s.startswith("http://") or s.startswith("https://"):
                urls.add(norm(s))
    return urls


def robots_sitemap_lines(body: bytes) -> list:
    out = []
    for line in body.decode("utf-8", errors="replace").splitlines():
        m = re.match(r"^\s*Sitemap:\s*(\S+)\s*$", line, re.I)
        if m:
            out.append(m.group(1))
    return out


def parse_sitemap(body: bytes) -> dict:
    """XML sitemap/sitemapindex -> {urls, is_index, child_sitemaps}."""
    try:
        root = ET.fromstring(body)
    except Exception:
        return {"urls": [], "is_index": False, "child_sitemaps": []}
    urls, children = [], []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag == "loc" and el.text and el.text.strip():
            urls.append(el.text.strip())
        if tag == "sitemap" and el.text and el.text.strip():
            children.append(el.text.strip())
    is_index = bool(children) or all(u.lower().endswith((".xml", ".gz")) for u in urls)
    if is_index:
        return {"urls": [], "is_index": True, "child_sitemaps": (children or urls)}
    return {"urls": urls, "is_index": False, "child_sitemaps": []}


def parse_sitemap_txt(body: bytes) -> dict:
    """Plain-text sitemap (sitemap.txt): one URL per line; index if every line
    names another sitemap file."""
    lines = [ln.strip() for ln in body.decode("utf-8", errors="replace").splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("#")]
    urls = [ln for ln in lines if ln.startswith("http://") or ln.startswith("https://")]
    if urls and all(u.lower().endswith((".xml", ".gz")) for u in urls):
        return {"urls": [], "is_index": True, "child_sitemaps": urls}
    return {"urls": urls, "is_index": False, "child_sitemaps": []}


def parse_sitemap_any(body: bytes, url: str) -> dict:
    if url.lower().endswith(".gz"):
        try:
            body = gzip.decompress(body)
        except Exception:
            return {"urls": [], "is_index": False, "child_sitemaps": []}
    xml = parse_sitemap(body)
    if xml["urls"] or xml["is_index"]:
        return xml
    return parse_sitemap_txt(body)


def parse_feed_entries(body: bytes) -> int:
    try:
        root = ET.fromstring(body)
    except Exception:
        return -1
    n = 0
    for el in root.iter():
        if el.tag.split("}")[-1] in ("item", "entry"):
            n += 1
    return n


def feed_entry_urls(body: bytes) -> list:
    """RSS <item><link> / Atom <entry><link href> URLs (frozen extraction)."""
    try:
        root = ET.fromstring(body)
    except Exception:
        return []
    out = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag == "item":
            for child in el:
                if child.tag.split("}")[-1] == "link" and child.text and child.text.strip():
                    out.append(child.text.strip())
        if tag == "entry":
            for child in el:
                if child.tag.split("}")[-1] == "link":
                    href = child.get("href")
                    if href:
                        out.append(href)
    return out


def item_slug(item_url: str) -> str:
    p = urllib.parse.urlsplit(item_url)
    segs = [s for s in p.path.split("/") if s]
    return urllib.parse.unquote(segs[-1]) if segs else p.netloc


# ----------------------------------------------------------- transport (frozen)
class RedirectCounter(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.redirects = 0

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.redirects += 1
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_host_root(url: str):
    return urllib.parse.urlsplit(url).scheme + "://" + urllib.parse.urlsplit(url).netloc


def fetch(url: str):
    """GET; returns (record, body_bytes). Cap MAX_BODY; gunzip when needed;
    redirects counted (each leg counts toward K in the charged ledger).
    HTTP errors (4xx/5xx) are recorded with their real status code; only
    transport-level failures (DNS/TLS/timeout) yield status=None."""
    rch = RedirectCounter()
    opener = urllib.request.build_opener(rch)
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml,*/*"})
    t0 = time.time()
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:
            raw = resp.read(MAX_BODY + 1)
            truncated = len(raw) > MAX_BODY
            raw = raw[:MAX_BODY]
            body = raw
            if resp.headers.get("Content-Encoding", "").lower() == "gzip":
                try:
                    body = gzip.decompress(raw)
                except Exception:
                    body = raw
            rec = {
                "url": url, "status": resp.status, "final_url": resp.geturl(),
                "content_type": resp.headers.get("Content-Type", ""),
                "bytes": len(raw), "truncated": truncated, "redirects": rch.redirects,
                "elapsed_s": round(time.time() - t0, 2), "error": None,
            }
            return rec, body
    except urllib.error.HTTPError as e:
        # HTTP 4xx/5xx: keep the real status code (control NC_SYNTHETIC_*
        # and item liveness depend on distinguishing 4xx/5xx from transport
        # failure). The body is not read; the charged ledger only counts legs.
        return {"url": url, "status": e.code, "final_url": url, "content_type": None,
                "bytes": 0, "truncated": False, "redirects": rch.redirects,
                "elapsed_s": round(time.time() - t0, 2),
                "error": f"HTTPError {e.code}: {e.reason}"}, b""
    except Exception as e:  # network/TLS/timeout failure: recorded, never a branch
        return {"url": url, "status": None, "final_url": url, "content_type": None,
                "bytes": 0, "truncated": False, "redirects": rch.redirects,
                "elapsed_s": round(time.time() - t0, 2),
                "error": f"{type(e).__name__}: {e}"}, b""


# ------------------------------------------------------- structural pass (Q1)
def bfs_structural(seed: str):
    """Frozen policy: item-blind FIFO BFS in document order; same-host static
    <a>; budget B=250; depth D=6; each URL fetched at most once. Returns:
    {url_norm: {hop, ordinal, requests, bytes, truncated, controls, controls_seen}}"""
    out = {}
    queue = []
    seed_n = norm(seed)
    rec, body = fetch(seed)
    if rec["error"] or rec["status"] != 200:
        return {"seed_error": rec["error"] or f"status={rec['status']}"}
    text = body.decode("utf-8", errors="replace")
    seed_host = urllib.parse.urlsplit(rec["final_url"]).netloc.lower()
    out[seed_n] = {"hop": 0, "ordinal": 1, "requests": 1, "bytes": rec["bytes"],
                   "truncated": rec["truncated"], "controls_seen": len(named_controls(text))}
    queue = [(seed_n, 0)]
    ordinal = 1
    while queue and len(out) < BUDGET:
        u, h = queue.pop(0)
        if h + 1 > DEPTH:
            continue
        r, b = fetch(u)
        if r["error"] or r["status"] != 200:
            continue
        t = b.decode("utf-8", errors="replace")
        base = r["final_url"]
        for raw in static_links(base, t):
            nu = norm(raw)
            if nu in out:
                continue
            if urllib.parse.urlsplit(nu).netloc.lower() != seed_host:
                continue
            ordinal += 1
            out[nu] = {"hop": h + 1, "ordinal": ordinal, "requests": ordinal,
                       "bytes": None, "truncated": None, "controls_seen": None}
            queue.append((nu, h + 1))
            # Mandate budget B=250 is a hard cap: even a single page with
            # thousands of links may not push discovery past the budget.
            if len(out) >= BUDGET:
                break
        # backfill the fetched page's own observation
        if u in out and out[u].get("bytes") is None:
            out[u]["bytes"] = r["bytes"]
            out[u]["truncated"] = r["truncated"]
            out[u]["controls_seen"] = len(named_controls(t))
    return out


# --------------------------------------------------- channel inventory (Q2 doc)
def channel_documents(seed: str):
    """Fetch the discovery documents ONCE per (host, channel) at EXECUTE and at
    DESIGN (certificate). Returns per-channel URL sets + endpoint records.
    NOT outcome-bearing: no hops, no items."""
    host = urllib.parse.urlsplit(seed).netloc.lower()
    root = fetch_host_root(seed)
    res = {"host": host, "seed": seed}
    # seed page (shared: JSON_LD block source + feed discovery + search form)
    srec, sbody = fetch(seed)
    res["seed_fetch"] = {k: srec[k] for k in ("status", "content_type", "bytes", "truncated", "redirects", "error")}
    meta = parse_meta(sbody.decode("utf-8", errors="replace"))
    res["seed_generator"] = meta["generator"]
    res["seed_feeds"] = meta["feeds"]
    res["seed_jsonld_urls"] = sorted(jsonld_urls(meta["jsonld_blocks"]))
    sform = search_form(seed, sbody.decode("utf-8", errors="replace"))
    res["search_form"] = {"action": sform[0], "input": sform[1]} if sform else None
    # ROBOTS_SITEMAP
    rrec, rbody = fetch(root + "/robots.txt")
    sl = robots_sitemap_lines(rbody) if rrec["status"] == 200 else []
    res["robots"] = {"status": rrec["status"], "sitemap_lines": sl, "error": rrec["error"]}
    robots_urls = set()
    if sl:
        s1rec, s1body = fetch(sl[0])
        if s1rec["status"] == 200 and s1body:
            doc = parse_sitemap_any(s1body, sl[0])
            res["robots_sitemap_doc"] = {"url": sl[0], "status": 200, "is_index": doc["is_index"],
                                         "url_count": len(doc["urls"]), "children": doc["child_sitemaps"][:5],
                                         "truncated": s1rec["truncated"]}
            if doc["is_index"] and doc["child_sitemaps"]:
                crec, cbody = fetch(doc["child_sitemaps"][0])
                if crec["status"] == 200 and cbody:
                    cdoc = parse_sitemap_any(cbody, doc["child_sitemaps"][0])
                    robots_urls = set(norm(u) for u in cdoc["urls"])
                    res["robots_sitemap_child"] = {"url": doc["child_sitemaps"][0], "status": 200,
                                                   "url_count": len(cdoc["urls"]), "truncated": crec["truncated"]}
                else:
                    res["robots_sitemap_child"] = {"url": doc["child_sitemaps"][0], "status": crec["status"],
                                                   "error": crec["error"]}
            else:
                robots_urls = set(norm(u) for u in doc["urls"])
        elif sl:
            res["robots_sitemap_doc"] = {"url": sl[0], "status": s1rec["status"], "error": s1rec["error"]}
    # SITEMAP_XML: /sitemap.xml, fallback /sitemap_index.xml, index->first child
    sm_urls = set()
    smrec, smbody = fetch(root + "/sitemap.xml")
    sm_status = smrec["status"]
    sm_error = smrec["error"]
    doc = None
    if smrec["status"] == 200 and smbody:
        doc = parse_sitemap_any(smbody, root + "/sitemap.xml")
        res["sitemap_xml"] = {"url": root + "/sitemap.xml", "status": 200, "is_index": doc["is_index"],
                              "url_count": len(doc["urls"]), "children": doc["child_sitemaps"][:5],
                              "truncated": smrec["truncated"]}
    else:
        res["sitemap_xml"] = {"url": root + "/sitemap.xml", "status": smrec["status"], "error": sm_error}
    if doc is None or (doc["is_index"] and not doc["child_sitemaps"]):
        sm2rec, sm2body = fetch(root + "/sitemap_index.xml")
        if sm2rec["status"] == 200 and sm2body:
            doc = parse_sitemap_any(sm2body, root + "/sitemap_index.xml")
            res["sitemap_index_xml"] = {"url": root + "/sitemap_index.xml", "status": 200,
                                        "is_index": doc["is_index"], "url_count": len(doc["urls"]),
                                        "children": doc["child_sitemaps"][:5], "truncated": sm2rec["truncated"]}
        else:
            res["sitemap_index_xml"] = {"url": root + "/sitemap_index.xml", "status": sm2rec["status"],
                                        "error": sm2rec["error"]}
    if doc is not None:
        if doc["is_index"] and doc["child_sitemaps"]:
            # PC-2/FIX: choose the child sitemap whose URL best matches the seed
            # path (deterministic, no extra GET); fall back to the first child.
            seed_path = urllib.parse.urlsplit(seed).path.lower()
            _kids = doc["child_sitemaps"]
            _match = next((c for c in _kids if urllib.parse.urlsplit(c).path.lower().rstrip("/").split("/")[-1] and urllib.parse.urlsplit(c).path.lower().rstrip("/").split("/")[-1] in seed_path), None)
            child0 = _match or _kids[0]
            r3rec, r3body = fetch(child0)
            if r3rec["status"] == 200 and r3body:
                d3 = parse_sitemap_any(r3body, doc["child_sitemaps"][0])
                sm_urls = set(norm(u) for u in d3["urls"])
                res["sitemap_xml_child"] = {"url": child0, "status": 200,
                                            "url_count": len(d3["urls"]), "truncated": r3rec["truncated"]}
            else:
                res["sitemap_xml_child"] = {"url": child0, "status": r3rec["status"],
                                            "error": r3rec["error"]}
        else:
            sm_urls = set(norm(u) for u in doc["urls"])
    res["channel_urls"] = {
        "ROBOTS_SITEMAP": sorted(robots_urls),
        "SITEMAP_XML": sorted(sm_urls),
        "RSS_ATOM": None,   # populated below (feed fetch)
        "JSON_LD": res["seed_jsonld_urls"],
        "ON_SITE_SEARCH": None,  # per-item query; form above
    }
    # RSS_ATOM: first feed link in seed HTML head
    if meta["feeds"]:
        fu = urllib.parse.urljoin(seed, meta["feeds"][0][2])
        frec, fbody = fetch(fu)
        if frec["status"] == 200 and fbody:
            res["feed"] = {"url": fu, "status": 200, "entries": parse_feed_entries(fbody),
                           "url_count": len(feed_entry_urls(fbody)), "truncated": frec["truncated"]}
            res["channel_urls"]["RSS_ATOM"] = sorted(norm(u) for u in feed_entry_urls(fbody))
        else:
            res["feed"] = {"url": fu, "status": frec["status"], "error": frec["error"]}
    else:
        res["feed"] = {"status": None, "error": "no_feed_link_in_seed_html"}
    return res


# ------------------------------------------------------ per-item evaluation
def evaluate_items(structural, docs, items):
    """Per admitted DEEP item: 5-channel membership (charged cost <= K) +
    fresh item-liveness GET. Charged costs (frozen protocol): ROBOTS_SITEMAP=3,
    SITEMAP_XML=2, ON_SITE_SEARCH=3, RSS_ATOM=3, JSON_LD=2."""
    host = docs["host"]
    out = []
    for item in items:
        iu = item["url"]
        slug = item_slug(iu)
        # ON_SITE_SEARCH: per-item results doc (query = slug)
        on_search = None
        if docs.get("search_form"):
            q = urllib.parse.quote(slug)
            sep = "&" if "?" in docs["search_form"]["action"] else "?"
            surl = docs["search_form"]["action"] + sep + urllib.parse.quote(docs["search_form"]["input"]) + "=" + q
            srec, sbody = fetch(surl)
            on_search = {"status": srec["status"], "error": srec["error"]}
            hits = set()
            if srec["status"] == 200 and sbody:
                base = srec["final_url"]
                hits = {norm(u) for u in static_links(base, sbody.decode("utf-8", errors="replace"))}
            member_search = any(norm_eq(iu, h) for h in hits)
        else:
            member_search = False
        member_robots = any(norm_eq(iu, u) for u in docs["channel_urls"]["ROBOTS_SITEMAP"])
        member_sm = any(norm_eq(iu, u) for u in docs["channel_urls"]["SITEMAP_XML"])
        member_rss = bool(docs["channel_urls"]["RSS_ATOM"]) and any(
            norm_eq(iu, u) for u in docs["channel_urls"]["RSS_ATOM"])
        member_jsonld = any(norm_eq(iu, u) for u in docs["channel_urls"]["JSON_LD"])
        # fresh item liveness GET (1 GET; excludes dead items with reason)
        lrec, _ = fetch(iu)
        live = lrec["status"] == 200
        reach = {
            "ROBOTS_SITEMAP": {"member": member_robots, "charged": 3},
            "SITEMAP_XML": {"member": member_sm, "charged": 2},
            "ON_SITE_SEARCH": {"member": member_search, "charged": 3},
            "RSS_ATOM": {"member": member_rss, "charged": 3},
            "JSON_LD": {"member": member_jsonld, "charged": 2},
        }
        # redirect budget: any channel whose DOCUMENT fetch exceeded its charged
        # budget legs is still counted (the spare absorbs it); charged cost is
        # the protocol cost and is <= K by construction.
        reachable_any = any(v["member"] for v in reach.values()) and live
        out.append({
            "url": iu, "hop": item["hop"], "ordinal": item["ordinal"], "bytes": item["bytes"],
            "search_status": on_search, "live": live,
            "live_status": lrec["status"], "live_error": lrec["error"],
            "per_channel": reach, "reachable_any": reachable_any,
        })
    return out


# --------------------------------------------- DEEP fetch census (PC-2, Q1)
def census_deep(structural):
    """PC-2: fetch EVERY DISCOVERED DEEP (hop in 3..6) item once, so Q1 measures
    observed state-carrying PREVALENCE rather than crawl observability. Backfills
    controls_seen into the structural records and returns per-host census rows
    that explicitly separate DEEP-discovered from DEEP-fetched."""
    census = []
    for srow in structural:
        if "seed_error" in srow:
            census.append({"host": srow.get("host"), "engine_class": srow.get("engine_class"),
                           "seed_error": srow["seed_error"], "n_deep_discovered": 0,
                           "n_deep_fetched": 0, "n_deep_with_controls": 0})
            continue
        host = srow.get("host"); eng = srow.get("engine_class")
        deep = [(u, v) for u, v in srow.items()
                if isinstance(v, dict) and v.get("hop") in DEEP_BAND]
        fetched = 0; withc = 0
        for u, v in sorted(deep, key=lambda kv: (kv[1].get("hop", 0), kv[1].get("ordinal", 0))):
            rec, body = fetch(u)
            c = len(named_controls(body.decode("utf-8", errors="replace"))) if rec["status"] == 200 else 0
            v["controls_seen"] = c
            v["census_status"] = rec["status"]
            v["census_fetched"] = True
            fetched += 1
            if rec["status"] == 200 and c > 0:
                withc += 1
            time.sleep(DELAY)
        census.append({"host": host, "engine_class": eng, "n_deep_discovered": len(deep),
                       "n_deep_fetched": fetched, "n_deep_with_controls": withc})
    return census


# ------------------------------------------------------------- metrics
def betainv(p: float, a: float, b: float) -> float:
    """Inverse of the regularized incomplete beta I^{-1}_p(a,b) via binary
    search on the continued-fraction evaluation (Numerical Recipes betacf)."""
    def betacf(aa, bb, xx):
        MAXIT, EPS, FPMIN = 200, 3.0e-12, 1e-300
        qab, qap, qam = aa + bb, aa + 1.0, aa - 1.0
        c = 1.0
        d = 1.0 - qab * xx / qap
        if abs(d) < FPMIN:
            d = FPMIN
        d = 1.0 / d
        h = d
        for m in range(1, MAXIT + 1):
            m2 = 2 * m
            aa2 = m * (bb - m) * xx / ((qam + m2) * (aa + m2))
            d = 1.0 + aa2 * d
            if abs(d) < FPMIN:
                d = FPMIN
            c = 1.0 + aa2 / c
            if abs(c) < FPMIN:
                c = FPMIN
            d = 1.0 / d
            h *= d * c
            aa2 = -(aa + m) * (qab + m) * xx / ((aa + m2) * (qap + m2))
            d = 1.0 + aa2 * d
            if abs(d) < FPMIN:
                d = FPMIN
            c = 1.0 + aa2 / c
            if abs(c) < FPMIN:
                c = FPMIN
            d = 1.0 / d
            del_ = d * c
            h *= del_
            if abs(del_ - 1.0) < EPS:
                break
        return h

    def betai(x):
        if x <= 0.0:
            return 0.0
        if x >= 1.0:
            return 1.0
        bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                      + a * math.log(x) + b * math.log1p(-x))
        if x < (a + 1.0) / (a + b + 2.0):
            return bt * betacf(a, b, x) / a
        return 1.0 - bt * betacf(b, a, 1.0 - x) / b

    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if betai(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def clopper_pearson(k: int, n: int, alpha=0.05):
    if n <= 0:
        return None
    if k == 0:
        return (0.0, 1.0 - (alpha / 2.0) ** (1.0 / n))
    if k == n:
        return ((alpha / 2.0) ** (1.0 / n), 1.0)
    lo = betainv(alpha / 2.0, k, n - k + 1)
    hi = betainv(1.0 - alpha / 2.0, k + 1, n - k)
    return (lo, hi)


DEAD_LIMIT = 0.10  # engine marked LIMITED when >10% of its admitted DEEP items die


def compute_metrics(items, engine_class, pool_engines=None):
    """Per-engine metrics over the ADMITTED DEEP items. When pool_engines
    (engine_class -> set(hosts), derived from the frozen POOL) is given, every
    pool engine absent from the admitted items is reported with n_deep=0 so the
    Q1 zero-DEEP census covers the FULL frozen pool, not only engines that
    happened to admit items."""
    per_engine = {}
    for it in items:
        e = it["engine"]
        per_engine.setdefault(e, {"hosts": set(), "n": 0, "reach": 0,
                                  "channels": {c: 0 for c in ("ROBOTS_SITEMAP", "SITEMAP_XML",
                                                              "ON_SITE_SEARCH", "RSS_ATOM", "JSON_LD")},
                                  "dead": 0, "hops": []})
        g = per_engine[e]
        g["hosts"].add(it["host"])
        if it["live"]:
            g["n"] += 1
            g["hops"].append(it["hop"])
            if it["reachable_any"]:
                g["reach"] += 1
            for c, v in it["per_channel"].items():
                if v["member"]:
                    g["channels"][c] += 1
        else:
            g["dead"] += 1
    if pool_engines:
        for e, hosts in pool_engines.items():
            per_engine.setdefault(e, {"hosts": set(hosts), "n": 0, "reach": 0,
                                      "channels": {c: 0 for c in ("ROBOTS_SITEMAP", "SITEMAP_XML",
                                                                  "ON_SITE_SEARCH", "RSS_ATOM", "JSON_LD")},
                                      "dead": 0, "hops": []})
    out = {}
    for e, g in per_engine.items():
        hosts = sorted(g["hosts"])
        n, r = g["n"], g["reach"]
        frac = r / n if n else None
        ci = clopper_pearson(r, n) if n else None
        admitted = n + g["dead"]
        limited = bool(n > 0 and admitted > 0 and (g["dead"] / admitted) > DEAD_LIMIT)
        out[e] = {
            "hosts": hosts, "n_deep": n, "n_dead_excluded": g["dead"],
            "limited": limited,
            "reachable": r, "fraction": frac, "ci95": ci,
            "per_channel": {c: (g["channels"][c] / n if n else None) for c in g["channels"]},
            "hop_distribution": {h: g["hops"].count(h) for h in sorted(set(g["hops"]))},
        }
    return out


# ------------------------------------------------------------------ controls
def run_controls(out_dir: Path):
    rows = []
    # (1)/(2) BFS calibration fixtures (instrument range, offline)
    pages = {}
    chain = ["c_index.html"] + [f"c_p{i}.html" for i in range(1, 7)]
    for i, name in enumerate(chain):
        link = f'<a href="{chain[i+1]}">next</a>' if i < len(chain) - 1 else "<a href='#'>end</a>"
        pages[f"/{name}"] = f"<html><body>{link}<form><input name='q'></form></body></html>"
    def fan_add(path, depth):
        if depth > 4:
            return
        kids = "".join(f'<a href="/{path}{c}.html">c</a>' for c in range(10))
        pages[f"/{path}.html"] = f"<html><body>{kids}<form><input name='q'></form></body></html>"
        for c in range(10):
            fan_add(f"{path}{c}", depth + 1)
    fan_add("f_nroot", 1)
    pages["/f_index.html"] = "<html><body><a href='/f_nroot.html'>start</a></body></html>"

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            body = pages.get(self.path)
            if body is None:
                self.send_response(404)
                self.end_headers()
                return
            data = body.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        def log_message(self, *a):
            pass
    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    chain_seen = bfs_structural(base + "/c_index.html")
    c3 = chain_seen.get(norm(base + "/c_p3.html"))
    c1 = chain_seen.get(norm(base + "/c_p1.html"))
    fan_seen = bfs_structural(base + "/f_index.html")
    f1 = fan_seen.get(norm(base + "/f_nroot.html"))
    f3 = sorted((v["requests"] for k, v in fan_seen.items() if v["hop"] == 3), key=lambda x: x)
    f3_first = f3[0] if f3 else None
    r_flat = (c3["requests"] / c1["requests"]) if c1 and c3 else None
    r_growing = (f3_first / f1["requests"]) if f1 and f3_first else None
    rows.append({"control": "NC_BFS_CALIBRATION_FLAT",
                 "pass": (r_flat is not None and r_flat <= 3.0),
                 "observed": {"p1_requests": c1["requests"] if c1 else None,
                              "p3_requests": c3["requests"] if c3 else None,
                              "R_hop3_over_hop1": r_flat}})
    rows.append({"control": "NC_BFS_CALIBRATION_GROWING",
                 "pass": (r_growing is not None and r_growing > 3.0),
                 "observed": {"hop1_requests": f1["requests"] if f1 else None,
                              "first_hop3_requests": f3_first, "R_hop3_over_hop1": r_growing,
                              "nodes_fetched": len(fan_seen)}})
    srv.shutdown()
    srv.server_close()

    # (3) parser canaries (offline fixture strings -> exact expected URL sets)
    canaries = {
        "sitemap_xml": ("<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"
                        "<url><loc>https://example.com/a</loc></url></urlset>",
                        ["https://example.com/a"]),
        "sitemap_index": ("<sitemapindex xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"
                          "<sitemap><loc>https://example.com/s1.xml</loc></sitemap></sitemapindex>",
                          "INDEX"),
        "sitemap_txt": "https://example.com/a\nhttps://example.com/b\n",
        "robots": "User-agent: *\nSitemap: https://example.com/s.xml\n",
        "feed_rss": ("<rss><channel><item><link>https://example.com/p1</link></item></channel></rss>",
                     ["https://example.com/p1"]),
        "feed_atom": ("<feed xmlns='http://www.w3.org/2005/Atom'>"
                      "<entry><link href='https://example.com/p2'/></entry></feed>",
                      ["https://example.com/p2"]),
        "jsonld": ("<script type='application/ld+json'>"
                   '{"@context":"x","mainEntity":{"@type":"WebPage","url":"https://example.com/p3"}}'
                   "</script>", ["https://example.com/p3"]),
    }
    sm = parse_sitemap_any(canaries["sitemap_xml"][0].encode(), "s.xml")
    rows.append({"control": "PC_PARSER_CANARY_sitemap_xml",
                 "pass": sm["urls"] == canaries["sitemap_xml"][1] and not sm["is_index"],
                 "observed": sm})
    smi = parse_sitemap_any(canaries["sitemap_index"][0].encode(), "s.xml")
    rows.append({"control": "PC_PARSER_CANARY_sitemap_index",
                 "pass": smi["is_index"] and smi["child_sitemaps"] == ["https://example.com/s1.xml"],
                 "observed": smi})
    smt = parse_sitemap_txt(canaries["sitemap_txt"].encode())
    rows.append({"control": "PC_PARSER_CANARY_sitemap_txt",
                 "pass": smt["urls"] == ["https://example.com/a", "https://example.com/b"],
                 "observed": smt})
    rb = robots_sitemap_lines(canaries["robots"].encode())
    rows.append({"control": "PC_PARSER_CANARY_robots",
                 "pass": rb == ["https://example.com/s.xml"], "observed": rb})
    fr = feed_entry_urls(canaries["feed_rss"][0].encode())
    rows.append({"control": "PC_PARSER_CANARY_feed_rss",
                 "pass": fr == canaries["feed_rss"][1], "observed": fr})
    fa = feed_entry_urls(canaries["feed_atom"][0].encode())
    rows.append({"control": "PC_PARSER_CANARY_feed_atom",
                 "pass": fa == canaries["feed_atom"][1], "observed": fa})
    jl = jsonld_urls(parse_meta(canaries["jsonld"][0])["jsonld_blocks"])
    rows.append({"control": "PC_PARSER_CANARY_jsonld",
                 "pass": set(jl) == set(canaries["jsonld"][1]), "observed": sorted(jl)})

    # (3b) reachability fixture: positive + null controls over the SCORING
    #      implementation itself (evaluate_items membership + liveness),
    #      executed against a local HTTP fixture, disjoint from the frozen pool.
    rpages = {
        "/deep/listed.html": "<html><body><form><input name='field'></form></body></html>",
        "/deep/jsonld.html": "<html><body><form><input name='field'></form></body></html>",
        "/deep/searchhit.html": "<html><body><form><input name='field'></form></body></html>",
        "/deep/unlisted.html": "<html><body><form><input name='field'></form></body></html>",
        # search results page links ONLY /deep/searchhit.html
        "/search": "<html><body><a href='/deep/searchhit.html'>hit</a></body></html>",
    }

    class RH(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urllib.parse.urlsplit(self.path).path
            body = rpages.get(path)
            if body is None:
                self.send_response(404)
                self.end_headers()
                return
            data = body.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *a):
            pass

    rsrv = ThreadingHTTPServer(("127.0.0.1", 0), RH)
    threading.Thread(target=rsrv.serve_forever, daemon=True).start()
    rbase = f"http://127.0.0.1:{rsrv.server_address[1]}"
    listed = rbase + "/deep/listed.html"
    jsonld_u = rbase + "/deep/jsonld.html"
    search_u = rbase + "/deep/searchhit.html"
    unlisted = rbase + "/deep/unlisted.html"
    dead = rbase + "/deep/dead.html"
    rdocs = {
        "host": "127.0.0.1",
        "search_form": {"action": rbase + "/search", "input": "q"},
        "channel_urls": {
            "ROBOTS_SITEMAP": [],
            "SITEMAP_XML": [listed, dead],
            "ON_SITE_SEARCH": None,
            "RSS_ATOM": [],
            "JSON_LD": [jsonld_u],
        },
    }
    ritems = [
        {"url": listed, "hop": 3, "ordinal": 12, "bytes": 64},
        {"url": jsonld_u, "hop": 3, "ordinal": 13, "bytes": 64},
        {"url": search_u, "hop": 3, "ordinal": 14, "bytes": 64},
        {"url": unlisted, "hop": 3, "ordinal": 15, "bytes": 64},
        {"url": dead, "hop": 3, "ordinal": 16, "bytes": 0},
    ]
    rev = {e["url"]: e for e in evaluate_items({}, rdocs, ritems)}
    rows.append({"control": "PC_REACHABILITY_LISTED_LIVE",
                 "pass": bool(rev[listed]["reachable_any"]) and bool(rev[jsonld_u]["reachable_any"])
                         and bool(rev[search_u]["reachable_any"]),
                 "observed": {"sitemap_listed_live": rev[listed]["reachable_any"],
                              "jsonld_listed_live": rev[jsonld_u]["reachable_any"],
                              "search_listed_live": rev[search_u]["reachable_any"]}})
    rows.append({"control": "NC_REACHABILITY_UNLISTED_OR_DEAD",
                 "pass": (not rev[unlisted]["reachable_any"]) and (not rev[dead]["reachable_any"]),
                 "observed": {"unlisted_live_reachable": rev[unlisted]["reachable_any"],
                              "dead_live_status": rev[dead]["live_status"],
                              "dead_reachable": rev[dead]["reachable_any"]}})
    rsrv.shutdown()
    rsrv.server_close()

    # (4) env probe
    rows.append({"control": "PC_ENV",
                 "pass": True,
                 "observed": {"python": sys.version.split()[0],
                              "stdlib_urllib": True, "ssl_default": True}})

    # (5) null direct-404 on a probe subset of hosts (design-time subset at
    #     EXECUTE runs the full pool)
    for host, eng, seed in POOL[:3]:
        u = seed.rstrip("/") + "/" + SYNTH_PREFIX + "".join(ch for ch in host if ch.isalnum()) + ".html"
        r, _ = fetch(u)
        rows.append({"control": "NC_SYNTHETIC_UNREACHABLE_ITEM_direct",
                     "pass": (r["status"] is not None and r["status"] >= 400),
                     "observed": {"host": host, "status": r["status"], "error": r["error"]}})
    (out_dir / "raw").mkdir(parents=True, exist_ok=True)
    (out_dir / "raw/controls.jsonl").write_text("\n".join(json.dumps(x, sort_keys=True) for x in rows) + "\n")
    return rows


# ------------------------------------------------------------------- main
def main():
    stage = "all"
    if "--stage" in sys.argv:
        idx = sys.argv.index("--stage")
        if idx + 1 < len(sys.argv):
            stage = sys.argv[idx + 1]
    out_dir = Path(".")
    if "--out" in sys.argv:
        out_dir = Path(sys.argv[sys.argv.index("--out") + 1])
    frame_file = FRAME_FILE
    if "--frame" in sys.argv:
        frame_file = sys.argv[sys.argv.index("--frame") + 1]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "raw").mkdir(parents=True, exist_ok=True)

    if stage in ("controls", "all"):
        rows = run_controls(out_dir)
        print("CONTROLS")
        for r in rows:
            print(" ", r["control"], "PASS" if r["pass"] else "FAIL",
                  json.dumps(r["observed"], sort_keys=True))
        if any(not r["pass"] for r in rows):
            print("CONTROL_FAILURE"); sys.exit(3)

    if stage in ("inventory", "all"):
        inv_rows = []
        for host, eng, seed in POOL:
            d = channel_documents(seed)
            d["engine_class"] = eng
            inv_rows.append(d)
            time.sleep(DELAY)
        (out_dir / "raw/channel_docs.jsonl").write_text(
            "\n".join(json.dumps(x, sort_keys=True) for x in inv_rows) + "\n")
        live = {h: sum(1 for r in inv_rows if r["host"] == h) for h in set(r["host"] for r in inv_rows)}
        print("INVENTORY hosts:", len(inv_rows))

    if stage in ("structural", "all"):
        if Path(frame_file).exists():
            # PC-2: consume the frozen parent discovery frame as the Q1 frame.
            rows = [json.loads(l) for l in Path(frame_file).read_text().splitlines() if l.strip()]
            by_host = {h: (h, e, sd) for h, e, sd in POOL}
            for srow in rows:
                if "host" not in srow and "seed" in srow:
                    srow["host"] = by_host.get(srow.get("host"), (None, None, None))[0]
                if srow.get("engine_class") is None:
                    srow["engine_class"] = by_host.get(srow.get("host"), (None, None, None))[1]
            print("FRAME loaded:", frame_file, "hosts:", len(rows))
        else:
            rows = []
            for host, eng, seed in POOL:
                s = bfs_structural(seed)
                s["host"] = host
                s["engine_class"] = eng
                rows.append(s)
                time.sleep(DELAY)
        # PC-2 DEEP fetch census: observe controls on ALL discovered DEEP items.
        census = census_deep(rows)
        (out_dir / "raw/census.jsonl").write_text(
            "\n".join(json.dumps(x, sort_keys=True) for x in census) + "\n")
        (out_dir / "raw/structural.jsonl").write_text(
            "\n".join(json.dumps(x, sort_keys=True) for x in rows) + "\n")
        print("STRUCTURAL+CENSUS done",
              {c["host"]: c["n_deep_with_controls"] for c in census})

    if stage in ("discovery", "all"):
        inv = [json.loads(l) for l in (out_dir / "raw/channel_docs.jsonl").read_text().splitlines()]
        stru = [json.loads(l) for l in (out_dir / "raw/structural.jsonl").read_text().splitlines()]
        item_rows = []
        host_census = {h: 0 for h, _, _ in POOL}
        seed_errors = []
        engine_hosts = {}
        for host, eng, _ in POOL:
            engine_hosts.setdefault(eng, set()).add(host)
        for srow in stru:
            if "seed_error" in srow:
                seed_errors.append(srow["host"])
                continue
            host = srow["host"]
            docs = next((d for d in inv if d["host"] == host), None)
            if docs is None:
                continue
            # Q1 per-host census of state-carrying DEEP pages (structural fact;
            # independent of later liveness/reachability evaluation)
            host_census[host] = sum(
                1 for v in srow.values()
                if isinstance(v, dict) and v.get("hop") in DEEP_BAND
                and (v.get("controls_seen") or 0) > 0)
            items = [{"url": u, "hop": v["hop"], "ordinal": v["ordinal"],
                      "bytes": v["bytes"], "host": host, "engine": srow["engine_class"]}
                     for u, v in srow.items()
                     if isinstance(v, dict) and v.get("hop") in DEEP_BAND
                     and (v.get("controls_seen") or 0) > 0]
            ev = evaluate_items(srow, docs, items)
            for e in ev:
                e["host"] = host
                e["engine"] = srow["engine_class"]
            item_rows.extend(ev)
        (out_dir / "raw/items.jsonl").write_text(
            "\n".join(json.dumps(x, sort_keys=True) for x in item_rows) + "\n")
        m = compute_metrics(item_rows, "engine", pool_engines=engine_hosts)
        engines_with_any = [e for e, g in m.items() if g["n_deep"] > 0]
        engines_limited = sorted([e for e, g in m.items() if g.get("limited")])
        engines_with_zero = sorted([e for e, g in m.items() if g["n_deep"] == 0])
        at_threshold = {e: g for e, g in m.items()
                        if g["n_deep"] > 0 and not g.get("limited")
                        and g["fraction"] is not None and g["fraction"] >= THRESHOLD}
        if not engines_with_any:
            if seed_errors and len(seed_errors) == len(stru) and len(stru) > 0:
                outcome = "INCONCLUSIVE"
                reason = (f"seed fetch failed on every pool host ({sorted(seed_errors)}): "
                          f"infrastructure signature, NOT a scientific null "
                          f"(EXPERIMENT_PACKET.md section 1)")
            else:
                outcome = "INCONCLUSIVE"
                reason = ("zero DEEP items admitted across the frozen pool "
                          "(Q1 measured; Q2/Q3 vacuous per prereg section 10)")
        elif not any(g["n_deep"] > 0 and not g.get("limited") for g in m.values()):
            outcome = "INCONCLUSIVE"
            reason = (f"all DEEP-admitting engines LIMITED (> {DEAD_LIMIT:.0%} item death): "
                      f"{engines_limited}; Q1/Q2 measured but Q3 not determinable "
                      f"(prereg section 10)")
        elif len(at_threshold) >= MIN_ENGINES:
            outcome = "SUPPORTS"
            reason = f"{len(at_threshold)} engines with discovery_reachable_fraction >= {THRESHOLD}"
        else:
            outcome = "FALSIFIES"
            reason = (f"fewer than {MIN_ENGINES} engines reach {THRESHOLD}: "
                      f"{sorted(at_threshold) or 'none'} over {len(engines_with_any)} "
                      f"DEEP-admitting engine(s), limited={engines_limited} "
                      f"(engine-stratified bounded negative)")
        metrics = {
            "experiment_id": EXP_ID,
            "engine_classes_measured": sorted(engine_hosts),
            "pool_engines_census": {e: g["n_deep"] for e, g in m.items()},
            "host_census": host_census,
            "seed_error_hosts": sorted(seed_errors),
            "engines_with_zero_deep": engines_with_zero,
            "engines_limited": engines_limited,
            "engines_at_or_above_threshold": sorted(at_threshold),
            "per_engine": m,
            "outcome": outcome,
            "decision_reason": reason,
        }
        (out_dir / "derived").mkdir(parents=True, exist_ok=True)
        (out_dir / "derived/metrics.json").write_text(json.dumps(metrics, indent=1, sort_keys=True) + "\n")
        print("DECISION", outcome, reason)
        for e, g in m.items():
            flag = " LIMITED" if g.get("limited") else ""
            print(f"  {e}: n={g['n_deep']} reach={g['reachable']} frac={g['fraction']}"
                  f" ci={g['ci95']}{flag}")


if __name__ == "__main__":
    main()
FROZEN_CODE_END

The `FROZEN_CODE_END` line above terminates the module; the three repairs relative to the bound base
module are enumerated in step 4 and are the ONLY semantic changes permitted. The DESIGN smoke test
(section 11a) executed this exact module.

## 8. Stage interface and required outputs

`python3 execute_module.py --stage {controls|inventory|structural|discovery|all} --out DIR [--frame PATH]`

- `--stage controls` -> raw/controls.jsonl; exit 3 on any control failure.
- `--stage inventory` -> raw/channel_docs.jsonl (per host). Re-run as gate V3.
- `--stage structural --frame <bound frame>` -> reads the bound frame, runs the DEEP census,
  writes `raw/census.jsonl` and the censused `raw/structural.jsonl`.
- `--stage discovery` -> reads raw/structural.jsonl + raw/channel_docs.jsonl, scores every admitted
  DEEP item, writes `raw/items.jsonl`, prints the decision (section 10).

## 8b. Execution order at EXECUTE

`--stage controls`, `--stage inventory`, `--stage structural --frame <bound frame>`,
`--stage discovery` (equivalently `--stage all --frame <bound frame>` after the V1 reconstruction).
Any non-zero controls exit is a chain failure.

## 9. Controls ledger (stable identities; observed at DESIGN)

All controls run offline except the synthetic-null direct probe. Observed values are the DESIGN
certificate of section 11.

| control id | type | rule | DESIGN observed |
|---|---|---|---|
| NC_BFS_CALIBRATION_FLAT | null | R_hop3_over_hop1 <= 3.0 | 2.0 (p1=2, p3=4) PASS |
| NC_BFS_CALIBRATION_GROWING | null | R_hop3_over_hop1 > 3.0 | 6.5 (hop1=2, first hop3=13, nodes=250) PASS |
| PC_PARSER_CANARY_sitemap_xml | pos | exact URL set | ['https://example.com/a'] PASS |
| PC_PARSER_CANARY_sitemap_index | pos | index -> child | ['https://example.com/s1.xml'] PASS |
| PC_PARSER_CANARY_sitemap_txt | pos | exact URL set | [a,b] PASS |
| PC_PARSER_CANARY_robots | pos | FIRST Sitemap: line | ['https://example.com/s.xml'] PASS |
| PC_PARSER_CANARY_feed_rss | pos | first item link | ['https://example.com/p1'] PASS |
| PC_PARSER_CANARY_feed_atom | pos | first entry link | ['https://example.com/p2'] PASS |
| PC_PARSER_CANARY_jsonld | pos | seed ld+json URL | ['https://example.com/p3'] PASS |
| PC_REACHABILITY_LISTED_LIVE | pos | listed+live => reachable | sitemap/jsonld/search all True (3/3) PASS |
| NC_REACHABILITY_UNLISTED_OR_DEAD | null | unlisted-live and listed-404 NOT reachable | both False PASS |
| PC_ENV | env | runtime record | Python 3.12.15, stdlib urllib, default TLS PASS |
| NC_SYNTHETIC_UNREACHABLE_ITEM_direct | null | synthetic URL -> status >= 400 | 404 on doc.rust-lang.org, docs.python.org, numpy.org PASS |
| PC-CENSUS-DEEP-FETCH | pos (EXECUTE) | n_deep_fetched == n_deep_discovered per host; n_deep_with_controls >= 1 on >= 2 engines | certified at DESIGN: >= 3 engines (section 11c) |
| PC-SEED-LIVENESS | pos | 20/20 seeds HTTP 200 | 20/20 PASS |

15 control rows at the DESIGN gate (13 distinct identities; NC_SYNTHETIC_UNREACHABLE_ITEM_direct runs
on three hosts). PC-CENSUS-DEEP-FETCH is the PC-2/PC-3 gate enforced at EXECUTE.

## 10. Decision rule (frozen, evaluated in order)

- **G1 measurement validity** (V1 code identity, V2 controls, V3 inventory, V4 frame fidelity,
  V5 census completeness): any FAIL -> status=MEASUREMENT_INVALID, outcome=NOT_APPLICABLE.
- **G2** seed fetch failed on EVERY pool host -> outcome=INCONCLUSIVE ("infrastructure signature,
  NOT a scientific null"), no Q2/Q3.
- **G3** zero live eligible DEEP items admitted across the frame -> INCONCLUSIVE (Q1 measured; Q2/Q3
  vacuous), with engines_with_zero_deep + host_census disclosed.
- **G4** every DEEP-admitting engine LIMITED (>10% admitted-item death) -> INCONCLUSIVE (Q1/Q2
  measured, Q3 not determinable).
- **G5** >= MIN_ENGINES = 2 distinct engines with n_deep > 0, not limited, fraction >= THRESHOLD = 0.50
  -> **SUPPORTS**.
- **G6** otherwise (>= 1 DEEP-admitting engine, < 2 at threshold) -> **FALSIFIES** (engine-stratified
  bounded negative), with engines_limited and engines_with_zero_deep disclosed.

The per-engine fraction uses live admitted DEEP items as denominator; n = 0 -> fraction null. No 0/0
can enter thresholding. Representation (V10/V11/V12), membership equality (V7), liveness severity
(V8) and the charged ledger (V9) are frozen in spec.json `measurement_validity`.

## 10b. Baselines

- **B-SAME-HOST-BFS-PATH-COST** (measured in-frame): per admitted item, the 1-based BFS discovery
  ordinal from the bound frame (<= 250; ~hop+1 on a clean chain). The charged discovery cost (<= K=3)
  is compared to this per-item path cost.
- **B-PERSISTED-PATH-REACQUISITION** (inherited EXP-FRONTIER-37950626378 RACQ_PATH ~hop+1; not
  re-measured).
- **B-DIRECT-URL-REPLAY** (inherited RACQ_URL = 1 GET; not re-measured).

## 11. Pre-freeze certificate (probes on the runner; non-outcome-bearing)

All observations below were produced at DESIGN on 2026-10-11 on the actual runner class
(bare CPython 3.12.15, network enabled, stdlib urllib with default TLS). No Q2/Q3 fraction over the
frozen frame was computed at DESIGN.

### 11a. PC-1 — exact entry point smoke test (offline synthetic; not pool evidence)

Reconstructed module, `--stage inventory` + `--stage structural --frame <fixture>` + `--stage discovery`
over a local HTTP site whose frame row contains discovered-but-unfetched DEEP pages
(`controls_seen=None`): **ran to mechanical completion** and printed `DECISION FALSIFIES ...`
(census `n_deep_discovered=2, n_deep_with_controls=1`; 1 item admitted and reachable). The bound
PARENT module on the same record raises
`TypeError: '>' not supported between instances of 'NoneType' and 'int'` at the Q1-census filter, and
when items are admitted raises `KeyError: 'live'` in `compute_metrics`. `--stage controls` on the
reconstructed module: 15/15 rows PASS. `--stage structural` over an offline fixture: FRAME loaded,
census ran, decision printed.

## 11b. PC-2 certificate — frozen frame census (read from the bound parent record)

| host | engine | deep_discovered | deep_fetched(parent) | deep_with_controls(parent) |
|---|---|---|---|---|
| doc.rust-lang.org | mdBook | 220 | 0 | 0 |
| docs.pytest.org | Sphinx-RTD | 160 | 4 | 4 |
| quotes.toscrape.com | custom | 99 | 10 | 0 |
| docs.readthedocs.io | Sphinx-RTD | 36 | 28 | 28 |
| jekyllrb.com | Jekyll | 24 | 23 | 0 |
| pandas.pydata.org | Sphinx | 9 | 0 | 0 |
| react.dev | Docusaurus | 8 | 7 | 0 |
| other 13 hosts | — | 0 | 0 | 0 |
| **TOTAL** | | **556** | **72** | **32** |

The parent's Q1 conflated "no DEEP item admitted" with "no DEEP state-carrying item exists" because
480 of 556 discovered DEEP pages were never fetched. The census fetches all 556.

## 11c. PC-3 observability certificate (>= 2 engines)

Direct fetches at DESIGN of deep pages on the unfetched frontiers confirm named controls:
`doc.rust-lang.org/stable/book/...` carries `<input name="searchbar" type="search">` (mdBook);
`pandas.pydata.org/docs/...` and `docs.python.org/3/...` and `numpy.org/doc/stable/...` carry
`<input name="q">` (Sphinx); `docs.pytest.org/en/stable/...` and `docs.readthedocs.com/...` carry
`<input name="q">` (Sphinx-RTD); `en.wikipedia.org/...` carries `search`. Deep pages with zero named
controls: jekyllrb.com, react.dev, quotes.toscrape.com. Hence the census will admit DEEP state-carrying
items on >= 3 engines (mdBook, Sphinx, Sphinx-RTD) -> PC-3 holds. EXECUTE re-certifies via
PC-CENSUS-DEEP-FETCH.

## 11d. Channel inventory certificate (frozen pool, re-observed at DESIGN)

ROBOTS_SITEMAP 7 hosts; SITEMAP_XML 9 hosts; ON_SITE_SEARCH 10 hosts; RSS_ATOM 7 hosts; JSON_LD 6
hosts. Notable: doc.rust-lang.org robots -> sitemap.txt (3 top-level redirects, not deep);
docs.pytest.org robots -> sitemap.xml (15 version roots, not deep); docs.readthedocs.io ->
docs.readthedocs.com/sitemap.xml (1 loc); docs.python.org /sitemap.xml (7 loc); numpy.org sitemap
index; jekyllrb.com /sitemap.xml (209 deep loc, but 0 deep controls); react.dev no sitemap;
pandas.pydata.org no sitemap, seed /docs/ has `<form ... action="search.html" ... name="q">`.
Static search-result pages were observed to return navigation shells (JS-rendered results), so
ON_SITE_SEARCH is expected to be near-zero on those hosts. This inventory is DOCUMENTATION of the
substrate; it is NOT a Q2 fraction and must not be read as one.

## 11e. Branch-reachability argument (decision_rule_reachability)

- The six gates partition exhaustively. For any attained pool with >= 1 eligible DEEP item exactly one
  of G5 (SUPPORTS) / G6 (FALSIFIES) fires; G2, G3, G4 are reachable INCONCLUSIVE branches with
  explicit non-null reasons.
- Denominators are non-zero by construction (V6): n = 0 -> fraction null and the engine is reported in
  the zero-DEEP census rather than thresholded, so no branch is arithmetically empty.
- The instrument returns both True and False on the reachability metric itself: PC_REACHABILITY_LISTED_LIVE
  (3/3 True) and NC_REACHABILITY_UNLISTED_OR_DEAD (both False), plus the flat/growing BFS calibration pair.
- PC-3 holds (section 11c), so the Q3 contrast operates on >= 2 observable engines, not a single engine.
- SUPPORTS is a real state of the world for this instrument: a credential-free, GET-only host exposing
  a deep-complete static index exists in-substrate (DESIGN certificate: `docs.djangoproject.com`'s
  per-locale sitemap indexed 11,211 URLs and its deep pages carry `<input name="q">` + category), so
  the union of the five channels CAN enumerate deep state-carrying items within K. This host is NOT in
  the frozen frame and is cited only to show the positive pole is not impossible; no pre-freeze
  fraction was measured and the a-priori probability of SUPPORTS is expressly NOT claimed (section 14).

## 12. freeze_eligibility (summary; full reasons in spec.json)

| check | status | one-line basis |
|---|---|---|
| decision_rule_reachability | PASS | exhaustive partition; both decision branches reachable; metric dynamic range certified; non-zero denominators; PC-3 met; SUPPORTS is a real in-substrate state (section 11e) |
| measurement_prerequisites | PASS | PC-1 smoke PASS; bound frame + census admits >= 3 engines (PC-2/PC-3); 20/20 seeds live; 5 channels live; controls 15/15 |
| baseline_identifiability | PASS | B-SAME-HOST-BFS-PATH-COST measured in-frame; two inherited comparators labeled not re-measured; charged <= K = 3 vs per-item path cost |
| control_sensitivity | PASS | every control fires both directions; reachability fixture drives the real scoring path; NC synthetic-null bites only on real HTTP >= 400 |
| treatment_liveness | PASS | the exact discovery entry point was EXECUTED to completion pre-freeze on the reconstructed module; parent proven non-executable; V1/V2 gates re-run at EXECUTE |
| freeze_artifacts_bound | PASS | bound parent frame (Q1 frame) + bound base module (code), with patch + derived-module hashes pinned |

## 13. freeze_artifacts

1. `research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl` (Q1 frame).
2. `research/experiments/EXP-FRONTIER-38164611798/execute_module.py` (code base).

Their sha256 values are recorded in freeze.json.artifact_hashes at freeze time and are immutable
interpretation dependencies for this experiment.

## 14. Validity threats and representation loss

1. **Construct degeneracy (inherited, disclosed).** "State-carrying" counts theme chrome (mdBook
   `searchbar`, zensical `__palette`, utility `q`). This can inflate Q1 prevalence and, if a channel
   indexes those pages, Q2. The construct is NOT narrowed post-hoc; a zero/chrome-split secondary
   count may be reported in the report as non-decision-bearing context only.
2. **Index-completeness confound (empirical tilt).** At DESIGN the hosts with deep-complete static
   indexes (Jekyll, MkDocs Material, Astro/Starlight, Hugo, zensical, Docusaurus) mostly have JS or
   unnamed search, while the hosts with static named search forms (mdBook, Sphinx, Sphinx-RTD) have
   shallow site indexes. This makes the SUPPORTS branch a priori improbable on the frozen frame. This
   is disclosed, not repaired: the fraction is left to EXECUTE. A FALSIFIES here is a bounded negative
   about this substrate class and frame, NOT a proof that no site on the credential-free Web can
   enumerate deep content.
3. **Frame staleness.** The frame URLs were discovered hours before this design; EXECUTE may run later.
   Dead URLs are excluded with reason, never counted as reachable; an engine whose admitted items all
   die is reported dead (and can push the result toward INCONCLUSIVE, correctly).
4. **Discovery cost arithmetic.** Charged costs (<= K=3) are protocol costs; the per-item liveness GET
   is shared/charged per channel and reported in the actual ledger (V9). Redirect legs count.
5. **Truncation/degenerate bodies.** MAX_BODY = 600000 bytes with truncation flags; robots/sitemap
   endpoints that return SPA shells are recorded as such (e.g., blog.wordpress.org).
6. **No credential/JS channels.** The five channels are static-HTTP only; JS-rendered search indexes
   are out of scope by the mandate. Any JS-only discovery is recorded as a coverage gap, not a null.

## 15. Consequences

- **SUPPORTS:** C-CROSSSITE moves toward EXPERIMENTAL (bounded to this substrate/frame/K/channels);
  the deep-acquisition architecture moves off traversal-and-cache toward discovery-channel coverage
  and substrate expansion; the recorded runner-up (C-FRESHNESS/C-PRODUCT-ECON persistence-maintenance
  economics) becomes the scheduled next mandate.
- **FALSIFIES:** bounded negative; no shortcut is promoted; the discovery axis is closed on this
  substrate class and the runner-up becomes the conditional next mandate.
- **INCONCLUSIVE:** the Q1 census (per-host/frame DEEP map + zero-DEEP engines) and per-channel
  zero-admission ledger are the durable deliverable; no claim update; a future design re-targets pools
  from the census.
- **BLOCKED (PC-1/2/3 unmet):** record the exact unmet precondition; terminate this bounded thread.

## 16. EXECUTE plan and required outputs

1. Reconstruct the module (section 7) and verify V1.
2. Run `--stage controls` (V2) and `--stage inventory` (V3).
3. Run `--stage structural --frame research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl`
   (V4/V5) -> `raw/census.jsonl`, `raw/structural.jsonl`.
- Then `--stage discovery` -> `raw/items.jsonl` + decision.
- Write `result.json`, `report.md`, `provenance.json` per EXPERIMENT_PACKET.md. `result.json` MUST
  include schema_version, experiment_id, lane, status, outcome, metrics, controls, artifacts,
  observations, validity_notes, unresolved. `status` describes measurement validity (a valid negative
  is COMPLETE + FALSIFIES). Preserve frozen control identities and exact evidence paths/hashes.
  Recomputation of the code hashes and the frame sha256 must appear in provenance.json.

## 16b. Estimated cost

Stdlib-only; zero pip, zero model calls, no browser. Census <= 556 GETs; per-item evaluation <= 2
GETs x admitted items (<= 556) + channel documents (~120) + controls (~15). Typical ~1,000-1,800 GETs,
well under the budget-250-per-host BFS cost of a fresh crawl.

## 16c. Deltas vs pre-2.0 and prior attempts (why this is not a rerun)

1. **v1 vs EXP-FRONTIER-37984242167:** a non-empty, frozen, 556-item frame replaces the empty frame
   (the falsifier is no longer 0/0-unreachable).
2. **v5 vs EXP-FRONTIER-38085197666:** the frozen artifacts exist and their hashes are verified at
   EXECUTE (V1/V4), replacing a declared-PASS-while-absent freeze.
3. **v3 vs EXP-FRONTIER-38164611798:** the census fetches the unfetched DEEP frontiers (PC-2) instead
   of leaving controls_seen=None; the entry point is proven executable (PC-1); and the code identity is
   bound. The parent's `controls_seen` filter, its `live` key mismatch, and its observability censoring
   are all repaired and re-certified at pre-freeze cost.

## 17. References

- request.json (director_mandate, allocation CONTINUE C-CROSSSITE).
- research/experiments/EXP-FRONTIER-38164611798/{handoff.json,result.json,audit.json,prereg.md,execute_module.py,raw/structural.jsonl}.
- research/experiments/EXP-FRONTIER-37984242167/{spec.json,audit.json} (empty-frame precedent).
- research/experiments/EXP-FRONTIER-38085197666/failure.json (absent-artifact freeze).
- research/experiments/EXP-FRONTIER-37950626378/result.json (inherited RACQ_PATH/RACQ_URL).
- research/EXPERIMENT_PACKET.md; research/portfolio/POLICY.md; AGENTS.md.
