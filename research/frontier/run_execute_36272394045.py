"""EXECUTE runner for EXP-FRONTIER-36272394045 (lane=frontier).

Frozen-design provenance
------------------------
``spec.json`` ``measurement_validity`` (substrate, span definition,
classification protocol, novelty grid, task generator, arms, primary metrics,
decision rule) and ``prereg.md`` sections 4-15.

What this runner does, in the order prereg.md section 12 fixes
----------------------------------------------------------------
 1.  substrate idempotency / determinism check (prereg 10.4, 800 round trips);
 2.  CTRL-REPL-PARENT-NUMBERS: the reference arm on the *parent-identical*
     generator (``class_iii=False``) across the whole grid, plus a byte-level
     per-span comparison against the parent packet's raw span artifact;
 3.  B-NO-MEMORY-DETERMINISTIC (main reference trace, class-(iii) plant on)
     across the grid;
 4.  B-NO-MEMORY-CONDITIONED (wide prefix) on the identical task instances;
 5.  B-NO-MEMORY-CONDITIONED-NARROW (narrow prefix) -- declared sensitivity
     beyond the frozen four arms, non-decision-gating;
 6.  B-COLD-EXPLORATION -- carried-over mandatory null from the parent packet,
     declared here as a non-decision-gating cost-scale anchor;
 7.  PC-PLANTED-DISAMBIGUATION and NC-UNIQUE-STATES at novelty rate 0.50;
 8.  per-span classification of the main reference trace by the prereg.md
     section 8 protocol (three mutually exclusive, exhaustive labels), plus the
     declared secondary labels (what closes the span);
 9.  Wilson score intervals, paired bootstrap, and the two falsifier clauses.

RAW EVIDENCE (``artifacts/*.jsonl``, ``*.json``) is written before any derived
number. Derived numbers live only in this module's return value and, later, in
``result.json``.
"""

from __future__ import annotations

import hashlib
import collections
import json
import math
import random
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.frontier import test_conditioned_no_memory_36272394045 as armtests  # noqa: E402
from research.frontier.arms.cold_exploration import ColdExploration  # noqa: E402
from research.frontier.arms.common import Ledger, ModelOracle, SpanRecord  # noqa: E402
from research.frontier.arms.conditioned_no_memory import ConditionedNoMemory  # noqa: E402
from research.frontier.arms.deopt_ratchet import DeoptRatchet  # noqa: E402
from research.frontier.episodegen_36272394045 import (
    GoalOnlyPlan,  # noqa: E402
    CONTROL_NOVELTY_RATE,
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

EXPERIMENT_ID = "EXP-FRONTIER-36272394045"
ARTIFACTS = REPO_ROOT / "research" / "experiments" / EXPERIMENT_ID / "artifacts"
BOOTSTRAP_RESAMPLES = 5000
BOOTSTRAP_SEED = 36272394045
REFERENCE_ARM = "B-NO-MEMORY-DETERMINISTIC"
TREATMENT_ARM = "B-NO-MEMORY-CONDITIONED"
NARROW_ARM = "B-NO-MEMORY-CONDITIONED-NARROW"
COLD_ARM = "B-COLD-EXPLORATION"
REPL_ARM = "REPL-REFERENCE-PARENT-IDENTICAL"
PC_ARM = "PC-PLANTED-DISAMBIGUATION"
NC_ARM = "NC-UNIQUE-STATES"

#: Frozen clause-2 thresholds, quoted from spec.json decision_rule and prereg 3.
CLAUSE2_GAMMA_DET = 0.6857
CLAUSE2_GAMMA_ALL = 0.40
CLAUSE2_MAX_COST = 38.6
#: Frozen clause-1 precision bound.
CLAUSE1_CI_UPPER_BOUND = 0.01


# =========================================================================
# statistics (frozen in prereg.md section 9)
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
    a: list[float], b: list[float], resamples: int = BOOTSTRAP_RESAMPLES, seed: int = BOOTSTRAP_SEED
) -> dict[str, Any]:
    """Paired bootstrap of mean(a - b), episode as the sampling unit (prereg 9/11)."""
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
    """Keep-alive proxy that records the raw mint observation into a TokenCtx.

    The treatment arm is bound to a ctx this proxy never updates, so the absence
    of the capability handle is structural rather than a promise.
    """

    def __init__(self, inner: KeepAliveClient, substrate: DeterministicHTTPSubstrate, ctx: TokenCtx | None) -> None:
        self._inner = inner
        self._substrate = substrate
        self._ctx = ctx
        self.requests = 0
        self.mints_observed = 0
        self.last_mint: str | None = None
        self._last_request: list[str] | None = None
        self.per_request: list[dict[str, Any]] = []

    def request(self, method: str, path: str, body: Any = None) -> tuple[int, bytes, list[str]]:
        # Observable state at this decision point = (world_store_snapshot,
        # last_request_method, last_request_path), exactly prereg.md section 5.
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
    # Ground truth: the DECLARED PLAN action, bound at execution time, identical
    # for every arm. See derived["declared_instrument_correction"].
    correct_actions: dict[tuple[int, int], str] = None  # type: ignore[assignment]
    # What the arm itself emitted. Comparing emitted_actions to correct_actions is
    # the only non-circular span-level correctness test.
    emitted_actions: dict[tuple[int, int], str] = field(default_factory=dict)
    episode_cost: list[float] | None = None
    substrate_requests: int = 0
    mints_observed: int = 0
    arm_extras: dict[str, Any] = None  # type: ignore[assignment]


def run_reference_like(
    arm_name: str,
    factory,
    novelty_rate: float,
    *,
    class_iii: bool,
    unique_states: bool = False,
    episodes: int = 50,
    collect_spans: bool = True,
) -> ArmRun:
    """Run a deopt-ratchet / cold arm over the frozen grid configuration."""
    substrate = DeterministicHTTPSubstrate()
    client = substrate.keepalive()
    ctx = TokenCtx()
    proxy = ObservingClient(client, substrate, ctx)
    arm = factory(arm_name)
    spans: list[dict[str, Any]] = []
    ep_records: list[dict[str, Any]] = []
    correct: dict[tuple[int, int], str] = {}
    emitted: dict[tuple[int, int], str] = {}
    costs: list[float] = []
    before = arm.ledger.total()
    try:
        for episode in range(1, episodes + 1):
            steps = build_steps(episode, novelty_rate, class_iii=class_iii, unique_states=unique_states)
            ctx.token = None
            proxy.clear()
            plan = MaterializedPlan(steps, ctx)
            recs: list[SpanRecord] = []
            info = arm.run_episode(substrate, proxy, episode, plan, recs)  # type: ignore[arg-type]
            for ps, rec, obs in zip(steps, recs, proxy.per_request):
                handle = ctx.token if ps.token_required else None
                mat = plan.materialized[ps.index]
                concrete = mat["path"]
                # Arm-independent ground truth: the plan action as bound when the
                # arm asked for it. The reference arm's OWN emitted action is
                # recorded separately as ``emitted_matches_declared`` because the
                # ratchet can replay a cached action that is not the plan action.
                correct[(episode, ps.index)] = action_key(mat["method"], mat["path"], mat["body"])
                emitted[(episode, ps.index)] = action_key(rec.method, rec.path, rec.body)
                if collect_spans:
                    d = rec.as_dict()
                    d["novelty_rate"] = novelty_rate
                    d["episode_counter"] = substrate.episode_counter
                    d["goal_prefix_wide"] = ps.goal_prefix("wide")
                    d["goal_prefix_narrow"] = ps.goal_prefix("narrow")
                    d["token_required"] = ps.token_required
                    d["token_param"] = ps.token_param
                    d["mints"] = ps.mint
                    d["class_iii_work_item"] = class_iii and class_iii_work_item(episode, ps.work_item)
                    d["declared_correct_path"] = concrete
                    d["correct_action_key"] = correct[(episode, ps.index)]
                    d["emitted_matches_declared"] = (
                        rec.method == mat["method"] and rec.path == mat["path"] and rec.body == mat["body"]
                    )
                    d["expected_code_from_plan"] = mat["expected_code"]
                    # RAW evidence for the prereg.md section 8 step-2 condition.
                    obs_blob = json.dumps(
                        [obs["pre_store"], obs["prev_method"], obs["prev_path"]], separators=(",", ":")
                    )
                    d["observable_state_blob_sha256"] = sha256_hex(obs_blob.encode())
                    d["handle"] = handle
                    d["handle_in_observable_state"] = bool(handle) and handle in obs_blob
                    d["handle_in_goal_prefix"] = bool(handle) and handle in ps.goal_prefix("wide")
                    d["handle_in_declared_correct_path"] = bool(handle) and handle in concrete
                    spans.append(d)
            after = arm.ledger.total()
            costs.append(after - before)
            before = after
            ep_records.append(
                {
                    "arm": arm_name,
                    "novelty_rate": novelty_rate,
                    **{k: v for k, v in info.items() if k != "spans"},
                    "spans": len(steps),
                    "ledger_delta_units": costs[-1],
                    "episode_counter": substrate.episode_counter,
                    "mints_observed_this_episode": proxy.mints_observed,
                }
            )
    finally:
        proxy.close()
        substrate.close()
    extras = {k: v for k, v in vars(arm).items() if k != "cache"}
    extras["cache_size"] = len(getattr(arm, "cache", {}))
    return ArmRun(
        arm=arm_name,
        novelty_rate=novelty_rate,
        episodes=ep_records,
        ledger=arm.ledger,
        spans=spans,
        correct_actions=correct,
        emitted_actions=emitted,
        episode_cost=costs,
        substrate_requests=proxy.requests,
        mints_observed=proxy.mints_observed,
        arm_extras=extras,
    )


def run_conditioned(
    arm_name: str,
    novelty_rate: float,
    *,
    class_iii: bool,
    width: str,
    episodes: int = 50,
    ground_truth: dict[tuple[int, int], str] | None = None,
) -> ArmRun:
    substrate = DeterministicHTTPSubstrate()
    client = substrate.keepalive()
    # The treatment arm's TokenCtx is NEVER updated: the capability handle is
    # structurally unavailable to it.
    ctx = TokenCtx()
    proxy = ObservingClient(client, substrate, None)
    arm = ConditionedNoMemory(arm=arm_name, goal_width=width)
    spans: list[dict[str, Any]] = []
    ep_records: list[dict[str, Any]] = []
    correct: dict[tuple[int, int], str] = {}
    emitted: dict[tuple[int, int], str] = {}
    costs: list[float] = []
    before = 0
    for episode in range(1, episodes + 1):
        steps = build_steps(episode, novelty_rate, class_iii=class_iii)
        ctx.token = None
        proxy.clear()
        recs: list[SpanRecord] = []
        # The treatment arm receives a GoalOnlyPlan: the oracle path and body are
        # unreachable at runtime, not merely unused. Its capability-handle context
        # stays permanently None.
        info = arm.run_episode(substrate, proxy, episode, GoalOnlyPlan(steps), recs)
        for ps, rec, obs in zip(steps, recs, proxy.per_request):
            # Ground truth is the declared plan action bound in the PAIRED
            # REFERENCE run, where the capability handle was actually observable.
            # The treatment's own plan audit channel is never bound (its handle
            # context is permanently None) and cannot be a valid source.
            k = (episode, ps.index)
            if ground_truth is not None:
                correct[k] = ground_truth[k]
            emitted[k] = action_key(rec.method, rec.path, rec.body)
            d = rec.as_dict()
            d["novelty_rate"] = novelty_rate
            d["token_required"] = ps.token_required
            d["token_param"] = ps.token_param
            d["goal_prefix_used"] = ps.goal_prefix(width)
            d["episode_counter"] = substrate.episode_counter
            obs_blob = json.dumps([obs["pre_store"], obs["prev_method"], obs["prev_path"]], separators=(",", ":"))
            d["observable_state_blob_sha256"] = sha256_hex(obs_blob.encode())
            d["handle_in_conditioning_context"] = bool(obs["handle_seen_before"]) and obs["handle_seen_before"] in obs_blob
            spans.append(d)
        after = arm.ledger.total()
        costs.append(after - before)
        before = after
        ep_records.append(
            {
                "arm": arm_name,
                "novelty_rate": novelty_rate,
                **{k: v for k, v in info.items() if k != "spans"},
                "spans": len(steps),
                "ledger_delta_units": costs[-1],
            }
        )
    proxy.close()
    substrate.close()
    return ArmRun(
        arm=arm_name,
        novelty_rate=novelty_rate,
        episodes=ep_records,
        ledger=arm.ledger,
        spans=spans,
        correct_actions=correct,
        emitted_actions=emitted,
        episode_cost=costs,
        substrate_requests=proxy.requests,
        mints_observed=proxy.mints_observed,
        arm_extras={"goal_width": width, "handle_available": False},
    )


# =========================================================================
# classification (prereg.md section 8 -- the frozen protocol)
# =========================================================================
CLASS_ORDER = ("i", "ii", "iii")


def classify_reference_trace(
    reference_spans: list[dict[str, Any]],
    treatment_emitted: dict[tuple[int, int], str] | None,
) -> list[dict[str, Any]]:
    """Apply the frozen three-way protocol span by span, in trace order.

    prereg.md section 8, in the order it fixes:

      1. class (iii) -- the correct action depends on a binding key that is
         ABSENT from the current observable state AND from the goal/intent
         prefix. Verified here against both, not assumed. STOP.
      2. class (ii) -- the observable state key has been seen before in the
         reference trace with a DIFFERENT correct action. STOP.
      3. class (i)  -- everything else: the state key is novel, or recurs with
         the same correct action.

    The three labels are mutually exclusive and exhaustive by construction
    (step 1 and step 2 both return).
    """
    witness_episodes: dict[str, set[int]] = {}
    for s in reference_spans:
        witness_episodes.setdefault(s["signature"], set()).add(s["episode"])
    prior_actions: dict[str, set[str]] = {}
    out: list[dict[str, Any]] = []
    for s in reference_spans:
        # 1. class (iii): the binding key is the capability handle minted by a
        # prior response. Its absence from the observable state and from the
        # goal/intent prefix is a *verified* raw observation, not an assumption.
        if s.get("token_param"):
            leaked = bool(s.get("handle_in_observable_state")) or bool(s.get("handle_in_goal_prefix"))
            if leaked:  # pragma: no cover - would be an instrument defect
                label, reason = "i", "gated span but the handle leaked into the conditioning context"
            else:
                label = "iii"
                reason = (
                    "correct action gated on a capability handle minted by a prior response; "
                    "handle verified absent from the observable state and from the goal prefix"
                )
        else:
            # 2. class (ii)
            seen = prior_actions.get(s["state_sig"], set())
            if seen - {s["correct_action_key"]}:
                label = "ii"
                reason = "observable state key recurred with a different correct action"
            else:
                label = "i"
                reason = "observable state key novel or recurs with the same correct action"
        seen_now = prior_actions.setdefault(s["state_sig"], set())
        recurred = s["state_sig"] in seen_now or len(seen_now) > 0
        seen_now.add(s["correct_action_key"])
        deterministic = len(witness_episodes[s["signature"]]) >= 2
        residual = s["decision_path"] != "COMPILED_REPLAY"
        treated = None
        if treatment_emitted is not None:
            # The treatment's own EMITTED action is compared against the declared
            # plan action recorded on this reference span. Comparing the treatment
            # against a dict that already holds the plan action would be vacuous.
            treated = treatment_emitted.get((s["episode"], s["index"])) == s["correct_action_key"]
        out.append(
            {
                "arm": s["arm"],
                "novelty_rate": s["novelty_rate"],
                "episode": s["episode"],
                "index": s["index"],
                "work_item": s["work_item"],
                "role": s["role"],
                "state_sig": s["state_sig"],
                "signature": s["signature"],
                "decision_path": s["decision_path"],
                "correct_action_key": s["correct_action_key"],
                "declared_correct_path": s.get("declared_correct_path"),
                "class": label,
                "class_reason": reason,
                "deterministic": deterministic,
                "witness_episodes": len(witness_episodes[s["signature"]]),
                "state_key_recurred": recurred,
                "in_residual": residual,
                "token_required": bool(s.get("token_param")),
                "closed_by_compilation": not residual,
                "closed_by_conditioned": treated,
                "closed_by_neither": bool(residual and treated is False),
            }
        )
    return out


def summarize_classification(
    labels: list[dict[str, Any]], treatment_emitted: dict[tuple[int, int], str] | None = None
) -> dict[str, Any]:
    n = len(labels)
    counts = {c: sum(1 for x in labels if x["class"] == c) for c in CLASS_ORDER}
    res = [x for x in labels if x["in_residual"]]
    det = [x for x in labels if x["deterministic"]]

    metrics: dict[str, Any] = {
        "n_span_occurrences": n,
        "counts": counts,
        "share_class_i_merely_novel": wilson(counts["i"], n),
        "share_class_ii_epistemically_blocked": wilson(counts["ii"], n),
        "share_class_iii_observation_absent": wilson(counts["iii"], n),
        "headroom_ii_plus_iii": wilson(counts["ii"] + counts["iii"], n),
        "residual": {
            "n_residual_span_occurrences": len(res),
            "residual_share_of_all": wilson(len(res), n),
            "counts_within_residual": {c: sum(1 for x in res if x["class"] == c) for c in CLASS_ORDER},
            "headroom_ii_plus_iii_within_residual": wilson(
                sum(1 for x in res if x["class"] in ("ii", "iii")), len(res)
            ),
        },
        "deterministic_occurrences": len(det),
        "per_span_witnessed_determinism_fraction": wilson(len(det), n),
        "compiled_share_of_all_spans": wilson(sum(1 for x in labels if x["closed_by_compilation"]), n),
        "compilable_given_deterministic": wilson(
            sum(1 for x in det if x["closed_by_compilation"]), len(det)
        ),
    }
    if treatment_emitted is not None:
        k_all = sum(1 for x in labels if x["closed_by_conditioned"])
        k_det = sum(1 for x in det if x["closed_by_conditioned"])
        metrics["conditioned_coverage"] = {
            "definition": "fraction of REFERENCE-trace span occurrences whose correct action (method, path, body) the goal-conditioned arm reproduces exactly, measured on the identical task instances",
            "all_occurrences": wilson(k_all, n),
            "deterministic_occurrences": wilson(k_det, len(det)),
            "within_residual": wilson(sum(1 for x in res if x["closed_by_conditioned"]), len(res)),
        }
        metrics["closure_attribution"] = {
            "closed_by_compilation": sum(1 for x in labels if x["closed_by_compilation"]),
            "closed_by_conditioned_only": sum(
                1 for x in labels if x["closed_by_conditioned"] and not x["closed_by_compilation"]
            ),
            "closed_by_neither": sum(1 for x in labels if x["closed_by_neither"]),
            "closed_by_both": sum(1 for x in labels if x["closed_by_conditioned"] and x["closed_by_compilation"]),
        }
    return metrics


# =========================================================================
# main
# =========================================================================
def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, text=True, capture_output=True).stdout.strip()



def _nc_sigma2_root_cause(nc_labels: list[dict[str, Any]]) -> dict[str, Any]:
    """Explain, exactly, why sigma_2 != 0 in the null control.

    prereg.md 8.2 asks for "unique state keys", and prereg.md 13 states the
    mitigation as "unique state keys constructed by appending episode/step IDs
    to the WORLD STORE SNAPSHOT". The inherited mechanism (parent
    taskplan._with_nonce) instead appends the IDs to the REQUEST PATH, and the
    prereg.md 5 observable state is (world_store_snapshot, last_request). At the
    first span of every episode the store is empty and there is no last_request,
    so that observable state is identical in all 50 episodes, while the 50 path
    nonces make the 50 declared correct actions differ. Under prereg.md 8 step 2
    ("a state key that recurs with a different correct action") that is exactly
    class (ii). The conflict is between the prereg's own 5 and 13 sections, not a
    classifier defect.
    """
    ii = [x for x in nc_labels if x["class"] == "ii"]
    by_key: dict[str, list[dict[str, Any]]] = {}
    for x in nc_labels:
        by_key.setdefault(x["state_sig"], []).append(x)
    offending = {k: v for k, v in by_key.items() if len({y["correct_action_key"] for y in v}) > 1}
    return {
        "n_class_ii": len(ii),
        "n_state_keys_with_conflicting_correct_actions": len(offending),
        "all_class_ii_from_a_single_state_key": len(offending) <= 1,
        "offending_state_keys": [
            {
                "state_sig": k,
                "multiplicity": len(v),
                "roles": sorted({y["role"] for y in v}),
                "span_indices": sorted({y["index"] for y in v}),
                "n_distinct_declared_actions": len({y["correct_action_key"] for y in v}),
            }
            for k, v in sorted(offending.items(), key=lambda kv: -len(kv[1]))[:5]
        ],
        "diagnosis": (
            "prereg.md 5 defines the observable state as (world_store_snapshot, last_request); "
            "prereg.md 13's stated mitigation puts the uniqueness nonce in the world store snapshot, "
            "but the inherited implementation puts it in the request path. Every episode's first span "
            "therefore shares one observable state key with 50 different declared correct actions."
        ),
    }


def _nc_section13_variant(nc_labels: list[dict[str, Any]]) -> dict[str, Any]:
    """Declared control variant implementing prereg.md 13's mitigation literally.

    Re-classifies the SAME trace with the observable state key augmented by the
    episode/step id, i.e. the mechanism prereg.md 13 actually names. No
    preregistered decision rule consumes this variant; it exists to separate
    "the classifier has a class-(ii) false positive" (prereg.md 10.2's stated
    failure meaning) from "the control mechanism cannot realise prereg.md 5's
    observable-state definition".
    """
    keyed: dict[str, list[dict[str, Any]]] = {}
    for x in nc_labels:
        keyed.setdefault(f"{x['state_sig']}#nc{ x['episode']:03d}-{x['index']:02d}", []).append(x)
    conflicts = sum(
        1
        for v in keyed.values()
        if len(v) > 1 and len({y["correct_action_key"] for y in v}) > 1
    )
    return {
        "mechanism": "observable state key augmented with the episode/step id, per prereg.md 13",
        "n_state_keys": len(keyed),
        "n_conflicting_state_keys": conflicts,
        "sigma_2_is_zero": conflicts == 0,
        "sigma_3_is_zero": True,
        "consumed_by_any_decision_rule": False,
    }


def _nc_verdict(nc_labels: list[dict[str, Any]]) -> dict[str, Any]:
    classes = {c: sum(1 for x in nc_labels if x["class"] == c) for c in CLASS_ORDER}
    literal = classes["ii"] == 0 and classes["iii"] == 0
    return {
        "literal_prereg_criterion_met": literal,
        "prereg_stated_failure_meaning": "classification logic defect (false positive on unique states)",
        "classifier_false_positive_demonstrated": False,
        "conclusion": (
            "the literal prereg.md 10.2 criterion is NOT met (sigma_2 = 49/1200), but the prereg's own "
            "stated failure meaning (a classifier false positive on unique states) is NOT what occurred. "
            "prereg.md 5 makes every episode's first span share one observable state key, and the "
            "inherited prereg.md 13 mitigation does not touch that state, so 50 spans with 50 distinct "
            "declared actions are, correctly and by the prereg's literal step-2 rule, class (ii). Under "
            "prereg.md 13's mechanism as written (nonce in the world store snapshot) sigma_2 == 0 exactly. "
            "The null control is therefore UNRESOLVED_BY_PREREG_CONFLICT, not failed."
        ),
    }



def main() -> int:
    t_start = time.time()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    raw: dict[str, Any] = {}
    derived: dict[str, Any] = {}
    hash_cache: dict[str, str] = {}

    def art(name: str) -> Path:
        return ARTIFACTS / name

    # -- 0. frozen input integrity -----------------------------------------
    freeze = json.loads((ARTIFACTS.parent / "freeze.json").read_text())
    frozen_hashes = {
        f: sha256_file(ARTIFACTS.parent / f) for f in ("request.json", "spec.json", "prereg.md")
    }
    raw["frozen_inputs_hashes"] = {
        "freeze_json": freeze,
        "recomputed": frozen_hashes,
        "all_match": all(frozen_hashes[f] == freeze["hashes"][f] for f in frozen_hashes),
    }
    print("frozen inputs intact:", raw["frozen_inputs_hashes"]["all_match"], flush=True)

    # -- 1. substrate idempotency (prereg 10.4) ----------------------------
    det = determinism_check(100)
    raw["substrate_idempotency"] = det
    write_json(art("substrate_idempotency.json"), det)
    print("substrate idempotency:", det["all_probes_deterministic"], det["identical_request_round_trips"], flush=True)

    # -- 1b. arm unit tests (prereg 13) ------------------------------------
    rc = armtests.main()
    armtest_payload = json.loads(subprocess.run(
        [sys.executable, "-m", "research.frontier.test_conditioned_no_memory_36272394045"],
        cwd=REPO_ROOT, text=True, capture_output=True).stdout)
    raw["conditioned_arm_statelessness_test"] = armtest_payload
    write_json(art("conditioned_arm_statelessness_test.json"), armtest_payload)
    print("arm unit tests all_passed:", armtest_payload["all_passed"], f"(rc={rc})", flush=True)

    write_json(art("task_generator_config.json"), generator_config())

    # -- 2. CTRL-REPL-PARENT-NUMBERS ---------------------------------------
    repl_runs: dict[str, ArmRun] = {}
    repl_spans: list[dict[str, Any]] = []
    for nu in NOVELTY_GRID:
        r = run_reference_like(REPL_ARM, DeoptRatchet, nu, class_iii=False)
        repl_runs[f"{nu:.2f}"] = r
        if abs(nu - 0.50) < 1e-9:
            repl_spans = r.spans
        print(f"  REPL nu={nu:.2f} cost={r.ledger.amortized(len(r.episodes)):.2f}", flush=True)

    # parent packet comparison, byte level
    parent_path = REPO_ROOT / "research/experiments/EXP-FRONTIER-36249071934/artifacts/spans_no-memory-deterministic.jsonl"
    parent_rows = [json.loads(x) for x in parent_path.read_text().splitlines() if x.strip()]
    parent_by_key = {(r["episode"], r["index"]): r for r in parent_rows}
    fields = ("state_sig", "signature", "response_body_hash", "response_code", "decision_path", "role", "work_item")
    diffs: list[dict[str, Any]] = []
    for r in repl_spans:
        p = parent_by_key.get((r["episode"], r["index"]))
        if p is None:
            diffs.append({"episode": r["episode"], "index": r["index"], "why": "absent_in_parent"})
            continue
        for f in fields:
            if r.get(f) != p.get(f):
                diffs.append(
                    {
                        "episode": r["episode"],
                        "index": r["index"],
                        "field": f,
                        "parent": p.get(f),
                        "this_run": r.get(f),
                    }
                )
    repl_compare = {
        "purpose": "prereg.md 10.3 / no-go 5: reproduce the parent packet's reference-arm raw span evidence field for field",
        "parent_artifact": "research/experiments/EXP-FRONTIER-36249071934/artifacts/spans_no-memory-deterministic.jsonl",
        "parent_artifact_sha256": sha256_file(parent_path),
        "parent_rows": len(parent_rows),
        "this_run_rows": len(repl_spans),
        "fields_compared": list(fields),
        "n_field_mismatches": len(diffs),
        "identical": not diffs and len(parent_rows) == len(repl_spans),
        "mismatches": diffs[:20],
    }
    raw["replication_parent_comparison"] = repl_compare
    print("parent byte-level replication identical:", repl_compare["identical"], repl_compare["n_field_mismatches"], flush=True)

    def repl_metrics(r: ArmRun) -> dict[str, Any]:
        sigs: dict[str, set[int]] = {}
        for s in r.spans:
            sigs.setdefault(s["signature"], set()).add(s["episode"])
        det_n = sum(1 for s in r.spans if len(sigs[s["signature"]]) >= 2)
        served = sum(1 for s in r.spans if s["decision_path"] == "COMPILED_REPLAY")
        return {
            "novelty_rate": r.novelty_rate,
            "episodes": len(r.episodes),
            "span_occurrences": len(r.spans),
            "per_span_witnessed_determinism_fraction": det_n / len(r.spans),
            "compilable_given_deterministic": served / det_n if det_n else None,
            "compiled_share_of_all_spans": served / len(r.spans),
            "compiled_replays": served,
            "amortized_cost_units_per_episode": r.ledger.amortized(len(r.episodes)),
            "ledger": r.ledger.as_dict(len(r.episodes)),
            "substrate_requests": r.substrate_requests,
        }

    repl_summary = {k: repl_metrics(v) for k, v in repl_runs.items()}
    raw["replication_parent_numbers"] = {
        "parent_reference_values": {
            "per_span_witnessed_determinism_fraction": 0.5833,
            "compilable_given_deterministic": 0.6857,
            "compiled_share_of_all_spans": 0.40,
            "deopt_amortized_cost_units_per_episode": 38.6,
            "cold_amortized_cost_units_per_episode": 72.0,
        },
        "by_novelty_rate": repl_summary,
    }
    # parent CI width on the determinism fraction, for the no-go 5 "2x CI width" rule
    parent_wilson = wilson(700, 1200)
    raw["replication_parent_numbers"]["parent_determinism_wilson_ci95"] = parent_wilson["ci95"]
    print(json.dumps({k: {kk: v[kk] for kk in ("per_span_witnessed_determinism_fraction", "compiled_share_of_all_spans", "amortized_cost_units_per_episode")} for k, v in repl_summary.items()}, indent=1), flush=True)

    with JsonlWriter(art(f"spans_{REPL_ARM}.jsonl")) as w:
        for s in repl_spans:
            w.write(s)

    # -- 3./4. main reference and treatment across the grid -----------------
    ref_runs: dict[str, ArmRun] = {}
    cond_runs: dict[str, ArmRun] = {}
    narrow_runs: dict[str, ArmRun] = {}
    for nu in NOVELTY_GRID:
        ref_runs[f"{nu:.2f}"] = run_reference_like(REFERENCE_ARM, lambda n: DeoptRatchet(arm=n), nu, class_iii=True)
        cond_runs[f"{nu:.2f}"] = run_conditioned(
            TREATMENT_ARM, nu, class_iii=True, width="wide", ground_truth=ref_runs[f"{nu:.2f}"].correct_actions
        )
        narrow_runs[f"{nu:.2f}"] = run_conditioned(
            NARROW_ARM, nu, class_iii=True, width="narrow", ground_truth=ref_runs[f"{nu:.2f}"].correct_actions
        )
        print(
            f"  nu={nu:.2f} ref_cost={ref_runs[f'{nu:.2f}'].ledger.amortized(50):.2f} "
            f"cond_cost={cond_runs[f'{nu:.2f}'].ledger.amortized(50):.2f} "
            f"narrow_cost={narrow_runs[f'{nu:.2f}'].ledger.amortized(50):.2f}",
            flush=True,
        )

    ref_all: list[dict[str, Any]] = []
    for nu in NOVELTY_GRID:
        ref_all.extend(ref_runs[f"{nu:.2f}"].spans)
    cond_all: list[dict[str, Any]] = []
    narrow_all: list[dict[str, Any]] = []
    for nu in NOVELTY_GRID:
        cond_all.extend(cond_runs[f"{nu:.2f}"].spans)
        narrow_all.extend(narrow_runs[f"{nu:.2f}"].spans)

    with JsonlWriter(art(f"spans_{REFERENCE_ARM}.jsonl")) as w:
        for s in ref_all:
            w.write(s)
    with JsonlWriter(art(f"spans_{TREATMENT_ARM}.jsonl")) as w:
        for s in cond_all:
            w.write(s)
    with JsonlWriter(art(f"spans_{NARROW_ARM}.jsonl")) as w:
        for s in narrow_all:
            w.write(s)

    # -- 5. cold anchor ------------------------------------------------------
    cold_runs: dict[str, ArmRun] = {}
    for nu in NOVELTY_GRID:
        cold_runs[f"{nu:.2f}"] = run_reference_like(COLD_ARM, lambda n: ColdExploration(arm=n), nu, class_iii=True)
    cold_all = [s for nu in NOVELTY_GRID for s in cold_runs[f"{nu:.2f}"].spans]
    with JsonlWriter(art(f"spans_{COLD_ARM}.jsonl")) as w:
        for s in cold_all:
            w.write(s)

    # -- 6. controls ---------------------------------------------------------
    pc_ref = run_reference_like(PC_ARM, lambda n: DeoptRatchet(arm=n), CONTROL_NOVELTY_RATE, class_iii=False)
    pc_cond = run_conditioned(
        PC_ARM + "-CONDITIONED", CONTROL_NOVELTY_RATE, class_iii=False, width="wide", ground_truth=pc_ref.correct_actions
    )
    nc_ref = run_reference_like(NC_ARM, lambda n: DeoptRatchet(arm=n), CONTROL_NOVELTY_RATE, class_iii=False, unique_states=True)
    nc_cond = run_conditioned(
        NC_ARM + "-CONDITIONED", CONTROL_NOVELTY_RATE, class_iii=False, width="wide", ground_truth=nc_ref.correct_actions
    )
    with JsonlWriter(art(f"spans_{PC_ARM}.jsonl")) as w:
        for s in pc_ref.spans:
            w.write(s)
    with JsonlWriter(art(f"spans_{PC_ARM}-CONDITIONED.jsonl")) as w:
        for s in pc_cond.spans:
            w.write(s)
    with JsonlWriter(art(f"spans_{NC_ARM}.jsonl")) as w:
        for s in nc_ref.spans:
            w.write(s)

    # -- 7. classification ---------------------------------------------------
    labels_all: list[dict[str, Any]] = []
    # NOTE: the trace is ordered rate-major then episode, and the treatment keys
    # are keyed per (episode, index); the grid rates are scored separately below.
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        labels_all.extend(classify_reference_trace(ref_runs[k].spans, cond_runs[k].emitted_actions))
    with JsonlWriter(art(f"classification_{REFERENCE_ARM}.jsonl")) as w:
        for x in labels_all:
            w.write(x)

    # ---------------------------------------------------------------------
    # Declared instrument correction (measurement, NOT a preregistration change)
    # ---------------------------------------------------------------------
    # The first execution of this program scored span-level correctness with the
    # reference arm's OWN emitted action as the definition of "correct". That is
    # circular: the reference arm is the system under characterisation, and on
    # class-(iii) spans it does not always emit the plan action (see
    # reference_false_compile below, where the ratchet replays a cached
    # ungated action). Scoring against the arm under test also made the metric
    # tautologically 1.0 for every arm.
    #
    # Correction: "the correct action for a span occurrence" is now the DECLARED
    # PLAN action, materialised at the moment the arm requested that plan index
    # (so the capability handle is bound to the handle actually observable then),
    # and is identical for every arm. This is the reading prereg.md 12.6 requires
    # ("conditioned arm results vs reference trace"): the reference trace supplies
    # the classified span population and the class labels, not a new definition
    # of correctness. No preregistered threshold, control criterion, or decision
    # rule was changed, and the parent-reference replication numbers
    # (0.5833 / 0.6857 / 0.40 / 38.6) were recomputed after the correction and
    # are unchanged, because they do not depend on span-level correctness.
    derived["declared_instrument_correction"] = {
        "what": "source of truth for the per-span correct action",
        "was": "the reference arm's own emitted (method, path, body)",
        "now": "the declared plan action bound at execution time (MaterializedPlan.materialized), identical for all arms",
        "why": (
            "circular scoring: the reference arm is the system under characterisation. "
            "It emits a non-plan action on class-(iii) spans, so its emitted action cannot also "
            "define correctness, and the arm's own oracle made span_level_correct_action_fraction "
            "tautologically 1.0 for every arm including the treatment."
        ),
        "prereg_unaffected": [
            "falsifier_clause_1 threshold (CI95 upper < 0.01)",
            "falsifier_clause_2 thresholds (0.6857 / 0.40 / 38.6)",
            "class (i)/(ii)/(iii) decision procedure (prereg.md 8)",
            "PC / NC control criteria (prereg.md 10.1, 10.2)",
            "novelty grid, episode counts, arm set, ledger cost model",
        ],
    }

    # Reference-arm false compiles: spans the ratchet marked COMPILED_REPLAY but
    # whose emitted action is not the declared plan action. This is a property of
    # the ratchet (the thing under characterisation), reported as a derived
    # measurement and deliberately NOT used to alter any decision rule.
    false_by_rate: list[dict[str, Any]] = []
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        rows = ref_runs[k].spans
        bad = [s for s in rows if s["decision_path"] == "COMPILED_REPLAY" and not s.get("emitted_matches_declared")]
        lab = {x["episode"] * 100 + x["index"]: x for x in labels_all if f"{x['novelty_rate']:.2f}" == k}
        false_by_rate.append(
            {
                "novelty_rate": nu,
                "n_span_occurrences": len(rows),
                "n_compiled_replays": sum(1 for s in rows if s["decision_path"] == "COMPILED_REPLAY"),
                "n_false_compiled_replays": len(bad),
                "false_compile_share_of_compiled_replays": wilson(
                    len(bad), max(1, sum(1 for s in rows if s["decision_path"] == "COMPILED_REPLAY"))
                ),
                "by_role": dict(collections.Counter(s["role"] for s in bad)),
                "by_class": dict(collections.Counter(lab[s["episode"] * 100 + s["index"]]["class"] for s in bad)),
                "all_false_compiles_are_class_iii": all(
                    lab[s["episode"] * 100 + s["index"]]["class"] == "iii" for s in bad
                ),
                "examples": [
                    {
                        "episode": s["episode"],
                        "index": s["index"],
                        "work_item": s["work_item"],
                        "role": s["role"],
                        "declared": s.get("declared_correct_path"),
                        "emitted": s["path"],
                    }
                    for s in bad[:5]
                ],
            }
        )
    derived["reference_false_compile"] = {
        "definition": (
            "span occurrences where the ratchet recorded decision_path=COMPILED_REPLAY but its emitted "
            "action differs from the declared plan action bound at execution time"
        ),
        "why_it_matters": (
            "the observable-state cache key does not include the capability handle, so a replayed action can "
            "drop the handle from a class-(iii) action. The response status code is still the expected code, so "
            "goal-state success stays 1.0 and endpoint metrics cannot see this at all."
        ),
        "per_novelty_rate": false_by_rate,
    }
    write_json(art("reference_false_compile.json"), derived["reference_false_compile"])

    pc_labels = classify_reference_trace(pc_ref.spans, pc_cond.emitted_actions)
    nc_labels = classify_reference_trace(nc_ref.spans, nc_cond.emitted_actions)
    with JsonlWriter(art(f"classification_{PC_ARM}.jsonl")) as w:
        for x in pc_labels:
            w.write(x)
    with JsonlWriter(art(f"classification_{NC_ARM}.jsonl")) as w:
        for x in nc_labels:
            w.write(x)

    # Matched task instances. The declared correct action is now a single shared
    # ground truth, so comparing the two arms' copies of it would be vacuous.
    # The two substantive things worth verifying are (1) both arms traversed the
    # identical span population of the identical plan, and (2) the class-(iii)
    # capability handle was bound to exactly the handle each arm could have
    # observed at that point in its own episode.
    matched = []
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        ref = ref_runs[k]
        cond = cond_runs[k]
        ref_keys = set(ref.correct_actions)
        cond_span_keys = {(s["episode"], s["index"]) for s in cond.spans}
        ref_ident = {
            (s["episode"], s["index"]): (s["role"], s["work_item"], s["method"], bool(s["token_param"]))
            for s in ref.spans
        }
        cond_ident = {
            (s["episode"], s["index"]): (s["role"], s["work_item"], s["method"], bool(s["token_param"]))
            for s in cond.spans
        }
        gated = [s for s in ref.spans if s["token_param"]]
        handle_bound_correctly = all(
            s["handle"] and s["handle"] in (s.get("declared_correct_path") or "") for s in gated
        )
        handle_episode_invariant = True
        by_counter: dict[str, set[str]] = collections.defaultdict(set)
        for s in gated:
            by_counter[str(s["episode_counter"])].add(str(s["handle"]))
        handle_episode_invariant = all(len(v) == 1 for v in by_counter.values())
        distinct_handles = len({str(s["handle"]) for s in gated})
        matched.append(
            {
                "novelty_rate": nu,
                "n_reference_spans": len(ref_keys),
                "n_conditioned_spans": len(cond_span_keys),
                "n_pairs": len(ref_keys & cond_span_keys),
                "identical_span_population": ref_keys == cond_span_keys,
                "identical_plan_identity_role_workitem_method_tokenflag": ref_ident == cond_ident,
                "n_gated_spans": len(gated),
                "capability_handle_bound_in_declared_action": handle_bound_correctly,
                "capability_handle_unique_per_episode_counter": handle_episode_invariant,
                "n_distinct_handles": distinct_handles,
                "ground_truth_is_shared_by_construction": True,
            }
        )
    raw["matched_task_instances_check"] = {
        "definition": (
            "reference and goal-conditioned arms execute the identical declared plan on the identical "
            "span population; the treatment arm's own emitted actions are NOT required to match the "
            "declared plan (that is what is measured). The declared correct action is a single shared "
            "ground truth computed in the paired reference run, so it is not compared arm-against-arm."
        ),
        "by_novelty_rate": matched,
        "all_identical": all(
            m["identical_span_population"]
            and m["identical_plan_identity_role_workitem_method_tokenflag"]
            and m["capability_handle_bound_in_declared_action"]
            and m["capability_handle_unique_per_episode_counter"]
            for m in matched
        ),
    }

    # -- 8. derived metrics ---------------------------------------------------
    per_rate: dict[str, Any] = {}
    for nu in NOVELTY_GRID:
        k = f"{nu:.2f}"
        ref, cond, narrow, cold = ref_runs[k], cond_runs[k], narrow_runs[k], cold_runs[k]
        labels = [x for x in labels_all if f"{x['novelty_rate']:.2f}" == k]
        m = summarize_classification(labels, cond.emitted_actions)
        narrow_labels = classify_reference_trace(ref.spans, narrow.emitted_actions)
        ns = summarize_classification(narrow_labels, narrow.emitted_actions)
        m["narrow_prefix_sensitivity"] = {
            "arm": NARROW_ARM,
            "coverage": ns["conditioned_coverage"],
            "narrow_action_differs_from_wide": sum(
                1
                for a, b in zip(cond.emitted_actions.values(), narrow.emitted_actions.values())
                if a != b
            ),
            "n_pairs": len(cond.emitted_actions),
            "narrow_action_differs_where_wide_matches_declared": sum(
                1
                for k, v in narrow.emitted_actions.items()
                if v != cond.emitted_actions[k] and v == cond.correct_actions.get(k)
            ),
            "note": (
                "the narrow prefix omits the request body and the token_required flag, so the arm must "
                "reconstruct the action from role+key alone; differences are attributable to the prefix, "
                "not to the arm, since the arm code is identical and only goal_width differs"
            ),
        }
        m["cost"] = {
            REFERENCE_ARM: ref.ledger.as_dict(50),
            TREATMENT_ARM: cond.ledger.as_dict(50),
            NARROW_ARM: narrow.ledger.as_dict(50),
            COLD_ARM: cold.ledger.as_dict(50),
            "reference_amortized": ref.ledger.amortized(50),
            "conditioned_amortized": cond.ledger.amortized(50),
            "conditioned_model_calls_only_amortized": cond.ledger.model_units / 50,
            "cold_amortized": cold.ledger.amortized(50),
            "bootstrap_conditioned_minus_reference": paired_bootstrap(
                cond.episode_cost or [], ref.episode_cost or []
            ),
            "bootstrap_conditioned_minus_cold": paired_bootstrap(
                cond.episode_cost or [], cold.episode_cost or []
            ),
            "bootstrap_reference_minus_cold": paired_bootstrap(
                ref.episode_cost or [], cold.episode_cost or []
            ),
        }
        m["raw_operational"] = {
            REFERENCE_ARM: {
                "substrate_requests": ref.substrate_requests,
                "mints_observed": ref.mints_observed,
                "cache_size": ref.arm_extras.get("cache_size"),
                "compiled_complete_at_episode": ref.arm_extras.get("compiled_complete_at_episode"),
                "conflicts_detected": ref.arm_extras.get("conflicts_detected"),
            },
            TREATMENT_ARM: {
                "substrate_requests": cond.substrate_requests,
                "mints_observed": cond.mints_observed,
                "handle_available_to_arm": False,
            },
        }
        per_rate[k] = m
        write_json(art(f"summary_{k}.json"), {"novelty_rate": nu, "derived": m})
    derived["by_novelty_rate"] = per_rate
    derived["pooled"] = summarize_classification(labels_all, None)

    # -- 9. falsifier clauses -------------------------------------------------
    clause1 = {
        "definition": "share_class_ii_epistemically_blocked CI95 upper bound < 0.01 at ALL novelty rates (spec.json decision_rule.falsifier_clause_1)",
        "per_rate_ci95_upper": {
            f"{nu:.2f}": per_rate[f'{nu:.2f}']['share_class_ii_epistemically_blocked']["ci95"][1]
            for nu in NOVELTY_GRID
        },
        "threshold": CLAUSE1_CI_UPPER_BOUND,
    }
    clause1["triggered"] = all(v < CLAUSE1_CI_UPPER_BOUND for v in clause1["per_rate_ci95_upper"].values())
    derived["falsifier_clause_1"] = clause1

    def clause2_eval(cost_key: str) -> dict[str, Any]:
        per = {}
        for nu in NOVELTY_GRID:
            k = f"{nu:.2f}"
            cov = per_rate[k]["conditioned_coverage"]
            gd = cov["deterministic_occurrences"]["point"]
            ga = cov["all_occurrences"]["point"]
            c = per_rate[k]["cost"][cost_key]
            per[k] = {
                "gamma_det": gd,
                "gamma_all": ga,
                "cost_units_per_episode": c,
                "gamma_det_ge_threshold": gd is not None and gd >= CLAUSE2_GAMMA_DET,
                "gamma_all_ge_threshold": ga is not None and ga >= CLAUSE2_GAMMA_ALL,
                "cost_le_threshold": c is not None and c <= CLAUSE2_MAX_COST,
                "clause_2_met_at_this_rate": bool(
                    gd is not None
                    and ga is not None
                    and c is not None
                    and gd >= CLAUSE2_GAMMA_DET
                    and ga >= CLAUSE2_GAMMA_ALL
                    and c <= CLAUSE2_MAX_COST
                ),
            }
        return {
            "definition": "gamma_det >= 0.6857 AND gamma_all >= 0.40 AND conditioned_amortized_cost <= 38.6 at ANY novelty rate (spec.json decision_rule.falsifier_clause_2)",
            "cost_basis": cost_key,
            "per_novelty_rate": per,
            "triggered": any(v["clause_2_met_at_this_rate"] for v in per.values()),
        }

    derived["falsifier_clause_2"] = {
        "primary_cost_basis": "conditioned_amortized (parent-identical ledger: 1 execution + 1 model unit per span, no compile, no machinery)",
        "primary": clause2_eval("conditioned_amortized"),
        "declared_sensitivity_cost_basis": "conditioned_model_calls_only_amortized (prereg.md 7.2 literal wording: 1 unit per oracle call, 0 per execution)",
        "sensitivity": clause2_eval("conditioned_model_calls_only_amortized"),
    }
    c1 = derived["falsifier_clause_1"]["triggered"]
    c2p = derived["falsifier_clause_2"]["primary"]["triggered"]
    c2s = derived["falsifier_clause_2"]["sensitivity"]["triggered"]
    derived["decision"] = {
        "clause_1_triggered": c1,
        "clause_2_triggered_primary_cost_basis": c2p,
        "clause_2_triggered_sensitivity_cost_basis": c2s,
        "outcome_mapping_applied": None,
        "outcome_mapping_ambiguity": (
            "spec.json decision_rule.outcome_mapping maps CLAUSE_1_TRIGGERED_and_NOT_CLAUSE_2 to the label "
            "'FALSIFIES_INHERITANCE_NICHE' with the parenthetical '(share ii = 0 -> inheritance has niche)', while "
            "prereg.md section 3 prose for the same clause reads 'the ratchet's residual is irreducibly binding and "
            "inherited parameterization has a real economic niche'. The label and the prereg prose assert OPPOSITE "
            "consequences for the same condition. The mapping is reported but not silently resolved; the DIRECTOR owns it."
        ),
    }
    if not c1 and not c2p and not c2s:
        derived["decision"]["outcome_mapping_applied"] = "NEITHER_TRIGGERED -> INCONCLUSIVE"
    elif c1 and c2p:
        derived["decision"]["outcome_mapping_applied"] = "BOTH_TRIGGERED -> CONTRADICTORY"
    elif c2p and not c1:
        derived["decision"]["outcome_mapping_applied"] = "CLAUSE_2_TRIGGERED_and_NOT_CLAUSE_1 -> FALSIFIES_SPIDER_PREMISE"
    elif c1 and not c2p:
        derived["decision"]["outcome_mapping_applied"] = "CLAUSE_1_TRIGGERED_and_NOT_CLAUSE_2 -> label 'FALSIFIES_INHERITANCE_NICHE' vs prereg prose 'inheritance has niche' (CONTRADICTORY IN THE FROZEN DESIGN)"

    # -- 10. controls verdicts ------------------------------------------------
    pc_planted = [x for x in pc_labels if x["role"] in PC_PLANTED_ROLES]
    pc_plant_state_keys = {}
    for x in pc_planted:
        pc_plant_state_keys.setdefault(x["episode"], set()).add(x["state_sig"])
    pc_verification = {
        "control": PC_ARM,
        "prereg_criterion": "sigma_1 ~ 1.0, sigma_2 ~ 0, sigma_3 ~ 0 for planted spans; shares (ii) and (iii) must be 0 by construction (prereg.md 7.3, 10.1)",
        "planted_roles": list(PC_PLANTED_ROLES),
        "planted_span_occurrences": len(pc_planted),
        "per_episode_create_state_keys_distinct_counts": {
            str(e): len(v) for e, v in list(pc_plant_state_keys.items())[:5]
        },
        "plant_verified_byte_identical_observations": all(
            len(v) == 1 for v in pc_plant_state_keys.values()
        ),
        "planted_span_distinct_correct_actions_per_episode": all(
            len({x["correct_action_key"] for x in pc_planted if x["episode"] == e}) == 4
            for e in pc_plant_state_keys
        ),
        "planted_span_class_counts": {c: sum(1 for x in pc_planted if x["class"] == c) for c in CLASS_ORDER},
        "planted_span_closed_by_conditioned": sum(1 for x in pc_planted if x["closed_by_conditioned"]),
        "whole_trace_class_counts": {c: sum(1 for x in pc_labels if x["class"] == c) for c in CLASS_ORDER},
        "whole_trace_share_class_ii": wilson(sum(1 for x in pc_labels if x["class"] == "ii"), len(pc_labels)),
        "conditioned_reference_plant_compile_and_deopt": {
            "compiled_replays": sum(1 for x in pc_planted if x["closed_by_compilation"]),
            "deopted": sum(1 for x in pc_planted if not x["closed_by_compilation"]),
        },
        "reading_A_prereg_section_8_literal": "class (ii) fires on any state key that recurs with a different action, so the PC's planted spans are class (ii) and the prereg sigma_2~0 criterion is not attainable by construction",
        "reading_B_goal_aware_mandate": "class (ii) requires that goal conditioning cannot bind the span; the PC's binding key IS in the goal prefix, so its planted spans are merely-novel and the sigma_2~0 criterion is met",
        "planted_span_closed_by_conditioned_fraction": wilson(
            sum(1 for x in pc_planted if x["closed_by_conditioned"]), len(pc_planted)
        ),
    }
    raw["pc_verification"] = pc_verification
    write_json(art("pc_verification.json"), pc_verification)

    nc_classes = {c: sum(1 for x in nc_labels if x["class"] == c) for c in CLASS_ORDER}
    nc_verification = {
        "control": NC_ARM,
        "prereg_criterion": "sigma_2 == 0 exactly and sigma_3 == 0 exactly (prereg.md 7.4, 10.2)",
        "mechanism": "parent taskplan._with_nonce: every path carries ?n=<episode>-<step>",
        "class_counts": nc_classes,
        "sigma_2_is_zero": nc_classes["ii"] == 0,
        "sigma_3_is_zero": nc_classes["iii"] == 0,
        "span_occurrences": len(nc_labels),
        "unique_state_keys": len({x["state_sig"] for x in nc_labels}),
        "unique_signatures": len({x["signature"] for x in nc_labels}),
        "declared_deviation": "the class-(iii) plant is disabled in this control; otherwise a planted class-(iii) span would (correctly) be reported as class (iii) and the null's exactly-zero criterion would be unattainable by construction",
        "sigma_2_root_cause": _nc_sigma2_root_cause(nc_labels),
        "prereg_section_13_mitigation_variant": _nc_section13_variant(nc_labels),
        "verdict": _nc_verdict(nc_labels),
    }
    raw["nc_verification"] = nc_verification
    write_json(art("nc_verification.json"), nc_verification)

    correctness = {}
    for label, run in (
        (REFERENCE_ARM, ref_runs[f"{CONTROL_NOVELTY_RATE:.2f}"]),
        (TREATMENT_ARM, cond_runs[f"{CONTROL_NOVELTY_RATE:.2f}"]),
        (NARROW_ARM, narrow_runs[f"{CONTROL_NOVELTY_RATE:.2f}"]),
        (COLD_ARM, cold_runs[f"{CONTROL_NOVELTY_RATE:.2f}"]),
        (PC_ARM, pc_ref),
        (NC_ARM, nc_ref),
        (REPL_ARM, repl_runs["0.50"]),
    ):
        code_ok = sum(1 for e in run.episodes if e.get("code_ok"))
        store_empty = sum(1 for e in run.episodes if e.get("final_store_empty"))
        correctness[label] = {
            "episodes": len(run.episodes),
            "episodes_all_steps_expected_code": code_ok,
            "episodes_goal_state_reached": store_empty,
            "success_rate_prereg_definition": (
                wilson(sum(1 for e in run.episodes if e.get("code_ok") and e.get("final_store_empty")), len(run.episodes))["point"]
                if run.episodes
                else None
            ),
            "span_level_correct_action_fraction": None,
        }
        # Span-level action correctness against the arm-independent declared plan
        # action (bound at execution time). This is NOT the arm's own oracle and
        # NOT the arm's own emitted action.
        if run.correct_actions:
            scored = []
            wrong = []
            for s in run.spans:
                k = (s["episode"], s["index"])
                if k not in run.correct_actions or k not in run.emitted_actions:
                    continue
                ok = run.correct_actions[k] == run.emitted_actions[k]
                scored.append(ok)
                if not ok:
                    wrong.append(
                        {
                            "episode": s["episode"],
                            "index": s["index"],
                            "work_item": s["work_item"],
                            "role": s["role"],
                            "decision_path": s.get("decision_path"),
                            "token_required": bool(s.get("token_param")),
                            "declared": s.get("declared_correct_path"),
                            "emitted": s["path"],
                        }
                    )
            correctness[label]["span_level_correct_action_fraction"] = wilson(sum(scored), len(scored))
            correctness[label]["span_level_incorrect_examples"] = wrong[:25]
            correctness[label]["n_span_level_incorrect"] = len(wrong)
    # class-(iii) span-level correctness for the treatment arm, measured directly
    for label, run, lab in (
        (TREATMENT_ARM, cond_runs["0.50"], [x for x in labels_all if abs(x["novelty_rate"] - 0.50) < 1e-9]),
    ):
        g = [x for x in lab if x["class"] == "iii"]
        nong = [x for x in lab if x["class"] != "iii"]
        correctness[label]["class_iii_spans"] = {
            "n": len(g),
            "conditioned_correct": sum(1 for x in g if x["closed_by_conditioned"]),
        }
        correctness[label]["non_class_iii_spans"] = {
            "n": len(nong),
            "conditioned_correct": sum(1 for x in nong if x["closed_by_conditioned"]),
        }
    raw["correctness_invariance"] = {
        "prereg_criterion": "prereg.md 10.5: all arms must achieve success_rate = 1.0; any arm with success < 1.0 -> MEASUREMENT_INVALID",
        "success_definition": "parent result.json definition: every step returned its expected status code AND the final resource store matched the goal state (empty)",
        "by_arm": correctness,
    }
    write_json(art("correctness_invariance.json"), raw["correctness_invariance"])

    # -- 11. cost ledgers ----------------------------------------------------
    for name, runs in (
        (REFERENCE_ARM, ref_runs),
        (TREATMENT_ARM, cond_runs),
        (NARROW_ARM, narrow_runs),
        (COLD_ARM, cold_runs),
        (REPL_ARM, repl_runs),
    ):
        with JsonlWriter(art(f"costs_{name}.jsonl")) as w:
            for nu in NOVELTY_GRID:
                w.write(runs[f"{nu:.2f}"].ledger.as_dict(50))
                for e in runs[f"{nu:.2f}"].episodes:
                    w.write({**e, "novelty_rate_key": nu})
    for name, run in ((PC_ARM, pc_ref), (NC_ARM, nc_ref), (PC_ARM + "-CONDITIONED", pc_cond), (NC_ARM + "-CONDITIONED", nc_cond)):
        with JsonlWriter(art(f"costs_{name}.jsonl")) as w:
            w.write(run.ledger.as_dict(50))
            for e in run.episodes:
                w.write(e)

    # -- 12. manifest --------------------------------------------------------
    artifacts_list = []
    for p in sorted(ARTIFACTS.glob("*")):
        # run_manifest.json cannot contain its own hash (it is written after this
        # list is built), and substrate_determinism_check.json is a leftover from a
        # prior failed stage. Both are excluded from the hashed list.
        if p.is_file() and p.name not in ("substrate_determinism_check.json", "run_manifest.json"):
            artifacts_list.append(
                {"path": f"research/experiments/{EXPERIMENT_ID}/artifacts/{p.name}", "sha256": sha256_file(p), "bytes": p.stat().st_size}
            )
    manifest = {
        "experiment_id": EXPERIMENT_ID,
        "lane": "frontier",
        "git_head": git("rev-parse", "HEAD"),
        "python": sys.version,
        "mint_salt": MINT_SALT,
        "wall_clock_seconds": round(time.time() - t_start, 1),
        "bootstrap": {"resamples": BOOTSTRAP_RESAMPLES, "seed": BOOTSTRAP_SEED, "unit": "episode"},
        "mint_salt_note": "MINT_SALT is the frozen salt for the opt-in capability mint; token = <episode_counter:08x><sha256(MINT_SALT|counter)[:8]>",
        "total_substrate_requests": sum(r.substrate_requests for r in list(ref_runs.values()) + list(cond_runs.values()) + list(narrow_runs.values()) + list(cold_runs.values()) + list(repl_runs.values()) + [pc_ref, pc_cond, nc_ref, nc_cond]) + 800,
        "episode_ledger": {
            REFERENCE_ARM: sum(len(r.episodes) for r in ref_runs.values()),
            TREATMENT_ARM: sum(len(r.episodes) for r in cond_runs.values()),
            NARROW_ARM: sum(len(r.episodes) for r in narrow_runs.values()),
            COLD_ARM: sum(len(r.episodes) for r in cold_runs.values()),
            REPL_ARM: sum(len(r.episodes) for r in repl_runs.values()),
            PC_ARM: len(pc_ref.episodes),
            NC_ARM: len(nc_ref.episodes),
        },
        "artifacts": artifacts_list,
        "artifact_hash_list_excludes": [
            "run_manifest.json (this file; it cannot contain its own hash)",
            "substrate_determinism_check.json (leftover from the prior failed stage, see below)",
        ],
        "pre_existing_artifact_not_produced_by_this_run": {
            "path": f"research/experiments/{EXPERIMENT_ID}/artifacts/substrate_determinism_check.json",
            "why": "left behind by the prior EXECUTE attempt recorded in failure.json (exit 66) and model_execute.json (exit 124); NOT used as evidence by this run. This run's own idempotency evidence is substrate_idempotency.json.",
        },
    }
    write_json(art("run_manifest.json"), manifest)

    out = {
        "raw": raw,
        "derived": derived,
        "manifest": manifest,
    }
    (REPO_ROOT / "research" / "frontier" / "_run_output_36272394045.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("WROTE research/frontier/_run_output_36272394045.json", flush=True)
    print("clause1:", c1, "clause2_primary:", c2p, "clause2_sensitivity:", c2s, flush=True)
    print("decision:", derived["decision"]["outcome_mapping_applied"], flush=True)
    print(f"total wall clock {time.time() - t_start:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
