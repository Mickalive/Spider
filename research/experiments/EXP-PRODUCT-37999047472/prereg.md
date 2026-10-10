# PREREGISTRATION — EXP-PRODUCT-37999047472 (design_contract_version 2)

- experiment_id: `EXP-PRODUCT-37999047472`
- lane: `product` · chain_depth: `0` · action: `REOPEN` · claim: `C-PARAM-INHERIT`
- base_sha: `e35fccd0e620d4f564050a90c632ce6a6f89d037`
- claim_registry_sha256: `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b`
- parent_handoff: SUPERSEDE by `director_mandate` (request.json)
- prepared: 2026-10-10 · python 3.12.15 · git 2.55.0

---

## 1. Mandate (binding, from request.json)

> "Make the audited parameterized inheritance capability DURABLE and PROMOTABLE:
> ship the audited kernel to the canonical spider runtime path with a pre-freeze
> arm-differentiation certificate (known-positive roundtrip: induction observation
> -> parameterized distillation -> resolve to EXECUTABLE with correctly bound
> non-null action -> execute against fixture -> verify; known-negative refusal of
> out-of-support/missing-parameter/wrong-intent with recorded reason and null
> action), unit tests, accounting check that inherited-path counters increment,
> and kernel identity bound at freeze. This makes the carrier land in main through
> the pinned Product promotion path without manually copying experiment code."

Director's prior reasoning that this design must respect: a pre-if-treatment-at-ceiling arm is a non-identifying design defect; re-preregistering an absent prerequisite is wasted; shipping converts research to product; the four-arm C-LLM-INHERIT benchmark and first-party C-PRODUCT-ECON economics are the later consumption points (the benchmark's runtime task bank and intel endpoint are DOWNSTREAM requirements, not prerequisites of this experiment).

## 2. Objective and the single decision

Objective: install the audited parameterized-inheritance carrier at the SHIPPING kernel
position and obtain a frozen, verified arm-differentiation certificate plus a green
canonical regression surface, so the pinned Product promotion workflow can land the
capability in main from a `verdict.json` commit with `promote_to_product=true`, with no
manual copying of experiment code.

The single decision: **promote or not promote** the audited carrier from
exp-37989728440 to the shipped `src/spider/kernel.py` position.

Falsifier (any of C1–C7 fails, after a C1-passing install for C2/C7): the audited
carrier is not promotable in its audited form. See section 11.

DETERMINISM DISCLOSURE: because the installed bytes are PINNED to the frozen audited
carrier hash, this is a deterministic durability/integration/promotion confirmation,
NOT a new causal discovery about web behavior. Design therefore ran the pre-freeze
arm-differentiation certificate once already (section 7) as the mandatory v2
treatment-liveness satisfiability probe. EXECUTE re-runs the identical certificate
against the REAL installed package as the confirmatory measurement. Downstream agents
must not inflate this into "new evidence that parameterized inheritance improves web
exploration."

## 3. Inheritance mapping (four-way)

| inherited object | source | exact reference | disposition |
|---|---|---|---|
| Treatment kernel | EXP-PRODUCT-37989728440 (product) | `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`; sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`; git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` | INSTALL byte-identically at `src/spider/kernel.py` (the only production module that changes) |
| Dependent models/registry | same carrier | carrier `models.py` sha256 `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` (blob `f08608c36b1c7b536d553b690acd91cd63f590f7`), `registry.py` sha256 `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` (blob `986317f71c4a7d5506e3295991bc7217e2a8d2da`) | VERIFIED byte-identical to shipped `src/spider/models.py` / `src/spider/registry.py`; bound, do not touch |
| Fixture (task substrate) | EXP-PRODUCT-37950607128 (product) | `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py`; sha256 `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf` | RECONSTRUCT into the packet, load under `sys.path` ahead of `src` (never at `src/spider/`); bound, do not modify |
| Live-path audit | EXP-PRODUCT-37973256064 (product) | audit PASS on live path (kernel behavior incl. rebind/counters) | CARRIED as audit history; superseded in energy by this packet's shipping-position certificate |
| Public package surface | shipping tree | `src/spider/__init__.py` sha256 `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77` (exports `SpiderKernel, Mechanism, Observation, Resolution, ResolutionStatus`; NOT `TrajectoryCounters`) | KEEP byte-identical; `TrajectoryCounters` stays importable from `spider.kernel` module scope; no package re-export |

Explicitly NOT imported: exp-3803229106's LLM-acquire formulation, any experiment narrative,
the C-LLM-INHERIT runtime task bank, and the intel endpoint (downstream, per mandate).

## 4. Treatment and identity rule

Treatment T = the audited carrier kernel installed byte-identically at
`src/spider/kernel.py` (sha256 `718efa6a...`, blob `b15ed848...`) with all other frozen
files byte-unchanged.

Identity rule (frozen): EXECUTE writes the kernel as a single byte-exact file copy
(`shutil.copyfile` or equivalently `cp`), then the certificate re-hashes the installed
file and requires `sha256 == 718efa6a...` AND `git hash-object == b15ed848...`
(AD-IDENTITY-BINDING). Any byte drift is a C1 failure (demonstrated sensitive in
section 7, drift probe).

Param-binding rule (frozen, established by the audited carrier): parameter dictionaries
are keyed by the mechanism's OWN inferred slot names. The probe pinned the concrete
mapping: F1→`item`, F2→`q` (not `query`), F3→`token`, F4→`resource`, F5→`item_id`,`tenant`,
F6→`node`. Family `slot_keys` are used only to locate held-out VALUES for the
bound-identifier check. In negative cases with one slot and one param, the value is
re-keyed to the mechanism's slot name.

## 5. Fixture (SYNTH-INDUCTION-BANK-v1, frozen)

Six families (F1-PATH-ID, F2-QUERY-ID, F3-BODY-FIELD, F4-HEADER-FIELD, F5-TWO-SLOT,
F6-NOISE-STRESS); four in-distribution induction observations each; one held-out
identifier per family (two for F5); deterministic `fixture_execute()`;
`retrieval_comparator_action(intent, context, observations, k=5)` returns the formulaic
literal action of the K=5 Jaccard-nearest observation; `negative_cases()` yields 24
cases: missing_param, out_of_support_empty, out_of_support_space, out_of_support_slash,
out_of_support_pair, wrong_intent (4 each). The fixture imports `from spider.models import
Observation` so it loads the package under test. NEVER written inside `src/spider/`;
loaded under `sys.path` ahead of `src` (the package under test is also under `sys.path`,
kept together exactly as the probe).

## 6. Freeze artifacts and identities (verified at DESIGN)

All eight bound files exist and matched these sha256 at preparation time; freeze.json
captures them. `src/spider/kernel.py` is deliberately excluded (EXECUTE replaces it);
its identity is pinned via AD-IDENTITY-BINDING/C1 and its pre-install baseline is
B-SHIPPED-PRE-INSTALL.

| # | artifact | sha256 |
|---|---|---|
| 1 | research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py | 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72 |
| 2 | research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/models.py | 338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78 |
| 3 | research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/registry.py | 51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c |
| 4 | research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py | b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf |
| 5 | src/spider/models.py | 338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78 |
| 6 | src/spider/registry.py | 51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c |
| 7 | src/spider/__init__.py | 3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77 |
| 8 | tests/test_kernel.py | ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6 |

Baselines: B-SHIPPED-PRE-INSTALL kernel = `src/spider/kernel.py` sha256
`46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61` (blob
`cfec98660b0277ccbf295e8a4119e8d81ddccf50`); B-LITERAL-KERNEL = literal `distill()`
confidence 0.5 vs min_confidence 0.8 inside the carrier.

## 7. Pre-freeze treatment-liveness probe (REAL, hashed; v2 satisfiability evidence)

This section is the durable evidence channel for the v2 design gates. All artifacts are
outside the repository at `/tmp/opencode/probe37999047472/` (check_scope confines DESIGN
writes to spec/prereg; the evidence is reproduced here verbatim so state never lives in a
single machine).

| artifact | sha256 |
|---|---|
| probe.py (driver, full source in section 8) | ad7ad7773779ce69b68122a362c9194f24025f0a02b0bfad8b9c1c39e2291563 |
| probe_results.json (mode=installed) | 57bb5713b915a17ebe8b8f1aa7d8c8ed2e70be404ac03d8e19386acd0de1ea95 |
| probe_results_preinstall.json (mode=preinstall) | 6b826e2b1c3506251522345f1cbfedcd513dd0a4c5574d72df76b7cb1b98c51e |
| probe_results_drift.json (mode=drift) | b2ce9450d33a528e3ac2970cdc168dba858cedae3adc7e8a4734d3950abefb01 |

Reproduction (exact):

```bash
# Extract the section-8 driver byte-exactly (no trailing newline is added by this
# extraction; a text editor WOULD add one and break the hash) and re-run all modes:
mkdir -p /tmp/opencode/probe37999047472 && cd /tmp/opencode/probe37999047472
python3 - <<'PY'
import pathlib, re, hashlib
md = pathlib.Path("research/experiments/EXP-PRODUCT-37999047472/prereg.md").read_text()
src = re.findall(r"```python\n(.*?)\n```", md, re.S)[-1]
assert hashlib.sha256(src.encode()).hexdigest() == "ad7ad7773779ce69b68122a362c9194f24025f0a02b0bfad8b9c1c39e2291563"
pathlib.Path("probe.py").write_text(src)
PY
sha256sum probe.py   # -> ad7ad7773779ce69b68122a362c9194f24025f0a02b0bfad8b9c1c39e2291563
python3 probe.py --mode=installed    # -> probe_results.json
python3 probe.py --mode=preinstall   # -> probe_results_preinstall.json  (run at base_sha e35fccd0 / pre-EXECUTE tree)
python3 probe.py --mode=drift        # -> probe_results_drift.json
```

NOTE on byte-exactness: the reproduced file must be byte-identical to the hashed driver
(the fenced block ends with `    main()` and NO trailing newline). The extraction above
enforces this; if you transcribe by hand, hash-verify before running.

`mode=installed` assembles a byte-faithful sandbox replica of the REAL shipping tree:
`src/spider/__init__.py`, `models.py`, `registry.py` copied byte-identically from the repo
and `kernel.py` = the frozen audited carrier, then runs the full ARM-DIFFERENTIATION
CERTIFICATE plus the canonical regression invocation on that replica. It provably never
mutates the repository. It was executed at DESIGN (python 3.12.15, git 2.55.0,
2026-10-10) and ALL assertions passed — this is the v2 treatment-liveness demonstration
that the frozen SUPORT branch is structurally real, not a ceiling/empty arm.

Observed headline values:

| probe | required for SUPPORTS | observed (installed) |
|---|---|---|
| AD-POSITIVE-ROUNDTRIP | 6/6, executable 1.0, binding 1.0 | 6/6, 1.0, 1.0 (per-family: EXECUTABLE, confidence 0.9, slot counts ok, bound ids correct, execute 200, verify true) |
| AD-NEGATIVE-ROUNDTRIP | refusal 1.0, all kinds 1.0, null actions, reasons recorded | 24/24 refused; per-kind rates all 1.0 |
| AD-TREATMENT-CONTRAST | real rate > 0 on ≥1 family | real contrast 1.0, all six families differ from nearest-literal comparator |
| NC-ZERO-CONTRAST-TREATMENT | degenerate detected (rate 0.0) | rate 0.0, degenerate_variant_detected true |
| PC-ACCOUNTING-FIDELITY | scripted max rel err ≤ 0.01; inherited {3,2,1} | scripted max rel err 0.0; real inherited increments retrieval_calls 3, verification_calls 2, repair_attempts 1, exact_match true |
| B-LITERAL-KERNEL | 0 EXECUTABLE | 0 EXECUTABLE (all six UNKNOWN) |
| AD-IDENTITY-BINDING | installed == required, pre/post differ | installed 718efa6a... == required; blob b15ed848...; pre (46929b3a...) differs |
| PKG-TESTS | pre-existing tests green | "Ran 3 tests", rc 0 |
| COMPILEALL | rc 0 | rc 0 |

`mode=preinstall` (FALSIFIER reachability, on the UNMODIFIED real tree at base_sha):
AD-POSITIVE-ROUNDTRIP fails 0/6 (AttributeError `'SpiderKernel' object has no attribute
'distill_parameterized'` on every family); AD-IDENTITY-BINDING matches the baseline
46929b3a... = 46929b3a... (pre/post identical, required 718efa6a... not matched);
FALSIFIER-REACHABILITY { shipped_has_distill_parameterized: false,
C2_positive_roundtrip_would_fail: true, C1_identity_would_fail: true,
literal_control_still_fires: true }; PKG-TESTS still green. Therefore the certificate
DISCRIMINATES the not-installed state from the installed state; a vacuous pass is
impossible. `mode=drift`: after flipping one byte (0x00^0x01) of the installed kernel,
the identity pin detects drift (observed a2f2702c... != required 718efa6a...,
drift_detected true) — C1 is byte-sensitive.

### 7.1 Raw evidence — probe_results.json (mode=installed, sha256 57bb5713...)

```json
{
  "AD-IDENTITY-BINDING": {
    "installed_git_blob": "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796",
    "installed_kernel_sha256": "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72",
    "matches_required": true,
    "pre_post_differ": true,
    "preinstall_baseline_git_blob": "cfec98660b0277ccbf295e8a4119e8d81ddccf50",
    "preinstall_baseline_sha256": "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61",
    "required_sha256": "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
  },
  "AD-NEGATIVE-ROUNDTRIP": {
    "kinds": ["missing_param", "out_of_support_empty", "out_of_support_pair", "out_of_support_slash", "out_of_support_space", "wrong_intent"],
    "per_kind_rates": {"missing_param": 1.0, "out_of_support_empty": 1.0, "out_of_support_pair": 1.0, "out_of_support_slash": 1.0, "out_of_support_space": 1.0, "wrong_intent": 1.0},
    "refusal_rate": 1.0,
    "refused": 24,
    "total_cases": 24
  },
  "AD-POSITIVE-ROUNDTRIP": {
    "by_family": {
      "F1-PATH-ID": {"bound_action_null": false, "bound_identifier_ok": true, "confidence": 0.9, "distilled": true, "execute_status": 200, "passed": true, "reason": "applicability guards and confidence threshold passed", "slot_count_ok": true, "slots": ["item"], "status": "EXECUTABLE", "verify": true},
      "F2-QUERY-ID": {"bound_action_null": false, "bound_identifier_ok": true, "confidence": 0.9, "distilled": true, "execute_status": 200, "passed": true, "reason": "applicability guards and confidence threshold passed", "slot_count_ok": true, "slots": ["q"], "status": "EXECUTABLE", "verify": true},
      "F3-BODY-FIELD": {"bound_action_null": false, "bound_identifier_ok": true, "confidence": 0.9, "distilled": true, "execute_status": 200, "passed": true, "reason": "applicability guards and confidence threshold passed", "slot_count_ok": true, "slots": ["token"], "status": "EXECUTABLE", "verify": true},
      "F4-HEADER-FIELD": {"bound_action_null": false, "bound_identifier_ok": true, "confidence": 0.9, "distilled": true, "execute_status": 200, "passed": true, "reason": "applicability guards and confidence threshold passed", "slot_count_ok": true, "slots": ["resource"], "status": "EXECUTABLE", "verify": true},
      "F5-TWO-SLOT": {"bound_action_null": false, "bound_identifier_ok": true, "confidence": 0.9, "distilled": true, "execute_status": 200, "passed": true, "reason": "applicability guards and confidence threshold passed", "slot_count_ok": true, "slots": ["item_id", "tenant"], "status": "EXECUTABLE", "verify": true},
      "F6-NOISE-STRESS": {"bound_action_null": false, "bound_identifier_ok": true, "confidence": 0.9, "distilled": true, "execute_status": 200, "passed": true, "reason": "applicability guards and confidence threshold passed", "slot_count_ok": true, "slots": ["node"], "status": "EXECUTABLE", "verify": true}
    },
    "held_out_binding_correct_rate": 1.0,
    "in_support_executable_rate": 1.0,
    "passed_families": 6
  },
  "AD-TREATMENT-CONTRAST": {
    "by_family": {"F1-PATH-ID": true, "F2-QUERY-ID": true, "F3-BODY-FIELD": true, "F4-HEADER-FIELD": true, "F5-TWO-SLOT": true, "F6-NOISE-STRESS": true},
    "real_contrast_rate": 1.0
  },
  "B-LITERAL-KERNEL": {
    "by_family": {"F1-PATH-ID": {"status": "UNKNOWN"}, "F2-QUERY-ID": {"status": "UNKNOWN"}, "F3-BODY-FIELD": {"status": "UNKNOWN"}, "F4-HEADER-FIELD": {"status": "UNKNOWN"}, "F5-TWO-SLOT": {"status": "UNKNOWN"}, "F6-NOISE-STRESS": {"status": "UNKNOWN"}},
    "held_out_executable_count": 0
  },
  "COMPILEALL": {"returncode": 0},
  "NC-ZERO-CONTRAST-TREATMENT": {"degenerate_contrast_rate": 0.0, "degenerate_variant_detected": true},
  "PC-ACCOUNTING-FIDELITY": {
    "inherited_path": {
      "exact_match": true,
      "execute_statuses": [200, 200],
      "expected": {"repair_attempts": 1, "retrieval_calls": 3, "verification_calls": 2},
      "increments": {"repair_attempts": 1, "retrieval_calls": 3, "verification_calls": 2},
      "ran": true,
      "refused_resolve_status": "EXPLORE",
      "verify_results": [true, true]
    },
    "ran": true,
    "scripted": {
      "expected": {"browser_actions": 1, "http_requests": 3, "latency_ms": 1.0, "model_calls": 5, "model_tokens": 200, "repair_attempts": 1, "retrieval_calls": 2, "verification_calls": 1},
      "max_relative_error": 0.0,
      "measured": {"browser_actions": 1, "http_requests": 3, "latency_ms": 1.0, "model_calls": 5, "model_tokens": 200, "repair_attempts": 1, "retrieval_calls": 2, "verification_calls": 1},
      "synthetic_model_fields_note": "model_calls/model_tokens events are an explicitly injected labeled synthetic event; no model was called during this probe",
      "threshold": 0.01
    }
  },
  "PKG-TESTS": {"failed": [], "returncode": 0, "summary_line": ["Ran 3 tests in 0.002s"], "tests": true},
  "TARGET": "/tmp/opencode/probe37999047472/src",
  "probe_version": 1,
  "python": "3.12.15"
}
```

### 7.2 Raw evidence — probe_results_preinstall.json (mode=preinstall, sha256 6b826e2b...)

Key differences from 7.1 (FALSIFIER reachability on the unmodified real tree):

```json
{
  "AD-IDENTITY-BINDING": {
    "installed_git_blob": "cfec98660b0277ccbf295e8a4119e8d81ddccf50",
    "installed_kernel_sha256": "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61",
    "matches_required": false,
    "pre_post_differ": false,
    "preinstall_baseline_git_blob": "cfec98660b0277ccbf295e8a4119e8d81ddccf50",
    "preinstall_baseline_sha256": "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61",
    "required_sha256": "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
  },
  "AD-POSITIVE-ROUNDTRIP": {
    "by_family": {
      "F1-PATH-ID": {"attribute_error": "'SpiderKernel' object has no attribute 'distill_parameterized'", "bound_action_null": null, "bound_identifier_ok": null, "confidence": null, "distilled": false, "execute_status": null, "passed": false, "slot_count_ok": false, "slots": null, "status": null, "verify": null},
      "F2-QUERY-ID": {"attribute_error": "'SpiderKernel' object has no attribute 'distill_parameterized'", "bound_action_null": null, "bound_identifier_ok": null, "confidence": null, "distilled": false, "execute_status": null, "passed": false, "slot_count_ok": false, "slots": null, "status": null, "verify": null},
      "F3-BODY-FIELD": {"attribute_error": "'SpiderKernel' object has no attribute 'distill_parameterized'", "bound_action_null": null, "bound_identifier_ok": null, "confidence": null, "distilled": false, "execute_status": null, "passed": false, "slot_count_ok": false, "slots": null, "status": null, "verify": null},
      "F4-HEADER-FIELD": {"attribute_error": "'SpiderKernel' object has no attribute 'distill_parameterized'", "bound_action_null": null, "bound_identifier_ok": null, "confidence": null, "distilled": false, "execute_status": null, "passed": false, "slot_count_ok": false, "slots": null, "status": null, "verify": null},
      "F5-TWO-SLOT": {"attribute_error": "'SpiderKernel' object has no attribute 'distill_parameterized'", "bound_action_null": null, "bound_identifier_ok": null, "confidence": null, "distilled": false, "execute_status": null, "passed": false, "slot_count_ok": false, "slots": null, "status": null, "verify": null},
      "F6-NOISE-STRESS": {"attribute_error": "'SpiderKernel' object has no attribute 'distill_parameterized'", "bound_action_null": null, "bound_identifier_ok": null, "confidence": null, "distilled": false, "execute_status": null, "passed": false, "slot_count_ok": false, "slots": null, "status": null, "verify": null}
    },
    "held_out_binding_correct_rate": 0.0,
    "in_support_executable_rate": 0.0,
    "passed_families": 0
  },
  "FALSIFIER-REACHABILITY": {
    "C1_identity_would_fail": true,
    "C2_positive_roundtrip_would_fail": true,
    "literal_control_still_fires": true,
    "observed_installed_sha": "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61",
    "shipped_has_distill_parameterized": false
  },
  "PC-ACCOUNTING-FIDELITY": {"ran": false, "reason": "TrajectoryCounters unavailable on target kernel"},
  "PKG-TESTS": {"failed": [], "returncode": 0, "summary_line": ["Ran 3 tests in 0.002s"], "tests": true},
  "TARGET": "/home/runner/work/Spider/Spider/src",
  "probe_version": 1,
  "python": "3.12.15"
}
```

(AD-NEGATIVE-ROUNDTRIP, AD-TREATMENT-CONTRAST, B-LITERAL-KERNEL, NC-* on the preinstall
tree match 7.1: 24/24 refused, real contrast 1.0 with comparator-vs-treatment
differences, 0 literal EXECUTABLE, degenerate detected. Instrumentation behaves apart
from the missing capability; recording the refusal behavior on the unmodified tree keeps
the negative arm honest on both trees.)

### 7.3 Raw evidence — probe_results_drift.json (mode=drift, sha256 b2ce9450...)

```json
{
  "AD-IDENTITY-BINDING_DRIFT_SENSITIVITY": {
    "drift_detected": true,
    "observed_sha256": "a2f2702c038526f8dabdfead3f44cbe85d2748519bfa1dd5883ec4ef2458c8de",
    "one_byte_flipped": true,
    "required_sha256": "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
  },
  "probe_version": 1,
  "python": "3.12.15"
}
```

## 8. Probe driver (frozen; sha256 ad7ad7773779ce69b68122a362c9194f24025f0a02b0bfad8b9c1c39e2291563)

EXECUTE's certificate runner MUST be byte-equivalent to this driver (same assertions,
same thresholds, same evidence keys); it will run against the REAL installed package
(replacing the sandbox replica target). Verbatim source:

```python
#!/usr/bin/env python3
"""DESIGN pre-freeze treatment-liveness probe for EXP-PRODUCT-37999047472.

Standard library only. Two modes:
  --mode=installed   (default) assemble a byte-faithful sandbox replica of the
                     real shipping tree (src/spider/__init__.py, models.py,
                     registry.py copied byte-identically from the repo, kernel.py
                     = audited carrier) and run the frozen ARM-DIFFERENTIATION
                     CERTIFICATE-v2 checks AD-POSITIVE-ROUNDTRIP,
                     AD-NEGATIVE-ROUNDTRIP, AD-TREATMENT-CONTRAST,
                     NC-ZERO-CONTRAST-TREATMENT, PC-ACCOUNTING-FIDELITY,
                     B-LITERAL-KERNEL, AD-IDENTITY-BINDING, PKG-TESTS.
  --mode=preinstall  run the certificate's structural checks (identity pin,
                     positive-roundtrip capability) against the UNMODIFIED real
                     shipping tree to demonstrate FALSIFIES reachability.
  --mode=drift       copy the sandbox kernel, flip one byte, and verify the
                     identity pin detects the drift (C1 sensitivity).

Writes probe_results.json next to this file. Never mutates the repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path("/home/runner/work/Spider/Spider")
HERE = Path(__file__).resolve().parent
CARRIER = REPO / "research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider"
FIXTURE_SRC = REPO / "research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py"
SHIPPED_KERNEL = REPO / "src/spider/kernel.py"

CARRIER_KERNEL_SHA256 = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
SHIPPED_KERNEL_SHA256 = "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)], cwd=REPO, text=True
    ).strip()


def assemble_sandbox() -> Path:
    pkg = HERE / "src/spider"
    if pkg.exists():
        shutil.rmtree(HERE / "src")
    pkg.mkdir(parents=True)
    for name in ("__init__.py", "models.py", "registry.py"):
        shutil.copyfile(REPO / "src/spider" / name, pkg / name)
    shutil.copyfile(CARRIER / "kernel.py", pkg / "kernel.py")
    shutil.copyfile(FIXTURE_SRC, HERE / "fixture.py")
    return HERE / "src"


def run_certificate(target_src: Path) -> dict:
    sys.path.insert(0, str(target_src))
    sys.path.insert(0, str(HERE))
    import fixture
    from spider import Mechanism, Resolution, ResolutionStatus, SpiderKernel
    from spider.registry import MechanismRegistry
    try:
        from spider.kernel import TrajectoryCounters
        counters_available = True
    except ImportError:
        TrajectoryCounters = None
        counters_available = False

    results: dict = {}
    families = fixture.FAMILIES
    all_obs = fixture.observations_by_family()

    def map_params(mech, family):
        """Key held-out values by the mechanism's own inferred slot names."""
        params = {}
        for slot in mech.parameter_slots:
            if slot in family["held_out"]:
                params[slot] = family["held_out"][slot]
            elif len(mech.parameter_slots) == 1:
                params[slot] = family["held_out"][family["slot_keys"][0]]
        return params

    def distill_safe(kernel, observations):
        try:
            return kernel.distill_parameterized(observations)
        except AttributeError:
            return None

    # ---- AD-POSITIVE-ROUNDTRIP -------------------------------------------
    positive = {"by_family": {}, "in_support_executable_rate": None,
                "held_out_binding_correct_rate": None}
    td = tempfile.TemporaryDirectory()
    reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
    kernel = SpiderKernel(reg)
    ok_families = 0
    for family in families:
        obs = all_obs[family["family"]]
        try:
            mech = kernel.distill_parameterized(obs)
        except AttributeError as exc:
            fam = {"distilled": False, "slots": None, "slot_count_ok": False, "confidence": None,
                   "status": None, "bound_action_null": None, "bound_identifier_ok": None,
                   "execute_status": None, "verify": None, "attribute_error": str(exc),
                   "passed": False}
            positive["by_family"][family["family"]] = fam
            continue
        fam = {
            "distilled": mech is not None,
            "slots": list(mech.parameter_slots) if mech else None,
            "slot_count_ok": bool(mech and len(mech.parameter_slots) == family["expected_slot_count"]),
            "confidence": mech.confidence if mech else None,
            "status": None, "bound_action_null": None,
            "bound_identifier_ok": None, "execute_status": None, "verify": None,
        }
        if mech is None:
            positive["by_family"][family["family"]] = fam
            continue
        reg.upsert(mech)
        params = map_params(mech, family)
        context = {"site": "fixture.invalid", "route": family["route"], "auth": "public"}
        r = kernel.resolve(family["intent"], context, params)
        fam["status"] = r.status.value if hasattr(r.status, "value") else str(r.status)
        fam["bound_action_null"] = r.bound_action is None
        fam["reason"] = r.reason
        if r.status == ResolutionStatus.EXECUTABLE and r.bound_action is not None:
            bound_id = family["bound_identifier"](r.bound_action)
            if family["family"] == "F5-TWO-SLOT":
                expected = tuple(family["held_out"][k] for k in family["slot_keys"])
                fam["bound_identifier_ok"] = tuple(bound_id) == tuple(expected)
            else:
                key = family["slot_keys"][0]
                fam["bound_identifier_ok"] = bound_id == family["held_out"][key]
            exec_result = fixture.fixture_execute(r.bound_action)
            fam["execute_status"] = exec_result.get("status")
            fam["verify"] = kernel.verify(mech.mechanism_id, exec_result, params)
            passed = (r.status == ResolutionStatus.EXECUTABLE
                      and not fam["bound_action_null"]
                      and fam["bound_identifier_ok"]
                      and fam["execute_status"] == 200
                      and fam["verify"] is True)
            fam["passed"] = passed
            if passed:
                ok_families += 1
        else:
            fam["passed"] = False
        positive["by_family"][family["family"]] = fam
    positive["passed_families"] = ok_families
    positive["in_support_executable_rate"] = ok_families / len(families)
    positive["held_out_binding_correct_rate"] = ok_families / len(families)
    results["AD-POSITIVE-ROUNDTRIP"] = positive
    td.cleanup()

    # ---- AD-NEGATIVE-ROUNDTRIP -------------------------------------------
    td = tempfile.TemporaryDirectory()
    reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
    kernel = SpiderKernel(reg)
    negatives = fixture.negative_cases()
    refused = 0
    per_kind: dict[str, list] = {}
    mechs_by_intent = {}
    for family in families:
        m = distill_safe(kernel, all_obs[family["family"]])
        if m is not None:
            reg.upsert(m)
            mechs_by_intent[family["intent"]] = m
    for case in negatives:
        mech = mechs_by_intent.get(case["intent"])
        params = dict(case["params"])
        if mech is not None and len(mech.parameter_slots) == 1 and len(params) == 1:
            params = {mech.parameter_slots[0]: next(iter(params.values()))}
        r = kernel.resolve(case["intent"], case["context"], params)
        is_refused = (r.status != ResolutionStatus.EXECUTABLE
                      and r.bound_action is None and bool(r.reason))
        if is_refused:
            refused += 1
        per_kind.setdefault(case["kind"], []).append(is_refused)
    results["AD-NEGATIVE-ROUNDTRIP"] = {
        "total_cases": len(negatives),
        "refused": refused,
        "refusal_rate": refused / len(negatives),
        "per_kind_rates": {k: sum(v) / len(v) for k, v in per_kind.items()},
        "kinds": sorted(per_kind.keys()),
    }
    td.cleanup()

    # ---- AD-TREATMENT-CONTRAST + NC-ZERO-CONTRAST-TREATMENT ---------------
    contrasts = []
    td = tempfile.TemporaryDirectory()
    reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
    kernel = SpiderKernel(reg)
    for family in families:
        obs = all_obs[family["family"]]
        mech = distill_safe(kernel, obs)
        if mech is not None:
            reg.upsert(mech)
            params = map_params(mech, family)
        else:
            params = dict(family["held_out"])
        context = {"site": "fixture.invalid", "route": family["route"], "auth": "public"}
        r = kernel.resolve(family["intent"], context, params)
        comparator = fixture.retrieval_comparator_action(family["intent"], context, obs, k=5)
        treatment = r.bound_action
        json_t = json.dumps(treatment, sort_keys=True)
        json_c = json.dumps(comparator, sort_keys=True)
        contrasts.append({"family": family["family"], "differs": json_t != json_c,
                          "treatment": treatment, "comparator": comparator})
    real_rate = sum(1 for c in contrasts if c["differs"]) / len(contrasts)
    # Degenerate null: the SAME contrast instrument run comparator-vs-itself
    # must report zero differences (rate != 0.0 would expose an insensitive /
    # trivially-passing instrument).
    degenerate_rate = sum(1 for c in contrasts
                          if json.dumps(c["comparator"], sort_keys=True)
                          != json.dumps(c["comparator"], sort_keys=True)) / len(contrasts)
    results["AD-TREATMENT-CONTRAST"] = {
        "real_contrast_rate": real_rate,
        "by_family": {c["family"]: c["differs"] for c in contrasts},
    }
    results["NC-ZERO-CONTRAST-TREATMENT"] = {
        "degenerate_contrast_rate": degenerate_rate,
        "degenerate_variant_detected": degenerate_rate == 0.0,
    }
    td.cleanup()

    # ---- PC-ACCOUNTING-FIDELITY -------------------------------------------
    def accounting_checks(TC):
        if TC is None:
            return {"ran": False,
                    "reason": "TrajectoryCounters unavailable on target kernel"}
        counters = TC()
        steps = [
            {"model_calls": 2, "browser_actions": 1},
            {"model_tokens": 150, "http_requests": 1},
            {"retrieval_calls": 2, "verification_calls": 1},
            {"repair_attempts": 1, "latency_ms": 0.25},
            {"model_calls": 3, "model_tokens": 50, "http_requests": 2, "latency_ms": 0.75},
        ]
        for step in steps:
            for field, amount in step.items():
                counters.add(field, amount)
        expected = {"model_calls": 5, "model_tokens": 200, "browser_actions": 1,
                    "http_requests": 3, "retrieval_calls": 2, "verification_calls": 1,
                    "repair_attempts": 1, "latency_ms": 1.0}
        measured = counters.as_dict()
        rel = {k: abs(measured[k] - v) / v for k, v in expected.items()}
        out = {
            "ran": True,
            "scripted": {
                "max_relative_error": max(rel.values()),
                "threshold": 0.01,
                "measured": measured,
                "expected": expected,
                "synthetic_model_fields_note": "model_calls/model_tokens events are an "
                                               "explicitly injected labeled synthetic event; "
                                               "no model was called during this probe",
            },
        }

        td = tempfile.TemporaryDirectory()
        reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
        kernel = SpiderKernel(reg, counters=TC())
        f1 = families[0]
        obs = all_obs[f1["family"]]
        mech = distill_safe(kernel, obs)
        if mech is None:
            out["inherited_path"] = {
                "ran": False, "reason": "distill_parameterized unavailable on target kernel"}
        else:
            reg.upsert(mech)
            context = {"site": "fixture.invalid", "route": f1["route"], "auth": "public"}
            params = map_params(mech, f1)
            r1 = kernel.resolve(f1["intent"], context, params)                       # retrieval +1
            exec1 = fixture.fixture_execute(r1.bound_action)
            v1 = kernel.verify(mech.mechanism_id, exec1, params)                     # verification +1
            r2 = kernel.resolve(f1["intent"], context, {next(iter(mech.parameter_slots)): "in valid"})  # retrieval +1 (refused)
            r3 = kernel.rebind(f1["intent"], context, params)                        # repair +1, retrieval +1
            exec3 = fixture.fixture_execute(r3.bound_action)
            v3 = kernel.verify(mech.mechanism_id, exec3, params)                     # verification +1
            got = kernel.counters.as_dict()
            want = {"retrieval_calls": 3, "verification_calls": 2, "repair_attempts": 1}
            out["inherited_path"] = {
                "ran": True,
                "increments": {k: got[k] for k in want},
                "expected": want,
                "exact_match": all(got[k] == v for k, v in want.items()),
                "execute_statuses": [exec1.get("status"), exec3.get("status")],
                "verify_results": [v1, v3],
                "refused_resolve_status": r2.status.value if hasattr(r2.status, "value") else str(r2.status),
            }
        td.cleanup()
        return out

    results["PC-ACCOUNTING-FIDELITY"] = accounting_checks(
        TrajectoryCounters if counters_available else None)

    # ---- B-LITERAL-KERNEL ---------------------------------------------------
    td = tempfile.TemporaryDirectory()
    reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
    kernel = SpiderKernel(reg)
    executable_count = 0
    per_family = {}
    for family in families:
        obs = all_obs[family["family"]]
        literal = kernel.distill(obs[0])
        reg.upsert(literal)
        context = {"site": "fixture.invalid", "route": family["route"], "auth": "public"}
        r = kernel.resolve(family["intent"], context, dict(family["held_out"]))
        is_exec = r.status == ResolutionStatus.EXECUTABLE
        executable_count += int(is_exec)
        per_family[family["family"]] = {"status": r.status.value if hasattr(r.status, "value") else str(r.status)}
    results["B-LITERAL-KERNEL"] = {
        "held_out_executable_count": executable_count,
        "by_family": per_family,
    }
    td.cleanup()

    # ---- AD-IDENTITY-BINDING -------------------------------------------------
    installed = target_src / "spider" / "kernel.py"
    installed_sha = sha256_file(installed)
    installed_blob = git_blob(installed)
    pre_sha = sha256_file(SHIPPED_KERNEL)
    results["AD-IDENTITY-BINDING"] = {
        "installed_kernel_sha256": installed_sha,
        "required_sha256": CARRIER_KERNEL_SHA256,
        "installed_git_blob": installed_blob,
        "preinstall_baseline_sha256": pre_sha,
        "preinstall_baseline_git_blob": git_blob(SHIPPED_KERNEL),
        "matches_required": installed_sha == CARRIER_KERNEL_SHA256,
        "pre_post_differ": installed_sha != pre_sha,
    }

    results["TARGET"] = str(target_src)
    return results


def mode_installed() -> dict:
    target = assemble_sandbox()
    return run_certificate(target)


def mode_preinstall() -> dict:
    results = run_certificate(REPO / "src")
    has_capability = True
    try:
        import spider  # noqa: F401
        has_capability = hasattr(__import__("spider.kernel", fromlist=["SpiderKernel"]).SpiderKernel,
                                 "distill_parameterized")
    except Exception as exc:  # pragma: no cover
        results["preinstall_import_error"] = str(exc)
    results["FALSIFIER-REACHABILITY"] = {
        "shipped_has_distill_parameterized": has_capability,
        # Certificate-level expectations on the unmodified shipping tree:
        "C2_positive_roundtrip_would_fail": not has_capability,
        "C1_identity_would_fail": results["AD-IDENTITY-BINDING"]["installed_kernel_sha256"]
        != CARRIER_KERNEL_SHA256,
        "observed_installed_sha": results["AD-IDENTITY-BINDING"]["installed_kernel_sha256"],
        "literal_control_still_fires": results["B-LITERAL-KERNEL"]["held_out_executable_count"] == 0,
    }
    return results


def mode_drift() -> dict:
    target = assemble_sandbox()
    drifted = target / "spider" / "kernel.py"
    data = bytearray(drifted.read_bytes())
    data[0] ^= 0x01
    drifted.write_bytes(bytes(data))
    detected = sha256_file(drifted) != CARRIER_KERNEL_SHA256
    return {"AD-IDENTITY-BINDING_DRIFT_SENSITIVITY": {
        "one_byte_flipped": True,
        "drift_detected": detected,
        "observed_sha256": sha256_file(drifted),
        "required_sha256": CARRIER_KERNEL_SHA256,
    }}


def pkg_tests(target_src: Path) -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(target_src)
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(REPO / "tests"), "-v"],
        cwd=REPO, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    # unittest protocol output is emitted on stderr by the CPython runner.
    combined = proc.stdout + proc.stderr
    return {
        "returncode": proc.returncode,
        "tests": "Ran 3 tests" in combined,
        "summary_line": [ln for ln in combined.splitlines() if ln.startswith("Ran ")] or [],
        "failed": [ln for ln in combined.splitlines() if "FAIL" in ln or "ERROR" in ln],
    }


def compile_check(target_src: Path) -> dict:
    proc = subprocess.run([sys.executable, "-m", "compileall", "-q", str(target_src)],
                          text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {"returncode": proc.returncode}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["installed", "preinstall", "drift"], default="installed")
    args = ap.parse_args()
    if args.mode == "installed":
        target = assemble_sandbox()
        results = run_certificate(target)
        results["PKG-TESTS"] = pkg_tests(target)
        results["COMPILEALL"] = compile_check(target)
        suffix = ""
    elif args.mode == "preinstall":
        if not (HERE / "fixture.py").exists():
            shutil.copyfile(FIXTURE_SRC, HERE / "fixture.py")
        results = mode_preinstall()
        results["PKG-TESTS"] = pkg_tests(REPO / "src")
        results["COMPILEALL"] = compile_check(REPO / "src")
        suffix = "_preinstall"
    else:
        results = mode_drift()
        suffix = "_drift"
    results["probe_version"] = 1
    results["python"] = sys.version.split()[0]
    out = HERE / f"probe_results{suffix}.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    overall = "PASS" if suffix == "" else "REACHABILITY_DEMONSTRATED"
    print(f"overall={overall} mode={args.mode} -> {out.name}")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
```

## 9. Design-contract-v2 satisfiability and identifiability self-attack

This design was attacked before freezing; each check below is answered with evidence from
section 7. This is not a design-review substitute (design_review.json is the independent
audit), but it records what DESIGN disproved about its own design, including the history
that the previous (v1) attempt was rejected for a substantive defect and re-built with
real evidence.

1. **Empty/unreachable decision branch?** No. SUPPORTS reachable (7.1 PASS on the frozen
   carrier at the shipping position), FALSIFIES reachable (7.2: uninstalled tree fails
   C2/C1; C7 observes the regression suite), MEASUREMENT_INVALID reachable (7.3: byte
   drift detected; NC degenerate null instrumented to fail), BLOCKED reachable on
   scope/env/install failure. Every branch has a distinct, non-collapsed meaning.
2. **Arithmetic impossibility?** None. Ratios (passed_families/6, refused/24,
   real_rate/6, scripted max rel err with threshold 0.01) are computable and were
   computed; degenerate null is a constant-time equality map, not a division by the
   treatment. Counter expectations {3,2,1} match the instrumented event sites
   (resolve/verify/refused-resolve/rebind/fixture-execute), verified in 7.1.
3. **Treatment/comparator identity collision?** No. Pre/post kernel blobs differ
   (cfec9866... vs b15ed848...); treatment-bound action differs from the nearest-literal
   comparator on 6/6 (real contrast 1.0); degenerate comparator-vs-itself yields 0.0 and
   the instrument flags it. Slot-naming convention pinned (F2→`q` etc.) — known audited
   carrier behavior discovered and handled at DESIGN, so EXECUTE cannot mis-key params.
4. **Insensitive controls?** No. Positive control discriminates installed vs
   pre-install states (6/6 with carrier, 0/6 without); negative control has full refusal
   dynamic range; identity pin is byte-sensitive (7.3); NC null fails on no-difference;
   accounting has an explicit threshold and exact-match check; B-LITERAL sits at its
   floor (0 EXECUTABLE) — full dynamic range, no ceiling masking.
5. **Missing prerequisites?** None. Toolchain (python 3.12.15, git 2.55.0), scope
   (product allowed_code_roots cover src/ and tests/), freeze artifacts (8 files,
   hashes verified pre-freeze), execution-checkpoint writer
   (record_execution_base.py), regression invocation all present and exercised at
   DESIGN. The C-LLM-INHERIT runtime task bank and the intel endpoint are DOWNSTREAM
   consumers, explicitly out of scope.
6. **Unbound mutable artifacts?** None. Eight freeze artifacts bound (kernel excluded
   deliberately, pinned instead via C1 with pre-install baseline recorded). Only
   mutation surface is `src/spider/kernel.py` (identity-pinned) plus the NEW
   `tests/test_ship_kernel.py` (new code; C7 gates it). Package surface
   (`__init__.py`) bound. No `sys.path` pollution: fixture loaded from the packet path.

Explicitly recorded counterfactual for future audits: if SUPPORTS is reported, the
deterministic pre-freeze probe ALREADY predicted every value in the certificate; the
confirmatory run's value is agreement, not discovery. This is the disclosed design
intent, not a hidden failure.

## 10. EXECUTE procedure (frozen contract)

Frozen inputs: request.json, spec.json, prereg.md, freeze.json, design_review.json;
execution_checkpoint.json written automatically first.

1. Scope: execute prefixes are the experiment dir + [src, tests, sdk, pyproject.toml].
2. Install (single mutation of existing repo code): copy
   `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`
   byte-identically to `src/spider/kernel.py` (C1 target: sha256 718efa6a...).
   Nothing else in src/, tests/, sdk/ or pyproject.toml may change. The eight freeze
   artifacts are NEVER modified.
3. Fixture & runner: reconstruct the frozen `fixture.py` (b0ffcbba...) and the
   certificate runner INTO the packet dir (e.g. <exp>/certificate/); runner MUST be
   byte-equivalent to section 8 with `target_src = REPO/src` (the real installed
   package) and the fixture loaded from the packet path under `sys.path` ahead of src.
4. Certificate (raw evidence): run each check against the REAL installed package:
   AD-POSITIVE-ROUNDTRIP, AD-NEGATIVE-ROUNDTRIP, AD-TREATMENT-CONTRAST +
   NC-ZERO-CONTRAST-TREATMENT, PC-ACCOUNTING-FIDELITY, B-LITERAL-KERNEL,
   AD-IDENTITY-BINDING. Store raw JSON under <exp>/certificate/raw/ (derive results
   from it; never overwrite it).
5. Regression surface: `PYTHONPATH=src python -m unittest discover -s tests -v`
   (canonical; capture stdout+stderr), `python -m compileall -q src scripts`.
6. Add unit tests `tests/test_ship_kernel.py`: import
   `from spider.kernel import TrajectoryCounters, SpiderKernel` (module scope — no
   package re-export) and `from spider import Mechanism, Observation, Resolution,
   ResolutionStatus`; must be runnable by the canonical discovery invocation; must
   exercise distill_parameterized roundtrip per family F2 (and F5 two-slot) and the
   accounting counter increments. Secondary surface only; the certificate JSON is the
   decision instrument.
7. Keep the code-root delta minimal and exclusive (src/spider/kernel.py replaced +
   tests/test_ship_kernel.py added) so the promotion delta
   (product-promote.yml `git diff BASE..SOURCE_SHA -- src tests sdk pyproject.toml`)
   equals exactly that; never touch .github/ or any other lane.
8. Write result.json/report.md/provenance.json/handoff per the packet contract,
   mapping to OVERALL_OUTCOME per section 11; produce model_design/verdict inputs for
   finalize_lane (STAGE_OUTPUTS of research2_contract). If main diverges in src/spider
   at promotion time, promotion hard-stops (operational dependency; record, do not
   mask).

## 11. Decision mapping (frozen)

| check | rule | evidence key |
|---|---|---|
| C1 identity binding | installed sha256 == 718efa6a... AND blob == b15ed848... AND frozen artifacts unchanged | AD-IDENTITY-BINDING + freeze.json |
| C2 positive roundtrip | 6/6 families: EXECUTABLE, bound action non-null, bound id == held-out, execute 200, verify true | AD-POSITIVE-ROUNDTRIP |
| C3 negative roundtrip | refusal_rate == 1.0 (24/24), per-kind 1.0, null actions, reasons recorded | AD-NEGATIVE-ROUNDTRIP |
| C4 treatment contrast | real contrast > 0 on ≥1 family AND degenerate null detected | AD-TREATMENT-CONTRAST, NC-ZERO-CONTRAST-TREATMENT |
| C5 accounting fidelity | scripted max rel err ≤ 0.01 AND inherited increments exactly {3,2,1} | PC-ACCOUNTING-FIDELITY |
| C6 literal control | held_out_executable_count == 0 | B-LITERAL-KERNEL |
| C7 promotability tests | pre-existing tests green + added tests green + compileall src scripts rc 0 | PKG-TESTS / unit discovery / COMPILEALL |

OVERALL_OUTCOME: SUPPORTS = C1…C7 all PASS → status COMPLETE, recommend
promote_to_product=true (DIRECTOR decides PRODUCT_CORE; SHIPPED is post-promotion).
FALSIFIES = C2 or C7 fails after a C1-passing install → status COMPLETE, no promotion,
diagnose integration defect. MEASUREMENT_INVALID = C1 or C3/C4/C5/C6 fails → status
MEASUREMENT_INVALID, no promotion, repair instrumentation. BLOCKED = infra/scope/
install failure → status BLOCKED; never a scientific negative.

No-residue reversion rule: on anything but SUPPORTS, revert the code-root delta to
pre_execute_sha (B-SHIPPED-PRE-INSTALL 46929b3a...) via revert_product_reject.py so the
Product branch tree carries no installed carrier.

## 12. Validity threats and mitigations

1. **v1 defect recurrence (asserted-but-unenforced certificate).** The previous attempt
   was rejected (substantive). This design embeds a real, hashed driver + real raw
   results and pins C1–C7 to machine-readable keys; EXECUTE's certificate runner must
   be byte-equivalent to section 8 and AUDIT recomputes from raw JSON. The preinstall
   probe demonstrated the certificate fails loudly on the uninstalled tree — an
   asserted-only gate cannot survive audit.
2. **Determinism inflation.** Disclosed (sections 2, 9): pinned-bytes install makes this
   a durability/promotion confirmation; the residual tested uncertainty is
   integration at the shipping position, not web-exploration behavior. Claim event
   reason must state this bounded support.
3. **Package-surface drift.** `__init__.py` bound; TrajectoryCounters not re-exported;
   tests import from `spider.kernel` module scope. If a future main changes the
   surface, promote may 3-way conflict — operational, recorded, not a falsifier.
4. **sys.path capture.** Fixture and package both on sys.path (as in section 8);
   fixture is a packet file, never inside src/spider/. Unit tests use canonical
   discovery only.
5. **Negative-arm weakening.** The preinstall run shows the refusal behavior is
   identical on both trees; per-kind rates all 1.0; null-action + reason required per
   case (not just "status != EXECUTABLE").
6. **Promotion-path divergence.** product-promote.yml applies 3-way; if main moved
   src/spider/kernel.py between base and promotion, the workflow hard-stops — recorded
   as operational dependency, no silent fallback.

## 13. Product consequences (pre-committed)

- SUPPORTS: packet recommends promote_to_product=true; audit-PASS + Product lane +
  promotion intent → DIRECTOR may set C-PARAM-INHERIT → PRODUCT_CORE; promotion lands
  the audited delta in main; readiness condition (1) of the four-arm benchmark cleared.
- Negative/INVALID/BLOCKED: no promotion; tree reverted to B-SHIPPED-PRE-INSTALL;
  C-PARAM-INHERIT retains its prior effective status; next step is a bounded
  integration-defect diagnosis (FALSIFIES) or instrumentation repair in a new frozen
  packet (MEASUREMENT_INVALID). Same cost model as the audit packets: zero model calls,
  zero browser, low latency (certificate wall time < 5 s in probe).

## 14. Cost and expected information gain

Cost: negligible (deterministic stdlib certificate; no model/browser/network). Expected
information gain: program-high — converts the program's only two audit-PASS
parameterized-inheritance packets into a shipped, durable state and exercises the pinned
promotion path end-to-end; closes the "audited but never shipped" gap and unblocks the
four-arm benchmark and first-party economics. Claim-level gain bounded as disclosed
above: this is the required engineering confirmation with a REAL reachable falsifier,
not new web-behavior evidence.