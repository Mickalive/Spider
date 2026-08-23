# TEAM GRAPH — Run 1: Cumulative Inheritance Experiment

Date: 2026-08-23 · Live websites · Playwright/Chromium · scripted heuristic agents
(no LLM in the loop; policies stand in for model diversity, G10 proxy)

## AUDIT STATUS

**Status: PROOF OF CONCEPT, NOT YET A GENERAL DEMONSTRATION.**

The original run report incorrectly claimed an **8.5× wall-clock speedup on
identical tasks**. That number compared non-matched condition averages and was
dominated by a 163 s failed/partial Wikipedia cold task. On the three tasks
that are actually identical in cold and replay (`Q_login`, `I_login`,
`B_travel_first_book`), mean wall time is 2.822 s cold vs 2.816 s replay:
**1.002×**, i.e. no meaningful wall-clock speedup in this scripted setting.

The useful result survives in a narrower form: exact replay produced **zero
novel decisions/actions** on the matched known routes. Because no LLM was in
the loop, this experiment was not designed to turn decision elimination into
wall-clock savings.

A separate audit also found a positional INSERT bug in the run-1 fragment
store initialization (`success_count` received a timestamp and `created`
received 1). The code is corrected in the audited branch. Therefore run-1
confidence values must not be treated as calibrated evidence.

## Design

- **Corpus**: 12 tasks / ~30 subgoals across 4 live sites
  (books.toscrape.com, quotes.toscrape.com, the-internet.herokuapp.com,
  en.wikipedia.org).
- **Store**: SQLite (`graph/store.py`) — states, actions, transitions and
  subgoal-keyed fragments.
- **Agents**: `agentG` keyword-ranker policy; `agentB` DOM-order walker
  policy. These are two scripted policies, not two independent LLMs.
- **Conditions**: `cold` → `inherit` → `replay`.
- Raw historical data: `results/graph/run1_20260823_095958.json`.

## Audited headline metrics

### Matched exact replay

| task | cold wall ms | replay wall ms | cold novel | replay novel |
|---|---:|---:|---:|---:|
| Q_login | 2812 | 2794 | 4 | 0 |
| I_login | 2940 | 2956 | 4 | 0 |
| B_travel_first_book | 2715 | 2699 | 2 | 0 |

Matched mean wall time: **2822 ms cold vs 2816 ms replay (1.002×)**.

### Cross-task composition

The three `inherit` composite tasks used 16 reused and 7 novel actions in
aggregate: **69.6% action reuse**. This is a valid proof that the implemented
system can consume previously stored fragments across tasks under the scripted
setup. It is **not yet evidence of general autonomous decomposition** because
subgoals, goal signatures and success predicates were hand-specified and the
composites were selected in a setting where useful fragments were known to
exist.

## What run 1 actually supports

1. **Known-route replay can eliminate new decisions.** On the three matched
   tasks above, all replayed actions were reused and no novel action was
   required.
2. **Fragment composition is operationally possible.** In the chosen composite
   tasks, about 70% of actions came from previously stored fragments.
3. **Entry-state reset retry is a useful engineering mechanism.** A fragment
   whose entry context is missing can sometimes be recovered by re-establishing
   the entry region rather than discarding the whole fragment.
4. **Policy-format portability has a weak proxy demonstration.** `agentG`
   produced knowledge consumed by `agentB`; because both are scripted
   heuristics, this does not yet establish model-agnostic LLM transfer.
5. **Negative result retained:** huge unstructured pages defeated these
   heuristic policies regardless of memory.

## What run 1 does NOT support

- no 8.5× wall-clock acceleration claim;
- no calibrated empirical confidence claim from run-1 stored counters;
- no proof that natural-language tasks are automatically decomposed into
  reusable fragments;
- no proof of cross-model transfer;
- no proof of cross-site universal skills;
- no claim that no competing system has a comparable combination of
  mechanisms. The ecosystem survey supports only "not identified in the
  systems inspected".

## Required next tests

1. Add invariant tests for fragment counters/timestamps and confidence.
2. Measure **decision cost**, LLM calls/tokens, browser interactions and
   novelty separately from network/page-load wall time.
3. Blind composition: hide complete target route, require sequence absent from
   training, and evaluate retrieval/decomposition without hand-selecting the
   needed fragments.
4. Compare against nearest-route retrieval, trajectory memory, concrete graph,
   and strong current browser-memory baselines.
5. Run ≥20 sequential agents on a growing store to obtain a real
   exploration-cost-vs-knowledge curve.
6. Calibrate staleness/recency only from observed future validation outcomes.
