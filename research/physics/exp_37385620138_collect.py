#!/usr/bin/env python3
"""
EXP-PHYSICS-37385620138 — COLLECTION (EXECUTE stage).

Phases, in order:

  0  frozen-input verification                      -> raw/frozen_input_verification.json
  1  candidate universe, seeded                     -> raw/candidate_universe.json
  2  robots.txt politeness filter (prereg s5.1)     -> raw/robots_screen.jsonl
  3  variation-coverage screen (prereg s5.2/s6.2)   -> raw/collection_log.jsonl
                                                       raw/screen_results.jsonl
  4  executor-added descriptive substrate diagnostics
     (NOT part of the frozen design, NOT used by the frozen decision rule)
       4a repeat-identical-request null             -> raw/diagnostics.jsonl
       4b conditional-GET revalidation probe         -> raw/diagnostics.jsonl
  5  positive control PC_KNOWN_PARAMETER_EFFECT on a local stdlib server
     (prereg s9.1)                                  -> raw/pc_collection_log.jsonl
                                                       raw/pc_truth.json

Substrate: stdlib urllib only. No browser, no Docker, no model key, no
credentials, no cookies, no session state. Every response is archived with its
status, headers, full body length, full body sha256 and DOM structural hash.
"""

from __future__ import annotations

import hashlib
import json
import random
import sys
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exp_37385620138_candidates as CAND  # noqa: E402
import exp_37385620138_lib as L  # noqa: E402
from exp_37385620138_lib import (  # noqa: E402
    DERIVED_DIR,
    EXP_DIR,
    MECHANISMS,
    RAW_DIR,
    eTLD1,
    http_get,
    intervention_url,
    load_request,
    sha256_file,
    write_json,
    write_jsonl,
)

WORKERS = 8
HOST_GAP = 0.30
TIMEOUT = 20.0


# ---------------------------------------------------------------------------
# per-host politeness
# ---------------------------------------------------------------------------

class Throttle:
    def __init__(self, gap: float) -> None:
        self.gap = gap
        self._last: dict[str, float] = {}
        self._locks: dict[str, threading.Lock] = {}
        self._guard = threading.Lock()

    def do(self, host: str, fn):
        with self._guard:
            lock = self._locks.setdefault(host, threading.Lock())
        with lock:
            prev = self._last.get(host)
            if prev is not None:
                delta = time.time() - prev
                if delta < self.gap:
                    time.sleep(self.gap - delta)
            self._last[host] = time.time()
            return fn()


THROTTLE = Throttle(HOST_GAP)


def fetch(url: str, extra_headers: dict | None = None, timeout: float = TIMEOUT) -> dict:
    host = urlsplit(url).netloc
    return THROTTLE.do(host, lambda: http_get(url, timeout=timeout, extra_headers=extra_headers))


# ---------------------------------------------------------------------------
# phase 0 — frozen inputs
# ---------------------------------------------------------------------------


def phase0() -> dict:
    from exp_37385620138_lib import verify_freeze

    rec = verify_freeze()
    rec["master_seed"] = L.MASTER_SEED
    rec["master_seed_rule"] = "int(request_hash[:8], 16)  # prereg s5.1"
    rec["substrate"] = {
        "protocol": "HTTPS GET via python stdlib urllib",
        "browser": False,
        "docker": False,
        "model_calls": 0,
        "model_api_keys": 0,
        "credentials": 0,
        "cookies_or_sessions": 0,
        "third_party_packages": [],
        "note": "numpy, scipy, flask, requests and bs4 are absent from this environment; "
                "every computation in this packet is pure standard library.",
    }
    write_json(RAW_DIR / "frozen_input_verification.json", rec)
    print(f"[phase0] hashes_match={rec['all_hashes_match']} master_seed={L.MASTER_SEED}")
    return rec


# ---------------------------------------------------------------------------
# phase 1 — candidate universe
# ---------------------------------------------------------------------------


def phase1() -> list[dict]:
    pairs = CAND.candidate_pairs()
    universe = []
    for i, p in enumerate(pairs):
        netloc = urlsplit(p["document_url"]).netloc
        universe.append({
            "candidate_id": f"C{i:04d}",
            "host": netloc,
            "site": eTLD1(netloc),
            "document_url": p["document_url"],
        })
    # prereg s5.1: deterministic order derived from the request digest
    rng = random.Random(L.MASTER_SEED)
    rng.shuffle(universe)
    for i, u in enumerate(universe):
        u["screen_order"] = i
        u["candidate_id"] = f"C{i:04d}"
    meta = {
        "seed": L.MASTER_SEED,
        "seed_rule": "int(request_hash[:8], 16) with request_hash from request.json",
        "source_arm_used": "manual curation list (prereg s5.1 third arm)",
        "source_arms_not_reproducible": [
            "Tranco top 1M (external bulk index, absent from repository)",
            "Common Crawl index (external bulk index, absent from repository)",
        ],
        "frozen_target_pairs": 200,
        "frozen_target_etld1": 50,
        "actual_pairs": len(universe),
        "actual_hosts": len({u["host"] for u in universe}),
        "actual_etld1": len({u["site"] for u in universe}),
        "hashed_by_freeze": False,
        "note": "This file is EXECUTOR-CONSTRUCTED. prereg s17 declares it frozen at freeze "
                "time, but freeze.json hashes only request.json, spec.json and prereg.md, so this "
                "file was not and could not be hashed. It is NOT claimed as frozen evidence.",
        "candidates": universe,
    }
    write_json(RAW_DIR / "candidate_universe.json", meta)
    print(f"[phase1] pairs={len(universe)} etld1={len({u['site'] for u in universe})}")
    return universe


# ---------------------------------------------------------------------------
# phase 2 — robots.txt politeness filter
# ---------------------------------------------------------------------------


def phase2(universe: list[dict]) -> list[dict]:
    hosts = sorted({u["host"] for u in universe})
    out: list[dict] = []

    def fetch_robots(host: str) -> dict:
        req = urllib.request.Request(f"https://{host}/robots.txt",
                                     headers={"User-Agent": "SPIDER-Research/2.0"})
        row: dict = {"host": host, "robots_url": f"https://{host}/robots.txt",
                     "status": None, "body_text": None, "transport_error": None}
        try:
            with urllib.request.urlopen(req, timeout=12.0) as r:
                raw = r.read(200_000)
                row["status"] = int(r.status)
                row["body_text"] = raw.decode("utf-8", "replace")
        except Exception as exc:
            code = getattr(exc, "code", None)
            row["status"] = int(code) if code is not None else None
            row["transport_error"] = f"{type(exc).__name__}: {exc}"[:160]
        return row

    def decide(row: dict) -> dict:
        host = row["host"]
        allowed = True
        detail = "no robots.txt served; treated as unrestricted"
        if row["body_text"]:
            rp = RobotFileParser()
            try:
                rp.parse(row["body_text"].splitlines())
                verdicts = {}
                for u in {c["document_url"] for c in universe if c["host"] == host}:
                    verdicts[u] = rp.can_fetch("SPIDER", u) or rp.can_fetch("*", u)
                disallowed = [u for u, ok in verdicts.items() if not ok]
                allowed = not disallowed
                detail = ("robots.txt served; all curated documents allowed"
                          if allowed else
                          f"robots.txt disallows {len(disallowed)} curated document(s): "
                          f"{sorted(disallowed)[:3]}")
            except Exception as exc:
                detail = f"robots parse error {type(exc).__name__}: unrestricted"
        row.pop("body_text", None)
        row["allowed"] = allowed
        row["detail"] = detail
        return row

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        rows = list(pool.map(fetch_robots, hosts))
    for row in rows:
        out.append(decide(row))
    write_jsonl(RAW_DIR / "robots_screen.jsonl", out)
    n_blocked = sum(1 for r in out if not r["allowed"])
    print(f"[phase2] hosts={len(out)} blocked={n_blocked}")
    return out


# ---------------------------------------------------------------------------
# phase 3 — variation-coverage screen + self-verifying matched-pair interventions
# ---------------------------------------------------------------------------


def phase3(universe: list[dict], robots: list[dict]) -> list[dict]:
    allowed_hosts = {r["host"] for r in robots if r["allowed"]}
    work = [u for u in universe if u["host"] in allowed_hosts]

    jobs: list[dict] = []
    for c in work:
        jobs.append({
            "candidate_id": c["candidate_id"], "site": c["site"], "host": c["host"],
            "document_url": c["document_url"], "role": "baseline",
            "url": c["document_url"], "mechanism_id": None, "intervention_type": None,
            "parameter": None, "value": None, "value_rank": None,
        })
        for mech in MECHANISMS:
            for rank, val in enumerate(mech["values"], start=1):
                jobs.append({
                    "candidate_id": c["candidate_id"], "site": c["site"], "host": c["host"],
                    "document_url": c["document_url"], "role": "probe",
                    "url": intervention_url(c["document_url"], mech, val),
                    "mechanism_id": mech["mechanism_id"],
                    "intervention_type": mech["intervention_type"],
                    "parameter": mech["parameter"], "value": val, "value_rank": rank,
                })

    print(f"[phase3] candidates={len(work)} jobs={len(jobs)}")

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(lambda j: fetch(j["url"]), jobs))

    rows = []
    for j, r in zip(jobs, results):
        row = dict(j)
        row.update({
            "final_url": r["final_url"],
            "status": r["status"],
            "resp_headers": r["resp_headers"],
            "content_type": r["content_type"],
            "body_len": r["body_len"],
            "body_sha256": r["body_sha256"],
            "structural_hash": r["structural_hash"],
            "structural_nodes": r["structural_nodes"],
            "elapsed_ms": r["elapsed_ms"],
            "transport_error": r["transport_error"],
            "t_requested": r["t_requested"],
        })
        rows.append(row)
    write_jsonl(RAW_DIR / "collection_log.jsonl", rows)

    # ---- frozen admission screen (prereg s5.2) -----------------------------
    by_cand: dict[str, list[dict]] = {}
    for r in rows:
        by_cand.setdefault(r["candidate_id"], []).append(r)

    screen = []
    for c in work:
        rs = by_cand[c["candidate_id"]]
        base = next(r for r in rs if r["role"] == "baseline")
        probes = [r for r in rs if r["role"] == "probe"]
        transport_ok = sum(1 for r in probes if r["status"] is not None and 200 <= r["status"] < 400)
        sigs = {f"{r['status']}|{r['body_sha256']}|{r['structural_hash']}" for r in probes}
        per_type_variation = {}
        for mech in MECHANISMS:
            vals = [r for r in probes if r["mechanism_id"] == mech["mechanism_id"]]
            sigset = {f"{r['status']}|{r['body_sha256']}|{r['structural_hash']}" for r in vals}
            per_type_variation[mech["mechanism_id"]] = len(sigset)
        path_statuses = sorted({r["status"] for r in probes
                                if r["intervention_type"] == "path_param"}, key=lambda x: (x is None, x))
        screen.append({
            "candidate_id": c["candidate_id"],
            "site": c["site"],
            "host": c["host"],
            "document_url": c["document_url"],
            "baseline_status": base["status"],
            "baseline_content_type": base["content_type"],
            "baseline_body_len": base["body_len"],
            "n_probes": len(probes),
            "transport_ok": transport_ok,
            "c1_transport_ok": transport_ok >= 12,
            "n_distinct_signatures": len(sigs),
            "c2_identifier_variation": len(sigs) >= 2,
            "signature_variation_per_mechanism": per_type_variation,
            "c3_template_variation": any(v > 1 for v in per_type_variation.values()),
            "path_param_statuses": path_statuses,
            "n_path_param_2xx_3xx": sum(1 for r in probes
                                         if r["intervention_type"] == "path_param"
                                         and r["status"] is not None and 200 <= r["status"] < 400),
            "n_query_param_2xx_3xx": sum(1 for r in probes
                                         if r["intervention_type"] == "query_param"
                                         and r["status"] is not None and 200 <= r["status"] < 400),
            "n_anchor_2xx_3xx": sum(1 for r in probes
                                    if r["intervention_type"] == "anchor_fragment"
                                    and r["status"] is not None and 200 <= r["status"] < 400),
            "admitted": None,
            "fail_reasons": [],
        })
    for s in screen:
        reasons = []
        if not s["c1_transport_ok"]:
            reasons.append("C1_transport_ok")
        if not s["c2_identifier_variation"]:
            reasons.append("C2_identifier_variation")
        if not s["c3_template_variation"]:
            reasons.append("C3_template_variation")
        s["fail_reasons"] = reasons
        s["admitted"] = not reasons
    write_jsonl(RAW_DIR / "screen_results.jsonl", screen)
    n_adm = sum(1 for s in screen if s["admitted"])
    print(f"[phase3] screened={len(screen)} admitted={n_adm} "
          f"sites_admitted={len({s['site'] for s in screen if s['admitted']})}")
    return screen


# ---------------------------------------------------------------------------
# phase 4 — executor-added descriptive substrate diagnostics (NOT frozen design)
# ---------------------------------------------------------------------------


def phase4(screen: list[dict]) -> list[dict]:
    from exp_37385620138_lib import read_jsonl

    healthy = [s for s in screen if s["baseline_status"] is not None and s["baseline_status"] < 400]
    work = healthy[:80]

    validators: dict[str, dict] = {}
    for r in read_jsonl(RAW_DIR / "collection_log.jsonl"):
        if r["role"] != "baseline":
            continue
        h = r.get("resp_headers") or {}
        validators[r["candidate_id"]] = {
            "etag": h.get("etag"),
            "last_modified": h.get("last-modified"),
        }

    jobs = []
    for s in work:
        jobs.append({"kind": "repeat_identical", "candidate_id": s["candidate_id"],
                     "site": s["site"], "url": s["document_url"], "index": 1})
        jobs.append({"kind": "repeat_identical", "candidate_id": s["candidate_id"],
                     "site": s["site"], "url": s["document_url"], "index": 2})
        jobs.append({"kind": "conditional_get", "candidate_id": s["candidate_id"],
                     "site": s["site"], "url": s["document_url"], "index": 0})
    print(f"[phase4] diagnostic candidates={len(work)} jobs={len(jobs)}")

    from concurrent.futures import ThreadPoolExecutor

    def run(j: dict) -> tuple[dict, dict]:
        if j["kind"] == "conditional_get":
            # A validating header is required for a 304 to be possible at all.
            v = validators.get(j["candidate_id"]) or {}
            hdrs = {}
            if v.get("etag"):
                hdrs["If-None-Match"] = v["etag"]
            elif v.get("last_modified"):
                hdrs["If-Modified-Since"] = v["last_modified"]
            return j, fetch(j["url"], extra_headers=hdrs or None, timeout=TIMEOUT)
        return j, fetch(j["url"])

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        out = list(pool.map(run, jobs))
    rows = []
    for j, r in out:
        rows.append({
            "kind": j["kind"], "candidate_id": j["candidate_id"], "site": j["site"],
            "url": j["url"], "index": j["index"], "status": r["status"],
            "body_sha256": r["body_sha256"], "structural_hash": r["structural_hash"],
            "resp_headers": r["resp_headers"], "body_len": r["body_len"],
            "transport_error": r["transport_error"], "t_requested": r["t_requested"],
        })
    write_jsonl(RAW_DIR / "diagnostics.jsonl", rows)
    n304 = sum(1 for r in rows if r["kind"] == "conditional_get" and r["status"] == 304)
    ncond = sum(1 for r in rows if r["kind"] == "conditional_get")
    print(f"[phase4] conditional_get_probes={ncond} returning_304={n304}")
    return rows


# ---------------------------------------------------------------------------
# phase 5 — positive control on a local stdlib server (prereg s9.1)
# ---------------------------------------------------------------------------

PC_SITES = [f"pc{i:02d}" for i in range(1, 21)]
PC_BIND = {
    # mechanism_id -> (baseline path, parameter, values) on the local server
    "M_PAGINATION": ("echo", "page", ["1", "2", "3", "10", "100"]),
    "M_SECTION": ("page/1", "section", ["intro", "methods", "results", "discussion", "appendix"]),
    "M_ANCHOR": ("page/1", "id", ["overview", "details", "examples", "references", "see-also"]),
}
SECTIONS = {"intro": "Introduction", "methods": "Methods", "results": "Results",
            "discussion": "Discussion", "appendix": "Appendix"}
PAGES = ["1", "2", "3", "10", "100"]


class PCHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "SPIDER-PC/1.0"

    def log_message(self, *a):  # silence
        return

    def _body(self, payload: bytes, etag: str, ctype: str = "text/html; charset=utf-8") -> None:
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("ETag", etag)
        self.send_header("Cache-Control", "max-age=0, must-revalidate")
        self.send_header("Last-Modified", "Wed, 01 Jan 2025 00:00:00 GMT")
        self.send_header("Vary", "Accept-Encoding")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):  # noqa: N802
        path, _, query = self.path.partition("?")
        q = dict(p.split("=", 1) if "=" in p else (p, "") for p in query.split("&") if p)
        parts = [p for p in path.split("/") if p]
        # /pc/<site>/echo[?param=v|page=v]
        if len(parts) == 3 and parts[0] == "pc" and parts[2] == "echo":
            val = q.get("param", q.get("page"))
            payload = json.dumps({"param": val}).encode()
            etag = '"echo-' + (val or "null") + '"'
            self._body(payload, etag, "application/json")
            return
        # /pc/<site>/page/<n>  and  /pc/<site>/page/<n>/<section>
        if len(parts) in (4, 5) and parts[0] == "pc" and parts[2] == "page":
            n = parts[4] if len(parts) == 5 else parts[3]
            title = SECTIONS.get(n, f"Page {n}")
            payload = (
                "<!doctype html><html><head><title>"
                f"{title}</title></head><body><main><h1>{title}</h1>"
                f'<div data-page="{n}">Content {title}</div></main></body></html>'
            ).encode()
            self._body(payload, '"page-' + n + '"')
            return
        self.send_response(404)
        self.send_header("Content-Length", "0")
        self.end_headers()


def phase5() -> list[dict]:
    srv = ThreadingHTTPServer(("127.0.0.1", 0), PCHandler)
    port = srv.server_address[1]
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    base = f"http://127.0.0.1:{port}"
    try:
        jobs = []
        for s in PC_SITES:
            for mech in MECHANISMS:
                doc_rel, param, values = PC_BIND[mech["mechanism_id"]]
                doc_url = f"{base}/pc/{s}/{doc_rel}"
                jobs.append({"kind": "baseline", "pc_site": s, "document_url": doc_url,
                             "mechanism_id": mech["mechanism_id"],
                             "intervention_type": mech["intervention_type"],
                             "url": doc_url, "parameter": param, "value": None, "value_rank": None})
                for rank, v in enumerate(values, start=1):
                    u = intervention_url(doc_url, mech, v)
                    jobs.append({"kind": "probe", "pc_site": s, "document_url": doc_url,
                                 "mechanism_id": mech["mechanism_id"],
                                 "intervention_type": mech["intervention_type"],
                                 "url": u, "parameter": param, "value": v, "value_rank": rank})
        rows = []
        for j in jobs:
            r = http_get(j["url"], timeout=10.0)
            row = dict(j)
            row.update({
                "final_url": r["final_url"], "status": r["status"],
                "resp_headers": r["resp_headers"], "body_len": r["body_len"],
                "body_sha256": r["body_sha256"], "structural_hash": r["structural_hash"],
                "transport_error": r["transport_error"], "t_requested": r["t_requested"],
            })
            rows.append(row)
    finally:
        srv.shutdown()
        srv.server_close()

    write_jsonl(RAW_DIR / "pc_collection_log.jsonl", rows)

    # ---- known ground truth (prereg s9.1) ----------------------------------
    truth = {
        "M_PAGINATION": {
            "endpoint": "/pc/<site>/echo?page=<v>",
            "declared_effect": "parameter echoed into the response body",
            "ground_truth_server_visible_change": True,
            "ground_truth_predicted_distance_direction": "non-zero, body differs for every v",
        },
        "M_SECTION": {
            "endpoint": "/pc/<site>/page/<v>",
            "declared_effect": "path segment selects a different document body",
            "ground_truth_server_visible_change": True,
            "ground_truth_predicted_distance_direction": "non-zero, body differs for every v",
        },
        "M_ANCHOR": {
            "endpoint": "/pc/<site>/page/1#<id>",
            "declared_effect": "fragment scrolls client-side",
            "ground_truth_server_visible_change": False,
            "ground_truth_predicted_distance_direction": "exactly zero, fragment is not in the request target",
        },
        "n_pc_sites": len(PC_SITES),
        "pc_site_split_rule": "prereg s11 step 3/4: 70% of admitted sites train, 30% test",
        "train_sites": PC_SITES[:14],
        "test_sites": PC_SITES[14:],
    }
    write_json(RAW_DIR / "pc_truth.json", truth)
    print(f"[phase5] pc_requests={len(rows)} pc_sites={len(PC_SITES)}")
    return rows


def main() -> None:
    load_request()
    phase0()
    universe = phase1()
    robots = phase2(universe)
    screen = phase3(universe, robots)
    phase4(screen)
    phase5()
    print("COLLECTION_COMPLETE")


if __name__ == "__main__":
    main()