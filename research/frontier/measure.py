"""Measurement layer for EXP-FRONTIER-36249071934.

Frozen-design provenance: prereg.md sections 7.1-7.4, 9, 10, 11.

Everything here is a DERIVED MEASUREMENT computed from the raw span records
emitted by the arms. Nothing in this module talks to the substrate or the arms.
"""

from __future__ import annotations

import math
import random
from typing import Any, Iterable, Sequence

BOOTSTRAP_RESAMPLES = 10_000
BOOTSTRAP_SEED = 20260926


# ---------------------------------------------------------------------------
# prereg.md 7.1 -- per-span witnessed determinism
# ---------------------------------------------------------------------------
def determinism(witness_counts: Sequence[int]) -> dict[str, Any]:
    """deterministic_spans / total_spans with the prereg's >=2-episode witness rule."""
    total = len(witness_counts)
    deterministic = sum(1 for c in witness_counts if c >= 2)
    frac = (deterministic / total) if total else float("nan")
    lo, hi = wilson(deterministic, total)
    return {
        "total_spans": total,
        "deterministic_spans": deterministic,
        "determinism_fraction": frac,
        "wilson_ci95": [lo, hi],
        "rule": "span signature identical across >=2 episodes (prereg.md 7.1)",
    }


def wilson(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = successes / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def learning_curve(records: Iterable[dict[str, Any]], witness_by_sig: dict[str, int]) -> list[dict[str, Any]]:
    """prereg.md 7.1 per-episode learning curve over distinct span signatures.

    Retrospective by construction: a signature counts in the numerator once its
    FINAL distinct-episode witness count reaches 2, so the curve shows what the
    ratchet was able to learn cumulatively, episode by episode. The
    non-retrospective companion is ``model_calls_per_episode``, which is what
    the ratchet actually spent.
    """
    curve: list[dict[str, Any]] = []
    seen_total = 0
    seen_deterministic = 0
    for ep, sigs in _group_unique_by_episode(records):
        seen_total += len(sigs)
        newly = sum(1 for sig in sigs if witness_by_sig.get(sig, 0) >= 2)
        seen_deterministic += newly
        curve.append(
            {
                "episode": ep,
                "cumulative_unique_spans": seen_total,
                "cumulative_deterministic_unique_spans": seen_deterministic,
                "cumulative_determinism_fraction": (seen_deterministic / seen_total) if seen_total else None,
                "episode_unique_spans": len(sigs),
                "episode_deterministic_unique_spans": newly,
            }
        )
    return curve


def _group_unique_by_episode(records: Iterable[dict[str, Any]]) -> list[tuple[int, list[str]]]:
    order: list[int] = []
    seen: dict[int, list[str]] = {}
    local: dict[int, set[str]] = {}
    for r in records:
        ep = r["episode"]
        if ep not in local:
            local[ep] = set()
            order.append(ep)
        local[ep].add(r["signature"])
    for ep in order:
        seen[ep] = sorted(local[ep])
    return [(ep, seen[ep]) for ep in order]


# ---------------------------------------------------------------------------
# prereg.md 7.4 -- residual-novelty tiers
# ---------------------------------------------------------------------------
NOVELTY_TIERS = ("never_seen", "seen_once", "seen_multiple")


def novelty_tiers(records: Sequence[dict[str, Any]], witness_by_sig: dict[str, int]) -> dict[str, Any]:
    """Cost/observation contribution by span novelty tier at the moment of execution.

    Tier is assigned from the *pre-execution* witness count of the span
    signature: 0 prior episodes -> never_seen, 1 -> seen_once, >=2 -> seen_multiple.
    """
    out: dict[str, dict[str, int]] = {t: {"spans": 0, "model_calls": 0, "compiled_replays": 0} for t in NOVELTY_TIERS}
    per_arm_model: dict[str, int] = {}
    for r in records:
        prior = r.get("prior_witnesses", 0)
        tier = "never_seen" if prior == 0 else ("seen_once" if prior == 1 else "seen_multiple")
        out[tier]["spans"] += 1
        if r["decision_path"].startswith("DEOPT"):
            out[tier]["model_calls"] += 1
            per_arm_model[r["arm"]] = per_arm_model.get(r["arm"], 0) + 1
        else:
            out[tier]["compiled_replays"] += 1
    return {"tiers": out, "model_calls_by_arm": per_arm_model}


# ---------------------------------------------------------------------------
# prereg.md 9 -- non-parametric bootstrap for cost differences
# ---------------------------------------------------------------------------
def bootstrap_cost_difference(
    a: Sequence[float], b: Sequence[float], resamples: int = BOOTSTRAP_RESAMPLES, seed: int = BOOTSTRAP_SEED
) -> dict[str, Any]:
    rng = random.Random(seed)
    n = min(len(a), len(b))
    a = list(a[:n])
    b = list(b[:n])
    point = sum(a) / n - sum(b) / n
    diffs: list[float] = []
    for _ in range(resamples):
        sa = 0.0
        sb = 0.0
        for _ in range(n):
            k = rng.randrange(n)
            sa += a[k]
            sb += b[k]
        diffs.append(sa / n - sb / n)
    diffs.sort()
    return {
        "n_episodes_paired": n,
        "resamples": resamples,
        "seed": seed,
        "mean_difference_units": point,
        "ci95": [diffs[int(0.025 * resamples)], diffs[int(0.975 * resamples) - 1]],
        "p_two_sided_bootstrap": (2 * min(sum(1 for d in diffs if d <= 0), sum(1 for d in diffs if d >= 0)) / resamples),
    }


# ---------------------------------------------------------------------------
# prereg.md 10 -- frozen decision rule
# ---------------------------------------------------------------------------
SUCCESS_THRESHOLD = 0.95
TIE_RELATIVE = 0.05


def classify_outcome(
    c_deopt: float, c_inherited: float, c_cold: float, s_deopt: float, s_inherited: float, s_cold: float
) -> dict[str, Any]:
    """Frozen three-way decision rule, applied verbatim."""
    matched = s_deopt >= SUCCESS_THRESHOLD and s_inherited >= SUCCESS_THRESHOLD and s_cold >= SUCCESS_THRESHOLD
    if not matched:
        failing = [
            name
            for name, s in (("B-NO-MEMORY-DETERMINISTIC", s_deopt), ("B-INHERITED-SPIDER", s_inherited), ("B-COLD-EXPLORATION", s_cold))
            if s < SUCCESS_THRESHOLD
        ]
        return {
            "classification": "MATCHED_CORRECTNESS_FAILED",
            "matched_correctness": False,
            "failing_arms": failing,
            "rule_trace": {
                "success_threshold": SUCCESS_THRESHOLD,
                "success_rates": {
                    "B-NO-MEMORY-DETERMINISTIC": s_deopt,
                    "B-INHERITED-SPIDER": s_inherited,
                    "B-COLD-EXPLORATION": s_cold,
                },
                "costs": {
                    "B-NO-MEMORY-DETERMINISTIC": c_deopt,
                    "B-INHERITED-SPIDER": c_inherited,
                    "B-COLD-EXPLORATION": c_cold,
                },
            },
        }
    dominant = c_deopt < c_inherited and c_deopt < c_cold
    tie = abs(c_deopt - c_inherited) <= TIE_RELATIVE * max(c_deopt, c_inherited) and c_deopt < c_cold and c_inherited < c_cold
    if dominant:
        cls = "DEOPT_DOMINATES"
    elif tie:
        cls = "DEOPT_TIES"
    else:
        cls = "DEOPT_LOSES"
    return {
        "classification": cls,
        "matched_correctness": True,
        "failing_arms": [],
        "rule_trace": {
            "success_threshold": SUCCESS_THRESHOLD,
            "success_rates": {
                "B-NO-MEMORY-DETERMINISTIC": s_deopt,
                "B-INHERITED-SPIDER": s_inherited,
                "B-COLD-EXPLORATION": s_cold,
            },
            "costs": {
                "B-NO-MEMORY-DETERMINISTIC": c_deopt,
                "B-INHERITED-SPIDER": c_inherited,
                "B-COLD-EXPLORATION": c_cold,
            },
            "tie_relative_threshold": TIE_RELATIVE,
            "deopt_less_inherited": c_deopt < c_inherited,
            "deopt_less_cold": c_deopt < c_cold,
        },
    }


def histogram(witness_counts: Sequence[int]) -> dict[str, int]:
    return {str(k): int(v) for k, v in sorted(_counts(witness_counts).items())}


def _counts(values: Iterable[int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for v in values:
        out[v] = out.get(v, 0) + 1
    return out
