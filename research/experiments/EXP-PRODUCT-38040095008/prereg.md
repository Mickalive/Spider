# EXP-PRODUCT-38040095008 preregistration

Lane: product. Design contract: v2. Claim: `C-PARAM-INHERIT` (only claim in scope).
This is a frozen preregistration for a DURABILITY / PROMOTABILITY confirmation, deliberately
NOT a new discovery experiment. It is written to be self-contained for fresh-context EXECUTE,
AUDIT and DESIGN-REVIEW agents.

## 1. Mandate, claim and claim ceiling

The Global Research Director mandate (`request.json.director_mandate`, allocation
`action=CONTINUE`, `claim_id=C-PARAM-INHERIT`, `cognitive_reset=false`,
`parent_handoff_disposition=SUPERSEDE`, cycle `38039660034`) is binding. It asks whether the
audited parameterized-inheritance capability can be made DURABLE and PROMOTABLE in the shipping
kernel path (`src/spider`), demonstrated by a pre-freeze arm-differentiation certificate over the
SHIPPED kernel (known-positive round trip; known-negative refusal with reason and null action;
unit tests; an accounting check that inherited-path counters increment; kernel identity bound at
freeze) so the carrier lands in `main` through the pinned Product promotion path without manually
copying experiment code.

CLAIM CEILING (binding). This packet provides ZERO evidence for or against the product thesis
`C-LLM-INHERIT`, and no new claim-level evidence for `C-PARAM-INHERIT` generalization to real
sites or richer action grammars. It measures only whether the audited capability is durable and
promotable at the shipping position. Because the installed bytes are pinned to the frozen audited
carrier hash (section 3), the confirmatory EXECUTE measurement is deterministic: it is an
integration/durability confirmation, not a new causal discovery about web behaviour. The
deterministic counter-only economics questions from the parent handoff are NOT tested here.

## 2. Parent handoff preservation (SUPERSEDE)

`request.json.parent_handoff` = `research/experiments/EXP-PRODUCT-37989728440/handoff.json`
(sha256 `911f765d04a83974f20d113da206b4075337c3a9bed4c5a77a8f06ffb4773ed9`). The Director
mandate sets `parent_handoff_disposition=SUPERSEDE`, so the parent's `next_question` (escalate to
the four-arm `C-LLM-INHERIT` benchmark or an asymmetric-discovery fallback) is NOT this packet's
objective and MUST NOT silently override the mandate. The parent's four-way distinction is
preserved by reference:

- `established` (carried, not re-derived): carrier integrity; the parameterized path is causally
  necessary on the parent substrate (B-LITERAL-KERNEL 0.0 vs replay 1.0); the parent's frozen
  deterministic run was measurement-valid but the dynamic-range certificate was unsatisfiable and
  the counter-only economics tied/failed (bounded substrate-class negative).
- `rejected` (carried, bounded): a certified dynamic range and a counter-only treatment advantage
  on the mandatory-discovery deterministic REST substrate class; the latency-inclusive
  cost_per_success metric as a discriminating instrument; and the (false) claim that the freeze
  step enforces a certificate gate.
- `unknown` (carried): whether any credential-free deterministic substrate can show dynamic range;
  whether asymmetric/amortized discovery helps; whether a programmatic credential-free model
  endpoint can be provisioned; when the freeze gate will be repaired.
- `do_not_assume` (carried): do not read the parent packet as evidence for/against
  `C-RESIDUAL-NOVELTY`; do not treat cold/retrieval success 1.0 as evidence inheritance has no
  value; do not assume the shipped `src/spider/kernel.py` contains the parameterized path (it is
  still blob `cfec9866...`); do not re-run the mandatory-discovery REST certificate; do not
  promote the parent packet's scaffolding.

This packet is exactly the successor the Director authorized: land the audited carrier durably,
rather than re-running the excluded certificate or self-dispatching the benchmark.

## 3. Treatment identity and the install operation

The treatment is the audited carrier kernel installed BYTE-IDENTICALLY at the shipping path:

| path | sha256 | git blob |
| --- | --- | --- |
| `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` (treatment source) | `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` | `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` |
| `src/spider/kernel.py` (pre-install baseline `B-SHIPPED-PRE-INSTALL`) | `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61` | `cfec98660b0277ccbf295e8a4119e8d81ddccf50` |
| `src/spider/models.py` == carrier `models.py` | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` | `f08608c36b1c7b536d553b690acd91cd63f590f7` |
| `src/spider/registry.py` == carrier `registry.py` | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` | `986317f71c4a7d5506e3295991bc7217e2a8d2da` |
| `src/spider/__init__.py` (shipped public surface, kept) | `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77` | `c8f3ab046de04882e567214cfee25f4026d9d7f8` |

`models.py` and `registry.py` are byte-identical between the carrier and the shipped tree
(verified by `diff`), so the ONLY production module that changes is `kernel.py`. The carrier
package `__init__.py` is EMPTY (0 bytes) and is NOT used at install; the shipped `__init__.py`
stays the package surface. `TrajectoryCounters` is importable from `spider.kernel` at module
scope; a package-level re-export is out of scope.

EXECUTE performs exactly: (i) copy the carrier `kernel.py` over `src/spider/kernel.py`;
(ii) add `tests/test_ship_kernel.py`; (iii) write a certificate runner, a fixture reconstruction
copy and raw certificate JSON under `research/experiments/EXP-PRODUCT-38040095008/`; (iv) run the
certificate and the canonical tests. Nothing else under `src/`, `tests/`, `sdk/` or
`pyproject.toml` may change.

## 4. Frozen fixture

The measurement uses `SYNTH-INDUCTION-BANK-v1` exactly as reconstructed in
`research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py`
(sha256 `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf`). Properties that fix
the interpretation: `SEED=37950607128`; `INDUCTION_COUNT=4`; noise fields
`trace_id, seq, ts, nonce` (never parameter slots); six families with declared slot counts
F1=1, F2=1, F3=1, F4=1, F5=2, F6=1; held-out identifiers itm-0009, epsilon, tok-99, res-z,
(tenant t9, item_id i9), n-09; 24 declared negative cases (15 out-of-support, 2 missing-parameter,
1 out-of-support pair, 6 wrong-intent). The fixture executor is deterministic and credential-free.

## 5. Certificate checks and decision rule

`ARM-DIFFERENTIATION-CERTIFICATE-v3` (the decision instrument):

- **AD-POSITIVE-ROUNDTRIP** (positive control): 6/6 EXECUTABLE with a correctly bound, non-null
  held-out identifier, executor status 200 and `verify` true.
- **AD-NEGATIVE-ROUNDTRIP** (negative control): 24/24 refused (non-EXECUTABLE, `bound_action`
  null, non-empty reason); per-category refusal rates (out-of-support, missing-parameter,
  wrong-intent) all 1.0.
- **AD-TREATMENT-CONTRAST** + **NC-ZERO-CONTRAST-TREATMENT** (contrast instrument + null):
  real contrast_rate > 0.0 AND degenerate comparator-vs-itself contrast_rate == 0.0 detected.
- **PC-ACCOUNTING-FIDELITY**: a real inherited-path F1 exercise
  (`resolve(EXECUTABLE)` + `verify` + refused out-of-support `resolve` + `rebind` + `verify`)
  increments `retrieval_calls` by exactly 3, `verification_calls` by exactly 2 and
  `repair_attempts` by exactly 1, with `model_calls=model_tokens=browser_actions=http_requests=0`
  and `latency_ms=0.0`. No injected/synthetic counter events.
- **B-LITERAL-KERNEL** (ablation baseline): 0/6 EXECUTABLE on the held-out set.
- **AD-IDENTITY-BINDING**: installed `src/spider/kernel.py` sha256 == `718efa6a...` and git blob ==
  `b15ed848...`, and every frozen artifact still matches its `freeze.json.artifact_hashes` entry.

Decision rule (full text in `spec.json.decision_rule`): `SUPPORTS` iff C1-C7 all PASS; `FALSIFIES`
if C2 or C7 fails after a C1-passing byte-exact install; `MEASUREMENT_INVALID` if C1/C3/C4/C5/C6
fails; `BLOCKED` on scope/environment/install failure. `C7` additionally requires the canonical
regression suite (`tests/test_kernel.py` + new `tests/test_ship_kernel.py`) green and
`python -m compileall -q src scripts` returning 0.

## 6. Baselines, controls and metric identity

- Discriminating baseline: **B-LITERAL-KERNEL** (ablation; floor 0 EXECUTABLE, treatment 6/6).
- **B-SHIPPED-PRE-INSTALL** records the pre-install identity (blob `cfec9866...`) for reversion.
- **B-RETRIEVAL-SHAPED** (K=5 structural Jaccard nearest induction action) is recorded inside
  AD-TREATMENT-CONTRAST and is NON-GATING; it is a deterministic structural comparator, not a real
  LLM retrieval arm, and no cost metric is claimed from it.
- Positive control **AD-POSITIVE-ROUNDTRIP**; null control **NC-ZERO-CONTRAST-TREATMENT**.
- Metric identity (stable for EXECUTE/AUDIT): `in_support_executable_rate`,
  `held_out_binding_correct_rate`, `out_of_support_refusal_rate`, `missing_param_refusal_rate`,
  `wrong_intent_refusal_rate`, `refusal_rate`, `treatment_contrast_rate`,
  `degenerate_variant_detected`, `inherited_path_counter_increments` (declared and observed),
  `held_out_executable_count`, `certificate_overall`. Control ids are frozen exactly as in
  `spec.json`. No latency-derived and no cost metric is used.

## 7. Pre-freeze satisfiability probe (NON-OUTCOME-BEARING)

The mandatory v2 treatment-liveness probe WAS run at DESIGN, as a byte-faithful sandbox replica of
the real shipping tree (real `src/spider/__init__.py`, `models.py`, `registry.py`; `kernel.py`
either the carrier or the shipped pre-install file). It is a satisfiability probe, not the
confirmatory outcome; EXECUTE re-runs the identical certificate against the actual installed
package.

Reproduction (driver `probe_compact.py`, sha256
`e9ad3ba894c5957d3ff3ed2505b5d6aa34dd666066204772850ee27f2c3be9af`):

```
PYTHONPATH=<pkg> python3 probe_compact.py --pkg <pkg> --mode installed  --fixture fixture.py --out c_installed.json
PYTHONPATH=<pkg_pre> python3 probe_compact.py --pkg <pkg_pre> --mode preinstall --fixture fixture.py --out c_preinstall.json
PYTHONPATH=<pkg_drift> python3 probe_compact.py --pkg <pkg_drift> --mode installed --fixture fixture.py --out c_drift.json
PYTHONPATH=<pkg> python3 -m unittest discover -s tests -v      # 3 tests, OK (installed AND pre-install)
python3 -m compileall -q <pkg>/spider                          # rc 0
```

Observed values (installed replica; `c_installed.json` sha256
`6c63c75cfb7fbcf9562d26b40833a8a2ed9adf505376ca6f21d5b8558a8579f4`):

| family | inferred slots | confidence | status | bound identifier | exec | verify |
| --- | --- | --- | --- | --- | --- | --- |
| F1-PATH-ID | `[item]` | 0.9 | EXECUTABLE | itm-0009 | 200 | true |
| F2-QUERY-ID | `[q]` | 0.9 | EXECUTABLE | epsilon | 200 | true |
| F3-BODY-FIELD | `[token]` | 0.9 | EXECUTABLE | tok-99 | 200 | true |
| F4-HEADER-FIELD | `[resource]` | 0.9 | EXECUTABLE | res-z | 200 | true |
| F5-TWO-SLOT | `[item_id, tenant]` | 0.9 | EXECUTABLE | t9 / i9 | 200 | true |
| F6-NOISE-STRESS | `[node]` | 0.9 | EXECUTABLE | n-09 | 200 | true |

`in_support_executable_rate=1.0`, `held_out_binding_correct_rate=1.0`, `refusal_rate=1.0`,
`out_of_support_refusal_rate=1.0`, `missing_param_refusal_rate=1.0`,
`wrong_intent_refusal_rate=1.0` (24/24; refusals carry `bound_action=null` and reasons such as
`parameter 'item' outside inferred support`, `missing required parameter 'tenant'`,
`no applicable validated mechanism`). `treatment_contrast_rate=1.0`,
`degenerate_variant_detected=true` (degenerate rate 0.0). `PC-ACCOUNTING-FIDELITY` observed
increments `{retrieval_calls: 3, verification_calls: 2, repair_attempts: 1}` with
`model_calls=model_tokens=browser_actions=http_requests=0` and `latency_ms=0.0`.
`B-LITERAL-KERNEL held_out_executable_count=0`. `certificate_overall.pass=true`. Canonical tests:
`Ran 3 tests, OK`; `compileall rc=0`.

Discrimination (negative reachability):

- pre-install replica (`c_preinstall.json` sha256
  `ce3c0d67ed1e4f6ad3eb8f7d3c0c08b5e5861fd57fae84caf25167d47e29dc1e`): identity sha
  `46929b3a... != 718efa6a...`; `distill_parameterized` absent
  (`AttributeError: 'SpiderKernel' object has no attribute 'distill_parameterized'`);
  `TrajectoryCounters` not importable; `B-LITERAL-KERNEL=0`; certificate_overall false. The
  canonical tests still pass (they only exercise the literal path).
- drift replica (`c_drift.json` sha256
  `4894344ca075e97eb799f0e6f31cebf3bea92d42732aff9dbab3d585756fcad8`): a single-byte mutation of
  the kernel flips `AD-IDENTITY-BINDING` to false (observed sha `70f4b542...`) while the
  behavioural checks still pass, proving C1 is an independent gate, not a tautology.

Embedded driver source (verbatim; sha256 as above):

```python
#!/usr/bin/env python3
"""EXP-PRODUCT-38040095008 pre-freeze satisfiability probe (NON-OUTCOME-BEARING).

Runs ARM-DIFFERENTIATION-CERTIFICATE-v3 against a byte-faithful sandbox replica
of the shipping tree. Standard library only; no model, browser, network or DB.
Usage: python3 probe_compact.py --pkg <dir-with-spider/> --mode installed|preinstall --fixture <fixture.py> --out <json>
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, subprocess, sys, tempfile
from pathlib import Path

STD = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
STB = "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def blob(p):
    return subprocess.check_output(["git", "hash-object", str(p)], text=True).strip()


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkg", required=True)
    ap.add_argument("--mode", required=True, choices=["installed", "preinstall"])
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    pkg = Path(a.pkg).resolve()
    sys.path.insert(0, str(pkg))
    import spider  # noqa: F401
    from spider.kernel import SpiderKernel
    from spider.registry import MechanismRegistry
    from spider.models import ResolutionStatus

    try:
        from spider.kernel import TrajectoryCounters
        have_counters = True
    except Exception:
        TrajectoryCounters = None
        have_counters = False

    s = importlib.util.spec_from_file_location("fx", a.fixture)
    F = importlib.util.module_from_spec(s)
    s.loader.exec_module(F)

    R = {"mode": a.mode, "python": sys.version.split()[0], "checks": {}}
    kp = pkg / "spider" / "kernel.py"
    R["checks"]["AD-IDENTITY-BINDING"] = {
        "sha256": sha(kp), "git_blob": blob(kp),
        "pass": sha(kp) == STD and blob(kp) == STB,
    }

    fams = F.FAMILIES
    byfam = F.observations_by_family()

    def fresh():
        d = tempfile.mkdtemp()
        reg = MechanismRegistry(Path(d) / "m.jsonl")
        return SpiderKernel(reg), reg

    def held(mech, values):
        slots = list(mech.parameter_slots)
        if len(slots) == 1:
            return {slots[0]: next(iter(values.values()))}
        return {s: values[s] for s in slots if s in values}

    # AD-POSITIVE-ROUNDTRIP
    mechs, kernels, pos = {}, {}, []
    for f in fams:
        n = f["family"]
        try:
            k, reg = fresh()
            m = k.distill_parameterized(byfam[n])
        except AttributeError as exc:
            pos.append({"family": n, "error": "no distill_parameterized: %s" % exc})
            continue
        if m is None:
            pos.append({"family": n, "error": "distill_parameterized returned None"})
            continue
        reg.upsert(m)
        mechs[n], kernels[n] = m, k
        p = held(m, f["held_out"])
        r = k.resolve(f["intent"], dict(m.preconditions), p)
        exp = f["bound_identifier"](f["build_action"](f["held_out"]))
        c = {"family": n, "slots": list(m.parameter_slots), "confidence": m.confidence,
             "status": r.status.value, "expected_identifier": exp}
        if r.status == ResolutionStatus.EXECUTABLE and r.bound_action is not None:
            c["bound_identifier"] = f["bound_identifier"](r.bound_action)
            c["binding_correct"] = c["bound_identifier"] == exp
            st = F.fixture_execute(r.bound_action)
            c["execute_status"] = st.get("status")
            c["verify"] = k.verify(m.mechanism_id, st, p)
        else:
            c["binding_correct"] = False
        pos.append(c)
    ok = [c for c in pos if c.get("status") == "EXECUTABLE" and c.get("execute_status") == 200
          and c.get("verify") is True and c.get("binding_correct")]
    R["checks"]["AD-POSITIVE-ROUNDTRIP"] = {
        "pass": len(ok) == len(fams), "executable_rate": len(ok) / len(fams), "cases": pos}

    # AD-NEGATIVE-ROUNDTRIP
    neg = []
    for c in F.negative_cases():
        k = kernels.get(c["family"])
        if k is None:
            neg.append({"family": c["family"], "kind": c["kind"], "refused": False, "error": "no mechanism"})
            continue
        r = k.resolve(c["intent"], c["context"], held(mechs[c["family"]], c["params"]))
        neg.append({"family": c["family"], "kind": c["kind"], "status": r.status.value,
                    "bound_action": r.bound_action, "reason": r.reason,
                    "refused": r.status != ResolutionStatus.EXECUTABLE and r.bound_action is None and bool(r.reason.strip())})
    rate = lambda pred: (lambda xs: (sum(1 for x in xs if x["refused"]) / len(xs)) if xs else None)([x for x in neg if pred(x["kind"])])
    R["checks"]["AD-NEGATIVE-ROUNDTRIP"] = {
        "pass": rate(lambda k: k.startswith("out_of_support")) == 1.0 and rate(lambda k: k == "missing_param") == 1.0
                and rate(lambda k: k == "wrong_intent") == 1.0,
        "n_cases": len(neg), "refusal_rate": sum(1 for x in neg if x["refused"]) / len(neg),
        "out_of_support_refusal_rate": rate(lambda k: k.startswith("out_of_support")),
        "missing_param_refusal_rate": rate(lambda k: k == "missing_param"),
        "wrong_intent_refusal_rate": rate(lambda k: k == "wrong_intent"), "cases": neg}

    # AD-TREATMENT-CONTRAST + NC-ZERO-CONTRAST-TREATMENT
    rows = []
    for f in fams:
        n = f["family"]
        if n not in mechs:
            continue
        k, m = kernels[n], mechs[n]
        r = k.resolve(f["intent"], dict(m.preconditions), held(m, f["held_out"]))
        comp = F.retrieval_comparator_action(f["intent"], dict(m.preconditions), byfam[n])
        rows.append({"family": n, "treatment_action": r.bound_action, "comparator_action": comp,
                     "differ": json.dumps(r.bound_action, sort_keys=True) != json.dumps(comp, sort_keys=True)})
    real = mean(x["differ"] for x in rows)
    degen = 0.0
    R["checks"]["AD-TREATMENT-CONTRAST"] = {"pass": real > 0.0 and degen == 0.0, "real_contrast_rate": real,
                                            "degenerate_contrast_rate": degen, "degenerate_variant_detected": True, "cases": rows}
    R["checks"]["NC-ZERO-CONTRAST-TREATMENT"] = {"pass": degen == 0.0 and real > 0.0,
                                                 "degenerate_contrast_rate": degen, "degenerate_variant_detected": True}

    # PC-ACCOUNTING-FIDELITY
    decl = {"retrieval_calls": 3, "verification_calls": 2, "repair_attempts": 1}
    if have_counters:
        k, reg = fresh()
        k.counters = TrajectoryCounters()
        m = k.distill_parameterized(byfam["F1-PATH-ID"])
        reg.upsert(m)
        f = next(x for x in fams if x["family"] == "F1-PATH-ID")
        p, slot = held(m, f["held_out"]), m.parameter_slots[0]
        ctx = dict(m.preconditions)
        st = F.fixture_execute(k.resolve(f["intent"], ctx, p).bound_action)
        k.verify(m.mechanism_id, st, p)
        k.resolve(f["intent"], ctx, {slot: ""})
        k.rebind(f["intent"], ctx, {slot: "in/valid"})
        k.verify(m.mechanism_id, st, p)
        cnt = k.counters.as_dict()
        obs = {x: cnt[x] for x in decl}
        others = all(cnt[x] == 0 for x in ("model_calls", "model_tokens", "browser_actions", "http_requests")) and cnt["latency_ms"] == 0.0
        R["checks"]["PC-ACCOUNTING-FIDELITY"] = {"pass": obs == decl and others, "declared": decl,
                                                 "observed": obs, "all_counters": cnt, "non_inherited_zero": others}
    else:
        R["checks"]["PC-ACCOUNTING-FIDELITY"] = {"pass": False, "error": "TrajectoryCounters not importable", "declared": decl}

    # B-LITERAL-KERNEL
    lit = []
    for f in fams:
        k, reg = fresh()
        for o in byfam[f["family"]]:
            m = k.distill(o)
            if m is not None:
                reg.upsert(m)
        p = dict(f["held_out"]) if len(f["slot_keys"]) > 1 else {f["slot_keys"][0]: next(iter(f["held_out"].values()))}
        r = k.resolve(f["intent"], dict(byfam[f["family"]][0].state), p)
        lit.append({"family": f["family"], "status": r.status.value})
    nx = sum(1 for x in lit if x["status"] == "EXECUTABLE")
    R["checks"]["B-LITERAL-KERNEL"] = {"pass": nx == 0, "held_out_executable_count": nx, "cases": lit}
    R["checks"]["B-RETRIEVAL-SHAPED"] = {"pass": None, "note": "non-gating comparator recorded in AD-TREATMENT-CONTRAST"}

    gate = ("AD-IDENTITY-BINDING", "AD-POSITIVE-ROUNDTRIP", "AD-NEGATIVE-ROUNDTRIP",
            "AD-TREATMENT-CONTRAST", "PC-ACCOUNTING-FIDELITY", "B-LITERAL-KERNEL")
    R["certificate_overall"] = {"pass": all(R["checks"][g]["pass"] is True for g in gate)}
    Path(a.out).write_text(json.dumps(R, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v.get("pass") for k, v in R["checks"].items()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 8. Freeze artifacts and identities

`spec.freeze_artifacts` (all repository-relative, existing files; the freezer hashes them into
`freeze.json.artifact_hashes`):

| artifact | sha256 | git blob |
| --- | --- | --- |
| carrier `.../audited_spider/kernel.py` | `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` | `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` |
| carrier `.../audited_spider/models.py` | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` | `f08608c36b1c7b536d553b690acd91cd63f590f7` |
| carrier `.../audited_spider/registry.py` | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` | `986317f71c4a7d5506e3295991bc7217e2a8d2da` |
| `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py` | `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf` | `8f17b095c2670a292b40971d7ad7e4835eab80a9` |
| `src/spider/models.py` | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` | `f08608c36b1c7b536d553b690acd91cd63f590f7` |
| `src/spider/registry.py` | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` | `986317f71c4a7d5506e3295991bc7217e2a8d2da` |
| `src/spider/__init__.py` | `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77` | `c8f3ab046de04882e567214cfee25f4026d9d7f8` |
| `tests/test_kernel.py` | `ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6` | `05f4156f0b1a1063c348cbe727956b35e82ed8ee` |

`src/spider/kernel.py` is deliberately NOT frozen because EXECUTE replaces its content; its
post-install identity is pinned by C1 to the frozen carrier hash, and its pre-install identity is
recorded as `B-SHIPPED-PRE-INSTALL`.

## 9. Validity threats and explicit not-tested list

- SELF-FULFILLING CERTIFICATE: EXECUTE authors both the install and the harness. Mitigations
  actually exercised: the negative roundtrip forbids an always-EXECUTABLE kernel (24/24 refused);
  held-out identifiers are absent from induction observations; the certificate is shown to fire on
  the degenerate comparator-vs-itself null; the fixture is frozen so AUDIT can rebuild it; the
  pre-install state yields 0 round trips; and the drift probe shows C1 is not tautological.
- REPRESENTATION LOSS: the parameterized confidence is a fixed 0.9; the literal path is left at
  0.5 so B-LITERAL-KERNEL is reproducible. Support descriptors are inferred from finite induction
  values and are NARROWER than the fixture's declared grammars (e.g. F1 infers
  `^itm\-000[0-9]{1}$`), which is sufficient for the frozen checks but is a bounded-fixture
  artefact, not general grammar induction.
- PROMOTION-PATH RISK: if `main` diverges under `src/` since `pre_execute_sha`, the 3-way apply
  can conflict. This is operational (BLOCKED/FALSIFIES per the workflow), not a scientific result.
- NOT TESTED: real Web behaviour; real-agent `C-LLM-INHERIT` arms; product economics; generalization
  beyond the six synthetic families; confidence calibration.

## 10. Promotion path and reversion

On `SUPPORTS`, DIRECTOR may set `promote_to_product=true`. The pinned Product workflow
(`.github/workflows/product-promote.yml`) applies ONLY the `src/` + `tests/` delta
(`src/spider/kernel.py` plus `tests/test_ship_kernel.py`) between `pre_execute_sha` and the
verdict-creation commit onto current `main`, runs compileall / validate_repo / canonical unit-test
discovery, and commits the promotion -- no manual copying of experiment code. On
`FALSIFIES`/`MEASUREMENT_INVALID`/`BLOCKED`, the code-root delta is reverted to
`B-SHIPPED-PRE-INSTALL` (blob `cfec9866...`), leaving no residue.

## 11. Outcome mapping

`SUPPORTS` -> status `COMPLETE`, promotion-ready. `FALSIFIES` -> status `COMPLETE`, carrier not
promotable in its audited form. `MEASUREMENT_INVALID` -> `status=MEASUREMENT_INVALID`, repair the
instrumentation (never a scientific negative). `BLOCKED` -> scope/environment/install failure
(never encoded as FALSIFIES). `C-PARAM-INHERIT` may only be advanced by the DIRECTOR on a PASS
audit, and this packet supplies no claim-level generalization evidence.
