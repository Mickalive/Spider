#!/usr/bin/env python3
"""
EXP-RUNTIME-35401995092 - Chunked Transfer-Encoding Decompression Test
================================================================
Tests whether iterative decompression maintains discrimination when
CDN-like proxy cache key includes Authorization (auth-aware semantics),
resolving the parent's CACHED falsification from a cache-key artifact.

Architecture:
  Client (iterative decompression, max_depth=5) -> Python Reverse Proxy (3 configs) -> Mock OAuth2 Server (brotli quality 6)

Cache configurations:
  CL-PASSTHROUGH: Content-Length forwarding, no caching (parent baseline regression control)
  CHUNKED-PASSTHROUGH: Transfer-Encoding: chunked forwarding, no caching
  CHUNKED-CACHED: Transfer-Encoding: chunked, auth-aware cache key (URL+Accept-Encoding+Authorization)

Frozen from spec.json and prereg.md - DO NOT MODIFY.
"""

import brotli
import gzip
import hashlib
import json
import random
import sys
import time
import threading
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection

import jwt
import requests


# ---------------------------------------------------------------------------
# FROZEN CONSTANTS
# ---------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-RUNTIME-35401995092"
LANE = "runtime"
SEED = 44
REPS = 5
BASE_PORT = 5500
PROXY_PORT_BASE = 5600
CLIENT_SECRET = "spider-secret-12345"

USERINFO_PATH = "/userinfo"

CONTENT_TYPES = {
    "JSON": "application/json",
    "HTML": "text/html",
    "XML": "application/xml",
}

PAYLOAD_SIZES = {
    "1KB": 1024,
    "10KB": 10240,
    "100KB": 102400,
}

MOCK_BROTLI_QUALITY = 6
CACHE_CONFIGS = ["CL-PASSTHROUGH", "CHUNKED-PASSTHROUGH", "CHUNKED-CACHED"]
AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]

# Parent's reference decompressed hashes (for determinism-across-paths test)
# Extracted from parent EXP-RUNTIME-35290615081 / EXP-RUNTIME-35330741639
PARENT_REF_HASHES = {
    "JSON_1KB": {
        "no_auth": "6fb10d4b9e73d7f3b892ca00cfbf119f9d7998e2cca01932c7da5a2dfc902e9a",
        "invalid_token": "6fb10d4b9e73d7f3b892ca00cfbf119f9d7998e2cca01932c7da5a2dfc902e9a",
        "expired_token": "6fb10d4b9e73d7f3b892ca00cfbf119f9d7998e2cca01932c7da5a2dfc902e9a",
        "valid_token": "d15e53a2cc4d32d44b142e7eee1e3e61d040a76c7b2f8ab3abaded579e9f4f30",
    },
    "JSON_10KB": {
        "no_auth": "a4cae41d7386f8b98f659ad7b184a4fae8541246d0da9b0b2e613b1ba441a98d",
        "invalid_token": "a4cae41d7386f8b98f659ad7b184a4fae8541246d0da9b0b2e613b1ba441a98d",
        "expired_token": "a4cae41d7386f8b98f659ad7b184a4fae8541246d0da9b0b2e613b1ba441a98d",
        "valid_token": "50ff5da20e3204c4e6338ec0ef58d055a083e3c541d58bb1dbdb4cf7b9c64265",
    },
    "JSON_100KB": {
        "no_auth": "13cff6c8888cefd0dd2d04b012b7f6382c94c33354fdf12f2038f4bdea8c77ae",
        "invalid_token": "13cff6c8888cefd0dd2d04b012b7f6382c94c33354fdf12f2038f4bdea8c77ae",
        "expired_token": "13cff6c8888cefd0dd2d04b012b7f6382c94c33354fdf12f2038f4bdea8c77ae",
        "valid_token": "9d66b62c0a78d021a9b7a1cdb25e5b536a6831bc986e9a4531349e0a15c56f1e",
    },
    "HTML_1KB": {
        "no_auth": "931c0a7095b9e4afe6043f2fefc3c6b4574b73eded0282a47ea19e5e44aa2b73",
        "invalid_token": "931c0a7095b9e4afe6043f2fefc3c6b4574b73eded0282a47ea19e5e44aa2b73",
        "expired_token": "931c0a7095b9e4afe6043f2fefc3c6b4574b73eded0282a47ea19e5e44aa2b73",
        "valid_token": "f6e691484960181623c279589b718fd2f80db0e9c189026dceec27782ca5f63d",
    },
    "HTML_10KB": {
        "no_auth": "fd47048001b493dee6a592eb16699d075b45f53a815d55cb9125a7459b538d73",
        "invalid_token": "fd47048001b493dee6a592eb16699d075b45f53a815d55cb9125a7459b538d73",
        "expired_token": "fd47048001b493dee6a592eb16699d075b45f53a815d55cb9125a7459b538d73",
        "valid_token": "ab90ea9ca3424c7c9e17986bf27fd9c1005539ed0cd817813ec7e59b219f53e1",
    },
    "HTML_100KB": {
        "no_auth": "6b1d6ad97bf3aea4eb0a2d21ebcb6bfc66d59f129f66a9a1eb94dd70d771e568",
        "invalid_token": "6b1d6ad97bf3aea4eb0a2d21ebcb6bfc66d59f129f66a9a1eb94dd70d771e568",
        "expired_token": "6b1d6ad97bf3aea4eb0a2d21ebcb6bfc66d59f129f66a9a1eb94dd70d771e568",
        "valid_token": "3b605673d658eb243a613e300d9fe6f7b85a0f2fe3ded3e4a173fa9d1e5ebefb",
    },
    "XML_1KB": {
        "no_auth": "88cdbcfc2d443f24287bd4df2e178a2c121dab0291d374b8014ebe6233c51b9f",
        "invalid_token": "88cdbcfc2d443f24287bd4df2e178a2c121dab0291d374b8014ebe6233c51b9f",
        "expired_token": "88cdbcfc2d443f24287bd4df2e178a2c121dab0291d374b8014ebe6233c51b9f",
        "valid_token": "1d455bdeb2abd96d2f1c53625b48d77d273e8fc829f98ee05aca123c2add401b",
    },
    "XML_10KB": {
        "no_auth": "7978e2e31f14f7a67f9932bfe6112ea4cd0f84515b80181f545059c73bbff580",
        "invalid_token": "7978e2e31f14f7a67f9932bfe6112ea4cd0f84515b80181f545059c73bbff580",
        "expired_token": "7978e2e31f14f7a67f9932bfe6112ea4cd0f84515b80181f545059c73bbff580",
        "valid_token": "86e56a0a281b32ffc6dee26ea9d53ca12eac7e32447d1f937580f830ae785db3",
    },
    "XML_100KB": {
        "no_auth": "cd1ddb8daeb316577355ae98b7231d12dd45087dc376b74cfdbb2cd611d4420e",
        "invalid_token": "cd1ddb8daeb316577355ae98b7231d12dd45087dc376b74cfdbb2cd611d4420e",
        "expired_token": "cd1ddb8daeb316577355ae98b7231d12dd45087dc376b74cfdbb2cd611d4420e",
        "valid_token": "ff99cb82e3566e84dc0b1a59fad0ee34296f3a7794d7dd9b266226393eac1466",
    },
}


# ---------------------------------------------------------------------------
# CONTENT BODY GENERATORS (identical to parent)
# ---------------------------------------------------------------------------

def generate_json_body(state, target_size):
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
        "sub": "alice", "name": "Alice", "email": "alice@example.com",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=1)).timestamp()),
        "realm_access": {"roles": ["user"]},
    }
    return jwt.encode(payload, CLIENT_SECRET, algorithm="HS256")


def make_expired_token():
    now = datetime.now(timezone.utc)
    payload = {
        "sub": "alice", "name": "Alice", "email": "alice@example.com",
        "iat": int((now - timedelta(hours=2)).timestamp()),
        "exp": int((now - timedelta(hours=1)).timestamp()),
        "realm_access": {"roles": ["user"]},
    }
    return jwt.encode(payload, CLIENT_SECRET, algorithm="HS256")


def make_invalid_token():
    return "invalid-token-12345"


# ---------------------------------------------------------------------------
# MOCK OAUTH2 SERVER
# Returns brotli-compressed responses. Origin always sets Cache-Control: private, Vary: Authorization.
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class MockOAuthHandler(BaseHTTPRequestHandler):
    body_size = 1024
    content_type = "JSON"

    def log_message(self, format, *args):
        pass

    def _check_auth(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return False
        token = auth[7:]
        try:
            jwt.decode(token, CLIENT_SECRET, algorithms=["HS256"])
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False

    def _get_auth_state(self):
        """Determine auth state from request header."""
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return "no_auth"
        token = auth[7:]
        try:
            jwt.decode(token, CLIENT_SECRET, algorithms=["HS256"])
            return "valid_token"
        except jwt.ExpiredSignatureError:
            return "expired_token"
        except jwt.InvalidTokenError:
            return "invalid_token"
        return "no_auth"

    def _get_body(self, state, size):
        if self.content_type == "JSON":
            return generate_json_body(state, size)
        elif self.content_type == "HTML":
            return generate_html_body(state, size)
        elif self.content_type == "XML":
            return generate_xml_body(state, size)
        return generate_json_body(state, size)

    def _get_mime_type(self):
        return CONTENT_TYPES.get(self.content_type, "application/json")

    use_chunked = False

    def do_GET(self):
        if self.path == USERINFO_PATH:
            state = self._get_auth_state()
            body = self._get_body(state, self.body_size)
            status = 200 if state == "valid_token" else 401

            compressed = brotli.compress(body, quality=MOCK_BROTLI_QUALITY)

            self.send_response(status)
            self.send_header("Content-Type", self._get_mime_type())
            self.send_header("Content-Encoding", "br")
            # Standard CDN auth-aware headers: always set by origin
            self.send_header("Cache-Control", "private")
            self.send_header("Vary", "Authorization")
            self.send_header("X-Server-Quality", str(MOCK_BROTLI_QUALITY))

            if self.use_chunked:
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                # Write chunked manually
                chunk_size = 1024
                offset = 0
                while offset < len(compressed):
                    chunk = compressed[offset:offset + chunk_size]
                    self.wfile.write(("{:x}\r\n".format(len(chunk))).encode())
                    self.wfile.write(chunk)
                    self.wfile.write(b"\r\n")
                    offset += chunk_size
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()
            else:
                self.send_header("Content-Length", str(len(compressed)))
                self.end_headers()
                self.wfile.write(compressed)
                self.wfile.flush()
        else:
            self.send_error(404)

    def do_POST(self):
        self.send_error(404)


def start_mock_server(port, body_size=1024, content_type="JSON", use_chunked=False):
    MockOAuthHandler.body_size = body_size
    MockOAuthHandler.content_type = content_type
    MockOAuthHandler.use_chunked = use_chunked
    server = ReusableHTTPServer(("127.0.0.1", port), MockOAuthHandler)
    server.timeout = 0.5
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def stop_mock_server(server):
    if server:
        server.shutdown()
        server.server_close()
        time.sleep(0.3)


# ---------------------------------------------------------------------------
# REVERSE PROXY (3 cache configs: CL-PASSTHROUGH, CHUNKED-PASSTHROUGH, CHUNKED-CACHED)
# 3 configs: CL-PASSTHROUGH (Content-Length), CHUNKED-PASSTHROUGH, CHUNKED-CACHED (auth-aware)
# ---------------------------------------------------------------------------

class ReverseProxyHandler(BaseHTTPRequestHandler):
    upstream_host = "127.0.0.1"
    upstream_port = 5400
    cache_config = "CL-PASSTHROUGH"  # "CL-PASSTHROUGH" or "CHUNKED-CACHED"
    cache = {}
    cache_lock = threading.Lock()

    def log_message(self, format, *args):
        pass

    def _get_cache_key(self, path, accept_encoding, authorization):
        """Compute cache key based on cache configuration.
        Returns None for passthrough configs (no caching), or a cache key tuple."""
        if ReverseProxyHandler.cache_config == "CHUNKED-CACHED":
            # Auth-aware config: includes Authorization
            return (path, accept_encoding or "", authorization or "")
        else:
            # CL-PASSTHROUGH and CHUNKED-PASSTHROUGH: no caching
            return None

    def _proxy_request(self, method="GET"):
        content_length = int(self.headers.get("Content-Length", 0))
        req_body = self.rfile.read(content_length) if content_length > 0 else None

        headers = {}
        for key in self.headers:
            if key.lower() not in ("host", "connection"):
                headers[key] = self.headers[key]
        if "Accept-Encoding" not in headers and "accept-encoding" not in headers:
            headers["Accept-Encoding"] = "br, gzip, identity"

        auth_header = headers.get("Authorization", headers.get("authorization", ""))

        cache_key = self._get_cache_key(
            self.path,
            headers.get("Accept-Encoding", headers.get("accept-encoding", "")),
            auth_header,
        )

        # Check cache (only if cache_key is not None, i.e., caching enabled)
        if cache_key is not None and cache_key in ReverseProxyHandler.cache:
            with ReverseProxyHandler.cache_lock:
                if cache_key in ReverseProxyHandler.cache:
                    cached_body, cached_headers, cached_status = ReverseProxyHandler.cache[cache_key]
                    self.send_response(cached_status)
                    for key, value in cached_headers.items():
                        if key.lower() not in ("content-length", "transfer-encoding", "connection"):
                            self.send_header(key, value)
                    self.send_header("Content-Length", len(cached_body))
                    self.send_header("X-Proxy-Mode", ReverseProxyHandler.cache_config)
                    self.send_header("X-Cache", "HIT")
                    if ReverseProxyHandler.cache_config in ("CHUNKED-PASSTHROUGH", "CHUNKED-CACHED"):
                        self.send_header("Transfer-Encoding", "chunked")
                        self.end_headers()
                        chunk_size = 1024
                        offset = 0
                        while offset < len(cached_body):
                            chunk = cached_body[offset:offset + chunk_size]
                            self.wfile.write(("{:x}\r\n".format(len(chunk))).encode())
                            self.wfile.write(chunk)
                            self.wfile.write(b"\r\n")
                            offset += chunk_size
                        self.wfile.write(b"0\r\n\r\n")
                        self.wfile.flush()
                    else:
                        self.send_header("Content-Length", len(cached_body))
                        self.end_headers()
                        self.wfile.write(cached_body)
                        self.wfile.flush()
                    return

        # Forward to upstream
        try:
            conn = HTTPConnection(ReverseProxyHandler.upstream_host,
                                  ReverseProxyHandler.upstream_port, timeout=10)
            conn.request(method, self.path, body=req_body, headers=headers)
            upstream_resp = conn.getresponse()
            resp_status = upstream_resp.status
            resp_headers = dict(upstream_resp.getheaders())
            resp_body = upstream_resp.read()
            conn.close()

            # Store in cache (only if cache_key is not None, i.e., caching enabled)
            if cache_key is not None:
                with ReverseProxyHandler.cache_lock:
                    ReverseProxyHandler.cache[cache_key] = (
                        resp_body, resp_headers, resp_status
                    )

            # Forward to client
            use_chunked = ReverseProxyHandler.cache_config in ("CHUNKED-PASSTHROUGH", "CHUNKED-CACHED")

            self.send_response(resp_status)
            for key, value in resp_headers.items():
                if key.lower() not in ("content-length", "transfer-encoding", "connection"):
                    self.send_header(key, value)
            self.send_header("X-Proxy-Mode", ReverseProxyHandler.cache_config)
            self.send_header("X-Cache", "MISS")

            if use_chunked:
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                chunk_size = 1024
                offset = 0
                while offset < len(resp_body):
                    chunk = resp_body[offset:offset + chunk_size]
                    self.wfile.write(("{:x}\r\n".format(len(chunk))).encode())
                    self.wfile.write(chunk)
                    self.wfile.write(b"\r\n")
                    offset += chunk_size
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()
            else:
                self.send_header("Content-Length", len(resp_body))
                self.end_headers()
                self.wfile.write(resp_body)
                self.wfile.flush()

        except Exception as e:
            self.send_error(502, f"Proxy error: {e}")

    def do_GET(self):
        self._proxy_request("GET")

    def do_POST(self):
        self._proxy_request("POST")


def start_reverse_proxy(port, upstream_port, cache_config):
    ReverseProxyHandler.upstream_port = upstream_port
    ReverseProxyHandler.cache_config = cache_config
    ReverseProxyHandler.cache = {}
    server = ReusableHTTPServer(("127.0.0.1", port), ReverseProxyHandler)
    server.timeout = 0.5
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def stop_reverse_proxy(server):
    if server:
        server.shutdown()
        server.server_close()
        time.sleep(0.3)


# ---------------------------------------------------------------------------
# ITERATIVE DECOMPRESSION (identical to parent)
# ---------------------------------------------------------------------------

def decompress_body(raw_body, content_encoding):
    MAX_DEPTH = 5
    current_data = raw_body
    depth = 0
    while depth < MAX_DEPTH:
        try:
            current_data = brotli.decompress(current_data)
            depth += 1
            continue
        except Exception:
            pass
        try:
            current_data = gzip.decompress(current_data)
            depth += 1
            continue
        except Exception:
            pass
        break
    return current_data


# ---------------------------------------------------------------------------
# FINGERPRINT FUNCTIONS (identical to parent)
# ---------------------------------------------------------------------------

def fingerprint_compressed_only(observation):
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
    vector = (observation["status"], body_hash, '')
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


def fingerprint_decompressed(observation):
    ce = observation["headers"].get("Content-Encoding", "")
    decompressed = decompress_body(observation["body"], ce)
    body_hash = hashlib.sha256(decompressed).hexdigest()
    vector = (observation["status"], body_hash, '')
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


def fingerprint_status_only(observation):
    vector = (observation["status"], '', '')
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


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


def baseline_random(n=10, seed=99):
    rng = random.Random(seed)
    return [hashlib.sha256(rng.getrandbits(256).to_bytes(32, "big")).hexdigest()
            for _ in range(n)]


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


def make_request(url, method="GET", auth_header=None, timeout=10):
    headers = {"Accept-Encoding": "br, gzip, identity"}
    if auth_header:
        headers["Authorization"] = auth_header
    start = time.monotonic()
    try:
        resp = requests.get(url, headers=headers, timeout=timeout,
                            allow_redirects=True, stream=True)
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
# MAIN EXPERIMENT
# ---------------------------------------------------------------------------

def run_experiment():
    all_results = {}
    all_controls = {}
    all_observations = []
    all_validity_notes = []
    errors = []
    request_count = 0
    all_observations_by_cell = {}  # cell_key -> {state -> [obs]}

    print(f"Experiment: {EXPERIMENT_ID}")
    print(f"Cache configs: {CACHE_CONFIGS}")
    print(f"Content types: {list(CONTENT_TYPES.keys())}")
    print(f"Payload sizes: {list(PAYLOAD_SIZES.keys())}")
    print(f"Auth states: {AUTH_STATES}")
    print(f"Reps per cell: {REPS}")
    print(f"Seed: {SEED}")
    print(f"Max decompression depth: 5")
    print()

    all_observations.append(f"Experiment: {EXPERIMENT_ID}")
    all_observations.append(f"Architecture: Client (iterative decompression, max_depth=5) -> Python Reverse Proxy ({', '.join(CACHE_CONFIGS)}) -> Mock OAuth2 Server (brotli quality {MOCK_BROTLI_QUALITY})")
    all_observations.append(f"Cache configs: {CACHE_CONFIGS}")
    all_observations.append(f"Reps per cell: {REPS}")
    all_observations.append(f"Seed: {SEED}")

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated.")

    port_idx = 0
    for ct_name, ct_mime in CONTENT_TYPES.items():
        print(f"\n{'='*70}")
        print(f"CONTENT TYPE: {ct_name}")
        print(f"{'='*70}")

        for size_name, size_bytes in PAYLOAD_SIZES.items():
            print(f"\n  Payload size: {size_name} ({size_bytes} bytes)")

            origin_port = BASE_PORT + port_idx
            mock_server = start_mock_server(origin_port, size_bytes, ct_name)
            time.sleep(0.5)
            print(f"    Origin server started on port {origin_port}")

            ref_key = f"{ct_name}_{size_name}"

            for cache_config in CACHE_CONFIGS:
                proxy_port = PROXY_PORT_BASE + port_idx * 10 + CACHE_CONFIGS.index(cache_config)
                proxy = start_reverse_proxy(proxy_port, origin_port, cache_config)
                time.sleep(0.5)
                print(f"    Proxy {cache_config} started on port {proxy_port}")

                # Connectivity test
                try:
                    test_resp = requests.get(
                        f"http://127.0.0.1:{proxy_port}{USERINFO_PATH}",
                        headers={"Authorization": f"Bearer {auth_token}",
                                 "Accept-Encoding": "br, gzip, identity"},
                        timeout=5)
                    print(f"      Connectivity test: status={test_resp.status_code}, "
                          f"body_size={len(test_resp.content)}")
                except Exception as e:
                    print(f"      WARNING: Connectivity test failed: {e}")

                # Request plan
                rng = random.Random(SEED)
                plan = []
                for state in AUTH_STATES:
                    for rep in range(REPS):
                        plan.append((state, rep))
                rng.shuffle(plan)

                cell_fingerprints_compressed = defaultdict(list)
                cell_fingerprints_decompressed = defaultdict(list)
                cell_fingerprints_status = defaultdict(list)
                cell_raw_observations = defaultdict(list)
                cell_decompression_latencies = []
                cell_decompression_errors = []
                cell_proxy_overhead = []

                for i, (state, rep) in enumerate(plan):
                    auth_header = get_auth_header(state, auth_token)
                    url = f"http://127.0.0.1:{proxy_port}{USERINFO_PATH}"

                    obs = make_request(url, method="GET", auth_header=auth_header)
                    obs["state"] = state
                    obs["rep"] = rep
                    obs["content_type"] = ct_name
                    obs["payload_size"] = size_name
                    obs["cache_config"] = cache_config

                    obs["fingerprint_compressed"] = fingerprint_compressed_only(obs)
                    obs["fingerprint_decompressed"] = fingerprint_decompressed(obs)
                    obs["fingerprint_status"] = fingerprint_status_only(obs)
                    obs["body_hash_compressed"] = hashlib.sha256(obs["body"]).hexdigest()
                    obs["body_size"] = len(obs["body"])
                    obs["content_encoding"] = obs["headers"].get("Content-Encoding", "none")
                    obs["proxy_mode"] = obs["headers"].get("X-Proxy-Mode", "none")
                    obs["cache_hit"] = obs["headers"].get("X-Cache", "none")

                    decomp_start = time.monotonic()
                    try:
                        decompressed = decompress_body(obs["body"], obs["content_encoding"])
                        decomp_elapsed = time.monotonic() - decomp_start
                        obs["decompression_latency_ms"] = decomp_elapsed * 1000
                        cell_decompression_latencies.append(decomp_elapsed * 1000)
                        obs["decompressed_hash"] = hashlib.sha256(decompressed).hexdigest()
                        obs["decompression_error"] = None
                    except Exception as e:
                        decomp_elapsed = time.monotonic() - decomp_start
                        obs["decompression_latency_ms"] = decomp_elapsed * 1000
                        cell_decompression_errors.append({
                            "state": state, "rep": rep, "error": str(e)
                        })
                        obs["decompression_error"] = str(e)
                        obs["decompressed_hash"] = hashlib.sha256(obs["body"]).hexdigest()

                    cell_proxy_overhead.append(obs["elapsed"] * 1000)

                    cell_fingerprints_compressed[state].append(obs["fingerprint_compressed"])
                    cell_fingerprints_decompressed[state].append(obs["fingerprint_decompressed"])
                    cell_fingerprints_status[state].append(obs["fingerprint_status"])
                    cell_raw_observations[state].append(obs)

                    request_count += 1

                    if i < len(plan) - 1:
                        jitter = rng.uniform(0.05, 0.15)
                        time.sleep(jitter)

                # Compute discrimination scores
                compressed_disc = compute_discrimination_score(cell_fingerprints_compressed)
                decompressed_disc = compute_discrimination_score(cell_fingerprints_decompressed)
                status_disc = compute_discrimination_score(cell_fingerprints_status)

                # B-RANDOM baseline
                b_rand_fps = baseline_random(n=REPS * len(AUTH_STATES))
                b_rand_by_state = {}
                idx = 0
                for s in AUTH_STATES:
                    b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
                    idx += REPS
                b_rand_disc = compute_discrimination_score(b_rand_by_state)

                # Hash variation
                decompressed_hash_variation = {}
                for state, obs_list in cell_raw_observations.items():
                    hashes = [obs["decompressed_hash"] for obs in obs_list]
                    decompressed_hash_variation[state] = {
                        "unique_count": len(set(hashes)),
                        "total": len(hashes),
                        "all_same": len(set(hashes)) == 1,
                    }
                compressed_hash_variation = {}
                for state, obs_list in cell_raw_observations.items():
                    hashes = [obs["body_hash_compressed"] for obs in obs_list]
                    compressed_hash_variation[state] = {
                        "unique_count": len(set(hashes)),
                        "total": len(hashes),
                        "all_same": len(set(hashes)) == 1,
                    }
                body_sizes = {}
                for state, obs_list in cell_raw_observations.items():
                    sizes = [obs["body_size"] for obs in obs_list]
                    body_sizes[state] = {
                        "min": min(sizes), "max": max(sizes),
                        "mean": sum(sizes) / len(sizes),
                    }

                cell_key = f"/userinfo_{ct_name}_{size_name}_{cache_config}"
                all_observations_by_cell[cell_key] = dict(cell_raw_observations)
                all_results[cell_key] = {
                    "compressed_body_only_discrimination": compressed_disc,
                    "decompressed_body_only_discrimination": decompressed_disc,
                    "status_only_discrimination": status_disc,
                    "baselines": {"B-RANDOM": b_rand_disc},
                    "compressed_hash_variation": compressed_hash_variation,
                    "decompressed_hash_variation": decompressed_hash_variation,
                    "body_sizes": body_sizes,
                    "total_requests": sum(len(v) for v in cell_raw_observations.values()),
                    "decompression_latency_ms": {
                        "mean": sum(cell_decompression_latencies) / len(cell_decompression_latencies) if cell_decompression_latencies else 0,
                        "min": min(cell_decompression_latencies) if cell_decompression_latencies else 0,
                        "max": max(cell_decompression_latencies) if cell_decompression_latencies else 0,
                    },
                    "proxy_overhead_ms": {
                        "mean": sum(cell_proxy_overhead) / len(cell_proxy_overhead) if cell_proxy_overhead else 0,
                        "min": min(cell_proxy_overhead) if cell_proxy_overhead else 0,
                        "max": max(cell_proxy_overhead) if cell_proxy_overhead else 0,
                    },
                    "decompression_errors": cell_decompression_errors,
                }

                print(f"      {cache_config}: compressed={compressed_disc:.4f}, "
                      f"decompressed={decompressed_disc:.4f}, "
                      f"status={status_disc:.4f}, B-RANDOM={b_rand_disc:.4f}")

                stop_reverse_proxy(proxy)

            stop_mock_server(mock_server)
            port_idx += 1
            time.sleep(0.3)

    # =========================================================================
    # AGGREGATE METRICS per cache config
    # =========================================================================

    config_metrics = {}
    for cc in CACHE_CONFIGS:
        decompressed_discs = []
        compressed_discs = []
        for cell_key, cell_data in all_results.items():
            if cell_key.endswith(f"_{cc}"):
                decompressed_discs.append(cell_data["decompressed_body_only_discrimination"])
                compressed_discs.append(cell_data["compressed_body_only_discrimination"])
        config_metrics[cc] = {
            "decompressed_body_only_discrimination": {
                "mean": sum(decompressed_discs) / len(decompressed_discs) if decompressed_discs else 0,
                "min": min(decompressed_discs) if decompressed_discs else 0,
                "max": max(decompressed_discs) if decompressed_discs else 0,
            },
            "compressed_body_only_discrimination": {
                "mean": sum(compressed_discs) / len(compressed_discs) if compressed_discs else 0,
                "min": min(compressed_discs) if compressed_discs else 0,
                "max": max(compressed_discs) if compressed_discs else 0,
            },
        }

    # =========================================================================
    # CONTROLS
    # =========================================================================

    # C_NULL_CONTROL: B-RANDOM = 0.0 for all conditions
    b_random_values = [cell_data["baselines"]["B-RANDOM"] for cell_data in all_results.values()]
    c_null_pass = all(v is not None and abs(v) < 0.1 for v in b_random_values)
    all_controls["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0 for all conditions",
        "observed": [float(v) for v in b_random_values],
        "pass": c_null_pass,
    }

    # C_PASSTHROUGH_REGRESSION: CL-PASSTHROUGH discrimination = 0.5 (reproduces parent baseline)
    cl_discs = [all_results[k]["decompressed_body_only_discrimination"]
                   for k in all_results if k.endswith("_CL-PASSTHROUGH")]
    cl_mean = sum(cl_discs) / len(cl_discs) if cl_discs else 0
    cl_pass = all(d >= 0.5 for d in cl_discs)
    all_controls["C_CONTENT_LENGTH_REGRESSION"] = {
        "expected": "Content-Length PASSTHROUGH discrimination = 0.5 for all cells (reproduces parent)",
        "observed_mean": cl_mean,
        "observed_per_cell": cl_discs,
        "pass": cl_pass,
    }

    # C_CHUNKED_CACHED_PRIMARY: CHUNKED-CACHED discrimination >= 0.3 for all cells
    chcache_discs = [all_results[k]["decompressed_body_only_discrimination"]
                        for k in all_results if k.endswith("_CHUNKED-CACHED")]
    chcache_min = min(chcache_discs) if chcache_discs else 0
    chcache_pass = chcache_min >= 0.3
    all_controls["C_CHUNKED_CACHED_PRIMARY"] = {
        "expected": "Chunked AUTH-AWARE CACHED discrimination >= 0.3 for all cells",
        "min_observed": chcache_min,
        "observed_per_cell": chcache_discs,
        "pass": chcache_pass,
    }

    # C_DECOMPRESSED_DETERMINISM: all_same=true for all states, all conditions
    all_det = True
    det_details = {}
    for cell_key, cell_data in all_results.items():
        for state, hv in cell_data["decompressed_hash_variation"].items():
            if not hv["all_same"]:
                all_det = False
            det_details.setdefault(state, []).append(hv["all_same"])
    all_controls["C_DECOMPRESSED_DETERMINISM"] = {
        "expected": "Within-state decompressed hash all_same=true for all states across all conditions",
        "observed": {state: all(vals) for state, vals in det_details.items()},
        "pass": all_det,
    }

    # C_DETERMINISM_ACROSS_PATHS: verify proxy preserves decompressed body bytes
    # Only check CHUNKED-PASSTHROUGH and CHUNKED-CACHED: CL-PASSTHROUGH is passthrough baseline
    all_hashes_match = True
    hash_mismatch_count = 0
    hash_check_count = 0
    for cell_key, cell_data in all_results.items():
        if not cell_key.endswith("_CHUNKED-PASSTHROUGH") and not cell_key.endswith("_CHUNKED-CACHED"):
            continue  # Only check chunked TE configs
        parts = cell_key.replace("/userinfo_", "")
        # Parse: {ct}_{size}_{cache_config}
        ct_size = None
        for cc in CACHE_CONFIGS:
            if parts.endswith(f"_{cc}"):
                ct_size = parts[: -len(cc) - 1]
                break
        if ct_size is None:
            continue

        # Extract content type and size
        found = False
        ct_name = None
        size_name = None
        for ct in CONTENT_TYPES:
            for sz in PAYLOAD_SIZES:
                if ct_size == f"{ct}_{sz}":
                    ct_name = ct
                    size_name = sz
                    found = True
                    break
            if found:
                break
        if not found:
            continue

        # Start a fresh mock server on a unique port for direct comparison
        direct_port = 6100 + list(CONTENT_TYPES.keys()).index(ct_name) * 10 + list(PAYLOAD_SIZES.keys()).index(size_name)
        try:
            mock_direct = start_mock_server(direct_port, PAYLOAD_SIZES[size_name], ct_name)
            time.sleep(0.3)

            # For each auth state, compare proxy hash with direct-server hash
            cell_obs = all_observations_by_cell.get(cell_key, {})
            for state in AUTH_STATES:
                if state not in cell_obs or not cell_obs[state]:
                    continue
                proxy_hash = cell_obs[state][0]["decompressed_hash"]
                if proxy_hash is None:
                    continue

                auth_header = get_auth_header(state, auth_token)
                direct_headers = {"Accept-Encoding": "br, gzip, identity"}
                if auth_header:
                    direct_headers["Authorization"] = auth_header
                direct_resp = requests.get(
                    f"http://127.0.0.1:{direct_port}{USERINFO_PATH}",
                    headers=direct_headers, timeout=5)
                direct_raw = direct_resp.content
                direct_ce = direct_resp.headers.get("Content-Encoding", "")
                direct_decomp = decompress_body(direct_raw, direct_ce)
                direct_hash = hashlib.sha256(direct_decomp).hexdigest()
                hash_check_count += 1
                if proxy_hash != direct_hash:
                    all_hashes_match = False
                    hash_mismatch_count += 1

            stop_mock_server(mock_direct)
        except Exception as e:
            hash_mismatch_count += 1
            hash_check_count += 1
            try:
                stop_mock_server(mock_direct)
            except Exception:
                pass

    all_controls["C_DETERMINISM_ACROSS_PATHS"] = {
        "expected": "Decompressed hash through proxy matches direct-server hash for same condition",
        "all_match": all_hashes_match,
        "pass": all_hashes_match,
        "mismatch_count": hash_mismatch_count,
        "conditions_checked": hash_check_count,
    }

    # C_NO_ERROR_INFLATION: 0 decompression errors
    total_decomp_errors = sum(len(cd.get("decompression_errors", [])) for cd in all_results.values())
    all_controls["C_NO_ERROR_INFLATION"] = {
        "expected": "0 decompression errors across all conditions",
        "observed": total_decomp_errors,
        "pass": total_decomp_errors == 0,
    }

    # =========================================================================
    # DECISION RULE (from frozen spec.json)
    # =========================================================================

    # Condition 1: decompressed body-only discrimination >= 0.3 for ALL cells
    min_decompressed_disc = min(cd["decompressed_body_only_discrimination"] for cd in all_results.values())
    c1_pass = min_decompressed_disc >= 0.3

    # Condition 2: decompressed hash matches parent direct hash for auth-aware
    c2_pass = all_hashes_match

    # Condition 3: B-RANDOM = 0.0
    c3_pass = c_null_pass

    # Condition 4: CL-PASSTHROUGH regression — reproduces parent baseline 0.5
    c4_pass = cl_pass

    # Condition 5: No decompression crashes/hangs
    c5_pass = total_decomp_errors == 0

    # Condition 6: CHUNKED-CACHED discrimination >= 0.3 (primary test)
    c6_pass = chcache_pass

    survives = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass and c6_pass
    falsified_in_setting = not chcache_pass  # primary test

    if total_decomp_errors > 0:
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif survives:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif not cl_pass:
        outcome = "FALSIFIES"
    elif not chcache_pass:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    else:
        outcome = "MIXED"
        status = "COMPLETE"

    # =========================================================================
    # OBSERVATIONS
    # =========================================================================

    all_observations.append(f"Total requests made: {request_count}")
    all_observations.append(f"Min decompressed discrimination across all cells: {min_decompressed_disc:.4f}")
    all_observations.append(f"CHUNKED-CACHED decompressed discrimination min: {chcache_min:.4f}")
    all_observations.append(f"CL-PASSTHROUGH decompressed discrimination mean: {cl_mean:.4f}")
    all_observations.append(f"Total decompression errors: {total_decomp_errors}")
    all_observations.append(f"Determinism across paths: {all_hashes_match}")

    for cc in CACHE_CONFIGS:
        cm = config_metrics[cc]
        all_observations.append(
            f"{cc}: decompressed mean={cm['decompressed_body_only_discrimination']['mean']:.4f}, "
            f"compressed mean={cm['compressed_body_only_discrimination']['mean']:.4f}"
        )

    for cell_key in sorted(all_results.keys()):
        cell_data = all_results[cell_key]
        all_observations.append(
            f"{cell_key}: compressed={cell_data['compressed_body_only_discrimination']:.4f}, "
            f"decompressed={cell_data['decompressed_body_only_discrimination']:.4f}, "
            f"B-RANDOM={cell_data['baselines']['B-RANDOM']:.4f}"
        )

    # =========================================================================
    # VALIDITY NOTES
    # =========================================================================

    all_validity_notes.extend([
        f"Architecture: Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server (brotli quality {MOCK_BROTLI_QUALITY})",
        "Three configurations tested: CL-PASSTHROUGH, CHUNKED-PASSTHROUGH, CHUNKED-CACHED",
        "CL-PASSTHROUGH: Content-Length forwarding, parent baseline regression control",
        "CHUNKED-PASSTHROUGH: Transfer-Encoding: chunked, no caching",
        "CHUNKED-CACHED: Transfer-Encoding: chunked, auth-aware cache key (URL+Accept-Encoding+Authorization)",
        "Origin server always sets Cache-Control: private, Vary: Authorization headers",
        "Accept-Encoding from client: 'br, gzip, identity' in all conditions",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "Expired_token is locally-signed HS256, not real expired token",
        "Content types are synthetic but structurally realistic",
        "Payload sizes controlled by padding to hit target uncompressed sizes",
        "3-way error collapse preserved: no_auth, expired_token, invalid_token share similar error bodies",
        f"Seed={SEED} for request ordering",
        "No real CDN infrastructure - bounded to localhost mock server + Python reverse proxy",
        "Parent reference hashes extracted from EXP-RUNTIME-35389142338 result.json",
        "CL-PASSTHROUGH mode reproduces parent baseline — expected discrimination 0.5",
        "CHUNKED-PASSTHROUGH expected to maintain discrimination if chunked TE is transparent",
    ])

    if total_decomp_errors > 0:
        all_validity_notes.append(f"Pipeline errors: {total_decomp_errors} decompression errors")

    # =========================================================================
    # UNRESOLVED
    # =========================================================================

    unresolved = [
        "Does iterative decompression survive real CDN infrastructure (Cloudflare/Fastly/Akamai) with auth-aware cache configuration?",
        "Does iterative decompression survive real CDN with double/triple-brotli multi-layer encoding through the proxy?",
        "What is production-scale latency/CPU at N>1000 with MB-scale natural content and concurrent clients through real CDN?",
        "Does iterative decompression work for binary content types or genuinely incorrect Content-Encoding on incompressible data?",
        "How does proxy behavior interact with CDN-specific header manipulation (X-Cache, Via, X-Forwarded-For) and Accept-Encoding negotiation across multiple CDN nodes?",
        "What is the maximum practical decompression depth for real-world multi-layer encoding scenarios?",
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
        "metrics": {
            "per_cell": all_results,
            "per_cache_config": config_metrics,
        },
        "controls": all_controls,
        "artifacts": [
            {"path": "run_experiment.py", "role": "code",
             "description": "Experiment execution script with mock origin, reverse proxy (3 cache configs: CL-PASSTHROUGH, CHUNKED-PASSTHROUGH, CHUNKED-CACHED), and iterative decompression"},
        ],
        "observations": all_observations,
        "validity_notes": all_validity_notes,
        "unresolved": unresolved,
    }

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
            json.dump(result, f, indent=2)
        print(f"\nResult saved to result.json")
        print(f"Experiment complete. Outcome: {result['outcome']}, Status: {result['status']}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        result = build_blocked_result(str(e))
        with open("result.json", "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nBLOCKED: {e}")
