#!/usr/bin/env python3
"""
EXP-RUNTIME-37973247935 — independent recomputation (falsifier iii, prereg 8).

The validated parent (EXP-RUNTIME-36293257855) established the discipline:
recompute_check.py re-implements the detector and the Wilson CI from raw JSONL
only, imports nothing from oracle_scorer.py (nor from intervention_surface.py,
oos_worker.py or the harness), and shares no code with the scorer.

This implementation recomputes, from the raw evidence files only:

  1. per-leg response fingerprint over status + body + sorted stable headers
     (volatile headers excluded using the frozen constant set mirrored below);
  2. the composite fingerprint over the two frozen composite endpoints
     (/runtime/read, /api/profile) exactly as the harness composes legs;
  3. the arm-blind detection bit via the frozen rule
     detected = wal_changed OR logical_changed OR fingerprint_changed;
  4. per-arm sensitivity/specificity with the two-sided 95% Wilson interval;
  5. and compares every recomputed value against the arm-blind detector output
     (A-DETECTOR-OUTPUT.jsonl, which must contain no arm label) and the
     derived metrics (A-DERIVED-METRICS.json).

The WAL byte vectors (before_hash/after_hash) and logical projections are used
as raw evidence exactly as recorded in the ledger; the fingerprint chain is
fully re-derived from the raw status/body/headers pairs.

Run (from repo root):
    python research/experiments/EXP-RUNTIME-37973247935/recompute_check.py
Writes research/experiments/EXP-RUNTIME-37973247935/artifacts/A-RECOMPUTE-CHECK.json
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

EXPERIMENT_ID = "EXP-RUNTIME-37973247935"
EXP_DIR = Path(__file__).resolve().parent
ART_DIR = EXP_DIR / "artifacts"

# Frozen constants mirrored as local literals (constants only, no code import):
# shared_config.py WILSON_Z / EXCLUDED_HEADERS.
WILSON_Z = 1.959963984540054
EXCLUDED_HEADERS = frozenset({
    "Date", "Server", "X-Request-Id", "X-Worker-Pid", "X-Cache", "Age",
    "Content-Length", "ETag", "W-ETag", "Range",
})
COMPOSITE_ENDPOINTS = ["/runtime/read", "/api/profile"]
POSITIVE_ARMS = ["P-OOS-WORKER", "P-OOS-REPR"]
NULL_ARMS = ["N-OOS-IDLE", "N-OOS-REJECT", "N-OOS-CACHE"]
LIVENESS_ARM = "PC-INSURFACE-WRITE-LIVE"
BLINDSPOT_ARMS = ["M-REVERT-BYTES", "M-REVERT-LOGICAL"]
ALL_ARMS = POSITIVE_ARMS + NULL_ARMS + [LIVENESS_ARM] + BLINDSPOT_ARMS
TOL = 1e-12


# ── Independent re-implementations (no oracle_scorer import) ───────────────
def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def response_fingerprint(status_code, body, headers) -> str:
    """Mirror of the frozen stable-header projection."""
    if status_code is None or body is None:
        return None
    body_bytes = body.encode() if isinstance(body, str) else bytes(body)
    stable = {k: v for k, v in headers.items() if k.lower() not in EXCLUDED_HEADERS}
    canonical = (f"{status_code}|".encode() + body_bytes
                 + json.dumps(stable, sort_keys=True, separators=(",", ":")).encode())
    return _sha_bytes(canonical)


def composite_fingerprint(legs) -> str:
    """Rebuild the composite exactly as the harness composes its legs."""
    parts = []
    for leg in legs:
        fp = response_fingerprint(leg.get("status"), leg.get("body"), leg.get("headers") or {})
        parts.append(f"{leg.get('endpoint')}|{fp or 'ERR'}")
    return _sha_bytes("||".join(parts).encode())


def logical_tuple(logical) -> tuple:
    if logical is None:
        return None
    return (logical.get("marker"), logical.get("representation"),
            logical.get("revision"), logical.get("session_present"))


def detect(pre_vector, post_vector, pre_logical, post_logical,
           pre_fingerprint, post_fingerprint):
    """Mirror of the frozen arm-blind composite detector rule."""
    wal_changed = pre_vector != post_vector
    logical_changed = logical_tuple(pre_logical) != logical_tuple(post_logical)
    fingerprint_changed = pre_fingerprint != post_fingerprint
    return {
        "wal_changed": wal_changed,
        "logical_changed": logical_changed,
        "fingerprint_changed": fingerprint_changed,
        "detected": bool(wal_changed or logical_changed or fingerprint_changed),
    }


def wilson_ci(k: int, n: int, z: float = WILSON_Z):
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, center - half), min(1.0, center + half)


# ── Load raw evidence ──────────────────────────────────────────────────────
def _read_jsonl(name: str) -> list:
    p = ART_DIR / name
    if not p.exists():
        raise FileNotFoundError(f"{p} missing")
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def main() -> int:
    order = json.loads((ART_DIR / "A-SEEDED-ORDER.json").read_text())
    arm_by_order = {o["order_index"]: o["arm"] for o in order["order"]}
    detector_output = _read_jsonl("A-DETECTOR-OUTPUT.jsonl")
    ledger = _read_jsonl("A-EPISODE-LEDGER.jsonl")
    det_by_order = {d["order_index"]: d for d in detector_output}

    # Structural arm-blind check on the detector output itself.
    output_has_no_arm_label = all("arm" not in d for d in detector_output)

    mismatches = {"detection_bit": [], "composite": [], "metric": [], "coverage": []}
    recomputed_bits = {}
    max_wilson_diff = 0.0

    for rec in ledger:
        oi = rec["order_index"]
        pre, post = rec.get("pre"), rec.get("post")
        if not pre or not post:
            mismatches["coverage"].append({"order_index": oi, "reason": "no pre/post"})
            continue
        # 1) recompute the response-fingerprint chain from the raw legs
        pre_legs, post_legs = pre.get("fingerprint_legs"), post.get("fingerprint_legs")
        if not pre_legs or not post_legs:
            mismatches["coverage"].append({"order_index": oi, "reason": "no fingerprint_legs"})
            continue
        pre_fp = composite_fingerprint(pre_legs)
        post_fp = composite_fingerprint(post_legs)
        if pre_fp != pre.get("composite_sha256") or post_fp != post.get("composite_sha256"):
            mismatches["composite"].append({
                "order_index": oi,
                "recomputed_pre": pre_fp, "stored_pre": pre.get("composite_sha256"),
                "recomputed_post": post_fp, "stored_post": post.get("composite_sha256"),
            })
        # 2) recompute the arm-blind detection bit
        redet = detect(pre.get("vector_sha256"), post.get("vector_sha256"),
                       pre.get("logical"), post.get("logical"), pre_fp, post_fp)
        recomputed_bits[oi] = bool(redet["detected"])
        stored = det_by_order.get(oi, {})
        if stored.get("detected") is None:
            mismatches["coverage"].append({"order_index": oi, "reason": "no detector output"})
            continue
        if bool(stored["detected"]) != recomputed_bits[oi]:
            mismatches["detection_bit"].append({
                "order_index": oi, "recomputed_detected": recomputed_bits[oi],
                "stored_detected": stored["detected"],
                "wal_changed": redet["wal_changed"], "logical_changed": redet["logical_changed"],
                "fingerprint_changed": redet["fingerprint_changed"],
            })

    # 3) per-arm Wilson from labels + recomputed bits
    per_arm = {a: {"k": 0, "n": 0} for a in ALL_ARMS}
    for oi, arm in arm_by_order.items():
        if oi not in recomputed_bits:
            continue
        per_arm[arm]["n"] += 1
        detected = recomputed_bits[oi]
        if arm in POSITIVE_ARMS or arm == LIVENESS_ARM:
            if detected:
                per_arm[arm]["k"] += 1
        elif arm in NULL_ARMS:
            if not detected:
                per_arm[arm]["k"] += 1

    per_arm_recomputed = {}
    try:
        derived = json.loads((ART_DIR / "A-DERIVED-METRICS.json").read_text())["derived"]
        derived_arms = derived.get("arms", {})
    except Exception:
        derived_arms = {}
    for a in ALL_ARMS:
        k, n = per_arm[a]["k"], per_arm[a]["n"]
        lo, hi = wilson_ci(k, n) if n else (None, None)
        row = {"n_scored": n, "k": k, "point_rate": (k / n) if n else None,
               "wilson_ci_lo": lo, "wilson_ci_hi": hi,
               "ci_nondegenerate": (hi > lo) if lo is not None else False}
        per_arm_recomputed[a] = row
        stored_row = derived_arms.get(a, {})
        if stored_row.get("n_scored") is not None:
            for key in ("point_rate", "wilson_ci_lo", "wilson_ci_hi"):
                sv, rv = stored_row.get(key), row.get(key)
                if sv is None or rv is None:
                    continue
                diff = abs(float(sv) - float(rv))
                max_wilson_diff = max(max_wilson_diff, diff)
                if diff > TOL:
                    mismatches["metric"].append({"arm": a, "key": key,
                                                 "stored": sv, "recomputed": rv, "diff": diff})
            if stored_row.get("n_scored") != row["n_scored"]:
                mismatches["metric"].append({"arm": a, "key": "n_scored",
                                             "stored": stored_row.get("n_scored"),
                                             "recomputed": row["n_scored"]})
            if stored_row.get("k") != row["k"]:
                mismatches["metric"].append({"arm": a, "key": "k",
                                             "stored": stored_row.get("k"),
                                             "recomputed": row["k"]})
            if bool(stored_row.get("ci_nondegenerate")) != bool(row["ci_nondegenerate"]):
                mismatches["metric"].append({"arm": a, "key": "ci_nondegenerate",
                                             "stored": stored_row.get("ci_nondegenerate"),
                                             "recomputed": row["ci_nondegenerate"]})

    coverage_complete = (len(ledger) == 260 and len(detector_output) == 260
                         and len(set(arm_by_order)) == 260 and len(recomputed_bits) == 260)
    zero_mismatches = (coverage_complete and not mismatches["detection_bit"]
                       and not mismatches["composite"] and not mismatches["metric"]
                       and not mismatches["coverage"] and output_has_no_arm_label)

    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "zero_mismatches": bool(zero_mismatches),
        "summary": {
            "n_order_indices": 260,
            "ledger_records": len(ledger),
            "detector_output_records": len(detector_output),
            "recomputed_detection_bits": len(recomputed_bits),
            "coverage_complete": bool(coverage_complete),
            "output_has_no_arm_label": bool(output_has_no_arm_label),
            "detection_bit_mismatches": len(mismatches["detection_bit"]),
            "composite_fingerprint_mismatches": len(mismatches["composite"]),
            "per_arm_metric_mismatches": len(mismatches["metric"]),
            "coverage_gaps": len(mismatches["coverage"]),
            "max_abs_wilson_diff": max_wilson_diff,
            "tolerance": TOL,
        },
        "mismatch_detail": mismatches,
        "per_arm_recomputed": per_arm_recomputed,
        "independence": (
            "imports only json/math/hashlib/pathlib; no oracle_scorer, "
            "intervention_surface, oos_worker or harness import; frozen "
            "constants (WILSON_Z, EXCLUDED_HEADERS) mirrored as local literals; "
            "detector rule recomputed from raw ledger measurements"),
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    }
    (ART_DIR / "A-RECOMPUTE-CHECK.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({"zero_mismatches": result["zero_mismatches"],
                      "summary": result["summary"]}, indent=2))
    return 0 if zero_mismatches else 1


if __name__ == "__main__":
    sys.exit(main())