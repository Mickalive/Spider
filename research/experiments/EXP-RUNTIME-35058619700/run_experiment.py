#!/usr/bin/env python3
"""
EXP-RUNTIME-35058619700 - Decompression-Normalization Under Gzip Quality Variation
====================================================================================
Tests whether decompression-normalization (hashing DECOMPRESSED response body after
reversing Content-Encoding) preserves body-only discrimination under varying gzip
quality levels, and whether normalization is algorithm-agnostic (gzip vs brotli).

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

EXPERIMENT_ID = "EXP-RUNTIME-35058619700"
LANE = "runtime"
SEED = 44
REPS = 20
MOCK_SERVER_PORT = 5000
PROXY_PORT = 5001
CLIENT_SECRET = "spider-secret-12345"

USERINFO_PATH = "/userinfo"
INTROSPECT_PATH = "/introspect"

# Gzip quality levels for varying conditions (frozen)
GZIP_QUALITY_RANGE = (1, 3, 5, 7, 9)
FIXED_GZIP_LEVEL = 9

# Brotli quality range for algorithm-equivalence replication (frozen)
BROTLI_QUALITY_RANGE = (4, 8)

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
    return "not-a-real-jwt-token"


# ---------------------------------------------------------------------------
# MOCK OAUTH2 SERVER
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True
    allow_reuse_port = True


class MockOAuth2Handler(BaseHTTPRequestHandler):
    body_size = 1024
    body_seed = 42

    def log_message(self, format, *args):
        pass

    def _generate_body(self, size, seed):
        rng = random.Random(seed)
        return bytes(rng.getrandbits(8) for _ in range(size))

    def _send_json_response(self, status_code, body_bytes, extra_headers=None):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        if extra_headers:
            for key, value in extra_headers.items():
                self.send_header(key, value)
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)

    def _is_valid_token(self, token):
        try:
            payload = jwt.decode(token, CLIENT_SECRET, algorithms=["HS256"])
            exp = payload.get("exp", 0)
            if exp < datetime.now(timezone.utc).timestamp():
                return False
            return True
        except Exception:
            return False

    def do_GET(self):
        if self.path == USERINFO_PATH:
            auth_header = self.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]
                if self._is_valid_token(token):
                    body_data = self._generate_body(self.body_size, self.body_seed)
                    response = json.dumps({"data": body_data.hex()}).encode()
                    self._send_json_response(200, response, {"Cache-Control": "no-cache"})
                    return

            error_body = json.dumps({"error": "invalid_token", "error_description": "Token verification failed"}).encode()
            self._send_json_response(401, error_body, {
                "WWW-Authenticate": 'Bearer realm="spider-test", error="invalid_token", error_description="Token verification failed"'
            })
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == INTROSPECT_PATH:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b""

            params = {}
            if post_data:
                for pair in post_data.decode().split("&"):
                    if "=" in pair:
                        key, value = pair.split("=", 1)
                        params[key] = value

            token = params.get("token", "")
            if token and token != "":
                if self._is_valid_token(token):
                    body_data = self._generate_body(self.body_size, self.body_seed)
                    response = json.dumps({"active": True, "data": body_data.hex()}).encode()
                    self._send_json_response(200, response)
                    return

            response = json.dumps({"active": False}).encode()
            self._send_json_response(200, response)
        else:
            self.send_error(404, "Not Found")


def start_mock_server(body_size, body_seed):
    MockOAuth2Handler.body_size = body_size
    MockOAuth2Handler.body_seed = body_seed
    server = ReusableHTTPServer(("127.0.0.1", MOCK_SERVER_PORT), MockOAuth2Handler)
    server.timeout = 0.5
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Mock server started on port {MOCK_SERVER_PORT} with body_size={body_size}, seed={body_seed}")
    return server


def stop_mock_server(server):
    if server:
        server.shutdown()
        print("Mock server stopped.")


# ---------------------------------------------------------------------------
# COMPRESSION / DECOMPRESSION FUNCTIONS
# ---------------------------------------------------------------------------

def compress_gzip(data, level=9):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=level, mtime=0) as f:
        f.write(data)
    return buf.getvalue()


def decompress_gzip(data):
    return gzip.decompress(data)


def compress_brotli(data, quality=6):
    return brotli.compress(data, quality=quality)


def decompress_brotli(data):
    return brotli.decompress(data)


# ---------------------------------------------------------------------------
# PROXY WITH CONDITION-BASED COMPRESSION
# ---------------------------------------------------------------------------

class ConditionProxyHandler(BaseHTTPRequestHandler):
    condition = "COMPRESSED-FIXED-GZIP"
    quality_rng = None  # set per-condition

    def log_message(self, format, *args):
        pass

    def _get_gzip_level(self):
        if self.condition in ("COMPRESSED-VARYING-GZIP", "DECOMPRESSED-VARYING-GZIP"):
            idx = self.quality_rng.randint(0, len(GZIP_QUALITY_RANGE) - 1)
            return GZIP_QUALITY_RANGE[idx]
        return FIXED_GZIP_LEVEL

    def _get_brotli_quality(self):
        if self.condition in ("DECOMPRESSED-VARYING-BROTLI",):
            idx = self.quality_rng.randint(0, len(BROTLI_QUALITY_RANGE) - 1)
            return BROTLI_QUALITY_RANGE[idx]
        return 6

    def do_request(self):
        target_url = f"http://127.0.0.1:{MOCK_SERVER_PORT}{self.path}"

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        headers = {}
        for key in self.headers:
            if key.lower() not in ("host", "transfer-encoding"):
                headers[key] = self.headers[key]
        headers["Accept-Encoding"] = "identity"  # Get raw response from mock server

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

        if self.condition == "IDENTITY":
            compressed_body = raw_body
            encoding = None
        elif self.condition in ("COMPRESSED-FIXED-GZIP", "COMPRESSED-VARYING-GZIP",
                                "DECOMPRESSED-FIXED-GZIP", "DECOMPRESSED-VARYING-GZIP"):
            level = self._get_gzip_level()
            compressed_body = compress_gzip(raw_body, level=level)
            encoding = "gzip"
        elif self.condition == "DECOMPRESSED-VARYING-BROTLI":
            quality = self._get_brotli_quality()
            compressed_body = compress_brotli(raw_body, quality=quality)
            encoding = "br"
        else:
            compressed_body = raw_body
            encoding = None

        self.send_response(resp.status_code)
        for key, value in resp.headers.items():
            key_lower = key.lower()
            if key_lower in ("transfer-encoding", "content-encoding", "content-length", "connection"):
                continue
            self.send_header(key, value)

        if encoding:
            self.send_header("Content-Encoding", encoding)
        self.send_header("Content-Length", str(len(compressed_body)))
        self.end_headers()
        self.wfile.write(compressed_body)

    def do_GET(self):
        self.do_request()

    def do_POST(self):
        self.do_request()


def start_proxy(condition, quality_rng):
    ConditionProxyHandler.condition = condition
    ConditionProxyHandler.quality_rng = quality_rng
    server = ReusableHTTPServer(("127.0.0.1", PROXY_PORT), ConditionProxyHandler)
    server.timeout = 0.5
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Proxy started on port {PROXY_PORT} with condition='{condition}'")
    return server


def stop_proxy(server):
    if server:
        server.shutdown()
        print("Proxy stopped.")


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
    """Hash the compressed body bytes (raw wire bytes)."""
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
    vector = (observation["status"], body_hash, '')
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


def fingerprint_decompressed(observation):
    """Decompress via Content-Encoding, then hash the decompressed body."""
    ce = observation["headers"].get("Content-Encoding", "")
    raw_body = observation["body"]
    if ce == "br":
        try:
            decompressed = brotli.decompress(raw_body)
        except Exception:
            decompressed = raw_body
    elif ce == "gzip":
        try:
            decompressed = gzip.decompress(raw_body)
        except Exception:
            decompressed = raw_body
    else:
        decompressed = raw_body
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
    """Discrimination = intra_match_rate - inter_match_rate."""
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
# CONDITIONS (frozen from spec.json)
# ---------------------------------------------------------------------------

CONDITIONS = [
    "COMPRESSED-FIXED-GZIP",
    "COMPRESSED-VARYING-GZIP",
    "DECOMPRESSED-FIXED-GZIP",
    "DECOMPRESSED-VARYING-GZIP",
    "DECOMPRESSED-VARYING-BROTLI",
]

AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]


# ---------------------------------------------------------------------------
# MAIN EXPERIMENT
# ---------------------------------------------------------------------------

def run_experiment():
    raw_observations_all = {}
    all_results = {}
    errors = []
    request_count = 0

    print(f"Experiment: {EXPERIMENT_ID}")
    print(f"Conditions: {CONDITIONS}")
    print(f"Auth states: {AUTH_STATES}")
    print(f"Reps per state: {REPS}")
    print(f"Seed: {SEED}")
    print(f"Gzip quality range for varying: {GZIP_QUALITY_RANGE}")
    print(f"Fixed gzip level: {FIXED_GZIP_LEVEL}")
    print(f"Brotli quality range for varying: {BROTLI_QUALITY_RANGE}")
    print()

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated. Length: {len(auth_token)}")

    # Body size: ~1KB uncompressed (matching parent)
    BODY_SIZE = 1024

    for condition in CONDITIONS:
        print(f"\n{'='*70}")
        print(f"CONDITION: {condition}")
        print(f"{'='*70}")

        # Per-condition RNG for quality variation (seeded for reproducibility)
        quality_rng = random.Random(SEED + hash(condition) % 10000)

        mock_server = start_mock_server(BODY_SIZE, SEED)
        time.sleep(0.5)

        # Verify mock server
        try:
            test_resp = requests.get(f"http://127.0.0.1:{MOCK_SERVER_PORT}{USERINFO_PATH}",
                                     headers={"Authorization": f"Bearer {auth_token}"},
                                     timeout=5)
            print(f"  Mock server test: status={test_resp.status_code}, body_size={len(test_resp.content)}")
        except Exception as e:
            print(f"  WARNING: Mock server test failed: {e}")

        proxy = start_proxy(condition, quality_rng)
        time.sleep(0.5)

        endpoints = get_endpoint_configs(auth_token, PROXY_PORT)

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
                    obs["condition"] = condition
                    obs["fingerprint_compressed"] = fingerprint_compressed_only(obs)
                    obs["fingerprint_decompressed"] = fingerprint_decompressed(obs)
                    obs["fingerprint_status"] = fingerprint_status_only(obs)
                    obs["body_hash_compressed"] = hashlib.sha256(obs["body"]).hexdigest()
                    obs["body_size"] = len(obs["body"])

                    # Extract Content-Encoding
                    ce = obs["headers"].get("Content-Encoding", "none")
                    obs["content_encoding"] = ce

                    raw_observations[state].append(obs)
                    fingerprints_compressed_by_state[state].append(obs["fingerprint_compressed"])
                    fingerprints_decompressed_by_state[state].append(obs["fingerprint_decompressed"])
                    fingerprints_status_by_state[state].append(obs["fingerprint_status"])
                    request_count += 1
                except Exception as e:
                    errors.append({"condition": condition, "endpoint": ep_name,
                                   "state": state, "rep": rep, "error": str(e)})

                if i < len(plan) - 1:
                    jitter = rng.uniform(0.05, 0.15)
                    time.sleep(jitter)

            # Compute discrimination scores
            compressed_disc = compute_discrimination_score(fingerprints_compressed_by_state)
            decompressed_disc = compute_discrimination_score(fingerprints_decompressed_by_state)
            status_disc = compute_discrimination_score(fingerprints_status_by_state)

            # Random baseline
            b_rand_fps = baseline_random(n=REPS * len(AUTH_STATES))
            b_rand_by_state = {}
            idx = 0
            for s in AUTH_STATES:
                b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
                idx += REPS
            b_rand_disc = compute_discrimination_score(b_rand_by_state)

            # Within-state variation (compressed)
            compressed_hash_variation = {}
            for state, obs_list in raw_observations.items():
                hashes = [obs["body_hash_compressed"] for obs in obs_list]
                compressed_hash_variation[state] = {
                    "unique_count": len(set(hashes)),
                    "total": len(hashes),
                    "all_same": len(set(hashes)) == 1,
                }

            # Within-state variation (decompressed)
            decompressed_hash_variation = {}
            for state, obs_list in raw_observations.items():
                decompressed_hashes = []
                for obs in obs_list:
                    ce = obs["headers"].get("Content-Encoding", "")
                    raw_body = obs["body"]
                    if ce == "br":
                        try:
                            dec = brotli.decompress(raw_body)
                        except Exception:
                            dec = raw_body
                    elif ce == "gzip":
                        try:
                            dec = gzip.decompress(raw_body)
                        except Exception:
                            dec = raw_body
                    else:
                        dec = raw_body
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

            ep_key = f"{ep_name}_{condition}"
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

        raw_observations_all[condition] = condition_raw_obs
        all_results[condition] = condition_results

        stop_proxy(proxy)
        time.sleep(1.0)

        stop_mock_server(mock_server)
        time.sleep(1.0)

    # =========================================================================
    # ASSEMBLE METRICS
    # =========================================================================

    metrics = {}
    for condition in CONDITIONS:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_{condition}"
            if condition in all_results and key in all_results[condition]:
                metrics[key] = all_results[condition][key]

    # Primary metric: /userinfo discrimination per condition
    userinfo_compressed_discs = {}
    userinfo_decompressed_discs = {}
    for condition in CONDITIONS:
        key = f"/userinfo_{condition}"
        if key in metrics:
            userinfo_compressed_discs[condition] = metrics[key]["compressed_body_only_discrimination"]
            userinfo_decompressed_discs[condition] = metrics[key]["decompressed_body_only_discrimination"]

    # =========================================================================
    # CONTROLS
    # =========================================================================

    control_details = {}

    # C_POSITIVE_CONTROL: B-COMPRESSED-FIXED-GZIP >= 0.35 on /userinfo
    b_compressed_fixed_gzip = userinfo_compressed_discs.get("COMPRESSED-FIXED-GZIP", None)
    c1_pass = b_compressed_fixed_gzip is not None and b_compressed_fixed_gzip >= 0.35
    control_details["C_POSITIVE_CONTROL"] = {
        "expected": "B-COMPRESSED-FIXED-GZIP >= 0.35 on /userinfo (replicates EXP-RUNTIME-34741873198 deterministic gzip)",
        "observed": float(b_compressed_fixed_gzip) if b_compressed_fixed_gzip is not None else None,
        "pass": c1_pass,
    }

    # C_NULL_CONTROL: B-RANDOM ~ 0.0 at all conditions
    b_random_all = []
    for condition in CONDITIONS:
        key = f"/userinfo_{condition}"
        if key in metrics:
            b_random_all.append(metrics[key]["baselines"]["B-RANDOM"])
    c2_pass = all(v is not None and abs(v) < 0.1 for v in b_random_all) if b_random_all else False
    control_details["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0 at all conditions",
        "observed": [float(v) for v in b_random_all],
        "pass": c2_pass,
    }

    # C_DECOMPRESSED_FIXED_PRESERVES: B-DECOMPRESSED-FIXED-GZIP >= 0.5 on /userinfo
    b_decompressed_fixed_gzip = userinfo_decompressed_discs.get("DECOMPRESSED-FIXED-GZIP", None)
    c3_pass = b_decompressed_fixed_gzip is not None and b_decompressed_fixed_gzip >= 0.5
    control_details["C_DECOMPRESSED_FIXED_PRESERVES"] = {
        "expected": "B-DECOMPRESSED-FIXED-GZIP >= 0.5 on /userinfo (decompression-normalization preserves discrimination under fixed gzip)",
        "observed": float(b_decompressed_fixed_gzip) if b_decompressed_fixed_gzip is not None else None,
        "pass": c3_pass,
    }

    # C_DECOMPRESSION_DETERMINISM: within-state decompressed hash variation = 0 for DECOMPRESSED-FIXED-GZIP
    decomp_fixed_variation = {}
    if "DECOMPRESSED-FIXED-GZIP" in all_results:
        for ep_key, ep_data in all_results["DECOMPRESSED-FIXED-GZIP"].items():
            if "/userinfo" in ep_key:
                for state, hv in ep_data["decompressed_hash_variation"].items():
                    decomp_fixed_variation[state] = hv["all_same"]
    c4_pass = all(decomp_fixed_variation.values()) if decomp_fixed_variation else False
    control_details["C_DECOMPRESSION_DETERMINISM"] = {
        "expected": "Within-state decompressed hash variation = 0 for DECOMPRESSED-FIXED-GZIP (gzip decompression is deterministic with mtime=0)",
        "observed": decomp_fixed_variation,
        "pass": c4_pass,
    }

    # C_QUALITY_VARIATION_ACTIVE: within-state compressed hash variation > 0 for COMPRESSED-VARYING-GZIP
    compressed_varying_variation = {}
    if "COMPRESSED-VARYING-GZIP" in all_results:
        for ep_key, ep_data in all_results["COMPRESSED-VARYING-GZIP"].items():
            if "/userinfo" in ep_key:
                for state, hv in ep_data["compressed_hash_variation"].items():
                    compressed_varying_variation[state] = hv["unique_count"]
    c5_pass = all(v > 1 for v in compressed_varying_variation.values()) if compressed_varying_variation else False
    control_details["C_QUALITY_VARIATION_ACTIVE"] = {
        "expected": "Within-state compressed hash variation > 0 for COMPRESSED-VARYING-GZIP (quality levels produce different compressed bytes)",
        "observed": compressed_varying_variation,
        "pass": c5_pass,
    }

    # C_NO_PIPELINE_ERRORS
    c6_pass = len(errors) == 0
    control_details["C_NO_PIPELINE_ERRORS"] = {
        "expected": "0 errors",
        "observed": len(errors),
        "pass": c6_pass,
    }

    # C_ALGORITHM_EQUIVALENCE: |B-DECOMPRESSED-VARYING-GZIP - B-DECOMPRESSED-VARYING-BROTLI| < 0.1
    b_decomp_varying_gzip = userinfo_decompressed_discs.get("DECOMPRESSED-VARYING-GZIP", None)
    b_decomp_varying_brotli = userinfo_decompressed_discs.get("DECOMPRESSED-VARYING-BROTLI", None)
    if b_decomp_varying_gzip is not None and b_decomp_varying_brotli is not None:
        algo_diff = abs(b_decomp_varying_gzip - b_decomp_varying_brotli)
    else:
        algo_diff = None
    c7_pass = algo_diff is not None and algo_diff < 0.1
    control_details["C_ALGORITHM_EQUIVALENCE"] = {
        "expected": "|B-DECOMPRESSED-VARYING-GZIP - B-DECOMPRESSED-VARYING-BROTLI| < 0.1 (algorithm-agnostic normalization)",
        "observed": float(algo_diff) if algo_diff is not None else None,
        "pass": c7_pass,
    }

    all_controls_pass = all(c["pass"] for c in control_details.values())

    # =========================================================================
    # DECISION RULE (from frozen spec.json)
    # =========================================================================

    # SURVIVES_CURRENT_TEST if ALL of:
    # (1) B-COMPRESSED-FIXED-GZIP >= 0.35 on /userinfo (positive control passes)
    # (2) B-RANDOM ~ 0.0 at all conditions (null control passes)
    # (3) B-DECOMPRESSED-FIXED-GZIP >= 0.5 on /userinfo (decompression-normalization preserves)
    survives = c1_pass and c2_pass and c3_pass and c6_pass

    # MIXED if B-DECOMPRESSED-FIXED-GZIP >= 0.5 BUT B-COMPRESSED-VARYING-GZIP < 0.35
    b_compressed_varying_gzip = userinfo_compressed_discs.get("COMPRESSED-VARYING-GZIP", None)
    mixed = (c3_pass and b_compressed_varying_gzip is not None and b_compressed_varying_gzip < 0.35)

    # FALSIFIED-IN-SETTING if B-DECOMPRESSED-FIXED-GZIP < 0.35
    falsified_in_setting = (b_decompressed_fixed_gzip is not None and b_decompressed_fixed_gzip < 0.35)

    # ALGORITHM-EQUIVALENT (advisory, not a verdict)
    algorithm_equivalent = c7_pass

    # MEASUREMENT_INVALID if pipeline errors or within-state variation > 0 for DECOMPRESSED-FIXED-GZIP
    measurement_invalid = (not c6_pass) or (not c4_pass)

    if measurement_invalid:
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif mixed:
        outcome = "MIXED"
        status = "COMPLETE"
    elif survives:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif falsified_in_setting:
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
        f"CDN proxy on localhost:{PROXY_PORT} with condition-based compression",
        f"Conditions: {CONDITIONS}",
        f"Auth states: {AUTH_STATES}",
        f"Reps per state per condition per endpoint: {REPS}",
        f"Endpoints: /userinfo (GET), /introspect (POST)",
        f"Total conditions x states x reps x endpoints = {len(CONDITIONS)} x {len(AUTH_STATES)} x {REPS} x 2 = {len(CONDITIONS) * len(AUTH_STATES) * REPS * 2}",
        f"Actual requests made: {request_count}",
        f"Seed: {SEED}",
        f"Brotli available: {BROTLI_AVAILABLE}",
        f"Gzip quality range for varying: {GZIP_QUALITY_RANGE}",
        f"Fixed gzip level: {FIXED_GZIP_LEVEL}",
        f"Brotli quality range for varying: {BROTLI_QUALITY_RANGE}",
    ]

    for condition in CONDITIONS:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_{condition}"
            if key in metrics:
                observations.append(
                    f"condition={condition} {ep_name}: "
                    f"compressed={metrics[key]['compressed_body_only_discrimination']:.4f}, "
                    f"decompressed={metrics[key]['decompressed_body_only_discrimination']:.4f}, "
                    f"status={metrics[key]['status_only_discrimination']:.4f}, "
                    f"B-RANDOM={metrics[key]['baselines']['B-RANDOM']:.4f}"
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
        "Proxy compresses all responses with gzip or brotli depending on condition",
        "Gzip quality variation uses random.randint with per-condition seed derived from SEED",
        "Gzip uses mtime=0 to eliminate timestamp non-determinism",
        "Brotli quality variation uses random.randint(4,8) with per-condition seed",
        "Decompression via gzip.decompress() after Content-Encoding 'gzip' removal",
        "Decompression via brotli.decompress() after Content-Encoding 'br' removal",
        "Same mock server as parent (EXP-RUNTIME-34986155186): 4 auth states, 3-way error collapse, discrimination ceiling 0.5",
        f"Body size: ~{BODY_SIZE} bytes uncompressed (1KB)",
        f"Seed={SEED} for request ordering and quality variation (deterministic across runs)",
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
        "Does decompression-normalization survive real CDN infrastructure with non-deterministic compression?",
        "Does result generalize to non-JSON content types (HTML, XML, binary) and to MB-scale?",
        "What is latency cost of per-response gzip/brotli decompression before hashing at production scale?",
        "What is behavior when Content-Encoding is missing, incorrect, or double-encoded?",
        "Is compressed-varying threshold <0.35 robust across seeds and body sizes?",
        "Does 2-unique-hashes vs 5-level quality range indicate saturation or would wider range produce larger degradation?",
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
            {"path": "raw_observations.json", "role": "raw", "description": "All HTTP observations per condition per endpoint per state"},
            {"path": "run_experiment.py", "role": "code", "description": "Frozen experiment execution script"},
        ],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    # Save raw observations
    raw_obs_serializable = {}
    for condition, endpoint_obs in raw_observations_all.items():
        raw_obs_serializable[condition] = {}
        for ep_name, state_obs in endpoint_obs.items():
            raw_obs_serializable[condition][ep_name] = {}
            for state, obs_list in state_obs.items():
                raw_obs_serializable[condition][ep_name][state] = []
                for obs in obs_list:
                    raw_obs_serializable[condition][ep_name][state].append({
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
                        "condition": obs["condition"],
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
        result = build_blocked_result(str(e))

    with open("result.json", "w") as f:
        json.dump(result, f, indent=2, cls=NumpyEncoder)
    print(f"\nResult written to result.json")
    print(f"Status: {result['status']}, Outcome: {result['outcome']}")
