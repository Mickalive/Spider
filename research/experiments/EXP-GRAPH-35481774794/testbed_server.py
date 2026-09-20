#!/usr/bin/env python3
"""
Production-like testbed server for EXP-GRAPH-35481774794.

CORRECTED from EXP-GRAPH-35476270792:
- V1 FIX: ALL responses use uuid.uuid4() for request_id (no token_hex).
- V_ETAG_PERMISSION_LEAKAGE FIX: permission_level derived from JWT payload
  BEFORE token validation, so write-permission expired requests get write-etag.
  This ensures ETag is independent of token expiry state.

Structural signal extraction: headers-only (ETag, Cache-Control,
UUID-based dynamic content hash), excluding error response bodies.

3 endpoints, 8 co-occurring conditions: token_state x cache_mode x permission_level.
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
import hashlib
import uuid
import math
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path
from collections import Counter

from flask import Flask, request, jsonify, session, make_response, g
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# ─── Configuration ─────────────────────────────────────────────

PORT = int(os.environ.get("TESTBED_PORT", "18970"))
SECRET_KEY = os.environ.get("TESTBED_SECRET", secrets.token_hex(32))
SESSION_DB_PATH = os.environ.get("TESTBED_DB", "/tmp/testbed_sessions_35481774794.db")
os.makedirs("/tmp/testbed_sessions_35481774794", exist_ok=True)
JITTER_MIN_MS = int(os.environ.get("TESTBED_JITTER_MIN", "10"))
JITTER_MAX_MS = int(os.environ.get("TESTBED_JITTER_MAX", "500"))
CACHE_MAX_AGE = int(os.environ.get("TESTBED_CACHE_MAX_AGE", "30"))
SERVER_SEED = int(os.environ.get("TESTBED_SEED", "42"))

# ─── RSA Key Generation ──────────────────────────────────────

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

# ─── SQLite Session/Permission Store ────────────────────────

class SQLiteSessionStore:
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self._local = threading.local()
        self._init_db()

    def _get_conn(self):
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            if self.db_path == ":memory:":
                self._local.conn = sqlite3.connect(":memory:", check_same_thread=False)
            else:
                self._local.conn = sqlite3.connect(self.db_path, timeout=10)
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA busy_timeout=5000")
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA wal_autocheckpoint=1000")
        return self._local.conn

    def _init_db(self):
        conn = self._get_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                valid INTEGER NOT NULL DEFAULT 1,
                created_at REAL NOT NULL,
                permission_level TEXT DEFAULT 'read',
                data TEXT DEFAULT '{}'
            );
            CREATE TABLE IF NOT EXISTS permissions (
                key TEXT PRIMARY KEY,
                value INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS response_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT,
                request_id TEXT,
                timestamp REAL,
                session_id TEXT,
                response_hash TEXT,
                cache_hit INTEGER DEFAULT 0
            );
        """)
        default_perms = {"read": 1, "write": 1, "admin": 0}
        for key, value in default_perms.items():
            conn.execute("INSERT OR REPLACE INTO permissions (key, value) VALUES (?, ?)", (key, value))
        conn.commit()

    def create_session(self, user_id="test_user", permission_level="read"):
        session_id = secrets.token_hex(16)
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO sessions (session_id, user_id, valid, created_at, permission_level) VALUES (?, ?, 1, ?, ?)",
            (session_id, user_id, time.time(), permission_level)
        )
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
        return session_id

    def validate_session(self, session_id):
        conn = self._get_conn()
        cursor = conn.execute("SELECT valid, permission_level FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)
        if row is None: return False, "read"
        return row["valid"] == 1, row["permission_level"]

    def invalidate_session(self, session_id):
        conn = self._get_conn()
        conn.execute("UPDATE sessions SET valid = 0 WHERE session_id = ?", (session_id,))
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)

    def set_permission(self, session_id, level):
        conn = self._get_conn()
        conn.execute("UPDATE sessions SET permission_level = ? WHERE session_id = ?", (level, session_id))
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)

    def set_permissions(self, permissions):
        conn = self._get_conn()
        for key, value in permissions.items():
            conn.execute("INSERT OR REPLACE INTO permissions (key, value) VALUES (?, ?)", (key, int(value)))
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)

    def clear_all_sessions(self):
        conn = self._get_conn()
        conn.execute("UPDATE sessions SET valid = 0")
        conn.commit()
        time.sleep(random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)

    def log_response(self, endpoint, request_id, response_hash, session_id="", cache_hit=0):
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO response_log (endpoint, request_id, timestamp, session_id, response_hash, cache_hit) VALUES (?, ?, ?, ?, ?, ?)",
            (endpoint, request_id, time.time(), session_id, response_hash, cache_hit)
        )
        conn.commit()

    def get_response_log(self):
        conn = self._get_conn()
        cursor = conn.execute("SELECT * FROM response_log ORDER BY id DESC LIMIT 1000")
        rows = [dict(r) for r in cursor.fetchall()]
        return rows


# ─── In-Memory Cache with TTL (CDN simulation) ──────────────

class CDNCache:
    def __init__(self, max_age=30):
        self.max_age = max_age
        self._cache = {}
        self._lock = threading.Lock()
        self._stats = {"hits": 0, "misses": 0, "invalidations": 0}

    def get(self, key):
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < self.max_age:
                    self._stats["hits"] += 1
                    return value, True
                else:
                    del self._cache[key]
            self._stats["misses"] += 1
            return None, False

    def set(self, key, value):
        with self._lock:
            self._cache[key] = (value, time.time())

    def invalidate(self, key=None):
        with self._lock:
            if key:
                self._cache.pop(key, None)
            else:
                self._cache.clear()
            self._stats["invalidations"] += 1

    def get_stats(self):
        with self._lock:
            return dict(self._stats)


# ─── HTTP Caching Helper ────────────────────────────────────

def apply_cache_headers(response, cache_enabled, max_age=30, no_store=False):
    if no_store or not cache_enabled:
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"
    else:
        response.headers["Cache-Control"] = f"max-age={max_age}, stale-while-revalidate=10"
        response.headers["Vary"] = "Accept, Authorization"
    return response


# ─── Flask App Setup ────────────────────────────────────────

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

server_state = {
    "seed": SERVER_SEED,
    "cache_enabled": True,
    "caching_max_age": CACHE_MAX_AGE,
    "permissions": {"read": True, "write": False, "admin": False},
    "user_profiles": {},
    "request_counter": 0,
}

session_store = SQLiteSessionStore(SESSION_DB_PATH)
cdn_cache = CDNCache(max_age=CACHE_MAX_AGE)

# ─── Dynamic Content Generation ───────────────────────────────

def generate_user_profile(user_id, permission_level, rng):
    base_profiles = {
        "alice": {"name": "Alice", "role": "analyst", "department": "engineering"},
        "bob": {"name": "Bob", "role": "manager", "department": "product"},
        "charlie": {"name": "Charlie", "role": "admin", "department": "ops"},
    }
    profile = base_profiles.get(user_id, {"name": user_id, "role": "user", "department": "general"})
    if permission_level == "read":
        profile["access"] = "read-only"
        profile["editable_fields"] = ["name", "department"]
    elif permission_level == "write":
        profile["access"] = "read-write"
        profile["editable_fields"] = ["name", "department", "role"]
        profile["last_edit"] = time.time()
    elif permission_level == "admin":
        profile["access"] = "admin"
        profile["editable_fields"] = ["name", "department", "role", "permissions"]
        profile["system_config"] = {"max_users": 1000, "session_timeout": 3600}
    profile["request_id"] = str(uuid.uuid4())
    profile["server_timestamp"] = time.time()
    profile["permission_level"] = permission_level
    profile["user_id"] = user_id
    return profile

def generate_data_list(user_id, permission_level, rng):
    n_items = rng.randint(5, 15)
    items = []
    for i in range(n_items):
        item = {
            "id": i,
            "name": f"item_{i}_{secrets.token_hex(4)}",
            "value": rng.randint(0, 1000),
            "category": rng.choice(["A", "B", "C", "D"]),
            "timestamp": time.time() + rng.uniform(-1, 1),
            "request_id": str(uuid.uuid4()),
        }
        if permission_level == "admin":
            item["internal_notes"] = f"Admin note for item {i}"
        if permission_level == "write":
            item["last_modified"] = time.time()
        items.append(item)
    response_data = {
        "items": items, "count": len(items), "user_id": user_id,
        "request_id": str(uuid.uuid4()), "server_timestamp": time.time(),
        "permission_level": permission_level,
    }
    return response_data

def generate_session_status(session_id, permission_level, rng):
    is_valid, perm_level = session_store.validate_session(session_id)
    status = {
        "session_id": session_id, "valid": is_valid,
        "permission_level": perm_level, "user_id": "test_user",
        "request_id": str(uuid.uuid4()), "server_timestamp": time.time(),
        "cache_control": "no-store",
    }
    if not is_valid:
        status["error"] = "Session expired or invalid"
        status["requires_reauth"] = True
    return status

# ─── JWT Helpers ────────────────────────────────────────────

def create_token(user_id="test_user", permission_level="read", expiry_hours=1, algorithm="RS256"):
    payload = {
        "sub": user_id, "permission_level": permission_level,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=expiry_hours)
    }
    if algorithm == "RS256":
        return jwt.encode(payload, RSA_PRIVATE_PEM, algorithm="RS256")
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def validate_token(token):
    try:
        payload = jwt.decode(token, RSA_PUBLIC_PEM, algorithms=["RS256"])
        return True, payload, None
    except jwt.ExpiredSignatureError:
        # V_ETAG_PERMISSION_LEAKAGE FIX: Decode expired token WITHOUT
        # verification to extract permission_level. This is safe because:
        # (a) we only use it for ETag stable_key, not for authorization,
        # (b) the token was legitimately issued (signed by us), just expired.
        try:
            payload = jwt.decode(token, RSA_PUBLIC_PEM, algorithms=["RS256"],
                                 options={"verify_exp": False, "verify_signature": False})
            return False, payload, "expired"
        except Exception:
            return False, {"error": "Token expired", "permission_level": "read"}, "expired"
    except jwt.InvalidSignatureError:
        return False, {"error": "Invalid signature"}, "invalid_signature"
    except jwt.DecodeError as e:
        return False, {"error": f"Decode error: {str(e)}"}, "decode_error"
    except Exception as e:
        return False, {"error": str(e)}, "unknown"

# ─── Auth Decorators ────────────────────────────────────────

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return _make_unauthorized_response("read")
        token = auth_header[7:]
        try:
            is_valid, payload, error = validate_token(token)
            if not is_valid:
                # V_ETAG_PERMISSION_LEAKAGE FIX: Extract permission_level
                # from the decoded payload (even expired tokens carry this).
                perm = payload.get("permission_level", "read") if isinstance(payload, dict) else "read"
                return _make_unauthorized_response(perm)
            request.token_payload = payload
            request.token_valid = True
            request.permission_level = payload.get("permission_level", "read")
            return f(*args, **kwargs)
        except Exception:
            return _make_unauthorized_response("read")
    return decorated

def _make_unauthorized_response(permission_level="read"):
    """Create a 401 response with ETag, Cache-Control, and request_id.

    V_ETAG_PERMISSION_LEAKAGE FIX: permission_level is derived from the
    JWT payload (even for expired tokens), so write-permission requests
    get write-etag instead of defaulting to read-etag.

    V1 FIX: request_id uses str(uuid.uuid4()) for ALL status codes.
    """
    path = request.path
    session_id = request.headers.get("X-Session-ID", secrets.token_hex(8))
    # Match the stable_key pattern used by route handlers
    if path == "/api/user/profile":
        stable_key = f"profile_test_user_{permission_level}"
    elif path == "/api/data/list":
        stable_key = f"datalist_test_user_{permission_level}"
    elif path == "/api/session/status":
        stable_key = f"session_{session_id}"
    else:
        stable_key = f"{path.replace('/', '_')}_{permission_level}"
    body_bytes = jsonify({"error": "Invalid token", "token_valid": False}).data
    etag = compute_etag(body_bytes, stable_key)
    # V1 FIX: request_id = uuid.uuid4() for ALL status codes
    response = make_response(jsonify({"error": "Invalid token", "token_valid": False, "request_id": str(uuid.uuid4())}), 401)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "max-age=30, stale-while-revalidate=10"
    response.headers["Vary"] = "Accept, Authorization"
    return response

# ─── Signal Extraction Helpers ──────────────────────────────

def compute_etag(body_bytes, stable_key):
    """Compute ETag from stable key (not body)."""
    return hashlib.sha256(stable_key.encode()).hexdigest()

def compute_request_id_entropy(request_id):
    if not request_id:
        return 0.0
    counts = Counter(request_id)
    length = len(request_id)
    entropy = 0.0
    for count in counts.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy

def get_dynamic_content_hash(response_data, request_id):
    timestamp = response_data.get("server_timestamp", time.time())
    uid = response_data.get("user_id", "test_user")
    perm = response_data.get("permission_level", "read")
    content_str = f"{timestamp}{request_id}{uid}{perm}"
    return hashlib.sha256(content_str.encode()).hexdigest()

# ─── Routes ──────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "server_state": {
            "cache_enabled": server_state["cache_enabled"],
            "cache_max_age": server_state["caching_max_age"],
            "permissions": server_state["permissions"],
            "seed": server_state["seed"],
            "jwt_algorithm": "RS256",
        }
    })

@app.route("/api/user/profile", methods=["GET"])
@require_token
def api_user_profile():
    rng = random.Random(int(time.time() * 1000) % (2**31))
    user_id = request.token_payload.get("sub", "test_user")
    perm_level = request.permission_level
    profile = generate_user_profile(user_id, perm_level, rng)
    request_id = profile["request_id"]

    stable_key = f"profile_{user_id}_{perm_level}"
    etag = compute_etag(b"", stable_key)

    response = make_response(jsonify(profile))
    response = apply_cache_headers(response, server_state["cache_enabled"], server_state["caching_max_age"])
    response.headers["ETag"] = etag

    if_none_match = request.headers.get("If-None-Match")
    if server_state["cache_enabled"] and if_none_match and if_none_match == etag:
        response = make_response("", 304)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "max-age=30, stale-while-revalidate=10"
        response.headers["Vary"] = "Accept, Authorization"
        cdn_cache.set(stable_key, profile)
        session_store.log_response("/api/user/profile", request_id, etag, "", cache_hit=1)
        return response

    cdn_cache.set(stable_key, profile)
    session_store.log_response("/api/user/profile", request_id, etag, "", cache_hit=0)

    session_id = request.cookies.get("session_id") or request.headers.get("X-Session-ID", "")
    is_valid, _ = session_store.validate_session(session_id)
    if not is_valid:
        response.headers["X-Session-State"] = "invalidated"

    return response

@app.route("/api/data/list", methods=["GET"])
@require_token
def api_data_list():
    rng = random.Random(int(time.time() * 1000) % (2**31))
    user_id = request.token_payload.get("sub", "test_user")
    perm_level = request.permission_level

    token_exp = request.token_payload.get("exp", 0)
    token_expired = datetime.now(timezone.utc) > datetime.fromtimestamp(token_exp, tz=timezone.utc)

    data = generate_data_list(user_id, perm_level, rng)
    request_id = data["request_id"]

    stable_key = f"datalist_{user_id}_{perm_level}"
    etag = compute_etag(b"", stable_key)

    response = make_response(jsonify(data))
    response = apply_cache_headers(response, server_state["cache_enabled"], server_state["caching_max_age"])
    response.headers["ETag"] = etag
    response.headers["Content-SHA256"] = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    if_none_match = request.headers.get("If-None-Match")
    if server_state["cache_enabled"] and if_none_match and if_none_match == etag:
        response = make_response("", 304)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "max-age=30, stale-while-revalidate=10"
        response.headers["Vary"] = "Accept, Authorization"
        return response

    if token_expired and perm_level != "admin":
        response.headers["X-RateLimit-Remaining"] = "0"
        response.headers["X-RateLimit-Triggered"] = "true"

    session_store.log_response("/api/data/list", request_id, etag, "", cache_hit=0)
    return response

@app.route("/api/session/status", methods=["GET"])
@require_token
def api_session_status():
    rng = random.Random(int(time.time() * 1000) % (2**31))
    session_id = request.cookies.get("session_id") or request.headers.get("X-Session-ID", secrets.token_hex(8))
    perm_level = request.permission_level

    is_valid, actual_perm = session_store.validate_session(session_id)
    status = generate_session_status(session_id, perm_level, rng)
    request_id = status["request_id"]

    response = make_response(jsonify(status), 200)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    body_bytes = json.dumps(status, sort_keys=True).encode()
    etag = compute_etag(body_bytes, f"session_{session_id}")
    response.headers["ETag"] = etag

    if not request.token_valid or not is_valid:
        response.headers["X-Token-Validation"] = "failed"
        status["token_validation_failure"] = 1
    else:
        status["token_validation_failure"] = 0

    session_store.log_response("/api/session/status", request_id, etag, session_id, cache_hit=0)
    return response

@app.route("/token", methods=["POST"])
def issue_token():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id", "test_user")
    permission_level = data.get("permission_level", "read")
    expiry_hours = data.get("expiry_hours", 1.0)
    expired = data.get("expired", False)
    algorithm = data.get("algorithm", "RS256")

    if expired:
        expiry_hours = -1

    token = create_token(user_id, permission_level, expiry_hours, algorithm=algorithm)
    session_id = session_store.create_session(user_id, permission_level)

    response = jsonify({"token": token, "session_id": session_id, "permission_level": permission_level})
    response.set_cookie("session_id", session_id, httponly=True, secure=False, samesite="Lax")
    return response

@app.route("/session/invalidate", methods=["POST"])
def invalidate_session():
    session_id = request.cookies.get("session_id") or request.headers.get("X-Session-ID")
    if session_id:
        session_store.invalidate_session(session_id)
    response = jsonify({"status": "invalidated", "session_id": session_id or "unknown"})
    response.set_cookie("session_id", "", expires=0)
    return response

@app.route("/admin/reset", methods=["POST"])
def reset_server():
    server_state["cache_enabled"] = True
    server_state["permissions"] = {"read": True, "write": False, "admin": False}
    server_state["request_counter"] = 0
    session_store.clear_all_sessions()
    cdn_cache.invalidate()
    return jsonify({"status": "reset"})

@app.route("/admin/set_cache", methods=["POST"])
def set_cache():
    data = request.get_json(silent=True) or {}
    server_state["cache_enabled"] = data.get("enabled", True)
    server_state["caching_max_age"] = data.get("max_age", CACHE_MAX_AGE)
    return jsonify({"status": "cache_set", "cache_enabled": server_state["cache_enabled"]})

@app.route("/admin/set_permissions", methods=["POST"])
def set_permissions():
    data = request.get_json(silent=True) or {}
    server_state["permissions"] = data.get("permissions", {"read": True, "write": False, "admin": False})
    for key, value in server_state["permissions"].items():
        session_store.set_permissions({key: value})
    return jsonify({"status": "permissions_set", "permissions": server_state["permissions"]})

@app.route("/admin/set_seed", methods=["POST"])
def set_seed():
    data = request.get_json(silent=True) or {}
    server_state["seed"] = data.get("seed", SERVER_SEED)
    return jsonify({"status": "seed_set", "seed": server_state["seed"]})

@app.route("/admin/get_stats", methods=["GET"])
def get_stats():
    stats = cdn_cache.get_stats()
    response_log = session_store.get_response_log()
    total_cache_hits = sum(1 for r in response_log if r.get("cache_hit", 0) == 1)
    total_requests = len(response_log)
    cache_hit_rate = total_cache_hits / total_requests if total_requests > 0 else 0.0
    return jsonify({
        "cdn_stats": stats, "cache_hit_rate": cache_hit_rate,
        "total_responses": total_requests,
        "server_seed": server_state["seed"], "cache_enabled": server_state["cache_enabled"]
    })

# ─── Main ────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Production-like Testbed Server for EXP-GRAPH-35481774794")
    parser.add_argument("--port", type=int, default=PORT, help="Port to run on")
    parser.add_argument("--seed", type=int, default=SERVER_SEED, help="Random seed")
    parser.add_argument("--db-path", type=str, default=SESSION_DB_PATH, help="SQLite DB path")
    parser.add_argument("--jitter-min", type=int, default=JITTER_MIN_MS, help="Min jitter in ms")
    parser.add_argument("--jitter-max", type=int, default=JITTER_MAX_MS, help="Max jitter in ms")
    parser.add_argument("--cache-max-age", type=int, default=CACHE_MAX_AGE, help="Cache max-age in seconds")
    parser.add_argument("--cache-disabled", action="store_true", default=False, help="Disable CDN caching")
    args = parser.parse_args()

    server_state["seed"] = args.seed
    server_state["caching_max_age"] = args.cache_max_age
    server_state["cache_enabled"] = not args.cache_disabled
    JITTER_MIN_MS = args.jitter_min
    JITTER_MAX_MS = args.jitter_max
    session_store = SQLiteSessionStore(args.db_path)
    cdn_cache = CDNCache(max_age=args.cache_max_age)

    print(f"Starting production-like testbed server on port {args.port}")
    print(f"  seed={args.seed}, cache_enabled={server_state['cache_enabled']}, max_age={args.cache_max_age}")
    print(f"  Jitter: {JITTER_MIN_MS}-{JITTER_MAX_MS}ms, RSA RS256 JWT, SQLite WAL-mode")
    print(f"  V_ETAG_PERMISSION_LEAKAGE FIX: permission_level from JWT payload")
    print(f"  V1 FIX: ALL request_ids use uuid.uuid4() (no token_hex)")

    app.run(host="127.0.0.1", port=args.port, debug=False, threaded=True)
