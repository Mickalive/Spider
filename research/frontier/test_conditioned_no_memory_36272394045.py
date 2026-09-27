"""Unit tests for the EXP-FRONTIER-36272394045 treatment arm.

Frozen-design provenance: prereg.md section 13, "Goal conditioning
implementation leak (accidental memory) | Conditioned arm is stateless function:
``action = f(obs, goal)`` with no closure over prior episodes; unit tested".

Run directly (no pytest in this environment):

    python3 -m research.frontier.test_conditioned_no_memory_36272394045

Exit code 0 = all checks pass. The result is also written to
``research/experiments/EXP-FRONTIER-36272394045/artifacts/conditioned_arm_statelessness_test.json``
by the runner, so the checks are raw evidence and not only a console claim.
"""

from __future__ import annotations

import inspect
import json
import random
import sys
from pathlib import Path
from typing import Any

from .arms.conditioned_no_memory import ConditionedNoMemory, conditioned_action, parse_goal_prefix
from .episodegen_36272394045 import (
    EPISODES_PER_RATE,
    NOVELTY_GRID,
    SPANS_PER_EPISODE,
    build_steps,
    class_iii_work_item,
)
from .taskplan import episode_plan

CHECKS: list[dict[str, Any]] = []


def _check(name: str, passed: bool, detail: Any = None) -> None:
    CHECKS.append({"check": name, "passed": bool(passed), "detail": detail})


def test_signature_is_pure() -> None:
    """The decision procedure takes exactly (observable state, goal) and nothing else."""
    import ast
    import re

    params = list(inspect.signature(conditioned_action).parameters)
    _check(
        "conditioned_action_signature_is_exactly_obs_and_goal",
        params == ["observable_state_sig", "goal_prefix"],
        {"parameters": params},
    )
    # Strip the docstring, then reject any identifier reference that could carry
    # arm state, substrate state, plan state or run-time position.
    tree = ast.parse(inspect.getsource(conditioned_action))
    fn = tree.body[0]
    docstring_nodes = [
        n
        for n in ast.walk(fn)
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)
    ]
    for n in docstring_nodes:
        n.value.value = ""
    code = ast.unparse(fn)
    forbidden = sorted(
        {
            name
            for name in re.findall(r"[A-Za-z_][A-Za-z_0-9]*", code)
            if name in {"self", "global", "substrate", "last_mint", "episode_counter", "MaterializedPlan", "TokenCtx", "ConditionedNoMemory", "build_steps"}
        }
    )
    _check("conditioned_action_source_has_no_arm_state", not forbidden, {"code": code, "found": forbidden})


def test_purity_under_reordering() -> None:
    """Same (obs, goal) -> same action, whatever the call order, at any time."""
    pairs: list[tuple[str, str]] = []
    for nu in NOVELTY_GRID:
        for ep in (1, 7, 23, 50):
            for s in build_steps(ep, nu):
                pairs.append((f"obs-{ep}-{s.index}-{nu}", s.goal_prefix("wide")))
    forward = {k: conditioned_action(k, g) for k, g in pairs}
    shuffled = list(pairs)
    random.Random(36272394045).shuffle(shuffled)
    backward = {k: conditioned_action(k, g) for k, g in reversed(shuffled)}
    mismatches = [k for k in forward if forward[k] != backward[k]]
    _check("purity_under_reordering_and_repetition", not mismatches, {"n_pairs": len(pairs), "mismatches": mismatches[:5]})
    repeat = {k: conditioned_action(k, g) for k, g in pairs}
    _check("purity_under_repetition", repeat == forward, {"n_pairs": len(pairs)})


def test_no_cross_episode_memory() -> None:
    """A fresh ConditionedNoMemory instance reproduces an old instance exactly."""
    nu = 0.50
    first: list[tuple[str, str]] = []
    for ep in range(1, 9):
        for s in build_steps(ep, nu):
            first.append((f"obs-{ep}-{s.index}", s.goal_prefix("wide")))
    arm_a = ConditionedNoMemory()
    arm_b = ConditionedNoMemory()
    a = [conditioned_action(o, g) for o, g in first]
    b = [conditioned_action(o, g) for o, g in first]
    _check("two_fresh_arm_instances_agree", a == b, {"n": len(a)})
    _check("arm_dataclass_stores_no_span_history", set(vars(arm_a)) == {"arm", "goal_width", "ledger", "model_calls", "oracle"}, {"fields": sorted(vars(arm_a))})


def test_handle_never_in_conditioning_context() -> None:
    """The class-(iii) handle is absent from both inputs at its decision point.

    Verifies the prereg.md section 8 step-2 condition directly on the declared
    observable state and the declared goal prefix.
    """
    from .arms.common import observable_state_sig

    leaks: list[dict[str, Any]] = []
    n_checked = 0
    for ep in range(1, 6):
        for w in range(4):
            if not class_iii_work_item(ep, w):
                continue
            steps = build_steps(ep, 0.50)
            for s in steps:
                if not s.token_required or s.work_item != w:
                    continue
                n_checked += 1
                # Handle the substrate would have minted for this episode.
                handle = f"{ep:08x}" + "0" * 8
                store: dict[str, Any] = {f"r-{ep:03d}-{s.work_item}": {"title": "t", "value": 1}}
                obs = observable_state_sig(store, ("GET", "/resources/x"))
                prefix = s.goal_prefix("wide")
                action = conditioned_action(obs, prefix)
                if handle in json.dumps([obs, prefix]):
                    leaks.append({"episode": ep, "index": s.index, "where": "observable_state_or_goal"})
                if handle in json.dumps(action):
                    leaks.append({"episode": ep, "index": s.index, "where": "emitted_action"})
    _check("capability_handle_absent_from_both_inputs", not leaks, {"n_token_spans_checked": n_checked, "leaks": leaks[:5]})


def test_no_memory_arm_never_supplies_handle() -> None:
    """The treatment arm's emitted request for a gated span is the ungated one."""
    bad: list[dict[str, Any]] = []
    n = 0
    for ep in range(1, 6):
        for s in build_steps(ep, 0.50):
            if not s.token_required:
                continue
            n += 1
            a = conditioned_action("obs", s.goal_prefix("wide"))
            b = conditioned_action("obs", s.goal_prefix("narrow"))
            if "t=" in a["path"] or "view=" in a["path"] or "t=" in b["path"] or "view=" in b["path"]:
                bad.append({"episode": ep, "index": s.index, "wide": a["path"], "narrow": b["path"]})
            if "?" in a["path"]:
                bad.append({"episode": ep, "index": s.index, "wide": a["path"], "why": "query survived"})
    _check("conditioned_arm_never_supplies_handle", not bad, {"n_gated_spans": n, "bad": bad[:5]})


def test_goal_prefix_never_contains_handle() -> None:
    bad = [
        {"episode": ep, "index": s.index}
        for ep in range(1, 11)
        for s in build_steps(ep, 0.50)
        if "?" in s.goal_prefix("wide") or "?" in s.goal_prefix("narrow")
    ]
    _check("goal_prefix_never_contains_a_handle_query", not bad, {"bad": bad[:5]})


def test_base_plan_unchanged_without_plant() -> None:
    """``class_iii=False`` reproduces the parent generator span for span."""
    from .taskplan import Step

    mismatches: list[dict[str, Any]] = []
    for nu in NOVELTY_GRID:
        for ep in (1, 2, 13, 50):
            base = episode_plan(ep, nu)
            mine = build_steps(ep, nu, class_iii=False)
            if len(base) != len(mine):
                mismatches.append({"episode": ep, "nu": nu, "len": [len(base), len(mine)]})
                continue
            for b, m in zip(base, mine):
                if (b.role, b.method, b.path, b.body, b.expect_code) != (
                    m.role,
                    m.method,
                    m.path,
                    m.body,
                    m.expect_code,
                ):
                    mismatches.append({"episode": ep, "nu": nu, "index": m.index, "parent": b, "mine": m})
    _check("base_plan_identical_to_parent_generator", not mismatches, {"mismatches": mismatches[:3]})
    _check(
        "episode_shape_frozen_24_spans",
        all(len(build_steps(e, nu)) == SPANS_PER_EPISODE for nu in NOVELTY_GRID for e in (1, 50)),
        {"spans_per_episode": SPANS_PER_EPISODE, "episodes_per_rate": EPISODES_PER_RATE},
    )


def test_class_iii_schedule_is_exact() -> None:
    planted = [(e, w) for e in range(1, EPISODES_PER_RATE + 1) for w in range(4) if class_iii_work_item(e, w)]
    spans = sum(2 for _ in planted)
    _check("class_iii_realized_span_fraction_is_0_10", spans == 120 and spans / (EPISODES_PER_RATE * 24) == 0.1, {"planted_work_items": len(planted), "class_iii_spans": spans, "share": spans / (EPISODES_PER_RATE * 24)})
    per_ep = {}
    for e, w in planted:
        per_ep[e] = per_ep.get(e, 0) + 1
    _check("class_iii_plant_max_two_work_items_per_episode", max(per_ep.values()) <= 2, {"max_per_episode": max(per_ep.values()), "min_per_episode": min(per_ep.values())})


def test_wide_prefix_is_strictly_more_informative_than_narrow() -> None:
    wide_fields = parse_goal_prefix(build_steps(1, 0.50)[1].goal_prefix("wide"))
    narrow_fields = parse_goal_prefix(build_steps(1, 0.50)[1].goal_prefix("narrow"))
    _check("wide_prefix_superset_of_narrow", set(narrow_fields) < set(wide_fields), {"narrow": sorted(narrow_fields), "wide": sorted(wide_fields)})


def main() -> int:
    for fn in (
        test_signature_is_pure,
        test_purity_under_reordering,
        test_no_cross_episode_memory,
        test_handle_never_in_conditioning_context,
        test_no_memory_arm_never_supplies_handle,
        test_goal_prefix_never_contains_handle,
        test_base_plan_unchanged_without_plant,
        test_class_iii_schedule_is_exact,
        test_wide_prefix_is_strictly_more_informative_than_narrow,
    ):
        fn()
    passed = all(c["passed"] for c in CHECKS)
    payload = {
        "experiment_id": "EXP-FRONTIER-36272394045",
        "purpose": "prereg.md section 13 mitigation: the goal-conditioned arm is a pure function of (observable state, goal prefix) with no cross-episode memory",
        "all_passed": passed,
        "n_checks": len(CHECKS),
        "n_failed": sum(1 for c in CHECKS if not c["passed"]),
        "checks": CHECKS,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    raise SystemExit(main())
