#!/usr/bin/env python3
"""
EXP-RUNTIME-35237982464 - Non-Deterministic Brotli Quality Variation
=====================================================================
Tests decompression-normalization (SHA256 on decompressed body + status)
when brotli quality level varies non-deterministically per request,
simulating CDN edge-selection non-determinism.

Architecture:
  Client -> CDN Quality Proxy (random brotli quality) -> Mock OAuth2 Server

The mock server returns UNCOMPRESSED bodies. The CDN proxy intercepts
each response, decompresses if needed, and re-compresses with a randomly
selected brotli quality from {4,5,6,7,8}. Quality is selected independently
per request, simulating CDN edge non-determinism.

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
import socket
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection

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

EXPERIMENT_ID = "EXP-RUNTIME-35237982464"
LANE = "runtime"
SEED = 44
REPS = 20
BASE_PORT = 5500  # Base port for mock servers
PROXY_PORT = 5600  # Base port for CDN proxies
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

# Brotli quality range (CDN proxy selects randomly from this set)
BROTLI_QUALITY_RANGE = [4, 5, 6, 7, 8]

AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]

BROTLI_AVAILABLE = True
try:
    import brotli as _brotli_test
except ImportError:
    BROTLI_AVAILABLE = False
    print("WARNING: brotli module not available. Brotli conditions will fail.")


# ---------------------------------------------------------------------------
# CONTENT BODY GENERATORS (same as parent - deterministic per state)
# ---------------------------------------------------------------------------

def generate_json_body(state, target_size):
    """Generate JSON body for given auth state and target size."""
    if state in ("no_auth", "expired_token", "invalid_token"):
        base = {"error": "invalid_token", "message": "Authentication failed"}
    else:
        base = {"sub": "alice", "name": "Alice", "email": "alice@example.com",
                "scope": "openid profile email"}
    current_json = json.dumps(base)
    current_size = len(current_json.encode("utf-8"))
    if current_size < target_size:
        padding_needed = target_size - current_size - 20
        if padding_needed > 0:
            base["data"] = "x" * padding_needed
    return json.dumps(base).encode("utf-8")[:target_size]


def generate_html_body(state, target_size):
    """Generate HTML body for given auth state and target size."""
    if state in ("no_auth", "expired_token", "invalid_token"):
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
    encoded = base_content.encode("utf-8")
    padding_block = b"<p>Additional data padding block for size control.</p>\n"
    while len(encoded) < target_size:
        encoded += padding_block
    return encoded[:target_size]


def generate_xml_body(state, target_size):
    """Generate XML body for given auth state and target size."""
    if state in ("no_auth", "expired_token", "invalid_token"):
        base_content = """<?xml version="1.0" encoding="UTF-8"?>
<response>
<status>error</status>
<error_code>401</error_code>
<error>invalid_token</error>
<message>Authentication failed. Please provide a valid Bearer token.</message>
</response>"""
    else:
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
# MOCK OAUTH2 SERVER (returns UNCOMPRESSED bodies - no compression)
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class MockOAuthHandler(BaseHTTPRequestHandler):
    """Mock OAuth2 server that returns UNCOMPRESSED bodies.
    Compression is handled by the CDN proxy layer."""
    body_size = 1024
    content_type = "JSON"
    seed = 44

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
        return CONTENT_TYPES.get(self.content_type, "application/json")

    def do_GET(self):
        if self.path == USERINFO_PATH:
            state = "valid_token" if self._check_auth() else "no_auth"
            body = self._get_body(state, self.body_size)
            status = 200 if self._check_auth() else 401

            # Return UNCOMPRESSED - CDN proxy handles compression
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

            if self._check_auth():
                state = "valid_token"
            else:
                try:
                    jwt.decode(token, CLIENT_SECRET, algorithms=["HS256"])
                    state = "valid_token"
                except jwt.ExpiredSignatureError:
                    state = "expired_token"
                except jwt.InvalidTokenError:
                    state = "invalid_token"

            body = self._get_body(state, self.body_size)

            # Return UNCOMPRESSED - CDN proxy handles compression
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
    print(f"  Mock server started on port {port} (content_type={content_type})")
    return server


def stop_mock_server(server):
    if server:
        server.shutdown()
        server.server_close()
        time.sleep(0.3)


# ---------------------------------------------------------------------------
# CDN QUALITY PROXY
# ---------------------------------------------------------------------------

class CDNQualityProxy(BaseHTTPRequestHandler):
    """CDN proxy that intercepts responses and re-compresses with random brotli quality.
    
    Each request gets an independent random quality from {4,5,6,7,8}.
    This simulates CDN edge-selection non-determinism where different edges
    or cache hits produce different quality levels for the same content.
    """
    upstream_host = "127.0.0.1"
    upstream_port = 5400
    quality_rng = None  # Set before starting

    def log_message(self, format, *args):
        pass

    def _proxy_request(self, method="GET"):
        """Forward request to upstream server and re-compress response with random quality."""
        # Select random brotli quality for THIS request
        quality = CDNQualityProxy.quality_rng.choice(BROTLI_QUALITY_RANGE)

        # Forward request to upstream (uncompressed server)
        try:
            conn = HTTPConnection(CDNQualityProxy.upstream_host,
                                  CDNQualityProxy.upstream_port, timeout=10)
            
            # Build headers to forward
            headers = {}
            for key in self.headers:
                if key.lower() not in ("host", "accept-encoding", "connection"):
                    headers[key] = self.headers[key]

            # Read request body if present
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

            conn.request(method, self.path, body=body, headers=headers)
            upstream_resp = conn.getresponse()

            # Read upstream response (uncompressed)
            resp_status = upstream_resp.status
            resp_headers = dict(upstream_resp.getheaders())
            resp_body = upstream_resp.read()
            conn.close()

            # Re-compress with random brotli quality
            compressed = brotli.compress(resp_body, quality=quality)

            # Send compressed response to client
            self.send_response(resp_status)
            # Forward original headers except Content-Length and Content-Encoding
            for key, value in resp_headers.items():
                if key.lower() not in ("content-length", "content-encoding", "transfer-encoding"):
                    self.send_header(key, value)
            self.send_header("Content-Type", resp_headers.get("Content-Type", "application/octet-stream"))
            self.send_header("Content-Encoding", "br")
            self.send_header("Content-Length", str(len(compressed)))
            self.send_header("X-Brotli-Quality", str(quality))
            self.end_headers()
            self.wfile.write(compressed)

        except Exception as e:
            self.send_error(502, f"Proxy error: {e}")

    def do_GET(self):
        self._proxy_request("GET")

    def do_POST(self):
        self._proxy_request("POST")


def start_cdn_proxy(proxy_port, upstream_port, quality_rng):
    """Start CDN quality proxy on proxy_port, forwarding to upstream_port."""
    CDNQualityProxy.upstream_port = upstream_port
    CDNQualityProxy.quality_rng = quality_rng
    server = ReusableHTTPServer(("127.0.0.1", proxy_port), CDNQualityProxy)
    server.timeout = 0.5
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"  CDN proxy started on port {proxy_port} -> upstream {upstream_port}")
    return server


def stop_cdn_proxy(server):
    if server:
        server.shutdown()
        server.server_close()
        time.sleep(0.3)


# ---------------------------------------------------------------------------
# COMPRESS UTILITIES
# ---------------------------------------------------------------------------

def compress_gzip(data, level=9):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=level, mtime=0) as f:
        f.write(data)
    return buf.getvalue()


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

def make_request(url, method="GET", auth_header=None, body=None, timeout=10):
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
    print(f"CDN PROXY: random quality per request (simulating CDN edge non-determinism)")
    print()

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated. Length: {len(auth_token)}")

    # Two baselines: DECOMPRESSED-VARYING-BROTLI and COMPRESSED-VARYING-BROTLI
    baselines_to_run = ["DECOMPRESSED-VARYING-BROTLI", "COMPRESSED-VARYING-BROTLI"]

    port_idx = 0
    for content_type_name, content_mime in CONTENT_TYPES.items():
        print(f"\n{'='*70}")
        print(f"CONTENT TYPE: {content_type_name}")
        print(f"{'='*70}")

        for size_name, size_bytes in PAYLOAD_SIZES.items():
            print(f"\n  Payload size: {size_name} ({size_bytes} bytes)")

            # Unique ports for this condition
            server_port = BASE_PORT + port_idx
            proxy_port = PROXY_PORT + port_idx
            port_idx += 1

            # Start mock server (no compression)
            mock_server = start_mock_server(server_port, size_bytes, SEED, content_type_name)
            time.sleep(0.5)

            # Start CDN proxy (random quality brotli)
            # Use a SEPARATE RNG for quality selection to ensure independence from request ordering
            quality_rng = random.Random(SEED + 7919)  # Different seed for quality
            cdn_proxy = start_cdn_proxy(proxy_port, server_port, quality_rng)
            time.sleep(0.5)

            # Test connectivity through CDN proxy
            try:
                test_resp = requests.get(
                    f"http://127.0.0.1:{proxy_port}{USERINFO_PATH}",
                    headers={"Authorization": f"Bearer {auth_token}"},
                    timeout=5)
                ce = test_resp.headers.get("Content-Encoding", "none")
                xq = test_resp.headers.get("X-Brotli-Quality", "none")
                print(f"    CDN proxy test: status={test_resp.status_code}, "
                      f"body_size={len(test_resp.content)}, ce={ce}, quality={xq}")
            except Exception as e:
                print(f"    WARNING: CDN proxy test failed: {e}")

            for baseline_name in baselines_to_run:
                print(f"\n    Baseline: {baseline_name}")

                condition_results = {}
                condition_raw_obs = {}

                for ep_name, ep_url_path, ep_method in [
                    ("/userinfo", USERINFO_PATH, "GET"),
                    ("/introspect", INTROSPECT_PATH, "POST"),
                ]:
                    # Request ordering RNG
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
                    quality_values_seen = []

                    for i, (state, rep) in enumerate(plan):
                        auth_header = get_auth_header(state, auth_token)

                        # Build request body for POST
                        body = None
                        if ep_method == "POST":
                            token_map = {
                                "no_auth": "",
                                "valid_token": auth_token,
                                "expired_token": make_expired_token(),
                                "invalid_token": make_invalid_token(),
                            }
                            body_data = {
                                "token": token_map.get(state, ""),
                                "client_id": "spider-client",
                                "client_secret": CLIENT_SECRET,
                            }
                            body = "&".join(f"{k}={v}" for k, v in body_data.items())

                        url = f"http://127.0.0.1:{proxy_port}{ep_url_path}"

                        try:
                            obs = make_request(url, method=ep_method,
                                               auth_header=auth_header, body=body)
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
                            xq = obs["headers"].get("X-Brotli-Quality", "none")
                            obs["brotli_quality"] = xq
                            quality_values_seen.append(xq)

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

                    # Quality values per state
                    quality_per_state = {}
                    for state, obs_list in raw_observations.items():
                        qualities = [obs["brotli_quality"] for obs in obs_list]
                        quality_per_state[state] = {
                            "values": list(set(qualities)),
                            "unique_count": len(set(qualities)),
                            "total": len(qualities),
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
                        "quality_values_seen": quality_per_state,
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
                    print(f"        Quality values seen: {list(set(quality_values_seen))}")

                    for state in AUTH_STATES:
                        chv = compressed_hash_variation[state]
                        dhv = decompressed_hash_variation[state]
                        qv = quality_per_state[state]
                        print(f"        {state}: compressed_unique={chv['unique_count']}/{chv['total']} "
                              f"decompressed_unique={dhv['unique_count']}/{dhv['total']} "
                              f"qualities={qv['unique_count']}")

                raw_observations_all[f"{content_type_name}_{size_name}_{baseline_name}"] = condition_raw_obs
                all_results[f"{content_type_name}_{size_name}_{baseline_name}"] = condition_results

            stop_cdn_proxy(cdn_proxy)
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

    # C_QUALITY_VARIATION_EXISTS: At least 2 distinct brotli quality levels per content type x size
    # (positive control - verifies CDN proxy actually varies quality)
    quality_variation_results = {}
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "/userinfo" in ep_key:
                for state, qv in ep_data["quality_values_seen"].items():
                    if state not in quality_variation_results:
                        quality_variation_results[state] = []
                    quality_variation_results[state].append(qv["unique_count"])

    c_quality_pass = all(
        all(cnt >= 2 for cnt in state_counts)
        for state_counts in quality_variation_results.values()
    ) if quality_variation_results else False

    control_details["C_QUALITY_VARIATION_EXISTS"] = {
        "expected": ">= 2 distinct brotli quality levels per content type x size (verifies CDN proxy varies quality)",
        "observed": quality_variation_results,
        "pass": c_quality_pass,
    }

    # C_NULL_CONTROL: B-RANDOM ~ 0.0 for all conditions
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
        "expected": "Within-state decompressed hash variation = 0 for all states across all content types x sizes",
        "observed": {state: all(values) for state, values in decomp_variation.items()},
        "pass": c_decomp_det_pass,
    }

    # C_COMPRESSION_ACTIVE: Content-Encoding != 'none' for all compressed observations
    all_encs = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            for state, cv in ep_data["compression_verification"].items():
                all_encs.extend(cv["content_encoding_values"])
    unique_encs = list(set(all_encs))
    c_compression_pass = all(e in ("br",) for e in unique_encs) and "none" not in unique_encs
    control_details["C_COMPRESSION_ACTIVE"] = {
        "expected": "Content-Encoding = 'br' for all CDN proxy observations",
        "observed": {"values_seen": unique_encs, "failure_count": all_encs.count("none")},
        "pass": c_compression_pass,
    }

    # C_NO_PIPELINE_ERRORS
    c_pipeline_pass = len(errors) == 0
    control_details["C_NO_PIPELINE_ERRORS"] = {
        "expected": "0 errors across all requests",
        "observed": len(errors),
        "pass": c_pipeline_pass,
    }

    # =========================================================================
    # DECISION RULE (from frozen spec.json)
    # =========================================================================

    # Condition 1: JSON decompressed body-only discrimination >= 0.3 at all 3 sizes
    json_disc_all_sizes = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "JSON" in ep_key and "/userinfo" in ep_key:
                json_disc_all_sizes.append(ep_data["decompressed_body_only_discrimination"])
    c1_pass = all(d >= 0.3 for d in json_disc_all_sizes) if json_disc_all_sizes else False

    # Condition 2: HTML decompressed body-only discrimination >= 0.3 at all 3 sizes
    html_disc_all_sizes = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "HTML" in ep_key and "/userinfo" in ep_key:
                html_disc_all_sizes.append(ep_data["decompressed_body_only_discrimination"])
    c2_pass = all(d >= 0.3 for d in html_disc_all_sizes) if html_disc_all_sizes else False

    # Condition 3: XML decompressed body-only discrimination >= 0.3 at all 3 sizes
    xml_disc_all_sizes = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "XML" in ep_key and "/userinfo" in ep_key:
                xml_disc_all_sizes.append(ep_data["decompressed_body_only_discrimination"])
    c3_pass = all(d >= 0.3 for d in xml_disc_all_sizes) if xml_disc_all_sizes else False

    # Condition 4: decompressed_hash_variation all_same=true for all content types x sizes x states
    c4_pass = c_decomp_det_pass

    # Condition 5: B-RANDOM = 0.0 for all conditions
    c5_pass = c_null_pass

    # Condition 6: C_QUALITY_VARIATION_EXISTS passes
    c6_pass = c_quality_pass

    survives = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass and c6_pass

    # Check for FALSIFIED-IN-SETTING: any content type has discrimination < 0.3
    all_type_disc = []
    for key, baseline_data in all_results.items():
        for ep_key, ep_data in baseline_data.items():
            if "/userinfo" in ep_key:
                all_type_disc.append((ep_key, ep_data["decompressed_body_only_discrimination"]))

    falsified_in_setting = any(d < 0.3 for _, d in all_type_disc)

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
        f"CDN Quality Proxy architecture: Client -> CDN Proxy (random brotli quality) -> Mock Server (uncompressed)",
        f"Content types tested: {list(CONTENT_TYPES.keys())}",
        f"Payload sizes tested: {list(PAYLOAD_SIZES.keys())}",
        f"Auth states: {AUTH_STATES}",
        f"Reps per state per condition: {REPS}",
        f"Endpoints: /userinfo (GET), /introspect (POST)",
        f"Total states x reps x endpoints = {len(AUTH_STATES)} x {REPS} x 2 = {len(AUTH_STATES) * REPS * 2} per condition",
        f"Actual requests made: {request_count}",
        f"Seed: {SEED} (request ordering), quality RNG seed: {SEED + 7919} (independent)",
        f"Brotli available: {BROTLI_AVAILABLE}",
        f"Brotli quality range: {BROTLI_QUALITY_RANGE} (random per request)",
        f"CDN proxy selects quality UNIFORMLY AT RANDOM per request from {{4,5,6,7,8}}",
        f"Mock server returns UNCOMPRESSED bodies - CDN proxy handles all compression",
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
                latency_obs.append(f"{ep_key}: mean={latency['mean']:.3f}ms, "
                                   f"min={latency['min']:.3f}ms, max={latency['max']:.3f}ms")

    if latency_obs:
        observations.append("Decompression latency per response:")
        observations.extend(latency_obs)

    # =========================================================================
    # VALIDITY NOTES
    # =========================================================================

    validity_notes = [
        "Architecture: Client -> CDN Quality Proxy (random brotli quality) -> Mock OAuth2 Server (uncompressed)",
        "CDN proxy decompresses server response (if needed) and re-compresses with random brotli quality",
        "Quality selection uses SEPARATE RNG (seed=SEED+7919) from request ordering (seed=SEED)",
        "Mock server generates UNCOMPRESSED bodies - deterministic per auth state",
        "CDN proxy applies random brotli quality {4,5,6,7,8} per request independently",
        "This simulates CDN edge-selection non-determinism where different edges produce different quality levels",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "expired_token is locally-signed HS256, not real expired token",
        f"Brotli module available: {BROTLI_AVAILABLE}",
        "Content types are synthetic but structurally realistic",
        "Payload sizes controlled by padding to hit target uncompressed sizes",
        "3-way error collapse preserved: no_auth, expired_token, invalid_token share similar error bodies",
        "Same 4 auth states as parent experiments",
        f"Seed={SEED} for request ordering, separate seed for quality selection",
        "No Accept-Encoding negotiation - client always requests brotli",
        "No chunked transfer-encoding - responses use Content-Length",
        "No real CDN infrastructure - bounded to localhost mock server + CDN proxy",
        "CDN proxy quality variation is uniform random, not content-dependent",
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
        "Does it handle CDN-specific phenomena: caching, chunked transfer-encoding, Accept-Encoding negotiation?",
        "What is production-scale latency at N>1000 requests with MB-scale payloads?",
        "Does brotli quality diversity increase with natural (non-padded) content at larger sizes?",
        "Does decompression-normalization work for binary content types?",
        "What happens with incorrect, missing, or double-encoded Content-Encoding?",
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
            {"path": "raw_observations.json", "role": "raw",
             "description": "All HTTP observations through CDN quality proxy per endpoint per state per content type per size"},
            {"path": "run_experiment.py", "role": "code",
             "description": "Experiment execution script with CDN quality proxy"},
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
                        "brotli_quality": obs["brotli_quality"],
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
