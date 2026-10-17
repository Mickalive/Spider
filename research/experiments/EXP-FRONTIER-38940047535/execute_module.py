#!/usr/bin/env python3
"""EXP-FRONTIER-38940047535 - maintenance/invalidation economics of a persisted
deep-path store on a live-registered population.

Frozen EXECUTE driver. stdlib-only, credential-free GET-only, single vantage.
Stages:
  controls  offline in-process HTTP fixture canaries (no external network)
  all       controls, then live census (population registration), then bounded
            revalidation cycles, then the frozen decision
Emits, under --out:
  raw/controls.jsonl, raw/control_probes.jsonl, raw/census.jsonl,
  raw/paths.jsonl, raw/store_pages.jsonl, raw/cycle_XX.jsonl,
  derived/metrics.json, derived/decision.json, raw/PROGRESS.json
"""
from __future__ import annotations

import argparse
import hashlib
import html.parser
import http.server
import json
import math
import socketserver
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# --------------------------------------------------------------------------
# frozen constants
# --------------------------------------------------------------------------
BUDGET = 250
DEPTH = 6
MIN_REL = 0.10
MIN_ABS_GETS = 5.0
ADMIT_MIN_HOP = 3
MIN_ADMITTED = 40
MIN_HOSTS = 2
TOTAL_GET_CEILING = 3200
CENSUS_HOST_BUDGET_S = 100.0
MODULE_WALL_BUDGET_S = 620.0
CYCLE_MARGIN_S = 20.0
PLANNED_CYCLES = 3
INTER_CYCLE_SLEEP_S = 60.0
REQUEST_TIMEOUT = 12.0
TOL_LADDER = (0.005, 0.01, 0.02, 0.05, 0.10)
N_CYCLE_PROBES = 6

SEEDS = [
    ("doc.rust-lang.org", "https://doc.rust-lang.org/stable/book/"),
    ("pandas.pydata.org", "https://pandas.pydata.org/docs/"),
    ("docs.readthedocs.io", "https://docs.readthedocs.io/en/stable/"),
    ("docs.pytest.org", "https://docs.pytest.org/en/stable/"),
]
PARENT_ITEMS = "research/experiments/EXP-FRONTIER-38184956362/raw/items.jsonl"
PARENT_STRUCT = "research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl"

POS_CONTROL_URLS = [
    "https://www.cloudflare.com/cdn-cgi/trace",
    "https://api.github.com/rate_limit",
    "https://timeapi.io/api/Time/current/zone?timeZone=UTC",
]
NULL_CONTROL_URLS = [
    "https://example.com/",
    "https://www.iana.org/domains/reserved",
]

ASSET_EXTS = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".zip", ".gz", ".tar", ".tgz",
    ".bz2", ".xz", ".mp3", ".mp4", ".webm", ".avi", ".mov", ".txt", ".xml",
)

T0 = time.monotonic()
GET_LEDGER = {"n": 0}


def elapsed() -> float:
    return time.monotonic() - T0


# --------------------------------------------------------------------------
# frozen decision function
# --------------------------------------------------------------------------
def pays(reference: float, candidate: float, min_abs: float = MIN_ABS_GETS) -> bool:
    need = max(MIN_REL * reference, min_abs)
    return (reference - candidate) >= need


def decide(rows, cold_batch_gets, n_items):
    """Frozen decision rule (mandate thresholds re-derived from the live census).

    A_w = per-item / no-sharing view: servicing ONE admitted item's persisted
          path costs mean_path GETs; the fair memoryful alternative is the
          amortized share of a cold re-crawl, cold_batch_gets/n_items. A_w pays
          iff mean_path <= 0.9 * (cold_batch_gets/n_items).
    B_w = store / sharing view: maintaining the WHOLE store for one cycle costs
          K_w distinct-page GETs (one fetch per distinct union page, the actual
          physical spend); the fair alternative is the cold batch re-crawl.
          B_w pays iff K_w <= 0.9 * cold_batch_gets.
    SUPPORTS  = A_w AND B_w at every measured cycle (pays per item and in aggregate).
    FALSIFIES = B_w false AND A_w false at every measured cycle (pays nowhere).
    MIXED     = every other combination. Because K <= sum_i|path_i| = N*mean_path, a
                per-item pay IMPLIES an aggregate pay, so the only MIXED sub-state this
                experiment can reach is "aggregate pays through cross-item page sharing
                while an isolated item does not pay"; the cross-cycle disagreement
                sub-state is certified by canary but cannot be produced by a frozen
                store page set.
    S-NOSHARE is the pessimistic sensitivity: the same aggregate comparison with
    a store that performs no cross-item page sharing (sum of path lengths).
    """
    if not rows or not n_items or cold_batch_gets <= 0:
        return {"outcome": "NO_DATA", "a_pays": [], "b_pays": [], "b_noshare_pays": [],
                "cold_amortized_gets": None, "batch_threshold_gets": None,
                "noshare_threshold_gets": None, "break_even_cycles": None,
                "n_items": n_items, "cycles": 0}
    cold_amort = cold_batch_gets / n_items
    batch_thr = cold_batch_gets - max(MIN_REL * cold_batch_gets, MIN_ABS_GETS)
    noshare_thr = batch_thr
    a_pays, b_pays, b_ns = [], [], []
    for r in rows:
        mp = float(r["mean_path_gets"])
        k = float(r["store_unique_gets"])
        ns = float(r["store_noshare_gets"])
        a_pays.append(pays(cold_amort, mp, min_abs=0.0))
        b_pays.append(pays(float(cold_batch_gets), k))
        b_ns.append(pays(float(cold_batch_gets), ns))
    if all(a_pays) and all(b_pays):
        outcome = "SUPPORTS"
    elif (not any(a_pays)) and (not any(b_pays)):
        outcome = "FALSIFIES"
    else:
        outcome = "MIXED"
    if all(a_pays) and all(b_ns):
        noshare = "SUPPORTS"
    elif (not any(a_pays)) and (not any(b_ns)):
        noshare = "FALSIFIES"
    else:
        noshare = "MIXED"
    return {"outcome": outcome, "a_pays": a_pays, "b_pays": b_pays,
            "b_noshare_pays": b_ns, "noshare_outcome": noshare,
            "cold_amortized_gets": cold_amort, "batch_threshold_gets": batch_thr,
            "noshare_threshold_gets": noshare_thr,
            "break_even_cycles": cold_batch_gets / rows[0]["store_unique_gets"]
            if rows[0]["store_unique_gets"] else None,
            "n_items": n_items, "cycles": len(rows)}


def wilson_upper(k: int, n: int, z: float = 1.959963984540054) -> float:
    """Wilson score 95% upper bound for a binomial proportion (0 events -> 0)."""
    if n <= 0:
        return 1.0
    p = k / n
    d = 1.0 + z * z / n
    centre = p + z * z / (2 * n)
    rad = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return min(1.0, (centre + rad) / d)


def poisson_ub(events: int, person_seconds: float) -> float:
    """Exact one-sided 95% upper bound on an incidence rate (Garwood, pure math).
    events == 0 reduces to the rule of three."""
    if person_seconds <= 0:
        return float("inf")
    if events <= 0:
        return 3.0 / person_seconds
    k = events
    while True:
        lam = k / person_seconds
        # P(X >= k | lam)
        term = math.exp(-lam)
        cum = term
        for i in range(1, k):
            term *= lam / i
            cum += term
        if (1.0 - cum) <= 0.05:
            return lam
        k += 1
        if k > 100000:
            return lam


# --------------------------------------------------------------------------
# transport (norm/is_asset/static_links/fetch mirror the bound parent policy)
# --------------------------------------------------------------------------
class _LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            d = dict(attrs)
            href = d.get("href")
            if href:
                self.hrefs.append(href)


def repo_root() -> Path:
    p = Path(__file__).resolve()
    for anc in [p.parent] + list(p.parents):
        if (anc / "research" / "lanes" / "registry.json").is_file():
            return anc
    return Path.cwd()


def norm(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    scheme = p.scheme.lower()
    netloc = p.netloc.lower()
    if ":" in netloc and not netloc.endswith("]"):
        host, _, port = netloc.rpartition(":")
        if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
            netloc = host
    path = p.path or "/"
    return urllib.parse.urlunsplit((scheme, netloc, path, p.query, ""))


def is_asset(url: str) -> bool:
    return urllib.parse.urlsplit(url).path.lower().endswith(ASSET_EXTS)


def static_links(base: str, body: bytes) -> list:
    lp = _LinkParser()
    try:
        lp.feed(body.decode("utf-8", "replace"))
    except Exception:
        return []
    out = []
    for h in lp.hrefs:
        u = urllib.parse.urljoin(base, h.strip())
        if urllib.parse.urlsplit(u).scheme not in ("http", "https"):
            continue
        if is_asset(u):
            continue
        out.append(u)
    return out


def fetch(url: str, timeout: float = REQUEST_TIMEOUT, sleep: float = 0.0) -> dict:
    t0 = time.monotonic()
    GET_LEDGER["n"] += 1
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "spider-r2/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            rec = {"status": int(r.status), "body_len": len(body),
                   "sha256": hashlib.sha256(body).hexdigest(),
                   "final_url": norm(r.geturl()),
                   "content_type": (r.headers.get("Content-Type") or "").split(";")[0].strip(),
                   "etag": r.headers.get("ETag") or "",
                   "last_modified": r.headers.get("Last-Modified") or "",
                   "elapsed": time.monotonic() - t0, "error": None, "body": body}
    except urllib.error.HTTPError as e:
        try:
            e.read()
        except Exception:
            pass
        rec = {"status": int(e.code), "body_len": 0, "sha256": None,
               "final_url": norm(url), "content_type": "", "etag": "",
               "last_modified": "", "elapsed": time.monotonic() - t0,
               "error": "http_%d" % e.code, "body": b""}
    except Exception as e:
        rec = {"status": 0, "body_len": 0, "sha256": None, "final_url": norm(url),
               "content_type": "", "etag": "", "last_modified": "",
               "elapsed": time.monotonic() - t0, "error": repr(e)[:120], "body": b""}
    if sleep:
        time.sleep(sleep)
    return rec


def bfs_census(seed: str, sleep: float = 0.0,
                deadline: float | None = None) -> dict:
    """Mirror of the bound parent bfs_with_parents (same-host static <a>,
    item-blind FIFO, budget BUDGET, depth DEPTH, each URL fetched at most once,
    seed anchor = netloc of the seed's FINAL url). Only recording is extended."""
    parent, hop, ordinal = {}, {}, {}
    out = set()
    time_truncated = False
    records, requests_log = {}, []
    gets = 0
    seed_n = norm(seed)
    rec = fetch(seed_n, sleep=sleep)
    gets += 1
    records[seed_n] = rec
    requests_log.append({"url": seed_n, "status": rec["status"], "gets": gets})
    if rec["status"] != 200:
        return {"seed_error": rec["error"] or ("status=%d" % rec["status"]),
                "parent": parent, "hop": hop, "ordinal": ordinal, "out": out,
                "records": records, "gets": gets, "requests": requests_log,
                "seed_host": None, "time_truncated": False}
    seed_host = urllib.parse.urlsplit(rec["final_url"]).netloc.lower()
    parent[seed_n] = None
    hop[seed_n] = 0
    ordinal[seed_n] = 1
    out.add(seed_n)
    seed_body = rec["body"]
    queue = [(seed_n, 0)]
    while queue and len(out) < BUDGET:
        if deadline is not None and time.monotonic() > deadline:
            time_truncated = True
            break
        u, h = queue.pop(0)
        if h + 1 > DEPTH:
            continue
        body = seed_body if u == seed_n else None
        base = rec["final_url"] if u == seed_n else None
        if body is None:
            r = fetch(u, sleep=sleep)
            gets += 1
            records[u] = r
            requests_log.append({"url": u, "status": r["status"], "gets": gets})
            if r["status"] != 200:
                continue
            body = r["body"]
            base = r["final_url"]
        for raw in static_links(base, body):
            nu = norm(raw)
            if nu in out:
                continue
            if urllib.parse.urlsplit(nu).netloc.lower() != seed_host:
                continue
            parent[nu] = u
            hop[nu] = h + 1
            ordinal[nu] = len(out) + 1
            out.add(nu)
            queue.append((nu, h + 1))
            if len(out) >= BUDGET:
                break
    return {"seed_error": None, "parent": parent, "hop": hop, "ordinal": ordinal,
            "out": out, "records": records, "gets": gets, "requests": requests_log,
            "seed_host": seed_host, "time_truncated": time_truncated}


def path_to(parent, url):
    if url not in parent:
        return None
    chain = []
    x = url
    guard = 0
    while x is not None and guard < 64:
        chain.append(x)
        x = parent.get(x)
        guard += 1
    return list(reversed(chain))


def classify(base_rec, rec) -> str:
    if rec["status"] == 0:
        return "DEAD"
    if rec["status"] != 200:
        return "DEAD"
    if base_rec is None:
        return "NEW"
    if rec["final_url"] != base_rec["final_url"]:
        return "MOVED"
    if rec["sha256"] != base_rec["sha256"]:
        if base_rec["content_type"] and rec["content_type"] and \
                base_rec["content_type"] != rec["content_type"]:
            return "CHANGED_CT"
        return "CHANGED"
    return "UNCHANGED"


def reval(urls, base, sleep: float = 0.0) -> dict:
    rows = []
    nbytes = 0
    t0 = time.monotonic()
    for u in urls:
        r = fetch(u, sleep=sleep)
        nbytes += r["body_len"]
        rows.append({"url": u, "status": r["status"], "final_url": r["final_url"],
                     "content_type": r["content_type"], "body_len": r["body_len"],
                     "sha256": r["sha256"], "verdict": classify(base.get(u), r)})
    return {"rows": rows, "gets": len(urls), "bytes": nbytes,
            "elapsed": time.monotonic() - t0}


# --------------------------------------------------------------------------
# offline controls (in-process HTTP fixture; no external network)
# --------------------------------------------------------------------------
_FIXTURE = {
    "/": b"<html><body><a href='/a.html'>a</a><a href='/x.html'>x</a></body></html>",
    "/a.html": b"<html><body><a href='/b.html'>b</a><a href='/item.html'>i</a></body></html>",
    "/x.html": b"<html><body><a href='/item2.html'>i2</a></body></html>",
    "/b.html": b"<html><body><a href='/item.html'>i</a></body></html>",
    "/item.html": b"<html><body>ITEM-v1</body></html>",
    "/item2.html": b"<html><body>ITEM2-v1</body></html>",
    "/moved.html": b"<html><body>MOVED-v1</body></html>",
    "/movedtarget.html": b"<html><body>MOVEDTARGET-v1</body></html>",
}
_FIXSTATE = {"deleted": set(), "mutated": False, "redirect": False}


class _FixtureHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path in _FIXSTATE["deleted"]:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if self.path == "/moved.html" and _FIXSTATE["redirect"]:
            self.send_response(302)
            self.send_header("Location", "/movedtarget.html")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        body = _FIXTURE.get(self.path)
        if body is None:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if self.path == "/item.html" and _FIXSTATE["mutated"]:
            body = body.replace(b"ITEM-v1", b"ITEM-v2")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _run_controls(out_dir: Path) -> int:
    rows = []

    def rec(cid, passed, observed):
        rows.append({"control_id": cid, "pass": bool(passed), "observed": observed})

    srv = socketserver.TCPServer(("127.0.0.1", 0), _FixtureHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        base = "http://127.0.0.1:%d" % srv.server_address[1]
        cen = bfs_census(base + "/")
        p1 = path_to(cen["parent"], norm(base + "/item.html"))
        want = [norm(base + "/"), norm(base + "/a.html"), norm(base + "/item.html")]
        rec("C-BFS-PARENT-CHAIN", p1 == want, {"path": p1, "want": want})

        items = {norm(base + "/item.html"): p1, norm(base + "/item2.html"):
                 path_to(cen["parent"], norm(base + "/item2.html"))}
        union = sorted({u for p in items.values() for u in p})
        noshare = sum(len(p) for p in items.values())
        base_map = {}
        for u in union:
            r = fetch(u)
            base_map[u] = {"final_url": r["final_url"], "sha256": r["sha256"],
                           "content_type": r["content_type"]}
        rec("C-STORE-DEDUP-ACCOUNTING",
            len(union) < noshare and len(union) == len(set(union)),
            {"distinct_union": len(union), "noshare_sum": noshare,
             "sharing_factor": noshare / len(union) if union else None})

        sig = {u: {"final_url": base_map[u]["final_url"],
                   "sha256": base_map[u]["sha256"],
                   "content_type": base_map[u]["content_type"]} for u in union}
        r0 = reval(union, sig)
        verdicts = {r["url"]: r["verdict"] for r in r0["rows"]}
        rec("C-REVAL-NOCHANGE",
            all(v == "UNCHANGED" for v in verdicts.values()),
            {"verdicts": verdicts, "gets": r0["gets"]})
        rec("C-PATH-CANARY",
            all(r["status"] == 200 for r in r0["rows"]),
            {"gets": r0["gets"], "n_union": len(union)})

        _FIXSTATE["mutated"] = True
        r1 = reval(union, sig)
        v1 = {r["url"]: r["verdict"] for r in r1["rows"]}
        rec("C-REVAL-CHANGE-DETECT",
            v1.get(norm(base + "/item.html")) == "CHANGED"
            and v1.get(norm(base + "/item2.html")) == "UNCHANGED",
            {"verdicts": v1})

        _FIXSTATE["deleted"].add("/item.html")
        r2 = reval(union, sig)
        v2 = {r["url"]: r["verdict"] for r in r2["rows"]}
        rec("C-LIVENESS-404", v2.get(norm(base + "/item.html")) == "DEAD",
            {"verdicts": v2})

        moved_url = norm(base + "/moved.html")
        rm = fetch(moved_url)
        sig_m = {moved_url: {"final_url": rm["final_url"], "sha256": rm["sha256"],
                             "content_type": rm["content_type"]}}
        _FIXSTATE["redirect"] = True
        r3 = reval([moved_url], sig_m)
        rec("C-REVAL-MOVED-REDIRECT",
            r3["rows"][0]["verdict"] == "MOVED",
            {"verdict": r3["rows"][0]["verdict"]})
        _FIXSTATE["redirect"] = False

        ub0 = poisson_ub(0, 1000.0)
        ub5 = poisson_ub(5, 1000.0)
        rec("C-HAZARD-BOUND-RULE3",
            abs(ub0 - 0.003) < 1e-12 and ub5 > ub0 and ub5 < 0.02,
            {"ub_zero": ub0, "ub_five": ub5})
        w0 = wilson_upper(0, 400)
        w7 = wilson_upper(7, 400)
        w30 = wilson_upper(30, 400)
        rec("C-WILSON-BOUND-DIRECTION",
            0.0 < w0 < 0.02 and 0.02 < w7 < 0.05 and 0.09 < w30 < 0.15
            and w0 < w7 < w30,
            {"wilson_zero": w0, "wilson_seven": w7, "wilson_thirty": w30})
        tau = {t: (t / (ub0 * 4.0) if ub0 > 0 else None) for t in TOL_LADDER}
        rec("C-TAU-LADDER-MONOTONE",
            all(tau[TOL_LADDER[i]] < tau[TOL_LADDER[i + 1]]
                for i in range(len(TOL_LADDER) - 1)),
            {"tau": tau})

        def mkrow(cycle, mean_path, k_gets, ns_gets):
            return {"cycle": cycle, "mean_path_gets": mean_path,
                    "store_unique_gets": k_gets, "store_noshare_gets": ns_gets,
                    "n_items": 10}

        d_sup = decide([mkrow(1, 3.0, 300, 600)], 926, 208)
        rec("C-DECISION-CANARY-SUPPORTS", d_sup["outcome"] == "SUPPORTS",
            {"outcome": d_sup["outcome"], "detail": d_sup})
        d_mix = decide([mkrow(1, 4.4, 201, 788)], 926, 208)
        rec("C-DECISION-CANARY-MIXED", d_mix["outcome"] == "MIXED",
            {"outcome": d_mix["outcome"], "detail": d_mix})
        d_mixw = decide([mkrow(1, 3.0, 300, 600), mkrow(2, 3.0, 931, 931)], 926, 208)
        rec("C-DECISION-CANARY-MIXED-FLIP", d_mixw["outcome"] == "MIXED",
            {"outcome": d_mixw["outcome"]})
        d_fal = decide([mkrow(1, 5.0, 931, 931)], 926, 208)
        rec("C-DECISION-CANARY-FALSIFIES", d_fal["outcome"] == "FALSIFIES",
            {"outcome": d_fal["outcome"]})
        d_nd = decide([], 926, 208)
        rec("C-DECISION-CANARY-NODATA", d_nd["outcome"] == "NO_DATA",
            {"outcome": d_nd["outcome"]})
    finally:
        srv.shutdown()

    (out_dir / "raw").mkdir(parents=True, exist_ok=True)
    with (out_dir / "raw" / "controls.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    ok = all(r["pass"] for r in rows)
    print(json.dumps({"stage": "controls", "all_pass": ok, "n": len(rows),
                      "failed": [r["control_id"] for r in rows if not r["pass"]]}))
    return 0 if ok else 1


# --------------------------------------------------------------------------
# live census + bounded revalidation cycles
# --------------------------------------------------------------------------
def _load_reference(root: Path):
    parent_urls, parent_ordinals = set(), {}
    p = root / PARENT_ITEMS
    if p.is_file():
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            it = json.loads(line)
            if it.get("live"):
                parent_urls.add(norm(it["url"]))
                parent_ordinals[norm(it["url"])] = it.get("ordinal")
    struct_ref = {}
    s = root / PARENT_STRUCT
    if s.is_file():
        for line in s.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            urls = {k: v for k, v in row.items() if isinstance(v, dict) and "hop" in v}
            if urls:
                struct_ref[row["host"]] = len(urls)
    return parent_urls, parent_ordinals, struct_ref


def _probe_controls(base, sleep: float = 0.0):
    rows = []
    for role, urls in (("pos", POS_CONTROL_URLS), ("null", NULL_CONTROL_URLS)):
        for u in urls:
            r = fetch(u, sleep=sleep)
            rows.append({"role": role, "url": u, "status": r["status"],
                         "sha256": r["sha256"], "final_url": r["final_url"],
                         "body_len": r["body_len"], "error": r["error"]})
    return rows


def _run_live(out_dir: Path, sleep: float, cycles: int):
    root = repo_root()
    raw = out_dir / "raw"
    der = out_dir / "derived"
    raw.mkdir(parents=True, exist_ok=True)
    der.mkdir(parents=True, exist_ok=True)
    parent_urls, parent_ordinals, struct_ref = _load_reference(root)

    gets0 = GET_LEDGER["n"]
    probes_t0 = _probe_controls(None, sleep=sleep)
    with (raw / "control_probes.jsonl").open("w") as fh:
        for r in probes_t0:
            fh.write(json.dumps({"obs": 0, **r}, sort_keys=True) + "\n")

    census_hosts, seed_errors = {}, {}
    for label, seed in SEEDS:
        cen = bfs_census(seed, sleep=sleep,
                         deadline=time.monotonic() + CENSUS_HOST_BUDGET_S)
        if cen["seed_error"]:
            seed_errors[label] = cen["seed_error"]
            continue
        census_hosts[label] = cen

    live_hosts = sorted(census_hosts)
    admitted, per_host = [], {}
    base_rec, t_first = {}, {}
    with (raw / "census.jsonl").open("w") as fh:
        for label in live_hosts:
            cen = census_hosts[label]
            host_adm = 0
            for u in sorted(cen["out"]):
                rec = cen["records"].get(u)
                h = cen["hop"].get(u, -1)
                ordv = cen["ordinal"].get(u, -1)
                row = {"host": label, "url": u, "hop": h, "ordinal": ordv,
                       "status": (rec or {}).get("status"),
                       "body_len": (rec or {}).get("body_len"),
                       "content_type": (rec or {}).get("content_type"),
                       "etag": (rec or {}).get("etag", ""),
                       "last_modified": (rec or {}).get("last_modified", ""),
                       "sha256": (rec or {}).get("sha256"),
                       "final_url": (rec or {}).get("final_url"),
                       "admitted": False, "in_parent_208": u in parent_urls,
                       "parent_ordinal": parent_ordinals.get(u)}
                if rec is not None and rec["status"] == 200:
                    base_rec[u] = {"final_url": rec["final_url"],
                                   "sha256": rec["sha256"],
                                   "content_type": rec["content_type"],
                                   "etag": rec["etag"],
                                   "last_modified": rec["last_modified"]}
                    t_first.setdefault(u, elapsed())
                if h >= ADMIT_MIN_HOP and rec is not None and rec["status"] == 200:
                    p = path_to(cen["parent"], u)
                    if p:
                        row["admitted"] = True
                        row["path_len"] = len(p)
                        admitted.append({"url": u, "host": label, "hop": h,
                                         "ordinal": ordv, "path": p})
                        host_adm += 1
                fh.write(json.dumps(row, sort_keys=True) + "\n")
            per_host[label] = {"n_admitted": host_adm,
                               "n_discovered": len(cen["out"]),
                               "gets": cen["gets"],
                               "n_crawled_at_record_time": len(cen["records"]),
                               "time_truncated": bool(cen["time_truncated"])}
    admitted.sort(key=lambda a: a["url"])
    with (raw / "paths.jsonl").open("w") as fh:
        for a in admitted:
            fh.write(json.dumps({"url": a["url"], "host": a["host"], "hop": a["hop"],
                                 "path": a["path"], "len": len(a["path"])},
                                sort_keys=True) + "\n")

    union_pages = sorted({u for a in admitted for u in a["path"]})
    endpoints = [a["url"] for a in admitted]
    endpoint_set = set(endpoints)
    interior_pages = [u for u in union_pages if u not in endpoint_set]
    with (raw / "store_pages.jsonl").open("w") as fh:
        for u in union_pages:
            fh.write(json.dumps({"url": u, "baseline": base_rec.get(u),
                                 "t_first_s": t_first.get(u)}, sort_keys=True) + "\n")

    n_admitted = len(admitted)
    path_lens = [len(a["path"]) for a in admitted]
    mean_path = (sum(path_lens) / n_admitted) if n_admitted else 0.0
    noshare_spend = sum(path_lens)
    cold_batch_gets = sum(per_host[h]["gets"] for h in per_host)
    cold_discovered = sum(per_host[h]["n_discovered"] for h in per_host)
    parent_overlap = sum(1 for a in admitted if a["url"] in parent_urls)

    lat = [r["elapsed"] for cen in census_hosts.values()
           for r in cen["records"].values() if r["status"] == 200]
    per_get = (sum(lat) / len(lat)) if lat else 0.2

    metrics = {
        "n_live_hosts": len(live_hosts), "seed_errors": seed_errors,
        "per_host": per_host,
        "M-CENSUS-n_admitted": n_admitted,
        "M-CENSUS-n_union_pages": len(union_pages),
        "M-CENSUS-mean_path_len": mean_path,
        "M-CENSUS-max_path_len": max(path_lens) if path_lens else 0,
        "M-COLD-BATCH-GETS": cold_batch_gets,
        "M-COLD-BATCH-DISCOVERED": cold_discovered,
        "M-COLD-BATCH-BYTES": sum((r or {}).get("body_len", 0)
                                  for cen in census_hosts.values()
                                  for r in cen["records"].values()),
        "M-COLD-BATCH-REF-STRUCT": struct_ref,
        "M-COLD-ITEM-ORDINAL": {
            "n": n_admitted,
            "mean": (sum(a["ordinal"] for a in admitted) / n_admitted) if n_admitted else None,
            "min": min((a["ordinal"] for a in admitted), default=None),
            "max": max((a["ordinal"] for a in admitted), default=None)},
        "M-CENSUS-OVERLAP-PARENT208": parent_overlap,
        "M-STORE-SHARING-FACTOR": (noshare_spend / len(union_pages)) if union_pages else None,
        "M-CENSUS-n_interior_pages": len(interior_pages),
        "M-REUSE-ITEMS-PER-PAGE": (n_admitted / len(interior_pages))
        if interior_pages else None,
        "M-CENSUS-GETS": GET_LEDGER["n"] - gets0,
        "census_elapsed_s": elapsed(),
    }

    census_gate = {
        "V3_seed_liveness": {"n_live_hosts": len(live_hosts),
                             "pass": len(live_hosts) >= MIN_HOSTS},
        "V3b_census_min_admitted": {"n_admitted": n_admitted, "min": MIN_ADMITTED,
                                    "pass": n_admitted >= MIN_ADMITTED},
        "V3c_coverage_definitional": {"n_paths": n_admitted,
                                      "n_admitted": n_admitted, "pass": True},
        "V6_denominator": {"cold_batch_gets": cold_batch_gets,
                           "n_admitted": n_admitted,
                           "pass": cold_batch_gets > 0 and n_admitted > 0},
    }
    metrics["gates_census"] = census_gate
    metrics["decision"] = {"outcome": "NO_DATA", "census_gate_failed": True,
                           "census_gate": census_gate}
    if not all(g["pass"] for g in census_gate.values()):
        metrics["M-WINDOWS-COMPLETED"] = 0
        metrics["M-TOTAL-GETS"] = GET_LEDGER["n"]
        metrics["M-MODULE-ELAPSED-S"] = elapsed()
        (der / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
        (der / "decision.json").write_text(json.dumps(metrics["decision"], indent=2,
                                                     sort_keys=True) + "\n")
        print(json.dumps({"stage": "live", "census_gate": "FAIL",
                          "gates": census_gate, "gets": GET_LEDGER["n"],
                          "elapsed_s": round(elapsed(), 1)}))
        return 0

    rows, cycle_rows = [], []
    invalid_pages, item_invalid, exposure = set(), {}, {}
    pos_changed, null_changed = False, False
    probe_base = {r["url"]: r for r in probes_t0}
    cycle = 0
    while cycle < cycles:
        est = (len(union_pages) + N_CYCLE_PROBES) * per_get \
            + INTER_CYCLE_SLEEP_S + CYCLE_MARGIN_S
        if elapsed() + est > MODULE_WALL_BUDGET_S:
            break
        if cycle > 0:
            time.sleep(INTER_CYCLE_SLEEP_S)
        cycle += 1
        t_cycle = elapsed()
        res = reval(union_pages, base_rec, sleep=sleep)
        for r in res["rows"]:
            if r["verdict"] in ("CHANGED", "DEAD", "MOVED", "CHANGED_CT"):
                invalid_pages.add(r["url"])
            if r["verdict"] == "UNCHANGED":
                exposure[r["url"]] = t_cycle - t_first.get(r["url"], 0.0)
        vmap = {x["url"]: x["verdict"] for x in res["rows"]}
        bad_v = ("CHANGED", "DEAD", "MOVED", "CHANGED_CT")
        bad = {}
        for a in admitted:
            bad_pages = [u for u in a["path"] if vmap.get(u) in bad_v]
            if bad_pages:
                item_invalid[a["url"]] = bad_pages
        # Endpoint-only ablation is a strict SUBSET of the full-path arm: every
        # admitted endpoint is already in the store's union page set, so its
        # verdicts and byte cost are read from the same cycle rows at zero extra
        # GET cost and its request count is exactly n_admitted.
        abl_bad = {u: vmap[u] for u in endpoints
                   if vmap.get(u) in ("CHANGED", "DEAD", "MOVED", "CHANGED_CT")}
        probes = _probe_controls(None, sleep=sleep)
        with (raw / "control_probes.jsonl").open("a") as fh:
            for r in probes:
                b = probe_base.get(r["url"])
                diff = bool(b) and (b["sha256"] != r["sha256"] or
                                    b["final_url"] != r["final_url"])
                if r["role"] == "pos" and diff:
                    pos_changed = True
                if r["role"] == "null" and diff:
                    null_changed = True
                fh.write(json.dumps({"obs": cycle, **r, "differs_from_obs0": diff},
                                    sort_keys=True) + "\n")
        interior_only = sorted(set(item_invalid) - set(abl_bad))
        row = {"cycle": cycle, "t_cycle_s": t_cycle,
               "n_items": n_admitted,
               "store_unique_gets": res["gets"],
               "store_unique_bytes": res["bytes"],
               "store_unique_elapsed_s": res["elapsed"],
               "store_noshare_gets": noshare_spend,
               "mean_path_gets": mean_path,
               "n_invalid_pages": len(invalid_pages),
               "n_items_invalid": len(item_invalid),
               "n_items_invalid_interior_only": len(interior_only),
               "ablation_endpoint_gets": len(endpoints),
               "ablation_endpoint_invalid": len(abl_bad),
               "ablation_endpoint_bytes": sum(x["body_len"] for x in res["rows"]
                                              if x["url"] in endpoint_set)}
        rows.append(row)
        cycle_rows.append({"cycle": cycle, "rows": res["rows"]})
        (raw / ("cycle_%02d.jsonl" % cycle)).write_text(
            "".join(json.dumps(x, sort_keys=True) + "\n" for x in res["rows"]))
        (raw / "PROGRESS.json").write_text(json.dumps(
            {"cycle": cycle, "elapsed_s": elapsed(), "gets": GET_LEDGER["n"],
             "n_invalid_pages": len(invalid_pages)}, indent=2) + "\n")

    metrics["M-WINDOWS-COMPLETED"] = len(rows)
    metrics["M-TOTAL-GETS"] = GET_LEDGER["n"]
    metrics["M-MODULE-ELAPSED-S"] = elapsed()
    if rows:
        metrics["M-REVAL-PATH-GETS"] = mean_path
        metrics["M-REVAL-UNIQUE-GETS"] = rows[0]["store_unique_gets"]
        metrics["M-REVAL-NOSHARE-GETS"] = noshare_spend
        metrics["M-REVAL-PATH-BYTES"] = rows[0]["store_unique_bytes"]
        metrics["M-REVAL-PATH-ELAPSED"] = rows[0]["store_unique_elapsed_s"]
        metrics["M-ENDPOINT-GETS"] = rows[0]["ablation_endpoint_gets"]
        metrics["M-BREAK-EVEN-DENSITY"] = (rows[0]["store_unique_gets"] / n_admitted
                                           if n_admitted else None)
        metrics["M-BREAK-EVEN-CYCLES"] = (cold_batch_gets / rows[0]["store_unique_gets"]
                                          if rows[0]["store_unique_gets"] else None)
        metrics["M-CHANGE-EVENTS"] = sum(1 for a in admitted for u in a["path"]
                                         if u in invalid_pages)
        metrics["M-DEAD-EVENTS"] = sum(
            1 for cr in cycle_rows for x in cr["rows"] if x["verdict"] == "DEAD")
        metrics["M-MOVED-EVENTS"] = sum(
            1 for cr in cycle_rows for x in cr["rows"] if x["verdict"] == "MOVED")
        metrics["M-CHANGE-RATE"] = (len(invalid_pages) / len(union_pages)
                                    if union_pages else None)
        metrics["M-DEAD-RATE"] = (metrics["M-DEAD-EVENTS"] /
                                  max(1, sum(len(cr["rows"]) for cr in cycle_rows)))
        metrics["M-FALSE-ACCEPT-NAIVE"] = (len(item_invalid) / n_admitted
                                           if n_admitted else None)
        n_pages_obs = sum(len(cr["rows"]) for cr in cycle_rows)
        ps = sum(exposure.values()) or 0.0
        ev = len(invalid_pages)
        metrics["M-STORE-PAGE-SECONDS"] = ps
        metrics["M-PAGES-OBSERVED"] = n_pages_obs
        metrics["M-N-PAGES-EVER-INVALID"] = ev
        metrics["M-HAZARD-RATE-UB95"] = poisson_ub(ev, ps) if ps > 0 else None
        metrics["M-PAGE-INVALID-UB95"] = wilson_upper(ev, len(union_pages))
        lmax = metrics["M-CENSUS-max_path_len"]
        hz = metrics["M-HAZARD-RATE-UB95"]
        if hz and lmax:
            fa = 1.0 - (1.0 - min(1.0, hz * metrics["M-MODULE-ELAPSED-S"])) ** lmax
            metrics["M-FALSE-ACCEPT-UB95"] = fa
            metrics["M-TAU-LADDER"] = {str(t): (t / (hz * lmax)) for t in TOL_LADDER}
        else:
            metrics["M-FALSE-ACCEPT-UB95"] = None
            metrics["M-TAU-LADDER"] = {str(t): None for t in TOL_LADDER}
        metrics["M-INTERIOR-ONLY-FAILS"] = rows[0]["n_items_invalid_interior_only"]
    metrics["M-LIVE-POS-CHANGE"] = pos_changed
    metrics["M-LIVE-NULL-CHANGED"] = null_changed

    decision = decide(rows, cold_batch_gets, n_admitted)
    metrics["decision"] = decision
    metrics["gates"] = {
        "V3_seed_liveness": {"n_live_hosts": len(live_hosts), "pass": len(live_hosts) >= MIN_HOSTS},
        "V3b_census_min_admitted": {"n_admitted": n_admitted, "min": MIN_ADMITTED,
                                    "pass": n_admitted >= MIN_ADMITTED},
        "V3c_coverage_definitional": {"n_paths": n_admitted, "n_admitted": n_admitted,
                                      "pass": True},
        "V4_budget": {"total_gets": GET_LEDGER["n"], "ceiling": TOTAL_GET_CEILING,
                      "pass": GET_LEDGER["n"] <= TOTAL_GET_CEILING},
        "V6_denominator": {"cold_batch_gets": cold_batch_gets, "n_admitted": n_admitted,
                           "pass": cold_batch_gets > 0 and n_admitted > 0},
        "V10_envelope": {"elapsed_s": elapsed(), "budget_s": MODULE_WALL_BUDGET_S,
                         "pass": elapsed() <= MODULE_WALL_BUDGET_S},
    }
    (der / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    (der / "decision.json").write_text(json.dumps(decision, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"stage": "live", "outcome": decision["outcome"],
                      "n_admitted": n_admitted, "n_union": len(union_pages),
                      "cold_batch_gets": cold_batch_gets, "cycles": len(rows),
                      "invalid_pages": len(invalid_pages),
                      "gets": GET_LEDGER["n"], "elapsed_s": round(elapsed(), 1)}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["controls", "all"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--sleep", type=float, default=0.0)
    ap.add_argument("--cycles", type=int, default=PLANNED_CYCLES)
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.stage == "controls":
        return _run_controls(out_dir)
    rc = _run_controls(out_dir)
    if rc != 0:
        return rc
    return _run_live(out_dir, args.sleep, args.cycles)


if __name__ == "__main__":
    raise SystemExit(main())
