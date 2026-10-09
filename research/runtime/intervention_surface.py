#!/usr/bin/env python3
"""
SPIDER Research 2.0 — runtime lane INTERVENTION SURFACE (ground-truth provider).

This module owns, and only owns, the intervention surface and its auth/session
boundary for EXP-RUNTIME-36293257855:

  * the Flask app factory `create_app()`;
  * the WAL schema and the controlled `runtime_probe` row;
  * the stable-header API fixture (`/api/profile`, `/api/data_list`);
  * fixture plumbing (`/admin/session`, `/admin/reset_probe`, `/admin/set_body_variant`);
  * the controlled intervention routes (`/runtime/read`, `/runtime/write`,
    `/runtime/set_representation`, `/runtime/restore`);
  * the real rendered SPA episode pages whose button clicks are the only write
    mechanism exercised by the transport.

Authorship separation (spec `measurement_validity.authorship_separation`,
prereg section 6.1): this module must NOT import `oracle_scorer` or any
detector code. It may import the constants-only `shared_config` module.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import jwt
from flask import Flask, g, jsonify, request as flask_request

from research.runtime import shared_config as SC

# Fresh testbed signing secret for this run. Only its SHA-256 and byte length
# are recorded in provenance; the value is a local testbed secret, never a
# capability or a credential.
TESTBED_SECRET = ("9c1d7f3a5b8e0c2d4f6a8b0c2e4d6f8a0b2c4e6d8f0a2c4e6b8d0f2a4c6e8"
                  "b0d2f4a6c8e0b2d4f6a8c0e2b4d6f8a0c2e4b6d8f0a2c4e6b8d0f2a4c6e8b0d2f4a6c8")
assert len(TESTBED_SECRET.encode()) >= 32
HS256_SECRET_HASH = hashlib.sha256(TESTBED_SECRET.encode()).hexdigest()
HS256_SECRET_LEN = len(TESTBED_SECRET.encode())


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_valid_token(sid: str, ttl_hours: float = 1.0) -> str:
    return jwt.encode({"sub": sid, "exp": datetime.now(timezone.utc) + timedelta(hours=ttl_hours)},
                      TESTBED_SECRET, algorithm="HS256")


def make_expired_token(sid: str) -> str:
    return jwt.encode({"sub": sid, "exp": datetime.now(timezone.utc) - timedelta(hours=1)},
                      TESTBED_SECRET, algorithm="HS256")


EPISODE_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Runtime Episode</title></head>
<body>
<h1>Runtime Browser Episode</h1>
<div id="state">idle #0</div>
<div id="last-response">{}</div>
<button data-testid="write-btn" id="btn-write" onclick="__doWrite()">Write</button>
<button data-testid="restore-btn" id="btn-restore" onclick="__doRestore()">Restore</button>
<script>
window._ctr = 0;
window.__READ_TOKEN__ = "__READ_TOKEN_VALUE__";
window.__ACTION__ = __ACTION_JSON__;
async function __readState() {
  const r = await fetch("/runtime/read", { headers: { "Authorization": "Bearer " + window.__READ_TOKEN__ } });
  const t = await r.text();
  const h = {};
  r.headers.forEach(function(v, k) { h[k] = v; });
  return { status: r.status, body: t, headers: h };
}
async function __doWrite() {
  const a = window.__ACTION__;
  const r = await fetch(a.path, { method: "POST",
    headers: { "Authorization": "Bearer " + a.token, "Content-Type": "application/json" },
    body: JSON.stringify({ op: a.op, value: a.value }) });
  const t = await r.text();
  document.getElementById("state").innerText = a.label + ": " + r.status + " #" + (++window._ctr);
  document.getElementById("last-response").innerText = t;
  return { status: r.status, body: t };
}
async function __doRestore() {
  const r = await fetch("/runtime/restore", { method: "POST",
    headers: { "Authorization": "Bearer " + window.__READ_TOKEN__, "Content-Type": "application/json" },
    body: "{}" });
  const t = await r.text();
  document.getElementById("state").innerText = "restore: " + r.status + " #" + (++window._ctr);
  document.getElementById("last-response").innerText = t;
  return { status: r.status, body: t };
}
</script>
</body></html>"""

READONLY_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Runtime Read-Only</title></head>
<body>
<h1>Runtime Read-Only Surface</h1>
<div id="state">idle #0</div>
<div id="last-response">{}</div>
<script>
window._ctr = 0;
window.__READ_TOKEN__ = "__READ_TOKEN_VALUE__";
async function __readState() {
  const r = await fetch("/runtime/read", { headers: { "Authorization": "Bearer " + window.__READ_TOKEN__ } });
  const t = await r.text();
  const h = {};
  r.headers.forEach(function(v, k) { h[k] = v; });
  return { status: r.status, body: t, headers: h };
}
window.addEventListener("load", async function() {
  const s = await __readState();
  document.getElementById("state").innerText = "read: " + s.status + " #" + (++window._ctr);
  document.getElementById("last-response").innerText = s.body;
});
</script>
</body></html>"""


def create_app(db_path: str = SC.DB_PATH) -> Flask:
    app = Flask(__name__)
    app.config["DATABASE"] = db_path

    def _connect() -> sqlite3.Connection:
        conn = sqlite3.connect(db_path, timeout=10, check_same_thread=False)
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA journal_mode=WAL")
        # Frozen substrate contract: no checkpoint/compaction during the
        # measured window on ANY connection.
        conn.execute("PRAGMA wal_autocheckpoint=0")
        conn.row_factory = sqlite3.Row
        return conn

    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop("db", None)
        if db:
            db.close()

    def init_db():
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        last_err = None
        for _ in range(20):
            try:
                conn = _connect()
                conn.execute(SC.SCHEMA["sessions"])
                conn.execute(SC.SCHEMA["body_config"])
                conn.execute(SC.SCHEMA["runtime_probe"])
                conn.execute("INSERT OR IGNORE INTO body_config VALUES (1,'A',?)",
                             (SC.BODY_STATES["A"]["json"],))
                conn.execute("INSERT OR IGNORE INTO runtime_probe VALUES (1,?,?,?,?)",
                             (SC.PRE_MARKER, SC.PRE_REPRESENTATION, SC.PRE_REVISION, SC.PRE_UPDATED_AT))
                conn.commit()
                conn.close()
                return
            except sqlite3.OperationalError as e:
                last_err = e
                try:
                    conn.close()
                except Exception:
                    pass
                time.sleep(0.1)
        raise RuntimeError(f"init_db failed after retries: {last_err}")

    init_db()

    @app.route("/health")
    def health():
        body = b'{"status":"ok"}'
        return body, 200, {"Content-Type": "application/json",
                           "Content-Length": str(len(body)), "X-Worker-Pid": str(os.getpid())}

    def _auth_valid(auth_header: str) -> bool:
        if not auth_header.startswith("Bearer "):
            return False
        try:
            jwt.decode(auth_header[7:], TESTBED_SECRET, algorithms=["HS256"])
            return True
        except Exception:
            return False

    def _handle_api():
        # Certified stable-header contract from the validated fixture.
        auth_header = flask_request.headers.get("Authorization", "")
        if _auth_valid(auth_header):
            cc_val, vary_val = "public, max-age=5", "Cookie"
        else:
            cc_val, vary_val = "no-store", "Authorization"
        conn = _connect()
        row = conn.execute("SELECT variant, content FROM body_config WHERE id=1").fetchone()
        conn.close()
        body_json = (row["content"] if row else "{}").encode()
        headers = {
            "Content-Type": "application/json",
            "Content-Length": str(len(body_json)),
            "ETag": 'W/"%s"' % hashlib.sha256(body_json).hexdigest(),
            "Cache-Control": cc_val,
            "Vary": vary_val,
            "X-Worker-Pid": str(os.getpid()),
        }
        return body_json, 200, headers

    @app.route("/api/profile")
    def api_profile():
        return _handle_api()

    @app.route("/api/data_list")
    def api_data_list():
        return _handle_api()

    # ── Fixture plumbing (direct-origin only; outside measured intervals) ──
    @app.post("/admin/set_body_variant")
    def set_variant():
        data = flask_request.get_json(silent=True) or {}
        variant = str(data.get("variant", "A"))
        content = SC.BODY_STATES.get(variant, SC.BODY_STATES["A"])["json"]
        conn = _connect()
        conn.execute("UPDATE body_config SET variant=?, content=? WHERE id=1", (variant, content))
        conn.commit()
        conn.close()
        return jsonify({"ok": True, "variant": variant})

    @app.post("/admin/reset_probe")
    def reset_probe():
        conn = _connect()
        conn.execute("UPDATE runtime_probe SET marker=?, representation=?, revision=?, updated_at=? WHERE id=1",
                     (SC.PRE_MARKER, SC.PRE_REPRESENTATION, SC.PRE_REVISION, SC.PRE_UPDATED_AT))
        conn.commit()
        row = conn.execute("SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1").fetchone()
        conn.close()
        return jsonify({"ok": True, "marker": row["marker"], "representation": row["representation"],
                        "revision": row["revision"], "updated_at": row["updated_at"]})

    @app.post("/admin/session")
    def admin_session():
        data = flask_request.get_json(silent=True) or {}
        sid = str(data.get("sid", ""))
        action = str(data.get("action", "upsert"))
        conn = _connect()
        if action == "upsert":
            conn.execute("INSERT OR REPLACE INTO sessions (sid, username, valid, created_at) VALUES (?,?,1,?)",
                         (sid, "user", time.time()))
        elif action == "delete":
            conn.execute("DELETE FROM sessions WHERE sid=?", (sid,))
        conn.commit()
        n = conn.execute("SELECT COUNT(*) FROM sessions WHERE sid=?", (sid,)).fetchone()[0]
        conn.close()
        return jsonify({"ok": True, "sid": sid, "action": action, "rows": n})

    # ── Controlled intervention surface + auth/session boundary ────────────
    def _authenticate() -> Tuple[Optional[Dict], Optional[Tuple[str, int]]]:
        """Verify HS256 signature AND expiry, then require a live sessions row
        for the token's sid. Every rejection happens BEFORE any UPDATE."""
        auth_header = flask_request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None, ("missing_token", 401)
        token = auth_header[7:]
        try:
            payload = jwt.decode(token, TESTBED_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None, ("expired_token", 401)
        except jwt.InvalidTokenError:
            return None, ("invalid_token", 401)
        sid = str(payload.get("sub", ""))
        conn = _connect()
        row = conn.execute("SELECT id FROM sessions WHERE sid=? AND valid=1", (sid,)).fetchone()
        conn.close()
        if not row:
            return None, ("deleted_session", 403)
        return payload, None

    def _read_probe() -> Dict[str, Any]:
        conn = _connect()
        row = conn.execute(
            "SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1").fetchone()
        conn.close()
        return {"marker": row["marker"], "representation": row["representation"],
                "revision": row["revision"], "updated_at": row["updated_at"]}

    @app.route("/runtime/read")
    def runtime_read():
        payload, err = _authenticate()
        if err:
            return jsonify({"error": err[0]}), err[1]
        state = _read_probe()
        state.update({"session_valid": True, "sid": payload["sub"]})
        return jsonify(state), 200

    def _do_update(col: str, value: str, payload: Dict) -> Any:
        conn = _connect()
        conn.execute(
            f"UPDATE runtime_probe SET {col}=?, revision=revision+1, updated_at=? WHERE id=1",
            (value, time.time()))
        conn.commit()
        conn.close()
        state = _read_probe()
        state.update({"session_valid": True, "sid": payload["sub"], "updated_field": col})
        return jsonify(state), 200

    @app.post("/runtime/write")
    def runtime_write():
        payload, err = _authenticate()
        if err:
            return jsonify({"error": err[0]}), err[1]
        data = flask_request.get_json(silent=True) or {}
        op = data.get("op")
        value = data.get("value")
        if op not in ("set_marker", "set_representation") or not isinstance(value, str) or not value:
            return jsonify({"error": "bad_request", "op": op}), 400
        return _do_update("marker" if op == "set_marker" else "representation", value, payload)

    @app.post("/runtime/set_representation")
    def runtime_set_representation():
        payload, err = _authenticate()
        if err:
            return jsonify({"error": err[0]}), err[1]
        data = flask_request.get_json(silent=True) or {}
        value = data.get("value")
        if not isinstance(value, str) or not value:
            return jsonify({"error": "bad_request"}), 400
        return _do_update("representation", value, payload)

    @app.post("/runtime/restore")
    def runtime_restore():
        payload, err = _authenticate()
        if err:
            return jsonify({"error": err[0]}), err[1]
        return _do_update("marker", SC.PRE_MARKER, payload)

    # ── Real rendered SPA episode pages ────────────────────────────────────
    @app.route("/episode/<sid>/<kind>")
    def episode(sid: str, kind: str):
        planted = flask_request.args.get("planted", "")
        valid_tok = make_valid_token(sid)
        if kind == "drift":
            action = {"path": "/runtime/set_representation", "op": "set_representation",
                      "value": planted, "token": valid_tok, "label": "drift"}
        elif kind == "invalid":
            action = {"path": "/runtime/write", "op": "set_marker",
                      "value": planted, "token": "invalid.token.here", "label": "invalid"}
        elif kind == "expired":
            action = {"path": "/runtime/write", "op": "set_marker",
                      "value": planted, "token": make_expired_token(sid), "label": "expired"}
        elif kind == "deleted":
            action = {"path": "/runtime/write", "op": "set_marker",
                      "value": planted, "token": valid_tok, "label": "deleted"}
        elif kind == "read":
            action = {"path": "/runtime/read", "op": None, "value": None,
                      "token": valid_tok, "label": "read"}
        else:  # "write"
            action = {"path": "/runtime/write", "op": "set_marker",
                      "value": planted, "token": valid_tok, "label": "write"}
        html = (EPISODE_HTML
                .replace("__READ_TOKEN_VALUE__", valid_tok)
                .replace("__ACTION_JSON__", json.dumps(action)))
        return html, 200, {"Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store"}

    @app.route("/readonly/<sid>")
    def readonly(sid: str):
        html = READONLY_HTML.replace("__READ_TOKEN_VALUE__", make_valid_token(sid))
        return html, 200, {"Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store"}

    return app
