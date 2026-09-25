#!/usr/bin/env python3
"""
EXP-GRAPH-36118890504 Flask 3.1.3 + PyJWT 2.13.0 HS256 single-node substrate.
Validated plain-HTTP observation/execution layer per Runtime EXP-RUNTIME-33902315583 ceiling.

Three isomorphic resources for A-to-B parameterized transfer test:
- Resource A (Train): GET /posts/{id} for ids 1..5
  Response: {"id": N, "userId": N, "title": "Post N", "body": "Body N"}
- Resource B (Test): GET /users/{id} for ids 6..10
  Response: {"id": N, "name": "User N", "username": "userN", "email": "userN@example.com"}
- Resource C (Null): POST /comments for ids 11..15
  Request: {"postId": N, "body": "comment"}
  Response: {"id": N, "postId": N, "name": "Comment N", "email": "commenter@example.com", "body": "comment"}

A and B are isomorphic: same HTTP method (GET), single path parameter {id}, JSON response with id field.
C is non-isomorphic: different method (POST), two parameters, different schema.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import random
from typing import Any

from flask import Flask, jsonify, request

# Configuration
EXPERIMENT_ID = "EXP-GRAPH-36118890504"
TESTBED_SECRET = os.environ.get("TESTBED_SECRET", "TESTBED_SECRET_SPIDER_36118890504")
PORT = int(os.environ.get("PORT", "18928"))  # Same port as EXP-RUNTIME-34015740602

# Jitter: 50-150ms uniform per Runtime validation
MIN_JITTER_MS = 50
MAX_JITTER_MS = 150


def apply_jitter() -> None:
    """Apply deterministic jitter per request."""
    jitter_ms = random.uniform(MIN_JITTER_MS, MAX_JITTER_MS)
    time.sleep(jitter_ms / 1000.0)


def verify_token(token: str) -> bool:
    """Verify HS256 JWT token."""
    try:
        import jwt
        jwt.decode(token, TESTBED_SECRET, algorithms=["HS256"])
        return True
    except Exception:
        return False


def make_token() -> str:
    """Create a valid HS256 JWT token."""
    import jwt
    return jwt.encode({"sub": "test", "exp": 9999999999}, TESTBED_SECRET, algorithm="HS256")


# Resource A: /posts/{id} for ids 1..5
def generate_post(id_val: int) -> dict[str, Any]:
    return {
        "id": id_val,
        "userId": id_val,
        "title": f"Post {id_val}",
        "body": f"Body {id_val}"
    }


# Resource B: /users/{id} for ids 6..10
def generate_user(id_val: int) -> dict[str, Any]:
    return {
        "id": id_val,
        "name": f"User {id_val}",
        "username": f"user{id_val}",
        "email": f"user{id_val}@example.com"
    }


# Resource C: /comments for ids 11..15 (POST)
def generate_comment(id_val: int, post_id: int, body: str) -> dict[str, Any]:
    return {
        "id": id_val,
        "postId": post_id,
        "name": f"Comment {id_val}",
        "email": "commenter@example.com",
        "body": body
    }


def create_app() -> Flask:
    app = Flask(__name__)

    @app.before_request
    def require_auth():
        # Skip auth for health check
        if request.path == "/health":
            return None
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401
        token = auth[7:]
        if not verify_token(token):
            return jsonify({"error": "bad token"}), 401
        return None

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "experiment": EXPERIMENT_ID})

    # Resource A: GET /posts/<int:id>
    @app.route("/posts/<int:id_val>", methods=["GET"])
    def get_post(id_val: int):
        apply_jitter()
        if id_val < 1 or id_val > 5:
            return jsonify({"error": "not found"}), 404
        return jsonify(generate_post(id_val))

    # Resource B: GET /users/<int:id>
    @app.route("/users/<int:id_val>", methods=["GET"])
    def get_user(id_val: int):
        apply_jitter()
        if id_val < 6 or id_val > 10:
            return jsonify({"error": "not found"}), 404
        return jsonify(generate_user(id_val))

    # Resource C: POST /comments
    @app.route("/comments", methods=["POST"])
    def post_comment():
        apply_jitter()
        data = request.get_json(silent=True) or {}
        post_id = data.get("postId")
        body = data.get("body", "")
        # Generate ID based on post_id for determinism
        id_val = 10 + post_id if post_id else 11
        if id_val < 11 or id_val > 15:
            return jsonify({"error": "invalid postId"}), 400
        return jsonify(generate_comment(id_val, post_id, body)), 201

    return app


if __name__ == "__main__":
    app = create_app()
    print(f"Starting {EXPERIMENT_ID} substrate on port {PORT}")
    print(f"Valid token: {make_token()}")
    app.run(host="127.0.0.1", port=PORT)