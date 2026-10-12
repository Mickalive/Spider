#!/usr/bin/env python3
"""DESIGN-time satisfiability probe for EXP-RUNTIME-38182129488.

Substrate class SBA-CREDENTIAL-FREE-V2 (Session-Binding-Amortized), REUSED
verbatim from the frozen predecessor EXP-RUNTIME-38169622704 (same RUN_SEED,
same server, same derivations, same families/K/novelty ladder, same 48-bit
binding, same endpoint semantics).

Scientific question (director mandate on C-MEAS-VALID):
  Does the certified (K-1)/K dynamic range survive a comparator that is
  *memoryful* within a session -- i.e. one that retains action/response
  receipts across tasks -- or was the predecessor's range an artifact of the
  memoryless-per-task construction of its comparators (B-COLD-RE-DERIVE,
  B-RETRIEVAL-SHAPED)?

This harness instantiates a pre-declared ordered MEMORY LATTICE of comparators
that differ ONLY in how much within-session memory they retain, and classifies
the resulting robustness as ROBUST / PARTIAL / COLLAPSED / MEASUREMENT_INVALID.

This probe is NON-OUTCOME-BEARING.  It verifies:
  * the stdlib HTTP transport answers on 127.0.0.1;
  * protocol semantics/invariants of the SBA construction;
  * arm liveness on ONE session per (arm, family, novelty band);
  * the closed-form predictions of the memory lattice;
  * decision-branch reachability over synthetic worlds;
  * determinism (two runs byte-identical).

It does NOT run the scored N-session matrix that produces the scientific
measurement.  stdlib only.
"""
from __future__ import annotations

import hashlib
import json
import threading
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

RUN_SEED = "SPIDER-RUNTIME-SBA-V2-2026"  # frozen predecessor construction
FAMILIES = {"F1-RECORDS": 8, "F2-WIDGETS": 10}
NOVELTIES = [0.0, 0.25, 0.5, 0.75]
SCORED_BAND = 0.50
COMPARATOR_MAX = 0.95
CORRECTNESS_FLOOR = 0.80
MARGIN_FLOOR = 0.05
COUNTER_DIMS = ["http_calls", "retrieval_calls", "verification_calls", "repair_calls"]
MIN_DISTINCT_DIMS = 2
BINDING_HEX = 12  # 48-bit

# Memory-lattice arms (ordered by retained-memory capacity).
ARMS = [
    "T-AMORTIZED-DISCOVERY",       # treatment
    "PC-EXACT-REPLAY",             # positive control (oracle binding)
    "B-KNOWLEDGE-NO-MEMORY",       # M-K: semantics, per-task fresh session
    "B-COLD-RE-DERIVE",            # M0: no memory
    "B-RETRIEVAL-SHAPED",          # M0 + stale retrieval
    "B-MEMORY-STATE",              # M1: GET-observation state, no receipts
    "B-MEMORY-WINDOW-1",           # M2a: last 1 commit receipt
    "B-MEMORY-WINDOW-2",           # M2b: last 2 commit receipts
    "B-MEMORY-RECEIPT",            # M3: full commit-receipt log (PRIMARY)
    "B-RETRIEVAL-MEMORYFUL",       # M3 + stale retrieval
]

# Pre-declared comparator classes and the primary comparator.
COMPARATOR_CLASSES = {
    "M0": ["B-COLD-RE-DERIVE", "B-RETRIEVAL-SHAPED"],
    "M1": ["B-MEMORY-STATE"],
    "M2": ["B-MEMORY-WINDOW-1", "B-MEMORY-WINDOW-2"],
    "M3": ["B-MEMORY-RECEIPT", "B-RETRIEVAL-MEMORYFUL"],
}
PRIMARY_COMPARATOR = "B-MEMORY-RECEIPT"
WEAKER_COMPARATORS = ["B-MEMORY-STATE", "B-MEMORY-WINDOW-1", "B-MEMORY-WINDOW-2"]


def h(*parts) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()


def counter_distinctness(c_t, c_c) -> int:
    return sum(1 for d in COUNTER_DIMS if c_t[d] != c_c[d])


def binding_uniqueness_check(n_sessions=20) -> dict:
    seen = {}
    collisions = 0
    sampled = 0
    for family in FAMILIES:
        for nov in NOVELTIES:
            for idx in range(n_sessions):
                sampled += 1
                b = session_binding(family, nov, idx)
                if b in seen and seen[b] != (family, nov, idx):
                    collisions += 1
                seen[b] = (family, nov, idx)
    return {"sampled": sampled, "collisions": collisions,
            "binding_bits": BINDING_HEX * 4}


def server_secret() -> str:
    return h(RUN_SEED, "server_secret")[:32]


def _drv(family: str, novelty: float, idx: int, label: str, n: int) -> str:
    return h(server_secret(), family, repr(novelty), idx, label)[:n]


def session_token(family, novelty, idx):
    return _drv(family, novelty, idx, "token", 16)


def session_binding(family, novelty, idx):
    return _drv(family, novelty, idx, "binding", BINDING_HEX)


def schema_epoch_value(family, novelty, idx):
    return _drv(family, novelty, idx, "schema", 8)


def public_resource(family, novelty, i):
    return h(server_secret(), family, repr(novelty), "res", i)[:10]


def k_of(family):
    return FAMILIES[family]


def chain_index(novelty, k):
    return k - 3 if novelty == 0.5 else k - 1


def precursor_index(novelty, k):
    return k - 4 if novelty == 0.5 else k - 3


def chain_requires_binding(novelty):
    return novelty >= SCORED_BAND


# --------------------------------------------------------------------------
# server (frozen; identical to EXP-RUNTIME-38169622704)
# --------------------------------------------------------------------------
class State:
    def __init__(self, expose_binding=False):
        self.lock = threading.Lock()
        self.sessions = {}
        self.next_idx = 0
        self.expose_binding = expose_binding

    def new_session(self, family, novelty):
        with self.lock:
            idx = self.next_idx
            self.next_idx += 1
            tok = session_token(family, novelty, idx)
            s = {
                "family": family, "novelty": novelty, "idx": idx, "token": tok,
                "binding": session_binding(family, novelty, idx),
                "schema": schema_epoch_value(family, novelty, idx),
                "committed": {},
            }
            self.sessions[tok] = s
            return s


class Handler(BaseHTTPRequestHandler):
    state: State = None  # injected

    def log_message(self, *a):
        pass

    def _send(self, code, obj):
        body = json.dumps(obj, sort_keys=True).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/healthz":
            return self._send(200, {"status": "ok"})
        parts = path.strip("/").split("/")
        if len(parts) == 4 and parts[:2] == ["api", "v1"] and parts[3] == "session":
            family = parts[2]
            if family not in FAMILIES:
                return self._send(404, {"error": "bad_family"})
            novelty = self._query_novelty()
            s = self.state.new_session(family, novelty)
            resp = {"session_token": s["token"], "schema_epoch": s["schema"], "epoch": s["idx"]}
            if self.state.expose_binding:
                resp["binding"] = s["binding"]
            return self._send(200, resp)
        if len(parts) == 5 and parts[:2] == ["api", "v1"] and parts[3] == "task":
            family = parts[2]
            tok = self.headers.get("X-Session", "")
            s = self.state.sessions.get(tok)
            if s is None:
                return self._send(400, {"error": "bad_session"})
            try:
                i = int(parts[4])
            except ValueError:
                return self._send(400, {"error": "bad_index"})
            k = k_of(family)
            if not (0 <= i < k):
                return self._send(400, {"error": "bad_index"})
            ci = chain_index(s["novelty"], k)
            is_chain = i == ci
            requires = s["novelty"] >= 0.25
            if is_chain and chain_requires_binding(s["novelty"]):
                resource = None
            else:
                resource = public_resource(family, s["novelty"], i)
            return self._send(200, {
                "index": i, "requires_schema": requires,
                "resource_id": resource, "is_chain": is_chain,
            })
        return self._send(404, {"error": "not_found"})

    def _query_novelty(self):
        if "?" not in self.path:
            return 0.5
        qs = self.path.split("?", 1)[1]
        for kv in qs.split("&"):
            if kv.startswith("novelty="):
                try:
                    return float(kv.split("=", 1)[1])
                except ValueError:
                    return 0.5
        return 0.5

    def do_POST(self):
        parts = self.path.strip("/").split("/")
        if not (len(parts) == 4 and parts[:2] == ["api", "v1"] and parts[3] == "commit"):
            return self._send(404, {"error": "not_found"})
        family = parts[2]
        if family not in FAMILIES:
            return self._send(404, {"error": "bad_family"})
        n = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(n).decode() or "{}")
        except (ValueError, UnicodeDecodeError):
            return self._send(400, {"error": "bad_body"})
        tok = body.get("session_token")
        s = self.state.sessions.get(tok)
        if s is None:
            return self._send(400, {"error": "bad_session"})
        idx = body.get("index")
        if not isinstance(idx, int) or not (0 <= idx < k_of(family)):
            return self._send(400, {"error": "bad_index"})
        if idx in s["committed"]:
            return self._send(409, {"error": "already_committed"})
        if s["novelty"] >= 0.25 and body.get("schema_epoch") != s["schema"]:
            return self._send(400, {"error": "schema_required"})
        k = k_of(family)
        ci = chain_index(s["novelty"], k)
        pi = precursor_index(s["novelty"], k)
        resource = body.get("resource_id")
        if idx == ci and chain_requires_binding(s["novelty"]):
            expected = s["binding"]
        else:
            expected = public_resource(family, s["novelty"], idx)
        if resource != expected:
            return self._send(400, {"error": "bad_resource"})
        s["committed"][idx] = True
        receipt = {"index": idx, "family": family, "epoch": s["idx"]}
        if idx == pi and not s["committed"].get("__revealed__"):
            s["committed"]["__revealed__"] = True
            receipt["chain_resource_id"] = s["binding"]
        return self._send(200, {"receipt": receipt})

    def do_PUT(self):
        return self._send(405, {"error": "method_not_allowed"})


def start_server(expose_binding=False):
    state = State(expose_binding=expose_binding)
    handler = type("H", (Handler,), {"state": state})
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd, state, f"http://127.0.0.1:{httpd.server_address[1]}"


def http_get(url, token=None):
    req = Request(url, method="GET")
    if token:
        req.add_header("X-Session", token)
    try:
        with urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode())
    except HTTPError as e:
        return e.code, json.loads(e.read().decode())


def http_post(url, payload):
    data = json.dumps(payload).encode()
    req = Request(url, data=data, method="POST", headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode())
    except HTTPError as e:
        return e.code, json.loads(e.read().decode())


def _mk(base, family, novelty, counters):
    def sess():
        counters["http_calls"] += 1
        st, b = http_get(f"{base}/api/v1/{family}/session?novelty={novelty}")
        assert st == 200
        return b

    def task(tok, i):
        counters["http_calls"] += 1
        st, b = http_get(f"{base}/api/v1/{family}/task/{i}", token=tok)
        assert st == 200
        return b

    def commit(tok, i, schema, resource):
        counters["http_calls"] += 1
        return http_post(f"{base}/api/v1/{family}/commit", {
            "session_token": tok, "index": i,
            "schema_epoch": schema, "resource_id": resource,
        })

    return sess, task, commit


def _scan_chains(receipts):
    """Generic scan of retained receipts for a chain_resource_id field."""
    cand = None
    for r in receipts:
        if isinstance(r, dict) and r.get("chain_resource_id"):
            cand = r["chain_resource_id"]
    return cand


# --------------------------------------------------------------------------
# arms (memory lattice).  Each arm is a distinct memory policy over the
# IDENTICAL frozen substrate.
# --------------------------------------------------------------------------
def run_arm(base, state, arm, family, novelty):
    k = k_of(family)
    counters = {d: 0 for d in COUNTER_DIMS}
    successes = 0
    ci = chain_index(novelty, k)
    pi = precursor_index(novelty, k)
    chain_active = chain_requires_binding(novelty)
    sess, task, commit = _mk(base, family, novelty, counters)

    if arm == "T-AMORTIZED-DISCOVERY":
        s = sess()
        receipts = {}
        for i in range(k):
            d = task(s["session_token"], i)
            res = d["resource_id"]
            if d["is_chain"] and chain_active:
                res = receipts[pi]["receipt"]["chain_resource_id"]
            counters["verification_calls"] += 1
            st, b = commit(s["session_token"], i, s["schema_epoch"], res)
            if st == 200:
                successes += 1
                receipts[i] = b
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    if arm == "PC-EXACT-REPLAY":
        s = sess()
        binding = session_binding(family, novelty, s["epoch"])
        for i in range(k):
            d = task(s["session_token"], i)
            res = binding if (d["is_chain"] and chain_active) else d["resource_id"]
            counters["verification_calls"] += 1
            st, b = commit(s["session_token"], i, s["schema_epoch"], res)
            if st == 200:
                successes += 1
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    if arm == "B-KNOWLEDGE-NO-MEMORY":
        # knows the chain rule but starts a fresh session per task and keeps
        # nothing across tasks -> cannot reach the same-session precursor.
        for i in range(k):
            s = sess()
            d = task(s["session_token"], i)
            res = d["resource_id"]
            counters["verification_calls"] += 1
            st, b = commit(s["session_token"], i, s["schema_epoch"], res)
            if st == 200:
                successes += 1
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    if arm == "B-COLD-RE-DERIVE":
        for i in range(k):
            s = sess()
            d = task(s["session_token"], i)
            res = d["resource_id"]
            if d["is_chain"] and chain_active:
                res = s.get("binding")  # only non-None under NC-MECHANISM-OFF
            counters["verification_calls"] += 1
            st, b = commit(s["session_token"], i, s["schema_epoch"], res)
            if st == 200:
                successes += 1
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    if arm == "B-RETRIEVAL-SHAPED":
        foreign = session_binding(family, novelty, 999999)
        for i in range(k):
            s = sess()
            d = task(s["session_token"], i)
            counters["retrieval_calls"] += 1
            res = d["resource_id"]
            if d["is_chain"] and chain_active:
                res = foreign
            counters["verification_calls"] += 1
            st, b = commit(s["session_token"], i, s["schema_epoch"], res)
            if st == 200:
                successes += 1
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    if arm == "B-MEMORY-STATE":
        # one session; retains observed GET resource_id values only (no receipts)
        s = sess()
        last_state = None
        for i in range(k):
            d = task(s["session_token"], i)
            if d["resource_id"] is not None:
                last_state = d["resource_id"]
            res = d["resource_id"]
            if d["is_chain"] and chain_active:
                res = last_state
            counters["verification_calls"] += 1
            st, b = commit(s["session_token"], i, s["schema_epoch"], res)
            if st == 200:
                successes += 1
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    if arm in ("B-MEMORY-WINDOW-1", "B-MEMORY-WINDOW-2"):
        m = 1 if arm.endswith("1") else 2
        s = sess()
        window = deque(maxlen=m)
        for i in range(k):
            d = task(s["session_token"], i)
            res = d["resource_id"]
            if d["is_chain"] and chain_active:
                res = _scan_chains(window)
            counters["verification_calls"] += 1
            st, b = commit(s["session_token"], i, s["schema_epoch"], res)
            if st == 200:
                successes += 1
                window.append(b["receipt"])
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    if arm == "B-MEMORY-RECEIPT":
        s = sess()
        log = []
        for i in range(k):
            d = task(s["session_token"], i)
            res = d["resource_id"]
            if d["is_chain"] and chain_active:
                res = _scan_chains(log)
            counters["verification_calls"] += 1
            st, b = commit(s["session_token"], i, s["schema_epoch"], res)
            if st == 200:
                successes += 1
                log.append(b["receipt"])
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    if arm == "B-RETRIEVAL-MEMORYFUL":
        s = sess()
        log = []
        foreign = session_binding(family, novelty, 999999)
        for i in range(k):
            d = task(s["session_token"], i)
            counters["retrieval_calls"] += 1
            res = d["resource_id"]
            if d["is_chain"] and chain_active:
                res = _scan_chains(log) or foreign  # memory preferred, stale fallback
            counters["verification_calls"] += 1
            st, b = commit(s["session_token"], i, s["schema_epoch"], res)
            if st == 200:
                successes += 1
                log.append(b["receipt"])
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    raise AssertionError(arm)


# --------------------------------------------------------------------------
# controls (declared nulls, measured in probe mode)
# --------------------------------------------------------------------------
def run_no_discovery_direct(base, family, novelty):
    """NC-NO-DISCOVERY-DIRECT: valid session but ignores schema_epoch/receipts."""
    k = k_of(family)
    counters = {d: 0 for d in COUNTER_DIMS}
    successes = 0
    sess, task, commit = _mk(base, family, novelty, counters)
    s = sess()
    for i in range(k):
        d = task(s["session_token"], i)
        st, _ = commit(s["session_token"], i, "", d["resource_id"])
        if st == 200:
            successes += 1
    return successes, k, counters


def run_memory_off(base, family, novelty):
    """NC-MEMORY-OFF: identical to B-MEMORY-RECEIPT but the receipt log is
    reset after every task.  Must degrade to the M0 rate; this isolates the
    *cause* of the M3 success (receipt retention)."""
    k = k_of(family)
    counters = {d: 0 for d in COUNTER_DIMS}
    successes = 0
    chain_active = chain_requires_binding(novelty)
    sess, task, commit = _mk(base, family, novelty, counters)
    s = sess()
    for i in range(k):
        d = task(s["session_token"], i)
        log = []  # reset every task
        res = d["resource_id"]
        if d["is_chain"] and chain_active:
            res = _scan_chains(log)
        counters["verification_calls"] += 1
        st, b = commit(s["session_token"], i, s["schema_epoch"], res)
        if st == 200:
            successes += 1
            log.append(b["receipt"])
        elif st == 400:
            counters["repair_calls"] += 1
    return successes, k, counters


def run_retrieval_redundant(base, family, novelty):
    """NC-RETRIEVAL-REDUNDANT: full receipt memory, and every chain task is
    additionally offered the correct (foreign) stale binding.  Memory must
    remain the cause; result must stay at the M3 rate."""
    k = k_of(family)
    counters = {d: 0 for d in COUNTER_DIMS}
    successes = 0
    chain_active = chain_requires_binding(novelty)
    sess, task, commit = _mk(base, family, novelty, counters)
    s = sess()
    log = []
    foreign = session_binding(family, novelty, 999999)
    for i in range(k):
        d = task(s["session_token"], i)
        counters["retrieval_calls"] += 1
        res = d["resource_id"]
        if d["is_chain"] and chain_active:
            res = _scan_chains(log)  # memory strictly preferred
        counters["verification_calls"] += 1
        st, b = commit(s["session_token"], i, s["schema_epoch"], res)
        if st == 200:
            successes += 1
            log.append(b["receipt"])
        elif st == 400:
            counters["repair_calls"] += 1
    return successes, k, counters


def run_reveal_order_flipped(base, family, novelty):
    """NC-REVEAL-ORDER-FLIPPED: full receipt memory, but the chain task is
    committed BEFORE its precursor in the same session.  At chain time the
    log contains no chain_resource_id, so the chain must fail; this isolates
    the precursor first-commit reveal as the cause of the M3 success."""
    k = k_of(family)
    counters = {d: 0 for d in COUNTER_DIMS}
    successes = 0
    chain_active = chain_requires_binding(novelty)
    sess, task, commit = _mk(base, family, novelty, counters)
    s = sess()
    ci = chain_index(novelty, k)
    pi = precursor_index(novelty, k)
    order = [i for i in range(k) if i not in (ci, pi)] + [ci, pi]
    log = []
    for i in order:
        d = task(s["session_token"], i)
        res = d["resource_id"]
        if d["is_chain"] and chain_active:
            res = _scan_chains(log)
        counters["verification_calls"] += 1
        st, b = commit(s["session_token"], i, s["schema_epoch"], res)
        if st == 200:
            successes += 1
            log.append(b["receipt"])
        elif st == 400:
            counters["repair_calls"] += 1
    return successes, k, counters


def capacity_threshold(liveness, family, nov):
    """Smallest retained-receipt capacity at which the range closes for a
    (family, band).  Capacity is the number of retained commit receipts the
    comparator scans: B-MEMORY-STATE=0, window-1=1, window-2=2, receipt=full.
    Returns None if the range never closes by capacity<=2 (full-memory cmp
    is evaluated separately)."""
    t = liveness["T-AMORTIZED-DISCOVERY"][family][str(nov)]["rate"]
    ladder = [("B-MEMORY-STATE", 0),
              ("B-MEMORY-WINDOW-1", 1),
              ("B-MEMORY-WINDOW-2", 2)]
    for arm, cap in ladder:
        r = liveness[arm][family][str(nov)]["rate"]
        if (t - r) < MARGIN_FLOOR:
            return cap
    return None


# --------------------------------------------------------------------------
# protocol invariants (frozen; identical to predecessor)
# --------------------------------------------------------------------------
def protocol_invariants(base, family="F1-RECORDS", novelty=0.5):
    out = {}
    k = k_of(family)
    st, s = http_get(f"{base}/api/v1/{family}/session?novelty={novelty}")
    out["session_never_reveals_binding"] = st == 200 and "binding" not in s
    tok = s["session_token"]
    binding = session_binding(family, novelty, s["epoch"])
    out["no_binding_in_session_body"] = binding not in json.dumps(s, sort_keys=True)
    task_bodies = [http_get(f"{base}/api/v1/{family}/task/{i}", token=tok)[1]
                   for i in range(k)]
    out["no_binding_in_task_bodies"] = all(
        binding not in json.dumps(b, sort_keys=True) for b in task_bodies)
    st, d_chain = http_get(f"{base}/api/v1/{family}/task/{chain_index(novelty, k)}", token=tok)
    out["chain_task_resource_null"] = st == 200 and d_chain["resource_id"] is None and d_chain["is_chain"]
    st, b = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": chain_index(novelty, k),
        "schema_epoch": s["schema_epoch"], "resource_id": "0" * BINDING_HEX,
    })
    out["wrong_binding_400_no_leak"] = st == 400 and "chain_resource_id" not in b
    out["no_binding_in_error_body"] = binding not in json.dumps(b, sort_keys=True)
    st, b = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": precursor_index(novelty, k),
        "schema_epoch": s["schema_epoch"],
        "resource_id": public_resource(family, novelty, precursor_index(novelty, k)),
    })
    out["precursor_reveals_binding_once"] = (
        st == 200 and b["receipt"].get("chain_resource_id") == session_binding(family, novelty, s["epoch"]))
    st, b = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": precursor_index(novelty, k),
        "schema_epoch": s["schema_epoch"],
        "resource_id": public_resource(family, novelty, precursor_index(novelty, k)),
    })
    out["precursor_recommit_409_no_reveal"] = st == 409 and "chain_resource_id" not in b
    st, b = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": chain_index(novelty, k),
        "schema_epoch": s["schema_epoch"],
        "resource_id": session_binding(family, novelty, s["epoch"]),
    })
    out["correct_binding_200"] = st == 200
    st, b = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": chain_index(novelty, k),
        "schema_epoch": s["schema_epoch"],
        "resource_id": session_binding(family, novelty, s["epoch"]),
    })
    out["chain_binding_single_use_409"] = st == 409
    return out


# --------------------------------------------------------------------------
# robustness certificate + memory-lattice branch classifier
# --------------------------------------------------------------------------
def mem_certifies(comp_rate, t_rate, all_rates, matched_correctness):
    """Robustness certificate for ONE comparator at ONE (family, novelty).

    Requires: comparator below the ceiling, no arm below the correctness
    floor, matched correctness at the treatment level, and a >= MARGIN_FLOOR
    treatment margin over the comparator.  Counter distinctness is reported as
    a diagnostic only (it is not required for a band certificate, to avoid an
    empty PARTIAL branch when a memoryful comparator reproduces the treatment
    counters exactly -- a counter-equivalence is itself an interpretable
    finding).
    """
    return (
        comp_rate < COMPARATOR_MAX
        and all(r >= CORRECTNESS_FLOOR for r in all_rates)
        and matched_correctness >= CORRECTNESS_FLOOR
        and (t_rate - comp_rate) >= MARGIN_FLOOR
    )


def classify_mem(world):
    """Frozen decision rule over the assembled gate world.

    Precedence:
      gates fail                                  -> MEASUREMENT_INVALID
      primary comparator (full receipt memory)    -> ROBUST
      any weaker comparator certifies             -> PARTIAL
      otherwise                                   -> COLLAPSED
    """
    if not world["gates_pass"]:
        return "MEASUREMENT_INVALID"
    if world["robust_certified"]:
        return "ROBUST"
    if world["partial_certified"]:
        return "PARTIAL"
    return "COLLAPSED"


def branch_reachability_mem():
    """Construct one synthetic world per decision label (all four reachable)."""
    worlds = {
        "ROBUST": classify_mem({
            "gates_pass": True, "robust_certified": True, "partial_certified": True}),
        "PARTIAL": classify_mem({
            "gates_pass": True, "robust_certified": False, "partial_certified": True}),
        "COLLAPSED": classify_mem({
            "gates_pass": True, "robust_certified": False, "partial_certified": False}),
        "MEASUREMENT_INVALID": classify_mem({
            "gates_pass": False, "robust_certified": False, "partial_certified": False}),
    }
    return worlds


def _rates_at(liveness, family, nov):
    return [liveness[a][family][str(nov)]["rate"] for a in ARMS]


def assess_memory_lattice(liveness):
    """Evaluate mem_certifies() for every comparator class and label the world.

    Uses the probe's single-session per-cell rates -- a closed-form
    *prediction*, not the scored measurement.
    """
    detail = {}
    robust = False
    partial = False
    for comp in [c for cls in COMPARATOR_CLASSES.values() for c in cls]:
        detail[comp] = {}
        for family in FAMILIES:
            for nov in [n for n in NOVELTIES if n >= SCORED_BAND]:
                t_rate = liveness["T-AMORTIZED-DISCOVERY"][family][str(nov)]["rate"]
                comp_rate = liveness[comp][family][str(nov)]["rate"]
                all_rates = _rates_at(liveness, family, nov)
                matched = t_rate
                ok = mem_certifies(comp_rate, t_rate, all_rates, matched)
                detail[comp][f"{family}|{nov}"] = {
                    "comparator_rate": comp_rate, "t_rate": t_rate,
                    "margin": round(t_rate - comp_rate, 6),
                    "min_arm_rate": min(all_rates), "certifies": ok}
                if comp == PRIMARY_COMPARATOR and ok:
                    robust = True
                if comp in WEAKER_COMPARATORS and ok:
                    partial = True
    world = {"gates_pass": True, "robust_certified": robust,
             "partial_certified": partial}
    return {"detail": detail, "world": world, "decision": classify_mem(world)}


# --------------------------------------------------------------------------
# main probe (DESIGN; non-outcome-bearing)
# --------------------------------------------------------------------------
def run_probe():
    out = {"seed": RUN_SEED, "families": FAMILIES, "novelties": NOVELTIES,
           "scored_band": SCORED_BAND, "arms": ARMS,
           "primary_comparator": PRIMARY_COMPARATOR}
    httpd, state, base = start_server(expose_binding=False)
    try:
        out["checks"] = {"transport_stdlib_http": False}
        st, _ = http_get(f"{base}/healthz")
        out["checks"]["transport_stdlib_http"] = st == 200
        out["checks"]["protocol_invariants"] = protocol_invariants(base)
        out["checks"]["all_protocol_invariants_pass"] = all(
            out["checks"]["protocol_invariants"].values())

        liveness = {}
        for arm in ARMS:
            liveness[arm] = {}
            for family in FAMILIES:
                liveness[arm][family] = {}
                for nov in NOVELTIES:
                    httpd_i, state_i, base_i = start_server(expose_binding=False)
                    try:
                        succ, counters = run_arm(base_i, state_i, arm, family, nov)
                    finally:
                        httpd_i.shutdown()
                    k = k_of(family)
                    liveness[arm][family][str(nov)] = {
                        "successes": succ, "k": k, "rate": succ / k, "counters": counters,
                    }
        out["arm_liveness"] = liveness

        # treatment + positive-control liveness
        out["checks"]["treatment_live_all_novelties"] = all(
            liveness["T-AMORTIZED-DISCOVERY"][f][str(n)]["rate"] == 1.0
            for f in FAMILIES for n in NOVELTIES)
        out["checks"]["pc_exact_replay_all_novelties"] = all(
            liveness["PC-EXACT-REPLAY"][f][str(n)]["rate"] == 1.0
            for f in FAMILIES for n in NOVELTIES)

        # closed-form memory-lattice predictions (non-outcome arithmetic)
        k1, k2 = k_of("F1-RECORDS"), k_of("F2-WIDGETS")
        m0_f1 = (k1 - 1) / k1
        m0_f2 = (k2 - 1) / k2
        pred = {}
        for arm in ARMS:
            pred[arm] = {}
            for family in FAMILIES:
                k = k_of(family)
                m0 = (k - 1) / k
                rates = {}
                for nov in NOVELTIES:
                    if not chain_requires_binding(nov):
                        rates[str(nov)] = 1.0
                    elif arm in ("T-AMORTIZED-DISCOVERY", "PC-EXACT-REPLAY",
                                 "B-MEMORY-WINDOW-2", "B-MEMORY-RECEIPT",
                                 "B-RETRIEVAL-MEMORYFUL"):
                        rates[str(nov)] = 1.0
                    elif arm == "B-MEMORY-WINDOW-1":
                        rates[str(nov)] = 1.0 if nov == 0.5 else m0
                    else:
                        rates[str(nov)] = m0
                pred[arm][family] = rates
        out["closed_form_predictions"] = pred
        out["checks"]["closed_form_matches_probe"] = all(
            pred[a][f][str(n)] == liveness[a][f][str(n)]["rate"]
            for a in ARMS for f in FAMILIES for n in NOVELTIES)
        out["checks"]["primary_collapses"] = (
            liveness[PRIMARY_COMPARATOR]["F1-RECORDS"]["0.5"]["rate"] == 1.0
            and liveness[PRIMARY_COMPARATOR]["F2-WIDGETS"]["0.5"]["rate"] == 1.0)
        out["checks"]["weak_comparator_in_band"] = all(
            CORRECTNESS_FLOOR <= liveness[c][f][str(n)]["rate"] < COMPARATOR_MAX
            for c in ("B-MEMORY-STATE", "B-COLD-RE-DERIVE")
            for f in FAMILIES for n in (0.5, 0.75))

        # mechanism-off: exposing the binding makes the cold comparator recover
        httpd_m, state_m, base_m = start_server(expose_binding=True)
        try:
            succ, _ = run_arm(base_m, state_m, "B-COLD-RE-DERIVE", "F1-RECORDS", 0.5)
        finally:
            httpd_m.shutdown()
        out["mechanism_off"] = {"cold_f1_rate": succ / k1, "successes": succ, "k": k1}
        out["checks"]["mechanism_off_destroys_certificate"] = (succ / k1) >= COMPARATOR_MAX

        # NC-NO-DISCOVERY-DIRECT
        ndd = {}
        for nov in (0.0, 0.5):
            httpd_c, state_c, base_c = start_server(expose_binding=False)
            try:
                succ, kk, _ = run_no_discovery_direct(base_c, "F1-RECORDS", nov)
            finally:
                httpd_c.shutdown()
            ndd[str(nov)] = succ / kk
        out["no_discovery_direct"] = ndd
        out["checks"]["no_discovery_direct_expected"] = (
            ndd["0.0"] == 1.0 and ndd["0.5"] == 0.0)

        # NC-MEMORY-OFF: M3 with per-task log reset must equal M0
        mo = {}
        for nov in (0.5, 0.75):
            httpd_c, state_c, base_c = start_server(expose_binding=False)
            try:
                succ, kk, _ = run_memory_off(base_c, "F1-RECORDS", nov)
            finally:
                httpd_c.shutdown()
            mo[str(nov)] = succ / kk
        out["memory_off"] = mo
        out["checks"]["memory_off_matches_m0"] = all(
            mo[str(n)] == m0_f1 for n in (0.5, 0.75))

        # NC-RETRIEVAL-REDUNDANT: adding stale retrieval to M3 leaves rate at 1.0
        rr = {}
        for nov in (0.5, 0.75):
            httpd_c, state_c, base_c = start_server(expose_binding=False)
            try:
                succ, kk, _ = run_retrieval_redundant(base_c, "F1-RECORDS", nov)
            finally:
                httpd_c.shutdown()
            rr[str(nov)] = succ / kk
        out["retrieval_redundant"] = rr
        out["checks"]["retrieval_redundant_no_gain"] = all(v == 1.0 for v in rr.values())

        # NC-REVEAL-ORDER-FLIPPED: chain-before-precursor must fail the chain
        rof = {}
        for nov in (0.5, 0.75):
            httpd_c, state_c, base_c = start_server(expose_binding=False)
            try:
                succ, kk, _ = run_reveal_order_flipped(base_c, "F1-RECORDS", nov)
            finally:
                httpd_c.shutdown()
            rof[str(nov)] = succ / kk
        out["reveal_order_flipped"] = rof
        out["checks"]["reveal_order_flipped_fails_chain"] = all(
            rof[str(n)] == m0_f1 for n in (0.5, 0.75))

        # capacity threshold: minimal retained-receipt capacity closing the range
        ct = {}
        for family in FAMILIES:
            ct[family] = {str(n): capacity_threshold(liveness, family, n)
                          for n in (0.5, 0.75)}
        out["capacity_threshold"] = ct
        out["checks"]["capacity_threshold_expected"] = all(
            ct[f]["0.5"] == 1 and ct[f]["0.75"] == 2 for f in FAMILIES)

        # NC-CEILING-BAND: all arms reach 1.0 at novelty 0.0
        out["checks"]["ceiling_band_all_arms_one"] = all(
            liveness[a][f]["0.0"]["rate"] == 1.0 for f in FAMILIES for a in ARMS)

        # NC-WINDOW-MONOTONIC: window1 <= window2 <= full per (family, band)
        out["checks"]["window_monotonic"] = all(
            liveness["B-MEMORY-WINDOW-1"][f][str(n)]["rate"]
            <= liveness["B-MEMORY-WINDOW-2"][f][str(n)]["rate"]
            <= liveness["B-MEMORY-RECEIPT"][f][str(n)]["rate"]
            for f in FAMILIES for n in (0.5, 0.75))

        # NC-BINDING-UNIQUENESS
        out["binding_uniqueness"] = binding_uniqueness_check()
        out["checks"]["binding_uniqueness_ok"] = out["binding_uniqueness"]["collisions"] == 0

        # closed-form (K-1)/K band sweep
        cf = {}
        for k in range(6, 13):
            rate = (k - 1) / k
            cf[str(k)] = {"comparator_rate": rate,
                          "in_band": CORRECTNESS_FLOOR <= rate < COMPARATOR_MAX,
                          "collides_095": rate == COMPARATOR_MAX,
                          "collides_floor": rate == CORRECTNESS_FLOOR}
        out["closed_form"] = cf
        out["checks"]["k_sweep_all_in_band"] = all(v["in_band"] for v in cf.values())
        out["checks"]["no_rate_collides_with_095"] = all(not v["collides_095"] for v in cf.values())
        out["checks"]["no_rate_collides_with_floor"] = all(not v["collides_floor"] for v in cf.values())

        # behavioural diagnostics at scored band
        ident = {}
        for family in FAMILIES:
            t = liveness["T-AMORTIZED-DISCOVERY"][family]["0.5"]
            m3 = liveness[PRIMARY_COMPARATOR][family]["0.5"]
            m0 = liveness["B-COLD-RE-DERIVE"][family]["0.5"]
            ident[family] = {
                "T_vs_M0_distinct_dimensions": counter_distinctness(t["counters"], m0["counters"]),
                "T_vs_M3_distinct_dimensions": counter_distinctness(t["counters"], m3["counters"]),
                "margin_M0": round(t["rate"] - m0["rate"], 6),
                "margin_M3": round(t["rate"] - m3["rate"], 6),
            }
        out["counter_identification"] = ident
        out["checks"]["counter_identification_diagnostic"] = ident

        # memory-lattice assessment
        out["memory_lattice"] = assess_memory_lattice(liveness)
        out["predicted_decision"] = out["memory_lattice"]["decision"]
        out["checks"]["predicted_decision"] = out["predicted_decision"]

        # branch reachability: all four labels constructible
        out["branch_reachability"] = branch_reachability_mem()
        out["checks"]["all_branches_inhabited"] = (
            len(set(out["branch_reachability"].values())) == 4)
    finally:
        httpd.shutdown()
    return out


# --------------------------------------------------------------------------
# scored matrix + gate evaluation (EXECUTE; NOT run during DESIGN)
# --------------------------------------------------------------------------
SCORED_SESSIONS_PER_CELL = 20
LEAK_KEYS = ("session_never_reveals_binding", "no_binding_in_session_body",
             "no_binding_in_task_bodies", "no_binding_in_error_body",
             "wrong_binding_400_no_leak", "precursor_recommit_409_no_reveal")


def run_scored_matrix(n_sessions=SCORED_SESSIONS_PER_CELL):
    """Run the frozen scored matrix.  Outcome-bearing; EXECUTE only."""
    cells = {}
    for family in FAMILIES:
        k = k_of(family)
        for nov in NOVELTIES:
            for arm in ARMS:
                succ_total = 0
                total = 0
                counters = {d: 0 for d in COUNTER_DIMS}
                for _ in range(n_sessions):
                    httpd, state, base = start_server(expose_binding=False)
                    try:
                        succ, c = run_arm(base, state, arm, family, nov)
                    finally:
                        httpd.shutdown()
                    succ_total += succ
                    total += k
                    for d in counters:
                        counters[d] += c[d]
                cells[f"{family}|{nov}|{arm}"] = {
                    "family": family, "novelty": nov, "arm": arm,
                    "successes": succ_total, "tasks": total,
                    "success_rate": succ_total / total,
                    "matched_correctness": succ_total / total,
                    "counters": counters,
                }
    return cells


def synthetic_cells_from_probe(probe, n_sessions=SCORED_SESSIONS_PER_CELL):
    """Build predicted scored cells from probe-measured per-cell results."""
    cells = {}
    for f in FAMILIES:
        for nov in NOVELTIES:
            for arm in ARMS:
                lv = probe["arm_liveness"][arm][f][str(nov)]
                cells[f"{f}|{nov}|{arm}"] = {
                    "family": f, "novelty": nov, "arm": arm,
                    "successes": round(lv["rate"] * n_sessions * k_of(f)),
                    "tasks": n_sessions * k_of(f),
                    "success_rate": lv["rate"],
                    "matched_correctness": lv["rate"],
                    "counters": {d: lv["counters"][d] * n_sessions for d in COUNTER_DIMS},
                }
    return cells


def evaluate_scored(cells, extra_gates=None):
    """Evaluate the V1-V8 gates and the memory-lattice certificate."""
    gates = {}
    gates["V5_arm_liveness"] = all(
        cells[f"{f}|{n}|{a}"]["success_rate"] == 1.0
        for f in FAMILIES for n in NOVELTIES
        for a in ("T-AMORTIZED-DISCOVERY", "PC-EXACT-REPLAY"))
    gates["V8_ceiling_band"] = all(
        cells[f"{f}|0.0|{a}"]["success_rate"] == 1.0
        for f in FAMILIES for a in ARMS)
    if extra_gates:
        gates.update(extra_gates)
    ident = {}
    for f in FAMILIES:
        t = cells[f"{f}|0.5|T-AMORTIZED-DISCOVERY"]
        m0 = cells[f"{f}|0.5|B-COLD-RE-DERIVE"]
        m3 = cells[f"{f}|0.5|{PRIMARY_COMPARATOR}"]
        ident[f] = {
            "T_vs_M0_distinct_dimensions": counter_distinctness(t["counters"], m0["counters"]),
            "T_vs_M3_distinct_dimensions": counter_distinctness(t["counters"], m3["counters"]),
            "margin_M0": t["success_rate"] - m0["success_rate"],
            "margin_M3": t["success_rate"] - m3["success_rate"],
        }
    return gates, ident


def assess_memory_lattice_cells(cells):
    """EXECUTE: evaluate mem_certifies() over the scored cells."""
    detail = {}
    robust = False
    partial = False
    for comp in [c for cls in COMPARATOR_CLASSES.values() for c in cls]:
        detail[comp] = {}
        for family in FAMILIES:
            for nov in [n for n in NOVELTIES if n >= SCORED_BAND]:
                t_rate = cells[f"{family}|{nov}|T-AMORTIZED-DISCOVERY"]["success_rate"]
                comp_rate = cells[f"{family}|{nov}|{comp}"]["success_rate"]
                all_rates = [cells[f"{family}|{nov}|{a}"]["success_rate"] for a in ARMS]
                matched = cells[f"{family}|{nov}|T-AMORTIZED-DISCOVERY"]["matched_correctness"]
                ok = mem_certifies(comp_rate, t_rate, all_rates, matched)
                detail[comp][f"{family}|{nov}"] = {
                    "comparator_rate": comp_rate, "t_rate": t_rate,
                    "margin": t_rate - comp_rate,
                    "min_arm_rate": min(all_rates), "certifies": ok}
                if comp == PRIMARY_COMPARATOR and ok:
                    robust = True
                if comp in WEAKER_COMPARATORS and ok:
                    partial = True
    return {"detail": detail, "robust_certified": robust, "partial_certified": partial}


def run_execute_controls(n_sessions=SCORED_SESSIONS_PER_CELL):
    """EXECUTE-only control measurements on the scored schedule."""
    rates = {}
    for family in FAMILIES:
        succ_total = 0
        total = 0
        for _ in range(n_sessions):
            httpd, state, base = start_server(expose_binding=True)
            try:
                succ, _ = run_arm(base, state, "B-COLD-RE-DERIVE", family, 0.5)
            finally:
                httpd.shutdown()
            succ_total += succ
            total += k_of(family)
        rates[family] = succ_total / total
    mem_off = {}
    for family in FAMILIES:
        succ_total = 0
        total = 0
        for _ in range(n_sessions):
            httpd, state, base = start_server(expose_binding=False)
            try:
                succ, kk, _ = run_memory_off(base, family, 0.5)
            finally:
                httpd.shutdown()
            succ_total += succ
            total += kk
        mem_off[family] = succ_total / total
    rof = {}
    for family in FAMILIES:
        succ_total = 0
        total = 0
        for _ in range(n_sessions):
            httpd, state, base = start_server(expose_binding=False)
            try:
                succ, kk, _ = run_reveal_order_flipped(base, family, 0.5)
            finally:
                httpd.shutdown()
            succ_total += succ
            total += kk
        rof[family] = succ_total / total
    return {"mechanism_off_cold_rate": rates,
            "mechanism_off_destroys_certificate":
                all(r >= COMPARATOR_MAX for r in rates.values()),
            "memory_off_rate": mem_off,
            "memory_off_matches_m0":
                all(abs(mem_off[f] - (k_of(f) - 1) / k_of(f)) < 1e-9 for f in FAMILIES),
            "reveal_order_flipped_rate": rof,
            "reveal_order_flipped_fails_chain":
                all(abs(rof[f] - (k_of(f) - 1) / k_of(f)) < 1e-9 for f in FAMILIES)}


def code_fidelity_manifest():
    import sys
    import pathlib
    src_sha = None
    try:
        if "__file__" in globals() and __file__:
            src_sha = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    except OSError:
        src_sha = None
    return {"python": sys.version.split()[0], "harness_sha256": src_sha}


def assemble_decision(cells, controls, protocol, v1, determinism_ok):
    """EXECUTE: full gate world + memory-lattice decision."""
    gates, ident = evaluate_scored(
        cells,
        extra_gates={
            "V8_mechanism_off": controls["mechanism_off_destroys_certificate"],
            "V8_memory_off_attribution": controls["memory_off_matches_m0"],
            "V8_reveal_order_attribution": controls["reveal_order_flipped_fails_chain"],
        })
    gates["V8_m0_counter_distinctness"] = all(
        ident[f]["T_vs_M0_distinct_dimensions"] >= MIN_DISTINCT_DIMS for f in FAMILIES)
    gates["V1_code_fidelity_manifest"] = bool(v1.get("harness_sha256"))
    gates["V2_transport_conformance"] = all(protocol.values())
    gates["V3_no_leak"] = all(protocol[k] for k in LEAK_KEYS)
    gates["V4_determinism"] = bool(determinism_ok)
    gates["V6_counter_instrumentation"] = all(
        all(d in c["counters"] for d in COUNTER_DIMS) for c in cells.values())
    gates["V7_matched_correctness"] = all(
        c["matched_correctness"] == c["success_rate"] for c in cells.values())
    lattice = assess_memory_lattice_cells(cells)
    world = {"gates_pass": all(gates.values()),
             "robust_certified": lattice["robust_certified"],
             "partial_certified": lattice["partial_certified"]}
    return {"gates": gates, "counter_identification": ident,
            "memory_lattice": lattice, "world": world,
            "decision": classify_mem(world), "v1": v1}


def run_execute():
    """EXECUTE-only: full scoring twice (determinism) + frozen decision rule."""
    cells_a = run_scored_matrix()
    cells_b = run_scored_matrix()
    determinism_ok = json.dumps(cells_a, sort_keys=True) == json.dumps(cells_b, sort_keys=True)
    controls = run_execute_controls()
    httpd, state, base = start_server(expose_binding=False)
    try:
        protocol = protocol_invariants(base)
    finally:
        httpd.shutdown()
    v1 = code_fidelity_manifest()
    result = assemble_decision(cells_a, controls, protocol, v1, determinism_ok)
    result["cells"] = cells_a
    result["controls"] = controls
    result["determinism_ok"] = determinism_ok
    return result


def run_selftest():
    """Exercise the full EXECUTE decision path on probe-derived synthetic cells."""
    probe = run_probe()
    cells = synthetic_cells_from_probe(probe)
    controls = {
        "mechanism_off_destroys_certificate": probe["checks"]["mechanism_off_destroys_certificate"],
        "memory_off_matches_m0": probe["checks"]["memory_off_matches_m0"],
        "reveal_order_flipped_fails_chain": probe["checks"]["reveal_order_flipped_fails_chain"],
    }
    full = assemble_decision(cells, controls, probe["checks"]["protocol_invariants"],
                             {"python": "synthetic", "harness_sha256": "synthetic"}, True)
    return {
        "note": ("non-outcome-bearing: assemble_decision() (all gates + memory-lattice "
                 "decision rule) exercised on probe-derived synthetic cells"),
        "gates": full["gates"],
        "world": full["world"],
        "decision": full["decision"],
        "probe_predicted_decision": probe["predicted_decision"],
        "check_evaluator_matches_probe":
            full["decision"] == probe["predicted_decision"],
        "check_decision_is_partial": full["decision"] == "PARTIAL",
    }


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["probe", "selftest", "scored"], default="probe")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    if args.mode == "probe":
        print(json.dumps(run_probe(), indent=2, sort_keys=True))
        return
    if args.mode == "selftest":
        print(json.dumps(run_selftest(), indent=2, sort_keys=True))
        return
    out = run_execute()
    text = json.dumps(out, indent=2, sort_keys=True)
    if args.out:
        import pathlib
        pathlib.Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
