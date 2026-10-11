# Preregistration: EXP-PRODUCT-38112384171 (PRODUCT lane)

**Design contract:** v2 (governed). **Lane:** product. **Claim:** C-PARAM-INHERIT.

## 1. Question (binding)
Can the audited parameterized mechanism carrier be installed byte-identically at `src/spider/kernel.py` with frozen identity
- git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`
- sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`

and pass a binding pre-freeze certificate that verifies:
(a) positive: resolve EXECUTABLE, confidence >= 0.9, bound action non-null, deterministic execute(status=200, verified=true) on an unseen held-out identifier from >=3 induction observations;
(b) negative: ResolutionStatus.UNKNOWN, null bound action, recorded reason for known-unsafe/unknown cases;
(c) inherited counters honest and invariant;
(d) installed identity equals frozen identity?

## 2. Hypothesis
Installing the frozen carrier byte-identically at the shipping kernel path produces the behavior above.

## 3. Baselines
- **B-LITERAL-DISTILL**: current literal distill() confidence 0.5 < min_confidence 0.8 -> not executable; confirms gating is active.

## 4. Controls
- **Positive (PC-PARAM-BOUND)**: frozen carrier parameterized binding from >=3 induction observations on unseen held-out identifier. Must satisfy: status==EXECUTABLE, confidence>=0.9, bound_action!=null, execute.status==200, execute.verified==true.
- **Null (NC-UNSAFE-UNKNOWN)**: out-of-support/missing-parameters/wrong-intent. Must satisfy: status==UNKNOWN, bound_action==null, reason present, no EXECUTABLE returned.

## 5. Falsifier
Any failure of (a)-(d) under frozen certificate (status/confidence mismatch, execute mismatch, unsafe case returns EXECUTABLE, counter integrity violation, identity mismatch).

## 6. Measurement validity
Criteria: identity hash matches frozen; `distill_parameterized` exists/callable; counter invariants hold (no double-counting); fixture execution deterministic; treatment/comparator distinct. Threats: packaging/path drift, identity substitution, counter conflation, non-deterministic fixture, threshold regression.

## 7. Decision rule (frozen)
Preconditions: installed identity == frozen sha256 AND PC-PARAM-BOUND passes all criteria AND NC-UNSAFE-UNKNOWN passes all criteria AND baselines behave as specified AND counter_invariants_valid == true. Success if ALL true; failure if any.

## 8. Consequences
- **Positive:** Discharges B1 (parameterized carrier shipped). Promotion ONLY after independent audit PASS. Enables B2/B3 without degeneracy.
- **Negative:** B1 remains blocked; kernel unchanged; no promotion; record exact failing criterion; minimal fix without weakening prereg.

## 9. Freeze eligibility (v2)
All six checks: decision_rule_reachability PASS, measurement_prerequisites PASS, baseline_identifiability PASS, control_sensitivity PASS, treatment_liveness PASS, freeze_artifacts_bound PASS.

## 10. Freeze artifacts
- `src/spider/kernel.py` (mutable local; bound by hash in freeze.json).

This is a design-only preregistration; no outcome-bearing measurements were performed during DESIGN.