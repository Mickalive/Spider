#!/usr/bin/env python3
"""
EXP-RUNTIME-34741873198 — Body-Only Fingerprint Under Deterministic CDN Negotiation
====================================================================================
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

# Client profiles: name -> Accept-Encoding header value
CLIENT_PROFILES = {
    "A": "br, gzip",       # CDN selects brotli (highest priority)
    "B": "gzip",           # CDN selects gzip (only option)
    "C": "identity",       # CDN selects identity (no compression)
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

def compress_gzip(data, level=9):
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


def select_compression_algorithm(accept_encoding):
    """CDN negotiation: select the highest-priority algorithm the client supports.
    
    Priority order: br > gzip > identity.
    This is deterministic — same Accept-Encoding always produces the same algorithm.
    """
    ae = accept_encoding.lower()
    if "br" in ae:
        return "br"
    elif "gzip" in ae:
        return "gzip"
    else:
        return "identity"


def apply_compression(body_bytes, algorithm):
    """Apply compression using the selected algorithm.
    
    Returns (compressed_bytes, encoding_header_value).
    Always uses deterministic parameters (fixed level) to simulate real CDN behavior
    where the same client with the same Accept-Encoding sees the same compressed bytes.
    """
    if algorithm == "br":
        compressed = compress_brotli(body_bytes, level=6)
        return compressed, "br"
    elif algorithm == "gzip":
        compressed = compress_gzip(body_bytes, level=9)
        return compressed, "gzip"
    else:
        # identity: no compression
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
    
    The proxy reads the client's Accept-Encoding header and deterministically selects
    the highest-priority algorithm the client supports (br > gzip > identity).
    This simulates real CDN behavior where the CDN picks one algorithm per client.
    """

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def do_request(self):
        """Forward request to Keycloak, compress response based on client's Accept-Encoding."""
        target_url = f"http://127.0.0.1:{KEYCLOAK_PORT}{self.path}"

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Forward request headers
        headers = {}
        for key in self.headers:
            if key.lower() not in ("host", "transfer-encoding"):
                headers[key] = self.headers[key]

        # Override client Accept-Encoding to identity to get raw response from Keycloak
        # (proxy will apply its own compression based on original client's Accept-Encoding)
        original_accept_encoding = self.headers.get("Accept-Encoding", "identity")
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

        # CDN negotiation: select algorithm based on original client's Accept-Encoding
        algorithm = select_compression_algorithm(original_accept_encoding)

        # Apply compression
        compressed_body, encoding = apply_compression(raw_body, algorithm)

        # Send response status
        self.send_response(resp.status_code)

        # Copy response headers (skip transfer-encoding, content-encoding, content-length)
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


def start_proxy():
    """Start the CDN negotiation proxy on PROXY_PORT."""
    server = ReusableHTTPServer(("127.0.0.1", PROXY_PORT), CDNNegotiationProxyHandler)
    server.timeout = 0.5

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"CDN negotiation proxy started on port {PROXY_PORT}")
    return server


def stop_proxy(server):
    """Stop the proxy server."""
    if server:
        server.shutdown()
        print("Proxy stopped.")


# ---------------------------------------------------------------------------
# HTTP REQUEST EXECUTION
# ---------------------------------------------------------------------------

def make_request(url, method="GET", auth_header=None, body=None, accept_encoding="identity", timeout=10):
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
    headers["Accept-Encoding"] = accept_encoding

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
    """Run the full deterministic CDN negotiation experiment."""
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

    # Step 6: Start proxy (CDN negotiation mode)
    proxy = start_proxy()
    time.sleep(0.5)  # let proxy bind

    # Step 7: Run experiment for each client profile
    auth_states = ["no_auth", "valid_token", "expired_token", "invalid_token"]
    endpoints = get_endpoint_configs(auth_token, PROXY_PORT)

    for profile_name, accept_encoding in CLIENT_PROFILES.items():
        print(f"\n{'='*60}")
        print(f"CLIENT PROFILE: {profile_name}")
        print(f"  Accept-Encoding: {accept_encoding}")
        print(f"  CDN selects: {select_compression_algorithm(accept_encoding)}")
        print(f"{'='*60}")

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
                                       auth_header=auth_header, body=body,
                                       accept_encoding=accept_encoding)
                    obs["state"] = state
                    obs["rep"] = rep
                    obs["fingerprint_body"] = fingerprint_body_only(obs)
                    obs["fingerprint_status"] = fingerprint_status_only(obs)
                    obs["body_hash"] = hashlib.sha256(obs["body"]).hexdigest()
                    obs["body_size"] = len(obs["body"])
                    obs["client_profile"] = profile_name
                    obs["accept_encoding"] = accept_encoding
                    obs["selected_algorithm"] = select_compression_algorithm(accept_encoding)
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

    # Step 8: Run mixed-client test (Client A and Client C alternating)
    print(f"\n{'='*60}")
    print("MIXED-CLIENT TEST: Client A (br, gzip) and Client C (identity) alternating")
    print(f"{'='*60}")

    mixed_raw_obs = {}
    for ep in endpoints:
        ep_name = ep["name"]
        print(f"\n  Endpoint: {ep_name}")

        # Build plan: 4 states x 10 reps x 2 clients = 80 requests, alternating A/C
        rng = random.Random(SEED)
        plan = []
        for state in auth_states:
            for rep in range(REPS):
                plan.append((state, rep, "A"))
                plan.append((state, rep, "C"))
        rng.shuffle(plan)

        raw_observations = defaultdict(list)
        fingerprints_body_by_state = defaultdict(list)

        for i, (state, rep, client) in enumerate(plan):
            auth_header = get_auth_header(state, auth_token)
            body = ep["body_fn"](state)
            accept_encoding = CLIENT_PROFILES[client]

            try:
                obs = make_request(ep["url"], method=ep["method"],
                                   auth_header=auth_header, body=body,
                                   accept_encoding=accept_encoding)
                obs["state"] = state
                obs["rep"] = rep
                obs["client_profile"] = client
                obs["fingerprint_body"] = fingerprint_body_only(obs)
                obs["body_hash"] = hashlib.sha256(obs["body"]).hexdigest()
                obs["body_size"] = len(obs["body"])
                obs["selected_algorithm"] = select_compression_algorithm(accept_encoding)
                raw_observations[state].append(obs)
                fingerprints_body_by_state[state].append(obs["fingerprint_body"])
            except Exception as e:
                errors.append({"client_profile": f"MIXED-{client}", "endpoint": ep_name,
                               "state": state, "rep": rep, "error": str(e)})

            if i < len(plan) - 1:
                jitter = rng.uniform(0.05, 0.15)
                time.sleep(jitter)

        body_disc = compute_discrimination_score(fingerprints_body_by_state)
        mixed_raw_obs[ep_name] = {
            "body_only_discrimination": body_disc,
            "raw_observations": raw_observations,
        }
        print(f"    Mixed-client body-only discrimination: {body_disc:.6f}")

    # Step 9: Stop proxy and Keycloak
    stop_proxy(proxy)
    stop_keycloak()

    # Step 10: Assemble metrics
    metrics = {}
    
    # Per-client-profile per-endpoint metrics
    for profile_name in CLIENT_PROFILES:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_{profile_name}"
            if key in all_results[profile_name]:
                metrics[key] = all_results[profile_name][key]

    # Mixed-client metrics
    for ep_name in ["/userinfo", "/introspect"]:
        key = f"{ep_name}_MIXED"
        if ep_name in mixed_raw_obs:
            metrics[key] = {
                "body_only_discrimination": mixed_raw_obs[ep_name]["body_only_discrimination"],
            }

    # Primary derived metrics: body-only discrimination on /userinfo per client profile
    userinfo_bo_discs = {}
    for profile_name in CLIENT_PROFILES:
        key = f"/userinfo_{profile_name}"
        if key in metrics:
            userinfo_bo_discs[profile_name] = metrics[key]["body_only_discrimination"]

    # Status-only discrimination on /userinfo per client profile (should be 0.5 invariant)
    userinfo_status_discs = {}
    for profile_name in CLIENT_PROFILES:
        key = f"/userinfo_{profile_name}"
        if key in metrics:
            userinfo_status_discs[profile_name] = metrics[key]["status_only_discrimination"]

    # B-IDENTITY-BODY-ONLY: body-only at profile C (identity) on /userinfo
    identity_body_only = userinfo_bo_discs.get("C", None)

    # B-DETERMINISTIC-BR-BODY-ONLY: body-only at profile A (brotli) on /userinfo
    br_body_only = userinfo_bo_discs.get("A", None)

    # B-DETERMINISTIC-GZIP-BODY-ONLY: body-only at profile B (gzip) on /userinfo
    gzip_body_only = userinfo_bo_discs.get("B", None)

    # B-MIXED-CLIENT-BODY-ONLY: mixed-client body-only on /userinfo
    mixed_body_only = metrics.get("/userinfo_MIXED", {}).get("body_only_discrimination", None)

    # B-STATUS-ONLY: status-only at profile C (identity) on /userinfo
    status_only = userinfo_status_discs.get("C", None)

    # Within-state hash variation for deterministic brotli (A) and gzip (B)
    within_state_variation = {}
    for profile_name in ["A", "B"]:
        key = f"/userinfo_{profile_name}"
        if key in metrics:
            hv = metrics[key]["body_hash_variation"]
            within_state_variation[profile_name] = {
                "all_states_all_same": all(v["all_same"] for v in hv.values()),
                "total_unique_hashes": sum(v["unique_count"] for v in hv.values()),
                "total_requests": sum(v["total"] for v in hv.values()),
                "per_state": hv,
            }

    # Null control: B-RANDOM at all client profiles
    null_control_values = {}
    for profile_name in CLIENT_PROFILES:
        key = f"/userinfo_{profile_name}"
        if key in metrics:
            null_control_values[profile_name] = metrics[key]["baselines"]["B-RANDOM"]

    # Add derived metrics
    metrics["M_DETERMINISTIC_DISCRIMINATION"] = {
        "identity_body_only": float(identity_body_only) if identity_body_only is not None else None,
        "br_body_only": float(br_body_only) if br_body_only is not None else None,
        "gzip_body_only": float(gzip_body_only) if gzip_body_only is not None else None,
        "description": "Body-only discrimination under deterministic brotli and gzip on /userinfo"
    }
    metrics["M_STATUS_INVARIANCE"] = {
        "per_profile": {k: float(v) for k, v in userinfo_status_discs.items()},
        "expected": 0.5,
        "description": "Status-only discrimination on /userinfo invariant across all client profiles"
    }
    metrics["M_WITHIN_STATE_VARIATION"] = within_state_variation
    metrics["M_CROSS_CLIENT_DIVERGENCE"] = {
        "identity_body_only": float(identity_body_only) if identity_body_only is not None else None,
        "mixed_client_body_only": float(mixed_body_only) if mixed_body_only is not None else None,
        "description": "Cross-client hash divergence: mixed clients should have degraded discrimination"
    }
    metrics["M_NULL_CONTROL"] = {
        "per_profile": {k: float(v) for k, v in null_control_values.items()},
        "description": "B-RANDOM discrimination at all client profiles"
    }

    # Step 11: Evaluate controls and decision rule
    control_pass = True
    control_details = {}

    # C1: Positive control — identity body-only >= 0.35
    c1_pass = identity_body_only is not None and identity_body_only >= 0.35
    control_details["C_POSITIVE_CONTROL_IDENTITY"] = {
        "expected": "B-IDENTITY-BODY-ONLY >= 0.35 on /userinfo",
        "observed": float(identity_body_only) if identity_body_only is not None else None,
        "pass": c1_pass,
    }
    if not c1_pass:
        control_pass = False

    # C2: Null control — B-RANDOM ~ 0.0 at all client profiles
    all_null_pass = all(
        v is not None and abs(v) < 0.1
        for v in null_control_values.values()
    )
    control_details["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0 at all client profiles",
        "observed": {k: float(v) for k, v in null_control_values.items()},
        "pass": all_null_pass,
    }
    if not all_null_pass:
        control_pass = False

    # C3: Deterministic brotli preserves — br_body_only >= identity - 0.15
    c3_pass = (br_body_only is not None and identity_body_only is not None
               and br_body_only >= identity_body_only - 0.15)
    control_details["C_DETERMINISTIC_BR_PRESERVES"] = {
        "expected": "B-DETERMINISTIC-BR-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15 on /userinfo",
        "observed": float(br_body_only) if br_body_only is not None else None,
        "pass": c3_pass,
    }
    if not c3_pass:
        control_pass = False

    # C4: Deterministic gzip preserves — gzip_body_only >= identity - 0.15
    c4_pass = (gzip_body_only is not None and identity_body_only is not None
               and gzip_body_only >= identity_body_only - 0.15)
    control_details["C_DETERMINISTIC_GZIP_PRESERVES"] = {
        "expected": "B-DETERMINISTIC-GZIP-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15 on /userinfo",
        "observed": float(gzip_body_only) if gzip_body_only is not None else None,
        "pass": c4_pass,
    }
    if not c4_pass:
        control_pass = False

    # C5: Within-state hash variation = 0 for deterministic brotli and gzip
    c5_pass = all(
        within_state_variation.get(p, {}).get("all_states_all_same", False)
        for p in ["A", "B"]
    )
    control_details["C_WITHIN_STATE_STABILITY"] = {
        "expected": "Within-state body hash variation = 0 for deterministic brotli and gzip",
        "observed": {p: within_state_variation.get(p, {}) for p in ["A", "B"]},
        "pass": c5_pass,
    }
    if not c5_pass:
        control_pass = False

    # C6: Mixed-client divergence — mixed < identity
    c6_pass = (mixed_body_only is not None and identity_body_only is not None
               and mixed_body_only < identity_body_only)
    control_details["C_MIXED_CLIENT_DIVERGENCE"] = {
        "expected": "B-MIXED-CLIENT-BODY-ONLY < B-IDENTITY-BODY-ONLY on /userinfo",
        "observed": float(mixed_body_only) if mixed_body_only is not None else None,
        "pass": c6_pass,
    }
    if not c6_pass:
        control_pass = False

    # C7: Status-only invariant = 0.5 across all profiles
    c7_pass = all(
        v is not None and abs(v - 0.5) < 0.01
        for v in userinfo_status_discs.values()
    )
    control_details["C_STATUS_INVARIANT"] = {
        "expected": "B-STATUS-ONLY >= 0.5 on /userinfo invariant across all client profiles",
        "observed": {k: float(v) for k, v in userinfo_status_discs.items()},
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
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif not c3_pass or not c4_pass:
        # Deterministic compression degrades body-only
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not c5_pass:
        # Deterministic compression produces non-deterministic output
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif not c1_pass or not c2_pass or not c8_pass:
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    else:
        outcome = "MIXED"
        status = "COMPLETE"

    # Observations
    observations = [
        f"Keycloak 25.0 deployed via Docker on localhost:{KEYCLOAK_PORT}",
        f"CDN negotiation proxy on localhost:{PROXY_PORT}",
        f"Client profiles: {CLIENT_PROFILES}",
        f"CDN negotiation: select highest-priority algorithm from Accept-Encoding (br > gzip > identity)",
        f"2 endpoints: /userinfo (GET), /introspect (POST)",
        f"4 auth states x {REPS} reps x {len(CLIENT_PROFILES)} client profiles x 2 endpoints = {4 * REPS * len(CLIENT_PROFILES) * 2} total requests",
        f"Plus mixed-client test: 4 states x {REPS} reps x 2 clients x 2 endpoints = {4 * REPS * 2 * 2} requests",
        f"Total requests: {4 * REPS * len(CLIENT_PROFILES) * 2 + 4 * REPS * 2 * 2}",
        f"Seed: {SEED}",
        f"Brotli available: {BROTLI_AVAILABLE}",
    ]

    # Per-client-profile per-endpoint observations
    for profile_name in CLIENT_PROFILES:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_{profile_name}"
            if key in metrics:
                observations.append(
                    f"Profile {profile_name} ({CLIENT_PROFILES[profile_name]}) {ep_name}: "
                    f"body={metrics[key]['body_only_discrimination']:.4f}, "
                    f"status={metrics[key]['status_only_discrimination']:.4f}, "
                    f"B-RANDOM={metrics[key]['baselines']['B-RANDOM']:.4f}"
                )

    # Mixed-client observations
    for ep_name in ["/userinfo", "/introspect"]:
        key = f"{ep_name}_MIXED"
        if key in metrics:
            observations.append(
                f"MIXED-CLIENT {ep_name}: body={metrics[key]['body_only_discrimination']:.4f}"
            )

    # Within-state variation observations
    for profile_name in ["A", "B"]:
        if profile_name in within_state_variation:
            wsv = within_state_variation[profile_name]
            observations.append(
                f"Profile {profile_name} within-state variation: "
                f"all_same={wsv['all_states_all_same']}, "
                f"unique_hashes={wsv['total_unique_hashes']}/{wsv['total_requests']}"
            )

    # Validity notes
    validity_notes = [
        "Same Keycloak 25.0 Docker deployment as parent experiments",
        "Same fingerprint algorithm as parent: SHA-256(repr((status, body_sha256, '')))",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "expired_token is locally-signed HS256, not Keycloak-issued (V6 leakage from parent)",
        f"Brotli module available: {BROTLI_AVAILABLE}",
        "Proxy overrides client Accept-Encoding to identity to get raw response from Keycloak",
        "Proxy reads original Accept-Encoding and deterministically selects algorithm (br > gzip > identity)",
        "Body hash computed on compressed bytes received by client (not raw bytes from Keycloak)",
        "Body-only discrimination is NOT tautological here — compression directly attacks the body hash",
        f"Seed={SEED} for request ordering (deterministic across runs)",
        "CDN negotiation is deterministic: same Accept-Encoding always produces same algorithm",
        "Compression uses fixed parameters (gzip level=9, brotli level=6) to simulate CDN determinism",
        "This is materially different from EXP-RUNTIME-34654566605 which tested per-request random compression",
    ]

    if not BROTLI_AVAILABLE:
        validity_notes.append("BROTLI NOT AVAILABLE: Client A falls back to gzip (weaker test of deterministic compression)")

    if errors:
        validity_notes.append(f"Pipeline errors: {len(errors)} requests failed")
        for e in errors[:5]:
            validity_notes.append(f"  Error: {e}")

    # Unresolved
    unresolved = [
        "Does body-only discrimination survive multiple stacked infrastructure layers with correlated compression?",
        "Does the result generalize to non-Keycloak OAuth/OIDC providers?",
        "Would a filtered full-vector baseline (status+WWW-Authenticate+Cache-Control+body_hash) survive deterministic compression?",
        "Does result generalize to larger/more diverse body content-types and sizes beyond Keycloak /userinfo 0/189 bytes?",
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
                        "selected_algorithm": obs["selected_algorithm"],
                        "content_encoding": obs["headers"].get("Content-Encoding", "none"),
                        "elapsed": obs["elapsed"],
                        "timestamp": obs["timestamp"],
                        "state": obs["state"],
                        "rep": obs["rep"],
                    })

    # Add mixed-client raw observations
    raw_obs_serializable["MIXED"] = {}
    for ep_name, mixed_data in mixed_raw_obs.items():
        raw_obs_serializable["MIXED"][ep_name] = {}
        for state, obs_list in mixed_data["raw_observations"].items():
            raw_obs_serializable["MIXED"][ep_name][state] = []
            for obs in obs_list:
                raw_obs_serializable["MIXED"][ep_name][state].append({
                    "url": obs["url"],
                    "status": obs["status"],
                    "headers": obs["headers"],
                    "body_hash": obs["body_hash"],
                    "body_size": obs["body_size"],
                    "body_preview": obs["body"][:500].decode("utf-8", errors="replace"),
                    "fingerprint_body": obs["fingerprint_body"],
                    "client_profile": obs["client_profile"],
                    "selected_algorithm": obs["selected_algorithm"],
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
