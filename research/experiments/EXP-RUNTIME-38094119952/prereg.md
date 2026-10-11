# EXP-RUNTIME-38094119952 preregistration

Lane: runtime. Claim: `C-MEAS-VALID`. Design contract version: 2.
Binding direction: `request.json.director_mandate` (action CONTINUE, target claim `C-MEAS-VALID`, parent handoff `EXP-RUNTIME-37973247935` SUPERSEDED: the out-of-surface transfer question is explicitly NOT re-designed here).

This is an INSTRUMENT / CERTIFICATE experiment. It does not test the inheritance economics of `C-PARAM-INHERIT` or `C-LLM-INHERIT`; it tests whether a credential-free substrate can be certified, arithmetically and before freeze, to have non-ceiling dynamic range (blocker B2). No outcome-bearing measurement is performed in DESIGN.

---

## 1. Motivation and inherited state

SPIDER's central unresolved question — does a real external LLM agent benefit from inherited procedures / parameterized mechanisms at lower fully-loaded cost per successful task — is gated by three verified blockers. B2 (Runtime's target) is: no non-ceiling task bank. Two product experiments established the bounded substrate-class negative:

- `EXP-PRODUCT-37989728440` (COMPLETE / FALSIFIES): on a credential-free deterministic REST substrate, B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED both performed the same mandatory session/resource/endpoint discovery and the deterministic server accepted the discovered in-support values, so both solved every task at novelty 0.5 and 0.75 (`success_rate = 1.0`). The dynamic-range certificate was therefore unsatisfiable on that class. The same packet also recorded a freeze-gate defect: `scripts/freeze_experiment.py` did not enforce a `dynamic_range_certified` key, so the packet froze with a false certificate.
- `EXP-PRODUCT-37973256064` and `EXP-PRODUCT-37982016598` hit the same 1.0 cold/retrieval ceiling.

The bounded negative closes the **symmetric mandatory-discovery** class. The Director mandate asks whether a **materially different** class — an **asymmetric-discovery** bank whose discovery cost cannot be amortized by any stateless policy but can be amortized by a session-carrying mechanism — can be certified arithmetically before freeze. That is the object of this experiment.

The repeated invalidation of this question by the same missing prerequisite (an unattainable pre-freeze certificate) is treated as a design/control-plane defect to repair once: ADB-v7 changes the substrate class (asymmetric carry chain), embeds the calibration sibling that proves the certificate is not constant-TRUE, and states the bounded-negative consequences explicitly. This is not a re-run of the mandatory-discovery deterministic REST class.

## 2. Question

Can a non-degenerate asymmetric-discovery task bank (ADB-v7) be certified arithmetically in DESIGN before freeze — cold re-derivation and a retrieval-shaped comparator demonstrably below the success ceiling at high residual novelty, a real treatment/comparator behavioural distinction, honest per-condition counters (`http_requests + retrieval_calls + verification_calls + repair_attempts`), and a preregistered contamination/dynamic-range certificate calibrated against a known-degenerate sibling — and be delivered as a reusable substrate that unblocks the flagship inheritance benchmark (blocker B2)? If the certificate is unsatisfiable on every credential-free substrate class tested, DESIGN records a bounded substrate-class negative and does NOT freeze.

## 3. Hypothesis

A credential-free deterministic localhost REST bank is a certified non-degenerate instrument iff its discovery structure is a session-scoped carry chain such that (a) each session begins with a fixed bootstrap (root, hub, boot/1..5 = 7 requests; `/boot/5` serves the session manifest), and each required role is resolved by a fixed 3-step chained protocol `GET /disc/<role>/<step>` where each step requires the previous step's value, so no policy can resolve a role in fewer than 3 requests per task without persisting the resolved token across tasks; (b) the hidden-role count grows with novelty as `h(n) = 8n`; (c) the task spec is handed to every arm as task input (not an HTTP request); (d) the published per-task integer HTTP budget `B(n) = {11,15,16,18}` is non-decreasing; and (e) the same certificate predicate is calibrated against a same-transport query-answerable sibling `CC-DEGENERATE`.

Under the frozen declaration the arithmetic predicts cold nominal server cost `{8,14,20,26}` and retrieval nominal server cost `{6,12,18,24}` (`{9,15,21,27}` including 3 local index probes) exceed `B(n)` at high novelty, while treatment costs `{9,7,7,7}` and the positive control `{8,10,12,14}` fit every level. The certificate therefore returns TRUE for ADB-v7 and FALSE for CC-DEGENERATE.

## 4. Substrate declaration (frozen identity)

Python 3.12 standard library only; `http.server.ThreadingHTTPServer` on `127.0.0.1:<ephemeral>`; `urllib.request`, `html.parser`, `json`, `hashlib`, `random.Random(SEED)`. No browser, no external network, no credentials, no cookies, no model calls. The site and arms import no pre-existing Runtime module.

- Families `F = 2` (F1, F2); `3` test sessions per family; `4` tasks per session (one per novelty level `n in {0.0,0.25,0.5,0.75}`); `24` test tasks per arm; high-novelty stratum (`n >= 0.5`) `= 12` tasks per arm.
- Session manifest task order is the frozen ascending sequence `['0.0','0.25','0.5','0.75']`.
- `h(n) = 8n -> {0,2,4,6}` nested roles; each task requires the first `h(n)` roles of the ordered registry.
- Bootstrap: `root, hub, boot/1..5` (`7`) carry-chained requests; `/boot/5` serves the manifest.
- Discovery (ADB-v7): `GET /disc/<role>/1 -> N_r`; `GET /disc/<role>/2/<N_r> -> P_r` (iff `N_r` valid); `GET /disc/<role>/3/<P_r> -> T_r` and commits role `r` (iff `P_r` valid). `3` requests per role; unshortenable, session-scoped.
- Discovery (CC-DEGENERATE): `GET /answer/<role> -> T_r` (`1` request; query-answerable).
- `/verify` (`1` per task) confirms committed state is the goal.
- Budgets: `B = {0.0:11, 0.25:15, 0.5:16, 0.75:18}`; `B_deg = {0.0:11, 0.25:13, 0.5:15, 0.75:17}`. Hard per-task HTTP cap; an episode that would exceed it halts at exactly the cap, zero overrun, scored failure.
- Seed `20261010`.

**Reusable-substrate delivery (EXECUTE):** `research/runtime/adb_v7_bank.py`, `research/runtime/adb_v7_harness.py`, and `research/experiments/EXP-RUNTIME-38094119952/bank_manifest.json` (canonical digest of the fully-rendered bank), hashes recorded in `provenance.json` and `result.json.artifacts`.

### Session scope (per arm)

- `T-AMORT-REUSE`: one session per 4-task block (3 sessions/family x 2 families = 6 sessions); resolved roles persist within a session only.
- `B-COLD-RE-DERIVE`, `B-RETRIEVAL-SHAPED`, `PC-FOREKNOWN-SCHEMA`: one fresh per-task episode (24 independent episodes each; no cross-task state).
- `CC-DEGENERATE` comparators: per-task episodes on the 4-task calibration bank.

### 4.1 Canonical declaration object (gate I6 reference)

The object below is the frozen declaration. EXECUTE renders the site from it and emits a canonical declaration ECHO: the declaration record containing exactly this key set with the values the render actually used. EXECUTE serializes that echo with `json.dumps(obj, sort_keys=True, separators=(',',':'))`; gate I6 requires that serialization to equal the canonical serialization of THIS object. Concrete per-session secrets, nonces and carry values are deliberately EXCLUDED from the echo (they regenerate deterministically from `seed` and the declaration) and so does an ephemeral port value; the echo contains only the declaration keys shown here. Nothing outside this key set may enter the comparison.

```json
{
  "declaration_version": "ADB-v7",
  "seed": 20261010,
  "levels": ["0.0", "0.25", "0.5", "0.75"],
  "high_novelty_levels": ["0.5", "0.75"],
  "role_rule": "h(n) = round(8*n)",
  "hidden_roles": {"0.0": 0, "0.25": 2, "0.5": 4, "0.75": 6},
  "families": ["F1", "F2"],
  "sessions_per_family": 3,
  "tasks_per_session": 4,
  "session_task_order": ["0.0", "0.25", "0.5", "0.75"],
  "bootstrap_routes": ["/", "/hub", "/boot/1", "/boot/2", "/boot/3", "/boot/4", "/boot/5"],
  "manifest_route": "/boot/5",
  "tasks_route": "/tasks",
  "verify_route": "/verify",
  "discovery_routes": ["/disc/<role>/1", "/disc/<role>/2/<N_r>", "/disc/<role>/3/<P_r>"],
  "discovery_carry_rule": "step2 requires the step1 value N_r; step3 requires the step2 value P_r",
  "calibration_discovery_route": "/answer/<role>",
  "budgets": {"0.0": 11, "0.25": 15, "0.5": 16, "0.75": 18},
  "calibration_budgets": {"0.0": 11, "0.25": 13, "0.5": 15, "0.75": 17},
  "transport": {"scheme": "http", "host": "127.0.0.1", "port": "ephemeral-not-frozen"},
  "implementation": "python3.12-stdlib-only",
  "counter_partition": ["bootstrap_requests", "tasks_page_requests", "discovery_calls", "verification_calls"],
  "calibration_counter_partition": ["bootstrap_requests", "tasks_page_requests", "calibration_calls", "verification_calls"]
}
```

The `port` value is the literal string `ephemeral-not-frozen`: the OS-chosen port is deliberately NOT part of the declaration identity, so I6 is well-defined without depending on an unresolvable runtime value. `disc` carry values, role ordering within the first `h(n)` registry draw, and listing order are generated deterministically from `seed` and the declaration, so they are reproducible by the recomputation and do not need to be embedded value-by-value.

## 5. Cost model and counters

Per-task HTTP cost (server-logged, ground truth):

| arm | bootstrap | discovery | tasks page | verify | nominal http | fits B? |
|---|---|---|---|---|---|---|
| B-COLD-RE-DERIVE | 7 | 3h | 0 | 1 | 8+3h = {8,14,20,26} | {T,T,F,F} |
| B-RETRIEVAL-SHAPED (server) | 5 | 3h | 0 | 1 | 6+3h = {6,12,18,24} | {T,T,F,F} |
| T-AMORT-REUSE | 7 (session) | 3*(new roles) | 1 (session) | 1 | {9,7,7,7} | {T,T,T,T} |
| PC-FOREKNOWN-SCHEMA | 7 | 0 (tokens given) | 0 | 1 | 8+h = {8,10,12,14} | {T,T,T,T} |

`B-RETRIEVAL-SHAPED` additionally spends `3` local index probes per task, counted as `retrieval_calls` (NOT HTTP), always included in the fully-loaded total: total `= {9,15,21,27}` nominal, `{9,15,19,21}` truncated.

Counter partition (enforced, gate I4): `http_requests == bootstrap_requests + tasks_page_requests + discovery_calls + verification_calls` (ADB-v7; `calibration_calls` replaces `discovery_calls` on CC-DEGENERATE). `retrieval_calls` is recorded independently and never summed into `http_requests`. `repair_attempts <= 1` per task and is a flagged subset of `http_requests`. `latency_ms` and model tokens are prohibited as decision inputs (prior audit found latency to be instrument noise).

Predicted observed (truncated) ledger: cold http `{8,14,16,18}`; retrieval server http `{6,12,16,18}`, retrieval total `{9,15,19,21}`; treatment `{9,7,7,7}`. Predicted total gap vs treatment: cold `{-1,7,9,11}`, retrieval `{0,8,12,14}` (non-decreasing; strictly increasing at high novelty; high-novelty minimum `9` cold, `12` retrieval).

## 6. Arithmetic certificate (computed in DESIGN, no outcomes)

| level | h | B | cold nominal | retrieval nominal (total) | treatment | PC |
|---|---|---|---|---|---|---|
| 0.0 | 0 | 11 | 8 | 6 (9) | 9 | 8 |
| 0.25 | 2 | 15 | 14 | 12 (15) | 7 | 10 |
| 0.5 | 4 | 16 | 20 | 18 (21) | 7 | 12 |
| 0.75 | 6 | 18 | 26 | 24 (27) | 7 | 14 |

Predicted ADB-v7 success: cold `{T,T,F,F}`, retrieval `{T,T,F,F}`, treatment `{T,T,T,T}`, PC `{T,T,T,T}`.
High-novelty (n=12/arm): comparator `0/12` (point 0.0, Wilson 95% hi `0.242494`), treatment `12/12` (point 1.0, Wilson 95% lo `0.757506`) — disjoint.

Calibration sibling CC-DEGENERATE (same transport, query-answerable): cold `8+h = {8,10,12,14}` and retrieval total `9+h = {9,11,13,15}` both fit `B_deg = {11,13,15,17}` at every level, so both comparators reach the ceiling `4/4` and the certificate returns FALSE.

**Certificate predicate.** `CERT(class) = TRUE` iff for EVERY high-novelty `(family, level)` cell the nominal per-task cost of BOTH comparators strictly exceeds `B(level)` AND the nominal per-task cost of the treatment is `<= B(level)` AND the positive control is `<= B(level)`. `CERT(ADB-v7)=TRUE`; `CERT(CC-DEGENERATE)=FALSE`. A constant-TRUE or constant-FALSE predicate is therefore excluded by construction (I11).

`bank_manifest.json` will record the canonical digest of the fully-rendered bank, so the concrete rendered instance is bound post-hoc beyond the abstract declaration.

### 6.1 Canonical certificate object (gate I6 reference)

The object below is the frozen predicted certificate. EXECUTE recomputes the certificate from the rendered declaration (section 4.1) and gate I6 requires the canonical serialization `json.dumps(obj, sort_keys=True, separators=(',',':'))` of the recomputed certificate to equal the canonical serialization of THIS object. Nominal per-task costs (not the truncated observed ledger) are the certificate inputs.

```json
{
  "levels": ["0.0", "0.25", "0.5", "0.75"],
  "high_novelty_levels": ["0.5", "0.75"],
  "budgets": {"0.0": 11, "0.25": 15, "0.5": 16, "0.75": 18},
  "cold_nominal_http": {"0.0": 8, "0.25": 14, "0.5": 20, "0.75": 26},
  "retrieval_nominal_total": {"0.0": 9, "0.25": 15, "0.5": 21, "0.75": 27},
  "treatment_nominal_http": {"0.0": 9, "0.25": 7, "0.5": 7, "0.75": 7},
  "positive_control_nominal_http": {"0.0": 8, "0.25": 10, "0.5": 12, "0.75": 14},
  "predicted_success": {
    "B-COLD-RE-DERIVE": {"0.0": true, "0.25": true, "0.5": false, "0.75": false},
    "B-RETRIEVAL-SHAPED": {"0.0": true, "0.25": true, "0.5": false, "0.75": false},
    "T-AMORT-REUSE": {"0.0": true, "0.25": true, "0.5": true, "0.75": true},
    "PC-FOREKNOWN-SCHEMA": {"0.0": true, "0.25": true, "0.5": true, "0.75": true}
  },
  "certificate_ADB_v7": true,
  "calibration_class_CC_DEGENERATE": {
    "budgets": {"0.0": 11, "0.25": 13, "0.5": 15, "0.75": 17},
    "cold_nominal_http": {"0.0": 8, "0.25": 10, "0.5": 12, "0.75": 14},
    "retrieval_nominal_total": {"0.0": 9, "0.25": 11, "0.5": 13, "0.75": 15},
    "certificate": false
  }
}
```

## 7. Controls

| id | type | expected | failure consequence |
|---|---|---|---|
| PC-FOREKNOWN-SCHEMA | positive (solvability ceiling) | 24/24 overall, 12/12 high-novelty | I1 -> MEASUREMENT_INVALID (bank unsolvable) |
| NC-OOS-SCHEMA | known-negative refusal null | refuse 5/5 at manifest classification, 0 false accepts | I2 -> MEASUREMENT_INVALID |
| NC-BUDGET-TRUNCATION | budget-enforcement control | 6 under-funded episodes halt at exactly 10, zero overrun | I3 -> MEASUREMENT_INVALID |
| M-COUNTER-RECONCILE | counter honesty | mismatches = 0 | I4 -> MEASUREMENT_INVALID |
| M-REPAIR-TRANSIENT | repair honesty | `repair_attempts=1` charged, or honest failure; no hidden retry | I4 -> MEASUREMENT_INVALID |
| PC-EXACT-SESSION-REPLAY | determinism | 6 replayed sessions reproduce counters exactly | I5/I8 -> MEASUREMENT_INVALID |
| CC-DEGENERATE | certificate sensitivity | both comparators at ceiling 4/4 | I11 -> MEASUREMENT_INVALID |

NC-OOS-SCHEMA is a refusal control: a greedy fall-through resolver would commit a role or call `/verify` and is caught as a false accept.

## 8. Decision rule

Frozen thresholds: `success_ceiling_point = 0.95`; `high_novelty_threshold = 0.5`; `n_high = n_low = 12`; treatment high-novelty `k = 12` (Wilson lo `0.757506 >= 0.75`); interval disjointness (comparator k<=6: hi `0.746218 < 0.757506`); `min_high_novelty_gap = 8`; `cc_degenerate_comparator_min_high_point = 0.95`; counter mismatch `= 0`; OOS false accepts `= 0`; overrun `= 0`; `repair_attempts <= 1`.

Propositions `P1..P7`: P1/P2 comparator high-novelty below ceiling and disjoint below treatment; P3 treatment live at high and low novelty; P4 gap non-decreasing and strictly increasing at high novelty; P5 minimum high-novelty total gap `>= 8`; P6 observed matrix/ledger equals predicted; P7 certificate discriminates (TRUE on ADB-v7, FALSE on CC-DEGENERATE).

Ordered, total and disjoint mapping:
0. infrastructure/bring-up failure -> INCONCLUSIVE (never a scientific negative);
1. any evaluable integrity gate I1..I11 FAILED -> MEASUREMENT_INVALID;
2. integrity set holds: SUPPORTS iff `P1..P7`; else FALSIFIES iff `NOT(P1 AND P2)`; else MIXED.

F1/F3 (comparator at ceiling / treatment not live) map to `COMPLETE` with FALSIFIES/MIXED. F4 (integrity) maps to MEASUREMENT_INVALID. F2 (empty stratum / comparator-admitting budget) is a DESIGN failure, not a result.

## 9. Bounded-negative clause

If the DESIGN arithmetic shows `CERT = FALSE` on ADB-v7, on CC-DEGENERATE, and on every other credential-free substrate class tested, this packet is NOT frozen and the recorded result is a BOUNDED SUBSTRATE-CLASS NEGATIVE (status `COMPLETE`, outcome `FALSIFIES`): no tested credential-free deterministic localhost construction yields certified non-ceiling dynamic range. The prior symmetric mandatory-discovery negative (`EXP-PRODUCT-37989728440`) is inherited evidence and is not re-measured.

## 10. EXECUTE procedure and abort gates

1. Bring up the site on an ephemeral localhost port; bind the rendered declaration (gate I6) and write `bank_manifest.json`.
2. Run the low-novelty block first as a post-freeze treatment-liveness abort gate (I9).
3. Run the 4-arm x 4-level matrix; then NC-OOS-SCHEMA (5), NC-BUDGET-TRUNCATION (6), CC-DEGENERATE calibration (4 tasks x 2 comparators), M-REPAIR-TRANSIENT, PC-EXACT-SESSION-REPLAY (6).
4. Recompute the certificate from the rendered bank and compare to section 6.1 (I6).
5. Any gate failure -> MEASUREMENT_INVALID with the exact gate; bring-up/transport failure -> INCONCLUSIVE.

## 11. Reusable substrate

On SUPPORTS, `research/runtime/adb_v7_bank.py` + `adb_v7_harness.py` + `bank_manifest.json` become the binder for blocker B2; downstream (Product for the B1 carrier) binds them by content hash. On FALSIFIES the deterministic credential-free localhost REST class is closed and Runtime redirects to intrinsic-difficulty or shipped-carrier routes.

## 12. Design-phase probes (non-outcome-bearing)

All three probes were run in DESIGN on the runner; outputs recorded verbatim:

- stdlib import probe: `python 3.12.15`; imported `http.server, urllib.request, html.parser, json, hashlib, random, statistics, socket, threading` — 0 missing.
- localhost `ThreadingHTTPServer` canary: bound `127.0.0.1:<OS-chosen ephemeral port>` and returned HTTP 200 to a `urllib.request` GET.
- arithmetic/certificate probe over the frozen declaration only: Wilson two-sided 95% (z=1.959963984540054, n=12): k=0 → point 0.0, hi `0.242494`; k=6 → lo `0.253782`, hi `0.746218`; k=7 → lo `0.319511`, hi `0.806740`; k=12 → lo `0.757506`, point 1.0. Nominal costs: cold `3h+8={8,14,20,26}`; retrieval total `3h+9={9,15,21,27}`; treatment `{9,7,7,7}`; PC `h+8={8,10,12,14}`; CC-DEGENERATE cold `{8,10,12,14}` and retrieval total `{9,11,13,15}`. The probe reproduced section 6 exactly.

No arm was run and no success was measured; the probes are satisfiability/attainability checks only.

## 13. Validity threats

- The substrate is synthetic; this certifies the INSTRUMENT's dynamic range under declared non-omniscient policies, not transfer to the open Web or to a real LLM agent (readiness condition 3).
- The asymmetry is within-session memory, disclosed openly; the comparators are the strongest bounded policies consistent with no cross-task persistence, and this is not a claim that an unrealized memory-carrying agent is bounded by them.
- Retrieval's stratum-success profile coincides with cold (it saves only the fixed 2-request root/hub prefix); the two comparators jointly bracket the ceiling rather than testing independent mechanisms. Disclosed, not hidden.
- The Wilson intervals are descriptive summaries over a fixed finite bank, not sampling-based confidence intervals.
- Control-plane note: as of this design no `design_contract_version >= 2` experiment in the repository has reached `freeze.json` (0 of 68) and no `design_review.json` exists anywhere; prior v2 design-review model attempts have repeatedly failed to produce a review receipt. This is an external instrument risk to freezing, not a property of this design's content; it is recorded here so AUDIT/DIRECTOR do not misattribute a review-stage failure to this design's scientific content.

## 14. Artifacts

- `research/experiments/EXP-RUNTIME-38094119952/spec.json`, `prereg.md` — frozen design.
- EXECUTE: `research/runtime/adb_v7_bank.py`, `research/runtime/adb_v7_harness.py`, `bank_manifest.json`, `raw_evidence/*`, `derived/*`, `result.json`, `report.md`, `provenance.json`.

## 15. DESIGN self-attack on the six freeze-eligibility checks

DESIGN actively tried to disprove its own satisfiability before finalizing; each attack and its resolution is recorded so the independent review can re-test the same objects.

1. `decision_rule_reachability` — **attack:** is the SUPPORTS branch arithmetically forced and the FALSIFIES branch unreachable? **resolution:** both reachable and demonstrated by probe. SUPPORTS if faithful render (comparator k=0/12). FALSIFIES if an integrity-passing render admits a shortcut so a comparator reaches high-novelty k>=7: hi `0.806740` >= treatment lo `0.757506`. MIXED if P1/P2 hold but a later proposition fails. Precedence is total (integrity gate first; then SUPPORTS; else FALSIFIES = NOT(P1 AND P2); else MIXED) with no branch masking a later one.
2. `measurement_prerequisites` — **attack:** is the task bank a prerequisite "created during EXECUTE" that determines measurement possibility? **resolution:** the bank is the object under certification, not an external prerequisite; its full identity is the canonical declaration object embedded in section 4.1, fixed at freeze, and gate I6 forces the rendered object to equal it. The only hard prerequisites (Python 3.12 stdlib, localhost bind) are available now and were probed (section 12). No credential, dataset, browser, network egress or model endpoint is read.
3. `baseline_identifiability` — **attack:** are the arms guaranteed identical, or does a cost metric omit a comparator dimension? **resolution:** the arms are provably distinct (cold `{T,T,F,F}`, retrieval `{T,T,F,F}`, treatment `{T,T,T,T}`) with non-overlapping high-novelty Wilson intervals (comparator hi `0.242494` < treatment lo `0.757506`). Every cost dimension is charged: retrieval's 3 index probes are counted as `retrieval_calls` and included in the gap total, never dropped; bootstrap differs (7 vs 5) and is exactly accounted. Not a floor/ceiling situation.
4. `control_sensitivity` — **attack:** are any controls tautological or impossible? **resolution:** the calibration control I11 forces the certificate to produce BOTH outcomes (TRUE on ADB-v7, FALSE on CC-DEGENERATE whose comparators reach 4/4), so a constant certificate fails; the positive control is arithmetically solvable (PC cost <= B at every level); the refusal null is violated by a greedy fall-through resolver; NC-BUDGET-TRUNCATION under-funds to budget 10 (< the n=0.5 need of 20) so overrun is observable; M-REPAIR-TRANSIENT injects a concrete single 503 and checks `repair_attempts == 1`. Each failure maps to a distinct gate.
5. `treatment_liveness` — **attack:** can the frozen treatment actually execute? **resolution:** T-AMORT-REUSE is a deterministic declared mechanism whose per-task costs `{9,7,7,7}` fit `B(n)={11,15,16,18}` at every level; the low-novelty block runs FIRST as an abort gate (I9) and the counter signature is disjoint from both comparators. No external Product carrier is required.
6. `freeze_artifacts_bound` — **attack:** is a mutable local dependency left unbound? **resolution:** no pre-existing mutable file/fixture is consumed; the interpretation surface is fixed by the embedded canonical objects and gate I6. The DESIGN write scope is only spec.json/prereg.md, so the generator/bank cannot be authored (and hashed) at DESIGN; it is an EXECUTE deliverable fingerprinted in result.json.artifacts. With no bound artifacts, `freeze_artifacts=[]` and status `NOT_APPLICABLE` is the only consistent pairing.

The intended bounded negative remains live: if a faithful render cannot make the certificate TRUE, section 9 records a substrate-class negative and the packet is NOT frozen.
