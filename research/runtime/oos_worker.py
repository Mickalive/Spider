#!/usr/bin/env python3
"""
SPIDER Research 2.0 — runtime lane OUT-OF-SURFACE WORKER (ground-truth provider).

This module owns, and only owns, the out-of-surface ground-truth mutations for
EXP-RUNTIME-37973247935. It is the component-level analogue of
`intervention_surface.py` for the out-of-surface scope: it connects DIRECTLY to
`/tmp/single.db` with `wal_autocheckpoint=0` and bypasses the Flask surface (and
therefore every controlled route) entirely.

Modes (frozen design, prereg section 5.1 / spec.measurement_validity):

  * commit_probe_update   — direct committed SQLite UPDATE of the controlled
                            `runtime_probe` row (marker/revision/updated_at)
  * commit_representation — direct committed SQLite UPDATE of the `body_config`
                            row (variant/content) that changes the body served
                            by the stable-header /api endpoints
  * idle                  — connect, read-only SELECT, close; no write/commit
  * reject_rollback       — attempt a mutation that violates CHECK(id=1) on
                            `runtime_probe`, then ROLLBACK; no committed change

Authorship separation (spec.measurement_validity.authorship_separation):
this module MUST NOT import `intervention_surface` or `oracle_scorer`, and MUST
NOT be imported by `oracle_scorer`. It may import the constants-only
`shared_config` module. It contains no detector logic and no scoring.

Every invocation returns a structured raw-evidence record (mode, SQL,
before/after row, committed, exception) and never fabricates success.
"""
from __future__ import annotations

import sqlite3
import time
from typing import Any, Dict, List, Optional

from research.runtime import shared_config as SC

_PROBE_COLS = ("marker", "representation", "revision", "updated_at")


def _utc_ts() -> float:
    return time.time()


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, timeout=10, check_same_thread=False)
    conn.execute("PRAGMA busy_timeout=5000")
    # Frozen substrate contract: no checkpoint/compaction on ANY connection.
    conn.execute("PRAGMA wal_autocheckpoint=0")
    conn.row_factory = sqlite3.Row
    return conn


def read_probe(db_path: str = SC.DB_PATH) -> Optional[Dict[str, Any]]:
    """Read-only projection of the controlled row. Never writes."""
    conn = _connect(db_path)
    try:
        row = conn.execute(
            "SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1"
        ).fetchone()
        if row is None:
            return None
        return {k: row[k] for k in _PROBE_COLS}
    finally:
        conn.close()


def read_body_config(db_path: str = SC.DB_PATH) -> Optional[Dict[str, Any]]:
    conn = _connect(db_path)
    try:
        row = conn.execute("SELECT variant, content FROM body_config WHERE id=1").fetchone()
        if row is None:
            return None
        return {"variant": row["variant"], "content": row["content"]}
    finally:
        conn.close()


def _ev(mode: str, sql: str, before: Any, after: Any, committed: bool,
        exception: Optional[str] = None) -> Dict[str, Any]:
    return {
        "mode": mode, "sql": sql, "before": before, "after": after,
        "committed": committed, "exception": exception,
        "invoked_at": _utc_ts(),
    }


def commit_probe_update(db_path: str = SC.DB_PATH,
                        marker: Optional[str] = None) -> Dict[str, Any]:
    """Direct committed UPDATE of the controlled runtime_probe row."""
    if not marker:
        marker = f"oos_{time.time_ns()}"
    conn = _connect(db_path)
    try:
        before = conn.execute(
            "SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1"
        ).fetchone()
        before = {k: before[k] for k in _PROBE_COLS} if before else None
        conn.execute(
            "UPDATE runtime_probe SET marker=?, revision=revision+1, updated_at=? WHERE id=1",
            (marker, _utc_ts()))
        conn.commit()
        after = conn.execute(
            "SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1"
        ).fetchone()
        after = {k: after[k] for k in _PROBE_COLS} if after else None
        return _ev("commit_probe_update",
                   "UPDATE runtime_probe SET marker=?, revision=revision+1, updated_at=? WHERE id=1",
                   before, after, True)
    except Exception as e:  # pragma: no cover - defensive
        try:
            conn.rollback()
        except Exception:
            pass
        return _ev("commit_probe_update",
                   "UPDATE runtime_probe SET marker=?, revision=revision+1, updated_at=? WHERE id=1",
                   None, None, False, f"{type(e).__name__}: {e}")
    finally:
        conn.close()


def commit_representation(db_path: str = SC.DB_PATH, variant: str = "B",
                          content: Optional[str] = None) -> Dict[str, Any]:
    """Direct committed UPDATE of the body_config row (changes served /api body)."""
    if content is None:
        content = SC.BODY_STATES.get(variant, SC.BODY_STATES["A"])["json"]
    conn = _connect(db_path)
    try:
        before = conn.execute("SELECT variant, content FROM body_config WHERE id=1").fetchone()
        before = {"variant": before["variant"], "content": before["content"]} if before else None
        conn.execute("UPDATE body_config SET variant=?, content=? WHERE id=1", (variant, content))
        conn.commit()
        after = conn.execute("SELECT variant, content FROM body_config WHERE id=1").fetchone()
        after = {"variant": after["variant"], "content": after["content"]} if after else None
        return _ev("commit_representation",
                   "UPDATE body_config SET variant=?, content=? WHERE id=1",
                   before, after, True)
    except Exception as e:  # pragma: no cover - defensive
        try:
            conn.rollback()
        except Exception:
            pass
        return _ev("commit_representation",
                   "UPDATE body_config SET variant=?, content=? WHERE id=1",
                   None, None, False, f"{type(e).__name__}: {e}")
    finally:
        conn.close()


def idle(db_path: str = SC.DB_PATH) -> Dict[str, Any]:
    """Connect, read-only SELECT, close. No write and no commit."""
    conn = _connect(db_path)
    try:
        row = conn.execute("SELECT marker, revision FROM runtime_probe WHERE id=1").fetchone()
        observed = {"marker": row["marker"], "revision": row["revision"]} if row else None
        return _ev("idle", "SELECT marker, revision FROM runtime_probe WHERE id=1",
                   observed, observed, False)
    except Exception as e:  # pragma: no cover - defensive
        return _ev("idle", "SELECT marker, revision FROM runtime_probe WHERE id=1",
                   None, None, False, f"{type(e).__name__}: {e}")
    finally:
        conn.close()


def reject_rollback(db_path: str = SC.DB_PATH) -> Dict[str, Any]:
    """Attempt a mutation violating CHECK(id=1), then ROLLBACK.

    No bytes commit. The CHECK constraint is the transitive schema guarantee
    the frozen design names; the raised exception IS the check firing.
    """
    conn = _connect(db_path)
    sql = ("INSERT INTO runtime_probe (id, marker, representation, revision, updated_at) "
           "VALUES (2, 'oos_reject', 'oos_reject', -1, -1.0)")
    try:
        conn.execute(sql)
        conn.commit()
        # Should never happen: CHECK(id=1) must reject the row.
        return _ev("reject_rollback", sql, None, None, True,
                   "UNEXPECTED: CHECK constraint did not fire")
    except sqlite3.IntegrityError as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return _ev("reject_rollback", sql, None, None, False,
                   f"IntegrityError: {e}")
    except Exception as e:  # pragma: no cover - defensive
        try:
            conn.rollback()
        except Exception:
            pass
        return _ev("reject_rollback", sql, None, None, False, f"{type(e).__name__}: {e}")
    finally:
        conn.close()


def restore_logical(db_path: str, marker: str, representation: str,
                    revision: int, updated_at: float) -> Dict[str, Any]:
    """Committed compensating inverse (logical state restored, WAL retained).

    Used only by the blind-spot M-REVERT-LOGICAL sub-condition; it is a direct
    committed out-of-surface write like the others.
    """
    conn = _connect(db_path)
    sql = ("UPDATE runtime_probe SET marker=?, representation=?, revision=?, updated_at=? "
           "WHERE id=1")
    try:
        before = conn.execute(
            "SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1"
        ).fetchone()
        before = {k: before[k] for k in _PROBE_COLS} if before else None
        conn.execute(sql, (marker, representation, revision, updated_at))
        conn.commit()
        after = conn.execute(
            "SELECT marker, representation, revision, updated_at FROM runtime_probe WHERE id=1"
        ).fetchone()
        after = {k: after[k] for k in _PROBE_COLS} if after else None
        return _ev("restore_logical", sql, before, after, True)
    except Exception as e:  # pragma: no cover - defensive
        try:
            conn.rollback()
        except Exception:
            pass
        return _ev("restore_logical", sql, None, None, False, f"{type(e).__name__}: {e}")
    finally:
        conn.close()


def snapshot_bytes(db_path: str = SC.DB_PATH) -> Dict[str, bytes]:
    """Exact byte snapshot of the gating files (db + wal + shadow)."""
    from pathlib import Path
    out: Dict[str, bytes] = {}
    for suffix in ("", "-wal", "-shm"):
        p = Path(db_path + suffix)
        out[suffix] = p.read_bytes() if p.exists() else b""
    return out


def restore_bytes(snapshot: Dict[str, bytes], db_path: str = SC.DB_PATH) -> None:
    """Write the exact snapshot bytes back. Used only by M-REVERT-BYTES."""
    from pathlib import Path
    for suffix, data in snapshot.items():
        Path(db_path + suffix).write_bytes(data)


def worker_source_stats() -> Dict[str, Any]:
    """Static self-description used by the harness reachability scan."""
    from pathlib import Path
    import ast
    path = Path(__file__).resolve()
    tree = ast.parse(path.read_text())
    mods: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            mods.append(node.module or "")
    return {"path": str(path), "imports": sorted(set(mods))}
