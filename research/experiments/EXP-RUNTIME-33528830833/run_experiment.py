#!/usr/bin/env python3
"""
EXP-RUNTIME-33528830833: HTTP Observation Substrate Validity Experiment

Tests whether a stdlib-only HTTP observation substrate produces
measurement-valid, discriminating observations that correctly attribute
response differences to auth/session state changes rather than confounds.
"""

import hashlib
import json
import os
import random
import socket
import sys
import threading
import time
import urllib.request
import urllib.error
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Optional

# ============================================================
# 1. DETERMINISTIC LOCAL HTTP SERVER
# ============================================================

# Fixed seed for any server-side randomness
SERVER_SEED = 42
random.seed(SERVER_SEED)

# Token states with deterministic expiry simulation
TOKENS = {
    "valid": {"status": "active", "expires": "2099-12-31T23:59:59Z", "user": "alice"},
    "near_expiry": {"status": "active", "expires": "2026-09-01T16:00:00Z", "user": "alice"},
    "expired": {"status": "expired", "expires": "2020-01-01T00:00:00Z", "user": "alice"},
    "invalid": {"status": "invalid", "expires": "N/A", "user": "alice"},
}

# Session cookies
SESSIONS = {
    "valid_session": {"session_id": "sess_abc123def456", "user": "alice", "role": "admin"},
}


class DeterministicHandler(BaseHTTPRequestHandler):
    """Handler with deterministic responses keyed by auth state."""

    def log_message(self, format, *args):
        """Suppress server logs to keep output clean."""
        pass

    def _get_auth_state(self) -> str:
        """Determine auth state from request headers."""
        auth = self.headers.get("Authorization", "")
        cookie = self.headers.get("Cookie", "")

        if auth.startswith("Bearer "):
            token = auth[7:]
            if token in TOKENS:
                return token
            return "invalid"
        elif "session_id=" in cookie:
            return "valid_session"
        else:
            return "public"

    def _generate_response(self, auth_state: str) -> Tuple[int, Dict[str, str], str]:
        """Generate deterministic response based on auth state."""
        if auth_state == "public":
            return (
                200,
                {
                    "Content-Type": "application/json",
                    "X-Auth-State": "public",
                    "X-Server-Id": "det-001",
                },
                json.dumps({"message": "Welcome, anonymous user", "data": None}),
            )
        elif auth_state == "valid":
            token_info = TOKENS["valid"]
            return (
                200,
                {
                    "Content-Type": "application/json",
                    "X-Auth-State": "authenticated",
                    "X-Server-Id": "det-001",
                    "X-User": token_info["user"],
                },
                json.dumps(
                    {
                        "message": f"Welcome, {token_info['user']}",
                        "data": {"secret": "classified_info_123"},
                    }
                ),
            )
        elif auth_state == "near_expiry":
            token_info = TOKENS["near_expiry"]
            return (
                200,
                {
                    "Content-Type": "application/json",
                    "X-Auth-State": "authenticated_near_expiry",
                    "X-Server-Id": "det-001",
                    "X-Token-Expiry": token_info["expires"],
                    "X-Warning": "token_expiring_soon",
                },
                json.dumps(
                    {
                        "message": f"Welcome, {token_info['user']}",
                        "data": {"secret": "classified_info_123"},
                        "warning": "Your token is expiring soon",
                    }
                ),
            )
        elif auth_state == "expired":
            return (
                401,
                {
                    "Content-Type": "application/json",
                    "X-Auth-State": "token_expired",
                    "X-Server-Id": "det-001",
                },
                json.dumps({"error": "Token expired", "code": "AUTH_EXPIRED"}),
            )
        elif auth_state == "invalid":
            return (
                403,
                {
                    "Content-Type": "application/json",
                    "X-Auth-State": "invalid_token",
                    "X-Server-Id": "det-001",
                },
                json.dumps({"error": "Invalid token", "code": "AUTH_INVALID"}),
            )
        elif auth_state == "valid_session":
            session_info = SESSIONS["valid_session"]
            return (
                200,
                {
                    "Content-Type": "application/json",
                    "X-Auth-State": "session_authenticated",
                    "X-Server-Id": "det-001",
                    "X-User": session_info["user"],
                    "X-Role": session_info["role"],
                },
                json.dumps(
                    {
                        "message": f"Welcome, {session_info['user']}",
                        "data": {
                            "secret": "classified_info_123",
                            "role": session_info["role"],
                        },
                    }
                ),
            )
        else:
            return (
                500,
                {"Content-Type": "application/json", "X-Server-Id": "det-001"},
                json.dumps({"error": "Unknown state"}),
            )

    def do_GET(self):
        auth_state = self._get_auth_state()
        status, headers, body = self._generate_response(auth_state)

        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_POST(self):
        auth_state = self._get_auth_state()
        status, headers, body = self._generate_response(auth_state)

        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))


def find_free_port() -> int:
    """Find a free port for the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def start_server(port: int) -> HTTPServer:
    """Start the deterministic HTTP server."""
    server = HTTPServer(("127.0.0.1", port), DeterministicHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


# ============================================================
# 2. HTTP OBSERVATION SUBSTRATE
# ============================================================


def compute_fingerprint(observation: Dict[str, Any]) -> str:
    """Compute SHA-256 fingerprint of an observation vector.
    
    Fingerprint = SHA-256 of (status_code, sorted_headers, body_sha256, redirect_chain)
    """
    redirect_chain = observation.get("redirect_chain", [])
    redirect_tuple = tuple(tuple(r) if isinstance(r, list) else r for r in redirect_chain)
    
    vector = (
        observation["status_code"],
        tuple(sorted(observation["headers"].items())),
        observation["body_sha256"],
        redirect_tuple,
    )
    
    serialized = json.dumps(vector, sort_keys=True).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def make_observation(
    url: str, auth_header: Optional[str] = None, cookie: Optional[str] = None
) -> Dict[str, Any]:
    """Make an HTTP request and capture raw observation + derived fingerprint."""
    headers = {}
    if auth_header:
        headers["Authorization"] = auth_header
    if cookie:
        headers["Cookie"] = cookie

    req = urllib.request.Request(url, headers=headers)
    
    redirect_chain = []
    status_code = None
    response_headers = {}
    body_bytes = b""

    try:
        class RedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                redirect_chain.append((code, newurl))
                return super().redirect_request(req, fp, code, msg, headers, newurl)

        opener = urllib.request.build_opener(RedirectHandler)
        with opener.open(req, timeout=10) as response:
            status_code = response.getcode()
            response_headers = dict(response.headers)
            body_bytes = response.read()
    except urllib.error.HTTPError as e:
        status_code = e.code
        response_headers = dict(e.headers)
        body_bytes = e.read()
    except Exception as e:
        status_code = 0
        response_headers = {"X-Error": str(e)}
        body_bytes = b""

    body_sha256 = hashlib.sha256(body_bytes).hexdigest()

    observation = {
        "status_code": status_code,
        "headers": response_headers,
        "body_sha256": body_sha256,
        "body_length": len(body_bytes),
        "redirect_chain": redirect_chain,
        "body_bytes": body_bytes.decode("utf-8", errors="replace"),
    }

    observation["fingerprint"] = compute_fingerprint(observation)
    return observation


# ============================================================
# 3. JACCARD SIMILARITY (for bit-level comparison)
# ============================================================


def hex_to_bits(hex_str: str) -> set:
    """Convert hex string to set of bit positions that are 1."""
    bits = set()
    for i, c in enumerate(hex_str):
        val = int(c, 16)
        for j in range(4):
            if val & (1 << (3 - j)):
                bits.add(i * 4 + j)
    return bits


def jaccard_similarity(a: str, b: str) -> float:
    """Compute Jaccard similarity between two fingerprint hex strings."""
    bits_a = hex_to_bits(a)
    bits_b = hex_to_bits(b)
    if not bits_a and not bits_b:
        return 1.0
    intersection = len(bits_a & bits_b)
    union = len(bits_a | bits_b)
    return intersection / union if union > 0 else 0.0


# ============================================================
# 4. BOOTSTRAP CONFIDENCE INTERVAL
# ============================================================


def bootstrap_ci(data: List[float], n_bootstrap: int = 1000, ci: float = 0.95) -> Tuple[float, float, float]:
    """Compute bootstrap confidence interval for mean."""
    random.seed(42)
    means = []
    for _ in range(n_bootstrap):
        sample = random.choices(data, k=len(data))
        means.append(sum(sample) / len(sample))
    means.sort()
    lower_idx = int((1 - ci) / 2 * n_bootstrap)
    upper_idx = int((1 + ci) / 2 * n_bootstrap)
    return (sum(data) / len(data), means[lower_idx], means[upper_idx])


# ============================================================
# 5. BASELINE FUNCTIONS
# ============================================================


def baseline_url_hash(url: str) -> str:
    """Baseline B-URL-HASH: SHA-256 of URL only."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def baseline_random() -> str:
    """Baseline B-RANDOM: Random 256-bit fingerprint."""
    return hashlib.sha256(os.urandom(32)).hexdigest()


def baseline_timing() -> str:
    """Baseline B-TIMING: SHA-256 of timestamp only."""
    return hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest()


# ============================================================
# 6. MAIN EXPERIMENT
# ============================================================


def run_experiment():
    """Execute the full experiment."""
    random.seed(42)
    
    port = find_free_port()
    server = start_server(port)
    base_url = f"http://127.0.0.1:{port}/test"
    
    time.sleep(0.1)  # Let server start
    
    print(f"Server running on port {port}")
    
    # Define the 5 server states
    states = {
        "public": {"auth_header": None, "cookie": None, "description": "No auth header"},
        "valid_token": {"auth_header": "Bearer valid", "cookie": None, "description": "Valid auth token"},
        "near_expiry": {"auth_header": "Bearer near_expiry", "cookie": None, "description": "Near-expiry token"},
        "expired_token": {"auth_header": "Bearer expired", "cookie": None, "description": "Expired token"},
        "invalid_token": {"auth_header": "Bearer invalid", "cookie": None, "description": "Invalid token"},
    }
    
    # Holdout state (not seen during fingerprint calibration)
    holdout_state = {
        "session_cookie": {"auth_header": None, "cookie": "session_id=sess_abc123def456", "description": "Valid session cookie (held out)"},
    }
    
    n_repetitions = 10
    
    # Raw observations storage
    raw_observations = {}
    fingerprints = {}
    
    # ---- Phase 1: Collect observations for all states ----
    print("\n=== Phase 1: Collecting observations ===")
    
    all_states = {**states, **holdout_state}
    state_order = list(all_states.keys())
    random.shuffle(state_order)
    
    for state_name in state_order:
        state = all_states[state_name]
        raw_observations[state_name] = []
        fingerprints[state_name] = []
        
        for rep in range(n_repetitions):
            obs = make_observation(
                base_url,
                auth_header=state["auth_header"],
                cookie=state["cookie"],
            )
            raw_observations[state_name].append(obs)
            fingerprints[state_name].append(obs["fingerprint"])
            
            print(f"  State: {state_name}, Rep: {rep+1}, FP: {obs['fingerprint'][:16]}...")
    
    # ---- Phase 2: Null control (reproducibility) ----
    print("\n=== Phase 2: Null control (reproducibility) ===")
    null_fingerprints = []
    null_obs = []
    for i in range(10):
        obs = make_observation(base_url)  # Same state each time
        null_fingerprints.append(obs["fingerprint"])
        null_obs.append(obs)
        print(f"  Null rep {i+1}: FP {obs['fingerprint'][:16]}...")
    
    # ---- Phase 3: Positive control (auth flip) ----
    print("\n=== Phase 3: Positive control ===")
    pos_no_auth = []
    pos_with_auth = []
    for i in range(10):
        obs_no = make_observation(base_url)
        obs_yes = make_observation(base_url, auth_header="Bearer valid")
        pos_no_auth.append(obs_no["fingerprint"])
        pos_with_auth.append(obs_yes["fingerprint"])
        print(f"  Positive rep {i+1}: no_auth={obs_no['fingerprint'][:16]}, with_auth={obs_yes['fingerprint'][:16]}")
    
    # ---- Phase 4: Drift control (valid -> near_expiry -> expired) ----
    print("\n=== Phase 4: Drift control ===")
    drift_states = ["valid_token", "near_expiry", "expired_token"]
    drift_fingerprints = {}
    for ds in drift_states:
        drift_fingerprints[ds] = []
        for i in range(5):
            state = states[ds]
            obs = make_observation(base_url, auth_header=state["auth_header"])
            drift_fingerprints[ds].append(obs["fingerprint"])
        print(f"  Drift state {ds}: FP {drift_fingerprints[ds][0][:16]}...")
    
    # ---- Phase 5: Compute metrics ----
    print("\n=== Phase 5: Computing metrics ===")
    
    # Null control FP rate: how many repeated identical requests produce different fingerprints?
    null_unique = len(set(null_fingerprints))
    null_fp_rate = 0.0 if null_unique == 1 else (null_unique - 1) / len(null_fingerprints)
    print(f"  Null control: unique fingerprints = {null_unique}, FP rate = {null_fp_rate:.3f}")
    
    # Positive control TP rate: how many auth-state changes produce different fingerprints?
    pos_matches = sum(1 for a, b in zip(pos_no_auth, pos_with_auth) if a == b)
    pos_tp_rate = 1.0 - (pos_matches / len(pos_no_auth))
    print(f"  Positive control: TP rate = {pos_tp_rate:.3f}")
    
    # Fingerprint reproducibility variance
    reproducibility = {}
    for state_name, fps in fingerprints.items():
        unique = len(set(fps))
        variance = (unique - 1) / len(fps) if unique > 0 else 0.0
        reproducibility[state_name] = {
            "unique_count": unique,
            "total": len(fps),
            "variance": variance,
        }
    print(f"  Reproducibility: { {k: v['unique_count'] for k, v in reproducibility.items()} }")
    
    # Drift monotonicity
    drift_medians = {}
    for ds in drift_states:
        # Compare with baseline (public state)
        sims = [jaccard_similarity(f, fingerprints["public"][0]) for f in drift_fingerprints[ds]]
        drift_medians[ds] = sum(sims) / len(sims)
    
    drift_order = sorted(drift_states, key=lambda s: drift_medians[s])
    is_monotonic = drift_order == drift_states  # valid > near_expiry > expired in similarity to public
    print(f"  Drift medians: {drift_medians}")
    print(f"  Drift monotonic: {is_monotonic}")
    
    # Discrimination score
    # Mean intra-state Jaccard similarity
    intra_sims = []
    for state_name, fps in fingerprints.items():
        if len(fps) < 2:
            continue
        for i in range(len(fps)):
            for j in range(i + 1, len(fps)):
                intra_sims.append(jaccard_similarity(fps[i], fps[j]))
    
    # Mean inter-state Jaccard similarity
    state_names = list(fingerprints.keys())
    inter_sims = []
    for i in range(len(state_names)):
        for j in range(i + 1, len(state_names)):
            for fi in fingerprints[state_names[i]]:
                for fj in fingerprints[state_names[j]]:
                    inter_sims.append(jaccard_similarity(fi, fj))
    
    mean_intra = sum(intra_sims) / len(intra_sims) if intra_sims else 0.0
    mean_inter = sum(inter_sims) / len(inter_sims) if inter_sims else 0.0
    
    if mean_inter > 0:
        discrimination_score = 1.0 - (mean_intra / mean_inter)
    else:
        discrimination_score = 1.0 if mean_intra == 0 else 0.0
    
    print(f"  Mean intra-state Jaccard: {mean_intra:.4f}")
    print(f"  Mean inter-state Jaccard: {mean_inter:.4f}")
    print(f"  Discrimination score: {discrimination_score:.4f}")
    
    # Bootstrap CI for discrimination score
    disc_values = []
    for _ in range(1000):
        sample_intra = random.choices(intra_sims, k=len(intra_sims)) if intra_sims else [0.0]
        sample_inter = random.choices(inter_sims, k=len(inter_sims)) if inter_sims else [1.0]
        mi = sum(sample_intra) / len(sample_intra)
        si = sum(sample_inter) / len(sample_inter)
        if si > 0:
            disc_values.append(1.0 - (mi / si))
        else:
            disc_values.append(1.0 if mi == 0 else 0.0)
    
    disc_values.sort()
    ci_lower = disc_values[int(0.025 * 1000)]
    ci_upper = disc_values[int(0.975 * 1000)]
    print(f"  Discrimination 95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
    
    # ---- Phase 6: Baselines ----
    print("\n=== Phase 6: Baselines ===")
    
    # For baselines, we simulate what a baseline would "observe"
    # B-URL-HASH: all requests to same URL get same fingerprint
    baseline_url_fps = [baseline_url_hash(base_url) for _ in range(10)]
    baseline_random_fps = [baseline_random() for _ in range(10)]
    baseline_timing_fps = [baseline_timing() for _ in range(10)]
    
    # Compute discrimination for each baseline
    def baseline_discrimination(baseline_fps: List[str], state_labels: List[str]) -> float:
        """How well does this baseline discriminate between states?"""
        # All requests to same URL -> same fingerprint for URL baseline
        # Different fingerprints for random/timing
        unique_fps = len(set(baseline_fps))
        total = len(baseline_fps)
        if unique_fps <= 1:
            return 0.0  # No discrimination
        return min(1.0, unique_fps / total)
    
    # For fair comparison, compute baseline discrimination across states
    # Each baseline generates fingerprints for each state
    baseline_url_all = []
    baseline_random_all = []
    baseline_timing_all = []
    state_labels_all = []
    
    for state_name in state_names:
        for _ in range(n_repetitions):
            baseline_url_all.append(baseline_url_hash(base_url))
            baseline_random_all.append(baseline_random())
            baseline_timing_all.append(baseline_timing())
            state_labels_all.append(state_name)
    
    # Baseline discrimination: how much variation across states vs within states
    def compute_baseline_discrimination(all_fps: List[str], labels: List[str]) -> float:
        """Discrimination score for a baseline."""
        if len(set(all_fps)) <= 1:
            return 0.0
        
        # Intra-state similarity
        intra = []
        for label in set(labels):
            fps_in_state = [f for f, l in zip(all_fps, labels) if l == label]
            for i in range(len(fps_in_state)):
                for j in range(i + 1, len(fps_in_state)):
                    intra.append(jaccard_similarity(fps_in_state[i], fps_in_state[j]))
        
        # Inter-state similarity
        inter = []
        unique_labels = list(set(labels))
        for i in range(len(unique_labels)):
            for j in range(i + 1, len(unique_labels)):
                fps_i = [f for f, l in zip(all_fps, labels) if l == unique_labels[i]]
                fps_j = [f for f, l in zip(all_fps, labels) if l == unique_labels[j]]
                for fi in fps_i:
                    for fj in fps_j:
                        inter.append(jaccard_similarity(fi, fj))
        
        mi = sum(intra) / len(intra) if intra else 0.0
        si = sum(inter) / len(inter) if inter else 1.0
        if si > 0:
            return 1.0 - (mi / si)
        return 1.0 if mi == 0 else 0.0
    
    b_url_disc = compute_baseline_discrimination(baseline_url_all, state_labels_all)
    b_random_disc = compute_baseline_discrimination(baseline_random_all, state_labels_all)
    b_timing_disc = compute_baseline_discrimination(baseline_timing_all, state_labels_all)
    
    print(f"  B-URL-HASH discrimination: {b_url_disc:.4f}")
    print(f"  B-RANDOM discrimination: {b_random_disc:.4f}")
    print(f"  B-TIMING discrimination: {b_timing_disc:.4f}")
    
    # ---- Phase 7: Holdout state discrimination ----
    print("\n=== Phase 7: Holdout state (session_cookie) ===")
    
    # Check that holdout state is discriminated from all seen states
    holdout_fp = fingerprints["session_cookie"]
    holdout_discriminated = True
    holdout_similarities = {}
    for seen_state in states.keys():
        sims = [jaccard_similarity(hf, sf) for hf in holdout_fp for sf in fingerprints[seen_state]]
        mean_sim = sum(sims) / len(sims)
        holdout_similarities[seen_state] = mean_sim
        if mean_sim > 0.95:  # Too similar to a seen state
            holdout_discriminated = False
            print(f"  WARNING: holdout similar to {seen_state}: {mean_sim:.4f}")
    
    print(f"  Holdout discriminated: {holdout_discriminated}")
    print(f"  Holdout similarities: {holdout_similarities}")
    
    # ---- Phase 8: Decision criteria ----
    print("\n=== Phase 8: Decision criteria ===")
    
    criteria = {
        "null_fp_rate_lt_5": null_fp_rate < 0.05,
        "positive_tp_rate_gt_95": pos_tp_rate > 0.95,
        "reproducibility_var_lt_5": all(v["variance"] < 0.05 for v in reproducibility.values()),
        "drift_monotonic": is_monotonic,
        "holdout_discriminated": holdout_discriminated,
        "all_baselines_worse": (
            discrimination_score > b_url_disc
            and discrimination_score > b_random_disc
            and discrimination_score > b_timing_disc
        ),
    }
    
    survives = all(criteria.values())
    
    for criterion, passed in criteria.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {criterion}: {status}")
    
    print(f"\n  OVERALL: {'SURVIVES' if survives else 'FALSIFIED'}")
    
    # ---- Phase 9: Assemble result ----
    result = {
        "experiment_id": "EXP-RUNTIME-33528830833",
        "lane": "runtime",
        "claim_id": "C-MEAS-VALID",
        "execution_status": "completed",
        "server_port": port,
        "server_seed": SERVER_SEED,
        
        "measurements": {
            "null_control": {
                "fingerprints": null_fingerprints,
                "unique_count": null_unique,
                "fp_rate": null_fp_rate,
            },
            "positive_control": {
                "no_auth_fingerprints": pos_no_auth,
                "with_auth_fingerprints": pos_with_auth,
                "tp_rate": pos_tp_rate,
            },
            "reproducibility": reproducibility,
            "drift_control": {
                "states_tested": drift_states,
                "fingerprints": drift_fingerprints,
                "medians": drift_medians,
                "is_monotonic": is_monotonic,
            },
            "discrimination": {
                "mean_intra_jaccard": mean_intra,
                "mean_inter_jaccard": mean_inter,
                "discrimination_score": discrimination_score,
                "ci_95_lower": ci_lower,
                "ci_95_upper": ci_upper,
            },
            "holdout": {
                "state": "session_cookie",
                "discriminated": holdout_discriminated,
                "similarities": holdout_similarities,
            },
            "baselines": {
                "B-URL-HASH": {"discrimination": b_url_disc},
                "B-RANDOM": {"discrimination": b_random_disc},
                "B-TIMING": {"discrimination": b_timing_disc},
            },
        },
        
        "fingerprints_by_state": {
            state: fingerprints[state] for state in state_names
        },
        
        "criteria": criteria,
        "verdict": "SURVIVES_CURRENT_TEST" if survives else "FALSIFIED",
        
        "per_state_summary": {},
    }
    
    # Per-state summary
    for state_name in state_names:
        fps = fingerprints[state_name]
        result["per_state_summary"][state_name] = {
            "unique_fingerprints": len(set(fps)),
            "total_observations": len(fps),
            "fingerprints": fps,
        }
    
    server.shutdown()
    
    return result


if __name__ == "__main__":
    result = run_experiment()
    
    # Write result
    output_path = os.path.join(os.path.dirname(__file__), "result.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nResults written to {output_path}")
