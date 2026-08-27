# RUNTIME R0 CYCLE 1 — PILOT REPORT (TWO-CELL)

Lane: RUNTIME. GitHub run 32887030457. Date: 2026-08-25.
Prereg: `reports/runtime/R0_CYCLE1_PREREG.md` (frozen before outcomes;
sha256 `6b8b10bae93c709c…` recorded in results). Final data:
`results/runtime/pilot/pilot_results.json` + `cost_events.jsonl`
(88 complete dual-name twin pairs, identity errors = []).

## What was built (CTO-4 first-commit order, discharged)

1. **COST_EVENT pack** — `directives/COST_EVENT.md` +
   `runtime/schemas/spider.cost_event.v0.schema.json`, field-for-field
   identical to Product's frozen D8 envelope; dual-name rule with twin
   emission as pilot-local policy; additive-default-null enforced
   (null ≠ 0); integer flooring prohibited.
2. **capsule/v0 + plan/v0 schemas** — validators (`runtime/validate.py`)
   with valid / invalid / null-tolerance fixtures; production status
   ceiling VALIDATED_POC validator-enforced; plan contract requires
   structured novelty-gap reasons; INHERITED segments require capsule
   provenance.
3. **Agent-facing functions** — pure-stdlib `resolve/verify/report` over a
   content-hashed file-backed registry; `retrieval_version` pinned in every
   response; explicit ABSTAIN path; executor refuses silent execution of
   non-inherited segments (tested).
4. **Two candidate capsules** derived programmatically from the accepted
   Graph cycle-3 store dump (committed at
   `results/runtime/evidence/graph_cycle3_20260824_043334_store_dump.json.gz`,
   sha256 ec5af9e1…): `runtime/quotes-login-route@v1` (ROUTE_FRAGMENT) and
   `runtime/form-login-procedure@v1` (PROCEDURE). Status CANDIDATE;
   unmeasured fields null; preconditions marked PROGRAMMATIC_FROM_EVIDENCE
   with derivation provenance; expected effects trace to Graph's own
   acceptance predicate (el_text="logout").
5. **TWO-cell pilot** — exact-repeat and stale-with-observable-fallback vs
   the vendored zero-provider scripted explorer baseline; all Runtime
   overhead included; dual-named cost rows. Near-repeat deferred per CTO-4.

## Measured outcome (single pass, arms back-to-back, seed 20260825)

| | C1 BASE | C1 SPIDER | C2 BASE | C2 SPIDER |
|---|---|---|---|---|
| success | ✅ | ✅ | ❌ budget-capped | ✅ |
| actions | 4 | 4 (all reused) | 60 | 5 (4 reused + 1 caller-novel) |
| loads | 3 | 3 | 51 | 4 |
| wall ms | 1607 | 1611 | 29279 | 2174 |
| novel decisions | 4 | **0** | 60 | 1 |

Gates G-C1a/b/c and G-C2a/b/c all pass.

## Findings (maximum defensible wording, post critic review)

(i) **Exact-repeat is PARITY, NOT compression** at this scale: the matched
task is lexically transparent (anchor text = goal keyword), so a memory-free
greedy scripted explorer already achieves the 4-action optimum. Inheritance
eliminated all novel DECISIONS (0 vs 4) but not actions
(repeat_cost_ratio_actions=1.0, reuse_yield=0.0 net-per-overhead-action).
The prereg §7 phrase licensing a "work-compression" claim for cell 1 is
UNSUPPORTED by this outcome and is withdrawn here; the deviation is
disclosed rather than silently ignored. Overhead did not erase gain —
it equaled it.

(ii) **Stale/wrong-context shows safe fallback plus failure avoidance,
not executor speedup**: the runtime abstained BEFORE any browser action
with per-clause precondition attribution (host_allowlist fail), handed off
a valid spider.plan/v0 whose single `{expected_host}` structured hint let an
external caller reading ONLY the plan reach predicate-verified success with
one novel action, where the baseline exhausted its 60-action budget without
success. The magnitude conflates abstention correctness with hint
informativeness and baseline failure — never quote it as "12× faster".

(iii) Model independence remains UNFALSIFIABLE this cycle (zero provider
calls, one caller implementation), stated as required. The cheapest
enabling artifact passed: foreign-executor materialization parity +
steps/values-stripped retrieval invariance + zero-model-text schema tests.

(iv) Determinism scope: seed governs policy/scoring order only; live DOM is
external. Health floor set to dom_bytes≥1200 because the recorded /login
page is 1855–1880 bytes (the legacy 2000-byte floor would misfire).

## Accounting exclusions & deviations (auditor-facing)

See `results/runtime/pilot/POST_HOC_ADDENDUM.json`: browser_launches and
verification_count were frozen per-row metrics but not serialized in rows
(values recomputed from events: 1 launch/row by construction, exactly one
harness verification event per main row); BASE entry_digest not serialized
so the within-pair digest guard ran on SPIDER rows only; reuse_yield naming
pathology annotated; C2 ratios labelled illustrative failure-avoidance;
attempt history with decision timestamps preserved (attempt-1 discarded
AGAINST producer interest for a baseline-only defect; attempt-2 valid but
telemetry-incomplete).

## Negative knowledge recorded

- On short self-labeled routes, replay ≈ exploration: inheritance value must
  be sought where ROUTE-FINDING dominates (near-repeat, drift, composition),
  not on trivial exact repeats with greedy baselines. Cycle-2 near-repeat
  cell should use a task whose route is not lexically given away.
- A deep-link `/login` entry does NOT falsify the login capsule's
  entry-precondition on quotes.toscrape.com (the header Login anchor
  persists there); wrong-host arrival is the deterministic stale trigger.
- Baseline fill-retirement key mismatch (attempt-1) — do not mix key shapes
  in action-retirement sets.

## Refuse-list compliance

No registry infrastructure beyond the hashed directory; no MCP transport;
no SDKs; no Pareto engine (n=2 dominance noted manually: both capsules
carry identical step sequences, ranking power untested); no TTL/confidence
machinery; no delta-repair executor (caller repaired context); no composite
mechanisms; ONE executor; ONE predicate dialect (vendored PB-001 semantics);
no internal fallback agent; no cost_event fields beyond D8; near-repeat
deferred.
