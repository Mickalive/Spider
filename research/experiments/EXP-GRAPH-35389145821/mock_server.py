#!/usr/bin/env python3
"""
Stochastic Flask mock API server for EXP-GRAPH-35389145821.

Extends EXP-GRAPH-35375596525 with operational HTTP conditional caching:
1. Client sends If-None-Match header with ETag from prior /schema response
2. Server returns 304 Not Modified when ETag matches
3. 304 response rate logged as manipulation check
4. Cache hit rate, ETag match rate, I/O latency distribution logged

Same stochastic base as parent:
- Flask 3.1.3, SQLite WAL-mode, in-memory cache TTL=0.5s, jitter 10-100ms
- Mixed JWT: HS256 (read/write), RS256 (admin)
- HTTP caching: Cache-Control, ETag, If-None-Match, 304 Not Modified
"""

import os
import sys
import json
import time
import secrets
import threading
import argparse
import random
import copy
import sqlite3
import tempfile
import hashlib
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Flask, request, jsonify, session, make_response
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


# ─── Configuration ─────────────────────────────────────────────────────

PORT = int(os.environ.get("MOCK_SERVER_PORT", "18930"))
SECRET_KEY = os.environ.get("MOCK_SERVER_SECRET", secrets.token_hex(32))
SESSION_DB_PATH = os.environ.get("MOCK_SERVER_DB", ":memory:")
SCHEMA_CACHE_TTL = float(os.environ.get("MOCK_SERVER_CACHE_TTL", "0.5"))
JITTER_MIN_MS = int(os.environ.get("MOCK_SERVER_JITTER_MIN", "1"))
JITTER_MAX_MS = int(os.environ.get("MOCK_SERVER_JITTER_MAX", "5"))

os.makedirs("/tmp/flask_sessions_35389145821", exist_ok=True)


# ─── RSA Key Generation ──────────────────────────────────────────────

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

RSA_PRIVATE_KEY, RSA_PUBLIC_KEY = generate_rsa_keys()
RSA_PRIVATE_PEM = RSA_PRIVATE_KEY.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
RSA_PUBLIC_PEM = RSA_PUBLIC_KEY.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


# ─── SQLite Session/Permission Store ────────────────────────────────

class SQLiteSessionStore:
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self._local = threading.local()
        self._init_db()

    def _get_conn(self):
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            if self.db_path == ":memory:":
                self._local.conn = sqlite3.connect(":memory:")
            else:
                self._local.conn = sqlite3.connect(self.db_path, timeout=10)
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA busy_timeout=5000")
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    def _init_db(self):
        conn = self._get_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                valid INTEGER NOT NULL DEFAULT 1,
                created_at REAL NOT NULL,
                data TEXT DEFAULT '{}'
            );
            CREATE TABLE IF NOT EXISTS permissions (
                key TEXT PRIMARY KEY,
                value INTEGER NOT NULL
            );
        """)
        default_perms = {"read": 1, "write": 1, "admin": 1}
        for key, value in default_perms.items():
            conn.execute("INSERT OR REPLACE INTO permissions (key, value) VALUES (?, ?)", (key, value))
        conn.commit()

    def create_session(self, user_id="test_user"):
        session_id = secrets.token_hex(16)
        conn = self._get_conn()
        conn.execute("INSERT INTO sessions (session_id, user_id, valid, created_at) VALUES (?, ?, 1, ?)",
                     (session_id, user_id, time.time()))
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
        return session_id

    def validate_session(self, session_id):
        conn = self._get_conn()
        cursor = conn.execute("SELECT valid FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
        return row is not None and row["valid"] == 1

    def invalidate_session(self, session_id):
        conn = self._get_conn()
        conn.execute("UPDATE sessions SET valid = 0 WHERE session_id = ?", (session_id,))
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)

    def clear_all_sessions(self):
        conn = self._get_conn()
        conn.execute("UPDATE sessions SET valid = 0")
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)

    def get_permissions(self):
        conn = self._get_conn()
        cursor = conn.execute("SELECT key, value FROM permissions")
        perms = {row["key"]: bool(row["value"]) for row in cursor.fetchall()}
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
        return perms

    def set_permissions(self, permissions):
        conn = self._get_conn()
        for key, value in permissions.items():
            conn.execute("INSERT OR REPLACE INTO permissions (key, value) VALUES (?, ?)", (key, int(value)))
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)


# ─── In-Memory Cache with TTL ──────────────────────────────────────

class SchemaCache:
    def __init__(self, ttl=0.5):
        self.ttl = ttl
        self._cache = {}
        self._lock = threading.Lock()

    def get(self, key):
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < self.ttl:
                    return value
                else:
                    del self._cache[key]
        return None

    def set(self, key, value):
        with self._lock:
            self._cache[key] = (value, time.time())

    def invalidate(self, key=None):
        with self._lock:
            if key:
                self._cache.pop(key, None)
            else:
                self._cache.clear()


# ─── HTTP Caching Helper ────────────────────────────────────────────

def compute_etag(body_bytes):
    return hashlib.sha256(body_bytes).hexdigest()


def apply_http_caching(response, caching_enabled):
    if caching_enabled:
        response.headers["Cache-Control"] = "max-age=5"
        response.headers["Vary"] = "Accept, Authorization"
    else:
        response.headers["Cache-Control"] = "no-store"
    return response


# ─── Flask App Setup ────────────────────────────────────────────────

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

server_state = {
    "signing_key": SECRET_KEY,
    "permissions": {"read": True, "write": True, "admin": True},
    "schema_fields": [],
    "schema_size": 10,
    "noise_pattern": None,
    "drift_pattern": None,
    "co_occurring": False,
    "seed": 42,
    "caching_enabled": True,
    # Manipulation check logging
    "request_log": [],
}

session_store = SQLiteSessionStore(SESSION_DB_PATH)
schema_cache = SchemaCache(ttl=SCHEMA_CACHE_TTL)


# ─── Schema Generation ──────────────────────────────────────────────

def generate_schema(n_fields, seed=42):
    rng = random.Random(seed)
    fields = []
    for i in range(n_fields):
        field_name = f"field_{i:03d}"
        field_type = rng.choice(["string", "integer", "boolean", "array"])
        fields.append({
            "name": field_name, "type": field_type,
            "description": f"Description for {field_name}",
            "required": i < max(1, n_fields // 3)
        })
    return fields


def apply_noise_to_schema(schema, noise_pattern, schema_size, rng):
    schema = copy.deepcopy(schema)
    if noise_pattern == "optional_field_addition":
        n_new = rng.randint(1, max(1, schema_size // 5))
        for i in range(n_new):
            schema.append({"name": f"new_optional_{i}", "type": "string", "description": f"New optional field {i}", "required": False})
    elif noise_pattern == "description_change":
        for field in schema:
            field["description"] = field["description"] + " (updated)"
    elif noise_pattern == "response_time_jitter":
        pass
    elif noise_pattern == "field_type_normalization":
        for field in schema:
            if field["type"] == "integer": field["type"] = "string"
            elif field["type"] == "boolean": field["type"] = "integer"
    return schema


def generate_response_data(schema, seed=42):
    rng = random.Random(seed)
    data = {}
    for field in schema:
        name = field["name"]
        ftype = field["type"]
        if ftype == "string": data[name] = rng.choice([f"value_{i}" for i in range(100)])
        elif ftype == "integer": data[name] = int(rng.randint(0, 1000))
        elif ftype == "boolean": data[name] = bool(rng.randint(0, 2))
        elif ftype == "array": data[name] = [rng.choice([f"item_{i}" for i in range(10)]) for _ in range(rng.randint(1, 5))]
    return data


# ─── JWT Helpers ────────────────────────────────────────────────────

def create_token(user_id="test_user", permissions=None, expiry_hours=1, signing_key=None, algorithm=None):
    if permissions is None: permissions = server_state["permissions"]
    if algorithm is None: algorithm = "HS256"
    payload = {"sub": user_id, "permissions": permissions, "iat": datetime.now(timezone.utc), "exp": datetime.now(timezone.utc) + timedelta(hours=expiry_hours)}
    if algorithm == "RS256": return jwt.encode(payload, RSA_PRIVATE_PEM, algorithm="RS256")
    else: return jwt.encode(payload, signing_key or server_state["signing_key"], algorithm="HS256")


def validate_token(token, signing_key=None):
    try:
        payload = jwt.decode(token, signing_key or server_state["signing_key"], algorithms=["HS256"])
        return True, payload
    except jwt.InvalidSignatureError: pass
    except jwt.ExpiredSignatureError: return False, {"error": "Token expired"}
    except jwt.DecodeError: pass
    try:
        payload = jwt.decode(token, RSA_PUBLIC_PEM, algorithms=["RS256"])
        return True, payload
    except jwt.InvalidSignatureError: return False, {"error": "Invalid signature"}
    except jwt.ExpiredSignatureError: return False, {"error": "Token expired"}
    except jwt.DecodeError as e: return False, {"error": f"Decode error: {str(e)}"}
    return False, {"error": "No valid algorithm matched"}


# ─── Auth Decorators ────────────────────────────────────────────────

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "): return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = auth_header[7:]
        is_valid, payload = validate_token(token)
        if not is_valid: return jsonify({"error": "Invalid token", "detail": payload.get("error")}), 401
        request.token_payload = payload
        return f(*args, **kwargs)
    return decorated

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            perms = session_store.get_permissions()
            if not perms.get(permission, False): return jsonify({"error": f"Permission denied: {permission}"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


# ─── Routes ──────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "server_state": {
        "drift_pattern": server_state["drift_pattern"], "noise_pattern": server_state["noise_pattern"],
        "co_occurring": server_state["co_occurring"], "schema_size": server_state["schema_size"],
        "jwt_algorithms": ["HS256", "RS256"], "caching_enabled": server_state["caching_enabled"],
    }})


@app.route("/schema", methods=["GET"])
def get_schema():
    """UNAUTHENTICATED endpoint returning current schema with HTTP caching."""
    cache_key = f"schema_{server_state['schema_size']}_{server_state['seed']}_{server_state['noise_pattern']}"
    
    # Try cache first (with TTL expiry)
    cached = schema_cache.get(cache_key)
    if cached is not None:
        schema_data = cached
        is_cached = True
    else:
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
        schema_data = server_state["schema_fields"]
        schema_cache.set(cache_key, schema_data)
        is_cached = False
    
    # Compute ETag from schema data only (EXCLUDING cached flag for stable ETags)
    schema_body = {"fields": schema_data, "size": len(schema_data)}
    body_bytes = json.dumps(schema_body, sort_keys=True).encode()
    etag = compute_etag(body_bytes)
    
    body_data = {"fields": schema_data, "size": len(schema_data), "cached": is_cached}
    body = jsonify(body_data)
    
    # Check If-None-Match conditional request (NEW: operational 304)
    if_none_match = request.headers.get("If-None-Match")
    is_304 = False
    if server_state["caching_enabled"] and if_none_match and if_none_match == etag:
        is_304 = True
        response = make_response("", 304)
        response = apply_http_caching(response, server_state["caching_enabled"])
        response.headers["ETag"] = etag
        # Log the 304 response
        server_state["request_log"].append({
            "path": "/schema", "response_type": "304", "etag": etag,
            "if_none_match": if_none_match, "timestamp": time.time()
        })
        return response
    
    # Normal response
    response = apply_http_caching(body, server_state["caching_enabled"])
    response.headers["ETag"] = etag
    
    # Log the 200 response
    server_state["request_log"].append({
        "path": "/schema", "response_type": "200", "etag": etag,
        "if_none_match": if_none_match, "cached": is_cached, "timestamp": time.time()
    })
    
    return response


@app.route("/token", methods=["POST"])
def issue_token():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id", "test_user")
    permissions = data.get("permissions", session_store.get_permissions())
    expiry_hours = data.get("expiry_hours", 1)
    is_admin = permissions.get("admin", False)
    algorithm = "RS256" if is_admin else "HS256"
    token = create_token(user_id, permissions, expiry_hours, algorithm=algorithm)
    session_id = session_store.create_session(user_id)
    response = jsonify({"token": token, "session_id": session_id})
    response.set_cookie("session_id", session_id, httponly=True, secure=False)
    return response


@app.route("/api/read", methods=["GET"])
@require_token
@require_permission("read")
def api_read():
    schema = server_state["schema_fields"]
    data = generate_response_data(schema)
    time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
    return jsonify(data)


@app.route("/api/write", methods=["POST"])
@require_token
@require_permission("write")
def api_write():
    schema = server_state["schema_fields"]
    data = generate_response_data(schema)
    data["write_status"] = "success"
    time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
    return jsonify(data)


@app.route("/api/admin", methods=["GET"])
@require_token
@require_permission("admin")
def api_admin():
    schema = server_state["schema_fields"]
    data = generate_response_data(schema)
    data["admin_data"] = "classified"
    time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
    return jsonify(data)


@app.route("/session/status", methods=["GET"])
def session_status():
    session_id = request.cookies.get("session_id") or request.headers.get("X-Session-ID")
    if not session_id: session_id = secrets.token_hex(16)
    is_valid = session_store.validate_session(session_id)
    if is_valid: return jsonify({"session_id": session_id, "valid": True}), 200
    else:
        status_code = random.choice([401, 403, 500])
        return jsonify({"session_id": session_id, "valid": False}), status_code


@app.route("/session/invalidate", methods=["POST"])
def invalidate_session_endpoint():
    session_id = request.cookies.get("session_id") or request.headers.get("X-Session-ID")
    session_store.invalidate_session(session_id)
    response = jsonify({"status": "invalidated"})
    response.set_cookie("session_id", "", expires=0)
    return response


@app.route("/admin/set_drift", methods=["POST"])
def set_drift():
    data = request.get_json(silent=True) or {}
    server_state["drift_pattern"] = data.get("pattern")
    server_state["co_occurring"] = data.get("co_occurring", False)
    if data.get("pattern") == "session_invalidation": session_store.clear_all_sessions()
    if "schema_size" in data:
        server_state["schema_size"] = data["schema_size"]
        server_state["schema_fields"] = generate_schema(data["schema_size"], server_state["seed"])
        schema_cache.invalidate()
    return jsonify({"status": "drift_set", "drift_pattern": server_state["drift_pattern"]})


@app.route("/admin/set_noise", methods=["POST"])
def set_noise():
    data = request.get_json(silent=True) or {}
    server_state["noise_pattern"] = data.get("pattern")
    if server_state["noise_pattern"] and server_state["schema_fields"]:
        rng = random.Random(server_state["seed"])
        server_state["schema_fields"] = apply_noise_to_schema(
            generate_schema(server_state["schema_size"], server_state["seed"]),
            server_state["noise_pattern"], server_state["schema_size"], rng)
        schema_cache.invalidate()
    return jsonify({"status": "noise_set", "noise_pattern": server_state["noise_pattern"]})


@app.route("/admin/set_caching", methods=["POST"])
def set_caching():
    data = request.get_json(silent=True) or {}
    server_state["caching_enabled"] = data.get("enabled", True)
    return jsonify({"status": "caching_set", "caching_enabled": server_state["caching_enabled"]})


@app.route("/admin/reset", methods=["POST"])
def reset_server():
    server_state["drift_pattern"] = None
    server_state["noise_pattern"] = None
    server_state["co_occurring"] = False
    server_state["signing_key"] = SECRET_KEY
    server_state["permissions"] = {"read": True, "write": True, "admin": True}
    server_state["schema_fields"] = generate_schema(server_state["schema_size"], server_state["seed"])
    session_store.clear_all_sessions()
    schema_cache.invalidate()
    server_state["request_log"] = []
    return jsonify({"status": "reset"})


@app.route("/admin/set_permissions", methods=["POST"])
def set_permissions():
    """Set permissions (drift pattern: permission_boundary)."""
    data = request.get_json(silent=True) or {}
    perms = data.get("permissions", {"read": True, "write": True, "admin": True})
    session_store.set_permissions(perms)
    return jsonify({"status": "permissions_set", "permissions": perms})


@app.route("/admin/get_request_log", methods=["GET"])
def get_request_log():
    return jsonify(server_state["request_log"])


@app.route("/admin/set_seed", methods=["POST"])
def set_seed():
    data = request.get_json(silent=True) or {}
    server_state["seed"] = data.get("seed", 42)
    return jsonify({"status": "seed_set", "seed": server_state["seed"]})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stochastic Mock API server for EXP-GRAPH-35389145821")
    parser.add_argument("--port", type=int, default=PORT, help="Port to run on")
    parser.add_argument("--schema-size", type=int, default=10, help="Schema size")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--db-path", type=str, default=SESSION_DB_PATH, help="SQLite DB path")
    parser.add_argument("--cache-ttl", type=float, default=SCHEMA_CACHE_TTL, help="Schema cache TTL")
    parser.add_argument("--caching-enabled", action="store_true", default=True, help="Enable HTTP caching")
    parser.add_argument("--caching-disabled", action="store_true", default=False, help="Disable HTTP caching")
    args = parser.parse_args()

    server_state["schema_size"] = args.schema_size
    server_state["seed"] = args.seed
    server_state["schema_fields"] = generate_schema(args.schema_size, args.seed)
    server_state["caching_enabled"] = not args.caching_disabled
    session_store.__init__(args.db_path)
    schema_cache.ttl = args.cache_ttl

    print(f"Starting stochastic mock server on port {args.port}")
    print(f"  schema_size={args.schema_size}, seed={args.seed}")
    print(f"  HTTP caching: {'enabled' if server_state['caching_enabled'] else 'disabled'}")
    app.run(host="127.0.0.1", port=args.port, debug=False, threaded=True)
