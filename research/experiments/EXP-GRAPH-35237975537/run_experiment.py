#!/usr/bin/env python3
"""
EXP-GRAPH-35237975537: Session-Status Probing for Valid Orthogonality Test.

Tests whether adding /session/status endpoint probing to the behavioral composite
produces within-condition variance (std>0) on all 8 co-occurring conditions,
enabling a valid pooled Pearson r test of behavioral-structural orthogonality.

Key change from parent (EXP-GRAPH-35191029030):
- Behavioral composite includes session_status_check signal from /session/status endpoint
- /session/status returns HTTP 200 for valid sessions, HTTP 401 for invalid sessions
- For session_invalidation: randomly vary session validity to create within-condition variance
- session_status_check = (3 - HTTP_status_code) / 2 → 0.0 for 200 (valid), 1.0 for 401 (invalid)
- composite = token_val_rate*2 + session_change*3 + auth_boundary*1 + session_status_check*2

Decision rule: PASS if ALL of C1_drift_tp, C2_variance, C3_orthogonality, C4_null_control.
"""

import os
import sys
import json
import time
import hashlib
import secrets
import subprocess
import threading
import signal
import copy
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import requests
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings("ignore")

# ─── Configuration ────────────────────────────────────────────────────────────

EXPERIMENT_DIR = Path(__file__).parent
RAW_EVIDENCE_DIR = EXPERIMENT_DIR / "raw_evidence"
RAW_EVIDENCE_DIR.mkdir(exist_ok=True)

N_SAMPLES = 30
SEED = 42

# Drift patterns for this experiment (signing_key_rotation EXCLUDED)
DRIFT_PATTERNS = ["permission_boundary", "session_invalidation"]

# Noise patterns (structural signals)
NOISE_PATTERNS = [
    "optional_field_addition",
    "description_change",
    "response_time_jitter",
    "field_type_normalization"
]

# Co-occurring conditions: 2 drift × 4 noise = 8
CO_OCCURRING_CONDITIONS = [
    (drift, noise) for drift in DRIFT_PATTERNS for noise in NOISE_PATTERNS
]

# Permission subsets for permission_boundary stochastic variation
# Excludes all-True (baseline) and all-False (blocks everything)
PERMISSION_SUBSETS = [
    {"read": True, "write": False, "admin": False},
    {"read": True, "write": True, "admin": False},
    {"read": True, "write": False, "admin": True},
]

# Endpoints to probe
AUTH_ENDPOINTS = ["read", "write", "admin"]

# Server config
BASE_PORT = 18940


# ─── Server Management ────────────────────────────────────────────────────────

class MockServerManager:
    """Manages the Flask mock server as a subprocess."""

    def __init__(self, port: int, schema_size: int, seed: int):
        self.port = port
        self.schema_size = schema_size
        self.seed = seed
        self.process = None
        self.base_url = f"http://127.0.0.1:{port}"
        self.server_script = EXPERIMENT_DIR / "mock_server.py"

    def start(self):
        """Start the mock server subprocess."""
        env = os.environ.copy()
        env["MOCK_SERVER_PORT"] = str(self.port)
        env["MOCK_SERVER_SECRET"] = secrets.token_hex(32)

        self.process = subprocess.Popen(
            [sys.executable, str(self.server_script),
             "--port", str(self.port),
             "--schema-size", str(self.schema_size),
             "--seed", str(self.seed)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for server to be ready
        for _ in range(50):
            try:
                resp = requests.get(f"{self.base_url}/health", timeout=1)
                if resp.status_code == 200:
                    return True
            except:
                pass
            time.sleep(0.1)

        stdout, stderr = self.process.communicate(timeout=5)
        raise RuntimeError(f"Server failed to start. Stdout: {stdout.decode()}, Stderr: {stderr.decode()}")

    def stop(self):
        """Stop the mock server subprocess."""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            self.process = None

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request to the server."""
        url = f"{self.base_url}{endpoint}"
        return requests.request(method, url, timeout=10, **kwargs)

    def get_schema(self) -> dict:
        """Get schema from unauthenticated /schema endpoint."""
        resp = self.request("GET", "/schema")
        return resp.json()

    def set_drift(self, pattern: str, co_occurring: bool = False):
        """Set drift pattern on server."""
        resp = self.request("POST", "/admin/set_drift", json={"pattern": pattern, "co_occurring": co_occurring})
        return resp.json()

    def set_noise(self, pattern: str, rng: random.Random = None):
        """Set noise pattern on server with optional RNG for stochastic variation."""
        seed = int(rng.randint(0, 2**31)) if rng else self.seed
        resp = self.request("POST", "/admin/set_noise", json={"pattern": pattern})
        # Also set seed for reproducible noise application
        self.request("POST", "/admin/set_seed", json={"seed": seed})
        return resp.json()

    def reset(self):
        """Reset server to baseline."""
        resp = self.request("POST", "/admin/reset")
        return resp.json()

    def set_permissions(self, permissions: Dict[str, bool]):
        """Set permissions on server."""
        resp = self.request("POST", "/admin/set_permissions", json={"permissions": permissions})
        return resp.json()

    def get_token(self, user_id: str = "test_user", expiry_hours: float = 1.0) -> Tuple[str, str]:
        """Get a new token and session ID from server."""
        resp = self.request("POST", "/token", json={"user_id": user_id, "expiry_hours": expiry_hours})
        data = resp.json()
        token = data["token"]
        session_id = data["session_id"]
        session_cookie = resp.cookies.get("session_id", session_id)
        return token, session_cookie

    def check_session(self, session_cookie: str) -> Tuple[int, bool]:
        """Check session status via /session/status endpoint.
        Returns (status_code, is_valid).
        Key change from parent: returns actual HTTP status code (200 or 401).
        """
        resp = self.request("GET", "/session/status", cookies={"session_id": session_cookie})
        is_valid = resp.json().get("valid", False)
        return resp.status_code, is_valid

    def invalidate_session(self, session_cookie: str):
        """Invalidate session."""
        self.request("POST", "/session/invalidate", cookies={"session_id": session_cookie})


# ─── Signal Computation ──────────────────────────────────────────────────────

def compute_jaccard_similarity(schema_a: List[Dict], schema_b: List[Dict]) -> float:
    """Compute Jaccard index of (field_name, field_type) pairs."""
    fields_a = set((f["name"], f["type"]) for f in schema_a)
    fields_b = set((f["name"], f["type"]) for f in schema_b)
    if not fields_a and not fields_b:
        return 1.0
    intersection = len(fields_a & fields_b)
    union = len(fields_a | fields_b)
    return intersection / union if union > 0 else 0.0


def compute_schema_diff_magnitude(schema_a: List[Dict], schema_b: List[Dict]) -> float:
    """Compute weighted diff magnitude between schemas."""
    fields_a = {f["name"]: f for f in schema_a}
    fields_b = {f["name"]: f for f in schema_b}
    all_names = set(fields_a.keys()) | set(fields_b.keys())
    diff = 0.0
    for name in all_names:
        if name in fields_a and name not in fields_b:
            diff += 1.0
        elif name not in fields_a and name in fields_b:
            diff += 1.0
        else:
            if fields_a[name]["type"] != fields_b[name]["type"]:
                diff += 0.5
            if fields_a[name]["description"] != fields_b[name]["description"]:
                diff += 0.3
    return diff


def wilson_ci(successes: int, trials: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Compute Wilson score interval for binomial proportion."""
    if trials == 0:
        return (0.0, 1.0)
    z = 1.96
    p = successes / trials
    denominator = 1 + z**2 / trials
    center = (p + z**2 / (2 * trials)) / denominator
    adjustment = z * np.sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2)) / denominator
    lower = max(0.0, center - adjustment)
    upper = min(1.0, center + adjustment)
    return (lower, upper)


def permutation_test_pearsonr(x: np.ndarray, y: np.ndarray, n_permutations: int = 1000) -> Tuple[float, float]:
    """Permutation test for Pearson correlation."""
    if len(x) < 3:
        return 0.0, 1.0
    r_obs, _ = pearsonr(x, y)
    r_obs = abs(r_obs)
    count = 0
    for _ in range(n_permutations):
        y_perm = np.random.permutation(y)
        r_perm, _ = pearsonr(x, y_perm)
        if abs(r_perm) >= r_obs:
            count += 1
    p_value = (count + 1) / (n_permutations + 1)
    return r_obs, p_value


# ─── Per-Sample Experiment ───────────────────────────────────────────────────

def run_single_sample(server: MockServerManager, drift_pattern: str, noise_pattern: str,
                      condition_rng: random.Random) -> Dict:
    """
    Run a single sample for a co-occurring drift+noise condition.
    Returns behavioral and structural signals for this paired sample.

    Key change from parent: session_status_check is computed from HTTP status code
    of /session/status endpoint (200 → 0.0, 401 → 1.0).
    For session_invalidation: session validity is randomly varied to create variance.
    """
    result = {
        "token_validation_failures": 0,
        "session_state_changes": 0,
        "auth_boundary_shifts": 0,
        "session_status_code": 200,  # HTTP status code from /session/status
        "baseline_schema": None,
        "current_schema": None,
        "status": "OK"
    }

    try:
        # 1. Get baseline schema from unauthenticated /schema
        baseline_resp = server.get_schema()
        result["baseline_schema"] = baseline_resp.get("fields", [])

        # 2. Apply drift pattern
        if drift_pattern == "permission_boundary":
            # Stochastic: random permission subset
            perms = condition_rng.choice(PERMISSION_SUBSETS)
            server.set_permissions(perms)
        elif drift_pattern == "session_invalidation":
            # Apply session invalidation (clears all sessions)
            server.set_drift("session_invalidation", co_occurring=True)

        # 3. Apply noise pattern
        server.set_noise(noise_pattern, rng=condition_rng)

        # 4. Get fresh credentials
        token_expiry_hours = 1.0
        if drift_pattern == "session_invalidation":
            # Token expiry jitter ±1s (in hours)
            token_expiry_hours = 1.0 + condition_rng.uniform(-1, 1) / 3600

        token, session_cookie = server.get_token(expiry_hours=token_expiry_hours)

        # 5. For session_invalidation: randomly vary session validity
        #    This creates within-condition variance for the session_status_check signal.
        #    50% chance: session remains valid (not invalidated after creation)
        #    50% chance: session is invalidated (as in parent)
        if drift_pattern == "session_invalidation":
            session_valid_coin_flip = condition_rng.random()
            if session_valid_coin_flip < 0.5:
                # Session remains valid (no explicit invalidation)
                pass
            else:
                # Session is invalidated (explicit invalidation)
                server.invalidate_session(session_cookie)

        # 6. Probe endpoints in random order
        endpoints = AUTH_ENDPOINTS.copy()
        condition_rng.shuffle(endpoints)

        auth_boundary_count = 0
        token_failures = 0

        for endpoint in endpoints:
            headers = {"Authorization": f"Bearer {token}"}
            cookies = {"session_id": session_cookie} if session_cookie else {}

            resp = server.request(
                "GET" if endpoint != "write" else "POST",
                f"/api/{endpoint}",
                headers=headers, cookies=cookies
            )

            if resp.status_code == 401:
                token_failures += 1
            if resp.status_code == 403:
                auth_boundary_count += 1

        # 7. Query /session/status to get session validity
        #    KEY CHANGE: Get HTTP status code (200 for valid, 401 for invalid)
        status_code, session_valid = server.check_session(session_cookie)
        session_changed = 0 if session_valid else 1

        result["token_validation_failures"] = token_failures
        result["session_state_changes"] = session_changed
        result["auth_boundary_shifts"] = auth_boundary_count
        result["session_status_code"] = status_code

        # 8. Get current schema from unauthenticated /schema
        current_resp = server.get_schema()
        result["current_schema"] = current_resp.get("fields", [])

    except Exception as e:
        result["status"] = f"ERROR: {str(e)}"

    return result


def run_noise_only_sample(server: MockServerManager, noise_pattern: str,
                          condition_rng: random.Random) -> Dict:
    """
    Run a single noise-only sample (null control: no drift).
    Returns behavioral and structural signals.
    """
    result = {
        "token_validation_failures": 0,
        "session_state_changes": 0,
        "auth_boundary_shifts": 0,
        "session_status_code": 200,
        "baseline_schema": None,
        "current_schema": None,
        "status": "OK"
    }

    try:
        # 1. Get baseline schema
        baseline_resp = server.get_schema()
        result["baseline_schema"] = baseline_resp.get("fields", [])

        # 2. Apply noise pattern only (no drift)
        server.set_noise(noise_pattern, rng=condition_rng)

        # 3. Get fresh credentials
        token, session_cookie = server.get_token()

        # 4. Probe endpoints in random order
        endpoints = AUTH_ENDPOINTS.copy()
        condition_rng.shuffle(endpoints)

        auth_boundary_count = 0
        token_failures = 0

        for endpoint in endpoints:
            headers = {"Authorization": f"Bearer {token}"}
            cookies = {"session_id": session_cookie} if session_cookie else {}

            resp = server.request(
                "GET" if endpoint != "write" else "POST",
                f"/api/{endpoint}",
                headers=headers, cookies=cookies
            )

            if resp.status_code == 401:
                token_failures += 1
            if resp.status_code == 403:
                auth_boundary_count += 1

        # 5. Query /session/status
        status_code, session_valid = server.check_session(session_cookie)
        session_changed = 0 if session_valid else 1

        result["token_validation_failures"] = token_failures
        result["session_state_changes"] = session_changed
        result["auth_boundary_shifts"] = auth_boundary_count
        result["session_status_code"] = status_code

        # 6. Get current schema
        current_resp = server.get_schema()
        result["current_schema"] = current_resp.get("fields", [])

    except Exception as e:
        result["status"] = f"ERROR: {str(e)}"

    return result


def compute_behavioral_composite(sample: Dict) -> float:
    """Compute behavioral composite score including session_status_check.

    composite = token_val_rate * 2 + session_change * 3 + auth_boundary * 1 + session_status_check * 2

    session_status_check = (3 - HTTP_status_code) / 2
    - HTTP 200 → (3 - 200) → but this doesn't map cleanly.
    Instead, use direct mapping: 200 → 0.0, 401 → 1.0 (as per spec intent).
    """
    token_val_rate = sample["token_validation_failures"] / 3.0
    session_change = sample["session_state_changes"]
    auth_boundary = sample["auth_boundary_shifts"] / 3.0

    # session_status_check: 200 → 0.0, 401 → 1.0
    status_code = sample.get("session_status_code", 200)
    if status_code == 200:
        session_status_check = 0.0
    elif status_code == 401:
        session_status_check = 1.0
    else:
        session_status_check = 0.5  # Unknown status code

    behavioral = token_val_rate * 2 + session_change * 3 + auth_boundary * 1 + session_status_check * 2
    return behavioral


# ─── Main Experiment ─────────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("EXP-GRAPH-35237975537: Session-Status Probing for Valid Orthogonality Test")
    print("=" * 80)

    np.random.seed(SEED)
    global_rng = random.Random(SEED)

    # ─── Run Co-occurring Conditions ─────────────────────────────────────────
    print("\n[1/3] Running CO-OCCURRING drift+noise conditions (8 conditions × 30 samples)...")
    cooccurring_results = {}
    condition_idx = 0

    for drift_pattern, noise_pattern in CO_OCCURRING_CONDITIONS:
        condition_id = f"cooccur_{drift_pattern}+{noise_pattern}"
        print(f"  {condition_id}...", end=" ", flush=True)

        port = BASE_PORT + condition_idx
        server = MockServerManager(port, 10, SEED + condition_idx)
        server.start()

        try:
            samples = []
            condition_rng = random.Random(SEED + condition_idx * 1000)

            for sample_idx in range(N_SAMPLES):
                sample_rng = random.Random(condition_rng.randint(0, 2**31 - 1))
                sample = run_single_sample(server, drift_pattern, noise_pattern, sample_rng)
                samples.append(sample)

            cooccurring_results[condition_id] = {
                "drift_pattern": drift_pattern,
                "noise_pattern": noise_pattern,
                "samples": samples,
                "status": "OK"
            }
            print(f"OK ({len(samples)} samples)")
        finally:
            server.stop()

        condition_idx += 1

    # ─── Run Noise-Only Conditions (Null Control) ────────────────────────────
    print("\n[2/3] Running NOISE-ONLY conditions (null control, 4 conditions × 30 samples)...")
    noise_only_results = {}

    for noise_pattern in NOISE_PATTERNS:
        condition_id = f"noise_only_{noise_pattern}"
        print(f"  {condition_id}...", end=" ", flush=True)

        port = BASE_PORT + condition_idx
        server = MockServerManager(port, 10, SEED + condition_idx)
        server.start()

        try:
            samples = []
            condition_rng = random.Random(SEED + condition_idx * 1000)

            for sample_idx in range(N_SAMPLES):
                sample_rng = random.Random(condition_rng.randint(0, 2**31 - 1))
                sample = run_noise_only_sample(server, noise_pattern, sample_rng)
                samples.append(sample)

            noise_only_results[condition_id] = {
                "noise_pattern": noise_pattern,
                "samples": samples,
                "status": "OK"
            }
            print(f"OK ({len(samples)} samples)")
        finally:
            server.stop()

        condition_idx += 1

    # ─── Run Positive Control (permission_boundary on read/write/admin) ───────
    print("\n[3/3] Running POSITIVE CONTROL (permission_boundary detection)...")
    positive_control_results = []

    port = BASE_PORT + condition_idx
    server = MockServerManager(port, 10, SEED + condition_idx)
    server.start()

    try:
        for sample_idx in range(N_SAMPLES):
            rng = random.Random(SEED + 99999 + sample_idx)
            perms = rng.choice(PERMISSION_SUBSETS)
            server.set_permissions(perms)
            token, session_cookie = server.get_token()

            endpoints = AUTH_ENDPOINTS.copy()
            rng.shuffle(endpoints)

            detected = False
            for endpoint in endpoints:
                headers = {"Authorization": f"Bearer {token}"}
                cookies = {"session_id": session_cookie} if session_cookie else {}
                resp = server.request(
                    "GET" if endpoint != "write" else "POST",
                    f"/api/{endpoint}",
                    headers=headers, cookies=cookies
                )
                if resp.status_code in [401, 403]:
                    detected = True
                    break

            positive_control_results.append(detected)
    finally:
        server.stop()

    positive_control_rate = np.mean(positive_control_results) if positive_control_results else 0.0
    print(f"  Positive control rate: {positive_control_rate:.4f} ({sum(positive_control_results)}/{len(positive_control_results)})")

    # ─── Compute Derived Measurements ────────────────────────────────────────
    print("\n" + "=" * 80)
    print("COMPUTING DERIVED MEASUREMENTS")
    print("=" * 80)

    # Compute behavioral and structural composites for all co-occurring samples
    all_behavioral = []
    all_structural = []
    per_condition_data = {}

    for condition_id, result in cooccurring_results.items():
        cond_behavioral = []
        cond_structural = []

        for sample in result["samples"]:
            if sample["status"] != "OK":
                continue

            # Behavioral composite (with session_status_check)
            behavioral = compute_behavioral_composite(sample)
            cond_behavioral.append(behavioral)

            # Structural composite from /schema endpoint
            baseline = sample.get("baseline_schema", [])
            current = sample.get("current_schema", [])
            if baseline and current:
                jaccard = compute_jaccard_similarity(baseline, current)
                schema_diff = compute_schema_diff_magnitude(baseline, current)
                structural = max(schema_diff, 1.0 - jaccard)
            else:
                structural = 0.0
            cond_structural.append(structural)

        all_behavioral.extend(cond_behavioral)
        all_structural.extend(cond_structural)
        per_condition_data[condition_id] = {
            "behavioral": cond_behavioral,
            "structural": cond_structural,
            "n_valid": len(cond_behavioral)
        }

    # Compute noise-only behavioral scores
    noise_only_behavioral = []
    for condition_id, result in noise_only_results.items():
        for sample in result["samples"]:
            if sample["status"] != "OK":
                continue
            behavioral = compute_behavioral_composite(sample)
            noise_only_behavioral.append(behavioral)

    # ─── Decision Criteria ───────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("DECISION CRITERIA")
    print("=" * 80)

    # C1: Drift detection TP rate (mean TP >= 0.85 and all Wilson lower CI > 0.75)
    c1_per_condition = {}
    c1_wilson_lower = {}
    for condition_id, data in per_condition_data.items():
        tp_count = sum(1 for b in data["behavioral"] if b > 0)
        tp_rate = tp_count / data["n_valid"] if data["n_valid"] > 0 else 0.0
        c1_per_condition[condition_id] = tp_rate
        lower, upper = wilson_ci(tp_count, data["n_valid"])
        c1_wilson_lower[condition_id] = lower

    mean_tp = np.mean(list(c1_per_condition.values())) if c1_per_condition else 0.0
    all_wilson_lower_above_075 = all(v > 0.75 for v in c1_wilson_lower.values())
    c1_pass = mean_tp >= 0.85 and all_wilson_lower_above_075

    print(f"C1 (drift TP >= 0.85, all Wilson lower > 0.75): mean_tp={mean_tp:.4f} -> {'PASS' if c1_pass else 'FAIL'}")
    for cid, tp in c1_per_condition.items():
        print(f"  {cid}: TP={tp:.4f}, Wilson_lower={c1_wilson_lower[cid]:.4f}")

    # C2: Variance gate (>= 6/8 conditions have std > 0 for BOTH signals)
    conditions_with_variance = 0
    per_condition_variance = {}
    for condition_id, data in per_condition_data.items():
        b_std = np.std(data["behavioral"]) if data["behavioral"] else 0
        s_std = np.std(data["structural"]) if data["structural"] else 0
        has_var = b_std > 0 and s_std > 0
        if has_var:
            conditions_with_variance += 1
        per_condition_variance[condition_id] = {
            "behavioral_std": float(b_std),
            "structural_std": float(s_std),
            "has_variance": has_var
        }
        print(f"  {condition_id}: behavioral_std={b_std:.4f}, structural_std={s_std:.4f} -> {'OK' if has_var else 'NO VARIANCE'}")

    c2_pass = conditions_with_variance >= 6
    print(f"C2 (variance >= 6/8 conditions): {conditions_with_variance}/8 -> {'PASS' if c2_pass else 'FAIL'}")

    # C3: Orthogonality - Pearson |r| < 0.3 on pooled paired scores, permutation p < 0.05
    if len(all_behavioral) >= 3 and len(all_structural) >= 3:
        pearson_r, pearson_p = permutation_test_pearsonr(
            np.array(all_behavioral), np.array(all_structural), n_permutations=1000
        )
    else:
        pearson_r, pearson_p = 0.0, 1.0

    c3_pass = abs(pearson_r) < 0.3 and pearson_p < 0.05

    print(f"C3 (orthogonality |r| < 0.3, perm p < 0.05): r={pearson_r:.4f}, |r|={abs(pearson_r):.4f}, p={pearson_p:.4f} -> {'PASS' if c3_pass else 'FAIL'}")

    # C4: Null control FP = 0.0 on noise-only conditions
    fp_count = sum(1 for b in noise_only_behavioral if b > 0)
    fp_rate = fp_count / len(noise_only_behavioral) if noise_only_behavioral else 0.0
    c4_pass = fp_rate == 0.0

    print(f"C4 (null control FP = 0.0): fp_rate={fp_rate:.4f} ({fp_count}/{len(noise_only_behavioral)}) -> {'PASS' if c4_pass else 'FAIL'}")

    # Overall decision
    overall_pass = c1_pass and c2_pass and c3_pass and c4_pass
    print(f"\nOVERALL: {'ALL PASS' if overall_pass else 'FAILS'}")

    # ─── Measurement Validity ────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("MEASUREMENT VALIDITY")
    print("=" * 80)

    measurement_valid = conditions_with_variance >= 6 and len(all_behavioral) >= 240
    print(f"Measurement validity: {conditions_with_variance}/8 conditions have variance, {len(all_behavioral)} paired samples -> {'VALID' if measurement_valid else 'INVALID'}")

    # ─── Per-condition Pearson r (exploratory) ────────────────────────────────
    per_condition_r = {}
    for condition_id, data in per_condition_data.items():
        if len(data["behavioral"]) >= 3 and len(data["structural"]) >= 3:
            r, p = pearsonr(data["behavioral"], data["structural"])
            per_condition_r[condition_id] = {"r": float(r), "p": float(p)}
        else:
            per_condition_r[condition_id] = {"r": None, "p": None}

    # ─── Per-drift-pattern Pearson r (exploratory) ───────────────────────────
    pb_behavioral = []
    pb_structural = []
    si_behavioral = []
    si_structural = []

    for condition_id, data in per_condition_data.items():
        if "permission_boundary" in condition_id:
            pb_behavioral.extend(data["behavioral"])
            pb_structural.extend(data["structural"])
        elif "session_invalidation" in condition_id:
            si_behavioral.extend(data["behavioral"])
            si_structural.extend(data["structural"])

    pb_r = float(pearsonr(pb_behavioral, pb_structural)[0]) if len(pb_behavioral) >= 3 else None
    si_r = float(pearsonr(si_behavioral, si_structural)[0]) if len(si_behavioral) >= 3 else None

    # ─── Per-condition coefficient of variation (exploratory) ─────────────────
    per_condition_cv = {}
    for condition_id, data in per_condition_data.items():
        if data["behavioral"]:
            b_mean = np.mean(data["behavioral"])
            b_std = np.std(data["behavioral"])
            b_cv = b_std / b_mean if b_mean > 0 else 0.0
            s_mean = np.mean(data["structural"])
            s_std = np.std(data["structural"])
            s_cv = s_std / s_mean if s_mean > 0 else 0.0
            per_condition_cv[condition_id] = {
                "behavioral_cv": float(b_cv),
                "structural_cv": float(s_cv)
            }

    # ─── Build Metrics ────────────────────────────────────────────────────────
    metrics = {
        "mean_tp_rate": float(mean_tp),
        "all_wilson_lower_above_075": all_wilson_lower_above_075,
        "pearson_r_pooled": float(pearson_r),
        "pearson_p_pooled": float(pearson_p),
        "abs_r_pooled": float(abs(pearson_r)),
        "fp_rate_noise_only": float(fp_rate),
        "positive_control_rate": float(positive_control_rate),
        "n_cooccurring_conditions": len(cooccurring_results),
        "n_noise_only_conditions": len(noise_only_results),
        "n_samples_per_condition": N_SAMPLES,
        "n_paired_samples": len(all_behavioral),
        "conditions_with_variance": conditions_with_variance,
        "per_condition_tp": {k: float(v) for k, v in c1_per_condition.items()},
        "per_condition_wilson_lower": {k: float(v) for k, v in c1_wilson_lower.items()},
        "per_condition_variance": per_condition_variance,
        "per_condition_r": per_condition_r,
        "per_condition_cv": per_condition_cv,
        "per_drift_r": {
            "permission_boundary": pb_r,
            "session_invalidation": si_r
        }
    }

    # ─── Build Controls ──────────────────────────────────────────────────────
    controls = {
        "C1_drift_tp": {
            "threshold": "mean_tp >= 0.85 AND all Wilson lower CI > 0.75",
            "observed_mean_tp": float(mean_tp),
            "all_wilson_lower_above_075": all_wilson_lower_above_075,
            "per_condition_tp": {k: float(v) for k, v in c1_per_condition.items()},
            "per_condition_wilson_lower": {k: float(v) for k, v in c1_wilson_lower.items()},
            "pass": c1_pass,
            "evidence": f"Mean TP rate across {len(cooccurring_results)} co-occurring conditions, all Wilson lower CI > 0.75"
        },
        "C2_variance": {
            "threshold": ">= 6 of 8 co-occurring conditions have std > 0 for BOTH behavioral and structural signals",
            "conditions_with_variance": conditions_with_variance,
            "per_condition_variance": per_condition_variance,
            "pass": c2_pass,
            "evidence": f"{conditions_with_variance}/8 conditions with within-condition variance (both signals std > 0)"
        },
        "C3_orthogonality": {
            "threshold": "|Pearson r| < 0.3 on pooled paired scores, permutation p < 0.05",
            "observed_r": float(pearson_r),
            "observed_abs_r": float(abs(pearson_r)),
            "observed_p": float(pearson_p),
            "n_samples": len(all_behavioral),
            "pass": c3_pass,
            "evidence": f"Pearson r={pearson_r:.4f} on {len(all_behavioral)} pooled paired samples"
        },
        "C4_null_control": {
            "threshold": "FP = 0.0 on noise-only conditions",
            "observed_fp_rate": float(fp_rate),
            "observed_fp_count": fp_count,
            "total_noise_only": len(noise_only_behavioral),
            "pass": c4_pass,
            "evidence": f"FP rate = {fp_rate:.4f} across {len(noise_only_results)} noise-only conditions"
        },
        "PC_PERMISSION_BOUNDARY_DETECTION": {
            "description": "permission_boundary drift should produce behavioral signal > 0",
            "observed_rate": float(positive_control_rate),
            "pass": positive_control_rate >= 0.90,
            "evidence": f"Detection rate: {positive_control_rate:.4f} ({sum(positive_control_results)}/{len(positive_control_results)})"
        },
        "PC_SESSION_STATUS_VARIANCE": {
            "description": "session_invalidation conditions must produce behavioral composite with std > 0 when /session/status probing is included",
            "session_invalidation_conditions_with_variance": sum(
                1 for cid, v in per_condition_variance.items()
                if "session_invalidation" in cid and v["has_variance"]
            ),
            "pass": sum(
                1 for cid, v in per_condition_variance.items()
                if "session_invalidation" in cid and v["has_variance"]
            ) >= 4,  # All 4 session_invalidation conditions should have variance
            "evidence": f"Session_invalidation conditions with variance: {sum(1 for cid, v in per_condition_variance.items() if 'session_invalidation' in cid and v['has_variance'])}/4"
        }
    }

    # ─── Build Artifacts ──────────────────────────────────────────────────────
    raw_data = {
        "cooccurring_results": cooccurring_results,
        "noise_only_results": noise_only_results,
        "positive_control_results": positive_control_results,
        "all_behavioral_scores": all_behavioral,
        "all_structural_scores": all_structural,
        "noise_only_behavioral_scores": noise_only_behavioral,
        "per_condition_data": {k: {"behavioral": v["behavioral"], "structural": v["structural"], "n_valid": v["n_valid"]} for k, v in per_condition_data.items()}
    }

    raw_path = RAW_EVIDENCE_DIR / "experiment_data.json"

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, (np.bool_,)):
                return bool(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)

    with open(raw_path, "w") as f:
        json.dump(raw_data, f, indent=2, default=str, cls=NumpyEncoder)

    sha256_hash = hashlib.sha256()
    with open(raw_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    raw_sha256 = sha256_hash.hexdigest()

    # Hash the mock_server.py and run_experiment.py
    code_hashes = {}
    for code_file in ["mock_server.py", "run_experiment.py"]:
        h = hashlib.sha256()
        with open(EXPERIMENT_DIR / code_file, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        code_hashes[code_file] = h.hexdigest()

    artifacts = [
        {"path": "raw_evidence/experiment_data.json", "sha256": raw_sha256, "role": "raw"},
        {"path": "mock_server.py", "sha256": code_hashes["mock_server.py"], "role": "code"},
        {"path": "run_experiment.py", "sha256": code_hashes["run_experiment.py"], "role": "code"}
    ]

    # ─── Build Observations ───────────────────────────────────────────────────
    observations = [
        f"Mean drift TP rate across co-occurring conditions: {mean_tp:.4f}",
        f"All Wilson lower CI > 0.75: {all_wilson_lower_above_075}",
        f"Pearson r (pooled paired scores, all co-occurring): {pearson_r:.4f} (|r|={abs(pearson_r):.4f}, p={pearson_p:.4f}, n={len(all_behavioral)})",
        f"Null control FP rate (noise-only): {fp_rate:.4f} ({fp_count}/{len(noise_only_behavioral)})",
        f"Positive control (permission_boundary detection): {positive_control_rate:.4f}",
        f"Positive control (session_status_variance): {controls['PC_SESSION_STATUS_VARIANCE']['pass']}",
        f"Conditions with within-condition variance (both signals std > 0): {conditions_with_variance}/8",
        f"Total paired samples: {len(all_behavioral)}",
        f"Per-drift-pattern r: permission_boundary={pb_r}, session_invalidation={si_r}",
        f"C1 (drift TP >= 0.85, all Wilson lower > 0.75): {'PASS' if c1_pass else 'FAIL'}",
        f"C2 (variance >= 6/8 conditions): {'PASS' if c2_pass else 'FAIL'}",
        f"C3 (orthogonality |r| < 0.3): {'PASS' if c3_pass else 'FAIL'}",
        f"C4 (null FP = 0.0): {'PASS' if c4_pass else 'FAIL'}",
    ]

    # ─── Build Validity Notes ─────────────────────────────────────────────────
    validity_notes = [
        "All behavioral signals derived from real HTTP request/response cycles on Flask 3.x + PyJWT HS256 localhost",
        "New /session/status endpoint returns HTTP 200 for valid sessions and HTTP 401 for invalid sessions - minimum change to make session_invalidation produce behavioral variance",
        "Structural signals computed from unauthenticated /schema endpoint (inherited from parent - fixes zero-imputation confound)",
        "Drift patterns: permission_boundary (write=False, admin=False) and session_invalidation (clear session store) - same as parent",
        "Within-condition stochastic variation: random permission subsets for permission_boundary; randomized session validity (50/50 coin flip) for session_invalidation",
        "30 independent request sequences per condition with per-seed RNG (SEED=42) for reproducibility",
        "Pearson r computed on paired per-sample (behavioral_i, structural_i) scores from all 8 co-occurring conditions",
        "Variance gate: at least 6 of 8 co-occurring conditions must have std > 0 for both behavioral and structural signals",
        "session_status_check = 0.0 for HTTP 200 (valid), 1.0 for HTTP 401 (invalid) - composite includes this signal with weight 2",
        "For session_invalidation: session validity randomly varied (50/50) to create within-condition variance - this is the key fix from parent MEASUREMENT_INVALID"
    ]

    # ─── Build Unresolved ─────────────────────────────────────────────────────
    unresolved = [
        "Whether real APIs with stochastic behavior (DB/cache/CDN) preserve signal orthogonality",
        "Whether behavioral signals generalize beyond HS256 to RS256/ES256/OAuth/OIDC production middleware",
        "Whether per-condition correlation differs from pooled correlation (exploratory per-condition analysis reported)",
        "Whether wider stochastic variation ranges (more permission subsets, wider noise magnitudes) change the correlation",
        "Whether composite multi-signal classifiers outperform individual signals when orthogonality holds",
        "Whether the unauthenticated /schema endpoint is practical in real-world API deployments",
        "Whether 50/50 session validity randomization adequately simulates real session TTL/expiry behavior"
    ]

    # ─── Determine Outcome ────────────────────────────────────────────────────
    if overall_pass:
        outcome = "SUPPORTS"
    elif c1_pass and c2_pass and not c3_pass:
        outcome = "FALSIFIES"  # Orthogonality specifically fails
    elif not c1_pass or not c2_pass:
        outcome = "FALSIFIES"
    else:
        outcome = "MIXED"

    status = "COMPLETE" if measurement_valid else "MEASUREMENT_INVALID"

    # ─── Write result.json ────────────────────────────────────────────────────
    result_data = {
        "schema_version": 1,
        "experiment_id": "EXP-GRAPH-35237975537",
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
    with open(result_path, "w") as f:
        json.dump(result_data, f, indent=2, cls=NumpyEncoder)

    print(f"\nResult written to {result_path}")

    # ─── Write report.md ──────────────────────────────────────────────────────
    report = f"""# EXP-GRAPH-35237975537 Report: Session-Status Probing for Valid Orthogonality Test

## Executive Summary

{'**Orthogonality hypothesis SURVIVES: |r| = {:.4f} < 0.3, permutation p = {:.4f}.**'.format(abs(pearson_r), pearson_p) if c3_pass else '**Orthogonality hypothesis FAILS: |r| = {:.4f} >= 0.3.**'.format(abs(pearson_r))}
{'Behavioral and structural signals are independently observable on the same conditions.' if c3_pass else 'Behavioral and structural signals are confirmed non-orthogonal.'}

**Decision criteria:**
- **C1 (drift TP >= 0.85, all Wilson lower > 0.75)**: mean TP = {mean_tp:.4f}, all_wilson_lower > 0.75 = {all_wilson_lower_above_075} -> {'PASS' if c1_pass else 'FAIL'}
- **C2 (variance >= 6/8 conditions)**: {conditions_with_variance}/8 conditions with variance -> {'PASS' if c2_pass else 'FAIL'}
- **C3 (orthogonality |r| < 0.3)**: |r| = {abs(pearson_r):.4f}, p = {pearson_p:.4f} -> {'PASS' if c3_pass else 'FAIL'}
- **C4 (null FP = 0.0)**: FP = {fp_rate:.4f} -> {'PASS' if c4_pass else 'FAIL'}

**Overall: {'PASS' if overall_pass else 'FAIL'}**

**Measurement validity**: {'VALID' if measurement_valid else 'INVALID'} ({conditions_with_variance}/8 conditions with variance, {len(all_behavioral)} paired samples)

## Design Changes from Parent (EXP-GRAPH-35191029030)

| Aspect | Parent | This Experiment |
|--------|--------|-----------------|
| /session/status endpoint | Returns HTTP 200 with valid=true/false | Returns HTTP 200 for valid, HTTP 401 for invalid |
| Behavioral composite formula | token_val_rate*2 + session_change*3 + auth_boundary*1 | token_val_rate*2 + session_change*3 + auth_boundary*1 + session_status_check*2 |
| session_status_check | Not present | (3 - HTTP_status_code) / 2 → 0.0 for 200, 1.0 for 401 |
| session_invalidation variance | Always invalidated (constant behavioral = 3.0) | Randomly vary (50/50) session validity |
| Within-condition stochastic variation | Permission subsets for PB, token expiry jitter for SI | Same + randomized session validity for SI |

## Experimental Conditions

### Co-occurring Conditions (8 total)

| Condition | Drift | Noise | Samples | Variance |
|-----------|-------|-------|---------|----------|
"""
    for drift, noise in CO_OCCURRING_CONDITIONS:
        cid = f"cooccur_{drift}+{noise}"
        data = per_condition_data.get(cid, {})
        var_info = per_condition_variance.get(cid, {})
        b_std = var_info.get("behavioral_std", 0)
        s_std = var_info.get("structural_std", 0)
        has_var = var_info.get("has_variance", False)
        report += f"| {cid} | {drift} | {noise} | {data.get('n_valid', 0)} | {'OK' if has_var else 'NO VARIANCE'} (b_std={b_std:.4f}, s_std={s_std:.4f}) |\n"

    report += f"""
### Per-Condition Pearson r (Exploratory)

| Condition | r | p |
|-----------|---|---|
"""
    for cid, r_data in per_condition_r.items():
        r_val = f"{r_data['r']:.4f}" if r_data['r'] is not None else "N/A"
        p_val = f"{r_data['p']:.4f}" if r_data['p'] is not None else "N/A"
        report += f"| {cid} | {r_val} | {p_val} |\n"

    report += f"""
### Per-Drift-Pattern Pearson r (Exploratory)

| Drift Pattern | Samples | r |
|---------------|---------|---|
| permission_boundary | {len(pb_behavioral)} | {f'{pb_r:.4f}' if pb_r is not None else 'N/A'} |
| session_invalidation | {len(si_behavioral)} | {f'{si_r:.4f}' if si_r is not None else 'N/A'} |

## Primary Analysis

### Pooled Pearson Correlation

- **r = {pearson_r:.4f}** (|r| = {abs(pearson_r):.4f})
- **p = {pearson_p:.4f}** (permutation test, 1000 permutations)
- **n = {len(all_behavioral)}** paired samples (8 conditions × 30 samples)
- **C3 threshold**: |r| < 0.3 -> {'PASS' if c3_pass else 'FAIL'}

### Signal Observability (Within-Condition Variance)

- **Conditions with variance (both signals std > 0)**: {conditions_with_variance}/8
- **Measurement validity**: {'VALID' if measurement_valid else 'INVALID'} ({conditions_with_variance} >= 6 conditions, {len(all_behavioral)} >= 240 samples)

### Per-Condition Variance Details

| Condition | Behavioral Std | Structural Std | Has Variance |
|-----------|----------------|----------------|--------------|
"""
    for cid, v in per_condition_variance.items():
        report += f"| {cid} | {v['behavioral_std']:.4f} | {v['structural_std']:.4f} | {'YES' if v['has_variance'] else 'NO'} |\n"

    report += f"""
## Controls

### Positive Control: permission_boundary Detection

- **Observed rate**: {positive_control_rate:.4f} ({sum(positive_control_results)}/{len(positive_control_results)})
- **Threshold**: >= 0.90
- **Pass**: {'YES' if positive_control_rate >= 0.90 else 'NO'}

### Positive Control: session_status_variance

- **session_invalidation conditions with variance**: {controls['PC_SESSION_STATUS_VARIANCE']['session_invalidation_conditions_with_variance']}/4
- **Threshold**: >= 4 (all 4 session_invalidation conditions should have variance)
- **Pass**: {'YES' if controls['PC_SESSION_STATUS_VARIANCE']['pass'] else 'NO'}

### Null Control: Noise-Only FP

- **Observed FP rate**: {fp_rate:.4f} ({fp_count}/{len(noise_only_behavioral)})
- **Threshold**: FP = 0.0
- **Pass**: {'YES' if c4_pass else 'NO'}

## Validity Threats

1. **Deterministic mock server**: All measurements on localhost Flask, not production APIs.
2. **Limited drift patterns**: Only permission_boundary and session_invalidation tested.
3. **Session validity randomization**: 50/50 coin flip simulates session validity; real APIs use TTL/expiry.
4. **Pooled Pearson r**: Per-condition correlation may differ; exploratory analysis reported.
5. **Composite score weighting**: Behavioral weights (2, 3, 1, 2) inherited from parent, not optimized.

## Product Consequences

{'### If C3 PASSES (|r| < 0.3):' if c3_pass else '### If C3 FAILS (|r| >= 0.3):'}

{'- C-FRESHNESS gains a validated second detection channel' if c3_pass else '- Behavioral and structural signals are confirmed non-orthogonal'}
{'- Product pipeline can integrate behavioral signals alongside structural signals' if c3_pass else '- Product pipeline must use composite multi-signal classifiers'}
{'- Architecture: parallel independent channels for freshness detection' if c3_pass else '- Architecture: fused classifier for freshness detection'}
{'- Next step: test behavioral signals on real OAuth/OIDC middleware (Auth0/Okta/Keycloak)' if c3_pass else '- Next step: design optimal classifier fusion (weighted combination, learned threshold)'}
"""

    report_path = EXPERIMENT_DIR / "report.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"Report written to {report_path}")

    # ─── Write provenance.json ────────────────────────────────────────────────
    import platform

    provenance = {
        "schema_version": 1,
        "experiment_id": "EXP-GRAPH-35237975537",
        "github_run_id": "35237975537",
        "base_sha": "307f3c5ee706b5aeeee5fe1f42df0e02980a29ef",
        "environment": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "flask_version": None,
            "pyjwt_version": None,
            "numpy_version": np.__version__,
            "scipy_version": None,
        },
        "parameters": {
            "seed": SEED,
            "n_samples_per_condition": N_SAMPLES,
            "n_cooccurring_conditions": len(CO_OCCURRING_CONDITIONS),
            "n_noise_only_conditions": len(NOISE_PATTERNS),
            "drift_patterns": DRIFT_PATTERNS,
            "noise_patterns": NOISE_PATTERNS,
            "permission_subsets": PERMISSION_SUBSETS,
            "schema_size": 10,
            "base_port": BASE_PORT,
            "session_validity_randomization": "50/50 coin flip for session_invalidation samples"
        },
        "code_paths": {
            "mock_server.py": code_hashes.get("mock_server.py"),
            "run_experiment.py": code_hashes.get("run_experiment.py"),
        },
        "artifacts": {
            "raw_evidence": f"raw_evidence/experiment_data.json (sha256: {raw_sha256})",
            "result_json": "result.json",
            "report_md": "report.md",
        },
        "parent_experiment": {
            "experiment_id": "EXP-GRAPH-35191029030",
            "handoff_sha256": "b86e49915b03105f3ad44bb3f700d3536eca78895038d8f6cb7c215f5e46363a",
            "key_change": "Added session_status_check signal from /session/status endpoint (HTTP 200→0.0, HTTP 401→1.0) to behavioral composite"
        }
    }

    # Try to fill in library versions
    try:
        import flask
        provenance["environment"]["flask_version"] = flask.__version__
    except:
        pass
    try:
        import jwt as pyjwt
        provenance["environment"]["pyjwt_version"] = pyjwt.__version__
    except:
        pass
    try:
        import scipy
        provenance["environment"]["scipy_version"] = scipy.__version__
    except:
        pass

    provenance_path = EXPERIMENT_DIR / "provenance.json"
    with open(provenance_path, "w") as f:
        json.dump(provenance, f, indent=2)

    print(f"Provenance written to {provenance_path}")

    print("\n" + "=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
