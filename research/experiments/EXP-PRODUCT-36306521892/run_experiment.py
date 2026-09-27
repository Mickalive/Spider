"""EXECUTE runner for EXP-PRODUCT-36306521892 (product lane, C-PRODUCT-ECON).

Executes the frozen dual-regime design in spec.json / prereg.md:

  1. Probe substrate surface contract (both regimes)
  2. Collect 150 induction observations from resource A (items) in cheap regime
  3. Induce mechanisms via kernel.distill_parameterized (committed at HEAD)
  4. Run arms in both regimes with fresh() between arms:
     B-COLD, B-SCRATCHPAD, B-NO-MEMORY, B-INSTRUCTIONS, B-RETRIEVAL-K5,
     INHERITANCE, PC-SAME-RESOURCE (cheap only), NC-SHUFFLED-INTENT
  5. Run NC-FALSE-ACCEPT probes
  6. Write RAW EVIDENCE only (observations, task_results, probe_results,
     mechanisms, substrate_probe). Derived metrics are computed by
     build_result.py.

Cost basis (single, declared): HTTP requests actually issued and counted by
the client. No imported per-observation constants, no jitter, no f-scaled
substitution. Re-authentication in the costly regime is charged as one real
HTTP request per re-login.
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
sys.path.insert(0, str(EXP))

from spider.kernel import SpiderKernel  # noqa: E402
from spider.models import Observation, ResolutionStatus  # noqa: E402
from spider.registry import MechanismRegistry  # noqa: E402

_spec = importlib.util.spec_from_file_location("dual_substrate", EXP / "substrate.py")
substrate = importlib.util.module_from_spec(_spec)
sys.modules["dual_substrate"] = substrate
_spec.loader.exec_module(substrate)

SEED = 42
BOOTSTRAP_B = 5000
NEGATIVE_PROBES_PER_ARM = 60

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

# 50 training ids (item-151..item-200); 150 held-out ids (item-1..item-150) for PC.
TRAIN_A_IDS = substrate.RESOURCE_A_IDS[150:200]
PC_A_IDS = {f["family"]: substrate.RESOURCE_A_IDS[i * 50:(i + 1) * 50] for i, f in enumerate(FAMILIES)}
B_IDS = list(substrate.RESOURCE_B_IDS)
B_FAMILY_IDS = {f["family"]: B_IDS[i::len(FAMILIES)] for i, f in enumerate(FAMILIES)}


# --------------------------------------------------------------------------- #
# Cost-counting HTTP client
# --------------------------------------------------------------------------- #


class Client:
    def __init__(self, base_url: str, mode: str):
        self.base = base_url
        self.mode = mode
        self.requests = 0
        self.reauths = 0
        self.token: str | None = None

    def _http(self, path: str, method: str = "GET", body=None, auth: bool = False):
        self.requests += 1
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method)
        if data is not None:
            req.add_header("Content-Type", "application/json")
        if auth:
            req.add_header("Authorization", f"Bearer {self.token}")
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

    def _login(self) -> None:
        self.requests += 1
        req = urllib.request.Request(self.base + "/auth/login", method="POST", data=b"{}")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            self.token = json.loads(resp.read())["token"]

    def call(self, path: str, method: str = "GET", body=None):
        if self.mode == "cheap":
            return self._http(path, method, body, auth=False)
        if self.token is None:
            self._login()
        status, payload = self._http(path, method, body, auth=True)
        if status == 401:
            # Token expired: charge the re-login as one real request, then retry.
            self.reauths += 1
            self._login()
            status, payload = self._http(path, method, body, auth=True)
        return status, payload

    def mark(self) -> int:
        return self.requests


def act(client: Client, path: str, method: str, identifier: str):
    if method == "PUT":
        return client.call(path, method="PUT", body={"label": f"lab-{identifier}"})
    if method == "DELETE":
        return client.call(path, method="DELETE")
    return client.call(path)


def task_success(status, payload, identifier, expected_status, executed_method, required_method):
    """Success = verb AND status AND returned entity."""
    if executed_method is not None and executed_method != required_method:
        return False
    if status != expected_status:
        return False
    if required_method == "DELETE":
        return bool(payload.get("deleted")) and payload.get("id") == identifier
    return payload.get("id") == identifier


def make_observation(intent, collection, identifier, method):
    return Observation(
        intent=intent,
        state={"collection": collection},
        action={"method": method, "path": f"/{collection}/{identifier}"},
        next_state={"status": 200, "id": identifier, "ok": True},
        success=True,
    )


# --------------------------------------------------------------------------- #
# Surface contract probe
# --------------------------------------------------------------------------- #


def probe_surface_contract(mode: str) -> dict:
    sub = substrate.Substrate(mode)
    sub.seed_many("items", substrate.RESOURCE_A_IDS[:5])
    sub.seed_many("products", substrate.RESOURCE_B_IDS[:5])
    client = Client(sub.base_url, mode)
    result = {"mode": mode, "checks": {}}

    if mode == "costly":
        # /auth/login returns token
        status, payload = client.call("/auth/login", method="POST", body={})
        result["checks"]["auth_login"] = {"status": status, "has_token": "token" in payload}
        token = payload.get("token", "")
        # /schema returns verbs
        req = urllib.request.Request(sub.base_url + "/schema")
        req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req) as resp:
            schema = json.loads(resp.read())
        result["checks"]["schema"] = {"status": resp.status, "has_verbs": "verbs" in schema}
        # pagination
        req = urllib.request.Request(sub.base_url + "/products?page=1&page_size=2")
        req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req) as resp:
            page = json.loads(resp.read())
        result["checks"]["pagination"] = {"status": resp.status, "count": page.get("count")}
        # token expiry: issue a fresh token and burn it
        status2, payload2 = client.call("/auth/login", method="POST", body={})
        tok2 = payload2.get("token", "")
        expired = False
        for _ in range(substrate.TOKEN_EXPIRY + 1):
            req = urllib.request.Request(sub.base_url + "/products/SKU-A")
            req.add_header("Authorization", f"Bearer {tok2}")
            try:
                with urllib.request.urlopen(req) as resp:
                    last = resp.status
            except urllib.error.HTTPError as e:
                last = e.code
                if e.code == 401:
                    expired = True
                    break
        result["checks"]["token_expires"] = {"expired": expired, "expiry": substrate.TOKEN_EXPIRY}
    else:
        # cheap: direct GET, no auth
        status, payload = client.call("/products/SKU-A")
        result["checks"]["direct_get"] = {"status": status, "id": payload.get("id")}
        # no auth header required
        req = urllib.request.Request(sub.base_url + "/products/SKU-A")
        with urllib.request.urlopen(req) as resp:
            result["checks"]["no_auth_required"] = {"status": resp.status}
        # no schema endpoint
        req = urllib.request.Request(sub.base_url + "/schema")
        try:
            with urllib.request.urlopen(req) as resp:
                result["checks"]["no_schema"] = {"status": resp.status}
        except urllib.error.HTTPError as e:
            result["checks"]["no_schema"] = {"status": e.code}

    sub.stop()
    return result


# --------------------------------------------------------------------------- #
# Induction
# --------------------------------------------------------------------------- #


def fresh(sub) -> None:
    sub.reset()
    sub.seed_many("items", substrate.RESOURCE_A_IDS)
    sub.seed_many("products", substrate.RESOURCE_B_IDS)


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


# --------------------------------------------------------------------------- #
# Arms
# --------------------------------------------------------------------------- #


def run_bcold(client: Client, sub, mode: str):
    """B-COLD: per-task executed cold discovery."""
    rows = []
    for spec_f in FAMILIES:
        collection = "products"
        for identifier in B_FAMILY_IDS[spec_f["family"]]:
            sub.store.seed(collection, identifier)
            before = client.mark()
            if mode == "costly":
                client.call("/schema")
                client.call(f"/{collection}?page=1&page_size=10")
            status, payload = act(client, f"/{collection}/{identifier}", spec_f["method"], identifier)
            if spec_f["method"] == "DELETE":
                sub.store.seed(collection, identifier)
            rows.append({
                "arm": f"B-COLD-{mode.upper()}", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status,
                "http_ok": status == 200,
                "executed_method": spec_f["method"], "required_method": spec_f["method"],
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        spec_f["method"], spec_f["method"]),
            })
    return rows


def run_scratchpad(client: Client, sub, mode: str):
    """B-SCRATCHPAD: task 1 pays cold cost, tasks 2..n reuse (1 req/task)."""
    rows = []
    for spec_f in FAMILIES:
        collection = "products"
        ids = B_FAMILY_IDS[spec_f["family"]]
        for idx, identifier in enumerate(ids):
            sub.store.seed(collection, identifier)
            before = client.mark()
            if idx == 0:
                if mode == "costly":
                    client.call("/schema")
                    client.call(f"/{collection}?page=1&page_size=10")
            status, payload = act(client, f"/{collection}/{identifier}", spec_f["method"], identifier)
            if spec_f["method"] == "DELETE":
                sub.store.seed(collection, identifier)
            rows.append({
                "arm": f"B-SCRATCHPAD-{mode.upper()}", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status,
                "http_ok": status == 200,
                "executed_method": spec_f["method"], "required_method": spec_f["method"],
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        spec_f["method"], spec_f["method"]),
            })
    return rows


def run_no_memory(client: Client, sub, mode: str):
    """B-NO-MEMORY: deterministic executor, hard-coded auth + pagination, no registry."""
    rows = []
    for spec_f in FAMILIES:
        collection = "products"
        for identifier in B_FAMILY_IDS[spec_f["family"]]:
            sub.store.seed(collection, identifier)
            before = client.mark()
            if mode == "costly":
                # Hard-coded pagination (schema is compiled in, no discovery).
                client.call(f"/{collection}?page=1&page_size=10")
            status, payload = act(client, f"/{collection}/{identifier}", spec_f["method"], identifier)
            if spec_f["method"] == "DELETE":
                sub.store.seed(collection, identifier)
            rows.append({
                "arm": f"B-NO-MEMORY-{mode.upper()}", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status,
                "http_ok": status == 200,
                "executed_method": spec_f["method"], "required_method": spec_f["method"],
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        spec_f["method"], spec_f["method"]),
            })
    return rows


def run_instructions(client: Client, sub, mode: str):
    """B-INSTRUCTIONS: pre-provided auth/schema/pagination instructions, agent executes."""
    rows = []
    for spec_f in FAMILIES:
        collection = "products"
        for identifier in B_FAMILY_IDS[spec_f["family"]]:
            sub.store.seed(collection, identifier)
            before = client.mark()
            if mode == "costly":
                # Instructions say: paginate to discover, then execute. No schema call.
                client.call(f"/{collection}?page=1&page_size=10")
            status, payload = act(client, f"/{collection}/{identifier}", spec_f["method"], identifier)
            if spec_f["method"] == "DELETE":
                sub.store.seed(collection, identifier)
            rows.append({
                "arm": f"B-INSTRUCTIONS-{mode.upper()}", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status,
                "http_ok": status == 200,
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


def run_retrieval_k5(client: Client, sub, mode: str, training):
    """B-RETRIEVAL-K5: retrieval over prior trajectories, then execute top match."""
    by_intent: dict[str, list[tuple]] = {}
    for o in training:
        by_intent.setdefault(o.intent, []).append(
            (o, embed(f"{o.intent}|{json.dumps(o.state, sort_keys=True)}")))
    rows = []
    for spec_f in FAMILIES:
        collection = "products"
        pool = by_intent.get(spec_f["intent_a"], [])
        query = embed(f"{spec_f['intent_b']}|collection=products")
        for identifier in B_FAMILY_IDS[spec_f["family"]]:
            sub.store.seed(collection, identifier)
            ranked = sorted(pool, key=lambda pair: -cosine(query, pair[1]))[:5]
            before = client.mark()
            status, payload = 0, {}
            bound_path = None
            executed_method = None
            if not ranked:
                # No prior trajectory: fall back to cold.
                if mode == "costly":
                    client.call("/schema")
                    client.call(f"/{collection}?page=1&page_size=10")
                status, payload = act(client, f"/{collection}/{identifier}", spec_f["method"], identifier)
                bound_path = f"/{collection}/{identifier}"
                executed_method = spec_f["method"]
            else:
                # Execute the top match's verb with the current identifier.
                o, _v = ranked[0]
                executed_method = o.action["method"]
                bound_path = f"/{collection}/{identifier}"
                status, payload = act(client, bound_path, executed_method, identifier)
            if spec_f["method"] == "DELETE":
                sub.store.seed(collection, identifier)
            rows.append({
                "arm": f"B-RETRIEVAL-K5-{mode.upper()}", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status,
                "http_ok": status == 200,
                "bound_path": bound_path,
                "executed_method": executed_method, "required_method": spec_f["method"],
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        executed_method, spec_f["method"]),
            })
    return rows


def run_inheritance_arm(client, kernel, sub, mode: str):
    """INHERITANCE: resolve mechanism -> bind -> execute the mechanism's own action."""
    rows = []
    for spec_f in FAMILIES:
        collection = "products"
        for identifier in B_FAMILY_IDS[spec_f["family"]]:
            sub.store.seed(collection, identifier)
            before = client.mark()
            ctx = {"collection": collection}
            params = {"id": identifier, "collection": collection}
            res = kernel.resolve(spec_f["intent_b"], ctx, params)
            status, payload = 0, {}
            bound_path = executed_method = None
            if res.status is ResolutionStatus.EXECUTABLE:
                bound_path = res.bound_action["path"]
                executed_method = res.bound_action.get("method")
                status, payload = act(client, bound_path, executed_method, identifier)
            if spec_f["method"] == "DELETE":
                sub.store.seed(collection, identifier)
            rows.append({
                "arm": f"INHERITANCE-{mode.upper()}", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status,
                "http_ok": status == 200,
                "resolution": res.status.value, "bound_path": bound_path,
                "executed_method": executed_method, "required_method": spec_f["method"],
                "mechanism_id": res.mechanism_id,
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        executed_method, spec_f["method"]),
            })
    return rows


def run_pc_same_resource(client, kernel, sub):
    """PC-SAME-RESOURCE: induced mechanisms on held-out resource A identifiers (cheap)."""
    rows = []
    for spec_f in FAMILIES:
        collection = "items"
        for identifier in PC_A_IDS[spec_f["family"]]:
            sub.store.seed(collection, identifier)
            before = client.mark()
            ctx = {"collection": collection}
            params = {"id": identifier, "collection": collection}
            res = kernel.resolve(spec_f["intent_a"], ctx, params)
            status, payload = 0, {}
            bound_path = executed_method = None
            if res.status is ResolutionStatus.EXECUTABLE:
                bound_path = res.bound_action["path"]
                executed_method = res.bound_action.get("method")
                status, payload = act(client, bound_path, executed_method, identifier)
            if spec_f["method"] == "DELETE":
                sub.store.seed(collection, identifier)
            rows.append({
                "arm": "PC-SAME-RESOURCE", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status,
                "http_ok": status == 200,
                "resolution": res.status.value, "bound_path": bound_path,
                "executed_method": executed_method, "required_method": spec_f["method"],
                "mechanism_id": res.mechanism_id,
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        executed_method, spec_f["method"]),
            })
    return rows


def run_nc_shuffled(client, kernel, sub, mode: str, nc_mechs):
    """NC-SHUFFLED-INTENT: shuffled-label mechanisms on resource B."""
    rows = []
    for spec_f in FAMILIES:
        collection = "products"
        for identifier in B_FAMILY_IDS[spec_f["family"]]:
            sub.store.seed(collection, identifier)
            before = client.mark()
            ctx = {"collection": collection}
            params = {"id": identifier, "collection": collection}
            res = kernel.resolve(spec_f["intent_b"], ctx, params)
            status, payload = 0, {}
            executed_method = None
            if res.status is ResolutionStatus.EXECUTABLE:
                executed_method = res.bound_action.get("method")
                status, payload = act(client, res.bound_action["path"], executed_method, identifier)
            if spec_f["method"] == "DELETE":
                sub.store.seed(collection, identifier)
            rows.append({
                "arm": f"NC-SHUFFLED-INTENT-{mode.upper()}", "family": spec_f["family"], "identifier": identifier,
                "requests": client.mark() - before, "status": status,
                "http_ok": status == 200,
                "resolution": res.status.value,
                "executed_method": executed_method, "required_method": spec_f["method"],
                "mechanism_id": res.mechanism_id,
                "success": task_success(status, payload, identifier, spec_f["ok"],
                                        executed_method, spec_f["method"]),
            })
    return rows


def run_probes(kernel, arm: str):
    """NC-FALSE-ACCEPT: 60 negative probes (20 per kind)."""
    rng = random.Random(SEED)
    rows = []
    ids = [f"SKU-{c}" for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] + [f"PROD-{i}" for i in range(100, 224)]
    for i in range(NEGATIVE_PROBES_PER_ARM):
        kind = ["out_of_support_binding", "invalid_intent", "empty_string_binding"][i % 3]
        intent = "read-widget" if kind == "invalid_intent" else FAMILIES[i % 3]["intent_b"]
        if kind == "empty_string_binding":
            params = {"id": "", "collection": "products"}
        elif kind == "out_of_support_binding":
            params = {"id": ids[rng.randrange(len(ids))] + "!!unsupported!!", "collection": "products"}
        else:
            params = {"id": ids[rng.randrange(len(ids))], "collection": "products"}
        res = kernel.resolve(intent, {"collection": "products"}, params)
        rows.append({
            "arm": arm, "probe_index": i, "kind": kind, "intent": intent,
            "executed": res.status is ResolutionStatus.EXECUTABLE, "status": res.status.value,
        })
    return rows


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)

    # 1. Surface contract probe (both regimes)
    probe_costly = probe_surface_contract("costly")
    probe_cheap = probe_surface_contract("cheap")
    (RAW / "substrate_probe.json").write_text(json.dumps({
        "costly": probe_costly, "cheap": probe_cheap,
    }, indent=2, sort_keys=True) + "\n")

    # 2. Induction in cheap regime (shared)
    cheap_sub = substrate.Substrate("cheap")
    fresh(cheap_sub)
    cheap_client = Client(cheap_sub.base_url, "cheap")
    training, induction_cost = collect_observations(cheap_client, cheap_sub)
    (RAW / "observations.jsonl").write_text("\n".join(json.dumps({
        "intent": o.intent, "state": o.state, "action": o.action,
        "next_state": o.next_state, "success": o.success}, sort_keys=True) for o in training) + "\n")

    # 3. Induce mechanisms (shared across regimes)
    td = tempfile.TemporaryDirectory()
    reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
    kernel = SpiderKernel(reg, min_confidence=0.8, intent_namespace_map=INTENT_NS)
    inherit_mechs = kernel.distill_parameterized(training, mechanism_prefix="inherit")

    # Null control: shuffled intent labels
    rng = random.Random(SEED)
    labels = [o.intent for o in training]
    rng.shuffle(labels)
    shuffled = [Observation(intent=l, state=o.state, action=o.action,
                            next_state=o.next_state, success=o.success)
                for o, l in zip(training, labels)]
    nc_mechs = kernel.distill_parameterized(shuffled, mechanism_prefix="nc")

    (RAW / "mechanisms.json").write_text(json.dumps({
        "inheritance": [m.as_dict() for m in inherit_mechs],
        "nc_shuffled_intent": [m.as_dict() for m in nc_mechs],
        "n_training_observations": len(training),
        "n_distinct_training_ids": len(TRAIN_A_IDS),
        "induction_cost_requests": induction_cost,
    }, indent=2, sort_keys=True) + "\n")

    rows: list[dict] = []
    costly_client = None

    # 4. Run arms in both regimes
    for mode in ("costly", "cheap"):
        sub = substrate.Substrate(mode)
        fresh(sub)
        client = Client(sub.base_url, mode)
        if mode == "costly":
            costly_client = client

        fresh(sub)
        rows += run_bcold(client, sub, mode)

        fresh(sub)
        rows += run_scratchpad(client, sub, mode)

        fresh(sub)
        rows += run_no_memory(client, sub, mode)

        fresh(sub)
        rows += run_instructions(client, sub, mode)

        fresh(sub)
        rows += run_retrieval_k5(client, sub, mode, training)

        fresh(sub)
        reg.replace(inherit_mechs)
        rows += run_inheritance_arm(client, kernel, sub, mode)

        if mode == "cheap":
            fresh(sub)
            rows += run_pc_same_resource(client, kernel, sub)

        fresh(sub)
        reg.replace(nc_mechs)
        rows += run_nc_shuffled(client, kernel, sub, mode, nc_mechs)

        sub.stop()

    # 5. NC-FALSE-ACCEPT probes (kernel-level, regime-independent)
    reg.replace(inherit_mechs)
    probe_rows = run_probes(kernel, "INHERITANCE")

    (RAW / "task_results.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n")
    (RAW / "probe_results.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in probe_rows) + "\n")

    # Total HTTP requests across all clients (cheap induction + both regimes)
    total_requests = cheap_client.requests + costly_client.requests
    summary = {
        "induction_cost": induction_cost,
        "n_training": len(training),
        "n_b_ids": len(B_IDS),
        "n_per_family": {f: len(B_FAMILY_IDS[f]) for f in B_FAMILY_IDS},
        "total_http_requests": total_requests,
        "reauths_costly": costly_client.reauths,
        "arms": sorted({r["arm"] for r in rows}),
        "probe_count": len(probe_rows),
    }
    (RAW / "run_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))

    cheap_sub.stop()
    td.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
