"""Arm B of EXP-FRONTIER-36272394045: B-NO-MEMORY-CONDITIONED (treatment).

Frozen-design provenance: spec.json ``baselines[B-NO-MEMORY-CONDITIONED]`` and
``measurement_validity.arms``; prereg.md sections 7.2, 8 and 13.

Mechanism, exactly as preregistered
-----------------------------------
  * no compilation, no replay table, no witness counting, no deopt logic;
  * no parameter induction, no parameter slots, no bind/verify/freshness;
  * no cross-episode memory of any kind;
  * the decision is a **pure function** of
    ``(observable_state, goal_intent_prefix)``:

        action = conditioned_action(observable_state_sig, goal_prefix)

    The function is a module-level ``def`` with no closure over arm state, no
    instance attributes, and no access to the substrate, the plan, the step
    index, the work item identity, or the episode counter. ``prereg.md`` 13
    requires this to be "stateless function ... unit tested"; see
    ``research/frontier/test_conditioned_no_memory_36272394045.py``.

Cost model
----------
``prereg.md`` 13 ("Cost model mismatch | Abstract units defined identically to
parent: 1 per oracle call; reference includes compile/deopt per parent spec")
requires the *parent* ledger: 1 execution unit per span executed plus 1 model
unit per deopt-to-oracle invocation, and no compile and no machinery units
because this arm performs no resolution. The model-calls-only reading (1 unit
per oracle call, 0 per execution, per ``prereg.md`` 7.2's literal wording) is
reported alongside it as a declared sensitivity because it changes falsifier
clause 2's cost leg.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Sequence

from ..episodegen_36272394045 import GoalStep
from ..substrate_deterministic_http import DeterministicHTTPSubstrate, KeepAliveClient, sha256_hex, span_signature
from ..taskplan import EXPECTED_CODES, Step
from .common import Ledger, ModelOracle, SpanRecord

#: role -> HTTP method. Public, frozen, and the only world knowledge the
#: treatment arm is allowed beyond the goal prefix it is handed.
ROLE_METHOD: dict[str, str] = {
    "entry_point": "GET",
    "create_resource": "PUT",
    "read_resource": "GET",
    "update_resource": "PATCH",
    "list_resources": "GET",
    "delete_resource": "DELETE",
}


def parse_goal_prefix(prefix: str) -> dict[str, str]:
    """Parse the frozen goal/intent prefix. Pure; no state."""
    out: dict[str, str] = {}
    for field_text in prefix.split("||"):
        field_text = field_text.strip()
        if "=" in field_text:
            key, _, value = field_text.partition("=")
            out[key.strip()] = value.strip()
    return out


def conditioned_action(observable_state_sig: str, goal_prefix: str) -> dict[str, Any]:
    """The treatment arm's entire decision procedure.

    ``observable_state_sig`` is accepted and hashed into the record so the
    function's dependence on it is explicit, but the declared observable state
    (world_store_snapshot, last_request_method, last_request_path) is not
    sufficient to determine the next action for any of the three classes: it
    never contains the work item's resource identity, the request body, or the
    capability handle. Every field used below comes from the goal prefix.

    A span whose correct action requires the capability handle
    (``token_required=1``) receives the *ungated* request, because the handle is
    present in neither input. That is the operational definition of class (iii).
    """
    goal = parse_goal_prefix(goal_prefix)
    role = goal["intent"]
    method = ROLE_METHOD[role]
    key = goal.get("key", "-")
    body_text = goal.get("body", "-")
    token_required = goal.get("token_required", "0") == "1"

    if role == "entry_point":
        path, body = "/", None
    elif role in ("read_resource", "update_resource", "delete_resource"):
        path, body = f"/resources/{key}", (None if body_text == "-" else json.loads(body_text))
    elif role == "create_resource":
        path, body = f"/resources/{key}", (None if body_text == "-" else json.loads(body_text))
    elif role == "list_resources":
        path, body = "/resources", None
    else:  # pragma: no cover - the frozen plan has no other role
        raise ValueError(f"unknown intent {role!r}")

    if token_required:
        # No handle in either input: the best deterministic action available is
        # the ungated request. Recorded explicitly, never silently dropped.
        path = path.split("?")[0]

    return {
        "method": method,
        "path": path,
        "body": body,
        "role": role,
        "expected_code": EXPECTED_CODES[role],
        "token_supplied": False,
        "observable_state_sig": observable_state_sig,
    }


@dataclass
class ConditionedNoMemory:
    """No-memory, goal-conditioned executor. Holds no knowledge between spans."""

    arm: str = "B-NO-MEMORY-CONDITIONED"
    goal_width: str = "wide"
    ledger: Ledger = field(default_factory=Ledger)
    model_calls: int = 0
    oracle: ModelOracle = field(default_factory=ModelOracle)  # counter only, never consulted for content

    def run_episode(
        self,
        substrate: DeterministicHTTPSubstrate,
        client: KeepAliveClient,
        episode: int,
        plan: Sequence[GoalStep],
        records: list[SpanRecord],
    ) -> dict[str, Any]:
        store_snapshot: dict[str, Any] = dict(substrate.store)
        last_request: tuple[str, str] | None = None
        code_ok = True
        action_correct = 0

        from .common import observable_state_sig

        # NOTE (prereg.md 13, "Goal conditioning implementation leak"): ``plan`` is
        # a GoalOnlyPlan, which raises AttributeError for anything outside
        # {index, work_item, role, token_required, novel, goal_prefix}. The
        # oracle path and body are not merely unused, they are unreachable at
        # runtime. The decision function's purity is additionally established
        # statically and behaviourally by
        # research/frontier/test_conditioned_no_memory_36272394045.py. The only
        # inputs read below are ``observable_state_sig`` and
        # ``plan_step.goal_prefix(...)``.
        for plan_step in plan:
            state_sig = observable_state_sig(store_snapshot, last_request)
            decision = conditioned_action(state_sig, plan_step.goal_prefix(self.goal_width))
            self.ledger.charge("model")
            self.model_calls += 1
            self.ledger.charge("execution")

            step = Step(
                decision["role"],
                decision["method"],
                decision["path"],
                decision["body"],
                decision["expected_code"],
            )
            code, raw, sent = client.request(step.method, step.path, step.body)
            ok = code == EXPECTED_CODES[step.role]
            code_ok = code_ok and ok

            records.append(
                SpanRecord(
                    arm=self.arm,
                    episode=episode,
                    index=plan_step.index,
                    role=step.role,
                    work_item=plan_step.work_item,
                    method=step.method,
                    path=step.path,
                    body=step.body,
                    declared_headers={"content-type": "application/json"} if step.body is not None else {},
                    request_headers_sent=sent,
                    response_code=code,
                    response_body_hash=sha256_hex(raw),
                    signature=span_signature(
                        step.method, step.path, _decl_headers(step.body), step.body, code, raw
                    ),
                    state_sig=state_sig,
                    decision_path="GOAL_CONDITIONED",
                    detail={
                        "expected_code": EXPECTED_CODES[step.role],
                        "code_ok": ok,
                        "goal_width": self.goal_width,
                        "goal_prefix": plan_step.goal_prefix(self.goal_width),
                        "token_required": plan_step.token_required,
                        "token_supplied": decision["token_supplied"],
                    },
                )
            )
            store_snapshot = dict(substrate.store)
            last_request = (step.method, step.path)

        return {
            "episode": episode,
            "spans": len(plan),
            "model_calls": self.model_calls,
            "compiled_replays": 0,
            "compile_events": 0,
            "final_store_empty": len(substrate.store) == 0,
            "code_ok": code_ok,
            "action_correct": action_correct,
        }


def _decl_headers(body: Any) -> dict[str, str]:
    return {"Content-Type": "application/json"} if body is not None else {}
