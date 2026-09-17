#!/usr/bin/env python3
"""
EXP-RUNTIME-35280364816 - Iterative Decompression for Multi-Layer Encoding
==========================================================================
Tests iterative decompression (decompress repeatedly until failure or max_depth=5)
under CDN-like encoding-layer non-determinism including double-brotli and triple-brotli.

Architecture:
  Client (iterative decompression) -> CDN Encoding Proxy (random encoding scenario) -> Mock OAuth2 Server

The mock server returns brotli-compressed responses at quality 6 (deterministic).
The CDN proxy intercepts each response and applies ONE OF SIX encoding scenarios:
1. Correct 'br' - standard brotli (baseline)
2. Missing Content-Encoding - no header, identity transfer
3. Incorrect 'gzip' label - brotli bytes served with Content-Encoding: gzip
4. Double-encoded 'br' - brotli bytes wrapped in another brotli layer (depth=2)
5. Triple-encoded 'br' - brotli bytes wrapped in three brotli layers (depth=3) -- NEW
6. Garbled 'br; quality=invalid' - malformed Content-Encoding value

The ONLY code change from parent EXP-RUNTIME-35262264593 is in decompress_body():
  Replace single-pass brotli/gzip/identity decompression with iterative decompression
  that loops until failure or max_depth=5.

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

EXPERIMENT_ID = "EXP-RUNTIME-35280364816"
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

# Brotli quality for mock server (deterministic baseline)
MOCK_BROTLI_QUALITY = 6

# Encoding scenarios (6 total - parent had 5, we add triple_br)
ENCODING_SCENARIOS = [
    "correct_br",
    "missing_ce",
    "incorrect_gzip",
    "double_br",
    "triple_br",    # NEW: triple brotli encoding
    "garbled_ce",
]

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
# MOCK OAUTH2 SERVER (returns BROTLI-COMPRESSED bodies at quality 6)
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class MockOAuthHandler(BaseHTTPRequestHandler):
    """Mock OAuth2 server that returns brotli-compressed responses at quality 6.
    
    The CDN encoding proxy applies encoding-layer non-determinism on top.
    """
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

            # Compress with brotli quality 6 (deterministic)
            compressed = brotli.compress(body, quality=MOCK_BROTLI_QUALITY)

            self.send_response(status)
            self.send_header("Content-Type", self._get_mime_type())
            self.send_header("Content-Encoding", "br")
            self.send_header("Content-Length", str(len(compressed)))
            self.send_header("X-Server-Quality", str(MOCK_BROTLI_QUALITY))
            self.end_headers()
            self.wfile.write(compressed)
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

            # Compress with brotli quality 6 (deterministic)
            compressed = brotli.compress(body, quality=MOCK_BROTLI_QUALITY)

            self.send_response(200)
            self.send_header("Content-Type", self._get_mime_type())
            self.send_header("Content-Encoding", "br")
            self.send_header("Content-Length", str(len(compressed)))
            self.send_header("X-Server-Quality", str(MOCK_BROTLI_QUALITY))
            self.end_headers()
            self.wfile.write(compressed)
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
# CDN ENCODING PROXY (applies encoding-layer non-determinism)
# ---------------------------------------------------------------------------

class CDNEncodingProxy(BaseHTTPRequestHandler):
    """CDN proxy that intercepts responses and applies random encoding scenarios.
    
    Each request gets an independent random encoding scenario, simulating CDN
    edge non-determinism in Accept-Encoding negotiation, cache poisoning,
    or misconfigured origins.
    
    Scenarios:
    1. correct_br: Standard brotli, passes through as-is
    2. missing_ce: Removes Content-Encoding header (identity transfer)
    3. incorrect_gzip: Serves brotli bytes with Content-Encoding: gzip
    4. double_br: Wraps brotli bytes in another brotli layer (depth=2)
    5. triple_br: Wraps brotli bytes in three brotli layers (depth=3) -- NEW
    6. garbled_ce: Sets Content-Encoding to malformed value
    """
    upstream_host = "127.0.0.1"
    upstream_port = 5400
    scenario_rng = None  # Set before starting

    def log_message(self, format, *args):
        pass

    def _apply_encoding_scenario(self, resp_body, resp_status, resp_headers, scenario):
        """Apply encoding transformation based on scenario."""
        server_ce = resp_headers.get("Content-Encoding", "br")
        server_q = resp_headers.get("X-Server-Quality", "6")
        
        if scenario == "correct_br":
            # Pass through as-is (standard brotli)
            return resp_body, "br", {}
        
        elif scenario == "missing_ce":
            # Remove Content-Encoding header - client receives raw brotli bytes
            # but with no encoding indicator
            return resp_body, None, {}
        
        elif scenario == "incorrect_gzip":
            # Serve brotli bytes with Content-Encoding: gzip
            return resp_body, "gzip", {}
        
        elif scenario == "double_br":
            # Wrap brotli bytes in another brotli layer
            double_compressed = brotli.compress(resp_body, quality=MOCK_BROTLI_QUALITY)
            return double_compressed, "br", {}
        
        elif scenario == "triple_br":
            # Wrap brotli bytes in three brotli layers
            once = brotli.compress(resp_body, quality=MOCK_BROTLI_QUALITY)
            twice = brotli.compress(once, quality=MOCK_BROTLI_QUALITY)
            thrice = brotli.compress(twice, quality=MOCK_BROTLI_QUALITY)
            return thrice, "br", {}
        
        elif scenario == "garbled_ce":
            # Set Content-Encoding to malformed value
            return resp_body, "br; quality=invalid", {}
        
        else:
            # Unknown scenario, pass through
            return resp_body, "br", {}

    def _proxy_request(self, method="GET"):
        """Forward request to upstream server and apply encoding transformation."""
        # Select random encoding scenario for THIS request
        scenario = CDNEncodingProxy.scenario_rng.choice(ENCODING_SCENARIOS)

        # Forward request to upstream (brotli-compressed server)
        try:
            conn = HTTPConnection(CDNEncodingProxy.upstream_host,
                                  CDNEncodingProxy.upstream_port, timeout=10)
            
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

            # Read upstream response (brotli-compressed)
            resp_status = upstream_resp.status
            resp_headers = dict(upstream_resp.getheaders())
            resp_body = upstream_resp.read()
            conn.close()

            # Apply encoding transformation
            transformed_body, new_ce, extra_headers = self._apply_encoding_scenario(
                resp_body, resp_status, resp_headers, scenario
            )

            # Send transformed response to client
            self.send_response(resp_status)
            # Forward original headers except Content-Length and Content-Encoding
            for key, value in resp_headers.items():
                if key.lower() not in ("content-length", "content-encoding", 
                                       "transfer-encoding", "x-server-quality"):
                    self.send_header(key, value)
            self.send_header("Content-Type", resp_headers.get("Content-Type", "application/octet-stream"))
            
            # Set transformed Content-Encoding
            if new_ce is not None:
                self.send_header("Content-Encoding", new_ce)
            
            self.send_header("Content-Length", str(len(transformed_body)))
            self.send_header("X-Encoding-Scenario", scenario)
            self.send_header("X-Server-Quality", resp_headers.get("X-Server-Quality", "6"))
            for key, value in extra_headers.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(transformed_body)

        except Exception as e:
            self.send_error(502, f"Proxy error: {e}")

    def do_GET(self):
        self._proxy_request("GET")

    def do_POST(self):
        self._proxy_request("POST")


def start_cdn_proxy(proxy_port, upstream_port, scenario_rng):
    """Start CDN encoding proxy on proxy_port, forwarding to upstream_port."""
    CDNEncodingProxy.upstream_port = upstream_port
    CDNEncodingProxy.scenario_rng = scenario_rng
    server = ReusableHTTPServer(("127.0.0.1", proxy_port), CDNEncodingProxy)
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


# ---------------------------------------------------------------------------
# ITERATIVE DECOMPRESSION (the ONLY change from parent)
# ---------------------------------------------------------------------------

def decompress_body(raw_body, content_encoding):
    """Iteratively decompress body based on Content-Encoding header.
    
    KEY CHANGE from parent: This function decompresses repeatedly until 
    decompression fails or max_depth=5 is reached, then returns the final output.
    
    At each iteration:
    1. Try brotli decompress
    2. If brotli fails, try gzip decompress
    3. If gzip fails, return current data (identity)
    4. If brotli or gzip succeeded, increment depth and repeat from step 1
    
    This handles:
    - Single-layer encoding (correct_br, missing_ce, incorrect_gzip, garbled_ce)
    - Double-encoded brotli (brotli(brotli(body))) - depth=2
    - Triple-encoded brotli (brotli(brotli(brotli(body)))) - depth=3
    """
    MAX_DEPTH = 5
    current_data = raw_body
    depth = 0
    decompression_log = []  # Track what happened at each depth
    
    while depth < MAX_DEPTH:
        # Try brotli decompress first
        try:
            decompressed = brotli.decompress(current_data)
            decompression_log.append(f"depth={depth}: brotli decompress success ({len(current_data)} -> {len(decompressed)} bytes)")
            current_data = decompressed
            depth += 1
            continue  # Try next iteration
        except Exception:
            pass
        
        # If brotli fails, try gzip
        try:
            decompressed = gzip.decompress(current_data)
            decompression_log.append(f"depth={depth}: gzip decompress success ({len(current_data)} -> {len(decompressed)} bytes)")
            current_data = decompressed
            depth += 1
            continue  # Try next iteration
        except Exception:
            pass
        
        # If both fail, we're done (identity / already decompressed)
        decompression_log.append(f"depth={depth}: no valid decompression, returning current data")
        break
    
    if depth >= MAX_DEPTH:
        decompression_log.append(f"reached max_depth={MAX_DEPTH}, stopping")
    
    return current_data


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
    print(f"Encoding scenarios: {ENCODING_SCENARIOS}")
    print(f"CDN PROXY: random encoding scenario per request (simulating CDN edge non-determinism)")
    print(f"MAX DECOMPRESSION DEPTH: 5")
    print()

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated. Length: {len(auth_token)}")

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

            # Start mock server (brotli-compressed at quality 6)
            mock_server = start_mock_server(server_port, size_bytes, SEED, content_type_name)
            time.sleep(0.5)

            # Start CDN proxy (random encoding scenario)
            # Use a SEPARATE RNG for scenario selection to ensure independence from request ordering
            scenario_rng = random.Random(SEED + 7919)  # Different seed for scenario
            cdn_proxy = start_cdn_proxy(proxy_port, server_port, scenario_rng)
            time.sleep(0.5)

            # Test connectivity through CDN proxy
            try:
                test_resp = requests.get(
                    f"http://127.0.0.1:{proxy_port}{USERINFO_PATH}",
                    headers={"Authorization": f"Bearer {auth_token}"},
                    timeout=5)
                ce = test_resp.headers.get("Content-Encoding", "none")
                xes = test_resp.headers.get("X-Encoding-Scenario", "none")
                print(f"    CDN proxy test: status={test_resp.status_code}, "
                      f"body_size={len(test_resp.content)}, ce={ce}, scenario={xes}")
            except Exception as e:
                print(f"    WARNING: CDN proxy test failed: {e}")

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
            encoding_scenarios_seen = []
            decompression_errors = []

            for i, (state, rep) in enumerate(plan):
                auth_header = get_auth_header(state, auth_token)

                # Build request body for POST
                body = None
                if True:  # Test both endpoints
                    ep_name, ep_url_path, ep_method = (
                        "/userinfo", USERINFO_PATH, "GET")
                    
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
                        obs["content_type"] = content_type_name
                        obs["payload_size"] = size_name
                        obs["fingerprint_compressed"] = fingerprint_compressed_only(obs)
                        obs["fingerprint_decompressed"] = fingerprint_decompressed(obs)
                        obs["fingerprint_status"] = fingerprint_status_only(obs)
                        obs["body_hash_compressed"] = hashlib.sha256(obs["body"]).hexdigest()
                        obs["body_size"] = len(obs["body"])

                        ce = obs["headers"].get("Content-Encoding", "none")
                        obs["content_encoding"] = ce
                        xes = obs["headers"].get("X-Encoding-Scenario", "none")
                        obs["encoding_scenario"] = xes
                        encoding_scenarios_seen.append(xes)

                        # Measure decompression latency and track errors
                        decomp_start = time.monotonic()
                        try:
                            decompressed = decompress_body(obs["body"], ce)
                            decomp_elapsed = time.monotonic() - decomp_start
                            obs["decompression_latency_ms"] = decomp_elapsed * 1000
                            decompression_latencies.append(decomp_elapsed * 1000)
                            obs["decompressed_hash"] = hashlib.sha256(decompressed).hexdigest()
                            obs["decompression_error"] = None
                        except Exception as e:
                            decomp_elapsed = time.monotonic() - decomp_start
                            obs["decompression_latency_ms"] = decomp_elapsed * 1000
                            decompression_errors.append({
                                "state": state, "rep": rep, "scenario": xes,
                                "error": str(e)
                            })
                            obs["decompression_error"] = str(e)
                            # Use raw body hash as fallback
                            obs["decompressed_hash"] = hashlib.sha256(obs["body"]).hexdigest()

                        raw_observations[state].append(obs)

                        # Track fingerprints
                        fingerprints_compressed_by_state[state].append(obs["fingerprint_compressed"])
                        fingerprints_decompressed_by_state[state].append(obs["fingerprint_decompressed"])
                        fingerprints_status_by_state[state].append(obs["fingerprint_status"])

                        request_count += 1
                    except Exception as e:
                        errors.append({"endpoint": ep_name,
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

            # Encoding scenario distribution per state
            scenario_distribution = {}
            for state, obs_list in raw_observations.items():
                scenarios = [obs["encoding_scenario"] for obs in obs_list]
                scenario_distribution[state] = {
                    "values": list(set(scenarios)),
                    "unique_count": len(set(scenarios)),
                    "total": len(scenarios),
                }

            # Content-Encoding values per state
            ce_distribution = {}
            for state, obs_list in raw_observations.items():
                ce_values = [obs["content_encoding"] for obs in obs_list]
                ce_distribution[state] = {
                    "values": list(set(ce_values)),
                    "unique_count": len(set(ce_values)),
                    "total": len(ce_values),
                }

            ep_key = f"/userinfo_{content_type_name}_{size_name}"
            all_results[ep_key] = {
                "compressed_body_only_discrimination": compressed_disc,
                "decompressed_body_only_discrimination": decompressed_disc,
                "status_only_discrimination": status_disc,
                "baselines": {
                    "B-RANDOM": b_rand_disc,
                },
                "compressed_hash_variation": compressed_hash_variation,
                "decompressed_hash_variation": decompressed_hash_variation,
                "encoding_scenarios_seen": scenario_distribution,
                "content_encoding_values": ce_distribution,
                "body_sizes": body_sizes,
                "total_requests": sum(len(v) for v in raw_observations.values()),
                "decompression_latency_ms": {
                    "mean": sum(decompression_latencies) / len(decompression_latencies) if decompression_latencies else 0,
                    "min": min(decompression_latencies) if decompression_latencies else 0,
                    "max": max(decompression_latencies) if decompression_latencies else 0,
                },
                "decompression_errors": decompression_errors,
            }
            raw_observations_all[f"{content_type_name}_{size_name}"] = raw_observations

            print(f"      /userinfo: compressed={compressed_disc:.4f}, "
                  f"decompressed={decompressed_disc:.4f}, "
                  f"status={status_disc:.4f}, B-RANDOM={b_rand_disc:.4f}")
            print(f"        Encoding scenarios seen: {list(set(encoding_scenarios_seen))}")
            if decompression_errors:
                print(f"        Decompression errors: {len(decompression_errors)}")

            for state in AUTH_STATES:
                chv = compressed_hash_variation[state]
                dhv = decompressed_hash_variation[state]
                sd = scenario_distribution[state]
                print(f"        {state}: compressed_unique={chv['unique_count']}/{chv['total']} "
                      f"decompressed_unique={dhv['unique_count']}/{dhv['total']} "
                      f"scenarios={sd['unique_count']}")

            stop_cdn_proxy(cdn_proxy)
            stop_mock_server(mock_server)
            time.sleep(0.3)

    # =========================================================================
    # ASSEMBLE METRICS
    # =========================================================================

    metrics = all_results

    # =========================================================================
    # CONTROLS
    # =========================================================================

    control_details = {}

    # C_ENCODING_VARIATION_EXISTS: At least 4 distinct encoding scenarios per content type x size
    # (6 scenarios total, need at least 4 observed per state per condition)
    scenario_variation_results = {}
    for ep_key, ep_data in all_results.items():
        for state, sd in ep_data["encoding_scenarios_seen"].items():
            if state not in scenario_variation_results:
                scenario_variation_results[state] = []
            scenario_variation_results[state].append(sd["unique_count"])

    c_encoding_pass = all(
        all(cnt >= 4 for cnt in state_counts)
        for state_counts in scenario_variation_results.values()
    ) if scenario_variation_results else False

    control_details["C_ENCODING_VARIATION_EXISTS"] = {
        "expected": ">= 4 distinct encoding scenarios per content type x size (6 total)",
        "observed": scenario_variation_results,
        "pass": c_encoding_pass,
    }

    # C_NULL_CONTROL: B-RANDOM ~ 0.0 for all conditions
    b_random_values = []
    for ep_key, ep_data in all_results.items():
        b_random_values.append(ep_data["baselines"]["B-RANDOM"])
    c_null_pass = all(v is not None and abs(v) < 0.1 for v in b_random_values) if b_random_values else False
    control_details["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0 at all conditions",
        "observed": [float(v) for v in b_random_values],
        "pass": c_null_pass,
    }

    # C_DECOMPRESSION_DETERMINISM: within-state decompressed hash variation = 0
    decomp_variation = {}
    for ep_key, ep_data in all_results.items():
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

    # C_GRACEFUL_DEGRADATION: No client crashes/hangs from garbled headers
    all_errors = []
    for ep_key, ep_data in all_results.items():
        all_errors.extend(ep_data.get("decompression_errors", []))
    c_graceful_pass = len(all_errors) == 0
    control_details["C_GRACEFUL_DEGRADATION"] = {
        "expected": "No client crashes/hangs from garbled encoding headers",
        "observed": {"error_count": len(all_errors), "errors": all_errors[:5]},
        "pass": c_graceful_pass,
    }

    # C_NO_PIPELINE_ERRORS
    c_pipeline_pass = len(errors) == 0
    control_details["C_NO_PIPELINE_ERRORS"] = {
        "expected": "0 errors across all requests",
        "observed": len(errors),
        "pass": c_pipeline_pass,
    }

    # C_TRIPLE_BR_DECOMPRESSIBLE: Triple-encoded responses decompress successfully (depth <= 5)
    # Check if any triple_br scenarios had decompression errors
    triple_br_errors = []
    for ep_key, ep_data in all_results.items():
        for state_obs in raw_observations_all.get(ep_key.replace("/userinfo_", "").replace("_", "_"), {}).values():
            for obs in state_obs:
                if obs.get("encoding_scenario") == "triple_br" and obs.get("decompression_error"):
                    triple_br_errors.append(obs)
    c_triple_pass = len(triple_br_errors) == 0
    control_details["C_TRIPLE_BR_DECOMPRESSIBLE"] = {
        "expected": "Triple-encoded responses decompress successfully (depth <= 5)",
        "observed": {"triple_br_error_count": len(triple_br_errors)},
        "pass": c_triple_pass,
    }

    # =========================================================================
    # DECISION RULE (from frozen spec.json)
    # =========================================================================

    # Condition 1: JSON decompressed body-only discrimination >= 0.3 at all 3 sizes
    json_disc_all_sizes = []
    for ep_key, ep_data in all_results.items():
        if "JSON" in ep_key:
            json_disc_all_sizes.append(ep_data["decompressed_body_only_discrimination"])
    c1_pass = all(d >= 0.3 for d in json_disc_all_sizes) if json_disc_all_sizes else False

    # Condition 2: HTML decompressed body-only discrimination >= 0.3 at all 3 sizes
    html_disc_all_sizes = []
    for ep_key, ep_data in all_results.items():
        if "HTML" in ep_key:
            html_disc_all_sizes.append(ep_data["decompressed_body_only_discrimination"])
    c2_pass = all(d >= 0.3 for d in html_disc_all_sizes) if html_disc_all_sizes else False

    # Condition 3: XML decompressed body-only discrimination >= 0.3 at all 3 sizes
    xml_disc_all_sizes = []
    for ep_key, ep_data in all_results.items():
        if "XML" in ep_key:
            xml_disc_all_sizes.append(ep_data["decompressed_body_only_discrimination"])
    c3_pass = all(d >= 0.3 for d in xml_disc_all_sizes) if xml_disc_all_sizes else False

    # Condition 4: decompressed_hash_variation all_same=true for all content types x sizes x states
    c4_pass = c_decomp_det_pass

    # Condition 5: B-RANDOM = 0.0 for all conditions
    c5_pass = c_null_pass

    # Condition 6: C_ENCODING_VARIATION_EXISTS passes
    c6_pass = c_encoding_pass

    survives = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass and c6_pass

    # Check for FALSIFIED-IN-SETTING: any content type has discrimination < 0.3
    all_type_disc = []
    for ep_key, ep_data in all_results.items():
        all_type_disc.append((ep_key, ep_data["decompressed_body_only_discrimination"]))

    falsified_in_setting = any(d < 0.3 for _, d in all_type_disc)

    # Check for determinism failure (hashes differ by encoding scenario)
    determinism_failure = False
    for ep_key, ep_data in all_results.items():
        for state, hv in ep_data["decompressed_hash_variation"].items():
            if not hv["all_same"]:
                determinism_failure = True

    if not c_pipeline_pass:
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif survives:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif falsified_in_setting or determinism_failure:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    else:
        outcome = "MIXED"
        status = "COMPLETE"

    # =========================================================================
    # OBSERVATIONS
    # =========================================================================

    observations = [
        f"CDN Encoding Proxy architecture: Client (iterative decompression, max_depth=5) -> CDN Proxy (random encoding scenario) -> Mock Server (brotli quality 6)",
        f"Content types tested: {list(CONTENT_TYPES.keys())}",
        f"Payload sizes tested: {list(PAYLOAD_SIZES.keys())}",
        f"Auth states: {AUTH_STATES}",
        f"Reps per state per condition: {REPS}",
        f"Endpoints: /userinfo (GET)",
        f"Total states x reps = {len(AUTH_STATES)} x {REPS} = {len(AUTH_STATES) * REPS} per condition",
        f"Actual requests made: {request_count}",
        f"Seed: {SEED} (request ordering), scenario RNG seed: {SEED + 7919} (independent)",
        f"Brotli available: {BROTLI_AVAILABLE}",
        f"Encoding scenarios: {ENCODING_SCENARIOS} (random per request)",
        f"Mock server compresses at brotli quality {MOCK_BROTLI_QUALITY} (deterministic)",
        f"CDN proxy applies encoding transformation per request",
        f"MAX DECOMPRESSION DEPTH: 5 (iterative decompression replaces single-pass)",
        f"Triple-encoded scenario: brotli(brotli(brotli(body))) wrapped in three brotli layers",
    ]

    # Add per-condition observations
    for ep_key, ep_data in all_results.items():
        observations.append(
            f"{ep_key}: compressed={ep_data['compressed_body_only_discrimination']:.4f}, "
            f"decompressed={ep_data['decompressed_body_only_discrimination']:.4f}, "
            f"status={ep_data['status_only_discrimination']:.4f}, "
            f"B-RANDOM={ep_data['baselines']['B-RANDOM']:.4f}"
        )

    # Add encoding scenario observations
    for ep_key, ep_data in all_results.items():
        for state, sd in ep_data["encoding_scenarios_seen"].items():
            observations.append(
                f"{ep_key} {state}: encoding scenarios = {sd['unique_count']}/{sd['total']}, "
                f"values = {sd['values']}"
            )

    # Add decompression latency observations
    latency_obs = []
    for ep_key, ep_data in all_results.items():
        if "decompression_latency_ms" in ep_data:
            latency = ep_data["decompression_latency_ms"]
            latency_obs.append(f"{ep_key}: mean={latency['mean']:.3f}ms, "
                               f"min={latency['min']:.3f}ms, max={latency['max']:.3f}ms")

    if latency_obs:
        observations.append("Decompression latency per response:")
        observations.extend(latency_obs)

    # Add decompression error observations
    error_obs = []
    for ep_key, ep_data in all_results.items():
        de = ep_data.get("decompression_errors", [])
        if de:
            error_obs.append(f"{ep_key}: {len(de)} decompression errors")
            for e in de[:3]:
                error_obs.append(f"  {e['scenario']}: {e['error']}")

    if error_obs:
        observations.append("Decompression errors:")
        observations.extend(error_obs)

    # =========================================================================
    # VALIDITY NOTES
    # =========================================================================

    validity_notes = [
        "Architecture: Client (iterative decompression, max_depth=5) -> CDN Encoding Proxy (random encoding scenario) -> Mock OAuth2 Server (brotli quality 6)",
        "Mock server compresses responses with brotli quality 6 (deterministic)",
        "CDN proxy applies one of 6 encoding scenarios per request independently (parent had 5, added triple_br)",
        "Scenario selection uses SEPARATE RNG (seed=SEED+7919) from request ordering (seed=SEED)",
        "Client decompression: iterative brotli->gzip->identity, looping until failure or max_depth=5",
        "This simulates CDN edge non-determinism in Accept-Encoding negotiation, cache poisoning, or misconfigured origins",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "expired_token is locally-signed HS256, not real expired token",
        f"Brotli module available: {BROTLI_AVAILABLE}",
        "Content types are synthetic but structurally realistic",
        "Payload sizes controlled by padding to hit target uncompressed sizes",
        "3-way error collapse preserved: no_auth, expired_token, invalid_token share similar error bodies",
        f"Seed={SEED} for request ordering, separate seed for encoding scenario selection",
        "No real CDN infrastructure - bounded to localhost mock server + encoding proxy",
        "Encoding scenarios are uniform random, not content-dependent",
        "Double-encoded scenario wraps brotli bytes in another brotli layer (depth=2)",
        "Triple-encoded scenario wraps brotli bytes in three brotli layers (depth=3)",
        "Garbled scenario sets Content-Encoding to 'br; quality=invalid'",
        "ITERATIVE DECOMPRESSION replaces single-pass decompress_body() from parent",
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
        "Does iterative decompression survive real CDN infrastructure (Cloudflare/Fastly/Akamai)?",
        "Does it handle CDN-specific phenomena: caching, chunked transfer-encoding, Accept-Encoding negotiation?",
        "What is production-scale latency at N>1000 requests with MB-scale payloads?",
        "Does iterative decompression work for binary content types?",
        "How does triple-encoding interact with intermediate proxies?",
        "What happens with Content-Encoding values that are valid but unexpected (e.g., 'br', 'zstd')?",
        "What is the maximum practical decompression depth for real-world multi-layer encoding?",
        "Does iterative decompression introduce false positives on genuinely non-compressed data?",
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
             "description": "All HTTP observations through CDN encoding proxy per endpoint per state per content type per size"},
            {"path": "run_experiment.py", "role": "code",
             "description": "Experiment execution script with iterative decompression and 6 encoding scenarios"},
        ],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    # Save raw observations
    raw_obs_serializable = {}
    for key, endpoint_obs in raw_observations_all.items():
        raw_obs_serializable[key] = {}
        for state, obs_list in endpoint_obs.items():
            raw_obs_serializable[key][state] = []
            for obs in obs_list:
                raw_obs_serializable[key][state].append({
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
                    "encoding_scenario": obs["encoding_scenario"],
                    "decompression_error": obs["decompression_error"],
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
        "observations": [],
        "validity_notes": [f"BLOCKED: {reason}"],
        "unresolved": [reason],
    }


if __name__ == "__main__":
    try:
        result = run_experiment()
        with open("result.json", "w") as f:
            json.dump(result, f, indent=2, cls=NumpyEncoder)
        print(f"\nResult saved to result.json")
        print(f"Experiment complete. Outcome: {result['outcome']}, Status: {result['status']}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        result = build_blocked_result(str(e))
        with open("result.json", "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nBLOCKED: {e}")
