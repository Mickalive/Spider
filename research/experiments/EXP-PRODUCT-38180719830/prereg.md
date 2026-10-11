# EXP-PRODUCT-38180719830 preregistration

Lane: product. Claim: C-PARAM-INHERIT (registry status EXPERIMENTAL; owners graph+product). Design-contract version: 2.
Immutable request: `research/experiments/EXP-PRODUCT-38180719830/request.json` (request_hash `8965d12b31c409c576568d8335d90b4454f21809438c3ab78b54279c80d602aa`, base_sha `80c74f86d59ba0a483badddf7ae0e775d2a32a8f`).
Parent handoff: `research/experiments/EXP-PRODUCT-37989728440/handoff.json` (sha256 `911f765d04a83974f20d113da206b4075337c3a9bed4c5a77a8f06ffb4773ed9`), disposition **SUPERSEDE** (Director mandate governs; the inherited 'four-arm benchmark or asymmetric-discovery fallback' is NOT this packet's object).
Base SHA at design time (probe ground truth): `83b4a0ba8bbed8d4febbeef978e51041ece61da1`.

This preregistration is frozen together with `spec.json` and `request.json` by `freeze.json`. Nothing in this
file may be edited after freeze. The data blocks between the BEGIN/END markers and the runner script are part
of this file and are therefore bound by `freeze.json.hashes["prereg.md"]`; the runner re-verifies that hash at
EXECUTE (V8-A), confirms its own source equals the `FROZEN RUNNER` block (V8-B), and re-verifies the freeze
artifact hashes against `freeze.json.artifact_hashes` (V8-C). `spec.json.freeze_artifacts` lists the repository
files this experiment reads; `src/spider/kernel.py` is deliberately **not** an artifact because it is the
treatment object (section 13). The certificate bank, fixture and canonical identities are carried **inside
this file**, not as new repository files, so no new mutable dependency is created.

---

## 1. Preregistered question, hypothesis and falsifier

Binding definitions live in `spec.json` (`question`, `hypothesis`, `falsifier`). In brief:

- **Question (Director mandate, verbatim clause structure).** Can the already-audited parameterized mechanism
  carrier be installed byte-identically at the shipping kernel path `src/spider/kernel.py` with a binding
  pre-freeze positive/negative certificate: (a) positive — `distill_parameterized` over >=3 induction
  observations resolves `EXECUTABLE` with a correctly bound non-null action at confidence 0.9, then the
  deterministic fixture execute returns status 200, then `verify` returns true on an **UNSEEN** held-out
  identifier; (b) negative — refuse out-of-support / missing-parameter / wrong-intent bindings with a recorded
  reason and a null bound action, returning **exactly** `ResolutionStatus.UNKNOWN` for the
  no-applicable-mechanism case; (c) honest inherited-path counters (`retrieval_calls`, `verification_calls`,
  `repair_attempts`); (d) installed identity equal to the frozen carrier git blob
  `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` / sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` —
  such that promotion is enabled **only on independent audit PASS**, discharging blocker B1.
- **Hypothesis.** The carrier installed byte-identically at `src/spider/kernel.py` passes all five clauses
  D0-D4 with V8 enforced; the conclusive failure branch is that the certificate FAILS on a correctly installed
  carrier (or BLOCKS on an identity/binding failure), which refuses promotion and records the exact blocker.
- **Falsifier.** A valid scientific negative (status COMPLETE, outcome FALSIFIES) requires D0 PASS (carrier
  installed byte-identically) and any failure of D1-POSITIVE, D2-NEGATIVE, D3-COUNTERS or D4-CONTROLS.
  Identity/binding/infrastructure failures are MEASUREMENT_INVALID/BLOCKED — never FALSIFIES. Both branches
  change the promotion decision (mandate: certificate PASS + audit PASS -> promotion enabled; FAIL -> promotion
  refused and the flagship benchmark cannot honestly run).

## 2. Scope and out-of-scope

Measured: byte-identical installation of the audited carrier at the shipping path; positive binding certificate
(d) on an unseen held-out identifier inside the induced support; three-category refusal certificate (b) ~+
exact-UNKNOWN semantics; honest transcript-consistent counters (c); causal attribution to the installed carrier
(literal ablation); package-surface integrity (freeze artifacts + regression suite); freeze binding (V8).
**Not** measured or claimed: the four-arm C-LLM-INHERIT benchmark (COLD vs INSTRUCTIONS vs RETRIEVAL vs SPIDER),
economics/latency, any claim advance (C-PARAM-INHERIT stays EXPERIMENTAL in all branches), and any product
promotion (only a DIRECTOR verdict can grant that). The parent handoff's fourth re-run of the
mandatory-discovery deterministic REST certificate is **explicitly excluded** (see section 4).

## 3. Not a repetition of prior work

- **Pre-2.0 (LEGACY: NO_MATCH).** The Director mandate's `comparative_reasoning` states parameterization
  returns zero pre-2.0 index hits; `distill_parameterized` is a Research 2.0 object. The historically relevant
  guards are honored rather than re-run: P2-REPLAY-COST (sha `9687ff787f2d74460bb7006826008852f5b4416b`,
  `HISTORICAL_AUDITED_BOUNDED`) — matched tasks and fully loaded counterfactuals, never frame scripted replay as
  agent economics; this certificate does not claim economics. P2-BLIND-COMPOSITION (sha
  `017a80aeb9a6759c8f6913a37031ff1616ec1bda`, `HISTORICAL_BOUNDED_NEEDS_EXACT_PRIMARY_CHECK`) — remove
  keyword/oracle and use strong comparators; this certificate's comparators are the literal ablation and
  exact-UNKNOWN/EXPLORE semantics with structurally distinct statuses.
- **R2 predecessors (not duplicates).** EXP-PRODUCT-37950607128 certified arm differentiation on a SYNTHETIC
  fixture; EXP-PRODUCT-37973256064 proved the parameterized path live on a **non-shipped** kernel (audit PASS,
  12/15 held-out EXECUTABLE, PC-EXACT-REPLAY 15/15, refusal 1.0). Neither installed the carrier at the shipping
  kernel path with identity pinned to blob `b15ed848...`/`718efa6a...` — that is this allocation's unique,
  gated object (mandate comparative_reasoning).
- **Parent handoff exclusion.** EXP-PRODUCT-37989728440's `next_question` proposed either a programmatic-model
  four-arm benchmark or an asymmetric-discovery substrate; the mandate's stop-trigger line and the parent's own
  `do_not_assume` (a fourth re-run of the mandatory-discovery deterministic REST certificate is explicitly
  excluded) keep the certificate here on the credential-free deterministic substrate with honest counters. The
  COLD/RETRIEVAL arms are not re-run because they sit at the 1.0 correctness ceiling on this substrate class
  (frozen C1/C5 unsatisfiable) — re-running them would be a non-discriminating repeat, not a second experiment.

## 4. Inherited state from the parent handoff (EXP-PRODUCT-37989728440, SUPERSEDE)

- **Established (inherited as measured, not re-asserted as claim evidence).** The mandatory-discovery
  deterministic credential-free REST substrate class saturates the frozen dynamic-range certificate: B-COLD and
  B-RETRIEVAL both at the 1.0 correctness ceiling at novelty >= 0.5 in F1/F2, so cost/novelty discrimination on
  that substrate is impossible; the parameterized treatment ties cold on deterministic counters there. The
  audited carrier (blob `b15ed848...` / sha256 `718efa6a...`) is live on a real credential-free substrate with
  honest accounting (EXP-PRODUCT-37973256064, audit PASS). The shipping `src/spider/kernel.py` is a literal
  kernel with no `distill_parameterized` (verified at design time: blob `cfec98660b...`, sha256 `46929b3a...`).
- **Rejected (must not be carried forward).** (i) That the mandatory-discovery REST substrate can discriminate a
  treatment (frozen unsatisfiable certificate). (ii) That `distill_parameterized` exists in the shipped kernel
  today (verified literal). (iii) That a mechanism installed only in a lane branch discharges the flagship
  benchmark's blocker B1 (it does not; B1 requires the carrier at the shipping path).
- **Unknown (this packet directly tests one).** Whether the audited carrier can be installed byte-identically
  at the shipping path and pass the binding certificate with honest counters (this packet's entire question).
  Still out of scope: the four-arm benchmark vs COLD/INSTRUCTIONS/RETRIEVAL and the asymmetric-discovery
  substrate (unfunded until readiness (2)+(3)).
- **Do not assume.** (i) That the certificate examines any model endpoint (credential-free by mandate; a
  capable endpoint is Intel's B3 blocker, not this packet's). (ii) That PROMOTION follows automatically from a
  certificate PASS here — only DIRECTOR verdict + independent audit PASS can enable it. (iii) That
  C-PARAM-INHERIT advances to VALIDATED on a PASS here — the registry next gate still requires the four-arm
  benchmark. (iv) That `src/spider/kernel.py` may be pinned by a freeze path hash — it is the treatment object;
  its identity is pinned by the two git blobs (section 13).

## 5. Satisfiability evidence (DESIGN probes; claim-bearing measurement never run in DESIGN)

All probes were hermetic (a cloned simulation tree with its own `.git` containing the two frozen blob objects
and the same package/experiment files); the shipping path was never touched (`git status --porcelain` in the
real repo showed no experiment/tree mutation, only DESIGN's own spec/prereg writes). The runner under test was
the **exact FROZEN RUNNER block** (section 14), materialized at the EXECUTE harness path, auto-detecting the
simulated repo root, with the sim's `freeze.json` produced by the real freezer's hash rules. Evidence:

1. **EXECUTE-mode full run, NO environment overrides** (defaults `git:<blob>` carrier/literal sources,
   auto-detected repo root) -> status COMPLETE, outcome SUPPORTS. `run_config` recorded: carrier_src
   `git:b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, literal_src `git:cfec98660b0277ccbf295e8a4119e8d81ddccf50`,
   probe_mode false, sources_are_git true. D0-IDENTITY PASS (pre 46929b3a... -> post 718efa6a..., carrier
   source sha 718efa6a...), D1-POSITIVE PASS (induction on item-001..005 -> support `^item\-00[0-9]{1}$`,
   slots `['item']`, confidence 0.9; held-out unseen `item-007` -> EXECUTABLE, bound url contains item-007,
   fixture status 200, verify true), D2-NEGATIVE PASS (item-010/item-999/item-xyz -> EXPLORE + 'support'
   reason + null action; {} and {'wrong_key':'x'} -> EXPLORE + 'parameter' reason + null action; delete_item
   -> exactly UNKNOWN 'no applicable validated mechanism'; never_seen_intent -> exactly UNKNOWN; all
   bound_action null), D3-COUNTERS PASS (retrieval 9 == transcript resolve+rebind count, verification 1,
   repair 1; model_calls 0, model_tokens 0), D4-CONTROLS PASS (literal lacks distill_parameterized;
   PC-EXACT-REPLAY 5/5 EXECUTABLE; regression 3/3), V8_FREEZE_BINDING PASS. Regression's 'Ran 3 tests' banner
   is written to stderr; stdout is a single parseable JSON document.
2. **Substituted carrier** (`EXP_CARRIER_SRC=git:<fake blob>` of the substitution kernel) -> status BLOCKED,
   outcome MEASUREMENT_INVALID, D0 FAIL (carrier source sha mismatch: got ed1d918c..., expected 718efa6a...),
   post-install identity absent, kernel untouched (file sha still 46929b3a...). Stop trigger works: the
   certificate never runs against a substituted carrier.
3. **Tampered freeze.json** (prereg hash altered) -> status BLOCKED, outcome MEASUREMENT_INVALID, V8 FAIL,
   kernel untouched.
4. **Missing freeze.json (EXECUTE mode)** -> status BLOCKED, outcome MEASUREMENT_INVALID, V8 MEASUREMENT_INVALID.
5. **Probe mode** (`EXP_PROBE_MODE=1`, no freeze.json) -> COMPLETE/SUPPORTS with V8 UNBOUND-RUN recorded and
   `run_config.probe_mode` true: probe mode never fabricates a binding check and never forces a BLOCKED stop;
   only EXECUTE mode enforces V8.

Git-object availability is not a design dependency: at real EXECUTE the runner runs inside the real repository,
whose object store contains both frozen blobs (`git cat-file -e b15ed848...` and `git cat-file -e
cfec9866...` verified at design time), and the default `git:` sources resolve there exactly as in probe 1.
The certificate-logic hardening runs during design iteration used explicit `file:` sources; probe 1 (git-backed,
no overrides) is the binding evidence that the whole path works under the EXECUTE contract as frozen.

## 6. Treatment and identity pinning

Treatment: install the audited carrier kernel byte-identically at `src/spider/kernel.py`. Source of truth is
the immutable git object: `git cat-file blob b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` (sha256
`718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`; the runner re-verifies the sha of the
materialized bytes before writing). Pre-install identity must be the literal 46929b3a... (first run) or an
already-installed carrier 718efa6a... (idempotent re-run after an interrupted EXECUTE); any other state blocks
the run (D0/P0). Carrier blob size 491 lines; literal blob 132 lines — structurally distinct (attribution).

## 7. Certificate bank, fixture and controls

- **Fixture (embedded in the FROZEN RUNNER).** In-process `http.server.ThreadingHTTPServer` on `127.0.0.1:0`
  (ephemeral loopback port), deterministic JSON responses: `GET /api/items/<id>` -> 200
  `{"type":"item","id":<id>,"data":"res:"+<id>}`, anything else -> 404. No RNG, no wall clock, no egress.
- **Induction observations** (5, >=3 per mandate): intent `read_item`, ids `item-001..item-005`, one per id.
- **Held-out positive identifier (UNSEEN, inside induced support):** `item-007` (single-digit suffix matches
  `^item\-00[0-9]{1}$`). Satisfiability guard V5: the audited support inference refuses two-digit suffixes, so
  `item-010` is the **out-of-support negative**, never the positive.
- **Controls (stable IDs where inherited).** `PC-EXACT-REPLAY` (positive control): the 5 training ids must
  re-resolve EXECUTABLE on the installed carrier (5/5). `B-LITERAL-KERNEL` (ablation, inherited ID): the shipped
  literal kernel from git blob `cfec9866...` in a hermetic temp package with the same models/registry/`__init__`;
  must NOT have `distill_parameterized` (attribution). `NC-OUT-OF-SUPPORT-ID` (item-010, item-999, item-xyz ->
  EXPLORE + 'support' reason + null action), `NC-MISSING-PARAMETER` ({} and `{'wrong_key':'x'}` -> EXPLORE +
  'parameter' reason + null action), `NC-WRONG-INTENT` (delete_item -> exactly UNKNOWN), `NC-NO-APPLICABLE-
  MECHANISM` (never_seen_intent -> exactly UNKNOWN). Regression: `tests/test_kernel.py` 3/3 on the installed
  carrier.

## 8. Certificate definition (frozen decision rule; binding detail in spec.json)

- **D0-IDENTITY**: pre-install sha in {46929b3a..., 718efa6a...}; carrier source sha == 718efa6a...; post-install
  bytes == git blob b15ed848... and file sha == 718efa6a.... FAIL -> BLOCKED/MEASUREMENT_INVALID (stop trigger).
- **D1-POSITIVE**: mechanism distilled (slots ['item'], support regex, confidence == 0.9); resolve on `item-007`
  -> EXECUTABLE; bound_action non-null with url containing `item-007`; executing -> fixture status 200; verify
  true. FAIL -> FALSIFIES.
- **D2-NEGATIVE**: 7 probes (3 out-of-support, 2 missing-parameter, wrong-intent, never-seen). All: bound_action
  null + non-empty reason + status != EXECUTABLE; out-of-support/missing-param -> EXPLORE with the correct
  reason class; wrong-intent/no-applicable -> EXACTLY UNKNOWN. FAIL -> FALSIFIES.
- **D3-COUNTERS**: retrieval_calls == #resolve+#rebind in transcript; verification_calls == #verify;
  repair_attempts == #rebind; model_calls == 0; model_tokens == 0. FAIL -> FALSIFIES.
- **D4-CONTROLS**: literal ablation has no distill_parameterized; PC-EXACT-REPLAY 5/5; regression 3/3.
  FAIL -> FALSIFIES.
- **V8-FREEZE-BINDING** (EXECUTE mode only): (A) sha256(prereg.md) == freeze.json.hashes['prereg.md']; (B)
  running source == FROZEN RUNNER block (normalized for a trailing newline and CRLF); (C) each artifact hash in
  freeze.json.artifact_hashes matches. Freeze.json missing/unreadable -> BLOCKED; mismatch -> MEASUREMENT_INVALID.
  Probe mode never fabricates V8.
- **Outcome mapping**: BLOCKED + MEASUREMENT_INVALID for D0/V8/infrastructure failures; COMPLETE + SUPPORTS if
  D1..D4 all PASS (and V8 enforced); COMPLETE + FALSIFIES if D1..D4 fails on a correctly installed carrier.
  Precedence: MEASUREMENT_INVALID > FALSIFIES > SUPPORTS. Promotion semantics: certificate PASS is necessary,
  not sufficient; only a DIRECTOR verdict after independent audit PASS enables promotion.

## 9. Metrics

M-CERT-PASS (D0-D4+V8 statuses), M-IDENTITIES (pre/carrier-source/post shas + blobs), M-POSITIVE
(resolution_status, confidence, bound url, fixture_status, verify), M-NEGATIVES (7 probes: case/status/reason/
bound_action), M-COUNTERS (retrieval/verification/repair/model_calls/model_tokens + transcript length),
M-PC-EXACT-REPLAY, M-ABLATION (has_distill_parameterized), M-REGRESSION (tests_run/failures/errors),
M-SUPPORT (mechanism_id, slots, support regex, confidence).

## 10. Honest counters (clause c semantics)

`TrajectoryCounters` (in `spider.kernel`) is attached at kernel construction; `resolve` increments
`retrieval_calls`, `verify` increments `verification_calls`, `rebind` increments `repair_attempts` (and calls
resolve, incrementing retrieval again). D3 asserts the counters equal an independent per-call invocation
transcript recorded by the runner; `model_calls == 0` and `model_tokens == 0` asserted. No counter event is
injected. `http_requests` is NOT auto-incremented by the kernel (it is runner-side); the certificate does not
gate on it, and the fixture's actual request count is recorded in observations. Probe-verified values for the
full certificate path: retrieval 9, verification 1, repair 1.

## 11. Validity gates

V1-DETERMINISM, V2-CREDENTIAL-FREE, V3-IDENTITY-THREE-PART, V4-STOP-TRIGGER, V5-HELD-OUT-INSIDE-SUPPORT,
V6-REFUSAL-SEMANTICS, V7-TRANSCRIPT-HONESTY, V8-FREEZE-BINDING, V9-REGRESSION, V10-ABLATION-ATTRIBUTION —
details in `spec.json#measurement_validity`. Known disclosed limitations: (i) induced support is a conservative
char-class/quantifier inference (audited behavior), which the bank exploits deliberately (single-digit positives,
two-digit negatives); (ii) the fixture is a minimal REST server, so execution correctness is verified only for
the GET/JSON shape the induction encodes; (iii) latent pretrained knowledge of the carrier's source cannot be
excluded — attribution rests on the byte-pinned blob identity plus the literal ablation, not on authorship
narratives.

## 12. Validity threats and mitigations

- **Substituted carrier** (mitigation: D0 sha + blob byte check, stop trigger, verified in probe).
- **Attribution confound** (mitigation: literal ablation from the frozen blob in a hermetic package; identical
  models/registry).
- **Non-discriminating bank** (mitigation: bank is 5-in-support/out-of-support-boundary by construction;
  support regex probed to accept item-007 and reject item-010/999/xyz; confidence fixed at 0.9).
- **Unreachable branch** (mitigation: all branches probed — SUPPORTS, FALSIFIES-by-construction, BLOCKED x3).
- **Counter dishonesty** (mitigation: transcript-vs-counter equality; probe values recorded).
- **Freeze drift** (mitigation: V8 three-part binding enforced at EXECUTE; kernel.py identity pinned by blobs,
  not a mutable path hash).

## 13. Freeze artifacts and binding model

`freeze_artifacts` (existing files, sha256 recorded in CANONICAL-HASHES and re-recorded in freeze.json at
freeze time): `pyproject.toml` (src discovery), `src/spider/__init__.py`, `src/spider/models.py`,
`src/spider/registry.py` (package surface the installed carrier imports; models/registry byte-identical to the
audited package copies), `tests/test_kernel.py` (regression suite). **`src/spider/kernel.py` is excluded by
design**: it is the treatment object. Freezing a path hash of the file the experiment itself rewrites would be
self-contradictory after installation; the mandate pins its identity instead via the immutable git blob
(`b15ed848...` / sha256 `718efa6a...` after install; `cfec9866...` / `46929b3a...` before). The pre-install
identity is additionally recorded as a baseline observation. The certificate runner and canonical identities are
embedded in this file (sections 14-15) and are therefore bound by `freeze.json.hashes['prereg.md']`; the fixture
is in-process stdlib inside the runner. No unbound mutable code, task bank, dataset or fixture remains.

## 14. FROZEN RUNNER (verbatim; bound by freeze.json.hashes['prereg.md'])

EXECUTE materializes this block byte-exact at
`research/experiments/EXP-PRODUCT-38180719830/harness/run_certificate.py` (create the harness directory if
absent), verifies V8-B against `__file__`, and runs it with NO environment overrides (default `git:` sources for
carrier and literal; auto-detected repo root from the harness path upward). The FROZEN RUNNER sha256 is recorded
in CANONICAL-HASHES: a114804c391aa8360d0616fa27a4b217783abea4f005a29f87d22f7566daf2f3
(sha256 of the exact bytes between the markers, no trailing newline; normalized at V8-B for trailing
newline/CRLF).

<!-- BEGIN FROZEN RUNNER -->
#!/usr/bin/env python3
"""FROZEN RUNNER for EXP-PRODUCT-38180719830 (embedded verbatim in prereg.md).

Deterministic, stdlib-only, credential-free installation + identity + binding
certificate for the audited parameterized carrier at the shipping kernel path
src/spider/kernel.py. Phases -> decision-rule clauses D0..D4:

  P0  pre-install identity baseline                         (D0)
  P1  B-LITERAL-KERNEL ablation: literal kernel from git   (D4)
  P2  byte-identical carrier installation                  (D0)
  P3  identity certificate (installed file == git blob)    (D0)
  P4  positive certificate: induction -> EXECUTABLE@0.9 ->
      fixture 200 -> verify true on UNSEEN held-out id     (D1)
  P5  negative certificate: out-of-support / missing-param
      / wrong-intent / no-applicable-mechanism: recorded reason
      + null bound action; exactly UNKNOWN for
      no-applicable-mechanism                              (D2)
  P6  honest inherited-path counters: retrieval_calls,
      verification_calls, repair_attempts == invocation
      transcript; model_calls == 0, model_tokens == 0      (D3)
  P7  controls: PC-EXACT-REPLAY (training ids resolve
      EXECUTABLE) + regression tests/test_kernel.py pass   (D4)
  P8  freeze binding (V8): sha256(prereg.md) == freeze.json
      hash; runner source == FROZEN RUNNER block of the
      hash-bound prereg; freeze artifact hashes match       (V8)

Stop trigger (mandate): if the carrier cannot be installed byte-identically
(git object missing) or the installed identity mismatches, record the exact
promotion blocker and exit BLOCKED; never test a substituted carrier.

Env overrides (hermetic dry-run only, never change certificate logic):
  EXP_CARRIER_SRC : git:<blob> (default) or file:<path>
  EXP_LITERAL_SRC : git:<blob> (default) or file:<path>
  EXP_TARGET_ROOT : repo root containing src/spider (default: auto-detected)

Output JSON: status (COMPLETE|BLOCKED), outcome (SUPPORTS|FALSIFIES), one
certificate clause per decision-rule check, identities, counters, observations.
"""
from __future__ import annotations

import hashlib
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

# -- injection point for canonical identities (prereg CANONICAL-HASHES) --
CARRIER_BLOB = "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796"
CARRIER_SHA256 = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
LITERAL_BLOB = "cfec98660b0277ccbf295e8a4119e8d81ddccf50"
LITERAL_SHA256 = "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61"
# ---------------------------------------------------------------------------

INTENT = "read_item"
TRAIN_IDS = ["item-001", "item-002", "item-003", "item-004", "item-005"]
HELD_OUT_IN_SUPPORT = "item-007"   # unseen; single-digit suffix -> inside induced support
OOS_IDS = ["item-010", "item-999", "item-xyz"]  # outside ^item\-00[0-9]{1}$ support
WRONG_INTENT = "delete_item"
NEVER_SEEN_INTENT = "never_seen_intent"
CTX = {"resource_type": "item", "authenticated": True}


def detect_repo_root() -> Path:
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "pyproject.toml").exists() and (p / "src/spider").exists():
            return p
        p = p.parent
    raise RuntimeError("repo root (pyproject.toml + src/spider) not found upward from runner")


REPO_ROOT = Path(os.environ.get("EXP_TARGET_ROOT") or str(detect_repo_root()))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_source(spec: str) -> bytes:
    if spec.startswith("git:"):
        blob = spec[4:]
        out = subprocess.run(["git", "-C", str(REPO_ROOT), "cat-file", "blob", blob],
                             capture_output=True)
        if out.returncode != 0:
            raise RuntimeError(f"git object {blob} unavailable: {out.stderr.decode()[:200]}")
        return out.stdout
    if spec.startswith("file:"):
        return Path(spec[5:]).read_bytes()
    raise RuntimeError(f"unknown source spec: {spec}")


class FixtureHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parts = self.path.strip("/").split("/")
        body = {}
        if len(parts) == 3 and parts[:2] == ["api", "items"]:
            body = {"type": "item", "id": parts[2], "data": "res:" + parts[2]}
            self.send_response(200)
        else:
            self.send_response(404)
        payload = json.dumps(body).encode()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


def start_fixture() -> tuple[http.server.ThreadingHTTPServer, int]:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FixtureHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1]


def execute(bound_action: dict) -> tuple[int, dict]:
    with urllib.request.urlopen(bound_action["url"], timeout=5) as resp:
        return resp.status, json.loads(resp.read().decode())


def mk_obs(intent, ident, port):
    url = f"http://127.0.0.1:{port}/api/items/{ident}"
    return {
        "intent": intent,
        "state": dict(CTX),
        "action": {"method": "GET", "url": url},
        "next_state": {"type": "item", "id": ident, "data": "res:" + ident},
        "success": True,
        "provenance": {"exp": "EXP-PRODUCT-38180719830", "role": "induction"},
    }


def make_pkg(target_pkg: Path, kernel_bytes: bytes, models: bytes, registry: bytes,
             init: bytes) -> None:
    target_pkg.mkdir(parents=True, exist_ok=True)
    (target_pkg / "kernel.py").write_bytes(kernel_bytes)
    (target_pkg / "models.py").write_bytes(models)
    (target_pkg / "registry.py").write_bytes(registry)
    (target_pkg / "__init__.py").write_bytes(init)


def drop_module(name: str) -> None:
    sys.modules.pop(name, None)


def _extract(text: str, name: str) -> str:
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END " + re.escape(name) + r" -->", text, re.S)
    if not m:
        raise RuntimeError(f"block {name} not found in prereg.md")
    return m.group(1)


def v8_freeze_binding(result: dict) -> bool:
    """V8 freeze binding. In EXECUTE mode (default) freeze.json MUST exist next
    to the experiment prereg and all three binding clauses must hold; a missing
    freeze.json or any mismatch is MEASUREMENT_INVALID (never FALSIFIES) and the
    certificate stops before any outcome measurement. In probe mode
    (EXP_PROBE_MODE=1) a missing freeze.json records UNBOUND-RUN so a hermetic
    satisfiability probe can run; an existing freeze.json is still enforced.
    Returns True to continue, False to stop as BLOCKED/MEASUREMENT_INVALID."""
    probe = os.environ.get("EXP_PROBE_MODE") == "1"
    exp = REPO_ROOT / "research/experiments/EXP-PRODUCT-38180719830"
    freeze_path = exp / "freeze.json"
    if not freeze_path.exists():
        if probe:
            result["observations"].append(
                {"type": "binding", "V8": "UNBOUND-RUN: no freeze.json found; V8 not enforced "
                                          "(probe mode only)."}
            )
            return True
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "freeze.json missing at " + str(freeze_path) + " (EXECUTE mode)",
        }
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return False
    try:
        freeze = json.loads(freeze_path.read_text())
        def _norm(s: str) -> str:
            return s.replace("\r\n", "\n").rstrip()
        prereg_b = (exp / "prereg.md").read_bytes()
        block = _extract(prereg_b.decode("utf-8"), "FROZEN RUNNER")
        this_src = Path(__file__).resolve().read_text(encoding="utf-8")
        ok_a = hashlib.sha256(prereg_b).hexdigest() == freeze["hashes"]["prereg.md"]
        ok_b = (_norm(this_src) == _norm(block))
        ok_c = True
        for rel, h in freeze.get("artifact_hashes", {}).items():
            if hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest() != h:
                ok_c = False
                break
    except Exception as exc:
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID", "reason": "freeze binding unreadable: " + str(exc)}
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return False
    ok_all = ok_a and ok_b and ok_c
    result["certificate"]["V8_FREEZE_BINDING"] = {
        "status": "PASS" if ok_all else "FAIL",
        "prereg_sha_matches": ok_a,
        "runner_source_matches_frozen_block": ok_b,
        "artifact_hashes_match": ok_c,
        "reason": "hash-bound prereg; running source == FROZEN RUNNER block; freeze artifact hashes intact",
    }
    result["observations"].append({"type": "binding", "V8": "enforced"})
    if not ok_all:
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return False
    return True


def main() -> dict:
    result = {
        "schema_version": 1,
        "experiment_id": "EXP-PRODUCT-38180719830",
        "lane": "product",
        "certificate": {},
        "identities": {},
        "counters_transcript": [],
        "observations": [],
        "unresolved": [],
    }

    kernel_path = REPO_ROOT / "src/spider/kernel.py"
    models_bytes = (REPO_ROOT / "src/spider/models.py").read_bytes()
    registry_bytes = (REPO_ROOT / "src/spider/registry.py").read_bytes()
    init_bytes = (REPO_ROOT / "src/spider/__init__.py").read_bytes()

    carrier_src = os.environ.get("EXP_CARRIER_SRC", f"git:{CARRIER_BLOB}")
    literal_src = os.environ.get("EXP_LITERAL_SRC", f"git:{LITERAL_BLOB}")
    result["run_config"] = {
        "repo_root": str(REPO_ROOT),
        "carrier_src": carrier_src,
        "literal_src": literal_src,
        "probe_mode": bool(os.environ.get("EXP_PROBE_MODE")),
        "sources_are_git": carrier_src.startswith("git:") and literal_src.startswith("git:"),
    }

    # ---- P8 freeze binding first (mandatory at EXECUTE; probe mode records UNBOUND-RUN) ----
    if not v8_freeze_binding(result):
        return result

    # ---- P0 pre-install identity baseline ----
    pre = sha256_bytes(kernel_path.read_bytes())
    result["identities"]["pre_install_sha256"] = pre
    result["identities"]["pre_install_expected"] = LITERAL_SHA256
    result["identities"]["pre_install_git_blob"] = LITERAL_BLOB
    result["observations"].append(
        {"type": "pre_install_identity", "sha256": pre, "expected": LITERAL_SHA256}
    )
    if pre not in (LITERAL_SHA256, CARRIER_SHA256):
        result["certificate"]["D0_IDENTITY"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "pre-install src/spider/kernel.py is neither the literal ("
                      + LITERAL_SHA256 + ") nor the already-installed carrier ("
                      + CARRIER_SHA256 + "); shipping path in unknown state",
        }
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result

    # ---- P1 B-LITERAL-KERNEL ablation (temp package; repo untouched) ----
    try:
        literal_bytes = read_source(literal_src)
        if sha256_bytes(literal_bytes) != LITERAL_SHA256:
            raise RuntimeError("literal blob sha mismatch")
        with tempfile.TemporaryDirectory() as td:
            pkg = Path(td) / "spider"
            make_pkg(pkg, literal_bytes, models_bytes, registry_bytes, init_bytes)
            sys.path.insert(0, td)
            for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
                drop_module(m)
            import spider as lit  # literal kernel package (audited models/registry)
            has_param_path = hasattr(lit.SpiderKernel, "distill_parameterized")
            sys.path.remove(td)
            for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
                drop_module(m)
            result["certificate"]["D4_CONTROLS"] = {
                "literal_ablation": {
                    "status": "PASS" if not has_param_path else "FAIL",
                    "has_distill_parameterized": has_param_path,
                    "reason": "literal kernel lacks distill_parameterized; positive certificate "
                              "attributes to the installed carrier only",
                }
            }
            result["observations"].append(
                {"type": "derived", "literal_has_distill_parameterized": has_param_path}
            )
    except Exception as exc:  # operational, not a negative result
        result["certificate"]["D4_CONTROLS"] = {
            "literal_ablation": {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        }
        result["status"] = "BLOCKED"
        return result

    # ---- P2 install carrier byte-identically; P3 identity certificate ----
    try:
        carrier_bytes = read_source(carrier_src)
        carrier_sha = sha256_bytes(carrier_bytes)
        result["identities"]["carrier_source_sha256"] = carrier_sha
        result["identities"]["carrier_git_blob"] = CARRIER_BLOB
        if carrier_sha != CARRIER_SHA256:
            result["certificate"]["D0_IDENTITY"] = {
                "status": "FAIL",
                "reason": "carrier source sha mismatch (got "
                          + carrier_sha + ", expected " + CARRIER_SHA256 + ")",
            }
            result["status"] = "BLOCKED"   # stop trigger: never test a substituted carrier
            result["outcome"] = "MEASUREMENT_INVALID"
            return result
        kernel_path.write_bytes(carrier_bytes)
        post = sha256_bytes(kernel_path.read_bytes())
        result["identities"]["post_install_sha256"] = post
        result["identities"]["post_install_git_blob"] = CARRIER_BLOB
        if post != CARRIER_SHA256:
            result["certificate"]["D0_IDENTITY"] = {
                "status": "FAIL",
                "reason": "installed kernel sha mismatch (got " + post + ")",
            }
            result["status"] = "BLOCKED"   # stop trigger
            result["outcome"] = "MEASUREMENT_INVALID"
            return result
        result["certificate"]["D0_IDENTITY"] = {
            "status": "PASS",
            "reason": "installed file byte-identical to frozen carrier git blob "
                      + CARRIER_BLOB + " (sha256 " + CARRIER_SHA256 + ")",
        }
    except Exception as exc:
        result["certificate"]["D0_IDENTITY"] = {
            "status": "MEASUREMENT_INVALID", "reason": str(exc)
        }
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result

    # ---- P4/P5/P6/P7 against INSTALLED package ----
    sys.path.insert(0, str(REPO_ROOT / "src"))
    for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
        drop_module(m)
    from spider.kernel import SpiderKernel, TrajectoryCounters
    from spider.models import Observation, ResolutionStatus
    from spider.registry import MechanismRegistry

    fixture, port = start_fixture()
    observations = [Observation(**mk_obs(INTENT, ident, port)) for ident in TRAIN_IDS]
    transcript: list[dict] = []

    try:
        with tempfile.TemporaryDirectory() as td:
            reg = MechanismRegistry(Path(td) / "mechanisms.jsonl")
            counters = TrajectoryCounters()
            kernel = SpiderKernel(reg, min_confidence=0.8, counters=counters)
            mech = kernel.distill_parameterized(observations)
            reg.upsert(mech)
            slots = mech.parameter_slots
            support = mech.verification_rule["parameter_supports"]
            result["observations"].append(
                {"type": "derived", "mechanism_id": mech.mechanism_id, "slots": slots,
                 "support": support, "confidence": mech.confidence}
            )

            # ---- D1 positive certificate on UNSEEN held-out identifier ----
            params = {s: HELD_OUT_IN_SUPPORT for s in slots}
            transcript.append({"op": "resolve", "args": [INTENT, HELD_OUT_IN_SUPPORT]})
            res = kernel.resolve(INTENT, CTX, params)
            pos_binding_ok = (
                res.status == ResolutionStatus.EXECUTABLE
                and res.bound_action is not None
                and HELD_OUT_IN_SUPPORT in res.bound_action["url"]
                and res.confidence == 0.9
            )
            status, body = (0, {})
            if res.bound_action:
                transcript.append({"op": "execute", "url": res.bound_action["url"]})
                status, body = execute(res.bound_action)
            transcript.append({"op": "verify", "args": [res.mechanism_id]})
            verify_ok = kernel.verify(res.mechanism_id, body, params) if status == 200 else False
            result["certificate"]["D1_POSITIVE"] = {
                "status": "PASS" if (pos_binding_ok and status == 200 and verify_ok) else "FAIL",
                "resolution_status": res.status.value,
                "resolution_confidence": res.confidence,
                "bound_action": res.bound_action,
                "fixture_status": status,
                "verify": verify_ok,
                "held_out": HELD_OUT_IN_SUPPORT,
                "reason": ">=3 induction observations; unseen held-out id bound EXECUTABLE@0.9; "
                          "fixture 200; verify true",
            }

            # ---- D2 negative certificate ----
            negatives = []
            for oos in OOS_IDS:
                transcript.append({"op": "resolve", "args": [INTENT, oos]})
                r = kernel.resolve(INTENT, CTX, {s: oos for s in slots})
                negatives.append({"case": f"out_of_support:{oos}", "status": r.status.value,
                                  "reason": r.reason, "bound_action": r.bound_action})
            transcript.append({"op": "resolve", "args": [INTENT, "<missing>"]})
            r = kernel.resolve(INTENT, CTX, {})
            negatives.append({"case": "missing_parameter", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            transcript.append({"op": "resolve", "args": [INTENT, "<wrong-key>"]})
            r = kernel.resolve(INTENT, CTX, {"wrong_key": "x"})
            negatives.append({"case": "missing_parameter_wrong_key", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            transcript.append({"op": "resolve", "args": [WRONG_INTENT, HELD_OUT_IN_SUPPORT]})
            r = kernel.resolve(WRONG_INTENT, CTX, params)
            negatives.append({"case": "wrong_intent", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            transcript.append({"op": "resolve", "args": [NEVER_SEEN_INTENT, "<none>"]})
            r = kernel.resolve(NEVER_SEEN_INTENT, {}, {})
            negatives.append({"case": "no_applicable_mechanism", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            all_refused = all(n["bound_action"] is None and n["reason"]
                              and n["status"] != "EXECUTABLE" for n in negatives)
            unknown_exact = all(
                n["status"] == "UNKNOWN"
                for n in negatives if n["case"] in ("wrong_intent", "no_applicable_mechanism")
            )
            oos_explore = all(
                n["status"] == "EXPLORE" and "support" in n["reason"]
                for n in negatives if n["case"].startswith("out_of_support:")
            )
            missing_explore = all(
                n["status"] == "EXPLORE" and "parameter" in n["reason"]
                for n in negatives if n["case"].startswith("missing_parameter")
            )
            result["certificate"]["D2_NEGATIVE"] = {
                "status": "PASS" if (all_refused and unknown_exact
                                     and oos_explore and missing_explore) else "FAIL",
                "negatives": negatives,
                "reason": "every refusal: recorded reason + null bound action; out-of-support/"
                          "missing-parameter EXPLORE; no-applicable-mechanism exactly UNKNOWN",
            }

            # ---- D3 honest counters vs invocation transcript ----
            counters_before = counters.as_dict()
            transcript.append({"op": "rebind", "args": [INTENT, HELD_OUT_IN_SUPPORT]})
            _ = kernel.rebind(INTENT, CTX, params)
            counters_after = counters.as_dict()
            expected_retrieval = sum(1 for t in transcript if t["op"] in ("resolve", "rebind"))
            expected_verify = sum(1 for t in transcript if t["op"] == "verify")
            expected_repair = sum(1 for t in transcript if t["op"] == "rebind")
            counters_ok = (
                counters_after["retrieval_calls"] == counters_before["retrieval_calls"] + 1
                and counters_after["repair_attempts"] == counters_before["repair_attempts"] + 1
                and counters_after["retrieval_calls"] == expected_retrieval
                and counters_after["verification_calls"] == expected_verify
                and counters_after["repair_attempts"] == expected_repair
                and counters_after["model_calls"] == 0
                and counters_after["model_tokens"] == 0
            )
            result["certificate"]["D3_COUNTERS"] = {
                "status": "PASS" if counters_ok else "FAIL",
                "counters_after": counters_after,
                "expected_from_transcript": {
                    "retrieval_calls": expected_retrieval,
                    "verification_calls": expected_verify,
                    "repair_attempts": expected_repair,
                },
                "reason": "retrieval_calls/verification_calls/repair_attempts equal the invocation "
                          "transcript; model_calls=0, model_tokens=0 (no model anywhere on path)",
            }
            result["counters_transcript"] = transcript
            result["counters"] = counters_after

            # ---- D4 controls: PC-EXACT-REPLAY ----
            replay = []
            for ident in TRAIN_IDS:
                transcript.append({"op": "resolve", "args": [INTENT, ident]})
                r = kernel.resolve(INTENT, CTX, {s: ident for s in slots})
                replay.append({"id": ident, "status": r.status.value})
            replay_ok = all(r["status"] == "EXECUTABLE" for r in replay)
            result["certificate"]["D4_CONTROLS"]["pc_exact_replay"] = {
                "status": "PASS" if replay_ok else "FAIL",
                "replay": replay,
                "reason": "all training ids re-resolve EXECUTABLE on installed carrier",
            }
            fixture.shutdown()
    except Exception as exc:
        fixture.shutdown()
        result["certificate"]["D0_IDENTITY"] = result["certificate"].get(
            "D0_IDENTITY", {"status": "MEASUREMENT_INVALID", "reason": "unknown"})
        result["certificate"]["CORE"] = {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result

    # ---- D4 controls: regression on installed carrier ----
    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test_*.py")
    tresult = unittest.TextTestRunner(verbosity=0).run(suite)
    result["certificate"]["D4_CONTROLS"]["regression"] = {
        "status": "PASS" if (tresult.wasSuccessful() and tresult.testsRun >= 3) else "FAIL",
        "tests_run": tresult.testsRun,
        "failures": len(tresult.failures),
        "errors": len(tresult.errors),
        "reason": "existing test_kernel suite passes on installed carrier",
    }

    clauses = [result["certificate"][k] for k in ("D0_IDENTITY", "D1_POSITIVE",
                                                  "D2_NEGATIVE", "D3_COUNTERS")]
    clauses.append(
        {"status": result["certificate"]["D4_CONTROLS"].get("pc_exact_replay", {}).get("status"),
         "literal": result["certificate"]["D4_CONTROLS"].get("literal_ablation", {}).get("status"),
         "regression": result["certificate"]["D4_CONTROLS"].get("regression", {}).get("status")}
    )
    if "V8_FREEZE_BINDING" in result["certificate"]:
        clauses.append(result["certificate"]["V8_FREEZE_BINDING"])
    all_pass = all(c.get("status") == "PASS" for c in clauses)
    result["status"] = "COMPLETE"
    result["outcome"] = "SUPPORTS" if all_pass else "FALSIFIES"
    result["unresolved"] = []
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
<!-- END FROZEN RUNNER -->

## 15. CANONICAL-HASHES

sha256 of the exact bytes between the markers for each block (no trailing newline; normalized at V8-B for
trailing newline/CRLF):

```json
{
  "FROZEN RUNNER": "a114804c391aa8360d0616fa27a4b217783abea4f005a29f87d22f7566daf2f3",
  "CARRIER_BLOB": "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796",
  "CARRIER_SHA256": "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72",
  "LITERAL_BLOB": "cfec98660b0277ccbf295e8a4119e8d81ddccf50",
  "LITERAL_SHA256": "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61",
  "artifacts": {
    "pyproject.toml": "5f03fb5914f388c19973831287cce6773c7364e1bea856a595cd7247d3115b83",
    "src/spider/__init__.py": "3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77",
    "src/spider/models.py": "338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78",
    "src/spider/registry.py": "51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c",
    "tests/test_kernel.py": "ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6"
  }
}
```

## 16. EXECUTE contract

1. Verify V8: freezed `freeze.json` exists, sha256(prereg.md) matches `freeze.json.hashes['prereg.md']`,
   `__file__` equals the FROZEN RUNNER block, freeze artifact hashes match (the runner does this first and stops
   BLOCKED otherwise; probe mode is NOT used at EXECUTE).
2. Run `python3 harness/run_certificate.py` from the experiment dir with NO environment overrides: must not set
   `EXP_CARRIER_SRC`, `EXP_LITERAL_SRC`, `EXP_TARGET_ROOT` or `EXP_PROBE_MODE` (defaults resolve the two frozen
   git blobs inside the real repository and auto-detect the repo root; the git-backed no-override path is probe-
   verified in section 5). Capture stdout and stderr separately: `> run_certificate.out.json 2> run_certificate.log`
   — stdout is the single JSON document (the unittest banner 'Ran 3 tests' goes to stderr). It (P0) records
   pre-install identity, (P1) runs the literal ablation, (P2/P3) installs the carrier byte-identically and
   verifies identity, (P4/P5/P6) runs positive/negative/counter certificates, (P7) runs controls + regression,
   and prints one JSON document to stdout.
3. Write `result.json` with the exact top-level shape from `research/EXPERIMENT_PACKET.md` (`schema_version`,
   `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`,
   `validity_notes`, `unresolved`), embedding the runner stdout (certificate clauses, identities, counters,
   transcript, negatives) as raw evidence; keep RAW EVIDENCE vs DERIVED MEASUREMENT vs INTERPRETATION distinct.
4. Preserve frozen control identifiers verbatim (B-LITERAL-KERNEL, B-PRE-INSTALL-KERNEL, PC-EXACT-REPLAY,
   NC-OUT-OF-SUPPORT-ID, NC-MISSING-PARAMETER, NC-WRONG-INTENT, NC-NO-APPLICABLE-MECHANISM).
5. On certificate failure: record the exact blocker (clause + observed values) and do NOT re-run the certificate
   against any substituted carrier (stop trigger, V4). On BLOCKED: record the exact operational reason; never
   report it as a scientific negative.
6. After EXECUTE the working tree intentionally contains the carrier at `src/spider/kernel.py`; that is the
   treatment outcome, not a regression. Do not revert or commit it — leave the tree state to the DIRECTOR
   verdict stage, and record the pre/post identities in `provenance.json`.

## 17. Consequences of both branches (preregistered)

- **SUPPORTS (certificate PASS, V8 enforced)**: necessary condition for enabling promotion of the parameterized
  carrier to the shipping kernel; a DIRECTOR verdict after independent audit PASS may then promote, discharging
  readiness condition (1) / blocker B1 for the flagship C-LLM-INHERIT benchmark. C-PARAM-INHERIT remains
  EXPERIMENTAL.
- **FALSIFIES (valid negative on a correctly installed carrier)**: promotion refused; shipping kernel stays
  literal; B1 stays open; exact blocker recorded; do not re-run on a substituted carrier.
- **BLOCKED / MEASUREMENT_INVALID**: exact operational receipt (identity, binding, git object, fixture); status
  is not a scientific outcome.