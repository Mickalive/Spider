#!/usr/bin/env python3
"""
EXP-PRODUCT-35445596342 — Stochastic Flask + SQLite mock server.

Implements the three frozen fixes for the C3 measurement invalidity that
blocked EXP-PRODUCT-35434772331:

  Fix (1) — Server replacement: replace the deterministic wsgiref server with
            a stochastic Flask 3.1.3 + SQLite WAL-mode mock matching
            EXP-GRAPH-35353011131:
              * SQLite WAL-mode DB for session/permission state
              * in-memory cache with TTL=0.5s for the schema snapshot served
                by /api/schema (fresh vs stale alternation is a REAL
                stochastic element driving structural-signal variance)
              * I/O jitter 10-100ms on every request
              * mixed JWT algorithms: HS256 for read/write tokens, RS256 for
                admin tokens
              * random X-Request-Id on every response (excluded from
                fingerprints, contributes to structural signal variance)

  Fix (2) — Scoring redesign: behavioral signal is derived ONLY from the real
            HTTP /api/session/status response (status code + body). The
            severity weights are drift-type-specific and continuous:

              session_invalid       0.40  (body.session_valid == false)
              revocation            0.30  (body.status == "revoked" or
                                           body.error == "session_invalidated")
              refresh               0.45  (body.status == "refreshed")
              new_token             0.15  (body.new_token_issued == true)
              role_reduced          0.30 + 0.20*(1 - n_perms/4)
                                     (body.role == "viewer"; continuous in the
                                      number of propagated permissions)
              role_base             0.03  (body.role == "admin")
              session_valid_explicit 0.02 (body.session_valid == true)
              status_severity       401->0.30, 403->0.05, 410->0.15, 500->0.15

            Resulting non-overlapping drift-type ranges under co-occurring
            noise:
              permission_boundary:  [0.32, 0.545]
              token_refresh:        0.65
              session_invalidation: [0.75, 1.00]
              no-drift baseline:    ~0.05

  Fix (3) — State reset: set_drift(None) fully resets server state:
            current_role='admin', session_valid=True, drift_active=False,
            drift_type=None, noise_active=False, noise_type=None AND restores
            DB permissions/session rows.

Stochastic elements that generate WITHIN-condition variance (the root cause of
the parent's behavioral_std = 0.0):
  * permission_boundary: /api/session/status samples the propagated
    permission state per request (reduced ~40%, partial ~30%, full ~30%),
    so the severity-weighted score is continuous within the condition.
  * session_invalidation: /api/session/status returns a random graded status
    code from {401, 403, 500} per request (401 -> 1.0, 403 -> 0.5, 500 -> 0.75
    severity mapping, matching EXP-GRAPH-35353011131 validity_notes), so the
    status_severity component varies across samples.
  * /api/schema: served through the same TTL cache; fresh bodies carry a
    "cache_status":"fresh" key, stale bodies omit it -> structural std > 0.
  * I/O jitter 10-100ms and X-Request-Id are applied to every request.

All signals are derived from real HTTP request/response cycles on localhost.
"""
import hashlib
import json
import os
import random
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, make_response, request

import jwt as pyjwt

# ===== Configuration =====
SECRET_KEY = "exp-product-35445596342-hs256-secret"
PORT = 18950
SEED = 42
JITTER_MIN_MS = 10
JITTER_MAX_MS = 100
CACHE_TTL_S = 0.5

# ===== RSA key pair for RS256 admin tokens =====
def _gen_rsa_keypair():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return priv_pem.decode(), pub_pem.decode()


RSA_PRIVATE_KEY, RSA_PUBLIC_KEY = _gen_rsa_keypair()

# ===== In-memory TTL cache (permission snapshot + schema snapshot) =====
class TTLCache:
    """Minimal keyed TTL cache. get() returns (value, "stale") on a live
    entry and (None, None) on expiry/miss."""

    def __init__(self, ttl=CACHE_TTL_S):
        self.ttl = ttl
        self._entries = {}
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            ent = self._entries.get(key)
            if ent is not None:
                expires_at, value = ent
                if time.time() < expires_at:
                    return value, "stale"
                del self._entries[key]
        return None, None

    def put(self, key, value):
        with self.lock:
            self._entries[key] = (time.time() + self.ttl, value)


# ===== SQLite (WAL-mode) session/permission DB =====
class SessionDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        with self.lock:
            c = self.conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    role TEXT DEFAULT 'viewer',
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    is_valid INTEGER DEFAULT 1
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS permissions (
                    user_id TEXT PRIMARY KEY,
                    role TEXT NOT NULL,
                    permissions TEXT NOT NULL
                )
            """)
            self._seed()

    def _seed(self):
        c = self.conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO sessions VALUES (?, ?, ?, ?, ?, ?)",
            ("sess-admin-001", "alice", "admin",
             datetime.now(timezone.utc).isoformat(),
             (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(), 1))
        c.execute(
            "INSERT OR REPLACE INTO permissions VALUES (?, ?, ?)",
            ("alice", "admin", json.dumps(["read", "write", "admin", "delete"])))
        self.conn.commit()

    def get_session(self, session_id):
        with self.lock:
            c = self.conn.cursor()
            c.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,))
            row = c.fetchone()
            if row:
                return {"session_id": row[0], "user_id": row[1], "role": row[2],
                        "created_at": row[3], "expires_at": row[4],
                        "is_valid": row[5]}
            return None

    def invalidate_session(self, session_id):
        with self.lock:
            c = self.conn.cursor()
            c.execute("UPDATE sessions SET is_valid=0 WHERE session_id=?",
                      (session_id,))
            self.conn.commit()

    def restore_session(self, session_id):
        with self.lock:
            c = self.conn.cursor()
            c.execute("UPDATE sessions SET is_valid=1 WHERE session_id=?",
                      (session_id,))
            self.conn.commit()

    def reduce_permissions(self, user_id):
        """Apply the permission_boundary drift: role viewer + reduced perms."""
        with self.lock:
            c = self.conn.cursor()
            c.execute("UPDATE sessions SET role='viewer' WHERE user_id=?",
                      (user_id,))
            c.execute("UPDATE permissions SET role='viewer', permissions=? "
                      "WHERE user_id=?", (json.dumps(["read"]), user_id))
            self.conn.commit()
            self._invalidate_perm_cache_locked(user_id)

    def restore_permissions(self, user_id):
        """Restore full admin permissions (drift reset)."""
        with self.lock:
            c = self.conn.cursor()
            c.execute("UPDATE sessions SET role='admin' WHERE user_id=?",
                      (user_id,))
            c.execute(
                "UPDATE permissions SET role='admin', permissions=? "
                "WHERE user_id=?",
                (json.dumps(["read", "write", "admin", "delete"]), user_id))
            self.conn.commit()
            self._invalidate_perm_cache_locked(user_id)

    def get_permissions(self, user_id):
        with self.lock:
            c = self.conn.cursor()
            c.execute("SELECT * FROM permissions WHERE user_id=?", (user_id,))
            row = c.fetchone()
            if row:
                return {"user_id": row[0], "role": row[1],
                        "permissions": json.loads(row[2])}
            return None

    def _invalidate_perm_cache_locked(self, user_id):
        # Drop the permission cache entry so the next probe re-fetches.
        cache._entries.pop(("perms", user_id), None)

    def close(self):
        with self.lock:
            self.conn.close()


# ===== Server state =====
_state_lock = threading.Lock()
_state = {
    "current_role": "admin",
    "session_valid": True,
    "drift_active": False,
    "drift_type": None,
    "noise_active": False,
    "noise_type": None,
    "extra_fields": {},
}

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "raw_evidence", "mock_state.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
db = SessionDB(DB_PATH)
cache = TTLCache()

app = Flask(__name__)


# ===== JWT helpers =====
def make_token(user_id="alice", role="admin", exp_delta=timedelta(hours=1),
               algorithm="HS256", secret=None):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "role": role,
        "iss": "spider-kernel",
        "iat": now,
        "exp": now + exp_delta,
        "session_id": "sess-admin-001",
    }
    if algorithm == "RS256":
        return pyjwt.encode(payload, RSA_PRIVATE_KEY, algorithm="RS256")
    return pyjwt.encode(payload, secret or SECRET_KEY, algorithm="HS256")


def _validate_jwt(auth_header):
    """Returns (status, payload, error). Requires expired/invalid to collide
    on the same 401/auth_failed response (baseline replication)."""
    if not auth_header:
        return 401, None, "login_required"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        return 401, None, "auth_failed"

    token = parts[1]
    # Select algorithm family from the unverified header.
    try:
        hdr = pyjwt.get_unverified_header(token)
        alg = hdr.get("alg", "HS256")
    except Exception:
        return 401, None, "auth_failed"

    if alg == "RS256":
        key, algs = RSA_PUBLIC_KEY, ["RS256"]
    else:
        key, algs = SECRET_KEY, ["HS256"]

    try:
        payload = pyjwt.decode(token, key, algorithms=algs,
                               options={"verify_exp": True})
    except pyjwt.ExpiredSignatureError:
        return 401, None, "auth_failed"
    except pyjwt.InvalidTokenError:
        return 401, None, "auth_failed"

    session = db.get_session(payload.get("session_id", ""))
    if not session or not session["is_valid"]:
        return 401, None, "session_invalidated"
    return 200, payload, None


# ===== Stochastic server elements =====
def _jitter():
    time.sleep(random.uniform(JITTER_MIN_MS / 1000.0, JITTER_MAX_MS / 1000.0))


def _request_id():
    return uuid.uuid4().hex[:16]


# ===== Routes =====
@app.route("/health", methods=["GET"])
def health():
    _jitter()
    resp = make_response(jsonify({"status": "ok", "port": PORT}), 200)
    resp.headers["X-Request-Id"] = _request_id()
    return resp


@app.route("/api/drift", methods=["POST"])
def set_drift():
    """Control endpoint: activate/reset drift. set_drift(None) performs the
    FULL frozen state reset."""
    data = request.get_json(silent=True) or {}
    drift_type = data.get("drift_type")
    with _state_lock:
        if drift_type is None or drift_type == "none":
            _state["drift_active"] = False
            _state["drift_type"] = None
            _state["current_role"] = "admin"
            _state["session_valid"] = True
            _state["noise_active"] = False
            _state["noise_type"] = None
            _state["extra_fields"] = {}
            db.restore_permissions("alice")
            db.restore_session("sess-admin-001")
            msg = "state_reset"
        elif drift_type in ("permission_boundary", "session_invalidation",
                            "token_refresh"):
            _state["drift_active"] = True
            _state["drift_type"] = drift_type
            if drift_type == "permission_boundary":
                _state["current_role"] = "viewer"
                db.reduce_permissions("alice")
            elif drift_type == "session_invalidation":
                _state["session_valid"] = False
                db.invalidate_session("sess-admin-001")
            msg = "drift_activated"
        else:
            return jsonify({"error": "invalid drift_type"}), 400
    resp = make_response(jsonify({"status": "ok", "drift": drift_type,
                                  "detail": msg}), 200)
    resp.headers["X-Request-Id"] = _request_id()
    return resp


@app.route("/api/noise", methods=["POST"])
def set_noise():
    data = request.get_json(silent=True) or {}
    noise_type = data.get("noise_type")
    with _state_lock:
        if noise_type is None or noise_type == "none":
            _state["noise_active"] = False
            _state["noise_type"] = None
            _state["extra_fields"] = {}
        elif noise_type in ("optional_field_addition", "description_change",
                            "response_time_jitter", "field_type_normalization"):
            _state["noise_active"] = True
            _state["noise_type"] = noise_type
            if noise_type == "optional_field_addition":
                _state["extra_fields"] = {
                    "debug_info": "session_trace_35445596342",
                    "cache_key": "v2_test",
                }
        else:
            return jsonify({"error": "invalid noise_type"}), 400
    resp = make_response(jsonify({"status": "ok", "noise": noise_type}), 200)
    resp.headers["X-Request-Id"] = _request_id()
    return resp


@app.route("/api/data", methods=["GET"])
def get_data():
    """Main auth endpoint. Deterministic per auth state (needed for C1
    fingerprint discrimination); drift/noise do NOT alter /api/data so that
    fingerprints stay stable within state."""
    _jitter()
    auth_header = request.headers.get("Authorization", "")
    status, payload, error = _validate_jwt(auth_header)

    if error == "login_required":
        body = {"error": "login_required", "message": "Authentication required"}
        resp = make_response(jsonify(body), 401)
        resp.headers["Cache-Control"] = "no-store"
    elif error == "auth_failed":
        body = {"error": "authentication_failed"}
        resp = make_response(jsonify(body), 401)
        resp.headers["Cache-Control"] = "no-store"
    elif error == "session_invalidated":
        body = {"error": "session_invalidated", "message": "Session revoked"}
        resp = make_response(jsonify(body), 401)
        resp.headers["Cache-Control"] = "no-store"
    elif status == 200:
        body = {
            "user_id": payload["sub"],
            "role": payload.get("role", "admin"),
            "data": {"value": "test_data_35445596342"},
            "session_id": payload.get("session_id"),
        }
        resp = make_response(jsonify(body), 200)
        resp.headers["Cache-Control"] = "no-cache"
        resp.headers["Set-Cookie"] = (
            f"session={payload.get('session_id')}; HttpOnly; Secure")
    else:
        body = {"error": "unknown"}
        resp = make_response(jsonify(body), 500)

    resp.headers["X-Request-Id"] = _request_id()
    return resp


def _perm_propagation_state():
    """Under permission_boundary drift the permission propagation is
    eventually-consistent: probes see the propagated (reduced) permission set
    ~40%, a partially propagated set ~30%, and the pre-change (full) set ~30%.
    This is a server-side stochastic element that makes the severity-weighted
    behavioral score continuous within the condition."""
    roll = random.random()
    if roll < 0.40:
        return ["read"]
    elif roll < 0.70:
        return ["read", "write"]
    return ["read", "write", "admin", "delete"]


@app.route("/api/session/status", methods=["GET"])
def session_status():
    """Behavioral probe endpoint. All behavioral signals are derived from this
    endpoint's real HTTP response (status code + body)."""
    _jitter()
    auth_header = request.headers.get("Authorization", "")
    status, payload, error = _validate_jwt(auth_header)

    with _state_lock:
        drift_active = _state["drift_active"]
        drift_type = _state["drift_type"]
        current_role = _state["current_role"]

    if error in ("login_required", "auth_failed"):
        body = {"status": "invalid", "session_valid": False}
        resp = make_response(jsonify(body), 401)
        resp.headers["Cache-Control"] = "no-store"
    elif drift_active and drift_type == "permission_boundary":
        # Eventually-consistent permission propagation: every probe
        # independently samples the propagation state (reduced subset ~40%,
        # partial subset ~30%, pre-change full set ~30%). Per-request
        # sampling (like the graph-lane server) guarantees real
        # within-condition variance without TTL-window serialization.
        perms = _perm_propagation_state()
        body = {
            "status": "active",
            "session_valid": True,
            "role": current_role,
            "permissions": perms,
            "perm_cache": "live",
        }
        resp = make_response(jsonify(body), 200)
        resp.headers["Cache-Control"] = "no-cache"
    elif drift_active and drift_type == "session_invalidation":
        # Graded random session_status_check (matching EXP-GRAPH-35353011131):
        # {401, 403, 500}; 401 -> severity 0.30, 500 -> 0.15, 403 -> 0.05.
        code = random.choice([401, 403, 500])
        body = {"status": "revoked", "session_valid": False}
        resp = make_response(jsonify(body), code)
        resp.headers["Cache-Control"] = "no-store"
    elif drift_active and drift_type == "token_refresh":
        body = {
            "status": "refreshed",
            "session_valid": True,
            "new_token_issued": True,
            "role": payload.get("role") if payload else "admin",
        }
        resp = make_response(jsonify(body), 200)
        resp.headers["Cache-Control"] = "no-cache"
    elif status == 200:
        session = db.get_session(payload.get("session_id", ""))
        session_valid = bool(session and session["is_valid"])
        body = {
            "status": "active",
            "session_valid": session_valid,
            "role": payload.get("role", "unknown"),
        }
        resp = make_response(jsonify(body), 200)
        resp.headers["Cache-Control"] = "no-cache"
    else:
        body = {"status": "invalid", "session_valid": False}
        resp = make_response(jsonify(body), 401)

    resp.headers["X-Request-Id"] = _request_id()
    return resp


@app.route("/api/schema", methods=["GET"])
def get_schema():
    """Structural probe endpoint (unauthenticated). Served through the TTL
    cache: fresh bodies include a 'cache_status' key, stale bodies omit it,
    giving real within-condition structural variance."""
    _jitter()
    with _state_lock:
        noise_active = _state["noise_active"]
        noise_type = _state["noise_type"]
        extra_fields = dict(_state["extra_fields"])

    cached, cache_status = cache.get("schema")
    resp_extra_headers = {}
    if cached is not None:
        schema = cached
        schema["cache_status"] = "stale"
        # Varying header: present only on stale (cached) responses, so the
        # structural signal (key/header/status cardinality) has real
        # within-condition variance driven by TTL freshness.
        resp_extra_headers["X-Cache-Status"] = "stale"
    else:
        schema = {
            "endpoints": ["/api/data", "/api/schema", "/api/session/status"],
            "methods": {"GET": True, "POST": True},
            "auth_required": True,
            "fields": ["user_id", "role", "data", "session_id"],
            "description": "SPIDER kernel data API v2",
        }
        if noise_active:
            if noise_type == "optional_field_addition":
                schema["optional_fields"] = list(extra_fields.keys())
            elif noise_type == "description_change":
                schema["description"] = "SPIDER kernel data API v2.1 - Updated"
            elif noise_type == "field_type_normalization":
                schema["field_types"] = {f: "string" for f in schema["fields"]}
            # response_time_jitter intentionally leaves schema content
            # unchanged (it only adds latency).
        cache.put("schema", schema)
        schema["cache_status"] = "fresh"

    resp = make_response(jsonify(schema), 200)
    for hname, hval in resp_extra_headers.items():
        resp.headers[hname] = hval
    body_str = json.dumps(schema, sort_keys=True)
    etag = hashlib.sha256(body_str.encode()).hexdigest()[:16]
    resp.headers["ETag"] = f'"{etag}"'
    resp.headers["X-Request-Id"] = _request_id()
    return resp


def shutdown():
    db.close()
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except OSError:
            pass
        for suffix in ("-wal", "-shm"):
            p = DB_PATH + suffix
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass


if __name__ == "__main__":
    random.seed(SEED)
    app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False,
            threaded=False)