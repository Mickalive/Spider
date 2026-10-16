#!/usr/bin/env python3
"""EXP-FRONTIER-38188815194 - persistence-maintenance economics of deep state-carrying paths.

Frozen EXECUTE driver. stdlib-only, credential-free GET-only.
Stages:
  controls   offline in-process HTTP fixture canaries (no external network)
  economics  network measurement over the bound frozen frame
  all        controls then economics
Emits, under --out: raw/controls.jsonl, raw/paths.jsonl, raw/economics.jsonl,
derived/metrics.json, derived/decision.json.
"""
from __future__ import annotations

import argparse
import hashlib
import html.parser
import http.server
import json
import socketserver
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BUDGET = 250
DEPTH = 6
MIN_REL = 0.10
MIN_ABS_GETS = 5.0
WINDOWS = [0, 300, 900, 1800]
TOTAL_GET_CEILING = 20000
HOSTS = [
    "doc.rust-lang.org",
    "pandas.pydata.org",
    "docs.readthedocs.io",
    "docs.pytest.org",
]
FRAME_ITEMS = "research/experiments/EXP-FRONTIER-38184956362/raw/items.jsonl"
FRAME_STRUCT = "research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl"
ASSET_EXTS = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".zip", ".gz", ".tar", ".tgz",
    ".bz2", ".xz", ".mp3", ".mp4", ".webm", ".avi", ".mov", ".txt", ".xml",
)


# --------------------------------------------------------------------------
# frozen decision function (mirrors prereg FROZEN_CODE block)
# --------------------------------------------------------------------------
def _pays(reference: float, candidate: float, min_abs: float = MIN_ABS_GETS) -> bool:
    need = max(MIN_REL * reference, min_abs)
    return (reference - candidate) >= need


def decide(rows, cold_batch_gets):
    """Frozen decision rule.

    Comparators for each window w:
      S_w  = mandate per-item comparison against the frozen search ordinal
             (always abundant on this frame -> reported, not a decision branch).
      A_w  = fully-loaded per-item comparison against cold_batch_gets/n_items
             (the per-item share of a cold re-crawl of the whole set). This is
             the memoryful, fully-loaded per-item cost and it is near-threshold,
             so it IS the per-item decision comparator.
      B_w  = batch/store comparison against cold_batch_gets (strongest fair
             memoryful baseline), pay iff reval_unique_gets <= 833.4.
    SUPPORTS  = B true at EVERY measured window (survives the memoryful baseline).
    FALSIFIES = B false at EVERY window AND A false at EVERY window.
    MIXED     = otherwise: B false while A true, or B flips across windows.
    """
    s_pays, a_pays, b_pays = [], [], []
    n_items = rows[0]["n_items"] if rows and "n_items" in rows[0] else 0
    cold_amort = (cold_batch_gets / n_items) if n_items else None
    for r in rows:
        cold = r["cold_item_gets"]
        rp = r["reval_path_gets"]
        if len(cold) == 0 or len(rp) != len(cold) or cold_amort is None:
            s_pays.append(None)
            a_pays.append(None)
            b_pays.append(None)
            continue
        s_pays.append(_pays(sum(cold) / len(cold), sum(rp) / len(rp)))
        a_pays.append(_pays(cold_amort, sum(rp) / len(rp), min_abs=0.0))
        b_pays.append(_pays(float(cold_batch_gets), float(r["reval_unique_gets"])))
    known = [i for i, x in enumerate(b_pays) if x is not None]
    if not known:
        return {"outcome": "NO_DATA",
                "search_pays": [None if x is None else bool(x) for x in s_pays],
                "amortized_pays": [None if x is None else bool(x) for x in a_pays],
                "batch_pays": [None if x is None else bool(x) for x in b_pays],
                "break_even_cycles": None,
                "cold_amortized_gets": cold_amort,
                "batch_threshold_gets": cold_batch_gets - max(MIN_REL * cold_batch_gets,
                                                               MIN_ABS_GETS)}
    b_all = bool(known) and all(b_pays[i] for i in known)
    b_any = any(b_pays[i] for i in known)
    a_any = any(x is True for x in a_pays)
    if b_all:
        outcome = "SUPPORTS"
    elif not b_any and not a_any:
        outcome = "FALSIFIES"
    else:
        outcome = "MIXED"
    t_star = None
    if rows and rows[0]["reval_unique_gets"] > 0:
        t_star = cold_batch_gets / rows[0]["reval_unique_gets"]
    return {"outcome": outcome,
            "search_pays": [None if x is None else bool(x) for x in s_pays],
            "amortized_pays": [None if x is None else bool(x) for x in a_pays],
            "batch_pays": [None if x is None else bool(x) for x in b_pays],
            "break_even_cycles": t_star,
            "cold_amortized_gets": cold_amort,
            "batch_threshold_gets": cold_batch_gets - max(MIN_REL * cold_batch_gets,
                                                           MIN_ABS_GETS)}


# --------------------------------------------------------------------------
# helpers (mirror the bound parent BFS policy)
# --------------------------------------------------------------------------
def repo_root() -> Path:
    p = Path(__file__).resolve()
    for anc in [p.parent] + list(p.parents):
        if (anc / "research" / "lanes" / "registry.json").is_file():
            return anc
    return Path.cwd()


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


def fetch(url: str, timeout: float = 12.0):
    t0 = time.monotonic()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "spider-r2/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return {"status": r.status, "body": body, "final_url": r.geturl(),
                    "elapsed": time.monotonic() - t0}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "body": b"", "final_url": url,
                "elapsed": time.monotonic() - t0}
    except Exception as e:  # network/DNS/TLS failure
        return {"status": 0, "body": b"", "final_url": url, "error": repr(e),
                "elapsed": time.monotonic() - t0}


def bfs_with_parents(seed: str, sleep: float = 0.0):
    """Mirror of bound parent bfs_structural: item-blind FIFO, same-host static
    <a>, budget 250, depth 6, each URL fetched at most once; records parents."""
    parent = {}
    hop = {}
    ordinal = {}
    out = set()
    seed_n = norm(seed)
    rec = fetch(seed)
    if sleep:
        time.sleep(sleep)
    if rec["status"] != 200:
        return {"seed_error": rec.get("error") or f"status={rec['status']}",
                "parent": parent, "hop": hop, "ordinal": ordinal, "gets": 1,
                "requests": [{"url": seed_n, "status": rec["status"], "gets": 1}]}
    seed_host = urllib.parse.urlsplit(rec["final_url"]).netloc.lower()
    parent[seed_n] = None
    hop[seed_n] = 0
    ordinal[seed_n] = 1
    out.add(seed_n)
    seed_body = rec["body"]
    queue = [(seed_n, 0)]
    gets = 1
    requests_log = [{"url": seed_n, "status": rec["status"], "gets": 1}]
    while queue and len(out) < BUDGET:
        u, h = queue.pop(0)
        if h + 1 > DEPTH:
            continue
        body = seed_body if u == seed_n else None
        base = rec["final_url"] if u == seed_n else None
        if body is None:
            r = fetch(u)
            gets += 1
            requests_log.append({"url": u, "status": r["status"], "gets": gets})
            if sleep:
                time.sleep(sleep)
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
    return {"parent": parent, "hop": hop, "ordinal": ordinal, "gets": gets,
            "requests": requests_log, "seed_host": seed_host}


def path_to(parent, url):
    if url not in parent:
        return None
    chain = []
    x = url
    while x is not None:
        chain.append(x)
        x = parent.get(x)
    return list(reversed(chain))


def snapshot_path(path, sleep: float = 0.0):
    sig = {}
    gets = 0
    for u in path:
        r = fetch(u)
        gets += 1
        if sleep:
            time.sleep(sleep)
        sig[u] = {"status": r["status"],
                  "sha256": hashlib.sha256(r["body"]).hexdigest()}
    return sig, gets


def revalidate_path(path, sig):
    gets = 0
    changed, dead = [], []
    bytes_in = 0
    t0 = time.monotonic()
    for u in path:
        r = fetch(u)
        gets += 1
        bytes_in += len(r["body"])
        if r["status"] != 200:
            dead.append(u)
        elif sig[u]["sha256"] != hashlib.sha256(r["body"]).hexdigest():
            changed.append(u)
    return {"gets": gets, "changed": changed, "dead": dead,
            "bytes": bytes_in, "elapsed": time.monotonic() - t0}


# --------------------------------------------------------------------------
# controls (offline in-process fixture)
# --------------------------------------------------------------------------
_FIXTURE = {
    "/": b"<html><body><a href='/a.html'>a</a></body></html>",
    "/a.html": b"<html><body><a href='/b.html'>b</a></body></html>",
    "/b.html": b"<html><body><a href='/item.html'>i</a></body></html>",
    "/item.html": b"<html><body>ITEM-v1</body></html>",
}
_FIXSTATE = {"deleted": set(), "mutated": False}


class _FixtureHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path in _FIXSTATE["deleted"]:
            self.send_response(404)
            self.end_headers()
            return
        body = _FIXTURE.get(self.path)
        if body is None:
            self.send_response(404)
            self.end_headers()
            return
        if self.path == "/item.html" and _FIXSTATE["mutated"]:
            body = body.replace(b"ITEM-v1", b"ITEM-v2")
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _run_controls(out_dir: Path):
    rows = []

    def rec(cid, passed, observed):
        rows.append({"control_id": cid, "pass": bool(passed), "observed": observed})

    srv = socketserver.TCPServer(("127.0.0.1", 0), _FixtureHandler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        bfs = bfs_with_parents(base + "/")
        p = path_to(bfs["parent"], base + "/item.html")
        want = [base + "/", base + "/a.html", base + "/b.html", base + "/item.html"]
        rec("C-BFS-PARENT-CHAIN", p == want, {"path": p})

        sig, sg = snapshot_path(p)
        rec("C-PATH-CANARY", all(v["status"] == 200 for v in sig.values()),
            {"path_len": len(p), "snapshot_gets": sg})

        r0 = revalidate_path(p, sig)
        rec("C-REVAL-NOCHANGE", r0["changed"] == [] and r0["dead"] == [],
            {"changed": r0["changed"], "dead": r0["dead"], "gets": r0["gets"]})

        _FIXSTATE["mutated"] = True
        r1 = revalidate_path(p, sig)
        rec("C-REVAL-CHANGE-DETECT", r1["changed"] == [base + "/item.html"],
            {"changed": r1["changed"]})

        _FIXSTATE["deleted"].add("/item.html")
        r2 = revalidate_path(p, sig)
        rec("C-LIVENESS-404", r2["dead"] == [base + "/item.html"],
            {"dead": r2["dead"]})

        d_sup = decide([{"cold_item_gets": [166] * 208,
                         "reval_path_gets": [5] * 208,
                         "reval_unique_gets": 700,
                         "n_items": 208}], 926)
        rec("C-DECISION-CANARY-SUPPORTS", d_sup["outcome"] == "SUPPORTS",
            {"outcome": d_sup["outcome"]})
        d_mix = decide([{"cold_item_gets": [166] * 208,
                         "reval_path_gets": [4] * 208,
                         "reval_unique_gets": 931,
                         "n_items": 208}], 926)
        rec("C-DECISION-CANARY-MIXED", d_mix["outcome"] == "MIXED",
            {"outcome": d_mix["outcome"]})
        d_mixw = decide([{"cold_item_gets": [166] * 208,
                          "reval_path_gets": [5] * 208,
                          "reval_unique_gets": 700,
                          "n_items": 208},
                         {"cold_item_gets": [166] * 208,
                          "reval_path_gets": [5] * 208,
                          "reval_unique_gets": 931,
                          "n_items": 208}], 926)
        rec("C-DECISION-CANARY-MIXED-WINDOW", d_mixw["outcome"] == "MIXED",
            {"outcome": d_mixw["outcome"]})
        d_fal = decide([{"cold_item_gets": [166] * 208,
                         "reval_path_gets": [5] * 208,
                         "reval_unique_gets": 931,
                         "n_items": 208}], 926)
        rec("C-DECISION-CANARY-FALSIFIES", d_fal["outcome"] == "FALSIFIES",
            {"outcome": d_fal["outcome"]})
    finally:
        srv.shutdown()

    (out_dir / "raw").mkdir(parents=True, exist_ok=True)
    with (out_dir / "raw" / "controls.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    ok = all(r["pass"] for r in rows)
    print(json.dumps({"stage": "controls", "all_pass": ok,
                      "n": len(rows),
                      "failed": [r["control_id"] for r in rows if not r["pass"]]}))
    return 0 if ok else 1


# --------------------------------------------------------------------------
# economics (network)
# --------------------------------------------------------------------------
def _load_frame(root: Path):
    items = [json.loads(l) for l in (root / FRAME_ITEMS).read_text().splitlines() if l.strip()]
    admitted = [i for i in items if i.get("live")]
    struct = {}
    for line in (root / FRAME_STRUCT).read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        struct[row["host"]] = row
    return admitted, struct


def _seed_for(struct_row):
    urls = {k: v for k, v in struct_row.items() if isinstance(v, dict) and "hop" in v}
    return min(urls.items(), key=lambda kv: kv[1]["hop"])[0]


def _run_economics(out_dir: Path, sleep: float, windows):
    root = repo_root()
    admitted, struct = _load_frame(root)
    by_host = {}
    for it in admitted:
        by_host.setdefault(it["host"], []).append(it)

    bfss = {}
    total_gets = 0
    cold_batch_gets = 0
    for host in HOSTS:
        if host not in struct:
            continue
        seed = _seed_for(struct[host])
        bfs = bfs_with_parents(seed, sleep=sleep)
        bfss[host] = bfs
        total_gets += bfs["gets"]
        cold_batch_gets += len({k for k, v in struct[host].items()
                                if isinstance(v, dict) and "hop" in v})

    paths = {}
    misses = []
    for host in HOSTS:
        if host not in bfss:
            continue
        for it in by_host.get(host, []):
            p = path_to(bfss[host]["parent"], norm(it["url"]))
            if p is None:
                misses.append(it["url"])
            else:
                paths[it["url"]] = p

    raw_paths = out_dir / "raw"
    raw_paths.mkdir(parents=True, exist_ok=True)
    with (raw_paths / "paths.jsonl").open("w") as fh:
        for url, p in sorted(paths.items()):
            fh.write(json.dumps({"url": url, "path": p, "len": len(p)}) + "\n")

    snapshots = {}
    snap_gets = 0
    for url, p in sorted(paths.items()):
        sig, g = snapshot_path(p, sleep=sleep)
        snapshots[url] = sig
        snap_gets += g

    econs = []
    reval_total = 0
    for w in windows:
        if w > 0:
            time.sleep(w)
        per_item_gets, unique_pages = [], set()
        changed_items, dead_items = [], []
        for url, p in sorted(paths.items()):
            r = revalidate_path(p, snapshots[url])
            per_item_gets.append(r["gets"])
            unique_pages.update(p)
            if r["dead"]:
                dead_items.append(url)
            elif r["changed"]:
                changed_items.append(url)
        reval_total += len(unique_pages)
        econs.append({"window_s": w,
                      "reval_path_gets": per_item_gets,
                      "reval_unique_gets": len(unique_pages),
                      "cold_item_gets": [it["ordinal"] for it in admitted
                                         if it["url"] in paths],
                      "n_items": len(per_item_gets),
                      "changed": changed_items,
                      "dead": dead_items})
        with (raw_paths / "economics.jsonl").open("a") as fh:
            fh.write(json.dumps({"window_s": w, "n_items": len(per_item_gets),
                                 "reval_unique_gets": len(unique_pages),
                                 "n_changed": len(changed_items),
                                 "n_dead": len(dead_items)}) + "\n")

    decision = decide(econs, cold_batch_gets)
    total = total_gets + snap_gets + reval_total
    metrics = {
        "cold_batch_gets": cold_batch_gets,
        "cold_item_ordinal_mean": sum(it["ordinal"] for it in admitted) / len(admitted),
        "n_admitted": len(admitted),
        "n_paths": len(paths),
        "n_misses": len(misses),
        "frame_fidelity_ok": len(misses) == 0,
        "total_gets": total,
        "budget_ok": total <= TOTAL_GET_CEILING,
        "windows": [{k: e[k] for k in ("window_s", "n_items", "reval_unique_gets",
                                       "n_changed", "n_dead")} for e in econs],
        "decision": decision,
    }
    der = out_dir / "derived"
    der.mkdir(parents=True, exist_ok=True)
    (der / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    (der / "decision.json").write_text(json.dumps(decision, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"stage": "economics", "outcome": decision["outcome"],
                      "cold_batch_gets": cold_batch_gets, "n_paths": len(paths),
                      "n_misses": len(misses), "total_gets": total}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["controls", "economics", "all"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--sleep", type=float, default=0.0)
    ap.add_argument("--window", type=int, default=None,
                    help="override single window for smoke; default full ladder")
    args = ap.parse_args()
    out_dir = Path(args.out)

    if args.stage in ("controls", "all"):
        rc = _run_controls(out_dir)
        if rc != 0 or args.stage == "controls":
            return rc
    windows = [args.window] if args.window is not None else list(WINDOWS)
    return _run_economics(out_dir, args.sleep, windows)


if __name__ == "__main__":
    raise SystemExit(main())
