# EXP-PRODUCT-38189918141 preregistration

**Lane:** product | **design_contract_version:** 2 | **status:** DESIGN (pre-freeze)
**Primary claim:** `C-PARAM-INHERIT` (EXPERIMENTAL) | **Secondary claim:** `C-SEMANTIC-RESOLVE` (HYPOTHESIS)
**Parent:** `EXP-PRODUCT-38186502935` (handoff sha256 `4e4956df16f9e0e729083367c2c960a8fcb3ad0c6834dc369562a2d8761d9365`, disposition USE)
**Director mandate:** `request.json#director_mandate` (action REOPEN, `C-PARAM-INHERIT`, cognitive_reset true, parent_handoff_disposition USE)

## 1. Scope and binding direction

This is a Product-local, non-externally-gated GENERALIZATION-BOUNDARY / OUT-OF-GRAMMAR FALSE-ACCEPT
certificate for the byte-identical installed carrier. It answers exactly the mandate question:

> is the carrier's conservative single-pattern support inference (`^item\-00[0-9]{1}$` learned from 5
> examples) a product defect or a correct abstention boundary -- i.e. on a materially varied /
> out-of-grammar payload bank does the carrier either bind correctly or refuse safely with ZERO false
> accepts, and exactly where does its generalization boundary lie?

It does NOT: re-run the readiness measurement (`item-000` positive / zero-HTTP `item-010` refusal are
inherited established state); test a substituted carrier; re-run the excluded mandatory-discovery
deterministic REST certificate; run or fund the four-arm C-LLM-INHERIT benchmark (readiness (2)
Runtime task bank and (3) Intel endpoint remain open and no mandate funds it). The runner is
READ-ONLY: it never writes `src/spider/` or any freeze artifact. `C-PARAM-INHERIT` stays
EXPERIMENTAL and `C-SEMANTIC-RESOLVE` stays HYPOTHESIS in ALL branches; no claim advance, no
promotion (the carrier was already promoted in `EXP-PRODUCT-38180719830`). No economics are measured
(`model_calls=0`, `model_tokens=0` by construction).

## 2. Inherited state (parent handoff `carry_forward`, preserved strictly)

- **established** (inherited, not re-measured here): readiness (1) is DISCHARGED on the
  byte-identical installed carrier -- 5 executed induction GETs distilled a mechanism with slots
  `['item']`, support `^item\-00[0-9]{1}$`, confidence `0.9`, resolving never-observed `item-000`
  EXECUTABLE -> oracle 200 -> verify true, with a zero-HTTP known-negative refusal on `item-010`;
  identity/premise holds read-only; counters honest and model-free; attribution controls pass; audit
  PASS. Evidence: `EXP-PRODUCT-38186502935/result.json`, `audit.json`, `run_e2e.out.json`.
- **rejected** (bounded to the parent fixture): "the installed carrier fails to execute end-to-end at
  shipped thresholds"; "the positive is attributable to the literal kernel/substrate".
- **unknown** (this packet's target): "whether the carrier's conservative single-pattern support
  inference generalizes or fails safely on materially varied / free-form payload values" was UNTESTED;
  only the in-support boundary (`item-000`) and out-of-support boundary (`item-010`) were probed.
- **do_not_assume** (binding here): do NOT read a PASS as advancing `C-PARAM-INHERIT`; do NOT
  generalize beyond the induced single-length support grammar; do NOT cite `mechanism_id` across runs
  (it embeds the ephemeral port); do NOT re-run the readiness measurement; do NOT test a substituted
  carrier (V4 stop trigger); do NOT re-run the excluded REST certificate; do NOT self-dispatch the
  four-arm benchmark.

This packet is a DISTINCT_EXTENSION: no pre-2.0 artifact tested the abstention boundary of a compiled
procedural carrier, and no parent measurement probed a materially varied payload bank.

## 3. Frozen treatment identity

- Carrier git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, sha256
  `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` == `src/spider/kernel.py`
  (verified at DESIGN; tree clean).
- Pre-promotion literal blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50`, sha256
  `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61` (ablation).
- Shipped thresholds: kernel default `min_confidence=0.8`; induced parameterized confidence `0.9`.

## 4. Frozen payload bank (78 items) and ground-truth label rule

The bank is built in-process inside the frozen runner (section 14) and is byte-frozen by
`freeze.json.hashes['prereg.md']`. It has 78 unique bids: 19 IN, 59 OUT.

**Label rule (declared identifier grammar under the fixed task schema):** an item is `IN` iff its
value is a `str` fullmatching `^item-[0-9]{3}$` AND `intent == 'read_item'` AND
`context == {'resource_type':'item','authenticated':True}` AND `params == {'item': value}`;
otherwise `OUT`.

- **IN (19, class `in_grammar`):** `item-000,001,002,003,004,005,006,007,008,009,010,011,042,099,
  100,123,256,500,999`.
- **OUT (59):** length 5 (`item-0`,`item-00`,`item-0000`,`item-00000`,`item-000000`); alpha 4
  (`item-00a`,`item-abc`,`item-a00`,`item-0x1`); case 2 (`ITEM-000`,`Item-000`); separator 4
  (`item_000`,`item.000`,`item:000`,`item/000`); whitespace 8 (`""`,`" "`,`"\t"`,`"\n"`,`"item-000 "`,
  `" item-000"`,`"item-000\n"`,`"item-000\t"`); injection 8 (`item-000;x`,`item-000'`,`item-000"`,
  `item-000\x00`,`../../etc/passwd`,`/api/items/item-000`,`http://evil.example/item-000`,
  `item-000/../secret`); query/fragment 4 (`item-000?x=1`,`item-000#frag`,`item-00%30`,`item-000%00`);
  unicode 2 (`item-00\u0663`,`item-00\uff10`); other prefixes 3 (`user-000`,`order-000`,`itemx000`);
  oversized 2 (`item-`+1000 zeros, `item-`+64 nines); non-string types 10 (`None,0,0.0,True,False,[],
  ['item-000'],{}, {'item':'item-000'}, b'item-000'`); context/intent/param mismatch 7
  (`resource_type=user`; `authenticated=False`; missing `authenticated`; empty context;
  `intent=delete_item`; `params={'wrong_key':...}`; `params={}`).

**DESIGN validation (non-outcome-bearing):** 78 unique bids; 19 IN / 59 OUT; every `in_grammar` item
`IN` and every other class `OUT`; **0 class/label mismatches**.

## 5. Inherited liveness + DESIGN satisfiability evidence

- Treatment liveness is INHERITED accepted evidence: `EXP-PRODUCT-38180719830` (promotion D1-D4 PASS)
  and `EXP-PRODUCT-38186502935` (full shipped path audit PASS on the byte-identical installed bytes).
- The induced support is an arithmetic function of the 5 training segment values (`item-001..005`):
  common prefix `item-00`, homogeneous digit class, uniform remainder length 1 -> `^item\-00[0-9]{1}$`
  (DESIGN probe: `_infer_support([...]) == '^item\-00[0-9]{1}$'`).
- Boundary predicate probe (value-level, no bank resolve): `_support_accepts(SHIPPED,'item-000')==True`,
  `_support_accepts(SHIPPED,'item-010')==False`.
- Detector-sensitivity probe: `_support_accepts(__COARSE__, v)` accepts 36 OUT string payloads, so
  `PC-UNSAFE-COARSE` false-accept margin >> 0.
- Refusal-route probe (public API, synthetic mechanism, no bank outcome): all 7
  context/intent/param-mismatch cases refuse with null action (5 exactly `UNKNOWN`, 2 `EXPLORE`
  missing-parameter) BEFORE the support check.
- Instrument probes: runner `py_compile` OK; helpers imported and unit-checked (bank/labels/summarize
  -> the three outcome mappings); regression 3/3; public API imports with default `min_confidence 0.8`.

## 6. Metrics (stable ids; all derived by the frozen runner)

| Metric | Definition |
| --- | --- |
| `M-FALSE-ACCEPT-COUNT` (primary) | T-SHIPPED OUT-labelled items with `resolve().status == EXECUTABLE` |
| `M-FALSE-ACCEPT-RATE` | `M-FALSE-ACCEPT-COUNT / n_out` |
| `M-SILENT-FALSE-ACCEPT-COUNT` | subset of false accepts that reach oracle 200 and `verify == True` |
| `M-FALSE-REJECT-COUNT` | T-SHIPPED IN-labelled items with `status != EXECUTABLE` |
| `M-COVERAGE` | `(n_in - M-FALSE-REJECT-COUNT) / n_in` |
| `M-REFUSAL-ZERO-HTTP` (co-primary) | total HTTP requests issued on OUT-labelled items (must be 0) |
| `M-BOUNDARY` | induced support regex + exact accepted/refused in-grammar id sets |
| `M-CONTROL-PC-COARSE-FALSE-ACCEPT-COUNT` | must be `>= 1` (detector sensitivity) |
| `M-CONTROL-NC-REJECT-ALL-ACCEPT-COUNT` / `...-HTTP-TOTAL` | must be `0` / `0` (null floor) |
| `M-COMPARATOR-WIDENED3-FALSE-ACCEPT-COUNT` / `...-COVERAGE` | strong comparator safety/coverage |
| `M-IDENTITY`, `M-DETERMINISM`, `M-REGRESSION` | validity gates |

## 7. Arms and controls (stable ids, reuse across EXECUTE/AUDIT)

- `T-SHIPPED` -- treatment: shipped carrier + 5-example induction (support `^item\-00[0-9]{1}$`).
- `PC-UNSAFE-COARSE` -- positive control: same mechanism, support rewritten to the carrier's own
  `__COARSE__` sentinel; MUST false-accept `>= 1` (non-vacuous safety oracle).
- `NC-REJECT-ALL` -- null control: empty registry; MUST accept nothing and issue zero HTTP.
- `B-WIDENED-3` -- strong comparator: same mechanism, support `^item\-[0-9]{3}$`; expected
  `FA == 0` AND `coverage == 1.0` (a safe, complete alternative). Recorded; not a hard gate.
- `B-LITERAL-KERNEL` -- ablation from git blob `cfec9866...`; MUST lack `distill_parameterized`.
- `PC-EXACT-REPLAY` -- 5 training ids re-resolve EXECUTABLE (execution-path control).
- `PC-DETERMINISM-REPEAT` -- two full runs must agree on treatment/coarse metrics and mechanism
  identity (port-invariant; `mechanism_id` excluded).
- `ORACLE-SERVER` -- in-process stdlib oracle: 200 for `^/api/items/item-[0-9]{3}$`, else 404;
  non-echo; its request counter is the authoritative HTTP measure.

## 8. Decision rule

**Gates (before any outcome mapping):**

1. **Validity gate** -- ALL of `V8-FREEZE-BINDING`, `M-IDENTITY`, `M-REGRESSION` (3/3),
   `PC-DETERMINISM-REPEAT`, `PC-EXACT-REPLAY` (5/5), `B-LITERAL-KERNEL` must PASS; else
   `status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`.
2. **Sensitivity gate** -- `PC-UNSAFE-COARSE FA >= 1` AND `NC-REJECT-ALL accept == 0` AND
   `NC-REJECT-ALL http == 0`; else `status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`.

**Outcome mapping (on a verified carrier with non-vacuous controls):**

| Condition | outcome | decision |
| --- | --- | --- |
| `M-FALSE-ACCEPT-COUNT > 0` or `M-REFUSAL-ZERO-HTTP > 0` | `FALSIFIES` | `SAFETY_DEFECT` |
| `FA == 0`, `HTTP-on-OUT == 0`, `M-FALSE-REJECT-COUNT == 0` | `SUPPORTS` | `SAFE_AND_COMPLETE` |
| `FA == 0`, `HTTP-on-OUT == 0`, `M-FALSE-REJECT-COUNT > 0` | `MIXED` | `SAFE_BUT_CONSERVATIVE` |

Precedence: `MEASUREMENT_INVALID > FALSIFIES > (SUPPORTS vs MIXED)`. Low coverage / false rejects
ALONE is NOT a safety falsification.

## 9. Consequences of both branches (preregistered)

- `SUPPORTS` / `MIXED` (`M-FALSE-ACCEPT-COUNT == 0`): the shipped UNKNOWN-preferring path is SAFE to
  expose to external agents on this bank (no out-of-grammar bind, zero out-of-grammar HTTP). If
  coverage `< 1.0`, the abstention boundary is documented as over-conservative, and when
  `B-WIDENED-3` passes, shown to be avoidable via a safe complete widening. External consumption is
  licensed with a documented coverage caveat; `C-PARAM-INHERIT` stays EXPERIMENTAL.
- `FALSIFIES` / `SAFETY_DEFECT`: at least one out-of-grammar payload binds (possibly silently
  executing with oracle 200 and verify true). External consumption stays blocked for this carrier;
  the exact offending bids + mechanism identity become the engineering-fix spec inside
  `resolve()`/support; `C-PARAM-INHERIT` stays EXPERIMENTAL and the four-arm benchmark remains
  unfunded.
- `BLOCKED` / `MEASUREMENT_INVALID`: the boundary cannot be assessed; the exact operational blocker
  (substituted carrier, freeze-binding mismatch, missing git object, fixture failure, vacuous
  control) is recorded. Infrastructure failure is NEVER repackaged as a scientific negative.

## 10. Validity threats / representation loss

- Single resource shape (`/api/items/item-NNN`) and a single in-process oracle; the boundary is
  measured for the induced single-length support grammar only, not for multi-resource or free-form
  semantics.
- `mechanism_id` embeds the ephemeral port and is NOT stable across runs; interpretation references
  support/slots/confidence, never `mechanism_id`.
- The oracle is a non-echo 200/404 fixture; it does not model real external side effects. The
  zero-HTTP requirement is a necessary, not sufficient, safety condition.
- `B-WIDENED-3` covers a 3-digit family boundary only; a genuinely free-form grammar is out of scope.
- The bank's OUT set necessarily encodes the declared grammar; it is a designed stress set, not a
  random sample of production traffic.

## 11. Validity gates (V1-V11, summarized; full text in spec.json#measurement_validity)

V1 determinism; V2 credential-free/model-free; V3 identity premise gate; V4 stop trigger; V5 bank
constructibility + label rule; V6 refusal semantics; V7 boundary honesty; V8 freeze binding
(prereg sha, runner == FROZEN RUNNER, SIX artifact hashes); V9 regression 3/3; V10 ablation
attribution; V11 control sensitivity (non-vacuous oracle).

## 12. Do-not-assume / scope discipline (from parent handoff, binding)

Do NOT read any branch as advancing `C-PARAM-INHERIT` (retained EXPERIMENTAL) or `C-SEMANTIC-RESOLVE`
(retained HYPOTHESIS); do NOT re-run the readiness measurement; do NOT test a substituted carrier
(V4); do NOT re-run the excluded mandatory-discovery REST certificate; do NOT self-dispatch the
four-arm benchmark; do NOT write any freeze artifact; do NOT cite `mechanism_id` across runs; do NOT
generalize beyond the fixed fixture and the induced support grammar.

## 13. Freeze artifacts and binding model

Freeze artifacts (SIX, all exist with recorded sha256 at DESIGN time): `pyproject.toml`,
`src/spider/__init__.py`, `src/spider/models.py`, `src/spider/registry.py`, `src/spider/kernel.py`
(read-only treatment -> immutable interpretation dependency), `tests/test_kernel.py`.

Binding model: the deterministic freeze step writes `freeze.json` pinning
`hashes['prereg.md'|'spec.json'|'request.json'|'design_review.json']` and `artifact_hashes` for the
six files. V8 enforces (A) prereg sha, (B) running runner source == the FROZEN RUNNER block extracted
from the hash-bound prereg, (C) all artifact hashes. The frozen bank, oracle and label rule are
in-process inside the runner, so no unbound dataset/task-bank/fixture remains.

## 14. FROZEN RUNNER (verbatim; bound by freeze.json.hashes['prereg.md'])

<!-- BEGIN FROZEN RUNNER -->
#!/usr/bin/env python3
"""FROZEN RUNNER for EXP-PRODUCT-38189918141 (embedded verbatim in prereg.md).

Read-only shipped-carrier GENERALIZATION-BOUNDARY certificate. Evaluates the
as-installed parameterized carrier (src/spider/kernel.py, git blob b15ed848... /
sha256 718efa6a...) on a frozen, materially varied payload bank with an
independent localhost oracle. NEVER writes src/spider/ and never calls a model.

Arms (stable ids):
  T-SHIPPED       shipped carrier + parent 5-example induction (treatment)
  PC-UNSAFE-COARSE same carrier, support overridden to the carrier's own
                  __COARSE__ fallback (positive control for the safety oracle)
  B-WIDENED-3     same carrier, support overridden to ^item\\-[0-9]{3}$ (safe
                  widening comparator)
  NC-REJECT-ALL   empty registry (null floor: zero accepts, zero HTTP)
  B-LITERAL-KERNEL pre-promotion literal kernel, lacks distill_parameterized
  PC-EXACT-REPLAY 5 trained ids re-resolve EXECUTABLE (execution-path control)
  ORACLE-SERVER   localhost oracle: 200 for /api/items/item-[0-9]{3}, else 404

Env overrides (hermetic dry-run only; never change certificate logic):
  EXP_TARGET_ROOT : repo root containing src/spider (default: auto-detected)
  EXP_PROBE_MODE  : "1" records UNBOUND-RUN for V8 when freeze.json is absent
"""
from __future__ import annotations

import copy
import hashlib
import http.server
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

# -- canonical identities (mirrors prereg CANONICAL-HASHES) --
CARRIER_BLOB = "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796"
CARRIER_SHA256 = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
LITERAL_BLOB = "cfec98660b0277ccbf295e8a4119e8d81ddccf50"
LITERAL_SHA256 = "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61"
EXPERIMENT_ID = "EXP-PRODUCT-38189918141"
EXP_DIR = "research/experiments/EXP-PRODUCT-38189918141"
INTENT = "read_item"
TREATMENT_CONTEXT = {"resource_type": "item", "authenticated": True}
TRAIN_IDS = ["item-001", "item-002", "item-003", "item-004", "item-005"]
EXPECTED_SUPPORT = r"^item\-00[0-9]{1}$"
WIDENED_SUPPORT = r"^item\-[0-9]{3}$"
EXPECTED_MIN_CONFIDENCE = 0.8
COARSE = "__COARSE__"
LABEL_RE = re.compile(r"item-[0-9]{3}")
VALID_RESOURCE_RE = re.compile(r"^/api/items/item-[0-9]{3}$")


def detect_repo_root() -> Path:
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "pyproject.toml").exists() and (p / "src/spider").exists():
            return p
        p = p.parent
    raise RuntimeError("repo root not found upward from runner")


REPO_ROOT = Path(os.environ.get("EXP_TARGET_ROOT") or str(detect_repo_root()))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_source(spec: str) -> bytes:
    if spec.startswith("git:"):
        out = subprocess.run(["git", "-C", str(REPO_ROOT), "cat-file", "blob", spec[4:]],
                             capture_output=True)
        if out.returncode != 0:
            raise RuntimeError("git blob unavailable: " + out.stderr.decode()[:200])
        return out.stdout
    if spec.startswith("file:"):
        return Path(spec[5:]).read_bytes()
    raise RuntimeError("unknown source spec: " + spec)


# ---------------------------------------------------------------- frozen bank
def _bank_spec() -> list[dict]:
    C = dict(TREATMENT_CONTEXT)
    bank: list[dict] = []

    def add(bid, value, cls, intent=INTENT, context=None, params=None):
        bank.append({"bid": bid, "value": value, "cls": cls, "intent": intent,
                     "context": dict(context) if context is not None else dict(C),
                     "params": dict(params) if params is not None else {"item": value}})

    for n in ["000", "001", "002", "003", "004", "005", "006", "007", "008", "009",
              "010", "011", "042", "099", "100", "123", "256", "500", "999"]:
        add("IG-" + n, "item-" + n, "in_grammar")
    add("OG-LEN-0", "item-0", "len")
    add("OG-LEN-00", "item-00", "len")
    add("OG-LEN-4", "item-0000", "len")
    add("OG-LEN-5", "item-00000", "len")
    add("OG-LEN-6", "item-000000", "len")
    add("OG-ALPHA-00A", "item-00a", "alpha")
    add("OG-ALPHA-ABC", "item-abc", "alpha")
    add("OG-ALPHA-A00", "item-a00", "alpha")
    add("OG-ALPHA-0X1", "item-0x1", "alpha")
    add("OG-CASE-UP", "ITEM-000", "case")
    add("OG-CASE-TITLE", "Item-000", "case")
    add("OG-SEP-US", "item_000", "sep")
    add("OG-SEP-DOT", "item.000", "sep")
    add("OG-SEP-COLON", "item:000", "sep")
    add("OG-SEP-SLASH", "item/000", "sep")
    add("OG-WS-EMPTY", "", "ws")
    add("OG-WS-SPACE", " ", "ws")
    add("OG-WS-TAB", "\t", "ws")
    add("OG-WS-NL", "\n", "ws")
    add("OG-WS-TRAIL", "item-000 ", "ws")
    add("OG-WS-LEAD", " item-000", "ws")
    add("OG-WS-TRAILNL", "item-000\n", "ws")
    add("OG-WS-TRAILTAB", "item-000\t", "ws")
    add("OG-INJ-SEMI", "item-000;x", "inj")
    add("OG-INJ-SQ", "item-000'", "inj")
    add("OG-INJ-DQ", 'item-000"', "inj")
    add("OG-INJ-NUL", "item-000\x00", "inj")
    add("OG-INJ-TRAV", "../../etc/passwd", "inj")
    add("OG-INJ-ABS", "/api/items/item-000", "inj")
    add("OG-INJ-URL", "http://evil.example/item-000", "inj")
    add("OG-INJ-DOTDOT", "item-000/../secret", "inj")
    add("OG-QRY", "item-000?x=1", "query")
    add("OG-FRAG", "item-000#frag", "query")
    add("OG-PCT", "item-00%30", "query")
    add("OG-PCTNUL", "item-000%00", "query")
    add("OG-UNI-AR", "item-00\u0663", "unicode")
    add("OG-UNI-FW", "item-00\uff10", "unicode")
    add("OG-OTH-USER", "user-000", "other")
    add("OG-OTH-ORDER", "order-000", "other")
    add("OG-OTH-X", "itemx000", "other")
    add("OG-BIG-1000", "item-" + "0" * 1000, "big")
    add("OG-BIG-64", "item-" + "9" * 64, "big")
    add("OG-TYP-NONE", None, "type")
    add("OG-TYP-INT0", 0, "type")
    add("OG-TYP-FLOAT", 0.0, "type")
    add("OG-TYP-TRUE", True, "type")
    add("OG-TYP-FALSE", False, "type")
    add("OG-TYP-LIST", [], "type")
    add("OG-TYP-LISTV", ["item-000"], "type")
    add("OG-TYP-DICT", {}, "type")
    add("OG-TYP-DICTV", {"item": "item-000"}, "type")
    add("OG-TYP-BYTES", b"item-000", "type")
    add("OG-CTX-USERTYPE", "item-000", "ctx",
        context={"resource_type": "user", "authenticated": True})
    add("OG-CTX-NOAUTH", "item-000", "ctx",
        context={"resource_type": "item", "authenticated": False})
    add("OG-CTX-MISSAUTH", "item-000", "ctx", context={"resource_type": "item"})
    add("OG-CTX-EMPTY", "item-000", "ctx", context={})
    add("OG-CTX-INTENT", "item-000", "ctx", intent="delete_item")
    add("OG-CTX-WRONGKEY", "item-000", "ctx", params={"wrong_key": "item-000"})
    add("OG-CTX-NOPARAM", "item-000", "ctx", params={})
    return bank


def label_of(item: dict) -> str:
    v = item["value"]
    if not isinstance(v, str):
        return "OUT"
    if not LABEL_RE.fullmatch(v):
        return "OUT"
    if item["intent"] != INTENT:
        return "OUT"
    if item["context"] != TREATMENT_CONTEXT:
        return "OUT"
    if item["params"] != {"item": v}:
        return "OUT"
    return "IN"


def value_repr(v) -> str:
    if isinstance(v, str):
        s = repr(v)
        return s if len(s) <= 140 else s[:140] + "...<%d chars>" % len(v)
    if isinstance(v, (int, float, bool)) or v is None:
        return repr(v)
    return type(v).__name__ + ":" + repr(v)[:80]


# --------------------------------------------------------------- oracle server
class OracleHandler(http.server.BaseHTTPRequestHandler):
    count = 0

    def do_GET(self):
        type(self).count += 1
        path = self.path.split("?", 1)[0]
        if VALID_RESOURCE_RE.fullmatch(path):
            ident = path.rsplit("/", 1)[-1]
            body = {"type": "item", "id": ident, "data": "res:" + ident}
            self.send_response(200)
        else:
            body = {"error": "not_found", "path": path}
            self.send_response(404)
        payload = json.dumps(body).encode()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


def start_oracle():
    handler = type("Oracle", (OracleHandler,), {"count": 0})
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1], handler


def execute_action(bound):
    url = bound.get("url") if isinstance(bound, dict) else None
    if not isinstance(url, str):
        return None, {"exec_error": "no_url"}
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())
    except Exception as exc:
        return None, {"exec_error": type(exc).__name__ + ": " + str(exc)[:160]}


def drop_modules():
    for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
        sys.modules.pop(m, None)


def make_arm_mechanism(mech, support, tmpdir, tag):
    reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry
    reg = reg_cls(Path(tmpdir) / ("mechanisms_%s.jsonl" % tag))
    m = copy.deepcopy(mech)
    m.verification_rule = {"parameter_supports": {s: support for s in m.parameter_slots}}
    reg.upsert(m)
    return reg


def evaluate(kernel, bank, handler):
    records = []
    for item in bank:
        http0 = handler.count
        rec = {"bid": item["bid"], "cls": item["cls"], "label": label_of(item),
               "value": value_repr(item["value"])}
        try:
            r = kernel.resolve(item["intent"], dict(item["context"]), dict(item["params"]))
            rec["status"] = r.status.value
            rec["reason"] = r.reason
            bound = r.bound_action
        except Exception as exc:
            rec["status"] = "RESOLVE_ERROR"
            rec["reason"] = type(exc).__name__ + ": " + str(exc)[:160]
            bound = None
        rec["bound"] = bound is not None
        ex_status, body, verify = None, None, None
        if bound is not None:
            ex_status, body = execute_action(bound)
            if ex_status == 200 and isinstance(body, dict):
                try:
                    verify = kernel.verify(item.get("_mech_id"), body, dict(item["params"]))
                except Exception:
                    verify = False
            elif ex_status is not None:
                verify = False
        rec["exec_status"] = ex_status
        rec["verify"] = verify
        rec["exec_error"] = body.get("exec_error") if isinstance(body, dict) else None
        rec["http_delta"] = handler.count - http0
        records.append(rec)
    return records


def summarize(records):
    n_in = sum(1 for r in records if r["label"] == "IN")
    n_out = sum(1 for r in records if r["label"] == "OUT")
    accepts = [r for r in records if r["status"] == "EXECUTABLE"]
    fa = [r for r in records if r["label"] == "OUT" and r["status"] == "EXECUTABLE"]
    sfa = [r for r in fa if r["exec_status"] == 200 and r["verify"] is True]
    fr = [r for r in records if r["label"] == "IN" and r["status"] != "EXECUTABLE"]
    http_out = sum(r["http_delta"] for r in records if r["label"] == "OUT")
    http_total = sum(r["http_delta"] for r in records)
    cov = (n_in - len(fr)) / n_in if n_in else None
    return {
        "n_in": n_in, "n_out": n_out,
        "accept_count": len(accepts),
        "false_accept_count": len(fa),
        "silent_false_accept_count": len(sfa),
        "false_reject_count": len(fr),
        "coverage": cov,
        "http_on_out_label": http_out,
        "http_total": http_total,
        "false_accept_bids": [r["bid"] for r in fa],
        "silent_false_accept_bids": [r["bid"] for r in sfa],
        "false_reject_bids": [r["bid"] for r in fr],
        "accept_bids": [r["bid"] for r in accepts],
    }


# --------------------------------------------------------------- V8 freeze bind
def _extract(text, name):
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END " + re.escape(name) + r" -->",
                  text, re.S)
    if not m:
        raise RuntimeError("block %s not found in prereg.md" % name)
    return m.group(1)


def v8_freeze_binding(result):
    probe = os.environ.get("EXP_PROBE_MODE") == "1"
    exp = REPO_ROOT / EXP_DIR
    freeze_path = exp / "freeze.json"
    if not freeze_path.exists():
        if probe:
            result["observations"].append({"type": "binding",
                                           "V8": "UNBOUND-RUN: no freeze.json (probe mode only)."})
            return True
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "freeze.json missing at %s (EXECUTE mode)" % freeze_path}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    try:
        freeze = json.loads(freeze_path.read_text())

        def norm(s):
            return s.replace("\r\n", "\n").rstrip()

        prereg_b = (exp / "prereg.md").read_bytes()
        block = _extract(prereg_b.decode("utf-8"), "FROZEN RUNNER")
        this_src = Path(__file__).resolve().read_text(encoding="utf-8")
        ok_a = hashlib.sha256(prereg_b).hexdigest() == freeze["hashes"]["prereg.md"]
        ok_b = norm(this_src) == norm(block)
        ok_c = all(hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest() == h
                   for rel, h in freeze.get("artifact_hashes", {}).items())
    except Exception as exc:
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID", "reason": "freeze binding unreadable: " + str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    ok_all = ok_a and ok_b and ok_c
    result["certificate"]["V8_FREEZE_BINDING"] = {
        "status": "PASS" if ok_all else "FAIL", "prereg_sha_matches": ok_a,
        "runner_source_matches_frozen_block": ok_b, "artifact_hashes_match": ok_c,
        "reason": "hash-bound prereg; running source == FROZEN RUNNER block; freeze artifacts intact"}
    if not ok_all:
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    return True


# -------------------------------------------------------------------- one run
def run_once(carrier_cls, counters_cls, reg_cls, mech_cls, obs_cls):
    server, port, handler = start_oracle()
    try:
        tmp = tempfile.mkdtemp(prefix="exp38189918141_")

        def new_kernel(tag):
            reg = reg_cls(Path(tmp) / ("reg_%s.jsonl" % tag))
            return reg, carrier_cls(reg, counters=counters_cls())

        reg, kernel = new_kernel("treatment")
        observations = []
        for ident in TRAIN_IDS:
            url = "http://127.0.0.1:%d/api/items/%s" % (port, ident)
            st, body = execute_action({"url": url})
            if st != 200:
                raise RuntimeError("induction GET %s -> %s" % (ident, st))
            observations.append(obs_cls(intent=INTENT, state=dict(TREATMENT_CONTEXT),
                                        action={"method": "GET", "url": url},
                                        next_state=body, success=True,
                                        provenance={"exp": EXPERIMENT_ID, "role": "induction"}))
        mech = kernel.distill_parameterized(observations)
        if mech is None:
            raise RuntimeError("distill_parameterized returned None")
        reg.upsert(mech)
        support = mech.verification_rule["parameter_supports"]
        identity = {"slots": list(mech.parameter_slots), "support": support,
                    "confidence": mech.confidence}

        bank = _bank_spec()
        for item in bank:
            item["_mech_id"] = mech.mechanism_id

        treat_recs = evaluate(kernel, bank, handler)

        coarse_reg = make_arm_mechanism(mech, COARSE, tmp, "coarse")
        coarse_recs = evaluate(carrier_cls(coarse_reg, counters=counters_cls()), bank, handler)
        widened_reg = make_arm_mechanism(mech, WIDENED_SUPPORT, tmp, "widened")
        widened_recs = evaluate(carrier_cls(widened_reg, counters=counters_cls()), bank, handler)
        empty_reg = reg_cls(Path(tmp) / "reg_empty.jsonl")
        empty_recs = evaluate(carrier_cls(empty_reg, counters=counters_cls()), bank, handler)

        replay = []
        for ident in TRAIN_IDS:
            r = kernel.resolve(INTENT, dict(TREATMENT_CONTEXT), {"item": ident})
            replay.append({"id": ident, "status": r.status.value})
        replay_ok = all(x["status"] == "EXECUTABLE" for x in replay)

        return {
            "mechanism_identity": identity,
            "treatment": summarize(treat_recs),
            "control_coarse": summarize(coarse_recs),
            "comparator_widened": summarize(widened_recs),
            "null_reject_all": summarize(empty_recs),
            "pc_exact_replay": {"status": "PASS" if replay_ok else "FAIL", "replay": replay},
            "treatment_records": treat_recs,
        }
    finally:
        server.shutdown()


def main():
    result = {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": "product",
              "certificate": {}, "observations": [], "unresolved": []}
    if not v8_freeze_binding(result):
        return result

    kernel_path = REPO_ROOT / "src/spider/kernel.py"
    shipping_sha = sha256_bytes(kernel_path.read_bytes())
    result["identities"] = {"shipping_kernel_sha256": shipping_sha,
                            "carrier_expected_sha256": CARRIER_SHA256,
                            "carrier_git_blob": CARRIER_BLOB}
    if shipping_sha != CARRIER_SHA256:
        result["certificate"]["M-IDENTITY"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "shipping kernel sha %s != frozen carrier %s" % (shipping_sha, CARRIER_SHA256)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result
    result["certificate"]["M-IDENTITY"] = {
        "status": "PASS", "reason": "shipping kernel == frozen carrier " + CARRIER_BLOB}

    sys.path.insert(0, str(REPO_ROOT / "src"))
    try:
        drop_modules()
        spider = __import__("spider")
        Carrier = spider.SpiderKernel
        obs_cls = spider.Observation
        counters_cls = __import__("spider.kernel", fromlist=["TrajectoryCounters"]).TrajectoryCounters
        reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry
        min_conf = Carrier.__init__.__defaults__[0]
        if min_conf != EXPECTED_MIN_CONFIDENCE:
            raise RuntimeError("shipped min_confidence default %s != %s" % (min_conf, EXPECTED_MIN_CONFIDENCE))
    except Exception as exc:
        result["certificate"]["M-IDENTITY"] = {"status": "MEASUREMENT_INVALID",
                                              "reason": "import/threshold failure: " + str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result

    # B-LITERAL-KERNEL ablation
    try:
        lit = read_source("git:" + LITERAL_BLOB)
        if sha256_bytes(lit) != LITERAL_SHA256:
            raise RuntimeError("literal blob sha mismatch")
        with tempfile.TemporaryDirectory() as td:
            pkg = Path(td) / "spider"
            pkg.mkdir(parents=True)
            for name in ("models.py", "registry.py", "__init__.py"):
                (pkg / name).write_bytes((REPO_ROOT / "src/spider" / name).read_bytes())
            (pkg / "kernel.py").write_bytes(lit)
            sys.path.insert(0, td)
            drop_modules()
            litpkg = __import__("spider")
            has_param = hasattr(litpkg.SpiderKernel, "distill_parameterized")
            sys.path.remove(td)
            drop_modules()
        result["certificate"]["B-LITERAL-KERNEL"] = {
            "status": "PASS" if not has_param else "FAIL",
            "has_distill_parameterized": has_param,
            "reason": "literal pre-promotion kernel cannot construct the parameterized mechanism"}
    except Exception as exc:
        result["certificate"]["B-LITERAL-KERNEL"] = {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result

    drop_modules()
    spider = __import__("spider")
    Carrier = spider.SpiderKernel
    obs_cls = spider.Observation
    counters_cls = __import__("spider.kernel", fromlist=["TrajectoryCounters"]).TrajectoryCounters
    reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry

    run1 = run_once(Carrier, counters_cls, reg_cls, spider.Mechanism, obs_cls)
    run2 = run_once(Carrier, counters_cls, reg_cls, spider.Mechanism, obs_cls)
    det = json.dumps(run1["treatment"], sort_keys=True) == json.dumps(run2["treatment"], sort_keys=True) \
        and json.dumps(run1["control_coarse"], sort_keys=True) == json.dumps(run2["control_coarse"], sort_keys=True) \
        and run1["mechanism_identity"] == run2["mechanism_identity"]
    result["certificate"]["PC-DETERMINISM-REPEAT"] = {
        "status": "PASS" if det else "FAIL",
        "reason": "two independent runs produce identical treatment/coarse metrics and mechanism identity"}

    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test_*.py")
    tr = unittest.TextTestRunner(verbosity=0).run(suite)
    result["certificate"]["M-REGRESSION"] = {
        "status": "PASS" if (tr.wasSuccessful() and tr.testsRun >= 3) else "FAIL",
        "tests_run": tr.testsRun, "failures": len(tr.failures), "errors": len(tr.errors)}

    t = run1["treatment"]
    result["certificate"]["T-SHIPPED"] = {
        "status": "PASS" if (t["false_accept_count"] == 0 and t["http_on_out_label"] == 0
                             and run1["pc_exact_replay"]["status"] == "PASS") else "FAIL",
        "false_accept_count": t["false_accept_count"],
        "silent_false_accept_count": t["silent_false_accept_count"],
        "false_reject_count": t["false_reject_count"],
        "coverage": t["coverage"],
        "http_on_out_label": t["http_on_out_label"],
        "false_accept_bids": t["false_accept_bids"],
        "silent_false_accept_bids": t["silent_false_accept_bids"],
        "false_reject_bids": t["false_reject_bids"],
        "accept_bids": t["accept_bids"],
        "reason": "carrier safety (zero out-of-grammar binds, zero HTTP on out-of-grammar) "
                  "plus coverage on the declared 3-digit id scheme"}
    result["certificate"]["PC-EXACT-REPLAY"] = run1["pc_exact_replay"]
    result["certificate"]["PC-UNSAFE-COARSE"] = {
        "status": "PASS" if run1["control_coarse"]["false_accept_count"] >= 1 else "FAIL",
        "false_accept_count": run1["control_coarse"]["false_accept_count"],
        "false_accept_bids": run1["control_coarse"]["false_accept_bids"],
        "reason": "positive control: the carrier's own __COARSE__ fallback must over-accept"}
    result["certificate"]["NC-REJECT-ALL"] = {
        "status": "PASS" if (run1["null_reject_all"]["accept_count"] == 0
                             and run1["null_reject_all"]["http_total"] == 0) else "FAIL",
        "accept_count": run1["null_reject_all"]["accept_count"],
        "http_total": run1["null_reject_all"]["http_total"],
        "reason": "null floor: empty registry accepts nothing and issues no HTTP"}
    result["certificate"]["B-WIDENED-3"] = {
        "status": "PASS" if (run1["comparator_widened"]["false_accept_count"] == 0
                             and run1["comparator_widened"]["coverage"] == 1.0) else "FAIL",
        "false_accept_count": run1["comparator_widened"]["false_accept_count"],
        "coverage": run1["comparator_widened"]["coverage"],
        "reason": "strong comparator: a safe 3-digit widening that is both safe and complete on the bank"}

    result["arms"] = {
        "T-SHIPPED": run1["treatment"],
        "PC-UNSAFE-COARSE": run1["control_coarse"],
        "B-WIDENED-3": run1["comparator_widened"],
        "NC-REJECT-ALL": run1["null_reject_all"],
    }
    result["mechanism_identity"] = run1["mechanism_identity"]
    result["treatment_records"] = run1["treatment_records"]
    result["certificate"]["M-BOUNDARY"] = {
        "induced_support": run1["mechanism_identity"]["support"],
        "accepted_in_grammar_ids": sorted(
            r["value"] for r in run1["treatment_records"]
            if r["label"] == "IN" and r["status"] == "EXECUTABLE"),
        "refused_in_grammar_ids": sorted(
            r["value"] for r in run1["treatment_records"]
            if r["label"] == "IN" and r["status"] != "EXECUTABLE"),
        "reason": "exact generalization boundary: which declared 3-digit ids the shipped "
                  "single-observation-length support binds vs refuses"}

    validity_gates = ("V8_FREEZE_BINDING", "M-IDENTITY", "M-REGRESSION",
                      "PC-DETERMINISM-REPEAT", "PC-EXACT-REPLAY", "B-LITERAL-KERNEL")
    validity = all(result["certificate"][k]["status"] == "PASS" for k in validity_gates)
    failed_validity = [k for k in validity_gates if result["certificate"][k]["status"] != "PASS"]
    sensitivity = (result["certificate"]["PC-UNSAFE-COARSE"]["status"] == "PASS"
                   and result["certificate"]["NC-REJECT-ALL"]["status"] == "PASS")
    if not validity:
        result["status"], result["outcome"] = "MEASUREMENT_INVALID", "NOT_APPLICABLE"
        result["reason"] = "instrument/validity gates failed: " + ", ".join(failed_validity)
        return result
    if not sensitivity:
        result["status"], result["outcome"] = "MEASUREMENT_INVALID", "NOT_APPLICABLE"
        result["reason"] = "safety oracle failed its sensitivity/null controls; cannot certify"
        return result

    fa = t["false_accept_count"]
    fr = t["false_reject_count"]
    widened_ok = result["certificate"]["B-WIDENED-3"]["status"] == "PASS"
    if fa > 0 or t["http_on_out_label"] > 0:
        result["status"], result["outcome"] = "COMPLETE", "FALSIFIES"
        result["decision"] = "SAFETY_DEFECT"
        result["reason"] = ("%d out-of-grammar payload(s) bound (silent=%d), HTTP on "
                            "out-of-grammar=%d; external consumption must be blocked until "
                            "resolve()/support is fixed"
                            % (fa, t["silent_false_accept_count"], t["http_on_out_label"]))
    elif fr == 0:
        result["status"], result["outcome"] = "COMPLETE", "SUPPORTS"
        result["decision"] = "SAFE_AND_COMPLETE"
        result["reason"] = "zero false accepts and full coverage on the declared bank"
    else:
        result["status"], result["outcome"] = "COMPLETE", "MIXED"
        result["decision"] = "SAFE_BUT_CONSERVATIVE"
        alt = ("B-WIDENED-3 demonstrates a safe, complete alternative"
               if widened_ok else "B-WIDENED-3 did not demonstrate a safe complete alternative")
        result["reason"] = ("zero false accepts (safe abstention boundary) but %d/%d legitimate "
                            "declared ids refused; %s" % (fr, t["n_in"], alt))
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True, default=repr))

<!-- END FROZEN RUNNER -->

## 15. CANONICAL-HASHES

Frozen canonical identities for the freeze step (bind via `freeze.json.hashes['prereg.md']`):

- Carrier git blob: `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`
  - sha256: `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`
- Literal (pre-promotion shipped) git blob: `cfec98660b0277ccbf295e8a4119e8d81ddccf50`
  - sha256: `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`
- Freeze artifacts (sha256, verified at DESIGN time):
  - `pyproject.toml`: `5f03fb5914f388c19973831287cce6773c7364e1bea856a595cd7247d3115b83`
  - `src/spider/__init__.py`: `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77`
  - `src/spider/models.py`: `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78`
  - `src/spider/registry.py`: `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c`
  - `src/spider/kernel.py`: `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` (== carrier)
  - `tests/test_kernel.py`: `ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6`
- Induced arithmetic (probe-verified): support `^item\-00[0-9]{1}$`, slots `['item']`, confidence
  `0.9`, default `min_confidence` `0.8`.
- Bank: 78 items (19 IN / 59 OUT), 0 class/label mismatches.

## 16. EXECUTE contract

1. Verify `request.json`, `spec.json`, `prereg.md` are the frozen versions (hashes match
   `freeze.json`); `git status` clean; shipping kernel sha == `718efa6a...` (premise re-check).
2. Materialize the runner: extract the `FROZEN RUNNER` block from the hash-bound `prereg.md` verbatim
   to `research/experiments/EXP-PRODUCT-38189918141/harness/run_bank.py` (write the file only).
3. Run `python3 research/experiments/EXP-PRODUCT-38189918141/harness/run_bank.py` with NO env
   overrides (EXECUTE mode; V8 enforced; shipped thresholds; no writes to `src/spider/`).
4. Preserve raw evidence: `run_bank.out.json`, `run_bank.log`, `run_bank.repeat.out.json` in the
   experiment dir; keep raw records, observations, derived metrics and interpretation distinct.
5. Write `result.json` (mandatory top-level shape: `schema_version`, `experiment_id`, `lane`,
   `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`,
   `unresolved`), `report.md`, `provenance.json`. `status=COMPLETE` with a negative/mixed `outcome`
   is a valid scientific result; `status=BLOCKED`/`outcome=MEASUREMENT_INVALID` records the exact
   operational blocker and is NEVER a negative.
6. Do NOT re-run the readiness measurement, do NOT test a substituted carrier, do NOT re-run the
   excluded mandatory-discovery REST certificate, do NOT write any freeze artifact, do NOT run the
   four-arm benchmark, do NOT git-commit/push. A DIRECTOR verdict consumes this packet.

## 17. Consequences of both branches (preregistered)

See section 9. In ALL branches `C-PARAM-INHERIT` stays EXPERIMENTAL, `C-SEMANTIC-RESOLVE` stays
HYPOTHESIS, no claim is advanced or promoted, and the four-arm benchmark remains unfunded.
