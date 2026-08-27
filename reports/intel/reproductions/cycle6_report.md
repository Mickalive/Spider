# INTEL REPRODUCTION REPORT — CYCLE 6 (REPAIR ROUND 2)
## unbrowse-route-capture-replay-ladder — multi-host scope, natural-TTL window 1, induced-mutation detection quality, GENERATED_SPEC_NULL

- Reproducer: INTEL_REPRODUCER (`docs/roles/INTEL_REPRODUCER.md`, binding)
- Run: GITHUB_RUN_ID 32897120087 (`intel-loop.yml`, cycle_index=6,
  repair_from_run_id=32890075186, repair_round=2)
- Branch: `cycle/intel/32897120087/repro`; freeze commit `869ae87`
  (2026-08-25T21:15:22Z); evidence commit `fc0c2da`
- Preregistration: `intel/prereg/cycle6_unbrowse_ladder_multihost_prereg.md`
  FROZEN before any condition-level observation; errata appended below
  separators only (E1 `544d9bf`, E2 `86aa063`, E3 `08f6745`, E4 `4200b13` +
  `59629c2`, E5 `b45e461`)
- Scout source: cycle-6 snapshot a74fdb0 (`/tmp/spider_intel_scout`;
  candidate synced byte-exactly into this tree, sha256 fc5b62e9…)
- Instrumentation lineage: restored byte-exact from round-0 commit c1543f8
  (`results/intel/reproductions/cycle6_restoration_note.md`), then the
  documented deltas below

---

## 1. Verdict (proposed)

**MEASUREMENT_INVALID** — claim tier ceiling: NONE_THIS_RUN.

The frozen decision rule was evaluated EXACTLY ONCE on committed raw
evidence by the frozen evaluator (`evaluate_rule.py`, output:
`results/intel/reproductions/cycle6/decision_rule_evaluation.json`). It fired
the preregistered invalidity condition ">1 host-task with <3 valid A/B pairs"
(three of four tasks have zero valid pairs because replay resolution failed
at their first call). Per §14 mapping, an invalidity condition yields
MEASUREMENT_INVALID regardless of clause outcomes. This verdict does NOT
falsify the mechanism and does NOT weaken accepted cycle-5 knowledge; it
records that this run's multi-host measurement is not interpretable at face
value, with causes attributed in §6.

## 2. Repair-round delivery map (round-1 gate RF-A..RF-H)

| RF | Delivery |
|---|---|
| RF-A restore c1543f8 byte-exact | DONE — 18/18 blob-hash verified before edits; note: `results/intel/reproductions/cycle6_restoration_note.md` |
| RF-B baseline-arm timed sleep | DONE — DELTA-1: `time.sleep(1.2)` removed from TIMED arm-A region, replaced by `_quiesce(tracker)` (same observable-condition policy as rest of flow) |
| RF-C prereg freeze BEFORE observation | DONE — frozen at `869ae87` before any collection; contains every round-0 RF-1 element + full pre-freeze disclosure (§11 of prereg incl. QUIESCE_GAP_MS 924.6 provenance, DEMO_TARGET_PRICE=790 live-read disclosure, contract probe) |
| RF-D natural-TTL bounded honestly | DONE — `ttl_window1.json` + `ttl_window2_protocol.json` committed; STALE_TTL counted nowhere; all TTL/staleness claims WITHHELD pending window 2; restful-booker excluded |
| RF-E execute post-freeze, commit raw evidence | DONE — attempt 7 completed P0-P7; 35 evidence files committed `fc0c2da` incl. SHA256SUMS.txt (33 entries), schedule revealed post-collection |
| RF-F verdict exactly once, honest reporting | DONE — single evaluator run above; negative/partial results preserved |
| RF-G report + state + candidate hygiene | DONE — this report; `state/intel_reproduction.json` rewritten to cycle 6 with full cycle-5 record preserved under `historical_records`; `state/intel_candidate.json` byte-synced to Scout (sha256 verified) |
| RF-H post-outcome immutability | HELD — after outcomes first became visible (attempt-6 P2 prints, 21:58Z), ZERO edits to frozen prereg text, code semantics, or evidence; the two defects discovered during analysis (§6 rows 4-5) are REPORTED, not patched |

### Code deltas vs c1543f8 (all pre-outcome, individually disclosed)

DELTA-1 (mandated RF-B): timed-region sleep -> `_quiesce`.
DELTA-2: wire existing `accept_demoblaze_replay` into B/D/P2 acceptance
(browser-side acceptance could never accept a projected replay payload —
unreachable success gate by construction).
DELTA-3a: demoblaze capture/extraction origin = api.demoblaze.com (SPA's
actual first-party API host; UI-origin rejected every body by construction).
DELTA-3b: ownership-scoped demoblaze cleanup after the disclosed probe showed
the shared backend returns OTHER sessions' cart rows (85 seen once).
DELTA-4 (E1): bootstrap() two-value unpack crash fix (pre-any-observation).
DELTA-5a/b (E2): TrafficRecorder.attach reconnection + P2 slot values.
DELTA-6a/b (E3, corrected in E4): bounded element waits (Locator.wait_for) +
P1 fault isolation recording discovery_error as first-class outcome.
DELTA-7 (E4): bare-host call sites for recorder/filter/extract/specgen.
DELTA-8 (E5): RB probe fault isolation (structured probe_errors; refusals
degrade to honest clause failures).

Errata E2-E5 each disclose the voided attempt that motivated them, state that
no arm-condition metric informed any edit, and were committed BEFORE the next
launch. E4 additionally discloses an error OF MINE: E3's first version used a
nonexistent Playwright API (`locator.wait_for_selector`), making petstore
failure deterministic until corrected.

### Collection attempts ledger (full transparency)

| # | Outcome | Side effects disclosed |
|---|---|---|
| 1 | crashed P1 bootstrap (DELTA-4 bug) | 1 throwaway demo account |
| 2 | killed by runner command timeout mid-P3 | partial artifacts wiped uncommitted |
| 3 | VOID: recorder never attached (all-zero routes observed) | demo account + cart rows |
| 4 | crashed petstore transient render gap | wiped uncommitted |
| 5 | VOID: E3 waits used nonexistent API; zero-route cause confirmed as DELTA-7 class | wiped uncommitted |
| 6 | completed P1-P3, crashed P4 on restful-booker HTTP 418 refusal | wiped uncommitted; observations quoted in E5 |
| **7** | **COMPLETE P0-P7** — committed evidence | final |

Cumulative environment residue: ~7 throwaway demoblaze accounts with cart
rows in the shared disposable demo DB (ownership-scoped cleanup cannot reach
across sessions); up to two lingering restful-booker scratch bookings until
its ~10-min reset cron.

## 3. Faithful-vs-adaptation disposition

See prereg §2 (frozen). In short: capture/filter/extract/parameterize/
pointer-store/replay/escalation/TTL mechanics FAITHFUL to the documented
mechanism family; shared-graph ranking tier and HTML-extraction tier omitted
(labeled); restful-booker scripted-capture substrate labeled adaptation;
GENERATED_SPEC_NULL and sealed-replica mutation arms are SPIDER additions;
intent maps hand-authored (disclosed); vendor marketplace/settlement rails
out of scope. Vendor headline (94-domain 950ms vs 3404ms) remains
OFFICIAL_CLAIM — untouched by anything in this cycle.

## 4. Environment facts (committed evidence)

- Availability start AND end (supplement): httpbin 200, petstore 200,
  demoblaze UI/API 200, rb ping 201 — all five surfaces up throughout
  (`availability_log.json`, `availability_log_end_supplement.json`).
- Quiescence recalibration day-of: petstore p99-gap x2 = 936.9 ms vs frozen
  924.6 (1.3% drift; hard cap bounds behavior; prereg §11 discloses both).
- restful-booker refused POST /booking with HTTP 418 twice in attempt 6 and
  twice again in attempt 7's Q1 (recorded via DELTA-8 as
  booking_creation_refused) while GET/auth/list kept working — consistent
  with write-path protection after cumulative attempt traffic; environment
  fact, not harness logic.
- demoblaze addtocart responds `text/html; charset=utf-8` (200) even to valid
  writes — site reality discovered at discovery time (manifests).

## 5. Frozen-rule evaluation (the one run)

Verdict: **MEASUREMENT_INVALID**
Invalidity conditions fired: `>1 task with <3 valid A/B pairs`
(T_HTTPBIN_COOKIE, T_PETSTORE_FIND, T_DEMOBLAZE_CART each 0 valid pairs).
Schedule hash verified True; availability gate passed; no other invalidity.

| Clause | Result | Detail |
|---|---|---|
| C1 multi-host discovery | FAIL (1/4 tasks) | FORM: routes learned, both runs accepted, replay equivalent=true BUT code SCHEMA_MISMATCH (strict missing-key deviations on echoed browser headers absent from urllib replays, e.g. `$.headers.Cache-Control/Origin/Priority/Referer`) -> frozen REPLAY_OK requirement unmet. COOKIE: PASS cleanly (REPLAY_OK + equivalent). PETSTORE: route learned but intent='' (see §6-3) -> NO_ROUTE. DEMOBLAZE: 6 routes learned but addtocart filtered by the vendor-faithful JSON/XML heuristic (site returns text/html) -> sequence NO_ROUTE. |
| C2 replay economics | FAIL (1/4 task-level passes) | FORM: 5/5 valid pairs, median A 628.9ms vs B 66.4ms = 9.47x, BCa log-ratio CI [1.467, ...] >0, B actions 0<6, equivalence 5/5 -> task PASS. COOKIE: 30/30 replays REPLAY_OK with zero detector deviations yet payload_ok=false on ALL (see §6-4) -> 0 valid pairs. PETSTORE/DEMOBLAZE: 0 valid pairs (NO_ROUTE). Holm family + LOHO therefore fail. |
| C3 capture-over-declaration | FAIL | demoblaze B rate 0.0 (NO_ROUTE) < required >=0.9; D rate 0.0 <=0.4 technically true but the conjunction fails. Descriptive: petstore D (public-contract fed) succeeded 5/5 — a perfect public OpenAPI contract DOES suffice where it exists, exactly the comparator's design; rb Q5 header-auth parity d=REPLAY_OK b=REPLAY_OK. |
| C4 mutation detection (replica-scoped) | FAIL | hash verified; sensitivity: M1,M3,M6 detected (SCHEMA_MISMATCH x2 each); M2,M5 NOT measured — requests were never built (PARAM_UNRESOLVED) due to the round-0 target->params substring heuristic ("posts" plural vs replica_get_post; items page param unsupplied). Benign trials: B1,B2,B3 all correctly REPLAY_OK; B4,B5 unmeasurable for the same reason -> recorded fp=10/25 (Wilson upper .593) is an ARTIFACT of those unresolved requests, not detector false alarms; pristine rechecks 6/7 REPLAY_OK, 1 PARAM_UNRESOLVED artifact. M4 blind as predeclared (REPLAY_OK x2). |
| C5 lifecycle core (RB substrate) | FAIL | Q1 parameterization: both creations REFUSED (HTTP 418) -> honest failure recorded, mechanism untested this run. Q2 negative AUTH_FAIL surfaced with nothing presented = TRUE (positive control nulled by same refusal). Q3 rewind compliance TRUE. Q4 surfaced_absence TRUE. pointer_only_store assertion returned FALSE — analyzed as a checker false alarm: the banned substring `password":` matches the TYPE-NAME sketch `{"password": "str"}` inside the auth route's body_template.shape; no literal value present (slot-marker regex clean). Checker escalation_events_present=false reflects probe-event log scope only (ladder_events.json contains the escalations). |

Natural-TTL: window-1 fingerprints + protocol committed; claims WITHHELD per
prereg §13. Nothing in this run speaks to calendar-time staleness.

## 6. Cause attribution (each row tied to evidence)

| # | Symptom | Attribution | Class |
|---|---|---|---|
| 1 | FORM P2/B SCHEMA_MISMATCH though payloads equivalent | Detector v2 strict missing-key on echoed-header envelope; urllib replays legitimately send fewer headers than browsers | Representation boundary (mechanism-relevant design datum: shape sketches over echo-prone endpoints need transport-volatile classes) |
| 2 | DEMOBLAZE addtocart absent from learned routes | Site responds text/html to the write endpoint; vendor-faithful filter keeps JSON/XML only | Environment x frozen-heuristic boundary |
| 3 | PETSTORE intent='' -> NO_ROUTE | Round-0 prefix matcher compares method-tagged keys against bare URLs, so query-bearing captures never inherit intents (extract.py third branch) | Instrument defect (latent; now characterized) |
| 4 | COOKIE 30/30 perfect replays scored payload_ok=false | Ladder.resolve_and_run success branch drops `parsed` (maps to `payload`) while run_B_pass reads `parsed`; deviation path coincidentally retains it | Instrument defect (latent) — also explains why FORM's C2 pass rode the SCHEMA_MISMATCH path |
| 5 | M2/M5 undetected; fp=10/25 artifact; 1 pristine PARAM_UNRESOLVED | run_mutation_arm params heuristic (`"posts"` plural substring; items `page` param never supplied) | Instrument defect (latent) |
| 6 | Q1 creations refused (418) | Environment write-protection | Environment |
| 7 | rb pointer-only assertion false | Checker banned-substring false alarm on type-name sketch key | Cosmetic checker defect |

Read-only analysis of committed rows further shows (EXPLORATORY
COUNTERFACTUAL — not the frozen rule, not confirmatory): under the obvious
wiring corrections of rows 3-5 alone, COOKIE presents 30/30 REPLAY_OK at
33-66ms against arm-A median 482.2ms (>=7x) and the mutation arm presents
6/6 executable mutation detections with 0/15 executable-benign false
alarms — a coherent hypothesis set for a FUTURE preregistration; none of it
is claimed as a result of this run.

## 7. What this run establishes

Nothing beyond the accepted cycle-5 result. Multi-host discovery/economics
fidelity, calendar-time staleness, induced-mutation detection quality,
generated-spec-null capture-value, and multi-host intent addressing remain
NOT ESTABLISHED. The binding wording ceiling remains exactly gate
CYCLE_32890075186.maximum_defensible_wording (nothing newer exists); this
report respects every forbidden_wordings entry of that gate, including: no
citation of any cycle-6 measurement as mechanism evidence; no claim that the
cycle-5 result was extended or replicated; no presentation of delivery/
instrument failures as mechanism falsification.

## 8. Next discriminating questions (for the lane, not self-assigned)

1. One clean pre-outcome cycle fixing the four characterized instrument
   defects (rows 3,4,5,7) under a fresh preregistration on untouched
   evidence — the expensive instrumentation now demonstrably reaches P7
   end-to-end and every external surface stayed up.
2. Detector representation policy for echo-envelope endpoints
   (transport-volatile classes vs strictness) — decide BEFORE outcomes.
3. Filter policy question raised honestly by row 2: does the mechanism
   family's JSON/XML heuristic need a declared treatment for successful
   non-JSON-labeled write responses? (Vendor-documented heuristic kept here.)
4. Natural-TTL window 2 (>=24h calendar gap) per the committed protocol.
5. Whether restful-booker's write-path 418 persists (cooldown study) before
   relying on it for lifecycle probes.

## 9. Artifacts

- Prereg + errata: `intel/prereg/cycle6_unbrowse_ladder_multihost_prereg.md`
- Code (19 modules): `intel/experiments/unbrowse_ladder_multihost/`
- Restoration/delta provenance:
  `results/intel/reproductions/cycle6_restoration_note.md`
- Raw evidence: `results/intel/reproductions/cycle6/*` (manifest
  SHA256SUMS.txt, 33 entries; decision_rule_evaluation.json appended
  post-manifest as the once-run output)
- Pre-freeze disclosures: `results/intel/reproductions/cycle6/pre_freeze_pilot/`
- State: `state/intel_reproduction.json` (cycle 6; cycle-5 record preserved),
  `state/intel_candidate.json` (byte-synced to Scout, sha256 fc5b62e9…)

— INTEL_REPRODUCER, cycle 6 repair round 2, 2026-08-25
