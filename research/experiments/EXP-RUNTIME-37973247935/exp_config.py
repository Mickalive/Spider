#!/usr/bin/env python3
"""
EXP-RUNTIME-37973247935 — experiment-local constants.

The validated parent components (`oracle_scorer.py`, `intervention_surface.py`,
`shared_config.py`, `bringup.py`) are byte-frozen and MUST NOT be mutated. The
new arm matrix, n, seeds and thresholds for this experiment therefore live here,
in an experiment-local constants-only module (prereg section 6.4, spec
measurement_validity.parent_components_immutable).
"""
from __future__ import annotations

EXPERIMENT_ID = "EXP-RUNTIME-37973247935"
LANE = "runtime"
CLAIM_ID = "C-MEAS-VALID"
RUN_ID = "37973247935"
MASTER_SEED = 37973247935

# ── New out-of-surface arm matrix (5 arms x 40) ────────────────────────────
OOS_POSITIVE_ARMS = ["P-OOS-WORKER", "P-OOS-REPR"]
OOS_NULL_ARMS = ["N-OOS-IDLE", "N-OOS-REJECT", "N-OOS-CACHE"]
OOS_ARMS = OOS_POSITIVE_ARMS + OOS_NULL_ARMS
OOS_EPISODES_PER_ARM = 40

# ── Instrument-liveness control (in-surface, 20) ───────────────────────────
LIVENESS_ARM = "PC-INSURFACE-WRITE-LIVE"
LIVENESS_N = 20

# ── Blind-spot probe (measured, never gated; 2 x 20) ───────────────────────
BLINDSPOT_ARMS = ["M-REVERT-BYTES", "M-REVERT-LOGICAL"]
BLINDSPOT_N = 20

# ── Capture stability (no-action pairs) ────────────────────────────────────
CAPTURE_STABILITY_PAIRS = 20

ALL_MATRIX_ARMS = OOS_ARMS + [LIVENESS_ARM] + BLINDSPOT_ARMS

# Per-arm episode count (matrix arms only).
ARM_N = {a: OOS_EPISODES_PER_ARM for a in OOS_ARMS}
ARM_N[LIVENESS_ARM] = LIVENESS_N
for _a in BLINDSPOT_ARMS:
    ARM_N[_a] = BLINDSPOT_N

# Arm class: "positive" | "null" | "liveness" | "blindspot"
ARM_KIND = {a: "positive" for a in OOS_POSITIVE_ARMS}
ARM_KIND.update({a: "null" for a in OOS_NULL_ARMS})
ARM_KIND[LIVENESS_ARM] = "liveness"
ARM_KIND.update({a: "blindspot" for a in BLINDSPOT_ARMS})

# Out-of-surface worker mode exercised per arm.
OOS_MODE = {
    "P-OOS-WORKER": "commit_probe_update",
    "P-OOS-REPR": "commit_representation",
    "N-OOS-IDLE": "idle",
    "N-OOS-REJECT": "reject_rollback",
    "N-OOS-CACHE": None,             # transport-component null (nginx proxy_cache)
    LIVENESS_ARM: None,              # in-surface browser button click
    "M-REVERT-BYTES": "commit_probe_update",
    "M-REVERT-LOGICAL": "commit_probe_update",
}

# Representation state used by the P-OOS-REPR direct mutation (differs from the
# frozen pre-state "A" planted by fixture reset).
OOS_REPR_VARIANT = "B"

# ── Decision thresholds (frozen; same values as the validated parent) ───────
POINT_MIN = 0.90
WILSON_LO_MIN = 0.80
LIVENESS_POINT_MIN = 1.0
NULL_MAX_FALSE_POSITIVES = 0

# Directional "contradiction" threshold for the non-gating blind-spot probe:
# a majority rate (>0.5) contradicts an "~0" prediction; <0.5 contradicts "~1".
BLINDSPOT_MAJORITY = 0.5

# oos_worker evidence artifact name.
OOS_EVIDENCE = "A-OOS-WORKER-EVIDENCE.jsonl"
