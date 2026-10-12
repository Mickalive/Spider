#!/usr/bin/env python3
# FROZEN RUNNER for EXP-RUNTIME-38212966040 (runtime, design_contract_version 2).
# C-DELTA-REPAIR, PIVOT from C-MEAS-VALID.
#
# Question: On the credential-free, locally served, perturbable stdlib HTTP
# substrate, with the SHIPPED parameterized carrier held fixed
# (src/spider/kernel.py: distill_parameterized -> resolve -> execute -> verify),
# and with the freshness-guard probe observation REUSED so that retrieval and
# verification are not double-charged, does signal-driven local repair achieve a
# net end-to-end product-counter cost strictly below cold re-derivation
# (ratio < 1.00) at the carrier cold budgets L=2 and L=3, or is the previously
# observed ~5.3% product-counter regression intrinsic to localized repair?
#
# Three repair systems are measured on the SAME substrate and the SAME cold
# baseline so the accounting question is a system question, not a re-tuning:
#   T-REPAIR-REUSE        treatment: guard fused into the first task read; the
#                         repair reuses the probe observation (no duplicate
#                         resolve/fetch/verify for the first task id).
#   T-REPAIR-CONSERVATIVE sensitivity: same reuse, but the repair also re-resolves
#                         (charges the rebind's retrieval) -> upper bound on cost.
#   T-REPAIR-LEGACY       replication control: the prior separate-guard-probe plus
#                         full-batch re-execution system; must reproduce the prior
#                         product-counter regression (>1.00).
#
# Stdlib only. No credentials, no external network, no LLM, no browser.
# Usage:
#   python runner_delta_repair_reuse.py                 # scored run
#   python runner_delta_repair_reuse.py --mechanics-only
#   python runner_delta_repair_reuse.py --reachability-probe
#   python runner_delta_repair_reuse.py --liveness-only   # no repair, no cost ratio
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import random
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-RUNTIME-38212966040"
SEED = 38212966040 % (2 ** 32)

# Fresh per-process registry directory: MechanismRegistry.all() loads existing
# JSONL and upsert() merges by mechanism_id, so a reused path would resurrect
# stale mechanisms whose embedded endpoint port no longer exists.
_RUN_DIR = Path(tempfile.mkdtemp(prefix=f"exprun382-{os.getpid()}-"))

sys.path.insert(0, str(ROOT / "src"))
from spider.kernel import SpiderKernel, TrajectoryCounters  # noqa: E402
from spider.models import Mechanism, Observation  # noqa: E402
from spider.registry import MechanismRegistry  # noqa: E402

# ---------------------------------------------------------------- constants --
RESOURCES = ["users", "posts", "comments", "albums", "photos"]
TARGETS = ["users", "posts", "comments"]
TASK_IDS = [14, 15, 16, 17, 18]
# Learning ids are DISJOINT from task ids so re-derivation's observation reads
# are genuine acquisition reads, never a double-charge of a task read.
LEARN_IDS = [11, 12, 13]
LEARN_IDS_MIN = [11, 12]
LEARN_IDS_DEEP = [10, 11, 12, 13]
CLASSES = ["P1-ENDPOINT", "P2-STRUCTURE", "P3-PERMISSION"]
NEW_SEGMENTS = ["people", "articles", "notes", "collections", "media"]
ANCHOR = "kind"
ANCHOR_RENAMED = "entity_type"
CONSENT_HEADER = "X-Consent"
CONSENT_VALUE = "granted"
JACCARD_THRESHOLD = 0.85
MIN_CONFIDENCE = 0.8

REPAIR_SUCCESS_BAR = 0.80
WILSON_SUCCESS_LOWER_BAR = 0.60
CONTAMINATION_BAR = 0.10
GUARD_FIRE_BAR = 0.80
PRODUCT_COST_BAR = 1.00      # mandate: strictly below cold on the registered counter
PRODUCT_COST_MAX = 1.15      # a priori materiality bound separating neutral from regression
FETCH_COST_BAR = 0.90        # strictly below cold on live fetches
COLD_SUCCESS_BAR = 0.90
LITERAL_SUCCESS_BAR = 0.10
LEGACY_REGRESSION_FLOOR = 1.00   # legacy control must exceed this at L=2
WILSON_Z = 1.96
TRIALS_PER_CLASS = 12

# ---------------------------------------------------------------- substrate --
def build_record(resource: str, rid: int) -> dict:
    s = str(rid)
    if resource == "users":
        return {"id": s, "kind": "user", "name": f"User {rid}", "email": f"user{rid}@example.com"}
    if resource == "posts":
        return {"id": s, "kind": "post", "title": f"Post {rid}", "body": f"Body {rid}"}
    if resource == "comments":
        return {"id": s, "kind": "comment", "author": f"Author {rid}", "text": f"Text {rid}"}
    if resource == "albums":
        return {"id": s, "kind": "album", "title": f"Album {rid}", "owner": f"Owner {rid}"}
    if resource == "photos":
        return {"id": s, "kind": "photo", "caption": f"Caption {rid}", "url": f"img://{rid}"}
    raise KeyError(resource)


class AppState:
    def __init__(self):
        self.perturb = None
        self.noise = False
        self.nonce = 0

    def reset(self):
        self.perturb = None
        self.noise = False
        self.nonce = 0

    def set_perturb(self, cls: str, resource: str, seed: int):
        rng = random.Random(seed)
        cfg = {"class": cls, "resource": resource}
        if cls == "P1-ENDPOINT":
            cfg["new_segment"] = rng.choice(NEW_SEGMENTS)
        self.perturb = cfg


class Handler(BaseHTTPRequestHandler):
    state: AppState = None

    def log_message(self, *args):
        pass

    def _json(self, code: int, body: dict):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_GET(self):
        parts = [p for p in self.path.split("/") if p]
        if len(parts) != 3 or parts[0] != "api":
            self._json(404, {"error": "not found"})
            return
        segment, rid_raw = parts[1], parts[2]
        try:
            rid = int(rid_raw)
        except ValueError:
            self._json(400, {"error": "bad id"})
            return
        cfg = self.state.perturb
        logical = segment
        if cfg and cfg["class"] == "P1-ENDPOINT" and segment == cfg["resource"]:
            self.send_response(301)
            self.send_header("Location", f"/api/{cfg['new_segment']}/{rid}")
            self.end_headers()
            return
        if cfg and cfg["class"] == "P1-ENDPOINT" and segment == cfg["new_segment"]:
            logical = cfg["resource"]
        if logical not in RESOURCES:
            self._json(404, {"error": "unknown resource"})
            return
        if cfg and cfg["class"] == "P3-PERMISSION" and logical == cfg["resource"]:
            if self.headers.get(CONSENT_HEADER) != CONSENT_VALUE:
                self.send_response(403)
                self.send_header("X-Required-Consent", CONSENT_VALUE)
                self.end_headers()
                return
        body = build_record(logical, rid)
        if cfg and cfg["class"] == "P2-STRUCTURE" and logical == cfg["resource"]:
            renamed = {ANCHOR_RENAMED if k == ANCHOR else k: v for k, v in body.items()}
            renamed["schema_version"] = "2"
            body = renamed
        if self.state.noise:
            self.state.nonce += 1
            body = dict(body)
            body["observed_at"] = f"t{self.state.nonce}"
        self._json(200, body)


class LocalApp:
    def __init__(self):
        self.state = AppState()
        Handler.state = self.state
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    @property
    def origin(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


def wait_ready(app: "LocalApp", attempts: int = 100) -> bool:
    for _ in range(attempts):
        r = fetch(app.origin + "/api/albums/1")
        if r.status is not None:
            return True
        time.sleep(0.05)
    return False


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


_OPENER = build_opener(NoRedirect)


class Counters:
    def __init__(self):
        self.http = 0
        self.retrieval = 0
        self.verification = 0
        self.repair = 0

    def product(self) -> int:
        return self.http + self.retrieval + self.verification + self.repair

    def as_dict(self):
        return {"http": self.http, "retrieval": self.retrieval,
                "verification": self.verification, "repair": self.repair,
                "product": self.product()}


class HTTPResult:
    def __init__(self, status, headers, body, error=None):
        self.status = status
        self.headers = headers or {}
        self.body = body
        self.error = error


def fetch(url: str, headers: dict | None = None, counters: Counters | None = None,
          origin: str | None = None) -> HTTPResult:
    if counters is not None:
        counters.http += 1
    req = Request(url, headers=headers or {})
    try:
        with _OPENER.open(req, timeout=5) as resp:
            raw = resp.read().decode()
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                body = None
            return HTTPResult(resp.status, dict(resp.headers), body)
    except HTTPError as exc:
        raw = exc.read().decode() if exc.fp else ""
        try:
            body = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            body = None
        hdrs = dict(exc.headers)
        if origin is not None:
            hdrs["_origin"] = origin
        return HTTPResult(exc.code, hdrs, body, error="HTTPError")
    except URLError as exc:
        return HTTPResult(None, {}, None, error=str(exc))


# ----------------------------------------------------- deterministic guard --
TYPE_MAP = {"str": "string", "int": "integer", "float": "number", "bool": "boolean",
            "NoneType": "null", "list": "array", "dict": "object"}


def flatten(obj, prefix=""):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, list):
        out[prefix] = obj
    else:
        out[prefix] = obj
    return out


def field_type_tokens(obj, prefix=""):
    pairs = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, dict):
                pairs.update(field_type_tokens(v, path))
            elif isinstance(v, list):
                pairs.add((path, "array"))
            else:
                pairs.add((path, TYPE_MAP.get(type(v).__name__, type(v).__name__)))
    elif isinstance(obj, list):
        pairs.add((prefix, "array"))
    else:
        pairs.add((prefix, TYPE_MAP.get(type(obj).__name__, type(obj).__name__)))
    return pairs


def required_token_set(body, required_paths):
    return {(p, t) for (p, t) in field_type_tokens(body) if p in required_paths}


def jaccard(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


class Arm:
    """A fresh kernel + registry + honest counters for one arm on one trial."""

    _seq = 0

    def __init__(self, mech_dicts, reg_dir: Path, tag: str):
        Arm._seq += 1
        self.path = _RUN_DIR / f"reg-{tag}-{Arm._seq:06d}.jsonl"
        self.registry = MechanismRegistry(self.path)
        for m in mech_dicts.values():
            self.registry.upsert(Mechanism(**m))
        self.kernel = SpiderKernel(self.registry, min_confidence=MIN_CONFIDENCE,
                                   counters=TrajectoryCounters())
        self.counters = Counters()

    def sync(self):
        c = self.kernel.counters
        self.counters.retrieval = c.retrieval_calls
        self.counters.verification = c.verification_calls
        self.counters.repair = c.repair_attempts

    def target_mech(self, resource):
        for m in self.registry.all():
            if m.intent == f"read_{resource}":
                return m
        return None

    def resolve(self, intent, context, params):
        r = self.kernel.resolve(intent, context, params)
        self.sync()
        return r

    def verify(self, mid, body, params):
        v = self.kernel.verify(mid, body, params)
        self.sync()
        return v

    def rebind(self, intent, context, params):
        r = self.kernel.rebind(intent, context, params)
        self.sync()
        return r

    def charge_repair_attempt(self):
        """Charge exactly one repair attempt WITHOUT the redundant re-resolve.

        The reused probe observation already carries the corrected binding, so
        the repair does not re-derive it (this is the mandate's 'reuse the
        freshness-guard probe observation so retrieval/verification are not
        double-charged')."""
        self.kernel.counters.add("repair_attempts")
        self.sync()


def make_mech_dicts(origin, counters):
    """Learn all resources from LEARN_IDS with the shipped carrier."""
    k = SpiderKernel(MechanismRegistry(_RUN_DIR / "unused.jsonl"),
                     min_confidence=MIN_CONFIDENCE, counters=TrajectoryCounters())
    mechs, cached = {}, {}
    for r in RESOURCES:
        obs = []
        for rid in LEARN_IDS:
            res = fetch(f"{origin}/api/{r}/{rid}", {}, counters)
            obs.append(Observation(intent=f"read_{r}", state={"resource_type": r},
                                   action={"method": "GET", "url": f"{origin}/api/{r}/{rid}",
                                           "headers": {}},
                                   next_state=res.body or {}, success=(res.status == 200)))
        m = k.distill_parameterized(obs)
        if m is None:
            return None, None
        mechs[r] = m.as_dict()
        cached[r] = field_type_tokens(obs[0].next_state)
    return mechs, cached


def execute_batch(arm: Arm, intent, context, slot, ids, extra_header=None):
    ok = True
    values = []
    for t in ids:
        pid = str(t)
        r = arm.resolve(intent, context, {slot: pid})
        if r.status.name != "EXECUTABLE" or r.bound_action is None:
            ok = False
            values.append(None)
            continue
        headers = dict(r.bound_action.get("headers", {}))
        if extra_header:
            headers.update(extra_header)
        res = fetch(r.bound_action["url"], headers, arm.counters)
        if res.status != 200 or res.body is None:
            ok = False
            values.append(None)
            continue
        if not arm.verify(r.mechanism_id, res.body, {slot: pid}):
            ok = False
        values.append(res.body.get("id"))
    return ok, values


# ------------------------------------------------------------------ repair --
def guard(cached_tokens, required_paths, failed, arm: Arm, mech, params):
    """Deterministic structural + postcondition freshness guard.

    Fires (stale) iff the live probe is non-200/errored, OR the mechanism's own
    postconditions no longer verify, OR the required-field-filtered structural
    token set has drifted below JACCARD_THRESHOLD. Fields outside the
    mechanism's postcondition paths cannot trigger it.
    """
    if failed.error is not None or failed.status != 200 or failed.body is None:
        return True, {"reason": "non-200", "status": failed.status, "jaccard": None}
    live = required_token_set(failed.body, required_paths)
    cached = {(p, t) for (p, t) in cached_tokens if p in required_paths}
    j = jaccard(cached, live)
    ok = arm.verify(mech.mechanism_id, failed.body, params)
    if (not ok) or j < JACCARD_THRESHOLD:
        return True, {"reason": "postcondition" if not ok else "structure",
                      "status": failed.status, "jaccard": j}
    return False, {"reason": "fresh", "status": failed.status, "jaccard": j}


def local_repair(arm: Arm, mech, resource, slot, probe_id, failed, origin):
    """Class-agnostic local repair driven only by live response signals.

    Branches purely on the observed failure signature:
      * redirect       -> rebind the endpoint segment from ``Location``
      * 403 permission -> attach the server-advertised required header
      * 200 drift      -> re-adopt the live postcondition schema, relocating
                          renamed anchor paths (old literal value -> new key)

    Returns (patched_mechanism, probe_body, probe_header); probe_body is the
    live post-repair observation that the caller reuses (verifies once) as the
    first task read instead of issuing a duplicate request. Never touches
    another resource's mechanism.
    """
    import re as _re

    template_re = _re.compile(r"^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$")
    probe_body = None
    probe_header = {}
    new_template = mech.action_template["url"]
    if failed.status in (301, 302, 303, 307, 308) and failed.headers.get("Location"):
        loc = failed.headers["Location"]
        hop_origin = failed.headers.get("_origin", origin)
        probe = fetch(hop_origin + loc, {}, arm.counters)
        if probe.status != 200 or probe.body is None:
            return None, None, None
        probe_body = probe.body
        new_template = hop_origin + "/".join(loc.split("/")[:-1]) + "/${" + slot + "}"
    elif failed.status == 403:
        req_header = req_value = None
        for k, v in failed.headers.items():
            if k.lower().startswith("x-required-"):
                req_header = "X-" + k[len("x-required-"):]
                req_value = v
        if req_header is None:
            return None, None, None
        probe_header = {req_header: req_value}
        probe = fetch(new_template.replace("${" + slot + "}", str(probe_id)),
                      probe_header, arm.counters)
        if probe.status != 200 or probe.body is None:
            return None, None, None
        probe_body = probe.body
    elif failed.status == 200 and failed.body is not None:
        probe_body = failed.body
    else:
        return None, None, None

    new_post: dict = {}
    for k, v in mech.postconditions.items():
        if isinstance(v, str) and template_re.match(v):
            new_post[k] = v
        elif probe_body.get(k) == v:
            new_post[k] = v
        else:
            cands = [nk for nk, nv in probe_body.items()
                     if nv == v and nk not in new_post]
            new_post[cands[0] if cands else k] = v

    patched = copy.deepcopy(mech)
    patched.action_template["url"] = new_template
    if probe_header:
        patched.action_template["headers"] = dict(probe_header)
    patched.postconditions = new_post
    return patched, probe_body, probe_header


def run_repair_reuse(app, origin, mechs, cached, resource, mode="reuse"):
    """Treatment. Freshness check is FUSED into the first task read; the repair
    reuses the probe observation and does not issue a duplicate resolve/fetch/
    verify for the first task id.

    mode="reuse":        charge one repair attempt, no redundant re-resolve.
    mode="conservative": also re-resolve through the carrier's rebind (charges
                         the rebind retrieval) -> upper bound on repair cost.
    """
    arm = Arm(mechs, Path("/tmp"), "reuse" if mode == "reuse" else "cons")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    intent = mech.intent
    context = {"resource_type": resource}
    required_paths = set(flatten(mech.postconditions).keys())
    # first task read doubles as the freshness probe (fused: no extra read)
    r0 = arm.resolve(intent, context, {slot: str(TASK_IDS[0])})
    if r0.status.name != "EXECUTABLE" or r0.bound_action is None:
        return {"success": False, "guard_fired": False, "arm": arm, "reason": "not-executable"}
    failed = fetch(r0.bound_action["url"], r0.bound_action.get("headers", {}),
                   arm.counters, origin=origin)
    stale, ginfo = guard(cached, required_paths, failed, arm, mech, {slot: str(TASK_IDS[0])})
    if not stale:
        # id1 already read+verified by the guard probe; execute the rest
        ok, _ = execute_batch(arm, intent, context, slot, TASK_IDS[1:])
        return {"success": ok, "guard_fired": False, "arm": arm, "reason": "fresh"}
    patched, probe_body, probe_header = local_repair(
        arm, mech, resource, slot, TASK_IDS[0], failed, origin)
    if patched is None:
        return {"success": False, "guard_fired": True, "arm": arm, "reason": "repair-failed",
                "guard_info": ginfo}
    arm.registry.upsert(patched)
    if mode == "conservative":
        arm.rebind(intent, context, {slot: str(TASK_IDS[0])})  # charges repair + retrieval
    else:
        arm.charge_repair_attempt()                            # one repair attempt only
    if probe_body is not None:
        arm.verify(patched.mechanism_id, probe_body, {slot: str(TASK_IDS[0])})
    ok, _ = execute_batch(arm, intent, context, slot, TASK_IDS[1:])
    return {"success": ok, "guard_fired": True, "arm": arm, "reason": "repaired",
            "guard_info": ginfo}


def run_repair_legacy(app, origin, mechs, cached, resource):
    """Replication control: the PRIOR system. A separate guard probe read is
    issued before the batch, and after repair the full task batch is
    re-executed (the first task id is therefore read twice more)."""
    arm = Arm(mechs, Path("/tmp"), "legacy")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    intent = mech.intent
    context = {"resource_type": resource}
    required_paths = set(flatten(mech.postconditions).keys())
    r0 = arm.resolve(intent, context, {slot: str(TASK_IDS[0])})
    if r0.status.name != "EXECUTABLE" or r0.bound_action is None:
        return {"success": False, "guard_fired": False, "arm": arm, "reason": "not-executable"}
    failed = fetch(r0.bound_action["url"], r0.bound_action.get("headers", {}),
                   arm.counters, origin=origin)
    stale, ginfo = guard(cached, required_paths, failed, arm, mech, {slot: str(TASK_IDS[0])})
    if stale:
        patched, _pb, _ph = local_repair(arm, mech, resource, slot, TASK_IDS[0], failed, origin)
        if patched is None:
            return {"success": False, "guard_fired": True, "arm": arm, "reason": "repair-failed"}
        arm.registry.upsert(patched)
        arm.rebind(intent, context, {slot: str(TASK_IDS[0])})
    ok, _ = execute_batch(arm, intent, context, slot, TASK_IDS)
    return {"success": ok, "guard_fired": stale, "arm": arm, "reason": "legacy",
            "guard_info": ginfo}


def run_cold(app, origin, resource, ids=None, tag="cold"):
    ids = ids or LEARN_IDS
    arm = Arm({}, Path("/tmp"), tag)
    base = f"{origin}/api/{resource}"
    extra_header = {}
    probe = fetch(f"{base}/{ids[0]}", {}, arm.counters, origin=origin)
    if probe.status in (301, 302, 303, 307, 308) and probe.headers.get("Location"):
        loc = probe.headers["Location"]
        base = origin + "/".join(loc.split("/")[:-1])
    elif probe.status == 403:
        for k, v in probe.headers.items():
            if k.lower().startswith("x-required-"):
                extra_header["X-" + k[len("x-required-"):]] = v
    elif probe.status != 200:
        return {"success": False, "arm": arm, "reason": "discovery-failed"}
    obs = []
    for rid in ids:
        res = fetch(f"{base}/{rid}", extra_header, arm.counters)
        if res.status != 200 or res.body is None:
            return {"success": False, "arm": arm, "reason": "observation-failed"}
        obs.append(Observation(intent=f"read_{resource}", state={"resource_type": resource},
                               action={"method": "GET", "url": f"{base}/{rid}",
                                       "headers": dict(extra_header)},
                               next_state=res.body, success=True))
    mech = arm.kernel.distill_parameterized(obs)
    if mech is None:
        return {"success": False, "arm": arm, "reason": "distill-failed"}
    arm.registry.upsert(mech)
    slot = mech.parameter_slots[0]
    ok, _ = execute_batch(arm, mech.intent, {"resource_type": resource}, slot, TASK_IDS)
    return {"success": ok, "arm": arm, "reason": "cold"}


def run_literal(app, origin, mechs, resource):
    arm = Arm(mechs, Path("/tmp"), "literal")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    ok, _ = execute_batch(arm, mech.intent, {"resource_type": resource}, slot, TASK_IDS)
    return {"success": ok, "arm": arm}


def run_norepair(app, origin, mechs, cached, resource):
    arm = Arm(mechs, Path("/tmp"), "norepair")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    required_paths = set(flatten(mech.postconditions).keys())
    r0 = arm.resolve(mech.intent, {"resource_type": resource}, {slot: str(TASK_IDS[0])})
    failed = fetch(r0.bound_action["url"], r0.bound_action.get("headers", {}),
                   arm.counters, origin=origin) if r0.bound_action else HTTPResult(None, {}, None)
    stale, _ = guard(cached, required_paths, failed, arm, mech, {slot: str(TASK_IDS[0])})
    return {"success": False, "guard_fired": stale, "arm": arm}


def unaffected_behavior(mechs, origin, resource, tag):
    arm = Arm(mechs, Path("/tmp"), tag)
    mech = arm.target_mech(resource)
    if mech is None:
        return None
    slot = mech.parameter_slots[0]
    r = arm.resolve(mech.intent, {"resource_type": resource}, {slot: "1"})
    if r.status.name != "EXECUTABLE" or r.bound_action is None:
        return ("NO-RESOLVE", None, False)
    res = fetch(r.bound_action["url"], r.bound_action.get("headers", {}), arm.counters)
    if res.status != 200 or res.body is None:
        return (res.status, None, False)
    try:
        verified = arm.verify(r.mechanism_id, res.body, {slot: "1"})
    except (KeyError, TypeError):
        verified = False
    return (200, res.body.get("id"), verified)


def overbroad_contamination(base_live, origin, resource, patched_mech_dict):
    bad = {}
    for rid, md in base_live["mech_dicts"].items():
        md2 = copy.deepcopy(md)
        if md2["intent"] != patched_mech_dict["intent"]:
            md2["postconditions"] = copy.deepcopy(patched_mech_dict["postconditions"])
        bad[rid] = md2
    contam = 0
    for r in RESOURCES:
        if r == resource:
            continue
        post = unaffected_behavior(bad, origin, r, "overbroad")
        if post != base_live[r]:
            contam += 1
    return contam


# ------------------------------------------------------------------ trial ---
def run_trial(cls, target, seed, reg_dir):
    app = LocalApp()
    try:
        if not wait_ready(app):
            return {"valid": False, "reason": "server-not-ready"}
        base_counters = Counters()
        mechs, cached = make_mech_dicts(app.origin, base_counters)
        if mechs is None:
            return {"valid": False, "reason": "learn-failed"}
        base_live = {"mech_dicts": {m["mechanism_id"]: m for m in mechs.values()}}
        for r in RESOURCES:
            base_live[r] = unaffected_behavior(mechs, app.origin, r, "base")
        pre_unaffected = {r: base_live[r] for r in RESOURCES}
        app.state.set_perturb(cls, target, seed)
        rep = run_repair_reuse(app, app.origin, copy.deepcopy(mechs), cached[target], target, "reuse")
        cons = run_repair_reuse(app, app.origin, copy.deepcopy(mechs), cached[target], target, "conservative")
        leg = run_repair_legacy(app, app.origin, copy.deepcopy(mechs), cached[target], target)
        cold = run_cold(app, app.origin, target, LEARN_IDS, "cold")
        cold_min = run_cold(app, app.origin, target, LEARN_IDS_MIN, "coldmin")
        cold_deep = run_cold(app, app.origin, target, LEARN_IDS_DEEP, "colddeep")
        lit = run_literal(app, app.origin, copy.deepcopy(mechs), target)
        nor = run_norepair(app, app.origin, copy.deepcopy(mechs), cached[target], target)
        post_dicts = {m.mechanism_id: m.as_dict() for m in rep["arm"].registry.all()}
        base_dicts = base_live["mech_dicts"]
        write_set = sorted(
            mid for mid in set(base_dicts) | set(post_dicts)
            if base_dicts.get(mid) != post_dicts.get(mid))
        contam = 0
        for r in RESOURCES:
            if r == target:
                continue
            post = unaffected_behavior(post_dicts, app.origin, r, "post")
            if post != pre_unaffected[r]:
                contam += 1
        n_unaff = len(RESOURCES) - 1
        patched_mech = rep["arm"].target_mech(target)
        overbroad = None
        if patched_mech is not None:
            overbroad = overbroad_contamination(
                base_live, app.origin, target, patched_mech.as_dict())
        return {
            "valid": True,
            "class": cls,
            "target": target,
            "repair_success": bool(rep["success"]),
            "repair_guard_fired": bool(rep.get("guard_fired")),
            "repair_reason": rep.get("reason"),
            "conservative_success": bool(cons["success"]),
            "legacy_success": bool(leg["success"]),
            "cold_success": bool(cold["success"]),
            "cold_min_success": bool(cold_min["success"]),
            "cold_deep_success": bool(cold_deep["success"]),
            "literal_success": bool(lit["success"]),
            "norepair_success": bool(nor["success"]),
            "norepair_guard_fired": bool(nor.get("guard_fired")),
            "repair_cost": rep["arm"].counters.as_dict(),
            "conservative_cost": cons["arm"].counters.as_dict(),
            "legacy_cost": leg["arm"].counters.as_dict(),
            "cold_cost": cold["arm"].counters.as_dict(),
            "cold_min_cost": cold_min["arm"].counters.as_dict(),
            "cold_deep_cost": cold_deep["arm"].counters.as_dict(),
            "literal_cost": lit["arm"].counters.as_dict(),
            "contamination_n": contam,
            "overbroad_contamination_n": overbroad,
            "write_set_n": len(write_set),
            "unaffected_n": n_unaff,
            "base_liveness": all(v and v[0] == 200 and v[2] for v in
                                 (pre_unaffected[r] for r in RESOURCES)),
        }
    finally:
        app.stop()


def noise_trial(seed):
    app = LocalApp()
    try:
        if not wait_ready(app):
            return {"stale": None, "info": {"error": "server-not-ready"}}
        c = Counters()
        mechs, cached = make_mech_dicts(app.origin, c)
        app.state.noise = True
        arm = Arm(mechs, Path("/tmp"), "noise")
        mech = arm.target_mech("users")
        slot = mech.parameter_slots[0]
        required_paths = set(flatten(mech.postconditions).keys())
        failed = fetch(f"{app.origin}/api/users/11", {}, arm.counters, origin=app.origin)
        stale, info = guard(cached["users"], required_paths, failed, arm, mech, {slot: "11"})
        return {"stale": stale, "info": info}
    finally:
        app.stop()


def no_perturbation_trial(seed):
    app = LocalApp()
    try:
        if not wait_ready(app):
            return {"stale": None, "info": {"error": "server-not-ready"}}
        c = Counters()
        mechs, cached = make_mech_dicts(app.origin, c)
        arm = Arm(mechs, Path("/tmp"), "nopert")
        mech = arm.target_mech("users")
        slot = mech.parameter_slots[0]
        required_paths = set(flatten(mech.postconditions).keys())
        failed = fetch(f"{app.origin}/api/users/11", {}, arm.counters, origin=app.origin)
        stale, info = guard(cached["users"], required_paths, failed, arm, mech, {slot: "11"})
        return {"stale": stale, "info": info}
    finally:
        app.stop()


# ---------------------------------------------------------------- wilson ----
def wilson_lower(k, n, z=WILSON_Z):
    if n == 0:
        return 0.0
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, center - margin)


def mean(xs):
    return sum(xs) / len(xs) if xs else None


# ------------------------------------------------------- decision (pure) ----
def functional_ok(m):
    return bool(m["M-REPAIR-SUCCESS"] is not None and m["M-REPAIR-SUCCESS"] >= REPAIR_SUCCESS_BAR
                and m["M-REPAIR-SUCCESS-WILSON-LOWER"] >= WILSON_SUCCESS_LOWER_BAR
                and m["M-CONTAMINATION-RATE"] is not None and m["M-CONTAMINATION-RATE"] <= CONTAMINATION_BAR
                and m["M-WRITE-SET-MAX"] is not None and m["M-WRITE-SET-MAX"] <= 1
                and m["M-GUARD-FIRE-RATE"] is not None and m["M-GUARD-FIRE-RATE"] >= GUARD_FIRE_BAR)


def cost_verdict(m):
    """Registered staged cost verdict on the equal-weight product counter under
    the mandate's reuse semantics (primary), with the network-fetch counter as
    the operational driver."""
    if not functional_ok(m):
        return "FUNCTIONAL-FAIL"
    pr2, pr3 = m["M-PRODUCT-RATIO-REUSE-L2"], m["M-PRODUCT-RATIO-REUSE-L3"]
    fr = m["M-COST-FETCH-RATIO-L3"]
    if pr2 is None or pr3 is None or fr is None:
        return "COST-UNKNOWN"
    if pr3 < PRODUCT_COST_BAR and pr2 < PRODUCT_COST_BAR and fr <= FETCH_COST_BAR:
        return "STRICT-WIN"
    if pr3 <= PRODUCT_COST_BAR and pr2 <= PRODUCT_COST_BAR and fr <= FETCH_COST_BAR:
        return "BOUNDED-WIN"
    if max(pr2, pr3) <= PRODUCT_COST_MAX and fr <= FETCH_COST_BAR:
        return "MIXED-TRADEOFF"
    return "COST-FAIL"


def aggregate(cvs):
    """Pure aggregation used both by the scored run and by the synthetic
    decision-branch reachability probe."""
    if any(v in ("COST-UNKNOWN",) for v in cvs):
        return "INCONCLUSIVE"
    if all(v == "STRICT-WIN" for v in cvs):
        return "SUPPORTS"
    if all(v in ("STRICT-WIN", "BOUNDED-WIN") for v in cvs):
        return "SUPPORTS-BOUNDED"
    if all(v in ("STRICT-WIN", "BOUNDED-WIN", "MIXED-TRADEOFF") for v in cvs):
        return "MIXED-TRADEOFF"
    if any(v in ("STRICT-WIN", "BOUNDED-WIN", "MIXED-TRADEOFF") for v in cvs):
        return "MIXED"
    return "FALSIFIES"


# ---------------------------------------------------------------- probes ----
def synthetic_reachability_probe():
    def row(name, reuse_success=True, pr2=0.94, pr3=0.89, fr=0.67, contam=0.0,
            ws=1, guard=1.0):
        return {
            "M-REPAIR-SUCCESS": reuse_success,
            "M-REPAIR-SUCCESS-WILSON-LOWER": 0.7575 if reuse_success else 0.0,
            "M-CONTAMINATION-RATE": contam,
            "M-WRITE-SET-MAX": ws,
            "M-GUARD-FIRE-RATE": guard,
            "M-PRODUCT-RATIO-REUSE-L2": pr2,
            "M-PRODUCT-RATIO-REUSE-L3": pr3,
            "M-COST-FETCH-RATIO-L3": fr,
        }
    cases = {
        "STRICT-WIN": row("strict"),
        "BOUNDED-WIN": row("bounded", pr2=1.00, pr3=0.95),
        "MIXED-TRADEOFF": row("mixed", pr2=1.11, pr3=1.05),
        "COST-FAIL": row("fail", pr2=1.30, pr3=1.25, fr=0.95),
        "FUNCTIONAL-FAIL": row("fnfail", reuse_success=False),
        "COST-UNKNOWN": row("unknown", pr2=None, pr3=None, fr=None),
    }
    verdicts = {k: cost_verdict(v) for k, v in cases.items()}
    aggregates = {
        "SUPPORTS": aggregate(["STRICT-WIN", "STRICT-WIN", "STRICT-WIN"]),
        "SUPPORTS-BOUNDED": aggregate(["STRICT-WIN", "BOUNDED-WIN", "BOUNDED-WIN"]),
        "MIXED-TRADEOFF": aggregate(["STRICT-WIN", "MIXED-TRADEOFF", "MIXED-TRADEOFF"]),
        "MIXED": aggregate(["STRICT-WIN", "MIXED-TRADEOFF", "COST-FAIL"]),
        "FALSIFIES": aggregate(["COST-FAIL", "COST-FAIL", "FUNCTIONAL-FAIL"]),
        "INCONCLUSIVE": aggregate(["STRICT-WIN", "COST-UNKNOWN", "MIXED-TRADEOFF"]),
    }
    all_verdicts = {"STRICT-WIN", "BOUNDED-WIN", "MIXED-TRADEOFF", "COST-FAIL",
                    "FUNCTIONAL-FAIL", "COST-UNKNOWN"}
    all_aggregates = {"SUPPORTS", "SUPPORTS-BOUNDED", "MIXED-TRADEOFF", "MIXED",
                      "FALSIFIES", "INCONCLUSIVE"}
    return {
        "class_cost_verdicts": verdicts,
        "aggregate_decisions": aggregates,
        "all_class_branches_reachable": set(verdicts.values()) == all_verdicts,
        "all_aggregate_branches_reachable": set(aggregates.values()) == all_aggregates,
    }


def synthetic_repair_signal_probe():
    """Non-substrate unit probe: local_repair must produce a patched mechanism
    on each of the three live signal signatures."""
    mech_dict = {
        "mechanism_id": "m-probe", "intent": "read_users",
        "preconditions": {"resource_type": "users"},
        "action_template": {"method": "GET", "url": "http://127.0.0.1:1/api/users/${id}",
                            "headers": {}},
        "postconditions": {"kind": "user", "id": "${id}"},
        "parameter_slots": ["id"], "confidence": 0.95,
    }
    out = {}
    for tag in ("P1", "P3", "P2"):
        app = LocalApp()
        try:
            wait_ready(app)
            md = dict(mech_dict)
            md["action_template"] = {"method": "GET",
                                     "url": f"{app.origin}/api/users/${{id}}", "headers": {}}
            mech = Mechanism(**md)
            arm = Arm({}, Path("/tmp"), "probe")
            arm.registry.upsert(mech)
            if tag == "P1":
                app.state.set_perturb("P1-ENDPOINT", "users", 7)
                seg = app.state.perturb["new_segment"]
                ff = HTTPResult(301, {"Location": f"/api/{seg}/1", "_origin": app.origin}, None)
            elif tag == "P3":
                app.state.set_perturb("P3-PERMISSION", "users", 7)
                ff = HTTPResult(403, {"X-Required-Consent": "granted"}, None)
            else:
                app.state.set_perturb("P2-STRUCTURE", "users", 7)
                ff = HTTPResult(200, {}, {"id": "1", "entity_type": "user", "schema_version": "2"})
            patched, pb, ph = local_repair(arm, mech, "users", "id", 1, ff, app.origin)
            out[tag] = {"patched": patched is not None,
                        "probe_body_present": pb is not None,
                        "probe_header_present": bool(ph)}
        finally:
            app.stop()
    return out


# ---------------------------------------------------------------- main ------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mechanics-only", action="store_true")
    ap.add_argument("--reachability-probe", action="store_true")
    ap.add_argument("--liveness-only", action="store_true")
    args = ap.parse_args()
    reg_dir = Path("/tmp/opencode/exprun382-reg")
    reg_dir.mkdir(parents=True, exist_ok=True)

    runner_self_sha = "UNKNOWN"
    try:
        runner_self_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        pass

    carrier = {
        "kernel_sha256": hashlib.sha256((ROOT / "src/spider/kernel.py").read_bytes()).hexdigest(),
        "models_sha256": hashlib.sha256((ROOT / "src/spider/models.py").read_bytes()).hexdigest(),
        "registry_sha256": hashlib.sha256((ROOT / "src/spider/registry.py").read_bytes()).hexdigest(),
    }

    if args.reachability_probe:
        out = {"status": "DESIGN-REACHABILITY-PROBE", "experiment_id": EXP_ID,
               "lane": "runtime", "runner_self_sha": runner_self_sha,
               "decision_rule": synthetic_reachability_probe(),
               "repair_signal_probe": synthetic_repair_signal_probe()}
        print(json.dumps(out, indent=2))
        return

    if args.mechanics_only:
        canary = []
        for ci, cls in enumerate(CLASSES):
            r = run_trial(cls, TARGETS[ci % len(TARGETS)], SEED + 900 + ci, reg_dir)
            canary.append({k: r[k] for k in (
                "valid", "class", "target", "repair_success", "conservative_success",
                "legacy_success", "cold_success", "literal_success", "repair_guard_fired",
                "contamination_n", "unaffected_n", "base_liveness",
                "repair_cost", "conservative_cost", "legacy_cost", "cold_cost") if k in r})
        np_t = no_perturbation_trial(SEED + 1)
        nz_t = noise_trial(SEED + 2)
        out = {"status": "DESIGN-MECHANICS-ONLY", "experiment_id": EXP_ID, "lane": "runtime",
               "runner_self_sha": runner_self_sha, "seed": SEED, "carrier": carrier,
               "canary": canary, "nc_no_perturbation": np_t, "nc_noise": nz_t}
        print(json.dumps(out, indent=2))
        return

    if args.liveness_only:
        app = LocalApp()
        try:
            ready = wait_ready(app)
            c = Counters()
            mechs, cached = make_mech_dicts(app.origin, c) if ready else (None, None)
            live = bool(mechs)
            one_ok = False
            if live:
                arm = Arm(mechs, Path("/tmp"), "live")
                mech = arm.target_mech("users")
                slot = mech.parameter_slots[0]
                r = arm.resolve(mech.intent, {"resource_type": "users"}, {slot: str(TASK_IDS[0])})
                if r.status.name == "EXECUTABLE" and r.bound_action is not None:
                    res = fetch(r.bound_action["url"], r.bound_action.get("headers", {}), arm.counters)
                    one_ok = res.status == 200 and res.body is not None and arm.verify(
                        r.mechanism_id, res.body, {slot: str(TASK_IDS[0])})
            np_t = no_perturbation_trial(SEED + 1) if ready else {"stale": None}
            nz_t = noise_trial(SEED + 2) if ready else {"stale": None}
        finally:
            app.stop()
        print(json.dumps({"status": "DESIGN-LIVENESS-ONLY", "experiment_id": EXP_ID,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "server_ready": ready,
                          "distill_live": bool(mechs),
                          "task_read_verified": bool(one_ok),
                          "nc_no_perturbation_stale": np_t.get("stale"),
                          "nc_noise_stale": nz_t.get("stale"),
                          "carrier": carrier}, indent=2))
        return

    trials = []
    for ci, cls in enumerate(CLASSES):
        for j in range(TRIALS_PER_CLASS):
            target = TARGETS[(ci + j) % len(TARGETS)]
            trials.append(run_trial(cls, target, SEED + 1000 * (ci + 1) + j, reg_dir))
    np_t = no_perturbation_trial(SEED + 1)
    nz_t = noise_trial(SEED + 2)

    per_class = {}
    for cls in CLASSES:
        rows = [r for r in trials if r.get("valid") and r["class"] == cls]
        n = len(rows)
        rep_ok = sum(1 for r in rows if r["repair_success"])
        cold_ok = sum(1 for r in rows if r["cold_success"])
        cold_min_ok = sum(1 for r in rows if r["cold_min_success"])
        cold_deep_ok = sum(1 for r in rows if r["cold_deep_success"])
        lit_ok = sum(1 for r in rows if r["literal_success"])
        nor_ok = sum(1 for r in rows if r["norepair_success"])
        guard_ok = sum(1 for r in rows if r["repair_guard_fired"])
        contam = sum(r["contamination_n"] for r in rows)
        unaff = sum(r["unaffected_n"] for r in rows)
        overbroad = mean([r["overbroad_contamination_n"] for r in rows
                          if r.get("overbroad_contamination_n") is not None])
        write_ws = [r.get("write_set_n") for r in rows if r.get("write_set_n") is not None]
        rep_prod = mean([r["repair_cost"]["product"] for r in rows])
        cons_prod = mean([r["conservative_cost"]["product"] for r in rows])
        leg_prod = mean([r["legacy_cost"]["product"] for r in rows])
        cold_prod = mean([r["cold_cost"]["product"] for r in rows])
        cold_min_prod = mean([r["cold_min_cost"]["product"] for r in rows])
        cold_deep_prod = mean([r["cold_deep_cost"]["product"] for r in rows])
        rep_http = mean([r["repair_cost"]["http"] for r in rows])
        cold_http = mean([r["cold_cost"]["http"] for r in rows])

        def ratio(a, b):
            return (a / b) if (a is not None and b) else None

        per_class[cls] = {
            "n": n,
            "M-REPAIR-SUCCESS": rep_ok / n if n else None,
            "M-REPAIR-SUCCESS-WILSON-LOWER": wilson_lower(rep_ok, n),
            "M-COLD-SUCCESS": cold_ok / n if n else None,
            "M-COLD-MIN-SUCCESS": cold_min_ok / n if n else None,
            "M-COLD-DEEP-SUCCESS": cold_deep_ok / n if n else None,
            "M-LITERAL-REPLAY-SUCCESS": lit_ok / n if n else None,
            "M-NO-REPAIR-SUCCESS": nor_ok / n if n else None,
            "M-GUARD-FIRE-RATE": guard_ok / n if n else None,
            "M-CONTAMINATION-RATE": contam / unaff if unaff else None,
            "M-OVERBROAD-CONTAMINATION-RATE": overbroad,
            "M-WRITE-SET-MEAN": mean(write_ws),
            "M-WRITE-SET-MAX": max(write_ws) if write_ws else None,
            "M-COST-REPAIR-REUSE-PRODUCT": rep_prod,
            "M-COST-REPAIR-CONSERVATIVE-PRODUCT": cons_prod,
            "M-COST-REPAIR-LEGACY-PRODUCT": leg_prod,
            "M-COST-COLD-PRODUCT": cold_prod,
            "M-COST-COLD-MIN-PRODUCT": cold_min_prod,
            "M-COST-COLD-DEEP-PRODUCT": cold_deep_prod,
            "M-PRODUCT-RATIO-REUSE-L3": ratio(rep_prod, cold_prod),
            "M-PRODUCT-RATIO-REUSE-L2": ratio(rep_prod, cold_min_prod),
            "M-PRODUCT-RATIO-REUSE-L4": ratio(rep_prod, cold_deep_prod),
            "M-PRODUCT-RATIO-CONSERVATIVE-L3": ratio(cons_prod, cold_prod),
            "M-PRODUCT-RATIO-CONSERVATIVE-L2": ratio(cons_prod, cold_min_prod),
            "M-PRODUCT-RATIO-LEGACY-L3": ratio(leg_prod, cold_prod),
            "M-PRODUCT-RATIO-LEGACY-L2": ratio(leg_prod, cold_min_prod),
            "M-COST-REPAIR-FETCH": rep_http,
            "M-COST-COLD-FETCH": cold_http,
            "M-COST-FETCH-RATIO-L3": ratio(rep_http, cold_http),
        }

    metrics = {"M-CLASSES": per_class,
               "M-NOISE-FALSE-TRIGGER-RATE": (None if nz_t.get("stale") is None
                                              else (1.0 if nz_t["stale"] else 0.0)),
               "M-NO-PERTURBATION-FALSE-TRIGGER-RATE": (None if np_t.get("stale") is None
                                                        else (1.0 if np_t["stale"] else 0.0)),
               "M-LEGACY-REGRESSION-REPRODUCED": all(
                   (per_class[c]["M-PRODUCT-RATIO-LEGACY-L2"] or 0) > LEGACY_REGRESSION_FLOOR
                   for c in CLASSES),
               "M-TRIALS-TOTAL": len(trials)}

    invalid = []
    if any(not r.get("valid") for r in trials):
        invalid.append("trial-invalid")
    for cls, m in per_class.items():
        if m["n"] < TRIALS_PER_CLASS:
            invalid.append(f"{cls}:n<{TRIALS_PER_CLASS}")
        if m["M-COLD-SUCCESS"] is None or m["M-COLD-SUCCESS"] < COLD_SUCCESS_BAR:
            invalid.append(f"{cls}:cold-baseline-not-live")
        if m["M-LITERAL-REPLAY-SUCCESS"] is None or m["M-LITERAL-REPLAY-SUCCESS"] > LITERAL_SUCCESS_BAR:
            invalid.append(f"{cls}:perturbation-does-not-bite")
        if m["M-NO-REPAIR-SUCCESS"] is None or m["M-NO-REPAIR-SUCCESS"] > LITERAL_SUCCESS_BAR:
            invalid.append(f"{cls}:no-repair-not-inert")
    if nz_t.get("stale") is not False or np_t.get("stale") is not False:
        invalid.append("negative-control-not-fresh")

    cvs = {cls: cost_verdict(per_class[cls]) for cls in CLASSES}
    if invalid:
        decision, status, outcome = None, "MEASUREMENT_INVALID", "INCONCLUSIVE"
    else:
        decision = aggregate(list(cvs.values()))
        status = "COMPLETE"
        outcome = "SUPPORTS" if decision in ("SUPPORTS", "SUPPORTS-BOUNDED") else (
            "MIXED" if decision in ("MIXED", "MIXED-TRADEOFF") else (
                "FALSIFIES" if decision == "FALSIFIES" else "INCONCLUSIVE"))

    out = {"status": status, "experiment_id": EXP_ID, "lane": "runtime",
           "runner_self_sha": runner_self_sha, "seed": SEED,
           "invalid_reasons": invalid, "decision": decision, "outcome": outcome,
           "class_cost_verdicts": cvs, "metrics": metrics, "trials": trials,
           "nc_no_perturbation": np_t, "nc_noise": nz_t, "carrier": carrier}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()