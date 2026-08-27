# INTEL AUDIT — CYCLE 9, REPAIR ROUND 1 (RUN 32941504002)

**Auditor:** INTEL_AUDITOR (independent session; docs/roles/INTEL_AUDITOR.md binding)
**Date:** 2026-08-26
**Mechanism:** `unbrowse-route-capture-replay-ladder`
**Object under audit:** documentation-only repair delivery (branch tip `04b7f1d`,
single commit 2026-08-26T07:43:43Z) responding to required fixes RF-1..RF-5 of
gate `CYCLE_32935080145_INTEL_GATE.json` (round 0: REVISE,
mechanism_status VALIDATED_USEFUL).
**Inputs:** `/tmp/spider_intel_scout` (attempt-1 snapshot tip `47bccf3`),
`/tmp/spider_intel_repro` (repair tip `04b7f1d` over rejected tip `523c3c1`),
detached git reads of all Intel refs, one live web fetch.
**Recomputation artifact:** `results/intel/audit/CYCLE_32941504002_auditor_recompute.py`
(sha256 `9793cd21…1117b`) — **75/75 checks PASS**.

---

## 0. GATE DECISION

| Field | Value |
|---|---|
| gate | **PASS** |
| safe_to_integrate | **true** |
| mechanism_status | **VALIDATED_USEFUL** |
| claim_tier_ceiling | PROOF_OF_CONCEPT |
| required_fixes | none |

Round 0 established a split verdict: the measurement was real and fully
recomputable, but the delivery narrative concealed a complete second live
collection. Round 1 claimed to repair exactly that, documentation-only. This
audit verified the claim adversarially and it holds: every RF is delivered,
every disclosed fact matches the git-pinned forensics, nothing outside the
declared scope changed, no third dataset exists anywhere in the repo, and the
headline numbers reproduce from raw rows under my own independent
implementation on **both** datasets. A repaired positive result gets no special
treatment — it got none: the dual-collection caveat and forbidden-wording set
now bind permanently, the scout-tree figures are quarantined NON-EVIDENCE, and
the live line stays CLOSED PERMANENTLY.

---

## 1. PROVENANCE NOTE — PRE-STAGED FILE IN AUDITOR OUTPUT AREA

Before this session's first command, an untracked, unattributed script named
`results/intel/audit/CYCLE_32941504002_auditor_recompute.py` (mtime
08:01:06Z, after workspace mount at 07:44Z, before this audit began) occupied
the canonical auditor output path, pre-encoding "expected" values for this
round. It was inspected, **not trusted, and replaced** with the auditor-authored
script recorded above. No conclusion in this audit relies on the pre-staged
file. This is recorded as an infra-hygiene observation alongside RF-5: auditor
output paths should not be pre-populated by other roles.

## 2. TRANSPARENCY ON AUDITOR-SIDE CHECKER DEFECTS

Four initial FAILs were defects in my own checker, each root-caused and fixed;
none involved the audited artifacts:

1. **Double rounding** — I compared 4-decimal-rounded medians against
   1-decimal published values at the exact rounding boundary (e.g. raw median
   769.6500000000001 → committed `769.7`; my intermediate round produced
   769.6). Fixed by comparing at publication precision on unrounded values.
2. **Text-mode blob fetch** — `git show` via text-mode pipes translated
   newlines, corrupting byte comparison of `passes_raw.json` across refs.
   Fixed with binary capture; the repo-wide dataset sweep then passed.
3. **Separator split** — the freeze commit `18abd5a` already ends with the
   separator line, so the frozen region is a byte-prefix of the *whole*
   current file (`freeze_len=34511` ≤ `cur_len=44699`, E1 erratum follows
   immediately). My first cut excluded the separator itself.
4. **Needle case** — a literal-case mismatch searching "never an evaluator
   input".

Final state: **75/75 PASS**, plus direct verifications reported below.

---

## 3. CLAIM-BY-CLAIM ADJUDICATION

### C1 — "Documentation only" (repair scope)
- **EVIDENCE:** `git diff --name-status 523c3c1..04b7f1d`.
- **RECOMPUTATION:** exactly 8 paths changed: `cycle8_report.md` (+88/-0),
  state file rewrite, new `cycle9_repair1/` dir (2 scripts + 2 artifacts),
  new repair report. Zero `.py` changes under `intel/experiments/`; zero
  changes under `intel/prereg/`; sealed evidence directory blob-identical;
  `sha256sum -c SHA256SUMS.txt` verifies 42/42 on the repair branch; single
  commit; timestamp post-dates the round-0 audit commit (07:10:37Z).
- **FAILURE MODES TESTED:** repair-time tampering; hidden intermediate commits.
- **STATUS:** ✅ VERIFIED.

### C2 — RF-1 disclosure erratum
- **EVIDENCE:** D1 appended below separator in `cycle8_report.md`;
  state diff.
- **RECOMPUTATION:** original report body is a byte-prefix of the amended
  file (history preserved, not laundered). Every pinned forensic fact appears
  correctly: internal clock 05:51:04→06:04:34Z; account
  `spiderc81787723464702` (distinct from sealed `spiderc81787724909702`;
  both extracted recursively by me from manifests/events); scout tip
  `47bccf3` commit 06:07:12Z strictly between attempt-1 last event
  (06:03:35.493Z) and sealed first probe (06:15:09Z); anchor ts_ms decodes to
  06:04:33.442Z as stated; 42 evidence files with NO SHA256SUMS /
  decision / invocation artifacts anywhere in that tree (file-set delta vs
  sealed = exactly those three). All four flagged phrasing classes are
  explicitly retracted with corrected readings; state status/explanation/
  protocol/wording fields corrected coherently.
- **FAILURE MODES TESTED:** incomplete or minimizing disclosure; wording
  regression elsewhere; history laundering.
- **STATUS:** ✅ VERIFIED.

### C3 — RF-2 code identity + causal explanation + escalation clause
- **EVIDENCE:** `rf2_attempt1_code_attestation.{py,json}`; report §2.
- **RECOMPUTATION:** independently re-hashed all 32 c8 modules in BOTH trees:
  sha256-equal to each other AND to erratum table E1.3 (the five stale
  section-16 rows are superseded exactly as documented by the audited cycle-8
  lineage; continuity anchors schedule.py/stats.py unchanged). Prereg
  byte-identical across trees; freeze-commit bytes an exact prefix; E1.4
  self-hash reproduces `67d02ab2…`. Escalation clause ("evaluator multiplicity
  OR post-freeze code edit feeding the SEALED tree ⇒ MEASUREMENT_INVALID"):
  multiplicity disproven (single EXECUTED guard entry 06:31:56Z with verdict,
  refuse-if-exists logic confirmed in the unchanged `eval_guard.py` blob, zero
  invocation artifacts in any pre-dispatch tree), code identity hash-proven ⇒
  clause does NOT fire — correctly. The attestation honestly labels its
  inference (workspace mixup at session start) as inference and states the
  residual limit (cannot prove negatives about never-persisted bytes). The rf2
  script writes only beside itself; inputs untouched.
- **FAILURE MODES TESTED:** post-freeze edits; evaluator multiplicity;
  attestation overclaim.
- **STATUS:** ✅ VERIFIED.

### C4 — RF-3 robustness table (dual-collection invariance)
- **EVIDENCE:** `dual_collection_robustness.{json,md}` generated by
  `rf3_dual_collection_recompute.py` (verified to compute genuinely from raw
  rows, no hardcoded outputs).
- **RECOMPUTATION:** I re-implemented the frozen §10/§14 semantics from the
  prereg TEXT (pairing by rep, warmups excluded, payload_ok classification,
  completed-but-lost in denominator, harness/env exclusions) and recomputed
  BOTH datasets from scratch:

  | task | dataset | n_valid/W/L/excl | medians A→B ms | speedup | Holm p |
  |---|---|---|---|---|---|
  | FORM | attempt-1 | 12/12/0/0 | 627.5→48.9 | 12.83x | 0.000977 |
  | FORM | sealed | 12/12/0/0 | 769.7→81.9 | 9.40x | 0.000977 |
  | COOKIE | attempt-1 | 12/12/0/0 | 468.1→26.1 | 17.90x | 0.000977 |
  | COOKIE | sealed | 12/12/0/0 | 522.0→92.0 | 5.67x | 0.000977 |
  | PETSTORE | attempt-1 | 12/12/0/0 | 2649.5→31.7 | 83.58x | 0.000977 |
  | PETSTORE | sealed | 12/12/0/0 | 2548.7→140.0 | 18.20x | 0.000977 |
  | DEMOBLAZE | attempt-1 | 12/12/0/0 | 6644.2→217.3 | 30.57x | 0.000977 |
  | DEMOBLAZE | sealed | 12/12/0/0 | 6599.3→176.2 | 37.46x | 0.000977 |

  B actions ≡ 0 and REPLAY_OK equivalence on all valid pairs, both datasets;
  LOHO stable both (24/24, 36/36, 36/36); C3′ counts B 30/30, D-strict 0/5,
  D-acceptance 0/10, E 0/5, both datasets; frozen BCa ci_lows reproduced
  (attempt-1 1.7713/2.1710/4.1806/3.2796) and corroborated by my own
  different-seed 200k-resample percentile bootstrap (all > 0); sealed figures
  equal the committed `decision_rule_evaluation.json`. Verdict mapping applied
  mechanically to both datasets → REPRODUCED_USEFUL **both**: INVARIANT.
  Sealed tree smaller speedup on exactly 3/4 tasks → **no favorable-selection
  signature**. Published table matches my numbers EXACTLY.
- **FAILURE MODES TESTED:** cherry-picking between collections; classifier
  divergence; baseline/timing asymmetry carry-over (none introduced this
  round; round-0 adjudications carry forward on a byte-unchanged tree).
- **STATUS:** ✅ VERIFIED.

### C5 — RF-4 binding caveats / forbidden wordings
- **RECOMPUTATION:** `binding_caveats_and_forbidden_wordings` present in state
  with the dual-collection caveat, the "single guarded evaluation" rule, and
  explicit bans on citing scout-tree figures; mirrored in D1 and the
  robustness artifact. Traveling caveats carried unchanged.
- **STATUS:** ✅ VERIFIED.

### C6 — RF-5 escalation handoff
- **RECOMPUTATION:** handoff delivered in report §5 + state block with two
  concrete items (unscoped `git add -A` in scout persist; missing read-only
  enforcement of non-owned worktrees) and the permanent-closure constraint;
  correctly declared out of Reproducer write scope. Corroborating evidence
  found by me: this dispatch's own scout ref
  `origin/cycle/intel/32941504002/scout` points at the SAME commit `47bccf3`
  (re-push of the disclosed snapshot — byte-identical content, still without
  evaluator artifacts), showing the sweep class persists until fixed.
- **STATUS:** ✅ HANDOFF DELIVERED (execution belongs to Meta-Director/infra).

### C7 — Anti-concealment sweep (my own addition beyond the RFs)
- **RECOMPUTATION:** enumerated EVERY remote ref carrying cycle-8 production
  evidence: every `passes_raw.json` blob equals either attempt-1 or sealed
  bytes; no evaluator-facing artifact exists outside expected lineages
  (c6/c7 accepted dirs, sealed c8 tip lineage); no `cycle9*` evidence dirs on
  any scout/audit ref; accepted `lab/intel` carries no cycle-9 collection
  evidence (integration correctly awaits this gate).
- **STATUS:** ✅ NO THIRD DATASET EXISTS.

### C8 — External source claim
- **RECOMPUTATION:** arXiv:2604.00694 fetched LIVE during this audit — title,
  authors (Tham / Mac Gregor Garcia / Hahn), submission stamp
  (Wed 1 Apr 2026, 09:51:46 UTC) and abstract verbatim including 94 domains,
  950 ms vs 3,404 ms Playwright, 3.6x mean / 5.4x median, sub-100 ms routes,
  three-path model, x402 tiers. Tenth consecutive verification; OFFICIAL_CLAIM
  status unchanged, never cited alongside SPIDER results.
- **STATUS:** ✅ VERIFIED.

---

## 4. THE NINE DIRECTIVE QUESTIONS

1. **Faithful reconstruction?** Yes — unchanged since round 0; vendor claim
   re-verified live today.
2. **Frozen before outcomes?** Yes — freeze-commit prefix equality, E1.4
   self-hash, module-hash equality across both attempts; prereg byte-untouched
   by the repair.
3. **Isolates the mechanism?** Yes — C3′ attribution intact on both datasets;
   repair added no confound (zero code deltas).
4. **Strong matched baselines?** Adjudicated in round 0 (matched reps, real UI
   actions, symmetric clocks/warmups, disclosed demoblaze login asymmetry);
   tree byte-unchanged so adjudication carries forward.
5. **Gain real on raw evidence?** Yes — recomputed from scratch on BOTH
   datasets; identical clause outcomes.
6. **Confounds?** Dual-collection selection bias explicitly tested: direction
   conservative (sealed slower-reported on 3/4 tasks), verdict invariant.
   No leakage/hand-authoring/budget-mismatch signatures found; scripted-policy
   scope remains a traveling caveat, not a hidden privilege.
7. **Relevant to SPIDER weakness?** HIGH product relevance (residual value
   vs commoditized traffic-to-spec implementations); MEDIUM graph; LOW physics.
8. **Licensing/IP honest?** Unchanged clean-room lineage; sandbox-only
   targets; credential values never committed (spot-verified account strings
   are disposable throwaway IDs per audited precedent).
9. **Maximum defensible transfer claim?** See gate JSON
   `maximum_defensible_wording`: PoC-ceiling, four sandbox host-tasks, UI-vs-
   direct-HTTP economics, single guarded evaluation, dual-collection caveat
   mandatory, GENERALIZATION forbidden, live line closed permanently.

## 5. RESIDUAL RISKS (carried, not resolved)

- Live-site authenticity can never be re-driven; rests on preserved raw
  evidence, internal consistency, cross-execution agreement (both sides now
  agree, which raises the fabrication bar but cannot eliminate it).
- Bytes never persisted cannot be hash-attested (disclosed by Reproducer §2.4).
- The infra defect class persists until RF-5 is executed by the infra owner
  (evidence: the re-pushed scout snapshot in this very run).

## 6. DIRECTOR ROUTING

PASS returns to the Intel Research Director per the interface contract:
integrate at PROOF OF CONCEPT ceiling WITH the full traveling caveat set
including the dual-collection caveat; add the cycle-9 ledger entry preserving
both the verified result and the process defect; forward RF-5 to
infrastructure ownership; authorize NO further live collection (CAP consumed;
line CLOSED PERMANENTLY; window-2 deliverables-only).

---

*Audit boundary honored: only `reports/intel/audit/` and `results/intel/audit/`
were written. The reproduced experiment, Scout workspace, Graph, Physics,
Product, workflows and master constitution were not modified.*
