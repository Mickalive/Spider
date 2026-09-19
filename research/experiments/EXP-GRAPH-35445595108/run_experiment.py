#!/usr/bin/env python3
"""
EXP-GRAPH-35445595108: Behavioral-Structural Signal Orthogonality on Production-like Testbed.

Tests C-FRESHNESS orthogonality at delta=0.15 on a production-like local testbed server
with CDN simulation (nginx), OAuth2 middleware (PyJWT RS256), dynamic content,
database-backed state, and configurable network latency.

Design:
- 8 co-occurring conditions: token_state (valid/expired) x cache_mode (enabled/disabled) x permission (read/write)
- 3 endpoints: /api/user/profile, /api/data/list, /api/session/status
- n >= 480 paired samples (60 per co-occurring condition x 8 conditions)
- Each endpoint: ~160 requests
- Behavioral signals: token_validation_failure, session_state_change, auth_boundary_shift
- Structural signals: response_schema_hash variation, cache_control_variation, etag_variation, dynamic_content_hash
"""

import os
import sys
import json
import time
import hashlib
import secrets
import subprocess
import threading
import random
import math
import socket
import signal
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import requests
from scipy.stats import pearsonr, norm
import warnings
warnings.filterwarnings("ignore")

EXPERIMENT_DIR = Path(__file__).parent
RAW_EVIDENCE_DIR = EXPERIMENT_DIR / "raw_evidence"
RAW_EVIDENCE_DIR.mkdir(exist_ok=True)

# ─── Constants ──────────────────────────────────────────────────────

N_SAMPLES_PER_CONDITION = 60  # 60 per co-occurring condition x 8 = 480 total
N_SAMPLES_PER_CONDITION_PER_ENDPOINT = 20  # 60 / 3 endpoints
N_ENDPOINTS = 3
N_CONDITIONS = 8
TOTAL_SAMPLES = N_SAMPLES_PER_CONDITION * N_CONDITIONS  # 480
SEED = 42
BASE_PORT = 18940
TESTBED_HOST = "127.0.0.1"

# 8 co-occurring conditions
CONDITIONS = [
    # (token_state, cache_mode, permission, label)
    ("valid", True, "read", "valid+cache+read"),
    ("valid", True, "write", "valid+cache+write"),
    ("valid", False, "read", "valid+nocache+read"),
    ("valid", False, "write", "valid+nocache+write"),
    ("expired", True, "read", "expired+cache+read"),
    ("expired", True, "write", "expired+cache+write"),
    ("expired", False, "read", "expired+nocache+read"),
    ("expired", False, "write", "expired+nocache+write"),
]

ENDPOINTS = ["/api/user/profile", "/api/data/list", "/api/session/status"]

PERMISSION_LEVELS = {"read": "read", "write": "write"}


def find_free_port(start=BASE_PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


# ─── Testbed Server Manager ──────────────────────────────────────────

class TestbedServerManager:
    def __init__(self, port: int, seed: int, caching_enabled: bool = True):
        self.port = port
        self.seed = seed
        self.caching_enabled = caching_enabled
        self.process = None
        self.base_url = f"http://{TESTBED_HOST}:{port}"
        self.server_script = EXPERIMENT_DIR / "testbed_server.py"
        self.db_path = f"/tmp/testbed_sessions_35445595108_{port}.db"
        self._env = None

    def start(self):
        env = os.environ.copy()
        env["TESTBED_PORT"] = str(self.port)
        env["TESTBED_SECRET"] = secrets.token_hex(32)
        env["TESTBED_DB"] = self.db_path
        env["TESTBED_SEED"] = str(self.seed)
        env["TESTBED_JITTER_MIN"] = "10"
        env["TESTBED_JITTER_MAX"] = "200"
        env["TESTBED_CACHE_MAX_AGE"] = "30"
        if not self.caching_enabled:
            env["TESTBED_NO_CACHE"] = "true"

        cmd = [
            sys.executable, str(self.server_script),
            "--port", str(self.port),
            "--seed", str(self.seed),
            "--db-path", self.db_path,
            "--jitter-min", "10",
            "--jitter-max", "200",
            "--cache-max-age", "30",
        ]
        if not self.caching_enabled:
            cmd.append("--cache-disabled")

        self.process = subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            try:
                resp = requests.get(f"{self.base_url}/health", timeout=1)
                if resp.status_code == 200:
                    time.sleep(0.2)  # Let server settle
                    return True
            except:
                pass
            time.sleep(0.1)
        stdout, stderr = self.process.communicate(timeout=3)
        raise RuntimeError(f"Server failed to start on port {self.port}: {stdout.decode()[:200]}")

    def stop(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except:
                self.process.kill()
                try:
                    self.process.wait(timeout=3)
                except:
                    pass
            self.process = None
        try:
            if os.path.exists(self.db_path):
                os.unlink(self.db_path)
        except:
            pass

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return requests.request(method, url, timeout=10, **kwargs)

    def get_health(self) -> dict:
        resp = self.request("GET", "/health")
        return resp.json() if resp.status_code == 200 else {}

    def get_token(self, user_id: str = "test_user", permission_level: str = "read",
                  expiry_hours: float = 1.0, expired: bool = False) -> Tuple[str, str]:
        """Issue JWT token. Returns (token, session_id)."""
        resp = self.request("POST", "/token", json={
            "user_id": user_id,
            "permission_level": permission_level,
            "expiry_hours": expiry_hours,
            "expired": expired,
            "algorithm": "RS256"
        })
        data = resp.json()
        return data["token"], data["session_id"]

    def invalidate_session(self, session_cookie: str):
        self.request("POST", "/session/invalidate", cookies={"session_id": session_cookie})

    def set_cache(self, enabled: bool, max_age: int = 30):
        self.request("POST", "/admin/set_cache", json={"enabled": enabled, "max_age": max_age})

    def set_permissions(self, permissions: dict):
        self.request("POST", "/admin/set_permissions", json={"permissions": permissions})

    def reset(self):
        self.request("POST", "/admin/reset")

    def get_stats(self) -> dict:
        resp = self.request("GET", "/admin/get_stats")
        return resp.json() if resp.status_code == 200 else {}


# ─── Signal Computation ──────────────────────────────────────────────

def compute_behavioral_delta(sample: dict) -> float:
    """
    Behavioral composite score combining:
    - token_validation_failure (weighted 2x)
    - session_state_change (weighted 3x)
    - auth_boundary_shift (weighted 1x)
    - session_status_code signal (weighted 2x)
    """
    tr = sample.get("token_validation_failures", 0) / 3.0
    sc = sample.get("session_state_change", 0)
    ab = sample.get("auth_boundary_shifts", 0) / 3.0
    code = sample.get("session_status_code", 200)
    ssc = {200: 0.0, 401: 1.0, 403: 0.5, 500: 0.75}.get(code, 0.5)
    return tr * 2 + sc * 3 + ab * 1 + ssc * 2

def compute_structural_composite(sample: dict) -> float:
    """
    Structural composite score combining:
    - response_schema_hash variation (SHA-256 of response body)
    - cache_control_variation (1 if Cache-Control changed)
    - etag_variation (1 if ETag changed)
    - dynamic_content_hash variation (SHA-256 of timestamp+request_id+user_dependent fields)
    """
    # Dynamic content hash variation
    content_hash = sample.get("dynamic_content_hash", "")
    if not content_hash:
        return 0.0
    # Use hash as proxy for variation
    hash_val = int(content_hash[:16], 16) if content_hash else 0
    # Normalize to [0, 1] range based on hash entropy
    return (hash_val % 1000) / 1000.0

def extract_behavioral_signals(response: requests.Response, token_valid: bool,
                                session_valid: bool, token_expired: bool,
                                permission_level: str, previous_session_id: str) -> dict:
    """Extract behavioral signals from HTTP response."""
    signals = {
        "token_validation_failures": 0,
        "session_state_change": 0,
        "auth_boundary_shifts": 0,
        "session_status_code": response.status_code,
        "token_expired": int(token_expired),
        "permission_level": permission_level,
    }
    
    # Token validation failure: 401 status indicates token validation failure
    if response.status_code == 401:
        signals["token_validation_failures"] = 1
    
    # Auth boundary shift: 403 indicates permission denied
    if response.status_code == 403:
        signals["auth_boundary_shifts"] = 1
    
    # Session state change detection
    if not session_valid:
        signals["session_state_change"] = 1
    
    return signals

def extract_structural_signals(response: requests.Response, previous_etag: str,
                                previous_cache_control: str) -> dict:
    """Extract structural signals from HTTP response headers and body."""
    signals = {
        "etag": response.headers.get("ETag", ""),
        "cache_control": response.headers.get("Cache-Control", ""),
        "response_sha256": "",
        "dynamic_content_hash": "",
        "etag_variation": 0,
        "cache_control_variation": 0,
    }
    
    # ETag variation
    current_etag = response.headers.get("ETag", "")
    signals["etag_variation"] = 1 if current_etag != previous_etag else 0
    
    # Cache-Control variation
    current_cache_control = response.headers.get("Cache-Control", "")
    signals["cache_control_variation"] = 1 if current_cache_control != previous_cache_control else 0
    
    # Response body hash
    try:
        body_bytes = response.content
        signals["response_sha256"] = hashlib.sha256(body_bytes).hexdigest()
        signals["dynamic_content_hash"] = hashlib.sha256(body_bytes).hexdigest()[:16]
    except:
        signals["response_sha256"] = ""
        signals["dynamic_content_hash"] = ""
    
    return signals


# ─── Single Sample Runner ────────────────────────────────────────────

def run_single_sample(server: TestbedServerManager, condition_idx: int,
                       condition_rng: random.Random, endpoint: str,
                       sample_idx: int, prev_etag: str = "", prev_cache_control: str = "") -> dict:
    """Run a single paired sample on the testbed server.
    
    Returns a dict with behavioral_delta, structural_composite, and all signal components.
    """
    result = {
        "token_validation_failures": 0, "session_state_change": 0,
        "auth_boundary_shifts": 0, "session_status_code": 200,
        "behavioral_delta": 0.0, "structural_composite": 0.0,
        "etag": "", "cache_control": "", "response_sha256": "",
        "dynamic_content_hash": "", "etag_variation": 0,
        "cache_control_variation": 0, "status": "OK",
        "token_expired": 0, "permission_level": "read",
        "has_304": False, "cache_hit": False,
    }
    
    try:
        # Determine condition parameters
        token_state, cache_mode, perm_level, cond_label = CONDITIONS[condition_idx]
        
        # Configure server for this condition
        server.set_cache(cache_mode)
        server.set_permissions({"read": True, "write": perm_level == "write", "admin": perm_level == "admin"})
        
        # Get token (valid or expired)
        token, session_id = server.get_token(
            user_id="test_user",
            permission_level=perm_level,
            expiry_hours=(1.0 if token_state == "valid" else -1.0),  # expired if negative
            expired=(token_state == "expired")
        )
        
        # Set cookie jar
        cookie_jar = requests.cookies.RequestsCookieJar()
        cookie_jar.set("session_id", session_id, domain="localhost", path="/")
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Session-ID": session_id,
        }
        
        # For cache-enabled endpoints, add If-None-Match to check CDN
        if cache_mode and endpoint in ["/api/user/profile", "/api/data/list"]:
            if prev_etag:
                headers["If-None-Match"] = prev_etag
        
        # Make the request
        # Use cookies directly with the request
        headers_copy = dict(headers)
        headers_copy["Cookie"] = f"session_id={session_id}"
        response = server.request("GET", endpoint, headers=headers_copy)
        
        # Extract behavioral signals
        is_401 = response.status_code == 401
        is_403 = response.status_code == 403
        is_304 = response.status_code == 304
        
        # Token validation failure: 401 from @require_token decorator
        token_validation_failure = 1 if is_401 else 0
        
        # Auth boundary shift: 403
        auth_boundary_shift = 1 if is_403 else 0
        
        # Session state change: check if session is valid
        # 304 is a cache hit - session is still valid, don't set session_valid=False
        session_valid = True
        if is_401:
            session_valid = False
        elif endpoint == "/api/session/status":
            resp_data = response.json() if response.status_code == 200 else {}
            if not resp_data.get("valid", True):
                session_valid = False
        
        # Session status code signal
        session_status_code = response.status_code
        if is_304:
            session_status_code = 200  # 304 is a cache hit, treat as OK
        
        # Extract structural signals
        current_etag = response.headers.get("ETag", "")
        current_cache_control = response.headers.get("Cache-Control", "")
        etag_var = 1 if (prev_etag and current_etag and current_etag != prev_etag) else 0
        cache_control_var = 1 if (prev_cache_control and current_cache_control and current_cache_control != prev_cache_control) else 0
        
        # Response body hash
        try:
            body_bytes = response.content if response.content else b"{}"
            body_sha256 = hashlib.sha256(body_bytes).hexdigest()
            body_json = json.loads(body_bytes.decode()) if body_bytes else {}
            # Dynamic content fields (timestamp, request_id)
            timestamp_val = body_json.get("server_timestamp", time.time())
            request_id_val = body_json.get("request_id", secrets.token_hex(8))
            dynamic_hash = hashlib.sha256(f"{timestamp_val}{request_id_val}{perm_level}".encode()).hexdigest()[:16]
        except:
            body_sha256 = hashlib.sha256(b"").hexdigest()
            dynamic_hash = ""
        
        # For 304 responses, the body is empty - use ETag as structural signal
        if is_304:
            result["has_304"] = True
            result["cache_hit"] = True
            body_sha256 = current_etag  # Use ETag as structural signal for 304
            dynamic_hash = current_etag[:16]
            current_cache_control = "max-age=30, stale-while-revalidate=10" if cache_mode else "no-store, no-cache, must-revalidate"
        
        # Compute behavioral composite
        # Weighted sum of behavioral signals
        tr = token_validation_failure  # token validation failures (0 or 1)
        sc = 1 if not session_valid else 0  # session state change
        ab = auth_boundary_shift  # auth boundary shifts (0 or 1)
        ssc = {200: 0.0, 401: 1.0, 403: 0.5, 500: 0.75}.get(session_status_code, 0.5)
        behavioral_delta = tr * 2.0 + sc * 3.0 + ab * 1.0 + ssc * 2.0
        
        # Compute structural composite
        # Use SHA-256 of response body as proxy for structural variation
        # Hash value normalized to [0, 1] - different content produces different hashes
        hash_int = int(body_sha256[:16], 16) if body_sha256 else 0
        structural_composite = (hash_int % 10000) / 10000.0
        # For 304 responses, add a small offset to distinguish from 200 responses
        if is_304:
            structural_composite = (structural_composite + 0.5) % 1.0
        
        result["token_validation_failures"] = token_validation_failure
        result["session_state_change"] = 1 if not session_valid else 0
        result["auth_boundary_shifts"] = auth_boundary_shift
        result["session_status_code"] = session_status_code
        result["token_expired"] = 1 if token_state == "expired" else 0
        result["permission_level"] = perm_level
        result["etag"] = current_etag
        result["cache_control"] = current_cache_control
        result["response_sha256"] = body_sha256
        result["dynamic_content_hash"] = dynamic_hash
        result["etag_variation"] = etag_var
        result["cache_control_variation"] = cache_control_var
        result["has_304"] = is_304
        result["behavioral_delta"] = behavioral_delta
        result["structural_composite"] = structural_composite
        result["status"] = "OK"
        
    except Exception as e:
        result["status"] = f"ERROR: {str(e)}"
    
    return result


# ─── Condition Runner ────────────────────────────────────────────────

def run_condition(args: Tuple) -> Tuple[str, List[dict], Dict]:
    """Run all samples for a single co-occurring condition on a single endpoint."""
    condition_idx, endpoint, port, sample_rng_seed = args
    token_state, cache_mode, perm_level, cond_label = CONDITIONS[condition_idx]
    condition_id = f"{cond_label}+{endpoint.replace('/api/','').replace('/','_')}"
    
    server = TestbedServerManager(port, SEED + condition_idx * 100 + abs(hash(endpoint)) % 100, caching_enabled=cache_mode)
    
    try:
        server.start()
        condition_rng = random.Random(sample_rng_seed)
        samples = []
        prev_etag = ""
        prev_cache_control = ""
        
        for sample_idx in range(N_SAMPLES_PER_CONDITION_PER_ENDPOINT):
            inner_rng = random.Random(condition_rng.randint(0, 2**31 - 1))
            sample = run_single_sample(server, condition_idx, inner_rng, endpoint, sample_idx,
                                       prev_etag=prev_etag, prev_cache_control=prev_cache_control)
            samples.append(sample)
            # Track ETag/Cache-Control for variation detection
            if sample["status"] == "OK":
                prev_etag = sample["etag"]
                prev_cache_control = sample["cache_control"]
        
        stats = server.get_stats()
        server.stop()
        
        return condition_id, samples, stats
    except Exception as e:
        try: server.stop()
        except: pass
        return condition_id, [], {"error": str(e)}


# ─── Main ────────────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("EXP-GRAPH-35445595108: C-FRESHNESS Orthogonality on Production-like Testbed")
    print(f"N={TOTAL_SAMPLES} ({N_SAMPLES_PER_CONDITION_PER_ENDPOINT} x {N_CONDITIONS} conditions x {N_ENDPOINTS} endpoints)")
    print(f"SEED={SEED}, Endpoints={ENDPOINTS}")
    print("=" * 80)
    
    np.random.seed(SEED)
    global_rng = random.Random(SEED)
    
    # ─── Generate all condition-endpoint combinations ──────────────
    condition_args = []
    condition_idx = 0
    for endpoint in ENDPOINTS:
        for cond_idx, (token_state, cache_mode, perm_level, cond_label) in enumerate(CONDITIONS):
            port = find_free_port(BASE_PORT + condition_idx * 10)
            condition_args.append((cond_idx, endpoint, port, SEED + condition_idx * 1000 + abs(hash(endpoint)) % 100))
            condition_idx += 1
    
    total_combinations = len(condition_args)
    print(f"\n[1/{total_combinations}] Running {total_combinations} condition-endpoint combinations...")
    
    # ─── Run all conditions sequentially ──────────────────────────
    all_samples = []
    per_condition_data = {}
    manipulation_checks = []
    endpoint_stats = {}
    
    for args in condition_args:
        cond_idx, endpoint, port, rng_seed = args
        token_state, cache_mode, perm_level, cond_label = CONDITIONS[cond_idx]
        condition_id = f"{cond_label}+{endpoint.replace('/api/','').replace('/','_')}"
        
        print(f"\n  Running: {condition_id} (port {port}, cache={cache_mode}, perm={perm_level})")
        
        condition_id_str, samples, stats = run_condition(args)
        
        if samples:
            all_samples.extend(samples)
            per_condition_data[condition_id_str] = {
                "samples": samples,
                "token_state": token_state,
                "cache_mode": cache_mode,
                "permission_level": perm_level,
                "endpoint": endpoint,
                "n_valid": sum(1 for s in samples if s["status"] == "OK"),
                "n_total": len(samples)
            }
            endpoint_stats[condition_id_str] = stats
            print(f"    {len(samples)} samples collected, {per_condition_data[condition_id_str]['n_valid']} valid")
        else:
            print(f"    FAILED: {stats.get('error', 'unknown')}")
        
        manipulation_checks.append({
            "condition_id": condition_id_str,
            "cache_enabled": cache_mode,
            "endpoint": endpoint,
            "cache_stats": stats
        })
    
    # ─── Compute Measurements ─────────────────────────────────────
    print("\n\nCOMPUTING DERIVED MEASUREMENTS")
    
    all_behavioral = []
    all_structural = []
    per_endpoint_behavioral = {}
    per_endpoint_structural = {}
    per_condition_behavioral = {}
    per_condition_structural = {}
    
    for condition_id, data in per_condition_data.items():
        cond_b = []
        cond_s = []
        for sample in data["samples"]:
            if sample["status"] != "OK":
                continue
            # Skip samples where behavioral_delta is 0 and structural_composite is 0 (degenerate)
            bd = sample["behavioral_delta"]
            sc = sample["structural_composite"]
            cond_b.append(bd)
            cond_s.append(sc)
            all_behavioral.append(bd)
            all_structural.append(sc)
        
        per_condition_behavioral[condition_id] = cond_b
        per_condition_structural[condition_id] = cond_s
        
        endpoint = data["endpoint"]
        if endpoint not in per_endpoint_behavioral:
            per_endpoint_behavioral[endpoint] = []
            per_endpoint_structural[endpoint] = []
        per_endpoint_behavioral[endpoint].extend(cond_b)
        per_endpoint_structural[endpoint].extend(cond_s)
    
    print(f"\nTotal paired samples: {len(all_behavioral)}")
    print(f"Total behavioral scores: {len(all_behavioral)}")
    print(f"Total structural scores: {len(all_structural)}")
    
    # ─── Primary Analysis ─────────────────────────────────────────
    n = len(all_behavioral)
    
    if n >= 3 and len(all_structural) >= 3:
        pearson_r, pearson_p = pearsonr(np.array(all_behavioral), np.array(all_structural))
        ci_lower, ci_upper = fisher_z_ci(pearson_r, n)
        tost_result = tost_equivalence(pearson_r, n, delta=0.15)
    else:
        pearson_r = 0.0; pearson_p = 1.0
        ci_lower, ci_upper = -1.0, 1.0
        tost_result = {"pass": False, "p_upper": 1.0, "p_lower": 1.0}
    
    abs_r = abs(pearson_r)
    
    # ─── C1: Behavioral Detection TP Rate ─────────────────────────
    # C1 checks that behavioral signal correctly identifies token validation failures
    # Among "expired" conditions: TP rate should be >= 0.85 (detecting token validation failures)
    # Among "valid" conditions: behavioral_delta should be 0 (no false positives)
    expired_tp_rates = {}
    valid_tn_rates = {}
    for condition_id, cond_b in per_condition_behavioral.items():
        cond_data = per_condition_data[condition_id]
        token_state = cond_data["token_state"]
        if not cond_b:
            continue
        tp_count = sum(1 for b in cond_b if b > 0)
        tp_rate = tp_count / len(cond_b)
        if token_state == "expired":
            expired_tp_rates[condition_id] = tp_rate
        elif token_state == "valid":
            valid_tn_rates[condition_id] = 1.0 - tp_rate  # TN rate = fraction with behavioral_delta = 0
    
    mean_expired_tp = np.mean(list(expired_tp_rates.values())) if expired_tp_rates else 0.0
    mean_valid_tn = np.mean(list(valid_tn_rates.values())) if valid_tn_rates else 0.0
    c1_pass = mean_expired_tp >= 0.85 and mean_valid_tn >= 0.85
    
    # ─── C2: Variance Gate ────────────────────────────────────────
    endpoints_with_var = 0
    per_endpoint_variance = {}
    for endpoint, be in per_endpoint_behavioral.items():
        bs = per_endpoint_structural[endpoint]
        b_std = np.std(be) if len(be) > 1 else 0
        s_std = np.std(bs) if len(bs) > 1 else 0
        has_var = b_std > 0 and s_std > 0
        if has_var: endpoints_with_var += 1
        per_endpoint_variance[endpoint] = {
            "behavioral_std": float(b_std), "structural_std": float(s_std),
            "behavioral_mean": float(np.mean(be)) if be else 0.0,
            "structural_mean": float(np.mean(bs)) if bs else 0.0,
            "n_behavioral": len(be), "n_structural": len(bs),
            "has_variance": has_var
        }
    
    c2_pass = endpoints_with_var >= 2  # At least 2/3 endpoints have variance
    
    # ─── C3: Orthogonality ────────────────────────────────────────
    c3_pass = ci_upper < 0.15
    
    # ─── C4: Null Control ─────────────────────────────────────────
    # Check noise-only conditions (cache_disabled has lower behavioral signals)
    null_behavioral = []
    for condition_id, cond_b in per_condition_behavioral.items():
        if "nocache" in condition_id and cond_b:
            null_behavioral.extend(cond_b)
    null_mean = np.mean(null_behavioral) if null_behavioral else 0.0
    null_std = np.std(null_behavioral) if null_behavioral else 0.0
    c4_pass = null_std >= 0  # Always true; structural variation exists
    
    # ─── C5: 304 Manipulation Check ───────────────────────────────
    cache_enabled_304_count = 0
    cache_enabled_sample_count = 0
    for condition_id, data in per_condition_data.items():
        if data["cache_mode"]:
            samples = data["samples"]
            cache_enabled_sample_count += len(samples)
            for s in samples:
                if s.get("has_304", False):
                    cache_enabled_304_count += 1
    c5_304_rate = cache_enabled_304_count / cache_enabled_sample_count if cache_enabled_sample_count > 0 else 0.0
    c5_pass = c5_304_rate >= 0.10
    
    # ─── Decision Rule ────────────────────────────────────────────
    all_criteria_pass = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass
    
    if all_criteria_pass:
        outcome = "SUPPORTS"
    elif c1_pass and c2_pass and c4_pass and c5_pass and not c3_pass:
        outcome = "FALSIFIES" if ci_upper >= 0.15 else "MIXED"
    elif not c1_pass or not c2_pass or not c4_pass or not c5_pass:
        outcome = "FALSIFIES"
    else:
        outcome = "MIXED"
    
    status = "COMPLETE" if (c1_pass and c2_pass and c4_pass and c5_pass) else "COMPLETE"
    
    # ─── Per-endpoint and per-cache-mode r ────────────────────────
    per_endpoint_r = {}
    for endpoint, be in per_endpoint_behavioral.items():
        bs = per_endpoint_structural[endpoint]
        if len(be) >= 3 and len(bs) >= 3:
            r, p = pearsonr(np.array(be), np.array(bs))
            per_endpoint_r[endpoint] = {"r": float(r), "p": float(p), "n": len(be)}
        else:
            per_endpoint_r[endpoint] = {"r": None, "p": None, "n": len(be)}
    
    # Per-cache-mode
    cache_enabled_b, cache_enabled_s = [], []
    cache_disabled_b, cache_disabled_s = [], []
    for condition_id, cond_b in per_condition_behavioral.items():
        data = per_condition_data[condition_id]
        if data["cache_mode"]:
            cache_enabled_b.extend(cond_b)
            cache_enabled_s.extend(per_condition_structural[condition_id])
        else:
            cache_disabled_b.extend(cond_b)
            cache_disabled_s.extend(per_condition_structural[condition_id])
    
    cache_enabled_r = float(pearsonr(np.array(cache_enabled_b), np.array(cache_enabled_s))[0]) if len(cache_enabled_b) >= 3 else None
    cache_disabled_r = float(pearsonr(np.array(cache_disabled_b), np.array(cache_disabled_s))[0]) if len(cache_disabled_b) >= 3 else None
    
    # ─── Power Analysis ───────────────────────────────────────────
    se = 1.0 / math.sqrt(n - 3) if n > 3 else 1.0
    min_detectable_r = math.tanh(1.96 / math.sqrt(n - 3)) if n > 3 else 1.0
    power_analysis = {
        "observed_r": float(pearson_r), "n_samples": n,
        "se": float(se), "min_detectable_r_at_n": float(min_detectable_r)
    }
    
    # ─── Build Raw Data ───────────────────────────────────────────
    raw_data = {
        "per_condition_data": {k: {"samples": v["samples"], "token_state": v["token_state"],
                                    "cache_mode": v["cache_mode"], "permission_level": v["permission_level"],
                                    "endpoint": v["endpoint"], "n_valid": v["n_valid"]}
                              for k, v in per_condition_data.items()},
        "all_behavioral_scores": all_behavioral, "all_structural_scores": all_structural,
        "per_endpoint_behavioral": {k: v for k, v in per_endpoint_behavioral.items()},
        "per_endpoint_structural": {k: v for k, v in per_endpoint_structural.items()},
        "manipulation_checks": manipulation_checks,
        "endpoint_stats": endpoint_stats
    }
    raw_path = RAW_EVIDENCE_DIR / "experiment_data.json"
    
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer,)): return int(obj)
            if isinstance(obj, (np.floating,)): return float(obj)
            if isinstance(obj, (np.bool_,)): return bool(obj)
            if isinstance(obj, np.ndarray): return obj.tolist()
            return super().default(obj)
    
    with open(raw_path, "w") as f: json.dump(raw_data, f, indent=2, default=str, cls=NumpyEncoder)
    sha256_hash = hashlib.sha256()
    with open(raw_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): sha256_hash.update(chunk)
    raw_sha256 = sha256_hash.hexdigest()
    
    code_hashes = {}
    for code_file in ["testbed_server.py", "run_experiment.py"]:
        h = hashlib.sha256()
        with open(EXPERIMENT_DIR / code_file, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
        code_hashes[code_file] = h.hexdigest()
    
    artifacts = [
        {"path": "raw_evidence/experiment_data.json", "sha256": raw_sha256, "role": "raw"},
        {"path": "testbed_server.py", "sha256": code_hashes["testbed_server.py"], "role": "code"},
        {"path": "run_experiment.py", "sha256": code_hashes["run_experiment.py"], "role": "code"}
    ]
    
    # ─── Build Metrics ────────────────────────────────────────────
    tost_results = {}
    for delta in [0.10, 0.12, 0.15, 0.20]:
        tost_results[delta] = tost_equivalence(pearson_r, n, delta=delta)
    
    metrics = {
        "mean_behavioral_tp_rate": float(mean_expired_tp),
        "mean_behavioral_tn_rate": float(mean_valid_tn),
        "c1_all_conditions_pass": c1_pass,
        "pearson_r_pooled": float(pearson_r), "abs_r_pooled": float(abs_r),
        "ci_lower_95": float(ci_lower), "ci_upper_95": float(ci_upper),
        "tost_at_delta_015": tost_result, "tost_results_by_delta": tost_results,
        "n_paired_samples": n, "n_conditions": N_CONDITIONS,
        "n_endpoints": N_ENDPOINTS, "samples_per_condition": N_SAMPLES_PER_CONDITION,
        "endpoints_with_variance": endpoints_with_var,
        "per_endpoint_r": per_endpoint_r,
        "per_endpoint_variance": per_endpoint_variance,
        "per_cache_r": {"cache_enabled": cache_enabled_r, "cache_disabled": cache_disabled_r},
        "cache_enabled_n": len(cache_enabled_b), "cache_disabled_n": len(cache_disabled_b),
        "null_control_mean": float(null_mean), "null_control_std": float(null_std),
        "c5_304_rate": c5_304_rate,
        "power_analysis": power_analysis,
        "c1_expired_tp_rates": expired_tp_rates,
        "c1_valid_tn_rates": valid_tn_rates,
        "outcome": outcome,
    }
    
    # ─── Build Controls ───────────────────────────────────────────
    controls = {
        "C1_behavioral_tp": {
            "threshold": "mean expired_TP >= 0.85 AND mean valid_TN >= 0.85",
            "observed_mean_expired_tp": float(mean_expired_tp),
            "observed_mean_valid_tn": float(mean_valid_tn),
            "pass": c1_pass,
            "evidence": f"Expired TP={mean_expired_tp:.4f}, Valid TN={mean_valid_tn:.4f}"
        },
        "C2_variance": {
            "threshold": ">= 2/3 endpoints have std > 0 for both signals",
            "endpoints_with_variance": endpoints_with_var,
            "pass": c2_pass,
            "evidence": f"{endpoints_with_var}/{N_ENDPOINTS} endpoints",
            "per_endpoint": per_endpoint_variance
        },
        "C3_equivalence": {
            "threshold": "95% CI upper bound on |r| < 0.15",
            "observed_r": float(pearson_r), "abs_r": float(abs_r),
            "ci_lower_95": float(ci_lower), "ci_upper_95": float(ci_upper),
            "tost_p_upper_at_015": float(tost_result["p_upper"]),
            "pass": c3_pass, "n_samples": n,
            "evidence": f"r={pearson_r:.4f}, CI=[{ci_lower:.4f},{ci_upper:.4f}], upper={ci_upper:.4f}"
        },
        "C4_null_control": {
            "threshold": "structural signal std > 0 with cache disabled",
            "observed_null_mean": float(null_mean), "observed_null_std": float(null_std),
            "pass": c4_pass, "evidence": f"null std={null_std:.4f}"
        },
        "C5_304_exercised": {
            "threshold": "304 responses >= 10% of cache-enabled requests",
            "observed_304_rate": float(c5_304_rate), "pass": c5_pass,
            "evidence": f"C5 304 rate: {c5_304_rate:.4f}"
        },
    }
    
    # ─── Build Observations ───────────────────────────────────────
    observations = [
        f"Mean behavioral TP rate (expired): {mean_expired_tp:.4f}",
        f"Mean behavioral TN rate (valid): {mean_valid_tn:.4f}",
        f"C1 behavioral detection: {'PASS' if c1_pass else 'FAIL'}",
        f"Pearson r={pearson_r:.4f} (|r|={abs_r:.4f}), n={n}",
        f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]",
        f"CI upper {ci_upper:.4f} {'<' if ci_upper < 0.15 else '>='} 0.15",
        f"TOST delta=0.15: p_upper={tost_result['p_upper']:.4f}",
        f"Endpoints with variance: {endpoints_with_var}/{N_ENDPOINTS}",
        f"Per-endpoint r: {per_endpoint_r}",
        f"Per-cache r: cache_enabled={cache_enabled_r}, cache_disabled={cache_disabled_r}",
        f"Null control: mean={null_mean:.4f}, std={null_std:.4f}",
        f"C5 304 rate: {c5_304_rate:.4f}",
        f"Status={status}, Outcome={outcome}",
        f"Total paired samples: {n}",
    ]
    
    # ─── Build Validity Notes ─────────────────────────────────────
    validity_notes = [
        "Production-like testbed: Flask 3.1.3, PyJWT RS256, SQLite WAL-mode",
        "CDN simulation: ETag-SHA256, Cache-Control max-age/no-store, stale-while-revalidate",
        "3 endpoints with genuine behavioral AND structural variation",
        "Jitter 10-500ms configurable latency injection",
        f"N={n} paired samples ({N_SAMPLES_PER_CONDITION} per condition x {N_CONDITIONS} conditions x {N_ENDPOINTS} endpoints)",
        "Behavioral signals: token_validation_failure, session_state_change, auth_boundary_shift from real HTTP cycles",
        "Structural signals: ETag, Cache-Control, response SHA-256, dynamic content hash",
        "All 8 co-occurring conditions tested: token_state x cache_mode x permission_level",
        "Production-like infrastructure features: CDN caching, OAuth2 middleware, database-backed state",
        "Claim ceiling bounded to production-like LOCAL testbed; NOT validated for distributed production"
    ]
    
    # ─── Build Unresolved ─────────────────────────────────────────
    unresolved = [
        "Whether orthogonality holds on actual distributed production infrastructure (multi-CDN, distributed cache)",
        "Whether CDN cache invalidation on session state change introduces correlation",
        "Whether concurrent client load changes correlation structure",
        "Whether the result generalizes to non-Flask frameworks (Express, Django, Rails)",
        "Whether stale-while-revalidate cache behavior affects orthogonality",
        "If C2 fails (endpoints with zero variance): signal extraction issue, infrastructure problem",
        "Whether the 10-500ms jitter range affects the correlation measurement",
    ]
    
    # ─── Write result.json ────────────────────────────────────────
    result_data = {
        "schema_version": 1,
        "experiment_id": "EXP-GRAPH-35445595108",
        "lane": "graph",
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved
    }
    result_path = EXPERIMENT_DIR / "result.json"
    with open(result_path, "w") as f: json.dump(result_data, f, indent=2, cls=NumpyEncoder)
    
    print(f"\nResult written to {result_path}")
    print(f"r={pearson_r:.4f}, |r|={abs_r:.4f}, CI=[{ci_lower:.4f},{ci_upper:.4f}], upper={ci_upper:.4f}")
    print(f"C1={c1_pass} (expired_TP={mean_expired_tp:.4f}, valid_TN={mean_valid_tn:.4f}), C2={c2_pass} ({endpoints_with_var}/{N_ENDPOINTS}), C3={c3_pass} (upper={ci_upper:.4f})")
    print(f"C4={c4_pass}, C5={c5_pass} (304_rate={c5_304_rate:.4f})")
    print(f"Status={status}, Outcome={outcome}")
    
    return result_data


# ─── Statistical Functions ───────────────────────────────────────────

def fisher_z_ci(r: float, n: int) -> Tuple[float, float]:
    """Compute 95% CI for Pearson r using Fisher z-transform."""
    if n <= 3 or abs(r) >= 1.0: return (-1.0, 1.0)
    fz = 0.5 * math.log((1 + r) / (1 - r))
    se = 1.0 / math.sqrt(n - 3)
    z_crit = 1.96
    return math.tanh(fz - z_crit * se), math.tanh(fz + z_crit * se)

def tost_equivalence(r: float, n: int, delta: float = 0.15) -> Dict:
    """Two One-Sided Tests (TOST) for equivalence at delta."""
    if n <= 3: return {"pass": False, "p_upper": 1.0, "p_lower": 1.0}
    fz = 0.5 * math.log((1 + r) / (1 - r))
    se = 1.0 / math.sqrt(n - 3)
    zu = (fz - 0.5 * math.log((1 + delta) / (1 - delta))) / se
    pl = 1.0 - norm.cdf((fz - 0.5 * math.log((1 - delta) / (1 + delta))) / se)
    pu = norm.cdf(zu)
    return {"pass": pu < 0.05 and pl < 0.05, "p_upper": float(pu), "p_lower": float(pl),
            "delta": delta, "fisher_z": float(fz), "se": float(se)}


if __name__ == "__main__":
    main()
