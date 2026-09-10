#!/usr/bin/env python3
"""
EXP-RUNTIME-34439061845 — WWW-Authenticate Transfer Across Keycloak Endpoints
===============================================================================
Tests whether the WWW-Authenticate header discrimination pattern observed on
Keycloak /userinfo transfers to /token (password grant), /token (client_credentials),
and /introspect endpoints.

Frozen from spec.json and prereg.md — DO NOT MODIFY.
"""

import hashlib
import json
import os
import random
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import jwt
import requests

# ---------------------------------------------------------------------------
# FROZEN CONSTANTS
# ---------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-RUNTIME-34439061845"
LANE = "runtime"
SEED = 44
REPS = 10
KEYCLOAK_PORT = 18080
REALM_NAME = "spider-test"
CLIENT_ID = "spider-client"
CLIENT_SECRET = "spider-secret-12345"
ADMIN_USER = "admin"
ADMIN_PASS = "admin"

EXCLUDED_HEADERS = {"date", "server", "x-request-id"}

# Endpoint definitions
USERINFO_URL = "http://127.0.0.1:{port}/realms/spider-test/protocol/openid-connect/userinfo"
TOKEN_URL = "http://127.0.0.1:{port}/realms/spider-test/protocol/openid-connect/token"
INTROSPECT_URL = "http://127.0.0.1:{port}/realms/spider-test/protocol/openid-connect/token/introspect"

# ---------------------------------------------------------------------------
# TOKEN GENERATION
# ---------------------------------------------------------------------------

def get_keycloak_token(username="alice", password="alice123"):
    """Get access token from Keycloak via direct access grant."""
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


def make_expired_token():
    """Generate an expired JWT (locally signed)."""
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


def make_invalid_token():
    """Generate a malformed token string."""
    return "not-a-real-jwt-token"


# ---------------------------------------------------------------------------
# KEYCLOAK DOCKER MANAGEMENT
# ---------------------------------------------------------------------------

def start_keycloak():
    """Start Keycloak in dev mode via Docker."""
    print("Starting Keycloak Docker container...")
    subprocess.run(["docker", "rm", "-f", "spider-keycloak-test"],
                   capture_output=True, timeout=30)
    proc = subprocess.Popen(
        ["docker", "run", "-d",
         "--name", "spider-keycloak-test",
         "-p", f"{KEYCLOAK_PORT}:8080",
         "-e", f"KEYCLOAK_ADMIN={ADMIN_USER}",
         "-e", f"KEYCLOAK_ADMIN_PASSWORD={ADMIN_PASS}",
         "quay.io/keycloak/keycloak:25.0",
         "start-dev"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate(timeout=30)
    if proc.returncode != 0:
        raise RuntimeError(f"docker run failed: {stderr.decode()}")
    print(f"Keycloak container started: {stdout.decode().strip()}")
    return proc


def wait_for_keycloak(timeout=120):
    """Wait for Keycloak to be ready."""
    print(f"Waiting for Keycloak to be ready (timeout={timeout}s)...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"http://127.0.0.1:{KEYCLOAK_PORT}/realms/master", timeout=5)
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
    subprocess.run(["docker", "rm", "-f", "spider-keycloak-test"],
                   capture_output=True, timeout=30)
    print("Keycloak stopped.")


def get_admin_token():
    """Get admin access token from Keycloak."""
    r = requests.post(
        f"http://127.0.0.1:{KEYCLOAK_PORT}/realms/master/protocol/openid-connect/token",
        data={"grant_type": "password", "client_id": "admin-cli",
              "username": ADMIN_USER, "password": ADMIN_PASS},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def configure_realm(admin_token):
    """Configure the spider-test realm."""
    headers = {"Authorization": f"Bearer {admin_token}", "Content-Type": "application/json"}

    realm_config = {
        "realm": REALM_NAME, "enabled": True, "registrationAllowed": False,
        "loginWithEmailAllowed": True, "duplicateEmailsAllowed": False,
        "resetPasswordAllowed": True, "editUsernameAllowed": False,
        "bruteForceProtected": False, "permanentLockout": False,
        "accessTokenLifespan": 300, "ssoSessionIdleTimeout": 1800,
    }
    r = requests.post(f"http://127.0.0.1:{KEYCLOAK_PORT}/admin/realms",
                      json=realm_config, headers=headers, timeout=10)
    if r.status_code == 201:
        print(f"Realm '{REALM_NAME}' created.")
    elif r.status_code == 409:
        print(f"Realm '{REALM_NAME}' already exists.")
    else:
        print(f"Realm creation: {r.status_code} {r.text}")
        r.raise_for_status()

    client_config = {
        "clientId": CLIENT_ID, "enabled": True, "protocol": "openid-connect",
        "publicClient": False, "secret": CLIENT_SECRET,
        "directAccessGrantsEnabled": True, "serviceAccountsEnabled": False,
        "standardFlowEnabled": False, "implicitFlowEnabled": False,
    }
    r = requests.post(f"http://127.0.0.1:{KEYCLOAK_PORT}/admin/realms/{REALM_NAME}/clients",
                      json=client_config, headers=headers, timeout=10)
    if r.status_code == 201:
        print(f"Client '{CLIENT_ID}' created.")
    elif r.status_code == 409:
        print(f"Client '{CLIENT_ID}' already exists.")
    else:
        print(f"Client creation: {r.status_code} {r.text}")
        r.raise_for_status()

    user_config = {
        "username": "alice", "enabled": True, "emailVerified": True,
        "email": "alice@example.com", "firstName": "Alice", "lastName": "Smith",
    }
    r = requests.post(f"http://127.0.0.1:{KEYCLOAK_PORT}/admin/realms/{REALM_NAME}/users",
                      json=user_config, headers=headers, timeout=10)
    if r.status_code in (201, 409):
        print("User 'alice' created or exists.")
    else:
        print(f"User creation: {r.status_code} {r.text}")
        r.raise_for_status()

    r = requests.get(f"http://127.0.0.1:{KEYCLOAK_PORT}/admin/realms/{REALM_NAME}/users?username=alice",
                     headers=headers, timeout=10)
    r.raise_for_status()
    users = r.json()
    if users:
        alice_id = users[0]["id"]
        r = requests.put(
            f"http://127.0.0.1:{KEYCLOAK_PORT}/admin/realms/{REALM_NAME}/users/{alice_id}/reset-password",
            json={"type": "password", "value": "alice123", "temporary": False},
            headers=headers, timeout=10,
        )
        if r.status_code in (200, 204):
            print("User 'alice' password set.")

    print("Realm configuration complete.")


# ---------------------------------------------------------------------------
# HTTP REQUEST EXECUTION
# ---------------------------------------------------------------------------

def make_request(url, method="GET", auth_header=None, body=None, timeout=10):
    """Execute HTTP request and capture raw observation."""
    headers = {}
    if auth_header:
        headers["Authorization"] = auth_header
    if body:
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    start = time.monotonic()
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        elif method == "POST":
            resp = requests.post(url, headers=headers, data=body, timeout=timeout, allow_redirects=True)
        else:
            raise ValueError(f"Unknown method: {method}")
        elapsed = time.monotonic() - start
        return {
            "url": url, "status": resp.status_code,
            "headers": dict(resp.headers), "body": resp.content,
            "redirect_url": resp.url if resp.url != url else None,
            "elapsed": elapsed, "timestamp": time.time(),
        }
    except Exception as e:
        elapsed = time.monotonic() - start
        return {
            "url": url, "status": 0, "headers": {},
            "body": str(e).encode("utf-8"),
            "redirect_url": None, "elapsed": elapsed, "timestamp": time.time(),
        }


# ---------------------------------------------------------------------------
# FINGERPRINT
# ---------------------------------------------------------------------------

def fingerprint(observation):
    """Deterministic fingerprint: SHA-256 of sorted-tuple vector."""
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
# JACCARD SIMILARITY
# ---------------------------------------------------------------------------

def hex_to_bits(hex_str):
    return [int(c, 16) >> i & 1 for c in hex_str for i in range(3, -1, -1)]


def jaccard_similarity(fp_a, fp_b):
    bits_a = hex_to_bits(fp_a)
    bits_b = hex_to_bits(fp_b)
    both = sum(a & b for a, b in zip(bits_a, bits_b))
    either = sum(a | b for a, b in zip(bits_a, bits_b))
    return both / either if either > 0 else 0.0


# ---------------------------------------------------------------------------
# DISCRIMINATION SCORE
# ---------------------------------------------------------------------------

def compute_discrimination_score(fingerprints_by_state):
    all_states = list(fingerprints_by_state.keys())
    intra_matches = 0
    intra_total = 0
    inter_matches = 0
    inter_total = 0

    for i, s1 in enumerate(all_states):
        fps1 = fingerprints_by_state[s1]
        for a in range(len(fps1)):
            for b in range(a + 1, len(fps1)):
                intra_total += 1
                if fps1[a] == fps1[b]:
                    intra_matches += 1
        for j, s2 in enumerate(all_states):
            if j <= i:
                continue
            fps2 = fingerprints_by_state[s2]
            for fa in fps1:
                for fb in fps2:
                    inter_total += 1
                    if fa == fb:
                        inter_matches += 1

    intra_match_rate = intra_matches / intra_total if intra_total > 0 else 0
    inter_match_rate = inter_matches / inter_total if inter_total > 0 else 0
    return intra_match_rate - inter_match_rate


# ---------------------------------------------------------------------------
# SINGLE-HEADER DISCRIMINATION
# ---------------------------------------------------------------------------

def compute_single_header_discrimination(fingerprints_by_state, header_key, raw_observations):
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
# BASELINES
# ---------------------------------------------------------------------------

def baseline_url_hash(url, n=10):
    return [hashlib.sha256(url.encode()).hexdigest() for _ in range(n)]


def baseline_random(n=10, seed=99):
    rng = random.Random(seed)
    return [hashlib.sha256(rng.getrandbits(256).to_bytes(32, "big")).hexdigest()
            for _ in range(n)]


# ---------------------------------------------------------------------------
# ENDPOINT DEFINITIONS
# ---------------------------------------------------------------------------

def get_endpoint_configs(auth_token):
    """Return endpoint configurations: (name, url, method, body_fn, expected_status_fn)"""
    expired_token = make_expired_token()
    invalid_token = make_invalid_token()

    def userinfo_body(state):
        """GET request: body is None, auth is in header."""
        return None

    def token_password_body(state):
        """POST password grant: credentials in body."""
        body = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": "alice",
            "password": "alice123",
            "scope": "openid",
        }
        return "&".join(f"{k}={v}" for k, v in body.items())

    def token_cc_body(state):
        """POST client_credentials grant: credentials in body."""
        body = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        return "&".join(f"{k}={v}" for k, v in body.items())

    def introspect_body(state):
        """POST introspect: token in body."""
        token_map = {
            "no_auth": "",
            "valid_token": auth_token,
            "expired_token": expired_token,
            "invalid_token": invalid_token,
        }
        body = {
            "token": token_map.get(state, ""),
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        return "&".join(f"{k}={v}" for k, v in body.items())

    def userinfo_expected_status(state):
        return 200 if state == "valid_token" else 401

    def token_expected_status(state):
        if state == "valid_token":
            return 200
        elif state == "no_auth":
            # password grant without auth: Keycloak processes form body credentials
            return 200
        else:
            # expired/invalid token in Authorization header: ignored for password grant
            return 200

    def introspect_expected_status(state):
        # introspect always returns 200 with {active: true/false}
        return 200

    return [
        {
            "name": "/userinfo (GET)",
            "url": USERINFO_URL.format(port=KEYCLOAK_PORT),
            "method": "GET",
            "body_fn": userinfo_body,
            "expected_status_fn": userinfo_expected_status,
        },
        {
            "name": "/token (POST password)",
            "url": TOKEN_URL.format(port=KEYCLOAK_PORT),
            "method": "POST",
            "body_fn": token_password_body,
            "expected_status_fn": token_expected_status,
        },
        {
            "name": "/token (POST client_credentials)",
            "url": TOKEN_URL.format(port=KEYCLOAK_PORT),
            "method": "POST",
            "body_fn": token_cc_body,
            "expected_status_fn": token_expected_status,
        },
        {
            "name": "/introspect (POST)",
            "url": INTROSPECT_URL.format(port=KEYCLOAK_PORT),
            "method": "POST",
            "body_fn": introspect_body,
            "expected_status_fn": introspect_expected_status,
        },
    ]


# ---------------------------------------------------------------------------
# AUTH STATE TOKEN GENERATION
# ---------------------------------------------------------------------------

def get_auth_header(state, auth_token):
    """Return Authorization header value for a given state."""
    if state == "no_auth":
        return None
    elif state == "valid_token":
        return f"Bearer {auth_token}"
    elif state == "expired_token":
        return f"Bearer {make_expired_token()}"
    elif state == "invalid_token":
        return f"Bearer {make_invalid_token()}"
    return None


# ---------------------------------------------------------------------------
# MAIN EXPERIMENT
# ---------------------------------------------------------------------------

def run_experiment():
    """Run the full multi-endpoint experiment."""
    raw_observations_all = {}  # endpoint_name -> state -> [obs]
    endpoint_results = {}
    errors = []

    # Step 1: Start Keycloak
    try:
        kc_proc = start_keycloak()
    except Exception as e:
        print(f"FAILED to start Keycloak: {e}")
        return build_blocked_result(f"Keycloak Docker start failed: {e}")

    # Step 2: Wait for Keycloak
    if not wait_for_keycloak(timeout=120):
        stop_keycloak()
        return build_blocked_result("Keycloak did not become ready within 120s")

    # Step 3: Configure realm
    try:
        admin_token = get_admin_token()
        configure_realm(admin_token)
    except Exception as e:
        stop_keycloak()
        return build_blocked_result(f"Keycloak realm configuration failed: {e}")

    # Step 4: Get valid token
    print("\nVerifying direct access grant...")
    try:
        auth_token = get_keycloak_token()
        if auth_token is None:
            stop_keycloak()
            return build_blocked_result("Direct access grant failed: could not obtain token")
        print(f"Direct access grant succeeded. Token length: {len(auth_token)}")
    except Exception as e:
        stop_keycloak()
        return build_blocked_result(f"Direct access grant failed: {e}")

    # Step 5: Get endpoint configs
    endpoints = get_endpoint_configs(auth_token)
    auth_states = ["no_auth", "valid_token", "expired_token", "invalid_token"]

    # Step 6: Run experiment for each endpoint
    rng = random.Random(SEED)

    for ep in endpoints:
        ep_name = ep["name"]
        print(f"\n{'='*60}")
        print(f"Testing endpoint: {ep_name}")
        print(f"{'='*60}")

        # Build plan: 4 states x 10 reps
        plan = []
        for state in auth_states:
            for rep in range(REPS):
                plan.append((state, rep))
        rng.shuffle(plan)

        raw_observations = defaultdict(list)
        fingerprints_by_state = defaultdict(list)

        for i, (state, rep) in enumerate(plan):
            auth_header = get_auth_header(state, auth_token)
            body = ep["body_fn"](state)

            try:
                obs = make_request(ep["url"], method=ep["method"],
                                   auth_header=auth_header, body=body)
                obs["state"] = state
                obs["rep"] = rep
                obs["fingerprint"] = fingerprint(obs)
                raw_observations[state].append(obs)
                fingerprints_by_state[state].append(obs["fingerprint"])
            except Exception as e:
                errors.append({"endpoint": ep_name, "state": state, "rep": rep, "error": str(e)})

            # Inter-request jitter
            if i < len(plan) - 1:
                jitter = rng.uniform(0, 0.2)
                time.sleep(jitter)

        # Compute discrimination
        disc_score = compute_discrimination_score(fingerprints_by_state)

        # Compute baselines
        url = ep["url"]
        b_url_fps = baseline_url_hash(url, n=REPS)
        b_url_by_state = {s: b_url_fps for s in auth_states}
        b_url_disc = compute_discrimination_score(b_url_by_state)

        b_rand_fps = baseline_random(n=REPS * len(auth_states))
        b_rand_by_state = {}
        idx = 0
        for s in auth_states:
            b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
            idx += REPS
        b_rand_disc = compute_discrimination_score(b_rand_by_state)

        # B-BODY-ONLY
        b_body_by_state = {}
        for state, obs_list in raw_observations.items():
            fps = [hashlib.sha256(obs["body"]).hexdigest() for obs in obs_list]
            b_body_by_state[state] = fps
        b_body_disc = compute_discrimination_score(b_body_by_state)

        # B-STATUS-ONLY
        b_status_by_state = {}
        for state, obs_list in raw_observations.items():
            fps = [hashlib.sha256(str(obs["status"]).encode()).hexdigest() for obs in obs_list]
            b_status_by_state[state] = fps
        b_status_disc = compute_discrimination_score(b_status_by_state)

        # WWW-Authenticate-only discrimination
        www_auth_disc = compute_single_header_discrimination(
            fingerprints_by_state, "WWW-Authenticate", raw_observations
        )

        # Cache-Control-only discrimination
        cc_disc = compute_single_header_discrimination(
            fingerprints_by_state, "Cache-Control", raw_observations
        )

        # Null FP rate
        total_requests = sum(len(v) for v in raw_observations.values())
        null_results = {}
        for state in auth_states:
            fps = fingerprints_by_state[state]
            unique = len(set(fps))
            total = len(fps)
            fp_rate = (unique - 1) / (total - 1) if total > 1 else 0.0
            null_results[state] = {"total": total, "unique": unique, "fp_rate": fp_rate}

        total_pairs = sum(max(r["total"] * (r["total"] - 1) // 2, 0) for r in null_results.values())
        total_diff_pairs = sum(
            max((r["unique"] - 1) * r["total"] // 2, 0) for r in null_results.values()
        ) if total_pairs > 0 else 0
        overall_fp_rate = total_diff_pairs / total_pairs if total_pairs > 0 else 0

        # Body identity: expired vs invalid
        body_hashes_by_state = {}
        for state, obs_list in raw_observations.items():
            body_hashes_by_state[state] = list(set(
                hashlib.sha256(obs["body"]).hexdigest() for obs in obs_list
            ))

        expired_invalid_identical = (
            len(body_hashes_by_state.get("expired_token", [])) >= 1
            and len(body_hashes_by_state.get("invalid_token", [])) >= 1
            and body_hashes_by_state["expired_token"][0] == body_hashes_by_state["invalid_token"][0]
        )

        # Drift: expired vs invalid
        expired_fps = fingerprints_by_state["expired_token"]
        invalid_fps = fingerprints_by_state["invalid_token"]
        drift_ei_jaccards = [jaccard_similarity(f1, f2) for f1 in expired_fps for f2 in invalid_fps]
        mean_drift_ei = sum(drift_ei_jaccards) / len(drift_ei_jaccards) if drift_ei_jaccards else 0

        # WWW-Authenticate verification
        www_auth_verification = {}
        for state in auth_states:
            obs_list = raw_observations[state]
            wa_vals = [obs["headers"].get("WWW-Authenticate", "(absent)") for obs in obs_list]
            www_auth_verification[state] = {
                "observed_values": list(set(wa_vals)),
                "consistent": len(set(wa_vals)) == 1,
            }

        # Cache-Control verification
        cc_verification = {}
        for state in auth_states:
            obs_list = raw_observations[state]
            cc_vals = [obs["headers"].get("Cache-Control", "(absent)") for obs in obs_list]
            cc_verification[state] = {
                "observed_values": list(set(cc_vals)),
                "consistent": len(set(cc_vals)) == 1,
            }

        endpoint_results[ep_name] = {
            "full_vector_discrimination": disc_score,
            "www_auth_only_discrimination": www_auth_disc,
            "cache_control_only_discrimination": cc_disc,
            "baselines": {
                "B-STATUS-ONLY": b_status_disc,
                "B-BODY-ONLY": b_body_disc,
                "B-URL-HASH": b_url_disc,
                "B-RANDOM": b_rand_disc,
            },
            "null_fp_rate": overall_fp_rate,
            "expired_invalid_identical": expired_invalid_identical,
            "drift_expired_invalid_jaccard": mean_drift_ei,
            "www_auth_verification": www_auth_verification,
            "cc_verification": cc_verification,
            "body_hashes_by_state": body_hashes_by_state,
            "total_requests": total_requests,
        }

        raw_observations_all[ep_name] = raw_observations

        print(f"\n--- Results for {ep_name} ---")
        print(f"Full-vector discrimination: {disc_score:.6f}")
        print(f"WWW-Authenticate-only: {www_auth_disc:.6f}")
        print(f"B-BODY-ONLY: {b_body_disc:.6f}")
        print(f"B-STATUS-ONLY: {b_status_disc:.6f}")
        print(f"Cache-Control-only: {cc_disc:.6f}")
        print(f"Null FP rate: {overall_fp_rate:.1%}")
        print(f"expired == invalid body: {expired_invalid_identical}")
        print(f"expired vs invalid Jaccard: {mean_drift_ei:.4f}")
        print(f"WWW-Authenticate verification: {json.dumps(www_auth_verification)}")

    # Step 7: Stop Keycloak
    stop_keycloak()

    # Step 8: Apply decision rule
    # Count additional endpoints (excluding /userinfo) where www_auth_disc > 0
    additional_endpoints = [ep["name"] for ep in endpoints if ep["name"] != "/userinfo (GET)"]
    www_auth_positive_count = sum(
        1 for ep_name in additional_endpoints
        if endpoint_results[ep_name]["www_auth_only_discrimination"] > 0
    )

    # Check positive control (userinfo)
    userinfo_www_auth = endpoint_results["/userinfo (GET)"]["www_auth_only_discrimination"]
    positive_control_pass = userinfo_www_auth > 0

    # Check null control
    all_null_fp_ok = all(
        endpoint_results[ep_name]["null_fp_rate"] < 0.05
        for ep_name in endpoint_results
    )

    # Check full-vector discrimination on additional endpoints
    full_vector_positive_count = sum(
        1 for ep_name in additional_endpoints
        if endpoint_results[ep_name]["full_vector_discrimination"] > 0.5
    )

    # Decision
    if (www_auth_positive_count >= 2
        and full_vector_positive_count >= 2
        and all_null_fp_ok
        and positive_control_pass):
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif www_auth_positive_count == 0 and full_vector_positive_count == 0:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not positive_control_pass:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not all_null_fp_ok:
        outcome = "MEASUREMENT_INVALID"
        status = "MEASUREMENT_INVALID"
    else:
        outcome = "MIXED"
        status = "COMPLETE"

    print(f"\n{'='*60}")
    print(f"FINAL DECISION")
    print(f"{'='*60}")
    print(f"WWW-Authenticate positive on {www_auth_positive_count}/3 additional endpoints")
    print(f"Full-vector > 0.5 on {full_vector_positive_count}/3 additional endpoints")
    print(f"Positive control (userinfo): {positive_control_pass}")
    print(f"Null FP rate OK: {all_null_fp_ok}")
    print(f"Status: {status}")
    print(f"Outcome: {outcome}")

    # Build observations
    observations = [
        f"Keycloak 25.0 deployed via Docker on localhost:{KEYCLOAK_PORT}",
        f"Realm '{REALM_NAME}' configured with client '{CLIENT_ID}'",
        f"4 endpoints tested: /userinfo, /token (password), /token (client_credentials), /introspect",
        f"4 auth states x {REPS} reps = {REPS * 4} requests per endpoint = {REPS * 4 * 4} total",
        f"Seed: {SEED}",
        f"Headers filtered: Date/Server/X-Request-Id excluded",
        f"WWW-Authenticate positive on {www_auth_positive_count}/3 additional endpoints",
        f"Full-vector > 0.5 on {full_vector_positive_count}/3 additional endpoints",
    ]

    # Per-endpoint observations
    for ep_name, results in endpoint_results.items():
        observations.append(
            f"{ep_name}: full={results['full_vector_discrimination']:.4f}, "
            f"www_auth={results['www_auth_only_discrimination']:.4f}, "
            f"body={results['baselines']['B-BODY-ONLY']:.4f}, "
            f"null_fp={results['null_fp_rate']:.1%}"
        )

    # Validity notes
    validity_notes = [
        "Same Keycloak 25.0 Docker deployment as parent experiment",
        "Same fingerprint algorithm: SHA-256(repr((status, tuple(sorted(filtered_headers.items())), body_sha256, redirect_chain)))",
        "Date/Server/X-Request-Id excluded from fingerprint",
        f"Python version: {sys.version}",
        "Natural network jitter (no synthetic jitter applied)",
        "expired_token is locally-signed HS256, not truly Keycloak-issued (same as parent)",
        "Keycloak may ignore Authorization header for /token endpoints (credentials in form body)",
        "introspect returns JSON with active:true/false regardless of Authorization header",
    ]

    # Unresolved
    unresolved = [
        "Does WWW-Authenticate discrimination transfer to other OAuth/OIDC providers (Auth0, Okta)?",
        "Does substrate maintain discrimination on production infrastructure with CDN/load-balancer?",
        "What happens on Keycloak /token endpoint when Authorization header is actually enforced?",
        "Cross-Python-version reproducibility of repr(vector) fingerprints?",
    ]

    # Build metrics
    metrics = {}
    for ep_name, results in endpoint_results.items():
        metrics[ep_name] = {
            "full_vector_discrimination": results["full_vector_discrimination"],
            "www_auth_only_discrimination": results["www_auth_only_discrimination"],
            "cache_control_only_discrimination": results["cache_control_only_discrimination"],
            "baselines": results["baselines"],
            "null_fp_rate": results["null_fp_rate"],
            "expired_invalid_identical": results["expired_invalid_identical"],
            "drift_expired_invalid_jaccard": results["drift_expired_invalid_jaccard"],
            "www_auth_verification": results["www_auth_verification"],
            "cc_verification": results["cc_verification"],
        }

    # Build controls
    controls = {
        "C_POSITIVE_CONTROL_USERINFO": {
            "expected": "WWW-Authenticate-only discrimination > 0 on /userinfo",
            "observed": f"{userinfo_www_auth:.6f}",
            "pass": positive_control_pass,
        },
        "C_NULL_FP_RATE": {
            "expected": "< 5% on all endpoints",
            "observed": {ep: f"{results['null_fp_rate']:.1%}" for ep, results in endpoint_results.items()},
            "pass": all_null_fp_ok,
        },
        "C_WWW_AUTH_TRANSFER": {
            "expected": "WWW-Authenticate-only discrimination > 0 on >= 2 of 3 additional endpoints",
            "observed": f"{www_auth_positive_count}/3 positive",
            "pass": www_auth_positive_count >= 2,
        },
        "C_FULL_VECTOR_TRANSFER": {
            "expected": "Full-vector discrimination > 0.5 on >= 2 of 3 additional endpoints",
            "observed": f"{full_vector_positive_count}/3 positive",
            "pass": full_vector_positive_count >= 2,
        },
        "C_BODY_IDENTITY_EXPIRED_INVALID": {
            "expected": "expired_token and invalid_token identical body hash on all endpoints",
            "observed": {ep: str(results["expired_invalid_identical"]) for ep, results in endpoint_results.items()},
            "pass": all(results["expired_invalid_identical"] for results in endpoint_results.values()),
        },
    }

    # Build artifacts
    artifacts = []
    for ep_name, results in endpoint_results.items():
        artifacts.append({
            "role": "derived",
            "description": f"{ep_name} results",
        })

    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    # Save raw observations
    raw_obs_path = "raw_observations.json"
    raw_obs_serializable = {}
    for ep_name, obs_dict in raw_observations_all.items():
        raw_obs_serializable[ep_name] = {}
        for state, obs_list in obs_dict.items():
            raw_obs_serializable[ep_name][state] = []
            for obs in obs_list:
                raw_obs_serializable[ep_name][state].append({
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

    return result


def build_blocked_result(reason):
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": "BLOCKED",
        "outcome": "NOT_APPLICABLE",
        "metrics": {},
        "controls": {},
        "artifacts": [],
        "observations": [f"Infrastructure failure: {reason}"],
        "validity_notes": [f"BLOCKED: {reason}. This is infrastructure failure, not scientific falsification."],
        "unresolved": [f"What specific action would unblock this experiment? Fix: {reason}"],
    }


if __name__ == "__main__":
    result = run_experiment()

    # Write result.json
    with open("result.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult written to result.json")
    print(f"Status: {result['status']}, Outcome: {result['outcome']}")
