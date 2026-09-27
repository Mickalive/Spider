"""Arm WITHIN_EPISODE_SCRATCHPAD of EXP-FRONTIER-36287182510 (new treatment arm).

Frozen-design provenance: ``spec.json`` ``measurement_validity.arms`` and
``prereg.md`` sections 5, 6.1 and 14.

The scientific question this arm exists to answer
------------------------------------------------
How far can a value propagate? prereg.md section 1 asks whether a
WITHIN-EPISODE scratchpad -- propagating only values it read from its own
earlier response bodies within the current episode, inducing no parameters,
compiling nothing across episodes and retaining nothing between episodes --
closes the observation-absent class (sigma_3).

Mechanism, exactly as preregistered
-----------------------------------
  * The decision is a **pure function** of

        (observable_state_sig, goal_prefix_wide_mint, scratchpad_values)

    implemented once, at module level, in :func:`scratchpad_action`. It closes
    over nothing: no instance attributes, no substrate, no plan, no step index.
  * ``scratchpad_values`` is a plain dict that lives only inside
    :meth:`WithinEpisodeScratchpad.run_episode` and is rebuilt from the
    response bodies the arm has itself read in the CURRENT episode. It is
    discarded at the episode boundary, so the arm holds nothing between
    episodes.
  * When a response body contains a ``capability_handle`` field, the arm stores
    it in the scratchpad keyed by the resource identity the body reports
    (``rid``), and also remembers it as ``last_handle``. That is the whole
    mechanism: read a value out of a prior response body, carry it one step
    forward, bind it into the next request. No parameter slots, no bind/verify
    /freshness machinery, no witness counting, no replay table.
  * The plan view handed to the arm is ``episodegen.GoalOnlyPlan``, which raises
    ``AttributeError`` for every attribute outside
    {index, work_item, role, token_required, novel, goal_prefix}. The oracle
    path and body are therefore unreachable at runtime, not merely unused, and
    ``mint`` is deliberately NOT in the allowed set either: the mint flag
    reaches the arm only as a field of the declared goal prefix.

Cost model (prereg.md sections 6.1 and 11)
-----------------------------------------
Parent-identical three-term ledger: 1 execution unit per span, 1 model unit per
span, 0 compile units, 0 machinery units. prereg.md 6.1 writes the model term as
"1 model unit per span (oracle call for spans not resolved from scratchpad)",
which admits two readings. This arm charges the literal primary reading
(1 model unit per span, identical to B-NO-MEMORY-CONDITIONED-WIDE, so the two
conditioned arms are compared on an identical ledger) and the runner also
reports the parenthetical reading as a declared sensitivity. The arm itself
never calls an oracle: its decision function is total, so the model unit is a
ledger charge for a per-span policy decision, exactly as it is for the parent's
conditioned arm (whose decision function is also total and whose oracle is a
counter that is never consulted for content).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Sequence

from ..episodegen_36272394045 import GoalStep
from ..substrate_deterministic_http import DeterministicHTTPSubstrate, KeepAliveClient, sha256_hex, span_signature
from ..taskplan import EXPECTED_CODES, Step
from .common import Ledger, SpanRecord

#: The declared goal-prefix width this arm is conditioned on. ``wide_mint`` is
#: ``wide`` plus the one declared field ``mint`` (episodegen DI-01); the handle
#: VALUE is in no prefix.
GOAL_WIDTH = "wide_mint"

#: role -> HTTP method. Identical to conditioned_no_memory.ROLE_METHOD, which is
#: the parent's public, frozen role->method map.
ROLE_METHOD: dict[str, str] = {
    "entry_point": "GET",
    "create_resource": "PUT",
    "read_resource": "GET",
    "update_resource": "PATCH",
    "list_resources": "GET",
    "delete_resource": "DELETE",
}

#: role -> capability query parameter. Frozen by the generator
#: (episodegen.CLASS_III_TOKEN_SLOTS: "t" for read_resource, "view" for
#: list_resources).
TOKEN_PARAM: dict[str, str] = {"read_resource": "t", "list_resources": "view"}


def parse_goal_prefix(prefix: str) -> dict[str, str]:
    """Parse the frozen goal/intent prefix. Pure; no state."""
    out: dict[str, str] = {}
    for field_text in prefix.split("||"):
        field_text = field_text.strip()
        if "=" in field_text:
            key, _, value = field_text.partition("=")
            out[key.strip()] = value.strip()
    return out


def resolve_handle(role: str, key: str, scratchpad_values: dict[str, Any]) -> tuple[str | None, str]:
    """Look the propagated value up in the scratchpad. Pure; no state.

    Returns ``(handle, source)``. ``source`` is ``"scratchpad_by_rid"``,
    ``"scratchpad_last_handle"`` or ``"absent"``, and is recorded per span so
    that the closure attribution in the report is measured rather than asserted.
    """
    if role == "list_resources":
        # The collection listing has no resource identity of its own; the only
        # value the arm can legitimately carry is the one it read most recently
        # from its own earlier response body in this episode.
        handle = scratchpad_values.get("last_handle")
        return (handle, "scratchpad_last_handle") if handle else (None, "absent")
    handle = (scratchpad_values.get("by_rid") or {}).get(key)
    return (handle, "scratchpad_by_rid") if handle else (None, "absent")


def scratchpad_action(
    observable_state_sig: str, goal_prefix: str, scratchpad_values: dict[str, Any]
) -> dict[str, Any]:
    """The treatment arm's entire decision procedure.

    ``observable_state_sig`` is hashed into the returned record so the function's
    dependence on it is explicit; every field actually read comes from the goal
    prefix or from the propagated scratchpad values. The capability handle value
    is in neither the observable state nor the goal prefix, which is precisely
    what makes the class-(iii) spans observation-absent.
    """
    goal = parse_goal_prefix(goal_prefix)
    role = goal["intent"]
    method = ROLE_METHOD[role]
    key = goal.get("key", "-")
    body_text = goal.get("body", "-")
    mint = goal.get("mint", "0") == "1"
    token_required = goal.get("token_required", "0") == "1"

    if role == "entry_point":
        path, body = "/", None
    else:
        path = "/resources" if role == "list_resources" else f"/resources/{key}"
        body = None if body_text == "-" else json.loads(body_text)
    if mint and role == "create_resource":
        # The declared plan action for a planted work item's create.
        path = f"{path}?mint=1"

    handle, source = (None, "not_required")
    if token_required:
        if role not in TOKEN_PARAM:  # pragma: no cover - the frozen plan has no other gated role
            raise ValueError(f"no declared capability parameter for intent {role!r}")
        handle, source = resolve_handle(role, key, scratchpad_values)
        if handle is not None:
            path = f"{path}?{TOKEN_PARAM[role]}={handle}"

    return {
        "method": method,
        "path": path,
        "body": body,
        "role": role,
        "expected_code": EXPECTED_CODES[role],
        "token_required": token_required,
        "token_supplied": handle is not None,
        "handle_source": source,
        "handle": handle,
        "mint_requested": mint,
        "observable_state_sig": observable_state_sig,
        "goal_width": GOAL_WIDTH,
    }


def always_mint_action(
    observable_state_sig: str, goal_prefix: str, scratchpad_values: dict[str, Any]
) -> dict[str, Any]:
    """DECLARED SENSITIVITY of :func:`scratchpad_action`, not the primary arm.

    Identical in every respect except that it requests a capability handle on
    EVERY ``create_resource`` span, whatever the declared plan action says. It
    exists so the DI-01 deviation (the extra ``mint`` prefix field) is auditable
    by measurement: an agent that is never told whether a create needs a
    capability pays for guessing, and this function measures the price.

    It is conditioned on the parent's frozen 7-field ``wide`` prefix, which
    carries no mint field at all, so the two functions differ in exactly one
    respect.
    """
    goal = parse_goal_prefix(goal_prefix)
    role = goal["intent"]
    method = ROLE_METHOD[role]
    key = goal.get("key", "-")
    body_text = goal.get("body", "-")
    token_required = goal.get("token_required", "0") == "1"

    if role == "entry_point":
        path, body = "/", None
    else:
        path = "/resources" if role == "list_resources" else f"/resources/{key}"
        body = None if body_text == "-" else json.loads(body_text)
    mint = role == "create_resource"
    if mint:
        path = f"{path}?mint=1"

    handle, source = (None, "not_required")
    if token_required:
        if role not in TOKEN_PARAM:  # pragma: no cover
            raise ValueError(f"no declared capability parameter for intent {role!r}")
        handle, source = resolve_handle(role, key, scratchpad_values)
        if handle is not None:
            path = f"{path}?{TOKEN_PARAM[role]}={handle}"

    return {
        "method": method,
        "path": path,
        "body": body,
        "role": role,
        "expected_code": EXPECTED_CODES[role],
        "token_required": token_required,
        "token_supplied": handle is not None,
        "handle_source": source,
        "handle": handle,
        "mint_requested": mint,
        "observable_state_sig": observable_state_sig,
        "goal_width": "wide",
    }


@dataclass
class WithinEpisodeScratchpad:
    """No persistent memory of any kind; one episode's values, then nothing."""

    arm: str = "WITHIN_EPISODE_SCRATCHPAD"
    ledger: Ledger = field(default_factory=Ledger)
    #: Which pure decision function this arm uses. A module-level ``def``; the
    #: only two values are the primary arm and its declared sensitivity.
    decide: Any = scratchpad_action
    goal_width: str = GOAL_WIDTH
    #: Operational counters, recorded as raw evidence. None of them is read by
    #: the decision function.
    episodes_run: int = 0
    scratchpad_resolved_spans: int = 0
    handle_reads_from_bodies: int = 0
    model_units_charged: int = 0

    # -- the scratchpad itself is a LOCAL of run_episode, by construction ----
    def run_episode(
        self,
        substrate: DeterministicHTTPSubstrate,
        client: KeepAliveClient,
        episode: int,
        plan: Sequence[GoalStep],
        records: list[SpanRecord],
    ) -> dict[str, Any]:
        from .common import observable_state_sig

        substrate.reset()  # fresh world + advanced episode counter, as the reference arm does
        self.episodes_run += 1
        store_snapshot: dict[str, Any] = dict(substrate.store)
        last_request: tuple[str, str] | None = None
        code_ok = True
        store_empty_at_start = len(substrate.store) == 0

        # -- the entire memory of this arm, for this episode, right here -----
        scratchpad_values: dict[str, Any] = {"by_rid": {}, "last_handle": None}
        # --------------------------------------------------------------------

        for plan_step in plan:
            state_sig = observable_state_sig(store_snapshot, last_request)
            decision = self.decide(state_sig, plan_step.goal_prefix(self.goal_width), scratchpad_values)
            # PRIMARY cost basis (prereg.md 6.1, literal): 1 model unit per span.
            self.ledger.charge("model")
            self.model_units_charged += 1
            self.ledger.charge("execution")
            if decision["token_supplied"]:
                self.ledger.bump("spans_resolved_from_scratchpad")
                self.scratchpad_resolved_spans += 1
            else:
                self.ledger.bump("spans_ungated_or_unresolved")

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

            # -- read the value out of THIS arm's own response body -----------
            observed_rid: str | None = None
            observed_handle: str | None = None
            try:
                parsed = json.loads(raw.decode("utf-8"))
            except Exception:  # pragma: no cover - every substrate response is JSON
                parsed = None
            if isinstance(parsed, dict):
                observed_handle = parsed.get("capability_handle")
                observed_rid = parsed.get("rid")
            if observed_handle:
                scratchpad_values["by_rid"][str(observed_rid)] = observed_handle
                scratchpad_values["last_handle"] = observed_handle
                self.handle_reads_from_bodies += 1
                self.ledger.bump("handle_values_read_from_response_bodies")
            # ------------------------------------------------------------------

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
                    signature=span_signature(step.method, step.path, _decl_headers(step.body), step.body, code, raw),
                    state_sig=state_sig,
                    decision_path="SCRATCHPAD_PROPAGATED" if decision["token_supplied"] else "SCRATCHPAD_PREFIX_ONLY",
                    detail={
                        "expected_code": EXPECTED_CODES[step.role],
                        "code_ok": ok,
                        "goal_width": self.goal_width,
                        "goal_prefix": plan_step.goal_prefix(self.goal_width),
                        "token_required": decision["token_required"],
                        "token_supplied": decision["token_supplied"],
                        "handle_source": decision["handle_source"],
                        "handle_used": decision["handle"],
                        "mint_requested": decision["mint_requested"],
                        "handle_observed_in_response_body": observed_handle,
                        "scratchpad_size_after_span": len(scratchpad_values["by_rid"]),
                    },
                )
            )
            store_snapshot = dict(substrate.store)
            last_request = (step.method, step.path)

        return {
            "episode": episode,
            "spans": len(plan),
            "model_calls": self.model_units_charged,
            "compiled_replays": 0,
            "compile_events": 0,
            "final_store_empty": len(substrate.store) == 0,
            "store_empty_at_episode_start": store_empty_at_start,
            "code_ok": code_ok,
            "handles_read_this_episode": sum(
                1 for r in records[-24:] if r.detail.get("handle_observed_in_response_body")
            ),
            "spans_resolved_from_scratchpad": sum(
                1 for r in records[-24:] if r.detail.get("token_supplied")
            ),
        }


class AlwaysMintScratchpad(WithinEpisodeScratchpad):
    """Declared sensitivity: mint on every create, with no ``mint`` prefix field.

    This is the arm a real agent would be if the task description never told it
    whether a create needs a capability. It is measured, not argued about, so
    the DI-01 deviation is auditable: it shows what the mint flag is worth in
    span-level action correctness.
    """

    def __init__(self) -> None:
        super().__init__(
            arm="WITHIN_EPISODE_SCRATCHPAD-NO-MINTFLAG",
            decide=always_mint_action,
            goal_width="wide",
        )


def _decl_headers(body: Any) -> dict[str, str]:
    return {"Content-Type": "application/json"} if body is not None else {}


__all__ = [
    "AlwaysMintScratchpad",
    "always_mint_action",
    "GOAL_WIDTH",
    "ROLE_METHOD",
    "TOKEN_PARAM",
    "WithinEpisodeScratchpad",
    "parse_goal_prefix",
    "resolve_handle",
    "scratchpad_action",
]
