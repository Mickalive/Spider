#!/usr/bin/env python3
"""
SPIDER Research 2.0 — runtime lane shared CONSTANTS only.

This module exists solely to keep one authoritative copy of the frozen WAL
path, schema, controlled-row sentinel values, header-exclusion set, arm
identities and decision thresholds. It contains NO logic: no Flask app, no
routes, no auth/session boundary, no detector and no scoring.

The authorship separation required by the frozen design is between the
intervention surface (ground-truth provider, `intervention_surface.py`) and
the oracle scorer (detector, `oracle_scorer.py`). Neither of those modules
imports the other; both may import this constants-only file, which is the
mitigation named explicitly in prereg.md section 12 ("Any shared constants
(e.g., WAL path) defined in a third shared_config.py imported by both, but
logic remains separated").
"""
from __future__ import annotations

# ── Frozen identities ──────────────────────────────────────────────────────
EXPERIMENT_ID = "EXP-RUNTIME-36293257855"
LANE = "runtime"
CLAIM_ID = "C-MEAS-VALID"
RUN_ID = "36293257855"
MASTER_SEED = 36293257855

# ── Frozen arm matrix ──────────────────────────────────────────────────────
ARMS = ["P-WRITE", "P-DRIFT", "N-READ", "N-INVALID", "N-EXPIRED", "N-DELETED"]
POSITIVE_ARMS = ["P-WRITE", "P-DRIFT"]
NULL_ARMS = ["N-READ", "N-INVALID", "N-EXPIRED", "N-DELETED"]
EPISODES_PER_ARM = 20

# ── Frozen decision thresholds (spec.json decision_rule) ───────────────────
WILSON_Z = 1.959963984540054  # frozen two-sided 95% Wilson z
THRESH_POINT = 0.90
THRESH_WILSON_LO = 0.80

# ── Frozen substrate contract ──────────────────────────────────────────────
DB_PATH = "/tmp/single.db"
WAL_PATH = DB_PATH + "-wal"
SHM_PATH = DB_PATH + "-shm"

# Controlled-row sentinel (prereg 5; parent validated fixture).
PRE_MARKER = "pre_marker"
PRE_REPRESENTATION = "pre_repr"
PRE_REVISION = 0
PRE_UPDATED_AT = 0.0

# Frozen response-fingerprint header exclusions. Date/Server/X-Request-Id are
# the prereg-mandated exclusions; the remaining volatile proxy/worker/cache
# headers are excluded exactly as in the validated parent instrument so the
# fingerprint is a stable projection of the controlled response.
EXCLUDED_HEADERS = frozenset({
    "Date", "Server", "X-Request-Id", "X-Worker-Pid", "X-Cache", "Age",
    "Content-Length", "ETag", "W-ETag", "Range",
})

# ── Frozen SQLite schema (WAL, wal_autocheckpoint=0) ───────────────────────
SCHEMA = {
    "sessions": ("CREATE TABLE IF NOT EXISTS sessions "
                 "(id INTEGER PRIMARY KEY, sid TEXT UNIQUE, username TEXT, "
                 "valid INTEGER DEFAULT 1, created_at REAL)"),
    "runtime_probe": ("CREATE TABLE IF NOT EXISTS runtime_probe "
                      "(id INTEGER PRIMARY KEY CHECK(id=1), marker TEXT NOT NULL, "
                      "representation TEXT NOT NULL, revision INTEGER NOT NULL, "
                      "updated_at REAL NOT NULL)"),
    "body_config": ("CREATE TABLE IF NOT EXISTS body_config "
                    "(id INTEGER PRIMARY KEY CHECK(id=1), variant TEXT, content TEXT)"),
}

# Certified stable-header API surfaces reused from the validated fixture.
BODY_STATES = {
    "A": {"json": '{"data": "hello", "version": 1}'},
    "B": {"json": '{"data": "hello!", "version": 2}'},
    "C": {"json": ('{"admin_note": "sensitive:42", "count": 42, "data": "hello", '
                   '"items": ["a","b","c"], "role": "admin", "version": 1}')},
    "D": {"json": '{"data": "hello world", "version": 3}'},
}
ENDPOINTS = ["/api/profile", "/api/data_list"]
