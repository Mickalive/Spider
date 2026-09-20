#!/usr/bin/env python3
"""
EXP-PRODUCT-35481773764 — Stochastic Flask + SQLite mock server with production-like structural noise.

Based on EXP-PRODUCT-35476271728/mock_server.py with the following changes:
- 4 NEW production-like structural noise types REPLACE the 4 parent simplistic types for co-occurring conditions.
- Parent types are retained for isolated baseline comparison only (not used in co-occurring conditions).
- Stochastic token_refresh drift with p_refresh_success=0.7.

Production-like noise types:
1. pagination_metadata: adds pagination fields (page, per_page, total_count, has_next) to response body, varying 2-6 per request.
2. variable_length_data: response body data_list length varies 0-8 items per request.
3. error_format_variation: error responses use different formats depending on error type.
4. cdn_cache_headers: adds CDN-specific response headers.

All other drift types and structural noise mechanisms remain identical to the parent experiment.
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
SECRET_KEY = "exp-product-35481773764-hs256-secret"
PORT = 18951
SEED = 42
JITTER_MIN_MS = 10
JITTER_MAX_MS = 100
CACHE_TTL_S = 0.5

# ===== Token refresh stochasticity =====
P_REFRESH_SUCCESS = 0.7

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

# ===== In-memory TTL cache =====
class TTLCache:
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
        with self.lock:
            c = self.conn.cursor()
            c.execute("UPDATE sessions SET role='viewer' WHERE user_id=?",
                      (user_id,))
            c.execute("UPDATE permissions SET role='viewer', permissions=? "
                      "WHERE user_id=?", (json.dumps(["read"]), user_id))
            self.conn.commit()
            self._invalidate_perm_cache_locked(user_id)

    def restore_permissions(self, user_id):
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
    if not auth_header:
        return 401, None, "login_required"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        return 401, None, "auth_failed"

    token = parts[1]
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


# ===== Production-like noise helpers =====
def _pagination_metadata():
    """Add pagination fields to response body, varying 2-6 per request."""
    page = random.randint(1, 10)
    per_page = random.choice([10, 20, 50, 100])
    total_count = random.randint(100, 1000)
    has_next = random.choice([True, False])
    fields = {"page": page, "per_page": per_page, "total_count": total_count, "has_next": has_next}
    # Randomly select 2-6 fields to include
    n_fields = random.randint(2, 6)
    selected_keys = random.sample(list(fields.keys()), min(n_fields, len(fields)))
    return {k: fields[k] for k in selected_keys}


def _variable_length_data():
    """Add data_list with variable length 0-8 items."""
    n_items = random.randint(0, 8)
    data_list = []
    for i in range(n_items):
        item = {
            "id": random.randint(1000, 9999),
            "name": f"item_{i}_{uuid.uuid4().hex[:4]}",
            "value": round(random.uniform(0.0, 100.0), 2),
            "active": random.choice([True, False]),
        }
        data_list.append(item)
    return {"data_list": data_list, "count": n_items}


def _error_format_variation(status_code):
    """Return error body format depending on status code."""
    if status_code == 401:
        return {"error": "authentication_failed", "message": "Invalid or expired token", "code": "AUTH_ERR_001"}
    elif status_code == 403:
        return {"error": "forbidden", "message": "Insufficient permissions", "required_permission": "admin"}
    elif status_code == 500:
        return {"error": "internal_server_error", "message": "Unexpected error", "request_id": uuid.uuid4().hex[:16]}
    else:
        return {"error": "unknown", "message": "Error occurred"}


def _cdn_cache_headers():
    """Return CDN-specific headers."""
    return {
        "X-Cache": random.choice(["HIT", "MISS"]),
        "X-CDN-Cache-Control": f"max-age={random.randint(0, 300)}",
        "Age": str(random.randint(0, 60)),
        "CF-Ray": str(uuid.uuid4()),
    }


# ===== Routes =====
@app.route("/health", methods=["GET"])
def health():
    _jitter()
    resp = make_response(jsonify({"status": "ok", "port": PORT}), 200)
    resp.headers["X-Request-Id"] = _request_id()
    return resp


@app.route("/api/drift", methods=["POST"])
def set_drift():
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
                            "response_time_jitter", "field_type_normalization",
                            "pagination_metadata", "variable_length_data",
                            "error_format_variation", "cdn_cache_headers"):
            _state["noise_active"] = True
            _state["noise_type"] = noise_type
            if noise_type == "optional_field_addition":
                _state["extra_fields"] = {
                    "debug_info": "session_trace_35456068953",
                    "cache_key": "v2_test",
                }
        else:
            return jsonify({"error": "invalid noise_type"}), 400
    resp = make_response(jsonify({"status": "ok", "noise": noise_type}), 200)
    resp.headers["X-Request-Id"] = _request_id()
    return resp


@app.route("/api/data", methods=["GET"])
def get_data():
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
            "data": {"value": "test_data_35456068953"},
            "session_id": payload.get("session_id"),
        }
        resp = make_response(jsonify(body), 200)
        resp.headers["Cache-Control"] = "no-cache"
        resp.headers["Set-Cookie"] = (
            f"session={payload.get('session_id')}; HttpOnly; Secure")
    else:
        body = {"error": "unknown"}
        resp = make_response(jsonify(body), 500)

    # Apply production-like noise if active
    with _state_lock:
        noise_active = _state["noise_active"]
        noise_type = _state["noise_type"]
    if noise_active:
        if noise_type == "pagination_metadata":
            pagination = _pagination_metadata()
            body.update(pagination)
        elif noise_type == "variable_length_data":
            data_list = _variable_length_data()
            body.update(data_list)
        elif noise_type == "error_format_variation" and resp.status_code >= 400:
            error_body = _error_format_variation(resp.status_code)
            body = error_body
        elif noise_type == "cdn_cache_headers":
            cdn_headers = _cdn_cache_headers()
            for k, v in cdn_headers.items():
                resp.headers[k] = v

    resp.headers["X-Request-Id"] = _request_id()
    return resp


def _perm_propagation_state():
    roll = random.random()
    if roll < 0.40:
        return ["read"]
    elif roll < 0.70:
        return ["read", "write"]
    return ["read", "write", "admin", "delete"]


@app.route("/api/session/status", methods=["GET"])
def session_status():
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
        code = random.choice([401, 403, 500])
        body = {"status": "revoked", "session_valid": False}
        resp = make_response(jsonify(body), code)
        resp.headers["Cache-Control"] = "no-store"
    elif drift_active and drift_type == "token_refresh":
        refresh_success = random.random() < P_REFRESH_SUCCESS
        if refresh_success:
            body = {
                "status": "refreshed",
                "session_valid": True,
                "new_token_issued": True,
                "role": payload.get("role") if payload else "admin",
            }
            resp = make_response(jsonify(body), 200)
        else:
            body = {
                "status": "token_refresh_error",
                "session_valid": True,
                "new_token_issued": False,
                "role": payload.get("role") if payload else "admin",
                "error": "refresh_token_invalid",
            }
            resp = make_response(jsonify(body), 401)
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

    # Apply production-like noise if active
    with _state_lock:
        noise_active = _state["noise_active"]
        noise_type = _state["noise_type"]
    if noise_active:
        if noise_type == "pagination_metadata":
            pagination = _pagination_metadata()
            body.update(pagination)
        elif noise_type == "variable_length_data":
            data_list = _variable_length_data()
            body.update(data_list)
        elif noise_type == "error_format_variation" and resp.status_code >= 400:
            error_body = _error_format_variation(resp.status_code)
            body = error_body
        elif noise_type == "cdn_cache_headers":
            cdn_headers = _cdn_cache_headers()
            for k, v in cdn_headers.items():
                resp.headers[k] = v

    resp.headers["X-Request-Id"] = _request_id()
    return resp


@app.route("/api/schema", methods=["GET"])
def get_schema():
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
            elif noise_type == "pagination_metadata":
                pagination = _pagination_metadata()
                schema.update(pagination)
            elif noise_type == "variable_length_data":
                data_list = _variable_length_data()
                schema.update(data_list)
            elif noise_type == "error_format_variation":
                # No effect on schema endpoint (error format variation only affects error responses)
                pass
            elif noise_type == "cdn_cache_headers":
                # No effect on schema endpoint body (headers added at response level)
                pass
        cache.put("schema", schema)
        schema["cache_status"] = "fresh"

    resp = make_response(jsonify(schema), 200)
    for hname, hval in resp_extra_headers.items():
        resp.headers[hname] = hval
    body_str = json.dumps(schema, sort_keys=True)
    etag = hashlib.sha256(body_str.encode()).hexdigest()[:16]
    resp.headers["ETag"] = f'"{etag}"'
    resp.headers["X-Request-Id"] = _request_id()
    
    # Apply CDN cache headers if active
    with _state_lock:
        noise_active = _state["noise_active"]
        noise_type = _state["noise_type"]
    if noise_active and noise_type == "cdn_cache_headers":
        cdn_headers = _cdn_cache_headers()
        for k, v in cdn_headers.items():
            resp.headers[k] = v
    
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