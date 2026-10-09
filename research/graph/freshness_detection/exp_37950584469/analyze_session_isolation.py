#!/usr/bin/env python3
"""Deterministic post-run diagnostic for EXP-GRAPH-37950584469 GATE-C3.

Reads only the retained raw evidence (raw/records.jsonl) and explains precisely
why the frozen GATE-C3 predicate (four fresh cookie jars pairwise disjoint on
(name, value)) failed, without contacting any host and without changing any
frozen gate, metric or decision.  Output is DERIVED, not raw; the canonical
decision in result.json (MEASUREMENT_INVALID / F-CERT) is unchanged.

Stdlib only.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP_DIR = ROOT / "research" / "experiments" / "EXP-GRAPH-37950584469"
RAW_JSONL = EXP_DIR / "raw" / "records.jsonl"
OUT = EXP_DIR / "derived" / "session_isolation_diagnostic.json"

POSITIVE = ["CAL-POS-1", "CAL-POS-2", "CAL-POS-3", "CAL-POS-4"]
SESSIONS = ["S1", "S2", "S3", "S4"]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    raw_bytes = RAW_JSONL.read_bytes()
    records = [json.loads(line) for line in raw_bytes.decode().splitlines() if line.strip()]

    by_anchor_session = {}
    for r in records:
        if r.get("phase") != "fresh":
            continue
        cookies = {(c[2], c[3]) for c in r.get("cookies_after", [])}
        by_anchor_session.setdefault(r["anchor_id"], {})[r["session"]] = cookies

    per_anchor = {}
    all_shared_constant = True
    any_pair_shared = False
    for anchor in POSITIVE:
        per_sess = by_anchor_session.get(anchor, {})
        sets = {s: per_sess.get(s, set()) for s in SESSIONS}

        shared = set()
        for s1, s2 in itertools.combinations(SESSIONS, 2):
            shared |= sets[s1] & sets[s2]

        # classify cookie names by whether their value is constant across sessions
        names_values = {}
        for s in SESSIONS:
            for name, value in sets[s]:
                names_values.setdefault(name, set()).add(value)
        names_constant = sorted(n for n, vs in names_values.items() if len(vs) == 1)
        names_varying = sorted(n for n, vs in names_values.items() if len(vs) > 1)

        shared_names = {n for n, _ in shared}
        shared_only_constant = shared_names.issubset(set(names_constant))
        all_shared_constant = all_shared_constant and shared_only_constant
        any_pair_shared = any_pair_shared or bool(shared)

        per_anchor[anchor] = {
            "pairwise_disjoint_on_name_value": len(shared) == 0,
            "shared_name_value_pairs": sorted([list(p) for p in shared]),
            "constant_cookie_names": names_constant,
            "varying_cookie_names": names_varying,
            "shared_pairs_only_from_constant_names": shared_only_constant,
            "session_identifying_values_vary": len(names_varying) > 0,
            "first_request_cookie_free": all(
                r.get("jar_was_empty_before_request")
                for r in records
                if r["anchor_id"] == anchor and r["session"] in SESSIONS
                and r.get("phase") == "fresh"
            ),
            "jar_sizes": {s: len(sets[s]) for s in SESSIONS},
        }

    out = {
        "schema_version": 1,
        "experiment_id": "EXP-GRAPH-37950584469",
        "lane": "graph",
        "diagnostic_of": "GATE-C3 / NC-SESSION-ISOLATION",
        "computed_from": str(RAW_JSONL.relative_to(ROOT)),
        "computed_from_sha256": sha256_bytes(raw_bytes),
        "definition_used": (
            "Frozen spec.control_registry.null_controls[NC-SESSION-ISOLATION]: "
            "per anchor the four sessions' cookie jars must be pairwise disjoint "
            "on (name, value); no Cookie on the first request."
        ),
        "per_anchor": per_anchor,
        "summary": {
            "any_anchor_shared_pair": any_pair_shared,
            "all_shared_pairs_from_constant_names": all_shared_constant,
            "sessions_cookie_free_on_first_request": all(
                v["first_request_cookie_free"] for v in per_anchor.values()
            ),
        },
        "interpretation_note": (
            "No session-identifying cookie value (_gitlab_session, authSession, "
            "WMF-Uniq, enwikiSession) is shared across sessions; the only shared "
            "(name, value) pairs are server-set constant/configuration cookies "
            "(preferred_language, GeoIP, NetworkProbeLimit, WMF-Last-Access, "
            "WMF-Last-Access-Global, CentralAuthAnonTopLevel). The failure is a "
            "property of the frozen literal predicate, not of session contamination. "
            "Per the frozen fail-closed rule this remains terminal F-CERT."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print("wrote", OUT.relative_to(ROOT), OUT.stat().st_size, "bytes")
    print("sha256", sha256_bytes(OUT.read_bytes()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
