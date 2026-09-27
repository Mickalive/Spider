"""Dual-regime HTTP substrate for EXP-PRODUCT-36306521892 (C-PRODUCT-ECON).

Frozen prereg section 4 requires a single in-process HTTP substrate with two
operating modes serving the same resource structure:

Costly regime (mode="costly"):
  - POST /auth/login -> Bearer token; token expires after TOKEN_EXPIRY requests
    (monotone counter); no re-issue endpoint (401 after expiry)
  - GET /schema -> verb/method/body templates (schema discovery)
  - GET /{collection}?page=N&page_size=10 -> paginated listing
  - GET/PUT/DELETE /{collection}/{id} requires valid token

Cheap regime (mode="cheap"):
  - No auth; all endpoints public
  - No schema discovery; no pagination
  - GET /{collection}/{id} returns the entity directly (1 request)

Resource structure (namespaces disjoint by construction):
  - Resource A (training): /items/{id}  — item-1 .. item-200
  - Resource B (transfer): /products/{id} — SKU-A..SKU-Z, PROD-100..PROD-199

The substrate is stdlib-only, deterministic, and resettable between arms.
"""

from __future__ import annotations

import hashlib
import json
import string
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

# --------------------------------------------------------------------------- #
# Identifier namespaces (disjoint by construction)
# --------------------------------------------------------------------------- #

RESOURCE_A_IDS: list[str] = [f"item-{i}" for i in range(1, 201)]
# 150 product ids = 50 per family (prereg minimum). Disjoint from item-N.
RESOURCE_B_IDS: list[str] = (
    [f"SKU-{c}" for c in string.ascii_uppercase] + [f"PROD-{i}" for i in range(100, 224)]
)

ALL_IDS = set(RESOURCE_A_IDS) | set(RESOURCE_B_IDS)
OVERLAP = set(RESOURCE_A_IDS) & set(RESOURCE_B_IDS)

#: Tokens are issued per login and expire after this many requests.
TOKEN_EXPIRY = 100


def label_for(identifier: str) -> str:
    """Deterministic label for an identifier. No RNG anywhere in the substrate."""
    bucket = int(hashlib.sha256(identifier.encode()).hexdigest()[:4], 16) % 8
    return f"lab{bucket}"


# --------------------------------------------------------------------------- #
# In-process mutable store, resettable between arms
# --------------------------------------------------------------------------- #


class Store:
    def __init__(self) -> None:
        self.entities: dict[tuple[str, str], dict[str, Any]] = {}
        self.request_counts: dict[str, int] = {}  # token -> request count
        self._lock = threading.Lock()

    def reset(self) -> None:
        with self._lock:
            self.entities.clear()
            self.request_counts.clear()

    def seed(self, collection: str, identifier: str) -> int | None:
        key = (collection, identifier)
        with self._lock:
            if key in self.entities:
                return None
            self.entities[key] = {
                "id": identifier,
                "label": label_for(identifier),
                "collection": collection,
            }
            return 1

    def get(self, collection: str, identifier: str) -> dict[str, Any] | None:
        with self._lock:
            return self.entities.get((collection, identifier))

    def update(self, collection: str, identifier: str, label: str) -> bool:
        with self._lock:
            key = (collection, identifier)
            if key not in self.entities:
                return False
            self.entities[key]["label"] = label
            return True

    def delete(self, collection: str, identifier: str) -> bool:
        with self._lock:
            key = (collection, identifier)
            if key not in self.entities:
                return False
            del self.entities[key]
            return True

    def list(self, collection: str, page: int, page_size: int) -> list[dict[str, Any]]:
        with self._lock:
            rows = [
                dict(value)
                for (coll, _), value in sorted(self.entities.items())
                if coll == collection
            ]
            start = (page - 1) * page_size
            return rows[start:start + page_size]

    def issue_token(self) -> str:
        with self._lock:
            raw = f"tok-{len(self.request_counts)}-{threading.get_ident()}"
            token = hashlib.sha256(raw.encode()).hexdigest()[:20]
            self.request_counts[token] = 0
            return token

    def is_token_valid(self, token: str) -> bool:
        with self._lock:
            if token not in self.request_counts:
                return False
            self.request_counts[token] += 1
            return self.request_counts[token] <= TOKEN_EXPIRY


# --------------------------------------------------------------------------- #
# HTTP handler
# --------------------------------------------------------------------------- #


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "spider-dual-substrate/1.0"
    sys_version = ""

    store: Store
    mode: str  # "costly" or "cheap"

    def log_message(self, *args: Any) -> None:
        pass

    def _token(self) -> str | None:
        if self.mode == "cheap":
            return "anonymous"
        header = self.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return None
        token = header[len("Bearer "):].strip()
        if not self.store.is_token_valid(token):
            return None
        return token

    def _body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        raw = self.rfile.read(length)
        try:
            parsed = json.loads(raw.decode())
        except (ValueError, UnicodeDecodeError):
            return {}
        return parsed if isinstance(parsed, dict) else {}

    def _send(self, status: int, payload: Any | None, extra_headers: dict[str, str] | None = None) -> None:
        body = b"" if payload is None else json.dumps(payload, sort_keys=True).encode()
        self.send_response(status)
        if body:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for key, value in (extra_headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _unauthorized(self) -> None:
        self._send(401, {"error": "unauthorized", "mode": self.mode})

    def _index(self) -> None:
        self._send(200, {
            "mode": self.mode,
            "collections": ["items", "products"],
            "verbs": {
                "read": "GET /{collection}/{id}",
                "update": "PUT /{collection}/{id} {\"label\"}",
                "delete": "DELETE /{collection}/{id}",
                "list": "GET /{collection}?page=N&page_size=10",
            },
        })

    def do_GET(self) -> None:
        token = self._token()
        if token is None:
            return self._unauthorized()
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]

        if not parts:
            return self._index()

        if parts[0] == "schema":
            if self.mode == "cheap":
                return self._send(404, {"error": "no schema in cheap mode"})
            return self._send(200, {
                "verbs": {
                    "read": "GET /{collection}/{id}",
                    "update": "PUT /{collection}/{id} {\"label\"}",
                    "delete": "DELETE /{collection}/{id}",
                },
                "auth": "Bearer token required",
                "pagination": "GET /{collection}?page=N&page_size=10",
            })

        if parts[0] == "auth":
            return self._send(404, {"error": "use POST /auth/login"})

        collection = parts[0]
        if len(parts) == 1:
            if self.mode == "cheap":
                # No pagination in cheap mode; return all rows
                rows = [dict(v) for (c, _), v in sorted(self.store.entities.items()) if c == collection]
                return self._send(200, {"collection": collection, "count": len(rows), "rows": rows})
            query = parse_qs(parsed.query)
            try:
                page = int((query.get("page") or ["1"])[0])
                page_size = int((query.get("page_size") or ["10"])[0])
            except ValueError:
                return self._send(400, {"error": "page and page_size must be integers"})
            if page < 1 or page_size < 1:
                return self._send(400, {"error": "page and page_size must be >= 1"})
            rows = self.store.list(collection, page, page_size)
            return self._send(200, {"collection": collection, "page": page, "count": len(rows), "rows": rows})

        identifier = "/".join(parts[1:])
        record = self.store.get(collection, identifier)
        if record is None:
            return self._send(404, {"error": "not found", "id": identifier})
        return self._send(200, dict(record))

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]

        if parts == ["auth", "login"]:
            if self.mode == "cheap":
                return self._send(404, {"error": "no auth in cheap mode"})
            token = self.store.issue_token()
            return self._send(200, {"token": token, "expires_after": TOKEN_EXPIRY})

        if self.mode == "costly":
            token = self._token()
            if token is None:
                return self._unauthorized()

        if len(parts) == 1:
            return self._send(405, {"error": "POST expects /auth/login"})
        return self._send(405, {"error": "POST not supported for resources"})

    def do_PUT(self) -> None:
        if self.mode == "costly":
            token = self._token()
            if token is None:
                return self._unauthorized()
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        if len(parts) != 2:
            return self._send(405, {"error": "PUT expects /{collection}/{id}"})
        body = self._body()
        label = body.get("label")
        if not isinstance(label, str):
            return self._send(400, {"error": "label is required"})
        collection, identifier = parts
        if not self.store.update(collection, identifier, label):
            return self._send(404, {"error": "not found", "id": identifier})
        return self._send(200, dict(self.store.get(collection, identifier)))

    def do_DELETE(self) -> None:
        if self.mode == "costly":
            token = self._token()
            if token is None:
                return self._unauthorized()
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        if len(parts) != 2:
            return self._send(405, {"error": "DELETE expects /{collection}/{id}"})
        collection, identifier = parts
        if not self.store.delete(collection, identifier):
            return self._send(404, {"error": "not found", "id": identifier})
        return self._send(200, {"deleted": True, "id": identifier})


class Substrate:
    """Owns the store and the in-process HTTP server. One instance per mode."""

    def __init__(self, mode: str) -> None:
        if mode not in ("costly", "cheap"):
            raise ValueError(f"unknown mode: {mode}")
        self.mode = mode
        self.store = Store()
        handler = type("_BoundHandler", (_Handler,), {"store": self.store, "mode": mode})
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.port = self.httpd.server_address[1]
        self.base_url = f"http://127.0.0.1:{self.port}"
        self._thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self._thread.start()

    def reset(self) -> None:
        self.store.reset()

    def seed_many(self, collection: str, identifiers: list[str]) -> int:
        for identifier in identifiers:
            self.store.seed(collection, identifier)
        return len(identifiers)

    def stop(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self._thread.join(timeout=5)
