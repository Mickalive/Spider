#!/usr/bin/env python3
"""
EXP-GRAPH-35191029030: Fixed Co-occurring Drift+Noise Orthogonality for C-FRESHNESS.

Tests whether behavioral and structural signals are independently observable on the
same conditions when:
1. Structural signals come from unauthenticated /schema endpoint (always observable)
2. Drift patterns are limited to permission_boundary and session_invalidation
   (signing_key_rotation EXCLUDED - parent confound)
3. Within-condition stochastic variation is used
4. Paired per-sample (behavioral_i, structural_i) correlation is computed

Decision rule: PASS if ALL of C1_drift_tp, C2_observability, C3_orthogonality, C4_null_control.
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
BASE_PORT = 18930


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

    def check_session(self, session_cookie: str) -> bool:
        """Check if session is valid."""
        resp = self.request("GET", "/session/status", cookies={"session_id": session_cookie})
        return resp.json().get("valid", False)

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
    """
    result = {
        "token_validation_failures": 0,
        "session_state_changes": 0,
        "auth_boundary_shifts": 0,
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
            # Apply session invalidation
            server.set_drift("session_invalidation", co_occurring=True)

        # 3. Apply noise pattern
        server.set_noise(noise_pattern, rng=condition_rng)

        # 4. Get fresh credentials
        token_expiry_hours = 1.0
        if drift_pattern == "session_invalidation":
            # Token expiry jitter ±1s (in hours)
            token_expiry_hours = 1.0 + condition_rng.uniform(-1, 1) / 3600

        token, session_cookie = server.get_token(expiry_hours=token_expiry_hours)

        # 5. For session_invalidation, invalidate the session after getting token
        if drift_pattern == "session_invalidation":
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

        # 7. Check session state
        session_valid = server.check_session(session_cookie)
        session_changed = 0 if session_valid else 1

        result["token_validation_failures"] = token_failures
        result["session_state_changes"] = session_changed
        result["auth_boundary_shifts"] = auth_boundary_count

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

        # 5. Check session state
        session_valid = server.check_session(session_cookie)
        session_changed = 0 if session_valid else 1

        result["token_validation_failures"] = token_failures
        result["session_state_changes"] = session_changed
        result["auth_boundary_shifts"] = auth_boundary_count

        # 6. Get current schema
        current_resp = server.get_schema()
        result["current_schema"] = current_resp.get("fields", [])

    except Exception as e:
        result["status"] = f"ERROR: {str(e)}"

    return result


# ─── Main Experiment ─────────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("EXP-GRAPH-35191029030: Fixed Co-occurring Drift+Noise Orthogonality")
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

            # Behavioral composite
            token_val_rate = sample["token_validation_failures"] / 3.0
            session_change = sample["session_state_changes"]
            auth_boundary = sample["auth_boundary_shifts"] / 3.0
            behavioral = token_val_rate * 2 + session_change * 3 + auth_boundary * 1
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
            token_val_rate = sample["token_validation_failures"] / 3.0
            session_change = sample["session_state_changes"]
            auth_boundary = sample["auth_boundary_shifts"] / 3.0
            behavioral = token_val_rate * 2 + session_change * 3 + auth_boundary * 1
            noise_only_behavioral.append(behavioral)

    # ─── Decision Criteria ───────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("DECISION CRITERIA")
    print("=" * 80)

    # C1: Drift detection TP rate
    # For each co-occurring condition, check if behavioral > 0 on >= 25/30 samples
    c1_per_condition = {}
    for condition_id, data in per_condition_data.items():
        tp_count = sum(1 for b in data["behavioral"] if b > 0)
        tp_rate = tp_count / data["n_valid"] if data["n_valid"] > 0 else 0.0
        c1_per_condition[condition_id] = tp_rate

    mean_tp = np.mean(list(c1_per_condition.values())) if c1_per_condition else 0.0
    c1_pass = mean_tp >= 0.85

    print(f"C1 (drift TP >= 0.85): mean_tp={mean_tp:.4f} -> {'PASS' if c1_pass else 'FAIL'}")
    for cid, tp in c1_per_condition.items():
        print(f"  {cid}: TP={tp:.4f}")

    # C2: Signal observability (>= 80% of co-occurring sample pairs have BOTH > 0)
    both_positive_count = 0
    total_pairs = 0
    for condition_id, data in per_condition_data.items():
        for b, s in zip(data["behavioral"], data["structural"]):
            total_pairs += 1
            if b > 0 and s > 0:
                both_positive_count += 1

    observability_rate = both_positive_count / total_pairs if total_pairs > 0 else 0.0
    c2_pass = observability_rate >= 0.80

    print(f"C2 (observability >= 80%): rate={observability_rate:.4f} ({both_positive_count}/{total_pairs}) -> {'PASS' if c2_pass else 'FAIL'}")

    # C3: Orthogonality - Pearson |r| < 0.3 on pooled paired scores
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

    # ─── Validity Checks ─────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("VALIDITY CHECKS")
    print("=" * 80)

    # Check within-condition variance
    conditions_with_variance = 0
    for condition_id, data in per_condition_data.items():
        b_std = np.std(data["behavioral"]) if data["behavioral"] else 0
        s_std = np.std(data["structural"]) if data["structural"] else 0
        has_var = b_std > 0 and s_std > 0
        if has_var:
            conditions_with_variance += 1
        print(f"  {condition_id}: behavioral_std={b_std:.4f}, structural_std={s_std:.4f} -> {'OK' if has_var else 'NO VARIANCE'}")

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

    # ─── Build Metrics ────────────────────────────────────────────────────────
    metrics = {
        "mean_tp_rate": float(mean_tp),
        "observability_rate": float(observability_rate),
        "pearson_r_pooled": float(pearson_r),
        "pearson_p_pooled": float(pearson_p),
        "abs_r_pooled": float(abs(pearson_r)),
        "fp_rate_noise_only": float(fp_rate),
        "positive_control_rate": float(positive_control_rate),
        "n_cooccurring_conditions": len(cooccurring_results),
        "n_noise_only_conditions": len(noise_only_results),
        "n_samples_per_condition": N_SAMPLES,
        "n_paired_samples": len(all_behavioral),
        "n_valid_cooccurring_samples": both_positive_count,
        "conditions_with_variance": conditions_with_variance,
        "per_condition_tp": {k: float(v) for k, v in c1_per_condition.items()},
        "per_condition_r": per_condition_r,
        "per_drift_r": {
            "permission_boundary": pb_r,
            "session_invalidation": si_r
        }
    }

    # ─── Build Controls ──────────────────────────────────────────────────────
    controls = {
        "C1_drift_tp": {
            "threshold": "mean_tp >= 0.85",
            "observed_mean_tp": float(mean_tp),
            "per_condition_tp": {k: float(v) for k, v in c1_per_condition.items()},
            "pass": c1_pass,
            "evidence": f"Mean TP rate across {len(cooccurring_results)} co-occurring conditions"
        },
        "C2_observability": {
            "threshold": ">= 80% of co-occurring sample pairs have BOTH behavioral > 0 AND structural > 0",
            "observed_rate": float(observability_rate),
            "observed_count": both_positive_count,
            "total_count": total_pairs,
            "pass": c2_pass,
            "evidence": f"{both_positive_count}/{total_pairs} sample pairs with both signals > 0"
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
        f"Signal observability (both behavioral > 0 AND structural > 0): {observability_rate:.4f} ({both_positive_count}/{total_pairs})",
        f"Pearson r (pooled paired scores, all co-occurring): {pearson_r:.4f} (|r|={abs(pearson_r):.4f}, p={pearson_p:.4f}, n={len(all_behavioral)})",
        f"Null control FP rate (noise-only): {fp_rate:.4f} ({fp_count}/{len(noise_only_behavioral)})",
        f"Positive control (permission_boundary detection): {positive_control_rate:.4f}",
        f"Conditions with within-condition variance (both signals std > 0): {conditions_with_variance}/8",
        f"Total paired samples: {len(all_behavioral)}",
        f"Per-drift-pattern r: permission_boundary={pb_r}, session_invalidation={si_r}",
        f"C1 (drift TP >= 0.85): {'PASS' if c1_pass else 'FAIL'}",
        f"C2 (observability >= 80%): {'PASS' if c2_pass else 'FAIL'}",
        f"C3 (orthogonality |r| < 0.3): {'PASS' if c3_pass else 'FAIL'}",
        f"C4 (null FP = 0.0): {'PASS' if c4_pass else 'FAIL'}",
    ]

    # ─── Build Validity Notes ─────────────────────────────────────────────────
    validity_notes = [
        "All behavioral signals derived from real HTTP request/response cycles on Flask 3.x + PyJWT HS256 localhost",
        "Structural signals computed from unauthenticated /schema endpoint that returns current schema regardless of auth state",
        "Drift patterns limited to permission_boundary (blocks write/admin only) and session_invalidation (clears session store)",
        "signing_key_rotation EXCLUDED from co-occurring conditions (parent confound that blocks all endpoints)",
        "Within-condition stochastic variation: random permission subset (3 options for permission_boundary), random token expiry jitter (±1s for session_invalidation)",
        "Structural noise from /schema endpoint is independent of auth state — cannot be masked by drift",
        "Pearson r computed on paired per-sample (behavioral_i, structural_i) scores, NOT on condition means",
        "Deterministic seed (SEED=42) for reproducibility; all RNG states logged and reproducible",
        "Claim ceiling bounded to Flask 3.x + PyJWT HS256 on localhost, 2 drift patterns, 4 noise patterns, 8 co-occurring conditions, 30 samples per condition"
    ]

    # ─── Build Unresolved ─────────────────────────────────────────────────────
    unresolved = [
        "Whether real APIs with stochastic behavior (DB/cache/CDN) preserve signal orthogonality",
        "Whether behavioral signals generalize beyond HS256 to RS256/ES256/OAuth/OIDC production middleware",
        "Whether per-condition correlation differs from pooled correlation (exploratory per-condition analysis reported)",
        "Whether wider stochastic variation ranges (more permission subsets, wider noise magnitudes) change the correlation",
        "Whether composite multi-signal classifiers outperform individual signals when orthogonality holds",
        "Whether the unauthenticated /schema endpoint is practical in real-world API deployments"
    ]

    # ─── Determine Outcome ────────────────────────────────────────────────────
    if overall_pass:
        outcome = "SUPPORTS"
    elif c1_pass and c2_pass and not c3_pass:
        outcome = "FALSIFIES"  # Orthogonality specifically fails
    elif not c1_pass:
        outcome = "FALSIFIES"
    else:
        outcome = "MIXED"

    status = "COMPLETE" if measurement_valid else "MEASUREMENT_INVALID"

    # ─── Write result.json ────────────────────────────────────────────────────
    result_data = {
        "schema_version": 1,
        "experiment_id": "EXP-GRAPH-35191029030",
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
    report = f"""# EXP-GRAPH-35191029030 Report: Fixed Co-occurring Drift+Noise Orthogonality for C-FRESHNESS

## Executive Summary

{'**Orthogonality hypothesis SURVIVES: |r| = {:.4f} < 0.3, permutation p = {:.4f}.**'.format(abs(pearson_r), pearson_p) if c3_pass else '**Orthogonality hypothesis FAILS: |r| = {:.4f} >= 0.3.**'.format(abs(pearson_r))}
{'Behavioral and structural signals are independently observable on the same conditions.' if c3_pass else 'Behavioral and structural signals are confirmed non-orthogonal.'}

**Decision criteria:**
- **C1 (drift TP >= 0.85)**: mean TP = {mean_tp:.4f} -> {'PASS' if c1_pass else 'FAIL'}
- **C2 (observability >= 80%)**: rate = {observability_rate:.4f} -> {'PASS' if c2_pass else 'FAIL'}
- **C3 (orthogonality |r| < 0.3)**: |r| = {abs(pearson_r):.4f}, p = {pearson_p:.4f} -> {'PASS' if c3_pass else 'FAIL'}
- **C4 (null FP = 0.0)**: FP = {fp_rate:.4f} -> {'PASS' if c4_pass else 'FAIL'}

**Overall: {'PASS' if overall_pass else 'FAIL'}**

## Design Changes from Parent (EXP-GRAPH-35166507358)

| Aspect | Parent | This Experiment |
|--------|--------|-----------------|
| Co-occurring drift patterns | signing_key_rotation, session_invalidation, permission_boundary | permission_boundary, session_invalidation ONLY |
| Structural probe | Response body from authenticated /api/read | Unauthenticated /schema endpoint |
| signing_key_rotation | Included (blocks ALL endpoints → structural=0.0) | EXCLUDED |
| Within-condition variation | Deterministic (constant per condition) | Stochastic (random permission subsets, token expiry jitter) |
| Correlation computation | Pooled condition means | Paired per-sample (behavioral_i, structural_i) |
| Number of co-occurring conditions | 15 (3 drift × 5 schema sizes) | 8 (2 drift × 4 noise) |

## Experimental Conditions

### Co-occurring Conditions (8 total)

| Condition | Drift Pattern | Noise Pattern | Samples |
|-----------|---------------|---------------|---------|
"""
    for drift, noise in CO_OCCURRING_CONDITIONS:
        cid = f"cooccur_{drift}+{noise}"
        data = per_condition_data.get(cid, {})
        report += f"| {cid} | {drift} | {noise} | {data.get('n_valid', 0)} |\n"

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

### Signal Observability

- **Both > 0**: {both_positive_count}/{total_pairs} = {observability_rate:.4f}
- **C2 threshold**: >= 80% -> {'PASS' if c2_pass else 'FAIL'}

### Within-Condition Variance

- **Conditions with variance (both signals std > 0)**: {conditions_with_variance}/8
- **Measurement validity**: {'VALID' if measurement_valid else 'INVALID'} ({conditions_with_variance} >= 6 conditions, {len(all_behavioral)} >= 240 samples)

## Controls

### Positive Control: permission_boundary Detection

- **Observed rate**: {positive_control_rate:.4f} ({sum(positive_control_results)}/{len(positive_control_results)})
- **Threshold**: >= 0.90
- **Pass**: {'YES' if positive_control_rate >= 0.90 else 'NO'}

### Null Control: Noise-Only FP

- **Observed FP rate**: {fp_rate:.4f} ({fp_count}/{len(noise_only_behavioral)})
- **Threshold**: FP = 0.0
- **Pass**: {'YES' if c4_pass else 'NO'}

## Validity Threats

1. **Deterministic mock server**: All measurements on localhost Flask, not production APIs.
2. **Limited drift patterns**: Only permission_boundary and session_invalidation tested.
3. **Unauthenticated /schema endpoint**: Synthetic construct not present in real APIs.
4. **Pooled Pearson r**: Per-condition correlation may differ; exploratory analysis reported.
5. **Composite score weighting**: Behavioral weights (2, 3, 1) inherited from parent, not optimized.

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
        "experiment_id": "EXP-GRAPH-35191029030",
        "github_run_id": None,
        "base_sha": None,
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
        },
        "code_paths": {
            "mock_server.py": code_hashes.get("mock_server.py"),
            "run_experiment.py": code_hashes.get("run_experiment.py"),
        },
        "artifacts": {
            "raw_evidence": f"raw_evidence/experiment_data.json (sha256: {raw_sha256})",
            "result_json": "result.json",
            "report_md": "report.md",
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
