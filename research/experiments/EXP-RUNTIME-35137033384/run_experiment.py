#!/usr/bin/env python3
"""
EXP-RUNTIME-35137033384 - Decompression-Normalization Under CDN-Like Non-Determinism
=====================================================================================
Tests decompression-normalization (SHA256 on decompressed body + status) under
realistic CDN-like non-determinism simulated via a CDN-noise proxy layer.

CDN-noise categories (per frozen spec section 4):
  1. Brotli quality variation {4,5,6,7,8} per request
  2. Chunked transfer-encoding (~30% of responses)
  3. CDN-specific response headers (CF-Ray, X-Cache, Age, Via)
  4. Accept-Encoding negotiation (20% gzip, 5% identity, rest brotli)
  5. Response caching (~30% cache hits)
  6. Content-Length variation (passive consequence)

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

EXPERIMENT_ID = "EXP-RUNTIME-35137033384"
LANE = "runtime"
SEED = 44
REPS = 20
MOCK_SERVER_PORT = 5000
CDN_PROXY_PORT = 5001
CLIENT_SECRET = "spider-secret-12345"

USERINFO_PATH = "/userinfo"
INTROSPECT_PATH = "/introspect"

# Frozen brotli quality range for CDN noise
BROTLI_QUALITY_RANGE = (4, 5, 6, 7, 8)

# CDN noise parameters (from frozen spec section 4)
CHUNKED_PROB = 0.3       # 30% of responses get chunked encoding
GZIP_OVERRIDE_PROB = 0.2  # 20% CDN responds with gzip regardless of client
IDENTITY_OVERRIDE_PROB = 0.05  # 5% CDN responds with identity
CACHE_HIT_PROB = 0.3      # 30% cache hits

AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]

BROTLI_AVAILABLE = True
try:
    import brotli as _brotli_test
except ImportError:
    BROTLI_AVAILABLE = False
    print("WARNING: brotli module not available. Brotli conditions will fail.")


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
# MOCK OAUTH2 SERVER (identical to parent)
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class MockOAuthHandler(BaseHTTPRequestHandler):
    body_size = 1024
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

    def do_GET(self):
        if self.path == USERINFO_PATH:
            if self._check_auth():
                body = json.dumps({
                    "sub": "alice",
                    "name": "Alice",
                    "email": "alice@example.com",
                    "data": "x" * (self.body_size - 100),
                }).encode()
            else:
                body = json.dumps({"error": "invalid_token"}).encode()

            self.send_response(200 if self._check_auth() else 401)
            self.send_header("Content-Type", "application/json")
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

            try:
                payload = jwt.decode(token, CLIENT_SECRET, algorithms=["HS256"])
                body = json.dumps({"active": True, "sub": payload.get("sub")}).encode()
            except jwt.ExpiredSignatureError:
                body = json.dumps({"active": False, "error": "token expired"}).encode()
            except jwt.InvalidTokenError:
                body = json.dumps({"active": False, "error": "invalid token"}).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)


def start_mock_server(body_size=1024, seed=44):
    MockOAuthHandler.body_size = body_size
    MockOAuthHandler.seed = seed
    server = ReusableHTTPServer(("127.0.0.1", MOCK_SERVER_PORT), MockOAuthHandler)
    server.timeout = 0.5
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Mock OAuth2 server started on port {MOCK_SERVER_PORT}")
    return server


def stop_mock_server(server):
    if server:
        server.shutdown()
        print("Mock server stopped.")


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
# CHUNKED TRANSFER-ENCODING WRAPPER
# ---------------------------------------------------------------------------

def wrap_chunked(data):
    """Wrap data in HTTP chunked transfer-encoding format.
    Splits into chunks of 1-4 KB."""
    chunks = []
    offset = 0
    while offset < len(data):
        chunk_size = random.randint(1024, 4096)
        chunk = data[offset:offset + chunk_size]
        chunks.append(f"{len(chunk):x}\r\n".encode() + chunk + b"\r\n")
        offset += chunk_size
    chunks.append(b"0\r\n\r\n")
    return b"".join(chunks)


# ---------------------------------------------------------------------------
# CDN-NOISE PROXY (the core of this experiment)
# ---------------------------------------------------------------------------

class CDNNoiseProxyHandler(BaseHTTPRequestHandler):
    """Proxy that applies 6 categories of CDN-like non-determinism."""
    quality_rng = None
    noise_rng = None
    cache = {}  # keyed by (path, auth_hash) -> (compressed_body, encoding, status, original_headers)
    cache_hits = 0
    cache_misses = 0

    def log_message(self, format, *args):
        pass

    def _select_quality(self):
        """Category 1: Brotli quality variation {4,5,6,7,8} per request."""
        idx = self.quality_rng.randint(0, len(BROTLI_QUALITY_RANGE) - 1)
        return BROTLI_QUALITY_RANGE[idx]

    def _should_chunk(self):
        """Category 2: ~30% of responses get chunked transfer-encoding."""
        return self.noise_rng.random() < CHUNKED_PROB

    def _generate_cdn_headers(self):
        """Category 3: CDN-specific response headers that vary per request."""
        cf_ray = hashlib.md5(self.noise_rng.getrandbits(128).to_bytes(16, 'big')).hexdigest()
        x_cache = self.noise_rng.choice(["HIT", "MISS"])
        age = self.noise_rng.randint(0, 300)
        via = "1.1 varnish"
        return {
            "CF-Ray": cf_ray,
            "X-Cache": x_cache,
            "Age": str(age),
            "Via": via,
        }

    def _select_encoding(self):
        """Category 4: Accept-Encoding negotiation override.
        20% gzip, 5% identity, 75% brotli (default)."""
        r = self.noise_rng.random()
        if r < IDENTITY_OVERRIDE_PROB:
            return "identity"
        elif r < IDENTITY_OVERRIDE_PROB + GZIP_OVERRIDE_PROB:
            return "gzip"
        else:
            return "br"

    def _get_cache_key(self, path, auth_header):
        """Generate cache key from path and auth state hash."""
        auth_hash = hashlib.md5((auth_header or "none").encode()).hexdigest()[:8]
        return (path, auth_hash)

    def _should_cache_serve(self):
        """Category 5: ~30% cache hits."""
        return self.noise_rng.random() < CACHE_HIT_PROB

    def _send_response_body(self, body, use_chunked):
        """Send response body, optionally wrapped in chunked transfer-encoding."""
        if use_chunked:
            chunked_data = wrap_chunked(body)
            self.wfile.write(chunked_data)
        else:
            self.wfile.write(body)

    def do_request(self):
        target_url = f"http://127.0.0.1:{MOCK_SERVER_PORT}{self.path}"

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Forward headers (skip hop-by-hop)
        headers = {}
        for key in self.headers:
            if key.lower() not in ("host", "transfer-encoding", "connection"):
                headers[key] = self.headers[key]
        # Always request identity from upstream so we control compression
        headers["Accept-Encoding"] = "identity"

        # Check cache first (Category 5)
        auth_header = headers.get("Authorization", "")
        cache_key = self._get_cache_key(self.path, auth_header)

        if cache_key in self.cache and self._should_cache_serve():
            # Cache HIT: serve cached compressed response with new CDN headers
            cached_body, cached_encoding, cached_status, _ = self.cache[cache_key]
            self.cache_hits += 1

            cdn_headers = self._generate_cdn_headers()
            cdn_headers["X-Cache"] = "HIT"

            # Category 2: Decide chunked BEFORE sending headers
            use_chunked = self._should_chunk()

            self.send_response(cached_status)
            self.send_header("Content-Encoding", cached_encoding)
            self.send_header("Content-Type", "application/json")
            if use_chunked:
                self.send_header("Transfer-Encoding", "chunked")
            else:
                self.send_header("Content-Length", str(len(cached_body)))
            for k, v in cdn_headers.items():
                self.send_header(k, v)
            self.end_headers()

            self._send_response_body(cached_body, use_chunked)
            return

        # Cache MISS: forward to mock server
        self.cache_misses += 1

        try:
            if self.command == "GET":
                resp = requests.get(target_url, headers=headers, timeout=10, allow_redirects=False)
            elif self.command == "POST":
                resp = requests.post(target_url, headers=headers, data=body, timeout=10, allow_redirects=False)
            else:
                self.send_error(501, "Not Implemented")
                return
        except Exception as e:
            self.send_error(502, f"Bad Gateway: {e}")
            return

        raw_body = resp.content
        original_status = resp.status_code

        # Category 4: Select encoding (may override client preference)
        encoding = self._select_encoding()

        # Compress with selected encoding
        if encoding == "br":
            quality = self._select_quality()  # Category 1
            compressed_body = compress_brotli(raw_body, quality=quality)
        elif encoding == "gzip":
            compressed_body = compress_gzip(raw_body, level=9)
        else:
            # identity: no compression
            compressed_body = raw_body

        # Store in cache (Category 5)
        self.cache[cache_key] = (compressed_body, encoding, original_status, resp.headers)

        # Category 3: CDN-specific headers
        cdn_headers = self._generate_cdn_headers()

        # Category 2: Chunked transfer-encoding - decide BEFORE headers
        use_chunked = self._should_chunk()

        # Send response
        self.send_response(original_status)
        self.send_header("Content-Encoding", encoding)
        self.send_header("Content-Type", "application/json")

        # Category 6: Content-Length varies (omitted for chunked)
        if use_chunked:
            self.send_header("Transfer-Encoding", "chunked")
        else:
            self.send_header("Content-Length", str(len(compressed_body)))

        # Category 3: Add CDN headers
        for k, v in cdn_headers.items():
            self.send_header(k, v)

        self.end_headers()

        # Category 2: Write body
        self._send_response_body(compressed_body, use_chunked)

    def do_GET(self):
        self.do_request()

    def do_POST(self):
        self.do_request()


def start_cdn_proxy(quality_seed, noise_seed):
    CDNNoiseProxyHandler.quality_rng = random.Random(quality_seed)
    CDNNoiseProxyHandler.noise_rng = random.Random(noise_seed)
    CDNNoiseProxyHandler.cache = {}
    CDNNoiseProxyHandler.cache_hits = 0
    CDNNoiseProxyHandler.cache_misses = 0
    server = ReusableHTTPServer(("127.0.0.1", CDN_PROXY_PORT), CDNNoiseProxyHandler)
    server.timeout = 0.5
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"CDN-noise proxy started on port {CDN_PROXY_PORT}")
    return server


def stop_cdn_proxy(server):
    if server:
        server.shutdown()
        print(f"CDN proxy stopped. Cache hits: {CDNNoiseProxyHandler.cache_hits}, "
              f"misses: {CDNNoiseProxyHandler.cache_misses}")


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
    """Compute Jaccard distance between fingerprint sets across auth states.
    Jaccard(A,B) = |A∩B|/|A∪B|, distance = 1 - Jaccard.
    We use: mean_{i!=j} (|F_i XOR F_j| / |F_i UNION F_j|)
    But following parent: intra_match_rate - inter_match_rate."""
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

def get_endpoint_configs(auth_token, proxy_port):
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
            "url": f"http://127.0.0.1:{proxy_port}{USERINFO_PATH}",
            "method": "GET",
            "body_fn": lambda state: None,
            "expected_status_fn": userinfo_expected_status,
        },
        {
            "name": "/introspect",
            "url": f"http://127.0.0.1:{proxy_port}{INTROSPECT_PATH}",
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
    print(f"Brotli quality range: {BROTLI_QUALITY_RANGE}")
    print(f"CDN noise: chunked={CHUNKED_PROB}, gzip_override={GZIP_OVERRIDE_PROB}, "
          f"identity_override={IDENTITY_OVERRIDE_PROB}, cache_hit={CACHE_HIT_PROB}")
    print()

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated. Length: {len(auth_token)}")

    BODY_SIZE = 1024

    # Derive CDN noise seeds deterministically from experiment seed (prereg section 9)
    # CDN noise seed = seed + hash("CDN_NOISE") % 10000
    cdn_noise_seed = (SEED + int(_hashlib.sha256(b"CDN_NOISE").hexdigest(), 16) % 10000) % (2**31)
    quality_seed = SEED + 1000  # separate seed for quality variation

    print(f"CDN noise seed: {cdn_noise_seed}")
    print(f"Quality seed: {quality_seed}")

    mock_server = start_mock_server(BODY_SIZE, SEED)
    time.sleep(0.5)

    # Test mock server connectivity
    try:
        test_resp = requests.get(f"http://127.0.0.1:{MOCK_SERVER_PORT}{USERINFO_PATH}",
                                 headers={"Authorization": f"Bearer {auth_token}"},
                                 timeout=5)
        print(f"Mock server test: status={test_resp.status_code}, body_size={len(test_resp.content)}")
    except Exception as e:
        print(f"WARNING: Mock server test failed: {e}")

    cdn_proxy = start_cdn_proxy(quality_seed, cdn_noise_seed)
    time.sleep(0.5)

    endpoints = get_endpoint_configs(auth_token, CDN_PROXY_PORT)

    # Run B-DECOMPRESSED-VARYING-BROTLI-CDN (primary) and B-COMPRESSED-VARYING-BROTLI-CDN (secondary)
    baselines_to_run = ["DECOMPRESSED-VARYING-BROTLI-CDN", "COMPRESSED-VARYING-BROTLI-CDN"]

    for baseline_name in baselines_to_run:
        print(f"\n{'='*70}")
        print(f"BASELINE: {baseline_name}")
        print(f"{'='*70}")

        condition_results = {}
        condition_raw_obs = {}

        for ep in endpoints:
            ep_name = ep["name"]
            print(f"\n  Endpoint: {ep_name}")

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

            for i, (state, rep) in enumerate(plan):
                auth_header = get_auth_header(state, auth_token)
                body = ep["body_fn"](state)

                try:
                    obs = make_request(ep["url"], method=ep["method"],
                                       auth_header=auth_header, body=body)
                    obs["state"] = state
                    obs["rep"] = rep
                    obs["baseline"] = baseline_name
                    obs["fingerprint_compressed"] = fingerprint_compressed_only(obs)
                    obs["fingerprint_decompressed"] = fingerprint_decompressed(obs)
                    obs["fingerprint_status"] = fingerprint_status_only(obs)
                    obs["body_hash_compressed"] = hashlib.sha256(obs["body"]).hexdigest()
                    obs["body_size"] = len(obs["body"])

                    ce = obs["headers"].get("Content-Encoding", "none")
                    obs["content_encoding"] = ce

                    # Track CDN headers for verification
                    obs["cdn_headers"] = {
                        "CF-Ray": obs["headers"].get("CF-Ray", ""),
                        "X-Cache": obs["headers"].get("X-Cache", ""),
                        "Age": obs["headers"].get("Age", ""),
                        "Via": obs["headers"].get("Via", ""),
                    }

                    raw_observations[state].append(obs)

                    # For DECOMPRESSED baseline, use decompressed fingerprint
                    # For COMPRESSED baseline, use compressed fingerprint
                    if baseline_name == "DECOMPRESSED-VARYING-BROTLI-CDN":
                        fingerprints_decompressed_by_state[state].append(obs["fingerprint_decompressed"])
                        fingerprints_compressed_by_state[state].append(obs["fingerprint_compressed"])
                    else:
                        # COMPRESSED: only compressed fingerprint matters
                        fingerprints_compressed_by_state[state].append(obs["fingerprint_compressed"])
                        # Also track decompressed for reference
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
            if baseline_name == "DECOMPRESSED-VARYING-BROTLI-CDN":
                compressed_disc = compute_discrimination_score(fingerprints_compressed_by_state)
                decompressed_disc = compute_discrimination_score(fingerprints_decompressed_by_state)
            else:
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
                decompressed_hashes = []
                for obs in obs_list:
                    ce = obs["headers"].get("Content-Encoding", "")
                    dec = decompress_body(obs["body"], ce)
                    decompressed_hashes.append(hashlib.sha256(dec).hexdigest())
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

            # CDN header verification (Category 3)
            cdn_header_verification = {}
            for state, obs_list in raw_observations.items():
                cf_ray_values = [obs["cdn_headers"]["CF-Ray"] for obs in obs_list]
                x_cache_values = [obs["cdn_headers"]["X-Cache"] for obs in obs_list]
                age_values = [obs["cdn_headers"]["Age"] for obs in obs_list]
                via_values = [obs["cdn_headers"]["Via"] for obs in obs_list]
                cdn_header_verification[state] = {
                    "cf_ray_unique": len(set(cf_ray_values)),
                    "x_cache_values": list(set(x_cache_values)),
                    "age_range": [min(int(a) for a in age_values), max(int(a) for a in age_values)],
                    "via_values": list(set(via_values)),
                }

            ep_key = f"{ep_name}_{baseline_name}"
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
                "cdn_header_verification": cdn_header_verification,
                "body_sizes": body_sizes,
                "total_requests": sum(len(v) for v in raw_observations.values()),
            }
            condition_raw_obs[ep_name] = raw_observations

            print(f"    Compressed body-only: {compressed_disc:.6f}, "
                  f"Decompressed body-only: {decompressed_disc:.6f}, "
                  f"Status-only: {status_disc:.6f}, B-RANDOM: {b_rand_disc:.6f}")

            for state in AUTH_STATES:
                chv = compressed_hash_variation[state]
                dhv = decompressed_hash_variation[state]
                print(f"    {state}: compressed_unique={chv['unique_count']}/{chv['total']} "
                      f"decompressed_unique={dhv['unique_count']}/{dhv['total']}")

        raw_observations_all[baseline_name] = condition_raw_obs
        all_results[baseline_name] = condition_results

    stop_cdn_proxy(cdn_proxy)
    time.sleep(1.0)
    stop_mock_server(mock_server)
    time.sleep(0.5)

    # =========================================================================
    # ASSEMBLE METRICS
    # =========================================================================

    metrics = {}
    for baseline_name in baselines_to_run:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_{baseline_name}"
            if baseline_name in all_results and key in all_results[baseline_name]:
                metrics[key] = all_results[baseline_name][key]

    # Primary metric: /userinfo discrimination
    userinfo_decompressed_disc = None
    userinfo_compressed_disc = None
    key_dec = "/userinfo_DECOMPRESSED-VARYING-BROTLI-CDN"
    key_comp = "/userinfo_COMPRESSED-VARYING-BROTLI-CDN"
    if key_dec in metrics:
        userinfo_decompressed_disc = metrics[key_dec]["decompressed_body_only_discrimination"]
    if key_comp in metrics:
        userinfo_compressed_disc = metrics[key_comp]["compressed_body_only_discrimination"]

    # Parent reference data (from EXP-RUNTIME-35058619700)
    PARENT_DECOMPRESSED_VARYING_GZIP_USERINFO = 0.5

    # =========================================================================
    # CONTROLS
    # =========================================================================

    control_details = {}

    # C_DECOMPRESSION_DETERMINISM: within-state decompressed hash variation = 0
    decomp_variation = {}
    if "DECOMPRESSED-VARYING-BROTLI-CDN" in all_results:
        for ep_key, ep_data in all_results["DECOMPRESSED-VARYING-BROTLI-CDN"].items():
            if "/userinfo" in ep_key:
                for state, hv in ep_data["decompressed_hash_variation"].items():
                    decomp_variation[state] = hv["all_same"]
    c_decomp_det_pass = all(decomp_variation.values()) if decomp_variation else False
    control_details["C_DECOMPRESSION_DETERMINISM"] = {
        "expected": "Within-state decompressed hash variation = 0 for all states under CDN-noise",
        "observed": decomp_variation,
        "pass": c_decomp_det_pass,
    }

    # C_NULL_CONTROL: B-RANDOM ~ 0.0
    b_random_values = []
    for baseline_name in baselines_to_run:
        key = f"/userinfo_{baseline_name}"
        if key in metrics:
            b_random_values.append(metrics[key]["baselines"]["B-RANDOM"])
    c_null_pass = all(v is not None and abs(v) < 0.1 for v in b_random_values) if b_random_values else False
    control_details["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0 at all conditions",
        "observed": [float(v) for v in b_random_values],
        "pass": c_null_pass,
    }

    # C_CDN_NOISE_ACTIVE: compressed-byte hashes vary across requests for same logical body
    cdn_noise_active = {}
    if "DECOMPRESSED-VARYING-BROTLI-CDN" in all_results:
        for ep_key, ep_data in all_results["DECOMPRESSED-VARYING-BROTLI-CDN"].items():
            if "/userinfo" in ep_key:
                for state, hv in ep_data["compressed_hash_variation"].items():
                    cdn_noise_active[state] = hv["unique_count"]
    c_cdn_pass = any(v > 1 for v in cdn_noise_active.values()) if cdn_noise_active else False
    control_details["C_CDN_NOISE_ACTIVE"] = {
        "expected": "Compressed-byte hashes vary across requests for same logical body (CDN noise introduces non-determinism)",
        "observed": cdn_noise_active,
        "pass": c_cdn_pass,
    }

    # C_ALGORITHM_EQUIVALENCE: |B-DECOMPRESSED-VARYING-GZIP(parent) - B-DECOMPRESSED-VARYING-BROTLI-CDN| < 0.1
    if userinfo_decompressed_disc is not None:
        algo_diff = abs(PARENT_DECOMPRESSED_VARYING_GZIP_USERINFO - userinfo_decompressed_disc)
    else:
        algo_diff = None
    c_algo_pass = algo_diff is not None and algo_diff < 0.1
    control_details["C_ALGORITHM_EQUIVALENCE"] = {
        "expected": "|B-DECOMPRESSED-VARYING-GZIP(parent=0.5) - B-DECOMPRESSED-VARYING-BROTLI-CDN| < 0.1",
        "observed": float(algo_diff) if algo_diff is not None else None,
        "pass": c_algo_pass,
    }

    # C_NO_PIPELINE_ERRORS
    c_pipeline_pass = len(errors) == 0
    control_details["C_NO_PIPELINE_ERRORS"] = {
        "expected": "0 errors",
        "observed": len(errors),
        "pass": c_pipeline_pass,
    }

    # =========================================================================
    # DECISION RULE (from frozen spec.json)
    # =========================================================================

    # Condition 1: within-state decompressed hash variation = 0 (positive control)
    c1_pass = c_decomp_det_pass

    # Condition 2: B-RANDOM ~ 0.0 (null control)
    c2_pass = c_null_pass

    # Condition 3: decompressed discrimination >= 0.5 on /userinfo (H1)
    c3_pass = userinfo_decompressed_disc is not None and userinfo_decompressed_disc >= 0.5

    # Condition 4: |parent - CDN| < 0.1 (H2 algorithm equivalence)
    c4_pass = c_algo_pass

    # Condition 5: CDN noise actually introduced non-determinism
    c5_pass = c_cdn_pass

    survives = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass

    algorithm_equivalent = c4_pass

    measurement_invalid = (not c_pipeline_pass) or (not c1_pass) or (not c5_pass)

    # H3: compressed-byte-only CDN discrimination < 0.35 on /userinfo
    h3_falsified = userinfo_compressed_disc is not None and userinfo_compressed_disc < 0.35
    h3_confirmed = userinfo_compressed_disc is not None and userinfo_compressed_disc >= 0.35

    if measurement_invalid:
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif survives:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif c3_pass and not c4_pass:
        # H1 survives but H2 fails: ALGORITHM-DEPENDENT
        outcome = "MIXED"
        status = "COMPLETE"
    elif not c3_pass:
        # H1 fails: FALSIFIED-IN-SETTING
        outcome = "FALSIFIES"
        status = "COMPLETE"
    else:
        outcome = "INCONCLUSIVE"
        status = "COMPLETE"

    # =========================================================================
    # OBSERVATIONS
    # =========================================================================

    observations = [
        f"Mock OAuth2 server on localhost:{MOCK_SERVER_PORT} returning JSON responses",
        f"CDN-noise proxy on localhost:{CDN_PROXY_PORT} with 6 categories of non-determinism",
        f"CDN noise seed: {cdn_noise_seed}, quality seed: {quality_seed}",
        f"Auth states: {AUTH_STATES}",
        f"Reps per state per endpoint: {REPS}",
        f"Endpoints: /userinfo (GET), /introspect (POST)",
        f"Total states x reps x endpoints = {len(AUTH_STATES)} x {REPS} x 2 = {len(AUTH_STATES) * REPS * 2} per baseline",
        f"Actual requests made: {request_count}",
        f"Seed: {SEED}",
        f"Brotli available: {BROTLI_AVAILABLE}",
        f"CDN noise parameters: chunked={CHUNKED_PROB}, gzip_override={GZIP_OVERRIDE_PROB}, "
        f"identity_override={IDENTITY_OVERRIDE_PROB}, cache_hit={CACHE_HIT_PROB}",
        f"Cache stats: hits={CDNNoiseProxyHandler.cache_hits}, misses={CDNNoiseProxyHandler.cache_misses}",
    ]

    for baseline_name in baselines_to_run:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_{baseline_name}"
            if key in metrics:
                observations.append(
                    f"baseline={baseline_name} {ep_name}: "
                    f"compressed={metrics[key]['compressed_body_only_discrimination']:.4f}, "
                    f"decompressed={metrics[key]['decompressed_body_only_discrimination']:.4f}, "
                    f"status={metrics[key]['status_only_discrimination']:.4f}, "
                    f"B-RANDOM={metrics[key]['baselines']['B-RANDOM']:.4f}"
                )

    # Add CDN header observations
    if key_dec in metrics and "cdn_header_verification" in metrics[key_dec]:
        for state in AUTH_STATES:
            cdn_v = metrics[key_dec]["cdn_header_verification"].get(state, {})
            observations.append(
                f"CDN headers {state}: cf_ray_unique={cdn_v.get('cf_ray_unique', '?')}, "
                f"x_cache={cdn_v.get('x_cache_values', '?')}, "
                f"age_range={cdn_v.get('age_range', '?')}, "
                f"via={cdn_v.get('via_values', '?')}"
            )

    # Add encoding distribution observations
    if key_dec in metrics and "compression_verification" in metrics[key_dec]:
        for state in AUTH_STATES:
            cv = metrics[key_dec]["compression_verification"].get(state, {})
            observations.append(
                f"Encoding distribution {state}: {cv.get('content_encoding_values', '?')}"
            )

    # =========================================================================
    # VALIDITY NOTES
    # =========================================================================

    validity_notes = [
        "Mock OAuth2 server (not Keycloak) returning JSON with random data field",
        "Fingerprint algorithm: SHA-256(repr((status, body_sha256, ''))) for compressed and decompressed",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "expired_token is locally-signed HS256, not real expired token",
        f"Brotli module available: {BROTLI_AVAILABLE}",
        "CDN-noise proxy applies 6 categories of non-determinism (per frozen spec section 4)",
        "Category 1: Brotli quality variation {4,5,6,7,8} per request",
        "Category 2: Chunked transfer-encoding (~30% of responses)",
        "Category 3: CDN headers (CF-Ray, X-Cache, Age, Via) vary per request",
        "Category 4: Accept-Encoding override (20% gzip, 5% identity, 75% brotli)",
        "Category 5: Response caching (~30% cache hits)",
        "Category 6: Content-Length variation (passive consequence)",
        f"CDN noise seed derived deterministically: seed + hash('CDN_NOISE') % 10000 = {cdn_noise_seed}",
        "Same mock server as parent: 4 auth states, 3-way error collapse, discrimination ceiling 0.5",
        f"Body size: ~{BODY_SIZE} bytes uncompressed (1KB)",
        f"Seed={SEED} for request ordering (deterministic across runs)",
        "Parent gzip reference data from EXP-RUNTIME-35058619700 (not re-executed)",
        "Effective brotli diversity: 2 variants (q4 distinct vs q5-8 identical for 1KB JSON) per parent audit",
    ]

    if not BROTLI_AVAILABLE:
        validity_notes.append("BROTLI NOT AVAILABLE: Cannot run brotli conditions")

    if errors:
        validity_notes.append(f"Pipeline errors: {len(errors)} requests failed")
        for e in errors[:5]:
            validity_notes.append(f"  Error: {e}")

    # Check CDN noise effectiveness
    if c_cdn_pass:
        validity_notes.append("CDN noise successfully introduced compressed-byte non-determinism")
    else:
        validity_notes.append("CDN noise may not have introduced sufficient compressed-byte variation")

    # Check encoding distribution
    if key_dec in metrics and "compression_verification" in metrics[key_dec]:
        all_encodings = set()
        for state in AUTH_STATES:
            cv = metrics[key_dec]["compression_verification"].get(state, {})
            all_encodings.update(cv.get("content_encoding_values", []))
        validity_notes.append(f"Observed encoding types: {all_encodings}")

    # =========================================================================
    # UNRESOLVED
    # =========================================================================

    unresolved = [
        "Does decompression-normalization survive real CDN infrastructure (Cloudflare/Fastly/Akamai) where per-edge brotli quality, caching, chunked transfer-encoding, and Accept-Encoding negotiation introduce non-determinism not present in this synthetic proxy?",
        "Does result generalize to non-JSON content types (HTML, XML, binary) and to MB-scale?",
        "What is latency cost of per-response brotli decompression before hashing at production scale?",
        "What is behavior when Content-Encoding is missing, incorrect, or double-encoded?",
        "Is the CDN-noise proxy's Accept-Encoding override realistic compared to real CDN negotiation?",
        "Does the in-memory cache model capture real CDN TTL, invalidation, and hierarchical caching behavior?",
        "Does 5-level brotli quality selection produce 5 distinct compressed outputs for larger or incompressible payloads?",
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
            {"path": "raw_observations.json", "role": "raw", "description": "All HTTP observations per baseline per endpoint per state"},
            {"path": "run_experiment.py", "role": "code", "description": "Experiment execution script with CDN-noise proxy"},
        ],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    # Save raw observations
    raw_obs_serializable = {}
    for baseline_name, endpoint_obs in raw_observations_all.items():
        raw_obs_serializable[baseline_name] = {}
        for ep_name, state_obs in endpoint_obs.items():
            raw_obs_serializable[baseline_name][ep_name] = {}
            for state, obs_list in state_obs.items():
                raw_obs_serializable[baseline_name][ep_name][state] = []
                for obs in obs_list:
                    raw_obs_serializable[baseline_name][ep_name][state].append({
                        "url": obs["url"],
                        "status": obs["status"],
                        "headers": obs["headers"],
                        "body_hash_compressed": obs["body_hash_compressed"],
                        "body_size": obs["body_size"],
                        "body_preview": obs["body"][:500].decode("utf-8", errors="replace"),
                        "fingerprint_compressed": obs["fingerprint_compressed"],
                        "fingerprint_decompressed": obs["fingerprint_decompressed"],
                        "fingerprint_status": obs["fingerprint_status"],
                        "content_encoding": obs["content_encoding"],
                        "cdn_headers": obs["cdn_headers"],
                        "baseline": obs["baseline"],
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
