#!/usr/bin/env python3
"""
EXP-RUNTIME-34902094115 - Body-Only Fingerprint Under Deterministic CDN Compression at KB-Scale
================================================================================================
Tests whether body-only HTTP fingerprint discrimination survives deterministic CDN
compression when response body sizes increase from 0-729 bytes to KB-scale JSON
(1KB, 10KB, 100KB).

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

EXPERIMENT_ID = "EXP-RUNTIME-34902094115"
LANE = "runtime"
SEED = 44
REPS = 10
MOCK_SERVER_PORT = 5000
PROXY_PORT = 5001
CLIENT_SECRET = "spider-secret-12345"

EXCLUDED_HEADERS = {"date", "server", "x-request-id"}

BODY_SIZES = {
    "1KB": 1024,
    "10KB": 10240,
    "100KB": 102400,
}

CLIENT_PROFILES = {
    "A_br_gzip": {
        "accept_encoding": "br, gzip",
        "selected_algorithm": "br",
        "description": "Client A: Accept-Encoding 'br, gzip' -> CDN selects brotli",
    },
    "B_gzip_only": {
        "accept_encoding": "gzip",
        "selected_algorithm": "gzip",
        "description": "Client B: Accept-Encoding 'gzip' -> CDN selects gzip",
    },
    "C_identity": {
        "accept_encoding": "identity",
        "selected_algorithm": "identity",
        "description": "Client C: Accept-Encoding 'identity' -> CDN selects identity",
    },
}

AUTH_RELATED_HEADERS = {"cache-control", "www-authenticate", "set-cookie", "content-type"}

USERINFO_PATH = "/userinfo"
INTROSPECT_PATH = "/introspect"

BROTLI_AVAILABLE = True
try:
    import brotli as _brotli_test
except ImportError:
    BROTLI_AVAILABLE = False
    print("WARNING: brotli module not available. Client A will fallback to gzip.")


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
        """Check if token is a valid JWT with exp in the future."""
        try:
            payload = jwt.decode(token, CLIENT_SECRET, algorithms=["HS256"])
            # Check expiry
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
# COMPRESSION FUNCTIONS
# ---------------------------------------------------------------------------

def compress_gzip(data, level):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=level, mtime=0) as f:
        f.write(data)
    return buf.getvalue()


def compress_brotli(data, level=6):
    return brotli.compress(data, quality=level)


def select_algorithm_for_client(client_accept_encoding):
    accept_lower = client_accept_encoding.lower()
    if "br" in accept_lower:
        if BROTLI_AVAILABLE:
            return "br"
        else:
            return "gzip"
    elif "gzip" in accept_lower:
        return "gzip"
    else:
        return "identity"


def compress_for_client(body_bytes, algorithm):
    if algorithm == "br":
        return compress_brotli(body_bytes), "br"
    elif algorithm == "gzip":
        return compress_gzip(body_bytes, 9), "gzip"
    else:
        return body_bytes, None


# ---------------------------------------------------------------------------
# REVERSE PROXY WITH CDN NEGOTIATION
# ---------------------------------------------------------------------------

class CDNNegotiationProxyHandler(BaseHTTPRequestHandler):
    client_accept_encoding = "br, gzip"

    def log_message(self, format, *args):
        pass

    def do_request(self):
        target_url = f"http://127.0.0.1:{MOCK_SERVER_PORT}{self.path}"

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        headers = {}
        for key in self.headers:
            if key.lower() not in ("host", "transfer-encoding"):
                headers[key] = self.headers[key]

        headers["Accept-Encoding"] = "identity"

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
        algorithm = select_algorithm_for_client(self.client_accept_encoding)
        compressed_body, encoding = compress_for_client(raw_body, algorithm)

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


def start_proxy(client_accept_encoding):
    CDNNegotiationProxyHandler.client_accept_encoding = client_accept_encoding

    server = ReusableHTTPServer(("127.0.0.1", PROXY_PORT), CDNNegotiationProxyHandler)
    server.timeout = 0.5

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    algorithm = select_algorithm_for_client(client_accept_encoding)
    print(f"Proxy started on port {PROXY_PORT} with Accept-Encoding='{client_accept_encoding}' -> algorithm={algorithm}")
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
# FINGERPRINT
# ---------------------------------------------------------------------------

def fingerprint_body_only(observation):
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
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

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated. Length: {len(auth_token)}")

    auth_states = ["no_auth", "valid_token", "expired_token", "invalid_token"]

    for size_name, size_bytes in BODY_SIZES.items():
        print(f"\n{'='*70}")
        print(f"BODY SIZE: {size_name} ({size_bytes} bytes)")
        print(f"{'='*70}")

        mock_server = start_mock_server(size_bytes, SEED)
        time.sleep(0.5)

        try:
            test_resp = requests.get(f"http://127.0.0.1:{MOCK_SERVER_PORT}{USERINFO_PATH}",
                                    headers={"Authorization": f"Bearer {auth_token}"},
                                    timeout=5)
            print(f"  Mock server test: status={test_resp.status_code}, body_size={len(test_resp.content)}")
        except Exception as e:
            print(f"  WARNING: Mock server test failed: {e}")

        size_results = {}
        size_raw_obs = {}

        for profile_name, profile_config in CLIENT_PROFILES.items():
            print(f"\n  CLIENT PROFILE: {profile_config['description']}")
            print(f"    Accept-Encoding: {profile_config['accept_encoding']}")
            print(f"    Expected algorithm: {profile_config['selected_algorithm']}")

            proxy = start_proxy(profile_config["accept_encoding"])
            time.sleep(0.5)

            endpoints = get_endpoint_configs(auth_token, PROXY_PORT)

            profile_results = {}
            profile_raw_obs = {}

            for ep in endpoints:
                ep_name = ep["name"]
                print(f"\n    Endpoint: {ep_name}")

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
                                           auth_header=auth_header, body=body)
                        obs["state"] = state
                        obs["rep"] = rep
                        obs["fingerprint_body"] = fingerprint_body_only(obs)
                        obs["fingerprint_status"] = fingerprint_status_only(obs)
                        obs["body_hash"] = hashlib.sha256(obs["body"]).hexdigest()
                        obs["body_size"] = len(obs["body"])
                        obs["client_profile"] = profile_name
                        obs["accept_encoding"] = profile_config["accept_encoding"]
                        raw_observations[state].append(obs)
                        fingerprints_body_by_state[state].append(obs["fingerprint_body"])
                        fingerprints_status_by_state[state].append(obs["fingerprint_status"])
                    except Exception as e:
                        errors.append({"client_profile": profile_name, "endpoint": ep_name,
                                       "state": state, "rep": rep, "error": str(e)})

                    if i < len(plan) - 1:
                        jitter = rng.uniform(0.05, 0.15)
                        time.sleep(jitter)

                body_disc = compute_discrimination_score(fingerprints_body_by_state)
                status_disc = compute_discrimination_score(fingerprints_status_by_state)

                b_rand_fps = baseline_random(n=REPS * len(auth_states))
                b_rand_by_state = {}
                idx = 0
                for s in auth_states:
                    b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
                    idx += REPS
                b_rand_disc = compute_discrimination_score(b_rand_by_state)

                body_hash_variation = {}
                for state, obs_list in raw_observations.items():
                    hashes = [obs["body_hash"] for obs in obs_list]
                    body_hash_variation[state] = {
                        "unique_count": len(set(hashes)),
                        "total": len(hashes),
                        "all_same": len(set(hashes)) == 1,
                    }

                compression_verification = {}
                for state, obs_list in raw_observations.items():
                    ce_headers = [obs["headers"].get("Content-Encoding", "none") for obs in obs_list]
                    compression_verification[state] = {
                        "content_encoding_values": list(set(ce_headers)),
                        "count": len(ce_headers),
                    }

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

                for state in auth_states:
                    hv = body_hash_variation[state]
                    print(f"    {state}: unique_hashes={hv['unique_count']}/{hv['total']}, "
                          f"all_same={hv['all_same']}")

            raw_observations_all[f"{size_name}_{profile_name}"] = profile_raw_obs
            all_results[f"{size_name}_{profile_name}"] = profile_results

            stop_proxy(proxy)
            time.sleep(1.0)

        stop_mock_server(mock_server)
        time.sleep(1.0)

        all_results[size_name] = size_results
        raw_observations_all[size_name] = size_raw_obs

    # Assemble metrics per body size
    metrics = {}
    for size_name in BODY_SIZES:
        for profile_name in CLIENT_PROFILES:
            for ep_name in ["/userinfo", "/introspect"]:
                key = f"{ep_name}_{profile_name}"
                composite_key = f"{size_name}_{profile_name}"
                if composite_key in all_results and key in all_results[composite_key]:
                    metrics_key = f"{size_name}_{key}"
                    metrics[metrics_key] = all_results[composite_key][key]

    # Compute primary derived metrics for /userinfo per body size
    userinfo_bo_discs = {}
    for size_name in BODY_SIZES:
        userinfo_bo_discs[size_name] = {}
        for profile_name in CLIENT_PROFILES:
            metrics_key = f"{size_name}_/userinfo_{profile_name}"
            if metrics_key in metrics:
                userinfo_bo_discs[size_name][profile_name] = metrics[metrics_key]["body_only_discrimination"]

    # Per-size controls
    all_controls_pass = True
    control_details = {}

    for size_name in BODY_SIZES:
        disc = userinfo_bo_discs.get(size_name, {})
        identity_body_only = disc.get("C_identity", None)
        br_body_only = disc.get("A_br_gzip", None)
        gzip_body_only = disc.get("B_gzip_only", None)

        # B-RANDOM
        rand_key = f"{size_name}_/userinfo_C_identity"
        b_random_disc = metrics.get(rand_key, {}).get("baselines", {}).get("B-RANDOM", None)

        # Status-only
        status_discs = {}
        for profile_name in CLIENT_PROFILES:
            mk = f"{size_name}_/userinfo_{profile_name}"
            if mk in metrics:
                status_discs[profile_name] = metrics[mk]["status_only_discrimination"]

        # Within-state variation
        within_state_variation = {}
        for profile_name in CLIENT_PROFILES:
            mk = f"{size_name}_/userinfo_{profile_name}"
            if mk in metrics:
                hv = metrics[mk]["body_hash_variation"]
                total_unique = sum(v["unique_count"] for v in hv.values())
                total_requests = sum(v["total"] for v in hv.values())
                all_same = all(v["all_same"] for v in hv.values())
                within_state_variation[profile_name] = {
                    "total_unique_hashes": total_unique,
                    "total_requests": total_requests,
                    "all_states_deterministic": all_same,
                    "per_state": hv,
                }

        # Cross-client divergence
        cross_client_divergence = {}
        if f"{size_name}_A_br_gzip" in raw_observations_all and f"{size_name}_C_identity" in raw_observations_all:
            for state in auth_states:
                hashes_a = [obs["body_hash"] for obs in
                           raw_observations_all.get(f"{size_name}_A_br_gzip", {}).get("/userinfo", {}).get(state, [])]
                hashes_c = [obs["body_hash"] for obs in
                           raw_observations_all.get(f"{size_name}_C_identity", {}).get("/userinfo", {}).get(state, [])]
                if hashes_a and hashes_c:
                    all_a = set(hashes_a)
                    all_c = set(hashes_c)
                    divergent = len(all_a - all_c) > 0 or len(all_c - all_a) > 0
                    cross_client_divergence[state] = {
                        "divergent": divergent,
                        "unique_hashes_a": len(all_a),
                        "unique_hashes_c": len(all_c),
                    }
                else:
                    cross_client_divergence[state] = {"divergent": None, "unique_hashes_a": 0, "unique_hashes_c": 0}

        # Mixed-client discrimination
        mixed_client_body_disc = None
        if f"{size_name}_A_br_gzip" in raw_observations_all and f"{size_name}_C_identity" in raw_observations_all:
            mixed_fps_by_state = defaultdict(list)
            for state in auth_states:
                fps_a = [obs["fingerprint_body"] for obs in
                        raw_observations_all.get(f"{size_name}_A_br_gzip", {}).get("/userinfo", {}).get(state, [])]
                fps_c = [obs["fingerprint_body"] for obs in
                        raw_observations_all.get(f"{size_name}_C_identity", {}).get("/userinfo", {}).get(state, [])]
                mixed_fps_by_state[state] = fps_a + fps_c
            mixed_client_body_disc = compute_discrimination_score(mixed_fps_by_state)

        # Store derived metrics
        prefix = size_name
        metrics[f"{prefix}_M_DETERMINISTIC_DISCRIMINATION"] = {
            "identity_body_only": float(identity_body_only) if identity_body_only is not None else None,
            "br_body_only": float(br_body_only) if br_body_only is not None else None,
            "gzip_body_only": float(gzip_body_only) if gzip_body_only is not None else None,
            "description": f"Body-only discrimination under deterministic brotli and gzip on /userinfo ({size_name})"
        }
        metrics[f"{prefix}_M_IDENTITY_CONTROL"] = {
            "value": float(identity_body_only) if identity_body_only is not None else None,
            "threshold": 0.35,
            "description": f"B-IDENTITY-BODY-ONLY: body-only discrimination at identity on /userinfo ({size_name})"
        }
        metrics[f"{prefix}_M_NULL_CONTROL"] = {
            "value": float(b_random_disc) if b_random_disc is not None else None,
            "threshold": "~0.0",
            "description": f"B-RANDOM discrimination at all client profiles ({size_name})"
        }
        metrics[f"{prefix}_M_DETERMINISTIC_BR_CONTROL"] = {
            "value": float(br_body_only) if br_body_only is not None else None,
            "threshold": ">= identity - 0.15",
            "description": f"B-DETERMINISTIC-BR-BODY-ONLY ({size_name})"
        }
        metrics[f"{prefix}_M_DETERMINISTIC_GZIP_CONTROL"] = {
            "value": float(gzip_body_only) if gzip_body_only is not None else None,
            "threshold": ">= identity - 0.15",
            "description": f"B-DETERMINISTIC-GZIP-BODY-ONLY ({size_name})"
        }
        metrics[f"{prefix}_M_CROSS_CLIENT_DIVERGENCE"] = {
            "divergence": cross_client_divergence,
            "description": f"Cross-client body hash divergence ({size_name})"
        }
        metrics[f"{prefix}_M_MIXED_CLIENT_DISCRIMINATION"] = {
            "value": float(mixed_client_body_disc) if mixed_client_body_disc is not None else None,
            "threshold": "< identity body-only",
            "description": f"B-MIXED-CLIENT-BODY-ONLY ({size_name})"
        }
        metrics[f"{prefix}_M_STATUS_ONLY_INVARIANCE"] = {
            "values": {k: float(v) for k, v in status_discs.items()},
            "threshold": "~ 0.5 on /userinfo invariant",
            "description": f"B-STATUS-ONLY ({size_name})"
        }
        metrics[f"{prefix}_M_WITHIN_STATE_VARIATION"] = within_state_variation

        # C1: Positive control
        c1_pass = identity_body_only is not None and identity_body_only >= 0.35
        # C2: Null control
        c2_pass = b_random_disc is not None and abs(b_random_disc) < 0.1
        # C3: Deterministic brotli preserves
        c3_pass = (br_body_only is not None and identity_body_only is not None
                   and br_body_only >= identity_body_only - 0.15)
        # C4: Deterministic gzip preserves
        c4_pass = (gzip_body_only is not None and identity_body_only is not None
                   and gzip_body_only >= identity_body_only - 0.15)
        # C5: Within-state deterministic
        c5_pass = True
        for profile_name in ["A_br_gzip", "B_gzip_only"]:
            if profile_name in within_state_variation:
                if not within_state_variation[profile_name]["all_states_deterministic"]:
                    c5_pass = False
        # C6: Mixed-client degrades
        c6_pass = (mixed_client_body_disc is not None and identity_body_only is not None
                   and mixed_client_body_disc < identity_body_only)
        # C7: Status-only invariant
        c7_pass = all(v >= 0.5 for v in status_discs.values()) if status_discs else False
        # C8: No pipeline errors (per-size, use global count)
        c8_pass = len(errors) == 0

        size_pass = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass and c6_pass and c7_pass and c8_pass

        control_details[f"{size_name}_C_POSITIVE_CONTROL"] = {
            "expected": "B-IDENTITY-BODY-ONLY >= 0.35",
            "observed": float(identity_body_only) if identity_body_only is not None else None,
            "pass": c1_pass,
        }
        control_details[f"{size_name}_C_NULL_CONTROL"] = {
            "expected": "B-RANDOM ~ 0.0",
            "observed": float(b_random_disc) if b_random_disc is not None else None,
            "pass": c2_pass,
        }
        control_details[f"{size_name}_C_DETERMINISTIC_BR_PRESERVES"] = {
            "expected": "B-DETERMINISTIC-BR-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15",
            "observed": float(br_body_only) if br_body_only is not None else None,
            "pass": c3_pass,
        }
        control_details[f"{size_name}_C_DETERMINISTIC_GZIP_PRESERVES"] = {
            "expected": "B-DETERMINISTIC-GZIP-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15",
            "observed": float(gzip_body_only) if gzip_body_only is not None else None,
            "pass": c4_pass,
        }
        control_details[f"{size_name}_C_WITHIN_STATE_DETERMINISTIC"] = {
            "expected": "Within-state body hash variation = 0 for deterministic brotli and gzip",
            "observed": {k: v["all_states_deterministic"] for k, v in within_state_variation.items()
                        if k in ["A_br_gzip", "B_gzip_only"]},
            "pass": c5_pass,
        }
        control_details[f"{size_name}_C_MIXED_CLIENT_DEGRADES"] = {
            "expected": "B-MIXED-CLIENT-BODY-ONLY < B-IDENTITY-BODY-ONLY",
            "observed": float(mixed_client_body_disc) if mixed_client_body_disc is not None else None,
            "pass": c6_pass,
        }
        control_details[f"{size_name}_C_STATUS_ONLY_INVARIANT"] = {
            "expected": "B-STATUS-ONLY >= 0.5 on /userinfo invariant",
            "observed": {k: float(v) for k, v in status_discs.items()},
            "pass": c7_pass,
        }
        control_details[f"{size_name}_C_NO_PIPELINE_ERRORS"] = {
            "expected": "0 errors",
            "observed": len(errors),
            "pass": c8_pass,
        }

        if not size_pass:
            all_controls_pass = False

    # Decision rule
    if all_controls_pass:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif any(not control_details[k]["pass"] for k in control_details if k.endswith("_C_NO_PIPELINE_ERRORS")):
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif any(not control_details[k]["pass"] for k in control_details if k.endswith("_C_POSITIVE_CONTROL") or k.endswith("_C_NULL_CONTROL")):
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif any(not control_details[k]["pass"] for k in control_details if k.endswith("_C_DETERMINISTIC_BR_PRESERVES") or k.endswith("_C_DETERMINISTIC_GZIP_PRESERVES")):
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif any(not control_details[k]["pass"] for k in control_details if k.endswith("_C_WITHIN_STATE_DETERMINISTIC")):
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    else:
        outcome = "MIXED"
        status = "COMPLETE"

    # Observations
    observations = [
        f"Mock OAuth2 server on localhost:{MOCK_SERVER_PORT} returning JSON responses",
        f"CDN negotiation proxy on localhost:{PROXY_PORT}",
        f"Client profiles: {list(CLIENT_PROFILES.keys())}",
        f"Body sizes: {BODY_SIZES}",
        f"2 endpoints: /userinfo (GET), /introspect (POST)",
        f"4 auth states x {REPS} reps x {len(CLIENT_PROFILES)} client profiles x 2 endpoints x {len(BODY_SIZES)} sizes = {4 * REPS * len(CLIENT_PROFILES) * 2 * len(BODY_SIZES)} total requests",
        f"Seed: {SEED}",
        f"Brotli available: {BROTLI_AVAILABLE}",
    ]

    for size_name in BODY_SIZES:
        for profile_name in CLIENT_PROFILES:
            for ep_name in ["/userinfo", "/introspect"]:
                mk = f"{size_name}_{ep_name}_{profile_name}"
                if mk in metrics:
                    observations.append(
                        f"size={size_name} profile={profile_name} {ep_name}: "
                        f"body={metrics[mk]['body_only_discrimination']:.4f}, "
                        f"status={metrics[mk]['status_only_discrimination']:.4f}, "
                        f"B-RANDOM={metrics[mk]['baselines']['B-RANDOM']:.4f}"
                    )

    validity_notes = [
        "Mock OAuth2 server (not Keycloak) returning JSON with random data field",
        "Same fingerprint algorithm as parent: SHA-256(repr((status, body_sha256, '')))",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "expired_token is locally-signed HS256, not real expired token",
        f"Brotli module available: {BROTLI_AVAILABLE}",
        "Proxy configured per client profile to apply fixed algorithm (not per-request header negotiation)",
        "Same Accept-Encoding always produces same algorithm - simulates deterministic CDN behavior",
        "Proxy overrides internal Accept-Encoding to identity to get raw response, then applies CDN-selected compression",
        "Body hash computed on compressed bytes received by client (not raw bytes from server)",
        "Python gzip is deterministic: same input + same level = same output (mtime=0 eliminates timestamp non-determinism)",
        "Python brotli is deterministic: same input + same level = same output",
        "Body-only discrimination is NOT tautological - compression directly attacks the body hash",
        f"Seed={SEED} for request ordering (deterministic across runs)",
        "This experiment extends EXP-RUNTIME-34741873198 from 0-729 bytes to 1KB-100KB JSON",
    ]

    if not BROTLI_AVAILABLE:
        validity_notes.append("BROTLI NOT AVAILABLE: Client A fallback to gzip")

    if errors:
        validity_notes.append(f"Pipeline errors: {len(errors)} requests failed")
        for e in errors[:5]:
            validity_notes.append(f"  Error: {e}")

    unresolved = [
        "Does body-only discrimination survive a real CDN (Cloudflare/Fastly/Akamai)?",
        "Does the result generalize to larger/more diverse body content-types beyond JSON?",
        "What discrimination floor remains when hashing decompressed bodies (normalization layer)?",
        "Would a filtered full-vector baseline survive compression?",
        "Does result generalize to production OAuth2 with real CDN and load-balancer?",
    ]

    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": control_details,
        "artifacts": [
            {"path": "raw_observations.json", "role": "raw", "description": "All HTTP observations per body size per client profile per endpoint per state"},
            {"path": "run_experiment.py", "role": "code", "description": "Frozen experiment execution script"},
        ],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    # Save raw observations
    raw_obs_serializable = {}
    for composite_key, endpoint_obs in raw_observations_all.items():
        if composite_key in BODY_SIZES:
            continue
        raw_obs_serializable[composite_key] = {}
        for ep_name, state_obs in endpoint_obs.items():
            raw_obs_serializable[composite_key][ep_name] = {}
            for state, obs_list in state_obs.items():
                raw_obs_serializable[composite_key][ep_name][state] = []
                for obs in obs_list:
                    raw_obs_serializable[composite_key][ep_name][state].append({
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

    with open("result.json", "w") as f:
        json.dump(result, f, indent=2, cls=NumpyEncoder)
    print(f"\nResult written to result.json")
    print(f"Status: {result['status']}, Outcome: {result['outcome']}")
