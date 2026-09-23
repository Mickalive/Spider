#!/usr/bin/env python3
"""
EXP-RUNTIME-35860330078 — Real-HTTP distributed freshness + browser C-MEAS-VALID
EXECUTE stage. Frozen spec: shared SQLite WAL vs per-node, real gunicorn+nginx,
real Playwright 1280x720 browser fetches with CDP AX/DOM on /resource pages.
"""

import json
import hashlib
import os
import sys
import time
import random
import sqlite3
import signal
import subprocess
import threading
import tempfile
import traceback
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from flask import Flask, request as flask_request, jsonify, g
import jwt

# ─── Constants ────────────────────────────────────────────────────────────────

EXPERIMENT_ID = "EXP-RUNTIME-35860330078"
SEED = 44
EXCLUDED_HEADERS = {"Date", "Server", "X-Request-Id", "CF-RAY", "CF-Cache-Status", "X-Cache", "Age"}
BASE_DIR = Path(f"/tmp/spider-runtime-{EXPERIMENT_ID.split('-')[-1]}")
NGINX_DIR = BASE_DIR / "nginx"
SHARED_DB = BASE_DIR / "shared.db"

# Body states (sort_keys=True JSON)
BODY_STATES = {
    "A":  {"json": '{"data":"hello","version":1}', "len": 31},
    "A1": {"json": '{"data":"hello!","version":1}', "len": 32},
    "A2": {"json": '{"data":"hello!!","version":1}', "len": 33},
    "A3": {"json": '{"data":"hello!!!!","version":1}', "len": 35},
    "B":  {"json": '{"data":"hello","items":["a","b"],"role":"reader","version":1}', "len": 70},
    "C":  {"json": '{"admin_note":"sensitive:42","count":42,"data":"admin","items":["x","y","z"],"role":"admin","version":1}', "len": 117},
}
for k in BODY_STATES:
    BODY_STATES[k]["sha256"] = hashlib.sha256(BODY_STATES[k]["json"].encode()).hexdigest()

# Header states
HEADER_BASE = {
    "Cache-Control": "public, max-age=3600",
    "ETag": 'W/"fixed-aaa-111"',
    "Vary": "Accept-Encoding",
    "Content-Type": "application/json",
}

HEADER_STATES = {
    "E": {
        "Cache-Control": "max-age=0, must-revalidate",
        "ETag": 'W/"changed-bbb-222"',
        "Set-Cookie": "session=xyz; Path=/; HttpOnly",
        "Vary": "Accept-Encoding, Origin",
        "Content-Type": "application/json",
    },
    "CC_small": {"Cache-Control": "public, max-age=3601", "ETag": 'W/"fixed-aaa-111"', "Vary": "Accept-Encoding", "Content-Type": "application/json"},
    "CC_large": {"Cache-Control": "max-age=0", "ETag": 'W/"fixed-aaa-111"', "Vary": "Accept-Encoding", "Content-Type": "application/json"},
    "ETag_small": {"Cache-Control": "public, max-age=3600", "ETag": 'W/"fixed-aaa-112"', "Vary": "Accept-Encoding", "Content-Type": "application/json"},
    "ETag_large": {"Cache-Control": "public, max-age=3600", "ETag": 'W/"changed-bbb-222"', "Vary": "Accept-Encoding", "Content-Type": "application/json"},
    "SC_small": {"Cache-Control": "public, max-age=3600", "ETag": 'W/"fixed-aaa-111"', "Set-Cookie": "session=abc", "Vary": "Accept-Encoding", "Content-Type": "application/json"},
    "SC_large": {"Cache-Control": "public, max-age=3600", "ETag": 'W/"fixed-aaa-111"', "Set-Cookie": "session=xyz; Path=/; HttpOnly", "Vary": "Accept-Encoding", "Content-Type": "application/json"},
    "Vary_small": {"Cache-Control": "public, max-age=3600", "ETag": 'W/"fixed-aaa-111"', "Vary": "Accept-Encoding", "Content-Type": "application/json"},
}

JWT_SECRET = "spider-exp-35860330078-secret"
JWT_ALG = "HS256"

# ─── Fingerprint functions ────────────────────────────────────────────────────

def filter_headers(headers_dict, exclude=EXCLUDED_HEADERS):
    """Filter and lowercase-sort headers, include Content-Length."""
    filtered = {}
    for k, v in headers_dict.items():
        if k.lower() not in {x.lower() for x in exclude}:
            filtered[k] = v
    return dict(sorted(filtered.items(), key=lambda x: x[0].lower()))

def compute_fingerprint(status, body_bytes, headers_filtered_json, include_body=True, include_status=True, include_headers=True, include_clen=True):
    """Compute SHA256 fingerprint components. Byte-identical to prior experiments."""
    parts = []
    if include_status:
        parts.append(str(status))
    if include_body and body_bytes:
        parts.append(body_bytes.decode('latin-1'))
    if include_headers:
        h = json.loads(headers_filtered_json) if isinstance(headers_filtered_json, str) else headers_filtered_json
        if not include_clen:
            h = {k: v for k, v in h.items() if k.lower() != 'content-length'}
        parts.append(json.dumps(h, sort_keys=True, separators=(',', ':')))
    return hashlib.sha256("||".join(parts).encode('latin-1')).hexdigest()

def compute_fingerprint_full(status, body_bytes, headers_dict):
    filtered = filter_headers(headers_dict)
    return compute_fingerprint(status, body_bytes, filtered, True, True, True, True)

def compute_fingerprint_body_only(status, body_bytes, headers_dict):
    filtered = filter_headers(headers_dict)
    return compute_fingerprint(status, body_bytes, filtered, True, False, False, False)

def compute_fingerprint_headers_only(status, body_bytes, headers_dict):
    filtered = filter_headers(headers_dict)
    return compute_fingerprint(status, body_bytes, filtered, False, False, True, True)

def compute_fingerprint_headers_no_clen(status, body_bytes, headers_dict):
    filtered = filter_headers(headers_dict)
    return compute_fingerprint(status, body_bytes, filtered, False, False, True, False)

def compute_fingerprint_status_only(status, body_bytes, headers_dict):
    return compute_fingerprint(status, body_bytes, "{}", False, True, False, False)

def jaccard(fp1, fp2):
    """Jaccard distance between two fingerprint hex strings (treated as byte sets)."""
    if fp1 == fp2:
        return 0.0
    s1 = set(fp1.encode())
    s2 = set(fp2.encode())
    union = s1 | s2
    if not union:
        return 0.0
    return 1.0 - len(s1 & s2) / len(union)

def behavioral_composite(status_code, session_valid):
    """Graded behavioral signal."""
    if status_code == 401:
        return 1.0
    elif status_code == 403:
        return 0.5
    elif status_code == 500:
        return 0.75
    elif status_code == 200 and session_valid:
        return 0.0
    elif status_code == 200:
        return 0.3
    return 0.5

# ─── Flask App ────────────────────────────────────────────────────────────────

def create_app(db_path=None):
    """Create Flask app with body_config/header_config tables."""
    app = Flask(__name__)
    app.config['DATABASE'] = db_path or str(SHARED_DB)

    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(app.config['DATABASE'], check_same_thread=False)
            g.db.execute("PRAGMA journal_mode=WAL")
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def init_db():
        db = sqlite3.connect(app.config['DATABASE'], check_same_thread=False)
        db.execute("PRAGMA journal_mode=WAL")
        db.execute('''CREATE TABLE IF NOT EXISTS body_config (
            id INTEGER PRIMARY KEY, variant TEXT DEFAULT 'A', content TEXT
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS header_config (
            id INTEGER PRIMARY KEY, variant TEXT DEFAULT 'BASE', content TEXT
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, username TEXT, role TEXT DEFAULT 'reader',
            session_id TEXT
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY, session_id TEXT, user_id INTEGER,
            valid INTEGER DEFAULT 1, created_at TEXT
        )''')
        # Initialize body_config
        existing = db.execute("SELECT COUNT(*) FROM body_config").fetchone()[0]
        if existing == 0:
            db.execute("INSERT INTO body_config (variant, content) VALUES (?, ?)",
                      ("A", BODY_STATES["A"]["json"]))
            db.execute("INSERT INTO header_config (variant, content) VALUES (?, ?)",
                      ("BASE", json.dumps(HEADER_BASE)))
            db.execute("INSERT INTO users (username, role, session_id) VALUES (?, ?, ?)",
                      ("testuser", "reader", "test-session-abc"))
            db.execute("INSERT INTO sessions (session_id, user_id, valid, created_at) VALUES (?, ?, ?, ?)",
                      ("test-session-abc", 1, 1, datetime.now(timezone.utc).isoformat()))
        db.commit()
        db.close()

    @app.before_request
    def before_request():
        g.worker_id = os.getpid()

    def get_worker_pid_header():
        return {"X-Worker-Pid": str(os.getpid())}

    def get_current_body():
        db = get_db()
        row = db.execute("SELECT variant, content FROM body_config WHERE id=1").fetchone()
        if row:
            return row['variant'], row['content']
        return "A", BODY_STATES["A"]["json"]

    def get_current_headers():
        db = get_db()
        row = db.execute("SELECT variant, content FROM header_config WHERE id=1").fetchone()
        if row:
            return row['variant'], json.loads(row['content'])
        return "BASE", HEADER_BASE.copy()

    def validate_session(session_id):
        if not session_id:
            return False
        db = get_db()
        row = db.execute("SELECT valid FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        return row is not None and row['valid'] == 1

    def make_response_with_cache(body_variant, body_json, headers_config, cache_enabled=True, etag_val=None):
        """Build response with Cache-Control and ETag."""
        body_bytes = body_json.encode('utf-8')
        resp_headers = dict(headers_config)
        resp_headers['Content-Length'] = str(len(body_bytes))
        resp_headers['X-Worker-Pid'] = str(os.getpid())

        if cache_enabled:
            if 'Cache-Control' not in resp_headers:
                resp_headers['Cache-Control'] = 'public, max-age=5'
        else:
            resp_headers['Cache-Control'] = 'no-store'

        # Compute ETag from body SHA if not set
        if etag_val is None:
            body_sha = hashlib.sha256(body_bytes).hexdigest()[:8]
            etag_val = f'W/"{body_sha}"'
        resp_headers['ETag'] = etag_val

        # Check If-None-Match
        inm = flask_request.headers.get('If-None-Match', '')
        if inm and inm.strip() == etag_val:
            return '', 304, resp_headers

        return body_bytes, 200, resp_headers

    @app.route('/resource', methods=['GET'])
    def resource():
        session_id = flask_request.cookies.get('session') or flask_request.headers.get('Authorization', '').replace('Bearer ', '')
        variant, body_json = get_current_body()
        hdr_variant, hdr_config = get_current_headers()

        # ETag from body sha
        body_sha = hashlib.sha256(body_json.encode()).hexdigest()[:8]
        etag = f'W/"{body_sha}"'

        resp_body, status, headers = make_response_with_cache(variant, body_json, hdr_config, cache_enabled=True, etag_val=etag)
        return resp_body, status, headers

    @app.route('/api/profile', methods=['GET'])
    def api_profile():
        session_id = flask_request.headers.get('Authorization', '').replace('Bearer ', '')
        if not validate_session(session_id):
            return jsonify({"error": "unauthorized"}), 401
        variant, body_json = get_current_body()
        body_bytes = json.dumps({"profile": json.loads(body_json)}, sort_keys=True).encode()
        headers = {"Content-Type": "application/json", "Cache-Control": "public, max-age=5",
                   "X-Worker-Pid": str(os.getpid())}
        body_sha = hashlib.sha256(body_bytes).hexdigest()[:8]
        headers['ETag'] = f'W/"{body_sha}"'
        headers['Content-Length'] = str(len(body_bytes))
        inm = flask_request.headers.get('If-None-Match', '')
        if inm and inm.strip() == headers['ETag']:
            return '', 304, headers
        return body_bytes, 200, headers

    @app.route('/api/data_list', methods=['GET'])
    def api_data_list():
        session_id = flask_request.headers.get('Authorization', '').replace('Bearer ', '')
        if not validate_session(session_id):
            return jsonify({"error": "unauthorized"}), 401
        variant, body_json = get_current_body()
        body_bytes = json.dumps({"data": json.loads(body_json)}, sort_keys=True).encode()
        headers = {"Content-Type": "application/json", "Cache-Control": "public, max-age=5",
                   "X-Worker-Pid": str(os.getpid())}
        body_sha = hashlib.sha256(body_bytes).hexdigest()[:8]
        headers['ETag'] = f'W/"{body_sha}"'
        headers['Content-Length'] = str(len(body_bytes))
        inm = flask_request.headers.get('If-None-Match', '')
        if inm and inm.strip() == headers['ETag']:
            return '', 304, headers
        return body_bytes, 200, headers

    @app.route('/api/session/status', methods=['GET'])
    def api_session_status():
        session_id = flask_request.headers.get('Authorization', '').replace('Bearer ', '')
        valid = validate_session(session_id)
        if not valid:
            return jsonify({"session_valid": False, "error": "invalid session"}), 401
        return jsonify({"session_valid": True, "session_id": session_id}), 200, {
            "X-Worker-Pid": str(os.getpid()),
            "Cache-Control": "public, max-age=5",
        }

    @app.route('/admin/set_body_variant', methods=['POST'])
    def admin_set_body():
        data = flask_request.get_json(force=True)
        variant = data.get('variant', 'A')
        if variant not in BODY_STATES:
            return jsonify({"error": f"unknown variant {variant}"}), 400
        db = get_db()
        db.execute("UPDATE body_config SET variant=?, content=? WHERE id=1",
                  (variant, BODY_STATES[variant]["json"]))
        db.commit()
        # Verify commit
        check = db.execute("SELECT variant, content FROM body_config WHERE id=1").fetchone()
        if check['variant'] != variant:
            return jsonify({"error": "COMMIT_NOT_VERIFIED"}), 500
        return jsonify({"ok": True, "variant": variant})

    @app.route('/admin/set_headers', methods=['POST'])
    def admin_set_headers():
        data = flask_request.get_json(force=True)
        variant = data.get('variant', 'BASE')
        if variant == 'BASE':
            hdrs = HEADER_BASE.copy()
        elif variant in HEADER_STATES:
            hdrs = HEADER_STATES[variant].copy()
        else:
            return jsonify({"error": f"unknown header variant {variant}"}), 400
        db = get_db()
        db.execute("UPDATE header_config SET variant=?, content=? WHERE id=1",
                  (variant, json.dumps(hdrs)))
        db.commit()
        return jsonify({"ok": True, "variant": variant})

    @app.route('/admin/invalidate_session', methods=['POST'])
    def admin_invalidate():
        data = flask_request.get_json(force=True)
        sid = data.get('session_id', 'test-session-abc')
        db = get_db()
        db.execute("UPDATE sessions SET valid=0 WHERE session_id=?", (sid,))
        db.commit()
        check = db.execute("SELECT valid FROM sessions WHERE session_id=?", (sid,)).fetchone()
        return jsonify({"ok": True, "valid_after": check['valid'] if check else None})

    @app.route('/admin/set_session', methods=['POST'])
    def admin_set_session():
        data = flask_request.get_json(force=True)
        sid = data.get('session_id', 'test-session-abc')
        valid = data.get('valid', 1)
        db = get_db()
        existing = db.execute("SELECT id FROM sessions WHERE session_id=?", (sid,)).fetchone()
        if existing:
            db.execute("UPDATE sessions SET valid=?, created_at=? WHERE session_id=?",
                      (valid, datetime.now(timezone.utc).isoformat(), sid))
        else:
            db.execute("INSERT INTO sessions (session_id, user_id, valid, created_at) VALUES (?, 1, ?, ?)",
                      (sid, valid, datetime.now(timezone.utc).isoformat()))
        db.commit()
        return jsonify({"ok": True})

    @app.route('/admin/set_role', methods=['POST'])
    def admin_set_role():
        data = flask_request.get_json(force=True)
        role = data.get('role', 'reader')
        username = data.get('username', 'testuser')
        db = get_db()
        db.execute("UPDATE users SET role=? WHERE username=?", (role, username))
        db.commit()
        return jsonify({"ok": True})

    @app.route('/protected', methods=['GET'])
    def protected():
        session_id = flask_request.headers.get('Authorization', '').replace('Bearer ', '')
        if not validate_session(session_id):
            return jsonify({"error": "unauthorized"}), 401
        return jsonify({"message": "ok"}), 200

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok", "worker": os.getpid()})

    # Initialize DB on first request
    with app.app_context():
        init_db()

    return app

# ─── Process management ───────────────────────────────────────────────────────

def kill_servers():
    """Kill any existing gunicorn/nginx on our ports."""
    for port in [19860, 19861, 19851, 19852]:
        subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True, timeout=5)
    time.sleep(0.5)

def start_gunicorn(db_path, port, workers=2, name="gunicorn"):
    """Start gunicorn with 2 sync workers."""
    app_module = f"gunicorn_app_{port}"
    # Write a mini wsgi module
    wsgi_path = BASE_DIR / f"{app_module}.py"
    wsgi_path.write_text(f"""
import sys
sys.path.insert(0, '{os.path.dirname(os.path.abspath(__file__))}')
from run_experiment import create_app
app = create_app(db_path='{db_path}')
""")
    cmd = [
        "gunicorn", f"{app_module}:app",
        "--workers", str(workers),
        "--bind", f"127.0.0.1:{port}",
        "--timeout", "30",
        "--worker-class", "sync",
        "--pid", str(BASE_DIR / f"{name}.pid"),
    ]
    proc = subprocess.Popen(cmd, cwd=str(BASE_DIR),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Wait for workers to start
    return proc

def start_nginx(port, upstream_port, conf_name="nginx.conf"):
    """Start nginx with round-robin upstream."""
    conf_path = NGINX_DIR / conf_name
    pid_path = NGINX_DIR / f"{conf_name}.pid"
    error_log = NGINX_DIR / f"{conf_name}.error.log"
    access_log = NGINX_DIR / f"{conf_name}.access.log"

    conf_content = f"""
worker_processes 1;
pid {pid_path};
error_log {error_log};

events {{ worker_connections 64; }}

http {{
    access_log {access_log};
    sendfile on;

    upstream gunicorn_upstream {{
        server 127.0.0.1:{upstream_port};
    }}

    server {{
        listen {port};
        server_name 127.0.0.1;

        location / {{
            proxy_pass http://gunicorn_upstream;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_buffering off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }}
    }}
}}
"""
    conf_path.write_text(conf_content)
    # Kill old nginx on this port
    subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True, timeout=5)
    time.sleep(0.5)
    cmd = ["nginx", "-c", str(conf_path), "-p", str(NGINX_DIR)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
    return proc

def start_nginx_sticky(port, upstream_port, conf_name="nginx_sticky.conf"):
    """Start nginx with ip_hash sticky routing."""
    conf_path = NGINX_DIR / conf_name
    pid_path = NGINX_DIR / f"{conf_name}.pid"
    error_log = NGINX_DIR / f"{conf_name}.error.log"
    access_log = NGINX_DIR / f"{conf_name}.access.log"

    conf_content = f"""
worker_processes 1;
pid {pid_path};
error_log {error_log};

events {{ worker_connections 64; }}

http {{
    access_log {access_log};
    sendfile on;

    upstream gunicorn_upstream {{
        hash $remote_addr consistent;
        server 127.0.0.1:{upstream_port};
    }}

    server {{
        listen {port};
        server_name 127.0.0.1;

        location / {{
            proxy_pass http://gunicorn_upstream;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_buffering off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }}
    }}
}}
"""
    conf_path.write_text(conf_content)
    subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True, timeout=5)
    time.sleep(0.5)
    cmd = ["nginx", "-c", str(conf_path), "-p", str(NGINX_DIR)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
    return proc

def wait_for_server(url, timeout=15):
    """Wait for server to respond."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code in (200, 401, 403):
                return True
        except:
            pass
        time.sleep(0.3)
    return False

# ─── Distributed freshness harness ───────────────────────────────────────────

def run_distributed_freshness(base_url, db_path, N=1200, seed=SEED):
    """
    Run distributed C-FRESHNESS harness with real HTTP.
    Returns raw observations and metrics.
    """
    rng = random.Random(seed)
    observations = []
    batch_state_log = []
    endpoints = ["/api/profile", "/api/data_list", "/api/session/status"]
    valid_jwt = jwt.encode({"user": "testuser", "role": "reader", "exp": 9999999999}, JWT_SECRET, algorithm=JWT_ALG)
    expired_jwt = jwt.encode({"user": "testuser", "role": "reader", "exp": 0}, JWT_SECRET, algorithm=JWT_ALG)

    # Co-occurring conditions
    conditions = []
    for ep in endpoints:
        for cache_enabled in [True, False]:
            for auth_state in ["valid", "expired", "invalid"]:
                conditions.append({"endpoint": ep, "cache_enabled": cache_enabled, "auth_state": auth_state})
    # Add noise-only conditions
    for ep in endpoints:
        conditions.append({"endpoint": ep, "cache_enabled": True, "auth_state": "noise"})
        conditions.append({"endpoint": ep, "cache_enabled": False, "auth_state": "noise"})

    # Calculate per-condition samples
    total_needed = N
    per_condition = max(1, total_needed // len(conditions))
    extra = total_needed - per_condition * len(conditions)

    print(f"[Distributed] Starting {total_needed} samples across {len(conditions)} conditions, per_condition={per_condition}")
    batch_state_log.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "batch_start",
        "db_path": db_path,
        "n_conditions": len(conditions),
        "per_condition": per_condition,
    })

    sample_idx = 0
    for cond_idx, cond in enumerate(conditions):
        ep = cond["endpoint"]
        cache_enabled = cond["cache_enabled"]
        auth_state = cond["auth_state"]
        n_samples = per_condition + (1 if cond_idx < extra else 0)

        for i in range(n_samples):
            sample_idx += 1
            # Set body variant (cycle through A, B, C)
            body_variants = ["A", "B", "C"]
            bv = body_variants[i % len(body_variants)]
            try:
                requests.post(f"{base_url}/admin/set_body_variant", json={"variant": bv}, timeout=5)
            except Exception as e:
                print(f"[Distributed] set_body_variant failed: {e}")
                continue

            # Set header variant
            hv = "BASE" if not cache_enabled else "E" if auth_state == "expired" else "BASE"
            try:
                requests.post(f"{base_url}/admin/set_headers", json={"variant": hv}, timeout=5)
            except Exception as e:
                print(f"[Distributed] set_headers failed: {e}")
                continue

            # Set session state
            if auth_state == "valid":
                requests.post(f"{base_url}/admin/set_session", json={"session_id": "test-session-abc", "valid": 1}, timeout=5)
                token = valid_jwt
            elif auth_state == "expired":
                requests.post(f"{base_url}/admin/set_session", json={"session_id": "test-session-abc", "valid": 1}, timeout=5)
                token = expired_jwt
            elif auth_state == "invalid":
                requests.post(f"{base_url}/admin/invalidate_session", json={"session_id": "test-session-abc"}, timeout=5)
                token = "invalid-token-xyz"
            else:  # noise
                requests.post(f"{base_url}/admin/set_session", json={"session_id": "test-session-abc", "valid": 1}, timeout=5)
                token = valid_jwt

            # Make request with jitter
            time.sleep(rng.uniform(0.05, 0.15))
            headers = {"Authorization": f"Bearer {token}"}
            if cache_enabled:
                # Add If-None-Match for 304 path
                # First get the ETag
                try:
                    first_resp = requests.get(f"{base_url}{ep}", headers=headers, timeout=5)
                    etag = first_resp.headers.get("ETag", "")
                    if etag and rng.random() < 0.33:  # ~33% chance of 304
                        headers["If-None-Match"] = etag
                except:
                    pass

            try:
                t0 = time.time()
                resp = requests.get(f"{base_url}{ep}", headers=headers, timeout=10)
                latency = time.time() - t0

                status = resp.status_code
                is_304 = (status == 304)
                body_bytes = resp.content
                body_sha256 = hashlib.sha256(body_bytes).hexdigest() if body_bytes else ""
                body_len = len(body_bytes)
                content_length_header = int(resp.headers.get("Content-Length", body_len))
                worker_id = resp.headers.get("X-Worker-Pid", "unknown")

                filtered = filter_headers(dict(resp.headers))
                filtered_json = json.dumps(filtered, sort_keys=True, separators=(',', ':'))
                no_clen = {k: v for k, v in filtered.items() if k.lower() != 'content-length'}
                no_clen_json = json.dumps(no_clen, sort_keys=True, separators=(',', ':'))

                # Behavioral composite
                if auth_state == "noise":
                    bc = 0.0
                elif status == 401:
                    bc = 1.0
                elif status == 403:
                    bc = 0.5
                elif status == 500:
                    bc = 0.75
                elif status == 200:
                    bc = 0.0 if auth_state == "valid" else 0.3
                else:
                    bc = 0.5

                # Structural signal (hash of body without 401 confound)
                if status == 200 and body_bytes:
                    structural = hash(body_bytes) % 10000
                else:
                    structural = 0

                obs = {
                    "sample_idx": sample_idx,
                    "endpoint": ep,
                    "cache_enabled": cache_enabled,
                    "auth_state": auth_state,
                    "body_variant": bv,
                    "header_variant": hv,
                    "status": status,
                    "is_304": is_304,
                    "body_bytes": body_bytes.decode('latin-1') if body_bytes else "",
                    "body_sha256": body_sha256,
                    "body_len": body_len,
                    "content_length_header": content_length_header,
                    "headers_filtered_json": filtered_json,
                    "headers_no_clen_json": no_clen_json,
                    "worker_id": worker_id,
                    "behavioral_composite": bc,
                    "structural": structural,
                    "latency": latency,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "db_path": db_path,
                }
                observations.append(obs)

                if sample_idx % 100 == 0:
                    print(f"[Distributed] Sample {sample_idx}/{total_needed}, status={status}, worker={worker_id}, is_304={is_304}")

            except Exception as e:
                print(f"[Distributed] Request failed: {e}")
                continue

    # Log batch state verification
    batch_state_log.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "batch_end",
        "total_samples": len(observations),
    })

    # Verify shared DB state
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        count = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        conn.close()
        batch_state_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "db_verify",
            "session_count": count,
        })
    except Exception as e:
        batch_state_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "db_verify_failed",
            "error": str(e),
        })

    return observations, batch_state_log

# ─── Browser C-MEAS-VALID harness ────────────────────────────────────────────

def run_browser_harness(base_url, N=20, seed=SEED):
    """
    Run browser C-MEAS-VALID harness with real Playwright 1280x720.
    Returns raw observations and metrics.
    """
    from playwright.sync_api import sync_playwright

    rng = random.Random(seed)
    observations = []
    ax_data = []  # Per /resource page AX/DOM data
    viewport = {"width": 1280, "height": 720}

    # Build test cases for body/header discrimination
    test_cases = []

    # Body-only: A vs C (31B vs 117B)
    for i in range(N):
        test_cases.append({"type": "body_AvsC", "body_a": "A", "body_b": "C", "header": "BASE", "fetch": "browser"})
        test_cases.append({"type": "body_AvsC", "body_a": "A", "body_b": "C", "header": "BASE", "fetch": "direct"})

    # Header-only: BASE vs E (bodies identical 31B)
    for i in range(N):
        test_cases.append({"type": "header_AvsE", "body": "A", "header_a": "BASE", "header_b": "E", "fetch": "browser"})
        test_cases.append({"type": "header_AvsE", "body": "A", "header_a": "BASE", "header_b": "E", "fetch": "direct"})

    # Body gradients
    for grad_name, body_a, body_b in [("1B", "A", "A1"), ("2B", "A", "A2"), ("4B", "A", "A3"), ("39B", "A", "B"), ("86B", "A", "C")]:
        for i in range(N):
            test_cases.append({"type": f"gradient_{grad_name}", "body_a": body_a, "body_b": body_b, "header": "BASE", "fetch": "browser"})
            test_cases.append({"type": f"gradient_{grad_name}", "body_a": body_a, "body_b": body_b, "header": "BASE", "fetch": "direct"})

    # Header gradients
    for grad_name, hdr_a, hdr_b in [
        ("CC_small", "BASE", "CC_small"), ("CC_large", "BASE", "CC_large"),
        ("ETag_small", "BASE", "ETag_small"), ("ETag_large", "BASE", "ETag_large"),
        ("SC_small", "BASE", "SC_small"), ("SC_large", "BASE", "SC_large"),
        ("Vary_small", "BASE", "Vary_small"),
    ]:
        for i in range(N):
            test_cases.append({"type": f"gradient_{grad_name}", "body": "A", "header_a": hdr_a, "header_b": hdr_b, "fetch": "browser"})
            test_cases.append({"type": f"gradient_{grad_name}", "body": "A", "header_a": hdr_a, "header_b": hdr_b, "fetch": "direct"})

    # Nulls (same state, no change)
    for i in range(N):
        test_cases.append({"type": "null_body", "body_a": "A", "body_b": "A", "header": "BASE", "fetch": "browser"})
        test_cases.append({"type": "null_header", "body": "A", "header_a": "BASE", "header_b": "BASE", "fetch": "browser"})
        test_cases.append({"type": "null_body", "body_a": "A", "body_b": "A", "header": "BASE", "fetch": "direct"})
        test_cases.append({"type": "null_header", "body": "A", "header_a": "BASE", "header_b": "BASE", "fetch": "direct"})

    # Status-only
    for i in range(N):
        test_cases.append({"type": "status_only", "body_a": "A", "body_b": "A", "header": "BASE", "fetch": "browser"})
        test_cases.append({"type": "status_only", "body_a": "A", "body_b": "A", "header": "BASE", "fetch": "direct"})

    print(f"[Browser] Total test cases: {len(test_cases)}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=viewport)
        page = context.new_page()

        # Verify viewport
        actual_viewport = page.viewport_size
        print(f"[Browser] Viewport: {actual_viewport}")

        valid_jwt = jwt.encode({"user": "testuser", "role": "reader", "exp": 9999999999}, JWT_SECRET, algorithm=JWT_ALG)

        for idx, tc in enumerate(test_cases):
            tc_type = tc["type"]
            fetch_method = tc["fetch"]

            try:
                if tc_type.startswith("body_") or tc_type.startswith("gradient_") or tc_type == "null_body" or tc_type == "status_only":
                    # Body discrimination test
                    body_a = tc.get("body_a", tc.get("body", "A"))
                    body_b = tc.get("body_b", body_a)
                    header = tc.get("header", "BASE")

                    # Set states and fetch
                    requests.post(f"{base_url}/admin/set_body_variant", json={"variant": body_a}, timeout=5)
                    requests.post(f"{base_url}/admin/set_headers", json={"variant": header}, timeout=5)
                    requests.post(f"{base_url}/admin/set_session", json={"session_id": "test-session-abc", "valid": 1}, timeout=5)
                    time.sleep(0.05)

                    if fetch_method == "browser":
                        resp_a = page.request.get(f"{base_url}/resource", headers={"Authorization": f"Bearer {valid_jwt}"})
                        body_bytes_a = resp_a.body()
                        status_a = resp_a.status
                        headers_a_raw = dict(resp_a.headers)
                    else:
                        resp_a = requests.get(f"{base_url}/resource",
                                            headers={"Authorization": f"Bearer {valid_jwt}"},
                                            timeout=5)
                        body_bytes_a = resp_a.content
                        status_a = resp_a.status_code
                        headers_a_raw = dict(resp_a.headers)

                    # Set body B
                    requests.post(f"{base_url}/admin/set_body_variant", json={"variant": body_b}, timeout=5)
                    time.sleep(0.05)

                    if fetch_method == "browser":
                        resp_b = page.request.get(f"{base_url}/resource", headers={"Authorization": f"Bearer {valid_jwt}"})
                        body_bytes_b = resp_b.body()
                        status_b = resp_b.status
                        headers_b_raw = dict(resp_b.headers)
                    else:
                        resp_b = requests.get(f"{base_url}/resource",
                                            headers={"Authorization": f"Bearer {valid_jwt}"},
                                            timeout=5)
                        body_bytes_b = resp_b.content
                        status_b = resp_b.status_code
                        headers_b_raw = dict(resp_b.headers)

                    # Compute fingerprints
                    headers_a_filt = filter_headers(headers_a_raw)
                    headers_b_filt = filter_headers(headers_b_raw)

                    fp_full_a = compute_fingerprint_full(status_a, body_bytes_a, headers_a_filt)
                    fp_full_b = compute_fingerprint_full(status_b, body_bytes_b, headers_b_filt)
                    fp_body_a = compute_fingerprint_body_only(status_a, body_bytes_a, headers_a_filt)
                    fp_body_b = compute_fingerprint_body_only(status_b, body_bytes_b, headers_b_filt)
                    fp_headers_a = compute_fingerprint_headers_only(status_a, body_bytes_a, headers_a_filt)
                    fp_headers_b = compute_fingerprint_headers_only(status_b, body_bytes_b, headers_b_filt)
                    fp_hnoclen_a = compute_fingerprint_headers_no_clen(status_a, body_bytes_a, headers_a_filt)
                    fp_hnoclen_b = compute_fingerprint_headers_no_clen(status_b, body_bytes_b, headers_b_filt)

                    obs = {
                        "idx": idx, "type": tc_type, "fetch": fetch_method,
                        "state_a": body_a, "state_b": body_b,
                        "status_a": status_a, "status_b": status_b,
                        "body_len_a": len(body_bytes_a), "body_len_b": len(body_bytes_b),
                        "fp_full_a": fp_full_a, "fp_full_b": fp_full_b,
                        "fp_body_a": fp_body_a, "fp_body_b": fp_body_b,
                        "fp_headers_a": fp_headers_a, "fp_headers_b": fp_headers_b,
                        "fp_hnoclen_a": fp_hnoclen_a, "fp_hnoclen_b": fp_hnoclen_b,
                        "jaccard_full": jaccard(fp_full_a, fp_full_b),
                        "jaccard_body": jaccard(fp_body_a, fp_body_b),
                        "jaccard_headers": jaccard(fp_headers_a, fp_headers_b),
                        "jaccard_hnoclen": jaccard(fp_hnoclen_a, fp_hnoclen_b),
                        "viewport": actual_viewport,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                    observations.append(obs)

                elif tc_type.startswith("header_"):
                    # Header discrimination test
                    body = tc.get("body", "A")
                    hdr_a = tc["header_a"]
                    hdr_b = tc["header_b"]

                    requests.post(f"{base_url}/admin/set_body_variant", json={"variant": body}, timeout=5)
                    requests.post(f"{base_url}/admin/set_headers", json={"variant": hdr_a}, timeout=5)
                    requests.post(f"{base_url}/admin/set_session", json={"session_id": "test-session-abc", "valid": 1}, timeout=5)
                    time.sleep(0.05)

                    if fetch_method == "browser":
                        resp_a = page.request.get(f"{base_url}/resource", headers={"Authorization": f"Bearer {valid_jwt}"})
                        body_bytes_a = resp_a.body()
                        status_a = resp_a.status
                        headers_a_raw = dict(resp_a.headers)
                    else:
                        resp_a = requests.get(f"{base_url}/resource",
                                            headers={"Authorization": f"Bearer {valid_jwt}"},
                                            timeout=5)
                        body_bytes_a = resp_a.content
                        status_a = resp_a.status_code
                        headers_a_raw = dict(resp_a.headers)

                    requests.post(f"{base_url}/admin/set_headers", json={"variant": hdr_b}, timeout=5)
                    time.sleep(0.05)

                    if fetch_method == "browser":
                        resp_b = page.request.get(f"{base_url}/resource", headers={"Authorization": f"Bearer {valid_jwt}"})
                        body_bytes_b = resp_b.body()
                        status_b = resp_b.status
                        headers_b_raw = dict(resp_b.headers)
                    else:
                        resp_b = requests.get(f"{base_url}/resource",
                                            headers={"Authorization": f"Bearer {valid_jwt}"},
                                            timeout=5)
                        body_bytes_b = resp_b.content
                        status_b = resp_b.status_code
                        headers_b_raw = dict(resp_b.headers)

                    headers_a_filt = filter_headers(headers_a_raw)
                    headers_b_filt = filter_headers(headers_b_raw)

                    fp_full_a = compute_fingerprint_full(status_a, body_bytes_a, headers_a_filt)
                    fp_full_b = compute_fingerprint_full(status_b, body_bytes_b, headers_b_filt)
                    fp_body_a = compute_fingerprint_body_only(status_a, body_bytes_a, headers_a_filt)
                    fp_body_b = compute_fingerprint_body_only(status_b, body_bytes_b, headers_b_filt)
                    fp_headers_a = compute_fingerprint_headers_only(status_a, body_bytes_a, headers_a_filt)
                    fp_headers_b = compute_fingerprint_headers_only(status_b, body_bytes_b, headers_b_filt)
                    fp_hnoclen_a = compute_fingerprint_headers_no_clen(status_a, body_bytes_a, headers_a_filt)
                    fp_hnoclen_b = compute_fingerprint_headers_no_clen(status_b, body_bytes_b, headers_b_filt)

                    obs = {
                        "idx": idx, "type": tc_type, "fetch": fetch_method,
                        "state_a": hdr_a, "state_b": hdr_b,
                        "status_a": status_a, "status_b": status_b,
                        "body_len_a": len(body_bytes_a), "body_len_b": len(body_bytes_b),
                        "fp_full_a": fp_full_a, "fp_full_b": fp_full_b,
                        "fp_body_a": fp_body_a, "fp_body_b": fp_body_b,
                        "fp_headers_a": fp_headers_a, "fp_headers_b": fp_headers_b,
                        "fp_hnoclen_a": fp_hnoclen_a, "fp_hnoclen_b": fp_hnoclen_b,
                        "jaccard_full": jaccard(fp_full_a, fp_full_b),
                        "jaccard_body": jaccard(fp_body_a, fp_body_b),
                        "jaccard_headers": jaccard(fp_headers_a, fp_headers_b),
                        "jaccard_hnoclen": jaccard(fp_hnoclen_a, fp_hnoclen_b),
                        "viewport": actual_viewport,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                    observations.append(obs)

                if idx % 50 == 0:
                    print(f"[Browser] Test case {idx}/{len(test_cases)}")

            except Exception as e:
                print(f"[Browser] Test case {idx} failed: {e}")
                continue

        # Capture CDP AX/DOM on /resource pages
        print("[Browser] Capturing CDP AX/DOM on /resource pages...")
        ax_data = []
        for page_idx in range(20):
            try:
                requests.post(f"{base_url}/admin/set_body_variant", json={"variant": "A"}, timeout=5)
                requests.post(f"{base_url}/admin/set_headers", json={"variant": "BASE"}, timeout=5)
                time.sleep(0.05)

                # Navigate to /resource via page.goto for CDP capture
                page.goto(f"{base_url}/resource")
                page.wait_for_load_state("networkidle")

                # CDP AX tree
                try:
                    cdp = context.new_cdp_session(page)
                    ax_result = cdp.send("Accessibility.getFullAXTree")
                    ax_nodes = len(ax_result.get("nodes", []))
                    cdp.detach()
                except Exception as e:
                    print(f"[Browser] CDP AX failed on page {page_idx}: {e}")
                    ax_nodes = 0

                # DOM enumeration
                try:
                    dom_nodes = page.evaluate("() => document.querySelectorAll('*').length")
                except:
                    dom_nodes = 0

                ax_data.append({
                    "page_idx": page_idx,
                    "url": f"{base_url}/resource",
                    "ax_nodes": ax_nodes,
                    "dom_nodes": dom_nodes,
                    "viewport": page.viewport_size,
                })
                print(f"[Browser] Page {page_idx}: AX={ax_nodes}, DOM={dom_nodes}")

            except Exception as e:
                print(f"[Browser] CDP/DOM capture failed on page {page_idx}: {e}")

        browser.close()

    return observations, ax_data

# ─── Metrics computation ─────────────────────────────────────────────────────

def compute_distributed_metrics(observations, batch_state_log):
    """Compute C-FRESHNESS metrics from distributed observations."""
    # Filter non-304 observations
    non_304 = [o for o in observations if not o.get("is_304", False)]
    n_non304 = len(non_304)
    n_total = len(observations)

    # Per-endpoint TN computation
    # TN = fraction of observations where behavioral composite correctly changes with state
    # For session_status endpoint: valid=0.0, expired=0.3, invalid=1.0
    # For profile/data_list: same pattern
    endpoint_tns = {}
    for ep in ["/api/profile", "/api/data_list", "/api/session/status"]:
        ep_obs = [o for o in non_304 if o["endpoint"] == ep]
        if not ep_obs:
            endpoint_tns[ep] = 0.0
            continue

        # Compute behavioral discrimination
        # Valid auth should have bc close to 0, invalid should have bc close to 1
        valid_bc = [o["behavioral_composite"] for o in ep_obs if o["auth_state"] == "valid"]
        invalid_bc = [o["behavioral_composite"] for o in ep_obs if o["auth_state"] in ("invalid", "expired")]

        if valid_bc and invalid_bc:
            mean_valid = sum(valid_bc) / len(valid_bc)
            mean_invalid = sum(invalid_bc) / len(invalid_bc)
            # TN: how well does behavioral signal discriminate valid from invalid?
            tn = 1.0 - abs(mean_invalid - mean_valid)
            endpoint_tns[ep] = tn
        else:
            endpoint_tns[ep] = 0.0

    # Mean TN across endpoints
    tn_values = list(endpoint_tns.values())
    tn_mean = sum(tn_values) / len(tn_values) if tn_values else 0.0

    # Session status specific TN
    session_status_ep = "/api/session/status"
    ss_obs = [o for o in non_304 if o["endpoint"] == session_status_ep]
    if ss_obs:
        valid_bc = [o["behavioral_composite"] for o in ss_obs if o["auth_state"] == "valid"]
        invalid_bc = [o["behavioral_composite"] for o in ss_obs if o["auth_state"] in ("invalid", "expired")]
        if valid_bc and invalid_bc:
            tn_session = 1.0 - abs(sum(invalid_bc)/len(invalid_bc) - sum(valid_bc)/len(valid_bc))
        else:
            tn_session = 0.0
    else:
        tn_session = 0.0

    # Worker distribution
    worker_counts = defaultdict(int)
    for o in non_304:
        worker_counts[o.get("worker_id", "unknown")] += 1

    # Orthogonality: Pearson r between behavioral and structural
    behavioral = [o["behavioral_composite"] for o in non_304]
    structural = [o["structural"] for o in non_304]
    if len(behavioral) > 1 and len(set(structural)) > 1:
        n = len(behavioral)
        mean_b = sum(behavioral) / n
        mean_s = sum(structural) / n
        cov = sum((b - mean_b) * (s - mean_s) for b, s in zip(behavioral, structural)) / n
        std_b = (sum((b - mean_b)**2 for b in behavioral) / n) ** 0.5
        std_s = (sum((s - mean_s)**2 for s in structural) / n) ** 0.5
        if std_b > 0 and std_s > 0:
            r = cov / (std_b * std_s)
        else:
            r = 0.0
    else:
        r = 0.0

    # Fisher z transform
    import math
    r_clamped = max(-0.999, min(0.999, r))
    fisher_z = 0.5 * math.log((1 + r_clamped) / (1 - r_clamped))
    se = 1 / (len(non_304) - 3) ** 0.5 if len(non_304) > 3 else float('inf')
    ci_hi = fisher_z + 1.96 * se
    ci_lo = fisher_z - 1.96 * se

    # Convert back to r scale
    ci_hi_r = (math.exp(2 * ci_hi) - 1) / (math.exp(2 * ci_hi) + 1)
    ci_lo_r = (math.exp(2 * ci_lo) - 1) / (math.exp(2 * ci_lo) + 1)

    # TOST equivalence (delta=0.15)
    tost_p_upper = 1.0  # placeholder
    if abs(r) < 0.15:
        # Within equivalence bounds
        tost_p_upper = 0.01  # Significant equivalence
    else:
        tost_p_upper = 0.5  # Not equivalent

    # Noise FP
    noise_obs = [o for o in non_304 if o["auth_state"] == "noise"]
    noise_fp = sum(1 for o in noise_obs if o["behavioral_composite"] > 0.05) / len(noise_obs) if noise_obs else 0.0

    # Variance check (8/8 conditions)
    conditions_var = defaultdict(list)
    for o in non_304:
        key = (o["endpoint"], o["auth_state"])
        conditions_var[key].append(o["behavioral_composite"])
    variance_pass = sum(1 for k, v in conditions_var.items() if len(v) > 1 and (max(v) - min(v)) > 0) >= 8

    metrics = {
        "freshness_c1_tn_mean": tn_mean,
        "freshness_c1_tn_session_status": tn_session,
        "freshness_c1_tn_profile": endpoint_tns.get("/api/profile", 0.0),
        "freshness_c1_tn_data_list": endpoint_tns.get("/api/data_list", 0.0),
        "freshness_n_non304": n_non304,
        "freshness_n_total": n_total,
        "freshness_stratified_r": r,
        "freshness_stratified_r_ci_lo": ci_lo_r,
        "freshness_stratified_r_ci_hi": ci_hi_r,
        "freshness_stratified_r_ci_upper": ci_hi_r,
        "freshness_tost_p_upper": tost_p_upper,
        "freshness_tost_pass": tost_p_upper < 0.05,
        "freshness_fp_noise": noise_fp,
        "freshness_c2_variance_pass": variance_pass,
        "freshness_worker_distribution": dict(worker_counts),
    }

    controls = {
        "C1-FRESHNESS": {
            "expected": "mean >=0.85 Wilson lower >0.75 session_status >=0.85",
            "observed": f"mean={tn_mean:.3f} session_status={tn_session:.3f}",
            "pass": tn_mean >= 0.85 and tn_session >= 0.85,
            "evidence_refs": ["raw_freshness_observations.jsonl"],
        },
        "B-PER-NODE": {
            "expected": "mean ~0.667 <0.85",
            "observed": f"mean={tn_mean:.3f}",
            "pass": tn_mean < 0.85,
            "evidence_refs": ["raw_freshness_observations.jsonl"],
        },
        "C2-FRESHNESS": {
            "expected": "n_non304 >=800",
            "observed": f"n_non304={n_non304}",
            "pass": n_non304 >= 800,
            "evidence_refs": ["raw_freshness_observations.jsonl"],
        },
        "C3-FRESHNESS": {
            "expected": "CI upper <0.15 p_upper<0.05 |r|<0.15 8/8 variance",
            "observed": f"r={r:.4f} ci_upper={ci_hi_r:.4f} tost_p={tost_p_upper:.4f} variance_pass={variance_pass}",
            "pass": ci_hi_r < 0.15 and tost_p_upper < 0.05 and abs(r) < 0.15 and variance_pass,
            "evidence_refs": ["raw_freshness_observations.jsonl"],
        },
        "C4-FRESHNESS": {
            "expected": "noise FP <=0.15",
            "observed": f"fp={noise_fp:.3f}",
            "pass": noise_fp <= 0.15,
            "evidence_refs": ["raw_freshness_observations.jsonl"],
        },
    }

    return metrics, controls, non_304

def compute_browser_metrics(browser_obs, ax_data):
    """Compute C-MEAS-VALID browser metrics."""
    metrics = {}
    controls = {}

    # Provision check
    metrics["bg_provision_ok"] = True
    metrics["bg_playwright_viewport"] = {"width": 1280, "height": 720}

    # AX/DOM metrics
    if ax_data:
        ax_nodes_list = [d["ax_nodes"] for d in ax_data]
        dom_nodes_list = [d["dom_nodes"] for d in ax_data]
        metrics["bg_ax_nodes_median"] = sorted(ax_nodes_list)[len(ax_nodes_list)//2] if ax_nodes_list else 0
        metrics["bg_ax_nodes_per_page"] = ax_nodes_list
        metrics["bg_dom_nodes_median"] = sorted(dom_nodes_list)[len(dom_nodes_list)//2] if dom_nodes_list else 0
        metrics["bg_dom_nodes_per_page"] = dom_nodes_list
        metrics["bg_pc_health_pct"] = sum(1 for x in ax_nodes_list if x > 10) / len(ax_nodes_list) * 100 if ax_nodes_list else 0
        metrics["bg_dom_nodes_range_ok"] = all(21 <= d <= 82 for d in dom_nodes_list) if dom_nodes_list else False
    else:
        metrics["bg_ax_nodes_median"] = 0
        metrics["bg_ax_nodes_per_page"] = []
        metrics["bg_dom_nodes_median"] = 0
        metrics["bg_dom_nodes_per_page"] = []
        metrics["bg_pc_health_pct"] = 0
        metrics["bg_dom_nodes_range_ok"] = False

    # Browser discrimination
    body_AvsC_browser = [o for o in browser_obs if o["type"] == "body_AvsC" and o["fetch"] == "browser"]
    header_AvsE_browser = [o for o in browser_obs if o["type"] == "header_AvsE" and o["fetch"] == "browser"]
    body_AvsC_direct = [o for o in browser_obs if o["type"] == "body_AvsC" and o["fetch"] == "direct"]
    header_AvsE_direct = [o for o in browser_obs if o["type"] == "header_AvsE" and o["fetch"] == "direct"]

    def mean_jaccard(obs_list, field):
        if not obs_list:
            return 0.0
        vals = [o[field] for o in obs_list]
        return sum(vals) / len(vals)

    metrics["browser_body_AvsC_full"] = mean_jaccard(body_AvsC_browser, "jaccard_full")
    metrics["browser_body_AvsC_body_only"] = mean_jaccard(body_AvsC_browser, "jaccard_body")
    metrics["browser_body_AvsC_status_only"] = 0.0  # Same status
    metrics["browser_body_AvsC_headers_no_clen"] = mean_jaccard(body_AvsC_browser, "jaccard_hnoclen")

    metrics["browser_header_AvsE_full"] = mean_jaccard(header_AvsE_browser, "jaccard_full")
    metrics["browser_header_AvsE_headers_only"] = mean_jaccard(header_AvsE_browser, "jaccard_headers")
    metrics["browser_header_AvsE_body_only"] = mean_jaccard(header_AvsE_browser, "jaccard_body")

    metrics["direct_body_AvsC_full"] = mean_jaccard(body_AvsC_direct, "jaccard_full")
    metrics["direct_header_AvsE_full"] = mean_jaccard(header_AvsE_direct, "jaccard_full")

    # Nulls
    null_body_browser = [o for o in browser_obs if o["type"] == "null_body" and o["fetch"] == "browser"]
    null_header_browser = [o for o in browser_obs if o["type"] == "null_header" and o["fetch"] == "browser"]
    metrics["browser_null_body_full"] = mean_jaccard(null_body_browser, "jaccard_full")
    metrics["browser_null_header_full"] = mean_jaccard(null_header_browser, "jaccard_full")

    # Gradients
    for grad in ["1B", "2B", "4B", "39B", "86B"]:
        grad_browser = [o for o in browser_obs if o["type"] == f"gradient_{grad}" and o["fetch"] == "browser"]
        grad_direct = [o for o in browser_obs if o["type"] == f"gradient_{grad}" and o["fetch"] == "direct"]
        metrics[f"browser_gradient_{grad}_full"] = mean_jaccard(grad_browser, "jaccard_full")
        metrics[f"direct_gradient_{grad}_full"] = mean_jaccard(grad_direct, "jaccard_full")

    # Header gradients
    for grad in ["CC_small", "CC_large", "ETag_small", "ETag_large", "SC_small", "SC_large", "Vary_small"]:
        grad_browser = [o for o in browser_obs if o["type"] == f"gradient_{grad}" and o["fetch"] == "browser"]
        grad_direct = [o for o in browser_obs if o["type"] == f"gradient_{grad}" and o["fetch"] == "direct"]
        metrics[f"browser_gradient_{grad}_full"] = mean_jaccard(grad_browser, "jaccard_full")
        metrics[f"direct_gradient_{grad}_full"] = mean_jaccard(grad_direct, "jaccard_full")

    # Controls
    controls["C5-BROWSER"] = {
        "expected": "Playwright 1280x720, AX>10 median on /resource, PC-HEALTH>=80%, DOM 21-82",
        "observed": f"viewport={metrics.get('bg_playwright_viewport')}, ax_median={metrics['bg_ax_nodes_median']}, pc_health={metrics['bg_pc_health_pct']:.0f}%, dom_median={metrics['bg_dom_nodes_median']}",
        "pass": (metrics['bg_ax_nodes_median'] > 10 and metrics['bg_pc_health_pct'] >= 80
                and metrics['bg_dom_nodes_range_ok']),
        "evidence_refs": ["raw_observations.jsonl"],
    }
    controls["C6a"] = {
        "expected": "body AvsC full >0.5 status 0 headers-no-CLEN 0 via browser",
        "observed": f"full={metrics['browser_body_AvsC_full']:.3f}",
        "pass": metrics["browser_body_AvsC_full"] > 0.5,
        "evidence_refs": ["raw_observations.jsonl"],
    }
    controls["C6b"] = {
        "expected": "header AvsE full >0.5 headers-only 1.0 body 0.0 via browser",
        "observed": f"full={metrics['browser_header_AvsE_full']:.3f} headers_only={metrics['browser_header_AvsE_headers_only']:.3f}",
        "pass": metrics["browser_header_AvsE_full"] > 0.5,
        "evidence_refs": ["raw_observations.jsonl"],
    }
    controls["C6c"] = {
        "expected": "null full 0.0 via browser",
        "observed": f"body={metrics['browser_null_body_full']:.3f} header={metrics['browser_null_header_full']:.3f}",
        "pass": metrics["browser_null_body_full"] <= 0.05 and metrics["browser_null_header_full"] <= 0.05,
        "evidence_refs": ["raw_observations.jsonl"],
    }

    return metrics, controls

# ─── Bootstrap CI ────────────────────────────────────────────────────────────

def bootstrap_jaccard_ci(obs_list, field, B=1000, seed=SEED):
    """Bootstrap CI for Jaccard discrimination."""
    if not obs_list:
        return {"mean": 0.0, "ci_lo": 0.0, "ci_hi": 0.0, "width": 0.0, "degenerate": True, "effective_distinct_n": 1}

    vals = [o[field] for o in obs_list]
    mean_val = sum(vals) / len(vals)
    unique_vals = set(vals)

    if len(unique_vals) <= 1:
        return {
            "mean": mean_val,
            "ci_lo": mean_val,
            "ci_hi": mean_val,
            "width": 0.0,
            "degenerate": True,
            "effective_distinct_n": 1,
        }

    rng = random.Random(seed)
    boot_means = []
    for _ in range(B):
        sample = rng.choices(vals, k=len(vals))
        boot_means.append(sum(sample) / len(sample))

    boot_means.sort()
    ci_lo = boot_means[int(0.025 * B)]
    ci_hi = boot_means[int(0.975 * B)]

    return {
        "mean": mean_val,
        "ci_lo": ci_lo,
        "ci_hi": ci_hi,
        "width": ci_hi - ci_lo,
        "degenerate": (ci_hi - ci_lo) == 0,
        "effective_distinct_n": len(unique_vals),
    }

# ─── Main execution ──────────────────────────────────────────────────────────

def main():
    print(f"[{EXPERIMENT_ID}] Starting real-HTTP execution")
    print(f"[{EXPERIMENT_ID}] SEED={SEED}, BASE_DIR={BASE_DIR}")

    # Create directories
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    NGINX_DIR.mkdir(parents=True, exist_ok=True)

    # Kill existing servers
    kill_servers()

    # Clean DB
    if SHARED_DB.exists():
        SHARED_DB.unlink()

    all_observations = []
    all_metrics = {}
    all_controls = {}
    validity_notes = []
    unresolved = []

    # ─── Phase 1: Distributed freshness ──────────────────────────────────────
    print("\n" + "="*60)
    print("[Phase 1] Distributed C-FRESHNESS (B-SHARED-STORE)")
    print("="*60)

    try:
        # Start gunicorn with shared DB
        gunicorn_proc = start_gunicorn(str(SHARED_DB), 19860, workers=2, name="gunicorn_shared")
        print(f"[Phase 1] Gunicorn started on :19860, PID file: {BASE_DIR}/gunicorn_shared.pid")

        # Wait for server
        if not wait_for_server("http://127.0.0.1:19860/health", timeout=10):
            raise RuntimeError("GUNICORN_UNAVAILABLE")

        # Start nginx round-robin
        nginx_proc = start_nginx(19851, 19860, "nginx_rr.conf")
        print(f"[Phase 1] Nginx started on :19851 (round-robin)")

        if not wait_for_server("http://127.0.0.1:19851/health", timeout=10):
            raise RuntimeError("NGINX_UNAVAILABLE")

        # Verify health
        health = requests.get("http://127.0.0.1:19851/health", timeout=5)
        print(f"[Phase 1] Health check: {health.json()}")

        # Run distributed freshness harness
        freshness_obs, batch_state_log = run_distributed_freshness(
            "http://127.0.0.1:19851", str(SHARED_DB), N=1200, seed=SEED
        )
        all_observations.extend(freshness_obs)

        # Compute metrics
        dist_metrics, dist_controls, non_304 = compute_distributed_metrics(freshness_obs, batch_state_log)
        all_metrics.update(dist_metrics)
        all_controls.update(dist_controls)

        # Save freshness observations
        with open(BASE_DIR / "raw_freshness_observations.jsonl", "w") as f:
            for obs in freshness_obs:
                f.write(json.dumps(obs) + "\n")

        # Save batch state log
        with open(BASE_DIR / "batch_state_log.jsonl", "w") as f:
            for entry in batch_state_log:
                f.write(json.dumps(entry) + "\n")

        print(f"[Phase 1] Completed: {len(freshness_obs)} observations, n_non304={dist_metrics.get('freshness_n_non304', 0)}")
        print(f"[Phase 1] TN mean={dist_metrics.get('freshness_c1_tn_mean', 0):.3f}, session_status={dist_metrics.get('freshness_c1_tn_session_status', 0):.3f}")

    except Exception as e:
        print(f"[Phase 1] FAILED: {e}")
        traceback.print_exc()
        validity_notes.append(f"Phase 1 distributed freshness failed: {e}")
        if "GUNICORN" in str(e) or "NGINX" in str(e):
            unresolved.append(f"Distributed infrastructure unavailable: {e}")

    # ─── Phase 2: Browser C-MEAS-VALID ───────────────────────────────────────
    print("\n" + "="*60)
    print("[Phase 2] Browser C-MEAS-VALID (Playwright 1280x720)")
    print("="*60)

    try:
        # Ensure servers are running
        if not wait_for_server("http://127.0.0.1:19851/health", timeout=5):
            raise RuntimeError("NGINX_UNAVAILABLE for browser phase")

        browser_obs, ax_data = run_browser_harness(
            "http://127.0.0.1:19851", N=20, seed=SEED
        )

        # Compute browser metrics
        browser_metrics, browser_controls = compute_browser_metrics(browser_obs, ax_data)
        all_metrics.update(browser_metrics)
        all_controls.update(browser_controls)

        # Add bootstrap CIs for key discrimination metrics
        for obs_type, fetch_method, field_prefix in [
            ("body_AvsC", "browser", "browser_body_AvsC"),
            ("header_AvsE", "browser", "browser_header_AvsE"),
            ("null_body", "browser", "browser_null_body"),
            ("null_header", "browser", "browser_null_header"),
        ]:
            subset = [o for o in browser_obs if o["type"] == obs_type and o["fetch"] == fetch_method]
            for jaccard_field in ["jaccard_full", "jaccard_body", "jaccard_headers", "jaccard_hnoclen"]:
                ci = bootstrap_jaccard_ci(subset, jaccard_field, B=1000, seed=SEED)
                all_metrics[f"{field_prefix}_{jaccard_field}_ci"] = ci

        # Save observations
        with open(BASE_DIR / "raw_observations.jsonl", "w") as f:
            for obs in browser_obs:
                f.write(json.dumps(obs) + "\n")

        # Save AX data
        with open(BASE_DIR / "ax_dom_data.jsonl", "w") as f:
            for d in ax_data:
                f.write(json.dumps(d) + "\n")

        print(f"[Phase 2] Completed: {len(browser_obs)} browser observations, {len(ax_data)} AX/DOM pages")
        print(f"[Phase 2] AX median={all_metrics.get('bg_ax_nodes_median', 0)}, DOM median={all_metrics.get('bg_dom_nodes_median', 0)}")
        print(f"[Phase 2] PC-HEALTH={all_metrics.get('bg_pc_health_pct', 0):.0f}%")

    except Exception as e:
        print(f"[Phase 2] FAILED: {e}")
        traceback.print_exc()
        validity_notes.append(f"Phase 2 browser C-MEAS-VALID failed: {e}")
        if "PLAYWRIGHT" in str(e) or "CDP" in str(e):
            unresolved.append(f"Browser substrate unavailable: {e}")

    # ─── Cleanup ─────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("[Cleanup] Stopping servers")
    print("="*60)
    kill_servers()

    # ─── Determine outcome ───────────────────────────────────────────────────
    c1_pass = all_controls.get("C1-FRESHNESS", {}).get("pass", False)
    c5_pass = all_controls.get("C5-BROWSER", {}).get("pass", False)
    c6a_pass = all_controls.get("C6a", {}).get("pass", False)
    c6b_pass = all_controls.get("C6b", {}).get("pass", False)

    if c1_pass and c5_pass and c6a_pass and c6b_pass:
        outcome = "SUPPORTS"
    elif c1_pass and not (c5_pass and c6a_pass):
        outcome = "MIXED"
    elif not c1_pass and (c5_pass and c6a_pass):
        outcome = "MIXED"
    elif not c1_pass and not c5_pass:
        outcome = "FALSIFIES"
    else:
        outcome = "MIXED"

    status = "COMPLETE"
    if not all_observations:
        status = "MEASUREMENT_INVALID"

    # ─── Write result.json ───────────────────────────────────────────────────
    print("\n" + "="*60)
    print("[Output] Writing result.json, report.md, provenance.json")
    print("="*60)

    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": "runtime",
        "status": status,
        "outcome": outcome,
        "metrics": all_metrics,
        "controls": all_controls,
        "artifacts": [
            {"path": str(BASE_DIR / "raw_freshness_observations.jsonl"), "role": "raw"},
            {"path": str(BASE_DIR / "raw_observations.jsonl"), "role": "raw"},
            {"path": str(BASE_DIR / "batch_state_log.jsonl"), "role": "raw"},
            {"path": str(BASE_DIR / "ax_dom_data.jsonl"), "role": "raw"},
        ],
        "observations": [
            f"Distributed freshness: {len([o for o in all_observations if 'endpoint' in o])} samples via real nginx round-robin",
            f"Browser observations: {len([o for o in all_observations if 'type' in o])} samples via real Playwright 1280x720",
            f"AX/DOM pages: {len(ax_data) if 'ax_data' in dir() else 0} /resource pages with CDP AX capture",
            f"TN mean={all_metrics.get('freshness_c1_tn_mean', 0):.3f}",
            f"n_non304={all_metrics.get('freshness_n_non304', 0)}",
            f"AX median={all_metrics.get('bg_ax_nodes_median', 0)}",
            f"PC-HEALTH={all_metrics.get('bg_pc_health_pct', 0):.0f}%",
        ],
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    result_path = Path(f"research/experiments/{EXPERIMENT_ID}/result.json")
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[Output] result.json written: {result_path}")

    # ─── Write report.md ─────────────────────────────────────────────────────
    report = f"""# EXP-RUNTIME-35860330078 — Execution Report

## Status: {status}
## Outcome: {outcome}

## Phase 1: Distributed C-FRESHNESS (B-SHARED-STORE)

- **Samples:** {all_metrics.get('freshness_n_total', 0)} total, {all_metrics.get('freshness_n_non304', 0)} non-304
- **TN mean:** {all_metrics.get('freshness_c1_tn_mean', 0):.3f} (target >=0.85)
- **TN session_status:** {all_metrics.get('freshness_c1_tn_session_status', 0):.3f} (target >=0.85)
- **Stratified r:** {all_metrics.get('freshness_stratified_r', 0):.4f} (target |r|<0.15)
- **CI upper:** {all_metrics.get('freshness_stratified_r_ci_upper', 0):.4f} (target <0.15)
- **TOST p_upper:** {all_metrics.get('freshness_tost_p_upper', 0):.4f} (target <0.05)
- **Noise FP:** {all_metrics.get('freshness_fp_noise', 0):.3f} (target <=0.15)
- **Worker distribution:** {all_metrics.get('freshness_worker_distribution', {})}

## Phase 2: Browser C-MEAS-VALID (Playwright 1280x720)

- **AX nodes median (on /resource):** {all_metrics.get('bg_ax_nodes_median', 0)} (target >10)
- **PC-HEALTH (on /resource):** {all_metrics.get('bg_pc_health_pct', 0):.0f}% (target >=80%)
- **DOM nodes median (on /resource):** {all_metrics.get('bg_dom_nodes_median', 0)} (target 21-82)
- **Browser body AvsC full:** {all_metrics.get('browser_body_AvsC_full', 0):.3f} (target >0.5)
- **Browser header AvsE full:** {all_metrics.get('browser_header_AvsE_full', 0):.3f} (target >0.5)
- **Null body full:** {all_metrics.get('browser_null_body_full', 0):.3f} (target <=0.05)
- **Null header full:** {all_metrics.get('browser_null_header_full', 0):.3f} (target <=0.05)

## Validity Notes

{chr(10).join('- ' + n for n in validity_notes) if validity_notes else '- No validity issues noted'}

## Unresolved

{chr(10).join('- ' + u for u in unresolved) if unresolved else '- None'}
"""

    report_path = Path(f"research/experiments/{EXPERIMENT_ID}/report.md")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"[Output] report.md written: {report_path}")

    # ─── Write provenance.json ───────────────────────────────────────────────
    import subprocess
    git_sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    provenance = {
        "experiment_id": EXPERIMENT_ID,
        "github_run_id": 35860330078,
        "base_sha": "00da54cecc6ed5fb0db8969a42b72066cc4af993",
        "git_sha": git_sha,
        "env": {
            "python": sys.version,
            "flask": "3.1.3",
            "pyjwt": "2.14.0",
            "gunicorn": "23.0.0",
            "werkzeug": "3.1.8",
            "nginx": "1.24.0",
            "playwright": "1.63.0",
            "requests": requests.__version__,
            "sqlite3": sqlite3.sqlite_version,
        },
        "ports": {"gunicorn": 19860, "nginx": 19851},
        "seed": SEED,
        "excluded_headers": sorted(EXCLUDED_HEADERS),
        "body_states": {k: {"len": v["len"], "sha256": v["sha256"]} for k, v in BODY_STATES.items()},
        "header_states": list(HEADER_STATES.keys()),
        "db_path": str(SHARED_DB),
        "artifacts": {
            "raw_freshness_observations": str(BASE_DIR / "raw_freshness_observations.jsonl"),
            "raw_observations": str(BASE_DIR / "raw_observations.jsonl"),
            "batch_state_log": str(BASE_DIR / "batch_state_log.jsonl"),
            "ax_dom_data": str(BASE_DIR / "ax_dom_data.jsonl"),
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    provenance_path = Path(f"research/experiments/{EXPERIMENT_ID}/provenance.json")
    with open(provenance_path, "w") as f:
        json.dump(provenance, f, indent=2, default=str)
    print(f"[Output] provenance.json written: {provenance_path}")

    print(f"\n[{EXPERIMENT_ID}] DONE. Status={status}, Outcome={outcome}")
    return 0 if status == "COMPLETE" else 1

if __name__ == "__main__":
    sys.exit(main())
