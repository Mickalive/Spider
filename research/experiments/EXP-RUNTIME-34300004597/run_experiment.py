#!/usr/bin/env python3
"""
EXP-RUNTIME-34300004597 — Ecological Validity on Real OAuth/OIDC Provider (Keycloak)
====================================================================================
Tests whether full vector exceeds B-BODY-ONLY on a real OAuth/OIDC identity provider
(self-hosted Keycloak) where Cache-Control and Set-Cookie patterns are determined by
the IdP middleware rather than application-set per auth state.

Frozen from spec.json and prereg.md — DO NOT MODIFY.
"""

import hashlib
import json
import os
import random
import subprocess
import sys
import time
import uuid
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import jwt
import requests

# ---------------------------------------------------------------------------
# FROZEN CONSTANTS
# ---------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-RUNTIME-34300004597"
BASE_URL = "http://127.0.0.1:{port}/realms/spider-test/protocol/openid-connect/userinfo"
TOKEN_URL = "http://127.0.0.1:{port}/realms/spider-test/protocol/openid-connect/token"
REALM_NAME = "spider-test"
CLIENT_ID = "spider-client"
CLIENT_SECRET = "spider-secret-12345"
ADMIN_USER = "admin"
ADMIN_PASS = "admin"
KEYCLOAK_PORT = 18080
REPS = 10
SEED = 44

EXCLUDED_HEADERS = {"date", "server", "x-request-id"}

# ---------------------------------------------------------------------------
# TOKEN GENERATION (Keycloak-realm-aware)
# ---------------------------------------------------------------------------

def get_keycloak_token(username: str = "alice", password: str = "alice123") -> Optional[str]:
    """Get an access token from Keycloak via direct access grant."""
    try:
        r = requests.post(
            TOKEN_URL.format(port=KEYCLOAK_PORT),
            data={
                "grant_type": "password",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "username": username,
                "password": password,
                "scope": "openid",
            },
            timeout=10,
        )
        if r.status_code == 200:
            return r.json()["access_token"]
    except Exception:
        pass
    return None


def make_expired_token() -> str:
    """Generate an expired JWT: sub=alice, exp=1h ago, HS256 (locally signed)."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": "alice",
        "name": "Alice",
        "email": "alice@example.com",
        "iat": int((now - timedelta(hours=2)).timestamp()),
        "exp": int((now - timedelta(hours=1)).timestamp()),
        "realm_access": {"roles": ["user"]},
    }
    return jwt.encode(payload, CLIENT_SECRET, algorithm="HS256")


def make_invalid_token() -> str:
    """Generate a malformed token string that fails JWT validation."""
    return "not-a-real-jwt-token"


# ---------------------------------------------------------------------------
# AUTH STATE DEFINITIONS (frozen)
# ---------------------------------------------------------------------------

# valid_token will be obtained from Keycloak's token endpoint at runtime
# For now, set to None; will be populated after Keycloak is configured
VALID_TOKEN_STR = None
EXPIRED_TOKEN_STR = make_expired_token()
INVALID_TOKEN_STR = make_invalid_token()

AUTH_STATES = {
    "no_auth": {
        "auth_header": None,
        "expected_status": 401,
    },
    "valid_token": {
        "auth_header": None,  # Will be set after getting token from Keycloak
        "expected_status": 200,
    },
    "expired_token": {
        "auth_header": f"Bearer {EXPIRED_TOKEN_STR}",
        "expected_status": 401,
    },
    "invalid_token": {
        "auth_header": f"Bearer {INVALID_TOKEN_STR}",
        "expected_status": 401,
    },
}


# ---------------------------------------------------------------------------
# KEYCLOAK DOCKER MANAGEMENT
# ---------------------------------------------------------------------------

def start_keycloak() -> subprocess.Popen:
    """Start Keycloak in dev mode via Docker."""
    print("Starting Keycloak Docker container...")

    # Remove any existing container
    subprocess.run(
        ["docker", "rm", "-f", "spider-keycloak-test"],
        capture_output=True, timeout=30,
    )

    proc = subprocess.Popen(
        [
            "docker", "run", "-d",
            "--name", "spider-keycloak-test",
            "-p", f"{KEYCLOAK_PORT}:8080",
            "-e", f"KEYCLOAK_ADMIN={ADMIN_USER}",
            "-e", f"KEYCLOAK_ADMIN_PASSWORD={ADMIN_PASS}",
            "quay.io/keycloak/keycloak:25.0",
            "start-dev",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate(timeout=30)
    if proc.returncode != 0:
        raise RuntimeError(f"docker run failed: {stderr.decode()}")
    print(f"Keycloak container started: {stdout.decode().strip()}")
    return proc


def wait_for_keycloak(timeout: int = 120) -> bool:
    """Wait for Keycloak to be ready."""
    print(f"Waiting for Keycloak to be ready (timeout={timeout}s)...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(
                f"http://127.0.0.1:{KEYCLOAK_PORT}/realms/master",
                timeout=5,
            )
            if r.status_code == 200:
                print("Keycloak is ready!")
                return True
        except Exception:
            pass
        time.sleep(2)
    return False


def stop_keycloak():
    """Stop and remove the Keycloak container."""
    print("Stopping Keycloak container...")
    subprocess.run(
        ["docker", "rm", "-f", "spider-keycloak-test"],
        capture_output=True, timeout=30,
    )
    print("Keycloak stopped.")


def get_admin_token() -> str:
    """Get an admin access token from Keycloak."""
    r = requests.post(
        f"http://127.0.0.1:{KEYCLOAK_PORT}/realms/master/protocol/openid-connect/token",
        data={
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": ADMIN_USER,
            "password": ADMIN_PASS,
        },
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def configure_realm(admin_token: str):
    """Configure the spider-test realm with direct access grants."""
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
    }

    # Create realm
    realm_config = {
        "realm": REALM_NAME,
        "enabled": True,
        "registrationAllowed": False,
        "loginWithEmailAllowed": True,
        "duplicateEmailsAllowed": False,
        "resetPasswordAllowed": True,
        "editUsernameAllowed": False,
        "bruteForceProtected": False,
        "permanentLockout": False,
        "maxFailureWaitSeconds": 900,
        "minimumQuickLoginWaitSeconds": 60,
        "waitIncrementSeconds": 60,
        "quickLoginCheckMilliSeconds": 1000,
        "maxDeltaTimeSeconds": 43200,
        "failureFactor": 5,
        "accessTokenLifespan": 300,
        "ssoSessionIdleTimeout": 1800,
        "accessTokenLifespanForImplicitFlow": 900,
        "accessCodeLifespan": 60,
        "accessCodeLifespanUserAction": 300,
        "accessCodeLifespanLogin": 1800,
        "actionTokenGeneratedByAdminLifespan": 43200,
        "actionTokenGeneratedByUserLifespan": 300,
    }

    r = requests.post(
        f"http://127.0.0.1:{KEYCLOAK_PORT}/admin/realms",
        json=realm_config,
        headers=headers,
        timeout=10,
    )
    if r.status_code == 201:
        print(f"Realm '{REALM_NAME}' created.")
    elif r.status_code == 409:
        print(f"Realm '{REALM_NAME}' already exists.")
    else:
        print(f"Realm creation: {r.status_code} {r.text}")
        r.raise_for_status()

    # Create client
    client_config = {
        "clientId": CLIENT_ID,
        "enabled": True,
        "protocol": "openid-connect",
        "publicClient": False,
        "secret": CLIENT_SECRET,
        "directAccessGrantsEnabled": True,
        "serviceAccountsEnabled": False,
        "standardFlowEnabled": False,
        "implicitFlowEnabled": False,
        "attributes": {
            "access.token.lifespan": "300",
        },
    }

    r = requests.post(
        f"http://127.0.0.1:{KEYCLOAK_PORT}/admin/realms/{REALM_NAME}/clients",
        json=client_config,
        headers=headers,
        timeout=10,
    )
    if r.status_code == 201:
        print(f"Client '{CLIENT_ID}' created.")
    elif r.status_code == 409:
        print(f"Client '{CLIENT_ID}' already exists.")
    else:
        print(f"Client creation: {r.status_code} {r.text}")
        r.raise_for_status()

    # Create user alice
    user_config = {
        "username": "alice",
        "enabled": True,
        "emailVerified": True,
        "email": "alice@example.com",
        "firstName": "Alice",
        "lastName": "Smith",
    }

    r = requests.post(
        f"http://127.0.0.1:{KEYCLOAK_PORT}/admin/realms/{REALM_NAME}/users",
        json=user_config,
        headers=headers,
        timeout=10,
    )
    if r.status_code == 201:
        print("User 'alice' created.")
    elif r.status_code == 409:
        print("User 'alice' already exists.")
    else:
        print(f"User creation: {r.status_code} {r.text}")
        r.raise_for_status()

    # Get user ID for alice
    r = requests.get(
        f"http://127.0.0.1:{KEYCLOAK_PORT}/admin/realms/{REALM_NAME}/users?username=alice",
        headers=headers,
        timeout=10,
    )
    r.raise_for_status()
    users = r.json()
    if not users:
        print("ERROR: User 'alice' not found after creation!")
    else:
        alice_id = users[0]["id"]
        print(f"User 'alice' ID: {alice_id}")

        # Set password for alice using user ID
        r = requests.put(
            f"http://127.0.0.1:{KEYCLOAK_PORT}/admin/realms/{REALM_NAME}/users/{alice_id}/reset-password",
            json={"type": "password", "value": "alice123", "temporary": False},
            headers=headers,
            timeout=10,
        )
        if r.status_code in (200, 204):
            print("User 'alice' password set.")
        else:
            print(f"Password set: {r.status_code} {r.text}")

    print("Realm configuration complete.")


# ---------------------------------------------------------------------------
# HTTP OBSERVATION CLIENT
# ---------------------------------------------------------------------------

def make_request(url: str, auth_header: str = None, timeout: int = 10) -> dict:
    """Execute HTTP request, capture raw observation."""
    headers = {}
    if auth_header:
        headers["Authorization"] = auth_header

    start = time.monotonic()
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        elapsed = time.monotonic() - start
        status = resp.status_code
        resp_headers = dict(resp.headers)
        body = resp.content
        redirect_url = resp.url if resp.url != url else None
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
    """
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
    redirect_chain = observation.get("redirect_url") or ""
    headers_filtered = {k: v for k, v in observation["headers"].items()
                        if k.lower() not in EXCLUDED_HEADERS}
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
    return [int(c, 16) >> i & 1 for c in hex_str for i in range(3, -1, -1)]


def jaccard_similarity(fp_a: str, fp_b: str) -> float:
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
    """Compute discrimination score: intra_match_rate - inter_match_rate."""
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
        unique_sampled = list(set(sampled))
        if len(unique_sampled) < 2:
            continue
        ds = compute_discrimination_score(
            {s: fingerprints_by_state[s] for s in unique_sampled}
        )
        scores.append(ds["discrimination_score"])

    if not scores:
        return {"mean": 0, "lower": 0, "upper": 0, "n_bootstrap": 0}

    scores.sort()
    alpha = (1 - ci) / 2
    lo = scores[int(alpha * len(scores))]
    hi = scores[int((1 - alpha) * len(scores))]
    mean = sum(scores) / len(scores)
    return {"mean": mean, "lower": lo, "upper": hi, "n_bootstrap": len(scores)}


# ---------------------------------------------------------------------------
# BASELINES
# ---------------------------------------------------------------------------

def baseline_url_hash(url: str, n: int = 10) -> list:
    return [hashlib.sha256(url.encode()).hexdigest() for _ in range(n)]


def baseline_random(n: int = 10, seed: int = 99) -> list:
    rng = random.Random(seed)
    return [hashlib.sha256(rng.getrandbits(256).to_bytes(32, "big")).hexdigest() for _ in range(n)]


def baseline_status_only(status: int, n: int = 10) -> list:
    return [hashlib.sha256(str(status).encode()).hexdigest() for _ in range(n)]


def baseline_body_only(body: bytes, n: int = 10) -> list:
    return [hashlib.sha256(body).hexdigest() for _ in range(n)]


# ---------------------------------------------------------------------------
# SINGLE-HEADER DISCRIMINATION
# ---------------------------------------------------------------------------

def compute_single_header_discrimination(fingerprints_by_state: dict, header_key: str, raw_observations: dict) -> dict:
    """Compute discrimination for a single header value."""
    header_fps_by_state = {}
    for state, obs_list in raw_observations.items():
        fps = []
        for obs in obs_list:
            val = obs["headers"].get(header_key, "")
            fp = hashlib.sha256(val.encode("utf-8")).hexdigest()
            fps.append(fp)
        header_fps_by_state[state] = fps
    return compute_discrimination_score(header_fps_by_state)


# ---------------------------------------------------------------------------
# MAIN EXPERIMENT
# ---------------------------------------------------------------------------

def run_experiment():
    """Run the full experiment on Keycloak OAuth/OIDC provider."""
    raw_obs_path = "raw_observations.json"

    # Step 1: Start Keycloak
    try:
        kc_proc = start_keycloak()
    except Exception as e:
        print(f"FAILED to start Keycloak: {e}")
        return build_blocked_result(f"Keycloak Docker start failed: {e}")

    # Step 2: Wait for Keycloak
    if not wait_for_keycloak(timeout=120):
        stop_keycloak()
        return build_blocked_result("Keycloak did not become ready within 120s timeout")

    # Step 3: Configure realm
    try:
        admin_token = get_admin_token()
        configure_realm(admin_token)
    except Exception as e:
        stop_keycloak()
        return build_blocked_result(f"Keycloak realm configuration failed: {e}")

    # Step 4: Verify token acquisition works and get valid token
    print("\nVerifying direct access grant...")
    try:
        keycloak_token = get_keycloak_token()
        if keycloak_token is None:
            stop_keycloak()
            return build_blocked_result("Direct access grant failed: could not obtain token")
        print(f"Direct access grant succeeded. Token length: {len(keycloak_token)}")

        # Set the valid token in AUTH_STATES
        AUTH_STATES["valid_token"]["auth_header"] = f"Bearer {keycloak_token}"
    except Exception as e:
        stop_keycloak()
        return build_blocked_result(f"Direct access grant failed: {e}")

    # Step 5: Execute experiment
    base_url = BASE_URL.format(port=KEYCLOAK_PORT)

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

    print(f"\n=== Experiment: Ecological Validity on Keycloak ===")
    print(f"States: {list(AUTH_STATES.keys())}")
    print(f"Reps per state: {REPS}")
    print(f"Total requests: {len(plan)}")
    print(f"Seed: {SEED}")
    print(f"Key design: expired_token and invalid_token return IDENTICAL bodies")
    print(f"  Headers determined by Keycloak middleware (NOT application-set)")
    print()

    for i, (state_name, rep) in enumerate(plan):
        cfg = AUTH_STATES[state_name]
        try:
            obs = make_request(base_url, auth_header=cfg["auth_header"])
            obs["state"] = state_name
            obs["rep"] = rep
            obs["fingerprint"] = fingerprint(obs)

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

    # Step 6: Validate error rate
    total_requests = len(plan)
    error_rate = len(errors) / total_requests if total_requests > 0 else 0
    measurement_valid = error_rate <= 0.20

    if not measurement_valid:
        print(f"\nMEASUREMENT_INVALID: error rate {error_rate:.1%} > 20%")
        stop_keycloak()
        return build_measurement_invalid_result(
            f"Keycloak error rate {error_rate:.1%} > 20% threshold",
            errors, total_requests, error_rate,
        )

    # Step 7: Verify identical bodies for expired/invalid
    body_hashes_by_state = {}
    for state, obs_list in raw_observations.items():
        body_hashes_by_state[state] = list(set(hashlib.sha256(obs["body"]).hexdigest() for obs in obs_list))

    expired_invalid_identical = (
        len(body_hashes_by_state.get("expired_token", [])) >= 1
        and len(body_hashes_by_state.get("invalid_token", [])) >= 1
        and body_hashes_by_state["expired_token"][0] == body_hashes_by_state["invalid_token"][0]
    )

    # If bodies are NOT identical, Keycloak may return different error messages
    # This is a configuration/design constraint, not infrastructure failure
    if not expired_invalid_identical:
        print("WARNING: expired_token and invalid_token bodies are NOT identical.")
        print(f"  expired hashes: {body_hashes_by_state.get('expired_token', [])}")
        print(f"  invalid hashes: {body_hashes_by_state.get('invalid_token', [])}")
        print("  This may affect discrimination analysis.")
        # Continue with measurement — bodies may differ, which is a valid IdP behavior

    print("\n--- Body Identity Verification ---")
    for state in ["expired_token", "invalid_token"]:
        print(f"  {state}: {body_hashes_by_state.get(state, ['N/A'])}")
    print(f"  expired == invalid: {expired_invalid_identical}")

    # Step 8: Verify Cache-Control presence in raw HTTP responses
    cache_control_verification = {}
    for state in AUTH_STATES:
        obs_list = raw_observations[state]
        if obs_list:
            cc_vals = [obs["headers"].get("Cache-Control", "(absent)") for obs in obs_list]
            cache_control_verification[state] = {
                "observed_values": list(set(cc_vals)),
                "consistent": len(set(cc_vals)) == 1,
            }

    print("\n--- Cache-Control Verification ---")
    for state, v in cache_control_verification.items():
        print(f"  {state}: observed={v['observed_values']}, consistent={v['consistent']}")

    # Step 9: Verify Set-Cookie presence
    set_cookie_verification = {}
    for state in AUTH_STATES:
        obs_list = raw_observations[state]
        if obs_list:
            sc_vals = [obs["headers"].get("Set-Cookie", "(absent)") for obs in obs_list]
            set_cookie_verification[state] = {
                "observed_present": any(v != "(absent)" for v in sc_vals),
                "consistent": len(set(sc_vals)) == 1,
            }

    print("\n--- Set-Cookie Verification ---")
    for state, v in set_cookie_verification.items():
        print(f"  {state}: present={v['observed_present']}, consistent={v['consistent']}")

    # Step 10: Compute discrimination score (full vector)
    disc = compute_discrimination_score(fingerprints_by_state)
    boot = bootstrap_ci_discrimination(fingerprints_by_state, seed=42)

    print(f"\n--- Full Vector Results ---")
    print(f"Discrimination: {disc['discrimination_score']:.6f}")
    print(f"Intra match rate: {disc['intra_match_rate']:.6f}")
    print(f"Inter match rate: {disc['inter_match_rate']:.6f}")
    print(f"Bootstrap 95% CI: [{boot['lower']:.6f}, {boot['upper']:.6f}]")

    # Step 11: Compute baselines
    baselines = {}

    # B-URL-HASH: URL is constant, expected 0.0
    b_url_fps = baseline_url_hash(base_url, n=REPS)
    b_url_by_state = {s: b_url_fps for s in AUTH_STATES}
    b_url_disc = compute_discrimination_score(b_url_by_state)
    baselines["B-URL-HASH"] = {"discrimination_score": b_url_disc["discrimination_score"]}
    print(f"\nB-URL-HASH discrimination: {b_url_disc['discrimination_score']:.6f}")

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

    # B-BODY-ONLY: expired/invalid may or may not share body
    b_body_by_state = {}
    for state, obs_list in raw_observations.items():
        fps = [hashlib.sha256(obs["body"]).hexdigest() for obs in obs_list]
        b_body_by_state[state] = fps
    b_body_disc = compute_discrimination_score(b_body_by_state)
    baselines["B-BODY-ONLY"] = {"discrimination_score": b_body_disc["discrimination_score"]}
    print(f"B-BODY-ONLY discrimination: {b_body_disc['discrimination_score']:.6f}")

    # Step 12: Single-Header Discrimination
    cache_control_disc = compute_single_header_discrimination(
        fingerprints_by_state, "Cache-Control", raw_observations
    )
    set_cookie_disc = compute_single_header_discrimination(
        fingerprints_by_state, "Set-Cookie", raw_observations
    )

    print(f"\n--- Single-Header Discrimination ---")
    print(f"Cache-Control-only discrimination: {cache_control_disc['discrimination_score']:.6f}")
    print(f"Set-Cookie-only discrimination: {set_cookie_disc['discrimination_score']:.6f}")

    # ETag-only (body correlation control)
    etag_disc = compute_single_header_discrimination(
        fingerprints_by_state, "ETag", raw_observations
    )
    etag_body_correlated = abs(etag_disc["discrimination_score"] - b_body_disc["discrimination_score"]) < 0.01
    print(f"ETag-only discrimination: {etag_disc['discrimination_score']:.6f}")

    # Step 13: Controls
    # Null control: FP rate
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

    total_pairs = sum(max(r["total"] * (r["total"] - 1) // 2, 0) for r in null_results.values())
    total_diff_pairs = sum(
        max((r["unique"] - 1) * r["total"] // 2, 0) for r in null_results.values()
    ) if total_pairs > 0 else 0
    overall_fp_rate = total_diff_pairs / total_pairs if total_pairs > 0 else 0
    null_control_pass = overall_fp_rate < 0.05

    # Positive controls
    cache_control_positive_control_pass = cache_control_disc["discrimination_score"] > 0
    set_cookie_positive_control_pass = set_cookie_disc["discrimination_score"] > 0
    positive_control_pass = disc["discrimination_score"] > 0.5

    # Incremental header value
    incremental_header_value = disc["discrimination_score"] - b_body_disc["discrimination_score"]
    body_only_ratio = disc["discrimination_score"] / b_body_disc["discrimination_score"] if b_body_disc["discrimination_score"] > 0 else float('inf')
    full_exceeds_body = disc["discrimination_score"] > b_body_disc["discrimination_score"]
    full_equals_body = abs(disc["discrimination_score"] - b_body_disc["discrimination_score"]) < 1e-9

    print(f"\n--- KEY TEST: Full Vector vs B-BODY-ONLY ---")
    print(f"B-BODY-ONLY: {b_body_disc['discrimination_score']:.6f}")
    print(f"Full-vector: {disc['discrimination_score']:.6f}")
    print(f"Incremental header value: {incremental_header_value:.6f}")
    print(f"Ratio (full/body): {body_only_ratio:.6f}")

    # Drift control
    drift_states = ["valid_token", "expired_token", "invalid_token"]
    drift_jaccards = []
    for idx_d in range(len(drift_states) - 1):
        s1, s2 = drift_states[idx_d], drift_states[idx_d + 1]
        fps1 = fingerprints_by_state[s1]
        fps2 = fingerprints_by_state[s2]
        sims = [jaccard_similarity(f1, f2) for f1 in fps1 for f2 in fps2]
        mean_sim = sum(sims) / len(sims) if sims else 0
        drift_jaccards.append(mean_sim)

    drift_all_discriminable = all(j < 0.5 for j in drift_jaccards)

    print(f"\n--- Drift Control ---")
    for idx_d in range(len(drift_states) - 1):
        print(f"  {drift_states[idx_d]} -> {drift_states[idx_d+1]}: Jaccard={drift_jaccards[idx_d]:.4f}")
    print(f"All discriminable (<0.5): {drift_all_discriminable}")

    # Step 14: Decision Rule
    survives = (
        full_exceeds_body
        and positive_control_pass
        and null_control_pass
        and cache_control_positive_control_pass
    )

    falsified_no_increment = full_equals_body
    falsified_no_cc_variation = not cache_control_positive_control_pass

    if survives:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif falsified_no_increment or falsified_no_cc_variation:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif disc["discrimination_score"] <= 0.5:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not null_control_pass:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    else:
        outcome = "MIXED"
        status = "COMPLETE"

    print(f"\n=== FINAL VERDICT ===")
    print(f"Status: {status}")
    print(f"Outcome: {outcome}")
    print(f"Survives: {survives}")
    print(f"Full > Body-Only: {full_exceeds_body}")
    print(f"Full == Body-Only: {full_equals_body}")
    print(f"Cache-Control varies: {cache_control_positive_control_pass}")

    # Build controls object
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
        "C_CACHE_CONTROL_VARIATION": {
            "expected": "Cache-Control-only discrimination > 0",
            "observed": f"{cache_control_disc['discrimination_score']:.6f}",
            "pass": cache_control_positive_control_pass,
            "detail": cache_control_verification,
        },
        "C_SET_COOKIE_VARIATION": {
            "expected": "Set-Cookie-only discrimination > 0",
            "observed": f"{set_cookie_disc['discrimination_score']:.6f}",
            "pass": set_cookie_positive_control_pass,
            "detail": set_cookie_verification,
        },
        "C_INCREMENTAL_HEADER_VALUE": {
            "expected": "full_vector_discrimination > B-BODY-ONLY",
            "observed": f"full={disc['discrimination_score']:.6f}, body_only={b_body_disc['discrimination_score']:.6f}, delta={incremental_header_value:.6f}",
            "pass": full_exceeds_body,
        },
        "C_BODY_CORRELATION_ETAG": {
            "expected": "ETag discrimination == B-BODY-ONLY (body-correlated)",
            "observed": f"ETag={etag_disc['discrimination_score']:.6f}, body={b_body_disc['discrimination_score']:.6f}",
            "pass": etag_body_correlated,
        },
        "C_BODY_IDENTITY_EXPIRED_INVALID": {
            "expected": "expired_token and invalid_token share identical body hash",
            "observed": f"expired={body_hashes_by_state.get('expired_token', ['N/A'])}, invalid={body_hashes_by_state.get('invalid_token', ['N/A'])}",
            "pass": expired_invalid_identical,
        },
        "C_DRIFT_VALID_VS_EXPIRED": {
            "expected": "Jaccard < 0.5 (discriminable)",
            "observed": f"Jaccard={drift_jaccards[0]:.4f}" if drift_jaccards else "N/A",
            "pass": drift_jaccards[0] < 0.5 if drift_jaccards else False,
        },
        "C_DRIFT_EXPIRED_VS_INVALID": {
            "expected": "Jaccard < 0.5 (discriminable via Cache-Control)",
            "observed": f"Jaccard={drift_jaccards[1]:.4f}" if len(drift_jaccards) > 1 else "N/A",
            "pass": drift_jaccards[1] < 0.5 if len(drift_jaccards) > 1 else False,
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
        "incremental_header_value": incremental_header_value,
        "full_vs_body_only_ratio": body_only_ratio,
        "cache_control_only_discrimination": cache_control_disc["discrimination_score"],
        "set_cookie_only_discrimination": set_cookie_disc["discrimination_score"],
        "etag_only_discrimination": etag_disc["discrimination_score"],
        "null_fp_rate": overall_fp_rate,
        "drift_jaccards": drift_jaccards,
        "drift_all_discriminable": drift_all_discriminable,
        "total_requests": total_requests,
        "error_rate": error_rate,
    }

    # Observations (raw, not interpretations)
    observations = [
        f"Keycloak 25.0 deployed via Docker on localhost:{KEYCLOAK_PORT}",
        f"Realm '{REALM_NAME}' configured with client '{CLIENT_ID}' (direct access grants enabled)",
        f"User 'alice' created with password authentication",
        f"Direct access grant verified: token acquisition successful",
        f"4 auth states x {REPS} reps = {total_requests} requests completed",
        f"Client-side jitter: 0-200ms inter-request delay (seed={SEED})",
        f"Key design: expired_token and invalid_token return IDENTICAL bodies (if IdP config allows)",
        f"Headers determined by Keycloak middleware (NOT application-set)",
        f"Headers filtered: Date/Server/X-Request-Id excluded from fingerprint",
        f"Cache-Control verification: {json.dumps(cache_control_verification)}",
        f"Set-Cookie verification: {json.dumps(set_cookie_verification)}",
        f"expired_token and invalid_token body hashes identical: {expired_invalid_identical}",
        f"body_hashes_by_state: {json.dumps({k: v for k, v in body_hashes_by_state.items()})}",
        f"Full-vector discrimination: {disc['discrimination_score']:.6f} (threshold: > 0.5)",
        f"Full-vector bootstrap 95% CI: [{boot['lower']:.6f}, {boot['upper']:.6f}]",
        f"B-STATUS-ONLY discrimination: {b_status_disc['discrimination_score']:.6f}",
        f"B-BODY-ONLY discrimination: {b_body_disc['discrimination_score']:.6f}",
        f"B-URL-HASH discrimination: {b_url_disc['discrimination_score']:.6f}",
        f"B-RANDOM discrimination: {b_rand_disc['discrimination_score']:.6f}",
        f"Cache-Control-only discrimination: {cache_control_disc['discrimination_score']:.6f}",
        f"Set-Cookie-only discrimination: {set_cookie_disc['discrimination_score']:.6f}",
        f"ETag-only discrimination: {etag_disc['discrimination_score']:.6f} (body-correlated)",
        f"Null FP rate: {overall_fp_rate:.1%} (threshold: < 5%)",
        f"Incremental header value (full - body_only): {incremental_header_value:.6f}",
        f"valid_token vs expired_token drift Jaccard: {drift_jaccards[0]:.4f}" if drift_jaccards else "N/A",
        f"expired_token vs invalid_token drift Jaccard: {drift_jaccards[1]:.4f}" if len(drift_jaccards) > 1 else "N/A",
    ]

    # Save raw observations
    raw_obs_serializable = {}
    for state, obs_list in raw_observations.items():
        raw_obs_serializable[state] = []
        for obs in obs_list:
            raw_obs_serializable[state].append({
                "url": obs["url"],
                "status": obs["status"],
                "headers": obs["headers"],
                "body_hash": hashlib.sha256(obs["body"]).hexdigest(),
                "body_preview": obs["body"][:500].decode("utf-8", errors="replace"),
                "fingerprint": obs["fingerprint"],
                "elapsed": obs["elapsed"],
                "timestamp": obs["timestamp"],
                "state": obs["state"],
                "rep": obs["rep"],
            })

    with open(raw_obs_path, "w") as f:
        json.dump(raw_obs_serializable, f, indent=2)
    print(f"\nRaw observations saved to {raw_obs_path}")

    # Stop Keycloak
    stop_keycloak()

    # Validity notes
    validity_notes = [
        f"Keycloak 25.0 deployed via Docker (image: quay.io/keycloak/keycloak:25.0) on localhost:{KEYCLOAK_PORT}",
        f"Realm '{REALM_NAME}' with direct access grants enabled — no browser needed for token acquisition",
        "Cache-Control and Set-Cookie patterns are determined by Keycloak middleware, NOT application-set per auth state",
        "This is the key difference from the Flask parent experiment where headers were deliberately varied per auth state",
        "Fingerprint uses repr(vector) with tuple(sorted(...)) — deterministic within same Python version but Python-version-dependent",
        "Date and Server headers excluded from fingerprint vector to prevent spurious variance",
        "X-Request-Id excluded from fingerprint — volatile per-request identifier",
        f"expired_token and invalid_token body identity: {expired_invalid_identical} — if not identical, Keycloak returns different error messages for expired vs invalid tokens",
        "ETag is body-correlated — adds no independent information",
        "Sample size: 40 requests (4 states x 10 reps) — limited statistical power for subtle discrimination differences",
        f"Python version: {sys.version}",
        f"Error rate: {error_rate:.1%} ({len(errors)} errors out of {total_requests} requests)",
        "Discrimination metric: intra_match_rate - inter_match_rate. Range [-1, 1]. Perfect = 1, no discrimination = 0.",
        "Keycloak was stopped after experiment to free resources.",
    ]

    # Unresolved
    unresolved = [
        "Does the substrate maintain discrimination on production OAuth/OIDC providers (Auth0, Okta) with CDN, load-balancer variance, and compressed encoding?",
        "What is the false-positive rate under server-side processing jitter >150ms or volatile standard headers beyond X-Request-Id?",
        "Can substrate detect continuous session drift as a continuous signal rather than discrete state classification?",
        "What is cross-Python-version reproducibility of repr(vector) hashes?",
        "What is the incremental header value when MORE than 2 error states share identical bodies?",
        "If Keycloak returns different bodies for expired vs invalid tokens, does body-only achieve perfect discrimination without headers?",
    ]

    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
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


def build_blocked_result(reason: str) -> dict:
    """Build a BLOCKED result for infrastructure failure."""
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": "runtime",
        "status": "BLOCKED",
        "outcome": "NOT_APPLICABLE",
        "metrics": {},
        "controls": {},
        "artifacts": [],
        "observations": [f"Infrastructure failure: {reason}"],
        "validity_notes": [f"BLOCKED: {reason}. This is infrastructure failure, not scientific falsification."],
        "unresolved": [f"What specific action would unblock this experiment? Fix: {reason}"],
    }


def build_measurement_invalid_result(reason: str, errors: list, total: int, error_rate: float) -> dict:
    """Build a MEASUREMENT_INVALID result."""
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": "runtime",
        "status": "MEASUREMENT_INVALID",
        "outcome": "NOT_APPLICABLE",
        "metrics": {"error_rate": error_rate, "total_requests": total, "errors": errors},
        "controls": {},
        "artifacts": [],
        "observations": [f"Measurement invalid: {reason}"],
        "validity_notes": [f"MEASUREMENT_INVALID: {reason}. Error rate {error_rate:.1%} > 20% threshold."],
        "unresolved": ["Retry with more stable Keycloak deployment or diagnose infrastructure issue."],
    }


if __name__ == "__main__":
    result = run_experiment()

    # Write result.json
    result_path = "result.json"
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nResult written to {result_path}")
    print(f"Status: {result['status']}, Outcome: {result['outcome']}")
