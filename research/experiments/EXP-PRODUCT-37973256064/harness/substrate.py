"""Real localhost stdlib-HTTP substrate for EXP-PRODUCT-37973256064.

Credential-free, standard-library only, deterministic. Implements the resource
model frozen in prereg.md section 3: three training resource types (items, users,
orders), each with ten systematic identifiers (``<prefix>-001`` .. ``<prefix>-010``),
plus one completely unseen resource type (products) used only by the null control.
A real ``http.server.HTTPServer`` handles one request at a time; responses carry
``Content-Type: application/json`` and a deterministic ``X-Request-Id``.

The substrate is explicitly NOT the synthetic SYNTH-INDUCTION-BANK-v1 fixture:
every observation here is produced by a real HTTP request/response cycle against a
localhost server.
"""

from __future__ import annotations

import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from urllib import error, request

SEED = 42

# Resource types trained on (A) and held out (B). The prereg creates A/B by
# splitting the ten identifiers of each type into 001-005 and 006-010.
TRAINING_TYPES = ("items", "users", "orders")
UNSEEN_TYPE = "products"

# Singular identifier prefix per type, as frozen in prereg section 3.2.
ID_PREFIX = {"items": "item", "users": "user", "orders": "order", "products": "product"}

TRAIN_IDS = [f"{ID_PREFIX[t]}-{i:03d}" for t in TRAINING_TYPES for i in range(1, 6)]
HELDOUT_IDS = {t: [f"{ID_PREFIX[t]}-{i:03d}" for i in range(6, 11)] for t in TRAINING_TYPES}
ALL_IDS = {t: [f"{ID_PREFIX[t]}-{i:03d}" for i in range(1, 11)] for t in TRAINING_TYPES}
UNSEEN_IDS = [f"{ID_PREFIX[UNSEEN_TYPE]}-{i:03d}" for i in range(1, 6)]


def _build_store() -> dict[str, dict[str, str]]:
    store: dict[str, dict[str, str]] = {}
    for rtype, ids in ALL_IDS.items():
        store[rtype] = {rid: f"payload::{rtype}::{rid}" for rid in ids}
    # products exist on the wire but are never observed during induction.
    store[UNSEEN_TYPE] = {rid: f"payload::{UNSEEN_TYPE}::{rid}" for rid in UNSEEN_IDS}
    return store


class _Handler(BaseHTTPRequestHandler):
    """Deterministic REST handler. One request at a time (no ThreadingHTTPServer)."""

    server_version = "SpiderSubstrate/1.0"
    sys_version = ""

    def log_message(self, fmt: str, *args: Any) -> None:  # silence stderr noise
        return

    # -- helpers ---------------------------------------------------------
    def _send_json(self, status: int, payload: dict[str, Any], request_id: str) -> None:
        body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Request-Id", request_id)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if status != 204:
            self.wfile.write(body)

    def _record(self, status: int, request_id: str, extra: dict[str, Any] | None = None) -> None:
        entry = {
            "seq": self.server.next_seq(),  # type: ignore[attr-defined]
            "method": self.command,
            "path": self.path,
            "status": status,
            "request_id": request_id,
        }
        if extra:
            entry.update(extra)
        self.server.request_log.append(entry)  # type: ignore[attr-defined]

    # -- routing ---------------------------------------------------------
    def _split(self) -> tuple[str | None, str | None]:
        parts = self.path.split("?", 1)[0].strip("/").split("/")
        if len(parts) == 3 and parts[0] == "api":
            return parts[1], parts[2]
        if len(parts) == 2 and parts[0] == "api":
            return parts[1], None
        return None, None

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        request_id = hashlib.sha256(("GET" + path).encode()).hexdigest()[:16]
        rtype, rid = self._split()
        store = self.server.store  # type: ignore[attr-defined]
        if rtype in store and rid in store[rtype]:
            self._send_json(200, {"type": rtype, "id": rid, "data": store[rtype][rid]}, request_id)
            self._record(200, request_id, {"resource_type": rtype, "identifier": rid})
        else:
            self._send_json(404, {"error": "not found", "type": rtype, "id": rid}, request_id)
            self._record(404, request_id, {"resource_type": rtype, "identifier": rid})

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length else b""
        request_id = hashlib.sha256(("POST" + self.path + raw.decode("utf-8", "replace")).encode()).hexdigest()[:16]
        rtype, _ = self._split()
        store = self.server.store  # type: ignore[attr-defined]
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send_json(400, {"error": "bad json"}, request_id)
            self._record(400, request_id, {"resource_type": rtype})
            return
        rid = payload.get("id")
        if rtype in store and isinstance(rid, str):
            store[rtype][rid] = payload.get("data", f"payload::{rtype}::{rid}")
            self._send_json(201, {"type": rtype, "id": rid, "data": store[rtype][rid]}, request_id)
            self._record(201, request_id, {"resource_type": rtype, "identifier": rid})
        else:
            self._send_json(404, {"error": "not found", "type": rtype, "id": rid}, request_id)
            self._record(404, request_id, {"resource_type": rtype, "identifier": rid})

    def do_PUT(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length else b""
        request_id = hashlib.sha256(("PUT" + self.path + raw.decode("utf-8", "replace")).encode()).hexdigest()[:16]
        rtype, rid = self._split()
        store = self.server.store  # type: ignore[attr-defined]
        if rtype in store and rid in store[rtype]:
            self._send_json(200, {"type": rtype, "id": rid, "data": store[rtype][rid]}, request_id)
            self._record(200, request_id, {"resource_type": rtype, "identifier": rid})
        else:
            self._send_json(404, {"error": "not found", "type": rtype, "id": rid}, request_id)
            self._record(404, request_id, {"resource_type": rtype, "identifier": rid})

    def do_DELETE(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        request_id = hashlib.sha256(("DELETE" + path).encode()).hexdigest()[:16]
        rtype, rid = self._split()
        store = self.server.store  # type: ignore[attr-defined]
        if rtype in store and rid in store[rtype]:
            del store[rtype][rid]
            self._send_json(204, {}, request_id)
            self._record(204, request_id, {"resource_type": rtype, "identifier": rid})
        else:
            self._send_json(404, {"error": "not found", "type": rtype, "id": rid}, request_id)
            self._record(404, request_id, {"resource_type": rtype, "identifier": rid})


class SubstrateServer:
    """Wraps an HTTPServer bound to an ephemeral localhost port."""

    def __init__(self) -> None:
        self.store = _build_store()
        self.request_log: list[dict[str, Any]] = []
        self._seq = 0
        self._lock = threading.Lock()
        self.httpd = HTTPServer(("127.0.0.1", 0), _Handler)
        self.httpd.store = self.store  # type: ignore[attr-defined]
        self.httpd.request_log = self.request_log  # type: ignore[attr-defined]
        self.httpd.next_seq = self._next_seq  # type: ignore[attr-defined]
        self.host, self.port = self.httpd.server_address
        self.base_url = f"http://{self.host}:{self.port}"
        self._thread: threading.Thread | None = None

    def _next_seq(self) -> int:
        # Serialised by the single-threaded server; lock keeps it stable anyway.
        with self._lock:
            self._seq += 1
            return self._seq

    def start(self) -> None:
        self._thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)


class SubstrateClient:
    """Credential-free HTTP client over urllib; counts every real request."""

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def execute(self, bound_action: dict[str, Any]) -> dict[str, Any]:
        method = bound_action.get("method", "GET")
        url = bound_action.get("url")
        if not isinstance(url, str):
            return {"status": None, "error": "no url in bound action", "body": None}
        headers = dict(bound_action.get("headers") or {})
        data = None
        if "json" in bound_action:
            data = json.dumps(bound_action["json"]).encode()
            headers.setdefault("Content-Type", "application/json")
        elif "body" in bound_action and isinstance(bound_action["body"], str):
            data = bound_action["body"].encode()
        req = request.Request(url, data=data, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:  # noqa: S310 (localhost only)
                raw = resp.read()
                status = resp.status
                response_headers = {k: v for k, v in resp.getheaders()}
        except error.HTTPError as exc:
            raw = exc.read()
            status = exc.code
            response_headers = {k: v for k, v in exc.headers.items()}
        except error.URLError as exc:  # pragma: no cover - infrastructure only
            return {"status": None, "error": str(exc), "body": None, "headers": {}}
        body: Any
        try:
            body = json.loads(raw.decode("utf-8")) if raw else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            body = raw.decode("utf-8", "replace")
        return {"status": status, "body": body, "headers": response_headers}


def is_success_response(response: dict[str, Any], rtype: str, rid: str) -> bool:
    """Mechanical postcondition: HTTP 200 and the body echoes the requested resource."""
    if response.get("status") != 200:
        return False
    body = response.get("body")
    return isinstance(body, dict) and body.get("type") == rtype and body.get("id") == rid
