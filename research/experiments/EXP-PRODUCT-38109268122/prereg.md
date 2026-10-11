# EXP-PRODUCT-38109268122 preregistration

Lane: `product`. Claim: `C-PARAM-INHERIT`. Design contract: v2. Status: DESIGN (pre-freeze; the deterministic freezer appends `freeze.json` after the independent `design_review.json` returns PASS).

This file is written before any confirmatory measurement. It freezes the question, the treatment, the baselines, the controls, the decision rule, the pre-freeze satisfiability evidence and the exact instrument driver. It must not be edited after `freeze.json` exists.

## 1. Governance and mandate binding

`research/experiments/EXP-PRODUCT-38109268122/request.json` carries a `director_mandate` with `schema_version` 1, `cycle_id` `38108882486`, `lane` `product`, `allocation.action` `CONTINUE`, `allocation.claim_id` `C-PARAM-INHERIT`, `allocation.parent_handoff_disposition` `SUPERSEDE` and `allocation.cognitive_reset` true. The mandate's strategic question is binding: install the already-audited parameterized mechanism carrier into the shipped kernel and promote it through the audited product promotion path with a binding pre-freeze positive/negative certificate, whose confidence flow is not defeated by the literal `distill()` candidate confidence 0.5 versus the default `resolve()` `min_confidence` 0.8, demonstrating one known-positive executable binding and one known-negative refusal, with honest counters and the pinned git blob/sha256 recorded for the later four-arm benchmark, triggering promotion ONLY on independent audit PASS -- thereby discharging blocker B1.

The parent handoff (`EXP-PRODUCT-37989728440`) is continuity evidence only. Its disposition here is `SUPERSEDE`: this packet does NOT re-run the mandatory-discovery deterministic credential-free REST certificate that the parent explicitly excludes, and does NOT adopt the parent's `next_question` (the external four-arm benchmark) as its own objective. It performs the B1 prerequisite that must precede that benchmark.

## 2. Claim identity and ceiling

Target claim: `C-PARAM-INHERIT` (effective Codex status EXPERIMENTAL). This experiment is a capability/durability gate, not an economics or generalization experiment. Claim ceiling: the packet may support "the audited parameterized-inheritance capability is live, safe and durable at the shipping position, with the literal 0.5-vs-0.8 confidence defect gated", and nothing broader. It provides ZERO evidence for or against C-LLM-INHERIT / C-RESIDUAL-NOVELTY / C-PRODUCT-ECON, and no new evidence that parameter inference generalizes to free-form payloads outside the frozen bank. `claim_ids` = `["C-PARAM-INHERIT"]` (inside the Product lane charter `priority_claims`).

## 3. Question, hypothesis, falsifier

Question, hypothesis and falsifier are stated exactly in `spec.json` (`question`, `hypothesis`, `falsifier`). In short: does a byte-identical install of the audited carrier at `src/spider/kernel.py` yield a shipped package that (a) executes a known-positive inherited parameterized binding on an UNSEEN held-out identifier, (b) refuses a known-negative binding with a recorded reason and a null action and returns exactly `UNKNOWN` for the no-applicable-mechanism case, (c) clears the 0.5-vs-0.8 confidence-flow requirement, (d) keeps counters honest, and (e) preserves the shipped regression surface, with the installed identity pinned to the frozen carrier blob/sha256?

## 4. Material divergence from pre-2.0 and prior 2.0 attempts

Pre-2.0: per the mandate's `comparative_reasoning`, the historical program (P2-REPLAY-COST pre2 4.114; P2-BLIND-COMPOSITION pre2 4.697; archived P2-MIND2WEB) withdrew an ~8.5x replay headline and showed exact-route replay is weak while retrieval is stronger, and it never shipped a parameterized carrier with a known-negative refusal. This packet is therefore not a duplicate rerun: it creates the shipped artifact the original program never had.

Prior 2.0 B1 attempts `EXP-PRODUCT-37999047472` and `EXP-PRODUCT-38040095008` also targeted the carrier install but never froze (design-stage failure fingerprint `3b9ff5e4e9e73f23e368efb4`, `model_design_review.json` model `opencode/exo-free` exit_code 1). This packet follows the current mandate more tightly than `EXP-PRODUCT-38040095008` in three ways: (i) it adds an explicit gating `CONFIDENCE-FLOW` check for the 0.5-vs-0.8 defect rather than folding it into the literal baseline; (ii) it requires the wrong-intent/no-applicable case to return exactly `ResolutionStatus.UNKNOWN` and records OUT-OF-SUPPORT/MISSING-PARAMETER honestly as `EXPLORE` rather than mislabelling them; (iii) it excludes `src/spider/kernel.py` from `freeze_artifacts` (EXECUTE must mutate it) and pins its post-install identity by decision-rule C1, avoiding the v2 immutability defect seen in `EXP-PRODUCT-38107837348` (which also used flat-string `freeze_eligibility`). No repo file outside `spec.json` and `prereg.md` was written at DESIGN.

## 5. Parent-handoff continuity (four-way distinction preserved)

From `research/experiments/EXP-PRODUCT-37989728440/handoff.json` (sha256 `911f765d04a83974f20d113da206b4075337c3a9bed4c5a77a8f06ffb4773ed9`):

- established: frozen-input/carrier integrity intact and the carrier is vendored byte-identically to git blob `b15ed848...` (sha256 `718efa6a...`); a measurement-valid deterministic REST run occurred; the kernel's parameterized path is causally necessary on that substrate (B-LITERAL-KERNEL 0.0 vs PC-EXACT-REPLAY 1.0); the shipped `src/spider/kernel.py` is still blob `cfec9866...` and does NOT contain the parameterized path.
- rejected (bounded, substrate class only): a certified dynamic range on the mandatory-discovery deterministic REST class; work compression / http-request savings for the treatment there; the latency-inclusive cost metric as discriminating; the claim that the freeze step enforces the C1 dynamic-range certificate.
- unknown: whether ANY credential-free deterministic substrate can show a certified dynamic range for this arm design; whether asymmetric/amortized discovery would let the treatment save work; whether the external four-arm C-LLM-INHERIT benchmark can run (needs a credential-free model endpoint); whether applying support predicates to free-form payload values is a defect; the freeze-gate repair timeline.
- do_not_assume: do not read the parent packet as evidence for/against C-RESIDUAL-NOVELTY; do not treat ceiling success rates as evidence inheritance lacks value; do not treat the 40/40 success or C3/C4 as work compression; do NOT assume the shipped kernel contains the parameterized path (it does not); do not assume the pre-freeze certificate gate is enforced by the freezer; do not re-run the deterministic REST certificate; do not promote any parent code/scaffolding; do not generalize the substrate workaround into a support-generalization result.

This experiment operates strictly on the "unknown/gap" that the parent left open at the shipping position and does not disturb the parent's bounded negatives.

## 6. Task bank, arms, controls and metrics

Task bank: the frozen `SYNTH-INDUCTION-BANK-v1` reconstruction at `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py` (sha256 `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf`). Six families (`F1-PATH-ID`, `F2-QUERY-ID`, `F3-BODY-FIELD`, `F4-HEADER-FIELD`, `F5-TWO-SLOT`, `F6-NOISE-STRESS`), four induction observations each, held-out identifiers `itm-0009`, `epsilon`, `tok-99`, `res-z`, `t9`/`i9`, `n-09` disjoint from the induction values, and 24 declared negative cases. Execution is a deterministic offline `fixture_execute` returning 200/412/422.

Treatment arm: the shipped package `src/spider` with the audited carrier kernel installed byte-identically at `src/spider/kernel.py` (`distill_parameterized -> resolve -> execute -> verify/UNKNOWN`).

Stable control/metric ids (reused by EXECUTE and AUDIT):
- `AD-POSITIVE-ROUNDTRIP` (known-positive): 6/6 `EXECUTABLE`, correct held-out binding, execute 200, verify true.
- `CONFIDENCE-FLOW` (mandate gate): parameterized confidence >= 0.8 while literal `distill()` confidence == 0.5 and a parameterized resolution reached `EXECUTABLE`.
- `AD-NEGATIVE-ROUNDTRIP` (known-negative refusal): 24/24 non-`EXECUTABLE`, `bound_action` null, non-empty reason; wrong-intent exactly `UNKNOWN`.
- `AD-TREATMENT-CONTRAST` (non-gating structural): real contrast > 0.0.
- `NC-ZERO-CONTRAST-TREATMENT` (degenerate null): contrast 0.0 and detected.
- `PC-ACCOUNTING-FIDELITY`: inherited-path increments exactly `{retrieval_calls: 3, verification_calls: 2, repair_attempts: 1}`, all other counters 0.
- `AD-IDENTITY-BINDING`: installed kernel == carrier hash/blob, distinct from the pre-install hash/blob.
- `B-LITERAL-KERNEL` (gating floor): 0/6 `EXECUTABLE`.
- `B-SHIPPED-PRE-INSTALL` (non-gating baseline state): blob `cfec9866...` sha256 `46929b3a...`.
- `B-RETRIEVAL-SHAPED` (non-gating structural comparator).

## 7. Pre-freeze satisfiability probe (cheap, non-outcome-bearing)

The required v2 treatment-liveness and reachability probes were executed at DESIGN against the exact frozen carrier bytes in a throwaway package outside the repository. No confirmatory outcome was inspected and no frozen threshold was tuned.

Commands (run in `/tmp`; the repository was not modified):

```
# throwaway package: carrier kernel + shipped models/registry + frozen fixture
python3 /tmp/opencode/b1probe/probe.py    # positive / negative / confidence-flow / literal floor
python3 /tmp/opencode/b1probe/probe2.py   # treatment contrast + degenerate null + drift
python3 /tmp/opencode/b1probe/probe3.py   # accounting increments
SPIDER_CERT_SRC=... SPIDER_CERT_FIXTURE=... python3 <harness>/certificate.py   # instrument dry-run
PYTHONPATH=src python3 -m unittest discover -s tests -v   # regression, both pre- and post-install replica
python3 -m compileall -q src scripts                       # compile surface
```

Observed (all PASS on the installed carrier; the instrument is the driver embedded below):

- `AD-POSITIVE-ROUNDTRIP`: 6/6. `EXECUTABLE`, confidence 0.9, bound identifiers `itm-0009`, `epsilon` (inferred slot `q`), `tok-99`, `res-z`, `t9`/`i9` (inferred slots `item_id`,`tenant`), `n-09`; execute status 200; verify true.
- `CONFIDENCE-FLOW`: parameterized `{0.9}` >= 0.8; literal `distill()` confidences `{0.5}` < 0.8; executable rate 1.0.
- `AD-NEGATIVE-ROUNDTRIP`: 24/24 refused; out-of-support and missing-parameter returned `EXPLORE`; all six wrong-intent cases returned exactly `UNKNOWN`; every `bound_action` null with a non-empty reason.
- `AD-TREATMENT-CONTRAST`: real contrast rate 1.0; degenerate (comparator-vs-itself) 0.0 and detected.
- `PC-ACCOUNTING-FIDELITY`: observed `{model_calls: 0, model_tokens: 0, browser_actions: 0, http_requests: 0, retrieval_calls: 3, verification_calls: 2, repair_attempts: 1, latency_ms: 0.0}`.
- `AD-IDENTITY-BINDING` dry-run: driver run in a git replica with the shipped literal blob at HEAD and the carrier installed produced PASS (`installed_sha256 == 718efa6a...`, `installed_git_blob == b15ed848...`); a single-byte mutation flipped the check (mutated sha `a2f2702c...`), proving C1 is independently sensitive.
- `B-LITERAL-KERNEL`: `held_out_executable_count == 0` (the shipped literal path is at the floor).
- Regression: `tests/test_kernel.py` 3/3 OK under `PYTHONPATH=src python -m unittest discover -s tests -v` on both the shipped tree and a byte-faithful post-install replica (only `kernel.py` replaced); `compileall -q src scripts` returned 0.

Reachability: SUPPORTS is reachable (above); FALSIFIES is reachable (the shipped literal state yields 0/6 and lacks `distill_parameterized`); MEASUREMENT_INVALID is reachable (the drift probe flips C1); BLOCKED is reachable on scope/environment/artifact-missing failure.

The instrument is frozen in text below and is written verbatim by EXECUTE to `research/experiments/EXP-PRODUCT-38109268122/harness/certificate.py`, importing the fixture from the frozen `EXP-PRODUCT-37950607128/harness` path. `SPIDER_CERT_SRC` / `SPIDER_CERT_FIXTURE` exist only for the DESIGN replica dry-run; the real run uses the repository defaults.

```python
#!/usr/bin/env python3
"""ARM-DIFFERENTIATION + CONFIDENCE-FLOW CERTIFICATE runner.

Frozen instrument for EXP-PRODUCT-38109268122 (Product lane, C-PARAM-INHERIT).
Credential-free, deterministic, standard-library only. It is the EXECUTE
confirmatory instrument; it is NOT the DESIGN satisfiability probe (whose
output is recorded in prereg.md section 7).

Checks (stable ids, reused by AUDIT):
  AD-POSITIVE-ROUNDTRIP, CONFIDENCE-FLOW, AD-NEGATIVE-ROUNDTRIP,
  AD-TREATMENT-CONTRAST, PC-ACCOUNTING-FIDELITY, AD-IDENTITY-BINDING,
  B-LITERAL-KERNEL.
C8_PROMOTABILITY-REGRESSION is run separately by EXECUTE (unittest + compileall).

Import roots are overridable by SPIDER_CERT_SRC / SPIDER_CERT_FIXTURE for the
pre-freeze replica probe; in the real run they default to the repository paths.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
EXPERIMENT_DIR = HERE.parent.parent
REPO_ROOT = EXPERIMENT_DIR.parents[2]
EXPERIMENT_ID = "EXP-PRODUCT-38109268122"

CARRIER_KERNEL_SHA256 = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
CARRIER_KERNEL_BLOB = "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796"
PREINSTALL_KERNEL_SHA256 = "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61"
MIN_CONFIDENCE = 0.8

SRC = Path(os.environ.get("SPIDER_CERT_SRC", str(REPO_ROOT / "src")))
FIXTURE_DIR = Path(os.environ.get(
    "SPIDER_CERT_FIXTURE",
    str(REPO_ROOT / "research" / "experiments" / "EXP-PRODUCT-37950607128" / "harness"),
))
for _p in (str(SRC), str(FIXTURE_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import fixture as fx  # noqa: E402
from spider.kernel import SpiderKernel, TrajectoryCounters, _support_accepts  # noqa: E402
from spider.models import ResolutionStatus  # noqa: E402
from spider.registry import MechanismRegistry  # noqa: E402


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def write_json(path: Path, payload) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, indent=2).encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


def stable_context(family: dict) -> dict:
    return {"site": "fixture.invalid", "route": family["route"], "auth": "public"}


def params_for(mech, held_values: list) -> dict:
    supports = (mech.verification_rule or {}).get("parameter_supports", {})
    params: dict = {}
    used: set = set()
    for slot in mech.parameter_slots:
        matched = [v for v in held_values if v not in used and _support_accepts(supports.get(slot), v)]
        if len(matched) == 1:
            params[slot] = matched[0]
            used.add(matched[0])
        elif held_values:
            fallback = next(v for v in held_values if v not in used)
            params[slot] = fallback
            used.add(fallback)
    return params


def main() -> int:
    obs = fx.build_observations()
    fam_obs = fx.observations_by_family()
    registry = MechanismRegistry(Path(tempfile.mkdtemp()) / "cert.jsonl")
    kernel = SpiderKernel(registry, min_confidence=MIN_CONFIDENCE, counters=TrajectoryCounters())
    mechs = {}
    for family in fx.FAMILIES:
        m = kernel.distill_parameterized(fam_obs[family["family"]])
        if m is not None:
            registry.upsert(m)
        mechs[family["family"]] = m

    # ---- AD-POSITIVE-ROUNDTRIP --------------------------------------------
    positive_cases = []
    for family in fx.FAMILIES:
        m = mechs[family["family"]]
        ctx = stable_context(family)
        params = params_for(m, list(family["held_out"].values())) if m else {}
        res = kernel.resolve(family["intent"], ctx, params) if m else None
        bound = executed = None
        verified = False
        if res is not None and res.status == ResolutionStatus.EXECUTABLE and res.bound_action is not None:
            bound = family["bound_identifier"](res.bound_action)
            executed = fx.fixture_execute(res.bound_action)
            verified = kernel.verify(m.mechanism_id, executed, params)
        expected = family["bound_identifier"](family["build_action"](family["held_out"]))
        positive_cases.append({
            "family": family["family"],
            "held_out": family["held_out"],
            "inferred_slots": list(m.parameter_slots) if m else [],
            "confidence": m.confidence if m else None,
            "resolution_status": res.status.value if res else None,
            "bound_identifier": bound,
            "expected_identifier": expected,
            "execution_status": (executed or {}).get("status"),
            "verify_true": verified,
            "pass": bool(m is not None and res is not None and res.status == ResolutionStatus.EXECUTABLE
                         and bound == expected and (executed or {}).get("status") == 200 and verified),
        })
    n_pos = len(positive_cases)
    n_pos_pass = sum(1 for c in positive_cases if c["pass"])
    positive = {
        "control_id": "AD-POSITIVE-ROUNDTRIP",
        "n_cases": n_pos,
        "n_pass": n_pos_pass,
        "in_support_executable_rate": sum(1 for c in positive_cases if c["resolution_status"] == "EXECUTABLE") / n_pos,
        "held_out_binding_correct_rate": sum(1 for c in positive_cases if c["bound_identifier"] == c["expected_identifier"]) / n_pos,
        "pass": n_pos_pass == n_pos,
        "cases": positive_cases,
    }

    # ---- CONFIDENCE-FLOW ---------------------------------------------------
    param_confidences = sorted({c["confidence"] for c in positive_cases if c["confidence"] is not None})
    literal_reg = MechanismRegistry(Path(tempfile.mkdtemp()) / "literal.jsonl")
    literal_kernel = SpiderKernel(literal_reg, min_confidence=MIN_CONFIDENCE)
    literal_confidences = set()
    literal_exec_held_out = 0
    for family in fx.FAMILIES:
        for o in fam_obs[family["family"]]:
            lm = literal_kernel.distill(o)
            if lm is not None:
                literal_reg.upsert(lm)
                literal_confidences.add(lm.confidence)
        if literal_kernel.resolve(family["intent"], stable_context(family), {}).status == ResolutionStatus.EXECUTABLE:
            literal_exec_held_out += 1
    confidence_flow = {
        "control_id": "CONFIDENCE-FLOW",
        "min_confidence": MIN_CONFIDENCE,
        "parameterized_confidences": param_confidences,
        "literal_distill_confidences": sorted(literal_confidences),
        "parameterized_at_or_above_threshold": all(c >= MIN_CONFIDENCE for c in param_confidences) and bool(param_confidences),
        "literal_below_threshold": literal_confidences == {0.5},
        "passed_by_execution": positive["in_support_executable_rate"] > 0.0,
        "pass": (bool(param_confidences) and all(c >= MIN_CONFIDENCE for c in param_confidences)
                 and literal_confidences == {0.5} and positive["in_support_executable_rate"] > 0.0),
    }

    # ---- AD-NEGATIVE-ROUNDTRIP --------------------------------------------
    negative_cases = []
    for case in fx.negative_cases():
        family = next(f for f in fx.FAMILIES if f["family"] == case["family"])
        m = mechs[family["family"]]
        if m is None:
            continue
        res = kernel.resolve(case["intent"], case["context"], case["params"])
        refused = (res.status != ResolutionStatus.EXECUTABLE and res.bound_action is None and bool(res.reason))
        negative_cases.append({**case, "resolution_status": res.status.value, "reason": res.reason,
                               "bound_action": res.bound_action, "refused": refused})
    neg_n = len(negative_cases)
    neg_refused = sum(1 for c in negative_cases if c["refused"])
    wrong_intent = [c for c in negative_cases if c["kind"] == "wrong_intent"]
    negative = {
        "control_id": "AD-NEGATIVE-ROUNDTRIP",
        "n_cases": neg_n,
        "n_refused": neg_refused,
        "refusal_rate": neg_refused / neg_n if neg_n else 0.0,
        "wrong_intent_statuses": sorted({c["resolution_status"] for c in wrong_intent}),
        "wrong_intent_all_unknown": bool(wrong_intent) and all(c["resolution_status"] == "UNKNOWN" for c in wrong_intent),
        "pass": neg_n > 0 and neg_refused == neg_n and bool(wrong_intent) and all(c["resolution_status"] == "UNKNOWN" for c in wrong_intent),
        "cases": negative_cases,
    }

    # ---- AD-TREATMENT-CONTRAST + NC-ZERO-CONTRAST-TREATMENT ---------------
    treatment, comparator = [], []
    for family in fx.FAMILIES:
        m = mechs[family["family"]]
        ctx = stable_context(family)
        params = params_for(m, list(family["held_out"].values())) if m else {}
        res = kernel.resolve(family["intent"], ctx, params) if m else None
        treatment.append(res.bound_action if res is not None and res.status == ResolutionStatus.EXECUTABLE else None)
        comparator.append(fx.retrieval_comparator_action(family["intent"], ctx, obs))
    real_nonzero = sum(1 for t, c in zip(treatment, comparator) if t != c)
    deg_nonzero = sum(1 for t, c in zip(comparator, comparator) if t != c)
    contrast = {
        "control_id": "AD-TREATMENT-CONTRAST",
        "real_contrast_rate": real_nonzero / len(treatment) if treatment else 0.0,
        "degenerate_contrast_rate": deg_nonzero / len(comparator) if comparator else 0.0,
        "degenerate_variant_detected": (deg_nonzero == 0),
        "pass": real_nonzero > 0 and deg_nonzero == 0,
    }

    # ---- PC-ACCOUNTING-FIDELITY -------------------------------------------
    acct = TrajectoryCounters()
    acct_kernel = SpiderKernel(registry, min_confidence=MIN_CONFIDENCE, counters=acct)
    f1 = next(f for f in fx.FAMILIES if f["family"] == "F1-PATH-ID")
    m1 = mechs["F1-PATH-ID"]
    good = params_for(m1, list(f1["held_out"].values()))
    r1 = acct_kernel.resolve(f1["intent"], stable_context(f1), good)
    acct_kernel.verify(m1.mechanism_id, fx.fixture_execute(r1.bound_action), good)
    acct_kernel.resolve(f1["intent"], stable_context(f1), {"item": "in valid"})
    r2 = acct_kernel.rebind(f1["intent"], stable_context(f1), good)
    acct_kernel.verify(m1.mechanism_id, fx.fixture_execute(r2.bound_action), good)
    observed = acct.as_dict()
    declared = {"retrieval_calls": 3, "verification_calls": 2, "repair_attempts": 1}
    expected_zero = ["model_calls", "model_tokens", "browser_actions", "http_requests", "latency_ms"]
    increments_ok = all(observed[k] == v for k, v in declared.items())
    zeros_ok = all(observed[k] == 0 for k in expected_zero)
    accounting = {
        "control_id": "PC-ACCOUNTING-FIDELITY",
        "declared_increments": declared,
        "observed_increments": {k: observed[k] for k in declared},
        "observed_zero_fields": {k: observed[k] for k in expected_zero},
        "scenario": {"resolve_executable": r1.status.value, "refused": "refused", "rebind_executable": r2.status.value},
        "pass": increments_ok and zeros_ok,
    }

    # ---- AD-IDENTITY-BINDING ----------------------------------------------
    installed = SRC / "spider" / "kernel.py"
    installed_bytes = installed.read_bytes()
    post_sha = sha256_bytes(installed_bytes)
    post_blob = git_blob_sha1(installed_bytes)
    try:
        pre_blob = subprocess.run(["git", "rev-parse", f"HEAD:src/spider/kernel.py"], cwd=str(REPO_ROOT),
                                  capture_output=True, text=True, check=True).stdout.strip()
    except Exception as exc:  # pragma: no cover
        pre_blob = None
    identity = {
        "control_id": "AD-IDENTITY-BINDING",
        "installed_kernel_path": str(installed.relative_to(REPO_ROOT)) if str(installed).startswith(str(REPO_ROOT)) else str(installed),
        "installed_sha256": post_sha,
        "installed_git_blob": post_blob,
        "required_carrier_sha256": CARRIER_KERNEL_SHA256,
        "required_carrier_blob": CARRIER_KERNEL_BLOB,
        "preinstall_kernel_sha256": PREINSTALL_KERNEL_SHA256,
        "preinstall_head_blob": pre_blob,
        "pass": (post_sha == CARRIER_KERNEL_SHA256 and post_blob == CARRIER_KERNEL_BLOB
                 and isinstance(pre_blob, str) and len(pre_blob) == 40 and pre_blob != CARRIER_KERNEL_BLOB),
    }

    # ---- B-LITERAL-KERNEL (gating floor) -----------------------------------
    literal_control = {
        "control_id": "B-LITERAL-KERNEL",
        "held_out_executable_count": literal_exec_held_out,
        "literal_confidences": sorted(literal_confidences),
        "pass": literal_exec_held_out == 0,
    }

    checks = {
        "AD-POSITIVE-ROUNDTRIP": positive,
        "CONFIDENCE-FLOW": confidence_flow,
        "AD-NEGATIVE-ROUNDTRIP": negative,
        "AD-TREATMENT-CONTRAST": contrast,
        "PC-ACCOUNTING-FIDELITY": accounting,
        "AD-IDENTITY-BINDING": identity,
        "B-LITERAL-KERNEL": literal_control,
    }
    gating = ["AD-POSITIVE-ROUNDTRIP", "CONFIDENCE-FLOW", "AD-NEGATIVE-ROUNDTRIP",
              "AD-TREATMENT-CONTRAST", "PC-ACCOUNTING-FIDELITY", "AD-IDENTITY-BINDING", "B-LITERAL-KERNEL"]
    overall = "PASS" if all(checks[k]["pass"] for k in gating) else "FAIL"

    metrics = {k: checks[k]["pass"] for k in gating}
    metrics["certificate_overall"] = overall
    metrics["in_support_executable_rate"] = positive["in_support_executable_rate"]
    metrics["held_out_binding_correct_rate"] = positive["held_out_binding_correct_rate"]
    metrics["negative_refusal_rate"] = negative["refusal_rate"]
    metrics["parameterized_confidences"] = param_confidences

    cert = {
        "certificate_id": "ARM-DIFFERENTIATION-CONFIDENCE-FLOW-CERTIFICATE-v1",
        "experiment_id": EXPERIMENT_ID,
        "checks": checks,
        "metrics": metrics,
        "certificate_overall": overall,
    }
    out = EXPERIMENT_DIR / "raw_certificate"
    cert_sha = write_json(out / "certificate.json", cert)
    acct_sha = write_json(out / "accounting_trace.json", accounting)
    print(json.dumps({"certificate_overall": overall, "metrics": metrics,
                      "certificate_sha256": cert_sha, "accounting_sha256": acct_sha}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

`C8_PROMOTABILITY-REGRESSION` is not part of the driver: EXECUTE runs `PYTHONPATH=src python -m unittest discover -s tests -v` and `python -m compileall -q src scripts` directly and records their exit codes as C8.

## 8. Freeze artifacts and identities

`freeze_artifacts` (exact repository-relative files; hashed into `freeze.json.artifact_hashes`):

| path | sha256 at DESIGN |
| --- | --- |
| `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` | `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` |
| `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/models.py` | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` |
| `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/registry.py` | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` |
| `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py` | `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf` |
| `src/spider/models.py` | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` |
| `src/spider/registry.py` | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` |
| `src/spider/__init__.py` | `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77` |
| `tests/test_kernel.py` | `ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6` |

`src/spider/kernel.py` is deliberately NOT a freeze artifact: EXECUTE replaces its content. Its pre-install identity (git blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50`, sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`, at git HEAD `f23063945fa5cb08943e5b15a90755b390047361`) is recorded as `B-SHIPPED-PRE-INSTALL`, and its required post-install identity (blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, sha256 `718efa6a...`) is pinned by decision-rule C1. The carrier's `models.py`/`registry.py` are byte-identical to the shipped ones (verified by hash), so the only production module whose content changes is `kernel.py`.

## 9. Decision rule and outcome mapping

Gating checks C1-C8 and the OVERALL_OUTCOME table are stated in `spec.json#decision_rule`. Summary: SUPPORTS = C1-C8 all PASS; FALSIFIES = C1/C5/C7 pass (real install, sane instrument) but any of C2/C3/C4/C6/C8 fails; MEASUREMENT_INVALID = C1 (identity/binding/frozen-artifact), C5 (accounting) or C7 (instrument sensitivity) fails; BLOCKED = prerequisite/environment failure. Measurement-invalid status never encodes a scientific negative. C4's per-case statuses must be reported exactly (no `EXPLORE` relabelled as `UNKNOWN`).

## 10. Product consequences, promotion rule and no-residue

Positive: on independent audit PASS the DIRECTOR may advance `C-PARAM-INHERIT` toward PRODUCT_CORE with `promote_to_product=true` (finalize_lane requires a PASS audit, the Product lane and promotion intent); the pinned promotion path applies ONLY the audited `src/` + `tests/` delta. EXECUTE does NOT self-promote and does not set claim status. Negative: no promotion; the `src/`+`tests/` delta is reverted to `B-SHIPPED-PRE-INSTALL`; `C-PARAM-INHERIT` retains its prior effective status (EXPERIMENTAL); B1 remains open and the expensive four-arm benchmark must not be funded.

## 11. Threats to validity and representation loss

- Determinism/ceiling: because the installed bytes are pinned to the audited carrier, the positive certificate is deterministic; the treatment's own 6/6 is not the discriminator. The discriminating contrast is treatment 6/6 at confidence 0.9 vs `B-LITERAL-KERNEL` 0/6 at confidence 0.5, plus the identity (C1) and drift branches. A treatment-only ceiling would be a null instrument; it is not used as one here.
- Synthetic bank: the fixture is a deterministic synthetic family bank, not real Web traffic; it can certify capability/safety/promotability but not external validity, cost savings or generalization to free-form payloads.
- Support semantics: reserve is that the carrier refuses identifiers outside the inferred grammar; the packet does not claim support generalization for free-form payloads (it inherits the parent's `do_not_assume`).
- Instrument-created-during-EXECUTE risk is removed by embedding the exact driver text in section 7; the fixture is frozen by hash.
- v2 design review: freezing requires an independent `design_review.json` PASS; the recurring `opencode/exo-free` reviewer failure (fingerprint `3b9ff5e4e9e73f23e368efb4`) is an operational dependency outside this DESIGN's control and would surface as an operational failure, not a scientific negative.

## 12. Estimated cost and expected information gain

Low cost (standard-library determinism, <60s at EXECUTE, no model/browser/network/GPU). High program value: it discharges the mandatory B1 prerequisite with an explicit confidence-flow and safe-refusal gate, exercises the pinned promotion path, and records the pinned carrier blob/sha256 (`b15ed848` / `718efa6a`) for the later four-arm benchmark. Claim-level gain is bounded and disclosed as a durability/integration confirmation, not new causal evidence.

## 13. Provenance and environment

- git HEAD at DESIGN: `f23063945fa5cb08943e5b15a90755b390047361`.
- Python 3.12.15; git 2.55.0; no network/model use.
- request: `research/experiments/EXP-PRODUCT-38109268122/request.json` (request_hash `86cb35ff6f5c7bb7dbe5e649a800dbb765c22d585cc6418116c7279a6d0dcdb6`), `director_mandate.cycle_id` `38108882486`.
- claim registry sha256 referenced by request: `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b`.
- evidence sources: `EXP-PRODUCT-37973256064` (audited live path), `EXP-PRODUCT-37950607128` (arm-differentiation certificate + frozen fixture), `EXP-PRODUCT-37989728440` (handoff + vendored carrier).
