"""EXECUTE runner for EXP-PRODUCT-36314204238.

Writes RAW EVIDENCE ONLY. This script measures and records; it does not decide.
No derived metric, no falsifier evaluation and no decision rule lives here -- all
of that is in build_result.py, so that the boundary between observation and
interpretation is a file boundary and not a promise.

Raw artifacts produced (prereg section 11):
    raw_evidence/substrate_probe.json    pre-arm surface contract, falsifier F5
    raw_evidence/observations.jsonl      every HTTP interaction, unaggregated
    raw_evidence/bind_results.jsonl      one record per task, binding outcome
    raw_evidence/exec_results.jsonl      one record per task, execution detail
    raw_evidence/probe_results.jsonl     malformed / out-of-namespace probes
    raw_evidence/run_config.json         resolved configuration and hashes

Request frame
-------------
The frozen design fixes collections, identifiers, arms, metrics, thresholds and
the decision rule. It does not fix the request string, so the frame is a
substrate choice and is recorded as one. Two frames are run, both with the
frozen 45 cells and 100 tasks per cell:

``R`` raw           the request names the identifier verbatim,
                   "read record item-217 in items catalog".
``B`` bare-ordinal  the request names only the ordinal and the collection word,
                   "read record 217 in items catalog", so the identifier FORM has
                   to be learned from observed variability to be rebuilt.

Both are run because they separate two different claims. On R the goal string
itself contains both slot values, so any binder that reads the goal can assemble
the path and the frame cannot discriminate a learned binder from a matcher. On B
it cannot, because "217" plus "items" does not contain the string "item-217".
R is reported as the primary frame because prereg 4.3 enumerates full
identifiers as the task input; B is reported alongside it and is the frame in
which the frozen F1 comparison is non-degenerate. Neither is selected after
seeing outcomes.
"""

from __future__ import annotations

import hashlib
import http.client
import json
import platform
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(HERE))

from spider.kernel import SpiderKernel  # noqa: E402
from spider.models import BINDER_ABSTAIN, BINDER_BOUND, Mechanism, Observation  # noqa: E402
from spider.registry import MechanismRegistry  # noqa: E402
from spider.variability import make_goal, parse_goal  # noqa: E402

from substrate import (  # noqa: E402
    AUTH_TOKEN,
    BASE_LATENCY_S,
    FAMILY_VERB,
    IN_SUPPORT_IDS,
    OUT_OF_SUPPORT_IDS,
    TRAIN_IDS,
    Substrate,
)

SEED = 42
RAW = HERE / "raw_evidence"

MULTIPLIERS = [1.0, 2.0, 5.0, 10.0, 20.0]
FRAMES = ["R", "B"]
BASE_RE_DERIVATION_REQUESTS = 3
INHERITED_REQUESTS = 1
TASKS_PER_CELL = 100
CONFIDENCE_THRESHOLD = 0.85
FAMILIES = ["read", "update", "delete"]
TRAIN_COLLECTIONS_MULTI = ["items", "products", "orders"]
TRAIN_COLLECTIONS_SINGLE = ["items"]
OUT_OF_SUPPORT_COLLECTION = "widgets"
#: Collection -> identifier prefix as a property of the SUBSTRATE. A binder may
#: not consult this; only the runner uses it to build ground truth, and arm A3's
#: maximally favourable harness uses it to assemble params (see matcher_params).
SUBSTRATE_PREFIX = {"items": "item", "products": "product", "orders": "order", "widgets": "widget"}


# --------------------------------------------------------------------------- #
# HTTP client. One kept-alive connection per thread; the substrate requires the
# fixed bearer token, so no request is ever spent on authentication.
# --------------------------------------------------------------------------- #


class Client:
    def __init__(self, substrate: "Substrate") -> None:
        self.substrate = substrate
        self._conn = http.client.HTTPConnection("127.0.0.1", substrate.port, timeout=10)
        self.records: list[dict[str, Any]] = []

    def set_latency_factor(self, factor: float) -> None:
        self.substrate.set_latency_factor(factor)

    def call(self, method: str, path: str, body: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], int]:
        payload = json.dumps(body, sort_keys=True) if body is not None else None
        headers = {"Authorization": AUTH_TOKEN, "Content-Type": "application/json"}
        started = time.perf_counter()
        self._conn.request(method, path, body=payload, headers=headers)
        response = self._conn.getresponse()
        raw = response.read()
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError:
            decoded = {"raw": raw.decode("utf-8", "replace")}
        latency_ms = float(decoded.get("latency_s", 0.0)) * 1000.0 if isinstance(decoded, dict) else 0.0
        self.records.append(
            {
                "method": method,
                "path": path,
                "request_body": body,
                "status": response.status,
                "response": decoded,
                "elapsed_ms": round(elapsed_ms, 4),
                "injected_latency_ms": round(latency_ms, 6),
            }
        )
        return response.status, decoded, len(payload or "")

    def mark(self) -> int:
        """Current length of the raw request log. Non-destructive.

        Counting requests must never consume the log: the raw HTTP records are
        the primary evidence (prereg 8.4) and a drain-based counter would leave
        observations.jsonl empty.
        """
        return len(self.records)

    def drain(self) -> list[dict[str, Any]]:
        out, self.records = self.records, []
        return out


# --------------------------------------------------------------------------- #
# Task construction.
# --------------------------------------------------------------------------- #


def cell_tasks() -> list[dict[str, Any]]:
    """The frozen 100 tasks of one cell: 50 in-support + 50 out-of-support."""
    tasks: list[dict[str, Any]] = []
    for i, ident_num in enumerate(IN_SUPPORT_IDS):
        family = FAMILIES[i % len(FAMILIES)]
        tasks.append(
            {
                "task_id": f"in-{ident_num}",
                "support": "in_support",
                "collection": "items" if i % 3 == 0 else ("products" if i % 3 == 1 else "orders"),
                "identifier_num": ident_num,
                "family": family,
            }
        )
    for i, ident_num in enumerate(OUT_OF_SUPPORT_IDS):
        family = FAMILIES[i % len(FAMILIES)]
        tasks.append(
            {
                "task_id": f"out-{ident_num}",
                "support": "out_of_support",
                "collection": OUT_OF_SUPPORT_COLLECTION,
                "identifier_num": ident_num,
                "family": family,
            }
        )
    return tasks


def ground_truth(task: dict[str, Any]) -> str:
    return f"/{task['collection']}/{SUBSTRATE_PREFIX[task['collection']]}-{task['identifier_num']}"


def goal_for(task: dict[str, Any], frame: str) -> str:
    prefix = SUBSTRATE_PREFIX[task["collection"]]
    target = (
        f"{prefix}-{task['identifier_num']}" if frame == "R" else str(task["identifier_num"])
    )
    return make_goal(task["family"], target, task["collection"])


def matcher_params(parsed: dict[str, str]) -> dict[str, str]:
    """The most favourable params a hand-written matcher could hand to the incumbent.

    The incumbent kernel never forms an identifier; its caller supplies the slot
    values. To avoid strawmanning arm A3 with a deliberately bad caller, the
    harness singularises the collection word and joins it to the ordinal. This is
    pure string manipulation of the request, exactly the class of behaviour
    C-PARAM-INHERIT is about, and it is the strongest such rule available.
    """
    collection = parsed["collection"]
    prefix = collection[:-1] if collection.endswith("s") else collection
    if parsed.get("form") == "B":
        identifier = f"{prefix}-{parsed['target']}"
    else:
        identifier = parsed["target"]
    return {"collection": collection, "id": identifier}


# --------------------------------------------------------------------------- #
# Training: real HTTP, the 3-request re-derivation path per observation.
# --------------------------------------------------------------------------- #


def re_derive(client: Client, collection: str, identifier: str, family: str, requests: int) -> dict[str, Any]:
    """Spend exactly ``requests`` requests to reach and act on one resource.

    The first request lists the collection, which is the only step that can
    discover an identifier form without already knowing it; the remainder are
    detail/verify traffic. Returns the discovered identifier and the final
    response so that every arm's cost and correctness are measured the same way.
    """
    verb = FAMILY_VERB[family]
    budget = int(round(requests))
    listing_status, listing_payload, _ = client.call("GET", f"/{collection}")
    available = listing_payload.get("identifiers", []) if listing_status == 200 else []
    discovered = identifier if identifier in available else ""
    status, payload = listing_status, listing_payload
    for _ in range(max(0, budget - 1)):
        if not discovered:
            break
        status, payload, _ = client.call(verb, f"/{collection}/{discovered}", {"status": "ok"})
    return {
        "discovered": discovered,
        "final_status": status,
        "final_response": payload,
        "listed": available,
    }


def build_training(
    client: Client, collections: list[str]
) -> list[Observation]:
    """Execute the frozen re-derivation path and record genuine observations."""
    observations: list[Observation] = []
    for collection in collections:
        for num in TRAIN_IDS:
            identifier = f"{SUBSTRATE_PREFIX[collection]}-{num}"
            for family in FAMILIES:
                before = client.mark()
                result = re_derive(
                    client, collection, identifier, family, BASE_RE_DERIVATION_REQUESTS
                )
                spent = client.mark() - before
                verb = FAMILY_VERB[family]
                success = result["final_status"] == 200 and result["discovered"] == identifier
                observations.append(
                    Observation(
                        intent=family,
                        state={
                            "collection": collection,
                            "resource": identifier,
                            "authenticated": True,
                        },
                        action={"method": verb, "path": f"/{collection}/{identifier}"},
                        next_state={
                            "collection": collection,
                            "identifier": identifier,
                            "status": "ok",
                            "exists": family != "delete",
                        },
                        success=success,
                        provenance={
                            "seed": SEED,
                            "phase": "induction",
                            "collection": collection,
                            "identifier": identifier,
                            "family": family,
                            "request_count": spent,
                        },
                    )
                )
    return observations


def modal_slot_values(
    training: list[Observation], mechanisms: list[Mechanism]
) -> dict[str, dict[str, dict[str, Any]]]:
    """Modal observed value per slot, per mechanism, from the training paths.

    This is the ONLY statistic the most-frequent-value null is allowed, and it is
    the mode, as its frozen definition requires.
    """
    by_intent: dict[str, list[str]] = defaultdict(list)
    for observation in training:
        by_intent[observation.intent].append(observation.action["path"])

    out: dict[str, dict[str, dict[str, Any]]] = {}
    for mechanism in mechanisms:
        template = [p for p in mechanism.action_template.get("path", "").split("/") if p]
        slot_entries: dict[str, dict[str, Any]] = {}
        for name in mechanism.parameter_slots:
            index = next(
                (
                    i
                    for i, part in enumerate(template)
                    if part == "${" + name + "}"
                ),
                None,
            )
            if index is None:
                continue
            values = [
                [s for s in path.split("/") if s][index]
                for path in by_intent.get(mechanism.intent, [])
                if len([s for s in path.split("/") if s]) > index
            ]
            if not values:
                continue
            counts = Counter(values)
            value, n = counts.most_common(1)[0]
            slot_entries[name] = {"value": value, "share": round(n / len(values), 6)}
        out[mechanism.mechanism_id] = slot_entries
    return out


def canonical_example(training: list[Observation], intent: str) -> str | None:
    for observation in training:
        if observation.intent == intent:
            return observation.action["path"]
    return None


# --------------------------------------------------------------------------- #
# Binding dispatch. One function per arm, all returning the same shape, so no arm
# can be scored on a field another arm does not produce.
# --------------------------------------------------------------------------- #


def bind_for_arm(
    arm: str,
    mechanism: Mechanism | None,
    parsed: dict[str, str],
    kernel: SpiderKernel,
    modal: dict[str, dict[str, Any]],
    canonical: str | None,
    tie_break: str = "longest_first",
) -> dict[str, Any]:
    if mechanism is None:
        return {
            "bind_status": BINDER_ABSTAIN,
            "bound_path": None,
            "bound_method": None,
            "bind_confidence": 0.0,
            "bind_reason": "arm has no induced mechanism",
            "slot_values": {},
            "slot_support": {},
        }
    if arm in ("A1", "A2"):
        outcome = kernel.bind_variability(mechanism, parsed)
    elif arm == "A4":
        outcome = kernel.bind_lexical_overlap(mechanism, parsed, tie_break=tie_break)
    elif arm == "A5":
        outcome = kernel.bind_positional_regex(mechanism, parsed, canonical)
    elif arm == "A6":
        outcome = kernel.bind_most_frequent_value(mechanism, parsed, modal)
    else:
        raise ValueError(f"unexpected binder arm {arm}")
    action = outcome.bound_action or {}
    return {
        "bind_status": outcome.status,
        "bound_path": action.get("path"),
        "bound_method": action.get("method"),
        "bind_confidence": round(float(outcome.bind_confidence), 6),
        "bind_reason": outcome.reason,
        "slot_values": outcome.slot_values,
        "slot_support": outcome.slot_support,
    }


def bind_declared_vocab(
    family: str, parsed: dict[str, str], kernel: SpiderKernel
) -> dict[str, Any]:
    """Arm A3: the incumbent declared-vocabulary path, unmodified.

    ``distill_parameterized`` turned the leading collection segment into a
    declared ``${collection}`` slot because it equalled ``state['collection']``,
    so the caller supplies the collection and the identifier as plain params and
    ``resolve`` binds them. No support is checked; the only gate is the
    syntactic ``_SLOT_VALUE`` guard.
    """
    params = matcher_params(parsed)
    context = {
        "collection": parsed["collection"],
        "resource": params["id"],
        "authenticated": True,
    }
    resolution = kernel.resolve(family, context, params)
    action = resolution.bound_action or {}
    return {
        "bind_status": BINDER_BOUND if resolution.status.value == "EXECUTABLE" else BINDER_ABSTAIN,
        "bound_path": action.get("path"),
        "bound_method": action.get("method"),
        "bind_confidence": round(float(resolution.confidence), 6),
        "bind_reason": f"resolve={resolution.status.value}: {resolution.reason}",
        "slot_values": params,
        "slot_support": {},
        "resolution_status": resolution.status.value,
        "mechanism_id": resolution.mechanism_id,
    }


def run_task(
    arm: str,
    mult: float,
    frame: str,
    task: dict[str, Any],
    client: Client,
    kernel: SpiderKernel,
    mechanism: Mechanism | None,
    modal: dict[str, Any],
    canonical: str | None,
    scratchpad: dict[str, str],
    tie_break: str = "longest_first",
) -> dict[str, Any]:
    """Run one task in one cell and return one raw record.

    Verification is identical for every arm: the final HTTP response must be 2xx
    and must name the collection and identifier the task asked for, with
    ``exists`` False after a delete. No arm gets a verification shortcut.
    """
    goal = goal_for(task, frame)
    parsed = parse_goal(goal)
    truth = ground_truth(task)
    verb = FAMILY_VERB[task["family"]]
    mark_start = client.mark()

    if arm == "A3":
        bound = bind_declared_vocab(task["family"], parsed, kernel)
    elif arm in ("A7", "A8", "A9"):
        bound = {
            "bind_status": BINDER_BOUND,
            "bound_path": None,
            "bound_method": verb,
            "bind_confidence": 1.0,
            "bind_reason": "",
            "slot_values": {},
            "slot_support": {},
        }
    else:
        bound = bind_for_arm(arm, mechanism, parsed, kernel, modal, canonical, tie_break)

    final_status: int | None = None
    final_response: dict[str, Any] = {}
    executed = False

    if arm in ("A7", "A8", "A9"):
        identifier = f"{SUBSTRATE_PREFIX[task['collection']]}-{task['identifier_num']}"
        if arm == "A7":
            # Cold re-derivation spends EXACTLY 3 x cost_multiplier requests and
            # the last of them IS the task's action, so the declared cost basis
            # (prereg 4.2) is met with no extra request.
            spent = int(round(BASE_RE_DERIVATION_REQUESTS * mult))
            result = re_derive(client, task["collection"], identifier, task["family"], spent)
            bound["bound_path"] = f"/{task['collection']}/{result['discovered']}"
            bound["bind_reason"] = f"cold re-derivation spent {spent} requests"
            final_status, final_response = result["final_status"], result["final_response"]
            executed = True
        elif arm == "A8":
            # Within-episode scratchpad: the episode accumulates what it has
            # discovered and pays full re-derivation only the FIRST time it meets
            # a collection. It carries the collection->identifier-prefix relation,
            # not a literal path, so it is a fair strong within-episode reuse
            # baseline rather than a cache of one answer.
            if task["collection"] not in scratchpad:
                spent = int(round(BASE_RE_DERIVATION_REQUESTS * mult))
                result = re_derive(client, task["collection"], identifier, task["family"], spent)
                discovered = result["discovered"]
                scratchpad[task["collection"]] = discovered.rsplit("-", 1)[0] if "-" in discovered else discovered
                bound["bound_path"] = f"/{task['collection']}/{discovered}"
                bound["bind_reason"] = f"scratchpad primed for {task['collection']} at {spent} requests"
                final_status, final_response = result["final_status"], result["final_response"]
            else:
                assembled = f"{scratchpad[task['collection']]}-{task['identifier_num']}"
                bound["bound_path"] = f"/{task['collection']}/{assembled}"
                bound["bind_reason"] = f"scratchpad hit for {task['collection']}"
                final_status, final_response, _ = client.call(verb, bound["bound_path"], {"status": "ok"})
            executed = True
        else:  # A9 retrieval-K5, one request, no induction
            params = matcher_params(parsed)
            bound["bound_path"] = f"/{task['collection']}/{params['id']}"
            bound["bind_reason"] = "retrieval-K5 single request, no induction"
            final_status, final_response, _ = client.call(verb, bound["bound_path"], {"status": "ok"})
            executed = True
    elif bound["bind_status"] == BINDER_BOUND and bound["bound_path"]:
        final_status, final_response, _ = client.call(verb, bound["bound_path"], {"status": "ok"})
        executed = True

    request_count = client.mark() - mark_start
    http_records = client.records[mark_start:]
    latency_ms = sum(r["injected_latency_ms"] for r in http_records)

    identifier_sent = None
    if bound["bound_path"]:
        parts = [p for p in bound["bound_path"].split("/") if p]
        identifier_sent = parts[-1] if len(parts) > 1 else None
    intended = f"{SUBSTRATE_PREFIX[task['collection']]}-{task['identifier_num']}"
    bind_correct = bool(
        bound["bound_path"]
        and bound["bound_path"] == truth
        and identifier_sent == intended
    )
    verified = bool(
        executed
        and final_status is not None
        and 200 <= final_status < 300
        and isinstance(final_response, dict)
        and final_response.get("collection") == task["collection"]
        and (final_response.get("identifier") == intended)
        and (final_response.get("exists") is (task["family"] != "delete"))
    )

    return {
        "seed": SEED,
        "arm": arm,
        "cost_multiplier": mult,
        "frame": frame,
        "task_id": task["task_id"],
        "support": task["support"],
        "family": task["family"],
        "collection": task["collection"],
        "identifier_intended": intended,
        "identifier_sent": identifier_sent,
        "goal": goal,
        "goal_frame": frame,
        "ground_truth_path": truth,
        "bind_status": bound["bind_status"],
        "bind_value": bound["bound_path"],
        "bind_method": bound["bound_method"],
        "bind_confidence": bound["bind_confidence"],
        "bind_reason": bound["bind_reason"],
        "slot_values": bound.get("slot_values", {}),
        "bind_correct": bind_correct,
        "executed": executed,
        "verified": verified,
        "http_status": final_status,
        "request_count": request_count,
        "injected_latency_ms": round(latency_ms, 6),
        "binder": arm,
        "tie_break": tie_break if arm == "A4" else None,
    }


# --------------------------------------------------------------------------- #
# F5 surface contract, verified before any measurement arm runs.
# --------------------------------------------------------------------------- #


def surface_probe(client: Client, kernel: SpiderKernel) -> dict[str, Any]:
    checks: dict[str, Any] = {}

    # (a) each cost_multiplier yields distinct mean re-derivation requests
    means: dict[str, float] = {}
    for mult in MULTIPLIERS:
        client.set_latency_factor(1.0)
        before = client.mark()
        for i in range(20):
            re_derive(
                client,
                "items",
                f"item-{201 + i}",
                "read",
                BASE_RE_DERIVATION_REQUESTS * mult,
            )
        means[str(mult)] = (client.mark() - before) / 20.0
    distinct = len(set(round(v, 6) for v in means.values()))
    checks["P1_multiplier_yields_distinct_mean_requests"] = {
        "expected": "5 distinct mean re-derivation request counts, one per cost_multiplier",
        "observed": means,
        "n_distinct": distinct,
        "pass": distinct == len(MULTIPLIERS),
    }

    # (b) inheritance path costs exactly 1 request
    client.set_latency_factor(1.0)
    reg_probe = MechanismRegistry(HERE / "raw_evidence" / "_probe_registry.jsonl")
    probe_kernel = SpiderKernel(reg_probe, min_confidence=CONFIDENCE_THRESHOLD)
    training = build_training_probe(client)
    mechanisms = probe_kernel.distill_variability(training, "probe")
    mechanism = next((m for m in mechanisms if m.intent == "read"), None)
    parsed = parse_goal(goal_for({"family": "read", "collection": "items", "identifier_num": 217}, "R"))
    before = client.mark()
    outcome = probe_kernel.bind_variability(mechanism, parsed)
    if outcome.status == BINDER_BOUND and outcome.bound_action:
        client.call("GET", outcome.bound_action["path"])
    inherited = client.mark() - before
    checks["P2_inheritance_path_costs_one_request"] = {
        "expected": 1,
        "observed": inherited,
        "bound_path": (outcome.bound_action or {}).get("path"),
        "pass": inherited == 1,
    }

    # (c) HTTP error rates < 0.01 across all verbs on the served population
    client.set_latency_factor(1.0)
    statuses: list[int] = []
    for collection in TRAIN_COLLECTIONS_MULTI + [OUT_OF_SUPPORT_COLLECTION]:
        verb = FAMILY_VERB["read"]
        status, payload, _ = client.call("GET", f"/{collection}")
        statuses.append(status)
        for ident in list(payload.get("identifiers", []))[:5]:
            statuses.append(client.call(verb, f"/{collection}/{ident}")[0])
            statuses.append(client.call("PUT", f"/{collection}/{ident}", {"status": "ok"})[0])
            statuses.append(client.call("DELETE", f"/{collection}/{ident}")[0])
    error_rate = sum(1 for s in statuses if not 200 <= s < 300) / len(statuses)
    checks["P3_http_error_rate_below_one_percent"] = {
        "expected": "< 0.01",
        "observed": round(error_rate, 6),
        "n_requests": len(statuses),
        "pass": error_rate < 0.01,
    }

    # (d) latency injection deterministic per seed and per multiplier
    latencies: dict[str, list[float]] = {}
    for mult in (1.0, 20.0):
        client.set_latency_factor(mult)
        samples = [
            client.call("GET", f"/items/item-{201 + i}")[1].get("latency_s")
            for i in range(5)
        ]
        latencies[str(mult)] = samples
    expected_1 = [round(BASE_LATENCY_S * 1.0, 9)] * 5
    expected_20 = [round(BASE_LATENCY_S * 20.0, 9)] * 5
    checks["P4_latency_injection_deterministic"] = {
        "expected": {"1.0": expected_1, "20.0": expected_20},
        "observed": latencies,
        "pass": latencies["1.0"] == expected_1 and latencies["20.0"] == expected_20,
    }

    # (e) server performs the correct state transition for every verb
    transitions: list[bool] = []
    for collection in TRAIN_COLLECTIONS_MULTI:
        for ident in (f"{SUBSTRATE_PREFIX[collection]}-151", f"{SUBSTRATE_PREFIX[collection]}-250"):
            _, detail, _ = client.call("GET", f"/{collection}/{ident}")
            transitions.append(detail.get("exists") is True)
            _, updated, _ = client.call("PUT", f"/{collection}/{ident}", {"status": "ok"})
            transitions.append(updated.get("updated") is True)
            _, deleted, _ = client.call("DELETE", f"/{collection}/{ident}")
            transitions.append(deleted.get("exists") is False)
    checks["P5_verb_state_transitions_correct"] = {
        "expected": "GET exists=True, PUT updated=True, DELETE exists=False for every served identifier",
        "observed": f"{sum(transitions)}/{len(transitions)} correct",
        "pass": all(transitions),
    }

    return {
        "seed": SEED,
        "checks": checks,
        "all_pass": all(c["pass"] for c in checks.values()),
        "note": "F5 substrate surface contract. If all_pass is false the frozen decision rule "
        "yields INCONCLUSIVE and no arm measurement is admissible.",
    }


def build_training_probe(client: Client) -> list[Observation]:
    """Small training slice for the surface probe only. Not a measurement arm."""
    observations: list[Observation] = []
    for collection in TRAIN_COLLECTIONS_MULTI:
        for num in range(151, 171):
            identifier = f"{SUBSTRATE_PREFIX[collection]}-{num}"
            for family in FAMILIES:
                observations.append(
                    Observation(
                        intent=family,
                        state={"collection": collection, "resource": identifier, "authenticated": True},
                        action={"method": FAMILY_VERB[family], "path": f"/{collection}/{identifier}"},
                        next_state={
                            "collection": collection,
                            "identifier": identifier,
                            "status": "ok",
                            "exists": family != "delete",
                        },
                        success=True,
                        provenance={"seed": SEED, "phase": "surface_probe"},
                    )
                )
    return observations


def malformed_probes(client: Client) -> list[dict[str, Any]]:
    """The preregistered malformed probes: empty, punctuation, wrong namespace."""
    probes = [
        ("empty-string", "read record  in items catalog", "items"),
        ("punctuation", "read record item!! in items catalog", "items"),
        ("wrong-namespace", "read record item-201 in widgets catalog", "items"),
    ]
    out: list[dict[str, Any]] = []
    for name, goal, expected_collection in probes:
        parsed = parse_goal(goal)
        record: dict[str, Any] = {
            "seed": SEED,
            "probe": name,
            "goal": goal,
            "parsed_recognised": bool(parsed),
            "parsed": parsed,
            "expected_collection": expected_collection,
        }
        if parsed:
            params = matcher_params(parsed)
            record["matcher_params"] = params
            status, payload, _ = client.call("GET", f"/{params['collection']}/{params['id']}")
            record["http_status"] = status
            record["http_response"] = payload
        out.append(record)
    return out


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    started = time.time()

    def sha256_file(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    registry_path = RAW / "_kernel_registry.jsonl"
    kernel = SpiderKernel(MechanismRegistry(registry_path), min_confidence=CONFIDENCE_THRESHOLD)

    with Substrate(latency_factor=1.0) as substrate:
        client = Client(substrate)

        probe = surface_probe(client, kernel)
        (RAW / "substrate_probe.json").write_text(
            json.dumps(probe, indent=2, sort_keys=True), encoding="utf-8"
        )
        print(f"[probe] all_pass={probe['all_pass']}", flush=True)
        if not probe["all_pass"]:
            failed = [k for k, v in probe["checks"].items() if not v["pass"]]
            print(f"[probe] FAILED: {failed}", flush=True)
            (RAW / "run_config.json").write_text(
                json.dumps(
                    {"seed": SEED, "aborted": True, "probe": probe,
                     "kernel_sha256": sha256_file(REPO / "src" / "spider" / "kernel.py")},
                    indent=2, sort_keys=True,
                ),
                encoding="utf-8",
            )
            return 2

        # -- induction, executed once and shared by both request frames -------- #
        client.set_latency_factor(1.0)
        before = client.mark()
        t0 = time.time()
        training_multi = build_training(client, TRAIN_COLLECTIONS_MULTI)
        multi_requests = client.mark() - before
        before = client.mark()
        training_single = build_training(client, TRAIN_COLLECTIONS_SINGLE)
        single_requests = client.mark() - before
        print(
            f"[induction] multi={len(training_multi)} obs/{multi_requests} req, "
            f"single={len(training_single)} obs/{single_requests} req, {time.time()-t0:.1f}s",
            flush=True,
        )
        (RAW / "induction_observations.jsonl").write_text(
            "\n".join(
                json.dumps(
                    {
                        "condition": condition,
                        "intent": o.intent,
                        "state": o.state,
                        "action": o.action,
                        "next_state": o.next_state,
                        "success": o.success,
                        "request_count": o.provenance.get("request_count"),
                    },
                    sort_keys=True,
                )
                for condition, group in (
                    ("multi", training_multi),
                    ("single_items", training_single),
                )
                for o in group
            )
            + "\n",
            encoding="utf-8",
        )

        # -- distillation ----------------------------------------------------- #
        A1 = kernel.distill_variability(training_multi, "A1")
        A2 = kernel.distill_variability(training_single, "A2")
        A3 = kernel.distill_parameterized(training_single, "A3")
        registry_path.write_text(
            "\n".join(
                json.dumps(m.as_dict(), sort_keys=True) for m in (A1 + A2 + A3)
            )
            + "\n",
            encoding="utf-8",
        )
        mechanisms_by_arm = {
            "A1": {m.intent: m for m in A1},
            "A2": {m.intent: m for m in A2},
            "A3": {m.intent: m for m in A3},
            "A4": {m.intent: m for m in A1},
            "A5": {m.intent: m for m in A1},
            "A6": {m.intent: m for m in A1},
        }
        modal = modal_slot_values(training_multi, A1)
        canonical = {m.intent: canonical_example(training_multi, m.intent) for m in A1}

        # -- measurement arms -------------------------------------------------- #
        tasks = cell_tasks()
        bind_rows: list[dict[str, Any]] = []
        exec_rows: list[dict[str, Any]] = []
        obs_rows: list[dict[str, Any]] = []
        rng = random.Random(SEED)
        for frame in FRAMES:
            for arm in ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"):
              # The lexical-overlap null's frozen definition leaves ties
              # undetermined and ties occur on every task of this frame, so both
              # extreme orderings are measured. build_result scores A4 at the
              # better of the two; the raw series keeps both.
              for tie_break in (("longest_first", "shortest_first") if arm == "A4" else ("longest_first",)):
                for mult in MULTIPLIERS:
                    client.set_latency_factor(mult)
                    scratchpad: dict[str, str] = {}
                    cell_mechanisms = mechanisms_by_arm.get(arm)
                    cell_modal = modal
                    for task in tasks:
                        mechanism = (
                            cell_mechanisms.get(task["family"])
                            if isinstance(cell_mechanisms, dict)
                            else None
                        )
                        record = run_task(
                            arm, mult, frame, task, client, kernel, mechanism,
                            modal.get(mechanism.mechanism_id, {}) if mechanism else {},
                            canonical.get(task["family"]), scratchpad, tie_break,
                        )
                        record["series"] = f"{arm}:{tie_break}" if arm == "A4" else arm
                        record["rng_draw"] = rng.random()
                        bind_rows.append(record)
                        exec_rows.append(
                            {
                                k: record[k]
                                for k in (
                                    "seed", "arm", "cost_multiplier", "frame", "task_id",
                                    "support", "family", "collection", "identifier_intended",
                                    "identifier_sent", "executed", "verified", "http_status",
                                    "request_count", "injected_latency_ms",
                                )
                            }
                        )
                    print(
                        f"[cell] frame={frame} arm={arm}/{tie_break} mult={mult:g} "
                        f"req={sum(r['request_count'] for r in bind_rows[-len(tasks):])}",
                        flush=True,
                    )
                    obs_rows.extend(client.drain())

        # -- malformed probes -------------------------------------------------- #
        client.set_latency_factor(1.0)
        probes = malformed_probes(client)
        obs_rows.extend(client.drain())

    (RAW / "observations.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in obs_rows) + "\n", encoding="utf-8"
    )
    (RAW / "bind_results.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in bind_rows) + "\n", encoding="utf-8"
    )
    (RAW / "exec_results.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in exec_rows) + "\n", encoding="utf-8"
    )
    (RAW / "probe_results.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in probes) + "\n", encoding="utf-8"
    )

    (RAW / "mechanisms_raw.json").write_text(
        json.dumps(
            {
                "A1_variability_multi": [m.as_dict() for m in A1],
                "A2_variability_single": [m.as_dict() for m in A2],
                "A3_declared_vocab_single": [m.as_dict() for m in A3],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    config = {
        "experiment_id": "EXP-PRODUCT-36314204238",
        "lane": "product",
        "seed": SEED,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "frames": FRAMES,
        "multipliers": MULTIPLIERS,
        "tasks_per_cell": TASKS_PER_CELL,
        "cells": len(FRAMES) * 9 * len(MULTIPLIERS),
        "total_tasks": len(bind_rows),
        "total_http_requests": substrate.request_count,
        "base_re_derivation_requests": BASE_RE_DERIVATION_REQUESTS,
        "inherited_requests": INHERITED_REQUESTS,
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "induction_observations": {
            "multi": len(training_multi),
            "single_items": len(training_single),
        },
        "induction_http_requests": {
            "multi": multi_requests,
            "single_items": single_requests,
        },
        "latency_injection": {"base_latency_s": BASE_LATENCY_S,
                              "rule": "base_latency_s * cost_multiplier, server-side, deterministic"},
        "cost_basis": "counted HTTP requests (prereg 6.5)",
        "hashes": {
            "src/spider/kernel.py": sha256_file(REPO / "src" / "spider" / "kernel.py"),
            "src/spider/variability.py": sha256_file(REPO / "src" / "spider" / "variability.py"),
            "src/spider/models.py": sha256_file(REPO / "src" / "spider" / "models.py"),
            "substrate.py": sha256_file(HERE / "substrate.py"),
            "run_experiment.py": sha256_file(HERE / "run_experiment.py"),
            "request.json": sha256_file(HERE / "request.json"),
            "spec.json": sha256_file(HERE / "spec.json"),
            "prereg.md": sha256_file(HERE / "prereg.md"),
        },
        "wall_clock_s": round(time.time() - started, 2),
    }
    (RAW / "run_config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps({k: config[k] for k in ("total_tasks", "total_http_requests", "wall_clock_s")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

