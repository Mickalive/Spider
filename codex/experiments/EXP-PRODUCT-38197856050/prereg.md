# Preregistration — EXP-PRODUCT-38197856050

- Lane: `product`
- Claim target (binding Director mandate): `C-PARAM-INHERIT`
- Dependency claims: `C-MEAS-VALID`, `C-LLM-INHERIT`
- `design_contract_version`: 2
- Status: **FROZEN** (DESIGN). Outcome-bearing execution is EXECUTE's job; no confirmatory measurement was taken during DESIGN.
- Immutable request: `research/experiments/EXP-PRODUCT-38197856050/request.json` (base_sha `2e6945546a700c19b7fd411ea8daa30aae66e6dd`, chain_depth `0`).
- Spec: `research/experiments/EXP-PRODUCT-38197856050/spec.json`.

## 1. Scope, mandate, inherited state

The Global Research Director mandate **REOPEN**s `C-PARAM-INHERIT` with
`parent_handoff_disposition=SUPERSEDE` (reason `global-director-REOPEN`). The parent handoff
(`EXP-PRODUCT-38189918141`) is *continuity evidence only*: it may not silently override the
SUPERSEDE/REOPEN decision. This experiment asks the smallest discriminating question that can
change the product decision about the shipped carrier.

### 1.1 Inherited state (preserved verbatim in category, not re-litigated)

**Established (accepted):**
- The shipped carrier (git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, sha256
  `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`, == `src/spider/kernel.py`)
  parameterizes a repeated item request into a support and re-binds it via
  `distill_parameterized` → `resolve`/`verify`.
- On the parent frozen bank (n=78; 19 IN, 59 OUT) the shipped induced support
  `^item\-00[0-9]{1}$` yielded `M-FALSE-ACCEPT-COUNT=0`, `M-FALSE-REJECT-COUNT=9`,
  `M-COVERAGE=0.5263157894736842`.
- `B-WIDENED-3` (`^item\-[0-9]{3}$`) was *safe and complete* on that bank; the literal-kernel
  pre-promotion blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50` (sha256
  `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`) lacks
  `distill_parameterized`.

**Rejected (do not re-run, do not assume true):**
- The four-arm `C-LLM-INHERIT` benchmark was NOT funded/run; no LLM-inheritance result exists.
- Safety certificate / readiness / excluded mandatory-discovery REST certificate from the parent
  experiment were **do_not_assume**; this prereg does not reuse them as evidence.

**Unknown:**
- Whether a *principled*, carrier-derived widening rule can attain `M-COVERAGE=1.0` with
  `M-FALSE-ACCEPT-COUNT=0` (equivalently zero HTTP-on-OUT) on a bank that includes
  variable-width and pinned-subrange families. This is the question.
- Whether the parent's single-family safety result generalizes beyond uniform-width `item-00X`.

**do_not_assume (parent):** (a) do not re-run the parent safety/readiness/excluded REST
certificate; (b) do not substitute a different carrier; (c) do not self-dispatch the four-arm
`C-LLM-INHERIT` benchmark.

### 1.2 Non-duplication

A keyword scan of `codex/legacy_artifact_index.json` for the mechanisms in scope
("support", "widen", "parameter", "grammar", "coverage", "false accept") returned
**NO_MATCH** to prior legacy artifacts. The nearest legacy neighbours are `P2-REPLAY-COST`
and `P2-BLIND-COMPOSITION` (both about cost/composition, not support widening). This is a
pre-2.0-independent, post-2.0 question and does not repeat pre-2.0 work.

## 2. Question, hypotheses, falsifier

**Question.** Can the shipped carrier widen its induced parameter support toward total coverage
without ever binding a value that the application would reject (i.e. without emitting a request
path that the service returns non-success/404 for)?

**H1 (product-hypothesis).** A principled widening rule derived by generalizing the observed
value grammar (widening the fixed width component to the smallest safe superset, using only
observed structural evidence) attains `M-T-WIDENED-COVERAGE = 1.0` with
`M-T-WIDENED-FALSE-ACCEPT-COUNT = 0` and `M-T-WIDENED-HTTP-ON-OUT = 0` on the frozen four-family
bank.

**H0 (null).** No such principled rule exists for all families: the carrier's observed
grammar does not uniquely identify a safe superset, so any widened rule that closes the
coverage gap also binds at least one out-of-grammar value (false accept), observable as a
non-success HTTP response from the oracle.

**Falsifier (decisive).** The frozen bank contains family `FAM-D` whose training values are a
*pinned subrange* `region-000..region-009`. The principled widening rule emits
`^region\-[0-9]{3}$`, which **over-accepts** `region-010..region-999`. If even one `FAM-D` OUT
item (e.g. `FD-OG-WRONGRANGE00` = `region-010`) is bound and executed against the oracle and the
oracle returns non-success, H1 is falsified (`outcome=FALSIFIES`, `decision=WIDENING_UNSAFE`).

## 3. Frozen bank and label rule

`harness/run_bank.py` (Section 14, FROZEN RUNNER) enumerates a single frozen bank of n=292
unique items in four families. Each family has a resource stem, an `id_prefix`, and a declared
inner pattern; the *declared pattern is the oracle's contract*, and the OUT label is assigned
purely by whether the concrete value matches the declared inner pattern for that family.

| family | resource path | train values | declared inner pattern |
|---|---|---|---|
| `FAM-A` | `/api/items/item-<id>` | `item-001`..`item-005` | `^item\-[0-9]{3}$` |
| `FAM-B` | `/api/accounts/acct-<id>` | `acct-0001`..`acct-0005` | `^acct\-[0-9]{4}$` |
| `FAM-C` | `/api/docs/doc-<id>` | `doc-01`..`doc-05` | `^doc\-[0-9]{1,4}$` |
| `FAM-D` | `/api/regions/region-<id>` | `region-000`..`region-009` | `^region\-00[0-9]$` |

Expected bank composition (frozen by the runner, re-derived in DESIGN probe): n=292, IN=63,
OUT=229; per family A 16/56, B 18/55, C 19/53, D 10/65.

Labelling is objective and outcome-independent: an item is IN iff its concrete id matches the
family's declared inner pattern, else OUT. HTTP-on-OUT is defined as: the runner issued a real
HTTP request whose path the oracle did not declare success for.

## 4. Arms and controls

**Treatment.**
- `T-WIDENED-PRINCIPLED` — the carrier with the frozen principled widening rule
  (`widen_support`, Section 5).

**Baselines (strong).**
- `B-SHIPPED` — the shipped carrier's own induced support, unchanged.
- `B-DECLARED-FULL` — the oracle-declared full pattern per family (ceiling; must be safe+complete,
  `M-COVERAGE=1.0`, `M-FALSE-ACCEPT-COUNT=0`).
- `B-LITERAL-KERNEL` — the literal pre-promotion kernel blob; must be unable to bind (`UNKNOWN`),
  or at minimum must not silently resolve.

**Positive controls (must be *sensitive* / must fail).**
- `PC-UNSAFE-COARSE` (`__COARSE__`) — over-broad; must accept ≥1 OUT (expected
  `M-CONTROL-PC-COARSE-FALSE-ACCEPT-COUNT=153`).
- `PC-OVERWIDE-OPEN` (unrestricted open width) — must accept ≥1 OUT (expected 33).
- `PC-DETERMINISM-REPEAT` — rerun of `B-SHIPPED`; byte-identical (sensitivity anchor).

**Null control.**
- `NC-REJECT-ALL` — refuse every item; must have `accept=0`, `http=0`, `coverage=0`.

**Validity anchor.**
- `PC-EXACT-REPLAY` — does the runner reproduce the parent's shipped numbers on the parent
  bank (n=78: 19 IN / 59 OUT, shipping fp=0, fr=9, coverage 0.5263157894736842)? Must PASS
  before any outcome is interpreted.

## 5. Frozen widening rule

The *only* decision rule under test is `widen_support` (canonical definition: FROZEN RUNNER,
Section 14). It is a read-only overlay: `src/spider/kernel.py` is left byte-identical, and the
runner overrides only `verification_rule.parameter_supports`. By V12 (Section 11) this is
support-descriptor-equivalent to re-running `distill_parameterized` with `_infer_support`
replaced by `widen_support`, because `mechanism_id` is support-independent.

Informally: take the observed values, split on the fixed `id_prefix`, find the common structure
of the remaining id token, and replace the *observed uniform width* with the smallest width
range consistent with the observed grammar — the same width for uniform-width families, and an
open equivalent width range for variable-width families, while leaving a pinned subrange
untouched. On `FAM-D` the observed width (3) is already the observed width, so the rule emits
`^region\-[0-9]{3}$`, which is the predicted falsifier.

## 6. Oracle

The runner starts a stdlib `ThreadingHTTPServer` bound to `127.0.0.1:0` (ephemeral port) with a
request counter. For each family it declares `VALID_PATH_RES[fam]`
(`^/api/<resource>s/<declared inner>$`) mapping to HTTP 200; any other path is 404. Every HTTP
value is a real request; a non-success response for an OUT item is counted as an
HTTP-on-OUT violation. No network egress beyond loopback is used.

## 7. Metrics (stable ids)

Primary:
- `M-T-WIDENED-FALSE-ACCEPT-COUNT` — OUT items whose value was bound (resolved) by
  `T-WIDENED-PRINCIPLED`.
- `M-T-WIDENED-SILENT-FALSE-ACCEPT-COUNT` — bound OUT items that were not executed
  (`refusal_executed` distinctions live in `M-T-WIDENED-REFUSAL-EXECUTED-COUNT`).
- `M-T-WIDENED-HTTP-ON-OUT` — bound+executed OUT items for which the oracle returned
  non-success.
- `M-T-WIDENED-FALSE-REJECT-COUNT` — IN items not bound.
- `M-T-WIDENED-COVERAGE` — IN bound / IN total; plus `M-T-WIDENED-COVERAGE-BY-FAMILY`.
- `M-T-WIDENED-REFUSAL-EXECUTED-COUNT` — refuse-path items that were nonetheless executed.

Secondary / comparison:
- `M-B-SHIPPED-COVERAGE` (expected 0.5079 on the four-family bank),
  `M-COVERAGE-DELTA` = `M-T-WIDENED-COVERAGE` − `M-B-SHIPPED-COVERAGE`.
- `M-WIDENED-SUPPORT-BY-FAMILY`, `M-SHIPPED-SUPPORT-BY-FAMILY` — emitted regex strings.
- `M-B-DECLARED-FULL-*`, `M-CONTROL-PC-COARSE-*`, `M-CONTROL-PC-OVERWIDE-*`,
  `M-CONTROL-NC-REJECT-ALL-*`.
- `M-REFUSAL-SEMANTICS-VIOLATIONS` — items refused but executed, or vice versa.
- `M-EXTERNAL-REPEAT-BYTE-IDENTICAL` — determinism.

Identity:
- `M-BANK` (n=292, IN=63, OUT=229, all rows unique), `M-IDENTITY` (experiment/lane identity),
  `M-SUPPORT-IDENTITY` (shipped support string == canonical shipped regex).

## 8. Decision rule

Precedence: `MEASUREMENT_INVALID` > `FALSIFIES` > (`SUPPORTS` | `MIXED`).

- **MEASUREMENT_INVALID** if `V8-FREEZE-BINDING` fails, `PC-EXACT-REPLAY` fails,
  `M-BANK` composition deviates, `M-IDENTITY`/`M-SUPPORT-IDENTITY` fail, or the bank/runner
  cannot be instantiated. (Infrastructure/validity failure ≠ negative result.)
- **FALSIFIES** (decision `WIDENING_UNSAFE`) if
  `M-T-WIDENED-FALSE-ACCEPT-COUNT > 0` OR `M-T-WIDENED-HTTP-ON-OUT > 0` OR
  `M-T-WIDENED-REFUSAL-EXECUTED-COUNT > 0`. **DESIGN prediction: FALSIFIES**, driven by
  `FAM-D` (expected 9 false accepts, all `FD-OG-WRONGRANGE00..08`).
- **SUPPORTS** (decision `WIDENING_SAFE_AND_COMPLETE`) if all safety conditions hold AND
  `M-T-WIDENED-COVERAGE == 1.0`.
- **MIXED** (decision `WIDENING_SAFE_BUT_INCOMPLETE`) if safe but coverage < 1.0.
- `INCONCLUSIVE` only if none of the above can be decided while measurement is still valid.

**Claim-status semantics (no self-promotion):** `C-PARAM-INHERIT` remains `EXPERIMENTAL` and
`C-SEMANTIC-RESOLVE` remains `HYPOTHESIS` in **all** branches. This experiment produces evidence
only; it does not advance, promote or ship any claim.

## 9. Reachability and DESIGN probes (non-outcome only)

Performed during DESIGN, none outcome-bearing (no treatment `resolve()` over the frozen bank):

- **D1 arithmetic/reachability:** the bank is constructible (n=292, 63 IN, 229 OUT, unique
  ids); each family has train≥5 and at least one OUT; no empty/unreachable branch.
- **D2 identity:** `B-SHIPPED` support equals the canonical shipped regex on all four families;
  `B-DECLARED-FULL` == declared patterns → safe+complete reachable (ceiling baseline is not
  0/1-degenerate).
- **D3 treatment liveness:** all 25 training values (A/B/C 5 each, D 10) are EXECUTABLE; the
  carrier induces a single bound slot with confidence 0.9 (≥ `min_confidence` 0.8) for all four
  families. A treatment that never bound would make the test vacuous.
- **D4 control sensitivity:** `PC-UNSAFE-COARSE` accepts OUT, `PC-OVERWIDE-OPEN` accepts OUT,
  `NC-REJECT-ALL` accepts nothing → controls are sensitive, not dead.
- **D5 treatment/comparator identity:** the only difference between `T-WIDENED-PRINCIPLED` and
  `B-SHIPPED` is the widening rule; same carrier, same bank, same oracle.
- **D6 satisfiability:** the FALSIFIES branch is concretely reachable via `FAM-D`; the
  SUPPORTS/MIXED branches are reachable via the other families; no arithmetic impossibility.

A plumbing smoke test of the runner's non-outcome paths passed (it caught a `Path / "%s"`
precedence bug before freeze, now fixed), and `py_compile` succeeds.

## 10. Freeze eligibility (v2, six checks)

| check | status | basis |
|---|---|---|
| `decision_rule_reachability` | PASS | D1/D6: all four branches reachable, no degenerate bank. |
| `measurement_prerequisites` | PASS | `src/spider/kernel.py` + models + registry present and hash-pinned; loopback oracle available; stdlib only. |
| `baseline_identifiability` | PASS | D2: `B-SHIPPED`, `B-DECLARED-FULL`, `B-LITERAL-KERNEL` distinct and identifiable. |
| `control_sensitivity` | PASS | D4: both positive controls fail as designed; null accepts nothing. |
| `treatment_liveness` | PASS | D3: 25/25 training values EXECUTABLE; confidence 0.9. |
| `freeze_artifacts_bound` | PASS | six immutable files listed below; no mutable local code/data/task-bank/fixture dependency outside the frozen runner. |

`freeze_artifacts` (all existing, non-empty): `pyproject.toml`, `src/spider/__init__.py`,
`src/spider/models.py`, `src/spider/registry.py`, `src/spider/kernel.py`,
`tests/test_kernel.py`. There is **no** local mutable task bank or fixture: the bank is
generated deterministically inside the frozen runner from the declared patterns, and all
treatment/control logic is inside the runner.

## 11. Binding model

- `EXPECTED_MIN_CONFIDENCE = 0.8` (kernel default; all four families induce 0.9).
- V8 freeze binding (checked by EXECUTE):
  1. `sha256(prereg.md) == freeze.json.hashes["prereg.md"]`;
  2. `norm(prereg.md source) == norm(FROZEN RUNNER block)` where
     `norm(s) = s.replace("\r\n", "\n").rstrip()`;
  3. `sha256(file) == freeze.json.artifact_hashes[file]` for every listed artifact.
- V12 equivalence (justifies read-only overlay): `mechanism_id` is support-independent, so
  overriding `verification_rule.parameter_supports` is equivalent to re-running
  `distill_parameterized` with `_infer_support` replaced by `widen_support`.
- Probe mode: `EXP_PROBE_MODE=1` records `UNBOUND-RUN` when `freeze.json` is absent;
  `EXP_TARGET_ROOT` sets the repo root.
- EXECUTE materializes `harness/run_bank.py` from the FROZEN RUNNER block below (byte-for-byte
  after `norm`).

## 12. Canonical hashes

| artifact | sha256 |
|---|---|
| `pyproject.toml` | `5f03fb5914f388c19973831287cce6773c7364e1bea856a595cd7247d3115b83` |
| `src/spider/__init__.py` | `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77` |
| `src/spider/models.py` | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` |
| `src/spider/registry.py` | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` |
| `src/spider/kernel.py` | `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` |
| `tests/test_kernel.py` | `ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6` |

FROZEN RUNNER block (normalized) sha256:
`ab2211cc163b31901517124ca56620e4dab4de03422de534c3b721e611aefbcf` (un-normalized file sha256 `5e193d8523f4b431375b6027542a63b863775e735f367019f1d35124ae367093`). These are DESIGN
references; the binding hashes are established by `freeze.json` at freeze time.

## 13. Cost and scope limits

- Stdlib only; loopback HTTP; no LLM calls; no network egress.
- EXECUTE scope: prefix `research/experiments/EXP-PRODUCT-38197856050` plus lane
  `allowed_code_roots`. DESIGN writes only `spec.json` and `prereg.md`.
- Estimated cost: small (single deterministic pass; ~292 oracle requests).

## 14. FROZEN RUNNER

Materialization source for `harness/run_bank.py`. The block below is verbatim; EXECUTE must
reproduce it exactly (V8 binding).
<!-- BEGIN FROZEN RUNNER -->
#!/usr/bin/env python3
"""FROZEN RUNNER for EXP-PRODUCT-38197856050 (embedded verbatim in prereg.md).

Read-only PRINCIPLED-SUPPORT-WIDENING safety/coverage certificate for the
as-installed parameterized carrier (src/spider/kernel.py, git blob b15ed848... /
sha256 718efa6a...).  NEVER writes src/spider/ and never calls a model.

Arms (stable ids):
  T-WIDENED-PRINCIPLED  the same carrier mechanisms with each induced support
                        replaced by the frozen data-driven widening rule
                        widen_support(observed segment values) (TREATMENT)
  B-SHIPPED             the unmodified induced supports (shipped baseline)
  B-DECLARED-FULL       support replaced by the DECLARED grammar per family
                        (strong upper-bound comparator: safe+complete exists)
  PC-UNSAFE-COARSE      support replaced by the carrier's own __COARSE__ sentinel
  PC-OVERWIDE-OPEN      support replaced by ^<id_prefix>\\-[0-9]+$ (open width)
  NC-REJECT-ALL         empty registry (null floor)
  B-LITERAL-KERNEL      pre-promotion literal kernel (lacks distill_parameterized)
  PC-EXACT-REPLAY       5 training ids per family re-resolve EXECUTABLE
  ORACLE-SERVER         localhost oracle: 200 iff path matches the family's
                        declared grammar, else 404

Families (declared identifier grammars):
  A item   /api/items/item-[0-9]{3}     train item-001..005   (uniform width)
  B account/api/accounts/acct-[0-9]{4}  train acct-0001..0005 (uniform width)
  C doc    /api/docs/doc-[0-9]{1,4}     train doc-01..05      (variable width)
  D region /api/regions/region-00[0-9]  train region-000..009 (pinned subrange)

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
EXPERIMENT_ID = "EXP-PRODUCT-38197856050"
EXP_DIR = "research/experiments/EXP-PRODUCT-38197856050"
EXPECTED_MIN_CONFIDENCE = 0.8
COARSE = "__COARSE__"

# Declared grammars + frozen training samples (the ONLY values the widening rule
# may see).  slot == resource because the carrier derives the parameter slot name
# from the plural URL segment (trailing "s" stripped).
FAMILIES = [
    {"fam": "A", "intent": "read_item", "resource": "item", "id_prefix": "item",
     "declared": r"^item\-[0-9]{3}$",
     "train": ["item-001", "item-002", "item-003", "item-004", "item-005"],
     "in_extra": ["item-000", "item-006", "item-007", "item-010", "item-042",
                  "item-099", "item-100", "item-123", "item-256", "item-500", "item-999"],
     "out_wrong_subrange": []},
    {"fam": "B", "intent": "read_account", "resource": "account", "id_prefix": "acct",
     "declared": r"^acct\-[0-9]{4}$",
     "train": ["acct-0001", "acct-0002", "acct-0003", "acct-0004", "acct-0005"],
     "in_extra": ["acct-0006", "acct-0007", "acct-0010", "acct-0042", "acct-0099",
                  "acct-0100", "acct-0123", "acct-0256", "acct-0500", "acct-0999",
                  "acct-1000", "acct-9999"],
     "out_wrong_subrange": []},
    {"fam": "C", "intent": "read_doc", "resource": "doc", "id_prefix": "doc",
     "declared": r"^doc\-[0-9]{1,4}$",
     "train": ["doc-01", "doc-02", "doc-03", "doc-04", "doc-05"],
     "in_extra": ["doc-0", "doc-1", "doc-9", "doc-10", "doc-11", "doc-99",
                  "doc-100", "doc-123", "doc-999", "doc-1000", "doc-9999"],
     "out_wrong_subrange": []},
    {"fam": "D", "intent": "read_region", "resource": "region", "id_prefix": "region",
     "declared": r"^region\-00[0-9]$",
     "train": ["region-000", "region-001", "region-002", "region-003", "region-004",
               "region-005", "region-006", "region-007", "region-008", "region-009"],
     "in_extra": [],
     "out_wrong_subrange": ["region-010", "region-011", "region-042", "region-099",
                            "region-100", "region-123", "region-256", "region-500",
                            "region-999"]},
]
FAM_BY_ID = {f["fam"]: f for f in FAMILIES}
EXPECTED_SHIPPED = {
    "A": r"^item\-00[0-9]{1}$", "B": r"^acct\-000[0-9]{1}$",
    "C": r"^doc\-0[0-9]{1}$", "D": r"^region\-00[0-9]{1}$",
}
EXPECTED_WIDENED = {
    "A": r"^item\-[0-9]{3}$", "B": r"^acct\-[0-9]{4}$",
    "C": r"^doc\-[0-9]{2}$", "D": r"^region\-[0-9]{3}$",
}

PAYLOAD_CLASSES = [
    ("LEN-TOO-SHORT1", lambda p, v: p + "-0"),
    ("LEN-TOO-SHORT2", lambda p, v: p + "-00"),
    ("LEN-TOO-LONG1", lambda p, v: p + "-" + "0" * 4),
    ("LEN-TOO-LONG2", lambda p, v: p + "-" + "0" * 5),
    ("LEN-TOO-LONG3", lambda p, v: p + "-" + "0" * 6),
    ("ALPHA-TAIL", lambda p, v: p + "-00a"),
    ("ALPHA-ALL", lambda p, v: p + "-abc"),
    ("ALPHA-HEAD", lambda p, v: p + "-a00"),
    ("HEX", lambda p, v: p + "-0x1"),
    ("CASE-UP", lambda p, v: p.upper() + "-000"),
    ("CASE-TITLE", lambda p, v: p.capitalize() + "-000"),
    ("SEP-US", lambda p, v: p + "_000"),
    ("SEP-DOT", lambda p, v: p + ".000"),
    ("SEP-COLON", lambda p, v: p + ":000"),
    ("SEP-SLASH", lambda p, v: p + "/000"),
    ("WS-EMPTY", lambda p, v: ""),
    ("WS-SPACE", lambda p, v: " "),
    ("WS-TAB", lambda p, v: "\t"),
    ("WS-NL", lambda p, v: "\n"),
    ("WS-TRAIL", lambda p, v: v + " "),
    ("WS-LEAD", lambda p, v: " " + v),
    ("INJ-SEMI", lambda p, v: v + ";x"),
    ("INJ-SQ", lambda p, v: v + "'"),
    ("INJ-DQ", lambda p, v: v + '"'),
    ("INJ-NUL", lambda p, v: v + "\x00"),
    ("INJ-TRAV", lambda p, v: "../../etc/passwd"),
    ("INJ-ABS", lambda p, v: "/api/" + p + "s/" + v),
    ("INJ-URL", lambda p, v: "http://evil.example/" + v),
    ("INJ-DOTDOT", lambda p, v: v + "/../secret"),
    ("QRY", lambda p, v: v + "?x=1"),
    ("FRAG", lambda p, v: v + "#frag"),
    ("PCT", lambda p, v: v.replace("0", "%30", 1)),
    ("UNI-AR", lambda p, v: p + "-00\u0663"),
    ("UNI-FW", lambda p, v: p + "-00\uff10"),
    ("OTH-USER", lambda p, v: "user-000"),
    ("OTH-ORDER", lambda p, v: "order-000"),
    ("OTH-CAT", lambda p, v: p + "x000"),
    ("BIG-1000", lambda p, v: p + "-" + "0" * 1000),
    ("BIG-64", lambda p, v: p + "-" + "9" * 64),
]
TYPE_PAYLOADS = [None, 0, 0.0, True, False, [], ["X"], {}, {"id": "X"}, b"X"]


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


# ------------------------------------------------- frozen widening inference
def _char_class(chars):
    digits = set("0123456789")
    lower = set("abcdefghijklmnopqrstuvwxyz")
    upper = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if chars and chars <= digits:
        return "0-9"
    if chars and chars <= lower:
        return "a-z"
    if chars and chars <= upper:
        return "A-Z"
    if chars and chars <= (lower | upper):
        return "a-zA-Z"
    if chars and chars <= (lower | digits):
        return "a-z0-9"
    if chars and chars <= (lower | upper | digits):
        return "a-zA-Z0-9"
    return None


def _common_prefix(values):
    if not values:
        return ""
    prefix = values[0]
    for value in values[1:]:
        limit = min(len(prefix), len(value))
        i = 0
        while i < limit and prefix[i] == value[i]:
            i += 1
        prefix = prefix[:i]
    return prefix


def widen_support(values) -> str:
    """Frozen data-driven widening rule (the TREATMENT hypothesis).

    Absorb the maximal trailing run of the common prefix whose characters lie in
    the SAME minimal character class as the observed varying remainder, then keep
    the observed uniform width (or '+' when widths differ).  Pure function of the
    observed values; it NEVER consults the declared grammar.  Falls back to the
    shipped greedy-prefix inference when the observed structure is not a single
    homogeneous class.
    """
    values = [str(v) for v in values]
    if not values:
        return COARSE
    prefix = _common_prefix(values)
    remains = [v[len(prefix):] for v in values]
    klass = _char_class(set("".join(remains)))
    if klass is None:
        return _shipped_infer(values)
    k = len(prefix)
    while k > 0 and _char_class({prefix[k - 1]}) == klass:
        k -= 1
    new_prefix = prefix[:k]
    new_remains = [v[len(new_prefix):] for v in values]
    new_klass = _char_class(set("".join(new_remains)))
    if new_klass is None:
        return _shipped_infer(values)
    lengths = {len(r) for r in new_remains}
    quant = "{%d}" % next(iter(lengths)) if len(lengths) == 1 else "+"
    return "^" + re.escape(new_prefix) + "[" + new_klass + "]" + quant + "$"


def _shipped_infer(values) -> str:
    """Verbatim copy of src/spider/kernel.py::_infer_support (frozen reference)."""
    values = [str(v) for v in values]
    if not values:
        return COARSE
    prefix = _common_prefix(values)
    remains = [v[len(prefix):] for v in values]
    klass = _char_class(set("".join(remains)))
    if klass is None:
        return COARSE
    lengths = {len(r) for r in remains}
    quantifier = "{%d}" % next(iter(lengths)) if len(lengths) == 1 else "+"
    return "^" + re.escape(prefix) + "[" + klass + "]" + quantifier + "$"


# ---------------------------------------------------------------- frozen bank
def build_bank():
    bank = []
    for f in FAMILIES:
        ctx = {"resource_type": f["resource"], "authenticated": True}
        slot = f["resource"]
        v0 = f["train"][0]

        def add(bid, value, intent=None, context=None, params=None, _f=f, _slot=slot):
            bank.append({"bid": bid, "fam": _f["fam"], "value": value,
                         "intent": _f["intent"] if intent is None else intent,
                         "context": dict(ctx) if context is None else context,
                         "params": dict(params) if params is not None else {_slot: value}})

        for i, v in enumerate(f["in_extra"]):
            add("F%s-IN-E%02d" % (f["fam"], i), v)
        for i, v in enumerate(f["train"]):
            add("F%s-IN-T%02d" % (f["fam"], i), v)
        for name, fn in PAYLOAD_CLASSES:
            val = fn(f["id_prefix"], v0)
            add("F%s-OG-%s" % (f["fam"], name), val)
        for i, wv in enumerate(f["out_wrong_subrange"]):
            add("F%s-OG-WRONGRANGE%02d" % (f["fam"], i), wv)
        for i, val in enumerate(TYPE_PAYLOADS):
            add("F%s-OG-TYPE%02d" % (f["fam"], i), val)
        vv = f["train"][1]
        add("F%s-OG-CTX-USERTYPE" % f["fam"], vv, context={"resource_type": "other",
                                                          "authenticated": True})
        add("F%s-OG-CTX-NOAUTH" % f["fam"], vv,
            context={"resource_type": f["resource"], "authenticated": False})
        add("F%s-OG-CTX-MISSING" % f["fam"], vv,
            context={"resource_type": f["resource"]})
        add("F%s-OG-CTX-EMPTY" % f["fam"], vv, context={})
        add("F%s-OG-CTX-INTENT" % f["fam"], vv, intent="delete_" + f["resource"])
        add("F%s-OG-CTX-WRONGKEY" % f["fam"], vv, params={"wrong_key": vv})
        add("F%s-OG-CTX-NOPARAM" % f["fam"], vv, params={})
    return bank


def label_of(item):
    f = FAM_BY_ID[item["fam"]]
    v = item["value"]
    if not isinstance(v, str):
        return "OUT"
    if re.fullmatch(f["declared"], v) is None:
        return "OUT"
    if item["intent"] != f["intent"]:
        return "OUT"
    if item["context"] != {"resource_type": f["resource"], "authenticated": True}:
        return "OUT"
    if item["params"] != {f["resource"]: v}:
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
def _path_re(f):
    return re.compile("^/api/" + f["resource"] + "s/" + f["declared"][1:-1] + "$")


VALID_PATH_RES = {f["fam"]: _path_re(f) for f in FAMILIES}


class OracleHandler(http.server.BaseHTTPRequestHandler):
    count = 0

    def do_GET(self):
        type(self).count += 1
        path = self.path.split("?", 1)[0]
        matched = next((fam for fam, rx in VALID_PATH_RES.items()
                        if rx.fullmatch(path)), None)
        if matched is not None:
            ident = path.rsplit("/", 1)[-1]
            body = {"type": FAM_BY_ID[matched]["resource"], "id": ident,
                    "data": "res:" + ident}
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


def make_arm_registry(mechs, support_by_fam, tmpdir, tag):
    reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry
    reg = reg_cls(Path(tmpdir) / ("mechanisms_%s.jsonl" % tag))
    for fam in ("A", "B", "C", "D"):
        m = copy.deepcopy(mechs[fam])
        if support_by_fam is not None:
            m.verification_rule = {"parameter_supports": {
                s: support_by_fam[fam] for s in m.parameter_slots}}
        reg.upsert(m)
    return reg


def evaluate(kernel, bank, handler):
    records = []
    for item in bank:
        http0 = handler.count
        rec = {"bid": item["bid"], "fam": item["fam"], "cls": item.get("cls", ""),
               "label": label_of(item), "value": value_repr(item["value"])}
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


def _summarize(records):
    n_in = sum(1 for r in records if r["label"] == "IN")
    n_out = sum(1 for r in records if r["label"] == "OUT")
    accepts = [r for r in records if r["status"] == "EXECUTABLE"]
    fa = [r for r in records if r["label"] == "OUT" and r["status"] == "EXECUTABLE"]
    sfa = [r for r in fa if r["exec_status"] == 200 and r["verify"] is True]
    fr = [r for r in records if r["label"] == "IN" and r["status"] != "EXECUTABLE"]
    http_out = sum(r["http_delta"] for r in records if r["label"] == "OUT")
    http_total = sum(r["http_delta"] for r in records)
    refusal_exec = sum(1 for r in records
                       if r["label"] == "OUT" and r["status"] != "EXECUTABLE"
                       and r["http_delta"] > 0)
    cov = (n_in - len(fr)) / n_in if n_in else None
    return {
        "n_in": n_in, "n_out": n_out, "accept_count": len(accepts),
        "false_accept_count": len(fa), "silent_false_accept_count": len(sfa),
        "false_reject_count": len(fr), "coverage": cov,
        "http_on_out_label": http_out, "http_total": http_total,
        "refusal_executed_count": refusal_exec,
        "false_accept_bids": [r["bid"] for r in fa],
        "silent_false_accept_bids": [r["bid"] for r in sfa],
        "false_reject_bids": [r["bid"] for r in fr],
    }


def summarize(records):
    out = _summarize(records)
    out["per_family"] = {}
    for fam in ("A", "B", "C", "D"):
        sub = [r for r in records if r["fam"] == fam]
        out["per_family"][fam] = _summarize(sub)
    return out


# --------------------------------------------------------------- V8 freeze bind
def _extract(text, name):
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END "
                  + re.escape(name) + r" -->", text, re.S)
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
def run_once(carrier_cls, counters_cls, reg_cls, obs_cls):
    server, port, handler = start_oracle()
    try:
        tmp = tempfile.mkdtemp(prefix="exp38197856050_")
        reg_cls(Path(tmp) / "base.jsonl")  # touch registry dir
        mechs = {}
        identity = {}
        for f in FAMILIES:
            obs = []
            for ident in f["train"]:
                url = "http://127.0.0.1:%d/api/%ss/%s" % (port, f["resource"], ident)
                st, body = execute_action({"url": url})
                if st != 200:
                    raise RuntimeError("induction GET %s -> %s" % (ident, st))
                obs.append(obs_cls(intent=f["intent"],
                                   state={"resource_type": f["resource"], "authenticated": True},
                                   action={"method": "GET", "url": url},
                                   next_state=body, success=True,
                                   provenance={"exp": EXPERIMENT_ID, "role": "induction"}))
            reg = reg_cls(Path(tmp) / ("base_%s.jsonl" % f["fam"]))
            kernel = carrier_cls(reg, counters=counters_cls())
            m = kernel.distill_parameterized(obs)
            if m is None:
                raise RuntimeError("distill_parameterized returned None for fam " + f["fam"])
            reg.upsert(m)
            mechs[f["fam"]] = m
            identity[f["fam"]] = {
                "slots": list(m.parameter_slots),
                "support": m.verification_rule["parameter_supports"],
                "confidence": m.confidence,
            }

        bank = build_bank()
        ids = [b["bid"] for b in bank]
        if len(ids) != len(set(ids)):
            raise RuntimeError("duplicate bank bids")

        shipped = {fam: mechs[fam].verification_rule["parameter_supports"][FAM_BY_ID[fam]["resource"]]
                   for fam in ("A", "B", "C", "D")}
        for fam in ("A", "B", "C", "D"):
            if shipped[fam] != EXPECTED_SHIPPED[fam]:
                raise RuntimeError("shipped support drift fam %s: %s" % (fam, shipped[fam]))
        widened = {fam: widen_support(FAM_BY_ID[fam]["train"]) for fam in ("A", "B", "C", "D")}
        for fam in ("A", "B", "C", "D"):
            if widened[fam] != EXPECTED_WIDENED[fam]:
                raise RuntimeError("widened support drift fam %s: %s" % (fam, widened[fam]))
        declared = {fam: FAM_BY_ID[fam]["declared"] for fam in ("A", "B", "C", "D")}
        openwide = {fam: "^" + re.escape(FAM_BY_ID[fam]["id_prefix"]) + r"\-[0-9]+$"
                    for fam in ("A", "B", "C", "D")}
        coarse = {fam: COARSE for fam in ("A", "B", "C", "D")}

        def arm(support_by_fam, tag):
            reg = make_arm_registry(mechs, support_by_fam, tmp, tag)
            k = carrier_cls(reg, counters=counters_cls())
            for item in bank:
                item["_mech_id"] = mechs[item["fam"]].mechanism_id
            return evaluate(k, bank, handler)

        treat_recs = arm(widened, "treatment")
        shipped_recs = arm(None, "shipped")
        declared_recs = arm(declared, "declared")
        coarse_recs = arm(coarse, "coarse")
        open_recs = arm(openwide, "open")
        empty_reg = reg_cls(Path(tmp) / "reg_empty.jsonl")
        empty_recs = evaluate(carrier_cls(empty_reg, counters=counters_cls()), bank, handler)

        replay = []
        for f in FAMILIES:
            for ident in f["train"]:
                r = carrier_cls(reg_cls(Path(tmp) / ("base_%s.jsonl" % f["fam"])),
                                counters=counters_cls()).resolve(
                    f["intent"], {"resource_type": f["resource"], "authenticated": True},
                    {f["resource"]: ident})
                replay.append({"fam": f["fam"], "id": ident, "status": r.status.value})

        return {
            "mechanism_identity": identity,
            "shipped_support": shipped,
            "widened_support": widened,
            "treatment": summarize(treat_recs),
            "shipped": summarize(shipped_recs),
            "comparator_declared": summarize(declared_recs),
            "control_coarse": summarize(coarse_recs),
            "control_open": summarize(open_recs),
            "null_reject_all": summarize(empty_recs),
            "pc_exact_replay": {"status": "PASS" if all(x["status"] == "EXECUTABLE"
                                                        for x in replay) else "FAIL",
                                "replay": replay},
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

    run1 = run_once(Carrier, counters_cls, reg_cls, obs_cls)
    run2 = run_once(Carrier, counters_cls, reg_cls, obs_cls)
    det = (json.dumps(run1["treatment"], sort_keys=True) == json.dumps(run2["treatment"], sort_keys=True)
           and json.dumps(run1["shipped"], sort_keys=True) == json.dumps(run2["shipped"], sort_keys=True)
           and json.dumps(run1["comparator_declared"], sort_keys=True)
           == json.dumps(run2["comparator_declared"], sort_keys=True)
           and run1["mechanism_identity"] == run2["mechanism_identity"]
           and run1["widened_support"] == run2["widened_support"])
    result["certificate"]["PC-DETERMINISM-REPEAT"] = {
        "status": "PASS" if det else "FAIL",
        "reason": "two independent runs produce identical treatment/shipped/declared metrics "
                  "and support identity"}

    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test_*.py")
    tr = unittest.TextTestRunner(verbosity=0).run(suite)
    result["certificate"]["M-REGRESSION"] = {
        "status": "PASS" if (tr.wasSuccessful() and tr.testsRun >= 3) else "FAIL",
        "tests_run": tr.testsRun, "failures": len(tr.failures), "errors": len(tr.errors)}

    t = run1["treatment"]
    s = run1["shipped"]
    dd = run1["comparator_declared"]
    result["certificate"]["M-SUPPORT-IDENTITY"] = {
        "status": "PASS" if (run1["shipped_support"] == EXPECTED_SHIPPED
                             and run1["widened_support"] == EXPECTED_WIDENED) else "FAIL",
        "shipped": run1["shipped_support"], "widened": run1["widened_support"],
        "reason": "induced shipped supports and frozen widened supports match the DESIGN constants"}

    result["certificate"]["T-WIDENED-PRINCIPLED"] = {
        "status": "PASS",
        "false_accept_count": t["false_accept_count"],
        "silent_false_accept_count": t["silent_false_accept_count"],
        "false_reject_count": t["false_reject_count"],
        "coverage": t["coverage"],
        "http_on_out_label": t["http_on_out_label"],
        "refusal_executed_count": t["refusal_executed_count"],
        "false_accept_bids": t["false_accept_bids"],
        "false_reject_bids": t["false_reject_bids"],
        "per_family": t["per_family"],
        "reason": "principled data-driven widening; safety iff false_accept_count==0 and "
                  "http_on_out_label==0; completeness iff coverage==1.0"}
    result["certificate"]["B-SHIPPED"] = {
        "status": "PASS" if s["false_accept_count"] == 0 else "FAIL",
        "false_accept_count": s["false_accept_count"], "false_reject_count": s["false_reject_count"],
        "coverage": s["coverage"], "http_on_out_label": s["http_on_out_label"],
        "per_family": s["per_family"], "reason": "shipped single-observation-length supports"}
    result["certificate"]["B-DECLARED-FULL"] = {
        "status": "PASS" if (dd["false_accept_count"] == 0 and dd["coverage"] == 1.0) else "FAIL",
        "false_accept_count": dd["false_accept_count"], "coverage": dd["coverage"],
        "per_family": dd["per_family"],
        "reason": "strong comparator: declared-grammar supports are safe+complete on the bank "
                  "(upper bound; not a shipped change)"}
    result["certificate"]["PC-UNSAFE-COARSE"] = {
        "status": "PASS" if run1["control_coarse"]["false_accept_count"] >= 1 else "FAIL",
        "false_accept_count": run1["control_coarse"]["false_accept_count"],
        "reason": "positive control: the carrier's own __COARSE__ fallback must over-accept"}
    result["certificate"]["PC-OVERWIDE-OPEN"] = {
        "status": "PASS" if run1["control_open"]["false_accept_count"] >= 1 else "FAIL",
        "false_accept_count": run1["control_open"]["false_accept_count"],
        "reason": "positive control: an open-width [0-9]+ support must over-accept wrong-width ids"}
    result["certificate"]["NC-REJECT-ALL"] = {
        "status": "PASS" if (run1["null_reject_all"]["accept_count"] == 0
                             and run1["null_reject_all"]["http_total"] == 0) else "FAIL",
        "accept_count": run1["null_reject_all"]["accept_count"],
        "http_total": run1["null_reject_all"]["http_total"],
        "reason": "null floor: empty registry accepts nothing and issues no HTTP"}
    result["certificate"]["PC-EXACT-REPLAY"] = run1["pc_exact_replay"]

    result["arms"] = {
        "T-WIDENED-PRINCIPLED": run1["treatment"],
        "B-SHIPPED": run1["shipped"],
        "B-DECLARED-FULL": run1["comparator_declared"],
        "PC-UNSAFE-COARSE": run1["control_coarse"],
        "PC-OVERWIDE-OPEN": run1["control_open"],
        "NC-REJECT-ALL": run1["null_reject_all"],
    }
    result["mechanism_identity"] = run1["mechanism_identity"]
    result["bank"] = {"n_items": len(build_bank()), "n_in": t["n_in"], "n_out": t["n_out"],
                      "per_family_n_in": {f: t["per_family"][f]["n_in"] for f in "ABCD"},
                      "per_family_n_out": {f: t["per_family"][f]["n_out"] for f in "ABCD"}}

    validity_gates = ("V8_FREEZE_BINDING", "M-IDENTITY", "M-REGRESSION",
                      "PC-DETERMINISM-REPEAT", "PC-EXACT-REPLAY", "B-LITERAL-KERNEL",
                      "M-SUPPORT-IDENTITY")
    validity = all(result["certificate"][k]["status"] == "PASS" for k in validity_gates)
    failed_validity = [k for k in validity_gates if result["certificate"][k]["status"] != "PASS"]
    sensitivity = (result["certificate"]["PC-UNSAFE-COARSE"]["status"] == "PASS"
                   and result["certificate"]["PC-OVERWIDE-OPEN"]["status"] == "PASS"
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
    http_out = t["http_on_out_label"]
    refexec = t["refusal_executed_count"]
    if fa > 0 or http_out > 0 or refexec > 0:
        unsafe = sorted(fam for fam in "ABCD" if t["per_family"][fam]["false_accept_count"] > 0
                        or t["per_family"][fam]["http_on_out_label"] > 0)
        result["status"], result["outcome"] = "COMPLETE", "FALSIFIES"
        result["decision"] = "WIDENING_UNSAFE"
        result["reason"] = ("principled widening bound %d out-of-grammar payload(s) "
                            "(silent=%d) and issued HTTP on out-of-grammar=%d (refusal-executed=%d); "
                            "unsafe families=%s; the safe-support widening must not be adopted "
                            "without an independent grammar/applicability guard"
                            % (fa, t["silent_false_accept_count"], http_out, refexec, unsafe))
    elif t["coverage"] == 1.0:
        result["status"], result["outcome"] = "COMPLETE", "SUPPORTS"
        result["decision"] = "WIDENING_SAFE_AND_COMPLETE"
        result["reason"] = ("zero false accepts and full coverage across all families: the "
                            "principled widening is safe and complete on the bank")
    else:
        result["status"], result["outcome"] = "COMPLETE", "MIXED"
        result["decision"] = "WIDENING_SAFE_BUT_INCOMPLETE"
        result["reason"] = ("zero false accepts (safe) but coverage %.4f < 1.0 (false rejects %d); "
                            "shipped coverage %.4f" % (t["coverage"], t["false_reject_count"],
                                                       s["coverage"]))
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True, default=repr))

<!-- END FROZEN RUNNER -->

