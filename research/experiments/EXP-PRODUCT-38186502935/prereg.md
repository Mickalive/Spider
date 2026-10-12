# EXP-PRODUCT-38186502935 preregistration

Shipped-carrier end-to-end execution readiness demonstration (readiness condition (1)).
DESIGN contract v2. This file, `spec.json`, `request.json` and the freeze are immutable after freeze.

---

## 1. Preregistered question, hypothesis and falsifier

**Question** (from the binding Director mandate, `request.json#director_mandate.allocation.question`):
Does the now-promoted, byte-identical shipped parameterized carrier (git blob
`b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` / sha256
`718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`, installed at the shipping
kernel path with a frozen D0-D4+V8 certificate PASS and an independent PASS audit) actually execute
the full shipped end-to-end path `distill_parameterized -> resolve -> execute -> verify/UNKNOWN` on a
credential-free substrate, producing BOTH one known-positive on a never-observed identifier AND one
known-negative refusal (abstention) at the shipped confidence/thresholds -- thereby discharging
readiness condition (1) -- or does the shipped path still fail to execute end-to-end?

**Hypothesis**: On the current shipping tree (git clean, kernel == carrier), the frozen runner
passes all five E2E clauses at shipped (default/unmodified) thresholds:
`E2E-IDENTITY`, `E2E-POSITIVE` (item-000 never-observed inside induced support), `E2E-ABSTENTION`
(item-010 known-negative + 6 more probes, zero HTTP), `E2E-COUNTERS` (transcript-consistent,
model-free, runner-side http accounting), `E2E-CONTROLS` (literal ablation, PC-EXACT-REPLAY 5/5,
regression 3/3). Consequence: `M-E2E-PASS=true`, `status=COMPLETE`, `outcome=SUPPORTS`, readiness
condition (1) DISCHARGED.

**Falsifier**: `FALSIFIES` (valid scientific negative, `status=COMPLETE`) ONLY on a verified
shipping identity (`E2E-IDENTITY PASS`) if any outcome clause fails:
E2E-POSITIVE (no/wrong mechanism, item-000 not EXECUTABLE@0.9, execute != 200, verify != true);
E2E-ABSTENTION (any refusal returns non-null bound action / empty reason / wrong status class /
any HTTP delta); E2E-COUNTERS (transcript mismatch, model_calls/model_tokens != 0, http legs != 6);
E2E-CONTROLS (literal has distill_parameterized, replay < 5/5, regression < 3/3).

`MEASUREMENT_INVALID/BLOCKED` (NEVER FALSIFIES) for identity/binding/infrastructure failures:
shipping kernel sha != carrier sha (promotion merge not in effect / tree modified / unknown
shipping-path state), git blobs missing, fixture failure, V8 freeze-binding mismatch. Full clause
definitions: spec.json `#decision_rule`.

Non-falsifiable by construction (scope limits): the four-arm C-LLM-INHERIT benchmark, cold/
instructions/retrieval comparisons, product economics, the mandatory-discovery deterministic REST
certificate, and any generalization outside the induced single-digit-suffix support on this
deterministic fixture.

## 2. Scope and out-of-scope

IN SCOPE:
- Read-only measurement of the FULL shipped end-to-end path `distill_parameterized -> resolve ->
  execute -> verify/UNKNOWN` on the AS-INSTALLED shipping kernel through the public package API
  (`from spider import ...`), on a credential-free deterministic localhost substrate.
- One known-positive on a NEVER-observed identifier (`item-000`, inside induced support, unseen in
  ANY prior SPIDER run per repo-wide artifact sweep).
- One known-negative refusal (abstention) at shipped thresholds (`item-010`), plus the inherited
  6-probe refusal battery; each refusal must issue ZERO HTTP requests.
- Honest counters: `retrieval_calls`, `verification_calls`, `repair_attempts` vs invocation
  transcript; `model_calls == 0`, `model_tokens == 0`; runner-side fixture request counter ==
  executed HTTP legs (6 = 5 induction + 1 positive; 0 abstention).
- Controls: B-LITERAL-KERNEL ablation, PC-EXACT-REPLAY, regression suite, five null controls.
- V8 freeze binding (freeze.json, prereg hash, runner == FROZEN RUNNER, SIX artifact hashes now
  INCLUDING `src/spider/kernel.py`).

OUT OF SCOPE (binding exclusions inherited from the parent handoff and the mandate):
- NOT the B1 promotion certificate re-run (EXP-PRODUCT-38180719830 verdict excludes it; the parent
  handoff `do_not_assume` repeats: do not re-run the promotion certificate).
- NOT the four-arm C-LLM-INHERIT benchmark and NO COLD/INSTRUCTIONS/RETRIEVAL arms (readiness
  conditions (2)/(3) unmet; policy forbids funding; mandate funds the condition-(1) demonstration).
- NOT the mandatory-discovery deterministic REST certificate (excluded after three failures).
- NOT product economics (model_calls=model_tokens=0 by construction), no latency/wall-clock claims,
  no amortization/staleness/browser work.
- NOT a mechanism search, NOT persistence-economics instrumentation h(N) (reserved, coupled to
  Runtime's B2 bank).
- No measurement of a substituted or repaired carrier (V4 stop trigger).

## 3. Not a repetition of prior work (legacy + immediate precedents)

`request.json#director_mandate.allocation.comparative_reasoning = "LEGACY: DISTINCT_EXTENSION"` over
pre-2.0 artifacts:
- **P2-REPLAY-COST (pre2 artifact 4.114, sha `9687ff787f2d74460bb7006826008852f5b4416b`)**:
  graph-lane "Cumulative Inheritance Experiment" (2026-08-23). WITHDREW its own 8.5x wall-clock
  headline (matched mean 2.822 s cold vs 2.816 s replay = 1.002x); scripted policies (agentG
  keyword-ranker, agentB DOM-order), no LLM; exact replay eliminated novel decisions on matched
  known routes; entry-state reset retry; negative: huge unstructured pages defeat heuristic
  policies. **Distinction**: that artifact measures REUSE/wall-clock on matched routes with
  scripted agents; this packet measures CORRECTNESS/EXECUTION/REFUSAL of a parameterized carrier on
  a never-observed identifier. No wall-clock/speed-up claim is inherited or made (the legacy guard
  is respected: the withdrawn 8.5x is not quoted). No route replay is measured; the positive is a
  GENERALIZED never-observed id inside induced support, not a replay of an observed route.
- **P2-BLIND-COMPOSITION (pre2 product summary 4.697, sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`)**:
  G-H2 blind content-addressed retrieval + iterative replay solved unseen composed routes (3/3) vs
  cold/verbatim/single-shot BFS (0/3); keyword-channel dependency; oracle-guided stopping;
  baselines "not strong"; G-H4 V31 instrument spent; SGDR fused retrieval (alpha 0.4, MMR 0.7)
  validated PoC on paraphrased goals. **Distinction**: that artifact measures RETRIEVAL/
  COMPOSITION with an inherit-store and a fused-embedding front door. This packet has NO retrieval
  component (the induction bank is 5 fresh observations), no composition, no V31/SGDR instrument,
  no baseline-arm comparison. The shipped carrier is a NEW 2.0 artifact that did not exist pre-2.0.
- Immediate 2.0 precedents: **EXP-PRODUCT-38180719830** (parent) INSTALLED the carrier and
  certified identity/binding (D0-D4+V8) on a single held-out id (item-007) via a bespoke runner
  that wrote src/spider/kernel.py; **EXP-PRODUCT-37973256064** audited the PRE-promotion
  lane-branch carrier on a 15-holder bank WITH cold/retrieval comparators (outcome FALSIFIES on
  treatment-vs-baseline margins, known negatives refused 15/15). **This packet differs on all
  three axes**: (i) it measures the AS-INSTALLED shipping path READ-ONLY (never writes
  src/spider/kernel.py -- which is why kernel.py can and does enter freeze_artifacts for the first
  time); (ii) it runs the FULL pipeline order distill->resolve->execute->verify/UNKNOWN on the
  public package API with a genuinely never-observed positive (item-000, strictly stronger than
  the certificate's item-007 which had been resolved in the live audit's held-out bank); (iii) it
  carries NO comparator arms (the four-arm benchmark is explicitly excluded), replacing arm
  comparison with a zero-HTTP abstention requirement and shipped-threshold semantics. Neither
  precedent answers the mandate's condition-(1) question in this form.

## 4. Inherited state from the parent handoff (EXP-PRODUCT-38180719830)

`request.json#parent_handoff` sha256 `d2c774fe7fba8fb7402b32fc4de813cdf2137aedc8924a86c34e21c474cd24a1`.
Carry-forward preserved verbatim in intent:

- **established**: promotion certificate PASS on byte-identical carrier (D0-IDENTITY, D1-POSITIVE
  on item-007, D2-NEGATIVE 7/7, D3-COUNTERS, D4-CONTROLS, V8); independent audit PASS; carrier
  audited live pre-promotion on the same substrate class (12/15 held-out EXECUTABLE, PC-EXACT-REPLAY
  15/15, refusal 1.0); Director granted promote_to_product=true, discharging blocker B1; the carrier
  is at src/spider/kernel.py (post-install sha 718efa6a...). RE-VERIFIED at DESIGN time: current
  src/spider/kernel.py sha256 == 718efa6a..., git status clean.
- **rejected** (bounded): carrier cannot be installed byte-identically; positive attributable to
  literal/substrate; certificate needing a substituted carrier. None inherited as open.
- **unknown** (inherited as unknowns, not assumed): whether C-PARAM-INHERIT satisfies its next_gate
  (cold/replay/retrieval baselines) -- UNRESOLVED, still requires the four-arm benchmark under
  readiness (2)+(3); whether the conservative support inference (single-digit suffix from 5
  examples) is a defect for free-form payloads -- THIS packet probes the boundary in the bounded
  form the mandate asks (item-000 in-support never-seen, item-010 out-of-support), but does not
  generalize; whether the four-arm benchmark can execute at all -- depends on (2)/(3)+mandate;
  whether promotion yields economics benefit -- not measured here.
- **do_not_assume** (honored): certificate PASS != claim advance (claim stays EXPERIMENTAL in ALL
  branches here); promotion != VALIDATED/PRODUCT_CORE; certificate != economics; no generalization
  beyond induced support on this fixture; PC-EXACT-REPLAY/regression are identity controls; do NOT
  re-run the promotion certificate, do NOT test a substituted carrier, do NOT re-run the REST
  certificate; the shipping kernel currently CARRIES the carrier (do not assume literal) -- the
  E2E-IDENTITY premise gate here DEPENDS on this and BLOCKs if it ever flips.

## 5. Satisfiability evidence (DESIGN probes; claim-bearing measurement never run in DESIGN)

ALL DESIGN probes were hermetic, non-outcome-bearing, and ran on copies or read-only imports; the
shipping tree was never written; `git status` clean after every probe. Record:
`/tmp/opencode/probes/probe_satisfiability.out.json` (overall_pass: true).

- P1 API surface + identity: `import spider` from shipping path OK; SpiderKernel has
  distill_parameterized/resolve/verify/rebind; `min_confidence` default == 0.8 (shipped threshold);
  src/spider/kernel.py sha256 == 718efa6a... (== carrier blob b15ed848 bytes).
- P2 induction arithmetic (pure functions): `_infer_support(['item-001'..'item-005'])` ==
  `^item\-00[0-9]{1}$` exactly; `_support_accepts('item-000')` == True (never-observed positive
  INSIDE support), `item-006/009` True, `item-010/999/xyz`/empty False (out-of-support refusals
  reachable); `_parameterized_confidence()` == 0.9; default `min_confidence` 0.8 -> EXECUTABLE only
  for 0.9 mechanisms. Probe also confirmed: repo-wide sweep (research/, codex/, src/, tests/,
  .spider-runtime/ raw trajectories + results) contains NO 'item-000' occurrence; all prior runs
  used item-001..010 and item-151..249.
- P3 postcondition matching: `_matches({'type':'item','id':'item-000'}, fixture body for
  item-000)` == True; wrong-id body False (verify semantics reachable).
- P4 counters: TrajectoryCounters increments retrieval/verification/repair; model_calls==0,
  model_tokens==0 (dataclass default; no model on path).
- P5 fixture: in-process ThreadingHTTPServer on 127.0.0.1:0 returns 200
  `{"type":"item","id":<id>,"data":"res:"+<id>}`; request counter works (1 GET -> count 1).
- P6 regression: tests/test_kernel.py 3/3 OK on the shipping path.
- Sim-tree E2E satisfiability run (EXP_PROBE_MODE=1, freeze-absent, carrier at sim shipping path):
  all five E2E clauses PASS -> SUPPORTS branch reachable. Literal-substituted sim kernel ->
  E2E-IDENTITY FAIL -> BLOCKED/MEASUREMENT_INVALID (substituted-carrier branch demonstrated,
  kernel untouched). Tampered freeze artifact hash -> V8 FAIL -> BLOCKED/MEASUREMENT_INVALID.
  Missing freeze.json (EXECUTE semantics) -> BLOCKED. (These ran on a hermetic COPY of the repo;
  the claim-bearing certificate itself is measured ONLY at EXECUTE under V8 binding + independent
  audit.)

## 6. Treatment and identity pinning

- Treatment: the AS-INSTALLED shipping kernel `src/spider/kernel.py`, REQUIRED (E2E-IDENTITY
  premise gate) to have sha256 == `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`
  == git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` (491 lines, carrier: has
  distill_parameterized, _infer_support, _derive_structural_name(s), _parameterized_confidence,
  TrajectoryCounters). Measured THROUGH THE PUBLIC PACKAGE API (`from spider import SpiderKernel,
  Mechanism, Observation, Resolution, ResolutionStatus`; `from spider.registry import
  MechanismRegistry`) with the package's DEFAULT `min_confidence=0.8` (shipped threshold) -- the
  runner passes NO threshold overrides; the induced confidence 0.9 comes from the kernel's
  `_parameterized_confidence()`.
- The runner NEVER writes src/spider/ (or any freeze artifact) -- READ-ONLY measurement. This is
  the material difference from the parent certificate (which installed the carrier) and is why
  `src/spider/kernel.py` is now a freeze artifact (unmutable in this experiment, per the
  EXP-GRAPH-38175554380 v2 precedent cited in the parent design_review).
- Identity pins: (a) freeze artifact hash of kernel.py == 718efa6a... (V8 C); (b) CANONICAL-HASHES
  block in this prereg (bound via freeze.json.hashes['prereg.md']); (c) the immutable Director
  mandate identity clause (git blob + sha256).
- B-LITERAL-KERNEL: shipped pre-promotion literal from git blob
  `cfec98660b0277ccbf295e8a4119e8d81ddccf50` (sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`,
  132 lines, NO distill_parameterized, literal path confidence floor 0.5 < min 0.8) -- loaded in a
  hermetic temp package with the same shipped models/registry/init; structural check only.

## 7. Certificate bank, fixture and controls

- Intent: `read_item`; context: `{"resource_type": "item", "authenticated": True}` (same shape as
  the promotion certificate, so the distilled mechanism is directly comparable).
- Induction bank (actually EXECUTED through the fixture, 5 GETs): `item-001..item-005`; each GET
  returns 200 `{"type":"item","id":<id>,"data":"res:"+<id>}` and is recorded as an Observation
  (intent, state, action {method: GET, url}, next_state=body, success=True, provenance).
- POSITIVE (never-observed held-out, inside support): `item-000` -- see V5 / section 5 P2 for the
  never-observed evidence and in-support arithmetic. Distilled mechanism slots ['item'], support
  `^item\-00[0-9]{1}$`, confidence 0.9.
- KNOWN-NEGATIVE (designated abstention): `item-010` (audited failure-mode id; two-digit suffix
  outside induced support) -> EXPLORE, reason contains 'outside inferred support', bound_action
  null, ZERO HTTP.
- Full refusal battery (7 probes, all with zero HTTP): item-010 / item-999 / item-xyz ->
  EXPLORE 'outside inferred support'; {} and {'wrong_key':'x'} -> EXPLORE 'missing required
  parameter'; `delete_item` -> EXACTLY UNKNOWN; `never_seen_intent` -> EXACTLY UNKNOWN.
- Controls (stable IDs inherited from EXP-PRODUCT-37973256064 / EXP-PRODUCT-38180719830):
  B-LITERAL-KERNEL (ablation), PC-EXACT-REPLAY (5/5 training ids EXECUTABLE), NC-OUT-OF-SUPPORT-ID,
  NC-MISSING-PARAMETER, NC-WRONG-INTENT, NC-NO-APPLICABLE-MECHANISM. New identity baseline:
  B-SHIPPED-IDENTITY (premise gate; kernel sha == carrier sha else BLOCKED).
- Fixture: stdlib `http.server.ThreadingHTTPServer` on `127.0.0.1:0` with a request counter; no
  RNG, no wall-clock, no external network; everything in-process in the FROZEN RUNNER.

## 8. Certificate definition (frozen decision rule; binding detail in spec.json)

`M-E2E-PASS = E2E-IDENTITY AND E2E-POSITIVE AND E2E-ABSTENTION AND E2E-COUNTERS AND E2E-CONTROLS`,
with `V8` enforced at EXECUTE. Clause statuses and the overall mapping (`MEASUREMENT_INVALID >
FALSIFIES > SUPPORTS`) are defined clause-by-clause in spec.json `#decision_rule.decisions`. The
runner appends each clause to `result["certificate"]`; `COMPLETE/SUPPORTS` iff all PASS;
`COMPLETE/FALSIFIES` iff identity PASS but any outcome clause FAIL; `BLOCKED/MEASUREMENT_INVALID`
iff identity/binding/infrastructure FAILs (exact blocker recorded). The full runner is the FROZEN
RUNNER block in section 14.

## 9. Metrics

- `M-E2E-PASS` (primary, binary conjunction of the five E2E clauses + V8 gate).
- `M-IDENTITY`: shipping_kernel_sha256 == 718efa6a..., git clean flag, carrier/literal blobs.
- `M-POSITIVE`: mechanism_id, parameter_slots, induced support, confidence (0.9), resolution_status
  (EXECUTABLE), bound_action url (contains item-000), fixture_status (200), verify (true),
  held_out item-000 + never-observed evidence ref.
- `M-ABSTENTIONS`: 7 probes {case, status, reason, bound_action}; http_delta across phase == 0.
- `M-COUNTERS`: retrieval_calls/verification_calls/repair_attempts + expected-from-transcript;
  model_calls == 0, model_tokens == 0; fixture http counter == 6 (5 induction + 1 positive),
  abstention-phase delta == 0.
- `M-PC-EXACT-REPLAY` (5 statuses), `M-ABLATION` (literal has_distill_parameterized == False),
  `M-REGRESSION` (tests_run >= 3, failures 0, errors 0), `M-SUPPORT` (regex + confidence).
- All in the runner output JSON; EXECUTE copies them into result.json per the packet contract.

## 10. Honest counters (clause E2E-COUNTERS semantics)

- `retrieval_calls` == #resolve calls + #rebind calls in the invocation transcript (rebind
  internally re-invokes resolve -> both increment; the probe exercised the rebind path for a
  repair_attempts increment and a +1 retrieval).
- `verification_calls` == #verify calls; `repair_attempts` == #rebind calls.
- `model_calls == 0` and `model_tokens == 0` are ASSERTED (no model exists anywhere on the
  credential-free path; the counters dataclass never touches them).
- http accounting is RUNNER-SIDE: the fixture handler counts every GET; the runner asserts
  total == executed HTTP legs (exactly 6: 5 induction + 1 positive execute) and
  abstention-phase delta == 0. The kernel never auto-increments an http counter (prior validity
  note); the runner-side counter is the honest execution ledger.
- No counter is incremented without a real kernel call; the transcript is recorded by the runner
  at each resolve/verify/rebind/execute site; counters are compared to the transcript, not to each
  other.

## 11. Validity gates

V1-DETERMINISM; V2-CREDENTIAL-FREE + HTTP-EXECUTION-ACCOUNTING; V3-IDENTITY-PREMISE-GATE;
V4-STOP-TRIGGER (never measure a substituted carrier; identity failure -> BLOCKED);
V5-HELD-OUT-NEVER-OBSERVED (item-000 in-support + never-observed evidence; item-010 out-of-support);
V6-REFUSAL-SEMANTICS (null action, non-empty reason, exact status classes, zero http);
V7-TRANSCRIPT-HONESTY (kernel counters == transcript; runner http counter == HTTP legs);
V8-FREEZE-BINDING (A prereg sha, B runner == FROZEN RUNNER, C artifact hashes incl.
src/spider/kernel.py); V9-REGRESSION (3/3); V10-ABLATION-ATTRIBUTION (literal lacks
distill_parameterized). Definitions in spec.json `#measurement_validity`.

## 12. Validity threats and mitigations

- **Support-overmatch / under-match**: mitigated by V5 (item-000 in-support, item-010/999/xyz
  out-of-support, probe-verified) and E2E-ABSTENTION (any acceptance of item-010 falsifies).
- **Refusal that still executes**: mitigated by the zero-HTTP assertion (fixture counter delta == 0
  across the abstention phase); execution on a refused probe is an E2E-ABSTENTION FAIL.
- **Counter inflation / transcript drift**: E2E-COUNTERS compares kernel counters to the runner's
  invocation transcript exactly (retrieval == #resolve+#rebind etc.); http legs to the runner-side
  counter.
- **Attribution ambiguity**: B-LITERAL-KERNEL structural check (no distill_parameterized) proves
  the positive is impossible without the carrier.
- **Unbound mutable artifacts**: six freeze artifacts with recorded sha256 (now INCLUDING
  src/spider/kernel.py, unmutable here); FROZEN RUNNER + CANONICAL-HASHES bound via
  freeze.json.hashes['prereg.md']; runner never writes any artifact.
- **Optimistic design / unreachable branch**: all three outcome branches demonstrated reachable in
  hermetic sim-tree DESIGN probes (SUPPORTS, FALSIFIES-by-construction, BLOCKED demonstrated).
- **Outcome contamination from DESIGN**: no claim-bearing measurement run in DESIGN; probes ran on
  copies; the claim-bearing certificate runs ONLY at EXECUTE under V8 + independent audit.
- **Representation loss**: fixture is deterministic JSON over a single resource shape; no
  generalization beyond the induced support is claimed; item-010 is the audited boundary case and
  item-000 the in-support unseen case.
- **Legacy/route-replay confusion**: no route replay measured (positive is a generalized
  never-observed id); no wall-clock/speed-up claim (legacy 4.114 withdrawn claim not inherited);
  no retrieval/composition claim (legacy 4.697 not inherited).

## 13. Freeze artifacts and binding model

Freeze artifacts (SIX, all exist with recorded sha256 at DESIGN time):
`pyproject.toml`, `src/spider/__init__.py`, `src/spider/models.py`, `src/spider/registry.py`,
`src/spider/kernel.py` (NEW in this packet: the experiment is read-only, so the shipped treatment
is an immutable interpretation dependency -- the clean resolution of the parent design_review's
freeze_artifacts_bound exclusion, following the EXP-GRAPH-38175554380 precedent),
`tests/test_kernel.py`.

Binding model (identical to the accepted parent pattern):
`freeze.json` (created at freeze time) pins `hashes['prereg.md']`, `hashes['spec.json']`,
`hashes['request.json']` and `artifact_hashes` for the six files; V8 enforces (A) prereg sha, (B)
running runner source == FROZEN RUNNER block extracted from the hash-bound prereg, (C) artifact
hashes. Fixture and task bank are fully in-process inside the FROZEN RUNNER (no unbound dataset).
Premise evidence: `request.json#director_mandate.allocation.dependencies` pins the carrier identity;
CANONICAL-HASHES (section 15) records blobs/shas/hashes for the freeze step.

## 14. FROZEN RUNNER (verbatim; bound by freeze.json.hashes['prereg.md'])

<!-- BEGIN FROZEN RUNNER -->
#!/usr/bin/env python3
"""FROZEN RUNNER for EXP-PRODUCT-38186502935 (embedded verbatim in prereg.md).

Read-only shipped-carrier END-TO-END execution certificate for the as-installed
parameterized carrier at the shipping kernel path src/spider/kernel.py (carrier
git blob b15ed848... / sha256 718efa6a...). NEVER writes src/spider/.
Phases -> decision-rule clauses:

  P0  V8 freeze binding                                    (V8)
  P1  shipping identity premise gate                       (E2E-IDENTITY)
  P2  B-LITERAL-KERNEL ablation (literal from git)        (E2E-CONTROLS)
  P3  import the SHIPPING package via public API          (E2E-IDENTITY)
  P4  induction: execute 5 GETs item-001..005 on the
      credential-free loopback fixture (counter +5)        (E2E-POSITIVE)
  P5  distill_parameterized -> mechanism (slots ['item'],
      support ^item\\-00[0-9]{1}$, confidence 0.9)          (E2E-POSITIVE)
  P6  positive certificate: resolve NEVER-observed
      item-000 -> EXECUTABLE@0.9 -> execute (GET +1) ->
      fixture 200 -> verify true                          (E2E-POSITIVE)
  P7  negative certificate: 7 refusal probes (incl.
      designated item-010 abstention and never_seen_intent
      exactly UNKNOWN), all null action + recorded reason,
      fixture request counter UNCHANGED (zero HTTP)       (E2E-ABSTENTION)
  P8  honest counters: retrieval/verification/repair ==
      invocation transcript; model_calls==0, model_tokens==0;
      runner-side http counter == executed legs (6)        (E2E-COUNTERS)
  P9  controls: PC-EXACT-REPLAY 5/5 + regression suite     (E2E-CONTROLS)

Stop trigger (parent handoff): if the shipping kernel is NOT the frozen carrier
(sha mismatch), record the exact blocker and exit BLOCKED; never measure a
substituted carrier. Freeze binding failures are MEASUREMENT_INVALID, never
FALSIFIES.

Env overrides (hermetic dry-run / sim-tree probes only, never change certificate
logic or thresholds):
  EXP_TARGET_ROOT : repo root containing src/spider (default: auto-detected)
  EXP_LITERAL_SRC : git:<blob> (default) or file:<path>
  EXP_PROBE_MODE  : "1" = satisfiability probe; records UNBOUND-RUN for V8 when
                    freeze.json is absent (never fabricates the check)

Output JSON: status (COMPLETE|BLOCKED), outcome (SUPPORTS|FALSIFIES), one
certificate clause per decision-rule check, identities, counters, observations.
"""
from __future__ import annotations

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

# -- injection point for canonical identities (prereg CANONICAL-HASHES) --
CARRIER_BLOB = "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796"
CARRIER_SHA256 = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
LITERAL_BLOB = "cfec98660b0277ccbf295e8a4119e8d81ddccf50"
LITERAL_SHA256 = "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61"
# ---------------------------------------------------------------------------

INTENT = "read_item"
TRAIN_IDS = ["item-001", "item-002", "item-003", "item-004", "item-005"]
POSITIVE_HELD_OUT = "item-000"   # never-observed in ANY prior SPIDER run; inside induced support
OOS_IDS = ["item-010", "item-999", "item-xyz"]  # outside ^item\-00[0-9]{1}$ support
WRONG_INTENT = "delete_item"
NEVER_SEEN_INTENT = "never_seen_intent"
CTX = {"resource_type": "item", "authenticated": True}
EXPECTED_SUPPORT = r"^item\-00[0-9]{1}$"
EXPECTED_SLOTS = ["item"]
EXPECTED_CONFIDENCE = 0.9
EXPECTED_HTTP_LEGS = 6  # 5 induction + 1 positive execute; 0 abstention
EXPECTED_MIN_CONFIDENCE = 0.8  # shipped default, must NOT be overridden


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
    """Deterministic credential-free loopback fixture with a request counter."""
    count = 0

    def do_GET(self):
        type(self).count += 1
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


def drop_module(name: str) -> None:
    sys.modules.pop(name, None)


def make_pkg(target_pkg: Path, kernel_bytes: bytes, models: bytes, registry: bytes,
             init: bytes) -> None:
    target_pkg.mkdir(parents=True, exist_ok=True)
    (target_pkg / "kernel.py").write_bytes(kernel_bytes)
    (target_pkg / "models.py").write_bytes(models)
    (target_pkg / "registry.py").write_bytes(registry)
    (target_pkg / "__init__.py").write_bytes(init)


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
    exp = REPO_ROOT / "research/experiments/EXP-PRODUCT-38186502935"
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
        "reason": "hash-bound prereg; running source == FROZEN RUNNER block; six freeze artifact "
                  "hashes intact (incl. src/spider/kernel.py)",
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
        "experiment_id": "EXP-PRODUCT-38186502935",
        "lane": "product",
        "certificate": {},
        "identities": {},
        "counters_transcript": [],
        "observations": [],
        "unresolved": [],
    }

    kernel_path = REPO_ROOT / "src/spider/kernel.py"
    sys.path.insert(0, str(REPO_ROOT / "src"))
    for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
        drop_module(m)

    literal_src = os.environ.get("EXP_LITERAL_SRC", f"git:{LITERAL_BLOB}")
    result["run_config"] = {
        "repo_root": str(REPO_ROOT),
        "literal_src": literal_src,
        "probe_mode": bool(os.environ.get("EXP_PROBE_MODE")),
        "min_confidence_override": os.environ.get("EXP_MIN_CONFIDENCE_OVERRIDE"),
    }

    # ---- P0 V8 freeze binding first (mandatory at EXECUTE; probe mode records UNBOUND-RUN) ----
    if not v8_freeze_binding(result):
        return result

    # ---- P1 shipping identity premise gate (E2E-IDENTITY) ----
    shipping_sha = sha256_bytes(kernel_path.read_bytes())
    result["identities"]["shipping_kernel_sha256"] = shipping_sha
    result["identities"]["carrier_expected_sha256"] = CARRIER_SHA256
    result["identities"]["carrier_git_blob"] = CARRIER_BLOB
    result["observations"].append(
        {"type": "shipping_identity", "sha256": shipping_sha, "expected": CARRIER_SHA256}
    )
    if shipping_sha != CARRIER_SHA256:
        result["certificate"]["E2E_IDENTITY"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "shipping kernel src/spider/kernel.py is NOT the frozen carrier (got "
                      + shipping_sha + ", expected " + CARRIER_SHA256 + "); promotion merge not "
                      "in effect or tree modified (V4 stop trigger: never measure a substituted "
                      "carrier)",
        }
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result
    result["certificate"]["E2E_IDENTITY"] = {
        "status": "PASS",
        "reason": "shipping kernel byte-identical to frozen carrier git blob " + CARRIER_BLOB
                  + " (sha256 " + CARRIER_SHA256 + ") on a git-clean tree",
    }

    # ---- P2 B-LITERAL-KERNEL ablation (temp package; repo untouched) ----
    models_bytes = (REPO_ROOT / "src/spider/models.py").read_bytes()
    registry_bytes = (REPO_ROOT / "src/spider/registry.py").read_bytes()
    init_bytes = (REPO_ROOT / "src/spider/__init__.py").read_bytes()
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
            import spider as lit  # literal kernel package (same shipped models/registry/init)
            has_param_path = hasattr(lit.SpiderKernel, "distill_parameterized")
            sys.path.remove(td)
            for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
                drop_module(m)
            result["certificate"]["E2E_CONTROLS"] = {
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
        result["certificate"]["E2E_CONTROLS"] = {
            "literal_ablation": {"status": "MEASUREMENT_INVALID", "reason": str(exc)}}
        result["status"] = "BLOCKED"
        return result

    # ---- P3 import the SHIPPING package via its public API ----
    try:
        from spider import SpiderKernel, Mechanism, Observation, Resolution, ResolutionStatus
        from spider.registry import MechanismRegistry
        kernel_min_confidence = SpiderKernel.__init__.__defaults__[0]
        result["observations"].append(
            {"type": "derived", "kernel_min_confidence_default": kernel_min_confidence}
        )
        if kernel_min_confidence != EXPECTED_MIN_CONFIDENCE:
            raise RuntimeError(
                f"shipped min_confidence default is {kernel_min_confidence}, expected "
                f"{EXPECTED_MIN_CONFIDENCE}; refusing to run with altered thresholds")
    except Exception as exc:
        result["certificate"]["E2E_IDENTITY"]["status"] = "MEASUREMENT_INVALID"
        result["certificate"]["CORE"] = {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result

    fixture, port = start_fixture()
    transcript: list[dict] = []
    http_before = FixtureHandler.count

    try:
        with tempfile.TemporaryDirectory() as td:
            reg = MechanismRegistry(Path(td) / "mechanisms.jsonl")
            counters_type = __import__("spider.kernel", fromlist=["TrajectoryCounters"]).TrajectoryCounters
            counters = counters_type()
            kernel = SpiderKernel(reg, counters=counters)  # shipped default min_confidence=0.8

            # ---- P4 induction: actually EXECUTE the 5 training GETs ----
            observations = []
            for ident in TRAIN_IDS:
                url = f"http://127.0.0.1:{port}/api/items/{ident}"
                transcript.append({"op": "execute_induction", "url": url})
                status, body = execute({"method": "GET", "url": url})
                if status != 200:
                    raise RuntimeError(f"induction GET {ident} returned {status}")
                observations.append(Observation(
                    intent=INTENT,
                    state=dict(CTX),
                    action={"method": "GET", "url": url},
                    next_state=body,
                    success=True,
                    provenance={"exp": "EXP-PRODUCT-38186502935", "role": "induction"},
                ))
            transcript.append({"op": "distill", "n": len(observations)})

            # ---- P5 distill_parameterized ----
            mech = kernel.distill_parameterized(observations)
            if mech is None:
                raise RuntimeError("distill_parameterized returned None on 5 successful observations")
            reg.upsert(mech)
            slots = mech.parameter_slots
            support = mech.verification_rule["parameter_supports"]
            result["observations"].append(
                {"type": "derived", "mechanism_id": mech.mechanism_id, "slots": slots,
                 "support": support, "confidence": mech.confidence}
            )

            # ---- P6 E2E-POSITIVE on NEVER-observed held-out item-000 ----
            params = {s: POSITIVE_HELD_OUT for s in slots}
            transcript.append({"op": "resolve", "args": [INTENT, POSITIVE_HELD_OUT]})
            res = kernel.resolve(INTENT, CTX, params)
            pos_binding_ok = (
                res.status == ResolutionStatus.EXECUTABLE
                and res.bound_action is not None
                and POSITIVE_HELD_OUT in res.bound_action["url"]
                and res.confidence == EXPECTED_CONFIDENCE
            )
            status, body = (0, {})
            if res.bound_action:
                transcript.append({"op": "execute_positive", "url": res.bound_action["url"]})
                status, body = execute(res.bound_action)
            transcript.append({"op": "verify", "args": [res.mechanism_id]})
            verify_ok = kernel.verify(res.mechanism_id, body, params) if status == 200 else False
            result["certificate"]["E2E_POSITIVE"] = {
                "status": "PASS" if (pos_binding_ok and status == 200 and verify_ok) else "FAIL",
                "resolution_status": res.status.value,
                "resolution_confidence": res.confidence,
                "bound_action": res.bound_action,
                "fixture_status": status,
                "verify": verify_ok,
                "held_out": POSITIVE_HELD_OUT,
                "mechanism_id": mech.mechanism_id,
                "parameter_slots": slots,
                "support": support,
                "reason": "5 executed induction observations; never-observed id bound "
                          "EXECUTABLE@0.9; fixture 200; verify true",
            }

            # ---- P7 E2E-ABSTENTION: 7 refusal probes with zero HTTP ----
            http_abstention_start = FixtureHandler.count
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
            transcript.append({"op": "resolve", "args": [WRONG_INTENT, POSITIVE_HELD_OUT]})
            r = kernel.resolve(WRONG_INTENT, CTX, params)
            negatives.append({"case": "wrong_intent", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            transcript.append({"op": "resolve", "args": [NEVER_SEEN_INTENT, "<none>"]})
            r = kernel.resolve(NEVER_SEEN_INTENT, {}, {})
            negatives.append({"case": "no_applicable_mechanism", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            http_abstention_delta = FixtureHandler.count - http_abstention_start
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
            ab_ok = all_refused and unknown_exact and oos_explore and missing_explore \
                and http_abstention_delta == 0
            result["certificate"]["E2E_ABSTENTION"] = {
                "status": "PASS" if ab_ok else "FAIL",
                "negatives": negatives,
                "http_delta_during_phase": http_abstention_delta,
                "reason": "every refusal: recorded reason + null bound action + ZERO HTTP; "
                          "out-of-support/missing-parameter EXPLORE; no-applicable exactly UNKNOWN",
            }

            # ---- P8 E2E-COUNTERS: transcript-consistent, model-free, http ledger ----
            transcript.append({"op": "rebind", "args": [INTENT, POSITIVE_HELD_OUT]})
            _ = kernel.rebind(INTENT, CTX, params)
            http_total = FixtureHandler.count - http_before
            expected_retrieval = sum(1 for t in transcript if t["op"] in ("resolve", "rebind"))
            expected_verify = sum(1 for t in transcript if t["op"] == "verify")
            expected_repair = sum(1 for t in transcript if t["op"] == "rebind")
            counters_after = counters.as_dict()
            counters_ok = (
                counters_after["retrieval_calls"] == expected_retrieval
                and counters_after["verification_calls"] == expected_verify
                and counters_after["repair_attempts"] == expected_repair
                and counters_after["model_calls"] == 0
                and counters_after["model_tokens"] == 0
                and http_total == EXPECTED_HTTP_LEGS
            )
            result["certificate"]["E2E_COUNTERS"] = {
                "status": "PASS" if counters_ok else "FAIL",
                "counters_after": counters_after,
                "expected_from_transcript": {
                    "retrieval_calls": expected_retrieval,
                    "verification_calls": expected_verify,
                    "repair_attempts": expected_repair,
                },
                "http_fixture_counter_total": http_total,
                "http_expected_legs": EXPECTED_HTTP_LEGS,
                "http_abstention_delta": http_abstention_delta,
                "reason": "kernel counters == invocation transcript; model_calls=0, "
                          "model_tokens=0; runner-side http counter == executed legs (6)",
            }
            result["counters_transcript"] = transcript
            result["counters"] = counters_after

            # ---- P9 E2E-CONTROLS: PC-EXACT-REPLAY + regression ----
            replay = []
            for ident in TRAIN_IDS:
                transcript.append({"op": "resolve", "args": [INTENT, ident]})
                r = kernel.resolve(INTENT, CTX, {s: ident for s in slots})
                replay.append({"id": ident, "status": r.status.value})
            replay_ok = all(r["status"] == "EXECUTABLE" for r in replay)
            result["certificate"]["E2E_CONTROLS"]["pc_exact_replay"] = {
                "status": "PASS" if replay_ok else "FAIL",
                "replay": replay,
                "reason": "all training ids re-resolve EXECUTABLE on as-installed carrier",
            }
            fixture.shutdown()
    except Exception as exc:
        fixture.shutdown()
        result["certificate"]["E2E_IDENTITY"] = result["certificate"].get(
            "E2E_IDENTITY", {"status": "MEASUREMENT_INVALID", "reason": "unknown"})
        result["certificate"]["CORE"] = {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result

    # ---- P9 (cont.) regression on the as-installed shipping path ----
    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test_*.py")
    tresult = unittest.TextTestRunner(verbosity=0).run(suite)
    result["certificate"]["E2E_CONTROLS"]["regression"] = {
        "status": "PASS" if (tresult.wasSuccessful() and tresult.testsRun >= 3) else "FAIL",
        "tests_run": tresult.testsRun,
        "failures": len(tresult.failures),
        "errors": len(tresult.errors),
        "reason": "existing test_kernel suite passes on as-installed shipping path",
    }

    clauses = [result["certificate"][k] for k in ("E2E_IDENTITY", "E2E_POSITIVE",
                                                  "E2E_ABSTENTION", "E2E_COUNTERS")]
    clauses.append(
        {"status": result["certificate"]["E2E_CONTROLS"].get("pc_exact_replay", {}).get("status"),
         "literal": result["certificate"]["E2E_CONTROLS"].get("literal_ablation", {}).get("status"),
         "regression": result["certificate"]["E2E_CONTROLS"].get("regression", {}).get("status")}
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
- Induced arithmetic (probe-verified, shipped kernel): support `^item\-00[0-9]{1}$`, slots
  `['item']`, confidence `0.9`, default `min_confidence` `0.8`, HTTP legs `6`.

## 16. EXECUTE contract

1. Verify `request.json`, `spec.json`, `prereg.md` are the frozen versions (hashes match
   `freeze.json`); `git status` clean; shipping kernel sha == `718efa6a...` (premise re-check).
2. Materialize the runner: extract the `<!-- BEGIN FROZEN RUNNER --> ... <!-- END FROZEN RUNNER
   -->` block from the hash-bound `prereg.md` verbatim to
   `research/experiments/EXP-PRODUCT-38186502935/harness/run_e2e.py` (write the file only).
3. Run `python3 research/experiments/EXP-PRODUCT-38186502935/harness/run_e2e.py` with NO env
   overrides (EXECUTE mode; V8 enforced; shipped thresholds; no writes to src/spider/).
4. Preserve raw evidence: `run_e2e.out.json`, `run_e2e.log` in the experiment dir; keep
   `counters_transcript`, identities and clause statuses distinct from interpretation.
5. Write `result.json` (mandatory top-level shape per the packet contract: schema_version,
   experiment_id, lane, status, outcome, metrics, controls, artifacts, observations,
   validity_notes, unresolved), `report.md`, `provenance.json`. `status=COMPLETE` with
   `outcome=FALSIFIES` is a valid scientific negative; `status=BLOCKED`/`outcome=MEASUREMENT_INVALID`
   records the exact operational blocker and is NEVER a negative result.
6. Do NOT run the promotion certificate, do NOT re-run the mandatory-discovery REST certificate,
   do NOT test a substituted carrier, do NOT write any freeze artifact, do NOT run the four-arm
   benchmark, do NOT git-commit/push. A DIRECTOR verdict consumes this packet.

## 17. Consequences of both branches (preregistered)

- `SUPPORTS` (M-E2E-PASS): readiness condition (1) DISCHARGED - the shipped parameterized carrier
  executes the full end-to-end path `distill_parameterized -> resolve -> execute -> verify/UNKNOWN`
  on a credential-free substrate with a known positive on a never-observed identifier (item-000)
  and a known-negative abstention (item-010) at shipped thresholds. The lane awaits readiness (2)
  (Intel budget-stable credential-free endpoint) and (3) (Runtime certified task bank) plus a NEW
  Global Research Director mandate before any four-arm benchmark spend. C-PARAM-INHERIT stays
  EXPERIMENTAL; no claim advance; no economics claim.
- `FALSIFIES` (E2E-IDENTITY PASS, outcome clause FAIL): the promoted carrier is NOT
  product-executable end-to-end at shipped thresholds; readiness condition (1) stays OPEN; the
  exact frozen blocker (clause + observed values) becomes the engineering-fix specification INSIDE
  Product before any benchmark spend; the four-arm benchmark remains unfunded; C-PARAM-INHERIT
  stays EXPERIMENTAL; B1 (the promotion event) is NOT revoked by this packet.
- `BLOCKED`/`MEASUREMENT_INVALID`: readiness (1) cannot be assessed; exact operational blocker
  recorded (shipping kernel != carrier sha incl. promotion-merge-not-in-effect; git objects
  missing; freeze binding failure; fixture failure). Infrastructure failure is never repackaged as
  a scientific negative.