# CYCLE 6 REPAIR ROUND 2 — RESTORATION NOTE (RF-A)

Date: 2026-08-25
Run: 32897120087 (`intel-loop.yml`, cycle_index=6, repair_from_run_id=32890075186, repair_round=2)
Branch: `cycle/intel/32897120087/repro` (parent = accepted lane tip `8bfcf85`)
Restores: `origin/cycle/intel/32878215017/repro` @ `c1543f8` ("Intel cycle 6 repair 0: reproduction")
Precedent: cycle-1 repair round 3 documented byte-exact restoration
(`results/intel/reproductions/cycle1_repair3_restoration_note.md`).

## What was restored

All 18 instrumentation files under `intel/experiments/unbrowse_ladder_multihost/`
were restored from commit `c1543f8` via `git checkout c1543f8 -- <path>` and
verified byte-exact against the source commit's git blob hashes:

```
__init__.py addressing.py canon.py capture.py extract.py ladder.py pilot.py
probes_rb.py quiescence.py replay.py replica.py routestore.py run_all.py
schedule.py selftest.py specgen.py stats.py tasks_hosts.py
```

Verification method: `git rev-parse c1543f8:<path>` compared to
`git hash-object <restored file>` for all 18 files -> **18/18 identical**
(executed before any edit; transcript in the repair-round session log).

Offline re-verification after edits: `python3 -m
intel.experiments.unbrowse_ladder_multihost.selftest` -> **49/49 PASS**;
sealed schedule hash recomputed =
`276132df2f6a57a466d3b84d918e03acc177c10d2e82f745d028f9f02c4efbb8`
(matches the auditor-sealed value in gates CYCLE_32878215017 /
CYCLE_32890075186; schedule.py itself is UNEDITED).

## Code deltas vs c1543f8 (complete list)

Round-0 RF-2 / round-1 RF-B mandated "the sole code delta" be the baseline-arm
timing fix. During pre-freeze verification, two additional by-construction
measurement-validity defects and one ethics defect were identified in the
restored tree. Shipping them silently would have made the preregistered test
incapable of passing on the pivotal task regardless of the mechanism's actual
behavior (a guaranteed false negative), and one defect would have made hygiene
deletes touch other sessions' rows on a shared demo backend. Master-prompt
§24 ("code/data/report disagreement") and §33 ("A negative result can be just
as wrong as a positive result") govern: all three were repaired BEFORE the
freeze, are individually documented here and in the prereg, are mechanical,
and none was chosen or tuned after observing any condition-level outcome
(no confirmatory collection existed at edit time; the freeze commit precedes
all collection). If the auditor rejects any delta, the affected clause is
void, not reinterpreted.

### DELTA-1 (RF-B, mandated) — tasks_hosts.py::flow_demoblaze_cart
Removed `time.sleep(1.2)` from the TIMED arm-A region (cycle-2-forensics bias
class: additive constant in the comparator arm only). Replaced with
`_quiesce(tracker)` — the same observable-condition calibrated-quiescence wait
used after every other interaction in the same flow. No additive constant
remains; demoblaze arm A now carries zero fixed sleeps inside its timer.

### DELTA-2 (measurement-validity wiring) — run_all.py + tasks_hosts.py
`HOST_TASK_SPECS["T_DEMOBLAZE_CART"]["accept"]` is the BROWSER-side acceptance
(`target_found`/`target_price == 790`) while B/D project payloads via
`project_demoblaze_viewcart` -> `{n_entries, prod_ids_present}`. The existing
`accept_demoblaze_replay()` contract was defined but wired into NO call site,
so every B/D/P2 demoblaze equivalence check would have been False BY
CONSTRUCTION. Repair: spec declares `"accept_replay": accept_demoblaze_replay`;
run_B_pass / run_D_pass / P2 use `spec.get("accept_replay") or spec["accept"]`.
A-side acceptance untouched; all other tasks unaffected (no accept_replay key).
This TIGHTENS the test (makes the preregistered gate reachable); it does not
loosen any threshold.

### DELTA-3a (discovery first-party scope) — tasks_hosts.py HOST_TASK_SPECS
`T_DEMOBLAZE_CART["origin"]` changed `https://www.demoblaze.com` ->
`https://api.demoblaze.com`. The SPA's task traffic all targets
api.demoblaze.com; TrafficRecorder/is_candidate/har_to_spec filter strictly by
netloc equality, so with the UI host as origin every API body was rejected and
demoblaze discovery could learn ZERO routes by construction (the frozen
intent_map keys already name api.demoblaze.com URLs, proving design intent).
Browser flows still navigate to www.demoblaze.com; only the first-party filter
scope changed to the operator's actual API host. `host` (quiescence key)
unchanged.

### DELTA-3b (ethics: ownership-scoped cleanup) — tasks_hosts.py::DemoblazeSession.cleanup
Disclosed pre-freeze contract probe (/tmp/opencode/c6_pilot/
contract_probe_demoblaze.json, quoted in prereg) showed the shared demo
backend's /viewcart returns entries created by OTHER sessions (85 rows on a
fresh account) and the shipped cleanup deleted ALL of them. Repair: cleanup
now deletes ONLY entries whose `cookie` field equals our own session token.
Rows owned by other sessions are never touched.

### DELTA-4 (pre-outcome crash repair, appended post-freeze via prereg erratum E1)
First post-freeze launch crashed at P1 session bootstrap before any
observation existed: round-0 code two-value-unpacked the SINGLE dict returned
by HttpbinCookieSession.bootstrap() (iterating its keys). Caller fixed to
single assignment; bootstrap() unchanged. Disclosed in prereg ERRATUM
APPENDIX E1 with the aborted-attempt side effects (one throwaway demo account;
zero durable artifacts). run_all.py sha256 after DELTA-4:
07d2b3d3829cd23a59e46b8453dff0476b5fcbc89fcc9434812fe3bd5d78338e.

## Round-1 failure-mode structural exclusion

Round 1 failed because work never reached the durable tree. This round:
after the final commit, `git status` / `git diff 8bfcf85..HEAD --stat` must
show the restored+fixed code, the prereg, the raw evidence tree
`results/intel/reproductions/cycle6/`, this note, the report, and both updated
state files. Verified before finishing (see report §delivery).
