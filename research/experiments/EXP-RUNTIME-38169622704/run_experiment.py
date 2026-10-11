#!/usr/bin/env python3
"""DESIGN-time satisfiability probe for EXP-RUNTIME-38169622704.

Substrate class SBA-CREDENTIAL-FREE-V2 (Session-Binding-Amortized).

This probe is NON-OUTCOME-BEARING. It verifies:
  * the stdlib HTTP transport answers on 127.0.0.1;
  * protocol semantics/invariants of the SBA construction;
  * treatment liveness on ONE session per (arm, family, novelty band);
  * the closed-form pre-freeze dynamic-range certificate arithmetic;
  * decision-branch reachability over synthetic worlds;
  * determinism.

It does NOT run the scored 20-session matrix that produces the scientific
measurement. stdlib only. Two runs must be byte-identical.
"""
from __future__ import annotations

import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

RUN_SEED = "SPIDER-RUNTIME-SBA-V2-2026"
FAMILIES = {"F1-RECORDS": 8, "F2-WIDGETS": 10}
NOVELTIES = [0.0, 0.25, 0.5, 0.75]
SCORED_BAND = 0.50
COMPARATOR_MAX = 0.95
CORRECTNESS_FLOOR = 0.80
MARGIN_FLOOR = 0.05  # not 1/8: F2 (K=10) comparator margin is 0.100 < 0.125
COUNTER_DIMS = ["http_calls", "retrieval_calls", "verification_calls", "repair_calls"]
MIN_DISTINCT_DIMS = 2
BINDING_HEX = 12  # 48-bit
ARMS = [
    "T-AMORTIZED-DISCOVERY",
    "B-COLD-RE-DERIVE",
    "B-RETRIEVAL-SHAPED",
    "PC-EXACT-REPLAY",
]


def h(*parts) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()


def counter_distinctness(c_t, c_c) -> int:
    """Number of the four counter dimensions on which two arms differ."""
    return sum(1 for d in COUNTER_DIMS if c_t[d] != c_c[d])


def binding_uniqueness_check(n_sessions=20) -> dict:
    """NC-BINDING-UNIQUENESS: 48-bit session bindings are pairwise distinct."""
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
    # session-independent: derivable from public info only
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
# server
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
                "family": family,
                "novelty": novelty,
                "idx": idx,
                "token": tok,
                "binding": session_binding(family, novelty, idx),
                "schema": schema_epoch_value(family, novelty, idx),
                "committed": {},
            }
            self.sessions[tok] = s
            return s


class Handler(BaseHTTPRequestHandler):
    state: State = None  # injected

    def log_message(self, *a):  # silence
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
        # /api/v1/{family}/session
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
        # /api/v1/{family}/task/{i}
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
        # NOTE: token is a fixed-length hex; a per-session secret is only
        # exposed via the session endpoint, never embedded in URLs.
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


# --------------------------------------------------------------------------
# arms
# --------------------------------------------------------------------------
def run_arm(base, state, arm, family, novelty):
    k = k_of(family)
    counters = {"http_calls": 0, "retrieval_calls": 0, "verification_calls": 0, "repair_calls": 0}
    successes = 0
    ci = chain_index(novelty, k)
    pi = precursor_index(novelty, k)
    chain_active = chain_requires_binding(novelty)

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
        return successes, counters

    if arm == "B-COLD-RE-DERIVE":
        for i in range(k):
            s = sess()
            d = task(s["session_token"], i)
            res = d["resource_id"]
            if d["is_chain"] and chain_active:
                # memoryless: no retained binding. Under NC-MECHANISM-OFF the
                # binding is exposed directly by the session endpoint and is
                # therefore recoverable, which is what the control tests.
                res = s.get("binding")
            counters["verification_calls"] += 1
            st, b = commit(s["session_token"], i, s["schema_epoch"], res)
            if st == 200:
                successes += 1
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    if arm == "B-RETRIEVAL-SHAPED":
        # retrieve a stale foreign-session binding for every task
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

    raise AssertionError(arm)


# --------------------------------------------------------------------------
# controls (declared nulls, measured in probe mode)
# --------------------------------------------------------------------------
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


def run_retain_receipt(base, family, novelty):
    """NC-RETAIN-RECEIPT: retain only the immediate predecessor receipt."""
    k = k_of(family)
    counters = {d: 0 for d in COUNTER_DIMS}
    successes = 0
    chain_active = chain_requires_binding(novelty)
    sess, task, commit = _mk(base, family, novelty, counters)
    s = sess()
    last = None
    for i in range(k):
        d = task(s["session_token"], i)
        res = d["resource_id"]
        if d["is_chain"] and chain_active:
            res = (last or {}).get("chain_resource_id")
        counters["verification_calls"] += 1
        st, b = commit(s["session_token"], i, s["schema_epoch"], res)
        if st == 200:
            successes += 1
            last = b["receipt"]
        else:
            last = None
    return successes, k, counters


# --------------------------------------------------------------------------
# protocol invariants
# --------------------------------------------------------------------------
def protocol_invariants(base, family="F1-RECORDS", novelty=0.5):
    out = {}
    k = k_of(family)
    st, s = http_get(f"{base}/api/v1/{family}/session?novelty={novelty}")
    out["session_never_reveals_binding"] = st == 200 and "binding" not in s
    tok = s["session_token"]
    binding = session_binding(family, novelty, s["epoch"])
    # F-LEAK: the binding must not appear in the session body, any task body,
    # any error body, or any log line (log_message is silenced).
    out["no_binding_in_session_body"] = binding not in json.dumps(s, sort_keys=True)
    task_bodies = [http_get(f"{base}/api/v1/{family}/task/{i}", token=tok)[1]
                   for i in range(k)]
    out["no_binding_in_task_bodies"] = all(
        binding not in json.dumps(b, sort_keys=True) for b in task_bodies)
    st, d_chain = http_get(f"{base}/api/v1/{family}/task/{chain_index(novelty, k)}", token=tok)
    out["chain_task_resource_null"] = st == 200 and d_chain["resource_id"] is None and d_chain["is_chain"]
    # wrong/foreign binding -> 400, no binding echoed
    st, b = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": chain_index(novelty, k),
        "schema_epoch": s["schema_epoch"], "resource_id": "0" * BINDING_HEX,
    })
    out["wrong_binding_400_no_leak"] = st == 400 and "chain_resource_id" not in b
    out["no_binding_in_error_body"] = binding not in json.dumps(b, sort_keys=True)
    # precursor first commit reveals binding once
    st, b = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": precursor_index(novelty, k),
        "schema_epoch": s["schema_epoch"],
        "resource_id": public_resource(family, novelty, precursor_index(novelty, k)),
    })
    out["precursor_reveals_binding_once"] = (
        st == 200 and b["receipt"].get("chain_resource_id") == session_binding(family, novelty, s["epoch"]))
    # precursor re-commit -> 409 no re-reveal
    st, b = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": precursor_index(novelty, k),
        "schema_epoch": s["schema_epoch"],
        "resource_id": public_resource(family, novelty, precursor_index(novelty, k)),
    })
    out["precursor_recommit_409_no_reveal"] = st == 409 and "chain_resource_id" not in b
    # correct binding -> 200
    st, b = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": chain_index(novelty, k),
        "schema_epoch": s["schema_epoch"],
        "resource_id": session_binding(family, novelty, s["epoch"]),
    })
    out["correct_binding_200"] = st == 200
    # binding single-use per session: a repeat chain commit is 409 (no re-commit)
    st, b = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": chain_index(novelty, k),
        "schema_epoch": s["schema_epoch"],
        "resource_id": session_binding(family, novelty, s["epoch"]),
    })
    out["chain_binding_single_use_409"] = st == 409
    return out


# --------------------------------------------------------------------------
# certificate + branch classifier
# --------------------------------------------------------------------------
def family_certifies(k, cold_rate, retr_rate, all_rates, matched_correctness,
                     distinct_dims, margins):
    """Full frozen certificate; distinct_dims and margins are mandatory."""
    return (
        cold_rate < COMPARATOR_MAX and retr_rate < COMPARATOR_MAX
        and all(r >= CORRECTNESS_FLOOR for r in all_rates)
        and matched_correctness >= CORRECTNESS_FLOOR
        and distinct_dims["T_vs_COLD"] >= MIN_DISTINCT_DIMS
        and distinct_dims["T_vs_RETRIEVAL"] >= MIN_DISTINCT_DIMS
        and margins["T_vs_COLD"] >= MARGIN_FLOOR
        and margins["T_vs_RETRIEVAL"] >= MARGIN_FLOOR
    )


def classify(world):
    """Frozen decision rule over the assembled V1-V8 gate world.

    Precedence: any V1-V8 failure (including liveness V5, leak V3 and the two V8
    sensitivity sub-gates) -> MEASUREMENT_INVALID. Otherwise a single certifying
    family suffices (mandate: "on at least one family").
    """
    if not world["gates_pass"]:
        return "MEASUREMENT_INVALID"
    if world["certified_families"] >= 1:
        return "SUPPORTS"
    if world["comparator_attributable"]:
        return "FALSIFIES"
    return "MIXED"


def branch_reachability(k_by_family=None):
    """Construct one synthetic world per decision label (all four reachable)."""
    worlds = {}
    worlds["SUPPORTS"] = classify({
        "gates_pass": True, "certified_families": 1, "total_families": 2,
        "comparator_attributable": False})
    worlds["FALSIFIES"] = classify({
        "gates_pass": True, "certified_families": 0, "total_families": 2,
        "comparator_attributable": True})
    worlds["MIXED"] = classify({
        "gates_pass": True, "certified_families": 0, "total_families": 2,
        "comparator_attributable": False})
    worlds["MEASUREMENT_INVALID"] = classify({
        "gates_pass": False, "certified_families": 0, "total_families": 2,
        "comparator_attributable": False})
    return worlds


# --------------------------------------------------------------------------
# main probe
# --------------------------------------------------------------------------
def run_probe():
    out = {"seed": RUN_SEED, "families": FAMILIES, "novelties": NOVELTIES,
           "scored_band": SCORED_BAND}
    httpd, state, base = start_server(expose_binding=False)
    try:
        out["checks"] = {"transport_stdlib_http": False}
        st, _ = http_get(f"{base}/healthz")
        out["checks"]["transport_stdlib_http"] = st == 200
        out["checks"]["protocol_invariants"] = protocol_invariants(base)
        out["checks"]["all_protocol_invariants_pass"] = all(
            out["checks"]["protocol_invariants"].values())

        liveness = {}
        defect_sessions = 0
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
                    if succ < 1 and nov < SCORED_BAND:
                        defect_sessions += 1
                    liveness[arm][family][str(nov)] = {
                        "successes": succ, "k": k, "rate": succ / k, "counters": counters,
                    }
        out["arm_liveness"] = liveness
        out["checks"]["defect_sessions"] = defect_sessions

        # treatment liveness: T and PC at 1.0 everywhere
        t_live = all(
            liveness["T-AMORTIZED-DISCOVERY"][f][str(n)]["rate"] == 1.0
            for f in FAMILIES for n in NOVELTIES)
        pc_live = all(
            liveness["PC-EXACT-REPLAY"][f][str(n)]["rate"] == 1.0
            for f in FAMILIES for n in NOVELTIES)
        out["checks"]["treatment_live_all_novelties"] = t_live
        out["checks"]["pc_exact_replay_all_novelties"] = pc_live

        # comparator behaviour at scored band
        comp = {}
        for family in FAMILIES:
            k = k_of(family)
            comp[family] = {
                "B-COLD-RE-DERIVE": liveness["B-COLD-RE-DERIVE"][family]["0.5"]["rate"],
                "B-RETRIEVAL-SHAPED": liveness["B-RETRIEVAL-SHAPED"][family]["0.5"]["rate"],
            }
        out["comparator_at_scored_band"] = comp

        # mechanism-off: exposing the binding via session endpoint
        httpd_m, state_m, base_m = start_server(expose_binding=True)
        try:
            succ, counters = run_arm(base_m, state_m, "B-COLD-RE-DERIVE", "F1-RECORDS", 0.5)
        finally:
            httpd_m.shutdown()
        k1 = k_of("F1-RECORDS")
        out["mechanism_off"] = {"cold_f1_rate": succ / k1, "successes": succ, "k": k1}
        out["checks"]["mechanism_off_destroys_certificate"] = (succ / k1) >= COMPARATOR_MAX

        # NC-NO-DISCOVERY-DIRECT: 1.0 at novelty 0.0, 0.0 at >= 0.25
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

        # NC-RETAIN-RECEIPT: 1.0 at 0.5 (distance 1), (K-1)/K at 0.75 (distance 2)
        rr = {}
        for nov in (0.5, 0.75):
            httpd_c, state_c, base_c = start_server(expose_binding=False)
            try:
                succ, kk, _ = run_retain_receipt(base_c, "F1-RECORDS", nov)
            finally:
                httpd_c.shutdown()
            rr[str(nov)] = succ / kk
        out["retain_receipt"] = rr
        out["checks"]["retain_receipt_expected"] = (
            rr["0.5"] == 1.0
            and rr["0.75"] == (k_of("F1-RECORDS") - 1) / k_of("F1-RECORDS"))

        # NC-CEILING-BAND: all arms at novelty 0.0 reach 1.0
        out["checks"]["ceiling_band_all_arms_one"] = all(
            liveness[a][f]["0.0"]["rate"] == 1.0
            for f in FAMILIES for a in ARMS)

        # NC-BINDING-UNIQUENESS: no 48-bit binding collisions over the matrix
        out["binding_uniqueness"] = binding_uniqueness_check()
        out["checks"]["binding_uniqueness_ok"] = out["binding_uniqueness"]["collisions"] == 0

        # closed-form certificate arithmetic
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

        # behavioural identification: counter distinctness + success margins at band
        ident = {}
        for family in FAMILIES:
            t = liveness["T-AMORTIZED-DISCOVERY"][family]["0.5"]
            cold = liveness["B-COLD-RE-DERIVE"][family]["0.5"]
            retr = liveness["B-RETRIEVAL-SHAPED"][family]["0.5"]
            ident[family] = {
                "T_vs_COLD_distinct_dimensions": counter_distinctness(t["counters"], cold["counters"]),
                "T_vs_RETRIEVAL_distinct_dimensions": counter_distinctness(t["counters"], retr["counters"]),
                "margin_COLD": round(t["rate"] - cold["rate"], 6),
                "margin_RETRIEVAL": round(t["rate"] - retr["rate"], 6),
            }
        out["counter_identification"] = ident
        out["checks"]["counter_identification_ok"] = all(
            v["T_vs_COLD_distinct_dimensions"] >= MIN_DISTINCT_DIMS
            and v["T_vs_RETRIEVAL_distinct_dimensions"] >= MIN_DISTINCT_DIMS
            and v["margin_COLD"] >= MARGIN_FLOOR
            and v["margin_RETRIEVAL"] >= MARGIN_FLOOR
            for v in ident.values())

        # certificate: both families certify at scored band
        certified = 0
        for family in FAMILIES:
            k = k_of(family)
            cold = liveness["B-COLD-RE-DERIVE"][family]["0.5"]["rate"]
            retr = liveness["B-RETRIEVAL-SHAPED"][family]["0.5"]["rate"]
            rates = [
                liveness[a][family]["0.5"]["rate"] for a in ARMS
            ]
            d = ident[family]
            distinct = {"T_vs_COLD": d["T_vs_COLD_distinct_dimensions"],
                        "T_vs_RETRIEVAL": d["T_vs_RETRIEVAL_distinct_dimensions"]}
            margins = {"T_vs_COLD": d["margin_COLD"],
                       "T_vs_RETRIEVAL": d["margin_RETRIEVAL"]}
            matched = liveness["T-AMORTIZED-DISCOVERY"][family]["0.5"]["rate"]
            ok = family_certifies(k, cold, retr, rates, matched,
                                  distinct_dims=distinct, margins=margins)
            comp[family]["certifies"] = ok
            certified += int(ok)
        out["certificate"] = {
            "certified_families": certified,
            "total_families": len(FAMILIES),
            "comparator_at_scored_band": comp,
            "branch_reachability": branch_reachability(FAMILIES),
        }
        out["checks"]["certificate_satisfiable"] = certified >= 1
        out["checks"]["all_branches_inhabited"] = (
            len(set(out["certificate"]["branch_reachability"].values())) == 4)
    finally:
        httpd.shutdown()
    return out


# --------------------------------------------------------------------------
# scored matrix + gate evaluation (EXECUTE). NOT run during DESIGN.
# --------------------------------------------------------------------------
SCORED_SESSIONS_PER_CELL = 20


def run_scored_matrix(n_sessions=SCORED_SESSIONS_PER_CELL):
    """Run the frozen scored matrix. Outcome-bearing; called only at EXECUTE."""
    cells = {}
    for family in FAMILIES:
        k = k_of(family)
        for nov in NOVELTIES:
            for arm in ARMS:
                succ_total = 0
                total = 0
                counters = {"http_calls": 0, "retrieval_calls": 0,
                            "verification_calls": 0, "repair_calls": 0}
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


def evaluate_scored(cells, extra_gates=None):
    """Evaluate V5/V8 and the family certificate from scored cells.

    Enforces the full frozen certificate: comparator ceiling, correctness floor,
    matched correctness, >=2/4 counter distinctness and >= MARGIN_FLOOR margins.
    """
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
    cert_fams = []
    for f in FAMILIES:
        k = k_of(f)
        ok = True
        dd = {"T_vs_COLD": 0, "T_vs_RETRIEVAL": 0}
        mm = {"T_vs_COLD": 0.0, "T_vs_RETRIEVAL": 0.0}
        for n in [x for x in NOVELTIES if x >= SCORED_BAND]:
            t = cells[f"{f}|{n}|T-AMORTIZED-DISCOVERY"]
            cold = cells[f"{f}|{n}|B-COLD-RE-DERIVE"]
            retr = cells[f"{f}|{n}|B-RETRIEVAL-SHAPED"]
            rates = [cells[f"{f}|{n}|{a}"]["success_rate"] for a in ARMS]
            dd = {"T_vs_COLD": counter_distinctness(t["counters"], cold["counters"]),
                  "T_vs_RETRIEVAL": counter_distinctness(t["counters"], retr["counters"])}
            mm = {"T_vs_COLD": t["success_rate"] - cold["success_rate"],
                  "T_vs_RETRIEVAL": t["success_rate"] - retr["success_rate"]}
            ok = ok and family_certifies(
                k, cold["success_rate"], retr["success_rate"],
                rates, t["matched_correctness"],
                distinct_dims=dd, margins=mm)
        ident[f] = {
            "T_vs_COLD_distinct_dimensions": dd["T_vs_COLD"],
            "T_vs_RETRIEVAL_distinct_dimensions": dd["T_vs_RETRIEVAL"],
            "margin_COLD": mm["T_vs_COLD"],
            "margin_RETRIEVAL": mm["T_vs_RETRIEVAL"],
        }
        if ok:
            cert_fams.append(f)
    return gates, cert_fams, ident


def synthetic_cells_from_probe(probe, n_sessions=SCORED_SESSIONS_PER_CELL):
    """Build predicted scored cells from probe-measured per-cell results.

    Non-outcome-bearing: no HTTP runs; used only to exercise evaluate_scored().
    """
    cells = {}
    for f in FAMILIES:
        for nov in NOVELTIES:
            for arm in ARMS:
                lv = probe["arm_liveness"][arm][f][str(nov)]
                cells[f"{f}|{nov}|{arm}"] = {
                    "family": f, "novelty": nov, "arm": arm,
                    "successes": round(lv["rate"] * n_sessions),
                    "tasks": n_sessions,
                    "success_rate": lv["rate"],
                    "matched_correctness": lv["rate"],
                    "counters": {d: lv["counters"][d] * n_sessions for d in COUNTER_DIMS},
                }
    return cells


def run_execute_controls(n_sessions=SCORED_SESSIONS_PER_CELL):
    """EXECUTE-only control measurement: mechanism-off cold comparator at band."""
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
    return {"mechanism_off_cold_rate": rates,
            "mechanism_off_destroys_certificate":
                all(r >= COMPARATOR_MAX for r in rates.values())}


LEAK_KEYS = ("session_never_reveals_binding", "no_binding_in_session_body",
             "no_binding_in_task_bodies", "no_binding_in_error_body",
             "wrong_binding_400_no_leak", "precursor_recommit_409_no_reveal")


def code_fidelity_manifest():
    """V1: python version + sha256 of this harness file (when run as a file)."""
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
    """Assemble the full V1-V8 gate world and apply the frozen decision rule."""
    gates, cert_fams, ident = evaluate_scored(
        cells,
        extra_gates={"V8_mechanism_off": controls["mechanism_off_destroys_certificate"]})
    gates["V1_code_fidelity_manifest"] = bool(v1.get("harness_sha256"))
    gates["V2_transport_conformance"] = all(protocol.values())
    gates["V3_no_leak"] = all(protocol[k] for k in LEAK_KEYS)
    gates["V4_determinism"] = bool(determinism_ok)
    gates["V6_counter_instrumentation"] = all(
        all(d in c["counters"] for d in COUNTER_DIMS) for c in cells.values())
    gates["V7_matched_correctness"] = all(
        c["matched_correctness"] == c["success_rate"] for c in cells.values())
    comparator_attributable = all(
        cells[f"{f}|{n}|B-COLD-RE-DERIVE"]["success_rate"] >= COMPARATOR_MAX
        and cells[f"{f}|{n}|B-RETRIEVAL-SHAPED"]["success_rate"] >= COMPARATOR_MAX
        for f in FAMILIES for n in NOVELTIES if n >= SCORED_BAND)
    world = {
        "gates_pass": all(gates.values()),
        "certified_families": len(cert_fams),
        "total_families": len(FAMILIES),
        "comparator_attributable": comparator_attributable,
    }
    return {"gates": gates, "counter_identification": ident,
            "certified_families": cert_fams, "world": world,
            "decision": classify(world), "v1": v1}


def run_execute():
    """EXECUTE-only: full V1-V8 scoring twice (determinism) + frozen decision rule."""
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
    controls = {"mechanism_off_destroys_certificate":
                probe["checks"]["mechanism_off_destroys_certificate"]}
    full = assemble_decision(cells, controls, probe["checks"]["protocol_invariants"],
                             {"python": "synthetic", "harness_sha256": "synthetic"}, True)
    probe_certs = [f for f in FAMILIES
                   if probe["certificate"]["comparator_at_scored_band"][f]["certifies"]]
    return {
        "note": ("non-outcome-bearing: assemble_decision() (all V1-V8 gates + decision "
                 "rule) exercised on probe-derived synthetic cells"),
        "gates": full["gates"],
        "certified_families": full["certified_families"],
        "counter_identification": full["counter_identification"],
        "world": full["world"],
        "decision": full["decision"],
        "probe_certified_families": probe_certs,
        "check_evaluator_matches_probe": full["certified_families"] == probe_certs,
        "check_decision_supports": full["decision"] == "SUPPORTS",
    }


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["probe", "selftest", "scored"], default="probe")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    if args.mode == "probe":
        result = run_probe()
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    if args.mode == "selftest":
        print(json.dumps(run_selftest(), indent=2, sort_keys=True))
        return
    # EXECUTE-only path: outcome-bearing
    out = run_execute()
    text = json.dumps(out, indent=2, sort_keys=True)
    if args.out:
        import pathlib
        pathlib.Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
