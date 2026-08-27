# INTEL AUDIT — CYCLE 8, REPAIR ROUND 3 (run 32931388530)

- Auditor: INTEL_AUDITOR (`docs/roles/INTEL_AUDITOR.md` binding; `directives/INTEL_AUDITOR.md` mandatory gate)
- Date: 2026-08-26 · Mechanism: `unbrowse-route-capture-replay-ladder`
- Object: repair round 3 delivery, branch `cycle/intel/32931388530/repro` = `ca97212` (= `d1ce094` → `411fdc9` → `ca97212` on round-1 tip `937c7a5`)
- Gate: **PASS** · Mechanism status: **INCONCLUSIVE** (pending measurement) · Claim tier this run: NONE
- Recompute script: `results/intel/audit/CYCLE_32931388530_auditor_recompute.py` — 37/37 PASS

---

## 0. What this round was supposed to be

Round 2 (run 32928978937) was certified an EMPTY DELIVERY: the persisted snapshot was
byte-identical to accepted-lane base `7a8182d`. The round-2 gate re-issued four fixes:

| Fix | Requirement |
|---|---|
| RFIX-A | Non-empty delivery descending from `937c7a5`, carrying the full c8 instrument, prereg+errata surface, Phase-0 artifacts, cycle-8 state file; Reproducer self-verifies persisted output |
| RFIX-B | Dated erratum BELOW the frozen separator: pre-collection attestation rounds 0→(3), refreshed sha256 table at the new freeze point, amended-file self-hash; frozen text byte-untouched |
| RFIX-C | Re-run ALL offline gates post-erratum with code untouched; commit rerun artifact under `pre_freeze_phase0/`; update state prereg hash |
| RFIX-D | Truthful provenance rewrite in `state/intel_reproduction.json` + repair-round ledger 0→1→2→(3); correct stale figures; keep verdict null / status pending |

The delivered tree claims documentary-only compliance: zero code edits, zero collection.

## 1. Claim-by-claim adversarial verification

### CLAIM 1 (RFIX-A): valid non-empty delivery from the right base
- EVIDENCE: git topology of `/tmp/spider_intel_repro`; `origin/cycle/intel/32931388530/repro`.
- CHECK: `rev-parse HEAD == ca97212 == origin/cycle/intel/32931388530/repro`;
  `merge-base --is-ancestor 937c7a5 HEAD` YES; contains freeze `18abd5a`;
  `diff --name-status 937c7a5..HEAD` = exactly 4 files (prereg, round3 artifact,
  delivery note, state file), none `.py`. Full instrument present (32 modules,
  prereg+E1, 5 Phase-0 artifacts, rewritten state file).
- FAILURE MODES TESTED: wrong-base delivery (round-2's defect class) — ruled out;
  partial delivery — every path named by RFIX-A exists.
- STATUS: **VERIFIED**, with one minor defect → see §2.

### CLAIM 2 (RFIX-B): lawful erratum, honest new freeze point
- EVIDENCE: `intel/prereg/cycle8_unbrowse_ladder_powered_prereg.md` at `18abd5a`,
  `937c7a5`, HEAD.
- CHECK: split at separator `--- (frozen text above; errata only below) ---`.
  Frozen region byte-identical across all three revisions; round-0 errata section
  verified EMPTY before append ⇒ E1 is a pure append through the channel the frozen
  text itself designates. E1.3 table: recomputed sha256 of all 32 modules matches;
  exactly five rows superseded vs frozen section 16 (`evaluate_rule.py`,
  `phase0_fixtures.py`, `run_all.py`, `selftest.py`, `tasks_hosts.py`) with truthful
  old values recorded; other 27 rows identical. E1.4 self-hash reproduces via its own
  published one-liner (`67d02ab2…`); full-file hash `e82140e3…` matches state claim;
  state `preregistration.sha256` equals the self-hash.
- FAILURE MODES TESTED: erratum-channel abuse (editing frozen text while claiming
  append-only) — disproven byte-for-byte; stale-table protocol breakage (the round-1
  REVISE cause: step 1 would fail BY CONSTRUCTION) — now resolved because a
  superseding authoritative table exists and verifies 32/32; forged self-hash — no.
- STATUS: **VERIFIED**.

### CLAIM 3 (RFIX-C): all gates green post-erratum, code untouched
- EVIDENCE: `results/intel/reproductions/cycle8/pre_freeze_phase0/round3_gate_rerun.json`
  + my own fresh-environment execution.
- CHECK (executed directly, not trusted):
  - selftest **115/115 PASS**;
  - phase0 fixtures **all_match TRUE** (11 cases derived from prereg text: 5 verdict
    mappings + 4 section-14 invalidity conditions + both RF-2 whole-host-death scenarios);
  - regression_lock **PASS bit-exact** vs committed c7 anchors — cross-checked against
    `results/intel/reproductions/cycle7/decision_rule_evaluation.json`: speedups
    3.54/2.66/7.64/20.9, ci_lows 0.6388/0.9574/2.008/2.8888, raw sign p 0.03125×4,
    Holm 0.125×4 (figures-only lock; c8 verdict-on-c7-data ignored by design);
  - wiring_audit clean; ttl_rehearsal control-no-claim + mutation-fires-positive both confirmed;
  - power tables byte-stable vs the prereg section-10 embedding;
  - sealed schedule regenerates `276132df…` exactly (schedule.py untouched since audited c6/c7).
  - Code-untouched proof independently reproduced: all 32 module blobs equal `937c7a5`.
- FAILURE MODES TESTED: self-reported-green-without-substance (I re-ran everything);
  hidden code edit between gates (blob equality kills it).
- STATUS: **VERIFIED / INDEPENDENTLY REPRODUCED**.

### CLAIM 4 (RFIX-D): provenance now truthful
- EVIDENCE: `state/intel_reproduction.json` vs raw trees `unbrowse_ladder_c7` vs `_c8`.
- CHECK (ground truth, not narrative): common=24; byte-verbatim=16 (exact list match);
  changed=8 exactly `{eval_guard, evaluate_rule, extract, run_all, selftest, specgen,
  stats, tasks_hosts}`; eval_guard AST-equal after removing module docstring ⇒
  docstring-only claim true; new=8 exactly the listed Phase-0 tooling modules;
  24+8=32. Repair ledger rounds 0→3 accurate, including the honest EMPTY-DELIVERY
  entry for round 2; `selftest 99→115` corrected; `verdict_proposed: null`;
  status pending-collection. The round-0 falsehood ("24 inherited byte-verbatim
  modules") is gone from the live file and remains preserved verbatim in the
  immutable round-0/1/2 audit gates — history not rewritten. Final commit `ca97212`
  inspected line-by-line: one sentence rephrased into equivalent truth; nothing
  semantic changed.
- FAILURE MODES TESTED: provenance inflation, history laundering, cosmetic-hiding — none found.
- STATUS: **VERIFIED**.

### CLAIM 5: zero condition-level outcomes exist; test unchanged
- EVIDENCE: entire `results/intel/reproductions/cycle8/` subtree; guard state.
- CHECK: subtree contains EXACTLY five NON-EVIDENCE Phase-0 files (soak_samples,
  spare_screening, repair1_gate_rerun, repair1_rf3_bite_proof, round3_gate_rerun);
  zero outcome-shaped filenames anywhere (passes_raw / ladder_events / ttl_window /
  SHA256SUMS / decision_rule_evaluation absent ⇒ guarded single evaluation has not
  run and cannot have run). Preregistered test constants (pairs=12, N_MIN_VALID=8,
  speedup≥2.0, one-sided Holm α=0.05, C3′ two-variant gates, invalidity conditions,
  verdict mapping) live inside the byte-invariant frozen region and the
  blob-identical evaluator — untouchable this round.
- STATUS: **VERIFIED**.

### CLAIM 6: headline arithmetic (recomputed regardless of round type)
- CHECK: Table 1 min achievable Holm-adjusted p = m·2⁻ⁿ recomputed n=5..12 with
  independent binomial/Holm code (reachable ⇔ n≥7; floor n=8 ⇒ 0.015625; scheduled
  n=12 ⇒ 0.000977). Eleven Table 2 composition entries recomputed — exact match
  including [2,2,1,1]@12→PASS 0.038574 and [3,0,0,0]@12→fail 0.072998. Window-2
  clock gates recomputed from committed anchors: c6 `1787695530749`+86400s =
  2026-08-26T22:05:30Z; c7 `1787704208665`+86400s = 2026-08-27T00:30:08Z — both as
  preregistered.
- STATUS: **VERIFIED**.

### CLAIM 7: external source & licensing posture
- CHECK: arXiv:2604.00694 fetched LIVE this audit — title/authors/submission date and
  every abstract figure verbatim (94 domains; 950 ms warmed cached vs 3,404 ms
  Playwright; 3.6× mean / 5.4× median), CC BY 4.0 confirmed. Eighth consecutive
  audit-chain verification. No new external claims entered (documentary round);
  clean-room lineage anchored by blob equality with previously audited trees.
- STATUS: **VERIFIED**.

## 2. Minor defects found (recorded, non-blocking)

1. **Off-by-one enumeration**: `cycle8_repair3_delivery_note.md` and
   `state/intel_reproduction.json` say `pre_freeze_phase0/` holds "now 6 files";
   the directory holds exactly FIVE (git: 4 at round-1 tip + 1 added). Every
   required artifact exists; pure documentation slip. Correction rides along in the
   collection dispatch's mandatory report/state update.
2. **Stale protocol wording**: state file next-dispatch step 1 still says
   "sha256sum -c against prereg section 16"; per E1.3's supremacy clause the check
   must run against the refreshed table (verified 32/32 here). Failure direction is
   safe (mismatch ⇒ investigate-before-collection), and both E1.3 and the delivery
   note already state the correct rule — but the executor must read it that way.

Why these do not force REVISE: neither touches any gate, threshold, metric,
exclusion rule, evidence file or the integrity protocol's outcome (both fail safe),
and both are corrected in documents that the recorded protocol writes anyway at
collection time. Burning a further repair round would repeat the round-2 pattern of
spending FINAL-round calendar on paperwork — a cost the round-2 gate itself flagged
as material. They are therefore bound as carry-forward notes in the gate JSON, which
is normative for the next dispatch.

## 3. Confounder / integrity attack summary

No result exists to confound; attacked the delivery itself:
fabrication (no outcome-shaped artifact anywhere; no manifest ⇒ evaluator
uninvocable), test-weakening-by-stealth (byte-proof against), erratum abuse
(byte-proof against), grep-hygiene laundering (commit inspected; original false
claim remains quoted in immutable predecessor gates), hidden work on stray refs
(`cycle/intel/repair3/repro` identified as unrelated cycle-1 content), provenance
inflation (claims re-derived from bytes, they hold), scope creep into scientific
claims (none made).

Carried-forward caveats that must travel into any future USEFUL wording (unchanged
from round-1 gate): roster-file/liveness-log non-cross-check; uncalibrated 400 ms
spare-host pacing inside arm A timed region (contingency only, ~0.4 s bound); M4
enum-flip blindness; sandbox scope + scripted policies; PROOF OF CONCEPT ceiling;
vendor headline OFFICIAL_CLAIM forever.

## 4. Decision

- **Gate: PASS** — the evidence/result of THIS round (documentary completion of
  RFIX-A..D) is valid; a negative or empty result could equally have passed if
  honestly delivered; this one is positive *and* true.
- **Mechanism status: INCONCLUSIVE** — pending-measurement state; not success, not failure.
- **safe_to_integrate: true** — the Director may accept this repair state and dispatch
  the FINAL confirmatory round under the recorded mechanical protocol (step 1 per
  E1.3). Round 4 remains FINAL; hard closure whatever the verdict returns.
- Wording ceiling for this run: see gate JSON `maximum_defensible_wording` — process
  completion, zero mechanism knowledge either direction.

— INTEL_AUDITOR, run 32931388530, 2026-08-26
