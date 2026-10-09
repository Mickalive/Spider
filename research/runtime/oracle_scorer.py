#!/usr/bin/env python3
"""
SPIDER Research 2.0 — runtime lane ORACLE SCORER (detector).

This module owns, and only owns, the composite intervention detector and its
statistics for EXP-RUNTIME-36293257855:

  * WAL byte vector capture: length-framed SHA-256 over `/tmp/single.db` plus
    `/tmp/single.db-wal` (both files fully read, length-prefixed);
  * logical projection extraction: read-only SQL projection of the controlled
    `runtime_probe` row plus the target session's presence;
  * response fingerprint: SHA-256 over status + body + sorted stable headers
    after excluding the frozen volatile-header set;
  * composite arm-blind detection:
        detected = (wal_changed OR logical_changed OR fingerprint_changed);
  * two-sided 95% Wilson score intervals;
  * arm-label join and per-arm sensitivity/specificity accounting.

Authorship separation (spec `measurement_validity.authorship_separation`,
prereg section 6.2): this module must NOT import `intervention_surface` or any
Flask/app code. It may import the constants-only `shared_config` module. The
detector is arm-blind: it never receives the arm label, the planted value, the
token class or any expected outcome.
"""
from __future__ import annotations

import hashlib
import json
import math
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from research.runtime import shared_config as SC

_EXCLUDED_LOWER = frozenset(h.lower() for h in SC.EXCLUDED_HEADERS)


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ── WAL byte vector (raw evidence) ─────────────────────────────────────────
def wal_vector_capture(db_path: str = SC.DB_PATH) -> Dict[str, Any]:
    """Length-framed SHA-256 over the raw DB and WAL bytes. The -shm file is
    recorded diagnostically only and never enters the vector."""
    db_p = Path(db_path)
    wal_p = Path(db_path + "-wal")
    shm_p = Path(db_path + "-shm")
    db_bytes = db_p.read_bytes() if db_p.exists() else b""
    wal_bytes = wal_p.read_bytes() if wal_p.exists() else b""
    shm_bytes = shm_p.read_bytes() if shm_p.exists() else b""
    frame = (len(db_bytes).to_bytes(8, "big") + db_bytes
             + len(wal_bytes).to_bytes(8, "big") + wal_bytes)
    return {
        "vector_sha256": _sha_bytes(frame),
        "db_bytes": len(db_bytes), "db_sha256": _sha_bytes(db_bytes),
        "wal_bytes": len(wal_bytes), "wal_sha256": _sha_bytes(wal_bytes),
        "shm_bytes": len(shm_bytes), "shm_sha256": _sha_bytes(shm_bytes),
    }


# ── Logical projection (read-only SQL) ─────────────────────────────────────
def logical_projection(sid: str, db_path: str = SC.DB_PATH) -> Dict[str, Any]:
    """Read-only projection of the controlled row and the target session.
    Never writes and never checkpoints."""
    conn = sqlite3.connect(db_path, timeout=10, check_same_thread=False)
    try:
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA wal_autocheckpoint=0")
        row = conn.execute(
            "SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1"
        ).fetchone()
        srow = conn.execute("SELECT id FROM sessions WHERE sid=? AND valid=1", (sid,)).fetchone()
        return {
            "marker": row[0] if row else None,
            "representation": row[1] if row else None,
            "revision": row[2] if row else None,
            "updated_at": row[3] if row else None,
            "session_present": srow is not None,
        }
    finally:
        conn.close()


# ── Response fingerprint ───────────────────────────────────────────────────
def response_fingerprint(status_code: int, body: Any, headers: Dict[str, str]) -> Optional[str]:
    """Stable projection of a controlled response. Volatile headers are
    excluded case-insensitively; a missing status/body is unknown, not a hash
    of emptiness."""
    if status_code is None or body is None:
        return None
    body_bytes = body.encode() if isinstance(body, str) else bytes(body)
    stable = {k: v for k, v in headers.items() if k.lower() not in _EXCLUDED_LOWER}
    canonical = (f"{status_code}|".encode() + body_bytes
                 + json.dumps(stable, sort_keys=True, separators=(",", ":")).encode())
    return _sha_bytes(canonical)


# ── Composite arm-blind detector ───────────────────────────────────────────
def _logical_tuple(logical: Optional[Dict[str, Any]]) -> Optional[Tuple]:
    if logical is None:
        return None
    return (logical.get("marker"), logical.get("representation"),
            logical.get("revision"), logical.get("session_present"))


def detect(*, pre_vector_sha256: Optional[str], post_vector_sha256: Optional[str],
           pre_logical: Optional[Dict[str, Any]], post_logical: Optional[Dict[str, Any]],
           pre_fingerprint: Optional[str], post_fingerprint: Optional[str]) -> Dict[str, Any]:
    """Arm-blind composite detection. The caller passes only raw measurements:
    no arm label, no planted value, no token class, no expected status."""
    missing = [name for name, val in (
        ("pre_vector_sha256", pre_vector_sha256), ("post_vector_sha256", post_vector_sha256),
        ("pre_logical", pre_logical), ("post_logical", post_logical),
        ("pre_fingerprint", pre_fingerprint), ("post_fingerprint", post_fingerprint),
    ) if val is None]
    if missing:
        return {"wal_changed": None, "logical_changed": None, "fingerprint_changed": None,
                "detected": None, "detector_error": f"missing raw measurement(s): {missing}"}
    wal_changed = pre_vector_sha256 != post_vector_sha256
    logical_changed = _logical_tuple(pre_logical) != _logical_tuple(post_logical)
    fingerprint_changed = pre_fingerprint != post_fingerprint
    return {
        "wal_changed": wal_changed,
        "logical_changed": logical_changed,
        "fingerprint_changed": fingerprint_changed,
        "detected": bool(wal_changed or logical_changed or fingerprint_changed),
    }


# ── Statistics ─────────────────────────────────────────────────────────────
def wilson_ci(k: int, n: int, z: float = SC.WILSON_Z) -> Tuple[float, float]:
    """Two-sided 95% Wilson score interval (frozen z)."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, center - half), min(1.0, center + half)


def score_arms(detector_records: List[Dict[str, Any]],
               arm_by_order: Dict[int, str]) -> Dict[str, Any]:
    """Join arm labels to already-written arm-blind detector output and compute
    per-arm sensitivity/specificity with two-sided 95% Wilson intervals."""
    per_arm: Dict[str, Dict[str, Any]] = {arm: {"k": 0, "n": 0, "per_episode": []} for arm in SC.ARMS}
    det_by_order = {d["order_index"]: d for d in detector_records}
    for order_index, arm in arm_by_order.items():
        det = det_by_order.get(order_index, {})
        bucket = per_arm[arm]
        if det.get("detected") is None:
            bucket["per_episode"].append({"order_index": order_index, "scored": False,
                                          "reason": det.get("detector_error", "missing detector output")})
            continue
        bucket["n"] += 1
        if arm in SC.POSITIVE_ARMS:
            if det["detected"]:
                bucket["k"] += 1
            bucket["per_episode"].append({"order_index": order_index, "scored": True,
                                          "detected": bool(det["detected"])})
        else:
            if not det["detected"]:
                bucket["k"] += 1
            bucket["per_episode"].append({"order_index": order_index, "scored": True,
                                          "false_positive": bool(det["detected"])})
    arm_results: Dict[str, Any] = {}
    for arm in SC.ARMS:
        k, n = per_arm[arm]["k"], per_arm[arm]["n"]
        point = (k / n) if n else None
        ci_lo, ci_hi = wilson_ci(k, n) if n else (None, None)
        arm_results[arm] = {
            "n_scored": n,
            "k": k,
            "estimand": "sensitivity" if arm in SC.POSITIVE_ARMS else "specificity",
            "point_rate": point,
            "wilson_ci_lo": ci_lo,
            "wilson_ci_hi": ci_hi,
            "ci_nondegenerate": (ci_hi > ci_lo) if (ci_lo is not None) else False,
            "per_episode": per_arm[arm]["per_episode"],
        }

    def _arm_ok(a: str) -> bool:
        r = arm_results[a]
        return (r["point_rate"] is not None and r["point_rate"] >= SC.THRESH_POINT
                and r["wilson_ci_lo"] is not None and r["wilson_ci_lo"] >= SC.THRESH_WILSON_LO
                and r["ci_nondegenerate"])

    all_arms_ok = all(_arm_ok(a) for a in SC.ARMS)
    return {
        "z": SC.WILSON_Z,
        "thresholds": {"point_min": SC.THRESH_POINT, "wilson_lo_min": SC.THRESH_WILSON_LO,
                       "non_degenerate": True},
        "arms": arm_results,
        "all_arms_pass": all_arms_ok,
        "positive_arms_pass": all(_arm_ok(a) for a in SC.POSITIVE_ARMS),
        "null_arms_pass": all(_arm_ok(a) for a in SC.NULL_ARMS),
        "all_intervals_nondegenerate": all(arm_results[a]["ci_nondegenerate"] for a in SC.ARMS),
        "matrix_verdict": "SUPPORTS" if all_arms_ok else "FALSIFIES",
    }
