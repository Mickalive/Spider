"""Local HTTP substrate for EXP-PRODUCT-36249064252 (C-PARAM-INHERIT).

Frozen prereg section 2 requires a locally served HTTP resource with

* real ETag / 304 conditional responses,
* session-scoped responses via a Bearer token,
* two resource families with **disjoint identifier value sets**,
* deterministic behaviour for a given (state, action, identifier) - no RNG.

Everything is stdlib ``http.server`` bound to 127.0.0.1 on an ephemeral port.
No browser, no docker, no LLM key, no external network.

Resource-A identifier namespace : ``item-1..item-100``, ``tag-1..tag-100``
Resource-B identifier namespace : ``SKU-A..SKU-Z``, ``PROD-100..PROD-199``

The two namespaces share no string, so an identifier learned on A can never be
reused verbatim on B (prereg section 2, "disjoint value sets").
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

RESOURCE_A_IDS: list[str] = [f"item-{i}" for i in range(1, 101)] + [f"tag-{i}" for i in range(1, 101)]
RESOURCE_A_COLLECTIONS = ("items", "tags")

RESOURCE_B_IDS: list[str] = (
    [f"SKU-{c}" for c in string.ascii_uppercase] + [f"PROD-{i}" for i in range(100, 200)]
)
RESOURCE_B_COLLECTION = "products"

ALL_IDS = set(RESOURCE_A_IDS) | set(RESOURCE_B_IDS)
OVERLAP = set(RESOURCE_A_IDS) & set(RESOURCE_B_IDS)

#: Tokens -> (user, role). ``owner`` may mutate; ``viewer`` may only read.
TOKENS: dict[str, tuple[str, str]] = {
    "tok-owner-a": ("alice", "owner"),
    "tok-viewer-a": ("bob", "viewer"),
    "tok-owner-b": ("carol", "owner"),
}

CATALOG_LABELS = tuple(f"cat{i}" for i in range(8))


def label_for(identifier: str) -> str:
    """Deterministic label for an identifier. No RNG anywhere in the substrate."""
    bucket = int(hashlib.sha256(identifier.encode()).hexdigest()[:4], 16) % len(CATALOG_LABELS)
    return CATALOG_LABELS[bucket]


def session_id_for(token: str) -> str:
    return "sess-" + hashlib.sha256(token.encode()).hexdigest()[:10]


def etag_for(collection: str, identifier: str, version: int, token: str) -> str:
    """Session-scoped ETag: a different token yields a different validator."""
    raw = f"{collection}/{identifier}/{version}/{session_id_for(token)}"
    return 'W/"' + hashlib.sha256(raw.encode()).hexdigest()[:20] + '"'


# --------------------------------------------------------------------------- #
# In-process mutable store, resettable between arms without any HTTP round trip
# --------------------------------------------------------------------------- #


class Store:
    def __init__(self) -> None:
        self.entities: dict[tuple[str, str], dict[str, Any]] = {}
        self.versions: dict[tuple[str, str], int] = {}

    def reset(self) -> None:
        self.entities.clear()
        self.versions.clear()

    def seed(self, collection: str, identifier: str) -> None:
        key = (collection, identifier)
        self.entities[key] = {
            "id": identifier,
            "label": label_for(identifier),
            "owner": "seed",
            "created_index": len(self.entities),
        }
        self.versions[key] = 1

    def create(self, collection: str, identifier: str, label: str, owner: str) -> int | None:
        key = (collection, identifier)
        if key in self.entities:
            return None
        self.entities[key] = {
            "id": identifier,
            "label": label,
            "owner": owner,
            "created_index": len(self.entities),
        }
        self.versions[key] = 1
        return 1

    def get(self, collection: str, identifier: str) -> dict[str, Any] | None:
        return self.entities.get((collection, identifier))

    def update(self, collection: str, identifier: str, label: str) -> int | None:
        key = (collection, identifier)
        if key not in self.entities:
            return None
        self.entities[key]["label"] = label
        self.versions[key] = self.versions.get(key, 1) + 1
        return self.versions[key]

    def delete(self, collection: str, identifier: str) -> bool:
        key = (collection, identifier)
        if key not in self.entities:
            return False
        del self.entities[key]
        self.versions.pop(key, None)
        return True

    def list(self, collection: str, term: str | None, limit: int | None) -> list[dict[str, Any]]:
        """Filtered listing. ``term`` is a substring match on the record id or label.

        Matching the id is what lets a query task be stated over an identifier
        namespace ("SKU", "PROD") rather than over opaque label values.
        """
        rows = [
            dict(value)
            for (coll, _), value in sorted(self.entities.items(), key=lambda kv: kv[1]["created_index"])
            if coll == collection
            and (not term or term in value["label"] or term in value["id"])
        ]
        return rows if limit is None else rows[:limit]


# --------------------------------------------------------------------------- #
# HTTP handler
# --------------------------------------------------------------------------- #


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "spider-substrate/1.0"
    sys_version = ""

    store: Store

    def log_message(self, *args: Any) -> None:  # silence per-request stderr noise
        pass

    # -- helpers ---------------------------------------------------------- #

    def _token(self) -> str | None:
        header = self.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return None
        token = header[len("Bearer ") :].strip()
        return token if token in TOKENS else None

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
        self._send(401, {"error": "unauthenticated"})

    def _forbidden(self) -> None:
        self._send(403, {"error": "role may not mutate"})

    def _scoped(self, record: dict[str, Any], token: str) -> dict[str, Any]:
        """Session-scoped response body: the same entity looks different per token."""
        user, _role = TOKENS[token]
        return {**record, "session": session_id_for(token), "visible_to": user}

    # -- verbs ------------------------------------------------------------ #

    def do_GET(self) -> None:  # noqa: N802
        token = self._token()
        if token is None:
            return self._unauthorized()
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]

        if not parts:
            # Public API index. Exists so that a documented, no-memory executor is
            # a *strong* baseline rather than an unreachable strawman.
            return self._send(
                200,
                {
                    "collections": list(RESOURCE_A_COLLECTIONS) + [RESOURCE_B_COLLECTION],
                    "verbs": {
                        "create": "POST /{collection} {\"id\",\"label\"}",
                        "read": "GET /{collection}/{id}",
                        "update": "PUT /{collection}/{id} {\"label\"}",
                        "delete": "DELETE /{collection}/{id}",
                        "list": "GET /{collection}?q=<label>&limit=<n>",
                    },
                },
            )

        collection = parts[0]
        if len(parts) == 1:
            query = parse_qs(parsed.query)
            term = (query.get("q") or [None])[0]
            raw_limit = (query.get("limit") or [None])[0]
            try:
                limit = int(raw_limit) if raw_limit is not None else None
            except ValueError:
                return self._send(400, {"error": "limit must be an integer"})
            rows = [self._scoped(row, token) for row in self.store.list(collection, term, limit)]
            return self._send(200, {"collection": collection, "count": len(rows), "rows": rows})

        identifier = "/".join(parts[1:])
        record = self.store.get(collection, identifier)
        if record is None:
            return self._send(404, {"error": "not found", "id": identifier})
        etag = etag_for(collection, identifier, self.store.versions[(collection, identifier)], token)
        if self.headers.get("If-None-Match") == etag:
            # Real 304: no body, validator only.
            self.send_response(304)
            self.send_header("ETag", etag)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None
        return self._send(200, self._scoped(record, token), {"ETag": etag})

    def do_POST(self) -> None:  # noqa: N802
        token = self._token()
        if token is None:
            return self._unauthorized()
        user, role = TOKENS[token]
        if role != "owner":
            return self._forbidden()
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        if len(parts) != 1:
            return self._send(405, {"error": "POST expects /{collection}"})
        body = self._body()
        identifier, label = body.get("id"), body.get("label")
        if not isinstance(identifier, str) or not isinstance(label, str):
            return self._send(400, {"error": "id and label are required strings"})
        version = self.store.create(parts[0], identifier, label, user)
        if version is None:
            return self._send(409, {"error": "already exists", "id": identifier})
        record = self._scoped(self.store.get(parts[0], identifier), token)
        return self._send(
            201,
            record,
            {"ETag": etag_for(parts[0], identifier, version, token), "Location": f"/{parts[0]}/{identifier}"},
        )

    def do_PUT(self) -> None:  # noqa: N802
        token = self._token()
        if token is None:
            return self._unauthorized()
        _user, role = TOKENS[token]
        if role != "owner":
            return self._forbidden()
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        if len(parts) != 2:
            return self._send(405, {"error": "PUT expects /{collection}/{id}"})
        body = self._body()
        label = body.get("label")
        if not isinstance(label, str):
            return self._send(400, {"error": "label is required"})
        collection, identifier = parts
        version = self.store.update(collection, identifier, label)
        if version is None:
            return self._send(404, {"error": "not found", "id": identifier})
        record = self._scoped(self.store.get(collection, identifier), token)
        return self._send(200, record, {"ETag": etag_for(collection, identifier, version, token)})

    def do_DELETE(self) -> None:  # noqa: N802
        token = self._token()
        if token is None:
            return self._unauthorized()
        _user, role = TOKENS[token]
        if role != "owner":
            return self._forbidden()
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        if len(parts) != 2:
            return self._send(405, {"error": "DELETE expects /{collection}/{id}"})
        collection, identifier = parts
        if not self.store.delete(collection, identifier):
            return self._send(404, {"error": "not found", "id": identifier})
        return self._send(200, {"deleted": True, "id": identifier, "session": session_id_for(token)})


class Substrate:
    """Owns the store and the in-process HTTP server. Call :meth:`reset` per arm."""

    def __init__(self) -> None:
        self.store = Store()
        handler = type("_BoundHandler", (_Handler,), {"store": self.store})
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
