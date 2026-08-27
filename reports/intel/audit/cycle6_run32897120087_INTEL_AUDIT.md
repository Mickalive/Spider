# INTEL AUDIT — CYCLE 6, REPAIR ROUND 2 (RUN 32897120087)

**Mechanism:** `unbrowse-route-capture-replay-ladder` (multi-host scope, natural-TTL window 1, induced-mutation detection quality, GENERATED_SPEC_NULL)
**Auditor:** INTEL_AUDITOR, independent session, run 32897120087
**Object under audit:** `/tmp/spider_intel_repro` @ `7a80b33` (branch `cycle/intel/32897120087/repro`; base `8bfcf85`; freeze `869ae87` 2026-08-25T21:15:22Z; evidence `fc0c2da`)
**Prior gates:** round 0 = `CYCLE_32878215017` REVISE/INCONCLUSIVE (instrumentation only); round 1 = `CYCLE_32890075186` REVISE/INCONCLUSIVE (empty snapshot; escalation trigger recorded)
**Reproducer-proposed verdict:** MEASUREMENT_INVALID

---

## 1. Gate summary

| Item | Result |
|---|---|
| **GATE** | **PASS** |
| safe_to_integrate | true (honest invalid-run documentation enters lane memory; NO positive mechanism entry) |
| mechanism_status (this run) | **MEASUREMENT_INVALID** |
| Claim tier ceiling | NONE_THIS_RUN |
| Binding accepted knowledge | unchanged: cycle-5 gate `CYCLE_32873081963` wording verbatim |

The round-1 gate's own flip condition was met exactly: RF-A..RF-H all delivered, the frozen decision rule was evaluated exactly once on committed raw evidence, and every headline number recomputes. The verdict happens to be MEASUREMENT_INVALID — which per master-prompt §24 is a *measurement* outcome, not mechanism falsification, and per directive line 17 is exactly the shape that may PASS.

## 2. Delivery verification (RF-A..RF-H)

| RF | Claim | Auditor verification | Status |
|---|---|---|---|
| RF-A restore c1543f8 byte-exact | 18/18 blob-hash verified pre-edit | I re-ran `git rev-parse c1543f8:<path>` vs current blobs: **15/18 byte-identical; exactly the 3 declared delta files differ** (`run_all.py`, `tasks_hosts.py`, `probes_rb.py` — DELTA-1..8) | DONE |
| RF-B baseline timed sleep | removed from TIMED arm-A region | Code inspection: no sleep in any timed region; remaining `time.sleep(2.5)/0.5` are in explicitly UNTIMED `demoblaze_browser_login` (identical-across-arms bootstrap per prereg §6); `_quiesce(0.03)` is poll-loop implementation, not additive constant | DONE |
| RF-C prereg frozen BEFORE observation | freeze commit precedes collection | `869ae87` at 21:15:22Z vs evidence `fc0c2da` at 22:08:15Z; **zero removed lines** in `git diff 869ae87..HEAD` on the prereg — errata E1-E5 strictly appended below the separator; §14 decision rule byte-untouched throughout | DONE |
| RF-D natural TTL bounded honestly | window files + withheld claims | `ttl_window1.json` (fingerprints+ts) and `ttl_window2_protocol.json` (`NOT_EXECUTED_THIS_RUN`) committed; evaluator's `natural_ttl` block is verdict-independent; STALE_TTL appears nowhere as evidence | DONE |
| RF-E raw evidence committed | P0-P7 complete | 33-entry `SHA256SUMS.txt` verifies clean (`sha256sum -c`: all OK); passes_raw has 184 rows including warmups (excluded from stats but committed), B extras to n=30/task, demoblaze C null-cell row present | DONE |
| RF-F rule evaluated exactly once, honest reporting | MEASUREMENT_INVALID | I reran the FROZEN evaluator (sha256 `bbc0c406…` = §16 row, unchanged since pre-collection freeze): output **byte-identical** (`242fb706…`). Verdict precedence verified in code: invalidity conditions checked first, exactly as prereg §14 maps them | DONE |
| RF-G report/state/candidate hygiene | cycle 6 + preserved history | Report present; `state/intel_reproduction.json` cycle 6 with cycle-5 record under `historical_records.cycle5`; `state/intel_candidate.json` sha256 == Scout copy == `fc5b62e9…` (recomputed both sides) | DONE |
| RF-H post-outcome immutability | zero edits after outcomes visible | `git diff fc0c2da..HEAD`: exactly one file added (`decision_rule_evaluation.json`, the once-run output). No code, prereg, or evidence edits post-outcome | HELD |

The round-1 escalation trigger ("BLOCKED if ANY required item again fails to commit") does not fire: every required item is committed.

## 3. Independent recomputation of headline numbers

My own second-path checker (`results/intel/audit/CYCLE_32897120087_auditor_recompute.py`, 20 checks, ALL PASS):

- **T_HTTPBIN_FORM** — A ms [646.2, 628.0, 628.9, 626.7, 736.5] → median **628.9**; B ms [218.3, 100.7, 66.4, 42.0, 46.6] → median **66.4**; speedup_median **9.47×**; my independent seeded percentile bootstrap CI [1.085, 2.760] consistent with the committed BCa [1.4669, 2.5555]; B actions 0 on all 31 rows; 5/5 valid pairs. Task-level C2 arithmetic is real — but it rides the SCHEMA_MISMATCH replay path (see §4 row 1) and fails the preregistered family gates (Holm 0.125 > 0.05; LOHO unstable). Under MEASUREMENT_INVALID precedence it may not be cited as mechanism evidence.
- **T_HTTPBIN_COOKIE** — **30/30 replays REPLAY_OK with zero detector deviations yet payload_ok=false on ALL** (defect row 4); arm-A median **482.2 ms** confirmed. The report's exploratory counterfactual "≥7×" is conservative: interleaved B(1–5) median 37.0 ms ⇒ 13.03×.
- **PETSTORE / DEMOBLAZE** — 0 valid pairs each (NO_ROUTE at first resolve call).
- **Mutation arm** — M1/M3/M6 detected ×2 each (SCHEMA_MISMATCH); M2/M5 never executed a request (PARAM_UNRESOLVED); all 10 benign "false positives" are PARAM_UNRESOLVED artifacts on exactly the two param-starved targets ⇒ executable-benign FP rate **0/15**; pristine rechecks 6/7 OK + 1 same artifact.
- **Schedule sealing** — revealed steps byte-equal to deterministic rebuild; canonical steps hash == sealed `276132df…` == `mutation_arm.schedule_hash`; `schedule_hash_verified=true` mechanical. My initial whole-dict hash mismatch was my comparator error (the hash covers the steps list); resolved, no tampering.
- **RB probes** — Q1 both creations refused (HTTP 418 environment protection, recorded honestly via DELTA-8); Q2 negative surfaced with nothing presented (positive control nulled by same refusal — correctly reported null); Q3 rewind-compliance only; Q4 deleted-record absence surfaced; Q5 header-auth parity d=b=REPLAY_OK.
- **Availability** — 5/5 surfaces at start AND end supplements.

Offline controls: selftest **49/49 PASS**; sealed-schedule determinism reproduced; imports across all 19 modules are stdlib + playwright only (clean-room holds).

## 4. Cause-attribution attack (all seven rows verified against code AND data)

| # | Reported cause | Auditor verification | Verdict |
|---|---|---|---|
| 1 | FORM SCHEMA_MISMATCH = strict missing-key on echoed browser headers | ladder_events: deviations are exactly `missing_key@$.headers.Cache-Control/Origin/Priority/Referer`; payloads acceptance-equivalent | CONFIRMED (representation boundary) |
| 2 | Demoblaze addtocart excluded by vendor-faithful JSON/XML filter | Both discovery manifests: `POST /addtocart → text/html; charset=utf-8`; filter keeps JSON/XML only | CONFIRMED (environment × frozen heuristic) |
| 3 | Petstore intent='' → NO_ROUTE | routes carry `intent:""`; extract.py matches method-tagged keys (`"GET https://…findByStatus"`) against query-bearing captures and prefix-compares bare URLs against method-tagged keys — structurally unmatchable | CONFIRMED (instrument defect) |
| 4 | Ladder success branch drops parsed body → perfect replays scored false | ladder.py maps `parsed→payload` on REPLAY_OK; run_B_pass reads `out["parsed"]` ⇒ None; escalation branch coincidentally retains `parsed` (why FORM scored at all) | CONFIRMED (instrument defect) |
| 5 | Mutation params heuristic starves M2/M5 + 10 benign FPs | run_all ~L716: `params={"id":1} if "booking" in target or "posts" in target else {}` — `replica_get_post` (singular) and items `page` param unmatched; data: all 10 FPs are B4/B5 trials on those two targets, all PARAM_UNRESOLVED | CONFIRMED (instrument defect) |
| 6 | RB write-refusal HTTP 418 | probe_events_rb: two `booking_creation_refused`; GET/auth/list kept working; consistent across attempts 6-7 | CONFIRMED (environment) |
| 7 | pointer_only_store false = checker substring false alarm | banned substring `"password":` in extract.py matches rb_auth TYPE-NAME sketch `{"password": "str", "username": "str"}`; no literal value present (slot-marker regex clean) | CONFIRMED (cosmetic checker defect) |

No evidence of outcome-shaped tuning: every defect runs AGAINST a positive result (they caused the invalidity), the final verdict is negative-leaning, and none was patched after outcomes became visible.

## 5. Confounder attack

- **Leakage/matchedness:** paired reps 1–5 interleaved by seeded block order (`block_order.json`, seed 20260826); warmups excluded from stats but committed; same clock semantics both arms; no server-reported timing anywhere.
- **Baseline strength:** A = calibrated-quiescence scripted traversal (cycle-2-forensics artifact class eliminated by DELTA-1); C privileged-docs null present where public docs exist, with demoblaze correctly NULL-celled rather than fabricated; D generated-spec comparator wired via DELTA-2 (tightening, not loosening).
- **Hand-authoring:** intent maps and addressing ground truth disclosed as hand-authored; the disabled prefix column is EXCLUDED from claims rather than silently reported — honest.
- **Selection/tuning pressure:** six voided attempts fully disclosed with side effects; DELTA-8 postdates attempt-6 partial observations but touches only P4 probe paths (P1-P3 metrics untouched); frozen §14 unchanged across all errata (verified zero removed lines). Residual caveat: partial attempt-6 P1-P3 codes were necessarily known before attempt 7; no rule element responded to them.
- **Ethics/licensing:** ownership-scoped cleanup landed before collection (DELTA-3b); the one-time 85-row cross-session deletion during the pre-freeze contract probe is disclosed without euphemism; residue (~7 throwaway demo accounts + cart rows, ≤2 RB bookings until reset cron) bounded and disclosed. reqres.in/dummyjson exclusions are conservative written interpretations, quoted verbatim at freeze. Clean-room stdlib-only lineage; vendor surfaces unfetched this session; paper CC BY 4.0.

## 6. External source claim

arXiv:2604.00694 fetched live by THIS session (third independent auditor verification): title, authors (Tham / Mac Gregor Garcia / Hahn), submission date (2026-04-01), CC BY 4.0 license, and abstract headline figures match Scout/candidate records verbatim (950 ms warmed cached vs 3,404 ms Playwright across 94 domains; 3.6× mean; 5.4× median; sub-100 ms well-cached routes; three-path model; x402 tiers). The vendor's 94-domain headline remains OFFICIAL_CLAIM — untested by SPIDER and, per the still-empty citation graph, by anyone else.

## 7. What this audit allows SPIDER to record

1. Run 32897120087 contributes ZERO mechanism knowledge beyond accepted cycle-5. All five mission questions (multi-host fidelity, calendar-time staleness, mutation-detection quality, capture-over-declaration, multi-host addressing) remain OPEN in every direction — neither confirmed nor refuted.
2. Legitimate OBSERVATION-tier byproducts for future cycles (environment/instrument facts, NOT mechanism measurements): httpbin FORM echoes browser headers into JSON bodies; api.demoblaze.com answers its cart-write endpoint text/html; restful-booker developed write-path 418 protection under repeated traffic while reads stayed open; the four instrument defects are precisely characterized with repair paths identified.
3. The harness now demonstrably reaches P7 end-to-end with sealing, availability bookkeeping, honest escalation vocabulary and fault isolation working; a single clean pre-outcome instrumentation cycle is a credible next step (lane-director decision, not self-assigned).
4. Accepted VALIDATED_MECHANISMS (cycle-1 SGDR, cycle-5 ladder) are untouched by this cycle.

Non-blocking notes (travel with provenance): stray `.rb_cap_path` scratch file committed inside the evidence dir, not covered by SHA256SUMS; `decision_rule_evaluation.json` intentionally appended post-manifest (disclosed); §16 hash table superseded four times via errata (transparent but noisy; all final hashes verify); state-file `strongest_defensible_wording` is a self-authored run-level wording superseded byte-wise by this gate.

## 8. Boundary

Read-only over all committed refs plus both mounted workspaces; execution limited to the offline selftest, schedule determinism, frozen-evaluator rerun, and my own pure-arithmetic recomputation over committed JSON. One live fetch (arXiv abstract page). The harness was deliberately NOT executed against live targets by the auditor.
