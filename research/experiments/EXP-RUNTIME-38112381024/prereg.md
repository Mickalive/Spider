# Preregistration: EXP-RUNTIME-38112381024 (Runtime)

**Experiment ID**: EXP-RUNTIME-38112381024  
**Lane**: runtime  
**Design contract version**: 2  
**Mode**: DESIGN ONLY (no outcome measurements)

## Director mandate summary
This experiment implements the Global Research Director mandate for runtime: certify a non-degenerate asymmetric-discovery task bank (B2 prerequisite) arithmetically BEFORE freeze, with cold/retrieval-shaped baselines below ceiling at high residual novelty, matched correctness, real behavioral distinction, honest counters, contamination/dynamic-range certificate. Excludes mandatory-discovery deterministic REST class (no fourth re-run). If unsatisfiable on every credential-free substrate tested (materially different from REST), record bounded substrate-class negative and freeze nothing.

## Question
Can a non-degenerate asymmetric-discovery task bank be certified arithmetically BEFORE freeze with B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED success_rate < 0.95 at novelty >= 0.5 on at least one task family, matched correctness >= 0.80 for all arms, real treatment/comparator behavioral distinction, honest per-condition counters (http_requests + retrieval_calls + verification_calls + repair_attempts), contamination/dynamic-range certificate, and exclusion of mandatory-discovery deterministic REST class?

## Hypothesis
A credential-free asymmetric-discovery multi-task substrate (session/resource/schema discovery amortized or cached across tasks) can satisfy all certificate conditions; else the certificate is unsatisfiable (bounded substrate-class negative, freeze nothing).

## Falsifier
For all credential-free substrates tested that are materially different from mandatory-discovery deterministic REST class, the arithmetic certificate fails. In that case outcome is UNSATISFIABLE with bounded negative for B2 substrate; no execution of treatment effect beyond certification.

## Baselines
- B-COLD-RE-DERIVE: cold re-derivation from minimal priors, no pre-cached solution path for instance. Constraint: success_rate < 0.95 at novelty >= 0.5 on >=1 task family; matched correctness >= 0.80.
- B-RETRIEVAL-SHAPED: retrieval-shaped comparator (shaped recall/usage of prior artifacts), distinct from cold/treatment. Constraint: success_rate < 0.95 at novelty >= 0.5 on >=1 task family; matched correctness >= 0.80.

## Controls
- Positive control (synthetic_non_degenerate_family): constructed family with novelty>=0.5 exhibits baselines < 0.95 and all arms >=0.80 correctness.
- Null control (degenerate_ceiling_family): constructed family where dynamic range should be zero or baselines approach ceiling → certificate rejects.

## Measurement validity
- Honest counters per arm/condition: http_requests, retrieval_calls, verification_calls, repair_attempts; no double-counting.
- Contamination: no leakage of solution artifacts between train/test instances; discovery amortization explicitly modeled; credential-free.
- Exclusion: mandatory-discovery deterministic REST class explicitly excluded (no fourth re-run).
- Behavioral distinct: treatment/comparator differ on >=1 observable behavior (not identity).
- Matched tasks: same task families/constraints across arms; correctness matched >=0.80.
- Stable identities: metric/control identities fixed before any satisfiability probe.

## Decision rule (arithmetic certificate)
CERTIFIED if (exists task family with novelty>=0.5 and B-COLD-RE-DERIVE.success_rate < 0.95 and B-RETRIEVAL-SHAPED.success_rate < 0.95) AND (all arms matched_correctness>=0.80) AND (treatment!=comparator behaviorally) AND (counters complete and contamination bounds satisfied). Else UNSATISFIABLE → bounded substrate-class negative; freeze nothing.

## v2 freeze eligibility (all PASS/NOT_APPLICABLE as specified)
- decision_rule_reachability: PASS (decidable; UNSATISFIABLE branch exists)
- measurement_prerequisites: PASS (counters/novelty/correctness/distinction observable from existing harness)
- baseline_identifiability: PASS (explicit constraints, distinct from treatment)
- control_sensitivity: PASS (positive should certify, null should reject)
- treatment_liveness: NOT_APPLICABLE (substrate certification only; no SPIDER treatment arm executed)
- freeze_artifacts_bound: NOT_APPLICABLE (no mutable local code/data/task-bank/fixture dependencies identified; families constructed from read-only primitives)

## Consequences
- Positive: reusable asymmetric-discovery task bank substrate certified → unblocks B2 inheritance benchmarks (C-PARAM-INHERIT/C-LLM-INHERIT) with honest cost accounting.
- Negative: certificate unsatisfiable on every credential-free substrate tested (materially different from REST) → bounded negative for B2 substrate; do not proceed to full flagship benchmark; repair substrate or PARK thread; freeze nothing.

## Notes on historical precedents
- Replay-cost lesson (pre2 4.114, sha 9687ff787f2d74460bb7006826008852f5b4416b): withdrawn 8.5x to ~1.002x on matched tasks; must use matched tasks and fully loaded counterfactual costs.
- Parent EXP-RUNTIME-37973247935: oracle out-of-surface issue (C-MEAS-VALID scope) — this mandate SUPERSEDES that in favor of B2 substrate certification; mandatory-discovery deterministic REST class explicitly excluded.
