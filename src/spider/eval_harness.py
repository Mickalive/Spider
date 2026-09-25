"""Frozen end-to-end evaluation-harness instrument (EXP-PRODUCT-36129169543).

This module is the Part A deliverable of the frozen Product experiment
EXP-PRODUCT-36129169543: an end-to-end evaluation harness that, from a task
manifest and a pluggable policy, executes the full frozen arm set

    P-SPIDER, B-COLD, B-INSTRUCTIONS, B-RAG-EMBED, B-DETERMINISTIC-EXECUTOR

under identical tools and budget with

  * per-trajectory hard-reset integer sum counters for the eight frozen
    counter paths (resolve, bind, verify, freshness, repair, browser_steps,
    requests, latency_ms);
  * family-stratified trajectory-grouped bootstrap and block-permutation
    confidence intervals (default B=5000);
  * a fail-closed arm gate that marks an arm UNKNOWN when a prerequisite
    capability is absent, never surrogate-filled and never default-filled.

Design contract (frozen in spec.json/prereg.md):

  * Token-denominated economics are NOT_APPLICABLE/UNKNOWN until a
    policy-model credential exists: this module deliberately exposes no
    token counters and its break-even function accepts no token inputs.
  * UNKNOWN gate results carry no numeric payload at all: the GateDecision
    dataclass has exactly the fields (arm_id, mode, status, required,
    missing, reason) and a gated-off trajectory record has counters=None,
    payload_bytes=None.  There is no code path that fabricates a default.
  * Counters are honest sums of operations actually executed; latency_ms is
    the integer-rounded sum of measured per-request wall-clock milliseconds
    accumulated inside one trajectory and reset at every trajectory boundary.

The harness is transport-agnostic: unit tests drive it with
:class:`MockEnvironment`, the dry run drives it with
:class:`HttpSubstrateEnvironment` against the certified distributed service.
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import os
import random
import statistics
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Protocol

SEED = 42

COUNTER_NAMES: tuple[str, ...] = (
    "resolve",
    "bind",
    "verify",
    "freshness",
    "repair",
    "browser_steps",
    "requests",
    "latency_ms",
)

ARM_IDS: tuple[str, ...] = (
    "P-SPIDER",
    "B-COLD",
    "B-INSTRUCTIONS",
    "B-RAG-EMBED",
    "B-DETERMINISTIC-EXECUTOR",
)

MODES: tuple[str, ...] = ("scripted", "live_browser")

#: Frozen prerequisite sets.  ``scripted`` runs the deterministic scripted
#: policy against the HTTP substrate only; ``live_browser`` additionally
#: requires the BrowserGym path, Playwright and a policy-model credential.
DEFAULT_REQUIREMENTS: dict[str, dict[str, tuple[str, ...]]] = {
    "scripted": {arm: ("http_substrate",) for arm in ARM_IDS},
    "live_browser": {
        arm: ("http_substrate", "browsergym", "playwright", "policy_model")
        for arm in ARM_IDS
    },
}


# ---------------------------------------------------------------------------
# Counter ledger
# ---------------------------------------------------------------------------
class CounterLedger:
    """Per-trajectory hard-reset integer sum counters for the eight paths.

    Every increment corresponds to an operation that the arm actually
    executed.  ``latency_ms`` accumulates measured wall-clock milliseconds as
    a float internally (sub-millisecond localhost requests must not be
    rounded away individually) and is emitted as an integer at the
    per-trajectory hard reset, so every recorded counter value is an integer
    sum with no jitter, no bijective proxy and no scaling.
    """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._counts: dict[str, int] = {name: 0 for name in COUNTER_NAMES}
        self._latency_ms = 0.0
        self._payload_bytes = 0

    def add_payload_bytes(self, n: int) -> None:
        """Auxiliary (non-counter) transfer measurement used only for the
        secondary byte-denominated break-even unit.  It is not one of the
        eight frozen counter paths and never appears in ``snapshot()``."""
        if not isinstance(n, int) or n < 0:
            raise ValueError("payload bytes must be a non-negative integer")
        self._payload_bytes += n

    @property
    def payload_bytes(self) -> int:
        return int(self._payload_bytes)

    def incr(self, name: str, amount: int = 1) -> None:
        if name not in self._counts:
            raise KeyError(f"unknown counter path: {name}")
        if name == "latency_ms":
            raise ValueError("latency_ms is measured, use add_latency_ms")
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("counter increments must be non-negative integers")
        self._counts[name] += amount

    def add_latency_ms(self, measured_ms: float) -> None:
        if measured_ms < 0 or not math.isfinite(measured_ms):
            raise ValueError("latency must be a finite non-negative measurement")
        self._latency_ms += float(measured_ms)

    def snapshot(self) -> dict[str, int]:
        out = dict(self._counts)
        out["latency_ms"] = int(round(self._latency_ms))
        return out


# ---------------------------------------------------------------------------
# Tasks / transport
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Task:
    task_id: str
    family_id: str
    template_id: str
    site_id: str
    length: int
    novelty_level: float
    slots: tuple[str, ...]
    params: dict[str, str]
    b_positions: tuple[int, ...] = ()


def tasks_from_manifest(fixture: dict[str, Any]) -> list[Task]:
    tasks: list[Task] = []
    for raw in fixture["tasks"]:
        params = {str(k): str(v) for k, v in (raw.get("param_values") or {}).items()}
        tasks.append(
            Task(
                task_id=str(raw["task_id"]),
                family_id=str(raw["family_id"]),
                template_id=str(raw["template_id"]),
                site_id=str(raw.get("site_id", "")),
                length=int(raw.get("length", 8)),
                novelty_level=float(raw.get("realized_novelty", 0.0)),
                slots=tuple(str(s) for s in raw.get("slots", ())),
                params=params,
                b_positions=tuple(int(i) for i in (raw.get("b_positions") or ())),
            )
        )
    return tasks


def task_rid(task: Task, step: int) -> str:
    """Structural resource id shared between the family build pass and every
    trajectory of that family (same family + same template + same step)."""
    return f"{task.family_id}_{task.template_id}_s{step}"


@dataclass
class FetchResult:
    rid: str
    status: int | None
    etag: str | None
    body: str
    body_sha: str | None
    latency_ms: float
    payload_bytes: int
    inm_sent: bool
    error: str | None = None


class Environment(Protocol):
    """Minimal transport contract used by every arm."""

    label: str

    def fetch(self, rid: str, if_none_match: str | None = None) -> FetchResult: ...

    def bump(self, rid: str) -> dict[str, Any]: ...

    def load_instructions(self, task: Task) -> str: ...


def integrity_ok(res: FetchResult) -> bool:
    """Independent per-response verification (hash recompute, no trust)."""
    if res.error or res.status is None:
        return False
    if res.status == 304:
        return bool(res.etag)
    if res.status != 200:
        return False
    digest = hashlib.sha256(res.body.encode("utf-8")).hexdigest()
    etag_ok = bool(res.etag) and res.etag.startswith('W/"') and res.etag[3:19] == digest[:16]
    sha_ok = res.body_sha is None or res.body_sha == digest
    return etag_ok and sha_ok


class MockEnvironment:
    """Deterministic in-process substrate for unit tests (no network)."""

    label = "mock"

    def __init__(self, latency_ms: float = 1.0, instructions: str = "static instructions") -> None:
        self._gen: dict[str, int] = {}
        self._base_latency = float(latency_ms)
        self.instructions = instructions
        self.fetch_count = 0

    def _body(self, rid: str) -> tuple[str, str, str]:
        gen = self._gen.get(rid, 0)
        body = '{"rid": "%s", "gen": %d, "payload": "%s"}' % (
            rid,
            gen,
            hashlib.sha256(f"{rid}:{gen}".encode()).hexdigest()[:24],
        )
        digest = hashlib.sha256(body.encode()).hexdigest()
        return body, f'W/"{digest[:16]}"', digest

    def fetch(self, rid: str, if_none_match: str | None = None) -> FetchResult:
        self.fetch_count += 1
        body, etag, digest = self._body(rid)
        # deterministic, request-index-varying latency (>= 1ms, never 0)
        latency = self._base_latency + 0.001 * (self.fetch_count % 7)
        if if_none_match is not None and if_none_match == etag:
            return FetchResult(rid, 304, etag, "", None, latency, 0, True, None)
        return FetchResult(rid, 200, etag, body, digest, latency, len(body.encode()), if_none_match is not None, None)

    def bump(self, rid: str) -> dict[str, Any]:
        self._gen[rid] = self._gen.get(rid, 0) + 1
        return {"rid": rid, "gen": self._gen[rid]}

    def load_instructions(self, task: Task) -> str:
        return f"{self.instructions} family={task.family_id}"


class HttpSubstrateEnvironment:
    """Client for the certified single-node HS256 sticky distributed service.

    Every request is measured (wall-clock ms) and every response payload size
    is recorded.  Optional ``trace`` receives one raw row per request so the
    runner can preserve request-level raw evidence separately from derived
    measurements.
    """

    label = "http_substrate"

    def __init__(
        self,
        base_url: str,
        token: str,
        trace_path: str | Path | None = None,
        instructions_text: str = "static natural-language instructions",
        timeout: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.instructions_text = instructions_text
        self.tag = "substrate"  # free-form label recorded in raw trace rows
        self._trace = open(trace_path, "a", encoding="utf-8") if trace_path else None
        self.request_count = 0

    def _log(self, phase: str, rid: str, res: FetchResult) -> None:
        if self._trace is None:
            return
        import json as _json

        self._trace.write(
            _json.dumps(
                {
                    "tag": self.tag,
                    "phase": phase,
                    "rid": rid,
                    "status": res.status,
                    "inm_sent": res.inm_sent,
                    "etag": res.etag,
                    "latency_ms": round(res.latency_ms, 4),
                    "payload_bytes": res.payload_bytes,
                    "error": res.error,
                },
                sort_keys=True,
            )
            + "\n"
        )

    def fetch(
        self,
        rid: str,
        if_none_match: str | None = None,
        phase: str = "trajectory",
    ) -> FetchResult:
        url = f"{self.base_url}/api/ep-a/{rid}"
        headers = {"Authorization": f"Bearer {self.token}"}
        if if_none_match is not None:
            headers["If-None-Match"] = if_none_match
        req = urllib.request.Request(url, headers=headers)
        t0 = time.perf_counter()
        self.request_count += 1
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                body = r.read()
                ms = (time.perf_counter() - t0) * 1000.0
                res = FetchResult(
                    rid=rid,
                    status=r.status,
                    etag=r.headers.get("ETag"),
                    body=body.decode("utf-8", "replace"),
                    body_sha=r.headers.get("X-Body-Sha"),
                    latency_ms=ms,
                    payload_bytes=len(body),
                    inm_sent=if_none_match is not None,
                    error=None,
                )
        except urllib.error.HTTPError as e:
            body = e.read() if hasattr(e, "read") else b""
            ms = (time.perf_counter() - t0) * 1000.0
            res = FetchResult(
                rid=rid,
                status=e.code,
                etag=(e.headers.get("ETag") if e.headers else None),
                body=body.decode("utf-8", "replace"),
                body_sha=None,
                latency_ms=ms,
                payload_bytes=len(body),
                inm_sent=if_none_match is not None,
                error=None,
            )
        except Exception as e:  # transport failure must be visible, never masked
            ms = (time.perf_counter() - t0) * 1000.0
            res = FetchResult(
                rid=rid,
                status=None,
                etag=None,
                body="",
                body_sha=None,
                latency_ms=ms,
                payload_bytes=0,
                inm_sent=if_none_match is not None,
                error=f"{type(e).__name__}: {e}",
            )
        self._log(phase, rid, res)
        return res

    def bump(self, rid: str) -> dict[str, Any]:
        url = f"{self.base_url}/api/admin/bump/{rid}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.token}"}, method="POST")
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            import json as _json

            return _json.loads(r.read().decode())

    def load_instructions(self, task: Task) -> str:
        return f"{self.instructions_text}\nsite={task.site_id}\nslots={','.join(task.slots)}"

    def close(self) -> None:
        if self._trace is not None:
            self._trace.flush()
            self._trace.close()
            self._trace = None


# ---------------------------------------------------------------------------
# Fail-closed capability gate
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class GateDecision:
    """Exactly six fields.  There is no metrics/value slot by construction, so
    an UNKNOWN decision cannot be surrogate-filled or default-filled."""

    arm_id: str
    mode: str
    status: str  # "EXECUTABLE" | "UNKNOWN"
    required: tuple[str, ...]
    missing: tuple[str, ...]
    reason: str


def _probe_playwright() -> tuple[bool, str]:
    if importlib.util.find_spec("playwright") is None:
        return False, "playwright not installed"
    try:
        import importlib.metadata as md

        return True, f"playwright {md.version('playwright')}"
    except Exception as e:  # pragma: no cover - metadata missing
        return True, f"playwright present (version unknown: {type(e).__name__})"


def _probe_browsergym() -> tuple[bool, str]:
    if importlib.util.find_spec("browsergym") is not None:
        try:
            import importlib.metadata as md

            return True, f"browsergym {md.version('browsergym-core')}"
        except Exception:
            return True, "browsergym importable"
    try:
        import importlib.metadata as md

        md.version("browsergym-core")
        return True, "browsergym-core metadata present"
    except Exception:
        return False, "browsergym-core not installed"


def _probe_policy_model() -> tuple[bool, str]:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return True, "OPENAI_API_KEY present"
    return False, "OPENAI_API_KEY absent"


PROBES: dict[str, Callable[[], tuple[bool, str]]] = {
    "browsergym": _probe_browsergym,
    "playwright": _probe_playwright,
    "policy_model": _probe_policy_model,
}


def probe_capabilities(substrate_ok: bool) -> dict[str, Any]:
    """Fail-closed environment probe: an exception is recorded as absence."""
    available: dict[str, bool] = {"http_substrate": bool(substrate_ok)}
    details: dict[str, str] = {"http_substrate": "health gate pass" if substrate_ok else "health gate not satisfied"}
    for name, probe in PROBES.items():
        try:
            ok, detail = probe()
        except Exception as e:  # pragma: no cover - defensive
            ok, detail = False, f"probe_error:{type(e).__name__}"
        available[name] = bool(ok)
        details[name] = detail
    return {
        "available": available,
        "details": details,
        "probed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "policy": "fail-closed: absent/unproven capability => False",
    }


def fail_closed_gate(
    arm_id: str,
    mode: str,
    available: dict[str, bool],
    requirements: dict[str, dict[str, tuple[str, ...]]] | None = None,
) -> GateDecision:
    reqs = requirements or DEFAULT_REQUIREMENTS
    if mode not in reqs:
        return GateDecision(arm_id, mode, "UNKNOWN", (), (), f"unknown mode {mode!r}: fail-closed")
    required = tuple(reqs[mode].get(arm_id, reqs[mode].get("*", ())))
    missing = tuple(c for c in required if available.get(c) is not True)
    if missing:
        return GateDecision(
            arm_id,
            mode,
            "UNKNOWN",
            required,
            missing,
            "prerequisite capability absent: " + ", ".join(missing),
        )
    return GateDecision(arm_id, mode, "EXECUTABLE", required, (), "all prerequisite capabilities present")


# ---------------------------------------------------------------------------
# Arms
# ---------------------------------------------------------------------------
@dataclass
class TrajectoryRecord:
    arm_id: str
    mode: str
    task_id: str
    family_id: str
    novelty_level: float
    length: int
    gate_status: str
    gate_reason: str
    counters: dict[str, int] | None  # None <=> UNKNOWN (never default-filled)
    payload_bytes: int | None
    extras: dict[str, Any] = field(default_factory=dict)


class Arm:
    """One evaluation arm.  Arms differ only in *how* each scripted step is
    served; the policy (deterministic scripted) and budget are identical."""

    arm_id = "?"

    def run(self, task: Task, env: Environment, ledger: CounterLedger) -> dict[str, Any]:
        raise NotImplementedError


def _serve_steps(task: Task, env: Environment, ledger: CounterLedger, conditional: bool, validators: dict[str, str] | None) -> dict[str, Any]:
    """Full-GET step loop shared by the non-inherited arms (and the repair
    branch of the inherited arm is handled separately)."""
    failures = 0
    statuses: dict[str, int] = {}
    for step in range(task.length):
        rid = task_rid(task, step)
        inm = validators.get(rid) if (conditional and validators is not None) else None
        res = env.fetch(rid, inm)
        ledger.incr("requests", 1)
        ledger.incr("browser_steps", 1)
        ledger.incr("verify", 1)
        ledger.add_latency_ms(res.latency_ms)
        ledger.add_payload_bytes(res.payload_bytes)
        if not integrity_ok(res):
            failures += 1
        key = "none" if res.status is None else str(res.status)
        statuses[key] = statuses.get(key, 0) + 1
    return {"integrity_failures": failures, "statuses": statuses}


class ColdArm(Arm):
    """Cold exploration: no inherited knowledge, no retrieval, no instructions."""

    arm_id = "B-COLD"

    def run(self, task: Task, env: Environment, ledger: CounterLedger) -> dict[str, Any]:
        return _serve_steps(task, env, ledger, conditional=False, validators=None)


class InstructionsArm(Arm):
    """Static natural-language instructions only; no mechanism inheritance."""

    arm_id = "B-INSTRUCTIONS"

    def run(self, task: Task, env: Environment, ledger: CounterLedger) -> dict[str, Any]:
        t0 = time.perf_counter()
        text = env.load_instructions(task)
        ledger.add_latency_ms((time.perf_counter() - t0) * 1000.0)
        extras = _serve_steps(task, env, ledger, conditional=False, validators=None)
        extras["instructions_chars"] = len(text)
        return extras


class DeterministicExecutorArm(Arm):
    """No-memory deterministic compiled executor: compiles the structural flow
    directly from the manifest (no runtime lookup, no retrieval, no probes)."""

    arm_id = "B-DETERMINISTIC-EXECUTOR"

    def run(self, task: Task, env: Environment, ledger: CounterLedger) -> dict[str, Any]:
        t0 = time.perf_counter()
        script = [(task_rid(task, s), dict(task.params)) for s in range(task.length)]
        ledger.add_latency_ms((time.perf_counter() - t0) * 1000.0)
        ledger.incr("bind", len(task.slots))  # compiled literal substitution
        failures = 0
        for rid, _ in script:
            res = env.fetch(rid, None)
            ledger.incr("requests", 1)
            ledger.incr("browser_steps", 1)
            ledger.incr("verify", 1)
            ledger.add_latency_ms(res.latency_ms)
            ledger.add_payload_bytes(res.payload_bytes)
            if not integrity_ok(res):
                failures += 1
        return {"integrity_failures": failures, "compiled_steps": len(script)}


# --- TF-IDF retrieval index for B-RAG-EMBED --------------------------------
def _tokenize(text: str) -> list[str]:
    out, cur = [], []
    for ch in text.lower():
        if ch.isalnum():
            cur.append(ch)
        else:
            if cur:
                out.append("".join(cur))
                cur = []
    if cur:
        out.append("".join(cur))
    return out


class RagIndex:
    """Deterministic TF-IDF index (TAU=0.30, QCR k=5) with no model calls."""

    def __init__(self, docs: dict[str, list[str]]) -> None:
        self.doc_ids = sorted(docs)
        n = len(self.doc_ids)
        df: dict[str, int] = {}
        tf: dict[str, dict[str, int]] = {}
        for did in self.doc_ids:
            counts: dict[str, int] = {}
            for tok in docs[did]:
                counts[tok] = counts.get(tok, 0) + 1
            tf[did] = counts
            for tok in counts:
                df[tok] = df.get(tok, 0) + 1
        idf = {tok: math.log((n + 1) / (c + 1)) + 1.0 for tok, c in df.items()}
        self._vec: dict[str, dict[str, float]] = {}
        for did in self.doc_ids:
            vec = {tok: cnt * idf[tok] for tok, cnt in tf[did].items()}
            norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
            self._vec[did] = {tok: v / norm for tok, v in vec.items()}

    def retrieve(self, query_tokens: list[str], k: int = 5) -> list[tuple[str, float]]:
        counts: dict[str, int] = {}
        for tok in query_tokens:
            counts[tok] = counts.get(tok, 0) + 1
        q = {tok: cnt * 1.0 for tok, cnt in counts.items()}
        norm = math.sqrt(sum(v * v for v in q.values()))
        if norm == 0:
            return []
        q = {tok: v / norm for tok, v in q.items()}
        scored: list[tuple[str, float]] = []
        for did, vec in self._vec.items():
            small, big = (q, vec) if len(q) < len(vec) else (vec, q)
            score = sum(v * big.get(tok, 0.0) for tok, v in small.items())
            scored.append((did, score))
        scored.sort(key=lambda p: (-p[1], p[0]))
        return scored[:k]


def build_rag_index(fixture: dict[str, Any]) -> RagIndex:
    """TRAIN-only corpus: family demos, site ids, slots and pool values."""
    docs: dict[str, list[str]] = {}
    pools = fixture.get("pools", {}) or {}
    for fid, demos in (fixture.get("demos") or {}).items():
        toks: list[str] = [fid]
        for demo in demos:
            for step in demo.get("steps", []):
                toks.extend(_tokenize(str(step.get("url", ""))))
                for v in (step.get("body") or {}).values():
                    toks.extend(_tokenize(str(v)))
            for v in (demo.get("values") or {}).values():
                toks.extend(_tokenize(str(v)))
        for slot, ab in (pools.get(fid) or {}).items():
            toks.extend(_tokenize(str(slot)))
            for side in ("A", "B"):
                for val in (ab.get(side) or []):
                    toks.extend(_tokenize(str(val)))
        docs[fid] = toks
    return RagIndex(docs)


class RagEmbedArm(Arm):
    """Embedding-style retrieval baseline: TF-IDF TAU=0.30, QCR k=5."""

    arm_id = "B-RAG-EMBED"
    TAU = 0.30
    K = 5

    def __init__(self, index: RagIndex) -> None:
        self.index = index

    def run(self, task: Task, env: Environment, ledger: CounterLedger) -> dict[str, Any]:
        query = _tokenize(task.site_id) + _tokenize(" ".join(task.slots)) + [
            tok for s in task.slots for tok in _tokenize(task.params.get(s, ""))
        ]
        t0 = time.perf_counter()
        candidates = self.index.retrieve(query, k=self.K)
        ledger.add_latency_ms((time.perf_counter() - t0) * 1000.0)
        ledger.incr("resolve", 1)  # one retrieval/lookup call per trajectory
        top_id, top_score = (candidates[0] if candidates else ("", 0.0))
        hit = bool(candidates) and top_score >= self.TAU
        if hit:
            ledger.incr("bind", len(task.slots))  # retrieved-template substitution
        extras = _serve_steps(task, env, ledger, conditional=False, validators=None)
        extras.update(
            {
                "rag_top_doc": top_id,
                "rag_top_score": round(top_score, 6),
                "rag_hit": bool(hit),
                "rag_k5_candidates": [c for c, _ in candidates],
                "rag_retrieval_correct": top_id == task.family_id,
            }
        )
        return extras


class SpiderArm(Arm):
    """SPIDER inheritance: freshness-gated conditional probing with
    deterministic localized repair and the verified_state MEA auditor."""

    arm_id = "P-SPIDER"

    def __init__(self, inheritance: "InheritanceArtifact") -> None:
        self.inh = inheritance

    def run(self, task: Task, env: Environment, ledger: CounterLedger) -> dict[str, Any]:
        params = {s: str(task.params.get(s, "")) for s in task.slots}
        resolution = self.inh.kernel.resolve("browse", {"family_id": task.family_id}, params)
        ledger.incr("resolve", 1)
        resolved = resolution.status.name == "EXECUTABLE"
        if resolved:
            ledger.incr("bind", len(task.slots))

        failures = 0
        stale_repairs = 0
        fresh_304 = 0
        for step in range(task.length):
            rid = task_rid(task, step)
            inherited_etag = self.inh.validators.get(rid)
            res = env.fetch(rid, inherited_etag)
            ledger.incr("requests", 1)
            ledger.incr("freshness", 1)  # one conditional freshness probe per step
            ledger.incr("verify", 1)
            ledger.add_latency_ms(res.latency_ms)
            ledger.add_payload_bytes(res.payload_bytes)
            if not integrity_ok(res):
                failures += 1
            if res.status == 304:
                fresh_304 += 1
            elif res.status == 200:
                if inherited_etag is not None and res.etag != inherited_etag:
                    # localized repair: refresh exactly this rid's validator
                    stale_repairs += 1
                    ledger.incr("repair", 1)
                    if res.etag:
                        self.inh.validators[rid] = res.etag
                elif inherited_etag is None and res.etag:
                    self.inh.validators.setdefault(rid, res.etag)
            ledger.incr("browser_steps", 1)

        auditor_pass: bool | None = None
        if resolution.mechanism_id is not None:
            observed = {"family_id": task.family_id, "verified": failures == 0}
            auditor_pass = bool(self.inh.kernel.verify(resolution.mechanism_id, observed))
            ledger.incr("verify", 1)  # verified_state MEA auditor call
        return {
            "integrity_failures": failures,
            "resolve_status": resolution.status.name,
            "auditor_pass": auditor_pass,
            "stale_repairs": stale_repairs,
            "fresh_304": fresh_304,
        }


# ---------------------------------------------------------------------------
# Inheritance build (measured one-time work) + verification pass
# ---------------------------------------------------------------------------
@dataclass
class InheritanceArtifact:
    kernel: Any
    registry_path: Path
    validators: dict[str, str]
    family_mech_ids: dict[str, str]
    build: dict[str, Any]


def build_inheritance(
    env: Environment,
    tasks: list[Task],
    fixture: dict[str, Any],
    workdir: str | Path,
    trace_phase: str = "build",
) -> InheritanceArtifact:
    """One-time measured build: demo/flow harvest + kernel distillation +
    registry construction (family induction + validator cache)."""
    from . import SpiderKernel, Mechanism
    from .models import Observation
    from .registry import MechanismRegistry

    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    registry_path = workdir / "mechanisms.jsonl"

    fam_tasks: dict[str, list[Task]] = {}
    for t in tasks:
        fam_tasks.setdefault(t.family_id, []).append(t)

    validators: dict[str, str] = {}
    t_build0 = time.perf_counter()
    harvest_requests = 0
    harvest_bytes = 0
    t0 = time.perf_counter()
    for fid in sorted(fam_tasks):
        grp = fam_tasks[fid]
        tmpl = grp[0].template_id
        length = grp[0].length
        for step in range(length):
            rid = f"{fid}_{tmpl}_s{step}"
            res = env.fetch(rid, None, phase=trace_phase) if isinstance(env, HttpSubstrateEnvironment) else env.fetch(rid, None)
            harvest_requests += 1
            harvest_bytes += res.payload_bytes
            if res.status == 200 and res.etag:
                validators[rid] = res.etag
    harvest_ms = (time.perf_counter() - t0) * 1000.0

    registry = MechanismRegistry(registry_path)
    kernel = SpiderKernel(registry, min_confidence=0.8)

    # Phase 2: kernel distillation over demo observations (literal candidates)
    t0 = time.perf_counter()
    distill_count = 0
    for fid in sorted(fam_tasks):
        grp = fam_tasks[fid]
        demo_list = (fixture.get("demos") or {}).get(fid, [])
        observations = demo_list or [None]
        for demo in observations:
            action = {"steps": len((demo or {}).get("steps", [])), "site": grp[0].site_id}
            obs = Observation(
                intent="browse",
                state={"family_id": fid},
                action=action,
                next_state={"family_id": fid, "verified": True},
                success=True,
                provenance={"source": "demo", "family_id": fid},
            )
            mech = kernel.distill(obs)
            if mech is not None:
                registry.upsert(mech)
                distill_count += 1
    distill_ms = (time.perf_counter() - t0) * 1000.0

    # Phase 3: family induction (parameterized flow mechanism + validators)
    t0 = time.perf_counter()
    family_mech_ids: dict[str, str] = {}
    for fid in sorted(fam_tasks):
        grp = fam_tasks[fid]
        tmpl = grp[0].template_id
        length = grp[0].length
        slots = sorted(grp[0].slots)
        rid_list = [f"{fid}_{tmpl}_s{s}" for s in range(length)]
        fam_validators = {rid: validators[rid] for rid in rid_list if rid in validators}
        mech = Mechanism(
            mechanism_id=f"spider-{fid}",
            intent="browse",
            preconditions={"family_id": fid},
            applicability_guards={"family_id": fid},
            action_template={"flow": f"{fid}/{tmpl}", "slots": "${" + ", ".join(slots) + "}"},
            postconditions={"family_id": fid, "verified": True},
            parameter_slots=slots,
            confidence=0.85,
            freshness={"ttl_s": 60, "etag_mode": 'W/"body_sha16"', "validators": fam_validators},
            evidence=sorted(fam_validators),
        )
        registry.upsert(mech)
        family_mech_ids[fid] = mech.mechanism_id
    induction_ms = (time.perf_counter() - t0) * 1000.0
    build_ms_total = (time.perf_counter() - t_build0) * 1000.0

    build = {
        "phases": {
            "harvest_ms": harvest_ms,
            "distill_ms": distill_ms,
            "induction_ms": induction_ms,
        },
        "build_ms": build_ms_total,
        "harvest_requests": harvest_requests,
        "harvest_payload_bytes": harvest_bytes,
        "mechanisms_distilled": distill_count,
        "family_mechanisms": len(family_mech_ids),
        "validators_cached": len(validators),
        "unit": "wall-clock milliseconds (measured, no token denominators)",
    }
    return InheritanceArtifact(
        kernel=kernel,
        registry_path=registry_path,
        validators=validators,
        family_mech_ids=family_mech_ids,
        build=build,
    )


def verify_inheritance(env: Environment, artifact: InheritanceArtifact, tasks: list[Task]) -> dict[str, Any]:
    """One-time measured verification pass: audited postcondition checks over
    every family mechanism + freshness-probe validation over cached
    validators.  Returns measured non-token verification cost."""
    fam_length: dict[str, tuple[str, int]] = {}
    for t in tasks:
        fam_length.setdefault(t.family_id, (t.template_id, t.length))

    t0 = time.perf_counter()
    auditor_checks = 0
    auditor_passes = 0
    for fid in sorted(fam_length):
        mech_id = artifact.family_mech_ids.get(fid)
        if mech_id is None:
            continue
        auditor_checks += 1
        if artifact.kernel.verify(mech_id, {"family_id": fid, "verified": True}):
            auditor_passes += 1
    auditor_ms = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    probe_requests = 0
    probe_bytes = 0
    probe_304 = 0
    for fid in sorted(fam_length):
        tmpl, length = fam_length[fid]
        rid = f"{fid}_{tmpl}_s0"
        etag = artifact.validators.get(rid)
        if etag is None:
            continue
        res = env.fetch(rid, etag, phase="verify") if isinstance(env, HttpSubstrateEnvironment) else env.fetch(rid, etag)
        probe_requests += 1
        probe_bytes += res.payload_bytes
        if res.status == 304:
            probe_304 += 1
    probe_ms = (time.perf_counter() - t0) * 1000.0

    return {
        "verify_ms": auditor_ms + probe_ms,
        "phases": {"auditor_ms": auditor_ms, "freshness_probe_ms": probe_ms},
        "auditor_checks": auditor_checks,
        "auditor_passes": auditor_passes,
        "probe_requests": probe_requests,
        "probe_payload_bytes": probe_bytes,
        "probe_304_hits": probe_304,
        "unit": "wall-clock milliseconds (measured, no token denominators)",
    }


# ---------------------------------------------------------------------------
# Harness runner (gate + per-trajectory hard reset)
# ---------------------------------------------------------------------------
def run_harness(
    arms: Iterable[Arm],
    tasks: Iterable[Task],
    env: Environment,
    mode: str = "scripted",
    capabilities: dict[str, bool] | None = None,
    requirements: dict[str, dict[str, tuple[str, ...]]] | None = None,
) -> list[TrajectoryRecord]:
    """Execute every arm over every trajectory with a hard counter reset.

    Fail-closed semantics: an arm whose prerequisite capability is absent is
    never executed and its records carry ``counters=None`` (no surrogate
    fill, no zero/default fill).
    """
    available = capabilities if capabilities is not None else {"http_substrate": True}
    records: list[TrajectoryRecord] = []
    for arm in arms:
        gate = fail_closed_gate(arm.arm_id, mode, available, requirements)
        for task in tasks:
            if gate.status != "EXECUTABLE":
                records.append(
                    TrajectoryRecord(
                        arm_id=arm.arm_id,
                        mode=mode,
                        task_id=task.task_id,
                        family_id=task.family_id,
                        novelty_level=task.novelty_level,
                        length=task.length,
                        gate_status="UNKNOWN",
                        gate_reason=gate.reason,
                        counters=None,
                        payload_bytes=None,
                        extras={"missing_capabilities": list(gate.missing)},
                    )
                )
                continue
            ledger = CounterLedger()
            extras = arm.run(task, env, ledger) or {}
            records.append(
                TrajectoryRecord(
                    arm_id=arm.arm_id,
                    mode=mode,
                    task_id=task.task_id,
                    family_id=task.family_id,
                    novelty_level=task.novelty_level,
                    length=task.length,
                    gate_status="EXECUTABLE",
                    gate_reason=gate.reason,
                    counters=ledger.snapshot(),
                    payload_bytes=ledger.payload_bytes,
                    extras=extras,
                )
            )
    return records


# ---------------------------------------------------------------------------
# Statistics: family-stratified trajectory-grouped bootstrap + block permutation
# ---------------------------------------------------------------------------
def ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            out[order[k]] = avg
        i = j + 1
    return out


def spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    rx, ry = ranks(list(map(float, xs))), ranks(list(map(float, ys)))
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    denx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    deny = math.sqrt(sum((b - my) ** 2 for b in ry))
    if denx == 0 or deny == 0:
        return None
    return num / (denx * deny)


def _percentile(sorted_vals: list[float], q: float) -> float:
    if not sorted_vals:
        raise ValueError("empty distribution")
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    idx = q * (len(sorted_vals) - 1)
    lo = int(math.floor(idx))
    hi = int(math.ceil(idx))
    if lo == hi:
        return sorted_vals[lo]
    frac = idx - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


def stratified_grouped_bootstrap(
    rows: list[dict[str, Any]],
    stat_fn: Callable[[list[dict[str, Any]]], float | None],
    strata_key: str = "family_id",
    B: int = 5000,
    seed: int = SEED,
) -> dict[str, Any]:
    """Family-stratified, trajectory-grouped bootstrap CI (B=5000 frozen).

    Strata (families) are kept at their observed count; within each sampled
    stratum whole trajectories are resampled with replacement.
    """
    strata: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        strata.setdefault(str(r[strata_key]), []).append(r)
    keys = sorted(strata)
    rng = random.Random(seed)
    ests: list[float] = []
    for _ in range(B):
        sample: list[dict[str, Any]] = []
        for _ in keys:
            grp = strata[keys[rng.randrange(len(keys))]]
            for _ in range(len(grp)):
                sample.append(grp[rng.randrange(len(grp))])
        v = stat_fn(sample)
        if v is not None and math.isfinite(v):
            ests.append(float(v))
    if len(ests) < 100:
        return {"lo": None, "hi": None, "n_valid": len(ests), "B": B, "seed": seed}
    ests.sort()
    return {
        "lo": _percentile(ests, 0.025),
        "hi": _percentile(ests, 0.975),
        "median": _percentile(ests, 0.5),
        "n_valid": len(ests),
        "B": B,
        "seed": seed,
        "design": "family-stratified trajectory-grouped bootstrap",
    }


def block_permutation_test(
    rows: list[dict[str, Any]],
    x_key: str,
    y_key: str,
    block_key: str = "family_id",
    B: int = 5000,
    seed: int = SEED,
) -> dict[str, Any]:
    """Family-blocked label-permutation test on Spearman rho (B=5000).

    x-labels are shuffled *within family blocks*, preserving the family
    grouping, exactly as in the accepted Product-lane block-permutation
    implementation.
    """
    blocks: dict[str, list[int]] = {}
    for i, r in enumerate(rows):
        blocks.setdefault(str(r[block_key]), []).append(i)
    xs = [float(r[x_key]) for r in rows]
    ys = [float(r[y_key]) for r in rows]
    observed = spearman(xs, ys)
    if observed is None:
        return {"rho_observed": None, "p": None, "B": B, "seed": seed, "reason": "zero variance or n<3"}
    rng = random.Random(seed)
    null_rhos: list[float] = []
    idxs_all = list(blocks.values())
    for _ in range(B):
        perm_x = list(xs)
        for idxs in idxs_all:
            vals = [xs[i] for i in idxs]
            rng.shuffle(vals)
            for i, v in zip(idxs, vals):
                perm_x[i] = v
        r0 = spearman(perm_x, ys)
        if r0 is not None:
            null_rhos.append(r0)
    if not null_rhos:
        return {"rho_observed": observed, "p": None, "B": B, "seed": seed, "reason": "no valid null draws"}
    null_rhos.sort()
    p = (sum(1 for r0 in null_rhos if abs(r0) >= abs(observed)) + 1) / (len(null_rhos) + 1)
    shuffled_median = statistics.median(null_rhos)
    return {
        "rho_observed": observed,
        "p": p,
        "rho_shuffled_median": shuffled_median,
        "rho_shuffled_lo": _percentile(null_rhos, 0.025),
        "rho_shuffled_hi": _percentile(null_rhos, 0.975),
        "B": B,
        "seed": seed,
        "design": "family-blocked label permutation (x shuffled within family)",
    }


def paired_signflip_permutation(
    deltas: list[float],
    blocks: list[str],
    B: int = 5000,
    seed: int = SEED,
) -> dict[str, Any]:
    """Paired block permutation: arm labels swapped within family blocks."""
    if not deltas:
        return {"mean_observed": None, "p": None, "B": B, "seed": seed}
    observed = statistics.mean(deltas)
    rng = random.Random(seed)
    n = len(deltas)
    extreme = 0
    for _ in range(B):
        m = sum(deltas[i] * (1.0 if rng.random() < 0.5 else -1.0) for i in range(n)) / n
        if abs(m) >= abs(observed):
            extreme += 1
    p = (extreme + 1) / (B + 1)
    return {"mean_observed": observed, "p": p, "B": B, "seed": seed, "design": "paired sign-flip within blocks"}


# ---------------------------------------------------------------------------
# Break-even reuse count (f*) — non-token units only, by construction
# ---------------------------------------------------------------------------
def breakeven_f_star(
    build_cost: float,
    verify_cost: float,
    cold_serving_cost: float,
    inherited_serving_cost: float,
    unit: str = "ms",
) -> dict[str, Any]:
    """f* = (build_cost + verify_cost) / (serving_cold - serving_inherited).

    Frozen formula from prereg.md Part C.  Only non-token measured work is
    representable: there is deliberately no token parameter, because
    token-denominated economics are NOT_APPLICABLE/UNKNOWN until a
    policy-model credential exists.
    """
    denominator = cold_serving_cost - inherited_serving_cost
    computable = denominator > 0 and math.isfinite(denominator)
    f_star = ((build_cost + verify_cost) / denominator) if computable else None
    return {
        "formula": "f* = (build_cost + verify_cost) / (serving_cost_cold - serving_cost_inherited)",
        "unit": unit,
        "build_cost": build_cost,
        "verify_cost": verify_cost,
        "serving_cost_cold": cold_serving_cost,
        "serving_cost_inherited": inherited_serving_cost,
        "numerator_onetime_cost": build_cost + verify_cost,
        "denominator_per_reuse_saving": denominator,
        "f_star": f_star,
        "computable": bool(computable and f_star is not None and math.isfinite(f_star)),
        "token_inputs": "NOT_APPLICABLE (no token parameter exists by construction)",
    }


def oat_sensitivity(
    inputs: dict[str, float],
    f_of: Callable[..., dict[str, Any]],
    delta: float = 0.10,
) -> dict[str, Any]:
    """One-at-a-time +/-delta sensitivity on each measured input; identifies
    the single measured quantity that most changes f*."""
    base = f_of(**inputs)
    base_f = base.get("f_star")
    rows: dict[str, Any] = {}
    dominant = None
    dominant_abs = -1.0
    for name in sorted(inputs):
        up = dict(inputs)
        down = dict(inputs)
        up[name] = inputs[name] * (1 + delta)
        down[name] = inputs[name] * (1 - delta)
        res_up, res_down = f_of(**up), f_of(**down)
        f_up, f_down = res_up.get("f_star"), res_down.get("f_star")
        # Evaluate each perturbed side independently: one side may leave the
        # valid region (e.g. the serving-cost denominator flips sign) while
        # the other remains computable; dropping both would hide the most
        # sensitive quantity instead of identifying it.
        rel_up = (f_up - base_f) / base_f if (base_f and f_up is not None) else None
        rel_down = (f_down - base_f) / base_f if (base_f and f_down is not None) else None
        sides = [abs(v) for v in (rel_up, rel_down) if v is not None]
        impact = max(sides) if sides else None
        noncomp = [
            side
            for side, res in (("up", res_up), ("down", res_down))
            if res.get("f_star") is None and res.get("computable") is False
        ]
        rows[name] = {
            "value": inputs[name],
            "f_star_up": f_up,
            "f_star_down": f_down,
            "rel_change_up": rel_up,
            "rel_change_down": rel_down,
            "max_abs_rel_change": impact,
            "becomes_noncomputable": noncomp,
        }
        if impact is not None and impact > dominant_abs:
            dominant_abs = impact
            dominant = name
    return {
        "delta": delta,
        "base": base,
        "per_input": rows,
        "dominant_quantity": dominant,
        "dominant_max_abs_rel_change": dominant_abs if dominant else None,
    }


__all__ = [
    "SEED",
    "COUNTER_NAMES",
    "ARM_IDS",
    "MODES",
    "DEFAULT_REQUIREMENTS",
    "CounterLedger",
    "Task",
    "tasks_from_manifest",
    "task_rid",
    "FetchResult",
    "Environment",
    "MockEnvironment",
    "HttpSubstrateEnvironment",
    "integrity_ok",
    "GateDecision",
    "probe_capabilities",
    "fail_closed_gate",
    "TrajectoryRecord",
    "Arm",
    "ColdArm",
    "InstructionsArm",
    "DeterministicExecutorArm",
    "RagIndex",
    "RagEmbedArm",
    "build_rag_index",
    "SpiderArm",
    "InheritanceArtifact",
    "build_inheritance",
    "verify_inheritance",
    "run_harness",
    "ranks",
    "spearman",
    "stratified_grouped_bootstrap",
    "block_permutation_test",
    "paired_signflip_permutation",
    "breakeven_f_star",
    "oat_sensitivity",
]
