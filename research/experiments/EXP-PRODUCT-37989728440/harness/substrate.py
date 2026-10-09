"""Redesigned credential-free localhost stdlib-HTTP substrate for EXP-PRODUCT-37989728440.

This is the mandatory-discovery substrate required by the frozen prereg section 3.
Unlike the two prior deterministic one-request GET substrates, the task
specification here is HIGH-LEVEL INTENT ONLY: the agent is told WHICH resource
type to mutate and WHICH property to set, but the session token, the valid
resource identifier and (at the highest novelty) the update endpoint variant
must be discovered with explicit HTTP discovery requests.

Frozen requirements implemented here (spec.json.measurement_validity):
  * credential-free, stdlib only, localhost 127.0.0.1, deterministic (SEED=42);
  * two task families F1 (documents/records) and F2 (widgets/gadgets);
  * four novelty levels 0.0 / 0.25 / 0.5 / 0.75 with genuine gradient;
  * correct action NOT fully determined by the task spec at high novelty;
  * real HTTP request/response cycles, no synthetic in-memory shortcut.

Server contract (frozen prereg section 3.4):
  GET  /api/session               -> {"session_token": ..., "expires": ...}
  GET  /api/resources             -> {"resources": [{"id","type","schema"}...]}
  GET  /api/schema/<type>         -> {"type","update_path","params","rev"}
  POST /api/<type>/<id>/update    -> {"success": true, ...}   (valid token/id/property/rev)
"""

from __future__ import annotations

import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from urllib import error, parse, request

SEED = 42

# Frozen task families (prereg section 3.5).
FAMILIES: dict[str, dict[str, Any]] = {
    "F1": {
        "types": {"documents": "doc", "records": "rec"},
        "properties": ["status", "priority", "owner"],
    },
    "F2": {
        "types": {"widgets": "wid", "gadgets": "gad"},
        "properties": ["config", "metadata", "tags"],
    },
}

NOVELTY_LEVELS: list[float] = [0.0, 0.25, 0.5, 0.75]
# Frozen novelty semantics (prereg section 3.3).
#   novelty   token_required  token_mode   id_provided  endpoint_provided
#   0.00      False           fixed        True         True
#   0.25      True            seed_fixed   True         True
#   0.50      True            rotating     False        True
#   0.75      True            rotating     False        False
NOVELTY_SEMANTICS: dict[float, dict[str, Any]] = {
    # token_mode "per_task" keeps training tokens varying so the kernel can
    # induce a session_token parameter slot (prereg section 4.1); the token is
    # still not *required* at novelty 0.0.
    0.0: {"token_required": False, "token_mode": "per_task", "id_provided": True, "endpoint_provided": True},
    0.25: {"token_required": True, "token_mode": "seed_fixed", "id_provided": True, "endpoint_provided": True},
    0.5: {"token_required": True, "token_mode": "rotating", "id_provided": False, "endpoint_provided": True},
    0.75: {"token_required": True, "token_mode": "rotating", "id_provided": False, "endpoint_provided": False},
}

TASKS_PER_LEVEL = 5
TRAIN_TASKS_PER_FAMILY = 10
UPDATE_PATH = "/api/{type}/{id}/update"


def _token(task_key: str, mode: str) -> str:
    if mode == "seed_fixed":
        raw = f"{SEED}:seed-fixed"
    else:
        raw = f"{SEED}:{task_key}"
    return "tok-" + hashlib.sha256(raw.encode()).hexdigest()[:16]


def _rev(task_key: str) -> str:
    return "r" + hashlib.sha256((task_key + ":rev").encode()).hexdigest()[:8]


def _in_support_id(prefix: str, digits2: int) -> str:
    """A ``prefix-0NN`` identifier that lies inside the induced support grammar.

    Declared support target from prereg section 8 is ``^<type>-0[0-9]{2}$``; the
    grammar is induced by the kernel from two-digit training remains that share
    the ``-0`` literal prefix. Both provided and session-discovered identifiers
    are drawn from this grammar so that novelty is about *discovery*, not about
    stepping outside the inferred support (the parent experiment's collapse).
    """
    return f"{prefix}-0{digits2:02d}"


def _discovered_digits(task_key: str) -> int:
    """Deterministic per-task two-digit value in 10..98 (never collides with 00)."""
    raw = int(hashlib.sha256(("discover:" + task_key).encode()).hexdigest(), 16)
    return 10 + (raw % 89)


def build_train_tasks() -> list[dict[str, Any]]:
    """Ten fully-specified training tasks per family at novelty 0.0.

    Five per resource type, with two-digit identifier remains that share the
    ``-0`` prefix, so ``_infer_support`` induces ``^<type>-0[0-9]{2}$`` exactly
    (prereg section 8 mitigation).
    """
    tasks: list[dict[str, Any]] = []
    for family, cfg in FAMILIES.items():
        types = sorted(cfg["types"].keys())
        for rtype in types:
            prefix = cfg["types"][rtype]
            for j in range(5):
                idx = (types.index(rtype) * 5) + j
                prop = cfg["properties"][idx % len(cfg["properties"])]
                rid = _in_support_id(prefix, (j + 1) * 11)  # 011,022,033,044,055
                key = f"train::{family}::{rtype}::{j}"
                spec = {
                    "intent": "update_resource",
                    "family": family,
                    "resource_type": rtype,
                    "target_property": prop,
                    # Given (not discovered) payload value, kept inside the
                    # regime from which the kernel induces a value-slot support so
                    # that mechanism binding is actually exercised (prereg section
                    # 8 support-boundary mitigation); value format is not the
                    # residual-novelty axis.
                    "target_value": f"draft-{j}",
                    "identifier": rid,
                    "endpoint": UPDATE_PATH,
                }
                tasks.append({
                    "task_id": key,
                    "family": family,
                    "resource_type": rtype,
                    "novelty_fraction": 0.0,
                    "spec": spec,
                    "phase": "training",
                    "target_identifier": rid,
                })
    return tasks


def build_test_tasks() -> list[dict[str, Any]]:
    """Five held-out tasks per family per novelty level (40 tasks total)."""
    tasks: list[dict[str, Any]] = []
    for family, cfg in FAMILIES.items():
        types = sorted(cfg["types"].keys())
        for novelty in NOVELTY_LEVELS:
            sem = NOVELTY_SEMANTICS[novelty]
            for i in range(TASKS_PER_LEVEL):
                rtype = types[i % len(types)]
                prop = cfg["properties"][i % len(cfg["properties"])]
                key = f"test::{family}::{novelty}::{i}"
                prefix = cfg["types"][rtype]
                if sem["id_provided"]:
                    rid = _in_support_id(prefix, (i + 1) * 13)  # 013,026,039,052,065
                else:
                    # Session-scoped identifier: NOT in the task spec, must be
                    # discovered via GET /api/resources, still inside support.
                    rid = _in_support_id(prefix, _discovered_digits(key))
                spec: dict[str, Any] = {
                    "intent": "update_resource",
                    "family": family,
                    "resource_type": rtype,
                    "target_property": prop,
                    # Held-out but support-respecting payload value (5..9, never
                    # a training value 0..4); keeps the given-value binding inside
                    # the inferred value-slot support.
                    "target_value": f"draft-{5 + i}",
                }
                if sem["id_provided"]:
                    spec["identifier"] = rid
                if sem["endpoint_provided"]:
                    spec["endpoint"] = UPDATE_PATH
                tasks.append({
                    "task_id": key,
                    "family": family,
                    "resource_type": rtype,
                    "novelty_fraction": novelty,
                    "spec": spec,
                    "phase": "test",
                    "target_identifier": rid,
                })
    return tasks


def build_scenario(task: dict[str, Any]) -> dict[str, Any]:
    """Deterministically instantiate the server-side state for one task."""
    family = task["family"]
    cfg = FAMILIES[family]
    sem = NOVELTY_SEMANTICS[task["novelty_fraction"]]
    key = task["task_id"]
    rtype = task["resource_type"]
    target_id = task["target_identifier"]
    token = _token(key, sem["token_mode"])
    resources: list[dict[str, Any]] = [
        {
            "id": target_id,
            "type": rtype,
            "schema": {"properties": list(cfg["properties"]), "shape": "flat" if family == "F1" else "nested"},
        }
    ]
    # One distractor resource of the other type in the same family.
    other_type = sorted(t for t in cfg["types"] if t != rtype)[0]
    resources.append({
        "id": f"{cfg['types'][other_type]}-distractor-001",
        "type": other_type,
        "schema": {"properties": list(cfg["properties"]), "shape": "flat" if family == "F1" else "nested"},
    })
    scenario: dict[str, Any] = {
        "task_id": key,
        "family": family,
        "novelty": task["novelty_fraction"],
        "resource_type": rtype,
        "token_required": sem["token_required"],
        "token": token,
        "resources": resources,
        "target": {
            "type": rtype,
            "id": target_id,
            "property": task["spec"]["target_property"],
            "value": task["spec"]["target_value"],
        },
        "update_path": UPDATE_PATH,
        "rev": _rev(key) if not sem["endpoint_provided"] else None,
        "rev_required": not sem["endpoint_provided"],
        "applied": None,
    }
    return scenario


class _Handler(BaseHTTPRequestHandler):
    server_version = "SpiderDiscoverySubstrate/1.0"
    sys_version = ""

    def log_message(self, fmt: str, *args: Any) -> None:  # silence stderr
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
        scenario = self.server.scenario  # type: ignore[attr-defined]
        entry = {
            "seq": self.server.next_seq(),  # type: ignore[attr-defined]
            "method": self.command,
            "path": self.path,
            "status": status,
            "request_id": request_id,
            "task_id": scenario.get("task_id") if scenario else None,
        }
        if extra:
            entry.update(extra)
        self.server.request_log.append(entry)  # type: ignore[attr-defined]

    def _parse(self) -> tuple[str | None, str | None, str | None]:
        path = self.path.split("?", 1)[0]
        parts = path.strip("/").split("/")
        query = parse.parse_qs(parse.urlparse(self.path).query)
        q0 = query.get("rev", [None])[0]
        if len(parts) == 2 and parts[0] == "api":
            return parts[1], None, q0
        if len(parts) == 3 and parts[0] == "api":
            return parts[1], parts[2], q0
        # POST /api/<type>/<id>/update
        if len(parts) == 4 and parts[0] == "api" and parts[3] == "update":
            return parts[1], parts[2], q0
        return None, None, q0

    def _rid(self, salt: str) -> str:
        return hashlib.sha256((salt + self.path).encode()).hexdigest()[:16]

    # -- routes ----------------------------------------------------------
    def do_GET(self) -> None:  # noqa: N802
        scenario = self.server.scenario  # type: ignore[attr-defined]
        seg1, seg2, _ = self._parse()
        rid = self._rid("GET")
        if scenario is None:
            self._send_json(503, {"error": "no scenario"}, rid)
            self._record(503, rid)
            return
        if seg1 == "session":
            self._send_json(200, {"session_token": scenario["token"], "expires": 9999999999}, rid)
            self._record(200, rid, {"route": "session"})
            return
        if seg1 == "resources":
            self._send_json(200, {"resources": scenario["resources"]}, rid)
            self._record(200, rid, {"route": "resources"})
            return
        if seg1 == "schema" and seg2 is not None:
            payload = {
                "type": seg2,
                "update_path": scenario["update_path"],
                "params": ["property", "value"],
                "rev": scenario["rev"],
            }
            self._send_json(200, payload, rid)
            self._record(200, rid, {"route": "schema", "resource_type": seg2})
            return
        self._send_json(404, {"error": "not found", "path": self.path}, rid)
        self._record(404, rid)

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length else b""
        scenario = self.server.scenario  # type: ignore[attr-defined]
        rid = self._rid("POST")
        seg1, seg2, rev = self._parse()
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send_json(400, {"error": "bad json"}, rid)
            self._record(400, rid)
            return
        if scenario is None:
            self._send_json(503, {"error": "no scenario"}, rid)
            self._record(503, rid)
            return
        token = self.headers.get("X-Session-Token")
        if scenario["token_required"] and token != scenario["token"]:
            self._send_json(401, {"error": "invalid or missing session token"}, rid)
            self._record(401, rid, {"route": "update", "reason": "token"})
            return
        resources = scenario["resources"]
        match = next((r for r in resources if r["id"] == seg2 and r["type"] == seg1), None)
        if match is None:
            self._send_json(404, {"error": "unknown resource id/type"}, rid)
            self._record(404, rid, {"route": "update", "reason": "id"})
            return
        if scenario["rev_required"] and rev != scenario["rev"]:
            self._send_json(422, {"error": "endpoint variant rev missing/mismatch"}, rid)
            self._record(422, rid, {"route": "update", "reason": "rev"})
            return
        prop = payload.get("property")
        value = payload.get("value")
        if not isinstance(prop, str) or not prop:
            self._send_json(422, {"error": "property required"}, rid)
            self._record(422, rid, {"route": "update", "reason": "property"})
            return
        applied = {"type": seg1, "id": seg2, "property": prop, "value": value}
        scenario["applied"] = applied
        self._send_json(200, {"success": True, **applied}, rid)
        self._record(200, rid, {"route": "update", **applied})


class SubstrateServer:
    """Single-request-at-a-time HTTPServer bound to an ephemeral localhost port."""

    def __init__(self) -> None:
        self.scenario: dict[str, Any] | None = None
        self.request_log: list[dict[str, Any]] = []
        self._seq = 0
        self._lock = threading.Lock()
        self.httpd = HTTPServer(("127.0.0.1", 0), _Handler)
        self.httpd.scenario = None  # type: ignore[attr-defined]
        self.httpd.request_log = self.request_log  # type: ignore[attr-defined]
        self.httpd.next_seq = self._next_seq  # type: ignore[attr-defined]
        self.host, self.port = self.httpd.server_address
        self.base_url = f"http://{self.host}:{self.port}"
        self._thread: threading.Thread | None = None

    def _next_seq(self) -> int:
        with self._lock:
            self._seq += 1
            return self._seq

    def set_scenario(self, scenario: dict[str, Any]) -> None:
        self.scenario = scenario
        self.httpd.scenario = scenario  # type: ignore[attr-defined]

    def start(self) -> None:
        self._thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)


class SubstrateClient:
    """Credential-free HTTP client over urllib; every call is a real request."""

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def execute(self, action: dict[str, Any]) -> dict[str, Any]:
        method = action.get("method", "GET")
        url = action.get("url")
        if not isinstance(url, str):
            return {"status": None, "error": "no url in action", "body": None, "headers": {}}
        headers = dict(action.get("headers") or {})
        data = None
        if "json" in action:
            data = json.dumps(action["json"]).encode()
            headers.setdefault("Content-Type", "application/json")
        req = request.Request(url, data=data, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:  # noqa: S310 localhost only
                raw = resp.read()
                status = resp.status
                response_headers = {k: v for k, v in resp.getheaders()}
        except error.HTTPError as exc:
            raw = exc.read()
            status = exc.code
            response_headers = {k: v for k, v in exc.headers.items()}
        except error.URLError as exc:  # pragma: no cover infrastructure only
            return {"status": None, "error": str(exc), "body": None, "headers": {}}
        body: Any
        try:
            body = json.loads(raw.decode("utf-8")) if raw else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            body = raw.decode("utf-8", "replace")
        return {"status": status, "body": body, "headers": response_headers}
