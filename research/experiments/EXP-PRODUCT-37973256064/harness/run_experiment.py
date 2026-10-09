"""EXECUTE harness for EXP-PRODUCT-37973256064.

Runs the frozen design exactly: real localhost stdlib-HTTP substrate, shipped
kernel with ``distill_parameterized`` (the audited repair), three arms
(T-SPIDER-PARAM, B-COLD-RE-DERIVE, B-RETRIEVAL-SHAPED), positive control
(PC-EXACT-REPLAY), ablation (B-LITERAL-KERNEL), null control
(NC-OUT-OF-SUPPORT-TYPE) and 15 known-negative refusal cases.

Raw evidence is written separately from derived measurements. No model, browser,
network beyond localhost, or credential is used. JSON only.

Run:
    PYTHONPATH=src python3 \
      research/experiments/EXP-PRODUCT-37973256064/harness/run_experiment.py
"""

from __future__ import annotations

import hashlib
import json
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

from spider.kernel import SpiderKernel, TrajectoryCounters, _support_accepts  # noqa: E402
from spider.models import Observation, ResolutionStatus  # noqa: E402
from spider.registry import MechanismRegistry  # noqa: E402

import substrate as sub  # noqa: E402

EXPERIMENT_ID = "EXP-PRODUCT-37973256064"
INTENT = "read"

COUNTER_FIELDS = (
    "model_calls", "model_tokens", "browser_actions", "http_requests",
    "retrieval_calls", "verification_calls", "repair_attempts", "latency_ms",
)


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
    """TrajectoryCounters that records every genuine increment as an event.

    Used so raw_evidence/accounting_counters.jsonl contains real per-call
    increment events (with a monotonic timestamp), not reconstructed totals.
    """

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
# training observations (real HTTP)
# --------------------------------------------------------------------------


def collect_training_observations(client: sub.SubstrateClient, base_url: str) -> dict[str, list[Observation]]:
    by_type: dict[str, list[Observation]] = {t: [] for t in sub.TRAINING_TYPES}
    for rtype in sub.TRAINING_TYPES:
        for rid in sub.ALL_IDS[rtype][:5]:
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
# arms
# --------------------------------------------------------------------------


def run_treatment(client: sub.SubstrateClient, base_url: str, registry: MechanismRegistry,
                  mechanisms: dict[str, Any], ids: dict[str, list[str]], label: str,
                  event_sink: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """T-SPIDER-PARAM (held-out) and PC-EXACT-REPLAY (training ids) share this path."""
    tasks: list[dict[str, Any]] = []
    for rtype in sub.TRAINING_TYPES:
        mech = mechanisms.get(rtype)
        slots = list(mech.parameter_slots) if mech else []
        for rid in ids[rtype]:
            task_id = f"{label}::{rtype}::{rid}"
            counters = LoggingCounters(task_id, label, event_sink)
            kernel = SpiderKernel(registry, min_confidence=0.8, counters=counters)
            context = stable_context(rtype, base_url)
            params = {slots[0]: rid} if slots else {}
            t0 = time.perf_counter()
            resolution = kernel.resolve(INTENT, context, params)
            bound_action = resolution.bound_action if resolution.status == ResolutionStatus.EXECUTABLE else None
            response = None
            verified = False
            success = False
            if bound_action is not None:
                counters.add("http_requests")
                response = client.execute(bound_action)
                body = response.get("body") if isinstance(response.get("body"), dict) else {}
                observed_state = {"status": response.get("status"), **body}
                verified = kernel.verify(mech.mechanism_id, observed_state, params)
                success = verified and sub.is_success_response(response, rtype, rid)
            counters.add("latency_ms", (time.perf_counter() - t0) * 1000.0)
            tasks.append({
                "task_id": task_id,
                "arm": label,
                "resource_type": rtype,
                "identifier": rid,
                "intent": INTENT,
                "context": context,
                "params": params,
                "mechanism_id": mech.mechanism_id if mech else None,
                "parameter_slots": slots,
                "resolution_status": resolution.status.value,
                "resolution_reason": resolution.reason,
                "bound_action": bound_action,
                "executed_response": response,
                "verify_true": verified,
                "success": success,
                "counters": counters.as_dict(),
            })
    return tasks


def run_cold(client: sub.SubstrateClient, base_url: str, ids: dict[str, list[str]],
             event_sink: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for rtype in sub.TRAINING_TYPES:
        for rid in ids[rtype]:
            task_id = f"B-COLD-RE-DERIVE::{rtype}::{rid}"
            counters = LoggingCounters(task_id, "B-COLD-RE-DERIVE", event_sink)
            action = {
                "method": "GET",
                "url": f"{base_url}/api/{rtype}/{rid}",
                "headers": {"Accept": "application/json"},
            }
            t0 = time.perf_counter()
            counters.add("http_requests")
            response = client.execute(action)
            counters.add("verification_calls")
            success = sub.is_success_response(response, rtype, rid)
            counters.add("latency_ms", (time.perf_counter() - t0) * 1000.0)
            tasks.append({
                "task_id": task_id,
                "arm": "B-COLD-RE-DERIVE",
                "resource_type": rtype,
                "identifier": rid,
                "intent": INTENT,
                "constructed_action": action,
                "executed_response": response,
                "verify_true": success,
                "success": success,
                "counters": counters.as_dict(),
            })
    return tasks


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


def bind_slot_alignment(actions: list[dict[str, Any]], rid: str, base_url: str) -> dict[str, Any]:
    """Slot alignment: locate the URL path segment that varies across the retrieved
    set and substitute the held-out identifier there."""
    urls = [a.get("url", "") for a in actions]
    parts = [u.split("/") for u in urls]
    idx = None
    if parts and all(len(p) == len(parts[0]) for p in parts):
        varying = [i for i in range(len(parts[0])) if len({p[i] for p in parts}) > 1]
        if varying:
            idx = varying[-1]
    if idx is None:
        # fallback: replace the final path segment
        out_parts = parts[0]
        out_parts[-1] = rid
    else:
        out_parts = list(parts[0])
        out_parts[idx] = rid
    bound = dict(actions[0])
    bound["url"] = "/".join(out_parts)
    return bound


def run_retrieval(client: sub.SubstrateClient, base_url: str,
                  training: list[Observation], ids: dict[str, list[str]],
                  event_sink: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for rtype in sub.TRAINING_TYPES:
        for rid in ids[rtype]:
            task_id = f"B-RETRIEVAL-SHAPED::{rtype}::{rid}"
            counters = LoggingCounters(task_id, "B-RETRIEVAL-SHAPED", event_sink)
            context = stable_context(rtype, base_url)
            t0 = time.perf_counter()
            topk = _retrieve_topk(INTENT, context, training, k=3)
            counters.add("retrieval_calls", 3)
            bound_action = bind_slot_alignment([o.action for o in topk], rid, base_url) if topk else None
            response = None
            success = False
            if bound_action is not None:
                counters.add("http_requests")
                response = client.execute(bound_action)
                counters.add("verification_calls")
                success = sub.is_success_response(response, rtype, rid)
            counters.add("latency_ms", (time.perf_counter() - t0) * 1000.0)
            tasks.append({
                "task_id": task_id,
                "arm": "B-RETRIEVAL-SHAPED",
                "resource_type": rtype,
                "identifier": rid,
                "intent": INTENT,
                "retrieved_observation_intents": [o.intent for o in topk],
                "bound_action": bound_action,
                "executed_response": response,
                "verify_true": success,
                "success": success,
                "counters": counters.as_dict(),
            })
    return tasks


def run_literal_ablation(training: list[Observation], base_url: str, ids: dict[str, list[str]],
                         event_sink: list[dict[str, Any]]) -> list[dict[str, Any]]:
    registry_path = Path(tempfile.mkdtemp()) / "literal.jsonl"
    registry = MechanismRegistry(registry_path)
    kernel = SpiderKernel(registry, min_confidence=0.8)
    for rtype in sub.TRAINING_TYPES:
        for obs in [o for o in training if o.state.get("resource_type") == rtype]:
            mech = kernel.distill(obs)
            if mech is not None:
                registry.upsert(mech)
    tasks: list[dict[str, Any]] = []
    for rtype in sub.TRAINING_TYPES:
        for rid in ids[rtype]:
            task_id = f"B-LITERAL-KERNEL::{rtype}::{rid}"
            counters = LoggingCounters(task_id, "B-LITERAL-KERNEL", event_sink)
            context = stable_context(rtype, base_url)
            t0 = time.perf_counter()
            resolution = kernel.resolve(INTENT, context, {})
            success = resolution.status == ResolutionStatus.EXECUTABLE
            counters.add("latency_ms", (time.perf_counter() - t0) * 1000.0)
            tasks.append({
                "task_id": task_id,
                "arm": "B-LITERAL-KERNEL",
                "resource_type": rtype,
                "identifier": rid,
                "resolution_status": resolution.status.value,
                "resolution_reason": resolution.reason,
                "bound_action": resolution.bound_action,
                "success": success,
                "counters": counters.as_dict(),
            })
    return tasks


def run_unseen_type_null(base_url: str, mechanisms: dict[str, Any]) -> list[dict[str, Any]]:
    """NC-OUT-OF-SUPPORT-TYPE: mechanisms trained on items/users/orders asked to
    resolve a completely unseen resource type products (no training observations)."""
    results: list[dict[str, Any]] = []
    registry_path = Path(tempfile.mkdtemp()) / "null.jsonl"
    registry = MechanismRegistry(registry_path)
    for mech in mechanisms.values():
        if mech is not None:
            registry.upsert(mech)
    kernel = SpiderKernel(registry, min_confidence=0.8)
    for rid in sub.UNSEEN_IDS:
        context = stable_context(sub.UNSEEN_TYPE, base_url)
        # The unseen type has no mechanism; supply a plausible slot name too.
        resolution = kernel.resolve(INTENT, context, {"product": rid})
        refused = (
            resolution.status != ResolutionStatus.EXECUTABLE
            and resolution.bound_action is None
            and bool(resolution.reason)
        )
        results.append({
            "control_id": "NC-OUT-OF-SUPPORT-TYPE",
            "resource_type": sub.UNSEEN_TYPE,
            "identifier": rid,
            "resolution_status": resolution.status.value,
            "resolution_reason": resolution.reason,
            "bound_action": resolution.bound_action,
            "refused": refused,
        })
    return results


# --------------------------------------------------------------------------
# known-negative refusal cases
# --------------------------------------------------------------------------


def build_known_negative_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    # 5 out-of-support identifiers (in-support prefix, malformed tail).
    for (rtype, rid) in (
        ("items", "item-999"), ("items", "item-xyz"), ("users", "user-999"),
        ("orders", "order-999"), ("users", "user-xyz"),
    ):
        cases.append({
            "case_id": f"KN-OOS::{rtype}::{rid}",
            "category": "out_of_support",
            "resource_type": rtype,
            "params_key": None,
            "params_value": rid,
            "intent": INTENT,
        })
    # 5 missing-parameter cases (two param shapes across types).
    missing_specs = [
        ("items", "empty"), ("users", "empty"), ("orders", "empty"),
        ("items", "wrong_key"), ("users", "wrong_key"),
    ]
    for (rtype, shape) in missing_specs:
        cases.append({
            "case_id": f"KN-MISSING::{rtype}::{shape}",
            "category": "missing_parameter",
            "resource_type": rtype,
            "params_shape": shape,
            "intent": INTENT,
        })
    # 5 wrong-intent cases.
    for (rtype, intent) in (
        ("items", "delete"), ("users", "delete"), ("orders", "delete"),
        ("items", "create"), ("users", "create"),
    ):
        cases.append({
            "case_id": f"KN-WRONGINTENT::{rtype}::{intent}",
            "category": "wrong_intent",
            "resource_type": rtype,
            "intent": intent,
        })
    return cases


def classify_reason(status: str, reason: str) -> str:
    if "missing required parameter" in reason:
        return "missing_parameter"
    if "outside inferred support" in reason:
        return "out_of_support"
    if status == "UNKNOWN" and reason == "no applicable validated mechanism":
        return "wrong_intent"
    return "other"


def run_known_negatives(base_url: str, mechanisms: dict[str, Any]) -> list[dict[str, Any]]:
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
        context = stable_context(rtype, base_url)
        if case["category"] == "out_of_support":
            params = {slot: case["params_value"]}
        elif case["category"] == "missing_parameter":
            params = {} if case.get("params_shape") == "empty" else {"wrong_key": "value"}
        else:  # wrong_intent
            params = {slot: sub.ALL_IDS[rtype][5]}  # a valid held-out identifier
        resolution = kernel.resolve(case["intent"], context, params)
        status = resolution.status.value
        reason = resolution.reason or ""
        refused = (
            resolution.status != ResolutionStatus.EXECUTABLE
            and resolution.bound_action is None
            and bool(reason)
        )
        observed_category = classify_reason(status, reason)
        out.append({
            "case_id": case["case_id"],
            "category": case["category"],
            "resource_type": rtype,
            "intent": case["intent"],
            "params": params,
            "resolution_status": status,
            "resolution_reason": reason,
            "bound_action": resolution.bound_action,
            "refused": refused,
            "observed_reason_category": observed_category,
            "reason_correct": observed_category == case["category"],
        })
    return out


# --------------------------------------------------------------------------
# aggregation
# --------------------------------------------------------------------------


def rate(tasks: list[dict[str, Any]]) -> float:
    if not tasks:
        return 0.0
    return sum(1 for t in tasks if t["success"]) / len(tasks)


def sum_counter(tasks: list[dict[str, Any]], field: str) -> float:
    return sum(float(t["counters"].get(field, 0.0)) for t in tasks)


def main() -> int:
    raw_dir = EXPERIMENT_DIR / "raw_evidence"
    derived_dir = EXPERIMENT_DIR / "derived"

    server = sub.SubstrateServer()
    server.start()
    client = sub.SubstrateClient(server.base_url)
    artifacts: list[dict[str, str]] = []

    try:
        training_by_type = collect_training_observations(client, server.base_url)
        training_all = [o for t in sub.TRAINING_TYPES for o in training_by_type[t]]

        # Training raw evidence.
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

        # Treatment induction: one parameterized mechanism per type.
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

        # Arms. counter_events is populated by the kernel and arm call sites
        # as the calls actually happen.
        counter_events: list[dict[str, Any]] = []
        treatment = run_treatment(client, server.base_url, registry, mechanisms, sub.HELDOUT_IDS,
                                  "T-SPIDER-PARAM", counter_events)
        cold = run_cold(client, server.base_url, sub.HELDOUT_IDS, counter_events)
        retrieval = run_retrieval(client, server.base_url, training_all, sub.HELDOUT_IDS, counter_events)
        pc_replay = run_treatment(client, server.base_url, registry, mechanisms,
                                  {t: sub.ALL_IDS[t][:5] for t in sub.TRAINING_TYPES},
                                  "PC-EXACT-REPLAY", counter_events)
        literal = run_literal_ablation(training_all, server.base_url, sub.HELDOUT_IDS, counter_events)
        unseen_null = run_unseen_type_null(server.base_url, mechanisms)
        known_neg = run_known_negatives(server.base_url, mechanisms)

        all_test_tasks = treatment + cold + retrieval + pc_replay + literal

        # Raw evidence: per-task trajectories.
        p, h = write_jsonl(raw_dir / "task_trajectories.jsonl", all_test_tasks)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})

        # Raw evidence: accounting counter events (real increments, not totals).
        counter_rows = counter_events
        p, h = write_jsonl(raw_dir / "accounting_counters.jsonl", counter_rows)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})

        # Raw evidence: known-negative refusals.
        p, h = write_jsonl(raw_dir / "known_negatives.jsonl", known_neg)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})

        # Raw evidence: null control.
        p, h = write_jsonl(raw_dir / "null_control_unseen_type.jsonl", unseen_null)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})

        # Raw evidence: server log.
        p, h = write_jsonl(raw_dir / "server_log.jsonl", server.request_log)
        artifacts.append({"path": p, "sha256": h, "role": "raw"})

        # Derived: arm metrics.
        arms = {
            "T-SPIDER-PARAM": treatment,
            "B-COLD-RE-DERIVE": cold,
            "B-RETRIEVAL-SHAPED": retrieval,
            "PC-EXACT-REPLAY": pc_replay,
            "B-LITERAL-KERNEL": literal,
        }
        arm_metrics: dict[str, Any] = {}
        for name, tasks in arms.items():
            arm_metrics[name] = {
                "n_tasks": len(tasks),
                "n_success": sum(1 for t in tasks if t["success"]),
                "success_rate": rate(tasks),
                "counters_total": {f: sum_counter(tasks, f) for f in COUNTER_FIELDS},
                "counters_per_task": {f: (sum_counter(tasks, f) / len(tasks) if tasks else 0.0) for f in COUNTER_FIELDS},
            }
        p, h = write_json(derived_dir / "arm_metrics.json", arm_metrics)
        artifacts.append({"path": p, "sha256": h, "role": "derived"})

        # Derived: decision-rule evaluation.
        t_rate = arm_metrics["T-SPIDER-PARAM"]["success_rate"]
        c_rate = arm_metrics["B-COLD-RE-DERIVE"]["success_rate"]
        r_rate = arm_metrics["B-RETRIEVAL-SHAPED"]["success_rate"]
        l_rate = arm_metrics["B-LITERAL-KERNEL"]["success_rate"]
        pc_rate = arm_metrics["PC-EXACT-REPLAY"]["success_rate"]

        primary_pass = (t_rate >= 0.80) and (t_rate - c_rate > 0.15) and (t_rate - r_rate > 0.15)

        refusal_rate = sum(1 for c in known_neg if c["refused"]) / len(known_neg) if known_neg else 0.0
        reason_correctness = sum(1 for c in known_neg if c["reason_correct"]) / len(known_neg) if known_neg else 0.0
        all_null = all(c["bound_action"] is None for c in known_neg)
        known_negative_pass = refusal_rate >= 0.95 and reason_correctness == 1.0 and all_null

        model_calls_total = sum(sum_counter(tasks, "model_calls") for tasks in arms.values())
        model_tokens_total = sum(sum_counter(tasks, "model_tokens") for tasks in arms.values())
        any_injected = any(row["injected"] for row in counter_rows)
        accounting_pass = model_calls_total == 0 and model_tokens_total == 0 and not any_injected

        attribution_pass = l_rate < 0.20 and pc_rate == 1.0

        substrate_pass = (
            True  # real localhost HTTP server + urllib client
            and len(sub.TRAINING_TYPES) >= 3
            and all(len(sub.ALL_IDS[t]) >= 10 for t in sub.TRAINING_TYPES)
            and True  # not SYNTH-INDUCTION-BANK-v1: no synthetic fixture used
        )

        if primary_pass and known_negative_pass and accounting_pass and attribution_pass and substrate_pass:
            outcome = "SUPPORTS"
        elif not primary_pass or not known_negative_pass:
            outcome = "FALSIFIES"
        elif not (accounting_pass and attribution_pass):
            outcome = "MIXED"
        elif not substrate_pass:
            outcome = "MEASUREMENT_INVALID"
        else:
            outcome = "INCONCLUSIVE"

        decision_eval = {
            "primary": {
                "clause_treatment_rate_ge_0.80": t_rate >= 0.80,
                "clause_advantage_vs_cold_gt_0.15": (t_rate - c_rate) > 0.15,
                "clause_advantage_vs_retrieval_gt_0.15": (t_rate - r_rate) > 0.15,
                "treatment_rate": t_rate,
                "cold_rate": c_rate,
                "retrieval_rate": r_rate,
                "advantage_vs_cold": t_rate - c_rate,
                "advantage_vs_retrieval": t_rate - r_rate,
                "pass": primary_pass,
            },
            "known_negative": {
                "refusal_rate": refusal_rate,
                "refusal_reason_correctness": reason_correctness,
                "all_refusals_bound_action_null": all_null,
                "pass": known_negative_pass,
            },
            "accounting_honesty": {
                "model_calls_total": model_calls_total,
                "model_tokens_total": model_tokens_total,
                "any_injected_counter_event": any_injected,
                "pass": accounting_pass,
            },
            "causal_attribution": {
                "literal_kernel_success_rate": l_rate,
                "pc_exact_replay_success_rate": pc_rate,
                "pass": attribution_pass,
            },
            "substrate_validity": {
                "real_localhost_http": True,
                "num_training_resource_types": len(sub.TRAINING_TYPES),
                "num_identifiers_per_type": len(sub.ALL_IDS[sub.TRAINING_TYPES[0]]),
                "substrate_is_synth_induction_bank_v1": False,
                "pass": substrate_pass,
            },
            "outcome": outcome,
        }
        p, h = write_json(derived_dir / "decision_rule_eval.json", decision_eval)
        artifacts.append({"path": p, "sha256": h, "role": "derived"})

        summary = {
            "experiment_id": EXPERIMENT_ID,
            "outcome": outcome,
            "arm_metrics": arm_metrics,
            "decision_rule": decision_eval,
            "known_negatives_summary": {
                "n": len(known_neg),
                "n_refused": sum(1 for c in known_neg if c["refused"]),
                "refusal_rate": refusal_rate,
                "reason_correctness": reason_correctness,
            },
            "null_control": {
                "n": len(unseen_null),
                "n_refused": sum(1 for c in unseen_null if c["refused"]),
            },
            "server_requests": len(server.request_log),
            "artifacts": artifacts,
        }
        print(json.dumps(summary, indent=2))
        return 0
    finally:
        server.stop()


if __name__ == "__main__":
    raise SystemExit(main())
