#!/usr/bin/env python3
"""EXP-GRAPH-36018188168 Flask 3.1.3 single-node substrate app.

Backed by SQLite WAL at /tmp/spider-runtime/single.db. The harness writes state
rows through its OWN sqlite3 connection (cross-process WAL propagation genuinely
exercised: harness writes, this app reads, immediate visibility). HS256 JWT
(PyJWT, shared TESTBED_SECRET) required on every request. GET /resource/<rid>
returns flat JSON (canonical derivation shared with the harness via
resource_for), ETag=SHA256(canonical_json_without_template)[:16],
If-None-Match -> 304 only when fresh and max-age=60, X-Csrf-Token,
X-Worker-Pid=os.getpid() (for $request_uri sticky verification), and
response-signaled _template{query_params, header_names}. gunicorn entry: app.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request

EXPERIMENT_ID = "EXP-GRAPH-36018188168"
TESTBED_SECRET = os.environ.get("TESTBED_SECRET", "TESTBED_SECRET_SPIDER_36018188168")
DB_PATH = os.environ.get("SPIDER_DB_PATH", "/tmp/spider-runtime/single.db")
DRIFT_POINT = 6

FAMILIES = ("dom_drift", "param_header_mutation", "cache_expiry")
NOISE_FAMILIES = ("noise_A_phone", "noise_B_nickname", "noise_C_null")

TYPE_MAP = {"str": "string", "int": "integer", "float": "number", "bool": "boolean",
            "NoneType": "string", "list": "array", "dict": "object"}


def normalize_type(n: str) -> str:
    return TYPE_MAP.get(n, n)


def extract_field_types(obj, prefix: str = ""):
    """(field_path, normalized_type) token set; _template is not a DOM field."""
    pairs = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "_template":
                continue
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                pairs.update(extract_field_types(v, path))
            elif isinstance(v, list):
                pairs.add((path, "array"))
            else:
                pairs.add((path, normalize_type(type(v).__name__)))
    elif isinstance(obj, list):
        pairs.add((prefix, "array"))
    else:
        pairs.add((prefix, normalize_type(type(obj).__name__)))
    return pairs


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def etag_for(body: dict) -> str:
    filtered = {k: v for k, v in body.items() if k != "_template"}
    return hashlib.sha256(canonical_json(filtered)).hexdigest()[:16]


def resource_for(rid: int, family: str, req_num: int) -> dict:
    """Deterministic canonical resource derivation — SINGLE SOURCE OF TRUTH shared
    with the harness (imported, not copy-pasted). Drift families become stale at
    request number >= 6; noise adds optional churn without changing required
    filtered signals; cache_expiry flips email value AND Cache-Control to max-age=0;
    param_header_mutation flips _template query name and X-Csrf-Token value."""
    if family in NOISE_FAMILIES or family in ("fresh_pool", "stable"):
        gt = "fresh"
        body = {"id": rid, "name": f"User {rid}", "email": f"user{rid}@example.com"}
        cc = "max-age=60"
        csrf = "token-abc123"
        qp = {"detail": "full"}
        if family == "noise_A_phone" and (rid + req_num) % 10 < 3:
            body["phone"] = f"555-{rid:04d}"
        if family == "noise_B_nickname" and (rid + req_num) % 10 < 3:
            body["nickname"] = f"nick{rid}"
        if family == "noise_C_null":
            if rid % 5 == 0:
                body["email"] = None
            if (rid + req_num) % 10 < 3:
                body["phone"] = f"555-{rid:04d}"
    else:
        gt = "stale" if req_num >= DRIFT_POINT else "fresh"
        if gt == "fresh":
            body = {"id": rid, "name": f"User {rid}", "email": f"user{rid}@example.com"}
            cc = "max-age=60"
            csrf = "token-abc123"
            qp = {"detail": "full"}
        elif family == "dom_drift":
            body = {"id": str(rid), "name": f"User {rid}",
                    "email": f"user{rid}@example.com", "phone": f"555-{rid:04d}"}
            cc = "max-age=60"
            csrf = "token-abc123"
            qp = {"detail": "full"}
        elif family == "param_header_mutation":
            body = {"id": rid, "name": f"User {rid}", "email": f"user{rid}@example.com"}
            cc = "max-age=60"
            csrf = "token-xyz789"
            qp = {"uid": "full"}
        elif family == "cache_expiry":
            body = {"id": rid, "name": f"User {rid}", "email": f"user{rid + 1000}@example.com"}
            cc = "max-age=0"
            csrf = "token-abc123"
            qp = {"detail": "full"}
        else:
            gt = "fresh"
            body = {"id": rid, "name": f"User {rid}", "email": f"user{rid}@example.com"}
            cc = "max-age=60"
            csrf = "token-abc123"
            qp = {"detail": "full"}
    template = {"query_params": sorted(qp.keys()), "header_names": ["X-Csrf-Token"]}
    return {"body": body, "ground_truth": gt, "cache_control": cc, "csrf": csrf,
            "query_params": qp, "template": template, "etag": etag_for(body)}


def _connect():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def _init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = _connect()
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("CREATE TABLE IF NOT EXISTS resource_state ("
                 "rid INTEGER PRIMARY KEY, family TEXT NOT NULL, "
                 "drift_start INTEGER NOT NULL)")
    conn.commit()
    conn.close()


def _read_state(rid: int):
    conn = _connect()
    row = conn.execute("SELECT family, drift_start FROM resource_state WHERE rid=?",
                       (rid,)).fetchone()
    conn.close()
    if row is None:
        return {"family": "fresh_pool", "drift_start": 9999}
    return {"family": row["family"], "drift_start": row["drift_start"]}


def create_app() -> Flask:
    _init_db()
    app = Flask(__name__)

    @app.route("/resource/<int:rid>", methods=["GET"])
    def resource(rid: int):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401
        token = auth[7:]
        try:
            import jwt
            jwt.decode(token, TESTBED_SECRET, algorithms=["HS256"])
        except Exception:
            return jsonify({"error": "bad token"}), 401
        state = _read_state(rid)
        family = state["family"]
        req_num = int(request.headers.get("X-Request-Num", "1"))
        res = resource_for(rid, family, req_num)
        etag = res["etag"]
        inm = request.headers.get("If-None-Match")
        if (inm and inm == etag and res["ground_truth"] == "fresh"
                and res["cache_control"] == "max-age=60"):
            resp = app.response_class(status=304)
            resp.headers["ETag"] = etag
            resp.headers["Cache-Control"] = res["cache_control"]
            resp.headers["X-Csrf-Token"] = res["csrf"]
            resp.headers["X-Worker-Pid"] = str(os.getpid())
            return resp
        body_with_template = dict(res["body"])
        body_with_template["_template"] = res["template"]
        resp = app.response_class(response=canonical_json(body_with_template),
                                  status=200, content_type="application/json")
        resp.headers["ETag"] = etag
        resp.headers["Cache-Control"] = res["cache_control"]
        resp.headers["X-Csrf-Token"] = res["csrf"]
        resp.headers["X-Worker-Pid"] = str(os.getpid())
        return resp

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=18090)