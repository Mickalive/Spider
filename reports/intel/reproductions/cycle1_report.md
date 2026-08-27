# INTEL REPRODUCTION REPORT — CYCLE 1

## sgdr-state-grounded-dynamic-retrieval (SGDR, arXiv:2606.04391)

- Date: 2026-08-24. Role: Intel Reproducer (binding fiche respected; Auditor validation is a separate session).
- Preregistration (FROZEN before any condition-level observation): `intel/prereg/cycle1_sgdr_prereg.md`.
- Code: `intel/experiments/sgdr_repro/` (hashes frozen in prereg). Clean-room: implemented solely from the Scout's formula-level spec; the CC BY-SA reference repository was neither fetched nor inspected.
- Reference repository (canonical, corrected repair round 1 per audit R3): **https://github.com/plusnli/online-skill-learning** — supersedes the stale URL `github.com/plusnli/skill-dynamic-retrieval` carried by the Scout cycle-1 candidate record (repository rename; content otherwise Auditor-verified accurate; CC BY-SA 4.0 — not fetched, not viewed, not copied by the Reproducer).
- Raw evidence + machine results: `results/intel/reproductions/cycle1/` (`manifest_library.json`, `manifest_contexts.json`, `executability_cache.json`, `retrieval_eval.json`, `conversion_runs.json`, `conversion_summary.json`, `summarizer_cache*.json`).

> **REPAIR ROUND 1 (2026-08-25).** Documentary repairs ONLY, answering INTEL_AUDIT
> `cycle1_run32781482957` (gate REVISE → required fixes R1–R3): **R1** provenance attestation at
> `intel/prereg/cycle1_repair1_provenance_attestation.md`; **R2** §2 erratum below; **R3** canonical
> URL above and in the prereg erratum appendix. NO data, raw evidence, code logic, metric, condition,
> or success-rule change of any kind; code and raw evidence are byte-identical to repair round 0
> (`results/intel/reproductions/cycle1_repair1_SHA256SUMS.txt`). The preregistered test is unchanged.
> All numbers below stand exactly as originally reported.

> **REPAIR ROUND 3 (2026-08-25) — RESTORATION + DOCUMENTARY DELTA ONLY.** Answers INTEL_AUDIT
> `cycle1_run32796176172` (gate REVISE; round 2 delivered an empty snapshot). This round's output is a
> **byte-exact restoration of commit `1e51a5c`** (the twice-independently-verified repair-round-1 tree)
> plus documentary deltas only, per required fixes RF-A…RF-E of that gate:
> - **RF-A**: all 23 round-1 paths restored byte-exact from `1e51a5c`; `sha256sum -c
>   results/intel/reproductions/cycle1_repair1_SHA256SUMS.txt` → **18/18 OK verified BEFORE any edit**.
>   No data, code logic, metric definition, condition, exclusion rule, or success-rule change of any kind;
>   the preregistered test is neither weakened nor retuned; `intel/prereg/cycle1_sgdr_prereg.md` and the
>   provenance attestation are byte-identical to round 1 (frozen section untouched).
> - **RF-B / RF-C / RF-D**: erratum wording corrected in §2 above and in `state/intel_reproduction.json`;
>   cost footnote restated above; round-provenance block added to the state file; short restoration note at
>   `results/intel/reproductions/cycle1_repair3_restoration_note.md`. Changed files enumerated there.
> - **RF-E delivery verification, performed this round**: (i) repro branch tip ≠ `origin/lab/intel`
>   (`0a55649`); (ii) all restored/updated paths present — enumeration: 10 × `intel/experiments/sgdr_repro/*.py`,
>   2 × `intel/prereg/*`, 1 × `reports/intel/reproductions/cycle1_report.md`, 8 ×
>   `results/intel/reproductions/cycle1/*.json`, 1 × `results/intel/reproductions/cycle1_repair1_SHA256SUMS.txt`,
>   1 × `state/intel_reproduction.json`, + 1 new restoration note = **24 paths total**; (iii) rerunning
>   `sgdr_repro.evaluate` on the restored caches regenerates `retrieval_eval.json` **byte-identically**
>   (sha256 `342ec130d0a052d0201ecaf9e9ce0ef6876f1d4a529e6987390a859c99db5061`) and
>   `python3 -m sgdr_repro.selftest` → **7/7 PASS**. Headline aggregates re-printed identically:
>   hard@1 A 0/74, B_plain/B_mmr 25/74, C_a04/C_a05 36/74, D_random 19/74; canonical A 13/13, B 12/13, C 13/13.

---

## 1. What was tested

Scoped claim (not the WebArena headline): in SPIDER's Graph setting, stepwise retrieval scored by
`alpha*cos(task,desc) + (1-alpha)*cos(state_summary,desc)` with pool top-M=max(3k,20) and greedy MMR (lambda=0.7)
addresses executable-correct fragments better than (A) incumbent exact `goal_sig` addressing and
(B) task-text-only embedding retrieval over identical descriptions, under paraphrased goals and shifted entry
contexts — and converts into fewer novel/exploration actions at no success regression.

Library: 12 fragments built by the UNMODIFIED incumbent cold exploration on books.toscrape / quotes.toscrape /
the-internet (all 5 cold tasks succeeded). Queries: 17 included subgoals x {literal, p1, p2} x {route, start,
distractor} contexts; ground truth = execution-based executability of every same-site fragment from every context
(211 probe records, cached and shared by all conditions).

## 2. Results

### Retrieval level (primary metric, hard slice = paraphrase OR entry-shift, correct@1)

| A_native | B_plain | B_mmr | C_a04 | C_a05 | D_random |
|---|---|---|---|---|---|
| 0/74 | 25/74 (.338) | 25/74 (.338) | **36/74 (.486)** | **36/74 (.486)** | 19/74 (.257) |

- Canonical slice sanity: A_native 13/13 (incumbent perfect in its native regime), C 13/13, B 12/13.
- Pairwise C vs strongest B on hard@1: **11 wins to 0 reversals** — strict per-query dominance.
- @3: MMR lifts both B_mmr and C to 68/74 (.919) — reranking helps recall; the state term drives the @1 gain.
- alpha=0.4 vs alpha=0.5 (paper/code discrepancy): **identical rankings everywhere** at this library scale.
- **ERRATUM [R2, repair round 1 — the original example here was factually wrong and is withdrawn].**
  Accurate statement (recomputed from committed `retrieval_eval.json` per-query rows; confirmed by
  independent Auditor recomputation): **all 11 hard-slice C-only wins occur in the
  int.dyn.{nav, ex2, start} cluster family on the-internet** (dynamic-content menu disambiguation;
  e.g., "run the second demonstration" addressed from shifted menu pages where task text alone is
  ambiguous or misleading). **Login and pager clusters show ZERO C-over-B advantage** (identical
  correct@1 rates under B_mmr and C). Per-cluster win counts: int.dyn.nav = 8, int.dyn.ex2 = 2,
   int.dyn.start = 1. The wins remain state-discrimination cases: Auditor-side ablations show fusing a
   wrong-context summary or using a summary-only score falls back to baseline level (both 24/74);
   constant-text fusion controls are not stable under the lexical-hash embedder (Auditor rescan:
   19–36/74 depending on dummy string, due to sha1 bucket collisions at d=512) and are not cited
   as evidence. The stable controls support the narrower statement that the gain requires
   current-state-carried information.

### Downstream conversion (identical incumbent policy; only fragment lookup swapped; library writes disabled for all)

| slice | condition | novel actions (total) | subgoal success | reuse fraction |
|---|---|---|---|---|
| literal (A has native IDs) | A_native | 21 | .900 | .696 |
| literal | B_mmr | 42 | .900 | .641 |
| literal | C_a04/a05 | **39** | .900 | .698 |
| paraphrase p1 (NL consumers; A=0 retrievals) | A_zero | 400 | .600 | .000 |
| paraphrase p1 | B_mmr | 42 | .800 | .650 |
| paraphrase p1 | C_a04/a05 | **36** | **.900** | **.660** |

Cost accounting: state summarizer = deterministic adaptation (no LLM key in environment); would-be LLM calls
≈ 12–13 total; exact split unreconciled at artifact level (collection cache counters record 11 misses across 49
distinct contexts; conversion-run counters record 2 misses, but the committed conversion cache holds only 1 key
not shared with the collection cache), then hash-cache makes marginal cost ~0 (mirrors reference
SHA256-content-hash caching); no metric impact. [Restated repair round 3 per audit RF2 to match committed
artifacts; the earlier "11 + 2" phrasing implied a reconciliation the artifacts do not carry.]

## 3. Frozen-rule verdict

Rule as written (combined conversion aggregate):
1. R1h(C)=36 > R1h(B_mmr)=25 > R1h(A)=0 — strictly ✓
2. Succ(C)=45/50=.90 >= max(.86, .78) ✓
3. Novel(C)=75 < min(Novel(A)=421, Novel(B_mmr)=84) ✓

**Proposed verdict: REPRODUCED_USEFUL**, claim tier ceiling PROOF OF CONCEPT.

### Ambiguity disclosure (recorded, not silently resolved)

The rule did not pin aggregation granularity. Under the STRICTEST per-slice reading, clause 3 fails on the
literal slice: with hand-authored sigs available, incumbent exact addressing remains more action-efficient
(21 vs 39 novel). The mechanism's operational advantage over the incumbent therefore exists exactly and only
in the natural-language-consumer regime — which is the regime SGDR targets and constitution §11 demands
("a future consumer must not need an internal fragment ID"). Against the like-for-like strongest baseline
B_mmr (same embedder, same MMR machinery, minus the state term), C wins on BOTH slices: fewer novel actions
(36<42, 39<42), higher or equal success (.90 vs .80 paraphrase; .90 = .90 literal), plus zero-reversal
retrieval dominance. The verdict follows the preregistered rule as written; the caveat is material and travels
with any downstream claim.

## 4. Validity gates and deviations log

- V1-V6 all pass as frozen (single embedder; hashlib-only scoring path; seeds 20260824 family; condition-independent
  cached ground truth; exclusions uniform and counted: 5 already-satisfied, 2 route-invalid contexts, 4 invalid probes,
  unsatisfiable qids excluded identically for all conditions).
- Collection-stage bugfixes, all PRE-condition-ranking except #3/#4 which occurred when conversion had produced ZERO
  usable rows; none touched rankings, metrics, or the frozen evaluation:
  1. probes stage missing `_frags` scope (crash);
  2. static precondition wrongly required all fragment steps resolvable in the ENTRY snapshot — broke cross-page
     procedures (login flows); replaced by incumbent step-by-step replay semantics; full probe re-collection;
  3. conversion pointed at nonexistent DB filename (crashed with no rows produced);
  4. goal-text builder KeyError on subgoals excluded by the frozen inclusion rule; fixed with public-keywords fallback,
     symmetric across conditions; conversion fully rerun (60/60 clean).
- No tuning of mechanisms, metrics, or success rules occurred after any outcome was visible.

## 5. Honest limits

1. Lexical-hash embedder regime (neural embedder unavailable offline); absolute numbers may differ with real embeddings;
   the C-vs-B contrast is internally controlled by design but the effect size is not transferable untested.
2. Deterministic summarizer replaces the reference LLM summarizer (contract-faithful page-kind + enabled-action-verb
   vocabulary, hash-cached, stub fallback); an LLM summarizer could produce different summary texts.
3. Small scripted-policy setting: 12 fragments, 3 sandbox sites, 10 subgoal types, heuristic agents; tiny n; no
   uncertainty intervals warranted; correlated queries within subgoals.
4. Same-site reuse only — cross-site/cross-domain transfer untested here AND untested by SGDR's authors.
5. WebArena headline numbers (37.5%/24.3% vs AWM/ASI/CER) were NOT reproduced — out of scope by prereg.
6. Insert-time dedup, sliding-window induction, verification prompts: not reproduced (out of isolation scope).
7. Mechanical descriptions are weak keys for some clusters (books travel/open-first/paginate stay unsolved at hard@1
   for ALL text conditions) — description quality, not fusion mechanism, is the binding constraint there.

## 6. Suggested next questions (for Intel Director / Graph lane)

- Does the state-grounding advantage survive a neural embedder and an LLM summarizer (the two disclosed adaptations)?
- Does fused retrieval still win when the fragment library is 10x larger (MMR/top-M become load-bearing)?
- Can mechanically-derived descriptions be upgraded without hand-authoring (the residual failure mode found here)?
