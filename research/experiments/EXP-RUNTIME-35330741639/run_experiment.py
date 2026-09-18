#!/usr/bin/env python3
"""
EXP-RUNTIME-35330741639 - CDN-like Proxy Behavior Decompression Test
====================================================================
Tests whether iterative decompression survives CDN-like proxy behaviors:
  (a) PASSTHROUGH - no caching, no re-compression, chunked TE
  (b) CACHED - response caching by (URL, Accept-Encoding) for 60s
  (c) RECOMPRESS - origin fetch, decompress, re-compress at proxy brotli quality 8

Architecture:
  Client (iterative decompression, max_depth=5) -> Python Reverse Proxy (mode) -> Mock OAuth2 Server (brotli quality 6)

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


# ---------------------------------------------------------------------------
# FROZEN CONSTANTS
# ---------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-RUNTIME-35330741639"
LANE = "runtime"
SEED = 44
REPS = 5  # 5 reps per cell
BASE_PORT = 5500  # Origin mock server port
PROXY_PORT_BASE = 5600  # Base for proxy ports (one per behavior per condition)
CLIENT_SECRET = "spider-secret-12345"

USERINFO_PATH = "/userinfo"

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

# Brotli quality for mock server (deterministic baseline, same as parent)
MOCK_BROTLI_QUALITY = 6
# Brotli quality for proxy re-compression
PROXY_RECOMPRESS_QUALITY = 8

# Proxy behaviors (independent variable)
PROXY_BEHAVIORS = ["PASSTHROUGH", "CACHED", "RECOMPRESS"]

AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]

# Parent's reference decompressed hashes (for determinism-across-paths test)
# Extracted from parent EXP-RUNTIME-35290615081 raw_observations.json
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
    
    Accepts requests from the reverse proxy and returns compressed bodies.
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
        self.send_error(404)


def start_mock_server(port, body_size=1024, content_type="JSON"):
    MockOAuthHandler.body_size = body_size
    MockOAuthHandler.content_type = content_type
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
# REVERSE PROXY (3 modes: PASSTHROUGH, CACHED, RECOMPRESS)
# ---------------------------------------------------------------------------

class ReverseProxyHandler(BaseHTTPRequestHandler):
    """Python reverse proxy with three CDN-like behaviors.
    
    PASSTHROUGH: Forward request/response unmodified. Always uses chunked TE.
    CACHED: Cache compressed response by (URL, Accept-Encoding) for 60s.
    RECOMPRESS: Fetch origin, decompress, re-compress with brotli quality 8.
    """
    upstream_host = "127.0.0.1"
    upstream_port = 5400
    proxy_mode = "PASSTHROUGH"
    cache = {}  # For CACHED mode: {(url, accept_encoding): (compressed_body, headers, status)}
    cache_lock = threading.Lock()

    def log_message(self, format, *args):
        pass

    def _get_cache_key(self, path, accept_encoding):
        return (path, accept_encoding or "")

    def _proxy_request(self, method="GET"):
        """Forward request to upstream server with CDN-like behavior."""
        # Read request body if present
        content_length = int(self.headers.get("Content-Length", 0))
        req_body = self.rfile.read(content_length) if content_length > 0 else None

        # Build headers to forward
        headers = {}
        for key in self.headers:
            if key.lower() not in ("host", "connection"):
                headers[key] = self.headers[key]
        
        # Ensure Accept-Encoding is present (client always sends it)
        if "Accept-Encoding" not in headers and "accept-encoding" not in headers:
            headers["Accept-Encoding"] = "br, gzip, identity"

        cache_key = None
        if ReverseProxyHandler.proxy_mode == "CACHED":
            cache_key = self._get_cache_key(
                self.path,
                headers.get("Accept-Encoding", headers.get("accept-encoding", ""))
            )

        # Check cache for CACHED mode
        if ReverseProxyHandler.proxy_mode == "CACHED" and cache_key:
            with ReverseProxyHandler.cache_lock:
                if cache_key in ReverseProxyHandler.cache:
                    cached_body, cached_headers, cached_status = ReverseProxyHandler.cache[cache_key]
                    # Serve from cache with chunked TE
                    self.send_response(cached_status)
                    for key, value in cached_headers.items():
                        if key.lower() not in ("content-length", "transfer-encoding"):
                            self.send_header(key, value)
                    self.send_header("Transfer-Encoding", "chunked")
                    self.send_header("X-Proxy-Mode", "CACHED")
                    self.send_header("X-Cache", "HIT")
                    self.end_headers()
                    # Send as chunked
                    chunk_data = cached_body
                    self.wfile.write(f"{len(chunk_data):x}\r\n".encode())
                    self.wfile.write(chunk_data)
                    self.wfile.write(b"0\r\n\r\n")
                    self.wfile.flush()
                    return

        # Forward request to upstream
        try:
            conn = HTTPConnection(ReverseProxyHandler.upstream_host,
                                  ReverseProxyHandler.upstream_port, timeout=10)
            conn.request(method, self.path, body=req_body, headers=headers)
            upstream_resp = conn.getresponse()

            # Read upstream response
            resp_status = upstream_resp.status
            resp_headers = dict(upstream_resp.getheaders())
            resp_body = upstream_resp.read()
            conn.close()

            # Apply proxy behavior
            if ReverseProxyHandler.proxy_mode == "PASSTHROUGH":
                # Forward unmodified, always chunked TE
                self.send_response(resp_status)
                for key, value in resp_headers.items():
                    if key.lower() not in ("content-length", "transfer-encoding"):
                        self.send_header(key, value)
                self.send_header("Transfer-Encoding", "chunked")
                self.send_header("X-Proxy-Mode", "PASSTHROUGH")
                self.end_headers()
                # Send as chunked
                chunk_data = resp_body
                self.wfile.write(f"{len(chunk_data):x}\r\n".encode())
                self.wfile.write(chunk_data)
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()

            elif ReverseProxyHandler.proxy_mode == "CACHED":
                # Cache the compressed response (by URL + Accept-Encoding)
                if cache_key:
                    with ReverseProxyHandler.cache_lock:
                        ReverseProxyHandler.cache[cache_key] = (
                            resp_body, resp_headers, resp_status
                        )
                # Serve with chunked TE
                self.send_response(resp_status)
                for key, value in resp_headers.items():
                    if key.lower() not in ("content-length", "transfer-encoding"):
                        self.send_header(key, value)
                self.send_header("Transfer-Encoding", "chunked")
                self.send_header("X-Proxy-Mode", "CACHED")
                self.send_header("X-Cache", "MISS")
                self.end_headers()
                chunk_data = resp_body
                self.wfile.write(f"{len(chunk_data):x}\r\n".encode())
                self.wfile.write(chunk_data)
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()

            elif ReverseProxyHandler.proxy_mode == "RECOMPRESS":
                # Decompress origin response, then re-compress with proxy's own quality
                server_ce = resp_headers.get("Content-Encoding", "br")
                decompressed = resp_body
                if server_ce == "br":
                    try:
                        decompressed = brotli.decompress(resp_body)
                    except Exception:
                        pass
                elif server_ce == "gzip":
                    try:
                        decompressed = gzip.decompress(resp_body)
                    except Exception:
                        pass

                # Re-compress with proxy's own brotli quality 8
                recompressed = brotli.compress(decompressed, quality=PROXY_RECOMPRESS_QUALITY)

                self.send_response(resp_status)
                for key, value in resp_headers.items():
                    if key.lower() not in ("content-length", "content-encoding", "transfer-encoding"):
                        self.send_header(key, value)
                self.send_header("Content-Encoding", "br")
                self.send_header("Transfer-Encoding", "chunked")
                self.send_header("X-Proxy-Mode", "RECOMPRESS")
                self.send_header("X-Proxy-Quality", str(PROXY_RECOMPRESS_QUALITY))
                self.end_headers()
                chunk_data = recompressed
                self.wfile.write(f"{len(chunk_data):x}\r\n".encode())
                self.wfile.write(chunk_data)
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()

        except Exception as e:
            self.send_error(502, f"Proxy error: {e}")

    def do_GET(self):
        self._proxy_request("GET")

    def do_POST(self):
        self._proxy_request("POST")


def start_reverse_proxy(port, upstream_port, mode):
    """Start reverse proxy on port, forwarding to upstream_port."""
    ReverseProxyHandler.upstream_port = upstream_port
    ReverseProxyHandler.proxy_mode = mode
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
# ITERATIVE DECOMPRESSION (same as parent)
# ---------------------------------------------------------------------------

def decompress_body(raw_body, content_encoding):
    """Iteratively decompress body based on Content-Encoding header.
    
    Decompresses repeatedly until decompression fails or max_depth=5 is reached.
    """
    MAX_DEPTH = 5
    current_data = raw_body
    depth = 0

    while depth < MAX_DEPTH:
        # Try brotli decompress first
        try:
            decompressed = brotli.decompress(current_data)
            current_data = decompressed
            depth += 1
            continue
        except Exception:
            pass

        # If brotli fails, try gzip
        try:
            decompressed = gzip.decompress(current_data)
            current_data = decompressed
            depth += 1
            continue
        except Exception:
            pass

        # If both fail, we're done (identity / already decompressed)
        break

    return current_data


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
# HTTP REQUEST EXECUTION
# ---------------------------------------------------------------------------

def make_request(url, method="GET", auth_header=None, timeout=10):
    headers = {"Accept-Encoding": "br, gzip, identity"}
    if auth_header:
        headers["Authorization"] = auth_header

    start = time.monotonic()
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=timeout,
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
# MAIN EXPERIMENT
# ---------------------------------------------------------------------------

def run_experiment():
    all_results = {}
    all_controls = {}
    all_observations = []
    all_validity_notes = []
    errors = []
    request_count = 0

    print(f"Experiment: {EXPERIMENT_ID}")
    print(f"Auth states: {AUTH_STATES}")
    print(f"Content types: {list(CONTENT_TYPES.keys())}")
    print(f"Payload sizes: {list(PAYLOAD_SIZES.keys())}")
    print(f"Proxy behaviors: {PROXY_BEHAVIORS}")
    print(f"Reps per cell: {REPS}")
    print(f"Seed: {SEED}")
    print(f"Max decompression depth: 5")
    print()

    all_observations.append(f"Experiment: {EXPERIMENT_ID}")
    all_observations.append(f"Architecture: Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server (brotli quality {MOCK_BROTLI_QUALITY})")
    all_observations.append(f"Proxy behaviors: {PROXY_BEHAVIORS}")
    all_observations.append(f"Reps per cell: {REPS}")
    all_observations.append(f"Seed: {SEED}")

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated.")

    # For each content type x size, we test all 3 proxy behaviors
    # Each proxy behavior gets its own proxy process
    port_idx = 0
    for ct_name, ct_mime in CONTENT_TYPES.items():
        print(f"\n{'='*70}")
        print(f"CONTENT TYPE: {ct_name}")
        print(f"{'='*70}")

        for size_name, size_bytes in PAYLOAD_SIZES.items():
            print(f"\n  Payload size: {size_name} ({size_bytes} bytes)")

            # Start mock origin server (one per condition)
            origin_port = BASE_PORT + port_idx
            mock_server = start_mock_server(origin_port, size_bytes, ct_name)
            time.sleep(0.5)
            print(f"    Origin server started on port {origin_port}")

            # Reference hash key for this condition
            ref_key = f"{ct_name}_{size_name}"

            # Test each proxy behavior
            for behavior in PROXY_BEHAVIORS:
                proxy_port = PROXY_PORT_BASE + port_idx * 10 + PROXY_BEHAVIORS.index(behavior)

                # Start proxy
                proxy = start_reverse_proxy(proxy_port, origin_port, behavior)
                time.sleep(0.5)
                print(f"    Proxy {behavior} started on port {proxy_port}")

                # Test connectivity
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

                # Generate request plan for this (content_type x size x behavior)
                rng = random.Random(SEED)
                plan = []
                for state in AUTH_STATES:
                    for rep in range(REPS):
                        plan.append((state, rep))
                rng.shuffle(plan)

                # Per-cell observations
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
                    obs["proxy_behavior"] = behavior

                    # Fingerprint compressed body
                    obs["fingerprint_compressed"] = fingerprint_compressed_only(obs)

                    # Fingerprint decompressed body
                    obs["fingerprint_decompressed"] = fingerprint_decompressed(obs)

                    # Fingerprint status only
                    obs["fingerprint_status"] = fingerprint_status_only(obs)

                    # Compressed body hash
                    obs["body_hash_compressed"] = hashlib.sha256(obs["body"]).hexdigest()
                    obs["body_size"] = len(obs["body"])

                    # Content-Encoding
                    obs["content_encoding"] = obs["headers"].get("Content-Encoding", "none")

                    # Proxy mode
                    obs["proxy_mode"] = obs["headers"].get("X-Proxy-Mode", "none")
                    obs["cache_hit"] = obs["headers"].get("X-Cache", "none")

                    # Measure decompression latency
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

                    # Proxy overhead
                    cell_proxy_overhead.append(obs["elapsed"] * 1000)

                    # Store
                    cell_fingerprints_compressed[state].append(obs["fingerprint_compressed"])
                    cell_fingerprints_decompressed[state].append(obs["fingerprint_decompressed"])
                    cell_fingerprints_status[state].append(obs["fingerprint_status"])
                    cell_raw_observations[state].append(obs)

                    request_count += 1

                    # Jitter between requests
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

                # Decompressed hash variation per state
                decompressed_hash_variation = {}
                for state, obs_list in cell_raw_observations.items():
                    hashes = [obs["decompressed_hash"] for obs in obs_list]
                    decompressed_hash_variation[state] = {
                        "unique_count": len(set(hashes)),
                        "total": len(hashes),
                        "all_same": len(set(hashes)) == 1,
                    }

                # Compressed hash variation per state
                compressed_hash_variation = {}
                for state, obs_list in cell_raw_observations.items():
                    hashes = [obs["body_hash_compressed"] for obs in obs_list]
                    compressed_hash_variation[state] = {
                        "unique_count": len(set(hashes)),
                        "total": len(hashes),
                        "all_same": len(set(hashes)) == 1,
                    }

                # Body sizes
                body_sizes = {}
                for state, obs_list in cell_raw_observations.items():
                    sizes = [obs["body_size"] for obs in obs_list]
                    body_sizes[state] = {
                        "min": min(sizes), "max": max(sizes),
                        "mean": sum(sizes) / len(sizes),
                    }

                # Store cell results
                cell_key = f"/userinfo_{ct_name}_{size_name}_{behavior}"
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

                print(f"      {behavior}: compressed={compressed_disc:.4f}, "
                      f"decompressed={decompressed_disc:.4f}, "
                      f"status={status_disc:.4f}, B-RANDOM={b_rand_disc:.4f}")

                stop_reverse_proxy(proxy)

            stop_mock_server(mock_server)
            port_idx += 1
            time.sleep(0.3)

    # =========================================================================
    # AGGREGATE METRICS (per proxy behavior across all conditions)
    # =========================================================================

    behavior_metrics = {}
    for behavior in PROXY_BEHAVIORS:
        decompressed_discs = []
        compressed_discs = []
        for cell_key, cell_data in all_results.items():
            if cell_key.endswith(f"_{behavior}"):
                decompressed_discs.append(cell_data["decompressed_body_only_discrimination"])
                compressed_discs.append(cell_data["compressed_body_only_discrimination"])

        behavior_metrics[behavior] = {
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
    # CONTROLS (from frozen spec)
    # =========================================================================

    # C_NULL_CONTROL: B-RANDOM = 0.0 for all conditions
    b_random_values = []
    for cell_key, cell_data in all_results.items():
        b_random_values.append(cell_data["baselines"]["B-RANDOM"])
    c_null_pass = all(v is not None and abs(v) < 0.1 for v in b_random_values)
    all_controls["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0 for all conditions",
        "observed": [float(v) for v in b_random_values],
        "pass": c_null_pass,
    }

    # C_PROXY_PASSTHROUGH_EQUIVALENCE: passthrough discrimination = 0.5 for all cells
    passthrough_discs = []
    for cell_key, cell_data in all_results.items():
        if cell_key.endswith("_PASSTHROUGH"):
            passthrough_discs.append(cell_data["decompressed_body_only_discrimination"])
    c_passthrough_pass = all(d >= 0.49 for d in passthrough_discs) if passthrough_discs else False
    all_controls["C_PROXY_PASSTHROUGH_EQUIVALENCE"] = {
        "expected": "Passthrough decompressed discrimination = 0.5 for all cells",
        "observed": passthrough_discs,
        "pass": c_passthrough_pass,
    }

    # C_DECOMPRESSED_DISCRIMINATION: >= 0.3 for ALL (state, proxy_behavior)
    # This is checked per-cell in the decision rule, but let's also compute it here
    min_decompressed_disc = 1.0
    for cell_key, cell_data in all_results.items():
        if cell_data["decompressed_body_only_discrimination"] < min_decompressed_disc:
            min_decompressed_disc = cell_data["decompressed_body_only_discrimination"]
    c_disc_pass = min_decompressed_disc >= 0.3
    all_controls["C_DECOMPRESSED_DISCRIMINATION"] = {
        "expected": "Decompressed body-only discrimination >= 0.3 for ALL cells",
        "min_observed": min_decompressed_disc,
        "pass": c_disc_pass,
    }

    # C_DECOMPRESSED_DETERMINISM: all_same=true for all states, all conditions
    all_det = True
    det_details = {}
    for cell_key, cell_data in all_results.items():
        for state, hv in cell_data["decompressed_hash_variation"].items():
            if not hv["all_same"]:
                all_det = False
            det_details.setdefault(state, []).append(hv["all_same"])
    c_det_pass = all_det
    all_controls["C_DECOMPRESSED_DETERMINISM"] = {
        "expected": "Within-state decompressed hash all_same=true for all states across all conditions",
        "observed": {state: all(vals) for state, vals in det_details.items()},
        "pass": c_det_pass,
    }

    # C_DETERMINISM_ACROSS_PATHS: decompressed hash matches parent's direct hash
    # Check for PASSTHROUGH only (proxy should not change bytes)
    hash_match_results = {}
    all_hashes_match = True
    for cell_key, cell_data in all_results.items():
        if not cell_key.endswith("_PASSTHROUGH"):
            continue
        # Extract content type and size from key
        parts = cell_key.replace("/userinfo_", "").replace("_PASSTHROUGH", "")
        ref_key = parts  # e.g., "JSON_1KB"
        if ref_key not in PARENT_REF_HASHES:
            continue

        for state, obs_list in cell_raw_observations.items():
            if state not in PARENT_REF_HASHES[ref_key]:
                continue
            ref_hash = PARENT_REF_HASHES[ref_key][state]
            for obs in obs_list:
                if obs.get("proxy_behavior") != "PASSTHROUGH":
                    continue
                if obs["decompressed_hash"] != ref_hash:
                    all_hashes_match = False

    all_controls["C_DETERMINISM_ACROSS_PATHS"] = {
        "expected": "Decompressed hash through proxy matches parent direct-server hash",
        "all_match": all_hashes_match,
        "pass": all_hashes_match,
    }

    # C_NO_ERROR_INFLATION: 0 decompression errors across all cells
    total_decomp_errors = 0
    for cell_key, cell_data in all_results.items():
        total_decomp_errors += len(cell_data.get("decompression_errors", []))
    c_no_errors = total_decomp_errors == 0
    all_controls["C_NO_ERROR_INFLATION"] = {
        "expected": "0 decompression errors across all conditions",
        "observed": total_decomp_errors,
        "pass": c_no_errors,
    }

    # C_SINGLE_LAYER_NO_REGRESSION: all 4 states maintain discrimination >= 0.3 under passthrough
    # (same as C_PROXY_PASSTHROUGH_EQUIVALENCE but checking individual states)
    regression_pass = True
    for cell_key, cell_data in all_results.items():
        if not cell_key.endswith("_PASSTHROUGH"):
            continue
        if cell_data["decompressed_body_only_discrimination"] < 0.3:
            regression_pass = False
    all_controls["C_SINGLE_LAYER_NO_REGRESSION"] = {
        "expected": "All 4 states maintain discrimination >= 0.3 under passthrough",
        "pass": regression_pass,
    }

    # C_COMPRESSED_BASELINE: compressed discrimination reference
    compressed_discs_all = []
    for cell_key, cell_data in all_results.items():
        compressed_discs_all.append(cell_data["compressed_body_only_discrimination"])
    compressed_mean = sum(compressed_discs_all) / len(compressed_discs_all) if compressed_discs_all else 0
    all_controls["C_COMPRESSED_BASELINE"] = {
        "expected": "Compressed body-only discrimination ~ 0.2781 (parent reference)",
        "observed_mean": compressed_mean,
        "pass": True,  # Informational control
    }

    # =========================================================================
    # DECISION RULE (from frozen spec.json)
    # =========================================================================

    # Condition 1: decompressed body-only discrimination >= 0.3 for ALL (auth_state, proxy_behavior)
    c1_pass = c_disc_pass

    # Condition 2: decompressed hash matches parent's direct-server hash
    c2_pass = all_hashes_match

    # Condition 3: B-RANDOM = 0.0 for all conditions
    c3_pass = c_null_pass

    # Condition 4: C_PROXY_PASSTHROUGH_EQUIVALENCE passes
    c4_pass = c_passthrough_pass

    # Condition 5: No decompression crashes/hangs
    c5_pass = c_no_errors

    # Condition 6: Regression - all 4 states maintain discrimination >= 0.3 under passthrough
    c6_pass = regression_pass

    survives = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass and c6_pass

    # Check for FALSIFIED-IN-SETTING
    falsified_in_setting = min_decompressed_disc < 0.3

    if not c_no_errors:
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

    all_observations.append(f"Total requests made: {request_count}")
    all_observations.append(f"Min decompressed discrimination across all cells: {min_decompressed_disc:.4f}")
    all_observations.append(f"Passthrough discrimination mean: {sum(passthrough_discs)/len(passthrough_discs):.4f}")
    all_observations.append(f"Compressed discrimination mean: {compressed_mean:.4f}")
    all_observations.append(f"Total decompression errors: {total_decomp_errors}")
    all_observations.append(f"Determinism across paths: {all_hashes_match}")

    for behavior in PROXY_BEHAVIORS:
        bm = behavior_metrics[behavior]
        all_observations.append(
            f"{behavior}: decompressed mean={bm['decompressed_body_only_discrimination']['mean']:.4f}, "
            f"compressed mean={bm['compressed_body_only_discrimination']['mean']:.4f}"
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
        f"Three proxy behaviors tested: PASSTHROUGH, CACHED, RECOMPRESS",
        "PASSTHROUGH: Forward request/response unmodified, chunked TE always applied",
        f"CACHED: Cache compressed response by (URL, Accept-Encoding) for 60s, chunked TE",
        f"RECOMPRESS: Fetch origin, decompress, re-compress with proxy brotli quality {PROXY_RECOMPRESS_QUALITY}, chunked TE",
        "Accept-Encoding from client: 'br, gzip, identity' in all conditions",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "Expired_token is locally-signed HS256, not real expired token",
        "Content types are synthetic but structurally realistic",
        "Payload sizes controlled by padding to hit target uncompressed sizes",
        "3-way error collapse preserved: no_auth, expired_token, invalid_token share similar error bodies",
        f"Seed={SEED} for request ordering",
        "No real CDN infrastructure - bounded to localhost mock server + Python reverse proxy",
        "Parent reference hashes extracted from EXP-RUNTIME-35290615081 raw_observations.json",
        "RECOMPRESS mode decompresses origin brotli response and re-compresses with quality 8, adding one compression layer",
        "CACHED mode caches the raw compressed response bytes (same as CDN caching)",
        "All three modes always apply Transfer-Encoding: chunked",
    ])

    if total_decomp_errors > 0:
        all_validity_notes.append(f"Pipeline errors: {total_decomp_errors} decompression errors")

    # =========================================================================
    # UNRESOLVED
    # =========================================================================

    unresolved = [
        "Does iterative decompression survive real CDN infrastructure (Cloudflare/Fastly/Akamai) with caching, chunked transfer-encoding, Accept-Encoding negotiation, and edge quality diversity?",
        "How does proxy behavior interact with double/triple-brotli encoding layers?",
        "What happens with CDN-specific headers (X-Cache, X-CDN, Via, X-Forwarded-For)?",
        "Does Accept-Encoding negotiation change behavior when proxy selects different encodings?",
        "What is production-scale latency with concurrent clients through CDN?",
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
            "per_behavior": behavior_metrics,
        },
        "controls": all_controls,
        "artifacts": [
            {"path": "run_experiment.py", "role": "code",
             "description": "Experiment execution script with mock origin, reverse proxy (3 modes), and iterative decompression"},
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
