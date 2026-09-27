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


#: Frozen salt for the opt-in capability-mint extension used by
#: EXP-FRONTIER-36272394045 (spec measurement_validity.task_generator item (d):
#: a declared non-zero class_iii_fraction whose binding key "comes from a prior
#: response"). Deterministic so an auditor can recompute every handle from the
#: raw trace; never present in the plan, the goal/intent prefix, the resource
#: store, or any request path.
MINT_SALT = sha256_hex(b"spider-mint-salt-EXP-FRONTIER-36272394045")[:16]


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


# ---------------------------------------------------------------------------
# Opt-in capability mint (EXP-FRONTIER-36272394045, spec measurement_validity.
# task_generator item (d): a declared non-zero class_iii_fraction whose binding
# key "comes from a prior response" and is absent from the observable state and
# from the goal/intent prefix).
#
# A minted handle is ``<episode_counter:08x><mac[:8]>`` where
# ``mac = sha256(MINT_SALT | counter)[:8]``. Validation is therefore a pure
# function of the request: the server keeps no per-handle state, so the substrate
# remains a pure function of the request plus the resource store and its
# determinism guarantee is unchanged.
#
# The handle is a pure function of (salt, episode counter) only. It is NOT a
# function of the resource store and NOT a function of any request path or
# resource identity, so an executor that can observe only
# (world_store_snapshot, last_request_method, last_request_path) -- the
# observable state prereg.md section 5 fixes -- cannot derive it, and neither can
# an executor that knows the task plan. The only channels that carry it are the
# mint response HEADER, the mint response BODY field ``capability_handle``
# (added by EXP-FRONTIER-36287182510, prereg.md section 5) and the raw
# server-side observation read by the runner.
# ---------------------------------------------------------------------------
TOKEN_LEN = 16


def _token_mac(counter: int) -> str:
    return sha256_hex(f"{MINT_SALT}|{counter:08x}".encode("utf-8"))[:8]


def mint_token(counter: int) -> str:
    """Deterministic episode-scoped capability handle."""
    return f"{counter:08x}{_token_mac(counter)}"


def token_valid(token: str) -> bool:
    """Stateless validation: recompute the MAC from the handle's own counter."""
    if len(token) != TOKEN_LEN:
        return False
    try:
        counter = int(token[:8], 16)
    except ValueError:
        return False
    if token[:8] != f"{counter:08x}":
        return False
    return token[8:] == _token_mac(counter)


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = BANNER
    sys_version = ""
    # Transport-only latency fix (EXP-FRONTIER-36272394045). The stdlib handler
    # writes response headers and response body as two separate socket writes;
    # with Nagle enabled the second write waits on the peer's delayed ACK, which
    # pinned the substrate at ~24 requests/second and made the preregistered
    # 30k-request program time out. TCP_NODELAY changes no response byte, so the
    # determinism guarantee and every recorded body hash are unaffected.
    disable_nagle_algorithm = True

    # -- plumbing ---------------------------------------------------------
    def log_message(self, fmt: str, *args: Any) -> None:  # silence stderr noise
        return

    def _send(self, code: int, payload: Any, extra_headers: dict[str, str] | None = None) -> bytes:
        raw = b"" if payload is None else canonical_json(payload).encode("utf-8")
        self.send_response(code)
        if raw:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        for name, value in sorted((extra_headers or {}).items()):
            self.send_header(name, value)
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

    # -- opt-in capability mint (EXP-FRONTIER-36272394045) ------------------
    @staticmethod
    def _query(path: str) -> dict[str, str]:
        if "?" not in path:
            return {}
        return dict(
            kv.split("=", 1) if "=" in kv else (kv, "")
            for kv in path.split("?", 1)[1].split("&")
            if kv
        )

    # -- verbs ------------------------------------------------------------
    def do_GET(self) -> None:
        collection, rid = self._split(self.path)
        query = self._query(self.path)
        if collection == "" and rid == "":
            self._send(200, {"server": BANNER, "resources": 0, "entry": "/"})
            return
        if collection != "resources":
            self._send(404, {"error": "not_found", "path": self.path})
            return
        if rid == "":
            if "view" in query:
                if not token_valid(query["view"]):
                    self._send(404, {"error": "not_found", "path": self.path})
                    return
                self._send(200, {"count": len(self.store), "items": self.store, "view_valid": True})
                return
            self._send(200, {"count": len(self.store), "items": self.store})
            return
        record = self.store.get(rid)
        if "t" in query:
            if record is None or not token_valid(query["t"]):
                self._send(404, {"error": "not_found", "path": self.path})
                return
            self._send(200, {"rid": rid, "record": record, "token_valid": True})
            return
        if record is None:
            self._send(404, {"error": "not_found", "rid": rid})
        else:
            self._send(200, {"rid": rid, "record": record})

    def do_PUT(self) -> None:
        collection, rid = self._split(self.path)
        body = self._body()
        query = self._query(self.path)
        if collection != "resources" or rid == "":
            self._send(404, {"error": "not_found", "path": self.path})
            return
        existed = rid in self.store
        # A bodyless PUT is a well-formed HTTP request that names a field-less
        # record, not a server fault. ``do_PATCH`` already treats a missing body
        # as an empty object; PUT now does the same instead of raising and
        # dropping the keep-alive connection. No request issued by the parent
        # task plan ever sends a missing body, so every recorded parent body
        # hash is unchanged.
        payload = body or {}
        self.store[rid] = {"title": payload.get("title"), "value": payload.get("value")}
        extra_headers: dict[str, str] = {}
        if "mint" in query:
            # EXP-FRONTIER-36287182510 (prereg.md section 5, "Critical modification
            # for this experiment"): the minted handle is published in the
            # RESPONSE BODY, in addition to the response header and the raw
            # server-side observation. This is what turns class (iii) from a
            # server-side plant into a real observable-channel problem: a value
            # an agent can read out of a prior response body and propagate.
            #
            # The body is the byte-identical non-mint PUT body PLUS the
            # ``capability_handle`` field, so every non-mint request shape keeps
            # its exact response bytes and CTRL-REPL-PARENT-NUMBERS (which runs
            # the reference arm with the class-(iii) plant disabled) is
            # unaffected. The handle is a pure function of (MINT_SALT, episode
            # counter) and is still never a function of the store, of the request
            # path, of the resource identity or of the plan.
            handle = mint_token(int(self.server.episode_counter))  # type: ignore[attr-defined]
            self.server.last_mint = handle  # type: ignore[attr-defined]
            extra_headers["X-Capability-Handle"] = handle
            response_payload: dict[str, Any] = {
                "rid": rid,
                "created": not existed,
                "record": self.store[rid],
                "capability_handle": handle,
            }
            self._send(200 if existed else 201, response_payload, extra_headers)
            return
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
        # Episode counter: advanced by ``reset()`` only, never by a request, and
        # never part of the resource store or of any response body. It is the
        # only episode-varying input to the opt-in capability mint.
        self._server.episode_counter = 0  # type: ignore[attr-defined]
        self._server.last_mint = None  # type: ignore[attr-defined]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self.port = int(self._server.server_address[1])

    # -- raw observation channel (class-(iii) construction) ------------------
    @property
    def episode_counter(self) -> int:
        """Current episode counter. NOT part of the observable state."""
        return int(self._server.episode_counter)  # type: ignore[attr-defined]

    @property
    def last_mint(self) -> str | None:
        """Handle minted by the most recent ``PUT ...?mint=`` on this server.

        Raw observation of a prior response. Recorded by the runner as the only
        channel through which a class-(iii) binding key becomes available; it is
        never added to the observable state or to any arm's input.
        """
        return self._server.last_mint  # type: ignore[attr-defined]

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
        self._server.episode_counter = int(self._server.episode_counter) + 1  # type: ignore[attr-defined]
        self._server.last_mint = None  # type: ignore[attr-defined]

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
