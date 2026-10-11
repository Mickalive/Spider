# Preregistration: EXP-PRODUCT-38107837348

## 1. Context and Director Mandate

**Global Research Director allocation**: PIVOT to Product lane, action PIVOT, claim_id C-PARAM-INHERIT.

**Binding strategic question** (from request.json.director_mandate.allocation.question):
> Can the already-audited parameterized mechanism carrier be installed into the shipped kernel and promoted through the audited product promotion path with a binding pre-freeze positive/negative certificate - src/spider/kernel.py gains a distill_parameterized -> resolve -> execute -> verify/UNKNOWN path whose confidence flow is not defeated by the current literal distill() candidate confidence 0.5 versus default execution threshold 0.8; the frozen experiment demonstrates one known-positive executable binding (an unseen-identifier parameterized mechanism executes) and one known-negative refusal (a binding the carrier cannot safely resolve returns UNKNOWN rather than a wrong execution), records the honest counters and the pinned git blob / sha256 of the shipped version for the later four-arm benchmark, and triggers promotion only on independent audit PASS - thereby discharging blocker B1?

**Parent handoff disposition**: SUPERSEDE (from Director mandate). The inherited parent handoff (EXP-PRODUCT-37989728440) is continuity evidence only and must not override the Director decision. We preserve established/rejected/unknown/do_not_assume distinctions.

## 2. Claims Under Test

**Primary: C-PARAM-INHERIT** — "Mechanisms parameterize to unseen identifiers"
- Registry status: EXPERIMENTAL
- Owner lanes: graph, product
- Product capability: parameterized inheritance
- This experiment discharges blocker B1 (shipped parameterized carrier) for the downstream four-arm benchmark.

## 3. Design (Design-Only)

This is a DESIGN-only task as specified. We do not run outcome-bearing measurements. We specify the smallest rigorous high-information experiment.

**Treatment target**: Install the audited parameterized mechanism carrier (git blob b15ed848, sha256 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72 from EXP-PRODUCT-37973256064) into the shipped kernel at `src/spider/kernel.py`. The integration must:
- Add `distill_parameterized()` that induces mechanisms from observations with parameter_slots/support predicates
- Ensure `resolve()` correctly binds parameters and respects `min_confidence` (default 0.8)
- Preserve literal `distill()` behavior (confidence 0.5) so it remains below threshold
- Return `UNKNOWN` with `bound_action=null` on unsafe bindings (known-negative)

**Known-positive test case** (unseen identifier): Mechanism induced from training observation, then resolved with params for an unseen identifier within inferred support → `EXECUTABLE` with correct `bound_action`.

**Known-negative test case** (unsafe binding): Attempt to resolve with out-of-support identifier / wrong intent / missing required parameter → `UNKNOWN`, `bound_action=null`, non-empty reason. Must refuse unsafe execution.

**Controls**:
- B-LITERAL-KERNEL: literal candidate (conf 0.5) must not become EXECUTABLE (threshold separation)
- B-EMPTY-REGISTRY: no applicable mechanisms → UNKNOWN
- NC-KNOWN-NEGATIVE: verifies abstention over wrong execution

## 4. Satisfiability Checks (Design-Contract v2)

We address all six freeze_eligibility checks:

1. **decision_rule_reachability** (PASS): The decision rule is decidable from test outcomes (boolean checks C1-C7). No arithmetic impossibility.
2. **measurement_prerequisites** (PASS): Tests use only in-process kernel calls; no external model/network dependencies required for the gate tests. Environment available (Python 3.12).
3. **baseline_identifiability** (PASS): B-LITERAL-KERNEL and B-EMPTY-REGISTRY provide clear baselines with expected behaviors.
4. **control_sensitivity** (PASS): NC-KNOWN-NEGATIVE is sensitive to the critical safety property (must return UNKNOWN, not EXECUTABLE). Known-positive must fire for treatment.
5. **treatment_liveness** (PASS): Treatment is the integration of the audited carrier into src/spider/kernel.py - structurally capable of being EXECUTABLE (carrier demonstrated liveness in prior experiment). Integration is feasible.
6. **freeze_artifacts_bound** (NOT_APPLICABLE): No mutable local code/data/task-bank/fixture dependencies outside the kernel under test that can change interpretation of the gate. We list `src/spider/kernel.py` as a freeze artifact for identity binding.

**Design attack (self-critique):**
- Treatment/comparator identity: B-LITERAL-KERNEL is the ablation (literal path only); treatment adds parameterized path. Separation verified.
- Ceiling/floor baselines: B-EMPTY-REGISTRY gives UNKNOWN floor; known-positive gives EXECUTABLE ceiling.
- Insensitive controls: NC-KNOWN-NEGATIVE directly tests the safety-critical property (abstention). Will catch if code returns EXECUTABLE on unsafe input.
- Empty/unreachable branches: All C1-C7 are reachable boolean conditions.
- Missing prerequisites: The audited carrier blob b15ed848 exists (verified from prior experiments); integration is local to src/spider/kernel.py.
- Mutable artifacts: Only src/spider/kernel.py itself is mutable in scope; we bind it via freeze_artifacts.

## 5. Decision Rule

C1-C7 as specified in spec.json. OVERALL: SUPPORTS if all C1-C7 PASS; FALSIFIES if any fail.

Promotion to product core (or marking promotion-ready) is **only** authorized if SUPPORTS and independent audit PASS. This matches the Director mandate.

## 6. Consequences

**Positive outcome (SUPPORTS + audit PASS):**
- B1 discharged. Shipped kernel has parameterized mechanism carrier with verified liveness and verified abstention.
- Kernel identity (blob/sha256/path) pinned for downstream four-arm C-LLM-INHERIT benchmark.
- Enables progression toward C-PARAM-INHERIT validation and C-PRODUCT-ECON/C-LLM-INHERIT benchmarks.
- Carrier integrated under Product lane scope with safety gate (UNKNOWN on unsafe bindings).

**Negative outcome (FALSIFIES):**
- B1 not discharged. Parameterized carrier remains experimental, not in shipped kernel.
- Downstream four-arm benchmark cannot use shipped kernel path for this carrier until fixed.
- Investigation required: fix integration (distill_parameterized missing/broken, threshold defeated, known-negative not refusing, regression). New experiment only if materially different fix; do not weaken preregistration.

## 7. Parent Handoff Preservation

From EXP-PRODUCT-37989728440 handoff, we preserve:
- **established**: Kernel carrier identity (b15ed848, sha256 718efa6a...) is the reference implementation; real-substrate liveness/separation established previously. 
- **rejected**: Do not promote without frozen gate passing; do not assume shipped kernel has parameterized path (it currently has cfec9866 without distill_parameterized).
- **unknown**: Endpoint/model provisioning separate (Intel lane); this is purely kernel integration/promotion gate.
- **do_not_assume**: Shipped kernel lacks treatment carrier; freeze gate must pass; promotion only on audit PASS.

The Director’s SUPERSEDE means we follow director_mandate over parent_handoff.next_question.

## 8. Design-Only Constraints

- No outcome-bearing measurements during DESIGN.
- Cheap satisfiability probes allowed (e.g. check method existence, verify code compiles, inspect confidence flow).
- Do not modify files outside granted scope (Product lane: src, tests, sdk, pyproject.toml). This targets src/spider/kernel.py.
- Use stable metric/control identities for downstream transmission.
- Never git commit/push/switch/reset.

## 9. References

- EXP-PRODUCT-37973256064: audit PASS, carrier b15ed848/sha256 718efa6a..., known-positive/known-negative established on real substrate.
- EXP-PRODUCT-37989728440: handoff preserving distinctions.
- Director mandate (request.json): B1 promotion+qualification with known-positive and known-negative, bind identity for four-arm benchmark.
