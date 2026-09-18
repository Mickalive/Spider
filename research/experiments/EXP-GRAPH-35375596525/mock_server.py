#!/usr/bin/env python3
"""
Stochastic Flask mock API server for EXP-GRAPH-35375596525.

Extends parent EXP-GRAPH-35353011131 with HTTP-level caching semantics:
1. SQLite DB-backed session/permission state (not in-memory dict)
2. In-memory cache with TTL-based expiry causing stale/fresh response alternation
3. Response timing jitter from real I/O operations (DB reads, cache lookups, JWT signing)
4. Mixed JWT algorithms: HS256 for read/write endpoints, RS256 for admin endpoints
5. NEW: HTTP-level caching semantics — Cache-Control, ETag, If-None-Match, 304 Not Modified

Two caching modes:
- Enabled: Cache-Control: max-age=5; ETag generated from response body SHA-256; If-None-Match; 304
- Disabled: Cache-Control: no-store; no ETag; no conditional requests
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


# ─── Configuration ─────────────────────────────────────────────────────────────

PORT = int(os.environ.get("MOCK_SERVER_PORT", "18930"))
SECRET_KEY = os.environ.get("MOCK_SERVER_SECRET", secrets.token_hex(32))
SESSION_DB_PATH = os.environ.get("MOCK_SERVER_DB", ":memory:")
SCHEMA_CACHE_TTL = float(os.environ.get("MOCK_SERVER_CACHE_TTL", "0.5"))  # seconds
JITTER_MIN_MS = int(os.environ.get("MOCK_SERVER_JITTER_MIN", "10"))
JITTER_MAX_MS = int(os.environ.get("MOCK_SERVER_JITTER_MAX", "100"))

os.makedirs("/tmp/flask_sessions_35375596525", exist_ok=True)


# ─── RSA Key Generation (for RS256 admin endpoints) ───────────────────────────

def generate_rsa_keys():
    """Generate RSA key pair for RS256 JWT algorithm."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


RSA_PRIVATE_KEY, RSA_PUBLIC_KEY = generate_rsa_keys()

# PEM encoding for JWT
RSA_PRIVATE_PEM = RSA_PRIVATE_KEY.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
RSA_PUBLIC_PEM = RSA_PUBLIC_KEY.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


# ─── SQLite Session/Permission Store ──────────────────────────────────────────

class SQLiteSessionStore:
    """SQLite-backed session and permission store with WAL-mode for concurrency."""
    
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self._local = threading.local()
        self._init_db()
    
    def _get_conn(self):
        """Get thread-local SQLite connection."""
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
        """Initialize database schema."""
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
        # Insert default permissions
        default_perms = {"read": 1, "write": 1, "admin": 1}
        for key, value in default_perms.items():
            conn.execute(
                "INSERT OR REPLACE INTO permissions (key, value) VALUES (?, ?)",
                (key, value)
            )
        conn.commit()
    
    def create_session(self, user_id="test_user"):
        """Create a new session in the database."""
        session_id = secrets.token_hex(16)
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO sessions (session_id, user_id, valid, created_at) VALUES (?, ?, 1, ?)",
            (session_id, user_id, time.time())
        )
        conn.commit()
        # Add jitter from real DB I/O
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
        return session_id
    
    def validate_session(self, session_id):
        """Validate session against database."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT valid FROM sessions WHERE session_id = ?",
            (session_id,)
        )
        row = cursor.fetchone()
        # Add jitter from real DB read
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
        return row is not None and row["valid"] == 1
    
    def invalidate_session(self, session_id):
        """Invalidate a session."""
        conn = self._get_conn()
        conn.execute(
            "UPDATE sessions SET valid = 0 WHERE session_id = ?",
            (session_id,)
        )
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
    
    def clear_all_sessions(self):
        """Clear all sessions (drift pattern: session_invalidation)."""
        conn = self._get_conn()
        conn.execute("UPDATE sessions SET valid = 0")
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
    
    def get_permissions(self):
        """Get current permissions from database."""
        conn = self._get_conn()
        cursor = conn.execute("SELECT key, value FROM permissions")
        perms = {row["key"]: bool(row["value"]) for row in cursor.fetchall()}
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
        return perms
    
    def set_permissions(self, permissions):
        """Set permissions in database."""
        conn = self._get_conn()
        for key, value in permissions.items():
            conn.execute(
                "INSERT OR REPLACE INTO permissions (key, value) VALUES (?, ?)",
                (key, int(value))
            )
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)


# ─── In-Memory Cache with TTL ────────────────────────────────────────────────

class SchemaCache:
    """In-memory cache with TTL-based expiry for /schema responses."""
    
    def __init__(self, ttl=0.5):
        self.ttl = ttl
        self._cache = {}
        self._lock = threading.Lock()
    
    def get(self, key):
        """Get cached value if not expired."""
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < self.ttl:
                    return value
                else:
                    del self._cache[key]
        return None
    
    def set(self, key, value):
        """Set cached value with current timestamp."""
        with self._lock:
            self._cache[key] = (value, time.time())
    
    def invalidate(self, key=None):
        """Invalidate cache entry or all entries."""
        with self._lock:
            if key:
                self._cache.pop(key, None)
            else:
                self._cache.clear()


# ─── HTTP Caching Helper ──────────────────────────────────────────────────────

def compute_etag(body_bytes):
    """Compute ETag from response body using SHA-256."""
    return hashlib.sha256(body_bytes).hexdigest()


def apply_http_caching(response, caching_enabled):
    """Apply HTTP caching headers to response based on caching mode."""
    if caching_enabled:
        # Cache-Control: max-age=5 seconds
        response.headers["Cache-Control"] = "max-age=5"
        # Vary header for content negotiation
        response.headers["Vary"] = "Accept, Authorization"
    else:
        # Cache-Control: no-store — no caching at all
        response.headers["Cache-Control"] = "no-store"
    return response


# ─── Flask App Setup ──────────────────────────────────────────────────────────

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

# Global server state
server_state = {
    "signing_key": SECRET_KEY,
    "permissions": {"read": True, "write": True, "admin": True},
    "schema_fields": [],
    "schema_size": 10,
    "noise_pattern": None,
    "drift_pattern": None,
    "co_occurring": False,
    "seed": 42,
    "caching_enabled": True,  # NEW: HTTP caching mode
}

# Stochastic stores
session_store = SQLiteSessionStore(SESSION_DB_PATH)
schema_cache = SchemaCache(ttl=SCHEMA_CACHE_TTL)


# ─── Schema Generation ────────────────────────────────────────────────────────

def generate_schema(n_fields, seed=42):
    """Generate a deterministic API response schema with n_fields."""
    rng = random.Random(seed)
    fields = []
    for i in range(n_fields):
        field_name = f"field_{i:03d}"
        field_type = rng.choice(["string", "integer", "boolean", "array"])
        fields.append({
            "name": field_name,
            "type": field_type,
            "description": f"Description for {field_name}",
            "required": i < max(1, n_fields // 3)
        })
    return fields


def apply_noise_to_schema(schema, noise_pattern, schema_size, rng):
    """Apply structural noise pattern to schema."""
    schema = copy.deepcopy(schema)
    if noise_pattern == "optional_field_addition":
        n_new = rng.randint(1, max(1, schema_size // 5))
        for i in range(n_new):
            schema.append({
                "name": f"new_optional_{i}",
                "type": "string",
                "description": f"New optional field {i}",
                "required": False
            })
    elif noise_pattern == "description_change":
        for field in schema:
            field["description"] = field["description"] + " (updated)"
    elif noise_pattern == "response_time_jitter":
        pass  # Handled at response level
    elif noise_pattern == "field_type_normalization":
        for field in schema:
            if field["type"] == "integer":
                field["type"] = "string"
            elif field["type"] == "boolean":
                field["type"] = "integer"
    return schema


def generate_response_data(schema, seed=42):
    """Generate response data matching the schema."""
    rng = random.Random(seed)
    data = {}
    for field in schema:
        name = field["name"]
        ftype = field["type"]
        if ftype == "string":
            data[name] = rng.choice([f"value_{i}" for i in range(100)])
        elif ftype == "integer":
            data[name] = int(rng.randint(0, 1000))
        elif ftype == "boolean":
            data[name] = bool(rng.randint(0, 2))
        elif ftype == "array":
            data[name] = [rng.choice([f"item_{i}" for i in range(10)]) for _ in range(rng.randint(1, 5))]
    return data


# ─── JWT Helpers (Mixed Algorithms) ──────────────────────────────────────────

def create_token(user_id="test_user", permissions=None, expiry_hours=1, signing_key=None, algorithm=None):
    """Create a JWT token with given parameters.
    
    Uses HS256 for read/write endpoints, RS256 for admin endpoints.
    """
    if permissions is None:
        permissions = server_state["permissions"]
    
    # Determine algorithm based on endpoint type
    if algorithm is None:
        algorithm = "HS256"  # Default for most endpoints
    
    payload = {
        "sub": user_id,
        "permissions": permissions,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=expiry_hours)
    }
    
    if algorithm == "RS256":
        return jwt.encode(payload, RSA_PRIVATE_PEM, algorithm="RS256")
    else:
        key = signing_key or server_state["signing_key"]
        return jwt.encode(payload, key, algorithm="HS256")


def validate_token(token, signing_key=None):
    """Validate a JWT token against the given signing key.
    
    Tries HS256 first, then RS256 for admin endpoints.
    """
    # Try HS256 first
    try:
        key = signing_key or server_state["signing_key"]
        payload = jwt.decode(token, key, algorithms=["HS256"])
        return True, payload
    except jwt.InvalidSignatureError:
        pass
    except jwt.ExpiredSignatureError:
        return False, {"error": "Token expired"}
    except jwt.DecodeError:
        pass
    
    # Try RS256
    try:
        payload = jwt.decode(token, RSA_PUBLIC_PEM, algorithms=["RS256"])
        return True, payload
    except jwt.InvalidSignatureError:
        return False, {"error": "Invalid signature"}
    except jwt.ExpiredSignatureError:
        return False, {"error": "Token expired"}
    except jwt.DecodeError as e:
        return False, {"error": f"Decode error: {str(e)}"}
    
    return False, {"error": "No valid algorithm matched"}


# ─── Auth Decorators ──────────────────────────────────────────────────────────

def require_token(f):
    """Decorator to require valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = auth_header[7:]
        is_valid, payload = validate_token(token)
        if not is_valid:
            return jsonify({"error": "Invalid token", "detail": payload.get("error")}), 401
        request.token_payload = payload
        return f(*args, **kwargs)
    return decorated


def require_permission(permission):
    """Decorator to require specific permission."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            perms = session_store.get_permissions()
            if not perms.get(permission, False):
                return jsonify({"error": f"Permission denied: {permission}"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "server_state": {
        "drift_pattern": server_state["drift_pattern"],
        "noise_pattern": server_state["noise_pattern"],
        "co_occurring": server_state["co_occurring"],
        "schema_size": server_state["schema_size"],
        "jwt_algorithms": ["HS256", "RS256"],
        "caching_enabled": server_state["caching_enabled"],
    }})


@app.route("/schema", methods=["GET"])
def get_schema():
    """UNAUTHENTICATED endpoint returning current schema.
    Uses cache with TTL for stale/fresh alternation.
    This is the structural probe independent of auth state.
    
    NEW: Supports HTTP caching semantics (Cache-Control, ETag, If-None-Match, 304).
    """
    cache_key = f"schema_{server_state['schema_size']}_{server_state['seed']}_{server_state['noise_pattern']}"
    
    # Try cache first (with TTL expiry)
    cached = schema_cache.get(cache_key)
    if cached is not None:
        schema_data = cached
        is_cached = True
    else:
        # Cache miss - compute from DB (with real I/O jitter)
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
        schema_data = server_state["schema_fields"]
        schema_cache.set(cache_key, schema_data)
        is_cached = False
    
    # Build response body
    body = jsonify({"fields": schema_data, "size": len(schema_data), "cached": is_cached})
    
    # Compute ETag from body bytes (content-only hash, excluding timing headers)
    body_bytes = json.dumps({"fields": schema_data, "size": len(schema_data), "cached": is_cached}, sort_keys=True).encode()
    etag = compute_etag(body_bytes)
    
    # Check If-None-Match conditional request
    if_none_match = request.headers.get("If-None-Match")
    if server_state["caching_enabled"] and if_none_match and if_none_match == etag:
        # Return 304 Not Modified (no body)
        response = make_response("", 304)
        response = apply_http_caching(response, server_state["caching_enabled"])
        response.headers["ETag"] = etag
        return response
    
    # Apply HTTP caching headers
    response = apply_http_caching(body, server_state["caching_enabled"])
    
    # Set ETag header (always, for both caching modes)
    response.headers["ETag"] = etag
    
    return response


@app.route("/token", methods=["POST"])
def issue_token():
    """Issue a new JWT token.
    Uses HS256 for standard tokens, RS256 for admin tokens."""
    data = request.get_json() or {}
    user_id = data.get("user_id", "test_user")
    permissions = data.get("permissions", session_store.get_permissions())
    expiry_hours = data.get("expiry_hours", 1)
    
    # Use RS256 for admin tokens, HS256 for others
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
    """Read endpoint - requires read permission. Uses HS256 token."""
    schema = server_state["schema_fields"]
    data = generate_response_data(schema)
    time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
    return jsonify(data)


@app.route("/api/write", methods=["POST"])
@require_token
@require_permission("write")
def api_write():
    """Write endpoint - requires write permission. Uses HS256 token."""
    schema = server_state["schema_fields"]
    data = generate_response_data(schema)
    data["write_status"] = "success"
    time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
    return jsonify(data)


@app.route("/api/admin", methods=["GET"])
@require_token
@require_permission("admin")
def api_admin():
    """Admin endpoint - requires admin permission. Uses RS256 token."""
    schema = server_state["schema_fields"]
    data = generate_response_data(schema)
    data["admin_data"] = "classified"
    time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
    return jsonify(data)


@app.route("/session/status", methods=["GET"])
def session_status():
    """Check session status.
    Returns randomly chosen status code from {401, 403, 500}
    when session is invalid (same as parent for graded session_status_check).
    """
    session_id = request.cookies.get("session_id") or request.headers.get("X-Session-ID")
    if not session_id:
        session_id = secrets.token_hex(16)
    
    is_valid = session_store.validate_session(session_id)
    if is_valid:
        return jsonify({"session_id": session_id, "valid": True}), 200
    else:
        # Randomly choose from {401, 403, 500} for graded session_status_check
        status_code = random.choice([401, 403, 500])
        return jsonify({"session_id": session_id, "valid": False}), status_code


@app.route("/session/invalidate", methods=["POST"])
def invalidate_session_endpoint():
    """Invalidate current session."""
    session_id = request.cookies.get("session_id") or request.headers.get("X-Session-ID")
    session_store.invalidate_session(session_id)
    response = jsonify({"status": "invalidated"})
    response.set_cookie("session_id", "", expires=0)
    return response


@app.route("/admin/set_drift", methods=["POST"])
def set_drift():
    """Set drift pattern and apply its effects immediately."""
    data = request.get_json() or {}
    pattern = data.get("pattern")
    server_state["drift_pattern"] = pattern
    server_state["co_occurring"] = data.get("co_occurring", False)

    if pattern == "session_invalidation":
        session_store.clear_all_sessions()
    elif pattern == "permission_boundary":
        pass  # Handled via /admin/set_permissions

    if "schema_size" in data:
        server_state["schema_size"] = data["schema_size"]
        server_state["schema_fields"] = generate_schema(data["schema_size"])
        schema_cache.invalidate()  # Invalidate cache on schema change

    return jsonify({"status": "drift_set", "drift_pattern": server_state["drift_pattern"]})


@app.route("/admin/set_noise", methods=["POST"])
def set_noise():
    """Set noise pattern."""
    data = request.get_json() or {}
    server_state["noise_pattern"] = data.get("pattern")
    if server_state["noise_pattern"] and server_state["schema_fields"]:
        rng = random.Random(server_state["seed"])
        server_state["schema_fields"] = apply_noise_to_schema(
            generate_schema(server_state["schema_size"], server_state["seed"]),
            server_state["noise_pattern"],
            server_state["schema_size"],
            rng
        )
        schema_cache.invalidate()  # Invalidate cache on noise change
    return jsonify({"status": "noise_set", "noise_pattern": server_state["noise_pattern"]})


@app.route("/admin/set_caching", methods=["POST"])
def set_caching():
    """Set HTTP caching mode (enabled/disabled)."""
    data = request.get_json() or {}
    server_state["caching_enabled"] = data.get("enabled", True)
    return jsonify({
        "status": "caching_set",
        "caching_enabled": server_state["caching_enabled"]
    })


@app.route("/admin/reset", methods=["POST"])
def reset_server():
    """Reset server to baseline state."""
    server_state["drift_pattern"] = None
    server_state["noise_pattern"] = None
    server_state["co_occurring"] = False
    server_state["signing_key"] = SECRET_KEY
    server_state["permissions"] = {"read": True, "write": True, "admin": True}
    server_state["schema_fields"] = generate_schema(server_state["schema_size"], server_state["seed"])
    session_store.clear_all_sessions()
    schema_cache.invalidate()
    return jsonify({"status": "reset"})


@app.route("/admin/set_permissions", methods=["POST"])
def set_permissions():
    """Set permissions (drift pattern: permission_boundary)."""
    data = request.get_json() or {}
    perms = data.get("permissions", {"read": True, "write": True, "admin": True})
    session_store.set_permissions(perms)
    return jsonify({"status": "permissions_set", "permissions": perms})


@app.route("/admin/set_seed", methods=["POST"])
def set_seed():
    """Set RNG seed for reproducibility."""
    data = request.get_json() or {}
    server_state["seed"] = data.get("seed", 42)
    return jsonify({"status": "seed_set", "seed": server_state["seed"]})


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stochastic Mock API server for EXP-GRAPH-35375596525")
    parser.add_argument("--port", type=int, default=PORT, help="Port to run on")
    parser.add_argument("--schema-size", type=int, default=10, help="Schema size")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--db-path", type=str, default=SESSION_DB_PATH, help="SQLite DB path")
    parser.add_argument("--cache-ttl", type=float, default=SCHEMA_CACHE_TTL, help="Schema cache TTL in seconds")
    parser.add_argument("--caching-enabled", action="store_true", default=True, help="Enable HTTP caching")
    parser.add_argument("--caching-disabled", action="store_true", default=False, help="Disable HTTP caching")
    args = parser.parse_args()

    server_state["schema_size"] = args.schema_size
    server_state["seed"] = args.seed
    server_state["schema_fields"] = generate_schema(args.schema_size, args.seed)
    server_state["caching_enabled"] = not args.caching_disabled

    # Reinitialize session store with specified DB path (module-level mutable object)
    session_store.__init__(args.db_path)
    schema_cache.ttl = args.cache_ttl

    print(f"Starting stochastic mock server on port {args.port}")
    print(f"  schema_size={args.schema_size}, seed={args.seed}")
    print(f"  DB path={args.db_path}, cache TTL={args.cache_ttl}s")
    print(f"  JWT algorithms: HS256 (read/write), RS256 (admin)")
    print(f"  Jitter range: {JITTER_MIN_MS}-{JITTER_MAX_MS}ms")
    print(f"  HTTP caching: {'enabled' if server_state['caching_enabled'] else 'disabled'}")

    app.run(host="127.0.0.1", port=args.port, debug=False, threaded=True)
