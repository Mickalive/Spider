# INTEL CYCLE 7 REPRODUCTION REPORT — unbrowse-route-capture-replay-ladder

**Verdict (frozen rule, evaluated EXACTLY ONCE): `INCONCLUSIVE`**
**Measurement status: VALID (zero preregistered invalidity conditions fired)**
**STOP RULE: NOT triggered** (it fires only on a second consecutive
MEASUREMENT_INVALID; this run is neither invalid nor instrument-failed).
Date: 2026-08-26. Branch: `cycle/intel/cycle7/repro`. Reproducer role:
`docs/roles/INTEL_REPRODUCER.md`; contract: `directives/INTEL_REPRO.md`.

---

## 1. Identity and provenance

- Mechanism: `unbrowse-route-capture-replay-ladder` — measurement-validity
  restoration round 3 under the Director's CAP.
- Scout source: cycle-7 reconfirmed candidate,
  `/tmp/spider_intel_scout/state/intel_candidate.json`
  sha256 `7a7729737e03fd464e9e1589815f2907e918cd6c93020b425f0baaf5b6255bf9`,
  byte-synced into the tree at repair-1 commit `e43a87d` from Scout snapshot
  commit `76d4e8f` (RF-3 precedent). Mission: `state/intel_loop.json`
  priority 1.
- Preregistration:
  `intel/prereg/cycle7_unbrowse_ladder_clean_instrument_prereg.md`,
  FROZEN at commit `7a1c878` (2026-08-26T00:13:41Z) BEFORE any
  condition-level observation; errata E1 (`8fe298e`, voided attempt 1
  pre-evidence) and E2 (`e43a87d`, pre-first-invocation evaluator wiring
  repair) appended below the separator only. Frozen text never edited.
- Binding prior ceilings respected: cycle-5 gate CYCLE_32873081963
  (PROOF OF CONCEPT, single-host wording remains the only validated
  knowledge) and cycle-6 gate CYCLE_32897120087 (MEASUREMENT_INVALID
  documentation; forbidden wordings carried).
- Vendor headline (arXiv:2604.00694, 94 domains, 950 ms vs 3404 ms)
  remains OFFICIAL_CLAIM, untested here regardless of outcome.

## 2. Execution ledger (complete, in order)

1. **Freeze** `7a1c878`: repaired harness (R3/R4/R5/R7 + P-WRITE/P-ECHO +
   D-independence + eval guard + triage), Phase-0 proof-pass all gates PASS
   (committed NON-EVIDENCE), full pre-freeze activity ledger in prereg §11.
2. **Attempt 1 VOIDED pre-evidence** (erratum E1): post-freeze collection
   reached P3; P2 exposed a latent call-sequence defect (petstore
   PARAM_UNRESOLVED by construction — a path R3 made reachable). Killed
   BEFORE any A/B/C/D pass row existed; partial artifacts deleted
   uncommitted; side effects disclosed in E1. Mechanical P2 alignment
   delta; collection restarted FROM SCRATCH.
3. **Attempt 2 = THE collection**: full P0-P7 executed 2026-08-26T00:14-
   00:30Z against live hosts (all five up at start AND end supplement;
   rb ping 201). Artifacts: 38-file evidence tree sealed in
   `results/intel/reproductions/cycle7/SHA256SUMS.txt` (self-check OK),
   including the mechanically regenerated
   `mutation_schedule_revealed.json` whose hash equals BOTH the frozen
   prereg value AND the hash recorded by P5 inside `mutation_arm.json`.
4. **Repair 1 PRE-FIRST-INVOCATION** (erratum E2, commit `e43a87d`): static
   producer/consumer audit found `evaluate_rule.py` gating clause 1 on
   `_c6` filenames absent from the c7 REQUIRED list — C1 was structurally
   unevaluable and any invocation would have mechanically forced
   FAILED_TO_REPRODUCE regardless of evidence. Repaired OUTCOME-BLIND
   before any invocation existed (full attestation in E2); validated on
   synthetic fixtures (3/3 verdict mapping) + selftest 72/72, all
   NON-EVIDENCE. Auditor attention explicitly drawn: this is the second
   mechanical wiring repair in the cycle; the observer-drift caveat in §8
   travels with any positive reading of this lineage.
5. **Single evaluation**: eval_guard EXECUTED ONCE at 2026-08-26T00:41:41Z
   over 38 manifest-verified files; invocation log records one EXECUTED
   entry, zero refusals, output `decision_rule_evaluation.json` now
   exists and permanently blocks re-invocation.

## 3. Mechanical verdict and per-clause table

| Clause | Content | Result |
|---|---|---|
| Invalidity conditions | required files / <4-of-5 hosts / >1 task <3 pairs / schedule hash | NONE (5/5 hosts; 0 tasks below pair floor; hash verified True) |
| C1 multi-host discovery | 4/4 host-tasks: double genuine completion accepted + >=1 route learned + discovery replay REPLAY_OK at acceptance-equivalence | **PASS 4/4** (routes learned 1/1/2/7) |
| C2 replay economics | per-task gates AND Holm family AND leave-one-host-out stability | per-task **4/4 pass**, LOHO stable — family gate FAIL -> clause **FAIL** |
| C3 capture-value-over-declaration | demoblaze B>=0.9 AND D<=0.4 | **PASS** (B 30/30=1.00; D 0/5=0.00) |
| C4 mutation detection (replica-scoped) | M1/M2/M3/M5/M6 detected; 0/25 FP Wilson<=0.15; pristine OK | **PASS** (each class SCHEMA_MISMATCH x2; M4 blind-as-predeclared REPLAY_OK x2; Wilson upper 0.1332) |
| C5 lifecycle core | RB checker all_pass | **FAIL** (environment-side write refusal; see §6) |
| Natural-TTL | window-1 anchor committed; window-2 clock-gated | claims WITHHELD per frozen structure (never enters verdict) |

Mapping: no invalidity; !all(C1..C5); C1 & !(C2 fail AND C3 fail) fails
because C3 passed => **INCONCLUSIVE** with this honest per-clause table.

## 4. What the valid measurement shows (clause-scoped wording only)

### 4.1 Multi-host capture->extract->parameterize->replay works (C1 PASS)

All four host-tasks — httpbin form POST, httpbin cookie flow,
petstore query-API find, demoblaze spec-less session-token SPA cart flow —
completed genuine browser discovery twice, yielded non-empty route stores
(1/1/2/7 routes), and replayed REPLAY_OK at acceptance-equivalence at
discovery time. This extends the cycle-5 single-host PoC *mechanism
reach* to four heterogeneous host-tasks including the pivotal spec-less
session-token SPA cell, within THIS RUN's scripted sandbox scope.

### 4.2 Replay economics: every per-task preregistered gate passed;
the frozen family gate failed (C2 FAIL — mechanical)

Per-task (n=5 interleaved valid pairs each, warmups excluded, B actions=0,
B equivalence on ALL pairs):

| Task | median A ms | median B ms | speedup | BCa log-ratio CI | wins |
|---|---|---|---|---|---|
| T_HTTPBIN_FORM | 795.4 | 224.7 | 3.54x | [0.639, 1.315] | 5/5 |
| T_HTTPBIN_COOKIE | 616.6 | 231.5 | 2.66x | [0.957, 1.061] | 5/5 |
| T_PETSTORE_FIND | 2531.5 | 331.3 | 7.64x | [2.008, 2.050] | 5/5 |
| T_DEMOBLAZE_CART | 7133.0 | 341.3 | 20.90x | [2.889, 3.080] | 5/5 |

Leave-one-host-out direction stable in all three exclusions (10/10 and
15/15 paired wins each).

The frozen family gate required all four Holm-adjusted sign-test
p-values < 0.05; raw p = 0.03125 everywhere adjusted to 0.125 => FAIL.

POST-HOC DESIGN OBSERVATION (exploratory; NOT a rule change, NOT evidence):
at n=5 pairs the smallest achievable one-sided sign p is 1/32 = 0.03125,
and Holm's smallest-of-four multiplier is 4, so the adjusted-p floor is
0.125 > 0.05 for ANY possible outcome. As frozen (structure inherited
identical from cycle-6 section 14), the C2 family gate had zero power at
the preregistered sample size; it could never pass. The mechanical verdict
therefore could never be REPRODUCED_USEFUL under any data this design
could produce. Disclosed because it determines what this run can and
cannot mean; the verdict stands exactly as the frozen rule computed it.

Consequently NO cross-host economics advantage claim may be made from
this run. The per-task statistics above are reported as measured
outcomes inside an INCONCLUSIVE result, under the UI-traversal-vs-direct-
HTTP-scripted-policy ceiling only.

### 4.3 Capture beats declaration on the decisive spec-less cell (C3 PASS)

Demoblaze (no public machine-readable contract): B replay succeeded 30/30;
the GENERATED_SPEC_NULL arm built from an independent dedicated capture
succeeded 0/5. Where a public contract exists (petstore), the docs-null
client succeeded descriptively 5/5 — consistent with the preregistered
segmentation prediction (docs-null ~= replay on spec-public hosts;
replay >> spec-null on the spec-less host), here measured cleanly for the
first time in this lineage. Descriptive: rb Q5 both lanes REPLAY_OK.

### 4.4 Mutation detection quality validated replica-scoped (C4 PASS)

Sealed schedule revealed post-collection with hash equality verified;
M1 field-removal, M2 type-change, M3 nesting-change, M5 pagination-shape,
M6 error-format each fired SCHEMA_MISMATCH on both executions; M4
enum-meaning-flip behaved as predeclared blind (REPLAY_OK x2, excluded);
benign FPR 0/25 (Wilson 95% upper 0.1332 <= 0.15); pristine rechecks all
OK. Wording boundary holds: replica-scoped sensitivity ONLY; no live-site
drift-detection claim.

### 4.5 Escalation transparency and hygiene

Ladder event stream: 160 events, all REPLAY_OK, zero substitution
surfaces; pointer-only store assertion true; demoblaze ownership-scoped
cleanups executed after each arm block; per-arm namespaced identities
held; availability start/end all green.

## 5. Addressing secondary arm (descriptive only, as frozen)

Exact-intent top-1 5/8, lexical 5/8 on the merged multi-host store. The
prefix-inheritance column ran structurally disabled again
(`build_prefix_store({})`) and stays EXCLUDED from claims per the
cycle-6 precedent; its recorded 0/8 with artifact_confirmed=true is an
instrument property, not a measurement of prefix inheritance.

## 6. C5 failure attribution: environment-side, pre-disclosed fallback

restful-booker refused EVERY write attempt with HTTP 418: the mandated
cooldown check itself (write_ok=false, status=418), then both Q1 booking
creations ("creation_refused"). Consequences, exactly as the frozen
fallback designed: Q1 parameterization had no created bookings to test
(FAIL), Q2's corrupted-auth negative control PASSED while its positive
control was structurally impossible (null), and the checker's escalation/
structured-code counters are empty as a downstream consequence of Q1
never reaching replay stage. Q3 rewind compliance, Q4 deleted-record
absence surfacing (HTTP_ERROR, deleted=true), and the pointer-only
assertion all PASSED. This is the documented persistent environment fact
from the pre-freeze probe (>1h natural cooldown did not clear 418), NOT
an instrument defect and NOT invalidity. C5 remains genuinely untested
on the parameterization-to-new-ids question this round.

## 7. Natural-TTL arm status

Window-1 fresh own-study anchor committed (policy B) at ts_ms
1787704208665 (= 2026-08-26T00:30:08Z); window-2 eligibility opens
1787790608665 (+24h). Non-decisional drift observation vs cycle-6
fingerprints: petstore/demoblaze/jsonplaceholder unchanged, httpbin
changed (volatile-by-design class, excluded from detection anyway).
All staleness claims WITHHELD pending window 2 per frozen section 13;
natural-TTL never entered the verdict.

## 8. Honest caveats

1. **Observer-drift residue**: two outcome-blind mechanical repairs were
   applied post-freeze this cycle (E1 pre-evidence voidance + restart;
   E2 pre-first-invocation evaluator wiring). Both are fully disclosed
   with attestations, but the cumulative pattern is real and must temper
   any positive reading of this lineage until an independent audit
   recomputes from raw rows.
2. **C2 family gate zero-power**: the INCONCLUSIVE verdict partially
   reflects a preregistered design that could not pass under any
   outcome (§4.2). The per-task economics signals are real measurements
   but cannot be aggregated into an accepted advantage claim by this
   run's rule.
3. **C5 environment-blocked**: lifecycle parameterization-to-new-ids and
   the auth positive control remain untested; restful-booker 418 is
   outside our control.
4. **Scripted policies throughout**: all economics numbers are
   UI-traversal-vs-direct-HTTP under controlled load policies with no
   LLM agents; no token-cost or autonomous-agent economics claims.
5. **Single-replica mutation scope**: C4 says nothing about live-site
   drift; M4 remains a predeclared blind spot of shape-based detectors.
6. **n=5 pairs/task, single session**: overnight volatility exposure
   disclosed pre-freeze; no continuous availability monitoring between
   phases.
7. **demoblaze shared demo DB**: residual rows from prior cycles'
   attempts persist beyond ownership-scoped cleanup; shape-only oracle
   and arm-namespacing contained cross-arm contamination this run
   (D-arm 0/5 vs B-arm 30/30 separation argues containment held).
8. **Vendor figures**: OFFICIAL_CLAIM tier only, with documented
   blog-vs-paper inconsistency; never citable alongside SPIDER results.

## 9. Maximum defensible wording (proposal to Auditor/Director)

> "In a preregistered, clean-instrument, single-shot evaluation (frozen
> decision rule evaluated exactly once on hash-sealed evidence; zero
> invalidity conditions), SPIDER's clean-room three-tier route ladder
> reproduced capture->extract->parameterize->replay on 4/4 heterogeneous
> first-party-API sandbox host-tasks including a spec-less session-token
> SPA, at acceptance-equivalence with zero browser actions on every
> measured replay pass; demonstrated capture-value-over-declaration on
> the decisive spec-less flow (route-store replay 30/30 vs independent
> generated-spec client 0/5) while a public-contract host showed the
> opposite segmentation descriptively (docs-null 5/5); and validated
> replica-scoped schema-mutation detection (5/5 detecting classes, 0/25
> benign false positives, Wilson 95% upper 0.133) with escalation
> transparency and no silent substitution anywhere. The preregistered
> verdict is nevertheless INCONCLUSIVE: the frozen cross-host economics
> family gate cannot be satisfied at the preregistered sample size
> (structural zero power, disclosed post hoc), and the restful-booker
> lifecycle core was environment-blocked (persistent HTTP 418 on all
> writes). No cross-host economics advantage, no staleness claim
> (window 2 pending), no generalization, and no vendor-headline support
> may be claimed from this run. Evidence tier: PROOF OF CONCEPT ceiling;
> accepted knowledge beyond cycle-5 wording requires lane-Director
> integration of clause-scoped findings after audit."

Forbidden wordings carried from the cycle-6 gate plus this run:
- citing ANY cycle-7 speedup/success figure as an ACCEPTED mechanism
  advantage (the rule returned INCONCLUSIVE);
- claiming multi-host economics superiority was established;
- claiming natural-TTL/staleness was measured (window 2 pending);
- treating C4 as live-site drift detection;
- presenting delivery/repair history as mechanism falsification, or
  INCONCLUSIVE as either success or failure of the mechanism.

## 10. STOP-RULE and continuation semantics (Director input)

The stop rule (second consecutive MEASUREMENT_INVALID) did NOT fire:
this measurement is valid. The CAP's close-set lists
REPRODUCED_USEFUL / REPRODUCED_NO_ADVANTAGE / FAILED_TO_REPRODUCE as
mission-closing verdicts; INCONCLUSIVE is outside both the close-set and
the stop-trigger, so continuation semantics require an explicit Lane
Director decision. Two candidate paths for that decision, offered
without prejudice: (a) treat the C2 zero-power finding as "materially
new external evidence" justifying ONE more narrowly-scoped preregistered
attempt with a reachable statistics plan; or (b) integrate the
clause-scoped positives (C1/C3/C4) and close the mission with the
withheld questions routed to queued candidates. That decision belongs to
the Director and Auditor, not to this report.
