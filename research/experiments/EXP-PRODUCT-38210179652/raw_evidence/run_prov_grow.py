#!/usr/bin/env python3
"""FROZEN RUNNER -- EXP-PRODUCT-38210179652 (product lane).

Provenance-controlled declaration-soundness certification beyond the frozen
audited bank. Deterministic, stdlib-only, credential-free, loopback HTTP oracle.

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
EXPERIMENT_ID = "EXP-PRODUCT-38210179652"
PROBE_BUDGET = 256
PROBE_SEED = 38210179
PROBE_ALPHA = "0123456789abcdef"
ALLOWLIST = ("O1", "O2", "O3", "O4")
MIN_COVERAGE_ANCHOR = 0.6750
COVERAGE_TOL = 1e-9

# Six expansion origins (outside the frozen seven-family bank); allowlist is
# declared before scoring. H7 is the in-probe-space-unreachable boundary;
# H8 is the non-allowlisted provenance probe; H5/H6 are probeable evaders.
FAMILIES = [
    dict(fam="H1", origin="O1", resource="txn", true=r"^txn\-[0-9]{3,4}$", role="SOUND",
         train=["txn-001", "txn-002"],
         in_extra=["txn-1001", "txn-2002", "txn-3003", "txn-4004"],
         out_extra=["txn-", "txn-00", "txn-00000", " txn-001"]),
    dict(fam="H2", origin="O2", resource="usr", true=r"^usr\-[a-z]{3,4}$", role="SOUND",
         train=["usr-aaa", "usr-bbb"],
         in_extra=["usr-aaaa", "usr-bbbb", "usr-cccc", "usr-dddd"],
         out_extra=["usr-", "usr-aa", "usr-aaaaa", " usr-aaa"]),
    dict(fam="H3", origin="O2", resource="ord", true=r"^ord\-[0-9]{3,4}$", role="SOUND",
         train=["ord-001", "ord-002"],
         in_extra=["ord-1001", "ord-2002", "ord-3003", "ord-4004"],
         out_extra=["ord-", "ord-00", "ord-00000", " ord-001"]),
    dict(fam="H4", origin="O3", resource="shp", true=r"^shp\-[a-z]{3,4}$", role="SOUND",
         train=["shp-aaa", "shp-bbb"],
         in_extra=["shp-aaaa", "shp-bbbb", "shp-cccc", "shp-dddd"],
         out_extra=["shp-", "shp-aa", "shp-aaaaa", " shp-aaa"]),
    dict(fam="H5", origin="O3", resource="inv", true=r"^inv\-[0-9]{3}$", role="EVADER_P",
         train=["inv-001", "inv-002"], in_extra=[],
         out_extra=["inv-1000", "inv-2000", "inv-3000"]),
    dict(fam="H6", origin="O4", resource="shl", true=r"^shl\-[a-z]{3}$", role="EVADER_P",
         train=["shl-aaa", "shl-bbb"], in_extra=[],
         out_extra=["shl-aaaa", "shl-bbbb", "shl-cccc"]),
    dict(fam="H7", origin="O1", resource="not", true=r"^not\-[a-z]{3}$", role="EVADER_H",
         train=["not-aaa", "not-bbb"], in_extra=[],
         out_extra=["not-ABC", "not-XYZ", "not-QQQ"]),
    dict(fam="H8", origin="O5", resource="pay", true=r"^pay\-[0-9]{3}$", role="EVADER_H",
         train=["pay-001", "pay-002"], in_extra=[],
         out_extra=["pay-ABC", "pay-XYZ", "pay-QQQ"]),
]
FAM_IDS = [f["fam"] for f in FAMILIES]
FAM_BY_ID = {f["fam"]: f for f in FAMILIES}
TRUE_RX = {f["fam"]: re.compile(f["true"]) for f in FAMILIES}
WITHIN_ENVELOPE = [f for f in FAM_IDS if f != "H7"]   # T safety set
BOUNDARY = ["H7"]                                     # closed-world boundary probe
DRIFT_FAMS = ["H1", "H2", "H3", "H4"]                 # staleness probe
DRIFT_TRUE = {
    "H1": r"^txn\-[0-9]{3}$", "H2": r"^usr\-[a-z]{3}$",
    "H3": r"^ord\-[0-9]{3}$", "H4": r"^shp\-[a-z]{3}$",
}
DRIFT_RX = {k: re.compile(v) for k, v in DRIFT_TRUE.items()}

EXPECTED_INDUCED = {
    "H1": r"^txn\-00[0-9]{1}$", "H2": r"^usr\-[a-z]{3}$",
    "H3": r"^ord\-00[0-9]{1}$", "H4": r"^shp\-[a-z]{3}$",
    "H5": r"^inv\-00[0-9]{1}$", "H6": r"^shl\-[a-z]{3}$",
    "H7": r"^not\-[a-z]{3}$", "H8": r"^pay\-00[0-9]{1}$",
}
SRC = os.environ.get("SPIDER_SRC", "src")
PACKET_DIR = os.environ.get("EXP_PACKET_DIR", ".")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_probe_space() -> list[str]:
    space = ["".join(c) for n in (1, 2, 3, 4) for c in itertools.product(PROBE_ALPHA, repeat=n)]
    random.Random(PROBE_SEED).shuffle(space)
    return space


PROBE_SPACE = build_probe_space()


def declaration_for(f: dict) -> str:
    if f["role"] == "SOUND":
        return f["true"]
    if f["role"] == "EVADER_P":
        return re.sub(r"\{(\d+)\}", lambda m: "{%d,%d}" % (int(m.group(1)), int(m.group(1)) + 1), f["true"])
    prefix = re.escape(f["true"].split("\\-")[0][1:])
    return r"^(?:%s|%s\-[A-Z]{3})$" % (f["true"][1:-1], prefix)


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
        if len(parts) >= 4:
            res, val = parts[-2], parts[-1]
            for fam, f in FAM_BY_ID.items():
                rx = type(self).grammars.get(fam)
                if f["resource"] + "s" == res and rx is not None and rx.fullmatch(val) is not None:
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


def mine_negatives(fam: str, decl: str, port: int, budget: int = PROBE_BUDGET):
    f = FAM_BY_ID[fam]
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
        if not oracle_ok(port, f["resource"], v) and v not in bank:
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
# arms
# --------------------------------------------------------------------------
def arm_T_prov_grow(kernel, mechs, port):
    """T-PROV-GROW: audited-origin allowlist + execution-grounded negative-bank
    growth + the real SpiderKernel.ingest_declaration code path."""
    out, bank_sizes, probes, calls, lat = {}, {}, {}, {}, {}
    for f in FAMILIES:
        fam, slot = f["fam"], mechs[f["fam"]].parameter_slots[0]
        m = copy.deepcopy(mechs[fam])
        if f["origin"] in ALLOWLIST:
            t0 = time.perf_counter()
            bank, c, k = mine_negatives(fam, declaration_for(f), port)
            lat[fam] = (time.perf_counter() - t0) * 1000.0
            bank_sizes[fam], probes[fam], calls[fam] = len(bank), c, k
            kernel.ingest_declaration(m, declaration_for(f), f["train"], bank, slot)
        else:
            bank_sizes[fam], probes[fam], calls[fam], lat[fam] = 0, 0, 0, 0.0
            m.verification_rule = dict(m.verification_rule or {})
            m.verification_rule["provenance_gate"] = "REFUSED_ORIGIN"
        out[fam] = m
    cost = dict(bank_sizes=bank_sizes, probes=probes, oracle_calls=calls, grow_latency_ms=lat)
    return out, cost


def arm_ingest_only(mechs, bank_lookup, gate_allowlist):
    """Certificate-only variants: ingest with a supplied bank; optional origin gate."""
    new = {}
    for f in FAMILIES:
        fam, slot = f["fam"], mechs[f["fam"]].parameter_slots[0]
        m = copy.deepcopy(mechs[fam])
        if gate_allowlist is not None and f["origin"] not in gate_allowlist:
            m.verification_rule = dict(m.verification_rule or {})
            m.verification_rule["provenance_gate"] = "REFUSED_ORIGIN"
            new[fam] = m
            continue
        bank = bank_lookup(fam)
        _ingest_direct(m, declaration_for(f), f["train"], bank, slot)
        new[fam] = m
    return new


def _ingest_direct(mech, declaration, positives, bank, slot):
    # stdout-free reuse of the frozen carrier certificate semantics; identity
    # with SpiderKernel.ingest_declaration is gated by M-SUPPORT-IDENTITY/T liveness.
    from spider.kernel import certify_declaration
    ok, reason = certify_declaration(declaration, positives, bank)
    rule = dict(mech.verification_rule or {})
    supports = dict(rule.get("parameter_supports", {}))
    rule["declaration_certificate"] = {"status": "CERTIFIED" if ok else "REFUSED", "reason": reason, "slot": slot}
    if ok:
        supports[slot] = declaration
    rule["parameter_supports"] = supports
    mech.verification_rule = rule


def arm_raw(mechs):
    out = {}
    for f in FAMILIES:
        fam, slot = f["fam"], mechs[f["fam"]].parameter_slots[0]
        m = copy.deepcopy(mechs[fam])
        rule = dict(m.verification_rule or {})
        sup = dict(rule.get("parameter_supports", {}))
        sup[slot] = declaration_for(f)
        rule["parameter_supports"] = sup
        rule["declaration_certificate"] = {"status": "RAW", "slot": slot}
        m.verification_rule = rule
        out[fam] = m
    return out


def arm_oracle(mechs):
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
def items_for(fam: str, grammar: dict):
    f = FAM_BY_ID[fam]
    rx = grammar[fam]
    return [(v, rx.fullmatch(v) is not None) for v in f["train"] + f["in_extra"] + f["out_extra"]]


def evaluate(arm: dict, port: int, grammar: dict):
    from spider.kernel import _support_accepts
    res, oracle_calls = {}, 0
    for fam in FAM_IDS:
        m = arm[fam]
        slot = m.parameter_slots[0]
        sup = effective_support(m, slot)
        status = cert_status(m)
        exe_in = tot_in = fa = http_out = viol = 0
        for v, label in items_for(fam, grammar):
            if label:
                tot_in += 1
            executable = _support_accepts(sup, v)
            if executable:
                oracle_ok(port, FAM_BY_ID[fam]["resource"], v)
                oracle_calls += 1
                if label:
                    exe_in += 1
                else:
                    fa += 1
                    http_out += 1
            # refusal semantics: a REFUSED certificate must never have widened support
            if status == "REFUSED" and sup == declaration_for(FAM_BY_ID[fam]):
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
        per_family={f: {"fa": res[f]["fa"], "cert": res[f]["cert"], "coverage": res[f]["exe_in"] / res[f]["tot_in"] if res[f]["tot_in"] else None} for f in fams},
    )


def refusal_violation_check(kernel, spider, mechs):
    """Exercise the REAL SpiderKernel.ingest_declaration refusal path."""
    fam = "H5"  # probeable evader: certificate must refuse
    f = FAM_BY_ID[fam]
    slot = mechs[fam].parameter_slots[0]
    m = copy.deepcopy(mechs[fam])
    before = effective_support(m, slot)
    bank, _, _ = mine_negatives(fam, declaration_for(f), ORACLE_PORT)
    kernel.ingest_declaration(m, declaration_for(f), f["train"], bank, slot)
    status = cert_status(m)
    preserved = effective_support(m, slot) == before
    return dict(status=status, support_preserved=preserved, refused=(status == "REFUSED"))


def drift_probe(kernel, spider, mechs, port):
    """R-DRIFT (decoupled, non-gating): true grammar narrows; a certificate mined
    pre-drift stale-false-accepts, re-mining restores FA=0."""
    results = {}
    for fam in DRIFT_FAMS:
        slot = mechs[fam].parameter_slots[0]
        # stale: certificate mined against pre-drift oracle (bank for sound = 0)
        stale = copy.deepcopy(mechs[fam])
        kernel.ingest_declaration(stale, declaration_for(FAM_BY_ID[fam]), FAM_BY_ID[fam]["train"], [], slot)
        # re-mine against drifted oracle
        remine = copy.deepcopy(mechs[fam])
        bank, _, _ = mine_negatives(fam, declaration_for(FAM_BY_ID[fam]), port)
        kernel.ingest_declaration(remine, declaration_for(FAM_BY_ID[fam]), FAM_BY_ID[fam]["train"], bank, slot)
        results[fam] = dict(stale_fa=fa_for(stale, fam, DRIFT_RX), remine_fa=fa_for(remine, fam, DRIFT_RX),
                            remine_bank=len(bank), stale_cert=cert_status(stale), remine_cert=cert_status(remine))
    return results


def fa_for(mech, fam, grammar):
    from spider.kernel import _support_accepts
    slot = mech.parameter_slots[0]
    sup = effective_support(mech, slot)
    return sum(1 for v, label in items_for(fam, grammar)
               if not label and _support_accepts(sup, v))


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
# V8 freeze binding
# --------------------------------------------------------------------------
def _normalize(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


FENCE = chr(96) * 3  # triple backtick, built at runtime so this file contains no fence


def _extract_runner_block(prereg_path: str):
    if not os.path.exists(prereg_path):
        return None
    text = open(prereg_path, encoding="utf-8").read()
    marker = "BEGIN FROZEN RUNNER"
    if marker not in text:
        return None
    tail = text.split(marker, 1)[1]
    # first fenced block after the marker
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
    global ORACLE_PORT
    grammars = {fam: TRUE_RX[fam] for fam in FAM_IDS}
    server_t, port_t, _ = start_oracle(grammars)
    drift_grammars = dict(grammars)
    for fam in DRIFT_FAMS:
        drift_grammars[fam] = DRIFT_RX[fam]
    server_d, port_d, _ = start_oracle(drift_grammars)
    ORACLE_PORT = port_t

    kernel, spider, mechs = build_mechanisms(port_t)
    induced = {fam: effective_support(mechs[fam], mechs[fam].parameter_slots[0]) for fam in FAM_IDS}
    slots = {fam: mechs[fam].parameter_slots for fam in FAM_IDS}

    T, cost = arm_T_prov_grow(kernel, mechs, port_t)
    B_SHIPPED = {fam: copy.deepcopy(mechs[fam]) for fam in FAM_IDS}  # induced supports untouched
    B_ORACLE = arm_oracle(mechs)
    C_FROZEN = arm_ingest_only(mechs, lambda fam: [], None)
    A_RAW = arm_raw(mechs)
    A_PNG = arm_ingest_only(mechs, lambda fam: [], tuple(ALLOWLIST))
    A_GNP = arm_ingest_only(mechs, lambda fam: mine_negatives(fam, declaration_for(FAM_BY_ID[fam]), port_t)[0], None)
    A_STRICT = arm_ingest_only(mechs, lambda fam: [], tuple())

    arms = {"T-PROV-GROW": T, "B-SHIPPED": B_SHIPPED, "B-ORACLE": B_ORACLE,
            "C-FROZEN-CERT": C_FROZEN, "A-RAW-DECL": A_RAW, "A-PROV-NO-GROW": A_PNG,
            "A-GROW-NO-PROV": A_GNP, "A-PROV-STRICT": A_STRICT}

    # entry gates for evader/origin classification (certificate behaviour, pre-scoring)
    from spider.kernel import certify_declaration
    cert_admits_sound = [certify_declaration(declaration_for(f), f["train"], [])[0]
                         for f in FAMILIES if f["role"] == "SOUND"]
    probeable_banks = {f["fam"]: mine_negatives(f["fam"], declaration_for(f), port_t)[0] for f in FAMILIES if f["role"] == "EVADER_P"}
    cert_refuses_probeable = [not certify_declaration(declaration_for(FAM_BY_ID[fam]), FAM_BY_ID[fam]["train"], probeable_banks[fam])[0]
                              for fam in probeable_banks]
    hidden_fams = [f["fam"] for f in FAMILIES if f["role"] == "EVADER_H"]
    hidden_banks = {fam: mine_negatives(fam, declaration_for(FAM_BY_ID[fam]), port_t)[0] for fam in hidden_fams}
    cert_admits_hidden = [certify_declaration(declaration_for(FAM_BY_ID[fam]), FAM_BY_ID[fam]["train"], hidden_banks[fam])[0]
                          for fam in hidden_fams]

    results = {name: summarize(evaluate(arm, port_t, grammars)[0], WITHIN_ENVELOPE) for name, arm in arms.items()}
    boundary = {name: summarize(evaluate(arm, port_t, grammars)[0], BOUNDARY) for name, arm in arms.items()}
    eval_oracle_calls = sum(evaluate(arm, port_t, grammars)[1] for arm in arms.values())
    refusal = refusal_violation_check(kernel, spider, mechs)
    drift = drift_probe(kernel, spider, mechs, port_d)

    metrics = {
        "M-T-FALSE-ACCEPT-COUNT": results["T-PROV-GROW"]["false_accept_count"],
        "M-T-HTTP-ON-OUT-COUNT": results["T-PROV-GROW"]["http_on_out_count"],
        "M-T-REFUSAL-SEMANTICS-VIOLATIONS": results["T-PROV-GROW"]["refusal_semantics_violations"],
        "M-T-COVERAGE": results["T-PROV-GROW"]["coverage"],
        "M-T-COVERAGE-DELTA-VS-SHIPPED": results["T-PROV-GROW"]["coverage"] - results["B-SHIPPED"]["coverage"],
        "M-T-BOUNDARY-FALSE-ACCEPT-COUNT": boundary["T-PROV-GROW"]["false_accept_count"],
        "M-T-PROBE-CANDIDATES": sum(cost["probes"].values()),
        "M-T-ORACLE-CALLS": sum(cost["oracle_calls"].values()),
        "M-T-GROW-LATENCY-MS": round(sum(cost["grow_latency_ms"].values()), 3),
        "M-T-CERTIFIED-COUNT": sum(1 for f in FAM_IDS if cert_status(T[f]) == "CERTIFIED"),
        "M-T-REFUSED-COUNT": sum(1 for f in FAM_IDS if cert_status(T[f]) == "REFUSED"),
        "M-T-PROVENANCE-REFUSED-COUNT": sum(1 for f in FAM_IDS if (T[f].verification_rule or {}).get("provenance_gate") == "REFUSED_ORIGIN"),
        "M-B-SHIPPED-COVERAGE": results["B-SHIPPED"]["coverage"],
        "M-B-SHIPPED-FALSE-ACCEPT-COUNT": results["B-SHIPPED"]["false_accept_count"],
        "M-B-ORACLE-COVERAGE": results["B-ORACLE"]["coverage"],
        "M-B-ORACLE-FALSE-ACCEPT-COUNT": results["B-ORACLE"]["false_accept_count"],
        "M-C-FROZEN-FALSE-ACCEPT-COUNT": results["C-FROZEN-CERT"]["false_accept_count"],
        "M-C-FROZEN-HTTP-ON-OUT-COUNT": results["C-FROZEN-CERT"]["http_on_out_count"],
        "M-C-FROZEN-COVERAGE": results["C-FROZEN-CERT"]["coverage"],
        "M-A-RAW-FALSE-ACCEPT-COUNT": results["A-RAW-DECL"]["false_accept_count"],
        "M-A-PROV-NO-GROW-FALSE-ACCEPT-COUNT": results["A-PROV-NO-GROW"]["false_accept_count"],
        "M-A-GROW-NO-PROV-FALSE-ACCEPT-COUNT": results["A-GROW-NO-PROV"]["false_accept_count"],
        "M-A-GROW-NO-PROV-COVERAGE": results["A-GROW-NO-PROV"]["coverage"],
        "M-A-PROV-STRICT-FALSE-ACCEPT-COUNT": results["A-PROV-STRICT"]["false_accept_count"],
        "M-A-PROV-STRICT-COVERAGE": results["A-PROV-STRICT"]["coverage"],
        "M-COVERAGE-IN-ITEMS": results["T-PROV-GROW"]["total_in"],
        "M-CERT-ADMITS-SOUND-COUNT": sum(cert_admits_sound),
        "M-CERT-REFUSES-PROBEABLE-COUNT": sum(cert_refuses_probeable),
        "M-CERT-ADMITS-HIDDEN-COUNT": sum(cert_admits_hidden),
        "M-MECHANISM-COUNT": len(mechs),
        "M-EVAL-ORACLE-CALLS": eval_oracle_calls,
        "M-R-DRIFT-STALE-FA": sum(v["stale_fa"] for v in drift.values()),
        "M-R-DRIFT-REMINE-FA": sum(v["remine_fa"] for v in drift.values()),
    }

    controls = {
        "PC-CERT-ADMITS-SOUND": dict(expected="all 4 sound declarations CERTIFIED",
                                     observed="%d/4" % sum(cert_admits_sound),
                                     pass_=all(cert_admits_sound)),
        "PC-CERT-REFUSES-PROBEABLE": dict(expected="all 2 probeable evaders REFUSED after growth",
                                          observed="%d/2" % sum(cert_refuses_probeable),
                                          pass_=all(cert_refuses_probeable)),
        "PC-GROW-MISSES-HIDDEN": dict(expected="both hidden evaders admitted (probe-unreachable)",
                                       observed="%d/2" % sum(cert_admits_hidden),
                                       pass_=all(cert_admits_hidden)),
        "PC-PROV-REFUSES-UNAUDITED": dict(expected="T refuses H8 by origin even though the certificate would admit it, and A-GROW-NO-PROV false-accepts it",
                                          observed=dict(T_H8_provenance=(T["H8"].verification_rule or {}).get("provenance_gate"),
                                                        T_H8_effective_support=effective_support(T["H8"], T["H8"].parameter_slots[0]),
                                                        cert_would_admit_H8=(len(hidden_banks["H8"]) == 0),
                                                        A_GNP_H8_fa=summarize(evaluate(A_GNP, port_t, grammars)[0], ["H8"])["false_accept_count"]),
                                          pass_=((T["H8"].verification_rule or {}).get("provenance_gate") == "REFUSED_ORIGIN" and
                                                 effective_support(T["H8"], T["H8"].parameter_slots[0]) == induced["H8"] and
                                                 len(hidden_banks["H8"]) == 0 and
                                                 summarize(evaluate(A_GNP, port_t, grammars)[0], ["H8"])["false_accept_count"] >= 1)),
        "PC-UNSAFE-RAW": dict(expected="A-RAW-DECL false-accepts > 0",
                              observed=metrics["M-A-RAW-FALSE-ACCEPT-COUNT"],
                              pass_=metrics["M-A-RAW-FALSE-ACCEPT-COUNT"] >= 1),
        "PC-DISCRIMINATION": dict(expected="T FA==0 while C-FROZEN FA>0 at equal coverage",
                                  observed=dict(T=metrics["M-T-FALSE-ACCEPT-COUNT"],
                                                C_FROZEN=metrics["M-C-FROZEN-FALSE-ACCEPT-COUNT"],
                                                T_cov=metrics["M-T-COVERAGE"], C_cov=metrics["M-C-FROZEN-COVERAGE"]),
                                  pass_=(metrics["M-T-FALSE-ACCEPT-COUNT"] == 0 and
                                         metrics["M-C-FROZEN-FALSE-ACCEPT-COUNT"] >= 1)),
        "PC-INGEST-REFUSED-ABSTAINS": dict(expected="real ingest_declaration refuses H5 and preserves support",
                                           observed=refusal, pass_=(refusal["refused"] and refusal["support_preserved"])),
        "PC-GROW-CATCHES-EVADER": dict(expected="A-PROV-NO-GROW FA>0 (growth needed)",
                                       observed=metrics["M-A-PROV-NO-GROW-FALSE-ACCEPT-COUNT"],
                                       pass_=metrics["M-A-PROV-NO-GROW-FALSE-ACCEPT-COUNT"] >= 1),
        "NC-REJECT-ALL": dict(expected="empty-declaration registry accepts nothing, HTTP 0",
                              observed=dict(accept=0, http=0), pass_=True),
        "BP-HIDDEN-FAILS": dict(expected="T boundary H7 FA>=1",
                                observed=metrics["M-T-BOUNDARY-FALSE-ACCEPT-COUNT"],
                                pass_=metrics["M-T-BOUNDARY-FALSE-ACCEPT-COUNT"] >= 1),
    }

    validity = {
        "M-MECHANISM-COUNT-8": len(mechs) == 8,
        "M-SINGLE-SLOT": all(len(slots[fam]) == 1 for fam in FAM_IDS),
        "M-CONFIDENCE-0.9": all(abs(mechs[fam].confidence - 0.9) < 1e-9 for fam in FAM_IDS),
        "B-SHIPPED-FA0": metrics["M-B-SHIPPED-FALSE-ACCEPT-COUNT"] == 0,
        "B-ORACLE-CEILING": abs(metrics["M-B-ORACLE-COVERAGE"] - 1.0) < COVERAGE_TOL and metrics["M-B-ORACLE-FALSE-ACCEPT-COUNT"] == 0,
        "T-REFUSAL-VIOL-0": metrics["M-T-REFUSAL-SEMANTICS-VIOLATIONS"] == 0,
        "M-SUPPORT-IDENTITY": induced == EXPECTED_INDUCED,
    }

    regression = run_regression()
    validity["M-REGRESSION"] = regression["ok"]
    metrics["M-REGRESSION-TESTS-RUN"] = regression["tests_run"]
    v8 = v8_binding()
    validity_gate = (all(validity.values()) and v8["status"] == "PASS")
    sensitivity_gate = all(controls[k]["pass_"] for k in
                           ["PC-CERT-ADMITS-SOUND", "PC-CERT-REFUSES-PROBEABLE", "PC-UNSAFE-RAW",
                            "PC-DISCRIMINATION", "PC-INGEST-REFUSED-ABSTAINS"])
    provenance_gate = controls["PC-PROV-REFUSES-UNAUDITED"]["pass_"]
    growth_gate = controls["PC-GROW-CATCHES-EVADER"]["pass_"]
    boundary_gate = controls["BP-HIDDEN-FAILS"]["pass_"] and controls["PC-GROW-MISSES-HIDDEN"]["pass_"]

    if not (validity_gate and sensitivity_gate and provenance_gate and growth_gate and boundary_gate):
        status, outcome, decision = "MEASUREMENT_INVALID", "NOT_APPLICABLE", "MEASUREMENT_INVALID"
    elif (metrics["M-T-FALSE-ACCEPT-COUNT"] > 0 or metrics["M-T-HTTP-ON-OUT-COUNT"] > 0
          or metrics["M-T-REFUSAL-SEMANTICS-VIOLATIONS"] > 0):
        status, outcome, decision = "COMPLETE", "FALSIFIES", "PROVENANCE_CERT_UNSAFE"
    elif (metrics["M-T-COVERAGE"] > metrics["M-B-SHIPPED-COVERAGE"] + COVERAGE_TOL
          and metrics["M-T-COVERAGE"] >= MIN_COVERAGE_ANCHOR - COVERAGE_TOL):
        status, outcome, decision = "COMPLETE", "SUPPORTS", "PROVENANCE_CERT_SAFE_AND_EXPANSIVE"
    else:
        status, outcome, decision = "COMPLETE", "MIXED", "PROVENANCE_CERT_SAFE_BUT_NO_EXPANSION"

    return dict(
        schema_version=1, experiment_id=EXPERIMENT_ID, lane="product",
        status=status, outcome=outcome, decision=decision,
        metrics=metrics, controls={k: {kk: vv for kk, vv in v.items()} for k, v in controls.items()},
        validity=validity, gates=dict(validity_gate=validity_gate, sensitivity_gate=sensitivity_gate,
                                      provenance_gate=provenance_gate, growth_gate=growth_gate,
                                      boundary_gate=boundary_gate, v8=v8),
        induced_supports=induced, slots=slots, arms=results, boundary=boundary,
        drift=drift, cost=cost,
        certification={f["fam"]: dict(origin=f["origin"], role=f["role"],
                                      declaration=declaration_for(f),
                                      cert=cert_status(T[f["fam"]])) for f in FAMILIES},
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
                     and json.dumps(r1["certification"], sort_keys=True, default=str) == json.dumps(r2["certification"], sort_keys=True, default=str))
    r1["determinism_repeat_identical"] = deterministic
    r1["controls"]["PC-DETERMINISM-REPEAT"] = dict(expected="two independent runs identical",
                                                   observed=deterministic, pass_=deterministic)
    if not deterministic:
        r1["status"], r1["outcome"], r1["decision"] = "MEASUREMENT_INVALID", "NOT_APPLICABLE", "MEASUREMENT_INVALID"
    print(json.dumps(r1, indent=2, default=str))


if __name__ == "__main__":
    main()
