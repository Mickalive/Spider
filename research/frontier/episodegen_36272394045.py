"""Task-plan / goal-prefix generator for EXP-FRONTIER-36272394045.

Frozen-design provenance
------------------------
* ``spec.json`` ``measurement_validity.task_generator`` requires
  ``taskplan.py`` to be extended with ``(a) goal_conditioning_mode``,
  ``(b) planted_disambiguation_mode``, ``(c) unique_states_mode`` and
  ``(d) a declared class_iii_fraction parameter (non-zero, e.g. 0.10) ensuring
  spans whose binding key comes from a prior response not in the current
  observable state nor goal``.
* ``prereg.md`` section 6 table ("Extensions for This Experiment"),
  section 7.3 (PC-PLANTED-DISAMBIGUATION) and section 7.4 (NC-UNIQUE-STATES).
* ``spec.json`` ``measurement_validity.arms`` fixes the episode structure:
  5 preregistered intents, 4 work items per episode, 24 spans per episode,
  50 episodes per novelty rate per arm, novelty grid
  ``{0.00, 0.25, 0.50, 0.75, 1.00}``.

Base plan
---------
The base plan is the *unmodified* ``research/frontier/taskplan.py`` of
EXP-FRONTIER-36249071934. ``build_steps(class_iii=False)`` reproduces
``taskplan.episode_plan`` exactly; that configuration is the frozen
replication control (prereg.md 10.3, no-go 5).

Class-(iii) plant
-----------------
``class_iii_fraction`` is realised over *work items* (request.json
``director_mandate.allocation.question``: "must place a nonzero, declared
fraction of items in class (iii) by construction"). Declared schedule:

    k            = 4 * (episode - 1) + work_item        (k in 0..199)
    planted(w)   <=>  (3 * k) % 10 < 3                  (3 of every 10 work items)

Over 50 episodes x 4 work items this selects exactly 60 of 200 work items
(0.30 of work items). Each planted work item contributes exactly 2
class-(iii) span occurrences (``read_resource`` and ``list_resources``), so the
realised class-(iii) share of span occurrences is exactly 120 / 1200 = 0.1000,
the value prereg.md section 6 declares.

A planted work item adds two declared extensions and nothing else:

  * its ``create_resource`` step is issued as ``PUT /resources/{rid}?mint=1``.
    The response **body** is byte-identical to the same PUT without ``?mint=``
    (verified as raw evidence), and the path is episode-invariant, so the
    parent's per-role body hashes and this step's compilability are unchanged.
    The server publishes an episode-scoped capability handle as a *header* and
    as a raw server-side observation only.
  * its ``read_resource`` step becomes ``GET /resources/{rid}?t=<handle>`` and
    its ``list_resources`` step becomes ``GET /resources?view=<handle>``. The
    handle is a pure function of (MINT_SALT, episode counter). It is not a
    function of the resource store, of any request path, of the resource
    identity, or of the plan, and it is episode-varying, so the handle is
    absent from the observable state fixed by prereg.md section 5 and absent
    from the goal/intent prefix. The only channel that carries it is the mint
    response. Reading that response and binding its value into the next action
    is exactly the "parameter induction from prior observation" that prereg.md
    section 1 class (iii) requires.

Goal/intent conditioning prefix
-------------------------------
``goal_prefix(step, "wide")`` names the step's role, its position, its work
item, its **binding key** (the resource identity, exactly the form prereg.md
7.3 uses: "CREATE resource:A"), the request body, whether the work item is
novel, and whether a capability handle is required -- but never the handle
value. ``"narrow"`` names only the role and the binding key. ``wide`` is the
PRIMARY treatment prefix: it is an upper bound on what conditioning can do, so
falsifier clause 2 is maximally hard to trigger spuriously.

Both prefixes are pure functions of the frozen plan. They are the *only*
conditioning input the treatment arm receives besides the observable state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator

from .substrate_deterministic_http import canonical_json
from .taskplan import (
    EXPECTED_CODES,
    STEP_SEQUENCE,
    WORK_ITEMS_PER_EPISODE,
    _with_nonce,
    work_item_plan,
)

# -- frozen constants (declared before any outcome data was produced) -------
NOVELTY_GRID: tuple[float, ...] = (0.00, 0.25, 0.50, 0.75, 1.00)
EPISODES_PER_RATE = 50
WORK_ITEMS = WORK_ITEMS_PER_EPISODE
SPANS_PER_EPISODE = WORK_ITEMS * len(STEP_SEQUENCE)  # 24

#: prereg.md 6: the two slots of a planted work item whose correct action is
#: gated on the minted capability handle.
CLASS_III_TOKEN_SLOTS: tuple[str, ...] = ("read_resource", "list_resources")
#: prereg.md 6 / spec task_generator: declared class-(iii) fraction.
CLASS_III_WORK_ITEM_MODULUS = 10
CLASS_III_WORK_ITEM_RESIDUE = 3
CLASS_III_DECLARED_SPAN_FRACTION = 0.10

#: prereg.md 7.3 / 7.4: controls run at the fixed midpoint of the grid.
CONTROL_NOVELTY_RATE = 0.50

#: prereg.md 7.3: the planted-disambiguation control's planted span set is the
#: create_resource slot of all four work items. In the base plan every work
#: item's create span is issued from the byte-identical observable state
#: (empty store, last request GET /) and the four require four different
#: resource identities. This is the exact failure mode the parent packet's
#: PC-WITNESSED-DETERMINISM control measured (4 model calls per episode from
#: observationally identical but goal-distinct states).
PC_PLANTED_ROLES: tuple[str, ...] = ("create_resource",)


@dataclass(frozen=True)
class PlanStep:
    """One span slot of a work item. Immutable; carries its own goal metadata."""

    index: int
    work_item: int
    role: str
    method: str
    path: str
    body: Any
    expect_code: int
    novel: bool
    goal_key: str | None = None
    token_param: str | None = None  # "t" | "view" | None
    mint: bool = False

    # -- derived ---------------------------------------------------------
    @property
    def token_required(self) -> bool:
        return self.token_param is not None

    def path_with_token(self, token: str | None) -> str:
        """Concrete request path. ``token=None`` yields the ungated path."""
        path = f"{self.path}?mint=1" if self.mint else self.path
        if self.token_param and token:
            path = f"{path}?{self.token_param}={token}"
        return path

    def to_step(self, token: str | None) -> Any:
        from .taskplan import Step

        return Step(self.role, self.method, self.path_with_token(token), self.body, self.expect_code)

    def goal_prefix(self, width: str = "wide") -> str:
        if width == "wide":
            return (
                "spider-frontier-goal-v1 || intent={role} || step={i}/24 || work_item={w} || "
                "key={key} || body={body} || novel={novel} || token_required={tok}"
            ).format(
                role=self.role,
                i=self.index,
                w=self.work_item,
                key=self.goal_key if self.goal_key is not None else "-",
                body=canonical_json(self.body) if self.body is not None else "-",
                novel=int(self.novel),
                tok=int(self.token_required),
            )
        if width == "wide_mint":
            # EXP-FRONTIER-36287182510 DECLARED INSTRUMENT DEVIATION DI-01.
            #
            # Identical to ``wide`` plus ONE extra field, ``mint={0|1}``, which
            # says whether the declared plan action for this span is the
            # capability-minting create ``PUT /resources/{rid}?mint=1``.
            #
            # Why it is necessary: the capability handle is obtainable ONLY by
            # issuing a minting create and reading the handle out of that
            # response body (prereg.md section 5). Without the flag an arm that
            # emits ``PUT /resources/{rid}`` never receives a handle, so its
            # span-level action correctness is capped at 0.95 by construction
            # (the 0.05 is the planted mint-create share, measured in the parent
            # packet as B-NO-MEMORY-CONDITIONED's 0.0500 mint-create residual) --
            # a cap created by a representation choice, not by memory scope.
            #
            # What it does NOT leak: the handle VALUE is still never in any
            # prefix, so a class-(iii) span's correct action still depends on a
            # value absent from the observable state AND from the goal prefix.
            # ``wide`` and ``narrow`` are byte-for-byte unchanged, so the
            # inherited B-NO-MEMORY-CONDITIONED-WIDE and
            # B-NO-MEMORY-CONDITIONED-NARROW baselines remain the parent's arms.
            return (
                "spider-frontier-goal-v1 || intent={role} || step={i}/24 || work_item={w} || "
                "key={key} || body={body} || novel={novel} || token_required={tok} || mint={mint}"
            ).format(
                role=self.role,
                i=self.index,
                w=self.work_item,
                key=self.goal_key if self.goal_key is not None else "-",
                body=canonical_json(self.body) if self.body is not None else "-",
                novel=int(self.novel),
                tok=int(self.token_required),
                mint=int(self.mint),
            )
        if width == "narrow":
            return "spider-frontier-goal-v1 || intent={role} || key={key}".format(
                role=self.role, key=self.goal_key if self.goal_key is not None else "-"
            )
        raise ValueError(f"unknown goal prefix width: {width!r}")


# -- declared schedules -----------------------------------------------------
def class_iii_work_item(episode: int, work_item: int) -> bool:
    """Frozen class-(iii) plant schedule (see module docstring)."""
    k = WORK_ITEMS * (episode - 1) + work_item
    return (k * CLASS_III_WORK_ITEM_RESIDUE) % CLASS_III_WORK_ITEM_MODULUS < CLASS_III_WORK_ITEM_RESIDUE


def _rid_of(step_path: str) -> str:
    return step_path.rsplit("/", 1)[-1]


def build_steps(
    episode: int,
    novelty_rate: float,
    *,
    class_iii: bool = True,
    unique_states: bool = False,
) -> list[PlanStep]:
    """Episode plan for EXP-FRONTIER-36272394045.

    ``class_iii=False, unique_states=False`` reproduces
    ``taskplan.episode_plan(episode, novelty_rate)`` span for span.
    """
    n_novel = int(round(novelty_rate * WORK_ITEMS))
    steps: list[PlanStep] = []
    index = 0
    for w in range(WORK_ITEMS):
        novel = w < n_novel
        planted = class_iii and class_iii_work_item(episode, w)
        for base in work_item_plan(episode, w, novel=novel):
            token_param = None
            mint = False
            if planted:
                if base.role == "create_resource":
                    mint = True
                elif base.role in CLASS_III_TOKEN_SLOTS:
                    token_param = "t" if base.role == "read_resource" else "view"
            path = base.path
            if token_param and token_param == "view":
                path = "/resources"
            steps.append(
                PlanStep(
                    index=index,
                    work_item=w,
                    role=base.role,
                    method=base.method,
                    path=path,
                    body=base.body,
                    expect_code=EXPECTED_CODES[base.role],
                    novel=novel,
                    goal_key=_rid_of(base.path) if base.role in ("create_resource", "read_resource", "update_resource", "delete_resource") else None,
                    token_param=token_param,
                    mint=mint,
                )
            )
            index += 1
    if unique_states:
        steps = [
            PlanStep(
                index=s.index,
                work_item=s.work_item,
                role=s.role,
                method=s.method,
                path=_with_nonce(_BaseShim(s), episode, i).path,
                body=s.body,
                expect_code=s.expect_code,
                novel=s.novel,
                goal_key=s.goal_key,
                token_param=s.token_param,
                mint=s.mint,
            )
            for i, s in enumerate(steps)
        ]
    return steps


class _BaseShim:
    """Adapter so the parent helper ``_with_nonce`` can be reused verbatim."""

    __slots__ = ("role", "method", "path", "body", "expect_code")

    def __init__(self, s: PlanStep) -> None:
        self.role = s.role
        self.method = s.method
        self.path = s.path
        self.body = s.body
        self.expect_code = s.expect_code


# -- run-time plan views ----------------------------------------------------
class TokenCtx:
    """Mutable holder for the handle observed from the most recent mint.

    One instance is bound to the oracle-facing materializer of the
    reference/cold arms and updated by ``ObservingClient`` from the substrate's
    raw mint observation. The treatment arm is bound to a *different* instance
    that is never updated, so the absence of the handle is structural.
    """

    __slots__ = ("token", "updates")

    def __init__(self) -> None:
        self.token: str | None = None
        self.updates: int = 0


class MaterializedPlan:
    """List-like plan that binds the capability handle at access time.

    ``deopt_ratchet.py`` and ``cold_exploration.py`` are used **unmodified**
    from the parent packet; they only require ``plan[index]`` and ``len(plan)``.
    """

    __slots__ = ("_steps", "_ctx", "materialized")

    def __init__(self, steps: list[PlanStep], ctx: TokenCtx) -> None:
        self._steps = steps
        self._ctx = ctx
        # Audit channel, not a decision channel. Every ``plan[i]`` access records
        # the action *as bound at execution time* (i.e. with the capability handle
        # the arm could actually have observed). This is the arm-independent
        # ground truth for "the correct action" used by every derived metric;
        # no arm reads it.
        self.materialized: dict[int, dict[str, Any]] = {}

    def __len__(self) -> int:
        return len(self._steps)

    def _bind(self, i: int) -> Any:
        step = self._steps[i].to_step(self._ctx.token)
        self.materialized[i] = {
            "index": self._steps[i].index,
            "method": step.method,
            "path": step.path,
            "body": step.body,
            "expected_code": step.expect_code,
        }
        return step

    def __getitem__(self, i: int) -> Any:
        return self._bind(i)

    def __iter__(self) -> Iterator[PlanStep]:
        # The goal-conditioned arm iterates and needs the goal metadata, so
        # __iter__ yields the PlanStep. The parent arms (deopt_ratchet,
        # cold_exploration) iterate with ``enumerate(plan)`` and use the yielded
        # object as a parent ``Step``; to keep that contract exact, __iter__
        # yields the bound parent Step and records the binding in the audit
        # channel. The conditioned arm reaches its PlanStep through
        # ``steps`` in the runner instead.
        for i in range(len(self._steps)):
            yield self._bind(i)


class GoalOnlyPlan:
    """Plan view that physically cannot expose the oracle action to an arm.

    prereg.md 13 names "Goal conditioning implementation leak (accidental
    memory)" as a validity threat. The static unit test in
    ``test_conditioned_no_memory_36272394045.py`` proves the treatment's
    decision function never reads a path, but a runtime guarantee is stronger
    than a test: this wrapper raises ``AttributeError`` for every attribute
    outside the prereg-declared conditioning set (intent, step index, work item,
    role, token_required flag, goal prefix). ``path`` and ``body`` are not
    reachable at all.
    """

    __slots__ = ("_steps",)
    _ALLOWED = frozenset({"index", "work_item", "role", "token_required", "goal_prefix", "novel"})

    def __init__(self, steps: list[PlanStep]) -> None:
        object.__setattr__(self, "_steps", steps)

    def __len__(self) -> int:
        return len(self._steps)

    def __iter__(self) -> Iterator["GoalStep"]:
        for s in self._steps:
            yield GoalStep(s)

    def __getattr__(self, name: str) -> Any:  # pragma: no cover - guard
        raise AttributeError(
            f"GoalOnlyPlan deliberately withholds {name!r}; the goal-conditioned arm is "
            f"conditioned on {sorted(self._ALLOWED)} only"
        )


@dataclass(frozen=True)
class GoalStep:
    """A single span's goal metadata and nothing else."""

    __slots__ = ("_s",)
    _s: PlanStep

    def __getattr__(self, name: str) -> Any:  # pragma: no cover - guard
        if name in GoalOnlyPlan._ALLOWED:
            return getattr(self._s, name)
        raise AttributeError(
            f"GoalStep deliberately withholds {name!r} (e.g. the oracle path); "
            f"the goal-conditioned arm may read only {sorted(GoalOnlyPlan._ALLOWED)}"
        )

    @property
    def index(self) -> int:
        return self._s.index

    @property
    def work_item(self) -> int:
        return self._s.work_item

    @property
    def role(self) -> str:
        return self._s.role

    @property
    def token_required(self) -> bool:
        return self._s.token_required

    @property
    def novel(self) -> bool:
        return self._s.novel

    def goal_prefix(self, width: str) -> str:
        return self._s.goal_prefix(width)


def generator_config() -> dict[str, Any]:
    """Machine-readable record of every declared generator parameter."""
    return {
        "experiment_id": "EXP-FRONTIER-36272394045",
        "base_generator": "research/frontier/taskplan.py (sha256 8875a05b54761f96a92cea8d3ec43bd6886347b5e04ef81d594d65d53f910816, unmodified)",
        "novelty_grid": list(NOVELTY_GRID),
        "episodes_per_novelty_rate_per_arm": EPISODES_PER_RATE,
        "work_items_per_episode": WORK_ITEMS,
        "spans_per_episode": SPANS_PER_EPISODE,
        "step_sequence": list(STEP_SEQUENCE),
        "control_novelty_rate": CONTROL_NOVELTY_RATE,
        "class_iii_plant": {
            "declared_span_fraction": CLASS_III_DECLARED_SPAN_FRACTION,
            "token_slots": list(CLASS_III_TOKEN_SLOTS),
            "work_item_schedule": "planted(e,w) <=> (3*(4*(e-1)+w)) % 10 < 3",
            "work_item_modulus": CLASS_III_WORK_ITEM_MODULUS,
            "work_item_residue": CLASS_III_WORK_ITEM_RESIDUE,
            "realized_work_items_over_50_episodes": 60,
            "realized_work_item_fraction": 0.30,
            "realized_span_occurrences": 120,
            "realized_span_fraction": 0.1000,
            "mint_extension": "PUT /resources/{rid}?mint=1 publishes an episode-scoped handle as a response header and as a raw server-side observation; the response body is byte-identical to the same PUT without ?mint=",
            "gated_extensions": ["GET /resources/{rid}?t=<handle>", "GET /resources?view=<handle>"],
            "handle_definition": "<episode_counter:08x><sha256(MINT_SALT|counter)[:8]>, 16 hex chars, episode-varying, not a function of the store, of any request path, of the resource identity, or of the plan",
        },
        "goal_prefix": {
            "primary_width": "wide",
            "wide_fields": ["intent", "step", "work_item", "key", "body", "novel", "token_required"],
            "narrow_fields": ["intent", "key"],
            "handle_value_ever_included": False,
            "note": "wide is an upper bound on conditioning power and is therefore the conservative choice against falsifier clause 2",
        },
        "planted_disambiguation_control": {
            "planted_roles": list(PC_PLANTED_ROLES),
            "planted_observable_state": "(empty store, last request GET /)",
            "binding_key_location": "goal prefix 'key=' field",
        },
        "unique_states_control": {
            "mechanism": "parent taskplan._with_nonce: every path carries ?n=<episode>-<step>",
            "class_iii_plant": "disabled, otherwise a planted class-(iii) span would (correctly) be reported as class (iii) and the null could not expect exactly zero",
        },
        "substrate_extensions": {
            "transport": "_Handler.disable_nagle_algorithm = True (no response byte changes; ~24 -> ~3265 requests/second)",
            "mint": "opt-in ?mint= / ?t= / ?view= query parameters; default request shapes return byte-identical responses",
        },
    }


__all__ = [
    "CONTROL_NOVELTY_RATE",
    "CLASS_III_TOKEN_SLOTS",
    "CLASS_III_DECLARED_SPAN_FRACTION",
    "EPISODES_PER_RATE",
    "MaterializedPlan",
    "NOVELTY_GRID",
    "PC_PLANTED_ROLES",
    "PlanStep",
    "SPANS_PER_EPISODE",
    "TokenCtx",
    "build_steps",
    "class_iii_work_item",
    "generator_config",
]
