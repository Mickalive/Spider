# PB-001 OPTIMIZATION RATIONALE — v2 (frozen before any outcome)

Beta: **PB-001** · Author: BETA ARCHITECT · Date: 2026-08-25
Charter: `directives/PRODUCT_OPTIMIZATION.md` (binding) · Request: `state/product_beta_request.json` rev 4
Basis: no Phase-A/B outcome exists anywhere in the repository or mounts (verified this session).
This document records the optimization program admission record, the bottleneck analysis, the
technically distinct variants considered BEFORE outcomes, and the selection justification for the
one change v2 makes relative to the preserved v1 freeze.

---

## 1. Program admission record (charter §2)

| Field | Record |
|---|---|
| Process under optimization | Candidate-fragment addressing/ranking for free-form natural-language goals in a memory-led browser-agent execution loop ("the front door") |
| BOTTLENECK | Retrieval ranking under paraphrase + entry-state shift — evidence-cited below (§2) |
| BASELINE | B0 cold same-backbone ReAct browser agent (`LOCALLY_REPRODUCED`: reference implementation built and run inside the frozen harness, hash-pinned at F1; representative of the mainstream open ReAct browser-use pattern, not a vendor product) · B1 AWM-class trajectory-prompt memory (`LOCALLY_REPRODUCED` instantiation of an externally-claimed class; mandatory comparator per constitution §13) · B2 exact replay (diagnostic). Context competitors Stagehand/Healenium/Skyvern/AWM headline numbers: `EXTERNAL_CLAIM_ONLY`, never baselines of record |
| METRICS | Prereg §6 verbatim (success, actions novel/reused, calls/tokens, perf_counter latency, reuse share, discipline events) |
| WIN RULE | Prereg §8 verbatim: Director floor clauses 1–4 + architect tightenings 5–7. Frozen; cannot be moved after outcomes |
| SCOPE CAP | Request `maximum_scope` verbatim (≤4 demo sites, ~30–60 rows, internal only) |
| KILL CONDITION | Request `kill_condition` verbatim |

## 2. Bottleneck identification

The product claim is "pay the cost of novelty, not the cost of the whole task." Decomposing the
SPIDER arm's pipeline against the accepted evidence:

| Stage | Status of evidence | Verdict |
|---|---|---|
| Store / exact replay / entry-reset | G-H1 audited: 0 novel actions on matched routes | NOT the bottleneck |
| Procedure packaging + iterative replay policy | G-H3 E2 / G-H4 R3 audited: login frag 16/16 vs graphiter 0/8; frag 4/4 vs edge-replay 0/4 | NOT the bottleneck |
| Executor plumbing with real LLM consumer | untested (A1) — but shared by all arms, so it cannot explain a treatment-specific failure | measured, not assumed |
| **Candidate ranking for free-form NL goals** | G-H3: held-out paraphrase retrieval@1 = 2/8 (weak); G-H4 V31 lifted it to 6/8 positives-only on a SPENT instrument; Intel cycle-1 (audited PASS, PoC tier): task-text-only ranking 25/74 hard@1 vs fused task+current-state-summary ranking 36/74, 11 paired wins / 0 reversals, wrong-context-summary fusion falls back to baseline level (24/74); converted into fewer novel exploration actions at equal-or-higher subgoal success in the NL-consumer regime (39 vs 42 literal; 36 vs 42 paraphrase) | **THE bottleneck** |
| Cross-site prediction / routing | Physics WP-003B-R2 + WP-005 FALSIFIED (audited) | excluded by falsification |

Interpretation: on repeat/near-repeat tasks the arm's savings are realized only if the right
stored procedure is selected from raw goal text when wording is paraphrased and the entry state has
shifted. The audited mechanism that specifically addresses this — grounding candidate scores in the
CURRENT STATE summary in addition to the goal text — is exactly what the task-only channel lacks;
the audit's ablation controls localize the gain to the state-grounding term, not to MMR or pooling
machinery (B_mmr alone = 25/74 = B_plain).

## 3. Technically distinct variants considered (pre-outcome)

All variants were evaluated on mechanism type, not implementation detail:

| ID | Variant | Mechanism type | Disposition |
|---|---|---|---|
| V-A | **SGDR-style fused scoring**: α·cos(task,desc)+(1−α)·cos(state-summary,desc), α=0.4, pool top-M=max(3k,20), greedy MMR λ=0.7, lexical-hash embedder, deterministic contract-faithful summarizer; V31 retained as preprocessing | replaces the RANKING layer over the same auto-derived descriptions; eligibility gate untouched | **SELECTED** (Director-directed and independently justified: only variant with audited pre-outcome evidence aimed at exactly this bottleneck) |
| V-B | Same fused formula but neural embedder + LLM summarizer | representation upgrade of V-A | REJECTED for this version: explicitly unvalidated adaptations (Intel gate residual limits); forbidden mid-beta by the directive; would also add provider cost asymmetrically to the treatment |
| V-C | Re-enable keyword/goal_sig channel or hand-authored signatures | addressing by store keys | REJECTED: violates A2 (free-form goals without signatures) and blind discipline; hand-authored exact signatures remain more action-efficient where they exist per Intel gate wording — but authoring them per task is precisely the cost the product removes |
| V-D | LLM/cross-encoder reranking of retrieved candidates | learned reranker | REJECTED: no audited evidence; adds model calls inside treatment totals; conflates A2 with a new unvalidated component |
| V-E | Keep v1 desc_only coverage scorer, retune TAU/MIN_MATCH thresholds | threshold tuning | REJECTED: outcome-blind guesswork; no audited support; risks inflating false accepts (the known failure mode) instead of fixing ranking |
| V-F | Hybrid cascade (fused score first, coverage fallback) | two-channel composition | REJECTED for v2: changes more than the directed single component, muddies attribution of any A2 outcome, and the combination is unevidenced. Recorded as a candidate for a future version IF v2's failure taxonomy shows gate-pass-but-misranked events |

Stepwise *dynamic* re-scoring (retrieving again at each subgoal with refreshed state summaries,
as in the reference SGDR loop) was also considered and DEFERRED: adding retrieval call sites would
be a second semantic change beyond the directed one and would blur attribution. The v2 change is
confined to the existing whole-goal retrieval event's scoring internals. This is a disclosed scope
limitation of A2's test: v2 tests end-to-end serving with entry-state grounding, not mid-trajectory
re-addressing.

## 4. Why the selected change is an actual optimization

- It changes the arm's decision boundary: which fragments become candidates for procedures versus
  exploration — the quantity that determines reused-vs-novel action mix, the primary savings channel.
- It is not repackaging: the scored objects, call sites, planner, executor and UNKNOWN discipline
  are unchanged; the ONLY altered computation is the ordering function over gate-passing candidates.
- Its expected effect direction and magnitude are anchored by an independent audited measurement
  (PoC tier): strictly more correct@1 selections than the v1-equivalent channel under exactly the
  panel's stressors (paraphrase + shifted entry contexts), with benign fall-back when the state
  summary is uninformative.
- It is measurable end-to-end: if the optimization fails to survive the LLM consumer (A1/A2), the
  win rule fires LOSE and PH-1 is downgraded — the beta remains decisive either way.

## 5. Operationalization frozen in the prereg (disclosed interpretation)

The directive fixes formula, α, pool, λ, embedder, summarizer, V31 retention and forbids neural/
LLM adaptations. One compositional detail required an architect decision, disclosed here and in
prereg §0/§3 so the auditor can check it:

> The frozen goalsig eligibility gates (TAU=0.30 coverage ∧ MIN_MATCH=2 matched pairs, DF-pruned,
> COV_CAP=6) are RETAINED as the OK|UNKNOWN gate; the fused score+MMR replaces only the RANKING
> among gate-passing candidates.

Rationale: the directive requires degrading "per unchanged UNKNOWN thresholds"; a pure cosine
scorer has no natural OK|UNKNOWN boundary, so preserving the audited gate constants is the only
reading that changes exactly one thing while keeping false-match protection identical to v1.
Consequences: RETRIEVER_MISS semantics unchanged; MMR diversity applies within the gate-passing
pool only; tie-break to lower fragment id copied from the audited implementation.

## 6. Fairness accounting deltas introduced by v2

- Baselines B0/B1/B2: prompts, corpora, budgets, code paths byte-identical to v1. No baseline
  capability changed.
- Treatment overhead: summarizer/embedder/MMR are CPU-side, harness-executed; their wall-clock is
  captured inside SPIDER `stage_ms_perf.retrieval`; they issue ZERO provider calls; token/call
  totals come exclusively from provider usage fields (no synthetic billing). Net effect: the swap
  can only hurt SPIDER's wall-clock clause, never help it — no hidden subsidy.
- Information symmetry: the current-state summary is derived from the observation every arm
  receives; no oracle information is injected. The acceptance predicate stays equally disclosed.
- Store hygiene unchanged: byte-restored KB per row, evaluation write-suppression asserted.

## 7. Wording-constraint inheritance register (charter §6 — travels into every beta output)

From Intel gate CYCLE_32800296360 (binds every use of the SGDR block):
1. Evidence tier PROOF_OF_CONCEPT; GENERALIZATION language of any kind forbidden.
2. "Beats the incumbent" unqualified — forbidden.
3. Combined Novel(C)=75 < min(421,84) may not be cited without budget/regime caveat.
4. Any claim that login/pager addressing improved — forbidden (none observed).
5. Constant-dummy-text 24/74 ablation figure may not be cited as evidence.
Plus carried limits: lexical-hash embedder + deterministic-summarizer regime; tiny library/sites;
hand-authored exact signatures remain more action-efficient where they exist; WebArena headline
numbers NOT reproduced and forbidden in any narrative; clean-room lineage only — never copy the
CC BY-SA reference source.
From Graph G-H4: no quantitative V31 retrieval-transfer rates in any beta output (instrument spent);
V31 is equipment only. From Physics: no predictive-dynamics feature or language anywhere.

## 8. Post-outcome versioning paths (charter §4 — declared now, decided later)

- WIN ⇒ next version only via a new freeze on untouched evidence (e.g., scale/library growth,
  stepwise dynamic re-scoring V-F/V-A composition) — each requiring its own admission record.
- LOSE ⇒ authorized repair versions must name the measured bottleneck from the failure taxonomy
  (e.g., gate-pass-but-misranked ⇒ consider V-F cascade; summary_status=fallback-dominated ⇒
  summarizer quality program; both require new freezes).
- Two consecutive MEASUREMENT_INVALID batches stop the program pending infrastructure repair.
