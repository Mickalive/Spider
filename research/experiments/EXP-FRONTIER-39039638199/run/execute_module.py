#!/usr/bin/env python3
"""EXP-FRONTIER-39039638199 - session-scale invalidation hazard on a
fetch-complete documentation-Web census frame, stratified by hop depth, with
censoring-aware one-sided Clopper-Pearson bounds and a named tolerance
certification / refusal decision.

Frozen EXECUTE driver.  stdlib-only, credential-free GET-only, single egress
vantage, no browser, no JavaScript execution, no persistence store, no
revalidation ladder, no cold-vs-store cost comparison.

Stages:
  controls  offline in-process HTTP fixture canaries + exact-bounds canaries
            (no external network)
  all       controls -> obs0 fetch-complete census -> separation sleep ->
            obs1 re-fetch of the admitted set -> retrospective longer-window
            channel -> frozen decision

Emits, under --out:
  raw/controls.jsonl, raw/control_probes.jsonl, raw/census.jsonl,
  raw/obs1.jsonl, raw/selfpair.jsonl, raw/retro.jsonl, raw/PROGRESS.json,
  derived/metrics.json, derived/decision.json
"""
from __future__ import annotations

import argparse
import hashlib
import html.parser
import http.server
import json
import math
import re
import socketserver
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# frozen constants
# --------------------------------------------------------------------------
SEEDS = [
    ("doc.rust-lang.org", "https://doc.rust-lang.org/stable/book/"),
    ("docs.pytest.org", "https://docs.pytest.org/en/stable/"),
    ("docs.readthedocs.io", "https://docs.readthedocs.io/en/stable/"),
    ("pandas.pydata.org", "https://pandas.pydata.org/docs/"),
]
DEPTH = 6
SHALLOW_MAX_HOP = 2
SHALLOW_CAP_PER_HOST = 140
DEEP_CAP_PER_HOST = 220
PER_HOST_GET_CEILING = 420
PER_HOST_WALL_S = 150.0
GET_CEILING_OBS0 = 1500
GET_CEILING_OBS1 = 1600
GET_CEILING_TOTAL = 3200
OBS1_TARGET_CAP = 1200
SEPARATION_S = 360.0
DT_MIN_S = 300.0
DT_MAX_S = 900.0
MODULE_WALL_BUDGET_S = 900.0
REQUEST_TIMEOUT = 12.0
MAX_BODY_BYTES = 8_000_000
WORKERS = 6
PER_HOST_CONCURRENCY = 2
PER_HOST_SPACING_S = 0.10
UA = "spider-r2/1.0"
ASSET_EXTS = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".zip", ".gz", ".tar", ".tgz",
    ".bz2", ".xz", ".mp3", ".mp4", ".webm", ".avi", ".mov", ".txt", ".xml",
)
CERT_GRID = (0.01, 0.02, 0.05)
MIN_N_PER_STRATUM = 60
MIN_HOST_STRATUM_N = 25
MIN_HOSTS_BOTH = 2
CENSOR_MAX = 0.20
HOST_CONC_WARN = 0.60
VERSION_PINNED_FRAC_WARN = 0.80
ALPHA = 0.05
SELFPAIR_N = 10
SELFPAIR_MAX_GAP_S = 5.0
POS_CONTROL_URLS = [
    "https://www.cloudflare.com/cdn-cgi/trace",
    "https://api.github.com/rate_limit",
    "https://timeapi.io/api/Time/current/zone?timeZone=UTC",
]
NULL_CONTROL_URLS = [
    "https://example.com/",
    "https://www.iana.org/domains/reserved",
]
PARENT_CENSUS = ("research/experiments/EXP-FRONTIER-38940047535/"
                 "run/raw/census.jsonl")
PARENT_PROVENANCE = ("research/experiments/EXP-FRONTIER-38940047535/"
                     "provenance.json")
RETRO_MIN_WINDOW_H = 6.0
RETRO_MAX_WINDOW_D = 30.0
VER_RE = re.compile(r"(^|/)(\d+\.\d+(\.\d+)?(\.x)?|v\d+(\.\d+)*)(/|$)")
MOV_RE = re.compile(
    r"/(stable|latest|dev|dev-requirements|main|master|trunk|edge|nightly)(/|$)")

_T0 = time.monotonic()
_GET_LOCK = threading.Lock()
_GETS = {"n": 0}
_HOST_SEM: dict = {}
_HOST_NEXT: dict = {}


def elapsed() -> float:
    return time.monotonic() - _T0


def gets() -> int:
    with _GET_LOCK:
        return _GETS["n"]


def _host_sem(host: str) -> threading.BoundedSemaphore:
    with _GET_LOCK:
        if host not in _HOST_SEM:
            _HOST_SEM[host] = threading.BoundedSemaphore(PER_HOST_CONCURRENCY)
        return _HOST_SEM[host]


def repo_root() -> Path:
    p = Path(__file__).resolve()
    for anc in [p.parent] + list(p.parents):
        if (anc / "research" / "lanes" / "registry.json").is_file():
            return anc
    return Path.cwd()


def iso(ts: float | None) -> str:
    if ts is None:
        return ""
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


# --------------------------------------------------------------------------
# canonicalisation (PRIMARY change channel) and URL classification
# --------------------------------------------------------------------------
_COMMENT_RE = re.compile(r"(?is)<!--.*?-->")
_SCRIPT_RE = re.compile(r"(?is)<script\b.*?</script\s*>")
_STYLE_RE = re.compile(r"(?is)<style\b.*?</style\s*>")
_TAG_RE = re.compile(r"(?s)<[^>]*>")
_WS_RE = re.compile(r"\s+")


def canon(body: bytes) -> str:
    """Frozen structural-text canonicalisation of a fetched body.

    Removes comments, <script> and <style> blocks and every remaining tag,
    unescapes the six standard entities, collapses whitespace runs, lowercases.
    HTML attributes are therefore NOT observable on this channel by
    construction; the byte channel is reported alongside precisely so that
    attribute-only and script-only churn stays visible instead of silently
    vanishing.
    """
    t = body.decode("utf-8", "replace")
    t = _COMMENT_RE.sub(" ", t)
    t = _SCRIPT_RE.sub(" ", t)
    t = _STYLE_RE.sub(" ", t)
    t = _TAG_RE.sub(" ", t)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")):
        t = t.replace(a, b)
    return _WS_RE.sub(" ", t).strip().lower()


def text_sha(body: bytes) -> str:
    return hashlib.sha256(canon(body).encode("utf-8")).hexdigest()


def url_class(url: str) -> str:
    p = urllib.parse.urlsplit(url).path
    if VER_RE.search(p):
        return "VERSION_PINNED"
    if MOV_RE.search(p):
        return "MOVING_ALIAS"
    return "OTHER"


# --------------------------------------------------------------------------
# exact one-sided Clopper-Pearson bounds (no scipy dependency)
# --------------------------------------------------------------------------
def binom_tail(k: int, n: int, p: float) -> float:
    if n <= 0:
        return 1.0
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 1.0 if k >= n else 0.0
    return sum(math.comb(n, i) * p ** i * (1.0 - p) ** (n - i)
               for i in range(0, k + 1))


def cp_ub95(k: int, n: int, alpha: float = ALPHA) -> float | None:
    """sup{p : P(X <= k | n, p) > alpha}: one-sided upper 95% binomial bound."""
    if n <= 0:
        return None
    if k >= n:
        return 1.0
    if binom_tail(k, n, 1.0) > alpha:
        return 1.0
    lo, hi = k / n, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if binom_tail(k, n, mid) > alpha:
            lo = mid
        else:
            hi = mid
    return hi


def cert_level(k: int, n: int) -> float | None:
    """Tightest level in CERT_GRID certified by the one-sided 95% bound."""
    if n <= 0:
        return None
    ub = cp_ub95(k, n)
    if ub is None:
        return None
    for level in CERT_GRID:
        if ub <= level:
            return level
    return None


def contrast_p(kd: int, nd: int, ks: int, ns: int) -> float:
    """Exact one-sided p-value for p_deep > p_shallow under the pooled rate."""
    tot, k = nd + ns, kd + ks
    if tot <= 0 or k <= 0 or ns <= 0:
        return 1.0
    return binom_tail(ks, ns, k / tot)


def mdc_deep_rate(nd: int, ns: int, cap: int = 60) -> float | None:
    """Smallest deep rate detectable at ALPHA when the shallow stratum has none."""
    if nd <= 0 or ns <= 0:
        return None
    for kd in range(1, cap + 1):
        if contrast_p(kd, nd, 0, ns) <= ALPHA:
            return kd / nd
    return None


# --------------------------------------------------------------------------
# transport (norm / is_asset / static_links / fetch mirror the bound parent policy)
# --------------------------------------------------------------------------
class _LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def norm(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    scheme = p.scheme.lower()
    netloc = p.netloc.lower()
    if ":" in netloc and not netloc.endswith("]"):
        host, _, port = netloc.rpartition(":")
        if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
            netloc = host
    return urllib.parse.urlunsplit((scheme, netloc, p.path or "/", p.query, ""))


def is_asset(url: str) -> bool:
    return urllib.parse.urlsplit(url).path.lower().endswith(ASSET_EXTS)


def static_links(base: str, body: bytes) -> list:
    lp = _LinkParser()
    try:
        lp.feed(body.decode("utf-8", "replace"))
    except Exception:
        return []
    out = []
    for href in lp.hrefs:
        try:
            u = urllib.parse.urljoin(base, href.strip())
        except Exception:
            continue
        if urllib.parse.urlsplit(u).scheme not in ("http", "https"):
            continue
        if is_asset(u):
            continue
        out.append(u)
    return out


def fetch(url: str, want_links: bool = False,
          timeout: float = REQUEST_TIMEOUT) -> dict:
    """One credential-free GET.  Returns a RAW observation record only.

    The body is hashed and (optionally) link-extracted at fetch time and then
    dropped: no body is ever retained, which keeps peak memory independent of
    frame size.  Bytes are never masked, so a server that returns different
    bytes for different User-Agent strings is observable as a byte-channel
    change and is not silently absorbed.
    """
    host = urllib.parse.urlsplit(url).netloc.lower()
    rec = {"url": norm(url), "status": None, "body_len": None, "sha256": None,
           "text_sha256": None, "final_url": None, "content_type": "",
           "etag": "", "last_modified": "", "truncated": False, "error": None,
           "t_start": None, "t_end": None}
    links: list = []
    with _host_sem(host):
        with _GET_LOCK:
            wait = _HOST_NEXT.get(host, 0.0) - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        rec["t_start"] = time.monotonic()
        body = b""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read(MAX_BODY_BYTES + 1)
                rec["status"] = int(r.status)
                rec["final_url"] = norm(r.geturl())
                rec["content_type"] = (
                    r.headers.get("Content-Type") or "").split(";")[0].strip()
                rec["etag"] = r.headers.get("ETag") or ""
                rec["last_modified"] = r.headers.get("Last-Modified") or ""
                if len(raw) > MAX_BODY_BYTES:
                    raw = raw[:MAX_BODY_BYTES]
                    rec["truncated"] = True
                body = raw
                if want_links:
                    links = static_links(rec["final_url"], body)
        except urllib.error.HTTPError as e:
            try:
                e.read()
            except Exception:
                pass
            rec["status"] = int(e.code)
            rec["final_url"] = norm(url)
            rec["error"] = "http_%d" % e.code
        except Exception as e:
            rec["final_url"] = norm(url)
            rec["error"] = repr(e)[:120]
        rec["t_end"] = time.monotonic()
        with _GET_LOCK:
            _HOST_NEXT[host] = time.monotonic()
            _GETS["n"] += 1
    rec["body_len"] = len(body)
    if body:
        rec["sha256"] = hashlib.sha256(body).hexdigest()
        rec["text_sha256"] = text_sha(body)
    rec["_links"] = links
    return rec


def fetch_many(urls: list, want_links: bool = False,
               workers: int = WORKERS) -> list:
    """Concurrent GETs.  Records are returned in input order."""
    out: list = [None] * len(urls)
    lock = threading.Lock()
    idx = {"i": 0}

    def run() -> None:
        while True:
            with lock:
                i = idx["i"]
                if i >= len(urls):
                    return
                idx["i"] = i + 1
            out[i] = fetch(urls[i], want_links=want_links)

    ths = [threading.Thread(target=run, daemon=True)
           for _ in range(max(1, workers))]
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    return out


# --------------------------------------------------------------------------
# fetch-complete, stratum-reserved, level-ordered BFS census (one host)
# --------------------------------------------------------------------------
def sweep_host(label: str, seed: str) -> dict:
    """Level-ordered BFS with a stratum-reserved fetch policy.

    Levels 0..SHALLOW_MAX_HOP form the SHALLOW stratum and are capped at
    SHALLOW_CAP_PER_HOST fetches; levels >= SHALLOW_MAX_HOP+1 form the DEEP
    stratum and are capped at DEEP_CAP_PER_HOST fetches.  Fetching therefore
    stops when the stratum's fetch budget is exhausted, never when discovery is
    exhausted.  This is the repair of the parent's discover-until-budget
    starvation, in which 363 of 402 discovered deep URLs were never fetched.
    """
    deadline = time.monotonic() + PER_HOST_WALL_S
    recs: dict = {}
    hop: dict = {}
    shallow_fetches = 0
    deep_fetches = 0
    seed_n = norm(seed)
    seed_rec = fetch(seed_n, want_links=True)
    recs[seed_n] = seed_rec
    hop[seed_n] = 0
    seed_host = urllib.parse.urlsplit(
        seed_rec["final_url"] or seed_n).netloc.lower()
    if seed_rec["status"] != 200:
        return {"host": label, "seed": seed_n,
                "seed_error": seed_rec["error"] or ("status=%s" % seed_rec["status"]),
                "recs": recs, "hop": hop, "shallow_fetches": 0, "deep_fetches": 0,
                "shallow_capped": False, "deep_capped": False,
                "time_truncated": False, "gets_host": gets()}
    seen = {seed_n}
    frontier = [seed_n]
    for lvl in range(DEPTH):
        if not frontier:
            break
        if lvl <= SHALLOW_MAX_HOP:
            if shallow_fetches >= SHALLOW_CAP_PER_HOST:
                # shallow stratum budget exhausted: skip (do not fetch) this
                # level but keep descending so the DEEP stratum is still
                # fetched from whatever was already discovered.
                continue
            budget = min(len(frontier), SHALLOW_CAP_PER_HOST - shallow_fetches)
        else:
            if deep_fetches >= DEEP_CAP_PER_HOST:
                break
            budget = min(len(frontier), DEEP_CAP_PER_HOST - deep_fetches)
        batch, frontier = frontier[:budget], frontier[budget:]
        if gets() >= GET_CEILING_OBS0 or gets() >= GET_CEILING_TOTAL:
            break
        if time.monotonic() > deadline:
            break
        got = fetch_many(batch, want_links=True, workers=PER_HOST_CONCURRENCY)
        if lvl <= SHALLOW_MAX_HOP:
            shallow_fetches += len(got)
        else:
            deep_fetches += len(got)
        nxt: list = []
        for u, rec in zip(batch, got):
            recs[u] = rec
            hop[u] = lvl
            if rec["status"] != 200:
                continue
            for raw in rec.get("_links", []):
                nu = norm(raw)
                if nu in seen:
                    continue
                if urllib.parse.urlsplit(nu).netloc.lower() != seed_host:
                    continue
                seen.add(nu)
                nxt.append(nu)
        frontier = frontier + nxt
    for rec in recs.values():
        rec.pop("_links", None)
    return {"host": label, "seed": seed_n, "seed_error": None, "recs": recs,
            "hop": hop, "shallow_fetches": shallow_fetches,
            "deep_fetches": deep_fetches,
            "shallow_capped": shallow_fetches >= SHALLOW_CAP_PER_HOST,
            "deep_capped": deep_fetches >= DEEP_CAP_PER_HOST,
            "time_truncated": time.monotonic() > deadline,
            "gets_host": gets()}


# --------------------------------------------------------------------------
# frozen decision function
# --------------------------------------------------------------------------
def decide(m: dict) -> dict:
    """Total function on the frozen metrics.  Every branch is reachable and no
    branch depends on anything not present in `m`.

    m keys used: control_ok, frame_ok, n_deep, n_shallow, k_text_deep,
    k_text_shallow, censor_frac_deep, censor_frac_shallow, host_conc_deep,
    host_conc_shallow, hosts_both, verpin_frac_deep, verpin_frac_shallow.
    """
    if not m["control_ok"] or not m["frame_ok"]:
        return {"label": "NO_DATA_CONTROL_OR_FRAME_FAIL", "status": "MEASUREMENT_INVALID",
                "certified_deep": None, "certified_shallow": None,
                "reason": "frozen validity gates failed before a certification is possible"}
    if m["n_deep"] < MIN_N_PER_STRATUM or m["n_shallow"] < MIN_N_PER_STRATUM:
        return {"label": "REFUSE_CERTIFY_INSUFFICIENT_N", "status": "COMPLETE",
                "certified_deep": None, "certified_shallow": None,
                "reason": "paired per-stratum n below MIN_N_PER_STRATUM=%d "
                          "(deep=%d shallow=%d)" % (MIN_N_PER_STRATUM, m["n_deep"],
                                                    m["n_shallow"])}
    if (m["censor_frac_deep"] > CENSOR_MAX or m["censor_frac_shallow"] > CENSOR_MAX):
        starved = []
        if m["censor_frac_deep"] > CENSOR_MAX:
            starved.append("DEEP")
        if m["censor_frac_shallow"] > CENSOR_MAX:
            starved.append("SHALLOW")
        return {"label": "REFUSE_CERTIFY_CENSORED_" + "_".join(starved),
                "status": "COMPLETE", "certified_deep": None,
                "certified_shallow": None,
                "reason": "observation-1 censoring above CENSOR_MAX=%.2f; the "
                          "surviving-pair bound would not generalise to the "
                          "admitted population" % CENSOR_MAX}
    ld = cert_level(m["k_text_deep"], m["n_deep"])
    ls = cert_level(m["k_text_shallow"], m["n_shallow"])
    if ld is None and ls is None:
        label = "GUARD_REQUIRED_BOTH_STRATA"
    elif ld is None:
        label = "CERTIFY_SHALLOW_GUARD_DEEP"
    elif ls is None:
        label = "CERTIFY_DEEP_GUARD_SHALLOW"
    else:
        label = "CERTIFY_BOTH_AT_" + ("%g" % max(ld, ls)).replace(".", "P")
    tags = []
    if m["hosts_both"] < MIN_HOSTS_BOTH:
        tags.append("DEPTH_NOT_IDENTIFIABLE")
    if max(m["host_conc_deep"], m["host_conc_shallow"]) >= HOST_CONC_WARN:
        tags.append("HOST_CONCENTRATED")
    if max(m["verpin_frac_deep"], m["verpin_frac_shallow"]) >= VERSION_PINNED_FRAC_WARN:
        tags.append("BOUNDED_TO_VERSION_PINNED")
    out = {"label": label + ("__" + "_".join(tags) if tags else ""),
           "status": "COMPLETE", "certified_deep": ld, "certified_shallow": ls,
           "tags": tags}
    if ld is None:
        out["reason"] = ("deep-stratum per-page text-change upper bound exceeds the "
                         "coarsest certified level (%.2f)" % CERT_GRID[-1])
    elif ls is None:
        out["reason"] = ("shallow-stratum per-page text-change upper bound exceeds the "
                         "coarsest certified level (%.2f)" % CERT_GRID[-1])
    else:
        out["reason"] = ("both strata certify zero-GET tolerance at the measured "
                         "separation; coarsest certified level %g" % max(ld, ls))
    if "DEPTH_NOT_IDENTIFIABLE" in tags:
        out["reason"] += ("; depth-concentration claim REFUSED because fewer than "
                          "%d hosts populate both strata" % MIN_HOSTS_BOTH)
    return out


# --------------------------------------------------------------------------
# offline controls (in-process HTTP fixture; no external network)
# --------------------------------------------------------------------------
FIXTURES = {
    "/static.html": (200, b"<html><head><title>Static</title></head><body>"
                     b"<h1>Static Page</h1><p>alpha beta gamma</p></body></html>"),
    "/textmut.html": (200, b"<html><head><title>Static</title></head><body>"
                      b"<h1>Static Page</h1><p>alpha beta DELTA</p></body></html>"),
    "/attr.html": (200, b"<html><head><title>Static</title></head><body class=\"a\" "
                   b"data-n=\"7\"><h1>Static Page</h1><p>alpha beta gamma</p></body></html>"),
    "/script.html": (200, b"<html><head><title>Static</title><script nonce=\"zzz\">"
                     b"var a=1;</script></head><body><h1>Static Page</h1>"
                     b"<p>alpha beta gamma</p></body></html>"),
    "/gone.html": (200, b"<html><body><h1>Temporary</h1><p>temp page</p></body></html>"),
}


def offline_controls() -> list:
    rows: list = []
    state = {"gone_404": False}

    class H(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):
            pass

        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/gone.html" and state["gone_404"]:
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            if path not in FIXTURES:
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            code, body = FIXTURES[path]
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_address[1]

    def rec(cid, expect, ok, detail):
        rows.append({"control": cid, "expected": expect, "observed": detail,
                     "pass": bool(ok)})

    a = fetch(base + "/static.html")
    b = fetch(base + "/static.html")
    rec("C-CANON-IDEMPOTENT", "canon(canon(x))==canon(x)",
        canon(canon(a and FIXTURES["/static.html"][1]).encode()) == canon(FIXTURES["/static.html"][1]),
        "static text_sha stable=%s" % (a["text_sha256"] == b["text_sha256"]))
    mut = fetch(base + "/textmut.html")
    rec("C-DETECT-TEXT-INJECTION", "visible-text change -> TEXT differs",
        mut["text_sha256"] != a["text_sha256"],
        "text_changed=%s byte_changed=%s" % (mut["text_sha256"] != a["text_sha256"],
                                              mut["sha256"] != a["sha256"]))
    attr = fetch(base + "/attr.html")
    rec("C-DETECT-ATTR-ONLY", "attribute-only change -> TEXT same, BYTE differs",
        attr["text_sha256"] == a["text_sha256"] and attr["sha256"] != a["sha256"],
        "text_same=%s byte_diff=%s" % (attr["text_sha256"] == a["text_sha256"],
                                        attr["sha256"] != a["sha256"]))
    scr = fetch(base + "/script.html")
    rec("C-DETECT-SCRIPT-ONLY", "script-nonce change -> TEXT same, BYTE differs",
        scr["text_sha256"] == a["text_sha256"] and scr["sha256"] != a["sha256"],
        "text_same=%s byte_diff=%s" % (scr["text_sha256"] == a["text_sha256"],
                                        scr["sha256"] != a["sha256"]))
    st = fetch(base + "/gone.html")
    st2 = fetch(base + "/gone.html")
    state["gone_404"] = True
    gone = fetch(base + "/gone.html")
    rec("C-CENSOR-404-DETECTED", "404 at obs1 -> censored channel, not a text event",
        gone["status"] == 404 and st["status"] == 200,
        "obs0=%s obs1=%s" % (st["status"], gone["status"]))
    rec("C-LIVE-DETECTOR-ON-FIXTURE", "two identical fixture GETs -> no change",
        st["text_sha256"] == st2["text_sha256"],
        "text_same=%s" % (st["text_sha256"] == st2["text_sha256"]))
    for (k, n), cid, want in (((0, 60), "C-CP-BOUND-N60", 0.048703),
                              ((0, 150), "C-CP-BOUND-N150", 0.019773),
                              ((0, 299), "C-CP-BOUND-N299", 0.009969),
                              ((1, 400), "C-CP-BOUND-K1N400", 0.011804)):
        got = cp_ub95(k, n)
        rec(cid, "exact one-sided 95%% UB at k=%d,n=%d" % (k, n),
            abs(got - want) < 5e-6, "ub=%.6f expected=%.6f" % (got, want))
    rec("C-CERT-LEVEL-LADDER", "cert_level(0,299)=0.01, (0,150)=0.02, (0,60)=0.05, (1,400)=0.02",
        cert_level(0, 299) == 0.01 and cert_level(0, 150) == 0.02
        and cert_level(0, 60) == 0.05 and cert_level(1, 400) == 0.02,
        "levels=%s" % [cert_level(0, 299), cert_level(0, 150), cert_level(0, 60),
                       cert_level(1, 400)])
    rec("C-CONTRAST-POWER", "contrast_p(6,380,0,420)<=0.05 and contrast_p(5,380,0,420)>0.05",
        contrast_p(6, 380, 0, 420) <= 0.05 and contrast_p(5, 380, 0, 420) > 0.05,
        "p6=%.5f p5=%.5f mdc=%s" % (contrast_p(6, 380, 0, 420),
                                     contrast_p(5, 380, 0, 420),
                                     mdc_deep_rate(380, 420)))
    base_m = {"control_ok": True, "frame_ok": True, "n_deep": 380, "n_shallow": 420,
              "k_text_deep": 0, "k_text_shallow": 0, "censor_frac_deep": 0.02,
              "censor_frac_shallow": 0.02, "host_conc_deep": 0.5, "host_conc_shallow": 0.4,
              "hosts_both": 3, "verpin_frac_deep": 0.05, "verpin_frac_shallow": 0.02}
    canaries = [
        ("C-DECIDE-CERTIFY-BOTH", dict(base_m)),
        ("C-DECIDE-GUARD-BOTH", dict(base_m, k_text_deep=12, k_text_shallow=9)),
        ("C-DECIDE-GUARD-DEEP", dict(base_m, k_text_deep=12)),
        ("C-DECIDE-GUARD-SHALLOW", dict(base_m, k_text_shallow=12)),
        ("C-DECIDE-INSUFFICIENT-N", dict(base_m, n_deep=40)),
        ("C-DECIDE-CENSORED", dict(base_m, censor_frac_deep=0.55)),
        ("C-DECIDE-CONTROL-FAIL", dict(base_m, control_ok=False)),
        ("C-DECIDE-NOT-IDENTIFIABLE", dict(base_m, hosts_both=1)),
        ("C-DECIDE-HOST-CONCENTRATED", dict(base_m, host_conc_deep=0.91)),
        ("C-DECIDE-VERSION-PINNED", dict(base_m, verpin_frac_shallow=0.85)),
    ]
    seen_labels = []
    for cid, mm in canaries:
        d = decide(mm)
        seen_labels.append(d["label"])
        rec(cid, "reachable decision branch: %s" % d["label"], True,
            "status=%s certified_deep=%s certified_shallow=%s"
            % (d["status"], d["certified_deep"], d["certified_shallow"]))
    rec("C-DECIDE-BRANCHES-DISTINCT", ">=9 distinct decision labels", 
        len(set(seen_labels)) >= 9, "labels=%s" % sorted(set(seen_labels)))
    srv.shutdown()
    return rows


# --------------------------------------------------------------------------
# live measurement
# --------------------------------------------------------------------------
def obs0_census() -> dict:
    out: dict = {}
    lock = threading.Lock()

    def run(label, seed):
        res = sweep_host(label, seed)
        with lock:
            out[label] = res

    ths = [threading.Thread(target=run, args=(l, s), daemon=True) for l, s in SEEDS]
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    return out


def parent_window() -> tuple:
    p = json.loads((repo_root() / PARENT_PROVENANCE).read_text(encoding="utf-8"))
    tl = p.get("timeline_utc", {})

    def parse(s):
        s = (s or "").split(" ")[0].strip()
        if not s.endswith("Z"):
            return None
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc).timestamp()

    return parse(tl.get("scored_run_started")), parse(tl.get("scored_run_finished"))




def summarize(rows0: list, rows1: list, selfpairs: list, probes0: list,
              retro_rows: list, retro_info: dict, census: dict, controls: list,
              code_sha: str, sleep_s: float, gets_controls: int, gets_obs0: int,
              gets_total: int) -> dict:
    """Pure derivation: RAW rows -> DERIVED metrics -> frozen decision.

    Extracted as a pure function so that the whole measurement -> decision path
    can be exercised offline on synthetic rows (control C-SUMMARY-PIPELINE)
    without any external network traffic.
    """
    host_of = {r["url"]: r["host"] for r in rows0}
    hop_of = {r["url"]: r["hop"] for r in rows0}
    paired_all = [r for r in rows1 if r["status"] == 200 and r["host"] is not None
                  and r["hop"] is not None and r["dt_s"] is not None]
    # ELIGIBLE analysis set: pages whose measured separation is at least
    # DT_MIN_S.  The rule is timestamp-based and outcome-independent, so it
    # cannot select on whether a page changed; pages below the floor are
    # reported, never silently analysed at too short a lag.
    paired = [r for r in paired_all if r["dt_s"] >= DT_MIN_S]
    all_cens = [r for r in rows1 if r["host"] is not None and r["hop"] is not None
                and r["status"] != 200]

    def stratum(name: str):
        deep = name == "DEEP"
        sel = [r for r in paired if (r["hop"] >= SHALLOW_MAX_HOP + 1) == deep]
        cens = [r for r in all_cens if (r["hop"] >= SHALLOW_MAX_HOP + 1) == deep]
        return sel, cens

    metrics: dict = {"M-GETS-TOTAL": gets_total}
    for name in ("DEEP", "SHALLOW", "ALL"):
        if name == "ALL":
            sel, cens = paired, all_cens
        else:
            sel, cens = stratum(name)
        n = len(sel)
        k_text = sum(1 for r in sel if r["text_changed"])
        k_byte = sum(1 for r in sel if r["byte_changed"])
        metrics["M-N-PAIR-" + name] = n
        metrics["M-CHANGE-TEXT-" + name] = k_text
        metrics["M-CHANGE-BYTE-" + name] = k_byte
        metrics["M-CHANGE-RATE-TEXT-" + name] = (k_text / n) if n else None
        metrics["M-CHANGE-ATTR-ONLY-" + name] = sum(
            1 for r in sel if r["byte_changed"] and not r["text_changed"])
        metrics["M-CHANGE-TRANSPORT-" + name] = sum(
            1 for r in sel if r["transport_changed"])
        metrics["M-HAZARD-TEXT-UB95-" + name] = cp_ub95(k_text, n)
        metrics["M-HAZARD-BYTE-UB95-" + name] = cp_ub95(k_byte, n)
        metrics["M-CERT-LEVEL-TEXT-" + name] = cert_level(k_text, n)
        metrics["M-CENSORED-" + name] = len(cens)
        metrics["M-CENSOR-FRAC-" + name] = (len(cens) / float(n + len(cens))) if (n + len(cens)) else None
        if name == "ALL":
            continue
        dead = sum(1 for r in cens if r["status"] in (404, 410))
        metrics["M-DEAD-404-" + name] = dead
        metrics["M-DEAD-UB95-" + name] = cp_ub95(dead, n + len(cens))
        metrics["M-UNREACHABLE-" + name] = len(cens) - dead
        metrics["M-RATE-LIMITED-" + name] = sum(
            1 for r in cens if r["status"] in (429, 403, 503))
        if n:
            for c in ("VERSION_PINNED", "MOVING_ALIAS", "OTHER"):
                metrics["M-CLASS-FRAC-%s-%s" % (c, name)] = sum(
                    1 for r in sel if r["url_class"] == c) / float(n)
                metrics["M-CHANGE-BY-CLASS-%s-%s" % (c, name)] = sum(
                    1 for r in sel if r["url_class"] == c and r["text_changed"])
        else:
            for c in ("VERSION_PINNED", "MOVING_ALIAS", "OTHER"):
                metrics["M-CLASS-FRAC-%s-%s" % (c, name)] = None
                metrics["M-CHANGE-BY-CLASS-%s-%s" % (c, name)] = 0
        hc: dict = {}
        for r in sel:
            hc[r["host"]] = hc.get(r["host"], 0) + 1
        metrics["M-HOST-CONC-MAX-" + name] = (max(hc.values()) / float(n)) if (n and hc) else None
    dts = sorted(r["dt_s"] for r in paired)
    dts_all = sorted(r["dt_s"] for r in paired_all)
    metrics["M-N-PAIR-EXCLUDED-BELOW-DT-MIN"] = len(paired_all) - len(paired)
    metrics["M-DT-MIN-S"] = dts[0] if dts else None
    metrics["M-DT-MEDIAN-S"] = dts[int(0.5 * (len(dts) - 1))] if dts else None
    metrics["M-DT-P90-S"] = dts[int(0.9 * (len(dts) - 1))] if dts else None
    metrics["M-DT-MAX-S"] = dts_all[-1] if dts_all else None
    metrics["M-DT-MEDIAN-ALLPAIRS-S"] = (dts_all[int(0.5 * (len(dts_all) - 1))]
                                         if dts_all else None)
    hosts_both = 0
    host_table: dict = {}
    for h in sorted({r["host"] for r in paired}):
        d = [r for r in paired if r["host"] == h and r["hop"] >= SHALLOW_MAX_HOP + 1]
        s = [r for r in paired if r["host"] == h and r["hop"] <= SHALLOW_MAX_HOP]
        host_table[h] = {"n_deep": len(d),
                         "k_text_deep": sum(1 for r in d if r["text_changed"]),
                         "n_shallow": len(s),
                         "k_text_shallow": sum(1 for r in s if r["text_changed"])}
        if len(d) >= MIN_HOST_STRATUM_N and len(s) >= MIN_HOST_STRATUM_N:
            hosts_both += 1
    metrics["M-HOST-TABLE"] = host_table
    metrics["M-HOSTS-WITH-BOTH-STRATA"] = hosts_both
    metrics["M-CONCENTRATION-P-ONE-SIDED"] = contrast_p(
        metrics["M-CHANGE-TEXT-DEEP"], metrics["M-N-PAIR-DEEP"],
        metrics["M-CHANGE-TEXT-SHALLOW"], metrics["M-N-PAIR-SHALLOW"])
    metrics["M-CONCENTRATION-MDC-RATE"] = mdc_deep_rate(
        metrics["M-N-PAIR-DEEP"], metrics["M-N-PAIR-SHALLOW"])
    metrics["M-CONCENTRATION-DETECTED"] = bool(
        metrics["M-CONCENTRATION-P-ONE-SIDED"] <= ALPHA
        and metrics["M-CHANGE-TEXT-DEEP"] > metrics["M-CHANGE-TEXT-SHALLOW"])
    pos = [r for r in probes0 if r["role"] == "pos"]
    null = [r for r in probes0 if r["role"] == "null"]
    metrics["M-LIVE-POS-CHANGED"] = sum(
        1 for r in pos if r["obs"] == 1 and r["status"] == 200 and r.get("text_changed"))
    metrics["M-LIVE-POS-OK"] = sum(1 for r in pos if r["obs"] == 1 and r["status"] == 200)
    metrics["M-LIVE-NULL-CHANGED"] = sum(
        1 for r in null if r["obs"] == 1 and r["status"] == 200 and r.get("text_changed"))
    metrics["M-LIVE-NULL-OK"] = sum(1 for r in null if r["obs"] == 1 and r["status"] == 200)
    metrics["M-SELFPAIR-CHANGED"] = sum(1 for r in selfpairs if r["text_changed"])
    metrics["M-SELFPAIR-BYTE-CHANGED"] = sum(1 for r in selfpairs if r["byte_changed"])
    metrics["M-SELFPAIR-N"] = len(selfpairs)
    metrics["M-SELFPAIR-MAX-GAP-S"] = max([r["gap_s"] for r in selfpairs], default=None)
    metrics["M-OFFLINE-CONTROLS-PASS"] = "%d/%d" % (
        sum(1 for c in controls if c["pass"]), len(controls))
    metrics["M-OFFLINE-CONTROLS-FAILING"] = [c["control"] for c in controls if not c["pass"]]
    metrics["M-GETS-CONTROLS-OFFLINE"] = gets_controls
    metrics["M-GETS-OBS0"] = gets_obs0 - gets_controls
    metrics["M-GETS-OBS1"] = gets_total - gets_obs0
    metrics["M-N-DISCOVERED"] = len(rows0)
    metrics["M-N-ADMITTED"] = sum(1 for r in rows0 if r["status"] == 200)
    metrics["M-N-TRUNCATED"] = sum(1 for r in rows0 if r.get("truncated"))
    metrics["M-TIME-TRUNCATED-HOSTS"] = sum(1 for r in census.values() if r["time_truncated"])
    metrics["M-SHALLOW-CAPPED-HOSTS"] = sum(1 for r in census.values() if r["shallow_capped"])
    metrics["M-DEEP-CAPPED-HOSTS"] = sum(1 for r in census.values() if r["deep_capped"])
    metrics["M-SEED-ERRORS"] = {k: v["seed_error"] for k, v in census.items()
                                if v.get("seed_error")}
    metrics["M-SEPARATION-REQUESTED-S"] = sleep_s
    metrics["M-WALL-S"] = round(elapsed(), 2)
    metrics["M-PARTIAL"] = bool(elapsed() > MODULE_WALL_BUDGET_S)

    comparable = [r for r in retro_rows if r["obs1_status"] == 200]
    retro_dt_h = (sorted([r["dt_h"] for r in comparable])[len(comparable) // 2]
                  if comparable else None)
    per_host: dict = {}
    for r in comparable:
        slot = per_host.setdefault(r["host"], [0, 0])
        slot[1] += 1
        if r["byte_changed"]:
            slot[0] += 1
    max_host_rate = max([v[0] / float(v[1]) for v in per_host.values() if v[1]],
                        default=None)
    retro_info = dict(retro_info)
    retro_info.update({
        "n_comparable": len(comparable),
        "n_byte_changed": sum(1 for r in comparable if r["byte_changed"]),
        "dt_h_min": min([r["dt_h"] for r in comparable], default=None),
        "dt_h_median": sorted([r["dt_h"] for r in comparable])[len(comparable) // 2]
        if comparable else None,
        "dt_h_max": max([r["dt_h"] for r in comparable], default=None),
        "max_per_host_change_rate": max_host_rate,
        "negotiation_suspected": bool(max_host_rate is not None and max_host_rate >= 0.90)})
    retro_info["admitted"] = bool(
        comparable and retro_dt_h is not None
        and RETRO_MIN_WINDOW_H <= retro_dt_h <= RETRO_MAX_WINDOW_D * 24.0
        and not retro_info["negotiation_suspected"])
    if not retro_info["admitted"]:
        retro_info["not_admitted_reason"] = (
            "no comparable pages" if not comparable else
            ("negotiation artifact suspected" if retro_info["negotiation_suspected"]
             else ("measured window %.3f h outside [%.1f h, %.1f d]"
                   % (retro_dt_h, RETRO_MIN_WINDOW_H, RETRO_MAX_WINDOW_D))))
    for name in ("ALL", "SHALLOW", "DEEP"):
        if name == "ALL":
            sel = comparable
        else:
            sel = [r for r in comparable
                   if (r["hop"] >= SHALLOW_MAX_HOP + 1) == (name == "DEEP")]
        k = sum(1 for r in sel if r["byte_changed"])
        metrics["M-RETRO-N-" + name] = len(sel)
        metrics["M-RETRO-CHANGE-BYTE-" + name] = k
        metrics["M-RETRO-UB95-" + name] = cp_ub95(k, len(sel))
        metrics["M-RETRO-CERT-LEVEL-" + name] = cert_level(k, len(sel))
    metrics["M-RETRO-INFO"] = retro_info

    control_ok = (metrics["M-LIVE-POS-CHANGED"] >= 1
                  and metrics["M-LIVE-NULL-CHANGED"] == 0
                  and metrics["M-SELFPAIR-CHANGED"] == 0
                  and metrics["M-LIVE-POS-OK"] >= 2
                  and metrics["M-LIVE-NULL-OK"] == 2
                  and metrics["M-SELFPAIR-N"] == SELFPAIR_N
                  and not metrics["M-OFFLINE-CONTROLS-FAILING"])
    dt_max = metrics["M-DT-MAX-S"]
    frame_ok = (not metrics["M-SEED-ERRORS"]
                and sleep_s >= DT_MIN_S
                and dt_max is not None and dt_max <= DT_MAX_S
                and metrics["M-N-PAIR-ALL"] > 0
                and (gets_total - gets_controls) <= GET_CEILING_TOTAL)
    decision = decide({
        "control_ok": control_ok, "frame_ok": frame_ok,
        "n_deep": metrics["M-N-PAIR-DEEP"], "n_shallow": metrics["M-N-PAIR-SHALLOW"],
        "k_text_deep": metrics["M-CHANGE-TEXT-DEEP"],
        "k_text_shallow": metrics["M-CHANGE-TEXT-SHALLOW"],
        "censor_frac_deep": metrics["M-CENSOR-FRAC-DEEP"] or 0.0,
        "censor_frac_shallow": metrics["M-CENSOR-FRAC-SHALLOW"] or 0.0,
        "host_conc_deep": metrics["M-HOST-CONC-MAX-DEEP"] or 0.0,
        "host_conc_shallow": metrics["M-HOST-CONC-MAX-SHALLOW"] or 0.0,
        "hosts_both": metrics["M-HOSTS-WITH-BOTH-STRATA"],
        "verpin_frac_deep": metrics["M-CLASS-FRAC-VERSION_PINNED-DEEP"] or 0.0,
        "verpin_frac_shallow": metrics["M-CLASS-FRAC-VERSION_PINNED-SHALLOW"] or 0.0})
    return {"metrics": metrics, "decision": decision,
            "validity": {"control_ok": control_ok, "frame_ok": frame_ok,
                         "retro_admitted": retro_info["admitted"]},
            "code_sha256_stripped": code_sha}

def synthetic_rows(n_deep: int, n_shallow: int, k_deep: int, k_shallow: int,
                   censored: int = 0, dead: int = 0, dt: float = 360.0,
                   changed_deep_only: bool = False, hosts: int = 3):
    """Deterministic synthetic RAW rows for the offline pipeline control.

    Pages are spread over `hosts` hosts in BOTH strata, so the host
    identifiability and host-concentration tags are exercised with the same
    shapes the live frame is expected to have rather than with a degenerate
    one-host-per-stratum frame.
    """
    rows0: list = []
    rows1: list = []
    ks = 0 if changed_deep_only else k_shallow
    uid = 0
    names = ["h%d" % i for i in range(hosts)]
    for stratum_name, total, k in (("DEEP", n_deep, k_deep),
                                   ("SHALLOW", n_shallow, ks)):
        hop = 3 if stratum_name == "DEEP" else 2
        for i in range(total):
            uid += 1
            host = names[i % hosts]
            url = "https://%s.test/%s%05d.html" % (host, stratum_name.lower(), uid)
            cls = "VERSION_PINNED" if (uid % 25 == 0) else "MOVING_ALIAS"
            rows0.append({"url": url, "host": host, "hop": hop, "obs": 0,
                          "status": 200, "sha256": "a", "text_sha256": "t",
                          "body_len": 100, "etag": "e", "last_modified": "lm",
                          "final_url": url, "content_type": "text/html",
                          "truncated": False, "error": None, "t_start": 0.0,
                          "t_end": 0.0, "url_class": cls})
            rows1.append({"url": url, "host": host, "hop": hop, "obs": 1,
                          "status": 200, "sha256": "b" if i < k else "a",
                          "text_sha256": "u" if i < k else "t",
                          "body_len": 100, "etag": "e", "last_modified": "lm",
                          "final_url": url, "content_type": "text/html",
                          "truncated": False, "error": None, "t_start": dt,
                          "t_end": dt + 0.1, "url_class": cls,
                          "dt_s": dt, "text_changed": i < k,
                          "byte_changed": i < k,
                          "transport_changed": i < k})
    for i in range(dead):
        uid += 1
        url = "https://h0.test/dead%05d.html" % uid
        rows0.append({"url": url, "host": "h0", "hop": 3, "obs": 0, "status": 200,
                      "sha256": "a", "text_sha256": "t", "body_len": 100,
                      "etag": "e", "last_modified": "lm", "final_url": url,
                      "content_type": "text/html", "truncated": False,
                      "error": None, "t_start": 0.0, "t_end": 0.0,
                      "url_class": "MOVING_ALIAS"})
        rows1.append({"url": url, "host": "h0", "hop": 3, "obs": 1, "status": 404,
                      "sha256": None, "text_sha256": None, "body_len": 0,
                      "etag": "", "last_modified": "", "final_url": url,
                      "content_type": "", "truncated": False, "error": "http_404",
                      "t_start": dt, "t_end": dt + 0.1, "url_class": "MOVING_ALIAS",
                      "dt_s": dt, "text_changed": False, "byte_changed": False,
                      "transport_changed": False})
    for i in range(max(0, censored - dead)):
        uid += 1
        url = "https://h0.test/err%05d.html" % uid
        rows0.append({"url": url, "host": "h0", "hop": 3, "obs": 0, "status": 200,
                      "sha256": "a", "text_sha256": "t", "body_len": 100,
                      "etag": "e", "last_modified": "lm", "final_url": url,
                      "content_type": "text/html", "truncated": False,
                      "error": None, "t_start": 0.0, "t_end": 0.0,
                      "url_class": "MOVING_ALIAS"})
        rows1.append({"url": url, "host": "h0", "hop": 3, "obs": 1, "status": 0,
                      "sha256": None, "text_sha256": None, "body_len": 0,
                      "etag": "", "last_modified": "", "final_url": url,
                      "content_type": "", "truncated": False, "error": "timeout",
                      "t_start": dt, "t_end": dt + 0.1, "url_class": "MOVING_ALIAS",
                      "dt_s": dt, "text_changed": False, "byte_changed": False,
                      "transport_changed": False})
    return rows0, rows1


def summary_control() -> list:
    """Offline end-to-end control of the RAW->DERIVED->decision path.

    Exercises every reachable decision label with synthetic RAW rows so that no
    branch of the frozen decision function is untested before freeze.
    """
    rows: list = []
    census = {"h0": {"time_truncated": False, "shallow_capped": False,
                     "deep_capped": False, "seed_error": None}}
    probes: list = []
    for u in ("u1", "u2", "u3"):
        probes.append({"role": "pos", "url": u, "obs": 0, "status": 200,
                       "sha256": "x", "text_sha256": "x"})
        probes.append({"role": "pos", "url": u, "obs": 1, "status": 200,
                       "sha256": "y", "text_sha256": "y", "text_changed": True,
                       "byte_changed": True})
    for u in ("n1", "n2"):
        probes.append({"role": "null", "url": u, "obs": 0, "status": 200,
                       "sha256": "x", "text_sha256": "x"})
        probes.append({"role": "null", "url": u, "obs": 1, "status": 200,
                       "sha256": "x", "text_sha256": "x", "text_changed": False,
                       "byte_changed": False})
    pairs = [{"url": "p%d" % i, "status_a": 200, "status_b": 200, "gap_s": 0.4,
              "text_changed": False, "byte_changed": False} for i in range(SELFPAIR_N)]
    ctl = [{"control": "SYNTH", "pass": True}]

    def run(nd, ns, kd, ks, cens=0, dead=0, changed_deep_only=False, dt=360.0,
            hosts=3, sep=360.0):
        r0, r1 = synthetic_rows(nd, ns, kd, ks, censored=cens, dead=dead, dt=dt,
                                changed_deep_only=changed_deep_only, hosts=hosts)
        return summarize(r0, r1, pairs, probes, [], {}, census, ctl, "sha", sep,
                         0, 10, 20)

    a = run(380, 420, 0, 0)
    rows.append({"control": "C-SUMMARY-ZERO-EVENTS",
                 "expected": "CERTIFY_BOTH_AT_0P01, no tags, n=380/420, 3 hosts span both strata",
                 "observed": "%s deep=%s shallow=%s tags=%s ub_deep=%.6f" % (
                     a["decision"]["label"], a["decision"]["certified_deep"],
                     a["decision"]["certified_shallow"], a["decision"]["tags"],
                     a["metrics"]["M-HAZARD-TEXT-UB95-DEEP"]),
                 "pass": a["decision"]["label"] == "CERTIFY_BOTH_AT_0P01"
                 and a["metrics"]["M-N-PAIR-DEEP"] == 380
                 and a["metrics"]["M-HOSTS-WITH-BOTH-STRATA"] == 3
                 and abs(a["metrics"]["M-HAZARD-TEXT-UB95-DEEP"] - 0.007853) < 5e-6})
    b = run(380, 420, 8, 0, changed_deep_only=True)
    rows.append({"control": "C-SUMMARY-DEEP-EVENTS",
                 "expected": "CERTIFY_BOTH_AT_0P05 with concentration detected (p=0.01468)",
                 "observed": "%s p=%.5f detected=%s deep_level=%s" % (
                     b["decision"]["label"],
                     b["metrics"]["M-CONCENTRATION-P-ONE-SIDED"],
                     b["metrics"]["M-CONCENTRATION-DETECTED"],
                     b["decision"]["certified_deep"]),
                 "pass": b["decision"]["label"] == "CERTIFY_BOTH_AT_0P05"
                 and b["metrics"]["M-CONCENTRATION-DETECTED"] is True
                 and abs(b["metrics"]["M-CONCENTRATION-P-ONE-SIDED"] - 0.01468) < 5e-5})
    c = run(380, 420, 0, 0, cens=40, dead=25)
    rows.append({"control": "C-SUMMARY-CENSOR-AND-DEAD",
                 "expected": "page-gone separated from change: 25 dead -> UB 0.082146; censoring 9.5% tolerated",
                 "observed": "dead_deep=%s ub=%s cens_frac=%s label=%s" % (
                     c["metrics"]["M-DEAD-404-DEEP"],
                     round(c["metrics"]["M-DEAD-UB95-DEEP"], 6),
                     round(c["metrics"]["M-CENSOR-FRAC-DEEP"], 4),
                     c["decision"]["label"]),
                 "pass": c["metrics"]["M-DEAD-404-DEEP"] == 25
                 and abs(c["metrics"]["M-DEAD-UB95-DEEP"] - 0.082146) < 5e-6
                 and c["metrics"]["M-CENSOR-FRAC-DEEP"] < CENSOR_MAX
                 and c["decision"]["label"] == "CERTIFY_BOTH_AT_0P01"})
    d = run(380, 420, 0, 0, cens=200)
    rows.append({"control": "C-SUMMARY-CENSOR-REFUSAL",
                 "expected": "REFUSE_CERTIFY_CENSORED_DEEP (stratum-specific) above CENSOR_MAX",
                 "observed": "%s cens_frac=%.3f" % (
                     d["decision"]["label"], d["metrics"]["M-CENSOR-FRAC-DEEP"]),
                 "pass": d["decision"]["label"] == "REFUSE_CERTIFY_CENSORED_DEEP"
                 and d["metrics"]["M-CENSOR-FRAC-DEEP"] > CENSOR_MAX
                 and d["metrics"]["M-CENSOR-FRAC-SHALLOW"] < CENSOR_MAX})
    e = run(40, 420, 0, 0)
    rows.append({"control": "C-SUMMARY-INSUFFICIENT-N",
                 "expected": "REFUSE_CERTIFY_INSUFFICIENT_N",
                 "observed": e["decision"]["label"],
                 "pass": e["decision"]["label"] == "REFUSE_CERTIFY_INSUFFICIENT_N"})
    f = run(380, 420, 20, 20)
    rows.append({"control": "C-SUMMARY-GUARD-BOTH",
                 "expected": "GUARD_REQUIRED_BOTH_STRATA (UB>0.05 in both strata)",
                 "observed": "%s ub_deep=%.5f ub_shallow=%.5f" % (
                     f["decision"]["label"],
                     f["metrics"]["M-HAZARD-TEXT-UB95-DEEP"],
                     f["metrics"]["M-HAZARD-TEXT-UB95-SHALLOW"]),
                 "pass": f["decision"]["label"] == "GUARD_REQUIRED_BOTH_STRATA"})
    g = run(380, 420, 20, 0, changed_deep_only=True)
    rows.append({"control": "C-SUMMARY-GUARD-DEEP-ONLY",
                 "expected": "CERTIFY_SHALLOW_GUARD_DEEP",
                 "observed": "%s deep=%s shallow=%s" % (
                     g["decision"]["label"], g["decision"]["certified_deep"],
                     g["decision"]["certified_shallow"]),
                 "pass": g["decision"]["label"] == "CERTIFY_SHALLOW_GUARD_DEEP"})
    h = run(380, 420, 0, 20)
    rows.append({"control": "C-SUMMARY-GUARD-SHALLOW-ONLY",
                 "expected": "CERTIFY_DEEP_GUARD_SHALLOW",
                 "observed": "%s deep=%s shallow=%s" % (
                     h["decision"]["label"], h["decision"]["certified_deep"],
                     h["decision"]["certified_shallow"]),
                 "pass": h["decision"]["label"] == "CERTIFY_DEEP_GUARD_SHALLOW"})
    i = run(380, 420, 0, 0, dt=120.0, sep=120.0)
    rows.append({"control": "C-SUMMARY-SHORT-SEPARATION",
                 "expected": "NO_DATA_CONTROL_OR_FRAME_FAIL when requested separation<DT_MIN_S",
                 "observed": "%s dt_median=%s control_ok=%s frame_ok=%s" % (
                     i["decision"]["label"], i["metrics"]["M-DT-MEDIAN-S"],
                     i["validity"]["control_ok"], i["validity"]["frame_ok"]),
                 "pass": i["decision"]["label"] == "NO_DATA_CONTROL_OR_FRAME_FAIL"})
    i2 = run(380, 420, 0, 0, dt=260.0, sep=360.0)
    rows.append({"control": "C-SUMMARY-ELIGIBLE-DT-FLOOR",
                 "expected": "pairs below DT_MIN_S excluded, not analysed at too short a lag",
                 "observed": "eligible=%s excluded=%s label=%s" % (
                     i2["metrics"]["M-N-PAIR-ALL"],
                     i2["metrics"]["M-N-PAIR-EXCLUDED-BELOW-DT-MIN"],
                     i2["decision"]["label"]),
                 "pass": i2["metrics"]["M-N-PAIR-EXCLUDED-BELOW-DT-MIN"] == 800
                 and i2["metrics"]["M-N-PAIR-ALL"] == 0
                 and i2["decision"]["label"] == "NO_DATA_CONTROL_OR_FRAME_FAIL"})
    j = run(380, 420, 0, 0, hosts=1)
    rows.append({"control": "C-SUMMARY-DEPTH-NOT-IDENTIFIABLE",
                 "expected": "DEPTH_NOT_IDENTIFIABLE tag when <MIN_HOSTS_BOTH hosts span both strata",
                 "observed": "%s hosts_both=%s" % (
                     j["decision"]["label"], j["metrics"]["M-HOSTS-WITH-BOTH-STRATA"]),
                 "pass": "DEPTH_NOT_IDENTIFIABLE" in j["decision"]["tags"]})
    k = run(380, 420, 0, 0)
    rows.append({"control": "C-SUMMARY-MDC-REPORTED",
                 "expected": "M-CONCENTRATION-MDC-RATE reported even with zero events (0.0158)",
                 "observed": "mdc=%s p=%s" % (
                     round(k["metrics"]["M-CONCENTRATION-MDC-RATE"], 5),
                     k["metrics"]["M-CONCENTRATION-P-ONE-SIDED"]),
                 "pass": k["metrics"]["M-CONCENTRATION-MDC-RATE"] is not None
                 and abs(k["metrics"]["M-CONCENTRATION-MDC-RATE"] - 0.015789) < 5e-5})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["controls", "all"], default="all")
    ap.add_argument("--out", required=True)
    ap.add_argument("--sleep", type=float, default=SEPARATION_S)
    ap.add_argument("--smoke", action="store_true",
                    help="obs0-only single-observation transport smoke test")
    args = ap.parse_args()
    root = repo_root()
    out = root / args.out if not args.out.startswith("/") else Path(args.out)
    (out / "raw").mkdir(parents=True, exist_ok=True)
    (out / "derived").mkdir(parents=True, exist_ok=True)

    def write_jsonl(rel: str, rows: list) -> None:
        (out / rel).write_text(
            "".join(json.dumps(r, sort_keys=True, default=str) + "\n" for r in rows),
            encoding="utf-8")

    code_sha = hashlib.sha256(
        Path(__file__).resolve().read_bytes().strip()).hexdigest()
    progress = {"stage": args.stage, "code_sha256_stripped": code_sha,
                "smoke": bool(args.smoke), "started_utc": iso(time.time()),
                "wall_budget_s": MODULE_WALL_BUDGET_S}

    controls = offline_controls() + summary_control()
    write_jsonl("raw/controls.jsonl", controls)
    (out / "derived" / "code_identity.json").write_text(
        json.dumps({"code_sha256_stripped": code_sha,
                    "path": str(Path(__file__).resolve())}, indent=2), encoding="utf-8")
    gets_controls = gets()
    progress["gets_after_offline_controls"] = gets_controls
    progress["offline_controls"] = {"n": len(controls),
                                    "passed": sum(1 for c in controls if c["pass"])}
    (out / "raw" / "PROGRESS.json").write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8")
    if args.stage == "controls":
        progress["finished_utc"] = iso(time.time())
        (out / "raw" / "PROGRESS.json").write_text(
            json.dumps(progress, indent=2, default=str), encoding="utf-8")
        print(json.dumps(progress["offline_controls"]))
        return

    # ---- observation 0: fetch-complete, stratum-reserved census --------------
    census = obs0_census()
    rows0: list = []
    for label, res in sorted(census.items()):
        ordered = sorted(res["recs"].items(),
                         key=lambda kv: (res["hop"].get(kv[0], 99), kv[0]))
        for u, rec in ordered:
            row = {k: v for k, v in rec.items() if k != "_links"}
            row.update({"host": label, "hop": res["hop"].get(u), "obs": 0,
                        "url_class": url_class(u)})
            rows0.append(row)
    write_jsonl("raw/census.jsonl", rows0)
    admitted = [r for r in rows0 if r["status"] == 200]
    progress["obs0"] = {"gets_ledger": gets(), "n_fetched": len(rows0),
                        "n_admitted": len(admitted), "wall_s": round(elapsed(), 2)}
    (out / "raw" / "PROGRESS.json").write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8")
    if args.smoke:
        progress["finished_utc"] = iso(time.time())
        (out / "raw" / "PROGRESS.json").write_text(
            json.dumps(progress, indent=2, default=str), encoding="utf-8")
        print(json.dumps(progress["obs0"], default=str))
        return

    # ---- control probes at observation 0 -------------------------------------
    probes: list = []
    for u in POS_CONTROL_URLS:
        rec = {k: v for k, v in fetch(u).items() if k != "_links"}
        rec.update({"role": "pos", "obs": 0})
        probes.append(rec)
    for u in NULL_CONTROL_URLS:
        rec = {k: v for k, v in fetch(u).items() if k != "_links"}
        rec.update({"role": "null", "obs": 0})
        probes.append(rec)

    # ---- separation ----------------------------------------------------------
    sleep_s = max(0.0, min(args.sleep, DT_MAX_S))
    progress["separation_requested_s"] = sleep_s
    (out / "raw" / "PROGRESS.json").write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8")
    time.sleep(sleep_s)

    # ---- observation 1: re-fetch of exactly the observation-0 admitted set ---
    host_of = {r["url"]: r["host"] for r in rows0}
    hop_of = {r["url"]: r["hop"] for r in rows0}
    targets = [r["url"] for r in admitted]
    if len(targets) > OBS1_TARGET_CAP:
        stride = len(targets) / float(OBS1_TARGET_CAP)
        targets = [targets[int(i * stride)] for i in range(OBS1_TARGET_CAP)]
    progress["obs1_targets"] = len(targets)
    (out / "raw" / "PROGRESS.json").write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8")
    got = fetch_many(targets, want_links=False, workers=WORKERS)
    by0 = {r["url"]: r for r in rows0}
    rows1: list = []
    for rec in got:
        base = by0.get(rec["url"])
        dt = None
        if base and base.get("t_end") and rec.get("t_start"):
            dt = rec["t_start"] - base["t_end"]
        row = {k: v for k, v in rec.items() if k != "_links"}
        both200 = bool(base is not None and base["status"] == 200 and rec["status"] == 200)
        row.update({"obs": 1, "host": host_of.get(rec["url"]),
                    "hop": hop_of.get(rec["url"]), "url_class": url_class(rec["url"]),
                    "dt_s": round(dt, 2) if dt is not None else None,
                    "text_changed": bool(both200 and base["text_sha256"] != rec["text_sha256"]),
                    "byte_changed": bool(both200 and base["sha256"] != rec["sha256"]),
                    "transport_changed": bool(
                        both200 and (base["etag"] != rec["etag"]
                                     or base["last_modified"] != rec["last_modified"]))})
        rows1.append(row)
    write_jsonl("raw/obs1.jsonl", rows1)

    # ---- within-round self-pair determinism control -------------------------
    pair_pool = targets[::max(1, len(targets) // SELFPAIR_N)][:SELFPAIR_N]
    selfpairs: list = []
    for u in pair_pool:
        a = fetch(u)
        b = fetch(u)
        selfpairs.append({"url": u, "status_a": a["status"], "status_b": b["status"],
                          "gap_s": round(b["t_start"] - a["t_end"], 3),
                          "text_changed": bool(a["status"] == 200 and b["status"] == 200
                                               and a["text_sha256"] != b["text_sha256"]),
                          "byte_changed": bool(a["status"] == 200 and b["status"] == 200
                                               and a["sha256"] != b["sha256"])})
    write_jsonl("raw/selfpair.jsonl", selfpairs)

    # ---- control probes at observation 1 -------------------------------------
    for rec0 in [p for p in probes if p["obs"] == 0]:
        rec = {k: v for k, v in fetch(rec0["url"]).items() if k != "_links"}
        rec.update({"role": rec0["role"], "obs": 1,
                    "text_changed": bool(rec0["status"] == 200 and rec["status"] == 200
                                         and rec0["text_sha256"] != rec["text_sha256"]),
                    "byte_changed": bool(rec0["status"] == 200 and rec["status"] == 200
                                         and rec0["sha256"] != rec["sha256"])})
        probes.append(rec)
    write_jsonl("raw/control_probes.jsonl", probes)

    # ---- retrospective longer-window channel (secondary, cannot relabel) -----
    p_start, p_end = parent_window()
    retro_rows: list = []
    retro_info: dict = {"parent_window_start_utc": iso(p_start),
                        "parent_window_end_utc": iso(p_end),
                        "parent_window_s": (p_end - p_start)
                        if (p_start and p_end) else None,
                        "min_window_h": RETRO_MIN_WINDOW_H,
                        "max_window_d": RETRO_MAX_WINDOW_D}
    if p_start and p_end:
        pref: dict = {}
        with (root / PARENT_CENSUS).open(encoding="utf-8") as fh:
            for line in fh:
                r = json.loads(line)
                if r.get("status") == 200 and r.get("sha256"):
                    pref[r["url"]] = r
        refs = fetch_many(sorted(pref), want_links=False, workers=WORKERS)
        for rec in refs:
            ref = pref.get(rec["url"])
            if not ref:
                continue
            retro_rows.append({
                "url": rec["url"], "host": ref.get("host"), "hop": ref.get("hop"),
                "obs1_status": rec["status"], "obs1_sha256": rec["sha256"],
                "parent_sha256": ref["sha256"], "parent_body_len": ref.get("body_len"),
                "obs1_body_len": rec["body_len"], "parent_etag": ref.get("etag"),
                "obs1_etag": rec.get("etag"),
                "byte_changed": bool(rec["status"] == 200
                                     and rec["sha256"] != ref["sha256"]),
                "dt_h": round((rec["t_start"] - p_end) / 3600.0, 3),
                "url_class": url_class(rec["url"])})
    write_jsonl("raw/retro.jsonl", retro_rows)

    # ---- derived measurements and the frozen decision -----------------------
    payload = summarize(rows0, rows1, selfpairs, probes, retro_rows, retro_info,
                        census, controls, code_sha, sleep_s,
                        gets_controls, progress["obs0"]["gets_ledger"], gets())
    payload["retro_info"] = retro_info
    payload["constants"] = {
        "SEPARATION_S": SEPARATION_S, "DT_MIN_S": DT_MIN_S, "DT_MAX_S": DT_MAX_S,
        "SHALLOW_CAP_PER_HOST": SHALLOW_CAP_PER_HOST,
        "DEEP_CAP_PER_HOST": DEEP_CAP_PER_HOST, "MIN_N_PER_STRATUM": MIN_N_PER_STRATUM,
        "CERT_GRID": list(CERT_GRID), "CENSOR_MAX": CENSOR_MAX,
        "GET_CEILING_TOTAL": GET_CEILING_TOTAL, "DEPTH": DEPTH,
        "WORKERS": WORKERS, "PER_HOST_CONCURRENCY": PER_HOST_CONCURRENCY,
        "PER_HOST_SPACING_S": PER_HOST_SPACING_S, "MAX_BODY_BYTES": MAX_BODY_BYTES}
    (out / "derived" / "metrics.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")
    (out / "derived" / "decision.json").write_text(
        json.dumps(payload["decision"], indent=2, sort_keys=True), encoding="utf-8")
    progress["finished_utc"] = iso(time.time())
    progress["wall_s"] = round(elapsed(), 2)
    progress["decision"] = payload["decision"]["label"]
    (out / "raw" / "PROGRESS.json").write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8")
    m = payload["metrics"]
    print(json.dumps({"decision": payload["decision"]["label"], "gets": gets(),
                      "n_deep": m["M-N-PAIR-DEEP"], "n_shallow": m["M-N-PAIR-SHALLOW"],
                      "k_deep": m["M-CHANGE-TEXT-DEEP"],
                      "k_shallow": m["M-CHANGE-TEXT-SHALLOW"],
                      "dt_median_s": m["M-DT-MEDIAN-S"],
                      "pos": m["M-LIVE-POS-CHANGED"], "null": m["M-LIVE-NULL-CHANGED"],
                      "selfpair": m["M-SELFPAIR-CHANGED"]}, default=str))


if __name__ == "__main__":
    main()