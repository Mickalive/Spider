"""Shared infrastructure for the three frozen arms of EXP-FRONTIER-36249071934.

Frozen-design provenance: prereg.md sections 6.1, 6.2, 6.3, 7.2, 12.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..substrate_deterministic_http import (
    DeterministicHTTPSubstrate,
    KeepAliveClient,
    canonical_json,
    sha256_hex,
    span_signature,
    state_signature,
)
from ..taskplan import Step

#: repository root == parents of research/frontier/arms/common.py
REPO_ROOT = Path(__file__).resolve().parents[3]


def ensure_src_on_path() -> None:
    """Make the *actual shipped* ``src/spider`` kernel importable, unmodified."""
    src = REPO_ROOT / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


# ---------------------------------------------------------------------------
# Model oracle (prereg.md 12)
# ---------------------------------------------------------------------------
class ModelOracle:
    """Deterministic stand-in for a perfect policy model.

    prereg.md 12: "Model oracle = deterministic function returning correct action
    for given state (simulated perfect model). Cost = 1 unit per call
    regardless of 'model quality'."

    The oracle is the *idealised* policy: it is given the remaining task plan,
    which is what a perfect model handed the task goal would have to infer. The
    compile+deopt arm is deliberately NOT given the plan -- it only ever sees
    the substrate world state and its own last request. This asymmetry is
    conservative with respect to the treatment arm and is reported in
    ``validity_notes``.
    """

    def __init__(self) -> None:
        self.calls = 0

    def decide(self, plan: list[Step], index: int, store: dict[str, Any]) -> Step:
        self.calls += 1
        return plan[index]


# ---------------------------------------------------------------------------
# Cost ledger (prereg.md 7.2)
# ---------------------------------------------------------------------------
COST_UNIT = {
    "compile": 1.0,   # one-time per unique span compiled
    "machinery": 1.0, # resolve + bind + verify + freshness check, per span
    "model": 1.0,     # one deopt-to-model invocation
    "execution": 1.0, # one span executed
}


@dataclass
class Ledger:
    """Per-arm cost ledger.

    prereg.md 7.2 defines ``amortized_cost = (compile + model + execution) /
    episodes``. prereg.md 6.2 adds, for the incumbent inheritance arm only, "1
    unit per resolve+bind+verify+freshness check per span". Those two clauses are
    reconciled by carrying a fourth component, ``machinery``, which is exactly
    1 unit per span for any arm that performs inheritance resolution and exactly
    0 for an arm that does not. Setting ``machinery = 0`` reduces the ledger
    back to the literal prereg.md 7.2 three-term formula, so the frozen metric
    definition is preserved. Charging the controls for resolution makes the
    comparison conservative *against* the treatment arm.
    """

    compile_units: int = 0
    machinery_units: int = 0
    model_units: int = 0
    execution_units: int = 0
    detail: dict[str, int] = field(default_factory=dict)

    def charge(self, component: str, n: int = 1) -> None:
        setattr(self, f"{component}_units", getattr(self, f"{component}_units") + n)
        self.detail[component] = self.detail.get(component, 0) + n

    def bump(self, key: str, n: int = 1) -> None:
        self.detail[key] = self.detail.get(key, 0) + n

    def total(self) -> int:
        return self.compile_units + self.machinery_units + self.model_units + self.execution_units

    def amortized(self, episodes: int) -> float:
        return self.total() / episodes if episodes else float("nan")

    def as_dict(self, episodes: int) -> dict[str, Any]:
        return {
            "episodes": episodes,
            "compile_units": self.compile_units,
            "machinery_units": self.machinery_units,
            "model_units": self.model_units,
            "execution_units": self.execution_units,
            "total_units": self.total(),
            "amortized_cost_units_per_episode": self.amortized(episodes),
            "component_detail": dict(sorted(self.detail.items())),
        }


# ---------------------------------------------------------------------------
# Span record (raw evidence)
# ---------------------------------------------------------------------------
@dataclass
class SpanRecord:
    arm: str
    episode: int
    index: int
    role: str
    work_item: int
    method: str
    path: str
    body: Any
    declared_headers: dict[str, str]
    request_headers_sent: list[str]
    response_code: int
    response_body_hash: str
    signature: str
    state_sig: str
    decision_path: str
    detail: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "arm": self.arm,
            "episode": self.episode,
            "index": self.index,
            "role": self.role,
            "work_item": self.work_item,
            "method": self.method,
            "path": self.path,
            "body": self.body,
            "declared_headers": self.declared_headers,
            "request_headers_sent": sorted(self.request_headers_sent),
            "response_code": self.response_code,
            "response_body_hash": self.response_body_hash,
            "signature": self.signature,
            "state_sig": self.state_sig,
            "decision_path": self.decision_path,
            "detail": self.detail,
        }


def observable_state_sig(store: dict[str, Any], last_request: tuple[str, str] | None) -> str:
    """State key available to a no-memory executor *without* a model call.

    Only two things are used: the substrate's observable world state, and the
    executor's own last request. No task plan, no step index, no goal.
    """
    return state_signature(
        {
            "store": store,
            "last_request": list(last_request) if last_request else None,
        }
    )


__all__ = [
    "COST_UNIT",
    "DeterministicHTTPSubstrate",
    "KeepAliveClient",
    "Ledger",
    "ModelOracle",
    "REPO_ROOT",
    "SpanRecord",
    "Step",
    "canonical_json",
    "ensure_src_on_path",
    "observable_state_sig",
    "sha256_hex",
    "span_signature",
]
