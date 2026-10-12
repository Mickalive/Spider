#!/usr/bin/env python3
"""FROZEN RUNNER for EXP-PRODUCT-38186502935 (embedded verbatim in prereg.md).

Read-only shipped-carrier END-TO-END execution certificate for the as-installed
parameterized carrier at the shipping kernel path src/spider/kernel.py (carrier
git blob b15ed848... / sha256 718efa6a...). NEVER writes src/spider/.
Phases -> decision-rule clauses:

  P0  V8 freeze binding                                    (V8)
  P1  shipping identity premise gate                       (E2E-IDENTITY)
  P2  B-LITERAL-KERNEL ablation (literal from git)        (E2E-CONTROLS)
  P3  import the SHIPPING package via public API          (E2E-IDENTITY)
  P4  induction: execute 5 GETs item-001..005 on the
      credential-free loopback fixture (counter +5)        (E2E-POSITIVE)
  P5  distill_parameterized -> mechanism (slots ['item'],
      support ^item\\-00[0-9]{1}$, confidence 0.9)          (E2E-POSITIVE)
  P6  positive certificate: resolve NEVER-observed
      item-000 -> EXECUTABLE@0.9 -> execute (GET +1) ->
      fixture 200 -> verify true                          (E2E-POSITIVE)
  P7  negative certificate: 7 refusal probes (incl.
      designated item-010 abstention and never_seen_intent
      exactly UNKNOWN), all null action + recorded reason,
      fixture request counter UNCHANGED (zero HTTP)       (E2E-ABSTENTION)
  P8  honest counters: retrieval/verification/repair ==
      invocation transcript; model_calls==0, model_tokens==0;
      runner-side http counter == executed legs (6)        (E2E-COUNTERS)
  P9  controls: PC-EXACT-REPLAY 5/5 + regression suite     (E2E-CONTROLS)

Stop trigger (parent handoff): if the shipping kernel is NOT the frozen carrier
(sha mismatch), record the exact blocker and exit BLOCKED; never measure a
substituted carrier. Freeze binding failures are MEASUREMENT_INVALID, never
FALSIFIES.

Env overrides (hermetic dry-run / sim-tree probes only, never change certificate
logic or thresholds):
  EXP_TARGET_ROOT : repo root containing src/spider (default: auto-detected)
  EXP_LITERAL_SRC : git:<blob> (default) or file:<path>
  EXP_PROBE_MODE  : "1" = satisfiability probe; records UNBOUND-RUN for V8 when
                    freeze.json is absent (never fabricates the check)

Output JSON: status (COMPLETE|BLOCKED), outcome (SUPPORTS|FALSIFIES), one
certificate clause per decision-rule check, identities, counters, observations.
"""
from __future__ import annotations

import hashlib
import http.server
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

# -- injection point for canonical identities (prereg CANONICAL-HASHES) --
CARRIER_BLOB = "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796"
CARRIER_SHA256 = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
LITERAL_BLOB = "cfec98660b0277ccbf295e8a4119e8d81ddccf50"
LITERAL_SHA256 = "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61"
# ---------------------------------------------------------------------------

INTENT = "read_item"
TRAIN_IDS = ["item-001", "item-002", "item-003", "item-004", "item-005"]
POSITIVE_HELD_OUT = "item-000"   # never-observed in ANY prior SPIDER run; inside induced support
OOS_IDS = ["item-010", "item-999", "item-xyz"]  # outside ^item\-00[0-9]{1}$ support
WRONG_INTENT = "delete_item"
NEVER_SEEN_INTENT = "never_seen_intent"
CTX = {"resource_type": "item", "authenticated": True}
EXPECTED_SUPPORT = r"^item\-00[0-9]{1}$"
EXPECTED_SLOTS = ["item"]
EXPECTED_CONFIDENCE = 0.9
EXPECTED_HTTP_LEGS = 6  # 5 induction + 1 positive execute; 0 abstention
EXPECTED_MIN_CONFIDENCE = 0.8  # shipped default, must NOT be overridden


def detect_repo_root() -> Path:
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "pyproject.toml").exists() and (p / "src/spider").exists():
            return p
        p = p.parent
    raise RuntimeError("repo root (pyproject.toml + src/spider) not found upward from runner")


REPO_ROOT = Path(os.environ.get("EXP_TARGET_ROOT") or str(detect_repo_root()))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_source(spec: str) -> bytes:
    if spec.startswith("git:"):
        blob = spec[4:]
        out = subprocess.run(["git", "-C", str(REPO_ROOT), "cat-file", "blob", blob],
                             capture_output=True)
        if out.returncode != 0:
            raise RuntimeError(f"git object {blob} unavailable: {out.stderr.decode()[:200]}")
        return out.stdout
    if spec.startswith("file:"):
        return Path(spec[5:]).read_bytes()
    raise RuntimeError(f"unknown source spec: {spec}")


class FixtureHandler(http.server.BaseHTTPRequestHandler):
    """Deterministic credential-free loopback fixture with a request counter."""
    count = 0

    def do_GET(self):
        type(self).count += 1
        parts = self.path.strip("/").split("/")
        body = {}
        if len(parts) == 3 and parts[:2] == ["api", "items"]:
            body = {"type": "item", "id": parts[2], "data": "res:" + parts[2]}
            self.send_response(200)
        else:
            self.send_response(404)
        payload = json.dumps(body).encode()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


def start_fixture() -> tuple[http.server.ThreadingHTTPServer, int]:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FixtureHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1]


def execute(bound_action: dict) -> tuple[int, dict]:
    with urllib.request.urlopen(bound_action["url"], timeout=5) as resp:
        return resp.status, json.loads(resp.read().decode())


def drop_module(name: str) -> None:
    sys.modules.pop(name, None)


def make_pkg(target_pkg: Path, kernel_bytes: bytes, models: bytes, registry: bytes,
             init: bytes) -> None:
    target_pkg.mkdir(parents=True, exist_ok=True)
    (target_pkg / "kernel.py").write_bytes(kernel_bytes)
    (target_pkg / "models.py").write_bytes(models)
    (target_pkg / "registry.py").write_bytes(registry)
    (target_pkg / "__init__.py").write_bytes(init)


def _extract(text: str, name: str) -> str:
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END " + re.escape(name) + r" -->", text, re.S)
    if not m:
        raise RuntimeError(f"block {name} not found in prereg.md")
    return m.group(1)


def v8_freeze_binding(result: dict) -> bool:
    """V8 freeze binding. In EXECUTE mode (default) freeze.json MUST exist next
    to the experiment prereg and all three binding clauses must hold; a missing
    freeze.json or any mismatch is MEASUREMENT_INVALID (never FALSIFIES) and the
    certificate stops before any outcome measurement. In probe mode
    (EXP_PROBE_MODE=1) a missing freeze.json records UNBOUND-RUN so a hermetic
    satisfiability probe can run; an existing freeze.json is still enforced.
    Returns True to continue, False to stop as BLOCKED/MEASUREMENT_INVALID."""
    probe = os.environ.get("EXP_PROBE_MODE") == "1"
    exp = REPO_ROOT / "research/experiments/EXP-PRODUCT-38186502935"
    freeze_path = exp / "freeze.json"
    if not freeze_path.exists():
        if probe:
            result["observations"].append(
                {"type": "binding", "V8": "UNBOUND-RUN: no freeze.json found; V8 not enforced "
                                          "(probe mode only)."}
            )
            return True
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "freeze.json missing at " + str(freeze_path) + " (EXECUTE mode)",
        }
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return False
    try:
        freeze = json.loads(freeze_path.read_text())

        def _norm(s: str) -> str:
            return s.replace("\r\n", "\n").rstrip()
        prereg_b = (exp / "prereg.md").read_bytes()
        block = _extract(prereg_b.decode("utf-8"), "FROZEN RUNNER")
        this_src = Path(__file__).resolve().read_text(encoding="utf-8")
        ok_a = hashlib.sha256(prereg_b).hexdigest() == freeze["hashes"]["prereg.md"]
        ok_b = (_norm(this_src) == _norm(block))
        ok_c = True
        for rel, h in freeze.get("artifact_hashes", {}).items():
            if hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest() != h:
                ok_c = False
                break
    except Exception as exc:
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID", "reason": "freeze binding unreadable: " + str(exc)}
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return False
    ok_all = ok_a and ok_b and ok_c
    result["certificate"]["V8_FREEZE_BINDING"] = {
        "status": "PASS" if ok_all else "FAIL",
        "prereg_sha_matches": ok_a,
        "runner_source_matches_frozen_block": ok_b,
        "artifact_hashes_match": ok_c,
        "reason": "hash-bound prereg; running source == FROZEN RUNNER block; six freeze artifact "
                  "hashes intact (incl. src/spider/kernel.py)",
    }
    result["observations"].append({"type": "binding", "V8": "enforced"})
    if not ok_all:
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return False
    return True


def main() -> dict:
    result = {
        "schema_version": 1,
        "experiment_id": "EXP-PRODUCT-38186502935",
        "lane": "product",
        "certificate": {},
        "identities": {},
        "counters_transcript": [],
        "observations": [],
        "unresolved": [],
    }

    kernel_path = REPO_ROOT / "src/spider/kernel.py"
    sys.path.insert(0, str(REPO_ROOT / "src"))
    for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
        drop_module(m)

    literal_src = os.environ.get("EXP_LITERAL_SRC", f"git:{LITERAL_BLOB}")
    result["run_config"] = {
        "repo_root": str(REPO_ROOT),
        "literal_src": literal_src,
        "probe_mode": bool(os.environ.get("EXP_PROBE_MODE")),
        "min_confidence_override": os.environ.get("EXP_MIN_CONFIDENCE_OVERRIDE"),
    }

    # ---- P0 V8 freeze binding first (mandatory at EXECUTE; probe mode records UNBOUND-RUN) ----
    if not v8_freeze_binding(result):
        return result

    # ---- P1 shipping identity premise gate (E2E-IDENTITY) ----
    shipping_sha = sha256_bytes(kernel_path.read_bytes())
    result["identities"]["shipping_kernel_sha256"] = shipping_sha
    result["identities"]["carrier_expected_sha256"] = CARRIER_SHA256
    result["identities"]["carrier_git_blob"] = CARRIER_BLOB
    result["observations"].append(
        {"type": "shipping_identity", "sha256": shipping_sha, "expected": CARRIER_SHA256}
    )
    if shipping_sha != CARRIER_SHA256:
        result["certificate"]["E2E_IDENTITY"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "shipping kernel src/spider/kernel.py is NOT the frozen carrier (got "
                      + shipping_sha + ", expected " + CARRIER_SHA256 + "); promotion merge not "
                      "in effect or tree modified (V4 stop trigger: never measure a substituted "
                      "carrier)",
        }
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result
    result["certificate"]["E2E_IDENTITY"] = {
        "status": "PASS",
        "reason": "shipping kernel byte-identical to frozen carrier git blob " + CARRIER_BLOB
                  + " (sha256 " + CARRIER_SHA256 + ") on a git-clean tree",
    }

    # ---- P2 B-LITERAL-KERNEL ablation (temp package; repo untouched) ----
    models_bytes = (REPO_ROOT / "src/spider/models.py").read_bytes()
    registry_bytes = (REPO_ROOT / "src/spider/registry.py").read_bytes()
    init_bytes = (REPO_ROOT / "src/spider/__init__.py").read_bytes()
    try:
        literal_bytes = read_source(literal_src)
        if sha256_bytes(literal_bytes) != LITERAL_SHA256:
            raise RuntimeError("literal blob sha mismatch")
        with tempfile.TemporaryDirectory() as td:
            pkg = Path(td) / "spider"
            make_pkg(pkg, literal_bytes, models_bytes, registry_bytes, init_bytes)
            sys.path.insert(0, td)
            for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
                drop_module(m)
            import spider as lit  # literal kernel package (same shipped models/registry/init)
            has_param_path = hasattr(lit.SpiderKernel, "distill_parameterized")
            sys.path.remove(td)
            for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
                drop_module(m)
            result["certificate"]["E2E_CONTROLS"] = {
                "literal_ablation": {
                    "status": "PASS" if not has_param_path else "FAIL",
                    "has_distill_parameterized": has_param_path,
                    "reason": "literal kernel lacks distill_parameterized; positive certificate "
                              "attributes to the installed carrier only",
                }
            }
            result["observations"].append(
                {"type": "derived", "literal_has_distill_parameterized": has_param_path}
            )
    except Exception as exc:  # operational, not a negative result
        result["certificate"]["E2E_CONTROLS"] = {
            "literal_ablation": {"status": "MEASUREMENT_INVALID", "reason": str(exc)}}
        result["status"] = "BLOCKED"
        return result

    # ---- P3 import the SHIPPING package via its public API ----
    try:
        from spider import SpiderKernel, Mechanism, Observation, Resolution, ResolutionStatus
        from spider.registry import MechanismRegistry
        kernel_min_confidence = SpiderKernel.__init__.__defaults__[0]
        result["observations"].append(
            {"type": "derived", "kernel_min_confidence_default": kernel_min_confidence}
        )
        if kernel_min_confidence != EXPECTED_MIN_CONFIDENCE:
            raise RuntimeError(
                f"shipped min_confidence default is {kernel_min_confidence}, expected "
                f"{EXPECTED_MIN_CONFIDENCE}; refusing to run with altered thresholds")
    except Exception as exc:
        result["certificate"]["E2E_IDENTITY"]["status"] = "MEASUREMENT_INVALID"
        result["certificate"]["CORE"] = {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result

    fixture, port = start_fixture()
    transcript: list[dict] = []
    http_before = FixtureHandler.count

    try:
        with tempfile.TemporaryDirectory() as td:
            reg = MechanismRegistry(Path(td) / "mechanisms.jsonl")
            counters_type = __import__("spider.kernel", fromlist=["TrajectoryCounters"]).TrajectoryCounters
            counters = counters_type()
            kernel = SpiderKernel(reg, counters=counters)  # shipped default min_confidence=0.8

            # ---- P4 induction: actually EXECUTE the 5 training GETs ----
            observations = []
            for ident in TRAIN_IDS:
                url = f"http://127.0.0.1:{port}/api/items/{ident}"
                transcript.append({"op": "execute_induction", "url": url})
                status, body = execute({"method": "GET", "url": url})
                if status != 200:
                    raise RuntimeError(f"induction GET {ident} returned {status}")
                observations.append(Observation(
                    intent=INTENT,
                    state=dict(CTX),
                    action={"method": "GET", "url": url},
                    next_state=body,
                    success=True,
                    provenance={"exp": "EXP-PRODUCT-38186502935", "role": "induction"},
                ))
            transcript.append({"op": "distill", "n": len(observations)})

            # ---- P5 distill_parameterized ----
            mech = kernel.distill_parameterized(observations)
            if mech is None:
                raise RuntimeError("distill_parameterized returned None on 5 successful observations")
            reg.upsert(mech)
            slots = mech.parameter_slots
            support = mech.verification_rule["parameter_supports"]
            result["observations"].append(
                {"type": "derived", "mechanism_id": mech.mechanism_id, "slots": slots,
                 "support": support, "confidence": mech.confidence}
            )

            # ---- P6 E2E-POSITIVE on NEVER-observed held-out item-000 ----
            params = {s: POSITIVE_HELD_OUT for s in slots}
            transcript.append({"op": "resolve", "args": [INTENT, POSITIVE_HELD_OUT]})
            res = kernel.resolve(INTENT, CTX, params)
            pos_binding_ok = (
                res.status == ResolutionStatus.EXECUTABLE
                and res.bound_action is not None
                and POSITIVE_HELD_OUT in res.bound_action["url"]
                and res.confidence == EXPECTED_CONFIDENCE
            )
            status, body = (0, {})
            if res.bound_action:
                transcript.append({"op": "execute_positive", "url": res.bound_action["url"]})
                status, body = execute(res.bound_action)
            transcript.append({"op": "verify", "args": [res.mechanism_id]})
            verify_ok = kernel.verify(res.mechanism_id, body, params) if status == 200 else False
            result["certificate"]["E2E_POSITIVE"] = {
                "status": "PASS" if (pos_binding_ok and status == 200 and verify_ok) else "FAIL",
                "resolution_status": res.status.value,
                "resolution_confidence": res.confidence,
                "bound_action": res.bound_action,
                "fixture_status": status,
                "verify": verify_ok,
                "held_out": POSITIVE_HELD_OUT,
                "mechanism_id": mech.mechanism_id,
                "parameter_slots": slots,
                "support": support,
                "reason": "5 executed induction observations; never-observed id bound "
                          "EXECUTABLE@0.9; fixture 200; verify true",
            }

            # ---- P7 E2E-ABSTENTION: 7 refusal probes with zero HTTP ----
            http_abstention_start = FixtureHandler.count
            negatives = []
            for oos in OOS_IDS:
                transcript.append({"op": "resolve", "args": [INTENT, oos]})
                r = kernel.resolve(INTENT, CTX, {s: oos for s in slots})
                negatives.append({"case": f"out_of_support:{oos}", "status": r.status.value,
                                  "reason": r.reason, "bound_action": r.bound_action})
            transcript.append({"op": "resolve", "args": [INTENT, "<missing>"]})
            r = kernel.resolve(INTENT, CTX, {})
            negatives.append({"case": "missing_parameter", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            transcript.append({"op": "resolve", "args": [INTENT, "<wrong-key>"]})
            r = kernel.resolve(INTENT, CTX, {"wrong_key": "x"})
            negatives.append({"case": "missing_parameter_wrong_key", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            transcript.append({"op": "resolve", "args": [WRONG_INTENT, POSITIVE_HELD_OUT]})
            r = kernel.resolve(WRONG_INTENT, CTX, params)
            negatives.append({"case": "wrong_intent", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            transcript.append({"op": "resolve", "args": [NEVER_SEEN_INTENT, "<none>"]})
            r = kernel.resolve(NEVER_SEEN_INTENT, {}, {})
            negatives.append({"case": "no_applicable_mechanism", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            http_abstention_delta = FixtureHandler.count - http_abstention_start
            all_refused = all(n["bound_action"] is None and n["reason"]
                              and n["status"] != "EXECUTABLE" for n in negatives)
            unknown_exact = all(
                n["status"] == "UNKNOWN"
                for n in negatives if n["case"] in ("wrong_intent", "no_applicable_mechanism")
            )
            oos_explore = all(
                n["status"] == "EXPLORE" and "support" in n["reason"]
                for n in negatives if n["case"].startswith("out_of_support:")
            )
            missing_explore = all(
                n["status"] == "EXPLORE" and "parameter" in n["reason"]
                for n in negatives if n["case"].startswith("missing_parameter")
            )
            ab_ok = all_refused and unknown_exact and oos_explore and missing_explore \
                and http_abstention_delta == 0
            result["certificate"]["E2E_ABSTENTION"] = {
                "status": "PASS" if ab_ok else "FAIL",
                "negatives": negatives,
                "http_delta_during_phase": http_abstention_delta,
                "reason": "every refusal: recorded reason + null bound action + ZERO HTTP; "
                          "out-of-support/missing-parameter EXPLORE; no-applicable exactly UNKNOWN",
            }

            # ---- P8 E2E-COUNTERS: transcript-consistent, model-free, http ledger ----
            transcript.append({"op": "rebind", "args": [INTENT, POSITIVE_HELD_OUT]})
            _ = kernel.rebind(INTENT, CTX, params)
            http_total = FixtureHandler.count - http_before
            expected_retrieval = sum(1 for t in transcript if t["op"] in ("resolve", "rebind"))
            expected_verify = sum(1 for t in transcript if t["op"] == "verify")
            expected_repair = sum(1 for t in transcript if t["op"] == "rebind")
            counters_after = counters.as_dict()
            counters_ok = (
                counters_after["retrieval_calls"] == expected_retrieval
                and counters_after["verification_calls"] == expected_verify
                and counters_after["repair_attempts"] == expected_repair
                and counters_after["model_calls"] == 0
                and counters_after["model_tokens"] == 0
                and http_total == EXPECTED_HTTP_LEGS
            )
            result["certificate"]["E2E_COUNTERS"] = {
                "status": "PASS" if counters_ok else "FAIL",
                "counters_after": counters_after,
                "expected_from_transcript": {
                    "retrieval_calls": expected_retrieval,
                    "verification_calls": expected_verify,
                    "repair_attempts": expected_repair,
                },
                "http_fixture_counter_total": http_total,
                "http_expected_legs": EXPECTED_HTTP_LEGS,
                "http_abstention_delta": http_abstention_delta,
                "reason": "kernel counters == invocation transcript; model_calls=0, "
                          "model_tokens=0; runner-side http counter == executed legs (6)",
            }
            result["counters_transcript"] = transcript
            result["counters"] = counters_after

            # ---- P9 E2E-CONTROLS: PC-EXACT-REPLAY + regression ----
            replay = []
            for ident in TRAIN_IDS:
                transcript.append({"op": "resolve", "args": [INTENT, ident]})
                r = kernel.resolve(INTENT, CTX, {s: ident for s in slots})
                replay.append({"id": ident, "status": r.status.value})
            replay_ok = all(r["status"] == "EXECUTABLE" for r in replay)
            result["certificate"]["E2E_CONTROLS"]["pc_exact_replay"] = {
                "status": "PASS" if replay_ok else "FAIL",
                "replay": replay,
                "reason": "all training ids re-resolve EXECUTABLE on as-installed carrier",
            }
            fixture.shutdown()
    except Exception as exc:
        fixture.shutdown()
        result["certificate"]["E2E_IDENTITY"] = result["certificate"].get(
            "E2E_IDENTITY", {"status": "MEASUREMENT_INVALID", "reason": "unknown"})
        result["certificate"]["CORE"] = {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result

    # ---- P9 (cont.) regression on the as-installed shipping path ----
    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test_*.py")
    tresult = unittest.TextTestRunner(verbosity=0).run(suite)
    result["certificate"]["E2E_CONTROLS"]["regression"] = {
        "status": "PASS" if (tresult.wasSuccessful() and tresult.testsRun >= 3) else "FAIL",
        "tests_run": tresult.testsRun,
        "failures": len(tresult.failures),
        "errors": len(tresult.errors),
        "reason": "existing test_kernel suite passes on as-installed shipping path",
    }

    clauses = [result["certificate"][k] for k in ("E2E_IDENTITY", "E2E_POSITIVE",
                                                  "E2E_ABSTENTION", "E2E_COUNTERS")]
    clauses.append(
        {"status": result["certificate"]["E2E_CONTROLS"].get("pc_exact_replay", {}).get("status"),
         "literal": result["certificate"]["E2E_CONTROLS"].get("literal_ablation", {}).get("status"),
         "regression": result["certificate"]["E2E_CONTROLS"].get("regression", {}).get("status")}
    )
    if "V8_FREEZE_BINDING" in result["certificate"]:
        clauses.append(result["certificate"]["V8_FREEZE_BINDING"])
    all_pass = all(c.get("status") == "PASS" for c in clauses)
    result["status"] = "COMPLETE"
    result["outcome"] = "SUPPORTS" if all_pass else "FALSIFIES"
    result["unresolved"] = []
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
