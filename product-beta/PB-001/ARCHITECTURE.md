# PB-001 ARCHITECTURE — Inherited Operational Memory Beta (SPIDER arm vs current-agent baselines) — v2

Beta: **PB-001** · Hypothesis: **PH-1** · Authorized: `state/product_beta_request.json` rev 4 (2026-08-25)
Architect freeze date: **2026-08-25** (v2) · Status: **READY** (see `state/product_beta_architecture.json`)
Binding benchmark: `BENCHMARK_PREREG.md` **v2** (frozen BEFORE any Phase-B outcome) · Interfaces: `INTERFACES.md` v2 ·
Build order: `BUILD_PLAN.json` plan_version 2.0 · Optimization rationale: `OPTIMIZATION_RATIONALE.md`

**v2 status basis**: no Phase-A/B outcome exists anywhere in the repository or mounts (re-verified
2026-08-25 against HEAD `2bf3c2b` and all remote branches). The v1 freeze
(`cycle/product/32799261473/architect`) is preserved provenance. v2 implements exactly ONE semantic
change directed by the Product Director before any outcome — the SPIDER-arm candidate scoring layer —
and re-freezes everything else verbatim (see `BENCHMARK_PREREG.md` §0 Delta, and `OPTIMIZATION_RATIONALE.md`).

---

## 0. Design goal and non-goals

This is the **smallest instrumented system that can honestly decide** whether SPIDER-style
inherited operational memory gives a real operational advantage to a real LLM browser agent on
repeat/near-repeat web tasks, versus a credible current-agent baseline. It is an internal
benchmark harness, not a product implementation.

Non-goals (hard exclusions, from the beta request):
- No production deployment, no public users, no commercialization, no external data sharing.
- No cross-site skill-transfer claims; no marketplace/sharing surface.
- No category-type goals as primary endpoints; no >3-distinct-fragment chains (Graph
  graph-inheritance-scaling territory — tracked descriptively only).
- **No predictive-dynamics feature of any kind** (Physics WP-003B-R2/WP-005 FALSIFIED, audited).
- No route/API-capture-replay or registry feature (Unbrowse-class claims OFFICIAL_CLAIM vendor-run
  only; Intel cycle-2 reproduction pending).
- No quantitative V31 retrieval-transfer claims anywhere in beta outputs (G-H4 fresh instrument is
  SPENT; V31 enters strictly as adopted equipment).
- No neural embedder and no LLM summarizer anywhere in this beta version (both are explicitly
  unvalidated adaptations of the audited SGDR configuration; Intel gate residual limits).

## 1. One-runtime, three-arm architecture

Unchanged from v1: **all arms run inside one frozen agent runtime** with identical observation
space, action space, budgets, decoding policy, backbone model and acceptance-predicate information.
The arms differ ONLY in what memory, if any, is injected:

```
                         ┌──────────────────────────────────────────────┐
                         │              AgentRuntime (frozen)           │
   task row ───────────► │  obs serializer → LLM policy → action exec   │
   (start URL, goal      │  budgets · perf_counter timers · JSONL log   │
    text, anchored       └───────┬──────────────────┬───────────────────┘
    predicate)                   │                  │
                     memory block │                  │ action primitives
                                 ▼                  ▼
                    ┌────────────────────┐   ┌─────────────────────────┐
   ARMS:            │ B0  cold ReAct     │   │ shared/browser Session   │
   ─────────        │ B1  + trajectory   │   │ (vendored, audited)      │
                    │     prompt memory  │   │ health-gated snapshots   │
                    │ SPIDER + procedure │   └─────────────────────────┘
                    │     store memory   │
                    └─────────┬──────────┘
                              ▼
                    ┌──────────────────────────────────────────────────┐
                    │ spider_mem (vendored validated blocks):          │
                    │ Store(SQLite states/transitions/fragments)       │
                    │ goalsig blind gate (UNKNOWN thresholds frozen)   │
                    │ fusion_scorer = SGDR-style fused task+state      │
                    │   summary ranking (lexical-hash embedder,        │
                    │   deterministic summarizer, MMR λ=0.7) [v2]      │
                    │ equipment_v31 (preprocessing ONLY)               │
                    │ iterative ProcedureExecutor (verify/replay/reset)│
                    │ UNKNOWN discipline · anchored predicates         │
                    │ KB dump/rebuild/hash · write suppression         │
                    └──────────────────────────────────────────────────┘
```

Strawman risk is handled structurally, not rhetorically: generous equal budgets (prereg §7), a
**baseline validity gate** (B0 must pass pilot smoke tasks before evaluation), and a win rule that
names **B1 (memory vs memory)** as the reduction comparator whenever it beats or ties B0
(constitution §13: memory-beating-no-memory is insufficient). Baseline capability is untouched by
v2 — the scoring swap is inside the SPIDER arm only.

## 2. Component map (v2)

| # | Component | Path (under `product-beta/PB-001/`) | Origin / provenance |
|---|---|---|---|
| C1 | `spider_mem/store` | `spider_mem/store.py` | vendored `graph/store.py` @ lab/graph `d41fe9b` (G-H1; counter-bug fix included) |
| C2 | `spider_mem/goalsig` | `spider_mem/goalsig.py` | vendored `graph/goalsig.py` @ `d41fe9b` (G-H2 constants TAU/MIN_MATCH/TOPK/DF_KEEP/COV_CAP). **v2 role: eligibility GATE only** |
| C3 | `spider_mem/equipment_v31` | `spider_mem/equipment_v31.py` | winning arm extracted from `graph/score_variants.py` @ `d41fe9b` (G-H4). EQUIPMENT/PREPROCESSING ONLY |
| C4 | `spider_mem/accept` | `spider_mem/accept.py` | vendored `graph/accept.py` @ `d41fe9b` (anchored path predicates, G-H3 E4) |
| C5 | `spider_mem/absence` | `spider_mem/absence.py` | adapted `graph/absence.py` (route-absence adjacent-pair test + depth-bound extension) |
| C6 | `spider_mem/kbfile` | `spider_mem/kbfile.py` | adapted `graph/rebuild_store.py`: dump/rebuild + sha256 byte-restore proofs |
| C7 | `runtime/session` | `runtime/session.py` | vendored `shared/browser.py` @ `d41fe9b` (raw observation capture, health floors) |
| C8 | `runtime/react` | `runtime/react.py` | NEW frozen reference ReAct loop (prompt templates fixed in prereg Appendix P) |
| C9 | `runtime/llm` | `runtime/llm.py` | NEW provider adapter contract (usage-token accounting mandatory) |
| C10 | `arms/b0`, `arms/b1`, `arms/spider` | `arms/*.py` | thin adapters over C8/C9; memory sources differ only |
| C11 | `harness/driver` | `harness/driver.py` | NEW row lifecycle, seeded schedule, KB restore per row, write-suppression assert, artifact writer |
| C12 | `producer` | `producer/run_phase_a.py` | producer cold-exploration + fragment saving adapted from Graph explorer producer path (PRODUCER-ONLY, disabled at evaluation) |
| C13 | `analysis/frozen` | `analysis/compute_verdict.py` | NEW mechanical win-rule evaluator (hash-pinned at F2 freeze) |
| C14 | `spider_mem/hash_embed` | `spider_mem/hash_embed.py` | vendored `intel/experiments/sgdr_repro/embedder.py` @ lab/intel `fca0acb` (lexical-hash embedder, sha1 bucketing) **[v2]** |
| C15 | `spider_mem/state_summarizer` | `spider_mem/state_summarizer.py` | vendored `sgdr_repro/summarizer.py` @ `fca0acb` (deterministic contract-faithful state summary + content-hash cache + fallback stubs) **[v2]** |
| C16 | `spider_mem/frag_describe` | `spider_mem/frag_describe.py` | vendored `sgdr_repro/descriptions.py` @ `fca0acb` (mechanical fragment-description derivation; verb vocabulary shared with C15) **[v2]** |
| C17 | `spider_mem/fusion_scorer` | `spider_mem/fusion_scorer.py` | adapted `sgdr_repro/retriever.py` @ `fca0acb`: FragmentBank embed cache, fused relevance, greedy MMR (λ=0.7, pool top-M=max(3k,20)=20, tie→lower id); A/D condition machinery stripped; composed AFTER the C2 gate **[v2 — THE directed change]** |

Vendored files carry provenance headers (`origin: lab/graph@d41fe9b <path>` /
`origin: lab/intel@fca0acb intel/experiments/sgdr_repro/<path>`) and their sha256s enter the build
manifest (freeze F1). The Builder must not modify mechanism semantics during vendoring; required
adaptations are listed per-file in `BUILD_PLAN.json`. Clean-room discipline: SGDR lineage vendors
ONLY from `intel/experiments/sgdr_repro/`; the CC BY-SA reference source is never copied.

## 3. Data flow (row lifecycle) — unchanged

1. **Row init**: fresh incognito browser context; cookies/storage empty; KB SQLite file restored
   byte-exactly from frozen dump copy; sha256(before) recorded.
2. **Health gate**: HTTP probe floors + DOM floors (`dom_bytes ≥ 2000`, `elements ≥ 5`) at entry;
   trip ⇒ row INFRA_EXCLUDED symmetrically for all arms (never counted against any arm).
3. **Arm execution** (one of B0/B1/SPIDER) under budgets: MAX_STEPS=30 actions, MAX_LLM_CALLS=60,
   MAX_ROW_TOKENS=200k, WALL_S=600 s. All LLM calls and all browser primitives logged with
   `perf_counter` timestamps and source tags.
4. **Outcome judging**: the harness — never the agent — evaluates the anchored predicate on the
   final state and verifies navigation-chain integrity. Success/failure is machine-judged.
5. **Write-suppression assert**: sha256(after) == sha256(before); store row counts unchanged.
6. **Artifacts**: append row record + full event JSONL; next row.

Producer phase (Phase A) runs ONCE before evaluation, using C12 with the same health gates,
to grow the knowledge base from 8 training tasks; its successful trajectories simultaneously
form B1's prompt-memory corpus (same experience, different packaging — what makes SPIDER-vs-B1 an
attribution test of *packaging*, assumption A3).

## 4. Assumption isolation matrix

| Assumption (from request) | Isolating contrast | Mechanism flags |
|---|---|---|
| A1 inheritance survives a real LLM consumer | SPIDER arm (LLM consumer) vs accepted scripted-consumer history; internally SPIDER vs B0/B1 with same LLM | `consumer=llm` everywhere in Phase B |
| A2 free-form NL goals served end-to-end by the audited fused scorer, w/o hand-authored signatures | R1/R2 goal texts carry no keywords/sigs; retriever consumes raw text (+ current-state summary) only; keyword channel DISABLED; V31 retained as preprocessing only | `query_mode=desc_only`, `equipment=v31`, `scorer=fused_sgdr_a04` |
| A3 packaged procedures > edge iteration AND > prompt-level trajectory memory | SPIDER vs B1 primary; edge-iteration ablation = capped diagnostic slice (≤6 rows, outside win-rule panel) | `arm=b1` vs `arm=spider`; ablation flag `memory.mode=edge_iter` |
| A4 savings material in tokens/calls/wall-clock | first-ever cost instrumentation of stack: usage tokens per call, perf_counter stage timers; summarizer CPU time lands inside SPIDER's `stage_ms_perf.retrieval` | instrumentation always on |
| A5 known failure modes contained | R3 novel-control rows + UNKNOWN/false-match discipline events + descriptive category-prefix logging | `regime=R3`, discipline ledger |

Unvalidated-mechanism isolation rule: components NOT among the validated building blocks
(store+replay+reset; blind retrieval gate; oracle-equalized iterative replay; login-procedure
packaging; V31-as-equipment; SGDR fused scoring at PoC tier in its validated configuration) are
NEW beta code (C8–C13 plumbing) and stay flag-separable so a failure can be attributed to new
plumbing rather than validated mechanisms. The C14–C17 stack is vendored verbatim from the audited
Intel reproduction and fixture-proven byte-faithful before it touches the product store (WP-0).

## 5. Memory-led execution model (SPIDER arm) — v2 scoring layer

1. **Whole-goal retrieval** on raw goal text (V31 canonicalization both sides, unchanged).
   Candidate eligibility: the FROZEN goalsig gate decides OK vs UNKNOWN exactly as in v1 —
   matched-pairs ≥ MIN_MATCH=2 AND coverage ≥ TAU=0.30 with DF-pruning and COV_CAP=6, on the same
   auto-derived token channels. Nothing clears the gate ⇒ explicit `UNKNOWN` (no fabrication),
   degrade to primitives/explore. Among gate-passing candidates, RANKING is the single changed
   component: fused score
   `score(f) = α·cos(E(goal_text), E(desc_f)) + (1−α)·cos(E(summary(state_t)), E(desc_f))`
   with α=0.4, E = lexical-hash embedder (C14), desc_f = mechanically derived fragment description
   (C16), `summary(state_t)` = deterministic contract-faithful summarizer output (C15) on the
   CURRENT observation at retrieval time (entry state at task start); pool = gate-passers capped to
   top-M=max(3k,20)=20 by fused score; greedy MMR λ=0.7 selects k=TOPK=3 with tie-break to lower
   fragment id. Retrieval call sites are UNCHANGED from v1 (one whole-goal retrieval event; no new
   retrieval events were added).
2. **LLM plan step** (counts toward budgets): model receives candidates + auto-derived descriptions
   (C16 text) and returns a JSON plan: ordered procedures to apply + free-text residual subgoals
   (≤4). The LLM may reject retrieved candidates (real-consumer selection, A1/A2).
3. **Procedure application**: replay steps with per-step verification (post-state fingerprint /
   subgoal anchor); entry-precondition mismatch triggers reset-retry (MAX_RESETS=2), then fallback
   to exploration. Iterated procedures (pager) apply up to MAX_APPLICATIONS=6.
4. **Residual exploration**: remaining subgoals executed by the SAME ReAct loop, tagged
   `exploration` (novel). Memory-solved claims require anchor-true observation — otherwise the
   event is a fabricated-success violation (win-rule breaker).
5. All retrieval/planning/summarization overhead is INSIDE SPIDER's measured totals:
   summarizer+embedder+MMR run harness-side but their wall-clock lands in
   `stage_ms_perf.retrieval` within SPIDER rows; they make ZERO provider calls (tokens/calls come
   from provider usage fields only); would-be-summary-miss counters are logged descriptively
   (`summary_stats`), never billed as synthetic calls (fairness floor: provider accounting only).

Known benign degradation mode, disclosed from audit controls: fusing a WRONG-context summary falls
back to task-only-retrieval level (24/74 vs 25/74 hard@1 in the audited PoC); i.e., the state
channel cannot be expected to help where the entry snapshot is uninformative, and may not hurt
below baseline level. No login/pager addressing improvement is claimed or expected from this change
(audit wording constraint — it binds reporting, and the panel keeps login/pager tasks so the claim
stays testable end-to-end).

## 6. Instrumentation architecture — unchanged plus descriptive fused-scoring capture

- `perf_counter()` float timings per row and per stage (`retrieval_ms`, `llm_ms`, `browser_ms`);
  NO integer-ms flooring for beta metrics (G-H4 hygiene).
- Per-call provider `usage` (prompt/completion tokens) captured from API responses; summed per row.
- Action mix tags: `memory_procedure` | `memory_guided` | `exploration` (uniform across arms;
  B1 actions following injected trajectories are `memory_guided`).
- Store sha256 before/after every row; write-suppression assertion hard-fails the batch.
- Health gate per row (HTTP + DOM floors); environment probes recorded per batch.
- **v2 addition (descriptive only)**: each retrieval event logs `n_gate_pass`, fused score vector
  of the selected candidates, `alpha_used`, `mmr_lambda_used`, `pool_size`,
  `summary_status ∈ {hit, miss, fallback}`, accumulated `summary_stats`. No win-rule clause reads
  these fields; they exist so the auditor can attribute RETRIEVER_MISS/FALSE_ACCEPT events to
  gate-vs-ranking stages.
- Failure taxonomy (first_failure_class): RETRIEVER_MISS, RETRIEVER_FALSE_ACCEPT,
  PLANNER_MISPLAN, PROCEDURE_EXEC_FAIL, PRECONDITION_MISMATCH, VERIFY_FAIL, RESET_EXHAUSTED,
  EXPLORE_BUDGET_EXHAUSTED, PROVIDER_ERROR, HEALTH_TRIP — every non-success row carries one.
- Raw rows + events + manifest + analysis code committed with seeds and freeze timestamps.

## 7. Fairness architecture — unchanged

1. One runtime, one obs/action space, one decoding policy (temperature=0, seed where supported),
   identical budget ceilings across arms.
2. The machine-checkable acceptance predicate is part of the task definition given IDENTICALLY
   to all arms (removes the G-H2/G-H4 oracle asymmetry).
3. KB byte-restored before every row; evaluation writes nothing (asserted).
4. Same producer experience feeds SPIDER's KB and B1's trajectory corpus.
5. B1 retrieval volume parity: top-k=3 trajectories vs SPIDER TOPK=3 candidates; rendered
   memory-block sizes bounded comparably (≤1800 tokens) and naturally costed.
6. Baseline validity gate: B0 must solve ≥2/3 pilot smoke tasks (disjoint from panel) before
   Phase B; failure ⇒ MEASUREMENT_INVALID, not a win.
7. No hints to SPIDER that B0/B1 lack: goal texts, start URLs, credentials and predicates are
   byte-identical inputs; paraphrases authored independently of panel construction.
8. The v2 scoring swap touches ONLY the treatment arm's ranking internals; baselines' prompts,
   corpora, budgets and code paths are byte-identical to v1. Treatment overhead (summarizer,
   embedding, MMR) is measured inside SPIDER totals — if anything this works against the
   treatment's wall-clock clause.

## 8. Compute & scope caps — unchanged

- ≤ 4 sites (panel uses 2; reserve pool additions only via the disclosed preflight contingency);
  60 outcome rows (10 tasks × 3 arms × 2 passes) + ≤4 B2 sanity rows + 3 pilot rows + ≤6
  diagnostic ablation rows.
- Total compute cap: ≤ 25M tokens and ≤ 4000 LLM calls across ALL phases, continuously logged;
  projected overrun ⇒ halt with partial artifacts and disclosure (BLOCKED/partial). The v2 scorer
  adds zero provider calls by construction.
- One backbone model family per beta version; model id/version pinned at F1 before outcomes.

## 9. Risks and structural mitigations (v2)

| Risk | Mitigation |
|---|---|
| Live-site drift mid-benchmark | per-row health gates, symmetric exclusion, frozen reserve-task swap rule (preflight only), two-pass replication |
| Provider nondeterminism | temperature=0 + seed; replication interpreted as flake-guard, not sampling inference (disclosed) |
| Strawman accusations (either direction) | single-runtime equality + baseline validity gate + B1-primacy comparator rule |
| Fabricated successes | harness-judged predicates, nav-chain integrity, zero-tolerance violation rule |
| Memory-induced wrong actions | per-step verification, reset caps, UNKNOWN discipline, false-match ledger |
| Quotes login redirect instability | element-anchored predicate, B2 sanity replay must confirm before Phase B, reserve auth task predeclared |
| **v2**: fused ranking misleads where entry summary is uninformative | audit controls show graceful fall-back to baseline level, not below; UNKNOWN gate unchanged; descriptive `summary_status` logging enables attribution; failure class RETRIEVER_MISS preserved |
| **v2**: vendor drift between Intel repro and beta copy | WP-0 offline fixture must reproduce committed cycle-1 numbers (36/74 vs 25/74 hard@1; 11 wins/0 reversals) byte-exactly BEFORE any product-store integration; mismatch ⇒ BLOCKED, never approximate |

## 10. Handoff

- `READY` ⇒ Beta Builder implements exactly `BUILD_PLAN.json` work packages without inventing
  essential rules; freeze checkpoints F1/F2 gate any outcome collection.
- Any post-F2 change to panel/prompts/thresholds/baselines/win rule quarantines results as
  exploratory and forces a new preregistration version (constitution §19 discipline).
- Kill conditions inherited verbatim from the beta request; ARCHITECTURE_BLOCKED path was
  evaluated and NOT triggered (an honest benchmark is constructible within scope).
