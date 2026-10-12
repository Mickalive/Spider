# EXP-FRONTIER-38188815194 preregistration

Status: DESIGN (design-contract v2). Awaiting independent design review and freeze.

Lane: `frontier`. Request: `research/experiments/EXP-FRONTIER-38188815194/request.json`
(request_hash `9db3da3eab312b40badcfdaa405fdc929cb575be808c673d74ebcd4bb1b58d6e`,
base_sha `d5d2ad8b0f01624fdeb1c324ad4277a7f116e75e`, cycle `38188115214`).
Director mandate: action `PIVOT`, target claim `C-CROSSSITE`, `cognitive_reset=true`,
reason `global-director-PIVOT`. Parent handoff: `EXP-FRONTIER-38184956362` (sha256
`ffcd914d5f1ed0447fd239b6e723fc39b73bcc4e8b13b6b468d980414e90d6d6`).

This packet refines the mandate's strategic question into the smallest rigorous
falsifiable measurement. It does not drift to the parent handoff and it does not
re-run the closed discovery experiment.

## 1. Identity, claim binding, and scope

- Target claim: `C-CROSSSITE` (registry status `HYPOTHESIS`; product capability
  "cross-site inheritance"; `next_gate` "true website holdout without site
  identity leakage"). `claim_ids=["C-CROSSSITE"]` keeps the spec inside the
  frontier lane charter (`C-WEB-DYNAMICS`, `C-RESIDUAL-NOVELTY`,
  `C-SEMANTIC-RESOLVE`, `C-CROSSSITE`).
- This experiment measures the **persistence-maintenance / invalidation
  economics** of a deep state-carrying acquisition path on the frozen
  credential-free frame. It does not validate cross-site transfer and does not
  promote `C-CROSSSITE`. At most it bounds the maintenance subthread that the
  expired discovery axis (`EXP-FRONTIER-38184956362`) opened.
- Substrate: credential-free, GET-only, stdlib `urllib`; single runner vantage;
  no LLM endpoint, no browser, no Docker, no credentials. Cost is measured in
  HTTP GETs (primary), bytes, and elapsed seconds.

## 2. Legacy and pre-2.0 disposition

- `P2-REPLAY-COST` (pre-2.0 artifact 4.114, sha
  `9687ff787f2d74460bb7006826008852f5b4416b`) withdrew an 8.5x speed claim:
  2.822 s cold vs 2.816 s replay on matched tasks = 1.002x. Binding guards
  adopted here: (i) compare on matched items with fully-loaded counterfactual
  costs; (ii) never frame scripted replay as real-agent economics; (iii) treat
  exact-path replay as a **baseline**, never as an assumed win.
- Legacy frontier volatility/freshness program (`CENSUS_REPORT_V3` sha
  `81aba1e898d96fe3c49ae9cd0f4ef00dfdad46a4`; charter-v3 closure sha
  `3bc393fc8d3c5fc2515da6e8c7481b2618fefdbe`; STAGE0R closure sha
  `0c25497a7e6b66aeb846468bacc5a51deb526470`) established that day-scale
  staleness is structurally undecidable on committed corpora (max same-target
  span 0.0218 d) and that only the seconds-to-minutes regime is measurable.
  Therefore every change/dead/false-accept statistic here is explicitly bounded
  to the session-scale regime and must never be reported as day-scale freshness.
- This is a `DISTINCT_EXTENSION`, not a rerun: it measures COST (GETs/bytes/
  elapsed) and session-scale invalidation, not a hazard rate, and it uses the
  measured same-host BFS cost plus a memoryful batch baseline.

## 3. Parent-handoff disposition (four-way, preserved)

Source: `research/experiments/EXP-FRONTIER-38184956362/handoff.json`.

- **established**: on the frozen 20-host/556-item credential-free GET-only frame
  the site-native discovery axis is validly closed — 0/208 admitted deep (hop
  3..6) state-carrying items reachable at charged <=K=3 across the five frozen
  channels (`G6 FALSIFIES`); the 208 admitted items live on four hosts
  (`doc.rust-lang.org` 13, `pandas.pydata.org` 8, `docs.readthedocs.io` 28,
  `docs.pytest.org` 159; hops 3-4; `live=true` for all 208); the frozen per-item
  cold BFS discovery/fetch ordinal has mean 166.0 (min 31, max 250).
- **rejected**: nothing from the parent is rejected here; the parent's bounded
  negative stands and is reused as the cold comparator, not re-measured.
- **unknown** (exactly what this experiment measures): session-scale
  change/dead rate of deep path pages; store-level path sharing (how many
  distinct pages the 208 paths touch after dedup); effective per-item and
  per-cycle maintenance cost; whether those costs undercut cold re-derivation.
- **do_not_assume**: that exact-path replay is cheap; that a memoryless
  (per-item) comparator alone suffices; that discovery can be profitably
  re-run; that a day-scale freshness signal exists; that any pre-freeze outcome
  fraction is known (none was measured).

## 4. Question and hypotheses

**Question.** On the frozen frame, against (a) the mandate's per-item cold
same-host BFS comparator (ordinal mean 166.0, min 31, max 250) and (b) the
strongest fair memoryful baseline (one cold re-crawl of each host per cycle,
which re-yields every deep item), does persisting a deep state-carrying path and
revalidating it (fresh GETs/bytes to replay the path for liveness and content
change) at nominal elapsed windows 0/300/900/1800 s undercut cold re-derivation;
at what break-even hop/store-reuse-density/elapsed-cycle count does persistence
stop paying; and is the naive exact-path replay false-accept rate bounded in the
measurable session regime only?

- **H1 (per-item, two comparators).** Path replay cost `~hop+1` GETs is far below
  the mandate's cold per-item *search* ordinal (mean 166), so that comparison
  pays at every window by construction (reported, not a decision branch). Against
  the **fully-loaded** per-item cost of maintaining the whole set — `926/208 =
  4.452` GETs/item, the per-item share of a cold batch re-crawl — the replay cost
  `931/208 = 4.476` GETs/item is essentially a tie, so this near-threshold
  comparison is the per-item decision comparator.
- **H2 (batch, strongest fair).** `sum_i(hop_i+1) = 931` approximately equals the
  cold batch cost `250+250+176+250 = 926`, so the memoryful batch comparison is
  near-threshold and is decided by store-level path sharing (distinct pages after
  dedup; threshold `926 - 92.6 = 833.4` GETs).
- **H3 (naive replay).** Naive exact-path replay (no revalidation) is cheap per
  use but carries a session-scale false-accept risk; if the measured change/dead
  rate is ~0 in the measured windows, endpoint-level liveness dominates
  full-path revalidation.

## 5. Population, frame, and substrate

Bound frame (all files also listed in `freeze_artifacts`):

- `research/experiments/EXP-FRONTIER-38184956362/raw/items.jsonl`
  (sha256 `c8215d69fbc4f230bd7087773c44aeecd68021a8b3349666adc5c19b0ed26ec5`)
  — the 208 admitted `live=true` deep items with `host`, `hop`, `ordinal`.
- `research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl`
  (sha256 `2afe65b63f751ef0d25578b02c9a667d43f866a0ac54504ebe1e1f4db839d747`)
  — frozen per-host BFS rows (250/250/176/250 discovered URLs; hop/ordinal/bytes).
- Reference BFS implementation:
  `research/experiments/EXP-FRONTIER-38184956362/execute_module.py` (sha256
  `b9b2efdc78266717946022002eb3bef301979ac6fc0967254202747037c5956f`) and its
  base `research/experiments/EXP-FRONTIER-38164611798/execute_module.py` (sha256
  `75a01d490ec81609cbf87a606f8cfa9227d07f07765b2eb4fd876fef2c8ff53a`).

Reconstruction policy (mirrors the bound parent `bfs_structural`): same-host
static `<a>` links, item-blind FIFO in document order, per-seed budget 250, depth
6, each URL fetched at most once; the same-host anchor is the netloc of the seed's
**final** URL after redirects (this is why the 28 `docs.readthedocs.io` items,
whose URLs canonicalize to `docs.readthedocs.com` after the seed redirect, are
reconstructible). Seeds are the minimal-hop URL per host: `doc.rust-lang.org` ->
`https://doc.rust-lang.org/stable/book/`, `pandas.pydata.org` ->
`https://pandas.pydata.org/docs/`, `docs.readthedocs.io` ->
`https://docs.readthedocs.io/en/stable/`, `docs.pytest.org` ->
`https://docs.pytest.org/en/stable/`.

## 6. Arms (stable ids)

- **Treatment `T-PERSIST-PATH-STORE`**: persist the snapshot of each admitted
  item's recovered path; at each window replay the path (fresh GETs) for liveness
  and SHA-256 content-change detection (a persisted store's revalidation).
  Cycle cost = number of distinct path pages requested once per cycle (store-level
  dedup) plus one GET per repeated page.
- **`B-COLD-BFS-PER-ITEM`** (mandate comparator): per admitted item, the frozen
  1-based BFS discovery/fetch ordinal (its cost to re-derive from cold without a
  store). Mean 166.0, min 31, max 250.
- **`B-COLD-BATCH-CRAWL`** (strongest fair, memoryful): one cold same-host BFS
  re-crawl per host per cycle, which re-yields all deep items; cost = row URL
  counts 250/250/176/250 = 926 GETs. This is the baseline the Director's
  "memoryful comparator" warning requires.
- **`B-NAIVE-EXACT-PATH-REPLAY`** (competitor-strength control, legacy guard):
  served persisted path with **no** revalidation; cost 0 per use; measured
  false-accept = item endpoint changed or dead at window w.
- **`A-ENDPOINT-ONLY-REVALIDATE`** (ablation, not the mandated treatment object):
  revalidate only the item endpoint (1 GET/item/cycle), isolating whether
  full-path replay is necessary.

Cost accounting is fully loaded: every HTTP request (including redirects and
conditional GETs) counts as one GET; bytes are the received body bytes; elapsed
is wall-clock.

## 7. Frozen metric ids

`M-COLD-ITEM-ORDINAL`, `M-COLD-ITEM-BFS-REMEASURED` (in-run reconstructed BFS
ordinal, fidelity cross-check only), `M-COLD-BATCH-GETS` (=926),
`M-COLD-BATCH-BYTES`, `M-REVAL-PATH-GETS` (per item per window),
`M-REVAL-UNIQUE-GETS` (distinct path pages per window, store-level),
`M-REVAL-PATH-BYTES`, `M-REVAL-PATH-ELAPSED`, `M-CHANGE-RATE`, `M-DEAD-RATE`,
`M-FALSE-ACCEPT-NAIVE`, `M-ENDPOINT-GETS`, `M-BREAK-EVEN-HOP`,
`M-BREAK-EVEN-DENSITY` (`reval_unique_gets / n_items`),
`M-BREAK-EVEN-CYCLES` (`cold_batch_gets / reval_unique_gets`).

## 8. Frozen control ids

Offline, in-process HTTP-fixture controls run by the frozen module's `controls`
stage (no external network), reusing the same `bfs_with_parents`, `path_to`,
`snapshot_path`, `revalidate_path`, and `decide` used to score the experiment:

- `C-BFS-PARENT-CHAIN` — parent-tracking BFS recovers `[seed, /a.html, /b.html,
  /item.html]`.
- `C-PATH-CANARY` — persist snapshot of a recovered path (all status 200).
- `C-REVAL-NOCHANGE` — unchanged fixture: 0 changed, 0 dead (null direction).
- `C-REVAL-CHANGE-DETECT` — mutated endpoint is detected by SHA-256.
- `C-LIVENESS-404` — removed endpoint is detected as dead (HTTP 404).
- `C-DECISION-CANARY-SUPPORTS` — `reval_unique_gets=700` (<= 833.4) -> `SUPPORTS`.
- `C-DECISION-CANARY-MIXED` — `reval_unique_gets=931` with mean path 4.0 GETs
  (`<= 4.007`, i.e. at least 10% below the amortized 4.452) -> `MIXED`.
- `C-DECISION-CANARY-MIXED-WINDOW` — batch pays at one window only -> `MIXED`.
- `C-DECISION-CANARY-FALSIFIES` — `reval_unique_gets=931` with mean path 5.0 GETs
  (> amortized cold) -> `FALSIFIES`.

EXECUTE-time network/code gates: `C-CODE-IDENTITY` (V1), `C-CONTROLS-GATE`
(V2, all nine controls PASS before economics), `C-FRAME-FIDELITY` (V3,
`n_misses==0`), `C-BUDGET` (V4, `total_gets <= 20000`), `C-SEED-LIVENESS` (V5).

## 9. Frozen EXECUTE module

The exact module below is the frozen EXECUTE driver (`execute_module.py`). It is
stdlib-only and credential-free. At EXECUTE it is reconstructed byte-for-byte
from this block; the extraction rule is: let `block` be the bytes strictly after
the opening marker line and strictly before the closing marker line, and
`C = block.strip()`; then `sha256(C)` must equal
`DERIVED_SHA256 = 0e42fa34c19d4c40b613610789cc8e3486308f6454e6d625c71c451fb06317ce`.
`prereg.md` is itself hashed in `freeze.json.hashes`, so the module identity is
frozen even though it is not a separate repository file.

Interface: `--stage controls|economics|all --out <dir> [--sleep S] [--window W]`.
Outputs under `--out`: `raw/controls.jsonl`, `raw/paths.jsonl`,
`raw/economics.jsonl`, `derived/metrics.json`, `derived/decision.json`.

FROZEN_CODE_BEGIN
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
FROZEN_CODE_END

## 10. Decision rule and gates

Evaluated in order.

- **G1 measurement validity.** If any of V1-V6 FAIL -> `status=MEASUREMENT_INVALID`,
  `outcome=NOT_APPLICABLE`; this is never a scientific negative.
- **G2 seed liveness.** If the seed fetch fails on every host -> `outcome=INCONCLUSIVE`
  with the explicit "not a scientific null" reason. A single dead host is
  excluded with reason; remaining hosts still decide.
- **G3 path-object existence.** If zero admitted items yield a recovered path
  (`n_paths==0`) -> `outcome=INCONCLUSIVE` (the treatment object could not be
  constructed); never a negative. The frozen `decide()` independently returns
  `NO_DATA` for an empty row set, so re-applying it to no rows cannot yield
  `FALSIFIES`.
- **G4 decision.** Otherwise apply the frozen `decide(rows, cold_batch_gets)` with
  `cold_batch_gets=926` and `n_items=208`, so the fully-loaded amortized per-item
  cold cost is `926/n_items = 4.452` GETs. For each window `w`:
  - `S_w` = mandate per-item *search* comparison pays (`mean(cold_item_gets) -
    mean(reval_path_gets) >= max(0.10*mean(cold), 5.0)`). On this frame it is
    always true; it is reported but is NOT a decision branch because it has no
    dynamic range.
  - `A_w` = fully-loaded per-item comparison pays (`4.452 - mean(reval_path_gets)
    >= 0.10*4.452 = 0.445`, i.e. `mean(reval_path_gets) <= 4.007`). This is the
    near-threshold per-item decision comparator.
  - `B_w` = batch/store comparison pays (`926 - reval_unique_gets >= 92.6`, i.e.
    `reval_unique_gets <= 833.4`).
  - `SUPPORTS` => `B_w` true at **every** measured window: full-path persistence
    beats the strongest fair memoryful baseline.
  - `FALSIFIES` => `B_w` false **and** `A_w` false at every measured window: the
    persistence claim fails even against the fully-loaded per-item cost.
  - `MIXED` => otherwise: `B` false while `A` true (pays per-item but not against
    a batch re-crawl), or `B` flips across the window ladder (time-bounded).
  Report `M-BREAK-EVEN-CYCLES = 926 / reval_unique_gets`, `M-BREAK-EVEN-DENSITY`,
  and `M-BREAK-EVEN-HOP` (smallest observed hop whose mean path GETs reach its
  mean cold ordinal; null if none). Search, amortized, and batch results are always
  reported separately; `A-ENDPOINT-ONLY-REVALIDATE` is reported as an ablation.

Outcome `MIXED` is decision-relevant, not a non-result: it bounds the mechanism
to sparse reuse / endpoint-level liveness.

## 11. Measurement validity gates

- **V1 code identity.** Reconstructed module hash == `DERIVED_SHA256`. Mismatch ->
  `MEASUREMENT_INVALID` before any outcome stage.
- **V2 controls gate.** All nine `controls` rows PASS before `economics` runs.
- **V3 frame fidelity.** `items.jsonl` yields exactly 208 `live=true` items on the
  four hosts, and every admitted item yields a recovered path (`n_misses==0`).
  Any miss -> `MEASUREMENT_INVALID` listing the missing items (representation
  loss, not a negative).
- **V4 budget.** `total_gets <= 20000`; overflow -> `MEASUREMENT_INVALID`.
- **V5 seed liveness.** Each host seed returns HTTP 200; a host that does not is
  excluded with reason.
- **V6 denominator guard.** `cold_batch_gets>0` and `n_items>0`; no 0/0 enters
  thresholding.
- **V7 session-scale bound.** All change/dead/false-accept statements are bounded
  to the measured windows (<=1800 s nominal); no day-scale extrapolation.
- **V8 decision determinism.** `decide` is applied to the recorded per-window
  rows; recomputation is stable and reproducible from `raw/economics.jsonl`.
- **V9 elapsed reporting.** Actual inter-window elapsed is recorded; windows are
  keyed by index, not by wall-clock attainment.

## 12. Satisfiability self-disproof (adversarial)

1. **Decision-rule reachability.** All three outcome branches fire: canaries
   `C-DECISION-CANARY-SUPPORTS` (`reval_unique_gets=700 <= 833.4`),
   `-MIXED` (`931 > 833.4` with mean path `4.0 <= 4.007`),
   `-MIXED-WINDOW` (batch flips across windows), and `-FALSIFIES`
   (`931 > 833.4` with mean path `5.0 > 4.007`) were executed at DESIGN and all
   PASS (section 13). No branch is empty and no branch is engineered. The two
   near-threshold quantities make the three branches genuinely reachable on this
   frame: the batch result hinges on measured store-level sharing (`reval_unique_gets`
   vs `833.4`, with `sum_i(hop_i+1)=931 > 926`), and the per-item result hinges on
   measured path length (`mean(reval_path_gets)` vs `4.007`, with the fully-loaded
   cost `926/208=4.452` vs expected `931/208=4.476`). `FALSIFIES` is a real state
   of the world (both thresholds missed) and `SUPPORTS` is a real state of the
   world (store sharing below `833.4`). No pre-freeze outcome fraction was
   measured; no a-priori probability is claimed.
2. **Measurement prerequisites.** Every prerequisite exists at DESIGN: the frame
   files are present with matching hashes; seeds are the frame's own min-hop URLs;
   the module is stdlib-only and was executed offline at DESIGN; the four hosts
   carried all 208 items live in the parent. Nothing possibility-determining is
   deferred to EXECUTE.
3. **Baseline identifiability.** Comparators are distinct and fully specified:
   per-item ordinal (measured, in-frame), memoryful batch re-crawl (926 GETs,
   computed from the bound frame), naive replay (0 GETs/use), endpoint-only
   ablation (208 GETs/cycle). The batch comparison is near-threshold (threshold
   833.4 vs expected ~931), so it is discriminating and not at a ceiling; the
   per-item comparison is abundant by construction and is reported as such. Both
   directions of the decision are reachable (section 12.1).
4. **Control sensitivity.** Every control fires in both directions under the same
   code that scores the experiment: change detection fires on mutation and not on
   no-change; liveness fires on 404; the decision canaries produce SUPPORTS, MIXED
   (two ways) and FALSIFIES. Observed DESIGN values are in section 13.
5. **Treatment liveness.** The treatment (path recovery + persist + revalidate +
   decide) was EXECUTED at pre-freeze cost, offline, to mechanical completion; see
   the transcript in section 13. The bound parent module's `bfs_structural` is the
   reconstruction policy mirror. EXECUTE re-runs the controls stage as a hard gate
   before any outcome stage.
6. **Freeze artifacts bound.** Every mutable local file whose identity can change
   the interpretation is listed in `freeze_artifacts` and hashed into
   `freeze.json.artifact_hashes`; the executed module identity is pinned by
   `DERIVED_SHA256` against the frozen prereg (section 9).

## 13. DESIGN pre-freeze probes (observed values)

Cheap, non-outcome-bearing; no network measurement of the outcome was performed.

- **Offline controls probe.** `python3 execute_module.py --stage controls --out
  <tmp>` (in-process HTTP fixture only) -> `{"all_pass": true, "n": 9, "failed": []}`.
  Observed: parent chain `[seed, /a.html, /b.html, /item.html]`;
  `C-REVAL-NOCHANGE` `{changed: [], dead: []}`; `C-REVAL-CHANGE-DETECT`
  `{changed: [".../item.html"]}`; `C-LIVENESS-404` `{dead: [".../item.html"]}`;
  decision canaries `SUPPORTS`, `MIXED`, `MIXED`, `FALSIFIES`.
- **Frame arithmetic probe (offline).** 208 admitted items on four hosts;
  `sum(hop+1)=931`; cold batch `= 250+250+176+250 = 926`; batch threshold
  `= 833.4`; fully-loaded amortized per-item cold `= 926/208 = 4.452`; amortized
  threshold `= 4.007`; per-item *search* ordinal mean `166.01`; all admitted URLs
  resolve to a min-hop seed with a same-host (post-redirect) anchor.
- **Frame integrity.** Bound file hashes match the values in section 17.

## 14. Budget, schedule, and stop/pivot triggers

- Ceiling `TOTAL_GET_CEILING = 20000` HTTP GETs. Expected: reconstruction
  `<= 926`; snapshot `<= 931`; four revalidation cycles `<= 4 x 931`; well within
  ceiling. Zero model calls, zero browser, zero credentials.
- Nominal window ladder `0/300/900/1800` s; measured wall-clock is recorded.
- **Stop/pivot trigger** (from the mandate): if revalidation cost is
  indistinguishable from cold re-derivation across the whole ladder, or if no
  liveness signal is measurable without a day-scale span, record the exact
  blocker and PARK the persistence subthread rather than enlarging the ladder.
- **Measurement-invalid signature**: V1-V6 failure -> `MEASUREMENT_INVALID`, never
  a negative; G2/G3 -> `INCONCLUSIVE`.

## 15. Validity threats and representation loss

- Single runner vantage; results are not external-valid across ASN/geography
  (inherited limitation).
- Session-scale only: change/dead rates are lower bounds on longer-horizon decay;
  never extrapolate to day scale.
- The frame's `ordinal` is a BFS discovery cost, not a clean-chain cost; it is the
  mandate's chosen comparator and is used as such.
- Store-level dedup assumes a persisted store shares path prefixes; if the
  measured store does not dedup, `B` is even less likely to pay, which is
  reported, not hidden.
- Frame fidelity depends on live hosts not having restructured since the frozen
  crawl; V3 turns any such drift into `MEASUREMENT_INVALID` rather than a silent
  population change.
- Empirical tilt: with the frozen frame's arithmetic (`unique ~= 931 > 833.4` and
  `mean path ~= 4.476 > 4.007`), the a-priori expected branch is `FALSIFIES`
  (both thresholds missed). `SUPPORTS` requires measured store-level sharing to
  push `reval_unique_gets <= 833.4`. `MIXED` requires measured per-item paths
  shorter than `4.007` while the batch still misses, or a batch flip across the
  ladder. All three are certified reachable by canary (section 12.1) and none was
  engineered; no pre-freeze outcome fraction was measured.

## 16. Consequences

- `SUPPORTS` -> build a persisted full-path store with a revalidation policy;
  feeds `C-CROSSSITE` maintenance economics and the product `C-PRODUCT-ECON`
  decision as a positive cost result.
- `MIXED` -> do not build a general full-path store; build endpoint-level
  liveness and/or reuse-bounded maintenance; the mechanism is bounded to sparse
  reuse.
- `FALSIFIES` -> cold re-derivation (or a different representation) is at least as
  cheap as full-path persist+revalidate, including the fully-loaded per-item cost;
  do not build the store and PARK the persistence subthread (no discovery rerun).
  No claim promotion either way in this packet.

## 17. Freeze artifacts

Interpretation dependencies (exact repository-relative file paths, hashed into
`freeze.json.artifact_hashes`):

1. `research/experiments/EXP-FRONTIER-38184956362/raw/items.jsonl`
2. `research/experiments/EXP-FRONTIER-38184956362/raw/structural.jsonl`
3. `research/experiments/EXP-FRONTIER-38184956362/raw/census.jsonl`
4. `research/experiments/EXP-FRONTIER-38184956362/derived/metrics.json`
5. `research/experiments/EXP-FRONTIER-38184956362/execute_module.py`
6. `research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl`
7. `research/experiments/EXP-FRONTIER-38164611798/execute_module.py`
8. `research/experiments/EXP-FRONTIER-38184956362/audit.json`
9. `research/experiments/EXP-FRONTIER-38184956362/result.json`

The executed module is additionally pinned by `DERIVED_SHA256` against this
preregistration.

## 18. Mandate fidelity and unresolved

- Fidelity: the mandate's comparator (per-item same-host BFS ordinal, mean 166.0)
  is retained as `B-COLD-BFS-PER-ITEM`; the mandate's memoryful-comparator warning
  is satisfied by `B-COLD-BATCH-CRAWL`; the mandate's competitor-strength control
  is satisfied by `B-NAIVE-EXACT-PATH-REPLAY`; the mandate's session-scale bound
  is enforced by V7. The mandate's question is answered by G4.
- Unresolved (for EXECUTE/AUDIT): the measured session-scale change/dead rate,
  store-level path sharing, and the resulting break-even are unknown at DESIGN by
  construction. No pre-freeze outcome was observed.
