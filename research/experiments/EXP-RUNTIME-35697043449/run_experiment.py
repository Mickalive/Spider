#!/usr/bin/env python3
"""
EXP-RUNTIME-35697043449 — Writable/Auth/Session/Drift Controls
Flask+SQLite+JWT localhost testbed for HTTP fingerprint substrate discrimination.

Measures:
  - Permission escalation (reader -> admin via SQLite UPDATE)
  - Session invalidation (server-side DELETE session)
  - Auth-state drift (fresh vs near-expiry JWT, identical responses)
  - Baselines: B-STATUS-ONLY, B-BODY-ONLY, B-HEADERS-ONLY
"""

import hashlib
import json
import os
import random
import secrets
import sqlite3
import subprocess
import sys
import time
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import jwt
import requests
from flask import Flask, g, jsonify, request as flask_request

# ─── Configuration ───────────────────────────────────────────────────────────
SEED = 44
N_SAMPLES = 20
JITTER_MIN_MS = 50
JITTER_MAX_MS = 150
JWT_SECRET = "test-secret-key-exp-runtime-35697043449"
JWT_ALGORITHM = "HS256"
DB_PATH = "/tmp/spider_auth_testbed.db"
PORT = 19847
HOST = "127.0.0.1"

EXCLUDED_HEADERS = {"Date", "Server", "X-Request-Id"}

random.seed(SEED)


# ─── Database Setup ──────────────────────────────────────────────────────────

def init_db():
    """Create fresh SQLite database with users and sessions tables."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'reader'
        )
    """)
    
    c.execute("""
        CREATE TABLE sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_hash TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            is_valid INTEGER NOT NULL DEFAULT 1
        )
    """)
    
    # Insert test users
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
              ("reader", hashlib.sha256(b"reader_pass").hexdigest(), "reader"))
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
              ("admin", hashlib.sha256(b"admin_pass").hexdigest(), "admin"))
    
    conn.commit()
    conn.close()


def reset_db():
    """Reset database to initial state."""
    init_db()


def get_db():
    """Get database connection for current request."""
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


# ─── JWT Helpers ─────────────────────────────────────────────────────────────

def create_token(username: str, role: str, exp_seconds: int = 3600, 
                 iat_offset: int = 0) -> str:
    """Create a JWT token with specified expiry and iat offset.
    
    The JWT contains only the subject (username) for identity.
    The server looks up the current role from SQLite, making
    writable role changes observable via HTTP.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        # Note: role is NOT embedded in the JWT. The server queries
        # SQLite for the current role, enabling writable controls.
        "iat": int((now - timedelta(seconds=iat_offset)).timestamp()),
        "exp": int((now - timedelta(seconds=iat_offset) + timedelta(seconds=exp_seconds)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_session(token: str, username: str, expires_seconds: int = 3600):
    """Store session in SQLite."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now(timezone.utc)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    c.execute(
        "INSERT INTO sessions (token_hash, username, created_at, expires_at, is_valid) "
        "VALUES (?, ?, ?, ?, 1)",
        (token_hash, username, now.isoformat(), 
         (now + timedelta(seconds=expires_seconds)).isoformat())
    )
    conn.commit()
    conn.close()


def invalidate_session(token: str):
    """Invalidate a session server-side."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    c.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))
    conn.commit()
    conn.close()


def check_session(token: str) -> bool:
    """Check if session is valid in SQLite."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    c.execute("SELECT is_valid FROM sessions WHERE token_hash = ? AND is_valid = 1",
              (token_hash,))
    row = c.fetchone()
    conn.close()
    return row is not None


def promote_user(username: str, new_role: str):
    """Promote user role via SQLite UPDATE (writable control)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
    conn.commit()
    conn.close()


# ─── Flask App ───────────────────────────────────────────────────────────────

def create_app() -> Flask:
    app = Flask(__name__)
    
    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()
    
    @app.route('/auth/token', methods=['POST'])
    def auth_token():
        data = flask_request.get_json(force=True)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "missing_credentials"}), 400
        
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        
        if user is None:
            return jsonify({"error": "invalid_credentials"}), 401
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user['password_hash'] != password_hash:
            return jsonify({"error": "invalid_credentials"}), 401
        
        token = create_token(username, user['role'])
        create_session(token, username)
        
        return jsonify({
            "token": token,
            "token_type": "Bearer",
            "expires_in": 3600
        }), 200
    
    @app.route('/protected', methods=['GET'])
    def protected():
        auth_header = flask_request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "authentication_required"}), 401
        
        token = auth_header[7:]
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token_expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid_token"}), 401
        
        if not check_session(token):
            return jsonify({"error": "session_invalid"}), 401
        
        username = payload.get('sub')
        
        # Server looks up CURRENT role from SQLite (not from JWT).
        # This makes writable role changes observable via HTTP.
        db = get_db()
        user = db.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
        if user is None:
            return jsonify({"error": "user_not_found"}), 404
        role = user['role']
        
        return jsonify({
            "role": role,
            "access": "full" if role == 'admin' else "limited",
            "username": username
        }), 200
    
    @app.route('/admin', methods=['GET'])
    def admin():
        auth_header = flask_request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "authentication_required"}), 401
        
        token = auth_header[7:]
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token_expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid_token"}), 401
        
        if not check_session(token):
            return jsonify({"error": "session_invalid"}), 401
        
        username = payload.get('sub')
        
        # Server looks up CURRENT role from SQLite (not from JWT).
        # This makes writable role changes observable via HTTP.
        db = get_db()
        user = db.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
        if user is None:
            return jsonify({"error": "user_not_found"}), 404
        role = user['role']
        
        if role != 'admin':
            return jsonify({"error": "forbidden"}), 403
        
        return jsonify({
            "role": "admin",
            "access": "full",
            "dashboard": "Admin Dashboard: All systems operational",
            "username": username
        }), 200
    
    @app.route('/session/status', methods=['GET'])
    def session_status():
        auth_header = flask_request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "authentication_required"}), 401
        
        token = auth_header[7:]
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token_expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid_token"}), 401
        
        session_valid = check_session(token)
        
        return jsonify({
            "session_valid": session_valid,
            "username": payload.get('sub'),
            "role": payload.get('role')
        }), 200
    
    return app


# ─── Observation Helpers ─────────────────────────────────────────────────────

def observe_response(endpoint: str, token: Optional[str] = None, 
                     method: str = "GET") -> Dict[str, Any]:
    """Make an HTTP request and observe the full response."""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    url = f"http://{HOST}:{PORT}{endpoint}"
    
    start_time = time.monotonic()
    if method == "GET":
        resp = requests.get(url, headers=headers, timeout=10)
    elif method == "POST":
        resp = requests.post(url, headers=headers, timeout=10)
    else:
        resp = requests.request(method, url, headers=headers, timeout=10)
    end_time = time.monotonic()
    
    # Collect filtered headers
    filtered_headers = {}
    for k, v in resp.headers.items():
        if k not in EXCLUDED_HEADERS:
            filtered_headers[k] = v
    
    return {
        "status": resp.status_code,
        "body": resp.text,
        "body_bytes": resp.content,
        "headers": filtered_headers,
        "headers_raw": dict(resp.headers),
        "response_time_ms": round((end_time - start_time) * 1000, 2),
    }


def compute_fingerprint(obs: Dict[str, Any], source: str = "full") -> str:
    """Compute a fingerprint hash from observation.
    
    source: 'full' = status+body+sorted_headers
            'status' = status only
            'body' = body only
            'headers' = headers only
    """
    if source == "full":
        parts = [
            str(obs["status"]),
            repr(obs["body_bytes"]),
            json.dumps(obs["headers"], sort_keys=True)
        ]
    elif source == "status":
        parts = [str(obs["status"])]
    elif source == "body":
        parts = [repr(obs["body_bytes"])]
    elif source == "headers":
        parts = [json.dumps(obs["headers"], sort_keys=True)]
    else:
        raise ValueError(f"Unknown source: {source}")
    
    return hashlib.sha256("||".join(parts).encode()).hexdigest()


def jaccard_distance(set_a: set, set_b: set) -> float:
    """Compute Jaccard distance between two fingerprint sets."""
    if len(set_a) == 0 and len(set_b) == 0:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return 1.0 - (intersection / union) if union > 0 else 0.0


def bootstrap_jaccard_ci(set_a: set, set_b: set, n_bootstrap: int = 1000,
                         alpha: float = 0.05) -> Tuple[float, float, float]:
    """Compute Jaccard distance and bootstrap 95% CI."""
    all_items = list(set_a | set_b)
    if len(all_items) == 0:
        return 0.0, 0.0, 0.0
    
    observed = jaccard_distance(set_a, set_b)
    
    boot_dists = []
    for _ in range(n_bootstrap):
        # Resample with replacement from each set
        boot_a = set(random.choices(list(set_a), k=len(set_a))) if set_a else set()
        boot_b = set(random.choices(list(set_b), k=len(set_b))) if set_b else set()
        boot_dists.append(jaccard_distance(boot_a, boot_b))
    
    boot_dists.sort()
    ci_lower = boot_dists[int(alpha / 2 * len(boot_dists))]
    ci_upper = boot_dists[int((1 - alpha / 2) * len(boot_dists))]
    
    return observed, ci_lower, ci_upper


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full experiment."""
    print("=" * 70)
    print("EXP-RUNTIME-35697043449 — Writable/Auth/Session/Drift Controls")
    print("=" * 70)
    
    # Initialize database
    reset_db()
    print("[OK] Database initialized")
    
    # Start Flask server
    app = create_app()
    server_thread = threading.Thread(
        target=lambda: app.run(host=HOST, port=PORT, debug=False, use_reloader=False),
        daemon=True
    )
    server_thread.start()
    time.sleep(1.0)  # Wait for server startup
    print(f"[OK] Flask server started on {HOST}:{PORT}")
    
    # Verify server is running
    try:
        requests.get(f"http://{HOST}:{PORT}/session/status", timeout=5)
    except Exception as e:
        print(f"[FAIL] Server not reachable: {e}")
        return None
    
    # ─── Step 1: Get initial reader token ────────────────────────────────────
    print("\n--- Step 1: Authentication ---")
    resp = requests.post(f"http://{HOST}:{PORT}/auth/token",
                         json={"username": "reader", "password": "reader_pass"},
                         timeout=5)
    reader_token = resp.json()["token"]
    print(f"[OK] Reader token obtained (len={len(reader_token)})")
    
    # ─── Step 2: Observe initial states ──────────────────────────────────────
    print("\n--- Step 2: Observing initial states ---")
    
    # State: valid_reader on /admin → 403
    obs_reader_admin = observe_response("/admin", reader_token)
    print(f"  valid_reader /admin: status={obs_reader_admin['status']}, "
          f"body_len={len(obs_reader_admin['body'])}")
    
    # State: valid_reader on /protected → 200
    obs_reader_protected = observe_response("/protected", reader_token)
    print(f"  valid_reader /protected: status={obs_reader_protected['status']}, "
          f"body_len={len(obs_reader_protected['body'])}")
    
    # ─── Step 3: N=20 observations per state ─────────────────────────────────
    print(f"\n--- Step 3: Collecting N={N_SAMPLES} observations per state ---")
    
    # Auth states (enum):
    # no_auth = no token
    # valid_reader = valid JWT, reader role, active session
    # valid_admin = valid JWT, admin role, active session (after promotion)
    # session_killed = valid JWT, reader role, session invalidated
    
    all_observations = {}
    
    # ─── 3a: no_auth observations ────────────────────────────────────────────
    print("  [1/4] no_auth: /protected without token")
    no_auth_fp = set()
    no_auth_observations = []
    for i in range(N_SAMPLES):
        jitter = random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0
        time.sleep(jitter)
        obs = observe_response("/protected", token=None)
        fp = compute_fingerprint(obs, "full")
        no_auth_fp.add(fp)
        no_auth_observations.append({
            "index": i, "status": obs["status"], "fingerprint": fp,
            "body_len": len(obs["body_bytes"]),
            "body_hash": hashlib.sha256(obs["body_bytes"]).hexdigest(),
            "headers_json": json.dumps(obs["headers"], sort_keys=True),
            "response_time_ms": obs["response_time_ms"]
        })
    print(f"    Unique fingerprints: {len(no_auth_fp)}, "
          f"Sample status: {no_auth_observations[0]['status']}")
    
    # ─── 3b: valid_reader observations (on /protected) ───────────────────────
    print("  [2/4] valid_reader: /protected with reader token")
    valid_reader_fp = set()
    valid_reader_observations = []
    for i in range(N_SAMPLES):
        jitter = random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0
        time.sleep(jitter)
        obs = observe_response("/protected", reader_token)
        fp = compute_fingerprint(obs, "full")
        valid_reader_fp.add(fp)
        valid_reader_observations.append({
            "index": i, "status": obs["status"], "fingerprint": fp,
            "body_len": len(obs["body_bytes"]),
            "body_hash": hashlib.sha256(obs["body_bytes"]).hexdigest(),
            "headers_json": json.dumps(obs["headers"], sort_keys=True),
            "response_time_ms": obs["response_time_ms"]
        })
    print(f"    Unique fingerprints: {len(valid_reader_fp)}, "
          f"Sample status: {valid_reader_observations[0]['status']}")
    
    # Also collect valid_reader on /admin for permission escalation
    print("  [2b/4] valid_reader: /admin with reader token")
    reader_admin_fp = set()
    reader_admin_observations = []
    for i in range(N_SAMPLES):
        jitter = random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0
        time.sleep(jitter)
        obs = observe_response("/admin", reader_token)
        fp = compute_fingerprint(obs, "full")
        reader_admin_fp.add(fp)
        reader_admin_observations.append({
            "index": i, "status": obs["status"], "fingerprint": fp,
            "body_len": len(obs["body_bytes"]),
            "body_hash": hashlib.sha256(obs["body_bytes"]).hexdigest(),
            "headers_json": json.dumps(obs["headers"], sort_keys=True),
            "response_time_ms": obs["response_time_ms"]
        })
    print(f"    Unique fingerprints: {len(reader_admin_fp)}, "
          f"Sample status: {reader_admin_observations[0]['status']}")
    
    # ─── 3c: Permission escalation — promote reader to admin ─────────────────
    print("  [3/4] Permission escalation: promoting reader to admin via SQLite UPDATE")
    promote_user("reader", "admin")
    time.sleep(0.1)  # Ensure commit is visible
    
    # Verify the update
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username = 'reader'")
    new_role = c.fetchone()[0]
    conn.close()
    print(f"    Verified: reader role is now '{new_role}'")
    
    # valid_admin observations (on /admin after promotion)
    print("  [3b/4] valid_admin: /admin with promoted reader token")
    valid_admin_fp = set()
    valid_admin_observations = []
    for i in range(N_SAMPLES):
        jitter = random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0
        time.sleep(jitter)
        obs = observe_response("/admin", reader_token)  # same JWT, but role changed server-side
        fp = compute_fingerprint(obs, "full")
        valid_admin_fp.add(fp)
        valid_admin_observations.append({
            "index": i, "status": obs["status"], "fingerprint": fp,
            "body_len": len(obs["body_bytes"]),
            "body_hash": hashlib.sha256(obs["body_bytes"]).hexdigest(),
            "headers_json": json.dumps(obs["headers"], sort_keys=True),
            "response_time_ms": obs["response_time_ms"]
        })
    print(f"    Unique fingerprints: {len(valid_admin_fp)}, "
          f"Sample status: {valid_admin_observations[0]['status']}")
    
    # ─── 3d: Session invalidation — kill reader session ──────────────────────
    print("  [4/4] Session invalidation: deleting reader session from SQLite")
    
    # Reset role back to reader first for clean session kill test
    promote_user("reader", "reader")
    time.sleep(0.1)
    
    # Get a fresh token for session kill test
    resp = requests.post(f"http://{HOST}:{PORT}/auth/token",
                         json={"username": "reader", "password": "reader_pass"},
                         timeout=5)
    session_kill_token = resp.json()["token"]
    
    # Verify session is valid first
    obs_before = observe_response("/protected", session_kill_token)
    print(f"    Before kill: status={obs_before['status']}")
    
    # Invalidate session
    invalidate_session(session_kill_token)
    time.sleep(0.1)
    
    # Verify session is invalid
    session_valid = check_session(session_kill_token)
    print(f"    Session valid after kill: {session_valid}")
    
    # session_killed observations (on /protected after session invalidation)
    session_killed_fp = set()
    session_killed_observations = []
    for i in range(N_SAMPLES):
        jitter = random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0
        time.sleep(jitter)
        obs = observe_response("/protected", session_kill_token)
        fp = compute_fingerprint(obs, "full")
        session_killed_fp.add(fp)
        session_killed_observations.append({
            "index": i, "status": obs["status"], "fingerprint": fp,
            "body_len": len(obs["body_bytes"]),
            "body_hash": hashlib.sha256(obs["body_bytes"]).hexdigest(),
            "headers_json": json.dumps(obs["headers"], sort_keys=True),
            "response_time_ms": obs["response_time_ms"]
        })
    print(f"    Unique fingerprints: {len(session_killed_fp)}, "
          f"Sample status: {session_killed_observations[0]['status']}")
    
    # ─── Step 4: Null control — fresh vs near-expiry tokens ──────────────────
    print("\n--- Step 4: Null control (auth-state drift) ---")
    
    # Create fresh tokens RIGHT NOW for the null control test.
    # fresh token: issued now, exp=3600s (3600s remaining)
    fresh_token = create_token("reader", "reader", exp_seconds=3600, iat_offset=0)
    # near-expiry token: issued now-3570s, exp=now+30 (30s remaining)
    # Both tokens have identical JWT claims (same sub, same iat-adjusted exp semantics)
    # 30s remaining provides sufficient window for N=20 paired observations (~6-10s)
    near_expiry_token = create_token("reader", "reader", exp_seconds=3600, iat_offset=3570)
    
    # Decode to verify (without expiry validation for near-expiry)
    fresh_payload = jwt.decode(fresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    near_expiry_payload = jwt.decode(near_expiry_token, JWT_SECRET, algorithms=[JWT_ALGORITHM],
                                     options={"verify_exp": False})
    print(f"  Fresh token: iat={fresh_payload['iat']}, exp={fresh_payload['exp']}, "
          f"remaining={fresh_payload['exp'] - int(datetime.now(timezone.utc).timestamp())}s")
    print(f"  Near-expiry token: iat={near_expiry_payload['iat']}, exp={near_expiry_payload['exp']}, "
          f"remaining={near_expiry_payload['exp'] - int(datetime.now(timezone.utc).timestamp())}s")
    
    # Ensure fresh token has an active session
    create_session(fresh_token, "reader")
    create_session(near_expiry_token, "reader")
    
    null_fresh_fp = set()
    null_near_expiry_fp = set()
    null_observations = []
    for i in range(N_SAMPLES):
        jitter = random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0
        time.sleep(jitter)
        
        obs_fresh = observe_response("/protected", fresh_token)
        fp_fresh = compute_fingerprint(obs_fresh, "full")
        null_fresh_fp.add(fp_fresh)
        
        jitter2 = random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0
        time.sleep(jitter2)
        
        obs_near = observe_response("/protected", near_expiry_token)
        fp_near = compute_fingerprint(obs_near, "full")
        null_near_expiry_fp.add(fp_near)
        
        null_observations.append({
            "index": i,
            "fresh_status": obs_fresh["status"],
            "fresh_fingerprint": fp_fresh,
            "near_status": obs_near["status"],
            "near_fingerprint": fp_near,
            "fresh_body_len": len(obs_fresh["body_bytes"]),
            "near_body_len": len(obs_near["body_bytes"]),
        })
        
    print(f"  Fresh unique fingerprints: {len(null_fresh_fp)}")
    print(f"  Near-expiry unique fingerprints: {len(null_near_expiry_fp)}")
    
    # Verify fresh token is still valid (near-expiry may have expired during observations)
    assert jwt.decode(fresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM]) is not None
    print("  Fresh token passes JWT validation: OK")
    # Note: near-expiry token may have expired during the observation window.
    # This is expected — the null control tests both tokens while BOTH are valid.
    # The server validates JWT expiry on each request, so if the near-expiry token
    # expires mid-test, the server returns 401 token_expired, which IS a different
    # response than the fresh token's 200 — this is the expected null control behavior:
    # fresh=near-expiry should produce identical responses while both are valid.
    
    # ─── Step 5: Compute discrimination metrics ──────────────────────────────
    print("\n--- Step 5: Computing discrimination metrics ---")
    
    metrics = {}
    
    # 5a: Permission escalation — full vector
    perm_disc, perm_ci_lo, perm_ci_hi = bootstrap_jaccard_ci(
        reader_admin_fp, valid_admin_fp)
    metrics["permission_escalation_full"] = {
        "discrimination": perm_disc,
        "ci_95_lower": perm_ci_lo,
        "ci_95_upper": perm_ci_hi,
        "set_a_size": len(reader_admin_fp),
        "set_b_size": len(valid_admin_fp),
        "interpretation": "reader_admin vs valid_admin on /admin"
    }
    print(f"  Permission escalation (full): {perm_disc:.4f} "
          f"[{perm_ci_lo:.4f}, {perm_ci_hi:.4f}]")
    
    # 5b: Session invalidation — full vector
    sess_disc, sess_ci_lo, sess_ci_hi = bootstrap_jaccard_ci(
        valid_reader_fp, session_killed_fp)
    metrics["session_invalidation_full"] = {
        "discrimination": sess_disc,
        "ci_95_lower": sess_ci_lo,
        "ci_95_upper": sess_ci_hi,
        "set_a_size": len(valid_reader_fp),
        "set_b_size": len(session_killed_fp),
        "interpretation": "valid_reader vs session_killed on /protected"
    }
    print(f"  Session invalidation (full): {sess_disc:.4f} "
          f"[{sess_ci_lo:.4f}, {sess_ci_hi:.4f}]")
    
    # 5c: Null control — full vector (fresh vs near-expiry)
    null_disc, null_ci_lo, null_ci_hi = bootstrap_jaccard_ci(
        null_fresh_fp, null_near_expiry_fp)
    metrics["null_control_full"] = {
        "discrimination": null_disc,
        "ci_95_lower": null_ci_lo,
        "ci_95_upper": null_ci_hi,
        "set_a_size": len(null_fresh_fp),
        "set_b_size": len(null_near_expiry_fp),
        "interpretation": "fresh vs near-expiry token on /protected"
    }
    print(f"  Null control (full): {null_disc:.4f} "
          f"[{null_ci_lo:.4f}, {null_ci_hi:.4f}]")
    
    # 5d: Baselines — STATUS-ONLY
    reader_admin_status_fps = set()
    admin_status_fps = set()
    for i in range(N_SAMPLES):
        # Re-observe for baseline computation (reuse existing observations)
        reader_admin_status_fps.add(compute_fingerprint(reader_admin_observations[i] if i < len(reader_admin_observations) else {"status": 403, "body": "", "headers": {}}, "status"))
        admin_status_fps.add(compute_fingerprint(valid_admin_observations[i] if i < len(valid_admin_observations) else {"status": 200, "body": "", "headers": {}}, "status"))
    
    # Actually, we need to recompute from the raw observations
    # Recompute fingerprints from stored observations
    reader_admin_status_set = set()
    admin_status_set = set()
    for obs in reader_admin_observations:
        reader_admin_status_set.add(str(obs["status"]))
    for obs in valid_admin_observations:
        admin_status_set.add(str(obs["status"]))
    
    metrics["baseline_status_only_permission"] = {
        "discrimination": jaccard_distance(reader_admin_status_set, admin_status_set),
        "set_a_statuses": list(reader_admin_status_set),
        "set_b_statuses": list(admin_status_set),
    }
    print(f"  B-STATUS-ONLY (permission): {metrics['baseline_status_only_permission']['discrimination']:.4f}")
    
    # B-STATUS-ONLY for session invalidation
    valid_reader_status_set = set()
    session_killed_status_set = set()
    for obs in valid_reader_observations:
        valid_reader_status_set.add(str(obs["status"]))
    for obs in session_killed_observations:
        session_killed_status_set.add(str(obs["status"]))
    
    metrics["baseline_status_only_session"] = {
        "discrimination": jaccard_distance(valid_reader_status_set, session_killed_status_set),
        "set_a_statuses": list(valid_reader_status_set),
        "set_b_statuses": list(session_killed_status_set),
    }
    print(f"  B-STATUS-ONLY (session): {metrics['baseline_status_only_session']['discrimination']:.4f}")
    
    # B-BODY-ONLY for permission escalation
    reader_admin_body_set = set()
    admin_body_set = set()
    for obs in reader_admin_observations:
        reader_admin_body_set.add(obs["body_hash"])
    for obs in valid_admin_observations:
        admin_body_set.add(obs["body_hash"])
    
    metrics["baseline_body_only_permission"] = {
        "discrimination": jaccard_distance(reader_admin_body_set, admin_body_set),
        "set_a_unique_bodies": len(reader_admin_body_set),
        "set_b_unique_bodies": len(admin_body_set),
    }
    print(f"  B-BODY-ONLY (permission): {metrics['baseline_body_only_permission']['discrimination']:.4f}")
    
    # B-BODY-ONLY for session invalidation
    valid_reader_body_set = set()
    session_killed_body_set = set()
    for obs in valid_reader_observations:
        valid_reader_body_set.add(obs["body_hash"])
    for obs in session_killed_observations:
        session_killed_body_set.add(obs["body_hash"])
    
    metrics["baseline_body_only_session"] = {
        "discrimination": jaccard_distance(valid_reader_body_set, session_killed_body_set),
        "set_a_unique_bodies": len(valid_reader_body_set),
        "set_b_unique_bodies": len(session_killed_body_set),
    }
    print(f"  B-BODY-ONLY (session): {metrics['baseline_body_only_session']['discrimination']:.4f}")
    
    # B-HEADERS-ONLY for permission escalation
    reader_admin_hdr_set = set()
    admin_hdr_set = set()
    for obs in reader_admin_observations:
        reader_admin_hdr_set.add(obs["headers_json"])
    for obs in valid_admin_observations:
        admin_hdr_set.add(obs["headers_json"])
    
    metrics["baseline_headers_only_permission"] = {
        "discrimination": jaccard_distance(reader_admin_hdr_set, admin_hdr_set),
        "set_a_unique_headers": len(reader_admin_hdr_set),
        "set_b_unique_headers": len(admin_hdr_set),
    }
    print(f"  B-HEADERS-ONLY (permission): {metrics['baseline_headers_only_permission']['discrimination']:.4f}")
    
    # B-HEADERS-ONLY for session invalidation
    valid_reader_hdr_set = set()
    session_killed_hdr_set = set()
    for obs in valid_reader_observations:
        valid_reader_hdr_set.add(obs["headers_json"])
    for obs in session_killed_observations:
        session_killed_hdr_set.add(obs["headers_json"])
    
    metrics["baseline_headers_only_session"] = {
        "discrimination": jaccard_distance(valid_reader_hdr_set, session_killed_hdr_set),
        "set_a_unique_headers": len(valid_reader_hdr_set),
        "set_b_unique_headers": len(session_killed_hdr_set),
    }
    print(f"  B-HEADERS-ONLY (session): {metrics['baseline_headers_only_session']['discrimination']:.4f}")
    
    # 5e: Check full vector exceeds max(baseline) for at least one condition
    perm_max_baseline = max(
        metrics["baseline_status_only_permission"]["discrimination"],
        metrics["baseline_body_only_permission"]["discrimination"]
    )
    sess_max_baseline = max(
        metrics["baseline_status_only_session"]["discrimination"],
        metrics["baseline_body_only_session"]["discrimination"]
    )
    
    metrics["full_exceeds_status_check"] = {
        "permission_full_vector": perm_disc,
        "permission_max_baseline": perm_max_baseline,
        "permission_exceeds": perm_disc >= perm_max_baseline,
        "session_full_vector": sess_disc,
        "session_max_baseline": sess_max_baseline,
        "session_exceeds": sess_disc >= sess_max_baseline,
        "either_exceeds": perm_disc >= perm_max_baseline or sess_disc >= sess_max_baseline,
    }
    print(f"  C4 full_exceeds_status: permission={perm_disc >= perm_max_baseline}, "
          f"session={sess_disc >= sess_max_baseline}")
    
    # ─── Step 6: Evaluate decision rule ──────────────────────────────────────
    print("\n--- Step 6: Decision Rule Evaluation ---")
    
    c1_permission_disc = perm_disc > 0.5
    c2_session_disc = sess_disc > 0.5
    c3_null_body = null_disc == 0.0 and null_ci_lo <= 0.0 <= null_ci_hi
    c4_full_exceeds = metrics["full_exceeds_status_check"]["either_exceeds"]
    c5_null_upper = null_disc <= 0.05
    
    conditions = {
        "C1_PERMISSION_DISC": {
            "pass": c1_permission_disc,
            "value": perm_disc,
            "threshold": "> 0.5",
        },
        "C2_SESSION_DISC": {
            "pass": c2_session_disc,
            "value": sess_disc,
            "threshold": "> 0.5",
        },
        "C3_NULL_BODY": {
            "pass": c3_null_body,
            "value": null_disc,
            "ci": [null_ci_lo, null_ci_hi],
            "threshold": "= 0.0, CI contains 0.0",
        },
        "C4_FULL_EXCEEDS_STATUS": {
            "pass": c4_full_exceeds,
            "permission_disc": perm_disc,
            "permission_max_baseline": perm_max_baseline,
            "session_disc": sess_disc,
            "session_max_baseline": sess_max_baseline,
            "threshold": ">= max(B-STATUS-ONLY, B-BODY-ONLY) on at least one condition",
        },
        "C5_NULL_CONTROL_PASS": {
            "pass": c5_null_upper,
            "value": null_disc,
            "threshold": "<= 0.05",
        },
    }
    
    for name, cond in conditions.items():
        status = "PASS" if cond["pass"] else "FAIL"
        print(f"  {name}: {status} (value={cond.get('value', 'N/A')}, threshold={cond['threshold']})")
    
    all_pass = all(c["pass"] for c in conditions.values())
    print(f"\n  Overall: {'SUPPORTS' if all_pass else 'FALSIFIED-IN-SETTING'}")
    
    # ─── Step 7: Package results ─────────────────────────────────────────────
    print("\n--- Step 7: Packaging results ---")
    
    # Save raw observations to JSONL
    raw_path = Path("raw_observations.jsonl")
    with open(raw_path, "w") as f:
        for obs in no_auth_observations:
            f.write(json.dumps({"state": "no_auth", **obs}) + "\n")
        for obs in valid_reader_observations:
            f.write(json.dumps({"state": "valid_reader", **obs}) + "\n")
        for obs in reader_admin_observations:
            f.write(json.dumps({"state": "reader_admin_403", **obs}) + "\n")
        for obs in valid_admin_observations:
            f.write(json.dumps({"state": "valid_admin_200", **obs}) + "\n")
        for obs in session_killed_observations:
            f.write(json.dumps({"state": "session_killed", **obs}) + "\n")
        for obs in null_observations:
            f.write(json.dumps({"state": "null_control", **obs}) + "\n")
    
    print(f"[OK] Raw observations saved to {raw_path}")
    
    return {
        "metrics": metrics,
        "conditions": conditions,
        "all_pass": all_pass,
        "fingerprints": {
            "no_auth": list(no_auth_fp),
            "valid_reader": list(valid_reader_fp),
            "reader_admin_403": list(reader_admin_fp),
            "valid_admin_200": list(valid_admin_fp),
            "session_killed": list(session_killed_fp),
            "null_fresh": list(null_fresh_fp),
            "null_near_expiry": list(null_near_expiry_fp),
        },
        "observations": {
            "no_auth": no_auth_observations,
            "valid_reader": valid_reader_observations,
            "reader_admin_403": reader_admin_observations,
            "valid_admin_200": valid_admin_observations,
            "session_killed": session_killed_observations,
            "null_control": null_observations,
        },
    }


if __name__ == "__main__":
    result = run_experiment()
    if result:
        # Save full result for downstream processing
        with open("experiment_result.json", "w") as f:
            json.dump(result, f, indent=2, default=str)
        print("\n[DONE] Experiment complete.")
    else:
        print("\n[FAIL] Experiment failed.")
        sys.exit(1)
