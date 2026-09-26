"""Real, reachable, deterministic local HTTP substrate for EXP-FRONTIER-36249071934.

Frozen-design provenance: prereg.md section 5.1/5.2/12.
  * Python stdlib only (``http.server`` / ``socketserver``). No Flask, FastAPI,
    BrowserGym, Playwright, Chromium, docker, or LLM API key.
  * The service is a *pure function of the request plus the current resource
    store*. No timestamps, no randomness, no ports or hostnames in any body, so
    ``sha256(response_body)`` is stable across processes and runs.

Intent -> HTTP surface (prereg.md 5.2 names five intents):

    create_resource  -> PUT    /resources/{rid}   (idempotent create)
    read_resource    -> GET    /resources/{rid}
    update_resource  -> PATCH  /resources/{rid}
    delete_resource  -> DELETE /resources/{rid}
    list_resources   -> GET    /resources

Plus one instance-independent entry-point fetch used by the task plan:

    entry_point      -> GET    /

The entry point exists because a real Web agent's first action of every task is
the same instance-independent fetch; it is *not* a knob tuned to hit any target
determinism fraction. The task-plan mixture ratio is declared in
``taskplan.py`` and its sensitivity is swept in the runner.

Span signature (prereg.md section 12, the refined definition):
    (method, path, normalized_headers, normalized_body, response_code, response_body_hash)
``normalized_headers`` keeps only client-declared content headers; the volatile
``Date``/``Server``/``Host``/``Content-Length`` transport headers are excluded.
"""

from __future__ import annotations

import hashlib
import http.client
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

BANNER = "spider-frontier-deterministic-substrate/1.0.0"

#: Volatile transport headers excluded from the normalized request signature.
VOLATILE_HEADERS = frozenset(
    {
        "date",
        "server",
        "host",
        "content-length",
        "connection",
        "user-agent",
        "accept-encoding",
    }
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_headers(headers: dict[str, str]) -> dict[str, str]:
    return {k.lower(): v for k, v in sorted(headers.items()) if k.lower() not in VOLATILE_HEADERS}


def span_signature(
    method: str,
    path: str,
    headers: dict[str, str],
    body: Any,
    response_code: int,
    response_body: bytes,
) -> str:
    """Frozen 6-tuple span signature (prereg.md section 12)."""
    payload = canonical_json(
        {
            "method": method.upper(),
            "path": path,
            "headers": normalize_headers(headers),
            "body": body,
            "response_code": int(response_code),
            "response_body_hash": sha256_hex(response_body),
        }
    )
    return sha256_hex(payload.encode("utf-8"))


def state_signature(store: dict[str, dict[str, Any]]) -> str:
    """Cheap observable world-state key handed to a no-memory executor.

    A no-memory compiled executor must be able to *locate* a compiled span
    without invoking a model. The only observation used here is the substrate's
    own observable world state (the canonical resource store). It deliberately
    excludes the task plan, the step index and any oracle knowledge, so the
    treatment arm is not handed the derived_context that the parent audit
    recorded as identifiability defect B1.
    """
    return sha256_hex(canonical_json(store).encode("utf-8"))


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = BANNER
    sys_version = ""

    # -- plumbing ---------------------------------------------------------
    def log_message(self, fmt: str, *args: Any) -> None:  # silence stderr noise
        return

    def _send(self, code: int, payload: Any) -> bytes:
        raw = b"" if payload is None else canonical_json(payload).encode("utf-8")
        self.send_response(code)
        if raw:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if raw:
            self.wfile.write(raw)
        return raw

    def _body(self) -> Any:
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return None
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    @property
    def store(self) -> dict[str, dict[str, Any]]:
        return self.server.store  # type: ignore[attr-defined]

    @staticmethod
    def _split(path: str) -> tuple[str, str]:
        parts = [p for p in path.split("?")[0].split("/") if p]
        return (parts[0] if parts else ""), (parts[1] if len(parts) > 1 else "")

    # -- verbs ------------------------------------------------------------
    def do_GET(self) -> None:
        collection, rid = self._split(self.path)
        if collection == "" and rid == "":
            self._send(200, {"server": BANNER, "resources": 0, "entry": "/"})
            return
        if collection != "resources":
            self._send(404, {"error": "not_found", "path": self.path})
            return
        if rid == "":
            self._send(200, {"count": len(self.store), "items": self.store})
            return
        record = self.store.get(rid)
        if record is None:
            self._send(404, {"error": "not_found", "rid": rid})
        else:
            self._send(200, {"rid": rid, "record": record})

    def do_PUT(self) -> None:
        collection, rid = self._split(self.path)
        body = self._body()
        if collection != "resources" or rid == "":
            self._send(404, {"error": "not_found", "path": self.path})
            return
        existed = rid in self.store
        self.store[rid] = {"title": body.get("title"), "value": body.get("value")}
        self._send(200 if existed else 201, {"rid": rid, "created": not existed, "record": self.store[rid]})

    def do_PATCH(self) -> None:
        collection, rid = self._split(self.path)
        body = self._body()
        if collection != "resources" or rid == "":
            self._send(404, {"error": "not_found", "path": self.path})
            return
        record = self.store.get(rid)
        if record is None:
            self._send(404, {"error": "not_found", "rid": rid})
            return
        record.update({k: v for k, v in (body or {}).items() if k in ("title", "value")})
        self._send(200, {"rid": rid, "updated": True, "record": record})

    def do_DELETE(self) -> None:
        collection, rid = self._split(self.path)
        if collection != "resources" or rid == "":
            self._send(404, {"error": "not_found", "path": self.path})
            return
        if rid not in self.store:
            self._send(404, {"error": "not_found", "rid": rid})
            return
        del self.store[rid]
        self._send(200, {"rid": rid, "deleted": True, "remaining": len(self.store)})


class DeterministicHTTPSubstrate:
    """Threaded stdlib HTTP service with a resettable deterministic store."""

    def __init__(self) -> None:
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self._server.store = {}  # type: ignore[attr-defined]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self.port = int(self._server.server_address[1])

    # -- lifecycle --------------------------------------------------------
    def close(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)

    def __enter__(self) -> "DeterministicHTTPSubstrate":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def reset(self) -> None:
        self._server.store.clear()  # type: ignore[attr-defined]

    @property
    def store(self) -> dict[str, dict[str, Any]]:
        return self._server.store  # type: ignore[attr-defined]

    # -- client -----------------------------------------------------------
    def request(self, method: str, path: str, body: Any = None) -> tuple[int, bytes, dict[str, str]]:
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        try:
            payload = None if body is None else canonical_json(body).encode("utf-8")
            headers = {"Content-Type": "application/json"} if payload is not None else {}
            conn.request(method.upper(), path, body=payload, headers=headers)
            resp = conn.getresponse()
            raw = resp.read()
            return resp.status, raw, dict(resp.getheaders())
        finally:
            conn.close()

    def keepalive(self) -> "KeepAliveClient":
        return KeepAliveClient(self.port)


class KeepAliveClient:
    """HTTP/1.1 keep-alive client; the substrate stays a real socket service."""

    def __init__(self, port: int) -> None:
        self._conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        self._conn.connect()

    def request(self, method: str, path: str, body: Any = None) -> tuple[int, bytes, list[str]]:
        payload = None if body is None else canonical_json(body).encode("utf-8")
        headers = {"Content-Type": "application/json"} if payload is not None else {}
        self._conn.request(method.upper(), path, body=payload, headers=headers)
        resp = self._conn.getresponse()
        raw = resp.read()
        # Declared request headers, recorded for the normalized span signature.
        return resp.status, raw, sorted(headers.keys())

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass

    def __enter__(self) -> "KeepAliveClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


# -- prereg.md 12: verify server idempotency, identical request -> identical
#    response, 100 repeats. Recorded as RAW availability/determinism evidence.
#    Each case declares the store seeding it needs, so the destructive verbs are
#    exercised on their SUCCESS path and not only on the 404 path.
_DETERMINISM_CASES: tuple[dict[str, Any], ...] = (
    {"key": "GET /", "method": "GET", "path": "/", "body": None, "setup": ()},
    {"key": "GET /resources", "method": "GET", "path": "/resources", "body": None, "setup": ()},
    {
        "key": "PUT /resources/alpha (create)",
        "method": "PUT",
        "path": "/resources/alpha",
        "body": {"title": "t", "value": 1},
        "setup": (),
    },
    {
        "key": "GET /resources/alpha (read existing)",
        "method": "GET",
        "path": "/resources/alpha",
        "body": None,
        "setup": (("PUT", "/resources/alpha", {"title": "t", "value": 1}),),
    },
    {
        "key": "PATCH /resources/alpha (update existing)",
        "method": "PATCH",
        "path": "/resources/alpha",
        "body": {"value": 2},
        "setup": (("PUT", "/resources/alpha", {"title": "t", "value": 1}),),
    },
    {
        "key": "GET /resources (list non-empty)",
        "method": "GET",
        "path": "/resources",
        "body": None,
        "setup": (("PUT", "/resources/alpha", {"title": "t", "value": 1}),),
    },
    {
        "key": "DELETE /resources/alpha (delete existing)",
        "method": "DELETE",
        "path": "/resources/alpha",
        "body": None,
        "setup": (("PUT", "/resources/alpha", {"title": "t", "value": 1}),),
    },
    {
        "key": "GET /resources/alpha (read after delete)",
        "method": "GET",
        "path": "/resources/alpha",
        "body": None,
        "setup": (
            ("PUT", "/resources/alpha", {"title": "t", "value": 1}),
            ("DELETE", "/resources/alpha", None),
        ),
    },
)


def determinism_check(repeats: int = 100) -> dict[str, Any]:
    probes: dict[str, dict[str, Any]] = {}
    with DeterministicHTTPSubstrate() as sub:
        client = sub.keepalive()
        try:
            for case in _DETERMINISM_CASES:
                seen: set[str] = set()
                codes: set[int] = set()
                for _ in range(repeats):
                    sub.reset()
                    for m, p, b in case["setup"]:
                        client.request(m, p, b)
                    code, raw, _sent = client.request(case["method"], case["path"], case["body"])
                    seen.add(sha256_hex(raw))
                    codes.add(code)
                probes[case["key"]] = {
                    "request": f"{case['method']} {case['path']}",
                    "repeats": repeats,
                    "unique_response_body_hashes": len(seen),
                    "status_codes": sorted(codes),
                    "deterministic": len(seen) == 1 and len(codes) == 1,
                }
        finally:
            client.close()
    return {
        "repeats_per_probe": repeats,
        "all_probes_deterministic": all(p["deterministic"] for p in probes.values()),
        "n_probes": len(probes),
        "identical_request_round_trips": sum(p["repeats"] for p in probes.values()),
        "probes": probes,
    }


if __name__ == "__main__":  # pragma: no cover - manual availability probe
    print(json.dumps(determinism_check(100), indent=2, sort_keys=True))
