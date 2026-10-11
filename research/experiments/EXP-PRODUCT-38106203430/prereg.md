# Preregistration: EXP-PRODUCT-38106203430

## 1. Experiment identity
- experiment_id: EXP-PRODUCT-38106203430
- lane: product
- design_contract_version: 2
- request: research/experiments/EXP-PRODUCT-38106203430/request.json (immutable)
- parent_handoff: EXP-PRODUCT-37989728440/handoff.json (continuity evidence only; SUPERSEDE disposition per director_mandate)
- director_mandate: PIVOT on C-RESIDUAL-NOVELTY targeting asymmetric-discovery substrate/blocker removal

## 2. Scientific question and scope
This is a DESIGN-ONLY readiness experiment. Do not run outcome-bearing measurements.

Question (as refined from director_mandate): Can a credential-free substrate engineered for asymmetric discovery (one-time session/resource/schema discovery amortized or cached across tasks) produce genuine behavioral variance (COLD success_rate meaningfully below the 1.0 ceiling) such that a four-arm comparison has non-degenerate dynamic range under counter-only metrics, without rerunning the mandatory-discovery symmetric deterministic REST certificate?

The inherited parent handoff’s `carry_forward.established/rejected/unknown/do_not_assume` are preserved as continuity evidence. The director_mandate’s strategic question is binding; parent handoff does not silently override SUPERSEDE decision.

## 3. Claims and ceiling
Primary claim: C-RESIDUAL-NOVELTY (bounded scope). This design does not advance the claim status; it only tests measurement readiness.

## 4. Substrate regime (critical distinction)
- Symmetric (previous failures): mandatory, symmetric discovery for every arm (cold/retrieval/treatment). Produced ceiling 1.0 for comparators; treatment tied cold on deterministic counters.
- Asymmetric (this design): discovery cost may be incurred at most once per session/family and amortized/cached across tasks (as permitted by the substrate). This is a different regime than the failed symmetric class.

Explicit exclusion: this experiment must not re-run the mandatory-discovery symmetric REST certificate (third consecutive failure). If asymmetric regime cannot produce discriminating range, the correct action is PARK/document provisioning receipt, not repeat the symmetric class.

## 5. Arms and controls
Baselines: B-COLD-ASYM, B-RETRIEVAL-SHAPED-ASYM, B-LITERAL-KERNEL, B-EMPTIED-REGISTRY. Positive control PC-EXACT-REPLAY. Null control NC-KNOWN-NEGATIVES.

Treatment carrier (reference): git blob b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796 (sha256 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72). The shipped kernel path in repo is separate and not modified by this design.

## 6. Measurement and economics
Economics metric set (counter-only): http_requests + retrieval_calls + verification_calls + repair_attempts. latency_ms/1000 is explicitly excluded as a discriminating instrument. model_calls == 0 and model_tokens == 0 for this readiness design. All counters must be deterministic, reproducible, audit-recomputable from raw evidence.

## 7. Certificate and decision rule
Design-time dynamic-range certificate must be computable and true for B-COLD-ASYM and B-RETRIEVAL-SHAPED-ASYM under asymmetric regime (success_rate_cold_asym < 0.95 at a discriminating novelty level). Treatment liveness (distinct from literal kernel), positive/null controls satisfied, counter-only identifiability, and explicit certificate exclusion are required.

Acceptance criteria: all six freeze_eligibility checks in v2 must be PASS or justified NOT_APPLICABLE; freeze_artifacts_bound is NOT_APPLICABLE with empty list.

## 8. Satisfiability attacks (self-attack required)
Before finalizing DESIGN: check for empty/unreachable branches, missing prerequisites, treatment/comparator identity, ceiling baselines, insensitive controls, and mutable code/data dependencies. Verify the asymmetric regime is genuinely different from symmetric (no hidden symmetry reintroduced). Confirm no outcome-bearing measurements are performed. Verify provisioning path is credential-free and budget-stable.

## 9. Evidence separation
Preserve RAW EVIDENCE → OBSERVATION → DERIVED MEASUREMENT → INTERPRETATION distinction per EXPERIMENT_PACKET.md. Never turn infrastructure unavailability into negative scientific result; if provisioning impossible, record provisioning receipt explicitly.

## 10. Transmission contract
Must produce exactly spec.json and prereg.md in the experiment directory. Use stable metric/control identities. No git commit/push/switch/reset. No EXECUTE/AUDIT/VERDICT generation in DESIGN.
