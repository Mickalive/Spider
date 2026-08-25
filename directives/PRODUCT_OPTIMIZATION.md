# SPIDER — PRODUCT OPTIMIZATION CHARTER

Binding on every Product role: PRODUCT_DIRECTOR, BETA_ARCHITECT,
BETA_BUILDER, BETA_TESTER_AUDITOR and any subagents assisting them.

Precedence: `SPIDER_MASTER_PROMPT.md` > this charter > role directives >
accepted ledgers > historical reports.

## 1. Purpose

Product work does not package mechanisms; it optimizes them. Every retained
process (memory, retrieval, route reuse, browser-to-API escalation, caching,
fallback, staleness handling, self-healing, semantic addressing, capability
registries, execution planning) is managed as an explicit optimization
program against a credible baseline, not as a feature demo.

## 2. Program admission rule

A process enters an optimization program only when the Director records:

1. BOTTLENECK — the measured or explicitly expected inefficiency, with its
   source (audited finding, reproduction, or declared hypothesis);
2. BASELINE — the strongest credible comparator available, with exact
   version/date and status `LOCALLY_REPRODUCED` or `EXTERNAL_CLAIM_ONLY`;
3. METRICS — preregistered operational metrics and budgets;
4. WIN RULE — falsifiable success/failure conditions frozen before outcomes;
5. SCOPE CAP and KILL CONDITION.

Vendor claims are never baselines of record until locally reproduced.
Memory beating no-memory is never sufficient (constitution §13).

## 3. Freeze discipline

- Preregister hypothesis, arms, tasks, budgets, metrics, win rule, scope and
  analysis plan BEFORE observing confirmatory outcomes (§19).
- A win rule may never be weakened, reinterpreted or moved after outcomes.
- Any analysis change after seeing results is exploratory; it cannot feed a
  confirmatory claim.
- A new confirmatory comparison requires a new freeze on untouched evidence.
- Pre-outcome architecture revisions are permitted only when no outcome
  exists anywhere, and must be disclosed as a delta section naming the sole
  semantic change.

## 4. Versioning after results

- Each optimization iteration carries a version id; prior versions remain
  preserved provenance and are never rewritten into clean history.
- After a loss, a new version is authorized ONLY if the audit supplies a
  measured bottleneck and a concrete technical modification plausibly
  addresses it. "Try again" is not a hypothesis.
- Two consecutive MEASUREMENT_INVALID batches stop the program pending an
  infrastructure repair decision.
- A cleanly losing program is closed as valid bounded negative evidence and
  the hypothesis is downgraded or rejected per Director decision.

## 5. Fairness floors (non-negotiable in any comparative run)

- Identical backbone model, decoding policy, observation/action space and
  step/token budgets across all arms unless a difference IS the hypothesis.
- Acceptance/completion predicates disclosed identically to all arms
  (no arm enjoys a private oracle).
- Anchored, machine-checkable success predicates; fabricated success is an
  automatic failure event for the arm that produced it.
- Knowledge stores byte-restored before evaluation rows; evaluation writes
  nothing back.
- All treatment-arm overhead (retrieval, planning, summarization) counted
  inside treatment totals. No hidden subsidy.
- Latency at `perf_counter` granularity; tokens/model-calls from provider
  accounting; seeds deterministic where the harness permits; site-health
  gates per row.

## 6. Wording-constraint inheritance

Any binding wording constraint attached to an upstream audited block
travels verbatim into every product use of that block (example: Intel SGDR
PoC-tier constraints; Graph V31 spent-instrument rule). A product report
may not launder a constrained claim into an unconstrained one by
rephrasing across documents.

## 7. Reporting honesty

- Report all regimes, all arms and all losses, including descriptive
  failure-mode data.
- Negative results are valid outputs and feed disposition decisions.
- No metric gaming: optimizing the metric without the user-visible
  capability (e.g., solving the predicate instead of the task) is treated
  as a fabricated success.

## 8. Scope ceiling

Internal benchmarking only. No public deployment, no external users, no
commercialization, no external data sharing without explicit human
authorization. Anything beyond an authorized beta's maximum_scope requires
a new Director authorization.
