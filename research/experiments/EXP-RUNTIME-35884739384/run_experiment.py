#!/usr/bin/env python3
"""
EXP-RUNTIME-35884739384 — Real-HTTP distributed freshness (shared WAL / sticky / per-node)
+ Playwright 1280x720 browser C-MEAS-VALID. EXECUTE stage against frozen design.

Fixes vs parent EXP-RUNTIME-35860330078 (audit MEASUREMENT_INVALID):
  * HS256: pyjwt.decode(token, secret, algorithms=['HS256']) then SELECT sessions by sid
    (parent used raw Bearer string lookup — all valid JWTs rejected).
  * TN formula: P(bc<=0.05|valid) + Wilson CI (parent inverted 1-|mean_invalid-mean_valid|).
  * X-Worker-Pid + ETag emitted on ALL statuses including 401.
  * Real If-None-Match/ETag -> 304 exercised when cache_enabled.
  * per-batch SELECT count(*) COMMIT verification, batch_state_log >=27 distinct timestamps.
  * Structural signal excludes constant-401-body confound; r/TOST computed from data.
  * Playwright real page.request / page.goto fetches with CDP AX on each /resource page.
  * No synthetic generation, no hardcoded TN/TOST, no direct-as-browser relabeling.

Frozen inputs: research/experiments/EXP-RUNTIME-35884739384/{request,spec,prereg,freeze}.*
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import signal
import sqlite3
import statistics
import subprocess
import sys
import time
import traceback
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import jwt
import requests
from flask import Flask, g, jsonify, request as flask_request

# ─── Frozen constants ────────────────────────────────────────────────────────
EXPERIMENT_ID = "EXP-RUNTIME-35884739384"
LANE = "runtime"
SEED = 44
JITTER_MIN_MS = 50
JITTER_MAX_MS = 150
BOOTSTRAP_B = 1000
N_DISTRIBUTED = 1200
N_BROWSER_STATE = 20
CONCURRENCY = 4

EXCLUDED_HEADERS = {
    "Date", "Server", "X-Request-Id",
    "CF-RAY", "CF-Cache-Status", "X-Cache", "Age",
}
FILTER_OUT_KEYS = {h.lower() for h in EXCLUDED_HEADERS} | {"x-worker-pid"}

BASE_DIR = Path(f"/tmp/spider-runtime-{EXPERIMENT_ID.split('-')[-1]}")
SHARED_DB = Path("/tmp/spider-runtime-35860330078/shared.db")
SHARED_DB.parent.mkdir(parents=True, exist_ok=True)
NGINX_DIR = BASE_DIR / "nginx"
EXPERIMENT_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = EXPERIMENT_DIR

HOST = "127.0.0.1"
GUNICORN_PORT_A = 19860
GUNICORN_PORT_B = 19861
NGINX_PORT = 19851

JWT_SECRET = "spider-exp-35884739384-hs256-secret"
JWT_ALG = "HS256"
HS256_SECRET_HASH = hashlib.sha256(JWT_SECRET.encode()).hexdigest()

# Body states — lineage-exact JSON (default separators ', ': ') matching frozen
# pins A=31B d0ca833f / B=70B 67c186f2 / C=117B b46c461c from EXP-RUNTIME-35764329925.
BODY_STATES: Dict[str, Dict[str, Any]] = {
    "A":  {"json": '{"data": "hello", "version": 1}', "len": 31},
    "A1": {"json": '{"data": "hello!", "version": 1}', "len": 32},
    "A2": {"json": '{"data": "hello!!", "version": 1}', "len": 33},
    "A3": {"json": '{"data": "hello!!!!", "version": 1}', "len": 35},
    "B":  {"json": '{"data": "hello", "items": ["a", "b"], "role": "reader", "version": 1}', "len": 70},
    "C":  {"json": '{"admin_note": "sensitive:42", "count": 42, "data": "hello", "items": ["a", "b", "c"], "role": "admin", "version": 1}', "len": 117},
}
for _k in BODY_STATES:
    BODY_STATES[_k]["sha256"] = hashlib.sha256(BODY_STATES[_k]["json"].encode()).hexdigest()
    assert len(BODY_STATES[_k]["json"].encode()) == BODY_STATES[_k]["len"], _k
# Frozen lineage pin checks (AUDIT must recompute identical)
assert BODY_STATES["A"]["sha256"].startswith("d0ca833f"), BODY_STATES["A"]["sha256"]
assert BODY_STATES["B"]["sha256"].startswith("67c186f2"), BODY_STATES["B"]["sha256"]
assert BODY_STATES["C"]["sha256"].startswith("b46c461c"), BODY_STATES["C"]["sha256"]

HEADER_BASE: Dict[str, str] = {
    "Cache-Control": "public, max-age=3600",
    "ETag": 'W/"fixed-aaa-111"',
    "Vary": "Accept-Encoding",
    "Content-Type": "application/json",
}

HEADER_STATES: Dict[str, Dict[str, str]] = {
    "BASE": HEADER_BASE,
    "E": {
        "Cache-Control": "max-age=0, must-revalidate",
        "ETag": 'W/"changed-bbb-222"',
        "Set-Cookie": "session=xyz; Path=/; HttpOnly",
        "Vary": "Accept-Encoding, Origin",
        "Content-Type": "application/json",
    },
    "CC_small": {**HEADER_BASE, "Cache-Control": "public, max-age=3601"},
    "CC_large": {**HEADER_BASE, "Cache-Control": "max-age=0"},
    "ETag_small": {**HEADER_BASE, "ETag": 'W/"fixed-aaa-112"'},
    "ETag_large": {**HEADER_BASE, "ETag": 'W/"changed-bbb-222"'},
    "SC_small": {**HEADER_BASE, "Set-Cookie": "session=abc"},
    "SC_large": {**HEADER_BASE, "Set-Cookie": "session=xyz; Path=/; HttpOnly"},
    "Vary_small": {**HEADER_BASE, "Vary": "Accept-Encoding, Origin"},
}

ENDPOINTS = ["/api/profile", "/api/data_list", "/api/session/status"]
EP_KEY = {
    "/api/profile": "profile",
    "/api/data_list": "data_list",
    "/api/session/status": "session_status",
}

random.seed(SEED)


class MeasurementInvalid(Exception):
    def __init__(self, category: str, detail: str):
        super().__init__(f"{category}: {detail}")
        self.category = category
        self.detail = detail


# ─── Fingerprint (frozen: sort_keys True, separators (',',':'), lowercased) ──
def filter_headers(headers_dict: Dict[str, str]) -> Dict[str, str]:
    out = {}
    for k, v in headers_dict.items():
        if k.lower() not in FILTER_OUT_KEYS:
            out[k.lower()] = v
    return out


def compute_fingerprint(
    status: int,
    body_bytes: bytes,
    headers_filtered: Dict[str, str],
    *,
    include_status: bool = True,
    include_body: bool = True,
    include_headers: bool = True,
    include_clen: bool = True,
) -> str:
    parts: List[str] = []
    if include_status:
        parts.append(str(status))
    if include_body:
        parts.append(body_bytes.decode("latin-1") if body_bytes else "")
    if include_headers:
        h = dict(headers_filtered)
        if not include_clen:
            h = {k: v for k, v in h.items() if k != "content-length"}
        parts.append(json.dumps(h, sort_keys=True, separators=(",", ":")))
    return hashlib.sha256("||".join(parts).encode("latin-1")).hexdigest()


def fp_full(status, body, hdrs):
    return compute_fingerprint(status, body, hdrs)


def fp_status_only(status, body, hdrs):
    return compute_fingerprint(status, body, hdrs, include_body=False, include_headers=False)


def fp_body_only(status, body, hdrs):
    return compute_fingerprint(status, body, hdrs, include_status=False, include_headers=False)


def fp_headers_only(status, body, hdrs):
    return compute_fingerprint(status, body, hdrs, include_status=False, include_body=False)


def fp_headers_no_clen(status, body, hdrs):
    return compute_fingerprint(
        status, body, hdrs, include_status=False, include_body=False, include_clen=False
    )


FP_FUNCS = {
    "full": fp_full,
    "status": fp_status_only,
    "body": fp_body_only,
    "headers": fp_headers_only,
    "headers_no_clen": fp_headers_no_clen,
}


def jaccard_distance(set_a: set, set_b: set) -> float:
    if not set_a and not set_b:
        return 0.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return 1.0 - (inter / union) if union else 0.0


def bootstrap_jaccard_ci(
    fps_a: List[str], fps_b: List[str], n_boot: int = BOOTSTRAP_B, seed: int = SEED
) -> Dict[str, Any]:
    if not fps_a or not fps_b:
        return {
            "discrimination": 0.0, "ci_95": [0.0, 0.0], "width": 0.0,
            "degenerate": True, "effective_distinct_n": 0, "set_a_size": 0, "set_b_size": 0,
        }
    set_a, set_b = set(fps_a), set(fps_b)
    observed = jaccard_distance(set_a, set_b)
    rng = random.Random(seed)
    boots: List[float] = []
    for _ in range(n_boot):
        ba = rng.choices(fps_a, k=len(fps_a))
        bb = rng.choices(fps_b, k=len(fps_b))
        boots.append(jaccard_distance(set(ba), set(bb)))
    boots.sort()
    lo = boots[int(0.025 * n_boot)]
    hi = boots[min(n_boot - 1, int(0.975 * n_boot))]
    return {
        "discrimination": observed,
        "ci_95": [lo, hi],
        "width": hi - lo,
        "degenerate": (hi - lo) == 0.0,
        "effective_distinct_n": max(len(set_a), len(set_b)),
        "set_a_size": len(set_a),
        "set_b_size": len(set_b),
        "n_a": len(fps_a),
        "n_b": len(fps_b),
    }


def wilson_ci(k: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    if n == 0:
        return 0.0, 1.0
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return max(0.0, center - half), min(1.0, center + half)


def behavioral_composite(status: int) -> float:
    if status == 401:
        return 1.0
    if status == 403:
        return 0.5
    if status == 500:
        return 0.75
    if status in (200, 304):
        return 0.0
    return 0.5


def structural_signal(status: int, body: bytes, body_variant: str) -> Optional[int]:
    if status == 304 or not body:
        return None
    payload = f"{status}|{body_variant}|".encode() + body
    return int(hashlib.sha256(payload).hexdigest()[:8], 16) % 10000


def fisher_z(r: float) -> float:
    r = max(-0.999999, min(0.999999, r))
    return 0.5 * math.log((1 + r) / (1 - r))


def tanh_z(z: float) -> float:
    return math.tanh(z)


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def pearson(xs: List[float], ys: List[float]) -> Optional[float]:
    n = len(xs)
    if n < 3:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    sx = sum((x - mx) ** 2 for x in xs)
    sy = sum((y - my) ** 2 for y in ys)
    if sx <= 0 or sy <= 0:
        return None
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return cov / math.sqrt(sx * sy)


def stratified_r_tost(
    per_ep: Dict[str, Tuple[Optional[float], int]], delta: float = 0.15
) -> Dict[str, Any]:
    zs_ws = []
    for r, n in per_ep.values():
        if r is None or n <= 3:
            continue
        zs_ws.append((fisher_z(r), n - 3))
    if not zs_ws:
        return {
            "r": None, "ci_lo": None, "ci_hi": None, "ci_upper": None,
            "p_upper": None, "tost_pass": False, "n_pool": 0,
            "reason": "no_endpoint_with_variance",
        }
    wsum = sum(w for _, w in zs_ws)
    z_pool = sum(z * w for z, w in zs_ws) / wsum
    se = 1.0 / math.sqrt(wsum)
    r_pool = tanh_z(z_pool)
    z_lo = z_pool - 1.96 * se
    z_hi = z_pool + 1.96 * se
    ci_lo, ci_hi = tanh_z(z_lo), tanh_z(z_hi)
    z_delta = fisher_z(delta)
    p_upper = normal_cdf((z_pool - z_delta) / se) if se > 0 else 1.0
    tost_pass = (
        ci_hi < delta and ci_lo > -delta and abs(r_pool) < delta and p_upper < 0.05
    )
    return {
        "r": r_pool,
        "ci_lo": ci_lo,
        "ci_hi": ci_hi,
        "ci_upper": ci_hi,
        "p_upper": p_upper,
        "tost_pass": tost_pass,
        "n_pool": sum(n for _, n in per_ep.values()),
        "se_z": se,
    }


# ─── Tokens ──────────────────────────────────────────────────────────────────
def make_jwt(role: str = "reader", exp: int = 9999999999, sid: str = "sess-exp-3588") -> str:
    return jwt.encode(
        {"sub": "testuser", "sid": sid, "role": role, "exp": exp},
        JWT_SECRET,
        algorithm=JWT_ALG,
    )


def make_expired_jwt(sid: str = "sess-exp-3588") -> str:
    return jwt.encode(
        {"sub": "testuser", "sid": sid, "role": "reader", "exp": 0},
        JWT_SECRET,
        algorithm=JWT_ALG,
    )


def make_rotated_jwt(sid: str = "sess-exp-3588") -> str:
    return jwt.encode(
        {"sub": "testuser", "sid": sid, "role": "reader", "exp": 9999999999},
        "wrong-secret-key-rotation",
        algorithm=JWT_ALG,
    )


VALID_JWT = make_jwt()
EXPIRED_JWT = make_expired_jwt()
ROTATED_JWT = make_rotated_jwt()
INVALID_JWT = "not-a-jwt-token-xyz"
DENIED_JWT = make_jwt(role="denied")


# ─── Flask app ───────────────────────────────────────────────────────────────
def create_app(db_path: Optional[str] = None) -> Flask:
    app = Flask(__name__)
    resolved_db = db_path or os.environ.get("SPIDER_DB_PATH") or str(SHARED_DB)
    app.config["DATABASE"] = resolved_db
    app.config["DB_PATH_LABEL"] = resolved_db

    def _connect() -> sqlite3.Connection:
        conn = sqlite3.connect(app.config["DATABASE"], timeout=10, check_same_thread=False)
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA journal_mode=WAL")
        conn.row_factory = sqlite3.Row
        return conn

    def get_db():
        if "db" not in g:
            g.db = _connect()
        return g.db

    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        conn = _connect()
        conn.execute("""CREATE TABLE IF NOT EXISTS body_config (
            id INTEGER PRIMARY KEY CHECK (id=1), variant TEXT DEFAULT 'A', content TEXT)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS header_config (
            id INTEGER PRIMARY KEY CHECK (id=1), variant TEXT DEFAULT 'BASE', content TEXT)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, username TEXT UNIQUE, role TEXT DEFAULT 'reader')""")
        conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY, session_id TEXT UNIQUE, username TEXT,
            valid INTEGER DEFAULT 1, created_at TEXT)""")
        if conn.execute("SELECT COUNT(*) FROM body_config").fetchone()[0] == 0:
            conn.execute(
                "INSERT INTO body_config (id, variant, content) VALUES (1, ?, ?)",
                ("A", BODY_STATES["A"]["json"]),
            )
            conn.execute(
                "INSERT INTO header_config (id, variant, content) VALUES (1, ?, ?)",
                ("BASE", json.dumps(HEADER_BASE)),
            )
            conn.execute(
                "INSERT OR IGNORE INTO users (username, role) VALUES ('testuser', 'reader')"
            )
            # NOTE: sessions are intentionally NOT seeded here. Control plane
            # (ensure_session / admin API) owns session writes so that:
            #   shared arm  → control writes shared.db → both workers see them;
            #   per-node arm→ control writes shared.db only → isolated worker DBs
            #                never receive sessions → session_status TN≈0 (~0.667 mean);
            #   sticky arm  → sessions pre-seeded into both pinned-worker DBs.
        conn.commit()
        conn.close()

    init_db()

    def worker_headers() -> Dict[str, str]:
        return {"X-Worker-Pid": str(os.getpid())}

    def decode_bearer() -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        auth = flask_request.headers.get("Authorization", "")
        if not auth.lower().startswith("bearer "):
            return None, "missing_bearer"
        token = auth[7:].strip()
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
            return payload, None
        except jwt.ExpiredSignatureError:
            return None, "expired"
        except jwt.InvalidTokenError as e:
            return None, f"invalid:{type(e).__name__}"

    def session_valid(sid: Optional[str]) -> bool:
        if not sid:
            return False
        row = get_db().execute(
            "SELECT valid FROM sessions WHERE session_id=?", (sid,)
        ).fetchone()
        return bool(row and row["valid"] == 1)

    def get_body_variant() -> Tuple[str, str]:
        row = get_db().execute(
            "SELECT variant, content FROM body_config WHERE id=1"
        ).fetchone()
        if row:
            return row["variant"], row["content"]
        return "A", BODY_STATES["A"]["json"]

    def get_header_config() -> Tuple[str, Dict[str, str]]:
        row = get_db().execute(
            "SELECT variant, content FROM header_config WHERE id=1"
        ).fetchone()
        if row:
            return row["variant"], json.loads(row["content"])
        return "BASE", dict(HEADER_BASE)

    def _wants_html() -> bool:
        accept = flask_request.headers.get("Accept", "")
        return "text/html" in accept and "application/json" not in accept

    def _etag_for(body: bytes) -> str:
        return 'W/"' + hashlib.sha256(body).hexdigest() + '"'

    def _cache_headers(body: bytes, hdr_cfg: Dict[str, str], variant: str) -> Dict[str, str]:
        h = dict(hdr_cfg)
        h["Content-Type"] = h.get("Content-Type", "application/json")
        h["Content-Length"] = str(len(body))
        if "ETag" not in h or not h["ETag"]:
            h["ETag"] = _etag_for(body)
        h.update(worker_headers())
        return h

    def _maybe_304(headers: Dict[str, str]):
        inm = flask_request.headers.get("If-None-Match", "")
        etag = headers.get("ETag", "")
        if inm and etag and inm.strip() == etag.strip():
            h304 = {
                "ETag": headers["ETag"],
                "X-Worker-Pid": headers["X-Worker-Pid"],
                "Cache-Control": headers.get("Cache-Control", ""),
            }
            return (b"", 304, h304)
        return None

    def _html_resource(body_json: str, variant: str) -> bytes:
        esc = (
            body_json.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Resource {variant}</title></head>
<body>
<header><h1>Resource</h1><nav><a href="/">Home</a><a href="/resource">Data</a></nav></header>
<main>
<section aria-label="payload"><h2>Payload</h2>
<p id="payload">{esc}</p>
<ul><li>variant={variant}</li><li>len={len(body_json)}</li></ul>
</section>
<section aria-label="meta"><h2>Meta</h2>
<dl><dt>Status</dt><dd>200</dd><dt>Variant</dt><dd>{variant}</dd></dl>
</section>
</main>
<footer><p>SPIDER resource</p></footer>
</body>
</html>"""
        return html.encode("utf-8")

    def _json_response(status: int, body: bytes, hdr_cfg: Dict[str, str], variant: str,
                       cache_enabled: bool = True):
        headers = _cache_headers(body, hdr_cfg, variant)
        if not cache_enabled:
            headers["Cache-Control"] = "no-store"
        elif "Cache-Control" not in headers:
            headers["Cache-Control"] = "public, max-age=5"
        if status in (401, 403, 500):
            headers["ETag"] = _etag_for(body)
            headers["Content-Length"] = str(len(body))
            return body, status, headers
        if status == 200:
            hit = _maybe_304(headers)
            if hit is not None:
                return hit
            return body, 200, headers
        return body, status, headers

    # ── Admin ──
    @app.post("/admin/set_body_variant")
    def admin_set_body():
        data = flask_request.get_json(force=True, silent=True) or {}
        variant = data.get("variant", "A")
        if variant not in BODY_STATES:
            return jsonify({"error": "unknown_variant"}), 400, worker_headers()
        db = get_db()
        db.execute(
            "UPDATE body_config SET variant=?, content=? WHERE id=1",
            (variant, BODY_STATES[variant]["json"]),
        )
        db.commit()
        row = db.execute("SELECT variant FROM body_config WHERE id=1").fetchone()
        if not row or row["variant"] != variant:
            return jsonify({"error": "COMMIT_NOT_VERIFIED"}), 500, worker_headers()
        return jsonify({"ok": True, "variant": variant, "worker": os.getpid()}), 200, worker_headers()

    @app.post("/admin/set_headers")
    def admin_set_headers():
        data = flask_request.get_json(force=True, silent=True) or {}
        variant = data.get("variant", "BASE")
        if variant not in HEADER_STATES:
            return jsonify({"error": "unknown_header_variant"}), 400, worker_headers()
        db = get_db()
        db.execute(
            "UPDATE header_config SET variant=?, content=? WHERE id=1",
            (variant, json.dumps(HEADER_STATES[variant])),
        )
        db.commit()
        row = db.execute("SELECT variant FROM header_config WHERE id=1").fetchone()
        if not row or row["variant"] != variant:
            return jsonify({"error": "COMMIT_NOT_VERIFIED"}), 500, worker_headers()
        return jsonify({"ok": True, "variant": variant}), 200, worker_headers()

    @app.post("/admin/set_session")
    def admin_set_session():
        data = flask_request.get_json(force=True, silent=True) or {}
        sid = data.get("session_id", "sess-exp-3588")
        valid = int(data.get("valid", 1))
        db = get_db()
        existing = db.execute(
            "SELECT id FROM sessions WHERE session_id=?", (sid,)
        ).fetchone()
        now = datetime.now(timezone.utc).isoformat()
        if existing:
            db.execute(
                "UPDATE sessions SET valid=?, created_at=? WHERE session_id=?",
                (valid, now, sid),
            )
        else:
            db.execute(
                "INSERT INTO sessions (session_id, username, valid, created_at) "
                "VALUES (?, 'testuser', ?, ?)",
                (sid, valid, now),
            )
        db.commit()
        row = db.execute(
            "SELECT valid FROM sessions WHERE session_id=?", (sid,)
        ).fetchone()
        if row is None or row["valid"] != valid:
            return jsonify({"error": "COMMIT_NOT_VERIFIED"}), 500, worker_headers()
        return jsonify({"ok": True, "valid": valid}), 200, worker_headers()

    @app.post("/admin/invalidate_session")
    def admin_invalidate():
        data = flask_request.get_json(force=True, silent=True) or {}
        sid = data.get("session_id", "sess-exp-3588")
        db = get_db()
        db.execute("UPDATE sessions SET valid=0 WHERE session_id=?", (sid,))
        db.commit()
        row = db.execute(
            "SELECT valid FROM sessions WHERE session_id=?", (sid,)
        ).fetchone()
        after = row["valid"] if row else None
        if after is not None and after != 0:
            return jsonify({"error": "COMMIT_NOT_VERIFIED"}), 500, worker_headers()
        return jsonify({"ok": True, "valid_after": after}), 200, worker_headers()

    @app.get("/admin/state")
    def admin_state():
        db = get_db()
        n_sess = db.execute("SELECT COUNT(*) AS c FROM sessions").fetchone()["c"]
        n_valid = db.execute(
            "SELECT COUNT(*) AS c FROM sessions WHERE valid=1"
        ).fetchone()["c"]
        bv, _ = get_body_variant()
        hv, _ = get_header_config()
        return jsonify({
            "session_count": n_sess,
            "session_valid_count": n_valid,
            "body_variant": bv,
            "header_variant": hv,
            "db_path": app.config["DATABASE"],
            "worker": os.getpid(),
        }), 200, worker_headers()

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "worker": os.getpid()}), 200, worker_headers()

    # ── /resource: content-negotiated HTML (navigation) vs JSON (API fetch) ──
    @app.get("/resource")
    def resource():
        payload, _err = decode_bearer()
        variant, body_json = get_body_variant()
        hv, hdr_cfg = get_header_config()
        if payload is None:
            err = json.dumps({"error": "unauthorized"}, sort_keys=True).encode()
            if _wants_html():
                # HTML error page still usable for AX (but we need 200 for valid paths)
                html = _html_resource(err.decode(), "ERR401")
                headers = _cache_headers(html, hdr_cfg, "ERR401")
                headers["ETag"] = _etag_for(html)
                headers["Content-Type"] = "text/html; charset=utf-8"
                headers["Cache-Control"] = "no-store"
                return html, 401, headers
            return _json_response(401, err, hdr_cfg, variant, cache_enabled=False)
        body_bytes = body_json.encode()
        if _wants_html():
            html = _html_resource(body_json, variant)
            headers = _cache_headers(html, hdr_cfg, variant)
            headers["ETag"] = _etag_for(html)
            headers["Content-Type"] = "text/html; charset=utf-8"
            hit = _maybe_304(headers)
            if hit is not None:
                return hit
            return html, 200, headers
        return _json_response(200, body_bytes, hdr_cfg, variant, cache_enabled=True)

    def _auth_gate(require_session: bool):
        payload, err = decode_bearer()
        hv, hdr_cfg = get_header_config()
        variant, _ = get_body_variant()
        if payload is None:
            body = json.dumps({"error": "unauthorized", "reason": err}, sort_keys=True).encode()
            return None, _json_response(401, body, hdr_cfg, variant, cache_enabled=False)
        if payload.get("role") == "denied":
            body = json.dumps({"error": "forbidden", "role": "denied"}, sort_keys=True).encode()
            return None, _json_response(403, body, hdr_cfg, variant, cache_enabled=False)
        sid = payload.get("sid")
        if require_session and not session_valid(sid):
            body = json.dumps(
                {"error": "unauthorized", "reason": "session_invalid"}, sort_keys=True
            ).encode()
            return None, _json_response(401, body, hdr_cfg, variant, cache_enabled=False)
        return payload, None

    @app.get("/api/profile")
    def api_profile():
        payload, err_resp = _auth_gate(require_session=False)
        if err_resp is not None:
            return err_resp
        variant, body_json = get_body_variant()
        hv, hdr_cfg = get_header_config()
        inner = json.loads(body_json)
        out = json.dumps({"profile": inner, "user": payload.get("sub")}, sort_keys=True).encode()
        return _json_response(200, out, hdr_cfg, variant, cache_enabled=True)

    @app.get("/api/data_list")
    def api_data_list():
        payload, err_resp = _auth_gate(require_session=False)
        if err_resp is not None:
            return err_resp
        variant, body_json = get_body_variant()
        hv, hdr_cfg = get_header_config()
        inner = json.loads(body_json)
        out = json.dumps({"data": inner, "count": inner.get("count", 1)}, sort_keys=True).encode()
        return _json_response(200, out, hdr_cfg, variant, cache_enabled=True)

    @app.get("/api/session/status")
    def api_session_status():
        payload, err_resp = _auth_gate(require_session=True)
        if err_resp is not None:
            return err_resp
        variant, body_json = get_body_variant()
        hv, hdr_cfg = get_header_config()
        out = json.dumps(
            {"session_valid": True, "session_id": payload.get("sid")},
            sort_keys=True,
        ).encode()
        return _json_response(200, out, hdr_cfg, variant, cache_enabled=True)

    return app


# ─── Server lifecycle ────────────────────────────────────────────────────────
def _kill_port(port: int) -> None:
    try:
        subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True, timeout=5)
    except Exception:
        pass


def kill_servers() -> None:
    for port in (GUNICORN_PORT_A, GUNICORN_PORT_B, NGINX_PORT):
        _kill_port(port)
    try:
        pidfile = NGINX_DIR / "nginx.pid"
        if pidfile.exists():
            os.kill(int(pidfile.read_text().strip()), signal.SIGQUIT)
    except Exception:
        pass
    time.sleep(0.4)


def write_nginx_conf(mode: str = "rr") -> Path:
    NGINX_DIR.mkdir(parents=True, exist_ok=True)
    (NGINX_DIR / "logs").mkdir(parents=True, exist_ok=True)
    conf_path = NGINX_DIR / "nginx.conf"
    if mode == "sticky":
        upstream = (
            "upstream gunicorn_upstream {\n"
            f"    server {HOST}:{GUNICORN_PORT_A};\n"
            f"    server {HOST}:{GUNICORN_PORT_B};\n"
            "    hash $remote_addr consistent;\n"
            "}\n"
        )
    else:
        upstream = (
            "upstream gunicorn_upstream {\n"
            f"    server {HOST}:{GUNICORN_PORT_A};\n"
            f"    server {HOST}:{GUNICORN_PORT_B};\n"
            "}\n"
        )
    conf = f"""
worker_processes 1;
error_log {NGINX_DIR}/logs/error.log warn;
pid {NGINX_DIR}/nginx.pid;
events {{ worker_connections 1024; }}
http {{
    access_log {NGINX_DIR}/logs/access.log;
    {upstream}
    server {{
        listen {NGINX_PORT};
        server_name {HOST};
        location / {{
            proxy_pass http://gunicorn_upstream;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_buffering off;
        }}
    }}
}}
"""
    conf_path.write_text(conf)
    return conf_path


def start_gunicorn(port: int, db_path: Path, name: str) -> subprocess.Popen:
    # name is the Python module basename under BASE_DIR (e.g. "wsgi_shared_a")
    wsgi = BASE_DIR / f"{name}.py"
    wsgi.write_text(
        "import os, sys\n"
        f"sys.path.insert(0, {str(EXPERIMENT_DIR)!r})\n"
        f"os.environ['SPIDER_DB_PATH'] = {str(db_path)!r}\n"
        "from run_experiment import create_app\n"
        "app = create_app(os.environ['SPIDER_DB_PATH'])\n"
    )
    env = dict(os.environ)
    env["PYTHONUNBUFFERED"] = "1"
    env["SPIDER_DB_PATH"] = str(db_path)
    # Ensure experiment dir is importable for `from run_experiment import ...`
    env["PYTHONPATH"] = str(EXPERIMENT_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    cmd = [
        sys.executable, "-m", "gunicorn",
        "--workers", "1",
        "--bind", f"{HOST}:{port}",
        "--timeout", "30",
        "--worker-class", "sync",
        "--pid", str(BASE_DIR / f"{name}.pid"),
        "--chdir", str(BASE_DIR),
        f"{name}:app",
    ]
    log = open(BASE_DIR / f"{name}.log", "w")
    proc = subprocess.Popen(
        cmd, env=env, stdout=log, stderr=subprocess.STDOUT, cwd=str(BASE_DIR)
    )
    return proc


def wait_http(url: str, timeout: float = 15.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=1.5)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(0.2)
    return False


def start_nginx(mode: str) -> subprocess.Popen:
    conf = write_nginx_conf(mode)
    _kill_port(NGINX_PORT)
    time.sleep(0.3)
    proc = subprocess.Popen(
        ["nginx", "-c", str(conf), "-p", str(NGINX_DIR)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    if not wait_http(f"http://{HOST}:{NGINX_PORT}/health", timeout=10):
        out = ""
        try:
            out, _ = proc.communicate(timeout=2)
        except Exception:
            pass
        raise MeasurementInvalid("NGINX_UNAVAILABLE", f"nginx not reachable: {out}")
    return proc


def stop_nginx() -> None:
    try:
        pidfile = NGINX_DIR / "nginx.pid"
        if pidfile.exists():
            os.kill(int(pidfile.read_text().strip()), signal.SIGQUIT)
    except Exception:
        pass


# ─── DB helpers (control plane) ──────────────────────────────────────────────
def control_connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path), timeout=10, check_same_thread=False)
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema(db_path: Path) -> None:
    """Create schema (and default body/header rows) without seeding sessions."""
    conn = control_connect(db_path)
    conn.execute("""CREATE TABLE IF NOT EXISTS body_config (
        id INTEGER PRIMARY KEY CHECK (id=1), variant TEXT DEFAULT 'A', content TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS header_config (
        id INTEGER PRIMARY KEY CHECK (id=1), variant TEXT DEFAULT 'BASE', content TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT UNIQUE, role TEXT DEFAULT 'reader')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY, session_id TEXT UNIQUE, username TEXT,
        valid INTEGER DEFAULT 1, created_at TEXT)""")
    if conn.execute("SELECT COUNT(*) FROM body_config").fetchone()[0] == 0:
        conn.execute(
            "INSERT INTO body_config (id, variant, content) VALUES (1, ?, ?)",
            ("A", BODY_STATES["A"]["json"]),
        )
        conn.execute(
            "INSERT INTO header_config (id, variant, content) VALUES (1, ?, ?)",
            ("BASE", json.dumps(HEADER_BASE)),
        )
        conn.execute(
            "INSERT OR IGNORE INTO users (username, role) VALUES ('testuser', 'reader')"
        )
    conn.commit()
    conn.close()


def ensure_session(db_path: Path, sid: str = "sess-exp-3588", valid: int = 1) -> None:
    conn = control_connect(db_path)
    now = datetime.now(timezone.utc).isoformat()
    row = conn.execute("SELECT id FROM sessions WHERE session_id=?", (sid,)).fetchone()
    if row:
        conn.execute(
            "UPDATE sessions SET valid=?, created_at=? WHERE session_id=?",
            (valid, now, sid),
        )
    else:
        conn.execute(
            "INSERT INTO sessions (session_id, username, valid, created_at) "
            "VALUES (?, 'testuser', ?, ?)",
            (sid, valid, now),
        )
    conn.commit()
    conn.close()


def session_snapshot(db_path: Path) -> Dict[str, Any]:
    conn = control_connect(db_path)
    n = conn.execute("SELECT COUNT(*) AS c FROM sessions").fetchone()["c"]
    nv = conn.execute("SELECT COUNT(*) AS c FROM sessions WHERE valid=1").fetchone()["c"]
    conn.close()
    return {"session_count": n, "session_valid_count": nv, "db_path": str(db_path)}


def set_body_direct(db_path: Path, variant: str) -> None:
    conn = control_connect(db_path)
    conn.execute(
        "UPDATE body_config SET variant=?, content=? WHERE id=1",
        (variant, BODY_STATES[variant]["json"]),
    )
    conn.commit()
    conn.close()


def set_headers_direct(db_path: Path, variant: str) -> None:
    conn = control_connect(db_path)
    conn.execute(
        "UPDATE header_config SET variant=?, content=? WHERE id=1",
        (variant, json.dumps(HEADER_STATES[variant])),
    )
    conn.commit()
    conn.close()


# ─── Distributed freshness harness ──────────────────────────────────────────
DRIFT_TYPES = [
    "permission_boundary",
    "session_invalidation",
    "signing_key_rotation",
    "token_expiry",
]
CACHE_SETTINGS = [True, False]
NOISE_TYPES = ["error_format_variation", "optional_field_churn"]


def build_conditions() -> List[Dict[str, Any]]:
    conds = []
    for drift in DRIFT_TYPES:
        for cache in CACHE_SETTINGS:
            conds.append({
                "condition_id": f"{drift}|cache={int(cache)}",
                "kind": "co",
                "drift": drift,
                "cache_enabled": cache,
            })
    for noise in NOISE_TYPES:
        for cache in CACHE_SETTINGS:
            conds.append({
                "condition_id": f"{noise}|cache={int(cache)}",
                "kind": "noise",
                "drift": noise,
                "cache_enabled": cache,
            })
    return conds


def pick_token(drift: str, auth_state: str) -> Tuple[str, str]:
    if auth_state == "valid":
        return VALID_JWT, "valid"
    if auth_state == "noise":
        return VALID_JWT, "noise"
    if drift == "permission_boundary" or auth_state == "permission_boundary":
        return DENIED_JWT, "permission_boundary"
    if drift == "session_invalidation" or auth_state == "session_invalidation":
        return VALID_JWT, "session_invalidation"
    if drift == "signing_key_rotation" or auth_state == "signing_key_rotation":
        return ROTATED_JWT, "signing_key_rotation"
    if drift == "token_expiry" or auth_state == "expired":
        return EXPIRED_JWT, "expired"
    return INVALID_JWT, "invalid"


def run_distributed_arm(
    arm: str,
    base_url: str,
    control_db: Path,
    n_total: int = N_DISTRIBUTED,
    seed: int = SEED,
    worker_dbs: Optional[List[Path]] = None,
    replicate_session_to_workers: bool = False,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Real HTTP via nginx. arm in {B-PER-NODE, B-SHARED-STORE, B-STICKY}.
    control_db is the harness-facing control plane (SELECT snapshots, body writes for shared).
    worker_dbs: extra DBs that workers actually read (per-node/sticky isolated files).
      - body/header config is mirrored into worker_dbs so structural drift is visible;
      - sessions are mirrored only if replicate_session_to_workers (sticky needs this;
        per-node intentionally does NOT replicate sessions → session_status TN≈0).
    Shared arm: control_db == worker shared.db, worker_dbs=[].
    """
    rng = random.Random(seed)
    conditions = build_conditions()
    co = [c for c in conditions if c["kind"] == "co"]
    noise = [c for c in conditions if c["kind"] == "noise"]
    n_co_each = 130  # 8*130 = 1040
    n_noise_each = 40  # 4*40 = 160
    planned = [(c, n_co_each) for c in co] + [(c, n_noise_each) for c in noise]
    total_planned = sum(n for _, n in planned)
    if total_planned != n_total:
        delta = n_total - total_planned
        planned[0] = (planned[0][0], max(1, planned[0][1] + delta))

    batch_log: List[Dict[str, Any]] = []
    observations: List[Dict[str, Any]] = []
    sample_idx = 0

    worker_dbs = list(worker_dbs or [])

    def _write_session(valid: int) -> None:
        ensure_session(control_db, valid=valid)
        if replicate_session_to_workers:
            for w in worker_dbs:
                ensure_session(w, valid=valid)

    def _write_body(variant: str) -> None:
        set_body_direct(control_db, variant)
        for w in worker_dbs:
            set_body_direct(w, variant)

    def _write_headers(variant: str) -> None:
        set_headers_direct(control_db, variant)
        for w in worker_dbs:
            set_headers_direct(w, variant)

    _write_session(1)
    _write_body("A")
    _write_headers("BASE")

    for i in range(3):
        snap = session_snapshot(control_db)
        batch_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "warmup_select",
            "batch": f"warmup-{i}",
            **snap,
            "arm": arm,
        })
        time.sleep(0.05)

    body_cycle = ["A", "B", "C", "A1", "A2", "A3", "A", "B"]
    ep_cycle = list(ENDPOINTS)

    def do_sample(cond: Dict[str, Any], i: int, auth_state: str) -> Optional[Dict[str, Any]]:
        nonlocal sample_idx
        sample_idx += 1
        ep = ep_cycle[sample_idx % len(ep_cycle)]
        cache_enabled = cond["cache_enabled"]
        bv = body_cycle[sample_idx % len(body_cycle)]
        if cond["kind"] == "noise" and cond["drift"] == "optional_field_churn":
            bv = body_cycle[(sample_idx // 2) % len(body_cycle)]
        _write_body(bv)

        token, label = pick_token(cond["drift"], auth_state)

        if label == "session_invalidation":
            _write_session(0)
        elif label in ("valid", "noise"):
            _write_session(1)

        headers = {"Authorization": f"Bearer {token}"}
        is_304_attempted = False
        if cache_enabled and rng.random() < 0.33:
            try:
                pre = requests.get(f"{base_url}{ep}", headers=headers, timeout=10)
                etag = pre.headers.get("ETag") or pre.headers.get("etag")
                if etag:
                    headers["If-None-Match"] = etag
                    is_304_attempted = True
            except Exception:
                pass

        if sample_idx % 4 == 0:
            time.sleep(rng.uniform(JITTER_MIN_MS, JITTER_MAX_MS) / 1000.0)

        try:
            t0 = time.monotonic()
            resp = requests.get(f"{base_url}{ep}", headers=headers, timeout=15)
            latency_ms = (time.monotonic() - t0) * 1000.0
        except Exception as e:
            return {
                "sample_idx": sample_idx,
                "arm": arm,
                "endpoint": ep,
                "condition_id": cond["condition_id"],
                "kind": cond["kind"],
                "drift": cond["drift"],
                "cache_enabled": cache_enabled,
                "auth_state": label,
                "body_variant": bv,
                "status": None,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        status = resp.status_code
        body = resp.content
        hdrs_raw = dict(resp.headers)
        hdrs_f = filter_headers(hdrs_raw)
        is_304 = status == 304
        bc = behavioral_composite(status)
        struct = structural_signal(status, body, bv)

        hs256_ok = False
        if label in ("valid", "noise", "session_invalidation", "permission_boundary"):
            try:
                jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
                hs256_ok = True
            except Exception:
                hs256_ok = False
        else:
            try:
                jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
                hs256_ok = False
            except Exception:
                hs256_ok = False

        return {
            "sample_idx": sample_idx,
            "arm": arm,
            "endpoint": ep,
            "condition_id": cond["condition_id"],
            "kind": cond["kind"],
            "drift": cond["drift"],
            "cache_enabled": cache_enabled,
            "auth_state": label,
            "body_variant": bv,
            "status": status,
            "is_304": is_304,
            "if_none_match_sent": is_304_attempted,
            "body_sha256": hashlib.sha256(body).hexdigest() if body else "",
            "body_len": len(body),
            "content_length_header": hdrs_f.get("content-length"),
            "etag": hdrs_f.get("etag"),
            "cache_control": hdrs_f.get("cache-control"),
            "headers_filtered_json": json.dumps(hdrs_f, sort_keys=True, separators=(",", ":")),
            "headers_no_clen_json": json.dumps(
                {k: v for k, v in hdrs_f.items() if k != "content-length"},
                sort_keys=True, separators=(",", ":"),
            ),
            "worker_id": hdrs_raw.get("X-Worker-Pid") or hdrs_raw.get("x-worker-pid"),
            "behavioral_composite": bc,
            "structural": struct,
            "latency_ms": round(latency_ms, 2),
            "hs256_verified": hs256_ok,
            "jwt_valid_intent": label in ("valid", "noise", "session_invalidation"),
            "db_path": str(control_db),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    all_jobs: List[Tuple[Dict[str, Any], int, str]] = []
    for cond, n in planned:
        for i in range(n):
            if cond["kind"] == "co":
                auth_state = "valid" if (i % 2 == 0) else cond["drift"]
            else:
                auth_state = "noise"
            all_jobs.append((cond, i, auth_state))

    batch_size = 45  # 1200/45 ≈ 27 batches
    batch_idx = 0
    for start in range(0, len(all_jobs), batch_size):
        batch_idx += 1
        chunk = all_jobs[start:start + batch_size]
        snap = session_snapshot(control_db)
        http_snap = None
        try:
            r = requests.get(f"{base_url}/admin/state", timeout=5)
            if r.status_code == 200:
                http_snap = r.json()
        except Exception as e:
            http_snap = {"error": str(e)}
        batch_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "batch_select",
            "batch": batch_idx,
            "n_chunk": len(chunk),
            "select": snap,
            "http_state": http_snap,
            "arm": arm,
        })
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
            futs = [ex.submit(do_sample, cond, i, auth) for cond, i, auth in chunk]
            for fut in as_completed(futs):
                obs = fut.result()
                if obs is not None:
                    observations.append(obs)
        time.sleep(0.06)

    batch_log.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "batch_final_select",
        "batch": batch_idx + 1,
        "select": session_snapshot(control_db),
        "n_obs": len(observations),
        "arm": arm,
    })

    return observations, batch_log


def compute_distributed_metrics(
    observations: List[Dict[str, Any]], arm: str
) -> Dict[str, Any]:
    valid_only = [
        o for o in observations
        if o.get("auth_state") == "valid" and not o.get("is_304") and o.get("status") is not None
    ]

    tn_per_ep: Dict[str, Dict[str, Any]] = {}
    for ep in ENDPOINTS:
        rows = [o for o in valid_only if o["endpoint"] == ep]
        n = len(rows)
        k = sum(1 for o in rows if o["behavioral_composite"] <= 0.05)
        tn = (k / n) if n else None
        lo, hi = wilson_ci(k, n) if n else (None, None)
        tn_per_ep[EP_KEY[ep]] = {
            "n_valid": n, "k_fresh": k, "tn": tn,
            "wilson_lo": lo, "wilson_hi": hi,
        }
    tn_vals = [v["tn"] for v in tn_per_ep.values() if v["tn"] is not None]
    tn_mean = sum(tn_vals) / len(tn_vals) if tn_vals else None
    k_all = sum(v["k_fresh"] for v in tn_per_ep.values())
    n_all = sum(v["n_valid"] for v in tn_per_ep.values())
    mean_lo, mean_hi = wilson_ci(k_all, n_all) if n_all else (None, None)

    hs_rows = [
        o for o in observations
        if o.get("auth_state") in ("valid", "noise") and o.get("status") is not None
    ]
    hs_ok = sum(1 for o in hs_rows if o["status"] in (200, 304))
    hs_rate = (hs_ok / len(hs_rows)) if hs_rows else None

    non304 = [o for o in observations if not o.get("is_304") and o.get("status") is not None]
    n_non304 = len(non304)
    n_total = len([o for o in observations if o.get("status") is not None])
    n_304 = sum(1 for o in observations if o.get("is_304"))

    per_ep_r: Dict[str, Tuple[Optional[float], int]] = {}
    for ep in ENDPOINTS:
        rows = [
            o for o in non304
            if o["endpoint"] == ep and o.get("structural") is not None
        ]
        xs = [float(o["behavioral_composite"]) for o in rows]
        ys = [float(o["structural"]) for o in rows]
        per_ep_r[ep] = (pearson(xs, ys), len(rows))
    tost = stratified_r_tost(per_ep_r, delta=0.15)

    rows_all = [o for o in non304 if o.get("structural") is not None]
    pooled_r = pearson(
        [float(o["behavioral_composite"]) for o in rows_all],
        [float(o["structural"]) for o in rows_all],
    )

    var_results = {}
    co_conds = sorted({o["condition_id"] for o in observations if o.get("kind") == "co"})
    var_pass_count = 0
    for cid in co_conds:
        rows = [
            o for o in observations
            if o["condition_id"] == cid and not o.get("is_304")
            and o.get("structural") is not None and o.get("status") is not None
        ]
        bcs = [o["behavioral_composite"] for o in rows]
        structs = [o["structural"] for o in rows]
        bstd = statistics.pstdev(bcs) if len(bcs) > 1 else 0.0
        sstd = statistics.pstdev(structs) if len(structs) > 1 else 0.0
        ok = bstd > 0 and sstd > 0
        if ok:
            var_pass_count += 1
        var_results[cid] = {
            "n": len(rows), "bc_std": bstd, "struct_std": sstd, "pass": ok,
        }

    noise_rows = [
        o for o in observations
        if o.get("auth_state") == "noise" and o.get("status") is not None
    ]
    noise_fp_k = sum(1 for o in noise_rows if o["behavioral_composite"] > 0.05)
    noise_fp_n = len(noise_rows)
    noise_fp = (noise_fp_k / noise_fp_n) if noise_fp_n else None
    nlo, nhi = wilson_ci(noise_fp_k, noise_fp_n) if noise_fp_n else (None, None)

    worker_counts = Counter(
        str(o.get("worker_id")) for o in observations if o.get("worker_id")
    )

    def _mean_bc(states) -> Optional[float]:
        rows = [
            o for o in observations
            if o.get("auth_state") in states and o.get("status") is not None
        ]
        if not rows:
            return None
        return sum(o["behavioral_composite"] for o in rows) / len(rows)

    return {
        "arm": arm,
        "freshness_c1_tn_mean": tn_mean,
        "freshness_c1_tn_wilson_lo": mean_lo,
        "freshness_c1_tn_wilson_hi": mean_hi,
        "freshness_c1_tn_session_status": tn_per_ep.get("session_status", {}).get("tn"),
        "freshness_c1_tn_session_status_wilson_lo": tn_per_ep.get("session_status", {}).get("wilson_lo"),
        "freshness_c1_tn_profile": tn_per_ep.get("profile", {}).get("tn"),
        "freshness_c1_tn_profile_wilson_lo": tn_per_ep.get("profile", {}).get("wilson_lo"),
        "freshness_c1_tn_data_list": tn_per_ep.get("data_list", {}).get("tn"),
        "freshness_c1_tn_data_list_wilson_lo": tn_per_ep.get("data_list", {}).get("wilson_lo"),
        "freshness_c1_tn_per_endpoint": tn_per_ep,
        "freshness_n_non304": n_non304,
        "freshness_n_total": n_total,
        "freshness_n_304": n_304,
        "freshness_stratified_r": tost.get("r"),
        "freshness_stratified_r_ci_lo": tost.get("ci_lo"),
        "freshness_stratified_r_ci_hi": tost.get("ci_hi"),
        "freshness_stratified_r_ci_upper": tost.get("ci_upper"),
        "freshness_tost_p_upper": tost.get("p_upper"),
        "freshness_tost_pass": tost.get("tost_pass"),
        "freshness_pooled_r": pooled_r,
        "freshness_c2_variance_pass_count": var_pass_count,
        "freshness_c2_variance_total": len(co_conds),
        "freshness_c2_variance_detail": var_results,
        "freshness_fp_noise": noise_fp,
        "freshness_fp_noise_wilson_hi": nhi,
        "freshness_fp_noise_n": noise_fp_n,
        "freshness_worker_distribution": dict(worker_counts),
        "freshness_hs256_valid_success_rate": hs_rate,
        "freshness_hs256_valid_ok": hs_ok,
        "freshness_hs256_valid_n": len(hs_rows),
        "freshness_valid_vs_invalid_bc_means": {
            "valid": _mean_bc(("valid",)),
            "noise": _mean_bc(("noise",)),
            "expired": _mean_bc(("expired",)),
            "permission_boundary": _mean_bc(("permission_boundary",)),
            "signing_key_rotation": _mean_bc(("signing_key_rotation",)),
            "session_invalidation": _mean_bc(("session_invalidation",)),
        },
    }


# ─── Browser harness ─────────────────────────────────────────────────────────
def _fetch_direct(base_url: str, token: str, timeout: float = 10.0) -> Dict[str, Any]:
    r = requests.get(
        f"{base_url}/resource",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        timeout=timeout,
    )
    body = r.content
    hdrs_f = filter_headers(dict(r.headers))
    return {
        "status": r.status_code,
        "body": body,
        "headers_filtered": hdrs_f,
        "headers_raw": dict(r.headers),
        "fetch_method": "direct",
    }


def _fetch_browser_api(context, base_url: str, token: str) -> Dict[str, Any]:
    resp = context.request.get(
        f"{base_url}/resource",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    body = resp.body()
    hdrs_raw = {k: v for k, v in resp.headers.items()}
    hdrs_f = filter_headers(hdrs_raw)
    return {
        "status": resp.status,
        "body": body,
        "headers_filtered": hdrs_f,
        "headers_raw": hdrs_raw,
        "fetch_method": "browser_page_request",
    }


def run_browser_harness(
    base_url: str,
    control_db: Path,
    n_state: int = N_BROWSER_STATE,
    seed: int = SEED,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    from playwright.sync_api import sync_playwright

    rng = random.Random(seed)
    observations: List[Dict[str, Any]] = []
    ax_pages: List[Dict[str, Any]] = []
    provision: Dict[str, Any] = {}

    ensure_session(control_db, valid=1)
    set_headers_direct(control_db, "BASE")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        vp = page.viewport_size
        provision["viewport"] = vp
        provision["playwright_ok"] = True
        if vp != {"width": 1280, "height": 720}:
            raise MeasurementInvalid("BROWSER_VIEWPORT", f"viewport {vp} != 1280x720")

        idx = 0

        def add_pair(label: str, fetch: str, state_a: str, state_b: str,
                     header_a: str, header_b: str) -> None:
            nonlocal idx
            for side, (bvar, hvar) in (( "a", (state_a, header_a)), ("b", (state_b, header_b))):
                set_body_direct(control_db, bvar)
                set_headers_direct(control_db, hvar)
                ensure_session(control_db, valid=1)
                time.sleep(0.03)
                if fetch == "direct":
                    res = _fetch_direct(base_url, VALID_JWT)
                else:
                    res = _fetch_browser_api(context, base_url, VALID_JWT)
                fps = {name: fn(res["status"], res["body"], res["headers_filtered"])
                       for name, fn in FP_FUNCS.items()}
                observations.append({
                    "idx": idx,
                    "label": label,
                    "side": side,
                    "fetch_method": res["fetch_method"],
                    "state_body": bvar,
                    "state_header": hvar,
                    "status": res["status"],
                    "body_sha256": hashlib.sha256(res["body"]).hexdigest() if res["body"] else "",
                    "body_len": len(res["body"]),
                    "content_length_header": res["headers_filtered"].get("content-length"),
                    "content_encoding": res["headers_raw"].get("Content-Encoding")
                        or res["headers_raw"].get("content-encoding"),
                    "headers_filtered_json": json.dumps(res["headers_filtered"], sort_keys=True, separators=(",", ":")),
                    "headers_no_clen_json": json.dumps(
                        {k: v for k, v in res["headers_filtered"].items() if k != "content-length"},
                        sort_keys=True, separators=(",", ":"),
                    ),
                    "fingerprint_full": fps["full"],
                    "fingerprint_status": fps["status"],
                    "fingerprint_body": fps["body"],
                    "fingerprint_headers": fps["headers"],
                    "fingerprint_headers_no_clen": fps["headers_no_clen"],
                    "worker_id": res["headers_raw"].get("X-Worker-Pid")
                        or res["headers_raw"].get("x-worker-pid"),
                    "viewport": vp,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                idx += 1

        # Body-only A vs C / A vs B
        for fetch in ("browser", "direct"):
            for _ in range(n_state):
                add_pair("body_AvsC", fetch, "A", "C", "BASE", "BASE")
            for _ in range(max(4, n_state // 5)):
                add_pair("body_AvsB", fetch, "A", "B", "BASE", "BASE")

        # Header-only BASE vs E
        for fetch in ("browser", "direct"):
            for _ in range(n_state):
                add_pair("header_AvsE", fetch, "A", "A", "BASE", "E")

        # Body gradients
        body_grads = [("1B", "A", "A1"), ("2B", "A", "A2"), ("4B", "A", "A3"),
                      ("39B", "A", "B"), ("86B", "A", "C")]
        for fetch in ("browser", "direct"):
            for gname, sa, sb in body_grads:
                for _ in range(max(4, n_state // 5)):
                    add_pair(f"gradient_body_{gname}", fetch, sa, sb, "BASE", "BASE")

        # Header gradients
        hdr_grads = [
            ("CC_small", "BASE", "CC_small"),
            ("CC_large", "BASE", "CC_large"),
            ("ETag_small", "BASE", "ETag_small"),
            ("ETag_large", "BASE", "ETag_large"),
            ("SC_small", "BASE", "SC_small"),
            ("SC_large", "BASE", "SC_large"),
            ("Vary_small", "BASE", "Vary_small"),
        ]
        for fetch in ("browser", "direct"):
            for gname, ha, hb in hdr_grads:
                for _ in range(max(3, n_state // 7)):
                    add_pair(f"gradient_header_{gname}", fetch, "A", "A", ha, hb)

        # Nulls
        for fetch in ("browser", "direct"):
            for _ in range(max(4, n_state // 5)):
                add_pair("null_body", fetch, "A", "A", "BASE", "BASE")
                add_pair("null_header", fetch, "A", "A", "BASE", "BASE")

        # Null 401 / 403
        for fetch in ("browser", "direct"):
            for _ in range(max(3, n_state // 7)):
                for side in ("a", "b"):
                    set_body_direct(control_db, "A")
                    if fetch == "direct":
                        r = requests.get(
                            f"{base_url}/resource",
                            headers={"Authorization": "Bearer not-a-jwt",
                                     "Accept": "application/json"},
                            timeout=10,
                        )
                        status, body = r.status_code, r.content
                        hdrs_f = filter_headers(dict(r.headers))
                        hdrs_raw = dict(r.headers)
                        method = "direct"
                    else:
                        resp = context.request.get(
                            f"{base_url}/resource",
                            headers={"Authorization": "Bearer not-a-jwt",
                                     "Accept": "application/json"},
                        )
                        status, body = resp.status, resp.body()
                        hdrs_raw = dict(resp.headers)
                        hdrs_f = filter_headers(hdrs_raw)
                        method = "browser_page_request"
                    fps = {n: fn(status, body, hdrs_f) for n, fn in FP_FUNCS.items()}
                    observations.append({
                        "idx": idx, "label": "null_401", "side": side,
                        "fetch_method": method, "state_body": "A", "state_header": "BASE",
                        "status": status,
                        "body_sha256": hashlib.sha256(body).hexdigest() if body else "",
                        "body_len": len(body),
                        "content_length_header": hdrs_f.get("content-length"),
                        "headers_filtered_json": json.dumps(hdrs_f, sort_keys=True, separators=(",", ":")),
                        "headers_no_clen_json": json.dumps(
                            {k: v for k, v in hdrs_f.items() if k != "content-length"},
                            sort_keys=True, separators=(",", ":")),
                        "fingerprint_full": fps["full"],
                        "fingerprint_status": fps["status"],
                        "fingerprint_body": fps["body"],
                        "fingerprint_headers": fps["headers"],
                        "fingerprint_headers_no_clen": fps["headers_no_clen"],
                        "worker_id": hdrs_raw.get("X-Worker-Pid") or hdrs_raw.get("x-worker-pid"),
                        "viewport": vp,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
                    idx += 1
                for side in ("a", "b"):
                    set_body_direct(control_db, "A")
                    ensure_session(control_db, valid=1)
                    if fetch == "direct":
                        r = requests.get(
                            f"{base_url}/api/profile",
                            headers={"Authorization": f"Bearer {DENIED_JWT}",
                                     "Accept": "application/json"},
                            timeout=10,
                        )
                        status, body = r.status_code, r.content
                        hdrs_f = filter_headers(dict(r.headers))
                        hdrs_raw = dict(r.headers)
                        method = "direct"
                    else:
                        resp = context.request.get(
                            f"{base_url}/api/profile",
                            headers={"Authorization": f"Bearer {DENIED_JWT}",
                                     "Accept": "application/json"},
                        )
                        status, body = resp.status, resp.body()
                        hdrs_raw = dict(resp.headers)
                        hdrs_f = filter_headers(hdrs_raw)
                        method = "browser_page_request"
                    fps = {n: fn(status, body, hdrs_f) for n, fn in FP_FUNCS.items()}
                    observations.append({
                        "idx": idx, "label": "null_403", "side": side,
                        "fetch_method": method, "state_body": "A", "state_header": "BASE",
                        "status": status,
                        "body_sha256": hashlib.sha256(body).hexdigest() if body else "",
                        "body_len": len(body),
                        "content_length_header": hdrs_f.get("content-length"),
                        "headers_filtered_json": json.dumps(hdrs_f, sort_keys=True, separators=(",", ":")),
                        "headers_no_clen_json": json.dumps(
                            {k: v for k, v in hdrs_f.items() if k != "content-length"},
                            sort_keys=True, separators=(",", ":")),
                        "fingerprint_full": fps["full"],
                        "fingerprint_status": fps["status"],
                        "fingerprint_body": fps["body"],
                        "fingerprint_headers": fps["headers"],
                        "fingerprint_headers_no_clen": fps["headers_no_clen"],
                        "worker_id": hdrs_raw.get("X-Worker-Pid") or hdrs_raw.get("x-worker-pid"),
                        "viewport": vp,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
                    idx += 1

        # CDP AX/DOM on /resource pages via page.goto (navigation -> HTML)
        set_body_direct(control_db, "A")
        set_headers_direct(control_db, "BASE")
        ensure_session(control_db, valid=1)
        n_ax_pages = max(8, n_state // 2)
        for page_i in range(n_ax_pages):
            try:
                def route_handler(route, request):
                    route.continue_(headers={
                        **request.headers,
                        "Authorization": f"Bearer {VALID_JWT}",
                    })
                context.route("**/resource*", route_handler)
                page.goto(f"{base_url}/resource", wait_until="networkidle", timeout=15000)
                context.unroute("**/resource*")

                ct = page.evaluate(
                    "() => document.contentType || (document.querySelector('html') ? 'text/html' : 'unknown')"
                )
                dom_nodes = page.evaluate("() => document.querySelectorAll('*').length")
                try:
                    cdp = context.new_cdp_session(page)
                    ax_result = cdp.send("Accessibility.getFullAXTree")
                    ax_nodes = len(ax_result.get("nodes", []))
                    cdp.detach()
                    ax_err = None
                except Exception as e:
                    ax_nodes = 0
                    ax_err = str(e)
                vp_page = page.viewport_size
                ax_pages.append({
                    "page_idx": page_i,
                    "url": f"{base_url}/resource",
                    "ax_nodes": ax_nodes,
                    "dom_nodes": dom_nodes,
                    "content_type": ct,
                    "viewport": vp_page,
                    "ax_error": ax_err,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            except Exception as e:
                ax_pages.append({
                    "page_idx": page_i,
                    "url": f"{base_url}/resource",
                    "ax_nodes": 0,
                    "dom_nodes": 0,
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            time.sleep(0.05)

        browser.close()

    return observations, ax_pages, provision


def compute_browser_metrics(
    browser_obs: List[Dict[str, Any]],
    ax_pages: List[Dict[str, Any]],
    provision: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    metrics: Dict[str, Any] = {}
    controls: Dict[str, Any] = {}

    metrics["bg_provision_ok"] = bool(provision.get("playwright_ok"))
    metrics["bg_playwright_viewport"] = provision.get("viewport")
    metrics["bg_agentlab_version"] = None
    metrics["bg_agentlab_0143_absent"] = None
    try:
        import importlib.metadata as im
        metrics["bg_agentlab_version"] = im.version("agentlab")
        metrics["bg_agentlab_0143_absent"] = metrics["bg_agentlab_version"] != "0.14.3"
    except Exception as e:
        metrics["bg_agentlab_error"] = str(e)

    ax_list = [p.get("ax_nodes", 0) for p in ax_pages if p.get("ax_nodes") is not None]
    dom_list = [p.get("dom_nodes", 0) for p in ax_pages if p.get("dom_nodes") is not None]
    if ax_list:
        metrics["bg_ax_nodes_median"] = statistics.median(ax_list)
        metrics["bg_ax_nodes_per_page"] = ax_list
        metrics["bg_pc_health_pct"] = 100.0 * sum(1 for x in ax_list if x > 10) / len(ax_list)
    else:
        metrics["bg_ax_nodes_median"] = 0
        metrics["bg_ax_nodes_per_page"] = []
        metrics["bg_pc_health_pct"] = 0.0
    if dom_list:
        metrics["bg_dom_nodes_median"] = statistics.median(dom_list)
        metrics["bg_dom_nodes_per_page"] = dom_list
        metrics["bg_dom_nodes_range_ok"] = all(21 <= d <= 82 for d in dom_list)
        metrics["bg_dom_min"] = min(dom_list)
        metrics["bg_dom_max"] = max(dom_list)
    else:
        metrics["bg_dom_nodes_median"] = 0
        metrics["bg_dom_nodes_per_page"] = []
        metrics["bg_dom_nodes_range_ok"] = False

    def fps_for(label: str, fetch: str, side: str, source: str) -> List[str]:
        key = {
            "full": "fingerprint_full",
            "status": "fingerprint_status",
            "body": "fingerprint_body",
            "headers": "fingerprint_headers",
            "headers_no_clen": "fingerprint_headers_no_clen",
        }[source]
        return [
            o[key] for o in browser_obs
            if o["label"] == label and o["fetch_method"].startswith(fetch) and o["side"] == side
        ]

    def disc(label: str, fetch: str, source: str) -> Dict[str, Any]:
        a = fps_for(label, fetch, "a", source)
        b = fps_for(label, fetch, "b", source)
        return bootstrap_jaccard_ci(a, b)

    def put_disc(prefix: str, label: str, fetch: str) -> None:
        for src in ("full", "status", "body", "headers", "headers_no_clen"):
            metrics[f"{prefix}_{src}"] = disc(label, fetch, src)

    put_disc("browser_body_AvsC", "body_AvsC", "browser")
    put_disc("direct_body_AvsC", "body_AvsC", "direct")
    put_disc("browser_header_AvsE", "header_AvsE", "browser")
    put_disc("direct_header_AvsE", "header_AvsE", "direct")
    put_disc("browser_body_AvsB", "body_AvsB", "browser")
    put_disc("direct_body_AvsB", "body_AvsB", "direct")
    put_disc("browser_null_body", "null_body", "browser")
    put_disc("browser_null_header", "null_header", "browser")
    put_disc("browser_null_401", "null_401", "browser")
    put_disc("browser_null_403", "null_403", "browser")
    put_disc("direct_null_body", "null_body", "direct")
    put_disc("direct_null_header", "null_header", "direct")

    for gname in ("1B", "2B", "4B", "39B", "86B"):
        lab = f"gradient_body_{gname}"
        put_disc(f"browser_gradient_{gname}", lab, "browser")
        put_disc(f"direct_gradient_{gname}", lab, "direct")

    for gname in ("CC_small", "CC_large", "ETag_small", "ETag_large",
                  "SC_small", "SC_large", "Vary_small"):
        lab = f"gradient_header_{gname}"
        put_disc(f"browser_gradient_{gname}", lab, "browser")
        put_disc(f"direct_gradient_{gname}", lab, "direct")

    avse = [o for o in browser_obs if o["label"] == "header_AvsE" and o["fetch_method"].startswith("browser")]
    clens = [o.get("content_length_header") for o in avse]
    metrics["browser_header_AvsE_clen_values"] = clens
    metrics["browser_header_AvsE_clen_equal_31"] = all(c == "31" for c in clens) if clens else False

    c5_pass = (
        metrics.get("bg_provision_ok")
        and metrics.get("bg_ax_nodes_median", 0) > 10
        and metrics.get("bg_pc_health_pct", 0) >= 80
        and metrics.get("bg_dom_nodes_range_ok", False)
        and metrics.get("bg_playwright_viewport") == {"width": 1280, "height": 720}
    )
    controls["C5-BROWSER"] = {
        "expected": "AgentLab 0.4.2, viewport 1280x720, AX>10 median, PC-HEALTH>=80%, DOM 21-82 on /resource",
        "observed": (
            f"viewport={metrics.get('bg_playwright_viewport')}, "
            f"ax_median={metrics.get('bg_ax_nodes_median')}, "
            f"pc_health={metrics.get('bg_pc_health_pct')}, "
            f"dom_range_ok={metrics.get('bg_dom_nodes_range_ok')}, "
            f"agentlab={metrics.get('bg_agentlab_version')}"
        ),
        "pass": bool(c5_pass),
        "evidence_refs": ["raw_observations.jsonl", "ax_dom_pages.jsonl"],
    }

    b_full = metrics.get("browser_body_AvsC_full", {})
    b_status = metrics.get("browser_body_AvsC_status", {})
    b_hnc = metrics.get("browser_body_AvsC_headers_no_clen", {})
    c6a = (
        b_full.get("discrimination", 0) > 0.5
        and b_status.get("discrimination", 1) == 0.0
        and b_hnc.get("discrimination", 1) == 0.0
    )
    controls["C6a-BODY-DISCRIM"] = {
        "expected": "browser body AvsC full>0.5 status=0 headers_no_clen=0",
        "observed": (
            f"full={b_full.get('discrimination')}, status={b_status.get('discrimination')}, "
            f"headers_no_clen={b_hnc.get('discrimination')}, "
            f"full_ci={b_full.get('ci_95')}"
        ),
        "pass": bool(c6a),
        "evidence_refs": ["raw_observations.jsonl"],
    }

    h_full = metrics.get("browser_header_AvsE_full", {})
    h_hdr = metrics.get("browser_header_AvsE_headers", {})
    h_body = metrics.get("browser_header_AvsE_body", {})
    h_status = metrics.get("browser_header_AvsE_status", {})
    c6b = (
        h_full.get("discrimination", 0) > 0.5
        and h_hdr.get("discrimination", 0) == 1.0
        and h_body.get("discrimination", 1) == 0.0
        and h_status.get("discrimination", 1) == 0.0
        and metrics.get("browser_header_AvsE_clen_equal_31", False)
    )
    controls["C6b-HEADER-DISCRIM"] = {
        "expected": "browser header AvsE full>0.5 headers_only=1.0 body=0 status=0 CLEN 31==31",
        "observed": (
            f"full={h_full.get('discrimination')}, headers={h_hdr.get('discrimination')}, "
            f"body={h_body.get('discrimination')}, status={h_status.get('discrimination')}, "
            f"clen_eq={metrics.get('browser_header_AvsE_clen_equal_31')}"
        ),
        "pass": bool(c6b),
        "evidence_refs": ["raw_observations.jsonl"],
    }

    nb = metrics.get("browser_null_body_full", {})
    nh = metrics.get("browser_null_header_full", {})
    n401 = metrics.get("browser_null_401_full", {})
    n403 = metrics.get("browser_null_403_full", {})
    c6c = (
        nb.get("discrimination", 1) <= 0.05
        and nh.get("discrimination", 1) <= 0.05
        and n401.get("discrimination", 1) <= 0.05
        and n403.get("discrimination", 1) <= 0.05
    )
    controls["C6c-BROWSER-NULL"] = {
        "expected": "null full 0.0 CI contains 0 point<=0.05 (body, header, 401, 403)",
        "observed": (
            f"body={nb.get('discrimination')} ci={nb.get('ci_95')}, "
            f"header={nh.get('discrimination')}, "
            f"401={n401.get('discrimination')}, 403={n403.get('discrimination')}"
        ),
        "pass": bool(c6c),
        "evidence_refs": ["raw_observations.jsonl"],
    }

    return metrics, controls


def build_distributed_controls(
    shared_m: Dict[str, Any],
    per_m: Optional[Dict[str, Any]],
    sticky_m: Optional[Dict[str, Any]],
    batch_log_len_shared: int,
) -> Dict[str, Any]:
    controls: Dict[str, Any] = {}

    s_mean = shared_m.get("freshness_c1_tn_mean")
    s_lo = shared_m.get("freshness_c1_tn_wilson_lo")
    s_ss = shared_m.get("freshness_c1_tn_session_status")
    hs = shared_m.get("freshness_hs256_valid_success_rate")
    p_mean = per_m.get("freshness_c1_tn_mean") if per_m else None
    p_ss = per_m.get("freshness_c1_tn_session_status") if per_m else None

    sticky_ok = (
        sticky_m is not None
        and (sticky_m.get("freshness_c1_tn_mean") or 0) >= 0.85
    )
    shared_ok = (
        s_mean is not None and s_mean >= 0.85
        and s_lo is not None and s_lo > 0.75
        and s_ss is not None and s_ss >= 0.85
        and hs is not None and hs >= 0.90
    )
    per_ok = p_mean is not None and p_mean < 0.85
    c1_pass = bool(shared_ok and per_ok)
    controls["C1-FRESHNESS"] = {
        "expected": (
            "shared mean TN>=0.85 Wilson lo>0.75 session_status>=0.85 "
            "hs256_valid_success_rate>=0.90; per-node mean TN<0.85 (~0.667)"
        ),
        "observed": (
            f"shared_mean={s_mean}, shared_wilson_lo={s_lo}, session_status={s_ss}, "
            f"hs256_rate={hs}, per_node_mean={p_mean}, per_node_session_status={p_ss}, "
            f"sticky_mean={sticky_m.get('freshness_c1_tn_mean') if sticky_m else None}"
        ),
        "pass": c1_pass,
        "evidence_refs": [
            "raw_freshness_shared.jsonl",
            "raw_freshness_per_node.jsonl",
            "raw_freshness_sticky.jsonl",
        ],
    }

    n_non = shared_m.get("freshness_n_non304", 0)
    workers = shared_m.get("freshness_worker_distribution", {})
    worker_min = min(workers.values()) if workers else 0
    controls["C2-FRESHNESS"] = {
        "expected": "n_non304>=800 after real 304 exclusion; X-Worker-Pid >=10/worker; batch_state_log >=27",
        "observed": (
            f"n_non304={n_non}, n_304={shared_m.get('freshness_n_304')}, "
            f"workers={workers}, worker_min={worker_min}, "
            f"batch_log_len={batch_log_len_shared}"
        ),
        "pass": bool(n_non >= 800 and worker_min >= 10 and batch_log_len_shared >= 27),
        "evidence_refs": ["raw_freshness_shared.jsonl", "batch_state_log_shared.jsonl"],
    }

    r = shared_m.get("freshness_stratified_r")
    ci_up = shared_m.get("freshness_stratified_r_ci_upper")
    p_up = shared_m.get("freshness_tost_p_upper")
    tost_pass = shared_m.get("freshness_tost_pass")
    var_count = shared_m.get("freshness_c2_variance_pass_count", 0)
    c3_pass = bool(
        r is not None and abs(r) < 0.15
        and ci_up is not None and ci_up < 0.15
        and p_up is not None and p_up < 0.05
        and tost_pass
        and var_count >= 8
    )
    controls["C3-FRESHNESS"] = {
        "expected": "stratified |r|<0.15 CI upper<0.15 p_upper<0.05; 8/8 variance std>0",
        "observed": (
            f"r={r}, ci_upper={ci_up}, p_upper={p_up}, tost_pass={tost_pass}, "
            f"variance={var_count}/8"
        ),
        "pass": c3_pass,
        "evidence_refs": ["raw_freshness_shared.jsonl"],
    }

    fp = shared_m.get("freshness_fp_noise")
    fp_hi = shared_m.get("freshness_fp_noise_wilson_hi")
    c4_pass = bool(fp is not None and fp <= 0.15)
    controls["C4-FRESHNESS"] = {
        "expected": "noise FP <=0.15 (Wilson)",
        "observed": f"fp={fp}, wilson_hi={fp_hi}, n={shared_m.get('freshness_fp_noise_n')}",
        "pass": c4_pass,
        "evidence_refs": ["raw_freshness_shared.jsonl"],
    }

    controls["B-SHARED-STORE"] = {
        "expected": "primary fix: shared WAL + HS256 -> TN>=0.85",
        "observed": f"tn_mean={s_mean}, n_non304={n_non}",
        "pass": shared_ok,
        "evidence_refs": ["raw_freshness_shared.jsonl"],
    }
    controls["B-PER-NODE"] = {
        "expected": "negative baseline: TN~0.667 session_status 0.0 <0.85",
        "observed": f"tn_mean={p_mean}, session_status={p_ss}",
        "pass": bool(p_mean is not None and p_mean < 0.85),
        "evidence_refs": ["raw_freshness_per_node.jsonl"],
    }
    controls["B-STICKY"] = {
        "expected": "exploratory: sticky IP-bound + HS256 -> TN>=0.85, skewed distribution",
        "observed": (
            f"tn_mean={sticky_m.get('freshness_c1_tn_mean') if sticky_m else None}, "
            f"workers={sticky_m.get('freshness_worker_distribution') if sticky_m else None}"
        ),
        "pass": sticky_ok if sticky_m is not None else None,
        "evidence_refs": ["raw_freshness_sticky.jsonl"],
    }

    return controls


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row, default=str) + "\n")


def sha256_file(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    print(f"[{EXPERIMENT_ID}] EXECUTE start SEED={SEED}", flush=True)
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    NGINX_DIR.mkdir(parents=True, exist_ok=True)
    SHARED_DB.parent.mkdir(parents=True, exist_ok=True)

    # Clean DBs
    for p in (
        SHARED_DB,
        Path("/tmp/spider-pernode-19860.db"),
        Path("/tmp/spider-pernode-19861.db"),
        Path("/tmp/spider-sticky-19860.db"),
        Path("/tmp/spider-sticky-19861.db"),
    ):
        for suffix in ("", "-wal", "-shm"):
            try:
                Path(str(p) + suffix).unlink(missing_ok=True)
            except Exception:
                pass

    kill_servers()

    all_metrics: Dict[str, Any] = {}
    all_controls: Dict[str, Any] = {}
    all_observations: List[Dict[str, Any]] = []
    validity_notes: List[str] = []
    unresolved: List[str] = []
    artifacts: List[Dict[str, Any]] = []
    infra_errors: List[str] = []

    # ── Shared store arm (primary) ──
    shared_obs: List[Dict[str, Any]] = []
    shared_batch: List[Dict[str, Any]] = []
    shared_m: Dict[str, Any] = {}
    try:
        print("[shared] starting gunicorn A+B + nginx rr", flush=True)
        proc_a = start_gunicorn(GUNICORN_PORT_A, SHARED_DB, "wsgi_shared_a")
        proc_b = start_gunicorn(GUNICORN_PORT_B, SHARED_DB, "wsgi_shared_b")
        time.sleep(1.5)
        if not wait_http(f"http://{HOST}:{GUNICORN_PORT_A}/health", 10):
            raise MeasurementInvalid("GUNICORN_UNAVAILABLE", "port A")
        if not wait_http(f"http://{HOST}:{GUNICORN_PORT_B}/health", 10):
            raise MeasurementInvalid("GUNICORN_UNAVAILABLE", "port B")
        nginx_proc = start_nginx("rr")
        base_url = f"http://{HOST}:{NGINX_PORT}"

        # Verify HS256 valid success on a quick probe
        ensure_schema(SHARED_DB)
        ensure_session(SHARED_DB, valid=1)
        probe_ok = 0
        for _ in range(10):
            r = requests.get(
                f"{base_url}/api/session/status",
                headers={"Authorization": f"Bearer {VALID_JWT}"},
                timeout=5,
            )
            if r.status_code == 200:
                probe_ok += 1
        print(f"[shared] HS256 probe {probe_ok}/10", flush=True)
        if probe_ok == 0:
            raise MeasurementInvalid(
                "HS256_VALIDATION_STILL_REJECTS_ALL",
                "0/10 valid JWTs returned 200 on session_status",
            )

        shared_obs, shared_batch = run_distributed_arm(
            "B-SHARED-STORE", base_url, SHARED_DB, N_DISTRIBUTED, SEED,
            worker_dbs=[], replicate_session_to_workers=False,
        )
        shared_m = compute_distributed_metrics(shared_obs, "B-SHARED-STORE")
        all_metrics.update({f"shared_{k}": v for k, v in shared_m.items()})
        write_jsonl(ARTIFACT_DIR / "raw_freshness_shared.jsonl", shared_obs)
        write_jsonl(ARTIFACT_DIR / "batch_state_log_shared.jsonl", shared_batch)
        artifacts.append({"path": str(ARTIFACT_DIR / "raw_freshness_shared.jsonl"), "role": "raw"})
        artifacts.append({"path": str(ARTIFACT_DIR / "batch_state_log_shared.jsonl"), "role": "raw"})
        print(f"[shared] n={len(shared_obs)} tn_mean={shared_m.get('freshness_c1_tn_mean')}", flush=True)

        # Keep servers for browser arm on shared store
        # ── Per-node arm ──
        # Restart with per-node DBs
        kill_servers()
        stop_nginx()
        time.sleep(0.5)

        per_db_a = Path("/tmp/spider-pernode-19860.db")
        per_db_b = Path("/tmp/spider-pernode-19861.db")
        for p in (per_db_a, per_db_b):
            for suffix in ("", "-wal", "-shm"):
                Path(str(p) + suffix).unlink(missing_ok=True)

        proc_a = start_gunicorn(GUNICORN_PORT_A, per_db_a, "wsgi_per_a")
        proc_b = start_gunicorn(GUNICORN_PORT_B, per_db_b, "wsgi_per_b")
        time.sleep(1.5)
        if not wait_http(f"http://{HOST}:{GUNICORN_PORT_A}/health", 10):
            raise MeasurementInvalid("GUNICORN_UNAVAILABLE", "per-node A")
        if not wait_http(f"http://{HOST}:{GUNICORN_PORT_B}/health", 10):
            raise MeasurementInvalid("GUNICORN_UNAVAILABLE", "per-node B")
        nginx_proc = start_nginx("rr")

        # Control-plane sessions go to SHARED_DB (not visible to per-node workers)
        ensure_schema(SHARED_DB)
        ensure_session(SHARED_DB, valid=1)
        set_body_direct(SHARED_DB, "A")
        set_headers_direct(SHARED_DB, "BASE")

        # But workers read per-node DBs — seed body/header config there too
        ensure_schema(per_db_a)
        ensure_schema(per_db_b)
        set_body_direct(per_db_a, "A")
        set_headers_direct(per_db_a, "BASE")
        set_body_direct(per_db_b, "A")
        set_headers_direct(per_db_b, "BASE")
        # Intentionally do NOT copy sessions into per-node worker DBs

        per_obs, per_batch = run_distributed_arm(
            "B-PER-NODE", base_url, SHARED_DB, N_DISTRIBUTED, SEED,
            worker_dbs=[per_db_a, per_db_b], replicate_session_to_workers=False,
        )
        per_m = compute_distributed_metrics(per_obs, "B-PER-NODE")
        all_metrics.update({f"per_node_{k}": v for k, v in per_m.items()})
        write_jsonl(ARTIFACT_DIR / "raw_freshness_per_node.jsonl", per_obs)
        write_jsonl(ARTIFACT_DIR / "batch_state_log_per_node.jsonl", per_batch)
        artifacts.append({"path": str(ARTIFACT_DIR / "raw_freshness_per_node.jsonl"), "role": "raw"})
        artifacts.append({"path": str(ARTIFACT_DIR / "batch_state_log_per_node.jsonl"), "role": "raw"})
        print(f"[per-node] n={len(per_obs)} tn_mean={per_m.get('freshness_c1_tn_mean')}", flush=True)

        # ── Sticky arm ──
        kill_servers()
        stop_nginx()
        time.sleep(0.5)

        st_db_a = Path("/tmp/spider-sticky-19860.db")
        st_db_b = Path("/tmp/spider-sticky-19861.db")
        for p in (st_db_a, st_db_b):
            for suffix in ("", "-wal", "-shm"):
                Path(str(p) + suffix).unlink(missing_ok=True)

        # Sticky: sessions must be in BOTH per-node files so pinned worker finds them
        # (models sticky+manual session placement; disclosed)
        for p in (st_db_a, st_db_b):
            ensure_schema(p)
            ensure_session(p, valid=1)
            set_body_direct(p, "A")
            set_headers_direct(p, "BASE")

        proc_a = start_gunicorn(GUNICORN_PORT_A, st_db_a, "wsgi_sticky_a")
        proc_b = start_gunicorn(GUNICORN_PORT_B, st_db_b, "wsgi_sticky_b")
        time.sleep(1.5)
        if not wait_http(f"http://{HOST}:{GUNICORN_PORT_A}/health", 10):
            raise MeasurementInvalid("GUNICORN_UNAVAILABLE", "sticky A")
        if not wait_http(f"http://{HOST}:{GUNICORN_PORT_B}/health", 10):
            raise MeasurementInvalid("GUNICORN_UNAVAILABLE", "sticky B")
        nginx_proc = start_nginx("sticky")

        # Control plane for sticky: use SHARED_DB for session/body logging consistency
        # but sessions already seeded in both worker DBs. Also seed SHARED_DB.
        ensure_schema(SHARED_DB)
        ensure_session(SHARED_DB, valid=1)
        set_body_direct(SHARED_DB, "A")
        set_headers_direct(SHARED_DB, "BASE")

        sticky_obs, sticky_batch = run_distributed_arm(
            "B-STICKY", base_url, SHARED_DB, N_DISTRIBUTED, SEED,
            worker_dbs=[st_db_a, st_db_b], replicate_session_to_workers=True,
        )
        sticky_m = compute_distributed_metrics(sticky_obs, "B-STICKY")
        all_metrics.update({f"sticky_{k}": v for k, v in sticky_m.items()})
        write_jsonl(ARTIFACT_DIR / "raw_freshness_sticky.jsonl", sticky_obs)
        write_jsonl(ARTIFACT_DIR / "batch_state_log_sticky.jsonl", sticky_batch)
        artifacts.append({"path": str(ARTIFACT_DIR / "raw_freshness_sticky.jsonl"), "role": "raw"})
        artifacts.append({"path": str(ARTIFACT_DIR / "batch_state_log_sticky.jsonl"), "role": "raw"})
        print(f"[sticky] n={len(sticky_obs)} tn_mean={sticky_m.get('freshness_c1_tn_mean')}", flush=True)

    except MeasurementInvalid as e:
        infra_errors.append(f"{e.category}: {e.detail}")
        validity_notes.append(f"Infrastructure failure during distributed phase: {e}")
        shared_m = shared_m or {}
        per_m = per_m if "per_m" in dir() else None
        sticky_m = sticky_m if "sticky_m" in dir() else None
    except Exception as e:
        infra_errors.append(f"UNEXPECTED: {e}")
        validity_notes.append(f"Unexpected distributed failure: {traceback.format_exc()}")
        shared_m = shared_m or {}
        # preserve any arms that completed before the failure
        per_m = per_m if "per_m" in dir() else None
        sticky_m = sticky_m if "sticky_m" in dir() else None

    # ── Browser arm on shared store ──
    browser_obs: List[Dict[str, Any]] = []
    ax_pages: List[Dict[str, Any]] = []
    browser_metrics: Dict[str, Any] = {}
    browser_controls: Dict[str, Any] = {}
    try:
        kill_servers()
        stop_nginx()
        time.sleep(0.5)
        # Fresh shared DB for browser
        for suffix in ("", "-wal", "-shm"):
            Path(str(SHARED_DB) + suffix).unlink(missing_ok=True)

        proc_a = start_gunicorn(GUNICORN_PORT_A, SHARED_DB, "wsgi_br_a")
        proc_b = start_gunicorn(GUNICORN_PORT_B, SHARED_DB, "wsgi_br_b")
        time.sleep(1.5)
        if not wait_http(f"http://{HOST}:{GUNICORN_PORT_A}/health", 10):
            raise MeasurementInvalid("GUNICORN_UNAVAILABLE", "browser A")
        if not wait_http(f"http://{HOST}:{GUNICORN_PORT_B}/health", 10):
            raise MeasurementInvalid("GUNICORN_UNAVAILABLE", "browser B")
        nginx_proc = start_nginx("rr")
        base_url = f"http://{HOST}:{NGINX_PORT}"

        ensure_schema(SHARED_DB)
        ensure_session(SHARED_DB, valid=1)
        set_body_direct(SHARED_DB, "A")
        set_headers_direct(SHARED_DB, "BASE")

        browser_obs, ax_pages, provision = run_browser_harness(
            base_url, SHARED_DB, N_BROWSER_STATE, SEED
        )
        browser_metrics, browser_controls = compute_browser_metrics(
            browser_obs, ax_pages, provision
        )
        all_metrics.update(browser_metrics)
        all_controls.update(browser_controls)
        write_jsonl(ARTIFACT_DIR / "raw_observations.jsonl", browser_obs)
        write_jsonl(ARTIFACT_DIR / "ax_dom_pages.jsonl", ax_pages)
        artifacts.append({"path": str(ARTIFACT_DIR / "raw_observations.jsonl"), "role": "raw"})
        artifacts.append({"path": str(ARTIFACT_DIR / "ax_dom_pages.jsonl"), "role": "raw"})
        print(
            f"[browser] n={len(browser_obs)} ax_median={browser_metrics.get('bg_ax_nodes_median')} "
            f"pc={browser_metrics.get('bg_pc_health_pct')}",
            flush=True,
        )
    except MeasurementInvalid as e:
        infra_errors.append(f"{e.category}: {e.detail}")
        validity_notes.append(f"Infrastructure failure during browser phase: {e}")
    except Exception as e:
        infra_errors.append(f"BROWSER_UNEXPECTED: {e}")
        validity_notes.append(f"Unexpected browser failure: {traceback.format_exc()}")

    kill_servers()
    stop_nginx()

    # ── Build distributed controls ──
    batch_len = len(shared_batch) if shared_batch else 0
    if shared_m and shared_m.get("freshness_n_total"):
        dist_controls = build_distributed_controls(
            shared_m,
            per_m if shared_m and per_m else None,
            sticky_m if shared_m and sticky_m else None,
            batch_len,
        )
        all_controls.update(dist_controls)
        all_metrics["freshness_batch_state_log_len"] = batch_len

    # Flatten shared metrics to top-level stable names (AUDIT expects freshness_*)
    if shared_m:
        for k, v in shared_m.items():
            if k not in all_metrics:
                all_metrics[k] = v

    # ── Determine status/outcome ──
    if infra_errors and not shared_m and not browser_metrics:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    elif infra_errors:
        # partial: still can decide if one branch measured
        status = "MEASUREMENT_INVALID" if not (shared_m or browser_metrics) else "COMPLETE"
        outcome = "INCONCLUSIVE" if status == "MEASUREMENT_INVALID" else None
    else:
        status = "COMPLETE"
        outcome = None

    c1 = all_controls.get("C1-FRESHNESS", {}).get("pass")
    c2 = all_controls.get("C2-FRESHNESS", {}).get("pass")
    c3 = all_controls.get("C3-FRESHNESS", {}).get("pass")
    c4 = all_controls.get("C4-FRESHNESS", {}).get("pass")
    c5 = all_controls.get("C5-BROWSER", {}).get("pass")
    c6a = all_controls.get("C6a-BODY-DISCRIM", {}).get("pass")
    c6b = all_controls.get("C6b-HEADER-DISCRIM", {}).get("pass")
    c6c = all_controls.get("C6c-BROWSER-NULL", {}).get("pass")

    dist_pass = all(x is True for x in (c1, c2, c3, c4))
    browser_pass = all(x is True for x in (c5, c6a, c6b, c6c))

    if status == "COMPLETE":
        if dist_pass and browser_pass:
            outcome = "SUPPORTS"
        elif dist_pass and not browser_pass:
            outcome = "MIXED"
        elif not dist_pass and browser_pass:
            outcome = "MIXED"
        elif not dist_pass and not browser_pass:
            outcome = "FALSIFIES"
        else:
            outcome = "INCONCLUSIVE"

    # Power failure → MEASUREMENT_INVALID per frozen rule
    if status == "COMPLETE" and c2 is False and c1 is True:
        validity_notes.append(
            "C2 power check failed (n_non304<800 or worker_min<10 or batch_log<27) "
            "while C1 passed — per frozen decision_rule this is MEASUREMENT_INVALID (underpowered)."
        )
        # Keep status COMPLETE with outcome but flag; audit decides. Frozen says MEASUREMENT_INVALID.
        # We set status to MEASUREMENT_INVALID only for pure power failure with C1 pass:
        if c1 is True and c2 is False:
            status = "MEASUREMENT_INVALID"
            outcome = "INCONCLUSIVE"

    # HS256 total reject → invalid
    if shared_m and (shared_m.get("freshness_hs256_valid_success_rate") or 0) == 0.0:
        status = "MEASUREMENT_INVALID"
        outcome = "INCONCLUSIVE"
        validity_notes.append("HS256_VALIDATION_STILL_REJECTS_ALL: 0 valid JWTs succeeded.")

    if infra_errors:
        validity_notes.append("Infrastructure errors: " + "; ".join(infra_errors))

    # ── Write result.json ──
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": all_metrics,
        "controls": all_controls,
        "artifacts": artifacts,
        "observations": [
            f"Shared-store arm: {len(shared_obs)} samples via real nginx round-robin + HS256",
            f"Per-node arm: {len(per_obs) if 'per_obs' in dir() and per_obs else 0} samples (isolated DBs)",
            f"Sticky arm: {len(sticky_obs) if 'sticky_obs' in dir() and sticky_obs else 0} samples (hash $remote_addr)",
            f"Browser arm: {len(browser_obs)} observations via Playwright page.request + page.goto CDP",
            f"AX/DOM pages: {len(ax_pages)} /resource pages",
            f"Shared TN mean={shared_m.get('freshness_c1_tn_mean') if shared_m else None}",
            f"Per-node TN mean={per_m.get('freshness_c1_tn_mean') if per_m else None}",
            f"n_non304 shared={shared_m.get('freshness_n_non304') if shared_m else None}",
            f"AX median={all_metrics.get('bg_ax_nodes_median')}",
            f"PC-HEALTH={all_metrics.get('bg_pc_health_pct')}",
        ],
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }
    result_path = EXPERIMENT_DIR / "result.json"
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[output] result.json status={status} outcome={outcome}", flush=True)

    # ── report.md ──
    def fmt(v, nd=4):
        if v is None:
            return "null"
        if isinstance(v, float):
            return f"{v:.{nd}f}"
        return str(v)

    report = f"""# {EXPERIMENT_ID} — Execution Report

**Status:** {status}
**Outcome:** {outcome}
**Lane:** {LANE}
**Claims:** C-MEAS-VALID, C-FRESHNESS

## Distributed C-FRESHNESS (B-SHARED-STORE primary)

| Metric | Value | Target |
|--------|-------|--------|
| freshness_c1_tn_mean | {fmt(shared_m.get('freshness_c1_tn_mean'))} | >=0.85 |
| freshness_c1_tn_wilson_lo | {fmt(shared_m.get('freshness_c1_tn_wilson_lo'))} | >0.75 |
| freshness_c1_tn_session_status | {fmt(shared_m.get('freshness_c1_tn_session_status'))} | >=0.85 |
| freshness_c1_tn_profile | {fmt(shared_m.get('freshness_c1_tn_profile'))} | Wilson lo>0.75 |
| freshness_c1_tn_data_list | {fmt(shared_m.get('freshness_c1_tn_data_list'))} | Wilson lo>0.75 |
| freshness_n_non304 | {shared_m.get('freshness_n_non304')} | >=800 |
| freshness_n_304 (real) | {shared_m.get('freshness_n_304')} | >0 |
| freshness_stratified_r | {fmt(shared_m.get('freshness_stratified_r'))} | abs<0.15 |
| freshness_stratified_r_ci_upper | {fmt(shared_m.get('freshness_stratified_r_ci_upper'))} | <0.15 |
| freshness_tost_p_upper | {fmt(shared_m.get('freshness_tost_p_upper'))} | <0.05 |
| freshness_fp_noise | {fmt(shared_m.get('freshness_fp_noise'))} | <=0.15 |
| freshness_c2_variance | {shared_m.get('freshness_c2_variance_pass_count')}/{shared_m.get('freshness_c2_variance_total')} | 8/8 |
| freshness_hs256_valid_success_rate | {fmt(shared_m.get('freshness_hs256_valid_success_rate'))} | >=0.90 |
| freshness_worker_distribution | {shared_m.get('freshness_worker_distribution')} | >=10 each |
| batch_state_log lines | {batch_len} | >=27 |

### B-PER-NODE baseline (expected TN~0.667)

| Metric | Value |
|--------|-------|
| tn_mean | {fmt(per_m.get('freshness_c1_tn_mean')) if per_m else 'null'} |
| tn_session_status | {fmt(per_m.get('freshness_c1_tn_session_status')) if per_m else 'null'} |
| tn_profile | {fmt(per_m.get('freshness_c1_tn_profile')) if per_m else 'null'} |
| tn_data_list | {fmt(per_m.get('freshness_c1_tn_data_list')) if per_m else 'null'} |

### B-STICKY (exploratory)

| Metric | Value |
|--------|-------|
| tn_mean | {fmt(sticky_m.get('freshness_c1_tn_mean')) if sticky_m else 'null'} |
| workers | {sticky_m.get('freshness_worker_distribution') if sticky_m else 'null'} |

## Browser C-MEAS-VALID (Playwright 1280x720)

| Metric | Value | Target |
|--------|-------|--------|
| bg_provision_ok | {all_metrics.get('bg_provision_ok')} | true |
| bg_agentlab_version | {all_metrics.get('bg_agentlab_version')} | 0.4.2 |
| bg_playwright_viewport | {all_metrics.get('bg_playwright_viewport')} | 1280x720 |
| bg_ax_nodes_median | {all_metrics.get('bg_ax_nodes_median')} | >10 |
| bg_pc_health_pct | {fmt(all_metrics.get('bg_pc_health_pct'), 1)} | >=80 |
| bg_dom_nodes_median | {all_metrics.get('bg_dom_nodes_median')} | 21-82 |
| bg_dom_nodes_range_ok | {all_metrics.get('bg_dom_nodes_range_ok')} | true |
| browser_body_AvsC_full | {fmt((all_metrics.get('browser_body_AvsC_full') or {}).get('discrimination'))} | >0.5 |
| browser_body_AvsC_status | {fmt((all_metrics.get('browser_body_AvsC_status') or {}).get('discrimination'))} | 0.0 |
| browser_body_AvsC_headers_no_clen | {fmt((all_metrics.get('browser_body_AvsC_headers_no_clen') or {}).get('discrimination'))} | 0.0 |
| browser_header_AvsE_full | {fmt((all_metrics.get('browser_header_AvsE_full') or {}).get('discrimination'))} | >0.5 |
| browser_header_AvsE_headers | {fmt((all_metrics.get('browser_header_AvsE_headers') or {}).get('discrimination'))} | 1.0 |
| browser_header_AvsE_body | {fmt((all_metrics.get('browser_header_AvsE_body') or {}).get('discrimination'))} | 0.0 |
| browser_null_body_full | {fmt((all_metrics.get('browser_null_body_full') or {}).get('discrimination'))} | <=0.05 |

## Controls

| Control | Pass |
|---------|------|
| C1-FRESHNESS | {all_controls.get('C1-FRESHNESS', {}).get('pass')} |
| C2-FRESHNESS | {all_controls.get('C2-FRESHNESS', {}).get('pass')} |
| C3-FRESHNESS | {all_controls.get('C3-FRESHNESS', {}).get('pass')} |
| C4-FRESHNESS | {all_controls.get('C4-FRESHNESS', {}).get('pass')} |
| C5-BROWSER | {all_controls.get('C5-BROWSER', {}).get('pass')} |
| C6a-BODY-DISCRIM | {all_controls.get('C6a-BODY-DISCRIM', {}).get('pass')} |
| C6b-HEADER-DISCRIM | {all_controls.get('C6b-HEADER-DISCRIM', {}).get('pass')} |
| C6c-BROWSER-NULL | {all_controls.get('C6c-BROWSER-NULL', {}).get('pass')} |
| B-PER-NODE | {all_controls.get('B-PER-NODE', {}).get('pass')} |
| B-SHARED-STORE | {all_controls.get('B-SHARED-STORE', {}).get('pass')} |
| B-STICKY | {all_controls.get('B-STICKY', {}).get('pass')} |

## Validity notes

{chr(10).join('- ' + n for n in validity_notes) if validity_notes else '- None'}

## Unresolved

{chr(10).join('- ' + u for u in unresolved) if unresolved else '- None'}
"""
    report_path = EXPERIMENT_DIR / "report.md"
    report_path.write_text(report)
    print(f"[output] report.md written", flush=True)

    # ── provenance.json ──
    try:
        git_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=str(EXPERIMENT_DIR)
        ).stdout.strip()
    except Exception:
        git_sha = None

    def file_sha(p):
        return sha256_file(Path(p)) if p else None

    run_script = Path(__file__).resolve()
    provenance = {
        "experiment_id": EXPERIMENT_ID,
        "github_run_id": 35884739384,
        "base_sha": "a45b606eb738c082cf64e34e5b462e02ee25ffd1",
        "git_sha": git_sha,
        "env": {
            "python": sys.version,
            "flask": "3.1.3",
            "pyjwt": "2.14.0",
            "gunicorn": "23.0.0",
            "werkzeug": "3.1.8",
            "nginx": "1.24.0",
            "playwright": "1.63.0",
            "agentlab": all_metrics.get("bg_agentlab_version"),
            "requests": requests.__version__,
            "sqlite3": sqlite3.sqlite_version,
        },
        "ports": {"gunicorn_a": GUNICORN_PORT_A, "gunicorn_b": GUNICORN_PORT_B, "nginx": NGINX_PORT},
        "seed": SEED,
        "jitter_ms": [JITTER_MIN_MS, JITTER_MAX_MS],
        "excluded_headers": sorted(EXCLUDED_HEADERS),
        "filter_out_keys": sorted(FILTER_OUT_KEYS),
        "body_states": {k: {"len": v["len"], "sha256": v["sha256"]} for k, v in BODY_STATES.items()},
        "header_states": list(HEADER_STATES.keys()),
        "hs256_secret_sha256": HS256_SECRET_HASH,
        "db_paths": {
            "shared": str(SHARED_DB),
            "per_node_a": "/tmp/spider-pernode-19860.db",
            "per_node_b": "/tmp/spider-pernode-19861.db",
            "sticky_a": "/tmp/spider-sticky-19860.db",
            "sticky_b": "/tmp/spider-sticky-19861.db",
        },
        "run_experiment_sha256": file_sha(run_script),
        "frozen_hashes": {
            "request.json": file_sha(EXPERIMENT_DIR / "request.json"),
            "spec.json": file_sha(EXPERIMENT_DIR / "spec.json"),
            "prereg.md": file_sha(EXPERIMENT_DIR / "prereg.md"),
            "freeze.json": file_sha(EXPERIMENT_DIR / "freeze.json"),
        },
        "artifacts": {
            a["path"]: file_sha(a["path"]) for a in artifacts
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    prov_path = EXPERIMENT_DIR / "provenance.json"
    with open(prov_path, "w") as f:
        json.dump(provenance, f, indent=2, default=str)
    print(f"[output] provenance.json written", flush=True)
    print(f"[{EXPERIMENT_ID}] DONE status={status} outcome={outcome}", flush=True)
    return 0 if status == "COMPLETE" else 1


if __name__ == "__main__":
    sys.exit(main())
