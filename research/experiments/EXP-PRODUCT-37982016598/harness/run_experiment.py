"""EXECUTE harness for EXP-PRODUCT-37982016598.

Frozen design: real credential-free localhost stdlib-HTTP substrate, four task
families (items/users/orders/products), four novelty levels (L0 001-005,
L1 006-010, L2 011-015, L3 016-020), arms
T-SPIDER-PARAM / B-COLD-RE-DERIVE / B-RETRIEVAL-SHAPED / B-EMPTIED-REGISTRY,
positive control PC-EXACT-REPLAY, 20 known-negative refusal cases, and a
dynamic-range certification.

IMPORTANT EXECUTION-BASE FACT (discovered by this stage, recorded as raw
evidence): the audited treatment carrier -- src/spider/kernel.py blob
b15ed848 / sha256 718efa6a (the parameterized ``distill_parameterized`` path)
-- was silently overwritten on this branch by merge commit 5601ede3 with the
pre-parameterization blob cfec9866.  The frozen design requires
``kernel.distill_parameterized``; the shipped path at the execution base does
not contain it.  To keep the run faithful to the FROZEN carrier identity, the
audited revision is vendored verbatim into ``harness/audited_spider`` (blob
b15ed848, sha256 718efa6a) and used for the treatment arm.  The shipped-path
regression is reported as a first-class validity finding; the shipped path is
probed directly and the probe result is preserved.

Raw evidence is written separately from derived measurements.  No model,
browser, external network, or credential is used.  JSON only.

Run:
    python3 research/experiments/EXP-PRODUCT-37982016598/harness/run_experiment.py
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
EXPERIMENT_DIR = HERE.parent.parent
REPO_ROOT = EXPERIMENT_DIR.parents[2]
for candidate in (str(REPO_ROOT / "src"), str(HERE.parent)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

import substrate as sub  # noqa: E402

# Audited carrier (frozen identity).  The shipped path regression is probed
# separately in probe_shipped_kernel().
from audited_spider.kernel import SpiderKernel, TrajectoryCounters, _support_accepts  # noqa: E402
from audited_spider.models import Observation, ResolutionStatus  # noqa: E402
from audited_spider.registry import MechanismRegistry  # noqa: E402

EXPERIMENT_ID = "EXP-PRODUCT-37982016598"
INTENT = "read"
NOVELTY_LEVELS = [0.0, 0.25, 0.5, 0.75]

COUNTER_FIELDS = (
    "model_calls", "model_tokens", "browser_actions", "http_requests",
    "retrieval_calls", "verification_calls", "repair_attempts", "latency_ms",
)
# Frozen composite cost per prereg section 7.
COMPOSITE_FIELDS = ("http_requests", "verification_calls", "repair_attempts")


# --------------------------------------------------------------------------
# io helpers
# --------------------------------------------------------------------------


def write_json(path: Path, payload: object) -> tuple[str, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, indent=2, sort_keys=False).encode("utf-8")
    path.write_bytes(data)
    return str(path.relative_to(REPO_ROOT)), hashlib.sha256(data).hexdigest()


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> tuple[str, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)
    data = text.encode("utf-8")
    path.write_bytes(data)
    return str(path.relative_to(REPO_ROOT)), hashlib.sha256(data).hexdigest()


class LoggingCounters(TrajectoryCounters):
    """TrajectoryCounters that records every genuine increment as an event."""

    def __init__(self, task_id: str, arm: str, sink: list[dict[str, Any]]) -> None:
        super().__init__()
        self._task_id = task_id
        self._arm = arm
        self._sink = sink

    def add(self, field: str, amount: float = 1) -> None:
        super().add(field, amount)
        self._sink.append({
            "task_id": self._task_id,
            "arm": self._arm,
            "counter": field,
            "amount": float(amount),
            "ts_ns": time.monotonic_ns(),
            "injected": False,
        })


def stable_context(rtype: str, base_url: str) -> dict[str, Any]:
    return {"resource_type": rtype, "site": base_url, "auth": "public"}


def flatten_keys(obj: Any, prefix: tuple[str, ...] = ()) -> set[tuple[str, ...]]:
    keys: set[tuple[str, ...]] = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            keys |= flatten_keys(value, prefix + (str(key),))
    elif isinstance(obj, (list, tuple)):
        for index, value in enumerate(obj):
            keys |= flatten_keys(value, prefix + (str(index),))
    else:
        if prefix:
            keys.add(prefix)
    return keys


def jaccard(a: set[Any], b: set[Any]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    return len(a & b) / len(union) if union else 1.0


# --------------------------------------------------------------------------
# shipped-path probe (first-class validity evidence)
# --------------------------------------------------------------------------


def probe_shipped_kernel() -> dict[str, Any]:
    """Directly probe the *shipped* src/spider/kernel.py for the frozen API."""
    import importlib
    probe: dict[str, Any] = {"shipped_import": None, "features": {}, "api_complete": None}
    try:
        import spider.kernel as shipped  # noqa: F401
        importlib.reload(shipped)
    except Exception as exc:  # pragma: no cover
        probe["shipped_import"] = f"ERROR:{type(exc).__name__}:{exc}"
        probe["api_complete"] = False
        return probe
    probe["shipped_import"] = "ok"
    probe["shipped_file"] = str(Path(shipped.__file__).relative_to(REPO_ROOT))
    probe["features"] = {
        "distill_parameterized": hasattr(shipped.SpiderKernel, "distill_parameterized"),
        "TrajectoryCounters": hasattr(shipped, "TrajectoryCounters"),
        "_support_accepts": hasattr(shipped, "_support_accepts"),
        "rebind": hasattr(shipped.SpiderKernel, "rebind"),
    }
    probe["api_complete"] = all(probe["features"].values())
    return probe


# --------------------------------------------------------------------------
# training observations (real HTTP)
# --------------------------------------------------------------------------


def collect_training_observations(client: sub.SubstrateClient, base_url: str) -> dict[str, list[Observation]]:
    by_type: dict[str, list[Observation]] = {t: [] for t in sub.TRAINING_TYPES}
    for rtype in sub.TRAINING_TYPES:
        for rid in [f"{sub.ID_PREFIX[rtype]}-{i:03d}" for i in sub.TRAIN_RANGE]:
            action = {
                "method": "GET",
                "url": f"{base_url}/api/{rtype}/{rid}",
                "headers": {"Accept": "application/json"},
            }
            response = client.execute(action)
            body = response.get("body") if isinstance(response.get("body"), dict) else {}
            next_state = {"status": response.get("status"), **body}
            obs = Observation(
                intent=INTENT,
                state=stable_context(rtype, base_url),
                action=action,
                next_state=next_state,
                success=sub.is_success_response(response, rtype, rid),
                provenance={"phase": "training", "resource_type": rtype, "identifier": rid},
            )
            by_type[rtype].append(obs)
    return by_type


# --------------------------------------------------------------------------
# task bank
# --------------------------------------------------------------------------


def build_task_bank() -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for rtype in sub.TRAINING_TYPES:
        for novelty in NOVELTY_LEVELS:
            for rid in sub.ids_for(rtype, novelty):
                tasks.append({
                    "task_id": f"{rtype}::L{novelty}::{rid}",
                    "family": rtype,
                    "resource_type": rtype,
                    "novelty_fraction": novelty,
                    "identifier": rid,
                    "intent": INTENT,
                })
    return tasks


# --------------------------------------------------------------------------
# arms
# --------------------------------------------------------------------------


def cold_action(base_url: str, rtype: str, rid: str) -> dict[str, Any]:
    return {
        "method": "GET",
        "url": f"{base_url}/api/{rtype}/{rid}",
        "headers": {"Accept": "application/json"},
    }


def run_treatment_arm(client: sub.SubstrateClient, base_url: str, registry: MechanismRegistry,
                      mechanisms: dict[str, Any], tasks: list[dict[str, Any]], label: str,
                      event_sink: list[dict[str, Any]],
                      fallback_to_cold: bool = False) -> list[dict[str, Any]]:
    """T-SPIDER-PARAM / PC-EXACT-REPLAY / B-EMPTIED-REGISTRY code path."""
    rows: list[dict[str, Any]] = []
    for task in tasks:
        rtype = task["resource_type"]
        rid = task["identifier"]
        wiki_task_id = f"{label}::{task['task_id']}"
        mech = mechanisms.get(rtype)
        slots = list(mech.parameter_slots) if mech else []
        counters = LoggingCounters(wiki_task_id, label, event_sink)
        kernel = SpiderKernel(registry, min_confidence=0.8, counters=counters)
        context = stable_context(rtype, base_url)
        params = {slots[0]: rid} if slots else {}
        t0 = time.perf_counter()
        resolution = kernel.resolve(INTENT, context, params)
        bound_action = resolution.bound_action if resolution.status == ResolutionStatus.EXECUTABLE else None
        fell_back = False
        if bound_action is None and fallback_to_cold:
            bound_action = cold_action(base_url, rtype, rid)
            fell_back = True
        response = None
        verified = False
        success = False
        if bound_action is not None:
            counters.add("http_requests")
            response = client.execute(bound_action)
            body = response.get("body") if isinstance(response.get("body"), dict) else {}
            observed_state = {"status": response.get("status"), **body}
            if fell_back:
                counters.add("verification_calls")
                verified = sub.is_success_response(response, rtype, rid)
            else:
                verified = kernel.verify(mech.mechanism_id, observed_state, params)
            success = verified and sub.is_success_response(response, rtype, rid)
        counters.add("latency_ms", (time.perf_counter() - t0) * 1000.0)
        rows.append({
            "task_id": wiki_task_id,
            "bank_task_id": task["task_id"],
            "family": task["family"],
            "resource_type": rtype,
            "identifier": rid,
            "novelty_fraction": task["novelty_fraction"],
            "arm": label,
            "intent": INTENT,
            "context": context,
            "params": params,
            "mechanism_id": mech.mechanism_id if mech else None,
            "parameter_slots": slots,
            "resolution_status": resolution.status.value,
            "resolution_reason": resolution.reason,
            "fell_back_to_cold": fell_back,
            "bound_action": bound_action,
            "executed_response": response,
            "verify_true": verified,
            "success": success,
            "counters": counters.as_dict(),
        })
    return rows


def run_cold_arm(client: sub.SubstrateClient, base_url: str, tasks: list[dict[str, Any]],
                 event_sink: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in tasks:
        rtype = task["resource_type"]
        rid = task["identifier"]
        task_id = f"B-COLD-RE-DERIVE::{task['task_id']}"
        counters = LoggingCounters(task_id, "B-COLD-RE-DERIVE", event_sink)
        action = cold_action(base_url, rtype, rid)
        t0 = time.perf_counter()
        counters.add("http_requests")
        response = client.execute(action)
        counters.add("verification_calls")
        success = sub.is_success_response(response, rtype, rid)
        counters.add("latency_ms", (time.perf_counter() - t0) * 1000.0)
        rows.append({
            "task_id": task_id,
            "bank_task_id": task["task_id"],
            "family": task["family"],
            "resource_type": rtype,
            "identifier": rid,
            "novelty_fraction": task["novelty_fraction"],
            "arm": "B-COLD-RE-DERIVE",
            "intent": INTENT,
            "constructed_action": action,
            "executed_response": response,
            "verify_true": success,
            "success": success,
            "counters": counters.as_dict(),
        })
    return rows


def _retrieve_topk(intent: str, context: dict[str, Any], observations: list[Observation], k: int = 3) -> list[Observation]:
    target = {("intent", intent)} | {("state",) + p for p in flatten_keys(context)}
    candidates = [o for o in observations if o.state.get("resource_type") == context.get("resource_type")]
    ranked = sorted(
        ((jaccard(target, {("intent", o.intent)} | {("state",) + p for p in flatten_keys(o.state)}
                  | {("action",) + p for p in flatten_keys(o.action)}), idx, o)
         for idx, o in enumerate(candidates)),
        key=lambda item: (-item[0], item[1]),
    )
    return [obs for _, _, obs in ranked[:k]]


def bind_slot_alignment(actions: list[dict[str, Any]], rid: str) -> dict[str, Any]:
    urls = [a.get("url", "") for a in actions]
    parts = [u.split("/") for u in urls]
    idx = None
    if parts and all(len(p) == len(parts[0]) for p in parts):
        varying = [i for i in range(len(parts[0])) if len({p[i] for p in parts}) > 1]
        if varying:
            idx = varying[-1]
    if idx is None:
        out_parts = list(parts[0])
        out_parts[-1] = rid
    else:
        out_parts = list(parts[0])
        out_parts[idx] = rid
    bound = dict(actions[0])
    bound["url"] = "/".join(out_parts)
    return bound


def run_retrieval_arm(client: sub.SubstrateClient, base_url: str, training: list[Observation],
                      tasks: list[dict[str, Any]], event_sink: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in tasks:
        rtype = task["resource_type"]
        rid = task["identifier"]
        task_id = f"B-RETRIEVAL-SHAPED::{task['task_id']}"
        counters = LoggingCounters(task_id, "B-RETRIEVAL-SHAPED", event_sink)
        context = stable_context(rtype, base_url)
        t0 = time.perf_counter()
        topk = _retrieve_topk(INTENT, context, training, k=3)
        counters.add("retrieval_calls", 3)
        bound_action = bind_slot_alignment([o.action for o in topk], rid) if topk else None
        response = None
        success = False
        if bound_action is not None:
            counters.add("http_requests")
            response = client.execute(bound_action)
            counters.add("verification_calls")
            success = sub.is_success_response(response, rtype, rid)
        counters.add("latency_ms", (time.perf_counter() - t0) * 1000.0)
        rows.append({
            "task_id": task_id,
            "bank_task_id": task["task_id"],
            "family": task["family"],
            "resource_type": rtype,
            "identifier": rid,
            "novelty_fraction": task["novelty_fraction"],
            "arm": "B-RETRIEVAL-SHAPED",
            "intent": INTENT,
            "retrieved_observation_intents": [o.intent for o in topk],
            "bound_action": bound_action,
            "executed_response": response,
            "verify_true": success,
            "success": success,
            "counters": counters.as_dict(),
        })
    return rows


# --------------------------------------------------------------------------
# known negatives
# --------------------------------------------------------------------------


def build_known_negative_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for rtype in sub.TRAINING_TYPES:
        prefix = sub.ID_PREFIX[rtype]
        cases.append({"case_id": f"KN-OOS::{rtype}", "category": "out_of_support",
                      "resource_type": rtype, "identifier": f"{prefix}-999"})
        cases.append({"case_id": f"KN-MISSING::{rtype}", "category": "missing_parameter",
                      "resource_type": rtype, "identifier": None})
        cases.append({"case_id": f"KN-WRONGINTENT::{rtype}", "category": "wrong_intent",
                      "resource_type": rtype, "identifier": sub.ALL_IDS[rtype][0], "intent": "delete"})
        cases.append({"case_id": f"KN-UNSEENTYPE::{rtype}", "category": "unseen_type",
                      "resource_type": "invoices", "identifier": "invoice-001"})
        cases.append({"case_id": f"KN-MALFORMED::{rtype}", "category": "malformed_body",
                      "resource_type": rtype, "identifier": "bad/../id"})
    return cases


def run_known_negatives_shipped_registry(mechanisms: dict[str, Any],
                                         event_sink: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Kernel-path refusal test (T-SPIDER-PARAM path) for declared negatives."""
    registry_path = Path(tempfile.mkdtemp()) / "known_neg.jsonl"
    registry = MechanismRegistry(registry_path)
    for mech in mechanisms.values():
        if mech is not None:
            registry.upsert(mech)
    kernel = SpiderKernel(registry, min_confidence=0.8)
    out: list[dict[str, Any]] = []
    for case in build_known_negative_cases():
        rtype = case["resource_type"]
        mech = mechanisms.get(rtype)
        slot = mech.parameter_slots[0] if mech and mech.parameter_slots else "id"
        context = stable_context(rtype, "http://127.0.0.1:0")
        intent = case.get("intent", INTENT)
        if case["category"] == "missing_parameter":
            params: dict[str, Any] = {}
        elif case["category"] == "malformed_body":
            params = {slot: case["identifier"]}
        elif case["category"] == "unseen_type":
            params = {"invoice": case["identifier"]}
        else:
            params = {slot: case["identifier"]}
        resolution = kernel.resolve(intent, context, params)
        refused = (
            resolution.status != ResolutionStatus.EXECUTABLE
            and resolution.bound_action is None
            and bool(resolution.reason)
        )
        out.append({
            "case_id": case["case_id"],
            "category": case["category"],
            "resource_type": rtype,
            "intent": intent,
            "params": params,
            "resolution_status": resolution.status.value,
            "resolution_reason": resolution.reason,
            "bound_action": resolution.bound_action,
            "refused": refused,
            "arm": "T-SPIDER-PARAM",
        })
    return out


# --------------------------------------------------------------------------
# dynamic range certification + aggregation
# --------------------------------------------------------------------------


def arm_metrics_by_level(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for novelty in NOVELTY_LEVELS:
        sel = [r for r in rows if r["novelty_fraction"] == novelty]
        n = len(sel)
        n_success = sum(1 for r in sel if r["success"])
        total_cost = sum(sum(float(r["counters"].get(f, 0.0)) for f in COMPOSITE_FIELDS) for r in sel)
        out[str(novelty)] = {
            "n_tasks": n,
            "n_success": n_success,
            "success_rate": (n_success / n) if n else 0.0,
            "total_composite_cost": total_cost,
            "cost_per_success": (total_cost / n_success) if n_success else None,
        }
    return out


def certify_dynamic_range(cold_by_level: dict[str, Any], retr_by_level: dict[str, Any]) -> dict[str, Any]:
    details: dict[str, Any] = {}
    passes = False
    certified_at = None
    for novelty in (0.5, 0.75):
        c = cold_by_level.get(str(novelty), {})
        r = retr_by_level.get(str(novelty), {})
        c_rate = c.get("success_rate")
        r_rate = r.get("success_rate")
        ok = (c_rate is not None and r_rate is not None and c_rate < 0.95 and r_rate < 0.95)
        details[str(novelty)] = {"cold_success_rate": c_rate, "retrieval_success_rate": r_rate, "pass": ok}
        if ok:
            passes = True
            certified_at = novelty
    return {
        "certified": passes,
        "cold_max_success_rate": max((v["success_rate"] for v in cold_by_level.values()), default=None),
        "retrieval_max_success_rate": max((v["success_rate"] for v in retr_by_level.values()), default=None),
        "certified_at_novelty": certified_at,
        "per_level": details,
    }


# --------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------


def spearman(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n < 3:
        return None

    def rank(vals: list[float]) -> list[float]:
        order = sorted(range(n), key=lambda i: vals[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[order[k]] = avg
            i = j + 1
        return ranks

    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def permutation_p_value(xs: list[float], ys: list[float], n_perm: int = 10000, seed: int = 42) -> float | None:
    obs = spearman(xs, ys)
    if obs is None:
        return None
    rng = random.Random(seed)
    n = len(xs)
    count = 0
    for _ in range(n_perm):
        perm = list(xs)
        rng.shuffle(perm)
        rho = spearman(perm, ys)
        if rho is not None and rho >= obs:
            count += 1
    return (count + 1) / (n_perm + 1)


def paired_permutation_p(a: list[float], b: list[float], n_perm: int = 10000, seed: int = 42) -> float | None:
    """One-sided paired permutation test for mean(a) < mean(b)."""
    diffs = [a[i] - b[i] for i in range(len(a))]
    if not diffs:
        return None
    obs = sum(diffs) / len(diffs)
    rng = random.Random(seed)
    count = 0
    for _ in range(n_perm):
        stat = sum(abs(d) * (1 if rng.random() < 0.5 else -1) for d in diffs) / len(diffs)
        if stat <= obs:
            count += 1
    return (count + 1) / (n_perm + 1)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------


def main() -> int:
    raw_dir = EXPERIMENT_DIR / "raw_evidence"
    derived_dir = EXPERIMENT_DIR / "derived"
    artifacts: list[dict[str, str]] = []

    server = sub.SubstrateServer()
    server.start()
    client = sub.SubstrateClient(server.base_url)
    counter_events: list[dict[str, Any]] = []

    try:
        shipped_probe = probe_shipped_kernel()
        p, h = write_json(raw_dir / "shipped_kernel_probe.json", shipped_probe)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})

        training_by_type = collect_training_observations(client, server.base_url)
        training_all = [o for t in sub.TRAINING_TYPES for o in training_by_type[t]]
        training_rows = [
            {
                "resource_type": o.state["resource_type"],
                "identifier": o.provenance["identifier"],
                "intent": o.intent,
                "state": o.state,
                "action": o.action,
                "next_state": o.next_state,
                "success": o.success,
            }
            for o in training_all
        ]
        p, h = write_jsonl(raw_dir / "training_observations.jsonl", training_rows)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})

        # Induction (audited carrier).
        registry_path = Path(tempfile.mkdtemp()) / "treatment.jsonl"
        registry = MechanismRegistry(registry_path)
        mechanisms: dict[str, Any] = {}
        for rtype in sub.TRAINING_TYPES:
            mech = SpiderKernel(registry, min_confidence=0.8).distill_parameterized(training_by_type[rtype])
            mechanisms[rtype] = mech
            if mech is not None:
                registry.upsert(mech)

        mechanisms_summary = {
            rtype: (
                {
                    "mechanism_id": mechanisms[rtype].mechanism_id,
                    "intent": mechanisms[rtype].intent,
                    "parameter_slots": list(mechanisms[rtype].parameter_slots),
                    "action_template": mechanisms[rtype].action_template,
                    "preconditions": mechanisms[rtype].preconditions,
                    "postconditions": mechanisms[rtype].postconditions,
                    "parameter_supports": mechanisms[rtype].verification_rule.get("parameter_supports", {}),
                    "confidence": mechanisms[rtype].confidence,
                }
                if mechanisms[rtype] is not None
                else None
            )
            for rtype in sub.TRAINING_TYPES
        }
        p, h = write_json(raw_dir / "induced_mechanisms.json", mechanisms_summary)
        artifacts.append({"path": p, "sha256": h, "role": "derived"})

        bank = build_task_bank()

        # Frozen arms.
        treatment = run_treatment_arm(client, server.base_url, registry, mechanisms, bank,
                                      "T-SPIDER-PARAM", counter_events)
        cold = run_cold_arm(client, server.base_url, bank, counter_events)
        retrieval = run_retrieval_arm(client, server.base_url, training_all, bank, counter_events)

        empty_registry = MechanismRegistry(Path(tempfile.mkdtemp()) / "empty.jsonl")
        emptied = run_treatment_arm(client, server.base_url, empty_registry, mechanisms, bank,
                                    "B-EMPTIED-REGISTRY", counter_events, fallback_to_cold=True)

        train_tasks = [
            {"task_id": f"{t}::L0::{rid}", "family": t, "resource_type": t,
             "novelty_fraction": 0.0, "identifier": rid, "intent": INTENT}
            for t in sub.TRAINING_TYPES
            for rid in [f"{sub.ID_PREFIX[t]}-{i:03d}" for i in sub.TRAIN_RANGE]
        ]
        pc_replay = run_treatment_arm(client, server.base_url, registry, mechanisms, train_tasks,
                                      "PC-EXACT-REPLAY", counter_events)

        known_neg = run_known_negatives_shipped_registry(mechanisms, counter_events)

        all_rows = treatment + cold + retrieval + emptied + pc_replay
        p, h = write_jsonl(raw_dir / "task_trajectories.jsonl", all_rows)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})
        p, h = write_jsonl(raw_dir / "accounting_counters.jsonl", counter_events)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})
        p, h = write_jsonl(raw_dir / "known_negatives.jsonl", known_neg)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})
        p, h = write_jsonl(raw_dir / "server_log.jsonl", server.request_log)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})

        # Per-arm metrics (aggregate + by novelty level).
        arm_rows = {
            "T-SPIDER-PARAM": treatment,
            "B-COLD-RE-DERIVE": cold,
            "B-RETRIEVAL-SHAPED": retrieval,
            "B-EMPTIED-REGISTRY": emptied,
            "PC-EXACT-REPLAY": pc_replay,
        }
        arm_metrics: dict[str, Any] = {}
        for name, rows in arm_rows.items():
            n = len(rows)
            n_success = sum(1 for r in rows if r["success"])
            total_cost = sum(sum(float(r["counters"].get(f, 0.0)) for f in COMPOSITE_FIELDS) for r in rows)
            arm_metrics[name] = {
                "n_tasks": n,
                "n_success": n_success,
                "success_rate": (n_success / n) if n else 0.0,
                "counters_total": {f: sum(float(r["counters"].get(f, 0.0)) for r in rows) for f in COUNTER_FIELDS},
                "total_composite_cost": total_cost,
                "cost_per_success": (total_cost / n_success) if n_success else None,
                "by_novelty": arm_metrics_by_level(rows),
            }
        p, h = write_json(derived_dir / "arm_metrics.json", arm_metrics)
        artifacts.append({"path": p, "sha256": h, "role": "derived"})

        # Dynamic range certificate (observed post-hoc; NOT a pre-freeze certificate).
        dr = certify_dynamic_range(
            arm_metrics["B-COLD-RE-DERIVE"]["by_novelty"],
            arm_metrics["B-RETRIEVAL-SHAPED"]["by_novelty"],
        )
        p, h = write_json(derived_dir / "dynamic_range_cert.json", dr)
        artifacts.append({"path": p, "sha256": h, "role": "derived"})

        # Cost advantage vs novelty (primary C3/C4 inputs).
        novelty_levels = NOVELTY_LEVELS
        adv_cold: list[float] = []
        adv_retr: list[float] = []
        adv_nov: list[float] = []
        t_by = arm_metrics["T-SPIDER-PARAM"]["by_novelty"]
        c_by = arm_metrics["B-COLD-RE-DERIVE"]["by_novelty"]
        r_by = arm_metrics["B-RETRIEVAL-SHAPED"]["by_novelty"]
        for nov in novelty_levels:
            t_c = t_by[str(nov)]["cost_per_success"]
            c_c = c_by[str(nov)]["cost_per_success"]
            r_c = r_by[str(nov)]["cost_per_success"]
            if t_c is not None and c_c is not None:
                adv_cold.append(c_c - t_c)
                adv_nov.append(nov)
            if t_c is not None and r_c is not None:
                adv_retr.append(r_c - t_c)

        rho_cold = spearman(adv_nov, adv_cold) if len(adv_nov) >= 3 else None
        rho_retr = spearman(adv_nov, adv_retr) if len(adv_nov) >= 3 else None
        p_cold = permutation_p_value(adv_nov, adv_cold) if rho_cold is not None else None
        p_retr = permutation_p_value(adv_nov, adv_retr) if rho_retr is not None else None

        # C5 at highest novelty (>= 0.7): paired per-task composite cost among successes.
        def costs_at(nov: float, rows: list[dict[str, Any]]) -> list[float]:
            return [sum(float(r["counters"].get(f, 0.0)) for f in COMPOSITE_FIELDS)
                    for r in rows if r["novelty_fraction"] == nov and r["success"]]

        t_hi = costs_at(0.75, treatment)
        c_hi = costs_at(0.75, cold)
        r_hi = costs_at(0.75, retrieval)
        c5_cold = paired_permutation_p(t_hi, c_hi) if t_hi and c_hi and len(t_hi) == len(c_hi) else None
        c5_retr = paired_permutation_p(t_hi, r_hi) if t_hi and r_hi and len(t_hi) == len(r_hi) else None

        # Matched correctness C2: all 4 arms success_rate >= 0.80 on >= 3/4 levels.
        def matched_ok(metrics_by_level: dict[str, Any]) -> bool:
            good = sum(1 for nov in novelty_levels if metrics_by_level[str(nov)]["success_rate"] >= 0.80)
            return good >= 3

        c2_details = {
            name: {
                "pass_per_level": {str(nov): arm_metrics[name]["by_novelty"][str(nov)]["success_rate"] >= 0.80
                                   for nov in novelty_levels},
                "levels_ge_0.80": sum(1 for nov in novelty_levels
                                      if arm_metrics[name]["by_novelty"][str(nov)]["success_rate"] >= 0.80),
                "ok": matched_ok(arm_metrics[name]["by_novelty"]),
            }
            for name in ("T-SPIDER-PARAM", "B-COLD-RE-DERIVE", "B-RETRIEVAL-SHAPED", "B-EMPTIED-REGISTRY")
        }
        c2_pass = all(v["ok"] for v in c2_details.values())

        # Secondary S1: emptied-registry ~ cold at all levels.
        s1: dict[str, Any] = {}
        s1_pass = True
        for nov in novelty_levels:
            e = arm_metrics["B-EMPTIED-REGISTRY"]["by_novelty"][str(nov)]
            c = arm_metrics["B-COLD-RE-DERIVE"]["by_novelty"][str(nov)]
            same = (e["success_rate"] == c["success_rate"] and e["cost_per_success"] == c["cost_per_success"])
            s1[str(nov)] = {"emptied_success_rate": e["success_rate"], "cold_success_rate": c["success_rate"],
                            "emptied_cost_per_success": e["cost_per_success"],
                            "cold_cost_per_success": c["cost_per_success"], "indistinguishable": same}
            s1_pass = s1_pass and same

        refusal_rate = (sum(1 for c in known_neg if c["refused"]) / len(known_neg)) if known_neg else 0.0
        s3_pass = refusal_rate >= 0.95

        # ---- frozen decision rule evaluation ----
        frozen_certified = False  # FROM FROZEN spec.json (immutable)
        c1_pass = bool(frozen_certified) and bool(dr["certified"])
        c3_pass = (rho_cold is not None and rho_cold > 0.5 and p_cold is not None and p_cold < 0.05)
        c4_pass = (rho_retr is not None and rho_retr > 0.5 and p_retr is not None and p_retr < 0.05)
        c5_pass = bool(
            c5_cold is not None and c5_cold < 0.05
            and c5_retr is not None and c5_retr < 0.05
            and t_hi and c_hi and r_hi
            and (sum(t_hi) / len(t_hi)) < (sum(c_hi) / len(c_hi))
            and (sum(t_hi) / len(t_hi)) < (sum(r_hi) / len(r_hi))
        )

        primary_conditions = {
            "C1_dynamic_range_certified": {"pass": c1_pass,
                                            "frozen_spec_field": frozen_certified,
                                            "observed_certified": dr["certified"],
                                            "note": "C1 is bound by prereg s6 to spec.json.dynamic_range_certified==true, frozen false."},
            "C2_matched_correctness": {"pass": c2_pass, "details": c2_details},
            "C3_spearman_cold": {"pass": c3_pass, "rho": rho_cold, "perm_p": p_cold, "n_levels": len(adv_nov)},
            "C4_spearman_retrieval": {"pass": c4_pass, "rho": rho_retr, "perm_p": p_retr, "n_levels": len(adv_nov)},
            "C5_advantage_at_high_novelty": {"pass": c5_pass, "treatment_costs": t_hi,
                                             "cold_costs": c_hi, "retrieval_costs": r_hi,
                                             "p_cold": c5_cold, "p_retrieval": c5_retr},
        }
        primary_pass = all(v["pass"] for v in primary_conditions.values())

        # Frozen mapping: C1 failure is explicitly MEASUREMENT_INVALID (prereg s5,
        # spec falsifier clause 3).  C2 failure with valid measurement is FALSIFIES.
        if not c1_pass:
            status, outcome = "MEASUREMENT_INVALID", "NOT_APPLICABLE"
        elif not c2_pass:
            status, outcome = "COMPLETE", "FALSIFIES"
        elif primary_pass:
            status, outcome = "COMPLETE", "SUPPORTS"
        else:
            status, outcome = "COMPLETE", "FALSIFIES"

        accounting_models = sum(
            arm_metrics[n]["counters_total"]["model_calls"] + arm_metrics[n]["counters_total"]["model_tokens"]
            for n in arm_rows
        )
        any_injected = any(row["injected"] for row in counter_events)

        decision_eval = {
            "frozen_certified_field": frozen_certified,
            "observed_dynamic_range_certificate": dr,
            "primary_conditions": primary_conditions,
            "primary_pass": primary_pass,
            "secondary": {
                "S1_emptied_matches_cold": {"pass": s1_pass, "by_level": s1},
                "S2_positive_control": {"pass": arm_metrics["PC-EXACT-REPLAY"]["success_rate"] == 1.0,
                                        "success_rate": arm_metrics["PC-EXACT-REPLAY"]["success_rate"]},
                "S3_known_negative_refusal": {"pass": s3_pass, "refusal_rate": refusal_rate,
                                              "n": len(known_neg),
                                              "scope_note": "kernel-path refusal only; direct-construction arms cannot refuse by construction"},
                "S4_support_boundary": mechanisms_summary,
            },
            "accounting": {"model_calls_plus_tokens_total": accounting_models,
                           "any_injected_counter_event": any_injected},
            "shipped_kernel_probe": shipped_probe,
            "status": status,
            "outcome": outcome,
        }
        p, h = write_json(derived_dir / "decision_rule_eval.json", decision_eval)
        artifacts.append({"path": p, "sha256": h, "role": "derived"})

        summary = {
            "experiment_id": EXPERIMENT_ID,
            "status": status,
            "outcome": outcome,
            "arm_success_rates": {k: v["success_rate"] for k, v in arm_metrics.items()},
            "arm_cost_per_success": {k: v["cost_per_success"] for k, v in arm_metrics.items()},
            "observed_dynamic_range_certificate": dr,
            "shipped_kernel_api_complete": shipped_probe["api_complete"],
            "server_requests": len(server.request_log),
            "artifacts": artifacts,
        }
        print(json.dumps(summary, indent=2))
        return 0
    finally:
        server.stop()


if __name__ == "__main__":
    raise SystemExit(main())
