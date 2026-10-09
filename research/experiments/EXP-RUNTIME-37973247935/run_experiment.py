#!/usr/bin/env python3
"""
EXP-RUNTIME-37973247935 — OUT-OF-SURFACE TRANSFER + WAL BLIND-SPOT PROBE
(claim C-MEAS-VALID).

Frozen inputs (request.json / spec.json / prereg.md / freeze.json) are
immutable. This harness executes the frozen design exactly and contains NO
intervention logic and NO detection logic: it imports the in-surface
ground-truth provider (`research.runtime.intervention_surface`), the
out-of-surface ground-truth provider (`research.runtime.oos_worker`) and the
frozen detector (`research.runtime.oracle_scorer`), and only orchestrates
bring-up, preflight certificates, the real Chromium episode loop, raw-evidence
persistence, arm-blind scoring, the fail-closed capability ledger and
independent recomputation.

Primary question: does the composite oracle that was validated only against
fixture-authored interventions retain arm-constrained discrimination when the
change is induced OUTSIDE the surface (direct SQLite mutations by
oos_worker.py), and what is the measured magnitude of the byte-equality WAL
oracle's write-then-revert blind spot?

Information discipline: RAW EVIDENCE (JSONL) is written before any derived
metric; the arm-blind detector output is written before arm labels are joined.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import random
import shutil
import socket
import sqlite3
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
_EXP_DIR = Path(__file__).resolve().parent

# exp_config.py is loaded by file path: the on-disk experiment directory is
# dash-named ("EXP-RUNTIME-37973247935"), so it cannot be a Python module name;
# importlib keeps the default namespace packages untouched (no __init__.py
# anywhere is created or modified).
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location(
    "exp_config_37973247935", str(_EXP_DIR / "exp_config.py"))
assert _spec is not None and _spec.loader is not None, "exp_config.py unreadable"
EC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(EC)

from research.runtime import shared_config as SC  # noqa: E402
from research.runtime import intervention_surface as SURFACE  # noqa: E402
from research.runtime import oracle_scorer as ORACLE  # noqa: E402
from research.runtime import oos_worker as OOS  # noqa: E402

# ── Frozen identities (experiment-local) ───────────────────────────────────
EXPERIMENT_ID = EC.EXPERIMENT_ID
LANE = EC.LANE
CLAIM_ID = EC.CLAIM_ID
RUN_ID = EC.RUN_ID
SEED = EC.MASTER_SEED

OOS_POSITIVE_ARMS = EC.OOS_POSITIVE_ARMS
OOS_NULL_ARMS = EC.OOS_NULL_ARMS
LIVENESS_ARM = EC.LIVENESS_ARM
BLINDSPOT_ARMS = EC.BLINDSPOT_ARMS
ALL_MATRIX_ARMS = EC.ALL_MATRIX_ARMS
ARM_N = EC.ARM_N
ARM_KIND = EC.ARM_KIND
OOS_MODE = EC.OOS_MODE

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
THROWAWAY_DB = "/tmp/oos_cl_throwaway.db"
CANONICAL_PATHS = [DB_PATH, DB_PATH + "-wal", DB_PATH + "-shm", str(NGINX_CONF),
                   str(CACHE_DIR), str(TEMP_DIR), RUN_LOCK]

# ── Frozen Chromium identity ───────────────────────────────────────────────
CHROMIUM_CANONICAL = "/home/runner/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"
CHROMIUM_SHA256 = "8c599d43aec53f2460a31ae2f4af6bd863f8258b34ff519564bc5d4726bfaa1e"
PLAYWRIGHT_PIN = "1.63.0"
VIEWPORT = {"width": 1280, "height": 720}
QUIESCENCE_MS = 50

EXP_DIR = _EXP_DIR
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
anchor_conn: Optional[sqlite3.Connection] = None


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


def _hget(headers: Dict[str, str], name: str) -> Optional[str]:
    if not headers:
        return None
    low = name.lower()
    for k, v in headers.items():
        if k.lower() == low:
            return v
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


def _local_vector(db_path: str) -> str:
    """Local length-framed SHA-256 over db+wal (identical framing to the
    frozen scorer, but independent so preflight never calls the scorer)."""
    dbp = Path(db_path)
    wp = Path(db_path + "-wal")
    dbb = dbp.read_bytes() if dbp.exists() else b""
    wbb = wp.read_bytes() if wp.exists() else b""
    frame = len(dbb).to_bytes(8, "big") + dbb + len(wbb).to_bytes(8, "big") + wbb
    return _sha_bytes(frame)


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
    for suf in ("", "-wal", "-shm"):
        try:
            p = Path(THROWAWAY_DB + suf)
            if p.exists():
                p.unlink()
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


# ── Attainability certificate (pure arithmetic) ────────────────────────────
def run_attainability_certificate() -> Dict[str, Any]:
    z = SC.WILSON_Z

    def table(n: int, estimand: str) -> Dict[str, Any]:
        rows = []
        for k in range(n + 1):
            pt = k / n
            lo, hi = ORACLE.wilson_ci(k, n, z)
            rows.append({"k": k, "point": round(pt, 6),
                         "wilson_lo": round(lo, 6), "wilson_hi": round(hi, 6),
                         "ci_nondegenerate": hi > lo})
        return {"n": n, "estimand": estimand, "table": rows}

    pos = table(40, "sensitivity")
    null = table(40, "specificity")
    live = table(20, "sensitivity")
    n20 = table(20, "sensitivity")
    pos_accept = [r for r in pos["table"]
                  if r["point"] >= EC.POINT_MIN and r["wilson_lo"] >= EC.WILSON_LO_MIN and r["ci_nondegenerate"]]
    live_accept = [r for r in live["table"] if r["point"] >= EC.LIVENESS_POINT_MIN and r["ci_nondegenerate"]]
    first_pos = pos_accept[0] if pos_accept else None
    cert = {
        "experiment_id": EXPERIMENT_ID,
        "z": z,
        "thresholds": {"point_min": EC.POINT_MIN, "wilson_lo_min": EC.WILSON_LO_MIN,
                       "liveness_point_min": EC.LIVENESS_POINT_MIN, "non_degenerate": True},
        "out_of_surface_positive_n": 40,
        "out_of_surface_positive_accept_region": {
            "min_k": first_pos["k"] if first_pos else None,
            "n": 40,
            "point_at_min_k": first_pos["point"] if first_pos else None,
            "wilson_lo_at_min_k": first_pos["wilson_lo"] if first_pos else None,
            "wilson_hi_at_min_k": first_pos["wilson_hi"] if first_pos else None,
            "non_degenerate": first_pos["ci_nondegenerate"] if first_pos else None,
            "boundary_fail_k": (first_pos["k"] - 1) if first_pos else None,
            "boundary_fail": (pos["table"][first_pos["k"] - 1] if (first_pos and first_pos["k"] >= 1) else None),
        },
        "out_of_surface_null_n": 40,
        "null_accept_region": {"max_false_positives": 0, "k": 40, "n": 40, "point": 1.0,
                               "wilson_lo": round(ORACLE.wilson_ci(40, 40, z)[0], 6)},
        "liveness_control_n": 20,
        "liveness_accept_region": {"min_k": live_accept[0]["k"] if live_accept else None, "n": 20,
                                   "point": live_accept[0]["point"] if live_accept else None,
                                   "wilson_lo": live_accept[0]["wilson_lo"] if live_accept else None},
        "n20_reference_that_motivates_n40": {
            "k19_point": n20["table"][19]["point"],
            "k19_wilson_lo": n20["table"][19]["wilson_lo"],
            "k18_point": n20["table"][18]["point"],
            "k18_wilson_lo": n20["table"][18]["wilson_lo"],
            "note": "k=19/20 fails wilson_lo>=0.80; k=37/40 passes. n=40 is attainable by a genuinely high-rate instrument.",
        },
        "positive_table": pos["table"],
        "null_table": null["table"],
        "liveness_table": live["table"],
        "generated_at": _utc(),
    }
    with open(ART_DIR / "A-ATTAINABILITY-CERTIFICATE.json", "w") as f:
        json.dump(cert, f, indent=2)
    return cert


# ── Control-liveness preflight (throwaway copies; no detector on episodes) ──
def _make_throwaway_db(path: str) -> str:
    for suf in ("", "-wal", "-shm"):
        p = Path(path + suf)
        try:
            if p.exists():
                p.unlink()
        except Exception:
            pass
    conn = sqlite3.connect(path, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA wal_autocheckpoint=0")
    conn.execute(SC.SCHEMA["sessions"])
    conn.execute(SC.SCHEMA["body_config"])
    conn.execute(SC.SCHEMA["runtime_probe"])
    conn.execute("INSERT OR IGNORE INTO body_config VALUES (1,'A',?)", (SC.BODY_STATES["A"]["json"],))
    conn.execute("INSERT OR IGNORE INTO runtime_probe VALUES (1,?,?,?,?)",
                 (SC.PRE_MARKER, SC.PRE_REPRESENTATION, SC.PRE_REVISION, SC.PRE_UPDATED_AT))
    conn.commit()
    conn.close()
    return path


def run_control_liveness(cert: Dict[str, Any]) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    def rec(cid, ok, detail):
        checks.append({"id": cid, "pass": bool(ok), "detail": detail})

    # CL-OOS-WORKER-COMMIT-PROBE
    try:
        _make_throwaway_db(THROWAWAY_DB)
        v0 = _local_vector(THROWAWAY_DB)
        l0 = OOS.read_probe(THROWAWAY_DB)
        res = OOS.commit_probe_update(THROWAWAY_DB, marker="cl_commit_probe")
        v1 = _local_vector(THROWAWAY_DB)
        l1 = OOS.read_probe(THROWAWAY_DB)
        ok = bool(res["committed"] and v0 != v1 and l0 != l1 and l1["marker"] == "cl_commit_probe")
        rec("CL-OOS-WORKER-COMMIT-PROBE", ok, {"committed": res["committed"], "vector_changed": v0 != v1,
                                               "logical_before": l0, "logical_after": l1})
    except Exception as e:
        rec("CL-OOS-WORKER-COMMIT-PROBE", False, {"error": f"{type(e).__name__}: {e}"})

    # CL-OOS-WORKER-COMMIT-REPR
    try:
        _make_throwaway_db(THROWAWAY_DB)
        v0 = _local_vector(THROWAWAY_DB)
        b0 = OOS.read_body_config(THROWAWAY_DB)
        res = OOS.commit_representation(THROWAWAY_DB, variant="B")
        v1 = _local_vector(THROWAWAY_DB)
        b1 = OOS.read_body_config(THROWAWAY_DB)
        ok = bool(res["committed"] and v0 != v1 and b0["content"] != b1["content"] and b1["variant"] == "B")
        rec("CL-OOS-WORKER-COMMIT-REPR", ok, {"committed": res["committed"], "vector_changed": v0 != v1,
                                              "body_before": b0, "body_after": b1})
    except Exception as e:
        rec("CL-OOS-WORKER-COMMIT-REPR", False, {"error": f"{type(e).__name__}: {e}"})

    # CL-OOS-WORKER-IDLE
    try:
        _make_throwaway_db(THROWAWAY_DB)
        v0 = _local_vector(THROWAWAY_DB)
        res = OOS.idle(THROWAWAY_DB)
        v1 = _local_vector(THROWAWAY_DB)
        ok = bool(v0 == v1 and not res["committed"] and res["exception"] is None)
        rec("CL-OOS-WORKER-IDLE", ok, {"vector_identical": v0 == v1, "committed": res["committed"],
                                       "exception": res["exception"]})
    except Exception as e:
        rec("CL-OOS-WORKER-IDLE", False, {"error": f"{type(e).__name__}: {e}"})

    # CL-OOS-WORKER-REJECT
    try:
        _make_throwaway_db(THROWAWAY_DB)
        v0 = _local_vector(THROWAWAY_DB)
        res = OOS.reject_rollback(THROWAWAY_DB)
        v1 = _local_vector(THROWAWAY_DB)
        fired = bool(res["exception"] and "IntegrityError" in res["exception"])
        ok = bool(v0 == v1 and not res["committed"] and fired)
        rec("CL-OOS-WORKER-REJECT", ok, {"vector_identical": v0 == v1, "committed": res["committed"],
                                         "exception": res["exception"]})
    except Exception as e:
        rec("CL-OOS-WORKER-REJECT", False, {"error": f"{type(e).__name__}: {e}"})

    # CL-REVERT-FIDELITY
    try:
        _make_throwaway_db(THROWAWAY_DB)
        v0 = _local_vector(THROWAWAY_DB)
        snap = OOS.snapshot_bytes(THROWAWAY_DB)
        wr = OOS.commit_probe_update(THROWAWAY_DB, marker="cl_revert")
        vmid = _local_vector(THROWAWAY_DB)
        OOS.restore_bytes(snap, THROWAWAY_DB)
        v1 = _local_vector(THROWAWAY_DB)
        ok = bool(wr["committed"] and vmid != v0 and v1 == v0)
        rec("CL-REVERT-FIDELITY", ok, {"write_committed": wr["committed"], "mid_changed": vmid != v0,
                                       "restored_identical": v1 == v0})
    except Exception as e:
        rec("CL-REVERT-FIDELITY", False, {"error": f"{type(e).__name__}: {e}"})

    # CL-CACHE-MISS-HIT (live nginx leg)
    try:
        nonce = str(time.time_ns())
        url = f"http://127.0.0.1:{NGINX_PORT}/health?clcache={nonce}"
        legs = []
        for _ in (1, 2):
            st, _, headers, _e = _http_json("GET", url)
            legs.append({"status": st, "x_cache": headers.get("X-Cache")})
        ok = legs[0]["x_cache"] == "MISS" and legs[1]["x_cache"] == "HIT"
        rec("CL-CACHE-MISS-HIT", ok, {"legs": legs})
    except Exception as e:
        rec("CL-CACHE-MISS-HIT", False, {"error": f"{type(e).__name__}: {e}"})

    # CL-INSURFACE-LIVE (structural + live in-surface write, outside the matrix)
    try:
        src = Path(SURFACE.__file__).read_text()
        structural = ('"/runtime/write"' in src or "/runtime/write" in src) and "def create_app" in src
        sid = "cl_insurface_live"
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session", body={"sid": sid, "action": "upsert"})
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/reset_probe")
        tok = SURFACE.make_valid_token(sid)
        st, body, _h, _e = _http_json(
            "POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/runtime/write",
            headers={"Authorization": f"Bearer {tok}"},
            body={"op": "set_marker", "value": "cl_insurface_live"})
        probe = OOS.read_probe()
        live = bool(st == 200 and probe and probe["marker"] == "cl_insurface_live")
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/reset_probe")
        rec("CL-INSURFACE-LIVE", bool(structural and live),
            {"structural": structural, "in_surface_write_status": st,
             "marker_after": probe["marker"] if probe else None})
    except Exception as e:
        rec("CL-INSURFACE-LIVE", False, {"error": f"{type(e).__name__}: {e}"})

    all_pass = all(c["pass"] for c in checks)
    out = {
        "experiment_id": EXPERIMENT_ID,
        "discipline": "throwaway DB copies / throwaway cache key; oracle_scorer never invoked on real episodes during preflight",
        "checks": checks,
        "all_pass": all_pass,
        "generated_at": _utc(),
        "readiness_pass": cert.get("pass") if cert else None,
    }
    with open(ART_DIR / "A-CONTROL-LIVENESS.json", "w") as f:
        json.dump(out, f, indent=2)
    return out

# ── Real Chromium DOM/AX capture (public CDP session API) ──────────────────
def capture_dom_ax(cdp) -> Dict[str, Any]:
    dom = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})
    ax = cdp.send("Accessibility.getFullAXTree")
    return {
        "dom_nodes": json.dumps(dom).count('"nodeId"'),
        "dom_sha256": _sha_bytes(json.dumps(dom, sort_keys=True).encode()),
        "ax_nodes": len(ax.get("nodes", [])),
        "ax_sha256": _sha_bytes(json.dumps(ax, sort_keys=True).encode()),
    }


# ── Composite response capture over /runtime/read + /api/profile ───────────
# /health is deliberately EXCLUDED from the composite so that the only proxy
# cacheable leg (transport null N-OOS-CACHE) can change X-Cache/Age without
# changing any content; the nginx cache leg is recorded separately as raw
# transport evidence on every cache arm episode. The composite reuse s the
# frozen stable-header response_fingerprint per leg (EXCLUDED_HEADERS applied
# inside oracle_scorer.response_fingerprint) and hashes the concatenation.
COMPOSITE_ENDPOINTS = ["/runtime/read", "/api/profile"]
_COMPOSITE_JS = """(tok) => {
  const eps = ["/runtime/read", "/api/profile"];
  return Promise.all(eps.map(async (ep) => {
    const r = await fetch(ep, { headers: { "Authorization": "Bearer " + tok } });
    const body = await r.text();
    const h = {};
    r.headers.forEach(function (v, k) { h[k] = v; });
    return { endpoint: ep, status: r.status, body: body, headers: h };
  }));
}"""


def _browser_composite(page, token: str) -> Dict[str, Any]:
    """Real-Chromium composite capture (public Playwright API only)."""
    legs = page.evaluate(_COMPOSITE_JS, token)
    for leg in legs:
        leg["fingerprint_sha256"] = ORACLE.response_fingerprint(
            leg["status"], leg["body"], leg["headers"])
    parts = [f"{leg['endpoint']}|{leg['fingerprint_sha256'] or 'ERR'}" for leg in legs]
    return {"legs": legs, "composite_sha256": _sha_bytes("||".join(parts).encode())}


# ── Out-of-surface worker dispatch (no detection here) ────────────────────
def _dispatch_oos(arm: str) -> Dict[str, Any]:
    mode = EC.OOS_MODE[arm]
    if mode == "commit_probe_update":
        return OOS.commit_probe_update(DB_PATH, marker=f"oos_{arm}_{time.time_ns()}")
    if mode == "commit_representation":
        return OOS.commit_representation(DB_PATH, variant=EC.OOS_REPR_VARIANT)
    if mode == "idle":
        return OOS.idle(DB_PATH)
    if mode == "reject_rollback":
        return OOS.reject_rollback(DB_PATH)
    return {"mode": None, "committed": False, "error": f"no worker mode declared for {arm}"}


def _run_cache_action() -> Dict[str, Any]:
    """N-OOS-CACHE frozen action: two requests on one fresh cacheable key
    through the exclusive nginx proxy_cache -> MISS then HIT, identical body.
    The cacheable key is unauthenticated /health (Authorization-bearing
    requests are cache-bypassed by the frozen nginx contract)."""
    nonce = str(time.time_ns())
    url = f"http://127.0.0.1:{NGINX_PORT}/health?n_oos_cache={nonce}"
    legs = []
    for leg_no in (1, 2):
        st, body, headers, err = _http_json("GET", url)
        legs.append({"leg": leg_no, "status": st, "body": body.decode(errors="replace"),
                     "x_cache": headers.get("X-Cache"),
                     "content_type": headers.get("Content-Type"),
                     "content_length": headers.get("Content-Length"),
                     "error": err})
    return {"mode": "nginx_proxy_cache_miss_then_hit", "legs": legs,
            "miss_then_hit": (len(legs) == 2 and legs[0]["x_cache"] == "MISS"
                              and legs[1]["x_cache"] == "HIT")}


def _fixture_setup(sid: str, reset_body: bool = True):
    """Fixture plumbing OUTSIDE the measured interval; recorded per episode."""
    _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
               body={"sid": sid, "action": "upsert"})
    _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/reset_probe")
    if reset_body:
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/set_body_variant",
                   body={"variant": "A"})
    # Settle any pending writer checkpoint before the measured interval,
    # preserving the intended fixture session state.
    _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
               body={"sid": sid, "action": "upsert"})
    time.sleep(0.05)


def _episode_page(browser, sid: str, kind: str, planted: str = ""):
    ctx = browser.new_context(viewport=dict(VIEWPORT))
    page = ctx.new_page()
    cdp = ctx.new_cdp_session(page)
    if kind == "liveness":
        url = (f"http://127.0.0.1:{NGINX_PORT}/episode/{sid}/write"
               f"?planted={urllib.parse.quote(planted)}")
    else:
        url = f"http://127.0.0.1:{NGINX_PORT}/readonly/{sid}"
    page.goto(url, wait_until="load", timeout=20000)
    page.wait_for_timeout(QUIESCENCE_MS)
    return ctx, page, cdp


def run_episode(browser, arm: str, ep_idx: int, order_index: int) -> Dict[str, Any]:
    sid = f"sess_{RUN_ID}_{arm}_{ep_idx}"
    kind = EC.ARM_KIND[arm]
    planted = f"planted_{RUN_ID}_{arm}_{ep_idx}"
    rec: Dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID, "arm": arm, "kind": kind,
        "episode_id": ep_idx, "order_index": order_index, "sid": sid,
        "utc_start": _utc(), "rng_seed": SEED + ep_idx,
        "transport": "chromium_playwright_public_api",
        "fixture_setup_before_interval": True, "quiescence_ms": QUIESCENCE_MS,
    }
    ctx = None
    try:
        _fixture_setup(sid)
        token = SURFACE.make_valid_token(sid)
        ctx, page, cdp = _episode_page(browser, sid, kind, planted)

        # ── PRE capture (inside measured interval) ──
        pre_vec = ORACLE.wal_vector_capture(DB_PATH)
        pre_logical = ORACLE.logical_projection(sid, DB_PATH)
        pre_fp = _browser_composite(page, token)
        pre_domax = capture_dom_ax(cdp)

        # ── ACTION (as per arm) ──
        action: Dict[str, Any] = {"mode": None}
        if kind == "liveness":
            prev = page.text_content("#state") or ""
            page.click('button[data-testid="write-btn"]', timeout=20000)
            page.wait_for_function(
                "(t) => document.getElementById('state').textContent !== t",
                arg=prev, timeout=20000)
            state_text = page.text_content("#state") or ""
            try:
                http_status = int(state_text.split(":")[1].split("#")[0].strip())
            except Exception:
                http_status = None
            action = {"mode": "in_surface_browser_click", "state_text": state_text,
                      "http_status": http_status}
        elif arm == "N-OOS-CACHE":
            action = _run_cache_action()
        else:
            action = _dispatch_oos(arm)

        page.wait_for_timeout(QUIESCENCE_MS)

        # ── POST capture (inside measured interval) ──
        post_vec = ORACLE.wal_vector_capture(DB_PATH)
        post_logical = ORACLE.logical_projection(sid, DB_PATH)
        post_fp = _browser_composite(page, token)
        post_domax = capture_dom_ax(cdp)

        rec.update({
            "pre": {"vector_sha256": pre_vec["vector_sha256"], "wal_bytes": pre_vec["wal_bytes"],
                    "db_bytes": pre_vec["db_bytes"], "logical": pre_logical,
                    "composite_sha256": pre_fp["composite_sha256"],
                    "fingerprint_legs": pre_fp["legs"], "domax": pre_domax},
            "post": {"vector_sha256": post_vec["vector_sha256"], "wal_bytes": post_vec["wal_bytes"],
                     "db_bytes": post_vec["db_bytes"], "logical": post_logical,
                     "composite_sha256": post_fp["composite_sha256"],
                     "fingerprint_legs": post_fp["legs"], "domax": post_domax},
            "action": action, "utc_end": _utc(), "completed": True,
        })
    except Exception as e:
        rec.update({"exception": f"{type(e).__name__}: {e}", "utc_end": _utc(), "completed": False,
                    "action": rec.get("action", {})})
    finally:
        if ctx is not None:
            try:
                ctx.close()
            except Exception:
                pass
    return rec


# ── Blindspot probe (write-then-revert inside the 50 ms capture window) ───
def run_blindspot_episode(browser, arm: str, ep_idx: int, order_index: int) -> Dict[str, Any]:
    sid = f"sess_{RUN_ID}_{arm}_{ep_idx}"
    rec: Dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID, "arm": arm, "kind": "blindspot",
        "episode_id": ep_idx, "order_index": order_index, "sid": sid,
        "utc_start": _utc(), "rng_seed": SEED + ep_idx,
        "transport": "chromium_playwright_public_api", "fixture_setup_before_interval": True,
        "quiescence_ms": QUIESCENCE_MS,
    }
    ctx = None
    try:
        _fixture_setup(sid)
        token = SURFACE.make_valid_token(sid)
        ctx, page, cdp = _episode_page(browser, sid, kind="blindspot")

        # PRE capture (inside measured interval)
        pre_vec = ORACLE.wal_vector_capture(DB_PATH)
        pre_logical = ORACLE.logical_projection(sid, DB_PATH)
        pre_fp = _browser_composite(page, token)
        pre_domax = capture_dom_ax(cdp)
        snap = OOS.snapshot_bytes(DB_PATH)

        # write-then-revert, entirely inside the interval
        write_ev = _dispatch_oos(arm)                      # commit_probe_update
        write_happened = bool(write_ev.get("committed"))
        confirm_logical = OOS.read_probe(DB_PATH)          # independent SQL confirmation
        write_confirmed = bool(confirm_logical is not None
                               and confirm_logical["marker"] != pre_logical["marker"])
        restored_files: List[str] = []
        if arm == "M-REVERT-BYTES":
            OOS.restore_bytes(snap, DB_PATH)
            restored_files = ["", "-wal", "-shm"]
            revert_ev = {"mode": "restore_bytes", "restored_files": restored_files}
        else:  # M-REVERT-LOGICAL
            revert_ev = OOS.restore_logical(DB_PATH, marker=SC.PRE_MARKER,
                                            representation=SC.PRE_REPRESENTATION,
                                            revision=SC.PRE_REVISION, updated_at=SC.PRE_UPDATED_AT)
            restored_files = []

        page.wait_for_timeout(QUIESCENCE_MS)

        # POST capture (inside measured interval)
        post_vec = ORACLE.wal_vector_capture(DB_PATH)
        post_logical = ORACLE.logical_projection(sid, DB_PATH)
        post_fp = _browser_composite(page, token)
        post_domax = capture_dom_ax(cdp)

        revert_bytes_identical = pre_vec["vector_sha256"] == post_vec["vector_sha256"]
        det = ORACLE.detect(pre_vector_sha256=pre_vec["vector_sha256"],
                            post_vector_sha256=post_vec["vector_sha256"],
                            pre_logical=pre_logical, post_logical=post_logical,
                            pre_fingerprint=pre_fp["composite_sha256"],
                            post_fingerprint=post_fp["composite_sha256"])
        rec.update({
            "pre": {"vector_sha256": pre_vec["vector_sha256"], "logical": pre_logical,
                    "composite_sha256": pre_fp["composite_sha256"],
                    "fingerprint_legs": pre_fp["legs"], "domax": pre_domax},
            "post": {"vector_sha256": post_vec["vector_sha256"], "logical": post_logical,
                     "composite_sha256": post_fp["composite_sha256"],
                     "fingerprint_legs": post_fp["legs"], "domax": post_domax},
            "action": write_ev, "revert_evidence": revert_ev,
            "write_happened": write_happened, "write_confirmed": write_confirmed,
            "revert_bytes_identical": revert_bytes_identical,
            "restored_files": restored_files,
            "detected": bool(det.get("detected")), "verdict": det,
            "utc_end": _utc(), "completed": True,
        })
    except Exception as e:
        rec.update({"exception": f"{type(e).__name__}: {e}", "utc_end": _utc(), "completed": False})
    finally:
        if ctx is not None:
            try:
                ctx.close()
            except Exception:
                pass
    return rec


# ── Capture stability pair (no-action window, real browser) ────────────────
def run_stability_pair(browser, pair_idx: int) -> Dict[str, Any]:
    sid = f"sess_{RUN_ID}_STAB_{pair_idx}"
    ctx = None
    out: Dict[str, Any] = {"pair": pair_idx, "interval_ms": 250}
    try:
        _fixture_setup(sid)
        token = SURFACE.make_valid_token(sid)
        ctx, page, cdp = _episode_page(browser, sid, kind="stab")
        pre_vec = ORACLE.wal_vector_capture(DB_PATH)
        pre_fp = _browser_composite(page, token)
        pre_logical = ORACLE.logical_projection(sid, DB_PATH)
        time.sleep(0.25)  # no action
        post_vec = ORACLE.wal_vector_capture(DB_PATH)
        post_fp = _browser_composite(page, token)
        post_logical = ORACLE.logical_projection(sid, DB_PATH)
        out.update({
            "pre_vector": pre_vec["vector_sha256"], "post_vector": post_vec["vector_sha256"],
            "vector_identical": pre_vec["vector_sha256"] == post_vec["vector_sha256"],
            "fingerprint_identical": pre_fp["composite_sha256"] == post_fp["composite_sha256"],
            "logical_identical": pre_logical == post_logical,
            "all_identical": (pre_vec["vector_sha256"] == post_vec["vector_sha256"]
                              and pre_fp["composite_sha256"] == post_fp["composite_sha256"]
                              and pre_logical == post_logical),
            "pre": pre_vec, "post": post_vec, "utc_end": _utc(),
        })
    except Exception as e:
        out.update({"exception": f"{type(e).__name__}: {e}", "utc_end": _utc()})
    finally:
        if ctx is not None:
            try:
                ctx.close()
            except Exception:
                pass
    return out


# ── Matrix (260 frozen episodes + 20 interleaved stability pairs) ───────────
def run_matrix(browser) -> Dict[str, Any]:
    episode_plan = [(arm, i) for arm in EC.ALL_MATRIX_ARMS for i in range(EC.ARM_N[arm])]
    random.Random(SEED).shuffle(episode_plan)
    order_archive = {
        "seed": SEED, "arms": EC.ALL_MATRIX_ARMS, "episodes_per_arm": EC.ARM_N,
        "total_episodes": len(episode_plan),
        "order": [{"order_index": idx, "arm": arm, "episode_id": i, "rng_seed": SEED + i}
                  for idx, (arm, i) in enumerate(episode_plan)],
        "archived_at": _utc(),
        "note": "raw order archived before any scoring (prereg 18); per-episode RNG seed = master_seed + episode_id",
    }
    with open(ART_DIR / "A-SEEDED-ORDER.json", "w") as f:
        json.dump(order_archive, f, indent=2)

    episode_records: List[Dict] = []
    blindspot_records: List[Dict] = []
    wal_records: List[Dict] = []
    oos_evidence: List[Dict] = []
    detector_records: List[Dict] = []
    stability_pairs: List[Dict] = []
    episode_by_order: Dict[int, Dict] = {}
    episode_count = 0

    for order_index, (arm, ep_idx) in enumerate(episode_plan):
        if arm in EC.BLINDSPOT_ARMS:
            rec = run_blindspot_episode(browser, arm, ep_idx, order_index)
            blindspot_records.append(rec)
        else:
            rec = run_episode(browser, arm, ep_idx, order_index)
            episode_records.append(rec)
        episode_by_order[order_index] = rec

        wal_records.append({
            "order_index": order_index, "episode_id": ep_idx, "arm": arm,
            "before_hash": (rec.get("pre") or {}).get("vector_sha256"),
            "after_hash": (rec.get("post") or {}).get("vector_sha256"),
            "wal_changed": ((rec.get("pre") or {}).get("vector_sha256")
                            != (rec.get("post") or {}).get("vector_sha256"))
            if (rec.get("pre") and rec.get("post")) else None,
            "pre": rec.get("pre"), "post": rec.get("post"),
        })

        action = rec.get("action") or {}
        if isinstance(action, dict) and action.get("mode") in (
                "commit_probe_update", "commit_representation", "idle",
                "reject_rollback", "restore_logical"):
            oos_evidence.append({"order_index": order_index, "episode_id": ep_idx,
                                 "arm": arm, **action})
        if isinstance(action, dict) and action.get("mode") == "nginx_proxy_cache_miss_then_hit":
            oos_evidence.append({"order_index": order_index, "episode_id": ep_idx,
                                 "arm": arm, "mode": "nginx_proxy_cache_miss_then_hit",
                                 "legs": action.get("legs"), "miss_then_hit": action.get("miss_then_hit")})
        if isinstance(action, dict) and action.get("mode") == "in_surface_browser_click":
            oos_evidence.append({"order_index": order_index, "episode_id": ep_idx,
                                 "arm": arm, "mode": "in_surface_browser_click",
                                 "state_text": action.get("state_text"),
                                 "http_status": action.get("http_status")})

        # ── Arm-blind detector pass: raw measurements only, no arm label ──
        pre, post = rec.get("pre"), rec.get("post")
        if pre and post:
            det = ORACLE.detect(
                pre_vector_sha256=pre["vector_sha256"], post_vector_sha256=post["vector_sha256"],
                pre_logical=pre["logical"], post_logical=post["logical"],
                pre_fingerprint=pre["composite_sha256"], post_fingerprint=post["composite_sha256"])
        else:
            det = {"wal_changed": None, "logical_changed": None, "fingerprint_changed": None,
                   "detected": None,
                   "detector_error": f"episode_exception: {(rec.get('exception') or 'no pre/post')}"}
        detector_records.append({"order_index": order_index, "episode_id": ep_idx, **det})
        episode_count += 1

        # ── Interleaved no-action stability pair every 13 episodes (20 total) ──
        if (order_index + 1) % 13 == 0 and (order_index + 1) < len(episode_plan):
            stability_pairs.append(run_stability_pair(browser, len(stability_pairs)))

        if order_index % 10 == 0:
            print(f"[Matrix] episode {order_index + 1}/{len(episode_plan)} complete", flush=True)

    # ── RAW evidence written before ANY derived metric / label join ──
    _write_jsonl("A-EPISODE-LEDGER.jsonl", episode_records + blindspot_records)
    _write_jsonl("A-WAL-VECTOR-BEFORE-AFTER.jsonl", wal_records)
    _write_jsonl("A-OOS-WORKER-EVIDENCE.jsonl", oos_evidence)
    _write_jsonl("A-BLINDSPOT-PROBE.jsonl", blindspot_records)
    _write_jsonl("A-CAPTURE-STABILITY.jsonl", stability_pairs)
    _write_jsonl("A-DETECTOR-OUTPUT.jsonl", detector_records)

    return {"episode_records": episode_records, "blindspot_records": blindspot_records,
            "wal_records": wal_records, "oos_evidence": oos_evidence,
            "detector_records": detector_records, "stability_pairs": stability_pairs,
            "episode_plan": episode_plan, "episode_by_order": episode_by_order}

# ── Static authorship / no-synthetic / scorer-unreachability checks ────────
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
    worker_path = Path(OOS.__file__).resolve()
    surface_mods = _imported_modules(surface_path)
    scorer_mods = _imported_modules(scorer_path)
    worker_mods = _imported_modules(worker_path)
    surface_imports_scorer = any("oracle_scorer" in m for m in surface_mods)
    scorer_imports_surface = any("intervention_surface" in m for m in scorer_mods)
    scorer_imports_worker = any("oos_worker" in m for m in scorer_mods)
    worker_imports_scorer = any("oracle_scorer" in m for m in worker_mods)
    worker_imports_surface = any("intervention_surface" in m for m in worker_mods)
    scorer_imports_flask = any(m == "flask" or m.startswith("flask.") for m in scorer_mods)
    return {
        "pass": not (surface_imports_scorer or scorer_imports_surface or scorer_imports_worker
                     or worker_imports_scorer or worker_imports_surface or scorer_imports_flask),
        "surface_path": str(surface_path.relative_to(REPO_ROOT)),
        "surface_sha256": _sha_file(surface_path),
        "scorer_path": str(scorer_path.relative_to(REPO_ROOT)),
        "scorer_sha256": _sha_file(scorer_path),
        "worker_path": str(worker_path.relative_to(REPO_ROOT)),
        "worker_sha256": _sha_file(worker_path),
        "surface_imports_scorer": surface_imports_scorer,
        "scorer_imports_surface": scorer_imports_surface,
        "scorer_imports_worker": scorer_imports_worker,
        "worker_imports_scorer": worker_imports_scorer,
        "worker_imports_surface": worker_imports_surface,
        "scorer_imports_flask": scorer_imports_flask,
        "shared_module": "research/runtime/shared_config.py (constants only; no logic)",
    }


def check_oos_unreachable_from_scorer() -> Dict[str, Any]:
    scorer_src = Path(ORACLE.__file__).resolve().read_text()
    worker_src = Path(OOS.__file__).resolve().read_text()
    scorer_references_worker = ("oos_worker" in scorer_src
                                or "commit_probe_update" in scorer_src
                                or "commit_representation" in scorer_src
                                or "reject_rollback" in scorer_src)
    worker_references_scorer = ("oracle_scorer" in worker_src
                                or "wal_vector_capture" in worker_src
                                or "response_fingerprint" in worker_src
                                or "wilson_ci" in worker_src
                                or "logical_projection" in worker_src)
    verdict = not (scorer_references_worker or worker_references_scorer)
    return {
        "pass": verdict,
        "scorer_path": str(Path(ORACLE.__file__).resolve().relative_to(REPO_ROOT)),
        "scorer_references_oos_worker": scorer_references_worker,
        "scorer_text_mentions": {
            "oos_worker": "oos_worker" in scorer_src,
            "commit_probe_update": "commit_probe_update" in scorer_src,
            "commit_representation": "commit_representation" in scorer_src,
            "reject_rollback": "reject_rollback" in scorer_src,
        },
        "worker_references_scorer": worker_references_scorer,
        "worker_text_mentions": {
            "oracle_scorer": "oracle_scorer" in worker_src,
            "wal_vector_capture": "wal_vector_capture" in worker_src,
            "response_fingerprint": "response_fingerprint" in worker_src,
            "wilson_ci": "wilson_ci" in worker_src,
            "logical_projection": "logical_projection" in worker_src,
        },
        "verdict_id": "V-OOS-UNREACHABLE-FROM-SCORER",
    }


def check_no_synthetic_fallback() -> Dict[str, Any]:
    src = Path(__file__).read_text()
    forbidden = [t for t in ("import " + "requests", "import " + "httpx",
                             "from " + "requests", "from " + "httpx") if t in src]
    return {"pass": not forbidden, "synthetic_fallback_used": False,
            "forbidden_client_imports_found": forbidden,
            "episode_transport": "Playwright 1.63.0 public API only",
            "note": "fixture admin/health calls use stdlib urllib; the N-OOS-CACHE transport-null action is two urllib GETs THROUGH the real nginx proxy_cache (the cache leg is the measured object, not a substitute)"}


# ── Capability ledger (one-command fail-closed bring-up) ──────────────────
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


# ── Durability record (contract result only, scientific_effect none) ──────
def run_durability_check() -> Dict[str, Any]:
    scope = [f"research/experiments/{EXPERIMENT_ID}/run_experiment.py",
             f"research/experiments/{EXPERIMENT_ID}/exp_config.py",
             f"research/experiments/{EXPERIMENT_ID}/bringup_contract.json",
             "research/runtime/intervention_surface.py",
             "research/runtime/oracle_scorer.py",
             "research/runtime/shared_config.py",
             "research/runtime/oos_worker.py",
             "research/runtime/bringup.py"]
    out: Dict[str, Any] = {"schema_version": 1, "checked_at": _utc()}
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                          cwd=str(REPO_ROOT)).stdout.strip()
    out["head_sha"] = head
    records = []
    all_head = True
    for rel in scope:
        disk = REL if (REL := os.path.join(str(REPO_ROOT), rel)) else None
        try:
            head_show = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True,
                                       cwd=str(REPO_ROOT), timeout=15).stdout
            head_exists = subprocess.run(["git", "cat-file", "-e", f"HEAD:{rel}"],
                                         capture_output=True, cwd=str(REPO_ROOT), timeout=15).returncode == 0
            disk_sha = _sha_bytes(Path(disk).read_bytes())
            head_sha = _sha_bytes(head_show.encode()) if head_exists and head_show else None
        except Exception:
            head_exists = False
            head_sha = None
            disk_sha = _sha_file(disk) if os.path.exists(disk) else None
        same = head_exists and head_sha is not None and head_sha == disk_sha
        all_head = all_head and same
        records.append({"path": rel, "head_exists": head_exists,
                        "head_sha256": head_sha, "disk_sha256": disk_sha, "byte_equal": same})
    out["scope"] = records
    out["all_frozen_scope_head_resident"] = all_head
    out["disposition"] = "REFERENCE_ONLY" if not all_head else "HEAD_RESIDENT"
    out["scientific_effect"] = "none on the measurement; a contract/durability result, never a falsification"
    with open(ART_DIR / "A-DURABILITY.json", "w") as f:
        json.dump(out, f, indent=2)
    return out


# ── Arm-blind scoring (label join AFTER detector output is archived) ────────
def score_arms(detector_records: List[Dict[str, Any]],
               arm_by_order: Dict[int, str]) -> Dict[str, Any]:
    per_arm: Dict[str, Dict[str, Any]] = {
        arm: {"k": 0, "n": 0, "per_episode": []} for arm in EC.ALL_MATRIX_ARMS}
    det_by_order = {d["order_index"]: d for d in detector_records}
    for order_index, arm in arm_by_order.items():
        det = det_by_order.get(order_index, {})
        bucket = per_arm[arm]
        if det.get("detected") is None:
            bucket["per_episode"].append({"order_index": order_index, "scored": False,
                                          "reason": det.get("detector_error", "missing detector output")})
            continue
        bucket["n"] += 1
        kind = EC.ARM_KIND[arm]
        if kind in ("positive", "liveness"):
            if det["detected"]:
                bucket["k"] += 1
            bucket["per_episode"].append({"order_index": order_index, "scored": True,
                                          "detected": bool(det["detected"])})
        else:  # null
            if not det["detected"]:
                bucket["k"] += 1
            bucket["per_episode"].append({"order_index": order_index, "scored": True,
                                          "false_positive": bool(det["detected"])})
    arms: Dict[str, Any] = {}
    for arm in EC.ALL_MATRIX_ARMS:
        k, n = per_arm[arm]["k"], per_arm[arm]["n"]
        point = (k / n) if n else None
        ci_lo, ci_hi = ORACLE.wilson_ci(k, n) if n else (None, None)
        arms[arm] = {
            "n_scored": n, "k": k,
            "estimand": ("sensitivity" if EC.ARM_KIND[arm] in ("positive", "liveness")
                         else "specificity"),
            "point_rate": point, "wilson_ci_lo": ci_lo, "wilson_ci_hi": ci_hi,
            "ci_nondegenerate": (ci_hi > ci_lo) if (ci_lo is not None) else False,
            "per_episode": per_arm[arm]["per_episode"],
        }
    null_fp = sum(1 for arm in EC.OOS_NULL_ARMS
                  for e in arms[arm]["per_episode"] if e.get("false_positive"))
    positives_pass = {
        arm: bool(arms[arm]["point_rate"] is not None
                  and arms[arm]["point_rate"] >= EC.POINT_MIN
                  and arms[arm]["wilson_ci_lo"] is not None
                  and arms[arm]["wilson_ci_lo"] >= EC.WILSON_LO_MIN
                  and arms[arm]["ci_nondegenerate"])
        for arm in EC.OOS_POSITIVE_ARMS
    }
    liveness = arms[EC.LIVENESS_ARM]
    liveness_sensitivity = liveness["point_rate"] if liveness["n_scored"] else None
    n_mismatch = {arm: (EC.ARM_N[arm] != arms[arm]["n_scored"]) for arm in EC.ALL_MATRIX_ARMS}
    return {
        "z": SC.WILSON_Z,
        "thresholds": {"point_min": EC.POINT_MIN, "wilson_lo_min": EC.WILSON_LO_MIN,
                       "non_degenerate": True},
        "arms": arms,
        "null_false_positives_total": null_fp,
        "null_false_positives_by_arm": {
            arm: sum(1 for e in arms[arm]["per_episode"] if e.get("false_positive"))
            for arm in EC.OOS_NULL_ARMS},
        "out_of_surface_positives_pass": positives_pass,
        "liveness_control": {"arm": EC.LIVENESS_ARM, "sensitivity": liveness_sensitivity,
                             "required": 1.0},
        "scored_n_matches_frozen_n": not any(n_mismatch.values()),
        "scored_n_mismatch": n_mismatch,
    }


def blindspot_metrics(blindspot_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for sub in EC.BLINDSPOT_ARMS:
        recs = [r for r in blindspot_records if r.get("arm") == sub]
        scored = [r for r in recs if r.get("completed") and r.get("detected") is not None]
        k = sum(1 for r in scored if r["detected"])
        n = len(scored)
        lo, hi = ORACLE.wilson_ci(k, n) if n else (None, None)
        out[sub] = {
            "sub_condition": sub,
            "n_executed": len(recs), "n_scored": n, "n_detected": k,
            "detection_fraction": (k / n) if n else None,
            "wilson_ci_lo": lo, "wilson_ci_hi": hi,
            "ci_nondegenerate": (hi > lo) if (lo is not None) else False,
            "write_happened_all": all(r.get("write_happened") for r in recs),
            "write_confirmed_all": all(r.get("write_confirmed") for r in recs),
            "revert_bytes_identical_all": all(r.get("revert_bytes_identical") for r in recs),
            "completed_all": all(r.get("completed") for r in recs),
            "directional_prediction": ("detect ~ 0" if sub == "M-REVERT-BYTES" else "detect ~ 1"),
        }
    both = all(out[s]["n_scored"] == EC.BLINDSPOT_N for s in EC.BLINDSPOT_ARMS)
    contradicted = {}
    if out["M-REVERT-BYTES"]["detection_fraction"] is not None:
        contradicted["M-REVERT-BYTES"] = out["M-REVERT-BYTES"]["detection_fraction"] > EC.BLINDSPOT_MAJORITY
    if out["M-REVERT-LOGICAL"]["detection_fraction"] is not None:
        contradicted["M-REVERT-LOGICAL"] = out["M-REVERT-LOGICAL"]["detection_fraction"] < EC.BLINDSPOT_MAJORITY
    out["both_directional_predictions_contradicted"] = bool(
        contradicted.get("M-REVERT-BYTES") and contradicted.get("M-REVERT-LOGICAL"))
    out["contradiction_vs_prediction"] = contradicted
    out["blindspot_n_complete"] = both
    out["note"] = "probe never gates SUPPORTS/FALSIFIES; interpretation only"
    return out


# ── Frozen decision mapping (prereg section 11 / spec decision_rule) ───────
def decide(derived: Dict[str, Any], bs: Dict[str, Any], recompute: Dict[str, Any],
           ledger_ok: bool, preflights_ok: bool, stability_ok: bool,
           authorship_pass: bool, oos_unreachable_pass: bool, synthetic_pass: bool,
           arm_blind_ok: bool) -> Tuple[str, str, List[str]]:
    # MEASUREMENT_INVALID triggers (never a scientific negative)
    invalid: List[str] = []
    if not authorship_pass:
        invalid.append("authorship_separation_violated")
    if not oos_unreachable_pass:
        invalid.append("scorer_unreachability_violated")
    if not synthetic_pass:
        invalid.append("synthetic_fallback_used")
    if not preflights_ok:
        invalid.append("attainability_or_control_liveness_preflight_failed")
    if not stability_ok:
        invalid.append("capture_stability_not_byte_identical")
    if derived["liveness_control"]["sensitivity"] != 1.0:
        invalid.append("instrument_liveness_sensitivity_below_1.0")
    for sub in EC.BLINDSPOT_ARMS:
        if sub == "M-REVERT-BYTES" and not bs[sub]["revert_bytes_identical_all"]:
            invalid.append("blindspot_revert_fidelity_not_achieved")
    if invalid:
        return "MEASUREMENT_INVALID", "INCONCLUSIVE", invalid

    # INCONCLUSIVE triggers (infrastructure / mechanical)
    inconclusive: List[str] = []
    if not ledger_ok:
        inconclusive.append("capability_ledger_required_scope_fail")
    if not derived["scored_n_matches_frozen_n"]:
        inconclusive.append("scored_episodes_per_arm_differs_from_frozen_n")
    missing_wal = [a for a, r in derived["arms"].items()
                   if any(e.get("scored") is False for e in r["per_episode"])]
    if missing_wal:
        inconclusive.append(f"mandatory_wal_evidence_missing_on_arms={missing_wal}")
    if inconclusive:
        return "BLOCKED", "INCONCLUSIVE", inconclusive

    # Scientific mapping (valid measurement)
    pos_pass = derived["out_of_surface_positives_pass"]
    null_fp = derived["null_false_positives_total"]
    liveness_ok = derived["liveness_control"]["sensitivity"] == 1.0
    recompute_ok = bool(recompute.get("zero_mismatches"))
    reasons: List[str] = []

    if pos_pass["P-OOS-WORKER"] and pos_pass["P-OOS-REPR"] and null_fp == 0 \
            and liveness_ok and recompute_ok and arm_blind_ok:
        outcome = "SUPPORTS"
    elif not (pos_pass["P-OOS-WORKER"] and pos_pass["P-OOS-REPR"]):
        outcome = "FALSIFIES"
        reasons.append("both out-of-surface positives fail the frozen positive thresholds")
    elif null_fp > 0:
        outcome = "MIXED"
        reasons.append("sensitivity transfers but specificity does not (null false positives present)")
    elif not recompute_ok:
        outcome = "FALSIFIES"
        reasons.append("falsifier (iii): independent recomputation zero_mismatches=false")
    elif not arm_blind_ok:
        outcome = "FALSIFIES"
        reasons.append("falsifier (iv): arm-blind discipline violated")
    else:
        outcome = "SUPPORTS"

    if outcome == "SUPPORTS" and bs.get("both_directional_predictions_contradicted"):
        outcome = "MIXED"
        reasons.append("blind-spot probe contradicts BOTH registered directional predictions (interpretation only)")
    return "COMPLETE", outcome, reasons


# ── Output writers ─────────────────────────────────────────────────────────
_ROLE_MAP = {
    "A-SEEDED-ORDER.json": "fixture", "A-DETECTOR-OUTPUT.jsonl": "raw",
    "A-WAL-VECTOR-BEFORE-AFTER.jsonl": "raw", "A-EPISODE-LEDGER.jsonl": "raw",
    "A-CAPTURE-STABILITY.jsonl": "raw", "A-OOS-WORKER-EVIDENCE.jsonl": "raw",
    "A-BLINDSPOT-PROBE.jsonl": "raw", "A-DERIVED-METRICS.json": "derived",
    "A-RECOMPUTE-CHECK.json": "derived", "A-AUTHORSHIP-CHECK.json": "raw",
    "A-OOS-UNREACHABLE.json": "raw", "A-SYNTHETIC-CHECK.json": "raw",
    "A-ATTAINABILITY-CERTIFICATE.json": "derived", "A-CONTROL-LIVENESS.json": "derived",
    "A-READINESS-CERTIFICATE.json": "raw", "A-DURABILITY.json": "derived",
    "B-PLAYWRIGHT-CAPABILITY.json": "raw", "B-WAL-EVIDENCE.jsonl": "raw",
    "capability_ledger.json": "derived", "C-BRINGUP-CONTRACT.json": "derived",
}


def _list_artifacts() -> List[Dict[str, Any]]:
    out = []
    if not ART_DIR.exists():
        return out
    for name in sorted(os.listdir(ART_DIR)):
        p = ART_DIR / name
        out.append({"path": f"research/experiments/{EXPERIMENT_ID}/artifacts/{name}",
                    "sha256": _sha_file(p),
                    "role": _ROLE_MAP.get(name, "raw")})
    return out


def write_result(derived: Dict[str, Any], bs: Dict[str, Any], recompute: Dict[str, Any],
                 ledger_result: Dict[str, Any], stability_pairs: List[Dict],
                 authorship: Dict[str, Any], oos_unreachable: Dict[str, Any],
                 synthetic: Dict[str, Any], durability: Dict[str, Any],
                 chromium: Dict[str, Any], reasons: List[str],
                 preflights: Dict[str, Any], cert: Dict[str, Any]) -> None:
    def _arm_row(a: str) -> Dict[str, Any]:
        r = derived["arms"][a]
        return {"estimand": r["estimand"], "n_scored": r["n_scored"], "k": r["k"],
                "point_rate": r["point_rate"], "wilson_ci_lo": r["wilson_ci_lo"],
                "wilson_ci_hi": r["wilson_ci_hi"], "ci_nondegenerate": r["ci_nondegenerate"]}

    metrics: Dict[str, Any] = {
        "claim_id": CLAIM_ID,
        "matrix_episodes_total": 260,
        "matrix_episodes_planned": sum(EC.ARM_N[a] for a in EC.ALL_MATRIX_ARMS),
        "blindspot_probe_episodes_planned": EC.BLINDSPOT_N * 2,
        "capture_stability_pairs_planned": EC.CAPTURE_STABILITY_PAIRS,
        "arms": {a: _arm_row(a) for a in EC.ALL_MATRIX_ARMS},
        "null_false_positives_total": derived["null_false_positives_total"],
        "null_false_positives_by_arm": derived["null_false_positives_by_arm"],
        "liveness_control_sensitivity": derived["liveness_control"]["sensitivity"],
        "cl_zero_false_positives_requirement": "0/120",
        "oos_positives_pass": derived["out_of_surface_positives_pass"],
        "blindspot": bs,
        "recompute_zero_mismatches": recompute.get("zero_mismatches"),
        "capability_ledger_required_scopes_pass": ledger_result.get("ledger_ok"),
        "readiness": {k: cert.get(k) for k in
                      ("n_total", "n_non304", "per_ep_non304", "n_distinct_x_worker_pid",
                       "min_per_uri_stickiness", "n_distinct_uris", "pass")},
        "cache_miss_then_hit": cert.get("cache_corroboration", {}).get("miss_then_hit"),
        "cache_observations": cert.get("cache_corroboration", {}).get("observations"),
        "preflights": preflights,
        "stability": {"n_pairs": len(stability_pairs),
                      "all_byte_identical": all(p.get("all_identical") for p in stability_pairs)},
        "chromium_sha256_matches_frozen": chromium.get("sha256_matches_frozen"),
        "browser_version": chromium.get("browser_version"),
        "setting": "2x gunicorn 23.0.0 @127.0.0.1:19860/19861 sharing /tmp/single.db WAL "
                   "(wal_autocheckpoint=0), exclusive nginx 1.24.0 @19851, hash $request_uri "
                   "consistent, real proxy_cache; out-of-surface mutations via "
                   "research/runtime/oos_worker.py; NO TLS/HTTP2/multi-host/real-site claim",
        "estimated_cost_projection": {"total_measured_episodes": 260, "browser_launches": 280},
    }

    controls: Dict[str, Any] = {
        "B-INSURFACE-BROWSER-VALIDATED": {
            "expected": "frozen parent baseline; not re-measured; composite oracle 6 in-surface arms x 20, "
                        "point=1.0 Wilson95=[0.8388748419471806, 1.0], recompute zero_mismatches, AUDIT PASS",
            "observed": "cited from research/experiments/EXP-RUNTIME-36293257855/{result.json,audit.json}",
            "pass": True, "evidence": "parent packet (immutable)"},
        "B-OUT-OF-SURFACE-PRECEDENT": {
            "expected": "none recorded in Codex/parent handoff",
            "observed": "{} — no precedent; this experiment is the first out-of-surface measurement",
            "pass": None, "evidence": "{}"},
        "PC-INSURFACE-WRITE-LIVE": {
            "expected": "sensitivity 1.0 (20/20) on the frozen in-surface planted browser write",
            "observed": (f"n_scored={derived['arms'][EC.LIVENESS_ARM]['n_scored']} "
                         f"k={derived['arms'][EC.LIVENESS_ARM]['k']} "
                         f"point={derived['arms'][EC.LIVENESS_ARM]['point_rate']}"),
            "pass": derived["liveness_control"]["sensitivity"] == 1.0,
            "evidence": "artifacts/A-DETECTOR-OUTPUT.jsonl; artifacts/A-EPISODE-LEDGER.jsonl"},
        "NC-OOS-NULL-MATRIX": {
            "expected": "0 false positives across 120 matched out-of-surface null episodes",
            "observed": f"fp_total={derived['null_false_positives_total']} "
                        f"by_arm={derived['null_false_positives_by_arm']}",
            "pass": derived["null_false_positives_total"] == 0,
            "evidence": "artifacts/A-DETECTOR-OUTPUT.jsonl; artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl"},
        "NC-CAPTURE-STABILITY": {
            "expected": "20 no-action pairs, all byte-identical (bounds spontaneous variation)",
            "observed": f"{len(stability_pairs)} pairs; "
                        f"all_identical={all(p.get('all_identical') for p in stability_pairs)}",
            "pass": stability_pairs and all(p.get("all_identical") for p in stability_pairs),
            "evidence": "artifacts/A-CAPTURE-STABILITY.jsonl"},
        "NC-ANCHOR-CONNECTION": {
            "expected": "one sqlite connection held open across the matrix so WAL is never "
                        "checkpointed/deleted by last-close",
            "observed": "held open from before the matrix until after all captures",
            "pass": True, "evidence": "observations; artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl"},
        "V-HEALTH-GATE": {
            "expected": "nginx 19851 + both origins 200 + X-Worker-Pid",
            "observed": all_controls.get("V-HEALTH-GATE", {}).get("observed", "not recorded"),
            "pass": bool(all_controls.get("V-HEALTH-GATE", {}).get("pass", False)),
            "evidence": "artifacts/A-CONTROL-LIVENESS.json#CL-CACHE-MISS-HIT; A-READINESS-CERTIFICATE.json"},
        "NC-EXCLUSIVE-NGINX": {
            "expected": "exactly one exclusive nginx master",
            "observed": all_controls.get("NC-EXCLUSIVE-NGINX", {}).get("observed", "not recorded"),
            "pass": bool(all_controls.get("NC-EXCLUSIVE-NGINX", {}).get("pass", False)),
            "evidence": "run observations"},
        "DIAG-CACHE-MISS-THEN-HIT": {
            "expected": "real proxy_cache yields MISS then HIT",
            "observed": json.dumps(cert.get("cache_corroboration", {}).get("observations", [])),
            "pass": bool(cert.get("cache_corroboration", {}).get("miss_then_hit")),
            "evidence": "artifacts/A-READINESS-CERTIFICATE.json#cache_corroboration"},
        "V-AUTHORSHIP-SEPARATION": {
            "expected": "surface/scorer/worker pairwise no-import; scorer no Flask",
            "observed": json.dumps({k: authorship[k] for k in
                                    ("surface_imports_scorer", "scorer_imports_surface",
                                     "scorer_imports_worker", "worker_imports_scorer",
                                     "worker_imports_surface", "scorer_imports_flask")}),
            "pass": bool(authorship.get("pass")),
            "evidence": "artifacts/A-AUTHORSHIP-CHECK.json"},
        "V-OOS-UNREACHABLE-FROM-SCORER": {
            "expected": "scorer cannot reach oos_worker (no import, no call)",
            "observed": json.dumps({"scorer_references_oos_worker": oos_unreachable.get("scorer_references_oos_worker"),
                                    "worker_references_scorer": oos_unreachable.get("worker_references_scorer")}),
            "pass": bool(oos_unreachable.get("pass")),
            "evidence": "artifacts/A-OOS-UNREACHABLE.json"},
        "V-NO-SYNTHETIC-FALLBACK": {
            "expected": "no httpx/requests client or synthetic substitute",
            "observed": json.dumps(synthetic.get("forbidden_client_imports_found", [])),
            "pass": bool(synthetic.get("pass")),
            "evidence": "artifacts/A-SYNTHETIC-CHECK.json"},
        "M-REVERT-BLINDSPOT": {
            "expected": "measured, never gated; M-REVERT-BYTES detect ~ 0, M-REVERT-LOGICAL detect ~ 1",
            "observed": json.dumps({s: {"detection_fraction": bs[s]["detection_fraction"],
                                        "wilson_ci_lo": bs[s]["wilson_ci_lo"],
                                        "wilson_ci_hi": bs[s]["wilson_ci_hi"],
                                        "write_confirmed_all": bs[s]["write_confirmed_all"],
                                        "revert_bytes_identical_all": bs[s]["revert_bytes_identical_all"]}
                                    for s in EC.BLINDSPOT_ARMS}),
            "pass": None,
            "evidence": "artifacts/A-BLINDSPOT-PROBE.jsonl; artifacts/A-DERIVED-METRICS.json#blindspot"},
    }
    for c in preflights.get("checks", []):
        controls[c["id"]] = {"expected": c.get("description", ""),
                             "observed": json.dumps(c.get("detail")),
                             "pass": bool(c.get("pass")),
                             "evidence": "artifacts/A-CONTROL-LIVENESS.json"}

    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
        "artifacts": _list_artifacts(),
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
        "decision_reasons": reasons,
        "determinism": {"master_seed": SEED,
                        "order_archive": "artifacts/A-SEEDED-ORDER.json",
                        "per_episode_rng": "random.Random(master_seed + episode_id)"},
        "producer_claim_status": "C-MEAS-VALID remains at the parent VALIDATED ceiling; this packet narrows or bounds the construct ceiling per outcome; no claim-registry edit, no product promotion by this packet",
    }
    with open(EXP_DIR / "result.json", "w") as f:
        json.dump(result, f, indent=2)
    return result


def write_report(derived: Dict[str, Any], bs: Dict[str, Any], recompute: Dict[str, Any],
                 ledger_result: Dict[str, Any], stability_pairs: List[Dict],
                 chromium: Dict[str, Any], reasons: List[str],
                 preflights: Dict[str, Any], cert: Dict[str, Any]) -> None:
    lines = [
        f"# EXP-RUNTIME-37973247935 — {outcome}", "",
        f"Lane: {LANE} | Claim: {CLAIM_ID} | Director mandate: CONTINUE, C-MEAS-VALID", "",
        "## Question",
        "Does the composite intervention oracle retain arm-constrained discrimination "
        "(point sensitivity/specificity >= 0.90, two-sided 95% Wilson lo >= 0.80, zero false "
        "positives, arm-blind, zero recompute mismatches) when the change is induced OUTSIDE the "
        "surface the detector's author wrote, and does a powered write-then-revert probe measure "
        "the byte-equality blind spot in both directions?", "",
        "## Decision",
        f"status={status} outcome={outcome}", f"reasons={reasons}", "",
        "## Per-arm results (n=40 positives/null, n=20 liveness; two-sided 95% Wilson)",
    ]
    for a in EC.ALL_MATRIX_ARMS:
        r = derived["arms"][a]
        lines.append(f"- {a} ({r['estimand']}): k={r['k']}/{r['n_scored']} point={r['point_rate']} "
                     f"Wilson95=[{r['wilson_ci_lo']}, {r['wilson_ci_hi']}] nondegenerate={r['ci_nondegenerate']}")
    lines += [
        "", f"null false positives total = {derived['null_false_positives_total']} "
            f"(requirement 0/120)",
        f"liveness control sensitivity = {derived['liveness_control']['sensitivity']} (requirement 1.0)",
        f"recompute zero_mismatches = {recompute.get('zero_mismatches')}",
        f"capability ledger required scopes pass = {ledger_result.get('ledger_ok')}",
        f"capture stability pairs all byte-identical = "
        f"{bool(stability_pairs and all(p.get('all_identical') for p in stability_pairs))}",
        f"chromium sha256 matches frozen = {chromium.get('sha256_matches_frozen')}",
        "", "## Blind-spot probe (measured; never gates)",
    ]
    for s in EC.BLINDSPOT_ARMS:
        lines.append(f"- {s}: detection_fraction={bs[s]['detection_fraction']} "
                     f"Wilson95=[{bs[s]['wilson_ci_lo']}, {bs[s]['wilson_ci_hi']}] "
                     f"write_confirmed_all={bs[s]['write_confirmed_all']} "
                     f"revert_bytes_identical_all={bs[s]['revert_bytes_identical_all']} "
                     f"(prediction: {bs[s]['directional_prediction']})")
    lines += [
        f"- both directional predictions contradicted = {bs.get('both_directional_predictions_contradicted')}",
        "", "## Controls / preflights",
    ]
    for c in preflights.get("checks", []):
        lines.append(f"- {c['id']}: pass={c['pass']} detail={json.dumps(c.get('detail'))}")
    lines += [
        "", "## Interpretation (bounded to the frozen claim)",
        "SUPPORTS would narrow the construct bound: the oracle detects committed state "
        "transitions it did not author, at the quoted ceiling; downstream lanes (Graph "
        "C-FRESHNESS / C-DELTA-REPAIR, Physics certification) may preregister the substrate "
        "at the new explicit ceiling; no product promotion.",
        "MIXED/FALSIFIES would narrow the ceiling to what this particular fixture does and "
        "route downstream work to a redesigned detector or a different substrate.",
        "INCONCLUSIVE / MEASUREMENT_INVALID are infrastructure/validity results, never "
        "scientific negatives.", "",
        f"Representation loss recorded: {len(validity_notes)} validity notes; "
        f"unresolved: {len(unresolved)}",
    ]
    with open(EXP_DIR / "report.md", "w") as f:
        f.write("\n".join(lines) + "\n")


def write_provenance(chromium: Dict[str, Any], durability: Dict[str, Any],
                     recompute: Dict[str, Any]) -> None:
    worktree = subprocess.run(["git", "status", "--short"], capture_output=True, text=True,
                              cwd=str(REPO_ROOT)).stdout.strip()
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                          cwd=str(REPO_ROOT)).stdout.strip()
    python_ver = sys.version.split()[0]
    prov = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "run_id": RUN_ID,
        "generated_at": _utc(),
        "base_sha": "7d87e40d51710c47f6fde0464a6834cb27056c3b",
        "head_sha": head,
        "worktree_status": worktree,
        "seeds": {"master_seed": SEED, "episode_order": f"random.Random({SEED}).shuffle(...)",
                  "per_episode": "master_seed + episode_id"},
        "frozen_inputs": {
            "request.json": _sha_file(EXP_DIR / "request.json"),
            "spec.json": _sha_file(EXP_DIR / "spec.json"),
            "prereg.md": _sha_file(EXP_DIR / "prereg.md"),
            "freeze.json": _sha_file(EXP_DIR / "freeze.json"),
        },
        "components": {
            "intervention_surface.py": _sha_file(Path(SURFACE.__file__)),
            "oracle_scorer.py": _sha_file(Path(ORACLE.__file__)),
            "shared_config.py": _sha_file(Path(SC.__file__ if hasattr(SC, "__file__") else "")),
            "oos_worker.py": _sha_file(Path(OOS.__file__)),
            "bringup.py": _sha_file(Path(REPO_ROOT) / "research/runtime/bringup.py"),
            "run_experiment.py": _sha_file(EXP_DIR / "run_experiment.py"),
            "exp_config.py": _sha_file(EXP_DIR / "exp_config.py"),
            "bringup_contract.json": _sha_file(EXP_DIR / "bringup_contract.json"),
        },
        "environment": {
            "python": python_ver, "platform": sys.platform,
            "flask_pin": "3.1.3", "pyjwt_pin": "2.15.0", "gunicorn_pin": "23.0.0",
            "playwright_pin": PLAYWRIGHT_PIN, "nginx_version": "1.24.0",
        },
        "browser": chromium,
        "substrate": {
            "upstreams": ["127.0.0.1:19860", "127.0.0.1:19861"],
            "nginx_listen": "127.0.0.1:19851",
            "database_path": DB_PATH, "journal_mode": "WAL", "wal_autocheckpoint": 0,
            "wal_bytes_diagnostic": "recorded per episode in A-WAL-VECTOR-BEFORE-AFTER.jsonl",
        },
        "commands": {
            "bringup": f"python -m research.runtime.bringup --config "
                       f"research/experiments/{EXPERIMENT_ID}/bringup_contract.json --ledger "
                       f"research/experiments/{EXPERIMENT_ID}/artifacts/capability_ledger.json",
            "recompute": f"python {EXP_DIR}/recompute_check.py",
            "run": f"python {EXP_DIR}/run_experiment.py",
        },
        "durability": durability,
        "recompute": recompute,
        "artifacts": _list_artifacts(),
    }
    with open(EXP_DIR / "provenance.json", "w") as f:
        json.dump(prov, f, indent=2)


def _write_minimal_outputs(reasons: List[str]) -> None:
    result = {
        "schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
        "status": status, "outcome": outcome,
        "metrics": all_metrics, "controls": all_controls, "artifacts": _list_artifacts(),
        "observations": observations, "validity_notes": validity_notes,
        "unresolved": unresolved, "decision_reasons": reasons,
    }
    with open(EXP_DIR / "result.json", "w") as f:
        json.dump(result, f, indent=2)
    with open(EXP_DIR / "report.md", "w") as f:
        f.write(f"# EXP-RUNTIME-37973247935\n\nstatus={status} outcome={outcome}\n\n"
                f"reasons={reasons}\n\nvalidity_notes={validity_notes}\n")
    write_provenance({}, {"disposition": "NOT_RUN", "scientific_effect": "none"},
                     {"zero_mismatches": False, "summary": {"error": "experiment did not complete"}})


# ── Small orchestration helpers ────────────────────────────────────────────
def _nginx_masters() -> Dict[str, Any]:
    out = subprocess.run(["ps", "-eo", "pid,cmd"], capture_output=True, text=True,
                         timeout=10, cwd=str(REPO_ROOT)).stdout
    ours, foreign = [], []
    for line in out.splitlines():
        if "nginx: master process" in line:
            (ours if str(NGINX_CONF) in line else foreign).append(line.strip())
    return {"ours": ours, "foreign": foreign,
            "exclusive": len(ours) == 1 and not foreign}


def _verify_chromium() -> Dict[str, Any]:
    exe = Path(CHROMIUM_CANONICAL)
    rec = {"executable_path": CHROMIUM_CANONICAL, "exists": exe.exists(),
           "frozen_sha256": CHROMIUM_SHA256, "playwright_pin": PLAYWRIGHT_PIN,
           "browser_version": None, "sha256_matches_frozen": False}
    if exe.exists():
        h = _sha_file(exe)
        rec["actual_sha256"] = h
        rec["sha256_matches_frozen"] = (h == CHROMIUM_SHA256)
    return rec


def _run_recompute() -> Dict[str, Any]:
    out = {"command": f"python {EXP_DIR}/recompute_check.py", "executed_at": _utc(),
           "completed": False}
    try:
        proc = subprocess.run([sys.executable, str(EXP_DIR / "recompute_check.py")],
                              capture_output=True, text=True, timeout=900, cwd=str(REPO_ROOT))
        out["exit_status"] = proc.returncode
        out["stdout_tail"] = proc.stdout[-3000:]
        out["stderr_tail"] = proc.stderr[-3000:]
        rc_path = ART_DIR / "A-RECOMPUTE-CHECK.json"
        out["recompute_check_written"] = rc_path.exists()
        if rc_path.exists():
            try:
                rc = json.loads(rc_path.read_text())
                out["zero_mismatches"] = rc.get("zero_mismatches")
                out["summary"] = rc.get("summary")
                out["completed"] = out["zero_mismatches"] is not None
            except Exception as e:
                out["exception"] = f"{type(e).__name__}: {e}"
    except Exception as e:
        out["exception"] = f"{type(e).__name__}: {e}"
    return out


def _fail(rc: int, st: str, oc: str, reason: str) -> int:
    global status, outcome
    status, outcome = st, oc
    validity_notes.append(reason)
    print(f"[FAIL] {st}/{oc}: {reason}", flush=True)
    _write_minimal_outputs([reason])
    return rc


# ── Main orchestration (single-command frozen execution) ───────────────────
def main() -> int:
    global status, outcome, ledger_result, all_metrics, anchor_conn
    status, outcome = "COMPLETE", "INCONCLUSIVE"
    ART_DIR.mkdir(parents=True, exist_ok=True)
    start_t = _utc()
    print("=" * 78, flush=True)
    print(f"EXP-RUNTIME-37973247935 lane=runtime claim={CLAIM_ID} seed={SEED}", flush=True)
    print(f"started {start_t}", flush=True)
    print("=" * 78, flush=True)

    reasons: List[str] = []
    use_sudo = _sudo_ok()
    observations.append(f"sudo available: {use_sudo}")
    ok, msg = acquire_run_lock()
    if not ok:
        return _fail(2, "BLOCKED", "INCONCLUSIVE", f"run lock: {msg}")
    observations.append("run lock acquired")

    browser = None
    pw = None
    try:
        _kill_owned()
        _clean_canonical_paths()
        time.sleep(0.5)

        # ── Phase 0: substrate bring-up (gunicorn x2 -> exclusive nginx) ──
        observations.append("substrate: writing nginx conf, starting gunicorn x2 (19860/19861), "
                            "starting nginx (19851, exclusive)")
        try:
            _write_nginx_conf(use_sudo)
            for p in _start_gunicorn(use_sudo):
                owned_procs.append(p)
            nginx_ok = False
            for _ in range(3):
                t = subprocess.run(["sudo", "nginx", "-t", "-c", str(NGINX_CONF)] if use_sudo
                                   else ["nginx", "-t", "-c", str(NGINX_CONF)],
                                   capture_output=True, text=True, timeout=15)
                if t.returncode == 0:
                    nginx_ok = True
                    break
                time.sleep(1.0)
            if not nginx_ok:
                return _fail(3, "BLOCKED", "INCONCLUSIVE",
                             f"nginx -t failed for {NGINX_CONF}: {t.stdout[-500:]} {t.stderr[-500:]}")
            if use_sudo:
                subprocess.run(["sudo", "nginx", "-c", str(NGINX_CONF)], capture_output=True, timeout=10)
            else:
                subprocess.run(["nginx", "-c", str(NGINX_CONF)], capture_output=True, timeout=10)
        except Exception as e:
            return _fail(3, "BLOCKED", "INCONCLUSIVE",
                         f"substrate bring-up failure: {type(e).__name__}: {e}")
        time.sleep(1.0)

        # ── Phase 0b: health gates + exclusivity ──
        ng_ok, ng_logs = _health_gate()
        all_controls["V-HEALTH-GATE"] = {"expected": "nginx 19851 200 + X-Worker-Pid",
                                         "observed": json.dumps(ng_logs[-3:]), "pass": ng_ok,
                                         "evidence": "phase 0b gate logs"}
        origins: Dict[int, bool] = {}
        for port in FLASK_PORTS:
            o_ok, o_logs = _origin_health_gate(port)
            origins[port] = o_ok
            observations.append(f"origin {port} health: {o_ok} "
                                f"(worker={o_logs[-1]['worker'] if o_logs else 'n/a'})")
        two_origins = all(origins.values())
        masters = _nginx_masters()
        exclusive = bool(masters["exclusive"])
        all_controls["NC-EXCLUSIVE-NGINX"] = {"expected": "exactly one nginx master, ours",
                                              "observed": json.dumps(masters), "pass": exclusive,
                                              "evidence": "phase 0b ps scan"}
        all_controls["V-UPSTREAM-2-SERVERS"] = {"expected": "both origins 200 via nginx",
                                                "observed": json.dumps(origins), "pass": two_origins,
                                                "evidence": "phase 0b origin health gates"}
        all_metrics["substrate"] = {"nginx_masters": masters, "origins_ok": origins}
        if not (ng_ok and two_origins and exclusive):
            return _fail(3, "BLOCKED", "INCONCLUSIVE",
                         "health gate / exclusive-nginx / 2-upstream gate failed")

        # ── Phase 1: readiness certificate + cache corroboration ──
        readiness_sid = f"readiness_{RUN_ID}"
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
                   body={"sid": readiness_sid, "action": "upsert"})
        valid_token = SURFACE.make_valid_token(readiness_sid)
        cert = run_readiness_certificate(valid_token)
        cert["cache_corroboration"] = cache_corroboration()
        with open(ART_DIR / "A-READINESS-CERTIFICATE.json", "w") as f:
            json.dump(cert, f, indent=2)
        all_metrics["readiness"] = {k: cert.get(k) for k in
                                    ("n_total", "n_non304", "per_ep_non304",
                                     "n_distinct_x_worker_pid", "min_per_uri_stickiness",
                                     "n_distinct_uris", "pass")}
        observations.append(f"readiness certificate: pass={cert['pass']} "
                            f"n_non304={cert['n_non304']} distinct_workers={cert['n_distinct_x_worker_pid']} "
                            f"stickiness={cert['min_per_uri_stickiness']}")
        if not cert["pass"]:
            return _fail(3, "BLOCKED", "INCONCLUSIVE",
                         "readiness certificate not satisfied (distributed substrate did not reach frozen floors)")

        # ── Phase 2: capability ledger (release lock; bringup takes its own) ──
        release_run_lock()
        try:
            ledger_result = run_capability_ledger()
        finally:
            acquire_run_lock()
        all_metrics["capability_ledger"] = {"ledger_ok": ledger_result.get("ledger_ok"),
                                            "scopes": ledger_result.get("receipt", {}).get("scopes")}
        if not ledger_result.get("ledger_ok"):
            return _fail(3, "BLOCKED", "INCONCLUSIVE",
                         "capability ledger required scopes not satisfied (bringup one-command contract failed)")

        # ── Phase 3: attainability reproduction + control-liveness preflight ──
        attain = run_attainability_certificate()
        accept = attain["out_of_surface_positive_accept_region"]
        preflight_repro = (accept["min_k"] == 37)
        cl = run_control_liveness(cert)
        all_metrics["preflights"] = {"attainability_accept_min_k_reproduced_37": preflight_repro,
                                     "control_liveness_all_pass": cl["all_pass"],
                                     "checks": cl["checks"]}
        observations.append(f"attainability accept min_k={accept['min_k']} (frozen 37); "
                            f"control-liveness all_pass={cl['all_pass']}")
        if not (preflight_repro and cl["all_pass"]):
            return _fail(4, "MEASUREMENT_INVALID", "INCONCLUSIVE",
                         "control-liveness preflight or attainability reproduction failed")

        # ── Phase 4: anchor WAL connection (last-close checkpoint guard) ──
        anchor_conn = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
        anchor_conn.execute("PRAGMA wal_autocheckpoint=0")
        anchor_conn.execute("SELECT 1")
        observations.append("anchor sqlite connection held open across the matrix "
                            "(prevents WAL last-close checkpoint/deletion)")

        # ── Phase 5: frozen Chromium verification + launch ──
        chromium = _verify_chromium()
        all_metrics["chromium"] = chromium
        if not chromium["sha256_matches_frozen"]:
            return _fail(3, "BLOCKED", "INCONCLUSIVE",
                         f"chromium sha256 mismatch: {chromium.get('actual_sha256')}")
        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start()
        browser = pw.chromium.launch(executable_path=CHROMIUM_CANONICAL,
                                     args=["--no-sandbox", "--disable-dev-shm-usage"])
        chromium["launch_ok"] = True
        chromium["browser_version"] = browser.version
        with open(ART_DIR / "B-PLAYWRIGHT-CAPABILITY.json", "w") as f:
            json.dump(chromium, f, indent=2)
        observations.append(f"chromium {browser.version} launched")

        # ── Phase 6: frozen matrix (260 episodes + 20 interleaved stability pairs) ──
        try:
            matrix = run_matrix(browser)
        except Exception as e:
            return _fail(1, "BLOCKED", "INCONCLUSIVE",
                         f"matrix infrastructure failure: {type(e).__name__}: {e}")

        # ── Phase 7: capture-stability gate (any non-identical no-action pair) ──
        stability_pairs = matrix["stability_pairs"]
        stability_ok = bool(len(stability_pairs) == EC.CAPTURE_STABILITY_PAIRS
                            and all(p.get("all_identical") for p in stability_pairs))
        observations.append(f"capture stability: {len(stability_pairs)} pairs, "
                            f"all_identical={stability_ok}")
        if not stability_ok:
            return _fail(4, "MEASUREMENT_INVALID", "INCONCLUSIVE",
                         "capture stability gate failed: a no-action pair was not byte-identical")

        # ── Phase 8: static authorship / anti-synthetic checks ──
        authorship = check_authorship_separation()
        oos_unreachable = check_oos_unreachable_from_scorer()
        synthetic = check_no_synthetic_fallback()
        for name, rec in (("A-AUTHORSHIP-CHECK.json", authorship),
                          ("A-OOS-UNREACHABLE.json", oos_unreachable),
                          ("A-SYNTHETIC-CHECK.json", synthetic)):
            with open(ART_DIR / name, "w") as f:
                json.dump(rec, f, indent=2)
        observations.append(f"authorship pass={authorship['pass']} "
                            f"oos_unreachable pass={oos_unreachable['pass']} "
                            f"synthetic pass={synthetic['pass']}")

        # ── Phase 9: arm-blind derived metrics (label join AFTER detector output) ──
        order_archive = json.loads((ART_DIR / "A-SEEDED-ORDER.json").read_text())
        arm_by_order = {o["order_index"]: o["arm"] for o in order_archive["order"]}
        derived = score_arms(matrix["detector_records"], arm_by_order)
        bs = blindspot_metrics(matrix["blindspot_records"])
        det_lines = (ART_DIR / "A-DETECTOR-OUTPUT.jsonl").read_text().splitlines()
        arm_blind_ok = bool(det_lines) and all("arm" not in json.loads(l) for l in det_lines)
        derived["arm_blind_output_has_no_arm_label"] = arm_blind_ok
        with open(ART_DIR / "A-DERIVED-METRICS.json", "w") as f:
            json.dump({"derived": derived, "blindspot": bs}, f, indent=2)
        observations.append(f"arm-blind detector output: no arm label present={arm_blind_ok}")

        # Representative first-completed before/after WAL evidence per arm
        arm_seen: set = set()
        wal_evidence = []
        for w in matrix["wal_records"]:
            if w["arm"] not in arm_seen and w.get("before_hash") and w.get("after_hash"):
                arm_seen.add(w["arm"])
                wal_evidence.append(w)
        _write_jsonl("B-WAL-EVIDENCE.jsonl", wal_evidence)

        # ── Phase 10: independent recompute (falsifier iii) ──
        recompute = _run_recompute()
        if not recompute.get("completed"):
            return _fail(3, "BLOCKED", "INCONCLUSIVE",
                         f"recompute subprocess did not complete: {recompute.get('exception')}")
        observations.append(f"recompute zero_mismatches={recompute.get('zero_mismatches')}")
        all_metrics["recompute"] = recompute

        # ── Phase 11: durability record ──
        durability = run_durability_check()
        all_metrics["durability"] = durability
        observations.append(f"durability: {durability['disposition']} "
                            f"all_frozen_scope_head_resident={durability['all_frozen_scope_head_resident']}")

        # ── Phase 12: frozen decision mapping ──
        st, oc, reason_list = decide(
            derived, bs, recompute, bool(ledger_result.get("ledger_ok")),
            preflight_repro and bool(cl["all_pass"]), stability_ok,
            bool(authorship.get("pass")), bool(oos_unreachable.get("pass")),
            bool(synthetic.get("pass")), arm_blind_ok)
        status, outcome = st, oc
        validity_notes.extend(reason_list)
        reasons.extend(reason_list)
        observations.append(f"decision: status={status} outcome={outcome} reasons={reason_list}")

        # ── Phase 13: deterministic outputs ──
        write_result(derived, bs, recompute, ledger_result, stability_pairs, authorship,
                     oos_unreachable, synthetic, durability, chromium, reasons,
                     all_metrics["preflights"], cert)
        write_report(derived, bs, recompute, ledger_result, stability_pairs, chromium,
                     reasons, all_metrics["preflights"], cert)
        write_provenance(chromium, durability, recompute)
        print("=" * 78, flush=True)
        print(f"status={status} outcome={outcome}", flush=True)
        print(f"reasons={reasons}", flush=True)
        print(f"experiment finished {_utc()}", flush=True)
        print("=" * 78, flush=True)
        return 0
    except Exception as e:
        # Any unexpected infrastructure exception is BLOCKED/INCONCLUSIVE, never a
        # scientific negative; if the decision phase already ran we keep it and
        # record the writer-phase exception.
        if status == "COMPLETE" and outcome == "INCONCLUSIVE":
            return _fail(1, "BLOCKED", "INCONCLUSIVE",
                         f"unexpected infrastructure failure: {type(e).__name__}: {e}")
        observations.append(f"exception after decision phase: {type(e).__name__}: {e}")
        try:
            _write_minimal_outputs(reasons)
        except Exception:
            pass
        return 1
    finally:
        if browser is not None:
            try:
                browser.close()
            except Exception:
                pass
        if pw is not None:
            try:
                pw.stop()
            except Exception:
                pass
        if anchor_conn is not None:
            try:
                anchor_conn.close()
            except Exception:
                pass
            anchor_conn = None
        _kill_owned()
        _clean_canonical_paths()
        release_run_lock()
        observations.append(f"cleanup complete; started {start_t}, ended {_utc()}")


# ── Smoke bring-up/preflight (validates integration; NO outcome measurement) ─
def smoke_main() -> int:
    # Deliberately NOT diverting ART_DIR: phases 1-3 of the real run write
    # A-READINESS-CERTIFICATE.json / A-CONTROL-LIVENESS.json /
    # A-ATTAINABILITY-CERTIFICATE.json / C-BRINGUP-CONTRACT.json /
    # capability_ledger.json to the same paths, and the bring-up ledger reads the
    # certificate from `experiment_dir/artifacts/`, so an identical artifact set
    # is the faithful integration test. The real run regenerates all of them.
    use_sudo = _sudo_ok()
    ART_DIR.mkdir(parents=True, exist_ok=True)
    ok, msg = acquire_run_lock()
    if not ok:
        print(f"SMOKE FAIL: run lock: {msg}", flush=True)
        return 2
    browser = pw = None
    try:
        _kill_owned()
        _clean_canonical_paths()
        time.sleep(0.5)
        _write_nginx_conf(use_sudo)
        for p in _start_gunicorn(use_sudo):
            owned_procs.append(p)
        t = subprocess.run(["sudo", "nginx", "-t", "-c", str(NGINX_CONF)] if use_sudo
                           else ["nginx", "-t", "-c", str(NGINX_CONF)],
                           capture_output=True, text=True, timeout=15)
        if t.returncode:
            raise RuntimeError(f"nginx -t: {t.stdout[-300:]} {t.stderr[-300:]}")
        if use_sudo:
            subprocess.run(["sudo", "nginx", "-c", str(NGINX_CONF)], capture_output=True, timeout=10)
        else:
            subprocess.run(["nginx", "-c", str(NGINX_CONF)], capture_output=True, timeout=10)
        time.sleep(1.0)
        ng_ok, ng_logs = _health_gate()
        origins = {p: _origin_health_gate(p)[0] for p in FLASK_PORTS}
        masters = _nginx_masters()
        print(f"[SMOKE] health nginx={ng_ok} origins={origins} "
              f"exclusive={masters['exclusive']}", flush=True)
        if not (ng_ok and all(origins.values()) and masters["exclusive"]):
            raise RuntimeError("health/exclusive/upstream gates")

        sid = f"smoke_{RUN_ID}"
        _http_json("POST", f"http://127.0.0.1:{FLASK_PORTS[0]}/admin/session",
                   body={"sid": sid, "action": "upsert"})
        cert = run_readiness_certificate(SURFACE.make_valid_token(sid))
        cert["cache_corroboration"] = cache_corroboration()
        with open(ART_DIR / "A-READINESS-CERTIFICATE.json", "w") as f:
            json.dump(cert, f, indent=2)
        print(f"[SMOKE] readiness pass={cert['pass']} n_non304={cert['n_non304']} "
              f"workers={cert['n_distinct_x_worker_pid']} "
              f"stickiness={cert['min_per_uri_stickiness']} "
              f"miss_then_hit={cert['cache_corroboration'].get('miss_then_hit')}", flush=True)
        if not cert["pass"]:
            raise RuntimeError("readiness certificate")

        release_run_lock()
        try:
            ledger_result = run_capability_ledger()
        finally:
            acquire_run_lock()
        print(f"[SMOKE] ledger_ok={ledger_result.get('ledger_ok')}", flush=True)
        if not ledger_result.get("ledger_ok"):
            raise RuntimeError("capability ledger")

        attain = run_attainability_certificate()
        acc = attain["out_of_surface_positive_accept_region"]
        print(f"[SMOKE] attainability min_k={acc['min_k']} (frozen 37)", flush=True)
        cl = run_control_liveness(cert)
        print(f"[SMOKE] control_liveness all_pass={cl['all_pass']}", flush=True)
        for c in cl["checks"]:
            print(f"  {c['id']}: pass={c['pass']} detail={json.dumps(c.get('detail'))[:220]}", flush=True)
        if not cl["all_pass"]:
            raise RuntimeError("control-liveness preflight")

        chromium = _verify_chromium()
        print(f"[SMOKE] chromium sha match={chromium['sha256_matches_frozen']}", flush=True)
        if not chromium["sha256_matches_frozen"]:
            raise RuntimeError("chromium sha256")
        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start()
        browser = pw.chromium.launch(executable_path=CHROMIUM_CANONICAL,
                                     args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx, page, cdp = _episode_page(browser, "smoke_round_page", kind="readonly")
        _fixture_setup("smoke_round")
        comp = _browser_composite(page, SURFACE.make_valid_token("smoke_round"))
        domax = capture_dom_ax(cdp)
        legs_ok = (len(comp["legs"]) == 2
                   and all(l["status"] == 200 and l["fingerprint_sha256"] for l in comp["legs"]))
        print(f"[SMOKE] composite statuses={[l['status'] for l in comp['legs']]} "
              f"legs_ok={legs_ok} dom_nodes={domax['dom_nodes']} ax_nodes={domax['ax_nodes']}",
              flush=True)
        ctx.close()
        if not legs_ok:
            raise RuntimeError("composite capture")
        print("SMOKE OK", flush=True)
        return 0
    except Exception as e:
        print(f"SMOKE FAIL: {type(e).__name__}: {e}", flush=True)
        return 1
    finally:
        if browser is not None:
            try:
                browser.close()
            except Exception:
                pass
        if pw is not None:
            try:
                pw.stop()
            except Exception:
                pass
        _kill_owned()
        _clean_canonical_paths()
        release_run_lock()


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        sys.exit(smoke_main())
    sys.exit(main())


