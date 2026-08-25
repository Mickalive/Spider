# SPIDER PRODUCT ARCHITECTURE HYPOTHESES

Conceptual combinations of AUDITED technical building blocks.

Statuses: WATCH / PROMISING / PRODUCT_CANDIDATE / REJECTED.
PRODUCT_CANDIDATE authorizes at most an internal benchmarkable beta; it
never authorizes public deployment or commercialization.

Last updated: 2026-08-25 (session on mounted snapshots: Graph through
Run 32783797303 audit PASS; Physics through WP-005 audit PASS; Intel
ledger empty).

---

## PH-1 — Inherited operational memory layer for repeat/near-repeat web tasks — **PRODUCT_CANDIDATE (Beta PB-001 authorized)**

- **User problem**: Browser agents re-pay full exploration cost (actions,
  model calls, tokens, latency, flaky retries) every run, even when the
  task is a repeat or near-repeat of something some agent already solved
  (same login flow, same pagination drill, same form path with shifted
  parameters or reworded goal).
- **Validated building blocks (source)**: cumulative store with
  provenance/confidence + exact replay + entry-state reset (G-H1);
  blind content-addressed fragment retrieval with expected-UNKNOWN
  discipline (G-H2); oracle-equalized iterative replay policy (G-H2/G-H3
  E2); multi-step login procedure packaging as first-class reusable unit
  (G-H3 E2, G-H4 R3); V31 closed-class descriptor/query equipment
  (G-H4) used AS EQUIPMENT ONLY.
- **Unvalidated assumptions**: inheritance survives a real LLM consumer
  (all accepted results are scripted deterministic consumers); free-form
  natural-language goals work end-to-end without hand-authored goal
  signatures; savings are material in tokens/model-calls/wall-clock;
  known failure modes (category goals, deep >3-fragment chains,
  cross-site) stay contained inside the declared scope.
- **Expected operational benefit**: on repeat/near-repeat tasks, large
  reductions in browser actions, model calls/tokens and latency at
  non-inferior success; reused-action share dominating the action mix.
- **Nearest competitors**: plain current browser agents (no memory);
  trajectory/workflow-memory systems (AWM-class retrieval augmentation);
  selector caches (Stagehand-class); workflow RPA replay (Skyvern-class).
- **Differentiation (bounded hypothesis, not a novelty claim)**:
  subgoal-addressable EXECUTABLE fragments with empirical validation
  statistics, provenance and freshness metadata consumed by an external
  model-agnostic layer — the combination was not identified among the
  systems inspected in Run 1.
- **Conceptual architecture**: producer runs grow a validated store →
  content-addressed retrieval (V31 canonicalization) selects fragments/
  procedures for subgoals of the free-form goal → consumer LLM executes
  memory-led with exploration fallback and explicit UNKNOWN reporting →
  anchored completion predicate equalized across arms → outcomes written
  back with provenance (calibration deferred).
- **Biggest uncertainty**: whether the scripted-setup advantage survives
  contact with an actual LLM in the loop without inflating errors
  (memory-induced wrong actions, stale-fragment traps).
- **Evidence needed**: Beta PB-001 outcome vs B0 cold-agent and B1
  trajectory-RAG baselines under preregistered win rule.
- **Status**: PRODUCT_CANDIDATE. Beta request: `state/product_beta_request.json` (PB-001).

## PH-2 — Shared capability infrastructure line (Steam-like) — **WATCH**

- **User problem**: many agents/teams independently re-explore the same
  sites; a registry through which agents discover, inherit, verify,
  version and possibly share reusable Web capabilities could amortize
  exploration across teams/models.
- **Mechanisms to evaluate as product mechanisms (NOT assumptions)**:
  discovery, semantic addressing, provenance, trust, scoring,
  freshness/decay, versioning, incentives, cross-model compatibility,
  permissions/auth, route invalidation.
- **Why WATCH**: Intel ledger is EMPTY (no reproduced+audited external
  mechanism); internal confidence/staleness are UNCALIBRATED (G8/G9
  open); cross-model consumption untested (G10 open). Nothing here may
  enter PB-001.
- **Path to PROMISING**: first audited Intel mechanism reproducing in a
  SPIDER-relevant test; G8/G9 calibration evidence; any cross-model
  consumption result.
- **Status**: WATCH.

## PH-3 — Predictive Web-dynamics routing ("physics-powered" navigation) — **REJECTED**

- **Claim that would be needed**: transferable action-conditioned
  environment regularity usable to predict/route transformations across
  sites beyond memory and similarity.
- **Evidence against (audited)**: Physics WP-003B-R2 FALSIFIED (mean D
  −0.5016, 0/5 adequate folds, site holdout) and WP-005 FALSIFIED at fine
  granularity (T1 wins 1/9 p=0.898; T2 wins 4/9 p=0.270); apparent
  predictability = persistence + site-local NN retrieval + generic
  action-type semantics. WP-004 committor work BLOCKED pending
  identifiability.
- **Disposition**: no product work builds on predictive dynamics. A
  genuinely new instrument (deliberate restart/matched-state designs,
  Physics WP-006 direction) producing a positive would be required to
  reopen this narrowly.
- **Status**: REJECTED.

## PH-4 — Selector self-healing / staleness product — **WATCH**

- **User problem**: agents break when site structure drifts; selectors
  need repair/revalidation (Healenium-adjacent space).
- **SPIDER angle**: store-level failure events + provenance + freshness
  could drive revalidation and localized re-exploration instead of
  silent failure (entry-reset mechanism is adjacent, audited as recovery
  POC only).
- **Why WATCH**: staleness/confidence UNCALIBRATED; no audited experiment
  demonstrates repair value over retry/TTL heuristics; competitor space
  established (Healenium). Needs an audited staleness-calibration or
  recovery-value result before any candidate status.
- **Status**: WATCH.

---

## Combination rules observed

- Only audited blocks combine into candidates (currently: PH-1 only).
- Physics negatives forbid any PH-1 marketing/feature language implying
  prediction or cross-site generalization.
- Intel emptiness forbids any sharing/marketplace surface in products.
- Any quantitative addressing claim inside a product report requires a
  third independently authored instrument (G-H4 spent-instrument rule).
