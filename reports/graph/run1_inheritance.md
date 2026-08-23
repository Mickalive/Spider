# TEAM GRAPH — Run 1: Cumulative Inheritance Experiment

Date: 2026-08-23 · Live websites · Playwright/Chromium · scripted heuristic agents
(no LLM in the loop; policies stand in for model diversity, G10 proxy)

## Design

- **Corpus**: 12 tasks / ~30 subgoals across 4 live sites
  (books.toscrape.com, quotes.toscrape.com, the-internet.herokuapp.com,
  en.wikipedia.org). Tasks span navigation, form/login flows, async
  dynamic content, pagination, info-extraction.
- **Store**: SQLite (`graph/store.py`) — states (raw gzipped snapshots +
  structural fingerprints), actions, transitions with outcome/error class,
  fragments keyed by subgoal descriptor (`goal_sig` + generic classes like
  `generic.form.login`), success/failure counts, recency-weighted Laplace
  confidence.
- **Agents**: `agentG` keyword-ranker policy; `agentB` DOM-order walker
  policy. Independent policies consuming ONE shared store.
- **Conditions**: `cold` (no reads) → `inherit` (fragment replay w/
  entry-state reset retry; novelty localized to glue) → `replay`
  (exact re-validation).
- Raw data: `results/graph/run1_20260823_095958.json`

## Headline metrics (per task averages)

| condition | n | actions | reused | novel | fail | wall s | subgoal succ |
|---|---|---|---|---|---|---|---|
| cold first exploration | 6 | 12.33 | 0.00 | 12.33 | 0.67 | 31.3 | 0.90 |
| inherit composites     | 3 | 7.67  | 5.33 | 2.33  | 0.00 | 28.8* | 0.90 |
| exact replay           | 4 | 4.50  | 4.50 | 0.00  | 0.00 | 3.7   | 1.00 |

\* inherit wall time dominated by one 74s async-wait outlier (I_COMPOSITE);
median inherit ≈ 8s vs cold median ≈ 18s. Exact replay = **8.5× wall-clock
speedup** over cold on identical tasks, with zero novel actions.

## Key findings

1. **Full-route replay eliminates exploration entirely.** All 4 replays:
   100% reused actions, 0 failures, success 1.0. Cached selector-level
   fragments survived across fresh browser contexts (no session cookies).
2. **Cross-task fragment composition works when entry context is handled.**
   Q_COMPOSITE (login ⊕ deep-pagination — parts learned under different
   tasks) succeeded under a DIFFERENT policy (agentB): 10 actions,
   6 reused, 1 recovery. B_COMPOSITE: 3/3 steps pure reuse, 0 novel.
3. **Entry-state anchoring is the dominant failure mode of naive replay.**
   Fragments learned from region A fail to fire from region B
   (`/secure` has no sidebar link to Dynamic Loading). The implemented
   *reset-to-entry retry* (goto known entry, re-replay) converted a hard
   failure into 7 reused + 3 novel glue actions. Novelty localization is
   real and measurable.
4. **Policy transfer (G10 proxy) holds**: knowledge produced by agentG was
   productively consumed by agentB (walker) — reuse is stored
   representationally, not procedurally.
5. **Honest negative**: on huge unstructured pages (Wikipedia, >400
   actionable elements) heuristic agents without an LLM fail regardless of
   memory (59–60 novel actions, no convergence). Operational memory does
   not substitute for semantic search ability; it compounds with it.

## Engineering bugs found & fixed during bring-up (recorded per §15)

- stale-state propagation between subgoals;
- element-index ≠ Playwright nth() mismatch → random wrong clicks (fixed
  via captured CSS paths);
- input values leaking into state fingerprints → infinite refill loops;
- case-sensitive goal predicates;
- non-interactive success markers invisible to predicates (added
  page_text observable);
- external links hijacking "root" prior (added internal/external flag).

Each bug corresponds to a class of failure an operational-memory layer
must represent (state identity, element identity, volatility, marker
visibility, boundary discipline).

## Threats to validity

- Single-run sequence, small corpus, sandbox-friendly sites; no site drift
  measured yet (staleness/half-life G8 remains open).
- Scripted heuristics ≠ LLM agents; absolute cost numbers will differ,
  reuse ratios should transfer.
- Subgoal predicates are mechanical; a real agent's success criterion is
  richer.

## Next questions (priority order)

1. G8/G9 staleness & confidence: mutate store entries (selector drift
   simulation by DOM perturbation) and measure confidence decay vs
   validation outcomes.
2. Scale composition: chains of ≥3 fragments incl. cross-site generic
   skills (login shape transfer quotes→the-internet).
3. LLM-in-the-loop replication of the same protocol to validate cost
   model against token costs.
4. Wikipedia-class pages: memory-augmented semantic retrieval (needs
   embedding or LLM ranker).
