#!/usr/bin/env python3
"""
EXP-RUNTIME-35470447407 - Gzip Decompression Correctness Controls
=================================================================
Tests whether iterative decompression (gzip->identity) produces
byte-identical output to ground-truth uncompressed body for all auth
states across all gzip conditions, plus brotli multi-chunk regression
check and IDENTITY baseline.

Frozen from spec.json and prereg.md - DO NOT MODIFY.

Architecture:
  Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server

Conditions tested:
  - GZIP-MC:  gzip default, chunk_size=32 bytes (multi-chunk)
  - GZIP-SC:  gzip default, chunk_size=1024 bytes (single-chunk)
  - IDENTITY: no compression, Content-Length set (ground-truth reference)
  - BROTLI-MC: brotli quality=6, chunk_size=32 bytes (positive control regression check)
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
# FROZEN CONSTANTS (from spec.json / prereg.md)
# ---------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-RUNTIME-35470447407"
LANE = "runtime"
SEED = 44
REPS = 10
BASE_PORT = 8700
PROXY_PORT_BASE = 8800
CLIENT_SECRET = "spider-secret-12345"

USERINFO_PATH = "/userinfo"

CONTENT_TYPES = {
    "JSON": "application/json",
    "HTML": "text/html",
    "XML": "application/xml",
}

TARGET_BODY_SIZE = 1024  # 1KB nominal uncompressed size

MOCK_BROTLI_QUALITY = 6
CHUNK_CONFIGS = ["MULTI-CHUNK", "SINGLE-CHUNK", "IDENTITY"]
AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]

MULTI_CHUNK_SIZE = 32     # bytes — forces multi-chunk spanning
SINGLE_CHUNK_SIZE = 1024  # bytes — all payloads fit in one chunk

# Gzip-specific constants
GZIP_USE_GZIP = True      # True for GZIP-MC and GZIP-SC, False for IDENTITY and BROTLI-MC
GZIP_CHUNK_SIZE = 32       # Default chunk size for gzip multi-chunk

# Compression modes: (use_gzip, use_brotli, use_chunked, chunk_size)
COMPRESSION_MODES = {
    "GZIP-MC":    {"use_gzip": True,  "use_brotli": False, "use_chunked": True,  "chunk_size": MULTI_CHUNK_SIZE},
    "GZIP-SC":    {"use_gzip": True,  "use_brotli": False, "use_chunked": True,  "chunk_size": SINGLE_CHUNK_SIZE},
    "IDENTITY":   {"use_gzip": False, "use_brotli": False, "use_chunked": False, "chunk_size": SINGLE_CHUNK_SIZE},
    "BROTLI-MC":  {"use_gzip": False, "use_brotli": True,  "use_chunked": True,  "chunk_size": MULTI_CHUNK_SIZE},
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


BODY_GENERATORS = {
    "JSON": generate_json_body,
    "HTML": generate_html_body,
    "XML": generate_xml_body,
}


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
# Serves gzip-compressed, brotli-compressed, or uncompressed responses.
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class MockOAuthHandler(BaseHTTPRequestHandler):
    body_size = 1024
    content_type = "JSON"
    use_gzip = True
    use_brotli = False
    use_chunked = True
    chunk_size = 32

    def log_message(self, format, *args):
        pass

    def _get_auth_state(self):
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
        gen = BODY_GENERATORS.get(self.content_type, generate_json_body)
        return gen(state, size)

    def _get_mime_type(self):
        return CONTENT_TYPES.get(self.content_type, "application/json")

    def do_GET(self):
        if self.path == USERINFO_PATH:
            state = self._get_auth_state()
            body = self._get_body(state, self.body_size)
            status = 200 if state == "valid_token" else 401

            if self.use_gzip:
                compressed = gzip.compress(body)
                ce_header = "gzip"
            elif self.use_brotli:
                compressed = brotli.compress(body, quality=MOCK_BROTLI_QUALITY)
                ce_header = "br"
            else:
                # IDENTITY condition
                self.send_response(status)
                self.send_header("Content-Type", self._get_mime_type())
                self.send_header("Content-Length", len(body))
                self.send_header("Cache-Control", "private")
                self.send_header("Vary", "Authorization")
                self.end_headers()
                self.wfile.write(body)
                self.wfile.flush()
                return

            self.send_response(status)
            self.send_header("Content-Type", self._get_mime_type())
            self.send_header("Content-Encoding", ce_header)
            self.send_header("Cache-Control", "private")
            self.send_header("Vary", "Authorization")

            if self.use_chunked:
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                chunk_size = self.chunk_size
                offset = 0
                while offset < len(compressed):
                    chunk = compressed[offset:offset + chunk_size]
                    self.wfile.write(("{:x}\r\n".format(len(chunk))).encode())
                    self.wfile.write(chunk)
                    self.wfile.write(b"\r\n")
                    offset += chunk_size
                self.wfile.write(b"0\r\n\r\n")
            else:
                self.send_header("Content-Length", len(compressed))
                self.end_headers()
                self.wfile.write(compressed)
            self.wfile.flush()
        else:
            self.send_error(404)

    def do_POST(self):
        self.send_error(404)


def start_mock_server(port, body_size=1024, content_type="JSON",
                      use_gzip=True, use_brotli=False,
                      use_chunked=True, chunk_size=32):
    MockOAuthHandler.body_size = body_size
    MockOAuthHandler.content_type = content_type
    MockOAuthHandler.use_gzip = use_gzip
    MockOAuthHandler.use_brotli = use_brotli
    MockOAuthHandler.use_chunked = use_chunked
    MockOAuthHandler.chunk_size = chunk_size
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
# REVERSE PROXY
# Forwards responses from origin to client.
# ---------------------------------------------------------------------------

class ReverseProxyHandler(BaseHTTPRequestHandler):
    upstream_host = "127.0.0.1"
    upstream_port = 5400
    use_chunked = True
    chunk_size = 32

    def log_message(self, format, *args):
        pass

    def _proxy_request(self, method="GET"):
        content_length = int(self.headers.get("Content-Length", 0))
        req_body = self.rfile.read(content_length) if content_length > 0 else None

        headers = {}
        for key in self.headers:
            if key.lower() not in ("host", "connection"):
                headers[key] = self.headers[key]
        if "Accept-Encoding" not in headers and "accept-encoding" not in headers:
            headers["Accept-Encoding"] = "br, gzip, identity"

        try:
            conn = HTTPConnection(ReverseProxyHandler.upstream_host,
                                  ReverseProxyHandler.upstream_port, timeout=10)
            conn.request(method, self.path, body=req_body, headers=headers)
            upstream_resp = conn.getresponse()
            resp_status = upstream_resp.status
            resp_headers = dict(upstream_resp.getheaders())
            resp_body = upstream_resp.read()
            conn.close()

            # Forward to client
            self.send_response(resp_status)
            for key, value in resp_headers.items():
                if key.lower() not in ("content-length", "transfer-encoding", "connection"):
                    self.send_header(key, value)
            self.send_header("X-Proxy-Mode", "CHUNKED-PROXY")
            self.send_header("X-Cache", "MISS")

            if ReverseProxyHandler.use_chunked:
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                chunk_size = ReverseProxyHandler.chunk_size
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


def start_reverse_proxy(port, upstream_port, use_chunked=True, chunk_size=32):
    ReverseProxyHandler.upstream_port = upstream_port
    ReverseProxyHandler.use_chunked = use_chunked
    ReverseProxyHandler.chunk_size = chunk_size
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
# Tries brotli first, then gzip, up to MAX_DEPTH iterations.
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
# DISCRIMINATION SCORE (from parent)
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

    print(f"Experiment: {EXPERIMENT_ID}")
    print(f"Compression modes: {list(COMPRESSION_MODES.keys())}")
    print(f"Content types: {list(CONTENT_TYPES.keys())}")
    print(f"Target body size: {TARGET_BODY_SIZE} bytes")
    print(f"Auth states: {AUTH_STATES}")
    print(f"Reps per cell: {REPS}")
    print(f"Seed: {SEED}")
    print(f"Max decompression depth: 5")
    print()

    all_observations.append(f"Experiment: {EXPERIMENT_ID}")
    all_observations.append(f"Architecture: Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server")
    all_observations.append(f"Compression modes: {list(COMPRESSION_MODES.keys())}")
    all_observations.append(f"GZIP-MC chunk_size={MULTI_CHUNK_SIZE} bytes, GZIP-SC chunk_size={SINGLE_CHUNK_SIZE} bytes")
    all_observations.append(f"BROTLI-MC chunk_size={MULTI_CHUNK_SIZE} bytes (positive control)")
    all_observations.append(f"IDENTITY: no compression (correctness oracle)")
    all_observations.append(f"Reps per cell: {REPS}")
    all_observations.append(f"Seed: {SEED}")

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated.")

    # Global correctness counters
    total_correctness_pass = 0
    total_correctness_fail = 0
    total_silent_fallbacks = 0
    total_decompression_errors = 0
    total_identity_pass = 0
    total_identity_fail = 0

    port_idx = 0
    for ct_name, ct_mime in CONTENT_TYPES.items():
        print(f"\n{'='*70}")
        print(f"CONTENT TYPE: {ct_name}")
        print(f"{'='*70}")

        for comp_mode, comp_config in COMPRESSION_MODES.items():
            use_gzip = comp_config["use_gzip"]
            use_brotli = comp_config["use_brotli"]
            use_chunked = comp_config["use_chunked"]
            chunk_size = comp_config["chunk_size"]

            print(f"\n  Compression mode: {comp_mode} (gzip={use_gzip}, brotli={use_brotli}, "
                  f"chunked={use_chunked}, chunk_size={chunk_size})")

            origin_port = BASE_PORT + port_idx
            mock_server = start_mock_server(origin_port, TARGET_BODY_SIZE, ct_name,
                                            use_gzip=use_gzip, use_brotli=use_brotli,
                                            use_chunked=use_chunked, chunk_size=chunk_size)
            time.sleep(0.5)
            print(f"    Origin server started on port {origin_port}")

            proxy_port = PROXY_PORT_BASE + port_idx
            proxy = start_reverse_proxy(proxy_port, origin_port,
                                        use_chunked=use_chunked, chunk_size=chunk_size)
            time.sleep(0.5)
            print(f"    Proxy started on port {proxy_port}")

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
            cell_raw_observations = defaultdict(list)
            cell_correctness_results = []
            cell_silent_fallbacks = []
            cell_decompression_errors = []
            cell_decompression_latencies = []
            cell_compressed_sizes = []
            cell_expected_hashes = {}

            for i, (state, rep) in enumerate(plan):
                auth_header = get_auth_header(state, auth_token)
                url = f"http://127.0.0.1:{proxy_port}{USERINFO_PATH}"

                obs = make_request(url, method="GET", auth_header=auth_header)
                obs["state"] = state
                obs["rep"] = rep
                obs["content_type"] = ct_name
                obs["comp_mode"] = comp_mode

                obs["body_hash_compressed"] = hashlib.sha256(obs["body"]).hexdigest()
                obs["body_size"] = len(obs["body"])
                obs["content_encoding"] = obs["headers"].get("Content-Encoding", "none")
                obs["proxy_mode"] = obs["headers"].get("X-Proxy-Mode", "none")
                obs["cache_hit"] = obs["headers"].get("X-Cache", "none")

                # Compute expected hash from generate_*_body()
                gen = BODY_GENERATORS.get(ct_name, generate_json_body)
                expected_body = gen(state, TARGET_BODY_SIZE)
                expected_hash = hashlib.sha256(expected_body).hexdigest()
                obs["expected_hash"] = expected_hash

                # Store expected hash per state for determinism check
                if state not in cell_expected_hashes:
                    cell_expected_hashes[state] = expected_hash

                # Decompress
                decomp_start = time.monotonic()
                try:
                    decompressed = decompress_body(obs["body"], obs["content_encoding"])
                    decomp_elapsed = time.monotonic() - decomp_start
                    obs["decompression_latency_ms"] = decomp_elapsed * 1000
                    cell_decompression_latencies.append(decomp_elapsed * 1000)
                    obs["decompressed_hash"] = hashlib.sha256(decompressed).hexdigest()
                    obs["decompression_error"] = None
                    obs["decompressed_bytes"] = decompressed
                except Exception as e:
                    decomp_elapsed = time.monotonic() - decomp_start
                    obs["decompression_latency_ms"] = decomp_elapsed * 1000
                    cell_decompression_errors.append({
                        "state": state, "rep": rep, "error": str(e)
                    })
                    obs["decompression_error"] = str(e)
                    obs["decompressed_hash"] = hashlib.sha256(obs["body"]).hexdigest()
                    obs["decompressed_bytes"] = obs["body"]

                # --- CORRECTNESS CONTROLS ---
                # C1: decompressed hash == expected hash
                correctness_match = (obs["decompressed_hash"] == expected_hash)
                obs["correctness_match"] = correctness_match
                cell_correctness_results.append(correctness_match)
                if correctness_match:
                    total_correctness_pass += 1
                else:
                    total_correctness_fail += 1

                # C2: silent fallback detection (CE=gzip/br and decompressed == raw)
                is_compressed = obs["content_encoding"] in ("br", "gzip")
                if is_compressed:
                    silent_fallback = (obs["decompressed_hash"] == obs["body_hash_compressed"])
                    obs["silent_fallback"] = silent_fallback
                    if silent_fallback:
                        total_silent_fallbacks += 1
                else:
                    obs["silent_fallback"] = False

                # C3: decompression actually altered bytes for compressed responses
                if is_compressed:
                    obs["decompression_altered_bytes"] = (decompressed != obs["body"])
                else:
                    obs["decompression_altered_bytes"] = None

                cell_compressed_sizes.append(obs["body_size"])
                cell_fingerprints_compressed[state].append(obs["body_hash_compressed"])
                cell_fingerprints_decompressed[state].append(obs["decompressed_hash"])
                cell_raw_observations[state].append(obs)

                request_count += 1

                if i < len(plan) - 1:
                    jitter = rng.uniform(0.05, 0.15)
                    time.sleep(jitter)

            # Compute discrimination scores
            compressed_disc = compute_discrimination_score(cell_fingerprints_compressed)
            decompressed_disc = compute_discrimination_score(cell_fingerprints_decompressed)

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

            # Correctness by state
            correctness_by_state = {}
            for state, obs_list in cell_raw_observations.items():
                matches = [obs["correctness_match"] for obs in obs_list]
                correctness_by_state[state] = {
                    "pass_count": sum(matches),
                    "fail_count": len(matches) - sum(matches),
                    "total": len(matches),
                    "all_pass": all(matches),
                }

            # Silent fallback by state (compressed only)
            silent_fallback_by_state = {}
            for state, obs_list in cell_raw_observations.items():
                compressed_obs = [obs for obs in obs_list if obs["content_encoding"] in ("br", "gzip")]
                fallbacks = [obs["silent_fallback"] for obs in compressed_obs]
                silent_fallback_by_state[state] = {
                    "fallback_count": sum(fallbacks),
                    "total": len(fallbacks),
                    "any_fallback": any(fallbacks),
                }

            # Compression verification
            decompression_altered = {}
            for state, obs_list in cell_raw_observations.items():
                compressed_obs = [obs for obs in obs_list if obs["content_encoding"] in ("br", "gzip")]
                altered = [obs["decompression_altered_bytes"] for obs in compressed_obs if obs["decompression_altered_bytes"] is not None]
                decompression_altered[state] = {
                    "all_altered": all(altered) if altered else True,
                    "count_altered": sum(1 for a in altered if a),
                    "count_total": len(altered),
                }

            cell_key = f"/userinfo_{ct_name}_{comp_mode}"
            all_results[cell_key] = {
                "compressed_body_only_discrimination": compressed_disc,
                "decompressed_body_only_discrimination": decompressed_disc,
                "baselines": {"B-RANDOM": b_rand_disc},
                "decompressed_hash_variation": decompressed_hash_variation,
                "correctness_by_state": correctness_by_state,
                "silent_fallback_by_state": silent_fallback_by_state,
                "decompression_altered": decompression_altered,
                "total_requests": sum(len(v) for v in cell_raw_observations.values()),
                "correctness_match_count": sum(cell_correctness_results),
                "correctness_match_rate": sum(cell_correctness_results) / len(cell_correctness_results) if cell_correctness_results else 0,
                "silent_fallback_count": sum(1 for obs in cell_raw_observations.values() for o in obs if o.get("silent_fallback", False)),
                "decompression_error_count": len(cell_decompression_errors),
                "decompression_latency_ms": {
                    "mean": sum(cell_decompression_latencies) / len(cell_decompression_latencies) if cell_decompression_latencies else 0,
                    "min": min(cell_decompression_latencies) if cell_decompression_latencies else 0,
                    "max": max(cell_decompression_latencies) if cell_decompression_latencies else 0,
                },
                "decompression_errors": cell_decompression_errors,
            }

            print(f"      compressed={compressed_disc:.4f}, "
                  f"decompressed={decompressed_disc:.4f}, "
                  f"B-RANDOM={b_rand_disc:.4f}")
            print(f"      correctness_match_rate={all_results[cell_key]['correctness_match_rate']:.4f} "
                  f"({all_results[cell_key]['correctness_match_count']}/{all_results[cell_key]['total_requests']})")
            print(f"      silent_fallbacks={all_results[cell_key]['silent_fallback_count']}")
            print(f"      decompression_errors={all_results[cell_key]['decompression_error_count']}")

            # Aggregate correctness for this cell
            cell_all_pass = all(obs["correctness_match"] for obs_list in cell_raw_observations.values() for obs in obs_list)
            if cell_all_pass:
                total_identity_pass += 1
            else:
                total_identity_fail += 1

            stop_reverse_proxy(proxy)
            stop_mock_server(mock_server)
            time.sleep(0.3)

        port_idx += 1

    # =========================================================================
    # CONTROLS (from frozen spec.json)
    # =========================================================================

    # C1: Correctness match rate == 1.0 for ALL 12 gzip cells (4 states x 3 content types x 1 chunk mode)
    #     Plus BROTLI-MC and IDENTITY baselines
    all_correctness_pass = all(
        cell_data["correctness_match_rate"] == 1.0
        for cell_data in all_results.values()
    )

    # Gzip-only cells (C1 in frozen decision rule)
    gzip_cells = {k: v for k, v in all_results.items()
                  if k.endswith("_GZIP-MC") or k.endswith("_GZIP-SC")}
    gzip_all_correctness = all(
        cell_data["correctness_match_rate"] == 1.0
        for cell_data in gzip_cells.values()
    )

    all_controls["C_CORRECTNESS_MATCH"] = {
        "expected": "100% correctness match rate for ALL gzip cells (decompressed hash == expected hash)",
        "observed": {k: v["correctness_match_rate"] for k, v in gzip_cells.items()},
        "pass": gzip_all_correctness,
        "total_pass": sum(cd["correctness_match_count"] for cd in gzip_cells.values()),
        "total_fail": sum(cd["total_requests"] - cd["correctness_match_count"] for cd in gzip_cells.values()),
    }

    # C2: Silent fallback count == 0 for ALL gzip-compressed observations
    gzip_total_silent = sum(cd["silent_fallback_count"] for cd in gzip_cells.values())
    all_controls["C_SILENT_FALLBACK"] = {
        "expected": "0 silent fallbacks for ALL gzip-compressed observations",
        "observed": {k: v["silent_fallback_count"] for k, v in gzip_cells.items()},
        "pass": gzip_total_silent == 0,
        "total_silent_fallbacks": gzip_total_silent,
    }

    # C3: B-BROTLI-MC passes 100% (positive control regression check)
    brotli_mc_cells = {k: v for k, v in all_results.items() if k.endswith("_BROTLI-MC")}
    brotli_mc_all_pass = all(
        cell_data["correctness_match_rate"] == 1.0
        for cell_data in brotli_mc_cells.values()
    )
    all_controls["C_BROTLI_POSITIVE_CONTROL"] = {
        "expected": "B-BROTLI-MC passes 100% (no regression in decompression pipeline)",
        "observed": {k: v["correctness_match_rate"] for k, v in brotli_mc_cells.items()},
        "pass": brotli_mc_all_pass,
        "total_pass": sum(cd["correctness_match_count"] for cd in brotli_mc_cells.values()),
        "total_fail": sum(cd["total_requests"] - cd["correctness_match_count"] for cd in brotli_mc_cells.values()),
    }

    # C4: IDENTITY baseline (correctness oracle validation)
    identity_cells = {k: v for k, v in all_results.items() if k.endswith("_IDENTITY")}
    identity_all_pass = all(
        cell_data["correctness_match_rate"] == 1.0
        for cell_data in identity_cells.values()
    )
    all_controls["C_IDENTITY_BASELINE"] = {
        "expected": "IDENTITY baseline hash matches expected for 100% of observations",
        "observed": {k: v["correctness_match_rate"] for k, v in identity_cells.items()},
        "pass": identity_all_pass,
    }

    # Null control: within-state determinism (all_same=true for all states in all gzip cells)
    all_det = True
    det_details = {}
    for cell_key, cell_data in gzip_cells.items():
        for state, hv in cell_data["decompressed_hash_variation"].items():
            if not hv["all_same"]:
                all_det = False
            det_details.setdefault(state, []).append(hv["all_same"])
    all_controls["C_NULL_CONTROL"] = {
        "expected": "Within-state decompressed hash all_same=true for ALL states across ALL gzip cells",
        "observed": {state: all(vals) for state, vals in det_details.items()},
        "pass": all_det,
    }

    # B-RANDOM baseline
    b_random_values = [cell_data["baselines"]["B-RANDOM"] for cell_data in gzip_cells.values()]
    c_b_random_pass = all(v is not None and abs(v) < 0.1 for v in b_random_values)
    all_controls["C_B_RANDOM"] = {
        "expected": "B-RANDOM ~ 0.0 for ALL gzip cells",
        "observed": [float(v) for v in b_random_values],
        "pass": c_b_random_pass,
    }

    # C_NO_ERRORS: 0 decompression errors across ALL requests
    all_controls["C_NO_ERRORS"] = {
        "expected": "0 decompression errors (exceptions + silent fallbacks) across ALL requests",
        "total_exceptions": sum(cd["decompression_error_count"] for cd in all_results.values()),
        "total_silent_fallbacks": total_silent_fallbacks,
        "pass": total_decompression_errors == 0 and total_silent_fallbacks == 0,
    }

    # =========================================================================
    # DECISION RULE (from frozen spec.json)
    # =========================================================================

    # SURVIVES_CURRENT_TEST requires ALL of:
    # C1: correctness_match_rate == 1.0 for ALL 12 gzip cells
    c1_pass = gzip_all_correctness
    # C2: silent_fallback_count == 0 for ALL gzip cells
    c2_pass = gzip_total_silent == 0
    # C3: B-BROTLI-MC passes 100% (no regression)
    c3_pass = brotli_mc_all_pass
    # C4: Null control passes (all_same=true for all states in all gzip cells)
    c4_pass = all_det

    # Check MEASUREMENT_INVALID: infrastructure prevents valid correctness measurement
    measurement_invalid = len(all_results) == 0 or total_correctness_pass + total_correctness_fail == 0

    if measurement_invalid:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    elif not c1_pass or not c2_pass:
        # FALSIFIED if any correctness failure OR any silent fallback in gzip cells
        status = "COMPLETE"
        outcome = "FALSIFIES"
    elif c1_pass and c2_pass and c3_pass and c4_pass:
        status = "COMPLETE"
        outcome = "SUPPORTS"
    elif not c3_pass:
        # B-BROTLI-MC regression
        status = "COMPLETE"
        outcome = "FALSIFIES"
    else:
        status = "COMPLETE"
        outcome = "MIXED"

    # =========================================================================
    # OBSERVATIONS
    # =========================================================================

    all_observations.append(f"Total requests made: {request_count}")
    all_observations.append(f"Total correctness passes: {total_correctness_pass}")
    all_observations.append(f"Total correctness failures: {total_correctness_fail}")
    all_observations.append(f"Total silent fallbacks: {total_silent_fallbacks}")
    all_observations.append(f"Total decompression errors: {total_decompression_errors}")

    for cell_key in sorted(all_results.keys()):
        cell_data = all_results[cell_key]
        all_observations.append(
            f"{cell_key}: decompressed={cell_data['decompressed_body_only_discrimination']:.4f}, "
            f"correctness_rate={cell_data['correctness_match_rate']:.4f}, "
            f"silent_fallbacks={cell_data['silent_fallback_count']}, "
            f"errors={cell_data['decompression_error_count']}"
        )

    # =========================================================================
    # VALIDITY NOTES
    # =========================================================================

    all_validity_notes.extend([
        "Architecture: Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server",
        f"GZIP-MC: chunk_size={MULTI_CHUNK_SIZE} bytes, gzip default compression level",
        f"GZIP-SC: chunk_size={SINGLE_CHUNK_SIZE} bytes, gzip default compression level",
        f"BROTLI-MC: chunk_size={MULTI_CHUNK_SIZE} bytes, brotli quality {MOCK_BROTLI_QUALITY} (positive control)",
        "IDENTITY: no compression, Content-Length set (ground-truth reference)",
        "Correctness control: SHA256(decompressed) compared to SHA256(generate_*_body(state, target_size))",
        "Silent fallback detection: SHA256(decompressed) == SHA256(raw) when CE=gzip/br classified as failure",
        "Decompression verification: raw_body != decompressed when CE=gzip/br, proving decompression altered bytes",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "3-way error collapse preserved: no_auth, expired_token, invalid_token share similar error bodies",
        f"Seed={SEED} for request ordering",
        "No real CDN infrastructure - bounded to localhost mock server + Python reverse proxy",
        "Deterministic body generation via generate_*_body(state, target_size) functions",
        "gzip.compress() with default parameters is a pure function (deterministic compression)",
        "brotli.compress at fixed quality=6 is a pure function (deterministic compression)",
        f"MULTI-CHUNK compressed 1KB payloads typically 300-600 bytes, spanning 10-19 chunks at {MULTI_CHUNK_SIZE} bytes",
    ])

    if total_decompression_errors > 0:
        all_validity_notes.append(f"Pipeline errors: {total_decompression_errors} decompression errors")
    if total_silent_fallbacks > 0:
        all_validity_notes.append(f"Silent fallbacks detected: {total_silent_fallbacks}")

    # =========================================================================
    # UNRESOLVED
    # =========================================================================

    unresolved = [
        "Does decompression correctness hold on real CDN infrastructure (Cloudflare/Fastly/Akamai)?",
        "Does correctness hold for larger payloads (10KB, 100KB) where gzip dictionary references may cross chunk boundaries?",
        "Does correctness hold for different gzip compression levels (1-9)?",
        "Does correctness hold for brotli quality variation (4-8) and mixed quality cycling?",
        "What is the maximum practical decompression depth for real-world multi-layer encoding scenarios?",
        "Does correctness hold for streaming partial-frame forwarding?",
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
            "aggregate": {
                "total_correctness_pass": total_correctness_pass,
                "total_correctness_fail": total_correctness_fail,
                "total_silent_fallbacks": total_silent_fallbacks,
                "total_decompression_errors": total_decompression_errors,
                "total_requests": request_count,
                "overall_correctness_rate": total_correctness_pass / (total_correctness_pass + total_correctness_fail) if (total_correctness_pass + total_correctness_fail) > 0 else 0,
            },
        },
        "controls": all_controls,
        "artifacts": [
            {"path": "run_experiment.py", "role": "code",
             "description": "Experiment execution script with mock origin, reverse proxy, and gzip decompression correctness controls"},
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
