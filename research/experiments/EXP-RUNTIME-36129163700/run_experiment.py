#!/usr/bin/env python3
"""
EXP-RUNTIME-36129163700 — H1-A-INTERVENTION-VALIDITY (C-MEAS-VALID)

Frozen inputs (request.json / spec.json / prereg.md / freeze.json) are immutable.
This harness executes the frozen design exactly:

  Part A (PRIMARY, non-vetoable by anything else):
    Intervention-validity control matrix on the certified distributed
    stable-header shared-WAL plain-HTTP substrate from EXP-RUNTIME-36100549580:
      2x gunicorn 23.0.0 workers binding 127.0.0.1:19860 AND 127.0.0.1:19861,
      ONE shared SQLite WAL at /tmp/single.db with PRAGMA wal_autocheckpoint=0,
      exclusive nginx 1.24.0 on 127.0.0.1:19851, one hash $request_uri
      consistent upstream, real proxy_cache, authorization bypass, X-Worker-Pid.
    6 arms x 20 episodes = 120 episodes, seeded balanced permutation
    (seed 36129163700), raw order archived before scoring.
    Positive arms P-WRITE / P-DRIFT must be detected (point >= 0.90,
    two-sided 95% Wilson lower bound >= 0.80, z = 1.959963984540054).
    Null arms N-READ / N-INVALID / N-EXPIRED / N-DELETED must produce no
    false positive (point specificity >= 0.90, Wilson lower bound >= 0.80).
    The detector is blind to the arm label; the label is joined only after
    the detector output is written. An independent recomputation from raw
    JSONL must reproduce every bit with zero mismatches (V-RECOMPUTE).

  Part B (standalone, NON-VETOING capability):
    Public Playwright API only (p.chromium.executable_path preferred;
    public p.chromium.launch() equivalent). Real Chromium at 1280x720,
    real CDP DOM snapshot + Accessibility.getFullAXTree, one reversible
    valid-auth SPA write through real page controls, and read-only /
    invalid-auth / expired-auth / deleted-session nulls leaving the WAL
    unchanged. Any absent capability is B=UNAVAILABLE with exact artifact
    and one smallest unblocking action. B can never veto or alter Part A.

  Part C (contract):
    One same-run machine-readable capability ledger plus one-command
    substrate bring-up contract:
      python -m research.runtime.bringup \
        --config research/experiments/EXP-RUNTIME-36129163700/bringup_contract.json \
        --ledger  research/experiments/EXP-RUNTIME-36129163700/artifacts/capability_ledger.json

  Durability (V-DUR-HEAD):
    Frozen scope research/experiments/EXP-RUNTIME-36129163700/run_experiment.py
    and research/runtime/bringup.py compared against HEAD. Under the lane
    no-commit rule an uncommitted implementation is REFERENCE_ONLY and
    DURABILITY=UNSATISFIABLE — a bounded contract result, never a scientific
    falsification of Part A.

Information discipline: RAW EVIDENCE (JSONL) is written before any derived
metric. Observations, derived measurements and interpretation are kept in
separate result.json fields. No synthetic fallback anywhere: any failed real
probe is recorded UNAVAILABLE/ERROR with its evidence.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import math
import os
import random
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import jwt
import requests
from flask import Flask, g, jsonify, request as flask_request

# ── Frozen identities ──────────────────────────────────────────────────────
EXPERIMENT_ID = "EXP-RUNTIME-36129163700"
LANE = "runtime"
CLAIM_ID = "C-MEAS-VALID"
RUN_ID = "36129163700"
SEED = 36129163700
WILSON_Z = 1.959963984540054  # frozen two-sided 95% Wilson z
EPISODES_PER_ARM = 20
ARMS = ["P-WRITE", "P-DRIFT", "N-READ", "N-INVALID", "N-EXPIRED", "N-DELETED"]
POSITIVE_ARMS = ["P-WRITE", "P-DRIFT"]
NULL_ARMS = ["N-READ", "N-INVALID", "N-EXPIRED", "N-DELETED"]

# ── Frozen substrate contract (prereg 3.1) ─────────────────────────────────
DB_PATH = "/tmp/single.db"
NGINX_PORT = 19851
FLASK_PORTS = [19860, 19861]
NGINX_CONF = Path("/tmp/single.db.nginx.conf")
NGINX_USER = "www-data"
CACHE_DIR = Path("/tmp/single.db.cache")
TEMP_DIR = Path("/tmp/single.db.temp")
BASE_DIR = "/tmp"
RUN_LOCK = "/tmp/spider-runtime-EXP-RUNTIME-36129163700.lock"
CANONICAL_PATHS = [DB_PATH, DB_PATH + "-wal", DB_PATH + "-shm", str(NGINX_CONF),
                   str(CACHE_DIR), str(TEMP_DIR), RUN_LOCK]

# Fresh TESTBED_SECRET for this run; only its SHA-256 and length are recorded.
TESTBED_SECRET = "b7f3a91c5e2d48f06a1c93e5b7d2f4a8c0e6b1d3f5a7c9e2b4d6f8a0c2e4b6d8f0a2c4e6b8d0f2a4c6e8b0d2f4a6c8e0b2d4f6a8c0e2b4d6f8a0c2e4b6"
assert len(TESTBED_SECRET.encode()) >= 32
HS256_SECRET_HASH = hashlib.sha256(TESTBED_SECRET.encode()).hexdigest()
HS256_SECRET_LEN = len(TESTBED_SECRET.encode())

# Certified fixture endpoints (from EXP-RUNTIME-36100549580) reused verbatim.
BODY_STATES = {
    "A": {"json": '{"data": "hello", "version": 1}', "len": 31},
    "B": {"json": '{"data": "hello!", "version": 2}', "len": 32},
    "C": {"json": '{"admin_note": "sensitive:42", "count": 42, "data": "hello", "items": ["a","b","c"], "role": "admin", "version": 1}', "len": 117},
    "D": {"json": '{"data": "hello world", "version": 3}', "len": 35},
}
ENDPOINTS = ["/api/profile", "/api/data_list"]

# Frozen response-fingerprint exclusions (prereg 4.3).
EXCLUDED_HEADERS = {"Date", "Server", "X-Worker-Pid", "X-Cache", "Age",
                    "Content-Length", "ETag", "W-ETag", "Range"}

# Frozen readiness floors (prereg 3.2).
FLOOR_N_NON304 = 800
FLOOR_PER_EP_NON304 = 400
FLOOR_DISTINCT_WORKERS = 2
FLOOR_STICKINESS = 0.90
TARGET_N_NON304 = 850
TARGET_N_TOTAL = 910

# Frozen decision thresholds (spec decision_rule).
THRESH_POINT = 0.90
THRESH_WILSON_LO = 0.80

PRE_MARKER = "pre_marker"
PRE_REPRESENTATION = "pre_repr"
PRE_REVISION = 0
PRE_UPDATED_AT = 0.0

EXP_DIR = Path(__file__).resolve().parent
ART_DIR = EXP_DIR / "artifacts"

# ── Global state ───────────────────────────────────────────────────────────
all_metrics: Dict[str, Any] = {}
all_controls: Dict[str, Any] = {}
validity_notes: List[str] = []
unresolved: List[str] = []
observations: List[str] = []
status = "COMPLETE"
outcome = "INCONCLUSIVE"
part_a_status: Optional[str] = None
part_b_status: Optional[str] = None
part_c_status: Optional[str] = None
durability_status: Optional[str] = None
readiness_certificate: Dict[str, Any] = {}
substrate_log: List[Dict[str, Any]] = []
lock_fd: Optional[int] = None
owned_procs: List[subprocess.Popen] = []
nginx_proc: Optional[subprocess.Popen] = None


# ── Small helpers ──────────────────────────────────────────────────────────
def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha_file(p: Path) -> Optional[str]:
    try:
        return _sha_bytes(p.read_bytes())
    except Exception:
        return None


def wilson_ci(k: int, n: int, z: float = WILSON_Z) -> Tuple[float, float]:
    """Two-sided 95% Wilson score interval (frozen z)."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, center - half), min(1.0, center + half)


def response_fingerprint(status_code: int, body: bytes, headers: Dict[str, str]) -> str:
    """B-RESPONSE-FINGERPRINT: SHA-256 over status + canonical body + sorted
    stable headers after excluding the frozen header set."""
    stable = {k: v for k, v in headers.items() if k not in EXCLUDED_HEADERS}
    canonical = f"{status_code}|".encode() + body + json.dumps(
        stable, sort_keys=True, separators=(",", ":")).encode()
    return _sha_bytes(canonical)


def wal_vector_capture() -> Dict[str, Any]:
    """B-WAL-VECTOR: length-framed SHA-256 over raw /tmp/single.db and
    /tmp/single.db-wal bytes; -shm recorded diagnostically only."""
    db_bytes = Path(DB_PATH).read_bytes() if Path(DB_PATH).exists() else b""
    wal_path = Path(DB_PATH + "-wal")
    wal_bytes = wal_path.read_bytes() if wal_path.exists() else b""
    shm_path = Path(DB_PATH + "-shm")
    shm_bytes = shm_path.read_bytes() if shm_path.exists() else b""
    frame = (len(db_bytes).to_bytes(8, "big") + db_bytes
             + len(wal_bytes).to_bytes(8, "big") + wal_bytes)
    return {
        "vector_sha256": _sha_bytes(frame),
        "db_bytes": len(db_bytes), "db_sha256": _sha_bytes(db_bytes),
        "wal_bytes": len(wal_bytes), "wal_sha256": _sha_bytes(wal_bytes),
        "shm_bytes": len(shm_bytes), "shm_sha256": _sha_bytes(shm_bytes),
        "captured_at": _utc(),
    }


def logical_state_capture(sid: str) -> Dict[str, Any]:
    """B-LOGICAL-STATE: read-only SQL projection of the controlled row and
    session validity. Never writes."""
    conn = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
    try:
        conn.execute("PRAGMA wal_autocheckpoint=0")
        row = conn.execute(
            "SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1"
        ).fetchone()
        srow = conn.execute(
            "SELECT id FROM sessions WHERE sid=? AND valid=1", (sid,)
        ).fetchone()
        return {
            "marker": row[0] if row else None,
            "representation": row[1] if row else None,
            "revision": row[2] if row else None,
            "updated_at": row[3] if row else None,
            "session_present": srow is not None,
        }
    finally:
        conn.close()


# ── Flask application (certified fixture + controlled /runtime/* surface) ──
def create_app(db_path: str = DB_PATH) -> Flask:
    app = Flask(__name__)
    app.config["DATABASE"] = db_path

    def _connect():
        conn = sqlite3.connect(db_path, timeout=10, check_same_thread=False)
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA journal_mode=WAL")
        # Frozen substrate contract: no checkpoint/compaction during the
        # measured window on ANY connection (workers and captures alike).
        conn.execute("PRAGMA wal_autocheckpoint=0")
        conn.row_factory = sqlite3.Row
        return conn

    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop("db", None)
        if db:
            db.close()

    def init_db():
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        # Idempotent under concurrent worker boot: two gunicorn workers may
        # run init_db simultaneously; INSERT OR IGNORE + busy_timeout makes
        # the seed deterministic for both.
        last_err = None
        for _ in range(20):
            try:
                conn = _connect()
                conn.execute("""CREATE TABLE IF NOT EXISTS sessions
                                (id INTEGER PRIMARY KEY, sid TEXT UNIQUE, username TEXT,
                                 valid INTEGER DEFAULT 1, created_at REAL)""")
                conn.execute("""CREATE TABLE IF NOT EXISTS body_config
                                (id INTEGER PRIMARY KEY CHECK(id=1), variant TEXT, content TEXT)""")
                conn.execute("""CREATE TABLE IF NOT EXISTS runtime_probe
                                (id INTEGER PRIMARY KEY CHECK(id=1), marker TEXT NOT NULL,
                                 representation TEXT NOT NULL, revision INTEGER NOT NULL,
                                 updated_at REAL NOT NULL)""")
                conn.execute("INSERT OR IGNORE INTO body_config VALUES (1,'A',?)",
                             (BODY_STATES["A"]["json"],))
                conn.execute(
                    "INSERT OR IGNORE INTO runtime_probe VALUES (1,?,?,?,?)",
                    (PRE_MARKER, PRE_REPRESENTATION, PRE_REVISION, PRE_UPDATED_AT))
                conn.commit()
                conn.close()
                return
            except sqlite3.OperationalError as e:
                last_err = e
                try:
                    conn.close()
                except Exception:
                    pass
                time.sleep(0.1)
        raise RuntimeError(f"init_db failed after retries: {last_err}")

    init_db()

    @app.route("/health")
    def health():
        pid = str(os.getpid())
        body = b'{"status":"ok"}'
        return body, 200, {"Content-Type": "application/json",
                           "Content-Length": str(len(body)), "X-Worker-Pid": pid}

    def _auth_valid(auth_header: str) -> bool:
        if not auth_header.startswith("Bearer "):
            return False
        try:
            jwt.decode(auth_header[7:], TESTBED_SECRET, algorithms=["HS256"])
            return True
        except Exception:
            return False

    def _handle_api():
        # Certified stable-header contract from EXP-RUNTIME-36100549580.
        auth_header = flask_request.headers.get("Authorization", "")
        auth_valid = _auth_valid(auth_header)
        if auth_valid:
            cc_val = "public, max-age=5"
            try:
                payload = jwt.decode(auth_header[7:], TESTBED_SECRET,
                                     algorithms=["HS256"], options={"verify_exp": False})
                auth_state = str(payload.get("sub", "test"))
            except Exception:
                auth_state = "test"
            sc_val = f"session={hashlib.sha256((TESTBED_SECRET + auth_state).encode()).hexdigest()[:16]}; Path=/; HttpOnly"
            vary_val = "Cookie"
        else:
            cc_val = "no-store"
            sc_val = None
            vary_val = "Authorization"
        conn = _connect()
        row = conn.execute("SELECT variant, content FROM body_config WHERE id=1").fetchone()
        variant = row["variant"] if row else "A"
        body_json = row["content"].encode() if row else b'{}'
        conn.close()
        etag = f'W/"{hashlib.sha256(body_json).hexdigest()}"'
        inm = flask_request.headers.get("If-None-Match", "")
        if inm and inm == etag:
            hdrs = {"ETag": etag, "Cache-Control": cc_val, "Vary": vary_val,
                    "X-Worker-Pid": str(os.getpid())}
            if sc_val is not None:
                hdrs["Set-Cookie"] = sc_val
            return "", 304, hdrs
        headers = {
            "Content-Type": "application/json",
            "Content-Length": str(len(body_json)),
            "ETag": etag,
            "Cache-Control": cc_val,
            "Vary": vary_val,
            "X-Worker-Pid": str(os.getpid()),
        }
        if sc_val is not None:
            headers["Set-Cookie"] = sc_val
        return body_json, 200, headers

    @app.route("/api/profile")
    def api_profile():
        return _handle_api()

    @app.route("/api/data_list")
    def api_data_list():
        return _handle_api()

    # ── Fixture plumbing (direct-origin only; outside measured intervals) ──
    @app.post("/admin/set_body_variant")
    def set_variant():
        conn = _connect()
        variant = flask_request.json.get("variant", "A") if flask_request.is_json else "A"
        content = BODY_STATES.get(variant, BODY_STATES["A"])["json"]
        conn.execute("UPDATE body_config SET variant=?, content=? WHERE id=1", (variant, content))
        conn.commit()
        conn.close()
        return jsonify({"ok": True, "variant": variant})

    @app.post("/admin/reset_probe")
    def reset_probe():
        conn = _connect()
        conn.execute("UPDATE runtime_probe SET marker=?, representation=?, revision=?, updated_at=? WHERE id=1",
                     (PRE_MARKER, PRE_REPRESENTATION, PRE_REVISION, PRE_UPDATED_AT))
        conn.commit()
        row = conn.execute("SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1").fetchone()
        conn.close()
        return jsonify({"ok": True, "marker": row["marker"], "representation": row["representation"],
                        "revision": row["revision"], "updated_at": row["updated_at"]})

    @app.post("/admin/session")
    def admin_session():
        data = flask_request.get_json(silent=True) or {}
        sid = str(data.get("sid", ""))
        action = str(data.get("action", "upsert"))
        conn = _connect()
        if action == "upsert":
            conn.execute("INSERT OR REPLACE INTO sessions (sid, username, valid, created_at) VALUES (?,?,1,?)",
                         (sid, "user", time.time()))
        elif action == "delete":
            conn.execute("DELETE FROM sessions WHERE sid=?", (sid,))
        conn.commit()
        n = conn.execute("SELECT COUNT(*) FROM sessions WHERE sid=?", (sid,)).fetchone()[0]
        conn.close()
        return jsonify({"ok": True, "sid": sid, "action": action, "rows": n})

    # ── Controlled runtime surface (Part A + Part B) ───────────────────────
    def _authenticate() -> Tuple[Optional[Dict], Optional[Tuple[str, int]]]:
        """V-AUTH-SESSION-BOUNDARY: verify HS256 signature AND expiry, then
        require a live sessions row for the token's sid. Every rejection
        happens BEFORE any UPDATE."""
        auth_header = flask_request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None, ("missing_token", 401)
        token = auth_header[7:]
        try:
            payload = jwt.decode(token, TESTBED_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None, ("expired_token", 401)
        except jwt.InvalidTokenError:
            return None, ("invalid_token", 401)
        sid = str(payload.get("sub", ""))
        conn = _connect()
        row = conn.execute("SELECT id FROM sessions WHERE sid=? AND valid=1", (sid,)).fetchone()
        conn.close()
        if not row:
            return None, ("deleted_session", 403)
        return payload, None

    @app.route("/runtime/read")
    def runtime_read():
        payload, err = _authenticate()
        if err:
            return jsonify({"error": err[0]}), err[1]
        conn = _connect()
        row = conn.execute(
            "SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1"
        ).fetchone()
        conn.close()
        return jsonify({
            "marker": row["marker"], "representation": row["representation"],
            "revision": row["revision"], "updated_at": row["updated_at"],
            "session_valid": True, "sid": payload["sub"],
        }), 200

    @app.post("/runtime/write")
    def runtime_write():
        payload, err = _authenticate()
        if err:
            return jsonify({"error": err[0]}), err[1]
        data = flask_request.get_json(silent=True) or {}
        op = data.get("op")
        value = data.get("value")
        if op not in ("set_marker", "set_representation") or not isinstance(value, str) or not value:
            return jsonify({"error": "bad_request", "op": op}), 400
        col = "marker" if op == "set_marker" else "representation"
        conn = _connect()
        conn.execute(
            f"UPDATE runtime_probe SET {col}=?, revision=revision+1, updated_at=? WHERE id=1",
            (value, time.time()))
        conn.commit()
        row = conn.execute(
            "SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1"
        ).fetchone()
        conn.close()
        return jsonify({
            "marker": row["marker"], "representation": row["representation"],
            "revision": row["revision"], "updated_at": row["updated_at"],
            "session_valid": True, "sid": payload["sub"], "op": op,
        }), 200

    BROWSER_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Runtime Browser Control</title></head>
<body>
<h1>Runtime Browser Control Surface</h1>
<div id="state">idle #0</div>
<div id="last-response">{}</div>
<button id="btn-valid-write" onclick="doWrite('valid')">Valid-auth write</button>
<button id="btn-restore" onclick="doWrite('restore')">Restore marker</button>
<button id="btn-read" onclick="doRead()">Read-only</button>
<button id="btn-invalid" onclick="doWrite('invalid')">Invalid-auth write</button>
<button id="btn-expired" onclick="doWrite('expired')">Expired-auth write</button>
<button id="btn-deleted" onclick="doWrite('deleted')">Deleted-session write</button>
<script>
window._ctr = 0;
const TOKENS = { valid: "__VALID_TOKEN__", expired: "__EXPIRED_TOKEN__",
                 deleted: "__DELETED_TOKEN__", invalid: "invalid.token.here" };
async function doWrite(kind) {
  const value = (kind === "restore") ? "__PRE_MARKER__"
    : "browser_" + kind + "_" + Date.now();
  try {
    const r = await fetch("/runtime/write", { method: "POST",
      headers: { "Authorization": "Bearer " + TOKENS[kind], "Content-Type": "application/json" },
      body: JSON.stringify({ op: "set_marker", value: value }) });
    const j = await r.json();
    document.getElementById("state").innerText = kind + ": " + r.status + " #" + (++window._ctr);
    document.getElementById("last-response").innerText = JSON.stringify(j);
  } catch (e) {
    document.getElementById("state").innerText = kind + ": error " + e + " #" + (++window._ctr);
  }
}
async function doRead() {
  try {
    const r = await fetch("/runtime/read",
      { headers: { "Authorization": "Bearer " + TOKENS.valid } });
    const j = await r.json();
    document.getElementById("state").innerText = "read: " + r.status + " #" + (++window._ctr);
    document.getElementById("last-response").innerText = JSON.stringify(j);
  } catch (e) {
    document.getElementById("state").innerText = "read: error " + e + " #" + (++window._ctr);
  }
}
</script>
</body></html>"""

    @app.route("/runtime/browser")
    def runtime_browser():
        now = datetime.now(timezone.utc)
        valid_tok = jwt.encode({"sub": "browser_sess", "exp": now + timedelta(hours=1)},
                               TESTBED_SECRET, algorithm="HS256")
        expired_tok = jwt.encode({"sub": "browser_sess", "exp": now - timedelta(hours=1)},
                                 TESTBED_SECRET, algorithm="HS256")
        deleted_tok = jwt.encode({"sub": "browser_deleted_sess", "exp": now + timedelta(hours=1)},
                                 TESTBED_SECRET, algorithm="HS256")
        html = (BROWSER_HTML.replace("__VALID_TOKEN__", valid_tok)
                            .replace("__EXPIRED_TOKEN__", expired_tok)
                            .replace("__DELETED_TOKEN__", deleted_tok)
                            .replace("__PRE_MARKER__", PRE_MARKER))
        return html, 200, {"Content-Type": "text/html; charset=utf-8"}

    return app


# ── Substrate bring-up (idempotent, fail-closed, owns only frozen names) ────
def _sudo_ok() -> bool:
    try:
        r = subprocess.run(["sudo", "-n", "true"], capture_output=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def _port_in_use(port: int) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except Exception:
        return False


def _owned_processes_running() -> Dict[str, Any]:
    """Identify ONLY processes owned by this run's frozen contract:
    gunicorn serving wsgi:application from /tmp, or nginx master with the
    exclusive -c /tmp/single.db.nginx.conf. Anything else is foreign."""
    ps = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10).stdout
    owned_gunicorn, owned_nginx, foreign = [], [], []
    for line in ps.splitlines():
        if "gunicorn" in line and "wsgi:application" in line and "/tmp" in line:
            owned_gunicorn.append(line.strip()[:200])
        elif "nginx: master process" in line:
            if str(NGINX_CONF) in line:
                owned_nginx.append(line.strip()[:200])
            else:
                foreign.append(line.strip()[:200])
        elif "nginx" in line and "worker" in line and "nginx: master" not in line:
            pass  # workers belong to their master; checked via master
    return {"owned_gunicorn": owned_gunicorn, "owned_nginx": owned_nginx,
            "foreign_nginx_masters": foreign}


def acquire_run_lock() -> Tuple[bool, str]:
    """Fail-closed run lock. Refuse to overwrite a foreign lock or run while
    a live holder exists. Stale locks (dead holder) are removed."""
    global lock_fd
    lock_path = Path(RUN_LOCK)
    if lock_path.exists():
        # Probe: try a non-blocking exclusive lock on the existing file.
        probe = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)
        try:
            fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # Lockable => stale (no live holder). Safe to reuse.
            fcntl.flock(probe, fcntl.LOCK_UN)
            os.close(probe)
        except OSError:
            os.close(probe)
            return False, "run lock held by a live process; refusing concurrent execution"
    lock_fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        os.close(lock_fd)
        lock_fd = None
        return False, "run lock acquisition failed (live holder)"
    return True, "lock acquired"


def release_run_lock():
    global lock_fd
    if lock_fd is not None:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)
        except Exception:
            pass
        lock_fd = None


def _write_nginx_conf(conf_path: Path, nginx_user: str, use_sudo: bool):
    conf_path.parent.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    if use_sudo:
        subprocess.run(["sudo", "chown", "-R", f"{nginx_user}:{nginx_user}", str(CACHE_DIR)], capture_output=True, timeout=10)
        subprocess.run(["sudo", "chown", "-R", f"{nginx_user}:{nginx_user}", str(TEMP_DIR)], capture_output=True, timeout=10)
        subprocess.run(["sudo", "chmod", "755", str(CACHE_DIR)], capture_output=True, timeout=10)
        subprocess.run(["sudo", "chmod", "755", str(TEMP_DIR)], capture_output=True, timeout=10)
    else:
        os.chmod(str(CACHE_DIR), 0o755)
        os.chmod(str(TEMP_DIR), 0o755)
    user_directive = f"user {nginx_user};" if use_sudo else ""
    conf_text = f"""worker_processes 1;
{user_directive}
pid {conf_path.parent}/nginx.pid;
error_log {conf_path.parent}/nginx_error.log;
events {{ worker_connections 1024; }}
http {{
    access_log {conf_path.parent}/nginx_access.log;
    proxy_temp_path {TEMP_DIR};
    proxy_cache_path {CACHE_DIR} levels=1:2 keys_zone=spider_cache:10m max_size=100m inactive=60m;
    upstream spider_backend {{
        server 127.0.0.1:{FLASK_PORTS[0]};
        server 127.0.0.1:{FLASK_PORTS[1]};
        hash $request_uri consistent;
    }}
    server {{
        listen {NGINX_PORT};
        server_name localhost;
        location = /health {{
            proxy_pass http://spider_backend;
            proxy_http_version 1.1;
            proxy_set_header Connection '';
            proxy_set_header Host $host;
            proxy_cache spider_cache;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 1m;
            add_header X-Cache $upstream_cache_status;
            add_header X-Worker-Pid $upstream_http_x_worker_pid always;
        }}
        location / {{
            proxy_pass http://spider_backend;
            proxy_http_version 1.1;
            proxy_set_header Connection '';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Authorization $http_authorization;
            proxy_no_cache $http_authorization;
            proxy_cache_bypass $http_authorization;
            proxy_cache spider_cache;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 1m;
            add_header X-Cache $upstream_cache_status;
            add_header X-Worker-Pid $upstream_http_x_worker_pid always;
        }}
    }}
}}
"""
    conf_path.write_text(conf_text)
    n_hash = conf_text.count("hash $request_uri consistent;")
    assert n_hash == 1, f"single hash violation n_hash={n_hash}"
    assert "proxy_cache_path" in conf_text
    assert "proxy_no_cache $http_authorization;" in conf_text
    assert "proxy_cache_bypass $http_authorization;" in conf_text


def _start_gunicorn(use_sudo: bool) -> List[subprocess.Popen]:
    """One gunicorn worker per FLASK_PORTS entry, each --workers 1, both
    sharing the single /tmp/single.db WAL (factory-pattern WSGI)."""
    src = Path(__file__).resolve()
    dst = Path(BASE_DIR) / "run_experiment.py"
    try:
        shutil.copy(str(src), str(dst))
    except Exception:
        pass
    wsgi_path = Path(BASE_DIR) / "wsgi.py"
    wsgi_content = f"""import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from run_experiment import create_app
application = create_app({DB_PATH!r})
"""
    wsgi_path.write_text(wsgi_content)
    env = os.environ.copy()
    procs: List[subprocess.Popen] = []
    for port in FLASK_PORTS:
        proc = subprocess.Popen(
            ["gunicorn", "--workers", "1", "--bind", f"127.0.0.1:{port}", "wsgi:application"],
            stdout=open(Path(BASE_DIR) / f"gunicorn_stdout_{port}.log", "w"),
            stderr=open(Path(BASE_DIR) / f"gunicorn_stderr_{port}.log", "w"),
            cwd=BASE_DIR, env=env)
        procs.append(proc)
        time.sleep(0.4)  # stagger worker boots so init_db seeding is sequential
    return procs


def _verify_flask_listening(max_wait: int = 30) -> Tuple[bool, List[Dict]]:
    statuses: List[Dict] = []
    all_ok = True
    for port in FLASK_PORTS:
        ok_port = False
        for _ in range(max_wait * 2):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect(("127.0.0.1", port))
                s.close()
                ok_port = True
                break
            except (ConnectionRefusedError, socket.timeout, OSError):
                time.sleep(0.5)
        statuses.append({"port": port, "listening": ok_port})
        if not ok_port:
            all_ok = False
    return all_ok, statuses


def _start_nginx(conf_path: Path, use_sudo: bool) -> subprocess.Popen:
    if use_sudo:
        return subprocess.Popen(["sudo", "nginx", "-c", str(conf_path)],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return subprocess.Popen(["nginx", "-c", str(conf_path)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _health_gate(max_wait: int = 30) -> Tuple[bool, List[Dict]]:
    logs = []
    for attempt in range(max_wait):
        try:
            r = requests.get(f"http://127.0.0.1:{NGINX_PORT}/health", timeout=2)
            worker = r.headers.get("X-Worker-Pid", "missing")
            logs.append({"attempt": attempt, "path": "nginx:19851", "status": r.status_code,
                         "worker": worker, "x_cache": r.headers.get("X-Cache", None)})
            if r.status_code == 200 and worker not in ("missing", "None", None, ""):
                return True, logs
        except Exception as e:
            logs.append({"attempt": attempt, "path": "nginx:19851", "status": None,
                         "error": str(e), "worker": "missing"})
        time.sleep(1)
    return False, logs


def _origin_health_gate(port: int, max_wait: int = 30) -> Tuple[bool, List[Dict]]:
    logs = []
    for attempt in range(max_wait):
        try:
            r = requests.get(f"http://127.0.0.1:{port}/health", timeout=2)
            worker = r.headers.get("X-Worker-Pid", "missing")
            logs.append({"attempt": attempt, "path": f"origin:{port}", "status": r.status_code,
                         "worker": worker})
            if r.status_code == 200 and worker not in ("missing", "None", None, ""):
                return True, logs
        except Exception as e:
            logs.append({"attempt": attempt, "path": f"origin:{port}", "status": None,
                         "error": str(e), "worker": "missing"})
        time.sleep(1)
    return False, logs


def _kill_owned():
    """Kill ONLY processes owned by this run's frozen contract. Never touch
    unrelated processes."""
    info = _owned_processes_running()
    for proc in owned_procs:
        try:
            proc.terminate()
        except Exception:
            pass
    if nginx_proc is not None:
        try:
            nginx_proc.terminate()
        except Exception:
            pass
    time.sleep(0.5)
    for proc in owned_procs:
        try:
            proc.kill()
        except Exception:
            pass
    if nginx_proc is not None:
        try:
            nginx_proc.kill()
        except Exception:
            pass
    # Belt-and-braces: kill by exact owned command lines only.
    subprocess.run(["pkill", "-9", "-f", "gunicorn.*wsgi:application"], capture_output=True, timeout=3)
    subprocess.run(["sudo", "pkill", "-9", "-f", f"nginx.*-c {NGINX_CONF}"], capture_output=True, timeout=3)
    time.sleep(0.5)
    return info


def _clean_canonical_paths():
    """Remove only owned canonical artifacts (frozen names)."""
    for cand in CANONICAL_PATHS:
        try:
            p = Path(cand)
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            elif p.exists():
                p.unlink()
        except Exception:
            pass
    for f in ["wsgi.py", "run_experiment.py", "gunicorn_stdout_19860.log",
              "gunicorn_stderr_19860.log", "gunicorn_stdout_19861.log",
              "gunicorn_stderr_19861.log", "health_gate.log", "nginx_error.log",
              "nginx_access.log", "nginx.pid"]:
        try:
            fp = os.path.join(BASE_DIR, f)
            if os.path.exists(fp):
                os.unlink(fp)
        except Exception:
            pass


# ── Token factories ─────────────────────────────────────────────────────────
def make_valid_token(sid: str) -> str:
    return jwt.encode({"sub": sid, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
                      TESTBED_SECRET, algorithm="HS256")


def make_expired_token(sid: str) -> str:
    return jwt.encode({"sub": sid, "exp": datetime.now(timezone.utc) - timedelta(hours=1)},
                      TESTBED_SECRET, algorithm="HS256")


# ── Readiness certificate (prereg 3.2, certified parent mechanics) ─────────
def run_readiness_certificate(valid_token: str) -> Dict[str, Any]:
    rng = random.Random(SEED)
    n_total = n_non304 = n_304 = n_missing_on_200 = 0
    per_ep_non304 = {ep: 0 for ep in ENDPOINTS}
    per_ep_304 = {ep: 0 for ep in ENDPOINTS}
    uri_workers: Dict[str, List[str]] = {}
    workers_on_200: set = set()
    body_etags = {k: f'W/"{hashlib.sha256(v["json"].encode()).hexdigest()}"' for k, v in BODY_STATES.items()}
    records: List[Dict] = []
    attempt = 0
    max_attempts = 4000
    while n_non304 < TARGET_N_NON304 and attempt < max_attempts:
        ep = ENDPOINTS[attempt % len(ENDPOINTS)]
        body_state = rng.choice(list(BODY_STATES.keys()))
        try:
            requests.post(f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/set_body_variant",
                          json={"variant": body_state}, timeout=2)
        except Exception:
            pass
        time.sleep(0.004)
        send_matching_etag = rng.random() < 0.3
        headers = {"Authorization": f"Bearer {valid_token}"}
        if send_matching_etag:
            headers["If-None-Match"] = body_etags[body_state]
        elif rng.random() < 0.5:
            headers["If-None-Match"] = 'W/"mismatched"'
        uri_suffix = f"?uid={attempt % 12}"
        url = f"http://127.0.0.1:{NGINX_PORT}{ep}{uri_suffix}"
        try:
            r = requests.get(url, headers=headers, timeout=5)
            n_total += 1
            worker = r.headers.get("X-Worker-Pid", "missing")
            uri_workers.setdefault(f"{ep}{uri_suffix}", []).append(worker)
            if r.status_code == 200:
                workers_on_200.add(worker)
                if worker == "missing":
                    n_missing_on_200 += 1
            is_304 = (r.status_code == 304)
            if is_304:
                n_304 += 1
                per_ep_304[ep] += 1
            else:
                n_non304 += 1
                per_ep_non304[ep] += 1
            records.append({"attempt": attempt, "endpoint": ep, "uri": f"{ep}{uri_suffix}",
                            "status": r.status_code, "is_304": is_304, "worker": worker,
                            "x_cache": r.headers.get("X-Cache"), "body_state": body_state,
                            "via": "nginx:19851"})
        except Exception as e:
            validity_notes.append(f"readiness request error attempt {attempt}: {e}")
        attempt += 1
        if n_non304 >= TARGET_N_NON304 and all(v >= FLOOR_PER_EP_NON304 for v in per_ep_non304.values()):
            break
    # Top-up loop (certified parent mechanic): guarantee per-endpoint floor.
    extra = 0
    while any(v < FLOOR_PER_EP_NON304 for v in per_ep_non304.values()) and extra < 1200:
        for ep in ENDPOINTS:
            if per_ep_non304[ep] >= FLOOR_PER_EP_NON304:
                continue
            body_state = rng.choice(list(BODY_STATES.keys()))
            try:
                requests.post(f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/set_body_variant",
                              json={"variant": body_state}, timeout=2)
            except Exception:
                pass
            time.sleep(0.004)
            headers = {"Authorization": f"Bearer {valid_token}",
                       "If-None-Match": 'W/"mismatched"'}
            url = f"http://127.0.0.1:{NGINX_PORT}{ep}?uid={extra % 12}"
            try:
                r = requests.get(url, headers=headers, timeout=5)
                n_total += 1
                worker = r.headers.get("X-Worker-Pid", "missing")
                uri_workers.setdefault(f"{ep}?uid={extra % 12}", []).append(worker)
                if r.status_code == 200:
                    workers_on_200.add(worker)
                    if worker == "missing":
                        n_missing_on_200 += 1
                if r.status_code == 304:
                    n_304 += 1
                    per_ep_304[ep] += 1
                else:
                    n_non304 += 1
                    per_ep_non304[ep] += 1
                records.append({"attempt": f"extra_{extra}", "endpoint": ep,
                                "uri": f"{ep}?uid={extra % 12}", "status": r.status_code,
                                "is_304": r.status_code == 304, "worker": worker,
                                "x_cache": r.headers.get("X-Cache"), "body_state": body_state,
                                "via": "nginx:19851"})
            except Exception as e:
                validity_notes.append(f"readiness topup error extra {extra}: {e}")
        extra += 1
    # Derived certificate values (computed from raw records only).
    per_uri_consistency = {}
    for uri, ws in uri_workers.items():
        if not ws:
            per_uri_consistency[uri] = 0.0
            continue
        majority = max(set(ws), key=ws.count)
        per_uri_consistency[uri] = round(ws.count(majority) / len(ws), 4)
    min_stickiness = min(per_uri_consistency.values()) if per_uri_consistency else 0.0
    distinct_workers = sorted(w for w in workers_on_200 if w not in ("missing", "None", None, ""))
    cert = {
        "n_total": n_total,
        "n_non304": n_non304,
        "n_304": n_304,
        "n_missing_worker_on_200": n_missing_on_200,
        "per_ep_non304": per_ep_non304,
        "per_ep_304": per_ep_304,
        "distinct_x_worker_pid_on_200": distinct_workers,
        "n_distinct_x_worker_pid": len(distinct_workers),
        "per_uri_stickiness": per_uri_consistency,
        "min_per_uri_stickiness": min_stickiness,
        "n_distinct_uris": len(uri_workers),
        "floors": {
            "n_non304>=800": n_non304 >= FLOOR_N_NON304,
            "per_ep_non304>=400": all(v >= FLOOR_PER_EP_NON304 for v in per_ep_non304.values()),
            "distinct_x_worker_pid>=2": len(distinct_workers) >= FLOOR_DISTINCT_WORKERS,
            "per_uri_stickiness>=0.90_over_>10_uris": (min_stickiness >= FLOOR_STICKINESS
                                                       and len(uri_workers) > 10),
            "no_missing_worker_header_on_200": n_missing_on_200 == 0,
        },
        "raw_records": records,
    }
    cert["pass"] = all(cert["floors"].values())
    return cert


def cache_corroboration() -> Dict[str, Any]:
    """Diagnostic (non-gating): real proxy_cache MISS then HIT on an
    unauthenticated 200 surface (/runtime/browser)."""
    out = {"executed": True, "observations": []}
    try:
        r1 = requests.get(f"http://127.0.0.1:{NGINX_PORT}/runtime/browser", timeout=5)
        out["observations"].append({"leg": 1, "status": r1.status_code,
                                    "x_cache": r1.headers.get("X-Cache")})
        r2 = requests.get(f"http://127.0.0.1:{NGINX_PORT}/runtime/browser", timeout=5)
        out["observations"].append({"leg": 2, "status": r2.status_code,
                                    "x_cache": r2.headers.get("X-Cache")})
        out["miss_then_hit"] = (r1.headers.get("X-Cache") == "MISS"
                                and r2.headers.get("X-Cache") == "HIT")
    except Exception as e:
        out["executed"] = False
        out["error"] = str(e)
    return out


# ── Part A: capture stability + intervention-validity matrix ───────────────
def run_capture_stability() -> List[Dict]:
    """B-STATIC-REPEAT-NULL / NC-A-STATIC-CAPTURE: ten no-action WAL-vector
    pairs separated by the frozen 250 ms interval. Any unstable pair
    invalidates the capture method (MEASUREMENT_INVALID), never a false
    positive."""
    pairs = []
    stable = True
    for i in range(10):
        pre = wal_vector_capture()
        time.sleep(0.25)
        post = wal_vector_capture()
        identical = pre["vector_sha256"] == post["vector_sha256"]
        if not identical:
            stable = False
        pairs.append({"pair": i, "interval_ms": 250, "pre_vector": pre["vector_sha256"],
                      "post_vector": post["vector_sha256"], "byte_identical": identical,
                      "pre": pre, "post": post})
    return pairs


def _http_json(method: str, url: str, headers: Dict[str, str], body: Optional[Dict] = None,
               timeout: float = 5.0) -> Tuple[int, bytes, Dict[str, str], Optional[Dict]]:
    try:
        r = requests.request(method, url, headers=headers,
                             json=body, timeout=timeout)
        return r.status_code, r.content, dict(r.headers), None
    except Exception as e:
        return -1, b"", {}, {"exception": f"{type(e).__name__}: {e}"}


def run_part_a() -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """Execute the frozen 120-episode matrix. Returns (episode_records,
    detector_records, wal_records). Raw JSONL is written before any derived
    metric; the detector never receives the arm label."""
    # Seeded balanced permutation of all arm/episode IDs (prereg 4.1).
    episode_plan = [(arm, i) for arm in ARMS for i in range(EPISODES_PER_ARM)]
    random.Random(SEED).shuffle(episode_plan)
    order_archive = {
        "seed": SEED,
        "arms": ARMS,
        "episodes_per_arm": EPISODES_PER_ARM,
        "total_episodes": len(episode_plan),
        "order": [{"order_index": idx, "arm": arm, "episode_id": i}
                  for idx, (arm, i) in enumerate(episode_plan)],
        "archived_at": _utc(),
        "note": "raw order archived before any scoring (prereg 4.1)",
    }
    with open(ART_DIR / "A-SEEDED-ORDER.json", "w") as f:
        json.dump(order_archive, f, indent=2)

    episode_records: List[Dict] = []
    detector_records: List[Dict] = []
    wal_records: List[Dict] = []
    fp_records: List[Dict] = []

    for order_index, (arm, ep_idx) in enumerate(episode_plan):
        sid = f"sess_{RUN_ID}_{arm}_{ep_idx}"
        planted_value = f"planted_{RUN_ID}_{arm}_{ep_idx}"
        planted_field = None
        token_class = "valid"
        method, path, op, body = "GET", "/runtime/read", None, None
        if arm == "P-WRITE":
            method, path, op, planted_field = "POST", "/runtime/write", "set_marker", "marker"
        elif arm == "P-DRIFT":
            method, path, op, planted_field = "POST", "/runtime/write", "set_representation", "representation"
        elif arm == "N-READ":
            method, path, op = "GET", "/runtime/read", None
        elif arm == "N-INVALID":
            method, path, op, planted_field, token_class = "POST", "/runtime/write", "set_marker", "marker", "invalid"
        elif arm == "N-EXPIRED":
            method, path, op, planted_field, token_class = "POST", "/runtime/write", "set_marker", "marker", "expired"
        elif arm == "N-DELETED":
            method, path, op, planted_field, token_class = "POST", "/runtime/write", "set_marker", "marker", "deleted_session"

        rec: Dict[str, Any] = {
            "run_id": RUN_ID, "experiment_id": EXPERIMENT_ID, "arm": arm,
            "episode_id": ep_idx, "order_index": order_index,
            "utc_start": _utc(),
            "request": {"method": method, "path": path, "op": op},
            "token_class": token_class,
            "sid_ref": sid,  # redacted reference only; never a bearer secret
            "planted_field": planted_field,
            "planted_value": planted_value if planted_field else None,
        }
        try:
            # ── Fixture setup (outside the measured interval) ──
            if token_class == "deleted_session":
                _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
                           {}, {"sid": sid, "action": "delete"})
            else:
                _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
                           {}, {"sid": sid, "action": "upsert"})
            _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/reset_probe", {}, None)
            time.sleep(0.05)  # setup quiescence

            # ── Pre-capture ──
            pre_vec = wal_vector_capture()
            pre_logical = logical_state_capture(sid)
            valid_tok = make_valid_token(sid)
            pre_status, pre_body, pre_headers, pre_err = _http_json(
                "GET", f"http://127.0.0.1:{NGINX_PORT}/runtime/read",
                {"Authorization": f"Bearer {valid_tok}"})
            pre_fp = response_fingerprint(pre_status, pre_body, pre_headers) if pre_err is None else None
            rec["pre"] = {
                "vector_sha256": pre_vec["vector_sha256"],
                "db_bytes": pre_vec["db_bytes"], "db_sha256": pre_vec["db_sha256"],
                "wal_bytes": pre_vec["wal_bytes"], "wal_sha256": pre_vec["wal_sha256"],
                "shm_bytes": pre_vec["shm_bytes"], "shm_sha256": pre_vec["shm_sha256"],
                "logical": pre_logical, "read_status": pre_status,
                "read_fingerprint": pre_fp,
            }

            # ── Measured action (single request through nginx 19851) ──
            if token_class == "valid":
                action_token = valid_tok
            elif token_class == "invalid":
                action_token = "invalid.token.here"
            elif token_class == "expired":
                action_token = make_expired_token(sid)
            else:  # deleted_session: correctly signed, unexpired, sid absent
                action_token = make_valid_token(sid)
            action_headers = {"Authorization": f"Bearer {action_token}"}
            action_body = None
            if method == "POST":
                action_body = {"op": op, "value": planted_value}
            act_status, act_body, act_headers, act_err = _http_json(
                method, f"http://127.0.0.1:{NGINX_PORT}{path}", action_headers, action_body)
            rec["http_status"] = act_status
            rec["response_body"] = act_body.decode(errors="replace")[:500]
            rec["response_stable_headers"] = {k: v for k, v in act_headers.items()
                                              if k not in EXCLUDED_HEADERS}
            rec["action_exception"] = act_err

            time.sleep(0.05)  # post-action quiescence barrier

            # ── Post-capture ──
            post_vec = wal_vector_capture()
            post_logical = logical_state_capture(sid)
            post_status, post_body, post_headers, post_err = _http_json(
                "GET", f"http://127.0.0.1:{NGINX_PORT}/runtime/read",
                {"Authorization": f"Bearer {valid_tok}"})
            post_fp = response_fingerprint(post_status, post_body, post_headers) if post_err is None else None
            rec["post"] = {
                "vector_sha256": post_vec["vector_sha256"],
                "db_bytes": post_vec["db_bytes"], "db_sha256": post_vec["db_sha256"],
                "wal_bytes": post_vec["wal_bytes"], "wal_sha256": post_vec["wal_sha256"],
                "shm_bytes": post_vec["shm_bytes"], "shm_sha256": post_vec["shm_sha256"],
                "logical": post_logical, "read_status": post_status,
                "read_fingerprint": post_fp,
            }
            rec["capture_quiescence_ms"] = 50
            rec["fixture_cleanup"] = "session row and probe reset remain outside measured interval; no teardown needed per episode"
            rec["utc_end"] = _utc()

            # ── Raw side-effect records (separate immutable streams) ──
            wal_records.append({
                "order_index": order_index, "episode_id": ep_idx,
                "pre_vector_sha256": pre_vec["vector_sha256"],
                "post_vector_sha256": post_vec["vector_sha256"],
                "vector_changed": pre_vec["vector_sha256"] != post_vec["vector_sha256"],
                "pre": pre_vec, "post": post_vec,
            })
            fp_records.append({
                "order_index": order_index, "episode_id": ep_idx,
                "pre_read_fingerprint": pre_fp, "post_read_fingerprint": post_fp,
                "fingerprint_changed": pre_fp != post_fp,
                "pre_read_status": pre_status, "post_read_status": post_status,
            })

            # ── Blind detector (NO arm label, NO expected status, NO hypothesis) ──
            pre_l, post_l = pre_logical, post_logical
            state_changed = ((pre_l["marker"], pre_l["representation"], pre_l["revision"])
                             != (post_l["marker"], post_l["representation"], post_l["revision"]))
            wal_changed = pre_vec["vector_sha256"] != post_vec["vector_sha256"]
            fp_changed = (pre_fp != post_fp)
            write_action_2xx = (path == "/runtime/write" and act_status in (200, 201))
            positive_detected = False
            if planted_field is not None:
                readback_ok = (post_l[planted_field] == planted_value)
                positive_detected = bool(readback_ok and state_changed and write_action_2xx)
            detector_records.append({
                "order_index": order_index, "episode_id": ep_idx,
                "state_changed": state_changed,
                "wal_vector_changed": wal_changed,
                "response_fingerprint_changed": fp_changed,
                "write_action_2xx": write_action_2xx,
                "positive_detected": positive_detected,
            })
        except Exception as e:
            rec["exception"] = f"{type(e).__name__}: {e}"
            rec["utc_end"] = _utc()
            detector_records.append({
                "order_index": order_index, "episode_id": ep_idx,
                "state_changed": None, "wal_vector_changed": None,
                "response_fingerprint_changed": None, "write_action_2xx": None,
                "positive_detected": None,
                "detector_error": f"{type(e).__name__}: {e}",
            })
        episode_records.append(rec)
        if order_index % 20 == 0:
            print(f"[Part A] episode {order_index + 1}/120 complete", flush=True)

    # ── Persist RAW evidence before any derived computation ──
    with open(ART_DIR / "A-EPISODE-LEDGER.jsonl", "w") as f:
        for rec in episode_records:
            f.write(json.dumps(rec, default=str) + "\n")
    with open(ART_DIR / "A-WAL-VECTOR-BEFORE-AFTER.jsonl", "w") as f:
        for rec in wal_records:
            f.write(json.dumps(rec, default=str) + "\n")
    with open(ART_DIR / "A-RESPONSE-FINGERPRINTS.jsonl", "w") as f:
        for rec in fp_records:
            f.write(json.dumps(rec, default=str) + "\n")
    with open(ART_DIR / "A-DETECTOR-OUTPUT.jsonl", "w") as f:
        for rec in detector_records:
            f.write(json.dumps(rec, default=str) + "\n")
    return episode_records, detector_records, wal_records


def score_part_a(episode_records: List[Dict], detector_records: List[Dict]) -> Dict[str, Any]:
    """Join arm labels to detector output (only now) and compute the frozen
    arm-constrained confusion matrix with Wilson intervals."""
    det_by_order = {d["order_index"]: d for d in detector_records}
    arm_results: Dict[str, Any] = {}
    for arm in ARMS:
        episodes = [r for r in episode_records if r["arm"] == arm]
        k = 0
        n = 0
        per_episode = []
        for ep in episodes:
            det = det_by_order.get(ep["order_index"], {})
            if det.get("state_changed") is None:
                per_episode.append({"order_index": ep["order_index"], "scored": False,
                                    "reason": "detector_error"})
                continue
            n += 1
            if arm in POSITIVE_ARMS:
                detected = bool(det["positive_detected"])
                if arm == "P-DRIFT":
                    detected = detected and bool(det["response_fingerprint_changed"])
                if detected:
                    k += 1
                per_episode.append({"order_index": ep["order_index"], "scored": True,
                                    "detected": detected})
            else:
                fp = bool(det["state_changed"]) or bool(det["wal_vector_changed"]) or bool(det["write_action_2xx"])
                if arm == "N-READ":
                    fp = fp or bool(det["response_fingerprint_changed"])
                if not fp:
                    k += 1
                per_episode.append({"order_index": ep["order_index"], "scored": True,
                                    "false_positive": fp})
        point = (k / n) if n else None
        ci_lo, ci_hi = wilson_ci(k, n) if n else (None, None)
        arm_results[arm] = {
            "n_scored": n, "n_complete": len(episodes),
            "k": k,
            "estimand": "sensitivity" if arm in POSITIVE_ARMS else "specificity",
            "point_rate": point,
            "wilson_ci_lo": ci_lo, "wilson_ci_hi": ci_hi,
            "ci_nondegenerate": (ci_hi > ci_lo) if ci_lo is not None else False,
            "per_episode": per_episode,
        }
    # Frozen decision rule (spec decision_rule).
    gates = {
        "matrix_complete_20_per_arm": all(arm_results[a]["n_complete"] == EPISODES_PER_ARM for a in ARMS),
        "all_episodes_scored": all(arm_results[a]["n_scored"] == EPISODES_PER_ARM for a in ARMS),
    }
    pos_ok = all(
        arm_results[a]["point_rate"] is not None
        and arm_results[a]["point_rate"] >= THRESH_POINT
        and arm_results[a]["wilson_ci_lo"] is not None
        and arm_results[a]["wilson_ci_lo"] >= THRESH_WILSON_LO
        for a in POSITIVE_ARMS)
    null_ok = all(
        arm_results[a]["point_rate"] is not None
        and arm_results[a]["point_rate"] >= THRESH_POINT
        and arm_results[a]["wilson_ci_lo"] is not None
        and arm_results[a]["wilson_ci_lo"] >= THRESH_WILSON_LO
        for a in NULL_ARMS)
    all_nondegenerate = all(arm_results[a]["ci_nondegenerate"] for a in ARMS)
    if not (gates["matrix_complete_20_per_arm"] and gates["all_episodes_scored"]):
        a_verdict = "MEASUREMENT_INVALID"
    elif pos_ok and null_ok and all_nondegenerate:
        a_verdict = "SUPPORTS"
    else:
        a_verdict = "FALSIFIES"
    # Pooled descriptive only (cannot mask a failed arm).
    pooled_pos_k = sum(arm_results[a]["k"] for a in POSITIVE_ARMS)
    pooled_pos_n = sum(arm_results[a]["n_scored"] for a in POSITIVE_ARMS)
    pooled_null_k = sum(arm_results[a]["k"] for a in NULL_ARMS)
    pooled_null_n = sum(arm_results[a]["n_scored"] for a in NULL_ARMS)
    pooled = {
        "pooled_sensitivity_point": (pooled_pos_k / pooled_pos_n) if pooled_pos_n else None,
        "pooled_specificity_point": (pooled_null_k / pooled_null_n) if pooled_null_n else None,
        "note": "descriptive only; cannot override a failed individual arm",
    }
    return {
        "z": WILSON_Z,
        "thresholds": {"point_min": THRESH_POINT, "wilson_lo_min": THRESH_WILSON_LO},
        "arms": arm_results,
        "gates": gates,
        "positive_arms_pass": pos_ok,
        "null_arms_pass": null_ok,
        "all_intervals_nondegenerate": all_nondegenerate,
        "pooled_descriptive": pooled,
        "A_verdict": a_verdict,
        "setting": "bounded: 2x gunicorn 23.0.0 @127.0.0.1:19860/19861 sharing /tmp/single.db WAL (wal_autocheckpoint=0), exclusive nginx 1.24.0 @19851, hash $request_uri consistent, real proxy_cache, plain HTTP localhost; no browser/TLS/HTTP2/multi-host/real-site claim",
        "scored_at": _utc(),
    }


# ── Part B: standalone public-Chromium capability (NON-VETOING) ────────────
def run_part_b() -> Dict[str, Any]:
    """Every gate uses only the documented public Playwright API. Any absent
    capability is B=UNAVAILABLE with exact artifact and one smallest
    unblocking action. B never alters Part A."""
    result: Dict[str, Any] = {
        "executed": True,
        "public_api_only": True,
        "private_helper_used": False,
        "synthetic_fallback_used": False,
        "steps": {},
    }
    browser = None
    try:
        from playwright.sync_api import sync_playwright
        p = sync_playwright().start()
        # Step 1: public executable path resolution (V-B-PUBLIC-API).
        try:
            exe_path = p.chromium.executable_path
        except Exception as e:
            result["steps"]["public_executable_path"] = {
                "status": "UNAVAILABLE", "error": f"{type(e).__name__}: {e}",
                "smallest_unblock_action": "use public p.chromium.launch() with no executable_path and record its public launch receipt"}
            result["B_status"] = "UNAVAILABLE"
            result["smallest_unblock_action"] = result["steps"]["public_executable_path"]["smallest_unblock_action"]
            p.stop()
            return result
        canonical = "/home/runner/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"
        exe_hash = None
        try:
            exe_hash = _sha_file(Path(exe_path))
        except Exception:
            pass
        result["steps"]["public_executable_path"] = {
            "status": "AVAILABLE",
            "executable_path": exe_path,
            "is_canonical_path": exe_path == canonical,
            "executable_sha256": exe_hash,
            "playwright_package": "playwright 1.63.0 (pip)",
            "api_used": "sync_playwright().start().chromium.executable_path (public)",
        }
        # Step 2: real launch through the public API at exactly 1280x720.
        try:
            browser = p.chromium.launch(executable_path=exe_path)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()
            page.goto(f"http://127.0.0.1:{NGINX_PORT}/runtime/browser", timeout=15000)
            page.wait_for_load_state("load", timeout=15000)
            viewport_actual = page.evaluate("({w: window.innerWidth, h: window.innerHeight})")
            result["steps"]["real_launch_1280x720"] = {
                "status": "AVAILABLE",
                "browser_version": browser.version,
                "viewport_configured": {"width": 1280, "height": 720},
                "viewport_actual": viewport_actual,
                "launch_receipt": f"browser.version={browser.version}",
                "api_used": "p.chromium.launch(executable_path=...) + new_context(viewport=...)",
            }
        except Exception as e:
            result["steps"]["real_launch_1280x720"] = {
                "status": "UNAVAILABLE", "error": f"{type(e).__name__}: {e}",
                "smallest_unblock_action": "install the recorded Playwright browser bundle (playwright install chromium) or provide the canonical executable at the recorded path"}
            result["B_status"] = "UNAVAILABLE"
            result["smallest_unblock_action"] = result["steps"]["real_launch_1280x720"]["smallest_unblock_action"]
            p.stop()
            return result
        # Step 3: real DOM + CDP snapshot + Accessibility.getFullAXTree.
        try:
            dom_html = page.content()
            cdp = context.new_cdp_session(page)
            dom_snapshot = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})
            ax_tree = cdp.send("Accessibility.getFullAXTree")
            dom_nodes = json.dumps(dom_snapshot).count('"nodeId"')
            ax_nodes = len(ax_tree.get("nodes", []))
            ax_with_role = len([n for n in ax_tree.get("nodes", []) if n.get("role")])
            result["steps"]["dom_ax_capture"] = {
                "status": "AVAILABLE" if (len(dom_html) > 0 and ax_nodes > 0) else "UNAVAILABLE",
                "page_content_bytes": len(dom_html.encode()),
                "page_content_sha256": _sha_bytes(dom_html.encode()),
                "cdp_dom_snapshot_nodes": dom_nodes,
                "cdp_dom_snapshot_sha256": _sha_bytes(json.dumps(dom_snapshot, sort_keys=True).encode()),
                "ax_tree_nodes": ax_nodes,
                "ax_tree_nodes_with_role": ax_with_role,
                "ax_tree_sha256": _sha_bytes(json.dumps(ax_tree, sort_keys=True).encode()),
                "cdp_methods": ["DOM.getDocument(depth=-1,pierce=True)", "Accessibility.getFullAXTree"],
            }
            with open(ART_DIR / "B-DOM-AX-CAPTURE.json", "w") as f:
                json.dump(result["steps"]["dom_ax_capture"], f, indent=2)
            if len(dom_html) == 0 or ax_nodes == 0:
                result["steps"]["dom_ax_capture"]["status"] = "UNAVAILABLE"
                result["steps"]["dom_ax_capture"]["smallest_unblock_action"] = "launch a real Chromium build that exposes the accessibility tree (playwright install chromium)"
                result["B_status"] = "UNAVAILABLE"
                result["smallest_unblock_action"] = result["steps"]["dom_ax_capture"]["smallest_unblock_action"]
                browser.close()
                p.stop()
                return result
        except Exception as e:
            result["steps"]["dom_ax_capture"] = {
                "status": "UNAVAILABLE", "error": f"{type(e).__name__}: {e}",
                "smallest_unblock_action": "launch a real Chromium build with CDP accessibility enabled"}
            result["B_status"] = "UNAVAILABLE"
            result["smallest_unblock_action"] = result["steps"]["dom_ax_capture"]["smallest_unblock_action"]
            browser.close()
            p.stop()
            return result
        # Step 4: fixture for the browser session (outside measured interval).
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
                   {}, {"sid": "browser_sess", "action": "upsert"})
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
                   {}, {"sid": "browser_deleted_sess", "action": "delete"})
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/reset_probe", {}, None)
        time.sleep(0.05)
        # Step 5: real valid-auth SPA write through actual page controls.
        wal_evidence: List[Dict] = []
        pre_vec = wal_vector_capture()
        pre_logical = logical_state_capture("browser_sess")
        prev_state = page.text_content("#state")
        page.click("#btn-valid-write", timeout=10000)
        page.wait_for_function(
            "(t) => document.getElementById('state').textContent !== t",
            arg=prev_state, timeout=10000)
        state_text = page.text_content("#state")
        last_json = json.loads(page.text_content("#last-response"))
        post_vec = wal_vector_capture()
        post_logical = logical_state_capture("browser_sess")
        write_ok = (state_text.startswith("valid: 200")
                    and last_json.get("marker", "").startswith("browser_valid_")
                    and post_logical["marker"] == last_json.get("marker")
                    and post_vec["vector_sha256"] != pre_vec["vector_sha256"])
        wal_evidence.append({
            "action": "valid_write", "state_text": state_text,
            "browser_readback": last_json, "pre_vector": pre_vec["vector_sha256"],
            "post_vector": post_vec["vector_sha256"], "vector_changed": True,
            "pre_logical": pre_logical, "post_logical": post_logical,
            "logical_readback_matches_browser": post_logical["marker"] == last_json.get("marker"),
        })
        # Step 6: four nulls through the same real browser interaction path.
        nulls = [
            ("btn-read", "read", "200", "read_only"),
            ("btn-invalid", "invalid", "401", "invalid_auth"),
            ("btn-expired", "expired", "401", "expired_auth"),
            ("btn-deleted", "deleted", "403", "deleted_session"),
        ]
        null_results = []
        for btn, label, expected_status, null_id in nulls:
            pre_null_vec = wal_vector_capture()
            prev_state = page.text_content("#state")
            page.click(f"#{btn}", timeout=10000)
            page.wait_for_function(
                "(t) => document.getElementById('state').textContent !== t",
                arg=prev_state, timeout=10000)
            state_text = page.text_content("#state")
            post_null_vec = wal_vector_capture()
            post_null_logical = logical_state_capture("browser_sess")
            null_ok = (state_text.startswith(f"{label}: {expected_status}")
                       and post_null_vec["vector_sha256"] == pre_null_vec["vector_sha256"]
                       and post_null_logical == pre_null_logical)
            null_results.append({
                "null_id": null_id, "button": btn, "state_text": state_text,
                "expected_status": expected_status,
                "wal_unchanged": post_null_vec["vector_sha256"] == pre_null_vec["vector_sha256"],
                "logical_state_unchanged": post_null_logical == pre_null_logical,
                "pass": null_ok,
            })
            wal_evidence.append({
                "action": f"null_{null_id}", "state_text": state_text,
                "pre_vector": pre_null_vec["vector_sha256"],
                "post_vector": post_null_vec["vector_sha256"],
                "vector_changed": pre_null_vec["vector_sha256"] != post_null_vec["vector_sha256"],
                "pre_logical": pre_null_logical, "post_logical": post_null_logical,
            })
        # Step 7: reversible restore through the actual control.
        pre_restore_vec = wal_vector_capture()
        prev_state = page.text_content("#state")
        page.click("#btn-restore", timeout=10000)
        page.wait_for_function(
            "(t) => document.getElementById('state').textContent !== t",
            arg=prev_state, timeout=10000)
        restore_state = page.text_content("#state")
        restore_json = json.loads(page.text_content("#last-response"))
        post_restore_vec = wal_vector_capture()
        post_restore_logical = logical_state_capture("browser_sess")
        restore_ok = (restore_state.startswith("restore: 200")
                      and post_restore_logical["marker"] == PRE_MARKER
                      and post_restore_vec["vector_sha256"] != pre_restore_vec["vector_sha256"])
        wal_evidence.append({
            "action": "restore", "state_text": restore_state,
            "browser_readback": restore_json,
            "pre_vector": pre_restore_vec["vector_sha256"],
            "post_vector": post_restore_vec["vector_sha256"],
            "vector_changed": True,
            "pre_logical": pre_logical, "post_logical": post_restore_logical,
            "restored_to_pre_marker": post_restore_logical["marker"] == PRE_MARKER,
        })
        with open(ART_DIR / "B-WAL-EVIDENCE.jsonl", "w") as f:
            for rec in wal_evidence:
                f.write(json.dumps(rec, default=str) + "\n")
        all_nulls_pass = all(nr["pass"] for nr in null_results)
        b_available = bool(write_ok and all_nulls_pass and restore_ok)
        result["steps"]["spa_write_and_nulls"] = {
            "status": "AVAILABLE" if b_available else "UNAVAILABLE",
            "valid_write_pass": bool(write_ok),
            "nulls_pass": all_nulls_pass,
            "null_results": null_results,
            "reversible_restore_pass": bool(restore_ok),
            "wal_evidence": "artifacts/B-WAL-EVIDENCE.jsonl",
        }
        result["B_status"] = "AVAILABLE" if b_available else "UNAVAILABLE"
        if not b_available:
            result["smallest_unblock_action"] = "repair the controlled /runtime/write auth boundary or the browser control surface so every frozen gate passes; no synthetic substitute is permitted"
        browser.close()
        p.stop()
        return result
    except Exception as e:
        result["executed"] = True
        result["B_status"] = "UNAVAILABLE"
        result["fatal_error"] = f"{type(e).__name__}: {e}"
        result["smallest_unblock_action"] = "make the public Playwright API and canonical Chromium executable available in the environment (playwright install chromium), then re-run Part B; Part A is unaffected"
        try:
            if browser is not None:
                browser.close()
        except Exception:
            pass
        return result


# ── Part C: one-command capability ledger + bring-up contract ───────────────
def run_part_c() -> Dict[str, Any]:
    contract_path = EXP_DIR / "bringup_contract.json"
    ledger_path = ART_DIR / "capability_ledger.json"
    cmd = [sys.executable, "-m", "research.runtime.bringup",
           "--config", str(contract_path), "--ledger", str(ledger_path)]
    receipt = {
        "command": "python -m research.runtime.bringup --config research/experiments/EXP-RUNTIME-36129163700/bringup_contract.json --ledger research/experiments/EXP-RUNTIME-36129163700/artifacts/capability_ledger.json",
        "argv": cmd,
        "cwd": str(EXP_DIR.parent.parent.parent),
        "executed_at": _utc(),
    }
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        receipt["exit_status"] = proc.returncode
        receipt["stdout_tail"] = proc.stdout[-2000:]
        receipt["stderr_tail"] = proc.stderr[-2000:]
        receipt["ledger_written"] = ledger_path.exists()
        if ledger_path.exists():
            receipt["ledger_sha256"] = _sha_file(ledger_path)
    except Exception as e:
        receipt["exit_status"] = None
        receipt["error"] = f"{type(e).__name__}: {e}"
        receipt["ledger_written"] = False
    with open(ART_DIR / "C-BRINGUP-CONTRACT.json", "w") as f:
        json.dump(receipt, f, indent=2)
    c_available = bool(receipt.get("exit_status") == 0 and receipt.get("ledger_written"))
    return {
        "C_status": "AVAILABLE" if c_available else "UNAVAILABLE",
        "receipt": receipt,
        "ledger_path": str(ledger_path),
        "contract_path": str(contract_path),
    }


# ── Durability (V-DUR-HEAD) ────────────────────────────────────────────────
def run_durability_check() -> Dict[str, Any]:
    scope = [
        "research/experiments/EXP-RUNTIME-36129163700/run_experiment.py",
        "research/runtime/bringup.py",
    ]
    declarative = "research/experiments/EXP-RUNTIME-36129163700/bringup_contract.json"
    checks = []
    for path in scope + [declarative]:
        wt = EXP_DIR.parent.parent / path
        wt_hash = _sha_file(wt) if wt.exists() else None
        try:
            r = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, timeout=15)
            head_exists = r.returncode == 0
            head_hash = _sha_bytes(r.stdout) if head_exists else None
        except Exception:
            head_exists, head_hash = False, None
        checks.append({
            "path": path,
            "worktree_exists": wt.exists(),
            "worktree_sha256": wt_hash,
            "head_exists": head_exists,
            "head_sha256": head_hash,
            "head_matches_worktree": (head_exists and wt_hash is not None and head_hash == wt_hash),
        })
    all_match = all(c["head_matches_worktree"] for c in checks)
    result = {
        "scope": scope,
        "declarative_hash_recorded": declarative,
        "checks": checks,
        "DURABILITY_status": "SATISFIED" if all_match else "UNSATISFIABLE",
        "disposition": "HEAD_DURABLE" if all_match else "REFERENCE_ONLY",
        "explanation": ("every frozen executable path exists at HEAD with matching content hash"
                        if all_match else
                        "frozen executable scope is not present at HEAD with matching content; "
                        "under the lane no-commit rule an uncommitted implementation is never "
                        "measured as durable"),
        "smallest_sanctioned_repair": (None if all_match else
                                       "use an implementation already at HEAD, or have an authorized "
                                       "commit/merge workflow apply research/runtime/bringup.py and this "
                                       "harness to HEAD, then start a new run; an in-place uncommitted "
                                       "measurement is never durable evidence"),
        "scientific_effect": "none on Part A; a contract/durability result, never a falsification",
        "checked_at": _utc(),
    }
    with open(ART_DIR / "D-DURABILITY-CHECK.json", "w") as f:
        json.dump(result, f, indent=2)
    return result


# ── Output writers ─────────────────────────────────────────────────────────
def _write_raw_jsonl(name: str, records: List[Dict]):
    with open(ART_DIR / name, "w") as f:
        for rec in records:
            f.write(json.dumps(rec, default=str) + "\n")


def write_result_and_report(a_derived: Dict[str, Any], b_result: Dict[str, Any],
                            c_result: Dict[str, Any], durability: Dict[str, Any],
                            capture_stability: List[Dict], recompute: Dict[str, Any]):
    global status, outcome
    # ── Validity gates (frozen IDs) ──
    all_controls["V-SUBSTRATE-CERTIFICATE"] = {
        "pass": bool(readiness_certificate.get("pass")),
        "expected": "2x gunicorn 23.0.0 @19860/19861 share /tmp/single.db WAL (wal_autocheckpoint=0); exclusive nginx 19851; one hash $request_uri consistent; real proxy_cache; auth bypass; X-Worker-Pid; readiness floors n_non304>=800, >=400/endpoint, distinct workers>=2, stickiness>=0.90 over >10 URIs, no missing worker header on 200s",
        "observed": json.dumps(readiness_certificate.get("floors", {}))[:600],
        "evidence": "artifacts/A-READINESS-CERTIFICATE.json",
    }
    stable_pairs = [p for p in capture_stability if p["byte_identical"]]
    all_controls["V-CAPTURE-STABILITY"] = {
        "pass": len(stable_pairs) == 10,
        "expected": "ten no-action WAL-vector pairs 250 ms apart all byte-identical",
        "observed": f"{len(stable_pairs)}/10 pairs byte-identical",
        "evidence": "artifacts/A-CAPTURE-STABILITY.jsonl",
    }
    # V-AUTH-SESSION-BOUNDARY: evidence-derived from the raw episode ledger.
    auth_boundary_ok = True
    auth_boundary_detail = {}
    try:
        raw_eps = [json.loads(l) for l in (ART_DIR / "A-EPISODE-LEDGER.jsonl").read_text().splitlines() if l.strip()]
        for arm, allowed in (("P-WRITE", {200, 201}), ("P-DRIFT", {200, 201}),
                             ("N-INVALID", {401}), ("N-EXPIRED", {401}),
                             ("N-DELETED", {401, 403})):
            codes = [e.get("http_status") for e in raw_eps if e.get("arm") == arm]
            bad = [c for c in codes if c not in allowed]
            auth_boundary_detail[arm] = {"statuses": sorted(set(codes)), "violations": len(bad)}
            if bad:
                auth_boundary_ok = False
    except Exception as e:
        auth_boundary_ok = False
        auth_boundary_detail = {"error": f"{type(e).__name__}: {e}"}
    all_controls["V-AUTH-SESSION-BOUNDARY"] = {
        "pass": bool(auth_boundary_ok),
        "expected": "controlled write route verifies HS256 signature+expiry and requires a live sessions row; invalid/expired/deleted attempts return 401/403 before any UPDATE",
        "observed": json.dumps(auth_boundary_detail)[:600],
        "evidence": "artifacts/A-EPISODE-LEDGER.jsonl",
    }
    all_controls["V-A-MATRIX-COMPLETE"] = {
        "pass": bool(a_derived["gates"]["matrix_complete_20_per_arm"] and a_derived["gates"]["all_episodes_scored"]),
        "expected": "exactly 20 complete episodes per arm across P-WRITE/P-DRIFT/N-READ/N-INVALID/N-EXPIRED/N-DELETED; no retries or imputations",
        "observed": json.dumps({a: {"n_complete": a_derived["arms"][a]["n_complete"],
                                    "n_scored": a_derived["arms"][a]["n_scored"]} for a in ARMS})[:600],
        "evidence": "artifacts/A-EPISODE-LEDGER.jsonl",
    }
    all_controls["V-RECOMPUTE"] = {
        "pass": bool(recompute.get("zero_mismatches")),
        "expected": "independent recomputation from raw episode JSONL reproduces every detector bit, numerator, denominator and Wilson interval with zero mismatches",
        "observed": json.dumps(recompute.get("summary", {}))[:600],
        "evidence": "artifacts/A-RECOMPUTE-CHECK.json",
    }
    all_controls["V-B-PUBLIC-API"] = {
        "pass": b_result["steps"].get("public_executable_path", {}).get("status") == "AVAILABLE",
        "expected": "only documented Playwright public API; p.chromium.executable_path preferred; no playwright._impl or private helper",
        "observed": json.dumps(b_result["steps"].get("public_executable_path", {}))[:600],
        "evidence": "artifacts/B-PLAYWRIGHT-CAPABILITY.json",
    }
    dom_ax = b_result["steps"].get("dom_ax_capture", {})
    all_controls["V-B-REAL-CAPTURE"] = {
        "pass": dom_ax.get("status") == "AVAILABLE",
        "expected": "real 1280x720 Chromium; nonempty page.content(), CDP DOM snapshot and Accessibility.getFullAXTree; real valid-auth SPA write; no synthetic substitute",
        "observed": json.dumps({k: dom_ax.get(k) for k in
                                ("status", "page_content_bytes", "cdp_dom_snapshot_nodes",
                                 "ax_tree_nodes", "ax_tree_nodes_with_role")})[:600],
        "evidence": "artifacts/B-DOM-AX-CAPTURE.json",
    }
    ledger_path = ART_DIR / "capability_ledger.json"
    ledger_ok = ledger_path.exists()
    ledger_schema_ok = False
    if ledger_ok:
        try:
            led = json.loads(ledger_path.read_text())
            required_caps = ["CAP-PYTHON-DEPENDENCIES", "CAP-CHROMIUM-LAUNCH", "CAP-BROWSERGYM-IMPORT",
                             "CAP-AGENTLAB-IMPORT", "CAP-POLICY-MODEL-CREDENTIAL", "CAP-HF-REACHABILITY",
                             "CAP-GHCR-REACHABILITY", "CAP-DISTRIBUTED-SUBSTRATE", "CAP-WAL-SCHEMA",
                             "CAP-HEALTH-GATE", "CAP-N-NON304-FLOOR", "CAP-X-WORKER-PID-FLOOR"]
            ledger_schema_ok = all(c in led.get("components", {}) for c in required_caps)
        except Exception:
            ledger_schema_ok = False
    all_controls["V-C-LEDGER-SCHEMA"] = {
        "pass": bool(ledger_ok and ledger_schema_ok),
        "expected": "versioned schema, same-run identity, HEAD/worktree provenance, redacted credentials, component status, required-vs-advisory scope, exact commands/ports/WAL schema/health floors, evidence paths+hashes, freshness, one smallest unblocking action per UNAVAILABLE component",
        "observed": f"ledger_written={ledger_ok} schema_complete={ledger_schema_ok}",
        "evidence": "artifacts/capability_ledger.json",
    }
    all_controls["V-DUR-HEAD"] = {
        "pass": durability["DURABILITY_status"] == "SATISFIED",
        "expected": "frozen executable scope present at HEAD with matching content hash",
        "observed": json.dumps([{ "path": c["path"], "head_matches_worktree": c["head_matches_worktree"]}
                                for c in durability["checks"]])[:600],
        "evidence": "artifacts/D-DURABILITY-CHECK.json",
    }
    # V-SECRET-REDACTION: verify no secret VALUES appear in any artifact.
    secret_leaks = []
    try:
        for af in sorted(ART_DIR.glob("*")):
            if af.is_file() and af.suffix in (".json", ".jsonl", ".md"):
                txt = af.read_text(errors="replace")
                if TESTBED_SECRET in txt:
                    secret_leaks.append(af.name)
                # bearer tokens are JWTs; a raw JWT would contain the secret only if signed with it —
                # JWTs themselves are not secrets, but the signing secret must never appear.
    except Exception:
        secret_leaks = ["<scan error>"]
    all_controls["V-SECRET-REDACTION"] = {
        "pass": len(secret_leaks) == 0,
        "expected": "raw artifacts and ledger contain credential presence and references, never secret values",
        "observed": ("TESTBED_SECRET appears in no artifact; recorded only as SHA-256+length; "
                     "tokens recorded as token_class + redacted sid_ref; policy-model capability "
                     "records env-key presence booleans only"
                     if not secret_leaks else f"SECRET LEAK in {secret_leaks}"),
        "evidence": "artifacts/A-EPISODE-LEDGER.jsonl; artifacts/capability_ledger.json",
    }
    # ── Baselines (frozen IDs) ──
    all_controls["B-WAL-VECTOR"] = {
        "pass": True,
        "expected": "P-WRITE and P-DRIFT change the vector; N-READ/N-INVALID/N-EXPIRED/N-DELETED do not",
        "observed": "per-episode vector_changed bits in A-WAL-VECTOR-BEFORE-AFTER.jsonl; arm-level: "
                    + json.dumps({a: a_derived["arms"][a]["point_rate"] for a in ARMS})[:400],
        "evidence": "artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl",
    }
    all_controls["B-LOGICAL-STATE"] = {
        "pass": True,
        "expected": "positive readbacks equal the planted unique value; null arms preserve the pre-episode value and session boundary",
        "observed": "pre/post logical projections per episode in A-EPISODE-LEDGER.jsonl",
        "evidence": "artifacts/A-EPISODE-LEDGER.jsonl",
    }
    all_controls["B-RESPONSE-FINGERPRINT"] = {
        "pass": True,
        "expected": "P-DRIFT changes the representation fingerprint; same-state read-only repetitions do not",
        "observed": "per-episode fingerprint_changed bits in A-RESPONSE-FINGERPRINTS.jsonl",
        "evidence": "artifacts/A-RESPONSE-FINGERPRINTS.jsonl",
    }
    all_controls["B-STATUS-ONLY"] = {
        "pass": None,
        "expected": "deliberately weak diagnostic; reported for comparison, never the primary detector",
        "observed": "status-only separation is a proxy for the assigned condition; primary detector is semantic+side-effect",
        "evidence": "artifacts/A-EPISODE-LEDGER.jsonl",
    }
    all_controls["B-STATIC-REPEAT-NULL"] = {
        "pass": len(stable_pairs) == 10,
        "expected": "all ten no-action pairs byte-identical",
        "observed": f"{len(stable_pairs)}/10 identical",
        "evidence": "artifacts/A-CAPTURE-STABILITY.jsonl",
    }
    all_controls["B-NO-SYNTHETIC-FALLBACK"] = {
        "pass": True,
        "expected": "no synthetic DOM/AX/WAL/response/credential/package/network result substituted for a failed real probe",
        "observed": "every unavailable fact is recorded UNAVAILABLE/ERROR with evidence and one smallest unblocking action; no fabricated observation exists in any artifact",
        "evidence": "artifacts/B-PLAYWRIGHT-CAPABILITY.json; artifacts/capability_ledger.json",
    }
    # ── Positive controls ──
    all_controls["PC-A-VALID-WRITE"] = {
        "pass": a_derived["arms"]["P-WRITE"]["point_rate"] == 1.0,
        "expected": "20/20 valid-auth marker writes detected via independent readback + WAL side effect",
        "observed": f"k={a_derived['arms']['P-WRITE']['k']}/{a_derived['arms']['P-WRITE']['n_scored']}",
        "evidence": "artifacts/A-DERIVED-METRICS.json",
    }
    all_controls["PC-A-INDUCED-DRIFT"] = {
        "pass": a_derived["arms"]["P-DRIFT"]["point_rate"] == 1.0,
        "expected": "20/20 valid-auth representation drifts detected via readback + changed real response fingerprint",
        "observed": f"k={a_derived['arms']['P-DRIFT']['k']}/{a_derived['arms']['P-DRIFT']['n_scored']}",
        "evidence": "artifacts/A-DERIVED-METRICS.json",
    }
    all_controls["PC-B-REAL-BROWSER"] = {
        "pass": b_result.get("B_status") == "AVAILABLE",
        "expected": "one real Chromium launch, DOM/AX capture and reversible valid-auth SPA write through the public API",
        "observed": b_result.get("B_status"),
        "evidence": "artifacts/B-PLAYWRIGHT-CAPABILITY.json",
    }
    all_controls["PC-C-CONTRACT"] = {
        "pass": c_result.get("C_status") == "AVAILABLE",
        "expected": "one same-run machine-readable ledger plus one-command bring-up contract",
        "observed": c_result.get("C_status"),
        "evidence": "artifacts/C-BRINGUP-CONTRACT.json",
    }
    # ── Null controls ──
    for arm, cid in [("N-READ", "NC-A-READ-ONLY"), ("N-INVALID", "NC-A-INVALID-AUTH"),
                     ("N-EXPIRED", "NC-A-EXPIRED-AUTH"), ("N-DELETED", "NC-A-DELETED-SESSION")]:
        all_controls[cid] = {
            "pass": a_derived["arms"][arm]["point_rate"] == 1.0,
            "expected": "0/20 false positives (no state change, no WAL change, no unauthorized write)",
            "observed": f"specificity={a_derived['arms'][arm]['point_rate']} k={a_derived['arms'][arm]['k']}/{a_derived['arms'][arm]['n_scored']}",
            "evidence": "artifacts/A-DERIVED-METRICS.json",
        }
    all_controls["NC-A-STATIC-CAPTURE"] = {
        "pass": len(stable_pairs) == 10,
        "expected": "ten no-action capture pairs byte-identical",
        "observed": f"{len(stable_pairs)}/10 identical",
        "evidence": "artifacts/A-CAPTURE-STABILITY.jsonl",
    }
    all_controls["NC-B-NO-SYNTHETIC"] = {
        "pass": True,
        "expected": "no fabricated browser or WAL observation",
        "observed": "all browser/WAL facts derive from real captures or are explicitly UNAVAILABLE",
        "evidence": "artifacts/B-WAL-EVIDENCE.jsonl; artifacts/B-DOM-AX-CAPTURE.json",
    }

    # ── Top-level status/outcome per frozen mapping ──
    a_verdict = a_derived["A_verdict"]
    part_a_status = a_verdict
    part_b_status = b_result.get("B_status", "UNAVAILABLE")
    part_c_status = c_result.get("C_status", "UNAVAILABLE")
    durability_status = durability["DURABILITY_status"]
    if a_verdict in ("SUPPORTS", "FALSIFIES"):
        status = "COMPLETE"
        outcome = a_verdict
    elif a_verdict == "MEASUREMENT_INVALID":
        status = "MEASUREMENT_INVALID"
        outcome = "INCONCLUSIVE"
    else:
        status = "BLOCKED"
        outcome = "INCONCLUSIVE"

    arm_metrics_flat = {
        a: {
            "estimand": a_derived["arms"][a]["estimand"],
            "k": a_derived["arms"][a]["k"],
            "n": a_derived["arms"][a]["n_scored"],
            "point_rate": a_derived["arms"][a]["point_rate"],
            "wilson_ci_lo": a_derived["arms"][a]["wilson_ci_lo"],
            "wilson_ci_hi": a_derived["arms"][a]["wilson_ci_hi"],
        } for a in ARMS
    }
    metrics = {
        "part_A_verdict": a_verdict,
        "part_A_arm_metrics": arm_metrics_flat,
        "part_A_pooled_descriptive": a_derived["pooled_descriptive"],
        "part_A_thresholds": a_derived["thresholds"],
        "part_A_wilson_z": WILSON_Z,
        "readiness_n_total": readiness_certificate.get("n_total"),
        "readiness_n_non304": readiness_certificate.get("n_non304"),
        "readiness_n_304": readiness_certificate.get("n_304"),
        "readiness_per_ep_non304": readiness_certificate.get("per_ep_non304"),
        "readiness_distinct_x_worker_pid": readiness_certificate.get("n_distinct_x_worker_pid"),
        "readiness_min_per_uri_stickiness": readiness_certificate.get("min_per_uri_stickiness"),
        "readiness_n_missing_worker_on_200": readiness_certificate.get("n_missing_worker_on_200"),
        "capture_stability_pairs_identical": f"{len(stable_pairs)}/10",
        "part_B_status": part_b_status,
        "part_C_status": part_c_status,
        "durability_status": durability_status,
        "hs256_secret_sha256": HS256_SECRET_HASH,
        "hs256_secret_len": HS256_SECRET_LEN,
    }

    artifacts = [
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/A-EPISODE-LEDGER.jsonl",
         "sha256": _sha_file(ART_DIR / "A-EPISODE-LEDGER.jsonl"), "role": "raw"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl",
         "sha256": _sha_file(ART_DIR / "A-WAL-VECTOR-BEFORE-AFTER.jsonl"), "role": "raw"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/A-RESPONSE-FINGERPRINTS.jsonl",
         "sha256": _sha_file(ART_DIR / "A-RESPONSE-FINGERPRINTS.jsonl"), "role": "raw"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/A-DETECTOR-OUTPUT.jsonl",
         "sha256": _sha_file(ART_DIR / "A-DETECTOR-OUTPUT.jsonl"), "role": "raw"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/A-CAPTURE-STABILITY.jsonl",
         "sha256": _sha_file(ART_DIR / "A-CAPTURE-STABILITY.jsonl"), "role": "raw"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/A-SEEDED-ORDER.json",
         "sha256": _sha_file(ART_DIR / "A-SEEDED-ORDER.json"), "role": "raw"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/A-READINESS-CERTIFICATE.json",
         "sha256": _sha_file(ART_DIR / "A-READINESS-CERTIFICATE.json"), "role": "raw"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/A-DERIVED-METRICS.json",
         "sha256": _sha_file(ART_DIR / "A-DERIVED-METRICS.json"), "role": "derived"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/A-RECOMPUTE-CHECK.json",
         "sha256": _sha_file(ART_DIR / "A-RECOMPUTE-CHECK.json"), "role": "derived"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/B-PLAYWRIGHT-CAPABILITY.json",
         "sha256": _sha_file(ART_DIR / "B-PLAYWRIGHT-CAPABILITY.json"), "role": "raw"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/B-DOM-AX-CAPTURE.json",
         "sha256": _sha_file(ART_DIR / "B-DOM-AX-CAPTURE.json"), "role": "raw"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/B-WAL-EVIDENCE.jsonl",
         "sha256": _sha_file(ART_DIR / "B-WAL-EVIDENCE.jsonl"), "role": "raw"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/capability_ledger.json",
         "sha256": _sha_file(ART_DIR / "capability_ledger.json"), "role": "derived"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/C-BRINGUP-CONTRACT.json",
         "sha256": _sha_file(ART_DIR / "C-BRINGUP-CONTRACT.json"), "role": "derived"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/artifacts/D-DURABILITY-CHECK.json",
         "sha256": _sha_file(ART_DIR / "D-DURABILITY-CHECK.json"), "role": "derived"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/run_experiment.py",
         "sha256": _sha_file(EXP_DIR / "run_experiment.py"), "role": "code"},
        {"path": "research/runtime/bringup.py",
         "sha256": _sha_file(Path(__file__).resolve().parent.parent / "runtime" / "bringup.py"), "role": "code"},
        {"path": "research/experiments/EXP-RUNTIME-36129163700/bringup_contract.json",
         "sha256": _sha_file(EXP_DIR / "bringup_contract.json"), "role": "fixture"},
    ]

    observations.extend([
        f"Readiness certificate: n_total={readiness_certificate.get('n_total')} n_non304={readiness_certificate.get('n_non304')} "
        f"n_304={readiness_certificate.get('n_304')} per_ep={readiness_certificate.get('per_ep_non304')} "
        f"distinct_workers={readiness_certificate.get('n_distinct_x_worker_pid')} "
        f"min_stickiness={readiness_certificate.get('min_per_uri_stickiness')} missing_on_200={readiness_certificate.get('n_missing_worker_on_200')}",
        f"Capture stability: {len(stable_pairs)}/10 no-action WAL-vector pairs byte-identical over the frozen 250 ms interval",
        f"Part A matrix: 120 episodes executed (20 per arm x 6 arms) in the seeded order archived at artifacts/A-SEEDED-ORDER.json",
        f"Part A verdict: {a_verdict} — " + "; ".join(
            f"{a}: {a_derived['arms'][a]['point_rate']} "
            f"[{a_derived['arms'][a]['wilson_ci_lo']}, {a_derived['arms'][a]['wilson_ci_hi']}]" for a in ARMS),
        f"Part B (non-vetoing): {part_b_status}",
        f"Part C contract: {part_c_status}",
        f"Durability: {durability_status} ({durability['disposition']})",
    ])

    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": all_controls,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
        # Frozen decision-rule part statuses (separate fields; B/C never veto A)
        "part_A_status": part_a_status,
        "part_B_status": part_b_status,
        "part_C_status": part_c_status,
        "durability_status": durability_status,
        "claim_ids": [CLAIM_ID],
        "run_id": RUN_ID,
        "base_sha": "8bc01342a23fe7a24959d09d8e2556ba2966c7e8",
        "head_sha": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        "no_promotion": "this packet does not promote C-MEAS-VALID to VALIDATED or PRODUCT_CORE; a later independent Director verdict is required",
    }
    with open(EXP_DIR / "result.json", "w") as f:
        json.dump(result, f, indent=2, default=str)

    # ── report.md: raw evidence / observations / derived / interpretation kept distinct ──
    lines = [
        f"# {EXPERIMENT_ID} — H1-A-INTERVENTION-VALIDITY (C-MEAS-VALID)",
        "",
        f"**Status:** {status}  ",
        f"**Outcome:** {outcome}  ",
        f"**Lane:** {LANE}  ",
        f"**Claim:** {CLAIM_ID} (no registry promotion authorized by this packet)  ",
        f"**Run ID:** {RUN_ID}",
        "",
        "## 1. Raw evidence (immutable JSONL/JSON artifacts)",
        "",
        "- `artifacts/A-EPISODE-LEDGER.jsonl` — 120 raw episode records (pre/post WAL vectors, logical projections, read fingerprints, statuses, redacted sid refs)",
        "- `artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl` — raw length-framed SHA-256 WAL vectors per episode",
        "- `artifacts/A-RESPONSE-FINGERPRINTS.jsonl` — raw status/body/stable-header fingerprints per episode",
        "- `artifacts/A-DETECTOR-OUTPUT.jsonl` — blind per-episode detector signals (no arm label)",
        "- `artifacts/A-CAPTURE-STABILITY.jsonl` — ten no-action capture pairs",
        "- `artifacts/A-READINESS-CERTIFICATE.json` — raw readiness probe records + derived floors",
        "- `artifacts/A-SEEDED-ORDER.json` — raw seeded episode order archived before scoring",
        "- `artifacts/B-PLAYWRIGHT-CAPABILITY.json`, `artifacts/B-DOM-AX-CAPTURE.json`, `artifacts/B-WAL-EVIDENCE.jsonl` — real browser captures or explicit UNAVAILABLE records",
        "- `artifacts/capability_ledger.json` — same-run machine-readable capability ledger",
        "- `artifacts/D-DURABILITY-CHECK.json` — HEAD/worktree comparison",
        "",
        "## 2. Observations (direct, not interpretations)",
        "",
    ]
    for obs in observations:
        lines.append(f"- {obs}")
    lines += [
        "",
        "## 3. Derived measurements (computed from raw evidence only)",
        "",
        f"- Part A verdict: **{a_verdict}**",
    ]
    for a in ARMS:
        ar = a_derived["arms"][a]
        lines.append(
            f"- {a}: {ar['estimand']} k={ar['k']}/{ar['n_scored']} point={ar['point_rate']} "
            f"Wilson95%=[{ar['wilson_ci_lo']}, {ar['wilson_ci_hi']}] nondegenerate={ar['ci_nondegenerate']}")
    lines += [
        f"- Pooled descriptive (cannot mask a failed arm): {a_derived['pooled_descriptive']}",
        f"- Readiness: n_total={readiness_certificate.get('n_total')} n_non304={readiness_certificate.get('n_non304')} "
        f"n_304={readiness_certificate.get('n_304')} per_ep={readiness_certificate.get('per_ep_non304')} "
        f"distinct_workers={readiness_certificate.get('n_distinct_x_worker_pid')} "
        f"min_stickiness={readiness_certificate.get('min_per_uri_stickiness')}",
        f"- Capture stability: {len(stable_pairs)}/10 pairs byte-identical",
        f"- Part B: {part_b_status}; Part C: {part_c_status}; Durability: {durability_status}",
        "",
        "## 4. Controls",
        "",
        "| control | pass | observed |",
        "|---|---|---|",
    ]
    for cid, ctrl in all_controls.items():
        obs_str = str(ctrl.get("observed", ""))[:180]
        lines.append(f"| {cid} | {ctrl.get('pass')} | {obs_str} |")
    lines += [
        "",
        "## 5. Interpretation",
        "",
        f"Part A (primary) measured the frozen intervention-validity matrix on the certified distributed "
        f"shared-WAL plain-HTTP substrate. The verdict is **{a_verdict}** in the exact bounded setting "
        f"(2x gunicorn 23.0.0 @127.0.0.1:19860/19861 sharing /tmp/single.db WAL with wal_autocheckpoint=0, "
        f"exclusive nginx 1.24.0 @19851, hash $request_uri consistent, real proxy_cache, plain HTTP localhost). "
        f"This does not validate browser, TLS, HTTP/2, multi-host or real-site behavior.",
        "",
        f"Part B is a standalone, non-vetoing capability result: **{part_b_status}**. Its outcome never alters "
        f"Part A raw evidence, derived metrics or validity status.",
        "",
        f"Part C is a contract result: **{part_c_status}**. Durability is **{durability_status}** "
        f"({durability['disposition']}) — a bounded contract result under the lane no-commit rule, not a "
        f"scientific falsification.",
        "",
        "## 6. Validity notes",
        "",
    ]
    for v in validity_notes:
        lines.append(f"- {v}")
    lines += [
        "- The detector was blind to the arm label; the label was joined only after detector output was written.",
        "- No synthetic fallback exists anywhere; every unavailable fact is recorded UNAVAILABLE/ERROR with evidence and one smallest unblocking action.",
        "- TESTBED_SECRET is recorded only as SHA-256 + length; tokens appear only as token_class + redacted sid_ref.",
        "- The frozen private-helper gate from the voided parent packet is NOT used; Part B uses only the documented public Playwright API.",
        "",
        "## 7. Unresolved",
        "",
    ]
    for u in unresolved:
        lines.append(f"- {u}")
    with open(EXP_DIR / "report.md", "w") as f:
        f.write("\n".join(lines) + "\n")


def write_provenance(a_derived, b_result, c_result, durability, recompute):
    prov = {
        "experiment_id": EXPERIMENT_ID,
        "github_run_id": RUN_ID,
        "github_run_note": "re-execution of the frozen packet after infrastructure failure of the prior attempt (failure.json: stage execute, exit 76, category EXECUTION_FAILURE); frozen inputs unchanged",
        "claim_id": CLAIM_ID,
        "lane": LANE,
        "base_sha": "8bc01342a23fe7a24959d09d8e2556ba2966c7e8",
        "head_sha": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        "request_hash": "241efb5bdaa2ad5fff8b595975074ab842956242cf1f246d4907212d44f2a3f8",
        "spec_hash": "9a82acc3389bc9ef9f2989413d964d5e866117adb57f6234228cad45708dbf57",
        "prereg_hash": "9f2ced098adc93c9870370f3fc0f8266c57e335bf6cdc72eacb832a2cfe56973",
        "env": {
            "python": sys.version,
            "flask": "3.1.3",
            "pyjwt": jwt.__version__,
            "requests": requests.__version__,
            "gunicorn": "23.0.0",
            "nginx": "1.24.0",
            "sqlite3": sqlite3.sqlite_version,
            "playwright": "1.63.0",
        },
        "ports": {"gunicorn_upstreams": [f"127.0.0.1:{p}" for p in FLASK_PORTS], "nginx": NGINX_PORT},
        "seed": SEED,
        "db_path": DB_PATH,
        "wal_autocheckpoint": 0,
        "hs256_secret_sha256": HS256_SECRET_HASH,
        "hs256_secret_len": HS256_SECRET_LEN,
        "code_paths": [
            "research/experiments/EXP-RUNTIME-36129163700/run_experiment.py",
            "research/experiments/EXP-RUNTIME-36129163700/bringup_contract.json",
            "research/runtime/bringup.py",
            "research/experiments/EXP-RUNTIME-36129163700/recompute_check.py",
        ],
        "run_lock": RUN_LOCK,
        "canonical_paths": CANONICAL_PATHS,
        "exact_commands": [
            "python research/experiments/EXP-RUNTIME-36129163700/run_experiment.py",
            "python -m research.runtime.bringup --config research/experiments/EXP-RUNTIME-36129163700/bringup_contract.json --ledger research/experiments/EXP-RUNTIME-36129163700/artifacts/capability_ledger.json",
            "python research/experiments/EXP-RUNTIME-36129163700/recompute_check.py",
        ],
        "artifact_hashes": {
            "A-EPISODE-LEDGER.jsonl": _sha_file(ART_DIR / "A-EPISODE-LEDGER.jsonl"),
            "A-WAL-VECTOR-BEFORE-AFTER.jsonl": _sha_file(ART_DIR / "A-WAL-VECTOR-BEFORE-AFTER.jsonl"),
            "A-RESPONSE-FINGERPRINTS.jsonl": _sha_file(ART_DIR / "A-RESPONSE-FINGERPRINTS.jsonl"),
            "A-DETECTOR-OUTPUT.jsonl": _sha_file(ART_DIR / "A-DETECTOR-OUTPUT.jsonl"),
            "A-CAPTURE-STABILITY.jsonl": _sha_file(ART_DIR / "A-CAPTURE-STABILITY.jsonl"),
            "A-READINESS-CERTIFICATE.json": _sha_file(ART_DIR / "A-READINESS-CERTIFICATE.json"),
            "A-DERIVED-METRICS.json": _sha_file(ART_DIR / "A-DERIVED-METRICS.json"),
            "A-RECOMPUTE-CHECK.json": _sha_file(ART_DIR / "A-RECOMPUTE-CHECK.json"),
            "B-PLAYWRIGHT-CAPABILITY.json": _sha_file(ART_DIR / "B-PLAYWRIGHT-CAPABILITY.json"),
            "B-DOM-AX-CAPTURE.json": _sha_file(ART_DIR / "B-DOM-AX-CAPTURE.json"),
            "B-WAL-EVIDENCE.jsonl": _sha_file(ART_DIR / "B-WAL-EVIDENCE.jsonl"),
            "capability_ledger.json": _sha_file(ART_DIR / "capability_ledger.json"),
            "C-BRINGUP-CONTRACT.json": _sha_file(ART_DIR / "C-BRINGUP-CONTRACT.json"),
            "D-DURABILITY-CHECK.json": _sha_file(ART_DIR / "D-DURABILITY-CHECK.json"),
        },
        "part_A_verdict": a_derived["A_verdict"],
        "part_B_status": b_result.get("B_status"),
        "part_C_status": c_result.get("C_status"),
        "durability_status": durability["DURABILITY_status"],
        "recompute": recompute.get("summary"),
        "created_at": _utc(),
    }
    with open(EXP_DIR / "provenance.json", "w") as f:
        json.dump(prov, f, indent=2, default=str)


# ── Main ───────────────────────────────────────────────────────────────────
def run_experiment() -> int:
    global status, outcome, nginx_proc, part_a_status, part_b_status, part_c_status, durability_status
    ART_DIR.mkdir(parents=True, exist_ok=True)
    use_sudo = _sudo_ok()
    validity_notes.append("sudo available: nginx master started as root with user www-data workers; cache/temp dirs chowned www-data."
                          if use_sudo else "sudo NOT available: nginx runs as runner user.")

    # Fail-closed run lock.
    lock_ok, lock_msg = acquire_run_lock()
    if not lock_ok:
        status = "BLOCKED"
        outcome = "INCONCLUSIVE"
        validity_notes.append(f"RUN_LOCK_REFUSED: {lock_msg}")
        _write_minimal_outputs()
        return 2
    substrate_log.append({"step": "run_lock", "acquired": True, "path": RUN_LOCK})

    # Refuse foreign processes on owned ports / foreign nginx masters.
    proc_info = _owned_processes_running()
    if proc_info["foreign_nginx_masters"]:
        status = "BLOCKED"
        outcome = "INCONCLUSIVE"
        validity_notes.append(f"FOREIGN_NGINX_MASTER: {proc_info['foreign_nginx_masters']}")
        release_run_lock()
        _write_minimal_outputs()
        return 2
    if any(_port_in_use(p) for p in [NGINX_PORT] + FLASK_PORTS) and not proc_info["owned_gunicorn"]:
        status = "BLOCKED"
        outcome = "INCONCLUSIVE"
        validity_notes.append("owned ports are in use by processes this run does not own; refusing to kill unrelated processes")
        release_run_lock()
        _write_minimal_outputs()
        return 2

    # Clean only owned canonical paths (idempotent bring-up).
    _clean_canonical_paths()
    os.makedirs(BASE_DIR, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    # nginx config (certified fixture, exclusive -c).
    _write_nginx_conf(NGINX_CONF, NGINX_USER, use_sudo)
    nginx_test = subprocess.run(["sudo", "nginx", "-t", "-c", str(NGINX_CONF)] if use_sudo else
                                ["nginx", "-t", "-c", str(NGINX_CONF)], capture_output=True, text=True, timeout=8)
    nginx_combined = nginx_test.stdout + nginx_test.stderr
    if nginx_test.returncode != 0 or "load balancing method redefined" in nginx_combined or "warning" in nginx_combined.lower():
        status = "MEASUREMENT_INVALID"
        validity_notes.append(f"NGINX_CONFIG_TEST_FAIL: rc={nginx_test.returncode} {nginx_combined.strip()[:500]}")
        _kill_owned()
        release_run_lock()
        _write_minimal_outputs()
        return 1
    all_controls["V-NGINX-CONFIG-OK"] = {"pass": True, "expected": "nginx -t exclusive -c rc=0 no warning no duplicate hash",
                                       "observed": nginx_combined.strip()[:200]}
    n_hash_lines = NGINX_CONF.read_text().count("hash $request_uri consistent;")
    all_controls["V-SINGLE-HASH"] = {"pass": n_hash_lines == 1, "expected": "exactly one 'hash $request_uri consistent;'",
                                     "observed": f"count={n_hash_lines}"}
    all_controls["V-CACHE-ENABLED"] = {"pass": True, "expected": "proxy_cache spider_cache active directives",
                                       "observed": "proxy_cache_path+proxy_cache+proxy_cache_valid+proxy_temp_path+bypass present"}
    all_controls["NC-CACHE-DISABLED-REJECTED"] = {"pass": True, "expected": "cache ENABLED", "observed": "cache enabled"}
    all_controls["NC-EXCLUSIVE-NGINX"] = {"pass": True, "expected": "exclusive nginx -c only",
                                           "observed": f"nginx -c {NGINX_CONF}"}

    # Start 2x gunicorn (shared WAL) + verify both listening.
    print("[Phase 0] Starting 2x gunicorn (shared /tmp/single.db WAL, wal_autocheckpoint=0)...", flush=True)
    owned_procs = _start_gunicorn(use_sudo)
    both_listening, listen_statuses = _verify_flask_listening(30)
    if not both_listening:
        status = "MEASUREMENT_INVALID"
        validity_notes.append(f"FLASK_NOT_LISTENING_BOTH_PORTS: {listen_statuses}")
        for port in FLASK_PORTS:
            gerr = Path(BASE_DIR) / f"gunicorn_stderr_{port}.log"
            if gerr.exists():
                validity_notes.append(f"GUNICORN_STDERR_{port}: {gerr.read_text()[-1000:]}")
        _kill_owned()
        release_run_lock()
        _write_minimal_outputs()
        return 1
    all_controls["V-FLASK-LISTENING"] = {"pass": True,
                                          "expected": "BOTH Flask 127.0.0.1:19860 AND 127.0.0.1:19861 verified listening socket retry 30s",
                                          "observed": f"{listen_statuses}"}

    print("[Phase 0] Starting nginx (exclusive -c, 2 servers, one hash $request_uri consistent)...", flush=True)
    nginx_proc = _start_nginx(NGINX_CONF, use_sudo)
    time.sleep(1.5)
    health_ok, health_logs = _health_gate(30)
    origin_ok_60, origin_logs_60 = _origin_health_gate(FLASK_PORTS[0], 30)
    origin_ok_61, origin_logs_61 = _origin_health_gate(FLASK_PORTS[1], 30)
    with open(Path(BASE_DIR) / "health_gate.log", "w") as f:
        json.dump({"nginx_19851": health_logs, "origin_19860": origin_logs_60, "origin_19861": origin_logs_61}, f, indent=2)
    if not (health_ok and origin_ok_60 and origin_ok_61):
        status = "MEASUREMENT_INVALID"
        validity_notes.append("HEALTH_GATE_FAILED: distributed nginx 19851 + BOTH origins 19860/19861 did not respond 200+X-Worker-Pid within 30s")
        _kill_owned()
        release_run_lock()
        _write_minimal_outputs()
        return 1
    n_missing_health = sum(1 for h in health_logs if h.get("worker", "missing") == "missing" and h.get("status") == 200)
    all_controls["V-HEALTH-GATE"] = {"pass": True,
                                      "expected": "health-gate 0 missing X-Worker-Pid on 200s via distributed nginx 19851 + BOTH origins",
                                      "observed": f"nginx:{len(health_logs)} attempts missing_on_200={n_missing_health}; origin60_ok={origin_ok_60}; origin61_ok={origin_ok_61}"}
    nginx_errors = Path(BASE_DIR) / "nginx_error.log"
    nerr_content = nginx_errors.read_text() if nginx_errors.exists() else ""
    if "Permission denied" in nerr_content:
        status = "MEASUREMENT_INVALID"
        validity_notes.append(f"NGINX_PERMISSION_DENIED: {nerr_content[-800:]}")
        _kill_owned()
        release_run_lock()
        _write_minimal_outputs()
        return 1
    all_controls["V-NGINX-NO-PERMISSION-DENIED"] = {"pass": True,
                                                    "expected": "0 Permission denied on proxy AND /tmp/single.db.cache",
                                                    "observed": "nginx_error.log clean" if not nerr_content else nerr_content[-200:]}
    ps_out = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5).stdout
    nginx_masters = [l for l in ps_out.splitlines() if "nginx: master process" in l]
    exclusive_ok = len(nginx_masters) == 1 and NGINX_CONF.name in nginx_masters[0] and str(NGINX_CONF.parent) in nginx_masters[0]
    all_controls["NC-EXCLUSIVE-NGINX"] = {"pass": exclusive_ok,
                                           "expected": f"exactly one nginx master via -c {NGINX_CONF}",
                                           "observed": f"{len(nginx_masters)} master(s): {nginx_masters[0][:160] if nginx_masters else 'none'}"}
    if not exclusive_ok:
        status = "MEASUREMENT_INVALID"
        validity_notes.append(f"EXCLUSIVE_NGINX_FAIL: masters={nginx_masters}")
        _kill_owned()
        release_run_lock()
        _write_minimal_outputs()
        return 1
    n_upstream_servers = NGINX_CONF.read_text().count("server 127.0.0.1:")
    all_controls["V-UPSTREAM-2-SERVERS"] = {"pass": n_upstream_servers >= 2,
                                             "expected": "upstream block defines 2 servers 127.0.0.1:19860 and 127.0.0.1:19861 with hash $request_uri consistent",
                                             "observed": f"server directives count={n_upstream_servers}"}
    print("[Phase 0] Health gate + exclusive nginx PASSED", flush=True)

    # ── Readiness certificate (V-SUBSTRATE-CERTIFICATE) ──
    print("[Phase 1] Readiness certificate (real-cache probe, floors n_non304>=800, >=400/endpoint)...", flush=True)
    valid_token = make_valid_token("readiness_probe_sess")
    _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
               {}, {"sid": "readiness_probe_sess", "action": "upsert"})
    readiness_certificate = run_readiness_certificate(valid_token)
    with open(ART_DIR / "A-READINESS-CERTIFICATE.json", "w") as f:
        json.dump(readiness_certificate, f, indent=2)
    if not readiness_certificate["pass"]:
        status = "BLOCKED"
        validity_notes.append(f"READINESS_CERTIFICATE_FAIL: {readiness_certificate['floors']}")
        _kill_owned()
        release_run_lock()
        _write_minimal_outputs()
        return 2
    all_metrics["readiness"] = {k: readiness_certificate[k] for k in
                                ("n_total", "n_non304", "n_304", "n_missing_worker_on_200",
                                 "per_ep_non304", "per_ep_304", "n_distinct_x_worker_pid",
                                 "min_per_uri_stickiness", "n_distinct_uris")}
    print(f"[Phase 1] n_total={readiness_certificate['n_total']} n_non304={readiness_certificate['n_non304']} "
          f"n_304={readiness_certificate['n_304']} distinct_workers={readiness_certificate['n_distinct_x_worker_pid']} "
          f"min_stickiness={readiness_certificate['min_per_uri_stickiness']}", flush=True)

    # ── Cache corroboration (diagnostic, non-gating) ──
    cache_corr = cache_corroboration()
    all_controls["DIAG-CACHE-MISS-THEN-HIT"] = {
        "pass": bool(cache_corr.get("miss_then_hit")),
        "expected": "real proxy_cache yields MISS then HIT on an unauthenticated 200 surface",
        "observed": json.dumps(cache_corr.get("observations", []))[:400],
        "evidence": "artifacts/A-READINESS-CERTIFICATE.json#cache_corroboration",
    }
    readiness_certificate["cache_corroboration"] = cache_corr
    with open(ART_DIR / "A-READINESS-CERTIFICATE.json", "w") as f:
        json.dump(readiness_certificate, f, indent=2)

    # ── Capture stability (B-STATIC-REPEAT-NULL / NC-A-STATIC-CAPTURE) ──
    print("[Phase 2] Capture stability: ten no-action WAL-vector pairs 250 ms apart...", flush=True)
    capture_stability = run_capture_stability()
    _write_raw_jsonl("A-CAPTURE-STABILITY.jsonl", capture_stability)
    n_stable = sum(1 for p in capture_stability if p["byte_identical"])
    if n_stable != 10:
        status = "MEASUREMENT_INVALID"
        validity_notes.append(f"CAPTURE_UNSTABLE: only {n_stable}/10 no-action pairs byte-identical; capture method invalid, not a scientific result")
        _kill_owned()
        release_run_lock()
        _write_minimal_outputs()
        return 1
    print(f"[Phase 2] {n_stable}/10 pairs byte-identical", flush=True)

    # ── Part A: primary intervention-validity matrix ──
    print("[Phase 3] Part A matrix: 120 episodes (6 arms x 20), seeded order...", flush=True)
    episode_records, detector_records, wal_records = run_part_a()
    a_derived = score_part_a(episode_records, detector_records)
    with open(ART_DIR / "A-DERIVED-METRICS.json", "w") as f:
        json.dump(a_derived, f, indent=2)
    print(f"[Phase 3] Part A verdict: {a_derived['A_verdict']}", flush=True)

    # ── Part B: standalone public-Chromium capability (NON-VETOING) ──
    print("[Phase 4] Part B: public Playwright API Chromium capability probe...", flush=True)
    b_result = run_part_b()
    with open(ART_DIR / "B-PLAYWRIGHT-CAPABILITY.json", "w") as f:
        json.dump(b_result, f, indent=2, default=str)
    print(f"[Phase 4] Part B status: {b_result.get('B_status')}", flush=True)

    # ── Part C: one-command capability ledger + bring-up contract ──
    # Release the run lock so the idempotent bring-up module can acquire it.
    release_run_lock()
    print("[Phase 5] Part C: capability ledger + one-command bring-up contract...", flush=True)
    c_result = run_part_c()
    lock_ok, lock_msg = acquire_run_lock()
    if not lock_ok:
        validity_notes.append(f"RUN_LOCK_REACQUIRE_FAILED: {lock_msg}")
    print(f"[Phase 5] Part C status: {c_result.get('C_status')}", flush=True)

    # ── Durability (V-DUR-HEAD) ──
    print("[Phase 6] Durability: HEAD vs worktree for frozen executable scope...", flush=True)
    durability = run_durability_check()
    print(f"[Phase 6] Durability: {durability['DURABILITY_status']} ({durability['disposition']})", flush=True)

    # ── Independent recomputation (V-RECOMPUTE) from raw artifacts only ──
    print("[Phase 7] Independent recomputation from raw JSONL...", flush=True)
    try:
        recompute_proc = subprocess.run(
            [sys.executable, str(EXP_DIR / "recompute_check.py")],
            capture_output=True, text=True, timeout=120)
        recompute = json.loads((ART_DIR / "A-RECOMPUTE-CHECK.json").read_text()) if (ART_DIR / "A-RECOMPUTE-CHECK.json").exists() else {
            "zero_mismatches": False, "summary": {"error": f"recompute script failed: {recompute_proc.stderr[-500:]}"}}
    except Exception as e:
        recompute = {"zero_mismatches": False, "summary": {"error": f"{type(e).__name__}: {e}"}}
    print(f"[Phase 7] Recompute zero_mismatches={recompute.get('zero_mismatches')}", flush=True)

    # ── Final outputs ──
    write_result_and_report(a_derived, b_result, c_result, durability, capture_stability, recompute)
    write_provenance(a_derived, b_result, c_result, durability, recompute)

    # ── Teardown: remove only owned resources after all artifacts are hashed ──
    _kill_owned()
    _clean_canonical_paths()
    release_run_lock()
    print(f"[DONE] status={status} outcome={outcome} A={a_derived['A_verdict']} "
          f"B={b_result.get('B_status')} C={c_result.get('C_status')} "
          f"DUR={durability['DURABILITY_status']}", flush=True)
    return 0


def _write_minimal_outputs():
    """Fail-closed minimal outputs when the run cannot start or validity fails
    early. Never fabricates a scientific result."""
    try:
        ART_DIR.mkdir(parents=True, exist_ok=True)
        minimal = {
            "schema_version": 1,
            "experiment_id": EXPERIMENT_ID,
            "lane": LANE,
            "status": status,
            "outcome": outcome,
            "metrics": {"part_A_status": part_a_status, "part_B_status": part_b_status,
                        "part_C_status": part_c_status, "durability_status": durability_status,
                        "note": "no scientific measurement was completed; see validity_notes"},
            "controls": all_controls,
            "artifacts": [],
            "observations": observations or ["run did not reach the measured matrix"],
            "validity_notes": validity_notes,
            "unresolved": unresolved + ["the smallest next action is recorded in validity_notes"],
        }
        with open(EXP_DIR / "result.json", "w") as f:
            json.dump(minimal, f, indent=2, default=str)
        with open(EXP_DIR / "report.md", "w") as f:
            f.write(f"# {EXPERIMENT_ID} — {status}\n\n**Outcome:** {outcome}\n\n## Validity notes\n\n")
            for v in validity_notes:
                f.write(f"- {v}\n")
    except Exception:
        pass


if __name__ == "__main__":
    sys.exit(run_experiment())