#!/usr/bin/env python3
"""
EXP-RUNTIME-35513777099 - Multi-Layer Encoding Decompression Correctness
========================================================================
Tests whether iterative decompression correctness holds for multi-layer
compressed encodings (gzip->brotli, brotli->gzip) where max_depth>1,
using high-entropy non-redundant payloads with compressed sizes in the
2-99KB range.

Frozen from spec.json and prereg.md - DO NOT MODIFY.

Architecture:
  Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server

Conditions tested:
  - GZIP-THEN-BROTLI: body -> gzip.compress(level=1) -> brotli.compress(quality=4) -> chunked
  - BROTLI-THEN-GZIP: body -> brotli.compress(quality=4) -> gzip.compress(level=1) -> chunked
"""

import binascii
import brotli
import gzip
import hashlib
import json
import math
import random
import struct
import sys
import time
import threading
import uuid
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection

import jwt
import requests


# ---------------------------------------------------------------------------
# FROZEN CONSTANTS (from frozen spec.json / prereg.md)
# ---------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-RUNTIME-35513777099"
LANE = "runtime"
SEED = 44
REPS = 5
BASE_PORT = 8700
PROXY_PORT_BASE = 8800
CLIENT_SECRET = "spider-secret-12345"

USERINFO_PATH = "/userinfo"

CONTENT_TYPES = {
    "JSON": "application/json",
    "HTML": "text/html",
    "BINARY": "application/octet-stream",
}

TARGET_SIZES = {
    "10KB": 10240,
    "100KB": 102400,
}

# Multi-layer encoding configurations
MULTI_LAYER_MODES = {
    "GZIP-THEN-BROTLI": {
        "layers": [
            {"type": "gzip", "level": 1},
            {"type": "brotli", "quality": 4},
        ],
        "use_chunked": True,
        "chunk_size": 32,
    },
    "BROTLI-THEN-GZIP": {
        "layers": [
            {"type": "brotli", "quality": 4},
            {"type": "gzip", "level": 1},
        ],
        "use_chunked": True,
        "chunk_size": 32,
    },
}

# Regression controls (single-layer, from parent)
REGRESSION_MODES = {
    "GZIP-SINGLE": {
        "layers": [{"type": "gzip", "level": None}],
        "use_chunked": True,
        "chunk_size": 32,
    },
    "BROTLI-SINGLE": {
        "layers": [{"type": "brotli", "quality": 6}],
        "use_chunked": True,
        "chunk_size": 32,
    },
}

AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]

# Shannon entropy minimum threshold (bits per byte)
SHANNON_ENTROPY_MIN = 3.5

# Word lists for high-entropy HTML generation
HTML_WORDS = [
    "quantum", "nebula", "algorithm", "synthesis", "morphology", "topology",
    "paradigm", "entropy", "syntactic", "recursive", "distributed", "asynchronous",
    "vector", "scalar", "heuristic", "stochastic", "orthogonal", "polymorphic",
    "isomorphic", "homomorphic", "cryptographic", "probabilistic", "steganographic",
    "metamorphic", "quantitative", "longitudinal", "multivariate", "dimensional",
    "resonance", "catalyst", "substrate", "amplitude", "frequency", "spectral",
    "turbulent", "viscous", "lamellar", "ferromagnetic", "piezoelectric",
    "superconductor", "semiconductor", "photoelectric", "thermodynamic",
    "electromagnetic", "gravitational", "chromatic", "diffraction", "interference",
    "polarization", "refraction", "scattering", "absorption", "emission",
    "fluorescence", "phosphorescence", "luminescence", "bioluminescence",
    "chromatography", "spectroscopy", "microscopy", "crystallography",
    "algorithmic", "heuristic", "deterministic", "stochastic", "Bayesian",
    "Gaussian", "Poisson", "Markovian", "Eulerian", "Lagrangian",
    "Hilbert", "Fourier", "Laplace", "Riemann", "Euclidean", "Riemannian",
    "manifold", "bundle", "morphism", "functor", "category", "groupoid",
    "semigroup", "monoid", "lattice", "poset", "topology", "homology",
    "cohomology", "homotopy", "sheaf", "presheaf", "differential",
    "geodesic", "curvature", "tensor", "matrix", "polynomial", "eigenvalue",
]


# ---------------------------------------------------------------------------
# SHANNON ENTROPY COMPUTATION
# ---------------------------------------------------------------------------

def compute_shannon_entropy(data):
    """Compute Shannon entropy H = -sum(p(b)*log2(p(b))) for byte values 0-255."""
    if len(data) == 0:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    length = len(data)
    h = 0.0
    for count in freq:
        if count > 0:
            p = count / length
            h -= p * math.log2(p)
    return h


# ---------------------------------------------------------------------------
# CONTENT BODY GENERATORS (HIGH-ENTROPY)
# Reused from parent EXP-RUNTIME-35495699298
# ---------------------------------------------------------------------------

def _he_seed(state, content_type, target_size):
    """Deterministic seed from state, content_type, and target_size."""
    seed_str = f"{state}:{content_type}:{target_size}:he_seed"
    digest = hashlib.sha256(seed_str.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big")


def generate_json_he_body(state, target_size):
    """High-entropy JSON with unique UUIDs, random floats, random tags/descriptions."""
    rng = random.Random(_he_seed(state, "JSON", target_size))

    if state in ("no_auth", "expired_token", "invalid_token"):
        entries = []
        current_size = 0
        header = json.dumps({"error": "invalid_token", "entries": []}).encode("utf-8")
        current_size = len(header)
        while current_size < target_size:
            uuid_val = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{state}:{rng.getrandbits(64)}"))
            entry = {
                "id": uuid_val,
                "key": rng.getrandbits(64).to_bytes(8, "big").hex(),
                "score": round(rng.uniform(-1000.0, 1000.0), 6),
                "tag": f"tag_{rng.randint(0, 999999):06d}",
                "desc": " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(3, 8))),
                "active": rng.choice([True, False]),
                "nested": {
                    "a": round(rng.uniform(0.0, 1.0), 8),
                    "b": rng.getrandbits(32),
                    "c": uuid_val,
                },
            }
            entry_json = json.dumps(entry)
            entry_bytes = entry_json.encode("utf-8")
            if current_size + len(entry_bytes) + 1 > target_size:
                break
            entries.append(entry)
            current_size += len(entry_bytes) + 1

        base = {"error": "invalid_token", "entries": entries}
        raw = json.dumps(base, separators=(",", ":")).encode("utf-8")
    else:
        entries = []
        current_size = 0
        while current_size < target_size:
            uuid_val = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{state}:{rng.getrandbits(64)}"))
            entry = {
                "sub": uuid_val,
                "name": " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(2, 4))),
                "email": f"{uuid_val[:8]}@{rng.choice(HTML_WORDS)}.example.com",
                "scope": " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(2, 6))),
                "score": round(rng.uniform(-1000.0, 1000.0), 6),
                "tag": f"tag_{rng.randint(0, 999999):06d}",
                "desc": " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(4, 12))),
                "active": rng.choice([True, False]),
                "nested": {
                    "x": round(rng.uniform(0.0, 1.0), 8),
                    "y": rng.getrandbits(32),
                    "z": uuid_val,
                },
            }
            entry_json = json.dumps(entry)
            entry_bytes = entry_json.encode("utf-8")
            if current_size + len(entry_bytes) + 1 > target_size:
                break
            entries.append(entry)
            current_size += len(entry_bytes) + 1

        base = {"sub": "alice", "name": "Alice", "entries": entries}
        raw = json.dumps(base, separators=(",", ":")).encode("utf-8")

    if len(raw) < target_size:
        padding_needed = target_size - len(raw)
        pad_bytes = bytes(rng.getrandbits(8) for _ in range(padding_needed))
        raw = raw + pad_bytes[:padding_needed]

    return raw[:target_size]


def generate_html_he_body(state, target_size):
    """High-entropy HTML with Wikipedia-style paragraphs, unique auth-state sections."""
    rng = random.Random(_he_seed(state, "HTML", target_size))

    sections = []
    sections.append("<!DOCTYPE html>")
    sections.append('<html lang="en">')
    sections.append("<head>")
    sections.append('<meta charset="UTF-8">')
    sections.append(f'<title>High-Entropy Document - {state}</title>')
    sections.append("</head>")
    sections.append("<body>")
    sections.append(f'<div class="auth-state" data-state="{state}">')

    section_id = 0
    current_size = sum(len(s.encode("utf-8")) for s in sections)

    while current_size < target_size:
        uuid_val = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{state}:{rng.getrandbits(64)}"))
        word_count = rng.randint(20, 60)
        words = [rng.choice(HTML_WORDS) for _ in range(word_count)]
        paragraph = " ".join(words) + "."
        header_text = " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(3, 6))).title()

        section = (
            f'<section id="s{section_id}" data-uuid="{uuid_val}">\n'
            f'<h{rng.randint(2, 4)}>{header_text}</h{rng.randint(2, 4)}>\n'
            f"<p>{paragraph}</p>\n"
            f"<p>" + " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(15, 40))) + ".</p>\n"
            f"</section>\n"
        )
        section_bytes = section.encode("utf-8")
        if current_size + len(section_bytes) > target_size:
            break
        sections.append(section)
        current_size += len(section_bytes)
        section_id += 1

    sections.append("</div>")
    sections.append("</body>")
    sections.append("</html>")

    raw = "\n".join(sections).encode("utf-8")

    if len(raw) < target_size:
        padding_needed = target_size - len(raw)
        pad_words = []
        while sum(len(w.encode("utf-8")) + 1 for w in pad_words) < padding_needed:
            pad_words.append(rng.choice(HTML_WORDS))
        padding = (" ".join(pad_words)).encode("utf-8")[:padding_needed]
        raw = raw + padding

    return raw[:target_size]


def generate_binary_he_body(state, target_size):
    """High-entropy binary format with magic header, version, state marker, entries with CRC32."""
    rng = random.Random(_he_seed(state, "BINARY", target_size))

    magic = b'\x89SPIDER\x01\x02'
    version = struct.pack(">I", 1)
    state_bytes = struct.pack(">I", hash(state) & 0xFFFFFFFF)

    header = magic + version + state_bytes
    current_size = len(header)

    entries = []
    while current_size < target_size:
        key = rng.getrandbits(64).to_bytes(8, "big")
        payload_len = rng.randint(4, 32)
        payload = bytes(rng.getrandbits(8) for _ in range(payload_len))
        entry = key + struct.pack(">I", payload_len) + payload
        if current_size + len(entry) + 4 > target_size:
            break
        entries.append(entry)
        current_size += len(entry) + 4

    raw = header
    for entry in entries:
        raw += entry
        crc = binascii.crc32(entry) & 0xFFFFFFFF
        raw += struct.pack(">I", crc)

    if len(raw) < target_size:
        padding_needed = target_size - len(raw)
        pad_bytes = bytes(rng.getrandbits(8) for _ in range(padding_needed))
        raw = raw + pad_bytes[:padding_needed]

    return raw[:target_size]


BODY_GENERATORS = {
    "JSON": generate_json_he_body,
    "HTML": generate_html_he_body,
    "BINARY": generate_binary_he_body,
}


# ---------------------------------------------------------------------------
# SHANNON ENTROPY PRE-FLIGHT VALIDATION
# ---------------------------------------------------------------------------

def validate_entropy_pre_flight():
    """Validate that all content types achieve minimum Shannon entropy across auth states and sizes."""
    results = {}
    for ct_name in CONTENT_TYPES:
        entropies = []
        for state in AUTH_STATES:
            for size_name, target_size in TARGET_SIZES.items():
                gen = BODY_GENERATORS[ct_name]
                body = gen(state, target_size)
                h = compute_shannon_entropy(body)
                entropies.append(h)
        mean_ent = sum(entropies) / len(entropies) if entropies else 0.0
        min_ent = min(entropies) if entropies else 0.0
        max_ent = max(entropies) if entropies else 0.0
        results[ct_name] = {
            "mean_entropy": mean_ent,
            "min_entropy": min_ent,
            "max_entropy": max_ent,
            "all_above_threshold": all(h >= SHANNON_ENTROPY_MIN for h in entropies),
            "per_state_size": {},
        }
        idx = 0
        for state in AUTH_STATES:
            for size_name in TARGET_SIZES:
                results[ct_name]["per_state_size"][f"{state}_{size_name}"] = entropies[idx]
                idx += 1
    return results


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
# Serves multi-layer compressed responses with configurable layers.
# ---------------------------------------------------------------------------

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class MockOAuthHandler(BaseHTTPRequestHandler):
    body_size = 1024
    content_type = "JSON"
    layers = []
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
        gen = BODY_GENERATORS.get(self.content_type, generate_json_he_body)
        return gen(state, size)

    def _get_mime_type(self):
        return CONTENT_TYPES.get(self.content_type, "application/json")

    def _apply_layers(self, body):
        """Apply compression layers in order. Returns (compressed_data, ce_header)."""
        current_data = body
        ce_parts = []
        
        for layer in MockOAuthHandler.layers:
            if layer["type"] == "gzip":
                if layer.get("level") is not None:
                    current_data = gzip.compress(current_data, compresslevel=layer["level"])
                else:
                    current_data = gzip.compress(current_data)
                ce_parts.append("gzip")
            elif layer["type"] == "brotli":
                quality = layer.get("quality", 6)
                current_data = brotli.compress(current_data, quality=quality)
                ce_parts.append("br")
        
        # Build Content-Encoding header (outermost first)
        ce_header = ", ".join(ce_parts) if ce_parts else "identity"
        return current_data, ce_header

    def do_GET(self):
        if self.path == USERINFO_PATH:
            state = self._get_auth_state()
            body = self._get_body(state, self.body_size)
            status = 200 if state == "valid_token" else 401

            if MockOAuthHandler.layers:
                compressed, ce_header = self._apply_layers(body)
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
            else:
                # Identity (no compression)
                self.send_response(status)
                self.send_header("Content-Type", self._get_mime_type())
                self.send_header("Content-Length", len(body))
                self.send_header("Cache-Control", "private")
                self.send_header("Vary", "Authorization")
                self.end_headers()
                self.wfile.write(body)
            self.wfile.flush()
        else:
            self.send_error(404)

    def do_POST(self):
        self.send_error(404)


def start_mock_server(port, body_size=1024, content_type="JSON",
                      layers=None, use_chunked=True, chunk_size=32):
    MockOAuthHandler.body_size = body_size
    MockOAuthHandler.content_type = content_type
    MockOAuthHandler.layers = layers or []
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
# Forwards responses from origin to client with chunked transfer-encoding.
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
                                  ReverseProxyHandler.upstream_port, timeout=30)
            conn.request(method, self.path, body=req_body, headers=headers)
            upstream_resp = conn.getresponse()
            resp_status = upstream_resp.status
            resp_headers = dict(upstream_resp.getheaders())
            resp_body = upstream_resp.read()
            conn.close()

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
# ITERATIVE DECOMPRESSION
# Tries brotli first, then gzip, up to MAX_DEPTH iterations.
# This correctly handles multi-layer encodings.
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


def make_request(url, method="GET", auth_header=None, timeout=30):
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

def run_single_cell(port_idx, ct_name, comp_mode, comp_config, target_size, auth_token, rng):
    """Run one experimental cell: (content_type, compression_mode, target_size)."""
    layers = comp_config["layers"]
    use_chunked = comp_config.get("use_chunked", True)
    chunk_size = comp_config.get("chunk_size", 32)

    origin_port = BASE_PORT + port_idx
    mock_server = start_mock_server(origin_port, target_size, ct_name,
                                    layers=layers, use_chunked=use_chunked,
                                    chunk_size=chunk_size)
    time.sleep(0.5)

    proxy_port = PROXY_PORT_BASE + port_idx
    proxy = start_reverse_proxy(proxy_port, origin_port,
                                use_chunked=use_chunked, chunk_size=chunk_size)
    time.sleep(0.5)

    try:
        test_resp = requests.get(
            f"http://127.0.0.1:{proxy_port}{USERINFO_PATH}",
            headers={"Authorization": f"Bearer {auth_token}",
                     "Accept-Encoding": "br, gzip, identity"},
            timeout=10)
    except Exception as e:
        stop_reverse_proxy(proxy)
        stop_mock_server(mock_server)
        return None, f"Connectivity test failed: {e}"

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
    cell_observations = []

    for i, (state, rep) in enumerate(plan):
        auth_header = get_auth_header(state, auth_token)
        url = f"http://127.0.0.1:{proxy_port}{USERINFO_PATH}"

        obs = make_request(url, method="GET", auth_header=auth_header)
        obs["state"] = state
        obs["rep"] = rep
        obs["content_type"] = ct_name
        obs["comp_mode"] = comp_mode
        obs["target_size"] = target_size

        obs["body_hash_compressed"] = hashlib.sha256(obs["body"]).hexdigest()
        obs["body_size"] = len(obs["body"])
        obs["content_encoding"] = obs["headers"].get("Content-Encoding", "none")
        obs["proxy_mode"] = obs["headers"].get("X-Proxy-Mode", "none")
        obs["cache_hit"] = obs["headers"].get("X-Cache", "none")

        gen = BODY_GENERATORS.get(ct_name, generate_json_he_body)
        expected_body = gen(state, target_size)
        expected_hash = hashlib.sha256(expected_body).hexdigest()
        obs["expected_hash"] = expected_hash

        if state not in cell_expected_hashes:
            cell_expected_hashes[state] = expected_hash

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

        correctness_match = (obs["decompressed_hash"] == expected_hash)
        obs["correctness_match"] = correctness_match
        cell_correctness_results.append(correctness_match)

        is_compressed = obs["content_encoding"] in ("br", "gzip")
        if is_compressed:
            silent_fallback = (obs["decompressed_hash"] == obs["body_hash_compressed"])
            obs["silent_fallback"] = silent_fallback
        else:
            obs["silent_fallback"] = False

        if is_compressed:
            obs["decompression_altered_bytes"] = (decompressed != obs["body"])
        else:
            obs["decompression_altered_bytes"] = None

        cell_compressed_sizes.append(obs["body_size"])
        cell_fingerprints_compressed[state].append(obs["body_hash_compressed"])
        cell_fingerprints_decompressed[state].append(obs["decompressed_hash"])
        cell_raw_observations[state].append(obs)

        obs_record = {k: v for k, v in obs.items()
                      if k not in ("decompressed_bytes", "body")}
        cell_observations.append(obs_record)

        if i < len(plan) - 1:
            jitter = rng.uniform(0.05, 0.15)
            time.sleep(jitter)

    compressed_disc = compute_discrimination_score(cell_fingerprints_compressed)
    decompressed_disc = compute_discrimination_score(cell_fingerprints_decompressed)

    b_rand_fps = baseline_random(n=REPS * len(AUTH_STATES))
    b_rand_by_state = {}
    idx = 0
    for s in AUTH_STATES:
        b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
        idx += REPS
    b_rand_disc = compute_discrimination_score(b_rand_by_state)

    decompressed_hash_variation = {}
    for state, obs_list in cell_raw_observations.items():
        hashes = [obs["decompressed_hash"] for obs in obs_list]
        decompressed_hash_variation[state] = {
            "unique_count": len(set(hashes)),
            "total": len(hashes),
            "all_same": len(set(hashes)) == 1,
        }

    correctness_by_state = {}
    for state, obs_list in cell_raw_observations.items():
        matches = [obs["correctness_match"] for obs in obs_list]
        correctness_by_state[state] = {
            "pass_count": sum(matches),
            "fail_count": len(matches) - sum(matches),
            "total": len(matches),
            "all_pass": all(matches),
        }

    silent_fallback_by_state = {}
    for state, obs_list in cell_raw_observations.items():
        compressed_obs = [obs for obs in obs_list if obs["content_encoding"] in ("br", "gzip")]
        fallbacks = [obs["silent_fallback"] for obs in compressed_obs]
        silent_fallback_by_state[state] = {
            "fallback_count": sum(fallbacks),
            "total": len(fallbacks),
            "any_fallback": any(fallbacks),
        }

    decompression_altered = {}
    for state, obs_list in cell_raw_observations.items():
        compressed_obs = [obs for obs in obs_list if obs["content_encoding"] in ("br", "gzip")]
        altered = [obs["decompression_altered_bytes"] for obs in compressed_obs if obs["decompression_altered_bytes"] is not None]
        decompression_altered[state] = {
            "all_altered": all(altered) if altered else True,
            "count_altered": sum(1 for a in altered if a),
            "count_total": len(altered),
        }

    cell_key = f"{ct_name}_{comp_mode}_{target_size}B"
    cell_data = {
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
        "compressed_size_bytes": {
            "mean": sum(cell_compressed_sizes) / len(cell_compressed_sizes) if cell_compressed_sizes else 0,
            "min": min(cell_compressed_sizes) if cell_compressed_sizes else 0,
            "max": max(cell_compressed_sizes) if cell_compressed_sizes else 0,
        },
        "observations": cell_observations,
    }

    stop_reverse_proxy(proxy)
    stop_mock_server(mock_server)
    time.sleep(0.3)

    return cell_key, cell_data


def run_experiment():
    all_results = {}
    all_controls = {}
    all_observations = []
    all_validity_notes = []
    errors = []
    request_count = 0

    print(f"Experiment: {EXPERIMENT_ID}")
    print(f"Content types: {list(CONTENT_TYPES.keys())}")
    print(f"Target sizes: {TARGET_SIZES}")
    print(f"Multi-layer modes: {list(MULTI_LAYER_MODES.keys())}")
    print(f"Regression modes: {list(REGRESSION_MODES.keys())}")
    print(f"Auth states: {AUTH_STATES}")
    print(f"Reps per cell: {REPS}")
    print(f"Seed: {SEED}")
    print(f"Max decompression depth: 5")
    print(f"Shannon entropy minimum: {SHANNON_ENTROPY_MIN} bits/byte")
    print()

    all_observations.append(f"Experiment: {EXPERIMENT_ID}")
    all_observations.append(f"Architecture: Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server")
    all_observations.append(f"Content types: {list(CONTENT_TYPES.keys())} (high-entropy generators)")
    all_observations.append(f"Multi-layer modes: {list(MULTI_LAYER_MODES.keys())}")
    all_observations.append(f"Regression modes: {list(REGRESSION_MODES.keys())}")
    all_observations.append(f"Target sizes: {TARGET_SIZES}")
    all_observations.append(f"Reps per cell: {REPS}")
    all_observations.append(f"Seed: {SEED}")

    # =========================================================================
    # PRE-FLIGHT: Shannon entropy validation
    # =========================================================================
    print("\n" + "=" * 70)
    print("PRE-FLIGHT: Shannon entropy validation")
    print("=" * 70)

    entropy_results = validate_entropy_pre_flight()
    entropy_fail = False
    for ct_name, ent_data in entropy_results.items():
        print(f"  {ct_name}: mean={ent_data['mean_entropy']:.4f} min={ent_data['min_entropy']:.4f} "
              f"max={ent_data['max_entropy']:.4f} above_threshold={ent_data['all_above_threshold']}")
        if not ent_data["all_above_threshold"]:
            entropy_fail = True

    if entropy_fail:
        print("\nMEASUREMENT_INVALID: Shannon entropy below 3.5 bits/byte for at least one content type")
        return build_measurement_invalid_result(
            "Shannon entropy below 3.5 bits/byte threshold for at least one content type",
            entropy_results
        )

    print("\nAll content types pass entropy validation (>= 3.5 bits/byte)")

    print("Generating valid token...")
    auth_token = make_valid_token()
    print(f"Valid token generated.")

    total_correctness_pass = 0
    total_correctness_fail = 0
    total_silent_fallbacks = 0
    total_decompression_errors = 0

    rng = random.Random(SEED)
    port_idx = 0

    # =========================================================================
    # PHASE 1: Main experimental cells (2 sizes x 3 types x 2 multi-layer encodings)
    # =========================================================================
    print("\n" + "=" * 70)
    print("PHASE 1: Main experimental cells (multi-layer encodings)")
    print("=" * 70)

    for size_name, target_size in TARGET_SIZES.items():
        for ct_name in CONTENT_TYPES.keys():
            for comp_mode, comp_config in MULTI_LAYER_MODES.items():
                cell_key, cell_data = run_single_cell(
                    port_idx, ct_name, comp_mode, comp_config,
                    target_size, auth_token, rng)
                port_idx += 1

                if cell_data is None:
                    errors.append(f"{cell_key}: {cell_key}")
                    continue

                all_results[cell_key] = cell_data
                total_correctness_pass += cell_data["correctness_match_count"]
                total_correctness_fail += (cell_data["total_requests"] - cell_data["correctness_match_count"])
                total_silent_fallbacks += cell_data["silent_fallback_count"]
                total_decompression_errors += cell_data["decompression_error_count"]
                request_count += cell_data["total_requests"]

                print(f"  {cell_key}: correctness={cell_data['correctness_match_rate']:.4f} "
                      f"({cell_data['correctness_match_count']}/{cell_data['total_requests']}), "
                      f"silent_fallbacks={cell_data['silent_fallback_count']}, "
                      f"compressed_size={cell_data['compressed_size_bytes']['mean']:.0f}B")

    # =========================================================================
    # PHASE 2: Regression controls (single-layer, 10KB)
    # =========================================================================
    print("\n" + "=" * 70)
    print("PHASE 2: Regression controls (single-layer)")
    print("=" * 70)

    for ct_name in CONTENT_TYPES.keys():
        for comp_mode, comp_config in REGRESSION_MODES.items():
            cell_key, cell_data = run_single_cell(
                port_idx, ct_name, comp_mode, comp_config,
                10240, auth_token, rng)
            port_idx += 1

            if cell_data is None:
                errors.append(f"{cell_key}: connectivity failed")
                continue

            all_results[cell_key] = cell_data
            total_correctness_pass += cell_data["correctness_match_count"]
            total_correctness_fail += (cell_data["total_requests"] - cell_data["correctness_match_count"])
            total_silent_fallbacks += cell_data["silent_fallback_count"]
            total_decompression_errors += cell_data["decompression_error_count"]
            request_count += cell_data["total_requests"]

            print(f"  {cell_key}: correctness={cell_data['correctness_match_rate']:.4f} "
                  f"({cell_data['correctness_match_count']}/{cell_data['total_requests']}), "
                  f"silent_fallbacks={cell_data['silent_fallback_count']}")

    # =========================================================================
    # PHASE 3: IDENTITY baselines (correctness oracle)
    # =========================================================================
    print("\n" + "=" * 70)
    print("PHASE 3: IDENTITY baselines (correctness oracle)")
    print("=" * 70)

    for size_name, target_size in TARGET_SIZES.items():
        for ct_name in CONTENT_TYPES.keys():
            identity_config = {
                "layers": [],
                "use_chunked": False,
                "chunk_size": 1024,
            }
            cell_key, cell_data = run_single_cell(
                port_idx, ct_name, f"IDENTITY-{size_name}", identity_config,
                target_size, auth_token, rng)
            port_idx += 1

            if cell_data is None:
                errors.append(f"{cell_key}: connectivity failed")
                continue

            all_results[cell_key] = cell_data
            total_correctness_pass += cell_data["correctness_match_count"]
            total_correctness_fail += (cell_data["total_requests"] - cell_data["correctness_match_count"])
            request_count += cell_data["total_requests"]

            print(f"  {cell_key}: correctness={cell_data['correctness_match_rate']:.4f} "
                  f"({cell_data['correctness_match_count']}/{cell_data['total_requests']})")

    # =========================================================================
    # CONTROLS
    # =========================================================================

    main_cells = {k: v for k, v in all_results.items()
                  if any(size in k for size in ["10240B", "102400B"])
                  and "IDENTITY" not in k}

    multi_layer_cells = {k: v for k, v in main_cells.items()
                         if any(mode in k for mode in MULTI_LAYER_MODES.keys())}

    regression_cells = {k: v for k, v in all_results.items()
                        if any(mode in k for mode in REGRESSION_MODES.keys())}

    identity_cells = {k: v for k, v in all_results.items() if "IDENTITY" in k}

    # C1: correctness_match_rate == 1.0 for ALL multi-layer cells
    all_main_correctness = all(
        v["correctness_match_rate"] == 1.0
        for v in main_cells.values()
    )
    all_multi_layer_correctness = all(
        v["correctness_match_rate"] == 1.0
        for v in multi_layer_cells.values()
    )

    all_controls["C_CORRECTNESS_MATCH"] = {
        "expected": "100% correctness match rate for ALL multi-layer cells (decompressed hash == expected hash)",
        "observed_multi_layer_cells": {k: v["correctness_match_rate"] for k, v in multi_layer_cells.items()},
        "observed_regression_cells": {k: v["correctness_match_rate"] for k, v in regression_cells.items()},
        "observed_identity_cells": {k: v["correctness_match_rate"] for k, v in identity_cells.items()},
        "pass_all_multi_layer": all_multi_layer_correctness,
        "pass_all_main": all_main_correctness,
        "pass_all_cells": all(v["correctness_match_rate"] == 1.0 for v in all_results.values()),
        "total_pass": total_correctness_pass,
        "total_fail": total_correctness_fail,
    }

    # C2: silent_fallback_count == 0 for ALL multi-layer cells
    total_silent_multi_layer = sum(v["silent_fallback_count"] for v in multi_layer_cells.values())
    all_controls["C_SILENT_FALLBACK"] = {
        "expected": "0 silent fallbacks for ALL compressed observations in multi-layer cells",
        "observed": {k: v["silent_fallback_count"] for k, v in multi_layer_cells.items()},
        "pass": total_silent_multi_layer == 0,
        "total_silent_fallbacks": total_silent_multi_layer,
    }

    # C3: Regression controls pass 100%
    regression_all_pass = all(
        v["correctness_match_rate"] == 1.0
        for v in regression_cells.values()
    )
    regression_gzip_pass = all(
        v["correctness_match_rate"] == 1.0
        for k, v in regression_cells.items() if "GZIP-SINGLE" in k
    )
    regression_brotli_pass = all(
        v["correctness_match_rate"] == 1.0
        for k, v in regression_cells.items() if "BROTLI-SINGLE" in k
    )
    all_controls["C_REGRESSION_CONTROLS"] = {
        "expected": "B-GZIP-SINGLE-LAYER-REGRESSION and B-BROTLI-SINGLE-LAYER-REGRESSION pass 100% (no pipeline regression)",
        "gzip_single": {k: v["correctness_match_rate"] for k, v in regression_cells.items() if "GZIP-SINGLE" in k},
        "brotli_single": {k: v["correctness_match_rate"] for k, v in regression_cells.items() if "BROTLI-SINGLE" in k},
        "pass_gzip": regression_gzip_pass,
        "pass_brotli": regression_brotli_pass,
        "pass_all": regression_all_pass,
    }

    # C4: IDENTITY baselines (correctness oracle validation)
    identity_all_pass = all(
        v["correctness_match_rate"] == 1.0
        for v in identity_cells.values()
    )
    all_controls["C_IDENTITY_BASELINE"] = {
        "expected": "IDENTITY baseline hash matches expected for 100% of observations",
        "observed": {k: v["correctness_match_rate"] for k, v in identity_cells.items()},
        "pass": identity_all_pass,
    }

    # C4 (null control): within-state determinism (B-RANDOM): all_same=true for all 4 auth states
    all_det = True
    det_details = defaultdict(list)
    for cell_key, cell_data in main_cells.items():
        for state in AUTH_STATES:
            if state in cell_data["decompressed_hash_variation"]:
                hv = cell_data["decompressed_hash_variation"][state]
                if not hv["all_same"]:
                    all_det = False
                det_details[state].append(hv["all_same"])

    all_controls["C_NULL_CONTROL"] = {
        "expected": "Within-state decompressed hash all_same=true for ALL 4 auth states across ALL multi-layer cells",
        "observed": {state: all(vals) for state, vals in det_details.items()},
        "pass": all_det,
    }

    # B-RANDOM baseline
    b_random_values = [cell_data["baselines"]["B-RANDOM"] for cell_data in main_cells.values()]
    c_b_random_pass = all(v is not None and abs(v) < 0.1 for v in b_random_values)
    all_controls["C_B_RANDOM"] = {
        "expected": "B-RANDOM ~ 0.0 for ALL multi-layer cells",
        "observed": [float(v) for v in b_random_values],
        "pass": c_b_random_pass,
    }

    # C5: B-COMPRESSED-TARGET-RANGE
    # At least 2 of 3 content types must achieve mean compressed_size_bytes >= 2000 at 10KB
    # and >= 5000 at 100KB
    compressed_target_results = {}
    for ct_name in CONTENT_TYPES:
        sizes_at_10k = []
        sizes_at_100k = []
        for cell_key, cell_data in multi_layer_cells.items():
            if cell_key.startswith(ct_name + "_"):
                if "10240B" in cell_key:
                    sizes_at_10k.append(cell_data["compressed_size_bytes"]["mean"])
                elif "102400B" in cell_key:
                    sizes_at_100k.append(cell_data["compressed_size_bytes"]["mean"])
        mean_10k = sum(sizes_at_10k) / len(sizes_at_10k) if sizes_at_10k else 0
        mean_100k = sum(sizes_at_100k) / len(sizes_at_100k) if sizes_at_100k else 0
        compressed_target_results[ct_name] = {
            "mean_compressed_10KB": mean_10k,
            "mean_compressed_100KB": mean_100k,
            "meets_10KB_threshold": mean_10k >= 2000,
            "meets_100KB_threshold": mean_100k >= 5000,
        }

    meets_10k_count = sum(1 for r in compressed_target_results.values() if r["meets_10KB_threshold"])
    meets_100k_count = sum(1 for r in compressed_target_results.values() if r["meets_100KB_threshold"])
    compressed_target_pass = meets_10k_count >= 2 and meets_100k_count >= 2

    all_controls["B_COMPRESSED_TARGET_RANGE"] = {
        "expected": "At least 2/3 content types achieve mean compressed_size_bytes >= 2000 at 10KB AND >= 5000 at 100KB",
        "per_content_type": compressed_target_results,
        "types_meeting_10KB_threshold": meets_10k_count,
        "types_meeting_100KB_threshold": meets_100k_count,
        "pass": compressed_target_pass,
    }

    all_controls["C_NO_ERRORS"] = {
        "expected": "0 decompression errors (exceptions + silent fallbacks) across ALL requests",
        "total_exceptions": total_decompression_errors,
        "total_silent_fallbacks": total_silent_fallbacks,
        "pass": total_decompression_errors == 0 and total_silent_fallbacks == 0,
    }

    # =========================================================================
    # DECISION RULE (from frozen spec)
    # =========================================================================

    # SURVIVES_CURRENT_TEST requires ALL of:
    # C1: correctness_match_rate == 1.0 for ALL multi-layer cells
    c1_pass = all_multi_layer_correctness
    # C2: silent_fallback_count == 0 for ALL multi-layer cells
    c2_pass = total_silent_multi_layer == 0
    # C3: regression controls pass 100%
    c3_pass = regression_all_pass
    # C4: null_control passes (all_same=true for all states in all multi-layer cells)
    c4_pass = all_det
    # C5: B-COMPRESSED-TARGET-RANGE passes
    c5_pass = compressed_target_pass

    # Check MEASUREMENT_INVALID
    measurement_invalid = len(all_results) == 0 or (total_correctness_pass + total_correctness_fail == 0)
    oracle_invalid = not identity_all_pass

    if measurement_invalid or oracle_invalid:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    elif not c5_pass:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    elif c1_pass and c2_pass and c3_pass and c4_pass and c5_pass:
        status = "COMPLETE"
        outcome = "SUPPORTS"
    elif not c1_pass or not c2_pass:
        status = "COMPLETE"
        outcome = "FALSIFIES"
    elif not c3_pass:
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
            f"{cell_key}: correctness_rate={cell_data['correctness_match_rate']:.4f} "
            f"({cell_data['correctness_match_count']}/{cell_data['total_requests']}), "
            f"silent_fallbacks={cell_data['silent_fallback_count']}, "
            f"compressed_size={cell_data['compressed_size_bytes']['mean']:.0f}B, "
            f"decomp_latency={cell_data['decompression_latency_ms']['mean']:.1f}ms"
        )

    # Entropy observations
    for ct_name, ent_data in entropy_results.items():
        all_observations.append(
            f"Entropy {ct_name}: mean={ent_data['mean_entropy']:.4f} "
            f"min={ent_data['min_entropy']:.4f} max={ent_data['max_entropy']:.4f}"
        )

    # =========================================================================
    # VALIDITY NOTES
    # =========================================================================

    all_validity_notes.extend([
        "Architecture: Client (iterative decompression, max_depth=5) -> Python Reverse Proxy -> Mock OAuth2 Server",
        f"Main experimental cells: {len(main_cells)} cells (2 sizes x 3 types x 2 multi-layer encodings)",
        f"Multi-layer encodings: GZIP-THEN-BROTLI (gzip level=1 -> brotli quality=4), BROTLI-THEN-GZIP (brotli quality=4 -> gzip level=1)",
        f"Regression controls: {len(regression_cells)} cells (single-layer, 10KB)",
        f"IDENTITY baselines: {len(identity_cells)} cells (correctness oracle at 10KB and 100KB)",
        f"Python version: {sys.version}",
        f"Seed={SEED} for request ordering and body generation",
        "Jitter: 50-150ms uniform between requests",
        "No real CDN infrastructure - bounded to localhost mock server + Python reverse proxy",
        "High-entropy body generation: unique UUIDs, random floats, varied content per state",
        f"Shannon entropy minimum threshold: {SHANNON_ENTROPY_MIN} bits/byte",
        f"chunk_size=32 for all compressed conditions (multi-chunk framing)",
        f"10KB payloads: multi-layer compressed sizes expected ~2-10KB spanning 60-300+ chunks at chunk_size=32",
        f"100KB payloads: multi-layer compressed sizes expected ~20-99KB spanning 600-3000+ chunks at chunk_size=32",
        "Multi-layer encodings exercise max_depth>1: iterative decompression must unwrap two layers",
    ])

    if total_decompression_errors > 0:
        all_validity_notes.append(f"Pipeline errors: {total_decompression_errors} decompression errors")
    if total_silent_fallbacks > 0:
        all_validity_notes.append(f"Silent fallbacks detected: {total_silent_fallbacks}")
    if errors:
        all_validity_notes.append(f"Infrastructure errors: {errors}")

    # =========================================================================
    # UNRESOLVED
    # =========================================================================

    unresolved = [
        "Does decompression correctness hold on real CDN infrastructure (Cloudflare/Fastly/Akamai) with high-entropy payloads?",
        "Does correctness hold for streaming incremental decompression across chunk boundaries without full reassembly?",
        "What is decompression latency at realistic compressed sizes (20-99KB) on real network infrastructure?",
        "Does high-entropy payload correctness hold for payloads beyond 100KB nominal?",
        "Do gzip levels 2-8 and brotli qualities 5-7 produce compressed structures that stress chunk boundaries differently?",
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
            "per_cell": {k: {kk: vv for kk, vv in v.items() if kk != "observations"} for k, v in all_results.items()},
            "aggregate": {
                "total_correctness_pass": total_correctness_pass,
                "total_correctness_fail": total_correctness_fail,
                "total_silent_fallbacks": total_silent_fallbacks,
                "total_decompression_errors": total_decompression_errors,
                "total_requests": request_count,
                "overall_correctness_rate": total_correctness_pass / (total_correctness_pass + total_correctness_fail) if (total_correctness_pass + total_correctness_fail) > 0 else 0,
                "main_cells_count": len(main_cells),
                "multi_layer_cells_count": len(multi_layer_cells),
                "regression_cells_count": len(regression_cells),
                "identity_cells_count": len(identity_cells),
            },
            "M_ENTROPY_SHANNON": {
                "per_content_type": {
                    ct_name: {
                        "mean_entropy_bits_per_byte": ent_data["mean_entropy"],
                        "min_entropy_bits_per_byte": ent_data["min_entropy"],
                        "max_entropy_bits_per_byte": ent_data["max_entropy"],
                        "all_above_threshold": ent_data["all_above_threshold"],
                    }
                    for ct_name, ent_data in entropy_results.items()
                },
                "threshold_bits_per_byte": SHANNON_ENTROPY_MIN,
                "pass": all(ent_data["all_above_threshold"] for ent_data in entropy_results.values()),
            },
            "B_COMPRESSED_TARGET_RANGE": {
                "per_content_type": compressed_target_results,
                "types_meeting_10KB_threshold": meets_10k_count,
                "types_meeting_100KB_threshold": meets_100k_count,
                "pass": compressed_target_pass,
            },
        },
        "controls": all_controls,
        "artifacts": [
            {"path": "run_experiment.py", "role": "code",
             "description": "Experiment execution script with mock origin, reverse proxy, high-entropy payload generators, multi-layer encoding support, and decompression correctness controls"},
        ],
        "observations": all_observations,
        "validity_notes": all_validity_notes,
        "unresolved": unresolved,
    }

    return result


def build_measurement_invalid_result(reason, entropy_results=None):
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": "MEASUREMENT_INVALID",
        "outcome": "NOT_APPLICABLE",
        "metrics": {
            "M_ENTROPY_SHANNON": {
                "per_content_type": {
                    ct_name: {
                        "mean_entropy_bits_per_byte": ent_data["mean_entropy"],
                        "min_entropy_bits_per_byte": ent_data["min_entropy"],
                        "max_entropy_bits_per_byte": ent_data["max_entropy"],
                        "all_above_threshold": ent_data["all_above_threshold"],
                    }
                    for ct_name, ent_data in (entropy_results or {}).items()
                },
                "threshold_bits_per_byte": SHANNON_ENTROPY_MIN,
                "pass": False,
            } if entropy_results else {},
        },
        "controls": {},
        "artifacts": [],
        "observations": [],
        "validity_notes": [f"MEASUREMENT_INVALID: {reason}"],
        "unresolved": [reason],
    }


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
