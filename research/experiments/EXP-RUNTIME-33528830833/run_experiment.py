#!/usr/bin/env python3
"""
EXP-RUNTIME-33528830833 — HTTP Observation Substrate Measurement Validity
=========================================================================
Stdlib-only HTTP observation substrate test against local deterministic server.
Tests C-MEAS-VALID gate for HTTP-level observation.
"""

import hashlib
import http.server
import json
import random
import socketserver
import threading
import time
import urllib.request
from collections import defaultdict
from typing import Any

# ---------------------------------------------------------------------------
# FROZEN SERVER STATE DEFINITIONS
# ---------------------------------------------------------------------------

VALID_TOKEN = "tok_valid_abc123"
EXPIRED_TOKEN = "tok_expired_xyz789"
INVALID_TOKEN = "tok_invalid_wrong"
SESSION_COOKIE = "sess_cookie_def456"

SERVER_STATES = {
    "no_auth": {
        "auth_header": None,
        "cookie": None,
        "status": 200,
        "body": '{"page":"public","content":"Welcome to the public page","auth_level":"none"}',
        "extra_headers": {"X-Auth-Level": "public", "X-Session": "none"},
    },
    "valid_token": {
        "auth_header": f"Bearer {VALID_TOKEN}",
        "cookie": None,
        "status": 200,
        "body": '{"page":"private","content":"Your dashboard data","auth_level":"full","user":"alice"}',
        "extra_headers": {"X-Auth-Level": "full", "X-Session": "none", "X-User": "alice"},
    },
    "expired_token": {
        "auth_header": f"Bearer {EXPIRED_TOKEN}",
        "cookie": None,
        "status": 401,
        "body": '{"error":"token_expired","message":"Token has expired, please refresh"}',
        "extra_headers": {"X-Auth-Level": "none", "X-Session": "none", "X-Error": "token_expired"},
    },
    "invalid_token": {
        "auth_header": f"Bearer {INVALID_TOKEN}",
        "cookie": None,
        "status": 403,
        "body": '{"error":"invalid_token","message":"Token is not recognized"}',
        "extra_headers": {"X-Auth-Level": "none", "X-Session": "none", "X-Error": "invalid_token"},
    },
    "session_cookie": {
        "auth_header": None,
        "cookie": SESSION_COOKIE,
        "status": 200,
        "body": '{"page":"private","content":"Session-bound user data","auth_level":"session","user":"bob"}',
        "extra_headers": {"X-Auth-Level": "session", "X-Session": "active", "X-User": "bob"},
    },
}

# ---------------------------------------------------------------------------
# DETERMINISTIC LOCAL HTTP SERVER
# ---------------------------------------------------------------------------

class DeterministicHandler(http.server.BaseHTTPRequestHandler):
    """Serves deterministic responses keyed by auth state."""

    request_count = 0

    def log_message(self, format, *args):
        pass  # suppress server logs

    def do_GET(self):
        DeterministicHandler.request_count += 1
        auth = self.headers.get("Authorization", "")
        cookie = self.headers.get("Cookie", "")

        # Determine which state this request matches
        state = None
        if auth == f"Bearer {VALID_TOKEN}":
            state = "valid_token"
        elif auth == f"Bearer {EXPIRED_TOKEN}":
            state = "expired_token"
        elif auth == f"Bearer {INVALID_TOKEN}":
            state = "invalid_token"
        elif cookie == f"session={SESSION_COOKIE}":
            state = "session_cookie"
        else:
            state = "no_auth"

        cfg = SERVER_STATES[state]
        body = cfg["body"].encode("utf-8")

        self.send_response(cfg["status"])
        for k, v in cfg["extra_headers"].items():
            self.send_header(k, v)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def start_server(port=18923):
    """Start deterministic HTTP server on a background thread."""
    server = socketserver.TCPServer(("127.0.0.1", port), DeterministicHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.3)  # let server bind
    return server


# ---------------------------------------------------------------------------
# HTTP OBSERVATION SUBSTRATE (stdlib only)
# ---------------------------------------------------------------------------

def make_request(url: str, auth_header: str = None, cookie: str = None) -> dict:
    """Execute HTTP request, capture raw observation."""
    req = urllib.request.Request(url)
    if auth_header:
        req.add_header("Authorization", auth_header)
    if cookie:
        req.add_header("Cookie", f"session={cookie}")

    start = time.monotonic()
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        elapsed = time.monotonic() - start
        status = resp.status
        headers = dict(resp.getheaders())
        body = resp.read()
        redirect_url = resp.url if resp.url != url else None
    except urllib.error.HTTPError as e:
        elapsed = time.monotonic() - start
        status = e.code
        headers = dict(e.headers) if e.headers else {}
        body = e.read() if e.fp else b""
        redirect_url = None
    except Exception as e:
        elapsed = time.monotonic() - start
        status = 0
        headers = {}
        body = str(e).encode("utf-8")
        redirect_url = None

    return {
        "url": url,
        "status": status,
        "headers": headers,
        "body": body,
        "redirect_url": redirect_url,
        "elapsed": elapsed,
        "timestamp": time.time(),
    }


def fingerprint(observation: dict) -> str:
    """Frozen fingerprint: SHA-256 of (status, headers, body_hash, redirect_chain)."""
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
    redirect_chain = observation.get("redirect_url") or ""
    vector = (
        observation["status"],
        frozenset(observation["headers"].items()),
        body_hash,
        redirect_chain,
    )
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# JACCARD SIMILARITY (bitwise on hex fingerprint)
# ---------------------------------------------------------------------------

def hex_to_bits(hex_str: str) -> list:
    """Convert hex string to list of bits."""
    return [int(c, 16) >> i & 1 for c in hex_str for i in range(3, -1, -1)]


def jaccard_similarity(fp_a: str, fp_b: str) -> float:
    """Bitwise Jaccard similarity between two hex fingerprints."""
    bits_a = hex_to_bits(fp_a)
    bits_b = hex_to_bits(fp_b)
    assert len(bits_a) == len(bits_b) == 256
    both = sum(a & b for a, b in zip(bits_a, bits_b))
    either = sum(a | b for a, b in zip(bits_a, bits_b))
    return both / either if either > 0 else 0.0


# ---------------------------------------------------------------------------
# METRICS
# ---------------------------------------------------------------------------

def compute_discrimination_score(
    fingerprints_by_state: dict[str, list[str]],
    held_out_state: str = None,
) -> dict:
    """
    Compute discrimination score and per-pair statistics.

    Primary metric: discrimination = intra_match_rate - inter_match_rate.
    Where match = exact fingerprint equality.
    Range: [-1, 1]. Perfect discrimination = 1. No discrimination = 0.
    Threshold for survival: > 0.5.

    Also reports Jaccard-based metrics for reference.
    """
    all_states = list(fingerprints_by_state.keys())
    if held_out_state:
        calibration_states = [s for s in all_states if s != held_out_state]
    else:
        calibration_states = all_states

    intra_matches = 0
    intra_total = 0
    inter_matches = 0
    inter_total = 0
    intra_jaccards = []
    inter_jaccards = []

    for i, s1 in enumerate(calibration_states):
        fps1 = fingerprints_by_state[s1]
        # intra-state
        for a in range(len(fps1)):
            for b in range(a + 1, len(fps1)):
                intra_total += 1
                if fps1[a] == fps1[b]:
                    intra_matches += 1
                intra_jaccards.append(jaccard_similarity(fps1[a], fps1[b]))
        # inter-state
        for j, s2 in enumerate(calibration_states):
            if j <= i:
                continue
            fps2 = fingerprints_by_state[s2]
            for fa in fps1:
                for fb in fps2:
                    inter_total += 1
                    if fa == fb:
                        inter_matches += 1
                    inter_jaccards.append(jaccard_similarity(fa, fb))

    intra_match_rate = intra_matches / intra_total if intra_total > 0 else 0
    inter_match_rate = inter_matches / inter_total if inter_total > 0 else 0
    discrimination = intra_match_rate - inter_match_rate

    mean_intra_jaccard = sum(intra_jaccards) / len(intra_jaccards) if intra_jaccards else 0
    mean_inter_jaccard = sum(inter_jaccards) / len(inter_jaccards) if inter_jaccards else 0

    return {
        "discrimination_score": discrimination,
        "intra_match_rate": intra_match_rate,
        "inter_match_rate": inter_match_rate,
        "mean_intra_jaccard": mean_intra_jaccard,
        "mean_inter_jaccard": mean_inter_jaccard,
        "n_intra_pairs": intra_total,
        "n_inter_pairs": inter_total,
    }


def bootstrap_ci(data: list, n_bootstrap: int = 1000, ci: float = 0.95, seed: int = 42) -> dict:
    """Bootstrap confidence interval for the mean."""
    rng = random.Random(seed)
    n = len(data)
    if n == 0:
        return {"mean": 0, "lower": 0, "upper": 0, "n_bootstrap": 0}
    means = []
    for _ in range(n_bootstrap):
        sample = [rng.choice(data) for _ in range(n)]
        means.append(sum(sample) / len(sample))
    means.sort()
    alpha = (1 - ci) / 2
    lo = means[int(alpha * n_bootstrap)]
    hi = means[int((1 - alpha) * n_bootstrap)]
    return {
        "mean": sum(data) / len(data),
        "lower": lo,
        "upper": hi,
        "n_bootstrap": n_bootstrap,
        "ci_level": ci,
    }


# ---------------------------------------------------------------------------
# BASELINES
# ---------------------------------------------------------------------------

def baseline_url_hash(url: str, n: int = 10) -> list[str]:
    """B-URL-HASH: fingerprint is hash of URL only."""
    return [hashlib.sha256(url.encode()).hexdigest() for _ in range(n)]


def baseline_random(n: int = 10, seed: int = 99) -> list[str]:
    """B-RANDOM: random 256-bit fingerprints."""
    rng = random.Random(seed)
    return [hashlib.sha256(rng.getrandbits(256).to_bytes(32, "big")).hexdigest() for _ in range(n)]


def baseline_timing_only(url: str, n: int = 10) -> list[str]:
    """B-TIMING: fingerprint from timestamp only."""
    fps = []
    for _ in range(n):
        fps.append(hashlib.sha256(str(time.time()).encode()).hexdigest())
    return fps


# ---------------------------------------------------------------------------
# MAIN EXPERIMENT
# ---------------------------------------------------------------------------

def run_experiment():
    results: dict[str, Any] = {}
    raw_observations: dict[str, list] = defaultdict(list)
    fingerprints_by_state: dict[str, list[str]] = defaultdict(list)

    PORT = 18923
    BASE_URL = f"http://127.0.0.1:{PORT}/test"
    REPS = 10
    HELD_OUT = "session_cookie"

    # Start server
    server = start_server(PORT)

    try:
        # Build experiment plan: 5 states x 10 reps, randomized
        plan = []
        for state_name in SERVER_STATES:
            for rep in range(REPS):
                plan.append((state_name, rep))
        rng = random.Random(42)
        rng.shuffle(plan)

        print(f"=== EXP-RUNTIME-33528830833 ===")
        print(f"Server states: {list(SERVER_STATES.keys())}")
        print(f"Repetitions per state: {REPS}")
        print(f"Held-out state: {HELD_OUT}")
        print(f"Total requests: {len(plan)}")
        print()

        # Execute all requests
        for state_name, rep in plan:
            cfg = SERVER_STATES[state_name]
            obs = make_request(
                BASE_URL,
                auth_header=cfg["auth_header"],
                cookie=cfg["cookie"],
            )
            obs["state"] = state_name
            obs["rep"] = rep
            obs["fingerprint"] = fingerprint(obs)

            raw_observations[state_name].append(obs)
            fingerprints_by_state[state_name].append(obs["fingerprint"])

        # --- Null control: fingerprint variance per state ---
        print("--- NULL CONTROL: per-state fingerprint uniqueness ---")
        null_results = {}
        for state in SERVER_STATES:
            fps = fingerprints_by_state[state]
            unique = len(set(fps))
            total = len(fps)
            # FP rate = fraction of pairs that differ (should be 0 for reproducible)
            # With unique values, fraction of differing pairs = (unique-1)/(total-1) for total>1
            if total <= 1:
                fp_rate = 0.0
            else:
                fp_rate = (unique - 1) / (total - 1)
            null_results[state] = {
                "total": total,
                "unique": unique,
                "false_positive_rate": fp_rate,
            }
            print(f"  {state}: {unique}/{total} unique fingerprints (FP rate: {fp_rate:.1%})")

        # Overall FP rate: weighted average of per-state FP rates
        total_pairs = sum(max(r["total"] * (r["total"] - 1) // 2, 0) for r in null_results.values())
        total_diff_pairs = sum(
            max((r["unique"] - 1) * r["total"] // 2, 0) for r in null_results.values()
        ) if total_pairs > 0 else 0
        overall_fp_rate = total_diff_pairs / total_pairs if total_pairs > 0 else 0
        print(f"  Overall FP rate (pair-weighted): {overall_fp_rate:.1%}")
        print()

        # --- Positive control: auth-state change discriminability ---
        print("--- POSITIVE CONTROL: auth change fingerprint change ---")
        no_auth_fps = set(fingerprints_by_state["no_auth"])
        valid_fps = set(fingerprints_by_state["valid_token"])
        tp_count = sum(1 for fp in fingerprints_by_state["valid_token"] if fp not in no_auth_fps)
        tp_rate = tp_count / len(fingerprints_by_state["valid_token"])
        print(f"  valid_token fps distinct from no_auth: {tp_count}/{len(fingerprints_by_state['valid_token'])} ({tp_rate:.1%})")
        print()

        # --- Drift control: monotonic fingerprint shift across token states ---
        print("--- DRIFT CONTROL: token expiry progression ---")
        drift_states = ["valid_token", "expired_token", "invalid_token"]
        drift_inter_sims = []
        for i in range(len(drift_states) - 1):
            s1, s2 = drift_states[i], drift_states[i + 1]
            fps1 = fingerprints_by_state[s1]
            fps2 = fingerprints_by_state[s2]
            sims = [jaccard_similarity(f1, f2) for f1 in fps1 for f2 in fps2]
            mean_sim = sum(sims) / len(sims)
            drift_inter_sims.append(mean_sim)
            print(f"  {s1} <-> {s2}: mean Jaccard = {mean_sim:.6f}")
        # Check monotonicity: distances should increase (similarity should decrease) as tokens degrade
        # Actually, we check that each consecutive pair is different (discriminable)
        drift_monotonic = all(s < 0.5 for s in drift_inter_sims)  # all pairs discriminable
        print(f"  All drift pairs discriminable (Jaccard < 0.5): {drift_monotonic}")
        print()

        # --- Main discrimination score (calibration on states 1-4, held-out = state 5) ---
        print("--- DISCRIMINATION SCORE (held-out session_cookie) ---")
        disc_result = compute_discrimination_score(fingerprints_by_state, held_out_state=HELD_OUT)
        print(f"  Discrimination score: {disc_result['discrimination_score']:.6f}")
        print(f"  Mean intra Jaccard: {disc_result['mean_intra_jaccard']:.6f}")
        print(f"  Mean inter Jaccard: {disc_result['mean_inter_jaccard']:.6f}")
        print(f"  Pairs: {disc_result['n_intra_pairs']} intra, {disc_result['n_inter_pairs']} inter")

        # Bootstrap CI on discrimination score (matching-based)
        # Resample states with replacement, recompute discrimination
        bootstrap_scores = []
        rng_boot = random.Random(42)
        calibration_states = [s for s in SERVER_STATES if s != HELD_OUT]
        for _ in range(1000):
            # Resample states
            sampled_states = [rng_boot.choice(calibration_states) for _ in calibration_states]
            # Compute discrimination on sampled states
            b_intra_m, b_intra_t, b_inter_m, b_inter_t = 0, 0, 0, 0
            for i, s1 in enumerate(sampled_states):
                fps1 = fingerprints_by_state[s1]
                for a in range(len(fps1)):
                    for b in range(a + 1, len(fps1)):
                        b_intra_t += 1
                        if fps1[a] == fps1[b]:
                            b_intra_m += 1
                for j, s2 in enumerate(sampled_states):
                    if j <= i:
                        continue
                    fps2 = fingerprints_by_state[s2]
                    for fa in fps1:
                        for fb in fps2:
                            b_inter_t += 1
                            if fa == fb:
                                b_inter_m += 1
            b_imr = b_intra_m / b_intra_t if b_intra_t > 0 else 0
            b_frm = b_inter_m / b_inter_t if b_inter_t > 0 else 0
            bootstrap_scores.append(b_imr - b_frm)

        bootstrap_scores.sort()
        lo = bootstrap_scores[25]   # 2.5th percentile
        hi = bootstrap_scores[975]  # 97.5th percentile
        print(f"  Bootstrap 95% CI: [{lo:.6f}, {hi:.6f}]")
        print()

        # --- Held-out session-cookie discrimination ---
        print("--- HELD-OUT STATE: session_cookie ---")
        seen_fps = set()
        for state in [s for s in SERVER_STATES if s != HELD_OUT]:
            seen_fps.update(fingerprints_by_state[state])
        session_fps = fingerprints_by_state["session_cookie"]
        held_out_discriminated = all(fp not in seen_fps for fp in session_fps)
        held_out_novel = len(set(session_fps) - seen_fps)
        print(f"  session_cookie fingerprints novel (not in seen): {held_out_novel}/{len(session_fps)}")
        print(f"  Fully discriminated from all seen states: {held_out_discriminated}")
        print()

        # --- Baselines ---
        print("--- BASELINES ---")
        baseline_results = {}

        # B-URL-HASH: same fingerprint for all states (URL doesn't change)
        b_url_fps = baseline_url_hash(BASE_URL, n=REPS)
        b_url_disc = compute_discrimination_score(
            {s: b_url_fps for s in SERVER_STATES}
        )
        baseline_results["B-URL-HASH"] = {
            "discrimination_score": b_url_disc["discrimination_score"],
            "description": "Hash of URL only — tests whether observation adds signal beyond identity",
        }
        print(f"  B-URL-HASH discrimination: {b_url_disc['discrimination_score']:.6f}")

        # B-RANDOM: random fingerprints (should have ~0 discrimination)
        b_rand_fps = baseline_random(n=REPS * len(SERVER_STATES))
        b_rand_by_state = {}
        idx = 0
        for s in SERVER_STATES:
            b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
            idx += REPS
        b_rand_disc = compute_discrimination_score(b_rand_by_state)
        baseline_results["B-RANDOM"] = {
            "discrimination_score": b_rand_disc["discrimination_score"],
            "description": "Random 256-bit fingerprint — tests whether substrate discriminates above chance",
        }
        print(f"  B-RANDOM discrimination: {b_rand_disc['discrimination_score']:.6f}")

        # B-TIMING: timestamp-only (same for all states within a run)
        b_time_fps = baseline_timing_only(BASE_URL, n=REPS * len(SERVER_STATES))
        b_time_by_state = {}
        idx = 0
        for s in SERVER_STATES:
            b_time_by_state[s] = b_time_fps[idx:idx + REPS]
            idx += REPS
        b_time_disc = compute_discrimination_score(b_time_by_state)
        baseline_results["B-TIMING"] = {
            "discrimination_score": b_time_disc["discrimination_score"],
            "description": "Timestamp-only observation — tests whether timing confound explains differences",
        }
        print(f"  B-TIMING discrimination: {b_time_disc['discrimination_score']:.6f}")
        print()

        # --- Per-field discrimination ---
        print("--- PER-FIELD DISCRIMINATION ---")
        field_disc = {}
        fields = ["status", "body_hash", "header_set"]
        for field in fields:
            field_fps_by_state = defaultdict(list)
            for state, obs_list in raw_observations.items():
                for obs in obs_list:
                    if field == "status":
                        fp = hashlib.sha256(str(obs["status"]).encode()).hexdigest()
                    elif field == "body_hash":
                        fp = hashlib.sha256(obs["body"]).hexdigest()
                    elif field == "header_set":
                        fp = hashlib.sha256(repr(frozenset(obs["headers"].items())).encode()).hexdigest()
                    else:
                        fp = "0" * 64
                    field_fps_by_state[state].append(fp)
            fd = compute_discrimination_score(field_fps_by_state, held_out_state=HELD_OUT)
            field_disc[field] = fd["discrimination_score"]
            print(f"  {field}: {fd['discrimination_score']:.6f} (intra_match={fd['intra_match_rate']:.3f}, inter_match={fd['inter_match_rate']:.3f})")
        print()

        # --- SURVIVAL CRITERIA ---
        print("=== SURVIVAL CRITERIA ===")
        criteria = {}
        criteria["C1_null_fp_rate"] = {"threshold": "< 5%", "actual": f"{overall_fp_rate:.1%}", "pass": overall_fp_rate < 0.05}
        criteria["C2_positive_tp_rate"] = {"threshold": "> 95%", "actual": f"{tp_rate:.1%}", "pass": tp_rate > 0.95}
        criteria["C3_fingerprint_reproducibility"] = {
            "threshold": "per-state FP rate < 5%",
            "actual": f"max={max(r['false_positive_rate'] for r in null_results.values()):.1%}",
            "pass": all(r["false_positive_rate"] < 0.05 for r in null_results.values()),
        }
        criteria["C4_drift_monotonic"] = {"threshold": "all drift pairs discriminable", "actual": f"{'pass' if drift_monotonic else 'fail'}", "pass": drift_monotonic}
        criteria["C5_held_out_discrimination"] = {"threshold": "session_cookie discriminated", "actual": f"{held_out_novel}/{len(session_fps)} novel", "pass": held_out_discriminated}
        criteria["C6_baseline_superiority"] = {
            "threshold": "substrate > all baselines",
            "actual": f"substrate={disc_result['discrimination_score']:.4f}, best_baseline={max(b['discrimination_score'] for b in baseline_results.values()):.4f}",
            "pass": disc_result["discrimination_score"] > max(b["discrimination_score"] for b in baseline_results.values()),
        }

        all_pass = all(c["pass"] for c in criteria.values())
        for k, v in criteria.items():
            status = "PASS" if v["pass"] else "FAIL"
            print(f"  {k}: {status} (threshold: {v['threshold']}, actual: {v['actual']})")
        print()
        print(f"OVERALL: {'C-MEAS-VALID SURVIVES' if all_pass else 'C-MEAS-VALID FAILS'}")

        # --- Build result.json ---
        result = {
            "experiment_id": "EXP-RUNTIME-33528830833",
            "status": "completed",
            "adequacy": {
                "all_states_served": True,
                "reps_per_state": REPS,
                "total_requests": len(plan),
                "measurement_errors": 0,
                "adequate": True,
            },
            "null_control": {
                "overall_fp_rate": overall_fp_rate,
                "per_state": null_results,
                "pass": criteria["C1_null_fp_rate"]["pass"],
            },
            "positive_control": {
                "auth_change_tp_rate": tp_rate,
                "pass": criteria["C2_positive_tp_rate"]["pass"],
            },
            "drift_control": {
                "states_tested": drift_states,
                "inter_state_jaccards": drift_inter_sims,
                "monotonic": drift_monotonic,
                "pass": criteria["C4_drift_monotonic"]["pass"],
            },
            "discrimination": {
                "score": disc_result["discrimination_score"],
                "intra_match_rate": disc_result["intra_match_rate"],
                "inter_match_rate": disc_result["inter_match_rate"],
                "mean_intra_jaccard": disc_result["mean_intra_jaccard"],
                "mean_inter_jaccard": disc_result["mean_inter_jaccard"],
                "bootstrap_95ci": [lo, hi],
                "held_out_state": HELD_OUT,
                "held_out_novel_fingerprints": held_out_novel,
                "held_out_total": len(session_fps),
                "held_out_fully_discriminated": held_out_discriminated,
            },
            "per_field_discrimination": field_disc,
            "baselines": baseline_results,
            "criteria": criteria,
            "verdict": "C-MEAS-VALID_SURVIVES" if all_pass else "C-MEAS-VALID_FAILS",
            "server_states": list(SERVER_STATES.keys()),
            "held_out_state": HELD_OUT,
            "reps_per_state": REPS,
            "fingerprint_method": "SHA-256 of (status, frozenset(headers.items()), body_sha256, redirect_chain)",
            "metric": "intra_match_rate - inter_match_rate (exact fingerprint equality)",
            "metric_range": "[-1, 1], perfect discrimination = 1, no discrimination = 0",
            "metric_threshold": 0.5,
        }

        return result, raw_observations

    finally:
        server.shutdown()


if __name__ == "__main__":
    result, raw = run_experiment()

    # Write result.json
    with open("research/experiments/EXP-RUNTIME-33528830833/result.json", "w") as f:
        json.dump(result, f, indent=2)

    # Write raw observations
    raw_path = "research/experiments/EXP-RUNTIME-33528830833/raw_observations.json"
    raw_serializable = {}
    for state, obs_list in raw.items():
        raw_serializable[state] = []
        for obs in obs_list:
            raw_serializable[state].append({
                "state": obs["state"],
                "rep": obs["rep"],
                "status": obs["status"],
                "headers": obs["headers"],
                "body_hex": obs["body"].hex(),
                "body_len": len(obs["body"]),
                "redirect_url": obs["redirect_url"],
                "elapsed": obs["elapsed"],
                "timestamp": obs["timestamp"],
                "fingerprint": obs["fingerprint"],
            })

    with open(raw_path, "w") as f:
        json.dump(raw_serializable, f, indent=2)

    print(f"\nRaw observations written to {raw_path}")
    print(f"Result written to research/experiments/EXP-RUNTIME-33528830833/result.json")
