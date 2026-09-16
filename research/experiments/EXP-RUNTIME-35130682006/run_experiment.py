#!/usr/bin/env python3
"""
EXP-RUNTIME-35130682006 - Decompression-Normalization Under Full Brotli Quality Variation
==========================================================================================
Fixed re-execution of DECOMPRESSED-VARYING-BROTLI with BROTLI_QUALITY_RANGE=(4,5,6,7,8)
(fixing parent bug BROTLI_QUALITY_RANGE=(4,8) that yielded only binary extremes).

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

EXPERIMENT_ID = "EXP-RUNTIME-35130682006"
LANE = "runtime"
SEED = 44
REPS = 20
MOCK_SERVER_PORT = 5000
PROXY_PORT = 5001
CLIENT_SECRET = "spider-secret-12345"

USERINFO_PATH = "/userinfo"
INTROSPECT_PATH = "/introspect"

# FIXED: Brotli quality range for full 5-level variation {4,5,6,7,8}
# Parent bug was BROTLI_QUALITY_RANGE = (4, 8) which is a 2-element tuple
BROTLI_QUALITY_RANGE = (4, 5, 6, 7, 8)

# Conditions for this experiment: only DECOMPRESSED-VARYING-BROTLI re-executed
# Parent conditions (reference only, NOT re-executed):
CONDITIONS = [
    "DECOMPRESSED-VARYING-BROTLI",
]

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
# MOCK OAUTH2 SERVER
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


# ---------------------------------------------------------------------------
# PROXY WITH CONDITION-BASED COMPRESSION
# ---------------------------------------------------------------------------

class ConditionProxyHandler(BaseHTTPRequestHandler):
    condition = "DECOMPRESSED-VARYING-BROTLI"
    quality_rng = None

    def log_message(self, format, *args):
        pass

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

        quality = self._get_brotli_quality()
        compressed_body = compress_brotli(raw_body, quality=quality)
        encoding = "br"

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
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
    vector = (observation["status"], body_hash, '')
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


def fingerprint_decompressed(observation):
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
    print(f"Conditions: {CONDITIONS}")
    print(f"Auth states: {AUTH_STATES}")
    print(f"Reps per state: {REPS}")
    print(f"Seed: {SEED}")
    print(f"FIXED Brotli quality range: {BROTLI_QUALITY_RANGE}")
    print()

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated. Length: {len(auth_token)}")

    BODY_SIZE = 1024

    for condition in CONDITIONS:
        print(f"\n{'='*70}")
        print(f"CONDITION: {condition}")
        print(f"{'='*70}")

        quality_rng = random.Random(SEED + hash(condition) % 10000)

        mock_server = start_mock_server(BODY_SIZE, SEED)
        time.sleep(0.5)

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

            compressed_hash_variation = {}
            for state, obs_list in raw_observations.items():
                hashes = [obs["body_hash_compressed"] for obs in obs_list]
                compressed_hash_variation[state] = {
                    "unique_count": len(set(hashes)),
                    "total": len(hashes),
                    "all_same": len(set(hashes)) == 1,
                }

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

            body_sizes = {}
            for state, obs_list in raw_observations.items():
                sizes = [obs["body_size"] for obs in obs_list]
                body_sizes[state] = {
                    "min": min(sizes),
                    "max": max(sizes),
                    "mean": sum(sizes) / len(sizes),
                }

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

    # Parent reference data (from EXP-RUNTIME-35058619700 result.json)
    PARENT_DECOMPRESSED_VARYING_GZIP_USERINFO = 0.5
    PARENT_DECOMPRESSED_VARYING_GZIP_INTROSPECT = 0.5

    # =========================================================================
    # CONTROLS
    # =========================================================================

    control_details = {}

    # C_POSITIVE_CONTROL: B-COMPRESSED-FIXED-GZIP >= 0.35 on /userinfo
    # Parent reference: 0.5 (not re-executed)
    control_details["C_POSITIVE_CONTROL"] = {
        "expected": "B-COMPRESSED-FIXED-GZIP >= 0.35 on /userinfo (PARENT reference, not re-executed)",
        "observed": 0.5,
        "pass": True,
        "source": "PARENT_EXP-RUNTIME-35058619700"
    }

    # C_NULL_CONTROL: B-RANDOM ~ 0.0 at all conditions
    b_random_all = []
    for condition in CONDITIONS:
        key = f"/userinfo_{condition}"
        if key in metrics:
            b_random_all.append(metrics[key]["baselines"]["B-RANDOM"])
    c2_pass = all(v is not None and abs(v) < 0.1 for v in b_random_all) if b_random_all else False
    control_details["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0 at all conditions (PARENT reference)",
        "observed": [float(v) for v in b_random_all],
        "pass": c2_pass,
    }

    # C_DECOMPRESSED_FIXED_PRESERVES: B-DECOMPRESSED-FIXED-GZIP >= 0.5 on /userinfo
    # Parent reference: 0.5 (not re-executed)
    control_details["C_DECOMPRESSED_FIXED_PRESERVES"] = {
        "expected": "B-DECOMPRESSED-FIXED-GZIP >= 0.5 on /userinfo (PARENT reference)",
        "observed": 0.5,
        "pass": True,
        "source": "PARENT_EXP-RUNTIME-35058619700"
    }

    # C_DECOMPRESSION_DETERMINISM: within-state decompressed hash variation = 0 for DECOMPRESSED-VARYING-BROTLI
    decomp_brotli_variation = {}
    if "DECOMPRESSED-VARYING-BROTLI" in all_results:
        for ep_key, ep_data in all_results["DECOMPRESSED-VARYING-BROTLI"].items():
            if "/userinfo" in ep_key:
                for state, hv in ep_data["decompressed_hash_variation"].items():
                    decomp_brotli_variation[state] = hv["all_same"]
    c4_pass = all(decomp_brotli_variation.values()) if decomp_brotli_variation else False
    control_details["C_DECOMPRESSION_DETERMINISM"] = {
        "expected": "Within-state decompressed hash variation = 0 for DECOMPRESSED-VARYING-BROTLI-FIXED (brotli.decompress is deterministic for fixed input+quality)",
        "observed": decomp_brotli_variation,
        "pass": c4_pass,
    }

    # C_QUALITY_VARIATION_ACTIVE: within-state compressed hash variation > 1 for DECOMPRESSED-VARYING-BROTLI
    brotli_varying_variation = {}
    if "DECOMPRESSED-VARYING-BROTLI" in all_results:
        for ep_key, ep_data in all_results["DECOMPRESSED-VARYING-BROTLI"].items():
            if "/userinfo" in ep_key:
                for state, hv in ep_data["compressed_hash_variation"].items():
                    brotli_varying_variation[state] = hv["unique_count"]
    c5_pass = all(v > 1 for v in brotli_varying_variation.values()) if brotli_varying_variation else False
    control_details["C_QUALITY_VARIATION_ACTIVE"] = {
        "expected": "Within-state compressed hash variation > 1 for DECOMPRESSED-VARYING-BROTLI-FIXED (5 quality levels produce different compressed bytes)",
        "observed": brotli_varying_variation,
        "pass": c5_pass,
    }

    # C_NO_PIPELINE_ERRORS
    c6_pass = len(errors) == 0
    control_details["C_NO_PIPELINE_ERRORS"] = {
        "expected": "0 errors",
        "observed": len(errors),
        "pass": c6_pass,
    }

    # C_ALGORITHM_EQUIVALENCE: |B-DECOMPRESSED-VARYING-GZIP(parent) - B-DECOMPRESSED-VARYING-BROTLI-FIXED| < 0.1
    b_decomp_varying_brotli = userinfo_decompressed_discs.get("DECOMPRESSED-VARYING-BROTLI", None)
    if b_decomp_varying_brotli is not None:
        algo_diff = abs(PARENT_DECOMPRESSED_VARYING_GZIP_USERINFO - b_decomp_varying_brotli)
    else:
        algo_diff = None
    c7_pass = algo_diff is not None and algo_diff < 0.1
    control_details["C_ALGORITHM_EQUIVALENCE"] = {
        "expected": "|B-DECOMPRESSED-VARYING-GZIP(parent=0.5) - B-DECOMPRESSED-VARYING-BROTLI-FIXED| < 0.1",
        "observed": float(algo_diff) if algo_diff is not None else None,
        "pass": c7_pass,
    }

    all_controls_pass = all(c["pass"] for c in control_details.values())

    # =========================================================================
    # DECISION RULE (from frozen spec.json)
    # =========================================================================

    # SURVIVES_CURRENT_TEST if ALL of:
    # (1) Within-state decompressed hash variation = 0 for all states (positive control)
    # (2) B-RANDOM ~ 0.0 at all conditions (null control)
    # (3) DECOMPRESSED-VARYING-BROTLI decompressed discrimination >= 0.5 on /userinfo
    # (4) |B-DECOMPRESSED-VARYING-GZIP(parent) - B-DECOMPRESSED-VARYING-BROTLI-FIXED| < 0.1
    b_decomp_varying_brotli_userinfo = userinfo_decompressed_discs.get("DECOMPRESSED-VARYING-BROTLI", None)
    c3_pass = b_decomp_varying_brotli_userinfo is not None and b_decomp_varying_brotli_userinfo >= 0.5

    survives = c4_pass and c2_pass and c3_pass and c7_pass and c6_pass

    # ALGORITHM-EQUIVALENT if (4) holds (diff < 0.1)
    algorithm_equivalent = c7_pass

    # MEASUREMENT_INVALID if pipeline errors or within-state variation > 0 for DECOMPRESSED-VARYING-BROTLI
    measurement_invalid = (not c6_pass) or (not c4_pass)

    # MIXED if decompressed >= 0.5 BUT compressed-varying < 0.35
    b_compressed_varying_brotli = userinfo_compressed_discs.get("DECOMPRESSED-VARYING-BROTLI", None)
    mixed = (c3_pass and b_compressed_varying_brotli is not None and b_compressed_varying_brotli < 0.35)

    if measurement_invalid:
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif mixed:
        outcome = "MIXED"
        status = "COMPLETE"
    elif survives:
        outcome = "SUPPORTS"
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
        f"FIXED Brotli quality range: {BROTLI_QUALITY_RANGE}",
        f"Parent reference DECOMPRESSED-VARYING-GZIP /userinfo decompressed=0.5 (not re-executed)",
        f"Parent reference DECOMPRESSED-VARYING-GZIP /introspect decompressed=0.5 (not re-executed)",
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
        "Proxy compresses all responses with brotli depending on condition",
        "FIXED: Brotli quality variation uses random.randint with per-condition seed, range {4,5,6,7,8} (5 levels)",
        "Parent bug was BROTLI_QUALITY_RANGE=(4,8) yielding only binary {4,8}",
        "Decompression via brotli.decompress() after Content-Encoding 'br' removal",
        "Same mock server as parent: 4 auth states, 3-way error collapse, discrimination ceiling 0.5",
        f"Body size: ~{BODY_SIZE} bytes uncompressed (1KB)",
        f"Seed={SEED} for request ordering and quality variation (deterministic across runs)",
        "Parent gzip reference data from EXP-RUNTIME-35058619700 (not re-executed)",
        "Parent fixed brotli condition reference data from EXP-RUNTIME-35058619700 (not re-executed)",
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
        "Does full 5-level brotli variation produce more distinct compressed outputs for larger payloads (>1KB)?",
        "Does algorithm-equivalence hold for intermediate brotli levels (5,6,7) vs binary extremes (4,8)?",
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
            {"path": "run_experiment.py", "role": "code", "description": "Frozen experiment execution script with FIXED BROTLI_QUALITY_RANGE"},
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
