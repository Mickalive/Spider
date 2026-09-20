#!/usr/bin/env python3
"""
B-FLASK-ONLY baseline server for EXP-GRAPH-35470449310.

V2 FIX from EXP-GRAPH-35456070379: This server now implements genuine
token-state variation (valid/expired tokens via Authorization header or
query param). The prior version had zero auth middleware, producing
behavioral_delta=0.0 for all 480 samples (std=0, r=NaN).

Plain Flask WITHOUT CDN simulation, OAuth middleware, or dynamic content.
Same corrected headers-only structural signal extraction as the testbed server.
Uses V1 FIX: ALL request_ids use uuid.uuid4() (no token_hex).

Serves as baseline to discriminate infrastructure-induced vs definition-induced correlation.
"""

import os
import sys
import json
import time
import secrets
import threading
import argparse
import random
import hashlib
import uuid
import math
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path
from collections import Counter

from flask import Flask, request, jsonify, make_response

# ─── Configuration ─────────────────────────────────────

PORT = int(os.environ.get("FLASK_ONLY_PORT", "18980"))
SECRET_KEY = os.environ.get("TESTBED_SECRET", secrets.token_hex(32))
SERVER_SEED = int(os.environ.get("TESTBED_SEED", "42"))
JITTER_MIN_MS = int(os.environ.get("TESTBED_JITTER_MIN", "10"))
JITTER_MAX_MS = int(os.environ.get("TESTBED_JITTER_MAX", "500"))

# ─── Simple Token Store ────────────────────────────────

class SimpleTokenStore:
    """In-memory token store with valid/expired states for B-FLASK-ONLY baseline."""
    def __init__(self):
        self._tokens = {}
        self._lock = threading.Lock()

    def create_token(self, token_type="valid", permission_level="read"):
        """Create a token. token_type: 'valid' or 'expired'."""
        token_id = secrets.token_hex(16)
        expires_at = time.time() + (3600 if token_type == "valid" else -3600)
        with self._lock:
            self._tokens[token_id] = {
                "token_id": token_id,
                "token_type": token_type,
                "permission_level": permission_level,
                "expires_at": expires_at,
                "created_at": time.time(),
            }
        return token_id

    def validate_token(self, token_id):
        """Validate a token. Returns (is_valid, payload_or_error)."""
        with self._lock:
            if token_id not in self._tokens:
                return False, {"error": "Token not found"}
            token = self._tokens[token_id]
            if time.time() > token["expires_at"]:
                return False, {"error": "Token expired", "token_type": "expired"}
            return True, {
                "token_id": token_id,
                "permission_level": token["permission_level"],
                "token_type": token["token_type"],
            }


token_store = SimpleTokenStore()

# ─── Flask App Setup ────────────────────────────────────────

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

server_state = {
    "seed": SERVER_SEED,
    "request_counter": 0,
}

# ─── Auth Decorator ────────────────────────────────────────

def require_token(f):
    """Simple token validation: checks Authorization header or token query param."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token_id = None

        if auth_header.startswith("Bearer "):
            token_id = auth_header[7:]
        else:
            token_id = request.args.get("token", None)

        if not token_id:
            return _make_unauthorized_response()

        is_valid, payload = token_store.validate_token(token_id)
        if not is_valid:
            return _make_unauthorized_response()

        request.token_payload = payload
        request.token_valid = True
        request.permission_level = payload.get("permission_level", "read")
        return f(*args, **kwargs)
    return decorated


def _make_unauthorized_response():
    """Create a 401 response. V1 FIX: request_id uses uuid.uuid4()."""
    path = request.path
    permission_level = request.args.get("permission_level", "read")
    if path == "/api/user/profile":
        stable_key = f"profile_test_user_{permission_level}"
    elif path == "/api/data/list":
        stable_key = f"datalist_test_user_{permission_level}"
    elif path == "/api/session/status":
        stable_key = f"session_{secrets.token_hex(8)}"
    else:
        stable_key = f"{path.replace('/', '_')}_{permission_level}"
    body_bytes = json.dumps({"error": "Invalid token", "token_valid": False}).encode()
    etag = hashlib.sha256(stable_key.encode()).hexdigest()
    response = make_response(jsonify({"error": "Invalid token", "token_valid": False, "request_id": str(uuid.uuid4())}), 401)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response


# ─── Dynamic Content Generation ───────────────────────────────

def generate_static_data(user_id, permission_level, rng):
    """Generate static response with dynamic fields (timestamp, request_id)."""
    data = {
        "items": [{"id": i, "name": f"item_{i}", "value": rng.randint(0, 100)} for i in range(rng.randint(3, 8))],
        "count": 0, "user_id": user_id,
        "request_id": str(uuid.uuid4()),
        "server_timestamp": time.time(),
        "permission_level": permission_level,
    }
    data["count"] = len(data["items"])
    return data

# ─── Signal Extraction Helpers ──────────────────────────────

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
    return jsonify({"status": "ok", "flask_only": True})

@app.route("/api/user/profile", methods=["GET"])
@require_token
def api_user_profile():
    rng = random.Random(int(time.time() * 1000) % (2**31))
    user_id = request.args.get("user_id", "test_user")
    permission_level = request.permission_level
    data = generate_static_data(user_id, permission_level, rng)
    request_id = data["request_id"]

    response = make_response(jsonify(data))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["ETag"] = hashlib.sha256(f"profile_{user_id}_{permission_level}".encode()).hexdigest()
    return response

@app.route("/api/data/list", methods=["GET"])
@require_token
def api_data_list():
    rng = random.Random(int(time.time() * 1000) % (2**31))
    user_id = request.args.get("user_id", "test_user")
    permission_level = request.permission_level
    data = generate_static_data(user_id, permission_level, rng)
    request_id = data["request_id"]

    response = make_response(jsonify(data))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["ETag"] = hashlib.sha256(f"datalist_{user_id}_{permission_level}".encode()).hexdigest()
    return response

@app.route("/api/session/status", methods=["GET"])
@require_token
def api_session_status():
    rng = random.Random(int(time.time() * 1000) % (2**31))
    session_id = request.args.get("session_id", secrets.token_hex(8))
    permission_level = request.permission_level

    status = {
        "session_id": session_id, "valid": True,
        "permission_level": permission_level, "user_id": "test_user",
        "request_id": str(uuid.uuid4()), "server_timestamp": time.time(),
    }

    response = make_response(jsonify(status))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["ETag"] = hashlib.sha256(f"session_{session_id}".encode()).hexdigest()
    return response

@app.route("/token", methods=["POST"])
def create_token_endpoint():
    """Create a token for B-FLASK-ONLY baseline."""
    data = request.get_json(silent=True) or {}
    token_type = data.get("token_type", "valid")  # "valid" or "expired"
    permission_level = data.get("permission_level", "read")

    token_id = token_store.create_token(token_type=token_type, permission_level=permission_level)
    return jsonify({"token": token_id, "token_type": token_type})

@app.route("/admin/get_stats", methods=["GET"])
def get_stats():
    return jsonify({"flask_only": True, "cache_enabled": False})

# ─── Main ────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="B-FLASK-ONLY Baseline Server for EXP-GRAPH-35470449310")
    parser.add_argument("--port", type=int, default=PORT, help="Port to run on")
    parser.add_argument("--seed", type=int, default=SERVER_SEED, help="Random seed")
    parser.add_argument("--jitter-min", type=int, default=JITTER_MIN_MS, help="Min jitter in ms")
    parser.add_argument("--jitter-max", type=int, default=JITTER_MAX_MS, help="Max jitter in ms")
    args = parser.parse_args()

    server_state["seed"] = args.seed
    JITTER_MIN_MS = args.jitter_min
    JITTER_MAX_MS = args.jitter_max

    print(f"Starting B-FLASK-ONLY baseline server on port {args.port}")
    print(f"  seed={args.seed}, Jitter: {JITTER_MIN_MS}-{JITTER_MAX_MS}ms")
    print(f"  V2 FIX: Token validation enabled (valid/expired via header or query param)")
    print(f"  V1 FIX: ALL request_ids use uuid.uuid4() (no token_hex)")
    
    app.run(host="127.0.0.1", port=args.port, debug=False, threaded=True)
