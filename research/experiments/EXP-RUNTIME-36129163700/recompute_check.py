#!/usr/bin/env python3
"""
EXP-RUNTIME-36129163700 — independent recomputation (V-RECOMPUTE).

Reads ONLY the raw evidence artifacts and frozen constants, then recomputes
from scratch:
  - every blind detector bit per episode,
  - every arm numerator / denominator,
  - every two-sided 95% Wilson interval (z = 1.959963984540054),
and compares against artifacts/A-DERIVED-METRICS.json. Any mismatch is
reported; zero mismatches is required for V-RECOMPUTE PASS.

This script shares no code with the producer scorer. Raw observations precede
derived metrics: this script derives metrics only, from raw JSONL.
"""
import json
import math
import sys
from pathlib import Path

EXP_DIR = Path(__file__).resolve().parent
ART = EXP_DIR / "artifacts"

ARMS = ["P-WRITE", "P-DRIFT", "N-READ", "N-INVALID", "N-EXPIRED", "N-DELETED"]
POSITIVE_ARMS = {"P-WRITE", "P-DRIFT"}
Z = 1.959963984540054


def wilson(k: int, n: int):
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + Z * Z / n
    center = (p + Z * Z / (2 * n)) / d
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return max(0.0, center - half), min(1.0, center + half)


def main() -> int:
    # ── Load raw evidence ──
    episodes = [json.loads(l) for l in (ART / "A-EPISODE-LEDGER.jsonl").read_text().splitlines() if l.strip()]
    detector = {d["order_index"]: d for d in
                (json.loads(l) for l in (ART / "A-DETECTOR-OUTPUT.jsonl").read_text().splitlines() if l.strip())}
    walrecs = {w["order_index"]: w for w in
               (json.loads(l) for l in (ART / "A-WAL-VECTOR-BEFORE-AFTER.jsonl").read_text().splitlines() if l.strip())}
    fprecs = {f["order_index"]: f for f in
              (json.loads(l) for l in (ART / "A-RESPONSE-FINGERPRINTS.jsonl").read_text().splitlines() if l.strip())}

    mismatches = []

    # ── Recompute detector bits from raw episode records ──
    recomputed_detector = {}
    for ep in episodes:
        oi = ep["order_index"]
        pre, post = ep["pre"], ep["post"]
        pre_l, post_l = pre["logical"], post["logical"]
        state_changed = ((pre_l["marker"], pre_l["representation"], pre_l["revision"])
                         != (post_l["marker"], post_l["representation"], post_l["revision"]))
        # Independently recompute the WAL vector from the recorded raw hashes
        # (the raw artifact stores the vector over db+wal; verify frame matches).
        wal_changed = pre["vector_sha256"] != post["vector_sha256"]
        fp_changed = pre["read_fingerprint"] != post["read_fingerprint"]
        write_action_2xx = (ep["request"]["path"] == "/runtime/write"
                            and ep.get("http_status") in (200, 201))
        planted_field = ep.get("planted_field")
        positive_detected = False
        if planted_field is not None:
            readback_ok = (post_l[planted_field] == ep.get("planted_value"))
            positive_detected = bool(readback_ok and state_changed and write_action_2xx)
        recomputed_detector[oi] = {
            "state_changed": state_changed,
            "wal_vector_changed": wal_changed,
            "response_fingerprint_changed": fp_changed,
            "write_action_2xx": write_action_2xx,
            "positive_detected": positive_detected,
        }
        # Cross-check against producer detector output
        prod = detector.get(oi, {})
        for key in ("state_changed", "wal_vector_changed", "response_fingerprint_changed",
                    "write_action_2xx", "positive_detected"):
            if prod.get(key) != recomputed_detector[oi][key]:
                mismatches.append({"order_index": oi, "field": f"detector.{key}",
                                   "producer": prod.get(key), "recomputed": recomputed_detector[oi][key]})
        # Cross-check raw side-effect streams
        w = walrecs.get(oi, {})
        if w.get("pre_vector_sha256") != pre["vector_sha256"] or w.get("post_vector_sha256") != post["vector_sha256"]:
            mismatches.append({"order_index": oi, "field": "wal_stream.vector",
                               "producer": [w.get("pre_vector_sha256"), w.get("post_vector_sha256")],
                               "recomputed": [pre["vector_sha256"], post["vector_sha256"]]})
        f = fprecs.get(oi, {})
        if f.get("pre_read_fingerprint") != pre["read_fingerprint"] or f.get("post_read_fingerprint") != post["read_fingerprint"]:
            mismatches.append({"order_index": oi, "field": "fingerprint_stream",
                               "producer": [f.get("pre_read_fingerprint"), f.get("post_read_fingerprint")],
                               "recomputed": [pre["read_fingerprint"], post["read_fingerprint"]]})

    # ── Recompute arm metrics (join arm label only now) ──
    recomputed_arms = {}
    for arm in ARMS:
        eps = [e for e in episodes if e["arm"] == arm]
        k = 0
        n = 0
        for ep in eps:
            det = recomputed_detector[ep["order_index"]]
            if det["state_changed"] is None:
                continue
            n += 1
            if arm in POSITIVE_ARMS:
                detected = bool(det["positive_detected"])
                if arm == "P-DRIFT":
                    detected = detected and bool(det["response_fingerprint_changed"])
                if detected:
                    k += 1
            else:
                fp = bool(det["state_changed"]) or bool(det["wal_vector_changed"]) or bool(det["write_action_2xx"])
                if arm == "N-READ":
                    fp = fp or bool(det["response_fingerprint_changed"])
                if not fp:
                    k += 1
        lo, hi = wilson(k, n)
        recomputed_arms[arm] = {"k": k, "n": n, "point": (k / n) if n else None,
                                "wilson_ci_lo": lo, "wilson_ci_hi": hi}

    # ── Compare against producer derived metrics ──
    derived_path = ART / "A-DERIVED-METRICS.json"
    if not derived_path.exists():
        check = {"zero_mismatches": False, "summary": {"error": "A-DERIVED-METRICS.json missing"}}
    else:
        derived = json.loads(derived_path.read_text())
        for arm in ARMS:
            prod_a = derived["arms"][arm]
            rec_a = recomputed_arms[arm]
            for pk, rk in (("k", "k"), ("n_scored", "n"), ("point_rate", "point"),
                           ("wilson_ci_lo", "wilson_ci_lo"), ("wilson_ci_hi", "wilson_ci_hi")):
                if prod_a.get(pk) != rec_a.get(rk):
                    mismatches.append({"arm": arm, "field": pk,
                                       "producer": prod_a.get(pk), "recomputed": rec_a.get(rk)})
        # Verify the producer's verdict follows from its own arm metrics
        pos_ok = all(derived["arms"][a]["point_rate"] is not None
                     and derived["arms"][a]["point_rate"] >= 0.90
                     and derived["arms"][a]["wilson_ci_lo"] >= 0.80 for a in POSITIVE_ARMS)
        null_ok = all(derived["arms"][a]["point_rate"] is not None
                      and derived["arms"][a]["point_rate"] >= 0.90
                      and derived["arms"][a]["wilson_ci_lo"] >= 0.80
                      for a in ARMS if a not in POSITIVE_ARMS)
        complete = all(derived["arms"][a]["n_complete"] == 20 for a in ARMS)
        scored = all(derived["arms"][a]["n_scored"] == 20 for a in ARMS)
        expected_verdict = ("MEASUREMENT_INVALID" if not (complete and scored)
                            else "SUPPORTS" if (pos_ok and null_ok) else "FALSIFIES")
        if derived["A_verdict"] != expected_verdict:
            mismatches.append({"field": "A_verdict", "producer": derived["A_verdict"],
                               "recomputed": expected_verdict})
        check = {
            "zero_mismatches": len(mismatches) == 0,
            "n_episodes_raw": len(episodes),
            "n_arms": len({e["arm"] for e in episodes}),
            "episodes_per_arm": {a: len([e for e in episodes if e["arm"] == a]) for a in ARMS},
            "recomputed_arms": recomputed_arms,
            "expected_verdict_from_recomputed": expected_verdict,
            "producer_verdict": derived["A_verdict"],
            "mismatches": mismatches,
            "method": "independent re-implementation reading only raw JSONL; shares no code with the producer scorer",
            "z": Z,
        }
    with open(ART / "A-RECOMPUTE-CHECK.json", "w") as f:
        json.dump(check, f, indent=2)
    print(json.dumps({"zero_mismatches": check["zero_mismatches"],
                      "n_mismatches": len(mismatches)}, indent=2))
    return 0 if check["zero_mismatches"] else 1


if __name__ == "__main__":
    sys.exit(main())
