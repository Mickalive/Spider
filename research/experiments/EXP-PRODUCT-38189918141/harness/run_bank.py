#!/usr/bin/env python3
"""FROZEN RUNNER for EXP-PRODUCT-38189918141 (embedded verbatim in prereg.md).

Read-only shipped-carrier GENERALIZATION-BOUNDARY certificate. Evaluates the
as-installed parameterized carrier (src/spider/kernel.py, git blob b15ed848... /
sha256 718efa6a...) on a frozen, materially varied payload bank with an
independent localhost oracle. NEVER writes src/spider/ and never calls a model.

Arms (stable ids):
  T-SHIPPED       shipped carrier + parent 5-example induction (treatment)
  PC-UNSAFE-COARSE same carrier, support overridden to the carrier's own
                  __COARSE__ fallback (positive control for the safety oracle)
  B-WIDENED-3     same carrier, support overridden to ^item\\-[0-9]{3}$ (safe
                  widening comparator)
  NC-REJECT-ALL   empty registry (null floor: zero accepts, zero HTTP)
  B-LITERAL-KERNEL pre-promotion literal kernel, lacks distill_parameterized
  PC-EXACT-REPLAY 5 trained ids re-resolve EXECUTABLE (execution-path control)
  ORACLE-SERVER   localhost oracle: 200 for /api/items/item-[0-9]{3}, else 404

Env overrides (hermetic dry-run only; never change certificate logic):
  EXP_TARGET_ROOT : repo root containing src/spider (default: auto-detected)
  EXP_PROBE_MODE  : "1" records UNBOUND-RUN for V8 when freeze.json is absent
"""
from __future__ import annotations

import copy
import hashlib
import http.server
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

# -- canonical identities (mirrors prereg CANONICAL-HASHES) --
CARRIER_BLOB = "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796"
CARRIER_SHA256 = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
LITERAL_BLOB = "cfec98660b0277ccbf295e8a4119e8d81ddccf50"
LITERAL_SHA256 = "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61"
EXPERIMENT_ID = "EXP-PRODUCT-38189918141"
EXP_DIR = "research/experiments/EXP-PRODUCT-38189918141"
INTENT = "read_item"
TREATMENT_CONTEXT = {"resource_type": "item", "authenticated": True}
TRAIN_IDS = ["item-001", "item-002", "item-003", "item-004", "item-005"]
EXPECTED_SUPPORT = r"^item\-00[0-9]{1}$"
WIDENED_SUPPORT = r"^item\-[0-9]{3}$"
EXPECTED_MIN_CONFIDENCE = 0.8
COARSE = "__COARSE__"
LABEL_RE = re.compile(r"item-[0-9]{3}")
VALID_RESOURCE_RE = re.compile(r"^/api/items/item-[0-9]{3}$")


def detect_repo_root() -> Path:
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "pyproject.toml").exists() and (p / "src/spider").exists():
            return p
        p = p.parent
    raise RuntimeError("repo root not found upward from runner")


REPO_ROOT = Path(os.environ.get("EXP_TARGET_ROOT") or str(detect_repo_root()))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_source(spec: str) -> bytes:
    if spec.startswith("git:"):
        out = subprocess.run(["git", "-C", str(REPO_ROOT), "cat-file", "blob", spec[4:]],
                             capture_output=True)
        if out.returncode != 0:
            raise RuntimeError("git blob unavailable: " + out.stderr.decode()[:200])
        return out.stdout
    if spec.startswith("file:"):
        return Path(spec[5:]).read_bytes()
    raise RuntimeError("unknown source spec: " + spec)


# ---------------------------------------------------------------- frozen bank
def _bank_spec() -> list[dict]:
    C = dict(TREATMENT_CONTEXT)
    bank: list[dict] = []

    def add(bid, value, cls, intent=INTENT, context=None, params=None):
        bank.append({"bid": bid, "value": value, "cls": cls, "intent": intent,
                     "context": dict(context) if context is not None else dict(C),
                     "params": dict(params) if params is not None else {"item": value}})

    for n in ["000", "001", "002", "003", "004", "005", "006", "007", "008", "009",
              "010", "011", "042", "099", "100", "123", "256", "500", "999"]:
        add("IG-" + n, "item-" + n, "in_grammar")
    add("OG-LEN-0", "item-0", "len")
    add("OG-LEN-00", "item-00", "len")
    add("OG-LEN-4", "item-0000", "len")
    add("OG-LEN-5", "item-00000", "len")
    add("OG-LEN-6", "item-000000", "len")
    add("OG-ALPHA-00A", "item-00a", "alpha")
    add("OG-ALPHA-ABC", "item-abc", "alpha")
    add("OG-ALPHA-A00", "item-a00", "alpha")
    add("OG-ALPHA-0X1", "item-0x1", "alpha")
    add("OG-CASE-UP", "ITEM-000", "case")
    add("OG-CASE-TITLE", "Item-000", "case")
    add("OG-SEP-US", "item_000", "sep")
    add("OG-SEP-DOT", "item.000", "sep")
    add("OG-SEP-COLON", "item:000", "sep")
    add("OG-SEP-SLASH", "item/000", "sep")
    add("OG-WS-EMPTY", "", "ws")
    add("OG-WS-SPACE", " ", "ws")
    add("OG-WS-TAB", "\t", "ws")
    add("OG-WS-NL", "\n", "ws")
    add("OG-WS-TRAIL", "item-000 ", "ws")
    add("OG-WS-LEAD", " item-000", "ws")
    add("OG-WS-TRAILNL", "item-000\n", "ws")
    add("OG-WS-TRAILTAB", "item-000\t", "ws")
    add("OG-INJ-SEMI", "item-000;x", "inj")
    add("OG-INJ-SQ", "item-000'", "inj")
    add("OG-INJ-DQ", 'item-000"', "inj")
    add("OG-INJ-NUL", "item-000\x00", "inj")
    add("OG-INJ-TRAV", "../../etc/passwd", "inj")
    add("OG-INJ-ABS", "/api/items/item-000", "inj")
    add("OG-INJ-URL", "http://evil.example/item-000", "inj")
    add("OG-INJ-DOTDOT", "item-000/../secret", "inj")
    add("OG-QRY", "item-000?x=1", "query")
    add("OG-FRAG", "item-000#frag", "query")
    add("OG-PCT", "item-00%30", "query")
    add("OG-PCTNUL", "item-000%00", "query")
    add("OG-UNI-AR", "item-00\u0663", "unicode")
    add("OG-UNI-FW", "item-00\uff10", "unicode")
    add("OG-OTH-USER", "user-000", "other")
    add("OG-OTH-ORDER", "order-000", "other")
    add("OG-OTH-X", "itemx000", "other")
    add("OG-BIG-1000", "item-" + "0" * 1000, "big")
    add("OG-BIG-64", "item-" + "9" * 64, "big")
    add("OG-TYP-NONE", None, "type")
    add("OG-TYP-INT0", 0, "type")
    add("OG-TYP-FLOAT", 0.0, "type")
    add("OG-TYP-TRUE", True, "type")
    add("OG-TYP-FALSE", False, "type")
    add("OG-TYP-LIST", [], "type")
    add("OG-TYP-LISTV", ["item-000"], "type")
    add("OG-TYP-DICT", {}, "type")
    add("OG-TYP-DICTV", {"item": "item-000"}, "type")
    add("OG-TYP-BYTES", b"item-000", "type")
    add("OG-CTX-USERTYPE", "item-000", "ctx",
        context={"resource_type": "user", "authenticated": True})
    add("OG-CTX-NOAUTH", "item-000", "ctx",
        context={"resource_type": "item", "authenticated": False})
    add("OG-CTX-MISSAUTH", "item-000", "ctx", context={"resource_type": "item"})
    add("OG-CTX-EMPTY", "item-000", "ctx", context={})
    add("OG-CTX-INTENT", "item-000", "ctx", intent="delete_item")
    add("OG-CTX-WRONGKEY", "item-000", "ctx", params={"wrong_key": "item-000"})
    add("OG-CTX-NOPARAM", "item-000", "ctx", params={})
    return bank


def label_of(item: dict) -> str:
    v = item["value"]
    if not isinstance(v, str):
        return "OUT"
    if not LABEL_RE.fullmatch(v):
        return "OUT"
    if item["intent"] != INTENT:
        return "OUT"
    if item["context"] != TREATMENT_CONTEXT:
        return "OUT"
    if item["params"] != {"item": v}:
        return "OUT"
    return "IN"


def value_repr(v) -> str:
    if isinstance(v, str):
        s = repr(v)
        return s if len(s) <= 140 else s[:140] + "...<%d chars>" % len(v)
    if isinstance(v, (int, float, bool)) or v is None:
        return repr(v)
    return type(v).__name__ + ":" + repr(v)[:80]


# --------------------------------------------------------------- oracle server
class OracleHandler(http.server.BaseHTTPRequestHandler):
    count = 0

    def do_GET(self):
        type(self).count += 1
        path = self.path.split("?", 1)[0]
        if VALID_RESOURCE_RE.fullmatch(path):
            ident = path.rsplit("/", 1)[-1]
            body = {"type": "item", "id": ident, "data": "res:" + ident}
            self.send_response(200)
        else:
            body = {"error": "not_found", "path": path}
            self.send_response(404)
        payload = json.dumps(body).encode()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


def start_oracle():
    handler = type("Oracle", (OracleHandler,), {"count": 0})
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1], handler


def execute_action(bound):
    url = bound.get("url") if isinstance(bound, dict) else None
    if not isinstance(url, str):
        return None, {"exec_error": "no_url"}
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())
    except Exception as exc:
        return None, {"exec_error": type(exc).__name__ + ": " + str(exc)[:160]}


def drop_modules():
    for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
        sys.modules.pop(m, None)


def make_arm_mechanism(mech, support, tmpdir, tag):
    reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry
    reg = reg_cls(Path(tmpdir) / ("mechanisms_%s.jsonl" % tag))
    m = copy.deepcopy(mech)
    m.verification_rule = {"parameter_supports": {s: support for s in m.parameter_slots}}
    reg.upsert(m)
    return reg


def evaluate(kernel, bank, handler):
    records = []
    for item in bank:
        http0 = handler.count
        rec = {"bid": item["bid"], "cls": item["cls"], "label": label_of(item),
               "value": value_repr(item["value"])}
        try:
            r = kernel.resolve(item["intent"], dict(item["context"]), dict(item["params"]))
            rec["status"] = r.status.value
            rec["reason"] = r.reason
            bound = r.bound_action
        except Exception as exc:
            rec["status"] = "RESOLVE_ERROR"
            rec["reason"] = type(exc).__name__ + ": " + str(exc)[:160]
            bound = None
        rec["bound"] = bound is not None
        ex_status, body, verify = None, None, None
        if bound is not None:
            ex_status, body = execute_action(bound)
            if ex_status == 200 and isinstance(body, dict):
                try:
                    verify = kernel.verify(item.get("_mech_id"), body, dict(item["params"]))
                except Exception:
                    verify = False
            elif ex_status is not None:
                verify = False
        rec["exec_status"] = ex_status
        rec["verify"] = verify
        rec["exec_error"] = body.get("exec_error") if isinstance(body, dict) else None
        rec["http_delta"] = handler.count - http0
        records.append(rec)
    return records


def summarize(records):
    n_in = sum(1 for r in records if r["label"] == "IN")
    n_out = sum(1 for r in records if r["label"] == "OUT")
    accepts = [r for r in records if r["status"] == "EXECUTABLE"]
    fa = [r for r in records if r["label"] == "OUT" and r["status"] == "EXECUTABLE"]
    sfa = [r for r in fa if r["exec_status"] == 200 and r["verify"] is True]
    fr = [r for r in records if r["label"] == "IN" and r["status"] != "EXECUTABLE"]
    http_out = sum(r["http_delta"] for r in records if r["label"] == "OUT")
    http_total = sum(r["http_delta"] for r in records)
    cov = (n_in - len(fr)) / n_in if n_in else None
    return {
        "n_in": n_in, "n_out": n_out,
        "accept_count": len(accepts),
        "false_accept_count": len(fa),
        "silent_false_accept_count": len(sfa),
        "false_reject_count": len(fr),
        "coverage": cov,
        "http_on_out_label": http_out,
        "http_total": http_total,
        "false_accept_bids": [r["bid"] for r in fa],
        "silent_false_accept_bids": [r["bid"] for r in sfa],
        "false_reject_bids": [r["bid"] for r in fr],
        "accept_bids": [r["bid"] for r in accepts],
    }


# --------------------------------------------------------------- V8 freeze bind
def _extract(text, name):
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END " + re.escape(name) + r" -->",
                  text, re.S)
    if not m:
        raise RuntimeError("block %s not found in prereg.md" % name)
    return m.group(1)


def v8_freeze_binding(result):
    probe = os.environ.get("EXP_PROBE_MODE") == "1"
    exp = REPO_ROOT / EXP_DIR
    freeze_path = exp / "freeze.json"
    if not freeze_path.exists():
        if probe:
            result["observations"].append({"type": "binding",
                                           "V8": "UNBOUND-RUN: no freeze.json (probe mode only)."})
            return True
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "freeze.json missing at %s (EXECUTE mode)" % freeze_path}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    try:
        freeze = json.loads(freeze_path.read_text())

        def norm(s):
            return s.replace("\r\n", "\n").rstrip()

        prereg_b = (exp / "prereg.md").read_bytes()
        block = _extract(prereg_b.decode("utf-8"), "FROZEN RUNNER")
        this_src = Path(__file__).resolve().read_text(encoding="utf-8")
        ok_a = hashlib.sha256(prereg_b).hexdigest() == freeze["hashes"]["prereg.md"]
        ok_b = norm(this_src) == norm(block)
        ok_c = all(hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest() == h
                   for rel, h in freeze.get("artifact_hashes", {}).items())
    except Exception as exc:
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID", "reason": "freeze binding unreadable: " + str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    ok_all = ok_a and ok_b and ok_c
    result["certificate"]["V8_FREEZE_BINDING"] = {
        "status": "PASS" if ok_all else "FAIL", "prereg_sha_matches": ok_a,
        "runner_source_matches_frozen_block": ok_b, "artifact_hashes_match": ok_c,
        "reason": "hash-bound prereg; running source == FROZEN RUNNER block; freeze artifacts intact"}
    if not ok_all:
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    return True


# -------------------------------------------------------------------- one run
def run_once(carrier_cls, counters_cls, reg_cls, mech_cls, obs_cls):
    server, port, handler = start_oracle()
    try:
        tmp = tempfile.mkdtemp(prefix="exp38189918141_")

        def new_kernel(tag):
            reg = reg_cls(Path(tmp) / ("reg_%s.jsonl" % tag))
            return reg, carrier_cls(reg, counters=counters_cls())

        reg, kernel = new_kernel("treatment")
        observations = []
        for ident in TRAIN_IDS:
            url = "http://127.0.0.1:%d/api/items/%s" % (port, ident)
            st, body = execute_action({"url": url})
            if st != 200:
                raise RuntimeError("induction GET %s -> %s" % (ident, st))
            observations.append(obs_cls(intent=INTENT, state=dict(TREATMENT_CONTEXT),
                                        action={"method": "GET", "url": url},
                                        next_state=body, success=True,
                                        provenance={"exp": EXPERIMENT_ID, "role": "induction"}))
        mech = kernel.distill_parameterized(observations)
        if mech is None:
            raise RuntimeError("distill_parameterized returned None")
        reg.upsert(mech)
        support = mech.verification_rule["parameter_supports"]
        identity = {"slots": list(mech.parameter_slots), "support": support,
                    "confidence": mech.confidence}

        bank = _bank_spec()
        for item in bank:
            item["_mech_id"] = mech.mechanism_id

        treat_recs = evaluate(kernel, bank, handler)

        coarse_reg = make_arm_mechanism(mech, COARSE, tmp, "coarse")
        coarse_recs = evaluate(carrier_cls(coarse_reg, counters=counters_cls()), bank, handler)
        widened_reg = make_arm_mechanism(mech, WIDENED_SUPPORT, tmp, "widened")
        widened_recs = evaluate(carrier_cls(widened_reg, counters=counters_cls()), bank, handler)
        empty_reg = reg_cls(Path(tmp) / "reg_empty.jsonl")
        empty_recs = evaluate(carrier_cls(empty_reg, counters=counters_cls()), bank, handler)

        replay = []
        for ident in TRAIN_IDS:
            r = kernel.resolve(INTENT, dict(TREATMENT_CONTEXT), {"item": ident})
            replay.append({"id": ident, "status": r.status.value})
        replay_ok = all(x["status"] == "EXECUTABLE" for x in replay)

        return {
            "mechanism_identity": identity,
            "treatment": summarize(treat_recs),
            "control_coarse": summarize(coarse_recs),
            "comparator_widened": summarize(widened_recs),
            "null_reject_all": summarize(empty_recs),
            "pc_exact_replay": {"status": "PASS" if replay_ok else "FAIL", "replay": replay},
            "treatment_records": treat_recs,
        }
    finally:
        server.shutdown()


def main():
    result = {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": "product",
              "certificate": {}, "observations": [], "unresolved": []}
    if not v8_freeze_binding(result):
        return result

    kernel_path = REPO_ROOT / "src/spider/kernel.py"
    shipping_sha = sha256_bytes(kernel_path.read_bytes())
    result["identities"] = {"shipping_kernel_sha256": shipping_sha,
                            "carrier_expected_sha256": CARRIER_SHA256,
                            "carrier_git_blob": CARRIER_BLOB}
    if shipping_sha != CARRIER_SHA256:
        result["certificate"]["M-IDENTITY"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "shipping kernel sha %s != frozen carrier %s" % (shipping_sha, CARRIER_SHA256)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result
    result["certificate"]["M-IDENTITY"] = {
        "status": "PASS", "reason": "shipping kernel == frozen carrier " + CARRIER_BLOB}

    sys.path.insert(0, str(REPO_ROOT / "src"))
    try:
        drop_modules()
        spider = __import__("spider")
        Carrier = spider.SpiderKernel
        obs_cls = spider.Observation
        counters_cls = __import__("spider.kernel", fromlist=["TrajectoryCounters"]).TrajectoryCounters
        reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry
        min_conf = Carrier.__init__.__defaults__[0]
        if min_conf != EXPECTED_MIN_CONFIDENCE:
            raise RuntimeError("shipped min_confidence default %s != %s" % (min_conf, EXPECTED_MIN_CONFIDENCE))
    except Exception as exc:
        result["certificate"]["M-IDENTITY"] = {"status": "MEASUREMENT_INVALID",
                                              "reason": "import/threshold failure: " + str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result

    # B-LITERAL-KERNEL ablation
    try:
        lit = read_source("git:" + LITERAL_BLOB)
        if sha256_bytes(lit) != LITERAL_SHA256:
            raise RuntimeError("literal blob sha mismatch")
        with tempfile.TemporaryDirectory() as td:
            pkg = Path(td) / "spider"
            pkg.mkdir(parents=True)
            for name in ("models.py", "registry.py", "__init__.py"):
                (pkg / name).write_bytes((REPO_ROOT / "src/spider" / name).read_bytes())
            (pkg / "kernel.py").write_bytes(lit)
            sys.path.insert(0, td)
            drop_modules()
            litpkg = __import__("spider")
            has_param = hasattr(litpkg.SpiderKernel, "distill_parameterized")
            sys.path.remove(td)
            drop_modules()
        result["certificate"]["B-LITERAL-KERNEL"] = {
            "status": "PASS" if not has_param else "FAIL",
            "has_distill_parameterized": has_param,
            "reason": "literal pre-promotion kernel cannot construct the parameterized mechanism"}
    except Exception as exc:
        result["certificate"]["B-LITERAL-KERNEL"] = {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result

    drop_modules()
    spider = __import__("spider")
    Carrier = spider.SpiderKernel
    obs_cls = spider.Observation
    counters_cls = __import__("spider.kernel", fromlist=["TrajectoryCounters"]).TrajectoryCounters
    reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry

    run1 = run_once(Carrier, counters_cls, reg_cls, spider.Mechanism, obs_cls)
    run2 = run_once(Carrier, counters_cls, reg_cls, spider.Mechanism, obs_cls)
    det = json.dumps(run1["treatment"], sort_keys=True) == json.dumps(run2["treatment"], sort_keys=True) \
        and json.dumps(run1["control_coarse"], sort_keys=True) == json.dumps(run2["control_coarse"], sort_keys=True) \
        and run1["mechanism_identity"] == run2["mechanism_identity"]
    result["certificate"]["PC-DETERMINISM-REPEAT"] = {
        "status": "PASS" if det else "FAIL",
        "reason": "two independent runs produce identical treatment/coarse metrics and mechanism identity"}

    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test_*.py")
    tr = unittest.TextTestRunner(verbosity=0).run(suite)
    result["certificate"]["M-REGRESSION"] = {
        "status": "PASS" if (tr.wasSuccessful() and tr.testsRun >= 3) else "FAIL",
        "tests_run": tr.testsRun, "failures": len(tr.failures), "errors": len(tr.errors)}

    t = run1["treatment"]
    result["certificate"]["T-SHIPPED"] = {
        "status": "PASS" if (t["false_accept_count"] == 0 and t["http_on_out_label"] == 0
                             and run1["pc_exact_replay"]["status"] == "PASS") else "FAIL",
        "false_accept_count": t["false_accept_count"],
        "silent_false_accept_count": t["silent_false_accept_count"],
        "false_reject_count": t["false_reject_count"],
        "coverage": t["coverage"],
        "http_on_out_label": t["http_on_out_label"],
        "false_accept_bids": t["false_accept_bids"],
        "silent_false_accept_bids": t["silent_false_accept_bids"],
        "false_reject_bids": t["false_reject_bids"],
        "accept_bids": t["accept_bids"],
        "reason": "carrier safety (zero out-of-grammar binds, zero HTTP on out-of-grammar) "
                  "plus coverage on the declared 3-digit id scheme"}
    result["certificate"]["PC-EXACT-REPLAY"] = run1["pc_exact_replay"]
    result["certificate"]["PC-UNSAFE-COARSE"] = {
        "status": "PASS" if run1["control_coarse"]["false_accept_count"] >= 1 else "FAIL",
        "false_accept_count": run1["control_coarse"]["false_accept_count"],
        "false_accept_bids": run1["control_coarse"]["false_accept_bids"],
        "reason": "positive control: the carrier's own __COARSE__ fallback must over-accept"}
    result["certificate"]["NC-REJECT-ALL"] = {
        "status": "PASS" if (run1["null_reject_all"]["accept_count"] == 0
                             and run1["null_reject_all"]["http_total"] == 0) else "FAIL",
        "accept_count": run1["null_reject_all"]["accept_count"],
        "http_total": run1["null_reject_all"]["http_total"],
        "reason": "null floor: empty registry accepts nothing and issues no HTTP"}
    result["certificate"]["B-WIDENED-3"] = {
        "status": "PASS" if (run1["comparator_widened"]["false_accept_count"] == 0
                             and run1["comparator_widened"]["coverage"] == 1.0) else "FAIL",
        "false_accept_count": run1["comparator_widened"]["false_accept_count"],
        "coverage": run1["comparator_widened"]["coverage"],
        "reason": "strong comparator: a safe 3-digit widening that is both safe and complete on the bank"}

    result["arms"] = {
        "T-SHIPPED": run1["treatment"],
        "PC-UNSAFE-COARSE": run1["control_coarse"],
        "B-WIDENED-3": run1["comparator_widened"],
        "NC-REJECT-ALL": run1["null_reject_all"],
    }
    result["mechanism_identity"] = run1["mechanism_identity"]
    result["treatment_records"] = run1["treatment_records"]
    result["certificate"]["M-BOUNDARY"] = {
        "induced_support": run1["mechanism_identity"]["support"],
        "accepted_in_grammar_ids": sorted(
            r["value"] for r in run1["treatment_records"]
            if r["label"] == "IN" and r["status"] == "EXECUTABLE"),
        "refused_in_grammar_ids": sorted(
            r["value"] for r in run1["treatment_records"]
            if r["label"] == "IN" and r["status"] != "EXECUTABLE"),
        "reason": "exact generalization boundary: which declared 3-digit ids the shipped "
                  "single-observation-length support binds vs refuses"}

    validity_gates = ("V8_FREEZE_BINDING", "M-IDENTITY", "M-REGRESSION",
                      "PC-DETERMINISM-REPEAT", "PC-EXACT-REPLAY", "B-LITERAL-KERNEL")
    validity = all(result["certificate"][k]["status"] == "PASS" for k in validity_gates)
    failed_validity = [k for k in validity_gates if result["certificate"][k]["status"] != "PASS"]
    sensitivity = (result["certificate"]["PC-UNSAFE-COARSE"]["status"] == "PASS"
                   and result["certificate"]["NC-REJECT-ALL"]["status"] == "PASS")
    if not validity:
        result["status"], result["outcome"] = "MEASUREMENT_INVALID", "NOT_APPLICABLE"
        result["reason"] = "instrument/validity gates failed: " + ", ".join(failed_validity)
        return result
    if not sensitivity:
        result["status"], result["outcome"] = "MEASUREMENT_INVALID", "NOT_APPLICABLE"
        result["reason"] = "safety oracle failed its sensitivity/null controls; cannot certify"
        return result

    fa = t["false_accept_count"]
    fr = t["false_reject_count"]
    widened_ok = result["certificate"]["B-WIDENED-3"]["status"] == "PASS"
    if fa > 0 or t["http_on_out_label"] > 0:
        result["status"], result["outcome"] = "COMPLETE", "FALSIFIES"
        result["decision"] = "SAFETY_DEFECT"
        result["reason"] = ("%d out-of-grammar payload(s) bound (silent=%d), HTTP on "
                            "out-of-grammar=%d; external consumption must be blocked until "
                            "resolve()/support is fixed"
                            % (fa, t["silent_false_accept_count"], t["http_on_out_label"]))
    elif fr == 0:
        result["status"], result["outcome"] = "COMPLETE", "SUPPORTS"
        result["decision"] = "SAFE_AND_COMPLETE"
        result["reason"] = "zero false accepts and full coverage on the declared bank"
    else:
        result["status"], result["outcome"] = "COMPLETE", "MIXED"
        result["decision"] = "SAFE_BUT_CONSERVATIVE"
        alt = ("B-WIDENED-3 demonstrates a safe, complete alternative"
               if widened_ok else "B-WIDENED-3 did not demonstrate a safe complete alternative")
        result["reason"] = ("zero false accepts (safe abstention boundary) but %d/%d legitimate "
                            "declared ids refused; %s" % (fr, t["n_in"], alt))
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True, default=repr))

