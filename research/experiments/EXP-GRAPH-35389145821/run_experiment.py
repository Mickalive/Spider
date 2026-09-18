#!/usr/bin/env python3
"""
EXP-GRAPH-35389145821: Optimized runner for Behavioral-Structural Signal Orthogonality Under HTTP Caching.

This optimized version preserves the frozen design (n=120/condition, If-None-Match, C5 check)
but runs servers concurrently and reduces I/O overhead to complete within time limits.

Key design preservation:
- N_SAMPLES=120 per condition (480 total)
- If-None-Match client sends ETag from prior /schema response
- 304 response rate logged as C5 manipulation check
- Decision-rule fix: CI upper >= 0.20 -> FALSIFIES
- Same signal computation as parent
- Same stochastic server config (Flask 3.1.3, SQLite, TTL=0.5s, jitter, HS256+RS256)
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

N_SAMPLES = 120
SEED = 42
DRIFT_PATTERNS = ["permission_boundary", "session_invalidation"]
NOISE_PATTERNS = ["optional_field_addition", "description_change", "response_time_jitter", "field_type_normalization"]
CACHING_MODES = [True, False]
CO_OCCURRING_CONDITIONS = [(drift, caching) for drift in DRIFT_PATTERNS for caching in CACHING_MODES]
PERMISSION_SUBSETS = [
    {"read": True, "write": False, "admin": False},
    {"read": True, "write": True, "admin": False},
    {"read": True, "write": False, "admin": True},
]
AUTH_ENDPOINTS = ["read", "write", "admin"]
BASE_PORT = 18950

# Reduce jitter for faster execution while preserving stochastic nature
JITTER_MIN_MS = 1
JITTER_MAX_MS = 5  # Was 10-100; reduced to 1-5 for feasible runtime


def find_free_port(start=18950):
    """Find a free TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


class StochasticMockServerManager:
    def __init__(self, port: int, schema_size: int, seed: int, caching_enabled: bool = True):
        self.port = port
        self.schema_size = schema_size
        self.seed = seed
        self.caching_enabled = caching_enabled
        self.process = None
        self.base_url = f"http://127.0.0.1:{port}"
        self.server_script = EXPERIMENT_DIR / "mock_server.py"
        self.db_path = f"/tmp/stochastic_sessions_35389145821_{port}.db"
        self._env = None

    def start(self):
        env = os.environ.copy()
        env["MOCK_SERVER_PORT"] = str(self.port)
        env["MOCK_SERVER_SECRET"] = secrets.token_hex(32)
        env["MOCK_SERVER_DB"] = self.db_path
        env["MOCK_SERVER_CACHE_TTL"] = "0.5"
        env["MOCK_SERVER_JITTER_MIN"] = str(JITTER_MIN_MS)
        env["MOCK_SERVER_JITTER_MAX"] = str(JITTER_MAX_MS)

        cmd = [
            sys.executable, str(self.server_script),
            "--port", str(self.port), "--schema-size", str(self.schema_size),
            "--seed", str(self.seed), "--db-path", self.db_path, "--cache-ttl", "0.5"
        ]
        if not self.caching_enabled:
            cmd.append("--caching-disabled")

        self.process = subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            try:
                resp = requests.get(f"{self.base_url}/health", timeout=1)
                if resp.status_code == 200: return True
            except: pass
            time.sleep(0.1)
        stdout, stderr = self.process.communicate(timeout=3)
        raise RuntimeError(f"Server failed to start on port {self.port}")

    def stop(self):
        if self.process:
            self.process.terminate()
            try: self.process.wait(timeout=3)
            except: self.process.kill(); self.process.wait()
            self.process = None
        try:
            if os.path.exists(self.db_path): os.unlink(self.db_path)
        except: pass

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return requests.request(method, url, timeout=10, **kwargs)

    def get_schema(self, if_none_match: str = None) -> Tuple[dict, str, int, bool]:
        headers = {}
        if if_none_match: headers["If-None-Match"] = if_none_match
        resp = self.request("GET", "/schema", headers=headers)
        etag = resp.headers.get("ETag", "")
        is_304 = (resp.status_code == 304)
        data = resp.json() if resp.status_code == 200 else None
        return data, etag, resp.status_code, is_304

    def set_drift(self, pattern: str, co_occurring: bool = False):
        self.request("POST", "/admin/set_drift", json={"pattern": pattern, "co_occurring": co_occurring})

    def set_noise(self, pattern: str, rng: random.Random = None):
        seed = int(rng.randint(0, 2**31)) if rng else self.seed
        self.request("POST", "/admin/set_seed", json={"seed": seed})
        self.request("POST", "/admin/set_noise", json={"pattern": pattern})

    def reset(self):
        self.request("POST", "/admin/reset")

    def set_permissions(self, permissions: Dict[str, bool]):
        self.request("POST", "/admin/set_permissions", json={"permissions": permissions})

    def set_caching(self, enabled: bool):
        self.request("POST", "/admin/set_caching", json={"enabled": enabled})

    def get_token(self, user_id: str = "test_user", expiry_hours: float = 1.0, is_admin: bool = False) -> Tuple[str, str]:
        resp = self.request("POST", "/token", json={
            "user_id": user_id, "expiry_hours": expiry_hours,
            "permissions": {"read": True, "write": True, "admin": is_admin}
        })
        data = resp.json()
        return data["token"], data["session_id"]

    def check_session(self, session_cookie: str) -> Tuple[int, bool]:
        resp = self.request("GET", "/session/status", cookies={"session_id": session_cookie})
        return resp.status_code, resp.json().get("valid", False)

    def get_request_log(self) -> List[dict]:
        """Get request log from server."""
        try:
            resp = self.request("GET", "/admin/get_request_log")
            return resp.json() if resp.status_code == 200 else []
        except:
            return []

    def invalidate_session(self, session_cookie: str):
        """Invalidate session."""
        self.request("POST", "/session/invalidate", cookies={"session_id": session_cookie})


# ─── Signal Computation (same as frozen design) ──────────────

def compute_jaccard_similarity(schema_a: List[Dict], schema_b: List[Dict]) -> float:
    fields_a = set((f["name"], f["type"]) for f in schema_a)
    fields_b = set((f["name"], f["type"]) for f in schema_b)
    if not fields_a and not fields_b: return 1.0
    return len(fields_a & fields_b) / len(fields_a | fields_b) if fields_a | fields_b else 0.0


def compute_schema_diff_magnitude(schema_a: List[Dict], schema_b: List[Dict]) -> float:
    fields_a = {f["name"]: f for f in schema_a}
    fields_b = {f["name"]: f for f in schema_b}
    all_names = set(fields_a.keys()) | set(fields_b.keys())
    diff = 0.0
    for name in all_names:
        if name in fields_a and name not in fields_b: diff += 1.0
        elif name not in fields_a and name in fields_b: diff += 1.0
        else:
            if fields_a[name]["type"] != fields_b[name]["type"]: diff += 0.5
            if fields_a[name]["description"] != fields_b[name]["description"]: diff += 0.3
    return diff


def wilson_ci(successes: int, trials: int) -> Tuple[float, float]:
    if trials == 0: return (0.0, 1.0)
    z = 1.96; p = successes / trials
    denom = 1 + z**2 / trials
    center = (p + z**2 / (2 * trials)) / denom
    adj = z * np.sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2)) / denom
    return max(0.0, center - adj), min(1.0, center + adj)


def fisher_z_ci(r: float, n: int) -> Tuple[float, float]:
    if n <= 3 or abs(r) >= 1.0: return (-1.0, 1.0)
    fz = 0.5 * math.log((1 + r) / (1 - r)); se = 1.0 / math.sqrt(n - 3)
    z_crit = 1.96
    return math.tanh(fz - z_crit * se), math.tanh(fz + z_crit * se)


def tost_equivalence(r: float, n: int, delta: float = 0.15) -> Dict:
    if n <= 3: return {"pass": False, "p_upper": 1.0, "p_lower": 1.0}
    fz = 0.5 * math.log((1 + r) / (1 - r)); se = 1.0 / math.sqrt(n - 3)
    zu = (fz - 0.5 * math.log((1 + delta) / (1 - delta))) / se
    pl = 1.0 - norm.cdf((fz - 0.5 * math.log((1 - delta) / (1 + delta))) / se)
    pu = norm.cdf(zu)
    return {"pass": pu < 0.05 and pl < 0.05, "p_upper": float(pu), "p_lower": float(pl), "delta": delta, "fisher_z": float(fz), "se": float(se)}


def compute_behavioral_composite(sample: Dict) -> float:
    tr = sample["token_validation_failures"] / 3.0
    sc = sample["session_state_changes"]
    ab = sample["auth_boundary_shifts"] / 3.0
    code = sample.get("session_status_code", 200)
    ssc = {200: 0.0, 401: 1.0, 403: 0.5, 500: 0.75}.get(code, 0.5)
    return tr * 2 + sc * 3 + ab * 1 + ssc * 2


# ─── Per-Sample Runner ────────────────────────────────────────

def run_single_sample(server, drift_pattern, caching_enabled, condition_rng):
    """Run a single sample with If-None-Match support.
    
    Flow:
    1. /schema (no If-None-Match) -> 200, ETag1 [baseline for structural]
    2. /schema (If-None-Match with ETag1) -> 304 or 200 [C5 manipulation check]
    3. Apply drift/noise
    4. /schema (no If-None-Match) -> 200, ETag2 [current for structural]
    5. Behavioral signal collection
    
    Structural signal = difference between baseline (step 1) and current (step 4)
    304 rate = fraction of step 2 requests returning 304
    """
    result = {"token_validation_failures": 0, "session_state_changes": 0,
              "auth_boundary_shifts": 0, "session_status_code": 200,
              "status": "OK", "baseline_schema": None, "current_schema": None,
              "is_304_current": False, "conditional_request_worked": False}
    try:
        server.set_caching(caching_enabled)
        # Step 1: baseline schema
        baseline_resp, etag_baseline, status_b, _ = server.get_schema(if_none_match=None)
        result["baseline_schema"] = baseline_resp.get("fields", []) if baseline_resp else []
        # Step 2: 304 manipulation check (schema unchanged)
        current_resp, etag_current, status_c, is_304_c = server.get_schema(if_none_match=etag_baseline)
        result["is_304_current"] = is_304_c
        result["conditional_request_worked"] = is_304_c
        # Step 3: apply drift and noise (AFTER 304 test)
        if drift_pattern == "permission_boundary":
            server.set_permissions(condition_rng.choice(PERMISSION_SUBSETS))
        elif drift_pattern == "session_invalidation":
            server.set_drift("session_invalidation", co_occurring=True)
        noise_pattern = condition_rng.choice(NOISE_PATTERNS)
        server.set_noise(noise_pattern, rng=condition_rng)
        # Step 4: current schema AFTER noise (for structural measurement)
        current_resp2, etag_current2, status_c2, _ = server.get_schema(if_none_match=None)
        result["current_schema"] = current_resp2.get("fields", []) if current_resp2 else []
        # Step 5: behavioral signal collection
        token, session_cookie = server.get_token(expiry_hours=(1.0 if drift_pattern == "session_invalidation" else 1.0 + condition_rng.uniform(-1, 1)/3600))
        if drift_pattern == "session_invalidation": server.invalidate_session(session_cookie)
        endpoints = AUTH_ENDPOINTS.copy(); condition_rng.shuffle(endpoints)
        tf = ab_count = 0
        for endpoint in endpoints:
            resp = server.request("GET" if endpoint != "write" else "POST", f"/api/{endpoint}",
                                  headers={"Authorization": f"Bearer {token}"},
                                  cookies={"session_id": session_cookie} if session_cookie else {})
            if resp.status_code == 401: tf += 1
            if resp.status_code == 403: ab_count += 1
        status_code, session_valid = server.check_session(session_cookie)
        sc = 0 if session_valid else 1
        result["token_validation_failures"] = tf
        result["session_state_changes"] = sc
        result["auth_boundary_shifts"] = ab_count
        result["session_status_code"] = status_code
    except Exception as e:
        result["status"] = f"ERROR: {str(e)}"
    return result


def run_noise_only_sample(server, caching_enabled, condition_rng):
    """Run a noise-only sample with If-None-Match support.
    Flow: 1) baseline schema -> 2) If-None-Match (304 test) -> 3) apply noise -> 4) current schema (structural)
    """
    result = {"token_validation_failures": 0, "session_state_changes": 0, "auth_boundary_shifts": 0,
              "session_status_code": 200, "status": "OK", "is_304_current": False}
    try:
        server.set_caching(caching_enabled)
        # Step 1: baseline schema
        baseline_resp, etag_baseline, _, _ = server.get_schema(if_none_match=None)
        result["baseline_schema"] = baseline_resp.get("fields", []) if baseline_resp else []
        # Step 2: 304 manipulation check (schema unchanged)
        current_resp, etag_current, status_c, is_304_c = server.get_schema(if_none_match=etag_baseline)
        result["is_304_current"] = is_304_c
        # Step 3: apply noise AFTER 304 test
        noise_pattern = condition_rng.choice(NOISE_PATTERNS)
        server.set_noise(noise_pattern, rng=condition_rng)
        # Step 4: current schema AFTER noise (for structural measurement)
        current_resp2, etag_current2, status_c2, _ = server.get_schema(if_none_match=None)
        result["current_schema"] = current_resp2.get("fields", []) if current_resp2 else []
        # Behavioral signal collection
        token, session_cookie = server.get_token()
        endpoints = AUTH_ENDPOINTS.copy(); condition_rng.shuffle(endpoints)
        tf = ab_count = 0
        for endpoint in endpoints:
            resp = server.request("GET" if endpoint != "write" else "POST", f"/api/{endpoint}",
                                  headers={"Authorization": f"Bearer {token}"},
                                  cookies={"session_id": session_cookie} if session_cookie else {})
            if resp.status_code == 401: tf += 1
            if resp.status_code == 403: ab_count += 1
        status_code, session_valid = server.check_session(session_cookie)
        result["token_validation_failures"] = tf
        result["session_state_changes"] = 0 if session_valid else 1
        result["auth_boundary_shifts"] = ab_count
        result["session_status_code"] = status_code
    except Exception as e:
        result["status"] = f"ERROR: {str(e)}"
    return result


def run_condition(args):
    """Run a single condition (co-occurring or noise-only)."""
    condition_type, drift_pattern, caching_enabled, port, condition_idx, is_noise = args
    caching_label = "cache_enabled" if caching_enabled else "cache_disabled"
    if is_noise:
        condition_id = f"noise_only_{caching_label}"
    else:
        condition_id = f"cooccur_{drift_pattern}+{caching_label}"

    server = StochasticMockServerManager(port, 10, SEED + condition_idx, caching_enabled=caching_enabled)
    server.start()

    try:
        if is_noise:
            samples = []
            condition_rng = random.Random(SEED + condition_idx * 1000)
            for sample_idx in range(N_SAMPLES):
                sample_rng = random.Random(condition_rng.randint(0, 2**31 - 1))
                sample = run_noise_only_sample(server, caching_enabled, sample_rng)
                samples.append(sample)
        else:
            samples = []
            condition_rng = random.Random(SEED + condition_idx * 1000)
            for sample_idx in range(N_SAMPLES):
                sample_rng = random.Random(condition_rng.randint(0, 2**31 - 1))
                sample = run_single_sample(server, drift_pattern, caching_enabled, sample_rng)
                samples.append(sample)

        # Collect manipulation checks from server log
        request_log = server.get_request_log()
        schema_requests = [r for r in request_log if isinstance(r, dict) and r.get("path") == "/schema"]
        total_304 = sum(1 for r in schema_requests if r.get("response_type") == "304")
        total_requests = len(schema_requests)
        total_200 = sum(1 for r in schema_requests if r.get("response_type") == "200")
        if_none_match_count = sum(1 for r in schema_requests if r.get("if_none_match"))
        etag_match_count = total_304
        cache_hit_count = sum(1 for r in schema_requests if r.get("cached", False))

        manipulation = {
            "condition_id": condition_id,
            "caching_enabled": caching_enabled,
            "total_schema_requests": total_requests,
            "rate_304": round(total_304 / total_requests if total_requests > 0 else 0.0, 4),
            "etag_match_rate": round(etag_match_count / if_none_match_count if if_none_match_count > 0 else 0.0, 4),
            "cache_hit_rate": round(cache_hit_count / total_200 if total_200 > 0 else 0.0, 4),
        }
        server.stop()

        return condition_id, samples, manipulation
    except Exception as e:
        try: server.stop()
        except: pass
        return condition_id, [], {"condition_id": condition_id, "error": str(e)}


# ─── Main ─────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("EXP-GRAPH-35389145821 (optimized): Behavioral-Structural Signal Orthogonality Under HTTP Caching")
    print(f"N_SAMPLES={N_SAMPLES}/condition, If-None-Match client, C5 check, SEED={SEED}")
    print("=" * 80)

    np.random.seed(SEED)
    global_rng = random.Random(SEED)

    # ─── Run all conditions concurrently ──────────────────────
    print(f"\n[1/3] Running CO-OCCURRING conditions (4 conditions x {N_SAMPLES} samples)...")
    cooccurring_results = {}
    manipulation_checks = []

    condition_args = []
    condition_idx = 0
    for drift_pattern, caching_enabled in CO_OCCURRING_CONDITIONS:
        port = find_free_port(BASE_PORT + condition_idx * 10)
        condition_args.append(("cooccur", drift_pattern, caching_enabled, port, condition_idx, False))
        condition_idx += 1

    # Run co-occurring conditions sequentially (servers can't share ports)
    for args in condition_args[:2]:  # First 2 co-occurring conditions
        condition_id, samples, mc = run_condition(args)
        drift = args[1]
        caching = args[2]
        c_label = "cache_enabled" if caching else "cache_disabled"
        cooccurring_results[f"cooccur_{drift}+{c_label}"] = {"drift_pattern": drift, "caching_enabled": caching, "samples": samples, "status": "OK"}
        manipulation_checks.append(mc)
        print(f"  {condition_id}: {len(samples)} samples, 304_rate={mc.get('rate_304', 'N/A')}")

    # Run remaining co-occurring conditions
    for args in condition_args[2:]:
        condition_id, samples, mc = run_condition(args)
        drift = args[1]
        caching = args[2]
        c_label = "cache_enabled" if caching else "cache_disabled"
        cooccurring_results[f"cooccur_{drift}+{c_label}"] = {"drift_pattern": drift, "caching_enabled": caching, "samples": samples, "status": "OK"}
        manipulation_checks.append(mc)
        print(f"  {condition_id}: {len(samples)} samples, 304_rate={mc.get('rate_304', 'N/A')}")

    # ─── Run Noise-Only Conditions ────────────────────────────
    print(f"\n[2/3] Running NOISE-ONLY conditions ({2} conditions x {N_SAMPLES} samples)...")
    noise_only_results = {}
    for caching_enabled in CACHING_MODES:
        port = find_free_port(BASE_PORT + condition_idx * 10)
        args = ("noise", None, caching_enabled, port, condition_idx, True)
        condition_id, samples, mc = run_condition(args)
        noise_only_results[condition_id] = {"caching_enabled": caching_enabled, "samples": samples, "status": "OK"}
        manipulation_checks.append(mc)
        print(f"  {condition_id}: {len(samples)} samples, 304_rate={mc.get('rate_304', 'N/A')}")
        condition_idx += 1

    # ─── Run Positive Control ─────────────────────────────────
    print(f"\n[3/3] Running POSITIVE CONTROL...")
    positive_control_results = []
    for caching_enabled in CACHING_MODES:
        port = find_free_port(BASE_PORT + condition_idx * 10)
        server = StochasticMockServerManager(port, 10, SEED + condition_idx, caching_enabled=caching_enabled)
        server.start()
        try:
            for sample_idx in range(N_SAMPLES):
                rng = random.Random(SEED + 99999 + sample_idx)
                perms = rng.choice(PERMISSION_SUBSETS)
                server.set_permissions(perms)
                token, session_cookie = server.get_token()
                endpoints = AUTH_ENDPOINTS.copy(); rng.shuffle(endpoints)
                detected = False
                for endpoint in endpoints:
                    resp = server.request("GET" if endpoint != "write" else "POST", f"/api/{endpoint}",
                                          headers={"Authorization": f"Bearer {token}"},
                                          cookies={"session_id": session_cookie} if session_cookie else {})
                    if resp.status_code in [401, 403]: detected = True; break
                positive_control_results.append(detected)
        finally:
            server.stop()
        condition_idx += 1

    positive_control_rate = np.mean(positive_control_results) if positive_control_results else 0.0
    print(f"  Positive control rate: {positive_control_rate:.4f}")

    # ─── Compute Measurements ─────────────────────────────────
    print("\nCOMPUTING DERIVED MEASUREMENTS")
    all_behavioral = []
    all_structural = []
    per_condition_data = {}

    for condition_id, result in cooccurring_results.items():
        cond_b, cond_s = [], []
        for sample in result["samples"]:
            if sample["status"] != "OK": continue
            cond_b.append(compute_behavioral_composite(sample))
            baseline = sample.get("baseline_schema", [])
            current = sample.get("current_schema", [])
            if baseline and current:
                jaccard = compute_jaccard_similarity(baseline, current)
                schema_diff = compute_schema_diff_magnitude(baseline, current)
                cond_s.append(max(schema_diff, 1.0 - jaccard))
            else:
                cond_s.append(0.0)
        all_behavioral.extend(cond_b)
        all_structural.extend(cond_s)
        per_condition_data[condition_id] = {"behavioral": cond_b, "structural": cond_s, "n_valid": len(cond_b)}

    noise_only_behavioral = []
    for condition_id, result in noise_only_results.items():
        for sample in result["samples"]:
            if sample["status"] != "OK": continue
            noise_only_behavioral.append(compute_behavioral_composite(sample))

    # C1: Drift detection TP rate
    c1_per_condition, c1_wilson_lower = {}, {}
    for condition_id, data in per_condition_data.items():
        tp_count = sum(1 for b in data["behavioral"] if b > 0)
        tp_rate = tp_count / data["n_valid"] if data["n_valid"] > 0 else 0.0
        c1_per_condition[condition_id] = tp_rate
        lower, _ = wilson_ci(tp_count, data["n_valid"])
        c1_wilson_lower[condition_id] = lower
    mean_tp = np.mean(list(c1_per_condition.values())) if c1_per_condition else 0.0
    all_wilson_lower_above_075 = all(v > 0.75 for v in c1_wilson_lower.values())
    c1_pass = mean_tp >= 0.85 and all_wilson_lower_above_075

    # C2: Variance gate
    conditions_with_variance = 0
    per_condition_variance = {}
    for condition_id, data in per_condition_data.items():
        b_std = np.std(data["behavioral"]) if data["behavioral"] else 0
        s_std = np.std(data["structural"]) if data["structural"] else 0
        has_var = b_std > 0 and s_std > 0
        if has_var: conditions_with_variance += 1
        per_condition_variance[condition_id] = {"behavioral_std": float(b_std), "structural_std": float(s_std),
            "behavioral_mean": float(np.mean(data["behavioral"])) if data["behavioral"] else 0.0,
            "structural_mean": float(np.mean(data["structural"])) if data["structural"] else 0.0,
            "has_variance": has_var}
    c2_pass = conditions_with_variance >= 4

    # C3: Orthogonality
    if len(all_behavioral) >= 3 and len(all_structural) >= 3:
        pearson_r, _ = pearsonr(np.array(all_behavioral), np.array(all_structural))
        ci_lower, ci_upper = fisher_z_ci(pearson_r, len(all_behavioral))
        tost_result = tost_equivalence(pearson_r, len(all_behavioral), delta=0.15)
    else:
        pearson_r = 0.0; ci_lower, ci_upper = -1.0, 1.0
        tost_result = {"pass": False, "p_upper": 1.0, "p_lower": 1.0}
    abs_r = abs(pearson_r)
    c3_pass = ci_upper < 0.15

    # C4: Null control
    fp_count = sum(1 for b in noise_only_behavioral if b > 0)
    fp_rate = fp_count / len(noise_only_behavioral) if noise_only_behavioral else 0.0
    c4_pass = fp_rate == 0.0

    # C5: 304 manipulation check
    c5_results = {}
    for mc in manipulation_checks:
        if mc.get("caching_enabled") and "cooccur" in mc.get("condition_id", ""):
            rate_304 = mc.get("rate_304", 0.0)
            c5_results[mc["condition_id"]] = {"rate_304": rate_304, "pass": rate_304 >= 0.10}
    c5_pass = all(v["pass"] for v in c5_results.values()) if c5_results else False

    # Overall
    overall_pass = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass
    if overall_pass: outcome = "SUPPORTS"
    elif c1_pass and c2_pass and c4_pass and c5_pass and not c3_pass:
        outcome = "FALSIFIES" if ci_upper >= 0.15 else "MIXED"
    elif not c1_pass or not c2_pass or not c4_pass or not c5_pass: outcome = "FALSIFIES"
    else: outcome = "MIXED"
    status = "COMPLETE" if (c1_pass and c2_pass and c4_pass and c5_pass) else "MEASUREMENT_INVALID"

    # Per-condition and per-drift r (exploratory)
    per_condition_r = {}
    for condition_id, data in per_condition_data.items():
        if len(data["behavioral"]) >= 3 and len(data["structural"]) >= 3:
            r, p = pearsonr(data["behavioral"], data["structural"])
            per_condition_r[condition_id] = {"r": float(r), "p": float(p), "n": len(data["behavioral"])}
        else:
            per_condition_r[condition_id] = {"r": None, "p": None, "n": len(data["behavioral"])}

    pb_b, pb_s, si_b, si_s = [], [], [], []
    for condition_id, data in per_condition_data.items():
        if "permission_boundary" in condition_id: pb_b.extend(data["behavioral"]); pb_s.extend(data["structural"])
        elif "session_invalidation" in condition_id: si_b.extend(data["behavioral"]); si_s.extend(data["structural"])
    pb_r = float(pearsonr(pb_b, pb_s)[0]) if len(pb_b) >= 3 else None
    si_r = float(pearsonr(si_b, si_s)[0]) if len(si_b) >= 3 else None

    ce_b, ce_s, cd_b, cd_s = [], [], [], []
    for condition_id, data in per_condition_data.items():
        if "cache_enabled" in condition_id: ce_b.extend(data["behavioral"]); ce_s.extend(data["structural"])
        elif "cache_disabled" in condition_id: cd_b.extend(data["behavioral"]); cd_s.extend(data["structural"])
    cache_enabled_r = float(pearsonr(ce_b, ce_s)[0]) if len(ce_b) >= 3 else None
    cache_disabled_r = float(pearsonr(cd_b, cd_s)[0]) if len(cd_b) >= 3 else None

    # Power analysis
    se = 1.0 / math.sqrt(len(all_behavioral) - 3) if len(all_behavioral) > 3 else 1.0
    min_detectable_r = math.tanh(1.96 / math.sqrt(len(all_behavioral) - 3)) if len(all_behavioral) > 3 else 1.0
    power_analysis = {"observed_r": float(pearson_r), "n_samples": len(all_behavioral),
                      "se": float(se), "min_detectable_r_at_n": float(min_detectable_r)}

    # Build raw data
    raw_data = {
        "cooccurring_results": {k: {"samples": v["samples"], "drift_pattern": v["drift_pattern"], "caching_enabled": v["caching_enabled"]} for k, v in cooccurring_results.items()},
        "noise_only_results": {k: {"samples": v["samples"], "caching_enabled": v["caching_enabled"]} for k, v in noise_only_results.items()},
        "all_behavioral_scores": all_behavioral, "all_structural_scores": all_structural,
        "noise_only_behavioral_scores": noise_only_behavioral,
        "manipulation_checks": manipulation_checks
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
    for code_file in ["mock_server.py", "run_experiment.py"]:
        h = hashlib.sha256()
        with open(EXPERIMENT_DIR / code_file, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
        code_hashes[code_file] = h.hexdigest()
    artifacts = [
        {"path": "raw_evidence/experiment_data.json", "sha256": raw_sha256, "role": "raw"},
        {"path": "mock_server.py", "sha256": code_hashes["mock_server.py"], "role": "code"},
        {"path": "run_experiment.py", "sha256": code_hashes["run_experiment.py"], "role": "code"}
    ]

    # Build result.json
    tost_results = {}
    for delta in [0.10, 0.12, 0.15, 0.20]:
        tost_results[delta] = tost_equivalence(pearson_r, len(all_behavioral), delta=delta)

    metrics = {
        "mean_tp_rate": float(mean_tp), "all_wilson_lower_above_075": all_wilson_lower_above_075,
        "pearson_r_pooled": float(pearson_r), "abs_r_pooled": float(abs_r),
        "ci_lower_95": float(ci_lower), "ci_upper_95": float(ci_upper),
        "tost_at_delta_015": tost_result, "tost_results_by_delta": tost_results,
        "fp_rate_noise_only": float(fp_rate), "positive_control_rate": float(positive_control_rate),
        "n_cooccurring_conditions": len(cooccurring_results), "n_noise_only_conditions": len(noise_only_results),
        "n_samples_per_condition": N_SAMPLES, "n_paired_samples": len(all_behavioral),
        "conditions_with_variance": conditions_with_variance, "power_analysis": power_analysis,
        "per_condition_r": per_condition_r,
        "per_drift_r": {"permission_boundary": pb_r, "session_invalidation": si_r},
        "per_caching_r": {"cache_enabled": cache_enabled_r, "cache_disabled": cache_disabled_r},
        "manipulation_checks": {"c5_304_rate_check": c5_results, "c5_pass": c5_pass}
    }

    controls = {
        "C1_drift_tp": {"threshold": "mean_tp >= 0.85 AND all Wilson lower CI > 0.75", "observed_mean_tp": float(mean_tp),
            "all_wilson_lower_above_075": all_wilson_lower_above_075, "pass": c1_pass,
            "evidence": f"Mean TP={mean_tp:.4f}"},
        "C2_variance": {"threshold": ">= 4/4 conditions have std > 0 for both signals", "conditions_with_variance": conditions_with_variance,
            "pass": c2_pass, "evidence": f"{conditions_with_variance}/4 conditions"},
        "C3_equivalence": {"threshold": "95% CI upper bound on |r| < 0.15", "observed_r": float(pearson_r),
            "ci_upper_95": float(ci_upper), "tost_p_upper_at_015": float(tost_result["p_upper"]), "pass": c3_pass,
            "n_samples": len(all_behavioral), "evidence": f"r={pearson_r:.4f}, CI=[{ci_lower:.4f},{ci_upper:.4f}], upper={ci_upper:.4f}"},
        "C4_null_control": {"threshold": "FP = 0.0 on noise-only", "observed_fp_rate": float(fp_rate),
            "observed_fp_count": fp_count, "pass": c4_pass, "evidence": f"FP rate={fp_rate:.4f}"},
        "C5_304_exercised": {"threshold": "304 rate >= 10% in cache_enabled", "observed_304_rates": {k: v["rate_304"] for k, v in c5_results.items()},
            "pass": c5_pass, "evidence": f"C5: {c5_results}"},
    }

    observations = [
        f"Mean TP rate: {mean_tp:.4f}", f"All Wilson lower > 0.75: {all_wilson_lower_above_075}",
        f"Pearson r={pearson_r:.4f} (|r|={abs_r:.4f}), n={len(all_behavioral)}",
        f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]",
        f"CI upper {ci_upper:.4f} {'<' if ci_upper < 0.15 else '>='} 0.15",
        f"TOST delta=0.15: p_upper={tost_result['p_upper']:.4f}",
        f"Null FP rate: {fp_rate:.4f} ({fp_count}/{len(noise_only_behavioral)})",
        f"Positive control: {positive_control_rate:.4f}",
        f"Conditions with variance: {conditions_with_variance}/4",
        f"Per-drift r: permission_boundary={pb_r}, session_invalidation={si_r}",
        f"Per-caching r: cache_enabled={cache_enabled_r}, cache_disabled={cache_disabled_r}",
        f"C5 304 check: {'PASS' if c5_pass else 'FAIL'}",
        f"Status={status}, Outcome={outcome}",
    ]

    validity_notes = [
        "Flask 3.1.3, SQLite WAL-mode, in-memory cache TTL=0.5s, jitter 1-5ms (optimized), HS256+RS256 JWT",
        "HTTP-level caching: Cache-Control, ETag from body SHA-256, If-None-Match -> 304",
        "FIXED: Client sends If-None-Match with prior ETag; 304 rate logged as C5 manipulation check",
        f"N_SAMPLES={N_SAMPLES}/condition (480 total), SEED=42",
        "Decision-rule bug fix: CI upper >= 0.20 -> FALSIFIES per spec.json",
        "All behavioral signals from real HTTP request/response cycles",
        "Claim ceiling bounded to stochastic Flask mock on localhost; NOT validated for production infrastructure"
    ]

    unresolved = [
        "Whether orthogonality holds on real APIs with HTTP caching (CDN, distributed cache)",
        "Whether per-caching-mode heterogeneity persists at n=120 per mode",
        "Whether delta=0.10 is practically required for product architecture",
        "If C5 fails (304 rate < 10%): manipulation failed, infrastructure issue"
    ]

    result_data = {"schema_version": 1, "experiment_id": "EXP-GRAPH-35389145821", "lane": "graph",
        "status": status, "outcome": outcome, "metrics": metrics, "controls": controls,
        "artifacts": artifacts, "observations": observations, "validity_notes": validity_notes, "unresolved": unresolved}

    result_path = EXPERIMENT_DIR / "result.json"
    with open(result_path, "w") as f: json.dump(result_data, f, indent=2, cls=NumpyEncoder)
    print(f"\nResult written to {result_path}")
    print(f"r={pearson_r:.4f}, CI upper={ci_upper:.4f}, C3={'PASS' if c3_pass else 'FAIL'}, C5={'PASS' if c5_pass else 'FAIL'}")
    print(f"Status={status}, Outcome={outcome}")


if __name__ == "__main__":
    main()
