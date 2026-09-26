#!/usr/bin/env python3
"""Frozen EXECUTE runner for EXP-FRONTIER-36249071934 (lane: frontier).

Runs exactly the design frozen in spec.json / prereg.md / freeze.json:

  main comparison   3 arms x 50 episodes x 24 spans, novelty rate 0.50
  controls          PC-WITNESSED-DETERMINISM, NC-ZERO-DETERMINISM,
                    PC-EXACT-REPLAY, NC-EMPTY-REGISTRY
  (non-decision-gating) novelty-rate sensitivity sweep, reported separately

Nothing here reads an outcome before it is written to a raw artifact. Every
number that later appears in result.json is computed by research/frontier/
measure.py from the raw span records written under artifacts/.

Usage:
    python3 research/frontier/run_experiment_EXP_FRONTIER_36249071934.py
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from research.frontier import measure  # noqa: E402
from research.frontier.arms.common import ensure_src_on_path  # noqa: E402
from research.frontier.arms.cold_exploration import ColdExploration  # noqa: E402
from research.frontier.arms.deopt_ratchet import DeoptRatchet  # noqa: E402
from research.frontier.arms.inherited_spider import InheritedSpider  # noqa: E402
from research.frontier.substrate_deterministic_http import (  # noqa: E402
    BANNER,
    DeterministicHTTPSubstrate,
    determinism_check,
)
from research.frontier.taskplan import (  # noqa: E402
    EXPECTED_CODES,
    MAIN_NOVELTY_RATE,
    SPANS_PER_EPISODE,
    SWEEP_NOVELTY_RATES,
    episode_plan,
)

EXPERIMENT_ID = "EXP-FRONTIER-36249071934"
PACKET_DIR = REPO_ROOT / "research" / "experiments" / EXPERIMENT_ID
ARTIFACT_DIR = PACKET_DIR / "artifacts"

EPISODES = 50
SWEEP_EPISODES = 20
SWEEP_ARMS = ("B-NO-MEMORY-DETERMINISTIC", "B-COLD-EXPLORATION")

ensure_src_on_path()


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def write_json(path: Path, payload: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True, default=str)
    path.write_text(text + "\n", encoding="utf-8")
    return hashlib.sha256((text + "\n").encode("utf-8")).hexdigest()


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, sort_keys=True, default=str) + "\n" for r in rows)
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def annotate_prior_witnesses(records: list[Any]) -> dict[str, int]:
    """Normalise raw SpanRecords to dicts and attach witness counts.

    prereg.md 7.4 tiers a span by how many DISTINCT EPISODES had already
    witnessed its signature before this execution. prereg.md 7.1 determinism
    uses the final distinct-episode witness count.
    """
    rows: list[dict[str, Any]] = []
    episodes_by_sig: dict[str, set[int]] = {}
    for r in records:
        row = r.as_dict() if hasattr(r, "as_dict") else dict(r)
        sig = row["signature"]
        ep = row["episode"]
        seen = episodes_by_sig.setdefault(sig, set())
        row["prior_witnesses"] = len(seen)
        seen.add(ep)
        rows.append(row)
    witness_by_sig = {sig: len(eps) for sig, eps in episodes_by_sig.items()}
    for row in rows:
        row["final_witnesses"] = witness_by_sig[row["signature"]]
    records[:] = rows
    return witness_by_sig


def run_arm(
    arm_obj: Any,
    arm_name: str,
    episodes: int,
    novelty_rate: float,
    machinery_per_span: bool = False,
    force_nonce: bool = False,
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    episode_rows: list[dict[str, Any]] = []
    collect = [] if arm_name == "B-INHERITED-SPIDER" else None
    with DeterministicHTTPSubstrate() as sub:
        client = sub.keepalive()
        try:
            for ep in range(1, episodes + 1):
                plan = episode_plan(ep, novelty_rate, force_nonce=force_nonce)
                if arm_name == "B-INHERITED-SPIDER" and ep == 1:
                    # prereg.md 6.2: the registry is populated by distill() from
                    # Episode 1 observations and is static thereafter.
                    row = arm_obj.run_episode(sub, client, ep, plan, records, collect=collect)
                else:
                    row = arm_obj.run_episode(sub, client, ep, plan, records)
                row["machinery_units"] = len(plan) if machinery_per_span else 0
                episode_rows.append(row)
        finally:
            client.close()
    witness_by_sig = annotate_prior_witnesses(records)
    return {
        "records": records,
        "episodes": episode_rows,
        "witness_by_sig": witness_by_sig,
        "ledger": arm_obj.ledger,
        "arm_obj": arm_obj,
    }


def episode_costs(episode_rows: list[dict[str, Any]]) -> list[float]:
    """Per-episode amortised cost in prereg abstract units.

    One unit per span executed, one per deopt, one per compile event, and one per
    inheritance-machinery step (resolve+bind+verify+freshness bundle) for any arm
    that performs one.
    """
    return [
        float(r["spans"] + r["model_calls"] + r.get("compile_events", 0) + r.get("machinery_units", 0))
        for r in episode_rows
    ]


def success_rate(episode_rows: list[dict[str, Any]]) -> float:
    if not episode_rows:
        return float("nan")
    ok = sum(1 for r in episode_rows if r["code_ok"] and r["final_store_empty"])
    return ok / len(episode_rows)


# ---------------------------------------------------------------------------
# RAW evidence 1: substrate availability
# ---------------------------------------------------------------------------
def availability_probe() -> dict[str, Any]:
    probe: dict[str, Any] = {
        "python": sys.version,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "stdlib_http_httpserver": True,
        "substrate_banner": BANNER,
    }
    for mod in ("flask", "fastapi", "browsergym", "playwright", "openai"):
        try:
            __import__(mod)
            probe[f"{mod}_importable"] = True
        except Exception:
            probe[f"{mod}_importable"] = False
    for var in ("OPENAI_API_KEY", "HF_TOKEN", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"):
        probe[f"env_{var}_present"] = bool(os.environ.get(var))
    try:
        probe["docker_cli_available"] = subprocess.run(
            ["docker", "--version"], capture_output=True, timeout=10
        ).returncode == 0
    except Exception:
        probe["docker_cli_available"] = False
    with DeterministicHTTPSubstrate() as sub:
        client = sub.keepalive()
        try:
            code, raw, _ = client.request("GET", "/")
            probe["stdlib_http_get_status"] = code
            probe["stdlib_http_get_body"] = json.loads(raw)
            code, raw, _ = client.request("PUT", "/resources/probe", {"title": "t", "value": 1})
            probe["stdlib_http_put_status"] = code
            probe["stdlib_http_post_supported"] = True
        finally:
            client.close()
    return probe


# ---------------------------------------------------------------------------
# RAW evidence 2: incumbent-kernel direct probe
# ---------------------------------------------------------------------------
def kernel_probe() -> dict[str, Any]:
    from spider.kernel import SpiderKernel
    from spider.models import Observation
    from spider.registry import MechanismRegistry
    import tempfile

    out: dict[str, Any] = {}
    with tempfile.TemporaryDirectory() as d:
        reg = MechanismRegistry(Path(d) / "registry.jsonl")
        k = SpiderKernel(reg)  # shipped defaults
        obs = Observation(
            intent="create_resource",
            state={"store_size": 0},
            action={"method": "PUT", "path": "/resources/r1", "body": {"title": "t", "value": 1}},
            next_state={"store_size": 1},
            success=True,
            provenance={"probe": True},
        )
        mech = k.distill(obs)
        out["distill_confidence"] = mech.confidence
        out["kernel_min_confidence"] = k.min_confidence
        out["distill_populates_parameter_slots"] = bool(mech.parameter_slots)
        out["distill_populates_freshness"] = bool(mech.freshness)
        out["distill_populates_applicability_guards"] = bool(mech.applicability_guards)
        out["distill_populates_verification_rule"] = bool(mech.verification_rule)
        out["distill_populates_repair_scope"] = bool(mech.repair_scope)
        out["distill_populates_failure_boundary"] = bool(mech.failure_boundary)
        out["registry_empty_before_distill"] = len(reg.all()) == 0
        out["registry_empty_after_distill_no_upsert"] = len(reg.all()) == 0
        reg.upsert(mech)
        exact = k.resolve("create_resource", {"store_size": 0})
        out["resolve_exact_intent_and_preconditions_status"] = exact.status.value
        out["resolve_exact_intent_and_preconditions_reason"] = exact.reason
        out["resolve_exact_confidence"] = exact.confidence
        out["resolve_paraphrased_intent_status"] = k.resolve(
            "create a new resource on the server", {"store_size": 0}
        ).status.value
        out["verify_returns"] = k.verify(mech.mechanism_id, {"store_size": 1, "store_keys": []})
        # diagnostic only (NOT the shipped configuration, NOT used by any arm)
        k_loose = SpiderKernel(reg, min_confidence=0.5)
        loose = k_loose.resolve("create_resource", {"store_size": 0})
        out["diagnostic_resolve_at_min_confidence_0_5_status"] = loose.status.value
        out["diagnostic_note"] = (
            "min_confidence=0.5 is a DIAGNOSTIC probe showing the binding constraint is the "
            "confidence gate, not applicability. No arm uses it."
        )
    src = (REPO_ROOT / "src" / "spider").rglob("*.py")
    confidences = []
    for p in src:
        confidences.extend(
            (str(p.relative_to(REPO_ROOT)), float(m.group(1)))
            for m in re.finditer(r"confidence\s*=\s*([0-9.]+)", p.read_text(encoding="utf-8"))
        )
    out["shipped_confidence_literals"] = confidences
    out["shipped_has_distill_parameterized"] = any(
        "def distill_parameterized" in p.read_text(encoding="utf-8")
        for p in (REPO_ROOT / "src" / "spider").rglob("*.py")
    )
    return out


# ---------------------------------------------------------------------------
# controls
# ---------------------------------------------------------------------------
CONTROL_TRACES: dict[str, list[dict[str, Any]]] = {}


def _capture(name: str, run: dict[str, Any]) -> None:
    CONTROL_TRACES[name] = run["records"]


def control_pc_witnessed_determinism() -> dict[str, Any]:
    arm = DeoptRatchet(arm="PC-WITNESSED-DETERMINISM")
    run = run_arm(arm, arm.arm, EPISODES, 0.0)
    _capture("PC-WITNESSED-DETERMINISM", run)
    det = measure.determinism(_witness_list(run))
    curve = measure.learning_curve(run["records"], run["witness_by_sig"])
    per_ep = [r["model_calls"] for r in run["episodes"]]
    cache_conflicts = [
        {
            "state_sig": k,
            "first_request": e.request,
            "witnesses": e.witnesses,
            "spans_touching_key": sorted(
                {
                    (r["episode"], r["index"], r["role"], r["method"], r["path"])
                    for r in run["records"]
                    if r["state_sig"] == k
                }
            )[:12],
        }
        for k, e in arm.cache.items()
        if e.ambiguous
    ]
    det_by_ep10 = _cumulative_det_at(curve, 10)
    literal_after_ep1 = sum(per_ep[1:])
    after_compile = arm.model_calls_after_compile_complete
    compiled_at = arm.compiled_complete_at_episode
    return {
        "id": "PC-WITNESSED-DETERMINISM",
        "role": "positive_control",
        "expected": "determinism_fraction=1.0, model_calls_after_compile=0, amortised cost -> compile+execution only",
        "observed": {
            "determinism_fraction": det["determinism_fraction"],
            "total_spans": det["total_spans"],
            "deterministic_spans": det["deterministic_spans"],
            "cumulative_determinism_fraction_by_episode_10": det_by_ep10,
            "model_calls_per_episode": per_ep,
            "model_calls_episodes_2_to_50_literal": literal_after_ep1,
            "compiled_complete_at_episode": compiled_at,
            "model_calls_strictly_after_compile_complete": after_compile,
            "amortized_cost_units_per_episode": arm.ledger.amortized(EPISODES),
            "ledger": arm.ledger.as_dict(EPISODES),
            "success_rate": success_rate(run["episodes"]),
            "model_calls_per_episode_steady_state": sorted(set(per_ep[4:])),
            "compiled_state_keys": sum(1 for e in arm.cache.values() if e.compiled_at_episode >= 0),
            "ambiguous_state_keys": len(arm.cache) and sum(1 for e in arm.cache.values() if e.ambiguous),
            "ambiguous_state_key_detail": cache_conflicts,
        },
        "pass": bool(
            (det_by_ep10 is not None and det_by_ep10 >= 0.99) and after_compile == 0
        ),
        "note": (
            "spec.json positive_control says 'compile all spans on first episode' while "
            "prereg.md 6.1 step 2 requires >=2 witnesses. Under the prereg rule compilation "
            "completes during episode 2, so episode 2 still deopts. Both the literal reading "
            "(model_calls_episodes_2_to_50) and the compilation-complete reading "
            "(model_calls_strictly_after_compile_complete) are reported; the PASS judgement uses "
            "the prereg.md 6.1 rule because prereg.md 8.1 is the frozen pass criterion."
        ),
    }


def control_nc_zero_determinism() -> dict[str, Any]:
    arm = DeoptRatchet(arm="NC-ZERO-DETERMINISM")
    run = run_arm(arm, arm.arm, EPISODES, 1.0, force_nonce=True)
    _capture("NC-ZERO-DETERMINISM", run)
    det = measure.determinism(_witness_list(run))
    cold = ColdExploration(arm="NC-ZERO-DETERMINISM-REF")
    run_cold = run_arm(cold, cold.arm, EPISODES, 1.0, machinery_per_span=True, force_nonce=True)
    c_nc = arm.ledger.amortized(EPISODES)
    c_cold = cold.ledger.amortized(EPISODES)
    # prereg.md 7.2 defines amortized_cost over exactly three components
    # (compile + model + execution). The prereg.md 6.2 inheritance-machinery
    # unit is an ADDITIONAL component, so the literal prereg.md 7.2 ratio and
    # the machinery-inclusive ratio are both reported.
    c_nc_3term = (arm.ledger.compile_units + arm.ledger.model_units + arm.ledger.execution_units) / EPISODES
    c_cold_3term = (cold.ledger.compile_units + cold.ledger.model_units + cold.ledger.execution_units) / EPISODES
    return {
        "id": "NC-ZERO-DETERMINISM",
        "role": "null_control",
        "expected": "determinism_fraction=0.0, model_calls = all spans every episode, cost_ratio_vs_cold >= 1.0",
        "observed": {
            "determinism_fraction": det["determinism_fraction"],
            "total_spans": det["total_spans"],
            "deterministic_spans": det["deterministic_spans"],
            "unique_span_signatures": len(run["witness_by_sig"]),
            "model_calls_total": arm.ledger.model_units,
            "total_spans_executed": arm.ledger.execution_units,
            "compile_units": arm.ledger.compile_units,
            "amortized_cost_units_per_episode": c_nc,
            "reference_cold_amortized_cost_units_per_episode": c_cold,
            "cost_ratio_vs_cold_machinery_inclusive": c_nc / c_cold,
            "amortized_cost_units_per_episode_prereg_7_2_three_term": c_nc_3term,
            "reference_cold_amortized_cost_units_per_episode_prereg_7_2_three_term": c_cold_3term,
            "cost_ratio_vs_cold_prereg_7_2_three_term": c_nc_3term / c_cold_3term,
            "success_rate": success_rate(run["episodes"]),
            "ledger": arm.ledger.as_dict(EPISODES),
        },
        "pass": bool(
            det["determinism_fraction"] <= 0.01 and (c_nc_3term / c_cold_3term) >= 1.0
        ),
        "note": (
            "The two cost ratios differ ONLY by the prereg.md 6.2 inheritance-machinery unit, which "
            "the deopt ratchet structurally never pays and the cold reference arm pays once per span. "
            "The PASS judgement uses the literal prereg.md 7.2 three-component formula; the "
            "machinery-inclusive ratio is reported alongside so the auditor can re-judge."
        ),
    }


def control_pc_exact_replay() -> dict[str, Any]:
    """prereg.md 8.3 -- the inherited kernel must reach EXECUTABLE on an exact
    mechanism match. This is a control on the *incumbent instrument*, not on
    the architecture hypothesis."""
    arm = InheritedSpider(arm="PC-EXACT-REPLAY")
    records: list[dict[str, Any]] = []
    statuses: dict[str, int] = {}
    with DeterministicHTTPSubstrate() as sub:
        client = sub.keepalive()
        try:
            for ep in (1, 2):
                plan = episode_plan(1, 0.0)  # fully structural plan: exact replay
                row = arm.run_episode(sub, client, ep, plan, records, collect=[] if ep == 1 else None)
                statuses[f"episode_{ep}"] = row["model_calls"]
        finally:
            client.close()
    rows = [r.as_dict() for r in records]
    annotate_prior_witnesses(rows)
    CONTROL_TRACES["PC-EXACT-REPLAY"] = rows
    res_counts: dict[str, int] = {}
    for r in rows:
        st = r["detail"]["resolution_status"]
        res_counts[st] = res_counts.get(st, 0) + 1
    dump = arm.registry_dump()
    return {
        "id": "PC-EXACT-REPLAY",
        "role": "additional_control_measured_not_decision_gating",
        "expected": "inherited kernel achieves EXECUTABLE with zero novel decisions on an exact mechanism match",
        "observed": {
            "episodes": 2,
            "spans": len(rows),
            "resolution_status_counts": res_counts,
            "model_calls_episode_1": statuses["episode_1"],
            "model_calls_episode_2": statuses["episode_2"],
            "novel_decisions_episode_2": statuses["episode_2"],
            "registry": dump,
            "kernel_config": arm.kernel_config,
        },
        "pass": bool(res_counts.get("EXECUTABLE", 0) > 0 and statuses["episode_2"] == 0),
        "note": (
            "mechanisms_distilled="
            f"{arm.mechanisms_distilled}, distill_calls={arm.distill_calls}. A FAIL here is an "
            "observation about the shipped kernel's executability, not about inheritance economics."
        ),
    }


def control_nc_empty_registry() -> dict[str, Any]:
    arm = ColdExploration(arm="NC-EMPTY-REGISTRY")
    run = run_arm(arm, arm.arm, 1, MAIN_NOVELTY_RATE)
    res_counts: dict[str, int] = {}
    for r in run["records"]:
        res_counts[r["detail"]["resolution_status"]] = res_counts.get(r["detail"]["resolution_status"], 0) + 1
    return {
        "id": "NC-EMPTY-REGISTRY",
        "role": "additional_control_measured_not_decision_gating",
        "expected": "inherited kernel returns UNKNOWN for every span when the registry is emptied",
        "observed": {
            "spans": len(run["records"]),
            "resolution_status_counts": res_counts,
            "registry_size": len(arm.registry.all()),
            "registry_empty": len(arm.registry.all()) == 0,
            "kernel_config": arm.kernel_config,
        },
        "pass": bool(res_counts.get("UNKNOWN", 0) == len(run["records"])),
    }


def _witness_list(run: dict[str, Any]) -> list[int]:
    return [r["final_witnesses"] for r in run["records"]]


def _cumulative_det_at(curve: list[dict[str, Any]], episode: int) -> float | None:
    for row in curve:
        if row["episode"] == episode:
            return row["cumulative_determinism_fraction"]
    return None


# ---------------------------------------------------------------------------
# non-decision-gating sensitivity sweep
# ---------------------------------------------------------------------------
def novelty_sweep() -> dict[str, Any]:
    rows = []
    for nu in SWEEP_NOVELTY_RATES:
        arm = DeoptRatchet(arm=f"SWEEP-NU{nu:.2f}-DEOPT")
        run = run_arm(arm, arm.arm, SWEEP_EPISODES, nu)
        det = measure.determinism(_witness_list(run))
        cold = ColdExploration(arm=f"SWEEP-NU{nu:.2f}-COLD")
        run_cold = run_arm(cold, cold.arm, SWEEP_EPISODES, nu, machinery_per_span=True)
        c_d = arm.ledger.amortized(SWEEP_EPISODES)
        c_c = cold.ledger.amortized(SWEEP_EPISODES)
        rows.append(
            {
                "target_novelty_rate": nu,
                "realized_determinism_fraction": det["determinism_fraction"],
                "realized_deterministic_spans": det["deterministic_spans"],
                "total_spans": det["total_spans"],
                "unique_span_signatures": len(run["witness_by_sig"]),
                "deopt_amortized_cost": c_d,
                "cold_amortized_cost": c_c,
                "deopt_minus_cold": c_d - c_c,
                "deopt_cost_ratio_vs_cold": c_d / c_c,
                "compile_units": arm.ledger.compile_units,
                "model_units_deopt": arm.ledger.model_units,
                "model_units_cold": cold.ledger.model_units,
                "success_deopt": success_rate(run["episodes"]),
                "success_cold": success_rate(run_cold["episodes"]),
            }
        )
    breakeven = [r for r in rows if r["deopt_minus_cold"] < 0]
    return {
        "role": "non_decision_gating_sensitivity",
        "why": (
            "The frozen design does not specify the task generator's novelty rate, so the headline "
            "per-span determinism fraction is a property of the pre-declared mixture rather than a "
            "discovered constant. Sweeping the rate locates the deopt ratchet's break-even and shows "
            "the headline point estimate is not an artefact of the chosen mixture. This sweep does "
            "NOT enter the frozen three-way decision rule."
        ),
        "episodes_per_point": SWEEP_EPISODES,
        "main_arm_novelty_rate": MAIN_NOVELTY_RATE,
        "points": rows,
        "break_even_novelty_rates_deopt_cheaper_than_cold": [r["target_novelty_rate"] for r in breakeven],
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> int:
    t0 = time.time()
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}

    print("[1/8] availability probe", flush=True)
    hashes["availability_probe.json"] = write_json(ARTIFACT_DIR / "availability_probe.json", availability_probe())

    print("[2/8] substrate determinism check (100 repeats x 8 probes)", flush=True)
    hashes["substrate_determinism_check.json"] = write_json(
        ARTIFACT_DIR / "substrate_determinism_check.json", determinism_check(100)
    )

    print("[3/8] incumbent-kernel direct probe", flush=True)
    hashes["kernel_probe.json"] = write_json(ARTIFACT_DIR / "kernel_probe.json", kernel_probe())

    print("[4/8] main comparison: 3 arms x 50 episodes", flush=True)
    arms: dict[str, Any] = {}
    for name, ctor in (
        ("B-NO-MEMORY-DETERMINISTIC", DeoptRatchet),
        ("B-INHERITED-SPIDER", InheritedSpider),
        ("B-COLD-EXPLORATION", ColdExploration),
    ):
        obj = ctor(arm=name)
        run = run_arm(
            obj, name, EPISODES, MAIN_NOVELTY_RATE, machinery_per_span=(name != "B-NO-MEMORY-DETERMINISTIC")
        )
        arms[name] = {"obj": obj, **run}
        print(f"      {name}: {len(run['records'])} spans", flush=True)

    print("[5/8] controls", flush=True)
    controls = {
        "PC-WITNESSED-DETERMINISM": control_pc_witnessed_determinism(),
        "NC-ZERO-DETERMINISM": control_nc_zero_determinism(),
        "PC-EXACT-REPLAY": control_pc_exact_replay(),
        "NC-EMPTY-REGISTRY": control_nc_empty_registry(),
    }
    hashes["controls.json"] = write_json(ARTIFACT_DIR / "controls.json", controls)

    print("[6/8] novelty-rate sensitivity sweep (non-decision-gating)", flush=True)
    sweep = novelty_sweep()
    hashes["sensitivity_novelty_sweep.json"] = write_json(ARTIFACT_DIR / "sensitivity_novelty_sweep.json", sweep)

    print("[7/8] raw span traces + episode ledgers", flush=True)
    for name, run in arms.items():
        slug = name.replace("B-", "").lower()
        hashes[f"spans_{slug}.jsonl"] = write_jsonl(ARTIFACT_DIR / f"spans_{slug}.jsonl", run["records"])
        hashes[f"episodes_{slug}.jsonl"] = write_jsonl(ARTIFACT_DIR / f"episodes_{slug}.jsonl", run["episodes"])
    for cname, rows in CONTROL_TRACES.items():
        slug = cname.lower().replace("-", "_")
        hashes[f"control_spans_{slug}.jsonl"] = write_jsonl(
            ARTIFACT_DIR / f"control_spans_{slug}.jsonl", rows
        )
    # matched-task-instance verification: the three arms must have observed the
    # identical span population, otherwise the cost comparison is not matched.
    keys = {
        name: {(r["episode"], r["index"]): (r["signature"], r["response_code"], r["response_body_hash"]) for r in run["records"]}
        for name, run in arms.items()
    }
    names = list(keys)
    shared = set(keys[names[0]])
    for n in names[1:]:
        shared &= set(keys[n])
    matched = {
        "shared_episode_index_keys": len(shared),
        "identical_signature_code_bodyhash": sum(
            1 for k in shared if len({keys[n][k] for n in names}) == 1
        ),
        "arms": names,
        "per_arm_span_counts": {n: len(keys[n]) for n in names},
        "all_arms_observed_identical_task_instances": all(
            len({keys[n][k] for n in names}) == 1 for k in shared
        ),
    }
    hashes["matched_task_instances_check.json"] = write_json(
        ARTIFACT_DIR / "matched_task_instances_check.json", matched
    )

    print("[8/8] derived measurements", flush=True)
    derived: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "generated_at_unix": int(t0),
        "design": {
            "episodes_per_arm": EPISODES,
            "spans_per_episode": SPANS_PER_EPISODE,
            "main_novelty_rate": MAIN_NOVELTY_RATE,
            "expected_codes": EXPECTED_CODES,
            "cost_units": {"compile": 1, "machinery": 1, "model": 1, "execution": 1},
            "success_threshold": measure.SUCCESS_THRESHOLD,
            "tie_relative_threshold": measure.TIE_RELATIVE,
            "bootstrap_resamples": measure.BOOTSTRAP_RESAMPLES,
            "bootstrap_seed": measure.BOOTSTRAP_SEED,
        },
        "arms": {},
    }
    for name, run in arms.items():
        obj = run["obj"]
        det = measure.determinism(_witness_list(run))
        curve = measure.learning_curve(run["records"], run["witness_by_sig"])
        tiers = measure.novelty_tiers(run["records"], run["witness_by_sig"])
        derived["arms"][name] = {
            "ledger": obj.ledger.as_dict(EPISODES),
            "success_rate": success_rate(run["episodes"]),
            "success_episodes": sum(1 for r in run["episodes"] if r["code_ok"] and r["final_store_empty"]),
            "determinism": det,
            "determinism_histogram_of_witness_counts": measure.histogram(_witness_list(run)),
            "learning_curve": curve,
            "determinism_fraction_by_episode_10_20_30_40_50": {
                str(e): _cumulative_det_at(curve, e) for e in (10, 20, 30, 40, 50)
            },
            "residual_novelty": tiers,
            "span_signature_diversity": len(run["witness_by_sig"]),
            "determinism_vs_compilability": _compilability(run["records"]),
            "model_calls_per_episode": [r["model_calls"] for r in run["episodes"]],
            "compile_events_per_episode": [r.get("compile_events", 0) for r in run["episodes"]],
            "compiled_replays_per_episode": [r.get("compiled_replays", 0) for r in run["episodes"]],
            "episode_amortized_cost_units": episode_costs(run["episodes"]),
            "decision_path_counts": _decision_paths(run["records"]),
        }
        if name == "B-INHERITED-SPIDER":
            derived["arms"][name]["registry_after_run"] = obj.registry_dump()
            derived["arms"][name]["kernel_config"] = obj.kernel_config
            derived["arms"][name]["mechanisms_distilled"] = obj.mechanisms_distilled
            derived["arms"][name]["distill_calls"] = obj.distill_calls
        if name == "B-NO-MEMORY-DETERMINISTIC":
            derived["arms"][name]["compiled_cache_entries"] = len(obj.cache)
            derived["arms"][name]["compiled_entries"] = sum(1 for e in obj.cache.values() if e.compiled_at_episode >= 0)
            derived["arms"][name]["ambiguous_cache_keys"] = sum(1 for e in obj.cache.values() if e.ambiguous)
            derived["arms"][name]["conflicts_detected"] = obj.conflicts_detected
            derived["arms"][name]["compiled_complete_at_episode"] = obj.compiled_complete_at_episode
            derived["arms"][name]["model_calls_strictly_after_compile_complete"] = obj.model_calls_after_compile_complete
            derived["arms"][name]["ambiguous_state_keys_detail"] = [
                {"state_sig": k, "first_request": e.request, "witnesses": e.witnesses}
                for k, e in obj.cache.items()
                if e.ambiguous
            ]

    c_d = derived["arms"]["B-NO-MEMORY-DETERMINISTIC"]["ledger"]["amortized_cost_units_per_episode"]
    c_i = derived["arms"]["B-INHERITED-SPIDER"]["ledger"]["amortized_cost_units_per_episode"]
    c_c = derived["arms"]["B-COLD-EXPLORATION"]["ledger"]["amortized_cost_units_per_episode"]
    s_d = derived["arms"]["B-NO-MEMORY-DETERMINISTIC"]["success_rate"]
    s_i = derived["arms"]["B-INHERITED-SPIDER"]["success_rate"]
    s_c = derived["arms"]["B-COLD-EXPLORATION"]["success_rate"]

    derived["matched_task_instances_check"] = matched
    derived["decision_rule"] = measure.classify_outcome(c_d, c_i, c_c, s_d, s_i, s_c)
    derived["cost_differences_bootstrap"] = {
        "deopt_minus_inherited": measure.bootstrap_cost_difference(
            derived["arms"]["B-NO-MEMORY-DETERMINISTIC"]["episode_amortized_cost_units"],
            derived["arms"]["B-INHERITED-SPIDER"]["episode_amortized_cost_units"],
        ),
        "deopt_minus_cold": measure.bootstrap_cost_difference(
            derived["arms"]["B-NO-MEMORY-DETERMINISTIC"]["episode_amortized_cost_units"],
            derived["arms"]["B-COLD-EXPLORATION"]["episode_amortized_cost_units"],
        ),
    }
    derived["primary_estimand"] = {
        "name": "per_span_witnessed_determinism_fraction",
        "measurement_arm": "B-NO-MEMORY-DETERMINISTIC",
        "note": (
            "Identical arm-plan and identical task instances across all three arms, so the span "
            "population is the same; the deopt arm is used as the measurement instrument because it "
            "is the only arm whose action selection is not gated by the incumbent kernel."
        ),
        "value": derived["arms"]["B-NO-MEMORY-DETERMINISTIC"]["determinism"]["determinism_fraction"],
        "wilson_ci95": derived["arms"]["B-NO-MEMORY-DETERMINISTIC"]["determinism"]["wilson_ci95"],
        "prereg_H1_threshold": 0.70,
        "prereg_H1_met": (
            derived["arms"]["B-NO-MEMORY-DETERMINISTIC"]["determinism"]["determinism_fraction"] >= 0.70
        ),
        "per_arm_cross_check": {
            k: v["determinism"]["determinism_fraction"] for k, v in derived["arms"].items()
        },
    }
    hashes["derived_metrics.json"] = write_json(ARTIFACT_DIR / "derived_metrics.json", derived)

    manifest = {
        "experiment_id": EXPERIMENT_ID,
        "python": sys.version,
        "platform": platform.platform(),
        "cwd": str(REPO_ROOT),
        "git_head": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True
        ).stdout.strip(),
        "git_status_porcelain": subprocess.run(
            ["git", "status", "--porcelain"], cwd=REPO_ROOT, capture_output=True, text=True
        ).stdout.strip(),
        "wall_time_seconds": round(time.time() - t0, 3),
        "artifact_sha256": hashes,
        "code_paths": [
            "research/frontier/substrate_deterministic_http.py",
            "research/frontier/taskplan.py",
            "research/frontier/measure.py",
            "research/frontier/arms/__init__.py",
            "research/frontier/arms/common.py",
            "research/frontier/arms/deopt_ratchet.py",
            "research/frontier/arms/inherited_spider.py",
            "research/frontier/arms/cold_exploration.py",
            "research/frontier/run_experiment_EXP_FRONTIER_36249071934.py",
        ],
        "shipped_kernel_imported_unmodified": ["src/spider/kernel.py", "src/spider/models.py", "src/spider/registry.py"],
    }
    hashes["run_manifest.json"] = write_json(ARTIFACT_DIR / "run_manifest.json", manifest)

    print(json.dumps(derived["decision_rule"], indent=2), flush=True)
    print("done in %.1fs" % (time.time() - t0), flush=True)
    return 0


def _compilability(records: list[dict[str, Any]]) -> dict[str, Any]:
    """prereg.md 7.1/7.4 -- split span occurrences by whether the frozen
    determinism rule marks them deterministic AND whether the no-memory ratchet
    could actually serve them from a compiled state->action entry.

    The gap between "deterministic" and "served by compiled replay" is the
    measured compilability boundary and is reported, not smoothed over.
    """
    det = [r for r in records if r["final_witnesses"] >= 2]
    served = [r for r in det if not r["decision_path"].startswith("DEOPT")]
    not_served = [r for r in det if r["decision_path"].startswith("DEOPT")]
    total = len(records)
    return {
        "total_span_occurrences": total,
        "deterministic_occurrences": len(det),
        "deterministic_fraction": len(det) / total if total else None,
        "served_by_compiled_replay": len(served),
        "deterministic_but_deopted": len(not_served),
        "compilable_given_deterministic": (len(served) / len(det)) if det else None,
        "compiled_share_of_all_spans": len(served) / total if total else None,
        "deterministic_but_deopted_by_role_workitem": _tally(
            (r["role"], r["work_item"]) for r in not_served
        ),
        "deterministic_but_deopted_cache_ambiguous": sum(
            1 for r in not_served if r["detail"].get("cache_ambiguous")
        ),
        "deterministic_but_deopted_cache_entry_absent": sum(
            1 for r in not_served if not r["detail"].get("cache_ambiguous")
        ),
    }


def _tally(values: Any) -> dict[str, int]:
    out: dict[str, int] = {}
    for v in values:
        key = "|".join(str(x) for x in v)
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items()))


def _decision_paths(records: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in records:
        out[r["decision_path"]] = out.get(r["decision_path"], 0) + 1
    return dict(sorted(out.items()))


if __name__ == "__main__":
    raise SystemExit(main())
