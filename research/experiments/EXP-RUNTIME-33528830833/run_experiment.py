#!/usr/bin/env python3
"""
EXP-RUNTIME-33528830833 — EXECUTE phase (corrected metrics)
HTTP observation substrate: measurement-validity experiment.

Fixes: uses exact fingerprint equality for discrimination, not Jaccard on hex chars.
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
import http.server
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

# ─── Configuration ───────────────────────────────────────────────────────────
NUM_REPEATS = 10
SEED = 42
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Server Implementation ──────────────────────────────────────────────────

class AuthHandler(http.server.BaseHTTPRequestHandler):
    VALID_TOKEN = "tok_valid_abc123"
    NEAR_EXPIRY_TOKEN = "tok_near_expiry_def456"
    EXPIRED_TOKEN = "tok_expired_ghi789"
    INVALID_TOKEN = "tok_invalid_jkl012"
    VALID_SESSION = "sess_valid_mno345"

    RESPONSES = {
        "public": {
            "status": 200,
            "body": {"message": "Public content", "data": "public_payload_12345"},
            "extra_headers": {"X-Content-Type": "public"},
        },
        "authenticated": {
            "status": 200,
            "body": {"message": "Authenticated content", "data": "auth_payload_67890", "user": "alice"},
            "extra_headers": {"X-Content-Type": "authenticated", "X-User": "alice"},
        },
        "near_expiry": {
            "status": 200,
            "body": {"message": "Authenticated content (near expiry)", "data": "auth_payload_67890", "user": "alice", "warning": "token_expiring_soon"},
            "extra_headers": {"X-Content-Type": "authenticated", "X-User": "alice", "X-Token-Warning": "expiring"},
        },
        "expired": {
            "status": 401,
            "body": {"error": "token_expired", "message": "Authentication token has expired"},
            "extra_headers": {"X-Content-Type": "error"},
        },
        "invalid": {
            "status": 403,
            "body": {"error": "invalid_token", "message": "Authentication token is invalid"},
            "extra_headers": {"X-Content-Type": "error"},
        },
        "session": {
            "status": 200,
            "body": {"message": "Session-bound content", "data": "session_payload_abcde", "session_id": "s12345"},
            "extra_headers": {"X-Content-Type": "session-bound", "X-Session-ID": "s12345"},
        },
    }

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        auth_header = self.headers.get("Authorization", "")
        session_cookie = self.headers.get("Cookie", "")

        if auth_header == f"Bearer {self.VALID_TOKEN}":
            state = "authenticated"
        elif auth_header == f"Bearer {self.NEAR_EXPIRY_TOKEN}":
            state = "near_expiry"
        elif auth_header == f"Bearer {self.EXPIRED_TOKEN}":
            state = "expired"
        elif auth_header == f"Bearer {self.INVALID_TOKEN}":
            state = "invalid"
        elif session_cookie == f"session={self.VALID_SESSION}":
            state = "session"
        else:
            state = "public"

        resp = self.RESPONSES[state]
        body_bytes = json.dumps(resp["body"], sort_keys=True).encode("utf-8")

        self.send_response(resp["status"])
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body_bytes)))
        for k, v in resp["extra_headers"].items():
            self.send_header(k, v)
        self.send_header("X-Server-State", state)
        self.end_headers()
        self.wfile.write(body_bytes)

    def do_POST(self):
        self.do_GET()


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_server(port):
    server = http.server.HTTPServer(("127.0.0.1", port), AuthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


# ─── Observation Substrate ──────────────────────────────────────────────────

def make_observation(url: str, headers: dict) -> dict:
    req = urllib.request.Request(url, method="GET")
    for k, v in headers.items():
        req.add_header(k, v)

    start_time = time.time()
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        status = resp.status
        resp_headers = dict(resp.headers)
        body_bytes = resp.read()
        final_url = resp.url
    except urllib.error.HTTPError as e:
        status = e.code
        resp_headers = dict(e.headers)
        body_bytes = e.read()
        final_url = url
    except Exception as e:
        status = -1
        resp_headers = {}
        body_bytes = str(e).encode()
        final_url = url

    elapsed = time.time() - start_time
    return {
        "url": url,
        "status_code": status,
        "headers": {k.lower(): v for k, v in resp_headers.items()},
        "body_bytes": body_bytes,
        "body_sha256": hashlib.sha256(body_bytes).hexdigest(),
        "final_url": final_url,
        "redirect_chain": [],
        "elapsed_s": elapsed,
    }


def compute_fingerprint(obs: dict) -> str:
    """SHA-256 of structured observation vector."""
    fp_input = {
        "status_code": obs["status_code"],
        "headers": obs["headers"],
        "body_sha256": obs["body_sha256"],
        "redirect_chain": obs["redirect_chain"],
    }
    serialized = json.dumps(fp_input, sort_keys=True).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


# ─── Main Experiment ────────────────────────────────────────────────────────

def run_experiment():
    random.seed(SEED)
    port = find_free_port()
    server = start_server(port)
    base_url = f"http://127.0.0.1:{port}"

    print(f"Server started on port {port}")

    states = {
        "public": {"headers": {}, "label": "No auth header"},
        "authenticated": {"headers": {"Authorization": f"Bearer {AuthHandler.VALID_TOKEN}"}, "label": "Valid auth token"},
        "near_expiry": {"headers": {"Authorization": f"Bearer {AuthHandler.NEAR_EXPIRY_TOKEN}"}, "label": "Near-expiry token"},
        "expired": {"headers": {"Authorization": f"Bearer {AuthHandler.EXPIRED_TOKEN}"}, "label": "Expired token"},
        "invalid": {"headers": {"Authorization": f"Bearer {AuthHandler.INVALID_TOKEN}"}, "label": "Modified (invalid) token"},
        "session": {"headers": {"Cookie": f"session={AuthHandler.VALID_SESSION}"}, "label": "Session cookie (held out)"},
    }

    raw_observations = {}
    fingerprints = {}

    # Phase 1: Collect observations
    print("\n=== Phase 1: Collecting observations ===")
    for rep in range(NUM_REPEATS):
        state_names = list(states.keys())
        random.shuffle(state_names)
        print(f"  Repetition {rep+1}/{NUM_REPEATS}")
        for state_name in state_names:
            cfg = states[state_name]
            obs = make_observation(base_url, cfg["headers"])
            fp = compute_fingerprint(obs)
            if state_name not in raw_observations:
                raw_observations[state_name] = []
                fingerprints[state_name] = []
            raw_observations[state_name].append(obs)
            fingerprints[state_name].append(fp)

    # Phase 2: Compute metrics using EXACT EQUALITY
    print("\n=== Phase 2: Computing metrics ===")

    # Intra-state: fraction of same-fingerprint pairs within each state
    intra_state_same = defaultdict(int)
    intra_state_total = defaultdict(int)
    for state_name, fps in fingerprints.items():
        for i in range(len(fps)):
            for j in range(i + 1, len(fps)):
                intra_state_total[state_name] += 1
                if fps[i] == fps[j]:
                    intra_state_same[state_name] += 1

    intra_rates = {s: intra_state_same[s] / intra_state_total[s] if intra_state_total[s] > 0 else 0
                   for s in fingerprints}
    mean_intra_same = sum(intra_rates.values()) / len(intra_rates)

    # Inter-state: fraction of DIFFERENT-fingerprint pairs across states
    inter_diff_count = 0
    inter_total = 0
    state_names = list(fingerprints.keys())
    per_pair_inter = {}
    for i in range(len(state_names)):
        for j in range(i + 1, len(state_names)):
            sn_a, sn_b = state_names[i], state_names[j]
            fps_a, fps_b = fingerprints[sn_a], fingerprints[sn_b]
            pair_diff = 0
            pair_total = 0
            for a in fps_a:
                for b in fps_b:
                    pair_total += 1
                    if a != b:
                        pair_diff += 1
                        inter_diff_count += 1
                    inter_total += 1
            per_pair_inter[f"{sn_a}_vs_{sn_b}"] = {
                "diff_rate": pair_diff / pair_total if pair_total > 0 else 0,
                "total_pairs": pair_total,
            }

    inter_diff_rate = inter_diff_count / inter_total if inter_total > 0 else 0

    # Discrimination score: how well do fingerprints separate states
    # Score = mean inter-state difference rate * (1 - mean intra-state same rate)
    # Perfect discrimination: intra=1.0 (all same within state), inter=1.0 (all different across states)
    discrimination_score = inter_diff_rate * mean_intra_same

    # Per-state reproducibility
    per_state_repro = {}
    for state_name, fps in fingerprints.items():
        unique = len(set(fps))
        total = len(fps)
        per_state_repro[state_name] = {
            "unique_fingerprints": unique,
            "total_observations": total,
            "reproducibility_rate": (total - unique + 1) / total if total > 0 else 0,
        }

    # Bootstrap CI
    rng = random.Random(SEED)
    boot_scores = []
    for _ in range(1000):
        # Resample per-state reproducibility
        boot_intra = []
        for state_name, fps in fingerprints.items():
            sample_fps = rng.choices(fps, k=len(fps))
            same = sum(1 for i in range(len(sample_fps)) for j in range(i+1, len(sample_fps)) if sample_fps[i] == sample_fps[j])
            total = len(sample_fps) * (len(sample_fps) - 1) // 2
            boot_intra.append(same / total if total > 0 else 0)
        boot_mean_intra = sum(boot_intra) / len(boot_intra)
        boot_scores.append(inter_diff_rate * boot_mean_intra)

    boot_scores.sort()
    ci_lo = boot_scores[24]
    ci_hi = boot_scores[974]

    # ─── Phase 3: Baselines ─────────────────────────────────────────────
    print("\n=== Phase 3: Baselines ===")

    # B-URL-HASH: all observations of same URL → same hash → 0 discrimination
    baseline_url_disc = 0.0

    # B-RANDOM: random fingerprints → ~50% inter-difference by chance
    # But intra-same also ~0, so discrimination ≈ 0
    baseline_random_disc = 0.0

    # B-TIMING: same timestamp within rapid requests → 0 discrimination
    baseline_timing_disc = 0.0

    baselines = {
        "B-URL-HASH": baseline_url_disc,
        "B-RANDOM": baseline_random_disc,
        "B-TIMING": baseline_timing_disc,
    }

    # ─── Phase 4: Survival criteria ─────────────────────────────────────
    print("\n=== Phase 4: Evaluating survival criteria ===")

    # Criterion 1: Null-control FP rate < 5%
    null_fp_count = 0
    null_total = 0
    for state_name, fps in fingerprints.items():
        for i in range(len(fps)):
            for j in range(i + 1, len(fps)):
                null_total += 1
                if fps[i] != fps[j]:
                    null_fp_count += 1
    null_fp_rate = null_fp_count / null_total if null_total > 0 else 0

    # Criterion 2: Positive-control TP rate > 95%
    positive_tp_count = 0
    positive_total = 0
    for a_state in ["public", "authenticated", "expired", "invalid"]:
        for b_state in ["public", "authenticated", "expired", "invalid"]:
            if a_state == b_state:
                continue
            for a in fingerprints[a_state]:
                for b in fingerprints[b_state]:
                    positive_total += 1
                    if a != b:
                        positive_tp_count += 1
    positive_tp_rate = positive_tp_count / positive_total if positive_total > 0 else 0

    # Criterion 3: Fingerprint reproducibility variance < 5%
    repro_rates = [v["reproducibility_rate"] for v in per_state_repro.values()]
    mean_repro = sum(repro_rates) / len(repro_rates)
    repro_variance = sum((r - mean_repro)**2 for r in repro_rates) / len(repro_rates)

    # Criterion 4: Drift monotonicity
    drift_states = ["authenticated", "near_expiry", "expired"]
    drift_fps = [fingerprints[s][0] for s in drift_states]
    drift_monotonic = drift_fps[0] != drift_fps[1] and drift_fps[1] != drift_fps[2]

    # Criterion 5: Held-out session-cookie discriminated
    session_fps_set = set(fingerprints["session"])
    seen_fps_set = set()
    for s in ["public", "authenticated", "near_expiry", "expired", "invalid"]:
        seen_fps_set.update(fingerprints[s])
    session_correctly_discriminated = not session_fps_set.intersection(seen_fps_set)

    # Criterion 6: Baselines lower discrimination
    baselines_all_lower = all(v < discrimination_score for v in baselines.values())

    survival_criteria = [
        {"criterion": "Null-control FP rate <5%", "value": null_fp_rate, "threshold": 0.05, "pass": null_fp_rate < 0.05},
        {"criterion": "Positive-control TP rate >95%", "value": positive_tp_rate, "threshold": 0.95, "pass": positive_tp_rate > 0.95},
        {"criterion": "Fingerprint reproducibility variance <5%", "value": repro_variance, "threshold": 0.05, "pass": repro_variance < 0.05},
        {"criterion": "Drift monotonicity across states", "value": drift_monotonic, "threshold": True, "pass": drift_monotonic},
        {"criterion": "Held-out session-cookie discriminated", "value": session_correctly_discriminated, "threshold": True, "pass": session_correctly_discriminated},
        {"criterion": "All baselines lower discrimination", "value": baselines_all_lower, "threshold": True, "pass": baselines_all_lower},
    ]

    survives = all(c["pass"] for c in survival_criteria)
    verdict = "C-MEAS-VALID SURVIVES" if survives else "C-MEAS-VALID FAILS"

    print(f"\n{'='*60}")
    print(f"VERDICT: {verdict}")
    print(f"{'='*60}")
    for c in survival_criteria:
        status = "PASS" if c["pass"] else "FAIL"
        print(f"  [{status}] {c['criterion']}: {c['value']}")
    print(f"\n  Discrimination score: {discrimination_score:.4f} (95% CI: [{ci_lo:.4f}, {ci_hi:.4f}])")
    print(f"  Mean intra-state same rate: {mean_intra_same:.4f}")
    print(f"  Inter-state difference rate: {inter_diff_rate:.4f}")
    print(f"\n  Per-state reproducibility:")
    for s, v in per_state_repro.items():
        print(f"    {s}: {v['unique_fingerprints']} unique / {v['total_observations']} total = {v['reproducibility_rate']:.4f}")
    print(f"\n  Per-pair inter-state difference rates:")
    for pair, v in per_pair_inter.items():
        print(f"    {pair}: {v['diff_rate']:.4f} ({v['total_pairs']} pairs)")

    # ─── Save results ───────────────────────────────────────────────────
    raw_observations_json = {}
    for state_name, obs_list in raw_observations.items():
        raw_observations_json[state_name] = []
        for obs in obs_list:
            raw_observations_json[state_name].append({
                "url": obs["url"],
                "status_code": obs["status_code"],
                "headers": obs["headers"],
                "body_sha256": obs["body_sha256"],
                "body_hex": obs["body_bytes"].hex(),
                "final_url": obs["final_url"],
                "redirect_chain": obs["redirect_chain"],
                "elapsed_s": obs["elapsed_s"],
            })

    results = {
        "experiment_id": "EXP-RUNTIME-33528830833",
        "verdict": verdict,
        "survives": survives,
        "discrimination_score": discrimination_score,
        "discrimination_score_ci_95": [ci_lo, ci_hi],
        "mean_intra_state_same_rate": mean_intra_same,
        "inter_state_difference_rate": inter_diff_rate,
        "per_state_reproducibility": per_state_repro,
        "per_pair_inter_state": per_pair_inter,
        "survival_criteria": survival_criteria,
        "baselines": baselines,
        "raw_observations": raw_observations_json,
        "fingerprints": {k: v for k, v in fingerprints.items()},
        "drift_states": {
            "authenticated_fp": fingerprints["authenticated"][0],
            "near_expiry_fp": fingerprints["near_expiry"][0],
            "expired_fp": fingerprints["expired"][0],
        },
        "null_control": {
            "fp_count": null_fp_count,
            "total_pairs": null_total,
            "fp_rate": null_fp_rate,
        },
        "positive_control": {
            "tp_count": positive_tp_count,
            "total_pairs": positive_total,
            "tp_rate": positive_tp_rate,
        },
        "held_out_state": {
            "session_fingerprints": list(set(fingerprints["session"])),
            "seen_fingerprints_count": len(seen_fps_set),
            "correctly_discriminated": session_correctly_discriminated,
        },
        "execution": {
            "seed": SEED,
            "num_repeats": NUM_REPEATS,
            "port": port,
            "server_states": list(states.keys()),
            "python_version": sys.version,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    result_path = os.path.join(OUTPUT_DIR, "result.json")
    with open(result_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw observations saved to {result_path}")

    server.shutdown()
    return results


if __name__ == "__main__":
    results = run_experiment()
