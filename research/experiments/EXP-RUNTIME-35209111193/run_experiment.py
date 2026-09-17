#!/usr/bin/env python3
"""
EXP-RUNTIME-35209111193 - Decompression-Normalization on Non-JSON Content Types
================================================================================
Tests decompression-normalization (SHA256 on decompressed body + status) on
HTML and XML content types at multiple payload sizes (1KB, 10KB, 100KB) under
brotli/gzip compression WITHOUT CDN noise.

Frozen from spec.json and prereg.md - DO NOT MODIFY.
"""

import brotli
import gzip
import hashlib
import io
import json
import os
import random
import sys
import time
import threading
import hashlib as _hashlib
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

import jwt
import requests
import numpy as np


class NumpyEncoder(json.JSONEncoder):
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

EXPERIMENT_ID = "EXP-RUNTIME-35209111193"
LANE = "runtime"
SEED = 44
REPS = 20
BASE_PORT = 5400  # Base port, increment per content type
CLIENT_SECRET = "spider-secret-12345"

USERINFO_PATH = "/userinfo"
INTROSPECT_PATH = "/introspect"

# Content types to test
CONTENT_TYPES = {
    "JSON": "application/json",
    "HTML": "text/html",
    "XML": "application/xml",
}

# Payload sizes
PAYLOAD_SIZES = {
    "1KB": 1024,
    "10KB": 10240,
    "100KB": 102400,
}

# Brotli quality range
BROTLI_QUALITY_RANGE = [4, 5, 6, 7, 8]

AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]

BROTLI_AVAILABLE = True
try:
    import brotli as _brotli_test
except ImportError:
    BROTLI_AVAILABLE = False
    print("WARNING: brotli module not available. Brotli conditions will fail.")


# ---------------------------------------------------------------------------
# CONTENT BODY GENERATORS
# ---------------------------------------------------------------------------

def generate_json_body(state, target_size):
    """Generate JSON body for given auth state and target size."""
    if state in ("no_auth", "expired_token", "invalid_token"):
        # Error body - all 3 error states share similar body
        base = {"error": "invalid_token", "message": "Authentication failed"}
    else:
        # Valid token body
        base = {"sub": "alice", "name": "Alice", "email": "alice@example.com", "scope": "openid profile email"}

    # Pad to target size
    current_json = json.dumps(base)
    current_size = len(current_json.encode("utf-8"))
    if current_size < target_size:
        padding_needed = target_size - current_size - 20  # Reserve for padding field
        if padding_needed > 0:
            base["data"] = "x" * padding_needed
    return json.dumps(base).encode("utf-8")[:target_size]


def generate_html_body(state, target_size):
    """Generate HTML body for given auth state and target size."""
    if state in ("no_auth", "expired_token", "invalid_token"):
        # Error HTML
        base_content = """<!DOCTYPE html>
<html>
<head><title>Authentication Error</title></head>
<body>
<div class="error">
<h1>401 Unauthorized</h1>
<p>Error: invalid_token</p>
<p>Authentication failed. Please provide a valid Bearer token.</p>
</div>
</body>
</html>"""
    else:
        # Valid HTML
        base_content = """<!DOCTYPE html>
<html>
<head><title>User Profile</title></head>
<body>
<div class="user">
<h1>User Profile</h1>
<p><strong>Name:</strong> Alice</p>
<p><strong>Email:</strong> alice@example.com</p>
<p><strong>Subject:</strong> alice</p>
<p><strong>Scope:</strong> openid profile email</p>
</div>
</body>
</html>"""

    # Pad to target size
    encoded = base_content.encode("utf-8")
    padding_block = b"<p>Additional data padding block for size control.</p>\n"
    while len(encoded) < target_size:
        encoded += padding_block

    return encoded[:target_size]


def generate_xml_body(state, target_size):
    """Generate XML body for given auth state and target size."""
    if state in ("no_auth", "expired_token", "invalid_token"):
        # Error XML
        base_content = """<?xml version="1.0" encoding="UTF-8"?>
<response>
<status>error</status>
<error_code>401</error_code>
<error>invalid_token</error>
<message>Authentication failed. Please provide a valid Bearer token.</message>
</response>"""
    else:
        # Valid XML
        base_content = """<?xml version="1.0" encoding="UTF-8"?>
<response>
<status>success</status>
<user>
<sub>alice</sub>
<name>Alice</name>
<email>alice@example.com</email>
<scope>openid profile email</scope>
</user>
</response>"""

    # Pad to target size
    encoded = base_content.encode("utf-8")
    padding_block = b"<data_item>Additional padding data for size control.</data_item>\n"
    while len(encoded) < target_size:
        encoded += padding_block

    return encoded[:target_size]


# ---------------------------------------------------------------------------
# TOKEN GENERATION
# ---------------------------------------------------------------------------

def make_valid_token():
    now = datetime.now(timezone.utc)
    payload = {
        "sub": "alice",
        "name": "Alice",
        "email": "alice@example.com",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=1)).timestamp()),
        "realm_access": {"roles": ["user"]},
    }
    return jwt.encode(payload, CLIENT_SECRET, algorithm="HS256")


def make_expired_token():
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
    return "invalid-token-12345"


# ---------------------------------------------------------------------------
# MOCK OAUTH2 SERVER (returns JSON/HTML/XML based on content type)
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class MockOAuthHandler(BaseHTTPRequestHandler):
    body_size = 1024
    content_type = "JSON"
    seed = 44
    request_counter = 0

    def log_message(self, format, *args):
        pass

    def _check_auth(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return False
        token = auth[7:]
        try:
            payload = jwt.decode(token, CLIENT_SECRET, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def _get_body(self, state, size):
        """Generate body based on content type setting."""
        if self.content_type == "JSON":
            return generate_json_body(state, size)
        elif self.content_type == "HTML":
            return generate_html_body(state, size)
        elif self.content_type == "XML":
            return generate_xml_body(state, size)
        else:
            return generate_json_body(state, size)

    def _get_mime_type(self):
        """Get MIME type based on content type setting."""
        return CONTENT_TYPES.get(self.content_type, "application/json")

    def do_GET(self):
        if self.path == USERINFO_PATH:
            state = "valid_token" if self._check_auth() else "no_auth"
            body = self._get_body(state, self.body_size)
            status = 200 if self._check_auth() else 401

            # --- COMPRESSION FIX: actually compress and set Content-Encoding ---
            accept_enc = self.headers.get("Accept-Encoding", "")
            # Prefer explicit Accept-Encoding; default to no compression if not asked
            if "br" in accept_enc:
                q = BROTLI_QUALITY_RANGE[MockOAuthHandler.request_counter % len(BROTLI_QUALITY_RANGE)]
                MockOAuthHandler.request_counter += 1
                compressed = brotli.compress(body, quality=q)
                self.send_response(status)
                self.send_header("Content-Type", self._get_mime_type())
                self.send_header("Content-Encoding", "br")
                self.send_header("Content-Length", str(len(compressed)))
                self.send_header("X-Brotli-Quality", str(q))
                self.end_headers()
                self.wfile.write(compressed)
            elif "gzip" in accept_enc:
                MockOAuthHandler.request_counter += 1
                compressed = compress_gzip(body)
                self.send_response(status)
                self.send_header("Content-Type", self._get_mime_type())
                self.send_header("Content-Encoding", "gzip")
                self.send_header("Content-Length", str(len(compressed)))
                self.end_headers()
                self.wfile.write(compressed)
            else:
                self.send_response(status)
                self.send_header("Content-Type", self._get_mime_type())
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == INTROSPECT_PATH:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            params = dict(p.split("=", 1) for p in post_data.decode().split("&") if "=" in p)
            token = params.get("token", "")

            # Determine state based on token
            if self._check_auth():
                state = "valid_token"
            else:
                # Check if expired or invalid
                try:
                    jwt.decode(token, CLIENT_SECRET, algorithms=["HS256"])
                    state = "valid_token"  # Shouldn't reach here
                except jwt.ExpiredSignatureError:
                    state = "expired_token"
                except jwt.InvalidTokenError:
                    state = "invalid_token"

            body = self._get_body(state, self.body_size)

            accept_enc = self.headers.get("Accept-Encoding", "")
            if "br" in accept_enc:
                q = BROTLI_QUALITY_RANGE[MockOAuthHandler.request_counter % len(BROTLI_QUALITY_RANGE)]
                MockOAuthHandler.request_counter += 1
                compressed = brotli.compress(body, quality=q)
                self.send_response(200)
                self.send_header("Content-Type", self._get_mime_type())
                self.send_header("Content-Encoding", "br")
                self.send_header("Content-Length", str(len(compressed)))
                self.send_header("X-Brotli-Quality", str(q))
                self.end_headers()
                self.wfile.write(compressed)
            elif "gzip" in accept_enc:
                MockOAuthHandler.request_counter += 1
                compressed = compress_gzip(body)
                self.send_response(200)
                self.send_header("Content-Type", self._get_mime_type())
                self.send_header("Content-Encoding", "gzip")
                self.send_header("Content-Length", str(len(compressed)))
                self.end_headers()
                self.wfile.write(compressed)
            else:
                self.send_response(200)
                self.send_header("Content-Type", self._get_mime_type())
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        else:
            self.send_error(404)


def start_mock_server(port, body_size=1024, seed=44, content_type="JSON"):
    MockOAuthHandler.body_size = body_size
    MockOAuthHandler.seed = seed
    MockOAuthHandler.content_type = content_type
    server = ReusableHTTPServer(("127.0.0.1", port), MockOAuthHandler)
    server.timeout = 0.5
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Mock OAuth2 server started on port {port} (content_type={content_type})")
    return server


def stop_mock_server(server):
    if server:
        server.shutdown()
        server.server_close()
        time.sleep(0.3)  # Wait for port release


# ---------------------------------------------------------------------------
# COMPRESS UTILITIES
# ---------------------------------------------------------------------------

def compress_gzip(data, level=9):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=level, mtime=0) as f:
        f.write(data)
    return buf.getvalue()


def compress_brotli(data, quality=6):
    return brotli.compress(data, quality=quality)


def decompress_body(raw_body, content_encoding):
    """Decompress body based on Content-Encoding header."""
    if content_encoding == "br":
        try:
            return brotli.decompress(raw_body)
        except Exception:
            return raw_body
    elif content_encoding == "gzip":
        try:
            return gzip.decompress(raw_body)
        except Exception:
            return raw_body
    else:
        return raw_body


# ---------------------------------------------------------------------------
# HTTP REQUEST EXECUTION
# ---------------------------------------------------------------------------

def make_request(url, method="GET", auth_header=None, body=None, timeout=10, accept_encoding=None):
    headers = {}
    if auth_header:
        headers["Authorization"] = auth_header
    if body:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if accept_encoding:
        headers["Accept-Encoding"] = accept_encoding

    start = time.monotonic()
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, stream=True)
        elif method == "POST":
            resp = requests.post(url, headers=headers, data=body, timeout=timeout, allow_redirects=True, stream=True)
        else:
            raise ValueError(f"Unknown method: {method}")

        raw_bytes = resp.raw.read(decode_content=False)
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
# FINGERPRINT FUNCTIONS
# ---------------------------------------------------------------------------

def fingerprint_compressed_only(observation):
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
    vector = (observation["status"], body_hash, '')
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


def fingerprint_decompressed(observation):
    ce = observation["headers"].get("Content-Encoding", "")
    raw_body = observation["body"]
    decompressed = decompress_body(raw_body, ce)
    body_hash = hashlib.sha256(decompressed).hexdigest()
    vector = (observation["status"], body_hash, '')
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


def fingerprint_status_only(observation):
    vector = (observation["status"], '', '')
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# DISCRIMINATION SCORE (Jaccard distance)
# ---------------------------------------------------------------------------

def compute_discrimination_score(fingerprints_by_state):
    """Compute Jaccard distance between fingerprint sets across auth states."""
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
    rng = random.Random(seed)
    return [hashlib.sha256(rng.getrandbits(256).to_bytes(32, "big")).hexdigest()
            for _ in range(n)]


# ---------------------------------------------------------------------------
# AUTH STATE TOKEN GENERATION
# ---------------------------------------------------------------------------

def get_auth_header(state, auth_token):
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

def get_endpoint_configs(auth_token, port):
    expired_token = make_expired_token()
    invalid_token = make_invalid_token()

    def introspect_body(state):
        token_map = {
            "no_auth": "",
            "valid_token": auth_token,
            "expired_token": expired_token,
            "invalid_token": invalid_token,
        }
        body = {
            "token": token_map.get(state, ""),
            "client_id": "spider-client",
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
            "url": f"http://127.0.0.1:{port}{USERINFO_PATH}",
            "method": "GET",
            "body_fn": lambda state: None,
            "expected_status_fn": userinfo_expected_status,
        },
        {
            "name": "/introspect",
            "url": f"http://127.0.0.1:{port}{INTROSPECT_PATH}",
            "method": "POST",
            "body_fn": introspect_body,
            "expected_status_fn": introspect_expected_status,
        },
    ]


# ---------------------------------------------------------------------------
# MAIN EXPERIMENT
# ---------------------------------------------------------------------------

def run_experiment():
    raw_observations_all = {}
    all_results = {}
    errors = []
    request_count = 0

    print(f"Experiment: {EXPERIMENT_ID}")
    print(f"Auth states: {AUTH_STATES}")
    print(f"Reps per state: {REPS}")
    print(f"Seed: {SEED}")
    print(f"Content types: {list(CONTENT_TYPES.keys())}")
    print(f"Payload sizes: {list(PAYLOAD_SIZES.keys())}")
    print(f"Brotli quality range: {BROTLI_QUALITY_RANGE}")
    print(f"without CDN noise — WITH SERVER COMPRESSION FIX - direct to mock server")
    print()

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated. Length: {len(auth_token)}")

    # Run baselines: DECOMPRESSED-VARYING-BROTLI and DECOMPRESSED-VARYING-GZIP
    baselines_to_run = ["DECOMPRESSED-VARYING-BROTLI", "DECOMPRESSED-VARYING-GZIP", "COMPRESSED-VARYING-BROTLI", "COMPRESSED-VARYING-GZIP"]

    port_idx = 0
    for content_type_name, content_mime in CONTENT_TYPES.items():
        print(f"\n{'='*70}")
        print(f"CONTENT TYPE: {content_type_name}")
        print(f"{'='*70}")

        for size_name, size_bytes in PAYLOAD_SIZES.items():
            print(f"\n  Payload size: {size_name} ({size_bytes} bytes)")

            # Use unique port for each server instance
            port = BASE_PORT + port_idx
            port_idx += 1

            # Start mock server for this content type and size
            mock_server = start_mock_server(port, size_bytes, SEED, content_type_name)
            time.sleep(0.5)

            # Test mock server connectivity
            try:
                test_resp = requests.get(f"http://127.0.0.1:{port}{USERINFO_PATH}",
                                         headers={"Authorization": f"Bearer {auth_token}"},
                                         timeout=5)
                print(f"    Mock server test: status={test_resp.status_code}, body_size={len(test_resp.content)}")
            except Exception as e:
                print(f"    WARNING: Mock server test failed: {e}")

            endpoints = get_endpoint_configs(auth_token, port)

            for baseline_name in baselines_to_run:
                print(f"\n    Baseline: {baseline_name}")

                condition_results = {}
                condition_raw_obs = {}

                for ep in endpoints:
                    ep_name = ep["name"]

                    rng = random.Random(SEED)
                    plan = []
                    for state in AUTH_STATES:
                        for rep in range(REPS):
                            plan.append((state, rep))
                    rng.shuffle(plan)

                    raw_observations = defaultdict(list)
                    fingerprints_compressed_by_state = defaultdict(list)
                    fingerprints_decompressed_by_state = defaultdict(list)
                    fingerprints_status_by_state = defaultdict(list)

                    decompression_latencies = []

                    for i, (state, rep) in enumerate(plan):
                        auth_header = get_auth_header(state, auth_token)
                        body = ep["body_fn"](state)

                        # Determine Accept-Encoding per baseline
                        if "BROTLI" in baseline_name:
                            ae = "br"
                        elif "GZIP" in baseline_name:
                            ae = "gzip"
                        else:
                            ae = None
                        try:
                            obs = make_request(ep["url"], method=ep["method"],
                                               auth_header=auth_header, body=body,
                                               accept_encoding=ae)
                            obs["state"] = state
                            obs["rep"] = rep
                            obs["baseline"] = baseline_name
                            obs["content_type"] = content_type_name
                            obs["payload_size"] = size_name
                            obs["fingerprint_compressed"] = fingerprint_compressed_only(obs)
                            obs["fingerprint_decompressed"] = fingerprint_decompressed(obs)
                            obs["fingerprint_status"] = fingerprint_status_only(obs)
                            obs["body_hash_compressed"] = hashlib.sha256(obs["body"]).hexdigest()
                            obs["body_size"] = len(obs["body"])

                            ce = obs["headers"].get("Content-Encoding", "none")
                            obs["content_encoding"] = ce

                            # Measure decompression latency
                            decomp_start = time.monotonic()
                            decompressed = decompress_body(obs["body"], ce)
                            decomp_elapsed = time.monotonic() - decomp_start
                            obs["decompression_latency_ms"] = decomp_elapsed * 1000
                            decompression_latencies.append(decomp_elapsed * 1000)

                            obs["decompressed_hash"] = hashlib.sha256(decompressed).hexdigest()

                            raw_observations[state].append(obs)

                            # Track fingerprints
                            fingerprints_compressed_by_state[state].append(obs["fingerprint_compressed"])
                            fingerprints_decompressed_by_state[state].append(obs["fingerprint_decompressed"])
                            fingerprints_status_by_state[state].append(obs["fingerprint_status"])

                            request_count += 1
                        except Exception as e:
                            errors.append({"baseline": baseline_name, "endpoint": ep_name,
                                           "state": state, "rep": rep, "error": str(e)})

                        if i < len(plan) - 1:
                            jitter = rng.uniform(0.05, 0.15)
                            time.sleep(jitter)

                    # Compute discrimination scores
                    compressed_disc = compute_discrimination_score(fingerprints_compressed_by_state)
                    decompressed_disc = compute_discrimination_score(fingerprints_decompressed_by_state)
                    status_disc = compute_discrimination_score(fingerprints_status_by_state)

                    b_rand_fps = baseline_random(n=REPS * len(AUTH_STATES))
                    b_rand_by_state = {}
                    idx = 0
                    for s in AUTH_STATES:
                        b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
                        idx += REPS
                    b_rand_disc = compute_discrimination_score(b_rand_by_state)

                    # Compressed hash variation
                    compressed_hash_variation = {}
                    for state, obs_list in raw_observations.items():
                        hashes = [obs["body_hash_compressed"] for obs in obs_list]
                        compressed_hash_variation[state] = {
                            "unique_count": len(set(hashes)),
                            "total": len(hashes),
                            "all_same": len(set(hashes)) == 1,
                        }

                    # Decompressed hash variation
                    decompressed_hash_variation = {}
                    for state, obs_list in raw_observations.items():
                        decompressed_hashes = [obs["decompressed_hash"] for obs in obs_list]
                        decompressed_hash_variation[state] = {
                            "unique_count": len(set(decompressed_hashes)),
                            "total": len(decompressed_hashes),
                            "all_same": len(set(decompressed_hashes)) == 1,
                        }

                    # Body sizes
                    body_sizes = {}
                    for state, obs_list in raw_observations.items():
                        sizes = [obs["body_size"] for obs in obs_list]
                        body_sizes[state] = {
                            "min": min(sizes),
                            "max": max(sizes),
                            "mean": sum(sizes) / len(sizes),
                        }

                    # Compression verification
                    compression_verification = {}
                    for state, obs_list in raw_observations.items():
                        ce_headers = [obs["headers"].get("Content-Encoding", "none") for obs in obs_list]
                        compression_verification[state] = {
                            "content_encoding_values": list(set(ce_headers)),
                            "count": len(ce_headers),
                        }

                    ep_key = f"{ep_name}_{baseline_name}_{content_type_name}_{size_name}"
                    condition_results[ep_key] = {
                        "compressed_body_only_discrimination": compressed_disc,
                        "decompressed_body_only_discrimination": decompressed_disc,
                        "status_only_discrimination": status_disc,
                        "baselines": {
                            "B-RANDOM": b_rand_disc,
                        },
                        "compressed_hash_variation": compressed_hash_variation,
                        "decompressed_hash_variation": decompressed_hash_variation,
                        "compression_verification": compression_verification,
                        "body_sizes": body_sizes,
                        "total_requests": sum(len(v) for v in raw_observations.values()),
                        "decompression_latency_ms": {
                            "mean": sum(decompression_latencies) / len(decompression_latencies) if decompression_latencies else 0,
                            "min": min(decompression_latencies) if decompression_latencies else 0,
                            "max": max(decompression_latencies) if decompression_latencies else 0,
                        },
                    }
                    condition_raw_obs[ep_name] = raw_observations

                    print(f"      {ep_name}: compressed={compressed_disc:.4f}, "
                          f"decompressed={decompressed_disc:.4f}, "
                          f"status={status_disc:.4f}, B-RANDOM={b_rand_disc:.4f}")

                    for state in AUTH_STATES:
                        chv = compressed_hash_variation[state]
                        dhv = decompressed_hash_variation[state]
                        print(f"        {state}: compressed_unique={chv['unique_count']}/{chv['total']} "
                              f"decompressed_unique={dhv['unique_count']}/{dhv['total']}")

                raw_observations_all[f"{content_type_name}_{size_name}_{baseline_name}"] = condition_raw_obs
                all_results[f"{content_type_name}_{size_name}_{baseline_name}"] = condition_results

            stop_mock_server(mock_server)
            time.sleep(0.3)

    # =========================================================================
    # ASSEMBLE METRICS
    # =========================================================================

    metrics = {}
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            metrics[ep_key] = ep_data

    # =========================================================================
    # CONTROLS
    # =========================================================================

    control_details = {}

    # C_COMPRESSION_ACTIVE: Content-Encoding != 'none'
    # Check all observations have br or gzip, not none
    all_encs=[]
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            for state, cv in ep_data["compression_verification"].items():
                all_encs.extend(cv["content_encoding_values"])
    unique_encs=list(set(all_encs))
    c_compression_pass=all(e in ("br","gzip") for e in unique_encs) and "none" not in unique_encs
    control_details["C_COMPRESSION_ACTIVE"]={
        "expected": "Content-Encoding != 'none' for all compressed observations",
        "observed": {"values_seen": unique_encs, "failure_count": all_encs.count("none"), "sample": []},
        "pass": c_compression_pass,
    }

    # C_DECOMPRESSION_DETERMINISM: within-state decompressed hash variation = 0
    decomp_variation = {}
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "/userinfo" in ep_key:
                for state, hv in ep_data["decompressed_hash_variation"].items():
                    if state not in decomp_variation:
                        decomp_variation[state] = []
                    decomp_variation[state].append(hv["all_same"])

    c_decomp_det_pass = all(all(v) for v in decomp_variation.values()) if decomp_variation else False
    control_details["C_DECOMPRESSION_DETERMINISM"] = {
        "expected": "Within-state decompressed hash variation = 0 for all states across all content types × sizes",
        "observed": {state: all(values) for state, values in decomp_variation.items()},
        "pass": c_decomp_det_pass,
    }

    # C_NULL_CONTROL: B-RANDOM ~ 0.0
    b_random_values = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "/userinfo" in ep_key:
                b_random_values.append(ep_data["baselines"]["B-RANDOM"])
    c_null_pass = all(v is not None and abs(v) < 0.1 for v in b_random_values) if b_random_values else False
    control_details["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0 at all conditions",
        "observed": [float(v) for v in b_random_values],
        "pass": c_null_pass,
    }

    # C_BROTLI_QUALITY_SCALING: unique compressed hashes at 100KB > unique at 1KB for HTML
    quality_diversity_1kb = []
    quality_diversity_100kb = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "HTML" in ep_key and "1KB" in ep_key:
                for state, hv in ep_data["compressed_hash_variation"].items():
                    quality_diversity_1kb.append(hv["unique_count"])
            elif "HTML" in ep_key and "100KB" in ep_key:
                for state, hv in ep_data["compressed_hash_variation"].items():
                    quality_diversity_100kb.append(hv["unique_count"])

    avg_diversity_1kb = sum(quality_diversity_1kb) / len(quality_diversity_1kb) if quality_diversity_1kb else 0
    avg_diversity_100kb = sum(quality_diversity_100kb) / len(quality_diversity_100kb) if quality_diversity_100kb else 0
    c_brotli_scaling_pass = avg_diversity_100kb > avg_diversity_1kb
    control_details["C_BROTLI_QUALITY_SCALING"] = {
        "expected": "Unique compressed hashes at 100KB > unique at 1KB for HTML",
        "observed": {
            "avg_diversity_1kb": avg_diversity_1kb,
            "avg_diversity_100kb": avg_diversity_100kb,
            "scaling_observed": c_brotli_scaling_pass,
        },
        "pass": c_brotli_scaling_pass,
    }

    # C_NO_PIPELINE_ERRORS
    c_pipeline_pass = len(errors) == 0
    control_details["C_NO_PIPELINE_ERRORS"] = {
        "expected": "0 errors across all requests",
        "observed": len(errors),
        "pass": c_pipeline_pass,
    }

    # C_REGRESSION_JSON: JSON discrimination at 1KB ≥ 0.3
    json_disc_1kb = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "JSON" in ep_key and "1KB" in ep_key and "/userinfo" in ep_key:
                json_disc_1kb.append(ep_data["decompressed_body_only_discrimination"])
    c_regression_json_pass = all(d >= 0.3 for d in json_disc_1kb) if json_disc_1kb else False
    control_details["C_REGRESSION_JSON"] = {
        "expected": "JSON decompressed body-only discrimination ≥ 0.3 at 1KB (regression from parent)",
        "observed": json_disc_1kb,
        "pass": c_regression_json_pass,
    }

    # =========================================================================
    # DECISION RULE (from frozen spec.json)
    # =========================================================================

    # Condition 1: JSON decompressed body-only discrimination ≥ 0.3 at all 3 sizes (regression)
    json_disc_all_sizes = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "JSON" in ep_key and "/userinfo" in ep_key:
                json_disc_all_sizes.append(ep_data["decompressed_body_only_discrimination"])
    c1_pass = all(d >= 0.3 for d in json_disc_all_sizes) if json_disc_all_sizes else False

    # Condition 2: HTML decompressed body-only discrimination ≥ 0.3 at all 3 sizes
    html_disc_all_sizes = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "HTML" in ep_key and "/userinfo" in ep_key:
                html_disc_all_sizes.append(ep_data["decompressed_body_only_discrimination"])
    c2_pass = all(d >= 0.3 for d in html_disc_all_sizes) if html_disc_all_sizes else False

    # Condition 3: XML decompressed body-only discrimination ≥ 0.3 at all 3 sizes
    xml_disc_all_sizes = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "XML" in ep_key and "/userinfo" in ep_key:
                xml_disc_all_sizes.append(ep_data["decompressed_body_only_discrimination"])
    c3_pass = all(d >= 0.3 for d in xml_disc_all_sizes) if xml_disc_all_sizes else False

    # Condition 4: decompressed_hash_variation all_same=true for all content types × sizes × states
    c4_pass = c_decomp_det_pass

    # Condition 5: B-RANDOM = 0.0 for all conditions
    c5_pass = c_null_pass

    # Condition 6: |brotli - gzip| < 0.1 for all content types × sizes
    algo_eq_diffs = []
    for key1, baseline_data1 in all_results.items():
        for key2, baseline_data2 in all_results.items():
            if key1 != key2:
                # Find matching conditions (same content type, size, endpoint)
                for ep_key1, ep_data1 in baseline_data1.items():
                    for ep_key2, ep_data2 in baseline_data2.items():
                        # Check if same content type, size, and endpoint
                        if (ep_key1.split("_")[0] == ep_key2.split("_")[0] and
                            "BROTLI" in key1 and "GZIP" in key2):
                            diff = abs(ep_data1["decompressed_body_only_discrimination"] -
                                      ep_data2["decompressed_body_only_discrimination"])
                            algo_eq_diffs.append(diff)

    c6_pass = all(d < 0.1 for d in algo_eq_diffs) if algo_eq_diffs else False

    survives = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass and c6_pass

    # Check for FALSIFIED-IN-SETTING: any non-JSON type has discrimination < 0.3
    non_json_disc = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if ("HTML" in ep_key or "XML" in ep_key) and "/userinfo" in ep_key:
                non_json_disc.append(ep_data["decompressed_body_only_discrimination"])

    falsified_in_setting = any(d < 0.3 for d in non_json_disc) if non_json_disc else False

    if not c_pipeline_pass:
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif survives:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif falsified_in_setting:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    else:
        outcome = "MIXED"
        status = "COMPLETE"

    # =========================================================================
    # OBSERVATIONS
    # =========================================================================

    observations = [
        f"Mock OAuth2 server started on unique ports per content type × size combination",
        f"Content types tested: {list(CONTENT_TYPES.keys())}",
        f"Payload sizes tested: {list(PAYLOAD_SIZES.keys())}",
        f"Auth states: {AUTH_STATES}",
        f"Reps per state per condition: {REPS}",
        f"Endpoints: /userinfo (GET), /introspect (POST)",
        f"Total states × reps × endpoints = {len(AUTH_STATES)} × {REPS} × 2 = {len(AUTH_STATES) * REPS * 2} per condition",
        f"Actual requests made: {request_count}",
        f"Seed: {SEED}",
        f"Brotli available: {BROTLI_AVAILABLE}",
        f"without CDN noise — WITH SERVER COMPRESSION FIX - direct compression from mock server",
        f"Brotli quality range: {BROTLI_QUALITY_RANGE}",
    ]

    # Add per-condition observations
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "/userinfo" in ep_key:
                observations.append(
                    f"{ep_key}: compressed={ep_data['compressed_body_only_discrimination']:.4f}, "
                    f"decompressed={ep_data['decompressed_body_only_discrimination']:.4f}, "
                    f"status={ep_data['status_only_discrimination']:.4f}, "
                    f"B-RANDOM={ep_data['baselines']['B-RANDOM']:.4f}"
                )

    # Add decompression latency observations
    latency_obs = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "decompression_latency_ms" in ep_data:
                latency = ep_data["decompression_latency_ms"]
                latency_obs.append(f"{ep_key}: mean={latency['mean']:.3f}ms, min={latency['min']:.3f}ms, max={latency['max']:.3f}ms")

    if latency_obs:
        observations.append("Decompression latency per response:")
        observations.extend(latency_obs)

    # =========================================================================
    # VALIDITY NOTES
    # =========================================================================

    validity_notes = [
        "Mock OAuth2 server (not Keycloak) returning JSON/HTML/XML responses",
        "Fingerprint algorithm: SHA-256(repr((status, body_sha256, ''))) for compressed and decompressed",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "expired_token is locally-signed HS256, not real expired token",
        f"Brotli module available: {BROTLI_AVAILABLE}",
        "without CDN noise — WITH SERVER COMPRESSION FIX - isolates content-type and size effects from CDN non-determinism",
        "Content types are synthetic but structurally realistic",
        "Payload sizes controlled by padding (repeating blocks) to hit target uncompressed sizes",
        "3-way error collapse preserved: no_auth, expired_token, invalid_token share similar error bodies",
        "Same 4 auth states as parent experiments",
        f"Seed={SEED} for request ordering (deterministic across runs)",
        "Algorithm equivalence tested via |brotli_decompressed - gzip_decompressed| per condition",
        "Decompression latency measured per-response at each size for cost assessment",
        "No real CDN infrastructure used - bounded to localhost mock server",
        "Brotli quality diversity expected to increase with payload size (resolves parent '2 variants' limitation)",
        "Unique port per content type × size combination avoids port conflicts",
    ]

    if not BROTLI_AVAILABLE:
        validity_notes.append("BROTLI NOT AVAILABLE: Cannot run brotli conditions")

    if errors:
        validity_notes.append(f"Pipeline errors: {len(errors)} requests failed")
        for e in errors[:5]:
            validity_notes.append(f"  Error: {e}")

    # =========================================================================
    # UNRESOLVED
    # =========================================================================

    unresolved = [
        "Does decompression-normalization survive real CDN infrastructure (Cloudflare/Fastly/Akamai)?",
        "What is production-scale latency at N>1000 requests with MB-scale payloads?",
        "Does it work on binary content types?",
        "What happens with incorrect/missing Content-Encoding?",
        "Does it work when Content-Encoding is double-encoded?",
        "How does it perform with natural (non-padded) content at various sizes?",
    ]

    # =========================================================================
    # BUILD RESULT
    # =========================================================================

    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": control_details,
        "artifacts": [
            {"path": "raw_observations.json", "role": "raw", "description": "All HTTP observations per baseline per endpoint per state per content type per size"},
            {"path": "run_experiment.py", "role": "code", "description": "Experiment execution script"},
        ],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    # Save raw observations
    raw_obs_serializable = {}
    for key, endpoint_obs in raw_observations_all.items():
        raw_obs_serializable[key] = {}
        for ep_name, state_obs in endpoint_obs.items():
            raw_obs_serializable[key][ep_name] = {}
            for state, obs_list in state_obs.items():
                raw_obs_serializable[key][ep_name][state] = []
                for obs in obs_list:
                    raw_obs_serializable[key][ep_name][state].append({
                        "url": obs["url"],
                        "status": obs["status"],
                        "headers": obs["headers"],
                        "body_hash_compressed": obs["body_hash_compressed"],
                        "decompressed_hash": obs["decompressed_hash"],
                        "body_size": obs["body_size"],
                        "body_preview": obs["body"][:500].decode("utf-8", errors="replace"),
                        "fingerprint_compressed": obs["fingerprint_compressed"],
                        "fingerprint_decompressed": obs["fingerprint_decompressed"],
                        "fingerprint_status": obs["fingerprint_status"],
                        "content_encoding": obs["content_encoding"],
                        "baseline": obs["baseline"],
                        "content_type": obs["content_type"],
                        "payload_size": obs["payload_size"],
                        "elapsed": obs["elapsed"],
                        "decompression_latency_ms": obs["decompression_latency_ms"],
                        "timestamp": obs["timestamp"],
                        "state": obs["state"],
                        "rep": obs["rep"],
                    })

    with open("raw_observations.json", "w") as f:
        json.dump(raw_obs_serializable, f, indent=2)
    print(f"\nRaw observations saved to raw_observations.json")

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
    try:
        result = run_experiment()
    except Exception as e:
        import traceback
        traceback.print_exc()
        result = build_blocked_result(str(e))

    with open("result.json", "w") as f:
        json.dump(result, f, indent=2, cls=NumpyEncoder)
    print(f"\nResult written to result.json")
    print(f"Status: {result['status']}, Outcome: {result['outcome']}")
