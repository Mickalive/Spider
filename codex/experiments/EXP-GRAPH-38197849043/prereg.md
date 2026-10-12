# EXP-GRAPH-38197849043 — preregistration (FROZEN)

**Status:** frozen design (design_contract_version 2). Do not edit after freeze.

| identity | value |
| --- | --- |
| experiment_id | `EXP-GRAPH-38197849043` |
| lane | `graph` |
| design_contract_version | `2` |
| target claim | `C-DELTA-REPAIR` |
| dependency claims | `C-PARAM-INHERIT`, `C-FRESHNESS`, `C-MEAS-VALID` |
| request `base_sha` | `2e6945546a700c19b7fd411ea8daa30aae66e6dd` |
| claim_registry_sha256 | `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b` |
| origin_github_run_id | `38197849043` |
| parent_handoff | `EXP-GRAPH-38188798583` (`sha256 f3113d27a041d6edb3f5e79539afe0fc0efb9be7a06a2f70eab27fb51b89e01e`), disposition **SUPERSEDE** |
| CANONICAL-RUNNER-SHA256 | `0322d92cfbc1314437a92eb0cdfeac43a8ecd3c5cdd520bae0a443c8d669eed1` |

The Director mandate (`request.json.director_mandate`) is binding. It REOPENs `C-DELTA-REPAIR`
(the program's only starved claim) and explicitly **forbids** the stale distributed
nginx/gunicorn/WAL substrate that previously produced `MEASUREMENT_INVALID`
(`EXP-GRAPH-36106653880`), mandating instead a credential-free, locally served,
perturbable HTTP application with the now-shipped parameterized carrier
(`src/spider/kernel.py`: `distill_parameterized -> resolve -> execute -> verify`,
reference `EXP-PRODUCT-38189918141`) plus a deterministic freshness guard. The parent
handoff `next_question` concerns a different thread (`C-SEMANTIC-RESOLVE`); it is inherited
continuity only and is SUPERSEDED here per the mandate.

## 1. Question

On a credential-free, locally served, perturbable HTTP application — using the **shipped**
parameterized carrier and a **deterministic structural + postcondition freshness guard** —
after a controlled LOCAL perturbation (endpoint parameter mutation, selector/structure
change, or permission-boundary change), does a local repair restore correct end-to-end task
success at a repair cost strictly below cold re-derivation, with ZERO behavioural
contamination of unaffected resource segments (localized write set; contamination rate
<= a preregistered bound), against strong baselines (cold re-derive, literal replay,
no-repair)? Report the repair-vs-cold cost ratio by perturbation class and the contamination
rate, so that `C-DELTA-REPAIR` is either bounded upward or falsified.

## 2. Hypothesis

`H1 (functional):` after a single LOCAL perturbation of one resource segment, a
signal-driven local repair of the SHIPPED parameterized mechanism restores correct
end-to-end task success on the perturbed resource at rate >= 0.80 per perturbation class
(Wilson 95% lower bound >= 0.60), with the deterministic guard firing on >= 0.80 of
perturbed trials.

`H2 (locality):` the repair's write set is localized to the single perturbed mechanism
(`M-WRITE-SET-MAX <= 1`) and behavioural contamination of the four unaffected resource
segments is <= 0.10, while a deliberately over-broad all-mechanism rewrite (NC-OVERBROAD-REPAIR)
is detected as contaminated.

`H3 (cost):` the repair cost ratio versus cold re-derivation is strictly below 1.00 on the
equal-weight registered operation counter, and <= 0.90 on live network fetches
(repair beats cold on both the total and the network-work dimensions).

## 3. Falsifier

The experiment is a valid negative for the mandate's strict cost claim if, on any
perturbation class, the guarded local repair fails to be simultaneously
(i) functionally live (repair success >= 0.80, Wilson lower >= 0.60), (ii) local
(write set <= 1 mechanism, contamination rate <= 0.10), and (iii) strictly cheaper than
cold re-derivation on the registered product counter (ratio < 1.00) AND on live fetches
(ratio <= 0.90). A functionally successful, contamination-free repair that is only
network-cheaper but not cheaper on the equal-weight product counter is a `MIXED`
(trade-off) result, not a strict support. A repair that contaminates unaffected segments,
or whose guard fails to fire, or whose cold/literal/no-repair baselines are not live,
is `MEASUREMENT_INVALID` or `FALSIFIES` and must not be reported as a positive.

## 4. Substrate, treatment identity, and perturbation classes

**Substrate (credential-free, local, stdlib only).** An in-process `ThreadingHTTPServer`
serves a small JSON API `/api/<resource>/<id>` over 127.0.0.1 on an ephemeral port. Records
return `id` as a **string** plus a stable anchor field `kind` and per-id data fields. Five
resources exist: `users`, `posts`, `comments`, `albums`, `photos`. The task is a
parameterized read of a resource across ids `TASK_IDS = [1,2,3,4,5]`; the mechanism is
learned from `LEARN_IDS = [1,2,3]`. Exactly ONE target resource is perturbed per trial
(targets rotate over `users`/`posts`/`comments`); the other four resources are the
contamination probes. There is **no** LLM, credentials, external network, browser, nginx,
gunicorn, Redis or WAL.

**Treatment `T-LOCAL-REPAIR`.** Uses the SHIPPED carrier unchanged:
`distill_parameterized` to learn a mechanism per resource, then `resolve` to bind a
parameterized action, and `verify` against postconditions. On a perturbed resource the
guard (section 5) fires and a deterministic, class-agnostic `local_repair` rewrites ONLY the
perturbed mechanism (same `mechanism_id`, via `registry.upsert`), then re-executes.

**Perturbation classes (one per trial, applied in-process to the single target).**

| class | perturbation | required repair signal |
| --- | --- | --- |
| `P1-ENDPOINT` | old path segment becomes `301` with `Location: /api/<new_segment>/<id>`; redirects are **not** auto-followed | rebind the endpoint segment from `Location` |
| `P2-STRUCTURE` | anchor `kind` renamed to `entity_type` and `schema_version:"2"` added; HTTP 200 | re-adopt the live postcondition schema, relocating the renamed anchor |
| `P3-PERMISSION` | target requires header `X-Consent: granted`, else `403` + `X-Required-Consent: granted` | attach the server-advertised required header |

The repair routine branches purely on the observed response signature (status/headers/body);
it is never told the perturbation class.

## 5. Deterministic freshness guard and local repair

The guard declares the live probe STALE iff any of:
1. the probe is non-200 or errored; **or**
2. the inherited mechanism's own postconditions no longer `verify` on the live body; **or**
3. the Jaccard similarity of the **required-field-filtered** structural token set
   (fields present in the mechanism's postconditions, mapped to string paths + JSON types)
   falls below `JACCARD_THRESHOLD = 0.85`.

Filtering to the mechanism's own postcondition paths makes the guard insensitive to
non-semantic churn: the `NC-NOISE` control adds a per-request `observed_at` nonce, which
must NOT trigger the guard. The guard has no fitted parameters.

Local repair procedures: `301/302/303/307/308` -> probe the `Location` and rebuild the URL
template at the parent path; `403` -> adopt any `X-Required-*` response header as a request
header and probe; `200` -> adopt the live body schema, keeping templated (slot) fields and
relocating literal anchor values to whichever live key now carries the same value. The
repair charges exactly one `repair_attempts` (via the carrier's `rebind`) plus its probe
fetch, and never edits another resource's mechanism.

## 6. Baselines and controls

| id | type | description |
| --- | --- | --- |
| `B-COLD` | cost baseline (primary) | cold re-derivation: discovery probe + `LEARN_IDS` (L=3) fresh observations, `distill_parameterized`, then execute the same 5 tasks. This is the mandate's strong cold/retrieval comparator. |
| `B-COLD-MIN` | cost sensitivity | identical but L=2 (the carrier's minimum viable re-derivation). |
| `B-COLD-DEEP` | cost sensitivity | identical but L=4. |
| `B-LITERAL-REPLAY` | mechanism control | replay the inherited (unrepaired) mechanism on the perturbed resource; must fail. |
| `B-NO-REPAIR` | abstention control | guard detects staleness but the system abstains; must fail (non-executing baseline; explicitly NOT the cost comparator). |
| `PC-BASE-LIVENESS` | positive control | pre-perturbation, every learned mechanism resolves EXECUTABLE and its first read verifies. |
| `NC-NO-PERTURBATION` | negative control | with no perturbation the guard must NOT fire (stale=false). |
| `NC-NOISE` | negative control | non-semantic `observed_at` churn must NOT fire the guard. |
| `NC-OVERBROAD-REPAIR` | negative control | applying the target's repaired postconditions to ALL mechanisms; the contamination metric must detect the resulting breakage where a semantic change exists (expected > 0 for `P2-STRUCTURE`). |

## 7. Decision rule

Per class, on the frozen classifier:

```
functional_ok := repair_success >= 0.80
             AND repair_success_wilson_lower >= 0.60
             AND contamination_rate <= 0.10
             AND write_set_max <= 1
             AND guard_fire_rate >= 0.80
cost_verdict := FUNCTIONAL-FAIL            if not functional_ok
              | STRICT-WIN                 if product_ratio < 1.00 AND fetch_ratio <= 0.90
              | BOUNDED-WIN                if product_ratio <= 1.00 AND fetch_ratio <= 0.90
              | MIXED-TRADEOFF             if product_ratio <= 1.15 AND fetch_ratio <= 0.90
              | COST-FAIL                  otherwise
```

where `product_ratio = mean(repair product)/mean(cold product)` over the registered
`TrajectoryCounters` components `{http_requests, retrieval_calls, verification_calls,
repair_attempts}` summed equally, and `fetch_ratio = mean(repair http)/mean(cold http)`.

Aggregate decision (classes `P1-ENDPOINT`, `P2-STRUCTURE`, `P3-PERMISSION`):

- any class invalid (cold not live / literal replay not inert / no-repair not inert /
  negative control not fresh / `n < 12` / invalid trial) -> `MEASUREMENT_INVALID`,
  `outcome=INCONCLUSIVE`;
- all classes `STRICT-WIN` -> `SUPPORTS`;
- all classes in `{STRICT-WIN, BOUNDED-WIN}` -> `SUPPORTS-BOUNDED`;
- all classes in `{STRICT-WIN, BOUNDED-WIN, MIXED-TRADEOFF}` -> `MIXED-TRADEOFF`;
- some class in a positive/neutral tier -> `MIXED`;
- otherwise -> `FALSIFIES`.

The `--mechanics-only` flag is a non-scored design canary and is NOT the confirmatory run.

Note on the cost denominator: the mandate's strong baseline is cold re-derivation on the
same perturbed task, so `B-NO-REPAIR` (a non-executing baseline) is reported but is never
used as the cost denominator. The mandate requires that cost be compared against cold
re-derivation, which is exactly `B-COLD`.

## 8. Design satisfiability probes (non-scored, DESIGN-time)

**8.1 Carrier liveness canary (`--mechanics-only`, SEED = 38197849043 mod 2^32).** Fixed
1 trial per class, run in DESIGN. It is not scored; it confirms the shipped carrier becomes
EXECUTABLE and the branches are reachable:

```
P1-ENDPOINT  repair=true  cold=true  literal=false  guard=true  contamination=0/4  base_liveness=true  repair product=20 vs cold product=19 (fetch 7 vs 9)
P2-STRUCTURE repair=true  cold=true  literal=false  guard=true  contamination=0/4  base_liveness=true  repair product=20 vs cold product=19 (fetch 6 vs 9)
P3-PERMISSION repair=true cold=true  literal=false  guard=true  contamination=0/4  base_liveness=true  repair product=20 vs cold product=19 (fetch 7 vs 9)
NC-NO-PERTURBATION stale=false ; NC-NOISE stale=false
```

This shows: the shipped carrier genuinely distills/resolves/verifies the parameterized task;
each perturbation bites (literal replay fails); the guard fires; the repair restores success;
contamination is zero; both negative controls stay fresh. The canary is deterministic
(two independent runs produced byte-identical output; the runner writes all registry state
under a fresh per-process temp directory to prevent cross-run contamination).

**Probe integrity / non-fitted thresholds.** The `--mechanics-only` canary is a DESIGN
satisfiability probe whose purpose is to demonstrate carrier liveness, perturbation bite,
guard firing, control sensitivity, and decision-rule reachability; it is explicitly
non-scored and the scored run re-measures everything independently at n=12. As a byproduct
the canary exposes single-trial cost magnitudes (shown above, 20 vs 19). No decision
threshold was derived from those magnitudes. `PRODUCT_COST_BAR = 1.00` and
`FETCH_COST_BAR = 0.90` are the mandate's strict semantics (strictly below cold
re-derivation; network-cheaper); `PRODUCT_COST_MAX = 1.15` is a conventional 15% materiality
band chosen a priori to separate a cost-neutral result from a material regression. All
thresholds are fixed here and MUST NOT be re-tuned after the scored run. This disclosure is
made so AUDIT can judge pre-registration integrity rather than infer it.

**8.2 Decision-branch reachability probe (synthetic, non-substrate).** The frozen
`aggregate_and_decide` code path was driven with synthetic trial rows (never substrate
outcomes) to prove every substantive branch is reachable: `SUPPORTS`, `SUPPORTS-BOUNDED`,
`MIXED`, `MIXED-TRADEOFF`, `FALSIFIES`, and `MEASUREMENT_INVALID` were each produced. The
rule is therefore satisfiable and not a tautology.

**8.3 Cost-denominator sensitivity.** Because the cold re-derivation budget is the principal
free parameter of the cost comparison, it is fixed a priori at L=3 (the same number of
observations used to learn the inherited mechanism), with L=2 and L=4 reported as
sensitivities (`M-COST-PRODUCT-RATIO-MIN`, `-DEEP`). A verdict that flips across these
budgets is reported as a cost-identifiability caveat rather than a robust win.

## 9. Measurement validity gates

- `V1-FREEZE_BINDING`: extracted runner bytes hash to `CANONICAL-RUNNER-SHA256`; request/
  prereg/artifact hashes match `freeze.json`.
- `V2-SUBSTRATE_ISOLATION`: stdlib only; no LLM/network/credential/browser; fresh per-run
  registry directory (no cross-run mechanism leakage).
- `V3-DETERMINISM`: fixed seeds; two independent canary runs byte-identical.
- `V4-PERTURBATION_BITES`: `B-LITERAL-REPLAY` success <= 0.10 on every class.
- `V5-COLD_BASELINE_LIVE`: `B-COLD` success >= 0.90 on every class (else `MEASUREMENT_INVALID`).
- `V6-NO_REPAIR_INERT`: `B-NO-REPAIR` success <= 0.10 (else `MEASUREMENT_INVALID`).
- `V7-GUARD_LIVENESS`: guard fires >= 0.80 on perturbed trials AND does not fire on
  `NC-NO-PERTURBATION` / `NC-NOISE` (else `MEASUREMENT_INVALID`).
- `V8-NO_TARGET_LEAKAGE`: the repair writes exactly one mechanism (`M-WRITE-SET-MAX <= 1`);
  contamination measured only on genuinely unaffected resources.
- `V9-INTEGER_COUNTERS`: all cost counters are integer counts from the shipped
  `TrajectoryCounters` surface; no estimated or model-token quantities.
- `V10-THRESHOLD_NOT_FITTED`: `JACCARD_THRESHOLD = 0.85` and all decision bars are
  preregistered and were not tuned against any scored run.
- `V11-N_CONTROLLED`: `TRIALS_PER_CLASS = 12` with rotating targets.
- `V12-POSITIVE_CONTROL`: `PC-BASE-LIVENESS` true before perturbation.

## 10. Freeze artifacts and canonical hashes

Mutable local interpretation dependencies (hashed into `freeze.json.artifact_hashes`):

- `src/spider/kernel.py` (the shipped carrier; treatment identity)
- `src/spider/models.py` (Mechanism/Observation/Resolution semantics)
- `src/spider/registry.py` (registry read/upsert/invalidate semantics; locality)

The executable decision path is embedded verbatim below and bound by
`CANONICAL-RUNNER-SHA256 = 0322d92cfbc1314437a92eb0cdfeac43a8ecd3c5cdd520bae0a443c8d669eed1` and by `freeze.json.hashes.prereg.md`. No external
task bank, dataset or fixture is read: the substrate is constructed inside the runner.

## 11. Environment and EXECUTE command

Python 3.12, stdlib only. After freeze, EXECUTE extracts the block delimited by the
FROZEN-RUNNER begin/end HTML comment markers below (captured group + one `\n`) to
`raw_evidence/runner_delta_repair.py` and runs:

```
python raw_evidence/runner_delta_repair.py | tee raw_evidence/runner_result_raw.json
```

The runner prints a single JSON object on stdout. `--mechanics-only` is a non-scored
canary only.

## 12. FROZEN-RUNNER

<!-- BEGIN FROZEN-RUNNER -->
#!/usr/bin/env python3
# FROZEN RUNNER for EXP-GRAPH-38197849043 (graph, design_contract_version 2).
# C-DELTA-REPAIR: on a credential-free, locally served, perturbable stdlib HTTP
# application, using the SHIPPED parameterized carrier
# (src/spider/kernel.py: distill_parameterized -> resolve -> execute -> verify)
# and a deterministic structural+postcondition freshness guard, does a LOCAL
# repair restore correct end-to-end task success at a repair cost strictly below
# cold re-derivation, with ZERO behavioural contamination of unaffected resource
# segments, against cold-re-derive / literal-replay / no-repair baselines?
# Reports the repair-vs-cold cost ratio and contamination rate by perturbation
# class (P1-ENDPOINT, P2-STRUCTURE, P3-PERMISSION).
#
# Stdlib only. No credentials, no external network, no LLM, no browser.
# Usage: python runner_delta_repair.py [--mechanics-only]
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import random
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38197849043"
SEED = 38197849043 % (2 ** 32)

# Every registry file lives in a fresh per-process directory so no mechanism
# state can leak across runs (MechanismRegistry.all() loads existing JSONL and
# upsert() merges by mechanism_id; a reused path would resurrect stale
# mechanisms whose embedded endpoint port no longer exists).
_RUN_DIR = Path(tempfile.mkdtemp(prefix=f"exp381-{os.getpid()}-"))

sys.path.insert(0, str(ROOT / "src"))
from spider.kernel import SpiderKernel, TrajectoryCounters  # noqa: E402
from spider.models import Mechanism, Observation  # noqa: E402
from spider.registry import MechanismRegistry  # noqa: E402

# ---------------------------------------------------------------- constants --
RESOURCES = ["users", "posts", "comments", "albums", "photos"]
TARGETS = ["users", "posts", "comments"]
TASK_IDS = [1, 2, 3, 4, 5]
LEARN_IDS = [1, 2, 3]
LEARN_IDS_MIN = [1, 2]
LEARN_IDS_DEEP = [1, 2, 3, 4]
CLASSES = ["P1-ENDPOINT", "P2-STRUCTURE", "P3-PERMISSION"]
NEW_SEGMENTS = ["people", "articles", "notes", "collections", "media"]
ANCHOR = "kind"
ANCHOR_RENAMED = "entity_type"
CONSENT_HEADER = "X-Consent"
CONSENT_VALUE = "granted"
JACCARD_THRESHOLD = 0.85
MIN_CONFIDENCE = 0.8

REPAIR_SUCCESS_BAR = 0.80
WILSON_SUCCESS_LOWER_BAR = 0.60
CONTAMINATION_BAR = 0.10
GUARD_FIRE_BAR = 0.80
PRODUCT_COST_BAR = 1.00      # strictly below cold on the registered counter
PRODUCT_COST_MAX = 1.15      # materiality bound on a total-cost regression
FETCH_COST_BAR = 0.90        # strictly below cold on live fetches
COLD_SUCCESS_BAR = 0.90
LITERAL_SUCCESS_BAR = 0.10
NOISE_FALSE_TRIGGER_BAR = 0.10
WILSON_Z = 1.96
TRIALS_PER_CLASS = 12

# ---------------------------------------------------------------- substrate --
def build_record(resource: str, rid: int) -> dict:
    s = str(rid)
    if resource == "users":
        return {"id": s, "kind": "user", "name": f"User {rid}", "email": f"user{rid}@example.com"}
    if resource == "posts":
        return {"id": s, "kind": "post", "title": f"Post {rid}", "body": f"Body {rid}"}
    if resource == "comments":
        return {"id": s, "kind": "comment", "author": f"Author {rid}", "text": f"Text {rid}"}
    if resource == "albums":
        return {"id": s, "kind": "album", "title": f"Album {rid}", "owner": f"Owner {rid}"}
    if resource == "photos":
        return {"id": s, "kind": "photo", "caption": f"Caption {rid}", "url": f"img://{rid}"}
    raise KeyError(resource)


class AppState:
    def __init__(self):
        self.perturb = None
        self.noise = False
        self.nonce = 0

    def reset(self):
        self.perturb = None
        self.noise = False
        self.nonce = 0

    def set_perturb(self, cls: str, resource: str, seed: int):
        rng = random.Random(seed)
        cfg = {"class": cls, "resource": resource}
        if cls == "P1-ENDPOINT":
            cfg["new_segment"] = rng.choice(NEW_SEGMENTS)
        self.perturb = cfg


class Handler(BaseHTTPRequestHandler):
    state: AppState = None

    def log_message(self, *args):
        pass

    def _json(self, code: int, body: dict):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_GET(self):
        parts = [p for p in self.path.split("/") if p]
        if len(parts) != 3 or parts[0] != "api":
            self._json(404, {"error": "not found"})
            return
        segment, rid_raw = parts[1], parts[2]
        try:
            rid = int(rid_raw)
        except ValueError:
            self._json(400, {"error": "bad id"})
            return
        cfg = self.state.perturb
        logical = segment
        if cfg and cfg["class"] == "P1-ENDPOINT" and segment == cfg["resource"]:
            self.send_response(301)
            self.send_header("Location", f"/api/{cfg['new_segment']}/{rid}")
            self.end_headers()
            return
        if cfg and cfg["class"] == "P1-ENDPOINT" and segment == cfg["new_segment"]:
            logical = cfg["resource"]
        if logical not in RESOURCES:
            self._json(404, {"error": "unknown resource"})
            return
        if cfg and cfg["class"] == "P3-PERMISSION" and logical == cfg["resource"]:
            if self.headers.get(CONSENT_HEADER) != CONSENT_VALUE:
                self.send_response(403)
                self.send_header("X-Required-Consent", CONSENT_VALUE)
                self.end_headers()
                return
        body = build_record(logical, rid)
        if cfg and cfg["class"] == "P2-STRUCTURE" and logical == cfg["resource"]:
            renamed = {ANCHOR_RENAMED if k == ANCHOR else k: v for k, v in body.items()}
            renamed["schema_version"] = "2"
            body = renamed
        if self.state.noise:
            self.state.nonce += 1
            body = dict(body)
            body["observed_at"] = f"t{self.state.nonce}"
        self._json(200, body)


class LocalApp:
    def __init__(self):
        self.state = AppState()
        Handler.state = self.state
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    @property
    def origin(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


def wait_ready(app: "LocalApp", attempts: int = 100) -> bool:
    """Block until the local server accepts and serves a request (no race)."""
    for _ in range(attempts):
        r = fetch(app.origin + "/api/albums/1")
        if r.status is not None:
            return True
        time.sleep(0.05)
    return False


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


_OPENER = build_opener(NoRedirect)


class Counters:
    def __init__(self):
        self.http = 0
        self.retrieval = 0
        self.verification = 0
        self.repair = 0

    def product(self) -> int:
        return self.http + self.retrieval + self.verification + self.repair

    def as_dict(self):
        return {"http": self.http, "retrieval": self.retrieval,
                "verification": self.verification, "repair": self.repair,
                "product": self.product()}


class HTTPResult:
    def __init__(self, status, headers, body, error=None):
        self.status = status
        self.headers = headers or {}
        self.body = body
        self.error = error


def fetch(url: str, headers: dict | None = None, counters: Counters | None = None,
          origin: str | None = None) -> HTTPResult:
    if counters is not None:
        counters.http += 1
    req = Request(url, headers=headers or {})
    try:
        with _OPENER.open(req, timeout=5) as resp:
            raw = resp.read().decode()
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                body = None
            return HTTPResult(resp.status, dict(resp.headers), body)
    except HTTPError as exc:
        raw = exc.read().decode() if exc.fp else ""
        try:
            body = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            body = None
        hdrs = dict(exc.headers)
        if origin is not None:
            hdrs["_origin"] = origin
        return HTTPResult(exc.code, hdrs, body, error="HTTPError")
    except URLError as exc:
        return HTTPResult(None, {}, None, error=str(exc))


# ----------------------------------------------------- deterministic guard --
TYPE_MAP = {"str": "string", "int": "integer", "float": "number", "bool": "boolean",
            "NoneType": "null", "list": "array", "dict": "object"}


def flatten(obj, prefix=""):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, list):
        out[prefix] = obj
    else:
        out[prefix] = obj
    return out


def field_type_tokens(obj, prefix=""):
    pairs = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, dict):
                pairs.update(field_type_tokens(v, path))
            elif isinstance(v, list):
                pairs.add((path, "array"))
            else:
                pairs.add((path, TYPE_MAP.get(type(v).__name__, type(v).__name__)))
    elif isinstance(obj, list):
        pairs.add((prefix, "array"))
    else:
        pairs.add((prefix, TYPE_MAP.get(type(obj).__name__, type(obj).__name__)))
    return pairs


def required_token_set(body, required_paths):
    return {(p, t) for (p, t) in field_type_tokens(body) if p in required_paths}


def jaccard(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


class Arm:
    """A fresh kernel + registry + honest counters for one arm on one trial."""

    _seq = 0

    def __init__(self, mech_dicts, reg_dir: Path, tag: str):
        Arm._seq += 1
        self.path = _RUN_DIR / f"reg-{tag}-{Arm._seq:06d}.jsonl"
        self.registry = MechanismRegistry(self.path)
        for m in mech_dicts.values():
            self.registry.upsert(Mechanism(**m))
        self.kernel = SpiderKernel(self.registry, min_confidence=MIN_CONFIDENCE,
                                   counters=TrajectoryCounters())
        self.counters = Counters()

    def sync(self):
        c = self.kernel.counters
        self.counters.retrieval = c.retrieval_calls
        self.counters.verification = c.verification_calls
        self.counters.repair = c.repair_attempts

    def target_mech(self, resource):
        for m in self.registry.all():
            if m.intent == f"read_{resource}":
                return m
        return None

    def resolve(self, intent, context, params):
        r = self.kernel.resolve(intent, context, params)
        self.sync()
        return r

    def verify(self, mid, body, params):
        v = self.kernel.verify(mid, body, params)
        self.sync()
        return v

    def rebind(self, intent, context, params):
        r = self.kernel.rebind(intent, context, params)
        self.sync()
        return r


def make_mech_dicts(origin, counters):
    """Learn all resources from LEARN_IDS with the shipped carrier."""
    k = SpiderKernel(MechanismRegistry(_RUN_DIR / "unused.jsonl"),
                     min_confidence=MIN_CONFIDENCE, counters=TrajectoryCounters())
    mechs, cached = {}, {}
    for r in RESOURCES:
        obs = []
        for rid in LEARN_IDS:
            res = fetch(f"{origin}/api/{r}/{rid}", {}, counters)
            obs.append(Observation(intent=f"read_{r}", state={"resource_type": r},
                                   action={"method": "GET", "url": f"{origin}/api/{r}/{rid}",
                                           "headers": {}},
                                   next_state=res.body or {}, success=(res.status == 200)))
        m = k.distill_parameterized(obs)
        if m is None:
            return None, None
        mechs[r] = m.as_dict()
        cached[r] = field_type_tokens(obs[0].next_state)
    return mechs, cached


def execute_batch(arm: Arm, intent, context, slot, ids, extra_header=None):
    ok = True
    values = []
    for t in ids:
        pid = str(t)
        r = arm.resolve(intent, context, {slot: pid})
        if r.status.name != "EXECUTABLE" or r.bound_action is None:
            ok = False
            values.append(None)
            continue
        headers = dict(r.bound_action.get("headers", {}))
        if extra_header:
            headers.update(extra_header)
        res = fetch(r.bound_action["url"], headers, arm.counters)
        if res.status != 200 or res.body is None:
            ok = False
            values.append(None)
            continue
        if not arm.verify(r.mechanism_id, res.body, {slot: pid}):
            ok = False
        values.append(res.body.get("id"))
    return ok, values


# ------------------------------------------------------------------ repair --
def guard(cached_tokens, required_paths, failed, arm: Arm, mech, params):
    """Deterministic structural + postcondition freshness guard.

    Fires (stale) iff the live probe is non-200/errored, OR the mechanism's own
    postconditions no longer verify, OR the *required-field-filtered* structural
    token set has drifted below the preregistered Jaccard threshold. Fields
    outside the mechanism's postcondition paths (e.g. a non-semantic
    ``observed_at`` nonce) cannot trigger it.
    """
    if failed.error is not None or failed.status != 200 or failed.body is None:
        return True, {"reason": "non-200", "status": failed.status, "jaccard": None}
    live = required_token_set(failed.body, required_paths)
    cached = {(p, t) for (p, t) in cached_tokens if p in required_paths}
    j = jaccard(cached, live)
    ok = arm.verify(mech.mechanism_id, failed.body, params)
    if (not ok) or j < JACCARD_THRESHOLD:
        return True, {"reason": "postcondition" if not ok else "structure",
                      "status": failed.status, "jaccard": j}
    return False, {"reason": "fresh", "status": failed.status, "jaccard": j}


def local_repair(arm: Arm, mech, resource, slot, probe_id, failed, origin):
    """Class-agnostic local repair driven only by live response signals.

    Branches purely on the observed failure signature:
      * redirect       -> rebind the endpoint segment from ``Location``
      * 403 permission -> attach the server-advertised required header
      * 200 drift      -> re-adopt the live postcondition schema, relocating
                          renamed anchor paths (old literal value -> new key)

    The repair keeps the same ``mechanism_id`` (a localized rewrite of one
    mechanism), never touches other resources' mechanisms, and charges exactly
    one ``repair_attempts`` plus the probe fetch.
    """
    import re as _re

    template_re = _re.compile(r"^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$")
    probe_body = None
    probe_header = {}
    new_template = mech.action_template["url"]
    if failed.status in (301, 302, 303, 307, 308) and failed.headers.get("Location"):
        loc = failed.headers["Location"]
        hop_origin = failed.headers.get("_origin", origin)
        probe = fetch(hop_origin + loc, {}, arm.counters)
        if probe.status != 200 or probe.body is None:
            return None
        probe_body = probe.body
        new_template = hop_origin + "/".join(loc.split("/")[:-1]) + "/${" + slot + "}"
    elif failed.status == 403:
        req_header = req_value = None
        for k, v in failed.headers.items():
            if k.lower().startswith("x-required-"):
                req_header = "X-" + k[len("x-required-"):]
                req_value = v
        if req_header is None:
            return None
        probe_header = {req_header: req_value}
        probe = fetch(new_template.replace("${" + slot + "}", str(probe_id)),
                      probe_header, arm.counters)
        if probe.status != 200 or probe.body is None:
            return None
        probe_body = probe.body
    elif failed.status == 200 and failed.body is not None:
        probe_body = failed.body
    else:
        return None

    # Re-adopt the live schema while preserving the original postcondition
    # semantics: templated (slot) fields keep their path; literal anchor values
    # are relocated to whichever live key now carries the same value.
    new_post: dict = {}
    for k, v in mech.postconditions.items():
        if isinstance(v, str) and template_re.match(v):
            new_post[k] = v
        elif probe_body.get(k) == v:
            new_post[k] = v
        else:
            cands = [nk for nk, nv in probe_body.items()
                     if nv == v and nk not in new_post]
            new_post[cands[0] if cands else k] = v

    patched = copy.deepcopy(mech)
    patched.action_template["url"] = new_template
    if probe_header:
        patched.action_template["headers"] = dict(probe_header)
    patched.postconditions = new_post
    arm.rebind(mech.intent, {"resource_type": resource}, {slot: str(probe_id)})
    return patched


def run_repair(app: LocalApp, origin, mechs, cached, resource, counters_noise=None):
    arm = Arm(mechs, Path("/tmp"), "repair")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    intent = mech.intent
    context = {"resource_type": resource}
    required_paths = set(flatten(mech.postconditions).keys())
    # first task attempt -> guard
    r0 = arm.resolve(intent, context, {slot: str(TASK_IDS[0])})
    if r0.status.name != "EXECUTABLE" or r0.bound_action is None:
        return {"success": False, "guard_fired": False, "arm": arm, "reason": "not-executable"}
    failed = fetch(r0.bound_action["url"], r0.bound_action.get("headers", {}),
                   arm.counters, origin=origin)
    stale, ginfo = guard(cached, required_paths, failed, arm, mech, {slot: str(TASK_IDS[0])})
    if not stale:
        ok, _ = execute_batch(arm, intent, context, slot, TASK_IDS)
        return {"success": ok, "guard_fired": False, "arm": arm, "reason": "fresh"}
    patched = local_repair(arm, mech, resource, slot, TASK_IDS[0], failed, origin)
    if patched is None:
        return {"success": False, "guard_fired": True, "arm": arm, "reason": "repair-failed",
                "guard_info": ginfo}
    arm.registry.upsert(patched)
    ok, _ = execute_batch(arm, intent, context, slot, TASK_IDS)
    return {"success": ok, "guard_fired": True, "arm": arm, "reason": "repaired",
            "guard_info": ginfo}


def run_cold(app, origin, resource, ids=None, tag="cold"):
    ids = ids or LEARN_IDS
    arm = Arm({}, Path("/tmp"), tag)
    # discovery
    base = f"{origin}/api/{resource}"
    extra_header = {}
    probe = fetch(f"{base}/{ids[0]}", {}, arm.counters, origin=origin)
    if probe.status in (301, 302, 303, 307, 308) and probe.headers.get("Location"):
        loc = probe.headers["Location"]
        base = origin + "/".join(loc.split("/")[:-1])
    elif probe.status == 403:
        for k, v in probe.headers.items():
            if k.lower().startswith("x-required-"):
                extra_header["X-" + k[len("x-required-"):]] = v
    elif probe.status != 200:
        return {"success": False, "arm": arm, "reason": "discovery-failed"}
    obs = []
    for rid in ids:
        res = fetch(f"{base}/{rid}", extra_header, arm.counters)
        if res.status != 200 or res.body is None:
            return {"success": False, "arm": arm, "reason": "observation-failed"}
        obs.append(Observation(intent=f"read_{resource}", state={"resource_type": resource},
                               action={"method": "GET", "url": f"{base}/{rid}",
                                       "headers": dict(extra_header)},
                               next_state=res.body, success=True))
    mech = arm.kernel.distill_parameterized(obs)
    if mech is None:
        return {"success": False, "arm": arm, "reason": "distill-failed"}
    arm.registry.upsert(mech)
    slot = mech.parameter_slots[0]
    ok, _ = execute_batch(arm, mech.intent, {"resource_type": resource}, slot, TASK_IDS)
    return {"success": ok, "arm": arm, "reason": "cold"}


def run_literal(app, origin, mechs, resource):
    arm = Arm(mechs, Path("/tmp"), "literal")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    ok, _ = execute_batch(arm, mech.intent, {"resource_type": resource}, slot, TASK_IDS)
    return {"success": ok, "arm": arm}


def run_norepair(app, origin, mechs, cached, resource):
    arm = Arm(mechs, Path("/tmp"), "norepair")
    mech = arm.target_mech(resource)
    slot = mech.parameter_slots[0]
    required_paths = set(flatten(mech.postconditions).keys())
    r0 = arm.resolve(mech.intent, {"resource_type": resource}, {slot: str(TASK_IDS[0])})
    failed = fetch(r0.bound_action["url"], r0.bound_action.get("headers", {}),
                   arm.counters, origin=origin) if r0.bound_action else HTTPResult(None, {}, None)
    stale, _ = guard(cached, required_paths, failed, arm, mech, {slot: str(TASK_IDS[0])})
    # abstain: no execution
    return {"success": False, "guard_fired": stale, "arm": arm}


def unaffected_behavior(mechs, origin, resource, tag):
    """Resolve+fetch+verify id1 for one resource; returns (status, id, verified)."""
    arm = Arm(mechs, Path("/tmp"), tag)
    mech = arm.target_mech(resource)
    if mech is None:
        return None
    slot = mech.parameter_slots[0]
    r = arm.resolve(mech.intent, {"resource_type": resource}, {slot: "1"})
    if r.status.name != "EXECUTABLE" or r.bound_action is None:
        return ("NO-RESOLVE", None, False)
    res = fetch(r.bound_action["url"], r.bound_action.get("headers", {}), arm.counters)
    if res.status != 200 or res.body is None:
        return (res.status, None, False)
    try:
        verified = arm.verify(r.mechanism_id, res.body, {slot: "1"})
    except (KeyError, TypeError):
        verified = False
    return (200, res.body.get("id"), verified)


def overbroad_contamination(base_live, origin, resource, patched_mech_dict):
    """NC-OVERBROAD-REPAIR: apply the target's repaired postconditions to every
    mechanism and measure how many unaffected resources the bad repair breaks.
    Demonstrates the contamination metric is sensitive where a semantic change
    exists (expect 0 for P1/P3 whose schema is unchanged, >0 for P2)."""
    bad = {}
    for rid, md in base_live["mech_dicts"].items():
        md2 = copy.deepcopy(md)
        if md2["intent"] != patched_mech_dict["intent"]:
            md2["postconditions"] = copy.deepcopy(patched_mech_dict["postconditions"])
        bad[rid] = md2
    contam = 0
    for r in RESOURCES:
        if r == resource:
            continue
        post = unaffected_behavior(bad, origin, r, "overbroad")
        if post != base_live[r]:
            contam += 1
    return contam


# ------------------------------------------------------------------ trial ---
def run_trial(cls, target, seed, reg_dir):
    app = LocalApp()
    try:
        if not wait_ready(app):
            return {"valid": False, "reason": "server-not-ready"}
        base_counters = Counters()
        mechs, cached = make_mech_dicts(app.origin, base_counters)
        if mechs is None:
            return {"valid": False, "reason": "learn-failed"}
        base_live = {"mech_dicts": {m["mechanism_id"]: m for m in mechs.values()}}
        for r in RESOURCES:
            base_live[r] = unaffected_behavior(mechs, app.origin, r, "base")
        pre_unaffected = {r: base_live[r] for r in RESOURCES}
        app.state.set_perturb(cls, target, seed)
        rep = run_repair(app, app.origin, copy.deepcopy(mechs), cached[target], target)
        cold = run_cold(app, app.origin, target, LEARN_IDS, "cold")
        cold_min = run_cold(app, app.origin, target, LEARN_IDS_MIN, "coldmin")
        cold_deep = run_cold(app, app.origin, target, LEARN_IDS_DEEP, "colddeep")
        lit = run_literal(app, app.origin, copy.deepcopy(mechs), target)
        nor = run_norepair(app, app.origin, copy.deepcopy(mechs), cached[target], target)
        # contamination: unaffected resources, post-repair registry vs base behaviour
        post_dicts = {m.mechanism_id: m.as_dict() for m in rep["arm"].registry.all()}
        base_dicts = base_live["mech_dicts"]
        write_set = sorted(
            mid for mid in set(base_dicts) | set(post_dicts)
            if base_dicts.get(mid) != post_dicts.get(mid))
        contam = 0
        for r in RESOURCES:
            if r == target:
                continue
            post = unaffected_behavior(post_dicts, app.origin, r, "post")
            if post != pre_unaffected[r]:
                contam += 1
        n_unaff = len(RESOURCES) - 1
        # NC-OVERBROAD: a deliberately global (non-local) rewrite
        patched_mech = rep["arm"].target_mech(target)
        overbroad = None
        if patched_mech is not None:
            overbroad = overbroad_contamination(
                base_live, app.origin, target, patched_mech.as_dict())
        return {
            "valid": True,
            "class": cls,
            "target": target,
            "repair_success": bool(rep["success"]),
            "repair_guard_fired": bool(rep.get("guard_fired")),
            "repair_reason": rep.get("reason"),
            "cold_success": bool(cold["success"]),
            "cold_reason": cold.get("reason"),
            "cold_min_success": bool(cold_min["success"]),
            "cold_deep_success": bool(cold_deep["success"]),
            "literal_success": bool(lit["success"]),
            "norepair_success": bool(nor["success"]),
            "norepair_guard_fired": bool(nor.get("guard_fired")),
            "repair_cost": rep["arm"].counters.as_dict(),
            "cold_cost": cold["arm"].counters.as_dict(),
            "cold_min_cost": cold_min["arm"].counters.as_dict(),
            "cold_deep_cost": cold_deep["arm"].counters.as_dict(),
            "literal_cost": lit["arm"].counters.as_dict(),
            "contamination_n": contam,
            "overbroad_contamination_n": overbroad,
            "write_set_n": len(write_set),
            "unaffected_n": n_unaff,
            "base_liveness": all(v and v[0] == 200 and v[2] for v in
                                 (pre_unaffected[r] for r in RESOURCES)),
        }
    finally:
        app.stop()


def noise_trial(seed):
    """NC-NOISE: non-semantic field churn must not trigger the guard."""
    app = LocalApp()
    try:
        if not wait_ready(app):
            return {"stale": None, "info": {"error": "server-not-ready"}}
        c = Counters()
        mechs, cached = make_mech_dicts(app.origin, c)
        app.state.noise = True
        arm = Arm(mechs, Path("/tmp"), "noise")
        mech = arm.target_mech("users")
        slot = mech.parameter_slots[0]
        required_paths = set(flatten(mech.postconditions).keys())
        failed = fetch(f"{app.origin}/api/users/1", {}, arm.counters, origin=app.origin)
        stale, info = guard(cached["users"], required_paths, failed, arm, mech, {slot: "1"})
        return {"stale": stale, "info": info}
    finally:
        app.stop()


def no_perturbation_trial(seed):
    """NC-NO-PERTURBATION: guard must not fire without a perturbation."""
    app = LocalApp()
    try:
        if not wait_ready(app):
            return {"stale": None, "info": {"error": "server-not-ready"}}
        c = Counters()
        mechs, cached = make_mech_dicts(app.origin, c)
        arm = Arm(mechs, Path("/tmp"), "nopert")
        mech = arm.target_mech("users")
        slot = mech.parameter_slots[0]
        required_paths = set(flatten(mech.postconditions).keys())
        failed = fetch(f"{app.origin}/api/users/1", {}, arm.counters, origin=app.origin)
        stale, info = guard(cached["users"], required_paths, failed, arm, mech, {slot: "1"})
        return {"stale": stale, "info": info}
    finally:
        app.stop()


# ---------------------------------------------------------------- wilson ----
def wilson_lower(k, n, z=WILSON_Z):
    if n == 0:
        return 0.0
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, center - margin)


def mean(xs):
    return sum(xs) / len(xs) if xs else None


# ---------------------------------------------------------------- main ------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mechanics-only", action="store_true")
    args = ap.parse_args()
    reg_dir = Path("/tmp/opencode/exp381-reg")
    reg_dir.mkdir(parents=True, exist_ok=True)

    runner_self_sha = "UNKNOWN"
    try:
        runner_self_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        pass

    if args.mechanics_only:
        # Non-scored design canary: fixed 1 trial per class, no threshold use.
        canary = []
        for ci, cls in enumerate(CLASSES):
            r = run_trial(cls, TARGETS[ci % len(TARGETS)], SEED + 900 + ci, reg_dir)
            canary.append({k: r[k] for k in ("valid", "class", "target", "repair_success",
                                             "cold_success", "literal_success", "repair_guard_fired",
                                             "contamination_n", "unaffected_n", "base_liveness",
                                             "repair_cost", "cold_cost") if k in r})
        np_t = no_perturbation_trial(SEED + 1)
        nz_t = noise_trial(SEED + 2)
        out = {"status": "DESIGN-MECHANICS-ONLY", "experiment_id": EXP_ID, "lane": "graph",
               "runner_self_sha": runner_self_sha, "seed": SEED,
               "carrier": {
                   "kernel": str(ROOT / "src/spider/kernel.py"),
                   "kernel_sha256": hashlib.sha256((ROOT / "src/spider/kernel.py").read_bytes()).hexdigest(),
                   "models_sha256": hashlib.sha256((ROOT / "src/spider/models.py").read_bytes()).hexdigest(),
                   "registry_sha256": hashlib.sha256((ROOT / "src/spider/registry.py").read_bytes()).hexdigest()},
               "canary": canary,
               "nc_no_perturbation": np_t,
               "nc_noise": nz_t}
        print(json.dumps(out, indent=2))
        return

    trials = []
    t = 0
    for ci, cls in enumerate(CLASSES):
        for j in range(TRIALS_PER_CLASS):
            target = TARGETS[(ci + j) % len(TARGETS)]
            trials.append(run_trial(cls, target, SEED + 1000 * (ci + 1) + j, reg_dir))
            t += 1
    np_t = no_perturbation_trial(SEED + 1)
    nz_t = noise_trial(SEED + 2)

    # ---- aggregate per class ----
    per_class = {}
    for cls in CLASSES:
        rows = [r for r in trials if r.get("valid") and r["class"] == cls]
        n = len(rows)
        rep_ok = sum(1 for r in rows if r["repair_success"])
        cold_ok = sum(1 for r in rows if r["cold_success"])
        cold_min_ok = sum(1 for r in rows if r["cold_min_success"])
        lit_ok = sum(1 for r in rows if r["literal_success"])
        nor_ok = sum(1 for r in rows if r["norepair_success"])
        guard_ok = sum(1 for r in rows if r["repair_guard_fired"])
        contam = sum(r["contamination_n"] for r in rows)
        unaff = sum(r["unaffected_n"] for r in rows)
        overbroad = mean([r["overbroad_contamination_n"] for r in rows
                          if r.get("overbroad_contamination_n") is not None])
        write_ws = [r.get("write_set_n") for r in rows if r.get("write_set_n") is not None]
        rep_prod = mean([r["repair_cost"]["product"] for r in rows])
        cold_prod = mean([r["cold_cost"]["product"] for r in rows])
        cold_min_prod = mean([r["cold_min_cost"]["product"] for r in rows])
        cold_deep_prod = mean([r["cold_deep_cost"]["product"] for r in rows])
        rep_http = mean([r["repair_cost"]["http"] for r in rows])
        cold_http = mean([r["cold_cost"]["http"] for r in rows])
        per_class[cls] = {
            "n": n,
            "M-REPAIR-SUCCESS": rep_ok / n if n else None,
            "M-REPAIR-SUCCESS-WILSON-LOWER": wilson_lower(rep_ok, n),
            "M-COLD-SUCCESS": cold_ok / n if n else None,
            "M-COLD-MIN-SUCCESS": cold_min_ok / n if n else None,
            "M-COLD-DEEP-SUCCESS": sum(1 for r in rows if r["cold_deep_success"]) / n if n else None,
            "M-LITERAL-REPLAY-SUCCESS": lit_ok / n if n else None,
            "M-NO-REPAIR-SUCCESS": nor_ok / n if n else None,
            "M-GUARD-FIRE-RATE": guard_ok / n if n else None,
            "M-CONTAMINATION-RATE": contam / unaff if unaff else None,
            "M-OVERBROAD-CONTAMINATION-RATE": overbroad,
            "M-WRITE-SET-MEAN": mean(write_ws),
            "M-WRITE-SET-MAX": max(write_ws) if write_ws else None,
            "M-COST-REPAIR-PRODUCT": rep_prod,
            "M-COST-COLD-PRODUCT": cold_prod,
            "M-COST-COLD-MIN-PRODUCT": cold_min_prod,
            "M-COST-COLD-DEEP-PRODUCT": cold_deep_prod,
            "M-COST-PRODUCT-RATIO": (rep_prod / cold_prod) if cold_prod else None,
            "M-COST-PRODUCT-RATIO-MIN": (rep_prod / cold_min_prod) if cold_min_prod else None,
            "M-COST-PRODUCT-RATIO-DEEP": (rep_prod / cold_deep_prod) if cold_deep_prod else None,
            "M-COST-REPAIR-FETCH": rep_http,
            "M-COST-COLD-FETCH": cold_http,
            "M-COST-FETCH-RATIO": (rep_http / cold_http) if cold_http else None,
        }

    metrics = {"M-CLASSES": per_class,
               "M-NOISE-FALSE-TRIGGER-RATE": (None if nz_t.get("stale") is None
                                               else (1.0 if nz_t["stale"] else 0.0)),
               "M-NO-PERTURBATION-FALSE-TRIGGER-RATE": (None if np_t.get("stale") is None
                                                        else (1.0 if np_t["stale"] else 0.0)),
               "M-TRIALS-TOTAL": len(trials)}

    # ---- decision ----
    invalid = []
    if any(not r.get("valid") for r in trials):
        invalid.append("trial-invalid")
    for cls, m in per_class.items():
        if m["n"] < TRIALS_PER_CLASS:
            invalid.append(f"{cls}:n<{TRIALS_PER_CLASS}")
        if m["M-COLD-SUCCESS"] is None or m["M-COLD-SUCCESS"] < COLD_SUCCESS_BAR:
            invalid.append(f"{cls}:cold-baseline-not-live")
        if m["M-LITERAL-REPLAY-SUCCESS"] is None or m["M-LITERAL-REPLAY-SUCCESS"] > LITERAL_SUCCESS_BAR:
            invalid.append(f"{cls}:perturbation-does-not-bite")
        if m["M-NO-REPAIR-SUCCESS"] is None or m["M-NO-REPAIR-SUCCESS"] > LITERAL_SUCCESS_BAR:
            invalid.append(f"{cls}:no-repair-not-inert")
    if nz_t.get("stale") is not False or np_t.get("stale") is not False:
        invalid.append("negative-control-not-fresh")

    def functional_ok(m):
        return bool(m["M-REPAIR-SUCCESS"] is not None and m["M-REPAIR-SUCCESS"] >= REPAIR_SUCCESS_BAR
                    and m["M-REPAIR-SUCCESS-WILSON-LOWER"] >= WILSON_SUCCESS_LOWER_BAR
                    and m["M-CONTAMINATION-RATE"] is not None and m["M-CONTAMINATION-RATE"] <= CONTAMINATION_BAR
                    and m["M-WRITE-SET-MAX"] is not None and m["M-WRITE-SET-MAX"] <= 1
                    and m["M-GUARD-FIRE-RATE"] is not None and m["M-GUARD-FIRE-RATE"] >= GUARD_FIRE_BAR)

    def cost_verdict(m):
        """Registered staged cost verdict on the equal-weight product counter
        (primary) with the network-fetch counter as the operational driver."""
        if not functional_ok(m):
            return "FUNCTIONAL-FAIL"
        pr, fr = m["M-COST-PRODUCT-RATIO"], m["M-COST-FETCH-RATIO"]
        if pr is None or fr is None:
            return "COST-UNKNOWN"
        if pr < PRODUCT_COST_BAR and fr <= FETCH_COST_BAR:
            return "STRICT-WIN"          # strictly cheaper total AND on network
        if pr <= PRODUCT_COST_BAR and fr <= FETCH_COST_BAR:
            return "BOUNDED-WIN"         # cost-neutral total, strictly cheaper network
        if pr <= PRODUCT_COST_MAX and fr <= FETCH_COST_BAR:
            return "MIXED-TRADEOFF"      # network-cheaper, but total-cost regression
        return "COST-FAIL"

    def cost_stability(m):
        """Is the cost verdict the same at the L=2 / L=3 / L=4 cold budgets?"""
        vals = []
        for key in ("M-COST-PRODUCT-RATIO-MIN", "M-COST-PRODUCT-RATIO",
                    "M-COST-PRODUCT-RATIO-DEEP"):
            r = m.get(key)
            if r is not None:
                vals.append(r < PRODUCT_COST_MAX)
        return (len(set(vals)) <= 1) if vals else None

    cvs = {cls: cost_verdict(per_class[cls]) for cls in CLASSES}
    stable = {cls: cost_stability(per_class[cls]) for cls in CLASSES}
    if invalid:
        decision, status, outcome = None, "MEASUREMENT_INVALID", "INCONCLUSIVE"
    elif all(cvs[c] == "STRICT-WIN" for c in CLASSES):
        decision, status, outcome = "SUPPORTS", "COMPLETE", "SUPPORTS"
    elif all(cvs[c] in ("STRICT-WIN", "BOUNDED-WIN") for c in CLASSES):
        decision, status, outcome = "SUPPORTS-BOUNDED", "COMPLETE", "SUPPORTS"
    elif all(cvs[c] in ("STRICT-WIN", "BOUNDED-WIN", "MIXED-TRADEOFF") for c in CLASSES):
        decision, status, outcome = "MIXED-TRADEOFF", "COMPLETE", "MIXED"
    elif any(cvs[c] in ("STRICT-WIN", "BOUNDED-WIN", "MIXED-TRADEOFF") for c in CLASSES):
        decision, status, outcome = "MIXED", "COMPLETE", "MIXED"
    else:
        decision, status, outcome = "FALSIFIES", "COMPLETE", "FALSIFIES"

    out = {"status": status, "experiment_id": EXP_ID, "lane": "graph",
           "runner_self_sha": runner_self_sha, "seed": SEED,
           "invalid_reasons": invalid, "decision": decision, "outcome": outcome,
           "class_cost_verdicts": cvs, "cost_verdict_stable_across_cold_budget": stable,
           "metrics": metrics,
           "trials": trials,
           "nc_no_perturbation": np_t, "nc_noise": nz_t,
           "carrier": {
               "kernel_sha256": hashlib.sha256((ROOT / "src/spider/kernel.py").read_bytes()).hexdigest(),
               "models_sha256": hashlib.sha256((ROOT / "src/spider/models.py").read_bytes()).hexdigest(),
               "registry_sha256": hashlib.sha256((ROOT / "src/spider/registry.py").read_bytes()).hexdigest()}}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
<!-- END FROZEN-RUNNER -->
