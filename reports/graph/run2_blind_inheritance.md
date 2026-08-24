# TEAM GRAPH — Cycle 32670239235: Blind Inheritance on Held-Out Composites

Date: 2026-08-24 (live-site runs 2026-08-23T23:5x – 2026-08-24T02:05 UTC)
Branch: `spider/graph-cycle-32670239235` · infra commit `5817fa8` (+ results commit)
Policies: scripted heuristics only, no LLM in the loop.

## AUDIT STATUS (independent audit + LAB DIRECTOR integration)

Independent audit verdicts (`reports/audit/CYCLE_32670239235.md`): engineering
claims VALIDATED; scientific claim **SURVIVES_AUDIT_WITH_LIMITS**.

| Claim | Status |
|---|---|
| Blind fragment composition succeeds on held-out composites whose full routes were never trained, with the consumer receiving **no hand-selected fragment IDs** | **PROOF OF CONCEPT** — cleanest evidence is `C_internet_login_checkboxes` (fully independent production-acquired provenance). On `C_quotes_login_love_p2` the third subgoal retrieved a fragment created earlier **within the same composite run** (audit F-G2), so that composite only partially satisfies the master §11 independence requirement. Previously worded "REPLICATED (2/2)" is qualified accordingly. |
| Content-derived addressing retrieves producer fragments from consumer-side task keywords without goal_sig lookup | SURVIVES_CURRENT_TEST (87.5% route-found, UNKNOWN honest, deterministic 16/16 across variants) |
| Fragment memory beats matched cold / nearest-trajectory / graph-BFS baselines on novel actions | SURVIVES_CURRENT_TEST for cold & graph (paired CIs excl. 0); vs trajectory: −43.6 [−74.0, −13.2] in run2c but success-rate parity — NEEDS_REPLICATION |
| Exact replay of known routes = zero novel actions | REPLICATED ×3 variants (5/5 tasks each) |
| Confidence scores are calibrated | **DATA_INSUFFICIENT** (all 40 prospective rounds in one score bucket) |

Director corrections applied at integration:
- (F-G1) The composite-outcomes table below originally presented stale
  run2b cells for the checkbox composite and a stale trajectory action count
  for the quotes composite. It was regenerated programmatically from
  `results/graph/run2c_cycle32670239235_20260824_020509.json`; the stale
  ledger figure ("cold 275") was likewise corrected to 191.
- (F-G3) Instrumentation disclosure added: snapshot `settle_ms` changed
  350→120 vs the cycle base (shared/browser.py). All within-cycle method
  comparisons share the instrument; wall_s is NOT comparable to run-1 numbers.
- (F-G2) Quotes-composite caveat annotated in the table and claim table.

## Design

Five held-out composite targets recombine parts learned only inside
independent production tasks (category navigation, pagination, product
opening, logins, hub navigation, status-code navigation). Full target routes
appear nowhere in training. Four methods share ONE consumer shell
(`graph/consumer.py`) and differ ONLY in the memory representation consulted;
each method runs on a physical copy of the identical post-production store;
cold gets an empty store with reads disabled. Per-target method order is
seed-randomized (`SEED=20260823`). Subgoal `sig` strings are provenance
labels only — retrieval never sees them (`graph/addressing.py`).

Preregistered endpoints (frozen before run2): mean novel actions per
composite per method; success rate; addressing UNKNOWN rate; retrieval
overhead. Exploratory: calibration reliability.

UNKNOWN discipline: below-gate retrievals return UNKNOWN and the consumer
explores; UNKNOWN is never filled from ground truth (unit-tested:
`tests/test_graph_cycle2.py::test_unknown_stays_unknown`,
`test_boilerplate_token_alone_does_not_retrieve`).

## Variant history (all artifacts preserved as provenance)

Live smoke checks between design-freeze and recording exposed measurement
defects; each fix is disclosed and tied to a defect observed against the
prior variant's own artifact:

- `run2` (results/graph/run2_cycle32670239235_20260823_235851.json):
  substring acceptance matched wrong pages ('science-fiction' satisfied
  'fiction'; global `/catalogue/page-2.html` satisfied 'page-2'); acquired
  fragments contained exploratory detour steps.
- `run2b` (…run2b_cycle32670239235_20260824_005039.json): + keyword-scale fix,
  product-page guard. Fantasy arm still invalid (same substring defects).
- `run2c` (**primary**, …run2c_cycle32670239235_20260824_020509.json):
  + structural URL-path evaluators (C4), href weighted below visible text
  (C3), route distillation at acquisition (C5), deterministic hub-recovery
  with churn detection available equally to ALL conditions (C6).
  Addressing gates/weights, budgets, corpus routes, methods and endpoints
  unchanged across variants.

## Results (run2c primary; replication column = same task under prior variants)

### Composite outcomes by method (total actions = novel+reused | status)

Regenerated programmatically from the run2c primary artifact (director
correction for audit finding F-G1; original table contained stale run2b cells).

| Composite | cold | trajectory | graph | fragment(SPIDER) | replicated? |
|---|---|---|---|---|---|
| login→checkboxes | 191 partial (2/3) | 78 SUCCESS (3/3) | 89 SUCCESS (3/3) | **7 SUCCESS** (3/3, reuse 5) | ✓ fragment success in run2b too; **note: in run2c trajectory & graph also succeed on this composite — fragment is cheapest by far but not uniquely successful** |
| login→tag-love→p2 | 28 SUCCESS (3/3) | 57 SUCCESS (3/3) | 29 SUCCESS (3/3) | **9 SUCCESS** (3/3, reuse 7) | ⚠ F-G2: third subgoal reused a fragment born earlier in the same composite run → partial self-inheritance; independence holds only for the first two subgoals |
| login→status-500 | 310 partial (0/3) | 113 partial (2/3) | 198 partial (1/3) | 103 partial (2/3, reuse 6) | success in run2/run2b (17–19 act) — sensitive to recovery mechanism (C6), see limits |
| login→dyn-ex2 | 310 partial (0/4) | 227 partial (1/4) | 221 partial (2/4) | 125 partial (2/4, reuse 6) | no variant fully solves ex2 (numeric blindness, below) |
| fantasy→p2→product | 271 partial (0/3) | 281 partial (0/3) | 277 partial (0/3) | 278 partial (0/3) | unsolved by EVERY method under policy B in all variants (run2/run2b 2/3 rows were predicate artifacts) |

### Aggregates over the 5 composites (run2c)

| method | novel/task | reused/task | success | wall s |
|---|---|---|---|---|
| cold | 222.0 | 0.0 | 0.2 | 188.6 |
| trajectory | 142.4 | 8.8 | 0.4 | 154.3 |
| graph-BFS | 160.2 | 2.6 | 0.4 | 166.2 |
| fragment | **98.8** | 5.6 | 0.4 | **119.5** |

Paired deltas (task-grouped bootstrap, B=10k, seed 20260823):
fragment−cold −123.2 [−199.4, −41.6]; fragment−graph −61.4 [−96.2, −24.2];
fragment−trajectory −43.6 [−74.0, −13.2] (success-rate deltas 0.2 [0,0.6],
0.0, 0.0).

### Addressing quality (fragment method, run2c)

16 subgoal lookups: 14 routes found (87.5%), 2 honest UNKNOWN (12.5%),
mean retrieval 0.41 ms/lookup. Top-choice agreement between run2b and run2c
stores: 16/16 despite differing production stores → content-driven, not
label-driven. Examples: query kws `["login"]` → `int.login` (score 1.0);
`["next","page"]` → clean `[click next]` pager cross-category (fantasy);
untrained "500" step correctly NOT satisfied by trained "200" fragment —
novelty localized to one click after a cheap misfire+recovery (by design).

### Replay validation & cost-vs-knowledge ledger

Replay of stored production tasks by the inheriting policy: 5/5 tasks,
zero novel actions (also 5/5 in run2 and run2b). Ordered ledger contains 35
sequential executions across three generations (produce → blind-inherit →
replay-validate) with store growth 21→32 fragments, satisfying the ≥20
sequential-agents directive; per-execution rows in
`results/graph/run2c_analysis.json` (`stream`).

### Prospective calibration (exploratory)

40 revalidation rounds over 20 frozen-confidence fragments: all confidences
fell in [0.5, 0.75]; empirical success 0.95. Single-bucket spread ⇒ no
calibration mapping estimable this cycle (DATA_INSUFFICIENT). Scores must
continue to be treated as uncalibrated engineering gates.

## Negative results and limits (load-bearing)

1. **Inheritance cannot compensate unreachable novelty**: the fantasy
   composite was failed by ALL four methods under the DOM-order consumer
   policy within matched budgets — deep menu scan costs exceed budget before
   the novelty region is reached. Memory value is conditional on the
   consumer being able to reach the frontier at all.
2. **Numeric specificity is invisible to the content channel**: single-digit
   tokens are stripped ("Example 1" vs "Example 2" indistinguishable), so the
   ex2 start subgoal retrieved the ex1 fragment (score 1.0). Fix candidate
   (keep digits) recorded but deliberately NOT applied post-outcome.
3. **Recovery-mechanism sensitivity**: replacing history-back with
   deterministic hub-return (C6) flipped status-500 from success to partial
   while making fragments cleaner — inheritance outcomes depend on glue
   recovery policy, not just stored routes.
4. **Confidence compression**: see calibration above.
5. Evaluator lesson for future cycles: hand-authored acceptance predicates
   are part of the measurement instrument; substring matching produced two
   partially-invalid recorded variants (preserved as provenance).

## What this cycle does NOT establish

no LLM-in-loop cost savings; no natural-language task decomposition;
no cross-model transfer (single scripted consumer policy); small n=5
composites; hand-authored acceptance predicates (evaluation instrument,
disclosed) and per-subgoal keywords (NL-description stand-ins) remain;
no cross-site skill transfer claims.

## Evidence pointers

- Primary raw: `results/graph/run2c_cycle32670239235_20260824_020509.json`
  (config incl. seeds/thresholds/commit, per-run metric dicts, retrieval
  diagnostics, ledger, calibration rows).
- Provenance: `run2_*`, `run2b_*` JSONs + their `*_analysis.json`.
- Analysis code: `graph/analyze_cycle2.py`; driver: `graph/run_cycle2.py`;
  addressing: `graph/addressing.py`; baselines: `graph/baselines.py`;
  consumer: `graph/consumer.py`; tests: `tests/test_graph_cycle2.py`.
