#!/usr/bin/env python3
"""
EXP-RUNTIME-34509593940 — Body-Only vs Full-Vector Under Header Noise
=====================================================================
Tests whether body-only HTTP fingerprint discrimination maintains stability
when a reverse proxy adds non-deterministic CDN/load-balancer/rate-limit
headers, while full-vector discrimination degrades.

Frozen from spec.json and prereg.md — DO NOT MODIFY.
"""

import hashlib
import json
import os
import random
import socket
import subprocess
import sys
import time
import threading
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

import jwt
import requests
import numpy as np
from scipy.stats import spearmanr


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that handles numpy types."""
    def default(self, obj):
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

# ---------------------------------------------------------------------------
# FROZEN CONSTANTS
# ---------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-RUNTIME-34509593940"
LANE = "runtime"
SEED = 44
REPS = 10
KEYCLOAK_PORT = 18080
PROXY_PORT = 18081
REALM_NAME = "spider-test"
CLIENT_ID = "spider-client"
CLIENT_SECRET = "spider-secret-12345"
ADMIN_USER = "admin"
ADMIN_PASS = "admin"

EXCLUDED_HEADERS = {"date", "server", "x-request-id"}

# Noise levels: number of injected headers
NOISE_LEVELS = [0, 1, 2, 4]

# Noise header pools
NOISE_HEADERS_POOL = {
    "X-Cache-Status": ["HIT", "MISS", "EXPIRED"],
    "X-CDN-Request-Id": "uuid4",  # generated dynamically
    "X-Edge-Location": ["US", "EU", "AP", "SA", "AF"],
    "X-Rate-Limit-Remaining": "int0-100",  # generated dynamically
}

# Headers the proxy must NOT modify
AUTH_RELATED_HEADERS = {"cache-control", "www-authenticate", "set-cookie", "content-type"}

# Endpoint definitions (via proxy)
USERINFO_PATH = "/realms/spider-test/protocol/openid-connect/userinfo"
INTROSPECT_PATH = "/realms/spider-test/protocol/openid-connect/token/introspect"
TOKEN_PATH = "/realms/spider-test/protocol/openid-connect/token"

# ---------------------------------------------------------------------------
# TOKEN GENERATION
# ---------------------------------------------------------------------------

def get_keycloak_token(username="alice", password="alice123"):
    """Get access token from Keycloak via direct access grant."""
    try:
        r = requests.post(
            f"http://127.0.0.1:{KEYCLOAK_PORT}/{TOKEN_PATH.lstrip('/')}",
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
# REVERSE PROXY WITH NOISE INJECTION
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    """HTTPServer with SO_REUSEADDR."""
    allow_reuse_address = True
    allow_reuse_port = True


class NoiseProxyHandler(BaseHTTPRequestHandler):
    """HTTP handler that proxies requests to Keycloak and adds noise headers."""

    noise_level = 0  # class-level, set before server starts
    rng = random.Random(SEED)

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def do_request(self):
        """Forward request to Keycloak, add noise headers to response."""
        # Build target URL
        target_url = f"http://127.0.0.1:{KEYCLOAK_PORT}{self.path}"

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Forward request
        headers = {}
        for key in self.headers:
            if key.lower() not in ("host", "transfer-encoding"):
                headers[key] = self.headers[key]

        try:
            if self.command == "GET":
                resp = requests.get(target_url, headers=headers, timeout=10, allow_redirects=False)
            elif self.command == "POST":
                resp = requests.post(target_url, headers=headers, data=body, timeout=10, allow_redirects=False)
            elif self.command == "PUT":
                resp = requests.put(target_url, headers=headers, data=body, timeout=10, allow_redirects=False)
            elif self.command == "DELETE":
                resp = requests.delete(target_url, headers=headers, timeout=10, allow_redirects=False)
            else:
                self.send_error(501, "Not Implemented")
                return
        except Exception as e:
            self.send_error(502, f"Bad Gateway: {e}")
            return

        # Send response status
        self.send_response(resp.status_code)

        # Copy response headers, add noise
        for key, value in resp.headers.items():
            if key.lower() in ("transfer-encoding", "connection"):
                continue
            self.send_header(key, value)

        # Inject noise headers (only non-auth-related)
        if self.noise_level > 0:
            noise_headers = self._generate_noise_headers(self.noise_level)
            for key, value in noise_headers.items():
                self.send_header(key, value)

        self.end_headers()

        # Forward response body
        self.wfile.write(resp.content)

    def _generate_noise_headers(self, level):
        """Generate noise headers based on level."""
        headers = {}
        pool = [
            ("X-Cache-Status", lambda: self.rng.choice(["HIT", "MISS", "EXPIRED"])),
            ("X-CDN-Request-Id", lambda: str(self.rng.uuid4()) if hasattr(self.rng, 'uuid4') else hashlib.md5(str(self.rng.random()).encode()).hexdigest()),
            ("X-Edge-Location", lambda: self.rng.choice(["US", "EU", "AP", "SA", "AF"])),
            ("X-Rate-Limit-Remaining", lambda: str(self.rng.randint(0, 100))),
        ]
        for i in range(min(level, len(pool))):
            name, gen = pool[i]
            headers[name] = gen()
        return headers

    def do_GET(self):
        self.do_request()

    def do_POST(self):
        self.do_request()

    def do_PUT(self):
        self.do_request()

    def do_DELETE(self):
        self.do_request()


def start_proxy(noise_level):
    """Start the noise injection proxy on PROXY_PORT."""
    NoiseProxyHandler.noise_level = noise_level
    NoiseProxyHandler.rng = random.Random(SEED)  # deterministic per noise level

    server = ReusableHTTPServer(("127.0.0.1", PROXY_PORT), NoiseProxyHandler)
    server.timeout = 0.5  # allow graceful shutdown

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Proxy started on port {PROXY_PORT} with noise_level={noise_level}")
    return server


def stop_proxy(server):
    """Stop the proxy server."""
    if server:
        server.shutdown()
        print("Proxy stopped.")


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

def fingerprint_full_vector(observation):
    """Full-vector fingerprint: SHA-256 of (status, filtered_headers, body_hash, redirect)."""
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


def fingerprint_body_only(observation):
    """Body-only fingerprint: SHA-256 of (status, body_hash, '')."""
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
    vector = (
        observation["status"],
        body_hash,
        '',
    )
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# DISCRIMINATION SCORE
# ---------------------------------------------------------------------------

def compute_discrimination_score(fingerprints_by_state):
    """Compute discrimination = intra_match_rate - inter_match_rate."""
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
# BASELINES
# ---------------------------------------------------------------------------

def baseline_random(n=10, seed=99):
    """Random fingerprint baseline."""
    rng = random.Random(seed)
    return [hashlib.sha256(rng.getrandbits(256).to_bytes(32, "big")).hexdigest()
            for _ in range(n)]


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
# ENDPOINT DEFINITIONS
# ---------------------------------------------------------------------------

def get_endpoint_configs(auth_token, proxy_port):
    """Return endpoint configurations via proxy."""
    expired_token = make_expired_token()
    invalid_token = make_invalid_token()

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

    def introspect_expected_status(state):
        return 200

    return [
        {
            "name": "/userinfo",
            "url": f"http://127.0.0.1:{proxy_port}/{USERINFO_PATH.lstrip('/')}",
            "method": "GET",
            "body_fn": lambda state: None,
            "expected_status_fn": userinfo_expected_status,
        },
        {
            "name": "/introspect",
            "url": f"http://127.0.0.1:{proxy_port}/{INTROSPECT_PATH.lstrip('/')}",
            "method": "POST",
            "body_fn": introspect_body,
            "expected_status_fn": introspect_expected_status,
        },
    ]


# ---------------------------------------------------------------------------
# MAIN EXPERIMENT
# ---------------------------------------------------------------------------

def run_experiment():
    """Run the full noise-injection experiment."""
    raw_observations_all = {}  # noise_level -> endpoint -> state -> [obs]
    all_results = {}
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

    # Step 5: Run experiment for each noise level
    auth_states = ["no_auth", "valid_token", "expired_token", "invalid_token"]

    for noise_level in NOISE_LEVELS:
        print(f"\n{'='*60}")
        print(f"NOISE LEVEL: {noise_level}")
        print(f"{'='*60}")

        # Start proxy with this noise level
        proxy = start_proxy(noise_level)
        time.sleep(0.5)  # let proxy bind

        # Get endpoint configs for this proxy
        endpoints = get_endpoint_configs(auth_token, PROXY_PORT)

        noise_results = {}
        noise_raw_obs = {}

        for ep in endpoints:
            ep_name = ep["name"]
            print(f"\n  Endpoint: {ep_name}")

            # Build plan: 4 states x 10 reps
            rng = random.Random(SEED + noise_level)
            plan = []
            for state in auth_states:
                for rep in range(REPS):
                    plan.append((state, rep))
            rng.shuffle(plan)

            raw_observations = defaultdict(list)
            fingerprints_full_by_state = defaultdict(list)
            fingerprints_body_by_state = defaultdict(list)

            for i, (state, rep) in enumerate(plan):
                auth_header = get_auth_header(state, auth_token)
                body = ep["body_fn"](state)

                try:
                    obs = make_request(ep["url"], method=ep["method"],
                                       auth_header=auth_header, body=body)
                    obs["state"] = state
                    obs["rep"] = rep
                    obs["fingerprint_full"] = fingerprint_full_vector(obs)
                    obs["fingerprint_body"] = fingerprint_body_only(obs)
                    raw_observations[state].append(obs)
                    fingerprints_full_by_state[state].append(obs["fingerprint_full"])
                    fingerprints_body_by_state[state].append(obs["fingerprint_body"])
                except Exception as e:
                    errors.append({"noise_level": noise_level, "endpoint": ep_name,
                                   "state": state, "rep": rep, "error": str(e)})

                # Inter-request jitter
                if i < len(plan) - 1:
                    jitter = rng.uniform(0.05, 0.15)
                    time.sleep(jitter)

            # Compute discrimination scores
            full_disc = compute_discrimination_score(fingerprints_full_by_state)
            body_disc = compute_discrimination_score(fingerprints_body_by_state)

            # Baselines
            b_rand_fps = baseline_random(n=REPS * len(auth_states))
            b_rand_by_state = {}
            idx = 0
            for s in auth_states:
                b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
                idx += REPS
            b_rand_disc = compute_discrimination_score(b_rand_by_state)

            # Status-only discrimination
            status_fps_by_state = {}
            for state, obs_list in raw_observations.items():
                status_fps_by_state[state] = [
                    hashlib.sha256(str(obs["status"]).encode()).hexdigest()
                    for obs in obs_list
                ]
            status_disc = compute_discrimination_score(status_fps_by_state)

            # Null FP rate
            total_requests = sum(len(v) for v in raw_observations.values())
            null_results = {}
            for state in auth_states:
                fps = fingerprints_full_by_state[state]
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

            # Noise headers verification
            noise_header_verification = {}
            for state in auth_states:
                obs_list = raw_observations[state]
                noise_headers_seen = defaultdict(list)
                for obs in obs_list:
                    for h in ["X-Cache-Status", "X-CDN-Request-Id", "X-Edge-Location", "X-Rate-Limit-Remaining"]:
                        if h in obs["headers"]:
                            noise_headers_seen[h].append(obs["headers"][h])
                noise_header_verification[state] = {
                    h: {"count": len(vals), "unique": len(set(vals))}
                    for h, vals in noise_headers_seen.items()
                }

            ep_key = f"{ep_name}_noise{noise_level}"
            noise_results[ep_key] = {
                "full_vector_discrimination": full_disc,
                "body_only_discrimination": body_disc,
                "status_only_discrimination": status_disc,
                "baselines": {
                    "B-RANDOM": b_rand_disc,
                },
                "null_fp_rate": overall_fp_rate,
                "expired_invalid_identical": expired_invalid_identical,
                "noise_header_verification": noise_header_verification,
                "total_requests": total_requests,
            }
            noise_raw_obs[ep_name] = raw_observations

            print(f"    Full-vector: {full_disc:.6f}, Body-only: {body_disc:.6f}, "
                  f"Status-only: {status_disc:.6f}, B-RANDOM: {b_rand_disc:.6f}, "
                  f"Null FP: {overall_fp_rate:.1%}")

        raw_observations_all[noise_level] = noise_raw_obs
        all_results[noise_level] = noise_results

        # Stop proxy
        stop_proxy(proxy)
        time.sleep(1.0)  # ensure port is fully released

    # Step 6: Stop Keycloak
    stop_keycloak()

    # Step 7: Assemble metrics
    metrics = {}
    for noise_level in NOISE_LEVELS:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_noise{noise_level}"
            if key in all_results[noise_level]:
                metrics[key] = all_results[noise_level][key]

    # Step 8: Compute primary derived metrics for /userinfo
    userinfo_fv_discs = []
    userinfo_bo_discs = []
    for nl in NOISE_LEVELS:
        key = f"/userinfo_noise{nl}"
        if key in metrics:
            userinfo_fv_discs.append(metrics[key]["full_vector_discrimination"])
            userinfo_bo_discs.append(metrics[key]["body_only_discrimination"])

    # Spearman correlation: full-vector disc vs noise level
    if len(userinfo_fv_discs) == len(NOISE_LEVELS):
        rho_fv, pval_fv = spearmanr(NOISE_LEVELS, userinfo_fv_discs)
    else:
        rho_fv, pval_fv = 0.0, 1.0

    # Spearman correlation: body-only disc vs noise level
    if len(userinfo_bo_discs) == len(NOISE_LEVELS):
        # Check if constant (all same value)
        if len(set(userinfo_bo_discs)) == 1:
            rho_bo, pval_bo = 0.0, 1.0  # undefined for constant; report 0 with high p
        else:
            rho_bo, pval_bo = spearmanr(NOISE_LEVELS, userinfo_bo_discs)
    else:
        rho_bo, pval_bo = 0.0, 1.0

    # Noise-invariance bound
    if len(userinfo_bo_discs) >= 2:
        noise_bound = abs(userinfo_bo_discs[-1] - userinfo_bo_discs[0])
    else:
        noise_bound = None

    # Positive control: body-only at noise=0 on /userinfo
    positive_control_value = userinfo_bo_discs[0] if userinfo_bo_discs else None

    # Null control: B-RANDOM at noise=0
    null_control_value = metrics.get("/userinfo_noise0", {}).get("baselines", {}).get("B-RANDOM", None)

    # Add derived metrics
    metrics["M_NOISE_DEGRADATION"] = {"rho": rho_fv, "p_value": pval_fv, "description": "Spearman rho: full-vector discrimination vs noise level on /userinfo"}
    metrics["M_BODY_ONLY_INVARIANT"] = {"rho": rho_bo, "p_value": pval_bo, "description": "Spearman rho: body-only discrimination vs noise level on /userinfo"}
    metrics["M_NOISE_BOUND"] = {"value": noise_bound, "threshold": 0.05, "description": "|body_only(noise=4) - body_only(noise=0)| on /userinfo"}
    metrics["M_POSITIVE_CONTROL"] = {"value": positive_control_value, "threshold": 0.35, "description": "Body-only discrimination at noise=0 on /userinfo"}
    metrics["M_NULL_CONTROL"] = {"value": null_control_value, "threshold": "~0.0", "description": "B-RANDOM discrimination at noise=0 on /userinfo"}

    # Step 9: Evaluate controls and decision rule
    control_pass = True
    control_details = {}

    # C1: Positive control
    c1_pass = positive_control_value is not None and positive_control_value >= 0.35
    control_details["C_POSITIVE_CONTROL"] = {
        "expected": "M_BODY_ONLY_DISC_NOISE0 >= 0.35",
        "observed": positive_control_value,
        "pass": c1_pass,
    }
    if not c1_pass:
        control_pass = False

    # C2: Null control
    c2_pass = null_control_value is not None and abs(null_control_value) < 0.1
    control_details["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0",
        "observed": null_control_value,
        "pass": c2_pass,
    }
    if not c2_pass:
        control_pass = False

    # C3: Full-vector degradation
    c3_pass = rho_fv <= -0.3
    control_details["C_NOISE_DEGRADATION"] = {
        "expected": "Spearman rho(FULL_VECTOR_DISC, noise) <= -0.3",
        "observed": rho_fv,
        "pass": c3_pass,
    }
    if not c3_pass:
        control_pass = False

    # C4: Body-only invariance
    c4_pass = rho_bo >= -0.3
    control_details["C_BODY_ONLY_INVARIANT"] = {
        "expected": "Spearman rho(BODY_ONLY_DISC, noise) >= -0.3",
        "observed": rho_bo,
        "pass": c4_pass,
    }
    if not c4_pass:
        control_pass = False

    # C5: Noise-invariance bound
    c5_pass = noise_bound is not None and noise_bound <= 0.05
    control_details["C_NOISE_BOUND"] = {
        "expected": "|body_only(noise=4) - body_only(noise=0)| <= 0.05",
        "observed": noise_bound,
        "pass": c5_pass,
    }
    if not c5_pass:
        control_pass = False

    # C6: No pipeline errors
    c6_pass = len(errors) == 0
    control_details["C_NO_PIPELINE_ERRORS"] = {
        "expected": "0 errors",
        "observed": len(errors),
        "pass": c6_pass,
    }
    if not c6_pass:
        control_pass = False

    # Decision rule
    if control_pass:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif not c3_pass and c4_pass and c5_pass:
        # Full-vector does NOT degrade — body-only offers no advantage
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not c4_pass or not c5_pass:
        # Body-only degrades — proxy modifying bodies
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif not c1_pass or not c2_pass:
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    else:
        outcome = "MIXED"
        status = "COMPLETE"

    # Observations
    observations = [
        f"Keycloak 25.0 deployed via Docker on localhost:{KEYCLOAK_PORT}",
        f"Reverse proxy on localhost:{PROXY_PORT} with noise levels {NOISE_LEVELS}",
        f"2 endpoints: /userinfo (GET), /introspect (POST)",
        f"4 auth states x {REPS} reps x {len(NOISE_LEVELS)} noise levels x 2 endpoints = {4 * REPS * len(NOISE_LEVELS) * 2} total requests",
        f"Seed: {SEED}",
        f"Noise headers: X-Cache-Status, X-CDN-Request-Id, X-Edge-Location, X-Rate-Limit-Remaining",
        f"Proxy preserves: body, status code, auth-related headers",
    ]

    # Per-noise-level per-endpoint observations
    for nl in NOISE_LEVELS:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_noise{nl}"
            if key in metrics:
                observations.append(
                    f"noise={nl} {ep_name}: full={metrics[key]['full_vector_discrimination']:.4f}, "
                    f"body={metrics[key]['body_only_discrimination']:.4f}, "
                    f"status={metrics[key]['status_only_discrimination']:.4f}, "
                    f"B-RANDOM={metrics[key]['baselines']['B-RANDOM']:.4f}"
                )

    observations.append(f"Full-vector Spearman rho vs noise: {rho_fv:.4f} (p={pval_fv:.4f})")
    observations.append(f"Body-only Spearman rho vs noise: {rho_bo:.4f} (p={pval_bo:.4f})")
    observations.append(f"Noise-invariance bound: {noise_bound:.4f}" if noise_bound is not None else "Noise-invariance bound: N/A")

    # Validity notes
    validity_notes = [
        "Same Keycloak 25.0 Docker deployment as parent experiments",
        "Same fingerprint algorithm as parent EXP-RUNTIME-34439061845",
        "EXCLUDED_HEADERS: date, server, x-request-id — same as parent",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "expired_token is locally-signed HS256, not Keycloak-issued (V6 leakage from parent)",
        "Proxy adds only infrastructure-irrelevant headers (not auth-related)",
        "Body-only invariance is tautological by construction (headers excluded from fingerprint)",
        "Single noise pattern tested — real production may have multiple infrastructure layers",
    ]

    if errors:
        validity_notes.append(f"Pipeline errors: {len(errors)} requests failed")
        for e in errors[:5]:
            validity_notes.append(f"  Error: {e}")

    # Unresolved
    unresolved = [
        "Does body-only discrimination survive CDN compression (body non-determinism)?",
        "Does body-only discrimination survive multiple stacked infrastructure layers?",
        "Does the result generalize to non-Keycloak OAuth/OIDC providers?",
        "What is the discrimination floor when bodies are compressed non-deterministically?",
    ]

    # Build result
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": control_details,
        "artifacts": [
            {"path": "raw_observations.json", "role": "raw", "description": "All HTTP observations per noise level per endpoint per state"},
            {"path": "run_experiment.py", "role": "code", "description": "Frozen experiment execution script"},
        ],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    # Save raw observations
    raw_obs_serializable = {}
    for nl, endpoint_obs in raw_observations_all.items():
        raw_obs_serializable[str(nl)] = {}
        for ep_name, state_obs in endpoint_obs.items():
            raw_obs_serializable[str(nl)][ep_name] = {}
            for state, obs_list in state_obs.items():
                raw_obs_serializable[str(nl)][ep_name][state] = []
                for obs in obs_list:
                    raw_obs_serializable[str(nl)][ep_name][state].append({
                        "url": obs["url"],
                        "status": obs["status"],
                        "headers": obs["headers"],
                        "body_hash": hashlib.sha256(obs["body"]).hexdigest(),
                        "body_preview": obs["body"][:500].decode("utf-8", errors="replace"),
                        "fingerprint_full": obs["fingerprint_full"],
                        "fingerprint_body": obs["fingerprint_body"],
                        "elapsed": obs["elapsed"],
                        "timestamp": obs["timestamp"],
                        "state": obs["state"],
                        "rep": obs["rep"],
                    })

    with open("raw_observations.json", "w") as f:
        json.dump(raw_obs_serializable, f, indent=2)
    print(f"\nRaw observations saved to raw_observations.json")

    return result


def build_blocked_result(reason):
    """Build a BLOCKED result for infrastructure failure."""
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
        json.dump(result, f, indent=2, cls=NumpyEncoder)
    print(f"\nResult written to result.json")
    print(f"Status: {result['status']}, Outcome: {result['outcome']}")
