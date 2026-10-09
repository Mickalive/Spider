#!/usr/bin/env python3
"""EXECUTE runner for EXP-GRAPH-37964565784 (graph lane, C-FRESHNESS).

Frozen two-arm transaction over one instrument and one frozen anchor set:

PART I  - replicate the parent's blocked read with the GATE-C3 session-isolation
          predicate REPAIRED at design time (audit required_fixes[0]); licensed
          outcome D1 EXTRACTION-DEFECT-CONFIRMED requires GATE E3 PASS and
          M-N-SESSION-SCOPED-CONFIRMED >= 3 of 4.
PART II - the mandate's explicit false-accept bound: repaired trial construction
          (all recorded/current session pairs; occurrence-count-stable AGSI
          instances) reads the incumbent value-blind guard vs the value-aware
          guard on real value-only rotation (D1V), anchor-clustered.

RAW EVIDENCE -> raw/.  DERIVED MEASUREMENTS -> derived/ + result.json.
INTERPRETATION -> report.md only.

Stdlib only (urllib, http.cookiejar, html.parser, re, ast, hashlib, json,
random, math, statistics).  No browser, no JS, no credentials, no write verb.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
import os
import platform
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.cookiejar import CookieJar
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import fixtures  # noqa: E402
import guard  # noqa: E402
import neutral_detector  # noqa: E402
import path_a_htmlparser as path_a  # noqa: E402
import path_b_regexlex as path_b  # noqa: E402

EXP_ID = "EXP-GRAPH-37964565784"
LANE = "graph"
RUN_ID = os.environ.get("GITHUB_RUN_ID", "37964565784")
FROZEN_SEED = 37964565784

# HERE=.../research/experiments/EXP-GRAPH-37964565784/code
#   parents[0]=EXP dir, [1]=experiments, [2]=research, [3]=repo root
ROOT = HERE.parents[3]
EXP_DIR = ROOT / "research" / "experiments" / EXP_ID
RAW_DIR = EXP_DIR / "raw"
BODY_DIR = RAW_DIR / "bodies"
DERIVED_DIR = EXP_DIR / "derived"

USER_AGENT = f"SPIDER-Research/2.0 (graph-lane; experiment {EXP_ID}; +https://spider-research.dev)"
PACING_SECONDS = 2.0
REQUEST_CAP = 200

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
ALL_ANCHORS = POSITIVE_ANCHORS + NEGATIVE_ANCHORS
SESSIONS = ["S1", "S2", "S3", "S4"]
TRANSPORT_HEADERS = ["ETag", "Last-Modified", "Cache-Control", "Vary"]
FROZEN_FILES = ["request.json", "spec.json", "prereg.md"]
FREEZE = json.loads((EXP_DIR / "freeze.json").read_text())

CONSTANT_CONFIG_ALLOWLIST = [
    "preferred_language",
    "GeoIP",
    "NetworkProbeLimit",
    "WMF-Last-Access",
    "WMF-Last-Access-Global",
    "CentralAuthAnonTopLevel",
]

BODY_MAX = 300_000  # per-body storage guard; anchors observed < 120 KB


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def percentile(sorted_vals, q):
    if not sorted_vals:
        return None
    idx = int((q / 100.0) * len(sorted_vals))
    idx = max(0, min(len(sorted_vals) - 1, idx))
    return sorted_vals[idx]


def wilson_interval(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return [round(max(0.0, center - half), 6), round(min(1.0, center + half), 6)]


# ---------------------------------------------------------------------------
# frozen-input verification (V11)
# ---------------------------------------------------------------------------
def verify_frozen_inputs(tag):
    results = {}
    ok = True
    for name in FROZEN_FILES:
        actual = sha256_file(EXP_DIR / name)
        expected = FREEZE["hashes"][name]
        match = actual == expected
        ok = ok and match
        results[name] = {"expected": expected, "actual": actual, "match": match, "when": tag}
    return ok, results


# ---------------------------------------------------------------------------
# capture
# ---------------------------------------------------------------------------
class Recorder:
    def __init__(self):
        self.records = []
        self.host_last_request = {}
        self.request_count = 0

    def _pace(self, host):
        last = self.host_last_request.get(host)
        if last is not None:
            wait = PACING_SECONDS - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
        self.host_last_request[host] = time.time()

    def capture(self, anchor_id, url, session, jar, phase="fresh", warm_index=None):
        host = urllib.parse.urlparse(url).hostname
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
            with opener.open(req, timeout=40) as resp:
                status = resp.status
                final_url = resp.geturl()
                body = resp.read(BODY_MAX + 1)
                resp_headers = {k: v for k, v in resp.headers.items()}
        except urllib.error.HTTPError as exc:
            status = exc.code
            final_url = exc.geturl()
            try:
                body = exc.read(BODY_MAX + 1)
            except Exception:
                body = b""
            resp_headers = {k: v for k, v in exc.headers.items()} if exc.headers else {}
            error = f"HTTPError:{exc.code}"
        except Exception as exc:  # noqa: BLE001
            error = f"{type(exc).__name__}:{exc}"
        elapsed = time.time() - t0

        hdr_lower = {k.lower(): v for k, v in resp_headers.items()}
        headers_of_interest = {
            k: hdr_lower.get(k.lower())
            for k in TRANSPORT_HEADERS + ["Content-Type", "Content-Length", "Server"]
        }
        headers_of_interest["Set-Cookie-Count"] = sum(
            1 for k in resp_headers if k.lower() == "set-cookie"
        )
        record = {
            "anchor_id": anchor_id,
            "url": url,
            "session": session,
            "phase": phase,
            "warm_index": warm_index,
            "requested_at_utc": requested_at,
            "final_url": final_url,
            "status": status,
            "error": error,
            "elapsed_s": round(elapsed, 3),
            "headers": headers_of_interest,
            "body_sha256": sha256_bytes(body) if body else None,
            "body_len": len(body),
            "body_path": None,
            "neutral_in_list_names": neutral_detector.find_in_list_names(body) if body else [],
            "jar_was_empty_before_request": jar_was_empty,
            "request_count": self.request_count,
            "cookie_jar_digest": jar_digest(jar),
            "cookies_after": sorted([[c.domain, c.path, c.name, c.value] for c in jar]),
        }
        self.records.append(record)
        return record, body


def jar_digest(jar):
    items = sorted([[c.domain, c.path, c.name, c.value] for c in jar])
    return sha256_bytes(json.dumps(items, separators=(",", ":")).encode("utf-8"))


def store_body(record, body, anchor_id, session, phase, warm_index):
    suffix = f"warm{warm_index}" if phase == "warm" else "fresh"
    path = BODY_DIR / anchor_id / f"{session}_{suffix}.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    record["body_path"] = str(path.relative_to(ROOT))


# ---------------------------------------------------------------------------
# path independence + no-anchor-special-casing (V03/V07/NC-PATH-INDEPENDENCE)
# ---------------------------------------------------------------------------
def path_independence_attestation():
    src_a = (HERE / "path_a_htmlparser.py").read_text()
    src_b = (HERE / "path_b_regexlex.py").read_text()
    src_n = (HERE / "neutral_detector.py").read_text()
    src_g = (HERE / "guard.py").read_text()

    tree_b = ast.parse(src_b)
    imports_b = []
    for node in ast.walk(tree_b):
        if isinstance(node, ast.Import):
            imports_b.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports_b.append(node.module or "")
    forbidden = sorted({m for m in imports_b if "path_a" in m or m == "html"})

    anchor_tokens = [
        "gitlab", "wikimedia", "wikipedia", "discourse", "iana", "jsdelivr",
        "debian", "httpbin", "CAL-POS", "CAL-NEG",
    ]
    all_src = src_a + src_b + src_n + src_g
    hosts_found = sorted({t for t in anchor_tokens if t in all_src})

    def agree(body):
        return pair_set(path_a.extract(body)) == pair_set(path_b.extract(body))

    original = fixtures.SYN_CANARY_BOTH
    perturbed = bytearray(original)
    idx = original.index(b"fixture-canary-value-7f3a")
    perturbed[idx] = ord("F") if perturbed[idx] != ord("F") else ord("f")
    perturbation_invariant = agree(original) == agree(bytes(perturbed))

    pass_ = (
        sha256_bytes(src_a.encode()) != sha256_bytes(src_b.encode())
        and len(forbidden) == 0
        and len(hosts_found) == 0
        and perturbation_invariant
    )
    return {
        "path_a_sha256": sha256_bytes(src_a.encode()),
        "path_b_sha256": sha256_bytes(src_b.encode()),
        "source_hashes_differ": sha256_bytes(src_a.encode()) != sha256_bytes(src_b.encode()),
        "path_b_imports": sorted(imports_b),
        "path_b_forbidden_imports": forbidden,
        "anchor_host_tokens_found_in_producer_sources": hosts_found,
        "no_anchor_special_casing": len(hosts_found) == 0,
        "perturbation_invariant": perturbation_invariant,
        "path_independence_pass": pass_,
    }


def pair_set(records):
    return {(r["field_name"], r["value"]) for r in records if r["state"] == "VALUE"}


def field_states(records):
    return sorted({(r["field_name"], r["state"]) for r in records})


# ---------------------------------------------------------------------------
# fixtures (V08)
# ---------------------------------------------------------------------------
def run_fixtures():
    a_c = path_a.extract(fixtures.SYN_CANARY_BOTH)
    b_c = path_b.extract(fixtures.SYN_CANARY_BOTH)
    expected = {("authenticity_token", "fixture-canary-value-7f3a"),
                ("csrf-token", "fixture-meta-canary-91bd")}
    canary_pass = pair_set(a_c) == expected and pair_set(b_c) == expected

    a_e = path_a.extract(fixtures.SYN_EMPTY_VALUE)
    b_e = path_b.extract(fixtures.SYN_EMPTY_VALUE)
    empty_agree = (
        field_states(a_e) == field_states(b_e)
        and field_states(a_e) == [("authenticity_token", "PRESENT_EMPTY"),
                                  ("csrf-token", "PRESENT_EMPTY")]
    )

    a_j = path_a.extract(fixtures.SYN_JSSTRING)
    b_j = path_b.extract(fixtures.SYN_JSSTRING)
    js_values = len(pair_set(a_j)) + len(pair_set(b_j))

    guard_results = {}
    guard_fixture_pass = True
    for fid, fdef in fixtures.GUARD_FIXTURES.items():
        observed = {
            gid: guard.decide(gid, fdef["fired"])
            for gid in ["B-INCUMBENT-SIGNAL-ONLY", "B-VALUE-AWARE", "B-FULL-GUARD"]
        }
        ok = all(observed[gid] == exp for gid, exp in fdef["expected"].items())
        guard_fixture_pass = guard_fixture_pass and ok
        guard_results[fid] = {
            "fired": fdef["fired"],
            "expected": fdef["expected"],
            "observed": observed,
            "pass": ok,
        }

    return {
        "M-FIXTURE-CANARY-PASS": canary_pass,
        "M-FIXTURE-EMPTY-AGREE": empty_agree,
        "M-FIXTURE-JSSTRING-VALUES": js_values,
        "M-GUARD-FIXTURE-PASS": guard_fixture_pass,
        "guard_fixtures": guard_results,
        "canary_a_pairs": sorted(pair_set(a_c)),
        "canary_b_pairs": sorted(pair_set(b_c)),
        "empty_a_states": field_states(a_e),
        "empty_b_states": field_states(b_e),
        "js_a_values": sorted(pair_set(a_j)),
        "js_b_values": sorted(pair_set(b_j)),
    }


# ---------------------------------------------------------------------------
# repaired session isolation (V06 / GATE-C3)
# ---------------------------------------------------------------------------
def evaluate_isolation(first_cookieless, name_sets, pair_sets, sessions, allowlist):
    shared_names = set()
    for i in range(len(sessions)):
        for j in range(i + 1, len(sessions)):
            shared_names |= name_sets[sessions[i]] & name_sets[sessions[j]]
    const_shared = sorted(n for n in shared_names if n in allowlist)
    unexpected_shared = sorted(n for n in shared_names if n not in allowlist)
    filtered = {
        s: {(n, v) for (n, v) in pair_sets[s] if n not in allowlist}
        for s in sessions
    }
    disjoint_after = True
    for i in range(len(sessions)):
        for j in range(i + 1, len(sessions)):
            if filtered[sessions[i]] & filtered[sessions[j]]:
                disjoint_after = False
    session_id_disjoint = len(unexpected_shared) == 0
    pass_ = bool(first_cookieless and session_id_disjoint and disjoint_after)
    return {
        "first_request_cookieless": bool(first_cookieless),
        "constconfig_shared_names": const_shared,
        "unexpected_shared_names": unexpected_shared,
        "session_identifying_disjoint": session_id_disjoint,
        "pairwise_disjoint_on_name_value_after_filter": disjoint_after,
        "pass": pass_,
    }


def session_isolation(records, jars):
    per_anchor = {}
    ok_all = True
    for anchor_id, _ in ALL_ANCHORS:
        name_sets, pair_sets, first_ok = {}, {}, True
        for s in SESSIONS:
            jar = jars.get((anchor_id, s))
            if jar is None:
                first_ok = False
                name_sets[s], pair_sets[s] = set(), set()
                continue
            name_sets[s] = {c.name for c in jar}
            pair_sets[s] = {(c.name, c.value) for c in jar}
            rec = next((r for r in records if r["anchor_id"] == anchor_id
                        and r["session"] == s and r["phase"] == "fresh"), None)
            if rec is None or not rec["jar_was_empty_before_request"]:
                first_ok = False
        res = evaluate_isolation(first_ok, name_sets, pair_sets, SESSIONS,
                                 CONSTANT_CONFIG_ALLOWLIST)
        res["jar_sizes"] = {s: len(name_sets[s]) for s in SESSIONS}
        per_anchor[anchor_id] = res
        ok_all = ok_all and res["pass"]
    return {"pass": ok_all, "per_anchor": per_anchor}


def constconfig_exclusion_not_vacuous():
    """NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS: a shared session-identifying name
    (_gitlab_session) alongside an allowlisted constant must FAIL the predicate.
    A predicate that passes this fixture is vacuous."""
    sessions = ["S1", "S2"]
    name_sets = {
        "S1": {"preferred_language", "_gitlab_session"},
        "S2": {"preferred_language", "_gitlab_session"},
    }
    pair_sets = {
        "S1": {("preferred_language", "en"), ("_gitlab_session", "abc")},
        "S2": {("preferred_language", "en"), ("_gitlab_session", "def")},
    }
    res = evaluate_isolation(True, name_sets, pair_sets, sessions, CONSTANT_CONFIG_ALLOWLIST)
    # Control: the same pair WITHOUT the session-identifying name must PASS.
    name_sets2 = {"S1": {"preferred_language"}, "S2": {"preferred_language"}}
    pair_sets2 = {"S1": {("preferred_language", "en")}, "S2": {("preferred_language", "en")}}
    res2 = evaluate_isolation(True, name_sets2, pair_sets2, sessions, CONSTANT_CONFIG_ALLOWLIST)
    return {
        "shared_session_identifying_name_fails": (res["pass"] is False
                                                   and res["unexpected_shared_names"] == ["_gitlab_session"]),
        "allowlisted_only_passes": res2["pass"] is True,
        "not_vacuous": (res["pass"] is False and res2["pass"] is True),
        "fixture_fail_observed": res,
        "fixture_pass_observed": res2,
    }


# ---------------------------------------------------------------------------
# extraction aggregation
# ---------------------------------------------------------------------------
def structure_signature(r):
    return (r["type_class"], r["form_action"], r["form_method"],
            tuple(r["form_input_names"]))


def normalize(records):
    counters = {}
    out = []
    for r in records:
        fn = r["field_name"]
        o = counters.get(fn, 0)
        counters[fn] = o + 1
        nr = dict(r)
        nr["occurrence_ordinal"] = o
        nr["structure_signature"] = list(structure_signature(r))
        out.append(nr)
    return out


def index_slots(records):
    """(field_name, occurrence_ordinal) -> record for one session."""
    slots = {}
    for r in records:
        slots[(r["field_name"], r["occurrence_ordinal"])] = r
    return slots


def anchor_path_metrics(per_session_records, headers_by_session, body_shas):
    all_values = set()
    extracted_sessions = 0
    for recs in per_session_records.values():
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
    field_value_sets = {}
    for recs in per_session_records.values():
        for r in recs:
            field_value_sets.setdefault(r["field_name"], set()).add((r["state"], r["value"]))
    return {
        "distinct_values": len(all_values),
        "extract_rate": extracted_sessions / len(SESSIONS),
        "verdict": verdict,
        "route_ok": route_ok,
        "distinct_body": distinct_body,
        "field_value_sets": field_value_sets,
        "all_values": sorted(all_values),
    }


def kappa(pairs):
    n = len(pairs)
    if n == 0:
        return None
    a = [p[0] for p in pairs]
    b = [p[1] for p in pairs]
    po = sum(1 for x, y in pairs if x == y) / n
    pa1, pb1 = sum(a) / n, sum(b) / n
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    if pe == 1.0:
        return None
    return (po - pe) / (1 - pe)


# ---------------------------------------------------------------------------
# trial construction and guard statistics (PART II)
# ---------------------------------------------------------------------------
def transport_signature(header_record):
    h = header_record.get("headers", {}) if header_record else {}
    cc = h.get("Cache-Control") or ""
    m = re.search(r"max-age\s*=\s*(\d+)", cc, re.I)
    max_age = m.group(1) if m else None
    return (h.get("ETag"), h.get("Last-Modified"), max_age, h.get("Vary"),
            header_record.get("final_url") if header_record else None)


def session_field_name_set(records):
    return tuple(sorted({r["field_name"] for r in records}))


def build_population(path_data, records):
    """path_data: {anchor: {session: [normalized records]}}.
    Returns included keys, excluded keys, realized trials (all pairs)."""
    per_anchor = {}
    included_keys = set()
    excluded_keys = set()
    for anchor_id, _ in POSITIVE_ANCHORS:
        sessions_slots = {s: index_slots(path_data[anchor_id][s]) for s in SESSIONS}
        counts = {}
        for s in SESSIONS:
            for (fn, _o) in sessions_slots[s]:
                counts.setdefault(fn, {})[s] = counts.setdefault(fn, {}).get(s, 0) + 1
        stable_fields, unstable_fields = [], []
        for fn, cnt in counts.items():
            vals = [cnt.get(s, 0) for s in SESSIONS]
            if len(set(vals)) == 1:
                stable_fields.append(fn)
            else:
                unstable_fields.append(fn)
        for fn in stable_fields:
            n = counts[fn][SESSIONS[0]]
            for o in range(n):
                included_keys.add((anchor_id, fn, o))
        for fn in unstable_fields:
            excluded_keys.add((anchor_id, fn))
        per_anchor[anchor_id] = {
            "sessions_slots": sessions_slots,
            "stable_fields": stable_fields,
            "unstable_fields": unstable_fields,
        }

    trials = []
    for r in range(len(SESSIONS)):
        for c in range(r + 1, len(SESSIONS)):
            sr, sc = SESSIONS[r], SESSIONS[c]
            for anchor_id, _ in POSITIVE_ANCHORS:
                pa = per_anchor[anchor_id]
                hdr_r = next((x for x in records if x["anchor_id"] == anchor_id
                              and x["session"] == sr and x["phase"] == "fresh"), None)
                hdr_c = next((x for x in records if x["anchor_id"] == anchor_id
                              and x["session"] == sc and x["phase"] == "fresh"), None)
                tsig_r, tsig_c = transport_signature(hdr_r), transport_signature(hdr_c)
                fset_r = session_field_name_set(path_data[anchor_id][sr])
                fset_c = session_field_name_set(path_data[anchor_id][sc])
                for key in sorted(included_keys):
                    if key[0] != anchor_id:
                        continue
                    rec = pa["sessions_slots"][sr].get((key[1], key[2]))
                    cur = pa["sessions_slots"][sc].get((key[1], key[2]))
                    if rec is None or cur is None:
                        continue
                    if rec["state"] != "VALUE" or cur["state"] != "VALUE":
                        continue
                    structural = tuple(rec["structure_signature"]) != tuple(cur["structure_signature"])
                    transport = tsig_r != tsig_c
                    postcond = fset_r != fset_c
                    endpoint = rec["form_action"] != cur["form_action"]
                    recorded, live = rec["value"], cur["value"]
                    fired = {
                        "CH-STRUCT-SIG": structural,
                        "CH-TRANSPORT-VALIDATOR": transport,
                        "CH-POSTCOND-SEM": postcond,
                        "CH-PRECOND-BINDING": live != recorded,
                    }
                    trials.append({
                        "anchor_id": anchor_id,
                        "field_name": key[1],
                        "occurrence_ordinal": key[2],
                        "recorded_session": sr,
                        "current_session": sc,
                        "recorded_value": recorded,
                        "live_value": live,
                        "label": "STALE" if live != recorded else "FRESH",
                        "structural_change": structural,
                        "endpoint_change": endpoint,
                        "transport_change": transport,
                        "postcond_change": postcond,
                        "fired": fired,
                        "B-INCUMBENT-SIGNAL-ONLY": guard.decide("B-INCUMBENT-SIGNAL-ONLY", fired),
                        "B-VALUE-AWARE": guard.decide("B-VALUE-AWARE", fired),
                        "B-FULL-GUARD": guard.decide("B-FULL-GUARD", fired),
                        "B-NO-GUARD-REPLAY": guard.decide("B-NO-GUARD-REPLAY", fired),
                    })
    return included_keys, excluded_keys, trials, per_anchor


def guard_statistics(trials, path_label):
    all_stale = [t for t in trials if t["label"] == "STALE"]
    all_fresh = [t for t in trials if t["label"] == "FRESH"]
    d1v = [t for t in trials
           if t["label"] == "STALE" and not t["structural_change"] and not t["transport_change"]]

    def rate(ts, guard_id, decision):
        if not ts:
            return None
        return sum(1 for t in ts if t[guard_id] == decision) / len(ts)

    fa_inc = rate(d1v, "B-INCUMBENT-SIGNAL-ONLY", "REUSE")
    fa_va = rate(d1v, "B-VALUE-AWARE", "REUSE")
    diff = None if (fa_inc is None or fa_va is None) else fa_inc - fa_va

    # non-degeneracy over ALL realized trials
    ch_names = guard.CHANNELS
    ch_fire = {c: 0 for c in ch_names}
    ch_not = {c: 0 for c in ch_names}
    ch_input_varied = {c: False for c in ch_names}
    for t in trials:
        for c in ch_names:
            if t["fired"][c]:
                ch_fire[c] += 1
            else:
                ch_not[c] += 1
    # activation input varied checks
    struct_variants, trans_variants, post_variants, value_variants = set(), set(), set(), set()
    for t in trials:
        struct_variants.add((t["anchor_id"], t["structural_change"]))
        trans_variants.add((t["anchor_id"], t["transport_change"]))
        post_variants.add((t["anchor_id"], t["postcond_change"]))
        value_variants.add((t["anchor_id"], t["recorded_value"] != t["live_value"]))
    ch_input_varied["CH-STRUCT-SIG"] = any(v for _, v in struct_variants)
    ch_input_varied["CH-TRANSPORT-VALIDATOR"] = any(v for _, v in trans_variants)
    ch_input_varied["CH-POSTCOND-SEM"] = any(v for _, v in post_variants)
    ch_input_varied["CH-PRECOND-BINDING"] = any(v for _, v in value_variants)
    channels = {}
    all_ok = True
    for c in ch_names:
        if not ch_input_varied[c]:
            channels[c] = {"status": "INACTIVE-ON-POPULATION", "fire": ch_fire[c],
                           "not_fire": ch_not[c], "waived": True}
        else:
            ok = ch_fire[c] > 0 and ch_not[c] > 0
            channels[c] = {"status": "ACTIVE", "fire": ch_fire[c],
                           "not_fire": ch_not[c], "waived": False, "satisfied": ok}
            all_ok = all_ok and ok

    decisions_d1v = sorted({t["B-INCUMBENT-SIGNAL-ONLY"] for t in d1v}
                           | {t["B-VALUE-AWARE"] for t in d1v})
    n_d1v = len(d1v)
    nondegenerate = (n_d1v >= 6) and (len(decisions_d1v) >= 2) and all_ok

    # anchor-clustered bootstrap on D1V
    anchors = sorted({t["anchor_id"] for t in d1v})
    fa_inc_ub = fa_va_ub = diff_low = diff_ub = None
    if anchors and n_d1v:
        by_anchor = {a: [t for t in d1v if t["anchor_id"] == a] for a in anchors}
        rng = random.Random(FROZEN_SEED)
        inc_dist, va_dist, diff_dist = [], [], []
        for _ in range(10000):
            sample = [rng.choice(anchors) for _ in range(len(anchors))]
            pooled = [t for a in sample for t in by_anchor[a]]
            if not pooled:
                continue
            pi = sum(1 for t in pooled if t["B-INCUMBENT-SIGNAL-ONLY"] == "REUSE") / len(pooled)
            pv = sum(1 for t in pooled if t["B-VALUE-AWARE"] == "REUSE") / len(pooled)
            inc_dist.append(pi)
            va_dist.append(pv)
            diff_dist.append(pi - pv)
        inc_dist.sort(); va_dist.sort(); diff_dist.sort()
        fa_inc_ub = percentile(inc_dist, 97.5)
        fa_va_ub = percentile(va_dist, 97.5)
        diff_low = percentile(diff_dist, 2.5)
        diff_ub = percentile(diff_dist, 97.5)

    # trialled diagnostic unclustered intervals (do-not-use for gates)
    k_inc = sum(1 for t in d1v if t["B-INCUMBENT-SIGNAL-ONLY"] == "REUSE")
    k_va = sum(1 for t in d1v if t["B-VALUE-AWARE"] == "REUSE")
    diag = {
        "M-DIAGNOSTIC-UNCLUSTERED-FA-INCUMBENT-D1V": {
            "value": wilson_interval(k_inc, n_d1v), "unit": "fraction CI",
            "do_not_use": True, "reason": "trial-level unclustered interval; V12 forbids using it for any gate"},
        "M-DIAGNOSTIC-UNCLUSTERED-FA-VALUEAWARE-D1V": {
            "value": wilson_interval(k_va, n_d1v), "unit": "fraction CI",
            "do_not_use": True, "reason": "trial-level unclustered interval; V12 forbids using it for any gate"},
    }

    n_decisions = len(decisions_d1v)
    if n_d1v < 6 or n_decisions < 2 or not nondegenerate:
        gate_b = "DATA-INSUFFICIENT-D1V"
    elif diff is not None and diff >= 0.10 and diff_low is not None and diff_low > 0:
        gate_b = "INCUMBENT-BLIND-CONFIRMED"
    else:
        gate_b = "INCUMBENT-NOT-BLIND"

    return {
        "path": path_label,
        "gate_b_branch": gate_b,
        "M-N-TRIALS": len(trials),
        "M-N-FRESH": len(all_fresh),
        "M-N-D1V": n_d1v,
        "M-N-D1V-ANCHORS": len(anchors),
        "M-N-STRUCT-DRIFT": sum(1 for t in trials if t["structural_change"]),
        "M-N-ENDPOINT-DRIFT": sum(1 for t in trials if t["endpoint_change"]),
        "M-N-TRANSPORT-DRIFT": sum(1 for t in trials if t["transport_change"]),
        "M-N-POSTCOND-DRIFT": sum(1 for t in trials if t["postcond_change"]),
        "M-FA-INCUMBENT-D1V": fa_inc,
        "M-FA-INCUMBENT-D1V-UB97": fa_inc_ub,
        "M-FA-VALUEAWARE-D1V": fa_va,
        "M-FA-VALUEAWARE-D1V-UB97": fa_va_ub,
        "M-PAIRED-FA-DIFF-D1V": diff,
        "M-PAIRED-FA-DIFF-D1V-LOW": diff_low,
        "M-PAIRED-FA-DIFF-D1V-UB97": diff_ub,
        "M-FA-INCUMBENT-ALL": rate(all_stale, "B-INCUMBENT-SIGNAL-ONLY", "REUSE"),
        "M-FA-VALUEAWARE-ALL": rate(all_stale, "B-VALUE-AWARE", "REUSE"),
        "M-FR-INCUMBENT-FRESH": rate(all_fresh, "B-INCUMBENT-SIGNAL-ONLY", "ABSTAIN"),
        "M-FR-VALUEAWARE-FRESH": rate(all_fresh, "B-VALUE-AWARE", "ABSTAIN"),
        "M-N-DECISIONS-D1V": n_decisions,
        "decisions_d1v": decisions_d1v,
        "channels": channels,
        "nondegenerate": nondegenerate,
        "anchors_with_d1v": anchors,
        "d1v_trial_examples": d1v[:12],
        "diagnostics": diag,
        "_all_trials_n": len(trials),
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    for d in (RAW_DIR, BODY_DIR, DERIVED_DIR):
        d.mkdir(parents=True, exist_ok=True)

    verify_ok_before, verify_before = verify_frozen_inputs("before")
    if not verify_ok_before:
        write_failure("V11 frozen-input verification failed before first request", verify_before)
        return 2

    # provenance: frozen-input re-verification of the codex dependency
    codex_dep = ROOT / "codex/experiments/EXP-FRONTIER-36306528608/raw/token_stability.jsonl"
    codex_dep_present = codex_dep.exists()
    codex_dep_sha = sha256_file(codex_dep) if codex_dep_present else None

    attestation = path_independence_attestation()
    fixtures_result = run_fixtures()
    nv = constconfig_exclusion_not_vacuous()

    rec = Recorder()
    jars, bodies = {}, {}

    # fresh captures, session-major
    for session in SESSIONS:
        for anchor_id, url in ALL_ANCHORS:
            jar = CookieJar()
            jars[(anchor_id, session)] = jar
            record, body = rec.capture(anchor_id, url, session, jar)
            bodies[(anchor_id, session)] = body
            store_body(record, body, anchor_id, session, "fresh", None)

    # warm-jar diagnostic: 2 same-jar re-captures per positive anchor from S4
    warm_bodies = {}
    for anchor_id, url in POSITIVE_ANCHORS:
        jar = jars[(anchor_id, "S4")]
        for wi in (1, 2):
            record, body = rec.capture(anchor_id, url, "S4", jar, phase="warm", warm_index=wi)
            warm_bodies[(anchor_id, wi)] = body
            store_body(record, body, anchor_id, "S4", "warm", wi)

    raw_jsonl = RAW_DIR / "records.jsonl"
    with raw_jsonl.open("w") as fh:
        for r in rec.records:
            fh.write(json.dumps(r, sort_keys=True) + "\n")

    isolation = session_isolation(rec.records, jars)

    # extraction over positives and negatives (byte-identical stored bodies)
    ext_a = {a: {s: path_a.extract(bodies[(a, s)]) for s in SESSIONS} for a, _ in POSITIVE_ANCHORS}
    ext_b = {a: {s: path_b.extract(bodies[(a, s)]) for s in SESSIONS} for a, _ in POSITIVE_ANCHORS}
    ext_a = {a: {s: normalize(ext_a[a][s]) for s in SESSIONS} for a, _ in POSITIVE_ANCHORS}
    ext_b = {a: {s: normalize(ext_b[a][s]) for s in SESSIONS} for a, _ in POSITIVE_ANCHORS}

    with (DERIVED_DIR / "extraction_A.jsonl").open("w") as fh:
        for a, _ in POSITIVE_ANCHORS:
            for s in SESSIONS:
                fh.write(json.dumps({"anchor_id": a, "session": s, "path": "A",
                                     "agsi": ext_a[a][s]}, sort_keys=True) + "\n")
    with (DERIVED_DIR / "extraction_B.jsonl").open("w") as fh:
        for a, _ in POSITIVE_ANCHORS:
            for s in SESSIONS:
                fh.write(json.dumps({"anchor_id": a, "session": s, "path": "B",
                                     "agsi": ext_b[a][s]}, sort_keys=True) + "\n")

    neg_vals = {}
    for a, _ in NEGATIVE_ANCHORS:
        va, vb = [], []
        for s in SESSIONS:
            body = bodies[(a, s)]
            va += [r for r in path_a.extract(body) if r["state"] == "VALUE"]
            vb += [r for r in path_b.extract(body) if r["state"] == "VALUE"]
        neg_vals[a] = {"A": [r["value"] for r in va], "B": [r["value"] for r in vb]}
    m_cert_neg_a = sum(len(v["A"]) for v in neg_vals.values())
    m_cert_neg_b = sum(len(v["B"]) for v in neg_vals.values())

    # GATE C metrics
    m_route = m_body = m_field = 0
    for a, _ in POSITIVE_ANCHORS:
        hdrs = {s: next(r for r in rec.records if r["anchor_id"] == a and r["session"] == s
                        and r["phase"] == "fresh") for s in SESSIONS}
        route_ok = sum(1 for s in SESSIONS if hdrs[s]["status"] == 200)
        if route_ok >= 3:
            m_route += 1
        bshas = [hdrs[s]["body_sha256"] for s in SESSIONS if hdrs[s]["body_sha256"]]
        if len(set(bshas)) >= 2:
            m_body += 1
        sess_field = sum(1 for s in SESSIONS if hdrs[s]["neutral_in_list_names"])
        if sess_field >= 3:
            m_field += 1

    gate_c1 = (m_route >= 3) and (m_field >= 3)
    gate_c2 = (m_cert_neg_a == 0) and (m_cert_neg_b == 0)
    gate_c3 = isolation["pass"] and nv["not_vacuous"]
    gate_c_pass = gate_c1 and gate_c2 and gate_c3
    gate_c4_ok = m_body >= 3

    # PART I: per-anchor path metrics and agreement
    anchor_metrics = {}
    m_agree_valueset = m_agree_verdict = 0
    m_ss = m_rl = m_unrel = 0
    kappa_pairs = []
    for a, _ in POSITIVE_ANCHORS:
        hdrs = {s: next(r for r in rec.records if r["anchor_id"] == a and r["session"] == s
                        and r["phase"] == "fresh") for s in SESSIONS}
        body_shas = {s: hdrs[s]["body_sha256"] for s in SESSIONS}
        ma = anchor_path_metrics(ext_a[a], hdrs, body_shas)
        mb = anchor_path_metrics(ext_b[a], hdrs, body_shas)
        anchor_metrics[a] = {"A": ma, "B": mb}
        if ma["field_value_sets"] == mb["field_value_sets"]:
            m_agree_valueset += 1
        if ma["verdict"] == mb["verdict"]:
            m_agree_verdict += 1
        if ma["verdict"] == mb["verdict"] == "RECOVERED_SESSION_SCOPED":
            m_ss += 1
        if (ma["verdict"] == mb["verdict"] and ma["verdict"] in ("RECOVERED_EMPTY", "NO_FIELD")):
            m_rl += 1
        if ma["verdict"] != mb["verdict"]:
            m_unrel += 1
        fields_union = set()
        for s in SESSIONS:
            fields_union |= {r["field_name"] for r in ext_a[a][s]}
            fields_union |= {r["field_name"] for r in ext_b[a][s]}
        for s in SESSIONS:
            for f in fields_union:
                pa = any(r["field_name"] == f and r["state"] == "VALUE" for r in ext_a[a][s])
                pb = any(r["field_name"] == f and r["state"] == "VALUE" for r in ext_b[a][s])
                kappa_pairs.append((pa, pb))
    m_kappa = kappa(kappa_pairs)

    canary_a = {r["value"] for s in SESSIONS for r in ext_a["CAL-POS-1"][s]
                if r["field_name"] == "authenticity_token" and r["state"] == "VALUE"}
    canary_b = {r["value"] for s in SESSIONS for r in ext_b["CAL-POS-1"][s]
                if r["field_name"] == "authenticity_token" and r["state"] == "VALUE"}
    m_canary = len(canary_a) >= 2 and len(canary_b) >= 2

    # PART II: trial construction on both paths
    incl_a, excl_a, trials_a, per_a = build_population(ext_a, rec.records)
    incl_b, excl_b, trials_b, per_b = build_population(ext_b, rec.records)
    trial_construction_stable = (incl_a == incl_b)
    guard_stats = guard_statistics(trials_a, "A")
    guard_stats_b = guard_statistics(trials_b, "B")

    with (DERIVED_DIR / "trials.jsonl").open("w") as fh:
        for t in trials_a:
            fh.write(json.dumps(t, sort_keys=True) + "\n")

    # warm-jar diagnostic
    warm_metrics = {}
    for a, _ in POSITIVE_ANCHORS:
        seq_fresh = [next(r for r in rec.records if r["anchor_id"] == a and r["session"] == "S4"
                          and r["phase"] == "fresh")]
        warm_recs = sorted([r for r in rec.records if r["anchor_id"] == a and r["phase"] == "warm"],
                           key=lambda r: r["warm_index"])
        seq = seq_fresh + warm_recs
        vals = []
        for r in seq:
            if r["phase"] == "fresh":
                b = bodies[(a, "S4")]
            else:
                b = warm_bodies[(a, r["warm_index"])]
            vals.append(tuple(sorted({x["value"] for x in path_a.extract(b) if x["state"] == "VALUE"})))
        body_seq = [bodies[(a, "S4")]] + [warm_bodies[(a, wi)] for wi in (1, 2)]
        denom = len(seq) - 1
        val_ch = sum(1 for i in range(1, len(vals)) if vals[i] != vals[i - 1])
        body_ch = sum(1 for i in range(1, len(body_seq))
                      if sha256_bytes(body_seq[i]) != sha256_bytes(body_seq[i - 1]))
        fresh_vals = [tuple(sorted({x["value"] for x in ext_a[a][s] if x["state"] == "VALUE"}))
                      for s in SESSIONS]
        fresh_ch = sum(1 for i in range(1, len(fresh_vals)) if fresh_vals[i] != fresh_vals[i - 1])
        wv = val_ch / denom if denom else None
        wb = body_ch / denom if denom else None
        fv = fresh_ch / (len(fresh_vals) - 1) if len(fresh_vals) > 1 else None
        if wv == 0 and fv == 0:
            ts = "NO_ROTATION"
        elif wv is not None and fv is not None and abs(wv - fv) <= 0.10:
            ts = "PER_REQUEST_SCALE"
        elif wv is not None and fv is not None and wv < fv - 0.10:
            ts = "SESSION_SCALE"
        else:
            ts = "UNDETERMINED"
        warm_metrics[a] = {"M-WARMJAR-VARIATION-RATE": wv,
                           "M-WARMJAR-BODY-VARIATION-RATE": wb,
                           "M-WARMJAR-FRESH-VALUE-VARIATION-RATE": fv,
                           f"M-ROTATION-TIMESCALE-{a}": ts}

    # decision rule
    gate_e1 = m_canary
    gate_e2 = (fixtures_result["M-FIXTURE-CANARY-PASS"]
               and fixtures_result["M-FIXTURE-EMPTY-AGREE"]
               and fixtures_result["M-FIXTURE-JSSTRING-VALUES"] == 0
               and fixtures_result["M-GUARD-FIXTURE-PASS"]
               and attestation["path_independence_pass"]
               and trial_construction_stable)
    gate_e3 = (m_agree_valueset >= 3) and (m_agree_verdict >= 3)
    if not gate_c_pass:
        status, outcome, branch = "MEASUREMENT_INVALID", "INCONCLUSIVE", "F-CERT"
    elif not gate_c4_ok:
        status, outcome, branch = "COMPLETE", "INCONCLUSIVE", "NO-BODY-VARIATION"
    elif not (gate_e1 and gate_e2):
        status, outcome, branch = "MEASUREMENT_INVALID", "INCONCLUSIVE", "F-INSTR"
    elif not gate_e3:
        status, outcome, branch = "COMPLETE", "MIXED", "EXTRACTION-UNRELIABLE"
    elif m_ss >= 3:
        status, outcome, branch = "COMPLETE", "SUPPORTS", "EXTRACTION-DEFECT-CONFIRMED"
    elif m_rl >= 3:
        status, outcome, branch = "COMPLETE", "FALSIFIES", "REPRESENTATION-LOSS-CONFIRMED"
    else:
        status, outcome, branch = "COMPLETE", "MIXED", "MIXED-ANCHORS"

    if branch == "EXTRACTION-DEFECT-CONFIRMED":
        gate_b_branch = guard_stats["gate_b_branch"]
    else:
        gate_b_branch = "NOT_READ_D1_NOT_REACHED"

    verify_ok_after, verify_after = verify_frozen_inputs("after")

    metrics = assemble_metrics(
        rec, isolation, m_route, m_body, m_field, m_cert_neg_a, m_cert_neg_b,
        anchor_metrics, m_agree_valueset, m_agree_verdict, m_kappa, m_canary,
        fixtures_result, m_ss, m_rl, m_unrel, warm_metrics,
        guard_stats, guard_stats_b, gate_b_branch, incl_a, excl_a, incl_b, excl_b,
        trials_a, neg_vals,
    )
    controls = assemble_controls(
        isolation, nv, attestation, fixtures_result, anchor_metrics, neg_vals,
        gate_c1, gate_c2, gate_c3, gate_c4_ok, gate_e1, gate_e2, gate_e3,
        m_canary, m_agree_valueset, m_agree_verdict, m_ss, m_rl, m_unrel,
        guard_stats, guard_stats_b, gate_b_branch, branch,
    )

    (DERIVED_DIR / "certificate.json").write_text(json.dumps({
        "M-CERT-ROUTE-OK": m_route, "M-CERT-BODY-VARIABLE": m_body,
        "M-CERT-FIELD-PRESENT": m_field,
        "M-CERT-SESSION-ISOLATION-PASS": isolation["pass"],
        "M-CERT-FIRST-REQUEST-COOKIELESS": all(
            v["first_request_cookieless"] for v in isolation["per_anchor"].values()),
        "M-CERT-SESSION-IDENTIFYING-DISJOINT": all(
            v["session_identifying_disjoint"] for v in isolation["per_anchor"].values()),
        "M-CERT-CONSTCONFIG-SHARED-NAMES": {a: v["constconfig_shared_names"]
                                            for a, v in isolation["per_anchor"].items()},
        "M-CERT-UNEXPECTED-SHARED-NAMES": {a: v["unexpected_shared_names"]
                                           for a, v in isolation["per_anchor"].items()},
        "M-CERT-NEG-VALUES-A": m_cert_neg_a, "M-CERT-NEG-VALUES-B": m_cert_neg_b,
        "per_anchor": isolation["per_anchor"],
        "NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS": nv,
    }, indent=2) + "\n")
    (DERIVED_DIR / "fixtures.json").write_text(json.dumps(fixtures_result, indent=2) + "\n")
    (DERIVED_DIR / "anchor_metrics.json").write_text(json.dumps(
        {a: {"A": {k: v for k, v in m["A"].items() if k != "field_value_sets"},
             "B": {k: v for k, v in m["B"].items() if k != "field_value_sets"}}
         for a, m in anchor_metrics.items()}, indent=2) + "\n")
    (DERIVED_DIR / "guard_stats.json").write_text(json.dumps(
        {"path_A": guard_stats, "path_B": guard_stats_b,
         "trial_construction_stable": trial_construction_stable,
         "included_keys_A": sorted(list(k) for k in incl_a),
         "included_keys_B": sorted(list(k) for k in incl_b)}, indent=2, default=str) + "\n")

    observations = build_observations(
        rec, isolation, anchor_metrics, neg_vals, fixtures_result, guard_stats,
        guard_stats_b, warm_metrics, m_canary, m_agree_valueset, m_agree_verdict,
        m_ss, m_rl, m_unrel, branch, gate_b_branch, trials_a, nv,
    )
    validity_notes = build_validity_notes(
        attestation, verify_ok_before, verify_ok_after, guard_stats, gate_c4_ok,
        m_body, codex_dep_present, codex_dep_sha,
    )
    unresolved = build_unresolved(branch, guard_stats, gate_b_branch, m_agree_valueset,
                                  m_agree_verdict, codex_dep_present)

    artifacts = collect_artifacts(
        raw_jsonl, bodies, warm_bodies, rec, guard_stats, verify_ok_before,
        verify_ok_after, codex_dep_present, codex_dep_sha,
    )

    result = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "branch": branch,
        "gate_b_branch": gate_b_branch,
        "claim_ids": ["C-FRESHNESS"],
        "metrics": metrics,
        "controls": controls,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
        "frozen_input_verification": {"before": verify_before, "after": verify_after},
    }
    (EXP_DIR / "result.json").write_text(json.dumps(result, indent=2, sort_keys=False) + "\n")

    provenance = build_provenance(rec, attestation, raw_jsonl, bodies, warm_bodies,
                                  verify_before, verify_after, codex_dep_present, codex_dep_sha)
    (EXP_DIR / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")

    write_report(result, anchor_metrics, neg_vals, guard_stats, guard_stats_b,
                 warm_metrics, isolation, nv, fixtures_result, attestation,
                 len(rec.records), m_cert_neg_a, m_cert_neg_b)

    print("STATUS", status, "OUTCOME", outcome, "BRANCH", branch)
    print("GATE_C", gate_c_pass, "C1", gate_c1, "C2", gate_c2, "C3", gate_c3, "C4", gate_c4_ok)
    print("GATE_E1", gate_e1, "GATE_E2", gate_e2, "GATE_E3", gate_e3)
    print("GATE_B", gate_b_branch)
    print("M-N-SESSION-SCOPED-CONFIRMED", m_ss, "M-N-D1V", guard_stats["M-N-D1V"],
          "M-N-DECISIONS-D1V", guard_stats["M-N-DECISIONS-D1V"])
    print("M-FA-INCUMBENT-D1V", guard_stats["M-FA-INCUMBENT-D1V"],
          "M-FA-VALUEAWARE-D1V", guard_stats["M-FA-VALUEAWARE-D1V"])
    print("requests", rec.request_count)
    return 0


# ---------------------------------------------------------------------------
# assembly
# ---------------------------------------------------------------------------
def assemble_metrics(rec, isolation, m_route, m_body, m_field, neg_a, neg_b,
                     anchor_metrics, agree_vs, agree_vd, m_kappa, m_canary,
                     fixtures_result, m_ss, m_rl, m_unrel, warm_metrics,
                     gs, gs_b, gate_b_branch, incl_a, excl_a, incl_b, excl_b,
                     trials, neg_vals):
    def mv(v, unit, reason=None):
        d = {"value": v, "unit": unit}
        if v is None and reason:
            d["reason_not_measured"] = reason
        return d

    reason_part2 = ("Part II is read only if Part I reaches D1 EXTRACTION-DEFECT-CONFIRMED "
                    "and NC-NONDEGENERATE-ESTIMATOR passes; reported null, never 0.0.")

    metrics = {
        "M-CERT-ROUTE-OK": mv(m_route, "anchors (0..4)"),
        "M-CERT-BODY-VARIABLE": mv(m_body, "anchors (0..4)"),
        "M-CERT-FIELD-PRESENT": mv(m_field, "anchors (0..4)"),
        "M-CERT-SESSION-ISOLATION-PASS": mv(isolation["pass"], "boolean"),
        "M-CERT-FIRST-REQUEST-COOKIELESS": mv(
            all(v["first_request_cookieless"] for v in isolation["per_anchor"].values()), "boolean"),
        "M-CERT-SESSION-IDENTIFYING-DISJOINT": mv(
            all(v["session_identifying_disjoint"] for v in isolation["per_anchor"].values()), "boolean"),
        "M-CERT-CONSTCONFIG-SHARED-NAMES": {
            "value": {a: v["constconfig_shared_names"] for a, v in isolation["per_anchor"].items()},
            "unit": "map"},
        "M-CERT-UNEXPECTED-SHARED-NAMES": {
            "value": {a: v["unexpected_shared_names"] for a, v in isolation["per_anchor"].items()},
            "unit": "map"},
        "M-CERT-NEG-VALUES-A": mv(neg_a, "count"),
        "M-CERT-NEG-VALUES-B": mv(neg_b, "count"),
        "M-EXTRACT-AGREE-VALUESET": mv(agree_vs, "anchors (0..4)"),
        "M-EXTRACT-AGREE-VERDICT": mv(agree_vd, "anchors (0..4)"),
        "M-EXTRACT-KAPPA": mv(m_kappa, "dimensionless"),
        "M-CANARY-PASS": mv(m_canary, "boolean"),
        "M-FIXTURE-CANARY-PASS": mv(fixtures_result["M-FIXTURE-CANARY-PASS"], "boolean"),
        "M-FIXTURE-EMPTY-AGREE": mv(fixtures_result["M-FIXTURE-EMPTY-AGREE"], "boolean"),
        "M-FIXTURE-JSSTRING-VALUES": mv(fixtures_result["M-FIXTURE-JSSTRING-VALUES"], "count (must be 0)"),
        "M-GUARD-FIXTURE-PASS": mv(fixtures_result["M-GUARD-FIXTURE-PASS"], "boolean"),
        "M-N-SESSION-SCOPED-CONFIRMED": mv(m_ss, "anchors (0..4)"),
        "M-N-REPRESENTATION-LOSS": mv(m_rl, "anchors (0..4)"),
        "M-N-EXTRACTION-UNRELIABLE": mv(m_unrel, "anchors (0..4)"),
        "M-N-AGSI-INSTANCES": mv(len([k for k in incl_a if contributes(trials, k)]), "count"),
        "M-N-AGSI-EXCLUDED-UNSTABLE": {
            "value": len(excl_a | excl_b), "unit": "keys",
            "path_A_excluded": sorted(list(k) for k in excl_a),
            "path_B_excluded": sorted(list(k) for k in excl_b)},
        "M-INVISIBLE-STALE-PREV": mv(
            None, "fraction",
            "SB-04: the behaviourally invisible stale cell is not measured by this packet; null, never 0.0."),
    }
    for a, m in anchor_metrics.items():
        metrics[f"M-DISTINCT-VALUES-A-{a}"] = mv(m["A"]["distinct_values"], "count")
        metrics[f"M-DISTINCT-VALUES-B-{a}"] = mv(m["B"]["distinct_values"], "count")
        metrics[f"M-EXTRACT-RATE-A-{a}"] = mv(m["A"]["extract_rate"], "fraction")
        metrics[f"M-EXTRACT-RATE-B-{a}"] = mv(m["B"]["extract_rate"], "fraction")
        metrics[f"M-ANCHOR-VERDICT-{a}"] = {"value": [m["A"]["verdict"], m["B"]["verdict"]],
                                             "unit": "enum-pair"}
    # warm-jar: canonical unsuffixed maps plus per-anchor instances
    metrics["M-WARMJAR-VARIATION-RATE"] = {
        "value": {a: warm_metrics[a]["M-WARMJAR-VARIATION-RATE"] for a in warm_metrics},
        "unit": "map (fraction per anchor)"}
    metrics["M-WARMJAR-BODY-VARIATION-RATE"] = {
        "value": {a: warm_metrics[a]["M-WARMJAR-BODY-VARIATION-RATE"] for a in warm_metrics},
        "unit": "map (fraction per anchor)"}
    metrics["M-WARMJAR-FRESH-VALUE-VARIATION-RATE"] = {
        "value": {a: warm_metrics[a]["M-WARMJAR-FRESH-VALUE-VARIATION-RATE"] for a in warm_metrics},
        "unit": "map (fraction per anchor)"}
    for a, wm in warm_metrics.items():
        metrics[f"M-WARMJAR-VARIATION-RATE-{a}"] = mv(wm["M-WARMJAR-VARIATION-RATE"], "fraction")
        metrics[f"M-WARMJAR-BODY-VARIATION-RATE-{a}"] = mv(wm["M-WARMJAR-BODY-VARIATION-RATE"], "fraction")
        metrics[f"M-WARMJAR-FRESH-VALUE-VARIATION-RATE-{a}"] = mv(
            wm["M-WARMJAR-FRESH-VALUE-VARIATION-RATE"], "fraction")
        metrics[f"M-ROTATION-TIMESCALE-{a}"] = mv(wm[f"M-ROTATION-TIMESCALE-{a}"], "enum")

    read_part2 = gate_b_branch != "NOT_READ_D1_NOT_REACHED"
    if read_part2:
        metrics["M-N-TRIALS"] = mv(gs["M-N-TRIALS"], "trials")
        metrics["M-N-FRESH"] = mv(gs["M-N-FRESH"], "trials")
        metrics["M-N-D1V"] = mv(gs["M-N-D1V"], "trials")
        metrics["M-N-D1V-ANCHORS"] = mv(gs["M-N-D1V-ANCHORS"], "anchors")
        metrics["M-N-STRUCT-DRIFT"] = mv(gs["M-N-STRUCT-DRIFT"], "trials")
        metrics["M-N-ENDPOINT-DRIFT"] = mv(gs["M-N-ENDPOINT-DRIFT"], "trials")
        metrics["M-N-TRANSPORT-DRIFT"] = mv(gs["M-N-TRANSPORT-DRIFT"], "trials")
        metrics["M-N-POSTCOND-DRIFT"] = mv(gs["M-N-POSTCOND-DRIFT"], "trials")
        metrics["M-FA-INCUMBENT-D1V"] = mv(gs["M-FA-INCUMBENT-D1V"], "fraction")
        metrics["M-FA-INCUMBENT-D1V-UB97"] = mv(gs["M-FA-INCUMBENT-D1V-UB97"], "fraction")
        metrics["M-FA-VALUEAWARE-D1V"] = mv(gs["M-FA-VALUEAWARE-D1V"], "fraction")
        metrics["M-FA-VALUEAWARE-D1V-UB97"] = mv(gs["M-FA-VALUEAWARE-D1V-UB97"], "fraction")
        metrics["M-PAIRED-FA-DIFF-D1V"] = mv(gs["M-PAIRED-FA-DIFF-D1V"], "fraction")
        metrics["M-PAIRED-FA-DIFF-D1V-LOW"] = mv(gs["M-PAIRED-FA-DIFF-D1V-LOW"], "fraction")
        metrics["M-PAIRED-FA-DIFF-D1V-UB97"] = mv(gs["M-PAIRED-FA-DIFF-D1V-UB97"], "fraction")
        metrics["M-FA-INCUMBENT-ALL"] = mv(gs["M-FA-INCUMBENT-ALL"], "fraction")
        metrics["M-FA-VALUEAWARE-ALL"] = mv(gs["M-FA-VALUEAWARE-ALL"], "fraction")
        metrics["M-FR-INCUMBENT-FRESH"] = mv(gs["M-FR-INCUMBENT-FRESH"], "fraction")
        metrics["M-FR-VALUEAWARE-FRESH"] = mv(gs["M-FR-VALUEAWARE-FRESH"], "fraction")
        metrics["M-N-DECISIONS-D1V"] = mv(gs["M-N-DECISIONS-D1V"], "count")
        for k, v in gs["diagnostics"].items():
            metrics[k] = v
    else:
        for mid in ["M-N-TRIALS", "M-N-FRESH", "M-N-D1V", "M-N-D1V-ANCHORS",
                    "M-N-STRUCT-DRIFT", "M-N-ENDPOINT-DRIFT", "M-N-TRANSPORT-DRIFT",
                    "M-N-POSTCOND-DRIFT", "M-FA-INCUMBENT-D1V", "M-FA-INCUMBENT-D1V-UB97",
                    "M-FA-VALUEAWARE-D1V", "M-FA-VALUEAWARE-D1V-UB97",
                    "M-PAIRED-FA-DIFF-D1V", "M-PAIRED-FA-DIFF-D1V-LOW",
                    "M-PAIRED-FA-DIFF-D1V-UB97", "M-FA-INCUMBENT-ALL", "M-FA-VALUEAWARE-ALL",
                    "M-FR-INCUMBENT-FRESH", "M-FR-VALUEAWARE-FRESH", "M-N-DECISIONS-D1V"]:
            metrics[mid] = mv(None, "fraction" if "FA" in mid or "FR" in mid or "PAIRED" in mid
                              else "count", reason_part2)
        # still disclose the constructed population diagnostically
        metrics["M-N-D1V"] = {"value": gs["M-N-D1V"], "unit": "trials",
                              "read": False,
                              "note": "constructed but not READ because Part I did not reach D1; "
                                      "kept for downstream recomputation only."}
        metrics["M-N-DECISIONS-D1V"] = {"value": gs["M-N-DECISIONS-D1V"], "unit": "count",
                                        "read": False}
    return metrics


def contributes(trials, key):
    return any(t["anchor_id"] == key[0] and t["field_name"] == key[1]
               and t["occurrence_ordinal"] == key[2] for t in trials)


def assemble_controls(isolation, nv, attestation, fixtures_result, anchor_metrics,
                      neg_vals, c1, c2, c3, c4, e1, e2, e3, canary, agree_vs,
                      agree_vd, m_ss, m_rl, m_unrel, gs, gs_b, gate_b_branch, branch):
    g = lambda ok: "PASS" if ok else "FAIL"
    controls = {
        "GATE-C1": {"expected": "M-CERT-ROUTE-OK>=3 and M-CERT-FIELD-PRESENT>=3",
                    "observed": {"route_ok": c1}, "result": g(c1)},
        "GATE-C2": {"expected": "M-CERT-NEG-VALUES-A==0 and M-CERT-NEG-VALUES-B==0",
                    "observed": c2, "result": g(c2)},
        "GATE-C3": {"expected": "repaired M-CERT-SESSION-ISOLATION-PASS and NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS",
                    "observed": {"isolation_pass": isolation["pass"],
                                 "not_vacuous": nv["not_vacuous"]},
                    "result": g(c3)},
        "GATE-C4": {"expected": "M-CERT-BODY-VARIABLE>=3 (non-blocking disclosure)",
                    "observed": c4, "result": "PASS" if c4 else "DISCLOSURE-NO-BODY-VARIATION"},
        "GATE-E1": {"expected": "M-CANARY-PASS==true", "observed": canary, "result": g(e1)},
        "GATE-E2": {"expected": "fixtures + NC-PATH-INDEPENDENCE + NC-TRIAL-CONSTRUCTION-STABILITY",
                    "observed": e2, "result": g(e2)},
        "GATE-E3": {"expected": "M-EXTRACT-AGREE-VALUESET>=3 and M-EXTRACT-AGREE-VERDICT>=3",
                    "observed": {"valueset": agree_vs, "verdict": agree_vd},
                    "result": g(e3)},
        "GATE-B": {"expected": "Part II read only if D1; INCUMBENT-BLIND-CONFIRMED iff diff>=0.10 and LB>0",
                   "observed": gate_b_branch, "result": gate_b_branch},
        "B-SINGLE-PATH-A": {"expected_behavior": "P-EXTRACT-A alone cannot self-certify",
                            "observed": {a: m["A"]["verdict"] for a, m in anchor_metrics.items()},
                            "result": "OBSERVED"},
        "B-SINGLE-PATH-B": {"expected_behavior": "independent regex/lexer; disagreement is the extraction signal",
                            "observed": {a: m["B"]["verdict"] for a, m in anchor_metrics.items()},
                            "result": "OBSERVED"},
        "B-PARENT-METHOD-REIMPL": {
            "expected_behavior": "best-effort documented reconstruction of the grandparent method over the same bytes; no gate depends on it",
            "observed": {"reconstruction_note": "Parent preserved no code; proxy = P-EXTRACT-A (html.parser, non-GET form token fields + frozen-list meta tokens, no JS).",
                         "CAL-POS-2_distinct_values": anchor_metrics["CAL-POS-2"]["A"]["distinct_values"],
                         "CAL-POS-2_verdict": anchor_metrics["CAL-POS-2"]["A"]["verdict"]},
            "result": "DISCLOSED-PROXY"},
        "B-INCUMBENT-SIGNAL-ONLY": {
            "expected_behavior": "value-blind: REUSE iff none of CH-STRUCT-SIG, CH-TRANSPORT-VALIDATOR, CH-POSTCOND-SEM fires",
            "observed": {"M-FA-INCUMBENT-D1V": gs["M-FA-INCUMBENT-D1V"],
                         "M-FA-INCUMBENT-D1V-UB97": gs["M-FA-INCUMBENT-D1V-UB97"],
                         "channels": gs["channels"]},
            "result": gate_b_branch},
        "B-VALUE-AWARE": {
            "expected_behavior": "CH-PRECOND-BINDING only: REUSE iff live == recorded",
            "observed": {"M-FA-VALUEAWARE-D1V": gs["M-FA-VALUEAWARE-D1V"],
                         "M-FA-VALUEAWARE-D1V-UB97": gs["M-FA-VALUEAWARE-D1V-UB97"]},
            "result": gate_b_branch},
        "B-FULL-GUARD": {"expected_behavior": "union of the four channels",
                         "observed": "reported as reference", "result": gate_b_branch},
        "B-NO-GUARD-REPLAY": {"expected_behavior": "always REUSE; raw-observation reference only",
                              "observed": {"n_trials": gs["M-N-TRIALS"], "n_d1v": gs["M-N-D1V"]},
                              "result": "OBSERVED"},
        "CH-STRUCT-SIG": {"expected": "fires iff structure signature differs",
                          "observed": gs["channels"]["CH-STRUCT-SIG"], "result": gs["channels"]["CH-STRUCT-SIG"]["status"]},
        "CH-TRANSPORT-VALIDATOR": {"expected": "fires iff transport signature differs",
                                   "observed": gs["channels"]["CH-TRANSPORT-VALIDATOR"],
                                   "result": gs["channels"]["CH-TRANSPORT-VALIDATOR"]["status"]},
        "CH-POSTCOND-SEM": {"expected": "fires iff session in-list field-name set differs",
                            "observed": gs["channels"]["CH-POSTCOND-SEM"],
                            "result": gs["channels"]["CH-POSTCOND-SEM"]["status"]},
        "CH-PRECOND-BINDING": {"expected": "fires iff live != recorded byte-exact",
                               "observed": gs["channels"]["CH-PRECOND-BINDING"],
                               "result": gs["channels"]["CH-PRECOND-BINDING"]["status"]},
        "PC-EXTRACT-CANARY": {"expected": "both paths >=2 distinct authenticity_token on CAL-POS-1",
                              "observed": canary, "result": g(canary)},
        "PC-GUARD-LOGIC": {"expected": "all SYN-GUARD-* fixtures produce pre-declared decisions",
                           "observed": fixtures_result["guard_fixtures"],
                           "result": g(fixtures_result["M-GUARD-FIXTURE-PASS"])},
        "NC-CAL-NEG-ALL-REJECTED": {
            "expected": "0 in-list values under BOTH paths on all 4 negatives",
            "observed": neg_vals, "result": g(c2)},
        "NC-EXTRACT-EMPTY-VALUE": {"expected": "SYN-EMPTY-VALUE PRESENT-EMPTY, both paths agree",
                                   "observed": fixtures_result["empty_a_states"],
                                   "result": g(fixtures_result["M-FIXTURE-EMPTY-AGREE"])},
        "NC-EXTRACT-JSSTRING": {"expected": "0 non-empty values from SYN-JSSTRING",
                                "observed": fixtures_result["M-FIXTURE-JSSTRING-VALUES"],
                                "result": g(fixtures_result["M-FIXTURE-JSSTRING-VALUES"] == 0)},
        "NC-PATH-INDEPENDENCE": {"expected": "AST import attestation + separate hashes + perturbation invariance",
                                 "observed": attestation,
                                 "result": g(attestation["path_independence_pass"])},
        "NC-SESSION-ISOLATION-REPAIRED": {"expected": "repaired predicate passes for every anchor/session",
                                          "observed": {a: v["pass"] for a, v in isolation["per_anchor"].items()},
                                          "result": g(isolation["pass"])},
        "NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS": {
            "expected": "shared _gitlab_session must FAIL; allowlisted-only must PASS",
            "observed": nv, "result": g(nv["not_vacuous"])},
        "NC-TRIAL-CONSTRUCTION-STABILITY": {
            "expected": "identical included-key set on both paths",
            "observed": "see GATE-E2 / guard_stats.json", "result": g(e2)},
        "NC-TIME-VS-SESSION": {"expected": "warm-jar diagnostic, frozen ceiling rule, not pass/fail",
                               "observed": "see M-WARMJAR-* and M-ROTATION-TIMESCALE-*",
                               "result": "DIAGNOSTIC"},
        "NC-NONDEGENERATE-ESTIMATOR": {
            "expected": "M-N-D1V>=6, >=2 decisions on D1V, every active channel fires and not-fires; inactive channels waived with reason",
            "observed": {"M-N-D1V": gs["M-N-D1V"], "M-N-DECISIONS-D1V": gs["M-N-DECISIONS-D1V"],
                         "nondegenerate": gs["nondegenerate"], "channels": gs["channels"]},
            "result": "PASS" if gs["nondegenerate"] else "DATA-INSUFFICIENT-D1V"},
        "NC-OPEN-GET-ONLY": {"expected": "every scored request is a credential-free idempotent GET",
                             "observed": "all requests method GET; no write verb, no credentials",
                             "result": "PASS"},
        "F-INSTR": {"observed_triggered": branch == "F-INSTR"},
        "F-REPLOSS": {"observed_triggered": branch == "REPRESENTATION-LOSS-CONFIRMED"},
        "F-UNRELIABLE": {"observed_triggered": branch == "EXTRACTION-UNRELIABLE"},
        "F-BLIND": {"observed_triggered": gate_b_branch == "INCUMBENT-NOT-BLIND"},
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
                            "result": g(fixtures_result["M-FIXTURE-CANARY-PASS"])},
        "SYN-EMPTY-VALUE": {"role": "instrument fixture (unscored)",
                            "result": g(fixtures_result["M-FIXTURE-EMPTY-AGREE"])},
        "SYN-JSSTRING": {"role": "instrument fixture (unscored)",
                         "result": g(fixtures_result["M-FIXTURE-JSSTRING-VALUES"] == 0)},
        "SYN-GUARD-D1V": {"role": "guard fixture (unscored)",
                          "result": g(fixtures_result["guard_fixtures"]["SYN-GUARD-D1V"]["pass"])},
        "SYN-GUARD-FRESH": {"role": "guard fixture (unscored)",
                            "result": g(fixtures_result["guard_fixtures"]["SYN-GUARD-FRESH"]["pass"])},
        "SYN-GUARD-POSTCOND": {"role": "guard fixture (unscored)",
                               "result": g(fixtures_result["guard_fixtures"]["SYN-GUARD-POSTCOND"]["pass"])},
    }
    return controls


def build_observations(rec, isolation, anchor_metrics, neg_vals, fixtures_result,
                       gs, gs_b, warm_metrics, canary, agree_vs, agree_vd, m_ss,
                       m_rl, m_unrel, branch, gate_b_branch, trials, nv):
    obs = []
    obs.append(f"Requests executed: {rec.request_count} (cap 200); all method GET; no credentials, no write verb.")
    obs.append("Repaired session isolation: M-CERT-SESSION-ISOLATION-PASS="
               f"{isolation['pass']}; per-anchor pass={ {a: v['pass'] for a, v in isolation['per_anchor'].items()} }.")
    obs.append("Constant-configuration shared cookie names per anchor: "
               f"{ {a: v['constconfig_shared_names'] for a, v in isolation['per_anchor'].items()} }.")
    obs.append("Unexpected shared cookie names (outside allowlist): "
               f"{ {a: v['unexpected_shared_names'] for a, v in isolation['per_anchor'].items()} }.")
    obs.append(f"NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS: shared _gitlab_session fails={not nv['shared_session_identifying_name_fails'] is False}; "
               f"allowlisted-only passes={nv['allowlisted_only_passes']}; not_vacuous={nv['not_vacuous']}.")
    for a, m in anchor_metrics.items():
        obs.append(f"{a}: verdict_A={m['A']['verdict']} (distinct={m['A']['distinct_values']}), "
                   f"verdict_B={m['B']['verdict']} (distinct={m['B']['distinct_values']}), "
                   f"route_ok={m['A']['route_ok']}/4, distinct_body={m['A']['distinct_body']}/4.")
    obs.append(f"M-EXTRACT-AGREE-VALUESET={agree_vs}/4, M-EXTRACT-AGREE-VERDICT={agree_vd}/4, M-CANARY-PASS={canary}.")
    obs.append(f"M-N-SESSION-SCOPED-CONFIRMED={m_ss}/4, M-N-REPRESENTATION-LOSS={m_rl}/4, "
               f"M-N-EXTRACTION-UNRELIABLE={m_unrel}/4.")
    for a, nd in neg_vals.items():
        obs.append(f"{a}: path_A non-empty values={nd['A']}, path_B non-empty values={nd['B']}.")
    obs.append(f"Drift population (path A): M-N-TRIALS={gs['M-N-TRIALS']}, M-N-FRESH={gs['M-N-FRESH']}, "
               f"M-N-D1V={gs['M-N-D1V']} over {gs['M-N-D1V-ANCHORS']} anchors; "
               f"struct={gs['M-N-STRUCT-DRIFT']}, endpoint={gs['M-N-ENDPOINT-DRIFT']}, "
               f"transport={gs['M-N-TRANSPORT-DRIFT']}, postcond={gs['M-N-POSTCOND-DRIFT']}.")
    obs.append(f"Channels (path A): {json.dumps(gs['channels'], sort_keys=True)}.")
    obs.append(f"Part II gate: {gate_b_branch}; M-N-DECISIONS-D1V={gs['M-N-DECISIONS-D1V']}; "
               f"M-FA-INCUMBENT-D1V={gs['M-FA-INCUMBENT-D1V']}; M-FA-VALUEAWARE-D1V={gs['M-FA-VALUEAWARE-D1V']}; "
               f"M-PAIRED-FA-DIFF-D1V={gs['M-PAIRED-FA-DIFF-D1V']} "
               f"(LB={gs['M-PAIRED-FA-DIFF-D1V-LOW']}, UB={gs['M-PAIRED-FA-DIFF-D1V-UB97']}).")
    obs.append("Warm-jar timescale per anchor: " + json.dumps(
        {a: {"warm_var": w["M-WARMJAR-VARIATION-RATE"], "fresh_var": w["M-WARMJAR-FRESH-VALUE-VARIATION-RATE"],
             "timescale": w[f"M-ROTATION-TIMESCALE-{a}"]} for a, w in warm_metrics.items()}, sort_keys=True))
    obs.append(f"Guard fixtures: {json.dumps(fixtures_result['guard_fixtures'], sort_keys=True)}.")
    obs.append(f"Trial construction stable across paths A/B (included-key sets identical)= "
               f"{gs['M-N-TRIALS'] == gs_b['M-N-TRIALS'] and gs['M-N-D1V'] == gs_b['M-N-D1V']}.")
    return obs


def build_validity_notes(attestation, v_before, v_after, gs, gate_c4_ok, m_body,
                         codex_dep_present, codex_dep_sha):
    notes = [
        "PART II TRIAL-CONSTRUCTION OPERATIONALIZATION. The frozen spec describes the AGSI "
        "instance key as '(anchor_id, field_name, structure_signature) plus a document-order "
        "occurrence ordinal'. Taken maximally literally (structure_signature inside the matching "
        "key), a structural change would alter the key, exclude the instance and make "
        "CH-STRUCT-SIG/M-N-STRUCT-DRIFT unreachable, contradicting the frozen metric registry and "
        "the NC-NONDEGENERATE-ESTIMATOR clause which anticipates CH-POSTCOND-SEM as the inactive "
        "channel. EXECUTE therefore pairs AGSI occurrences across sessions by "
        "(anchor_id, field_name, document-order occurrence ordinal among same-field occurrences) "
        "and requires the same-field occurrence COUNT to be identical across all four sessions "
        "before a slot contributes; structure_signature is recorded and used as the "
        "CH-STRUCT-SIG activation input, not as part of the matching key. This is a disclosed "
        "operationalization of an ambiguous frozen clause; it was fixed before any guard statistic "
        "was computed and is applied identically to both paths.",
        "PART II VALUE-TRIAL REQUIREMENT. A realized trial requires BOTH the recorded and current "
        "occurrence state to be VALUE (non-empty exact string), mirroring the parent's frozen "
        "operationalization and the ground_truth formula. Occurrences that are PRESENT-EMPTY on "
        "either side are not realized as value trials.",
        "PART II IS STATUS-NON-CHANGING. GATE B branches (INCUMBENT-BLIND-CONFIRMED / "
        "INCUMBENT-NOT-BLIND / DATA-INSUFFICIENT-D1V) are recorded under metrics/controls/"
        "observations and never change status/outcome.",
        "RESAMPLING UNIT. Part II intervals resample ANCHORS with replacement, B=10000, seed "
        "37964565784, percentile method. The trial-level Wilson intervals are reported only as "
        "M-DIAGNOSTIC-UNCLUSTERED-* with do_not_use=true; no gate uses them.",
        f"V05 NO-JS REPRESENTATION LOSS DECLARED. No JavaScript was executed and no browser was "
        f"used; only raw HTTP response bytes were parsed. Client-side/XHR-minted values, canvas "
        f"content and authenticated state are structurally invisible.",
        f"NC-PATH-INDEPENDENCE attestation: path_independence_pass={attestation['path_independence_pass']}, "
        f"path_B_forbidden_imports={attestation['path_b_forbidden_imports']}, "
        f"no_anchor_special_casing={attestation['no_anchor_special_casing']}, "
        f"perturbation_invariant={attestation['perturbation_invariant']}.",
        f"V11 frozen-input re-verification before={v_before} after={v_after}.",
        f"GATE C4 (non-blocking) M-CERT-BODY-VARIABLE={m_body}/4; "
        f"{'satisfied' if gate_c4_ok else 'NO-BODY-VARIATION disclosure'}.",
        f"PROVENANCE DEPENDENCY codex/experiments/EXP-FRONTIER-36306528608/raw/token_stability.jsonl "
        f"present={codex_dep_present}" + (f" sha256={codex_dep_sha}" if codex_dep_sha else
        " (reported absent; design-owned by the Codex synchronization step; GATE C re-measures "
        "live and does not depend on it; audit required_fixes[1] recorded)."),
        "CC-A SCOPE. All results are scoped to the 4 pinned credential-free, server-rendered, "
        "no-JavaScript GET-only anchors, K=4 fresh sessions, stdlib HTTP, one capture date and one "
        "egress path. Prevalence over 'the Web' is never quoted.",
        "PER-REQUEST vs SESSION ROTATION. M-ROTATION-TIMESCALE is a diagnostic with the frozen "
        "CC-H ceiling; if PER_REQUEST_SCALE, value-binding freshness is bounded to a short-lived "
        "applicability check, not session-scoped durability.",
        "The two extraction paths were adapted from the parent packet's independently written "
        "stdlib paths and are separate producer files for this experiment; independence is "
        "structural (different algorithms, no shared code, AST-verified) and corroborated by the "
        "canary, fixtures and negatives (CC-F).",
    ]
    if gs["M-N-D1V"] and gs["M-N-D1V"] < 6:
        notes.append(f"D1V population is below the frozen adequacy floor (M-N-D1V={gs['M-N-D1V']} < 6); "
                     "no false-accept or blindness claim is made.")
    inactive = [c for c, v in gs["channels"].items() if v["status"] == "INACTIVE-ON-POPULATION"]
    if inactive:
        notes.append("INACTIVE-ON-POPULATION channels (waived with reason): " + ", ".join(inactive)
                     + "; their drift family stays UNKNOWN.")
    return notes


def build_unresolved(branch, gs, gate_b_branch, agree_vs, agree_vd, codex_dep_present):
    ur = []
    if branch != "EXTRACTION-DEFECT-CONFIRMED":
        ur.append("Part I did not reach D1; the extraction-vs-representation-loss attribution for "
                  "these anchors remains unresolved and no claim-level statement is licensed.")
    if gate_b_branch == "DATA-INSUFFICIENT-D1V":
        ur.append(f"Part II is DATA-INSUFFICIENT-D1V (M-N-D1V={gs['M-N-D1V']}, "
                  f"M-N-DECISIONS-D1V={gs['M-N-DECISIONS-D1V']}, nondegenerate={gs['nondegenerate']}); "
                  "the incumbent guard's false-accept bound on value-only rotation is not measured.")
    elif gate_b_branch == "NOT_READ_D1_NOT_REACHED":
        ur.append("Part II was not read because Part I did not reach D1.")
    if not codex_dep_present:
        ur.append("codex/experiments/EXP-FRONTIER-36306528608/raw/token_stability.jsonl is absent; "
                  "provenance completeness gap (audit required_fixes[1]).")
    ur.append("Whether CAL-POS-4's NO_FIELD verdict is genuine absence or a limitation of the "
              "frozen token-name list is unresolved.")
    ur.append("Whether the wpCreateaccountToken discrepancy is stable over time and across egress "
              "networks is unresolved; this run records one date and one egress path.")
    ur.append("The behaviourally invisible stale cell (SB-04, M-INVISIBLE-STALE-PREV) and the "
              "permission-boundary drift family (SB-02) remain unmeasured by design.")
    return ur


def collect_artifacts(raw_jsonl, bodies, warm_bodies, rec, gs, v_before, v_after,
                      codex_dep_present, codex_dep_sha):
    arts = []

    def add(path, role):
        p = ROOT / path
        if p.exists() and p.is_file():
            arts.append({"path": path, "sha256": sha256_file(p), "role": role})

    add(str(raw_jsonl.relative_to(ROOT)), "raw")
    for a, _ in POSITIVE_ANCHORS + NEGATIVE_ANCHORS:
        for s in SESSIONS:
            add(f"research/experiments/{EXP_ID}/raw/bodies/{a}/{s}_fresh.html", "raw")
    for a, _ in POSITIVE_ANCHORS:
        for wi in (1, 2):
            add(f"research/experiments/{EXP_ID}/raw/bodies/{a}/S4_warm{wi}.html", "raw")
    for name in ["derived/extraction_A.jsonl", "derived/extraction_B.jsonl", "derived/trials.jsonl",
                 "derived/certificate.json", "derived/fixtures.json", "derived/anchor_metrics.json",
                 "derived/guard_stats.json"]:
        add(f"research/experiments/{EXP_ID}/{name}", "derived")
    for name in ["path_a_htmlparser.py", "path_b_regexlex.py", "neutral_detector.py",
                 "fixtures.py", "guard.py", "run_experiment.py"]:
        add(f"research/experiments/{EXP_ID}/code/{name}", "code")
    if codex_dep_present:
        arts.append({"path": "codex/experiments/EXP-FRONTIER-36306528608/raw/token_stability.jsonl",
                     "sha256": codex_dep_sha, "role": "fixture"})
    return arts


def build_provenance(rec, attestation, raw_jsonl, bodies, warm_bodies, v_before, v_after,
                     codex_dep_present, codex_dep_sha):
    import platform as _p
    return {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "lane": LANE,
        "origin_github_run_id": RUN_ID,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "base_sha": json.loads((EXP_DIR / "request.json").read_text()).get("base_sha"),
        "environment": {
            "python": sys.version,
            "python_implementation": _p.python_implementation(),
            "platform": _p.platform(),
            "stdlib_only": True,
            "dependencies": ["urllib", "http.cookiejar", "html.parser", "re", "ast", "hashlib",
                             "json", "math", "random", "statistics", "platform", "datetime",
                             "pathlib", "time"],
            "browser": None,
            "docker": None,
            "model_calls": 0,
            "credentials": None,
        },
        "frozen_seed": FROZEN_SEED,
        "seed_mechanism": "random.Random(37964565784) for the anchor-clustered bootstrap; "
                          "Python process-randomized hash() is never used as a seed or key",
        "request_count": rec.request_count,
        "request_cap": REQUEST_CAP,
        "method": "GET only",
        "pacing_seconds_per_host": PACING_SECONDS,
        "anchors": {
            "positive": [{"anchor_id": a, "url": u} for a, u in POSITIVE_ANCHORS],
            "negative": [{"anchor_id": a, "url": u} for a, u in NEGATIVE_ANCHORS],
            "retired": [{"anchor_id": "CAL-POS-5",
                         "url": "https://bugs.launchpad.net/ubuntu/+reportbug",
                         "reason": "404x4 in parent; excluded from all denominators; not contacted"}],
        },
        "sessions": {"K_total": 4, "ids": SESSIONS, "recorded_session": "S1",
                     "current_sessions": ["S2", "S3", "S4"]},
        "capture_utc_range": {
            "first": min(r["requested_at_utc"] for r in rec.records),
            "last": max(r["requested_at_utc"] for r in rec.records),
        },
        "frozen_input_verification": {"before": v_before, "after": v_after},
        "code_attestation": attestation,
        "provenance_dependency": {
            "path": "codex/experiments/EXP-FRONTIER-36306528608/raw/token_stability.jsonl",
            "present": codex_dep_present, "sha256": codex_dep_sha,
            "note": "audit required_fixes[1]; owned by the Codex synchronization step; not edited here; "
                    "GATE C re-measures live and does not depend on it.",
        },
        "artifact_aggregates": {
            "raw_records_sha256": sha256_file(raw_jsonl) if raw_jsonl.exists() else None,
            "n_body_files": sum(1 for a, _ in ALL_ANCHORS for s in SESSIONS)
                            + sum(1 for a, _ in POSITIVE_ANCHORS for _ in (1, 2)),
        },
        "commands": [f"python3 {HERE / 'run_experiment.py'}"],
    }


def write_failure(message, detail):
    (EXP_DIR / "failure.json").write_text(json.dumps({
        "schema_version": 1, "experiment_id": EXP_ID, "lane": LANE, "stage": "execute",
        "category": "measurement_infrastructure", "message": message, "detail": detail,
        "retryable": True,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
    }, indent=2) + "\n")


def write_report(result, anchor_metrics, neg_vals, gs, gs_b, warm_metrics, isolation,
                 nv, fixtures_result, attestation, n_records, neg_a, neg_b):
    m = result["metrics"]

    def V(mid):
        v = m.get(mid)
        if isinstance(v, dict):
            return v.get("value")
        return v

    lines = []
    lines.append(f"# EXP-GRAPH-37964565784 — EXECUTE report (graph, C-FRESHNESS)\n")
    lines.append(f"**status={result['status']} · outcome={result['outcome']} · branch={result['branch']} · "
                 f"Part II gate={result['gate_b_branch']}**\n")
    lines.append("This packet repairs the parent's GATE-C3 certificate predicate at design time "
                 "(audit required_fixes[0]) and re-runs the same frozen two-path extraction read, "
                 "then reads the incumbent value-blind guard versus the value-aware guard on real "
                 "value-only rotation with anchor-clustered bounds.\n")
    lines.append("## 1. Raw evidence and certificate (GATE C)\n")
    lines.append(f"- Requests: {n_records} (all GET, cap 200); all first requests cookie-free: "
                 f"{V('M-CERT-FIRST-REQUEST-COOKIELESS')}.")
    lines.append(f"- M-CERT-ROUTE-OK={V('M-CERT-ROUTE-OK')}/4, M-CERT-BODY-VARIABLE={V('M-CERT-BODY-VARIABLE')}/4, "
                 f"M-CERT-FIELD-PRESENT={V('M-CERT-FIELD-PRESENT')}/4.")
    lines.append(f"- M-CERT-SESSION-ISOLATION-PASS={V('M-CERT-SESSION-ISOLATION-PASS')}; "
                 f"NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS={nv['not_vacuous']}.")
    lines.append(f"- M-CERT-NEG-VALUES-A={V('M-CERT-NEG-VALUES-A')}, M-CERT-NEG-VALUES-B={V('M-CERT-NEG-VALUES-B')} "
                 f"(all four negatives).")
    lines.append("\n## 2. Part I — extraction validity under the repaired certificate (GATE E)\n")
    for a, mm in anchor_metrics.items():
        lines.append(f"- **{a}**: verdict_A={mm['A']['verdict']} (distinct={mm['A']['distinct_values']}), "
                     f"verdict_B={mm['B']['verdict']} (distinct={mm['B']['distinct_values']}), "
                     f"route_ok={mm['A']['route_ok']}/4, distinct_body={mm['A']['distinct_body']}/4.")
    lines.append(f"- M-EXTRACT-AGREE-VALUESET={V('M-EXTRACT-AGREE-VALUESET')}/4, "
                 f"M-EXTRACT-AGREE-VERDICT={V('M-EXTRACT-AGREE-VERDICT')}/4, "
                 f"M-CANARY-PASS={V('M-CANARY-PASS')}, M-EXTRACT-KAPPA={V('M-EXTRACT-KAPPA')}.")
    lines.append(f"- M-N-SESSION-SCOPED-CONFIRMED={V('M-N-SESSION-SCOPED-CONFIRMED')}/4, "
                 f"M-N-REPRESENTATION-LOSS={V('M-N-REPRESENTATION-LOSS')}/4, "
                 f"M-N-EXTRACTION-UNRELIABLE={V('M-N-EXTRACTION-UNRELIABLE')}/4.")
    lines.append("\n## 3. Part II — repaired drift population and explicit false-accept bound (GATE B)\n")
    lines.append(f"- M-N-D1V={V('M-N-D1V')} over {V('M-N-D1V-ANCHORS')} anchors; "
                 f"M-N-DECISIONS-D1V={V('M-N-DECISIONS-D1V')}; nondegenerate={gs['nondegenerate']}.")
    lines.append(f"- Channels (path A): {json.dumps(gs['channels'], sort_keys=True)}.")
    lines.append(f"- M-FA-INCUMBENT-D1V={V('M-FA-INCUMBENT-D1V')} "
                 f"(UB97={V('M-FA-INCUMBENT-D1V-UB97')}); "
                 f"M-FA-VALUEAWARE-D1V={V('M-FA-VALUEAWARE-D1V')} "
                 f"(UB97={V('M-FA-VALUEAWARE-D1V-UB97')}); "
                 f"M-PAIRED-FA-DIFF-D1V={V('M-PAIRED-FA-DIFF-D1V')} "
                 f"(LB={V('M-PAIRED-FA-DIFF-D1V-LOW')}, UB={V('M-PAIRED-FA-DIFF-D1V-UB97')}).")
    lines.append(f"- Part II gate branch: **{result['gate_b_branch']}** (status-non-changing).")
    lines.append("\n## 4. Timescale diagnostic (CC-H)\n")
    for a, w in warm_metrics.items():
        lines.append(f"- {a}: {w[f'M-ROTATION-TIMESCALE-{a}']} "
                     f"(warm_var={w['M-WARMJAR-VARIATION-RATE']}, "
                     f"fresh_var={w['M-WARMJAR-FRESH-VALUE-VARIATION-RATE']}, "
                     f"body_var={w['M-WARMJAR-BODY-VARIATION-RATE']}).")
    lines.append("\n## 5. Controls\n")
    for cid in ["GATE-C1", "GATE-C2", "GATE-C3", "GATE-C4", "GATE-E1", "GATE-E2", "GATE-E3",
                "PC-EXTRACT-CANARY", "PC-GUARD-LOGIC", "NC-CAL-NEG-ALL-REJECTED",
                "NC-PATH-INDEPENDENCE", "NC-SESSION-ISOLATION-REPAIRED",
                "NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS", "NC-NONDEGENERATE-ESTIMATOR"]:
        c = result["controls"].get(cid, {})
        lines.append(f"- {cid}: {c.get('result')}")
    lines.append("\n## 6. Interpretation (bounded)\n")
    if result["branch"] == "EXTRACTION-DEFECT-CONFIRMED":
        lines.append("The repaired certificate passed and both independently written stdlib paths "
                     "agree on per-field value sets and session-scoped verdicts; the parent's "
                     "failure on these anchors is attributable to an instrument/extraction "
                     "certificate defect, not to representation loss. C-FRESHNESS may advance at "
                     "most to EXPERIMENTAL, only via the DIRECTOR (CC-B). No promotion is authorized.")
    elif result["branch"] == "REPRESENTATION-LOSS-CONFIRMED":
        lines.append("Both paths agree on zero/single-value recovery while bodies vary: bounded "
                     "representation-loss on this anchor class (CC-C). No stdlib no-JS guard can be "
                     "calibrated here; C-FRESHNESS stays HYPOTHESIS.")
    elif result["branch"] == "EXTRACTION-UNRELIABLE":
        lines.append("The two paths disagree on at least two anchors: extraction validity is not "
                     "established and no substrate verdict follows (F-UNRELIABLE).")
    elif result["branch"] == "F-CERT":
        lines.append("The repaired certificate failed a blocking gate: terminal MEASUREMENT_INVALID "
                     "(F-CERT); no claim-level statement is licensed.")
    elif result["branch"] == "F-INSTR":
        lines.append("An instrument gate failed: terminal MEASUREMENT_INVALID (F-INSTR).")
    else:
        lines.append(f"Bounded read: {result['branch']}.")
    if result["gate_b_branch"] == "INCUMBENT-BLIND-CONFIRMED":
        lines.append("Part II: the value-blind incumbent guard false-accepts on real value-only "
                     "rotation materially more than the value-aware guard; the shipped architecture "
                     "must retain CH-PRECOND-BINDING (bounded to these anchors, CC-E).")
    elif result["gate_b_branch"] == "INCUMBENT-NOT-BLIND":
        lines.append("Part II: the incumbent value-blind set is not materially more false-accepting "
                     "than the value-aware channel on real D1V trials (bounded negative about "
                     "necessity, not a C-FRESHNESS falsification).")
    elif result["gate_b_branch"] == "DATA-INSUFFICIENT-D1V":
        lines.append("Part II is DATA-INSUFFICIENT-D1V: the drift population is below the frozen "
                     "adequacy floor; the false-accept bound is not measured (a power statement, "
                     "not a negative).")
    lines.append("\nNo promotion into Product Core, no replay-by-assumption. M-INVISIBLE-STALE-PREV "
                 "is null, never 0.0; SB-02 and SB-04 remain unmeasured by design.")
    (EXP_DIR / "report.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
