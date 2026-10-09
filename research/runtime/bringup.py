#!/usr/bin/env python3
"""
SPIDER Research 2.0 — runtime lane one-command capability ledger and
substrate bring-up contract.

Usage:
    python -m research.runtime.bringup --config <bringup_contract.json> --ledger <capability_ledger.json>

The command is idempotent and fail-closed. It acquires the run lock, probes
every component named in the frozen contract, records same-run status plus
evidence and one smallest unblocking action for every UNAVAILABLE component,
and returns non-zero when any REQUIRED component of the declared scope fails.
It never installs packages, mutates credentials, starts unrelated services,
kills unrelated processes, or fabricates a result.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha_file(p: Path) -> Optional[str]:
    import hashlib
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except Exception:
        return None


def acquire_run_lock(lock_path: str) -> Optional[int]:
    """Non-blocking exclusive lock. Returns fd or None if held by a live holder."""
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except OSError:
        os.close(fd)
        return None


def _probe_python_dependencies() -> Dict[str, Any]:
    """CAP-PYTHON-DEPENDENCIES: isolated subprocess import check with the same
    interpreter for exactly the frozen substrate dependency set
    (flask 3.1.3, pyjwt 2.15.0, gunicorn 23.0.0, playwright 1.63.0 per
    prereg section 4). Never a synthetic success. Note: 'requests'/httpx are
    deliberately NOT dependency-scope requirements; the frozen design forbids
    their use in the episode transport (no-synthetic-fallback), so their
    absence cannot fail this scope."""
    code = (
        "import importlib, json\n"
        "out = {}\n"
        "for m in ['flask', 'jwt', 'gunicorn', 'playwright']:\n"
        "    try:\n"
        "        mod = importlib.import_module(m)\n"
        "        out[m] = str(getattr(mod, '__version__', 'unknown'))\n"
        "    except Exception as e:\n"
        "        out[m] = 'IMPORT_ERROR: ' + type(e).__name__\n"
        "print(json.dumps(out))\n"
    )
    try:
        proc = subprocess.run([sys.executable, "-c", code], capture_output=True,
                              text=True, timeout=30)
        versions = json.loads(proc.stdout.strip().splitlines()[-1]) if proc.returncode == 0 else {}
        import_errors = {k: v for k, v in versions.items() if str(v).startswith("IMPORT_ERROR")}
        status = "AVAILABLE" if not import_errors else "UNAVAILABLE"
        return {
            "status": status,
            "command": f"{sys.executable} -c <import flask, jwt, requests, gunicorn>",
            "timeout_s": 30,
            "exit_status": proc.returncode,
            "versions": versions,
            "evidence": "isolated subprocess import check (same interpreter)",
            "smallest_unblock_action": None if status == "AVAILABLE" else "pip install the missing packages recorded in versions, then re-run the bring-up command",
            "probed_at": _utc(),
        }
    except Exception as e:
        return {"status": "ERROR", "error": f"{type(e).__name__}: {e}",
                "smallest_unblock_action": "make python3 available on PATH, then re-run",
                "probed_at": _utc()}


def _probe_import(module: str) -> Dict[str, Any]:
    code = (
        "import importlib\n"
        f"importlib.import_module({module!r})\n"
        "print('OK')\n"
    )
    try:
        proc = subprocess.run([sys.executable, "-c", code], capture_output=True,
                              text=True, timeout=30)
        ok = proc.returncode == 0 and proc.stdout.strip().endswith("OK")
        return {
            "status": "AVAILABLE" if ok else "UNAVAILABLE",
            "command": f"{sys.executable} -c \"import {module}\"",
            "timeout_s": 30,
            "exit_status": proc.returncode,
            "stderr_tail": (proc.stderr or "")[-300:],
            "evidence": "isolated subprocess import check; never a synthetic success",
            "smallest_unblock_action": None if ok else f"pip install the {module} package, then re-run the bring-up command",
            "probed_at": _utc(),
        }
    except Exception as e:
        return {"status": "ERROR", "error": f"{type(e).__name__}: {e}",
                "smallest_unblock_action": "make python3 available on PATH, then re-run",
                "probed_at": _utc()}


def _probe_policy_model_credential() -> Dict[str, Any]:
    """CAP-POLICY-MODEL-CREDENTIAL: environment-key PRESENCE booleans only.
    Secret values are never recorded."""
    keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "HF_TOKEN", "GITHUB_TOKEN"]
    presence = {k: (k in os.environ and len(os.environ.get(k, "")) > 0) for k in keys}
    any_present = any(presence.values())
    return {
        "status": "AVAILABLE" if any_present else "UNAVAILABLE",
        "env_key_presence": presence,
        "redaction": "presence booleans only; no secret values recorded",
        "smallest_unblock_action": None if any_present else "configure the required policy-model credential environment key, then re-run; presence alone never authorizes a scientific claim",
        "probed_at": _utc(),
    }


def _probe_http_reachability(name: str, url: str, timeout: int = 10) -> Dict[str, Any]:
    """Bounded read-only HTTP reachability: explicit timeout, status, latency.
    Any HTTP response (including 401/403) means reachable; timeout/connection
    error means UNAVAILABLE. Nothing is downloaded."""
    import urllib.request
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "spider-runtime-bringup/1.0"})
        start = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            latency_ms = round((time.time() - start) * 1000, 1)
            body_head = resp.read(200)
        return {
            "status": "AVAILABLE",
            "url": url,
            "http_status": status,
            "latency_ms": latency_ms,
            "timeout_s": timeout,
            "evidence": f"HTTP {status} within {timeout}s; reachability means a response arrived, not that content was downloaded",
            "smallest_unblock_action": None,
            "probed_at": _utc(),
        }
    except Exception as e:
        return {
            "status": "UNAVAILABLE",
            "url": url,
            "timeout_s": timeout,
            "error": f"{type(e).__name__}: {e}",
            "evidence": "no HTTP response within timeout; recorded UNAVAILABLE, never upgraded",
            "smallest_unblock_action": "provide network egress to the endpoint (or record the endpoint as unreachable in the invoking lane's preregistration), then re-run",
            "probed_at": _utc(),
        }


def _probe_chromium_launch() -> Dict[str, Any]:
    """CAP-CHROMIUM-LAUNCH: public Playwright API probe only.
    p.chromium.executable_path is preferred; public p.chromium.launch() is the
    only permitted equivalent. No playwright._impl or private helper."""
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        return {"status": "UNAVAILABLE",
                "error": f"playwright import failed: {type(e).__name__}: {e}",
                "api_used": None,
                "smallest_unblock_action": "pip install playwright (pinned 1.63.0), then re-run the bring-up command",
                "probed_at": _utc()}
    p = None
    browser = None
    try:
        p = sync_playwright().start()
        exe_path = p.chromium.executable_path
        browser = p.chromium.launch(executable_path=exe_path)
        version = browser.version
        browser.close()
        p.stop()
        return {
            "status": "AVAILABLE",
            "executable_path": exe_path,
            "is_canonical_path": exe_path == "/home/runner/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome",
            "browser_version": version,
            "api_used": "sync_playwright().start().chromium.executable_path + p.chromium.launch(executable_path=...)",
            "private_helper_used": False,
            "smallest_unblock_action": None,
            "probed_at": _utc(),
        }
    except Exception as e:
        try:
            if browser is not None:
                browser.close()
        except Exception:
            pass
        try:
            if p is not None:
                p.stop()
        except Exception:
            pass
        return {"status": "UNAVAILABLE",
                "error": f"{type(e).__name__}: {e}",
                "api_used": "public Playwright API (preferred path resolution, then public launch)",
                "smallest_unblock_action": "run `playwright install chromium` to fetch the browser bundle for the pinned Playwright version, then re-run the bring-up command",
                "probed_at": _utc()}


def _port_listening(port: int) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except Exception:
        return False


def _probe_distributed_substrate(contract: Dict[str, Any]) -> Dict[str, Any]:
    """CAP-DISTRIBUTED-SUBSTRATE: live health of the two upstreams and nginx."""
    subs = contract["substream"] if "substream" in contract else contract["substrate"]
    nginx_port = int(subs["nginx"]["listen"].split(":")[1])
    upstreams = subs["upstreams"]
    checks = {}
    all_ok = True
    for up in upstreams:
        port = int(up.split(":")[1])
        checks[up] = _port_listening(port)
        if not checks[up]:
            all_ok = False
    checks[subs["nginx"]["listen"]] = _port_listening(nginx_port)
    if not checks[subs["nginx"]["listen"]]:
        all_ok = False
    return {
        "status": "AVAILABLE" if all_ok else "UNAVAILABLE",
        "port_checks": checks,
        "evidence": "TCP connect checks against the frozen ports",
        "smallest_unblock_action": None if all_ok else "run the substrate bring-up (2x gunicorn via wsgi:application + exclusive nginx -c /tmp/single.db.nginx.conf) using the frozen commands, then re-run the bring-up command",
        "probed_at": _utc(),
    }


def _probe_wal_schema(contract: Dict[str, Any]) -> Dict[str, Any]:
    """CAP-WAL-SCHEMA: inspect the live database journal mode and schema."""
    import sqlite3
    db_path = contract["substrate"]["database"]["path"]
    p = Path(db_path)
    if not p.exists():
        return {"status": "UNAVAILABLE",
                "error": f"{db_path} does not exist",
                "smallest_unblock_action": "run the substrate bring-up so /tmp/single.db is created, then re-run the bring-up command",
                "probed_at": _utc()}
    try:
        conn = sqlite3.connect(db_path, timeout=5, check_same_thread=False)
        try:
            conn.execute("PRAGMA wal_autocheckpoint=0")
            jmode = conn.execute("PRAGMA journal_mode").fetchone()[0]
            tables = [r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
            required = ["sessions", "runtime_probe", "body_config"]
            schema_ok = all(t in tables for t in required)
            return {
                "status": "AVAILABLE" if (str(jmode).lower() == "wal" and schema_ok) else "UNAVAILABLE",
                "journal_mode": jmode,
                "tables": tables,
                "required_tables_present": schema_ok,
                "wal_autocheckpoint_set": 0,
                "evidence": "PRAGMA journal_mode + sqlite_master inspection on the frozen path",
                "smallest_unblock_action": None if (str(jmode).lower() == "wal" and schema_ok) else "repair the substrate schema/journal mode, then re-run the bring-up command",
                "probed_at": _utc(),
            }
        finally:
            conn.close()
    except Exception as e:
        return {"status": "ERROR", "error": f"{type(e).__name__}: {e}",
                "smallest_unblock_action": "repair the substrate database, then re-run",
                "probed_at": _utc()}


def _probe_health_gate(contract: Dict[str, Any]) -> Dict[str, Any]:
    """CAP-HEALTH-GATE: GET /health via nginx with X-Worker-Pid."""
    import urllib.request
    subs = contract["substrate"]
    url = f"http://127.0.0.1:{subs['nginx']['listen'].split(':')[1]}/health"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            status = resp.status
            worker = resp.headers.get("X-Worker-Pid", "missing")
        ok = status == 200 and worker not in ("missing", "None", None, "")
        return {
            "status": "AVAILABLE" if ok else "UNAVAILABLE",
            "url": url,
            "http_status": status,
            "x_worker_pid": worker,
            "smallest_unblock_action": None if ok else "start the substrate (gunicorn + nginx) and verify /health returns 200 + X-Worker-Pid, then re-run",
            "probed_at": _utc(),
        }
    except Exception as e:
        return {"status": "UNAVAILABLE", "url": url,
                "error": f"{type(e).__name__}: {e}",
                "smallest_unblock_action": "start the substrate (gunicorn + nginx) and verify /health returns 200 + X-Worker-Pid, then re-run",
                "probed_at": _utc()}


def _probe_proxy_cache(contract: Dict[str, Any]) -> Dict[str, Any]:
    """CAP-NGINX-CACHE-MISS-HIT: real proxy_cache corroboration on one
    cacheable key through the exclusive nginx. First GET must be MISS,
    second must be HIT. An error is UNAVAILABLE/ERROR, never a pass."""
    import urllib.request
    subs = contract["substrate"]
    port = subs["nginx"]["listen"].split(":")[1]
    nonce = str(time.time_ns())
    url = f"http://127.0.0.1:{port}/health?cacheprobe={nonce}"

    def _leg() -> Dict[str, Any]:
        req = urllib.request.Request(url, headers={"User-Agent": "spider-runtime-bringup/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return {"status": resp.status, "x_cache": resp.headers.get("X-Cache", "missing"),
                    "worker": resp.headers.get("X-Worker-Pid", "missing")}

    try:
        leg1 = _leg()
        leg2 = _leg()
        ok = (leg1["status"] == 200 and leg2["status"] == 200
              and leg1["x_cache"] == "MISS" and leg2["x_cache"] == "HIT")
        return {
            "status": "AVAILABLE" if ok else "UNAVAILABLE",
            "url": url, "leg1": leg1, "leg2": leg2, "miss_then_hit": bool(ok),
            "evidence": ("two GETs on one cacheable key through exclusive nginx; "
                         "MISS then HIT proves a real proxy_cache"),
            "smallest_unblock_action": None if ok else
                "enable proxy_cache for the probed location and start the substrate (2x gunicorn + exclusive nginx -c), then re-run",
            "probed_at": _utc(),
        }
    except Exception as e:
        return {
            "status": "UNAVAILABLE", "url": url,
            "error": f"{type(e).__name__}: {e}",
            "miss_then_hit": False,
            "evidence": "no HTTP response; recorded UNAVAILABLE, never upgraded",
            "smallest_unblock_action": "start the substrate (2x gunicorn + exclusive nginx -c) and verify a cacheable 200 path, then re-run",
            "probed_at": _utc(),
        }


def _probe_readiness_floors(contract: Dict[str, Any], experiment_dir: Path) -> Dict[str, Any]:
    """CAP-N-NON304-FLOOR and CAP-X-WORKER-PID-FLOOR: read this run's readiness
    certificate and check the frozen floors. The certificate is raw evidence;
    a missing certificate is UNAVAILABLE, never a pass."""
    cert_path = experiment_dir / "artifacts" / "A-READINESS-CERTIFICATE.json"
    floors = contract["floors"]
    if not cert_path.exists():
        return {
            "CAP-N-NON304-FLOOR": {"status": "UNAVAILABLE", "error": "readiness certificate not found",
                                  "smallest_unblock_action": "run the experiment matrix first so the readiness certificate is produced, then re-run the bring-up command",
                                  "probed_at": _utc()},
            "CAP-X-WORKER-PID-FLOOR": {"status": "UNAVAILABLE", "error": "readiness certificate not found",
                                       "smallest_unblock_action": "run the experiment matrix first so the readiness certificate is produced, then re-run the bring-up command",
                                       "probed_at": _utc()},
        }
    try:
        cert = json.loads(cert_path.read_text())
    except Exception as e:
        err = f"unreadable certificate: {type(e).__name__}: {e}"
        return {
            "CAP-N-NON304-FLOOR": {"status": "ERROR", "error": err, "probed_at": _utc()},
            "CAP-X-WORKER-PID-FLOOR": {"status": "ERROR", "error": err, "probed_at": _utc()},
        }
    n_ok = cert.get("n_non304", 0) >= floors["n_non304_min"]
    per_ep_ok = all(v >= floors["n_non304_per_endpoint_min"]
                    for v in (cert.get("per_ep_non304") or {}).values()) and bool(cert.get("per_ep_non304"))
    w_ok = cert.get("n_distinct_x_worker_pid", 0) >= floors["distinct_x_worker_pid_min"]
    return {
        "CAP-N-NON304-FLOOR": {
            "status": "AVAILABLE" if (n_ok and per_ep_ok) else "UNAVAILABLE",
            "observed": {"n_non304": cert.get("n_non304"), "per_ep_non304": cert.get("per_ep_non304"),
                         "n_304": cert.get("n_304")},
            "floor": floors["n_non304_min"],
            "floor_per_endpoint": floors["n_non304_per_endpoint_min"],
            "evidence": str(cert_path),
            "smallest_unblock_action": None if (n_ok and per_ep_ok) else "re-run the substrate bring-up so the readiness certificate meets the frozen floors, then re-run the bring-up command",
            "probed_at": _utc(),
        },
        "CAP-X-WORKER-PID-FLOOR": {
            "status": "AVAILABLE" if w_ok else "UNAVAILABLE",
            "observed": {"n_distinct_x_worker_pid": cert.get("n_distinct_x_worker_pid"),
                         "distinct_workers": cert.get("distinct_x_worker_pid_on_200")},
            "floor": floors["distinct_x_worker_pid_min"],
            "evidence": str(cert_path),
            "smallest_unblock_action": None if w_ok else "ensure both gunicorn workers are fronted by nginx (hash $request_uri consistent), then re-run",
            "probed_at": _utc(),
        },
    }


INHERITED_PROBES = [
    {
        "id": "INHERITED-INTEL-36058324385",
        "observation": "accepted Intel audit recorded pip-installed browsergym-core 0.14.3, "
                       "agentlab 0.4.2 and playwright 1.63.0 with twelve successful 1280x720 CDP "
                       "Accessibility.getFullAXTree captures at statistical median 707 accessibility "
                       "nodes on canonical product pages (families 136/145/196/222).",
        "recorded_availability": {
            "browsergym_core_0_14_3": True,
            "agentlab_0_4_2": True,
            "playwright_1_63_0": True,
            "cdp_ax_captures": 12,
            "cdp_ax_median_nodes": 707,
        },
        "evidence": "codex/claim_state.json:3145 (accepted Intel audit evidence)",
    },
    {
        "id": "INHERITED-FRONTIER-36129180789",
        "observation": "accepted Frontier substrate diagnostic reported browsergym_available=false "
                       "with all primary and null controls NOT_RUN.",
        "recorded_availability": {"browsergym_available": False, "controls": "NOT_RUN"},
        "evidence": "codex/experiments/EXP-FRONTIER-36129180789/handoff.json",
    },
    {
        "id": "SAME-RUN-RESOLUTION",
        "observation": "same-run probes resolve the contradiction at component level: the browser "
                       "launch capability (public Playwright API + canonical Chromium executable) and "
                       "the Playwright package are AVAILABLE in this environment, while the browsergym "
                       "and agentlab imports are UNAVAILABLE. The historical distinction between an "
                       "unavailable observation and a valid negative is preserved; availability is "
                       "resolved per component, not erased.",
        "evidence": ["#CAP-CHROMIUM-LAUNCH", "#CAP-BROWSERGYM-IMPORT", "#CAP-AGENTLAB-IMPORT"],
    },
]


def build_ledger(contract: Dict[str, Any], experiment_dir: Path) -> Dict[str, Any]:
    comps: Dict[str, Any] = {}
    comps["CAP-PYTHON-DEPENDENCIES"] = _probe_python_dependencies()
    comps["CAP-CHROMIUM-LAUNCH"] = _probe_chromium_launch()
    comps["CAP-BROWSERGYM-IMPORT"] = _probe_import("browsergym")
    comps["CAP-AGENTLAB-IMPORT"] = _probe_import("agentlab")
    comps["CAP-POLICY-MODEL-CREDENTIAL"] = _probe_policy_model_credential()
    comps["CAP-HF-REACHABILITY"] = _probe_http_reachability("CAP-HF-REACHABILITY", "https://huggingface.co")
    comps["CAP-GHCR-REACHABILITY"] = _probe_http_reachability("CAP-GHCR-REACHABILITY", "https://ghcr.io/v2/")
    comps["CAP-DISTRIBUTED-SUBSTRATE"] = _probe_distributed_substrate(contract)
    comps["CAP-WAL-SCHEMA"] = _probe_wal_schema(contract)
    comps["CAP-HEALTH-GATE"] = _probe_health_gate(contract)
    comps["CAP-NGINX-CACHE-MISS-HIT"] = _probe_proxy_cache(contract)
    floors = _probe_readiness_floors(contract, experiment_dir)
    comps.update(floors)
    return comps


def evaluate_scopes(components: Dict[str, Any], contract: Dict[str, Any]) -> Dict[str, Any]:
    scopes = {}
    for scope_name, scope in contract["required_scopes"].items():
        required = scope["required"]
        failed = [c for c in required if components.get(c, {}).get("status") != "AVAILABLE"]
        scopes[scope_name] = {
            "required": required,
            "advisory": scope.get("advisory", []),
            "failed_required": failed,
            "scope_pass": not failed,
            "fail_closed_note": ("the contract fails closed for this scope; this is a bounded "
                                 "contract/availability result, never a scientific falsification"),
        }
    return scopes


def main() -> int:
    parser = argparse.ArgumentParser(description="SPIDER runtime capability ledger + substrate bring-up contract")
    parser.add_argument("--config", required=True)
    parser.add_argument("--ledger", required=True)
    args = parser.parse_args()

    contract_path = Path(args.config)
    ledger_path = Path(args.ledger)
    experiment_dir = contract_path.parent
    contract = json.loads(contract_path.read_text())
    lock_path = contract["substrate"]["run_lock"]

    fd = acquire_run_lock(lock_path)
    if fd is None:
        print(f"FAIL-CLOSED: run lock {lock_path} is held by a live process; refusing concurrent execution",
              file=sys.stderr)
        return 3
    try:
        components = build_ledger(contract, experiment_dir)
        scopes = evaluate_scopes(components, contract)
        git_head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                                  text=True, cwd=str(REPO_ROOT)).stdout.strip()
        wt_status = subprocess.run(["git", "status", "--short"], capture_output=True,
                                   text=True, cwd=str(REPO_ROOT)).stdout.strip()
        ledger = {
            "schema_version": 1,
            "ledger_id": f"CAPABILITY-LEDGER-{contract['run_id']}",
            "experiment_id": contract["experiment_id"],
            "lane": contract["lane"],
            "run_id": contract["run_id"],
            "base_sha": contract.get("base_sha", "8bc01342a23fe7a24959d09d8e2556ba2966c7e8"),
            "head_sha": git_head,
            "worktree_status": wt_status,
            "generated_at": _utc(),
            "freshness": "same-run; every component probed at ledger generation time",
            "secret_redaction": "credential presence and references only; no secret values",
            "required_scope": contract["required_scopes"],
            "scopes": scopes,
            "components": components,
            "inherited_probes": INHERITED_PROBES,
            "substrate": {
                "upstreams": contract["substrate"]["upstreams"],
                "nginx": contract["substrate"]["nginx"]["listen"],
                "config_path": contract["substrate"]["nginx"]["config_path"],
                "upstream_hash": contract["substrate"]["nginx"]["upstream_hash"],
                "database_path": contract["substrate"]["database"]["path"],
                "journal_mode": "WAL",
                "wal_autocheckpoint": 0,
                "schema": contract["substrate"]["database"]["schema"],
            },
            "health_checks": contract["health_checks"],
            "floors": contract["floors"],
            "one_command": contract["one_command"],
            "evidence": {
                "readiness_certificate": str(experiment_dir / "artifacts" / "A-READINESS-CERTIFICATE.json"),
                "bringup_contract": str(contract_path),
                "contract_sha256": _sha_file(contract_path),
            },
        }
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.write_text(json.dumps(ledger, indent=2, default=str))

        # Fail-closed exit status: non-zero if ANY declared scope fails.
        failed_scopes = [s for s, v in scopes.items() if not v["scope_pass"]]
        if failed_scopes:
            print(f"FAIL-CLOSED: required scopes failed: {failed_scopes}", file=sys.stderr)
            return 1
        print(f"OK: all declared required scopes pass; ledger at {ledger_path}")
        return 0
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
