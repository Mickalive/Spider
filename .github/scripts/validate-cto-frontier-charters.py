#!/usr/bin/env python3
"""Validate Chief CTO Frontier charter output with field-level diagnostics.

This is an orchestration/control-plane validator only. It does not certify any
scientific claim or the substantive merit/orthogonality of a charter.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

TEAM_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")
STATUSES = {"CREATE", "CONTINUE", "PAUSE", "TERMINATE", "MERGE"}
PRIORITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
TOP_LEVEL_KEYS = (
    "top_system_bottleneck",
    "highest_upside_program",
    "kill_or_deprioritize",
    "cross_lane_incompatibilities",
    "runtime_missing_primitives",
    "baseline_gaps",
    "recommended_allocations",
    "evidence_refs",
    "research_portfolio",
)
PORTFOLIO_KEYS = (
    "portfolio_thesis",
    "uncovered_bottlenecks",
    "frontier_team_charters",
    "merge_or_kill_actions",
    "cross_team_dependencies",
)
NONEMPTY_STRING_FIELDS = (
    "team_id",
    "domain",
    "mission",
    "question",
    "why_now",
    "why_not_existing_lane",
    "expected_work_compression_leverage",
)
ARRAY_FIELDS = (
    "evidence_inputs",
    "validity_threats",
    "required_artifacts",
    "handoff_targets",
)


def type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    return type(value).__name__


def load_json(path: Path, label: str, errors: list[str]) -> Any:
    if not path.is_file():
        errors.append(f"{label}: missing file {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(
            f"{label}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        )
        return None


def main() -> int:
    state_path = Path(sys.argv[1] if len(sys.argv) > 1 else "state/cto_direction.json")
    physics_path = Path(
        sys.argv[2]
        if len(sys.argv) > 2
        else "/tmp/spider_physics/state/physics_loop.json"
    )
    errors: list[str] = []

    state = load_json(state_path, "CTO state", errors)
    if not isinstance(state, dict):
        if state is not None:
            errors.append(f"CTO state: expected object, got {type_name(state)}")
        return finish(errors)

    for key in TOP_LEVEL_KEYS:
        if key not in state:
            errors.append(f"CTO state.{key}: missing required key")

    portfolio = state.get("research_portfolio")
    if not isinstance(portfolio, dict):
        errors.append(
            "CTO state.research_portfolio: expected object, "
            f"got {type_name(portfolio)}"
        )
        return finish(errors)

    for key in PORTFOLIO_KEYS:
        if key not in portfolio:
            errors.append(f"research_portfolio.{key}: missing required key")

    charters = portfolio.get("frontier_team_charters")
    if not isinstance(charters, list):
        errors.append(
            "research_portfolio.frontier_team_charters: expected array, "
            f"got {type_name(charters)}"
        )
        return finish(errors)

    seen: dict[tuple[str, int], int] = {}
    active_physics: list[str] = []

    for index, charter in enumerate(charters):
        prefix = f"frontier_team_charters[{index}]"
        if not isinstance(charter, dict):
            errors.append(f"{prefix}: expected object, got {type_name(charter)}")
            continue

        team_id_raw = charter.get("team_id")
        label = team_id_raw if isinstance(team_id_raw, str) and team_id_raw else f"index={index}"
        prefix = f"frontier charter {label}"

        for field in NONEMPTY_STRING_FIELDS:
            value = charter.get(field)
            if not isinstance(value, str):
                errors.append(
                    f"{prefix}.{field}: expected non-empty string, got {type_name(value)}"
                )
            elif not value.strip():
                errors.append(f"{prefix}.{field}: expected non-empty string, got empty string")

        if isinstance(team_id_raw, str) and team_id_raw and not TEAM_ID_RE.fullmatch(team_id_raw):
            errors.append(
                f"{prefix}.team_id: must match {TEAM_ID_RE.pattern!r}, got {team_id_raw!r}"
            )

        version = charter.get("charter_version")
        if type(version) is not int or version < 1:  # bool must not pass as int
            errors.append(
                f"{prefix}.charter_version: expected integer >= 1, got "
                f"{type_name(version)} {version!r}"
            )

        status = charter.get("status")
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(
                f"{prefix}.status: expected one of {sorted(STATUSES)}, got {status!r}"
            )

        priority = charter.get("priority")
        if not isinstance(priority, str) or priority not in PRIORITIES:
            errors.append(
                f"{prefix}.priority: expected one of {sorted(PRIORITIES)}, got {priority!r}"
            )

        for field in ARRAY_FIELDS:
            value = charter.get(field)
            if not isinstance(value, list):
                errors.append(
                    f"{prefix}.{field}: expected array, got {type_name(value)}"
                )

        for field in ("strongest_null_or_baseline", "stop_condition"):
            if field not in charter:
                errors.append(f"{prefix}.{field}: missing required key")
            elif charter[field] is None:
                errors.append(f"{prefix}.{field}: must not be null")

        if (
            isinstance(team_id_raw, str)
            and type(version) is int
            and version >= 1
        ):
            key = (team_id_raw, version)
            if key in seen:
                errors.append(
                    f"{prefix}: duplicate (team_id, charter_version) tuple {key!r}; "
                    f"first occurrence index={seen[key]}"
                )
            else:
                seen[key] = index

        domain = charter.get("domain")
        if (
            status in {"CREATE", "CONTINUE"}
            and isinstance(domain, str)
            and "physics" in domain.casefold()
            and isinstance(team_id_raw, str)
        ):
            active_physics.append(team_id_raw)

    physics_required = False
    if physics_path.is_file():
        physics = load_json(physics_path, "Physics state", errors)
        if isinstance(physics, dict):
            handoff = physics.get("frontier_handoff")
            if isinstance(handoff, dict):
                physics_required = handoff.get("required") is True

    if physics_required and not active_physics:
        errors.append(
            "Physics frontier coverage: accepted Physics state requires an active "
            "CREATE/CONTINUE charter whose domain explicitly contains 'Physics'"
        )

    if not errors:
        print(
            "CTO_FRONTIER_SCHEMA_OK "
            f"charters={len(charters)} "
            f"active_physics={len(active_physics)}"
        )
        for index, charter in enumerate(charters):
            print(
                "CTO_FRONTIER_CHARTER_OK "
                f"index={index} team_id={charter['team_id']} "
                f"version={charter['charter_version']} status={charter['status']}"
            )
    return finish(errors)


def finish(errors: list[str]) -> int:
    if not errors:
        return 0
    print(f"::error::Frontier charter validation failed with {len(errors)} error(s)")
    for error in errors:
        print(f"::error::{error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
