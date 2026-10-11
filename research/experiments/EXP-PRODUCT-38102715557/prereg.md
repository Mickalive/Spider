# EXP-PRODUCT-38102715557 preregistration

## 1. Identity and scope

- experiment_id: EXP-PRODUCT-38102715557
- lane: product; design_contract_version: 2 (request.json)
- claim_ids: ["C-PARAM-INHERIT"] (matches Director target claim; lane charter product.priority_claims)
- request.json: base_sha 954c27fe330988417ab54ac1195b57d80a194f37, claim_registry_sha256 3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b, request_hash 3f79814bcb47e9a6235e6ead8e6abceacc167f4556349466dacae146b5ba158b, cycle_id 38102323363, origin run id 38102715557.
- This packet is the DELIVERY given to EXECUTE and AUDIT: the design, the frozen decision rule, the control identities, the probe record, the promotion-path constraints. Predecessors with the same mandate (EXP-PRODUCT-38099789047, 38094123727, 38101226651 and earlier) failed at DESIGN stage; eight were design-reviewer model infrastructure failures (failure.json "stage exited with code 1", retryable=false) and one (38094123727) received a REVISE review that was discarded. This is a fresh re-attempt under a NEW request/experiment id, not a re-run of a frozen measurement.
- This design was additionally self-attacked at DESIGN by a fresh-context adversarial reviewer; the one genuine defect it found (the original null control compared a deterministic pure function to itself and was therefore tautological / insensitive) was REPAIRED before this preregistration was written: the null now runs through the same explicit two-sided contrast instrument as the real arm, with a perturbation canary.

## 2. Director mandate and claim

- allocation: action CONTINUE; claim C-PARAM-INHERIT; cognitive_reset true; parent_handoff_disposition SUPERSEDE; dependencies []; comparative_reasoning LEGACY: DISTINCT_EXTENSION with the caveat that the legacy index exposes only path/role/verdict-token fields (no pre-2.0 artifact landed a parameterized inherited mechanism into a shipped kernel). A targeted legacy search for 'distill_parameterized promotion / shipped carrier' returned nothing relevant.
- Binding strategic question (verbatim from request.json director_mandate.allocation.question): "Can the audited parameterized inherited carrier be landed into the shipped kernel through the sanctioned promotion path - so that after promotion the shipped execution path contains a concrete parameterized mechanism that an inherited procedure visibly instantiates and executes, together with a companion known-negative refusal certificate - such that blocker B1 is satisfied and the pre-freeze executable mechanism required by readiness condition (1) exists, rather than once more running the four-arm economics benchmark on a kernel that still emits literals below the execution threshold?"
- The mandate agent priors are explicit design constraints, applied in this packet: (1) not a measurement-repair loop with an unchanged prerequisite -- this packet changes the SHIPPED kernel state; (2) sampling frame/dynamic range certified before freeze -- section 7 demonstrates both the floor (0 EXECUTABLE) and the treatment ceiling (6/6) pre-freeze; (3) no ceiling-vs-ceiling indistinguishability -- B-LITERAL-KERNEL sits at the floor, treatment at a demonstrated 6/6 that is separated from the literal state by identity + behavior; (4) executable parameterized mechanism + known-negative refusal is the product primitive -- this is exactly AD-POSITIVE-ROUNDTRIP + AD-NEGATIVE-ROUNDTRIP sidecar; (5) local-attractor flags trigger reset, not quota -- acknowledged; the reset happened via cognitive_reset and this is the re-attempt built to the v2 standard.
- What this experiment is NOT: it is NOT the four-arm economics benchmark, NOT a C-LLM-INHERIT measurement, NOT a real-Web measurement. It satisfies readiness condition (1) (a shipped executable parameterized carrier / B1); economics and generalization to real LLM/browser substrates remain gated on the provisioned endpoint (parent next_question) and get NO evidence from this packet.

## 3. Inherited state (parent EXP-PRODUCT-37989728440, handoff.json sha256 911f765d04a83974f20d113da206b4075337c3a9bed4c5a77a8f06ffb4773ed9)

Preserved distinctions (carry_forward), adopted as premises -- not re-derived here. parent_handoff_disposition is SUPERSEDE, so this packet does not fund the parent's next_question; it performs the Director's promotion task instead.

- established: frozen-input/carrier integrity (carrier vendored byte-identical to git blob b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796, sha256 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72; shipped src/spider/kernel.py unchanged blob cfec98660b0277ccbf295e8a4119e8d81ddccf50); measurement-valid deterministic run of the economics certificate with zero dynamic range on the mandatory-discovery deterministic REST substrate class; bounded substrate-class negative (both comparators at the 1.0 ceiling); the treatment is causally necessary on that substrate only when discovery is asymmetric, which the economics substrate does not provide; C3 cost-per-success was latency_ms/1000 instrument noise; governance defect (freeze gate not enforced at the time).
- rejected (bounded): certified dynamic range on the mandatory-discovery deterministic REST substrate; counter-only economics advantage of the treatment on that substrate; latency-inclusive cost metric as a discriminator; the asserted-but-absent freeze enforcement.
- unknown: whether ANY credential-free deterministic substrate has certified dynamic range for that arm design; asymmetric/amortized-discovery economics; the four-arm benchmark (requires provisioned endpoint, EXP-INTEL-37973264582); whether the kernel's support-predicate application to free-form payloads is a defect (substrate worked around it); when the freeze-gate repair happened (it is fixed in current scripts/freeze_experiment.py, which now computes and enforces the C1 gate shape via validate_v2_design).
- do_not_assume: (a) no evidence for/against C-RESIDUAL-NOVELTY from the parent; (b) cold/retrieval 1.0 is the substrate ceiling, not a valuation of inheritance; (c) the treatment's parent-packet success is 0 work-compression; (d) THE SHIPPED KERNEL STILL LACKS THE PARAMETERIZED PATH -- src/spider/kernel.py remains literal blob cfec9866 (this packet is the delta that changes that); (e) do not freeze certificate-gated packets without enforcement (v2 freeze_experiment.py enforces the six eligibility checks, including a substantive prereg and design_review PASS); (f) do not re-run the economics certificate (a fourth re-run is excluded by the mandate); (g) do not promote code without the sanctioned verdict/promotion path; (h) model_calls=0/model_tokens=0 is zero by construction, never a measured zero-cost claim; (i) the support-generalization ceiling exists: induction from 4 values infers NARROWER supports than the declared grammars (e.g. F1 infers a narrow digit-class/quantity that rejects adjacent unseen forms), recorded by audit of EXP-PRODUCT-37950607128/37973256064 as unresolved U-SUPPORT-GENERALIZATION -- this packet's positives must stay INSIDE the inferred supports, so it is not a support-generalization result.

## 4. Treatment, baselines, controls

Treatment (T-PARAM-AT-SHIPPING-POSITION): install the audited carrier kernel BYTE-IDENTICALLY at src/spider/kernel.py (the only production module that changes; models/registry/__init__ are byte-identical to the carrier's already -- see section 6). The inherited procedure that visibly instantiates the concrete parameterized mechanism is `distill_parameterized` (inherited, unchanged, audited); `resolve` executes it; `verify` confirms templated postconditions; `rebind` is the repair step; `TrajectoryCounters` is the accounting surface.

Baselines (stable ids):
- B-LITERAL-KERNEL (ablation): literal `distill` at confidence 0.5 < min_confidence 0.8, no parameter_slots, preserved unchanged inside the carrier; expected 0 EXECUTABLE on parameterized held-out tasks (FLOOR of dynamic range). Probe observed 0.
- B-RETRIEVAL-SHAPED (comparator): literal action of the K=5 structurally nearest induction observation (Jaccard over flattened intent/state/action key paths); used ONLY inside AD-TREATMENT-CONTRAST; non-gating.
- B-SHIPPED-PRE-INSTALL (baseline_state): the pre-install shipping kernel identity blob cfec98660b0277ccbf295e8a4119e8d81ddccf50 / sha256 46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61; used for identity contrast and reversion.

Controls (stable ids):
- AD-POSITIVE-ROUNDTRIP (positive): one parameterized Mechanism per family, induced by distill_parameterized from the four induction observations, resolve on the never-observed held-out identifier (re-keyed onto the mechanism's OWN slots -- see section 5 mapping rule), fixture execute 200, verify true; uniqueness guard: exactly ONE permutation of slots -> held-out values may resolve EXECUTABLE with correct binding (over-acceptance fails C2).
- AD-NEGATIVE-ROUNDTRIP (known-negative refusal sidecar): all 24 declared negatives (out-of-support empty/space/slash, missing-parameter, out-of-support pair, wrong-intent) refused with non-EXECUTABLE status, bound_action null, non-empty reason; per-category rates all 1.0; sidecar artifact known_negatives.jsonl written.
- NC-ZERO-CONTRAST-TREATMENT (null): the ONE explicit two-sided contrast instrument contrast_instrument(family, treatment_action, comparator_action) extracts each action's family bound identifier and returns score 0.0 when they are equal, 1.0 when they differ. Three arms share it: (real) parameterized held-out bound action vs retrieved literal action; (degenerate null) comparator action on BOTH sides; (perturbation canary) two distinct valid induction actions. C4 passes only if real == 1.0/differ on 6/6, degenerate == 0.0/equal on 6/6 (degenerate_variant_detected true), and perturbation == 1.0/differ on 6/6. A hard-wired instrument cannot satisfy all three; this replaces the original comparator-vs-itself comparison that an adversarial reviewer correctly rejected as tautological.
- PC-ACCOUNTING-FIDELITY: (a) scripted 8-counter trajectory max relative error <= 0.01; (b) real inherited-path exercise on F1: retrieval_calls exactly 3, verification_calls exactly 2, repair_attempts exactly 1; model_calls/model_tokens zero by construction.
- AD-IDENTITY-BINDING: installed kernel sha256/blob == frozen carrier; every freeze artifact matches freeze.json.artifact_hashes; pre/post identity differ.

## 5. Measurement, decision rule, consequences

Full decision rule (C1 identity_binding, C2 positive_roundtrip, C3 known_negative_sidecar, C4 treatment_contrast, C5 accounting_fidelity, C6 literal_control, C7 promotability_tests, OVERALL_OUTCOME SUPPORTS/FALSIFIES/MEASUREMENT_INVALID/BLOCKED with explicit precedence) is specified verbatim in spec.json#decision_rule and is the frozen decision instrument. The certificate runner writes raw JSON; the unit tests are NOT the decision instrument.

OVERALL_OUTCOME precedence (frozen): (1) BLOCKED if install/certificate cannot run; (2) MEASUREMENT_INVALID if C1 fails or any of C3/C4/C5/C6 fails; (3) FALSIFIES if C1 passed and (C2 or C7 fails); (4) SUPPORTS iff C1-C7 all PASS. A non-C1-passing install is never FALSIFIES.

Slot re-keying rule (frozen): held-out values are located via the family `slot_keys` in `held_out`; they are re-keyed onto the mechanism's OWN inferred slot names. The unique correct permutation is identified by resolve-EXECUTABLE + correct bound identifier; exactly one such permutation must exist per family (probe: F2 maps `query -> q`; F1/F3/F4/F6 map identity; F5 maps `{tenant, item_id}` in the correct order). The same rule re-keys negative-case params.

Consequences:
- positive (SUPPORTS): blocker B1 / readiness condition (1) satisfied on the shipped path; packet recommends promote_to_product=true; DIRECTOR may advance C-PARAM-INHERIT to PRODUCT_CORE after PASS audit + promotion; promotion applies ONLY the audited delta (src/spider/kernel.py + tests/test_ship_kernel.py) via product-promote.yml.
- negative (FALSIFIES over a C1-passing install): audited carrier not promotable in audited form; bounded integration-defect diagnosis next; revert to B-SHIPPED-PRE-INSTALL (revert_product_reject.py); C-PARAM-INHERIT stays EXPERIMENTAL.
- MEASUREMENT_INVALID (C1/C3/C4/C5/C6 failure): instrumentation fault, not a scientific negative; repair + new frozen packet; no promotion.
- BLOCKED: infrastructure/prerequisite failure (e.g., src/ unwritable, runner cannot execute); never encoded as FALSIFIES.

## 6. Freeze artifacts and identities

Freeze artifacts (existing repository files; sha256 at freeze time recorded in freeze.json.artifact_hashes):

| path | sha256 |
|---|---|
| research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py | 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72 (blob b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796) |
| research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/models.py | 338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78 |
| research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/registry.py | 51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c |
| research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py | b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf |
| src/spider/models.py | 338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78 |
| src/spider/registry.py | 51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c |
| src/spider/__init__.py | 3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77 |
| tests/test_kernel.py | ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6 |

src/spider/kernel.py is deliberately NOT a freeze artifact: EXECUTE replaces its content; its post-install identity is pinned by decision_rule C1 to the frozen carrier hash (718efa6a.../b15ed848...) and its pre-install identity is B-SHIPPED-PRE-INSTALL (46929b3a.../cfec9866...). models.py and registry.py are bound TWICE (vendored copy and shipped copy) because they must be byte-identical before/after install; __init__.py is the kept public surface.

## 7. Pre-freeze satisfiability probe (v2)

Non-outcome-bearing satisfiability/identifiability probe executed at DESIGN (2026-10-11, Python 3.12.15, git 2.55.0), outside the repository (no repo mutation; check_scope design exact-set only permits spec.json/prereg.md). It lays the frozen carrier at the kernel position inside a byte-faithful sandbox replica of the REAL shipping tree and runs the ENTIRE decision machinery plus regression/compile checks; EXECUTE re-runs the identical certificate against the REAL installed package as the confirmatory measurement. A probe/EXECUTE deviation is a measurement-invalidity signal, never a silent pass.

Reproduction (run outside the repo; probe driver source follows verbatim):

    python3 probe_exp_38102715557.py > probe_out.txt
    # sha256 of the driver below: 9ea65e41591e8385c0d49b8ac7ae82a2ea69e6209b71320c7bd6a962a6fa8e3e
    # last line "PROBE_SUMMARY <json>" is the observed record embedded next.

Observed PROBE_SUMMARY (verbatim JSON, parsed from the probe's last line):

```json
{
 "artifact_hashes": {
  "audited_carrier_kernel": "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72",
  "fixture": "b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf",
  "shipped_init": "3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77",
  "shipped_models": "338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78",
  "shipped_registry": "51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c",
  "tests": "ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6",
  "vendored_models": "338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78",
  "vendored_registry": "51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c"
 },
 "artifacts_match": true,
 "certificate": {
  "accounting_inherited": {
   "r1_executable": true,
   "r2_refused": true,
   "r3_executable": true,
   "repair_attempts": 1,
   "retrieval_calls": 3,
   "v1": true,
   "v2": true,
   "verification_calls": 2
  },
  "accounting_scripted_max_rel_err": 0.0,
  "contrast_degenerate": [
   {
    "comparable": true,
    "comparator_id": "'itm-0001'",
    "differ": false,
    "family": "F1-PATH-ID",
    "score": 0.0,
    "treatment_id": "'itm-0001'"
   },
   {
    "comparable": true,
    "comparator_id": "'alpha'",
    "differ": false,
    "family": "F2-QUERY-ID",
    "score": 0.0,
    "treatment_id": "'alpha'"
   },
   {
    "comparable": true,
    "comparator_id": "'tok-11'",
    "differ": false,
    "family": "F3-BODY-FIELD",
    "score": 0.0,
    "treatment_id": "'tok-11'"
   },
   {
    "comparable": true,
    "comparator_id": "'res-a'",
    "differ": false,
    "family": "F4-HEADER-FIELD",
    "score": 0.0,
    "treatment_id": "'res-a'"
   },
   {
    "comparable": true,
    "comparator_id": "('t1', 'i1')",
    "differ": false,
    "family": "F5-TWO-SLOT",
    "score": 0.0,
    "treatment_id": "('t1', 'i1')"
   },
   {
    "comparable": true,
    "comparator_id": "'n-01'",
    "differ": false,
    "family": "F6-NOISE-STRESS",
    "score": 0.0,
    "treatment_id": "'n-01'"
   }
  ],
  "contrast_degenerate_all_equal": true,
  "contrast_perturbation": [
   {
    "comparable": true,
    "comparator_id": "'itm-0002'",
    "differ": true,
    "family": "F1-PATH-ID",
    "score": 1.0,
    "treatment_id": "'itm-0001'"
   },
   {
    "comparable": true,
    "comparator_id": "'beta'",
    "differ": true,
    "family": "F2-QUERY-ID",
    "score": 1.0,
    "treatment_id": "'alpha'"
   },
   {
    "comparable": true,
    "comparator_id": "'tok-22'",
    "differ": true,
    "family": "F3-BODY-FIELD",
    "score": 1.0,
    "treatment_id": "'tok-11'"
   },
   {
    "comparable": true,
    "comparator_id": "'res-b'",
    "differ": true,
    "family": "F4-HEADER-FIELD",
    "score": 1.0,
    "treatment_id": "'res-a'"
   },
   {
    "comparable": true,
    "comparator_id": "('t2', 'i2')",
    "differ": true,
    "family": "F5-TWO-SLOT",
    "score": 1.0,
    "treatment_id": "('t1', 'i1')"
   },
   {
    "comparable": true,
    "comparator_id": "'n-02'",
    "differ": true,
    "family": "F6-NOISE-STRESS",
    "score": 1.0,
    "treatment_id": "'n-01'"
   }
  ],
  "contrast_perturbation_all_differ": true,
  "contrast_real": [
   {
    "comparable": true,
    "comparator_id": "'itm-0001'",
    "differ": true,
    "family": "F1-PATH-ID",
    "score": 1.0,
    "treatment_id": "'itm-0009'"
   },
   {
    "comparable": true,
    "comparator_id": "'alpha'",
    "differ": true,
    "family": "F2-QUERY-ID",
    "score": 1.0,
    "treatment_id": "'epsilon'"
   },
   {
    "comparable": true,
    "comparator_id": "'tok-11'",
    "differ": true,
    "family": "F3-BODY-FIELD",
    "score": 1.0,
    "treatment_id": "'tok-99'"
   },
   {
    "comparable": true,
    "comparator_id": "'res-a'",
    "differ": true,
    "family": "F4-HEADER-FIELD",
    "score": 1.0,
    "treatment_id": "'res-z'"
   },
   {
    "comparable": true,
    "comparator_id": "('t1', 'i1')",
    "differ": true,
    "family": "F5-TWO-SLOT",
    "score": 1.0,
    "treatment_id": "('t9', 'i9')"
   },
   {
    "comparable": true,
    "comparator_id": "'n-01'",
    "differ": true,
    "family": "F6-NOISE-STRESS",
    "score": 1.0,
    "treatment_id": "'n-09'"
   }
  ],
  "contrast_real_all_positive": true,
  "contrast_real_unequal_families": 6,
  "literal_held_out_executable": 0,
  "negative_all_refused": true,
  "negative_kind_rates": {
   "missing_param": 1.0,
   "out_of_support_empty": 1.0,
   "out_of_support_pair": 1.0,
   "out_of_support_slash": 1.0,
   "out_of_support_space": 1.0,
   "wrong_intent": 1.0
  },
  "negative_total": 24,
  "positive": [
   {
    "binding_correct": true,
    "confidence": 0.9,
    "executable_permutations": 1,
    "execute_status": 200,
    "family": "F1-PATH-ID",
    "mapping": {
     "item": "item"
    },
    "mechanism": "mech-ad325cd27feb8da1",
    "no_noise_slots": true,
    "positive_pass": true,
    "slots": [
     "item"
    ],
    "slots_match_family_count": true,
    "unique_executable": true,
    "verified": true
   },
   {
    "binding_correct": true,
    "confidence": 0.9,
    "executable_permutations": 1,
    "execute_status": 200,
    "family": "F2-QUERY-ID",
    "mapping": {
     "query": "q"
    },
    "mechanism": "mech-e59412d7b3edb229",
    "no_noise_slots": true,
    "positive_pass": true,
    "slots": [
     "q"
    ],
    "slots_match_family_count": true,
    "unique_executable": true,
    "verified": true
   },
   {
    "binding_correct": true,
    "confidence": 0.9,
    "executable_permutations": 1,
    "execute_status": 200,
    "family": "F3-BODY-FIELD",
    "mapping": {
     "token": "token"
    },
    "mechanism": "mech-d19d08496a1bd730",
    "no_noise_slots": true,
    "positive_pass": true,
    "slots": [
     "token"
    ],
    "slots_match_family_count": true,
    "unique_executable": true,
    "verified": true
   },
   {
    "binding_correct": true,
    "confidence": 0.9,
    "executable_permutations": 1,
    "execute_status": 200,
    "family": "F4-HEADER-FIELD",
    "mapping": {
     "resource": "resource"
    },
    "mechanism": "mech-3e2577335e582a44",
    "no_noise_slots": true,
    "positive_pass": true,
    "slots": [
     "resource"
    ],
    "slots_match_family_count": true,
    "unique_executable": true,
    "verified": true
   },
   {
    "binding_correct": true,
    "confidence": 0.9,
    "executable_permutations": 1,
    "execute_status": 200,
    "family": "F5-TWO-SLOT",
    "mapping": {
     "item_id": "item_id",
     "tenant": "tenant"
    },
    "mechanism": "mech-bf8cbe6329fd99f5",
    "no_noise_slots": true,
    "positive_pass": true,
    "slots": [
     "item_id",
     "tenant"
    ],
    "slots_match_family_count": true,
    "unique_executable": true,
    "verified": true
   },
   {
    "binding_correct": true,
    "confidence": 0.9,
    "executable_permutations": 1,
    "execute_status": 200,
    "family": "F6-NOISE-STRESS",
    "mapping": {
     "node": "node"
    },
    "mechanism": "mech-213938b55a4850b1",
    "no_noise_slots": true,
    "positive_pass": true,
    "slots": [
     "node"
    ],
    "slots_match_family_count": true,
    "unique_executable": true,
    "verified": true
   }
  ],
  "positive_families_pass": 6
 },
 "compileall_rc": 0,
 "drift_detected": true,
 "drift_sha": "42e3b667c8b1e6b2f7cd8636a7de526fe0108da90f7b452b60704ae6bf9eb8c0",
 "identity_carrier_match": true,
 "identity_pre_post_differ": true,
 "pkg_tests_ok": true,
 "pkg_tests_rc": 0,
 "preinstall_has_distill_parameterized": false,
 "preinstall_identity_differs": true,
 "preinstall_kernel_sha": "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61",
 "sandbox_kernel_blob": "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796",
 "sandbox_kernel_sha": "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
}
```

Key values (from PROBE_SUMMARY): sandbox_kernel_sha == 718efa6a... (carrier); sandbox_kernel_blob == b15ed848... (carrier); identity_carrier_match true; identity_pre_post_differ true (46929b3a != 718efa6a); artifacts_match true (all eight hashes); certificate: positive_families_pass 6 (each family: confidence 0.9, unique executable permutation 1, mapping correct, execute status 200, verified true, no noise slots); negative_total 24, negative_all_refused true, kind rates all 1.0; two-sided contrast instrument: contrast_real_unequal_families 6 and contrast_real_all_positive true (treatment held-out identifier differs from the retrieved induction identifier), contrast_degenerate_all_equal true (score 0.0, degenerate null detected), contrast_perturbation_all_differ true (score 1.0 on two distinct valid induction actions, proving the instrument is not stuck at 0.0); accounting_scripted_max_rel_err 0.0; accounting_inherited {retrieval_calls 3, verification_calls 2, repair_attempts 1, r1/r3 EXECUTABLE, r2 refused, v1/v2 true}; literal_held_out_executable 0; pkg_tests_rc 0 pkg_tests_ok true (canonical `PYTHONPATH=<sandbox src> python -m unittest discover -s tests -v`); compileall_rc 0; preinstall_has_distill_parameterized false, preinstall_kernel_sha 46929b3a..., preinstall_identity_differs true; drift_sha 42e3b667c8b1e6b2f7cd8636a7de526fe0108da90f7b452b60704ae6bf9eb8c0 != 718efa6a..., drift_detected true.

Probe driver source (verbatim; sha256 9ea65e41591e8385c0d49b8ac7ae82a2ea69e6209b71320c7bd6a962a6fa8e3e):

```python
#!/usr/bin/env python3
"""DESIGN pre-freeze satisfiability probe for EXP-PRODUCT-38102715557 (v2).

Non-outcome-bearing: runs the frozen decision machinery against a BYTE-FAITHFUL
SANDBOX REPLICA of the shipping tree (audited carrier kernel laid at the kernel
position), NOT against the real installed src/spider package. The confirmatory
measurement happens in EXECUTE against the real installed package.

Checks:
  A_SANDBOX_IDENTITY    installed kernel sha256==carrier, blob==carrier, artifacts match
  A_POSITIVE_ROUNDTRIP  6/6 families EXECUTABLE + correct binding + fixture 200 + verify true
  A_NEGATIVE_ROUNDTRIP  24/24 negatives refused, null action, non-empty reason, kinds 1.0
  A_TREATMENT_CONTRAST  two-sided contrast instrument: real differ 6/6, degenerate 0.0
                        (null), perturbation canary differ, all via the SAME instrument
  A_ACCOUNTING_FIDELITY scripted max rel err <= 0.01; inherited increments {3,2,1}
  A_LITERAL_CONTROL     B-LITERAL-KERNEL held_out_executable_count == 0
  A_PKG_TESTS           tests/test_kernel.py green under canonical invocation
  A_COMPILEALL          python -m compileall -q on sandbox src, rc 0
  B_PREINSTALL_LIVENESS shipped tree has no distill_parameterized; identity differs
  C_DRIFT_DETECTION     one-byte kernel drift is detected by identity binding
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
CARRIER = ROOT / "research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider"
FIXTURE = ROOT / "research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py"
SHIPPED = ROOT / "src/spider"
TESTS = ROOT / "tests"

CARRIER_KERNEL_SHA = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
CARRIER_KERNEL_BLOB = "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796"
SHIPPED_KERNEL_SHA = "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61"
MODELS_SHA = "338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78"
REGISTRY_SHA = "51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c"
INIT_SHA = "3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77"
TEST_KERNEL_SHA = "ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6"
FIXTURE_SHA = "b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf"


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def make_sandbox(alter_kernel=None) -> Path:
    sandbox_src = Path(tempfile.mkdtemp(prefix="sandbox_38102715557_")) / "src"
    pkg = sandbox_src / "spider"
    pkg.mkdir(parents=True)
    shutil.copy2(SHIPPED / "__init__.py", pkg / "__init__.py")
    shutil.copy2(SHIPPED / "models.py", pkg / "models.py")
    shutil.copy2(SHIPPED / "registry.py", pkg / "registry.py")
    text = (CARRIER / "kernel.py").read_text()
    if alter_kernel is not None:
        text = text.replace(alter_kernel[0], alter_kernel[1], 1)
    (pkg / "kernel.py").write_text(text)
    return sandbox_src


def git_blob(path: Path) -> str:
    out = subprocess.run(["git", "hash-object", str(path)], cwd=ROOT,
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


CERTIFICATE = r'''
import json, sys, itertools, tempfile
from pathlib import Path
sys.path.insert(0, "/home/runner/work/Spider/Spider")
import importlib.util
spec = importlib.util.spec_from_file_location("fixture", "/home/runner/work/Spider/Spider/research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
from spider.kernel import SpiderKernel, TrajectoryCounters
from spider.registry import MechanismRegistry
from spider.models import ResolutionStatus

NOISE = set(fixture.NOISE_FIELDS)
by_family = fixture.observations_by_family()
negatives = fixture.negative_cases()
out = {}


def held_params_for(kernel, fam, mech):
    slots = list(mech.parameter_slots)
    keys = list(fam["slot_keys"])
    expected = fam["bound_identifier"](fam["build_action"](fam["held_out"]))
    good = []
    for perm in itertools.permutations(slots):
        params = {slot: fam["held_out"][key] for slot, key in zip(perm, keys)}
        context = {"site": "fixture.invalid", "route": fam["route"], "auth": "public"}
        r = kernel.resolve(fam["intent"], context, params)
        if r.status == ResolutionStatus.EXECUTABLE:
            ident = fam["bound_identifier"](r.bound_action) if r.bound_action is not None else None
            good.append({"perm": perm, "params": params, "resolvable": True,
                         "binding_correct": ident == expected, "bound": r.bound_action})
    mapping = {}
    if len(good) == 1 and good[0]["binding_correct"]:
        mapping = {key: slot for slot, key in zip(good[0]["perm"], keys)}
    return mapping, good


def bound_identifier(fam, action):
    """Extract the family's bound identifier from an action; None if not one."""
    if action is None:
        return None
    try:
        return repr(fam["bound_identifier"](action))
    except Exception:
        return None


def contrast_instrument(fam, treatment_action, comparator_action):
    """The ONE contrast instrument used by both the real and null arms.

    Compares the bound identifier the family actually executes.  It returns a
    score in {0.0, 1.0} and a boolean; it can return either value depending on
    its inputs, which is exactly what the degenerate null and the perturbation
    canary jointly establish.
    """
    ti = bound_identifier(fam, treatment_action)
    ci = bound_identifier(fam, comparator_action)
    if ti is None or ci is None:
        return {"comparable": False, "differ": None, "score": None,
                "treatment_id": ti, "comparator_id": ci}
    differ = ti != ci
    return {"comparable": True, "differ": differ, "score": 1.0 if differ else 0.0,
            "treatment_id": ti, "comparator_id": ci}


# ---- AD-POSITIVE-ROUNDTRIP ----
pos = []
treatment_by_family = {}
for fam in fixture.FAMILIES:
    key = fam["family"]
    obs = by_family[key]
    with tempfile.TemporaryDirectory() as td:
        reg = MechanismRegistry(str(Path(td) / "m.jsonl"))
        kernel = SpiderKernel(reg, counters=TrajectoryCounters())
        mech = kernel.distill_parameterized(obs)
        row = {"family": key, "mechanism": None}
        if mech is not None:
            reg.upsert(mech)
            slots = list(mech.parameter_slots)
            supports = mech.verification_rule.get("parameter_supports", {})
            mapping, good = held_params_for(kernel, fam, mech)
            executable = len(good) == 1 and good[0]["resolvable"] and good[0]["binding_correct"]
            bound = good[0]["bound"] if good else None
            treatment_by_family[key] = bound
            executed = fixture.fixture_execute(bound) if bound is not None else None
            verified = False
            if executable and bound is not None and mech.mechanism_id:
                params = good[0]["params"]
                verified = kernel.verify(mech.mechanism_id, fam["build_next"](fam["held_out"], 99), params)
            row.update({
                "mechanism": mech.mechanism_id,
                "confidence": mech.confidence,
                "slots": slots,
                "slots_match_family_count": len(slots) == len(fam["slot_keys"]),
                "no_noise_slots": not (set(slots) & NOISE),
                "executable_permutations": len(good),
                "unique_executable": len(good) == 1,
                "mapping": mapping,
                "binding_correct": good[0]["binding_correct"] if good else False,
                "execute_status": executed.get("status") if isinstance(executed, dict) else None,
                "verified": verified,
                "positive_pass": executable and bool(mapping) and executed is not None
                                and executed.get("status") == 200 and verified,
            })
        pos.append(row)
out["positive"] = pos
out["positive_families_pass"] = sum(1 for x in pos if x.get("positive_pass"))

# ---- AD-NEGATIVE-ROUNDTRIP ----
neg = {}
rate = {}
for c in negatives:
    key = c["family"]
    fam = next(f for f in fixture.FAMILIES if f["family"] == key)
    with tempfile.TemporaryDirectory() as td:
        reg = MechanismRegistry(str(Path(td) / "m.jsonl"))
        kernel = SpiderKernel(reg)
        mech = kernel.distill_parameterized(by_family[key])
        if mech is not None:
            reg.upsert(mech)
        mapping, _ = held_params_for(kernel, fam, mech)
        params = {mapping[k]: v for k, v in c["params"].items() if k in mapping}
        r = kernel.resolve(c["intent"], dict(c["context"]), params)
    status = r.status.value if hasattr(r.status, "value") else str(r.status)
    refused = status != "EXECUTABLE" and r.bound_action is None and bool(r.reason)
    neg.setdefault(c["kind"], []).append({"family": key, "status": status, "refused": refused})
for kind, rows in neg.items():
    rate[kind] = sum(1 for x in rows if x["refused"]) / len(rows)
out["negative_total"] = sum(len(v) for v in neg.values())
out["negative_kind_rates"] = rate
out["negative_all_refused"] = all(x["refused"] for rows in neg.values() for x in rows)

# ---- AD-TREATMENT-CONTRAST (single two-sided instrument) ----
real_contrast = []
degenerate = []
perturbation = []
for fam in fixture.FAMILIES:
    key = fam["family"]
    obs = by_family[key]
    context = {"site": "fixture.invalid", "route": fam["route"], "auth": "public"}
    treatment = treatment_by_family.get(key)
    retrieved = fixture.retrieval_comparator_action(fam["intent"], context, obs)
    # real: treatment bound action vs retrieved literal action
    real = contrast_instrument(fam, treatment, retrieved)
    real_contrast.append({"family": key, **real})
    # degenerate null: the SAME instrument with the comparator on BOTH sides
    degen = contrast_instrument(fam, retrieved, retrieved)
    degenerate.append({"family": key, **degen})
    # perturbation canary: feed the SAME instrument two structurally valid but
    # DIFFERENT induction actions and confirm it flips to differ=True (proves
    # the instrument can return 1.0 and is not stuck at 0.0)
    a0 = fam["build_action"](fam["induction"][0])
    a1 = fam["build_action"](fam["induction"][1])
    pert = contrast_instrument(fam, a0, a1)
    perturbation.append({"family": key, **pert})
out["contrast_real"] = real_contrast
out["contrast_real_unequal_families"] = sum(
    1 for x in real_contrast if x["comparable"] and x["differ"])
out["contrast_real_all_positive"] = all(
    x["comparable"] and x["differ"] and x["score"] == 1.0 for x in real_contrast)
out["contrast_degenerate"] = degenerate
out["contrast_degenerate_all_equal"] = all(
    x["comparable"] and (not x["differ"]) and x["score"] == 0.0 for x in degenerate)
out["contrast_perturbation"] = perturbation
out["contrast_perturbation_all_differ"] = all(
    x["comparable"] and x["differ"] and x["score"] == 1.0 for x in perturbation)

# ---- PC-ACCOUNTING-FIDELITY ----
c = TrajectoryCounters()
scripted = [("retrieval_calls", 2), ("verification_calls", 1), ("http_requests", 3),
            ("repair_attempts", 1), ("browser_actions", 0), ("model_calls", 0),
            ("model_tokens", 0), ("latency_ms", 0.5)]
for field, amount in scripted:
    c.add(field, amount)
errs = []
for k, v in dict(scripted).items():
    errs.append(abs(c.as_dict()[k] - v) / max(abs(v), 1.0))
out["accounting_scripted_max_rel_err"] = max(errs)

fam1 = fixture.FAMILIES[0]
obs = by_family["F1-PATH-ID"]
with tempfile.TemporaryDirectory() as td:
    reg = MechanismRegistry(str(Path(td) / "m.jsonl"))
    mech = SpiderKernel(reg).distill_parameterized(obs)
    if mech is not None:
        reg.upsert(mech)
    mapping, _ = held_params_for(SpiderKernel(reg), fam1, mech)
    counters = TrajectoryCounters()
    kernel = SpiderKernel(reg, counters=counters)
    held = fam1["held_out"]
    p = {mapping[k]: v for k, v in held.items() if k in mapping}
    context = {"site": "fixture.invalid", "route": "items", "auth": "public"}
    r1 = kernel.resolve("fetch_item", context, p)
    v1 = kernel.verify(r1.mechanism_id, fam1["build_next"](held, 99), p)
    r2 = kernel.resolve("fetch_item", context, {mapping["item"]: ""})
    r3 = kernel.rebind("fetch_item", context, p)
    v2 = kernel.verify(r3.mechanism_id, fam1["build_next"](held, 99), p)
    got = counters.as_dict()
out["accounting_inherited"] = {
    "retrieval_calls": got["retrieval_calls"], "verification_calls": got["verification_calls"],
    "repair_attempts": got["repair_attempts"], "r1_executable": r1.status == ResolutionStatus.EXECUTABLE,
    "v1": v1, "r2_refused": r2.bound_action is None, "r3_executable": r3.status == ResolutionStatus.EXECUTABLE,
    "v2": v2,
}

# ---- B-LITERAL-KERNEL ----
literal_count = 0
for fam in fixture.FAMILIES:
    with tempfile.TemporaryDirectory() as td:
        reg = MechanismRegistry(str(Path(td) / "m.jsonl"))
        kernel = SpiderKernel(reg)
        for o in by_family[fam["family"]]:
            m = kernel.distill(o)
            if m is not None:
                reg.upsert(m)
        context = {"site": "fixture.invalid", "route": fam["route"], "auth": "public"}
        params = {k: fam["held_out"][k] for k in fam["slot_keys"]}
        r = kernel.resolve(fam["intent"], context, params)
        if r.status == ResolutionStatus.EXECUTABLE:
            literal_count += 1
out["literal_held_out_executable"] = literal_count

print("PROBE_RESULTS " + json.dumps(out, sort_keys=True))
'''


def run_certificate(sandbox_src: Path):
    env = dict(os.environ, PYTHONPATH=str(sandbox_src))
    return subprocess.run([sys.executable, "-c", CERTIFICATE], env=env,
                          capture_output=True, text=True)


results = {}

sandbox = make_sandbox()
installed_sha = sha(sandbox / "spider" / "kernel.py")
installed_blob = git_blob(sandbox / "spider" / "kernel.py")
results["sandbox_kernel_sha"] = installed_sha
results["sandbox_kernel_blob"] = installed_blob
results["identity_carrier_match"] = (
    installed_sha == CARRIER_KERNEL_SHA and installed_blob == CARRIER_KERNEL_BLOB)
results["identity_pre_post_differ"] = SHIPPED_KERNEL_SHA != installed_sha

results["artifact_hashes"] = {
    "audited_carrier_kernel": sha(CARRIER / "kernel.py"),
    "vendored_models": sha(CARRIER / "models.py"),
    "vendored_registry": sha(CARRIER / "registry.py"),
    "fixture": sha(FIXTURE),
    "shipped_models": sha(SHIPPED / "models.py"),
    "shipped_registry": sha(SHIPPED / "registry.py"),
    "shipped_init": sha(SHIPPED / "__init__.py"),
    "tests": sha(TESTS / "test_kernel.py"),
}
ah = results["artifact_hashes"]
results["artifacts_match"] = (
    ah["audited_carrier_kernel"] == CARRIER_KERNEL_SHA
    and ah["vendored_models"] == MODELS_SHA
    and ah["vendored_registry"] == REGISTRY_SHA
    and ah["fixture"] == FIXTURE_SHA
    and ah["shipped_models"] == MODELS_SHA
    and ah["shipped_registry"] == REGISTRY_SHA
    and ah["shipped_init"] == INIT_SHA
    and ah["tests"] == TEST_KERNEL_SHA
)

proc = run_certificate(sandbox)
if proc.returncode != 0:
    print("CERTIFICATE_RC", proc.returncode)
    print(proc.stdout)
    print(proc.stderr)
    raise SystemExit(1)
line = next(l for l in proc.stdout.splitlines() if l.startswith("PROBE_RESULTS "))
results["certificate"] = json.loads(line[len("PROBE_RESULTS "):])

env = dict(os.environ, PYTHONPATH=str(sandbox))
tp = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(TESTS), "-v"],
                    cwd=ROOT, env=env, capture_output=True, text=True)
results["pkg_tests_rc"] = tp.returncode
results["pkg_tests_ok"] = tp.returncode == 0 and "OK" in (tp.stdout + tp.stderr)
cp = subprocess.run([sys.executable, "-m", "compileall", "-q", str(sandbox)],
                    capture_output=True, text=True)
results["compileall_rc"] = cp.returncode

# preinstall state of the real shipped tree
env_real = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
pre = subprocess.run([sys.executable, "-c",
    "import spider.kernel as k; print('PREINSTALL', k.SpiderKernel.__dict__.get('distill_parameterized') is not None)"],
    env=env_real, capture_output=True, text=True)
results["preinstall_has_distill_parameterized"] = "True" in pre.stdout
results["preinstall_kernel_sha"] = sha(SHIPPED / "kernel.py")
results["preinstall_identity_differs"] = (
    sha(SHIPPED / "kernel.py") == SHIPPED_KERNEL_SHA and SHIPPED_KERNEL_SHA != CARRIER_KERNEL_SHA)

# drift detection
drift = make_sandbox(alter_kernel=("return 0.9", "return 0.8"))
results["drift_sha"] = sha(drift / "spider" / "kernel.py")
results["drift_detected"] = results["drift_sha"] != CARRIER_KERNEL_SHA

print("PROBE_SUMMARY " + json.dumps(results, sort_keys=True))

```

## 8. Validity threats and disclosures

- Deterministic engineering confirmation, not causal discovery: the installed bytes are pinned to the frozen audited carrier; claim-level ceiling per sections 2-3 (C-PARAM-INHERIT stays EXPERIMENTAL until a PASS audit + verdict + promotion; economics/generalization untouched).
- The support-generalization ceiling (U-SUPPORT-GENERALIZATION) is inherited and acknowledged; positives stay inside inferred supports; this packet is not a free-form payload result.
- Wrong-intent refusals share the generic 'no applicable validated mechanism' reason with the null-type control (parent-audit caveat); the sidecar categorizes by harness mapping; distinct intent-mismatch detection is not independently demonstrated.
- model_calls=0/model_tokens=0 are by construction (no model invoked), not a measured zero-cost claim (parent do_not_assume (h)).
- Contrast instrument honesty: the contrast instrument compares the family's executed bound identifier, not full action dicts; it is deliberately two-sided (real 1.0, degenerate 0.0, perturbation canary 1.0). It is a behavioral-difference check, not a semantic-similarity metric; the real arm's difference is the substantive one (held-out identifier vs observed identifier), and it is reported per family.
- C2-FALSIFIES is nearly degenerate by construction because the install is byte-pinned to a previously-audited carrier; the genuinely informative FALSIFIES route is C7 (regression/compile surface), where the EXECUTE-added test module is unpinned new code. This is disclosed rather than hidden.
- The certificate runner is not a repository file; its exact logic is frozen verbatim in this section (sha256 of the embedded driver is the same as the driver sha above) and its raw JSON output is the primary evidence. tests/test_ship_kernel.py is EXECUTE-added and therefore unpinned; the decision never depends on it alone (C2-C6 gate from the certificate JSON).
- Promotion is an operational dependency (product-promote.yml diffs pre_execute_sha -> verdict-creation commit over allowed_code_roots; a diverged main can hard-stop the 3-way apply) -- not a scientific falsifier. This packet demonstrates promotability (C7); the actual promotion is the later DIRECTOR/workflow step, not part of EXECUTE.
- There is no stochastic arm-to-arm variation and no sampling error in the decision instrument; therefore no p-value/replicate argument is required or made. The only variability is installation/identity, which C1 and the reversion path handle.

## 9. Promotion-path operational notes

- EXECUTE may mutate ONLY src/spider/kernel.py (replace with the carrier bytes) and ADD tests/test_ship_kernel.py under the Product execute scope (check_scope.py execute prefixes: experiment dir + allowed_code_roots [src, tests, sdk, pyproject.toml]). Nothing else under src/ tests/ sdk/ pyproject.toml may change; sdk/ and pyproject.toml must remain untouched.
- recording: scripts/record_execution_base.py writes execution_checkpoint.json (pre_execute_sha) before EXECUTE; do not modify frozen files (request.json/spec.json/prereg.md/freeze.json/execution_checkpoint.json).
- result.json/report.md/provenance.json must follow research/EXPERIMENT_PACKET.md shapes exactly; status/outcome semantics: valid scientific negative -> status COMPLETE + outcome FALSIFIES; instrumentation failure -> MEASUREMENT_INVALID; environment failure -> BLOCKED.
- after a non-SUPPORTS outcome, revert_product_reject.py restores the code-root delta to pre_execute_sha (B-SHIPPED-PRE-INSTALL) leaving no residue.
- the certificate runner must capture both stdout and stderr (unittest protocol is emitted on stderr under CPython).
