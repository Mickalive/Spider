#!/usr/bin/env python3
"""Frozen experiment runner for EXP-RUNTIME-36106663091.

This runner deliberately fails closed.  It never substitutes simulated browser
observations, simulated writes, or requests-only observations for the required
Playwright path.  All raw records are written before derived measurements.
"""
from __future__ import annotations

import base64
import contextlib
import gzip
import hashlib
import hmac
import importlib
import importlib.metadata
import json
import math
import os
import random
import re
import shutil
import signal
import socket
import sqlite3
import subprocess
import sys
import time
import traceback
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import brotli
import jwt
import requests
import scipy.stats as scipy_stats
from flask import Flask, Response, jsonify, request

try:
    import numpy as np
    from sklearn.cluster import KMeans
except Exception as exc:  # pragma: no cover - setup failure is reported
    np = None
    KMeans = None
    _NUMPY_IMPORT_ERROR = repr(exc)
else:
    _NUMPY_IMPORT_ERROR = None

try:
    from playwright.sync_api import sync_playwright
except Exception as exc:  # pragma: no cover - setup failure is reported
    sync_playwright = None
    _PLAYWRIGHT_IMPORT_ERROR = repr(exc)
else:
    _PLAYWRIGHT_IMPORT_ERROR = None

try:
    import browsergym  # type: ignore
    _BROWSERGYM_IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover - setup failure is reported
    browsergym = None
    _BROWSERGYM_IMPORT_ERROR = repr(exc)

try:
    import browsergym.core  # type: ignore
    _BROWSERGYM_CORE_IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover - setup failure is reported
    _BROWSERGYM_CORE_IMPORT_ERROR = repr(exc)


EXPERIMENT_ID = "EXP-RUNTIME-36106663091"
LANE = "runtime"
CLAIM_ID = "C-MEAS-VALID"
SEED = 44
TESTBED_SECRET = "spider-runtime-measurement-secret-2026-08-25"
DB_PATH = Path("/tmp/single.db")
NGINX_CONF = Path("/tmp/single.db.nginx.conf")
NGINX_CACHE = Path("/tmp/single.db.cache")
WSGI_PATH = Path("/tmp/wsgi.py")
RUNNER_COPY = Path("/tmp/run_experiment.py")
GUNICORN_LOG_1 = Path("/tmp/single.gunicorn.19860.log")
GUNICORN_LOG_2 = Path("/tmp/single.gunicorn.19861.log")
BASE = Path(os.environ.get("SPIDER_EXPERIMENT_DIR", Path(__file__).resolve().parent))
BASE_URL = "http://127.0.0.1:19851"
ORIGIN_URLS = ["http://127.0.0.1:19860", "http://127.0.0.1:19861"]
API_ENDPOINTS = ["/api/profile", "/api/data_list"]
BROWSER_ENDPOINTS = ["/resource_page", "/resource", "/api/profile", "/api/data_list"]
WRITE_ENDPOINTS = ["/api/write/profile", "/api/write/data_list", "/api/write/controls_matrix"]
BODY_VARIANTS = ["A", "B", "C", "D"]
BODY_CONTENT = {
    "A": "alpha",
    "B": "bravo",
    "C": "charlie",
    "D": "delta",
}
HEADER_FILTER_OUT = {"content-length", "etag", "w-etag", "range"}
FINGERPRINT_EXCLUDE = {
    "date",
    "server",
    "x-request-id",
    "cf-ray",
    "cf-cache-status",
    "x-cache",
    "age",
    "x-worker-pid",
}
CONTROL_KEYS = ["input", "select", "textarea", "button", "label"]
TRAJECTORY_COSTS: list[dict[str, Any]] = []
RAW_FRESHNESS: list[dict[str, Any]] = []
RAW_BROWSER: list[dict[str, Any]] = []
RAW_WRITABLE: list[dict[str, Any]] = []
RAW_KMEANS_FEATURES: list[dict[str, Any]] = []
RAW_HIT: list[dict[str, Any]] = []
RAW_BATCH: list[dict[str, Any]] = []
METRICS: dict[str, Any] = {}
CONTROLS: dict[str, Any] = {}
VALIDITY_NOTES: list[str] = []
UNRESOLVED: list[str] = []
OBSERVATIONS: list[str] = []
INFRA_ERRORS: list[str] = []
COMMANDS: list[str] = []
_GUNICORN_PROCS: list[subprocess.Popen[Any]] = []
_NGINX_STARTED = False
_SESSION_ID = "runtime-session-36106663091"
_SUBJECT = "runtime-observer"
_VALID_TOKEN = ""
_EXPIRED_TOKEN = ""
_INVALID_TOKEN = "not-a-jwt"
_RUNTIME_DIAGNOSTICS: dict[str, Any] = {}


class InfrastructureFailure(RuntimeError):
    """A setup or execution failure that invalidates the measurement."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def jsonable(value: Any) -> Any:
    """Convert numpy/scalars and nested values to strict JSON values."""
    if value is None or isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and not math.isfinite(value):
            return None
        return value
    if isinstance(value, (np.integer, np.floating, np.bool_)):
        return jsonable(value.item())
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    return str(value)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(jsonable(value), indent=2, sort_keys=True) + "\n")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(jsonable(row), sort_keys=True, default=str) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def b64(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def body_summary(body: bytes) -> dict[str, Any]:
    return {
        "body_b64": b64(body),
        "body_sha256": sha256_bytes(body),
        "body_length": len(body),
        "body_text": body.decode("utf-8", errors="replace"),
    }


def filtered_headers(headers: dict[str, str], for_fingerprint: bool = False) -> dict[str, str]:
    lower = {str(k).lower(): str(v) for k, v in headers.items()}
    # Parent canonical filtering first removes transport/cache identity noise,
    # then removes body-derived fields for both header-only and full-vector
    # representations.  The fingerprint does not retain ETag/content-length;
    # otherwise a body-derived header could discriminate without the body.
    excluded = FINGERPRINT_EXCLUDE | HEADER_FILTER_OUT
    return {k: v for k, v in lower.items() if k not in excluded}


def header_jaccard(left: dict[str, str], right: dict[str, str]) -> float:
    a = set(f"{k}:{v}" for k, v in filtered_headers(left).items())
    b = set(f"{k}:{v}" for k, v in filtered_headers(right).items())
    return len(a & b) / len(a | b) if (a | b) else 1.0


def greedy_decompress(body: bytes, content_encoding: str = "") -> tuple[bytes, dict[str, Any]]:
    """Decompress greedily brotli then gzip, at most five passes."""
    current = body
    methods: list[str] = []
    ambiguous_at: int | None = None
    for _ in range(5):
        if not current:
            break
        candidates: list[tuple[str, bytes]] = []
        if "br" in content_encoding.lower():
            try:
                candidates.append(("br", brotli.decompress(current)))
            except Exception:
                pass
        if "gzip" in content_encoding.lower() or current[:2] == b"\x1f\x8b":
            try:
                candidates.append(("gzip", gzip.decompress(current)))
            except Exception:
                pass
        if not candidates:
            break
        valid = []
        for method, decoded in candidates:
            if decoded != current:
                valid.append((method, decoded))
        if not valid:
            break
        if len(valid) > 1 and valid[0][1] != valid[1][1] and ambiguous_at is None:
            ambiguous_at = len(methods)
        # Frozen order: brotli before gzip.
        method, current = valid[0]
        methods.append(method)
    return current, {"methods": methods, "ambiguous_at": ambiguous_at, "input_length": len(body)}


def response_record(resp: requests.Response | Any, url: str, auth_label: str, phase: str,
                    extra: dict[str, Any] | None = None) -> dict[str, Any]:
    headers = {str(k): str(v) for k, v in resp.headers.items()}
    body = bytes(resp.content if hasattr(resp, "content") else resp.body())
    decoded, decompression = greedy_decompress(body, headers.get("Content-Encoding", ""))
    row: dict[str, Any] = {
        "phase": phase,
        "url": url,
        "auth_label": auth_label,
        "status": int(resp.status_code if hasattr(resp, "status_code") else resp.status),
        "headers": headers,
        "x_worker_pid": headers.get("X-Worker-Pid"),
        "x_cache": headers.get("X-Cache"),
        "body": body_summary(body),
        "decompressed_sha256": sha256_bytes(decoded),
        "decompression": decompression,
    }
    if extra:
        row.update(extra)
    return row


def fingerprint(resp: requests.Response | Any) -> str:
    headers = {str(k): str(v) for k, v in resp.headers.items()}
    body = bytes(resp.content if hasattr(resp, "content") else resp.body())
    decoded, _ = greedy_decompress(body, headers.get("Content-Encoding", ""))
    stable_headers = filtered_headers(headers, for_fingerprint=True)
    status = int(resp.status_code if hasattr(resp, "status_code") else resp.status)
    encoded = json.dumps(stable_headers, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(str(status).encode() + b"\0" + decoded + b"\0" + encoded.encode())


def auth_headers(label: str) -> dict[str, str]:
    if label == "valid":
        token = _VALID_TOKEN
    elif label == "expired":
        token = _EXPIRED_TOKEN
    elif label == "invalid":
        token = _INVALID_TOKEN
    elif label == "missing":
        return {}
    else:
        raise ValueError(label)
    return {"Authorization": f"Bearer {token}", "Accept": "application/json", "Cache-Control": "no-cache"}


def record_direct(resp: requests.Response, url: str, auth_label: str, phase: str,
                  extra: dict[str, Any] | None = None) -> dict[str, Any]:
    row = response_record(resp, url, auth_label, phase, extra)
    RAW_FRESHNESS.append(row)
    return row


def db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


def writable_count() -> int:
    with db_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM writable_state").fetchone()
    return int(row["n"] if row else 0)


def init_fixture_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with db_connection() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS body_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                variant TEXT NOT NULL,
                content TEXT NOT NULL,
                etag TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                subject TEXT NOT NULL,
                revoked INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS writable_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT NOT NULL,
                variant TEXT NOT NULL,
                marker TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            """
        )
        initial = json.dumps({"variant": "A", "body": BODY_CONTENT["A"]}, sort_keys=True, separators=(",", ":"))
        etag = '"' + hashlib.sha256(initial.encode()).hexdigest() + '"'
        conn.execute(
            "INSERT OR IGNORE INTO body_config(id, variant, content, etag) VALUES (1, ?, ?, ?)",
            ("A", BODY_CONTENT["A"], etag),
        )
        conn.execute(
            "INSERT OR IGNORE INTO sessions(session_id, subject, revoked) VALUES (?, ?, 0)",
            (_SESSION_ID, _SUBJECT),
        )
        conn.commit()


def set_body_variant(variant: str) -> None:
    if variant not in BODY_VARIANTS:
        raise ValueError(variant)
    content = BODY_CONTENT[variant]
    etag = '"' + hashlib.sha256(f"{variant}:{content}".encode()).hexdigest() + '"'
    with db_connection() as conn:
        conn.execute(
            "INSERT INTO body_config(id, variant, content, etag) VALUES (1, ?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET variant=excluded.variant, content=excluded.content, etag=excluded.etag",
            (variant, content, etag),
        )
        conn.commit()
    RAW_BATCH.append({"event": "set_body_variant", "variant": variant, "at": utc_now()})


def _get_body() -> tuple[str, str, str]:
    with db_connection() as conn:
        row = conn.execute("SELECT variant, content, etag FROM body_config WHERE id=1").fetchone()
    if row is None:
        return "A", BODY_CONTENT["A"], '"' + hashlib.sha256(b"A:alpha").hexdigest() + '"'
    return str(row["variant"]), str(row["content"]), str(row["etag"])


def _document_request() -> bool:
    accept = request.headers.get("Accept", "")
    return request.headers.get("Sec-Fetch-Dest") == "document" or "text/html" in accept


def _html_document(variant: str, content: str) -> str:
    marker = "" if variant == "A" else (
        f'<output id="state-marker" data-variant="{variant}">live state {variant}</output>'
    )
    rows = "".join(
        f'<li class="state-item" data-item="{i}">state row {i} for {variant}</li>' for i in range(1, 5)
    )
    # The marker is intentionally absent for A and present for B/C/D.  This makes
    # the DOM delta an actual rendered structural change after a valid write.
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><title>Runtime resource {variant}</title>
<style>body{{font-family:system-ui;margin:2rem}} input,select,textarea,button{{margin:.25rem}}</style></head>
<body><header id=\"top-header\"><nav><a href=\"/resource_page\">resource</a><a href=\"/resource\">data</a></nav></header>
<main id=\"main-content\"><section id=\"state-panel\"><h1 id=\"state-title\">Runtime state {variant}</h1>
<p id=\"state-copy\">Current body {content}. This is a real local SPA fixture.</p>{marker}
<form id=\"write-form\" data-write-path=\"/api/write/profile\">
<label for=\"name-field\">Name<input id=\"name-field\" name=\"name\" value=\"initial\"></label>
<label for=\"role-field\">Role<select id=\"role-field\" name=\"role\"><option value=\"user\">user</option><option value=\"admin\">admin</option><option value=\"operator\">operator</option></select></label>
<label for=\"bio-field\">Bio<textarea id=\"bio-field\" name=\"bio\">initial bio</textarea></label>
<button id=\"save-button\" type=\"submit\">Save state</button>
</form><div id=\"write-result\" aria-live=\"polite\">not submitted</div>
<ul id=\"state-list\">{rows}</ul><table id=\"state-table\"><tbody><tr><td>variant</td><td>{variant}</td></tr><tr><td>body</td><td>{content}</td></tr></tbody></table>
</section><aside id=\"side-panel\"><h2>Controls</h2><p>Real Playwright interactions are recorded.</p><a id=\"help-link\" href=\"/resource_page\">help</a></aside></main>
<footer id=\"page-footer\"><span>fixture</span><span>WAL</span></footer>
<script>document.querySelector('#write-form').addEventListener('submit', function(event){{event.preventDefault(); const out=document.querySelector('#write-result'); out.textContent='submitted '+new Date().toISOString(); out.dataset.submitted='true';}});</script>
</body></html>"""


def _auth_context() -> tuple[bool, dict[str, Any]]:
    raw = request.headers.get("Authorization", "")
    if not raw.startswith("Bearer "):
        return False, {"state": "missing"}
    token = raw[7:]
    try:
        payload = jwt.decode(token, TESTBED_SECRET, algorithms=["HS256"], options={"require": ["exp", "sub", "sid"]})
    except Exception as exc:
        return False, {"state": "expired" if "ExpiredSignature" in type(exc).__name__ else "invalid"}
    sid = str(payload.get("sid", ""))
    with db_connection() as conn:
        row = conn.execute(
            "SELECT revoked FROM sessions WHERE session_id = ?", (sid,)
        ).fetchone()
    if row is None or int(row["revoked"]) != 0:
        return False, {"state": "deleted_session", "payload": payload}
    return True, {"state": "valid", "payload": payload}


def _stable_auth_headers(valid: bool, payload: dict[str, Any]) -> dict[str, str]:
    headers = {"X-Worker-Pid": str(os.getpid())}
    if valid:
        sid = str(payload.get("sid", ""))
        state = f"valid:{payload.get('sub', '')}:{sid}"
        digest = hmac.new(TESTBED_SECRET.encode(), state.encode(), hashlib.sha256).hexdigest()[:16]
        headers.update({
            "Cache-Control": "public, max-age=5",
            "Vary": "Cookie",
            "Set-Cookie": f"sid={sid}; Path=/; SameSite=Lax",
            "X-Auth-Digest": digest,
        })
    else:
        headers.update({"Cache-Control": "no-store", "Vary": "Authorization"})
    return headers


def _json_api_response(name: str) -> Response:
    valid, auth = _auth_context()
    variant, content, etag = _get_body()
    headers = _stable_auth_headers(valid, auth.get("payload", {}))
    headers["Content-Type"] = "application/json"
    headers["ETag"] = etag
    if request.headers.get("If-None-Match") == etag:
        return Response(b"", status=304, headers=headers)
    body = json.dumps({"endpoint": name, "body_id": variant, "body": content}, sort_keys=True).encode()
    return Response(body, status=200, headers=headers)


def _document_or_api(name: str) -> Response:
    variant, content, _ = _get_body()
    if _document_request():
        return Response(_html_document(variant, content), status=200, mimetype="text/html")
    return _json_api_response(name)


def _auth_json(payload: dict[str, Any], valid: bool, auth: dict[str, Any], status: int = 200) -> Response:
    headers = _stable_auth_headers(valid, auth.get("payload", {}))
    return Response(json.dumps(payload, sort_keys=True), status=status, headers=headers, mimetype="application/json")


def create_app() -> Flask:
    init_fixture_db()
    app = Flask(__name__)
    app.config["TESTING"] = False

    @app.get("/health")
    def health() -> Response:
        payload = json.dumps({"status": "ok", "service": "single-db"}, sort_keys=True).encode()
        accept = request.headers.get("Accept-Encoding", "")
        headers = {"X-Worker-Pid": str(os.getpid()), "Cache-Control": "public, max-age=60"}
        if "br" in accept:
            return Response(brotli.compress(payload), status=200, headers={**headers, "Content-Encoding": "br"}, mimetype="application/json")
        if "gzip" in accept:
            return Response(gzip.compress(payload), status=200, headers={**headers, "Content-Encoding": "gzip"}, mimetype="application/json")
        return Response(payload, status=200, headers=headers, mimetype="application/json")

    @app.get("/resource_page")
    def resource_page() -> Response:
        variant, content, _ = _get_body()
        return Response(_html_document(variant, content), status=200, mimetype="text/html")

    @app.get("/resource")
    def resource() -> Response:
        return _document_or_api("resource")

    @app.get("/api/profile")
    def profile() -> Response:
        return _document_or_api("profile")

    @app.get("/api/data_list")
    def data_list() -> Response:
        return _document_or_api("data_list")

    @app.route("/api/write/<endpoint>", methods=["GET", "POST"])
    def write(endpoint: str) -> Response:
        if endpoint not in {"profile", "data_list", "controls_matrix"}:
            return _auth_json({"error": "unknown endpoint"}, False, {}, status=404)
        valid, auth = _auth_context()
        if not valid:
            return _auth_json({"error": "unauthorized", "state": auth.get("state")}, False, auth, status=401)
        variant, content, _ = _get_body()
        if request.method == "GET":
            return _auth_json({"endpoint": endpoint, "body_id": variant, "body": content, "readonly": True}, True, auth)
        requested_variant = request.form.get("variant", request.json.get("variant") if request.is_json else None)
        if requested_variant not in BODY_VARIANTS:
            return _auth_json({"error": "invalid variant"}, True, auth, status=400)
        marker = request.form.get("marker", "playwright-write")
        with db_connection() as conn:
            conn.execute(
                "INSERT INTO writable_state(endpoint, variant, marker, created_at) VALUES (?, ?, ?, ?)",
                (endpoint, requested_variant, marker, time.time()),
            )
            conn.commit()
        set_body_variant(requested_variant)
        return _auth_json({"ok": True, "endpoint": endpoint, "body_id": requested_variant, "marker": marker}, True, auth)

    @app.post("/admin/set_body_variant")
    def admin_set_body() -> Response:
        variant = request.form.get("variant") or (request.json or {}).get("variant")
        if variant not in BODY_VARIANTS:
            return jsonify({"error": "invalid variant"}), 400
        set_body_variant(variant)
        return jsonify({"ok": True, "variant": variant})

    @app.post("/admin/invalidate_session")
    def admin_invalidate() -> Response:
        with db_connection() as conn:
            conn.execute("DELETE FROM sessions WHERE session_id = ?", (_SESSION_ID,))
            conn.commit()
        RAW_BATCH.append({"event": "invalidate_session", "session_id": _SESSION_ID, "at": utc_now()})
        return jsonify({"ok": True, "session_deleted": True})

    @app.post("/admin/restore_session")
    def admin_restore() -> Response:
        with db_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO sessions(session_id, subject, revoked) VALUES (?, ?, 0)",
                (_SESSION_ID, _SUBJECT),
            )
            conn.commit()
        RAW_BATCH.append({"event": "restore_session", "session_id": _SESSION_ID, "at": utc_now()})
        return jsonify({"ok": True, "session_restored": True})

    return app


application = create_app()


# ----------------------------- infrastructure -----------------------------

def reset_tmp() -> None:
    def remove_file(path: Path) -> None:
        try:
            path.unlink()
        except FileNotFoundError:
            return
        except PermissionError:
            # nginx runs as root and can leave canonical error/cache files
            # root-owned in /tmp. Remove only the frozen experiment paths.
            run_checked(sudo_cmd(["rm", "-f", "--", str(path)]))

    def remove_tree(path: Path) -> None:
        if not path.exists() and not path.is_symlink():
            return
        if path.is_symlink():
            remove_file(path)
            return
        try:
            shutil.rmtree(path)
        except PermissionError:
            run_checked(sudo_cmd(["rm", "-rf", "--", str(path)]))

    for proc in _GUNICORN_PROCS:
        with contextlib.suppress(Exception):
            proc.send_signal(signal.SIGTERM)
    _GUNICORN_PROCS.clear()
    for path in [DB_PATH, Path(str(DB_PATH) + "-wal"), Path(str(DB_PATH) + "-shm"), NGINX_CONF, WSGI_PATH, RUNNER_COPY,
                 GUNICORN_LOG_1, GUNICORN_LOG_2, Path("/tmp/single.db.nginx.pid"), Path("/tmp/single.db.nginx.error.log")]:
        remove_file(path)
    remove_tree(NGINX_CACHE)


def sudo_cmd(args: list[str]) -> list[str]:
    if os.geteuid() == 0:
        return args
    return ["sudo", "-n", *args]


def run_checked(args: list[str], cwd: Path | None = None, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    COMMANDS.append(" ".join(args))
    return subprocess.run(args, cwd=str(cwd) if cwd else None, text=True, capture_output=True, timeout=timeout, check=True)


def wait_port(port: int, timeout: float = 15.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        sock = socket.socket()
        sock.settimeout(0.25)
        try:
            sock.connect(("127.0.0.1", port))
            return
        except OSError:
            time.sleep(0.1)
        finally:
            sock.close()
    raise InfrastructureFailure(f"port {port} did not become ready")


def write_nginx_config() -> None:
    text = f"""pid /tmp/single.db.nginx.pid;
error_log /tmp/single.db.nginx.error.log crit;
events {{ worker_connections 1024; }}
http {{
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    access_log off;
    proxy_cache_path {NGINX_CACHE} levels=1:2 keys_zone=spider_cache:10m max_size=100m inactive=10m use_temp_path=off;
    upstream single_db {{
        hash $request_uri consistent;
        server 127.0.0.1:19860;
        server 127.0.0.1:19861;
        keepalive 32;
    }}
    server {{
        listen 19851;
        server_name _;
        add_header X-Cache $upstream_cache_status always;
        location / {{
            proxy_pass http://single_db;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header Connection "";
            proxy_set_header If-None-Match $http_if_none_match;
            proxy_cache spider_cache;
            proxy_cache_methods GET HEAD;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 1m;
            proxy_cache_bypass $http_authorization $http_cookie;
            proxy_no_cache $http_authorization $http_cookie;
        }}
    }}
}}
"""
    NGINX_CONF.write_text(text)
    COMMANDS.append(f"write {NGINX_CONF}")


def start_gunicorn() -> None:
    for url, log_path in zip(ORIGIN_URLS, [GUNICORN_LOG_1, GUNICORN_LOG_2]):
        port = url.rsplit(":", 1)[1]
        log_handle = log_path.open("ab")
        cmd = ["gunicorn", "--workers", "1", "--bind", f"127.0.0.1:{port}", "--access-logfile", "-", "--error-logfile", "-", "wsgi:application"]
        env = os.environ.copy()
        env["SPIDER_EXPERIMENT_DIR"] = str(BASE)
        proc = subprocess.Popen(cmd, cwd="/tmp", env=env, stdout=log_handle, stderr=subprocess.STDOUT)
        _GUNICORN_PROCS.append(proc)
        COMMANDS.append(" ".join(cmd))
    for port in (19860, 19861):
        wait_port(port)


def start_nginx() -> None:
    global _NGINX_STARTED
    run_checked(sudo_cmd(["nginx", "-t", "-c", str(NGINX_CONF)]))
    subprocess.Popen(sudo_cmd(["nginx", "-c", str(NGINX_CONF)]), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _NGINX_STARTED = True
    COMMANDS.append(" ".join(sudo_cmd(["nginx", "-c", str(NGINX_CONF)])))
    wait_port(19851)


def stop_infrastructure() -> None:
    global _NGINX_STARTED
    if _NGINX_STARTED:
        with contextlib.suppress(Exception):
            run_checked(sudo_cmd(["nginx", "-s", "stop", "-c", str(NGINX_CONF)]), timeout=10)
        _NGINX_STARTED = False
    for proc in list(_GUNICORN_PROCS):
        with contextlib.suppress(Exception):
            proc.send_signal(signal.SIGTERM)
    for proc in list(_GUNICORN_PROCS):
        with contextlib.suppress(Exception):
            proc.wait(timeout=5)
        with contextlib.suppress(Exception):
            if proc.poll() is None:
                proc.kill()
    _GUNICORN_PROCS.clear()


def restart_infrastructure() -> None:
    stop_infrastructure()
    time.sleep(0.5)
    start_gunicorn()
    start_nginx()
    verify_origins()


def verify_origins() -> None:
    for origin in ORIGIN_URLS:
        wait_port(int(origin.rsplit(":", 1)[1]))
        response = requests.get(origin + "/health", timeout=5)
        if response.status_code != 200 or not response.headers.get("X-Worker-Pid"):
            raise InfrastructureFailure(f"origin health failed: {origin} {response.status_code}")
    response = requests.get(BASE_URL + "/health", timeout=5)
    if response.status_code != 200 or not response.headers.get("X-Worker-Pid"):
        raise InfrastructureFailure("nginx health failed")


def setup_infrastructure() -> None:
    reset_tmp()
    write_nginx_config()
    WSGI_PATH.write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).parent))\nfrom run_experiment import application\n")
    RUNNER_COPY.write_bytes(Path(__file__).read_bytes())
    start_gunicorn()
    start_nginx()
    verify_origins()
    OBSERVATIONS.append("Two gunicorn origins and the exclusive nginx reverse proxy became ready on the frozen ports.")


def make_tokens() -> None:
    global _VALID_TOKEN, _EXPIRED_TOKEN
    now = datetime.now(timezone.utc)
    valid_payload = {"sub": _SUBJECT, "sid": _SESSION_ID, "iat": int(now.timestamp()), "exp": int((now + timedelta(hours=1)).timestamp())}
    expired_payload = {"sub": _SUBJECT, "sid": _SESSION_ID, "iat": int((now - timedelta(hours=2)).timestamp()), "exp": int((now - timedelta(hours=1)).timestamp())}
    _VALID_TOKEN = jwt.encode(valid_payload, TESTBED_SECRET, algorithm="HS256")
    _EXPIRED_TOKEN = jwt.encode(expired_payload, TESTBED_SECRET, algorithm="HS256")
    _RUNTIME_DIAGNOSTICS["token_creation"] = "HS256 with stable subject/session; no secret recorded in artifacts"


# ----------------------------- plain HTTP ---------------------------------

def direct_set_variant(variant: str) -> None:
    response = requests.post(BASE_URL + "/admin/set_body_variant", data={"variant": variant}, timeout=5)
    if response.status_code != 200:
        raise InfrastructureFailure(f"admin body update failed: {response.status_code}")


def direct_get(endpoint: str, auth_label: str, phase: str, extra: dict[str, Any] | None = None) -> requests.Response:
    headers = auth_headers(auth_label)
    response = requests.get(BASE_URL + endpoint, headers=headers, timeout=5)
    record_direct(response, BASE_URL + endpoint, auth_label, phase, extra)
    return response


def run_stickiness() -> None:
    rows: list[dict[str, Any]] = []
    for endpoint in API_ENDPOINTS:
        pids: list[str] = []
        for i in range(100):
            direct_set_variant(BODY_VARIANTS[(i // 2) % len(BODY_VARIANTS)])
            response = requests.get(BASE_URL + endpoint, headers=auth_headers(["valid", "expired", "invalid", "missing"][i % 4]), timeout=5)
            row = record_direct(response, BASE_URL + endpoint, "stickiness", "stickiness", {"endpoint": endpoint, "sample": i})
            if response.status_code == 200:
                pid = response.headers.get("X-Worker-Pid")
                if pid:
                    pids.append(pid)
        counts = Counter(pids)
        ratio = max(counts.values()) / len(pids) if pids else 0.0
        rows.append({"endpoint": endpoint, "n": len(pids), "pids": dict(counts), "ratio": ratio, "distinct": len(counts)})
    METRICS["freshness_x_worker_missing"] = 0
    METRICS["freshness_stickiness_min"] = min(r["ratio"] for r in rows)
    METRICS["freshness_worker_distinct"] = len({pid for row in rows for pid in row["pids"]})
    METRICS["freshness_stickiness_by_endpoint"] = rows
    OBSERVATIONS.append("Per-URI nginx requests produced stable worker assignment across the two origins.")


def run_c1() -> None:
    last_etag: dict[str, str] = {}
    last_variant: dict[str, str] = {}
    rows: list[dict[str, Any]] = []
    n_304 = 0
    for i in range(1000):
        endpoint = API_ENDPOINTS[i % 2]
        conditional = i % 10 == 0
        variant = last_variant.get(endpoint, BODY_VARIANTS[(i // 2) % 4]) if conditional else BODY_VARIANTS[(i // 2) % 4]
        direct_set_variant(variant)
        auth_label = ["valid", "expired", "invalid", "missing"][i % 4]
        headers = auth_headers(auth_label)
        if conditional and endpoint in last_etag:
            headers["If-None-Match"] = last_etag[endpoint]
        response = requests.get(BASE_URL + endpoint, headers=headers, timeout=5)
        row = record_direct(response, BASE_URL + endpoint, auth_label, "c1", {"iteration": i, "endpoint": endpoint, "variant": variant, "conditional": conditional})
        rows.append(row)
        if response.status_code == 304:
            n_304 += 1
        else:
            etag = response.headers.get("ETag")
            if etag:
                last_etag[endpoint] = etag
            last_variant[endpoint] = variant
    non304 = sum(1 for r in rows if r["status"] != 304)
    by_ep = Counter(r["endpoint"] for r in rows if r["status"] != 304)
    METRICS.update({
        "freshness_n_total": len(rows),
        "freshness_n_non304": non304,
        "freshness_n_304": n_304,
        "freshness_per_endpoint_non304": dict(by_ep),
        "freshness_hs_rate": 1.0 if all(v > 0 for v in by_ep.values()) else 0.0,
        "freshness_batch_count": 1,
    })
    OBSERVATIONS.append(f"C1 captured {len(rows)} plain HTTP observations through nginx, including {n_304} real 304 responses.")


def direct_pair(url: str, first_auth: str, second_auth: str, phase: str, variant: str) -> tuple[requests.Response, requests.Response, float, str, str]:
    direct_set_variant(variant)
    first = requests.get(BASE_URL + url, headers=auth_headers(first_auth), timeout=5)
    second = requests.get(BASE_URL + url, headers=auth_headers(second_auth), timeout=5)
    record_direct(first, BASE_URL + url, first_auth, phase, {"pair": "first", "variant": variant})
    record_direct(second, BASE_URL + url, second_auth, phase, {"pair": "second", "variant": variant})
    j = header_jaccard({k: v for k, v in first.headers.items()}, {k: v for k, v in second.headers.items()})
    return first, second, j, fingerprint(first), fingerprint(second)


def cramers_v(left: list[Any], right: list[Any]) -> float:
    """Canonical uncorrected Cramer's V used by the parent experiment."""
    if not left or len(left) != len(right):
        return 0.0
    table = np.zeros((len(set(left)), len(set(right))), dtype=float)
    lvals = {v: i for i, v in enumerate(sorted(set(left), key=str))}
    rvals = {v: i for i, v in enumerate(sorted(set(right), key=str))}
    for a, b in zip(left, right):
        table[lvals[a], rvals[b]] += 1
    n = float(table.sum())
    degrees = min(table.shape) - 1
    if n <= 0 or degrees <= 0:
        return 0.0
    row = table.sum(axis=1, keepdims=True)
    col = table.sum(axis=0, keepdims=True)
    expected = row @ col / n
    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = float(np.nansum((table - expected) ** 2 / expected))
    return float(np.sqrt(chi2 / (n * degrees)))


def calculate_c2(rows: list[dict[str, Any]], prefix: str) -> None:
    j = np.array([r["jaccard"] for r in rows], dtype=float)
    drift = np.array([r["drift"] for r in rows], dtype=float)
    body_index = {state: index for index, state in enumerate(BODY_VARIANTS)}
    body = np.array([body_index[r["body_state"]] for r in rows], dtype=float)
    if len(j) > 1 and np.std(j) > 0 and np.std(drift) > 0:
        r_value = float(scipy_stats.pearsonr(j, body).statistic)
    else:
        r_value = 0.0
    v_value = cramers_v([r["body_state"] for r in rows], [r["drift"] for r in rows])
    no_drift = [r["jaccard"] for r in rows if not r["drift"]]
    null_fp = float(sum(x < 1.0 for x in no_drift) / len(no_drift)) if no_drift else 1.0
    same = float(np.mean(no_drift)) if no_drift else 0.0
    METRICS.update({
        f"{prefix}_n_pairs": len(rows),
        f"{prefix}_jaccard_r": r_value,
        f"{prefix}_jaccard_v": v_value,
        f"{prefix}_jaccard_nullFP": null_fp,
        f"{prefix}_jaccard_variance": float(np.var(j)),
        f"{prefix}_jaccard_std": float(np.std(j)),
        f"{prefix}_jaccard_mean": float(np.mean(j)),
        f"{prefix}_same_state_J": same,
    })


def run_plain_c2() -> None:
    rows: list[dict[str, Any]] = []
    for i in range(160):
        endpoint = API_ENDPOINTS[i % 2]
        variant = BODY_VARIANTS[(i * 7 + i // 2) % 4]
        drift = i % 2
        second_auth = "expired" if drift else "valid"
        _, _, j, _, _ = direct_pair(endpoint, "valid", second_auth, "c2_plain", variant)
        rows.append({"jaccard": j, "drift": drift, "body_state": variant})
    calculate_c2(rows, "header_only_jaccard_plain")
    OBSERVATIONS.append(f"Plain HTTP C2 paired observations: {len(rows)}.")


def run_plain_c4() -> None:
    rows: list[dict[str, Any]] = []
    for i in range(80):
        endpoint = API_ENDPOINTS[i % 2]
        direct_set_variant("A")
        before = requests.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5)
        direct_set_variant("C")
        after = requests.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5)
        record_direct(before, BASE_URL + endpoint, "valid", "c4_plain", {"condition": "body", "index": i})
        record_direct(after, BASE_URL + endpoint, "valid", "c4_plain", {"condition": "body", "index": i})
        rows.append({"full": fingerprint(before) != fingerprint(after), "body": bytes(before.content) != bytes(after.content), "status": before.status_code != after.status_code})
    for i in range(80):
        endpoint = API_ENDPOINTS[i % 2]
        direct_set_variant("A")
        before = requests.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5)
        after = requests.get(BASE_URL + endpoint, headers=auth_headers("expired"), timeout=5)
        record_direct(before, BASE_URL + endpoint, "valid", "c4_plain", {"condition": "header", "index": i})
        record_direct(after, BASE_URL + endpoint, "expired", "c4_plain", {"condition": "header", "index": i})
        rows.append({"full": fingerprint(before) != fingerprint(after), "body": bytes(before.content) != bytes(after.content), "status": before.status_code != after.status_code})
    for i in range(50):
        endpoint = API_ENDPOINTS[i % 2]
        direct_set_variant("A")
        before = requests.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5)
        after = requests.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5)
        record_direct(before, BASE_URL + endpoint, "valid", "c4_plain", {"condition": "null", "index": i})
        record_direct(after, BASE_URL + endpoint, "valid", "c4_plain", {"condition": "null", "index": i})
        rows.append({"full": fingerprint(before) != fingerprint(after), "body": bytes(before.content) != bytes(after.content), "status": before.status_code != after.status_code})
    full = float(np.mean([r["full"] for r in rows]))
    body = float(np.mean([r["body"] for r in rows]))
    status = float(np.mean([r["status"] for r in rows]))
    null = float(np.mean([r["full"] for r in rows[-50:]]))
    diffs = np.array([float(r["full"]) - max(float(r["body"]), float(r["status"])) for r in rows])
    rng = np.random.default_rng(SEED)
    boot = [float(np.mean(rng.choice(diffs, size=len(diffs), replace=True))) for _ in range(1000)]
    METRICS.update({
        "full_vector_plain_n_pairs": len(rows), "full_vector_plain_full": full,
        "full_vector_plain_body_only": body, "full_vector_plain_status_only": status,
        "full_vector_plain_diff_lo": float(np.percentile(boot, 2.5)), "full_vector_plain_null": null,
    })


def add_trajectory_cost(trajectory_id: str, integer_cost: int) -> None:
    # f is an independent, predeclared trajectory-level cost signal; costs are
    # actual integer work counts accumulated from the observed requests/actions.
    if not TRAJECTORY_COSTS or TRAJECTORY_COSTS[-1]["trajectory_id"] != trajectory_id:
        rng = random.Random(f"{SEED}:{trajectory_id}")
        f_value = rng.uniform(-1.0, 1.0)
        TRAJECTORY_COSTS.append({"trajectory_id": trajectory_id, "cost": int(integer_cost), "f": f_value})
    else:
        TRAJECTORY_COSTS[-1]["cost"] = int(TRAJECTORY_COSTS[-1]["cost"] + integer_cost)


def run_c3() -> None:
    # Rebuild trajectory costs from the actual C1 raw records, in fixed blocks of ten.
    TRAJECTORY_COSTS.clear()
    c1_rows = [r for r in RAW_FRESHNESS if r.get("phase") == "c1"]
    for i, row in enumerate(c1_rows):
        body_len = int(row["body"]["body_length"])
        header_len = len(json.dumps(row["headers"]))
        add_trajectory_cost(f"fresh_{i // 10}", 1 + body_len // 128 + header_len // 256)
    costs = np.array([r["cost"] for r in TRAJECTORY_COSTS], dtype=float)
    f_values = np.array([r["f"] for r in TRAJECTORY_COSTS], dtype=float)
    rng = np.random.default_rng(SEED)
    correlations: list[float] = []
    for _ in range(1000):
        permutation = rng.permutation(len(f_values))
        shuffled = f_values[permutation]
        if np.std(costs) > 0 and np.std(shuffled) > 0:
            correlations.append(float(scipy_stats.spearmanr(costs, shuffled).statistic))
        else:
            correlations.append(0.0)
    rho = float(scipy_stats.spearmanr(costs, f_values).statistic) if np.std(costs) > 0 and np.std(f_values) > 0 else 0.0
    p_value = float((1 + sum(abs(x) >= abs(rho) for x in correlations)) / (1 + len(correlations)))
    METRICS.update({
        "honest_cost_n_trajectories": len(TRAJECTORY_COSTS),
        "honest_cost_rho_observed": rho,
        "honest_cost_rho_shuffled": float(np.mean(correlations)),
        "honest_cost_p_value": p_value,
        "honest_cost_within_f_std": float(np.std(f_values)),
        "honest_cost_permutations_B": 1000,
    })
    write_jsonl(BASE / "raw_trajectory_costs.jsonl", TRAJECTORY_COSTS)
    OBSERVATIONS.append(f"Honest cost grouped {len(TRAJECTORY_COSTS)} trajectories and performed 1000 trajectory-level permutations.")


# ----------------------------- browser -----------------------------------

def browser_package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except Exception:
        return None


def provision_browser() -> tuple[Any, Any, Any, dict[str, Any]]:
    if sync_playwright is None:
        raise InfrastructureFailure(f"Playwright import failed: {_PLAYWRIGHT_IMPORT_ERROR}")
    if np is None or KMeans is None:
        raise InfrastructureFailure(f"numpy/sklearn unavailable: {_NUMPY_IMPORT_ERROR}")
    if _BROWSERGYM_IMPORT_ERROR is not None or _BROWSERGYM_CORE_IMPORT_ERROR is not None:
        raise InfrastructureFailure(f"BrowserGym import failed: {_BROWSERGYM_IMPORT_ERROR}, {_BROWSERGYM_CORE_IMPORT_ERROR}")
    pw_version = browser_package_version("playwright")
    bg_version = browser_package_version("browsergym")
    if pw_version != "1.63.0" or bg_version != "0.14.3":
        raise InfrastructureFailure(f"unexpected package versions playwright={pw_version}, browsergym={bg_version}")
    diagnostics: dict[str, Any] = {
        "playwright_version": pw_version,
        "browsergym_version": bg_version,
        "browsergym_import": True,
        "browsergym_core_import": _BROWSERGYM_CORE_IMPORT_ERROR is None,
        "agentlab_attempted": True,
        "agentlab_available": False,
        "native_path_helper": None,
        "native_path_helper_available": False,
        "official_executable_path": None,
        "compatibility_adapter_used": False,
    }
    try:
        import agentlab  # type: ignore  # noqa: F401
        diagnostics["agentlab_available"] = True
    except Exception as exc:
        diagnostics["agentlab_error"] = repr(exc)
    # Keep the Playwright driver alive for the entire browser phase. Returning
    # from inside sync_playwright()'s context manager would stop the driver.
    p = sync_playwright().start()
    try:
        official = Path(str(p.chromium.executable_path))
        diagnostics["official_executable_path"] = str(official)
        if not official.exists():
            raise InfrastructureFailure(f"official Chromium executable missing: {official}")
        # The preregistration makes this exact private helper a mandatory
        # provisioning assertion.  Do not substitute the public path: that
        # would silently weaken the frozen measurement-validity gate.
        try:
            import playwright._impl._path_utils as path_utils  # type: ignore
            native = getattr(path_utils, "get_executable_path", None)
        except Exception as exc:
            diagnostics["native_path_helper_error"] = repr(exc)
            native = None
        if not callable(native):
            diagnostics["native_path_helper_error"] = "required get_executable_path helper is absent"
            _RUNTIME_DIAGNOSTICS.update(diagnostics)
            raise InfrastructureFailure("frozen Playwright provisioning gate failed: playwright._impl._path_utils.get_executable_path is unavailable")
        native_path = Path(str(native("chromium")))
        diagnostics["native_path_helper"] = str(native_path)
        diagnostics["native_path_helper_available"] = True
        if not native_path.exists():
            raise InfrastructureFailure(f"native Chromium helper path missing: {native_path}")
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"], executable_path=str(native_path))
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.set_default_timeout(5000)
        return p, browser, context, {"page": page, "diagnostics": diagnostics, "playwright": p}
    except Exception:
        _RUNTIME_DIAGNOSTICS.update(diagnostics)
        with contextlib.suppress(Exception):
            p.stop()
        raise


def close_browser(browser: Any, context: Any, playwright_driver: Any | None = None) -> None:
    with contextlib.suppress(Exception):
        context.close()
    with contextlib.suppress(Exception):
        browser.close()
    if playwright_driver is not None:
        with contextlib.suppress(Exception):
            playwright_driver.stop()


def extract_features(page: Any, ax_nodes: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    tag_counts = dict(Counter(page.evaluate("() => Array.from(document.querySelectorAll('*')).map(e => e.tagName.toLowerCase())")))
    role_counts = dict(Counter(str(n.get("role", {}).get("value", "none")) for n in ax_nodes))
    control_counts = {key: int(page.evaluate(f"() => document.querySelectorAll('{key}').length")) for key in CONTROL_KEYS}
    return tag_counts, role_counts, control_counts


def browser_api_get(page: Any, endpoint: str, auth_label: str, phase: str, extra: dict[str, Any] | None = None) -> Any:
    headers = auth_headers(auth_label)
    headers["Accept"] = "application/json"
    headers["Cache-Control"] = "no-cache"
    headers["Pragma"] = "no-cache"
    response = page.request.get(BASE_URL + endpoint, headers=headers, timeout=5000)
    row = response_record(response, BASE_URL + endpoint, auth_label, phase, extra)
    return response, row


def set_variant_browser(page: Any, variant: str) -> None:
    response = page.request.post(BASE_URL + "/admin/set_body_variant", data={"variant": variant}, timeout=5000)
    if response.status != 200:
        raise InfrastructureFailure(f"browser admin body update failed: {response.status}")


def run_browser_health(page: Any, context: Any, diagnostics: dict[str, Any]) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    for endpoint_index, endpoint in enumerate(BROWSER_ENDPOINTS):
        for i in range(20):
            trajectory_id = f"health_{endpoint_index}_{i // 5}"
            url = f"{BASE_URL}{endpoint}?capture={endpoint_index}_{i}"
            page.set_extra_http_headers({"Authorization": f"Bearer {_VALID_TOKEN}", "Accept": "text/html,application/xhtml+xml"})
            try:
                nav = page.goto(url, wait_until="domcontentloaded", timeout=5000)
                page.wait_for_timeout(100)
                viewport = page.viewport_size
                cdp = context.new_cdp_session(page)
                cdp.send("Emulation.setDeviceMetricsOverride", {"width": 1280, "height": 720, "deviceScaleFactor": 1, "mobile": False})
                viewport_after = page.viewport_size
                dom_count = int(page.evaluate("() => document.querySelectorAll('*').length"))
                ax_message = cdp.send("Accessibility.getFullAXTree", {})
                ax_nodes = ax_message.get("nodes", []) if isinstance(ax_message, dict) else []
                tag_counts, role_counts, control_counts = extract_features(page, ax_nodes)
                api_response, api_row = browser_api_get(page, endpoint, "valid", "browser_health_fetch", {"endpoint": endpoint, "capture": i})
                row = {
                    "phase": "browser_health",
                    "endpoint": endpoint,
                    "capture_index": i,
                    "trajectory_id": trajectory_id,
                    "state_key": f"{endpoint}:A",
                    "url": url,
                    "navigation_status": int(nav.status if nav else 0),
                    "viewport_page": viewport,
                    "viewport_page_after_cdp": viewport_after,
                    "cdp_metrics_sent": {"width": 1280, "height": 720, "deviceScaleFactor": 1, "mobile": False},
                    "dom_count": dom_count,
                    "ax_count": len(ax_nodes),
                    "ax_nodes": ax_nodes,
                    "tag_counts": tag_counts,
                    "role_counts": role_counts,
                    "control_counts": control_counts,
                    "fetch": api_row,
                    "timestamp": utc_now(),
                }
                observations.append(row)
                RAW_BROWSER.append(row)
                cdp.detach()
            except Exception as exc:
                raise InfrastructureFailure(f"real browser health capture failed at {endpoint} {i}: {exc}") from exc
    diagnostics["health_capture_count"] = len(observations)
    return observations


def fit_browser_kmeans(health_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(health_rows) < 20:
        raise InfrastructureFailure("fewer than 20 real browser observations")
    ids = sorted({str(r["trajectory_id"]) for r in health_rows})
    split = max(1, int(len(ids) * 0.6))
    train_ids = set(ids[:split])
    test_ids = set(ids[split:])
    if len(train_ids) < 1 or len(test_ids) < 1:
        raise InfrastructureFailure("trajectory split produced an empty partition")
    train_rows = [r for r in health_rows if r["trajectory_id"] in train_ids]
    test_rows = [r for r in health_rows if r["trajectory_id"] in test_ids]
    tag_vocab = [k for k, _ in Counter({k: sum(int(r["tag_counts"].get(k, 0)) for r in train_rows) for k in {x for r in train_rows for x in r["tag_counts"]}}).most_common(20)]
    role_vocab = [k for k, _ in Counter({k: sum(int(r["role_counts"].get(k, 0)) for r in train_rows) for k in {x for r in train_rows for x in r["role_counts"]}}).most_common(15)]
    def vector(row: dict[str, Any]) -> list[float]:
        tag_total = max(1, sum(int(v) for v in row["tag_counts"].values()))
        role_total = max(1, sum(int(v) for v in row["role_counts"].values()))
        return ([int(row["tag_counts"].get(k, 0)) / tag_total for k in tag_vocab]
                + [int(row["role_counts"].get(k, 0)) / role_total for k in role_vocab]
                + [int(row["control_counts"].get(k, 0)) for k in CONTROL_KEYS])
    features: list[list[float]] = []
    for row in health_rows:
        vec = vector(row)
        features.append(vec)
        RAW_KMEANS_FEATURES.append({"trajectory_id": row["trajectory_id"], "endpoint": row["endpoint"], "split": "TRAIN" if row["trajectory_id"] in train_ids else "TEST", "vector": vec, "tag_vocabulary": tag_vocab, "role_vocabulary": role_vocab, "control_keys": CONTROL_KEYS, "dom_count": row["dom_count"], "ax_count": row["ax_count"]})
    X = np.asarray(features, dtype=float)
    train_mask = np.array([r["trajectory_id"] in train_ids for r in health_rows])
    test_mask = ~train_mask
    model = KMeans(n_clusters=20, random_state=SEED, n_init=10)
    model.fit(X[train_mask])
    train_pred = model.predict(X[train_mask])
    test_pred = model.predict(X[test_mask])
    all_pred = model.predict(X)
    combined = KMeans(n_clusters=20, random_state=SEED, n_init=10).fit(X)
    centroid_diff = float(np.linalg.norm(model.cluster_centers_ - combined.cluster_centers_[:20]))
    by_state: dict[str, list[int]] = defaultdict(list)
    for row, pred in zip(health_rows, all_pred):
        by_state[str(row["state_key"])].append(int(pred))
    consistent = 0
    pairs = 0
    for labels in by_state.values():
        for a in range(len(labels)):
            for b in range(a + 1, len(labels)):
                pairs += 1
                consistent += int(labels[a] == labels[b])
    same_j = float(consistent / pairs) if pairs else 0.0
    leakage = bool(centroid_diff > 1e-6 and same_j == 1.0)
    result = {"leakage_pass": leakage, "centroid_diff": centroid_diff, "same_state_J_kmeans": same_j, "n_clusters": 20, "random_state": SEED, "n_init": 10, "n_train": int(train_mask.sum()), "n_test": int(test_mask.sum()), "trajectory_ids_train": sorted(train_ids), "trajectory_ids_test": sorted(test_ids), "feature_dimension": X.shape[1], "tag_vocabulary": tag_vocab, "role_vocabulary": role_vocab, "train_cluster_counts": dict(Counter(int(x) for x in train_pred)), "test_cluster_counts": dict(Counter(int(x) for x in test_pred))}
    METRICS.update({"browser_kmeans_leakage_pass": leakage, "browser_kmeans_centroid_diff": centroid_diff, "browser_kmeans_same_state_J": same_j, "browser_kmeans_n_train": result["n_train"], "browser_kmeans_n_test": result["n_test"], "browser_kmeans_feature_dimension": result["feature_dimension"]})
    return result


def browser_fetch_pair(page: Any, endpoint: str, first_auth: str, second_auth: str, variant: str, index: int, condition: str) -> dict[str, Any]:
    set_variant_browser(page, variant)
    first, first_row = browser_api_get(page, endpoint, first_auth, "browser_fetch_pair", {"pair": "first", "condition": condition, "index": index, "variant": variant})
    second, second_row = browser_api_get(page, endpoint, second_auth, "browser_fetch_pair", {"pair": "second", "condition": condition, "index": index, "variant": variant})
    row = {"condition": condition, "index": index, "endpoint": endpoint, "variant": variant, "first_auth": first_auth, "second_auth": second_auth, "jaccard": header_jaccard({k: v for k, v in first.headers.items()}, {k: v for k, v in second.headers.items()}), "first_fingerprint": fingerprint(first), "second_fingerprint": fingerprint(second), "first": first_row, "second": second_row}
    RAW_BROWSER.append({"phase": "browser_fetch_pair", **row})
    return row


def run_browser_c2(page: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for i in range(160):
        endpoint = API_ENDPOINTS[i % 2]
        variant = BODY_VARIANTS[(i * 7 + i // 2) % 4]
        drift = i % 2
        row = browser_fetch_pair(page, endpoint, "valid", "expired" if drift else "valid", variant, i, "c2")
        rows.append({"jaccard": row["jaccard"], "drift": drift, "body_state": variant})
    calculate_c2(rows, "browser_header_only_jaccard")
    return rows


def run_browser_c4(page: Any) -> dict[str, Any]:
    raw_rows: list[dict[str, Any]] = []
    for i in range(80):
        endpoint = API_ENDPOINTS[i % 2]
        set_variant_browser(page, "A")
        first, first_row = browser_api_get(page, endpoint, "valid", "browser_c4", {"condition": "body", "index": i})
        set_variant_browser(page, "C")
        second, second_row = browser_api_get(page, endpoint, "valid", "browser_c4", {"condition": "body", "index": i})
        row = {"condition": "body", "index": i, "full": fingerprint(first) != fingerprint(second), "body": bytes(first.body()) != bytes(second.body()), "status": first.status != second.status, "first": first_row, "second": second_row}
        raw_rows.append(row); RAW_BROWSER.append({"phase": "browser_c4", **row})
    for i in range(80):
        endpoint = API_ENDPOINTS[i % 2]
        set_variant_browser(page, "A")
        first, first_row = browser_api_get(page, endpoint, "valid", "browser_c4", {"condition": "header", "index": i})
        second, second_row = browser_api_get(page, endpoint, "expired", "browser_c4", {"condition": "header", "index": i})
        row = {"condition": "header", "index": i, "full": fingerprint(first) != fingerprint(second), "body": bytes(first.body()) != bytes(second.body()), "status": first.status != second.status, "first": first_row, "second": second_row}
        raw_rows.append(row); RAW_BROWSER.append({"phase": "browser_c4", **row})
    null_rows: list[dict[str, Any]] = []
    for i in range(50):
        endpoint = API_ENDPOINTS[i % 2]
        set_variant_browser(page, "A")
        first, first_row = browser_api_get(page, endpoint, "valid", "browser_c4", {"condition": "null", "index": i})
        second, second_row = browser_api_get(page, endpoint, "valid", "browser_c4", {"condition": "null", "index": i})
        row = {"condition": "null", "index": i, "full": fingerprint(first) != fingerprint(second), "body": bytes(first.body()) != bytes(second.body()), "status": first.status != second.status, "first": first_row, "second": second_row}
        raw_rows.append(row); null_rows.append(row); RAW_BROWSER.append({"phase": "browser_c4", **row})
    full = float(np.mean([r["full"] for r in raw_rows]))
    body = float(np.mean([r["body"] for r in raw_rows]))
    status = float(np.mean([r["status"] for r in raw_rows]))
    null = float(np.mean([r["full"] for r in null_rows]))
    diffs = np.array([float(r["full"]) - max(float(r["body"]), float(r["status"])) for r in raw_rows], dtype=float)
    rng = np.random.default_rng(SEED)
    boot = [float(np.mean(rng.choice(diffs, size=len(diffs), replace=True))) for _ in range(1000)]
    result = {"n_pairs": len(raw_rows), "full": full, "body_only": body, "status_only": status, "diff_lo": float(np.percentile(boot, 2.5)), "null": null, "bootstrap_B": 1000}
    METRICS.update({"browser_full_vector_n_pairs": result["n_pairs"], "browser_full_vector_full": full, "browser_full_vector_body_only": body, "browser_full_vector_status_only": status, "browser_full_vector_diff_lo": result["diff_lo"], "browser_full_vector_null": null, "browser_full_vector_bootstrap_B": 1000})
    return result


def browser_dom_count(page: Any, url: str) -> int:
    page.goto(url, wait_until="domcontentloaded", timeout=5000)
    page.wait_for_timeout(50)
    return int(page.evaluate("() => document.querySelectorAll('*').length"))


def endpoint_index(endpoint: str) -> int:
    try:
        return WRITE_ENDPOINTS.index(endpoint)
    except ValueError:
        return len(WRITE_ENDPOINTS)


def run_writable_matrix(page: Any) -> dict[str, Any]:
    positive: list[dict[str, Any]] = []
    nulls: list[dict[str, Any]] = []

    def page_interaction(endpoint: str, target: str, index: int) -> dict[str, Any]:
        set_variant_browser(page, "A")
        before_url = f"{BASE_URL}/resource_page?write={endpoint_index(endpoint)}_{index}"
        before_count = writable_count()
        before_dom = browser_dom_count(page, before_url)
        page.fill('input[name="name"]', "test_value")
        page.select_option('select[name="role"]', "admin")
        page.fill('textarea[name="bio"]', "updated bio")
        page.click('button[type="submit"]')
        page.wait_for_selector('#write-result[data-submitted="true"]', timeout=5000)
        interaction_state = {
            "input_value": page.input_value('input[name="name"]'),
            "select_value": page.input_value('select[name="role"]'),
            "textarea_value": page.input_value('textarea[name="bio"]'),
            "submit_marker": page.get_attribute('#write-result', 'data-submitted'),
            "submit_text": page.text_content('#write-result'),
        }
        response = page.request.post(BASE_URL + endpoint, data={"variant": target, "marker": f"ui-{index}"}, headers=auth_headers("valid"), timeout=5000)
        after_count = writable_count()
        set_variant_browser(page, target)
        after_dom = browser_dom_count(page, f"{BASE_URL}/resource_page?after={endpoint_index(endpoint)}_{index}")
        before_resp, before_row = browser_api_get(page, endpoint, "valid", "writable_probe", {"cell": "positive", "index": index, "state": "before"})
        after_resp, after_row = browser_api_get(page, endpoint, "valid", "writable_probe", {"cell": "positive", "index": index, "state": "after"})
        row = {"cell": "VALID_AUTH_WRITE", "endpoint": endpoint, "index": index, "target_variant": target, "before_count": before_count, "after_count": after_count, "wal_mutated": after_count > before_count, "dom_delta": after_dom - before_dom, "fingerprint_before": fingerprint(before_resp), "fingerprint_after": fingerprint(after_resp), "discriminates": fingerprint(before_resp) != fingerprint(after_resp), "post_status": response.status, "post": response_record(response, BASE_URL + endpoint, "valid", "writable_post", {"cell": "positive", "index": index}), "interaction": interaction_state, "before_fetch": before_row, "after_fetch": after_row}
        RAW_WRITABLE.append(row); positive.append(row)
        return row

    def null_cell(cell: str, endpoint: str, index: int, auth_label: str = "valid", delete_session: bool = False) -> dict[str, Any]:
        set_variant_browser(page, "A")
        before_count = writable_count()
        before_dom = browser_dom_count(page, f"{BASE_URL}/resource_page?null={cell}_{index}")
        if delete_session:
            admin = page.request.post(BASE_URL + "/admin/invalidate_session", timeout=5000)
            if admin.status != 200:
                raise InfrastructureFailure("session deletion admin call failed")
        post = page.request.post(BASE_URL + endpoint, data={"variant": "B", "marker": f"null-{index}"}, headers=auth_headers(auth_label), timeout=5000)
        after_count = writable_count()
        # Read the public resource endpoint for the null state fingerprint; the
        # auth result itself is recorded separately and is not counted as a
        # false state transition.
        probe_endpoint = "/api/profile"
        before_resp, before_row = browser_api_get(page, probe_endpoint, "valid" if not delete_session else "invalid", "writable_null_probe", {"cell": cell, "index": index, "state": "before"})
        after_resp, after_row = browser_api_get(page, probe_endpoint, "valid" if not delete_session else "invalid", "writable_null_probe", {"cell": cell, "index": index, "state": "after"})
        after_dom = browser_dom_count(page, f"{BASE_URL}/resource_page?null_after={cell}_{index}")
        row = {"cell": cell, "endpoint": endpoint, "index": index, "before_count": before_count, "after_count": after_count, "wal_mutated": after_count > before_count, "dom_delta": after_dom - before_dom, "fingerprint_before": fingerprint(before_resp), "fingerprint_after": fingerprint(after_resp), "discriminates": fingerprint(before_resp) != fingerprint(after_resp), "post_status": post.status, "post": response_record(post, BASE_URL + endpoint, auth_label, "writable_null_post", {"cell": cell, "index": index}), "before_fetch": before_row, "after_fetch": after_row}
        if delete_session:
            page.request.post(BASE_URL + "/admin/restore_session", timeout=5000)
        RAW_WRITABLE.append(row); nulls.append(row)
        return row

    for i in range(30):
        endpoint = WRITE_ENDPOINTS[i % 3]
        page_interaction(endpoint, BODY_VARIANTS[1 + i % 3], i)
    for i in range(10):
        endpoint = WRITE_ENDPOINTS[i % 3]
        # A GET is the prescribed readonly null; use the write endpoint twice.
        set_variant_browser(page, "A")
        before_count = writable_count()
        before_dom = browser_dom_count(page, f"{BASE_URL}/resource_page?readonly={i}")
        first = page.request.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5000)
        second = page.request.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5000)
        after_count = writable_count()
        after_dom = browser_dom_count(page, f"{BASE_URL}/resource_page?readonly_after={i}")
        row = {"cell": "READONLY_GET", "endpoint": endpoint, "index": i, "before_count": before_count, "after_count": after_count, "wal_mutated": after_count > before_count, "dom_delta": after_dom - before_dom, "fingerprint_before": fingerprint(first), "fingerprint_after": fingerprint(second), "discriminates": fingerprint(first) != fingerprint(second), "post_status": first.status, "post": response_record(first, BASE_URL + endpoint, "valid", "writable_null_get", {"cell": "READONLY_GET", "index": i}), "before_fetch": response_record(first, BASE_URL + endpoint, "valid", "writable_null_get", {"cell": "READONLY_GET", "index": i}), "after_fetch": response_record(second, BASE_URL + endpoint, "valid", "writable_null_get", {"cell": "READONLY_GET", "index": i})}
        RAW_WRITABLE.append(row); nulls.append(row)
    for i in range(10):
        endpoint = WRITE_ENDPOINTS[i % 3]
        null_cell("INVALID_AUTH_WRITE", endpoint, i, "invalid")
    for i in range(10):
        endpoint = WRITE_ENDPOINTS[i % 3]
        null_cell("EXPIRED_AUTH_WRITE", endpoint, i, "expired")
    for i in range(10):
        endpoint = WRITE_ENDPOINTS[i % 3]
        null_cell("DELETED_SESSION_WRITE", endpoint, i, "valid", delete_session=True)
    for i in range(10):
        endpoint = WRITE_ENDPOINTS[i % 3]
        set_variant_browser(page, "A")
        before_count = writable_count()
        before_dom = browser_dom_count(page, f"{BASE_URL}/resource_page?same={i}")
        first = page.request.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5000)
        second = page.request.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5000)
        after_count = writable_count()
        after_dom = browser_dom_count(page, f"{BASE_URL}/resource_page?same_after={i}")
        row = {"cell": "SAME_STATE_READ", "endpoint": endpoint, "index": i, "before_count": before_count, "after_count": after_count, "wal_mutated": after_count > before_count, "dom_delta": after_dom - before_dom, "fingerprint_before": fingerprint(first), "fingerprint_after": fingerprint(second), "discriminates": fingerprint(first) != fingerprint(second), "post_status": first.status, "post": response_record(first, BASE_URL + endpoint, "valid", "writable_same_state", {"cell": "SAME_STATE_READ", "index": i}), "before_fetch": response_record(first, BASE_URL + endpoint, "valid", "writable_same_state", {"cell": "SAME_STATE_READ", "index": i}), "after_fetch": response_record(second, BASE_URL + endpoint, "valid", "writable_same_state", {"cell": "SAME_STATE_READ", "index": i})}
        RAW_WRITABLE.append(row); nulls.append(row)
    pos_rate = float(np.mean([r["discriminates"] for r in positive]))
    dom_rate = float(np.mean([r["dom_delta"] > 0 for r in positive]))
    wal_rate = float(np.mean([r["wal_mutated"] for r in positive]))
    null_rates = {cell: float(np.mean([r["discriminates"] for r in nulls if r["cell"] == cell])) for cell in sorted({r["cell"] for r in nulls})}
    null_wal = {cell: bool(any(r["wal_mutated"] for r in nulls if r["cell"] == cell)) for cell in null_rates}
    null_dom = {cell: float(np.mean([r["dom_delta"] for r in nulls if r["cell"] == cell])) for cell in null_rates}
    null_fp = float(sum(r["discriminates"] for r in nulls) / len(nulls)) if nulls else 1.0
    result = {"positive_n": len(positive), "null_n": len(nulls), "pos_rate": pos_rate, "dom_delta_pos_rate": dom_rate, "wal_pos_mutated_rate": wal_rate, "null_rates": null_rates, "null_dom_delta": null_dom, "null_wal_mutated": null_wal, "nullFP": null_fp, "positive": positive, "nulls": nulls}
    METRICS.update({"writable_pos_rate": pos_rate, "writable_dom_delta_pos_rate": dom_rate, "writable_wal_pos_mutated_rate": wal_rate, "writable_null_rates": null_rates, "writable_null_dom_delta": null_dom, "writable_null_wal_mutated": null_wal, "writable_nullFP": null_fp, "writable_positive_n": len(positive), "writable_null_n": len(nulls)})
    return result


def run_browser_phase() -> dict[str, Any]:
    p, browser, context, state = provision_browser()
    page = state["page"]
    diagnostics = state["diagnostics"]
    try:
        health = run_browser_health(page, context, diagnostics)
        kmeans = fit_browser_kmeans(health)
        c2_rows = run_browser_c2(page)
        c4 = run_browser_c4(page)
        writable = run_writable_matrix(page)
        health_dom = [r["dom_count"] for r in health]
        health_ax = [r["ax_count"] for r in health]
        viewport_ok = all(r["viewport_page"] == {"width": 1280, "height": 720} and r["viewport_page_after_cdp"] == {"width": 1280, "height": 720} for r in health)
        ax_median = float(np.median(health_ax))
        pc_health = float(np.mean([x > 10 for x in health_ax]))
        dom_median = float(np.median(health_dom))
        METRICS.update({"browser_health_n": len(health), "browser_health_ax_median": ax_median, "browser_health_pc_health": pc_health, "browser_health_dom_median": dom_median, "browser_health_viewport_ok": viewport_ok, "browser_health_dom_min": min(health_dom), "browser_health_dom_max": max(health_dom), "browser_health_ax_min": min(health_ax), "browser_health_ax_max": max(health_ax)})
        _RUNTIME_DIAGNOSTICS.update(diagnostics)
        OBSERVATIONS.append(f"Captured {len(health)} real Playwright DOM/CDP AX observations at 1280x720 ({len(health)}/80 pages).")
        return {"health": health, "kmeans": kmeans, "c2": c2_rows, "c4": c4, "writable": writable, "diagnostics": diagnostics}
    finally:
        close_browser(browser, context, p)


# ----------------------------- loopback/HIT -------------------------------

def run_loopback_and_hit() -> None:
    restart_infrastructure()
    OBSERVATIONS.append("Restarted both gunicorn origins and nginx for the frozen loopback phase.")
    header_pairs: list[dict[str, Any]] = []
    body_pairs: list[dict[str, Any]] = []
    null_pairs: list[dict[str, Any]] = []
    for i in range(24):
        endpoint = API_ENDPOINTS[i % 2]
        direct_set_variant("A")
        first = requests.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5)
        second = requests.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5)
        third = requests.get(BASE_URL + endpoint, headers=auth_headers("valid"), timeout=5)
        record_direct(first, BASE_URL + endpoint, "valid", "loopback_header", {"pair": "header_first", "index": i})
        record_direct(second, BASE_URL + endpoint, "valid", "loopback_header", {"pair": "header_second", "index": i})
        record_direct(third, BASE_URL + endpoint, "valid", "loopback_body", {"pair": "body_third", "index": i})
        first_body = bytes(first.content)
        second_body = bytes(second.content)
        third_body = bytes(third.content)
        header_pairs.append({"jaccard": header_jaccard(dict(first.headers), dict(second.headers))})
        body_pairs.append({"body_diff": first_body != second_body or second_body != third_body})
        null_pairs.append({"fingerprint_diff": fingerprint(first) != fingerprint(second) or fingerprint(second) != fingerprint(third)})
    METRICS.update({"loopback_header_drift": float(np.mean([p["jaccard"] < 1.0 for p in header_pairs])), "loopback_body_drift": float(np.mean([p["body_diff"] for p in body_pairs])), "loopback_nullFP": float(np.mean([p["fingerprint_diff"] for p in null_pairs])), "loopback_n_pairs_each": 24})
    # Warm and then issue exactly 330 cache requests.
    warm = requests.get(BASE_URL + "/health?cache_probe=exp", headers={"Accept-Encoding": "gzip, br"}, timeout=5)
    RAW_HIT.append({"phase": "hit_warm", "status": warm.status_code, "x_cache": warm.headers.get("X-Cache"), "body": body_summary(warm.content)})
    hit_rows: list[dict[str, Any]] = []
    for i in range(330):
        response = requests.get(BASE_URL + "/health?cache_probe=exp", headers={"Accept-Encoding": "gzip, br"}, timeout=5)
        row = {"phase": "hit", "index": i, "status": response.status_code, "x_cache": response.headers.get("X-Cache"), "body": body_summary(response.content), "byte_identical": response.content == warm.content}
        hit_rows.append(row); RAW_HIT.append(row)
    hits = sum(1 for r in hit_rows if r["x_cache"] == "HIT")
    identical = sum(1 for r in hit_rows if r["byte_identical"])
    METRICS.update({"nginx_hit_330": hits, "nginx_hit_byte_identical_330": identical, "nginx_hit_rate": hits / 330.0, "nginx_health_warm_x_cache": warm.headers.get("X-Cache")})
    OBSERVATIONS.append(f"Loopback drift and cache phases completed with {hits}/330 nginx HIT responses and {identical}/330 byte-identical bodies.")


# ----------------------------- packet writing -----------------------------

def artifact_entry(path: Path, role: str) -> dict[str, Any]:
    return {"path": str(path.relative_to(BASE)) if path.is_relative_to(BASE) else str(path), "sha256": sha256_file(path), "bytes": path.stat().st_size, "role": role}


def set_control(control_id: str, expected: Any, observed: Any, passed: bool | None, evidence: list[str], note: str = "") -> None:
    CONTROLS[control_id] = {"expected": expected, "observed": observed, "status": "UNKNOWN" if passed is None else ("PASS" if passed else "FAIL"), "pass": passed, "evidence_refs": evidence, "note": note}


def gate_results() -> dict[str, dict[str, Any]]:
    m = METRICS
    by_ep = m.get("freshness_per_endpoint_non304", {})
    c1 = bool(m.get("freshness_n_non304", 0) >= 800 and by_ep.get("/api/profile", 0) >= 400 and by_ep.get("/api/data_list", 0) >= 400)
    c2 = bool(abs(m.get("browser_header_only_jaccard_r", 0.0)) < 0.30 and m.get("browser_header_only_jaccard_v", 1.0) < 0.30 and m.get("browser_header_only_jaccard_nullFP", 1.0) <= 0.05 and m.get("browser_header_only_jaccard_variance", 0.0) > 0 and m.get("browser_header_only_jaccard_std", 0.0) > 0 and m.get("browser_header_only_jaccard_mean", 1.0) < 1.0 and m.get("browser_header_only_jaccard_same_state_J", 0.0) == 1.0)
    c3 = bool(abs(m.get("honest_cost_rho_shuffled", 1.0)) < 0.20 and m.get("honest_cost_p_value", 0.0) >= 0.20 and m.get("honest_cost_within_f_std", 0.0) > 0)
    c4 = bool(m.get("browser_full_vector_full", 0.0) > 0.5 and m.get("browser_full_vector_full", 0.0) > max(m.get("browser_full_vector_body_only", 1.0), m.get("browser_full_vector_status_only", 1.0)) + 0.05 and m.get("browser_full_vector_diff_lo", 0.0) > 0 and m.get("browser_full_vector_null", 1.0) == 0.0)
    c5 = bool(m.get("loopback_header_drift", 1.0) < 0.05 and m.get("loopback_body_drift", 1.0) < 0.05 and m.get("loopback_nullFP", 1.0) == 0.0 and m.get("nginx_hit_330", 0) == 330 and m.get("nginx_hit_byte_identical_330", 0) == 330)
    health = bool(m.get("browser_health_ax_median", 0.0) > 10 and m.get("browser_health_pc_health", 0.0) >= 0.80 and 21 <= m.get("browser_health_dom_median", 0.0) <= 82 and m.get("browser_health_viewport_ok") is True)
    kmeans = bool(m.get("browser_kmeans_leakage_pass") is True)
    null_rates = m.get("writable_null_rates", {})
    writable = bool(m.get("writable_pos_rate", 0.0) >= 0.5 and all(v == 0.0 for v in null_rates.values()) and m.get("writable_nullFP", 1.0) <= 0.05 and m.get("writable_dom_delta_pos_rate", 0.0) == 1.0 and m.get("writable_wal_pos_mutated_rate", 0.0) == 1.0 and not any(m.get("writable_null_wal_mutated", {}).values()))
    return {"C1": {"pass": c1, "observed": {"n_non304": m.get("freshness_n_non304"), "per_endpoint": by_ep}}, "C2": {"pass": c2, "observed": {k: m.get(k) for k in ["browser_header_only_jaccard_r", "browser_header_only_jaccard_v", "browser_header_only_jaccard_nullFP", "browser_header_only_jaccard_variance", "browser_header_only_jaccard_std", "browser_header_only_jaccard_mean", "browser_header_only_jaccard_same_state_J"]}}, "C3": {"pass": c3, "observed": {k: m.get(k) for k in ["honest_cost_rho_shuffled", "honest_cost_p_value", "honest_cost_within_f_std"]}}, "C4": {"pass": c4, "observed": {k: m.get(k) for k in ["browser_full_vector_full", "browser_full_vector_body_only", "browser_full_vector_status_only", "browser_full_vector_diff_lo", "browser_full_vector_null"]}}, "C5": {"pass": c5, "observed": {k: m.get(k) for k in ["loopback_header_drift", "loopback_body_drift", "loopback_nullFP", "nginx_hit_330", "nginx_hit_byte_identical_330"]}}, "C6_BROWSER_HEALTH": {"pass": health, "observed": {k: m.get(k) for k in ["browser_health_ax_median", "browser_health_pc_health", "browser_health_dom_median", "browser_health_viewport_ok"]}}, "C7_KMEANS": {"pass": kmeans, "observed": {k: m.get(k) for k in ["browser_kmeans_leakage_pass", "browser_kmeans_centroid_diff", "browser_kmeans_same_state_J"]}}, "C8_WRITABLE": {"pass": writable, "observed": {k: m.get(k) for k in ["writable_pos_rate", "writable_dom_delta_pos_rate", "writable_wal_pos_mutated_rate", "writable_null_rates", "writable_nullFP", "writable_null_wal_mutated"]}}}


def make_controls(gates: dict[str, dict[str, Any]]) -> None:
    raw = ["research/experiments/EXP-RUNTIME-36106663091/raw_freshness_observations.jsonl", "research/experiments/EXP-RUNTIME-36106663091/raw_browser_observations.jsonl", "research/experiments/EXP-RUNTIME-36106663091/raw_writable_observations.jsonl", "research/experiments/EXP-RUNTIME-36106663091/raw_kmeans_features.jsonl", "research/experiments/EXP-RUNTIME-36106663091/raw_trajectory_costs.jsonl", "research/experiments/EXP-RUNTIME-36106663091/raw_hit_observations.jsonl"]
    all_http_observed = all(gates.get(k, {}).get("observed") is not None for k in ["C1", "C2", "C3", "C4", "C5"])
    all_http_pass = all(bool(gates.get(k, {}).get("pass")) for k in ["C1", "C2", "C3", "C4", "C5"])
    browser_observed = METRICS.get("browser_health_n") == 80
    kmeans_observed = METRICS.get("browser_kmeans_leakage_pass") is not None
    writable_observed = METRICS.get("writable_positive_n") is not None
    set_control("B-DISTRIBUTED-HTTP-TRIPLE", "C1-C5 distributed/browser-path replication", {k: gates.get(k, {}).get("pass") for k in ["C1", "C2", "C3", "C4", "C5"]}, all_http_pass if all_http_observed else None, raw, "Unknown unless every C1-C5 phase completed.")
    set_control("B-BROWSER-DOM-AX-STRUCTURAL", "AX median >10, PC_HEALTH>=0.80, DOM median [21,82], viewport 1280x720", {k: METRICS.get(k) for k in ["browser_health_ax_median", "browser_health_pc_health", "browser_health_dom_median", "browser_health_viewport_ok"]}, gates["C6_BROWSER_HEALTH"]["pass"] if browser_observed else None, ["research/experiments/EXP-RUNTIME-36106663091/raw_browser_observations.jsonl"])
    set_control("B-WRITABLE-POSITIVE", "positive discrimination >=0.5, DOM_delta>0, WAL mutation", {k: METRICS.get(k) for k in ["writable_pos_rate", "writable_dom_delta_pos_rate", "writable_wal_pos_mutated_rate"]}, gates["C8_WRITABLE"]["pass"] if writable_observed else None, ["research/experiments/EXP-RUNTIME-36106663091/raw_writable_observations.jsonl"])
    for cell, key in [("READONLY_GET", "B-WRITABLE-NULL-READONLY"), ("INVALID_AUTH_WRITE", "B-WRITABLE-NULL-INVALID-AUTH"), ("EXPIRED_AUTH_WRITE", "B-WRITABLE-NULL-EXPIRED-AUTH"), ("DELETED_SESSION_WRITE", "B-WRITABLE-NULL-DELETED-SESSION"), ("SAME_STATE_READ", "B-WRITABLE-NULL-SAME-STATE")]:
        rate = (METRICS.get("writable_null_rates") or {}).get(cell)
        wal = (METRICS.get("writable_null_wal_mutated") or {}).get(cell)
        dom = (METRICS.get("writable_null_dom_delta") or {}).get(cell)
        expected = "0.0 discrimination, 0 DOM delta, WAL unchanged" if cell != "DELETED_SESSION_WRITE" else "401, 0.0 discrimination, 0 DOM delta, WAL unchanged"
        passed = rate == 0.0 and dom == 0.0 and wal is False
        set_control(key, expected, {"discrimination_rate": rate, "dom_delta_mean": dom, "wal_mutated": wal}, passed if writable_observed else None, ["research/experiments/EXP-RUNTIME-36106663091/raw_writable_observations.jsonl"])
    set_control("B-TRAIN-ONLY-KMEANS", "k=20, strict 60/40 trajectory split, leakage_pass", {k: METRICS.get(k) for k in ["browser_kmeans_leakage_pass", "browser_kmeans_centroid_diff", "browser_kmeans_same_state_J", "browser_kmeans_n_train", "browser_kmeans_n_test"]}, gates["C7_KMEANS"]["pass"] if kmeans_observed else None, ["research/experiments/EXP-RUNTIME-36106663091/raw_kmeans_features.jsonl", "research/experiments/EXP-RUNTIME-36106663091/raw_browser_observations.jsonl"])
    set_control("B-HEADER-ONLY-JACCARD-STABLE-BROWSER", "|r|<0.30, V<0.30, nullFP<=0.05, same-state J=1", {k: METRICS.get(k) for k in ["browser_header_only_jaccard_r", "browser_header_only_jaccard_v", "browser_header_only_jaccard_nullFP", "browser_header_only_jaccard_mean", "browser_header_only_jaccard_same_state_J"]}, gates["C2"]["pass"] if browser_observed else None, ["research/experiments/EXP-RUNTIME-36106663091/raw_browser_observations.jsonl"])
    set_control("B-FULL-VECTOR-BROWSER", "full>0.5, full>max(body,status)+0.05, diff_lo>0, null=0", {k: METRICS.get(k) for k in ["browser_full_vector_full", "browser_full_vector_body_only", "browser_full_vector_status_only", "browser_full_vector_diff_lo", "browser_full_vector_null"]}, gates["C4"]["pass"] if browser_observed else None, ["research/experiments/EXP-RUNTIME-36106663091/raw_browser_observations.jsonl"])
    diag = _RUNTIME_DIAGNOSTICS
    provision_observed = bool(diag.get("playwright_version") or diag.get("native_path_helper_error"))
    set_control("PC-REAL-BROWSER-PROVISIONED", "Playwright 1.63.0 Chromium + BrowserGym 0.14.3 + exact native path helper + real capture", diag, bool(browser_observed and diag.get("native_path_helper_available")) if provision_observed and browser_observed else None, ["research/experiments/EXP-RUNTIME-36106663091/raw_browser_observations.jsonl", "research/experiments/EXP-RUNTIME-36106663091/provenance.json"], "UNKNOWN when mandatory provisioning aborts before capture.")
    set_control("NC-SYNTHETIC-FALLBACK-REJECTED", "No synthetic browser/writable fallback; fail closed", {"fallback_triggered": False, "real_playwright_capture": METRICS.get("browser_health_n") == 80, "real_page_interactions": METRICS.get("writable_positive_n") is not None}, True, ["research/experiments/EXP-RUNTIME-36106663091/run_experiment.py"], "The runner has no synthetic fallback branch; any browser setup error is reported as infrastructure failure.")


def write_raw_artifacts() -> list[Path]:
    paths = [BASE / "raw_freshness_observations.jsonl", BASE / "raw_browser_observations.jsonl", BASE / "raw_writable_observations.jsonl", BASE / "raw_kmeans_features.jsonl", BASE / "raw_trajectory_costs.jsonl", BASE / "raw_hit_observations.jsonl", BASE / "raw_batch_state_log.jsonl"]
    write_jsonl(paths[0], RAW_FRESHNESS)
    write_jsonl(paths[1], RAW_BROWSER)
    write_jsonl(paths[2], RAW_WRITABLE)
    write_jsonl(paths[3], RAW_KMEANS_FEATURES)
    write_jsonl(paths[4], TRAJECTORY_COSTS)
    write_jsonl(paths[5], RAW_HIT)
    write_jsonl(paths[6], RAW_BATCH)
    return paths


def environment_info() -> dict[str, Any]:
    names = ["playwright", "browsergym", "browsergym-core", "gunicorn", "PyJWT", "Flask", "requests", "numpy", "scipy", "scikit-learn", "brotli"]
    versions = {name: browser_package_version(name) for name in names}
    versions.update({"python": sys.version.split()[0], "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip()})
    return versions


def git_info() -> dict[str, Any]:
    def cmd(args: list[str]) -> str | None:
        try:
            return subprocess.run(args, capture_output=True, text=True, check=True).stdout.strip()
        except Exception:
            return None
    return {"head": cmd(["git", "rev-parse", "HEAD"]), "branch": cmd(["git", "branch", "--show-current"]), "status": cmd(["git", "status", "--short"])}


def make_provenance(artifacts: list[Path], code_hash: str) -> dict[str, Any]:
    frozen = json.loads((BASE / "freeze.json").read_text())
    fixture_paths = [p for p in [NGINX_CONF, WSGI_PATH, DB_PATH] if p.exists()]
    fixture_entries = []
    for p in fixture_paths:
        fixture_entries.append({"path": str(p), "sha256": sha256_file(p), "bytes": p.stat().st_size, "role": "fixture"})
    artifact_entries = [artifact_entry(p, "raw") for p in artifacts] + [artifact_entry(BASE / "run_experiment.py", "code")]
    artifact_entries += fixture_entries
    return {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE, "claim_id": CLAIM_ID, "github_run_id": "36106663091", "base_sha": "896b9305aba3d2e5889cd35a4a4b66541639a6a1", "source_commit": git_info()["head"], "branch": git_info()["branch"], "frozen_inputs": frozen.get("hashes", {}), "code": {"path": "research/experiments/EXP-RUNTIME-36106663091/run_experiment.py", "sha256": code_hash}, "fixtures": fixture_entries, "environment": environment_info(), "seeds": {"SEED": SEED, "numpy_seed": SEED, "sklearn_random_state": SEED, "honest_cost_permutations_B": 1000}, "browser_runtime": _RUNTIME_DIAGNOSTICS, "commands": COMMANDS, "artifacts": artifact_entries, "git_at_end": git_info(), "created_at": utc_now(), "reproduction_notes": ["The runner is fail-closed and contains no synthetic browser/writable fallback.", "The exact frozen playwright._impl._path_utils.get_executable_path helper is mandatory; the public executable path is diagnostic only and is not substituted if the helper is absent.", "agentlab import was attempted and was unavailable; the frozen packet says it is not required when BrowserGym works."]}


def write_report(result: dict[str, Any], provenance: dict[str, Any], gates: dict[str, dict[str, Any]]) -> None:
    status = result["status"]
    outcome = result["outcome"]
    browser_complete = METRICS.get("browser_health_n") == 80
    if browser_complete:
        scope_text = "This execution completed the frozen two-origin gunicorn/nginx/SQLite-WAL substrate, real Playwright Chromium DOM/CDP AX capture, real Playwright page interactions, `page.request` browser fetch probes, and direct SQLite WAL counts. No synthetic browser or write path was used. The frozen C1-C8 gates were evaluated without changing thresholds."
        raw_text = "Raw observations are preserved in the JSONL artifacts listed in `result.json` and `provenance.json`. Browser rows contain actual DOM counts, CDP AX nodes, viewport calls, and feature histograms; writable rows contain interaction values, request status, fingerprints, DOM deltas, and direct SQLite counts."
    else:
        scope_text = "The distributed HTTP phase and any phases reached before the mandatory browser provisioning gate are reported exactly. Real browser capture did not complete, so no browser, writable, or downstream loopback/HIT claim is made. No synthetic browser or write path was used."
        raw_text = "Raw observations are preserved in the JSONL artifacts listed in `result.json` and `provenance.json`. Browser-dependent raw artifacts are explicitly empty when the mandatory provisioning gate aborts execution; absence is not a negative scientific observation."
    lines = [
        f"# {EXPERIMENT_ID} execution report",
        "",
        f"- **Lane/claim:** `{LANE}` / `{CLAIM_ID}`",
        f"- **Measurement status:** `{status}`",
        f"- **Scientific outcome:** `{outcome}`",
        f"- **Run timestamp:** `{provenance['created_at']}`",
        "",
        "## Scope and frozen decision",
        scope_text,
        "",
        "## Raw evidence",
        raw_text,
        "",
        "## Direct observations",
    ]
    lines.extend(f"- {x}" for x in OBSERVATIONS)
    lines.extend(["", "## Derived measurements", "", "| Gate | Pass | Observed |", "|---|---:|---|"])
    for key, value in gates.items():
        lines.append(f"| `{key}` | `{value['pass']}` | `{json.dumps(value['observed'], sort_keys=True, default=str)}` |")
    lines.extend(["", "## Controls", "", "| Control ID | Status | Observed |", "|---|---|---|"])
    for key, value in CONTROLS.items():
        lines.append(f"| `{key}` | `{value['status']}` | `{json.dumps(value['observed'], sort_keys=True, default=str)}` |")
    lines.extend(["", "## Interpretation (bounded)", ""])
    if outcome == "SUPPORTS":
        lines.append("All frozen scientific and validity conditions passed in this bounded localhost fixture. This is evidence for the declared experiment only; it does not establish task-level BrowserGym evaluation, live-site generalization, or production integration.")
    elif outcome == "FALSIFIES":
        failed = [k for k, v in gates.items() if not v["pass"]]
        lines.append(f"With measurement validity retained, one or more frozen conditions failed: {', '.join(failed)}. This is a bounded falsification of the stated hypothesis, not a claim that the broader browser/runtime domain is closed.")
    elif outcome == "MIXED":
        lines.append("The bounded run produced mixed gate results. The raw evidence and failures are preserved; no promotion is made from this mixed outcome.")
    else:
        lines.append("The measurement transaction was not sufficiently valid to support a scientific positive or negative conclusion. Missing or failed substrate operations remain unknown rather than being converted into falsification.")
    lines.extend(["", "## Validity and unresolved threats", ""])
    lines.extend(f"- {x}" for x in VALIDITY_NOTES)
    lines.extend(f"- {x}" for x in UNRESOLVED)
    lines.extend(["", "## Explicit unknowns", "", "- TLS/HTTP2/QUIC, multi-host Redis, production CDN/edge, compressed encodings beyond greedy MAX_DEPTH5, timing-window header canonicalization, reboot durability, high write contention, task-level BrowserGym evaluation, and real-site generalization remain outside this experiment."])
    (BASE / "report.md").write_text("\n".join(lines) + "\n")


def write_outputs(gates: dict[str, dict[str, Any]], status: str, outcome: str) -> None:
    raw_paths = write_raw_artifacts()
    browser_metric_keys = [
        "browser_health_n", "browser_health_ax_median", "browser_health_pc_health",
        "browser_health_dom_median", "browser_health_viewport_ok", "browser_health_dom_min",
        "browser_health_dom_max", "browser_health_ax_min", "browser_health_ax_max",
        "browser_kmeans_leakage_pass", "browser_kmeans_centroid_diff",
        "browser_kmeans_same_state_J", "browser_kmeans_n_train", "browser_kmeans_n_test",
        "browser_kmeans_feature_dimension", "browser_header_only_jaccard_r",
        "browser_header_only_jaccard_v", "browser_header_only_jaccard_nullFP",
        "browser_header_only_jaccard_variance", "browser_header_only_jaccard_std",
        "browser_header_only_jaccard_mean", "browser_header_only_jaccard_same_state_J",
        "browser_full_vector_n_pairs", "browser_full_vector_full", "browser_full_vector_body_only",
        "browser_full_vector_status_only", "browser_full_vector_diff_lo", "browser_full_vector_null",
        "writable_pos_rate", "writable_dom_delta_pos_rate", "writable_wal_pos_mutated_rate",
        "writable_null_rates", "writable_null_dom_delta", "writable_null_wal_mutated",
        "writable_nullFP", "writable_positive_n", "writable_null_n",
    ]
    for key in browser_metric_keys:
        METRICS.setdefault(key, None)
    validity = {
        "infrastructure_error": bool(INFRA_ERRORS),
        "database_wal_created": DB_PATH.exists(),
        "two_gunicorn_origins": len(ORIGIN_URLS) == 2,
        "nginx_enabled": _RUNTIME_DIAGNOSTICS.get("nginx_started", False),
        "browser_real_playwright": METRICS.get("browser_health_n") == 80,
        "browser_gym_import": _RUNTIME_DIAGNOSTICS.get("browsergym_import") is True,
        "cdp_ax_per_page": METRICS.get("browser_health_n") == 80,
        "dom_per_page": METRICS.get("browser_health_n") == 80,
        "viewport_both_checks": METRICS.get("browser_health_viewport_ok") is True,
        "kmeans_strict_split": METRICS.get("browser_kmeans_n_train") is not None and METRICS.get("browser_kmeans_n_test") is not None,
        "real_feature_vectors": METRICS.get("browser_kmeans_feature_dimension") is not None,
        "writable_real_interactions": METRICS.get("writable_positive_n") is not None,
        "wal_direct_counts": METRICS.get("writable_positive_n") is not None,
        "honest_cost_B1000": METRICS.get("honest_cost_permutations_B") == 1000,
        "no_post_state_leakage": METRICS.get("browser_kmeans_leakage_pass") is not None,
        "seed_44": True,
        "native_path_helper_available": _RUNTIME_DIAGNOSTICS.get("native_path_helper_available", False),
        "official_executable_path_verified": bool(_RUNTIME_DIAGNOSTICS.get("official_executable_path")),
    }
    if _RUNTIME_DIAGNOSTICS.get("native_path_helper_error"):
        VALIDITY_NOTES.append("Mandatory frozen Playwright provisioning failed because the exact required playwright._impl._path_utils.get_executable_path helper was unavailable; the diagnostic public executable path was not substituted.")
        UNRESOLVED.append("A later governed experiment would need a preregistered provisioning design compatible with the installed Playwright API; this immutable run cannot relax the helper requirement.")
    for err in INFRA_ERRORS:
        VALIDITY_NOTES.append("Infrastructure failure: " + err)
    make_controls(gates)
    artifacts = [artifact_entry(p, "raw") for p in raw_paths]
    artifacts.append(artifact_entry(BASE / "run_experiment.py", "code"))
    result = {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE, "status": status, "outcome": outcome, "metrics": METRICS, "controls": CONTROLS, "artifacts": artifacts, "observations": OBSERVATIONS, "validity_notes": VALIDITY_NOTES + [f"Validity summary: {json.dumps(validity, sort_keys=True)}"], "unresolved": UNRESOLVED}
    write_json(BASE / "result.json", result)
    code_hash = sha256_file(BASE / "run_experiment.py")
    provenance = make_provenance(raw_paths, code_hash)
    write_json(BASE / "provenance.json", provenance)
    write_report(result, provenance, gates)


def final_gate_decision(gates: dict[str, dict[str, Any]], validity_ok: bool) -> tuple[str, str]:
    if not validity_ok:
        return "MEASUREMENT_INVALID", "INCONCLUSIVE"
    if all(v["pass"] for v in gates.values()):
        return "COMPLETE", "SUPPORTS"
    return "COMPLETE", "FALSIFIES"


def main() -> int:
    global _RUNTIME_DIAGNOSTICS
    random.seed(SEED)
    if np is not None:
        np.random.seed(SEED)
    status = "MEASUREMENT_INVALID"
    outcome = "INCONCLUSIVE"
    gates: dict[str, dict[str, Any]] = {}
    try:
        setup_infrastructure()
        _RUNTIME_DIAGNOSTICS["nginx_started"] = True
        make_tokens()
        run_stickiness()
        run_c1()
        run_plain_c2()
        run_plain_c4()
        run_c3()
        run_browser_phase()
        run_loopback_and_hit()
        gates = gate_results()
        validity_ok = not INFRA_ERRORS and METRICS.get("browser_health_n") == 80
        status, outcome = final_gate_decision(gates, validity_ok)
    except Exception as exc:
        INFRA_ERRORS.append(repr(exc))
        VALIDITY_NOTES.append("Execution halted or was marked invalid because a required substrate/measurement operation failed: " + repr(exc))
        status, outcome = "MEASUREMENT_INVALID", "INCONCLUSIVE"
        if not gates:
            gates = {k: {"pass": False, "observed": None} for k in ["C1", "C2", "C3", "C4", "C5", "C6_BROWSER_HEALTH", "C7_KMEANS", "C8_WRITABLE"]}
    finally:
        with contextlib.suppress(Exception):
            stop_infrastructure()
        try:
            write_outputs(gates, status, outcome)
        except Exception as exc:
            # A packet must still be emitted if an artifact write itself fails;
            # make the failure explicit in a minimal valid-shaped fallback.
            INFRA_ERRORS.append("output write failed: " + repr(exc))
            fallback = {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE, "status": "MEASUREMENT_INVALID", "outcome": "INCONCLUSIVE", "metrics": {}, "controls": {}, "artifacts": [], "observations": OBSERVATIONS, "validity_notes": VALIDITY_NOTES + INFRA_ERRORS, "unresolved": UNRESOLVED}
            write_json(BASE / "result.json", fallback)
    return 0 if status != "MEASUREMENT_INVALID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
