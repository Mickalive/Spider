#!/usr/bin/env python3
"""FROZEN RUNNER for EXP-PRODUCT-38180719830 (embedded verbatim in prereg.md).

Deterministic, stdlib-only, credential-free installation + identity + binding
certificate for the audited parameterized carrier at the shipping kernel path
src/spider/kernel.py. Phases -> decision-rule clauses D0..D4:

  P0  pre-install identity baseline                         (D0)
  P1  B-LITERAL-KERNEL ablation: literal kernel from git   (D4)
  P2  byte-identical carrier installation                  (D0)
  P3  identity certificate (installed file == git blob)    (D0)
  P4  positive certificate: induction -> EXECUTABLE@0.9 ->
      fixture 200 -> verify true on UNSEEN held-out id     (D1)
  P5  negative certificate: out-of-support / missing-param
      / wrong-intent / no-applicable-mechanism: recorded reason
      + null bound action; exactly UNKNOWN for
      no-applicable-mechanism                              (D2)
  P6  honest inherited-path counters: retrieval_calls,
      verification_calls, repair_attempts == invocation
      transcript; model_calls == 0, model_tokens == 0      (D3)
  P7  controls: PC-EXACT-REPLAY (training ids resolve
      EXECUTABLE) + regression tests/test_kernel.py pass   (D4)
  P8  freeze binding (V8): sha256(prereg.md) == freeze.json
      hash; runner source == FROZEN RUNNER block of the
      hash-bound prereg; freeze artifact hashes match       (V8)

Stop trigger (mandate): if the carrier cannot be installed byte-identically
(git object missing) or the installed identity mismatches, record the exact
promotion blocker and exit BLOCKED; never test a substituted carrier.

Env overrides (hermetic dry-run only, never change certificate logic):
  EXP_CARRIER_SRC : git:<blob> (default) or file:<path>
  EXP_LITERAL_SRC : git:<blob> (default) or file:<path>
  EXP_TARGET_ROOT : repo root containing src/spider (default: auto-detected)

Output JSON: status (COMPLETE|BLOCKED), outcome (SUPPORTS|FALSIFIES), one
certificate clause per decision-rule check, identities, counters, observations.
"""
from __future__ import annotations

import hashlib
import http.server
import json
import os
import re
import shutil
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
HELD_OUT_IN_SUPPORT = "item-007"   # unseen; single-digit suffix -> inside induced support
OOS_IDS = ["item-010", "item-999", "item-xyz"]  # outside ^item\-00[0-9]{1}$ support
WRONG_INTENT = "delete_item"
NEVER_SEEN_INTENT = "never_seen_intent"
CTX = {"resource_type": "item", "authenticated": True}


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
    def do_GET(self):
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


def mk_obs(intent, ident, port):
    url = f"http://127.0.0.1:{port}/api/items/{ident}"
    return {
        "intent": intent,
        "state": dict(CTX),
        "action": {"method": "GET", "url": url},
        "next_state": {"type": "item", "id": ident, "data": "res:" + ident},
        "success": True,
        "provenance": {"exp": "EXP-PRODUCT-38180719830", "role": "induction"},
    }


def make_pkg(target_pkg: Path, kernel_bytes: bytes, models: bytes, registry: bytes,
             init: bytes) -> None:
    target_pkg.mkdir(parents=True, exist_ok=True)
    (target_pkg / "kernel.py").write_bytes(kernel_bytes)
    (target_pkg / "models.py").write_bytes(models)
    (target_pkg / "registry.py").write_bytes(registry)
    (target_pkg / "__init__.py").write_bytes(init)


def drop_module(name: str) -> None:
    sys.modules.pop(name, None)


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
    exp = REPO_ROOT / "research/experiments/EXP-PRODUCT-38180719830"
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
        "reason": "hash-bound prereg; running source == FROZEN RUNNER block; freeze artifact hashes intact",
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
        "experiment_id": "EXP-PRODUCT-38180719830",
        "lane": "product",
        "certificate": {},
        "identities": {},
        "counters_transcript": [],
        "observations": [],
        "unresolved": [],
    }

    kernel_path = REPO_ROOT / "src/spider/kernel.py"
    models_bytes = (REPO_ROOT / "src/spider/models.py").read_bytes()
    registry_bytes = (REPO_ROOT / "src/spider/registry.py").read_bytes()
    init_bytes = (REPO_ROOT / "src/spider/__init__.py").read_bytes()

    carrier_src = os.environ.get("EXP_CARRIER_SRC", f"git:{CARRIER_BLOB}")
    literal_src = os.environ.get("EXP_LITERAL_SRC", f"git:{LITERAL_BLOB}")
    result["run_config"] = {
        "repo_root": str(REPO_ROOT),
        "carrier_src": carrier_src,
        "literal_src": literal_src,
        "probe_mode": bool(os.environ.get("EXP_PROBE_MODE")),
        "sources_are_git": carrier_src.startswith("git:") and literal_src.startswith("git:"),
    }

    # ---- P8 freeze binding first (mandatory at EXECUTE; probe mode records UNBOUND-RUN) ----
    if not v8_freeze_binding(result):
        return result

    # ---- P0 pre-install identity baseline ----
    pre = sha256_bytes(kernel_path.read_bytes())
    result["identities"]["pre_install_sha256"] = pre
    result["identities"]["pre_install_expected"] = LITERAL_SHA256
    result["identities"]["pre_install_git_blob"] = LITERAL_BLOB
    result["observations"].append(
        {"type": "pre_install_identity", "sha256": pre, "expected": LITERAL_SHA256}
    )
    if pre not in (LITERAL_SHA256, CARRIER_SHA256):
        result["certificate"]["D0_IDENTITY"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "pre-install src/spider/kernel.py is neither the literal ("
                      + LITERAL_SHA256 + ") nor the already-installed carrier ("
                      + CARRIER_SHA256 + "); shipping path in unknown state",
        }
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result

    # ---- P1 B-LITERAL-KERNEL ablation (temp package; repo untouched) ----
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
            import spider as lit  # literal kernel package (audited models/registry)
            has_param_path = hasattr(lit.SpiderKernel, "distill_parameterized")
            sys.path.remove(td)
            for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
                drop_module(m)
            result["certificate"]["D4_CONTROLS"] = {
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
        result["certificate"]["D4_CONTROLS"] = {
            "literal_ablation": {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        }
        result["status"] = "BLOCKED"
        return result

    # ---- P2 install carrier byte-identically; P3 identity certificate ----
    try:
        carrier_bytes = read_source(carrier_src)
        carrier_sha = sha256_bytes(carrier_bytes)
        result["identities"]["carrier_source_sha256"] = carrier_sha
        result["identities"]["carrier_git_blob"] = CARRIER_BLOB
        if carrier_sha != CARRIER_SHA256:
            result["certificate"]["D0_IDENTITY"] = {
                "status": "FAIL",
                "reason": "carrier source sha mismatch (got "
                          + carrier_sha + ", expected " + CARRIER_SHA256 + ")",
            }
            result["status"] = "BLOCKED"   # stop trigger: never test a substituted carrier
            result["outcome"] = "MEASUREMENT_INVALID"
            return result
        kernel_path.write_bytes(carrier_bytes)
        post = sha256_bytes(kernel_path.read_bytes())
        result["identities"]["post_install_sha256"] = post
        result["identities"]["post_install_git_blob"] = CARRIER_BLOB
        if post != CARRIER_SHA256:
            result["certificate"]["D0_IDENTITY"] = {
                "status": "FAIL",
                "reason": "installed kernel sha mismatch (got " + post + ")",
            }
            result["status"] = "BLOCKED"   # stop trigger
            result["outcome"] = "MEASUREMENT_INVALID"
            return result
        result["certificate"]["D0_IDENTITY"] = {
            "status": "PASS",
            "reason": "installed file byte-identical to frozen carrier git blob "
                      + CARRIER_BLOB + " (sha256 " + CARRIER_SHA256 + ")",
        }
    except Exception as exc:
        result["certificate"]["D0_IDENTITY"] = {
            "status": "MEASUREMENT_INVALID", "reason": str(exc)
        }
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result

    # ---- P4/P5/P6/P7 against INSTALLED package ----
    sys.path.insert(0, str(REPO_ROOT / "src"))
    for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
        drop_module(m)
    from spider.kernel import SpiderKernel, TrajectoryCounters
    from spider.models import Observation, ResolutionStatus
    from spider.registry import MechanismRegistry

    fixture, port = start_fixture()
    observations = [Observation(**mk_obs(INTENT, ident, port)) for ident in TRAIN_IDS]
    transcript: list[dict] = []

    try:
        with tempfile.TemporaryDirectory() as td:
            reg = MechanismRegistry(Path(td) / "mechanisms.jsonl")
            counters = TrajectoryCounters()
            kernel = SpiderKernel(reg, min_confidence=0.8, counters=counters)
            mech = kernel.distill_parameterized(observations)
            reg.upsert(mech)
            slots = mech.parameter_slots
            support = mech.verification_rule["parameter_supports"]
            result["observations"].append(
                {"type": "derived", "mechanism_id": mech.mechanism_id, "slots": slots,
                 "support": support, "confidence": mech.confidence}
            )

            # ---- D1 positive certificate on UNSEEN held-out identifier ----
            params = {s: HELD_OUT_IN_SUPPORT for s in slots}
            transcript.append({"op": "resolve", "args": [INTENT, HELD_OUT_IN_SUPPORT]})
            res = kernel.resolve(INTENT, CTX, params)
            pos_binding_ok = (
                res.status == ResolutionStatus.EXECUTABLE
                and res.bound_action is not None
                and HELD_OUT_IN_SUPPORT in res.bound_action["url"]
                and res.confidence == 0.9
            )
            status, body = (0, {})
            if res.bound_action:
                transcript.append({"op": "execute", "url": res.bound_action["url"]})
                status, body = execute(res.bound_action)
            transcript.append({"op": "verify", "args": [res.mechanism_id]})
            verify_ok = kernel.verify(res.mechanism_id, body, params) if status == 200 else False
            result["certificate"]["D1_POSITIVE"] = {
                "status": "PASS" if (pos_binding_ok and status == 200 and verify_ok) else "FAIL",
                "resolution_status": res.status.value,
                "resolution_confidence": res.confidence,
                "bound_action": res.bound_action,
                "fixture_status": status,
                "verify": verify_ok,
                "held_out": HELD_OUT_IN_SUPPORT,
                "reason": ">=3 induction observations; unseen held-out id bound EXECUTABLE@0.9; "
                          "fixture 200; verify true",
            }

            # ---- D2 negative certificate ----
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
            transcript.append({"op": "resolve", "args": [WRONG_INTENT, HELD_OUT_IN_SUPPORT]})
            r = kernel.resolve(WRONG_INTENT, CTX, params)
            negatives.append({"case": "wrong_intent", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
            transcript.append({"op": "resolve", "args": [NEVER_SEEN_INTENT, "<none>"]})
            r = kernel.resolve(NEVER_SEEN_INTENT, {}, {})
            negatives.append({"case": "no_applicable_mechanism", "status": r.status.value,
                              "reason": r.reason, "bound_action": r.bound_action})
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
            result["certificate"]["D2_NEGATIVE"] = {
                "status": "PASS" if (all_refused and unknown_exact
                                     and oos_explore and missing_explore) else "FAIL",
                "negatives": negatives,
                "reason": "every refusal: recorded reason + null bound action; out-of-support/"
                          "missing-parameter EXPLORE; no-applicable-mechanism exactly UNKNOWN",
            }

            # ---- D3 honest counters vs invocation transcript ----
            counters_before = counters.as_dict()
            transcript.append({"op": "rebind", "args": [INTENT, HELD_OUT_IN_SUPPORT]})
            _ = kernel.rebind(INTENT, CTX, params)
            counters_after = counters.as_dict()
            expected_retrieval = sum(1 for t in transcript if t["op"] in ("resolve", "rebind"))
            expected_verify = sum(1 for t in transcript if t["op"] == "verify")
            expected_repair = sum(1 for t in transcript if t["op"] == "rebind")
            counters_ok = (
                counters_after["retrieval_calls"] == counters_before["retrieval_calls"] + 1
                and counters_after["repair_attempts"] == counters_before["repair_attempts"] + 1
                and counters_after["retrieval_calls"] == expected_retrieval
                and counters_after["verification_calls"] == expected_verify
                and counters_after["repair_attempts"] == expected_repair
                and counters_after["model_calls"] == 0
                and counters_after["model_tokens"] == 0
            )
            result["certificate"]["D3_COUNTERS"] = {
                "status": "PASS" if counters_ok else "FAIL",
                "counters_after": counters_after,
                "expected_from_transcript": {
                    "retrieval_calls": expected_retrieval,
                    "verification_calls": expected_verify,
                    "repair_attempts": expected_repair,
                },
                "reason": "retrieval_calls/verification_calls/repair_attempts equal the invocation "
                          "transcript; model_calls=0, model_tokens=0 (no model anywhere on path)",
            }
            result["counters_transcript"] = transcript
            result["counters"] = counters_after

            # ---- D4 controls: PC-EXACT-REPLAY ----
            replay = []
            for ident in TRAIN_IDS:
                transcript.append({"op": "resolve", "args": [INTENT, ident]})
                r = kernel.resolve(INTENT, CTX, {s: ident for s in slots})
                replay.append({"id": ident, "status": r.status.value})
            replay_ok = all(r["status"] == "EXECUTABLE" for r in replay)
            result["certificate"]["D4_CONTROLS"]["pc_exact_replay"] = {
                "status": "PASS" if replay_ok else "FAIL",
                "replay": replay,
                "reason": "all training ids re-resolve EXECUTABLE on installed carrier",
            }
            fixture.shutdown()
    except Exception as exc:
        fixture.shutdown()
        result["certificate"]["D0_IDENTITY"] = result["certificate"].get(
            "D0_IDENTITY", {"status": "MEASUREMENT_INVALID", "reason": "unknown"})
        result["certificate"]["CORE"] = {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        result["status"] = "BLOCKED"
        result["outcome"] = "MEASUREMENT_INVALID"
        return result

    # ---- D4 controls: regression on installed carrier ----
    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test_*.py")
    tresult = unittest.TextTestRunner(verbosity=0).run(suite)
    result["certificate"]["D4_CONTROLS"]["regression"] = {
        "status": "PASS" if (tresult.wasSuccessful() and tresult.testsRun >= 3) else "FAIL",
        "tests_run": tresult.testsRun,
        "failures": len(tresult.failures),
        "errors": len(tresult.errors),
        "reason": "existing test_kernel suite passes on installed carrier",
    }

    clauses = [result["certificate"][k] for k in ("D0_IDENTITY", "D1_POSITIVE",
                                                  "D2_NEGATIVE", "D3_COUNTERS")]
    clauses.append(
        {"status": result["certificate"]["D4_CONTROLS"].get("pc_exact_replay", {}).get("status"),
         "literal": result["certificate"]["D4_CONTROLS"].get("literal_ablation", {}).get("status"),
         "regression": result["certificate"]["D4_CONTROLS"].get("regression", {}).get("status")}
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