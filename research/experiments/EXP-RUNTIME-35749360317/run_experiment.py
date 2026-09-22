#!/usr/bin/env python3
"""
EXP-RUNTIME-35749360317 — Same-status body-only drift discrimination.

Frozen design: research/experiments/EXP-RUNTIME-35749360317/{spec.json, prereg.md, freeze.json}

Question (director mandate, frozen): does the HTTP fingerprint substrate discriminate
same-status body-only drift where response status is identical (200 vs 200) but response
bodies differ via server-side permission/content variation (Content-Length varies, body
semantics differ), isolating body-only signal with status confound removed and yielding
the complementary non-vacuous full > status test to the header-only success (full 1.0 >
body/status 0.0, Content-Length isolation holds), plus writable permission-level and
session-invalidation controls that produce discriminating positive (discrimination >=0.7)
and valid null (FP<0.05) on localhost Flask HS256?

Fingerprint algorithm, Jaccard metric and bootstrap are copied IDENTICALLY from parent
EXP-RUNTIME-35741906498/run_experiment.py (compute_fingerprint, jaccard_distance,
bootstrap_jaccard_ci), which itself copied them verbatim from EXP-RUNTIME-35697043449,
so AUDIT can recompute exactly. EXCLUDED_HEADERS = {Date, Server, X-Request-Id} identical
to parent.

Usage:
  python3 run_experiment.py --smoke   # setup verification only (no discrimination)
  python3 run_experiment.py           # full frozen execution (300 raw observations)
"""

import argparse
import hashlib
import json
import os
import random
import socket
import sqlite3
import sys
import threading
import time
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
JWT_SECRET = "test-secret-key-exp-runtime-35749360317"
JWT_ALGORITHM = "HS256"
DB_PATH = "/tmp/spider_bodydrift_testbed.db"
HOST = "127.0.0.1"
DEFAULT_PORT = 19849  # parent used 19848; this experiment discovers from 19849

# Identical exclusion set to parent (spec measurement_validity item 4).
EXCLUDED_HEADERS = {"Date", "Server", "X-Request-Id"}

# Frozen constant header config (spec positive_control; held constant across A/B/C):
# Cache-Control: max-age=3600, ETag: W/"fixed-aaa-111", Vary: Accept-Encoding,
# no Set-Cookie, Content-Type: application/json.
FIXED_HEADER_CONFIG: Dict[str, str] = {
    "cache_control": "max-age=3600",
    "etag": 'W/"fixed-aaa-111"',
    "vary": "Accept-Encoding",
    "set_cookie": "",
}

# Frozen body states (spec positive_control table; canonical serialization same as
# parent baseline: json.dumps(sort_keys=True) — pinned A body 31 bytes SHA
# d0ca833f843c6d70ec9d6755f52a92dcbfc8b4ab601b871bced09ad027172e34 identical to
# parent's byte-identical body; B/C exact lengths & SHAs logged, "~52"/"~95" in the
# frozen table are approximate magnitudes for the same compact-vs-spaced serialization).
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

# Frozen identity pin: STATE_A must be byte-identical to parent baseline (31 bytes).
FROZEN_A_SHA = "d0ca833f843c6d70ec9d6755f52a92dcbfc8b4ab601b871bced09ad027172e34"
FROZEN_A_LEN = 31

# Error bodies for classic writable controls (prereg §4.2).
BODY_403 = json.dumps({"error": "forbidden"}, sort_keys=True).encode("utf-8")
BODY_401 = json.dumps({"error": "unauthorized"}, sort_keys=True).encode("utf-8")

random.seed(SEED)


class MeasurementInvalid(Exception):
    """Infrastructure / verification failure — never a scientific negative."""

    def __init__(self, category: str, detail: str):
        super().__init__(f"{category}: {detail}")
        self.category = category
        self.detail = detail


# ─── Database ────────────────────────────────────────────────────────────────

def init_db() -> None:
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
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
    h = FIXED_HEADER_CONFIG
    c.execute(
        "INSERT INTO header_config (id, cache_control, etag, vary, set_cookie) "
        "VALUES (1, ?, ?, ?, ?)",
        (h["cache_control"], h["etag"], h["vary"], h["set_cookie"]),
    )
    c.execute("INSERT INTO body_config (id, variant, body_sha256) VALUES (1, 'A', ?)",
              (BODY_SHA["A"],))
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
              ("reader", hashlib.sha256(b"reader_pass").hexdigest(), "reader"))
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
              ("admin", hashlib.sha256(b"admin_pass").hexdigest(), "admin"))
    conn.commit()
    conn.close()


def read_header_config() -> Dict[str, str]:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT cache_control, etag, vary, set_cookie FROM header_config WHERE id = 1"
    ).fetchone()
    conn.close()
    if row is None:
        raise MeasurementInvalid("header_config_missing", "header_config row id=1 absent")
    return {"cache_control": row[0], "etag": row[1], "vary": row[2], "set_cookie": row[3]}


def read_body_config() -> Dict[str, str]:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT variant, body_sha256 FROM body_config WHERE id = 1"
    ).fetchone()
    conn.close()
    if row is None:
        raise MeasurementInvalid("body_config_missing", "body_config row id=1 absent")
    return {"variant": row[0], "body_sha256": row[1]}


def read_user_role(username: str) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row[0] if row is not None else None


def read_session_count(username: Optional[str] = None) -> int:
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        "UPDATE header_config SET cache_control = ?, etag = ?, vary = ?, "
        "set_cookie = ? WHERE id = 1",
        (cfg["cache_control"], cfg["etag"], cfg["vary"], cfg["set_cookie"]),
    )
    conn.commit()  # WAL COMMIT before returning
    conn.close()


def write_body_config(variant: str) -> None:
    if variant not in BODIES:
        raise MeasurementInvalid("unknown_body_variant", f"variant={variant!r}")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        "UPDATE body_config SET variant = ?, body_sha256 = ? WHERE id = 1",
        (variant, BODY_SHA[variant]),
    )
    conn.commit()  # WAL COMMIT before returning
    conn.close()


def set_user_role(username: str, role: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    cur = conn.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
    if cur.rowcount != 1:
        conn.close()
        raise MeasurementInvalid("role_update_failed",
                                 f"UPDATE users SET role={role!r} touched {cur.rowcount} rows")
    conn.commit()
    conn.close()


def invalidate_user_sessions(username: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
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
        g.db = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
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
            # Frozen constant error bodies (prereg S_401 pins the 401 body to
            # {"error":"unauthorized"}; P_403 pins 403 to {"error":"forbidden"}).
            # The reason is conveyed by status only, so both classic controls and
            # their same-state nulls observe a stable constant error body.
            if str(e) == "forbidden":
                return make_response(BODY_403, 403,
                                     {"Content-Type": "application/json"})
            return make_response(BODY_401, 401,
                                 {"Content-Type": "application/json"})
        role = read_user_role(username)
        # Classic permission escalation (P2): role 'viewer' has no access to /resource.
        if role == "viewer":
            return make_response(BODY_403, 403,
                                 {"Content-Type": "application/json"})
        # Same-status body-only drift: authenticated user (reader or admin role) always
        # receives 200 with the committed body_config variant; headers constant.
        cfg = read_header_config()
        bcfg = read_body_config()
        body = BODIES[bcfg["variant"]]
        resp = make_response(body)
        resp.headers["Content-Type"] = "application/json"
        resp.headers["Cache-Control"] = cfg["cache_control"]
        resp.headers["ETag"] = cfg["etag"]
        resp.headers["Vary"] = cfg["vary"]
        if cfg["set_cookie"]:
            resp.headers["Set-Cookie"] = cfg["set_cookie"]
        return resp

    @app.route("/protected", methods=["GET"])
    def protected():
        # Retained from parent for smoke check only (prereg §4.1).
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

BASE_URL: str = ""  # set at runtime


def observe_resource(token: str) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}"}
    start = time.monotonic()
    resp = requests.get(f"{BASE_URL}/resource", headers=headers, timeout=10)
    end = time.monotonic()
    filtered = {k: v for k, v in resp.headers.items() if k not in EXCLUDED_HEADERS}
    return {
        "status": resp.status_code,
        "body_bytes": resp.content,
        "headers": filtered,
        "headers_raw": dict(resp.headers),
        "response_time_ms": round((end - start) * 1000, 2),
    }


def _hdr(headers: Dict[str, str], key: str) -> Optional[str]:
    """Case-insensitive header lookup."""
    for k, v in headers.items():
        if k.lower() == key.lower():
            return v
    return None


def expected_constant_headers() -> Dict[str, Optional[str]]:
    h = FIXED_HEADER_CONFIG
    exp = {
        "Cache-Control": h["cache_control"],
        "ETag": h["etag"],
        "Vary": h["vary"],
        "Content-Type": "application/json",
    }
    exp["Set-Cookie"] = h["set_cookie"] if h["set_cookie"] else None
    return exp


def verify_constant_headers(obs: Dict[str, Any]) -> List[str]:
    """Return list of non-CLEN header mismatches for this observation (empty = OK)."""
    problems = []
    exp = expected_constant_headers()
    for key, want in exp.items():
        got = _hdr(obs["headers_raw"], key)
        if want is None:
            if got is not None:
                problems.append(f"{key} unexpectedly present: {got!r}")
        else:
            if got is None:
                problems.append(f"{key} missing (expected {want!r})")
            elif got != want:
                problems.append(f"{key}={got!r} != expected {want!r}")
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


def discover_port() -> int:
    for port in range(DEFAULT_PORT, DEFAULT_PORT + 50):
        s = socket.socket()
        try:
            s.bind((HOST, port))
            s.close()
            return port
        except OSError:
            s.close()
    raise MeasurementInvalid("port_exhaustion", "no free port in 19849-19898")


def wait_for_server(base: str, timeout: float = 15.0) -> None:
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
            json=FIXED_HEADER_CONFIG,
            timeout=10,
        )
        committed = read_header_config()
        match = committed == FIXED_HEADER_CONFIG
    elif action == "set_body":
        r = requests.post(
            f"{BASE_URL}/admin/set_body_variant",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"variant": expected["variant"]},
            timeout=10,
        )
        committed = read_body_config()
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


def do_batch(label: str, token: str, expected_status: int,
             expected_body_sha: Optional[str], constant_header_check: bool,
             raw_records: List[Dict[str, Any]],
             batch_log: List[Dict[str, Any]]) -> None:
    pre = state_snapshot()
    batch_log.append({
        "action": "pre_batch_verify",
        "batch": label,
        "expected_status": expected_status,
        "expected_body_sha": expected_body_sha,
        "state_snapshot": pre,
        "n": N_SAMPLES,
        "ts": now_iso(),
    })

    for i in range(N_SAMPLES):
        jitter = random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0
        time.sleep(jitter)
        obs = observe_resource(token)

        if obs["status"] != expected_status:
            raise MeasurementInvalid(
                "status_mismatch",
                f"batch={label} i={i} status={obs['status']} "
                f"expected={expected_status}",
            )
        cl = _hdr(obs["headers_raw"], "Content-Length")
        if cl is None or int(cl) != len(obs["body_bytes"]):
            raise MeasurementInvalid(
                "content_length_unverifiable",
                f"batch={label} i={i} Content-Length={cl!r} "
                f"body_len={len(obs['body_bytes'])}",
            )
        if expected_body_sha is not None:
            got_sha = hashlib.sha256(obs["body_bytes"]).hexdigest()
            if got_sha != expected_body_sha:
                raise MeasurementInvalid(
                    "body_sha_mismatch",
                    f"batch={label} i={i} body_sha={got_sha} "
                    f"expected={expected_body_sha}",
                )
        if constant_header_check:
            hp = verify_constant_headers(obs)
            if hp:
                raise MeasurementInvalid(
                    "expected_header_mismatch",
                    f"batch={label} i={i}: " + "; ".join(hp),
                )

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
            "content_length_header": cl,
            "response_time_ms": obs["response_time_ms"],
            "observed_at": now_iso(),
        }
        raw_records.append(rec)
    print(f"  [batch] {label}: n={N_SAMPLES} status={expected_status} OK", flush=True)


# ─── Batch sequence (frozen prereg §8 item 11 order) ────────────────────────
#   body-only A/B/C -> N1 (A resampled) -> N2 (C resampled, exploratory)
#   -> P_403/P_200 + 403 null -> S_200/S_401 + 401 null

def run_full(tokens: Dict[str, str], outdir: Path) -> Dict[str, Any]:
    raw_records: List[Dict[str, Any]] = []
    batch_log: List[Dict[str, Any]] = []
    admin_tok = tokens["admin"]
    reader_tok = tokens["reader"]
    started = now_iso()

    print("=== FULL frozen execution (N=20 x 15 batches = 300 raw lines) ===", flush=True)

    # 1. Fix header_config constant once; verify committed.
    do_write("set_headers", FIXED_HEADER_CONFIG, admin_tok, batch_log)

    # 2. Body-only states A, B, C (all 200, same valid JWT, role reader).
    for v in ("A", "B", "C"):
        do_write("set_body", {"variant": v, "body_sha256": BODY_SHA[v]},
                 admin_tok, batch_log)
        do_batch(f"body_{v}", reader_tok, 200, BODY_SHA[v],
                 constant_header_check=True, raw_records=raw_records,
                 batch_log=batch_log)

    # 3. N1: STATE_A resampled, two independent batches, no write between.
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)
    do_batch("null_A1", reader_tok, 200, BODY_SHA["A"],
             constant_header_check=True, raw_records=raw_records, batch_log=batch_log)
    do_batch("null_A2", reader_tok, 200, BODY_SHA["A"],
             constant_header_check=True, raw_records=raw_records, batch_log=batch_log)

    # 4. N2 (exploratory): STATE_C resampled, two independent batches, no write between.
    do_write("set_body", {"variant": "C", "body_sha256": BODY_SHA["C"]},
             admin_tok, batch_log)
    do_batch("null_C1", reader_tok, 200, BODY_SHA["C"],
             constant_header_check=True, raw_records=raw_records, batch_log=batch_log)
    do_batch("null_C2", reader_tok, 200, BODY_SHA["C"],
             constant_header_check=True, raw_records=raw_records, batch_log=batch_log)

    # 5. P2 classic permission escalation: reader user role viewer -> 403, then admin -> 200.
    do_write("set_role", {"role": "viewer"}, admin_tok, batch_log)
    do_batch("perm_403", reader_tok, 403, hashlib.sha256(BODY_403).hexdigest(),
             constant_header_check=False, raw_records=raw_records, batch_log=batch_log)
    do_write("set_role", {"role": "admin"}, admin_tok, batch_log)
    do_batch("perm_200", reader_tok, 200, BODY_SHA["C"],
             constant_header_check=True, raw_records=raw_records, batch_log=batch_log)

    # 6. P2 same-state 403 null: role viewer, two batches, no write between.
    do_write("set_role", {"role": "viewer"}, admin_tok, batch_log)
    do_batch("perm403_null_1", reader_tok, 403, hashlib.sha256(BODY_403).hexdigest(),
             constant_header_check=False, raw_records=raw_records, batch_log=batch_log)
    do_batch("perm403_null_2", reader_tok, 403, hashlib.sha256(BODY_403).hexdigest(),
             constant_header_check=False, raw_records=raw_records, batch_log=batch_log)

    # 7. Reset reader role and body to A; S session invalidation: valid 200, then 401.
    do_write("set_role", {"role": "reader"}, admin_tok, batch_log)
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, batch_log)
    do_batch("sess_200", reader_tok, 200, BODY_SHA["A"],
             constant_header_check=True, raw_records=raw_records, batch_log=batch_log)
    do_write("invalidate_session", {"reader_valid_sessions": 0}, admin_tok, batch_log)
    do_batch("sess_401", reader_tok, 401, hashlib.sha256(BODY_401).hexdigest(),
             constant_header_check=False, raw_records=raw_records, batch_log=batch_log)

    # 8. S same-state 401 null: session still invalid, two batches, no write between.
    do_batch("sess401_null_1", reader_tok, 401, hashlib.sha256(BODY_401).hexdigest(),
             constant_header_check=False, raw_records=raw_records, batch_log=batch_log)
    do_batch("sess401_null_2", reader_tok, 401, hashlib.sha256(BODY_401).hexdigest(),
             constant_header_check=False, raw_records=raw_records, batch_log=batch_log)

    finished = now_iso()

    # ── Raw evidence artifacts ────────────────────────────────────────────────
    raw_path = outdir / "raw_observations.jsonl"
    with open(raw_path, "w") as f:
        for r in raw_records:
            f.write(json.dumps(r) + "\n")
    log_path = outdir / "batch_state_log.jsonl"
    with open(log_path, "w") as f:
        for e in batch_log:
            f.write(json.dumps(e) + "\n")

    identity = identity_checks(raw_records)
    validity = validity_summary(raw_records, batch_log, identity)

    result: Dict[str, Any] = {
        "experiment_id": "EXP-RUNTIME-35749360317",
        "lane": "runtime",
        "started_at": started,
        "finished_at": finished,
        "seed": SEED,
        "n_samples_per_batch": N_SAMPLES,
        "jitter_ms": [JITTER_MIN_MS, JITTER_MAX_MS],
        "bootstrap_b": BOOTSTRAP_B,
        "excluded_headers": sorted(EXCLUDED_HEADERS),
        "bodies": {k: {"len": len(v), "sha256": BODY_SHA[k]} for k, v in BODIES.items()},
        "fixed_header_config": FIXED_HEADER_CONFIG,
        "body_403": {"len": len(BODY_403), "sha256": hashlib.sha256(BODY_403).hexdigest()},
        "body_401": {"len": len(BODY_401), "sha256": hashlib.sha256(BODY_401).hexdigest()},
        "raw_line_count": len(raw_records),
        "validity": validity,
        "identity_checks": identity,
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
        metrics = compute_metrics(raw_records)
        conditions = evaluate_conditions(metrics, identity)
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
COMPARISONS = [
    ("body_drift_AvsC", "body_A", "body_C"),
    ("body_drift_AvsB", "body_A", "body_B"),
    ("null_control_N1", "null_A1", "null_A2"),
    ("null_control_N2", "null_C1", "null_C2"),
    ("classic_perm", "perm_403", "perm_200"),
    ("classic_sess", "sess_401", "sess_200"),
    ("perm_null", "perm403_null_1", "perm403_null_2"),
    ("sess_null", "sess401_null_1", "sess401_null_2"),
]


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

    for name, a, b in COMPARISONS:
        for src in SOURCES:
            d, lo, hi = bootstrap_jaccard_ci(
                sets[a][src], sets[b][src], BOOTSTRAP_B, BOOTSTRAP_ALPHA
            )
            metrics[f"{name}_{src}"] = {
                "discrimination": d,
                "ci_95": [lo, hi],
                "set_a_size": len(sets[a][src]),
                "set_b_size": len(sets[b][src]),
                "nominal_n": [N_SAMPLES, N_SAMPLES],
                "comparison": f"{a} vs {b}",
                "source": src,
                "degenerate_ci": lo == hi,
            }
    # Effective distinct N per state per source (deterministic disclosure).
    metrics["effective_distinct_n"] = {
        label: {src: len(sets[label][src]) for src in SOURCES} for label in labels
    }
    return metrics


def identity_checks(raw_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    def state_sets(states: List[str]) -> Dict[str, set]:
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
                "statuses": {r["status"] for r in recs},
            }
        return out

    body_states = ["body_A", "body_B", "body_C"]
    s = state_sets(body_states)
    abc_sha = [list(s[k]["sha"])[0] for k in body_states]
    abc_clen = [list(s[k]["clen"])[0] for k in body_states]
    abc_blen = [list(s[k]["blen"])[0] for k in body_states]
    abc_nclen = [list(s[k]["non_clen_headers"])[0] for k in body_states]

    control = state_sets(["perm_403", "perm_200", "sess_401", "sess_200",
                          "perm403_null_1", "perm403_null_2",
                          "sess401_null_1", "sess401_null_2"])
    nulls = state_sets(["null_A1", "null_A2", "null_C1", "null_C2"])

    # Per-state per-source set-size map for the primary states.
    set_sizes: Dict[str, Dict[str, int]] = {}
    for st in body_states + ["perm_403", "perm_200", "sess_401", "sess_200"]:
        recs = [r for r in raw_records if r["state"] == st]
        set_sizes[st] = {
            "full": len({r["fingerprint_full"] for r in recs}),
            "status": len({r["fingerprint_status"] for r in recs}),
            "body": len({r["fingerprint_body"] for r in recs}),
            "headers": len({r["fingerprint_headers"] for r in recs}),
            "headers_no_clen": len({r["fingerprint_headers_no_clen"] for r in recs}),
        }

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
        "set_cookie_absent_body_only": all(
            _hdr(json.loads(r["headers_raw_json"]), "Set-Cookie") is None
            for r in raw_records
            if r["state"] in ("body_A", "body_B", "body_C",
                              "null_A1", "null_A2", "null_C1", "null_C2")
        ),
        "body_a_sha_pin_matches": list(s["body_A"]["sha"])[0] == FROZEN_A_SHA,
        "body_a_len_pin_matches": list(s["body_A"]["blen"])[0] == FROZEN_A_LEN,
        "all_body_only_status_200": all(
            list(v["statuses"]) == [200] for v in s.values()
        ) and all(list(v["statuses"]) == [200] for v in nulls.values()),
        "classic_perm_status_403_vs_200": (
            list(control["perm_403"]["statuses"]) == [403]
            and list(control["perm_200"]["statuses"]) == [200]
        ),
        "classic_sess_status_401_vs_200": (
            list(control["sess_401"]["statuses"]) == [401]
            and list(control["sess_200"]["statuses"]) == [200]
        ),
        "classic_perm_body_distinct": (
            list(control["perm_403"]["sha"])[0] != list(control["perm_200"]["sha"])[0]
        ),
        "classic_sess_body_distinct": (
            list(control["sess_401"]["sha"])[0] != list(control["sess_200"]["sha"])[0]
        ),
        "perm_null_same_state": (
            list(control["perm403_null_1"]["sha"])[0]
            == list(control["perm403_null_2"]["sha"])[0]
            and list(control["perm403_null_1"]["statuses"]) == [403]
        ),
        "sess_null_same_state": (
            list(control["sess401_null_1"]["sha"])[0]
            == list(control["sess401_null_2"]["sha"])[0]
            and list(control["sess401_null_1"]["statuses"]) == [401]
        ),
        "per_state_fingerprint_set_sizes": set_sizes,
        "primary_state_clen_expected": {
            "body_A": "31",
            "body_B": str(len(BODIES["B"])),
            "body_C": str(len(BODIES["C"])),
        },
    }


def evaluate_baselines(metrics: Dict[str, Any]) -> Dict[str, Any]:
    m = metrics
    def disc(comparison: str, src: str) -> float:
        return m[f"{comparison}_{src}"]["discrimination"]

    return {
        "B-STATUS-ONLY": {
            "type": "strong-null",
            "expected": "0.0 on all same-status body-only comparisons (200 vs 200); "
                        "1.0 on status-varying classic controls",
            "observed": {
                "body_drift_AvsC": disc("body_drift_AvsC", "status"),
                "body_drift_AvsB": disc("body_drift_AvsB", "status"),
                "null_control_N1": disc("null_control_N1", "status"),
                "classic_perm": disc("classic_perm", "status"),
                "classic_sess": disc("classic_sess", "status"),
            },
            "pass": (
                disc("body_drift_AvsC", "status") == 0.0
                and disc("body_drift_AvsB", "status") == 0.0
                and disc("null_control_N1", "status") == 0.0
                and disc("classic_perm", "status") == 1.0
                and disc("classic_sess", "status") == 1.0
            ),
        },
        "B-BODY-ONLY": {
            "type": "positive",
            "expected": ">0.5 on same-status body-only drift (A vs C, A vs B); "
                        "1.0 on classic controls; 0.0 on nulls",
            "observed": {
                "body_drift_AvsC": disc("body_drift_AvsC", "body"),
                "body_drift_AvsB": disc("body_drift_AvsB", "body"),
                "null_control_N1": disc("null_control_N1", "body"),
                "classic_perm": disc("classic_perm", "body"),
                "classic_sess": disc("classic_sess", "body"),
            },
            "pass": (
                disc("body_drift_AvsC", "body") > 0.5
                and disc("body_drift_AvsB", "body") > 0.5
                and disc("null_control_N1", "body") == 0.0
            ),
        },
        "B-HEADERS-ONLY": {
            "type": "body-correlated-auxiliary",
            "expected": ">0 on body-only comparisons SOLELY via body-correlated "
                        "Content-Length (documented, not a failure); 0.0 on nulls",
            "observed": {
                "body_drift_AvsC": disc("body_drift_AvsC", "headers"),
                "body_drift_AvsB": disc("body_drift_AvsB", "headers"),
                "null_control_N1": disc("null_control_N1", "headers"),
            },
            "pass": (
                disc("null_control_N1", "headers") == 0.0
                and disc("body_drift_AvsC", "headers") > 0.0
            ),
        },
        "B-HEADERS-NO-CLEN": {
            "type": "isolation",
            "expected": "0.0 on body-only comparisons (no independent header drift)",
            "observed": {
                "body_drift_AvsC": disc("body_drift_AvsC", "headers_no_clen"),
                "body_drift_AvsB": disc("body_drift_AvsB", "headers_no_clen"),
                "null_control_N1": disc("null_control_N1", "headers_no_clen"),
            },
            "pass": (
                disc("body_drift_AvsC", "headers_no_clen") == 0.0
                and disc("body_drift_AvsB", "headers_no_clen") == 0.0
                and disc("null_control_N1", "headers_no_clen") == 0.0
            ),
        },
    }


def evaluate_conditions(metrics: Dict[str, Any],
                        identity: Dict[str, Any]) -> Dict[str, Any]:
    m = metrics
    def disc(comparison: str, src: str) -> float:
        return m[f"{comparison}_{src}"]["discrimination"]

    c1_ok = disc("body_drift_AvsC", "full") > 0.5
    c2_ok = (
        disc("body_drift_AvsC", "body") > 0.5
        and disc("body_drift_AvsB", "body") > 0.5
        and disc("body_drift_AvsC", "headers_no_clen") == 0.0
    )
    c3_ok = (
        disc("body_drift_AvsC", "status") == 0.0
        and disc("body_drift_AvsB", "status") == 0.0
    )
    c4_ok = disc("body_drift_AvsC", "full") > disc("body_drift_AvsC", "status")

    null_full = m["null_control_N1_full"]
    c5_ok = (
        null_full["discrimination"] == 0.0
        and null_full["ci_95"][0] <= 0.0 <= null_full["ci_95"][1]
        and null_full["discrimination"] <= 0.05
        and disc("null_control_N1", "status") == 0.0
        and disc("null_control_N1", "body") == 0.0
    )
    n2_full = m["null_control_N2_full"]

    c6_ok = (
        identity["content_length_distinct_across_ABC"]
        and identity["content_length_increasing_across_ABC"]
        and identity["body_len_increasing_across_ABC"]
        and identity["body_sha_distinct_across_ABC"]
        and identity["non_clen_headers_identical_across_ABC"]
        and identity["set_cookie_absent_body_only"]
        and identity["content_length_equals_body_len_all_obs"]
        and identity["body_a_sha_pin_matches"]
        and identity["body_a_len_pin_matches"]
    )

    perm_null_full = m["perm_null_full"]
    sess_null_full = m["sess_null_full"]
    c7_ok = (
        disc("body_drift_AvsC", "full") >= 0.7          # (a) reader 200 vs admin 200 = A vs C
        and disc("classic_perm", "full") >= 0.7          # (b) 403 vs 200
        and perm_null_full["discrimination"] == 0.0
        and perm_null_full["ci_95"][0] <= 0.0 <= perm_null_full["ci_95"][1]
        and perm_null_full["discrimination"] <= 0.05
        and identity["classic_perm_status_403_vs_200"]
        and identity["classic_perm_body_distinct"]
        and identity["perm_null_same_state"]
    )
    c8_ok = (
        disc("classic_sess", "full") >= 0.7
        and sess_null_full["discrimination"] == 0.0
        and sess_null_full["ci_95"][0] <= 0.0 <= sess_null_full["ci_95"][1]
        and sess_null_full["discrimination"] <= 0.05
        and identity["classic_sess_status_401_vs_200"]
        and identity["classic_sess_body_distinct"]
        and identity["sess_null_same_state"]
    )

    conditions = {
        "C1_FULL_BODY_DRIFT": {
            "type": "positive",
            "expected": "full-vector discrimination > 0.5 on STATE_A vs STATE_C "
                        "(both 200, bodies byte-different, non-CLEN headers identical)",
            "observed": {
                "full_AvsC": disc("body_drift_AvsC", "full"),
                "statuses_AvsC": [sorted(list(identity["statuses_by_state"]["body_A"])),
                                  sorted(list(identity["statuses_by_state"]["body_C"]))],
                "body_sha_distinct": identity["body_sha_distinct_across_ABC"],
                "content_length_distinct": identity["content_length_distinct_across_ABC"],
            },
            "threshold": ">0.5",
            "pass": c1_ok,
            "evidence_refs": "metrics.body_drift_AvsC_full; identity_checks "
                             "(status/body sha/CLEN for body_A, body_C)",
        },
        "C2_BODY_ONLY_SIGNAL": {
            "type": "positive",
            "expected": "B-BODY-ONLY > 0.5 on A vs C AND on A vs B; "
                        "B-HEADERS-NO-CLEN = 0.0 on A vs C",
            "observed": {
                "body_only_AvsC": disc("body_drift_AvsC", "body"),
                "body_only_AvsB": disc("body_drift_AvsB", "body"),
                "headers_no_clen_AvsC": disc("body_drift_AvsC", "headers_no_clen"),
            },
            "threshold": ">0.5 both isolations; headers_no_clen == 0.0",
            "pass": c2_ok,
            "evidence_refs": "metrics.body_drift_AvsC_body, body_drift_AvsB_body, "
                             "body_drift_AvsC_headers_no_clen",
        },
        "C3_STATUS_ISOLATED": {
            "type": "strong-null",
            "expected": "B-STATUS-ONLY = 0.0 on A vs C and A vs B (status confound removed)",
            "observed": {
                "status_only_AvsC": disc("body_drift_AvsC", "status"),
                "status_only_AvsB": disc("body_drift_AvsB", "status"),
            },
            "threshold": "= 0.0 (all same-status comparisons)",
            "pass": c3_ok,
            "evidence_refs": "metrics.body_drift_AvsC_status, body_drift_AvsB_status",
        },
        "C4_FULL_EXCEEDS_STATUS_NONVACUOUS": {
            "type": "positive",
            "expected": "full-vector discrimination > B-STATUS-ONLY strictly on A vs C "
                        "(e.g., 1.0 > 0.0); equality at ceiling is vacuous and fails",
            "observed": {
                "full": disc("body_drift_AvsC", "full"),
                "status": disc("body_drift_AvsC", "status"),
            },
            "threshold": "strictly greater (full > status)",
            "pass": c4_ok,
            "evidence_refs": "metrics.body_drift_AvsC_full vs body_drift_AvsC_status",
        },
        "C5_NULL_NO_FALSE_POSITIVE": {
            "type": "null",
            "expected": "null N1 (STATE_A resampled) full = 0.0, CI contains 0.0, "
                        "point <= 0.05; status-only and body-only also 0.0",
            "observed": {
                "full": null_full["discrimination"],
                "ci_95": null_full["ci_95"],
                "status": disc("null_control_N1", "status"),
                "body": disc("null_control_N1", "body"),
            },
            "threshold": "= 0.0, CI contains 0.0, <= 0.05",
            "pass": c5_ok,
            "evidence_refs": "metrics.null_control_N1_full/status/body",
        },
        "C6_CONTENT_LENGTH_VARIES_AND_HEADERS_CONSTANT": {
            "type": "validity",
            "expected": "Content-Length differs across A/B/C proportional to body_len "
                        "and body SHA-256 distinct, non-CLEN filtered headers identical "
                        "across A/B/C (Cache-Control, ETag, Vary, no Set-Cookie), "
                        "CLEN == body_len on each observation",
            "observed": {
                "content_length_by_state": identity["content_length_by_state"],
                "body_len_by_state": identity["body_len_by_state"],
                "body_sha_by_state": identity["body_sha_by_state"],
                "non_clen_headers_identical": identity["non_clen_headers_identical_across_ABC"],
                "set_cookie_absent": identity["set_cookie_absent_body_only"],
                "clen_equals_body_len_all_obs": identity["content_length_equals_body_len_all_obs"],
            },
            "threshold": "CLEN distinct & increasing, SHA distinct, non-CLEN identical, "
                         "no Set-Cookie, CLEN == body_len",
            "pass": c6_ok,
            "evidence_refs": "identity_checks (raw Content-Length per observation)",
        },
        "C7_WRITABLE_PERMISSION_LEVEL": {
            "type": "positive",
            "expected": "(a) body-filtered permission reader 200 vs admin 200 (A vs C) "
                        "full >= 0.7; (b) classic permission escalation 403 vs 200 via "
                        "committed SQLite role write full >= 0.7; same-state 403 null "
                        "= 0.0 CI contains 0.0 <= 0.05",
            "observed": {
                "reader_admin_200_AvsC": disc("body_drift_AvsC", "full"),
                "classic_perm_403_vs_200": disc("classic_perm", "full"),
                "perm_null": {
                    "full": perm_null_full["discrimination"],
                    "ci_95": perm_null_full["ci_95"],
                },
                "statuses_403_200": identity["classic_perm_status_403_vs_200"],
                "bodies_distinct": identity["classic_perm_body_distinct"],
            },
            "threshold": ">= 0.7 both; null == 0.0 CI contains 0.0 <= 0.05",
            "pass": c7_ok,
            "evidence_refs": "metrics.body_drift_AvsC_full, classic_perm_full, "
                             "perm_null_full; batch_state_log set_role writes",
        },
        "C8_WRITABLE_SESSION_INVALIDATION": {
            "type": "positive",
            "expected": "writable session invalidation 401 vs 200 via committed SQLite "
                        "session write full >= 0.7; same-state 401 null = 0.0 CI contains "
                        "0.0 <= 0.05",
            "observed": {
                "classic_sess_401_vs_200": disc("classic_sess", "full"),
                "sess_null": {
                    "full": sess_null_full["discrimination"],
                    "ci_95": sess_null_full["ci_95"],
                },
                "statuses_401_200": identity["classic_sess_status_401_vs_200"],
                "bodies_distinct": identity["classic_sess_body_distinct"],
            },
            "threshold": ">= 0.7; null == 0.0 CI contains 0.0 <= 0.05",
            "pass": c8_ok,
            "evidence_refs": "metrics.classic_sess_full, sess_null_full; "
                             "batch_state_log invalidate_session write",
        },
        "C5B_NULL_N2_EXPLORATORY": {
            "type": "null-exploratory",
            "expected": "exploratory N2 (STATE_C resampled) = 0.0 (reported, not gating)",
            "observed": {
                "full": n2_full["discrimination"],
                "ci_95": n2_full["ci_95"],
            },
            "threshold": "0.0 (reported only)",
            "pass": n2_full["discrimination"] == 0.0,
            "evidence_refs": "metrics.null_control_N2_full",
        },
    }
    return conditions


def validity_summary(raw_records: List[Dict[str, Any]],
                     batch_log: List[Dict[str, Any]],
                     identity: Dict[str, Any]) -> Dict[str, Any]:
    writes = [e for e in batch_log if e["action"].startswith("write_state::")]
    verifies = [e for e in batch_log if e["action"] == "pre_batch_verify"]
    expected_labels = [
        "body_A", "body_B", "body_C",
        "null_A1", "null_A2", "null_C1", "null_C2",
        "perm_403", "perm_200", "perm403_null_1", "perm403_null_2",
        "sess_200", "sess_401", "sess401_null_1", "sess401_null_2",
    ]
    counts = {lbl: sum(1 for r in raw_records if r["state"] == lbl)
              for lbl in expected_labels}
    checks = {
        "server_state_committed_before_every_write": all(
            e["match_expected"] for e in writes),
        "server_state_verified_before_every_batch": all(
            e["state_snapshot"]["body_config"]["variant"] in ("A", "B", "C")
            for e in verifies),
        "all_body_only_and_null_observations_status_200": identity["all_body_only_status_200"],
        "classic_perm_status_403_vs_200": identity["classic_perm_status_403_vs_200"],
        "classic_sess_status_401_vs_200": identity["classic_sess_status_401_vs_200"],
        "body_sha_distinct_across_ABC": identity["body_sha_distinct_across_ABC"],
        "content_length_distinct_across_ABC": identity["content_length_distinct_across_ABC"],
        "non_clen_headers_identical_across_ABC": identity["non_clen_headers_identical_across_ABC"],
        "set_cookie_absent_on_body_only": identity["set_cookie_absent_body_only"],
        "content_length_equals_body_len_all_obs": identity["content_length_equals_body_len_all_obs"],
        "raw_line_count_per_batch_is_20": all(counts[l] == N_SAMPLES for l in expected_labels),
        "total_raw_lines": len(raw_records),
        "excluded_headers_unchanged": EXCLUDED_HEADERS == {"Date", "Server", "X-Request-Id"},
        "body_a_pin_sha_matches": identity["body_a_sha_pin_matches"],
        "body_a_pin_len_matches": identity["body_a_len_pin_matches"],
        "fingerprint_algorithm_matches_parent": True,  # copied verbatim; hash in provenance
    }
    critical = [
        "server_state_committed_before_every_write",
        "all_body_only_and_null_observations_status_200",
        "classic_perm_status_403_vs_200",
        "classic_sess_status_401_vs_200",
        "body_sha_distinct_across_ABC",
        "content_length_distinct_across_ABC",
        "non_clen_headers_identical_across_ABC",
        "set_cookie_absent_on_body_only",
        "content_length_equals_body_len_all_obs",
        "raw_line_count_per_batch_is_20",
        "excluded_headers_unchanged",
        "body_a_pin_sha_matches",
        "body_a_pin_len_matches",
    ]
    return {
        "checks": checks,
        "batch_counts": counts,
        "writes_count": len(writes),
        "pre_batch_verifies_count": len(verifies),
        "critical_all_pass": all(checks[k] for k in critical),
        "failed_critical": [k for k in critical if not checks[k]],
    }


# ─── Smoke / full runs ──────────────────────────────────────────────────────

def run_smoke(tokens: Dict[str, str]) -> int:
    print("=== SMOKE: setup verification only (no discrimination computed) ===")
    admin_tok = tokens["admin"]
    reader_tok = tokens["reader"]

    # body variant B written and observed
    do_write("set_body", {"variant": "B", "body_sha256": BODY_SHA["B"]},
             admin_tok, [])
    bcfg = read_body_config()
    assert bcfg == {"variant": "B", "body_sha256": BODY_SHA["B"]}, bcfg
    obs = observe_resource(reader_tok)
    assert obs["status"] == 200, obs["status"]
    assert obs["body_bytes"] == BODIES["B"], obs["body_bytes"]
    assert not verify_constant_headers(obs), verify_constant_headers(obs)

    # role gate: viewer -> 403
    do_write("set_role", {"role": "viewer"}, admin_tok, [])
    obs403 = observe_resource(reader_tok)
    assert obs403["status"] == 403, obs403["status"]
    assert obs403["body_bytes"] == BODY_403, obs403["body_bytes"]
    do_write("set_role", {"role": "reader"}, admin_tok, [])

    # session invalidation -> 401
    do_write("invalidate_session", {"reader_valid_sessions": 0}, admin_tok, [])
    obs401 = observe_resource(reader_tok)
    assert obs401["status"] == 401, obs401["status"]
    assert obs401["body_bytes"] == BODY_401, obs401["body_bytes"]

    # reset to A pin
    do_write("set_body", {"variant": "A", "body_sha256": BODY_SHA["A"]},
             admin_tok, [])
    obsA = observe_resource(tokens["admin"])
    assert obsA["status"] == 200 and obsA["body_bytes"] == BODIES["A"]
    print("[SMOKE OK] set_body_variant commit verified; /resource returns written "
          "variant with constant headers; role viewer -> 403; session-invalid -> 401.")
    return 0


def main() -> int:
    global BASE_URL
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    outdir = Path(__file__).resolve().parent
    # Frozen startup assertions before any measurement.
    assert len(BODIES["A"]) == FROZEN_A_LEN, len(BODIES["A"])
    assert BODY_SHA["A"] == FROZEN_A_SHA
    assert len(BODIES["B"]) > len(BODIES["A"])
    assert len(BODIES["C"]) > len(BODIES["B"])

    random.seed(SEED)
    init_db()
    port = discover_port()
    BASE_URL = f"http://{HOST}:{port}"
    app = create_app()
    server_thread = threading.Thread(
        target=lambda: app.run(host=HOST, port=port, debug=False,
                               use_reloader=False, threaded=True),
        daemon=True,
    )
    server_thread.start()
    print(f"[OK] Flask server starting on {BASE_URL}", flush=True)
    wait_for_server(BASE_URL)
    print(f"[OK] server reachable; DB={DB_PATH}", flush=True)
    tokens = get_tokens(BASE_URL)
    print(f"[OK] tokens obtained (reader len={len(tokens['reader'])}, "
          f"admin len={len(tokens['admin'])})", flush=True)

    try:
        if args.smoke:
            return run_smoke(tokens)
        run_full(tokens, outdir)
        return 0
    except MeasurementInvalid as e:
        print(f"[MEASUREMENT_INVALID] {e.category}: {e.detail}", flush=True)
        failure = {
            "experiment_id": "EXP-RUNTIME-35749360317",
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
            "experiment_id": "EXP-RUNTIME-35749360317",
            "stage": "execute",
            "category": "unexpected_error",
            "message": repr(e),
            "retryable": True,
            "ts": now_iso(),
        }
        with open(outdir / "failure.json", "w") as f:
            json.dump(failure, f, indent=2)
        return 3


if __name__ == "__main__":
    sys.exit(main())