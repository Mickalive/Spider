"""Frozen-design executor for EXP-FRONTIER-37950626378.

Lane: frontier. Target claim: C-RESIDUAL-NOVELTY.

WHAT THIS SCRIPT IS. It executes the frozen request.json / spec.json / prereg.md /
freeze.json verbatim. It does not re-design, re-freeze or amend any frozen input.
Every implementation choice that resolves an ambiguity in the frozen text is
written to derived/implementation_choices.json so that AUDIT can recompute or
dispute it.

SAFETY. HTTP GET only via Python stdlib urllib. TLS verified. No browser, no
Docker, no model key, no credentials, no cookies, no write verb, no third-party
state mutation. 0 non-GET requests are issued.

SUBSTRATE (spec.operational_definitions.substrate):
  User-Agent 'SPIDER-research-frontier-37950626378/1.0', timeout 12 s, max body
  600000 bytes, redirects followed.

PHASES.
  0 preflight     constants, environment record, frozen-input hash verification
  1 controls      POS_KNOWN_HOP_CONTROL, NEG_UNREACHABLE_CONTROL,
                  NARROW_CHAIN_CALIBRATION, BROAD_FANOUT_CALIBRATION
  2 structural    item-blind FIFO document-order BFS per frozen candidate root,
                  budget B=250, depth cap D=6, K=2 independent sessions/site
  3 costs         per admitted item RED / RACQ_PATH / RACQ_URL charges in both
                  sessions from the observed session bodies
  4 ratios        per-site and pooled NEAR-vs-DEEP ratios + break-even reuse
"""

from __future__ import annotations

import hashlib
import json
import os
import socket
import ssl
import statistics
import sys
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

# --------------------------------------------------------------------------
# 0. FROZEN CONSTANTS (spec.json / prereg.md, immutable)
# --------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-FRONTIER-37950626378"
GITHUB_RUN_ID = "37950626378"
LANE = "frontier"
CLAIM_IDS = ["C-RESIDUAL-NOVELTY"]

USER_AGENT = "SPIDER-research-frontier-37950626378/1.0"
TIMEOUT_S = 12
MAX_BODY_BYTES = 600000
BUDGET_PAGES = 250
DEPTH_CAP = 6
SESSIONS_PER_SITE = 2
MATERIALITY_FACTOR = 3.0
SESSIONS_PER_SITE = 2

BANDS = {"NEAR": (0, 1), "DEEP": (3, 4, 5, 6)}
MID_HOP = 2

BREAK_EVEN_SAVING_REQUESTS_MIN = 1
BREAK_EVEN_SAVING_BYTES_MIN = 1024

ASSET_EXTS = {
    "png", "jpg", "jpeg", "gif", "svg", "ico", "css", "js", "pdf", "zip", "gz",
    "woff", "woff2", "ttf", "otf", "mp4", "webp", "xml", "rss", "atom", "epub",
    "mobi", "mp3", "ogg", "djvu", "exe", "iso",
}

# Frozen candidate roots (spec.target_pool.candidate_roots), order preserved.
SITES = [
    ("rust_book", "https://doc.rust-lang.org/book/", "mdBook", "doc.rust-lang.org"),
    ("rust_cargo", "https://doc.rust-lang.org/cargo/", "mdBook", "doc.rust-lang.org"),
    ("rust_nomicon", "https://doc.rust-lang.org/nomicon/", "mdBook", "doc.rust-lang.org"),
    ("gnu", "https://www.gnu.org/", "GNU web", "www.gnu.org"),
    ("quotes", "https://quotes.toscrape.com/", "custom", "quotes.toscrape.com"),
    ("gentoo", "https://forums.gentoo.org/", "phpBB", "forums.gentoo.org"),
]

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXP_DIR = os.path.join(ROOT, "research", "experiments", EXPERIMENT_ID)
RAW_DIR = os.path.join(EXP_DIR, "raw")
DERIVED_DIR = os.path.join(EXP_DIR, "derived")

IMPLEMENTATION_CHOICES: list[dict] = []


def note(choice_id: str, question: str, resolution: str, effect: str) -> None:
    IMPLEMENTATION_CHOICES.append({
        "choice_id": choice_id,
        "frozen_text_is_ambiguous_about": question,
        "resolution_applied": resolution,
        "effect_on_result": effect,
    })


note("IC-01",
     "spec.operational_definitions.navigation_graph says 'same registrable host as "
     "the seed's final URL'.",
     "Implemented as exact hostname equality against the seed's final URL hostname "
     "(same host, any scheme http/https). No eTLD+1 expansion is performed.",
     "Could exclude links that a registrable-domain interpretation would admit "
     "(e.g. subdomains). Applies identically to all bands and to the controls.")

note("IC-02",
     "spec.operational_definitions.navigation_graph says edges are <a href> links "
     "'in document order' but sets no per-page link cap.",
     "No per-page link cap is applied. The only bounds are the frozen budget "
     "B=250, depth cap D=6 and each-URL-fetched-once.",
     "Matches the frozen text. If a page published more than 250 links the "
     "budget bound would dominate anyway.")

note("IC-03",
     "spec.operational_definitions.frozen_policy bounds the per-site structural "
     "crawl at B=250, but the pre-freeze BROAD_FANOUT_CALIBRATION observed "
     "requests(hop3)=932, which exceeds B=250.",
     "The two local calibration controls are executed under the identical frozen "
     "BFS policy but with a fixture page budget of 1000, sufficient to reach the "
     "first hop-3 node, exactly as the frozen pre-freeze observation did. The six "
     "real candidate roots use the frozen B=250.",
     "Does not touch the site cost measurements or the falsifier. Required to "
     "reproduce the frozen control observation; without it the GROWING branch of "
     "the frozen two-sided certificate could not be live-reproduced.")

note("IC-04",
     "spec.arms does not say whether RACQ_PATH/RACQ_URL must re-issue GETs or may "
     "reuse the bodies observed in the same session.",
     "RACQ_PATH.bytes and RACQ_URL.bytes are charged from the bodies actually "
     "fetched in the SAME session that produced RED (the structural BFS fetches "
     "every page); RACQ_PATH.requests=h+1 and RACQ_URL.requests=1 are the frozen "
     "arm definitions. No extra duplicate GET is issued for an arm because the "
     "cost unit is the GET count and the body bytes, both already observed in "
     "that session.",
     "Avoids double-charging the substrate for identical content. RED and both "
     "RACQ arms are therefore strictly paired on the same session and item set.")

note("IC-05",
     "spec.operational_definitions.hop_distance says shortest-path length 'measured "
     "by the frozen policy', which is a budgeted BFS rather than a full graph.",
     "Hop is the BFS level at which a URL is first discovered under the frozen "
     "item-blind FIFO document-order crawl (the BFS frontier order guarantees this "
     "equals the shortest path in the sub-graph explored within budget).",
     "Inside-budget pages get their true shortest-path hop; pages only reachable "
     "through edges not explored within budget are not admitted.")

note("IC-07",
     "Three frozen candidate roots (book, cargo, nomicon) share the seed host "
     "doc.rust-lang.org, and spec.metrics.per_item defines item_id = "
     "sha256(seed_host + '|' + page_url + '|' + control_name + '|' + control_type).",
     "Per-site ratios use each candidate root's own kept items (a physical page may "
     "legitimately appear under more than one root). The POOLED ratio deduplicates "
     "by the frozen stable item_id so the same physical item discovered from two "
     "doc.rust-lang.org roots is not counted twice; the number of duplicate rows "
     "removed is reported.",
     "Prevents the doc.rust-lang.org overlap from triple-weighting the pooled "
     "medians. Per-site numbers and raw rows are unaffected.")

note("IC-06",
     "prereg VN-V4 says a site whose two sessions disagree on an item's hop or "
     "request count is 'flagged and excluded with a recorded reason'.",
     "Applied literally at site level: if any same-key item in a site disagrees "
     "between session A and session B on hop or RED.requests, the whole site is "
     "excluded and the reason recorded. All raw per-session values remain in "
     "raw/observations.jsonl.",
     "Can only remove items, never add them; if that drops the pool below "
     "ADMISSION_GATE_V1 the experiment is MEASUREMENT_INVALID, never a branch.")


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


class JsonlWriter:
    def __init__(self, path: str, hash_field: str = "record_hash") -> None:
        self.path = path
        self.hash_field = hash_field
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.fh = open(path, "w", encoding="utf-8")
        self.n = 0

    def write(self, record: dict) -> None:
        rec = dict(record)
        stripped = {k: v for k, v in rec.items() if k != self.hash_field}
        rec[self.hash_field] = sha256_hex(canonical_json(stripped).encode("utf-8"))
        self.fh.write(canonical_json(rec) + "\n")
        self.fh.flush()
        self.n += 1

    def close(self) -> None:
        self.fh.close()


_SSL_CTX = ssl.create_default_context()


def http_get(url: str, attempts: int = 2) -> dict:
    """One GET, redirects followed, TLS verified, body capped at MAX_BODY_BYTES."""
    last_err = None
    for attempt in range(attempts):
        t0 = time.time()
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Connection": "close",
            },
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S, context=_SSL_CTX) as resp:
                raw = resp.read(MAX_BODY_BYTES + 1)
                truncated = len(raw) > MAX_BODY_BYTES
                raw = raw[:MAX_BODY_BYTES]
                return {
                    "ok": True, "error": None, "status": resp.status,
                    "final_url": resp.geturl(), "raw": raw,
                    "headers": [[k, v] for k, v in resp.headers.items()],
                    "truncated": truncated, "elapsed_s": round(time.time() - t0, 4),
                }
        except urllib.error.HTTPError as exc:
            raw = b""
            try:
                raw = exc.read(MAX_BODY_BYTES + 1)[:MAX_BODY_BYTES]
            except Exception:  # noqa: BLE001
                pass
            return {
                "ok": True, "error": None, "status": exc.code,
                "final_url": getattr(exc, "url", url), "raw": raw,
                "headers": [[k, v] for k, v in (exc.headers.items() if exc.headers else [])],
                "truncated": False, "elapsed_s": round(time.time() - t0, 4),
            }
        except Exception as exc:  # noqa: BLE001
            last_err = f"{type(exc).__name__}:{exc}"
            if attempt + 1 < attempts:
                time.sleep(0.8)
                continue
            return {
                "ok": False, "error": last_err, "status": None,
                "final_url": url, "raw": b"", "headers": [],
                "truncated": False, "elapsed_s": round(time.time() - t0, 4),
            }
    return {"ok": False, "error": last_err, "status": None, "final_url": url,
            "raw": b"", "headers": [], "truncated": False, "elapsed_s": 0.0}


# --------------------------------------------------------------------------
# HTML extraction (stdlib html.parser only; no browser, no JavaScript)
# --------------------------------------------------------------------------

class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.controls: list[dict] = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "input":
            name = (a.get("name") or "").strip()
            if name:
                self.controls.append({"name": name,
                                      "type": (a.get("type") or "text").lower()})
        elif tag == "select":
            name = (a.get("name") or "").strip()
            if name:
                self.controls.append({"name": name, "type": "select"})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def parse_page(body_bytes: bytes, content_type: str | None) -> PageParser:
    charset = "utf-8"
    if content_type and "charset=" in content_type.lower():
        charset = content_type.lower().split("charset=", 1)[1].split(";", 1)[0].strip()
    try:
        text = body_bytes.decode(charset, "replace")
    except Exception:  # noqa: BLE001
        text = body_bytes.decode("utf-8", "replace")
    p = PageParser()
    try:
        p.feed(text)
        p.close()
    except Exception:  # noqa: BLE001 - malformed markup must not abort the run
        pass
    return p


def is_asset_url(url: str) -> bool:
    path = urllib.parse.urlparse(url).path
    last = path.rsplit("/", 1)[-1]
    if "." not in last:
        return False
    ext = last.rsplit(".", 1)[-1].lower()
    return ext in ASSET_EXTS


def normalize_href(href: str, base: str) -> str | None:
    href = (href or "").strip()
    if not href or href.startswith(("#", "mailto:", "javascript:", "tel:", "data:",
                                    "ftp:", "file:")):
        return None
    try:
        u = urllib.parse.urljoin(base, href)
    except Exception:  # noqa: BLE001
        return None
    p = urllib.parse.urlsplit(u)
    if p.scheme not in ("http", "https"):
        return None
    url = urllib.parse.urlunsplit((p.scheme, p.netloc, p.path or "/", p.query, ""))
    if is_asset_url(url):
        return None
    return url


# --------------------------------------------------------------------------
# crawl (frozen policy)
# --------------------------------------------------------------------------

def crawl_with_items(label: str, root: str, session_idx: int, budget: int = BUDGET_PAGES,
                     depth_cap: int = DEPTH_CAP,
                     http_writer: JsonlWriter | None = None) -> dict:
    t0 = time.time()
    first = http_get(root)
    final_root = normalize_href(first["final_url"], first["final_url"]) or root
    host = urllib.parse.urlsplit(final_root).netloc
    hostname = urllib.parse.urlsplit(final_root).hostname

    pages: dict[str, dict] = {}
    order: list[str] = []
    cum_bytes = 0
    hop: dict[str, int] = {final_root: 0}
    parent: dict[str, str | None] = {final_root: None}
    seen: set[str] = {final_root}
    items: list[dict] = []
    queue: deque[str] = deque()
    cached: dict[str, dict] = {final_root: first}

    def log_get(url: str, rec: dict, hop_val: int, body_len: int) -> None:
        if http_writer is not None:
            http_writer.write({
                "site": label, "session": session_idx, "url": url,
                "final_url": rec["final_url"], "ok": rec["ok"], "status": rec["status"],
                "error": rec["error"], "hop": hop_val, "body_bytes": body_len,
                "body_sha256": sha256_hex(rec["raw"]) if rec["raw"] else None,
                "truncated": rec.get("truncated", False),
                "elapsed_s": rec.get("elapsed_s"), "fetched_at": time.time(),
            })

    # Seed
    seed_len = len(first["raw"])
    log_get(final_root, first, 0, seed_len)
    if not first["ok"] or first["status"] is None:
        return {"site": label, "session": session_idx, "root": root,
                "final_root": final_root, "host": host, "hostname": hostname,
                "ok": False, "error": first["error"] or f"status={first['status']}",
                "pages": [], "items": [], "n_get": 1, "cum_bytes": 0,
                "elapsed_s": round(time.time() - t0, 4)}
    order.append(final_root)
    cum_bytes += seed_len
    pages[final_root] = {
        "url": final_root,
        "final_url": normalize_href(first["final_url"], first["final_url"]) or final_root,
        "status": first["status"], "body_bytes": seed_len, "hop": 0,
        "fetch_index": 1, "cum_bytes": cum_bytes,
    }
    if first["status"] == 200 and first["raw"]:
        queue.append(final_root)

    while queue and len(order) < budget:
        cur = queue.popleft()
        rec = cached.pop(cur, None)
        if rec is None:
            rec = http_get(cur)
        if not rec["ok"] or rec["status"] is None:
            if cur in pages:
                pages[cur]["error"] = rec["error"]
            log_get(cur, rec, hop.get(cur, -1), len(rec["raw"]))
            continue
        body_len = len(rec["raw"])
        if cur != final_root:
            order.append(cur)
            cum_bytes += body_len
            pages[cur] = {
                "url": cur,
                "final_url": normalize_href(rec["final_url"], rec["final_url"]) or cur,
                "status": rec["status"], "body_bytes": body_len, "hop": hop[cur],
                "fetch_index": len(order), "cum_bytes": cum_bytes,
            }
            log_get(cur, rec, hop[cur], body_len)
        if rec["status"] != 200 or not rec["raw"]:
            continue
        ctype = next((v for k, v in rec["headers"] if k.lower() == "content-type"), None)
        parsed = parse_page(rec["raw"], ctype)
        for c in parsed.controls:
            items.append({
                "page_url": cur,
                "final_url": pages[cur]["final_url"],
                "control_name": c["name"], "control_type": c["type"], "hop": hop[cur],
            })
        if hop[cur] >= depth_cap:
            continue
        final_host = urllib.parse.urlsplit(rec["final_url"]).netloc
        for href in parsed.links:
            absu = normalize_href(href, rec["final_url"])
            if not absu:
                continue
            if urllib.parse.urlsplit(absu).netloc != final_host:
                continue
            if absu in seen:
                continue
            seen.add(absu)
            hop[absu] = hop[cur] + 1
            parent[absu] = cur
            queue.append(absu)

    return {
        "site": label, "session": session_idx, "root": root,
        "final_root": final_root, "host": host, "hostname": hostname,
        "ok": True, "error": None, "pages": [pages[u] for u in order],
        "items": items, "n_get": len(order), "cum_bytes": cum_bytes,
        "parent": {k: v for k, v in parent.items()},
        "elapsed_s": round(time.time() - t0, 4),
    }


# --------------------------------------------------------------------------
# local fixture controls
# --------------------------------------------------------------------------

def start_fixture(handler_cls) -> tuple[ThreadingHTTPServer, str]:
    srv = ThreadingHTTPServer(("127.0.0.1", 0), handler_cls)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    host, port = srv.server_address
    return srv, f"http://{host}:{port}/"


class NarrowChainHandler(BaseHTTPRequestHandler):
    N = 6

    def log_message(self, *a):  # silence
        pass

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/":
            idx = 0
        elif path.startswith("/p") and path[2:].isdigit():
            idx = int(path[2:])
        else:
            self.send_response(404); self.end_headers(); return
        if idx > self.N:
            self.send_response(404); self.end_headers(); return
        body = f"<html><body><h1>chain {idx}</h1>"
        if idx < self.N:
            body += f'<a href="/p{idx+1}">next</a>'
        body += "</body></html>"
        raw = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


class BroadFanoutHandler(BaseHTTPRequestHandler):
    FANOUT = 30
    MAXDEPTH = 4

    def log_message(self, *a):
        pass

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/":
            depth = 0
        else:
            segs = [s for s in path.split("/") if s]
            if segs and segs[0] == "t":
                depth = len(segs) - 1
            else:
                self.send_response(404); self.end_headers(); return
        body = f"<html><body><h1>depth {depth}</h1>"
        if depth < self.MAXDEPTH:
            for i in range(self.FANOUT):
                body += f'<a href="{path.rstrip("/")}/t/{i}">c{i}</a>' if path != "/" \
                    else f'<a href="/t/{i}">c{i}</a>'
        body += "</body></html>"
        raw = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def first_hop_request_count(cr: dict, h: int) -> int | None:
    for pg in cr["pages"]:
        if pg.get("status") == 200 and pg.get("hop") == h:
            return pg["fetch_index"]
    return None


def run_controls(http_writer: JsonlWriter) -> dict:
    controls: dict[str, dict] = {}

    # --- POS_KNOWN_HOP_CONTROL ---
    seed = "https://doc.rust-lang.org/book/"
    target = "https://doc.rust-lang.org/book/ch01-01-installation.html"
    cr = crawl_with_items("pos_control", seed, 0, budget=BUDGET_PAGES, http_writer=http_writer)
    tgt = None
    if cr.get("ok"):
        for pg in cr["pages"]:
            if normalize_href(pg["url"], pg["url"]) == target:
                tgt = pg
                break
    found = bool(tgt and tgt.get("status") == 200)
    pos_hop = tgt.get("hop") if tgt else None
    controls["POS_KNOWN_HOP_CONTROL"] = {
        "kind": "positive", "expected": {"found": True, "hop": 1, "status": 200},
        "observed": {"found": found, "hop": pos_hop,
                     "requests": tgt.get("fetch_index") if tgt else None,
                     "cum_bytes": tgt.get("cum_bytes") if tgt else None,
                     "status": tgt.get("status") if tgt else None},
        "pass": bool(found and pos_hop == 1),
    }

    # --- NEG_UNREACHABLE_CONTROL ---
    neg_target = "https://doc.rust-lang.org/book/__spider_nonexistent_37950626378__.html"
    neg_found = False
    if cr.get("ok"):
        for pg in cr["pages"]:
            if normalize_href(pg["url"], pg["url"]) == neg_target:
                neg_found = True
                break
    controls["NEG_UNREACHABLE_CONTROL"] = {
        "kind": "null/negative", "expected": {"found": False},
        "observed": {"found": neg_found}, "pass": (not neg_found),
    }

    # --- NARROW_CHAIN_CALIBRATION ---
    srv, root = start_fixture(NarrowChainHandler)
    try:
        ncr = crawl_with_items("narrow_chain", root, 0, budget=1000,
                               http_writer=http_writer)
        r1 = first_hop_request_count(ncr, 1)
        r2 = first_hop_request_count(ncr, 2)
        r3 = first_hop_request_count(ncr, 3)
        ratio = (r3 / r1) if (r1 and r3) else None
        controls["NARROW_CHAIN_CALIBRATION"] = {
            "kind": "dynamic-range FLAT",
            "expected": "requests(hop h) == h+1 and R = requests(hop3)/requests(hop1) <= 3.0",
            "observed": {"requests": {"hop1": r1, "hop2": r2, "hop3": r3},
                         "R_hop3_over_hop1": ratio},
            "pass": bool(r1 == 2 and r3 == 4 and ratio is not None and ratio <= 3.0),
        }
    finally:
        srv.shutdown()
        srv.server_close()

    # --- BROAD_FANOUT_CALIBRATION ---
    srv, root = start_fixture(BroadFanoutHandler)
    try:
        bcr = crawl_with_items("broad_fanout", root, 0, budget=1000,
                               http_writer=http_writer)
        b1 = first_hop_request_count(bcr, 1)
        b3 = first_hop_request_count(bcr, 3)
        ratio = (b3 / b1) if (b1 and b3) else None
        controls["BROAD_FANOUT_CALIBRATION"] = {
            "kind": "dynamic-range GROWING",
            "expected": "R = requests(hop3)/requests(hop1) > 3.0",
            "observed": {"requests": {"hop1": b1, "hop3": b3},
                         "R_hop3_over_hop1": ratio},
            "pass": bool(ratio is not None and ratio > 3.0),
        }
    finally:
        srv.shutdown()
        srv.server_close()

    return controls


# --------------------------------------------------------------------------
# metrics
# --------------------------------------------------------------------------

def median(vals: list[float]) -> float | None:
    return statistics.median(vals) if vals else None


def band_of(h: int) -> str:
    if h in BANDS["NEAR"]:
        return "NEAR"
    if h in BANDS["DEEP"]:
        return "DEEP"
    return "MID"


def item_key(rec: dict) -> tuple:
    return (rec["page_url"], rec["control_name"], rec["control_type"])


def build_item_costs(session_a: dict, session_b: dict) -> dict:
    """Per item, both sessions. RED from BFS prefix; RACQ from same-session bodies."""
    def index_session(cr: dict) -> dict:
        pgmap = {p["url"]: p for p in cr["pages"]}
        items = {}
        for it in cr["items"]:
            k = (it["page_url"], it["control_name"], it["control_type"])
            items[k] = it
        return pgmap, items

    pga, ita = index_session(session_a)
    pgb, itb = index_session(session_b)
    shared = sorted(set(ita) & set(itb), key=lambda k: (ita[k]["hop"], k))

    per_item = []
    reasons = {"missing_in_one_session": 0, "hop_disagreement": 0,
               "red_requests_disagreement": 0, "status_not_200": 0}
    for k in shared:
        pa = pga.get(k[0])
        pb = pgb.get(k[0])
        ia = ita[k]
        ib = itb[k]
        if pa is None or pb is None:
            reasons["missing_in_one_session"] += 1
            continue
        if pa.get("status") != 200 or pb.get("status") != 200:
            reasons["status_not_200"] += 1
            continue
        if ia["hop"] != ib["hop"]:
            reasons["hop_disagreement"] += 1
            continue
        if pa.get("fetch_index") != pb.get("fetch_index"):
            reasons["red_requests_disagreement"] += 1
            continue
        # shortest path from parent pointers (session A)
        parent = session_a.get("parent", {})
        path = [k[0]]
        while path[-1] != session_a["final_root"] and path[-1] in parent and parent[path[-1]]:
            path.append(parent[path[-1]])
        path = list(reversed(path))  # seed -> item
        path_pages = [pga[u] for u in path if u in pga]
        racq_path_bytes = sum(p.get("body_bytes", 0) for p in path_pages)
        racq_url_bytes = pa.get("body_bytes", 0)
        red_requests = pa["fetch_index"]
        red_bytes = pa["cum_bytes"]
        racq_path_requests = len(path)
        path_matches_hop = (racq_path_requests == ia["hop"] + 1)
        saving_req = red_requests - racq_path_requests
        saving_bytes = red_bytes - racq_path_bytes
        eligible = (saving_req >= BREAK_EVEN_SAVING_REQUESTS_MIN and
                    saving_bytes >= BREAK_EVEN_SAVING_BYTES_MIN)
        top_host = urllib.parse.urlsplit(session_a["final_root"]).netloc
        item_id = sha256_hex(
            f"{top_host}|{k[0]}|{k[1]}|{k[2]}".encode())
        per_item.append({
            "item_id": item_id, "site": session_a["site"],
            "site_host": session_a["host"],
            "page_url": k[0], "final_url": pa.get("final_url"),
            "control_name": k[1], "control_type": k[2],
            "hop": ia["hop"], "band": band_of(ia["hop"]),
            "red_requests": red_requests, "red_bytes": red_bytes, "red_tokens": None,
            "racq_path_requests": racq_path_requests,
            "racq_path_bytes": racq_path_bytes,
            "racq_url_requests": 1, "racq_url_bytes": racq_url_bytes,
            "path_urls": path,
            "path_len": racq_path_requests,
            "path_len_equals_hop_plus_one": path_matches_hop,
            "saving_requests": saving_req, "saving_bytes": saving_bytes,
            "break_even_eligible": eligible,
            "break_even_reuse_count_requests":
                (racq_path_requests / saving_req) if (eligible and saving_req > 0) else None,
            "break_even_reuse_count_bytes":
                (racq_path_bytes / saving_bytes) if (eligible and saving_bytes > 0) else None,
            "session_b_red_requests": pb.get("fetch_index"),
            "session_b_red_bytes": pb.get("cum_bytes"),
        })
    return {"items": per_item, "shared_item_count": len(shared),
            "exclusion_reasons": reasons}


def ratio_block(items: list[dict]) -> dict:
    deep = [i for i in items if i["band"] == "DEEP"]
    near = [i for i in items if i["band"] == "NEAR"]
    dr = median([i["red_requests"] for i in deep])
    nr = median([i["red_requests"] for i in near])
    db = median([i["red_bytes"] for i in deep])
    nb = median([i["red_bytes"] for i in near])
    rr = (dr / nr) if (dr is not None and nr) else None
    rb = (db / nb) if (db is not None and nb) else None
    if rr is None or rb is None:
        verdict = "UNDEFINED"
    elif rr <= MATERIALITY_FACTOR and rb <= MATERIALITY_FACTOR:
        verdict = "FLAT"
    elif rr > MATERIALITY_FACTOR and rb > MATERIALITY_FACTOR:
        verdict = "GROWING"
    else:
        verdict = "MIXED"
    return {
        "n_deep": len(deep), "n_near": len(near), "n_mid_excluded":
            len([i for i in items if i["band"] == "MID"]),
        "median_red_requests_deep": dr, "median_red_requests_near": nr,
        "median_red_bytes_deep": db, "median_red_bytes_near": nb,
        "ratio_requests_deep_over_near": rr, "ratio_bytes_deep_over_near": rb,
        "verdict": verdict,
    }


def break_even_block(items: list[dict]) -> dict:
    out = {}
    for band in ("NEAR", "MID", "DEEP"):
        sub = [i for i in items if i["band"] == band]
        elig_req = [i["break_even_reuse_count_requests"] for i in sub
                    if i["break_even_eligible"] and i["break_even_reuse_count_requests"] is not None]
        elig_bytes = [i["break_even_reuse_count_bytes"] for i in sub
                      if i["break_even_eligible"] and i["break_even_reuse_count_bytes"] is not None]
        out[band] = {
            "n_items": len(sub), "n_eligible": len([i for i in sub if i["break_even_eligible"]]),
            "median_break_even_reuse_count_requests": median(elig_req),
            "median_break_even_reuse_count_bytes": median(elig_bytes),
        }
    return out


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> int:
    t0 = time.time()
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DERIVED_DIR, exist_ok=True)

    # frozen input hash verification
    frozen_hashes = {}
    freeze_path = os.path.join(EXP_DIR, "freeze.json")
    with open(freeze_path) as fh:
        freeze = json.load(fh)
    verified = {}
    for name, expected in freeze["hashes"].items():
        with open(os.path.join(EXP_DIR, name), "rb") as fh:
            got = sha256_hex(fh.read())
        verified[name] = {"expected": expected, "actual": got, "match": got == expected}
    frozen_hashes = verified

    try:
        import tiktoken  # noqa: F401
        tokenizer_version = getattr(tiktoken, "__version__", "unknown")
    except Exception:  # noqa: BLE001
        tokenizer_version = None

    try:
        socket.gethostbyname("doc.rust-lang.org")
        network = "AVAILABLE"
    except Exception as exc:  # noqa: BLE001
        network = f"UNAVAILABLE:{type(exc).__name__}:{exc}"

    http_writer = JsonlWriter(os.path.join(RAW_DIR, "http.jsonl"), "record_hash")
    controls_writer = JsonlWriter(os.path.join(RAW_DIR, "controls.jsonl"), "record_hash")
    obs_writer = JsonlWriter(os.path.join(RAW_DIR, "observations.jsonl"), "observation_hash")

    # ---------------- Phase 1: controls ----------------
    print("[controls] starting", flush=True)
    controls = run_controls(http_writer)
    controls_writer.write({"phase": "controls", "controls": controls})
    print("[controls] " + json.dumps(controls), flush=True)

    # ---------------- Phase 2: structural pass ----------------
    sessions: dict[str, dict] = {}
    for label, root, engine, host in SITES:
        sitesess = {}
        for k in range(SESSIONS_PER_SITE):
            path = os.path.join(DERIVED_DIR, f"site_{label}_s{k}.json")
            cr = crawl_with_items(label, root, k, budget=BUDGET_PAGES,
                                  http_writer=http_writer)
            with open(path, "w") as fh:
                json.dump(cr, fh, indent=1, sort_keys=True)
            sitesess[k] = cr
            print(f"[structural] {label} s{k}: ok={cr['ok']} n_get={cr['n_get']} "
                  f"items={len(cr['items'])} bytes={cr['cum_bytes']}", flush=True)
        sessions[label] = sitesess

    # ---------------- admission ----------------
    site_reports = {}
    all_items: list[dict] = []
    for label, root, engine, host in SITES:
        sa = sessions[label][0]
        sb = sessions[label][1]
        if not sa.get("ok") or not sb.get("ok"):
            site_reports[label] = {
                "site": label, "engine": engine, "root": root,
                "status": "UNREACHABLE", "error_a": sa.get("error"),
                "error_b": sb.get("error"),
            }
            continue
        costs = build_item_costs(sa, sb)
        excl = costs["exclusion_reasons"]
        # VN-V4 site-level instability flag
        unstable = (excl["hop_disagreement"] > 0 or
                    excl["red_requests_disagreement"] > 0)
        for it in costs["items"]:
            it["site_unstable_excluded"] = unstable
        kept = [it for it in costs["items"] if not unstable]
        for it in kept:
            obs_writer.write({**it, "engine": engine})
        all_items.extend(kept)
        site_reports[label] = {
            "site": label, "engine": engine, "root": root,
            "final_root": sa["final_root"], "host": sa["host"],
            "sessions_ok": True, "n_get_s0": sa["n_get"], "n_get_s1": sb["n_get"],
            "items_shared": costs["shared_item_count"],
            "items_kept": len(kept),
            "exclusion_reasons": excl,
            "site_unstable_excluded": unstable,
            "n_deep_kept": len([i for i in kept if i["band"] == "DEEP"]),
            "n_near_kept": len([i for i in kept if i["band"] == "NEAR"]),
            "ratio_session_a": ratio_block(kept),
        }
        print(f"[admission] {label}: kept={len(kept)} unstable={unstable} "
              f"ratioA={site_reports[label]['ratio_session_a']['verdict']}", flush=True)

    gate = {
        "id": "ADMISSION_GATE_V1",
        "requires": {"admitted_DEEP_items_min": 5, "admitted_NEAR_items_min": 8,
                     "distinct_seed_hosts_min": 2},
        "observed": {
            "admitted_DEEP_items": len([i for i in all_items if i["band"] == "DEEP"]),
            "admitted_NEAR_items": len([i for i in all_items if i["band"] == "NEAR"]),
            "admitted_MID_items": len([i for i in all_items if i["band"] == "MID"]),
            "distinct_seed_hosts": len({i["site_host"] for i in all_items}),
        },
    }
    gate["pass"] = (gate["observed"]["admitted_DEEP_items"] >= 5 and
                    gate["observed"]["admitted_NEAR_items"] >= 8 and
                    gate["observed"]["distinct_seed_hosts"] >= 2)

    # IC-07: pooled ratio deduplicates by the frozen stable item_id so the shared
    # doc.rust-lang.org roots do not triple-count the same physical item.
    seen_ids: set[str] = set()
    pooled_items: list[dict] = []
    n_dup = 0
    for it in all_items:
        if it["item_id"] in seen_ids:
            n_dup += 1
            continue
        seen_ids.add(it["item_id"])
        pooled_items.append(it)

    pooled = ratio_block(pooled_items)
    pooled = {**pooled, "n_items_deduped": len(pooled_items),
              "n_duplicate_rows_removed": n_dup}
    breakeven = break_even_block(pooled_items)
    path_consistency = {
        "n_items": len(pooled_items),
        "n_path_len_equals_hop_plus_one":
            sum(1 for i in pooled_items if i["path_len_equals_hop_plus_one"]),
    }

    metrics = {
        "experiment_id": EXPERIMENT_ID, "lane": LANE,
        "environment": {"python": sys.version.split()[0], "platform": sys.platform,
                        "tiktoken_version": tokenizer_version,
                        "token_channel_available": tokenizer_version is not None,
                        "network": network},
        "frozen_inputs": frozen_hashes,
        "controls": controls,
        "admission_gate": gate,
        "site_reports": site_reports,
        "pooled": pooled,
        "breakeven": breakeven,
        "path_consistency": path_consistency,
        "wall_clock_seconds": round(time.time() - t0, 2),
        "n_http_get": http_writer.n,
        "n_admitted_items": len(all_items),
        "implementation_choices": IMPLEMENTATION_CHOICES,
        "per_item": all_items,
    }
    with open(os.path.join(DERIVED_DIR, "metrics.json"), "w") as fh:
        json.dump(metrics, fh, indent=1, sort_keys=True)
    with open(os.path.join(DERIVED_DIR, "implementation_choices.json"), "w") as fh:
        json.dump(IMPLEMENTATION_CHOICES, fh, indent=1)

    http_writer.close()
    controls_writer.close()
    obs_writer.close()

    print("[done] " + json.dumps({
        "gate_pass": gate["pass"], "pooled": pooled,
        "controls": {k: v["pass"] for k, v in controls.items()},
        "wall_clock_seconds": metrics["wall_clock_seconds"],
        "n_http_get": metrics["n_http_get"],
    }), flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        sys.exit(1)
