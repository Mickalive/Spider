# INTEL AUDIT — CYCLE 1, RUN 32800296360, REPAIR ROUND 3

- Auditor: INTEL_AUDITOR (`docs/roles/INTEL_AUDITOR.md` binding; `directives/INTEL_AUDITOR.md` mandatory gate). Independent session; prior audits `cycle1_run32781482957`, `cycle1_run32792931901`, `cycle1_run32796176172` re-derived where relied upon, not trusted.
- Date: 2026-08-25. Stance: adversarial ("assume the headline may be wrong").
- Mechanism: `sgdr-state-grounded-dynamic-retrieval` (SGDR, arXiv:2606.04391; canonical repo https://github.com/plusnli/online-skill-learning, CC BY-SA 4.0).
- Object under audit: Reproducer repair round 3 (`fec6779`, branch tip == `origin/cycle/intel/32800296360/repro`), which owed RF-A…RF-E per gate `CYCLE_32796176172_INTEL_GATE.json`, under that gate's explicit flip condition: "RF-A through RF-E completed exactly as specified → next audit PASS".
- Verdict summary: **PASS.** The round-2 empty-snapshot failure is fully remediated: the verified round-1 reproduction is restored byte-exactly, all documentary fixes are delivered exactly as prescribed, and delivery verification claims are true (re-executed by me, not trusted from banners). The measurement was additionally re-verified fresh this session from committed raw evidence.
- Mechanism status: **VALIDATED_USEFUL** (carried and re-confirmed; claim tier ceiling PROOF OF CONCEPT).

---

## 1. Round-3 scope verification (restoration + documentary deltas only?)

| Check | Result |
|---|---|
| Ancestry | HEAD `fec6779` is a single commit on lane base `0a55649`; working tree clean; refs `origin/cycle/intel/32800296360/repro` == `origin/cycle/intel/repair3/repro` == HEAD |
| Full-tree diff `1e51a5c..HEAD` | Exactly 3 files: `reports/intel/reproductions/cycle1_report.md` (M), `state/intel_reproduction.json` (M), `results/intel/reproductions/cycle1_repair3_restoration_note.md` (A) |
| Diff vs lane base `0a55649..HEAD` | Exactly the 24 declared paths; no workflow/policy edits; no hidden files (`git status --ignored` clean beyond `.gitignore` classes) |
| Frozen materials byte-identity | `git diff 1e51a5c..HEAD -- intel/prereg/ intel/experiments/ results/intel/reproductions/cycle1/` → **0 lines** (10 code + 2 prereg + 8 evidence byte-identical to the twice-verified round-1 tree) |
| Manifest `cycle1_repair1_SHA256SUMS.txt` | Recomputed in restored tree: **18/18 OK**; manifest itself byte-identical to round 1 |
| Prereg frozen-hash table | Recomputed: 6/10 match, drifted files exactly `collect.py`/`convert.py`/`retriever.py`/`stimuli.py`, current hashes equal to the attestation table (unchanged since round 0) |

Repair-scope discipline: **VERIFIED.** No data, code-logic, metric, condition, exclusion, or success-rule element changed this round.

## 2. Required-fix verification (RF-A…RF-E)

- **RF-A (byte-exact restoration): RESOLVED — verified by end-state equality.** All 20 frozen paths diff-empty against `1e51a5c`; manifest 18/18 OK recomputed by me in the restored tree. The "verified BEFORE any edit" timing is attestation-based, but the scientific requirement is end-state fidelity, which I established independently: any post-restoration tampering would have broken byte-equality or the manifest, neither of which occurs.
- **RF-B (erratum wording): RESOLVED verbatim.** Report §2 erratum now carries exactly the prescribed stable-controls sentence ("wrong-context summary or summary-only score falls back to baseline level (both 24/74); constant-text fusion controls are not stable … 19–36/74 depending on dummy string, due to sha1 bucket collisions at d=512 … not cited as evidence"); the false constant-dummy clause is gone. `state/intel_reproduction.json` `honest_caveats[2]` aligned identically. I re-derived both cited controls myself this session (**WRONGCTX 24/74, SUMONLY 24/74** — own ablation scoring over the frozen embedder + committed caches; script preserved as audit artifact) — the sentence's numbers are correct.
- **RF-C (cost footnote): RESOLVED verbatim, arithmetic confirmed.** Restated text matches the prescription. Artifact counts re-derived by me: collection cache = **11 keys**, OK-status contexts = **49 of 51 records** (2 invalid); conversion-run counters sum to **2 would-be misses** (both C_a04 rep-0); committed conversion cache holds **10 keys, 9 shared with collection, exactly 1 unshared** → "≈12–13 total; exact split unreconciled at artifact level; no metric impact" is accurate and appropriately hedged.
- **RF-D (round provenance): RESOLVED.** `repair_round` marker 1→3; `repair_round_3_provenance` block enumerating changed files; restoration note present and accurate; `wording_ceiling_note` correctly repoints to the superseding round-1 gate.
- **RF-E (delivery verification): RESOLVED — all three sub-items independently re-executed by me:** (i) repro tip `fec6779` ≠ base `0a55649`; (ii) all 24 declared paths present (name-status enumeration matches the claimed 10+2+1+8+1+1+1); (iii) rerunning `sgdr_repro.evaluate` on the restored caches regenerates `retrieval_eval.json` **byte-identically** (sha256 `342ec130d0a052d0201ecaf9e9ce0ef6876f1d4a529e6987390a859c99db5061`, computed before and after regeneration in a sandbox copy) and `python3 -m sgdr_repro.selftest` reports **7/7 PASS**.

Binding-wording check: state-file `strongest_defensible_wording` is **verbatim-equal** to the round-1 gate's binding `maximum_defensible_wording` (programmatic comparison). All five round-1 forbidden-wording items remain covered (one item paraphrased, semantically identical).

## 3. Fresh measurement audit (independent of prior sessions)

Recomputed this session from committed raw evidence:

- **Retrieval level** (from `per_query` rows): n=87 queries, hard=74, canonical=13. Hard@1: A_native **0/74**, B_plain/B_mmr **25/74**, C_a04/C_a05 **36/74**, D_random **19/74**. Canonical@1: A 13/13, B 12/13, C 13/13, D 2/13. @3 hard: B_mmr/C **68/74**. Pairwise C_a04 vs B_mmr on hard@1: **11 wins / 0 reversals** (25 both-correct, 38 neither). C-only win clusters: **int.dyn.nav=8, int.dyn.ex2=2, int.dyn.start=1; login/pager zero** — the report §2 erratum is factually exact.
- **Report bookkeeping**: "17 included subgoals" = distinct (task, subgoal-index) pairs among the 49 OK contexts = 17, exactly those passing the frozen inclusion rule against library sigs incl. generic mappings. Ground truth = 211 probe records (43 true / 164 false / 4 invalid); 5 already-satisfied + 15 unsatisfiable qids excluded uniformly (exclusion logic condition-independent in code). Library = 12 fragments, all success_count=1/failure_count=0 (cold-exploration origin intact).
- **Conversion level** (from raw run rows, 60/60 clean = 38 success + 22 partial): literal novel A/B/C = **21/42/39** @ pooled success **27/30 = .900** each; paraphrase-p1 A_zero/B/C = **400/42/36** @ **12/20=.600, 16/20=.800, 18/20=.900**. Combined rule-as-written: Novel A=421, B_mmr=84, C_best=75; Succ A=39/50=.78, B=43/50=.86, C=45/50=.90. Clause 1 (36>25>0) ✓, clause 2 (.90 ≥ max(.86,.78)) ✓, clause 3 (75 < min(421,84)) ✓ → **REPRODUCED_USEFUL follows the frozen rule exactly as written**. The strictest per-slice reading still fails clause 3 on literal vs A_native (39>21) — disclosed unchanged, travels with any downstream claim.
- **Leakage/confounder sweep re-run fresh**: summaries derive from entry snapshots only (content-hash cached; deterministic given cache — evaluator stats hits=49/misses=0 confirm warm-cache provenance of the committed eval); truth cache condition-independent; seeds fixed (20260824 family; hashlib-only scoring path inspected in `embedder.py`/`retriever.py`); no LLM anywhere; no premature integration anywhere in either mount (`VALIDATED_MECHANISMS.json` empty, ledger untouched, diff-vs-base contains no policy/workflow files).

## 4. External source claim

Re-verified live this session: `github.com/plusnli/online-skill-learning` exists and is the official implementation of "Online Skill Learning for Web Agents via State-Grounded Dynamic Retrieval" (arXiv:2606.04391); README internally references old `skill-dynamic-retrieval/` paths (rename residue consistent with rounds 1–2 findings); license CC BY-SA 4.0 with vendored Apache-2.0 browsergym + NOTICE; README documents solve→evaluate→induce→update pipeline, per-site JSONL skill libraries, per-step retrieval logging with goal/state-summary — consistent with the mechanism contract the clean-room implementation targets. Clean-room discipline (reference code never fetched/viewed/copied) remains plausible and consistent with the stdlib-only structure; licensing constraint for SPIDER integration (no CC BY-SA code reuse) stands.

## 5. Claim-by-claim status

| # | Claim (this round) | Status |
|---|---|---|
| C1 | Byte-exact restoration of the verified round-1 tree (RF-A) | VERIFIED (end-state byte-equality + manifest) |
| C2 | Erratum wording replaced with stable-controls sentence (RF-B) | VERbatim VERIFIED; control figures 24/24 re-derived by me |
| C3 | Cost footnote restated consistently with artifacts (RF-C) | VERIFIED; counts re-derived (11/49/2/1-unshared) |
| C4 | Round provenance block + restoration note enumerate all changes (RF-D) | VERIFIED (diff confirms nothing else changed) |
| C5 | Delivery verification: tip≠base, 24 paths, byte-identical eval regeneration, selftest 7/7 (RF-E) | VERIFIED by independent re-execution |
| C6 | Headline numbers unchanged and real | RE-VERIFIED end-to-end from raw evidence this session |
| C7 | External-source identity/licensing | RE-VERIFIED live |

## 6. Why PASS

The round-2 gate predeclared its own flip condition, and every element of RF-A…RF-E is now complete and independently verified. The measurement underneath has now survived three independent auditor sessions (two full from-prereg recomputations in rounds 0–1; this session's fresh aggregate recomputation, artifact-count reconciliation, control re-derivation, and byte-identical regeneration). A positive result received no special treatment here: it passed because every load-bearing number, control, provenance bound, and delivery claim checked out against committed evidence.

Residual limitations carried forward (disclosed, non-blocking):
1. Fix timing for the 4 hash-drifted files remains attestation-based (single-commit history) — bounded behaviorally; unchanged since round 0.
2. Evidence tier stays PROOF OF CONCEPT: lexical-hash embedder, deterministic summarizer, 12 fragments, 3 sandbox sites, scripted policies, same-site only, tiny n. GENERALIZATION language remains forbidden.
3. Scout-owned `state/intel_candidate.json` still carries the stale repository URL — Reproducer write scope respected; **Intel Research Director must propagate the canonical URL before/at integration snapshot.**

## 7. Relevance assessments (mechanism-level, unchanged)

- GRAPH: HIGH — direct upgrade path for the measured §14 weakness (hand-authored goal_sig addressing; entry-context mismatch); maps onto existing store schema; today bounded to same-site, small-library, lexical-embedder regime.
- PRODUCT: MEDIUM — repeated-exploration cost reduction in principle; toy-scale setting prevents cost claims today.
- PHYSICS: LOW — retrieval mechanics, not environment dynamics; contextually corroborates WP-002B's nearest-neighbour competence finding.

## 8. Gate

Machine-readable: `results/intel/audit/CYCLE_32800296360_INTEL_GATE.json` — `gate: PASS`, `mechanism_status: VALIDATED_USEFUL`, `safe_to_integrate: true`. Eligible for entry into `VALIDATED_MECHANISMS` at PROOF OF CONCEPT ceiling under the binding maximum-defensible wording and forbidden wordings.

Audit artifacts preserved:
- `results/intel/audit/CYCLE_32800296360_ablation_rederive.py`
