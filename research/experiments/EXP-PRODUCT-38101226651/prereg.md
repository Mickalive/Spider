# EXP-PRODUCT-38101226651 preregistration

## 1. Identity and scope

- experiment_id: EXP-PRODUCT-38101226651
- lane: product; design_contract_version: 2 (request.json)
- claim_ids: ["C-PARAM-INHERIT"] (matches Director target claim; lane charter product.priority_claims)
- request.json: base_sha 954c27fe330988417ab54ac1195b57d80a194f37, claim_registry_sha256 3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b, request_hash b54981713b59dc313bcd40e8746832c6b1d9f5ccc0aca7358ac0b4a100316cb7, cycle_id 38100706570, origin run id 38101226651.
- This packet is the DELIVERY given to EXECUTE and AUDIT: the design, the frozen decision rule, the control identities, the probe record, the promotion-path constraints. The prior PREFREEZE attempt with the same mandate question (EXP-PRODUCT-38099789047) failed at DESIGN stage (design-reviewer infrastructure failure, failure.json "stage exited with code 1", retryable=false); this is a fresh re-attempt, not a re-run of a frozen measurement.

## 2. Director mandate and claim

- allocation: action CONTINUE; claim C-PARAM-INHERIT; cognitive_reset true; parent_handoff_disposition SUPERSEDE; dependencies []; comparative_reasoning LEGACY NO_MATCH with the caveat that the index exposes only path/role/verdict-token fields (no pre-2.0 artifact landed a parameterized inherited mechanism into a shipped kernel).
- Binding strategic question (verbatim from request.json director_mandate.allocation.question): "Can the audited parameterized inherited carrier be landed into the shipped kernel through the sanctioned promotion path - so that after promotion the shipped execution path contains a concrete parameterized mechanism that an inherited procedure visibly instantiates and executes, together with a companion known-negative refusal certificate - such that blocker B1 is satisfied and the pre-freeze executable mechanism required by readiness condition (1) exists, rather than once more running the four-arm economics benchmark on a kernel that still emits literals below the execution threshold?"
- The mandate agent priors are explicit design constraints, applied in this packet: (1) not a measurement-repair loop with an unchanged prerequisite — this packet changes the SHIPPED kernel state; (2) sampling frame/dynamic range certified before freeze — section 7 demonstrates both the floor (0 EXECUTABLE) and the treatment ceiling (6/6) pre-freeze; (3) no ceiling-vs-ceiling indistinguishability — B-LITERAL-KERNEL sits at the floor, treatment at a demonstrated 6/6 that is separated from the literal state by identity + behavior; (4) executable parameterized mechanism + known-negative refusal is the product primitive — this is exactly AD-POSITIVE-ROUNDTRIP + AD-NEGATIVE-ROUNDTRIP sidecar; (5) local-attractor flags trigger reset, not quota — acknowledged; the reset happened via cognitive_reset and this is the single re-attempt built to the v2 standard.
- What this experiment is NOT: it is NOT the four-arm economics benchmark, NOT a C-LLM-INHERIT measurement, NOT a real-Web measurement. It satisfies readiness condition (1) (a shipped executable parameterized carrier / B1); economics and generalization to real LLM/browser substrates remain gated on the provisioned endpoint (parent next_question) and get NO evidence from this packet.

## 3. Inherited state (parent EXP-PRODUCT-37989728440, handoff.json sha256 911f765d04a83974f20d113da206b4075337c3a9bed4c5a77a8f06ffb4773ed9)

Preserved distinctions (carry_forward), adopted as premises — not re-derived here:

- established: frozen-input/carrier integrity (carrier vendored byte-identical to git blob b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796, sha256 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72; shipped src/spider/kernel.py unchanged blob cfec98660b0277ccbf295e8a4119e8d81ddccf50); measurement-valid deterministic run of the economics certificate with zero dynamic range on the mandatory-discovery deterministic REST substrate class; bounded substrate-class negative (both comparators at the 1.0 ceiling); the treatment is causally necessary on that substrate only when discovery is asymmetric, which the economics substrate does not provide; C3 cost-per-success was latency_ms/1000 instrument noise; governance defect (freeze gate not enforced at the time).
- rejected (bounded): certified dynamic range on the mandatory-discovery deterministic REST substrate; counter-only economics advantage of the treatment on that substrate; latency-inclusive cost metric as a discriminator; the asserted-but-absent freeze enforcement.
- unknown: whether ANY credential-free deterministic substrate has certified dynamic range for that arm design; asymmetric/amortized-discovery economics; the four-arm benchmark (requires provisioned endpoint, EXP-INTEL-37973264582); whether the kernel's support-predicate application to free-form payloads is a defect (substrate worked around it); when the freeze-gate repair happened (it is fixed in current scripts/freeze_experiment.py, which now computes and enforces the C1 gate shape via validate_v2_design).
- do_not_assume: (a) no evidence for/against C-RESIDUAL-NOVELTY from the parent; (b) cold/retrieval 1.0 is the substrate ceiling, not a valuation of inheritance; (c) the treatment's parent-packet success is 0 work-compression; (d) THE SHIPPED KERNEL STILL LACKS THE PARAMETERIZED PATH — src/spider/kernel.py remains literal blob cfec9866 (this packet is the delta that changes that); (e) do not freeze certificate-gated packets without enforcement (v2 freeze_experiment.py enforces the six eligibility checks, including a substantive prereg and design_review PASS); (f) do not re-run the economics certificate (a fourth re-run is excluded by the mandate); (g) do not promote code without the sanctioned verdict/promotion path; (h) model_calls=0/model_tokens=0 is zero by construction, never a measured zero-cost claim; (i) the support-generalization ceiling exists: induction from 4 values infers NARROWER supports than the declared grammars (e.g. F1 `^itm\-000[0-9]{1}$` rejects the adjacent `itm-0010`), recorded by audit of EXP-PRODUCT-37950607128/37973256064 as unresolved U-SUPPORT-GENERALIZATION — this packet's positives must stay INSIDE the inferred supports, so it is not a support-generalization result.

## 4. Treatment, baselines, controls

Treatment (T-PARAM-AT-SHIPPING-POSITION): install the audited carrier kernel BYTE-IDENTICALLY at src/spider/kernel.py (the only production module that changes; models/registry/__init__ are byte-identical to the carrier's already — see section 6). The inherited procedure that visibly instantiates the concrete parameterized mechanism is `distill_parameterized` (inherited, unchanged, audited); `resolve` executes it; `verify` confirms templated postconditions; `rebind` is the repair step; `TrajectoryCounters` is the accounting surface.

Baselines (stable ids):
- B-LITERAL-KERNEL (ablation): literal `distill` at confidence 0.5 < min_confidence 0.8, no parameter_slots, preserved unchanged inside the carrier; expected 0 EXECUTABLE on parameterized held-out tasks (FLOOR of dynamic range).
- B-RETRIEVAL-SHAPED (comparator): literal action of the K=5 structurally nearest induction observation (Jaccard over flattened intent/state/action key paths); used ONLY inside AD-TREATMENT-CONTRAST; non-gating.
- B-SHIPPED-PRE-INSTALL (baseline_state): the pre-install shipping kernel identity blob cfec98660b0277ccbf295e8a4119e8d81ddccf50 / sha256 46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61; used for identity contrast and reversion.

Controls (stable ids):
- AD-POSITIVE-ROUNDTRIP (positive): one parameterized Mechanism per family, induced by distill_parameterized from the four induction observations, resolve on the never-observed held-out identifier (re-keyed onto the mechanism's OWN slots — see section 5 mapping rule), fixture execute 200, verify true; uniqueness guard: exactly ONE permutation of slots -> held-out values may resolve EXECUTABLE with correct binding (over-acceptance fails C2).
- AD-NEGATIVE-ROUNDTRIP (known-negative refusal sidecar): all 24 declared negatives (out-of-support empty/space/slash, missing-parameter, out-of-support pair, wrong-intent) refused with non-EXECUTABLE status, bound_action null, non-empty reason; per-category rates all 1.0; sidecar artifact known_negatives.jsonl written.
- NC-ZERO-CONTRAST-TREATMENT (null): comparator-vs-itself contrast must be exactly 0.0 and DETECTED as degenerate (sensitivity check of the contrast instrument).
- PC-ACCOUNTING-FIDELITY: (a) scripted 8-counter trajectory max relative error <= 0.01; (b) real inherited-path exercise on F1: retrieval_calls exactly 3, verification_calls exactly 2, repair_attempts exactly 1; model_calls/model_tokens zero by construction.
- AD-IDENTITY-BINDING: installed kernel sha256/blob == frozen carrier; every freeze artifact matches freeze.json.artifact_hashes; pre/post identity differ.

## 5. Measurement, decision rule, consequences

Full decision rule (C1 identity_binding, C2 positive_roundtrip, C3 known_negative_sidecar, C4 treatment_contrast, C5 accounting_fidelity, C6 literal_control, C7 promotability_tests, OVERALL_OUTCOME SUPPORTS/FALSIFIES/MEASUREMENT_INVALID/BLOCKED) is specified verbatim in spec.json#decision_rule and is the frozen decision instrument. The certificate runner writes raw JSON; the unit tests are NOT the decision instrument.

Slot re-keying rule (frozen): held-out values are located via the family `slot_keys` in `held_out`; they are re-keyed onto the mechanism's OWN inferred slot names. The unique correct permutation is identified by resolve-EXECUTABLE + correct bound identifier; exactly one such permutation must exist per family (probe: F2 maps `query -> q`; F1/F3/F4/F6 map identity; F5 maps `{tenant, item_id}` in the correct order). same rule re-keys negative-case params.

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

Non-outcome-bearing satisfiability/identifiability probe executed at DESIGN (2026-10-11, Python 3.12.15, git 2.55.0), outside the repo (no repo mutation; check_scope design exact-set only permits spec.json/prereg.md). It lays the frozen carrier at the kernel position inside a byte-faithful sandbox replica of the REAL shipping tree and runs the ENTIRE decision machinery plus regression/compile checks; EXECUTE re-runs the identical certificate against the REAL installed package as the confirmatory measurement. A probe/EXECUTE deviation is a measurement-invalidity signal, never a silent pass.

Reproduction (run outside the repo; probe driver source follows verbatim):

    cp /tmp/opencode/probe_exp_38101226651.py .   # sha256 a7f42ec4e87089b10bd18d2e1492e1dd2ca3dc8194ff68608ec665855e2f608e
    python3 probe_exp_38101226651.py > probe_out.txt
    # last line PROBE_SUMMARY <json> is the observed record below.

Observed PROBE_SUMMARY (verbatim, one line):

```json
{"artifact_hashes": {"audited_carrier_kernel": "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72", "fixture": "b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf", "shipped_init": "3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77", "shipped_models": "338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78", "shipped_registry": "51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c", "tests": "ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6", "vendored_models": "338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78", "vendored_registry": "51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c"}, "artifacts_match": true, "certificate": {"accounting_inherited": {"r1_executable": true, "r2_refused": true, "r3_executable": true, "repair_attempts": 1, "retrieval_calls": 3, "v1": true, "v2": true, "verification_calls": 2}, "accounting_scripted_max_rel_err": 0.0, "contrast_degenerate": [{"a_equals_b": true, "family": "F1-PATH-ID"}, {"a_equals_b": true, "family": "F2-QUERY-ID"}, {"a_equals_b": true, "family": "F3-BODY-FIELD"}, {"a_equals_b": true, "family": "F4-HEADER-FIELD"}, {"a_equals_b": true, "family": "F5-TWO-SLOT"}, {"a_equals_b": true, "family": "F6-NOISE-STRESS"}], "contrast_degenerate_all_equal": true, "contrast_real": [{"family": "F1-PATH-ID", "has_mapping": true, "treatment_equals_retrieval": false}, {"family": "F2-QUERY-ID", "has_mapping": true, "treatment_equals_retrieval": false}, {"family": "F3-BODY-FIELD", "has_mapping": true, "treatment_equals_retrieval": false}, {"family": "F4-HEADER-FIELD", "has_mapping": true, "treatment_equals_retrieval": false}, {"family": "F5-TWO-SLOT", "has_mapping": true, "treatment_equals_retrieval": false}, {"family": "F6-NOISE-STRESS", "has_mapping": true, "treatment_equals_retrieval": false}], "contrast_real_unequal_families": 6, "literal_held_out_executable": 0, "negative_all_refused": true, "negative_kind_rates": {"missing_param": 1.0, "out_of_support_empty": 1.0, "out_of_support_pair": 1.0, "out_of_support_slash": 1.0, "out_of_support_space": 1.0, "wrong_intent": 1.0}, "negative_total": 24, "positive": [{"binding_correct": true, "confidence": 0.9, "executable_permutations": 1, "execute_status": 200, "family": "F1-PATH-ID", "mapping": {"item": "item"}, "mechanism": "mech-ad325cd27feb8da1", "no_noise_slots": true, "positive_pass": true, "slots": ["item"], "slots_match_family_count": true, "supports": {"item": "^itm\\-000[0-9]{1}$"}, "unique_executable": true, "verified": true}, {"binding_correct": true, "confidence": 0.9, "executable_permutations": 1, "execute_status": 200, "family": "F2-QUERY-ID", "mapping": {"query": "q"}, "mechanism": "mech-e59412d7b3edb229", "no_noise_slots": true, "positive_pass": true, "slots": ["q"], "slots_match_family_count": true, "supports": {"q": "^[a-z]+$"}, "unique_executable": true, "verified": true}, {"binding_correct": true, "confidence": 0.9, "executable_permutations": 1, "execute_status": 200, "family": "F3-BODY-FIELD", "mapping": {"token": "token"}, "mechanism": "mech-d19d08496a1bd730", "no_noise_slots": true, "positive_pass": true, "slots": ["token"], "slots_match_family_count": true, "supports": {"token": "^tok\\-[0-9]{2}$"}, "unique_executable": true, "verified": true}, {"binding_correct": true, "confidence": 0.9, "executable_permutations": 1, "execute_status": 200, "family": "F4-HEADER-FIELD", "mapping": {"resource": "resource"}, "mechanism": "mech-3e2577335e582a44", "no_noise_slots": true, "positive_pass": true, "slots": ["resource"], "slots_match_family_count": true, "supports": {"resource": "^res\\-[a-z]{1}$"}, "unique_executable": true, "verified": true}, {"binding_correct": true, "confidence": 0.9, "executable_permutations": 1, "execute_status": 200, "family": "F5-TWO-SLOT", "mapping": {"item_id": "item_id", "tenant": "tenant"}, "mechanism": "mech-bf8cbe6329fd99f5", "no_noise_slots": true, "positive_pass": true, "slots": ["item_id", "tenant"], "slots_match_family_count": true, "supports": {"item_id": "^i[0-9]{1}$", "tenant": "^t[0-9]{1}$"}, "unique_executable": true, "verified": true}, {"binding_correct": true, "confidence": 0.9, "executable_permutations": 1, "execute_status": 200, "family": "F6-NOISE-STRESS", "mapping": {"node": "node"}, "mechanism": "mech-213938b55a4850b1", "no_noise_slots": true, "positive_pass": true, "slots": ["node"], "slots_match_family_count": true, "supports": {"node": "^n\\-0[0-9]{1}$"}, "unique_executable": true, "verified": true}], "positive_families_pass": 6}, "compileall_rc": 0, "drift_detected": true, "drift_sha": "42e3b667c8b1e6b2f7cd8636a7de526fe0108da90f7b452b60704ae6bf9eb8c0", "identity_carrier_match": true, "identity_pre_post_differ": true, "pkg_tests_ok": true, "pkg_tests_rc": 0, "preinstall": {"has_distill_parameterized": false}, "preinstall_identity_differs": true, "preinstall_kernel_sha": "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61", "sandbox_kernel_blob": "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796", "sandbox_kernel_sha": "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"}
```

Key values (from PROBE_SUMMARY): sandbox_kernel_sha == 718efa6a... (carrier); sandbox_kernel_blob == b15ed848... (carrier); identity_carrier_match true; identity_pre_post_differ true (46929b3a != 718efa6a); artifacts_match true (all eight hashes); certificate: positive_families_pass 6 (each family: confidence 0.9, unique executable permutation 1, mapping correct, execute status 200, verified true, no noise slots); negative_total 24, negative_all_refused true, kind rates all 1.0; contrast_real_unequal_families 6, contrast_degenerate_all_equal true (degenerate detected); accounting_scripted_max_rel_err 0.0; accounting_inherited {retrieval_calls 3, verification_calls 2, repair_attempts 1, r1/r3 EXECUTABLE, r2 refused, v1/v2 true}; literal_held_out_executable 0; pkg_tests_rc 0 pkg_tests_ok true (canonical `PYTHONPATH=<sandbox src> python -m unittest discover -s tests -v`); compileall_rc 0; preinstall has_distill_parameterized false, preinstall_kernel_sha 46929b3a..., preinstall_identity_differs true; drift_sha 42e3b667... != 718efa6a..., drift_detected true.

Probe driver source (verbatim):

```python
#!/usr/bin/env python3
"""DESIGN pre-freeze satisfiability probe for EXP-PRODUCT-38101226651 (v2).

Non-outcome-bearing: this probe runs the frozen decision machinery against a
BYTE-FAITHFUL SANDBOX REPLICA of the shipping tree (carrier kernel laid at the
kernel position), NOT against the real installed src/spider package. The
confirmatory measurement happens in EXECUTE against the real installed package.

Checks:
  A_SANDBOX_IDENTITY   installed kernel sha256==carrier, blob==carrier, artifacts match
  A_POSITIVE_ROUNDTRIP 6/6 families EXECUTABLE + correct binding + fixture 200 + verify true
  A_NEGATIVE_ROUNDTRIP 24/24 negatives refused, null action, non-empty reason, kinds 1.0
  A_TREATMENT_CONTRAST real contrast > 0.0 on >=1 family AND degenerate detected
  A_ACCOUNTING_FIDELITY scripted max rel err <= 0.01; inherited increments {3,2,1}
  A_LITERAL_CONTROL    B-LITERAL-KERNEL held_out_executable_count == 0
  A_PKG_TESTS          tests/test_kernel.py green under canonical invocation
  A_COMPILEALL         python -m compileall -q on sandbox src, rc 0
  B_PREINSTALL_LIVENESS shipped tree has no distill_parameterized; B-LITERAL 0; identity differs
  C_DRIFT_DETECTION    one-byte kernel drift is detected by identity binding
"""
from __future__ import annotations

import hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
CARRIER_KERNEL = ROOT / "research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py"
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

sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

def make_sandbox(alter_kernel: str | None = None) -> Path:
    sandbox_src = Path(tempfile.mkdtemp(prefix="sandbox_38101226651_")) / "src"
    pkg = sandbox_src / "spider"
    pkg.mkdir(parents=True)
    shutil.copy2(SHIPPED / "__init__.py", pkg / "__init__.py")
    shutil.copy2(SHIPPED / "models.py", pkg / "models.py")
    shutil.copy2(SHIPPED / "registry.py", pkg / "registry.py")
    text = CARRIER_KERNEL.read_text()
    if alter_kernel is not None:
        text = text.replace(alter_kernel[0], alter_kernel[1], 1)
    (pkg / "kernel.py").write_text(text)
    return sandbox_src

def git_blob(path: Path) -> str:
    out = subprocess.run(
        ["git", "hash-object", str(path)], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return out.stdout.strip()

def run_certificate(sandbox_src: Path) -> dict:
    env = dict(os.environ, PYTHONPATH=str(sandbox_src))
    code = r'''
import json, sys
from pathlib import Path
sys.path.insert(0, "/home/runner/work/Spider/Spider")
import importlib.util
spec = importlib.util.spec_from_file_location("fixture", "/home/runner/work/Spider/Spider/research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
from spider.kernel import SpiderKernel, TrajectoryCounters
from spider.registry import MechanismRegistry
from spider.models import Observation, ResolutionStatus
import tempfile

NOISE = set(fixture.NOISE_FIELDS)
by_family = fixture.observations_by_family()
negatives = fixture.negative_cases()
out = {}


def held_params_for(kernel, fam, mech):
    """Freeze-convention mapping: held-out values are taken from the family's
    held_out dict (keyed by family slot_keys) and re-keyed onto the mechaniSM's
    OWN inferred slot names. Callers MUST already have upserTed the induced
    mechanism into kernel.registry. The correct permutation is uniquely
    identified by resolving EXECUTABLE with a correctly bound identifier; a
    kernel that over-accepts produces MORE than one executable permutation and
    FAILS the uniqueness guard, so the convention cannot silently mask
    over-acceptance.
    """
    import itertools
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

# ---- AD-POSITIVE-ROUNDTRIP ----
pos = []
for fam in fixture.FAMILIES:
    key = fam["family"]
    obs = by_family[key]
    with tempfile.TemporaryDirectory() as td:
        reg = MechanismRegistry(str(Path(td) / "m.jsonl"))
        kernel = SpiderKernel(reg, counters=TrajectoryCounters())
        mech = kernel.distill_parameterized(obs)
        row = {"family": key, "mechanism": None, "mapping": None}
        if mech is not None:
            reg.upsert(mech)
            slots = list(mech.parameter_slots)
            supports = mech.verification_rule.get("parameter_supports", {})
            mapping, good = held_params_for(kernel, fam, mech)
            text = fam["bound_identifier"](fam["build_action"](fam["held_out"]))
            executable = len(good) == 1 and good[0]["resolvable"] and good[0]["binding_correct"]
            bound = good[0]["bound"] if good else None
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
                "supports": supports,
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
    with tempfile.TemporaryDirectory() as td:
        reg = MechanismRegistry(str(Path(td) / "m.jsonl"))
        kernel = SpiderKernel(reg)
        mech = kernel.distill_parameterized(by_family[c["family"]])
        if mech is not None:
            reg.upsert(mech)
        mapping, _ = held_params_for(kernel, next(f for f in fixture.FAMILIES if f["family"] == key), mech)
        params = {mapping[k]: v for k, v in c["params"].items() if k in mapping}
        r = kernel.resolve(c["intent"], dict(c["context"]), params)
    status = r.status.value if hasattr(r.status, "value") else str(r.status)
    refused = status != "EXECUTABLE" and r.bound_action is None and bool(r.reason)
    neg.setdefault(c["kind"], []).append({"family": key, "status": status, "refused": refused, "reason": r.reason})
for kind, rows in neg.items():
    rate[kind] = sum(1 for x in rows if x["refused"]) / len(rows)
out["negative_total"] = sum(len(v) for v in neg.values())
out["negative_kind_rates"] = rate
out["negative_all_refused"] = all(x["refused"] for rows in neg.values() for x in rows)

# ---- AD-TREATMENT-CONTRAST ----
real_contrast = []
for fam in fixture.FAMILIES:
    key = fam["family"]
    obs = by_family[key]
    context = {"site": "fixture.invalid", "route": fam["route"], "auth": "public"}
    with tempfile.TemporaryDirectory() as td:
        reg = MechanismRegistry(str(Path(td) / "m.jsonl"))
        kernel = SpiderKernel(reg)
        mech = kernel.distill_parameterized(obs)
        if mech is not None:
            reg.upsert(mech)
        mapping, good = held_params_for(kernel, fam, mech)
        treatment = good[0]["bound"] if good else None
    retrieved = fixture.retrieval_comparator_action(fam["intent"], context, obs)
    real_contrast.append({"family": key, "has_mapping": bool(mapping), "treatment_equals_retrieval": treatment == retrieved})
# degenerate: comparator against itself
degenerate = []
for fam in fixture.FAMILIES:
    key = fam["family"]
    obs = by_family[key]
    context = {"site": "fixture.invalid", "route": fam["route"], "auth": "public"}
    a = fixture.retrieval_comparator_action(fam["intent"], context, obs)
    b = fixture.retrieval_comparator_action(fam["intent"], context, obs)
    degenerate.append({"family": key, "a_equals_b": a == b})
out["contrast_real_unequal_families"] = sum(1 for x in real_contrast if x["has_mapping"] and not x["treatment_equals_retrieval"])
out["contrast_real"] = real_contrast
out["contrast_degenerate_all_equal"] = all(x["a_equals_b"] for x in degenerate)
out["contrast_degenerate"] = degenerate

# ---- PC-ACCOUNTING-FIDELITY ----
c = TrajectoryCounters()
scripted = [("retrieval_calls", 2), ("verification_calls", 1), ("http_requests", 3),
            ("repair_attempts", 1), ("browser_actions", 0), ("model_calls", 0),
            ("model_tokens", 0), ("latency_ms", 0.5)]
for field, amount in scripted:
    c.add(field, amount)
ground = dict(scripted)
errs = []
for k, v in ground.items():
    denom = max(abs(v), 1.0)
    errs.append(abs(c.as_dict()[k] - v) / denom)
out["accounting_scripted_max_rel_err"] = max(errs)

byf = fixture.observations_by_family()
fam1 = fixture.FAMILIES[0]
obs = byf["F1-PATH-ID"]
with tempfile.TemporaryDirectory() as td:
    reg = MechanismRegistry(str(Path(td) / "m.jsonl"))
    mech = kernel = None
    mech = SpiderKernel(reg).distill_parameterized(obs)   # counter-free induction
    if mech is not None:
        reg.upsert(mech)
    mapping, good_ = held_params_for(SpiderKernel(reg), fam1, mech)  # counter-free mapping probe
    counters = TrajectoryCounters()
    kernel = SpiderKernel(reg, counters=counters)         # counters start at zero here
    held = fam1["held_out"]
    p = {mapping[k]: v for k, v in held.items() if k in mapping}
    context = {"site": "fixture.invalid", "route": "items", "auth": "public"}
    r1 = kernel.resolve("fetch_item", context, p)                                 # retrieval_calls 1
    if r1.status != ResolutionStatus.EXECUTABLE:
        raise SystemExit("ACCT r1 not executable: " + json.dumps({"status": r1.status.value if hasattr(r1.status,'value') else str(r1.status), "reason": r1.reason, "registry": [m.mechanism_id for m in reg.all()], "p": p, "good": good_, "mech": mech is not None}))
    v1 = kernel.verify(r1.mechanism_id, fam1["build_next"](held, 99), p)          # verification_calls 1
    r2 = kernel.resolve("fetch_item", context, {mapping["item"]: ""})             # retrieval_calls 2 (refused)
    r3 = kernel.rebind("fetch_item", context, p)                                  # repair_attempts 1 + retrieval_calls 3
    v2 = kernel.verify(r3.mechanism_id, fam1["build_next"](held, 99), p)          # verification_calls 2
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
    obs = by_family[fam["family"]]
    with tempfile.TemporaryDirectory() as td:
        reg = MechanismRegistry(str(Path(td) / "m.jsonl"))
        kernel = SpiderKernel(reg)
        for o in obs:
            m = kernel.distill(o)
            if m is not None:
                reg.upsert(m)
        context = {"site": "fixture.invalid", "route": fam["route"], "auth": "public"}
        slot_keys = list(fam["slot_keys"])
        held = fam["held_out"]
        params = {k: held[k] for k in slot_keys}
        r = kernel.resolve(fam["intent"], context, params)
        if r.status == ResolutionStatus.EXECUTABLE:
            literal_count += 1
out["literal_held_out_executable"] = literal_count

print("PROBE_RESULTS " + json.dumps(out, sort_keys=True))
'''
    proc = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr

results = {}

# ---- A: sandbox with the frozen carrier at the kernel position ----
sandbox = make_sandbox()
installed_sha = sha(sandbox / "spider" / "kernel.py")
installed_blob = git_blob(sandbox / "spider" / "kernel.py")
results["sandbox_kernel_sha"] = installed_sha
results["sandbox_kernel_blob"] = installed_blob
results["identity_carrier_match"] = (installed_sha == CARRIER_KERNEL_SHA) and (installed_blob == CARRIER_KERNEL_BLOB)
results["identity_pre_post_differ"] = SHIPPED_KERNEL_SHA != installed_sha
# frozen artifact identities unchanged in the repo
results["artifact_hashes"] = {
    "audited_carrier_kernel": sha(CARRIER_KERNEL),
    "vendored_models": sha(ROOT / "research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/models.py"),
    "vendored_registry": sha(ROOT / "research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/registry.py"),
    "fixture": sha(FIXTURE),
    "shipped_models": sha(SHIPPED / "models.py"),
    "shipped_registry": sha(SHIPPED / "registry.py"),
    "shipped_init": sha(SHIPPED / "__init__.py"),
    "tests": sha(TESTS / "test_kernel.py"),
}
results["artifacts_match"] = (
    results["artifact_hashes"]["audited_carrier_kernel"] == CARRIER_KERNEL_SHA
    and results["artifact_hashes"]["vendored_models"] == MODELS_SHA
    and results["artifact_hashes"]["vendored_registry"] == REGISTRY_SHA
    and results["artifact_hashes"]["fixture"] == FIXTURE_SHA
    and results["artifact_hashes"]["shipped_models"] == MODELS_SHA
    and results["artifact_hashes"]["shipped_registry"] == REGISTRY_SHA
    and results["artifact_hashes"]["shipped_init"] == INIT_SHA
    and results["artifact_hashes"]["tests"] == TEST_KERNEL_SHA
)
rc, stdout, stderr = run_certificate(sandbox)
assert rc == 0, f"certificate runner failed: rc={rc}\nstdout={stdout}\nstderr={stderr}"
line = next(l for l in stdout.splitlines() if l.startswith("PROBE_RESULTS "))
results["certificate"] = json.loads(line[len("PROBE_RESULTS "):])

# canonical regression invocation against the sandbox replica
env = dict(os.environ, PYTHONPATH=str(sandbox))
tp = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(TESTS), "-v"],
                    cwd=ROOT, env=env, capture_output=True, text=True)
results["pkg_tests_rc"] = tp.returncode
results["pkg_tests_ok"] = tp.returncode == 0 and "OK" in tp.stdout + tp.stderr
cp = subprocess.run([sys.executable, "-m", "compileall", "-q", str(sandbox)], capture_output=True, text=True)
results["compileall_rc"] = cp.returncode

# ---- B: preinstall state of the real shipped tree ----
env_real = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
code_b = r'''
import sys, json
sys.path.insert(0, "/home/runner/work/Spider/Spider")
import importlib.util
spec = importlib.util.spec_from_file_location("fixture", "/home/runner/work/Spider/Spider/research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py")
fixture = importlib.util.module_from_spec(spec); spec.loader.exec_module(fixture)
import spider.kernel as k
out = {"has_distill_parameterized": hasattr(k.SpiderKernel, "distill_parameterized")}
print("PREINSTALL " + json.dumps(out, sort_keys=True))
'''
pb = subprocess.run([sys.executable, "-c", code_b], env=env_real, capture_output=True, text=True)
pbline = next(l for l in (pb.stdout + pb.stderr).splitlines() if l.startswith("PREINSTALL "))
results["preinstall"] = json.loads(pbline[len("PREINSTALL "):])
results["preinstall_kernel_sha"] = sha(SHIPPED / "kernel.py")
results["preinstall_identity_differs"] = sha(SHIPPED / "kernel.py") == SHIPPED_KERNEL_SHA and SHIPPED_KERNEL_SHA != CARRIER_KERNEL_SHA

# ---- C: drift detection ----
drift_sandbox = make_sandbox(alter_kernel=("0.9", "0.8"))
drift_sha = sha(drift_sandbox / "spider" / "kernel.py")
results["drift_sha"] = drift_sha
results["drift_detected"] = drift_sha != CARRIER_KERNEL_SHA

print("PROBE_SUMMARY " + json.dumps(results, sort_keys=True))```

## 8. Validity threats and disclosures

- Deterministic engineering confirmation, not causal discovery: the installed bytes are pinned to the frozen audited carrier; claim-level ceiling per sections 2-3 (C-PARAM-INHERIT stays EXPERIMENTAL until a PASS audit + verdict + promotion; economics/generalization untouched).
- The support-generalization ceiling (U-SUPPORT-GENERALIZATION) is inherited and acknowledged; positives stay inside inferred supports; this packet is not a free-form payload result.
- Wrong-intent refusals share the generic 'no applicable validated mechanism' reason with the null-type control (parent-audit caveat); the sidecar categorizes by harness mapping; distinct intent-mismatch detection is not independently demonstrated.
- model_calls=0/model_tokens=0 are by construction (no model invoked), not a measured zero-cost claim (parent do_not_assume (h)).
- Promotion is an operational dependency (product-promote.yml diffs pre_execute_sha -> verdict-creation commit over allowed_code_roots; a diverged main can hard-stop the 3-way apply) — not a scientific falsifier.
- Determinism of the negative-sidecar measurement is bounded by the fixture being deterministic and credential-free; the fixture's deterministic executor returns 412/422 protocol responses that are part of the certificate's negative expectations only insofar as they are never reached (all negatives must be refused BEFORE execution at resolve time).

## 9. Promotion-path operational notes

- EXECUTE may mutate ONLY src/spider/kernel.py (replace with the carrier bytes) and ADD tests/test_ship_kernel.py under the Product execute scope (check_scope.py execute prefixes: experiment dir + allowed_code_roots [src, tests, sdk, pyproject.toml]). Nothing else under src/ tests/ sdk/ pyproject.toml may change; sdk/ and pyproject.toml must remain untouched.
- recording: scripts/record_execution_base.py writes execution_checkpoint.json (pre_execute_sha) before EXECUTE; do not modify frozen files (request.json/spec.json/prereg.md/freeze.json/execution_checkpoint.json).
- result.json/report.md/provenance.json must follow research/EXPERIMENT_PACKET.md shapes exactly; status/outcome semantics: valid scientific negative -> status COMPLETE + outcome FALSIFIES; instrumentation failure -> MEASUREMENT_INVALID; environment failure -> BLOCKED.
- after a non-SUPPORTS outcome, revert_product_reject.py restores the code-root delta to pre_execute_sha (B-SHIPPED-PRE-INSTALL) leaving no residue.
- the certificate runner must capture both stdout and stderr (unittest protocol is emitted on stderr under CPython).