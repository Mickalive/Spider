#!/usr/bin/env python3
"""
EXP-RUNTIME-36293257855 — independent recomputation (V-RECOMPUTE).

Reads ONLY raw evidence artifacts and frozen constants, then re-derives from
scratch:
  * every arm-blind composite detector bit per episode
    (wal_changed OR logical_changed OR fingerprint_changed),
  * every arm numerator / denominator (arm labels joined only after the bits),
  * every two-sided 95% Wilson score interval (z = 1.959963984540054),
and compares against artifacts/A-DERIVED-METRICS.json. Any mismatch is
reported; zero mismatches is required for V-RECOMPUTE PASS.

Raw inputs (never the producer scorer's code):
  - artifacts/A-SEEDED-ORDER.json          (episode order + arm labels)
  - artifacts/A-EPISODE-LEDGER.jsonl       (raw pre/post measurements)
  - artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl
  - artifacts/A-DETECTOR-OUTPUT.jsonl      (producer arm-blind bits)
  - artifacts/A-DERIVED-METRICS.json       (the object being checked)

This script shares no code with research/runtime/oracle_scorer.py. It
re-implements the frozen detector and Wilson formula from the raw records.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

EXP_DIR = Path(__file__).resolve().parent
ART = EXP_DIR / "artifacts"

ARMS = ["P-WRITE", "P-DRIFT", "N-READ", "N-INVALID", "N-EXPIRED", "N-DELETED"]
POSITIVE_ARMS = {"P-WRITE", "P-DRIFT"}
NULL_ARMS = {"N-READ", "N-INVALID", "N-EXPIRED", "N-DELETED"}
Z = 1.959963984540054
POINT_MIN = 0.90
WILSON_LO_MIN = 0.80


def _load_jsonl(name: str):
    p = ART / name
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def _logical_tuple(logical):
    if logical is None:
        return None
    return (logical.get("marker"), logical.get("representation"),
            logical.get("revision"), logical.get("session_present"))


def _wilson(k: int, n: int):
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + Z * Z / n
    center = (p + Z * Z / (2 * n)) / d
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return max(0.0, center - half), min(1.0, center + half)


def main() -> int:
    mismatches = []

    order = json.loads((ART / "A-SEEDED-ORDER.json").read_text())["order"]
    episodes = {e["order_index"]: e for e in _load_jsonl("A-EPISODE-LEDGER.jsonl")}
    wal_stream = {w["order_index"]: w for w in _load_jsonl("A-WAL-VECTOR-BEFORE-AFTER.jsonl")}
    producer_det = {d["order_index"]: d for d in _load_jsonl("A-DETECTOR-OUTPUT.jsonl")}

    # ── Re-derive the arm-blind detector bit from raw measurements ──
    recomputed_det = {}
    for entry in order:
        oi = entry["order_index"]
        ep = episodes.get(oi)
        if ep is None or not ep.get("completed"):
            recomputed_det[oi] = {"wal_changed": None, "logical_changed": None,
                                  "fingerprint_changed": None, "detected": None,
                                  "reason": "episode missing or not completed"}
            continue
        pre, post = ep.get("pre"), ep.get("post")
        if not pre or not post:
            recomputed_det[oi] = {"wal_changed": None, "logical_changed": None,
                                  "fingerprint_changed": None, "detected": None,
                                  "reason": "raw pre/post measurements missing"}
            continue
        wal_changed = pre.get("vector_sha256") != post.get("vector_sha256")
        logical_changed = _logical_tuple(pre.get("logical")) != _logical_tuple(post.get("logical"))
        fingerprint_changed = pre.get("read_fingerprint") != post.get("read_fingerprint")
        detected = bool(wal_changed or logical_changed or fingerprint_changed)
        recomputed_det[oi] = {"wal_changed": wal_changed, "logical_changed": logical_changed,
                              "fingerprint_changed": fingerprint_changed, "detected": detected}

        # Cross-check the producer's arm-blind detector output
        prod = producer_det.get(oi)
        if prod is None:
            mismatches.append({"order_index": oi, "field": "detector.missing",
                               "producer": None, "recomputed": "present"})
        else:
            for key in ("wal_changed", "logical_changed", "fingerprint_changed", "detected"):
                if prod.get(key) != recomputed_det[oi][key]:
                    mismatches.append({"order_index": oi, "field": f"detector.{key}",
                                       "producer": prod.get(key),
                                       "recomputed": recomputed_det[oi][key]})

        # Cross-check the raw side-effect streams against the ledger
        w = wal_stream.get(oi)
        if w is None:
            mismatches.append({"order_index": oi, "field": "wal_stream.missing",
                               "producer": None, "recomputed": None})
        elif (w.get("before_hash") != pre.get("vector_sha256")
              or w.get("after_hash") != post.get("vector_sha256")):
            mismatches.append({"order_index": oi, "field": "wal_stream.vector",
                               "producer": [w.get("before_hash"), w.get("after_hash")],
                               "recomputed": [pre.get("vector_sha256"), post.get("vector_sha256")]})
        elif w.get("wal_changed") != wal_changed:
            mismatches.append({"order_index": oi, "field": "wal_stream.wal_changed",
                               "producer": w.get("wal_changed"), "recomputed": wal_changed})

    # ── Join arm labels only now and recompute per-arm sensitivity/specificity ──
    recomputed_arms = {}
    for arm in ARMS:
        k = n = 0
        for entry in order:
            if entry["arm"] != arm:
                continue
            det = recomputed_det.get(entry["order_index"], {})
            if det.get("detected") is None:
                continue
            n += 1
            if arm in POSITIVE_ARMS:
                if det["detected"]:
                    k += 1
            else:
                if not det["detected"]:
                    k += 1
        lo, hi = _wilson(k, n)
        point = (k / n) if n else None
        recomputed_arms[arm] = {
            "n_scored": n, "k": k, "point_rate": point,
            "wilson_ci_lo": lo, "wilson_ci_hi": hi,
            "ci_nondegenerate": hi > lo,
        }

    def _arm_ok(a):
        r = recomputed_arms[a]
        return (r["point_rate"] is not None and r["point_rate"] >= POINT_MIN
                and r["wilson_ci_lo"] >= WILSON_LO_MIN and r["ci_nondegenerate"])

    recomputed_all_arms_pass = all(_arm_ok(a) for a in ARMS)
    recomputed_verdict = "SUPPORTS" if recomputed_all_arms_pass else "FALSIFIES"

    # ── Compare against the producer's derived metrics ──
    derived_path = ART / "A-DERIVED-METRICS.json"
    if not derived_path.exists():
        check = {"zero_mismatches": False,
                 "summary": {"error": "A-DERIVED-METRICS.json missing"}}
    else:
        derived = json.loads(derived_path.read_text())
        for arm in ARMS:
            prod_a = derived.get("arms", {}).get(arm, {})
            rec_a = recomputed_arms[arm]
            for pk in ("k", "n_scored", "point_rate", "wilson_ci_lo", "wilson_ci_hi",
                       "ci_nondegenerate"):
                if prod_a.get(pk) != rec_a.get(pk):
                    mismatches.append({"arm": arm, "field": pk,
                                       "producer": prod_a.get(pk), "recomputed": rec_a.get(pk)})
        if derived.get("matrix_verdict") != recomputed_verdict:
            mismatches.append({"field": "matrix_verdict", "producer": derived.get("matrix_verdict"),
                               "recomputed": recomputed_verdict})
        if bool(derived.get("all_arms_pass")) != recomputed_all_arms_pass:
            mismatches.append({"field": "all_arms_pass",
                               "producer": derived.get("all_arms_pass"),
                               "recomputed": recomputed_all_arms_pass})

        check = {
            "zero_mismatches": len(mismatches) == 0,
            "n_episodes_raw": len(episodes),
            "n_episodes_ordered": len(order),
            "n_arms": len({e["arm"] for e in order}),
            "episodes_per_arm": {a: sum(1 for e in order if e["arm"] == a) for a in ARMS},
            "recomputed_arms": recomputed_arms,
            "recomputed_all_arms_pass": recomputed_all_arms_pass,
            "recomputed_verdict": recomputed_verdict,
            "producer_verdict": derived.get("matrix_verdict"),
            "mismatches": mismatches,
            "method": ("independent re-implementation reading only raw JSONL and A-SEEDED-ORDER.json; "
                       "shares no code with the producer scorer; arm labels joined only after the bits"),
            "z": Z,
            "thresholds": {"point_min": POINT_MIN, "wilson_lo_min": WILSON_LO_MIN,
                           "non_degenerate": True},
        }

    with open(ART / "A-RECOMPUTE-CHECK.json", "w") as f:
        json.dump(check, f, indent=2)

    print(json.dumps({"zero_mismatches": check["zero_mismatches"],
                      "n_mismatches": len(mismatches), "n_episodes_raw": check.get("n_episodes_raw")},
                     indent=2))
    return 0 if check["zero_mismatches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
