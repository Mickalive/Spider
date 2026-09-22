"""Flask testbed mock for C-FRESHNESS kernel integration experiment.

Reuses the validated mock infrastructure from prior experiments:
- Flask 3.1.3 + PyJWT 2.14.0 HS256
- TTL cache 0.5s + jitter 1-100ms
- 3 endpoints: /api/user/profile, /api/data/list, /api/session/status
- Token management: single HS256 shared secret (TESTBED_SECRET)
- Drift types: expired token, session invalidation, permission boundary
- Noise types: optional_field_addition, description_change, response_time_jitter,
  field_type_normalization

Key design: ALL responses (including 401/403) include structural headers
(ETag, Cache-Control, X-Request-Id) so behavioral and structural signals
are independent — matching the validated parallel-channel architecture.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
import uuid

import jwt
from flask import Flask, jsonify, request

TESTBED_SECRET = "testbed-hs256-shared-secret-exp-product-35697049382"
JWT_ALGORITHM = "HS256"

app = Flask(__name__)


def _add_structural_headers(resp, data_for_etag: dict | None = None):
    """Add structural headers to ANY response (success or error)."""
    if data_for_etag is not None:
        raw = json.dumps(data_for_etag, sort_keys=True).encode()
        etag = f'"{hashlib.md5(raw).hexdigest()}"'
    else:
        etag = f'"error-{uuid.uuid4().hex[:8]}"'
    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = "no-store, no-cache"
    resp.headers["X-Request-Id"] = str(uuid.uuid4())
    return resp


def _validate_token(token: str) -> dict | None:
    """Validate a JWT token. Returns payload or None."""
    try:
        payload = jwt.decode(token, TESTBED_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def _apply_noise(endpoint: str, response_data: dict, query_args: dict) -> dict:
    """Apply noise patterns based on query parameters."""
    noise_type = query_args.get("noise", "")
    if not noise_type:
        return response_data

    data = dict(response_data)

    if noise_type == "optional_field_addition":
        size = int(query_args.get("size", "3"))
        for i in range(size):
            data[f"extra_field_{i}"] = f"noise_value_{i}"
    elif noise_type == "description_change":
        data["description"] = data.get("description", "") + " [modified]"
    elif noise_type == "response_time_jitter":
        jitter_ms = int(query_args.get("jitter_ms", "50"))
        time.sleep(jitter_ms / 1000.0)
    elif noise_type == "field_type_normalization":
        if "count" in data:
            data["count"] = str(data["count"])
        if "items" in data and isinstance(data["items"], list):
            data["items"] = json.dumps(data["items"])

    return data


@app.route("/api/user/profile", methods=["GET"])
def user_profile():
    """User profile endpoint. Returns 401 for expired/invalid, 403 for wrong role."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        error_data = {"error": "missing authorization"}
        resp = jsonify(error_data)
        return _add_structural_headers(resp, error_data), 401

    token = auth[7:]
    payload = _validate_token(token)
    if payload is None:
        error_data = {"error": "invalid or expired token"}
        resp = jsonify(error_data)
        return _add_structural_headers(resp, error_data), 401

    # Permission boundary: admin role not allowed on user profile
    if payload.get("role") == "admin":
        error_data = {"error": "forbidden: admin role not allowed"}
        resp = jsonify(error_data)
        return _add_structural_headers(resp, error_data), 403

    data = {
        "user_id": payload.get("sub", "unknown"),
        "role": payload.get("role", "user"),
        "name": "Test User",
        "email": "test@example.com",
        "description": "User profile endpoint response",
        "count": 42,
    }
    data = _apply_noise("profile", data, request.args)
    resp = jsonify(data)
    return _add_structural_headers(resp, data)


@app.route("/api/data/list", methods=["GET"])
def data_list():
    """Data list endpoint. Returns 401 for expired/invalid, 403 for wrong role."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        error_data = {"error": "missing authorization"}
        resp = jsonify(error_data)
        return _add_structural_headers(resp, error_data), 401

    token = auth[7:]
    payload = _validate_token(token)
    if payload is None:
        error_data = {"error": "invalid or expired token"}
        resp = jsonify(error_data)
        return _add_structural_headers(resp, error_data), 401

    # Permission boundary: admin role not allowed on data list
    if payload.get("role") == "admin":
        error_data = {"error": "forbidden: admin role not allowed"}
        resp = jsonify(error_data)
        return _add_structural_headers(resp, error_data), 403

    data = {
        "items": [
            {"id": 1, "name": "item-1"},
            {"id": 2, "name": "item-2"},
            {"id": 3, "name": "item-3"},
        ],
        "total": 3,
        "role": payload.get("role", "user"),
        "description": "Data list endpoint response",
        "count": 3,
    }
    data = _apply_noise("data_list", data, request.args)
    resp = jsonify(data)
    return _add_structural_headers(resp, data)


@app.route("/api/session/status", methods=["GET"])
def session_status():
    """Session status endpoint. Returns 401 for expired/invalid, 403 for wrong role."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        error_data = {"error": "missing authorization"}
        resp = jsonify(error_data)
        return _add_structural_headers(resp, error_data), 401

    token = auth[7:]
    payload = _validate_token(token)
    if payload is None:
        error_data = {"error": "invalid or expired token"}
        resp = jsonify(error_data)
        return _add_structural_headers(resp, error_data), 401

    # Permission boundary: admin role not allowed on session status
    if payload.get("role") == "admin":
        error_data = {"error": "forbidden: admin role not allowed"}
        resp = jsonify(error_data)
        return _add_structural_headers(resp, error_data), 403

    data = {
        "session_id": payload.get("jti", "unknown"),
        "status": "active",
        "role": payload.get("role", "user"),
        "expires_at": payload.get("exp", 0),
        "description": "Session status endpoint response",
        "count": 1,
    }
    data = _apply_noise("session", data, request.args)
    resp = jsonify(data)
    return _add_structural_headers(resp, data)


def start_server(port: int = 18928) -> None:
    """Start the testbed server in the current thread (blocking)."""
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    start_server()
