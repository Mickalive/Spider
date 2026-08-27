# R0 CYCLE 1 — TWO-CELL PILOT PREREGISTRATION (FROZEN BEFORE OUTCOMES)

Lane: RUNTIME. Cycle: R0-1 (GitHub run 32887030457). Date frozen: 2026-08-25.
Status: FROZEN. This file was written before any live pilot outcome row
existed; the pilot driver records `prereg_sha256` inside its results file,
captured at run start. Any analysis change after seeing outcomes would be
exploratory and must be labeled as such.

## 1. Question

Does the minimal SPIDER Runtime loop compress work on a matched exact-repeat
task, and does it fail SAFELY (observable abstain + handoff, no silent
execution) when the inherited capsule's precondition does not hold?

This cycle does NOT claim near-repeat transfer, composition, cross-model
inheritance or calibrated confidence. One caller implementation exists
(scripted, zero provider calls); the model-independence gate is therefore
UNFALSIFIABLE this cycle and is stated as such in the ledger. The cheapest
enabling artifact (foreign-executor materialization parity test) IS run.

## 2. Fixed inputs

- Capsules: exactly two, derived programmatically from the accepted Graph
  cycle-3 post-training store dump
  (`results/runtime/evidence/graph_cycle3_20260824_043334_store_dump.json.gz`,
  sha256 ec5af9e146ea629fac642ec4a7b14c49b685e5c193cff345a92191b7e05e7073;
  lineage lab/graph, audit-gated). Selection rule: fragments with >=1 fill
  AND >=1 click step; route lineage = site-prefixed goal_sig, generic
  lineage = `generic.`-prefixed goal_sig (producer-side only). Status stays
  CANDIDATE; unmeasured fields null.
- Retrieval: vendored goalsig desc_only scoring over `intent.semantic_keys`
  ONLY, tau=0.30 / min_match=2 / topk=3, UNTUNED constants (declared;
  ranking power untested at n=2). Tie-break: coverage -> site-scoped ->
  lexical capsule_id. retrieval_version pinned in every response.
- Sites: quotes.toscrape.com, books.toscrape.com (frozen sandbox sites,
  borrowed from accepted lanes). Live DOM drift between capsule recording
  (2026-08-24) and run date is a disclosed threat; preflight probes guard it.

## 3. Tasks (Runtime-authored; PB-001 panel.json NOT imported)

Shared success predicate id `rt.tasks:quotes_login_success@v1`
(host_allowlist=[quotes.toscrape.com], elem_text_any=["logout"]):
traces to Graph's own acceptance for this task family (`el_text="logout"`).

- T1 (exact-repeat): start https://quotes.toscrape.com/ ; goal_text
  "log in to quotes toscrape with the username spiderbot and password
  notasecret" ; fills = the two public demo credentials (same values as the
  recorded evidence; symmetry machine-checked at runtime:
  capsule step values == task parameter values).
- T2 (stale/wrong-context): SAME goal_text and predicate; entry context
  MUTATED to https://books.toscrape.com/ (wrong-host arrival — a natural
  deep-entry failure mode; the capsule's recorded host precondition no
  longer holds). The capsule artifact is NOT edited.

## 4. Arms

- BASE ("b0" in cost rows): vendored zero-provider scripted explorer
  (runtime/baseline.py; graph-lineage agent-G adaptation, memory removed).
- SPIDER ("spider"): resolve -> applicability -> executor replay OR handoff;
  in T2 the harness plays the CALLER: after receiving the materialized
  handoff plan it may act on its structured hint, then re-resolves.

## 5. Cells, order, rerun policy

Cell C1 = T1 both arms; Cell C2 = T2 both arms. Arms run back-to-back per
cell (BASE first, then SPIDER), fresh browser context per row. Preflight
smoke probes (phase=smoke) must confirm BEFORE the batch: login anchor on
quotes home; username/password inputs on quotes /login; books home reachable.
Deterministic HEALTH_TRIP classes eligible for max ONE rerun per cell
(original preserved, `rerun_of` recorded): unhealthy entry page
(dom_bytes<1200 OR elements<5), entry DOM digest mismatch WITHIN a cell pair,
navigation transport error. Everything else is recorded as-is, no reruns.

## 6. Metrics (frozen definitions)

Per row (both arms): predicate-judged success; browser actions
(click/fill/select/check/press/submit_enter executed); loads (navigations);
novel vs reused actions; llm_calls (=0); prompt/completion tokens (=0);
cached_tokens=null; retrieval latency (perf_counter float ms, native units);
verification count; wall_ms_perf float; browser launches (=1 per row by
construction; asserted equal across arms).

Derived (cell level):
- repeat_cost_ratio_actions = spider_total_actions / base_total_actions
- overhead_loads_ratio = spider_loads / base_loads
- novelty_fraction = novel_actions / total_actions (per arm)
- reuse_yield = (base_actions - spider_comparable_actions) /
    max(1, overhead_actions) where overhead_actions counts ONLY action-class
    recovery/retry work performed BY the runtime (expected 0 this cycle).
NO ms->action conversion anywhere: latencies stay native floats.

Cell C2 additionally records: abstain event (zero runtime browser actions
before handoff), per-clause applicability attribution, caller-side novel
goto counted as novel_action under SPIDER arm, final verified outcome.

## 7. Gates (frozen before outcomes)

- G-C1a: both arms succeed on T1 (predicate-judged).
- G-C1b: SPIDER total_actions <= BASE total_actions AND SPIDER
  reused_actions >= 4 AND SPIDER novel_actions == 0.
- G-C1c: every SPIDER action preceded by an applicability-pass event
  (no silent execution; auditable trail).
- G-C2a: applicability returns FAIL with per-clause attribution; ZERO
  runtime browser actions precede the handoff event.
- G-C2b: handoff plan validates against spider.plan/v0; caller continuation
  reaches verified success.
- G-C2c: BASE outcome on T2 reported truthfully whatever it is.
Cycle verdict wording ceiling: "work-compression on the matched exact-repeat
task at single-pass pilot scale" + "safe observable fallback under mutated
context". Replication, near-repeat and composition are explicitly deferred
to cycle 2. If G-C1b fails, that is reported as a VALID NEGATIVE (overhead
erases inheritance gain at this scale) — scope will not be widened to flip it.

## 8. Determinism scope

Seed 20260825 governs policy/scoring ORDER only; live-server and DOM
behavior are external and probed, not controlled. Temperature/model concepts
do not apply (zero provider calls anywhere in either arm).
