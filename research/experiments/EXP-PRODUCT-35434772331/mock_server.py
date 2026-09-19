#!/usr/bin/env python3
"""
EXP-PRODUCT-35434772331 Mock Server
Simulates a SPIDER kernel with JWT auth, session management, and drift/noise patterns.

Port: 18935 (unique from parent experiments)
"""
import json
import hashlib
import time
import random
import sqlite3
import threading
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Flask, request, jsonify, make_response
import jwt as pyjwt

# --- Configuration ---
SECRET_KEY = "test-secret-key-35434772331"
ALGORITHM = "HS256"
PORT = 18935
SEED = 42

# Auth states
AUTH_STATES = {
    "no_auth": {
        "description": "No Authorization header provided",
        "expected_status": 401,
        "expected_body_key": "login_required",
    },
    "valid_token": {
        "description": "Valid JWT Bearer token",
        "expected_status": 200,
        "expected_body_key": "success",
    },
    "expired_token": {
        "description": "Expired JWT Bearer token",
        "expected_status": 401,
        "expected_body_key": "auth_failed",
    },
    "invalid_token": {
        "description": "Invalid/malformed JWT Bearer token",
        "expected_status": 401,
        "expected_body_key": "auth_failed",
    },
}

# Drift patterns (auth drift = real security state changes)
DRIFT_PATTERNS = {
    "permission_boundary": {
        "description": "User role changes from admin to viewer mid-session",
        "behavioral_impact": True,
        "structural_impact": False,
    },
    "session_invalidation": {
        "description": "Session revoked server-side mid-sequence",
        "behavioral_impact": True,
        "structural_impact": False,
    },
    "token_refresh": {
        "description": "Token silently refreshed, new JWT issued",
        "behavioral_impact": True,
        "structural_impact": False,
    },
}

# Noise patterns (non-auth structural variation)
NOISE_PATTERNS = {
    "optional_field_addition": {
        "description": "Optional metadata field added to response",
        "behavioral_impact": False,
        "structural_impact": True,
    },
    "description_change": {
        "description": "API description text updated",
        "behavioral_impact": False,
        "structural_impact": True,
    },
    "response_time_jitter": {
        "description": "Extra processing delay added",
        "behavioral_impact": False,
        "structural_impact": True,
    },
    "field_type_normalization": {
        "description": "Field type annotation normalized",
        "behavioral_impact": False,
        "structural_impact": True,
    },
}

# SQLite database for sessions and permissions
DB_PATH = ":memory:"

class SessionDB:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
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
            # Seed data
            c.execute(
                "INSERT OR REPLACE INTO sessions VALUES (?, ?, ?, ?, ?, ?)",
                ("sess-admin-001", "alice", "admin", 
                 datetime.now(timezone.utc).isoformat(),
                 (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
                 1)
            )
            c.execute(
                "INSERT OR REPLACE INTO permissions VALUES (?, ?, ?)",
                ("alice", "admin", json.dumps(["read", "write", "admin", "delete"]))
            )
            self.conn.commit()
    
    def get_session(self, session_id):
        with self.lock:
            c = self.conn.cursor()
            c.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,))
            row = c.fetchone()
            if row:
                return {
                    "session_id": row[0], "user_id": row[1], "role": row[2],
                    "created_at": row[3], "expires_at": row[4], "is_valid": row[5]
                }
            return None
    
    def invalidate_session(self, session_id):
        with self.lock:
            c = self.conn.cursor()
            c.execute("UPDATE sessions SET is_valid=0 WHERE session_id=?", (session_id,))
            self.conn.commit()
    
    def change_role(self, user_id, new_role):
        with self.lock:
            c = self.conn.cursor()
            c.execute("UPDATE sessions SET role=? WHERE user_id=?", (new_role, user_id))
            c.execute("UPDATE permissions SET role=? WHERE user_id=?", (new_role, user_id))
            perms = json.dumps(["read"]) if new_role == "viewer" else json.dumps(["read", "write", "admin", "delete"])
            c.execute("UPDATE permissions SET permissions=? WHERE user_id=?", (perms, user_id))
            self.conn.commit()
    
    def get_permissions(self, user_id):
        with self.lock:
            c = self.conn.cursor()
            c.execute("SELECT * FROM permissions WHERE user_id=?", (user_id,))
            row = c.fetchone()
            if row:
                return {"user_id": row[0], "role": row[1], "permissions": json.loads(row[2])}
            return None


db = SessionDB()
app = Flask(__name__)
app.config['SERVER_NAME'] = f'127.0.0.1:{PORT}'

# State tracking for drift sequences
sequence_state = {
    "current_role": "admin",
    "session_valid": True,
    "drift_active": False,
    "drift_type": None,
    "noise_active": False,
    "noise_type": None,
    "extra_fields": {},
}


def make_valid_token(user_id="alice", role="admin", exp_hours=1):
    """Create a valid JWT token."""
    payload = {
        "sub": user_id,
        "role": role,
        "iss": "spider-kernel",
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=exp_hours),
        "session_id": "sess-admin-001",
    }
    return pyjwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def make_expired_token(user_id="alice", role="admin"):
    """Create an expired JWT token."""
    payload = {
        "sub": user_id,
        "role": role,
        "iss": "spider-kernel",
        "iat": datetime.now(timezone.utc) - timedelta(hours=2),
        "exp": datetime.now(timezone.utc) - timedelta(hours=1),
        "session_id": "sess-admin-001",
    }
    return pyjwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def make_invalid_token():
    """Create an invalid JWT token (wrong secret)."""
    payload = {
        "sub": "alice",
        "role": "admin",
        "iss": "spider-kernel",
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "session_id": "sess-admin-001",
    }
    return pyjwt.encode(payload, "wrong-secret-key", algorithm=ALGORITHM)


def get_auth_token(auth_header):
    """Extract and validate JWT from Authorization header. Returns (status, payload, error)."""
    if not auth_header:
        return 401, None, "login_required"
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        return 401, None, "auth_failed"
    
    token = parts[1]
    
    # Check for expired token first
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        # Token is valid
        session = db.get_session(payload.get("session_id", ""))
        if session and not session["is_valid"]:
            return 401, None, "session_invalidated"
        return 200, payload, None
    except pyjwt.ExpiredSignatureError:
        return 401, None, "auth_failed"
    except pyjwt.InvalidTokenError:
        return 401, None, "auth_failed"


# --- Endpoints ---

@app.route("/api/data", methods=["GET"])
def get_data():
    """Main data endpoint - returns different responses based on auth state."""
    # Add processing jitter
    jitter = random.uniform(0.05, 0.15)
    time.sleep(jitter)
    
    auth_header = request.headers.get("Authorization")
    status, payload, error = get_auth_token(auth_header)
    
    if error == "login_required":
        body = {"error": "login_required", "message": "Authentication required"}
        resp = make_response(jsonify(body), 401)
    elif error == "auth_failed":
        body = {"error": "authentication_failed"}
        resp = make_response(jsonify(body), 401)
    elif error == "session_invalidated":
        body = {"error": "session_invalidated", "message": "Session has been revoked"}
        resp = make_response(jsonify(body), 401)
    elif status == 200:
        # Successful response
        body = {
            "user_id": payload["sub"],
            "role": payload["role"],
            "data": {"value": "test_data_35434772331"},
            "session_id": payload.get("session_id"),
        }
        if sequence_state["drift_active"] and sequence_state["drift_type"] == "permission_boundary":
            body["role"] = sequence_state["current_role"]
            perms = db.get_permissions(payload["sub"])
            if perms:
                body["permissions"] = perms["permissions"]
        resp = make_response(jsonify(body), 200)
    else:
        body = {"error": "unknown"}
        resp = make_response(jsonify(body), 500)
    
    # Add noise-pattern headers if active
    if sequence_state["noise_active"]:
        noise_type = sequence_state["noise_type"]
        if noise_type == "optional_field_addition":
            resp.headers["X-Api-Metadata"] = json.dumps(sequence_state["extra_fields"])
        elif noise_type == "field_type_normalization":
            resp.headers["X-Api-Version"] = "2.0-normalized"
        elif noise_type == "response_time_jitter":
            time.sleep(random.uniform(0.01, 0.05))  # Extra jitter
    
    # Cache-Control varies with auth state
    if status == 200:
        resp.headers["Cache-Control"] = "no-cache"
    else:
        resp.headers["Cache-Control"] = "no-store"
    
    # Set-Cookie only for valid tokens
    if status == 200:
        resp.headers["Set-Cookie"] = f"session={payload.get('session_id', 'none')}; HttpOnly; Secure"
    
    return resp


@app.route("/api/schema", methods=["GET"])
def get_schema():
    """Structural endpoint - returns API schema (simulates structural signal)."""
    time.sleep(random.uniform(0.02, 0.08))
    
    schema = {
        "endpoints": ["/api/data", "/api/schema", "/api/session/status"],
        "methods": {"GET": True, "POST": False},
        "auth_required": True,
        "fields": ["user_id", "role", "data", "session_id"],
        "description": "SPIDER kernel data API v2",
    }
    
    if sequence_state["noise_active"]:
        noise_type = sequence_state["noise_type"]
        if noise_type == "optional_field_addition":
            schema["optional_fields"] = list(sequence_state["extra_fields"].keys())
        elif noise_type == "description_change":
            schema["description"] = "SPIDER kernel data API v2.1 - Updated"
        elif noise_type == "field_type_normalization":
            schema["field_types"] = {f: "string" for f in schema["fields"]}
    
    resp = make_response(jsonify(schema), 200)
    
    # ETag varies with noise
    body_str = json.dumps(schema, sort_keys=True)
    etag = hashlib.sha256(body_str.encode()).hexdigest()[:16]
    resp.headers["ETag"] = f'"{etag}"'
    
    return resp


@app.route("/api/session/status", methods=["GET"])
def session_status():
    """Behavioral signal endpoint - returns session status."""
    time.sleep(random.uniform(0.02, 0.08))
    
    auth_header = request.headers.get("Authorization")
    status, payload, error = get_auth_token(auth_header)
    
    if error == "login_required":
        return jsonify({"status": "unauthenticated", "session_valid": False}), 401
    elif error in ("auth_failed", "session_invalidated"):
        return jsonify({"status": "invalid", "session_valid": False}), 401
    elif status == 200:
        session = db.get_session(payload.get("session_id", ""))
        session_valid = session and session["is_valid"] if session else False
        
        # Drift: permission boundary check
        if sequence_state["drift_active"] and sequence_state["drift_type"] == "permission_boundary":
            return jsonify({
                "status": "active",
                "session_valid": session_valid,
                "role": sequence_state["current_role"],
                "permissions": db.get_permissions(payload["sub"])["permissions"],
            }), 200
        elif sequence_state["drift_active"] and sequence_state["drift_type"] == "session_invalidation":
            return jsonify({"status": "revoked", "session_valid": False}), 403
        elif sequence_state["drift_active"] and sequence_state["drift_type"] == "token_refresh":
            return jsonify({"status": "refreshed", "session_valid": True, "new_token_issued": True}), 200
        else:
            return jsonify({
                "status": "active",
                "session_valid": session_valid,
                "role": payload.get("role", "unknown"),
            }), 200
    
    return jsonify({"status": "error"}), 500


@app.route("/api/drift", methods=["POST"])
def set_drift():
    """Control endpoint to activate drift patterns."""
    data = request.json or {}
    drift_type = data.get("drift_type")
    
    if drift_type and drift_type in DRIFT_PATTERNS:
        sequence_state["drift_active"] = True
        sequence_state["drift_type"] = drift_type
        
        if drift_type == "permission_boundary":
            sequence_state["current_role"] = "viewer"
            db.change_role("alice", "viewer")
        elif drift_type == "session_invalidation":
            sequence_state["session_valid"] = False
            db.invalidate_session("sess-admin-001")
        
        return jsonify({"status": "drift_activated", "type": drift_type}), 200
    elif drift_type is None or drift_type == "none":
        sequence_state["drift_active"] = False
        sequence_state["drift_type"] = None
        # Reset
        db.change_role("alice", "admin")
        db.conn.cursor().execute(
            "UPDATE sessions SET is_valid=1 WHERE session_id='sess-admin-001'"
        )
        db.conn.commit()
        return jsonify({"status": "drift_cleared"}), 200
    
    return jsonify({"error": "invalid drift_type"}), 400


@app.route("/api/noise", methods=["POST"])
def set_noise():
    """Control endpoint to activate noise patterns."""
    data = request.json or {}
    noise_type = data.get("noise_type")
    
    if noise_type and noise_type in NOISE_PATTERNS:
        sequence_state["noise_active"] = True
        sequence_state["noise_type"] = noise_type
        
        if noise_type == "optional_field_addition":
            sequence_state["extra_fields"] = {
                "debug_info": "session_trace_35434772331",
                "cache_key": "v2_test",
            }
        
        return jsonify({"status": "noise_activated", "type": noise_type}), 200
    elif noise_type is None or noise_type == "none":
        sequence_state["noise_active"] = False
        sequence_state["noise_type"] = None
        sequence_state["extra_fields"] = {}
        return jsonify({"status": "noise_cleared"}), 200
    
    return jsonify({"error": "invalid noise_type"}), 400


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "port": PORT}), 200


if __name__ == "__main__":
    random.seed(SEED)
    app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False)
