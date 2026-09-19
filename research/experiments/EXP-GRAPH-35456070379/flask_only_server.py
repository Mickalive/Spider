#!/usr/bin/env python3
"""
B-FLASK-ONLY baseline server for EXP-GRAPH-35456070379.

Plain Flask WITHOUT CDN simulation, OAuth middleware, or dynamic content.
Same corrected headers-only structural signal extraction as the testbed server.

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

PORT = int(os.environ.get("FLASK_ONLY_PORT", "18960"))
SECRET_KEY = os.environ.get("TESTBED_SECRET", secrets.token_hex(32))
SERVER_SEED = int(os.environ.get("TESTBED_SEED", "42"))
JITTER_MIN_MS = int(os.environ.get("TESTBED_JITTER_MIN", "10"))
JITTER_MAX_MS = int(os.environ.get("TESTBED_JITTER_MAX", "500"))

# ─── Flask App Setup ────────────────────────────────────────

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

server_state = {
    "seed": SERVER_SEED,
    "request_counter": 0,
}

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
def api_user_profile():
    rng = random.Random(int(time.time() * 1000) % (2**31))
    user_id = request.args.get("user_id", "test_user")
    permission_level = request.args.get("permission_level", "read")
    data = generate_static_data(user_id, permission_level, rng)
    request_id = data["request_id"]
    
    # B-FLASK-ONLY: No CDN cache, no auth, but still set headers
    response = make_response(jsonify(data))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["ETag"] = hashlib.sha256(f"profile_{user_id}_{permission_level}".encode()).hexdigest()
    return response

@app.route("/api/data/list", methods=["GET"])
def api_data_list():
    rng = random.Random(int(time.time() * 1000) % (2**31))
    user_id = request.args.get("user_id", "test_user")
    permission_level = request.args.get("permission_level", "read")
    data = generate_static_data(user_id, permission_level, rng)
    request_id = data["request_id"]
    
    response = make_response(jsonify(data))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["ETag"] = hashlib.sha256(f"datalist_{user_id}_{permission_level}".encode()).hexdigest()
    return response

@app.route("/api/session/status", methods=["GET"])
def api_session_status():
    rng = random.Random(int(time.time() * 1000) % (2**31))
    session_id = request.args.get("session_id", secrets.token_hex(8))
    permission_level = request.args.get("permission_level", "read")
    
    status = {
        "session_id": session_id, "valid": True,
        "permission_level": permission_level, "user_id": "test_user",
        "request_id": str(uuid.uuid4()), "server_timestamp": time.time(),
    }
    
    response = make_response(jsonify(status))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["ETag"] = hashlib.sha256(f"session_{session_id}".encode()).hexdigest()
    return response

@app.route("/admin/get_stats", methods=["GET"])
def get_stats():
    return jsonify({"flask_only": True, "cache_enabled": False})

# ─── Main ────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="B-FLASK-ONLY Baseline Server for EXP-GRAPH-35456070379")
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
    
    app.run(host="127.0.0.1", port=args.port, debug=False, threaded=True)
