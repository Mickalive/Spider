#!/usr/bin/env python3
"""EXP-PRODUCT-36129169543 EXECUTE runner — Parts A (evidence), B (dry run
on the certified distributed substrate) and C (break-even reuse count).

This runner executes the frozen design in spec.json/prereg.md.  It preserves
raw evidence under ``artifacts/raw/`` and derived measurements under
``artifacts/derived/``; interpretation happens only in result.json/report.md.

Frozen decision rules executed here (prereg.md §5):

  Part A — all five arms implemented, eight counter paths increment,
           fail-closed gate tested, unit tests pass, zero surrogate fills.
  Part B — deterministic scripted policy on the certified single-node HS256
           sticky substrate (health gate n_non304>=360 stratified,
           TN>=0.85); five arms complete; eight counters per trajectory;
           B=5000 bootstrap + B=5000 block-permutation CIs compute;
           UNKNOWN gates fire for BrowserGym/credentials; zero crashes,
           zero surrogate fills.
  Part C — f* = (build + verify) / (cold serving - inherited serving) from
           measured non-token work only; OAT +/-10% sensitivity identifies
           the dominant measured quantity; token economics NOT_APPLICABLE.

Exit code is always 0: infrastructure problems are recorded as
MEASUREMENT_INVALID evidence (never as a scientific negative).
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import socket
import sqlite3
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "src"))

from spider.eval_harness import (  # noqa: E402
    ARM_IDS,
    COUNTER_NAMES,
    ColdArm,
    DeterministicExecutorArm,
    HttpSubstrateEnvironment,
    InstructionsArm,
    MockEnvironment,
    RagEmbedArm,
    SpiderArm,
    block_permutation_test,
    breakeven_f_star,
    build_inheritance,
    build_rag_index,
    fail_closed_gate,
    oat_sensitivity,
    paired_signflip_permutation,
    probe_capabilities,
    run_harness,
    spearman,
    stratified_grouped_bootstrap,
    task_rid,
    tasks_from_manifest,
    verify_inheritance,
)

EXP_ID = "EXP-PRODUCT-36129169543"
PARENT_EXP = "EXP-PRODUCT-36095578013"
SEED = 42
B = 5000  # frozen bootstrap and block-permutation replicates

FIXTURE_DIR = HERE / "fixtures"
RAW = HERE / "artifacts" / "raw"
DER = HERE / "artifacts" / "derived"
REGISTRY_SNAPSHOT = HERE / "artifacts" / "code"
PARENT_FIX = REPO / "research" / "experiments" / PARENT_EXP / "fixtures"

HOLDOUT_NAME = "webarena_verified_v2_tasks_192_36_rebuilt.json"
HOLDOUT_SHA = "101e481ddb610df9598b0e3e5650e8c163ec7cbdc4679c5efc1e31104b3074c5"
QCR_NAME = "qcr_bank_manifest.json"
QCR_SHA = "8c69804b249ec9c84cf05d86a21c7ebe7a31af5f8d45e50a4e6d477b449f9f58"

RUNTIME = Path("/tmp/spider-runtime")
GUNICORN_PORT = 18929
NGINX_PORT = 18930
JWT_SECRET = "spider-exp-36129169543-hs256-secret"

DEP_PINS = ["gunicorn==23.0.0", "Flask==3.1.3", "PyJWT==2.14.0"]

STATUS = {"overall": "COMPLETE", "reasons": []}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def run_cmd(cmd: list[str], timeout: int = 120, env: dict | None = None, cwd: Path | None = None) -> dict:
    t0 = time.time()
    try:
        p = subprocess.run(
            cmd, cwd=str(cwd) if cwd else None, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
        )
        return {"cmd": cmd, "exit": p.returncode, "stdout": p.stdout[-8000:], "stderr": p.stderr[-8000:], "secs": round(time.time() - t0, 2)}
    except Exception as e:
        return {"cmd": cmd, "exit": None, "stdout": "", "stderr": f"{type(e).__name__}: {e}", "secs": round(time.time() - t0, 2)}


# ---------------------------------------------------------------------------
# Dependencies / fixtures / unit tests (Part A evidence)
# ---------------------------------------------------------------------------
def ensure_dependencies() -> dict:
    missing = []
    for mod, pin in (("gunicorn", "gunicorn==23.0.0"), ("flask", "Flask==3.1.3"), ("jwt", "PyJWT==2.14.0")):
        import importlib.util

        if importlib.util.find_spec(mod) is None:
            missing.append(pin)
    out = {"missing_pins": missing, "install": None}
    if missing:
        out["install"] = run_cmd([sys.executable, "-m", "pip", "install", "--quiet", *missing], timeout=300)
    versions = {}
    for dist in ("gunicorn", "flask", "pyjwt"):
        r = run_cmd([sys.executable, "-m", "pip", "show", dist])
        versions[dist] = next((ln.split(":", 1)[1].strip() for ln in r["stdout"].splitlines() if ln.startswith("Version:")), "unknown")
    out["versions"] = versions
    return out


def stage_fixtures() -> dict:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    out = {"staged": [], "sha256": {}}
    for name, expected in ((HOLDOUT_NAME, HOLDOUT_SHA), (QCR_NAME, QCR_SHA)):
        dst = FIXTURE_DIR / name
        src = PARENT_FIX / name
        if not dst.exists():
            shutil.copy2(src, dst)
            out["staged"].append(name)
        actual = sha256_file(dst)
        parent_actual = sha256_file(src)
        out["sha256"][name] = {"expected_prereg": expected, "staged": actual, "parent_source": parent_actual}
        if actual != expected or parent_actual != expected:
            raise RuntimeError(f"fixture hash mismatch for {name}: {actual} vs {expected}")
    return out


def run_unit_tests() -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO / "src")
    res = run_cmd([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], env=env, cwd=REPO, timeout=600)
    (RAW / "unit_tests.txt").write_text(res["stdout"] + "\n" + res["stderr"], encoding="utf-8")
    tail = (res["stdout"] + res["stderr"]).strip().splitlines()
    return {
        "command": "PYTHONPATH=src python3 -m unittest discover -s tests -v",
        "exit": res["exit"],
        "passed": res["exit"] == 0,
        "tail": tail[-3:],
        "tests_module": "tests/test_eval_harness.py (+ tests/test_kernel.py regression)",
    }


# ---------------------------------------------------------------------------
# Certified substrate bring-up + health gate
# ---------------------------------------------------------------------------
APP_PY = r'''
import hashlib, json, os, sqlite3, threading, time
import jwt
from flask import Flask, request, jsonify, Response

DB_PATH = os.environ.get("SPIDER_SHARED_DB", "/tmp/spider-runtime/shared.db")
SECRET = os.environ.get("SPIDER_JWT_SECRET", "spider-exp-36129169543-hs256-secret")
APP = Flask("spider_single_node")
_LOCK = threading.Lock()

def db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    with _LOCK:
        conn = db()
        conn.execute("""CREATE TABLE IF NOT EXISTS req_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts REAL, method TEXT, uri TEXT, status INTEGER,
            etag TEXT, if_none_match TEXT, etag_matched INTEGER,
            worker_pid INTEGER, jwt_alg TEXT)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS resources(
            rid TEXT PRIMARY KEY, gen INTEGER, body TEXT, body_sha TEXT,
            updated_at REAL)""")
        conn.commit(); conn.close()

def issue_token():
    return jwt.encode({"sub": "exp-36129169543", "alg_hint": "HS256",
                       "iat": int(time.time()), "exp": int(time.time()) + 3600},
                      SECRET, algorithm="HS256")

def require_jwt():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "missing bearer"}), 401
    token = auth[len("Bearer "):]
    try:
        header = jwt.get_unverified_header(token)
        if header.get("alg") != "HS256":
            return jsonify({"error": "alg not HS256"}), 401
        jwt.decode(token, SECRET, algorithms=["HS256"])
        return None
    except Exception as e:
        return jsonify({"error": f"jwt: {e}"}), 401

def log_req(uri, status, etag, inm, matched):
    try:
        with _LOCK:
            conn = db()
            conn.execute("INSERT INTO req_log(ts,method,uri,status,etag,if_none_match,etag_matched,worker_pid,jwt_alg) VALUES(?,?,?,?,?,?,?,?,?)",
                         (time.time(), request.method, uri, status, etag, inm, 1 if matched else 0,
                          os.getpid(), "HS256"))
            conn.commit(); conn.close()
    except Exception:
        pass

@APP.route("/healthz")
def healthz():
    err = require_jwt()
    if err: return err
    conn = db(); mode = conn.execute("PRAGMA journal_mode").fetchone()[0]; conn.close()
    return jsonify({"ok": True, "pid": os.getpid(), "journal_mode": mode, "alg": "HS256"})

@APP.route("/api/token")
def token():
    return jsonify({"token": issue_token()})

@APP.route("/api/ep-a/<rid>")
def ep_a(rid):
    return serve_resource(f"ep-a:{rid}")

@APP.route("/api/ep-b/<rid>")
def ep_b(rid):
    return serve_resource(f"ep-b:{rid}")

@APP.route("/api/admin/bump/<path:rid>", methods=["POST"])
def bump(rid):
    err = require_jwt()
    if err: return err
    conn = db()
    row = conn.execute("SELECT gen FROM resources WHERE rid=?", (rid,)).fetchone()
    gen = (row[0] if row else 0) + 1
    body = json.dumps({"rid": rid, "gen": gen, "payload": hashlib.sha256(f"{rid}:{gen}".encode()).hexdigest()[:24]}, sort_keys=True)
    sha = hashlib.sha256(body.encode()).hexdigest()
    conn.execute("INSERT INTO resources(rid,gen,body,body_sha,updated_at) VALUES(?,?,?,?,?) "
                 "ON CONFLICT(rid) DO UPDATE SET gen=excluded.gen, body=excluded.body, "
                 "body_sha=excluded.body_sha, updated_at=excluded.updated_at",
                 (rid, gen, body, sha, time.time()))
    conn.commit(); conn.close()
    return jsonify({"rid": rid, "gen": gen})

def serve_resource(rid):
    err = require_jwt()
    if err:
        log_req(request.path, 401, "", request.headers.get("If-None-Match"), False)
        return err
    conn = db()
    row = conn.execute("SELECT gen, body, body_sha FROM resources WHERE rid=?", (rid,)).fetchone()
    if row is None:
        gen, body = 0, json.dumps({"rid": rid, "gen": 0,
                                   "payload": hashlib.sha256(f"{rid}:0".encode()).hexdigest()[:24]},
                                  sort_keys=True)
        sha = hashlib.sha256(body.encode()).hexdigest()
        conn.execute("INSERT INTO resources(rid,gen,body,body_sha,updated_at) VALUES(?,?,?,?,?)",
                     (rid, 0, body, sha, time.time()))
        conn.commit()
    else:
        gen, body, sha = row
    conn.close()
    etag = f'W/"{sha[:16]}"'
    inm = request.headers.get("If-None-Match")
    matched = bool(inm) and (inm == etag or inm == "*" or etag in [x.strip() for x in inm.split(",")])
    if inm is not None and matched:
        log_req(request.full_path if request.query_string else request.path, 304, etag, inm, True)
        resp = Response(status=304)
        resp.headers["ETag"] = etag
        resp.headers["Cache-Control"] = "max-age=60"
        return resp
    log_req(request.full_path if request.query_string else request.path, 200, etag, inm, False)
    resp = Response(body, status=200, mimetype="application/json")
    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = "max-age=60"
    resp.headers["X-Body-Sha"] = sha
    return resp

init_db()
'''

NGINX_CONF = '''
worker_processes 1;
error_log {run}/nginx_error.log warn;
pid {run}/nginx.pid;
daemon on;
events {{ worker_connections 256; }}
http {{
    access_log {run}/nginx_access.log;
    client_body_temp_path {run}/cbt;
    proxy_temp_path {run}/proxt;
    fastcgi_temp_path {run}/fcgit;
    uwsgi_temp_path {run}/uwsgit;
    scgi_temp_path {run}/scgit;
    upstream spider_backend {{
        hash $request_uri consistent;
        server 127.0.0.1:{gport};
    }}
    log_format sticky '$request_uri upstream=$upstream_addr status=$status';
    server {{
        listen 127.0.0.1:{nport};
        access_log {run}/nginx_sticky.log sticky;
        location / {{
            proxy_pass http://spider_backend;
            proxy_set_header Host $host;
            proxy_set_header If-None-Match $http_if_none_match;
            proxy_set_header Authorization $http_authorization;
            proxy_pass_header ETag;
        }}
    }}
}}
'''


def http_get(url: str, token: str | None, inm: str | None = None, timeout: float = 10.0) -> dict:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if inm is not None:
        headers["If-None-Match"] = inm
    req = urllib.request.Request(url, headers=headers)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return {
                "status": r.status, "etag": r.headers.get("ETag"),
                "body_sha": r.headers.get("X-Body-Sha"), "body": body.decode("utf-8", "replace"),
                "bytes": len(body), "latency_ms": round((time.perf_counter() - t0) * 1000.0, 4),
                "inm_sent": inm is not None, "error": None,
            }
    except urllib.error.HTTPError as e:
        body = e.read() if hasattr(e, "read") else b""
        return {
            "status": e.code, "etag": (e.headers.get("ETag") if e.headers else None),
            "body_sha": None, "body": body.decode("utf-8", "replace"),
            "bytes": len(body), "latency_ms": round((time.perf_counter() - t0) * 1000.0, 4),
            "inm_sent": inm is not None, "error": None,
        }
    except Exception as e:
        return {
            "status": None, "etag": None, "body_sha": None, "body": "", "bytes": 0,
            "latency_ms": round((time.perf_counter() - t0) * 1000.0, 4),
            "inm_sent": inm is not None, "error": f"{type(e).__name__}: {e}",
        }


def provision_substrate() -> dict:
    run_cmd(["pkill", "-f", "gunicorn.*18929"], timeout=10)
    run_cmd(["pkill", "-x", "nginx"], timeout=10)
    time.sleep(0.5)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    for d in ("cbt", "proxt", "fcgit", "uwsgit", "scgit"):
        (RUNTIME / d).mkdir(exist_ok=True)
    db_path = RUNTIME / "shared.db"
    for p in [db_path, Path(str(db_path) + "-wal"), Path(str(db_path) + "-shm")]:
        if p.exists():
            p.unlink()
    (RUNTIME / "app.py").write_text(APP_PY)
    (RUNTIME / "nginx.conf").write_text(NGINX_CONF.format(run=str(RUNTIME), gport=GUNICORN_PORT, nport=NGINX_PORT))

    out = {"experiment_id": EXP_ID, "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    out["nginx_test"] = run_cmd(["nginx", "-t", "-c", str(RUNTIME / "nginx.conf")], timeout=15)

    env = {**os.environ, "SPIDER_SHARED_DB": str(db_path), "SPIDER_JWT_SECRET": JWT_SECRET}
    gerr = open(RUNTIME / "gunicorn_stdout.log", "ab")
    gp = subprocess.Popen(
        [sys.executable, "-m", "gunicorn", "-w", "1", "--bind", f"127.0.0.1:{GUNICORN_PORT}",
         "--pid", str(RUNTIME / "gunicorn.pid"), "--error-logfile", str(RUNTIME / "gunicorn_error.log"),
         "--chdir", str(RUNTIME), "app:APP"],
        env=env, stdout=gerr, stderr=gerr)
    out["gunicorn_pid"] = gp.pid
    for _ in range(60):
        time.sleep(0.1)
        r = http_get(f"http://127.0.0.1:{GUNICORN_PORT}/api/token", None, timeout=2)
        if r["status"] == 200:
            out["gunicorn_up"] = True
            break
    else:
        out["gunicorn_up"] = False

    nerr = open(RUNTIME / "nginx_stdout.log", "ab")
    np_ = subprocess.Popen(["nginx", "-c", str(RUNTIME / "nginx.conf")], stdout=nerr, stderr=nerr)
    np_.wait(timeout=10)
    out["nginx_start_exit"] = np_.returncode
    for _ in range(30):
        time.sleep(0.1)
        r = http_get(f"http://127.0.0.1:{NGINX_PORT}/api/token", None, timeout=2)
        if r["status"] == 200:
            out["nginx_up"] = True
            break
    else:
        out["nginx_up"] = False

    try:
        tok = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{GUNICORN_PORT}/api/token", timeout=3).read())["token"]
        req = urllib.request.Request(f"http://127.0.0.1:{GUNICORN_PORT}/healthz", headers={"Authorization": f"Bearer {tok}"})
        out["health_direct"] = json.loads(urllib.request.urlopen(req, timeout=3).read())
    except Exception as e:
        out["health_direct"] = {"error": str(e)}
    write_json(RAW / "substrate_start.json", out)
    return out


def get_token(base: str) -> str:
    return json.loads(urllib.request.urlopen(f"{base}/api/token", timeout=5).read())["token"]


def health_gate() -> dict:
    """Frozen gate: n_non304 >= 360 stratified (>=180/endpoint), TN >= 0.85,
    WAL single-worker HS256 sticky, ETag W/"body_sha" conditional probe."""
    base = f"http://127.0.0.1:{NGINX_PORT}"
    tok = get_token(base)
    trace = open(RAW / "health_gate_trace.jsonl", "w", encoding="utf-8")
    n_non304 = {"ep-a": 0, "ep-b": 0}
    n_304 = {"ep-a": 0, "ep-b": 0}
    errors = 0
    inm_seen = 0
    total = 0
    etag_w_seen = False
    body_sha_seen = False

    def row(phase: str, ep: str, rid: str, r: dict) -> None:
        nonlocal errors, inm_seen, total, etag_w_seen, body_sha_seen
        total += 1
        if r["error"]:
            errors += 1
        if r["inm_sent"]:
            inm_seen += 1
        if isinstance(r["etag"], str) and r["etag"].startswith('W/"'):
            etag_w_seen = True
        if r["body_sha"]:
            body_sha_seen = True
        trace.write(json.dumps({"phase": phase, "ep": ep, "rid": rid, "status": r["status"],
                                "etag": r["etag"], "inm_sent": r["inm_sent"],
                                "latency_ms": r["latency_ms"], "error": r["error"]}) + "\n")

    # Phase 1: stale If-None-Match must NOT be accepted (true negative for staleness)
    for ep in ("ep-a", "ep-b"):
        for i in range(200):
            rid = f"gate-{ep}-{i}"
            r = http_get(f"{base}/api/{ep}/{rid}", tok, inm='W/"0000000000000000"')
            row("stale_probe", ep, rid, r)
            if r["status"] == 200:
                n_non304[ep] += 1
            elif r["status"] == 304:
                n_304[ep] += 1

    # Phase 2: TN_fresh — a matching validator must yield 304 (no refetch)
    tn_hits = 0
    tn_n = 150
    for i in range(tn_n):
        rid = f"gate-tn-{i}"
        r1 = http_get(f"{base}/api/ep-a/{rid}", tok)
        row("tn_prime", "ep-a", rid, r1)
        r2 = http_get(f"{base}/api/ep-a/{rid}", tok, inm=r1["etag"])
        row("tn_conditional", "ep-a", rid, r2)
        if r2["status"] == 304:
            tn_hits += 1
    tn_rate = tn_hits / tn_n

    trace.close()

    # Substrate structural checks
    structural: dict[str, Any] = {}
    try:
        conn = sqlite3.connect(str(RUNTIME / "shared.db"))
        structural["journal_mode"] = conn.execute("PRAGMA journal_mode").fetchone()[0]
        rows = conn.execute("SELECT DISTINCT worker_pid FROM req_log").fetchall()
        structural["distinct_worker_pids"] = sorted(r[0] for r in rows)
        algs = conn.execute("SELECT DISTINCT jwt_alg FROM req_log").fetchall()
        structural["jwt_algs"] = sorted(r[0] for r in algs)
        structural["req_log_rows"] = conn.execute("SELECT COUNT(*) FROM req_log").fetchone()[0]
        conn.close()
    except Exception as e:
        structural["error"] = str(e)

    sticky_lines = []
    sticky_path = RUNTIME / "nginx_sticky.log"
    if sticky_path.exists():
        sticky_lines = [ln for ln in sticky_path.read_text(errors="replace").splitlines() if ln.strip()]
    upstreams = sorted({ln.split("upstream=")[1].split()[0] for ln in sticky_lines if "upstream=" in ln})
    structural["nginx_sticky_lines"] = len(sticky_lines)
    structural["nginx_upstreams"] = upstreams

    stratified = all(v >= 180 for v in n_non304.values()) and sum(n_non304.values()) >= 360
    gate = {
        "n_non304_stratified": n_non304,
        "n_non304_total": sum(n_non304.values()),
        "n_304_stratified": n_304,
        "gate_threshold": "n_non304>=360 total and >=180 per endpoint",
        "stratified_pass": stratified,
        "tn_fresh_hits": tn_hits,
        "tn_fresh_n": tn_n,
        "TN_fresh": tn_rate,
        "tn_threshold": 0.85,
        "tn_pass": tn_rate >= 0.85,
        "if_none_match_exercised_fraction": inm_seen / total if total else 0.0,
        "errors": errors,
        "etag_W_format_seen": etag_w_seen,
        "x_body_sha_seen": body_sha_seen,
        "structural": structural,
        "single_worker": structural.get("distinct_worker_pids") is not None and len(structural.get("distinct_worker_pids", [])) == 1,
        "hs256": structural.get("jwt_algs") == ["HS256"],
        "wal": structural.get("journal_mode") == "wal",
        "sticky_via_nginx": len(upstreams) >= 1 and any(u.startswith("127.0.0.1:") for u in upstreams),
        "requests_issued": total,
    }
    gate["health_gate_pass"] = bool(
        gate["stratified_pass"] and gate["tn_pass"] and gate["errors"] == 0
        and gate["etag_W_format_seen"] and gate["x_body_sha_seen"]
        and gate["single_worker"] and gate["hs256"] and gate["wal"] and gate["sticky_via_nginx"]
    )
    write_json(DER / "health_gate.json", gate)
    return gate


# ---------------------------------------------------------------------------
# Derived summaries
# ---------------------------------------------------------------------------
def arm_summary(records: list) -> dict:
    out: dict[str, Any] = {}
    for arm in ARM_IDS:
        recs = [r for r in records if r.arm_id == arm]
        executable = [r for r in recs if r.gate_status == "EXECUTABLE" and r.counters is not None]
        entry: dict[str, Any] = {
            "n_records": len(recs),
            "n_executable": len(executable),
            "gate_statuses": sorted({r.gate_status for r in recs}),
            "counters_sum": {c: sum(r.counters[c] for r in executable) for c in COUNTER_NAMES},
            "counters_mean_per_trajectory": {
                c: (statistics.mean(r.counters[c] for r in executable) if executable else None)
                for c in COUNTER_NAMES
            },
            "payload_bytes_total": sum(r.payload_bytes for r in executable if r.payload_bytes is not None),
            "payload_bytes_mean": (
                statistics.mean(r.payload_bytes for r in executable) if executable else None
            ),
            "latency_ms_total": sum(r.counters["latency_ms"] for r in executable),
            "integrity_failures": sum(int(r.extras.get("integrity_failures") or 0) for r in executable),
            "stale_repairs_total": sum(int(r.extras.get("stale_repairs") or 0) for r in executable),
            "resolve_executable": sum(
                1 for r in executable if r.extras.get("resolve_status") == "EXECUTABLE"
            ),
            "auditor_pass": sum(1 for r in executable if r.extras.get("auditor_pass") is True),
            "counter_ops_mean_per_trajectory": (
                statistics.mean(
                    sum(v for k, v in r.counters.items() if k != "latency_ms") for r in executable
                )
                if executable else None
            ),
        }
        out[arm] = entry
    return out


def paired_ci_block(records: list) -> dict:
    """Family-stratified trajectory-grouped bootstrap (B=5000) and paired
    block-permutation (B=5000) for P-SPIDER vs each baseline on the measured
    non-token serving dimensions."""
    idx = {(r.arm_id, r.task_id): r for r in records}
    tasks = sorted({r.task_id for r in records})
    out: dict[str, Any] = {"B": B, "seed": SEED, "comparisons": {}}
    for baseline in [a for a in ARM_IDS if a != "P-SPIDER"]:
        rows = []
        for tid in tasks:
            sp = idx.get(("P-SPIDER", tid))
            bl = idx.get((baseline, tid))
            if not sp or not bl or sp.counters is None or bl.counters is None:
                continue
            rows.append(
                {
                    "family_id": sp.family_id,
                    "task_id": tid,
                    "delta_latency_ms": bl.counters["latency_ms"] - sp.counters["latency_ms"],
                    "delta_payload_bytes": (bl.payload_bytes or 0) - (sp.payload_bytes or 0),
                    "delta_requests": bl.counters["requests"] - sp.counters["requests"],
                }
            )
        comp: dict[str, Any] = {"n_paired": len(rows)}
        for metric in ("delta_latency_ms", "delta_payload_bytes", "delta_requests"):
            ci = stratified_grouped_bootstrap(
                rows, lambda s, m=metric: statistics.mean(r[m] for r in s), B=B, seed=SEED
            )
            perm = paired_signflip_permutation(
                [r[metric] for r in rows], [r["family_id"] for r in rows], B=B, seed=SEED
            )
            comp[metric] = {
                "observed_mean": statistics.mean(r[metric] for r in rows) if rows else None,
                "bootstrap_ci95": [ci.get("lo"), ci.get("hi")],
                "bootstrap_B": ci.get("B"),
                "bootstrap_n_valid": ci.get("n_valid"),
                "block_permutation_p": perm.get("p"),
                "unit": "ms" if metric.endswith("ms") else ("bytes" if metric.endswith("bytes") else "requests"),
                "direction": "positive => P-SPIDER spent less than the baseline",
            }
        out["comparisons"][baseline] = comp
    return out


def null_control_block(records: list) -> dict:
    """NC-SHUFFLED-FAMILY-STRATIFIED (frozen).

    Statistic: per-trajectory counter delta between the two arms that perform
    identical HTTP work under the deterministic scripted policy,
    Delta_i = latency_ms(B-INSTRUCTIONS)_i - latency_ms(B-COLD)_i.  The two
    arms differ only by one local instruction-file read, so under the null the
    delta is measurement noise: no counter formula couples it deterministically
    to L or to novelty (the inherited NC1 failure mode, deterministic coupling
    reused=max(0,L-n_novel*2), cannot arise from an honest difference of two
    identical request sequences).

    Gates (frozen): |rho_shuffled| < 0.20; |rho_length| < 0.20 per novelty
    stratum; family-blocked permutation p >= 0.20.
    """
    idx = {(r.arm_id, r.task_id): r for r in records}
    rows = []
    for tid in sorted({r.task_id for r in records}):
        inst = idx.get(("B-INSTRUCTIONS", tid))
        cold = idx.get(("B-COLD", tid))
        if not inst or not cold or inst.counters is None or cold.counters is None:
            continue
        rows.append(
            {
                "family_id": cold.family_id,
                "task_id": tid,
                "delta": inst.counters["latency_ms"] - cold.counters["latency_ms"],
                "length": cold.length,
                "novelty": cold.novelty_level,
            }
        )

    perm = block_permutation_test(rows, "novelty", "delta", block_key="family_id", B=B, seed=SEED)
    strata: dict[float, list[dict]] = {}
    for r in rows:
        strata.setdefault(float(r["novelty"]), []).append(r)

    per_stratum = {}
    for level in sorted(strata):
        grp = strata[level]
        rho = spearman([r["delta"] for r in grp], [r["length"] for r in grp])
        distinct_l = len({r["length"] for r in grp})
        ok = rho is not None and abs(rho) < 0.20
        # Report-only diagnostic (gate unchanged, frozen literal reading):
        # chance baseline for rho_length within this stratum via trajectory-
        # level permutation of delta.  Distinguishes a genuinely coupled
        # statistic from a per-stratum gate that is simply underpowered at n.
        import random as _random

        rng = _random.Random(SEED + int(round(level * 1000)))
        deltas = [r["delta"] for r in grp]
        lengths = [r["length"] for r in grp]
        null_rhos: list[float] = []
        extreme = 0
        obs_abs = abs(rho) if rho is not None else None
        for _ in range(B):
            shuffled = list(deltas)
            rng.shuffle(shuffled)
            rr = spearman(shuffled, lengths)
            if rr is not None:
                null_rhos.append(rr)
                if obs_abs is not None and abs(rr) >= obs_abs:
                    extreme += 1
        perm_p = (extreme + 1) / (len(null_rhos) + 1) if null_rhos else None
        per_stratum[str(level)] = {
            "n": len(grp),
            "distinct_L": distinct_l,
            "rho_length": rho,
            "gate": "|rho_length| < 0.20",
            "pass": bool(ok),
            "degenerate": rho is None,
            "rho_length_shuffled_median": statistics.median(null_rhos) if null_rhos else None,
            "rho_length_perm_p": perm_p,
            "rho_length_perm_p_note": "report-only diagnostic; not a frozen gate",
        }
    rho_pooled = spearman([r["delta"] for r in rows], [r["length"] for r in rows])
    rho_shuffled_median = perm.get("rho_shuffled_median")
    p = perm.get("p")

    gates = {
        "rho_shuffled": rho_shuffled_median is not None and abs(rho_shuffled_median) < 0.20,
        "block_permutation_p": p is not None and p >= 0.20,
        "rho_length_all_strata": all(v["pass"] for v in per_stratum.values()) and bool(per_stratum),
    }
    return {
        "id": "NC-SHUFFLED-FAMILY-STRATIFIED",
        "statistic": "Delta = latency_ms(B-INSTRUCTIONS) - latency_ms(B-COLD) per trajectory",
        "stratification": "family-blocked permutation; novelty-level strata for rho_length",
        "n_rows": len(rows),
        "rho_shuffled_median": rho_shuffled_median,
        "rho_shuffled_ci95": [perm.get("rho_shuffled_lo"), perm.get("rho_shuffled_hi")],
        "rho_shuffled_gate": "|rho_shuffled| < 0.20",
        "rho_novelty_observed": perm.get("rho_observed"),
        "block_permutation_p": p,
        "block_permutation_p_gate": "p >= 0.20",
        "rho_length_per_stratum": per_stratum,
        "rho_length_pooled_diagnostic": rho_pooled,
        "B": B,
        "seed": SEED,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
        "expected_behavior": "shuffled correlations near zero; block-permutation p >= 0.20; no deterministic coupling from counter formulas",
    }


def breakeven_block(summary: dict, records: list, build: dict, verify: dict, ci_block: dict) -> dict:
    cold = summary["B-COLD"]
    spider = summary["P-SPIDER"]
    cold_lat = cold["counters_mean_per_trajectory"]["latency_ms"]
    spider_lat = spider["counters_mean_per_trajectory"]["latency_ms"]
    cold_bytes = cold["payload_bytes_mean"]
    spider_bytes = spider["payload_bytes_mean"]
    cold_req = cold["counters_mean_per_trajectory"]["requests"]
    spider_req = spider["counters_mean_per_trajectory"]["requests"]
    cold_ops = cold["counter_ops_mean_per_trajectory"]
    spider_ops = spider["counter_ops_mean_per_trajectory"]

    inputs_ms = {
        "build_cost": build["build_ms"],
        "verify_cost": verify["verify_ms"],
        "cold_serving_cost": cold_lat,
        "inherited_serving_cost": spider_lat,
    }
    f_ms = breakeven_f_star(**inputs_ms, unit="ms")
    sens_ms = oat_sensitivity(inputs_ms, lambda **kw: breakeven_f_star(**kw, unit="ms"), delta=0.10)

    inputs_bytes = {
        "build_cost": float(build["harvest_payload_bytes"]),
        "verify_cost": float(verify["probe_payload_bytes"]),
        "cold_serving_cost": cold_bytes,
        "inherited_serving_cost": spider_bytes,
    }
    f_bytes = breakeven_f_star(**inputs_bytes, unit="bytes")
    sens_bytes = oat_sensitivity(inputs_bytes, lambda **kw: breakeven_f_star(**kw, unit="bytes"), delta=0.10)

    f_requests = breakeven_f_star(
        float(build["harvest_requests"] + verify["probe_requests"]),
        0.0, cold_req, spider_req, unit="requests",
    )
    f_ops = breakeven_f_star(0.0, 0.0, cold_ops, spider_ops, unit="counter_ops")

    # Bootstrap CI for the primary latency denominator -> f* interval
    idx = {(r.arm_id, r.task_id): r for r in records}
    rows = []
    for tid in sorted({r.task_id for r in records}):
        sp = idx.get(("P-SPIDER", tid))
        cl = idx.get(("B-COLD", tid))
        if sp and cl and sp.counters is not None and cl.counters is not None:
            rows.append({"family_id": sp.family_id, "delta": cl.counters["latency_ms"] - sp.counters["latency_ms"]})
    den_ci = stratified_grouped_bootstrap(
        rows, lambda s: statistics.mean(r["delta"] for r in s), B=B, seed=SEED
    )
    f_ci = None
    if f_ms["computable"] and den_ci.get("lo") and den_ci["lo"] > 0:
        num = inputs_ms["build_cost"] + inputs_ms["verify_cost"]
        f_ci = [num / den_ci["hi"], num / den_ci["lo"]]
    elif f_ms["computable"] and den_ci.get("median") and den_ci["median"] > 0:
        num = inputs_ms["build_cost"] + inputs_ms["verify_cost"]
        den_median = den_ci["median"]
        f_ci = None  # keep null rather than extrapolate outside the CI bounds

    primary_unit = "ms" if f_ms["computable"] else ("bytes" if f_bytes["computable"] else None)
    primary = f_ms if primary_unit == "ms" else (f_bytes if primary_unit == "bytes" else f_ms)
    primary_sens = sens_ms if primary_unit == "ms" else (sens_bytes if primary_unit == "bytes" else sens_ms)

    return {
        "formula": "f* = (build_cost + verify_cost) / (serving_cost_cold - serving_cost_inherited)",
        "inputs_ms": inputs_ms,
        "f_star_ms": f_ms,
        "sensitivity_ms": sens_ms,
        "f_star_bytes": f_bytes,
        "sensitivity_bytes": sens_bytes,
        "f_star_requests": f_requests,
        "f_star_counter_ops": f_ops,
        "primary_unit": primary_unit,
        "primary_f_star": primary.get("f_star"),
        "primary_sensitivity": primary_sens,
        "dominant_quantity": primary_sens.get("dominant_quantity"),
        "dominant_max_abs_rel_change": primary_sens.get("dominant_max_abs_rel_change"),
        "denominator_ci95_latency_ms": [den_ci.get("lo"), den_ci.get("hi")],
        "f_star_ci95_latency_ms": f_ci,
        "token_economics": {
            "status": "NOT_APPLICABLE",
            "f_star_token": None,
            "reason": "OPENAI_API_KEY absent; frozen spec forbids token counters/costs until a policy-model credential exists (UNKNOWN)",
        },
        "reuse_unit": "one executed trajectory (task) reusing the inherited family artifact",
        "notes": [
            "build/verify/serving are measured wall-clock and transfer work from this dry run",
            "requests and counter_ops units are reported even when not computable (denominator ~0 or negative) because they show where the saving lives",
        ],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    for d in (RAW, DER, REGISTRY_SNAPSHOT):
        d.mkdir(parents=True, exist_ok=True)

    # Attempt archival: raw traces are opened in append mode downstream, so a
    # re-run after an implementation-defect fix must start from clean files.
    # Preserve every prior derived output verbatim for provenance.
    if (DER / "metrics_summary.json").exists():
        archive = HERE / "artifacts" / "attempt1"
        for sub in ("raw", "derived"):
            src, dst = HERE / "artifacts" / sub, archive / sub
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        for stale in ("artifacts/raw/request_trace.jsonl", "artifacts/raw/health_gate_trace.jsonl"):
            p = HERE / stale
            if p.exists():
                p.unlink()

    summary: dict[str, Any] = {"experiment_id": EXP_ID, "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    substrate = None
    gate = None
    env = None
    try:
        summary["dependencies"] = ensure_dependencies()
        summary["fixtures"] = stage_fixtures()
        summary["unit_tests"] = run_unit_tests()

        fixture = json.loads((FIXTURE_DIR / HOLDOUT_NAME).read_text())
        tasks = tasks_from_manifest(fixture)
        manifest_checks = {
            "n_tasks": len(tasks),
            "n_families": len({t.family_id for t in tasks}),
            "single_template_per_family": len({(t.family_id, t.template_id) for t in tasks})
            == len({t.family_id for t in tasks}),
            "single_L_per_family": len({(t.family_id, t.length) for t in tasks})
            == len({t.family_id for t in tasks}),
            "novelty_levels": sorted({round(t.novelty_level, 6) for t in tasks}),
            "L_values": sorted({t.length for t in tasks}),
            "slots_have_no_dotted_names": all("." not in s for t in tasks for s in t.slots),
        }
        summary["manifest_checks"] = manifest_checks
        if not (
            manifest_checks["n_tasks"] == 192
            and manifest_checks["n_families"] == 36
            and manifest_checks["single_template_per_family"]
            and manifest_checks["single_L_per_family"]
        ):
            raise RuntimeError(f"manifest invariant violated: {manifest_checks}")

        # --- substrate + health gate (Part B prerequisite) ------------------
        substrate = provision_substrate()
        if not (substrate.get("gunicorn_up") and substrate.get("nginx_up")):
            gate = {"health_gate_pass": False, "failure": "substrate did not come up", "substrate_start": substrate}
            write_json(DER / "health_gate.json", gate)
            summary["status"] = "MEASUREMENT_INVALID"
            summary["reason"] = "infrastructure: substrate bring-up failed (not a scientific negative)"
            write_json(DER / "metrics_summary.json", summary)
            print(json.dumps(summary, indent=1))
            return 0
        gate = health_gate()
        if not gate["health_gate_pass"]:
            summary["status"] = "MEASUREMENT_INVALID"
            summary["reason"] = "infrastructure: health gate failed (not a scientific negative)"
            write_json(DER / "metrics_summary.json", summary)
            print(json.dumps(summary, indent=1))
            return 0

        caps = probe_capabilities(substrate_ok=True)
        write_json(DER / "capability_probe.json", caps)

        # --- build + verify inheritance (Part C inputs, measured) -----------
        base_url = f"http://127.0.0.1:{NGINX_PORT}"
        token = get_token(base_url)
        env = HttpSubstrateEnvironment(base_url, token, trace_path=RAW / "request_trace.jsonl")
        env.tag = "substrate"

        env.tag = "build"
        inheritance = build_inheritance(env, tasks, fixture, REGISTRY_SNAPSHOT / "registry", trace_phase="build")
        build = inheritance.build
        write_json(RAW / "build.json", build)

        env.tag = "verify"
        verify = verify_inheritance(env, inheritance, tasks)
        write_json(RAW / "verify_pass.json", verify)

        env.tag = "rag_index"
        t0 = time.perf_counter()
        rag_index = build_rag_index(fixture)
        rag_index_ms = (time.perf_counter() - t0) * 1000.0

        # --- Part B: run all five arms (deterministic scripted policy) ------
        spider_arm = SpiderArm(inheritance)
        base_arms = [
            ColdArm(),
            InstructionsArm(),
            RagEmbedArm(rag_index),
            DeterministicExecutorArm(),
        ]
        records = []
        arm_phases: dict[str, Any] = {}
        for arm in base_arms:
            env.tag = arm.arm_id
            t0 = time.perf_counter()
            recs = run_harness([arm], tasks, env, mode="scripted", capabilities=caps["available"])
            arm_phases[arm.arm_id] = {"secs": round(time.perf_counter() - t0, 3), "records": len(recs)}
            records.extend(recs)

        # Deterministic staleness injection right before the inherited arm so
        # the localized-repair counter path is exercised end to end.
        fam_novelty: dict[str, float] = {}
        for t in tasks:
            fam_novelty[t.family_id] = max(fam_novelty.get(t.family_id, 0.0), t.novelty_level)
        bumped = []
        for fid in sorted(fam_novelty):
            if fam_novelty[fid] <= 0:
                continue
            grp = [t for t in tasks if t.family_id == fid]
            tmpl, length = grp[0].template_id, grp[0].length
            rid = f"{fid}_{tmpl}_s0"
            try:
                # The substrate stores ep-A resources under the ep-a: prefix
                # (serve_resource(f"ep-a:{rid}")); bumping the bare rid would
                # hit a different key and never produce staleness.
                env.bump(f"ep-a:{rid}")
                bumped.append(rid)
            except Exception as e:
                bumped.append(f"{rid}:ERROR:{type(e).__name__}:{e}")
        write_json(RAW / "staleness_injection.json", {
            "policy": "bump step-0 structural resource for every family whose max realized_novelty > 0",
            "n_bumped": len(bumped),
            "rids": bumped,
            "purpose": "exercise the freshness->stale->localized-repair counter path on the real substrate",
        })

        env.tag = "P-SPIDER"
        t0 = time.perf_counter()
        recs = run_harness([spider_arm], tasks, env, mode="scripted", capabilities=caps["available"])
        arm_phases["P-SPIDER"] = {"secs": round(time.perf_counter() - t0, 3), "records": len(recs)}
        records.extend(recs)
        env.close()

        # RAW evidence: one row per trajectory
        with open(RAW / "trajectories.jsonl", "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps({
                    "arm_id": r.arm_id, "mode": r.mode, "task_id": r.task_id,
                    "family_id": r.family_id, "novelty_level": r.novelty_level,
                    "length": r.length, "gate_status": r.gate_status,
                    "gate_reason": r.gate_reason, "counters": r.counters,
                    "payload_bytes": r.payload_bytes, "extras": r.extras,
                }, sort_keys=True) + "\n")

        summary["arm_phases"] = arm_phases
        summary["arm_summary"] = arm_summary(records)

        # --- Part B gates ---------------------------------------------------
        executable_by_arm = {a: summary["arm_summary"][a]["n_executable"] for a in ARM_IDS}
        all_arms_complete = all(executable_by_arm[a] == len(tasks) for a in ARM_IDS)
        unknown_gates = probe_capabilities(substrate_ok=True)
        live_gate = {a: fail_closed_gate(a, "live_browser", unknown_gates["available"]).status for a in ARM_IDS}
        scripted_gate = {a: fail_closed_gate(a, "scripted", unknown_gates["available"]).status for a in ARM_IDS}

        # gate demo records (no numbers on the UNKNOWN side, by construction)
        demo_env = MockEnvironment()
        demo_records = run_harness(
            [ColdArm(), InstructionsArm(), RagEmbedArm(rag_index), DeterministicExecutorArm(), spider_arm],
            tasks[:3], demo_env, mode="live_browser", capabilities=unknown_gates["available"],
        )
        write_json(DER / "gate_demo.json", {
            "live_browser_gate_by_arm": live_gate,
            "scripted_gate_by_arm": scripted_gate,
            "capability_details": unknown_gates["details"],
            "unknown_demo_records": [
                {"arm_id": r.arm_id, "gate_status": r.gate_status, "counters": r.counters,
                 "payload_bytes": r.payload_bytes, "missing": r.extras.get("missing_capabilities")}
                for r in demo_records
            ],
            "no_surrogate_or_default_fill": all(
                r.counters is None and r.payload_bytes is None
                for r in demo_records if r.gate_status == "UNKNOWN"
            ),
        })

        # transport errors in the arm/build trace (zero-crash criterion)
        trace_errors = 0
        trace_rows = 0
        with open(RAW / "request_trace.jsonl", encoding="utf-8") as f:
            for line in f:
                trace_rows += 1
                if json.loads(line).get("error"):
                    trace_errors += 1

        ci_block = paired_ci_block(records)
        write_json(DER / "ci.json", ci_block)
        ci_compute_ok = all(
            comp[m]["bootstrap_ci95"][0] is not None
            and comp[m]["bootstrap_ci95"][1] is not None
            and comp[m]["block_permutation_p"] is not None
            for comp in ci_block["comparisons"].values()
            for m in ("delta_latency_ms", "delta_payload_bytes", "delta_requests")
        )

        nc = null_control_block(records)
        write_json(DER / "null_control.json", nc)

        breakeven = breakeven_block(summary["arm_summary"], records, build, verify, ci_block)
        write_json(DER / "breakeven.json", breakeven)

        # --- Part A / B / C verdict inputs ---------------------------------
        part_a = {
            "five_arms_implemented": sorted({r.arm_id for r in records}) == sorted(ARM_IDS),
            "eight_counter_paths_present": list(COUNTER_NAMES),
            "all_eight_counter_paths_nonzero": all(
                summary["arm_summary"][a]["counters_sum"][c] > 0
                for c in COUNTER_NAMES
                for a in [max(ARM_IDS, key=lambda x: summary["arm_summary"][x]["counters_sum"][c])]
            ),
            "unit_tests_passed": summary["unit_tests"]["passed"],
            "zero_surrogate_fills": all(
                (r.counters is None) if r.gate_status == "UNKNOWN" else (
                    r.counters is not None and set(r.counters) == set(COUNTER_NAMES)
                )
                for r in records
            ),
            "gate_unknown_records_have_no_numbers": all(
                r.counters is None for r in records if r.gate_status == "UNKNOWN"
            ),
        }
        part_b = {
            "health_gate_pass": gate["health_gate_pass"],
            "all_five_arms_complete": all_arms_complete,
            "executable_by_arm": executable_by_arm,
            "n_records_total": len(records),
            "all_eight_counters_recorded_per_trajectory": all(
                r.counters is not None and set(r.counters) == set(COUNTER_NAMES)
                for r in records if r.gate_status == "EXECUTABLE"
            ),
            "bootstrap_and_permutation_compute": ci_compute_ok,
            "B": B,
            "unknown_gates_fire_for_live_mode": all(v == "UNKNOWN" for v in live_gate.values()),
            "scripted_mode_executable": all(v == "EXECUTABLE" for v in scripted_gate.values()),
            "trace_request_rows": trace_rows,
            "transport_errors": trace_errors,
            "zero_crashes": trace_errors == 0,
            "zero_default_fills": part_a["gate_unknown_records_have_no_numbers"],
            "disclosure": "instrument correctness ONLY — not a scientific or product result",
        }
        part_c = {
            "f_star_computed": breakeven["primary_f_star"] is not None and breakeven["primary_unit"] is not None,
            "primary_unit": breakeven["primary_unit"],
            "f_star": breakeven["primary_f_star"],
            "dominant_quantity": breakeven["dominant_quantity"],
            "formula": breakeven["formula"],
            "token_economics_status": "NOT_APPLICABLE",
            "inputs_ms": breakeven["inputs_ms"],
        }

        part_a_pass = all(part_a[k] for k in (
            "five_arms_implemented", "all_eight_counter_paths_nonzero",
            "unit_tests_passed", "zero_surrogate_fills", "gate_unknown_records_have_no_numbers",
        ))
        part_b_pass = all(part_b[k] for k in (
            "health_gate_pass", "all_five_arms_complete", "all_eight_counters_recorded_per_trajectory",
            "bootstrap_and_permutation_compute", "unknown_gates_fire_for_live_mode",
            "scripted_mode_executable", "zero_crashes", "zero_default_fills",
        ))
        part_c_pass = bool(part_c["f_star_computed"] and part_c["dominant_quantity"])

        summary["part_a"] = {**part_a, "PASS": part_a_pass}
        summary["part_b"] = {**part_b, "PASS": part_b_pass}
        summary["part_c"] = {**part_c, "PASS": part_c_pass}
        summary["null_control"] = {
            "id": nc["id"], "all_gates_pass": nc["all_gates_pass"], "gates": nc["gates"],
            "rho_shuffled_median": nc["rho_shuffled_median"],
            "block_permutation_p": nc["block_permutation_p"],
        }
        if part_a_pass and part_b_pass and part_c_pass:
            summary["status"] = "COMPLETE"
            summary["outcome_rule"] = "all three parts PASS -> SUPPORTS (instrument decidable, f* computable)"
        elif summary.get("status") == "MEASUREMENT_INVALID":
            pass
        else:
            summary["status"] = "COMPLETE"
            summary["outcome_rule"] = "a part failed validly -> FALSIFIES (specific instrument gap)"
            summary["failed_parts"] = [n for n, ok in (("A", part_a_pass), ("B", part_b_pass), ("C", part_c_pass)) if not ok]

        # kernel durability observation (inherited do-not-assume)
        kernel_path = REPO / "src" / "spider" / "kernel.py"
        summary["kernel_observation"] = {
            "working_tree_sha256": sha256_file(kernel_path),
            "dot_regex_present": "${" in kernel_path.read_text() and "[A-Za-z0-9_\\.]" in kernel_path.read_text(),
            "note": "parent packet recorded uncommitted working-tree patch d926279d (dot-regex); this execute base has no such patch",
        }
        summary["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        write_json(DER / "metrics_summary.json", summary)
        print(json.dumps({k: summary[k] for k in (
            "status", "outcome_rule", "failed_parts", "part_a", "part_b", "part_c", "null_control",
        ) if k in summary}, indent=1, default=str))
        return 0

    except Exception as e:
        import traceback

        crash = {"error": f"{type(e).__name__}: {e}", "traceback": traceback.format_exc()}
        write_json(RAW / "crash.json", crash)
        summary["status"] = "BLOCKED" if summary.get("part_a") else "MEASUREMENT_INVALID"
        summary["reason"] = f"runner exception: {type(e).__name__}: {e}"
        write_json(DER / "metrics_summary.json", summary)
        print(json.dumps({"crashed": crash["error"]}, indent=1))
        return 0
    finally:
        stop_substrate()


def stop_substrate() -> None:
    try:
        run_cmd(["nginx", "-s", "stop", "-c", str(RUNTIME / "nginx.conf")], timeout=10)
    except Exception:
        pass
    try:
        run_cmd(["pkill", "-f", "gunicorn.*18929"], timeout=10)
    except Exception:
        pass


if __name__ == "__main__":
    raise SystemExit(main())
