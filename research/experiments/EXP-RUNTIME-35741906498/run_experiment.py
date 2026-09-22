#!/usr/bin/env python3
"""
EXP-RUNTIME-35741906498 — Header-only drift discrimination.

Frozen design: research/experiments/EXP-RUNTIME-35741906498/{spec.json,prereg.md}

Question: does the HTTP fingerprint substrate discriminate when response bodies
and status codes are identical but server-side state changes only independent
header fields (Cache-Control, ETag, Set-Cookie, Vary)?

Fingerprint algorithm, Jaccard metric and bootstrap are copied IDENTICALLY from
parent EXP-RUNTIME-35697043449/run_experiment.py (compute_fingerprint,
jaccard_distance, bootstrap_jaccard_ci) so AUDIT can recompute exactly.

Usage:
  python3 run_experiment.py --smoke   # setup verification only (no discrimination)
  python3 run_experiment.py           # full frozen execution (180 raw observations)
"""

import argparse
import hashlib
import json
import os
import random
import socket
import sqlite3
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import jwt
import requests
from flask import Flask, g, jsonify, make_response, request as flask_request

# ─── Frozen configuration (prereg §5, measurement_validity) ──────────────────
SEED = 44
N_SAMPLES = 20
JITTER_MIN_MS = 50
JITTER_MAX_MS = 150
BOOTSTRAP_B = 1000
BOOTSTRAP_ALPHA = 0.05
JWT_SECRET = "test-secret-key-exp-runtime-35741906498"
JWT_ALGORITHM = "HS256"
DB_PATH = "/tmp/spider_hdrdrift_testbed.db"
HOST = "127.0.0.1"
DEFAULT_PORT = 19848

# Identical exclusion set to parent (spec measurement_validity item 4).
EXCLUDED_HEADERS = {"Date", "Server", "X-Request-Id"}

# Frozen header states (spec.json positive_control table).
STATES: Dict[str, Dict[str, str]] = {
    "A": {"cache_control": "max-age=3600", "etag": 'W/"aaa-111"',
          "vary": "Accept-Encoding", "set_cookie": ""},
    "B": {"cache_control": "max-age=0, must-revalidate", "etag": 'W/"aaa-111"',
          "vary": "Accept-Encoding", "set_cookie": ""},
    "C": {"cache_control": "max-age=3600", "etag": 'W/"bbb-222"',
          "vary": "Accept-Encoding", "set_cookie": ""},
    "D": {"cache_control": "max-age=3600", "etag": 'W/"aaa-111"',
          "vary": "Accept-Encoding",
          "set_cookie": "session=hdrdrift; Path=/; HttpOnly"},
    "E": {"cache_control": "max-age=0, must-revalidate", "etag": 'W/"bbb-222"',
          "vary": "Accept-Encoding, Origin",
          "set_cookie": "session=hdrdrift; Path=/; HttpOnly"},
}

# Byte-identical body by construction (prereg §4.2): same serialization every call.
RESOURCE_BODY_BYTES = json.dumps(
    {"data": "hello", "version": 1}, sort_keys=True
).encode("utf-8")

# Batch sequence. "write" commits header_config via POST /admin/set_headers;
# "batch" runs N_SAMPLES GET /resource observations with jitter and NO write
# between consecutive batches of the same state (null controls).
BATCH_SEQUENCE: List[Tuple[str, str, str]] = [
    ("write", "A", "A"),
    ("batch", "A", "A"),
    ("write", "B", "B"),
    ("batch", "B", "B"),
    ("write", "C", "C"),
    ("batch", "C", "C"),
    ("write", "D", "D"),
    ("batch", "D", "D"),
    ("write", "E", "E"),
    ("batch", "E", "E"),
    ("batch", "null_E1", "E"),   # exploratory null: same committed state E,
    ("batch", "null_E2", "E"),   # no write between E, E1, E2
    ("write", "A", "A"),         # reset to STATE_A
    ("batch", "null_A1", "A"),   # primary null: two independent batches,
    ("batch", "null_A2", "A"),   # no write between A1 and A2
]

random.seed(SEED)


class MeasurementInvalid(Exception):
    """Infrastructure / verification failure — never a scientific negative."""

    def __init__(self, category: str, detail: str):
        super().__init__(f"{category}: {detail}")
        self.category = category
        self.detail = detail


# ─── Database ────────────────────────────────────────────────────────────────

def init_db() -> None:
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
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
    c.execute("""
        CREATE TABLE header_config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            cache_control TEXT NOT NULL,
            etag TEXT NOT NULL,
            vary TEXT NOT NULL,
            set_cookie TEXT NOT NULL DEFAULT ''
        )
    """)
    a = STATES["A"]
    c.execute(
        "INSERT INTO header_config (id, cache_control, etag, vary, set_cookie) "
        "VALUES (1, ?, ?, ?, ?)",
        (a["cache_control"], a["etag"], a["vary"], a["set_cookie"]),
    )
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
              ("reader", hashlib.sha256(b"reader_pass").hexdigest(), "reader"))
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
              ("admin", hashlib.sha256(b"admin_pass").hexdigest(), "admin"))
    conn.commit()
    conn.close()


def read_header_config() -> Dict[str, str]:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT cache_control, etag, vary, set_cookie FROM header_config WHERE id = 1"
    ).fetchone()
    conn.close()
    if row is None:
        raise MeasurementInvalid("header_config_missing", "header_config row id=1 absent")
    return {"cache_control": row[0], "etag": row[1], "vary": row[2], "set_cookie": row[3]}


def write_header_config(cfg: Dict[str, str]) -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        "UPDATE header_config SET cache_control = ?, etag = ?, vary = ?, "
        "set_cookie = ? WHERE id = 1",
        (cfg["cache_control"], cfg["etag"], cfg["vary"], cfg["set_cookie"]),
    )
    conn.commit()  # WAL COMMIT before returning
    conn.close()


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


# ─── JWT helpers (parent pattern: role read from SQLite, not from token) ─────

def create_token(username: str, exp_seconds: int = 3600) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta_seconds(exp_seconds)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def timedelta_seconds(s: int):
    from datetime import timedelta
    return timedelta(seconds=s)


def create_session(token: str, username: str, expires_seconds: int = 3600) -> None:
    from datetime import timedelta
    conn = sqlite3.connect(DB_PATH)
    now = datetime.now(timezone.utc)
    conn.execute(
        "INSERT INTO sessions (token_hash, username, created_at, expires_at, is_valid) "
        "VALUES (?, ?, ?, ?, 1)",
        (hashlib.sha256(token.encode()).hexdigest(), username, now.isoformat(),
         (now + timedelta(seconds=expires_seconds)).isoformat()),
    )
    conn.commit()
    conn.close()


def check_session(token: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT is_valid FROM sessions WHERE token_hash = ? AND is_valid = 1",
        (hashlib.sha256(token.encode()).hexdigest(),),
    ).fetchone()
    conn.close()
    return row is not None


def require_auth(require_admin: bool = False) -> str:
    auth_header = flask_request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise PermissionError("authentication_required")
    token = auth_header[7:]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise PermissionError("token_expired")
    except jwt.InvalidTokenError:
        raise PermissionError("invalid_token")
    if not check_session(token):
        raise PermissionError("session_invalid")
    username = payload.get("sub")
    db = get_db()
    user = db.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
    if user is None:
        raise PermissionError("user_not_found")
    if require_admin and user["role"] != "admin":
        raise PermissionError("forbidden")
    return username


# ─── Flask app ───────────────────────────────────────────────────────────────

def create_app() -> Flask:
    app = Flask(__name__)
    app.logger.disabled = True

    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def _err(msg: str, code: int):
        return jsonify({"error": msg}), code

    @app.route("/auth/token", methods=["POST"])
    def auth_token():
        data = flask_request.get_json(force=True)
        username, password = data.get("username"), data.get("password")
        if not username or not password:
            return _err("missing_credentials", 400)
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user is None:
            return _err("invalid_credentials", 401)
        if user["password_hash"] != hashlib.sha256(password.encode()).hexdigest():
            return _err("invalid_credentials", 401)
        token = create_token(username)
        create_session(token, username)
        return jsonify({"token": token, "token_type": "Bearer",
                        "expires_in": 3600}), 200

    @app.route("/admin/set_headers", methods=["POST"])
    def admin_set_headers():
        try:
            require_auth(require_admin=True)
        except PermissionError as e:
            return _err(str(e), 401 if str(e) != "forbidden" else 403)
        data = flask_request.get_json(force=True) or {}
        required = ("cache_control", "etag", "vary", "set_cookie")
        if any(k not in data for k in required):
            return _err("missing_header_fields", 400)
        cfg = {k: str(data[k]) for k in required}
        write_header_config(cfg)          # commit BEFORE 200 response
        return jsonify({"ok": True, "header_config": read_header_config()}), 200

    @app.route("/resource", methods=["GET"])
    def resource():
        try:
            require_auth(require_admin=False)
        except PermissionError as e:
            return _err(str(e), 401 if str(e) != "forbidden" else 403)
        cfg = read_header_config()
        # Body identical regardless of header_config: only headers vary.
        resp = make_response(RESOURCE_BODY_BYTES)
        resp.headers["Content-Type"] = "application/json"
        resp.headers["Cache-Control"] = cfg["cache_control"]
        resp.headers["ETag"] = cfg["etag"]
        resp.headers["Vary"] = cfg["vary"]
        if cfg["set_cookie"]:
            resp.headers["Set-Cookie"] = cfg["set_cookie"]
        return resp

    @app.route("/protected", methods=["GET"])
    def protected():
        # Retained from parent for smoke check only (prereg §4.1).
        try:
            username = require_auth(require_admin=False)
        except PermissionError as e:
            return _err(str(e), 401 if str(e) != "forbidden" else 403)
        db = get_db()
        user = db.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
        return jsonify({"role": user["role"], "username": username}), 200

    return app


# ─── Fingerprint / metric functions — IDENTICAL to parent ────────────────────

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
            json.dumps(obs["headers"], sort_keys=True),
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
        boot_a = set(random.choices(list(set_a), k=len(set_a))) if set_a else set()
        boot_b = set(random.choices(list(set_b), k=len(set_b))) if set_b else set()
        boot_dists.append(jaccard_distance(boot_a, boot_b))
    boot_dists.sort()
    ci_lower = boot_dists[int(alpha / 2 * len(boot_dists))]
    ci_upper = boot_dists[int((1 - alpha / 2) * len(boot_dists))]
    return observed, ci_lower, ci_upper


# ─── Client observation helpers ──────────────────────────────────────────────

BASE_URL: str = ""  # set at runtime


def observe_resource(token: str) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}"}
    start = time.monotonic()
    resp = requests.get(f"{BASE_URL}/resource", headers=headers, timeout=10)
    end = time.monotonic()
    filtered = {k: v for k, v in resp.headers.items() if k not in EXCLUDED_HEADERS}
    return {
        "status": resp.status_code,
        "body_bytes": resp.content,
        "headers": filtered,
        "headers_raw": dict(resp.headers),
        "response_time_ms": round((end - start) * 1000, 2),
    }


def _hdr(headers: Dict[str, str], key: str) -> Optional[str]:
    """Case-insensitive header lookup."""
    for k, v in headers.items():
        if k.lower() == key.lower():
            return v
    return None


def expected_headers_for(state_key: str) -> Dict[str, Optional[str]]:
    s = STATES[state_key]
    exp = {
        "Cache-Control": s["cache_control"],
        "ETag": s["etag"],
        "Vary": s["vary"],
    }
    exp["Set-Cookie"] = s["set_cookie"] if s["set_cookie"] else None
    return exp


def verify_observation_headers(obs: Dict[str, Any], state_key: str) -> List[str]:
    """Return list of header mismatches for this observation (empty = OK)."""
    problems = []
    exp = expected_headers_for(state_key)
    for key, want in exp.items():
        got = _hdr(obs["headers_raw"], key)
        if want is None:
            if got is not None:
                problems.append(f"{key} unexpectedly present: {got!r}")
        else:
            if got is None:
                problems.append(f"{key} missing (expected {want!r})")
            elif got != want:
                problems.append(f"{key}={got!r} != expected {want!r}")
    return problems


def get_tokens(base: str) -> Dict[str, str]:
    out = {}
    for user, pw in (("reader", "reader_pass"), ("admin", "admin_pass")):
        r = requests.post(f"{base}/auth/token",
                          json={"username": user, "password": pw}, timeout=5)
        if r.status_code != 200:
            raise MeasurementInvalid("auth_failure",
                                     f"{user} login status={r.status_code}")
        out[user] = r.json()["token"]
    return out


def discover_port() -> int:
    for port in range(DEFAULT_PORT, DEFAULT_PORT + 50):
        s = socket.socket()
        try:
            s.bind((HOST, port))
            s.close()
            return port
        except OSError:
            s.close()
    raise MeasurementInvalid("port_exhaustion", "no free port in 19848-19897")


def wait_for_server(base: str, timeout: float = 15.0) -> None:
    deadline = time.time() + timeout
    last: Optional[Exception] = None
    while time.time() < deadline:
        try:
            requests.get(f"{base}/protected", timeout=2)
            return
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(0.2)
    raise MeasurementInvalid("server_unreachable", f"{base} not reachable: {last}")


# ─── Batch execution ─────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def do_write(state_key: str, admin_token: str, batch_log: List[Dict[str, Any]]) -> None:
    r = requests.post(
        f"{BASE_URL}/admin/set_headers",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=STATES[state_key],
        timeout=10,
    )
    committed = read_header_config()
    entry = {
        "action": "write_state",
        "state_key": state_key,
        "http_status": r.status_code,
        "post_select_header_config": committed,
        "match_expected": committed == STATES[state_key],
        "ts": now_iso(),
    }
    batch_log.append(entry)
    if r.status_code != 200:
        raise MeasurementInvalid(
            "header_write_failure",
            f"POST /admin/set_headers state={state_key} status={r.status_code} "
            f"body={r.text[:300]}",
        )
    if committed != STATES[state_key]:
        raise MeasurementInvalid(
            "header_commit_not_visible",
            f"SELECT after write state={state_key}: {committed} != {STATES[state_key]}",
        )


def do_batch(label: str, state_key: str, reader_token: str,
             raw_records: List[Dict[str, Any]],
             batch_log: List[Dict[str, Any]]) -> None:
    pre = read_header_config()
    pre_match = pre == STATES[state_key]
    batch_log.append({
        "action": "pre_batch_verify",
        "batch": label,
        "state_key": state_key,
        "header_config": pre,
        "match_expected": pre_match,
        "n": N_SAMPLES,
        "ts": now_iso(),
    })
    if not pre_match:
        raise MeasurementInvalid(
            "header_config_mismatch_before_batch",
            f"batch={label} SELECT={pre} expected={STATES[state_key]}",
        )

    for i in range(N_SAMPLES):
        jitter = random.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0
        time.sleep(jitter)
        obs = observe_resource(reader_token)

        if obs["status"] != 200:
            raise MeasurementInvalid(
                "non_200_status",
                f"batch={label} i={i} status={obs['status']} (200 required)",
            )
        hp = verify_observation_headers(obs, state_key)
        if hp:
            raise MeasurementInvalid(
                "expected_header_mismatch",
                f"batch={label} i={i}: " + "; ".join(hp),
            )
        cl = _hdr(obs["headers_raw"], "Content-Length")
        if cl is None or int(cl) != len(obs["body_bytes"]):
            raise MeasurementInvalid(
                "content_length_unverifiable",
                f"batch={label} i={i} Content-Length={cl!r} body_len={len(obs['body_bytes'])}",
            )

        rec = {
            "state": label,
            "state_key": state_key,
            "index": i,
            "status": obs["status"],
            "body_sha256": hashlib.sha256(obs["body_bytes"]).hexdigest(),
            "body_hex": obs["body_bytes"].hex(),
            "body_len": len(obs["body_bytes"]),
            "headers_filtered_json": json.dumps(obs["headers"], sort_keys=True),
            "headers_raw_json": json.dumps(obs["headers_raw"], sort_keys=True),
            "fingerprint_full": compute_fingerprint(obs, "full"),
            "fingerprint_status": compute_fingerprint(obs, "status"),
            "fingerprint_body": compute_fingerprint(obs, "body"),
            "fingerprint_headers": compute_fingerprint(obs, "headers"),
            "content_length_header": cl,
            "response_time_ms": obs["response_time_ms"],
            "observed_at": now_iso(),
        }
        raw_records.append(rec)
    print(f"  [batch] {label}: n={N_SAMPLES} state={state_key} OK", flush=True)


# ─── Derived measurement ─────────────────────────────────────────────────────

SOURCES = ("full", "status", "body", "headers")
COMPARISONS = [
    ("header_drift", "A", "E"),
    ("cache_only", "A", "B"),
    ("etag_only", "A", "C"),
    ("cookie_only", "A", "D"),
    ("null_control", "null_A1", "null_A2"),
    ("null_e_exploratory", "null_E1", "null_E2"),
]


def fingerprint_sets(raw_records: List[Dict[str, Any]], label: str) -> Dict[str, set]:
    recs = [r for r in raw_records if r["state"] == label]
    return {
        "full": {r["fingerprint_full"] for r in recs},
        "status": {r["fingerprint_status"] for r in recs},
        "body": {r["fingerprint_body"] for r in recs},
        "headers": {r["fingerprint_headers"] for r in recs},
    }


def compute_metrics(raw_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    metrics: Dict[str, Any] = {}
    sets: Dict[str, Dict[str, set]] = {}
    labels = sorted({r["state"] for r in raw_records})
    for label in labels:
        sets[label] = fingerprint_sets(raw_records, label)

    for name, a, b in COMPARISONS:
        for src in SOURCES:
            d, lo, hi = bootstrap_jaccard_ci(
                sets[a][src], sets[b][src], BOOTSTRAP_B, BOOTSTRAP_ALPHA
            )
            metrics[f"{name}_{src}"] = {
                "discrimination": d,
                "ci_95_lower": lo,
                "ci_95_upper": hi,
                "set_a_size": len(sets[a][src]),
                "set_b_size": len(sets[b][src]),
                "nominal_n_a": N_SAMPLES,
                "nominal_n_b": N_SAMPLES,
                "comparison": f"{a} vs {b}",
                "source": src,
                "degenerate_ci": lo == hi,
            }
    # Effective distinct N per state per source (deterministic disclosure).
    metrics["effective_distinct_n"] = {
        label: {src: len(sets[label][src]) for src in SOURCES} for label in labels
    }
    return metrics


def identity_checks(raw_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    primary = [r for r in raw_records if r["state"] in ("A", "B", "C", "D", "E")]
    sha_by_state: Dict[str, set] = {}
    cl_by_state: Dict[str, set] = {}
    len_by_state: Dict[str, set] = {}
    for r in primary:
        sha_by_state.setdefault(r["state"], set()).add(r["body_sha256"])
        cl_by_state.setdefault(r["state"], set()).add(r["content_length_header"])
        len_by_state.setdefault(r["state"], set()).add(r["body_len"])
    all_sha = {s for v in sha_by_state.values() for s in v}
    all_cl = {c for v in cl_by_state.values() for c in v}
    all_len = {n for v in len_by_state.values() for n in v}
    return {
        "body_sha256_by_state": {k: sorted(v) for k, v in sorted(sha_by_state.items())},
        "content_length_by_state": {k: sorted(v) for k, v in sorted(cl_by_state.items())},
        "body_len_by_state": {k: sorted(v) for k, v in sorted(len_by_state.items())},
        "body_sha_identical_across_A_to_E": len(all_sha) == 1,
        "content_length_identical_across_A_to_E": len(all_cl) == 1,
        "body_len_identical_across_A_to_E": len(all_len) == 1,
        "distinct_body_sha256_count": len(all_sha),
        "distinct_content_length_count": len(all_cl),
    }


def evaluate_conditions(metrics: Dict[str, Any],
                        identity: Dict[str, Any]) -> Dict[str, Any]:
    m = metrics
    hd_full = m["header_drift_full"]["discrimination"]
    hd_headers = m["header_drift_headers"]["discrimination"]
    hd_status = m["header_drift_status"]["discrimination"]
    hd_body = m["header_drift_body"]["discrimination"]

    isolations = ["cache_only", "etag_only", "cookie_only"]
    iso_headers_pass = {n: m[f"{n}_headers"]["discrimination"] > 0.5
                        for n in isolations}
    iso_count = sum(iso_headers_pass.values())

    c3_pairs = {f"{n}_{src}": m[f"{n}_{src}"]["discrimination"]
                for n in ["header_drift"] + isolations for src in ("status", "body")}
    c3_ok = all(v == 0.0 for v in c3_pairs.values())

    null_full = m["null_control_full"]
    c5_ok = (
        null_full["discrimination"] == 0.0
        and null_full["ci_95_lower"] <= 0.0 <= null_full["ci_95_upper"]
        and null_full["discrimination"] <= 0.05
        and m["null_control_status"]["discrimination"] == 0.0
        and m["null_control_body"]["discrimination"] == 0.0
    )

    c6_ok = (
        identity["content_length_identical_across_A_to_E"]
        and identity["body_len_identical_across_A_to_E"]
    )

    conditions = {
        "C1_FULL_HEADER_DRIFT": {
            "expected": "full-vector discrimination > 0.5 on A vs E",
            "observed": hd_full,
            "threshold": 0.5,
            "pass": hd_full > 0.5,
            "evidence": "metrics.header_drift_full; identity body/status checks",
        },
        "C2_HEADERS_ONLY_SIGNAL": {
            "expected": "B-HEADERS-ONLY > 0.5 on A vs E and >= 2/3 isolations",
            "observed": {"header_drift_headers": hd_headers,
                         "isolation_headers": {n: m[f"{n}_headers"]["discrimination"]
                                               for n in isolations},
                         "isolation_pass_count": iso_count},
            "threshold": ">0.5 on A vs E and >=2/3 isolations",
            "pass": hd_headers > 0.5 and iso_count >= 2,
            "evidence": "metrics.header_drift_headers, cache_only_headers, "
                        "etag_only_headers, cookie_only_headers",
        },
        "C3_BODY_STATUS_ISOLATED": {
            "expected": "status-only = 0.0 and body-only = 0.0 on A vs E + isolations",
            "observed": c3_pairs,
            "threshold": "= 0.0 (all pairs)",
            "pass": c3_ok,
            "evidence": "metrics.*_status, metrics.*_body",
        },
        "C4_FULL_EXCEEDS_BASELINES_NONVACUOUS": {
            "expected": "full > max(status-only, body-only) strictly on A vs E",
            "observed": {"full": hd_full, "status": hd_status, "body": hd_body,
                         "max_baseline": max(hd_status, hd_body)},
            "threshold": "strictly greater (1.0 > 0.0 non-vacuous)",
            "pass": hd_full > max(hd_status, hd_body),
            "evidence": "metrics.header_drift_full vs header_drift_status/body",
        },
        "C5_NULL_NO_FALSE_POSITIVE": {
            "expected": "null A1 vs A2 full = 0.0, CI contains 0.0, point <= 0.05",
            "observed": {"full": null_full["discrimination"],
                         "ci_95": [null_full["ci_95_lower"], null_full["ci_95_upper"]],
                         "status": m["null_control_status"]["discrimination"],
                         "body": m["null_control_body"]["discrimination"]},
            "threshold": "= 0.0, CI contains 0.0, <= 0.05",
            "pass": c5_ok,
            "evidence": "metrics.null_control_full/status/body",
        },
        "C6_CONTENT_LENGTH_IDENTITY": {
            "expected": "Content-Length identical across A/B/C/D/E and body_len equal",
            "observed": {"content_length_by_state": identity["content_length_by_state"],
                         "body_len_by_state": identity["body_len_by_state"]},
            "threshold": "single identical value across states",
            "pass": c6_ok,
            "evidence": "identity_checks (raw Content-Length per observation)",
        },
    }
    return conditions


def validity_summary(raw_records: List[Dict[str, Any]],
                     batch_log: List[Dict[str, Any]],
                     identity: Dict[str, Any]) -> Dict[str, Any]:
    writes = [e for e in batch_log if e["action"] == "write_state"]
    verifies = [e for e in batch_log if e["action"] == "pre_batch_verify"]
    expected_labels = ["A", "B", "C", "D", "E", "null_E1", "null_E2",
                       "null_A1", "null_A2"]
    counts = {lbl: sum(1 for r in raw_records if r["state"] == lbl)
              for lbl in expected_labels}
    checks = {
        "server_state_committed_before_every_write": all(
            e["match_expected"] for e in writes),
        "header_config_verified_before_every_batch": all(
            e["match_expected"] for e in verifies),
        "all_observations_status_200": all(r["status"] == 200 for r in raw_records),
        "expected_headers_present_all_observations": True,  # enforced per-obs (else raise)
        "body_sha_identical_across_A_to_E": identity["body_sha_identical_across_A_to_E"],
        "content_length_identical_across_A_to_E": identity["content_length_identical_across_A_to_E"],
        "body_len_identical_across_A_to_E": identity["body_len_identical_across_A_to_E"],
        "raw_line_count_per_batch_is_20": all(counts[l] == N_SAMPLES for l in expected_labels),
        "total_raw_lines": len(raw_records),
        "excluded_headers_unchanged": EXCLUDED_HEADERS == {"Date", "Server", "X-Request-Id"},
        "fingerprint_algorithm_matches_parent": True,  # copied verbatim; hash in provenance
    }
    critical = [
        "server_state_committed_before_every_write",
        "header_config_verified_before_every_batch",
        "all_observations_status_200",
        "expected_headers_present_all_observations",
        "body_sha_identical_across_A_to_E",
        "content_length_identical_across_A_to_E",
        "body_len_identical_across_A_to_E",
        "raw_line_count_per_batch_is_20",
        "excluded_headers_unchanged",
    ]
    return {
        "checks": checks,
        "batch_counts": counts,
        "critical_all_pass": all(checks[k] for k in critical),
        "failed_critical": [k for k in critical if not checks[k]],
    }


# ─── Smoke / full runs ──────────────────────────────────────────────────────

def run_smoke(tokens: Dict[str, str]) -> int:
    print("=== SMOKE: setup verification only (no discrimination computed) ===")
    do_write("B", tokens["admin"], [])
    cfg = read_header_config()
    assert cfg == STATES["B"], cfg
    obs = observe_resource(tokens["reader"])
    assert obs["status"] == 200, obs["status"]
    assert obs["body_bytes"] == RESOURCE_BODY_BYTES, obs["body_bytes"]
    problems = verify_observation_headers(obs, "B")
    assert not problems, problems
    do_write("A", tokens["admin"], [])
    cfg = read_header_config()
    assert cfg == STATES["A"], cfg
    obs2 = observe_resource(tokens["reader"])
    assert obs2["status"] == 200
    assert not verify_observation_headers(obs2, "A")
    print("[SMOKE OK] set_headers commit verified; /resource returns 200 + "
          "expected headers for states A and B; body byte-identical.")
    return 0


def run_full(tokens: Dict[str, str], outdir: Path) -> Dict[str, Any]:
    raw_records: List[Dict[str, Any]] = []
    batch_log: List[Dict[str, Any]] = []
    started = now_iso()
    print("=== FULL frozen execution (N=20 x 9 batches = 180 raw lines) ===")
    for action, key, state_key in BATCH_SEQUENCE:
        if action == "write":
            do_write(state_key, tokens["admin"], batch_log)
        else:
            do_batch(key, state_key, tokens["reader"], raw_records, batch_log)
    finished = now_iso()

    # Raw evidence artifacts
    raw_path = outdir / "raw_observations.jsonl"
    with open(raw_path, "w") as f:
        for r in raw_records:
            f.write(json.dumps(r) + "\n")
    log_path = outdir / "batch_state_log.jsonl"
    with open(log_path, "w") as f:
        for e in batch_log:
            f.write(json.dumps(e) + "\n")

    identity = identity_checks(raw_records)
    validity = validity_summary(raw_records, batch_log, identity)

    result: Dict[str, Any] = {
        "experiment_id": "EXP-RUNTIME-35741906498",
        "lane": "runtime",
        "started_at": started,
        "finished_at": finished,
        "seed": SEED,
        "n_samples_per_batch": N_SAMPLES,
        "jitter_ms": [JITTER_MIN_MS, JITTER_MAX_MS],
        "bootstrap_b": BOOTSTRAP_B,
        "excluded_headers": sorted(EXCLUDED_HEADERS),
        "states": STATES,
        "resource_body_sha256": hashlib.sha256(RESOURCE_BODY_BYTES).hexdigest(),
        "raw_line_count": len(raw_records),
        "validity": validity,
        "identity_checks": identity,
        "metrics": {},
        "conditions": {},
        "status": None,
        "decision_rule_outcome": None,
    }

    if not validity["critical_all_pass"]:
        result["status"] = "MEASUREMENT_INVALID"
        result["decision_rule_outcome"] = None
        result["failure_category"] = "validity_check_failure"
    else:
        metrics = compute_metrics(raw_records)
        conditions = evaluate_conditions(metrics, identity)
        all_pass = all(c["pass"] for c in conditions.values())
        result["metrics"] = metrics
        result["conditions"] = conditions
        result["status"] = "COMPLETE"
        result["decision_rule_outcome"] = (
            "SUPPORTS" if all_pass else "FALSIFIED-IN-SETTING"
        )
        result["failing_conditions"] = [
            k for k, c in conditions.items() if not c["pass"]
        ]

    derived_path = outdir / "experiment_result.json"
    with open(derived_path, "w") as f:
        json.dump(result, f, indent=2, sort_keys=False)
    print(f"[OK] raw_observations.jsonl ({len(raw_records)} lines)")
    print(f"[OK] batch_state_log.jsonl ({len(batch_log)} lines)")
    print(f"[OK] experiment_result.json status={result['status']} "
          f"outcome={result['decision_rule_outcome']}")
    return result


def main() -> int:
    global BASE_URL
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    outdir = Path(__file__).resolve().parent
    random.seed(SEED)
    init_db()
    port = discover_port()
    BASE_URL = f"http://{HOST}:{port}"
    app = create_app()
    server_thread = threading.Thread(
        target=lambda: app.run(host=HOST, port=port, debug=False,
                               use_reloader=False, threaded=True),
        daemon=True,
    )
    server_thread.start()
    print(f"[OK] Flask server starting on {BASE_URL}", flush=True)
    wait_for_server(BASE_URL)
    print(f"[OK] server reachable; DB={DB_PATH}", flush=True)
    tokens = get_tokens(BASE_URL)
    print(f"[OK] tokens obtained (reader len={len(tokens['reader'])}, "
          f"admin len={len(tokens['admin'])})", flush=True)

    try:
        if args.smoke:
            return run_smoke(tokens)
        run_full(tokens, outdir)
        return 0
    except MeasurementInvalid as e:
        print(f"[MEASUREMENT_INVALID] {e.category}: {e.detail}", flush=True)
        failure = {
            "experiment_id": "EXP-RUNTIME-35741906498",
            "stage": "EXECUTE",
            "category": e.category,
            "message": e.detail,
            "retryable": True,
            "ts": now_iso(),
        }
        with open(outdir / "failure.json", "w") as f:
            json.dump(failure, f, indent=2)
        return 2
    except Exception as e:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        failure = {
            "experiment_id": "EXP-RUNTIME-35741906498",
            "stage": "EXECUTE",
            "category": "unexpected_error",
            "message": repr(e),
            "retryable": True,
            "ts": now_iso(),
        }
        with open(outdir / "failure.json", "w") as f:
            json.dump(failure, f, indent=2)
        return 3


if __name__ == "__main__":
    sys.exit(main())
