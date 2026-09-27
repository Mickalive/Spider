"""Measurement-valid local HTTP substrate for EXP-PRODUCT-36314204238.

stdlib only, no external dependencies, deterministic. The server holds four
collections of well-formed identifiers and serves all of them, including the
out-of-support ``widgets`` collection, so that a binder which emits a request for
an identifier it has no training evidence for is NOT rescued by a 404: the
false accept is silent, which is the entire point of the semantic probe.

Endpoints::

    GET    /{collection}          -> list of identifiers
    GET    /{collection}/{ident}  -> detail
    PUT    /{collection}/{ident}  -> update, body {"status": "ok"}
    DELETE /{collection}/{ident}  -> delete

Every request requires ``Authorization: Bearer probe-token``; anything else is
401. Per-request latency is injected deterministically as
``BASE_LATENCY_S * latency_factor`` so the frozen cost manipulation is a real
server-side property and not an arithmetic annotation, and every raw record
carries the observed status and the injected delay.
"""

from __future__ import annotations

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

#: Bearer token the substrate requires. Credential-free in the sense that it is
#: fixed and published: it costs zero requests to hold and never expires, so it
#: cannot smuggle an auth-cost asymmetry into the re-derivation comparison.
AUTH_TOKEN = "Bearer probe-token"

#: Injected latency per request at latency_factor = 1.0.
BASE_LATENCY_S = 0.0002

#: Collection -> singular identifier prefix. This mapping is a property of the
#: SUBSTRATE (how the corpus was generated), not of any binder. No binder in
#: src/spider/ consults it.
COLLECTION_PREFIX = {
    "items": "item",
    "products": "product",
    "orders": "order",
    "widgets": "widget",
}

FAMILY_VERB = {"read": "GET", "update": "PUT", "delete": "DELETE"}


def identifiers_for(collection: str) -> list[str]:
    """Identifiers the substrate serves for one collection."""
    prefix = COLLECTION_PREFIX[collection]
    if collection == "widgets":
        return [f"{prefix}-{i}" for i in range(151, 201)]
    return [f"{prefix}-{i}" for i in range(151, 251)]


TRAIN_IDS = list(range(151, 201))
IN_SUPPORT_IDS = list(range(201, 251))
OUT_OF_SUPPORT_IDS = list(range(151, 201))


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "spider-substrate/1.0"
    #: Without this, a header write followed by a body write on a keep-alive
    #: connection collides with Nagle and costs ~40 ms per request through
    #: delayed ACK. The substrate would then measure TCP behaviour rather than
    #: the frozen request-count cost basis.
    disable_nagle_algorithm = True

    # -- plumbing ------------------------------------------------------------- #

    def log_message(self, *args: Any) -> None:  # pragma: no cover - silence
        return

    def _authorised(self) -> bool:
        return self.headers.get("Authorization") == AUTH_TOKEN

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, sort_keys=True).encode()
        head = (
            f"HTTP/1.1 {status} {BaseHTTPRequestHandler.responses.get(status, ('OK',))[0]}\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"\r\n"
        ).encode()
        self.wfile.write(head + body)

    def _drain_body(self) -> bytes:
        """Consume the request body on EVERY verb.

        With HTTP/1.1 keep-alive an unread body stays in the socket buffer and
        the next request on the same connection is parsed as garbage. A handler
        that ignores its body therefore corrupts the connection rather than
        ignoring the body, so this is called by all three verbs.
        """
        length = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(length) if length else b""

    def _sleep(self) -> float:
        delay = BASE_LATENCY_S * float(self.server.latency_factor)
        if delay > 0:
            time.sleep(delay)
        return delay

    def _split(self) -> tuple[str, str] | None:
        parts = [p for p in self.path.split("?")[0].split("/") if p]
        if len(parts) == 1 and parts[0] in COLLECTION_PREFIX:
            return parts[0], ""
        if len(parts) == 2 and parts[0] in COLLECTION_PREFIX:
            return parts[0], parts[1]
        return None

    def _exists(self, collection: str, ident: str) -> bool:
        return ident in set(identifiers_for(collection))

    # -- verbs ---------------------------------------------------------------- #

    def do_GET(self) -> None:  # noqa: N802
        self._drain_body()
        delay = self._sleep()
        self.server.request_count += 1
        if not self._authorised():
            self._send(401, {"error": "unauthorised", "latency_s": delay})
            return
        split = self._split()
        if split is None:
            self._send(404, {"error": "no such resource", "latency_s": delay})
            return
        collection, ident = split
        if not ident:
            self._send(200, {"collection": collection, "identifiers": identifiers_for(collection), "latency_s": delay})
            return
        if not self._exists(collection, ident):
            self._send(404, {"error": "no such identifier", "latency_s": delay})
            return
        self._send(200, {"collection": collection, "identifier": ident, "exists": True, "latency_s": delay})

    def do_PUT(self) -> None:  # noqa: N802
        delay = self._sleep()
        self.server.request_count += 1
        payload = self._drain_body()
        if not self._authorised():
            self._send(401, {"error": "unauthorised", "latency_s": delay})
            return
        split = self._split()
        if split is None:
            self._send(404, {"error": "no such resource", "latency_s": delay})
            return
        collection, ident = split
        if not ident or not self._exists(collection, ident):
            self._send(404, {"error": "no such identifier", "latency_s": delay})
            return
        self._send(200, {
            "collection": collection,
            "identifier": ident,
            "updated": True,
            "exists": True,
            "body": payload.decode("utf-8", "replace"),
            "latency_s": delay,
        })

    def do_DELETE(self) -> None:  # noqa: N802
        self._drain_body()
        delay = self._sleep()
        self.server.request_count += 1
        if not self._authorised():
            self._send(401, {"error": "unauthorised", "latency_s": delay})
            return
        split = self._split()
        if split is None:
            self._send(404, {"error": "no such resource", "latency_s": delay})
            return
        collection, ident = split
        if not ident or not self._exists(collection, ident):
            self._send(404, {"error": "no such identifier", "latency_s": delay})
            return
        self._send(200, {"collection": collection, "identifier": ident, "exists": False, "latency_s": delay})


class Substrate:
    """Context manager owning a live substrate on an ephemeral loopback port."""

    def __init__(self, latency_factor: float = 1.0) -> None:
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self._server.latency_factor = latency_factor  # type: ignore[attr-defined]
        self._server.request_count = 0  # type: ignore[attr-defined]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def port(self) -> int:
        return int(self._server.server_address[1])

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    @property
    def request_count(self) -> int:
        return int(self._server.request_count)  # type: ignore[attr-defined]

    def set_latency_factor(self, factor: float) -> None:
        self._server.latency_factor = factor  # type: ignore[attr-defined]

    def __enter__(self) -> Substrate:
        self._thread.start()
        return self

    def __exit__(self, *exc: Any) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)
