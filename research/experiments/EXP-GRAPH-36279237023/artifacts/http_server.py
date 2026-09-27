"""Stdlib-only HTTP application for EXP-GRAPH-36279237023 (prereg.md 3.1).

Preregistering exactly this and nothing more:
  * Python `http.server` with a custom BaseHTTPRequestHandler; no web framework;
  * 20 REST endpoints = 5 resource families x 4 verbs (CREATE/READ/UPDATE/DELETE);
  * in-memory dictionaries per family, fully reset before every task;
  * no persistence;
  * `state_hash()` returns SHA256 over the canonical JSON serialisation of the
    complete server state, i.e. the logged per-task state hash required by
    prereg.md 5.2 / measurement-validity condition V7.

Requests are issued over a real TCP socket from http.client so that the
verification measure (prereg.md 6.3 http_execution_success_rate) exercises the
HTTP path rather than calling handler functions in-process.
"""

from __future__ import annotations

import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

FAMILIES = ["users", "posts", "comments", "albums", "photos"]
VERB_TO_STATUS = {
    "create": 201,
    "read": 200,
    "update": 200,
    "delete": 204,
}
# Deterministic initial records so that READ/UPDATE/DELETE of a well-formed id
# can succeed without depending on task order. Seeded by fixture, not by UUID
# (the parent packet's unseeded uuid4() was an explicit reproducibility defect).
SEED_RECORDS: dict[str, list[int]] = {
    "users": list(range(1, 11)),
    "posts": list(range(1, 11)),
    "comments": list(range(1, 11)),
    "albums": list(range(1, 11)),
    "photos": list(range(1, 11)),
}


class Store:
    """Complete, serialisable application state."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.records: dict[str, dict[int, dict]] = {
            f: {i: {"id": i, "seeded": True} for i in recs} for f, recs in SEED_RECORDS.items()
        }
        self.next_id: dict[str, int] = {f: 1000 for f in FAMILIES}
        # request_count is a transport counter, not application state. It is
        # deliberately EXCLUDED from the state hash: including it would make the
        # pre-request hash differ from the post-request hash and would make
        # "identical starting state" unverifiable (prereg 5.2 / V7).
        self.request_count = 0

    def snapshot(self) -> str:
        return json.dumps(
            {"records": self.records, "next_id": self.next_id},
            sort_keys=True,
            separators=(",", ":"),
        )

    def state_hash(self) -> str:
        return hashlib.sha256(self.snapshot().encode("utf-8")).hexdigest()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    store: Store  # injected by make_server

    def log_message(self, *_args) -> None:  # keep stdout clean and deterministic
        return

    # -- helpers ---------------------------------------------------------
    def _send(self, code: int, payload: dict | None = None) -> None:
        body = b"" if payload is None else json.dumps(payload).encode("utf-8")
        self.send_response(code)
        if body:
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
        else:
            self.send_header("Content-Length", "0")
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return {}

    def _route(self) -> tuple[str | None, str | None, int | None]:
        path = unquote(urlparse(self.path).path).strip("/")
        parts = path.split("/")
        if len(parts) == 1:
            return parts[0], None, None
        if len(parts) == 2:
            try:
                return parts[0], None, int(parts[1])
            except ValueError:
                return parts[0], None, None
        return None, None, None

    # -- verbs -----------------------------------------------------------
    def do_POST(self) -> None:
        self.store.request_count += 1
        family, _, _ = self._route()
        if family not in FAMILIES:
            self._send(404, {"error": "unknown family"})
            return
        body = self._read_body()
        rid = self.store.next_id[family]
        self.store.next_id[family] = rid + 1
        self.store.records[family][rid] = dict(body)
        self._send(201, {"id": rid, "family": family, "record": body})

    def do_GET(self) -> None:
        self.store.request_count += 1
        family, _, rid = self._route()
        if family not in FAMILIES:
            self._send(404, {"error": "unknown family"})
            return
        if rid is None:
            self._send(200, {"family": family, "count": len(self.store.records[family])})
            return
        rec = self.store.records[family].get(rid)
        if rec is None:
            self._send(404, {"error": "not found", "id": rid})
            return
        self._send(200, {"id": rid, "family": family, "record": rec})

    def do_PUT(self) -> None:
        self.store.request_count += 1
        family, _, rid = self._route()
        if family not in FAMILIES:
            self._send(404, {"error": "unknown family"})
            return
        if rid is None or rid not in self.store.records[family]:
            self._send(404, {"error": "not found", "id": rid})
            return
        body = self._read_body()
        self.store.records[family][rid].update(body)
        self._send(200, {"id": rid, "family": family, "record": self.store.records[family][rid]})

    def do_DELETE(self) -> None:
        self.store.request_count += 1
        family, _, rid = self._route()
        if family not in FAMILIES:
            self._send(404, {"error": "unknown family"})
            return
        if rid is None or rid not in self.store.records[family]:
            self._send(404, {"error": "not found", "id": rid})
            return
        del self.store.records[family][rid]
        self._send(204)


def make_server(host: str = "127.0.0.1", port: int = 0) -> tuple[ThreadingHTTPServer, Store]:
    store = Store()
    handler = type("BoundHandler", (Handler,), {"store": store})
    httpd = ThreadingHTTPServer((host, port), handler)
    httpd.daemon_threads = True
    return httpd, store


def serve_in_background(host: str = "127.0.0.1", port: int = 0):
    """Start the server on a daemon thread and return (httpd, store, base_url)."""
    httpd, store = make_server(host, port)
    thread = threading.Thread(target=httpd.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
    thread.start()
    return httpd, store, f"http://{httpd.server_address[0]}:{httpd.server_address[1]}"


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    httpd, _store, url = serve_in_background(port=port)
    print(url, flush=True)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        httpd.shutdown()
