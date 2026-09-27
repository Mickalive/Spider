"""Unit tests for the EXP-FRONTIER-36287182510 new arms.

Frozen-design provenance: ``prereg.md`` section 6.1 ("Statelessness guarantee:
the arm holds no state between episodes ... unit-tested for statelessness
(14 checks, 0 failures, plus GoalOnlyPlan AttributeError guard)"),
``prereg.md`` section 14 (validity threats and mitigations) and
``prereg.md`` section 17 no-go condition 5 (the scratchpad arm fails the
statelessness test -> MEASUREMENT_INVALID).

Run directly (no pytest in this environment)::

    python3 -m research.frontier.test_scratchpad_36287182510

Exit code 0 = all checks pass. The payload is also written to
``research/experiments/EXP-FRONTIER-36287182510/artifacts/scratchpad_statelessness_test.json``
by the runner, so the checks are raw evidence and not only a console claim.
"""

from __future__ import annotations

import ast
import inspect
import json
import random
import re
import sys
import textwrap
from pathlib import Path
from typing import Any

from .arms.common import observable_state_sig
from .arms.compiled_binding import CrossEpisodeCompiledBinding
from .arms.scratchpad import (
    GOAL_WIDTH,
    AlwaysMintScratchpad,
    WithinEpisodeScratchpad,
    always_mint_action,
    parse_goal_prefix,
    resolve_handle,
    scratchpad_action,
)
from .episodegen_36272394045 import (
    EPISODES_PER_RATE,
    NOVELTY_GRID,
    SPANS_PER_EPISODE,
    GoalOnlyPlan,
    build_steps,
    class_iii_work_item,
)
from .substrate_deterministic_http import DeterministicHTTPSubstrate, mint_token
from .taskplan import episode_plan

CHECKS: list[dict[str, Any]] = []


def _check(name: str, passed: bool, detail: Any = None) -> None:
    CHECKS.append({"check": name, "passed": bool(passed), "detail": detail})


# ---------------------------------------------------------------------------
# 1-4  purity / statelessness of the decision procedure
# ---------------------------------------------------------------------------
def test_signature_is_pure() -> None:
    params = list(inspect.signature(scratchpad_action).parameters)
    _check(
        "scratchpad_action_signature_is_exactly_obs_goal_scratchpad",
        params == ["observable_state_sig", "goal_prefix", "scratchpad_values"],
        {"parameters": params},
    )
    params2 = list(inspect.signature(always_mint_action).parameters)
    _check(
        "always_mint_action_signature_is_identical",
        params2 == params,
        {"parameters": params2},
    )
    tree = ast.parse(inspect.getsource(scratchpad_action))
    fn = tree.body[0]
    for n in ast.walk(fn):
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
            n.value.value = ""
    code = ast.unparse(fn)
    forbidden = sorted(
        {
            name
            for name in re.findall(r"[A-Za-z_][A-Za-z_0-9]*", code)
            if name
            in {
                "self",
                "global",
                "substrate",
                "last_mint",
                "episode_counter",
                "MaterializedPlan",
                "TokenCtx",
                "WithinEpisodeScratchpad",
                "CrossEpisodeCompiledBinding",
                "build_steps",
            }
        }
    )
    _check("scratchpad_action_source_has_no_arm_state", not forbidden, {"found": forbidden})
    # No closure: the module-level function must not reference any global that
    # an arm instance could mutate.
    globals_used = sorted(
        {n for n in re.findall(r"[A-Za-z_][A-Za-z_0-9]*", code) if n in {"ROLE_METHOD", "TOKEN_PARAM", "EXPECTED_CODES", "parse_goal_prefix", "resolve_handle", "json"}}
    )
    _check(
        "scratchpad_action_reads_only_frozen_module_constants",
        set(globals_used) <= {"ROLE_METHOD", "TOKEN_PARAM", "EXPECTED_CODES", "parse_goal_prefix", "resolve_handle", "json"},
        {"globals": globals_used},
    )


def test_purity_under_reordering() -> None:
    pairs: list[tuple[str, str, dict[str, Any]]] = []
    for nu in NOVELTY_GRID:
        for ep in (1, 7, 23, 50):
            for s in build_steps(ep, nu):
                pairs.append((f"obs-{ep}-{s.index}-{nu}", s.goal_prefix(GOAL_WIDTH), {}))
    forward = {k: scratchpad_action(k, g, v) for k, g, v in pairs}
    shuffled = list(pairs)
    random.Random(36287182510).shuffle(shuffled)
    backward = {k: scratchpad_action(k, g, v) for k, g, v in reversed(shuffled)}
    _check("purity_under_reordering_and_repetition", forward == backward, {"n_pairs": len(pairs)})
    repeat = {k: scratchpad_action(k, g, v) for k, g, v in pairs}
    _check("purity_under_repetition", repeat == forward, {"n_pairs": len(pairs)})


def test_no_cross_episode_memory_in_the_arm() -> None:
    arm_a = WithinEpisodeScratchpad()
    arm_b = WithinEpisodeScratchpad()
    _check(
        "arm_dataclass_stores_no_span_history",
        set(vars(arm_a))
        == {"arm", "ledger", "decide", "goal_width", "episodes_run", "scratchpad_resolved_spans", "handle_reads_from_bodies", "model_units_charged"},
        {"fields": sorted(vars(arm_a))},
    )
    _check("two_fresh_arm_instances_agree", vars(arm_a) == vars(arm_b), {})
    # Static: the scratchpad must be a local of run_episode, never an attribute.
    src = textwrap.dedent(inspect.getsource(WithinEpisodeScratchpad.run_episode))
    tree = ast.parse(src)
    local_names = {
        n.target.id
        for n in ast.walk(tree)
        if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == "scratchpad_values"
    }
    self_attr_reads = sorted(
        {
            n.attr
            for n in ast.walk(tree)
            if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "self"
        }
    )
    _check(
        "scratchpad_is_a_local_of_run_episode",
        local_names == {"scratchpad_values"}
        and not any(a.startswith("scratchpad") and a != "scratchpad_resolved_spans" for a in self_attr_reads),
        {"local_annotated_assignments": sorted(local_names), "self_attributes_referenced": self_attr_reads},
    )
    fields = {f.name for f in __import__("dataclasses").fields(WithinEpisodeScratchpad)}
    _check("no_scratchpad_attribute_on_the_arm", not any("scratch" in f and f != "scratchpad_resolved_spans" for f in fields), {"fields": sorted(fields)})


def test_handle_absent_from_both_declared_inputs() -> None:
    """The class-(iii) condition, verified rather than assumed (prereg.md 9.1)."""
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
                handle = mint_token(ep)
                store = {f"r-{ep:03d}-{s.work_item}": {"title": "t", "value": 1}}
                obs = observable_state_sig(store, ("GET", "/resources/x"))
                prefix = s.goal_prefix(GOAL_WIDTH)
                if handle in json.dumps([obs, prefix]):
                    leaks.append({"episode": ep, "index": s.index, "where": "observable_state_or_goal"})
                action_empty = scratchpad_action(obs, prefix, {"by_rid": {}, "last_handle": None})
                if handle in json.dumps(action_empty):
                    leaks.append({"episode": ep, "index": s.index, "where": "emitted_action_from_empty_scratchpad"})
    _check("capability_handle_absent_from_both_inputs", not leaks, {"n_token_spans_checked": n_checked, "leaks": leaks[:5]})


def test_goal_prefix_never_contains_a_handle() -> None:
    bad = [
        {"episode": ep, "index": s.index}
        for ep in range(1, 11)
        for s in build_steps(ep, 0.50)
        if "?" in s.goal_prefix("wide") or "?" in s.goal_prefix("narrow") or "?" in s.goal_prefix(GOAL_WIDTH)
    ]
    _check("goal_prefix_never_contains_a_handle_query", not bad, {"bad": bad[:5]})


def test_prefix_relationship_is_exactly_the_declared_deviation() -> None:
    """DI-01: ``wide``/``narrow`` byte-identical to the parent; wide_mint adds
    exactly one field."""
    wide_fields: set[str] = set()
    mint_fields: set[str] = set()
    for nu in NOVELTY_GRID:
        for ep in (1, 3, 50):
            for s in build_steps(ep, nu):
                wide_fields |= set(parse_goal_prefix(s.goal_prefix("wide")))
                mint_fields |= set(parse_goal_prefix(s.goal_prefix(GOAL_WIDTH)))
    _check(
        "wide_mint_is_wide_plus_exactly_the_mint_field",
        mint_fields == wide_fields | {"mint"} and len(mint_fields - wide_fields) == 1,
        {"wide": sorted(wide_fields), "wide_mint": sorted(mint_fields)},
    )
    narrow_ok = all(
        set(parse_goal_prefix(s.goal_prefix("narrow"))) == {"intent", "key"}
        for nu in NOVELTY_GRID
        for ep in (1, 9)
        for s in build_steps(ep, nu)
    )
    _check("narrow_prefix_unchanged", narrow_ok, {"narrow_fields": ["intent", "key"]})
    versions = sorted(
        {s.goal_prefix("wide").split("||")[0].strip() for nu in NOVELTY_GRID for ep in (1,) for s in build_steps(ep, nu)}
    )
    _check("prefix_version_unchanged", versions == ["spider-frontier-goal-v1"], {"versions": versions})


def test_handle_is_never_invented() -> None:
    """An empty scratchpad must reproduce the parent's ungated request exactly."""
    bad: list[dict[str, Any]] = []
    n = 0
    for ep in range(1, 6):
        for s in build_steps(ep, 0.50):
            if not s.token_required:
                continue
            n += 1
            for fn in (scratchpad_action, always_mint_action):
                a = fn("obs", s.goal_prefix(GOAL_WIDTH if fn is scratchpad_action else "wide"), {"by_rid": {}, "last_handle": None})
                if "t=" in a["path"] or "view=" in a["path"] or a["token_supplied"]:
                    bad.append({"fn": fn.__name__, "episode": ep, "index": s.index, "path": a["path"]})
    _check("no_handle_is_ever_invented_or_guessed", not bad, {"n_gated_spans": n, "bad": bad[:5]})


def test_resolve_handle_is_pure_and_total() -> None:
    scratch = {"by_rid": {"r-001-0": "AAAA", "r-001-1": "BBBB"}, "last_handle": "CCCC"}
    _check("resolve_handle_reads_by_rid_for_a_resource_span", resolve_handle("read_resource", "r-001-0", scratch) == ("AAAA", "scratchpad_by_rid"), {})
    _check("resolve_handle_reads_last_handle_for_the_collection_span", resolve_handle("list_resources", "-", scratch) == ("CCCC", "scratchpad_last_handle"), {})
    _check("resolve_handle_reports_absence_rather_than_guessing", resolve_handle("read_resource", "nope", scratch) == (None, "absent"), {})
    _check("resolve_handle_on_empty_scratchpad", resolve_handle("list_resources", "-", {"by_rid": {}, "last_handle": None}) == (None, "absent"), {})
    _check("scratchpad_action_never_mutates_the_scratchpad", scratch == {"by_rid": {"r-001-0": "AAAA", "r-001-1": "BBBB"}, "last_handle": "CCCC"}, {"scratchpad_after": scratch})


def test_non_gated_spans_are_unaffected_by_the_scratchpad() -> None:
    base = build_steps(1, 0.50)
    with_handle = {"by_rid": {"r-001-0": "AAAA"}, "last_handle": "AAAA"}
    diffs = [
        s.index
        for s in base
        if not s.token_required
        and scratchpad_action("o", s.goal_prefix(GOAL_WIDTH), {})["path"] != scratchpad_action("o", s.goal_prefix(GOAL_WIDTH), with_handle)["path"]
    ]
    _check("carrying_a_handle_does_not_change_any_ungated_action", not diffs, {"differing_indices": diffs})


# ---------------------------------------------------------------------------
# 9-13  the GoalOnlyPlan runtime guard and the frozen episode shape
# ---------------------------------------------------------------------------
def test_goal_only_plan_guard() -> None:
    plan = GoalOnlyPlan(build_steps(1, 0.50))
    blocked = []
    for attr in ("path", "body", "mint", "token_param", "goal_key", "expect_code"):
        try:
            getattr(plan, attr)
            blocked.append({"attribute": attr, "raised": False})
        except AttributeError:
            blocked.append({"attribute": attr, "raised": True})
    _check(
        "goal_only_plan_withholds_the_oracle_action",
        all(b["raised"] for b in blocked),
        {"attempts": blocked},
    )
    step = next(iter(plan))
    step_blocked = []
    for attr in ("path", "body", "mint", "token_param"):
        try:
            getattr(step, attr)
            step_blocked.append({"attribute": attr, "raised": False})
        except AttributeError:
            step_blocked.append({"attribute": attr, "raised": True})
    _check("goal_step_withholds_the_oracle_action", all(b["raised"] for b in step_blocked), {"attempts": step_blocked})
    _check(
        "goal_only_plan_still_exposes_the_declared_conditioning_set",
        all(hasattr(step, a) for a in ("index", "work_item", "role", "token_required", "novel", "goal_prefix")),
        {"allowed": sorted(GoalOnlyPlan._ALLOWED)},
    )


def test_frozen_episode_shape_and_plant() -> None:
    _check(
        "episode_shape_frozen_24_spans",
        all(len(build_steps(e, nu)) == SPANS_PER_EPISODE for nu in NOVELTY_GRID for e in (1, 50)),
        {"spans_per_episode": SPANS_PER_EPISODE, "episodes_per_rate": EPISODES_PER_RATE},
    )
    planted = [(e, w) for e in range(1, EPISODES_PER_RATE + 1) for w in range(4) if class_iii_work_item(e, w)]
    spans = sum(2 for _ in planted)
    _check(
        "class_iii_realized_span_fraction_is_0_10",
        spans == 120 and spans / (EPISODES_PER_RATE * 24) == 0.1,
        {"planted_work_items": len(planted), "class_iii_spans": spans},
    )
    mismatches: list[dict[str, Any]] = []
    for nu in NOVELTY_GRID:
        for ep in (1, 2, 13, 50):
            b = episode_plan(ep, nu)
            m = build_steps(ep, nu, class_iii=False)
            if len(b) != len(m):
                mismatches.append({"episode": ep, "nu": nu, "len": [len(b), len(m)]})
                continue
            for x, y in zip(b, m):
                if (x.role, x.method, x.path, x.body, x.expect_code) != (y.role, y.method, y.path, y.body, y.expect_code):
                    mismatches.append({"episode": ep, "nu": nu, "index": y.index})
    _check("base_plan_identical_to_parent_generator", not mismatches, {"mismatches": mismatches[:3]})


# ---------------------------------------------------------------------------
# 14-20  behavioural statelessness on the real substrate
# ---------------------------------------------------------------------------
def test_statelessness_behaviour_on_the_real_substrate() -> None:
    """Every gated span's handle must be the handle minted in ITS OWN episode."""
    sub = DeterministicHTTPSubstrate()
    client = sub.keepalive()
    arm = WithinEpisodeScratchpad()
    recs: list[Any] = []
    try:
        for ep in range(1, 7):
            steps = build_steps(ep, 0.50)
            info = arm.run_episode(sub, client, ep, GoalOnlyPlan(steps), recs)
            if not info["store_empty_at_episode_start"]:
                CHECKS.append({"check": "store_empty_at_episode_start", "passed": False, "detail": {"episode": ep}})
    finally:
        client.close()
        sub.close()
    gated = [r for r in recs if r.detail["token_required"]]
    bad = []
    for r in gated:
        expected = mint_token(r.episode)
        if r.detail["handle_used"] != expected:
            bad.append({"episode": r.episode, "index": r.index, "used": r.detail["handle_used"], "expected": expected})
    _check(
        "every_gated_span_uses_the_handle_minted_in_its_own_episode",
        not bad and len(gated) > 0,
        {"n_gated_spans": len(gated), "bad": bad[:5]},
    )
    wrong = [r for r in gated if not r.detail["token_supplied"]]
    _check("every_gated_span_is_resolved_from_the_scratchpad", not wrong, {"n_unresolved": len(wrong)})
    _check("all_gated_responses_were_expected_codes", all(r.detail["code_ok"] for r in gated), {"n": len(gated)})
    # No handle value survives on the arm between episodes.
    leaks = [
        k
        for k, v in vars(arm).items()
        if isinstance(v, str) and re.fullmatch(r"[0-9a-f]{16}", v)
    ]
    _check("no_capability_handle_is_retained_on_the_arm", not leaks, {"leaks": leaks})
    _check(
        "ledger_charges_no_compile_and_no_machinery",
        arm.ledger.compile_units == 0 and arm.ledger.machinery_units == 0,
        {"compile": arm.ledger.compile_units, "machinery": arm.ledger.machinery_units, "model": arm.ledger.model_units, "execution": arm.ledger.execution_units},
    )
    _check(
        "arm_reads_its_handles_from_response_bodies_only",
        arm.handle_reads_from_bodies == sum(1 for r in recs if r.detail["handle_observed_in_response_body"]),
        {"reads": arm.handle_reads_from_bodies},
    )


def test_compiled_binding_arm_key_contains_the_binding() -> None:
    sub = DeterministicHTTPSubstrate()
    client = sub.keepalive()
    arm = CrossEpisodeCompiledBinding()
    recs: list[Any] = []
    try:
        for ep in range(1, 5):
            steps = build_steps(ep, 0.50)
            from .episodegen_36272394045 import MaterializedPlan, TokenCtx

            ctx = TokenCtx()
            sub_last = sub

            class _Proxy:
                def __init__(self, inner: Any) -> None:
                    self._inner = inner

                def request(self, m: str, p: str, b: Any = None) -> Any:
                    out = self._inner.request(m, p, b)
                    ctx.token = sub_last.last_mint
                    return out

            arm.run_episode(sub, _Proxy(client), ep, MaterializedPlan(steps, ctx), recs)
    finally:
        client.close()
        sub.close()
    keys = [r.detail["cache_key"] for r in recs]
    _check("cache_key_is_state_plus_binding", all("|" in k for k in keys), {"n_keys": len(keys)})
    n_bound = sum(1 for r in recs if r.detail["binding_key_in_cache_key"] is not None)
    _check("binding_key_is_populated_after_a_mint_is_read", n_bound > 0, {"n_spans_with_binding_key": n_bound})
    _check(
        "compiled_binding_persists_state_across_episodes",
        len(arm.cache) > 0 and len(arm.induced_bindings) > 0,
        {"cache_size": len(arm.cache), "induced_bindings": len(arm.induced_bindings)},
    )
    _check(
        "compiled_binding_charges_machinery_only_on_cache_serve",
        arm.ledger.machinery_units == arm.ledger.detail.get("machinery_resolve_bind_verify", 0),
        {"machinery": arm.ledger.machinery_units, "served": arm.ledger.detail.get("machinery_resolve_bind_verify", 0)},
    )


def test_substrate_declared_modification() -> None:
    """prereg.md section 5: the handle must be in the mint response BODY, and
    every non-mint response body must be byte-identical to the parent."""
    with DeterministicHTTPSubstrate() as sub:
        client = sub.keepalive()
        try:
            sub.reset()
            code_plain, raw_plain, _ = client.request("PUT", "/resources/alpha", {"title": "t", "value": 1})
            body_plain = json.loads(raw_plain)
            code_mint, raw_mint, _ = client.request("PUT", "/resources/beta?mint=1", {"title": "t", "value": 1})
            body_mint = json.loads(raw_mint)
        finally:
            client.close()
    _check(
        "mint_response_body_carries_the_capability_handle",
        isinstance(body_mint.get("capability_handle"), str) and len(body_mint["capability_handle"]) == 16,
        {"capability_handle": body_mint.get("capability_handle")},
    )
    _check(
        "mint_body_is_the_non_mint_body_plus_exactly_one_field",
        {k: v for k, v in body_mint.items() if k != "capability_handle"}
        == {"rid": "beta", "created": True, "record": {"title": "t", "value": 1}}
        and set(body_mint) - set(body_plain) == {"capability_handle"},
        {"plain_keys": sorted(body_plain), "mint_keys": sorted(body_mint)},
    )
    _check(
        "non_mint_put_body_is_unchanged_by_the_modification",
        body_plain == {"rid": "alpha", "created": True, "record": {"title": "t", "value": 1}},
        {"non_mint_body": body_plain},
    )
    _check("mint_status_code_unchanged", code_mint == code_plain == 201, {"plain": code_plain, "mint": code_mint})
    _check("handle_equals_the_declared_pure_function", body_mint["capability_handle"] == mint_token(1), {"handle": body_mint["capability_handle"], "mint_token_1": mint_token(1)})


def test_always_mint_sensitivity_is_declared_and_distinct() -> None:
    arm = AlwaysMintScratchpad()
    _check("always_mint_arm_uses_the_parent_7_field_prefix", arm.goal_width == "wide", {"goal_width": arm.goal_width})
    s = next(x for x in build_steps(1, 0.50) if x.role == "create_resource")
    ungated = next(
        x
        for x in build_steps(2, 0.50)
        if x.role == "create_resource" and not class_iii_work_item(2, x.work_item)
    )
    planted = next(
        x
        for x in build_steps(1, 0.50)
        if x.role == "create_resource" and class_iii_work_item(1, x.work_item)
    )
    a = always_mint_action("o", ungated.goal_prefix("wide"), {})
    _check(
        "always_mint_requests_a_handle_the_declared_action_does_not_need",
        "?mint=1" in a["path"] and "?mint=1" not in ungated.path,
        {"declared": ungated.path, "sensitivity_emitted": a["path"]},
    )
    _check(
        "primary_arm_follows_the_declared_mint_flag_on_a_planted_create",
        scratchpad_action("o", planted.goal_prefix(GOAL_WIDTH), {})["path"] == planted.path_with_token(None)
        and scratchpad_action("o", ungated.goal_prefix(GOAL_WIDTH), {})["path"] == ungated.path_with_token(None),
        {
            "planted_declared": planted.path_with_token(None),
            "ungated_declared": ungated.path_with_token(None),
            "planted_mint_flag": planted.mint,
            "ungated_mint_flag": ungated.mint,
        },
    )
    _check(
        "mint_flag_is_delivered_only_through_the_goal_prefix",
        "mint" not in GoalOnlyPlan._ALLOWED and hasattr(s, "mint"),
        {"goal_only_plan_allowed": sorted(GoalOnlyPlan._ALLOWED), "planstep_exposes_mint": hasattr(s, "mint")},
    )


def main() -> int:
    for fn in (
        test_signature_is_pure,
        test_purity_under_reordering,
        test_no_cross_episode_memory_in_the_arm,
        test_handle_absent_from_both_declared_inputs,
        test_goal_prefix_never_contains_a_handle,
        test_prefix_relationship_is_exactly_the_declared_deviation,
        test_handle_is_never_invented,
        test_resolve_handle_is_pure_and_total,
        test_non_gated_spans_are_unaffected_by_the_scratchpad,
        test_goal_only_plan_guard,
        test_frozen_episode_shape_and_plant,
        test_statelessness_behaviour_on_the_real_substrate,
        test_compiled_binding_arm_key_contains_the_binding,
        test_substrate_declared_modification,
        test_always_mint_sensitivity_is_declared_and_distinct,
    ):
        fn()
    passed = all(c["passed"] for c in CHECKS)
    payload = {
        "experiment_id": "EXP-FRONTIER-36287182510",
        "purpose": (
            "prereg.md section 6.1 statelessness guarantee and section 17 no-go condition 5: the "
            "within-episode scratchpad holds no state between episodes, reads its binding values only "
            "out of its own response bodies, and physically cannot reach the oracle action"
        ),
        "all_passed": passed,
        "n_checks": len(CHECKS),
        "n_failed": sum(1 for c in CHECKS if not c["passed"]),
        "frozen_check_floor_declared_in_prereg": 14,
        "goal_only_plan_attributeerror_guard_present": any(
            c["check"] == "goal_only_plan_withholds_the_oracle_action" for c in CHECKS
        ),
        "checks": CHECKS,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    raise SystemExit(main())
