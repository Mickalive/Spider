from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class ResolutionStatus(str, Enum):
    EXECUTABLE = "EXECUTABLE"
    REPAIRABLE = "REPAIRABLE"
    EXPLORE = "EXPLORE"
    UNKNOWN = "UNKNOWN"


#: Outcome classes for parameter binding. ABSTAIN is scored as its own outcome
#: class rather than folded into success or failure (frozen decision rule,
#: spec.json decision_rule.abstention_class).
BINDER_BOUND = "BOUND"
BINDER_ABSTAIN = "ABSTAIN"


@dataclass(frozen=True)
class Observation:
    intent: str
    state: dict[str, Any]
    action: dict[str, Any]
    next_state: dict[str, Any]
    success: bool
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass
class Mechanism:
    mechanism_id: str
    intent: str
    preconditions: dict[str, Any]
    action_template: dict[str, Any]
    postconditions: dict[str, Any]
    parameter_slots: list[str] = field(default_factory=list)
    auth_scope: str | None = None
    freshness: dict[str, Any] = field(default_factory=dict)
    applicability_guards: dict[str, Any] = field(default_factory=dict)
    verification_rule: dict[str, Any] = field(default_factory=dict)
    failure_boundary: dict[str, Any] = field(default_factory=dict)
    repair_scope: dict[str, Any] = field(default_factory=dict)
    intent_namespace_map: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    confidence: float = 0.0
    invalidated: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Resolution:
    status: ResolutionStatus
    mechanism_id: str | None
    reason: str
    bound_action: dict[str, Any] | None = None
    confidence: float = 0.0


@dataclass(frozen=True)
class BindOutcome:
    """Result of a parameter-binding attempt for one task.

    ``status`` is BINDER_BOUND or BINDER_ABSTAIN. An abstention is a scored
    outcome class, not an absence of one, so every field is populated on both
    paths and callers never have to infer an outcome from a missing value.
    """

    status: str
    bound_action: dict[str, Any] | None
    bind_confidence: float
    reason: str
    slot_values: dict[str, str] = field(default_factory=dict)
    slot_support: dict[str, Any] = field(default_factory=dict)
