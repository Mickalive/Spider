#!/usr/bin/env python3
"""Canonical machine-readable constants for the Research 2.0 packet contract."""
from __future__ import annotations

CLAIM_STATUSES = frozenset({
    "HYPOTHESIS",
    "EXPERIMENTAL",
    "VALIDATED",
    "PRODUCT_CORE",
    "SHIPPED",
    "REJECTED",
    "BLOCKED",
    "MEASUREMENT_INVALID",
    "SUPERSEDED",
})
DIRECTOR_CLAIM_STATUSES = frozenset(CLAIM_STATUSES - {"SHIPPED"})
CLAIM_STATUS_ALIASES = {
    "SUPPORTED": "EXPERIMENTAL",
    "SUPPORTED_BOUNDED": "EXPERIMENTAL",
    "PARTIAL": "EXPERIMENTAL",
    "OPEN": "EXPERIMENTAL",
}
AUDIT_STATUSES = frozenset({"PASS", "REVISE", "FAIL", "MEASUREMENT_INVALID", "BLOCKED"})
RESULT_STATUSES = frozenset({"COMPLETE", "BLOCKED", "MEASUREMENT_INVALID"})
RESULT_OUTCOMES = frozenset({"SUPPORTS", "FALSIFIES", "MIXED", "INCONCLUSIVE", "NOT_APPLICABLE"})
LANES = frozenset({"graph", "physics", "runtime", "product", "intel", "frontier"})
PORTFOLIO_ACTIONS = frozenset({"CONTINUE", "PIVOT", "PARK", "REOPEN", "TERMINATE"})
PORTFOLIO_ACTIVE_ACTIONS = frozenset({"CONTINUE", "PIVOT", "REOPEN"})

PACKET_FILES = (
    "request.json",
    "spec.json",
    "prereg.md",
    "freeze.json",
    "result.json",
    "report.md",
    "provenance.json",
    "audit.json",
    "verdict.json",
    "handoff.json",
)

STAGE_OUTPUTS = {
    "install": (),
    "design": ("freeze.json",),
    "execute": ("result.json", "report.md", "provenance.json"),
    "audit": ("audit.json",),
    "director": ("verdict.json", "handoff.json"),
}
