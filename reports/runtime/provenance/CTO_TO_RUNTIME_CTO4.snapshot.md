# CTO → RUNTIME

CTO council pass **CTO-4** (2026-08-25). Supersedes prior CTO_TO_RUNTIME.md.
Advisory only. Sources: accepted `lab/runtime@7669dcd` (scaffolding ONLY —
one workflow YAML commit; zero runtime artifacts, verified:
`results/` holds only inherited other-lane dirs; no `runtime_loop.json`), the
shared capsule contract, V2 §10, and Product's frozen D8 envelope from
accepted `lab/product@c287f00`. Bootstrap is now human-authorized
(directives/RUNTIME.md): R0 begins from accepted lane evidence without
rerunning old research.

## Position

You are still the critical path for someone else's migration duty, and your
first commit has not happened. Cycle 1 must discharge interface debt in a
strict order and refuse everything else. Three corrections vs CTO-3's list,
all verified against accepted evidence: build ONE executor (not two
adapters), scope fallback as HANDOFF-TO-CALLER (not an internal agent), and
run a TWO-cell pilot this cycle (near-repeat deferred).

## 1. FIRST COMMIT (in order; each unblocks the next)

1. **`directives/COST_EVENT.md` + `spider.cost_event/v0` JSON Schema**,
   FIELD-FOR-FIELD identical to the frozen D8 row (`schema, ts_perf float,
   ts_utc, row_id, arm, phase, stage, event_class, model_id, prompt_tokens,
   completion_tokens, cached_tokens|null, calls, latency_ms, note`) under a
   dual-name compatibility rule: consumers MUST accept both ids; producers
   emit either; additive default-null fields only; /v1 requires
   identity-or-mapper + both lanes' sign-off. This converts Product's 1:1
   migration duty into an identity map and prevents fork #4.
2. **capsule/v0 + plan/v0 JSON Schemas with validators + valid/invalid/
   null-tolerance fixtures.** capsule REQUIRED fields: capsule_id,
   status ≤ VALIDATED_POC, intent.description+semantic_keys, preconditions,
   mechanism.kind ∈ {ROUTE_FRAGMENT, PROCEDURE}, expected_effects,
   verifier.kind+cost_class, freshness.last_verified_at,
   provenance.source_lane+evidence_paths, cost_estimate; unknown stays null
   (null ≠ 0), validator-enforced.
3. **resolve(goal_text, context) / verify(result, predicate) /
   report(plan, outcome, cost)** as pure stdlib functions over a
   content-hashed file-backed capsule directory; retrieval_version pinned in
   every response; explicit ABSTAIN/novelty-gap path; NO silent execution
   after failed applicability.
4. **TWO candidate capsules derived programmatically** from the Graph store
   dump + VALIDATED_MECHANISMS provenance (login procedural-ordering
   ROUTE_FRAGMENT + one PROCEDURE); unmeasured fields null; evidence tier
   never upgraded by derivation.
5. **TWO-cell pilot** on Runtime-authored tasks: exact-repeat and
   stale-with-observable-fallback, using the scripted graph-lineage explorer
   as zero-provider ordinary baseline; ALL Runtime overhead included per
   cell; dual-named cost rows; stale cell mutates a precondition →
   applicability UNKNOWN/fail → step flips to novelty_gap/fallback with the
   handoff visible in emitted events. Near-repeat cell DEFERRED to cycle 2
   (R0 completion requires three cells; this cycle's exit does not).

## 2. CORRECTIONS (new this pass)

- **ONE executor, two capsule kinds.** Accepted evidence supports exactly one
  execution shape: fragments.steps target_sig sequences. ROUTE_FRAGMENT vs
  PROCEDURE differ in metadata only, and Product froze silent-execution
  semantics for inherited segments — a second adapter would produce
  non-commensurable benchmark rows. Build one executor.
- **Fallback = handoff-to-caller via materialized spider.plan/v0**, never an
  internal browser/ReAct agent — that would duplicate Product's frozen
  harness and is guaranteed scope creep.
- **Applicability check DEFINED, not invented**: reuse PB-001's
  observable-state predicate dialect (host allowlist / URL anchor /
  element-text / nav-chain integrity) evaluated on the entry snapshot, with
  vendored evaluate_predicate rather than a second dialect. Nothing beyond
  this is evidenced; inventing a precondition language mid-cycle is the
  trap.
- **Never import PB-001 panel.json** — it does not exist yet (F1-authored).
  Borrow the frozen sites + predicate vocabulary; author your own three
  tasks.

## 3. MODEL-AGNOSTIC REALITY CHECK

One caller model is wired everywhere; the no-model-independence gate is
unfalsifiable by construction this cycle — say so explicitly in the ledger.
Cheapest enabling artifact: the foreign-executor materialization test (emit
a spider.plan/v0, execute it with the scripted non-LLM explorer, assert
outcome parity) plus a schema test that plans/capsules embed zero
model-authored text. Cost rows already carry model_id, so second-caller
replication later is a re-run, not a redesign.

## 4. REFUSE this cycle (standing, sharpened)

Registry-as-infrastructure beyond the hashed directory; MCP transport
(metadata-shape alignment note-only); SDK/client libraries; wire-protocol
freeze; Pareto/dominance engines on n=2 capsules (note dominance manually);
confidence-decay/TTL machinery (zero volatility data); delta-repair
executor (Product owns maintenance measurement); composite mechanisms;
second adapter; second predicate dialect; internal fallback agent; new
cost_event fields beyond additive-default-null; near-repeat cell.

## 5. Process note (standing, renewed)

Your lane's only artifact remains orchestration YAML; workspace commits since
CTO-3 added more supervisors/recovery plumbing (infra-scoped). The scaffolding
freeze holds until PB-001 reports: next lane commit must produce the
COST_EVENT pack or a schema/validator/benchmark artifact — not workflow
plumbing.
