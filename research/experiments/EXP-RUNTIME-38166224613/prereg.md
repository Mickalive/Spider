# Preregistration: EXP-RUNTIME-38166224613 (DESIGN ONLY)

Experiment ID: EXP-RUNTIME-38166224613
Lane: runtime
Design contract version: 2
Claim: C-MEAS-VALID (substrate validity)

## 1. Scientific question
This is a DESIGN-stage pre-freeze certificate (no outcome-bearing confirmatory measurements). The question is whether a credential-free task bank engineered for ASYMMETRIC discovery—multi-task sessions where one-time session/resource/schema discovery is amortized or cached across tasks—can satisfy an arithmetic dynamic-range certificate that distinguishes it from the bounded-negative mandatory-discovery deterministic REST class, so it can serve as the reusable substrate unblocking B2.

## 2. Hypothesis
There exists at least one credential-free asymmetric-discovery task bank family such that B-COLD-RE-DERIVE.success_rate < 0.95 and B-RETRIEVAL-SHAPED.success_rate < 0.95 at novelty >= 0.50, with matched_correctness >= 0.80 for all arms and treatment/comparator distinguishable. If no such family exists across >=2 independent families, the class is bounded negative.

## 3. Distinctions (non-duplication)
- Distinct from prior replay/cost work (P2-REPLAY-COST): focuses on pre-freeze dynamic-range certificate, not cost measurement.
- Distinct from P2-WP003 leakage precedent: different control plane (task bank substrate readiness), shares measurement-integrity guardrails.
- Follows Director mandate: treats parent handoff as continuity only (SUPERSEDE); does not auto-chain the composite-oracle transfer question.

## 4. Baselines and controls
Baselines:
- B-COLD-RE-DERIVE (cold re-derivation; no reuse beyond environment setup)
- B-RETRIEVAL-SHAPED (strong retrieval-shaped comparator)

Positive control: PC-MATCHED-CORRECTNESS >= 0.80 for all arms.
Null control: NC-TREATMENT-IDENTITY == true (candidate treatment must be distinguishable from comparators).

## 5. Measurement validity (must hold)
MV-ARM-BLIND-SCORING, MV-NOVELTY-FRACTION (novelty>=0.50), MV-ASYMMETRIC-DISCOVERY, MV-FAMILY-INDEPENDENCE (>=2 independent families), MV-MATCHED-TASKS.

## 6. Decision rule (arithmetic, pre-freeze)
Certificate satisfied if all preconditions true AND (B-COLD-RE-DERIVE<0.95 AND B-RETRIEVAL-SHAPED<0.95 at novelty>=0.50) AND all arms have matched_correctness>=0.80 AND treatment distinct. Otherwise CERTIFICATE_UNSATISFIABLE (bounded negative). No freeze occurs if unsatisfiable.

## 7. Design contract v2 (freeze eligibility)
decision_rule_reachability PASS; measurement_prerequisites NOT_APPLICABLE; baseline_identifiability PASS; control_sensitivity PASS; treatment_liveness NOT_APPLICABLE (pre-freeze scan); freeze_artifacts_bound PASS. All mutable local dependencies bound in freeze_artifacts.

## 8. Scope & non-measurement
DESIGN ONLY. No outcome-bearing measurements. Cheap satisfiability probes only. This design neither executes nor reports confirmatory metrics.

## 9. Consequences
Positive: enables B2 substrate with certified dynamic range. Negative: bounded substrate-class negative with arithmetic justification; avoids ceiling rediscovery.
