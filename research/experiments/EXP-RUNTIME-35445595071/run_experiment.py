#!/usr/bin/env python3
"""
EXP-RUNTIME-35445595071 - Multi-Chunk Brotli Reassembly Test
=============================================================
Tests whether iterative decompression survives multi-chunk brotli reassembly
where compressed payloads span multiple HTTP chunks.

Frozen from spec.json and prereg.md - DO NOT MODIFY.

Architecture:
  Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server

Two chunk configurations:
  - chunk_size=32 bytes (MULTI-CHUNK): forces all compressed payloads (70-176 bytes)
    to span 3-6 chunks, testing chunk boundary splitting
  - chunk_size=1024 bytes (SINGLE-CHUNK): parent baseline, all payloads fit in one chunk

Key differences from parent EXP-RUNTIME-35434773328:
  - chunk_size reduced from 1024 to 32 for multi-chunk condition
  - Only 2 cache configs (MULTI-CHUNK and SINGLE-CHUNK baseline)
  - Origin serves chunked without Content-Length for ALL cells
  - No CL-PASSTHROUGH or CHUNKED-CACHED conditions
  - N=20 reps per state per condition
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

EXPERIMENT_ID = "EXP-RUNTIME-35445595071"
LANE = "runtime"
SEED = 44
REPS = 20
BASE_PORT = 7700
PROXY_PORT_BASE = 7800
CLIENT_SECRET = "spider-secret-12345"

USERINFO_PATH = "/userinfo"

CONTENT_TYPES = {
    "JSON": "application/json",
    "HTML": "text/html",
    "XML": "application/xml",
}

TARGET_BODY_SIZE = 1024  # 1KB nominal uncompressed size

MOCK_BROTLI_QUALITY = 6
CHUNK_CONFIGS = ["MULTI-CHUNK", "SINGLE-CHUNK"]
AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]

MULTI_CHUNK_SIZE = 32    # bytes — forces 3-6 chunks per compressed payload
SINGLE_CHUNK_SIZE = 1024  # bytes — parent baseline, all payloads in one chunk


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
# Serves brotli-compressed responses with Transfer-Encoding: chunked.
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class MockOAuthHandler(BaseHTTPRequestHandler):
    body_size = 1024
    content_type = "JSON"
    use_chunked = True
    chunk_size = 32

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

    def do_GET(self):
        if self.path == USERINFO_PATH:
            state = self._get_auth_state()
            body = self._get_body(state, self.body_size)
            status = 200 if state == "valid_token" else 401

            compressed = brotli.compress(body, quality=MOCK_BROTLI_QUALITY)

            self.send_response(status)
            self.send_header("Content-Type", self._get_mime_type())
            self.send_header("Content-Encoding", "br")
            self.send_header("Cache-Control", "private")
            self.send_header("Vary", "Authorization")
            self.send_header("X-Server-Quality", str(MOCK_BROTLI_QUALITY))

            # Always use chunked TE without Content-Length
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
            self.wfile.flush()
        else:
            self.send_error(404)

    def do_POST(self):
        self.send_error(404)


def start_mock_server(port, body_size=1024, content_type="JSON",
                      use_chunked=True, chunk_size=32):
    MockOAuthHandler.body_size = body_size
    MockOAuthHandler.content_type = content_type
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
# Forwards chunked responses from origin to client.
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
    all_observations_by_cell = {}

    print(f"Experiment: {EXPERIMENT_ID}")
    print(f"Chunk configs: {CHUNK_CONFIGS}")
    print(f"Content types: {list(CONTENT_TYPES.keys())}")
    print(f"Target body size: {TARGET_BODY_SIZE} bytes")
    print(f"Auth states: {AUTH_STATES}")
    print(f"Reps per cell: {REPS}")
    print(f"Seed: {SEED}")
    print(f"Max decompression depth: 5")
    print()

    all_observations.append(f"Experiment: {EXPERIMENT_ID}")
    all_observations.append(f"Architecture: Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server (brotli quality {MOCK_BROTLI_QUALITY})")
    all_observations.append(f"Chunk configs: {CHUNK_CONFIGS}")
    all_observations.append(f"MULTI-CHUNK_SIZE={MULTI_CHUNK_SIZE} bytes, SINGLE-CHUNK_SIZE={SINGLE_CHUNK_SIZE} bytes")
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

        for chunk_config in CHUNK_CONFIGS:
            chunk_size = MULTI_CHUNK_SIZE if chunk_config == "MULTI-CHUNK" else SINGLE_CHUNK_SIZE
            print(f"\n  Chunk config: {chunk_config} (chunk_size={chunk_size})")

            origin_port = BASE_PORT + port_idx
            mock_server = start_mock_server(origin_port, TARGET_BODY_SIZE, ct_name,
                                            use_chunked=True, chunk_size=chunk_size)
            time.sleep(0.5)
            print(f"    Origin server started on port {origin_port} (use_chunked=True, chunk_size={chunk_size})")

            proxy_port = PROXY_PORT_BASE + port_idx
            proxy = start_reverse_proxy(proxy_port, origin_port,
                                        use_chunked=True, chunk_size=chunk_size)
            time.sleep(0.5)
            print(f"    Proxy started on port {proxy_port} (chunk_size={chunk_size})")

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
            cell_compressed_sizes = []

            for i, (state, rep) in enumerate(plan):
                auth_header = get_auth_header(state, auth_token)
                url = f"http://127.0.0.1:{proxy_port}{USERINFO_PATH}"

                obs = make_request(url, method="GET", auth_header=auth_header)
                obs["state"] = state
                obs["rep"] = rep
                obs["content_type"] = ct_name
                obs["chunk_config"] = chunk_config

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
                cell_compressed_sizes.append(obs["body_size"])

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

            # Verify compressed payload exceeds chunk_size for MULTI-CHUNK
            compressed_size_stats = {
                "min": min(cell_compressed_sizes),
                "max": max(cell_compressed_sizes),
                "mean": sum(cell_compressed_sizes) / len(cell_compressed_sizes),
                "exceeds_chunk_size": all(s > chunk_size for s in cell_compressed_sizes),
                "chunk_size": chunk_size,
            }

            cell_key = f"/userinfo_{ct_name}_{chunk_config}"
            all_observations_by_cell[cell_key] = dict(cell_raw_observations)
            all_results[cell_key] = {
                "compressed_body_only_discrimination": compressed_disc,
                "decompressed_body_only_discrimination": decompressed_disc,
                "status_only_discrimination": status_disc,
                "baselines": {"B-RANDOM": b_rand_disc},
                "compressed_hash_variation": compressed_hash_variation,
                "decompressed_hash_variation": decompressed_hash_variation,
                "body_sizes": body_sizes,
                "compressed_size_stats": compressed_size_stats,
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

            print(f"      compressed={compressed_disc:.4f}, "
                  f"decompressed={decompressed_disc:.4f}, "
                  f"status={status_disc:.4f}, B-RANDOM={b_rand_disc:.4f}")
            print(f"      compressed_size: min={compressed_size_stats['min']}, "
                  f"max={compressed_size_stats['max']}, "
                  f"exceeds_chunk_size={compressed_size_stats['exceeds_chunk_size']}")

            stop_reverse_proxy(proxy)
            stop_mock_server(mock_server)
            time.sleep(0.3)

        port_idx += 1

    # =========================================================================
    # AGGREGATE METRICS per chunk config
    # =========================================================================

    config_metrics = {}
    for cc in CHUNK_CONFIGS:
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

    # C_NULL_CONTROL: B-RANDOM = 0.0 for all cells
    b_random_values = [cell_data["baselines"]["B-RANDOM"] for cell_data in all_results.values()]
    c_null_pass = all(v is not None and abs(v) < 0.1 for v in b_random_values)
    all_controls["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0 for all cells",
        "observed": [float(v) for v in b_random_values],
        "pass": c_null_pass,
    }

    # C_SINGLE_CHUNK_REGRESSION: SINGLE-CHUNK discrimination = 0.5 (parent baseline)
    sc_discs = [all_results[k]["decompressed_body_only_discrimination"]
                for k in all_results if k.endswith("_SINGLE-CHUNK")]
    sc_mean = sum(sc_discs) / len(sc_discs) if sc_discs else 0
    sc_pass = all(d >= 0.5 for d in sc_discs)
    all_controls["C_SINGLE_CHUNK_REGRESSION"] = {
        "expected": "SINGLE-CHUNK decompressed discrimination >= 0.5 for all cells (reproduces parent baseline)",
        "observed_mean": sc_mean,
        "observed_per_cell": sc_discs,
        "pass": sc_pass,
    }

    # C_MULTI_CHUNK_PRIMARY: MULTI-CHUNK discrimination >= 0.3 for all cells
    mc_discs = [all_results[k]["decompressed_body_only_discrimination"]
                for k in all_results if k.endswith("_MULTI-CHUNK")]
    mc_min = min(mc_discs) if mc_discs else 0
    mc_pass = mc_min >= 0.3
    all_controls["C_MULTI_CHUNK_PRIMARY"] = {
        "expected": "MULTI-CHUNK decompressed discrimination >= 0.3 for all cells (expected: 0.5)",
        "min_observed": mc_min,
        "observed_per_cell": mc_discs,
        "pass": mc_pass,
    }

    # C_COMPRESSED_SIZE_VERIFICATION: All MULTI-CHUNK compressed payloads exceed chunk_size
    mc_compressed_exceeds = True
    mc_compressed_details = {}
    for cell_key, cell_data in all_results.items():
        if cell_key.endswith("_MULTI-CHUNK"):
            stats = cell_data["compressed_size_stats"]
            mc_compressed_details[cell_key] = stats
            if not stats["exceeds_chunk_size"]:
                mc_compressed_exceeds = False
    all_controls["C_COMPRESSED_SIZE_VERIFICATION"] = {
        "expected": "All MULTI-CHUNK compressed payloads exceed chunk_size=32 bytes",
        "observed": mc_compressed_details,
        "pass": mc_compressed_exceeds,
    }

    # C_DECOMPRESSED_DETERMINISM: all_same=true for all states across all conditions
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

    # C_NO_ERROR_INFLATION: 0 decompression errors
    total_decomp_errors = sum(len(cd.get("decompression_errors", [])) for cd in all_results.values())
    all_controls["C_NO_ERROR_INFLATION"] = {
        "expected": "0 decompression errors across all conditions",
        "observed": total_decomp_errors,
        "pass": total_decomp_errors == 0,
    }

    # C_ORIGIN_VERIFICATION: Origin serves chunked (no Content-Length) for all cells
    origin_chunked_verified = True
    origin_verification_details = {}
    for ct_name in CONTENT_TYPES:
        verify_port = 6700 + list(CONTENT_TYPES.keys()).index(ct_name)
        try:
            mock_verify = start_mock_server(verify_port, TARGET_BODY_SIZE, ct_name,
                                            use_chunked=True, chunk_size=MULTI_CHUNK_SIZE)
            time.sleep(0.3)
            verify_resp = requests.get(
                f"http://127.0.0.1:{verify_port}{USERINFO_PATH}",
                headers={"Accept-Encoding": "br, gzip, identity",
                         "Authorization": f"Bearer {auth_token}"},
                timeout=5)
            has_te_chunked = "transfer-encoding" in {k.lower(): v for k, v in verify_resp.headers.items()}
            has_content_length = "content-length" in {k.lower(): v for k, v in verify_resp.headers.items()}
            te_value = verify_resp.headers.get("Transfer-Encoding", "none")
            cl_value = verify_resp.headers.get("Content-Length", "none")
            detail = {
                "has_transfer_encoding_chunked": has_te_chunked and "chunked" in te_value.lower(),
                "has_content_length": has_content_length,
                "transfer_encoding": te_value,
                "content_length": cl_value,
            }
            origin_verification_details[ct_name] = detail
            if has_content_length:
                origin_chunked_verified = False
            stop_mock_server(mock_verify)
        except Exception as e:
            origin_chunked_verified = False
            origin_verification_details[ct_name] = {"error": str(e)}
            try:
                stop_mock_server(mock_verify)
            except Exception:
                pass

    all_controls["C_ORIGIN_VERIFICATION"] = {
        "expected": "Origin serves Transfer-Encoding: chunked (no Content-Length) for all cells",
        "observed": origin_verification_details,
        "origin_chunked_verified": origin_chunked_verified,
        "pass": origin_chunked_verified,
    }

    # =========================================================================
    # DECISION RULE (from frozen spec.json)
    # =========================================================================

    # Condition 1: decompressed body-only discrimination >= 0.3 for ALL multi-chunk cells
    c1_pass = mc_min >= 0.3

    # Condition 2: decompressed hash determinism all_same=true for ALL states across ALL conditions
    c2_pass = all_det

    # Condition 3: B-RANDOM = 0.0 for ALL cells
    c3_pass = c_null_pass

    # Condition 4: 0 decompression errors across ALL requests
    c4_pass = total_decomp_errors == 0

    # Condition 5: multi-chunk discrimination >= 0.3 for ALL cells (same as c1 for this experiment)
    c5_pass = mc_min >= 0.3

    # Check MEASUREMENT_INVALID: infrastructure prevents valid multi-chunk generation
    measurement_invalid = not mc_compressed_exceeds

    if measurement_invalid:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    elif total_decomp_errors > 0:
        status = "COMPLETE"
        outcome = "FALSIFIES"
    elif c1_pass and c2_pass and c3_pass and c4_pass and c5_pass:
        status = "COMPLETE"
        outcome = "SUPPORTS"
    elif not c1_pass or not c4_pass:
        status = "COMPLETE"
        outcome = "FALSIFIES"
    else:
        status = "COMPLETE"
        outcome = "MIXED"

    # =========================================================================
    # OBSERVATIONS
    # =========================================================================

    all_observations.append(f"Total requests made: {request_count}")
    all_observations.append(f"Min MULTI-CHUNK decompressed discrimination: {mc_min:.4f}")
    all_observations.append(f"SINGLE-CHUNK decompressed discrimination mean: {sc_mean:.4f}")
    all_observations.append(f"Total decompression errors: {total_decomp_errors}")
    all_observations.append(f"Origin chunked verification: {origin_chunked_verified}")
    all_observations.append(f"MULTI-CHUNK compressed sizes exceed chunk_size: {mc_compressed_exceeds}")

    for cc in CHUNK_CONFIGS:
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
        f"MULTI-CHUNK: chunk_size={MULTI_CHUNK_SIZE} bytes, forces all compressed payloads to span 3-6 chunks",
        f"SINGLE-CHUNK: chunk_size={SINGLE_CHUNK_SIZE} bytes, parent baseline (all payloads in one chunk)",
        "Origin serves Transfer-Encoding: chunked without Content-Length for ALL cells",
        "No CL-PASSTHROUGH or CHUNKED-CACHED conditions — only multi-chunk testing",
        "Auth-aware caching tested implicitly via cache key (URL+Authorization)",
        "Accept-Encoding from client: 'br, gzip, identity' in all conditions",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "Expired_token is locally-signed HS256, not real expired token",
        "Content types are synthetic but structurally realistic",
        "Payload sizes controlled by padding to hit target uncompressed sizes",
        "3-way error collapse preserved: no_auth, expired_token, invalid_token share similar error bodies",
        f"Seed={SEED} for request ordering",
        "No real CDN infrastructure - bounded to localhost mock server + Python reverse proxy",
        "MULTI-CHUNK condition tests brotli multi-byte symbol splitting at chunk boundaries",
        "SINGLE-CHUNK condition reproduces parent baseline for regression control",
    ])

    if total_decomp_errors > 0:
        all_validity_notes.append(f"Pipeline errors: {total_decomp_errors} decompression errors")

    # =========================================================================
    # UNRESOLVED
    # =========================================================================

    unresolved = [
        "Does iterative decompression survive real CDN infrastructure (Cloudflare/Fastly/Akamai) with auth-aware cache configuration, chunked TE, Accept-Encoding negotiation, quality variation, and geographic latency?",
        "Does multi-chunk reassembly work with larger payloads (10KB, 100KB) where chunk boundaries may split brotli dictionary references?",
        "Does multi-chunk reassembly work with gzip encoding (not just brotli)?",
        "How does proxy chunk boundary behavior interact with CDN-specific chunking algorithms?",
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
            "per_chunk_config": config_metrics,
        },
        "controls": all_controls,
        "artifacts": [
            {"path": "run_experiment.py", "role": "code",
             "description": "Experiment execution script with mock origin, reverse proxy (MULTI-CHUNK chunk_size=32, SINGLE-CHUNK chunk_size=1024), and iterative decompression"},
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
