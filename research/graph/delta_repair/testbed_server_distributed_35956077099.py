#!/usr/bin/env python3
"""
Distributed testbed server for EXP-GRAPH-35956077099 — C-DELTA-REPAIR.

Flask 3.1.3 + PyJWT 2.13.0 HS256 + SQLite WAL shared at /tmp/spider-runtime/EXP-GRAPH-35956077099/shared.db.
Serves /resource/{id} with deterministic flat JSON, ETag, Cache-Control, X-Csrf-Token, X-Worker-Pid.
Supports If-None-Match 304, JWT auth, gunicorn 2-worker round-robin via nginx.
"""
import os, sys, json, time, sqlite3, hashlib, uuid, math, random
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Flask, request, jsonify, make_response, g
import jwt

# ─── Configuration ─────────────────────────────────────
PORT = int(os.environ.get("TESTBED_PORT", "18980"))
SECRET_KEY = os.environ.get("TESTBED_SECRET", "testbed-secret-key-exp-graph-35956077099")
SHARED_DB = os.environ.get("SHARED_DB", "/tmp/spider-runtime/EXP-GRAPH-35956077099/shared.db")
RESOURCE_DIR = "/tmp/spider-runtime/EXP-GRAPH-35956077099/resources"
os.makedirs(SHARED_DB.rsplit("/", 1)[0], exist_ok=True)
os.makedirs(RESOURCE_DIR, exist_ok=True)
os.makedirs("/tmp/spider-runtime/EXP-GRAPH-35956077099", exist_ok=True)

JITTER_MIN_MS = int(os.environ.get("TESTBED_JITTER_MIN", "10"))
JITTER_MAX_MS = int(os.environ.get("TESTBED_JITTER_MAX", "500"))
CACHE_MAX_AGE_FRESH = int(os.environ.get("TESTBED_CACHE_MAX_AGE_FRESH", "60"))
CACHE_MAX_AGE_STALE = int(os.environ.get("TESTBED_CACHE_MAX_AGE_STALE", "0"))
NO_STORE = int(os.environ.get("TESTBED_NO_STORE", "0"))

# Deterministic resource generation seed
RESOURCE_SEED = int(os.environ.get("TESTBED_SEED", "42"))
random.seed(RESOURCE_SEED)

# ─── SQLite WAL ────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(SHARED_DB, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA wal_autocheckpoint=1000")
    conn.execute("""CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT,
        nickname TEXT,
        dom_version TEXT,
        param_version TEXT,
        header_version TEXT,
        cache_version TEXT
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS resource_cache (
        resource_id INTEGER,
        dom_tokens TEXT,
        header_tokens TEXT,
        endpoint_template TEXT,
        etag TEXT,
        cache_control TEXT,
        x_csrf_token TEXT,
        FOREIGN KEY(resource_id) REFERENCES resources(id)
    )""")
    conn.commit()
    return conn

DB_CONN = init_db()

def get_db():
    conn = sqlite3.connect(SHARED_DB, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

# ─── Flask App ──────────────────────────────────────────
app = Flask(__name__)

def _jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Missing token"}), 401
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

def _extract_field_types(obj, prefix=""):
    """Extract (field_path, type) pairs from JSON object, excluding _template."""
    pairs = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "_template":
                continue
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                pairs.update(_extract_field_types(v, path))
            elif isinstance(v, list):
                pairs.add((path, "array"))
            elif v is None:
                pairs.add((path, "string"))
            else:
                t = type(v).__name__
                type_map = {"str": "string", "int": "integer", "float": "number", "bool": "boolean"}
                pairs.add((path, type_map.get(t, t)))
    return pairs

def _canonical_json_without_template(obj):
    """Return JSON with _template removed, sorted keys."""
    d = json.loads(json.dumps(obj))
    d.pop("_template", None)
    return json.dumps(d, sort_keys=True, separators=(',', ':'))

def _make_etag(obj):
    return hashlib.sha256(_canonical_json_without_template(obj).encode()).hexdigest()[:16]

def _generate_resource(id_val):
    """Generate deterministic resource data based on id."""
    h = hashlib.sha256(f"{RESOURCE_SEED}:{id_val}".encode()).hexdigest()
    name = f"resource_{h[:8]}"
    email = f"user_{h[8:16]}@example.com"
    phone = f"+1{h[16:24]}"
    nickname = f"nick_{h[24:32]}"
    dom_version = f"v{h[32:36]}"
    param_version = f"p{h[36:40]}"
    header_version = f"h{h[40:44]}"
    cache_version = f"c{h[44:48]}"
    return {
        "id": id_val,
        "name": name,
        "email": email,
        "phone": phone,
        "nickname": nickname,
        "_dom_version": dom_version,
        "_param_version": param_version,
        "_header_version": header_version,
        "_cache_version": cache_version,
    }

def _apply_perturbation(resource, family, id_val):
    """Apply deterministic perturbation to a resource."""
    r = dict(resource)
    if family == "dom_drift":
        if r["id"] == id_val:
            r["id"] = str(r["id"])  # int->str type change
            r["phone"] = f"+1{hashlib.sha256(f'{RESOURCE_SEED}:{id_val}:dom'.encode()).hexdigest()[:12]}"
    elif family == "param_header_mutation":
        if r["id"] == id_val:
            r["_param_version"] = f"uid_{hashlib.sha256(f'{RESOURCE_SEED}:{id_val}:param'.encode()).hexdigest()[:8]}"
            r["_header_version"] = f"{hashlib.sha256(f'{RESOURCE_SEED}:{id_val}:header'.encode()).hexdigest()[:8]}"
    elif family == "cache_expiry":
        if r["id"] == id_val:
            r["_cache_version"] = f"{hashlib.sha256(f'{RESOURCE_SEED}:{id_val}:cache'.encode()).hexdigest()[:8]}"
    return r

# Store original and perturbed resources in DB
RESOURCE_IDS = list(range(1000, 1050))
INITIAL_RESOURCES = {}
PERTURBED = {}

def _init_resources():
    global INITIAL_RESOURCES, PERTURBED
    conn = get_db()
    for rid in RESOURCE_IDS[:50]:
        resource = _generate_resource(rid)
        INITIAL_RESOURCES[rid] = dict(resource)
        # Store in DB
        conn.execute(
            "INSERT OR REPLACE INTO resources (id, name, email, phone, nickname, dom_version, param_version, header_version, cache_version) VALUES (?,?,?,?,?,?,?,?,?)",
            (rid, resource["name"], resource["email"], resource["phone"], resource["nickname"],
             resource["_dom_version"], resource["_param_version"], resource["_header_version"], resource["_cache_version"])
        )
    conn.commit()
    conn.close()

_init_resources()

@app.route("/resource/<int:resource_id>", methods=["GET"])
@_jwt_required
def get_resource(resource_id):
    """Serve resource with deterministic JSON, ETag, Cache-Control."""
    time.sleep(random.uniform(JITTER_MIN_MS/1000, JITTER_MAX_MS/1000))
    
    # Check If-None-Match
    if_none_match = request.headers.get("If-None-Match", "")
    
    # Get resource
    conn = get_db()
    row = conn.execute("SELECT * FROM resources WHERE id=?", (resource_id,)).fetchone()
    conn.close()
    
    if row is None:
        # Try perturbed resources
        if resource_id in PERTURBED:
            resource = PERTURBED[resource_id]
        else:
            return jsonify({"error": "Not found"}), 404
    else:
        resource = {
            "id": row[0], "name": row[1], "email": row[2],
            "phone": row[3], "nickname": row[4],
            "_dom_version": row[5], "_param_version": row[6],
            "_header_version": row[7], "_cache_version": row[8]
        }
    
    # Check if perturbed
    if resource_id in PERTURBED:
        resource = PERTURBED[resource_id]
    
    # Build response body
    body = {
        "id": resource["id"],
        "name": resource["name"],
        "email": resource["email"],
        "phone": resource["phone"],
        "nickname": resource["nickname"],
        "_template": {
            "query_params": ["detail"],
            "header_names": ["X-Csrf-Token"]
        }
    }
    
    etag = _make_etag(body)
    x_csrf = resource["_header_version"]
    
    # Determine cache control
    if resource_id in PERTURBED and PERTURBED[resource_id]["_cache_version"] != resource["_cache_version"]:
        cache_control = f"max-age={CACHE_MAX_AGE_STALE}"
    else:
        cache_control = f"max-age={CACHE_MAX_AGE_FRESH}"
    
    # Check 304
    if if_none_match and if_none_match.strip('"') == etag:
        resp = make_response("", 304)
        resp.headers["ETag"] = f'"{etag}"'
        resp.headers["Cache-Control"] = cache_control
        resp.headers["X-Csrf-Token"] = x_csrf
        resp.headers["X-Worker-Pid"] = str(os.getpid())
        return resp
    
    resp = make_response(json.dumps(body, sort_keys=True), 200)
    resp.headers["ETag"] = f'"{etag}"'
    resp.headers["Cache-Control"] = cache_control
    resp.headers["X-Csrf-Token"] = x_csrf
    resp.headers["X-Worker-Pid"] = str(os.getpid())
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/resource/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "worker_pid": os.getpid()})

@app.route("/resource/patch/<int:resource_id>", methods=["POST"])
@_jwt_required
def patch_resource(resource_id):
    """Apply perturbation to a resource (for testing repair)."""
    data = request.json
    family = data.get("family")
    id_val = data.get("id", resource_id)
    
    resource = _generate_resource(resource_id)
    perturbed = _apply_perturbation(resource, family, id_val)
    PERTURBED[resource_id] = perturbed
    
    # Update DB
    conn = get_db()
    conn.execute(
        "UPDATE resources SET dom_version=?, param_version=?, header_version=?, cache_version=? WHERE id=?",
        (perturbed["_dom_version"], perturbed["_param_version"], perturbed["_header_version"],
         perturbed["_cache_version"], resource_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({"status": "patched", "family": family, "id": resource_id})

if __name__ == "__main__":
    print(f"Starting distributed testbed server on port {PORT}")
    print(f"Shared DB: {SHARED_DB}")
    print(f"SECRET_KEY set: {bool(SECRET_KEY)}")
    app.run(host="127.0.0.1", port=PORT, threaded=True)
