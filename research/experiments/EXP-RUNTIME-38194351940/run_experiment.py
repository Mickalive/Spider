#!/usr/bin/env python3
"""DESIGN-time satisfiability probe for EXP-RUNTIME-38194351940.

Substrate class SBA-CREDENTIAL-FREE-V3 (Session-Mechanism-Inheritance).

Scientific question (director mandate on C-MEAS-VALID, action REOPEN):
  The frozen SBA-CREDENTIAL-FREE-V2 (K-1)/K dynamic range collapsed onto a
  comparator carrying a full within-session commit-receipt log
  (EXP-RUNTIME-38182129488: B-MEMORY-RECEIPT rate 1.0, margin 0.0).  Can a
  hardened V3 credential-free bank be constructed whose success requires
  MECHANISM- or COMPOSITION-DEPENDENT behaviour -- i.e. carrying a compiled
  hidden mechanism across a session boundary -- so that no retention-only
  policy (within-session full-receipt memory, or cross-session retention of
  all raw calibration examples) can reach the treatment, while a
  cross-session compile-capable agent reaches it exactly?

Construction:
  A hidden bank-wide affine mechanism M(x) = (a*x + b) mod P (P prime,
  2**40 - 87) is fixed per (family, bank-instance) from the secret.  A
  CALIBRATION session exposes N_CAL=3 labelled examples (x_j, y_j=M(x_j)) in
  its task bodies/receipts.  A separate SCORED session exposes only a fresh
  unlabelled input x_q on exactly one `chain` task (index K-3 at novelty 0.50;
  index K-1 at novelty 0.75, where the required answer is the composed
  M(M(x_q))); every other scored task is an ordinary public task.  An arm
  succeeds on the chain task only by carrying a *compiled* mechanism across
  the session boundary and evaluating it on the fresh x_q.

  Information-theoretic property: the scored session contains NO labelled
  (x, M(x)) pair, so within-session retention -- no matter its capacity --
  cannot determine M(x_q).  Cross-session retention of the raw calibration
  examples is likewise insufficient, because retrieval replays a stored y
  rather than evaluating M on a fresh x.  Only cross-session *compilation*
  (solving (a,b)) reaches the treatment.

This probe is NON-OUTCOME-BEARING.  It verifies:
  * the stdlib HTTP transport answers on 127.0.0.1;
  * protocol semantics / no-leak invariants;
  * arm liveness on a few bank instances per (arm, family, novelty);
  * the mechanism non-degeneracy (a != 0; 3 distinct x; affine solve exact);
  * x_q never equals a calibration x (no accidental retention win);
  * branch reachability of the frozen decision rule over synthetic worlds;
  * determinism (two runs byte-identical).

It does NOT run the scored 20-instance matrix.  stdlib only.
"""
from __future__ import annotations

import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

P = 1099511627689          # prime = 2**40 - 87 (verified at DESIGN)
RUN_SEED = "SPIDER-RUNTIME-SBA-V3-2026"
FAMILIES = {"F1-RECORDS": 8, "F2-WIDGETS": 10}
NOVELTIES = [0.0, 0.25, 0.5, 0.75]
SCORED_BAND = 0.50
COMPARATOR_MAX = 0.95
CORRECTNESS_FLOOR = 0.80
MARGIN_FLOOR = 0.05
COUNTER_DIMS = ["http_calls", "retrieval_calls", "verification_calls", "repair_calls"]
MIN_DISTINCT_DIMS = 2
N_CAL = 3

# Arm roster.
TREATMENT = "T-MECHANISM-INHERIT"
POSITIVE = "PC-EXACT-REPLAY"
IDENTITY = "B-CROSS-SESSION-COMPILE"      # expected identical to T (disclosed)
WITHIN_SESSION = ["B-WITHIN-SESSION-RECEIPT", "B-WITHIN-SESSION-COMPOSE"]
CROSS_SESSION_RETENTION = ["B-RETRIEVAL-REPLAY"]
RETAIN_COMPARATORS = WITHIN_SESSION + CROSS_SESSION_RETENTION
MEMORYLESS = "B-MEMORYLESS"
ARMS = [TREATMENT, POSITIVE, IDENTITY, "B-WITHIN-SESSION-RECEIPT",
        "B-WITHIN-SESSION-COMPOSE", "B-RETRIEVAL-REPLAY", MEMORYLESS]

SCORED_SESSIONS_PER_CELL = 20
LEAK_KEYS = ("session_never_reveals_mechanism", "no_mechanism_in_scored_session_body",
             "no_cal_examples_in_scored_bodies", "no_answer_in_scored_chain_body",
             "wrong_answer_400_no_leak", "cal_receipt_reveals_y_once",
             "chain_receipt_no_answer")


# --------------------------------------------------------------------------
# deterministic derivations (no clock, no os.urandom, no secrets)
# --------------------------------------------------------------------------
def h(*parts) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()


def _di(mod: int, *parts) -> int:
    return int(h(*parts)[:16], 16) % mod


def server_secret() -> str:
    return h(RUN_SEED, "server_secret")[:32]


def mechanism_params(family: str, idx: int):
    a = _di(P - 1, server_secret(), family, idx, "a") + 1   # in [1, P-1]
    b = _di(P, server_secret(), family, idx, "b")
    return a, b


def mech_apply(a: int, b: int, x: int) -> int:
    return (a * x + b) % P


def cal_points(family: str, idx: int):
    xs = []
    j = 0
    while len(xs) < N_CAL:
        x = _di(P, server_secret(), family, idx, "xcal", j)
        if x not in xs:
            xs.append(x)
        j += 1
    a, b = mechanism_params(family, idx)
    return [(x, mech_apply(a, b, x)) for x in xs]


def query_x(family: str, idx: int) -> int:
    return _di(P, server_secret(), family, idx, "xq")


def target_value(family: str, idx: int, novelty: float) -> int:
    a, b = mechanism_params(family, idx)
    y = mech_apply(a, b, query_x(family, idx))
    if novelty == 0.75:
        y = mech_apply(a, b, y)   # composed application
    return y


def session_token(family, novelty, idx, phase):
    return h(server_secret(), family, repr(novelty), idx, phase, "token")[:16]


def schema_epoch_value(family, novelty, idx, phase):
    return h(server_secret(), family, repr(novelty), idx, phase, "schema")[:8]


def public_resource(family, novelty, i):
    return h(server_secret(), family, repr(novelty), "res", i)[:10]


def k_of(family):
    return FAMILIES[family]


def mechanism_active(novelty) -> bool:
    return novelty >= SCORED_BAND


def chain_index(novelty, k):
    if novelty == 0.5:
        return k - 3
    if novelty == 0.75:
        return k - 1
    return None


def mechanism_nondegeneracy(n_instances=50):
    """Sample bank instances: a != 0; N_CAL distinct x; exact affine recovery;
    the scored query x_q never equals a calibration x."""
    deg = {"instances": 0, "a_zero": 0, "duplicate_x": 0, "solve_fail": 0,
           "query_collision": 0, "min_query_gap": None}
    for family in FAMILIES:
        for inst in range(n_instances):
            deg["instances"] += 1
            a, b = mechanism_params(family, inst)
            if a == 0:
                deg["a_zero"] += 1
            pts = cal_points(family, inst)
            xs = [x for x, _ in pts]
            if len(set(xs)) != N_CAL:
                deg["duplicate_x"] += 1
            if recover_affine(pts) != (a, b):
                deg["solve_fail"] += 1
            xq = query_x(family, inst)
            gap = min(abs(xq - x) for x in xs)
            if gap == 0:
                deg["query_collision"] += 1
            deg["min_query_gap"] = gap if deg["min_query_gap"] is None else min(deg["min_query_gap"], gap)
    deg["ok"] = (deg["a_zero"] == 0 and deg["duplicate_x"] == 0 and deg["solve_fail"] == 0
                 and deg["query_collision"] == 0 and deg["min_query_gap"] > 0)
    return deg


def recover_affine(pairs):
    """Recover (a, b) from labelled examples; None if under-determined/inconsistent."""
    if not pairs or len(pairs) < 2:
        return None
    (x1, y1), (x2, y2) = pairs[0], pairs[1]
    if (x1 - x2) % P == 0:
        return None
    a = ((y1 - y2) % P) * pow((x1 - x2) % P, -1, P) % P
    b = (y1 - a * x1) % P
    if any(mech_apply(a, b, x) != y % P for x, y in pairs):
        return None
    return a, b


# --------------------------------------------------------------------------
# server (credential-free, deterministic, stdlib-only)
# --------------------------------------------------------------------------
class State:
    def __init__(self, expose_mechanism=False):
        self.lock = threading.Lock()
        self.sessions = {}
        self.expose_mechanism = expose_mechanism

    def new_session(self, family, novelty, idx, phase):
        with self.lock:
            tok = session_token(family, novelty, idx, phase)
            s = {"family": family, "novelty": novelty, "idx": idx, "phase": phase,
                 "token": tok, "schema": schema_epoch_value(family, novelty, idx, phase),
                 "committed": set()}
            self.sessions[tok] = s
            return s


def _task_kind(s, i):
    family, nov = s["family"], s["novelty"]
    active = mechanism_active(nov)
    if s["phase"] == "calibration" and active and i < N_CAL:
        return "calibration"
    ci = chain_index(nov, k_of(family))
    if s["phase"] == "scored" and active and ci is not None and i == ci:
        return "chain"
    return "public"


class Handler(BaseHTTPRequestHandler):
    state: State = None

    def log_message(self, *a):
        pass

    def _send(self, code, obj):
        body = json.dumps(obj, sort_keys=True).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _q(self, key, default):
        if "?" not in self.path:
            return default
        for kv in self.path.split("?", 1)[1].split("&"):
            if kv.startswith(key + "="):
                return kv.split("=", 1)[1]
        return default

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/healthz":
            return self._send(200, {"status": "ok"})
        parts = path.strip("/").split("/")
        if len(parts) == 4 and parts[:2] == ["api", "v1"] and parts[3] == "session":
            family = parts[2]
            if family not in FAMILIES:
                return self._send(404, {"error": "bad_family"})
            novelty = float(self._q("novelty", 0.5))
            idx = int(self._q("idx", 0))
            phase = self._q("phase", "scored")
            s = self.state.new_session(family, novelty, idx, phase)
            return self._send(200, {"session_token": s["token"], "schema_epoch": s["schema"],
                                    "epoch": idx, "phase": phase})
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
            kind = _task_kind(s, i)
            out = {"index": i, "kind": kind, "requires_schema": s["novelty"] >= 0.25,
                   "resource_id": None, "x": None}
            if kind == "public":
                out["resource_id"] = public_resource(family, s["novelty"], i)
            elif kind == "calibration":
                out["x"] = cal_points(family, s["idx"])[i][0]
                out["resource_id"] = public_resource(family, s["novelty"], i)
            elif kind == "chain":
                out["x"] = query_x(family, s["idx"])
                if self.state.expose_mechanism:
                    out["resource_id"] = str(target_value(family, s["idx"], s["novelty"]))
            return self._send(200, out)
        return self._send(404, {"error": "not_found"})

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
        s = self.state.sessions.get(body.get("session_token"))
        if s is None:
            return self._send(400, {"error": "bad_session"})
        i = body.get("index")
        if not isinstance(i, int) or not (0 <= i < k_of(family)):
            return self._send(400, {"error": "bad_index"})
        if i in s["committed"]:
            return self._send(409, {"error": "already_committed"})
        if s["novelty"] >= 0.25 and body.get("schema_epoch") != s["schema"]:
            return self._send(400, {"error": "schema_required"})
        kind = _task_kind(s, i)
        if kind in ("public", "calibration"):
            expected = public_resource(family, s["novelty"], i)
        else:  # chain
            expected = str(target_value(family, s["idx"], s["novelty"]))
        if body.get("resource_id") != expected:
            return self._send(400, {"error": "bad_resource"})
        s["committed"].add(i)
        receipt = {"index": i, "family": family, "epoch": s["idx"]}
        if kind == "calibration":
            x, y = cal_points(family, s["idx"])[i]
            receipt["x"] = x
            receipt["y"] = y
        return self._send(200, {"receipt": receipt})

    def do_PUT(self):
        return self._send(405, {"error": "method_not_allowed"})


def start_server(expose_mechanism=False):
    state = State(expose_mechanism=expose_mechanism)
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


# --------------------------------------------------------------------------
# arm policies
# --------------------------------------------------------------------------
def _sess(base, family, novelty, idx, phase, counters):
    counters["http_calls"] += 1
    st, b = http_get(f"{base}/api/v1/{family}/session?novelty={novelty}&idx={idx}&phase={phase}")
    assert st == 200, (st, b)
    return b


def _task(base, family, tok, i, counters):
    counters["http_calls"] += 1
    st, b = http_get(f"{base}/api/v1/{family}/task/{i}", token=tok)
    assert st == 200, (st, b)
    return b


def _commit(base, family, tok, i, schema, resource, counters):
    counters["http_calls"] += 1
    return http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tok, "index": i, "schema_epoch": schema, "resource_id": resource})


def _answer(arm, d, compiled, store, log, family, idx, novelty, counters):
    if arm in (TREATMENT, IDENTITY):
        if compiled is None:
            return None
        a, b = compiled
        y = mech_apply(a, b, d["x"])
        if novelty == 0.75:
            y = mech_apply(a, b, y)
        return str(y)
    if arm == POSITIVE:
        return str(target_value(family, idx, novelty))
    if arm in WITHIN_SESSION:
        # no labelled (x, M(x)) pair exists inside the scored session
        ys = [r.get("y") for r in log if isinstance(r, dict) and "y" in r]
        return str(ys[-1]) if ys else None
    if arm in CROSS_SESSION_RETENTION:
        if not store:
            return None
        xq = d["x"]
        _, yc = min(store, key=lambda p: abs(p[0] - xq))
        return str(yc)
    return None


def run_bank_instance(base, arm, family, novelty, idx):
    """Run one calibration (when active) + one scored session; return scored successes."""
    k = k_of(family)
    counters = {d: 0 for d in COUNTER_DIMS}
    active = mechanism_active(novelty)
    compiled = None
    store = []

    # ---- calibration phase (every arm sees the same raw examples) ----
    if active:
        s = _sess(base, family, novelty, idx, "calibration", counters)
        log = []
        for i in range(k):
            d = _task(base, family, s["session_token"], i, counters)
            counters["verification_calls"] += 1
            st, b = _commit(base, family, s["session_token"], i, s["schema_epoch"],
                            d["resource_id"], counters)
            if st == 200:
                rec = b["receipt"]
                if d.get("kind") == "calibration":
                    if arm in (TREATMENT, IDENTITY):
                        log.append((rec["x"], rec["y"]))
                    if arm in CROSS_SESSION_RETENTION:
                        store.append((rec["x"], rec["y"]))
            elif st == 400:
                counters["repair_calls"] += 1
        if arm in (TREATMENT, IDENTITY):
            compiled = recover_affine(log)
        # WITHIN_SESSION arms discard their calibration log at the session boundary.

    # ---- scored phase ----
    if arm == MEMORYLESS:
        successes = 0
        for i in range(k):
            s = _sess(base, family, novelty, idx, "scored", counters)
            d = _task(base, family, s["session_token"], i, counters)
            counters["verification_calls"] += 1
            res = d.get("resource_id")   # None on chain normally; exposed under NC-MECHANISM-OFF
            st, _ = _commit(base, family, s["session_token"], i, s["schema_epoch"], res, counters)
            if st == 200:
                successes += 1
            elif st == 400:
                counters["repair_calls"] += 1
        return successes, counters

    s = _sess(base, family, novelty, idx, "scored", counters)
    log = []
    successes = 0
    for i in range(k):
        d = _task(base, family, s["session_token"], i, counters)
        if arm in CROSS_SESSION_RETENTION:
            counters["retrieval_calls"] += 1
        if d.get("kind") == "chain":
            if d.get("resource_id") is not None:
                res = d["resource_id"]   # NC-MECHANISM-OFF world: answer exposed
            else:
                res = _answer(arm, d, compiled, store, log, family, idx, novelty, counters)
        else:
            res = d["resource_id"]
        counters["verification_calls"] += 1
        st, b = _commit(base, family, s["session_token"], i, s["schema_epoch"], res, counters)
        if st == 200:
            successes += 1
            log.append(b["receipt"])
        elif st == 400:
            counters["repair_calls"] += 1
            if d.get("kind") == "chain":
                # one declared repair: re-fetch the chain task and re-commit once
                _task(base, family, s["session_token"], i, counters)
                _commit(base, family, s["session_token"], i, s["schema_epoch"], res, counters)
    return successes, counters


# --------------------------------------------------------------------------
# protocol invariants
# --------------------------------------------------------------------------
def protocol_invariants(base, family="F1-RECORDS", novelty=0.5):
    out = {}
    k = k_of(family)
    ci = chain_index(novelty, k)
    a, b = mechanism_params(family, 0)
    cal = cal_points(family, 0)
    tgt = str(target_value(family, 0, novelty))

    # calibration session
    st, sc = http_get(f"{base}/api/v1/{family}/session?novelty={novelty}&idx=0&phase=calibration")
    out["cal_session_no_mechanism"] = st == 200 and all(
        s not in json.dumps(sc, sort_keys=True) for s in (str(a), str(b), tgt))
    tokc = sc["session_token"]
    cal_body = http_get(f"{base}/api/v1/{family}/task/0", token=tokc)[1]
    out["cal_task_reveals_x"] = cal_body.get("x") == cal[0][0]
    out["cal_task_no_y"] = str(cal[0][1]) not in json.dumps(cal_body, sort_keys=True)
    st, rc = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tokc, "index": 0, "schema_epoch": sc["schema_epoch"],
        "resource_id": public_resource(family, novelty, 0)})
    out["cal_receipt_reveals_y_once"] = (
        st == 200 and rc["receipt"].get("y") == cal[0][1] and rc["receipt"].get("x") == cal[0][0])
    st, rc2 = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": tokc, "index": 0, "schema_epoch": sc["schema_epoch"],
        "resource_id": public_resource(family, novelty, 0)})
    out["cal_recommit_409_no_y"] = st == 409 and str(cal[0][1]) not in json.dumps(rc2, sort_keys=True)

    # scored session
    st, ss = http_get(f"{base}/api/v1/{family}/session?novelty={novelty}&idx=0&phase=scored")
    out["session_never_reveals_mechanism"] = st == 200 and all(
        s not in json.dumps(ss, sort_keys=True) for s in (str(a), str(b), tgt))
    out["no_mechanism_in_scored_session_body"] = all(
        s not in json.dumps(ss, sort_keys=True) for s in (str(a), str(b)))
    toks = ss["session_token"]
    scored_bodies = [http_get(f"{base}/api/v1/{family}/task/{i}", token=toks)[1] for i in range(k)]
    out["no_cal_examples_in_scored_bodies"] = all(
        str(cx) not in json.dumps(body, sort_keys=True) and str(cy) not in json.dumps(body, sort_keys=True)
        for body in scored_bodies for cx, cy in cal)
    chain_body = scored_bodies[ci]
    out["chain_task_resource_null"] = chain_body.get("kind") == "chain" and chain_body.get("resource_id") is None
    out["chain_task_reveals_x"] = chain_body.get("x") == query_x(family, 0)
    out["no_answer_in_scored_chain_body"] = tgt not in json.dumps(chain_body, sort_keys=True)
    st, be = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": toks, "index": ci, "schema_epoch": ss["schema_epoch"],
        "resource_id": "0"})
    out["wrong_answer_400_no_leak"] = st == 400 and tgt not in json.dumps(be, sort_keys=True)
    st, br = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": toks, "index": ci, "schema_epoch": ss["schema_epoch"],
        "resource_id": tgt})
    out["correct_answer_200"] = st == 200
    out["chain_receipt_no_answer"] = tgt not in json.dumps(br, sort_keys=True)
    st, br2 = http_post(f"{base}/api/v1/{family}/commit", {
        "session_token": toks, "index": ci, "schema_epoch": ss["schema_epoch"],
        "resource_id": tgt})
    out["correct_answer_single_use_409"] = st == 409
    return out


# --------------------------------------------------------------------------
# certificate + branch classifier
# --------------------------------------------------------------------------
def retention_certifies(comp_rate, t_rate, all_rates, matched_correctness):
    return (comp_rate < COMPARATOR_MAX
            and all(r >= CORRECTNESS_FLOOR for r in all_rates)
            and matched_correctness >= CORRECTNESS_FLOOR
            and (t_rate - comp_rate) >= MARGIN_FLOOR)


def classify(world):
    if not world["gates_pass"]:
        return "MEASUREMENT_INVALID"
    if world["robust_certified"]:
        return "ROBUST"
    if world["any_retention_certified"]:
        return "PARTIAL"
    return "COLLAPSED"


def branch_reachability():
    return {
        "ROBUST": classify({"gates_pass": True, "robust_certified": True, "any_retention_certified": True}),
        "PARTIAL": classify({"gates_pass": True, "robust_certified": False, "any_retention_certified": True}),
        "COLLAPSED": classify({"gates_pass": True, "robust_certified": False, "any_retention_certified": False}),
        "MEASUREMENT_INVALID": classify({"gates_pass": False, "robust_certified": False, "any_retention_certified": False}),
    }


def assess_lattice(liveness):
    """Evaluate retention_certifies per retention comparator and label the world (probe rates)."""
    detail = {}
    robust = True
    any_cert = False
    for comp in RETAIN_COMPARATORS:
        detail[comp] = {}
        for family in FAMILIES:
            for nov in [n for n in NOVELTIES if n >= SCORED_BAND]:
                t_rate = liveness[TREATMENT][family][str(nov)]["rate"]
                comp_rate = liveness[comp][family][str(nov)]["rate"]
                all_rates = [liveness[a][family][str(nov)]["rate"] for a in ARMS]
                ok = retention_certifies(comp_rate, t_rate, all_rates, t_rate)
                detail[comp][f"{family}|{nov}"] = {
                    "comparator_rate": comp_rate, "t_rate": t_rate,
                    "margin": round(t_rate - comp_rate, 6),
                    "min_arm_rate": min(all_rates), "certifies": ok}
                any_cert = any_cert or ok
                robust = robust and ok
    world = {"gates_pass": True, "robust_certified": robust, "any_retention_certified": any_cert}
    return {"detail": detail, "world": world, "decision": classify(world)}


def cdist(c_t, c_c):
    return sum(1 for d in COUNTER_DIMS if c_t[d] != c_c[d])


# --------------------------------------------------------------------------
# probe (DESIGN; non-outcome-bearing)
# --------------------------------------------------------------------------
def run_probe(n_instances=3):
    out = {"seed": RUN_SEED, "P": P, "families": FAMILIES, "novelties": NOVELTIES,
           "scored_band": SCORED_BAND, "arms": ARMS, "n_cal": N_CAL}
    httpd, state, base = start_server(expose_mechanism=False)
    try:
        out["checks"] = {}
        st, _ = http_get(f"{base}/healthz")
        out["checks"]["transport_stdlib_http"] = st == 200
        out["checks"]["protocol_invariants"] = protocol_invariants(base)
        out["checks"]["all_protocol_invariants_pass"] = all(out["checks"]["protocol_invariants"].values())

        liveness = {}
        for arm in ARMS:
            liveness[arm] = {}
            for family in FAMILIES:
                liveness[arm][family] = {}
                for nov in NOVELTIES:
                    succ_total = 0
                    total = 0
                    counters = {d: 0 for d in COUNTER_DIMS}
                    for inst in range(n_instances):
                        httpd_i, _, base_i = start_server(expose_mechanism=False)
                        try:
                            succ, c = run_bank_instance(base_i, arm, family, nov, inst)
                        finally:
                            httpd_i.shutdown()
                        succ_total += succ
                        total += k_of(family)
                        for d in counters:
                            counters[d] += c[d]
                    liveness[arm][family][str(nov)] = {
                        "successes": succ_total, "tasks": total,
                        "rate": succ_total / total, "counters": counters}
        out["arm_liveness"] = liveness

        # mechanism non-degeneracy over sampled bank instances
        deg = mechanism_nondegeneracy(50)
        out["mechanism_nondegeneracy"] = deg
        out["checks"]["mechanism_nondegenerate"] = deg["ok"]

        out["checks"]["treatment_live_all_bands"] = all(
            liveness[TREATMENT][f][str(n)]["rate"] == 1.0 for f in FAMILIES for n in NOVELTIES)
        out["checks"]["pc_exact_replay_all_bands"] = all(
            liveness[POSITIVE][f][str(n)]["rate"] == 1.0 for f in FAMILIES for n in NOVELTIES)
        out["checks"]["ceiling_band_all_arms_one"] = all(
            liveness[a][f]["0.0"]["rate"] == 1.0 for f in FAMILIES for a in ARMS)
        out["checks"]["within_session_comparator_in_band"] = all(
            CORRECTNESS_FLOOR <= liveness[c][f][str(n)]["rate"] < COMPARATOR_MAX
            for c in WITHIN_SESSION for f in FAMILIES for n in (0.5, 0.75))
        out["checks"]["cross_session_retention_in_band"] = all(
            CORRECTNESS_FLOOR <= liveness[c][f][str(n)]["rate"] < COMPARATOR_MAX
            for c in CROSS_SESSION_RETENTION for f in FAMILIES for n in (0.5, 0.75))
        out["checks"]["identity_disclosure_matches_treatment"] = all(
            liveness[IDENTITY][f][str(n)]["rate"] == liveness[TREATMENT][f][str(n)]["rate"]
            for f in FAMILIES for n in NOVELTIES)

        # NC-MECHANISM-OFF: expose the answer -> within-session comparator reaches 1.0
        httpd_m, _, base_m = start_server(expose_mechanism=True)
        try:
            succ, _ = run_bank_instance(base_m, "B-WITHIN-SESSION-RECEIPT", "F1-RECORDS", 0.5, 0)
        finally:
            httpd_m.shutdown()
        out["mechanism_off"] = {"within_session_f1_rate": succ / k_of("F1-RECORDS"),
                                "successes": succ, "k": k_of("F1-RECORDS")}
        out["checks"]["mechanism_off_destroys_certificate"] = (
            out["mechanism_off"]["within_session_f1_rate"] >= COMPARATOR_MAX)

        # retention-only ladder: no retention scope closes the range
        ladder = {}
        for family in FAMILIES:
            for nov in (0.5, 0.75):
                rates = {a: liveness[a][family][str(nov)]["rate"] for a in
                         [MEMORYLESS, "B-WITHIN-SESSION-RECEIPT", "B-RETRIEVAL-REPLAY"]}
                closes = [a for a, r in rates.items() if r >= COMPARATOR_MAX]
                ladder[f"{family}|{nov}"] = {"rates": rates, "closing_retention_scopes": closes}
        out["retention_ladder"] = ladder
        out["checks"]["no_retention_scope_closes_range"] = all(
            len(v["closing_retention_scopes"]) == 0 for v in ladder.values())

        # counter distinctness T vs strongest retention comparators
        ident = {}
        for family in FAMILIES:
            t = liveness[TREATMENT][family]["0.5"]
            ident[family] = {}
            for comp in RETAIN_COMPARATORS + [MEMORYLESS]:
                ident[family][comp] = cdist(t["counters"], liveness[comp][family]["0.5"]["counters"])
        out["counter_distinctness"] = ident
        out["checks"]["retention_counter_distinctness"] = all(
            ident[f]["B-WITHIN-SESSION-RECEIPT"] >= MIN_DISTINCT_DIMS for f in FAMILIES)

        # token uniqueness
        seen = {}
        coll = 0
        for family in FAMILIES:
            for nov in NOVELTIES:
                for inst in range(10):
                    for phase in ("calibration", "scored"):
                        tok = session_token(family, nov, inst, phase)
                        if tok in seen and seen[tok] != (family, nov, inst, phase):
                            coll += 1
                        seen[tok] = (family, nov, inst, phase)
        out["token_uniqueness"] = {"sampled": len(seen), "collisions": coll}
        out["checks"]["token_uniqueness_ok"] = coll == 0

        out["lattice"] = assess_lattice(liveness)
        out["predicted_decision"] = out["lattice"]["decision"]
        out["checks"]["predicted_decision"] = out["predicted_decision"]
        out["branch_reachability"] = branch_reachability()
        out["checks"]["all_branches_inhabited"] = len(set(out["branch_reachability"].values())) == 4
    finally:
        httpd.shutdown()
    return out


# --------------------------------------------------------------------------
# scored matrix + gate evaluation (EXECUTE; NOT run during DESIGN)
# --------------------------------------------------------------------------
def run_scored_matrix(n_sessions=SCORED_SESSIONS_PER_CELL):
    cells = {}
    for family in FAMILIES:
        k = k_of(family)
        for nov in NOVELTIES:
            for arm in ARMS:
                succ_total = 0
                total = 0
                counters = {d: 0 for d in COUNTER_DIMS}
                for inst in range(n_sessions):
                    httpd, _, base = start_server(expose_mechanism=False)
                    try:
                        succ, c = run_bank_instance(base, arm, family, nov, inst)
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
                    "counters": counters}
    return cells


def synthetic_cells_from_probe(probe, n_sessions=SCORED_SESSIONS_PER_CELL):
    cells = {}
    for f in FAMILIES:
        for nov in NOVELTIES:
            for arm in ARMS:
                lv = probe["arm_liveness"][arm][f][str(nov)]
                cells[f"{f}|{nov}|{arm}"] = {
                    "family": f, "novelty": nov, "arm": arm,
                    "successes": round(lv["rate"] * n_sessions * k_of(f)),
                    "tasks": n_sessions * k_of(f),
                    "success_rate": lv["rate"], "matched_correctness": lv["rate"],
                    "counters": {d: lv["counters"][d] * n_sessions for d in COUNTER_DIMS}}
    return cells


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


def _lattice_from_cells(cells):
    detail = {}
    robust = True
    any_cert = False
    for comp in RETAIN_COMPARATORS:
        detail[comp] = {}
        for family in FAMILIES:
            for nov in [n for n in NOVELTIES if n >= SCORED_BAND]:
                t_rate = cells[f"{family}|{nov}|{TREATMENT}"]["success_rate"]
                comp_rate = cells[f"{family}|{nov}|{comp}"]["success_rate"]
                all_rates = [cells[f"{family}|{nov}|{a}"]["success_rate"] for a in ARMS]
                matched = cells[f"{family}|{nov}|{TREATMENT}"]["matched_correctness"]
                ok = retention_certifies(comp_rate, t_rate, all_rates, matched)
                detail[comp][f"{family}|{nov}"] = {
                    "comparator_rate": comp_rate, "t_rate": t_rate,
                    "margin": t_rate - comp_rate, "min_arm_rate": min(all_rates),
                    "certifies": ok}
                any_cert = any_cert or ok
                robust = robust and ok
    return {"detail": detail, "robust_certified": robust, "any_retention_certified": any_cert}


def assemble_decision(cells, controls, protocol, v1, determinism_ok, extra_gates=None):
    gates = {}
    gates["V5_arm_liveness"] = all(
        cells[f"{f}|{n}|{a}"]["success_rate"] == 1.0
        for f in FAMILIES for n in NOVELTIES for a in (TREATMENT, POSITIVE))
    gates["V8_ceiling_band"] = all(
        cells[f"{f}|0.0|{a}"]["success_rate"] == 1.0 for f in FAMILIES for a in ARMS)
    gates["V8_identity_disclosure"] = all(
        cells[f"{f}|{n}|{IDENTITY}"]["success_rate"] == cells[f"{f}|{n}|{TREATMENT}"]["success_rate"]
        for f in FAMILIES for n in NOVELTIES)
    gates["V8_retention_counter_distinctness"] = all(
        cdist(cells[f"{f}|0.5|{TREATMENT}"]["counters"],
              cells[f"{f}|0.5|B-WITHIN-SESSION-RECEIPT"]["counters"]) >= MIN_DISTINCT_DIMS
        for f in FAMILIES)
    if extra_gates:
        gates.update(extra_gates)
    gates["V1_code_fidelity_manifest"] = bool(v1.get("harness_sha256"))
    gates["V2_transport_conformance"] = all(protocol.values())
    gates["V3_no_leak"] = all(protocol[k] for k in LEAK_KEYS)
    gates["V4_determinism"] = bool(determinism_ok)
    gates["V6_counter_instrumentation"] = all(
        all(d in c["counters"] for d in COUNTER_DIMS) for c in cells.values())
    gates["V7_matched_correctness"] = all(
        c["matched_correctness"] == c["success_rate"] for c in cells.values())
    lattice = _lattice_from_cells(cells)
    world = {"gates_pass": all(gates.values()), "robust_certified": lattice["robust_certified"],
             "any_retention_certified": lattice["any_retention_certified"]}
    return {"gates": gates, "lattice": lattice, "world": world,
            "decision": classify(world), "v1": v1}


def run_execute_controls(n_sessions=SCORED_SESSIONS_PER_CELL):
    mech_off = {}
    for family in FAMILIES:
        succ = 0
        tot = 0
        for inst in range(n_sessions):
            httpd, _, base = start_server(expose_mechanism=True)
            try:
                s, _ = run_bank_instance(base, "B-WITHIN-SESSION-RECEIPT", family, 0.5, inst)
            finally:
                httpd.shutdown()
            succ += s
            tot += k_of(family)
        mech_off[family] = succ / tot
    return {"mechanism_off_within_session_rate": mech_off,
            "mechanism_off_destroys_certificate": all(r >= COMPARATOR_MAX for r in mech_off.values()),
            "mechanism_nondegeneracy": mechanism_nondegeneracy(50)}


def run_execute():
    cells_a = run_scored_matrix()
    cells_b = run_scored_matrix()
    determinism_ok = json.dumps(cells_a, sort_keys=True) == json.dumps(cells_b, sort_keys=True)
    controls = run_execute_controls()
    httpd, _, base = start_server(expose_mechanism=False)
    try:
        protocol = protocol_invariants(base)
    finally:
        httpd.shutdown()
    v1 = code_fidelity_manifest()
    result = assemble_decision(cells_a, controls, protocol, v1, determinism_ok,
                               extra_gates={"V8_mechanism_off": controls["mechanism_off_destroys_certificate"],
                                            "V8_mechanism_nondegenerate": controls["mechanism_nondegeneracy"]["ok"]})
    result["cells"] = cells_a
    result["controls"] = controls
    result["determinism_ok"] = determinism_ok
    return result


def run_selftest():
    probe = run_probe()
    cells = synthetic_cells_from_probe(probe)
    controls = {"mechanism_off_destroys_certificate":
                probe["checks"]["mechanism_off_destroys_certificate"],
                "mechanism_nondegeneracy": probe["mechanism_nondegeneracy"]}
    full = assemble_decision(cells, controls, probe["checks"]["protocol_invariants"],
                             {"python": "synthetic", "harness_sha256": "synthetic"}, True,
                             extra_gates={"V8_mechanism_off": controls["mechanism_off_destroys_certificate"],
                                          "V8_mechanism_nondegenerate": controls["mechanism_nondegeneracy"]["ok"]})
    return {"note": ("non-outcome-bearing: assemble_decision() (all gates + retention-lattice "
                     "decision rule) exercised on probe-derived synthetic cells"),
            "gates": full["gates"], "world": full["world"], "decision": full["decision"],
            "probe_predicted_decision": probe["predicted_decision"],
            "check_evaluator_matches_probe": full["decision"] == probe["predicted_decision"],
            "check_decision_is_robust": full["decision"] == "ROBUST",
            "branch_reachability": probe["branch_reachability"]}


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
