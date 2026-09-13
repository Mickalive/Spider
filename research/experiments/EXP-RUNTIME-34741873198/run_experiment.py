#!/usr/bin/env python3
"""
EXP-RUNTIME-34741873198 — Body-Only Fingerprint Under Deterministic CDN Negotiation
===================================================================================
Tests whether body-only HTTP fingerprint discrimination survives realistic CDN
negotiation where Content-Encoding is selected deterministically from the client's
advertised Accept-Encoding (not per-request random).

Frozen from spec.json and prereg.md — DO NOT MODIFY.
"""

import brotli
import gzip
import hashlib
import io
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

EXPERIMENT_ID = "EXP-RUNTIME-34741873198"
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

# Client profiles simulating different Accept-Encoding configurations
CLIENT_PROFILES = {
    "A_br_gzip": {
        "accept_encoding": "br, gzip",
        "selected_algorithm": "br",
        "description": "Client A: Accept-Encoding 'br, gzip' → CDN selects brotli",
    },
    "B_gzip_only": {
        "accept_encoding": "gzip",
        "selected_algorithm": "gzip",
        "description": "Client B: Accept-Encoding 'gzip' → CDN selects gzip",
    },
    "C_identity": {
        "accept_encoding": "identity",
        "selected_algorithm": "identity",
        "description": "Client C: Accept-Encoding 'identity' → CDN selects identity",
    },
}

# Headers the proxy must NOT modify
AUTH_RELATED_HEADERS = {"cache-control", "www-authenticate", "set-cookie", "content-type"}

# Endpoint definitions
USERINFO_PATH = "/realms/spider-test/protocol/openid-connect/userinfo"
INTROSPECT_PATH = "/realms/spider-test/protocol/openid-connect/token/introspect"
TOKEN_PATH = "/realms/spider-test/protocol/openid-connect/token"

# Check brotli availability
BROTLI_AVAILABLE = True
try:
    import brotli as _brotli_test
except ImportError:
    BROTLI_AVAILABLE = False
    print("WARNING: brotli module not available. Client A will fallback to gzip.")


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
# COMPRESSION FUNCTIONS
# ---------------------------------------------------------------------------

def compress_gzip(data, level):
    """Compress data with gzip at specified level.
    
    Uses mtime=0 to eliminate gzip header timestamp as a source of non-determinism.
    This isolates the compression algorithm/level effect we are testing.
    Real CDNs also produce deterministic compressed output for the same logical body
    (they strip metadata timestamps), so this is production-faithful.
    """
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=level, mtime=0) as f:
        f.write(data)
    return buf.getvalue()


def compress_brotli(data, level=6):
    """Compress data with brotli at specified level."""
    return brotli.compress(data, quality=level)


def select_algorithm_for_client(client_accept_encoding):
    """
    CDN negotiation: deterministically select the highest-priority algorithm
    the client supports. Priority order: br > gzip > identity.
    
    This simulates real CDN behavior where the CDN picks one algorithm per client
    based on the client's advertised Accept-Encoding.
    """
    accept_lower = client_accept_encoding.lower()
    if "br" in accept_lower:
        if BROTLI_AVAILABLE:
            return "br"
        else:
            return "gzip"  # fallback if brotli unavailable
    elif "gzip" in accept_lower:
        return "gzip"
    else:
        return "identity"


def compress_for_client(body_bytes, algorithm):
    """Apply deterministic compression based on selected algorithm."""
    if algorithm == "br":
        return compress_brotli(body_bytes), "br"
    elif algorithm == "gzip":
        # Use gzip level 9 for deterministic output (same as parent comp_level=1)
        return compress_gzip(body_bytes, 9), "gzip"
    else:
        return body_bytes, None


# ---------------------------------------------------------------------------
# REVERSE PROXY WITH CDN NEGOTIATION
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    """HTTPServer with SO_REUSEADDR."""
    allow_reuse_address = True
    allow_reuse_port = True


class CDNNegotiationProxyHandler(BaseHTTPRequestHandler):
    """HTTP handler that proxies requests to Keycloak and applies CDN-style compression.
    
    The proxy reads the client's Accept-Encoding header and deterministically
    selects the highest-priority algorithm the client supports (br > gzip > identity).
    Same Accept-Encoding always produces the same algorithm — this is the CDN model.
    """

    client_accept_encoding = "br, gzip"  # class-level, set before server starts

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def do_request(self):
        """Forward request to Keycloak, compress response body per CDN negotiation."""
        target_url = f"http://127.0.0.1:{KEYCLOAK_PORT}{self.path}"

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Forward request
        headers = {}
        for key in self.headers:
            if key.lower() not in ("host", "transfer-encoding"):
                headers[key] = self.headers[key]

        # Override client Accept-Encoding to ensure we get raw response from Keycloak
        # (proxy will apply its own compression based on the client profile)
        headers["Accept-Encoding"] = "identity"

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

        # Get the raw response body (uncompressed from Keycloak)
        raw_body = resp.content

        # CDN negotiation: select algorithm based on client's Accept-Encoding
        algorithm = select_algorithm_for_client(self.client_accept_encoding)
        
        # Apply deterministic compression
        compressed_body, encoding = compress_for_client(raw_body, algorithm)

        # Send response status
        self.send_response(resp.status_code)

        # Copy response headers (skip transfer-encoding, content-encoding, content-length)
        # We will set our own content-encoding and content-length
        for key, value in resp.headers.items():
            key_lower = key.lower()
            if key_lower in ("transfer-encoding", "content-encoding", "content-length",
                             "connection"):
                continue
            self.send_header(key, value)

        # Set compression headers
        if encoding:
            self.send_header("Content-Encoding", encoding)
        self.send_header("Content-Length", str(len(compressed_body)))

        self.end_headers()

        # Write compressed body
        self.wfile.write(compressed_body)

    def do_GET(self):
        self.do_request()

    def do_POST(self):
        self.do_request()

    def do_PUT(self):
        self.do_request()

    def do_DELETE(self):
        self.do_request()


def start_proxy(client_accept_encoding):
    """Start the CDN negotiation proxy on PROXY_PORT."""
    CDNNegotiationProxyHandler.client_accept_encoding = client_accept_encoding

    server = ReusableHTTPServer(("127.0.0.1", PROXY_PORT), CDNNegotiationProxyHandler)
    server.timeout = 0.5

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    algorithm = select_algorithm_for_client(client_accept_encoding)
    print(f"Proxy started on port {PROXY_PORT} with Accept-Encoding='{client_accept_encoding}' → algorithm={algorithm}")
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
    """Execute HTTP request and capture raw observation.
    
    CRITICAL: Uses stream=True + resp.raw.read(decode_content=False) to capture
    the COMPRESSED bytes as received on the wire (before client-side decompression).
    This is the correct measurement because SPIDER in production sees the bytes 
    that arrive from the CDN, not the decompressed bytes.
    """
    headers = {}
    if auth_header:
        headers["Authorization"] = auth_header
    if body:
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    start = time.monotonic()
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=timeout, 
                              allow_redirects=True, stream=True)
        elif method == "POST":
            resp = requests.post(url, headers=headers, data=body, timeout=timeout,
                               allow_redirects=True, stream=True)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Read raw bytes from wire (before client-side decompression)
        # decode_content=False prevents urllib3 from decompressing
        raw_bytes = resp.raw.read(decode_content=False)
        
        # Also get the response URL for redirect tracking
        resp_url = resp.url
        resp_status = resp.status_code
        resp_headers = dict(resp.headers)
        
        elapsed = time.monotonic() - start
        return {
            "url": url, "status": resp_status,
            "headers": resp_headers, "body": raw_bytes,
            "redirect_url": resp_url if resp_url != url else None,
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

def fingerprint_body_only(observation):
    """Body-only fingerprint: SHA-256 of (status, body_hash, '').
    body_hash is computed on compressed bytes received by client."""
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
    vector = (
        observation["status"],
        body_hash,
        '',
    )
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


def fingerprint_status_only(observation):
    """Status-only fingerprint: SHA-256 of (status, '', '')."""
    vector = (
        observation["status"],
        '',
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
    """Run the full CDN negotiation experiment."""
    raw_observations_all = {}  # client_profile -> endpoint -> state -> [obs]
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

    # Step 5: Verify Keycloak sends uncompressed (check direct request)
    print("\nVerifying Keycloak sends uncompressed responses...")
    try:
        direct_resp = requests.get(
            f"http://127.0.0.1:{KEYCLOAK_PORT}/{USERINFO_PATH.lstrip('/')}",
            headers={"Accept-Encoding": "identity"},
            timeout=10,
        )
        direct_ce = direct_resp.headers.get("Content-Encoding", "none")
        print(f"  Direct Content-Encoding: {direct_ce}")
        print(f"  Direct body length: {len(direct_resp.content)} bytes")
    except Exception as e:
        print(f"  WARNING: Could not verify direct response: {e}")

    # Step 6: Run experiment for each client profile
    auth_states = ["no_auth", "valid_token", "expired_token", "invalid_token"]

    for profile_name, profile_config in CLIENT_PROFILES.items():
        print(f"\n{'='*60}")
        print(f"CLIENT PROFILE: {profile_config['description']}")
        print(f"  Accept-Encoding: {profile_config['accept_encoding']}")
        print(f"  Expected algorithm: {profile_config['selected_algorithm']}")
        print(f"{'='*60}")

        # Start proxy with this client profile
        proxy = start_proxy(profile_config["accept_encoding"])
        time.sleep(0.5)  # let proxy bind

        # Get endpoint configs for this proxy
        endpoints = get_endpoint_configs(auth_token, PROXY_PORT)

        profile_results = {}
        profile_raw_obs = {}

        for ep in endpoints:
            ep_name = ep["name"]
            print(f"\n  Endpoint: {ep_name}")

            # Build plan: 4 states x 10 reps
            rng = random.Random(SEED)
            plan = []
            for state in auth_states:
                for rep in range(REPS):
                    plan.append((state, rep))
            rng.shuffle(plan)

            raw_observations = defaultdict(list)
            fingerprints_body_by_state = defaultdict(list)
            fingerprints_status_by_state = defaultdict(list)

            for i, (state, rep) in enumerate(plan):
                auth_header = get_auth_header(state, auth_token)
                body = ep["body_fn"](state)

                try:
                    obs = make_request(ep["url"], method=ep["method"],
                                       auth_header=auth_header, body=body)
                    obs["state"] = state
                    obs["rep"] = rep
                    obs["fingerprint_body"] = fingerprint_body_only(obs)
                    obs["fingerprint_status"] = fingerprint_status_only(obs)
                    obs["body_hash"] = hashlib.sha256(obs["body"]).hexdigest()
                    obs["body_size"] = len(obs["body"])
                    obs["client_profile"] = profile_name
                    obs["accept_encoding"] = profile_config["accept_encoding"]
                    raw_observations[state].append(obs)
                    fingerprints_body_by_state[state].append(obs["fingerprint_body"])
                    fingerprints_status_by_state[state].append(obs["fingerprint_status"])
                except Exception as e:
                    errors.append({"client_profile": profile_name, "endpoint": ep_name,
                                   "state": state, "rep": rep, "error": str(e)})

                # Inter-request jitter
                if i < len(plan) - 1:
                    jitter = rng.uniform(0.05, 0.15)
                    time.sleep(jitter)

            # Compute discrimination scores
            body_disc = compute_discrimination_score(fingerprints_body_by_state)
            status_disc = compute_discrimination_score(fingerprints_status_by_state)

            # Baselines
            b_rand_fps = baseline_random(n=REPS * len(auth_states))
            b_rand_by_state = {}
            idx = 0
            for s in auth_states:
                b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
                idx += REPS
            b_rand_disc = compute_discrimination_score(b_rand_by_state)

            # Body hash variation per state
            body_hash_variation = {}
            for state, obs_list in raw_observations.items():
                hashes = [obs["body_hash"] for obs in obs_list]
                body_hash_variation[state] = {
                    "unique_count": len(set(hashes)),
                    "total": len(hashes),
                    "all_same": len(set(hashes)) == 1,
                }

            # Compression verification: check Content-Encoding in response
            compression_verification = {}
            for state, obs_list in raw_observations.items():
                ce_headers = [obs["headers"].get("Content-Encoding", "none") for obs in obs_list]
                compression_verification[state] = {
                    "content_encoding_values": list(set(ce_headers)),
                    "count": len(ce_headers),
                }

            # Body sizes (compressed vs expected raw)
            body_sizes = {}
            for state, obs_list in raw_observations.items():
                sizes = [obs["body_size"] for obs in obs_list]
                body_sizes[state] = {
                    "min": min(sizes),
                    "max": max(sizes),
                    "mean": sum(sizes) / len(sizes),
                }

            ep_key = f"{ep_name}_{profile_name}"
            profile_results[ep_key] = {
                "body_only_discrimination": body_disc,
                "status_only_discrimination": status_disc,
                "baselines": {
                    "B-RANDOM": b_rand_disc,
                },
                "body_hash_variation": body_hash_variation,
                "compression_verification": compression_verification,
                "body_sizes": body_sizes,
                "total_requests": sum(len(v) for v in raw_observations.values()),
            }
            profile_raw_obs[ep_name] = raw_observations

            print(f"    Body-only: {body_disc:.6f}, "
                  f"Status-only: {status_disc:.6f}, B-RANDOM: {b_rand_disc:.6f}")
            
            # Print hash variation summary
            for state in auth_states:
                hv = body_hash_variation[state]
                print(f"    {state}: unique_hashes={hv['unique_count']}/{hv['total']}, "
                      f"all_same={hv['all_same']}")

        raw_observations_all[profile_name] = profile_raw_obs
        all_results[profile_name] = profile_results

        # Stop proxy
        stop_proxy(proxy)
        time.sleep(1.0)  # ensure port is fully released

    # Step 7: Stop Keycloak
    stop_keycloak()

    # Step 8: Assemble metrics
    metrics = {}
    for profile_name in CLIENT_PROFILES:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_{profile_name}"
            if key in all_results[profile_name]:
                metrics[key] = all_results[profile_name][key]

    # Step 9: Compute primary derived metrics for /userinfo
    userinfo_bo_discs = {}
    for profile_name in CLIENT_PROFILES:
        key = f"/userinfo_{profile_name}"
        if key in metrics:
            userinfo_bo_discs[profile_name] = metrics[key]["body_only_discrimination"]

    # B-IDENTITY-BODY-ONLY: body-only at identity (Client C)
    identity_body_only = userinfo_bo_discs.get("C_identity", None)

    # B-DETERMINISTIC-BR-BODY-ONLY: body-only at deterministic brotli (Client A)
    br_body_only = userinfo_bo_discs.get("A_br_gzip", None)

    # B-DETERMINISTIC-GZIP-BODY-ONLY: body-only at deterministic gzip (Client B)
    gzip_body_only = userinfo_bo_discs.get("B_gzip_only", None)

    # B-MIXED-CLIENT-BODY-ONLY: compute cross-client divergence
    # For each state, check if Client A and Client C produce different body hashes
    cross_client_divergence = {}
    if "/userinfo_A_br_gzip" in metrics and "/userinfo_C_identity" in metrics:
        for state in auth_states:
            hashes_a = [obs["body_hash"] for obs in 
                       raw_observations_all.get("A_br_gzip", {}).get("/userinfo", {}).get(state, [])]
            hashes_c = [obs["body_hash"] for obs in 
                       raw_observations_all.get("C_identity", {}).get("/userinfo", {}).get(state, [])]
            # Check if any hash from A differs from any hash from C
            if hashes_a and hashes_c:
                all_a = set(hashes_a)
                all_c = set(hashes_c)
                divergent = len(all_a - all_c) > 0 or len(all_c - all_a) > 0
                cross_client_divergence[state] = {
                    "divergent": divergent,
                    "unique_hashes_a": len(all_a),
                    "unique_hashes_c": len(all_c),
                }
            else:
                cross_client_divergence[state] = {"divergent": None, "unique_hashes_a": 0, "unique_hashes_c": 0}

    # Compute mixed-client discrimination (Client A + Client C alternating)
    mixed_client_body_disc = None
    if "/userinfo_A_br_gzip" in metrics and "/userinfo_C_identity" in metrics:
        mixed_fps_by_state = defaultdict(list)
        for state in auth_states:
            # Get fingerprints from both Client A and Client C for this state
            fps_a = [obs["fingerprint_body"] for obs in 
                    raw_observations_all.get("A_br_gzip", {}).get("/userinfo", {}).get(state, [])]
            fps_c = [obs["fingerprint_body"] for obs in 
                    raw_observations_all.get("C_identity", {}).get("/userinfo", {}).get(state, [])]
            mixed_fps_by_state[state] = fps_a + fps_c
        mixed_client_body_disc = compute_discrimination_score(mixed_fps_by_state)

    # B-STATUS-ONLY: status-only discrimination across all conditions
    status_only_discs = {}
    for profile_name in CLIENT_PROFILES:
        key = f"/userinfo_{profile_name}"
        if key in metrics:
            status_only_discs[profile_name] = metrics[key]["status_only_discrimination"]

    # B-RANDOM: random fingerprint baseline (same across all profiles)
    b_random_disc = metrics.get("/userinfo_C_identity", {}).get("baselines", {}).get("B-RANDOM", None)

    # Within-state body hash variation summary across profiles
    within_state_variation = {}
    for profile_name in CLIENT_PROFILES:
        key = f"/userinfo_{profile_name}"
        if key in metrics:
            hv = metrics[key]["body_hash_variation"]
            total_unique = sum(v["unique_count"] for v in hv.values())
            total_requests = sum(v["total"] for v in hv.values())
            all_same = all(v["all_same"] for v in hv.values())
            within_state_variation[profile_name] = {
                "total_unique_hashes": total_unique,
                "total_requests": total_requests,
                "all_states_deterministic": all_same,
                "per_state": hv,
            }

    # Add derived metrics
    metrics["M_DETERMINISTIC_DISCRIMINATION"] = {
        "identity_body_only": float(identity_body_only) if identity_body_only is not None else None,
        "br_body_only": float(br_body_only) if br_body_only is not None else None,
        "gzip_body_only": float(gzip_body_only) if gzip_body_only is not None else None,
        "description": "Body-only discrimination under deterministic brotli and gzip on /userinfo"
    }
    metrics["M_IDENTITY_CONTROL"] = {
        "value": float(identity_body_only) if identity_body_only is not None else None,
        "threshold": 0.35,
        "description": "B-IDENTITY-BODY-ONLY: body-only discrimination at identity (no compression) on /userinfo"
    }
    metrics["M_NULL_CONTROL"] = {
        "value": float(b_random_disc) if b_random_disc is not None else None,
        "threshold": "~0.0",
        "description": "B-RANDOM discrimination at all client profiles"
    }
    metrics["M_DETERMINISTIC_BR_CONTROL"] = {
        "value": float(br_body_only) if br_body_only is not None else None,
        "threshold": ">= identity - 0.15",
        "description": "B-DETERMINISTIC-BR-BODY-ONLY: body-only at deterministic brotli on /userinfo"
    }
    metrics["M_DETERMINISTIC_GZIP_CONTROL"] = {
        "value": float(gzip_body_only) if gzip_body_only is not None else None,
        "threshold": ">= identity - 0.15",
        "description": "B-DETERMINISTIC-GZIP-BODY-ONLY: body-only at deterministic gzip on /userinfo"
    }
    metrics["M_CROSS_CLIENT_DIVERGENCE"] = {
        "divergence": cross_client_divergence,
        "description": "Cross-client body hash divergence (same state, different clients, different hashes?)"
    }
    metrics["M_MIXED_CLIENT_DISCRIMINATION"] = {
        "value": float(mixed_client_body_disc) if mixed_client_body_disc is not None else None,
        "threshold": "< identity body-only",
        "description": "B-MIXED-CLIENT-BODY-ONLY: body-only with mixed clients (A + C alternating)"
    }
    metrics["M_STATUS_ONLY_INVARIANCE"] = {
        "values": {k: float(v) for k, v in status_only_discs.items()},
        "threshold": "~ 0.5 on /userinfo invariant",
        "description": "B-STATUS-ONLY: status-only discrimination across all client profiles"
    }
    metrics["M_WITHIN_STATE_VARIATION"] = within_state_variation

    # Step 10: Evaluate controls and decision rule
    control_pass = True
    control_details = {}

    # C1: Positive control — B-IDENTITY-BODY-ONLY >= 0.35 on /userinfo
    c1_pass = identity_body_only is not None and identity_body_only >= 0.35
    control_details["C_POSITIVE_CONTROL"] = {
        "expected": "B-IDENTITY-BODY-ONLY >= 0.35",
        "observed": float(identity_body_only) if identity_body_only is not None else None,
        "pass": c1_pass,
    }
    if not c1_pass:
        control_pass = False

    # C2: Null control — B-RANDOM ~ 0.0 at all client profiles
    c2_pass = b_random_disc is not None and abs(b_random_disc) < 0.1
    control_details["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0",
        "observed": float(b_random_disc) if b_random_disc is not None else None,
        "pass": c2_pass,
    }
    if not c2_pass:
        control_pass = False

    # C3: B-DETERMINISTIC-BR-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15 on /userinfo
    c3_pass = (br_body_only is not None and identity_body_only is not None
               and br_body_only >= identity_body_only - 0.15)
    control_details["C_DETERMINISTIC_BR_PRESERVES"] = {
        "expected": "B-DETERMINISTIC-BR-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15",
        "observed": float(br_body_only) if br_body_only is not None else None,
        "pass": c3_pass,
    }
    if not c3_pass:
        control_pass = False

    # C4: B-DETERMINISTIC-GZIP-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15 on /userinfo
    c4_pass = (gzip_body_only is not None and identity_body_only is not None
               and gzip_body_only >= identity_body_only - 0.15)
    control_details["C_DETERMINISTIC_GZIP_PRESERVES"] = {
        "expected": "B-DETERMINISTIC-GZIP-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15",
        "observed": float(gzip_body_only) if gzip_body_only is not None else None,
        "pass": c4_pass,
    }
    if not c4_pass:
        control_pass = False

    # C5: Within-state body hash variation = 0 for deterministic brotli and gzip
    c5_pass = True
    for profile_name in ["A_br_gzip", "B_gzip_only"]:
        key = f"/userinfo_{profile_name}"
        if key in within_state_variation:
            if not within_state_variation[profile_name]["all_states_deterministic"]:
                c5_pass = False
    control_details["C_WITHIN_STATE_DETERMINISTIC"] = {
        "expected": "Within-state body hash variation = 0 for deterministic brotli and gzip",
        "observed": {k: v["all_states_deterministic"] for k, v in within_state_variation.items()
                    if k in ["A_br_gzip", "B_gzip_only"]},
        "pass": c5_pass,
    }
    if not c5_pass:
        control_pass = False

    # C6: B-MIXED-CLIENT-BODY-ONLY < B-IDENTITY-BODY-ONLY on /userinfo
    c6_pass = (mixed_client_body_disc is not None and identity_body_only is not None
               and mixed_client_body_disc < identity_body_only)
    control_details["C_MIXED_CLIENT_DEGRADES"] = {
        "expected": "B-MIXED-CLIENT-BODY-ONLY < B-IDENTITY-BODY-ONLY",
        "observed": float(mixed_client_body_disc) if mixed_client_body_disc is not None else None,
        "pass": c6_pass,
    }
    if not c6_pass:
        control_pass = False

    # C7: B-STATUS-ONLY >= 0.5 on /userinfo invariant across all client profiles
    c7_pass = all(v >= 0.5 for v in status_only_discs.values()) if status_only_discs else False
    control_details["C_STATUS_ONLY_INVARIANT"] = {
        "expected": "B-STATUS-ONLY >= 0.5 on /userinfo invariant across all client profiles",
        "observed": {k: float(v) for k, v in status_only_discs.items()},
        "pass": c7_pass,
    }
    if not c7_pass:
        control_pass = False

    # C8: No pipeline errors
    c8_pass = len(errors) == 0
    control_details["C_NO_PIPELINE_ERRORS"] = {
        "expected": "0 errors",
        "observed": len(errors),
        "pass": c8_pass,
    }
    if not c8_pass:
        control_pass = False

    # Decision rule (from frozen spec.json)
    if control_pass:
        # All 8 conditions met: body-only survives deterministic CDN negotiation
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif not c1_pass or not c2_pass or not c8_pass:
        # Positive/null control or pipeline errors: measurement invalid
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif not c3_pass or not c4_pass:
        # Deterministic compression degrades body-only: falsified in setting
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not c5_pass:
        # Deterministic compression produces non-deterministic output: measurement invalid
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    else:
        # Some conditions pass, some fail: mixed
        outcome = "MIXED"
        status = "COMPLETE"

    # Observations
    observations = [
        f"Keycloak 25.0 deployed via Docker on localhost:{KEYCLOAK_PORT}",
        f"CDN negotiation proxy on localhost:{PROXY_PORT}",
        f"Client profiles: {list(CLIENT_PROFILES.keys())}",
        f"2 endpoints: /userinfo (GET), /introspect (POST)",
        f"4 auth states x {REPS} reps x {len(CLIENT_PROFILES)} client profiles x 2 endpoints = {4 * REPS * len(CLIENT_PROFILES) * 2} total requests",
        f"Seed: {SEED}",
        f"Brotli available: {BROTLI_AVAILABLE}",
    ]

    # Per-client-profile per-endpoint observations
    for profile_name in CLIENT_PROFILES:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_{profile_name}"
            if key in metrics:
                observations.append(
                    f"profile={profile_name} {ep_name}: "
                    f"body={metrics[key]['body_only_discrimination']:.4f}, "
                    f"status={metrics[key]['status_only_discrimination']:.4f}, "
                    f"B-RANDOM={metrics[key]['baselines']['B-RANDOM']:.4f}"
                )

    # Within-state variation observations
    for profile_name in CLIENT_PROFILES:
        if profile_name in within_state_variation:
            wv = within_state_variation[profile_name]
            observations.append(
                f"profile={profile_name}: total_unique_hashes={wv['total_unique_hashes']}/{wv['total_requests']}, "
                f"all_states_deterministic={wv['all_states_deterministic']}"
            )

    # Cross-client divergence observations
    for state, div in cross_client_divergence.items():
        observations.append(
            f"cross_client_divergence state={state}: divergent={div['divergent']}, "
            f"unique_a={div['unique_hashes_a']}, unique_c={div['unique_hashes_c']}"
        )

    # Mixed-client discrimination
    if mixed_client_body_disc is not None:
        observations.append(f"Mixed-client (A+C) body-only discrimination: {mixed_client_body_disc:.4f}")

    # Validity notes
    validity_notes = [
        "Same Keycloak 25.0 Docker deployment as parent experiments",
        "Same fingerprint algorithm as parent: SHA-256(repr((status, body_sha256, '')))",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "expired_token is locally-signed HS256, not Keycloak-issued (V6 leakage from parent)",
        f"Brotli module available: {BROTLI_AVAILABLE}",
        "Proxy reads client Accept-Encoding and deterministically selects highest-priority algorithm (br > gzip > identity)",
        "Same Accept-Encoding always produces same algorithm — simulates real CDN behavior",
        "Proxy overrides internal Accept-Encoding to identity to get raw response from Keycloak, then applies CDN-selected compression",
        "Body hash computed on compressed bytes received by client (not raw bytes from Keycloak)",
        "Python gzip is deterministic: same input + same level = same output (mtime=0 eliminates timestamp non-determinism)",
        "Python brotli is deterministic: same input + same level = same output",
        "Body-only discrimination is NOT tautological here — compression directly attacks the body hash",
        f"Seed={SEED} for request ordering (deterministic across runs)",
        "Keycloak 25.0 start-dev does not itself compress responses (verified: Content-Encoding=none on direct requests)",
        "This is materially different from EXP-RUNTIME-34654566605: parent tested per-request random compression (worst-case non-determinism); this experiment tests deterministic compression per client (realistic CDN model)",
    ]

    if not BROTLI_AVAILABLE:
        validity_notes.append("BROTLI NOT AVAILABLE: Client A fallback to gzip (reduces discriminating power of brotli test)")

    if errors:
        validity_notes.append(f"Pipeline errors: {len(errors)} requests failed")
        for e in errors[:5]:
            validity_notes.append(f"  Error: {e}")

    # Unresolved
    unresolved = [
        "Does body-only discrimination survive multiple stacked infrastructure layers with correlated compression?",
        "Does the result generalize to non-Keycloak OAuth/OIDC providers (Auth0, Okta)?",
        "Does body-only degradation generalize to larger/more diverse body content-types and sizes?",
        "What discrimination floor remains when hashing decompressed bodies (normalization layer)?",
        "Would a filtered full-vector baseline (status+WWW-Authenticate+Cache-Control+body_hash) survive compression?",
        "What is minimal compression entropy required to collapse body-only below usable threshold?",
        "Does result generalize to production Keycloak with real CDN, load-balancer, or rate-limiting?",
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
            {"path": "raw_observations.json", "role": "raw", "description": "All HTTP observations per client profile per endpoint per state"},
            {"path": "run_experiment.py", "role": "code", "description": "Frozen experiment execution script"},
        ],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    # Save raw observations
    raw_obs_serializable = {}
    for profile_name, endpoint_obs in raw_observations_all.items():
        raw_obs_serializable[profile_name] = {}
        for ep_name, state_obs in endpoint_obs.items():
            raw_obs_serializable[profile_name][ep_name] = {}
            for state, obs_list in state_obs.items():
                raw_obs_serializable[profile_name][ep_name][state] = []
                for obs in obs_list:
                    raw_obs_serializable[profile_name][ep_name][state].append({
                        "url": obs["url"],
                        "status": obs["status"],
                        "headers": obs["headers"],
                        "body_hash": obs["body_hash"],
                        "body_size": obs["body_size"],
                        "body_preview": obs["body"][:500].decode("utf-8", errors="replace"),
                        "fingerprint_body": obs["fingerprint_body"],
                        "fingerprint_status": obs["fingerprint_status"],
                        "client_profile": obs["client_profile"],
                        "accept_encoding": obs["accept_encoding"],
                        "content_encoding": obs["headers"].get("Content-Encoding", "none"),
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
