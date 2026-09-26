# EXP-FRONTIER-36129180789 Report — Residual Novelty vs No-Memory Deterministic Executor

**Lane:** frontier — C-RESIDUAL-NOVELTY (pay-novelty-not-length)
**Status:** MEASUREMENT_INVALID
**Outcome:** NOT_APPLICABLE
**Freeze:** 2026-09-25T11:32:07.696373+00:00

## Executive Summary

This experiment tests SPIDER's **central premise** against the **strongest available null**: a no-memory deterministic executor compiled from the current observation alone.

**Director Mandate (binding):**
> "The decisive question SPIDER has never asked is whether inheritance is needed at all. Every prior design compared inheritance against cold, instructions and retrieval, but never against a deterministic executor that has no memory and derives its plan from the current observation... If that no-memory executor matches inherited execution at matched correctness and equal cost, then C-RESIDUAL-NOVELTY, C-PRODUCT-ECON and the compilation priors are jointly moot and the architecture must change. That is a null against SPIDER's own premise, which is the highest-upside falsification available and exactly Frontier's charter. It is also reachable: it needs a real service and two executors, not a public-Web corpus and not a policy model."

**Result: MEASUREMENT_INVALID (validity gate, not scientific falsification)**

All required live substrates are unavailable:
- Real HTTP service (Flask/FastAPI) — Python packages not installed
- Runtime capability ledger — `/tmp/spider-runtime/capability_ledger.json` not found; distributed-substrate bring-up contract not certified
- Graph C-FRESHNESS gate — `research/graph/state.json` not found; TN>=0.85 with >=30 stale probes not validated

Per frozen `spec.json` measurement_validity[0] and `prereg.md` section 4/10: **If ANY substrate is unavailable → live_available = false → MEASUREMENT_INVALID diagnostic. STOP. Do not substitute synthetic fixtures, jittered counters, or n×3200/f×6.0 proxies. Record finding and halt.**

## Substrate Diagnostic

| Substrate | Required | Available | Details |
|-----------|----------|-----------|---------|
| Real HTTP Service | Flask or FastAPI for local test server | **NO** | Neither Flask nor FastAPI installed |
| Runtime Capability Ledger | Certifies distributed-substrate bring-up contract | **NO** | `/tmp/spider-runtime/capability_ledger.json` not found |
| Graph C-FRESHNESS Gate | TN >= 0.85, >=30 stale probes | **NO** | `research/graph/state.json` not found |

**Overall:** `live_available=false`

## Controls Status

All positive controls (PC) and null controls (NC) requiring live execution are **NOT_RUN**:

| Control | Status | Reason |
|---------|--------|--------|
| PC-EXACT-MATCH | FAIL (NOT_RUN) | Requires live paired executors with identical derived_context |
| NC-INHERITANCE-ABLATION | FAIL (NOT_RUN) | Requires live execution with empty registry |
| NC-ORACLE-LEAK | FAIL (NOT_RUN) | Requires live harness inspection |
| NC-BIJECTIVE-COST | FAIL (NOT_RUN) | Requires live honest cost measurements |
| NC-SHUFFLED-NULL | FAIL (NOT_RUN) | Requires live execution + 5000 permutations |
| NC-GUARD-SPECIFICITY | FAIL (NOT_RUN) | Requires live guard ablation |

**Per frozen decision rule: MEASUREMENT_INVALID if live_available=false OR any PC/NC fails.** This is a validity gate, not a scientific negative result.

## Scientific Context (from Director Mandate)

- **Prior synthetic falsification:** EXP-FRONTIER-36042599040 validly FALSIFIED synthetic alias economics on 36-family TAU0.30 Jaccard 0.0 gate (rho=0.4837 CI[0.410,0.552] <0.60, ECE=0.216>0.15, RAG dominance false) with all 11 PCs/NCs PASS
- **Alias ceiling bounded:** 17-deep retrieval-diversity tunnel at 21/40=0.525 pooled Wilson [0.352,0.648] with 0/10 mixed routing gain 0.0 (EXP-FRONTIER-36052053591 lineage)
- **4 deterministic compilation bypasses:** All MEASUREMENT_INVALID bounded at same 0.525 ceiling with 0/10 mixed
- **Director PIVOT with cognitive_reset=true:** SUPERSEDE parent. Test the no-memory deterministic executor as the strongest null against SPIDER's own premise.
- **Comparative reasoning:** This is the decisive experiment SPIDER has never run. If the no-memory executor matches inherited execution, the architecture must change.

## Validity Threats & Representation Loss

1. **No live evidence:** This experiment provides zero evidence for or against C-RESIDUAL-NOVELTY against the no-memory executor. The prior synthetic FALSIFIED-IN-SETTING (rho 0.4837) is bounded to TAU0.30 disjoint Jaccard 0.0, not live heterogeneous tasks.

2. **Substrate dependencies are hard gates:** The Director mandate explicitly lists Runtime capability ledger and Graph freshness as dependencies. None are satisfied.

3. **Synthetic substitution forbidden:** Per frozen spec BINDING-RULE and prereg, synthetic fixtures must NOT be substituted.

4. **Agent priors are not SPIDER evidence:** Director mandate agent priors (Agentic Compilation DSM $0.002-0.092, Agent JIT 10.4x, hierarchical decomposition, path dependence) are labeled priors distinguished in validity_notes/do_not_assume; they cannot satisfy S1-S6.

5. **Token dimension correctly handled:** No policy-model credential available → token cost NOT_APPLICABLE → reported UNKNOWN, never surrogate-filled.

## Unresolved Questions (Carried Forward)

All primary survival criteria S1-S6 remain unevaluated:
- S1: rho_novelty >=0.60 lower>0.40 p<0.05 (TAU+freshness-gated)
- S2: pooled |rho_length|<0.20 upper<0.25 p>=0.05 (decoupling)
- S3: per-stratum |rho_length|<0.20 upper<0.30 for all 5 novelty strata + length tertiles
- S4: calibration UNKNOWN precision>=0.85 false_accept<=0.10 ECE<=0.15 upper<=0.18
- S5: Pareto saving>=25% vs cold, strict dominance vs RAG k5 at f10/f100, external DSM/JIT reference
- S6: honest gap >0.35, |rho_proxy|<0.60, |rho_shuffled|<0.20 centered

Infrastructure unblockers needed:
- Runtime capability ledger deployment with distributed-substrate bring-up certification
- Graph C-FRESHNESS gate validation with TN>=0.85 and >=30 stale probes
- Local HTTP test server (Flask/FastAPI) deployment

## Artifacts

- `artifacts/substrate_diagnostic.json` — Complete substrate availability diagnostic with SHA256

## Next Steps

Per frozen decision rule and Director mandate: **This experiment records MEASUREMENT_INVALID and stops.** Do not substitute synthetic fixtures. The experiment can only proceed when ALL three hard gates are satisfied:
1. Local HTTP service (Flask/FastAPI) available
2. Runtime capability ledger certifying distributed-substrate bring-up
3. Graph C-FRESHNESS gate TN>=0.85 with >=30 stale probes

Upon substrate PASS, execute the paired within-task design with three arms (Inherited, NoMemory, Ablation) on matched task families with controlled novelty fractions, using honest per-trajectory hard-reset integer counters and the frozen decision rule (S1-S6 + FALSIFIED_IN_SETTING_TRIGGER).
