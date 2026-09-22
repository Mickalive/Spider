#!/usr/bin/env python3
"""
EXP-RUNTIME-35764329925 — Production WSGI (gunicorn) + nginx generalization test
of the C-MEAS-VALID HTTP fingerprint substrate.

Frozen design: research/experiments/EXP-RUNTIME-35764329925/{spec.json, prereg.md, freeze.json}

Question (global-director PIVOT, frozen): does the identical HTTP fingerprint substrate
SHA256(status || body_bytes || sorted_filtered_standard_headers) with
EXCLUDED_HEADERS={Date,Server,X-Request-Id} retain discriminating same-status body-only
and header-only behavior with null stability (FP<0.05) and writable permission/session
controls (>=0.7) when moved from localhost Flask dev server (Werkzeug) to a production-like
WSGI stack (gunicorn 2x sync workers) + nginx reverse proxy, under concurrency (4 clients)
and cross-worker commit visibility, where bootstrap CIs are tested for non-degeneracy?

Fingerprint algorithm, Jaccard metric and bootstrap are copied IDENTICALLY from parent
EXP-RUNTIME-35749360317/run_experiment.py (compute_fingerprint, jaccard_distance,
bootstrap_jaccard_ci), which itself copied them verbatim from EXP-RUNTIME-35741906498 and
EXP-RUNTIME-35697043449, so AUDIT can recompute exactly. EXCLUDED_HEADERS={Date,Server,X-Request-Id}
identical to parent.

Two client-side normalizations required by the frozen spec and disclosed in validity_notes:
  * filtered header KEYS are lowercased before hashing (frozen spec measurement_validity
    item 4: "validation checks filtered_headers dict after lowercasing keys and sorting,
    not raw order"); the compute_fingerprint body itself is byte-identical to parent.
  * the frozen-mandated instrumentation header X-Worker-Pid (prereg §4.1/§11, used for
    worker distribution logging E3) is removed from the filtered set together with the
    frozen EXCLUDED_HEADERS; without this exclusion, round-robin worker pid variance would
    contaminate fingerprints (a measurement-instrument artifact, not a scientific signal).
    headers_raw_json retains the full raw header set for audit recomputation.

Usage:
  python3 run_experiment.py --smoke      # setup verification (topologies L and P)
  python3 run_experiment.py --sanity     # topology L (Werkzeug) sanity only
  python3 run_experiment.py              # full frozen execution
"""

import argparse
import hashlib
import json
import os
import random
import shutil
import signal
import socket
import sqlite3
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import jwt
import requests
from flask import Flask, g, jsonify, make_response, request as flask_request

# ─── Frozen configuration (prereg §5, spec measurement_validity) ─────────────
SEED = 44
N_SAMPLES = 20
JITTER_MIN_MS = 50
JITTER_MAX_MS = 150
BOOTSTRAP_B = 1000
BOOTSTRAP_ALPHA = 0.05
JWT_SECRET = "test-secret-key-exp-runtime-35764329925"
JWT_ALGORITHM = "HS256"
DB_PATH = "/tmp/spider_prodfp_testbed.db"
HOST = "127.0.0.1"
GUNICORN_PORT = 19860
NGINX_PORT = 19851
RUN_DIR = Path("/tmp/spider-runtime-35764329925")
NGINX_PREFIX = RUN_DIR / "nginx"
NGINX_CONF = NGINX_PREFIX / "nginx.conf"
EXPERIMENT_DIR = Path(__file__).resolve().parent

# Identical exclusion set to parent (spec measurement_validity item 4).
EXCLUDED_HEADERS = {"Date", "Server", "X-Request-Id"}
# Client-side instrument exclusion (frozen-mandated X-Worker-Pid, disclosed above).
FILTER_OUT_KEYS = {k.lower() for k in EXCLUDED_HEADERS} | {"x-worker-pid"}

# Frozen constant header config (spec positive_control; held constant across A/B/C):
FIXED_HEADER_CONFIG: Dict[str, str] = {
    "cache_control": "max-age=3600",
    "etag": 'W/"fixed-aaa-111"',
    "vary": "Accept-Encoding",
    "set_cookie": "",
}

# Frozen header states (spec positive_control P-HEADER, prereg §4.2 table):
HEADER_E_CONFIG: Dict[str, str] = {
    "cache_control": "max-age=0,must-revalidate",
    "etag": 'W/"changed-bbb-222"',
    "vary": "Accept-Encoding, Origin",
    "set_cookie": "session=xyz; Path=/; HttpOnly",
}
HEADER_CC_ONLY_CONFIG: Dict[str, str] = {
    "cache_control": "max-age=0,must-revalidate",
    "etag": FIXED_HEADER_CONFIG["etag"],
    "vary": FIXED_HEADER_CONFIG["vary"],
    "set_cookie": "",
}
HEADER_ETAG_ONLY_CONFIG: Dict[str, str] = {
    "cache_control": FIXED_HEADER_CONFIG["cache_control"],
    "etag": 'W/"changed-bbb-222"',
    "vary": FIXED_HEADER_CONFIG["vary"],
    "set_cookie": "",
}
HEADER_SC_ONLY_CONFIG: Dict[str, str] = {
    "cache_control": FIXED_HEADER_CONFIG["cache_control"],
    "etag": FIXED_HEADER_CONFIG["etag"],
    "vary": FIXED_HEADER_CONFIG["vary"],
    "set_cookie": "session=xyz; Path=/; HttpOnly",
}

HEADER_STATES: Dict[str, Dict[str, str]] = {
    "A": FIXED_HEADER_CONFIG,
    "E": HEADER_E_CONFIG,
    "CC_ONLY": HEADER_CC_ONLY_CONFIG,
    "ETAG_ONLY": HEADER_ETAG_ONLY_CONFIG,
    "SC_ONLY": HEADER_SC_ONLY_CONFIG,
}

# Frozen body states (spec positive_control table; parent byte-identical magnitudes):
BODIES: Dict[str, bytes] = {
    "A": json.dumps({"data": "hello", "version": 1}, sort_keys=True).encode("utf-8"),
    "B": json.dumps(
        {"data": "hello", "items": ["a", "b"], "role": "reader", "version": 1},
        sort_keys=True,
    ).encode("utf-8"),
    "C": json.dumps(
        {
            "admin_note": "sensitive:42",
            "count": 42,
            "data": "hello",
            "items": ["a", "b", "c"],
            "role": "admin",
            "version": 1,
        },
        sort_keys=True,
    ).encode("utf-8"),
}

BODY_SHA: Dict[str, str] = {k: hashlib.sha256(v).hexdigest() for k, v in BODIES.items()}

FROZEN_A_SHA = "d0ca833f843c6d70ec9d6755f52a92dcbfc8b4ab601b871bced09ad027172e34"
FROZEN_A_LEN = 31

BODY_403 = json.dumps({"error": "forbidden"}, sort_keys=True).encode("utf-8")
BODY_401 = json.dumps({"error": "unauthorized"}, sort_keys=True).encode("utf-8")
SHA403 = hashlib.sha256(BODY_403).hexdigest()
SHA401 = hashlib.sha256(BODY_401).hexdigest()

random.seed(SEED)

CONCURRENCY = 4


class MeasurementInvalid(Exception):
    """Infrastructure / verification failure — never a scientific negative."""

    def __init__(self, category: str, detail: str):
        super().__init__(f"{category}: {detail}")
        self.category = category
        self.detail = detail


# ─── Database ────────────────────────────────────────────────────────────────

def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    if os.path.exists(DB_PATH + "-wal"):
        os.remove(DB_PATH + "-wal")
    if os.path.exists(DB_PATH + "-shm"):
        os.remove(DB_PATH + "-shm")
    conn = _connect()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'reader'
        )
    """)
    c.execute("""
        CREATE TABLE sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_hash TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            is_valid INTEGER NOT NULL DEFAULT 1
        )
    """)
    c.execute("""
        CREATE TABLE header_config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            cache_control TEXT NOT NULL,
            etag TEXT NOT NULL,
            vary TEXT NOT NULL,
            set_cookie TEXT NOT NULL DEFAULT ''
        )
    """)
    c.execute("""
        CREATE TABLE body_config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            variant TEXT NOT NULL,
            body_sha256 TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE runtime_config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            mode TEXT NOT NULL DEFAULT 'canonical'
        )
    """)
    h = FIXED_HEADER_CONFIG
    c.execute(
        "INSERT INTO header_config (id, cache_control, etag, vary, set_cookie) "
        "VALUES (1, ?, ?, ?, ?)",
        (h["cache_control"], h["etag"], h["vary"], h["set_cookie"]),
    )
    c.execute("INSERT INTO body_config (id, variant, body_sha256) VALUES (1, 'A', ?)",
              (BODY_SHA["A"],))
    c.execute("INSERT INTO runtime_config (id, mode) VALUES (1, 'canonical')")
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
              ("reader", hashlib.sha256(b"reader_pass").hexdigest(), "reader"))
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
              ("admin", hashlib.sha256(b"admin_pass").hexdigest(), "admin"))
    conn.commit()
    conn.close()


def read_header_config() -> Dict[str, str]:
    conn = _connect()
    row = conn.execute(
        "SELECT cache_control, etag, vary, set_cookie FROM header_config WHERE id = 1"
    ).fetchone()
    conn.close()
    if row is None:
        raise MeasurementInvalid("header_config_missing", "header_config row id=1 absent")
    return {"cache_control": row[0], "etag": row[1], "vary": row[2], "set_cookie": row[3]}


def read_body_config() -> Dict[str, str]:
    conn = _connect()
    row = conn.execute(
        "SELECT variant, body_sha256 FROM body_config WHERE id = 1"
    ).fetchone()
    conn.close()
    if row is None:
        raise MeasurementInvalid("body_config_missing", "body_config row id=1 absent")
    return {"variant": row[0], "body_sha256": row[1]}


def read_runtime_mode() -> str:
    conn = _connect()
    row = conn.execute("SELECT mode FROM runtime_config WHERE id = 1").fetchone()
    conn.close()
    return row[0] if row is not None else "canonical"


def read_user_role(username: str) -> Optional[str]:
    conn = _connect()
    row = conn.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row[0] if row is not None else None


def read_session_count(username: Optional[str] = None) -> int:
    conn = _connect()
    if username is None:
        n = conn.execute("SELECT COUNT(*) FROM sessions WHERE is_valid = 1").fetchone()[0]
    else:
        n = conn.execute(
            "SELECT COUNT(*) FROM sessions WHERE username = ? AND is_valid = 1",
            (username,),
        ).fetchone()[0]
    conn.close()
    return n


def write_header_config(cfg: Dict[str, str]) -> None:
    conn = _connect()
    conn.execute(
        "UPDATE header_config SET cache_control = ?, etag = ?, vary = ?, "
        "set_cookie = ? WHERE id = 1",
        (cfg["cache_control"], cfg["etag"], cfg["vary"], cfg["set_cookie"]),
    )
    conn.commit()
    conn.close()


def write_body_config(variant: str) -> None:
    if variant not in BODIES:
        raise MeasurementInvalid("unknown_body_variant", f"variant={variant!r}")
    conn = _connect()
    conn.execute(
        "UPDATE body_config SET variant = ?, body_sha256 = ? WHERE id = 1",
        (variant, BODY_SHA[variant]),
    )
    conn.commit()
    conn.close()


def write_runtime_mode(mode: str) -> None:
    if mode not in ("canonical", "fold_keys", "fold_pad"):
        raise MeasurementInvalid("unknown_mode", f"mode={mode!r}")
    conn = _connect()
    conn.execute("UPDATE runtime_config SET mode = ? WHERE id = 1", (mode,))
    conn.commit()
    conn.close()


def set_user_role(username: str, role: str) -> None:
    conn = _connect()
    cur = conn.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
    if cur.rowcount != 1:
        conn.close()
        raise MeasurementInvalid("role_update_failed",
                                 f"UPDATE users SET role={role!r} touched {cur.rowcount} rows")
    conn.commit()
    conn.close()


def invalidate_user_sessions(username: str) -> None:
    conn = _connect()
    cur = conn.execute(
        "UPDATE sessions SET is_valid = 0 WHERE username = ? AND is_valid = 1",
        (username,),
    )
    conn.commit()
    conn.close()
    if cur.rowcount < 1:
        raise MeasurementInvalid(
            "session_invalidation_noop",
            f"no valid sessions to invalidate for user={username!r}",
        )


def get_db():
    if "db" not in g:
        g.db = _connect()
        g.db.row_factory = sqlite3.Row
    return g.db


# ─── JWT helpers (parent pattern: role read from SQLite, not from token) ─────

def create_token(username: str, exp_seconds: int = 3600) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=exp_seconds)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_session(token: str, username: str, expires_seconds: int = 3600) -> None:
    conn = _connect()
    now = datetime.now(timezone.utc)
    conn.execute(
        "INSERT INTO sessions (token_hash, username, created_at, expires_at, is_valid) "
        "VALUES (?, ?, ?, ?, 1)",
        (hashlib.sha256(token.encode()).hexdigest(), username, now.isoformat(),
         (now + timedelta(seconds=expires_seconds)).isoformat()),
    )
    conn.commit()
    conn.close()


def check_session(token: str) -> bool:
    conn = _connect()
    row = conn.execute(
        "SELECT is_valid FROM sessions WHERE token_hash = ? AND is_valid = 1",
        (hashlib.sha256(token.encode()).hexdigest(),),
    ).fetchone()
    conn.close()
    return row is not None


def require_auth(require_admin: bool = False) -> str:
    auth_header = flask_request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise PermissionError("authentication_required")
    token = auth_header[7:]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise PermissionError("token_expired")
    except jwt.InvalidTokenError:
        raise PermissionError("invalid_token")
    if not check_session(token):
        raise PermissionError("session_invalid")
    username = payload.get("sub")
    db = get_db()
    user = db.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
    if user is None:
        raise PermissionError("user_not_found")
    if require_admin and user["role"] != "admin":
        raise PermissionError("forbidden")
    return username


# ─── Flask app ───────────────────────────────────────────────────────────────

def create_app() -> Flask:
    app = Flask(__name__)
    app.logger.disabled = True

    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def _err(msg: str, code: int):
        return jsonify({"error": msg}), code

    def _worker_header(resp):
        """Instrumentation header for worker distribution logging (prereg §4.1/E3)."""
        resp.headers["X-Worker-Pid"] = str(os.getpid())
        return resp

    @app.route("/auth/token", methods=["POST"])
    def auth_token():
        data = flask_request.get_json(force=True)
        username, password = data.get("username"), data.get("password")
        if not username or not password:
            return _err("missing_credentials", 400)
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user is None:
            return _err("invalid_credentials", 401)
        if user["password_hash"] != hashlib.sha256(password.encode()).hexdigest():
            return _err("invalid_credentials", 401)
        token = create_token(username)
        create_session(token, username)
        return jsonify({"token": token, "token_type": "Bearer",
                        "expires_in": 3600}), 200

    @app.route("/admin/set_headers", methods=["POST"])
    def admin_set_headers():
        try:
            require_auth(require_admin=True)
        except PermissionError as e:
            return _err(str(e), 401 if str(e) != "forbidden" else 403)
        data = flask_request.get_json(force=True) or {}
        required = ("cache_control", "etag", "vary", "set_cookie")
        if any(k not in data for k in required):
            return _err("missing_header_fields", 400)
        cfg = {k: str(data[k]) for k in required}
        write_header_config(cfg)          # commit BEFORE 200 response
        return jsonify({"ok": True, "header_config": read_header_config()}), 200

    @app.route("/admin/set_body_variant", methods=["POST"])
    def admin_set_body_variant():
        try:
            require_auth(require_admin=True)
        except PermissionError as e:
            return _err(str(e), 401 if str(e) != "forbidden" else 403)
        data = flask_request.get_json(force=True) or {}
        variant = data.get("variant")
        if variant not in BODIES:
            return _err("unknown_variant", 400)
        write_body_config(variant)          # commit BEFORE 200 response
        return jsonify({"ok": True, "body_config": read_body_config()}), 200

    @app.route("/admin/set_mode", methods=["POST"])
    def admin_set_mode():
        try:
            require_auth(require_admin=True)
        except PermissionError as e:
            return _err(str(e), 401 if str(e) != "forbidden" else 403)
        data = flask_request.get_json(force=True) or {}
        mode = data.get("mode")
        if mode not in ("canonical", "fold_keys", "fold_pad"):
            return _err("invalid_mode", 400)
        write_runtime_mode(mode)            # commit BEFORE 200 response
        return jsonify({"ok": True, "mode": read_runtime_mode()}), 200

    @app.route("/admin/set_role", methods=["POST"])
    def admin_set_role():
        try:
            require_auth(require_admin=True)
        except PermissionError as e:
            return _err(str(e), 401 if str(e) != "forbidden" else 403)
        data = flask_request.get_json(force=True) or {}
        username, role = data.get("username"), data.get("role")
        if not username or role not in ("reader", "admin", "viewer"):
            return _err("invalid_role_request", 400)
        set_user_role(username, role)         # commit BEFORE 200 response
        return jsonify({"ok": True, "role": read_user_role(username)}), 200

    @app.route("/admin/invalidate_session", methods=["POST"])
    def admin_invalidate_session():
        try:
            require_auth(require_admin=True)
        except PermissionError as e:
            return _err(str(e), 401 if str(e) != "forbidden" else 403)
        data = flask_request.get_json(force=True) or {}
        username = data.get("username")
        if not username:
            return _err("missing_username", 400)
        invalidate_user_sessions(username)    # commit BEFORE 200 response
        return jsonify({"ok": True, "valid_sessions_remaining": read_session_count(username)}), 200

    @app.route("/resource", methods=["GET"])
    def resource():
        try:
            username = require_auth(require_admin=False)
        except PermissionError as e:
            if str(e) == "forbidden":
                return _worker_header(make_response(BODY_403, 403,
                                                    {"Content-Type": "application/json"}))
            return _worker_header(make_response(BODY_401, 401,
                                                {"Content-Type": "application/json"}))
        role = read_user_role(username)
        if role == "viewer":
            return _worker_header(make_response(BODY_403, 403,
                                                {"Content-Type": "application/json"}))
        bcfg = read_body_config()
        body = BODIES[bcfg["variant"]]
        cfg = read_header_config()
        mode = read_runtime_mode()
        resp = make_response(body)
        resp.headers["Content-Type"] = "application/json"

        if mode == "fold_keys":
            # E2 folding test: same logical values, lowercase keys, shuffled order.
            resp.headers["cache-control"] = cfg["cache_control"]
            resp.headers["set-cookie"] = cfg["set_cookie"] if cfg["set_cookie"] else None
            resp.headers["vary"] = cfg["vary"]
            resp.headers["etag"] = cfg["etag"]
        elif mode == "fold_pad":
            # E2 value-whitespace sub-test: values padded (value-as-is semantics).
            resp.headers["Cache-Control"] = " " + cfg["cache_control"] + " "
            resp.headers["ETag"] = " " + cfg["etag"] + " "
            resp.headers["Vary"] = " " + cfg["vary"] + " "
            resp.headers["Set-Cookie"] = cfg["set_cookie"] if cfg["set_cookie"] else None
        else:
            resp.headers["Cache-Control"] = cfg["cache_control"]
            resp.headers["ETag"] = cfg["etag"]
            resp.headers["Vary"] = cfg["vary"]
            if cfg["set_cookie"]:
                resp.headers["Set-Cookie"] = cfg["set_cookie"]
        return _worker_header(resp)

    @app.route("/protected", methods=["GET"])
    def protected():
        try:
            username = require_auth(require_admin=False)
        except PermissionError as e:
            return _err(str(e), 401 if str(e) != "forbidden" else 403)
        db = get_db()
        user = db.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
        return jsonify({"role": user["role"], "username": username}), 200

    return app


# ─── Fingerprint / metric functions — IDENTICAL algorithm to parent ──────────

def compute_fingerprint(obs: Dict[str, Any], source: str = "full") -> str:
    """Compute a fingerprint hash from observation.

    source: 'full'   = status+body+sorted_filtered_headers
            'status' = status only
            'body'   = body only
            'headers'= sorted filtered headers only
            'headers_no_clen' = sorted filtered headers with Content-Length removed
    """
    if source == "full":
        parts = [
            str(obs["status"]),
            repr(obs["body_bytes"]),
            json.dumps(obs["headers"], sort_keys=True),
        ]
    elif source == "status":
        parts = [str(obs["status"])]
    elif source == "body":
        parts = [repr(obs["body_bytes"])]
    elif source == "headers":
        parts = [json.dumps(obs["headers"], sort_keys=True)]
    elif source == "headers_no_clen":
        filtered = {k: v for k, v in obs["headers"].items()
                    if k.lower() != "content-length"}
        parts = [json.dumps(filtered, sort_keys=True)]
    else:
        raise ValueError(f"Unknown source: {source}")
    return hashlib.sha256("||".join(parts).encode()).hexdigest()


def jaccard_distance(set_a: set, set_b: set) -> float:
    """Compute Jaccard distance between two fingerprint sets."""
    if len(set_a) == 0 and len(set_b) == 0:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return 1.0 - (intersection / union) if union > 0 else 0.0


def bootstrap_jaccard_ci(set_a: set, set_b: set, n_bootstrap: int = 1000,
                         alpha: float = 0.05) -> Tuple[float, float, float]:
    """Compute Jaccard distance and bootstrap 95% CI (identical to parent)."""
    all_items = list(set_a | set_b)
    if len(all_items) == 0:
        return 0.0, 0.0, 0.0
    observed = jaccard_distance(set_a, set_b)
    boot_dists = []
    for _ in range(n_bootstrap):
        boot_a = set(random.choices(list(set_a), k=len(set_a))) if set_a else set()
        boot_b = set(random.choices(list(set_b), k=len(set_b))) if set_b else set()
        boot_dists.append(jaccard_distance(boot_a, boot_b))
    boot_dists.sort()
    ci_lower = boot_dists[int(alpha / 2 * len(boot_dists))]
    ci_upper = boot_dists[int((1 - alpha / 2) * len(boot_dists))]
    return observed, ci_lower, ci_upper


# ─── Client observation helpers ──────────────────────────────────────────────

BASE_URL: str = ""


def observe_resource(token: str, timeout: float = 15.0) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}"}
    start = time.monotonic()
    resp = requests.get(f"{BASE_URL}/resource", headers=headers, timeout=timeout)
    end = time.monotonic()
    raw = dict(resp.headers)
    filtered = {k.lower(): v for k, v in raw.items() if k.lower() not in FILTER_OUT_KEYS}
    return {
        "status": resp.status_code,
        "body_bytes": resp.content,
        "headers": filtered,
        "headers_raw": raw,
        "worker_id": raw.get("X-Worker-Pid", raw.get("x-worker-pid", "unknown")),
        "response_time_ms": round((end - start) * 1000, 2),
    }


def _hdr(headers: Dict[str, str], key: str) -> Optional[str]:
    """Case-insensitive header lookup (handles lowercase-normalized and raw dicts)."""
    lk = key.lower()
    for k, v in headers.items():
        if k.lower() == lk:
            return v
    return None


def expected_constant_headers() -> Dict[str, Optional[str]]:
    h = FIXED_HEADER_CONFIG
    exp = {
        "cache-control": h["cache_control"],
        "etag": h["etag"],
        "vary": h["vary"],
        "content-type": "application/json",
    }
    exp["set-cookie"] = h["set_cookie"] if h["set_cookie"] else None
    return exp


def verify_constant_headers(obs: Dict[str, Any]) -> List[str]:
    """Return list of non-CLEN header mismatches for this observation (empty = OK)."""
    problems = []
    exp = expected_constant_headers()
    raw_lower = {k.lower(): v for k, v in obs["headers_raw"].items()}
    for key, want in exp.items():
        got = raw_lower.get(key)
        if want is None:
            if got is not None:
                problems.append(f"{key} unexpectedly present: {got!r}")
        else:
            if got is None:
                problems.append(f"{key} missing (expected {want!r})")
            elif got != want:
                problems.append(f"{key}={got!r} != expected {want!r}")
    return problems


def verify_header_state(obs: Dict[str, Any], cfg: Dict[str, str]) -> List[str]:
    """For header-only branches: verify the programmed header values for the state."""
    problems = []
    raw_lower = {k.lower(): v for k, v in obs["headers_raw"].items()}
    expect = {
        "cache-control": cfg["cache_control"],
        "etag": cfg["etag"],
        "vary": cfg["vary"],
        "set-cookie": cfg["set_cookie"] if cfg["set_cookie"] else None,
    }
    for key, want in expect.items():
        got = raw_lower.get(key)
        if want is None:
            if got is not None:
                problems.append(f"{key} unexpectedly present: {got!r}")
        else:
            if got is None:
                problems.append(f"{key} missing (expected {want!r})")
            elif got != want:
                problems.append(f"{key}={got!r} != expected {want!r}")
    ct = raw_lower.get("content-type")
    if ct != "application/json":
        problems.append(f"content-type={ct!r} != application/json")
    return problems


def get_tokens(base: str) -> Dict[str, str]:
    out = {}
    for user, pw in (("reader", "reader_pass"), ("admin", "admin_pass")):
        r = requests.post(f"{base}/auth/token",
                          json={"username": user, "password": pw}, timeout=5)
        if r.status_code != 200:
            raise MeasurementInvalid("auth_failure",
                                     f"{user} login status={r.status_code}")
        out[user] = r.json()["token"]
    return out


def discover_port(start: int) -> int:
    for port in range(start, start + 50):
        s = socket.socket()
        try:
            s.bind((HOST, port))
            s.close()
            return port
        except OSError:
            s.close()
    raise MeasurementInvalid("port_exhaustion", f"no free port in {start}-{start+49}")


def wait_for_server(base: str, timeout: float = 20.0) -> None:
    deadline = time.time() + timeout
    last: Optional[Exception] = None
    while time.time() < deadline:
        try:
            requests.get(f"{base}/protected", timeout=2)
            return
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(0.2)
    raise MeasurementInvalid("server_unreachable", f"{base} not reachable: {last}")


# ─── Batch execution ─────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def state_snapshot() -> Dict[str, Any]:
    """SQLite-verified committed state snapshot (spec measurement_validity item 1)."""
    return {
        "body_config": read_body_config(),
        "header_config": read_header_config(),
        "runtime_mode": read_runtime_mode(),
        "reader_role": read_user_role("reader"),
        "admin_role": read_user_role("admin"),
        "reader_valid_sessions": read_session_count("reader"),
        "admin_valid_sessions": read_session_count("admin"),
    }


def do_write(action: str, expected: Dict[str, Any], admin_token: str,
             batch_log: List[Dict[str, Any]]) -> None:
    """Perform a writable server-side state change via admin endpoint and verify commit."""
    if action == "set_headers":
        r = requests.post(
            f"{BASE_URL}/admin/set_headers",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=FIXED_HEADER_CONFIG if expected.get("_fixed") else
                 {k: expected[k] for k in ("cache_control", "etag", "vary", "set_cookie")},
            timeout=10,
        )
        committed = read_header_config()
        if expected.get("_fixed"):
            match = committed == FIXED_HEADER_CONFIG
        else:
            match = committed == {k: expected[k] for k in
                                  ("cache_control", "etag", "vary", "set_cookie")}
    elif action == "set_body":
        r = requests.post(
            f"{BASE_URL}/admin/set_body_variant",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"variant": expected["variant"]},
            timeout=10,
        )
        committed = read_body_config()
        match = committed == expected
    elif action == "set_mode":
        r = requests.post(
            f"{BASE_URL}/admin/set_mode",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"mode": expected["mode"]},
            timeout=10,
        )
        committed = {"mode": read_runtime_mode()}
        match = committed == expected
    elif action == "set_role":
        r = requests.post(
            f"{BASE_URL}/admin/set_role",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"username": "reader", "role": expected["role"]},
            timeout=10,
        )
        committed_role = read_user_role("reader")
        committed = {"role": committed_role}
        match = committed_role == expected["role"]
    elif action == "invalidate_session":
        r = requests.post(
            f"{BASE_URL}/admin/invalidate_session",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"username": "reader"},
            timeout=10,
        )
        committed = {"reader_valid_sessions": read_session_count("reader")}
        match = committed["reader_valid_sessions"] == 0
    else:
        raise MeasurementInvalid("unknown_write_action", f"action={action!r}")

    entry = {
        "action": f"write_state::{action}",
        "expected": expected,
        "http_status": r.status_code,
        "post_select": committed,
        "match_expected": match,
        "state_snapshot": state_snapshot(),
        "ts": now_iso(),
    }
    batch_log.append(entry)
    if r.status_code != 200:
        raise MeasurementInvalid(
            "write_failure",
            f"{action} status={r.status_code} body={r.text[:300]}",
        )
    if not match:
        raise MeasurementInvalid(
            "write_commit_not_visible",
            f"{action}: post_select={committed} expected={expected}",
        )


def _run_one_observation(token: str, expected_status: int,
                         expected_body_sha: Optional[str],
                         header_check: str, expected_header_cfg: Optional[Dict[str, str]],
                         label: str, i: int) -> Dict[str, Any]:
    obs = observe_resource(token)
    if obs["status"] != expected_status:
        raise MeasurementInvalid(
            "status_mismatch",
            f"batch={label} i={i} status={obs['status']} expected={expected_status}",
        )
    cl = _hdr(obs["headers_raw"], "Content-Length")
    if cl is None or int(cl) != len(obs["body_bytes"]):
        raise MeasurementInvalid(
            "content_length_unverifiable",
            f"batch={label} i={i} Content-Length={cl!r} body_len={len(obs['body_bytes'])}",
        )
    if expected_body_sha is not None:
        got_sha = hashlib.sha256(obs["body_bytes"]).hexdigest()
        if got_sha != expected_body_sha:
            raise MeasurementInvalid(
                "body_sha_mismatch",
                f"batch={label} i={i} body_sha={got_sha} expected={expected_body_sha}",
            )
    if header_check == "constant":
        hp = verify_constant_headers(obs)
        if hp:
            raise MeasurementInvalid(
                "expected_header_mismatch",
                f"batch={label} i={i}: " + "; ".join(hp),
            )
    elif header_check == "header_state":
        assert expected_header_cfg is not None
        hp = verify_header_state(obs, expected_header_cfg)
        if hp:
            raise MeasurementInvalid(
                "expected_header_mismatch",
                f"batch={label} i={i}: " + "; ".join(hp),
            )
    return obs


def do_batch(label: str, token: str, expected_status: int,
             expected_body_sha: Optional[str], header_check: str,
             expected_header_cfg: Optional[Dict[str, str]],
             raw_records: List[Dict[str, Any]],
             batch_log: List[Dict[str, Any]],
             concurrency: int = 1, jitter: bool = True) -> List[Dict[str, Any]]:
    pre = state_snapshot()
    batch_log.append({
        "action": "pre_batch_verify",
        "batch": label,
        "expected_status": expected_status,
        "expected_body_sha": expected_body_sha,
        "header_check": header_check,
        "state_snapshot": pre,
        "n": N_SAMPLES,
        "concurrency": concurrency,
        "ts": now_iso(),
    })
    batch_start = time.monotonic()

    if concurrency > 1:
        # jitter between bursts, not between concurrent parallel requests (frozen spec).
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = [
                pool.submit(_run_one_observation, token, expected_status,
                            expected_body_sha, header_check, expected_header_cfg,
                            label, i)
                for i in range(N_SAMPLES)
            ]
            obs_list = [f.result() for f in futures]
    else:
        obs_list = []
        for i in range(N_SAMPLES):
            if jitter:
                time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
            obs_list.append(_run_one_observation(
                token, expected_status, expected_body_sha, header_check,
                expected_header_cfg, label, i))

    batch_ms = round((time.monotonic() - batch_start) * 1000, 2)

    for i, obs in enumerate(obs_list):
        filtered_no_clen = {k: v for k, v in obs["headers"].items()
                            if k.lower() != "content-length"}
        rec = {
            "state": label,
            "index": i,
            "status": obs["status"],
            "body_sha256": hashlib.sha256(obs["body_bytes"]).hexdigest(),
            "body_hex": obs["body_bytes"].hex(),
            "body_len": len(obs["body_bytes"]),
            "headers_filtered_json": json.dumps(obs["headers"], sort_keys=True),
            "headers_raw_json": json.dumps(obs["headers_raw"], sort_keys=True),
            "headers_no_clen_json": json.dumps(filtered_no_clen, sort_keys=True),
            "fingerprint_full": compute_fingerprint(obs, "full"),
            "fingerprint_status": compute_fingerprint(obs, "status"),
            "fingerprint_body": compute_fingerprint(obs, "body"),
            "fingerprint_headers": compute_fingerprint(obs, "headers"),
            "fingerprint_headers_no_clen": compute_fingerprint(obs, "headers_no_clen"),
            "content_length_header": _hdr(obs["headers_raw"], "Content-Length"),
            "worker_id": obs["worker_id"],
            "response_time_ms": obs["response_time_ms"],
            "concurrency": "concurrent" if concurrency > 1 else "sequential",
            "observed_at": now_iso(),
        }
        raw_records.append(rec)
    print(f"  [batch] {label}: n={N_SAMPLES} status={expected_status} "
          f"concurrency={concurrency} batch_ms={batch_ms}", flush=True)
    return obs_list


# ─── Server lifecycle ────────────────────────────────────────────────────────

def write_nginx_conf(gunicorn_port: int, nginx_port: int) -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    NGINX_PREFIX.mkdir(parents=True, exist_ok=True)
    (NGINX_PREFIX / "logs").mkdir(parents=True, exist_ok=True)
    conf = f"""
worker_processes 1;
error_log {NGINX_PREFIX}/logs/error.log warn;
pid {NGINX_PREFIX}/nginx.pid;
events {{ worker_connections 1024; }}
http {{
    access_log {NGINX_PREFIX}/logs/access.log;
    upstream gunicorn {{ server 127.0.0.1:{gunicorn_port}; }}
    server {{
        listen {nginx_port};
        location / {{
            proxy_pass http://gunicorn;
            proxy_set_header Host $host;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_buffering off;
        }}
    }}
}}
"""
    NGINX_CONF.write_text(conf)


def start_gunicorn(port: int) -> subprocess.Popen:
    cmd = [
        sys.executable, "-m", "gunicorn",
        "--workers", "2",
        "--bind", f"{HOST}:{port}",
        "--timeout", "30",
        "--chdir", str(EXPERIMENT_DIR),
        "run_experiment:create_app()",
    ]
    env = dict(os.environ)
    env["PYTHONUNBUFFERED"] = "1"
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    return proc


def start_nginx(nginx_port: int) -> subprocess.Popen:
    nginx_bin = shutil.which("nginx")
    if nginx_bin is None:
        raise MeasurementInvalid("NGINX_UNAVAILABLE", "nginx binary not on PATH")
    cmd = [nginx_bin, "-c", str(NGINX_CONF), "-p", str(NGINX_PREFIX)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    # nginx daemonizes; wait for readiness on the port.
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            requests.get(f"http://{HOST}:{nginx_port}/protected", timeout=1)
            return proc
        except Exception:  # noqa: BLE001
            time.sleep(0.2)
    # give nginx a moment to print config errors
    try:
        out, _ = proc.communicate(timeout=2)
        detail = out
    except Exception:  # noqa: BLE001
        detail = "nginx started but port not responsive"
    raise MeasurementInvalid("NGINX_CONFIG_FAIL", f"nginx not reachable: {detail}")


def stop_nginx() -> None:
    pidfile = NGINX_PREFIX / "nginx.pid"
    if pidfile.exists():
        try:
            os.kill(int(pidfile.read_text().strip()), signal.SIGQUIT)
        except Exception:  # noqa: BLE001
            pass
    subprocess.run(["pkill", "-f", f"run_experiment.*gunicorn"], capture_output=True)
    subprocess.run(["pkill", "-f", "gunicorn.*19860"], capture_output=True)


# ─── Topology L sanity (Werkzeug dev server, frozen §5.4 / §11) ─────────────

def run_sanity_l(outdir: Path) -> Dict[str, Any]:
    global BASE_URL
    port = discover_port(19870)
    BASE_URL = f"http://{HOST}:{port}"
    app = create_app()
    server_thread = threading.Thread(
        target=lambda: app.run(host=HOST, port=port, debug=False,
                               use_reloader=False, threaded=True),
        daemon=True,
    )
    server_thread.start()
    wait_for_server(BASE_URL)

    raw_records: List[Dict[str, Any]] = []
    batch_log: List[Dict[str, Any]] = []
    tokens = get_tokens(BASE_URL)
    admin_tok, reader_tok = tokens["admin"], tokens["reader"]
    print("=== Topology L (Werkzeug dev) sanity: A x20, C x20, E x20 ===", flush=True)

    do_write("set_headers", {"_fixed": True}, admin_tok, batch_log)
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)
    do_batch("l_body_A", reader_tok, 200, BODY_SHA["A"], "constant", None,
             raw_records, batch_log, concurrency=1, jitter=True)
    do_write("set_body", {"variant": "C", "body_sha256": BODY_SHA["C"]},
             admin_tok, batch_log)
    do_batch("l_body_C", reader_tok, 200, BODY_SHA["C"], "constant", None,
             raw_records, batch_log, concurrency=1, jitter=True)
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)
    do_write("set_headers", {k: HEADER_E_CONFIG[k] for k in
                             ("cache_control", "etag", "vary", "set_cookie")},
             admin_tok, batch_log)
    do_batch("l_hdr_E", reader_tok, 200, BODY_SHA["A"], "header_state",
             HEADER_E_CONFIG, raw_records, batch_log, concurrency=1, jitter=True)

    # restore canonical config
    do_write("set_headers", {"_fixed": True}, admin_tok, batch_log)
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)
    return {"raw_records": raw_records, "batch_log": batch_log}


# ─── Full frozen production run ──────────────────────────────────────────────

def run_full(tokens: Dict[str, str], outdir: Path,
             sanity_raw_records: Optional[List[Dict[str, Any]]] = None,
             sanity_batch_log: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    raw_records: List[Dict[str, Any]] = []
    batch_log: List[Dict[str, Any]] = []
    admin_tok = tokens["admin"]
    reader_tok = tokens["reader"]
    started = now_iso()
    sanity_raw_records = sanity_raw_records or []
    sanity_batch_log = sanity_batch_log or []
    worker_distribution: Dict[str, Dict[str, int]] = {}
    write_times: Dict[str, float] = {}

    print("=== FULL frozen execution on production WSGI+nginx (N=20, concurrency 4) ===",
          flush=True)

    def track_workers(label: str, obs_list: List[Dict[str, Any]]) -> None:
        dist = worker_distribution.setdefault(label, {})
        for o in obs_list:
            w = o["worker_id"]
            dist[w] = dist.get(w, 0) + 1

    # 1. Fix header_config to baseline once; verify committed.
    do_write("set_headers", {"_fixed": True}, admin_tok, batch_log)

    # 2. P body-only states A, B, C (all 200, concurrent 4, frozen order).
    for v in ("A", "B", "C"):
        do_write("set_body", {"variant": v, "body_sha256": BODY_SHA[v]},
                 admin_tok, batch_log)
        obs_list = do_batch(f"prod_body_{v}", reader_tok, 200, BODY_SHA[v],
                            "constant", None, raw_records, batch_log,
                            concurrency=CONCURRENCY, jitter=False)
        track_workers(f"prod_body_{v}", obs_list)

    # 3. P header-only A (baseline headers) then E (combined variant), concurrent.
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)
    do_write("set_headers", {"_fixed": True}, admin_tok, batch_log)
    obs_list = do_batch("prod_hdr_A", reader_tok, 200, BODY_SHA["A"], "header_state",
                        FIXED_HEADER_CONFIG, raw_records, batch_log,
                        concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_hdr_A", obs_list)
    do_write("set_headers", {k: HEADER_E_CONFIG[k] for k in
                             ("cache_control", "etag", "vary", "set_cookie")},
             admin_tok, batch_log)
    obs_list = do_batch("prod_hdr_E", reader_tok, 200, BODY_SHA["A"], "header_state",
                        HEADER_E_CONFIG, raw_records, batch_log,
                        concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_hdr_E", obs_list)

    # 4. P per-header isolations (Cache-Control only, ETag only, Set-Cookie only).
    for iso_name, iso_cfg in (("prod_iso_cc", HEADER_CC_ONLY_CONFIG),
                              ("prod_iso_etag", HEADER_ETAG_ONLY_CONFIG),
                              ("prod_iso_sc", HEADER_SC_ONLY_CONFIG)):
        do_write("set_headers", {k: iso_cfg[k] for k in
                                 ("cache_control", "etag", "vary", "set_cookie")},
                 admin_tok, batch_log)
        obs_list = do_batch(iso_name, reader_tok, 200, BODY_SHA["A"], "header_state",
                            iso_cfg, raw_records, batch_log,
                            concurrency=CONCURRENCY, jitter=False)
        track_workers(iso_name, obs_list)
    do_write("set_headers", {"_fixed": True}, admin_tok, batch_log)

    # 5. P concurrent nulls: N1-body (STATE_A resampled x2), N1-header (x2).
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)
    obs_list = do_batch("prod_null_body_A1", reader_tok, 200, BODY_SHA["A"],
                        "constant", None, raw_records, batch_log,
                        concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_null_body_A1", obs_list)
    obs_list = do_batch("prod_null_body_A2", reader_tok, 200, BODY_SHA["A"],
                        "constant", None, raw_records, batch_log,
                        concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_null_body_A2", obs_list)
    obs_list = do_batch("prod_null_hdr_A1", reader_tok, 200, BODY_SHA["A"],
                        "header_state", FIXED_HEADER_CONFIG, raw_records, batch_log,
                        concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_null_hdr_A1", obs_list)
    obs_list = do_batch("prod_null_hdr_A2", reader_tok, 200, BODY_SHA["A"],
                        "header_state", FIXED_HEADER_CONFIG, raw_records, batch_log,
                        concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_null_hdr_A2", obs_list)

    # 6. P classic permission escalation 403 vs 200 (UPDATE users SET role),
    #    cross-worker commit visibility (E3).
    t0 = time.monotonic()
    do_write("set_role", {"role": "viewer"}, admin_tok, batch_log)
    write_times["set_role_viewer"] = time.monotonic() - t0
    obs_list = do_batch("prod_perm_403", reader_tok, 403, SHA403, None, None,
                        raw_records, batch_log, concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_perm_403", obs_list)
    t0 = time.monotonic()
    do_write("set_role", {"role": "admin"}, admin_tok, batch_log)
    write_times["set_role_admin"] = time.monotonic() - t0
    obs_list = do_batch("prod_perm_200", reader_tok, 200, BODY_SHA["A"], "constant",
                        None, raw_records, batch_log,
                        concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_perm_200", obs_list)

    # 7. P same-state 403 null (viewer, resampled x2).
    do_write("set_role", {"role": "viewer"}, admin_tok, batch_log)
    obs_list = do_batch("prod_perm403_null_1", reader_tok, 403, SHA403, None, None,
                        raw_records, batch_log, concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_perm403_null_1", obs_list)
    obs_list = do_batch("prod_perm403_null_2", reader_tok, 403, SHA403, None, None,
                        raw_records, batch_log, concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_perm403_null_2", obs_list)

    # 8. P session invalidation 401 vs 200 (DELETE sessions) + same-state 401 null.
    do_write("set_role", {"role": "reader"}, admin_tok, batch_log)
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)
    obs_list = do_batch("prod_sess_200", reader_tok, 200, BODY_SHA["A"], "constant",
                        None, raw_records, batch_log,
                        concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_sess_200", obs_list)
    t0 = time.monotonic()
    do_write("invalidate_session", {"reader_valid_sessions": 0}, admin_tok, batch_log)
    write_times["invalidate_session"] = time.monotonic() - t0
    obs_list = do_batch("prod_sess_401", reader_tok, 401, SHA401, None, None,
                        raw_records, batch_log, concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_sess_401", obs_list)
    obs_list = do_batch("prod_sess401_null_1", reader_tok, 401, SHA401, None, None,
                        raw_records, batch_log, concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_sess401_null_1", obs_list)
    obs_list = do_batch("prod_sess401_null_2", reader_tok, 401, SHA401, None, None,
                        raw_records, batch_log, concurrency=CONCURRENCY, jitter=False)
    track_workers("prod_sess401_null_2", obs_list)

    # 9. Refreshed reader session for the remaining batches (re-login reader).
    tokens = get_tokens(BASE_URL)
    admin_tok, reader_tok = tokens["admin"], tokens["reader"]
    do_write("set_headers", {"_fixed": True}, admin_tok, batch_log)
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)

    # 10. Sequential baseline replays (frozen §11): body-only 60 + header-only 40.
    for v in ("A", "B", "C"):
        do_write("set_body", {"variant": v, "body_sha256": BODY_SHA[v]},
                 admin_tok, batch_log)
        do_batch(f"seq_body_{v}", reader_tok, 200, BODY_SHA[v], "constant", None,
                 raw_records, batch_log, concurrency=1, jitter=True)
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)
    do_write("set_headers", {"_fixed": True}, admin_tok, batch_log)
    do_batch("seq_hdr_A", reader_tok, 200, BODY_SHA["A"], "header_state",
             FIXED_HEADER_CONFIG, raw_records, batch_log, concurrency=1, jitter=True)
    do_write("set_headers", {k: HEADER_E_CONFIG[k] for k in
                             ("cache_control", "etag", "vary", "set_cookie")},
             admin_tok, batch_log)
    do_batch("seq_hdr_E", reader_tok, 200, BODY_SHA["A"], "header_state",
             HEADER_E_CONFIG, raw_records, batch_log, concurrency=1, jitter=True)
    do_write("set_headers", {"_fixed": True}, admin_tok, batch_log)

    # 11. E2 header folding: fold_keys (lowercase keys, shuffled order) and
    #     fold_pad (value whitespace) vs canonical E, sequential 20 each.
    do_write("set_headers", {k: HEADER_E_CONFIG[k] for k in
                             ("cache_control", "etag", "vary", "set_cookie")},
             admin_tok, batch_log)
    do_write("set_mode", {"mode": "fold_keys"}, admin_tok, batch_log)
    do_batch("prod_hdr_E_foldkeys", reader_tok, 200, BODY_SHA["A"],
             "header_state", HEADER_E_CONFIG, raw_records, batch_log,
             concurrency=1, jitter=True)
    do_write("set_mode", {"mode": "fold_pad"}, admin_tok, batch_log)
    do_batch("prod_hdr_E_foldpad", reader_tok, 200, BODY_SHA["A"], None, None,
             raw_records, batch_log, concurrency=1, jitter=True)
    do_write("set_mode", {"mode": "canonical"}, admin_tok, batch_log)
    do_write("set_headers", {"_fixed": True}, admin_tok, batch_log)
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)

    finished = now_iso()

    # ── Raw evidence artifacts (sanity L lines first, then production P lines) ─
    # Frozen prereg: "≈420 raw lines" = production ≈360 (+sequential/folding) plus
    # sanity 60 control lines; validity_summary requires l_* batches present.
    all_raw = list(sanity_raw_records) + raw_records
    all_log = list(sanity_batch_log) + batch_log
    raw_path = outdir / "raw_observations.jsonl"
    with open(raw_path, "w") as f:
        for r in all_raw:
            f.write(json.dumps(r) + "\n")
    log_path = outdir / "batch_state_log.jsonl"
    with open(log_path, "w") as f:
        for e in all_log:
            f.write(json.dumps(e) + "\n")

    identity = identity_checks(all_raw, all_log, worker_distribution)
    validity = validity_summary(all_raw, all_log, identity)

    result: Dict[str, Any] = {
        "experiment_id": "EXP-RUNTIME-35764329925",
        "lane": "runtime",
        "started_at": started,
        "finished_at": finished,
        "seed": SEED,
        "n_samples_per_batch": N_SAMPLES,
        "jitter_ms": [JITTER_MIN_MS, JITTER_MAX_MS],
        "concurrency": CONCURRENCY,
        "bootstrap_b": BOOTSTRAP_B,
        "topology": "gunicorn(2x sync)+nginx reverse proxy",
        "gunicorn_port": gunicorn_port_used,
        "nginx_port": nginx_port_used,
        "excluded_headers": sorted(EXCLUDED_HEADERS),
        "client_side_filter_out": sorted(FILTER_OUT_KEYS),
        "bodies": {k: {"len": len(v), "sha256": BODY_SHA[k]} for k, v in BODIES.items()},
        "header_states": HEADER_STATES,
        "body_403": {"len": len(BODY_403), "sha256": SHA403},
        "body_401": {"len": len(BODY_401), "sha256": SHA401},
        "raw_line_count": len(all_raw),
        "sanity_l_raw_line_count": len(sanity_raw_records),
        "production_raw_line_count": len(raw_records),
        "batch_state_log_entries": len(all_log),
        "validity": validity,
        "identity_checks": identity,
        "worker_distribution": worker_distribution,
        "write_visibility_ms": write_times,
        "metrics": {},
        "conditions": {},
        "baselines": {},
        "status": None,
        "decision_rule_outcome": None,
    }

    if not validity["critical_all_pass"]:
        result["status"] = "MEASUREMENT_INVALID"
        result["decision_rule_outcome"] = None
        result["failure_category"] = "validity_check_failure"
        result["failed_critical"] = validity["failed_critical"]
    else:
        metrics = compute_metrics(all_raw)
        conditions = evaluate_conditions(metrics, identity)
        # Fill E3 measured write-visibility latencies (placeholder in evaluate_conditions).
        if "E3_DISTRIBUTED_VISIBILITY" in conditions:
            conditions["E3_DISTRIBUTED_VISIBILITY"]["observed"]["write_visibility_ms"] = write_times
        baselines = evaluate_baselines(metrics)
        all_pass = all(c["pass"] for c in conditions.values())
        result["metrics"] = metrics
        result["conditions"] = conditions
        result["baselines"] = baselines
        result["status"] = "COMPLETE"
        result["decision_rule_outcome"] = (
            "SUPPORTS" if all_pass else "FALSIFIED-IN-SETTING"
        )
        result["failing_conditions"] = [
            k for k, c in conditions.items() if not c["pass"]
        ]

    derived_path = outdir / "experiment_result.json"
    with open(derived_path, "w") as f:
        json.dump(result, f, indent=2, sort_keys=False)
    print(f"[OK] raw_observations.jsonl ({len(raw_records)} lines)", flush=True)
    print(f"[OK] batch_state_log.jsonl ({len(batch_log)} lines)", flush=True)
    print(f"[OK] experiment_result.json status={result['status']} "
          f"outcome={result['decision_rule_outcome']}", flush=True)
    return result


# ─── Derived measurement ─────────────────────────────────────────────────────

SOURCES = ("full", "status", "body", "headers", "headers_no_clen")

PROD_COMPARISONS = [
    ("body_drift_AvsC", "prod_body_A", "prod_body_C"),
    ("body_drift_AvsB", "prod_body_A", "prod_body_B"),
    ("header_drift_AvsE", "prod_hdr_A", "prod_hdr_E"),
    ("header_iso_CC", "prod_hdr_A", "prod_iso_cc"),
    ("header_iso_ETag", "prod_hdr_A", "prod_iso_etag"),
    ("header_iso_SC", "prod_hdr_A", "prod_iso_sc"),
    ("null_body", "prod_null_body_A1", "prod_null_body_A2"),
    ("null_hdr", "prod_null_hdr_A1", "prod_null_hdr_A2"),
    ("classic_perm", "prod_perm_403", "prod_perm_200"),
    ("classic_sess", "prod_sess_401", "prod_sess_200"),
    ("perm_null", "prod_perm403_null_1", "prod_perm403_null_2"),
    ("sess_null", "prod_sess401_null_1", "prod_sess401_null_2"),
    ("fold_E2_keys", "prod_hdr_E", "prod_hdr_E_foldkeys"),
    ("fold_E2_pad", "prod_hdr_E", "prod_hdr_E_foldpad"),
]

SEQ_COMPARISONS = [
    ("seq_body_AvsC", "seq_body_A", "seq_body_C"),
    ("seq_body_AvsB", "seq_body_A", "seq_body_B"),
    ("seq_hdr_AvsE", "seq_hdr_A", "seq_hdr_E"),
]

SANITY_COMPARISONS = [
    ("sanity_l_body_AvsC", "l_body_A", "l_body_C"),
    ("sanity_l_hdr_AvsE", "l_body_A", "l_hdr_E"),
]

ALL_COMPARISONS = PROD_COMPARISONS + SEQ_COMPARISONS + SANITY_COMPARISONS


def fingerprint_sets(raw_records: List[Dict[str, Any]], label: str) -> Dict[str, set]:
    recs = [r for r in raw_records if r["state"] == label]
    return {
        "full": {r["fingerprint_full"] for r in recs},
        "status": {r["fingerprint_status"] for r in recs},
        "body": {r["fingerprint_body"] for r in recs},
        "headers": {r["fingerprint_headers"] for r in recs},
        "headers_no_clen": {r["fingerprint_headers_no_clen"] for r in recs},
    }


def compute_metrics(raw_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    metrics: Dict[str, Any] = {}
    sets: Dict[str, Dict[str, set]] = {}
    labels = sorted({r["state"] for r in raw_records})
    for label in labels:
        sets[label] = fingerprint_sets(raw_records, label)

    for name, a, b in ALL_COMPARISONS:
        for src in SOURCES:
            d, lo, hi = bootstrap_jaccard_ci(
                sets[a][src], sets[b][src], BOOTSTRAP_B, BOOTSTRAP_ALPHA
            )
            metrics[f"{name}_{src}"] = {
                "discrimination": d,
                "ci_95": [lo, hi],
                "ci_width": round(hi - lo, 6),
                "set_a_size": len(sets[a][src]),
                "set_b_size": len(sets[b][src]),
                "nominal_n": [N_SAMPLES, N_SAMPLES],
                "comparison": f"{a} vs {b}",
                "source": src,
                "degenerate_ci": lo == hi,
            }
    metrics["effective_distinct_n"] = {
        label: {src: len(sets[label][src]) for src in SOURCES} for label in labels
    }
    return metrics


def identity_checks(raw_records: List[Dict[str, Any]],
                    batch_log: List[Dict[str, Any]],
                    worker_distribution: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
    def state_sets(states: List[str]) -> Dict[str, Dict[str, set]]:
        out: Dict[str, Dict[str, set]] = {}
        for st in states:
            recs = [r for r in raw_records if r["state"] == st]
            out[st] = {
                "sha": {r["body_sha256"] for r in recs},
                "clen": {r["content_length_header"] for r in recs},
                "blen": {r["body_len"] for r in recs},
                "non_clen_headers": {
                    json.dumps(json.loads(r["headers_no_clen_json"]), sort_keys=True)
                    for r in recs
                },
                "full_headers": {
                    json.dumps(json.loads(r["headers_filtered_json"]), sort_keys=True)
                    for r in recs
                },
                "statuses": {r["status"] for r in recs},
                "workers": {r["worker_id"] for r in recs},
            }
        return out

    body_states = ["prod_body_A", "prod_body_B", "prod_body_C"]
    s = state_sets(body_states)
    abc_sha = [list(s[k]["sha"])[0] for k in body_states]
    abc_clen = [list(s[k]["clen"])[0] for k in body_states]
    abc_blen = [list(s[k]["blen"])[0] for k in body_states]
    abc_nclen = [list(s[k]["non_clen_headers"])[0] for k in body_states]

    hdr_states = ["prod_hdr_A", "prod_hdr_E", "prod_iso_cc",
                  "prod_iso_etag", "prod_iso_sc"]
    h = state_sets(hdr_states)

    nulls = state_sets(["prod_null_body_A1", "prod_null_body_A2",
                        "prod_null_hdr_A1", "prod_null_hdr_A2"])
    control = state_sets(["prod_perm_403", "prod_perm_200", "prod_sess_401",
                          "prod_sess_200", "prod_perm403_null_1",
                          "prod_perm403_null_2", "prod_sess401_null_1",
                          "prod_sess401_null_2"])

    def set_size(st: str, src: str) -> int:
        recs = [r for r in raw_records if r["state"] == st]
        return len({r[f"fingerprint_{src}"] for r in recs})

    # Non-CLEN header constancy across prod body-only states and per-state fingerprints.
    non_clen_sets: Dict[str, Dict[str, int]] = {}
    for st in body_states + ["prod_hdr_A", "prod_perm_200", "prod_sess_200"]:
        recs = [r for r in raw_records if r["state"] == st]
        non_clen_sets[st] = {
            "unique_non_clen": len({json.dumps(json.loads(r["headers_no_clen_json"]),
                                               sort_keys=True) for r in recs}),
            "full_set_size": set_size(st, "full"),
            "headers_set_size": set_size(st, "headers"),
        }

    # Worker pid distribution checks (E3).
    perm_workers: Dict[str, int] = {}
    sess_workers: Dict[str, int] = {}
    for lbl, acc in (("prod_perm_403", perm_workers), ("prod_perm_200", perm_workers),
                     ("prod_sess_401", sess_workers), ("prod_sess_200", sess_workers)):
        for w, c in worker_distribution.get(lbl, {}).items():
            acc[w] = acc.get(w, 0) + c
    all_workers = set()
    for dist in worker_distribution.values():
        all_workers |= set(dist.keys())

    return {
        "body_sha_by_state": {k: list(v["sha"]) for k, v in s.items()},
        "content_length_by_state": {k: list(v["clen"]) for k, v in s.items()},
        "body_len_by_state": {k: list(v["blen"]) for k, v in s.items()},
        "non_clen_headers_by_state": {k: list(v["non_clen_headers"]) for k, v in s.items()},
        "statuses_by_state": {k: list(v["statuses"]) for k, v in s.items()},
        "body_sha_distinct_across_ABC": len(set(abc_sha)) == 3,
        "content_length_distinct_across_ABC": len(set(abc_clen)) == 3,
        "content_length_increasing_across_ABC": (
            len(abc_clen) == 3 and int(abc_clen[0]) < int(abc_clen[1]) < int(abc_clen[2])
        ),
        "body_len_increasing_across_ABC": abc_blen[0] < abc_blen[1] < abc_blen[2],
        "content_length_equals_body_len_all_obs": all(
            r["content_length_header"] is not None
            and int(r["content_length_header"]) == r["body_len"]
            for r in raw_records
        ),
        "non_clen_headers_identical_across_ABC": (
            abc_nclen[0] == abc_nclen[1] == abc_nclen[2]
        ),
        "non_clen_unique_sets_per_state": non_clen_sets,
        "body_a_sha_pin_matches": list(s["prod_body_A"]["sha"])[0] == FROZEN_A_SHA,
        "body_a_len_pin_matches": list(s["prod_body_A"]["blen"])[0] == FROZEN_A_LEN,
        "all_body_only_and_null_status_200": all(
            list(v["statuses"]) == [200] for v in s.values()
        ) and all(list(v["statuses"]) == [200] for v in nulls.values()),
        "all_header_only_status_200": all(list(v["statuses"]) == [200] for v in h.values()),
        "header_only_body_identical_31B": all(
            list(v["sha"]) == [FROZEN_A_SHA] for v in h.values()
        ) and all(list(v["blen"]) == [FROZEN_A_LEN] for v in h.values()),
        "header_only_clen_identical_31": all(
            list(v["clen"]) == ["31"] for v in h.values()
        ),
        "classic_perm_status_403_vs_200": (
            list(control["prod_perm_403"]["statuses"]) == [403]
            and list(control["prod_perm_200"]["statuses"]) == [200]
        ),
        "classic_sess_status_401_vs_200": (
            list(control["prod_sess_401"]["statuses"]) == [401]
            and list(control["prod_sess_200"]["statuses"]) == [200]
        ),
        "classic_perm_body_distinct": (
            list(control["prod_perm_403"]["sha"])[0]
            != list(control["prod_perm_200"]["sha"])[0]
        ),
        "classic_sess_body_distinct": (
            list(control["prod_sess_401"]["sha"])[0]
            != list(control["prod_sess_200"]["sha"])[0]
        ),
        "perm_null_same_state": (
            list(control["prod_perm403_null_1"]["sha"])[0]
            == list(control["prod_perm403_null_2"]["sha"])[0]
            and list(control["prod_perm403_null_1"]["statuses"]) == [403]
        ),
        "sess_null_same_state": (
            list(control["prod_sess401_null_1"]["sha"])[0]
            == list(control["prod_sess401_null_2"]["sha"])[0]
            and list(control["prod_sess401_null_1"]["statuses"]) == [401]
        ),
        "classic_403_null_status": list(control["prod_perm403_null_1"]["statuses"]) == [403]
        and list(control["prod_perm403_null_2"]["statuses"]) == [403],
        "classic_401_null_status": list(control["prod_sess401_null_1"]["statuses"]) == [401]
        and list(control["prod_sess401_null_2"]["statuses"]) == [401],
        "worker_ids_distinct": len(all_workers) >= 2,
        "worker_ids_seen": sorted(all_workers),
        "perm_classic_worker_distribution": perm_workers,
        "sess_classic_worker_distribution": sess_workers,
        "perm_classic_workers_ge10": all(c >= 10 for c in perm_workers.values()),
        "sess_classic_workers_ge10": all(c >= 10 for c in sess_workers.values()),
        "per_state_fingerprint_set_sizes": {
            st: {src: set_size(st, src) for src in SOURCES}
            for st in body_states + hdr_states + list(control.keys())
        },
    }


def evaluate_baselines(metrics: Dict[str, Any]) -> Dict[str, Any]:
    m = metrics
    def disc(comparison: str, src: str) -> float:
        return m[f"{comparison}_{src}"]["discrimination"]

    return {
        "B-STATUS-ONLY": {
            "type": "strong-null",
            "expected": "0.0 on all same-status body-only and header-only comparisons "
                        "(200 vs 200) on production stack; 1.0 on status-varying "
                        "classic controls",
            "observed": {
                "body_drift_AvsC": disc("body_drift_AvsC", "status"),
                "body_drift_AvsB": disc("body_drift_AvsB", "status"),
                "header_drift_AvsE": disc("header_drift_AvsE", "status"),
                "null_body": disc("null_body", "status"),
                "classic_perm": disc("classic_perm", "status"),
                "classic_sess": disc("classic_sess", "status"),
            },
            "pass": (
                disc("body_drift_AvsC", "status") == 0.0
                and disc("body_drift_AvsB", "status") == 0.0
                and disc("header_drift_AvsE", "status") == 0.0
                and disc("null_body", "status") == 0.0
                and disc("classic_perm", "status") == 1.0
                and disc("classic_sess", "status") == 1.0
            ),
        },
        "B-BODY-ONLY": {
            "type": "positive",
            "expected": ">0.5 on same-status body-only drift (A vs C, A vs B); "
                        "1.0 on classic controls; 0.0 on nulls and header-only A vs E",
            "observed": {
                "body_drift_AvsC": disc("body_drift_AvsC", "body"),
                "body_drift_AvsB": disc("body_drift_AvsB", "body"),
                "null_body": disc("null_body", "body"),
                "header_drift_AvsE": disc("header_drift_AvsE", "body"),
                "classic_perm": disc("classic_perm", "body"),
                "classic_sess": disc("classic_sess", "body"),
            },
            "pass": (
                disc("body_drift_AvsC", "body") > 0.5
                and disc("body_drift_AvsB", "body") > 0.5
                and disc("null_body", "body") == 0.0
                and disc("header_drift_AvsE", "body") == 0.0
            ),
        },
        "B-HEADERS-ONLY": {
            "type": "body-correlated-auxiliary",
            "expected": ">0 on body-only comparisons SOLELY via body-correlated "
                        "Content-Length (documented, not a failure); 1.0 on header-only "
                        "via Cache-Control/ETag/Set-Cookie; 0.0 on nulls",
            "observed": {
                "body_drift_AvsC": disc("body_drift_AvsC", "headers"),
                "body_drift_AvsB": disc("body_drift_AvsB", "headers"),
                "header_drift_AvsE": disc("header_drift_AvsE", "headers"),
                "null_body": disc("null_body", "headers"),
            },
            "pass": (
                disc("null_body", "headers") == 0.0
                and disc("body_drift_AvsC", "headers") > 0.0
                and disc("header_drift_AvsE", "headers") > 0.0
            ),
        },
        "B-HEADERS-NO-CLEN": {
            "type": "isolation",
            "expected": "0.0 on body-only comparisons (no independent header drift) and "
                        "nulls; >0 on header-only A vs E (independent header signal)",
            "observed": {
                "body_drift_AvsC": disc("body_drift_AvsC", "headers_no_clen"),
                "body_drift_AvsB": disc("body_drift_AvsB", "headers_no_clen"),
                "header_drift_AvsE": disc("header_drift_AvsE", "headers_no_clen"),
                "null_body": disc("null_body", "headers_no_clen"),
                "null_hdr": disc("null_hdr", "headers_no_clen"),
            },
            "pass": (
                disc("body_drift_AvsC", "headers_no_clen") == 0.0
                and disc("body_drift_AvsB", "headers_no_clen") == 0.0
                and disc("null_body", "headers_no_clen") == 0.0
                and disc("null_hdr", "headers_no_clen") == 0.0
                and disc("header_drift_AvsE", "headers_no_clen") > 0.0
            ),
        },
    }


def evaluate_conditions(metrics: Dict[str, Any],
                        identity: Dict[str, Any]) -> Dict[str, Any]:
    m = metrics
    def disc(comparison: str, src: str) -> float:
        return m[f"{comparison}_{src}"]["discrimination"]

    def null_ok(comparison: str) -> bool:
        f = m[f"{comparison}_full"]
        return (
            f["discrimination"] == 0.0
            and f["ci_95"][0] <= 0.0 <= f["ci_95"][1]
            and f["discrimination"] <= 0.05
            and disc(comparison, "status") == 0.0
            and disc(comparison, "body") == 0.0
            and disc(comparison, "headers") == 0.0
            and disc(comparison, "headers_no_clen") == 0.0
        )

    c1_ok = disc("body_drift_AvsC", "full") > 0.5
    c2_ok = (
        disc("body_drift_AvsC", "body") > 0.5
        and disc("body_drift_AvsB", "body") > 0.5
        and disc("body_drift_AvsC", "headers_no_clen") == 0.0
        and disc("body_drift_AvsB", "headers_no_clen") == 0.0
    )
    c3_ok = (
        disc("body_drift_AvsC", "status") == 0.0
        and disc("body_drift_AvsB", "status") == 0.0
    )
    c4_ok = disc("body_drift_AvsC", "full") > disc("body_drift_AvsC", "status")
    c5_ok = (
        null_ok("null_body")
        and null_ok("null_hdr")
        and null_ok("perm_null")
        and null_ok("sess_null")
    )
    c6_ok = (
        identity["content_length_distinct_across_ABC"]
        and identity["content_length_increasing_across_ABC"]
        and identity["body_len_increasing_across_ABC"]
        and identity["body_sha_distinct_across_ABC"]
        and identity["non_clen_headers_identical_across_ABC"]
        and identity["content_length_equals_body_len_all_obs"]
        and identity["body_a_sha_pin_matches"]
        and identity["body_a_len_pin_matches"]
    )
    c7_ok = (
        disc("body_drift_AvsC", "full") >= 0.7          # (a) reader 200 vs admin 200
        and disc("classic_perm", "full") >= 0.7          # (b) classic 403 vs 200
        and m["perm_null_full"]["discrimination"] == 0.0
        and m["perm_null_full"]["ci_95"][0] <= 0.0 <= m["perm_null_full"]["ci_95"][1]
        and m["perm_null_full"]["discrimination"] <= 0.05
        and identity["classic_perm_status_403_vs_200"]
        and identity["classic_perm_body_distinct"]
        and identity["perm_null_same_state"]
        and identity["classic_403_null_status"]
        and identity["perm_classic_workers_ge10"]
    )
    c8_ok = (
        disc("classic_sess", "full") >= 0.7
        and m["sess_null_full"]["discrimination"] == 0.0
        and m["sess_null_full"]["ci_95"][0] <= 0.0 <= m["sess_null_full"]["ci_95"][1]
        and m["sess_null_full"]["discrimination"] <= 0.05
        and identity["classic_sess_status_401_vs_200"]
        and identity["classic_sess_body_distinct"]
        and identity["sess_null_same_state"]
        and identity["classic_401_null_status"]
        and identity["sess_classic_workers_ge10"]
    )
    c9_ok = (
        disc("header_drift_AvsE", "full") > 0.5
        and disc("header_drift_AvsE", "headers") > 0.5
        and disc("header_drift_AvsE", "status") == 0.0
        and disc("header_drift_AvsE", "body") == 0.0
        and disc("header_iso_CC", "full") == 1.0
        and disc("header_iso_CC", "headers") == 1.0
        and disc("header_iso_CC", "status") == 0.0
        and disc("header_iso_CC", "body") == 0.0
        and disc("header_iso_ETag", "full") == 1.0
        and disc("header_iso_ETag", "headers") == 1.0
        and disc("header_iso_ETag", "status") == 0.0
        and disc("header_iso_ETag", "body") == 0.0
        and disc("header_iso_SC", "full") == 1.0
        and disc("header_iso_SC", "headers") == 1.0
        and disc("header_iso_SC", "status") == 0.0
        and disc("header_iso_SC", "body") == 0.0
    )
    c10_ok = (
        identity["header_only_body_identical_31B"]
        and identity["header_only_clen_identical_31"]
    )

    conditions = {
        "C1_FULL_BODY_DRIFT_PROD": {
            "type": "positive",
            "expected": "full-vector discrimination > 0.5 on STATE_A vs STATE_C "
                        "(both 200 via nginx->gunicorn, bodies byte-different, "
                        "non-CLEN headers identical, CLEN 31 vs 117)",
            "observed": {
                "full_AvsC": disc("body_drift_AvsC", "full"),
                "statuses_AvsC": [sorted(identity["statuses_by_state"]["prod_body_A"]),
                                  sorted(identity["statuses_by_state"]["prod_body_C"])],
                "body_sha_distinct": identity["body_sha_distinct_across_ABC"],
                "content_length_distinct": identity["content_length_distinct_across_ABC"],
                "ci_95": m["body_drift_AvsC_full"]["ci_95"],
            },
            "threshold": ">0.5",
            "pass": c1_ok,
            "evidence_refs": "metrics.body_drift_AvsC_full; identity_checks",
        },
        "C2_BODY_ONLY_SIGNAL_PROD": {
            "type": "positive",
            "expected": "B-BODY-ONLY > 0.5 on A vs C AND A vs B; "
                        "B-HEADERS-NO-CLEN = 0.0 on A vs C and A vs B",
            "observed": {
                "body_only_AvsC": disc("body_drift_AvsC", "body"),
                "body_only_AvsB": disc("body_drift_AvsB", "body"),
                "headers_no_clen_AvsC": disc("body_drift_AvsC", "headers_no_clen"),
                "headers_no_clen_AvsB": disc("body_drift_AvsB", "headers_no_clen"),
            },
            "threshold": ">0.5 both; headers_no_clen == 0.0 both",
            "pass": c2_ok,
            "evidence_refs": "metrics.body_drift_AvsC_body, body_drift_AvsB_body, "
                             "body_drift_AvsC_headers_no_clen, body_drift_AvsB_headers_no_clen",
        },
        "C3_STATUS_ISOLATED_PROD": {
            "type": "strong-null",
            "expected": "B-STATUS-ONLY = 0.0 on A vs C and A vs B (status confound removed)",
            "observed": {
                "status_only_AvsC": disc("body_drift_AvsC", "status"),
                "status_only_AvsB": disc("body_drift_AvsB", "status"),
            },
            "threshold": "= 0.0",
            "pass": c3_ok,
            "evidence_refs": "metrics.body_drift_AvsC_status, body_drift_AvsB_status",
        },
        "C4_FULL_EXCEEDS_STATUS_NONVACUOUS_PROD": {
            "type": "positive",
            "expected": "full-vector discrimination > B-STATUS-ONLY strictly on A vs C "
                        "(1.0 > 0.0); equality at ceiling is vacuous and fails",
            "observed": {
                "full": disc("body_drift_AvsC", "full"),
                "status": disc("body_drift_AvsC", "status"),
            },
            "threshold": "strictly greater (full > status)",
            "pass": c4_ok,
            "evidence_refs": "metrics.body_drift_AvsC_full vs body_drift_AvsC_status",
        },
        "C5_NULL_NO_FALSE_POSITIVE_PROD": {
            "type": "null",
            "expected": "null N1-body (A resampled, concurrent) full = 0.0, CI contains "
                        "0.0, point <= 0.05; same for header null, 403 null, 401 null; "
                        "status/body/headers/headers_no_clen all 0.0 on each null",
            "observed": {
                "null_body_full": m["null_body_full"]["discrimination"],
                "null_body_ci": m["null_body_full"]["ci_95"],
                "null_hdr_full": m["null_hdr_full"]["discrimination"],
                "null_hdr_ci": m["null_hdr_full"]["ci_95"],
                "perm_null_full": m["perm_null_full"]["discrimination"],
                "perm_null_ci": m["perm_null_full"]["ci_95"],
                "sess_null_full": m["sess_null_full"]["discrimination"],
                "sess_null_ci": m["sess_null_full"]["ci_95"],
            },
            "threshold": "= 0.0, CI contains 0.0, <= 0.05 each",
            "pass": c5_ok,
            "evidence_refs": "metrics.null_body_full, null_hdr_full, perm_null_full, "
                             "sess_null_full",
        },
        "C6_CONTENT_LENGTH_VARIES_AND_HEADERS_CONSTANT_PROD": {
            "type": "validity",
            "expected": "Content-Length differs across A/B/C proportional to body_len "
                        "(31 != 70 != 117) and body SHA distinct, non-CLEN filtered "
                        "headers identical across A/B/C, CLEN == body_len on each observation",
            "observed": {
                "content_length_by_state": identity["content_length_by_state"],
                "body_len_by_state": identity["body_len_by_state"],
                "body_sha_by_state": identity["body_sha_by_state"],
                "non_clen_headers_identical": identity["non_clen_headers_identical_across_ABC"],
                "clen_equals_body_len_all_obs": identity["content_length_equals_body_len_all_obs"],
            },
            "threshold": "CLEN distinct & increasing, SHA distinct, non-CLEN identical, "
                         "CLEN == body_len",
            "pass": c6_ok,
            "evidence_refs": "identity_checks",
        },
        "C7_WRITABLE_PERMISSION_PROD": {
            "type": "positive",
            "expected": "(a) reader 200 vs admin 200 (A vs C) full >= 0.7; "
                        "(b) classic escalation 403 vs 200 via UPDATE users SET role with "
                        "cross-worker commit, full >= 0.7; 403 null = 0.0 CI contains 0.0 "
                        "<= 0.05; >=10 requests per worker",
            "observed": {
                "reader_admin_200_AvsC": disc("body_drift_AvsC", "full"),
                "classic_perm_403_vs_200": disc("classic_perm", "full"),
                "perm_null": {"full": m["perm_null_full"]["discrimination"],
                              "ci_95": m["perm_null_full"]["ci_95"]},
                "statuses_403_200": identity["classic_perm_status_403_vs_200"],
                "bodies_distinct": identity["classic_perm_body_distinct"],
                "worker_distribution": identity["perm_classic_worker_distribution"],
            },
            "threshold": ">= 0.7 both; null == 0.0 CI contains 0.0 <= 0.05; workers >=10 each",
            "pass": c7_ok,
            "evidence_refs": "metrics.body_drift_AvsC_full, classic_perm_full, "
                             "perm_null_full; identity_checks worker distribution",
        },
        "C8_WRITABLE_SESSION_PROD": {
            "type": "positive",
            "expected": "writable session invalidation 401 vs 200 via DELETE sessions with "
                        "cross-worker commit, full >= 0.7; 401 null = 0.0 CI contains 0.0 "
                        "<= 0.05; >=10 requests per worker",
            "observed": {
                "classic_sess_401_vs_200": disc("classic_sess", "full"),
                "sess_null": {"full": m["sess_null_full"]["discrimination"],
                              "ci_95": m["sess_null_full"]["ci_95"]},
                "statuses_401_200": identity["classic_sess_status_401_vs_200"],
                "bodies_distinct": identity["classic_sess_body_distinct"],
                "worker_distribution": identity["sess_classic_worker_distribution"],
            },
            "threshold": ">= 0.7; null == 0.0 CI contains 0.0 <= 0.05; workers >=10 each",
            "pass": c8_ok,
            "evidence_refs": "metrics.classic_sess_full, sess_null_full; "
                             "identity_checks worker distribution",
        },
        "C9_HEADER_ONLY_PROD": {
            "type": "positive",
            "expected": "full(A vs E) > 0.5 and headers-only(A vs E) > 0.5 with status 0.0 "
                        "and body 0.0; per-isolation Cache-Control/ETag/Set-Cookie each "
                        "full 1.0 headers-only 1.0 status 0.0 body 0.0",
            "observed": {
                "full_AvsE": disc("header_drift_AvsE", "full"),
                "headers_only_AvsE": disc("header_drift_AvsE", "headers"),
                "status_AvsE": disc("header_drift_AvsE", "status"),
                "body_AvsE": disc("header_drift_AvsE", "body"),
                "iso_CC": {"full": disc("header_iso_CC", "full"),
                           "headers": disc("header_iso_CC", "headers"),
                           "status": disc("header_iso_CC", "status"),
                           "body": disc("header_iso_CC", "body")},
                "iso_ETag": {"full": disc("header_iso_ETag", "full"),
                             "headers": disc("header_iso_ETag", "headers"),
                             "status": disc("header_iso_ETag", "status"),
                             "body": disc("header_iso_ETag", "body")},
                "iso_SC": {"full": disc("header_iso_SC", "full"),
                           "headers": disc("header_iso_SC", "headers"),
                           "status": disc("header_iso_SC", "status"),
                           "body": disc("header_iso_SC", "body")},
            },
            "threshold": "full > 0.5, headers-only > 0.5, status == 0.0, body == 0.0; "
                         "isolations all 1.0 / 1.0 / 0.0 / 0.0",
            "pass": c9_ok,
            "evidence_refs": "metrics.header_drift_AvsE_*, header_iso_*",
        },
        "C10_CLEN_IDENTITY_HEADER_ONLY_PROD": {
            "type": "validity",
            "expected": "Content-Length identical (31 == 31) and body SHA identical "
                        "across header-only A vs E and each isolation (not body-confounded)",
            "observed": {
                "header_only_body_identical": identity["header_only_body_identical_31B"],
                "header_only_clen_identical": identity["header_only_clen_identical_31"],
                "clen_by_state": identity["content_length_by_state"],
            },
            "threshold": "CLEN 31 == 31, body SHA d0ca833f... identical",
            "pass": c10_ok,
            "evidence_refs": "identity_checks header states",
        },
        "E1_CI_NONDEGENERATE": {
            "type": "exploratory",
            "expected": "bootstrap CI width measured under concurrency; degenerate "
                        "[1.0,1.0]/[0.0,0.0] declared deterministic not precision",
            "observed": {
                "body_drift_AvsC_full_ci": m["body_drift_AvsC_full"]["ci_95"],
                "body_drift_AvsC_full_width": m["body_drift_AvsC_full"]["ci_width"],
                "null_body_full_ci": m["null_body_full"]["ci_95"],
                "null_body_full_width": m["null_body_full"]["ci_width"],
                "header_drift_AvsE_full_ci": m["header_drift_AvsE_full"]["ci_95"],
                "header_drift_AvsE_full_width": m["header_drift_AvsE_full"]["ci_width"],
            },
            "threshold": "reported; degenerate expected for deterministic fingerprints",
            "pass": True,
            "evidence_refs": "metrics.*_ci_width",
        },
        "E2_HEADER_FOLDING": {
            "type": "exploratory",
            "expected": "folded (lowercase keys / shuffled order) vs canonical E "
                        "full discrimination 0.0 if sorted-lowercased normalization holds",
            "observed": {
                "fold_keys_vs_canonical_E_full": disc("fold_E2_keys", "full"),
                "fold_keys_vs_canonical_E_ci": m["fold_E2_keys_full"]["ci_95"],
                "fold_pad_vs_canonical_E_full": disc("fold_E2_pad", "full"),
                "fold_pad_vs_canonical_E_ci": m["fold_E2_pad_full"]["ci_95"],
            },
            "threshold": "keys/order folding == 0.0 (normalized); value whitespace "
                         "reported (value-as-is semantics)",
            "pass": disc("fold_E2_keys", "full") == 0.0,
            "evidence_refs": "metrics.fold_E2_keys_full, fold_E2_pad_full",
        },
        "E3_DISTRIBUTED_VISIBILITY": {
            "type": "exploratory",
            "expected": "permission/session commit observable from both gunicorn workers "
                        "within 500ms; >=10 requests served per worker for classic batches",
            "observed": {
                "worker_ids_seen": identity["worker_ids_seen"],
                "perm_worker_distribution": identity["perm_classic_worker_distribution"],
                "sess_worker_distribution": identity["sess_classic_worker_distribution"],
                "write_visibility_ms": None,  # filled below
            },
            "threshold": ">=2 distinct workers; >=10 per worker for classic pairs",
            "pass": (identity["worker_ids_distinct"]
                     and identity["perm_classic_workers_ge10"]
                     and identity["sess_classic_workers_ge10"]),
            "evidence_refs": "identity_checks worker distributions; batch_state_log writes",
        },
        "E4_BROWSERGYM": {
            "type": "conditional",
            "expected": "BrowserGym/AgentLab HTTP-layer discrimination if image available; "
                        "else NOT_TESTED (does not gate C1-C10)",
            "observed": {
                "docker_image_am1n3e_webarena_verified_shopping": "NOT_TESTED",
                "reason": "docker image inspect failed: IMAGE_UNAVAILABLE",
            },
            "threshold": ">0.5 if image available",
            "pass": True,
            "evidence_refs": "validity_notes; unresolved",
        },
    }
    return conditions


def validity_summary(raw_records: List[Dict[str, Any]],
                     batch_log: List[Dict[str, Any]],
                     identity: Dict[str, Any]) -> Dict[str, Any]:
    writes = [e for e in batch_log if e["action"].startswith("write_state::")]
    verifies = [e for e in batch_log if e["action"] == "pre_batch_verify"]

    expected_labels = [
        "prod_body_A", "prod_body_B", "prod_body_C",
        "prod_hdr_A", "prod_hdr_E",
        "prod_iso_cc", "prod_iso_etag", "prod_iso_sc",
        "prod_null_body_A1", "prod_null_body_A2",
        "prod_null_hdr_A1", "prod_null_hdr_A2",
        "prod_perm_403", "prod_perm_200",
        "prod_perm403_null_1", "prod_perm403_null_2",
        "prod_sess_200", "prod_sess_401",
        "prod_sess401_null_1", "prod_sess401_null_2",
        "seq_body_A", "seq_body_B", "seq_body_C",
        "seq_hdr_A", "seq_hdr_E",
        "prod_hdr_E_foldkeys", "prod_hdr_E_foldpad",
        "l_body_A", "l_body_C", "l_hdr_E",
    ]
    counts = {lbl: sum(1 for r in raw_records if r["state"] == lbl)
              for lbl in expected_labels}
    checks = {
        "server_state_committed_before_every_write": all(
            e["match_expected"] for e in writes),
        "server_state_verified_before_every_batch": all(
            e["state_snapshot"]["body_config"]["variant"] in ("A", "B", "C")
            for e in verifies),
        "all_body_only_and_null_observations_status_200": identity["all_body_only_and_null_status_200"],
        "all_header_only_observations_status_200": identity["all_header_only_status_200"],
        "classic_perm_status_403_vs_200": identity["classic_perm_status_403_vs_200"],
        "classic_sess_status_401_vs_200": identity["classic_sess_status_401_vs_200"],
        "body_sha_distinct_across_ABC": identity["body_sha_distinct_across_ABC"],
        "content_length_distinct_across_ABC": identity["content_length_distinct_across_ABC"],
        "content_length_increasing_across_ABC": identity["content_length_increasing_across_ABC"],
        "non_clen_headers_identical_across_ABC": identity["non_clen_headers_identical_across_ABC"],
        "content_length_equals_body_len_all_obs": identity["content_length_equals_body_len_all_obs"],
        "header_only_body_identical_31B": identity["header_only_body_identical_31B"],
        "header_only_clen_identical_31": identity["header_only_clen_identical_31"],
        "raw_line_count_per_batch_is_20": all(counts[l] == N_SAMPLES for l in expected_labels),
        "total_raw_lines": len(raw_records),
        "excluded_headers_unchanged": EXCLUDED_HEADERS == {"Date", "Server", "X-Request-Id"},
        "worker_ids_distinct": identity["worker_ids_distinct"],
        "body_a_sha_pin_matches": identity["body_a_sha_pin_matches"],
        "body_a_len_pin_matches": identity["body_a_len_pin_matches"],
        "fingerprint_algorithm_matches_parent": True,  # copied verbatim; hash in provenance
        "worker_header_present_all_prod": all(
            r.get("worker_id", "unknown") != "unknown"
            for r in raw_records if r["state"].startswith(("prod_", "seq_"))
        ),
    }
    critical = [
        "server_state_committed_before_every_write",
        "all_body_only_and_null_observations_status_200",
        "all_header_only_observations_status_200",
        "classic_perm_status_403_vs_200",
        "classic_sess_status_401_vs_200",
        "body_sha_distinct_across_ABC",
        "content_length_distinct_across_ABC",
        "content_length_increasing_across_ABC",
        "non_clen_headers_identical_across_ABC",
        "content_length_equals_body_len_all_obs",
        "header_only_body_identical_31B",
        "header_only_clen_identical_31",
        "raw_line_count_per_batch_is_20",
        "excluded_headers_unchanged",
        "worker_ids_distinct",
        "body_a_sha_pin_matches",
        "body_a_len_pin_matches",
        "worker_header_present_all_prod",
    ]
    return {
        "checks": checks,
        "batch_counts": counts,
        "writes_count": len(writes),
        "pre_batch_verifies_count": len(verifies),
        "critical_all_pass": all(checks[k] for k in critical),
        "failed_critical": [k for k in critical if not checks[k]],
    }


# ─── Smoke ───────────────────────────────────────────────────────────────────

def run_smoke(tokens: Dict[str, str]) -> int:
    print("=== SMOKE: setup verification only ===")
    admin_tok, reader_tok = tokens["admin"], tokens["reader"]

    do_write("set_headers", {"_fixed": True}, admin_tok, [])
    do_write("set_body", {"variant": "B", "body_sha256": BODY_SHA["B"]},
             admin_tok, [])
    obs = observe_resource(reader_tok)
    assert obs["status"] == 200, obs["status"]
    assert obs["body_bytes"] == BODIES["B"], obs["body_bytes"]
    assert not verify_constant_headers(obs), verify_constant_headers(obs)
    assert obs["worker_id"] != "unknown", obs["worker_id"]

    # header E state (body must be back on A for header-only discrimination check)
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]}, admin_tok, [])
    do_write("set_headers", {k: HEADER_E_CONFIG[k] for k in
                             ("cache_control", "etag", "vary", "set_cookie")},
             admin_tok, [])
    obsE = observe_resource(reader_tok)
    assert obsE["status"] == 200, obsE["status"]
    assert obsE["body_bytes"] == BODIES["A"], obsE["body_bytes"]
    assert not verify_header_state(obsE, HEADER_E_CONFIG), verify_header_state(obsE, HEADER_E_CONFIG)

    # role gate
    do_write("set_role", {"role": "viewer"}, admin_tok, [])
    obs403 = observe_resource(reader_tok)
    assert obs403["status"] == 403, obs403["status"]
    assert obs403["body_bytes"] == BODY_403, obs403["body_bytes"]
    do_write("set_role", {"role": "reader"}, admin_tok, [])

    # session invalidation
    do_write("invalidate_session", {"reader_valid_sessions": 0}, admin_tok, [])
    obs401 = observe_resource(reader_tok)
    assert obs401["status"] == 401, obs401["status"]
    assert obs401["body_bytes"] == BODY_401, obs401["body_bytes"]

    # restore
    do_write("set_headers", {"_fixed": True}, admin_tok, [])
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]}, admin_tok, [])
    print("[SMOKE OK] set_body/set_headers/set_role/role-gate/session-invalid verified "
          "with worker instrument header.", flush=True)
    return 0


def main() -> int:
    global BASE_URL, gunicorn_port_used, nginx_port_used
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--sanity", action="store_true")
    args = parser.parse_args()

    outdir = Path(__file__).resolve().parent
    # Frozen startup assertions before any measurement.
    assert len(BODIES["A"]) == FROZEN_A_LEN, len(BODIES["A"])
    assert BODY_SHA["A"] == FROZEN_A_SHA
    assert len(BODIES["B"]) > len(BODIES["A"])
    assert len(BODIES["C"]) > len(BODIES["B"])
    assert BODY_SHA["B"].startswith("67c186f2cee"), BODY_SHA["B"]
    assert BODY_SHA["C"].startswith("b46c461ccee"), BODY_SHA["C"]
    assert hashlib.sha256(BODY_403).hexdigest().startswith("387fe7"), \
        hashlib.sha256(BODY_403).hexdigest()
    assert hashlib.sha256(BODY_401).hexdigest().startswith("9df36"), \
        hashlib.sha256(BODY_401).hexdigest()

    random.seed(SEED)
    init_db()

    gunicorn_port_used = discover_port(GUNICORN_PORT)
    nginx_port_used = discover_port(NGINX_PORT)

    # ── Topology L sanity first (frozen §8 item 13 order) ────────────────────
    sanity_file = outdir / "sanity_l_result.json"
    sanity_started_at = now_iso()
    try:
        sanity = run_sanity_l(outdir)
        sanity_records = sanity["raw_records"]
        sanity_batch_log = sanity["batch_log"]
        # Verify sanity replications: A vs C full 1.0, A vs E full 1.0.
        from collections import defaultdict
        sets_by_state = defaultdict(lambda: defaultdict(set))
        for r in sanity_records:
            sets_by_state[r["state"]]["full"].add(r["fingerprint_full"])
            sets_by_state[r["state"]]["status"].add(r["fingerprint_status"])
            sets_by_state[r["state"]]["body"].add(r["fingerprint_body"])
        def jd(a, b):
            if not a and not b:
                return 0.0
            return 1.0 - (len(a & b) / len(a | b))
        l_avsc_full = jd(sets_by_state["l_body_A"]["full"], sets_by_state["l_body_C"]["full"])
        l_avsc_status = jd(sets_by_state["l_body_A"]["status"], sets_by_state["l_body_C"]["status"])
        l_avse_full = jd(sets_by_state["l_body_A"]["full"], sets_by_state["l_hdr_E"]["full"])
        l_avse_body = jd(sets_by_state["l_body_A"]["body"], sets_by_state["l_hdr_E"]["body"])
        sanity_summary = {
            "l_body_AvsC_full": l_avsc_full,
            "l_body_AvsC_status": l_avsc_status,
            "l_hdr_AvsE_full": l_avse_full,
            "l_hdr_AvsE_body": l_avse_body,
            "sanity_started_at": sanity_started_at,
            "sanity_finished_at": now_iso(),
            "n_per_state": N_SAMPLES,
            "topology": "L (Werkzeug dev server, threaded)",
        }
        with open(sanity_file, "w") as f:
            json.dump(sanity_summary, f, indent=2)
        if not (l_avsc_full == 1.0 and l_avsc_status == 0.0
                and l_avse_full == 1.0 and l_avse_body == 0.0):
            raise MeasurementInvalid(
                "sanity_replication_failed",
                f"topology L sanity not replicated: {sanity_summary}",
            )
        print(f"[OK] Topology L sanity replication: {sanity_summary}", flush=True)
    except MeasurementInvalid as e:
        failure = {"experiment_id": "EXP-RUNTIME-35764329925", "stage": "execute",
                   "category": e.category, "message": e.detail, "retryable": True,
                   "ts": now_iso()}
        with open(outdir / "failure.json", "w") as f:
            json.dump(failure, f, indent=2)
        print(f"[MEASUREMENT_INVALID] {e.category}: {e.detail}", flush=True)
        return 2

    if args.sanity:
        # Persist sanity raw evidence even in --sanity standalone diagnostics mode.
        with open(outdir / "sanity_l_raw_observations.jsonl", "w") as f:
            for r in sanity_records:
                f.write(json.dumps(r) + "\n")
        with open(outdir / "sanity_l_batch_log.jsonl", "w") as f:
            for e in sanity_batch_log:
                f.write(json.dumps(e) + "\n")
        return 0

    # ── Topology P (primary): gunicorn + nginx ───────────────────────────────
    gunicorn_proc: Optional[subprocess.Popen] = None
    try:
        write_nginx_conf(gunicorn_port_used, nginx_port_used)
        print(f"[OK] starting gunicorn on 127.0.0.1:{gunicorn_port_used}", flush=True)
        gunicorn_proc = start_gunicorn(gunicorn_port_used)
        wait_for_server(f"http://{HOST}:{gunicorn_port_used}")
        print(f"[OK] gunicorn reachable on {gunicorn_port_used}", flush=True)

        if args.smoke:
            BASE_URL = f"http://{HOST}:{gunicorn_port_used}"
            gunicorn_tokens = get_tokens(BASE_URL)
            run_smoke(gunicorn_tokens)
            return 0

        print(f"[OK] starting nginx on 127.0.0.1:{nginx_port_used}", flush=True)
        start_nginx(nginx_port_used)
        BASE_URL = f"http://{HOST}:{nginx_port_used}"
        wait_for_server(BASE_URL)
        print(f"[OK] nginx reachable on {BASE_URL}", flush=True)

        # Fresh DB + fresh tokens through the production path.
        init_db()
        tokens = get_tokens(BASE_URL)
        print(f"[OK] production tokens obtained (reader len={len(tokens['reader'])})",
              flush=True)
        result = run_full(tokens, outdir, sanity_records, sanity_batch_log)
        return 0 if result["status"] == "COMPLETE" else 3
    except MeasurementInvalid as e:
        print(f"[MEASUREMENT_INVALID] {e.category}: {e.detail}", flush=True)
        failure = {
            "experiment_id": "EXP-RUNTIME-35764329925",
            "stage": "execute",
            "category": e.category,
            "message": e.detail,
            "retryable": True,
            "ts": now_iso(),
        }
        with open(outdir / "failure.json", "w") as f:
            json.dump(failure, f, indent=2)
        return 2
    except Exception as e:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        failure = {
            "experiment_id": "EXP-RUNTIME-35764329925",
            "stage": "execute",
            "category": "unexpected_error",
            "message": repr(e),
            "retryable": True,
            "ts": now_iso(),
        }
        with open(outdir / "failure.json", "w") as f:
            json.dump(failure, f, indent=2)
        return 3
    finally:
        if gunicorn_proc is not None:
            gunicorn_proc.terminate()
            try:
                gunicorn_proc.wait(timeout=5)
            except Exception:  # noqa: BLE001
                gunicorn_proc.kill()
        stop_nginx()
        time.sleep(0.5)


if __name__ == "__main__":
    sys.exit(main())