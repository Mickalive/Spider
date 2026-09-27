"""EXECUTE runner for EXP-PRODUCT-36293260887 (product lane, C-PARAM-INHERIT).

Executes the frozen design in spec.json / prereg.md against the hash-verified
substrate reused from EXP-PRODUCT-36272385776 (sha256 d3fe358e...).

Cost basis (single, declared): HTTP requests actually issued and counted.

TWO DISCLOSED PROTOCOL AMENDMENTS, both forced by the frozen substrate and
neither a preregistration change. Both are recorded in result.json.validity_notes.

  A1 TOKEN RE-AUTHENTICATION. The substrate gives each static token a budget of
     TOKEN_EXPIRY = 100 requests, counted in a monotone shared store, and
     exposes NO token-issuance endpoint (prereg section 7 claims "Bearer token
     issuance -> validation"; that endpoint returns 401). Once exhausted, a
     token can never be renewed. A frozen design of this size needs well over
     100 requests. Re-authentication is therefore stood in for by clearing the
     budget, and EVERY re-auth is charged as one real HTTP request so that the
     cost accounting stays honest and B-COLD keeps genuine dynamic range.

  A2 RESOURCE-B SAMPLE SIZE. The substrate exposes 126 resource-B identifiers.
     Three families therefore admit at most 42 tasks each, below the
     preregistered n >= 50. Resource-A arms reach 50 per family.

Writes RAW EVIDENCE only:
  raw_evidence/observations.jsonl, task_results.jsonl, probe_results.jsonl,
  mechanisms.json, derived.json, bootstrap.json
No interpretation is written by this file.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
import sys
import tempfile
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

EXP = Path(__file__).resolve().parent
REPO = EXP.parents[2]
RAW = EXP / "raw_evidence"
sys.path.insert(0, str(REPO / "src"))

from spider.kernel import SpiderKernel  # noqa: E402
from spider.models import Observation, ResolutionStatus  # noqa: E402
from spider.registry import MechanismRegistry  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "spider_substrate", EXP.parent / "EXP-PRODUCT-36272385776" / "substrate.py"
)
substrate = importlib.util.module_from_spec(_spec)
sys.modules["spider_substrate"] = substrate
_spec.loader.exec_module(substrate)

SEED = 42
BOOTSTRAP_B = 5000
N_PER_FAMILY = 50
NEGATIVE_PROBES_PER_ARM = 60
TOKEN = "tok-owner-a"

INTENT_NS = {
    "read-item": ["read-product"],
    "update-item": ["update-product"],
    "delete-item": ["delete-product"],
}

FAMILIES = [
    {"family": "read", "method": "GET", "intent_a": "read-item", "intent_b": "read-product", "ok": 200},
    {"family": "update", "method": "PUT", "intent_a": "update-item", "intent_b": "update-product", "ok": 200},
    {"family": "delete", "method": "DELETE", "intent_a": "delete-item", "intent_b": "delete-product", "ok": 200},
]

PC_A_IDS = {f: substrate.RESOURCE_A_IDS[i * 50:(i + 1) * 50] for i, f in enumerate(["read", "update", "delete"])}
TRAIN_A_IDS = substrate.RESOURCE_A_IDS[150:200]
B_IDS = list(substrate.RESOURCE_B_IDS)
B_FAMILY_IDS = {f["family"]: B_IDS[i::len(FAMILIES)] for i, f in enumerate(FAMILIES)}


# --------------------------------------------------------------------------- #
# Cost-counting HTTP client with the disclosed re-auth amendment
# --------------------------------------------------------------------------- #

class Client:
    def __init__(self, base_url: str, sub):
        self.base = base_url
        self.sub = sub
        self.requests = 0
        self.reauths = 0
        self.by_path: Counter = Counter()

    def _raw(self, path, method, body, auth):
        self.requests += 1
        self.by_path[path.split("?")[0]] += 1
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method)
        if data is not None:
            req.add_header("Content-Type", "application/json")
        if auth:
            req.add_header("Authorization", f"Bearer {TOKEN}")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read()
                return resp.status, (json.loads(raw) if raw else {})
        except urllib.error.HTTPError as e:
            raw = e.read()
            try:
                return e.code, (json.loads(raw) if raw else {})
            except ValueError:
                return e.code, {}
        except Exception:
            return 0, {}

    def call(self, path, method="GET", body=None, auth=True):
        status, payload = self._raw(path, method, body, auth)
        if auth and status == 401:
            # Amendment A1: charge the re-auth, then stand in for token re-issue.
            self.requests += 1
            self.reauths += 1
            self.sub.store.request_counts.clear()
            status, payload = self._raw(path, method, body, auth)
        return status, payload

    def mark(self) -> int:
        return self.requests


def act(client: Client, path: str, method: str, identifier: str):
    if method == "PUT":
        return client.call(path, method="PUT", body={"label": f"lab-{identifier}"})
    if method == "DELETE":
        return client.call(path, method="DELETE")
    return client.call(path)


def make_observation(intent, collection, identifier, method):
    return Observation(
        intent=intent,
        state={"authenticated": True, "collection": collection},
        action={"method": method, "path": f"/{collection}/{identifier}"},
        next_state={"status": 200, "ok": True, "id": identifier},
        success=True,
    )


def task_success(status, payload, identifier, expected_status, executed_method, required_method):
    """End-to-end task success, at three levels of strictness.

    The substrate is permissive: a GET where a DELETE was required still returns
    200 with the right entity. Counting that as success would let an arm that
    applied the WRONG VERB score identically to a correct one, and would make
    every "matched end-to-end success" comparison meaningless. Success therefore
    requires the required verb, the expected status, and the right entity.
    """
    if executed_method is not None and executed_method != required_method:
        return False
    if status != expected_status:
        return False
    if payload.get("id") not in (identifier, None):
        return False
    if required_method == "DELETE":
        return bool(payload.get("deleted")) or bool(payload.get("id"))
    return payload.get("id") == identifier or required_method == "GET" and status == expected_status


# --------------------------------------------------------------------------- #
# Arms
# --------------------------------------------------------------------------- #

def collect_observations(client: Client, sub):
    obs, start = [], client.mark()
    for spec_f in FAMILIES:
        for identifier in TRAIN_A_IDS:
            status, _ = act(client, f"/items/{identifier}", spec_f["method"], identifier)
            if spec_f["method"] == "DELETE":
                sub.store.seed("items", identifier)
            if status == 200:
                obs.append(make_observation(spec_f["intent_a"], "items", identifier, spec_f["method"]))
    return obs, client.mark() - start


def fresh(sub) -> None:
    """Reset substrate state and reseed. Prereg split_integrity requires the
    store to be reset between arms; without this, an arm that issues DELETE
    silently starves a later arm of the entities it needs to read."""
    sub.reset()
    sub.seed_many("items", substrate.RESOURCE_A_IDS)
    sub.seed_many("products", substrate.RESOURCE_B_IDS)


def run_bcold(client: Client, sub):
    """B-COLD: per-task EXECUTED discovery. Auth, verb/schema discovery,
    existence confirmation, then the target verb. No count is configured."""
    rows = []
    for spec_f in FAMILIES:
        collection = "products"
        for identifier in B_FAMILY_IDS[spec_f["family"]]:
            sub.store.seed(collection, identifier)
            before = client.mark()
            client.call(f"/{collection}/{identifier}")            # auth + existence
            client.call("/")                                      # verb/schema discovery
            client.call(f"/{collection}?limit=100")               # filtered listing
            status, payload = act(client, f"/{collection}/{identifier}", spec_f["method"], identifier)
            rows.append({
                "arm": "B-COLD", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status,
                "http_ok": status == 200,
                "executed_method": spec_f["method"], "required_method": spec_f["method"],
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        spec_f["method"], spec_f["method"]),
            })
    return rows


def run_mechanism_arm(client, kernel, sub, arm, use_b_intent, collection, family_ids, force=False):
    """Resolve -> bind -> EXECUTE THE MECHANISM'S OWN ACTION -> verify.

    The verb is taken from the resolved action_template, never from the task
    family. Supplying the family's verb would silently rescue a mechanism whose
    induced verb is wrong, which is precisely what the null arm must expose.
    """
    rows = []
    for spec_f in FAMILIES:
        intent = spec_f["intent_b"] if use_b_intent else spec_f["intent_a"]
        slots = {s for m in kernel.registry.all() for s in m.parameter_slots}
        for identifier in family_ids[spec_f["family"]]:
            before = client.mark()
            ctx = {"authenticated": True, "collection": collection}
            params = {"id": identifier}
            if "collection" in slots:
                params["collection"] = collection
            res = (kernel.force_resolve if force else kernel.resolve)(intent, ctx, params)
            status, payload = 0, {}
            bound_path = executed_method = None
            if res.status is ResolutionStatus.EXECUTABLE:
                bound_path = res.bound_action["path"]
                executed_method = res.bound_action.get("method")
                sub.store.seed(collection, identifier)
                status, payload = act(client, bound_path, executed_method, identifier)
            used = client.mark() - before
            rows.append({
                "arm": arm, "family": spec_f["family"], "identifier": identifier,
                "requests": used, "status": status, "http_ok": status == 200,
                "resolution": res.status.value, "bound_path": bound_path,
                "executed_method": executed_method, "required_method": spec_f["method"],
                "mechanism_id": res.mechanism_id,
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        executed_method, spec_f["method"]),
            })
    return rows


def run_literal_replay(client, training):
    by_intent: dict[str, list[str]] = {}
    for o in training:
        by_intent.setdefault(o.intent, []).append(o.action["path"])
    rows = []
    for spec_f in FAMILIES:
        paths = by_intent.get(spec_f["intent_a"], [f"/items/{TRAIN_A_IDS[0]}"])
        for index, identifier in enumerate(B_FAMILY_IDS[spec_f["family"]]):
            literal = paths[index % len(paths)]
            before = client.mark()
            status, payload = act(client, literal, spec_f["method"], identifier)
            rows.append({
                "arm": "B-LITERAL-REPLAY", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status, "http_ok": status == 200,
                "bound_path": literal, "returned_id": payload.get("id"),
                "executed_method": spec_f["method"], "required_method": spec_f["method"],
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        spec_f["method"], spec_f["method"]),
            })
    return rows


def embed(text: str) -> dict[str, float]:
    vec: dict[str, float] = {}
    padded = f"^{text}$"
    for n in (3, 4):
        for i in range(len(padded) - n + 1):
            h = int(hashlib.sha256(padded[i:i + n].encode()).hexdigest()[:8], 16) % 512
            vec[h] = vec.get(h, 0.0) + 1.0
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    return {k: v / norm for k, v in vec.items()}


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(k, 0.0) for k, v in a.items())


def run_retrieval_k5(client, training):
    by_intent: dict[str, list[tuple]] = {}
    for o in training:
        by_intent.setdefault(o.intent, []).append(
            (o, embed(f"{o.intent}|{json.dumps(o.state, sort_keys=True)}")))
    rows = []
    for spec_f in FAMILIES:
        pool = by_intent.get(spec_f["intent_a"], [])
        query = embed(f"{spec_f['intent_b']}|authenticated=True,collection=products")
        for identifier in B_FAMILY_IDS[spec_f["family"]]:
            ranked = sorted(pool, key=lambda pair: -cosine(query, pair[1]))[:5]
            before = client.mark()
            status, payload = 0, {}
            bound = None
            for o, _v in ranked:
                bound = o.action["path"]
                status, payload = act(client, bound, spec_f["method"], identifier)
                if status == 200:
                    break
            rows.append({
                "arm": "B-RETRIEVAL-K5", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status, "http_ok": status == 200,
                "bound_path": bound, "returned_id": payload.get("id"),
                "executed_method": spec_f["method"], "required_method": spec_f["method"],
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        spec_f["method"], spec_f["method"]),
            })
    return rows


def run_probes(kernel, arm, include_collection):
    rng = random.Random(SEED)
    rows = []
    ids = [f"SKU-{c}" for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] + [f"PROD-{i}" for i in range(100, 200)]
    for i in range(NEGATIVE_PROBES_PER_ARM):
        kind = ["out_of_support_binding", "invalid_intent", "malformed_params"][i % 3]
        intent = "read-widget" if kind == "invalid_intent" else FAMILIES[i % 3]["intent_b"]
        if kind == "malformed_params":
            params = {"id": ""} if i % 2 else {}
        elif kind == "out_of_support_binding":
            params = {"id": ids[rng.randrange(len(ids))] + "!!unsupported!!"}
        else:
            params = {"id": ids[rng.randrange(len(ids))]}
        if include_collection:
            params["collection"] = "products"
        res = kernel.resolve(intent, {"authenticated": True, "collection": "products"}, params)
        rows.append({
            "arm": arm, "probe_index": i, "kind": kind, "intent": intent,
            "executed": res.status is ResolutionStatus.EXECUTABLE, "status": res.status.value,
        })
    return rows


# --------------------------------------------------------------------------- #
# Family-stratified bootstrap
# --------------------------------------------------------------------------- #

def stratified_bootstrap(by_family, stat, b=BOOTSTRAP_B):
    rng = random.Random(SEED)
    fams = sorted(by_family)
    if not fams:
        return {"point": None, "ci_low": None, "ci_high": None, "n": 0, "B": b, "n_strata": 0}
    point = stat({f: by_family[f] for f in fams})
    draws = []
    for _ in range(b):
        sample = {f: ([by_family[f][rng.randrange(len(by_family[f]))] for _ in range(len(by_family[f]))]
                      if by_family[f] else []) for f in fams}
        try:
            draws.append(stat(sample))
        except (ZeroDivisionError, ValueError):
            continue
    draws.sort()
    if not draws:
        return {"point": point, "ci_low": None, "ci_high": None, "n": 0, "B": b, "n_strata": len(fams)}
    return {
        "point": point, "ci_low": draws[int(0.025 * len(draws))],
        "ci_high": draws[min(len(draws) - 1, int(0.975 * len(draws)))],
        "n": len(draws), "B": b, "n_strata": len(fams),
    }


def rate(sample):
    vals = [v for f in sample for v in sample[f]]
    return sum(vals) / len(vals) if vals else float("nan")


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    sub = substrate.Substrate()
    sub.seed_many("items", substrate.RESOURCE_A_IDS)
    sub.seed_many("products", substrate.RESOURCE_B_IDS)
    client = Client(sub.base_url, sub)

    training, induction_cost = collect_observations(client, sub)
    (RAW / "observations.jsonl").write_text("\n".join(json.dumps({
        "intent": o.intent, "state": o.state, "action": o.action,
        "next_state": o.next_state, "success": o.success}, sort_keys=True) for o in training) + "\n")

    td = tempfile.TemporaryDirectory()
    reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
    kernel = SpiderKernel(reg, min_confidence=0.8, intent_namespace_map=INTENT_NS)

    treatment_mechs = kernel.distill_parameterized(training, mechanism_prefix="treatment")
    ident_mechs = kernel.distill_parameterized(
        training, mechanism_prefix="ident", induce_identity_slots=True)

    rng = random.Random(SEED)
    labels = [o.intent for o in training]
    rng.shuffle(labels)
    shuffled = [Observation(intent=l, state=o.state, action=o.action,
                            next_state=o.next_state, success=o.success)
                for o, l in zip(training, labels)]
    nc_mechs = kernel.distill_parameterized(
        shuffled, mechanism_prefix="nc", induce_identity_slots=True)

    (RAW / "mechanisms.json").write_text(json.dumps({
        "treatment_pinned_collection": [m.as_dict() for m in treatment_mechs],
        "treatment_identity_slot": [m.as_dict() for m in ident_mechs],
        "nc_shuffled_intent": [m.as_dict() for m in nc_mechs],
        "n_training_observations": len(training),
        "n_distinct_training_ids": len(TRAIN_A_IDS),
    }, indent=2, sort_keys=True) + "\n")

    rows: list[dict] = []
    fresh(sub)
    rows += run_bcold(client, sub)

    fresh(sub)
    reg.replace(treatment_mechs)
    rows += run_mechanism_arm(client, kernel, sub, "PC-SAME-RESOURCE", False, "items", PC_A_IDS)
    rows += run_mechanism_arm(client, kernel, sub, "Treatment", True, "products", B_FAMILY_IDS)

    fresh(sub)
    rows += run_literal_replay(client, training)
    fresh(sub)
    rows += run_retrieval_k5(client, training)

    fresh(sub)
    reg.replace(ident_mechs)
    rows += run_mechanism_arm(client, kernel, sub, "Treatment-IDENTITY-SLOT", True, "products", B_FAMILY_IDS)
    fresh(sub)
    rows += run_mechanism_arm(client, kernel, sub, "Treatment-IDENTITY-SLOT-FORCED", True,
                              "products", B_FAMILY_IDS, force=True)

    fresh(sub)
    reg.replace(nc_mechs)
    rows += run_mechanism_arm(client, kernel, sub, "NC-SHUFFLED-INTENT", True, "products", B_FAMILY_IDS)
    fresh(sub)
    rows += run_mechanism_arm(client, kernel, sub, "NC-SHUFFLED-INTENT-FORCED", True,
                              "products", B_FAMILY_IDS, force=True)

    (RAW / "task_results.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n")

    reg.replace(treatment_mechs)
    tr_probes = run_probes(kernel, "Treatment", include_collection=False)
    reg.replace(ident_mechs)
    id_probes = run_probes(kernel, "Treatment-IDENTITY-SLOT", include_collection=True)
    reg.replace(nc_mechs)
    nc_probes = run_probes(kernel, "NC-SHUFFLED-INTENT", include_collection=True)
    probe_rows = tr_probes + id_probes + nc_probes
    (RAW / "probe_results.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in probe_rows) + "\n")

    def arm(name):
        return [r for r in rows if r["arm"] == name]

    def fams(name):
        return {f: [r for r in arm(name) if r["family"] == f] for f in {r["family"] for r in arm(name)}}

    def boot(name, key):
        return stratified_bootstrap(
            {f: [float(r[key]) for r in rs] for f, rs in fams(name).items()}, rate)

    arms = sorted({r["arm"] for r in rows})
    costs = {n: boot(n, "requests") for n in arms}
    successes = {n: boot(n, "success") for n in arms}
    http_oks = {n: boot(n, "http_ok") for n in arms}

    t_cost = costs["Treatment"]["point"]
    n_treat = len(arm("Treatment"))

    def amortized(base):
        return (induction_cost + n_treat * t_cost) / (n_treat * base) if base else None

    b_cost = costs["B-COLD"]["point"]
    n_max = math.ceil(induction_cost / (b_cost - t_cost)) if b_cost and b_cost > t_cost else None

    def per_family(name):
        out = {}
        for f, rs in sorted(fams(name).items()):
            out[f] = {
                "n": len(rs),
                "success_rate": sum(r["success"] for r in rs) / len(rs) if rs else None,
                "http_ok_rate": sum(r["http_ok"] for r in rs) / len(rs) if rs else None,
                "mean_requests": sum(r["requests"] for r in rs) / len(rs) if rs else None,
                "resolution_counts": dict(Counter(r.get("resolution", "n/a") for r in rs)),
            }
        return out

    def probe_rate(arm_name, key="executed"):
        rs = [p for p in probe_rows if p["arm"] == arm_name]
        return (sum(bool(p[key]) for p in rs) / len(rs)) if rs else None

    ident_mech_slots = sorted({s for m in ident_mechs for s in m.parameter_slots})
    pinned_bound = sorted({r.get("bound_path") for r in arm("Treatment") if r.get("bound_path")})
    ident_bound = sorted({r.get("bound_path") for r in arm("Treatment-IDENTITY-SLOT") if r.get("bound_path")})
    nc_wrong_verb = sum(
        1 for r in arm("NC-SHUFFLED-INTENT-FORCED")
        if r.get("executed_method") and r["executed_method"] != r["required_method"])

    # Break-even is solved directly, and compared against N_MAX computed from the
    # prereg formula, to test whether clause F6 can discriminate at all.
    def break_even_direct(bc, tc, ic):
        if tc >= bc:
            return None
        return math.ceil(ic / (bc - tc))

    n_per_family = {
        n: {f: len(rs) for f, rs in fams(n).items()} for n in arms
    }
    probe_by_kind = {}
    for p in probe_rows:
        key = f"{p['arm']}|{p['kind']}"
        probe_by_kind.setdefault(key, {"n": 0, "executed": 0})
        probe_by_kind[key]["n"] += 1
        probe_by_kind[key]["executed"] += int(p["executed"])

    derived = {
        "arms": arms,
        "arm_n": {n: len(arm(n)) for n in arms},
        "arm_n_per_family": n_per_family,
        "arm_meets_n50_per_family": {
            n: all(v >= 50 for v in d.values()) for n, d in n_per_family.items()},
        "arm_per_family": {n: per_family(n) for n in arms},
        "arm_success_rate": successes,
        "arm_http_ok_rate": http_oks,
        "arm_mean_requests_per_task": costs,
        "matched_end_to_end_success": {
            "treatment": successes["Treatment"]["point"],
            "treatment_identity_slot": successes["Treatment-IDENTITY-SLOT"]["point"],
            "b_literal_replay": successes["B-LITERAL-REPLAY"]["point"],
            "b_retrieval_k5": successes["B-RETRIEVAL-K5"]["point"],
            "b_cold": successes["B-COLD"]["point"],
        },
        "amortized_cost_ratio_vs_bcold": amortized(costs["B-COLD"]["point"]),
        "amortized_cost_ratio_vs_literal_replay": amortized(costs["B-LITERAL-REPLAY"]["point"]),
        "amortized_cost_ratio_vs_retrieval_k5": amortized(costs["B-RETRIEVAL-K5"]["point"]),
        "induction_cost_total": induction_cost,
        "n_max_derived_at_execute": n_max,
        "n_max_frozen": None,
        "break_even_transfer_tasks": n_max,
        "pinned_treatment_bound_paths": pinned_bound,
        "identity_slot_bound_path_examples": ident_bound[:4] + ["..."],
        "identity_slot_bound_path_n_distinct": len(ident_bound),
        "nc_forced_wrong_verb_count": nc_wrong_verb,
        "identity_mechanism_slots": ident_mech_slots,
        "identity_mechanism_paths": sorted({m.action_template["path"] for m in ident_mechs}),
        "identity_mechanism_confidence": {m.intent: m.confidence for m in ident_mechs},
        "nc_mechanism_confidence": {m.intent: m.confidence for m in nc_mechs},
        "treatment_prefix_preserved": all(
            p and p != "${id}" and "${" in p for p in
            {m.action_template["path"] for m in treatment_mechs}),
        "probe_false_accept_rate": {
            n: probe_rate(n) for n in sorted({p["arm"] for p in probe_rows})},
        "probe_false_accept_by_kind": probe_by_kind,
        "probe_abstention_precision": {
            n: (1.0 - probe_rate(n)) if probe_rate(n) is not None else None
            for n in sorted({p["arm"] for p in probe_rows})},
        "nc_cost_ratio_vs_bcold": (costs["NC-SHUFFLED-INTENT"]["point"] / b_cost) if b_cost else None,
        "n_max_from_prereg_formula": n_max,
        "break_even_solved_directly": break_even_direct(b_cost, t_cost, induction_cost),
        "f6_is_identity": n_max == break_even_direct(b_cost, t_cost, induction_cost),
        "reauths_total": client.reauths,
        "http_requests_total": client.requests,
    }
    (RAW / "derived.json").write_text(json.dumps(derived, indent=2, sort_keys=True, default=str) + "\n")
    print(json.dumps(derived, indent=2, sort_keys=True, default=str))
    sub.stop()
    td.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
