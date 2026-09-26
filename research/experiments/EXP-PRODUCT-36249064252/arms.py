"""Arms, clients and task model for EXP-PRODUCT-36249064252.

Everything here is experiment apparatus. The only product code exercised is
``src/spider/kernel.py``. Each arm is declared with an explicit, fixed candidate
policy so that the auditor can check that no baseline was weakened or rigged.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Sequence

TRAINING_LABEL = "catalog-default"
OWNER_TOKEN = "tok-owner-a"
VIEWER_TOKEN = "tok-viewer-a"

#: Fixed, declared generic REST-convention probe policy for the cold baseline.
#: It is NOT tuned to this substrate: it is the ordinary "I know the collection,
#: the identifier and the verb, but not this API's exact shape" prior.
COLD_WRITE_CANDIDATES: tuple[tuple[str, str, Any], ...] = (
    ("POST", "/{collection}", {"id": "{id}", "label": TRAINING_LABEL}),
    ("PUT", "/{collection}/{id}", {"label": TRAINING_LABEL}),
    ("DELETE", "/{collection}/{id}", None),
    ("POST", "/{collection}/{id}", {"id": "{id}", "label": TRAINING_LABEL}),
    ("PATCH", "/{collection}/{id}", {"label": TRAINING_LABEL}),
    ("PUT", "/{collection}", {"id": "{id}", "label": TRAINING_LABEL}),
)
COLD_READ_CANDIDATES: tuple[tuple[str, str, Any], ...] = (
    ("GET", "/{collection}/{id}", None),
    ("GET", "/{collection}?q={id}&limit=1", None),
    ("GET", "/{collection}?id={id}", None),
    ("GET", "/api/{collection}/{id}", None),
    ("GET", "/{id}", None),
    ("GET", "/{collection}/{id}/", None),
)
COLD_QUERY_CANDIDATES: tuple[tuple[str, str, Any], ...] = (
    ("GET", "/{collection}?q={q}&limit={limit}", None),
    ("GET", "/{collection}", None),
    ("GET", "/{collection}?limit={limit}", None),
    ("GET", "/api/{collection}?q={q}&limit={limit}", None),
    ("GET", "/{collection}?q=&limit={limit}", None),
    ("GET", "/{collection}?q={q}", None),
)


# --------------------------------------------------------------------------- #
# Instrumented HTTP client
# --------------------------------------------------------------------------- #


@dataclass
class Wire:
    requests: int = 0
    response_bytes: int = 0
    request_bytes: int = 0
    statuses: list[int] = field(default_factory=list)

    def merge(self, other: "Wire") -> None:
        self.requests += other.requests
        self.response_bytes += other.response_bytes
        self.request_bytes += other.request_bytes
        self.statuses.extend(other.statuses)


@dataclass
class Response:
    status: int
    body: bytes
    headers: dict[str, str]


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.total = Wire()

    def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        token: str = OWNER_TOKEN,
        headers: dict[str, str] | None = None,
    ) -> tuple[Response, Wire]:
        wire = Wire()
        data = json.dumps(body).encode() if body is not None else None
        wire.requests = 1
        wire.request_bytes = len(data or b"")
        request = urllib.request.Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {token}",
                **({"Content-Type": "application/json"} if data else {}),
                **(headers or {}),
            },
        )
        try:
            with urllib.request.urlopen(request) as raw:
                response = Response(raw.status, raw.read(), dict(raw.headers))
        except urllib.error.HTTPError as error:
            response = Response(error.code, error.read(), dict(error.headers))
        wire.response_bytes = len(response.body)
        wire.statuses = [response.status]
        self.total.merge(wire)
        return response, wire

    def get_json(self, path: str, token: str = OWNER_TOKEN) -> Any:
        response, _ = self.request("GET", path, token=token)
        try:
            return json.loads(response.body.decode())
        except (ValueError, UnicodeDecodeError):
            return None


# --------------------------------------------------------------------------- #
# Task model
# --------------------------------------------------------------------------- #

FAMILIES = ("crud-write", "crud-read", "query")


@dataclass(frozen=True)
class Task:
    task_id: str
    family: str
    intent: str
    collection: str
    identifier: str | None
    query_term: str | None
    query_limit: int | None
    role: str = "owner"
    resource: str = "B"

    def context(self) -> dict[str, Any]:
        return {
            "auth": "valid_token",
            "role": self.role,
            "collection": self.collection,
            "session_id": "sess-current",
        }

    def token(self) -> str:
        return OWNER_TOKEN if self.role == "owner" else VIEWER_TOKEN

    def params(self, slots: Iterable[str] = ()) -> dict[str, Any]:
        """Binding values a caller can legitimately know for this task."""
        out: dict[str, Any] = {"collection": self.collection, "auth_token": self.token()}
        if self.identifier is not None:
            out["id"] = self.identifier
        if self.query_term is not None:
            out["q"] = self.query_term
        if self.query_limit is not None:
            out["limit"] = self.query_limit
        for slot in slots:
            out.setdefault(slot, "")
        return out


@dataclass
class TaskResult:
    task_id: str
    arm: str
    family: str
    intent: str
    resolution_status: str
    resolution_reason: str
    mechanism_id: str | None
    confidence: float
    bound_action: dict[str, Any] | None
    executed: bool
    fallback_used: bool
    success: bool
    postcondition_ok: bool
    semantic_correct: bool
    binding_correct: bool | None
    verified: bool
    requests: int
    response_bytes: int
    request_bytes: int
    kernel_calls: int
    wall_ms: float
    trace: list[dict[str, Any]] = field(default_factory=list)
    note: str = ""


# --------------------------------------------------------------------------- #
# Shared execution helpers
# --------------------------------------------------------------------------- #


def _path_and_query(action: dict[str, Any]) -> str:
    path = action.get("path") or action.get("url") or "/"
    query = action.get("query") or {}
    if query:
        path = f"{path}?{urllib.parse.urlencode(query)}"
    return path


def _substitute(template: str, values: dict[str, Any]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def _postcondition(action_response: Any, status: int) -> dict[str, Any]:
    """Method-level postcondition actually observed, in the kernel's vocabulary."""
    resource_present = False
    if isinstance(action_response, dict):
        if status == 304:
            resource_present = True
        elif "deleted" in action_response:
            resource_present = bool(action_response.get("deleted"))
        elif "rows" in action_response:
            resource_present = int(action_response.get("count", 0)) > 0
        elif "id" in action_response:
            resource_present = True
    return {"status": status, "ok": 200 <= status < 300, "resource_present": resource_present}


def semantic_check(task: Task, payload: Any) -> bool:
    """Stricter than 2xx: did the response actually concern the requested entity?"""
    if not isinstance(payload, dict):
        return False
    if task.intent == "list":
        rows = payload.get("rows")
        limit = task.query_limit
        if not isinstance(rows, list) or not rows:
            return False
        if limit is not None and len(rows) > limit:
            return False
        term = task.query_term or ""
        return all(term in str(row.get("id", "")) or term in str(row.get("label", "")) for row in rows)
    if task.identifier is not None:
        return str(payload.get("id", task.identifier)) == task.identifier
    return bool(payload)


# --------------------------------------------------------------------------- #
# Cold exploration (shared fallback)
# --------------------------------------------------------------------------- #


def cold_candidates(task: Task) -> tuple[tuple[str, str, Any], ...]:
    if task.intent in ("create", "update", "delete"):
        return COLD_WRITE_CANDIDATES
    if task.intent == "read":
        return COLD_READ_CANDIDATES
    return COLD_QUERY_CANDIDATES


def run_cold(
    client: Client,
    task: Task,
    kernel_verify: Callable[[str, dict[str, Any]], bool] | None,
    mechanism_id: str | None = None,
) -> dict[str, Any]:
    """Blind discovery: probe the declared candidate policy until the postcondition holds."""
    values = {
        "collection": task.collection,
        "id": task.identifier or "",
        "q": task.query_term or "",
        "limit": task.query_limit if task.query_limit is not None else 1,
    }
    trace: list[dict[str, Any]] = []
    wire = Wire()
    for method, template, body in cold_candidates(task):
        path = _substitute(template, values)
        resolved_body = _substitute_keys(body, values) if body is not None else None
        response, used = client.request(method, path, resolved_body, token=task.token())
        wire.merge(used)
        try:
            payload = json.loads(response.body.decode())
        except (ValueError, UnicodeDecodeError):
            payload = None
        observed = _postcondition(payload, response.status)
        verified = bool(kernel_verify(mechanism_id, observed)) if kernel_verify and mechanism_id else observed["ok"] and observed["resource_present"]
        trace.append(
            {
                "method": method,
                "path": path,
                "status": response.status,
                "response_bytes": used.response_bytes,
                "postcondition": observed,
                "solved": bool(verified and semantic_check(task, payload)),
            }
        )
        if verified and semantic_check(task, payload):
            return {
                "success": True,
                "postcondition_ok": True,
                "semantic_correct": True,
                "verified": True,
                "trace": trace,
                "wire": wire,
                "bound_action": {"method": method, "path": path, "body": resolved_body},
            }
    return {
        "success": False,
        "postcondition_ok": False,
        "semantic_correct": False,
        "verified": False,
        "trace": trace,
        "wire": wire,
        "bound_action": None,
    }


def _substitute_keys(body: Any, values: dict[str, Any]) -> Any:
    if isinstance(body, dict):
        return {key: _substitute_keys(value, values) for key, value in body.items()}
    if isinstance(body, str):
        return _substitute(body, values)
    return body


# --------------------------------------------------------------------------- #
# Deterministic hashed-embedding retrieval baseline (B-RETRIEVAL-K5)
# --------------------------------------------------------------------------- #

_EMBED_DIM = 512


def embed(text: str) -> dict[int, float]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    vector: dict[int, float] = {}
    for token in tokens:
        bucket = int(hashlib.sha256(token.encode()).hexdigest()[:8], 16) % _EMBED_DIM
        vector[bucket] = vector.get(bucket, 0.0) + 1.0
    norm = math.sqrt(sum(value * value for value in vector.values())) or 1.0
    return {key: value / norm for key, value in vector.items()}


def cosine(left: dict[int, float], right: dict[int, float]) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(key, 0.0) for key, value in left.items())


def observation_text(observation: Any) -> str:
    action = observation.action
    query = action.get("query") or {}
    return " ".join(
        [
            observation.intent,
            str(action.get("method", "")),
            str(action.get("path", "")),
            " ".join(f"{k}={v}" for k, v in sorted(query.items())),
            str(observation.state.get("collection", "")),
            str(observation.provenance.get("identifier", "")),
        ]
    )


def task_text(task: Task) -> str:
    return " ".join(
        [
            task.intent,
            {"create": "POST", "read": "GET", "update": "PUT", "delete": "DELETE", "list": "GET"}[task.intent],
            f"/{task.collection}",
            f"q={task.query_term}" if task.query_term else "",
            f"limit={task.query_limit}" if task.query_limit is not None else "",
            str(task.identifier or ""),
        ]
    )


def retrieve(query: str, store: Sequence[tuple[str, Any]], k: int = 5) -> list[tuple[float, Any]]:
    vector = embed(query)
    scored = [(cosine(vector, embed(text)), item) for text, item in store]
    scored.sort(key=lambda pair: (-pair[0], pair[1].provenance.get("identifier", "")))
    return scored[:k]


def _swap_in_strings(value: Any, old: str, new: str) -> Any:
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, dict):
        return {k: _swap_in_strings(v, old, new) for k, v in value.items()}
    if isinstance(value, list):
        return [_swap_in_strings(v, old, new) for v in value]
    return value


def retrieval_bind(observation: Any, task: Task, *, align_collection: bool) -> dict[str, Any] | None:
    """Heuristic slot matching: copy the retrieved example and swap the entity token.

    ``align_collection=False`` is the frozen B-RETRIEVAL-K5 behaviour (entity swap
    only). ``align_collection=True`` is the strengthened diagnostic variant that
    additionally realigns the collection token using the retrieved observation's own
    recorded context field.
    """
    a_id = str(observation.provenance.get("identifier") or "")
    b_id = task.identifier or task.query_term or ""
    if not a_id or not b_id:
        return None
    action = {k: v for k, v in observation.action.items() if k in ("method", "path", "body", "query")}
    bound = _swap_in_strings(action, a_id, b_id)
    if align_collection:
        a_collection = str(observation.state.get("collection") or "")
        if a_collection and a_collection != task.collection:
            bound = _swap_in_strings(bound, f"/{a_collection}", f"/{task.collection}")
    return bound
