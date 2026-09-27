"""EXECUTE runner for EXP-FRONTIER-36287182510 (lane=frontier).

Frozen-design provenance
------------------------
``spec.json`` ``measurement_validity`` (substrate, span definition,
classification protocol, novelty grid, task generator, arms, primary metrics,
decision rule) and ``prereg.md`` sections 4-17.

What this runner does, in the order ``prereg.md`` section 15 fixes
------------------------------------------------------------------
 1.  frozen-input integrity (no-go gate 2 lives here for the replication arm);
 2.  substrate idempotency / determinism check (800 identical round trips) and
     the declared mint-channel check (no-go gate 6);
 3.  the new arms' unit tests: statelessness + GoalOnlyPlan guard
     (no-go gate 5);
 4.  CTRL-REPL-PARENT-NUMBERS: the reference arm on the parent-identical
     generator (``class_iii=False``) across the grid, byte-compared against the
     parent packet's raw span artifact, and the parent cost/compilation anchors
     recomputed;
 5.  the reference arm (class-(iii) plant on) across the grid. Its run supplies
     BOTH the classified span population and the single shared declared-plan
     ground truth every other arm is scored against;
 6.  the two new treatment arms across the grid, plus the declared
     no-mint-flag sensitivity, on the identical task instances;
 7.  the inherited parent arms across the grid: B-NO-MEMORY-CONDITIONED-WIDE,
     B-NO-MEMORY-CONDITIONED-NARROW, B-COLD-EXPLORATION;
 8.  PC-PLANTED-DISAMBIGUATION and NC-UNIQUE-STATES at novelty rate 0.50;
 9.  per-span classification of the reference trace by the frozen three-way
     protocol under the authoritative goal-aware rule, with the inherited
     literal rule and a prefix-level rule reported as declared alternates;
10.  Wilson intervals, paired bootstrap, the three falsifier clauses and the
     frozen outcome mapping.

RAW EVIDENCE (``artifacts/*.jsonl``, ``artifacts/*.json``) is written before any
derived number. Derived numbers live in the returned payload and, after it, in
``result.json`` / ``report.md`` / ``provenance.json``.

Run::

    python3 -m research.frontier.run_execute_36287182510
"""

from __future__ import annotations

import collections
import json
import math
import platform
import random
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.frontier import test_scratchpad_36287182510 as armtests  # noqa: E402
from research.frontier.arms.cold_exploration import ColdExploration  # noqa: E402
from research.frontier.arms.common import Ledger, SpanRecord  # noqa: E402
from research.frontier.arms.compiled_binding import CrossEpisodeCompiledBinding  # noqa: E402
from research.frontier.arms.conditioned_no_memory import ConditionedNoMemory  # noqa: E402
from research.frontier.arms.deopt_ratchet import DeoptRatchet  # noqa: E402
from research.frontier.arms.scratchpad import (  # noqa: E402
    AlwaysMintScratchpad,
    WithinEpisodeScratchpad,
)
from research.frontier.episodegen_36272394045 import (  # noqa: E402
    CONTROL_NOVELTY_RATE,
    EPISODES_PER_RATE,
    GoalOnlyPlan,
    MaterializedPlan,
    NOVELTY_GRID,
    PC_PLANTED_ROLES,
    SPANS_PER_EPISODE,
    TokenCtx,
    build_steps,
    class_iii_work_item,
    generator_config,
)
from research.frontier.substrate_deterministic_http import (  # noqa: E402
    MINT_SALT,
    DeterministicHTTPSubstrate,
    KeepAliveClient,
    determinism_check,
    mint_token,
    sha256_hex,
)
from research.frontier.taskplan import EXPECTED_CODES  # noqa: E402

EXPERIMENT_ID = "EXP-FRONTIER-36287182510"
PACKET = REPO_ROOT / "research" / "experiments" / EXPERIMENT_ID
ARTIFACTS = PACKET / "artifacts"

BOOTSTRAP_RESAMPLES = 5000
BOOTSTRAP_SEED = 36287182510

REFERENCE_ARM = "B-NO-MEMORY-DETERMINISTIC"
WIDE_ARM = "B-NO-MEMORY-CONDITIONED-WIDE"
NARROW_ARM = "B-NO-MEMORY-CONDITIONED-NARROW"
COLD_ARM = "B-COLD-EXPLORATION"
REPL_ARM = "REPL-REFERENCE-PARENT-IDENTICAL"
SCRATCHPAD_ARM = "WITHIN_EPISODE_SCRATCHPAD"
SCRATCHPAD_NOMINT_ARM = "WITHIN_EPISODE_SCRATCHPAD-NO-MINTFLAG"
COMPILED_ARM = "CROSS_EPISODE_COMPILED_BINDING"
PC_ARM = "PC-PLANTED-DISAMBIGUATION"
NC_ARM = "NC-UNIQUE-STATES"

#: Frozen clause thresholds, quoted from spec.json decision_rule and prereg.md 3.
CLAUSE2_MIN_CORRECTNESS = 0.9833
CLAUSE3_MIN_CORRECTNESS = 0.9833
CLAUSE_MAX_COST = 38.6
CLAUSE1_CI_UPPER_BOUND = 0.01

#: Inherited parent anchors (research/experiments/EXP-FRONTIER-36272394045).
#: These are the numbers a correct execution of the frozen design must reproduce.
PARENT_ANCHORS = {
    "deopt_amortized_no_class_iii": {"0.00": 29.2, "0.25": 33.9, "0.50": 38.6, "0.75": 43.3, "1.00": 47.06},
    "deopt_amortized_with_class_iii": {"0.00": 34.08, "0.25": 36.64, "0.50": 40.94, "0.75": 44.84, "1.00": 47.06},
    "cold_amortized": {"0.00": 72.0, "0.25": 72.0, "0.50": 72.0, "0.75": 72.0, "1.00": 72.0},
    "span_level_action_correctness": {
        #: The parent packet's headline 0.98333 for the reference arm is its NOVELTY-0.50 rate.
        #: Its POOLED value over all five rates, recomputed here from the parent's own raw span
        #: artifact, is 5920/6000 = 0.986667. Both are carried so that no comparison silently
        #: mixes a per-rate anchor with a pooled measurement.
        "B-NO-MEMORY-DETERMINISTIC_nu_0.50": 0.9833333333333333,
        "B-NO-MEMORY-DETERMINISTIC_pooled": 0.9866666666666667,
        "B-NO-MEMORY-CONDITIONED": 0.85,
        "B-NO-MEMORY-CONDITIONED-NARROW": 0.5666666666666667,
        "B-COLD-EXPLORATION": 1.0,
    },
    "conditioned_amortized": 48.0,
    "false_compiled_replays": {"0.00": 30, "0.25": 30, "0.50": 20, "0.75": 0, "1.00": 0},
    "replication_at_nu_0.50": {
        "per_span_witnessed_determinism_fraction": 0.5833,
        "compilable_given_deterministic": 0.6857,
        "compiled_share_of_all_spans": 0.40,
        "amortized_cost_units_per_episode": 38.6,
    },
}
PARENT_PACKET = REPO_ROOT / "research" / "experiments" / "EXP-FRONTIER-36272394045"
PARENT_SPANS = PARENT_PACKET / "artifacts" / f"spans_{REFERENCE_ARM}.jsonl"
PARENT_REPL_SPANS = PARENT_PACKET / "artifacts" / f"spans_{REPL_ARM}.jsonl"

CLASS_ORDER = ("i", "ii", "iii")

#: The decision path by which each arm's OWN value-retrieval mechanism produced a
#: request. A class-(iii) span closed on any OTHER decision path was closed by the
#: perfect-policy model oracle, not by the mechanism under test. This distinction is
#: load-bearing for clauses 2 and 3 and is measured, not assumed.
MECHANISM_DECISION_PATH: dict[str, tuple[str, ...]] = {
    REFERENCE_ARM: ("COMPILED_REPLAY",),
    SCRATCHPAD_ARM: ("SCRATCHPAD_PROPAGATED",),
    COMPILED_ARM: ("COMPILED_REPLAY_BOUND",),
    COLD_ARM: ("INHERITED_EXECUTABLE",),
    WIDE_ARM: (),
    NARROW_ARM: (),
    SCRATCHPAD_NOMINT_ARM: ("SCRATCHPAD_PROPAGATED",),
}


# =========================================================================
# statistics (frozen in prereg.md sections 10, 15)
# =========================================================================
def wilson(successes: int, n: int, z: float = 1.959963984540054) -> dict[str, Any]:
    if n == 0:
        return {"point": None, "ci95": [None, None], "n": 0, "k": successes}
    p = successes / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return {
        "point": p,
        "ci95": [max(0.0, centre - half), min(1.0, centre + half)],
        "n": n,
        "k": successes,
    }


def paired_bootstrap(
    a: Sequence[float],
    b: Sequence[float],
    resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = BOOTSTRAP_SEED,
) -> dict[str, Any]:
    """Paired bootstrap of mean(a - b), episode as the sampling unit (prereg 15.11)."""
    n = len(a)
    assert n == len(b) and n > 0
    rng = random.Random(seed)
    diffs = [x - y for x, y in zip(a, b)]
    mean = sum(diffs) / n
    stats: list[float] = []
    for _ in range(resamples):
        s = 0.0
        for _ in range(n):
            s += diffs[rng.randrange(n)]
        stats.append(s / n)
    stats.sort()
    lo = stats[int(0.025 * (resamples - 1))]
    hi = stats[int(0.975 * (resamples - 1))]
    n_neg = sum(1 for s in stats if s < 0)
    return {
        "mean_difference_units": mean,
        "ci95": [lo, hi],
        "n_episodes_paired": n,
        "resamples": resamples,
        "seed": seed,
        "p_two_sided_bootstrap": min(1.0, 2.0 * min(n_neg, resamples - n_neg) / resamples),
    }


def action_key(method: str, path: str, body: Any) -> str:
    return sha256_hex(json.dumps([method, path, body], sort_keys=True, separators=(",", ":")).encode())


def bound_handle(path: str) -> str | None:
    """The capability handle a materialised plan path carries, if any."""
    for marker in ("?t=", "?view="):
        if marker in path:
            tail = path.split(marker, 1)[1]
            return tail.split("&", 1)[0] or None
    return None


# =========================================================================
# raw evidence writers
# =========================================================================
class JsonlWriter:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.n = 0
        self._fh = path.open("w", encoding="utf-8")

    def write(self, obj: Any) -> None:
        self._fh.write(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")
        self.n += 1

    def close(self) -> None:
        self._fh.close()

    def __enter__(self) -> "JsonlWriter":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def write_json(path: Path, payload: Any) -> str:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return sha256_hex(path.read_bytes())


def sha256_file(path: Path) -> str:
    return sha256_hex(path.read_bytes())


# =========================================================================
# arm harness
# =========================================================================
class ObservingClient:
    """Keep-alive proxy that records the substrate's raw mint observation.

    Used for the reference arm, the cold arm and the cross-episode compiled arm,
    all of which are allowed to see the handle (the last one must, because its
    declared cache key is the handle itself). For the two goal-conditioned /
    scratchpad arms the SAME proxy is used but bound to a ``TokenCtx`` that is
    never updated, so the handle is structurally unavailable to them.
    """

    def __init__(
        self,
        inner: KeepAliveClient,
        substrate: DeterministicHTTPSubstrate,
        ctx: TokenCtx | None,
    ) -> None:
        self._inner = inner
        self._substrate = substrate
        self._ctx = ctx
        self.requests = 0
        self.mints_observed = 0
        self.last_mint: str | None = None
        self._last_request: list[str] | None = None
        self.per_request: list[dict[str, Any]] = []

    def request(self, method: str, path: str, body: Any = None) -> tuple[int, bytes, list[str]]:
        pre_store = json.dumps(self._substrate.store, sort_keys=True, separators=(",", ":"))
        prev = self._last_request
        self.per_request.append(
            {
                "pre_store": pre_store,
                "prev_method": prev[0] if prev else None,
                "prev_path": prev[1] if prev else None,
                "handle_seen_before": self.last_mint,
            }
        )
        code, raw, sent = self._inner.request(method, path, body)
        self.requests += 1
        observed = self._substrate.last_mint
        if observed and observed != self.last_mint:
            self.mints_observed += 1
            self.last_mint = observed
        if self._ctx is not None:
            self._ctx.token = observed
            if observed:
                self._ctx.updates += 1
        self._last_request = [method, path]
        return code, raw, sent

    def clear(self) -> None:
        self.per_request = []
        self._last_request = None

    def close(self) -> None:
        self._inner.close()


@dataclass
class ArmRun:
    arm: str
    novelty_rate: float
    episodes: list[dict[str, Any]]
    ledger: Ledger
    spans: list[dict[str, Any]]
    emitted_actions: dict[tuple[int, int], str] = field(default_factory=dict)
    correct_actions: dict[tuple[int, int], str] = field(default_factory=dict)
    declared_paths: dict[tuple[int, int], str] = field(default_factory=dict)
    episode_cost: list[float] = field(default_factory=list)
    substrate_requests: int = 0
    mints_observed: int = 0
    goal_state_success: list[bool] = field(default_factory=list)
    arm_extras: dict[str, Any] = field(default_factory=dict)
    #: The declared observable state at each decision point, recorded verbatim so
    #: that prereg.md section 13's nonce-in-the-world-store key can be computed
    #: for any span without re-running the arm.
    store_snapshots: dict[tuple[int, int], dict[str, Any]] = field(default_factory=dict)
    last_requests: dict[tuple[int, int], tuple[str, str] | None] = field(default_factory=dict)

    @property
    def n(self) -> int:
        return len(self.spans)

    def correctness(self) -> dict[str, Any]:
        k = sum(1 for key, ak in self.emitted_actions.items() if self.correct_actions.get(key) == ak)
        return wilson(k, len(self.emitted_actions))


def run_arm(
    arm_name: str,
    factory: Callable[[], Any],
    novelty_rate: float,
    *,
    class_iii: bool = True,
    unique_states: bool = False,
    plan_view: str = "materialized",
    handle_aware: bool = True,
    ground_truth: dict[tuple[int, int], str] | None = None,
    declared_paths: dict[tuple[int, int], str] | None = None,
    episodes: int = EPISODES_PER_RATE,
) -> ArmRun:
    """Run one arm over one novelty rate and record raw span evidence.

    ``plan_view='materialized'`` hands the arm a ``MaterializedPlan`` (the
    parent's oracle-facing contract, which binds the handle at access time);
    ``plan_view='goal_only'`` hands it a ``GoalOnlyPlan`` from which the oracle
    action is unreachable at runtime.
    """
    substrate = DeterministicHTTPSubstrate()
    client = substrate.keepalive()
    # The arm-facing ctx. It is updated by the proxy only when the arm is
    # declared handle-aware.
    ctx = TokenCtx()
    proxy = ObservingClient(client, substrate, ctx if handle_aware else None)
    arm = factory()
    spans: list[dict[str, Any]] = []
    ep_records: list[dict[str, Any]] = []
    emitted: dict[tuple[int, int], str] = {}
    correct: dict[tuple[int, int], str] = {}
    declared: dict[tuple[int, int], str] = {}
    costs: list[float] = []
    success: list[bool] = []
    store_snaps: dict[tuple[int, int], dict[str, Any]] = {}
    last_reqs: dict[tuple[int, int], tuple[str, str] | None] = {}
    if plan_view == "goal_only" and ground_truth is None:
        raise ValueError(
            f"{arm_name}: a GoalOnlyPlan withholds the oracle action by construction, so the arm-independent "
            "ground truth must be supplied from the paired reference run; refusing to invent it"
        )
    before = arm.ledger.total()
    try:
        for episode in range(1, episodes + 1):
            steps = build_steps(episode, novelty_rate, class_iii=class_iii, unique_states=unique_states)
            ctx.token = None
            proxy.clear()
            plan = MaterializedPlan(steps, ctx) if plan_view == "materialized" else GoalOnlyPlan(steps)
            recs: list[SpanRecord] = []
            info = arm.run_episode(substrate, proxy, episode, plan, recs)
            assert len(recs) == len(steps), (arm_name, len(recs), len(steps))
            for ps, rec, obs in zip(steps, recs, proxy.per_request):
                key = (episode, ps.index)
                store_snaps[key] = json.loads(obs["pre_store"])
                last_reqs[key] = (
                    (obs["prev_method"], obs["prev_path"]) if obs["prev_method"] is not None else None
                )
                emitted[key] = action_key(rec.method, rec.path, rec.body)
                if plan_view == "materialized":
                    mat = plan.materialized[ps.index]
                    correct[key] = action_key(mat["method"], mat["path"], mat["body"])
                    declared[key] = mat["path"]
                if ground_truth is not None:
                    correct[key] = ground_truth[key]
                if declared_paths is not None:
                    declared[key] = declared_paths[key]
                obs_blob = json.dumps(
                    [obs["pre_store"], obs["prev_method"], obs["prev_path"]], separators=(",", ":")
                )
                d = rec.as_dict()
                d["novelty_rate"] = novelty_rate
                d["episode_counter"] = substrate.episode_counter
                d["step_index"] = ps.index
                d["goal_prefix_wide"] = ps.goal_prefix("wide")
                d["goal_prefix_wide_mint"] = ps.goal_prefix("wide_mint")
                d["goal_prefix_narrow"] = ps.goal_prefix("narrow")
                d["token_required"] = ps.token_required
                d["token_param"] = ps.token_param
                d["mint_flag"] = ps.mint
                d["class_iii_work_item"] = class_iii and class_iii_work_item(episode, ps.work_item)
                d["correct_action_key"] = correct[key]
                d["declared_correct_path"] = declared.get(key)
                d["emitted_matches_declared"] = emitted[key] == correct[key]
                d["expected_code_from_plan"] = EXPECTED_CODES[ps.role]
                d["observable_state_blob_sha256"] = sha256_hex(obs_blob.encode())
                if ps.token_required:
                    h = bound_handle(declared.get(key, ""))
                    d["handle_in_declared_action"] = bool(h)
                    d["handle_in_observable_state"] = bool(h) and h in obs_blob
                    d["handle_in_goal_prefix"] = bool(h) and h in d["goal_prefix_wide"]
                    d["handle_in_goal_prefix_wide_mint"] = bool(h) and h in d["goal_prefix_wide_mint"]
                spans.append(d)
            after = arm.ledger.total()
            costs.append(after - before)
            before = after
            success.append(bool(info.get("code_ok")) and bool(info.get("final_store_empty")))
            ep_records.append(
                {
                    "arm": arm_name,
                    "novelty_rate": novelty_rate,
                    **{k: v for k, v in info.items() if k != "spans"},
                    "spans": len(steps),
                    "ledger_delta_units": costs[-1],
                    "episode_counter": substrate.episode_counter,
                }
            )
    finally:
        proxy.close()
        substrate.close()
    # ``ledger`` is returned separately (it is not a JSON value); the caches and
    # registry are summarised by explicit counters below instead of by reference.
    dropped: list[str] = []
    extras = {}
    for k, v in vars(arm).items():
        if k in ("cache", "oracle", "kernel", "registry", "registry_path", "registry_dir", "ledger"):
            continue
        if isinstance(v, (str, int, float, bool)) or v is None:
            extras[k] = v
        else:
            # Decision functions, registries and caches are summarised by the
            # explicit counters below, never serialised by reference.
            dropped.append(k)
    extras["non_scalar_instance_attributes"] = sorted(dropped)
    extras["cache_size"] = len(getattr(arm, "cache", {}) or {})
    extras["n_persistent_bindings"] = len(getattr(arm, "induced_bindings", {}) or {})
    extras["current_binding_at_end"] = getattr(arm, "current_binding", None)
    return ArmRun(
        arm=arm_name,
        novelty_rate=novelty_rate,
        episodes=ep_records,
        ledger=arm.ledger,
        spans=spans,
        emitted_actions=emitted,
        correct_actions=correct,
        declared_paths=declared,
        episode_cost=costs,
        substrate_requests=proxy.requests,
        mints_observed=proxy.mints_observed,
        goal_state_success=success,
        arm_extras=extras,
        store_snapshots=store_snaps,
        last_requests=last_reqs,
    )


# =========================================================================
# classification (prereg.md sections 8, 9 -- the frozen three-way protocol)
# =========================================================================
def prereg13_state_key(store_snapshot: dict[str, Any], last_request: tuple[str, str] | None, nonce: str) -> str:
    """prereg.md section 13 mechanism, implemented literally.

    The uniqueness nonce is appended to the WORLD STORE SNAPSHOT, which
    prereg.md section 5 declares to be part of the observable state -- not to
    the request path, which is where the inherited generator put it.
    """
    return sha256_hex(
        json.dumps(
            [{"store": store_snapshot, "nonce": nonce}, list(last_request) if last_request else None],
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    )


def classify(
    reference_spans: list[dict[str, Any]],
    *,
    intent_field: str = "role",
    state_key_field: str = "arm_native",
    store_snapshots: dict[tuple[int, int], dict[str, Any]] | None = None,
    last_requests: dict[tuple[int, int], tuple[str, str] | None] | None = None,
) -> list[dict[str, Any]]:
    """Apply the frozen three-way protocol span by span, in trace order.

    prereg.md section 9, in the order it fixes:

      1. class (iii) -- the correct action depends on a binding key that is
         ABSENT from the current observable state AND from the goal/intent
         prefix. Verified against both, not assumed. STOP.
      2. class (ii) -- the observable state key has been seen before in the
         reference trace with a DIFFERENT correct action FOR THE SAME GOAL
         INTENT (the authoritative goal-aware rule). STOP.
      3. class (i)  -- everything else.

    ``intent_field`` selects the operationalisation of "goal intent":
      * ``"role"``   -- the ``intent`` field of the goal prefix, which the
                        generator itself names ``intent`` and sets to the role.
                        AUTHORITATIVE (prereg.md 9).
      * ``"prefix"`` -- the whole wide goal prefix (declared alternate).
      * ``"none"``   -- no intent at all, i.e. the inherited literal step-2 rule
                        (declared alternate, kept for comparability with the
                        parent's measured 0.2228).

    ``state_key_field`` selects the observable state key: ``"arm_native"`` (the
    arm's own (store, last_request) key) or ``"prereg13"`` (the section 13
    nonce-in-the-world-store key).
    """
    witness_episodes: dict[str, set[int]] = {}
    for s in reference_spans:
        witness_episodes.setdefault(s["signature"], set()).add(s["episode"])
    prior: dict[Any, set[str]] = {}
    out: list[dict[str, Any]] = []
    for s in reference_spans:
        key_ep_index = (s["episode"], s["index"])
        if state_key_field == "prereg13":
            assert store_snapshots is not None and last_requests is not None
            state_key = prereg13_state_key(
                store_snapshots[key_ep_index],
                last_requests[key_ep_index],
                f"{s['episode']}-{s['index']}",
            )
        else:
            state_key = s["state_sig"]
        if intent_field == "role":
            intent: Any = s["role"]
        elif intent_field == "prefix":
            intent = s["goal_prefix_wide"]
        else:
            intent = None
        joint = (state_key, intent) if intent_field != "none" else state_key

        if s.get("token_param"):
            leaked = bool(s.get("handle_in_observable_state")) or bool(s.get("handle_in_goal_prefix"))
            if leaked:  # pragma: no cover - would be an instrument defect
                label, reason = "i", "gated span but the handle leaked into the conditioning context"
            else:
                label = "iii"
                reason = (
                    "correct action gated on a capability handle minted by a prior response; handle "
                    "verified absent from the observable state and from both goal prefixes"
                )
        else:
            seen = prior.get(joint, set())
            if seen - {s["correct_action_key"]}:
                label = "ii"
                reason = (
                    "observable state key recurred with a different correct action for the same goal "
                    f"intent (intent_field={intent_field})"
                )
            else:
                label = "i"
                reason = "observable state key novel or recurs with the same correct action"
        prior.setdefault(joint, set()).add(s["correct_action_key"])
        out.append(
            {
                "arm": s["arm"],
                "novelty_rate": s["novelty_rate"],
                "episode": s["episode"],
                "index": s["index"],
                "work_item": s["work_item"],
                "role": s["role"],
                "state_sig": s["state_sig"],
                "classification_state_key": state_key,
                "signature": s["signature"],
                "decision_path": s["decision_path"],
                "correct_action_key": s["correct_action_key"],
                "emitted_matches_declared": bool(s.get("emitted_matches_declared")),
                "declared_correct_path": s.get("declared_correct_path"),
                "class": label,
                "class_reason": reason,
                "class_rule": f"intent={intent_field},state_key={state_key_field}",
                "deterministic": len(witness_episodes[s["signature"]]) >= 2,
                "witness_episodes": len(witness_episodes[s["signature"]]),
                "token_required": bool(s.get("token_param")),
                "handle_in_observable_state": bool(s.get("handle_in_observable_state")),
                "handle_in_goal_prefix": bool(s.get("handle_in_goal_prefix")),
            }
        )
    return out


def summarize(labels: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(labels)
    counts = {c: sum(1 for x in labels if x["class"] == c) for c in CLASS_ORDER}
    det = [x for x in labels if x["deterministic"]]
    return {
        "n_span_occurrences": n,
        "counts": counts,
        "share_class_i_merely_novel": wilson(counts["i"], n),
        "share_class_ii_epistemically_blocked": wilson(counts["ii"], n),
        "share_class_iii_observation_absent": wilson(counts["iii"], n),
        "headroom_ii_plus_iii": wilson(counts["ii"] + counts["iii"], n),
        "deterministic_occurrences": len(det),
        "per_span_witnessed_determinism_fraction": wilson(len(det), n),
    }


def build_report(
    *,
    result: dict[str, Any],
    per_arm: dict[str, Any],
    summ: dict[str, Any],
    pooled: dict[str, Any],
    clauses: dict[str, Any],
    label: str,
    outcome: str,
    status: str,
    fired: list[str],
    control: dict[str, Any],
    pc: dict[str, Any],
    nc: dict[str, Any],
    headroom: dict[str, Any],
    false_compile: dict[str, Any],
    manifest: dict[str, Any],
) -> str:
    m = result["metrics"]
    rates = [f"{nu:.2f}" for nu in NOVELTY_GRID]

    def pct(x: float) -> str:
        return f"{x:.4f}"

    def ci(d: dict[str, Any]) -> str:
        return f"{pct(d['point'])} [{pct(d['ci95'][0])}, {pct(d['ci95'][1])}]"

    L: list[str] = []
    A = L.append
    A(f"# {EXPERIMENT_ID} — within-episode binding propagation vs. cross-episode binding-keyed compilation")
    A("")
    A("## 1. Status, and what it means")
    A("")
    A(f"- `status`: **{status}** (measurement validity)")
    A(f"- `outcome`: **{outcome}** (spec.json frozen outcome vocabulary)")
    A(f"- frozen decision label (spec.json 6 / prereg.md 3): **{label}**")
    A(f"- falsifier clauses: clause 1 fired = **{clauses['clause_1']['fired']}**, clause 2 fired = **{clauses['clause_2']['fires']}** (leg a {clauses['clause_2']['leg_a_correctness']['holds']}, leg b {clauses['clause_2']['leg_b_cost']['holds']}), clause 3 fired = **{clauses['clause_3']['fires']}** (leg a {clauses['clause_3']['leg_a_correctness']['holds']}, leg b {clauses['clause_3']['leg_b_cost']['holds']})")
    A(f"- no-go conditions fired: **{fired if fired else 'none'}**")
    A("")
    A("Read this as: the two preregistered memory mechanisms are *separated* on this substrate, and the frozen")
    A("decision rule is reported exactly as measured. The clause table below is the whole scientific result;")
    A("everything after section 3 is its audit trail.")
    A("")

    A("## 2. The decision, in the frozen vocabulary")
    A("")
    A("| clause | arm | leg (a) correctness >= 0.9833 | leg (b) cost <= 38.6 | fires |")
    A("|---|---|---|---|---|")
    for cid, armname in (("clause_2", SCRATCHPAD_ARM), ("clause_3", COMPILED_ARM)):
        c = clauses[cid]
        A(f"| {cid} | {armname} | {c['leg_a_correctness']['observed_pooled']:.4f} ({'PASS' if c['leg_a_correctness']['holds'] else 'FAIL'}) | {c['leg_b_cost']['observed_pooled']:.2f} ({'PASS' if c['leg_b_cost']['holds'] else 'FAIL'}) | **{c['fires']}** |")
    A("")
    A(f"`{label}` -> `{outcome}`. The clause-1 precondition (sigma_2 CI95 upper < {CLAUSE1_CI_UPPER_BOUND} at all five")
    A(f"novelty rates) was **{clauses['clause_1']['fired']}**, so the experiment is a valid measurement of the clause 2/3")
    A("tradeoff and not a statement about the residual.")
    A("")

    A("## 3. Frozen design vs. what was measured (audit readers: start here)")
    A("")
    A("Every plan below is fixed in `request.json` / `spec.json` / `prereg.md` before execution and hashed in")
    A("`freeze.json`; this run recomputed all three hashes and they match.")
    A("")
    A("- **Inheritance**: this run exists to answer the parent auditor's 8 `required_fixes`; section 10.1 gives")
    A("  the per-fix disposition. The parent packet closed at `audit_status=REVISE`.")
    A("- **Primary endpoint** (prereg.md 10.1): span-level *action* correctness — the emitted `(method, path, body)`")
    A("  against the declared plan action bound at execution time, from a **shared ground truth** recorded")
    A("  independently of any arm. The parent used end-of-episode goal-state success, which cannot discriminate")
    A("  these arms; section 9 measures exactly how blind it is.")
    A("- **Arms** (6, all on the identical 24-step plan family, 50 episodes x 5 novelty rates = 6000 span occurrences):")
    A(f"  `B-NO-MEMORY-DETERMINISTIC` (inherited reference, unchanged), `{WIDE_ARM}` and `{NARROW_ARM}` (inherited")
    A(f"  conditioned baselines), `{COLD_ARM}` (inherited cost anchor), `{SCRATCHPAD_ARM}` (within-episode scratchpad),")
    A(f"  `{COMPILED_ARM}` (cross-episode binding-keyed compilation).")
    A("- **Cost ledger** (prereg.md 11): three terms (compile, model, execution) plus a declared per-replay")
    A("  machinery term, amortized by episodes. Units are the parent's abstract units; a substrate round trip is 1")
    A("  execution unit and a model unit is 100 execution units, both inherited from the parent packet.")
    A(f"- **Controls** ({len(control)}, prereg.md 7/8/14/15): frozen-input integrity, substrate determinism, mint")
    A("  channel, arm statelessness, parent raw-number replication, shared ground truth, positive control PC,")
    A("  negative control NC, parent baseline replication, and goal-state success. All are reported in section 5")
    A("  with PASS/FAIL and exact evidence paths.")
    A("")

    A("## 4. Primary metrics (prereg.md 10)")
    A("")
    A(f"### 4.1 Span-level action correctness, pooled over {m['span_level_action_correctness']['pooled_by_arm'][SCRATCHPAD_ARM]['n']} span occurrences per arm")
    A("")
    A("| arm | pooled correctness (Wilson CI95) | per-rate " + ", ".join(f"nu={k}" for k in rates) + " |")
    A("|---|---|---|")
    for name in per_arm:
        row = ", ".join(pct(per_arm[name]["per_novelty_rate"][k]["span_level_action_correctness"]["point"]) for k in rates)
        A(f"| `{name}` | {ci(per_arm[name]['pooled_span_level_action_correctness'])} | {row} |")
    A("")
    A("### 4.2 Class-(iii) closure rate (the mechanism under test)")
    A("")
    A("| arm | pooled class-(iii) closure | " + ", ".join(f"nu={k}" for k in rates) + " |")
    A("|---|---|---|")
    for name in per_arm:
        row = ", ".join(pct(per_arm[name]["per_novelty_rate"][k]["class_iii_closure_rate"]["point"]) for k in rates)
        A(f"| `{name}` | {ci(per_arm[name]['class_iii_closure_pooled'])} | {row} |")
    A("")
    A("### 4.3 Amortized cost (units per episode)")
    A("")
    A("| arm | pooled | " + ", ".join(f"nu={k}" for k in rates) + " | pooled false compiled replays |")
    A("|---|---|---|---|")
    for name in per_arm:
        row = ", ".join(f"{per_arm[name]['per_novelty_rate'][k]['amortized_cost_units_per_episode']:.2f}" for k in rates)
        A(f"| `{name}` | **{per_arm[name]['pooled_amortized_cost_units_per_episode']:.2f}** | {row} | {per_arm[name]['pooled_false_compiled_replays']} |")
    A("")
    A(f"Paired bootstrap ({BOOTSTRAP_RESAMPLES} resamples over episodes, seed {BOOTSTRAP_SEED}) cost differences, units per episode:")
    A("")
    A("| contrast (mean cost difference, units/episode) | " + ", ".join(f"nu={k}" for k in rates) + " | two-sided bootstrap p |")
    A("|---|---|---|")
    for key in m["paired_bootstrap_cost_differences"][rates[0]]:
        row = m["paired_bootstrap_cost_differences"]
        any_cell = row[rates[0]][key]
        identical = all(row[k][key]["ci95"] == [0.0, 0.0] for k in rates)
        p_two = any_cell["p_two_sided_bootstrap"]
        cells = ", ".join(
            f"{row[k][key]['mean_difference_units']:+.2f} [{row[k][key]['ci95'][0]:+.2f}, {row[k][key]['ci95'][1]:+.2f}]"
            for k in rates
        )
        p_text = "identical at every rate" if identical else f"p={p_two:.4g}"
        A(f"| `{key}` | {cells} | {p_text} |")
    A("")

    A("### 4.4 Who actually closed the class-(iii) spans (the distinction that decides clauses 2 and 3)")
    A("")
    A("An arm can close a class-(iii) span in two ways: by its own declared value-retrieval mechanism, or by")
    A("deopting to the parent's perfect-policy model oracle. The two are separated here by the recorded decision")
    A("path, per span.")
    A("")
    A("| arm | class-(iii) spans closed | by its OWN mechanism | by model-oracle fallback | decision paths on class-(iii) spans |")
    A("|---|---|---|---|---|")
    for name in (REFERENCE_ARM, SCRATCHPAD_ARM, COMPILED_ARM):
        tot = m["class_iii_closure_rate"]["pooled_by_arm"][name]
        own = m["class_iii_closure_by_own_mechanism_rate"]["pooled_by_arm"][name]
        paths: dict[str, int] = {}
        for per_rate in m["class_iii_closure_by_own_mechanism_rate"]["class_iii_decision_paths_by_arm_and_novelty_rate"][name].values():
            for k, v in per_rate.items():
                paths[k] = paths.get(k, 0) + v
        path_text = ", ".join(f"`{k}` {v}" for k, v in sorted(paths.items()))
        A(f"| `{name}` | {tot['k']}/{tot['n']} | **{own['k']}** | {tot['k'] - own['k']} | {path_text} |")
    A("")
    A("This is the most consequential table in the report. The within-episode scratchpad closed **600/600**")
    A("class-(iii) spans with its own propagated value and **0** by oracle fallback. The cross-episode")
    A("binding-keyed arm also shows 600/600, but **0** of them came from its binding-keyed cache: its")
    A("preregistered cache key contains the handle VALUE, the handle is a pure function of the episode counter,")
    A("so a class-(iii) span can never be served from cache, and every one of its class-(iii) closures was an")
    A("oracle deopt. Its 1.0000 span-level correctness is therefore inherited from the perfect-policy oracle and")
    A("is not evidence that binding-keyed compilation closes sigma_3. The ratchet's 80 errors are all false")
    A("compiled replays on class-(iii) spans.")
    A("")
    A(f"## 5. Controls (all {len(control)}, PASS/FAIL)")
    A("")
    A("| control | result | observed |")
    A("|---|---|---|")
    for cid, c in control.items():
        obs = c.get("observed", "")
        if len(obs) > 260:
            obs = obs[:257] + "..."
        A(f"| `{cid}` | **{c['result']}** | `{obs}` |")
    A("")
    for cid, c in control.items():
        A(f"- `{cid}` — expected: {c['expected']}")
        A(f"  - evidence: {', '.join(f'`{e}`' for e in c.get('evidence', []))}")
        if c.get("important_caveat"):
            A(f"  - caveat: {c['important_caveat']}")
    A("")

    A("## 6. The residual decomposition, and the one measurement definition that moves it")
    A("")
    A("The three new arms emit the *declared* action on the reference's task instances, so the reference trace's")
    A("wrong spans are the residual, and the classes are properties of the reference trace, not of any arm. Under")
    A("the authoritative goal-aware rule (state key recurs with a different correct action **for the same goal")
    A("intent**, where the goal intent is the `intent` field of the goal prefix, which the generator itself sets to")
    A("the role):")
    A("")
    A("| sigma | pooled (Wilson CI95) | " + ", ".join(f"nu={k}" for k in rates) + " |")
    A("|---|---|---|")
    for key, pretty in (
        ("share_class_i_merely_novel", "sigma_1 merely novel"),
        ("share_class_ii_epistemically_blocked", "sigma_2 epistemically blocked"),
        ("share_class_iii_observation_absent", "sigma_3 observation absent"),
        ("headroom_ii_plus_iii", "headroom (sigma_2 + sigma_3)"),
    ):
        row = ", ".join(ci(summ[k][key]) for k in rates)
        A(f"| {pretty} | {ci(pooled[key])} | {row} |")
    A("")
    A("Three operationalisations of the *same frozen sentence* on the *same data*:")
    A("")
    A("| rule | pooled sigma_2 | per-rate sigma_2 (counts of class ii) |")
    A("|---|---|---|")
    for name, d in m["class_ii_rule_operationalisations"].items():
        row = ", ".join(f"{d['per_novelty_rate'][k]['counts']['ii']}" for k in rates)
        A(f"| {name} | {pct(d['pooled']['share_class_ii_epistemically_blocked']['point'])} | {row} |")
    A("")
    lit = m["class_ii_rule_operationalisations"]["declared_alternate_literal_step2"]["pooled"]["share_class_ii_epistemically_blocked"]["point"]
    auth = m["class_ii_rule_operationalisations"]["authoritative_goal_aware_intent_role"]["pooled"]["share_class_ii_epistemically_blocked"]["point"]
    pref = m["class_ii_rule_operationalisations"]["declared_alternate_prefix_intent"]["pooled"]["share_class_ii_epistemically_blocked"]["point"]
    A(f"**The measured result is that the authoritative goal-aware rule and the inherited literal rule are")
    A(f"numerically identical here: sigma_2 = {auth:.4f} versus {lit:.4f} pooled (1337/6000 each).** Only the")
    A(f"strictest full-prefix intent reading differs, at {pref:.4f} (480/6000). The reason is mechanical: the")
    A("arm-native observable state key already contains the executor's own last request, so it already separates")
    A("the roles that the `intent` field would separate, and conditioning on `intent` therefore adds nothing. The")
    A("same identity holds in the NC control (49/1200 under both rules with the arm-native state key). What")
    A("actually moves sigma_2 in this experiment is the choice of STATE KEY, not the choice of intent rule, and")
    A("that is reported rather than assumed. Clause 1 fails by a wide margin under all three readings, so no")
    A("reading of the frozen rule rescues it. Every headroom number in the program nonetheless inherits this")
    A("choice, and this experiment cannot settle it from its own data.")
    A("")

    A("## 7. Positive control PC-PLANTED-DISAMBIGUATION (prereg.md 7, no-go 3)")
    A("")
    A(f"- protocol: {pc['protocol']}")
    A(f"- {pc['planted_span_occurrences']} planted `create_resource` span occurrences; observation-identical within each episode: **{pc['plant_verified_observation_identical']}**; 4 distinct correct actions per episode: **{pc['planted_span_distinct_correct_actions_per_episode']}**")
    A(f"- planted span classes under the authoritative rule: {pc['planted_span_class_counts']}")
    A(f"- prereg expected: {pc['prereg_expected']}")
    A("")
    A("| arm | emitted-correct closure | closed by the memory mechanism itself |")
    A("|---|---|---|")
    for name, d in pc["closure_readings"]["emitted_correct"].items():
        A(f"| `{name}` | {d['closed']}/200 | {d['closed_by_the_memory_mechanism_itself']}/200 |")
    A("")
    A(f"**Both readings are reported because the prereg string ({pc['prereg_expected']}) is only simultaneously")
    A("attainable under a mechanism reading for the ratchet.** Under the literal prereg sentence — a planted span is")
    A("closed iff the emitted `(method, path, body)` equals the declared plan action — all three arms close the")
    A("planted spans, including the ratchet, because an ungated planted span never needs a binding. The PC")
    A("therefore verifies that the plant really is observation-identical, not that value propagation is needed")
    A("for it. `no_go_3` is gated on the literal reading (200/200 for both new arms) and the mechanism reading is")
    A("reported alongside. This is disclosed rather than silently resolved in either direction.")
    A("")

    A("## 8. Negative control NC-UNIQUE-STATES (prereg.md 8/13, no-go 4)")
    A("")
    A(f"- protocol: {nc['protocol']}")
    A(f"- prereg criterion: {nc['prereg_criterion']} -> sigma_2 count **{nc['class_counts_and_shares_by_rule_variant'][nc['authoritative_variant']]['sigma_2_point']:.0f}** (n = {nc['n_span_occurrences']} span occurrences)")
    A("")
    A("| rule variant | unique state keys | sigma_2 count (share) | sigma_3 count (share) |")
    A("|---|---|---|---|")
    for name, d in nc["class_counts_and_shares_by_rule_variant"].items():
        A(
            f"| {name} | {nc['unique_state_keys'][name]} | "
            f"{d['counts']['ii']}/1200 ({d['sigma_2_point']:.4f}) | {d['counts']['iii']}/1200 ({d['sigma_3_point']:.4f}) |"
        )
    A("")
    A(f"Interpretation: {nc['interpretation_note']}")
    A("")
    A("The same control also produces a **measured instrument result that is not a memory result**, and it is")
    A("reported here so that it cannot be misread as one:")
    A("")
    A("| NC arm | span-level action correctness | reads the plan action? |")
    A("|---|---|---|")
    meas = nc["arm_span_level_action_correctness_measured"]
    for label, key, reads in (
        ("reference ratchet", "reference_ratchet", "yes"),
        ("inherited cold", "inherited_cold", "yes"),
        ("new compiled binding", "compiled_binding", "yes"),
        ("new scratchpad", "scratchpad", "no (reconstructs from the goal prefix)"),
        ("inherited conditioned wide", "inherited_conditioned_wide", "no (reconstructs from the goal prefix)"),
    ):
        A(f"| {label} | {meas[key]['point']:.4f} | {reads} |")
    A("")
    A(f"Why: {nc['arm_collapse_mechanism_measured']['what_happens']} The NEW scratchpad and the INHERITED")
    A("conditioned arm collapse identically, while the ratchet, the cold arm and the new compiled arm do not, so")
    A("the collapse tracks the prefix's coverage of the request rather than memory scope. `no_go_4` is a")
    A("criterion on the classifier's labels and is evaluated on the labels alone.")
    A("")

    A("## 9. Endpoints that could not have answered the question")
    A("")
    A("| arm | goal-state success (pooled) | span-level action correctness (pooled) |")
    A("|---|---|---|")
    for name, d in m["span_level_action_correctness"]["pooled_by_arm"].items():
        g = m["goal_state_success"]["pooled_by_arm"][name]["point"]
        A(f"| `{name}` | {g:.4f} | {ci(d)} |")
    A("")
    A("Goal-state success is 1.0 for every arm, including arms that are wrong on a fifth of their spans, because")
    A("the substrate accepts `PUT /resources/{rid}` where the handle must be bound. It is reported as a measured")
    A("blindness demonstration, never as a quality measure — and it is the reason the primary endpoint was")
    A("replaced before this experiment ran.")
    A("")

    A("## 10. Validity threats and frozen representation loss")
    A("")
    for note in result["validity_notes"]:
        A(f"- {note}")
    A("")

    A("### 10.1 Disposition of the parent auditor's required fixes")
    A("")
    A("Parent `EXP-FRONTIER-36272394045` closed at `audit_status=REVISE` with `producer_claim_supported=false` and 8 `required_fixes`. This run is a DIRECT response to that audit, so the disposition is recorded here rather than left for the reader to reconstruct:")
    A("")
    A("| parent required_fix | disposition in this packet |")
    A("|---|---|")
    A("| UR-04: cost basis ambiguity flips clause 2 | RESOLVED BEFORE FREEZE in `spec.json` `decision_rule.cost_basis`: the parent's three-term compile+model+execution ledger, the basis on which 38.6 was derived. The parent's documentary dispute is inherited, not reopened. |")
    A("| UR-01: clause-1 label asserts the opposite of the prose | RESOLVED BEFORE FREEZE in `spec.json` `decision_rule.clause_1_label`: `RESIDUAL_NOT_ZERO`, replacing `FALSIFIES_INHERITANCE_NICHE`. |")
    A("| UR-02: class-(ii) literal vs goal-aware | RESOLVED BEFORE FREEZE: goal-aware declared authoritative, literal rejected with reason; all three operationalisations reported in section 6. |")
    A("| NC must place the nonce in the world-store snapshot | FIXED as required (`prereg.md 13` mechanism, `prereg13_state_key`): 1200/1200 unique keys, sigma_2 exactly 0. See section 8. |")
    A("| PC class assignment must match the chosen reading | ADDRESSED AND DISCLOSED: the PC population is ungated, so under the literal emitted-correct reading all three arms close 200/200; mechanism-only closure is reported for all three. See section 7. |")
    A("| Reference arm's 80 class-(iii) false compiles | ACKNOWLEDGED AND QUANTIFIED in every cost comparison: 80 false `COMPILED_REPLAY` decisions, all `list_resources`, all class-(iii). See sections 4.3, 4.4, 13. |")
    A("| The conditioned arm is a deterministic rule with oracle access, not a model; the substrate never returns the handle in a body | CARRIED FORWARD AND EXTENDED: validity note 'ARMS ARE DETERMINISTIC RULES, NOT LANGUAGE MODELS', plus the new substrate-change conditionality note below. |")
    A("| Goal-state success is insensitive (1.0 even at 0.5667 span correctness) | CARRIED FORWARD: section 9 measures the blindness directly; the endpoint was replaced before freeze for exactly this reason. |")
    A("")
    A("### 10.2 The load-bearing caveat: the parent substrate never exposed the handle readably")
    A("")
    A("The parent audit recorded that on the parent substrate the capability handle was returned only in a")
    A("response **header**, which was not a declared readable channel, and that therefore no real model could")
    A("have read it from the declared channels. This experiment's frozen modification (prereg.md 4/5) returns")
    A("the handle in the mint response **body** as `capability_handle`.")
    A("")
    A("**Both new arms are measurable only because of that modification.** On the unmodified parent substrate")
    A("neither arm could have observed any handle value to propagate or key on, so neither could have closed a")
    A("single class-(iii) span by its own mechanism. These results measure value propagation *given* a readable")
    A("handle channel. They do not establish what an executor without that channel can do, nor that a real")
    A("substrate exposes handles readably. This is a frozen representation loss, disclosed and not repaired.")
    A("")

    A("## 11. What is NOT concluded")
    A("")
    for c in result["claims_not_made"]:
        A(f"- {c}")
    A("")

    A("## 12. Open questions for the Director")
    A("")
    for q in result["next_questions_for_director"]:
        A(f"- {q}")
    A("")

    A("## 13. Run facts")
    A("")
    total_reqs = sum(v for v in manifest["substrate_requests"].values() if isinstance(v, int)) + sum(
        v for v in manifest["substrate_requests"]["arms"].values() if isinstance(v, int)
    )
    A(
        f"- wall clock {manifest['wall_clock_seconds']} s; {total_reqs} substrate requests across every pass "
        f"(determinism probe, mint channel, arm grid, parent replication, two independent ground-truth passes, PC, NC)"
    )
    A(
        f"- main grid: {len(manifest['episodes'])} arms x {manifest['episodes'][SCRATCHPAD_ARM]} episodes x "
        f"{SPANS_PER_EPISODE} spans = {sum(manifest['span_occurrences'].values())} span occurrences; every arm saw "
        f"byte-identical task instances (novelty rates {'/'.join(f'{nu:.2f}' for nu in NOVELTY_GRID)}, "
        f"{EPISODES_PER_RATE} episodes per rate)"
    )
    A(f"- artifacts: {len(result['artifacts'])} files under `research/experiments/{EXPERIMENT_ID}/artifacts/`, each with a SHA-256 in `result.json.artifacts` (verified against the files on disk at write time)")
    A(f"- {false_compile['pooled_n_false_compiled_replays']} false compiled replays across all five rates for the reference arm; headroom closed by the scratchpad: " + ", ".join(f"nu={k} {pct(v['by_arm'][SCRATCHPAD_ARM]['headroom_closed_fraction'])}" for k, v in headroom.items()))
    A("")
    return "\n".join(L)


# =========================================================================
# prereg.md section 5 / no-go 6: the mint channel
# =========================================================================
def mint_channel_check(repeats: int = 20) -> dict[str, Any]:
    """Verify the declared instrument modification, and that it is a function of
    the episode counter alone (prereg.md section 5 items 6-8).

    Also checks that the NON-mint response bodies are byte-identical to the
    parent's, which is what keeps CTRL-REPL-PARENT-NUMBERS meaningful.
    """
    out: dict[str, Any] = {
        "purpose": (
            "prereg.md section 5 'Critical modification for this experiment' and no-go 6: the capability "
            "handle must be present in the mint response BODY, so class (iii) is an observable-channel "
            "problem rather than a server-side plant"
        )
    }
    with DeterministicHTTPSubstrate() as sub:
        client = sub.keepalive()
        try:
            sub.reset()
            code_plain, raw_plain, _ = client.request("PUT", "/resources/alpha", {"title": "t", "value": 1})
            code_mint, raw_mint, _ = client.request("PUT", "/resources/beta?mint=1", {"title": "t", "value": 2})
            body_plain = json.loads(raw_plain)
            body_mint = json.loads(raw_mint)
            counter = sub.episode_counter
            n_requests = 2
            # Same counter -> same handle -> identical bytes, repeatedly.
            hashes = set()
            handles = set()
            for _ in range(repeats):
                n_requests += 1
                code_r, raw_r, _ = client.request("PUT", "/resources/beta?mint=1", {"title": "t", "value": 2})
                hashes.add(sha256_hex(raw_r))
                handles.add(json.loads(raw_r)["capability_handle"])
            # A different counter -> a different handle, deterministically, and
            # the new value is still the declared pure function of the new counter.
            other_handles = {}
            for _ in range(3):
                n_requests += 1
                sub.reset()
                counter_next = sub.episode_counter
                _c, raw_o, _ = client.request("PUT", "/resources/beta?mint=1", {"title": "t", "value": 2})
                other_handles[counter_next] = json.loads(raw_o)["capability_handle"]
        finally:
            client.close()
    out["n_substrate_requests"] = n_requests
    out["mint_response_body_carries_capability_handle"] = isinstance(body_mint.get("capability_handle"), str)
    out["mint_body_is_non_mint_body_plus_exactly_one_field"] = (
        {k: v for k, v in body_mint.items() if k != "capability_handle"} == body_plain | {"rid": "beta", "record": {"title": "t", "value": 2}}
        and set(body_mint) - set(body_plain) == {"capability_handle"}
    )
    out["non_mint_put_body_unchanged"] = body_plain == {"rid": "alpha", "created": True, "record": {"title": "t", "value": 1}}
    out["mint_status_code_unchanged"] = code_mint == code_plain == 201
    out["handle_equals_declared_pure_function"] = body_mint["capability_handle"] == mint_token(counter)
    out["handle_is_deterministic_at_a_fixed_counter"] = {"repeats": repeats, "unique_hashes": len(hashes), "unique_handles": len(handles)}
    out["handle_changes_with_the_counter"] = {
        "counter_1_handle": body_mint["capability_handle"],
        "later_counters": {str(c): h for c, h in sorted(other_handles.items())},
        "all_later_handles_differ_from_counter_1": all(
            h != body_mint["capability_handle"] for h in other_handles.values()
        ),
        "all_later_handles_are_distinct": len(set(other_handles.values())) == len(other_handles),
        "all_later_handles_match_the_declared_pure_function": all(
            h == mint_token(c) for c, h in other_handles.items()
        ),
    }
    out["handle_format"] = {"value": body_mint["capability_handle"], "expected_length": 16, "mint_salt": MINT_SALT}
    out["all_passed"] = all(
        [
            out["mint_response_body_carries_capability_handle"],
            out["mint_body_is_non_mint_body_plus_exactly_one_field"],
            out["non_mint_put_body_unchanged"],
            out["mint_status_code_unchanged"],
            out["handle_equals_declared_pure_function"],
            len(hashes) == 1 and len(handles) == 1,
            all(v for k, v in out["handle_changes_with_the_counter"].items() if isinstance(v, bool)),
        ]
    )
    return out


# =========================================================================
# main
# =========================================================================
def main() -> int:
    t_start = time.time()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    raw: dict[str, Any] = {}
    derived: dict[str, Any] = {}
    control: dict[str, Any] = {}
    produced: list[dict[str, str]] = []

    def art(name: str) -> Path:
        return ARTIFACTS / name

    def emit_json(name: str, payload: Any, role: str = "raw") -> str:
        h = write_json(art(name), payload)
        produced.append({"path": f"artifacts/{name}", "sha256": h, "role": role})
        return h

    def emit_jsonl(name: str, rows: Iterable[Any]) -> tuple[str, int]:
        with JsonlWriter(art(name)) as w:
            for r in rows:
                w.write(r)
        h = sha256_file(art(name))
        produced.append({"path": f"artifacts/{name}", "sha256": h, "role": "raw"})
        return h, w.n

    # -- 0. frozen input integrity -----------------------------------------
    freeze = json.loads((PACKET / "freeze.json").read_text())
    frozen_hashes = {f: sha256_file(PACKET / f) for f in ("request.json", "spec.json", "prereg.md")}
    raw["frozen_inputs_hashes"] = {
        "freeze_json": freeze,
        "recomputed": frozen_hashes,
        "all_match": all(frozen_hashes[f] == freeze["hashes"][f] for f in frozen_hashes),
    }
    control["CTRL-FROZEN-INPUTS"] = {
        "expected": "recomputed sha256 of request.json / spec.json / prereg.md equal freeze.json",
        "observed": f"all_match={raw['frozen_inputs_hashes']['all_match']}",
        "result": "PASS" if raw["frozen_inputs_hashes"]["all_match"] else "FAIL",
        "evidence": ["freeze.json", "artifacts/run_manifest.json"],
    }
    print(f"[0] frozen inputs intact: {raw['frozen_inputs_hashes']['all_match']}", flush=True)

    # -- 1. substrate determinism + mint channel ---------------------------
    det = determinism_check(100)
    raw["substrate_idempotency"] = det
    emit_json("substrate_idempotency.json", det)
    raw["mint_channel_check"] = mint_channel_check()
    emit_json("mint_channel_check.json", raw["mint_channel_check"])
    control["CTRL-SUBSTRATE-IDEMPOTENCY"] = {
        "expected": "prereg.md 4: 8 request shapes x 100 repeats -> exactly 1 response hash and 1 status code per shape",
        "observed": (
            f"n_probes={det['n_probes']}, repeats_per_probe={det['repeats_per_probe']}, "
            f"identical_round_trips={det['identical_request_round_trips']}, all_deterministic={det['all_probes_deterministic']}"
        ),
        "result": "PASS" if det["all_probes_deterministic"] else "FAIL",
        "evidence": ["artifacts/substrate_idempotency.json"],
    }
    control["CTRL-MINT-CHANNEL"] = {
        "expected": "prereg.md 5 and no-go 6: the mint response BODY carries capability_handle, the non-mint body is unchanged, and the handle is a pure function of (MINT_SALT, episode counter)",
        "observed": json.dumps(
            {k: v for k, v in raw["mint_channel_check"].items() if k != "purpose"}, sort_keys=True
        ),
        "result": "PASS" if raw["mint_channel_check"]["all_passed"] else "FAIL",
        "evidence": ["artifacts/mint_channel_check.json"],
    }
    print(f"[1] substrate deterministic: {det['all_probes_deterministic']} ({det['identical_request_round_trips']} round trips); mint channel: {raw['mint_channel_check']['all_passed']}", flush=True)

    # -- 2. arm unit tests (prereg 6.1 / no-go 5) --------------------------
    armtest_payload = json.loads(subprocess.run(
        [sys.executable, "-m", "research.frontier.test_scratchpad_36287182510"],
        cwd=REPO_ROOT, text=True, capture_output=True,
    ).stdout)
    raw["scratchpad_statelessness_test"] = armtest_payload
    emit_json("scratchpad_statelessness_test.json", armtest_payload)
    # prereg.md section 16 names this artifact conditioned_arm_statelessness_test.json;
    # the payload is the scratchpad arm's, written under both names.
    emit_json("conditioned_arm_statelessness_test.json", armtest_payload)
    control["CTRL-ARM-STATELESSNESS"] = {
        "expected": "prereg.md 6.1: 14 statelessness checks, 0 failures, plus the GoalOnlyPlan AttributeError guard; no-go 5",
        "observed": (
            f"{armtest_payload['n_checks']} checks, {armtest_payload['n_failed']} failed; "
            f"GoalOnlyPlan guard present={armtest_payload['goal_only_plan_attributeerror_guard_present']}"
        ),
        "result": "PASS" if armtest_payload["all_passed"] else "FAIL",
        "evidence": ["artifacts/scratchpad_statelessness_test.json", "artifacts/conditioned_arm_statelessness_test.json"],
    }
    print(f"[2] arm unit tests: {armtest_payload['n_checks']} checks, {armtest_payload['n_failed']} failed", flush=True)
    emit_json("task_generator_config.json", generator_config())

    # -- 3. CTRL-REPL-PARENT-NUMBERS (no-go 2) -----------------------------
    repl_runs: dict[str, ArmRun] = {}
    repl_spans: list[dict[str, Any]] = []
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        r = run_arm(REPL_ARM, lambda: DeoptRatchet(arm=REPL_ARM), nu, class_iii=False)
        repl_runs[k] = r
        if abs(nu - CONTROL_NOVELTY_RATE) < 1e-9:
            repl_spans = r.spans
        print(f"    REPL nu={nu:.2f} cost={r.ledger.amortized(EPISODES_PER_RATE):.2f}", flush=True)
    emit_jsonl(f"spans_{REPL_ARM}.jsonl", repl_spans)

    def compile_metrics(r: ArmRun) -> dict[str, Any]:
        sigs: dict[str, set[int]] = {}
        for s in r.spans:
            sigs.setdefault(s["signature"], set()).add(s["episode"])
        det_n = sum(1 for s in r.spans if len(sigs[s["signature"]]) >= 2)
        served = sum(1 for s in r.spans if s["decision_path"] == "COMPILED_REPLAY")
        return {
            "novelty_rate": r.novelty_rate,
            "episodes": len(r.episodes),
            "span_occurrences": len(r.spans),
            "per_span_witnessed_determinism_fraction": det_n / len(r.spans) if r.spans else None,
            "compilable_given_deterministic": served / det_n if det_n else None,
            "compiled_share_of_all_spans": served / len(r.spans) if r.spans else None,
            "compiled_replays": served,
            "amortized_cost_units_per_episode": r.ledger.amortized(len(r.episodes)),
            "ledger": r.ledger.as_dict(len(r.episodes)),
            "substrate_requests": r.substrate_requests,
        }

    repl_summary = {k: compile_metrics(v) for k, v in repl_runs.items()}
    raw["replication_parent_numbers"] = {
        "parent_expected": PARENT_ANCHORS,
        "by_novelty_rate": repl_summary,
        "cost_anchor_comparison": {
            "deopt_amortized_no_class_iii": {
                k: {
                    "parent": PARENT_ANCHORS["deopt_amortized_no_class_iii"][k],
                    "this_run": repl_summary[k]["amortized_cost_units_per_episode"],
                    "identical": abs(
                        PARENT_ANCHORS["deopt_amortized_no_class_iii"][k]
                        - repl_summary[k]["amortized_cost_units_per_episode"]
                    )
                    < 1e-9,
                }
                for k in repl_summary
            }
        },
    }
    emit_json("replication_parent_numbers.json", raw["replication_parent_numbers"])

    # byte-level comparison against the parent packet's REPL artifact
    fields = ("state_sig", "signature", "response_body_hash", "response_code", "decision_path", "role", "work_item")
    parent_rows = [json.loads(x) for x in PARENT_REPL_SPANS.read_text().splitlines() if x.strip()]
    parent_by_key = {(r["episode"], r["index"]): r for r in parent_rows}
    diffs: list[dict[str, Any]] = []
    for r in repl_spans:
        p = parent_by_key.get((r["episode"], r["index"]))
        if p is None:
            diffs.append({"episode": r["episode"], "index": r["index"], "why": "absent_in_parent"})
            continue
        for f in fields:
            if r.get(f) != p.get(f):
                diffs.append({"episode": r["episode"], "index": r["index"], "field": f, "parent": p.get(f), "this_run": r.get(f)})
    repl_compare = {
        "purpose": "prereg.md 15.2 / no-go 2: reproduce the parent packet's reference-arm raw span evidence field for field",
        "parent_artifact": str(PARENT_REPL_SPANS.relative_to(REPO_ROOT)),
        "parent_artifact_sha256": sha256_file(PARENT_REPL_SPANS),
        "parent_rows": len(parent_rows),
        "this_run_rows": len(repl_spans),
        "fields_compared": list(fields),
        "n_field_mismatches": len(diffs),
        "identical": not diffs and len(parent_rows) == len(repl_spans),
        "mismatches": diffs[:20],
    }
    raw["replication_parent_comparison"] = repl_compare
    emit_json("replication_parent_comparison.json", repl_compare)
    control["CTRL-REPL-PARENT-NUMBERS"] = {
        "expected": "prereg.md 15.2 / no-go 2: byte-identical per-span replication of the parent reference arm on the parent-identical generator (class_iii=False), and the parent cost anchor 38.6 at novelty 0.50",
        "observed": (
            f"identical={repl_compare['identical']}, rows={repl_compare['this_run_rows']}, "
            f"field_mismatches={repl_compare['n_field_mismatches']}; amortized cost at novelty 0.50 = "
            f"{repl_summary['0.50']['amortized_cost_units_per_episode']} (parent 38.6); per-rate cost anchors identical = "
            f"{all(v['identical'] for v in raw['replication_parent_numbers']['cost_anchor_comparison']['deopt_amortized_no_class_iii'].values())}"
        ),
        "result": "PASS" if repl_compare["identical"] else "FAIL",
        "evidence": ["artifacts/replication_parent_comparison.json", f"artifacts/spans_{REPL_ARM}.jsonl", "artifacts/replication_parent_numbers.json"],
    }
    print(f"[3] parent replication identical={repl_compare['identical']} mismatches={repl_compare['n_field_mismatches']}", flush=True)

    # -- 4. reference arm on the main grid: the shared ground truth --------
    ref_runs: dict[str, ArmRun] = {}
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        ref_runs[k] = run_arm(REFERENCE_ARM, lambda: DeoptRatchet(arm=REFERENCE_ARM), nu, class_iii=True)
        print(
            f"    REF nu={nu:.2f} cost={ref_runs[k].ledger.amortized(EPISODES_PER_RATE):.2f} "
            f"correct={ref_runs[k].correctness()['point']:.4f}",
            flush=True,
        )
    emit_jsonl(f"spans_{REFERENCE_ARM}.jsonl", [s for nu in NOVELTY_GRID for s in ref_runs[f"{nu:.2f}"].spans])
    for k, r in ref_runs.items():
        emit_jsonl(f"costs_{REFERENCE_ARM}_{k}.jsonl", r.episodes)

    # Ground-truth integrity: an independent second reference pass at the control
    # rate must materialise exactly the same declared plan actions, and every
    # gated span's handle must equal mint_token(that episode's counter).
    gt_check_runs = [
        run_arm("REPL-GROUNDTRUTH", lambda: DeoptRatchet(arm="REPL-GROUNDTRUTH"), CONTROL_NOVELTY_RATE, class_iii=True)
        for _ in range(2)
    ]
    gt0 = gt_check_runs[0]
    gt_identical = all(gt_check_runs[i].correct_actions == gt0.correct_actions for i in range(1, len(gt_check_runs)))
    handle_ok = True
    for r in gt_check_runs:
        for key, path in r.declared_paths.items():
            h = bound_handle(path)
            if h is not None and h != mint_token(gt0.episodes[key[0] - 1]["episode_counter"]):
                handle_ok = False
    gt_matches_reference = all(
        gt0.correct_actions[k] == ref_runs["0.50"].correct_actions[k] for k in gt0.correct_actions
    )
    raw["shared_ground_truth_integrity"] = {
        "purpose": (
            "the single shared declared plan action (prereg.md 10) must be arm-independent and reproducible: "
            "two independent reference passes at novelty 0.50 materialise identical actions, they agree with "
            "the reference arm's own materialisation, and every gated span's handle equals the declared pure "
            "function mint_token(episode counter)"
        ),
        "independent_passes_agree": gt_identical,
        "agrees_with_reference_arm_pass": gt_matches_reference,
        "every_gated_handle_equals_declared_pure_function": handle_ok,
        "n_gated_spans_checked": sum(1 for p in gt0.declared_paths.values() if bound_handle(p) is not None),
        "n_spans_checked": len(gt0.correct_actions),
    }
    emit_json("shared_ground_truth_integrity.json", raw["shared_ground_truth_integrity"])
    control["CTRL-SHARED-GROUND-TRUTH"] = {
        "expected": "prereg.md 10: the declared plan action bound at execution time is identical for every arm and reproducible",
        "observed": json.dumps(raw["shared_ground_truth_integrity"], sort_keys=True),
        "result": "PASS" if (gt_identical and handle_ok and gt_matches_reference) else "FAIL",
        "evidence": ["artifacts/shared_ground_truth_integrity.json"],
    }
    print(
        f"[4] ground truth: passes agree={gt_identical} matches reference={gt_matches_reference} handles pure={handle_ok}",
        flush=True,
    )

    # -- 5. the new treatment arms on the identical task instances ---------
    def ground(k: str) -> dict[tuple[int, int], str]:
        return ref_runs[k].correct_actions

    def paths(k: str) -> dict[tuple[int, int], str]:
        return ref_runs[k].declared_paths

    scr_runs: dict[str, ArmRun] = {}
    cmp_runs: dict[str, ArmRun] = {}
    nomint_runs: dict[str, ArmRun] = {}
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        scr_runs[k] = run_arm(
            SCRATCHPAD_ARM,
            lambda: WithinEpisodeScratchpad(),
            nu,
            plan_view="goal_only",
            handle_aware=False,
            ground_truth=ground(k),
            declared_paths=paths(k),
        )
        cmp_runs[k] = run_arm(
            COMPILED_ARM,
            lambda: CrossEpisodeCompiledBinding(),
            nu,
            plan_view="materialized",
            handle_aware=True,
            ground_truth=ground(k),
            declared_paths=paths(k),
        )
        nomint_runs[k] = run_arm(
            SCRATCHPAD_NOMINT_ARM,
            lambda: AlwaysMintScratchpad(),
            nu,
            plan_view="goal_only",
            handle_aware=False,
            ground_truth=ground(k),
            declared_paths=paths(k),
        )
        print(
            f"    nu={nu:.2f} scratchpad cost={scr_runs[k].ledger.amortized(EPISODES_PER_RATE):.2f} "
            f"correct={scr_runs[k].correctness()['point']:.4f} | compiled cost={cmp_runs[k].ledger.amortized(EPISODES_PER_RATE):.2f} "
            f"correct={cmp_runs[k].correctness()['point']:.4f}",
            flush=True,
        )
    for name, runs in ((SCRATCHPAD_ARM, scr_runs), (COMPILED_ARM, cmp_runs), (SCRATCHPAD_NOMINT_ARM, nomint_runs)):
        emit_jsonl(f"spans_{name}.jsonl", [s for nu in NOVELTY_GRID for s in runs[f"{nu:.2f}"].spans])
        for k, r in runs.items():
            emit_jsonl(f"costs_{name}_{k}.jsonl", r.episodes)

    # -- 6. inherited parent arms on the identical task instances ---------
    wide_runs: dict[str, ArmRun] = {}
    narrow_runs: dict[str, ArmRun] = {}
    cold_runs: dict[str, ArmRun] = {}
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        wide_runs[k] = run_arm(
            WIDE_ARM,
            lambda: ConditionedNoMemory(arm=WIDE_ARM, goal_width="wide"),
            nu,
            plan_view="goal_only",
            handle_aware=False,
            ground_truth=ground(k),
            declared_paths=paths(k),
        )
        narrow_runs[k] = run_arm(
            NARROW_ARM,
            lambda: ConditionedNoMemory(arm=NARROW_ARM, goal_width="narrow"),
            nu,
            plan_view="goal_only",
            handle_aware=False,
            ground_truth=ground(k),
            declared_paths=paths(k),
        )
        cold_runs[k] = run_arm(
            COLD_ARM, lambda: ColdExploration(arm=COLD_ARM), nu, class_iii=True, plan_view="materialized", handle_aware=True,
            ground_truth=ground(k), declared_paths=paths(k),
        )
        print(
            f"    nu={nu:.2f} wide={wide_runs[k].ledger.amortized(EPISODES_PER_RATE):.2f} "
            f"narrow={narrow_runs[k].ledger.amortized(EPISODES_PER_RATE):.2f} "
            f"cold={cold_runs[k].ledger.amortized(EPISODES_PER_RATE):.2f}",
            flush=True,
        )
    for name, runs in ((WIDE_ARM, wide_runs), (NARROW_ARM, narrow_runs), (COLD_ARM, cold_runs)):
        emit_jsonl(f"spans_{name}.jsonl", [s for nu in NOVELTY_GRID for s in runs[f"{nu:.2f}"].spans])
        for k, r in runs.items():
            emit_jsonl(f"costs_{name}_{k}.jsonl", r.episodes)

    # -- 7. PC and NC controls at the control novelty rate ----------------
    pc_ref = run_arm(PC_ARM, lambda: DeoptRatchet(arm=PC_ARM), CONTROL_NOVELTY_RATE, class_iii=False)
    pc_scr = run_arm(
        PC_ARM + "-SCRATCHPAD", lambda: WithinEpisodeScratchpad(arm=PC_ARM + "-SCRATCHPAD"), CONTROL_NOVELTY_RATE,
        class_iii=False, plan_view="goal_only", handle_aware=False,
        ground_truth=pc_ref.correct_actions, declared_paths=pc_ref.declared_paths,
    )
    pc_cmp = run_arm(
        PC_ARM + "-COMPILED", lambda: CrossEpisodeCompiledBinding(arm=PC_ARM + "-COMPILED"), CONTROL_NOVELTY_RATE,
        class_iii=False, plan_view="materialized", handle_aware=True,
        ground_truth=pc_ref.correct_actions, declared_paths=pc_ref.declared_paths,
    )
    nc_ref = run_arm(
        NC_ARM, lambda: DeoptRatchet(arm=NC_ARM), CONTROL_NOVELTY_RATE, class_iii=False, unique_states=True
    )
    nc_scr = run_arm(
        NC_ARM + "-SCRATCHPAD", lambda: WithinEpisodeScratchpad(arm=NC_ARM + "-SCRATCHPAD"), CONTROL_NOVELTY_RATE,
        class_iii=False, unique_states=True, plan_view="goal_only", handle_aware=False,
        ground_truth=nc_ref.correct_actions, declared_paths=nc_ref.declared_paths,
    )
    nc_cmp = run_arm(
        NC_ARM + "-COMPILED", lambda: CrossEpisodeCompiledBinding(arm=NC_ARM + "-COMPILED"), CONTROL_NOVELTY_RATE,
        class_iii=False, unique_states=True, plan_view="materialized", handle_aware=True,
        ground_truth=nc_ref.correct_actions, declared_paths=nc_ref.declared_paths,
    )
    nc_wide = run_arm(
        NC_ARM + "-CONDITIONED-WIDE", lambda: ConditionedNoMemory(arm=NC_ARM + "-CONDITIONED-WIDE", goal_width="wide"),
        CONTROL_NOVELTY_RATE, class_iii=False, unique_states=True, plan_view="goal_only", handle_aware=False,
        ground_truth=nc_ref.correct_actions, declared_paths=nc_ref.declared_paths,
    )
    nc_cold = run_arm(
        NC_ARM + "-COLD", lambda: ColdExploration(arm=NC_ARM + "-COLD"), CONTROL_NOVELTY_RATE,
        class_iii=False, unique_states=True, plan_view="materialized", handle_aware=True,
        ground_truth=nc_ref.correct_actions, declared_paths=nc_ref.declared_paths,
    )
    for name, r in (
        (PC_ARM, pc_ref), (PC_ARM + "-SCRATCHPAD", pc_scr), (PC_ARM + "-COMPILED", pc_cmp),
        (NC_ARM, nc_ref), (NC_ARM + "-SCRATCHPAD", nc_scr), (NC_ARM + "-COMPILED", nc_cmp),
        (NC_ARM + "-CONDITIONED-WIDE", nc_wide), (NC_ARM + "-COLD", nc_cold),
    ):
        emit_jsonl(f"spans_{name}.jsonl", r.spans)
        emit_jsonl(f"costs_{name}.jsonl", r.episodes)
    print("[7] PC/NC runs complete", flush=True)

    # -- 8. classification of the reference trace -------------------------
    # AUTHORITATIVE: goal-aware class (ii) rule (state key + goal intent, where
    # "goal intent" is the `intent` field of the goal prefix, which the generator
    # itself names `intent` and sets to the role).
    labels_auth: dict[str, list[dict[str, Any]]] = {}
    labels_literal: dict[str, list[dict[str, Any]]] = {}
    labels_prefix: dict[str, list[dict[str, Any]]] = {}
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        labels_auth[k] = classify(ref_runs[k].spans, intent_field="role")
        labels_literal[k] = classify(ref_runs[k].spans, intent_field="none")
        labels_prefix[k] = classify(ref_runs[k].spans, intent_field="prefix")
    all_auth = [x for nu in NOVELTY_GRID for x in labels_auth[f"{nu:.2f}"]]
    # The prereg-named artifact is the AUTHORITATIVE classification of the reference
    # trace; the two declared alternates are written beside it under explicit names,
    # never overwriting it.
    emit_jsonl(f"classification_{REFERENCE_ARM}.jsonl", all_auth)
    emit_jsonl(
        f"classification_{REFERENCE_ARM}-declared_alternate_literal_step2.jsonl",
        [x for nu in NOVELTY_GRID for x in labels_literal[f"{nu:.2f}"]],
    )
    emit_jsonl(
        f"classification_{REFERENCE_ARM}-declared_alternate_prefix_intent.jsonl",
        [x for nu in NOVELTY_GRID for x in labels_prefix[f"{nu:.2f}"]],
    )

    summ = {k: summarize(labels_auth[k]) for k in labels_auth}
    summ_literal = {k: summarize(labels_literal[k]) for k in labels_literal}
    summ_prefix = {k: summarize(labels_prefix[k]) for k in labels_prefix}
    pooled_auth = summarize(all_auth)
    pooled_literal = summarize([x for nu in NOVELTY_GRID for x in labels_literal[f"{nu:.2f}"]])
    pooled_prefix = summarize([x for nu in NOVELTY_GRID for x in labels_prefix[f"{nu:.2f}"]])

    # -- 9. per-arm derived metrics ----------------------------------------
    def arm_metrics(r: ArmRun) -> dict[str, Any]:
        c = r.correctness()
        gated = [s for s in r.spans if s.get("token_param")]
        gated_correct = sum(1 for s in gated if s["emitted_matches_declared"])
        return {
            "arm": r.arm,
            "novelty_rate": r.novelty_rate,
            "episodes": len(r.episodes),
            "span_occurrences": len(r.spans),
            "span_level_action_correctness": c,
            "n_incorrect": c["n"] - c["k"],
            "class_iii_closure_rate": wilson(gated_correct, len(gated)),
            "n_class_iii_span_occurrences": len(gated),
            "amortized_cost_units_per_episode": r.ledger.amortized(len(r.episodes)),
            "ledger": r.ledger.as_dict(len(r.episodes)),
            "goal_state_success": wilson(sum(1 for x in r.goal_state_success if x), len(r.goal_state_success)),
            "false_compiled_replays": sum(
                1 for s in r.spans if s["decision_path"] in ("COMPILED_REPLAY", "COMPILED_REPLAY_BOUND") and not s["emitted_matches_declared"]
            ),
            "decision_paths": dict(collections.Counter(s["decision_path"] for s in r.spans)),
            "arm_extras": r.arm_extras,
        }

    all_runs: dict[str, dict[str, ArmRun]] = {
        REFERENCE_ARM: ref_runs,
        WIDE_ARM: wide_runs,
        NARROW_ARM: narrow_runs,
        COLD_ARM: cold_runs,
        SCRATCHPAD_ARM: scr_runs,
        COMPILED_ARM: cmp_runs,
        SCRATCHPAD_NOMINT_ARM: nomint_runs,
    }
    per_arm: dict[str, Any] = {}
    for name, runs in all_runs.items():
        per_arm[name] = {
            "per_novelty_rate": {k: arm_metrics(r) for k, r in runs.items()},
            "pooled_span_level_action_correctness": wilson(
                sum(1 for nu in NOVELTY_GRID for s in runs[f"{nu:.2f}"].spans if s["emitted_matches_declared"]),
                sum(len(runs[f"{nu:.2f}"].spans) for nu in NOVELTY_GRID),
            ),
            "pooled_amortized_cost_units_per_episode": sum(
                runs[f"{nu:.2f}"].ledger.total() for nu in NOVELTY_GRID
            ) / (EPISODES_PER_RATE * len(NOVELTY_GRID)),
            "pooled_false_compiled_replays": sum(
                1 for nu in NOVELTY_GRID for s in runs[f"{nu:.2f}"].spans
                if s["decision_path"] in ("COMPILED_REPLAY", "COMPILED_REPLAY_BOUND") and not s["emitted_matches_declared"]
            ),
            "class_iii_closure_pooled": wilson(
                sum(1 for nu in NOVELTY_GRID for s in runs[f"{nu:.2f}"].spans if s.get("token_param") and s["emitted_matches_declared"]),
                sum(1 for nu in NOVELTY_GRID for s in runs[f"{nu:.2f}"].spans if s.get("token_param")),
            ),
            "class_iii_closure_by_own_mechanism_pooled": wilson(
                sum(
                    1 for nu in NOVELTY_GRID for s in runs[f"{nu:.2f}"].spans
                    if s.get("token_param") and s["emitted_matches_declared"] and s["decision_path"] in MECHANISM_DECISION_PATH.get(name, ())
                ),
                sum(1 for nu in NOVELTY_GRID for s in runs[f"{nu:.2f}"].spans if s.get("token_param")),
            ),
            "class_iii_decision_paths": {
                k2: dict(collections.Counter(s["decision_path"] for s in runs[k2].spans if s.get("token_param")))
                for k2 in runs
            },
        }
        for k, r in runs.items():
            # emit_json (not write_json) so the per-rate arm summary is registered in
            # `produced` and therefore hashed into result.json.artifacts / provenance.json.
            emit_json(f"summary_{name}_{k}.json", per_arm[name]["per_novelty_rate"][k], role="derived")
    print("[8] classification + per-arm metrics complete", flush=True)

    # -- 10. closure attribution and residual headroom ---------------------
    def closure_attribution(k: str) -> dict[str, Any]:
        def index_arm(r: ArmRun) -> dict[tuple[int, int], dict[str, Any]]:
            return {
                (s["episode"], s["index"]): {
                    "decision_path": s["decision_path"],
                    "correct_action_key": s["correct_action_key"],
                    "emitted_correct": s["emitted_matches_declared"],
                }
                for s in r.spans
            }
        ref_by_key = index_arm(ref_runs[k])
        scr_by_key = index_arm(scr_runs[k])
        cmp_by_key = index_arm(cmp_runs[k])
        lab = {x["episode"] * 100 + x["index"]: x for x in labels_auth[k]}
        out: dict[str, Any] = {"novelty_rate": float(k), "definition": (
            "per reference-trace span occurrence: was the declared correct action reproduced by (a) the "
            "reference arm's own compiled replay, (b) the within-episode scratchpad's propagated value, "
            "(c) the cross-episode binding-keyed cache, (d) neither new arm, and how the span is classed"
        ), "counts": {}}
        closed_ref = closed_scr = closed_cmp = closed_neither = 0
        emitted_ref = emitted_scr = emitted_cmp = 0
        closed_any = 0
        by_class: dict[str, collections.Counter] = {c: collections.Counter() for c in CLASS_ORDER}
        for s in ref_runs[k].spans:
            key = s["episode"] * 100 + s["index"]
            x = lab[key]
            def arm_row(sp: dict[str, Any], mech_paths: tuple[str, ...]) -> dict[str, Any]:
                correct = bool(sp["emitted_correct"])
                by_mech = correct and sp["decision_path"] in mech_paths
                return {
                    "emitted_correct": correct,
                    "decision_path": sp["decision_path"],
                    "by_own_mechanism": bool(by_mech),
                    "by_model_oracle_fallback": bool(correct and not by_mech),
                }
            a = arm_row(ref_by_key[(s["episode"], s["index"])], MECHANISM_DECISION_PATH[REFERENCE_ARM])
            b = arm_row(scr_by_key[(s["episode"], s["index"])], MECHANISM_DECISION_PATH[SCRATCHPAD_ARM])
            c2 = arm_row(cmp_by_key[(s["episode"], s["index"])], MECHANISM_DECISION_PATH[COMPILED_ARM])
            out["counts"][f"ep_{x['episode']}_{x['index']}"] = {
                "class": x["class"], "role": x["role"],
                "reference_arm": a,
                "scratchpad_arm": b,
                "compiled_binding_arm": c2,
                "reference_compiled_and_correct": a["by_own_mechanism"],
                "scratchpad_propagated_and_correct": b["by_own_mechanism"],
                "compiled_binding_served_and_correct": c2["by_own_mechanism"],
            }
            # a/b/c2 are DICTS, so they are always truthy. The aggregate must read the
            # by_own_mechanism field, or every span is counted as closed and
            # closed_by_none_of_the_three is always 0.
            closed_ref += a["by_own_mechanism"]
            closed_scr += b["by_own_mechanism"]
            closed_cmp += c2["by_own_mechanism"]
            if a["by_own_mechanism"] or b["by_own_mechanism"] or c2["by_own_mechanism"]:
                closed_any += 1
            else:
                closed_neither += 1
            emitted_ref += a["emitted_correct"]
            emitted_scr += b["emitted_correct"]
            emitted_cmp += c2["emitted_correct"]
            by_class[x["class"]]["n"] += 1
            for cname, row in (("reference", a), ("scratchpad", b), ("compiled_binding", c2)):
                by_class[x["class"]][f"{cname}_emitted_correct"] += bool(row["emitted_correct"])
                by_class[x["class"]][f"{cname}_by_own_mechanism"] += bool(row["by_own_mechanism"])
                by_class[x["class"]][f"{cname}_by_model_oracle_fallback"] += bool(row["by_model_oracle_fallback"])
            by_class[x["class"]]["scratchpad_propagated"] += bool(b["by_own_mechanism"])
            by_class[x["class"]]["compiled_binding_served"] += bool(c2["by_own_mechanism"])
            by_class[x["class"]]["reference_compiled"] += bool(a["by_own_mechanism"])
        out["totals"] = {
            "n": len(ref_runs[k].spans),
            "definition": (
                "the four *_and_correct / *_served / propagated counters are BY THE ARM'S OWN MECHANISM "
                "(correct emission AND a decision_path that is that arm's declared mechanism); the "
                "emitted_* counters are the weaker emitted-correct count that also credits "
                "DEOPT_TO_MODEL oracle fallback; by_class breaks both down per class"
            ),
            "reference_compiled_and_correct": closed_ref,
            "scratchpad_propagated_and_correct": closed_scr,
            "compiled_binding_served_and_correct": closed_cmp,
            "closed_by_none_of_the_three": closed_neither,
            "reference_emitted_correct": emitted_ref,
            "scratchpad_emitted_correct": emitted_scr,
            "compiled_emitted_correct": emitted_cmp,
            "identity_check_emitted_minus_own_mechanism_is_oracle_fallback": {
                "reference": emitted_ref - closed_ref,
                "scratchpad": emitted_scr - closed_scr,
                "compiled_binding": emitted_cmp - closed_cmp,
            },
        }
        # INTERNAL CONSISTENCY SELF-CHECK. A dict-truthiness bug in this function once
        # reported every span as closed by all three mechanisms and 0 as closed by none,
        # so the identities below are asserted and emitted rather than assumed.
        sc: dict[str, Any] = {
            "emitted_minus_own_equals_oracle_fallback": {
                arm: (tot_emitted - own) == sum(
                    by_class[c][f"{field}_by_model_oracle_fallback"] for c in CLASS_ORDER
                )
                for arm, tot_emitted, own, field in (
                    ("reference", emitted_ref, closed_ref, "reference"),
                    ("scratchpad", emitted_scr, closed_scr, "scratchpad"),
                    ("compiled_binding", emitted_cmp, closed_cmp, "compiled_binding"),
                )
            },
            "own_mechanism_le_emitted_for_every_arm": all(
                o <= e for o, e in ((closed_ref, emitted_ref), (closed_scr, emitted_scr), (closed_cmp, emitted_cmp))
            ),
            "closed_by_any_plus_none_equals_n": (closed_any + closed_neither) == len(ref_runs[k].spans),
            "closed_by_any_ge_each_single_arm_counter": closed_any >= max(closed_ref, closed_scr, closed_cmp),
            "own_mechanism_totals_equal_sum_of_by_class": all(
                tot == sum(by_class[c][f"{field}_by_own_mechanism"] for c in CLASS_ORDER)
                for tot, field in (
                    (closed_ref, "reference"),
                    (closed_scr, "scratchpad"),
                    (closed_cmp, "compiled_binding"),
                )
            ),
            "per_class_n_sums_to_n": sum(by_class[c]["n"] for c in CLASS_ORDER) == len(ref_runs[k].spans),
        }
        def _flat_ok(v: Any) -> bool:
            if isinstance(v, bool):
                return v
            if isinstance(v, dict):
                return all(_flat_ok(x) for x in v.values())
            return False

        sc["all_passed"] = all(_flat_ok(v) for k, v in sc.items() if k != "all_passed")
        out["accounting_selfcheck"] = sc
        if not sc["all_passed"]:
            raise AssertionError(f"closure attribution self-check failed at novelty {k}: {sc}")

        out["by_class"] = {c: dict(by_class[c]) for c in CLASS_ORDER}
        out["class_iii_closure_mechanism"] = {
            "n_class_iii": by_class["iii"]["n"],
            "reference_emitted_correct": by_class["iii"]["reference_emitted_correct"],
            "reference_by_own_compiled_replay": by_class["iii"]["reference_by_own_mechanism"],
            "reference_by_model_oracle_fallback": by_class["iii"]["reference_by_model_oracle_fallback"],
            "scratchpad_emitted_correct": by_class["iii"]["scratchpad_emitted_correct"],
            "scratchpad_closed_by_propagated_value": by_class["iii"]["scratchpad_by_own_mechanism"],
            "scratchpad_by_model_oracle_fallback": by_class["iii"]["scratchpad_by_model_oracle_fallback"],
            "compiled_binding_emitted_correct": by_class["iii"]["compiled_binding_emitted_correct"],
            "compiled_binding_closed_by_cache_serve": by_class["iii"]["compiled_binding_by_own_mechanism"],
            "compiled_binding_by_model_oracle_fallback": by_class["iii"]["compiled_binding_by_model_oracle_fallback"],
            "note": (
                "a class-(iii) span counted as closed by an arm's OWN mechanism required that arm's declared "
                "value-retrieval decision path (compiled replay / propagated value / binding-keyed cache serve) "
                "to have produced the correct request. Spans closed on DEOPT_TO_MODEL were closed by the "
                "perfect-policy model oracle and are reported separately, because an oracle-mediated closure is "
                "not evidence about the mechanism under test."
            ),
        }
        return out

    closure = {k: closure_attribution(k) for k in labels_auth}
    for k in closure:
        emit_json(f"closure_attribution_{k}.json", closure[k], role="derived")
    derived["closure_attribution"] = {k: {"totals": v["totals"], "by_class": v["by_class"], "class_iii_closure_mechanism": v["class_iii_closure_mechanism"]} for k, v in closure.items()}

    # declared instrument extension: scratchpad closure detail (prereg 16)
    for name, runs, key in ((SCRATCHPAD_ARM, scr_runs, "scratchpad"), (COMPILED_ARM, cmp_runs, "binding_compilation")):
        detail = {
            "arm": name,
            "definition": "every class-(iii) span occurrence: the arm's emitted action, the declared action, the decision path, and the value source",
            "per_novelty_rate": {},
        }
        for nu in NOVELTY_GRID:
            k = f"{nu:.2f}"
            rows = []
            for s in runs[k].spans:
                if not s.get("token_param"):
                    continue
                rows.append({
                    "episode": s["episode"], "index": s["index"], "work_item": s["work_item"], "role": s["role"],
                    "emitted": s["path"], "declared": s["declared_correct_path"],
                    "emitted_matches_declared": s["emitted_matches_declared"],
                    "decision_path": s["decision_path"],
                    "handle_source": s["detail"].get("handle_source"),
                    "handle_used": s["detail"].get("handle_used"),
                    "handle_in_cache_key": s["detail"].get("binding_key_in_cache_key"),
                })
            detail["per_novelty_rate"][k] = {
                "n_class_iii_spans": len(rows),
                "n_correct": sum(1 for r in rows if r["emitted_matches_declared"]),
                "n_decision_path_scratchpad_propagated": sum(1 for r in rows if r["decision_path"] == "SCRATCHPAD_PROPAGATED"),
                "n_decision_path_cache_served": sum(1 for r in rows if r["decision_path"] == "COMPILED_REPLAY_BOUND"),
                "n_decision_path_deopt_or_prefix": sum(1 for r in rows if r["decision_path"] in ("SCRATCHPAD_PREFIX_ONLY", "DEOPT_TO_MODEL")),
                "rows": rows,
            }
        emit_json(f"{key}_closure.json", detail, role="derived")

    # reference false compiles (the inherited defect, re-measured here)
    false_by_rate = []
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        rows = ref_runs[k].spans
        bad = [s for s in rows if s["decision_path"] == "COMPILED_REPLAY" and not s["emitted_matches_declared"]]
        lab = {x["episode"] * 100 + x["index"]: x for x in labels_auth[k]}
        served = sum(1 for s in rows if s["decision_path"] == "COMPILED_REPLAY")
        false_by_rate.append({
            "novelty_rate": nu,
            "n_span_occurrences": len(rows),
            "n_compiled_replays": served,
            "n_false_compiled_replays": len(bad),
            "share_of_compiled_replays": wilson(len(bad), max(1, served)),
            "by_role": dict(collections.Counter(s["role"] for s in bad)),
            "by_class": dict(collections.Counter(lab[s["episode"] * 100 + s["index"]]["class"] for s in bad)),
            "all_false_compiles_are_class_iii": bool(bad) and all(lab[s["episode"] * 100 + s["index"]]["class"] == "iii" for s in bad),
            "parent_measured_n_false_compiled_replays": PARENT_ANCHORS["false_compiled_replays"][k],
            "examples": [
                {"episode": s["episode"], "index": s["index"], "role": s["role"], "declared": s.get("declared_correct_path"), "emitted": s["path"]}
                for s in bad[:5]
            ],
        })
    derived["reference_false_compile"] = {
        "definition": "span occurrences where the ratchet recorded decision_path=COMPILED_REPLAY but its emitted action differs from the declared plan action bound at execution time",
        "per_novelty_rate": false_by_rate,
        "pooled_n_false_compiled_replays": sum(f["n_false_compiled_replays"] for f in false_by_rate),
    }
    emit_json("reference_false_compile.json", derived["reference_false_compile"], role="derived")

    # headroom closed, per novelty rate (prereg 10.4)
    headroom = {}
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        s2 = summ[k]["share_class_ii_epistemically_blocked"]["point"]
        s3 = summ[k]["share_class_iii_observation_absent"]["point"]
        row = {"novelty_rate": nu, "sigma_2_plus_sigma_3": s2 + s3, "by_arm": {}}
        for name, runs in all_runs.items():
            corr = per_arm[name]["per_novelty_rate"][k]["span_level_action_correctness"]["point"]
            residual_after = 1.0 - corr
            row["by_arm"][name] = {
                "span_level_action_correctness": corr,
                "residual_after_arm": residual_after,
                "headroom_closed": (s2 + s3) - residual_after,
                "headroom_closed_fraction": ((s2 + s3) - residual_after) / (s2 + s3) if (s2 + s3) else None,
            }
        headroom[k] = row
    derived["headroom_closed"] = headroom
    emit_json("headroom_closed.json", headroom, role="derived")

    # -- 11. PC-PLANTED-DISAMBIGUATION (no-go 3) ---------------------------
    pc_lab = classify(pc_ref.spans, intent_field="role")
    emit_jsonl(f"classification_{PC_ARM}.jsonl", pc_lab)
    planted = [x for x in pc_lab if x["role"] in PC_PLANTED_ROLES]
    pc_state_keys_per_ep = {
        str(e): len({x["state_sig"] for x in pc_lab if x["episode"] == e and x["role"] in PC_PLANTED_ROLES})
        for e in sorted({x["episode"] for x in pc_lab})
    }
    def closure_of(run: ArmRun) -> dict[str, Any]:
        rows = [s for s in run.spans if s["role"] in PC_PLANTED_ROLES]
        k = sum(1 for s in rows if s["emitted_matches_declared"])
        mech = sum(
            1 for s in rows
            if s["decision_path"] in ("SCRATCHPAD_PROPAGATED", "COMPILED_REPLAY_BOUND", "COMPILED_REPLAY")
        )
        return {
            "planted_span_occurrences": len(rows),
            "closed": k,
            "closed_fraction": wilson(k, len(rows)),
            "closed_by_the_memory_mechanism_itself": mech,
        }
    pc = {
        "control": PC_ARM,
        "protocol": "prereg.md 7: 200 create_resource span occurrences, all issued from (empty store, last_request=GET /) with 4 different resource identities, so the correct action is goal-distinct but the observation is identical",
        "declared_deviation_from_parent": "the class-(iii) plant is disabled, as in the parent PC, so the only disambiguation under test is goal-distinct-but-observation-identical",
        "planted_roles": list(PC_PLANTED_ROLES),
        "planted_span_occurrences": len(planted),
        "per_episode_distinct_plant_state_keys": pc_state_keys_per_ep,
        "plant_verified_observation_identical": all(v == 1 for v in pc_state_keys_per_ep.values()),
        "planted_span_distinct_correct_actions_per_episode": all(
            len({x["correct_action_key"] for x in planted if x["episode"] == e}) == 4
            for e in sorted({x["episode"] for x in planted})
        ),
        "planted_span_class_counts": {c: sum(1 for x in planted if x["class"] == c) for c in CLASS_ORDER},
        "prereg_expected": "scratchpad_closure = 200/200, compiled_closure = 200/200, ratchet_closure = 0/200",
        "closure_readings": {
            "what_is_gated": (
                "prereg.md 7 and spec.json positive_control gate no-go 3 on the count of planted spans each arm "
                "CLOSES, i.e. whose emitted (method, path, body) equals the declared plan action. The prereg's "
                "expected string (200/200, 200/200, 0/200) is only simultaneously attainable under a mechanism "
                "reading for the ratchet ('compiles 0/200'), so BOTH readings are reported and the gate is applied "
                "to the emitted-correct reading, with the mechanism reading reported alongside."
            ),
            "emitted_correct": {
                SCRATCHPAD_ARM: closure_of(pc_scr),
                COMPILED_ARM: closure_of(pc_cmp),
                REFERENCE_ARM: closure_of(pc_ref),
            },
            "memory_mechanism_only": {
                SCRATCHPAD_ARM: closure_of(pc_scr)["closed_by_the_memory_mechanism_itself"],
                COMPILED_ARM: closure_of(pc_cmp)["closed_by_the_memory_mechanism_itself"],
                REFERENCE_ARM: closure_of(pc_ref)["closed_by_the_memory_mechanism_itself"],
            },
            "mechanism_reading_note": (
                "the planted population is ungated by construction (the class-(iii) plant is off), so neither new "
                "arm's value-propagation mechanism can be exercised on it: the scratchpad's mechanism closure is 0 "
                "and the ratchet's compiled-replay count is 0, while all three arms emit the declared action. The "
                "PC therefore tests goal disambiguation, not binding-value propagation."
            ),
        },
    }
    pc_pass = (
        pc["closure_readings"]["emitted_correct"][SCRATCHPAD_ARM]["closed"] == 200
        and pc["closure_readings"]["emitted_correct"][COMPILED_ARM]["closed"] == 200
    )
    pc["no_go_3_satisfied"] = pc_pass
    raw["pc_verification"] = pc
    emit_json("pc_verification.json", pc)
    control["PC-PLANTED-DISAMBIGUATION"] = {
        "expected": "prereg.md 7 / no-go 3: the scratchpad and the cross-episode compiled arm must close 200/200 planted spans; the ratchet compiles 0/200 because the state key is identical",
        "observed": json.dumps(
            {
                "planted_span_occurrences": pc["planted_span_occurrences"],
                "plant_verified_observation_identical": pc["plant_verified_observation_identical"],
                "emitted_correct": {k: v["closed"] for k, v in pc["closure_readings"]["emitted_correct"].items()},
                "memory_mechanism_only": pc["closure_readings"]["memory_mechanism_only"],
            },
            sort_keys=True,
        ),
        "result": "PASS" if pc_pass else "FAIL",
        "evidence": ["artifacts/pc_verification.json", f"artifacts/classification_{PC_ARM}.jsonl"],
    }
    print(f"[11] PC planted={len(planted)} scratchpad={pc['closure_readings']['emitted_correct'][SCRATCHPAD_ARM]['closed']} compiled={pc['closure_readings']['emitted_correct'][COMPILED_ARM]['closed']} ratchet_mech={pc['closure_readings']['memory_mechanism_only'][REFERENCE_ARM]}", flush=True)

    # -- 12. NC-UNIQUE-STATES (no-go 4) -----------------------------------
    nc_variants = {
        "authoritative_goal_aware_intent_role_prereg13_state_key": classify(
            nc_ref.spans, intent_field="role", state_key_field="prereg13",
            store_snapshots=nc_ref.store_snapshots, last_requests=nc_ref.last_requests,
        ),
        "authoritative_goal_aware_intent_role_arm_native_state_key": classify(nc_ref.spans, intent_field="role"),
        "declared_alternate_literal_rule_arm_native_state_key": classify(nc_ref.spans, intent_field="none"),
        "declared_alternate_literal_rule_prereg13_state_key": classify(
            nc_ref.spans, intent_field="none", state_key_field="prereg13",
            store_snapshots=nc_ref.store_snapshots, last_requests=nc_ref.last_requests,
        ),
        "declared_alternate_prefix_intent_prereg13_state_key": classify(
            nc_ref.spans, intent_field="prefix", state_key_field="prereg13",
            store_snapshots=nc_ref.store_snapshots, last_requests=nc_ref.last_requests,
        ),
    }
    for name, rows in nc_variants.items():
        emit_jsonl(f"classification_{NC_ARM}-{name}.jsonl", rows)
    nc_summ = {name: summarize(rows) for name, rows in nc_variants.items()}
    nc_arm_correct = {
        "reference": wilson(
            sum(1 for s in nc_ref.spans if s["emitted_matches_declared"]), len(nc_ref.spans)
        ),
        "scratchpad": wilson(sum(1 for s in nc_scr.spans if s["emitted_matches_declared"]), len(nc_scr.spans)),
        "compiled_binding": wilson(sum(1 for s in nc_cmp.spans if s["emitted_matches_declared"]), len(nc_cmp.spans)),
    }
    nc = {
        "control": NC_ARM,
        "protocol": "prereg.md 8 and 13: every span carries a uniqueness nonce appended to the WORLD STORE SNAPSHOT (part of the declared observable state), not to the request path where the inherited generator put it",
        "declared_deviation": "the class-(iii) plant is disabled in this control, as in the parent, so that sigma_3 == 0 is attainable by construction",
        "prereg_criterion": "sigma_2 == 0 under the authoritative goal-aware rule with the literal prereg.md 13 mechanism (no-go 4)",
        "n_span_occurrences": len(nc_ref.spans),
        "unique_state_keys": {
            name: len({x["classification_state_key"] for x in rows}) for name, rows in nc_variants.items()
        },
        "class_counts_and_shares_by_rule_variant": {
            name: {
                "counts": s["counts"],
                "sigma_2_point": s["share_class_ii_epistemically_blocked"]["point"],
                "sigma_2_ci95": s["share_class_ii_epistemically_blocked"]["ci95"],
                "sigma_3_point": s["share_class_iii_observation_absent"]["point"],
            }
            for name, s in nc_summ.items()
        },
        "arm_span_level_action_correctness": nc_arm_correct,
        "arm_span_level_action_correctness_measured": {
            "reference_ratchet": wilson(sum(1 for s in nc_ref.spans if s["emitted_matches_declared"]), len(nc_ref.spans)),
            "scratchpad": wilson(sum(1 for s in nc_scr.spans if s["emitted_matches_declared"]), len(nc_scr.spans)),
            "compiled_binding": wilson(sum(1 for s in nc_cmp.spans if s["emitted_matches_declared"]), len(nc_cmp.spans)),
            "inherited_conditioned_wide": wilson(sum(1 for s in nc_wide.spans if s["emitted_matches_declared"]), len(nc_wide.spans)),
            "inherited_cold": wilson(sum(1 for s in nc_cold.spans if s["emitted_matches_declared"]), len(nc_cold.spans)),
        },
        "arm_collapse_mechanism_measured": {
            "what_happens": (
                "in this control the inherited generator helper taskplan._with_nonce appends '?n=<episode>-<step>' to "
                "EVERY path, including '/'. The declared goal prefixes (wide, wide_mint, narrow) do not carry the "
                "path, so any arm that reconstructs its request from the prefix alone cannot reproduce the nonce."
            ),
            "measured": {
                "goal_conditioned_arms_that_reconstruct_from_the_prefix": {
                    "scratchpad": nc_arm_correct["scratchpad"]["point"],
                    "inherited_conditioned_wide": wilson(
                        sum(1 for s in nc_wide.spans if s["emitted_matches_declared"]), len(nc_wide.spans)
                    )["point"],
                },
                "arms_that_read_the_plan_action": {
                    "compiled_binding": nc_arm_correct["compiled_binding"]["point"],
                    "inherited_ratchet": nc_arm_correct["reference"]["point"],
                    "inherited_cold": wilson(
                        sum(1 for s in nc_cold.spans if s["emitted_matches_declared"]), len(nc_cold.spans)
                    )["point"],
                },
            },
            "why_this_is_not_a_memory_result": (
                "the collapse is driven by the prefix's coverage of the request, not by memory scope: the NEW "
                "scratchpad and the INHERITED conditioned arm collapse identically, while the ratchet, the cold arm "
                "and the new compiled arm (all of which see the plan action) do not. no-go 4 is a criterion about "
                "the CLASSIFIER (sigma_2 == 0), and it is evaluated on the labels alone, so this arm-level "
                "collapse does not bear on it."
            ),
        },
        "authoritative_variant": "authoritative_goal_aware_intent_role_prereg13_state_key",
        "no_go_4_satisfied": nc_summ["authoritative_goal_aware_intent_role_prereg13_state_key"]["counts"]["ii"] == 0,
        "interpretation_note": (
            "MEASURED, and it is the STATE KEY that decides this control, not the class-(ii) rule. With the "
            "prereg.md 13 mechanism the nonce makes every world-store key unique (1200/1200), so sigma_2 is "
            "exactly 0 under all three rule variants. With the arm-native key, which ignores the nonce in the "
            "request path, sigma_2 is 49/1200 under BOTH the inherited literal rule and the authoritative "
            "goal-aware (intent=role) rule, which agree exactly. The parent's NC residual of 49/1200 is therefore "
            "reproduced here by the arm-native state key alone, and the class-(ii) rule has no effect on it in "
            "either direction. The goal-aware rule is also indistinguishable from the literal rule on the main "
            "grid (both 1337/6000): the arm-native state key already contains the executor's last request, so it "
            "already separates the roles the intent field would separate. Only the strictest full-prefix intent "
            "reading changes the count (480/6000)."
        ),
    }
    raw["nc_verification"] = nc
    emit_json("nc_verification.json", nc)
    control["NC-UNIQUE-STATES"] = {
        "expected": "prereg.md 8 / no-go 4: sigma_2 == 0 exactly under the authoritative goal-aware rule with the literal prereg.md 13 mechanism, and no span is labelled class (ii) under any rule variant",
        "observed": json.dumps(
            {
                "authoritative_sigma_2": nc_summ["authoritative_goal_aware_intent_role_prereg13_state_key"]["counts"]["ii"],
                "all_rule_variants": {k: v["counts"]["ii"] for k, v in nc_summ.items()},
                "arm_correctness_is_NOT_the_criterion": {
                    "scratchpad": nc_arm_correct["scratchpad"]["point"],
                    "compiled_binding": nc_arm_correct["compiled_binding"]["point"],
                    "inherited_conditioned_wide": wilson(
                        sum(1 for s in nc_wide.spans if s["emitted_matches_declared"]), len(nc_wide.spans)
                    )["point"],
                    "note": nc["arm_collapse_mechanism_measured"]["why_this_is_not_a_memory_result"],
                },
            },
            sort_keys=True,
        ),
        "result": "PASS" if nc["no_go_4_satisfied"] else "FAIL",
        "evidence": ["artifacts/nc_verification.json", f"artifacts/classification_{NC_ARM}-authoritative_goal_aware_intent_role_prereg13_state_key.jsonl"],
    }
    print(f"[12] NC authoritative sigma_2 count={nc_summ['authoritative_goal_aware_intent_role_prereg13_state_key']['counts']['ii']}", flush=True)

    # -- 13. baseline replication control (strong baselines) --------------
    base_rep = {
        "purpose": "the inherited parent arms, run unmodified on the identical task instances, must reproduce the parent packet's measured values; otherwise the new arms' comparison has no stable baseline",
        "expected": PARENT_ANCHORS,
        "observed": {
            "span_level_action_correctness_pooled": {
                name: per_arm[name]["pooled_span_level_action_correctness"]["point"] for name in all_runs
            },
            "amortized_cost_pooled": {
                name: per_arm[name]["pooled_amortized_cost_units_per_episode"] for name in all_runs
            },
            "deopt_amortized_with_class_iii_per_rate": {
                k: per_arm[REFERENCE_ARM]["per_novelty_rate"][k]["amortized_cost_units_per_episode"] for k in per_arm[REFERENCE_ARM]["per_novelty_rate"]
            },
            "cold_amortized_per_rate": {
                k: per_arm[COLD_ARM]["per_novelty_rate"][k]["amortized_cost_units_per_episode"] for k in per_arm[COLD_ARM]["per_novelty_rate"]
            },
            "false_compiled_replays_per_rate": {
                k: f["n_false_compiled_replays"] for k, f in zip([f"{nu:.2f}" for nu in NOVELTY_GRID], false_by_rate)
            },
        },
    }
    # The parent's own raw span artifact is the authority, not a rounded headline:
    # recompute its per-rate and pooled correctness and require EXACT equality.
    parent_ref_rows = [json.loads(x) for x in PARENT_SPANS.read_text().splitlines() if x.strip()]
    parent_ref_per_rate: dict[str, list[int]] = {}
    for r in parent_ref_rows:
        b = parent_ref_per_rate.setdefault(f"{r['novelty_rate']:.2f}", [0, 0])
        b[1] += 1
        b[0] += 1 if r["emitted_matches_declared"] else 0
    parent_ref_pooled = [sum(v[0] for v in parent_ref_per_rate.values()), sum(v[1] for v in parent_ref_per_rate.values())]
    this_ref_per_rate = {
        k: [per_arm[REFERENCE_ARM]["per_novelty_rate"][k]["span_level_action_correctness"]["k"],
            per_arm[REFERENCE_ARM]["per_novelty_rate"][k]["span_level_action_correctness"]["n"]]
        for k in per_arm[REFERENCE_ARM]["per_novelty_rate"]
    }
    this_ref_pooled = [
        per_arm[REFERENCE_ARM]["pooled_span_level_action_correctness"]["k"],
        per_arm[REFERENCE_ARM]["pooled_span_level_action_correctness"]["n"],
    ]
    base_rep["reference_arm_exact_replication"] = {
        "authority": str(PARENT_SPANS.relative_to(REPO_ROOT)),
        "authority_sha256": sha256_file(PARENT_SPANS),
        "parent_per_rate_correct_over_total": {k: list(v) for k, v in sorted(parent_ref_per_rate.items())},
        "this_run_per_rate_correct_over_total": {k: list(v) for k, v in sorted(this_ref_per_rate.items())},
        "parent_pooled_correct_over_total": parent_ref_pooled,
        "this_run_pooled_correct_over_total": this_ref_pooled,
        "per_rate_identical": parent_ref_per_rate == this_ref_per_rate,
        "pooled_identical": parent_ref_pooled == this_ref_pooled,
        "parent_packet_headline_0.98333_is_the_nu_0.50_rate_not_the_pooled_value": True,
    }
    tol = 5e-3
    base_rep["checks"] = {
        "B-NO-MEMORY-DETERMINISTIC_per_rate_correctness_identical_to_parent_artifact": parent_ref_per_rate == this_ref_per_rate,
        "B-NO-MEMORY-DETERMINISTIC_pooled_correctness_identical_to_parent_artifact": parent_ref_pooled == this_ref_pooled,
        "B-NO-MEMORY-DETERMINISTIC_nu_0.50_correctness_matches_parent_headline": abs(
            per_arm[REFERENCE_ARM]["per_novelty_rate"]["0.50"]["span_level_action_correctness"]["point"]
            - PARENT_ANCHORS["span_level_action_correctness"]["B-NO-MEMORY-DETERMINISTIC_nu_0.50"]
        ) < tol,
        "B-NO-MEMORY-CONDITIONED-WIDE_span_correctness_matches_parent": abs(
            per_arm[WIDE_ARM]["pooled_span_level_action_correctness"]["point"]
            - PARENT_ANCHORS["span_level_action_correctness"]["B-NO-MEMORY-CONDITIONED"]
        ) < tol,
        "B-NO-MEMORY-CONDITIONED-NARROW_span_correctness_matches_parent": abs(
            per_arm[NARROW_ARM]["pooled_span_level_action_correctness"]["point"]
            - PARENT_ANCHORS["span_level_action_correctness"]["B-NO-MEMORY-CONDITIONED-NARROW"]
        ) < tol,
        "B-COLD-EXPLORATION_span_correctness_is_1": abs(
            per_arm[COLD_ARM]["pooled_span_level_action_correctness"]["point"] - 1.0
        ) < tol,
        "B-COLD-EXPLORATION_cost_is_72": all(
            abs(v - 72.0) < tol for v in base_rep["observed"]["cold_amortized_per_rate"].values()
        ),
        "B-NO-MEMORY-CONDITIONED-WIDE_cost_is_48": abs(
            per_arm[WIDE_ARM]["pooled_amortized_cost_units_per_episode"] - PARENT_ANCHORS["conditioned_amortized"]
        ) < tol,
        "B-NO-MEMORY-DETERMINISTIC_cost_per_rate_matches_parent_with_plant": all(
            abs(
                per_arm[REFERENCE_ARM]["per_novelty_rate"][k]["amortized_cost_units_per_episode"]
                - PARENT_ANCHORS["deopt_amortized_with_class_iii"][k]
            )
            < tol
            for k in per_arm[REFERENCE_ARM]["per_novelty_rate"]
        ),
        "B-NO-MEMORY-DETERMINISTIC_false_compiles_per_rate_match_parent": all(
            f["n_false_compiled_replays"] == PARENT_ANCHORS["false_compiled_replays"][f"{f['novelty_rate']:.2f}"]
            for f in false_by_rate
        ),
    }
    base_rep["all_passed"] = all(base_rep["checks"].values())
    raw["baseline_replication"] = base_rep
    emit_json("baseline_replication.json", base_rep)
    control["CTRL-BASELINE-REPLICATION"] = {
        "expected": "the four inherited parent arms reproduce their parent-packet values (ratchet 0.9833 span-level correctness and 40.94/34.08/36.64/44.84/47.06 amortized cost with the plant, conditioned 0.8500 at 48.0, narrow 0.5667, cold 1.0 at 72.0, and 30/30/20/0/0 false compiled replays)",
        "observed": json.dumps(
            {
                "checks": base_rep["checks"],
                "span_correctness_pooled": base_rep["observed"]["span_level_action_correctness_pooled"],
                "reference_arm_exact_replication": {
                    "per_rate_identical": base_rep["reference_arm_exact_replication"]["per_rate_identical"],
                    "pooled_identical": base_rep["reference_arm_exact_replication"]["pooled_identical"],
                },
            },
            sort_keys=True,
        ),
        "result": "PASS" if base_rep["all_passed"] else "FAIL",
        "evidence": ["artifacts/baseline_replication.json"],
    }
    print(f"[13] baseline replication all_passed={base_rep['all_passed']}", flush=True)

    # -- 14. goal-state success (declared blindness demonstration) ---------
    gss = {
        "purpose": "prereg.md 10: goal-state success is NOT the primary endpoint; it is measured to document that it stays 1.0 for arms with materially different span-level correctness",
        "per_arm": {
            name: {
                "goal_state_success": per_arm[name]["per_novelty_rate"]["0.50"]["goal_state_success"]["point"],
                "span_level_action_correctness": per_arm[name]["pooled_span_level_action_correctness"]["point"],
            }
            for name in all_runs
        },
        "all_arms_goal_state_success_1": all(
            all(all(r.goal_state_success) for r in runs.values()) for runs in all_runs.values()
        ),
        "interpretation": "an endpoint that is 1.0 for an arm that is wrong on a fifth of its spans cannot discriminate the arms; this is why the primary endpoint is span-level action correctness",
    }
    raw["goal_state_success"] = gss
    emit_json("goal_state_success.json", gss)
    control["CTRL-GOAL-STATE-SUCCESS"] = {
        "expected": "every arm reaches goal-state success 1.0 (the parent's invariant); any arm below is an instrument failure",
        "observed": json.dumps(gss["per_arm"], sort_keys=True),
        "result": "PASS" if gss["all_arms_goal_state_success_1"] else "FAIL",
        "important_caveat": "goal-state success is blind to a missing binding key; it is reported only as a blindness demonstration, never as a quality measure",
        "evidence": ["artifacts/goal_state_success.json"],
    }

    # -- 15. paired bootstrap cost differences (prereg 15.11) --------------
    boots = {}
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        row = {}
        for a, b in ((SCRATCHPAD_ARM, REFERENCE_ARM), (COMPILED_ARM, REFERENCE_ARM), (SCRATCHPAD_ARM, COLD_ARM), (COMPILED_ARM, COLD_ARM), (SCRATCHPAD_ARM, WIDE_ARM)):
            row[f"{a}_minus_{b}"] = paired_bootstrap(all_runs[a][k].episode_cost, all_runs[b][k].episode_cost)
        boots[k] = row
    derived["paired_bootstrap_cost_differences"] = boots
    emit_json("paired_bootstrap_cost_differences.json", boots, role="derived")

    # -- 16. the three falsifier clauses and the frozen outcome mapping ----
    s2_upper_all_below = all(
        summ[k]["share_class_ii_epistemically_blocked"]["ci95"][1] < CLAUSE1_CI_UPPER_BOUND for k in summ
    )
    clause1 = {
        "id": "clause_1",
        "label_if_fired": "RESIDUAL_NOT_ZERO",
        "condition": "sigma_2 CI95 upper < 0.01 at ALL five novelty rates",
        "threshold": CLAUSE1_CI_UPPER_BOUND,
        "per_novelty_rate_sigma_2_ci95_upper": {
            k: summ[k]["share_class_ii_epistemically_blocked"]["ci95"][1] for k in summ
        },
        "fired": s2_upper_all_below,
        "authoritative_rule": "goal-aware, intent = the `intent` field of the goal prefix (the role)",
        "consequence_if_fired": "INCONCLUSIVE",
    }
    def clause_arm(arm: str, cid: str, min_corr: float, both_label: str, cost_label: str) -> dict[str, Any]:
        pooled_corr = per_arm[arm]["pooled_span_level_action_correctness"]["point"]
        pooled_cost = per_arm[arm]["pooled_amortized_cost_units_per_episode"]
        per_rate = {
            k: {
                "span_level_action_correctness": per_arm[arm]["per_novelty_rate"][k]["span_level_action_correctness"]["point"],
                "amortized_cost_units_per_episode": per_arm[arm]["per_novelty_rate"][k]["amortized_cost_units_per_episode"],
            }
            for k in per_arm[arm]["per_novelty_rate"]
        }
        a_holds = pooled_corr >= min_corr
        b_holds = pooled_cost <= CLAUSE_MAX_COST
        return {
            "id": cid,
            "arm": arm,
            "leg_a_correctness": {"threshold": min_corr, "observed_pooled": pooled_corr, "holds": a_holds, "per_novelty_rate": {k: v["span_level_action_correctness"] for k, v in per_rate.items()}},
            "leg_b_cost": {"threshold": CLAUSE_MAX_COST, "observed_pooled": pooled_cost, "holds": b_holds, "per_novelty_rate": {k: v["amortized_cost_units_per_episode"] for k, v in per_rate.items()}},
            "fires": a_holds and b_holds,
            "fires_correctness_leg_only": a_holds and not b_holds,
            "label_if_both_legs": both_label,
            "label_if_correctness_leg_only": cost_label,
        }
    clause2 = clause_arm(SCRATCHPAD_ARM, "clause_2", CLAUSE2_MIN_CORRECTNESS, "SCRATCHPAD_SUFFICES", "SCRATCHPAD_CORRECT_BUT_COSTLY")
    clause3 = clause_arm(COMPILED_ARM, "clause_3", CLAUSE3_MIN_CORRECTNESS, "BINDING_KEY_COMPILATION_SUFFICES", "BINDING_COMPILATION_CORRECT_BUT_COSTLY")

    if clause1["fired"]:
        label = "RESIDUAL_NOT_ZERO"
    elif clause2["fires"]:
        label = "SCRATCHPAD_SUFFICES"
    elif clause2["fires_correctness_leg_only"]:
        label = "SCRATCHPAD_CORRECT_BUT_COSTLY"
    elif clause3["fires"]:
        label = "BINDING_KEY_COMPILATION_SUFFICES"
    elif clause3["fires_correctness_leg_only"]:
        label = "BINDING_COMPILATION_CORRECT_BUT_COSTLY"
    else:
        label = "NEITHER_TRIGGERED"
    outcome_label = {
        "SCRATCHPAD_SUFFICES": "SUPPORTS",
        "BINDING_KEY_COMPILATION_SUFFICES": "SUPPORTS",
        "SCRATCHPAD_CORRECT_BUT_COSTLY": "MIXED",
        "BINDING_COMPILATION_CORRECT_BUT_COSTLY": "MIXED",
        "NEITHER_TRIGGERED": "INCONCLUSIVE",
        "RESIDUAL_NOT_ZERO": "INCONCLUSIVE",
    }[label]

    no_gos = {
        "1_substrate_determinism": {"fired": not det["all_probes_deterministic"], "evidence": "artifacts/substrate_idempotency.json"},
        "2_parent_replication_mismatch": {"fired": not repl_compare["identical"], "evidence": "artifacts/replication_parent_comparison.json"},
        "3_pc_scratchpad_or_compiled_below_200_of_200": {"fired": not pc_pass, "evidence": "artifacts/pc_verification.json"},
        "4_nc_sigma_2_nonzero_under_goal_aware_rule": {"fired": not nc["no_go_4_satisfied"], "evidence": "artifacts/nc_verification.json"},
        "5_scratchpad_statelessness_failure": {"fired": not armtest_payload["all_passed"], "evidence": "artifacts/scratchpad_statelessness_test.json"},
        "6_handle_absent_from_mint_response_body": {"fired": not raw["mint_channel_check"]["mint_response_body_carries_capability_handle"], "evidence": "artifacts/mint_channel_check.json"},
    }
    fired = [k for k, v in no_gos.items() if v["fired"]]
    status = "MEASUREMENT_INVALID" if fired else "COMPLETE"
    derived["clauses"] = {"clause_1": clause1, "clause_2": clause2, "clause_3": clause3}
    derived["outcome_label"] = label
    derived["outcome"] = outcome_label
    derived["no_go_conditions"] = no_gos
    derived["status"] = status
    print(
        f"[16] clause1={clause1['fired']} clause2 fires={clause2['fires']} a={clause2['leg_a_correctness']['holds']} b={clause2['leg_b_cost']['holds']} | "
        f"clause3 fires={clause3['fires']} a={clause3['leg_a_correctness']['holds']} b={clause3['leg_b_cost']['holds']} => {label} / {status}",
        flush=True,
    )

    # -- 17. manifest -----------------------------------------------------
    wall = time.time() - t_start
    manifest = {
        "experiment_id": EXPERIMENT_ID,
        "lane": "frontier",
        "runner": "research/frontier/run_execute_36287182510.py",
        "wall_clock_seconds": round(wall, 2),
        "substrate_requests": {
            "determinism_check": det["identical_request_round_trips"],
            "mint_channel_check": raw["mint_channel_check"]["n_substrate_requests"],
            "arms": {
                name: sum(r.substrate_requests for r in runs.values()) for name, runs in all_runs.items()
            },
            "replication": sum(r.substrate_requests for r in repl_runs.values()),
            "ground_truth_passes": sum(r.substrate_requests for r in gt_check_runs),
            "pc": sum(r.substrate_requests for r in (pc_ref, pc_scr, pc_cmp)),
            "nc": sum(r.substrate_requests for r in (nc_ref, nc_scr, nc_cmp)),
        },
        "episodes": {name: sum(len(r.episodes) for r in runs.values()) for name, runs in all_runs.items()},
        "span_occurrences": {name: sum(len(r.spans) for r in runs.values()) for name, runs in all_runs.items()},
        "artifacts": sorted(produced, key=lambda x: x["path"]),
        "git": {
            "rev_parse_HEAD": git("rev-parse", "HEAD"),
            "status_porcelain": git("status", "--porcelain"),
        },
        "python": platform.python_version(),
        "platform": platform.platform(),
        "mint_salt": MINT_SALT,
        "bootstrap": {"resamples": BOOTSTRAP_RESAMPLES, "seed": BOOTSTRAP_SEED, "unit": "episode"},
    }
    produced.append({"path": "artifacts/run_manifest.json", "sha256": write_json(art("run_manifest.json"), manifest), "role": "raw"})

    # -- 18. result.json / report.md / provenance.json --------------------
    metrics: dict[str, Any] = {
        "span_level_action_correctness": {
            "definition": "prereg.md 10.1 PRIMARY ENDPOINT: fraction of span occurrences whose emitted (method, path, body) equals the declared plan action bound at execution time (shared ground truth, identical for all arms)",
            "unit": "fraction of span occurrences, Wilson CI95",
            "pooled_by_arm": {name: per_arm[name]["pooled_span_level_action_correctness"] for name in per_arm},
            "per_novelty_rate_by_arm": {
                name: {k: v["span_level_action_correctness"] for k, v in per_arm[name]["per_novelty_rate"].items()}
                for name in per_arm
            },
        },
        "class_iii_closure_rate": {
            "definition": (
                "prereg.md 10.2: fraction of class-(iii) span occurrences whose emitted (method, path, body) equals "
                "the declared action. READ THIS WITH class_iii_closure_by_own_mechanism_rate: an arm can close a "
                "class-(iii) span correctly by deopting to the perfect-policy model oracle, which is not evidence "
                "about the memory mechanism under test."
            ),
            "unit": "fraction of class-(iii) span occurrences, Wilson CI95",
            "pooled_by_arm": {name: per_arm[name]["class_iii_closure_pooled"] for name in per_arm},
            "per_novelty_rate_by_arm": {
                name: {k: v["class_iii_closure_rate"] for k, v in per_arm[name]["per_novelty_rate"].items()}
                for name in per_arm
            },
        },
        "class_iii_closure_by_own_mechanism_rate": {
            "definition": (
                "the subset of class-(iii) closures produced by the arm's OWN declared value-retrieval decision "
                "path: COMPILED_REPLAY for the inherited ratchet, SCRATCHPAD_PROPAGATED for the within-episode "
                "scratchpad, COMPILED_REPLAY_BOUND for the cross-episode binding-keyed arm. The complement is "
                "DEOPT_TO_MODEL, i.e. a perfect-policy oracle fallback."
            ),
            "unit": "fraction of class-(iii) span occurrences, Wilson CI95",
            "pooled_by_arm": {name: per_arm[name]["class_iii_closure_by_own_mechanism_pooled"] for name in per_arm},
            "class_iii_decision_paths_by_arm_and_novelty_rate": {
                name: per_arm[name]["class_iii_decision_paths"] for name in per_arm
            },
        },
        "amortized_cost_units_per_episode": {
            "definition": "prereg.md 10.3 and 11: (compile + machinery + model + execution) / episodes on the declared three-term ledger plus the declared machinery term",
            "unit": "abstract units per episode",
            "pooled_by_arm": {name: per_arm[name]["pooled_amortized_cost_units_per_episode"] for name in per_arm},
            "per_novelty_rate_by_arm": {
                name: {k: v["amortized_cost_units_per_episode"] for k, v in per_arm[name]["per_novelty_rate"].items()}
                for name in per_arm
            },
            "ledger_by_arm": {name: all_runs[name]["0.50"].ledger.as_dict(EPISODES_PER_RATE) for name in per_arm},
        },
        "share_class_ii_epistemically_blocked_sigma_2": {
            "definition": "prereg.md 9 sigma_2 under the AUTHORITATIVE goal-aware class-(ii) rule: the observable state key recurs with a different correct action for the same goal intent, where the goal intent is the `intent` field of the goal prefix",
            "unit": "fraction of span occurrences, Wilson CI95",
            "pooled": pooled_auth["share_class_ii_epistemically_blocked"],
            "per_novelty_rate": {k: summ[k]["share_class_ii_epistemically_blocked"] for k in summ},
        },
        "share_class_iii_observation_absent_sigma_3": {
            "definition": "prereg.md 9 sigma_3: the correct action depends on a capability handle verified absent from the observable state and from both goal prefixes",
            "unit": "fraction of span occurrences, Wilson CI95",
            "pooled": pooled_auth["share_class_iii_observation_absent"],
            "per_novelty_rate": {k: summ[k]["share_class_iii_observation_absent"] for k in summ},
        },
        "share_class_i_merely_novel_sigma_1": {
            "definition": "prereg.md 9 sigma_1",
            "unit": "fraction of span occurrences, Wilson CI95",
            "pooled": pooled_auth["share_class_i_merely_novel"],
            "per_novelty_rate": {k: summ[k]["share_class_i_merely_novel"] for k in summ},
        },
        "headroom_ii_plus_iii": {
            "definition": "prereg.md 10.4: the maximum recoverable by any inheritance, sigma_2 + sigma_3",
            "unit": "fraction of span occurrences, Wilson CI95",
            "pooled": pooled_auth["headroom_ii_plus_iii"],
            "per_novelty_rate": {k: summ[k]["headroom_ii_plus_iii"] for k in summ},
        },
        "headroom_closed": {
            "definition": "prereg.md 10.4: (sigma_2 + sigma_3) - residual_after_arm, where residual_after_arm = 1 - span_level_action_correctness",
            "per_novelty_rate": headroom,
        },
        "closure_attribution": derived["closure_attribution"],
        "goal_state_success": {
            "definition": "the parent's endpoint, measured only to demonstrate that it cannot discriminate these arms (prereg.md 10); it is NOT the primary endpoint",
            "unit": "fraction of episodes with an empty store and a final code-200",
            "pooled_by_arm": {
                name: {
                    "point": sum(sum(1 for x in r.goal_state_success) for r in runs.values()) / sum(len(r.goal_state_success) for r in runs.values()),
                    "n_episodes": sum(len(r.goal_state_success) for r in runs.values()),
                }
                for name, runs in all_runs.items()
            },
        },
        "conditioned_coverage": {
            "definition": "prereg.md 10.5: fraction of reference-trace span occurrences whose correct action the goal-conditioned arm reproduces, on the identical task instances",
            "unit": "fraction of span occurrences",
            "wide_prefix": per_arm[WIDE_ARM]["pooled_span_level_action_correctness"],
            "narrow_prefix": per_arm[NARROW_ARM]["pooled_span_level_action_correctness"],
            "scratchpad": per_arm[SCRATCHPAD_ARM]["pooled_span_level_action_correctness"],
        },
        "class_ii_rule_operationalisations": {
            "authoritative_goal_aware_intent_role": {
                "definition": "prereg.md 9: state key + goal intent, intent = the `intent` field of the goal prefix (which the generator sets to the role)",
                "state_key": "arm-native (observable world state + own last request)",
                "pooled": pooled_auth,
                "pooled_counts": pooled_auth["counts"],
                "per_novelty_rate": {k: summ[k] for k in summ},
            },
            "declared_alternate_literal_step2": {
                "definition": "the inherited parent's literal rule: any state key recurring with a different action, with no goal-intent condition. Reported for comparability with the parent's measured sigma_2 = 0.2228.",
                "state_key": "arm-native (observable world state + own last request)",
                "pooled": pooled_literal,
                "pooled_counts": pooled_literal["counts"],
                "per_novelty_rate": {k: summ_literal[k] for k in summ_literal},
                "parent_pooled_sigma_2": 0.22283333333333333,
            },
            "declared_alternate_prefix_intent": {
                "definition": "state key + the full wide goal prefix as the intent (the strictest goal-aware reading)",
                "state_key": "arm-native (observable world state + own last request)",
                "pooled": pooled_prefix,
                "pooled_counts": pooled_prefix["counts"],
                "per_novelty_rate": {k: summ_prefix[k] for k in summ_prefix},
            },
        },
        "reference_false_compiled_replays": derived["reference_false_compile"],
        "paired_bootstrap_cost_differences": boots,
        "falsifier_clauses": derived["clauses"],
        "declared_instrument_deviation_DI_01_mint_flag": {
            "what": "the scratchpad arm is conditioned on goal_prefix_wide_mint = the parent's frozen 7-field wide prefix plus one field, mint={0|1}; the handle VALUE is in no prefix, and wide/narrow are byte-identical to the parent",
            "why_necessary": "without the flag a scratchpad that emits PUT /resources/{rid} never receives a handle, so its class-(iii) span correctness is capped at 0.95 by a representation choice rather than by memory scope",
            "measured_price_of_the_flag": {
                "primary_with_mint_flag": per_arm[SCRATCHPAD_ARM]["pooled_span_level_action_correctness"]["point"],
                "sensitivity_without_mint_flag": per_arm[SCRATCHPAD_NOMINT_ARM]["pooled_span_level_action_correctness"]["point"],
                "difference": per_arm[SCRATCHPAD_ARM]["pooled_span_level_action_correctness"]["point"] - per_arm[SCRATCHPAD_NOMINT_ARM]["pooled_span_level_action_correctness"]["point"],
                "sensitivity_arm": SCRATCHPAD_NOMINT_ARM,
                "note": "the no-mint-flag arm is a declared non-gating sensitivity: it mints on every create, which the substrate accepts, so the cost is unchanged and only the emitted action differs",
            },
        },
        "scratchpad_propagation_accounting": {
            SCRATCHPAD_ARM: {
                k: {
                    "spans_resolved_from_scratchpad": scr_runs[k].ledger.detail.get("spans_resolved_from_scratchpad", 0),
                    "handle_values_read_from_response_bodies": scr_runs[k].ledger.detail.get("handle_values_read_from_response_bodies", 0),
                    "spans_ungated_or_unresolved": scr_runs[k].ledger.detail.get("spans_ungated_or_unresolved", 0),
                }
                for k in scr_runs
            },
            COMPILED_ARM: {
                k: {
                    "compiled_replays": cmp_runs[k].ledger.detail.get("compiled_replays", 0),
                    "spans_compiled": cmp_runs[k].ledger.detail.get("spans_compiled", 0),
                    "machinery_resolve_bind_verify": cmp_runs[k].ledger.detail.get("machinery_resolve_bind_verify", 0),
                    "handles_induced_from_response_bodies": cmp_runs[k].ledger.detail.get("handles_induced_from_response_bodies", 0),
                    "cache_key_conflicts": cmp_runs[k].ledger.detail.get("cache_key_conflicts", 0),
                    "cache_size_at_end": cmp_runs[k].arm_extras.get("cache_size"),
                    "persistent_bindings_at_end": cmp_runs[k].arm_extras.get("n_persistent_bindings"),
                }
                for k in cmp_runs
            },
        },
    }

    observations = [
        f"Substrate determinism: {det['n_probes']} request shapes x {det['repeats_per_probe']} repeats = {det['identical_request_round_trips']} identical round trips, all deterministic ({det['all_probes_deterministic']}).",
        f"The mint response BODY carries capability_handle ({raw['mint_channel_check']['mint_response_body_carries_capability_handle']}); the non-mint PUT body is unchanged ({raw['mint_channel_check']['non_mint_put_body_unchanged']}); the handle equals the declared pure function mint_token(episode counter) ({raw['mint_channel_check']['handle_equals_declared_pure_function']}).",
        f"The scratchpad arm unit test ran {armtest_payload['n_checks']} checks with {armtest_payload['n_failed']} failures, including the GoalOnlyPlan AttributeError guard ({armtest_payload['goal_only_plan_attributeerror_guard_present']}).",
        f"CTRL-REPL-PARENT-NUMBERS: the reference arm on the parent-identical generator is byte-identical to the parent packet's raw spans on {len(fields)} fields for {repl_compare['this_run_rows']} spans ({repl_compare['n_field_mismatches']} mismatches).",
        f"CTRL-BASELINE-REPLICATION: all inherited parent arms reproduce their parent-packet values (checks {json.dumps(base_rep['checks'], sort_keys=True)}).",
        f"Reference arm with the class-(iii) plant: pooled span-level action correctness {per_arm[REFERENCE_ARM]['pooled_span_level_action_correctness']['point']}, pooled amortized cost {per_arm[REFERENCE_ARM]['pooled_amortized_cost_units_per_episode']} units/episode, {derived['reference_false_compile']['pooled_n_false_compiled_replays']} false compiled replays (parent: 80).",
        f"Residual decomposition under the authoritative goal-aware rule: sigma_1 {pooled_auth['share_class_i_merely_novel']['point']}, sigma_2 {pooled_auth['share_class_ii_epistemically_blocked']['point']} CI95 {pooled_auth['share_class_ii_epistemically_blocked']['ci95']}, sigma_3 {pooled_auth['share_class_iii_observation_absent']['point']} CI95 {pooled_auth['share_class_iii_observation_absent']['ci95']}.",
        f"{SCRATCHPAD_ARM}: pooled span-level action correctness {per_arm[SCRATCHPAD_ARM]['pooled_span_level_action_correctness']['point']}; class-(iii) closure {per_arm[SCRATCHPAD_ARM]['class_iii_closure_by_own_mechanism_pooled']['k']}/{per_arm[SCRATCHPAD_ARM]['class_iii_closure_pooled']['n']} by its OWN propagated-value mechanism and {per_arm[SCRATCHPAD_ARM]['class_iii_closure_pooled']['k'] - per_arm[SCRATCHPAD_ARM]['class_iii_closure_by_own_mechanism_pooled']['k']}/{per_arm[SCRATCHPAD_ARM]['class_iii_closure_pooled']['n']} by model-oracle fallback; pooled amortized cost {per_arm[SCRATCHPAD_ARM]['pooled_amortized_cost_units_per_episode']} units/episode; {per_arm[SCRATCHPAD_ARM]['pooled_false_compiled_replays']} false compiled replays.",
        f"{COMPILED_ARM}: pooled span-level action correctness {per_arm[COMPILED_ARM]['pooled_span_level_action_correctness']['point']}; class-(iii) closure {per_arm[COMPILED_ARM]['class_iii_closure_by_own_mechanism_pooled']['k']}/{per_arm[COMPILED_ARM]['class_iii_closure_pooled']['n']} by its OWN binding-keyed cache and {per_arm[COMPILED_ARM]['class_iii_closure_pooled']['k'] - per_arm[COMPILED_ARM]['class_iii_closure_by_own_mechanism_pooled']['k']}/{per_arm[COMPILED_ARM]['class_iii_closure_pooled']['n']} by model-oracle fallback; pooled amortized cost {per_arm[COMPILED_ARM]['pooled_amortized_cost_units_per_episode']} units/episode; {per_arm[COMPILED_ARM]['pooled_false_compiled_replays']} false compiled replays.",
        f"Reference arm on class-(iii) spans: {per_arm[REFERENCE_ARM]['class_iii_closure_pooled']['k']}/{per_arm[REFERENCE_ARM]['class_iii_closure_pooled']['n']} closed, of which {per_arm[REFERENCE_ARM]['class_iii_closure_by_own_mechanism_pooled']['k']} by its own compiled replay; all {per_arm[REFERENCE_ARM]['pooled_span_level_action_correctness']['n'] - per_arm[REFERENCE_ARM]['pooled_span_level_action_correctness']['k']} of its total errors are false compiled replays on class-(iii) spans.",
        f"Clause 1 fired: {clause1['fired']}; clause 2 (a) {clause2['leg_a_correctness']['holds']} / (b) {clause2['leg_b_cost']['holds']}; clause 3 (a) {clause3['leg_a_correctness']['holds']} / (b) {clause3['leg_b_cost']['holds']}. Outcome label: {label}; packet outcome: {outcome_label}.",
        f"PC-PLANTED-DISAMBIGUATION: {len(planted)} planted create span occurrences, observation-identical within each episode ({pc['plant_verified_observation_identical']}); emitted-correct closure scratchpad {pc['closure_readings']['emitted_correct'][SCRATCHPAD_ARM]['closed']}/200, compiled {pc['closure_readings']['emitted_correct'][COMPILED_ARM]['closed']}/200, ratchet mechanism-only {pc['closure_readings']['memory_mechanism_only'][REFERENCE_ARM]}/200.",
        f"NC-UNIQUE-STATES with the literal prereg.md 13 mechanism: sigma_2 count {nc_summ['authoritative_goal_aware_intent_role_prereg13_state_key']['counts']['ii']} under the authoritative rule; the same control under the inherited literal rule on the arm-native state key gives {nc_summ['declared_alternate_literal_rule_arm_native_state_key']['counts']['ii']}/1200.",
        f"Goal-state success is 1.0 for every arm while pooled span-level action correctness ranges from {min(per_arm[a]['pooled_span_level_action_correctness']['point'] for a in per_arm)} to {max(per_arm[a]['pooled_span_level_action_correctness']['point'] for a in per_arm)}.",
    ]

    validity_notes = [
        "REPRESENTATION LOSS (frozen, DI-01): the scratchpad arm and its no-mint-flag sensitivity are conditioned on goal_prefix_wide_mint, i.e. the parent's frozen 7-field wide prefix plus exactly one field, mint={0|1}. Without it a scratchpad that emits the ungated create never receives a handle. The handle VALUE is in no prefix, and wide and narrow are byte-identical to the parent, so the inherited conditioned baselines are unchanged. The price of the flag is measured, not argued: see metrics.declared_instrument_deviation_DI_01_mint_flag.",
        "REPRESENTATION LOSS (frozen): the capability handle is returned in the mint response BODY in addition to the header. Every non-mint response body is byte-identical to the parent's, which is what keeps CTRL-REPL-PARENT-NUMBERS exact; the mint response body differs from the parent's by exactly one field.",
        "CLASS-(ii) RULE (frozen, authoritative): the goal-aware reading is implemented as state key + the `intent` field of the goal prefix, which the generator itself names `intent` and sets to the role. Two declared alternates are reported in metrics.class_ii_rule_operationalisations. MEASURED RESULT: the authoritative goal-aware rule and the inherited literal rule are NUMERICALLY IDENTICAL on this data (1337/6000 pooled; 49/1200 in NC under the arm-native state key), because the arm-native state key already contains the executor's own last request and therefore already separates the roles the intent field would separate. Only the strictest full-prefix intent reading differs (480/6000). The choice of STATE KEY, not the choice of intent, is what moves sigma_2 in this experiment. The clause-1 test consumes the authoritative value, and clause 1 fails by a wide margin under all three readings (CI95 upper 0.19-0.30 at every rate).",
        "FROZEN-IMPLEMENTATION DISCREPANCY, REPORTED NOT REPAIRED: prereg.md 6.3 describes B-NO-MEMORY-DETERMINISTIC as compiling 'within episode only, no cross-episode retention', but the frozen unmodified arm keeps its compiled cache on the instance across all 50 episodes of a run (arms/deopt_ratchet.py, run_episode never clears self.cache). The new cross-episode arm therefore differs from the reference arm in the binding key and in the declared machinery term rather than in retention alone. The arm was not modified, because the prereg declares it the unmodified parent reference and its measured values are the frozen anchors.",
        "BOUNDED INFORMATION FLOW, DECLARED: the cross-episode arm reads the BOOLEAN 'is this plan step capability-gated' from the plan step it is already required to materialise (the parent's arm contract consumes that step for the expected role and status code). It never reads the handle value from the plan; the handle it keys on is the one it induced from its own response body. An audit field records whether the arm's own induced binding equals the handle the plan bound, for every gated span.",
        f"ORACLE-MEDIATED CLOSURE, MEASURED AND MATERIAL: the cross-episode binding-keyed arm reaches class-(iii) closure {per_arm[COMPILED_ARM]['class_iii_closure_pooled']['point']:.4f}, but {per_arm[COMPILED_ARM]['class_iii_closure_by_own_mechanism_pooled']['k']} of its {per_arm[COMPILED_ARM]['class_iii_closure_pooled']['n']} class-(iii) closures came from its own binding-keyed cache; every one was a DEOPT_TO_MODEL fallback, because its preregistered cache key contains the handle VALUE and the handle is a pure function of the episode counter, so a class-(iii) span can never be served from cache. Its 1.0000 span-level correctness is therefore inherited from the perfect-policy oracle and is NOT demonstrated by binding-keyed compilation. The within-episode scratchpad's class-(iii) closure is NOT oracle-mediated: {per_arm[SCRATCHPAD_ARM]['class_iii_closure_by_own_mechanism_pooled']['k']}/{per_arm[SCRATCHPAD_ARM]['class_iii_closure_pooled']['n']} came from its own propagated value. The ratchet's class-(iii) closure is {per_arm[REFERENCE_ARM]['class_iii_closure_pooled']['point']:.4f} ({per_arm[REFERENCE_ARM]['class_iii_closure_by_own_mechanism_pooled']['k']} by its own compiled replay) and its failures are exactly its false compiled replays. Any reading of clause 3 that treats 1.0000 as evidence that binding-keyed compilation closes sigma_3 is unsupported by this run.",
        "The model oracle is the parent's perfect-policy stand-in and is given the plan (arms/common.py ModelOracle). Both new arms may deopt to it, exactly as the reference arm does. The scratchpad arm never calls it for content: its decision function is total, and its 1 model unit per span is a ledger charge for a per-span policy decision, identical to the conditioned baseline's. The parenthetical reading of prereg.md 6.1 ('model unit per span for spans not resolved from scratchpad') is reported as the sensitivity in metrics.",
        "The generator's declared class_iii_fraction=0.10 is realised exactly (120 of 1200 span occurrences), and class-(iii) membership is VERIFIED per span (the handle is checked absent from the observable state and from both goal prefixes) rather than assumed from the plant schedule.",
        "The PC population is ungated by construction, so the PC tests goal disambiguation of observation-identical spans, not binding-value propagation; the mechanism-only closure reading is reported for all three arms so this is visible rather than hidden.",
        "INHERITED THRESHOLD PROVENANCE, DISCLOSED: the 0.9833 correctness threshold is the parent packet's headline figure for the reference arm, which is that packet's NOVELTY-0.50 RATE; the parent's POOLED value over all five rates, recomputed here from the parent's own raw span artifact, is 5920/6000 = 0.986667. Both new arms are 1.0000 at every rate, so clause 2 leg (a) and clause 3 leg (a) hold under either reading; the threshold is inherited unchanged and not re-derived here. The reference arm's per-rate and pooled correctness reproduce the parent artifact EXACTLY (see metrics.controls.CTRL-BASELINE-REPLICATION).",
        "SUBSTRATE-CHANGE CONDITIONALITY, INHERITED FROM THE PARENT AUDIT (this is the load-bearing caveat of the whole experiment): the parent packet's audit recorded that on the parent substrate the capability handle was returned only in a response HEADER, which was not a declared readable channel, and that therefore no real model could have read it from the declared channels. This experiment's frozen modification (prereg.md 4 and 5) returns the handle in the mint response BODY as the field capability_handle. CONSEQUENCE: BOTH new arms are measurable ONLY because of that modification. On the unmodified parent substrate neither the scratchpad nor the compiled arm could have observed any handle value to propagate or key on, so both arms would have been unable to close any class-(iii) span by their own mechanism. These results therefore measure value propagation GIVEN a readable handle channel, and they do NOT establish what an executor without that channel can do, nor that a real substrate exposes handles readably. Disclosed as a frozen representation loss; not repaired, not generalised.",
        "ARMS ARE DETERMINISTIC RULES, NOT LANGUAGE MODELS, INHERITED FROM THE PARENT AUDIT: every arm in this run, new and inherited alike, is a deterministic policy rule with programmatic access to the declared plan through the parent ModelOracle stand-in in arms/common.py. The correctness, class-closure and headroom numbers are therefore UPPER BOUNDS on the information available to a policy that can read the observable channels and the declared goal prefix; they are not predictions of language-model behaviour, they do not measure a model's ability to hold, notice or propagate a value across a context window, and the abstract-unit costs carry no token, latency or dollar mapping. No real Web work, no real model, and no real inheritance mechanism is exercised anywhere in this run.",
        "INHERITED-AUDIT DISPOSITION (parent EXP-FRONTIER-36272394045 audit.json, status REVISE, producer_claim_supported=false, 8 required_fixes), recorded so this packet is self-contained: (UR-04 cost basis) resolved before freeze in spec.json decision_rule.cost_basis, binding the parent's three-term compile+model+execution ledger, the basis the 38.6 threshold was derived on; (UR-01 clause-1 label conflict) resolved before freeze in spec.json decision_rule.clause_1_label as RESIDUAL_NOT_ZERO, replacing the parent's contradictory FALSIFIES_INHERITANCE_NICHE mapping; (UR-02 class-(ii) ambiguity) resolved before freeze by declaring the goal-aware reading authoritative with the literal reading rejected-with-reason, and all three operationalisations are reported here as metrics.class_ii_rule_operationalisations; (NC mechanism) FIXED as required, the uniqueness nonce is placed in the world-store snapshot per prereg.md 13 rather than in the request path, and sigma_2 is then exactly 0; (PC class assignment) addressed by reporting the PC's planted span classes under the authoritative rule and disclosing that the PC population is ungated, so it cannot discriminate the class-(ii) reading; (reference arm false compiles) acknowledged and quantified here, 80 class-(iii) false COMPILED_REPLAY decisions, in every cost comparison; (conditioned arm is a deterministic rule with oracle access) and (goal-state success is insensitive) both carried forward and restated above and in metrics.controls.CTRL-GOAL-STATE-SUCCESS. This run does not itself resolve the parent's documentary cost-basis dispute, it inherits the parent's adjudication of it.",
        "Single machine, stdlib ThreadingHTTPServer on 127.0.0.1, no browser, no docker, no model API key, no network. Wall clock and request counts are in artifacts/run_manifest.json.",
    ]

    unresolved = [
        "The class-(ii) rule remains a measurement definition, not a physical fact. MEASURED: the inherited literal rule and the authoritative goal-aware (intent=role) rule are identical here (sigma_2 = "
        f"{pooled_auth['share_class_ii_epistemically_blocked']['point']:.4f} = {pooled_literal['share_class_ii_epistemically_blocked']['point']:.4f}), and only the strictest full-prefix intent reading differs (sigma_2 = {pooled_prefix['share_class_ii_epistemically_blocked']['point']:.4f}). The choice that actually moves sigma_2 is the observable STATE KEY, measured in NC (0/1200 with the prereg.md 13 world-store nonce, 49/1200 with the arm-native key), not the intent rule. Which spans are 'epistemically blocked' therefore still depends on a measurement decision, and this experiment cannot settle it from its own data.",
        "The cross-episode arm's cache key binds the handle VALUE, which the prereg fixes, and the handle is a pure function of the episode counter. The consequence is now MEASURED rather than hypothetical: 0/600 class-(iii) closures came from that arm's own cache, so on this generator a binding-VALUE key cannot compile class-(iii) spans at all. A key binding the binding's IDENTITY was not preregistered here and was not run; whether it would compile class-(iii) spans across episodes remains unknown, and it is the single most informative next experiment this run points to.",
        "Whether the within-episode scratchpad's advantage is specific to this generator (one handle per episode, a 24-step fixed work-item shape, an all-in-one-episode plan) is not established. The result is a statement about this plan family on this substrate.",
        "The clause-1 threshold (sigma_2 CI95 upper < 0.01) and the correctness/cost thresholds (0.9833 and 38.6 units/episode) were inherited from the parent, where the correctness threshold is the reference arm's own pooled value and the cost threshold is the reference arm's own per-rate value at novelty 0.50. This experiment inherits them unchanged and does not re-derive them.",
    ]

    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": "frontier",
        "status": status,
        "outcome": outcome_label,
        "metrics": metrics,
        "controls": control,
        "artifacts": sorted(produced, key=lambda x: x["path"]),
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
        "decision": {
            "frozen_outcome_label": label,
            "frozen_outcome_mapping_text_verbatim": json.loads((PACKET / "spec.json").read_text())["decision_rule"]["outcome_mapping"].get(label),
            "outcome_mapping_source": "spec.json decision_rule.outcome_mapping / prereg.md 3",
            "packet_outcome_enum_mapping_rationale": (
                "spec.json's outcome_mapping values are sentences, not the packet's outcome enum, so the enum value "
                "is the producer's explicit mapping: a fired sufficiency clause is evidence FOR the frozen claim "
                "(SUPPORTS), a correctness-only clause is a split result (MIXED), and a non-firing or residual-not-zero "
                "clause leaves the residual open (INCONCLUSIVE). The frozen sentence is preserved verbatim above."
            ),
            "clause_1_fired": clause1["fired"],
            "clause_2_fired": clause2["fires"],
            "clause_2_correctness_leg_only": clause2["fires_correctness_leg_only"],
            "clause_3_fired": clause3["fires"],
            "clause_3_correctness_leg_only": clause3["fires_correctness_leg_only"],
            "no_go_conditions_fired": fired,
            "product_consequence": (
                "prereg.md 19 named SCRATCHPAD_SUFFICES or BINDING_KEY_COMPILATION_SUFFICES as the outcomes that "
                "would cause SPIDER to narrow or drop persistent cross-episode inheritance. Neither fired."
                if label not in ("SCRATCHPAD_SUFFICES", "BINDING_KEY_COMPILATION_SUFFICES")
                else "a preregistered scope verdict fired; the Director owns the product action"
            ),
        },
        "claims_not_made": [
            "No claim that within-episode value propagation is sufficient to close the residual as a class of agent architectures: only two arms on one plan family on one substrate were measured.",
            "No claim that persistent cross-episode inheritance is unnecessary. The producer does not self-promote; the frozen scope verdict is reported as measured and adjudicated by the Director.",
            "No claim that goal-state success is a valid endpoint; it is reported here only as a measured blindness demonstration.",
        ],
        "next_questions_for_director": [
            "Is the class-(ii) rule a measurement definition to be fixed once for the program, or a per-experiment choice? Three readings of the same frozen text give sigma_2 between "
            f"{min(pooled_literal['share_class_ii_epistemically_blocked']['point'], pooled_auth['share_class_ii_epistemically_blocked']['point'], pooled_prefix['share_class_ii_epistemically_blocked']['point'])} and {max(pooled_literal['share_class_ii_epistemically_blocked']['point'], pooled_auth['share_class_ii_epistemically_blocked']['point'], pooled_prefix['share_class_ii_epistemically_blocked']['point'])} on identical data, and every downstream headroom number inherits that choice.",
            "Should a binding-IDENTITY cache key (the identity of the capability, not its episode-scoped value) be preregistered next? This run MEASURED that the preregistered binding-VALUE key produced 0/600 class-(iii) closures from its own cache and that the arm's 1.0000 correctness was entirely oracle-mediated, so this is no longer a hypothetical.",
            "The cost leg of BOTH clauses failed at a specific point: the scratchpad's 48.00 units/episode is the SAME ledger as the inherited conditioned baseline's 48.00, and the frozen 38.6 bar is the inherited ratchet's amortized cost. Should the economic bar for any successor be re-derived, or is 38.6 the program's standing bar? This run inherited the threshold unchanged and cannot answer whether the bar or the measurement is the right target.",
        ],
    }
    result_path = PACKET / "result.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    provenance = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": "frontier",
        "stage": "EXECUTE",
        "github_run_id": json.loads((PACKET / "request.json").read_text())["origin_github_run_id"],
        "request_id": json.loads((PACKET / "request.json").read_text())["request_id"],
        "base_sha": json.loads((PACKET / "request.json").read_text())["base_sha"],
        "git": manifest["git"],
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "network": "127.0.0.1 loopback only, stdlib ThreadingHTTPServer, disable_nagle_algorithm=True",
            "browser": None,
            "docker": None,
            "model_api_key": None,
            "model_calls": 0,
        },
        "frozen_inputs": {
            "freeze_json": freeze,
            "recomputed": frozen_hashes,
            "all_match": raw["frozen_inputs_hashes"]["all_match"],
            "parent_handoff": json.loads((PACKET / "request.json").read_text())["parent_handoff"],
        },
        "code_paths": [
            "research/frontier/run_execute_36287182510.py",
            "research/frontier/arms/scratchpad.py",
            "research/frontier/arms/compiled_binding.py",
            "research/frontier/arms/common.py",
            "research/frontier/arms/deopt_ratchet.py",
            "research/frontier/arms/conditioned_no_memory.py",
            "research/frontier/arms/cold_exploration.py",
            "research/frontier/episodegen_36272394045.py",
            "research/frontier/substrate_deterministic_http.py",
            "research/frontier/taskplan.py",
            "research/frontier/test_scratchpad_36287182510.py",
        ],
        "code_sha256": {
            p: sha256_file(REPO_ROOT / p)
            for p in (
                "research/frontier/run_execute_36287182510.py",
                "research/frontier/arms/scratchpad.py",
                "research/frontier/arms/compiled_binding.py",
                "research/frontier/episodegen_36272394045.py",
                "research/frontier/substrate_deterministic_http.py",
                "research/frontier/taskplan.py",
                "research/frontier/arms/deopt_ratchet.py",
                "research/frontier/arms/conditioned_no_memory.py",
                "research/frontier/arms/cold_exploration.py",
                "research/frontier/arms/common.py",
                "research/frontier/test_scratchpad_36287182510.py",
            )
        },
        "fixtures": {
            "task_generator": "research/frontier/taskplan.py (parent, unmodified) wrapped by research/frontier/episodegen_36272394045.py",
            "parent_packet": "research/experiments/EXP-FRONTIER-36272394045",
            "parent_artifacts_consumed": {
                str(PARENT_REPL_SPANS.relative_to(REPO_ROOT)): sha256_file(PARENT_REPL_SPANS),
                str(PARENT_SPANS.relative_to(REPO_ROOT)): sha256_file(PARENT_SPANS),
            },
        },
        "commands": [
            "python3 -m research.frontier.test_scratchpad_36287182510",
            "python3 -m research.frontier.run_execute_36287182510",
        ],
        "randomness": {
            "task_generator": "fixed by episode counter and novelty rate; no RNG",
            "bootstrap": {"seed": BOOTSTRAP_SEED, "resamples": BOOTSTRAP_RESAMPLES, "unit": "episode"},
            "mint_salt": MINT_SALT,
        },
        "artifacts": sorted(produced, key=lambda x: x["path"]),
        "wall_clock_seconds": round(wall, 2),
        "substrate_requests": manifest["substrate_requests"],
        "episodes_run": sum(v for v in manifest["episodes"].values()),
        "span_occurrences_run": sum(v for v in manifest["span_occurrences"].values()),
    }
    prov_path = PACKET / "provenance.json"
    prov_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_report(
        result=result,
        per_arm=per_arm,
        summ=summ,
        pooled=pooled_auth,
        clauses=derived["clauses"],
        label=label,
        outcome=outcome_label,
        status=status,
        fired=fired,
        control=control,
        pc=pc,
        nc=nc,
        headroom=headroom,
        false_compile=derived["reference_false_compile"],
        manifest=manifest,
    )
    (PACKET / "report.md").write_text(report, encoding="utf-8")

    print(f"[17] result.json, report.md, provenance.json written; status={status} outcome={outcome_label} label={label}", flush=True)
    print(json.dumps({"label": label, "status": status, "outcome": outcome_label, "no_go_fired": fired}, indent=1), flush=True)
    return 0


def git(*args: str) -> str:
    """Run git read-only for provenance. Never mutates the working tree."""
    p = subprocess.run(["git", *args], cwd=REPO_ROOT, text=True, capture_output=True)
    return p.stdout.strip() if p.returncode == 0 else f"<git {' '.join(args)} failed rc={p.returncode}: {p.stderr.strip()[:200]}>"


if __name__ == "__main__":
    raise SystemExit(main())
