#!/usr/bin/env python3
"""
EXP-RUNTIME-34015740602 — Production-Like OAuth Middleware HTTP Observation
=========================================================================
Tests whether the HTTP fingerprint substrate maintains discrimination > 0.5
on a production-like OAuth middleware with realistic response variation:
cache-Control, ETag, X-Request-Id, Set-Cookie.

Frozen from spec.json and prereg.md — DO NOT MODIFY.
"""

import hashlib
import json
import os
import random
import sys
import threading
import time
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

import flask
import jwt
import requests

# ---------------------------------------------------------------------------
# FROZEN CONSTANTS
# ---------------------------------------------------------------------------

SECRET_KEY = "test-secret-key-12345"
BASE_URL = "http://127.0.0.1:{port}/api/userinfo"
REPS = 10
SEED = 44
JITTER_MIN = 0.05
JITTER_MAX = 0.15


# ---------------------------------------------------------------------------
# TOKEN GENERATION
# ---------------------------------------------------------------------------

def make_valid_token() -> str:
    """Generate a valid JWT: sub=alice, exp=now+1h, HS256."""
    now = datetime.utcnow()
    payload = {
        "sub": "alice",
        "name": "Alice",
        "email": "alice@example.com",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=1)).timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def make_expired_token() -> str:
    """Generate an expired JWT: sub=alice, exp=1h ago, HS256."""
    now = datetime.utcnow()
    payload = {
        "sub": "alice",
        "name": "Alice",
        "email": "alice@example.com",
        "iat": int((now - timedelta(hours=2)).timestamp()),
        "exp": int((now - timedelta(hours=1)).timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def make_invalid_token() -> str:
    """Generate a malformed token string that fails PyJWT validation."""
    return "not-a-real-jwt-token"


# ---------------------------------------------------------------------------
# AUTH STATE DEFINITIONS (frozen)
# ---------------------------------------------------------------------------

VALID_TOKEN_STR = make_valid_token()
EXPIRED_TOKEN_STR = make_expired_token()
INVALID_TOKEN_STR = make_invalid_token()

# Response bodies for each auth state (frozen)
BODIES = {
    "no_auth": {"error": "login_required", "message": "Authentication required"},
    "valid_token": {
        "sub": "alice",
        "name": "Alice",
        "email": "alice@example.com",
        "iat": int(datetime.utcnow().timestamp()),
        "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp()),
    },
    "expired_token": {"error": "token_expired", "message": "Token has expired"},
    "invalid_token": {"error": "invalid_token", "message": "Token validation failed"},
}

AUTH_STATES = {
    "no_auth": {
        "auth_header": None,
        "expected_status": 401,
        "cache_control": "no-cache",
        "set_cookie": False,
    },
    "valid_token": {
        "auth_header": f"Bearer {VALID_TOKEN_STR}",
        "expected_status": 200,
        "cache_control": "no-store",
        "set_cookie": True,
    },
    "expired_token": {
        "auth_header": f"Bearer {EXPIRED_TOKEN_STR}",
        "expected_status": 401,
        "cache_control": "no-cache",
        "set_cookie": False,
    },
    "invalid_token": {
        "auth_header": f"Bearer {INVALID_TOKEN_STR}",
        "expected_status": 401,
        "cache_control": "no-cache",
        "set_cookie": False,
    },
}


# ---------------------------------------------------------------------------
# FLASK APP with OAuth-like middleware + production-realistic headers
# ---------------------------------------------------------------------------

app = flask.Flask(__name__)
app.logger.setLevel("WARNING")


@app.route("/api/userinfo", methods=["GET"])
def get_userinfo():
    """OAuth2-like token introspection middleware.
    Returns 200 for valid tokens, 401 otherwise.
    Production-realistic headers: cache-Control, ETag, Set-Cookie, X-Request-Id.
    expired and invalid return DIFFERENT response bodies (frozen design)."""
    # Server-side jitter
    time.sleep(random.uniform(JITTER_MIN, JITTER_MAX))

    # X-Request-Id: UUID per request (volatile, EXCLUDED from fingerprint)
    request_id = str(uuid.uuid4())

    auth_header = flask.request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        # no_auth state
        body_dict = BODIES["no_auth"]
        body_json = flask.json.dumps(body_dict, separators=(",", ":"))
        body_bytes = body_json.encode("utf-8")
        body_sha = hashlib.sha256(body_bytes).hexdigest()
        etag = f'W/"{body_sha}"'

        resp = flask.Response(body_bytes, status=401, mimetype="application/json")
        resp.headers["Cache-Control"] = "no-cache"
        resp.headers["ETag"] = etag
        resp.headers["X-Request-Id"] = request_id
        return resp

    token = auth_header[7:]  # Remove "Bearer "

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # valid_token state: 200 with user profile body
        body_dict = BODIES["valid_token"]
        # Update iat/exp to match actual token
        body_dict["iat"] = payload.get("iat", int(datetime.utcnow().timestamp()))
        body_dict["exp"] = payload.get("exp", int((datetime.utcnow() + timedelta(hours=1)).timestamp()))
        body_json = flask.json.dumps(body_dict, separators=(",", ":"))
        body_bytes = body_json.encode("utf-8")
        body_sha = hashlib.sha256(body_bytes).hexdigest()
        etag = f'W/"{body_sha}"'

        resp = flask.Response(body_bytes, status=200, mimetype="application/json")
        resp.headers["Cache-Control"] = "no-store"
        resp.headers["ETag"] = etag
        resp.headers["X-Request-Id"] = request_id
        resp.headers["Set-Cookie"] = f"session={token}; Path=/; HttpOnly"
        return resp
    except jwt.ExpiredSignatureError:
        # expired_token state: 401 with DISTINCT body
        body_dict = BODIES["expired_token"]
        body_json = flask.json.dumps(body_dict, separators=(",", ":"))
        body_bytes = body_json.encode("utf-8")
        body_sha = hashlib.sha256(body_bytes).hexdigest()
        etag = f'W/"{body_sha}"'

        resp = flask.Response(body_bytes, status=401, mimetype="application/json")
        resp.headers["Cache-Control"] = "no-cache"
        resp.headers["ETag"] = etag
        resp.headers["X-Request-Id"] = request_id
        return resp
    except jwt.InvalidTokenError:
        # invalid_token state: 401 with DISTINCT body
        body_dict = BODIES["invalid_token"]
        body_json = flask.json.dumps(body_dict, separators=(",", ":"))
        body_bytes = body_json.encode("utf-8")
        body_sha = hashlib.sha256(body_bytes).hexdigest()
        etag = f'W/"{body_sha}"'

        resp = flask.Response(body_bytes, status=401, mimetype="application/json")
        resp.headers["Cache-Control"] = "no-cache"
        resp.headers["ETag"] = etag
        resp.headers["X-Request-Id"] = request_id
        return resp


# ---------------------------------------------------------------------------
# HTTP OBSERVATION CLIENT (requests library)
# ---------------------------------------------------------------------------

def make_request(url: str, auth_header: str = None, timeout: int = 10) -> dict:
    """Execute HTTP request, capture raw observation."""
    headers = {}
    if auth_header:
        headers["Authorization"] = auth_header

    start = time.monotonic()
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        elapsed = time.monotonic() - start
        status = resp.status_code
        resp_headers = dict(resp.headers)
        body = resp.content
        redirect_url = resp.url if resp.url != url else None
    except requests.exceptions.HTTPError as e:
        elapsed = time.monotonic() - start
        status = e.response.status_code if e.response is not None else 0
        resp_headers = dict(e.response.headers) if e.response is not None and e.response.headers else {}
        body = e.response.content if e.response is not None and e.response.content else b""
        redirect_url = None
    except Exception as e:
        elapsed = time.monotonic() - start
        status = 0
        resp_headers = {}
        body = str(e).encode("utf-8")
        redirect_url = None

    return {
        "url": url,
        "status": status,
        "headers": resp_headers,
        "body": body,
        "redirect_url": redirect_url,
        "elapsed": elapsed,
        "timestamp": time.time(),
    }


# ---------------------------------------------------------------------------
# FINGERPRINT (deterministic sorted-tuple, excluding Date/Server/X-Request-Id)
# ---------------------------------------------------------------------------

def fingerprint(observation: dict) -> str:
    """
    Deterministic fingerprint: SHA-256 of sorted-tuple vector.
    Excludes Date, Server, and X-Request-Id (volatile per-request UUID).
    Inherited from parent with X-Request-Id exclusion added.
    """
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
    redirect_chain = observation.get("redirect_url") or ""
    # Exclude Date, Server (volatile), and X-Request-Id (per-request UUID)
    excluded = {"date", "server", "x-request-id"}
    headers_filtered = {k: v for k, v in observation["headers"].items()
                        if k.lower() not in excluded}
    vector = (
        observation["status"],
        tuple(sorted(headers_filtered.items())),
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

def compute_discrimination_score(fingerprints_by_state: dict) -> dict:
    """
    Compute discrimination score and per-pair statistics.
    discrimination = intra_match_rate - inter_match_rate.
    Range: [-1, 1]. Perfect discrimination = 1. No discrimination = 0.
    """
    all_states = list(fingerprints_by_state.keys())

    intra_matches = 0
    intra_total = 0
    inter_matches = 0
    inter_total = 0
    intra_jaccards = []
    inter_jaccards = []

    for i, s1 in enumerate(all_states):
        fps1 = fingerprints_by_state[s1]
        for a in range(len(fps1)):
            for b in range(a + 1, len(fps1)):
                intra_total += 1
                if fps1[a] == fps1[b]:
                    intra_matches += 1
                intra_jaccards.append(jaccard_similarity(fps1[a], fps1[b]))
        for j, s2 in enumerate(all_states):
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


def bootstrap_ci_discrimination(
    fingerprints_by_state: dict,
    n_bootstrap: int = 1000,
    ci: float = 0.95,
    seed: int = 42,
) -> dict:
    """Bootstrap CI for discrimination score via state resampling."""
    rng = random.Random(seed)
    all_states = list(fingerprints_by_state.keys())

    scores = []
    for _ in range(n_bootstrap):
        sampled = [rng.choice(all_states) for _ in all_states]
        ds = compute_discrimination_score(
            {s: fingerprints_by_state[s] for s in set(sampled)}
        )
        scores.append(ds["discrimination_score"])

    scores.sort()
    alpha = (1 - ci) / 2
    lo = scores[int(alpha * n_bootstrap)]
    hi = scores[int((1 - alpha) * n_bootstrap)]
    mean = sum(scores) / len(scores)
    return {"mean": mean, "lower": lo, "upper": hi, "n_bootstrap": n_bootstrap}


# ---------------------------------------------------------------------------
# BASELINES
# ---------------------------------------------------------------------------

def baseline_url_hash(url: str, n: int = 10) -> list:
    """B-URL-HASH: fingerprint is hash of URL only."""
    return [hashlib.sha256(url.encode()).hexdigest() for _ in range(n)]


def baseline_random(n: int = 10, seed: int = 99) -> list:
    """B-RANDOM: random 256-bit fingerprints."""
    rng = random.Random(seed)
    return [hashlib.sha256(rng.getrandbits(256).to_bytes(32, "big")).hexdigest() for _ in range(n)]


def baseline_status_only(status: int, n: int = 10) -> list:
    """B-STATUS-ONLY: fingerprint from status code only."""
    return [hashlib.sha256(str(status).encode()).hexdigest() for _ in range(n)]


def baseline_body_only(body: bytes, n: int = 10) -> list:
    """B-BODY-ONLY: fingerprint from response body only."""
    return [hashlib.sha256(body).hexdigest() for _ in range(n)]


# ---------------------------------------------------------------------------
# MAIN EXPERIMENT
# ---------------------------------------------------------------------------

def run_experiment():
    """Run the full experiment on production-like OAuth middleware server."""
    PORT = 18928  # different from parent to avoid port collision

    # Start Flask server in background thread
    print("Starting production-like OAuth middleware server...")
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False),
        daemon=True,
    )
    server_thread.start()
    time.sleep(1.5)  # let Flask bind

    base_url = BASE_URL.format(port=PORT)
    print(f"Server started on port {PORT}")

    # Build experiment plan: 4 states x 10 reps, randomized
    rng = random.Random(SEED)
    plan = []
    for state_name in AUTH_STATES:
        for rep in range(REPS):
            plan.append((state_name, rep))
    rng.shuffle(plan)

    raw_observations = defaultdict(list)
    fingerprints_by_state = defaultdict(list)
    errors = []

    print(f"\n=== Experiment: Production-Like OAuth Middleware ===")
    print(f"States: {list(AUTH_STATES.keys())}")
    print(f"Reps per state: {REPS}")
    print(f"Total requests: {len(plan)}")
    print(f"Seed: {SEED}")
    print()

    # Execute all requests
    for i, (state_name, rep) in enumerate(plan):
        cfg = AUTH_STATES[state_name]
        try:
            obs = make_request(base_url, auth_header=cfg["auth_header"])
            obs["state"] = state_name
            obs["rep"] = rep
            obs["fingerprint"] = fingerprint(obs)

            # Validate expected status
            if obs["status"] != cfg["expected_status"]:
                errors.append({
                    "state": state_name,
                    "rep": rep,
                    "error": f"Expected status {cfg['expected_status']}, got {obs['status']}",
                })

            raw_observations[state_name].append(obs)
            fingerprints_by_state[state_name].append(obs["fingerprint"])

        except Exception as e:
            errors.append({
                "state": state_name,
                "rep": rep,
                "error": str(e),
            })

        # Inter-request jitter: 0-200ms
        if i < len(plan) - 1:
            jitter = rng.uniform(0, 0.2)
            time.sleep(jitter)

    # Check validity
    total_requests = len(plan)
    error_rate = len(errors) / total_requests if total_requests > 0 else 0
    measurement_valid = error_rate <= 0.20

    if not measurement_valid:
        print(f"\nMEASUREMENT_INVALID: error rate {error_rate:.1%} > 20%")
        return {
            "schema_version": 1,
            "experiment_id": "EXP-RUNTIME-34015740602",
            "lane": "runtime",
            "status": "MEASUREMENT_INVALID",
            "outcome": "NOT_APPLICABLE",
            "metrics": {},
            "controls": {},
            "artifacts": [],
            "observations": [f"Flask server error rate {error_rate:.1%} > 20% threshold"],
            "validity_notes": [f"Measurement invalid: {len(errors)} errors out of {total_requests} requests"],
            "unresolved": [],
        }

    # Compute discrimination score (full vector)
    disc = compute_discrimination_score(fingerprints_by_state)
    boot = bootstrap_ci_discrimination(fingerprints_by_state, seed=42)

    print(f"\n--- Full Vector Results ---")
    print(f"Discrimination: {disc['discrimination_score']:.6f}")
    print(f"Intra match rate: {disc['intra_match_rate']:.6f}")
    print(f"Inter match rate: {disc['inter_match_rate']:.6f}")
    print(f"Bootstrap 95% CI: [{boot['lower']:.6f}, {boot['upper']:.6f}]")
    print()

    # Compute baselines
    baselines = {}

    # B-URL-HASH: URL is constant, expected 0.0
    b_url_fps = baseline_url_hash(base_url, n=REPS)
    b_url_by_state = {s: b_url_fps for s in AUTH_STATES}
    b_url_disc = compute_discrimination_score(b_url_by_state)
    baselines["B-URL-HASH"] = {"discrimination_score": b_url_disc["discrimination_score"]}
    print(f"B-URL-HASH discrimination: {b_url_disc['discrimination_score']:.6f}")

    # B-RANDOM: expected ~0.0
    b_rand_fps = baseline_random(n=REPS * len(AUTH_STATES))
    b_rand_by_state = {}
    idx = 0
    for s in AUTH_STATES:
        b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
        idx += REPS
    b_rand_disc = compute_discrimination_score(b_rand_by_state)
    baselines["B-RANDOM"] = {"discrimination_score": b_rand_disc["discrimination_score"]}
    print(f"B-RANDOM discrimination: {b_rand_disc['discrimination_score']:.6f}")

    # B-STATUS-ONLY: 3 states share status 401, expected low
    b_status_by_state = {}
    for state, obs_list in raw_observations.items():
        fps = [hashlib.sha256(str(obs["status"]).encode()).hexdigest() for obs in obs_list]
        b_status_by_state[state] = fps
    b_status_disc = compute_discrimination_score(b_status_by_state)
    baselines["B-STATUS-ONLY"] = {"discrimination_score": b_status_disc["discrimination_score"]}
    print(f"B-STATUS-ONLY discrimination: {b_status_disc['discrimination_score']:.6f}")

    # B-BODY-ONLY: all 4 states have distinct bodies, expected high
    b_body_by_state = {}
    for state, obs_list in raw_observations.items():
        fps = [hashlib.sha256(obs["body"]).hexdigest() for obs in obs_list]
        b_body_by_state[state] = fps
    b_body_disc = compute_discrimination_score(b_body_by_state)
    baselines["B-BODY-ONLY"] = {"discrimination_score": b_body_disc["discrimination_score"]}
    print(f"B-BODY-ONLY discrimination: {b_body_disc['discrimination_score']:.6f}")
    print()

    # --- Controls ---

    # Null control: FP rate under server-side jitter
    # Same auth state repeated -> should get same fingerprint
    null_results = {}
    for state in AUTH_STATES:
        fps = fingerprints_by_state[state]
        unique = len(set(fps))
        total = len(fps)
        fp_rate = (unique - 1) / (total - 1) if total > 1 else 0.0
        null_results[state] = {
            "total": total,
            "unique": unique,
            "false_positive_rate": fp_rate,
        }

    # Overall FP rate
    total_pairs = sum(max(r["total"] * (r["total"] - 1) // 2, 0) for r in null_results.values())
    total_diff_pairs = sum(
        max((r["unique"] - 1) * r["total"] // 2, 0) for r in null_results.values()
    ) if total_pairs > 0 else 0
    overall_fp_rate = total_diff_pairs / total_pairs if total_pairs > 0 else 0

    null_control_pass = overall_fp_rate < 0.05

    print(f"--- Null Control (Server-Jitter) ---")
    print(f"Overall FP rate: {overall_fp_rate:.1%} (threshold: < 5%)")
    print(f"Per-state:")
    for state, r in null_results.items():
        print(f"  {state}: {r['unique']}/{r['total']} unique, FP={r['false_positive_rate']:.1%}")
    print(f"PASS: {null_control_pass}")
    print()

    # Positive control: full-vector discrimination > 0.5
    positive_control_pass = disc["discrimination_score"] > 0.5

    print(f"--- Positive Control ---")
    print(f"Full-vector discrimination: {disc['discrimination_score']:.6f} (threshold: > 0.5)")
    print(f"PASS: {positive_control_pass}")
    print()

    # Baseline superiority: full vector > B-STATUS-ONLY
    baseline_status_superiority_pass = disc["discrimination_score"] > b_status_disc["discrimination_score"]

    print(f"--- Baseline Superiority: Full vs B-STATUS-ONLY ---")
    print(f"B-STATUS-ONLY: {b_status_disc['discrimination_score']:.6f}")
    print(f"Full-vector: {disc['discrimination_score']:.6f}")
    print(f"Full vector exceeds B-STATUS-ONLY: {baseline_status_superiority_pass}")
    print()

    # Body-only comparison: full vector vs B-BODY-ONLY
    # Key exploratory test: does full vector > B-BODY-ONLY when headers vary?
    body_only_ratio = disc["discrimination_score"] / b_body_disc["discrimination_score"] if b_body_disc["discrimination_score"] > 0 else float('inf')

    print(f"--- Baseline Comparison: Full vs B-BODY-ONLY (EXPLORATORY) ---")
    print(f"B-BODY-ONLY: {b_body_disc['discrimination_score']:.6f}")
    print(f"Full-vector: {disc['discrimination_score']:.6f}")
    print(f"Ratio (full/body): {body_only_ratio:.6f}")
    if disc["discrimination_score"] > b_body_disc["discrimination_score"]:
        print(f"Full vector EXCEEDS B-BODY-ONLY: headers add independent information")
    elif disc["discrimination_score"] == b_body_disc["discrimination_score"]:
        print(f"Full vector EQUALS B-BODY-ONLY: body is dominant signal")
    else:
        print(f"Full vector is LESS THAN B-BODY-ONLY: headers introduce noise")
    print()

    # Drift control: consecutive pairs discriminable (Jaccard < 0.5)
    drift_states = ["valid_token", "expired_token", "invalid_token"]
    drift_jaccards = []
    for i in range(len(drift_states) - 1):
        s1, s2 = drift_states[i], drift_states[i + 1]
        fps1 = fingerprints_by_state[s1]
        fps2 = fingerprints_by_state[s2]
        sims = [jaccard_similarity(f1, f2) for f1 in fps1 for f2 in fps2]
        mean_sim = sum(sims) / len(sims) if sims else 0
        drift_jaccards.append(mean_sim)

    drift_all_discriminable = all(j < 0.5 for j in drift_jaccards)

    print(f"--- Drift Control ---")
    for i in range(len(drift_states) - 1):
        print(f"  {drift_states[i]} -> {drift_states[i+1]}: Jaccard={drift_jaccards[i]:.4f}")
    print(f"All discriminable (<0.5): {drift_all_discriminable}")
    print()

    # --- Decision Rule ---
    # SURVIVES if ALL of:
    # 1. Full-vector discrimination > 0.5
    # 2. Null control FP rate < 5%
    # 3. valid_token vs expired_token drift pair discriminable (Jaccard < 0.5)
    # Note: expired_token vs invalid_token now has DIFFERENT bodies (may be discriminable)

    valid_expired_jaccard = drift_jaccards[0] if len(drift_jaccards) > 0 else 1.0
    expired_invalid_jaccard = drift_jaccards[1] if len(drift_jaccards) > 1 else 1.0
    valid_expired_discriminable = valid_expired_jaccard < 0.5

    survives = (
        positive_control_pass
        and null_control_pass
        and valid_expired_discriminable
        and len(errors) == 0
    )

    if survives:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif disc["discrimination_score"] <= 0.5:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not null_control_pass:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not valid_expired_discriminable:
        outcome = "MIXED"
        status = "COMPLETE"
    else:
        outcome = "FALSIFIES"
        status = "COMPLETE"

    print(f"\n=== FINAL VERDICT ===")
    print(f"Status: {status}")
    print(f"Outcome: {outcome}")
    print(f"Survives: {survives}")

    # Build controls object with stable IDs
    controls = {
        "C_NULL_FP_RATE": {
            "expected": "< 5%",
            "observed": f"{overall_fp_rate:.1%}",
            "pass": null_control_pass,
            "detail": null_results,
        },
        "C_POSITIVE_DISCRIMINATION": {
            "expected": "> 0.5",
            "observed": f"{disc['discrimination_score']:.6f}",
            "pass": positive_control_pass,
        },
        "C_BASELINE_STATUS_SUPERIORITY": {
            "expected": "full-vector > B-STATUS-ONLY",
            "observed": f"B-STATUS-ONLY={b_status_disc['discrimination_score']:.6f}, full={disc['discrimination_score']:.6f}",
            "pass": baseline_status_superiority_pass,
        },
        "C_DRIFT_VALID_VS_EXPIRED": {
            "expected": "Jaccard < 0.5 (discriminable)",
            "observed": f"Jaccard={valid_expired_jaccard:.4f}",
            "pass": valid_expired_discriminable,
        },
        "C_DRIFT_EXPIRED_VS_INVALID": {
            "expected": "Jaccard < 0.5 (discriminable — DIFFERENT bodies unlike parent)",
            "observed": f"Jaccard={expired_invalid_jaccard:.4f}",
            "pass": expired_invalid_jaccard < 0.5,  # discriminable because bodies differ
        },
        "C_ERROR_RATE": {
            "expected": "< 20%",
            "observed": f"{error_rate:.1%}",
            "pass": error_rate <= 0.20,
        },
    }

    # Build metrics object
    metrics = {
        "full_vector_discrimination": disc["discrimination_score"],
        "full_vector_intra_match_rate": disc["intra_match_rate"],
        "full_vector_inter_match_rate": disc["inter_match_rate"],
        "full_vector_mean_intra_jaccard": disc["mean_intra_jaccard"],
        "full_vector_mean_inter_jaccard": disc["mean_inter_jaccard"],
        "full_vector_bootstrap_95ci": [boot["lower"], boot["upper"]],
        "baselines": {k: v["discrimination_score"] for k, v in baselines.items()},
        "full_vs_body_only_ratio": body_only_ratio,
        "null_fp_rate": overall_fp_rate,
        "drift_jaccards": drift_jaccards,
        "drift_all_discriminable": drift_all_discriminable,
        "total_requests": total_requests,
        "error_rate": error_rate,
    }

    # Observations (direct observations, not interpretations)
    observations = [
        f"Production-like OAuth middleware server started on port {PORT} with PyJWT HS256 validation",
        f"4 auth states x {REPS} reps = {total_requests} requests completed",
        f"Server-side jitter: 50-150ms random processing delay per request",
        f"Client-side jitter: 0-200ms inter-request delay (seed={SEED})",
        f"Production-realistic headers: cache-Control (varies by state), ETag (body-dependent), X-Request-Id (UUID per request, EXCLUDED from fingerprint), Set-Cookie (valid_token only)",
        f"expired_token and invalid_token return DIFFERENT response bodies (unlike parent Flask/JWT experiment)",
        f"X-Request-Id excluded from fingerprint (volatile per-request UUID)",
        f"Full-vector discrimination: {disc['discrimination_score']:.6f} (threshold: > 0.5)",
        f"Full-vector bootstrap 95% CI: [{boot['lower']:.6f}, {boot['upper']:.6f}]",
        f"B-STATUS-ONLY discrimination: {b_status_disc['discrimination_score']:.6f} (3 states share status 401)",
        f"B-BODY-ONLY discrimination: {b_body_disc['discrimination_score']:.6f} (all 4 states have distinct bodies)",
        f"B-URL-HASH discrimination: {b_url_disc['discrimination_score']:.6f} (URL is constant)",
        f"Null FP rate under server-side jitter: {overall_fp_rate:.1%} (threshold: < 5%)",
        f"valid_token vs expired_token drift Jaccard: {valid_expired_jaccard:.4f} (threshold: < 0.5)",
        f"expired_token vs invalid_token drift Jaccard: {expired_invalid_jaccard:.4f} (bodies differ, expected < 0.5)",
        f"Full vs B-BODY-ONLY ratio: {body_only_ratio:.6f}",
    ]

    # Validity notes
    validity_notes = [
        "Server is Flask 3.1.3 with PyJWT 2.13.0 HS256 validation — real JWT middleware with production-like headers.",
        "Fingerprint uses repr(vector) with tuple(sorted(...)) — deterministic within same Python version but Python-version-dependent.",
        "Date and Server headers excluded from fingerprint vector to prevent spurious variance.",
        "X-Request-Id (UUID per request) excluded from fingerprint — volatile per-request identifier, not state-discriminative.",
        "cache-Control varies by auth state: no-store for valid_token, no-cache for errors — production-realistic pattern.",
        "ETag is body-dependent (W/\"<body_sha256>\") — correlated with body_hash, adds no independent information.",
        "Set-Cookie present only for valid_token — binary header signal varying with auth state.",
        "expired_token and invalid_token return DISTINCT response bodies (unlike parent Flask/JWT where they were identical).",
        "Server-side jitter 50-150ms tests timing invariance when timing is excluded from fingerprint.",
        f"Python version: {sys.version}",
        f"Error rate: {error_rate:.1%} ({len(errors)} errors out of {total_requests} requests)",
        "Sample size: 40 requests (4 states x 10 reps) — limited statistical power for subtle discrimination differences.",
    ]

    # Unresolved
    unresolved = [
        "Does the substrate maintain discrimination on real production OAuth/OIDC providers (Auth0, Okta, Keycloak) with CDN, load-balancer variance, and compressed encoding?",
        "What is the false-positive rate under server-side processing jitter >150ms or volatile standard headers beyond X-Request-Id?",
        "Does full vector exceed B-BODY-ONLY when Set-Cookie and cache-Control vary with auth state on real production providers?",
        "Can substrate detect continuous session drift as a continuous signal rather than discrete state classification?",
        "What is cross-Python-version reproducibility of repr(vector) hashes?",
    ]

    # Save raw observations (relative to experiment directory)
    raw_obs_path = "raw_observations.json"
    raw_obs_serializable = {}
    for state, obs_list in raw_observations.items():
        raw_obs_serializable[state] = []
        for obs in obs_list:
            raw_obs_serializable[state].append({
                "url": obs["url"],
                "status": obs["status"],
                "headers": obs["headers"],
                "body_hash": hashlib.sha256(obs["body"]).hexdigest(),
                "body_preview": obs["body"][:200].decode("utf-8", errors="replace"),
                "fingerprint": obs["fingerprint"],
                "elapsed": obs["elapsed"],
                "timestamp": obs["timestamp"],
                "state": obs["state"],
                "rep": obs["rep"],
            })

    with open(raw_obs_path, "w") as f:
        json.dump(raw_obs_serializable, f, indent=2)

    print(f"\nRaw observations saved to {raw_obs_path}")

    return {
        "schema_version": 1,
        "experiment_id": "EXP-RUNTIME-34015740602",
        "lane": "runtime",
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
        "artifacts": [
            {"path": raw_obs_path, "role": "raw"},
        ],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }


if __name__ == "__main__":
    result = run_experiment()

    # Write result.json (relative to experiment directory)
    result_path = "result.json"
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nResult written to {result_path}")
