#!/usr/bin/env python3
"""EXECUTE runner for EXP-GRAPH-37950584469 (graph lane).

Runs the frozen two-path extraction-validity experiment over a credential-free,
server-rendered anchor set with a fail-closed pre-confirmatory substrate
certificate (GATE C), instrument checks (GATE E), anchor verdicts (D1/D2/D3) and
the conditional part-(ii) value-only-rotation blindness read (GATE B).

RAW EVIDENCE is written under research/experiments/EXP-GRAPH-37950584469/raw/.
DERIVED MEASUREMENTS are computed here and emitted into result.json.
Interpretation lives only in report.md.

Stdlib only (urllib, http.cookiejar, html.parser, re, ast, hashlib, json, random,
statistics).  No browser, no JS, no credentials, no write verbs.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import platform
import random
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.cookiejar import CookieJar
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fixtures  # noqa: E402
import neutral_detector  # noqa: E402
import path_a_htmlparser as path_a  # noqa: E402
import path_b_regexlex as path_b  # noqa: E402

EXP_ID = "EXP-GRAPH-37950584469"
LANE = "graph"
RUN_ID = os.environ.get("GITHUB_RUN_ID", "37950584469")
SEED = 36314193643

ROOT = Path(__file__).resolve().parents[4]  # repo root
EXP_DIR = ROOT / "research" / "experiments" / EXP_ID
RAW_DIR = EXP_DIR / "raw"
BODY_DIR = RAW_DIR / "bodies"
DERIVED_DIR = EXP_DIR / "derived"

USER_AGENT = f"SPIDER-Research/2.0 (graph-lane; experiment {EXP_ID}; +https://spider-research.dev)"
PACING_SECONDS = 2.0
REQUEST_CAP = 200
FROZEN_SEED = 36314193643

POSITIVE_ANCHORS = [
    ("CAL-POS-1", "https://gitlab.com/-/trial_registrations/new/"),
    ("CAL-POS-2", "https://auth.wikimedia.org/enwiki/w/index.php?title=Special:CreateAccount"),
    ("CAL-POS-3", "https://en.wikipedia.org/w/index.php?title=Special:UserLogin&action=form"),
    ("CAL-POS-4", "https://meta.discourse.org/"),
]
NEGATIVE_ANCHORS = [
    ("CAL-NEG-1", "https://www.iana.org/domains/reserved"),
    ("CAL-NEG-2", "https://cdn.jsdelivr.net/gh/python/cpython@v3.12.0/README.rst"),
    ("CAL-NEG-3", "https://www.debian.org/"),
    ("CAL-NEG-4", "https://httpbin.org/forms/post"),
]
SESSIONS = ["S1", "S2", "S3", "S4"]
TRANSPORT_HEADERS = ["ETag", "Last-Modified", "Cache-Control", "Vary"]

FROZEN_FILES = ["request.json", "spec.json", "prereg.md"]
FREEZE = json.loads((EXP_DIR / "freeze.json").read_text())


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def verify_frozen_inputs(tag: str):
    results = {}
    ok = True
    for name in FROZEN_FILES:
        actual = sha256_file(EXP_DIR / name)
        expected = FREEZE["hashes"][name]
        match = actual == expected
        ok = ok and match
        results[name] = {"expected": expected, "actual": actual, "match": match, "when": tag}
    return ok, results


# --------------------------------------------------------------------------
# capture
# --------------------------------------------------------------------------
class Recorder:
    def __init__(self):
        self.records = []
        self.host_last_request = {}
        self.request_count = 0

    def _pace(self, host: str):
        last = self.host_last_request.get(host)
        if last is not None:
            wait = PACING_SECONDS - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
        self.host_last_request[host] = time.time()

    def capture(self, anchor_id, url, session, jar, phase="fresh", warm_index=None, attempt=1):
        host = urllib.request.urlparse(url).hostname
        self._pace(host)
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "close",
        }
        jar_was_empty = len(list(jar)) == 0
        requested_at = datetime.now(timezone.utc).isoformat()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        req = urllib.request.Request(url, headers=headers, method="GET")
        self.request_count += 1
        status = None
        body = b""
        final_url = url
        resp_headers = {}
        error = None
        t0 = time.time()
        try:
            with opener.open(req, timeout=30) as resp:
                status = resp.status
                final_url = resp.geturl()
                body = resp.read()
                resp_headers = {k: v for k, v in resp.headers.items()}
        except urllib.error.HTTPError as exc:
            status = exc.code
            final_url = exc.geturl()
            try:
                body = exc.read()
            except Exception:
                body = b""
            resp_headers = {k: v for k, v in exc.headers.items()} if exc.headers else {}
            error = f"HTTPError:{exc.code}"
        except Exception as exc:  # noqa: BLE001
            error = f"{type(exc).__name__}:{exc}"

        elapsed = time.time() - t0
        body_sha = sha256_bytes(body) if body else None
        jar_digest = _jar_digest(jar)
        neutral_names = neutral_detector.find_in_list_names(body) if body else []
        headers_of_interest = {
            k: resp_headers.get(k)
            for k in TRANSPORT_HEADERS + ["Content-Type", "Content-Length", "Server"]
        }
        headers_of_interest["Set-Cookie-Count"] = sum(
            1 for k in resp_headers if k.lower() == "set-cookie"
        )
        cookies_after = sorted(
            [[c.domain, c.path, c.name, c.value] for c in jar]
        )
        record = {
            "anchor_id": anchor_id,
            "url": url,
            "session": session,
            "phase": phase,
            "warm_index": warm_index,
            "attempt": attempt,
            "requested_at_utc": requested_at,
            "final_url": final_url,
            "status": status,
            "error": error,
            "elapsed_s": round(elapsed, 3),
            "headers": headers_of_interest,
            "body_sha256": body_sha,
            "body_len": len(body),
            "body_path": None,
            "neutral_in_list_names": neutral_names,
            "jar_was_empty_before_request": jar_was_empty,
            "request_count": self.request_count,
            "cookie_jar_digest": jar_digest,
            "cookies_after": cookies_after,
        }
        self.records.append(record)
        return record, body


def _jar_digest(jar: CookieJar) -> str:
    items = sorted([[c.domain, c.path, c.name, c.value] for c in jar])
    return sha256_bytes(json.dumps(items, separators=(",", ":")).encode("utf-8"))


urllib.request.urlparse = __import__("urllib.parse", fromlist=["urlparse"]).urlparse  # type: ignore


def _jar_pairs(jar: CookieJar):
    return {(c.name, c.value) for c in jar}


# --------------------------------------------------------------------------
# extraction-path independence attestation
# --------------------------------------------------------------------------
def path_independence_attestation():
    src_a = (Path(__file__).resolve().parent / "path_a_htmlparser.py").read_text()
    src_b = (Path(__file__).resolve().parent / "path_b_regexlex.py").read_text()
    tree_b = ast.parse(src_b)
    imports_b = []
    for node in ast.walk(tree_b):
        if isinstance(node, ast.Import):
            imports_b.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports_b.append(node.module or "")
    forbidden = {m for m in imports_b if "path_a" in m or "html" in m}
    # literal host / anchor special-casing check (V07)
    anchor_tokens = [
        "gitlab", "wikimedia", "wikipedia", "discourse", "iana", "jsdelivr",
        "debian", "httpbin", "CAL-POS", "CAL-NEG",
    ]
    src_neutral = (Path(__file__).resolve().parent / "neutral_detector.py").read_text()
    hosts_found = sorted({t for t in anchor_tokens if t in src_a or t in src_b or t in src_neutral})
    # perturbation invariance
    original = fixtures.SYN_CANARY_BOTH
    def agree(body):
        return _pair_set(path_a.extract(body)) == _pair_set(path_b.extract(body))
    perturbed = bytearray(original)
    # one-character mutation inside an attribute value, not in tag structure
    idx = original.index(b"fixture-canary-value-7f3a")
    perturbed[idx] = ord("F") if perturbed[idx] != ord("F") else ord("f")
    perturbation_invariant = agree(original) == agree(bytes(perturbed))
    return {
        "path_a_sha256": sha256_bytes(src_a.encode()),
        "path_b_sha256": sha256_bytes(src_b.encode()),
        "source_hashes_differ": sha256_bytes(src_a.encode()) != sha256_bytes(src_b.encode()),
        "path_b_imports": sorted(imports_b),
        "path_b_forbidden_imports": sorted(forbidden),
        "path_b_imports_path_a_or_html": len(forbidden) > 0,
        "anchor_host_tokens_found_in_producer_sources": hosts_found,
        "no_anchor_special_casing": len(hosts_found) == 0,
        "perturbation_invariant": perturbation_invariant,
        "path_independence_pass": (
            sha256_bytes(src_a.encode()) != sha256_bytes(src_b.encode())
            and len(forbidden) == 0
            and len(hosts_found) == 0
            and perturbation_invariant
        ),
    }


# --------------------------------------------------------------------------
# fixtures
# --------------------------------------------------------------------------
def _pair_set(records):
    return {(r["field_name"], r["value"]) for r in records if r["state"] == "VALUE"}


def _field_states(records):
    return sorted({(r["field_name"], r["state"]) for r in records})


def run_fixtures():
    a_canary = path_a.extract(fixtures.SYN_CANARY_BOTH)
    b_canary = path_b.extract(fixtures.SYN_CANARY_BOTH)
    expected = {("authenticity_token", "fixture-canary-value-7f3a"),
                ("csrf-token", "fixture-meta-canary-91bd")}
    canary_pass = _pair_set(a_canary) == expected and _pair_set(b_canary) == expected

    a_empty = path_a.extract(fixtures.SYN_EMPTY_VALUE)
    b_empty = path_b.extract(fixtures.SYN_EMPTY_VALUE)
    a_states = _field_states(a_empty)
    b_states = _field_states(b_empty)
    empty_agree = (
        a_states == b_states
        and a_states == [("authenticity_token", "PRESENT_EMPTY"), ("csrf-token", "PRESENT_EMPTY")]
    )

    a_js = path_a.extract(fixtures.SYN_JSSTRING)
    b_js = path_b.extract(fixtures.SYN_JSSTRING)
    js_values = len(_pair_set(a_js)) + len(_pair_set(b_js))

    return {
        "canary_a_pairs": sorted(_pair_set(a_canary)),
        "canary_b_pairs": sorted(_pair_set(b_canary)),
        "M_FIXTURE_CANARY_PASS": canary_pass,
        "empty_a_states": a_states,
        "empty_b_states": b_states,
        "M_FIXTURE_EMPTY_AGREE": empty_agree,
        "M_FIXTURE_JSSTRING_VALUES": js_values,
        "js_a_values": sorted(_pair_set(a_js)),
        "js_b_values": sorted(_pair_set(b_js)),
    }


# --------------------------------------------------------------------------
# extraction aggregation
# --------------------------------------------------------------------------
def index_by_field(records):
    out: dict[str, list] = {}
    for r in records:
        out.setdefault(r["field_name"], []).append(r)
    return out


def path_metrics(anchor, per_session_records, headers_by_session, body_shas):
    """per_session_records: {session: [agsi,...]}; returns per-path metrics."""
    idx = {s: index_by_field(recs) for s, recs in per_session_records.items()}
    all_values = set()
    extracted_sessions = 0
    for s, recs in per_session_records.items():
        vals = {r["value"] for r in recs if r["state"] == "VALUE"}
        if vals:
            extracted_sessions += 1
        all_values |= vals
    route_ok = sum(1 for s in SESSIONS if headers_by_session.get(s, {}).get("status") == 200)
    distinct_body = len({body_shas[s] for s in SESSIONS if body_shas.get(s)})
    has_any_field = any(recs for recs in per_session_records.values())
    if route_ok < 3:
        verdict = "UNREACHABLE"
    elif len(all_values) >= 2 and distinct_body >= 2:
        verdict = "RECOVERED_SESSION_SCOPED"
    elif len(all_values) == 1:
        verdict = "RECOVERED_INVARIANT"
    elif has_any_field:
        verdict = "RECOVERED_EMPTY"
    else:
        verdict = "NO_FIELD"
    # per-field observed (state, value) sets for agreement
    field_value_sets = {}
    for s, fields in idx.items():
        for field, recs in fields.items():
            bucket = field_value_sets.setdefault(field, set())
            for r in recs:
                bucket.add((r["state"], r["value"]))
    return {
        "distinct_values": len(all_values),
        "extract_rate": extracted_sessions / len(SESSIONS),
        "verdict": verdict,
        "route_ok": route_ok,
        "distinct_body": distinct_body,
        "field_value_sets": field_value_sets,
        "field_present_by_session": {
            s: sorted(set(fields.keys())) for s, fields in idx.items()
        },
        "all_values": sorted(all_values),
    }


def kappa(pairs):
    """Cohen's kappa over list of (rater_a, rater_b) boolean presence labels."""
    n = len(pairs)
    if n == 0:
        return None
    a = [p[0] for p in pairs]
    b = [p[1] for p in pairs]
    po = sum(1 for x, y in pairs if x == y) / n
    pa1 = sum(a) / n
    pb1 = sum(b) / n
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    if pe == 1.0:
        return None
    return (po - pe) / (1 - pe)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    for d in (RAW_DIR, BODY_DIR, DERIVED_DIR):
        d.mkdir(parents=True, exist_ok=True)

    verify_ok_before, verify_before = verify_frozen_inputs("before")
    if not verify_ok_before:
        _emit_failure("V11 frozen-input verification failed before first request", verify_before)
        raise SystemExit(2)

    attestation = path_independence_attestation()
    fixtures_result = run_fixtures()

    rec = Recorder()
    jars = {}          # (anchor_id, session) -> CookieJar
    bodies = {}        # (anchor_id, session) -> bytes
    warm_jars = {}     # anchor_id -> CookieJar (S4 jar)

    # ---- fresh captures: session-major so jars are created per (anchor,session)
    for session in SESSIONS:
        for anchor_id, url in POSITIVE_ANCHORS + NEGATIVE_ANCHORS:
            jar = CookieJar()
            jars[(anchor_id, session)] = jar
            record, body = rec.capture(anchor_id, url, session, jar)
            bodies[(anchor_id, session)] = body
            _store_body(record, body, anchor_id, session, None)

    # ---- warm-jar diagnostic: 2 same-jar re-captures per positive anchor from S4
    for anchor_id, url in POSITIVE_ANCHORS:
        jar = jars[(anchor_id, "S4")]
        warm_jars[anchor_id] = jar
        for wi in (1, 2):
            record, body = rec.capture(anchor_id, url, "S4", jar, phase="warm", warm_index=wi)
            bodies[(anchor_id, f"S4-warm{wi}")] = body
            _store_body(record, body, anchor_id, "S4", wi)

    # persist raw records
    raw_jsonl = RAW_DIR / "records.jsonl"
    with raw_jsonl.open("w") as fh:
        for r in rec.records:
            fh.write(json.dumps(r, sort_keys=True) + "\n")

    # ---- session isolation
    session_isolation = _session_isolation(rec.records, jars)

    # ---- extraction over positives + negatives
    extraction_derived = []
    pos_data = {}
    for anchor_id, url in POSITIVE_ANCHORS:
        a_by_session, b_by_session = {}, {}
        for session in SESSIONS:
            body = bodies[(anchor_id, session)]
            a_by_session[session] = path_a.extract(body)
            b_by_session[session] = path_b.extract(body)
            extraction_derived.append({"anchor_id": anchor_id, "session": session,
                                       "path": "A", "agsi": a_by_session[session]})
            extraction_derived.append({"anchor_id": anchor_id, "session": session,
                                       "path": "B", "agsi": b_by_session[session]})
        headers_by_session = {s: _headers_for(rec.records, anchor_id, s) for s in SESSIONS}
        body_shas = {s: _body_sha_for(rec.records, anchor_id, s) for s in SESSIONS}
        pos_data[anchor_id] = {
            "a": a_by_session, "b": b_by_session,
            "headers": headers_by_session, "body_shas": body_shas,
        }
    neg_data = {}
    for anchor_id, url in NEGATIVE_ANCHORS:
        a_list, b_list = [], []
        for session in SESSIONS:
            body = bodies[(anchor_id, session)]
            a_list += path_a.extract(body)
            b_list += path_b.extract(body)
        neg_data[anchor_id] = {"a": a_list, "b": b_list}

    with (DERIVED_DIR / "extraction.jsonl").open("w") as fh:
        for row in extraction_derived:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    # ---- GATE C metrics
    m_cert_route_ok = 0
    m_cert_body_variable = 0
    m_cert_field_present = 0
    for anchor_id, url in POSITIVE_ANCHORS:
        d = pos_data[anchor_id]
        route_ok = sum(1 for s in SESSIONS if d["headers"][s].get("status") == 200)
        if route_ok >= 3:
            m_cert_route_ok += 1
        if len({d["body_shas"][s] for s in SESSIONS if d["body_shas"][s]}) >= 2:
            m_cert_body_variable += 1
        sess_with_field = sum(
            1 for s in SESSIONS
            if neutral_detector.find_in_list_names(bodies[(anchor_id, s)])
        )
        if sess_with_field >= 3:
            m_cert_field_present += 1
    m_cert_neg_values_a = sum(
        1 for a in neg_data for r in neg_data[a]["a"] if r["state"] == "VALUE")
    m_cert_neg_values_b = sum(
        1 for a in neg_data for r in neg_data[a]["b"] if r["state"] == "VALUE")

    gate_c1 = (m_cert_route_ok >= 3) and (m_cert_field_present >= 3)
    gate_c2 = (m_cert_neg_values_a == 0) and (m_cert_neg_values_b == 0)
    gate_c3 = session_isolation["pass"]
    gate_c_pass = gate_c1 and gate_c2 and gate_c3
    gate_c4_body_variable_ok = m_cert_body_variable >= 3

    # ---- per-anchor path metrics
    anchor_metrics = {}
    m_agree_valueset = 0
    m_agree_verdict = 0
    m_n_session_scoped = 0
    m_n_representation_loss = 0
    m_n_extraction_unreliable = 0
    kappa_pairs = []
    for anchor_id, url in POSITIVE_ANCHORS:
        d = pos_data[anchor_id]
        ma = path_metrics(anchor_id, d["a"], d["headers"], d["body_shas"])
        mb = path_metrics(anchor_id, d["b"], d["headers"], d["body_shas"])
        anchor_metrics[anchor_id] = {"A": ma, "B": mb}
        if ma["field_value_sets"] == mb["field_value_sets"]:
            m_agree_valueset += 1
        if ma["verdict"] == mb["verdict"]:
            m_agree_verdict += 1
        if ma["verdict"] == mb["verdict"] == "RECOVERED_SESSION_SCOPED":
            m_n_session_scoped += 1
        if (ma["verdict"] == mb["verdict"]
                and ma["verdict"] in ("RECOVERED_EMPTY", "NO_FIELD")
                and mb["distinct_body"] >= 2):
            m_n_representation_loss += 1
        if ma["verdict"] != mb["verdict"]:
            m_n_extraction_unreliable += 1
        # kappa over (anchor, session, field) presence
        fields_union = set()
        for s in SESSIONS:
            fields_union |= set(ma["field_present_by_session"][s])
            fields_union |= set(mb["field_present_by_session"][s])
        for s in SESSIONS:
            for field in fields_union:
                present_a = bool([r for r in d["a"][s]
                                  if r["field_name"] == field and r["state"] == "VALUE"])
                present_b = bool([r for r in d["b"][s]
                                  if r["field_name"] == field and r["state"] == "VALUE"])
                kappa_pairs.append((present_a, present_b))

    m_kappa = kappa(kappa_pairs)

    # ---- canary
    canary_a = anchor_metrics["CAL-POS-1"]["A"]
    canary_b = anchor_metrics["CAL-POS-1"]["B"]
    canary_a_vals = {r["value"] for s in SESSIONS for r in pos_data["CAL-POS-1"]["a"][s]
                     if r["field_name"] == "authenticity_token" and r["state"] == "VALUE"}
    canary_b_vals = {r["value"] for s in SESSIONS for r in pos_data["CAL-POS-1"]["b"][s]
                     if r["field_name"] == "authenticity_token" and r["state"] == "VALUE"}
    m_canary_pass = len(canary_a_vals) >= 2 and len(canary_b_vals) >= 2

    # ---- warm-jar diagnostic
    warm_metrics = {}
    for anchor_id, url in POSITIVE_ANCHORS:
        warm_records = [r for r in rec.records if r["anchor_id"] == anchor_id and r["phase"] == "warm"]
        warm_records.sort(key=lambda r: r["warm_index"])
        fresh_s4 = [r for r in rec.records if r["anchor_id"] == anchor_id
                    and r["session"] == "S4" and r["phase"] == "fresh"][0]
        # within-warm-jar variation: consecutive comparisons S4->W1, W1->W2
        seq = [fresh_s4] + warm_records
        value_comps = list(zip(seq[:-1], seq[1:]))
        val_changes = 0
        body_changes = 0
        for prev, cur in value_comps:
            pv = _first_agsi_value(path_a.extract(bodies.get((anchor_id, prev["session"])) or b""))
            # use stored body for all
        # recompute using bodies stored per record
        def _body_of(r):
            if r["phase"] == "fresh":
                return bodies.get((anchor_id, r["session"]), b"")
            return bodies.get((anchor_id, f'{r["session"]}-warm{r["warm_index"]}'), b"")
        vals = [_first_agsi_value(path_a.extract(_body_of(r))) for r in seq]
        bodies_seq = [_body_of(r) for r in seq]
        for i in range(1, len(seq)):
            if vals[i] != vals[i - 1]:
                val_changes += 1
            if sha256_bytes(bodies_seq[i]) != sha256_bytes(bodies_seq[i - 1]):
                body_changes += 1
        denom = len(seq) - 1
        warm_metrics[anchor_id] = {
            "warm_jar_variation_rate": (val_changes / denom) if denom else None,
            "warm_jar_body_variation_rate": (body_changes / denom) if denom else None,
            "fresh_jar_value_variation_rate": _fresh_value_variation(pos_data[anchor_id]["a"]),
        }

    # ---- part (ii): D1V trials
    d1v = _d1v_analysis(pos_data, m_n_session_scoped)

    # ---- decision rule
    status, outcome, branch = _decide(
        gate_c1, gate_c2, gate_c3, gate_c_pass, gate_c4_body_variable_ok,
        m_canary_pass, fixtures_result, attestation,
        m_agree_valueset, m_agree_verdict,
        m_n_session_scoped, m_n_representation_loss, m_n_extraction_unreliable,
        d1v,
    )

    verify_ok_after, verify_after = verify_frozen_inputs("after")

    # ---- assemble result.json
    metrics = _assemble_metrics(
        m_cert_route_ok, m_cert_body_variable, m_cert_field_present, session_isolation,
        m_cert_neg_values_a, m_cert_neg_values_b, anchor_metrics,
        m_agree_valueset, m_agree_verdict, m_kappa, m_canary_pass, fixtures_result,
        m_n_session_scoped, m_n_representation_loss, m_n_extraction_unreliable,
        warm_metrics, d1v,
    )
    controls = _assemble_controls(
        session_isolation, anchor_metrics, neg_data, attestation, fixtures_result,
        d1v, gate_c1, gate_c2, gate_c3, gate_c4_body_variable_ok,
        m_canary_pass, m_agree_valueset, m_agree_verdict, branch,
    )

    artifacts = _collect_artifacts()

    result = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "branch": branch,
        "metrics": metrics,
        "controls": controls,
        "artifacts": artifacts,
        "observations": _observations(
            rec, session_isolation, anchor_metrics, neg_data, fixtures_result, d1v,
            m_canary_pass, m_agree_valueset, m_agree_verdict, branch,
        ),
        "validity_notes": _validity_notes(
            verify_ok_before, verify_ok_after, attestation, d1v, m_kappa,
            gate_c4_body_variable_ok,
        ),
        "unresolved": _unresolved(branch, d1v, m_agree_valueset, m_agree_verdict),
        "frozen_input_verification": {"before": verify_before, "after": verify_after},
    }
    (EXP_DIR / "result.json").write_text(json.dumps(result, indent=2, sort_keys=False) + "\n")

    provenance = _provenance(rec, attestation, raw_jsonl, verify_before)
    (EXP_DIR / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")

    _write_report(result, report_extra={
        "anchor_metrics": anchor_metrics,
        "neg_data_values": {a: {"A": [r["value"] for r in neg_data[a]["a"] if r["state"] == "VALUE"],
                                "B": [r["value"] for r in neg_data[a]["b"] if r["state"] == "VALUE"]}
                            for a in neg_data},
        "fixtures": fixtures_result,
        "attestation": attestation,
        "d1v": d1v,
        "warm_metrics": warm_metrics,
        "session_isolation": session_isolation,
        "record_count": len(rec.records),
    })

    print("STATUS", status, "OUTCOME", outcome, "BRANCH", branch)
    print("GATE_C", gate_c_pass, "C1", gate_c1, "C2", gate_c2, "C3", gate_c3, "C4", gate_c4_body_variable_ok)
    print("requests", rec.request_count)
    return 0


def _first_agsi_value(records):
    vals = [r["value"] for r in records if r["state"] == "VALUE"]
    return tuple(sorted(vals))


def _fresh_value_variation(a_by_session):
    seq = [a_by_session[s] for s in SESSIONS]
    vals = [_first_agsi_value(recs) for recs in seq]
    denom = len(vals) - 1
    changes = sum(1 for i in range(1, len(vals)) if vals[i] != vals[i - 1])
    return (changes / denom) if denom else None


def _headers_for(records, anchor_id, session):
    for r in records:
        if r["anchor_id"] == anchor_id and r["session"] == session and r["phase"] == "fresh":
            return r
    return {}


def _body_sha_for(records, anchor_id, session):
    h = _headers_for(records, anchor_id, session)
    return h.get("body_sha256")


def _store_body(record, body, anchor_id, session, warm_index):
    suffix = f"warm{warm_index}" if warm_index else "fresh"
    path = BODY_DIR / anchor_id / f"{session}_{suffix}.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    record["body_path"] = str(path.relative_to(ROOT))


def _session_isolation(records, jars):
    per_anchor = {}
    ok_all = True
    for anchor_id in [a for a, _ in POSITIVE_ANCHORS] + [a for a, _ in NEGATIVE_ANCHORS]:
        sets = {}
        empties = {}
        for session in SESSIONS:
            jar = jars.get((anchor_id, session))
            if jar is None:
                continue
            sets[session] = _jar_pairs(jar)
            empties[session] = any(
                r["anchor_id"] == anchor_id and r["session"] == session
                and r["phase"] == "fresh" and r["jar_was_empty_before_request"]
                for r in records
            )
        disjoint = True
        sessions = list(sets)
        for i in range(len(sessions)):
            for j in range(i + 1, len(sessions)):
                if sets[sessions[i]] & sets[sessions[j]]:
                    disjoint = False
        all_empty = all(empties.values())
        anchor_ok = disjoint and all_empty
        ok_all = ok_all and anchor_ok
        per_anchor[anchor_id] = {
            "pairwise_disjoint": disjoint,
            "no_first_request_cookie": all_empty,
            "sizes": {s: len(sets[s]) for s in sessions},
            "pass": anchor_ok,
        }
    return {"pass": ok_all, "per_anchor": per_anchor}


# --------------------------------------------------------------------------
# D1V / part ii
# --------------------------------------------------------------------------
def _transport_signature(header_record):
    h = header_record.get("headers", {})
    cc = h.get("Cache-Control") or ""
    m = re.search(r"max-age\s*=\s*(\d+)", cc, re.I)
    max_age = m.group(1) if m else None
    return (h.get("ETag"), h.get("Last-Modified"), max_age, h.get("Vary"))


def _structure_signature(agsi):
    return (agsi["type_class"], agsi["form_action"], agsi["form_method"],
            tuple(agsi["form_input_names"]))


def _d1v_analysis(pos_data, m_n_session_scoped):
    all_trials = []
    d1v_trials = []
    channel_fire = {"CH-STRUCT-SIG": 0, "CH-TRANSPORT-VALIDATOR": 0, "CH-POSTCOND-SEM": 0}
    channel_names = ["CH-STRUCT-SIG", "CH-TRANSPORT-VALIDATOR", "CH-POSTCOND-SEM", "CH-PRECOND-BINDING"]
    channel_fire = {c: 0 for c in channel_names}
    channel_not_fire = {c: 0 for c in channel_names}
    for anchor_id in [a for a, _ in POSITIVE_ANCHORS]:
        d = pos_data[anchor_id]
        fields = set()
        for s in SESSIONS:
            fields |= set(r["field_name"] for r in d["a"][s])
        for field in sorted(fields):
            rec_s1 = [r for r in d["a"]["S1"] if r["field_name"] == field]
            if len(rec_s1) != 1 or rec_s1[0]["state"] != "VALUE":
                continue
            s1 = rec_s1[0]
            for st in ["S2", "S3", "S4"]:
                rec_st = [r for r in d["a"][st] if r["field_name"] == field]
                if len(rec_st) != 1:
                    continue
                cur = rec_st[0]
                if cur["state"] != "VALUE":
                    continue
                recorded = s1["value"]
                live = cur["value"]
                structural_change = _structure_signature(s1) != _structure_signature(cur)
                transport_change = _transport_signature(d["headers"]["S1"]) != _transport_signature(d["headers"][st])
                field_set_s1 = set(r["field_name"] for r in d["a"]["S1"])
                field_set_st = set(r["field_name"] for r in d["a"][st])
                postcond_change = field_set_s1 != field_set_st
                fire = {
                    "CH-STRUCT-SIG": structural_change,
                    "CH-TRANSPORT-VALIDATOR": transport_change,
                    "CH-POSTCOND-SEM": postcond_change,
                    "CH-PRECOND-BINDING": live != recorded,
                }
                for c, f in fire.items():
                    if f:
                        channel_fire[c] += 1
                    else:
                        channel_not_fire[c] += 1
                incumbent_reuse = not (structural_change or transport_change or postcond_change)
                valueaware_reuse = (live == recorded)
                trial = {
                    "anchor_id": anchor_id,
                    "field_name": field,
                    "current_session": st,
                    "recorded_value": recorded,
                    "live_value": live,
                    "label": "STALE" if live != recorded else "FRESH",
                    "structural_change": structural_change,
                    "transport_change": transport_change,
                    "postcond_change": postcond_change,
                    "incumbent_reuse": incumbent_reuse,
                    "valueaware_reuse": valueaware_reuse,
                }
                all_trials.append(trial)
                if (live != recorded) and not structural_change and not transport_change:
                    d1v_trials.append(trial)

    n_d1v = len(d1v_trials)
    n_decisions = len({t["incumbent_reuse"] for t in d1v_trials} | {t["valueaware_reuse"] for t in d1v_trials})
    fa_incumbent = (sum(1 for t in d1v_trials if t["incumbent_reuse"]) / n_d1v) if n_d1v else None
    fa_valueaware = (sum(1 for t in d1v_trials if t["valueaware_reuse"]) / n_d1v) if n_d1v else None
    diff = None
    diff_low = None
    if n_d1v:
        diffs = [1.0 if t["incumbent_reuse"] else 0.0 for t in d1v_trials]
        vals = [1.0 if t["valueaware_reuse"] else 0.0 for t in d1v_trials]
        diff = sum(diffs) / n_d1v - sum(vals) / n_d1v
        per_anchor = {}
        for t in d1v_trials:
            per_anchor.setdefault(t["anchor_id"], []).append(
                1.0 if t["incumbent_reuse"] else 0.0)
        anchors = sorted(per_anchor)
        rng = random.Random(FROZEN_SEED)
        boots = []
        for _ in range(10000):
            sample = [rng.choice(anchors) for _ in range(len(anchors))]
            pooled = [v for a in sample for v in per_anchor[a]]
            boots.append(sum(pooled) / len(pooled))
        boots.sort()
        diff_low = boots[int(0.025 * len(boots))]

    # non-degeneracy (NC-NONDEGENERATE-ESTIMATOR): >=2 decisions on D1V and
    # every channel active anywhere both fires and does not fire at least once.
    channels_nondegenerate = all(channel_fire[c] > 0 and channel_not_fire[c] > 0 for c in channel_names)
    nondegenerate = (n_decisions >= 2) and channels_nondegenerate

    # GATE B decision
    if m_n_session_scoped < 3:
        gate_b_branch = "NOT_READ_D1_NOT_REACHED"
    elif n_d1v < 6 or n_decisions < 2 or not nondegenerate:
        gate_b_branch = "DATA-INSUFFICIENT-D1V"
    elif diff is not None and diff >= 0.10 and diff_low is not None and diff_low > 0:
        gate_b_branch = "INCUMBENT-BLIND-CONFIRMED"
    else:
        gate_b_branch = "INCUMBENT-NOT-BLIND"

    return {
        "M-N-D1V": n_d1v,
        "M-N-DECISIONS-D1V": n_decisions,
        "M-FA-INCUMBENT-D1V": fa_incumbent,
        "M-FA-VALUEAWARE-D1V": fa_valueaware,
        "M-PAIRED-FA-DIFF-D1V": diff,
        "M-PAIRED-FA-DIFF-D1V-LOW": diff_low,
        "nondegenerate": nondegenerate,
        "channels_nondegenerate": channels_nondegenerate,
        "channel_fire": channel_fire,
        "channel_not_fire": channel_not_fire,
        "gate_b_branch": gate_b_branch,
        "n_all_trials": len(all_trials),
        "n_d1v_trials": len(d1v_trials),
        "d1v_trial_examples": d1v_trials[:10],
    }


# --------------------------------------------------------------------------
# decision
# --------------------------------------------------------------------------
def _decide(gate_c1, gate_c2, gate_c3, gate_c_pass, gate_c4_ok,
            m_canary_pass, fixtures_result, attestation,
            agree_valueset, agree_verdict,
            n_session_scoped, n_rep_loss, n_unreliable, d1v):
    if not gate_c_pass:
        return "MEASUREMENT_INVALID", "INCONCLUSIVE", "F-CERT"
    if not gate_c4_ok:
        return "COMPLETE", "INCONCLUSIVE", "NO-BODY-VARIATION"
    gate_e1 = m_canary_pass
    gate_e2 = (fixtures_result["M_FIXTURE_CANARY_PASS"]
               and fixtures_result["M_FIXTURE_EMPTY_AGREE"]
               and fixtures_result["M_FIXTURE_JSSTRING_VALUES"] == 0
               and attestation["path_independence_pass"])
    if not (gate_e1 and gate_e2):
        return "MEASUREMENT_INVALID", "INCONCLUSIVE", "F-INSTR"
    gate_e3 = (agree_valueset >= 3) and (agree_verdict >= 3)
    if not gate_e3:
        return "COMPLETE", "MIXED", "EXTRACTION-UNRELIABLE"
    if n_session_scoped >= 3:
        return "COMPLETE", "SUPPORTS", "EXTRACTION-DEFECT-CONFIRMED"
    if n_rep_loss >= 3:
        return "COMPLETE", "FALSIFIES", "REPRESENTATION-LOSS-CONFIRMED"
    return "COMPLETE", "MIXED", "MIXED-ANCHORS"


# --------------------------------------------------------------------------
# metrics / controls / observations / provenance / report
# --------------------------------------------------------------------------
def _assemble_metrics(route_ok, body_var, field_present, session_isolation,
                      neg_a, neg_b, anchor_metrics, agree_valueset, agree_verdict,
                      m_kappa, m_canary_pass, fixtures_result, n_ss, n_rl, n_unrel,
                      warm_metrics, d1v):
    metrics = {
        "M-CERT-ROUTE-OK": {"value": route_ok, "unit": "anchors (0..4)"},
        "M-CERT-BODY-VARIABLE": {"value": body_var, "unit": "anchors (0..4)"},
        "M-CERT-FIELD-PRESENT": {"value": field_present, "unit": "anchors (0..4)"},
        "M-CERT-SESSION-ISOLATION-PASS": {"value": session_isolation["pass"], "unit": "boolean"},
        "M-CERT-NEG-VALUES-A": {"value": neg_a, "unit": "count"},
        "M-CERT-NEG-VALUES-B": {"value": neg_b, "unit": "count"},
        "M-EXTRACT-AGREE-VALUESET": {"value": agree_valueset, "unit": "anchors (0..4)"},
        "M-EXTRACT-AGREE-VERDICT": {"value": agree_verdict, "unit": "anchors (0..4)"},
        "M-EXTRACT-KAPPA": {"value": m_kappa, "unit": "dimensionless"},
        "M-CANARY-PASS": {"value": m_canary_pass, "unit": "boolean"},
        "M-FIXTURE-CANARY-PASS": {"value": fixtures_result["M_FIXTURE_CANARY_PASS"], "unit": "boolean"},
        "M-FIXTURE-EMPTY-AGREE": {"value": fixtures_result["M_FIXTURE_EMPTY_AGREE"], "unit": "boolean"},
        "M-FIXTURE-JSSTRING-VALUES": {"value": fixtures_result["M_FIXTURE_JSSTRING_VALUES"], "unit": "count (must be 0)"},
        "M-N-SESSION-SCOPED-CONFIRMED": {"value": n_ss, "unit": "anchors (0..4)"},
        "M-N-REPRESENTATION-LOSS": {"value": n_rl, "unit": "anchors (0..4)"},
        "M-N-EXTRACTION-UNRELIABLE": {"value": n_unrel, "unit": "anchors (0..4)"},
        "M-INVISIBLE-STALE-PREV": {
            "value": None,
            "unit": "fraction",
            "reason_not_measured": "SB-04: the behaviourally invisible stale cell is not measured by this "
                                   "packet and may satisfy no gate; reported null, never 0.0.",
        },
    }
    for anchor_id in anchor_metrics:
        ma = anchor_metrics[anchor_id]["A"]
        mb = anchor_metrics[anchor_id]["B"]
        metrics[f"M-DISTINCT-VALUES-A-{anchor_id}"] = {"value": ma["distinct_values"], "unit": "count"}
        metrics[f"M-DISTINCT-VALUES-B-{anchor_id}"] = {"value": mb["distinct_values"], "unit": "count"}
        metrics[f"M-EXTRACT-RATE-A-{anchor_id}"] = {"value": ma["extract_rate"], "unit": "fraction"}
        metrics[f"M-EXTRACT-RATE-B-{anchor_id}"] = {"value": mb["extract_rate"], "unit": "fraction"}
        metrics[f"M-ANCHOR-VERDICT-{anchor_id}"] = {"value": [ma["verdict"], mb["verdict"]], "unit": "enum-pair"}
        metrics[f"M-WARMJAR-VARIATION-RATE-{anchor_id}"] = {
            "value": warm_metrics[anchor_id]["warm_jar_variation_rate"], "unit": "fraction"}
        metrics[f"M-WARMJAR-BODY-VARIATION-RATE-{anchor_id}"] = {
            "value": warm_metrics[anchor_id]["warm_jar_body_variation_rate"], "unit": "fraction"}
        metrics[f"M-WARMJAR-FRESH-VALUE-VARIATION-RATE-{anchor_id}"] = {
            "value": warm_metrics[anchor_id]["fresh_jar_value_variation_rate"], "unit": "fraction"}
    metrics["M-FA-INCUMBENT-D1V"] = {"value": d1v["M-FA-INCUMBENT-D1V"], "unit": "fraction"}
    metrics["M-FA-VALUEAWARE-D1V"] = {"value": d1v["M-FA-VALUEAWARE-D1V"], "unit": "fraction"}
    metrics["M-PAIRED-FA-DIFF-D1V"] = {"value": d1v["M-PAIRED-FA-DIFF-D1V"], "unit": "fraction"}
    metrics["M-PAIRED-FA-DIFF-D1V-LOW"] = {"value": d1v["M-PAIRED-FA-DIFF-D1V-LOW"], "unit": "fraction"}
    metrics["M-N-D1V"] = {"value": d1v["M-N-D1V"], "unit": "trials"}
    metrics["M-N-DECISIONS-D1V"] = {"value": d1v["M-N-DECISIONS-D1V"], "unit": "count"}
    return metrics


def _assemble_controls(session_isolation, anchor_metrics, neg_data, attestation,
                       fixtures_result, d1v, c1, c2, c3, c4, m_canary_pass,
                       agree_valueset, agree_verdict, branch):
    pos_pass = all(anchor_metrics[a]["A"]["verdict"] == "RECOVERED_SESSION_SCOPED"
                   and anchor_metrics[a]["B"]["verdict"] == "RECOVERED_SESSION_SCOPED"
                   for a in anchor_metrics)
    return {
        "GATE-C1": {"expected": "M-CERT-ROUTE-OK>=3 and M-CERT-FIELD-PRESENT>=3",
                     "observed": c1, "result": "PASS" if c1 else "FAIL"},
        "GATE-C2": {"expected": "M-CERT-NEG-VALUES-A==0 and M-CERT-NEG-VALUES-B==0",
                     "observed": c2, "result": "PASS" if c2 else "FAIL"},
        "GATE-C3": {"expected": "M-CERT-SESSION-ISOLATION-PASS==true",
                     "observed": session_isolation["pass"], "result": "PASS" if c3 else "FAIL"},
        "GATE-C4": {"expected": "M-CERT-BODY-VARIABLE>=3 (non-blocking disclosure)",
                     "observed": c4, "result": "PASS" if c4 else "DISCLOSURE-NO-BODY-VARIATION"},
        "GATE-E1": {"expected": "M-CANARY-PASS==true", "observed": m_canary_pass,
                     "result": "PASS" if m_canary_pass else "FAIL"},
        "GATE-E2": {"expected": "fixtures + NC-PATH-INDEPENDENCE pass",
                     "observed": {
                         "M-FIXTURE-CANARY-PASS": fixtures_result["M_FIXTURE_CANARY_PASS"],
                         "M-FIXTURE-EMPTY-AGREE": fixtures_result["M_FIXTURE_EMPTY_AGREE"],
                         "M-FIXTURE-JSSTRING-VALUES": fixtures_result["M_FIXTURE_JSSTRING_VALUES"],
                         "NC-PATH-INDEPENDENCE": attestation["path_independence_pass"],
                     },
                     "result": "PASS" if (fixtures_result["M_FIXTURE_CANARY_PASS"]
                                          and fixtures_result["M_FIXTURE_EMPTY_AGREE"]
                                          and fixtures_result["M_FIXTURE_JSSTRING_VALUES"] == 0
                                          and attestation["path_independence_pass"]) else "FAIL"},
        "GATE-E3": {"expected": "M-EXTRACT-AGREE-VALUESET>=3 and M-EXTRACT-AGREE-VERDICT>=3",
                     "observed": {"M-EXTRACT-AGREE-VALUESET": agree_valueset,
                                  "M-EXTRACT-AGREE-VERDICT": agree_verdict},
                     "result": "PASS" if (agree_valueset >= 3 and agree_verdict >= 3) else "FAIL"},
        "B-SINGLE-PATH-A": {
            "expected_behavior": "P-EXTRACT-A alone cannot self-certify",
            "observed": {a: anchor_metrics[a]["A"]["verdict"] for a in anchor_metrics},
            "result": "OBSERVED",
        },
        "B-SINGLE-PATH-B": {
            "expected_behavior": "P-EXTRACT-B alone; disagreement with A is the extraction signal",
            "observed": {a: anchor_metrics[a]["B"]["verdict"] for a in anchor_metrics},
            "result": "OBSERVED",
        },
        "B-PARENT-METHOD-REIMPL": {
            "expected_behavior": "best-effort reconstruction of the parent's method over the same stored bodies; no gate depends on it",
            "observed": {
                "reconstruction_note": "Parent preserved no code. Proxy = P-EXTRACT-A (html.parser, non-GET form token fields + frozen-list meta tokens, no JS), which is the recorded description of the parent method.",
                "CAL-POS-2_distinct_values": anchor_metrics["CAL-POS-2"]["A"]["distinct_values"],
                "CAL-POS-2_verdict": anchor_metrics["CAL-POS-2"]["A"]["verdict"],
            },
            "result": "DISCLOSED-PROXY",
        },
        "B-INCUMBENT-SIGNAL-ONLY": {
            "expected_behavior": "value-blind: CH-STRUCT-SIG + CH-TRANSPORT-VALIDATOR + CH-POSTCOND-SEM; predicted to reuse on ~1.0 of clean D1V trials",
            "observed": {
                "M-FA-INCUMBENT-D1V": d1v["M-FA-INCUMBENT-D1V"],
                "channel_fire_counts": d1v["channel_fire"],
                "channel_not_fire_counts": d1v["channel_not_fire"],
            },
            "result": d1v["gate_b_branch"],
        },
        "B-VALUE-AWARE": {
            "expected_behavior": "CH-PRECOND-BINDING: abstains iff live != recorded; byte-equality revalidation, not server validity",
            "observed": {"M-FA-VALUEAWARE-D1V": d1v["M-FA-VALUEAWARE-D1V"]},
            "result": d1v["gate_b_branch"],
        },
        "B-NO-GUARD-REPLAY": {
            "expected_behavior": "always reuse; raw-observation reference for STALE/FRESH accounting",
            "observed": {
                "n_all_trials": d1v["n_all_trials"],
                "n_stale_trials": d1v["n_d1v_trials"],
            },
            "result": "OBSERVED",
        },
        "PC-EXTRACT-CANARY": {
            "expected": "both paths recover >=2 distinct authenticity_token values on CAL-POS-1",
            "observed": m_canary_pass, "result": "PASS" if m_canary_pass else "FAIL",
        },
        "PC-INCUMBENT-BLINDNESS": {
            "expected": "M-FA-INCUMBENT-D1V reported against frozen structural prediction 1.0",
            "observed": d1v["M-FA-INCUMBENT-D1V"],
            "result": d1v["gate_b_branch"],
        },
        "NC-CAL-NEG-ALL-REJECTED": {
            "expected": "0 in-list values under BOTH paths on all 4 negatives",
            "observed": {
                "CAL-NEG-1": {"A": [r["value"] for r in neg_data["CAL-NEG-1"]["a"] if r["state"] == "VALUE"],
                              "B": [r["value"] for r in neg_data["CAL-NEG-1"]["b"] if r["state"] == "VALUE"]},
                "CAL-NEG-2": {"A": [r["value"] for r in neg_data["CAL-NEG-2"]["a"] if r["state"] == "VALUE"],
                              "B": [r["value"] for r in neg_data["CAL-NEG-2"]["b"] if r["state"] == "VALUE"]},
                "CAL-NEG-3": {"A": [r["value"] for r in neg_data["CAL-NEG-3"]["a"] if r["state"] == "VALUE"],
                              "B": [r["value"] for r in neg_data["CAL-NEG-3"]["b"] if r["state"] == "VALUE"]},
                "CAL-NEG-4": {"A": [r["value"] for r in neg_data["CAL-NEG-4"]["a"] if r["state"] == "VALUE"],
                              "B": [r["value"] for r in neg_data["CAL-NEG-4"]["b"] if r["state"] == "VALUE"]},
            },
            "result": "PASS" if c2 else "FAIL",
        },
        "NC-EXTRACT-EMPTY-VALUE": {
            "expected": "both paths classify SYN-EMPTY-VALUE fields PRESENT-EMPTY and agree",
            "observed": fixtures_result["M_FIXTURE_EMPTY_AGREE"],
            "result": "PASS" if fixtures_result["M_FIXTURE_EMPTY_AGREE"] else "FAIL",
        },
        "NC-EXTRACT-JSSTRING": {
            "expected": "0 non-empty values from SYN-JSSTRING, both paths",
            "observed": fixtures_result["M_FIXTURE_JSSTRING_VALUES"],
            "result": "PASS" if fixtures_result["M_FIXTURE_JSSTRING_VALUES"] == 0 else "FAIL",
        },
        "NC-PATH-INDEPENDENCE": {
            "expected": "AST import attestation, separate hashes, perturbation invariance",
            "observed": {
                "source_hashes_differ": attestation["source_hashes_differ"],
                "path_b_forbidden_imports": attestation["path_b_forbidden_imports"],
                "no_anchor_special_casing": attestation["no_anchor_special_casing"],
                "perturbation_invariant": attestation["perturbation_invariant"],
            },
            "result": "PASS" if attestation["path_independence_pass"] else "FAIL",
        },
        "NC-SESSION-ISOLATION": {
            "expected": "fresh disjoint jars; no first-request Cookie",
            "observed": session_isolation["per_anchor"],
            "result": "PASS" if session_isolation["pass"] else "FAIL",
        },
        "NC-TIME-VS-SESSION": {
            "expected": "warm-jar diagnostic reported; not a pass/fail gate",
            "observed": "see M-WARMJAR-*-RATE metrics",
            "result": "DIAGNOSTIC",
        },
        "NC-NONDEGENERATE-ESTIMATOR": {
            "expected": ">=2 decisions on D1V and every active channel fires and does not fire once",
            "observed": {
                "M-N-DECISIONS-D1V": d1v["M-N-DECISIONS-D1V"],
                "nondegenerate": d1v["nondegenerate"],
                "channels_nondegenerate": d1v["channels_nondegenerate"],
                "channel_fire": d1v["channel_fire"],
                "channel_not_fire": d1v["channel_not_fire"],
            },
            "result": "PASS" if d1v["nondegenerate"] else "DEGENERATE-NOT-EVALUABLE",
        },
        "F-INSTR": {"observed_triggered": branch == "F-INSTR"},
        "F-REPLOSS": {"observed_triggered": branch == "REPRESENTATION-LOSS-CONFIRMED"},
        "F-UNRELIABLE": {"observed_triggered": branch == "EXTRACTION-UNRELIABLE"},
        "F-BLIND": {"observed_triggered": d1v["gate_b_branch"] == "INCUMBENT-NOT-BLIND"},
        "F-CERT": {"observed_triggered": branch == "F-CERT"},
        "CAL-POS-1": {"role": "positive; SPIDER_CORROBORATED canary",
                       "verdict_pair": [anchor_metrics["CAL-POS-1"]["A"]["verdict"],
                                        anchor_metrics["CAL-POS-1"]["B"]["verdict"]]},
        "CAL-POS-2": {"role": "positive; reconciliation anchor",
                       "verdict_pair": [anchor_metrics["CAL-POS-2"]["A"]["verdict"],
                                        anchor_metrics["CAL-POS-2"]["B"]["verdict"]]},
        "CAL-POS-3": {"role": "positive; SPIDER_PARTIAL",
                       "verdict_pair": [anchor_metrics["CAL-POS-3"]["A"]["verdict"],
                                        anchor_metrics["CAL-POS-3"]["B"]["verdict"]]},
        "CAL-POS-4": {"role": "positive; A_PRIORI_CONSTRUCT",
                       "verdict_pair": [anchor_metrics["CAL-POS-4"]["A"]["verdict"],
                                        anchor_metrics["CAL-POS-4"]["B"]["verdict"]]},
        "CAL-POS-5": {"role": "RETIRED (404x4 in parent); excluded from all denominators",
                       "result": "NOT_CONTACTED"},
        "CAL-NEG-1": {"role": "negative"}, "CAL-NEG-2": {"role": "negative"},
        "CAL-NEG-3": {"role": "negative"}, "CAL-NEG-4": {"role": "negative"},
        "SYN-CANARY-BOTH": {"role": "instrument fixture (unscored)",
                             "result": "PASS" if fixtures_result["M_FIXTURE_CANARY_PASS"] else "FAIL"},
        "SYN-EMPTY-VALUE": {"role": "instrument fixture (unscored)",
                             "result": "PASS" if fixtures_result["M_FIXTURE_EMPTY_AGREE"] else "FAIL"},
        "SYN-JSSTRING": {"role": "instrument fixture (unscored)",
                          "result": "PASS" if fixtures_result["M_FIXTURE_JSSTRING_VALUES"] == 0 else "FAIL"},
    }


def _observations(rec, session_isolation, anchor_metrics, neg_data, fixtures_result,
                  d1v, m_canary_pass, agree_valueset, agree_verdict, branch):
    obs = []
    obs.append(f"Requests executed: {rec.request_count} (cap 200).")
    obs.append("Fresh sessions per anchor: " + ", ".join(
        f"{a} jar_sizes={session_isolation['per_anchor'][a]['sizes']}"
        for a in session_isolation["per_anchor"] if a.startswith("CAL-POS")))
    for anchor_id, m in anchor_metrics.items():
        obs.append(
            f"{anchor_id}: verdict_A={m['A']['verdict']} (distinct={m['A']['distinct_values']}), "
            f"verdict_B={m['B']['verdict']} (distinct={m['B']['distinct_values']}), "
            f"route_ok={m['A']['route_ok']}/4, distinct_body={m['A']['distinct_body']}/4."
        )
    obs.append(f"M-EXTRACT-AGREE-VALUESET={agree_valueset}/4, M-EXTRACT-AGREE-VERDICT={agree_verdict}/4.")
    obs.append(f"M-CANARY-PASS={m_canary_pass} (CAL-POS-1 authenticity_token >=2 distinct under both paths).")
    for a, nd in neg_data.items():
        vals_a = [r["value"] for r in nd["a"] if r["state"] == "VALUE"]
        vals_b = [r["value"] for r in nd["b"] if r["state"] == "VALUE"]
        obs.append(f"{a}: path_A non-empty values={vals_a}, path_B non-empty values={vals_b}.")
    obs.append("D1V: M-N-D1V={} M-N-DECISIONS-D1V={} M-FA-INCUMBENT-D1V={} M-FA-VALUEAWARE-D1V={} "
               "M-PAIRED-FA-DIFF-D1V={} low={}; gate_b_branch={}.".format(
                   d1v["M-N-D1V"], d1v["M-N-DECISIONS-D1V"], d1v["M-FA-INCUMBENT-D1V"],
                   d1v["M-FA-VALUEAWARE-D1V"], d1v["M-PAIRED-FA-DIFF-D1V"],
                   d1v["M-PAIRED-FA-DIFF-D1V-LOW"], d1v["gate_b_branch"]))
    obs.append(f"Instrument fixtures: canary={fixtures_result['M_FIXTURE_CANARY_PASS']}, "
               f"empty_agree={fixtures_result['M_FIXTURE_EMPTY_AGREE']}, "
               f"jsstring_values={fixtures_result['M_FIXTURE_JSSTRING_VALUES']}.")
    obs.append(f"Branch: {branch}.")
    return obs


def _validity_notes(verify_before_ok, verify_after_ok, attestation, d1v, m_kappa,
                    gate_c4_ok):
    notes = []
    notes.append(
        "V11: request.json/spec.json/prereg.md sha256 re-verified against freeze.json before the "
        f"first request ({'OK' if verify_before_ok else 'MISMATCH'}) and after the last "
        f"({'OK' if verify_after_ok else 'MISMATCH'}).")
    notes.append(
        "V05/V16: no JavaScript, no browser, no headless rendering executed. Zero recovery (if any) "
        "is a fact about raw bytes only; client-side/XHR-minted values, canvas content and "
        "authenticated state remain structurally invisible and open.")
    notes.append(
        "Entity decoding: CPython's html.parser already decodes HTML character references in "
        "attribute values (verified: a&amp;lt;b&amp; -> a&lt;b&). An additional html.unescape call "
        "would double-decode, so path A relies on the stdlib parser's single decode; path B uses an "
        "independent hand-written decoder. This is the sole operationalization deviation from the "
        "spec's literal 'html.unescape' phrasing.")
    notes.append(
        "ABSENT vs PRESENT-EMPTY: spec.recovered_value_definition says an absent value attribute "
        "means ABSENT, while NC-EXTRACT-EMPTY-VALUE requires a field with no value attribute to be "
        "classified PRESENT-EMPTY. The fixture requirement is operationally explicit, so a found "
        "in-list field with no/empty value is classified PRESENT-EMPTY; ABSENT is used only for a "
        "field name not observed in a session.")
    notes.append(
        "D1V non-degeneracy: NC-NONDEGENERATE-ESTIMATOR is applied as (a) >=2 distinct decisions on "
        "the D1V subset and (b) every active channel fires and does not fire at least once over the "
        "full trial population. Channels are evaluated on captured real data, not hardcoded. "
        f"nondegenerate={d1v['nondegenerate']}.")
    notes.append(
        f"Cohens kappa (M-EXTRACT-KAPPA) is None (undefined) when chance agreement is 1.0. "
        f"Observed kappa={m_kappa}.")
    notes.append(
        "Certificate evidence artifact codex/experiments/EXP-FRONTIER-36306528608/raw/"
        "token_stability.jsonl (sha256 1bbde51d...) referenced by spec.substrate_certificate was NOT "
        "present in the checked-out repository at EXECUTE time; the accepted frontier result.json "
        "(sha256 7b0347ba...) was present. GATE C independently re-measures route validity, body "
        "variation and field presence from live captures, so the certificate did not depend on the "
        "missing file; the absence is disclosed as a provenance limitation.")
    notes.append(
        "B-PARENT-METHOD-REIMPL is a disclosed proxy (parent preserved no code); no gate depends on it.")
    notes.append(
        "Anchor construct overfit is constrained by V07 (no anchor/host-specific rules in producer "
        "sources) and by the same code/name-list being applied to all anchors and negatives.")
    notes.append(
        f"GATE-C4 (M-CERT-BODY-VARIABLE>=3): {'PASS' if gate_c4_ok else 'FAIL -> NO-BODY-VARIATION branch'}.")
    notes.append(
        "Raw bodies retained per record under raw/bodies/; raw/records.jsonl carries timestamp, final "
        "URL, status, headers of interest, body_sha256, storage path, jar digest, neutral detector names.")
    return notes


def _unresolved(branch, d1v, agree_valueset, agree_verdict):
    return [
        "Whether the parent's 4/5 zero-distinct-value gate-0 failure generalizes beyond these four "
        "anchors to the broader credential-free server-rendered Web. CC-A forbids prevalence claims.",
        "Whether the auth.wikimedia.org wpCreateaccountToken discrepancy is reproducible over time / "
        "from different egress networks; this run captures one date and one egress ASN.",
        f"Part (ii) status: {d1v['gate_b_branch']}; the value-aware channel's necessity on non-D1V "
        "drift families (permission-boundary change, SB-02) was not tested and remains open.",
        "The structurally invisible stale cell (M-INVISIBLE-STALE-PREV) and permission-boundary "
        "change remain permanently unmeasured by this design.",
        "Whether a value-blind guard operating point, prevalence or economic break-even follows; none "
        "is measured by this packet (CC-B).",
    ]


def _collect_artifacts():
    artifacts = []
    here = Path(__file__).resolve().parent
    for name in ["path_a_htmlparser.py", "path_b_regexlex.py", "neutral_detector.py",
                 "fixtures.py", "run_experiment.py"]:
        p = here / name
        artifacts.append({"path": str(p.relative_to(ROOT)), "sha256": sha256_file(p), "role": "code"})
    for p in sorted(BODY_DIR.rglob("*")):
        if p.is_file():
            artifacts.append({"path": str(p.relative_to(ROOT)), "sha256": sha256_file(p), "role": "raw"})
    for p in sorted(DERIVED_DIR.rglob("*")):
        if p.is_file():
            artifacts.append({"path": str(p.relative_to(ROOT)), "sha256": sha256_file(p), "role": "derived"})
    rj = RAW_DIR / "records.jsonl"
    if rj.exists():
        artifacts.append({"path": str(rj.relative_to(ROOT)), "sha256": sha256_file(rj), "role": "raw"})
    return artifacts


def _provenance(rec, attestation, raw_jsonl, verify_before):
    return {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "lane": LANE,
        "github_run_id": RUN_ID,
        "execution_start_utc": rec.records[0]["requested_at_utc"] if rec.records else None,
        "execution_end_utc": rec.records[-1]["requested_at_utc"] if rec.records else None,
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "working_directory": str(ROOT),
            "stdlib_only": True,
            "dependencies": ["urllib.request", "http.cookiejar", "html.parser", "re", "ast",
                             "hashlib", "json", "random", "statistics", "time"],
            "no_browser": True, "no_js": True, "no_credentials": True,
            "no_write_verbs": True, "no_model_calls": True, "no_docker": True,
        },
        "frozen_inputs_verification": verify_before,
        "source_files": _collect_artifacts(),
        "path_independence_attestation": attestation,
        "request_count": rec.request_count,
        "request_cap": REQUEST_CAP,
        "pacing_seconds": PACING_SECONDS,
        "seed": FROZEN_SEED,
        "user_agent": USER_AGENT,
        "raw_records_path": str(raw_jsonl.relative_to(ROOT)),
        "written_scope_assertion": (
            "Writes were confined to research/experiments/EXP-GRAPH-37950584469/ and "
            "research/graph/freshness_detection/exp_37950584469/."
        ),
    }


def _write_report(result, report_extra):
    am = report_extra["anchor_metrics"]
    lines = []
    lines.append(f"# EXP-GRAPH-37950584469 — EXECUTE report\n")
    lines.append(f"Lane: `graph` · Status: **{result['status']}** · Outcome: **{result['outcome']}** · Branch: **{result['branch']}**\n")
    lines.append("This report explains `result.json`; it does not exceed the frozen claim or silently "
                 "contradict the canonical JSON. RAW EVIDENCE (`raw/`), OBSERVATIONS and DERIVED "
                 "MEASUREMENTS (`result.json`) are kept distinct from INTERPRETATION (this section).\n")
    lines.append("## 1. What was run\n")
    lines.append(f"- Frozen anchor set: CAL-POS-1..4 positive, CAL-NEG-1..4 negative; CAL-POS-5 retired. "
                 f"K=4 disjoint-cookie-jar sessions (S1 recorded, S2–S4 current) plus 2 warm-jar re-captures "
                 f"per positive anchor. Total requests: {report_extra['record_count']} (cap 200).")
    lines.append("- Two independently written stdlib extraction paths: `P-EXTRACT-A` (html.parser) and "
                 "`P-EXTRACT-B` (regex/lexer with hand-written entity decoder). Same byte-identical bodies to both.")
    lines.append("- GATE C (substrate certificate) → GATE E (instrument + E3 extraction agreement) → "
                 "D1/D2/D3 anchor verdicts → conditional GATE B (value-only-rotation blindness).\n")
    lines.append("## 2. Certificate and instrument gates\n")
    lines.append(f"- GATE-C1 (`M-CERT-ROUTE-OK`, `M-CERT-FIELD-PRESENT`): "
                 f"{result['metrics']['M-CERT-ROUTE-OK']['value']}/4, "
                 f"{result['metrics']['M-CERT-FIELD-PRESENT']['value']}/4.")
    lines.append(f"- GATE-C2 (`M-CERT-NEG-VALUES-A/B`): "
                 f"{result['metrics']['M-CERT-NEG-VALUES-A']['value']}/"
                 f"{result['metrics']['M-CERT-NEG-VALUES-B']['value']}.")
    lines.append(f"- GATE-C3 session isolation: {result['controls']['NC-SESSION-ISOLATION']['result']}.")
    lines.append(f"- GATE-C4 body variation: {result['controls']['GATE-C4']['result']}.")
    lines.append(f"- GATE-E1 canary: M-CANARY-PASS={result['metrics']['M-CANARY-PASS']['value']}; "
                 f"GATE-E2 fixtures/path-independence: {result['controls']['GATE-E2']['result']}; "
                 f"GATE-E3 agreement: {result['controls']['GATE-E3']['result']}.\n")
    lines.append("## 3. Per-anchor extraction verdicts\n")
    lines.append("| anchor | verdict_A | distinct_A | verdict_B | distinct_B | route_ok | distinct_body |")
    lines.append("|---|---|---|---|---|---|---|")
    for a in ["CAL-POS-1", "CAL-POS-2", "CAL-POS-3", "CAL-POS-4"]:
        lines.append(f"| {a} | {am[a]['A']['verdict']} | {am[a]['A']['distinct_values']} | "
                     f"{am[a]['B']['verdict']} | {am[a]['B']['distinct_values']} | "
                     f"{am[a]['A']['route_ok']}/4 | {am[a]['A']['distinct_body']}/4 |")
    lines.append("")
    lines.append("## 4. Falsifiers reached and decision\n")
    lines.append(f"- Branch `{result['branch']}`; falsifier flags recorded under `controls`.")
    d1v = report_extra["d1v"]
    lines.append(f"- Part (ii): M-N-D1V={d1v['M-N-D1V']}, M-N-DECISIONS-D1V={d1v['M-N-DECISIONS-D1V']}, "
                 f"M-FA-INCUMBENT-D1V={d1v['M-FA-INCUMBENT-D1V']}, "
                 f"M-FA-VALUEAWARE-D1V={d1v['M-FA-VALUEAWARE-D1V']}, "
                 f"M-PAIRED-FA-DIFF-D1V={d1v['M-PAIRED-FA-DIFF-D1V']}, "
                 f"low={d1v['M-PAIRED-FA-DIFF-D1V-LOW']}, gate_b_branch={d1v['gate_b_branch']}.\n")
    lines.append("## 5. Interpretation (bounded)\n")
    lines.append("Any interpretation here is bounded by CC-A..CC-F. No prevalence over 'the Web' is claimed, "
                 "no guard operating point is measured, and nothing is promoted into Product Core. "
                 "`M-INVISIBLE-STALE-PREV` is null, never 0.0.\n")
    lines.append("## 6. Provenance and raw evidence\n")
    lines.append("- Raw records: `raw/records.jsonl`; raw bodies: `raw/bodies/<anchor>/<session>_<phase>.html`; "
                 "derived extraction: `derived/extraction.jsonl`; code: "
                 "`research/graph/freshness_detection/exp_37950584469/`.")
    (EXP_DIR / "report.md").write_text("\n".join(lines) + "\n")


def _emit_failure(message, detail):
    failure = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "lane": LANE,
        "stage": "execute",
        "category": "frozen-input-verification",
        "message": message,
        "detail": detail,
        "retryable": False,
    }
    (EXP_DIR / "failure.json").write_text(json.dumps(failure, indent=2) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
