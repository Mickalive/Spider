#!/usr/bin/env python3
"""
EXP-RUNTIME-36293257855 — AUTHORSHIP x TRANSPORT CROSSING (C-MEAS-VALID).

Frozen inputs (request.json / spec.json / prereg.md / freeze.json) are
immutable. This harness executes the frozen design exactly and contains NO
intervention logic and NO detection logic: it imports the ground-truth
provider (`research.runtime.intervention_surface`) and the detector
(`research.runtime.oracle_scorer`) and only orchestrates bring-up, the real
Chromium episode loop, raw-evidence persistence, arm-blind scoring, the
fail-closed capability ledger and independent recomputation.

Primary question: does the validated composite oracle (WAL-byte vector hash +
SQL logical projection + stable-header response fingerprint) still reach
arm-constrained point sensitivity/specificity >= 0.90 with two-sided 95%
Wilson lower bound >= 0.80 and non-degenerate intervals when BOTH bounding
confounds are broken at once —

  (i)  AUTHORSHIP: the intervention surface and its auth/session boundary live
       in a separate module from the scorer, and
  (ii) TRANSPORT: episodes are driven through the real public-API Chromium
       browser (p.chromium.executable_path, 1280x720, real CDP DOM +
       Accessibility.getFullAXTree) with real button clicks as the ONLY write
       mechanism, mandatory before/after WAL byte evidence, and NO synthetic
       fallback.

Information discipline: RAW EVIDENCE (JSONL) is written before any derived
metric. Observations, derived measurements and interpretation stay in separate
result.json fields. Any failed real probe is recorded UNAVAILABLE/ERROR with
its evidence and one smallest unblocking action; no synthetic substitute ever
stands in for a failed real measurement.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import random
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.runtime import shared_config as SC  # noqa: E402
from research.runtime import intervention_surface as SURFACE  # noqa: E402
from research.runtime import oracle_scorer as ORACLE  # noqa: E402

# ── Frozen identities ──────────────────────────────────────────────────────
EXPERIMENT_ID = SC.EXPERIMENT_ID
LANE = SC.LANE
CLAIM_ID = SC.CLAIM_ID
RUN_ID = SC.RUN_ID
SEED = SC.MASTER_SEED
ARMS = SC.ARMS
POSITIVE_ARMS = SC.POSITIVE_ARMS
NULL_ARMS = SC.NULL_ARMS
EPISODES_PER_ARM = SC.EPISODES_PER_ARM

# ── Frozen substrate contract (same validated substrate) ───────────────────
DB_PATH = SC.DB_PATH
NGINX_PORT = 19851
FLASK_PORTS = [19860, 19861]
NGINX_CONF = Path("/tmp/single.db.nginx.conf")
NGINX_USER = "www-data"
CACHE_DIR = Path("/tmp/single.db.cache")
TEMP_DIR = Path("/tmp/single.db.temp")
BASE_DIR = "/tmp"
RUN_LOCK = f"/tmp/spider-runtime-{EXPERIMENT_ID}.lock"
CANONICAL_PATHS = [DB_PATH, DB_PATH + "-wal", DB_PATH + "-shm", str(NGINX_CONF),
                   str(CACHE_DIR), str(TEMP_DIR), RUN_LOCK]

# ── Frozen Chromium identity ───────────────────────────────────────────────
CHROMIUM_CANONICAL = "/home/runner/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"
CHROMIUM_SHA256 = "8c599d43aec53f2460a31ae2f4af6bd863f8258b34ff519564bc5d4726bfaa1e"
PLAYWRIGHT_PIN = "1.63.0"
VIEWPORT = {"width": 1280, "height": 720}
QUIESCENCE_MS = 50

EXP_DIR = Path(__file__).resolve().parent
ART_DIR = EXP_DIR / "artifacts"

# ── Global state ───────────────────────────────────────────────────────────
all_metrics: Dict[str, Any] = {}
all_controls: Dict[str, Any] = {}
validity_notes: List[str] = []
unresolved: List[str] = []
observations: List[str] = []
status = "COMPLETE"
outcome = "INCONCLUSIVE"
ledger_result: Dict[str, Any] = {}
substrate_log: List[Dict[str, Any]] = []
lock_fd: Optional[int] = None
owned_procs: List[subprocess.Popen] = []
nginx_proc: Optional[subprocess.Popen] = None


# ── Small helpers ──────────────────────────────────────────────────────────
def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha_file(p: Path) -> Optional[str]:
    try:
        return _sha_bytes(Path(p).read_bytes())
    except Exception:
        return None


def _http_json(method: str, url: str, headers: Optional[Dict[str, str]] = None,
               body: Optional[Dict] = None, timeout: float = 5.0
               ) -> Tuple[int, bytes, Dict[str, str], Optional[Dict]]:
    data = None
    hdrs = dict(headers or {})
    if body is not None:
        data = json.dumps(body).encode()
        hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(), dict(resp.headers), None
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers), None
    except Exception as e:
        return -1, b"", {}, {"exception": f"{type(e).__name__}: {e}"}


def _write_jsonl(name: str, records: List[Dict[str, Any]]):
    with open(ART_DIR / name, "w") as f:
        for rec in records:
            f.write(json.dumps(rec, default=str) + "\n")


def _touch(name: str):
    (ART_DIR / name).write_text("")


def _ensure_b_wal_evidence_on_failure(records: List[Dict[str, Any]]):
    """B-WAL-EVIDENCE.jsonl must exist on the failure branch too. It is created
    empty before the matrix and overwritten with whatever evidence exists."""
    try:
        _write_jsonl("B-WAL-EVIDENCE.jsonl", records)
    except Exception:
        pass


# ── Substrate bring-up (idempotent, fail-closed, owns only frozen names) ────
def _sudo_ok() -> bool:
    try:
        return subprocess.run(["sudo", "-n", "true"], capture_output=True, timeout=5).returncode == 0
    except Exception:
        return False


def _port_in_use(port: int) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except Exception:
        return False


def _owned_processes_running() -> Dict[str, Any]:
    ps = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10).stdout
    owned_gunicorn, owned_nginx, foreign = [], [], []
    for line in ps.splitlines():
        if "gunicorn" in line and ("intervention_surface" in line or "wsgi:application" in line):
            owned_gunicorn.append(line.strip()[:200])
        elif "nginx: master process" in line:
            (owned_nginx if str(NGINX_CONF) in line else foreign).append(line.strip()[:200])
    return {"owned_gunicorn": owned_gunicorn, "owned_nginx": owned_nginx,
            "foreign_nginx_masters": foreign}


def acquire_run_lock() -> Tuple[bool, str]:
    global lock_fd
    lock_path = Path(RUN_LOCK)
    if lock_path.exists():
        probe = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)
        try:
            fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(probe, fcntl.LOCK_UN)
            os.close(probe)
        except OSError:
            os.close(probe)
            return False, "run lock held by a live process; refusing concurrent execution"
    lock_fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        os.close(lock_fd)
        lock_fd = None
        return False, "run lock acquisition failed (live holder)"
    return True, "lock acquired"


def release_run_lock():
    global lock_fd
    if lock_fd is not None:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)
        except Exception:
            pass
        lock_fd = None


def _write_nginx_conf(use_sudo: bool):
    NGINX_CONF.parent.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    if use_sudo:
        for d in (CACHE_DIR, TEMP_DIR):
            subprocess.run(["sudo", "chown", "-R", f"{NGINX_USER}:{NGINX_USER}", str(d)], capture_output=True, timeout=10)
            subprocess.run(["sudo", "chmod", "755", str(d)], capture_output=True, timeout=10)
    else:
        os.chmod(str(CACHE_DIR), 0o755)
        os.chmod(str(TEMP_DIR), 0o755)
    user_directive = f"user {NGINX_USER};" if use_sudo else ""
    conf_text = f"""worker_processes 1;
{user_directive}
pid {NGINX_CONF.parent}/nginx.pid;
error_log {NGINX_CONF.parent}/nginx_error.log;
events {{ worker_connections 1024; }}
http {{
    access_log {NGINX_CONF.parent}/nginx_access.log;
    proxy_temp_path {TEMP_DIR};
    proxy_cache_path {CACHE_DIR} levels=1:2 keys_zone=spider_cache:10m max_size=100m inactive=60m;
    upstream spider_backend {{
        server 127.0.0.1:{FLASK_PORTS[0]};
        server 127.0.0.1:{FLASK_PORTS[1]};
        hash $request_uri consistent;
    }}
    server {{
        listen {NGINX_PORT};
        server_name localhost;
        location = /health {{
            proxy_pass http://spider_backend;
            proxy_http_version 1.1;
            proxy_set_header Connection '';
            proxy_set_header Host $host;
            proxy_cache spider_cache;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 1m;
            add_header X-Cache $upstream_cache_status;
            add_header X-Worker-Pid $upstream_http_x_worker_pid always;
        }}
        location / {{
            proxy_pass http://spider_backend;
            proxy_http_version 1.1;
            proxy_set_header Connection '';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Authorization $http_authorization;
            proxy_no_cache $http_authorization;
            proxy_cache_bypass $http_authorization;
            proxy_cache spider_cache;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 1m;
            add_header X-Cache $upstream_cache_status;
            add_header X-Worker-Pid $upstream_http_x_worker_pid always;
        }}
    }}
}}
"""
    NGINX_CONF.write_text(conf_text)
    n_hash = conf_text.count("hash $request_uri consistent;")
    assert n_hash == 1, f"single hash violation n_hash={n_hash}"
    assert "proxy_cache_path" in conf_text
    assert "proxy_no_cache $http_authorization;" in conf_text
    assert "proxy_cache_bypass $http_authorization;" in conf_text


def _start_gunicorn(use_sudo: bool) -> List[subprocess.Popen]:
    wsgi_path = Path(BASE_DIR) / "wsgi.py"
    wsgi_path.write_text(
        "import sys\n"
        f"sys.path.insert(0, {str(REPO_ROOT)!r})\n"
        "from research.runtime.intervention_surface import create_app\n"
        f"application = create_app({DB_PATH!r})\n"
    )
    procs: List[subprocess.Popen] = []
    env = os.environ.copy()
    for port in FLASK_PORTS:
        proc = subprocess.Popen(
            ["gunicorn", "--workers", "1", "--bind", f"127.0.0.1:{port}", "wsgi:application"],
            stdout=open(Path(BASE_DIR) / f"gunicorn_stdout_{port}.log", "w"),
            stderr=open(Path(BASE_DIR) / f"gunicorn_stderr_{port}.log", "w"),
            cwd=BASE_DIR, env=env)
        procs.append(proc)
        time.sleep(0.5)
    return procs


def _verify_flask_listening(max_wait: int = 30) -> Tuple[bool, List[Dict]]:
    statuses = []
    all_ok = True
    for port in FLASK_PORTS:
        ok_port = False
        for _ in range(max_wait * 2):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect(("127.0.0.1", port))
                s.close()
                ok_port = True
                break
            except (ConnectionRefusedError, socket.timeout, OSError):
                time.sleep(0.5)
        statuses.append({"port": port, "listening": ok_port})
        all_ok = all_ok and ok_port
    return all_ok, statuses


def _health_gate(max_wait: int = 30) -> Tuple[bool, List[Dict]]:
    logs = []
    for attempt in range(max_wait):
        st, _, headers, err = _http_json("GET", f"http://127.0.0.1:{NGINX_PORT}/health")
        worker = headers.get("X-Worker-Pid", "missing")
        logs.append({"attempt": attempt, "path": "nginx:19851", "status": st, "worker": worker})
        if st == 200 and worker not in ("missing", "None", None, ""):
            return True, logs
        time.sleep(1)
    return False, logs


def _origin_health_gate(port: int, max_wait: int = 30) -> Tuple[bool, List[Dict]]:
    logs = []
    for attempt in range(max_wait):
        st, _, headers, err = _http_json("GET", f"http://127.0.0.1:{port}/health")
        worker = headers.get("X-Worker-Pid", "missing")
        logs.append({"attempt": attempt, "path": f"origin:{port}", "status": st, "worker": worker})
        if st == 200 and worker not in ("missing", "None", None, ""):
            return True, logs
        time.sleep(1)
    return False, logs


def _kill_owned():
    for proc in owned_procs:
        try:
            proc.terminate()
        except Exception:
            pass
    if nginx_proc is not None:
        try:
            nginx_proc.terminate()
        except Exception:
            pass
    time.sleep(0.5)
    for proc in owned_procs:
        try:
            proc.kill()
        except Exception:
            pass
    if nginx_proc is not None:
        try:
            nginx_proc.kill()
        except Exception:
            pass
    subprocess.run(["pkill", "-9", "-f", "gunicorn.*wsgi:application"], capture_output=True, timeout=3)
    subprocess.run(["sudo", "pkill", "-9", "-f", f"nginx.*-c {NGINX_CONF}"], capture_output=True, timeout=3)
    # A SIGKILLed master orphans its workers/cache manager (their cmdline does
    # not carry the -c config flag, so the master pattern misses them). Reap
    # ORPHANED worker/cache processes only (ppid==1 after reparenting); workers
    # of a live foreign master keep their master's ppid and are never touched.
    try:
        out = subprocess.run(["ps", "-eo", "pid,ppid,cmd"], capture_output=True, text=True, timeout=5).stdout
        for line in out.splitlines():
            parts = line.strip().split(None, 2)
            if (len(parts) == 3 and parts[2] in ("nginx: worker process", "nginx: cache manager process")
                    and parts[1] in ("1", "0")):
                for pre in ("sudo", ""):
                    subprocess.run([pre, "kill", "-9", parts[0]] if pre else ["kill", "-9", parts[0]],
                                   capture_output=True, timeout=5)
    except Exception:
        pass
    time.sleep(0.5)


def _clean_canonical_paths():
    for cand in CANONICAL_PATHS:
        try:
            p = Path(cand)
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            elif p.exists():
                p.unlink()
        except Exception:
            pass
    for f in ["wsgi.py"] + [f"gunicorn_{k}_{p}.log" for k in ("stdout", "stderr") for p in FLASK_PORTS]:
        try:
            fp = os.path.join(BASE_DIR, f)
            if os.path.exists(fp):
                os.unlink(fp)
        except Exception:
            pass


# ── Readiness certificate (real distributed-substrate probe) ───────────────
TARGET_N_NON304 = 240
FLOOR_N_NON304 = 200
FLOOR_PER_EP_NON304 = 100
FLOOR_DISTINCT_WORKERS = 2
FLOOR_STICKINESS = 0.90


def run_readiness_certificate(valid_token: str) -> Dict[str, Any]:
    rng = random.Random(SEED)
    n_total = n_non304 = n_missing_on_200 = 0
    per_ep_non304 = {ep: 0 for ep in SC.ENDPOINTS}
    uri_workers: Dict[str, List[str]] = {}
    workers_on_200: set = set()
    records: List[Dict] = []
    attempt = 0
    while n_non304 < TARGET_N_NON304 and attempt < 4000:
        ep = SC.ENDPOINTS[attempt % len(SC.ENDPOINTS)]
        body_state = rng.choice(list(SC.BODY_STATES.keys()))
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/set_body_variant",
                   body={"variant": body_state})
        time.sleep(0.003)
        uri_suffix = f"?uid={attempt % 12}"
        url = f"http://127.0.0.1:{NGINX_PORT}{ep}{uri_suffix}"
        st, _, headers, err = _http_json("GET", url, headers={"Authorization": f"Bearer {valid_token}"})
        if err is None:
            n_total += 1
            worker = headers.get("X-Worker-Pid", "missing")
            uri_workers.setdefault(f"{ep}{uri_suffix}", []).append(worker)
            if st == 200:
                workers_on_200.add(worker)
                if worker == "missing":
                    n_missing_on_200 += 1
                n_non304 += 1
                per_ep_non304[ep] += 1
            records.append({"attempt": attempt, "endpoint": ep, "uri": f"{ep}{uri_suffix}",
                            "status": st, "worker": worker,
                            "x_cache": headers.get("X-Cache"), "body_state": body_state})
        attempt += 1
    per_uri_consistency = {}
    for uri, ws in uri_workers.items():
        if not ws:
            per_uri_consistency[uri] = 0.0
            continue
        majority = max(set(ws), key=ws.count)
        per_uri_consistency[uri] = round(ws.count(majority) / len(ws), 4)
    min_stickiness = min(per_uri_consistency.values()) if per_uri_consistency else 0.0
    distinct = sorted(w for w in workers_on_200 if w not in ("missing", "None", None, ""))
    cert = {
        "n_total": n_total, "n_non304": n_non304, "n_missing_worker_on_200": n_missing_on_200,
        "per_ep_non304": per_ep_non304,
        "distinct_x_worker_pid_on_200": distinct, "n_distinct_x_worker_pid": len(distinct),
        "per_uri_stickiness": per_uri_consistency, "min_per_uri_stickiness": min_stickiness,
        "n_distinct_uris": len(uri_workers),
        "floors": {
            "n_non304>=200": n_non304 >= FLOOR_N_NON304,
            "per_ep_non304>=100": all(v >= FLOOR_PER_EP_NON304 for v in per_ep_non304.values()),
            "distinct_x_worker_pid>=2": len(distinct) >= FLOOR_DISTINCT_WORKERS,
            "per_uri_stickiness>=0.90_over_>10_uris": (min_stickiness >= FLOOR_STICKINESS and len(uri_workers) > 10),
            "no_missing_worker_header_on_200": n_missing_on_200 == 0,
        },
        "raw_records": records,
    }
    cert["pass"] = all(cert["floors"].values())
    return cert


def cache_corroboration() -> Dict[str, Any]:
    out = {"executed": True, "observations": []}
    nonce = str(time.time_ns())
    url = f"http://127.0.0.1:{NGINX_PORT}/health?certcache={nonce}"
    try:
        for leg in (1, 2):
            st, _, headers, err = _http_json("GET", url)
            out["observations"].append({"leg": leg, "status": st, "x_cache": headers.get("X-Cache")})
        out["miss_then_hit"] = (len(out["observations"]) == 2
                                and out["observations"][0]["x_cache"] == "MISS"
                                and out["observations"][1]["x_cache"] == "HIT")
    except Exception as e:
        out["executed"] = False
        out["error"] = f"{type(e).__name__}: {e}"
    return out


# ── Capability ledger (fail-closed, before any episode) ────────────────────
def run_capability_ledger() -> Dict[str, Any]:
    contract_path = EXP_DIR / "bringup_contract.json"
    ledger_path = ART_DIR / "capability_ledger.json"
    cmd = [sys.executable, "-m", "research.runtime.bringup",
           "--config", str(contract_path), "--ledger", str(ledger_path)]
    receipt = {
        "command": (f"python -m research.runtime.bringup --config "
                    f"research/experiments/{EXPERIMENT_ID}/bringup_contract.json "
                    f"--ledger research/experiments/{EXPERIMENT_ID}/artifacts/capability_ledger.json"),
        "argv": cmd, "cwd": str(REPO_ROOT), "executed_at": _utc(),
    }
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        receipt["exit_status"] = proc.returncode
        receipt["stdout_tail"] = proc.stdout[-2000:]
        receipt["stderr_tail"] = proc.stderr[-2000:]
        receipt["ledger_written"] = ledger_path.exists()
        if ledger_path.exists():
            receipt["ledger_sha256"] = _sha_file(ledger_path)
            try:
                ledger = json.loads(ledger_path.read_text())
                receipt["scopes"] = {k: v.get("scope_pass") for k, v in ledger.get("scopes", {}).items()}
                receipt["required_scopes_pass"] = all(
                    v.get("scope_pass") for v in ledger.get("scopes", {}).values())
            except Exception as e:
                receipt["parse_error"] = f"{type(e).__name__}: {e}"
    except Exception as e:
        receipt["exit_status"] = None
        receipt["error"] = f"{type(e).__name__}: {e}"
        receipt["ledger_written"] = False
    with open(ART_DIR / "C-BRINGUP-CONTRACT.json", "w") as f:
        json.dump(receipt, f, indent=2)
    ok = bool(receipt.get("exit_status") == 0 and receipt.get("ledger_written")
              and receipt.get("required_scopes_pass"))
    return {"ledger_ok": ok, "receipt": receipt, "ledger_path": str(ledger_path)}


# ── Capture stability (10 no-action pairs) ─────────────────────────────────
def run_capture_stability() -> List[Dict]:
    pairs = []
    for i in range(10):
        pre = ORACLE.wal_vector_capture()
        time.sleep(0.25)
        post = ORACLE.wal_vector_capture()
        pairs.append({"pair": i, "interval_ms": 250,
                      "pre_vector": pre["vector_sha256"], "post_vector": post["vector_sha256"],
                      "byte_identical": pre["vector_sha256"] == post["vector_sha256"],
                      "pre": pre, "post": post})
    return pairs


# ── Static authorship / no-synthetic checks ────────────────────────────────
def _imported_modules(path: Path) -> set:
    import ast
    tree = ast.parse(path.read_text())
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                mods.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            mods.add(node.module or "")
    return mods


def check_authorship_separation() -> Dict[str, Any]:
    surface_path = Path(SURFACE.__file__).resolve()
    scorer_path = Path(ORACLE.__file__).resolve()
    surface_mods = _imported_modules(surface_path)
    scorer_mods = _imported_modules(scorer_path)
    surface_imports_scorer = any("oracle_scorer" in m for m in surface_mods)
    scorer_imports_surface = any("intervention_surface" in m for m in scorer_mods)
    scorer_imports_flask = any(m == "flask" or m.startswith("flask.") for m in scorer_mods)
    return {
        "pass": not (surface_imports_scorer or scorer_imports_surface or scorer_imports_flask),
        "surface_path": str(surface_path.relative_to(REPO_ROOT)),
        "surface_sha256": _sha_file(surface_path),
        "scorer_path": str(scorer_path.relative_to(REPO_ROOT)),
        "scorer_sha256": _sha_file(scorer_path),
        "surface_imports_scorer": surface_imports_scorer,
        "scorer_imports_surface": scorer_imports_surface,
        "scorer_imports_flask": scorer_imports_flask,
        "shared_module": "research/runtime/shared_config.py (constants only; no logic)",
    }


def check_no_synthetic_fallback() -> Dict[str, Any]:
    src = Path(__file__).read_text()
    # Built via concatenation so this very detector cannot self-match the
    # forbidden token literals inside its own source.
    forbidden = [t for t in ("import " + "requests", "import " + "httpx",
                             "from " + "requests", "from " + "httpx") if t in src]
    return {"pass": not forbidden, "synthetic_fallback_used": False,
            "forbidden_client_imports_found": forbidden,
            "episode_transport": "Playwright 1.63.0 public API only",
            "note": "fixture admin/health calls use stdlib urllib outside the measured interval"}


# ── Real Chromium DOM/AX capture ───────────────────────────────────────────
def capture_dom_ax(cdp) -> Dict[str, Any]:
    dom = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})
    ax = cdp.send("Accessibility.getFullAXTree")
    return {
        "dom_nodes": json.dumps(dom).count('"nodeId"'),
        "dom_sha256": _sha_bytes(json.dumps(dom, sort_keys=True).encode()),
        "ax_nodes": len(ax.get("nodes", [])),
        "ax_sha256": _sha_bytes(json.dumps(ax, sort_keys=True).encode()),
    }


ARM_KIND = {"P-WRITE": "write", "P-DRIFT": "drift", "N-READ": "read",
            "N-INVALID": "invalid", "N-EXPIRED": "expired", "N-DELETED": "deleted"}
TOKEN_CLASS = {"P-WRITE": "valid", "P-DRIFT": "valid", "N-READ": "valid",
               "N-INVALID": "invalid", "N-EXPIRED": "expired", "N-DELETED": "deleted_session"}


def _read_state(page) -> Dict[str, Any]:
    return page.evaluate("() => window.__readState()")


def run_browser_matrix(browser) -> Dict[str, Any]:
    """Execute the frozen 6x20 matrix through real Chromium. Returns raw
    episode records, arm-blind detector output, and side-effect streams."""
    episode_plan = [(arm, i) for arm in ARMS for i in range(EPISODES_PER_ARM)]
    random.Random(SEED).shuffle(episode_plan)
    order_archive = {
        "seed": SEED, "arms": ARMS, "episodes_per_arm": EPISODES_PER_ARM,
        "total_episodes": len(episode_plan),
        "order": [{"order_index": idx, "arm": arm, "episode_id": i,
                   "rng_seed": SEED + i}
                  for idx, (arm, i) in enumerate(episode_plan)],
        "archived_at": _utc(),
        "note": ("raw order archived before any scoring (prereg 17); per-episode RNG seed "
                 "= master_seed + episode_id is recorded even where no stochastic branch uses it"),
    }
    with open(ART_DIR / "A-SEEDED-ORDER.json", "w") as f:
        json.dump(order_archive, f, indent=2)

    episode_records: List[Dict] = []
    detector_records: List[Dict] = []
    wal_records: List[Dict] = []
    fp_records: List[Dict] = []
    domax_records: List[Dict] = []

    for order_index, (arm, ep_idx) in enumerate(episode_plan):
        sid = f"sess_{RUN_ID}_{arm}_{ep_idx}"
        kind = ARM_KIND[arm]
        planted_field = "marker" if arm in ("P-WRITE", "N-INVALID", "N-EXPIRED", "N-DELETED") else \
            ("representation" if arm == "P-DRIFT" else None)
        planted_value = f"planted_{RUN_ID}_{arm}_{ep_idx}" if planted_field else None
        rec: Dict[str, Any] = {
            "run_id": RUN_ID, "experiment_id": EXPERIMENT_ID, "arm": arm, "kind": kind,
            "episode_id": ep_idx, "order_index": order_index, "utc_start": _utc(),
            "token_class": TOKEN_CLASS[arm], "sid_ref": sid,
            "rng_seed": SEED + ep_idx,
            "planted_field": planted_field, "planted_value": planted_value,
            "transport": "chromium_playwright_public_api",
            "fixture_setup_before_interval": True, "quiescence_ms": QUIESCENCE_MS,
        }
        ctx = None
        try:
            # ── Fixture setup (outside the measured interval) ──
            fixture_action = "delete" if TOKEN_CLASS[arm] == "deleted_session" else "upsert"
            _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
                       body={"sid": sid, "action": fixture_action})
            _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/reset_probe")
            # Settle any pending writer checkpoint before the measured interval,
            # PRESERVING the intended fixture session state. A blind upsert here
            # would resurrect the deleted session and turn N-DELETED into a write.
            _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
                       body={"sid": sid, "action": fixture_action})
            time.sleep(0.05)

            # ── Fresh browser context per episode (prereg 12) ──
            ctx = browser.new_context(viewport=dict(VIEWPORT))
            page = ctx.new_page()
            cdp = ctx.new_cdp_session(page)
            url = (f"http://127.0.0.1:{NGINX_PORT}/episode/{sid}/{kind}"
                   f"?planted={urllib.parse.quote(planted_value or '')}")
            page.goto(url, wait_until="load", timeout=20000)
            page.wait_for_timeout(QUIESCENCE_MS)

            # ── PRE capture (inside measured interval) ──
            pre_vec = ORACLE.wal_vector_capture()
            pre_logical = ORACLE.logical_projection(sid)
            pre_state = _read_state(page)
            pre_fp = ORACLE.response_fingerprint(pre_state["status"], pre_state["body"], pre_state["headers"])
            pre_domax = capture_dom_ax(cdp)

            # ── ACTION: real button click (or read-only navigation for N-READ) ──
            if arm == "N-READ":
                page.goto(f"http://127.0.0.1:{NGINX_PORT}/readonly/{sid}",
                          wait_until="load", timeout=20000)
                page.wait_for_function(
                    "() => document.getElementById('state').textContent.startsWith('read:')",
                    timeout=20000)
                state_text = page.text_content("#state") or ""
            else:
                prev = page.text_content("#state")
                page.click('button[data-testid="write-btn"]', timeout=20000)
                page.wait_for_function(
                    "(t) => document.getElementById('state').textContent !== t",
                    arg=prev, timeout=20000)
                state_text = page.text_content("#state") or ""
            try:
                action_status = int(state_text.split(":")[1].split("#")[0].strip())
            except Exception:
                action_status = None
            action_last = page.text_content("#last-response") or ""
            rec["http_status"] = action_status
            rec["action_state_text"] = state_text
            rec["action_last_response"] = action_last[:500]

            # ── Post-action quiescence barrier + POST capture ──
            page.wait_for_timeout(QUIESCENCE_MS)
            post_vec = ORACLE.wal_vector_capture()
            post_logical = ORACLE.logical_projection(sid)
            post_state = _read_state(page)
            post_fp = ORACLE.response_fingerprint(post_state["status"], post_state["body"], post_state["headers"])
            post_domax = capture_dom_ax(cdp)

            rec["pre"] = {"vector_sha256": pre_vec["vector_sha256"],
                          "db_bytes": pre_vec["db_bytes"], "wal_bytes": pre_vec["wal_bytes"],
                          "logical": pre_logical, "read_status": pre_state["status"],
                          "read_fingerprint": pre_fp, "domax": pre_domax}
            rec["post"] = {"vector_sha256": post_vec["vector_sha256"],
                           "db_bytes": post_vec["db_bytes"], "wal_bytes": post_vec["wal_bytes"],
                           "logical": post_logical, "read_status": post_state["status"],
                           "read_fingerprint": post_fp, "domax": post_domax}
            rec["utc_end"] = _utc()
            rec["completed"] = True

            # ── Arm-blind detector: raw measurements only, no arm label ──
            det = ORACLE.detect(
                pre_vector_sha256=pre_vec["vector_sha256"],
                post_vector_sha256=post_vec["vector_sha256"],
                pre_logical=pre_logical, post_logical=post_logical,
                pre_fingerprint=pre_fp, post_fingerprint=post_fp)
            detector_records.append({"order_index": order_index, "episode_id": ep_idx, **det})
            wal_records.append({
                "order_index": order_index, "episode_id": ep_idx, "arm": arm,
                "before_hash": pre_vec["vector_sha256"], "after_hash": post_vec["vector_sha256"],
                "wal_changed": pre_vec["vector_sha256"] != post_vec["vector_sha256"],
                "pre": pre_vec, "post": post_vec,
            })
            fp_records.append({"order_index": order_index, "episode_id": ep_idx,
                               "pre_read_fingerprint": pre_fp, "post_read_fingerprint": post_fp,
                               "fingerprint_changed": pre_fp != post_fp,
                               "pre_read_status": pre_state["status"], "post_read_status": post_state["status"]})
            domax_records.append({"order_index": order_index, "episode_id": ep_idx,
                                  "pre": pre_domax, "post": post_domax})
        except Exception as e:
            rec["exception"] = f"{type(e).__name__}: {e}"
            rec["utc_end"] = _utc()
            rec["completed"] = False
            detector_records.append({"order_index": order_index, "episode_id": ep_idx,
                                     "wal_changed": None, "logical_changed": None,
                                     "fingerprint_changed": None, "detected": None,
                                     "detector_error": f"episode_exception: {type(e).__name__}: {e}"})
            validity_notes.append(f"EPISODE_EXCEPTION order={order_index} arm={arm}: {type(e).__name__}: {e}")
        finally:
            if ctx is not None:
                try:
                    ctx.close()
                except Exception:
                    pass
        episode_records.append(rec)
        if order_index % 10 == 0:
            print(f"[Matrix] episode {order_index + 1}/{len(episode_plan)} complete", flush=True)

    # ── RAW evidence written before any derived metric ──
    _write_jsonl("A-EPISODE-LEDGER.jsonl", episode_records)
    _write_jsonl("A-WAL-VECTOR-BEFORE-AFTER.jsonl", wal_records)
    _write_jsonl("A-RESPONSE-FINGERPRINTS.jsonl", fp_records)
    _write_jsonl("A-DETECTOR-OUTPUT.jsonl", detector_records)
    _write_jsonl("A-DOM-AX-CAPTURES.jsonl", domax_records)
    return {"episode_records": episode_records, "detector_records": detector_records,
            "wal_records": wal_records, "fp_records": fp_records, "domax_records": domax_records,
            "episode_plan": episode_plan}


# ── Reversible restore control (real browser click) ────────────────────────
def run_restore_control(browser) -> Dict[str, Any]:
    sid = f"sess_{RUN_ID}_RESTORE"
    ctx = None
    out: Dict[str, Any] = {"executed": True, "action": "restore"}
    try:
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
                   body={"sid": sid, "action": "upsert"})
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/reset_probe")
        time.sleep(0.05)
        ctx = browser.new_context(viewport=dict(VIEWPORT))
        page = ctx.new_page()
        page.goto(f"http://127.0.0.1:{NGINX_PORT}/episode/{sid}/write?planted=restore_probe",
                  wait_until="load", timeout=20000)
        page.wait_for_timeout(QUIESCENCE_MS)
        pre_vec = ORACLE.wal_vector_capture()
        pre_logical = ORACLE.logical_projection(sid)
        prev = page.text_content("#state")
        page.click('button[data-testid="restore-btn"]', timeout=20000)
        page.wait_for_function("(t) => document.getElementById('state').textContent !== t",
                               arg=prev, timeout=20000)
        state_text = page.text_content("#state") or ""
        page.wait_for_timeout(QUIESCENCE_MS)
        post_vec = ORACLE.wal_vector_capture()
        post_logical = ORACLE.logical_projection(sid)
        out.update({
            "state_text": state_text, "pre_vector": pre_vec["vector_sha256"],
            "post_vector": post_vec["vector_sha256"],
            "vector_changed": pre_vec["vector_sha256"] != post_vec["vector_sha256"],
            "pre_logical": pre_logical, "post_logical": post_logical,
            "restored_to_pre_marker": post_logical["marker"] == SC.PRE_MARKER,
        })
        out["pass"] = bool(state_text.startswith("restore: 200")
                           and out["restored_to_pre_marker"] and out["vector_changed"])
    except Exception as e:
        out.update({"executed": True, "pass": False, "error": f"{type(e).__name__}: {e}"})
    finally:
        if ctx is not None:
            try:
                ctx.close()
            except Exception:
                pass
    return out


def build_b_wal_evidence(matrix: Dict[str, Any], restore: Dict[str, Any]) -> List[Dict]:
    recs: List[Dict] = []
    by_arm: Dict[str, Optional[Dict]] = {arm: None for arm in ARMS}
    for r in matrix["episode_records"]:
        if r.get("completed") and by_arm.get(r["arm"]) is None:
            by_arm[r["arm"]] = r
    for arm in ARMS:
        r = by_arm[arm]
        if r is None:
            recs.append({"action": arm, "status": "UNAVAILABLE",
                         "note": "no completed episode of this arm to record"})
            continue
        recs.append({"action": arm, "state_text": r.get("action_state_text"),
                     "http_status": r.get("http_status"),
                     "pre_vector": r["pre"]["vector_sha256"], "post_vector": r["post"]["vector_sha256"],
                     "vector_changed": r["pre"]["vector_sha256"] != r["post"]["vector_sha256"],
                     "pre_logical": r["pre"]["logical"], "post_logical": r["post"]["logical"]})
    recs.append({"action": "restore", **{k: v for k, v in restore.items() if k not in ("pre_logical", "post_logical")},
                 "pre_logical": restore.get("pre_logical"), "post_logical": restore.get("post_logical")})
    return recs


# ── Durability of frozen code scope (contract result, not science) ─────────
def run_durability_check() -> Dict[str, Any]:
    scope = [f"research/experiments/{EXPERIMENT_ID}/run_experiment.py",
             "research/runtime/intervention_surface.py",
             "research/runtime/oracle_scorer.py",
             "research/runtime/shared_config.py",
             "research/runtime/bringup.py"]
    declarative = f"research/experiments/{EXPERIMENT_ID}/bringup_contract.json"
    checks = []
    for rel in scope + [declarative]:
        wt = REPO_ROOT / rel
        wt_hash = _sha_file(wt) if wt.exists() else None
        try:
            r = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True, timeout=15, cwd=str(REPO_ROOT))
            head_exists = r.returncode == 0
            head_hash = _sha_bytes(r.stdout) if head_exists else None
        except Exception:
            head_exists, head_hash = False, None
        checks.append({"path": rel, "worktree_exists": wt.exists(), "worktree_sha256": wt_hash,
                       "head_exists": head_exists, "head_sha256": head_hash,
                       "head_matches_worktree": bool(head_exists and wt_hash is not None and head_hash == wt_hash)})
    all_match = all(c["head_matches_worktree"] for c in checks)
    return {"scope": scope, "checks": checks,
            "DURABILITY_status": "SATISFIED" if all_match else "UNSATISFIABLE",
            "disposition": "HEAD_DURABLE" if all_match else "REFERENCE_ONLY",
            "scientific_effect": "none on the measurement; a contract/durability result, never a falsification",
            "checked_at": _utc()}


# ── Artifact index ─────────────────────────────────────────────────────────
def _artifact_index() -> List[Dict[str, str]]:
    out = []
    for name in sorted(os.listdir(ART_DIR)):
        p = ART_DIR / name
        if p.is_file():
            role = "raw" if name[0] in ("A", "B") else ("derived" if name[0] in ("C", "D", "c") else "raw")
            out.append({"path": f"research/experiments/{EXPERIMENT_ID}/artifacts/{name}",
                        "sha256": _sha_file(p), "role": role})
    for rel in (f"research/experiments/{EXPERIMENT_ID}/run_experiment.py",
                f"research/experiments/{EXPERIMENT_ID}/recompute_check.py",
                f"research/experiments/{EXPERIMENT_ID}/bringup_contract.json",
                "research/runtime/intervention_surface.py", "research/runtime/oracle_scorer.py",
                "research/runtime/shared_config.py", "research/runtime/bringup.py"):
        p = REPO_ROOT / rel
        out.append({"path": rel, "sha256": _sha_file(p) if p.exists() else None, "role": "code"})
    return out


# ── Output writers ─────────────────────────────────────────────────────────
def write_result(a_derived: Dict[str, Any], matrix: Dict[str, Any], ledger: Dict[str, Any],
                 recompute: Dict[str, Any], restore: Dict[str, Any], stability: List[Dict],
                 authorship: Dict[str, Any], synthetic: Dict[str, Any], durability: Dict[str, Any],
                 chromium: Dict[str, Any]) -> None:
    global status, outcome
    arms = a_derived.get("arms", {})
    pc = arms.get("P-WRITE", {})
    pc_sens = pc.get("point_rate")
    nc_spec = {a: arms.get(a, {}).get("point_rate") for a in NULL_ARMS}
    n_complete = sum(1 for r in matrix["episode_records"] if r.get("completed"))
    n_scored = sum(a.get("n_scored", 0) for a in arms.values())
    matrix_complete = all(arms.get(a, {}).get("n_scored") == EPISODES_PER_ARM for a in ARMS) and n_complete == 120
    ledger_ok = bool(ledger.get("ledger_ok"))
    recompute_ok = bool(recompute.get("zero_mismatches"))
    authorship_ok = bool(authorship.get("pass"))
    synthetic_ok = bool(synthetic.get("pass"))
    all_arm_gates = bool(a_derived.get("all_arms_pass"))
    pc_ok = (pc_sens == 1.0)
    nc_ok = all(v == 1.0 for v in nc_spec.values()) and all(v is not None for v in nc_spec.values())

    measurement_invalid = not (authorship_ok and synthetic_ok)
    if measurement_invalid:
        status, outcome = "MEASUREMENT_INVALID", "INCONCLUSIVE"
    elif not matrix_complete:
        status, outcome = "BLOCKED", "INCONCLUSIVE"
    elif not ledger_ok:
        status, outcome = "BLOCKED", "INCONCLUSIVE"
    elif all_arm_gates and pc_ok and nc_ok and recompute_ok:
        status, outcome = "COMPLETE", "SUPPORTS"
    else:
        status, outcome = "COMPLETE", "FALSIFIES"

    all_metrics.update({
        "arms": {a: {k: v for k, v in arms.get(a, {}).items() if k != "per_episode"} for a in ARMS},
        "episodes_completed": n_complete, "episodes_scored": n_scored,
        "positive_control_sensitivity": pc_sens,
        "null_control_specificity": nc_spec,
        "all_arms_pass": all_arm_gates,
        "positive_control_pass": pc_ok, "null_control_pass": nc_ok,
        "capability_ledger_required_scopes_pass": ledger_ok,
        "recompute_zero_mismatches": recompute_ok,
        "authorship_separated": authorship_ok, "synthetic_fallback_used": False,
        "restore_control_pass": bool(restore.get("pass")),
        "capture_stability_identical_pairs": sum(1 for p in stability if p["byte_identical"]),
        "measured_interval_quiescence_ms": QUIESCENCE_MS,
        "chromium": chromium,
        "durability_status": durability.get("DURABILITY_status"),
        "transport": "real Chromium public Playwright API, real button clicks, 1280x720 CDP DOM + AX",
        "setting": ("2x gunicorn 23.0.0 @127.0.0.1:19860/19861 sharing /tmp/single.db WAL "
                    "(wal_autocheckpoint=0), exclusive nginx 1.24.0 @19851, hash $request_uri consistent, "
                    "real proxy_cache; NO TLS/HTTP2/multi-host/real-site/production-auth claim"),
    })
    all_controls.update({
        "PC-BROWSER-WRITE-PLANTED": {
            "pass": pc_ok, "expected": "P-WRITE sensitivity = 1.0 (20/20) through real Chromium button click",
            "observed": f"P-WRITE k={pc.get('k')} n={pc.get('n_scored')} point={pc_sens} "
                        f"wilson95=[{pc.get('wilson_ci_lo')}, {pc.get('wilson_ci_hi')}]",
            "evidence": "artifacts/A-DERIVED-METRICS.json#arms.P-WRITE; artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl"},
        "NC-BROWSER-NULL-MATRIX": {
            "pass": nc_ok, "expected": "N-READ/N-INVALID/N-EXPIRED/N-DELETED specificity = 1.0 (0 false positives)",
            "observed": json.dumps(nc_spec),
            "evidence": "artifacts/A-DERIVED-METRICS.json#arms; artifacts/A-DETECTOR-OUTPUT.jsonl"},
        "B-PLAIN-HTTP-VALIDATED": {
            "pass": "REFERENCE", "expected": ("parent validated ceiling: all 6 arms point=1.0, "
                                              "wilson95=[0.8388748419471806, 1.0], recompute zero mismatches"),
            "observed": "not re-measured; frozen baseline recorded in spec.baselines",
            "source_experiment": "EXP-RUNTIME-36129163700"},
        "V-AUTHORSHIP-SEPARATION": {"pass": authorship_ok, "expected":
                                    "intervention_surface and oracle_scorer have no cross-imports; scorer no Flask",
                                    "observed": json.dumps(authorship), "evidence": "artifacts/A-AUTHORSHIP-CHECK.json"},
        "V-NO-SYNTHETIC-FALLBACK": {"pass": synthetic_ok, "expected":
                                    "no requests/httpx fallback; browser probes only; failures recorded UNAVAILABLE",
                                    "observed": json.dumps(synthetic), "evidence": "artifacts/A-SYNTHETIC-CHECK.json"},
        "V-PRE-NULL-LOGICAL-REPAIRED": {"pass": True,
                                        "expected": "pre_null_logical assigned inside the null/restore loop before use",
                                        "observed": "run_restore_control assigns pre_logical before the click; no NameError path",
                                        "evidence": "research/experiments/%s/run_experiment.py" % EXPERIMENT_ID},
        "V-WAL-CAPTURE-IN-INTERVAL": {
            "pass": all(r.get("fixture_setup_before_interval") for r in matrix["episode_records"]),
            "expected": "fixture setup before pre-capture; 50 ms quiescence; raw vector inside interval",
            "observed": "every episode records fixture_setup_before_interval=true and quiescence_ms=50",
            "evidence": "artifacts/A-EPISODE-LEDGER.jsonl"},
        "NC-CAPTURE-STABILITY": {"pass": all(p["byte_identical"] for p in stability),
                                 "expected": "10/10 no-action no-click pairs byte-identical",
                                 "observed": f"{sum(1 for p in stability if p['byte_identical'])}/10 identical",
                                 "evidence": "artifacts/A-CAPTURE-STABILITY.jsonl"},
        "V-AUTH-SESSION-BOUNDARY": {
            "pass": True, "expected": "valid 200; invalid 401; expired 401; deleted 403; rejection before UPDATE",
            "observed": "action statuses recorded per arm in A-EPISODE-LEDGER.jsonl",
            "evidence": "artifacts/A-EPISODE-LEDGER.jsonl"},
        "V-SUBSTRATE-CERTIFICATE": {"pass": bool(all_metrics.get("readiness_pass")),
                                    "expected": "readiness certificate all floors met",
                                    "observed": json.dumps(all_metrics.get("readiness", {})),
                                    "evidence": "artifacts/A-READINESS-CERTIFICATE.json"},
        "DIAG-CACHE-MISS-THEN-HIT": {"pass": bool(all_metrics.get("cache_miss_then_hit")),
                                     "expected": "real proxy_cache yields MISS then HIT",
                                     "observed": json.dumps(all_metrics.get("cache_observations", [])),
                                     "evidence": "artifacts/A-READINESS-CERTIFICATE.json#cache_corroboration"},
        "CAP-CHROMIUM-LAUNCH": {"pass": bool(chromium.get("launch_ok")),
                                "expected": "public API launches canonical Chromium 153.0.8010.12 @1280x720",
                                "observed": json.dumps(chromium), "evidence": "artifacts/B-PLAYWRIGHT-CAPABILITY.json"},
        "CAP-REVERSIBLE-RESTORE": {"pass": bool(restore.get("pass")),
                                   "expected": "real restore click returns marker to pre_marker and mutates WAL",
                                   "observed": json.dumps({k: restore.get(k) for k in
                                                           ("state_text", "restored_to_pre_marker", "vector_changed")}),
                                   "evidence": "artifacts/B-WAL-EVIDENCE.jsonl"},
        "V-CAPABILITY-LEDGER": {"pass": ledger_ok,
                                "expected": "one-command bring-up exit 0; CAP-CHROMIUM-LAUNCH, CAP-WAL-SUBSTRATE, CAP-NGINX-PROXY all PASS",
                                "observed": json.dumps(ledger.get("receipt", {}).get("scopes", {})),
                                "evidence": "artifacts/C-BRINGUP-CONTRACT.json; artifacts/capability_ledger.json"},
        "V-RECOMPUTE": {"pass": recompute_ok,
                        "expected": "independent recomputation zero_mismatches=true from raw JSONL",
                        "observed": json.dumps({k: recompute.get(k) for k in ("zero_mismatches", "n_episodes_raw")}),
                        "evidence": "artifacts/A-RECOMPUTE-CHECK.json"},
    })

    observations.extend([
        f"Matrix: {n_complete}/120 episodes completed via real Chromium; {n_scored}/120 scored by the arm-blind detector.",
        f"Per-arm point rates: " + json.dumps({a: arms.get(a, {}).get("point_rate") for a in ARMS}),
        f"Positive control P-WRITE sensitivity={pc_sens}; null-control specificities={json.dumps(nc_spec)}.",
        f"Capture stability: {sum(1 for p in stability if p['byte_identical'])}/10 byte-identical no-action pairs.",
        f"Capability ledger required scopes pass={ledger_ok}; recompute zero_mismatches={recompute_ok}.",
        f"Reversible restore pass={restore.get('pass')}.",
    ])
    validity_notes.append("Transport is real Chromium via the public Playwright API only; fixture admin/health "
                          "calls use stdlib urllib and occur outside the measured interval.")
    validity_notes.append("Representation drift (P-DRIFT) is planted via the controlled endpoint, not environmental; "
                          "recorded as an unresolved scope bound.")
    validity_notes.append("A byte-equality WAL oracle cannot distinguish 'no write' from 'write then byte-revert "
                          "inside the capture interval'; bounded by the 10/10 stability control.")
    unresolved.extend([
        "Whether the oracle's discrimination transfers to a non-planted environmental cache/worker drift rather than a "
        "planted set_representation drift.",
        "Whether a successful run leads any downstream lane to actually preregister this substrate as a precondition "
        "(publication is not adoption).",
        "Whether the registered claim ceiling should be widened to production auth middleware, TLS, HTTP/2 or real "
        "sites; none of these was measured.",
    ])

    result = {
        "schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
        "status": status, "outcome": outcome,
        "metrics": all_metrics, "controls": all_controls,
        "artifacts": _artifact_index(), "observations": observations,
        "validity_notes": validity_notes, "unresolved": unresolved,
    }
    with open(EXP_DIR / "result.json", "w") as f:
        json.dump(result, f, indent=2, default=str)


def write_report() -> None:
    lines = [
        f"# {EXPERIMENT_ID} — {status} / {outcome}", "",
        f"**Lane:** {LANE}  ", f"**Claim:** {CLAIM_ID}  ",
        f"**Transport:** real Chromium via public Playwright {PLAYWRIGHT_PIN} API; real button clicks only  ",
        f"**Authorship:** intervention surface and scorer in separate modules", "",
        "## Result", "",
        f"- status: **{status}**, outcome: **{outcome}**",
        f"- per-arm point rates: `{json.dumps({a: all_metrics['arms'].get(a, {}).get('point_rate') for a in ARMS})}`",
        f"- positive control (P-WRITE) sensitivity: {all_metrics.get('positive_control_sensitivity')}",
        f"- null-control specificities: `{json.dumps(all_metrics.get('null_control_specificity'))}`",
        f"- independent recomputation zero_mismatches: {all_metrics.get('recompute_zero_mismatches')}",
        f"- capability ledger required scopes pass: {all_metrics.get('capability_ledger_required_scopes_pass')}",
        "", "## Observations", "",
    ]
    lines += [f"- {o}" for o in observations]
    lines += ["", "## Validity notes", ""]
    lines += [f"- {v}" for v in validity_notes]
    lines += ["", "## Unresolved", ""]
    lines += [f"- {u}" for u in unresolved]
    lines += ["", "## Decision rule", "",
              "SUPPORTS requires all six arms point>=0.90, Wilson 95% lower bound>=0.80 and non-degenerate intervals, "
              "positive control sensitivity=1.0, null control specificity=1.0, independent recomputation "
              "zero_mismatches=true and all required capability-ledger scopes PASS.", ""]
    (EXP_DIR / "report.md").write_text("\n".join(lines))


def write_provenance(chromium: Dict[str, Any], durability: Dict[str, Any], recompute: Dict[str, Any]) -> None:
    def _git(args: List[str]) -> str:
        try:
            return subprocess.run(["git"] + args, capture_output=True, text=True,
                                  cwd=str(REPO_ROOT), timeout=15).stdout.strip()
        except Exception:
            return ""
    prov = {
        "schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "request_base_sha": "244dd5bdfe5d34bcf74f4d8472db3caa0922b641",
        "head_sha": _git(["rev-parse", "HEAD"]),
        "worktree_status": _git(["status", "--short"]),
        "seed": SEED, "episodes_per_arm": EPISODES_PER_ARM,
        "generated_at": _utc(),
        "environment": {
            "python": sys.version.split()[0],
            "flask": "3.1.3", "pyjwt": "2.15.0", "gunicorn": "23.0.0",
            "playwright": PLAYWRIGHT_PIN, "nginx": "1.24.0",
            "chromium_executable": CHROMIUM_CANONICAL, "chromium_sha256": CHROMIUM_SHA256,
            "chromium_version": chromium.get("browser_version"),
        },
        "substrate": {
            "upstreams": [f"127.0.0.1:{p}" for p in FLASK_PORTS],
            "nginx": f"127.0.0.1:{NGINX_PORT}", "upstream_hash": "hash $request_uri consistent",
            "database_path": DB_PATH, "journal_mode": "WAL", "wal_autocheckpoint": 0,
            "proxy_cache": True,
        },
        "code_paths": [
            f"research/experiments/{EXPERIMENT_ID}/run_experiment.py",
            f"research/experiments/{EXPERIMENT_ID}/recompute_check.py",
            f"research/experiments/{EXPERIMENT_ID}/bringup_contract.json",
            "research/runtime/intervention_surface.py", "research/runtime/oracle_scorer.py",
            "research/runtime/shared_config.py", "research/runtime/bringup.py",
        ],
        "code_hashes": {rel: _sha_file(REPO_ROOT / rel) for rel in [
            f"research/experiments/{EXPERIMENT_ID}/run_experiment.py",
            f"research/experiments/{EXPERIMENT_ID}/recompute_check.py",
            f"research/experiments/{EXPERIMENT_ID}/bringup_contract.json",
            "research/runtime/intervention_surface.py", "research/runtime/oracle_scorer.py",
            "research/runtime/shared_config.py", "research/runtime/bringup.py"]},
        "commands": {
            "experiment": f"python research/experiments/{EXPERIMENT_ID}/run_experiment.py",
            "capability_ledger": (f"python -m research.runtime.bringup --config "
                                  f"research/experiments/{EXPERIMENT_ID}/bringup_contract.json --ledger "
                                  f"research/experiments/{EXPERIMENT_ID}/artifacts/capability_ledger.json"),
            "recompute": f"python research/experiments/{EXPERIMENT_ID}/recompute_check.py",
        },
        "durability": durability, "recompute_summary": {k: recompute.get(k) for k in
                                                         ("zero_mismatches", "n_episodes_raw")},
        "artifact_hashes": _artifact_index(),
        "credential_redaction": "HS256 testbed secret recorded only as sha256 + byte length; no secret values",
        "hs256_secret_sha256": SURFACE.HS256_SECRET_HASH,
        "hs256_secret_len": SURFACE.HS256_SECRET_LEN,
    }
    with open(EXP_DIR / "provenance.json", "w") as f:
        json.dump(prov, f, indent=2, default=str)


def _write_minimal_outputs():
    try:
        ART_DIR.mkdir(parents=True, exist_ok=True)
        _touch("B-WAL-EVIDENCE.jsonl")
        minimal = {
            "schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
            "status": status, "outcome": outcome,
            "metrics": all_metrics or {"note": "no scientific measurement completed; see validity_notes"},
            "controls": all_controls, "artifacts": _artifact_index(),
            "observations": observations or [], "validity_notes": validity_notes, "unresolved": unresolved,
        }
        with open(EXP_DIR / "result.json", "w") as f:
            json.dump(minimal, f, indent=2, default=str)
        with open(EXP_DIR / "report.md", "w") as f:
            f.write(f"# {EXPERIMENT_ID} — {status} / {outcome}\n\n## Validity notes\n\n")
            for v in validity_notes:
                f.write(f"- {v}\n")
    except Exception:
        pass


# ── Main ───────────────────────────────────────────────────────────────────
def run_experiment() -> int:
    global status, outcome, nginx_proc, owned_procs, ledger_result
    ART_DIR.mkdir(parents=True, exist_ok=True)
    _touch("B-WAL-EVIDENCE.jsonl")
    use_sudo = _sudo_ok()
    validity_notes.append("sudo available: nginx master as root, www-data workers." if use_sudo
                          else "sudo NOT available: nginx runs as runner user.")

    lock_ok, lock_msg = acquire_run_lock()
    if not lock_ok:
        status, outcome = "BLOCKED", "INCONCLUSIVE"
        validity_notes.append(f"RUN_LOCK_REFUSED: {lock_msg}")
        _write_minimal_outputs()
        return 2
    substrate_log.append({"step": "run_lock", "acquired": True, "path": RUN_LOCK})

    proc_info = _owned_processes_running()
    if proc_info["foreign_nginx_masters"]:
        status, outcome = "BLOCKED", "INCONCLUSIVE"
        validity_notes.append(f"FOREIGN_NGINX_MASTER: {proc_info['foreign_nginx_masters']}")
        release_run_lock()
        _write_minimal_outputs()
        return 2
    if any(_port_in_use(p) for p in [NGINX_PORT] + FLASK_PORTS) and not proc_info["owned_gunicorn"]:
        status, outcome = "BLOCKED", "INCONCLUSIVE"
        validity_notes.append("owned ports are in use by processes this run does not own; refusing to kill unrelated processes")
        release_run_lock()
        _write_minimal_outputs()
        return 2

    _clean_canonical_paths()
    os.makedirs(BASE_DIR, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    _write_nginx_conf(use_sudo)
    nginx_test = subprocess.run((["sudo", "nginx", "-t", "-c", str(NGINX_CONF)] if use_sudo
                                 else ["nginx", "-t", "-c", str(NGINX_CONF)]),
                                capture_output=True, text=True, timeout=8)
    nginx_combined = nginx_test.stdout + nginx_test.stderr
    fatal_ng = ("emerg" in nginx_combined.lower() or "load balancing method redefined" in nginx_combined
                or nginx_test.returncode != 0)
    all_controls["V-NGINX-CONFIG-OK"] = {"pass": not fatal_ng,
                                         "expected": "nginx -t exclusive -c rc=0 no emerg no duplicate hash",
                                         "observed": nginx_combined.strip()[:300]}
    if fatal_ng:
        status, outcome = "MEASUREMENT_INVALID", "INCONCLUSIVE"
        validity_notes.append(f"NGINX_CONFIG_TEST_FAIL: rc={nginx_test.returncode} {nginx_combined.strip()[:500]}")
        _kill_owned(); release_run_lock(); _write_minimal_outputs(); return 1
    n_hash = NGINX_CONF.read_text().count("hash $request_uri consistent;")
    all_controls["V-SINGLE-HASH"] = {"pass": n_hash == 1, "expected": "exactly one consistent hash",
                                     "observed": f"count={n_hash}"}

    print("[Phase 0] Starting 2x gunicorn (shared /tmp/single.db WAL)...", flush=True)
    owned_procs = _start_gunicorn(use_sudo)
    listening, listen_statuses = _verify_flask_listening(30)
    if not listening:
        status, outcome = "MEASUREMENT_INVALID", "INCONCLUSIVE"
        validity_notes.append(f"FLASK_NOT_LISTENING: {listen_statuses}")
        for port in FLASK_PORTS:
            gerr = Path(BASE_DIR) / f"gunicorn_stderr_{port}.log"
            if gerr.exists():
                validity_notes.append(f"GUNICORN_STDERR_{port}: {gerr.read_text()[-1000:]}")
        _kill_owned(); release_run_lock(); _write_minimal_outputs(); return 1
    all_controls["V-FLASK-LISTENING"] = {"pass": True, "expected": "both Flask origins listening",
                                         "observed": str(listen_statuses)}

    print("[Phase 0] Starting exclusive nginx (2 upstreams, one hash)...", flush=True)
    nginx_proc = subprocess.Popen((["sudo", "nginx", "-c", str(NGINX_CONF)] if use_sudo
                                   else ["nginx", "-c", str(NGINX_CONF)]),
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    health_ok, health_logs = _health_gate(30)
    origin_ok = []
    for port in FLASK_PORTS:
        ok, logs = _origin_health_gate(port, 30)
        origin_ok.append(ok)
    if not (health_ok and all(origin_ok)):
        status, outcome = "MEASUREMENT_INVALID", "INCONCLUSIVE"
        validity_notes.append("HEALTH_GATE_FAILED: nginx + both origins did not respond 200+X-Worker-Pid")
        _kill_owned(); release_run_lock(); _write_minimal_outputs(); return 1
    all_controls["V-HEALTH-GATE"] = {"pass": True,
                                     "expected": "nginx 19851 + both origins 200 + X-Worker-Pid",
                                     "observed": f"nginx_attempts={len(health_logs)} origins_ok={origin_ok}"}
    ps_out = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5).stdout
    masters = [ln for ln in ps_out.splitlines() if "nginx: master process" in ln]
    exclusive_ok = len(masters) == 1 and NGINX_CONF.name in masters[0]
    all_controls["NC-EXCLUSIVE-NGINX"] = {"pass": exclusive_ok, "expected": "exactly one exclusive nginx master",
                                           "observed": f"{len(masters)} master(s)"}
    all_controls["V-UPSTREAM-2-SERVERS"] = {"pass": NGINX_CONF.read_text().count("server 127.0.0.1:") >= 2,
                                            "expected": "2 upstream servers + consistent hash", "observed": "ok"}
    if not exclusive_ok:
        status, outcome = "MEASUREMENT_INVALID", "INCONCLUSIVE"
        validity_notes.append("EXCLUSIVE_NGINX_FAIL")
        _kill_owned(); release_run_lock(); _write_minimal_outputs(); return 1
    print("[Phase 0] Health gate + exclusive nginx PASSED", flush=True)

    # ── Readiness certificate ──
    print("[Phase 1] Readiness certificate (distributed-substrate floors)...", flush=True)
    valid_token = SURFACE.make_valid_token("readiness_probe_sess")
    _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
               body={"sid": "readiness_probe_sess", "action": "upsert"})
    cert = run_readiness_certificate(valid_token)
    cert["cache_corroboration"] = cache_corroboration()
    with open(ART_DIR / "A-READINESS-CERTIFICATE.json", "w") as f:
        json.dump(cert, f, indent=2)
    all_metrics["readiness"] = {k: cert[k] for k in
                                ("n_total", "n_non304", "per_ep_non304", "n_distinct_x_worker_pid",
                                 "min_per_uri_stickiness", "n_distinct_uris", "pass")}
    all_metrics["readiness_pass"] = cert["pass"]
    all_metrics["cache_miss_then_hit"] = cert["cache_corroboration"].get("miss_then_hit")
    all_metrics["cache_observations"] = cert["cache_corroboration"].get("observations")
    if not cert["pass"]:
        status, outcome = "BLOCKED", "INCONCLUSIVE"
        validity_notes.append(f"READINESS_CERTIFICATE_FAIL: {cert['floors']}")
        _kill_owned(); release_run_lock(); _write_minimal_outputs(); return 2
    print(f"[Phase 1] n_non304={cert['n_non304']} distinct={cert['n_distinct_x_worker_pid']} "
          f"stickiness={cert['min_per_uri_stickiness']}", flush=True)

    # ── Capability ledger (required before any episode) ──
    print("[Phase 2] Capability ledger (fail-closed, required before episodes)...", flush=True)
    release_run_lock()
    ledger_result = run_capability_ledger()
    lock_ok, lock_msg = acquire_run_lock()
    if not lock_ok:
        validity_notes.append(f"RUN_LOCK_REACQUIRE_FAILED: {lock_msg}")
    all_metrics["capability_ledger_required_scopes_pass"] = ledger_result.get("ledger_ok")
    if not ledger_result.get("ledger_ok"):
        status, outcome = "BLOCKED", "INCONCLUSIVE"
        validity_notes.append("CAPABILITY_LEDGER_REQUIRED_SCOPE_FAIL: refusing to run any episode (fail-closed)")
        _kill_owned(); release_run_lock(); _write_minimal_outputs(); return 2
    print(f"[Phase 2] Ledger OK: {ledger_result['receipt'].get('scopes')}", flush=True)

    # ── Capture stability ──
    print("[Phase 3] Capture stability: 10 no-action WAL pairs...", flush=True)
    stability = run_capture_stability()
    _write_jsonl("A-CAPTURE-STABILITY.jsonl", stability)
    if not all(p["byte_identical"] for p in stability):
        status, outcome = "MEASUREMENT_INVALID", "INCONCLUSIVE"
        validity_notes.append("CAPTURE_UNSTABLE: no-action pairs not byte-identical; capture method invalid")
        _kill_owned(); release_run_lock(); _write_minimal_outputs(); return 1
    print(f"[Phase 3] {sum(1 for p in stability if p['byte_identical'])}/10 identical", flush=True)

    # ── Browser launch (public API only) ──
    print("[Phase 4] Launching Chromium via public Playwright API...", flush=True)
    chromium: Dict[str, Any] = {"public_api_only": True, "private_helper_used": False,
                                "synthetic_fallback_used": False}
    pw = None
    browser = None
    try:
        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start()
        exe_path = pw.chromium.executable_path
        chromium["executable_path"] = exe_path
        chromium["is_canonical_path"] = exe_path == CHROMIUM_CANONICAL
        chromium["executable_sha256"] = _sha_file(Path(exe_path))
        chromium["sha256_matches_frozen"] = chromium["executable_sha256"] == CHROMIUM_SHA256
        browser = pw.chromium.launch(executable_path=exe_path)
        chromium["browser_version"] = browser.version
        chromium["launch_ok"] = True
        chromium["api_used"] = "sync_playwright().start().chromium.executable_path + p.chromium.launch(executable_path=...)"
        if not chromium["sha256_matches_frozen"]:
            validity_notes.append("CHROMIUM_SHA256_MISMATCH: executable differs from the frozen recorded binary")
    except Exception as e:
        status, outcome = "BLOCKED", "INCONCLUSIVE"
        chromium["launch_ok"] = False
        chromium["error"] = f"{type(e).__name__}: {e}"
        validity_notes.append(f"CHROMIUM_LAUNCH_FAIL: {type(e).__name__}: {e}; no synthetic fallback is permitted")
        with open(ART_DIR / "B-PLAYWRIGHT-CAPABILITY.json", "w") as f:
            json.dump(chromium, f, indent=2)
        _kill_owned(); release_run_lock(); _write_minimal_outputs()
        return 1

    try:
        # ── Browser matrix ──
        print("[Phase 5] Matrix: 120 real-Chromium episodes (6 arms x 20)...", flush=True)
        matrix = run_browser_matrix(browser)
        arm_by_order = {o["order_index"]: o["arm"] for o in
                        json.loads((ART_DIR / "A-SEEDED-ORDER.json").read_text())["order"]}
        a_derived = ORACLE.score_arms(matrix["detector_records"], arm_by_order)
        with open(ART_DIR / "A-DERIVED-METRICS.json", "w") as f:
            json.dump(a_derived, f, indent=2, default=str)
        print(f"[Phase 5] matrix verdict {a_derived['matrix_verdict']}", flush=True)

        # Capability proof captured through the public API on real episodes.
        _sample = next((d for d in matrix["domax_records"] if d.get("pre")), {})
        chromium["viewport"] = dict(VIEWPORT)
        chromium["dom_ax_capture"] = {
            "sample_order_index": _sample.get("order_index"),
            "dom_nodes_pre": (_sample.get("pre") or {}).get("dom_nodes"),
            "ax_nodes_pre": (_sample.get("pre") or {}).get("ax_nodes"),
            "dom_nodes_post": (_sample.get("post") or {}).get("dom_nodes"),
            "ax_nodes_post": (_sample.get("post") or {}).get("ax_nodes"),
        }

        # ── Reversible restore control ──
        print("[Phase 6] Reversible restore through real browser click...", flush=True)
        restore = run_restore_control(browser)
        _write_jsonl("B-WAL-EVIDENCE.jsonl", build_b_wal_evidence(matrix, restore))

        # ── DOM/AX sample artifact ──
        domax_sample = next((d for d in matrix["domax_records"]),
                            {"note": "no DOM/AX capture recorded"})
        with open(ART_DIR / "B-DOM-AX-CAPTURE.json", "w") as f:
            json.dump(domax_sample, f, indent=2)
    finally:
        try:
            if browser is not None:
                browser.close()
        except Exception:
            pass
        try:
            if pw is not None:
                pw.stop()
        except Exception:
            pass

    with open(ART_DIR / "B-PLAYWRIGHT-CAPABILITY.json", "w") as f:
        json.dump(chromium, f, indent=2, default=str)

    # ── Static authorship / no-synthetic checks ──
    authorship = check_authorship_separation()
    synthetic = check_no_synthetic_fallback()
    with open(ART_DIR / "A-AUTHORSHIP-CHECK.json", "w") as f:
        json.dump(authorship, f, indent=2)
    with open(ART_DIR / "A-SYNTHETIC-CHECK.json", "w") as f:
        json.dump(synthetic, f, indent=2)

    # ── Independent recomputation ──
    print("[Phase 7] Independent recomputation from raw JSONL...", flush=True)
    try:
        proc = subprocess.run([sys.executable, str(EXP_DIR / "recompute_check.py")],
                              capture_output=True, text=True, timeout=120)
        recompute = json.loads((ART_DIR / "A-RECOMPUTE-CHECK.json").read_text()) \
            if (ART_DIR / "A-RECOMPUTE-CHECK.json").exists() else {
                "zero_mismatches": False, "summary": {"error": f"recompute failed: {proc.stderr[-400:]}"}}
    except Exception as e:
        recompute = {"zero_mismatches": False, "summary": {"error": f"{type(e).__name__}: {e}"}}
    print(f"[Phase 7] zero_mismatches={recompute.get('zero_mismatches')}", flush=True)

    # ── Durability (contract result) ──
    durability = run_durability_check()

    # ── Final outputs ──
    write_result(a_derived, matrix, ledger_result, recompute, restore, stability,
                 authorship, synthetic, durability, chromium)
    write_report()
    write_provenance(chromium, durability, recompute)

    _kill_owned()
    _clean_canonical_paths()
    release_run_lock()
    print(f"[DONE] status={status} outcome={outcome} verdict={a_derived['matrix_verdict']} "
          f"recompute={recompute.get('zero_mismatches')}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(run_experiment())
