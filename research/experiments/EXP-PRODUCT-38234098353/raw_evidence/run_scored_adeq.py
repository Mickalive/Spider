#!/usr/bin/env python3
"""FROZEN RUNNER -- EXP-PRODUCT-38234098353 (product lane).

Measured-trust-root + probe-adequacy declaration certificate. Deterministic,
stdlib-only, credential-free, loopback HTTP oracle.

The runner is embedded verbatim in prereg.md and is the frozen interpretation
object. It measures ONLY the frozen bank/arms/controls defined in this file.
"""
from __future__ import annotations

import copy
import hashlib
import http.server
import itertools
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

# --------------------------------------------------------------------------
# FROZEN CONSTANTS
# --------------------------------------------------------------------------
EXPERIMENT_ID = "EXP-PRODUCT-38234098353"
PROBE_BUDGET = 256
PROBE_SEED = 38234098
PROBE_ALPHA = "0123456789abcdef"
PROBE_MAXLEN = 4
PROV_TAU = 0.5
MIN_COVERAGE_ANCHOR = 0.6750
COVERAGE_TOL = 1e-9

# ---------------------------------------------------------------------------
# Expansion bank B1..B10 (within-envelope) + B11 (trusted boundary).
# Origins O1..O4 trusted by the MEASURED provenance scorer; O5,O6 untrusted.
# ---------------------------------------------------------------------------
FAMILIES = [
 dict(fam="B1", origin="O1", resource="txn", role="SOUND",
      true=r"^txn\-[0-9]{3,4}$", decl=r"^txn\-[0-9]{3,4}$",
      train=["txn-001", "txn-002"],
      in_extra=["txn-1001", "txn-2002", "txn-3003", "txn-4004", "txn-5005", "txn-6006"],
      out_extra=["txn-", "txn-00", "txn-00000", " txn-001"]),
 dict(fam="B2", origin="O2", resource="usr", role="SOUND",
      true=r"^usr\-[a-f]{3,4}$", decl=r"^usr\-[a-f]{3,4}$",
      train=["usr-aaa", "usr-bbb"],
      in_extra=["usr-aaaa", "usr-bbbb", "usr-cccc", "usr-dddd", "usr-eeee", "usr-ffff"],
      out_extra=["usr-", "usr-aa", "usr-aaaaa", " usr-aaa"]),
 dict(fam="B3", origin="O3", resource="ord", role="SOUND",
      true=r"^ord\-[0-9]{3,4}$", decl=r"^ord\-[0-9]{3,4}$",
      train=["ord-001", "ord-002"],
      in_extra=["ord-1001", "ord-2002", "ord-3003", "ord-4004", "ord-5005", "ord-6006"],
      out_extra=["ord-", "ord-00", "ord-00000", " ord-001"]),
 dict(fam="B4", origin="O4", resource="shp", role="SOUND",
      true=r"^shp\-[a-f]{3,4}$", decl=r"^shp\-[a-f]{3,4}$",
      train=["shp-aaa", "shp-bbb"],
      in_extra=["shp-aaaa", "shp-bbbb", "shp-cccc", "shp-dddd", "shp-eeee", "shp-ffff"],
      out_extra=["shp-", "shp-aa", "shp-aaaaa", " shp-aaa"]),
 dict(fam="B5", origin="O2", resource="inv", role="EVADER_P",
      true=r"^inv\-[0-9]{3}$", decl=r"^inv\-[0-9]{3,4}$",
      train=["inv-001", "inv-002"], in_extra=[],
      out_extra=["inv-1000", "inv-2000", "inv-3000"]),
 dict(fam="B6", origin="O3", resource="shl", role="EVADER_P",
      true=r"^shl\-[a-f]{3}$", decl=r"^shl\-[a-f]{3,4}$",
      train=["shl-aaa", "shl-bbb"], in_extra=[],
      out_extra=["shl-aaaa", "shl-bbbb", "shl-cccc"]),
 dict(fam="B7", origin="O1", resource="not", role="EVADER_A",
      true=r"^not\-[a-f]{3}$", decl=r"^not\-[a-f]{3}$|^not\-[A-Z]{3}$",
      train=["not-aaa", "not-bbb"], in_extra=[],
      out_extra=["not-ABC", "not-XYZ", "not-QQQ"]),
 dict(fam="B8", origin="O3", resource="rpt", role="EVADER_A",
      true=r"^rpt\-[a-f]{3}$", decl=r"^rpt\-[a-f]{3}$|^rpt\-[A-Z]{3}$",
      train=["rpt-aaa", "rpt-bbb"], in_extra=[],
      out_extra=["rpt-ABC", "rpt-XYZ", "rpt-QQQ"]),
 dict(fam="B9", origin="O5", resource="sku", role="EVADER_S",
      true=r"^sku\-[0-9]{4}$", decl=r"^sku\-[0-9]{4}$|^sku\-(?:abcd|abef|beef)$",
      train=["sku-0001", "sku-0002"], in_extra=[],
      out_extra=["sku-abcd", "sku-abef", "sku-beef"]),
 dict(fam="B10", origin="O4", resource="tkt", role="EVADER_P",
      true=r"^tkt\-[a-f]{3}$", decl=r"^tkt\-[a-f]{3,4}$",
      train=["tkt-aaa", "tkt-bbb"], in_extra=[],
      out_extra=["tkt-aaaa", "tkt-bbbb", "tkt-cccc"]),
 dict(fam="B11", origin="O4", resource="wgt", role="BOUNDARY",
      true=r"^wgt\-[0-9]{4}$", decl=r"^wgt\-[0-9]{4}$|^wgt\-(?:abcd|abef|beef)$",
      train=["wgt-0001", "wgt-0002"], in_extra=[],
      out_extra=["wgt-abcd", "wgt-abef", "wgt-beef"]),
]
FAM_IDS = [f["fam"] for f in FAMILIES]
FAM_BY_ID = {f["fam"]: f for f in FAMILIES}
TRUE_RX = {f["fam"]: re.compile(f["true"]) for f in FAMILIES}
DECL = {f["fam"]: f["decl"] for f in FAMILIES}
WITHIN_ENVELOPE = [f for f in FAM_IDS if f != "B11"]
BOUNDARY = ["B11"]

EXPECTED_INDUCED = {
 "B1": r"^txn\-00[0-9]{1}$", "B2": r"^usr\-[a-z]{3}$",
 "B3": r"^ord\-00[0-9]{1}$", "B4": r"^shp\-[a-z]{3}$",
 "B5": r"^inv\-00[0-9]{1}$", "B6": r"^shl\-[a-z]{3}$",
 "B7": r"^not\-[a-z]{3}$", "B8": r"^rpt\-[a-z]{3}$",
 "B9": r"^sku\-000[0-9]{1}$", "B10": r"^tkt\-[a-z]{3}$",
 "B11": r"^wgt\-000[0-9]{1}$",
}
EXPECTED_ADEQUACY = {
 "B1": True, "B2": True, "B3": True, "B4": True,
 "B5": True, "B6": True, "B7": False, "B8": False,
 "B9": True, "B10": True, "B11": True,
}
# ---------------------------------------------------------------------------
# Provenance calibration ledgers: each origin has 4 historical declarations.
# Trusted origins (O1..O4): 4 sound. Untrusted (O5,O6): 1 sound + 3 unsound
# budget-sparse over-accepts. The score is MEASURED by mining negatives with
# the fixed probe and running the shipped certificate against the truth label.
# ---------------------------------------------------------------------------
CAL = []
for _origin in ("O1", "O2", "O3", "O4"):
    for _k in range(4):
        _res = "t%s%d" % (_origin.lower(), _k)
        _true = r"^%s\-[0-9]{3}$" % _res
        CAL.append(dict(origin=_origin, res=_res, true=_true, decl=_true,
                        positives=["%s-001" % _res, "%s-002" % _res], truth="SOUND"))
for _origin in ("O5", "O6"):
    _res = "s%s" % _origin.lower()
    _true = r"^%s\-[0-9]{3}$" % _res
    CAL.append(dict(origin=_origin, res=_res, true=_true, decl=_true,
                    positives=["%s-001" % _res, "%s-002" % _res], truth="SOUND"))
    for _k in range(3):
        _res = "u%s%d" % (_origin.lower(), _k)
        _true = r"^%s\-[0-9]{4}$" % _res
        _decl = r"^%s\-[0-9]{4}$|^%s\-(?:abcd|abef|beef)$" % (_res, _res)
        CAL.append(dict(origin=_origin, res=_res, true=_true, decl=_decl,
                        positives=["%s-0001" % _res, "%s-0002" % _res], truth="UNSOUND"))
CAL_ORIGINS = ("O1", "O2", "O3", "O4", "O5", "O6")
TRUSTED = ("O1", "O2", "O3", "O4")

SRC = os.environ.get("SPIDER_SRC", "src")
PACKET_DIR = os.environ.get("EXP_PACKET_DIR", ".")

FENCE = chr(96) * 3


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_probe_space() -> list[str]:
    space = ["".join(c) for n in range(1, PROBE_MAXLEN + 1) for c in itertools.product(PROBE_ALPHA, repeat=n)]
    random.Random(PROBE_SEED).shuffle(space)
    return space


PROBE_SPACE = build_probe_space()
FIRST_BUDGET = set(PROBE_SPACE[:PROBE_BUDGET])


def literal_prefix(decl: str) -> str:
    out, i = [], 0
    if decl.startswith("^"):
        i = 1
    while i < len(decl):
        ch = decl[i]
        if ch == "\\" and i + 1 < len(decl) and decl[i + 1] == "-":
            out.append("-")
            i += 2
            continue
        if ch in "^$.*+?()[]{}|\\":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def _expand_class(content: str) -> set:
    chars: set = set()
    i = 0
    while i < len(content):
        if i + 2 < len(content) and content[i + 1] == "-":
            chars.update(chr(c) for c in range(ord(content[i]), ord(content[i + 2]) + 1))
            i += 3
        else:
            chars.add(content[i])
            i += 1
    return chars


def probe_adequacy(decl: str) -> bool:
    """Bounded syntactic probe-adequacy detector.

    ADEQUATE (return True) iff the declaration cannot be shown to accept a
    character outside PROBE_ALPHA or a string longer than PROBE_MAXLEN reachable
    characters, i.e. its syntactic over-accept envelope is within the fixed
    probe's reachable region. INADEQUATE (False) if it contains a character
    class that expands outside PROBE_ALPHA, an explicit uppercase literal, or a
    quantifier bound beyond PROBE_MAXLEN.

    Deliberately BLIND to within-envelope budget-sparse over-accepts (literals
    over PROBE_ALPHA of length <= PROBE_MAXLEN that the bounded probe does not
    sample); that blindness is the exhibited residual boundary B11.
    """
    for m in re.finditer(r"\[([^\]]*)\]", decl):
        content = m.group(1)
        if content.startswith("^"):
            return False
        if any(ch not in PROBE_ALPHA for ch in _expand_class(content)):
            return False
    stripped = re.sub(r"\[[^\]]*\]", "", decl)
    if re.search(r"[A-Z]", stripped):
        return False
    for m in re.finditer(r"\{(\d+)(,(\d*))?\}", decl):
        lo = int(m.group(1))
        if lo > PROBE_MAXLEN:
            return False
        if m.group(2) is not None and m.group(3) == "":
            return False
        if m.group(3):
            if int(m.group(3)) > PROBE_MAXLEN:
                return False
    return True


# --------------------------------------------------------------------------
# loopback oracle
# --------------------------------------------------------------------------
class _OracleHandler(http.server.BaseHTTPRequestHandler):
    grammars: dict = {}
    count = 0

    def do_GET(self):
        type(self).count += 1
        parts = self.path.split("?", 1)[0].split("/")
        ok = False
        if len(parts) >= 3:
            res, val = parts[-2], parts[-1]
            for name, rx in type(self).grammars.items():
                if res in (name, name + "s") and rx.fullmatch(val) is not None:
                    ok = True
                    break
        body = json.dumps({"ok": ok}).encode()
        self.send_response(200 if ok else 404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


def start_oracle(grammars: dict):
    handler = type("Oracle", (_OracleHandler,), {"count": 0, "grammars": grammars})
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1], handler


def oracle_ok(port: int, resource: str, value: str) -> bool:
    url = "http://127.0.0.1:%d/api/%ss/%s" % (port, resource, value)
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.status == 200
    except Exception:
        return False


def mine_negatives_resource(resource: str, decl: str, port: int, budget: int = PROBE_BUDGET):
    rx = re.compile(decl)
    prefix = literal_prefix(decl)
    bank, candidates, calls = [], 0, 0
    for tok in PROBE_SPACE:
        if candidates >= budget:
            break
        v = prefix + tok
        candidates += 1
        if rx.fullmatch(v) is None:
            continue
        calls += 1
        if not oracle_ok(port, resource, v) and v not in bank:
            bank.append(v)
    return bank, candidates, calls


# --------------------------------------------------------------------------
# real carrier induction + ingestion
# --------------------------------------------------------------------------
def build_mechanisms(port: int):
    if SRC not in sys.path:
        sys.path.insert(0, SRC)
    import spider
    from spider.registry import MechanismRegistry

    by_intent: dict = {}
    for f in FAMILIES:
        for v in f["train"]:
            o = spider.Observation(
                intent="get_" + f["resource"],
                state={"resource_type": f["resource"], "authenticated": True},
                action={"method": "GET", "url": "http://127.0.0.1:9/api/%ss/%s" % (f["resource"], v)},
                next_state={"ok": True}, success=True, provenance=None)
            by_intent.setdefault(o.intent, []).append(o)
    kernel = spider.SpiderKernel(MechanismRegistry(Path(tempfile.mkdtemp()) / "m.jsonl"))
    mechs = {}
    for f in FAMILIES:
        m = kernel.distill_parameterized(by_intent["get_" + f["resource"]])
        if m is None:
            raise RuntimeError("induction failed for " + f["fam"])
        mechs[f["fam"]] = m
    return kernel, spider, mechs


def effective_support(mech, slot: str) -> str:
    return mech.verification_rule.get("parameter_supports", {})[slot]


def cert_status(mech) -> str:
    return (mech.verification_rule or {}).get("declaration_certificate", {}).get("status", "NONE")


# --------------------------------------------------------------------------
# measured provenance scorer
# --------------------------------------------------------------------------
def provenance_scores(cal_port: int) -> dict:
    scores = {}
    for origin in CAL_ORIGINS:
        entries = [e for e in CAL if e["origin"] == origin]
        correct = 0
        for e in entries:
            bank, _, _ = mine_negatives_resource(e["res"], e["decl"], cal_port)
            from spider.kernel import certify_declaration
            ok, _reason = certify_declaration(e["decl"], e["positives"], bank)
            verdict = "SOUND" if ok else "UNSOUND"
            if verdict == e["truth"]:
                correct += 1
        scores[origin] = correct / len(entries)
    return scores


def inferred_allowlist(scores: dict) -> tuple:
    return tuple(o for o in CAL_ORIGINS if scores[o] >= PROV_TAU - COVERAGE_TOL)


# --------------------------------------------------------------------------
# general declaration arm
# --------------------------------------------------------------------------
def arm_decl(kernel, mechs, bank_port, *, origin_gate, adequacy, growth, raw):
    new, meta = {}, {}
    for f in FAMILIES:
        fam, slot = f["fam"], mechs[f["fam"]].parameter_slots[0]
        m = copy.deepcopy(mechs[fam])
        decl = DECL[fam]
        m.verification_rule = dict(m.verification_rule or {})
        if raw:
            sup = dict(m.verification_rule.get("parameter_supports", {}))
            sup[slot] = decl
            m.verification_rule["parameter_supports"] = sup
            m.verification_rule["declaration_certificate"] = {"status": "RAW", "slot": slot}
            meta[fam] = "RAW"
            new[fam] = m
            continue
        if origin_gate is not None and f["origin"] not in origin_gate:
            m.verification_rule["provenance_gate"] = "REFUSED_ORIGIN"
            meta[fam] = "PROV_REFUSED"
            new[fam] = m
            continue
        if adequacy and not probe_adequacy(decl):
            m.verification_rule["adequacy_gate"] = "REFUSED_INADEQUATE"
            meta[fam] = "ADEQ_REFUSED"
            new[fam] = m
            continue
        bank = mine_negatives_resource(f["resource"], decl, bank_port)[0] if growth else []
        kernel.ingest_declaration(m, decl, f["train"], bank, slot)
        meta[fam] = cert_status(m)
        new[fam] = m
    return new, meta


def arm_substitute_true(mechs):
    out = {}
    for f in FAMILIES:
        fam, slot = f["fam"], mechs[f["fam"]].parameter_slots[0]
        m = copy.deepcopy(mechs[fam])
        rule = dict(m.verification_rule or {})
        sup = dict(rule.get("parameter_supports", {}))
        sup[slot] = f["true"]
        rule["parameter_supports"] = sup
        rule["declaration_certificate"] = {"status": "ORACLE", "slot": slot}
        m.verification_rule = rule
        out[fam] = m
    return out


# --------------------------------------------------------------------------
# evaluation
# --------------------------------------------------------------------------
def items_for(fam: str):
    f = FAM_BY_ID[fam]
    rx = TRUE_RX[fam]
    return [(v, rx.fullmatch(v) is not None) for v in f["train"] + f["in_extra"] + f["out_extra"]]


def evaluate(arm: dict, port: int):
    from spider.kernel import _support_accepts
    res, oracle_calls = {}, 0
    for fam in FAM_IDS:
        m = arm[fam]
        slot = m.parameter_slots[0]
        sup = effective_support(m, slot)
        status = cert_status(m)
        exe_in = tot_in = fa = http_out = viol = 0
        for v, label in items_for(fam):
            if label:
                tot_in += 1
            if _support_accepts(sup, v):
                oracle_ok(port, FAM_BY_ID[fam]["resource"], v)
                oracle_calls += 1
                if label:
                    exe_in += 1
                else:
                    fa += 1
                    http_out += 1
            if status == "REFUSED" and sup == DECL[fam]:
                viol += 1
        res[fam] = dict(exe_in=exe_in, tot_in=tot_in, fa=fa, http_out=http_out,
                        support=sup, cert=status, violations=viol)
    return res, oracle_calls


def summarize(res: dict, fams):
    exe_in = sum(res[f]["exe_in"] for f in fams)
    tot_in = sum(res[f]["tot_in"] for f in fams)
    return dict(
        false_accept_count=sum(res[f]["fa"] for f in fams),
        http_on_out_count=sum(res[f]["http_out"] for f in fams),
        refusal_semantics_violations=sum(res[f]["violations"] for f in fams),
        executed_in=exe_in, total_in=tot_in,
        coverage=(exe_in / tot_in) if tot_in else 0.0,
        per_family={f: {"fa": res[f]["fa"], "cert": res[f]["cert"],
                        "coverage": (res[f]["exe_in"] / res[f]["tot_in"]) if res[f]["tot_in"] else None}
                    for f in fams},
    )


def refusal_violation_check(kernel, mechs, bank_port):
    """Exercise the REAL SpiderKernel.ingest_declaration refusal path on a
    probeable evader (B5): growth supplies negatives and the certificate refuses
    while preserving the induced support."""
    fam = "B5"
    f = FAM_BY_ID[fam]
    slot = mechs[fam].parameter_slots[0]
    m = copy.deepcopy(mechs[fam])
    before = effective_support(m, slot)
    bank = mine_negatives_resource(f["resource"], DECL[fam], bank_port)[0]
    kernel.ingest_declaration(m, DECL[fam], f["train"], bank, slot)
    status = cert_status(m)
    preserved = effective_support(m, slot) == before
    return dict(status=status, support_preserved=preserved, refused=(status == "REFUSED"), bank_size=len(bank))


# --------------------------------------------------------------------------
# regression gate
# --------------------------------------------------------------------------
def run_regression():
    env = dict(os.environ)
    env["PYTHONPATH"] = SRC + os.pathsep + env.get("PYTHONPATH", "")
    try:
        p = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                           capture_output=True, text=True, env=env, timeout=600)
    except Exception as exc:  # noqa
        return dict(tests_run=0, ok=False, detail="regression could not run: %s" % exc)
    out = (p.stderr or "") + (p.stdout or "")
    m = re.search(r"Ran (\d+) tests?", out)
    tests_run = int(m.group(1)) if m else 0
    ok = (p.returncode == 0) and tests_run >= 3
    return dict(tests_run=tests_run, ok=ok, returncode=p.returncode)


# --------------------------------------------------------------------------
# freeze binding
# --------------------------------------------------------------------------
def _normalize(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def _extract_runner_block(prereg_path: str):
    if not os.path.exists(prereg_path):
        return None
    text = open(prereg_path, encoding="utf-8").read()
    marker = "BEGIN FROZEN RUNNER"
    if marker not in text:
        return None
    tail = text.split(marker, 1)[1]
    if FENCE not in tail:
        return None
    body = tail.split(FENCE, 1)[1]
    if "\n" in body:
        body = body.split("\n", 1)[1]
    end = body.find(FENCE)
    return body[:end] if end >= 0 else body


def v8_binding():
    fr = os.path.join(PACKET_DIR, "freeze.json")
    prereg = os.path.join(PACKET_DIR, "prereg.md")
    checks = {}
    try:
        running = open(__file__, encoding="utf-8").read()
    except Exception:
        running = ""
    block = _extract_runner_block(prereg)
    if block is not None and running:
        checks["runner_block"] = _normalize(block) == _normalize(running)
    if os.path.exists(fr):
        freeze = json.load(open(fr))
        checks["prereg_sha"] = sha256_file(prereg) == freeze.get("hashes", {}).get("prereg.md")
        for rel, want in (freeze.get("artifact_hashes") or {}).items():
            checks[rel] = os.path.exists(rel) and sha256_file(rel) == want
        status = "PASS" if (checks and all(checks.values())) else "FAIL"
        return dict(gate="V8_FREEZE_BINDING", status=status, mode="BOUND", checks=checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return dict(gate="V8_FREEZE_BINDING", status=status, mode="UNBOUND-RUN",
                reason="freeze.json absent (probe mode)", checks=checks)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def run_once(probe_mode: bool):
    grammars = {f["resource"]: TRUE_RX[f["fam"]] for f in FAMILIES}
    for e in CAL:
        grammars[e["res"]] = re.compile(e["true"])
    server, port, _ = start_oracle(grammars)

    kernel, spider, mechs = build_mechanisms(port)
    induced = {fam: effective_support(mechs[fam], mechs[fam].parameter_slots[0]) for fam in FAM_IDS}
    slots = {fam: mechs[fam].parameter_slots for fam in FAM_IDS}

    scores = provenance_scores(port)
    allowlist = inferred_allowlist(scores)
    adequacy = {fam: probe_adequacy(DECL[fam]) for fam in FAM_IDS}

    T, Tmeta = arm_decl(kernel, mechs, port, origin_gate=allowlist, adequacy=True, growth=True, raw=False)
    A_NO_ADEQ, _ = arm_decl(kernel, mechs, port, origin_gate=allowlist, adequacy=False, growth=True, raw=False)
    A_NO_PROV, _ = arm_decl(kernel, mechs, port, origin_gate=None, adequacy=True, growth=True, raw=False)
    A_NO_GROW, _ = arm_decl(kernel, mechs, port, origin_gate=allowlist, adequacy=True, growth=False, raw=False)
    C_FIAT, _ = arm_decl(kernel, mechs, port, origin_gate=tuple(TRUSTED), adequacy=False, growth=True, raw=False)
    C_FIAT_OVER, _ = arm_decl(kernel, mechs, port, origin_gate=tuple(TRUSTED) + ("O5",), adequacy=True, growth=True, raw=False)
    C_FROZEN, _ = arm_decl(kernel, mechs, port, origin_gate=None, adequacy=False, growth=False, raw=False)
    A_RAW, _ = arm_decl(kernel, mechs, port, origin_gate=None, adequacy=False, growth=False, raw=True)
    A_WITHHOLD, _ = arm_decl(kernel, mechs, port, origin_gate=tuple(), adequacy=True, growth=True, raw=False)
    B_SHIPPED = {fam: copy.deepcopy(mechs[fam]) for fam in FAM_IDS}
    B_ORACLE = arm_substitute_true(mechs)

    arms = {"T-SCORED-ADEQ": T, "A-NO-ADEQ": A_NO_ADEQ, "A-NO-PROV": A_NO_PROV,
            "A-NO-GROW": A_NO_GROW, "C-FIAT-ADEQ": C_FIAT, "C-FIAT-OVERTRUST": C_FIAT_OVER,
            "C-FROZEN-CERT": C_FROZEN, "A-RAW-DECL": A_RAW, "A-WITHHOLD-ALL": A_WITHHOLD,
            "B-SHIPPED": B_SHIPPED, "B-ORACLE": B_ORACLE}

    from spider.kernel import certify_declaration
    cert_admits_sound = [certify_declaration(DECL[f["fam"]], f["train"], [])[0]
                         for f in FAMILIES if f["role"] == "SOUND"]
    probeable = [f["fam"] for f in FAMILIES if f["role"] == "EVADER_P"]
    cert_refuses_probeable = [not certify_declaration(DECL[fam], FAM_BY_ID[fam]["train"],
                                                      mine_negatives_resource(FAM_BY_ID[fam]["resource"], DECL[fam], port)[0])[0]
                              for fam in probeable]

    results = {name: summarize(evaluate(arm, port)[0], WITHIN_ENVELOPE) for name, arm in arms.items()}
    boundary = {name: summarize(evaluate(arm, port)[0], BOUNDARY) for name, arm in arms.items()}
    refusal = refusal_violation_check(kernel, mechs, port)

    metrics = {
        "M-T-FALSE-ACCEPT-COUNT": results["T-SCORED-ADEQ"]["false_accept_count"],
        "M-T-HTTP-ON-OUT-COUNT": results["T-SCORED-ADEQ"]["http_on_out_count"],
        "M-T-REFUSAL-SEMANTICS-VIOLATIONS": results["T-SCORED-ADEQ"]["refusal_semantics_violations"],
        "M-T-COVERAGE": results["T-SCORED-ADEQ"]["coverage"],
        "M-T-COVERAGE-DELTA-VS-SHIPPED": results["T-SCORED-ADEQ"]["coverage"] - results["B-SHIPPED"]["coverage"],
        "M-T-BOUNDARY-FALSE-ACCEPT-COUNT": boundary["T-SCORED-ADEQ"]["false_accept_count"],
        "M-T-CERTIFIED-COUNT": sum(1 for f in FAM_IDS if cert_status(T[f]) == "CERTIFIED"),
        "M-T-PROV-REFUSED-COUNT": sum(1 for f in FAM_IDS if (T[f].verification_rule or {}).get("provenance_gate") == "REFUSED_ORIGIN"),
        "M-T-ADEQ-REFUSED-COUNT": sum(1 for f in FAM_IDS if (T[f].verification_rule or {}).get("adequacy_gate") == "REFUSED_INADEQUATE"),
        "M-B-SHIPPED-COVERAGE": results["B-SHIPPED"]["coverage"],
        "M-B-SHIPPED-FALSE-ACCEPT-COUNT": results["B-SHIPPED"]["false_accept_count"],
        "M-B-ORACLE-COVERAGE": results["B-ORACLE"]["coverage"],
        "M-B-ORACLE-FALSE-ACCEPT-COUNT": results["B-ORACLE"]["false_accept_count"],
        "M-A-NO-ADEQ-FALSE-ACCEPT-COUNT": results["A-NO-ADEQ"]["false_accept_count"],
        "M-A-NO-PROV-FALSE-ACCEPT-COUNT": results["A-NO-PROV"]["false_accept_count"],
        "M-A-NO-GROW-FALSE-ACCEPT-COUNT": results["A-NO-GROW"]["false_accept_count"],
        "M-C-FIAT-FALSE-ACCEPT-COUNT": results["C-FIAT-ADEQ"]["false_accept_count"],
        "M-C-FIAT-OVER-FALSE-ACCEPT-COUNT": results["C-FIAT-OVERTRUST"]["false_accept_count"],
        "M-C-FROZEN-FALSE-ACCEPT-COUNT": results["C-FROZEN-CERT"]["false_accept_count"],
        "M-A-RAW-FALSE-ACCEPT-COUNT": results["A-RAW-DECL"]["false_accept_count"],
        "M-A-WITHHOLD-FALSE-ACCEPT-COUNT": results["A-WITHHOLD-ALL"]["false_accept_count"],
        "M-A-WITHHOLD-COVERAGE": results["A-WITHHOLD-ALL"]["coverage"],
        "M-COVERAGE-IN-ITEMS": results["T-SCORED-ADEQ"]["total_in"],
        "M-CERT-ADMITS-SOUND-COUNT": sum(cert_admits_sound),
        "M-CERT-REFUSES-PROBEABLE-COUNT": sum(cert_refuses_probeable),
        "M-MECHANISM-COUNT": len(mechs),
        "M-REG-PROV-SCORES": {o: round(scores[o], 6) for o in CAL_ORIGINS},
        "M-INFERRED-ALLOWLIST": list(allowlist),
        "M-ADEQUACY-CLASSIFIED": {fam: adequacy[fam] for fam in FAM_IDS},
    }

    controls = {
        "PC-PROV-SCORE-SEPARATES": dict(
            expected="all trusted origins score 1.0, all untrusted score <= 0.25; inferred allowlist == O1..O4",
            observed=dict(scores={o: scores[o] for o in CAL_ORIGINS}, allowlist=list(allowlist)),
            pass_=(all(scores[o] >= 1.0 - COVERAGE_TOL for o in TRUSTED)
                   and all(scores[o] <= 0.25 + COVERAGE_TOL for o in ("O5", "O6"))
                   and set(allowlist) == set(TRUSTED))),
        "PC-PROV-ADMITS-TRUSTED": dict(
            expected="every trusted-origin bank family is admitted by the inferred allowlist (not PROV_REFUSED)",
            observed=[fam for fam in FAM_IDS if (T[fam].verification_rule or {}).get("provenance_gate") == "REFUSED_ORIGIN"],
            pass_=all((T[f["fam"]].verification_rule or {}).get("provenance_gate") != "REFUSED_ORIGIN"
                      for f in FAMILIES if f["origin"] in TRUSTED)),
        "PC-PROV-REFUSES-UNTRUSTED": dict(
            expected="B9 (untrusted O5) is withheld by the provenance gate and keeps the induced support",
            observed=dict(gate=(T["B9"].verification_rule or {}).get("provenance_gate"),
                          support=effective_support(T["B9"], T["B9"].parameter_slots[0]),
                          induced=induced["B9"]),
            pass_=((T["B9"].verification_rule or {}).get("provenance_gate") == "REFUSED_ORIGIN"
                   and effective_support(T["B9"], T["B9"].parameter_slots[0]) == induced["B9"])),
        "PC-PROV-REFUSES-SPARSE": dict(
            expected="certificate-with-growth WOULD certify B9 (probe misses the budget-sparse token) yet provenance withholds it; A-NO-PROV false-accepts it",
            observed=dict(cert_would_admit=(
                certify_declaration(DECL["B9"], FAM_BY_ID["B9"]["train"],
                                    mine_negatives_resource("sku", DECL["B9"], port)[0])[0]),
                a_no_prov_B9_fa=results["A-NO-PROV"]["per_family"]["B9"]["fa"]),
            pass_=(certify_declaration(DECL["B9"], FAM_BY_ID["B9"]["train"],
                                       mine_negatives_resource("sku", DECL["B9"], port)[0])[0]
                   and results["A-NO-PROV"]["per_family"]["B9"]["fa"] >= 1)),
        "PC-ADEQUACY-CLASSIFIES": dict(
            expected="detector output equals frozen EXPECTED_ADEQUACY for all 11 families",
            observed=adequacy, pass_=(adequacy == EXPECTED_ADEQUACY)),
        "PC-ADEQUACY-DETECTS-INADEQUATE": dict(
            expected="B7 and B8 flagged INADEQUATE",
            observed={f: adequacy[f] for f in ("B7", "B8")},
            pass_=(not adequacy["B7"] and not adequacy["B8"])),
        "PC-ADEQUACY-PASSES-ADEQUATE": dict(
            expected="B1-B6,B9,B10,B11 pass the adequacy detector",
            observed={f: adequacy[f] for f in FAM_IDS if f not in ("B7", "B8")},
            pass_=all(adequacy[f] for f in FAM_IDS if f not in ("B7", "B8"))),
        "PC-ADEQ-NEEDED": dict(
            expected="A-NO-ADEQ false-accepts >= 1 (B7/B8 admitted)",
            observed=metrics["M-A-NO-ADEQ-FALSE-ACCEPT-COUNT"],
            pass_=metrics["M-A-NO-ADEQ-FALSE-ACCEPT-COUNT"] >= 1),
        "PC-PROV-NEEDED": dict(
            expected="A-NO-PROV false-accepts >= 1 (B9 admitted)",
            observed=metrics["M-A-NO-PROV-FALSE-ACCEPT-COUNT"],
            pass_=metrics["M-A-NO-PROV-FALSE-ACCEPT-COUNT"] >= 1),
        "PC-GROW-NEEDED": dict(
            expected="A-NO-GROW false-accepts >= 1 (probeable evaders admitted)",
            observed=metrics["M-A-NO-GROW-FALSE-ACCEPT-COUNT"],
            pass_=metrics["M-A-NO-GROW-FALSE-ACCEPT-COUNT"] >= 1),
        "PC-CERT-ADMITS-SOUND": dict(
            expected="all 4 sound declarations CERTIFIED",
            observed="%d/4" % sum(cert_admits_sound), pass_=all(cert_admits_sound)),
        "PC-GROW-CATCHES-PROBEABLE": dict(
            expected="all 3 probeable evaders REFUSED after growth",
            observed="%d/3" % sum(cert_refuses_probeable), pass_=all(cert_refuses_probeable)),
        "PC-INGEST-REFUSED-ABSTAINS": dict(
            expected="real ingest_declaration refuses B5 and preserves support",
            observed=refusal, pass_=(refusal["refused"] and refusal["support_preserved"])),
        "PC-UNSAFE-RAW": dict(
            expected="A-RAW-DECL false-accepts > 0",
            observed=metrics["M-A-RAW-FALSE-ACCEPT-COUNT"],
            pass_=metrics["M-A-RAW-FALSE-ACCEPT-COUNT"] >= 1),
        "PC-DISCRIMINATION": dict(
            expected="T FA==0 while C-FIAT-ADEQ FA>0 at equal coverage",
            observed=dict(T=metrics["M-T-FALSE-ACCEPT-COUNT"], C_FA=metrics["M-C-FIAT-FALSE-ACCEPT-COUNT"],
                          T_cov=metrics["M-T-COVERAGE"], C_cov=results["C-FIAT-ADEQ"]["coverage"]),
            pass_=(metrics["M-T-FALSE-ACCEPT-COUNT"] == 0 and metrics["M-C-FIAT-FALSE-ACCEPT-COUNT"] >= 1
                   and abs(metrics["M-T-COVERAGE"] - results["C-FIAT-ADEQ"]["coverage"]) < COVERAGE_TOL)),
        "PC-MEASURED-TRUST-DOMINATES-OVERTRUST": dict(
            expected="a fiat allowlist that over-trusts O5 false-accepts B9 while the MEASURED trust root refuses it",
            observed=dict(C_over_fa=metrics["M-C-FIAT-OVER-FALSE-ACCEPT-COUNT"],
                          T_fa=metrics["M-T-FALSE-ACCEPT-COUNT"]),
            pass_=(metrics["M-C-FIAT-OVER-FALSE-ACCEPT-COUNT"] >= 1
                   and metrics["M-T-FALSE-ACCEPT-COUNT"] == 0)),
        "PC-GROW-MISSES-SPARSE": dict(
            expected="certificate-with-growth certifies B11 (trusted budget-sparse over-accept)",
            observed=dict(cert=certify_declaration(DECL["B11"], FAM_BY_ID["B11"]["train"],
                                                   mine_negatives_resource("wgt", DECL["B11"], port)[0])[0]),
            pass_=certify_declaration(DECL["B11"], FAM_BY_ID["B11"]["train"],
                                      mine_negatives_resource("wgt", DECL["B11"], port)[0])[0]),
        "BP-TRUSTED-SPARSE-FAILS": dict(
            expected="T boundary B11 false-accepts >= 1 (irreducible residual)",
            observed=metrics["M-T-BOUNDARY-FALSE-ACCEPT-COUNT"],
            pass_=metrics["M-T-BOUNDARY-FALSE-ACCEPT-COUNT"] >= 1),
        "NC-REJECT-ALL": dict(
            expected="A-WITHHOLD-ALL accepts no out-of-support value, coverage == B-SHIPPED",
            observed=dict(fa=metrics["M-A-WITHHOLD-FALSE-ACCEPT-COUNT"], cov=metrics["M-A-WITHHOLD-COVERAGE"]),
            pass_=(metrics["M-A-WITHHOLD-FALSE-ACCEPT-COUNT"] == 0
                   and abs(metrics["M-A-WITHHOLD-COVERAGE"] - metrics["M-B-SHIPPED-COVERAGE"]) < COVERAGE_TOL)),
    }

    validity = {
        "M-MECHANISM-COUNT-11": len(mechs) == 11,
        "M-SINGLE-SLOT": all(len(slots[fam]) == 1 for fam in FAM_IDS),
        "M-CONFIDENCE-0.9": all(abs(mechs[fam].confidence - 0.9) < 1e-9 for fam in FAM_IDS),
        "B-SHIPPED-FA0": metrics["M-B-SHIPPED-FALSE-ACCEPT-COUNT"] == 0,
        "B-ORACLE-CEILING": abs(metrics["M-B-ORACLE-COVERAGE"] - 1.0) < COVERAGE_TOL
                            and metrics["M-B-ORACLE-FALSE-ACCEPT-COUNT"] == 0,
        "T-REFUSAL-VIOL-0": metrics["M-T-REFUSAL-SEMANTICS-VIOLATIONS"] == 0,
        "M-SUPPORT-IDENTITY": induced == EXPECTED_INDUCED,
        "M-ADEQ-DETERMINISTIC": adequacy == EXPECTED_ADEQUACY,
        "M-SPARSE-TOKENS-MISSED": not ({"abcd", "abef", "beef"} & FIRST_BUDGET),
    }

    regression = run_regression()
    validity["M-REGRESSION"] = regression["ok"]
    metrics["M-REGRESSION-TESTS-RUN"] = regression["tests_run"]
    v8 = v8_binding()
    validity_gate = (all(validity.values()) and v8["status"] == "PASS")
    sensitivity_gate = all(controls[k]["pass_"] for k in
                           ["PC-CERT-ADMITS-SOUND", "PC-GROW-CATCHES-PROBEABLE", "PC-UNSAFE-RAW",
                            "PC-DISCRIMINATION", "PC-MEASURED-TRUST-DOMINATES-OVERTRUST",
                            "PC-INGEST-REFUSED-ABSTAINS"])
    provenance_gate = all(controls[k]["pass_"] for k in
                          ["PC-PROV-SCORE-SEPARATES", "PC-PROV-ADMITS-TRUSTED",
                           "PC-PROV-REFUSES-UNTRUSTED", "PC-PROV-REFUSES-SPARSE"])
    adequacy_gate = all(controls[k]["pass_"] for k in
                        ["PC-ADEQUACY-CLASSIFIES", "PC-ADEQUACY-DETECTS-INADEQUATE", "PC-ADEQUACY-PASSES-ADEQUATE"])
    growth_gate = all(controls[k]["pass_"] for k in ["PC-GROW-NEEDED", "PC-GROW-CATCHES-PROBEABLE"])
    necessity_gate = all(controls[k]["pass_"] for k in ["PC-ADEQ-NEEDED", "PC-PROV-NEEDED", "PC-GROW-NEEDED"])
    boundary_gate = controls["PC-GROW-MISSES-SPARSE"]["pass_"] and controls["BP-TRUSTED-SPARSE-FAILS"]["pass_"]

    if not (validity_gate and sensitivity_gate and provenance_gate and adequacy_gate
            and growth_gate and necessity_gate and boundary_gate):
        status, outcome, decision = "MEASUREMENT_INVALID", "NOT_APPLICABLE", "MEASUREMENT_INVALID"
    elif (metrics["M-T-FALSE-ACCEPT-COUNT"] > 0 or metrics["M-T-HTTP-ON-OUT-COUNT"] > 0
          or metrics["M-T-REFUSAL-SEMANTICS-VIOLATIONS"] > 0):
        status, outcome, decision = "COMPLETE", "FALSIFIES", "SCORED_ADEQ_CERT_UNSAFE"
    elif (metrics["M-T-COVERAGE"] > metrics["M-B-SHIPPED-COVERAGE"] + COVERAGE_TOL
          and metrics["M-T-COVERAGE"] >= MIN_COVERAGE_ANCHOR - COVERAGE_TOL):
        status, outcome, decision = "COMPLETE", "SUPPORTS", "SCORED_ADEQ_CERT_SAFE_AND_EXPANSIVE"
    else:
        status, outcome, decision = "COMPLETE", "MIXED", "SCORED_ADEQ_CERT_SAFE_BUT_NO_EXPANSION"

    return dict(
        schema_version=1, experiment_id=EXPERIMENT_ID, lane="product",
        status=status, outcome=outcome, decision=decision,
        metrics=metrics, controls={k: dict(v) for k, v in controls.items()},
        validity=validity,
        gates=dict(validity_gate=validity_gate, sensitivity_gate=sensitivity_gate,
                   provenance_gate=provenance_gate, adequacy_gate=adequacy_gate,
                   growth_gate=growth_gate, necessity_gate=necessity_gate, boundary_gate=boundary_gate, v8=v8),
        induced_supports=induced, slots=slots, arms=results, boundary=boundary,
        adequacy=adequacy,
        provenance=dict(scores={o: scores[o] for o in CAL_ORIGINS}, allowlist=list(allowlist)),
        cost=dict(first_budget_size=len(FIRST_BUDGET)),
    )


def main():
    probe = os.environ.get("EXP_PROBE_MODE") == "1"
    r1 = run_once(probe)
    r2 = run_once(probe)
    det_keys = [k for k in r1["metrics"] if "LATENCY" not in k and not k.endswith("MS")]
    deterministic = (json.dumps({k: r1["metrics"][k] for k in det_keys}, sort_keys=True)
                     == json.dumps({k: r2["metrics"][k] for k in det_keys}, sort_keys=True)
                     and json.dumps(r1["arms"], sort_keys=True, default=str) == json.dumps(r2["arms"], sort_keys=True, default=str)
                     and json.dumps(r1["boundary"], sort_keys=True, default=str) == json.dumps(r2["boundary"], sort_keys=True, default=str)
                     and json.dumps(r1["provenance"], sort_keys=True, default=str) == json.dumps(r2["provenance"], sort_keys=True, default=str))
    r1["determinism_repeat_identical"] = deterministic
    r1["controls"]["PC-DETERMINISM-REPEAT"] = dict(expected="two independent runs identical",
                                                   observed=deterministic, pass_=deterministic)
    if not deterministic:
        r1["status"], r1["outcome"], r1["decision"] = "MEASUREMENT_INVALID", "NOT_APPLICABLE", "MEASUREMENT_INVALID"
    print(json.dumps(r1, indent=2, default=str))


if __name__ == "__main__":
    main()
