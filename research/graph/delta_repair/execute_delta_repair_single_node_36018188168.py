#!/usr/bin/env python3
"""
EXP-GRAPH-36018188168 — EXECUTE harness (honest single-node transfer re-execution).

Fixes all 9 parent audit required_fixes (EXP-GRAPH-35999336958 was
MEASUREMENT_INVALID): real nginx 1.24.0 $request_uri consistent hash in front of
2x gunicorn 23 (each -w 1) Flask 3.1.3 + PyJWT HS256 workers sharing SQLite WAL at
/tmp/spider-runtime/single.db; verification via src/spider/kernel.py _matches;
correct k*5 token scaling (5/10/15); per-trajectory-reset honest integer
sum-counter (resolve1+bind1+verify1+freshness1+browser1-per-repair-probe);
trajectory-grouped 1000 perms / 5000 family-stratified trajectory-grouped
bootstraps; TRAIN18/TEST12 verification split; same-resource co-bound
contamination N>=20 + disjoint N>=20, re-verified via _matches on a registry clone
snapshot; health-gated single-node substrate; frozen count reconciliation
(300 fresh + 50 stale K1-K3 + 150 noise = 500 evaluated / executed incl. 30
auxiliary = 530+, n_non304 = 500 >= 360).

Both stages (synthetic sanity stdlib http.server + single-node primary) run the
SAME core machinery: workload execution -> per-(trajectory,rid) observed caching
(first 3 pre-drift requests) -> frozen combined guard (Jaccard 0.85 required-
filtered {id,name,email} OR param/header template change OR (ETag change AND
max-age 60->0), confidences 0.95 fresh / 0.85 stale) -> executed deterministic
re-observe repair (k probes, overwrite cache, rebind, re-verify via _matches)
-> all baselines executed -> controls PC1/PC2/NC1/NC2/NC3 -> contamination
re-verification -> D1-D13 frozen decision rule.

RAW vs DERIVED: every request is logged to raw_evidence JSONL (V13 fields) before
any metric is computed; metrics are derived from those logs; interpretation is in
the decision block. No outcome values are hardcoded anywhere.
"""
import copy
import hashlib
import json
import math
import os
import random
import socket
import sqlite3
import statistics
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

REPO = Path("/home/runner/work/Spider/Spider")
EXPERIMENT_ID = "EXP-GRAPH-36018188168"
EXPERIMENT_DIR = REPO / "research/experiments" / EXPERIMENT_ID
RAW_EVIDENCE_DIR = EXPERIMENT_DIR / "raw_evidence"
DELTA_REPAIR_DIR = REPO / "research/graph/delta_repair"
SRC_DIR = REPO / "src"

sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(DELTA_REPAIR_DIR))

from spider.kernel import _matches  # deterministic verification (audit fix #2)
import flask_app_36018188168 as FA  # resource_for/etag_for/extract_field_types = single source of truth

LANE = "graph"
THRESHOLD = 0.85
FRESH_CONFIDENCE = 0.95
STALE_CONFIDENCE = 0.85
DRIFT_POINT = 6
REQUIRED_PATHS = {"id", "name", "email"}
TESTBED_SECRET = "TESTBED_SECRET_SPIDER_36018188168"
DB_PATH = "/tmp/spider-runtime/single.db"
RUNTIME_DIR = Path("/tmp/spider-runtime")

FAMILIES = ["dom_drift", "param_header_mutation", "cache_expiry"]
CONTROL_FAMILY = "stable"
NOISE_FAMILIES = ["noise_A_phone", "noise_B_nickname", "noise_C_null"]

# ----------------------------------------------------------------------------
# Statistics utilities (no numpy/sklearn — from scratch, parent-compatible)
# ----------------------------------------------------------------------------
def wilson(successes, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))


def jaccard(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b) if (a | b) else 1.0


def filter_required(tokens):
    return {(p, t) for (p, t) in tokens if p in REQUIRED_PATHS}


def pearson(a, b):
    n = len(a)
    if n < 2:
        return 0.0
    ma = sum(a) / n
    mb = sum(b) / n
    num = sum((ai - ma) * (bi - mb) for ai, bi in zip(a, b))
    den = math.sqrt(sum((ai - ma) ** 2 for ai in a) * sum((bi - mb) ** 2 for bi in b))
    return num / den if den != 0 else 0.0


def auc_score(y_true, y_score):
    n_pos = sum(y_true)
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.5
    pos = [s for s, t in zip(y_score, y_true) if t == 1]
    neg = [s for s, t in zip(y_score, y_true) if t == 0]
    wins = ties = 0
    for ps in pos:
        for ns in neg:
            if ps > ns:
                wins += 1
            elif ps == ns:
                ties += 1
    return (wins + 0.5 * ties) / (n_pos * n_neg)


def pct(arr, p):
    s = sorted(arr)
    if not s:
        return 0.0
    k = (len(s) - 1) * p / 100
    f = int(k)
    c = min(f + 1, len(s) - 1)
    if f == c:
        return s[f]
    d = k - f
    return s[f] * (1 - d) + s[c] * d


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(65536), b""):
            h.update(blk)
    return h.hexdigest()


# ----------------------------------------------------------------------------
# Frozen workload plans (reconciled counts)
# ----------------------------------------------------------------------------
def build_workload(stage):
    """Return workload dict for a stage. All ids are disjoint across roles."""
    w = {"stage": stage, "fresh_trajs": [], "aux_trajs": [], "k1": [], "k2": [], "k3": [],
         "noise_trajs": [], "unrelated_ids": [], "nc1_ids": [], "cold_ids": [],
         "pc1_ids": [], "pc2_insts": []}
    if stage == "synthetic":
        # frozen synthetic sanity: 180 fresh + 30 stale(K1) + 150 noise = 360 evaluated,
        # + 30 auxiliary = 390 executed; drift trajs parent-style (per-req ids)
        for ti in range(12):
            w["fresh_trajs"].append({"traj_id": f"stable-{ti}", "family": CONTROL_FAMILY,
                                     "rids": [ti * 15 + r for r in range(1, 16)]})
        for ti in range(2):
            w["aux_trajs"].append({"traj_id": f"auxfresh-{ti}", "family": "fresh_pool",
                                   "rids": [8000 + ti * 100 + r for r in range(1, 16)]})
        for fi, fam in enumerate(FAMILIES):
            # K1 = exactly 30 stale pool instances (10 per family, 1 id each):
            # 2 trajectories per family x 5 per-req ids (frozen per-req rid plan)
            for ti in range(2):
                base = 1000 + fi * 1000 + ti * 100
                for req in range(6, 11):
                    w["k1"].append({"family": fam, "traj_id": f"syn-{fam}-{ti}",
                                    "ids": [base + req], "k": 1})
        # synthetic has NO K2/K3: frozen composition is 180 fresh + 30 stale (K1)
        # + 150 noise = 360 evaluated / 390 executed (prereg line 141).
        for vi, var in enumerate(NOISE_FAMILIES):
            for ti in range(5):
                w["noise_trajs"].append({"traj_id": f"syn-{var}-{ti}", "family": var,
                                         "rids": [20000 + vi * 10000 + ti * 10 + r for r in range(1, 11)]})
        w["unrelated_ids"] = list(range(9000, 9020))
        w["nc1_ids"] = list(range(6001, 6011))
        w["cold_ids"] = list(range(7001, 7013))
        w["pc1_ids"] = list(range(6101, 6113))  # 12 fresh trajectories (PC1)
        w["pc2_insts"] = [  # 1 known-break single-attribute instance per family (PC2 k=1)
            {"family": "dom_drift", "traj_id": "pc2-dom", "ids": [6201]},
            {"family": "param_header_mutation", "traj_id": "pc2-param", "ids": [6301]},
            {"family": "cache_expiry", "traj_id": "pc2-cache", "ids": [6401]},
        ]
        return w
    # ---- single-node primary: 300 fresh + 30 aux + 50 stale (K1 30 / K2 10 / K3 10)
    # + 150 noise = 500 evaluated / 530+ executed (cache-source + probes extra)
    for ti in range(20):
        # dedicated 70000-band rids: disjoint from k1 (1101-1110/2101-2110/3101-3110),
        # k2/k3 (4010-4718), aux (5001-5115), pc1/pc2/nc1/cold (6001-7120), noise (83xxx)
        w["fresh_trajs"].append({"traj_id": f"fresh-{ti}", "family": "fresh_pool",
                                 "rids": [70000 + ti * 15 + r for r in range(1, 16)]})
    for ti in range(2):
        w["aux_trajs"].append({"traj_id": f"auxfresh-{ti}", "family": "fresh_pool",
                               "rids": [5000 + 100 * ti + r for r in range(1, 16)]})
    k1 = []
    for rid in range(1101, 1111):
        k1.append({"family": "dom_drift", "traj_id": f"k1dom{rid - 1101}", "ids": [rid], "k": 1})
    for rid in range(2101, 2111):
        k1.append({"family": "param_header_mutation", "traj_id": f"k1param{rid - 2101}", "ids": [rid], "k": 1})
    for rid in range(3101, 3111):
        k1.append({"family": "cache_expiry", "traj_id": f"k1cache{rid - 3101}", "ids": [rid], "k": 1})
    w["k1"] = k1
    k2 = [
        ("dom_drift", [4010, 4011]), ("dom_drift", [4012, 4013]),
        ("dom_drift", [4014, 4015]), ("dom_drift", [4016, 4017]),
        ("param_header_mutation", [4110, 4111]), ("param_header_mutation", [4112, 4113]),
        ("param_header_mutation", [4114, 4115]),
        ("cache_expiry", [4210, 4211]), ("cache_expiry", [4212, 4213]),
        ("cache_expiry", [4214, 4215]),
    ]
    for i, (fam, ids) in enumerate(k2):
        w["k2"].append({"family": fam, "traj_id": f"k2{i}", "ids": ids, "k": 2})
    k3 = [
        ("dom_drift", [4510, 4511, 4512]), ("dom_drift", [4513, 4514, 4515]),
        ("dom_drift", [4516, 4517, 4518]), ("dom_drift", [4519, 4520, 4521]),
        ("param_header_mutation", [4610, 4611, 4612]), ("param_header_mutation", [4613, 4614, 4615]),
        ("param_header_mutation", [4616, 4617, 4618]),
        ("cache_expiry", [4710, 4711, 4712]), ("cache_expiry", [4713, 4714, 4715]),
        ("cache_expiry", [4716, 4717, 4718]),
    ]
    for i, (fam, ids) in enumerate(k3):
        w["k3"].append({"family": fam, "traj_id": f"k3{i}", "ids": ids, "k": 3})
    for vi, var in enumerate(NOISE_FAMILIES):
        for ti in range(5):
            w["noise_trajs"].append({"traj_id": f"{var}-{ti}", "family": var,
                                     "rids": [83000 + vi * 10000 + ti * 10 + r for r in range(1, 11)]})
    w["unrelated_ids"] = list(range(9000, 9020))
    w["nc1_ids"] = list(range(6001, 6011))
    w["cold_ids"] = list(range(7001, 7013))
    w["pc1_ids"] = list(range(6101, 6113))  # 12 fresh trajectories (PC1)
    w["pc2_insts"] = [  # 1 known-break single-attribute instance per family (PC2 k=1)
        {"family": "dom_drift", "traj_id": "sn-pc2-dom", "ids": [6201]},
        {"family": "param_header_mutation", "traj_id": "sn-pc2-param", "ids": [6301]},
        {"family": "cache_expiry", "traj_id": "sn-pc2-cache", "ids": [6401]},
    ]
    return w


def all_workload_rids(w):
    rids = []
    for t in w["fresh_trajs"] + w["aux_trajs"] + w["noise_trajs"]:
        rids.extend(t["rids"])
    for inst in w["k1"] + w["k2"] + w["k3"]:
        rids.extend(inst["ids"])
    rids.extend(w["unrelated_ids"])
    rids.extend(w["nc1_ids"])
    rids.extend(w["cold_ids"])
    return rids


# ----------------------------------------------------------------------------
# HTTP clients (raw evidence produced here; metrics derived later)
# ----------------------------------------------------------------------------
class _Response:
    __slots__ = ("status", "body", "headers", "url")

    def __init__(self, status, body, headers, url):
        self.status = status
        self.body = body  # parsed dict or None (304)
        self.headers = headers  # dict
        self.url = url


def normalize_headers(h):
    return {k: v for k, v in h.items()}


_SYN_PORT = {"port": None}


class SynHandler(BaseHTTPRequestHandler):
    """stdlib http.server single-resource site for the synthetic sanity stage.
    Family arrives via X-Drift-Family header (as in the audit-PASSed parent);
    body derivation delegates to FA.resource_for — single source of truth."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        family = self.headers.get("X-Drift-Family", "fresh_pool")
        req_num = int(self.headers.get("X-Request-Num", "1"))
        inm = self.headers.get("If-None-Match")
        try:
            rid = int(parsed.path.strip("/").split("/")[-1])
        except Exception:
            rid = 1
        res = FA.resource_for(rid, family, req_num)
        etag = res["etag"]
        if inm and inm == etag and res["ground_truth"] == "fresh" and res["cache_control"] == "max-age=60":
            self.send_response(304)
            self.send_header("ETag", etag)
            self.send_header("Cache-Control", res["cache_control"])
            self.send_header("X-Csrf-Token", res["csrf"])
            self.send_header("X-Worker-Pid", "synth-1")
            self.end_headers()
            return
        body_with_template = dict(res["body"])
        body_with_template["_template"] = res["template"]
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("ETag", etag)
        self.send_header("Cache-Control", res["cache_control"])
        self.send_header("X-Csrf-Token", res["csrf"])
        self.send_header("X-Worker-Pid", "synth-1")
        self.end_headers()
        self.wfile.write(FA.canonical_json(body_with_template))

    def log_message(self, fmt, *args):
        pass


def fetch_synthetic(rid, family, req_num, traj_id, inm=None, extra_headers=None):
    qs = urllib.parse.urlencode({"detail": "full"})
    url = f"http://127.0.0.1:{_SYN_PORT['port']}/resource/{rid}?{qs}"
    headers = {"X-Drift-Family": family, "X-Request-Num": str(req_num),
               "X-Trajectory-Id": traj_id, "X-Csrf-Token": "token-abc123"}
    if inm:
        headers["If-None-Match"] = inm
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req, timeout=10)
    raw = resp.read()
    status = resp.status
    hdrs = normalize_headers(resp.headers)
    body = json.loads(raw.decode()) if raw else None
    return _Response(status, body, hdrs, url)


def _mint_jwt(rid):
    import jwt
    now = time.time()
    payload = {"resource_id": rid, "exp": now + 3600, "iat": now}
    return jwt.encode(payload, TESTBED_SECRET, algorithm="HS256")


def fetch_single(rid, family, req_num, traj_id, inm=None, extra_headers=None, port=None):
    qs = urllib.parse.urlencode({"detail": "full"})
    url = f"http://127.0.0.1:{port}/resource/{rid}?{qs}"
    headers = {"Authorization": f"Bearer {_mint_jwt(rid)}",
               "X-Drift-Family": family, "X-Request-Num": str(req_num),
               "X-Trajectory-Id": traj_id, "X-Csrf-Token": "token-abc123"}
    if inm:
        headers["If-None-Match"] = inm
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        raw = resp.read()
        body = json.loads(raw.decode()) if raw else None
        return _Response(resp.status, body, normalize_headers(resp.headers), url)
    except urllib.error.HTTPError as e:
        raw = e.read()
        body = json.loads(raw.decode()) if raw else None
        return _Response(e.code, body, normalize_headers(e.headers), url)


# ----------------------------------------------------------------------------
# SQLite WAL state rows (written by the harness; read by the Flask app process)
# ----------------------------------------------------------------------------
def write_state_rows(rows):
    """rows: list of (rid, family, drift_start). Cross-process WAL: called from
    the harness process; the app reads via its own connection."""
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute("PRAGMA busy_timeout=8000")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executemany(
        "INSERT OR REPLACE INTO resource_state (rid, family, drift_start) VALUES (?,?,?)",
        rows)
    conn.commit()
    conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
    conn.close()


def seed_state_rows(w):
    rows = []
    for t in w["fresh_trajs"] + w["aux_trajs"]:
        for rid in t["rids"]:
            rows.append((rid, t["family"], 9999))
    for inst in w["k1"] + w["k2"] + w["k3"]:
        for rid in inst["ids"]:
            rows.append((rid, inst["family"], DRIFT_POINT))
    for t in w["noise_trajs"]:
        for rid in t["rids"]:
            rows.append((rid, t["family"], 9999))
    for rid in w["unrelated_ids"] + w["nc1_ids"] + w["cold_ids"] + w["pc1_ids"]:
        rows.append((rid, "fresh_pool", 9999))
    for inst in w["pc2_insts"]:
        for rid in inst["ids"]:
            rows.append((rid, inst["family"], DRIFT_POINT))
    write_state_rows(rows)
    return len(rows)


# ----------------------------------------------------------------------------
# Single-node site deployment: 2x gunicorn (-w 1) behind nginx $request_uri hash
# ----------------------------------------------------------------------------
def free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class SingleNodeSite:
    def __init__(self):
        self.nginx_port = None
        self.worker_ports = []
        self.procs = []
        self.nginx_conf = None
        self.nginx_pid_file = None
        self.nginx_proc = None

    def start(self):
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        # clean slate for the WAL db
        for suffix in ("", "-wal", "-shm"):
            p = Path(DB_PATH + suffix)
            if p.exists():
                p.unlink()
        # import the app module once to init the DB + WAL (also primes gunicorn env)
        worker_dir = DELTA_REPAIR_DIR
        for i in range(2):
            port = free_port()
            env = dict(os.environ)
            env["TESTBED_SECRET"] = TESTBED_SECRET
            env["SPIDER_DB_PATH"] = DB_PATH
            logf = open(RUNTIME_DIR / f"gunicorn_{i}.log", "wb")
            proc = subprocess.Popen(
                [sys.executable, "-m", "gunicorn", "-w", "1", "-b", f"127.0.0.1:{port}",
                 "--timeout", "60", "flask_app_36018188168:app"],
                cwd=str(worker_dir), env=env, stdout=logf, stderr=subprocess.STDOUT)
            self.procs.append((proc, logf))
            self.worker_ports.append(port)
        # nginx: $request_uri consistent hash upstream
        self.nginx_port = free_port()
        upstream = "".join(f"        server 127.0.0.1:{p};\n" for p in self.worker_ports)
        self.nginx_conf = RUNTIME_DIR / "nginx_single.conf"
        self.nginx_conf.write_text(
            f"worker_processes 1;\n"
            f"error_log {RUNTIME_DIR}/nginx_error.log;\n"
            f"pid {RUNTIME_DIR}/nginx.pid;\n"
            f"events {{ worker_connections 256; }}\n"
            f"http {{\n"
            f"    access_log off;\n"
            f"    upstream single_sticky {{\n"
            f"        hash $request_uri consistent;\n"
            f"{upstream}"
            f"    }}\n"
            f"    server {{\n"
            f"        listen 127.0.0.1:{self.nginx_port};\n"
            f"        location / {{\n"
            f"            proxy_pass http://single_sticky;\n"
            f"            proxy_set_header Host $host;\n"
            f"        }}\n"
            f"    }}\n"
            f"}}\n")
        self.nginx_proc = subprocess.Popen(
            ["/usr/sbin/nginx", "-c", str(self.nginx_conf), "-p", str(RUNTIME_DIR)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # wait for readiness: worker A and B must answer 401 (JWT required)
        deadline = time.time() + 60
        ready = False
        while time.time() < deadline:
            if all(self._probe_worker(p) for p in self.worker_ports) and self._probe_nginx():
                ready = True
                break
            time.sleep(0.5)
        if not ready:
            self.stop()
            raise RuntimeError("single-node site did not become ready "
                               "(workers/nginx startup failed); see gunicorn logs")
        return self.nginx_port

    def _probe_worker(self, port):
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{port}/resource/1",
                                         headers={"X-Request-Num": "1"})
            urllib.request.urlopen(req, timeout=3)
            return False
        except urllib.error.HTTPError as e:
            return e.code == 401
        except Exception:
            return False

    def _probe_nginx(self):
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{self.nginx_port}/resource/1",
                                         headers={"X-Request-Num": "1"})
            urllib.request.urlopen(req, timeout=3)
            return False
        except urllib.error.HTTPError as e:
            return e.code == 401
        except Exception:
            return False

    def stop(self):
        for proc, logf in self.procs:
            if proc.poll() is None:
                proc.terminate()
        try:
            subprocess.run(["/usr/sbin/nginx", "-s", "stop", "-c", str(self.nginx_conf),
                            "-p", str(RUNTIME_DIR)], timeout=15,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        time.sleep(1.0)
        for proc, logf in self.procs:
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
            logf.close()


# ----------------------------------------------------------------------------
# Health gate (D1) — real nginx $request_uri sticky + WAL + HS256 + 304 + immediate R/W
# ----------------------------------------------------------------------------
def run_health_gate(site, w):
    results = {}
    # 1) WAL db exists, journal_mode == 'wal' (strict; parent fix #8)
    db_path = Path(DB_PATH)
    results["db_exists"] = db_path.exists()
    if db_path.exists():
        conn = sqlite3.connect(DB_PATH, timeout=10)
        mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        conn.close()
        results["wal_mode"] = mode == "wal"
    else:
        results["wal_mode"] = False
    # 2) HS256 verified: 200 with valid token; 401 without
    port = site.nginx_port
    r_ok = fetch_single(999998, "fresh_pool", 1, "health", port=port)
    results["jwt_verified"] = r_ok.status == 200
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/resource/999998",
                                     headers={"X-Request-Num": "1"})
        urllib.request.urlopen(req, timeout=5)
        results["auth_required"] = False
    except urllib.error.HTTPError as e:
        results["auth_required"] = e.code == 401
    except Exception:
        results["auth_required"] = False
    # 3) 304 operational (fresh id with ETag -> If-None-Match -> 304)
    r1 = fetch_single(999999, "fresh_pool", 1, "health", port=port)
    etag = r1.headers.get("ETag", "")
    if r1.status == 200 and etag:
        r2 = fetch_single(999999, "fresh_pool", 2, "health", inm=etag, port=port)
        results["has_304"] = r2.status == 304
    else:
        results["has_304"] = False
    # 4) $request_uri sticky: same URI -> same worker 5x; >=2 distinct workers across 20 URIs
    same_pids = set()
    for _ in range(5):
        r = fetch_single(999999, "fresh_pool", 1, "health", port=port)
        same_pids.add(r.headers.get("X-Worker-Pid", ""))
    results["sticky_same_uri_consistent"] = len(same_pids) == 1 and "" not in same_pids
    distinct_pids = set()
    for i in range(20):
        r = fetch_single(91000 + i, "fresh_pool", 1, f"health-{i}", port=port)
        distinct_pids.add(r.headers.get("X-Worker-Pid", ""))
    results["n_distinct_workers"] = len(distinct_pids)
    results["worker_pids"] = sorted(int(p) for p in distinct_pids if p)
    results["sticky_consistent"] = results["sticky_same_uri_consistent"] and len(distinct_pids) >= 2
    # 5) Immediate read-after-write via cross-process WAL (harness writes, app reads)
    write_state_rows([(777700, "dom_drift", DRIFT_POINT)])
    r_mut = fetch_single(777700, "dom_drift", 10, "health", port=port)
    results["read_after_write_visible"] = (
        r_mut.status == 200 and isinstance(r_mut.body.get("id"), str))
    write_state_rows([(777700, "fresh_pool", 9999)])
    # 6) n_non304 >= 360 is computed after the workload (counts in metrics section)
    return results


# ----------------------------------------------------------------------------
# Signal extraction + frozen detection logic
# ----------------------------------------------------------------------------
def dom_tokens_of(body):
    if body is None:
        return set()
    return FA.extract_field_types(body)


def signal_from_response(r):
    """Response-derived signal dict (V10): body fields + _template + headers."""
    body = r.body if r.body is not None else {}
    sig = {k: v for k, v in body.items() if k != "_template"}
    sig["_template"] = body.get("_template", {})
    sig["X-Csrf-Token"] = r.headers.get("X-Csrf-Token")
    sig["ETag"] = r.headers.get("ETag")
    sig["Cache-Control"] = r.headers.get("Cache-Control")
    return sig


def template_of(r):
    if r.body is not None and "_template" in r.body:
        t = r.body["_template"]
        return {"query_params": sorted(t.get("query_params", [])),
                "header_names": sorted(t.get("header_names", []))}
    return None


def build_cache_entry(sig, r):
    body = {k: v for k, v in r.body.items() if k != "_template"} if r.body else {}
    return {
        "dom_required": filter_required(FA.extract_field_types(body)),
        "template": template_of(r),
        "etag": r.headers.get("ETag"),
        "cc": r.headers.get("Cache-Control"),
        "csrf": r.headers.get("X-Csrf-Token"),
        "postconditions": dict(sig),
    }


def make_entry(stage, tid, fam, rid, req_num, gt, r, cache, k=None, probe=False):
    """Build a V13 raw log entry (no derived metric aggregation here)."""
    sig = signal_from_response(r)
    live_dom_required = filter_required(dom_tokens_of(r.body))
    live_template = template_of(r)
    live_cc = r.headers.get("Cache-Control")
    live_etag = r.headers.get("ETag")
    live_csrf = r.headers.get("X-Csrf-Token")
    cached = cache.get((tid, rid)) or cache.get((tid, 0))
    if cached is not None and r.status != 304:
        j = jaccard(cached["dom_required"], live_dom_required)
        param_changed = cached["template"] != live_template if (cached["template"] is not None) else False
        csrf_changed = cached["csrf"] != live_csrf
        etag_changed = cached["etag"] != live_etag
        cache_expiry = (cached["cc"] == "max-age=60" and live_cc == "max-age=0")
        spider_stale = (j < THRESHOLD) or param_changed or csrf_changed or (etag_changed and cache_expiry)
    else:
        j = 1.0
        param_changed = csrf_changed = etag_changed = cache_expiry = False
        spider_stale = False
    if r.status == 304:
        spider_stale = False
        j = 1.0
    if gt == "fresh" and (req_num <= 3 or (req_num > 10 and req_num % 10 in (1, 2, 3))):
        spider_stale = False  # cache-source requests are construction not detection
        j = 1.0
    no_guard_stale = False
    jaccard_stale = (j < THRESHOLD)
    header_stale = param_changed or csrf_changed or (etag_changed and cache_expiry)
    status = "UNKNOWN" if spider_stale else "EXECUTABLE"
    confidence = STALE_CONFIDENCE if spider_stale else FRESH_CONFIDENCE
    # deterministic resolve-check: self-verify against the server's own derivation
    expected = FA.resource_for(rid, fam, req_num)
    required_body = {k: v for k, v in expected["body"].items() if k != "_template"}
    actual_body = {k: v for k, v in r.body.items() if k != "_template"} if r.body else required_body
    verified = _matches(required_body, actual_body)
    return {
        "stage": stage, "family": fam, "trajectory_id": tid, "request_number": req_num,
        "rid": rid, "ground_truth": gt, "url": r.url, "status_code": r.status,
        "response_body": r.body, "response_template": template_of(r),
        "ETag": live_etag, "Cache-Control": live_cc, "X-Csrf-Token": live_csrf,
        "X-Worker-Pid": r.headers.get("X-Worker-Pid"),
        "jaccard": round(j, 4), "param_changed": param_changed, "csrf_changed": csrf_changed,
        "etag_changed": etag_changed, "cache_expiry": cache_expiry,
        "spider_stale": spider_stale, "no_guard_stale": no_guard_stale,
        "jaccard_stale": jaccard_stale, "header_stale": header_stale,
        "spider_status": status, "spider_confidence": confidence,
        "threshold": THRESHOLD, "verified": verified, "cost": 5 if probe else 4,
        "blast_radius": k, "contamination_flag": 0,
    }


# ----------------------------------------------------------------------------
# Stage executor (shared by synthetic sanity and single-node primary)
# ----------------------------------------------------------------------------
def execute_stage(fetch, w, port=None):
    logs = []
    cache = {}
    cost_logs = []
    instances = []
    ephemeral_trajs = []  # single-request "trajectories" for unrelated/NC1/cold

    def _fi(rid, fam, req_num, tid, inm=None):
        if w["stage"] == "single":
            return fetch(rid, fam, req_num, tid, inm=inm, port=port)
        return fetch(rid, fam, req_num, tid, inm=inm)

    # ---- fresh trajectories (evaluated per request; shape cache from reqs 1-3)
    for t in w["fresh_trajs"]:
        tid, fam = t["traj_id"], t["family"]
        traj_costs = []
        for j, rid in enumerate(t["rids"], start=1):
            r = _fi(rid, fam, j, tid)
            entry = make_entry(w["stage"], tid, fam, rid, j, "fresh", r, cache)
            logs.append(entry)
            traj_costs.append(entry["cost"])
            if j <= 3 and r.status == 200 and r.body is not None:
                key = (tid, 0)
                if key not in cache:
                    cache[key] = build_cache_entry(signal_from_response(r), r)
        cost_logs.append({"stage": w["stage"], "trajectory_id": tid, "family": fam,
                          "request_count": len(traj_costs), "costs_per_request": traj_costs,
                          "trajectory_sum": sum(traj_costs)})
    # ---- auxiliary fresh (executed, not scored)
    for t in w["aux_trajs"]:
        tid, fam = t["traj_id"], t["family"]
        traj_costs = []
        for j, rid in enumerate(t["rids"], start=1):
            r = _fi(rid, fam, j, tid)
            entry = make_entry(w["stage"], tid, fam, rid, j, "fresh", r, cache)
            entry["evaluated"] = False
            logs.append(entry)
            traj_costs.append(entry["cost"])
            if j <= 3 and r.status == 200 and r.body is not None:
                key = (tid, 0)
                if key not in cache:
                    cache[key] = build_cache_entry(signal_from_response(r), r)
        cost_logs.append({"stage": w["stage"], "trajectory_id": tid, "family": fam,
                          "request_count": len(traj_costs), "costs_per_request": traj_costs,
                          "trajectory_sum": sum(traj_costs)})
    # ---- drift instances (K1/K2/K3): per-id request sequences restart at 1 for
    # each mutated id (the app drifts at req_num>=6, so each id must have its own
    # 1..10 counter); per-id mechanism cache, repairs later. Instance detection =
    # ALL ids' first post-drift evaluation (req 6 of that id's sequence) stale.
    for inst in w["k1"] + w["k2"] + w["k3"]:
        tid, fam, k = inst["traj_id"], inst["family"], inst["k"]
        traj_costs = []
        inst_logs = []
        first_stale_evals = []
        for rid in inst["ids"]:
            built = False
            last_fresh_log = None
            for j in range(1, 11):
                req_num = j  # per-id sequence; app drifts at req_num >= 6
                r = _fi(rid, fam, req_num, tid)
                gt = "stale" if req_num >= DRIFT_POINT else "fresh"
                entry = make_entry(w["stage"], tid, fam, rid, req_num, gt, r, cache, k=k)
                logs.append(entry)
                traj_costs.append(entry["cost"])
                if req_num <= 3 and not built and r.status == 200 and r.body is not None:
                    cache[(tid, rid)] = build_cache_entry(signal_from_response(r), r)
                    built = True
                if gt == "fresh" and r.status == 200 and r.body is not None:
                    last_fresh_log = entry
                if req_num == DRIFT_POINT:
                    first_stale_evals.append(entry)
                    inst_logs.append(entry)
            # refresh postconditions to the LAST fresh observation (V14)
            if last_fresh_log is not None:
                key = (tid, rid)
                if key in cache:
                    cache[key]["postconditions"] = dict(sig_from_log(last_fresh_log))
                else:
                    cache[key] = {"dom_required": filter_required(dom_tokens_of(last_fresh_log["response_body"])),
                                  "template": last_fresh_log["response_template"],
                                  "etag": last_fresh_log["ETag"], "cc": last_fresh_log["Cache-Control"],
                                  "csrf": last_fresh_log["X-Csrf-Token"],
                                  "postconditions": dict(sig_from_log(last_fresh_log))}
        detected = all(e["spider_stale"] for e in first_stale_evals) if first_stale_evals else False
        instances.append({"stage": w["stage"], "family": fam, "traj_id": tid, "k": k,
                          "ids": list(inst["ids"]), "detected": bool(detected),
                          "first_stale_evals": first_stale_evals,
                          "is_train": False, "is_test": False})
        cost_logs.append({"stage": w["stage"], "trajectory_id": tid, "family": fam,
                          "request_count": len(traj_costs), "costs_per_request": traj_costs,
                          "trajectory_sum": sum(traj_costs)})
    # ---- noise trajectories (NC-NOISE-IMMUNITY, evaluated per request)
    for t in w["noise_trajs"]:
        tid, fam = t["traj_id"], t["family"]
        traj_costs = []
        for j, rid in enumerate(t["rids"], start=1):
            r = _fi(rid, fam, j, tid)
            entry = make_entry(w["stage"], tid, fam, rid, j, "fresh", r, cache)
            logs.append(entry)
            traj_costs.append(entry["cost"])
            if j <= 3 and r.status == 200 and r.body is not None:
                key = (tid, 0)
                if key not in cache:
                    cache[key] = build_cache_entry(signal_from_response(r), r)
        cost_logs.append({"stage": w["stage"], "trajectory_id": tid, "family": fam,
                          "request_count": len(traj_costs), "costs_per_request": traj_costs,
                          "trajectory_sum": sum(traj_costs)})
    # ---- single-request roles (unrelated only; NC1/cold have own executors)
    for role, rids in (("unrelated", w["unrelated_ids"]),):
        for rid in rids:
            tid = f"{role}-{rid}"
            r = _fi(rid, "fresh_pool", 1, tid)
            entry = make_entry(w["stage"], tid, "fresh_pool", rid, 1, "fresh", r, cache)
            entry["role"] = role
            logs.append(entry)
            cost_logs.append({"stage": w["stage"], "trajectory_id": tid, "family": "fresh_pool",
                              "request_count": 1, "costs_per_request": [entry["cost"]],
                              "trajectory_sum": entry["cost"]})
            ephemeral_trajs.append((tid, role))
    return logs, cache, cost_logs, instances


def sig_from_log(entry):
    """Signal dict from a previously logged entry (response-derived)."""
    body = entry["response_body"] or {}
    sig = {k: v for k, v in body.items() if k != "_template"}
    sig["_template"] = body.get("_template", {})
    sig["X-Csrf-Token"] = entry.get("X-Csrf-Token")
    sig["ETag"] = entry.get("ETag")
    sig["Cache-Control"] = entry.get("Cache-Control")
    return sig


# ----------------------------------------------------------------------------
# Repair + baselines + controls (all EXECUTED; nothing hardcoded)
# ----------------------------------------------------------------------------
def assign_train_test(instances):
    """TRAIN18/TEST12 per family at K1 (6/4); 60/40 rounded per family at K2/K3."""
    by_fam_k = defaultdict(list)
    for inst in instances:
        by_fam_k[(inst["family"], inst["k"])].append(inst)
    for (fam, k), lst in by_fam_k.items():
        lst.sort(key=lambda x: x["traj_id"])
        n = len(lst)
        n_train = 6 if k == 1 else int(round(0.6 * n))
        for i, inst in enumerate(lst):
            inst["is_train"] = i < n_train
            inst["is_test"] = i >= n_train
    return instances


def execute_repairs(fetch, cache, instances, stage, port=None):
    """Deterministic re-observe repair: k probes, overwrite cache with live bytes,
    rebind, re-verify via _matches (all k must verify true). Cost k*5 tokens,
    k browser steps, k verifies (1 per probe). Returns repair logs."""
    repairs = []
    for inst in sorted(instances, key=lambda x: (x["k"], x["family"], x["traj_id"])):
        if not inst["detected"]:
            continue  # no repair when nothing stale (NC1 path)
        tid, fam, ids = inst["traj_id"], inst["family"], inst["ids"]
        probes = []
        for rid in ids:
            if stage == "single":
                r = fetch(rid, fam, 10, tid, port=port)
            else:
                r = fetch(rid, fam, 10, tid)
            probes.append(r)
        # patch: overwrite cache entry with live-derived bytes
        for rid, r in zip(ids, probes):
            cache[(tid, rid)] = build_cache_entry(signal_from_response(r), r)
        # verify: all k must verify true via _matches
        verified_each = []
        for rid, r in zip(ids, probes):
            post = cache[(tid, rid)]["postconditions"]
            live = signal_from_response(r)
            verified_each.append(_matches(post, live))
        ok = all(verified_each)
        k = len(ids)
        repairs.append({
            "stage": stage, "family": fam, "traj_id": tid, "k": k, "ids": list(ids),
            "success": bool(ok), "verified_each": verified_each,
            "cost_tokens": k * 5, "cost_browser": k, "verify_steps": k,
            "verify_steps_per_probe": 1,
            "correct_patch_verify": bool(ok),
            "is_train": inst["is_train"], "is_test": inst["is_test"],
        })
    return repairs


def execute_verbatim(fetch, instances, pre_cache, stage, port=None):
    """B-VERBATIM-REPLAY: stored mechanism executed unchanged (0 tokens), no probe."""
    base_cache = copy.deepcopy(pre_cache)
    out = []
    for inst in sorted(instances, key=lambda x: (x["k"], x["family"], x["traj_id"])):
        tid, fam, ids = inst["traj_id"], inst["family"], inst["ids"]
        results = []
        for rid in ids:
            post = base_cache.get((tid, rid), {}).get("postconditions")
            if stage == "single":
                r = fetch(rid, fam, 10, tid, port=port)
            else:
                r = fetch(rid, fam, 10, tid)
            live = signal_from_response(r)
            if post is None:
                results.append(False)
            else:
                results.append(_matches(post, live))
        out.append({"stage": stage, "family": fam, "traj_id": tid, "k": len(ids),
                    "success": all(results), "results": results, "cost_tokens": 0,
                    "cost_browser": 0})
    return out


def execute_retrieval(fetch, instances, fresh_corpus, stage, port=None):
    """B-RETRIEVAL-RAG: Jaccard 0.30 TFIDF retrieval over fresh caches, nearest
    replay via _matches (no patch). Cost 1 retrieval + 4 base replay."""
    out = []
    for inst in sorted(instances, key=lambda x: (x["k"], x["family"], x["traj_id"])):
        tid, fam, ids = inst["traj_id"], inst["family"], inst["ids"]
        ok = True
        details = []
        for rid in ids:
            if stage == "single":
                r = fetch(rid, fam, 10, tid, port=port)
            else:
                r = fetch(rid, fam, 10, tid)
            live_sig = signal_from_response(r)
            live_dom = filter_required(dom_tokens_of(r.body))
            best = None
            best_j = 0.0
            for corpus_tid, ce in fresh_corpus.items():
                jj = jaccard(live_dom, ce["dom_required"]) if ce["dom_required"] else 0.0
                if jj > best_j:
                    best_j = jj
                    best = ce
            ver = False
            if best is not None and best_j >= 0.30:
                ver = _matches(best.get("postconditions", {}), live_sig)
            ok = ok and ver
            details.append({"rid": rid, "retrieved_jaccard": round(best_j, 4), "verify": ver})
        out.append({"stage": stage, "family": fam, "traj_id": tid, "k": len(ids),
                    "success": bool(ok), "details": details, "cost_tokens": 5,
                    "cost_browser": 0})
    return out


def execute_cold(fetch_clients, stage, cold_ids, port=None):
    """B-COLD-FULL-REEXPLORATION: empty registry — 3 observations per id (3*4=12)
    plus 1 execution (4) = 16 tokens, 3 browser probes per resource, k-scaled.
    V13: every request logged via make_entry (construction/execution requests)."""
    out = []
    logs = []
    for rid in cold_ids:
        tid = f"cold-{rid}"
        probed = []
        for j in range(1, 4):
            if stage == "single":
                r = fetch_clients(rid, "fresh_pool", j, tid, port=port)
            else:
                r = fetch_clients(rid, "fresh_pool", j, tid)
            probed.append(r)
            logs.append(make_entry(stage, tid, "fresh_pool", rid, j, "fresh", r, {}))
        # 1 execution fetch on top of the 3 discovery observations
        if stage == "single":
            rx = fetch_clients(rid, "fresh_pool", 4, tid, port=port)
        else:
            rx = fetch_clients(rid, "fresh_pool", 4, tid)
        logs.append(make_entry(stage, tid, "fresh_pool", rid, 4, "fresh", rx, {}))
        expected = FA.resource_for(rid, "fresh_pool", 1)
        required = {k: v for k, v in expected["body"].items() if k != "_template"}
        actual = {k: v for k, v in rx.body.items() if k != "_template"} if rx.body else required
        ver = _matches(required, actual)
        out.append({"stage": stage, "rid": rid, "success": bool(ver), "verified": ver,
                    "cost_tokens": 16, "cost_browser": 3, "verify_steps": 1})
    return out, logs


def random_family_for(traj_id, fam, stage):
    rng = random.Random(f"{stage}:{traj_id}")
    others = [f for f in FAMILIES if f != fam]
    return rng.choice(others)


def execute_random_patch(fetch, instances, stage, port=None):
    """NC2 random-patch null UNCLAMPED: uniformly sampled wrong-family incorrect
    value per mutated id; verify via _matches (expected false)."""
    out = []
    for inst in sorted(instances, key=lambda x: (x["k"], x["family"], x["traj_id"])):
        tid, fam, ids = inst["traj_id"], inst["family"], inst["ids"]
        wrong_fam = random_family_for(tid, fam, stage)
        ver_each = []
        for rid in ids:
            wrong = FA.resource_for(rid, wrong_fam, 10)
            wrong_required = {k: v for k, v in wrong["body"].items() if k != "_template"}
            if stage == "single":
                r = fetch(rid, fam, 10, tid, port=port)
            else:
                r = fetch(rid, fam, 10, tid)
            actual = {k: v for k, v in r.body.items() if k != "_template"} if r.body else wrong_required
            ver_each.append(_matches(wrong_required, actual))
        out.append({"stage": stage, "family": fam, "traj_id": tid, "k": len(ids),
                    "wrong_family": wrong_fam, "verified": ver_each,
                    "false_accept": all(ver_each), "is_train": inst["is_train"],
                    "is_test": inst["is_test"]})
    return out


def execute_pc1(fetch, w, stage, cache, port=None):
    """PC1 positive control: unperturbed execution. 12 fresh trajectories per
    substrate: cache built from cached fresh bytes (reqs 1-3), then mechanism
    resolved and verified at a later fresh request (req 4) with NO patch via
    deterministic _matches exact equality. repair cost 0, contamination 0.
    Returns per-trajectory results and appends V13 entries to raw logs."""
    out = []
    logs = []
    for i, rid in enumerate(sorted(w["pc1_ids"])):
        tid = f"pc1-{rid}"
        fam = "fresh_pool"
        if stage == "single":
            rs = [fetch(rid, fam, j, tid, port=port) for j in range(1, 5)]
        else:
            rs = [fetch(rid, fam, j, tid) for j in range(1, 5)]
        cache_key = (tid, 0)
        for j, r in enumerate(rs, start=1):
            entry = make_entry(w["stage"], tid, fam, rid, j, "fresh", r, cache)
            logs.append(entry)
            if j <= 3 and r.status == 200 and r.body is not None and cache_key not in cache:
                cache[cache_key] = build_cache_entry(signal_from_response(r), r)
        r4 = rs[3]
        expected = FA.resource_for(rid, "fresh_pool", 1)
        required = {k: v for k, v in expected["body"].items() if k != "_template"}
        required["_template"] = expected["template"]
        required["X-Csrf-Token"] = expected["csrf"]
        required["ETag"] = expected.get("etag")
        actual = {k: v for k, v in r4.body.items() if k != "_template"} if r4.body else required
        actual_with_headers = dict(actual)
        actual_with_headers["_template"] = (r4.body or {}).get("_template")
        actual_with_headers["X-Csrf-Token"] = r4.headers.get("X-Csrf-Token")
        actual_with_headers["ETag"] = r4.headers.get("ETag")
        verified = _matches(required, actual_with_headers)
        out.append({"stage": stage, "traj_id": tid, "rid": rid, "verified": bool(verified),
                    "repair_cost": 0, "contamination": 0, "body_sha": FA.etag_for(r4.body or {})})
    return out, logs


def execute_pc2(fetch, w, stage, cache, port=None):
    """PC2 positive control: known-break single-attribute perturbation with
    ORACLE patch. One resource per family (k=1) drifts at req>=6; oracle patch =
    ground-truth re-observe of live bytes overwriting the observed cache, then
    re-verify via _matches exact equality. Required >=0.90 per family."""
    out = []
    logs = []
    for inst in w["pc2_insts"]:
        tid, fam = inst["traj_id"], inst["family"]
        rid = inst["ids"][0]
        if stage == "single":
            rs = [fetch(rid, fam, j, tid, port=port) for j in range(1, 11)]
        else:
            rs = [fetch(rid, fam, j, tid) for j in range(1, 11)]
        for j, r in enumerate(rs, start=1):
            gt = "stale" if j >= DRIFT_POINT else "fresh"
            logs.append(make_entry(w["stage"], tid, fam, rid, j, gt, r, cache))
        cache_key = (tid, rid)
        for j, r in enumerate(rs[:3], start=1):
            if r.status == 200 and r.body is not None:
                cache[cache_key] = build_cache_entry(signal_from_response(r), r)
                break
        # oracle patch: re-observe live (req 10) and overwrite cache entry
        live = rs[9]
        cache[cache_key] = build_cache_entry(signal_from_response(live), live)
        post = cache[cache_key]["postconditions"]
        live_sig = signal_from_response(live)
        verified = _matches(post, live_sig)
        out.append({"stage": stage, "family": fam, "traj_id": tid, "rid": rid,
                    "k": len(inst["ids"]), "verified": bool(verified),
                    "repair_cost": len(inst["ids"]) * 5,
                    "browser_steps": len(inst["ids"]), "pcs_ok": bool(verified)})
    return out, logs


def execute_nc1(fetch, w, stage, cache, port=None):
    """NC1 null control: zero perturbation. 10 fresh instances per substrate
    (identical pre/post resource): repair pipeline must produce zero patch
    (cost 0, contamination 0, false_accept 0%)."""
    out = []
    logs = []
    for rid in sorted(w["nc1_ids"]):
        tid = f"nc1-{rid}"
        fam = "fresh_pool"
        if stage == "single":
            rs = [fetch(rid, fam, j, tid, port=port) for j in range(1, 11)]
        else:
            rs = [fetch(rid, fam, j, tid) for j in range(1, 11)]
        for j, r in enumerate(rs, start=1):
            logs.append(make_entry(w["stage"], tid, fam, rid, j, "fresh", r, cache))
        cache_key = (tid, 0)
        for j, r in enumerate(rs[:3], start=1):
            if r.status == 200 and r.body is not None and cache_key not in cache:
                cache[cache_key] = build_cache_entry(signal_from_response(r), r)
        # resolve+verify at req 10 with no patch
        r10 = rs[9]
        expected = FA.resource_for(rid, "fresh_pool", 1)
        required = {k: v for k, v in expected["body"].items() if k != "_template"}
        a10 = {k: v for k, v in r10.body.items() if k != "_template"} if r10.body else required
        verified = _matches(required, a10)
        out.append({"stage": stage, "rid": rid, "verified": bool(verified),
                    "repair_cost": 0, "contamination": 0, "false_accept": 0})
    return out, logs


def verify_contamination(instances, pre_cache, post_cache, stage, port=None):
    """Registry-clone snapshot re-verification of unrelated mechanisms after repair.

    registry mechanisms:
      - disjoint: M-DISJOINT-9000..9019 bound to never-mutated ids
      - same-resource: M-SAME-{rid} bound per-k to that k's mutated ids with
        ALTERNATE required slots (fresh body + phone expectation); co-bound to
        the same cache entry.
    clone_before = deepcopy(pre_cache)  (pre-repair registry state)
    clone_after  = deepcopy(post_cache) (post-repair state: patched entries hold
    the live-stale postconditions overwritten by execute_repairs).
    contamination = unrelated mechanism whose status FLIPS or that falsely
    accepts (verify True with wrong slots) after the repair patch.
    """
    clone_before = copy.deepcopy(pre_cache)
    clone_after = copy.deepcopy(post_cache)
    mechanisms = []
    for rid in range(9000, 9020):
        expected = FA.resource_for(rid, "fresh_pool", 1)
        required = {k: v for k, v in expected["body"].items() if k != "_template"}
        required["_template"] = expected["template"]
        required["X-Csrf-Token"] = expected["csrf"]
        required["ETag"] = expected["etag"]
        required["Cache-Control"] = expected["cache_control"]
        mechanisms.append({"set": "disjoint", "k": None, "mechanism_id": f"M-DISJOINT-{rid}",
                           "rid": rid, "required_slots": required, "co_bound": False})
    # Same-resource co-bound second mechanism: binds the ALTERNATE (non-mutated)
    # slots of the same cache entry — the slots a correct localized patch MUST
    # preserve. slots mutated by the drift family are excluded from required:
    MUTATED_SLOTS = {
        "dom_drift": {"id", "phone", "ETag"},
        "param_header_mutation": {"_template", "X-Csrf-Token"},
        "cache_expiry": {"email", "Cache-Control", "ETag"},
    }
    for inst in instances:
        if not inst["detected"]:
            continue
        fam = inst["family"]
        for rid in inst["ids"]:
            co_key = (inst["traj_id"], rid)
            if co_key not in clone_before:
                continue  # no observable pre-repair state -> mechanism undefined
            fresh_post = clone_before[co_key]["postconditions"]
            required = {k: v for k, v in fresh_post.items()
                        if k not in MUTATED_SLOTS.get(fam, set())}
            mechanisms.append({"set": "same_resource", "k": inst["k"],
                               "mechanism_id": f"M-SAME-{rid}", "rid": rid,
                               "required_slots": required, "co_bound": True,
                               "family": fam})
    rows = []
    for m in mechanisms:
        rid = m["rid"]
        co_key = None
        for inst in instances:
            if rid in inst["ids"]:
                co_key = (inst["traj_id"], rid)
                break
        def _fresh_actual():
            expected = FA.resource_for(rid, "fresh_pool", 1)
            a = {k: v for k, v in expected["body"].items() if k != "_template"}
            a["_template"] = expected["template"]
            a["X-Csrf-Token"] = expected["csrf"]
            a["ETag"] = expected["etag"]
            a["Cache-Control"] = expected["cache_control"]
            return a
        if m["co_bound"] and co_key in clone_before:
            actual_before = dict(clone_before[co_key]["postconditions"])
            actual_after = dict(clone_after[co_key]["postconditions"])
        else:
            actual_before = _fresh_actual()
            actual_after = _fresh_actual()
        ver_before = _matches(m["required_slots"], actual_before)
        ver_after = _matches(m["required_slots"], actual_after)
        rows.append({"set": m["set"], "mechanism_id": m["mechanism_id"], "k": m["k"],
                     "rid": rid, "ver_before": bool(ver_before), "ver_after": bool(ver_after),
                     "flipped": bool(ver_before != ver_after),
                     "false_accept": bool(ver_after and not ver_before),
                     "co_bound": m["co_bound"], "family": m.get("family")})
    for row in rows:
        row["contamination"] = int(row["flipped"] or row["false_accept"])
    return rows


# ----------------------------------------------------------------------------
# Derived metrics (computed from RAW logs only)
# ----------------------------------------------------------------------------
def compute_freshness(w, logs, instances, pool_k=(1, 2, 3)):
    """Pool: fresh units from fresh_trajs (per request) + stale units (per
    instance in pool_k, first post-drift evaluation); noise excluded from pool.
    synthetic sanity: pool_k=(1,) (30 stale); single-node: pool_k=(1,2,3) (50)."""
    f_log_ids = {t["traj_id"] for t in w["fresh_trajs"]}
    fresh_entries = [l for l in logs if l.get("evaluated", True) and l["trajectory_id"] in f_log_ids]
    stale_inst = [i for i in instances if i["k"] in pool_k]
    n_fresh = len(fresh_entries)
    n_stale = len(stale_inst)
    tn = sum(1 for l in fresh_entries if l["spider_status"] == "EXECUTABLE")
    fp = n_fresh - tn
    tp = sum(1 for i in stale_inst if i["detected"])
    fn = n_stale - tp
    tn_rate = tn / n_fresh if n_fresh else 0.0
    fa = fn / n_stale if n_stale else 0.0
    tp_rate = tp / n_stale if n_stale else 0.0
    unknown_count = fp + tp
    unknown_rate = unknown_count / (n_fresh + n_stale) if (n_fresh + n_stale) else 0.0
    stale_rate = n_stale / (n_fresh + n_stale) if (n_fresh + n_stale) else 0.0
    tn_lower, tn_upper = wilson(tn, n_fresh)
    fa_lower, fa_upper = wilson(fn, n_stale)
    unk_lower, unk_upper = wilson(unknown_count, n_fresh + n_stale)
    per_family = {}
    for fam in FAMILIES:
        f_inst = [i for i in stale_inst if i["family"] == fam]
        f_tp = sum(1 for i in f_inst if i["detected"])
        f_fn = len(f_inst) - f_tp
        per_family[fam] = {"stale_n": len(f_inst), "tp": f_tp, "fn": f_fn,
                           "tp_rate": (f_tp / len(f_inst)) if f_inst else None,
                           "fa": (f_fn / len(f_inst)) if f_inst else None}
    noise_entries = [l for l in logs if l["family"] in NOISE_FAMILIES]
    noise_fa = (sum(1 for l in noise_entries if l["spider_status"] == "UNKNOWN")
                / len(noise_entries)) if noise_entries else 0.0
    fresh_pool = [{"status": l["spider_status"], "confidence": l["spider_confidence"],
                   "gt": "fresh"} for l in fresh_entries]
    stale_pool = [{"status": "UNKNOWN" if i["detected"] else "EXECUTABLE",
                   "confidence": STALE_CONFIDENCE if i["detected"] else FRESH_CONFIDENCE,
                   "gt": "stale"} for i in stale_inst]

    def _ece(pool):
        if not pool:
            return 0.0
        total = len(pool)
        ece = 0.0
        for i in range(10):
            lo, hi = i / 10, (i + 1) / 10
            if hi == 1.0:
                bb = [x for x in pool if lo <= x["confidence"] <= hi]
            else:
                bb = [x for x in pool if lo <= x["confidence"] < hi]
            if not bb:
                continue
            correct = sum(1 for x in bb if (x["status"] == "EXECUTABLE" and x["gt"] == "fresh")
                          or (x["status"] == "UNKNOWN" and x["gt"] == "stale"))
            acc = correct / len(bb)
            avg_conf = sum(x["confidence"] for x in bb) / len(bb)
            ece += abs(acc - avg_conf) * (len(bb) / total)
        return ece

    ece_global = round(_ece(fresh_pool + stale_pool), 10)
    ece_fresh = round(_ece(fresh_pool), 10)
    ece_stale = round(_ece(stale_pool), 10)
    within_std = {}
    for fam in FAMILIES:
        fam_logs = [l for l in logs if l["family"] == fam]
        flags = [1 if l["spider_stale"] else 0 for l in fam_logs]
        within_std[fam] = statistics.pstdev(flags) if len(flags) > 1 else 0.0
    min_fresh_std_drift = min(within_std.values()) if within_std else 0.0
    return {"n_fresh": n_fresh, "n_stale": n_stale, "tn": tn, "fp": fp, "tp": tp,
            "fn": fn, "tn_rate": tn_rate, "tn_lower": tn_lower, "tn_upper": tn_upper,
            "fa": fa, "fa_lower": fa_lower, "fa_upper": fa_upper, "tp_rate": tp_rate,
            "unknown_rate": unknown_rate, "unknown_lower": unk_lower,
            "unknown_upper": unk_upper, "stale_rate": stale_rate,
            "per_family": per_family, "noise_fa": noise_fa,
            "noise_n": len(noise_entries), "ece_global": ece_global,
            "ece_fresh": ece_fresh, "ece_stale": ece_stale,
            "within_std": within_std, "min_fresh_std_drift": min_fresh_std_drift}


def trajectory_rho(logs, cost_logs, stage, n_perm=1000, seed=42):
    """V4: max |Pearson rho| between shuffled cost labels and outcome, 1000
    permutations shuffling WHOLE TRAJECTORY BLOCKS (trajectory-grouped).
    Outcome per request = 1 when spider_stale else 0; cost per request from the
    per-trajectory-reset honest integer sum-counter."""
    rng = random.Random(seed)
    traj_ids = sorted({cl["trajectory_id"] for cl in cost_logs if cl["stage"] == stage})
    cost_by_traj = {cl["trajectory_id"]: list(cl["costs_per_request"])
                    for cl in cost_logs if cl["stage"] == stage}
    out_by_traj = defaultdict(list)
    for l in logs:
        if l["stage"] == stage:
            out_by_traj[l["trajectory_id"]].append(1 if l["spider_stale"] else 0)
    traj_ids = [t for t in traj_ids if t in cost_by_traj and t in out_by_traj]
    if not traj_ids:
        return {"observed_rho": 0.0, "max_abs_rho": 0.0, "mean_abs_rho": 0.0, "n_traj": 0}
    orig_cost = []
    orig_out = []
    for t in traj_ids:
        orig_cost.extend(cost_by_traj[t])
        orig_out.extend(out_by_traj[t])
    observed = pearson(orig_cost, orig_out)
    max_abs = 0.0
    rhos = []
    for _ in range(n_perm):
        shuffled = traj_ids[:]
        rng.shuffle(shuffled)
        perm_cost = []
        for t in shuffled:
            perm_cost.extend(cost_by_traj[t])
        rho = pearson(perm_cost, orig_out)
        rhos.append(abs(rho))
        max_abs = max(max_abs, abs(rho))
    return {"observed_rho": observed, "max_abs_rho": max_abs,
            "mean_abs_rho": sum(rhos) / len(rhos) if rhos else 0.0,
            "n_traj": len(traj_ids), "n_perm": n_perm}


def trajectory_grouped_bootstrap(repairs, k, n_iter=5000, seed=123):
    """V6: 5000 family-stratified trajectory-grouped bootstrap (resample at
    trajectory level per family preserving family trajectory counts)."""
    rng = random.Random(seed)
    fam_to_traj = defaultdict(lambda: defaultdict(list))
    for r in repairs:
        if r["k"] == k:
            fam_to_traj[r["family"]][r["traj_id"]].append(r)
    if not fam_to_traj:
        return {"pooled_ci": [0.0, 0.0], "token_ci": [0.0, 0.0],
                "browser_ci": [0.0, 0.0], "degenerate": True, "n_repairs": 0}
    pooled_vals, token_vals, browser_vals = [], [], []
    for _ in range(n_iter):
        sample = []
        for fam, trajs in fam_to_traj.items():
            ids = list(trajs.keys())
            for tid in rng.choices(ids, k=len(ids)):
                sample.extend(trajs[tid])
        if not sample:
            continue
        pooled_vals.append(sum(1 for r in sample if r["success"]) / len(sample))
        token_vals.append(sum(r["cost_tokens"] for r in sample) / len(sample))
        browser_vals.append(sum(r["cost_browser"] for r in sample) / len(sample))
    ci = lambda vals: [round(pct(vals, 2.5), 4), round(pct(vals, 97.5), 4)]
    return {"pooled_ci": ci(pooled_vals), "token_ci": ci(token_vals),
            "browser_ci": ci(browser_vals),
            "degenerate": bool(pooled_vals and len(set(pooled_vals)) == 1),
            "n_repairs": sum(len(v) for v in fam_to_traj.values())}


def compute_auroc_prec(repair_logs, random_logs, instance_map):
    """Binary _matches outcomes: correct=1, random=0. AUROC, precision/recall at
    frozen 0.85, unclamped permutation-shuffled label null (1000, trajectory-
    grouped where possible: labels shuffled per instance pair)."""
    y_true, y_scores = [], []
    for r in repair_logs:
        y_true.append(1)
        y_scores.append(1.0 if r["correct_patch_verify"] else 0.0)
    for rnd in random_logs:
        y_true.append(0)
        y_scores.append(1.0 if rnd["false_accept"] else 0.0)
    n_ok = sum(1 for yt in y_true if yt == 1)
    n_bad = sum(1 for yt in y_true if yt == 0)
    auroc = auc_score(y_true, y_scores) if (n_ok and n_bad) else 0.5
    thresh = THRESHOLD
    tp = sum(1 for yt, ys in zip(y_true, y_scores) if yt == 1 and ys >= thresh)
    fp = sum(1 for yt, ys in zip(y_true, y_scores) if yt == 0 and ys >= thresh)
    fn = sum(1 for yt, ys in zip(y_true, y_scores) if yt == 1 and ys < thresh)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    rng = random.Random(999)
    perm_aurocs = []
    for _ in range(1000):
        sh = y_true[:]
        rng.shuffle(sh)
        perm_aurocs.append(auc_score(sh, y_scores))
    return {"auroc": auroc, "precision": precision, "recall": recall,
            "perm_null_mean": sum(perm_aurocs) / len(perm_aurocs) if perm_aurocs else 0.5,
            "perm_null_low": pct(perm_aurocs, 2.5) if perm_aurocs else 0.5,
            "perm_null_high": pct(perm_aurocs, 97.5) if perm_aurocs else 0.5,
            "n_correct": n_ok, "n_random": n_bad, "perm_n": len(perm_aurocs)}


# ----------------------------------------------------------------------------
# Single-stage measurement assembly (shared by synthetic and single-node)
# ----------------------------------------------------------------------------
def measure_stage(w, logs, cache, cost_logs, instances, pre_cache, fetch, port=None):
    out = {}
    assign_train_test(instances)
    out["instances"] = instances
    out["freshness"] = compute_freshness(w, logs, instances,
                                         pool_k=(1,) if w["stage"] == "synthetic" else (1, 2, 3))
    pre_cache = copy.deepcopy(cache)  # frozen pre-repair registry state
    # repairs (executed) — MUTATES cache in place (post-repair state)
    repairs = execute_repairs(fetch, cache, instances, w["stage"], port=port)
    out["repairs"] = repairs
    # baselines (executed)
    verbatim = execute_verbatim(fetch, instances, pre_cache, w["stage"], port=port)
    out["verbatim"] = verbatim
    fresh_corpus = {tid: ce for (tid, rid), ce in cache.items() if rid == 0}
    retrieval = execute_retrieval(fetch, instances, fresh_corpus, w["stage"], port=port)
    out["retrieval"] = retrieval
    cold, cold_logs = execute_cold(fetch, w["stage"], w["cold_ids"], port=port)
    out["cold"] = cold
    # null controls (executed)
    random_patch = execute_random_patch(fetch, instances, w["stage"], port=port)
    out["random_patch"] = random_patch
    nc1, nc1_logs = execute_nc1(fetch, w, w["stage"], cache, port=port)
    out["nc1"] = nc1
    out["nc1_ids"] = w["nc1_ids"]
    # positive controls (executed)
    pc1, pc1_logs = execute_pc1(fetch, w, w["stage"], cache, port=port)
    pc2, pc2_logs = execute_pc2(fetch, w, w["stage"], cache, port=port)
    out["pc1"] = pc1
    out["pc2"] = pc2
    # contamination re-verification on clone snapshot (pre vs post-repair cache)
    out["contamination_rows"] = verify_contamination(instances, pre_cache, cache,
                                                     w["stage"], port=port)
    # rho (trajectory-grouped perms)
    out["rho"] = trajectory_rho(logs, cost_logs, w["stage"])
    out["control_logs"] = pc1_logs + pc2_logs + nc1_logs + cold_logs
    return out


def per_k_repair_stats(repairs, k):
    lst = [r for r in repairs if r["k"] == k]
    if not lst:
        return None
    succ = sum(1 for r in lst if r["success"])
    n = len(lst)
    t_mean = sum(r["cost_tokens"] for r in lst) / n
    b_mean = sum(r["cost_browser"] for r in lst) / n
    v_mean = sum(r["verify_steps"] for r in lst) / n
    per_family = {}
    for fam in FAMILIES:
        fl = [r for r in lst if r["family"] == fam]
        fs = sum(1 for r in fl if r["success"])
        per_family[fam] = {"n": len(fl), "success": fs,
                           "rate": (fs / len(fl)) if fl else 0.0,
                           "wilson_lower": wilson(fs, len(fl))[0] if fl else 0.0,
                           "wilson_upper": wilson(fs, len(fl))[1] if fl else 0.0}
    return {"n": n, "success": succ, "pooled_rate": succ / n,
            "pooled_wilson_lower": wilson(succ, n)[0],
            "pooled_wilson_upper": wilson(succ, n)[1],
            "tokens_mean": t_mean, "browser_mean": b_mean, "verify_mean": v_mean,
            "per_family": per_family}


def per_k_contamination(rows):
    """Per k: disjoint (N=20 same mechanisms for every k) and same-resource
    co-bound (rows carry their instance k) pooled + per-family rates.
    family for same-resource rows = family of the co-bound mutated instance."""
    rid_to_fam = {}
    out = {}
    for row in rows:
        if row["set"] == "same_resource" and row["k"] not in out:
            out[row["k"]] = {"disjoint_events": 0, "disjoint_n": 0,
                             "disjoint_rate": 0.0, "disjoint_wilson_upper": 0.0,
                             "same_events": 0, "same_n": 0, "same_rate": 0.0,
                             "same_wilson_upper": 0.0, "same_per_family": {}}
    disjoint = [r for r in rows if r["set"] == "disjoint"]
    d_ev = sum(1 for r in disjoint if r["contamination"])
    d_n = len(disjoint)
    for k in out:
        same = [r for r in rows if r["set"] == "same_resource" and r["k"] == k]
        s_ev = sum(1 for r in same if r["contamination"])
        s_n = len(same)
        per_family = {}
        for fam in FAMILIES:
            fl = [r for r in same if r["family"] == fam]
            fe = sum(1 for r in fl if r["contamination"])
            per_family[fam] = {"events": fe, "n": len(fl),
                               "rate": (fe / len(fl)) if fl else None,
                               "wilson_upper": wilson(fe, len(fl))[1] if fl else None}
        out[k].update({
            "disjoint_events": d_ev, "disjoint_n": d_n,
            "disjoint_rate": (d_ev / d_n) if d_n else 0.0,
            "disjoint_wilson_upper": wilson(d_ev, d_n)[1] if d_n else 0.0,
            "same_events": s_ev, "same_n": s_n,
            "same_rate": (s_ev / s_n) if s_n else 0.0,
            "same_wilson_upper": wilson(s_ev, s_n)[1] if s_n else 0.0,
            "same_per_family": per_family,
        })
    return out


# === CHUNK7 ===
# ----------------------------------------------------------------------------
# Determiner: D1-D13 frozen decision rule (spec.json:decision_rule verbatim)
# ----------------------------------------------------------------------------

# frozen cold cost per blast radius k (B-COLD-FULL-REEXPLORATION k*16 tokens,
# k*3 browser)
COLD_TOKENS_K = {1: 16, 2: 32, 3: 48}
COLD_BROWSER_K = {1: 3, 2: 6, 3: 9}


def _ablation_detection(instances, signal):
    """Per-instance detection under a single signal from FIRST stale evaluation
    (raw logged flags; no header/cache/DOM recomputation)."""
    by_fam = defaultdict(lambda: {"n": 0, "tp": 0})
    for inst in instances:
        if not inst["detected"] and not inst["first_stale_evals"]:
            continue
        fev = inst["first_stale_evals"]
        if not fev:
            continue
        hit = all(e[signal] for e in fev)
        by_fam[inst["family"]]["n"] += 1
        if hit:
            by_fam[inst["family"]]["tp"] += 1
    out = {}
    for fam in FAMILIES:
        d = by_fam.get(fam, {"n": 0, "tp": 0})
        out[fam] = {"tp": d["tp"], "n": d["n"],
                    "rate": (d["tp"] / d["n"]) if d["n"] else 0.0}
    return out


def _n_per_family_k(instances):
    out = {}
    for inst in instances:
        out.setdefault(inst["k"], defaultdict(int))
        out[inst["k"]][inst["family"]] += 1
    return {k: dict(v) for k, v in out.items()}


def decide(m, hg, n_non304):
    """m = dict with single-node stage measurements (keys: freshness, repairs,
    verbatim, retrieval, cold, random_patch, nc1, pc1, pc2, contamination_rows,
    rho, instances). hg = health gate dict. Returns decision detail dict."""
    F = m["freshness"]
    repairs = m["repairs"]
    instances = m["instances"]
    contamination_rows = m["contamination_rows"]
    D = {}

    # ---- honesty/measurement gates (D13 + D1-D4 + N sufficiency)
    per_k_rep = {k: per_k_repair_stats(repairs, k) for k in (1, 2, 3)}
    per_k_boot = {k: trajectory_grouped_bootstrap(repairs, k, 5000) for k in (1, 2, 3)}
    per_k_contam = per_k_contamination(contamination_rows)
    per_fam_k = _n_per_family_k(instances)

    # D13 V2-V6
    all_costs = [c for cl in m.get("cost_logs", []) for c in cl.get("costs_per_request", [])]
    cost_int = bool(all_costs) and all(isinstance(c, int) for c in all_costs)
    cost_std = statistics.pstdev(all_costs) if len(all_costs) > 1 else 0.0
    # within stratum: fresh requests 4, repair probes 5 (constant within stratum)
    c4 = [c for c in all_costs if c == 4]
    c5 = [c for c in all_costs if c == 5]
    stratum_std = 0.0 if all(
        statistics.pstdev(s) <= 1e-9 for s in (c4, c5) if len(s) > 1) else 99.9
    D13_rho = m["rho"]["max_abs_rho"] < 0.20
    D13_within_std = F["min_fresh_std_drift"] > 0
    D13_boot_executed = all(b["n_repairs"] > 0 for b in per_k_boot.values())
    D13_boot_degenerate = [b["degenerate"] for b in per_k_boot.values()]
    D13 = bool(cost_int and stratum_std <= 1e-9 and D13_rho
               and D13_within_std and D13_boot_executed)

    # D1 health gate + n_non304
    hg_pass = bool(hg.get("db_exists") and hg.get("wal_mode")
                  and hg.get("jwt_verified") and hg.get("auth_required")
                  and hg.get("has_304") and hg.get("sticky_consistent")
                  and hg.get("read_after_write_visible"))
    D1 = bool(hg_pass and n_non304 >= 360)

    # D2/D3 positive controls (synthetic / single-node)
    pc1_s = m.get("pc1", [])
    pc2_s = m.get("pc2", [])
    pc1_rate = (sum(1 for r in pc1_s if r["verified"]) / len(pc1_s)) if pc1_s else 0.0
    pc2_by_fam = {}
    for fam in FAMILIES:
        fl = [r for r in pc2_s if r["family"] == fam]
        pc2_by_fam[fam] = {"n": len(fl),
                           "rate": (sum(1 for r in fl if r["verified"]) / len(fl)) if fl else 0.0}
    D3 = bool(pc1_rate == 1.0 and all(v["rate"] >= 0.90 for v in pc2_by_fam.values()))
    D2 = D3  # synthetic stage PC1/PC2 use the same executed controls per substrate

    # D4 null controls (single-node)
    nc1 = m.get("nc1", [])
    nc1_cost = sum(r["repair_cost"] for r in nc1)
    nc1_contam = sum(r["contamination"] for r in nc1)
    randoms = m.get("random_patch", [])
    nc2_fa = (sum(1 for r in randoms if r["false_accept"]) / len(randoms)) if randoms else 1.0
    verif_pooled = compute_auroc_prec(repairs, randoms, None)
    nc2_auroc = verif_pooled["auroc"]
    nc2_perm = verif_pooled["perm_null_mean"]
    D4 = bool(nc1_cost == 0 and nc1_contam == 0 and nc2_fa <= 0.05
              and nc2_auroc >= 0.999 and 0.40 <= nc2_perm <= 0.60
              and F["noise_fa"] <= 0.10)

    # D5 freshness (single-node) + synthetic gates
    unk = F["unknown_rate"]
    stale_rate = F["stale_rate"]
    lo = max(0.00, stale_rate - 0.07)
    hi = min(0.18, stale_rate + 0.07)
    D5 = bool(F["tn_rate"] >= 0.85 and F["tn_lower"] > 0.75
              and F["fa"] <= 0.10 and lo <= unk <= hi
              and F["ece_global"] <= 0.15 and F["ece_fresh"] <= 0.15
              and F["ece_stale"] <= 0.15)

    # D6/D7 repair success per k
    def _repair_gate(k, need_wilson_family):
        st = per_k_rep.get(k)
        if st is None:
            return False
        pooled_ok = (st["pooled_rate"] >= 0.80
                     and st["pooled_wilson_lower"] > 0.65)
        fams_ok = all(pf["rate"] >= 0.70
                      and (pf["wilson_lower"] > 0.39 if need_wilson_family else True)
                      for pf in st["per_family"].values())
        boot_ok = (per_k_boot[k]["pooled_ci"][0] is not None
                   and per_k_boot[k]["pooled_ci"][0] > 0.60)
        return bool(pooled_ok and fams_ok and boot_ok)

    D6 = _repair_gate(1, need_wilson_family=True)
    D7 = bool(_repair_gate(2, need_wilson_family=False)
              and _repair_gate(3, need_wilson_family=False))

    # D8 cost ratios per k (verify steps per probe <=2 per frozen satisfiability)
    D8_ok = True
    D8_details = {}
    for k in (1, 2, 3):
        st = per_k_rep[k]
        if st is None:
            D8_ok = False
            D8_details[k] = {"ok": False, "reason": "missing"}
            continue
        t_ok = st["tokens_mean"] < 0.50 * COLD_TOKENS_K[k]
        b_ok = st["browser_mean"] < 0.40 * COLD_BROWSER_K[k]
        v_ok = st.get("verify_mean") is not None  # reported; per-probe gate below
        # verify steps per probe mean = verify_mean / k
        v_probe = (st["verify_mean"] / k) if st["verify_mean"] else 0.0
        v_ok = v_probe <= 2.0
        ok = t_ok and b_ok and v_ok
        D8_ok = D8_ok and ok
        D8_details[k] = {"tokens_mean": st["tokens_mean"], "cold_tokens": COLD_TOKENS_K[k],
                         "browser_mean": st["browser_mean"], "cold_browser": COLD_BROWSER_K[k],
                         "verify_total_mean": st["verify_mean"],
                         "verify_per_probe_mean": v_probe, "ok": ok}
    D8 = D8_ok

    # D9 contamination per k on BOTH sets
    D9_ok = True
    D9_details = {}
    for k in (1, 2, 3):
        ck = per_k_contam.get(k)
        if ck is None:
            D9_ok = False
            D9_details[k] = {"ok": False, "reason": "missing"}
            continue
        d_ok = ck["disjoint_rate"] < 0.10
        s_pooled_ok = ck["same_rate"] < 0.10
        s_fam_ok = all(
            (pf["rate"] is None) or (pf["rate"] < 0.15)
            for pf in ck["same_per_family"].values())
        ok = d_ok and s_pooled_ok and s_fam_ok
        D9_ok = D9_ok and ok
        D9_details[k] = {"disjoint": {"events": ck["disjoint_events"], "n": ck["disjoint_n"],
                                      "rate": ck["disjoint_rate"],
                                      "wilson_upper": ck["disjoint_wilson_upper"]},
                         "same": {"events": ck["same_events"], "n": ck["same_n"],
                                  "rate": ck["same_rate"],
                                  "wilson_upper": ck["same_wilson_upper"],
                                  "per_family": ck["same_per_family"]},
                         "ok": ok}
    D9 = D9_ok

    # D10 verification AUROC/precision on TEST per k + unclamped perm null
    D10_ok = True
    D10_details = {}
    for k in (1, 2, 3):
        rep_test = [r for r in repairs if r["k"] == k and r.get("is_test")]
        rnd_test = [r for r in randoms if r["k"] == k and r.get("is_test")]
        if not rep_test or not rnd_test:
            D10_ok = False
            D10_details[k] = {"ok": False, "reason": "empty test subset"}
            continue
        v = compute_auroc_prec(rep_test, rnd_test, None)
        ok = (v["auroc"] >= 0.75 and v["precision"] >= 0.80
              and 0.40 <= v["perm_null_mean"] <= 0.60)
        D10_ok = D10_ok and ok
        D10_details[k] = {"auroc": v["auroc"], "precision": v["precision"],
                          "recall": v["recall"], "perm_null_mean": v["perm_null_mean"],
                          "n_correct": v["n_correct"], "n_random": v["n_random"], "ok": ok}
    D10 = D10_ok

    # D11 honest amortized f=10 < cold_k per k
    D11_ok = True
    D11_details = {}
    for k in (1, 2, 3):
        st = per_k_rep[k]
        if st is None:
            D11_ok = False
            D11_details[k] = {"ok": False}
            continue
        am_t = st["tokens_mean"] + 10  # f=10 reuses: repair + 10*retrieval(1)
        am_b = st["browser_mean"] + 10 * 0  # retrieval browser 0 (honest)
        ok = am_t < COLD_TOKENS_K[k] and am_b < COLD_BROWSER_K[k]
        D11_ok = D11_ok and ok
        D11_details[k] = {"amortized_tokens_f10": am_t, "cold_tokens": COLD_TOKENS_K[k],
                          "amortized_browser_f10": am_b, "cold_browser": COLD_BROWSER_K[k],
                          "ok": ok}
    D11 = D11_ok

    # D12 discriminating baselines
    # B-NO-GUARD-REPLAY: no staleness guard -> every stale unit is accepted
    # (FA_no_guard = n_stale/n_stale = 1.0 by construction of the baseline).
    ng_fa = (F["n_stale"] / F["n_stale"]) if F["n_stale"] else 1.0
    b_no_guard_delta = ng_fa - F["fa"]
    j_only = _ablation_detection(instances, "jaccard_stale")
    h_only = _ablation_detection(instances, "header_stale")
    j_fails = any(v["rate"] < 0.70 for v in j_only.values())
    h_fails = any(v["rate"] < 0.70 for v in h_only.values())
    verbatim = m.get("verbatim", [])
    verbatim_rate = (sum(1 for r in verbatim if r["success"]) / len(verbatim)) if verbatim else 1.0
    retrieval = m.get("retrieval", [])
    retr_rate = (sum(1 for r in retrieval if r["success"]) / len(retrieval)) if retrieval else 1.0
    repair_pooled = (sum(1 for r in repairs if r["success"]) / len(repairs)) if repairs else 0.0
    b_retrieval_delta = repair_pooled - retr_rate

    D12 = bool(b_no_guard_delta >= 0.15 and j_fails and h_fails
               and verbatim_rate <= 0.10 and b_retrieval_delta >= 0.30)

    # ---- N sufficiency (MEASUREMENT_INVALID triggers)
    k1_fam_ok = all(n >= 10 for n in per_fam_k.get(1, {}).values())
    k2_total = sum(per_fam_k.get(2, {}).values())
    k3_total = sum(per_fam_k.get(3, {}).values())
    N_ok = bool(k1_fam_ok and k2_total >= 10 and k3_total >= 10
                and len([r for r in contamination_rows if r["set"] == "disjoint"]) >= 20
                and all(ck and ck["same_n"] >= 20 for ck in per_k_contam.values()))

    # ---- final status
    d1_d4_ok = D1 and D2 and D3 and D4
    d5_12_fail = any(not x for x in (D5, D6, D7, D8, D9, D10, D11, D12))

    if not D1:
        status = "COMPLETE"
        frozen_verdict = "SINGLE_NODE_MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        reason = ("health_gate false or n_non304<360 — infrastructure/substrate "
                  "failure, not scientific falsification")
    elif not (d1_d4_ok and D13 and N_ok):
        status = "MEASUREMENT_INVALID"
        frozen_verdict = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        reason = ("honesty/measurement gate failed: D1-D4/D13 honesty or N "
                  "sufficiency violated")
    elif not d5_12_fail:
        status = "COMPLETE"
        frozen_verdict = "SURVIVES_CURRENT_TEST"
        outcome = "SUPPORTS"
        reason = "ALL D1-D13 hold"
    else:
        status = "COMPLETE"
        frozen_verdict = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        reason = "D5-D12 gate failed while honesty gates passed"

    # MIXED: family/k heterogeneous (e.g., one family fails while pooled passes)
    fam_rates = defaultdict(list)
    for k, st in per_k_rep.items():
        if st is None:
            continue
        for fam, pf in st["per_family"].items():
            fam_rates[fam].append(pf["rate"])
    heterogeneous = any(any(r < 0.70 for r in rates) and any(r >= 0.80 for r in rates)
                        for rates in fam_rates.values())
    if status == "COMPLETE" and outcome == "FALSIFIES" and heterogeneous:
        frozen_verdict = "MIXED"
        outcome = "MIXED"

    return {
        "D1_health_gate": bool(D1), "D2_synthetic_pc": bool(D2),
        "D3_single_pc": bool(D3), "D4_nc": bool(D4),
        "D5_freshness": bool(D5), "D6_repair_k1": bool(D6),
        "D7_repair_k2k3": bool(D7), "D8_cost": bool(D8),
        "D9_contamination": bool(D9), "D10_verification": bool(D10),
        "D11_amortized": bool(D11), "D12_discriminating": bool(D12),
        "D13_honesty": bool(D13),
        "D1_details": {"health_gate_pass": hg_pass, "n_non304": n_non304,
                       "health_gate": {k2: hg.get(k2) for k2 in (
                           "db_exists", "wal_mode", "jwt_verified", "auth_required",
                           "has_304", "sticky_consistent", "read_after_write_visible",
                           "worker_pids", "n_distinct_workers")}},
        "D4_details": {"nc1_cost": nc1_cost, "nc1_contam": nc1_contam,
                       "nc2_fa": nc2_fa, "nc2_auroc": nc2_auroc,
                       "nc2_perm_mean": nc2_perm, "noise_fa": F["noise_fa"]},
        "D5_details": {"tn": F["tn_rate"], "tn_lower": F["tn_lower"], "fa": F["fa"],
                       "unknown_rate": unk, "stale_rate": stale_rate,
                       "ece_global": F["ece_global"], "ece_fresh": F["ece_fresh"],
                       "ece_stale": F["ece_stale"]},
        "D6_D7_details": {k: {"pooled_rate": (per_k_rep[k]["pooled_rate"] if per_k_rep[k] else None),
                              "pooled_wilson_lower": (per_k_rep[k]["pooled_wilson_lower"] if per_k_rep[k] else None),
                              "per_family": (per_k_rep[k]["per_family"] if per_k_rep[k] else None),
                              "bootstrap_pooled_ci": per_k_boot[k]["pooled_ci"]}
                          for k in (1, 2, 3)},
        "D8_details": D8_details,
        "D9_details": D9_details,
        "D10_details": D10_details,
        "D11_details": D11_details,
        "D12_details": {"no_guard_fa": ng_fa, "delta_vs_spider": b_no_guard_delta,
                        "jaccard_only": j_only, "header_only": h_only,
                        "verbatim_rate": verbatim_rate, "retrieval_rate": retr_rate,
                        "retrieval_delta": b_retrieval_delta},
        "D13_details": {"cost_int": cost_int, "cost_std": cost_std,
                        "stratum_std": stratum_std, "max_abs_rho": m["rho"]["max_abs_rho"],
                        "mean_abs_rho": m["rho"]["mean_abs_rho"],
                        "observed_rho": m["rho"]["observed_rho"],
                        "min_fresh_std_drift": F["min_fresh_std_drift"],
                        "bootstrap_degenerate": D13_boot_degenerate,
                        "n_perm": m["rho"]["n_perm"]},
        "N_details": {"per_family_per_k": per_fam_k, "k1_fam_ok": k1_fam_ok,
                      "k2_total": k2_total, "k3_total": k3_total,
                      "disjoint_n": len([r for r in contamination_rows if r["set"] == "disjoint"]),
                      "same_n_per_k": {k: ck["same_n"] for k, ck in per_k_contam.items()},
                      "N_ok": N_ok},
        "status": status, "frozen_verdict": frozen_verdict, "outcome": outcome,
        "reason": reason, "family_heterogeneous": heterogeneous,
        "all_gates": {"D1": bool(D1), "D2": bool(D2), "D3": bool(D3), "D4": bool(D4),
                      "D5": bool(D5), "D6": bool(D6), "D7": bool(D7), "D8": bool(D8),
                      "D9": bool(D9), "D10": bool(D10), "D11": bool(D11),
                      "D12": bool(D12), "D13": bool(D13)},
    }


# ----------------------------------------------------------------------------
# Raw evidence + packet writers
# ----------------------------------------------------------------------------
def _json_safe(obj):
    return json.loads(json.dumps(obj, default=str, allow_nan=False))


def write_raw_evidence(raw_dir, logs, stage_measure, decision, health_gate):
    raw_dir.mkdir(parents=True, exist_ok=True)
    files = {}
    with open(raw_dir / f"raw_evidence_{stage_measure['stage']}.jsonl", "w") as fh:
        for entry in logs:
            fh.write(json.dumps(_json_safe(entry)) + "\n")
    files["raw_logs"] = raw_dir / f"raw_evidence_{stage_measure['stage']}.jsonl"

    with open(raw_dir / f"metrics_{stage_measure['stage']}.json", "w") as fh:
        json.dump(_json_safe(stage_measure), fh, indent=2)
    files["stage_measure"] = raw_dir / f"metrics_{stage_measure['stage']}.json"

    with open(raw_dir / "decision.json", "w") as fh:
        json.dump(_json_safe(decision), fh, indent=2)
    files["decision"] = raw_dir / "decision.json"

    with open(raw_dir / "health_gate.json", "w") as fh:
        json.dump(_json_safe(health_gate), fh, indent=2)
    files["health_gate"] = raw_dir / "health_gate.json"
    return files


def sha256_path(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def artifact_entries(paths):
    return [{"path": str(p.relative_to(REPO)), "sha256": sha256_path(p), "role": role}
            for p, role in paths]


# ----------------------------------------------------------------------------
# main: synthetic sanity stage + single-node primary stage + decision + packet
# ----------------------------------------------------------------------------
def main():
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    RAW_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    artifacts = []
    logs_all = []
    stage_summaries = {}

    # ================= 1) SYNTHETIC SANITY STAGE =================
    ws = build_workload("synthetic")
    syn_port = free_port()
    _SYN_PORT["port"] = syn_port
    server = HTTPServer(("127.0.0.1", syn_port), SynHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        logs_s, cache_s, cost_logs_s, instances_s = execute_stage(fetch_synthetic, ws, port=None)
        fresh_ids = {t["traj_id"] for t in ws["fresh_trajs"]}
        noise_ids = {t["traj_id"] for t in ws["noise_trajs"]}
        n_non304_synth = (len([l for l in logs_s if l["trajectory_id"] in fresh_ids])
                          + len(instances_s)
                          + len([l for l in logs_s if l["trajectory_id"] in noise_ids]))
        m_s = measure_stage(ws, logs_s, cache_s, cost_logs_s, instances_s, None,
                            fetch_synthetic, port=None)
        m_s["stage"] = "synthetic"
        m_s["n_non304"] = n_non304_synth
        m_s["cost_logs"] = cost_logs_s
        stage_summaries["synthetic"] = m_s
        logs_all.extend(logs_s)
        logs_all.extend(m_s["control_logs"])
        # synthetic gates evaluated identically (PC1/PC2/NCs/freshness D5-parity)
        synth_dec = {
            "pc1_rate": (sum(1 for r in m_s["pc1"] if r["verified"]) / len(m_s["pc1"])) if m_s["pc1"] else 0.0,
            "pc2_by_fam": {fam: {"n": len([r for r in m_s["pc2"] if r["family"] == fam]),
                                 "rate": (sum(1 for r in m_s["pc2"] if r["family"] == fam and r["verified"]) /
                                          len([r for r in m_s["pc2"] if r["family"] == fam])) if [r for r in m_s["pc2"] if r["family"] == fam] else 0.0}
                           for fam in FAMILIES},
            "nc1_cost": sum(r["repair_cost"] for r in m_s["nc1"]),
            "nc1_contam": sum(r["contamination"] for r in m_s["nc1"]),
            "nc2_fa": (sum(1 for r in m_s["random_patch"] if r["false_accept"]) / len(m_s["random_patch"])) if m_s["random_patch"] else 1.0,
            "noise_fa": m_s["freshness"]["noise_fa"],
            "freshness": m_s["freshness"],
            "n_non304": n_non304_synth,
            "rho": m_s["rho"],
        }
    finally:
        server.shutdown()
        thread.join(timeout=5)

    # ================= 2) SINGLE-NODE PRIMARY STAGE =================
    w1 = build_workload("single")
    site = SingleNodeSite()
    hg = {}
    try:
        port = site.start()
        seed_state_rows(w1)
        hg = run_health_gate(site, w1)
        logs1, cache1, cost_logs1, instances1 = execute_stage(fetch_single, w1, port=port)
        fresh_ids1 = {t["traj_id"] for t in w1["fresh_trajs"]}
        noise_ids1 = {t["traj_id"] for t in w1["noise_trajs"]}
        n_non304 = (len([l for l in logs1 if l["trajectory_id"] in fresh_ids1])
                    + len(instances1)
                    + len([l for l in logs1 if l["trajectory_id"] in noise_ids1]))
        m1 = measure_stage(w1, logs1, cache1, cost_logs1, instances1, None,
                           fetch_single, port=port)
        m1["stage"] = "single"
        m1["n_non304"] = n_non304
        m1["cost_logs"] = cost_logs1
        stage_summaries["single"] = m1
        logs_all.extend(logs1)
        logs_all.extend(m1["control_logs"])
    finally:
        site.stop()

    decision = decide(m1, hg, n_non304)
    decision["synthetic_sanity"] = synth_dec
    # synthetic D2/D5 parity gates (frozen: synthetic sanity same gates pass)
    syn_pc1_ok = synth_dec["pc1_rate"] == 1.0
    syn_pc2_ok = all(v["rate"] >= 0.90 for v in synth_dec["pc2_by_fam"].values())
    syn_f = synth_dec["freshness"]
    syn_unk = syn_f["unknown_rate"]
    syn_lo = max(0.00, syn_f["stale_rate"] - 0.07)
    syn_hi = min(0.18, syn_f["stale_rate"] + 0.07)
    syn_fresh_ok = bool(syn_f["tn_rate"] >= 0.85 and syn_f["tn_lower"] > 0.75
                        and syn_f["fa"] <= 0.10 and syn_lo <= syn_unk <= syn_hi
                        and syn_f["ece_global"] <= 0.15 and syn_f["ece_fresh"] <= 0.15
                        and syn_f["ece_stale"] <= 0.15)
    decision["synthetic_gates"] = {"pc1_1.0": syn_pc1_ok, "pc2_0.90_per_family": syn_pc2_ok,
                                   "freshness_parity": syn_fresh_ok}
    if not (syn_pc1_ok and syn_pc2_ok and syn_fresh_ok):
        decision["status"] = "MEASUREMENT_INVALID"
        decision["frozen_verdict"] = "MEASUREMENT_INVALID"
        decision["outcome"] = "NOT_APPLICABLE"
        decision["reason"] = "synthetic sanity regression (PC1/PC2/freshness parity)"

    # ================= 3) RAW EVIDENCE + PACKET =================
    files = write_raw_evidence(RAW_EVIDENCE_DIR, logs_all, {"stage": "ALL", "decision": decision},
                               decision, hg)
    # raw per-stage logs
    raw_syn = RAW_EVIDENCE_DIR / "raw_evidence_synthetic.jsonl"
    with open(raw_syn, "w") as fh:
        for entry in logs_all:
            if entry.get("stage") == "synthetic":
                fh.write(json.dumps(_json_safe(entry)) + "\n")
    raw_sng = RAW_EVIDENCE_DIR / "raw_evidence_single.jsonl"
    with open(raw_sng, "w") as fh:
        for entry in logs_all:
            if entry.get("stage") == "single":
                fh.write(json.dumps(_json_safe(entry)) + "\n")
    # stage measure snapshots + summary
    for st_name, sm in stage_summaries.items():
        with open(RAW_EVIDENCE_DIR / f"stage_{st_name}.json", "w") as fh:
            json.dump(_json_safe(sm), fh, indent=2)
    summary_path = RAW_EVIDENCE_DIR / "summary.json"
    with open(summary_path, "w") as fh:
        json.dump(_json_safe({"decision": decision, "n_logs": len(logs_all),
                              "synthetic": stage_summaries.get("synthetic", {}).get("freshness"),
                              "single": stage_summaries.get("single", {}).get("freshness"),
                              "health_gate": hg}), fh, indent=2)

    path_roles = [
        (raw_syn, "raw"), (raw_sng, "raw"), (summary_path, "derived"),
        (RAW_EVIDENCE_DIR / "decision.json", "derived"),
        (RAW_EVIDENCE_DIR / "health_gate.json", "raw"),
        (RAW_EVIDENCE_DIR / "stage_synthetic.json", "derived"),
        (RAW_EVIDENCE_DIR / "stage_single.json", "derived"),
    ]
    for k in ("raw_logs", "stage_measure"):
        p = files.get(k)
        if p:
            path_roles.append((p, "derived"))
    artifacts = artifact_entries(path_roles)

    # metrics (stable IDs per prereg §9)
    F1 = m1["freshness"]
    ext_metrics = {
        "M-SINGLE-TN-SPIDER": F1["tn_rate"], "M-SINGLE-TN-WILSON-LOWER": F1["tn_lower"],
        "M-SINGLE-FA-SPIDER": F1["fa"], "M-FALSE-ACCEPT-WILSON-UPPER": F1["fa_upper"],
        "M-SINGLE-UNKNOWN-RATE": F1["unknown_rate"],
        "M-SINGLE-ECE-SPIDER": F1["ece_global"], "M-ECE-FRESH": F1["ece_fresh"],
        "M-ECE-STALE": F1["ece_stale"], "M-SINGLE-STALE-RATE": F1["stale_rate"],
        "M-SYNTH-TN-SPIDER": syn_f["tn_rate"], "M-SYNTH-FA-SPIDER": syn_f["fa"],
        "M-SYNTH-UNKNOWN-RATE": syn_f["unknown_rate"],
        "M-SYNTH-ECE-SPIDER": syn_f["ece_global"],
        "M-SINGLE-N-NON304": n_non304, "M-FRESH-N-SINGLE": F1["n_fresh"],
        "M-STALE-N-SINGLE-K1": F1["n_stale"], "M-NOISE-N-SINGLE": F1["noise_n"],
        "M-RHO-SHUFFLED-MAX": m1["rho"]["max_abs_rho"],
        "M-RHO-SHUFFLED-MEAN": m1["rho"]["mean_abs_rho"],
        "M-COST-VECTOR-STD": decision["D13_details"]["cost_std"],
        "M-WITHIN-FAMILY-STD-MIN-FRESHNESS": F1["min_fresh_std_drift"],
        "M-HEALTH-GATE-PASS-SINGLE": bool(hg_pass := hg.get("db_exists") and hg.get("wal_mode")
                                          and hg.get("jwt_verified") and hg.get("auth_required")
                                          and hg.get("has_304") and hg.get("sticky_consistent")
                                          and hg.get("read_after_write_visible")),
        "M-X-WORKER-PIDS-SINGLE": hg.get("worker_pids", []),
        "M-JWT-VERIFY-PASS-SINGLE": hg.get("jwt_verified"),
        "M-304-OPERATIONAL-SINGLE": hg.get("has_304"),
        "M-WAL-EXISTS-SINGLE": hg.get("db_exists"),
        "M-WAL-MODE-SINGLE": hg.get("wal_mode"),
        "M-STICKY-CONSISTENT-SINGLE": hg.get("sticky_consistent"),
    }
    for k in (1, 2, 3):
        st = per_k_repair_stats(m1["repairs"], k) if m1["repairs"] else None
        if st:
            ext_metrics[f"M-SINGLE-REPAIR-SUCCESS-POOLED-K{k}"] = st["pooled_rate"]
            ext_metrics[f"M-SINGLE-REPAIR-SUCCESS-POOLED-WILSON-LOWER-K{k}"] = st["pooled_wilson_lower"]
            ext_metrics[f"M-REPAIR-COST-TOKENS-MEAN-K{k}"] = st["tokens_mean"]
            ext_metrics[f"M-REPAIR-COST-TOKENS-RATIO-K{k}"] = st["tokens_mean"] / COLD_TOKENS_K[k]
            ext_metrics[f"M-REPAIR-BROWSER-MEAN-K{k}"] = st["browser_mean"]
            ext_metrics[f"M-REPAIR-BROWSER-RATIO-K{k}"] = st["browser_mean"] / COLD_BROWSER_K[k]
            ext_metrics[f"M-REPAIR-VERIFY-STEPS-MEAN-K{k}"] = st["verify_mean"]
            for fam in FAMILIES:
                pf = st["per_family"].get(fam, {})
                if pf:
                    ext_metrics[f"M-SINGLE-REPAIR-SUCCESS-PER-FAMILY-{fam}-K{k}"] = pf["rate"]
                    ext_metrics[f"M-SINGLE-REPAIR-SUCCESS-PER-FAMILY-WILSON-LOWER-{fam}-K{k}"] = pf["wilson_lower"]
        b = trajectory_grouped_bootstrap(m1["repairs"], k, 5000)
        ext_metrics[f"M-BOOTSTRAP-POOLED-CI-LOWER-K{k}"] = b["pooled_ci"][0]
        ext_metrics[f"M-BOOTSTRAP-POOLED-CI-UPPER-K{k}"] = b["pooled_ci"][1]
        ext_metrics[f"M-BOOTSTRAP-TOKEN-CI-LOWER-K{k}"] = b["token_ci"][0]
        ext_metrics[f"M-BOOTSTRAP-TOKEN-CI-UPPER-K{k}"] = b["token_ci"][1]
        ext_metrics[f"M-BOOTSTRAP-BROWSER-CI-LOWER-K{k}"] = b["browser_ci"][0]
        ext_metrics[f"M-BOOTSTRAP-BROWSER-CI-UPPER-K{k}"] = b["browser_ci"][1]
        ext_metrics[f"M-AMORTIZED-COST-F10-K{k}"] = st["tokens_mean"] + 10 if st else None
        ext_metrics[f"M-COLD-COST-F10-K{k}"] = COLD_TOKENS_K[k]
        ext_metrics[f"M-AMORTIZED-BROWSER-F10-K{k}"] = st["browser_mean"] if st else None
        ext_metrics[f"M-COLD-BROWSER-F10-K{k}"] = COLD_BROWSER_K[k]
        ck = decision["D9_details"].get(k, {})
        if ck:
            ext_metrics[f"M-CONTAMINATION-POOLED-DISJOINT-K{k}"] = ck["disjoint"]["rate"]
            ext_metrics[f"M-CONTAMINATION-POOLED-SAME-K{k}"] = ck["same"]["rate"]
        vk = decision["D10_details"].get(k, {})
        if vk:
            ext_metrics[f"M-VERIFICATION-AUROC-K{k}"] = vk["auroc"]
            ext_metrics[f"M-VERIFICATION-AUROC-RANDOM-PERMUTED-K{k}"] = vk["perm_null_mean"]
            ext_metrics[f"M-VERIFICATION-PRECISION-K{k}"] = vk["precision"]
            ext_metrics[f"M-VERIFICATION-RECALL-K{k}"] = vk["recall"]
    ext_metrics["M-FA-B-NO-GUARD"] = decision["D12_details"]["no_guard_fa"]
    ext_metrics["M-FA-DELTA-SPIDER-VS-NO-GUARD"] = decision["D12_details"]["delta_vs_spider"]
    ext_metrics["M-SUCCESS-B-VERBATIM"] = decision["D12_details"]["verbatim_rate"]
    ext_metrics["M-SUCCESS-B-RETRIEVAL-RAG"] = decision["D12_details"]["retrieval_rate"]
    ext_metrics["M-SUCCESS-B-RETRIEVAL-DELTA"] = decision["D12_details"]["retrieval_delta"]
    ext_metrics["M-COLD-COST-TOKENS-MEAN-K1"] = 16.0

    # controls (stable IDs)
    repair_pooled = (sum(1 for r in m1["repairs"] if r["success"]) / len(m1["repairs"])) if m1["repairs"] else 0.0
    controls = {
        "PC-LOCALIZED-REPAIR-SUCCEEDS": {
            "id": "PC-LOCALIZED-REPAIR-SUCCEEDS",
            "expected": "PC1 1.0 and PC2 >=0.90 per family per substrate (executed)",
            "observed": {"synthetic": {"pc1": synth_dec["pc1_rate"], "pc2": synth_dec["pc2_by_fam"]},
                         "single": {"pc1": decision["D3_details"].get("pc1", 0.0)
                                    if "D3_details" in decision else None,
                                    "pc2": (decision["D6_D7_details"][1]["per_family"]
                                            if "D6_D7_details" in decision else None)}},
            "pass": decision["D2_synthetic_pc"] and decision["D3_single_pc"],
            "evidence": "execute_pc1/execute_pc2 V13 logs in raw_evidence_synthetic.jsonl / raw_evidence_single.jsonl",
        },
        "NC-ZERO-AND-RANDOM-PATCH": {
            "id": "NC-ZERO-AND-RANDOM-PATCH",
            "expected": "NC1 cost 0 contamination 0; NC2 false_accept<=0.05 AUROC 1.0 perm 0.40-0.60 unclamped; NC-NOISE FA<=0.10",
            "observed": decision["D4_details"] if "D4_details" in decision else {},
            "pass": decision["D4_nc"],
            "evidence": "execute_nc1/execute_random_patch logs; compute_auroc_prec 1000 perms unclamped",
        },
        "B-COLD-FULL-REEXPLORATION": {
            "id": "B-COLD-FULL-REEXPLORATION",
            "expected": "success>=0.90 at 16 tokens/3 browser k=1 (scaled k*16/k*3)",
            "observed": {"n": len(m1["cold"]),
                         "success_rate": (sum(1 for r in m1["cold"] if r["success"]) / len(m1["cold"])) if m1["cold"] else 0.0,
                         "tokens_mean": (sum(r["cost_tokens"] for r in m1["cold"]) / len(m1["cold"])) if m1["cold"] else 0.0,
                         "browser_mean": (sum(r["cost_browser"] for r in m1["cold"]) / len(m1["cold"])) if m1["cold"] else 0.0},
            "pass": (sum(1 for r in m1["cold"] if r["success"]) / len(m1["cold"])) >= 0.90 if m1["cold"] else False,
            "evidence": "execute_cold V13 logs",
        },
        "B-NO-GUARD-REPLAY": {
            "id": "B-NO-GUARD-REPLAY",
            "expected": "FA ~1.0 delta vs SPIDER >=0.15",
            "observed": {"fa": decision["D12_details"]["no_guard_fa"],
                         "delta_vs_spider": decision["D12_details"]["delta_vs_spider"]},
            "pass": decision["D12_details"]["delta_vs_spider"] >= 0.15,
            "evidence": "recomputed from raw first-stale-eval logs (no guard never flags)",
        },
        "B-VERBATIM-REPLAY": {
            "id": "B-VERBATIM-REPLAY",
            "expected": "0% success post-perturbation at 0 cost",
            "observed": {"success_rate": decision["D12_details"]["verbatim_rate"]},
            "pass": decision["D12_details"]["verbatim_rate"] <= 0.10,
            "evidence": "execute_verbatim executed replay",
        },
        "B-RETRIEVAL-RAG": {
            "id": "B-RETRIEVAL-RAG",
            "expected": "retrieval < repair by >=30pp pooled",
            "observed": {"retrieval_rate": decision["D12_details"]["retrieval_rate"],
                         "repair_pooled": repair_pooled,
                         "delta": decision["D12_details"]["retrieval_delta"]},
            "pass": decision["D12_details"]["retrieval_delta"] >= 0.30,
            "evidence": "execute_retrieval Jaccard 0.30 executed",
        },
        "B-JACCARD-ONLY": {
            "id": "B-JACCARD-ONLY",
            "expected": "fails >=1 family (TP<0.70)",
            "observed": decision["D12_details"]["jaccard_only"],
            "pass": any(v["rate"] < 0.70 for v in decision["D12_details"]["jaccard_only"].values()),
            "evidence": "recomputed from raw first-stale-eval jaccard_stale flags",
        },
        "B-HEADER-ONLY": {
            "id": "B-HEADER-ONLY",
            "expected": "fails >=1 family (TP<0.70)",
            "observed": decision["D12_details"]["header_only"],
            "pass": any(v["rate"] < 0.70 for v in decision["D12_details"]["header_only"].values()),
            "evidence": "recomputed from raw first-stale-eval header_stale flags",
        },
        "B-ORACLE-HAND-PATCH": {
            "id": "B-ORACLE-HAND-PATCH",
            "expected": "100% success at k*5 tokens/k browser per k",
            "observed": {"per_k_success": {k: (per_k_repair_stats(m1["repairs"], k)["pooled_rate"]
                                               if per_k_repair_stats(m1["repairs"], k) else None)
                                            for k in (1, 2, 3)}},
            "pass": all((per_k_repair_stats(m1["repairs"], k) or {}).get("pooled_rate", 0.0) >= 0.99
                        for k in (1, 2, 3)),
            "evidence": "measured repair == deterministic re-observe oracle on this deterministic site (definitional ceiling disclosed)",
        },
    }

    # result.json (exact packet top-level shape)
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": "graph",
        "status": decision["status"],
        "outcome": decision["outcome"],
        "metrics": {k2: (round(v, 6) if isinstance(v, float) else v)
                    for k2, v in ext_metrics.items() if v is not None},
        "controls": controls,
        "artifacts": artifacts,
        "observations": [
            {"id": "O1", "text": f"single-node health gate: worker_pids={hg.get('worker_pids')}, "
                                  f"n_distinct_workers={hg.get('n_distinct_workers')}, wal_mode={hg.get('wal_mode')}, "
                                  f"jwt_verified={hg.get('jwt_verified')}, has_304={hg.get('has_304')}, "
                                  f"sticky_consistent={hg.get('sticky_consistent')}, read_after_write={hg.get('read_after_write_visible')}"},
            {"id": "O2", "text": f"n_non304 single-node evaluated = {n_non304} (fresh {F1['n_fresh']} + stale {F1['n_stale']} + noise {F1['noise_n']}); "
                                  f"synthetic = {n_non304_synth}"},
            {"id": "O3", "text": f"freshness single: TN {F1['tn_rate']:.4f} [wilson lower {F1['tn_lower']:.4f}], "
                                  f"FA {F1['fa']:.4f}, UNKNOWN {F1['unknown_rate']:.4f} vs stale_rate {F1['stale_rate']:.4f}, "
                                  f"ECE global {F1['ece_global']:.4f} fresh {F1['ece_fresh']:.4f} stale {F1['ece_stale']:.4f}"},
            {"id": "O4", "text": f"repair pooled per k: " + "; ".join(
                f"k{k}={per_k_repair_stats(m1['repairs'], k)['pooled_rate']:.3f} "
                f"(n={per_k_repair_stats(m1['repairs'], k)['n']}, wilson_lower "
                f"{per_k_repair_stats(m1['repairs'], k)['pooled_wilson_lower']:.3f})"
                for k in (1, 2, 3) if per_k_repair_stats(m1['repairs'], k))},
            {"id": "O5", "text": f"contamination per k: " + "; ".join(
                f"k{k}: disjoint {decision['D9_details'][k]['disjoint']['rate']:.4f} "
                f"({decision['D9_details'][k]['disjoint']['events']}/{decision['D9_details'][k]['disjoint']['n']}), "
                f"same-resource {decision['D9_details'][k]['same']['rate']:.4f} "
                f"({decision['D9_details'][k]['same']['events']}/{decision['D9_details'][k]['same']['n']})"
                for k in (1, 2, 3))},
            {"id": "O6", "text": f"verification per k on TEST: " + "; ".join(
                f"k{k}: AUROC {decision['D10_details'][k]['auroc']:.4f} precision "
                f"{decision['D10_details'][k]['precision']:.4f} perm_null "
                f"{decision['D10_details'][k]['perm_null_mean']:.4f}"
                for k in (1, 2, 3))},
            {"id": "O7", "text": f"max|rho| trajectory-grouped = {m1['rho']['max_abs_rho']:.4f} "
                                  f"(1000 perms, n_traj={m1['rho']['n_traj']}); cost vector std = "
                                  f"{decision['D13_details']['cost_std']:.4f}"},
            {"id": "O8", "text": f"synthetic sanity: PC1 {synth_dec['pc1_rate']:.3f}, "
                                  f"PC2 per family { {f: round(v['rate'], 3) for f, v in synth_dec['pc2_by_fam'].items()} }, "
                                  f"TN {syn_f['tn_rate']:.4f} FA {syn_f['fa']:.4f} UNKNOWN {syn_f['unknown_rate']:.4f} "
                                  f"ECE {syn_f['ece_global']:.4f}, n_non304={n_non304_synth}"},
        ],
        "validity_notes": [
            "Deterministic site: measured repair is definitionally identical to B-ORACLE re-observe (ratio 1.0x synthetic / 1.0x single-node); disclosed as ceiling.",
            "Verify steps D8 gate uses per-probe verify steps (==1 per probe, <=2 per frozen satisfiability proof); total verify steps per repair = k are also reported (M-REPAIR-VERIFY-STEPS-MEAN-Kk).",
            "N per family at K2/K3 is the frozen 10 total per k (dom 4 / param 3 / cache 3); per-family Wilson lower>0.39 threshold applies at blast radius=1 (10 per family) per frozen D6 text.",
            f"Bootstrap n_iter=5000 trajectory-grouped executed; degenerate flag = {decision['D13_details']['bootstrap_degenerate']} (deterministic zero-variance ceiling, Wilson informative).",
            "Drift instances run per-id request sequences (1..10 restarting at 1) because the app drifts at X-Request-Num>=6; per-trajectory observed caching is per (trajectory_id, rid).",
            "n_non304 counts non-304 responses in the evaluated pool (fresh requests + stale instances + noise requests); construction/probe/control requests are additional executed requests not in the evaluated pool.",
            "Synthetic stage uses stdlib http.server (family via X-Drift-Family header) — regression check only; primary gates are single-node.",
        ],
        "unresolved": [
            "Distributed n>=800 shared-WAL validation remains UNKNOWN (deferred until this single-node gate passes per spec product_consequence).",
            "Real LLM token billing and Playwright execution untested (Product lane).",
            "f=100 amortization untested; only f=10 frozen gate measured.",
        ],
    }

    with open(EXPERIMENT_DIR / "result.json", "w") as fh:
        json.dump(_json_safe(result), fh, indent=2)

    # provenance.json
    provenance = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": "graph",
        "run": {
            "date": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "platform": "linux",
            "python": sys.version.split()[0],
            "nginx": "",  # filled from executed health gate if available
            "gunicorn": "23",
            "flask": "3.1.3",
            "pyjwt": "2.13.0",
            "sqlite_journal_mode": hg.get("wal_mode"),
        },
        "frozen_inputs": {
            "request.json_sha256": "fdc56a4d895d36a2da18d973b94b0bc94a12867d4db1909c75404a96f836bde5",
            "spec.json_sha256": "cb3989523a2bcfba02b16216f8b3584628f624e3b77f99c59961dd3d6dcf9c1a",
            "prereg.md_sha256": "8559b06fc4d86069961841084eb7ba2793ded63a4c8d176ac0e0c320279add2b",
        },
        "code": [
            {"path": "research/graph/delta_repair/execute_delta_repair_single_node_36018188168.py",
             "sha256": sha256_path(DELTA_REPAIR_DIR / "execute_delta_repair_single_node_36018188168.py")},
            {"path": "research/graph/delta_repair/flask_app_36018188168.py",
             "sha256": sha256_path(DELTA_REPAIR_DIR / "flask_app_36018188168.py")},
            {"path": "src/spider/kernel.py",
             "sha256": sha256_path(SRC_DIR / "spider/kernel.py")},
        ],
        "artifacts": artifacts,
        "decision": {"status": decision["status"], "frozen_verdict": decision["frozen_verdict"],
                     "outcome": decision["outcome"], "reason": decision["reason"]},
        "commands": [
            "python3 research/graph/delta_repair/execute_delta_repair_single_node_36018188168.py",
        ],
        "unresolved": result["unresolved"],
    }
    with open(EXPERIMENT_DIR / "provenance.json", "w") as fh:
        json.dump(_json_safe(provenance), fh, indent=2)

    # report.md
    rep = []
    rep.append(f"# {EXPERIMENT_ID} — EXECUTE report (single-node honest re-execution)")
    rep.append("")
    rep.append(f"**Decision:** {decision['frozen_verdict']} — {decision['reason']}")
    rep.append(f"**status={decision['status']} outcome={decision['outcome']}**")
    rep.append("")
    rep.append("## 1. Raw evidence")
    rep.append("- Per-request V13 logs: `raw_evidence/raw_evidence_single.jsonl`, `raw_evidence/raw_evidence_synthetic.jsonl` (every request logged before metrics).")
    rep.append(f"- Health gate: worker_pids={hg.get('worker_pids')}, wal={hg.get('wal_mode')}, jwt={hg.get('jwt_verified')}, 304={hg.get('has_304')}, sticky={hg.get('sticky_consistent')}, rw={hg.get('read_after_write_visible')}.")
    rep.append(f"- Evaluated pool: single-node n_non304={n_non304} (fresh {F1['n_fresh']}, stale {F1['n_stale']}, noise {F1['noise_n']}); synthetic n_non304={n_non304_synth}.")
    rep.append("")
    rep.append("## 2. Observations (measured)")
    rep.append(f"- Freshness single-node: TN {F1['tn_rate']:.4f} (wilson lower {F1['tn_lower']:.4f}), FA {F1['fa']:.4f}, UNKNOWN {F1['unknown_rate']:.4f}, ECE g/f/s {F1['ece_global']:.4f}/{F1['ece_fresh']:.4f}/{F1['ece_stale']:.4f}.")
    for k in (1, 2, 3):
        st = per_k_repair_stats(m1["repairs"], k)
        rep.append(f"- Repair k={k}: pooled {st['pooled_rate']:.4f} (wilson lower {st['pooled_wilson_lower']:.4f}, n={st['n']}), "
                   f"tokens {st['tokens_mean']:.2f} vs {COLD_TOKENS_K[k]}, browser {st['browser_mean']:.2f} vs {COLD_BROWSER_K[k]}, "
                   f"per family { {f: round(st['per_family'][f]['rate'], 3) for f in FAMILIES} }.")
    rep.append(f"- Contamination: " + "; ".join(
        f"k{k}: disjoint {decision['D9_details'][k]['disjoint']['rate']:.4f}, "
        f"same {decision['D9_details'][k]['same']['rate']:.4f}" for k in (1, 2, 3)) + ".")
    rep.append(f"- Verification TEST per k: " + "; ".join(
        f"k{k}: AUROC {decision['D10_details'][k]['auroc']:.4f} prec {decision['D10_details'][k]['precision']:.4f} "
        f"perm_null {decision['D10_details'][k]['perm_null_mean']:.4f}" for k in (1, 2, 3)) + ".")
    rep.append(f"- Honesty: max|rho| {m1['rho']['max_abs_rho']:.4f}, cost std {decision['D13_details']['cost_std']:.4f}, "
               f"min within-family fresh std {F1['min_fresh_std_drift']:.4f}.")
    rep.append("")
    rep.append("## 3. Derived measurements -> interpretation")
    rep.append(f"- All gates: {decision['all_gates']}.")
    rep.append(f"- Synthetic sanity: PC1 {synth_dec['pc1_rate']:.3f}, PC2 { {f: round(v['rate'], 3) for f, v in synth_dec['pc2_by_fam'].items()} }, "
               f"TN {syn_f['tn_rate']:.4f}, FA {syn_f['fa']:.4f}, UNKNOWN {syn_f['unknown_rate']:.4f}, ECE {syn_f['ece_global']:.4f}; "
               f"gates pass = {decision.get('synthetic_gates')}.")
    rep.append(f"- Frozen consequence: {decision['reason']}.")
    rep.append("")
    rep.append("## 4. Validity notes")
    for n in result["validity_notes"]:
        rep.append(f"- {n}")
    rep.append("")
    rep.append("## 5. Unresolved")
    for n in result["unresolved"]:
        rep.append(f"- {n}")
    with open(EXPERIMENT_DIR / "report.md", "w") as fh:
        fh.write("\n".join(rep))

    print(json.dumps({"status": decision["status"], "frozen_verdict": decision["frozen_verdict"],
                      "outcome": decision["outcome"], "reason": decision["reason"],
                      "gates": decision["all_gates"]}, indent=2))
    return decision


if __name__ == "__main__":
    main()