#!/usr/bin/env python3
"""
Flask mock API server for EXP-GRAPH-GRAPH-35191029030.
Adds unauthenticated /schema endpoint for structural probing independent of auth state.
Drift patterns: permission_boundary, session_invalidation only (signing_key_rotation EXCLUDED).
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
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Flask, request, jsonify, session, make_response
import jwt


# ─── Configuration ─────────────────────────────────────────────────────────────

PORT = int(os.environ.get("MOCK_SERVER_PORT", "18930"))
SECRET_KEY = os.environ.get("MOCK_SERVER_SECRET", secrets.token_hex(32))
JWT_ALGORITHM = "HS256"
SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = "/tmp/flask_sessions_35191029030"
SESSION_PERMANENT = False

os.makedirs(SESSION_FILE_DIR, exist_ok=True)


# ─── Flask App Setup ──────────────────────────────────────────────────────────

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SESSION_TYPE"] = SESSION_TYPE
app.config["SESSION_FILE_DIR"] = SESSION_FILE_DIR
app.config["SESSION_PERMANENT"] = SESSION_PERMANENT

# Global server state
server_state = {
    "signing_key": SECRET_KEY,
    "session_store": {},
    "permissions": {"read": True, "write": True, "admin": True},
    "schema_fields": [],
    "schema_size": 10,
    "noise_pattern": None,
    "drift_pattern": None,
    "co_occurring": False,
    "seed": 42,
}

sessions = {}


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


# ─── JWT Helpers ──────────────────────────────────────────────────────────────

def create_token(user_id="test_user", permissions=None, expiry_hours=1, signing_key=None):
    """Create a JWT token with given parameters."""
    if signing_key is None:
        signing_key = server_state["signing_key"]
    if permissions is None:
        permissions = server_state["permissions"]
    payload = {
        "sub": user_id,
        "permissions": permissions,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=expiry_hours)
    }
    return jwt.encode(payload, signing_key, algorithm=JWT_ALGORITHM)


def validate_token(token, signing_key=None):
    """Validate a JWT token against the given signing key."""
    if signing_key is None:
        signing_key = server_state["signing_key"]
    try:
        payload = jwt.decode(token, signing_key, algorithms=[JWT_ALGORITHM])
        return True, payload
    except jwt.InvalidSignatureError:
        return False, {"error": "Invalid signature"}
    except jwt.ExpiredSignatureError:
        return False, {"error": "Token expired"}
    except jwt.DecodeError as e:
        return False, {"error": f"Decode error: {str(e)}"}


# ─── Session Helpers ──────────────────────────────────────────────────────────

def get_session_id():
    """Get or create session ID from cookie or header."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = request.headers.get("X-Session-ID")
    if not session_id:
        session_id = secrets.token_hex(16)
    return session_id


def validate_session(session_id):
    """Validate session against server-side store."""
    return session_id in sessions and sessions[session_id].get("valid", False)


def create_session(user_id="test_user"):
    """Create a new server-side session."""
    session_id = secrets.token_hex(16)
    sessions[session_id] = {
        "user_id": user_id,
        "valid": True,
        "created_at": time.time(),
        "data": {}
    }
    return session_id


def invalidate_session(session_id):
    """Invalidate a session."""
    if session_id in sessions:
        sessions[session_id]["valid"] = False


def clear_all_sessions():
    """Clear all sessions (drift pattern: session_invalidation)."""
    for sid in sessions:
        sessions[sid]["valid"] = False


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
            if not server_state["permissions"].get(permission, False):
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
        "schema_size": server_state["schema_size"]
    }})


@app.route("/schema", methods=["GET"])
def get_schema():
    """UNAUTHENTICATED endpoint returning current schema.
    This is the structural probe independent of auth state."""
    return jsonify({"fields": server_state["schema_fields"], "size": len(server_state["schema_fields"])})


@app.route("/token", methods=["POST"])
def issue_token():
    """Issue a new JWT token."""
    data = request.get_json() or {}
    user_id = data.get("user_id", "test_user")
    permissions = data.get("permissions", server_state["permissions"])
    expiry_hours = data.get("expiry_hours", 1)
    token = create_token(user_id, permissions, expiry_hours)
    session_id = create_session(user_id)
    response = jsonify({"token": token, "session_id": session_id})
    response.set_cookie("session_id", session_id, httponly=True, secure=False)
    return response


@app.route("/api/read", methods=["GET"])
@require_token
@require_permission("read")
def api_read():
    """Read endpoint - requires read permission."""
    schema = server_state["schema_fields"]
    data = generate_response_data(schema)
    return jsonify(data)


@app.route("/api/write", methods=["POST"])
@require_token
@require_permission("write")
def api_write():
    """Write endpoint - requires write permission."""
    schema = server_state["schema_fields"]
    data = generate_response_data(schema)
    data["write_status"] = "success"
    return jsonify(data)


@app.route("/api/admin", methods=["GET"])
@require_token
@require_permission("admin")
def api_admin():
    """Admin endpoint - requires admin permission."""
    schema = server_state["schema_fields"]
    data = generate_response_data(schema)
    data["admin_data"] = "classified"
    return jsonify(data)


@app.route("/session/status", methods=["GET"])
def session_status():
    """Check session status."""
    session_id = get_session_id()
    is_valid = validate_session(session_id)
    return jsonify({"session_id": session_id, "valid": is_valid})


@app.route("/session/invalidate", methods=["POST"])
def invalidate_session_endpoint():
    """Invalidate current session."""
    session_id = get_session_id()
    invalidate_session(session_id)
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
        clear_all_sessions()
    elif pattern == "permission_boundary":
        pass  # Handled via /admin/set_permissions

    if "schema_size" in data:
        server_state["schema_size"] = data["schema_size"]
        server_state["schema_fields"] = generate_schema(data["schema_size"])

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
    return jsonify({"status": "noise_set", "noise_pattern": server_state["noise_pattern"]})


@app.route("/admin/reset", methods=["POST"])
def reset_server():
    """Reset server to baseline state."""
    server_state["drift_pattern"] = None
    server_state["noise_pattern"] = None
    server_state["co_occurring"] = False
    server_state["signing_key"] = SECRET_KEY
    server_state["permissions"] = {"read": True, "write": True, "admin": True}
    server_state["schema_fields"] = generate_schema(server_state["schema_size"], server_state["seed"])
    clear_all_sessions()
    return jsonify({"status": "reset"})


@app.route("/admin/set_permissions", methods=["POST"])
def set_permissions():
    """Set permissions (drift pattern: permission_boundary)."""
    data = request.get_json() or {}
    server_state["permissions"] = data.get("permissions", {"read": True, "write": True, "admin": True})
    return jsonify({"status": "permissions_set", "permissions": server_state["permissions"]})


@app.route("/admin/set_seed", methods=["POST"])
def set_seed():
    """Set RNG seed for reproducibility."""
    data = request.get_json() or {}
    server_state["seed"] = data.get("seed", 42)
    return jsonify({"status": "seed_set", "seed": server_state["seed"]})


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mock API server for EXP-GRAPH-35191029030")
    parser.add_argument("--port", type=int, default=PORT, help="Port to run on")
    parser.add_argument("--schema-size", type=int, default=10, help="Schema size")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    server_state["schema_size"] = args.schema_size
    server_state["seed"] = args.seed
    server_state["schema_fields"] = generate_schema(args.schema_size, args.seed)

    print(f"Starting mock server on port {args.port} with schema_size={args.schema_size}, seed={args.seed}")
    print(f"Signing key: {SECRET_KEY[:8]}...")

    app.run(host="127.0.0.1", port=args.port, debug=False, threaded=True)
