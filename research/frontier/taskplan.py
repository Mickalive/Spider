"""Pre-declared task plan for EXP-FRONTIER-36249071934.

Frozen-design provenance: prereg.md sections 5.2, 7.4, 8.1, 8.2.

STRUCTURE (fixed before any outcome measurement)
------------------------------------------------
An episode is 4 work items. A work item is exactly the six steps

    1. GET    /                      role=entry_point
    2. PUT    /resources/{rid}        role=create_resource
    3. GET    /resources/{rid}        role=read_resource
    4. PATCH  /resources/{rid}        role=update_resource
    5. GET    /resources              role=list_resources
    6. DELETE /resources/{rid}        role=delete_resource

=> 24 spans per episode, 1200 spans per arm over 50 episodes. That sits inside
the preregistered envelope ("~15-25 spans/episode", "~1,000 spans/arm").

Novelty control
---------------
A *work item* is either NOVEL (its resource identity is scoped to the episode,
so its create/read/update/delete requests and its collection-listing response
change every episode) or STRUCTURAL (its resource identity is a fixed constant
``s-const-{w}``, so its whole step signature is byte-identical every episode).
The novelty rate ``nu`` is the fraction of the 4 work items that are NOVEL and
is swept over {0.00, 0.25, 0.50, 0.75, 1.00}.

The MAIN arm uses ``nu = 0.50``: two novel and two structural work items. This
value was fixed before execution as the neutral midpoint of that grid, so the
headline point estimate is neither a floor nor a ceiling and does not favour
either architecture. It is recorded here in code so the choice is inspectable,
and the full sweep is reported separately as non-decision-gating evidence.

Realized per-span determinism is NOT equal to ``nu``: the ``GET /`` entry point
is byte-identical in every work item regardless of ``nu``, and a structural
work item's collection listing is identical too. The realized fraction is
therefore an *emergent measured quantity*, exactly as prereg.md section 7.1
requires, and the ``nu`` -> realized-fraction map is itself a reported result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

MAIN_NOVELTY_RATE = 0.50
SWEEP_NOVELTY_RATES = (0.00, 0.25, 0.50, 0.75, 1.00)

WORK_ITEMS_PER_EPISODE = 4
STEP_SEQUENCE: tuple[str, ...] = (
    "entry_point",
    "create_resource",
    "read_resource",
    "update_resource",
    "list_resources",
    "delete_resource",
)

SPANS_PER_EPISODE = WORK_ITEMS_PER_EPISODE * len(STEP_SEQUENCE)


@dataclass(frozen=True)
class Step:
    role: str
    method: str
    path: str
    body: Any = None
    expect_code: int = 200


def _rid(episode: int, work_item: int, novel: bool) -> str:
    return f"r-{episode:03d}-{work_item}" if novel else f"s-const-{work_item}"


def _body(episode: int, work_item: int, novel: bool) -> dict[str, Any]:
    """Deterministic request body; episode-scoped only for novel work items."""
    stem = f"title-{episode:03d}" if novel else "title-const"
    return {"title": stem, "value": work_item * 100 + (episode if novel else 0)}


def work_item_plan(episode: int, work_item: int, novel: bool) -> list[Step]:
    rid = _rid(episode, work_item, novel)
    return [
        Step("entry_point", "GET", "/", None, 200),
        Step("create_resource", "PUT", f"/resources/{rid}", _body(episode, work_item, novel), 201),
        Step("read_resource", "GET", f"/resources/{rid}", None, 200),
        Step("update_resource", "PATCH", f"/resources/{rid}", {"value": 9000 + work_item}, 200),
        Step("list_resources", "GET", "/resources", None, 200),
        Step("delete_resource", "DELETE", f"/resources/{rid}", None, 200),
    ]


def _with_nonce(step: Step, episode: int, index: int) -> Step:
    """prereg.md 8.2 NC-ZERO-DETERMINISM: "unique path/query/body per episode".

    Forces every span of every episode to carry an episode-unique query so that
    no span signature can repeat, including the otherwise always-identical
    entry-point fetch.
    """
    sep = "&" if "?" in step.path else "?"
    return Step(
        step.role,
        step.method,
        f"{step.path}{sep}n={episode:03d}-{index:02d}",
        step.body,
        step.expect_code,
    )


def episode_plan(episode: int, novelty_rate: float, force_nonce: bool = False) -> list[Step]:
    n_novel = int(round(novelty_rate * WORK_ITEMS_PER_EPISODE))
    steps: list[Step] = []
    for w in range(WORK_ITEMS_PER_EPISODE):
        steps.extend(work_item_plan(episode, w, novel=(w < n_novel)))
    if force_nonce:
        steps = [_with_nonce(s, episode, i) for i, s in enumerate(steps)]
    return steps


def goal_state() -> dict[str, Any]:
    """Goal state for matched-correctness scoring (prereg.md 7.3).

    "A task succeeds if the final state matches the expected goal state."
    Every work item ends with DELETE, so the empty resource store is the
    reachable goal state for every plan in this experiment. A step-level
    response-code check is applied on top of this by ``measure.py``.
    """
    return {"store_empty": True}


#: Pre-declared expected response status per role.
EXPECTED_CODES: dict[str, int] = {
    "entry_point": 200,
    "create_resource": 201,
    "read_resource": 200,
    "update_resource": 200,
    "list_resources": 200,
    "delete_resource": 200,
}
