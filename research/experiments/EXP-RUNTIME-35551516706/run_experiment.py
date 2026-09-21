#!/usr/bin/env python3
"""
EXP-RUNTIME-35551516706 -- EXECUTE (frozen spec.json / prereg.md / freeze.json).

Frozen question: On a local nginx caching reverse proxy that produces real
cache HIT responses, does oracle-free greedy iterative decompression produce
byte-identical output to ground truth for cached (stale) responses, and does
the decompressed output differ from the DYNAMIC-path decompressed output?

Frozen algorithm (prereg section 7): oracle-free greedy decode -- try brotli,
then gzip, until neither succeeds (MAX_DEPTH=5), NO SHA256 oracle.

RAW EVIDENCE (response body bytes incl. base64 + headers + status) is kept
distinct from DERIVED MEASUREMENTS (decompressed SHAs, correct booleans,
decode methods, ambiguous flags) in every JSONL row:
{"raw": {...}, "derived": {...}}.

Phases (frozen prereg):
  Phase 0: infrastructure validation (nginx -v/-t, origin up, warm-up >=1 HIT)
  Phase 1: origin ground truth + B-LOCALHOST-DIRECT positive control (48x5)
  Phase 2: DYNAMIC path through nginx (cache-busting unique URL, MISS) 48x5
  Phase 3: HIT path through nginx (fixed URL populate+test, N=5) 48x5 -> 240 HIT obs
  Phase 4: C8 DYNAMIC-vs-HIT wire-byte identity (last rep per cell)
  Phase 5: C3 cache stability (6 groups x 3 consecutive) + C4 identity (15 obs)
  Phase 6: C5 depth 3-5 stacked encodings through nginx cache
  Phase 7: C6 large >100KB payloads through nginx cache
  Phase 8: B-ORACLE-GUIDED-REGRESSION and B-FIXED-ORDER-CDN on same wire bytes

Parent payload-generation protocol (EXP-RUNTIME-35544804817) reused exactly:
SEED=44, AUTH_STATE=valid_token, TARGET_SIZE=10240, high-entropy bodies,
ORDERS {GZIP-OUTER, BROTLI-OUTER}, CHUNK_SIZES {8192,32}, 4 AE variants.
"""
import binascii
import base64
import brotli
import gzip
import hashlib
import http.client
import http.server
import io
import json
import math
import os
import pathlib
import random
import re
import struct
import subprocess
import sys
import threading
import time
import urllib.parse
import uuid

HERE = pathlib.Path(__file__).parent
EXPERIMENT_ID = "EXP-RUNTIME-35551516706"
LANE = "runtime"
SEED = 44
REPS = 5
MAX_DEPTH = 5
TARGET_SIZE = 10240
LARGE_TARGET = 150000
ORIGIN_PORT = 18794
NGINX_PORT = 18080
NGINX_CONF_TMP = pathlib.Path("/tmp/opencode/exp35551516706_nginx.conf")
NGINX_PREFIX = pathlib.Path("/tmp/opencode/exp35551516706_nginx_root")
ROWS_PATH = HERE / "raw_cell_results.jsonl"
MANIFEST_PATH = HERE / "payload_manifest.json"
SUMMARY_PATH = HERE / "summary.json"
HVD_PATH = HERE / "hit_vs_dynamic.json"
NGINX_CONF_ARTIFACT = HERE / "nginx_cache.conf"
RUN_LOG = HERE / "run.log"

CONTENT_TYPES = {"JSON": "application/json", "HTML": "text/html",
                 "BINARY": "application/octet-stream"}
ORDERS = {
    "GZIP-OUTER": ([{"type": "brotli", "quality": 4}, {"type": "gzip", "level": 1}], "gzip"),
    "BROTLI-OUTER": ([{"type": "gzip", "level": 1}, {"type": "brotli", "quality": 4}], "br"),
}
CHUNK_SIZES = [8192, 32]
AE_VARIANTS = {"none": None, "gzip": "gzip", "br": "br", "both": "gzip, br"}
AUTH_STATE = "valid_token"

HTML_WORDS = [
    "quantum", "nebula", "algorithm", "synthesis", "morphology", "topology",
    "paradigm", "entropy", "syntactic", "recursive", "distributed",
    "asynchronous", "vector", "scalar", "heuristic", "stochastic",
    "orthogonal", "polymorphic", "isomorphic", "homomorphic",
    "cryptographic", "probabilistic", "steganographic", "metamorphic",
    "quantitative", "longitudinal", "multivariate", "dimensional",
    "resonance", "catalyst", "substrate", "amplitude", "frequency",
    "spectral", "turbulent", "viscous", "lamellar", "ferromagnetic",
    "piezoelectric", "superconductor", "semiconductor", "photoelectric",
    "thermodynamic", "electromagnetic", "gravitational", "chromatic",
    "diffraction", "interference", "polarization", "refraction",
    "scattering", "absorption", "emission", "fluorescence",
    "phosphorescence", "luminescence", "bioluminescence", "chromatography",
    "spectroscopy", "microscopy", "crystallography", "algorithmic",
    "heuristic", "deterministic", "stochastic", "Bayesian", "Gaussian",
    "Poisson", "Markovian", "Eulerian", "Lagrangian", "Hilbert", "Fourier",
    "Laplace", "Riemann", "Euclidean", "Riemannian", "manifold", "bundle",
    "morphism", "functor", "category", "groupoid", "semigroup", "monoid",
    "lattice", "poset", "topology", "homology", "cohomology", "homotopy",
    "sheaf", "presheaf", "differential", "geodesic", "curvature", "tensor",
    "matrix", "polynomial", "eigenvalue",
]


def compute_shannon_entropy(data):
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


def _he_seed(state, content_type, target_size):
    seed_str = f"{state}:{content_type}:{target_size}:he_seed"
    digest = hashlib.sha256(seed_str.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big")


def generate_json_he_body(state, target_size):
    rng = random.Random(_he_seed(state, "JSON", target_size))
    entries = []
    current_size = 0
    while current_size < target_size:
        uuid_val = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{state}:{rng.getrandbits(64)}"))
        entry = {"sub": uuid_val, "name": " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(2, 4))),
                 "email": f"{uuid_val[:8]}@{rng.choice(HTML_WORDS)}.example.com",
                 "scope": " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(2, 6))),
                 "score": round(rng.uniform(-1000.0, 1000.0), 6),
                 "tag": f"tag_{rng.randint(0, 999999):06d}",
                 "desc": " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(4, 12))),
                 "active": rng.choice([True, False]),
                 "nested": {"x": round(rng.uniform(0.0, 1.0), 8), "y": rng.getrandbits(32), "z": uuid_val}}
        entry_bytes = json.dumps(entry).encode("utf-8")
        if current_size + len(entry_bytes) + 1 > target_size:
            break
        entries.append(entry)
        current_size += len(entry_bytes) + 1
    raw = json.dumps({"sub": "alice", "name": "Alice", "entries": entries},
                     separators=(",", ":")).encode("utf-8")
    if len(raw) < target_size:
        pad = bytes(rng.getrandbits(8) for _ in range(target_size - len(raw)))
        raw = raw + pad[:target_size - len(raw)]
    return raw[:target_size]


def generate_html_he_body(state, target_size):
    rng = random.Random(_he_seed(state, "HTML", target_size))
    sections = ["<!DOCTYPE html>", '<html lang="en">', "<head>",
                '<meta charset="UTF-8">',
                f"<title>High-Entropy Document - {state}</title>", "</head>",
                "<body>", f'<div class="auth-state" data-state="{state}">']
    section_id = 0
    current_size = sum(len(s.encode("utf-8")) for s in sections)
    while current_size < target_size:
        uuid_val = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{state}:{rng.getrandbits(64)}"))
        words = [rng.choice(HTML_WORDS) for _ in range(rng.randint(20, 60))]
        paragraph = " ".join(words) + "."
        header_text = " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(3, 6))).title()
        hlevel = rng.randint(2, 4)
        section = (f'<section id="s{section_id}" data-uuid="{uuid_val}">\n'
                   f"<h{hlevel}>{header_text}</h{hlevel}>\n<p>{paragraph}</p>\n<p>"
                   + " ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(15, 40)))
                   + ".</p>\n</section>\n")
        section_bytes = section.encode("utf-8")
        if current_size + len(section_bytes) > target_size:
            break
        sections.append(section)
        current_size += len(section_bytes)
        section_id += 1
    sections.extend(["</div>", "</body>", "</html>"])
    raw = "\n".join(sections).encode("utf-8")
    if len(raw) < target_size:
        pad_words = []
        while sum(len(w.encode("utf-8")) + 1 for w in pad_words) < target_size - len(raw):
            pad_words.append(rng.choice(HTML_WORDS))
        padding = (" ".join(pad_words)).encode("utf-8")[:target_size - len(raw)]
        raw = raw + padding
    return raw[:target_size]


def generate_binary_he_body(state, target_size):
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
        raw += struct.pack(">I", binascii.crc32(entry) & 0xFFFFFFFF)
    if len(raw) < target_size:
        pad = bytes(rng.getrandbits(8) for _ in range(target_size - len(raw)))
        raw = raw + pad[:target_size - len(raw)]
    return raw[:target_size]


BODY_GENERATORS = {"JSON": generate_json_he_body, "HTML": generate_html_he_body,
                   "BINARY": generate_binary_he_body}


def compress_layers(body, layers_inner_first):
    data = body
    for layer in layers_inner_first:
        if layer["type"] == "gzip":
            data = gzip.compress(data, compresslevel=layer.get("level", 6))
        elif layer["type"] == "brotli":
            data = brotli.compress(data, quality=layer.get("quality", 6))
    return data


def fullbody_decompress(data):
    current = data
    depth = 0
    while depth < MAX_DEPTH:
        try:
            current = brotli.decompress(current)
            depth += 1
            continue
        except Exception:
            pass
        try:
            current = gzip.decompress(current)
            depth += 1
            continue
        except Exception:
            pass
        break
    return current


# ======================================================================
# ORACLE-FREE GREEDY DECODE (frozen per prereg section 7)
# NO SHA256 check at any point -- identical to parent EXP-RUNTIME-35544804817
# ======================================================================
def oracle_free_greedy_decode(raw_bytes):
    """Try brotli -> gzip until neither succeeds. Returns (decoded, method, ambiguous)."""
    current = raw_bytes
    path = []
    ambiguous = False
    for depth in range(MAX_DEPTH):
        br_result = None
        gz_result = None
        try:
            br_result = brotli.decompress(current)
        except Exception:
            pass
        try:
            gz_result = gzip.decompress(current)
        except Exception:
            pass
        if br_result is not None and gz_result is not None:
            ambiguous = True
            path.append("br")
            current = br_result
        elif br_result is not None:
            path.append("br")
            current = br_result
        elif gz_result is not None:
            path.append("gz")
            current = gz_result
        else:
            break
    method = "+".join(path) if path else "identity"
    return current, method, ambiguous


# ======================================================================
# ORACLE-GUIDED DECODE (regression baseline B-ORACLE-GUIDED-REGRESSION;
# identical to parent EXP-RUNTIME-35542474231 encoding_agnostic_decode)
# ======================================================================
def oracle_guided_decode(raw_bytes, ground_truth_sha256):
    current = raw_bytes
    path = []
    for depth in range(MAX_DEPTH):
        if hashlib.sha256(current).hexdigest() == ground_truth_sha256:
            method = "+".join(path) if path else "identity"
            return current, method
        try:
            decoded = brotli.decompress(current)
            path.append("br")
            current = decoded
            continue
        except Exception:
            pass
        try:
            decoded = gzip.decompress(current)
            path.append("gz")
            current = decoded
            continue
        except Exception:
            pass
        if hashlib.sha256(current).hexdigest() == ground_truth_sha256:
            method = "+".join(path) if path else "identity"
            return current, method
        break
    if hashlib.sha256(current).hexdigest() == ground_truth_sha256:
        method = "+".join(path) if path else "identity"
        return current, method
    return None, None


# ======================================================================
# FIXED-ORIGIN-ORDER DECODE (baseline B-FIXED-ORDER-CDN; parent framing
# assumption: response bytes follow origin layer order + served CE
# ======================================================================
def streaming_unwrap_one(data, enc_type, chunk_size):
    if enc_type in ("brotli", "br"):
        d = brotli.Decompressor()
        parts = []
        for i in range(0, len(data), chunk_size):
            r = d.process(data[i:i + chunk_size])
            if r:
                parts.append(r)
        return b"".join(parts)
    elif enc_type == "gzip":
        buf = io.BytesIO(data)
        gz = gzip.GzipFile(fileobj=buf)
        parts = []
        while True:
            piece = gz.read(chunk_size)
            if not piece:
                break
            parts.append(piece)
        return b"".join(parts)
    elif enc_type in ("identity", ""):
        return data
    raise ValueError(f"unknown encoding {enc_type}")


def streaming_decompress_multi_layer(data, layers_inner_first, chunk_size):
    out = data
    for layer in reversed(layers_inner_first):
        out = streaming_unwrap_one(out, layer["type"], chunk_size)
    return out# ======================================================================
# ORIGIN SERVER (reused parent protocol: serves pre-compressed bodies per
# path token, ignores Accept-Encoding, Cache-Control: public, max-age=300)
# ======================================================================
TOKEN_RE = re.compile(r"^/(m|cache|dy|id|depth|large|stab|iden)/([A-Za-z0-9_.-]+)(\?.*)?$")


class OriginHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "SPIDER-Origin/1.0"

    def do_GET(self):
        match = TOKEN_RE.match(self.path)
        if match is None:
            self.send_error(404, "not found")
            return
        token = match.group(2)
        if token not in self.server.serve:
            self.send_error(404, "unknown token")
            return
        entry = self.server.serve[token]
        body = entry["compressed"]
        self.send_response(200)
        self.send_header("Content-Type", entry["content_type"])
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=300")
        if entry.get("content_encoding"):
            self.send_header("Content-Encoding", entry["content_encoding"])
        self.send_header("X-Origin-Token", token)
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


class ThreadingOrigin(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, addr, serve):
        self.serve = serve
        super().__init__(addr, OriginHandler)


# ======================================================================
# RAW HTTP CLIENT (captures exact response bytes + headers + status)
# ======================================================================
def raw_get(host, port, path, headers, timeout=20.0):
    start = time.monotonic()
    conn = http.client.HTTPConnection(host, port, timeout=timeout)
    try:
        conn.request("GET", path, headers=headers)
        resp = conn.getresponse()
        status = resp.status
        resp_headers = {k.lower(): v for k, v in resp.getheaders()}
        body = resp.read()
        conn.close()
        elapsed_ms = (time.monotonic() - start) * 1000.0
        return status, resp_headers, body, elapsed_ms, None
    except Exception as exc:  # transport failure -- NEVER conflated with scientific result
        elapsed_ms = (time.monotonic() - start) * 1000.0
        return None, {}, b"", elapsed_ms, f"{type(exc).__name__}: {exc}"


# ======================================================================
# PAYLOAD REGISTRY (48-cell matrix + depth + large + identity + stability)
# ======================================================================
class PayloadRegistry:
    def __init__(self):
        self.manifest = {}
        self.serve = {}
        self.cells = []
        self.pkeys = []
        self._rng = random.Random(SEED + 1)

    def _register(self, pkey, body, content_type, layers_inner_first, compressed,
                  content_encoding, tag, depth=None, target_size=None):
        plain_sha = hashlib.sha256(body).hexdigest()
        comp_sha = hashlib.sha256(compressed).hexdigest()
        gt = fullbody_decompress(compressed)
        gt_sha = hashlib.sha256(gt).hexdigest()
        entry = {
            "pkey": pkey, "content_type": content_type, "plain_len": len(body),
            "plain_sha256": plain_sha, "comp_len": len(compressed),
            "comp_sha256": comp_sha, "layers_inner_first": layers_inner_first,
            "content_encoding": content_encoding, "tag": tag,
            "depth": depth, "target_size": target_size,
            "entropy": round(compute_shannon_entropy(body), 6),
            "gt_sha256": gt_sha, "gt_is_plain": gt == body,
        }
        self.manifest[pkey] = entry
        self.serve[pkey] = {"compressed": compressed, "content_type": content_type,
                            "content_encoding": content_encoding, "comp_sha256": comp_sha}
        self.pkeys.append(pkey)
        return entry

    def build(self):
        """Build all payloads deterministically. Persist manifest + serve-table."""
        for ct in CONTENT_TYPES:
            for ok, (layers, ce) in ORDERS.items():
                for cs in CHUNK_SIZES:
                    body_fragment = None
                    for ae_key, ae_val in AE_VARIANTS.items():
                        pkey = f"{ct}_{ok}_C{cs}_{ae_key}"
                        if body_fragment is None:
                            body = BODY_GENERATORS[ct](AUTH_STATE, TARGET_SIZE)
                            body_fragment = body
                        else:
                            body = body_fragment
                        compressed = compress_layers(body, layers)
                        self._register(pkey, body, CONTENT_TYPES[ct], layers, compressed,
                                       ce if ae_val is not None else None,
                                       f"primary-{ok}-C{cs}-AE-{ae_key}",
                                       target_size=TARGET_SIZE)
                        self.cells.append(pkey)
        # depth payloads (C5): 3 types x depths 3,4,5
        for ct in CONTENT_TYPES:
            for depth in (3, 4, 5):
                pkey = f"{ct}_DEPTH{depth}"
                body = BODY_GENERATORS[ct](AUTH_STATE, TARGET_SIZE)
                layers = [{"type": "brotli", "quality": 4}] * depth
                layers = [{"type": "gzip", "level": 1} if i % 2 else {"type": "brotli", "quality": 4}
                          for i in range(depth)]
                compressed = compress_layers(body, layers)
                self._register(pkey, body, CONTENT_TYPES[ct], layers, compressed,
                               "br" if depth % 2 else "gzip", f"depth-{depth}",
                               depth=depth, target_size=TARGET_SIZE)
        # large payloads (C6): 3 types x 2 orders, >100KB
        for ct in CONTENT_TYPES:
            for ok, (layers, ce) in ORDERS.items():
                pkey = f"{ct}_LARGE_{ok}"
                body = BODY_GENERATORS[ct](AUTH_STATE, LARGE_TARGET)
                compressed = compress_layers(body, layers)
                self._register(pkey, body, CONTENT_TYPES[ct], layers, compressed, ce,
                               f"large-{ok}", target_size=LARGE_TARGET)
        # identity payloads (C4): uncompressed
        for ct in CONTENT_TYPES:
            pkey = f"{ct}_IDENTITY"
            body = BODY_GENERATORS[ct](AUTH_STATE, TARGET_SIZE)
            self._register(pkey, body, CONTENT_TYPES[ct], [], body, None, "identity",
                           target_size=TARGET_SIZE)
        # stability groups (C3): 2 JSON + 2 HTML + 1 binary + 1 large
        stab_keys = [("JSON", "GZIP-OUTER", TARGET_SIZE), ("JSON", "BROTLI-OUTER", TARGET_SIZE),
                     ("HTML", "GZIP-OUTER", TARGET_SIZE), ("HTML", "BROTLI-OUTER", TARGET_SIZE),
                     ("BINARY", "GZIP-OUTER", TARGET_SIZE), ("JSON", "GZIP-OUTER", LARGE_TARGET)]
        for i, (ct, ok, tsize) in enumerate(stab_keys, start=1):
            pkey = f"STAB_{i}_{ct}_{ok}"
            body = BODY_GENERATORS[ct](AUTH_STATE, tsize)
            layers, ce = ORDERS[ok]
            compressed = compress_layers(body, layers)
            self._register(pkey, body, CONTENT_TYPES[ct], layers, compressed, ce,
                           f"stability-{i}", target_size=tsize)


# ======================================================================
# ROW/AUDIT UTILITIES
# ======================================================================
class RowWriter:
    def __init__(self, path):
        self.path = path
        self.fh = open(path, "w", encoding="utf-8")
        self.rows = []
        self.seen_keys = set()
        self.duplicates = []

    def write(self, session_kind, cell, rep, payload_key, phase, url,
              accept_encoding, raw, derived):
        key = (session_kind, cell, rep)
        if key in self.seen_keys:
            self.duplicates.append(key)
        self.seen_keys.add(key)
        row = {
            "experiment_id": EXPERIMENT_ID,
            "lane": LANE,
            "phase": phase,
            "session_kind": session_kind,
            "cell": cell,
            "rep": rep,
            "payload_key": payload_key,
            "url": url,
            "accept_encoding": accept_encoding,
            "raw": raw,
            "derived": derived,
        }
        self.rows.append(row)
        self.fh.write(json.dumps(row) + "\n")

    def all_rows(self):
        return self.rows

    def close(self):
        self.fh.close()


def make_raw(status, resp_headers, body, elapsed_ms, transport_error):
    return {
        "status": status,
        "headers": resp_headers,
        "body_sha256": hashlib.sha256(body).hexdigest() if body else None,
        "body_b64": base64.b64encode(body).decode("ascii") if body else "",
        "body_len": len(body),
        "elapsed_ms": round(elapsed_ms, 3),
        "transport_error": transport_error,
    }


def make_derived(gt, plain_sha, raw_body):
    """Compute all three decoders over the SAME raw wire bytes."""
    if not raw_body or gt is None:
        return {
            "oracle_free_sha256": None, "oracle_free_correct": None,
            "oracle_free_method": None, "oracle_free_ambiguous": None,
            "oracle_free_error": "no wire bytes",
            "oracle_guided_correct": None, "oracle_guided_method": None,
            "fixed_order_correct": None, "fixed_order_method": None,
        }
    of_body, of_method, of_ambiguous = oracle_free_greedy_decode(raw_body)
    of_sha = hashlib.sha256(of_body).hexdigest()
    og_body, og_method = oracle_guided_decode(raw_body, gt["gt_sha256"])
    try:
        fixed_body = streaming_decompress_multi_layer(
            raw_body, gt["layers_inner_first"], 8192 if gt["depth"] is None else gt["target_size"] or 8192)
        fixed_sha = hashlib.sha256(fixed_body).hexdigest()
        fixed_correct = fixed_sha == plain_sha
    except Exception as exc:
        fixed_correct = False
        fixed_sha = None
    return {
        "oracle_free_sha256": of_sha,
        "oracle_free_correct": of_sha == plain_sha,
        "oracle_free_method": of_method,
        "oracle_free_ambiguous": of_ambiguous,
        "oracle_free_error": None,
        "oracle_guided_sha256": hashlib.sha256(og_body).hexdigest() if og_body else None,
        "oracle_guided_correct": bool(og_body),
        "oracle_guided_method": og_method,
        "fixed_order_sha256": fixed_sha,
        "fixed_order_correct": fixed_correct,
        "fixed_order_method": None,
    }


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(RUN_LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")# ======================================================================
# NGINX CACHE PROXY HARNESS (frozen prereg section 6)
# ======================================================================
NGINX_CONF_TEMPLATE = """worker_processes 1;
error_log {prefix}/logs/error.log warn;
pid {prefix}/logs/nginx.pid;
events {{ worker_connections 128; }}
http {{
    access_log off;
    gzip off;
    proxy_cache_path {prefix}/cache levels=1:2 keys_zone=spider:16m max_size=512m inactive=10m use_temp_path=off;
    server {{
        listen 127.0.0.1:{nginx_port};
        server_name localhost;
        location / {{
            proxy_pass http://127.0.0.1:{origin_port};
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header Connection "";
            proxy_cache spider;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 5m;
            proxy_buffering on;
            add_header X-Cache $upstream_cache_status always;
        }}
    }}
}}
"""


def write_nginx_conf(prefix, nginx_port, origin_port, relaxed=False):
    conf = NGINX_CONF_TEMPLATE.format(prefix=prefix, nginx_port=nginx_port,
                                      origin_port=origin_port)
    if relaxed:
        conf = conf.replace("proxy_cache_valid 200 5m;",
                            "proxy_cache_valid 200 5m;\n            proxy_ignore_headers Cache-Control Expires Set-Cookie;")
    NGINX_CONF_TMP.write_text(conf, encoding="utf-8")
    NGINX_CONF_ARTIFACT.write_text(conf, encoding="utf-8")
    return NGINX_CONF_TMP


def nginx_run(args, timeout=30):
    return subprocess.run(["/usr/sbin/nginx", "-p", str(NGINX_PREFIX), *args],
                          capture_output=True, text=True, timeout=timeout)


def start_nginx():
    (NGINX_PREFIX / "logs").mkdir(parents=True, exist_ok=True)
    (NGINX_PREFIX / "cache").mkdir(parents=True, exist_ok=True)
    r = nginx_run(["-t", "-c", str(NGINX_CONF_TMP)])
    if r.returncode != 0:
        return False, r.stdout + r.stderr
    r = nginx_run(["-c", str(NGINX_CONF_TMP)])
    if r.returncode != 0:
        return False, r.stdout + r.stderr
    return True, r.stdout + r.stderr


def stop_nginx():
    nginx_run(["-s", "quit"], timeout=15)
    time.sleep(0.5)


# ======================================================================
# PHASE IMPLEMENTATIONS
# ======================================================================
ORIGIN_BASE = f"http://127.0.0.1:{ORIGIN_PORT}"
PROXY_BASE = f"http://127.0.0.1:{NGINX_PORT}"


def cell_ae(cell):
    """Accept-Encoding variant for a primary cell (cell name ends with ae_key)."""
    ae_key = cell.rsplit("_", 1)[-1]
    return AE_VARIANTS.get(ae_key)


def phase0_infra(rows, registry):
    """Infrastructure validation: nginx -v/-t, origin up, warm-up >=1 HIT."""
    log("PHASE 0: infrastructure validation")
    results = {"nginx_version": None, "nginx_t": None, "origin_up": False,
               "warmup_count": 0, "warmup_hits": 0}
    try:
        r = subprocess.run(["/usr/sbin/nginx", "-v"], capture_output=True, text=True, timeout=15)
        results["nginx_version"] = (r.stdout + r.stderr).strip()
    except Exception as exc:
        results["nginx_version"] = f"error: {exc}"
    # origin smoke test
    pkey = registry.pkeys[0]
    gt = registry.manifest[pkey]
    status, hdrs, body, ms, terr = raw_get("127.0.0.1", ORIGIN_PORT, f"/m/{pkey}", {})
    results["origin_up"] = status == 200 and not terr
    # start nginx
    ok, out = start_nginx()
    results["nginx_t"] = out.strip()
    if not ok:
        return results, False
    time.sleep(0.5)
    # warm-up: 10 consecutive GETs to the SAME fixed URL -> expect HITs
    warm_token = f"{pkey}_WARM"
    registry.serve[warm_token] = registry.serve[pkey]
    for i in range(10):
        status, hdrs, body, ms, terr = raw_get("127.0.0.1", NGINX_PORT, f"/cache/{warm_token}", {})
        results["warmup_count"] += 1
        xcache = hdrs.get("x-cache")
        if xcache and xcache.upper() == "HIT":
            results["warmup_hits"] += 1
        raw = make_raw(status, hdrs, body, ms, terr)
        derived = make_derived(gt, gt["plain_sha256"], body if not terr else b"")
        rows.write("WARMUP", "warmup-10x", i, warm_token, "phase0",
                   f"/cache/{warm_token}", None, raw, derived)
    log(f"PHASE 0: nginx={results['nginx_version']!r} origin_up={results['origin_up']} "
        f"warmup_hits={results['warmup_hits']}/10")
    return results, results["warmup_hits"] >= 1


def phase1_localhost_direct(rows, registry):
    """B-LOCALHOST-DIRECT positive control: origin direct, 48 cells x 5."""
    log("PHASE 1: B-LOCALHOST-DIRECT (origin ground truth, 48x5=240)")
    counts = {"total": 0, "correct": 0}
    for cell in registry.cells:
        gt = registry.manifest[cell]
        headers = {"User-Agent": "SPIDER-R2/1.0"}
        ae = cell_ae(cell)
        if ae:
            headers["Accept-Encoding"] = ae
        for rep in range(REPS):
            status, hdrs, body, ms, terr = raw_get("127.0.0.1", ORIGIN_PORT, f"/m/{cell}", headers)
            raw = make_raw(status, hdrs, body, ms, terr)
            derived = make_derived(gt, gt["plain_sha256"], body if not terr else b"")
            rows.write("LOCALHOST", cell, rep, cell, "phase1", f"/m/{cell}", ae, raw, derived)
            counts["total"] += 1
            if derived["oracle_free_correct"] and not terr:
                counts["correct"] += 1
    log(f"PHASE 1: oracle-free correct {counts['correct']}/{counts['total']}")
    return counts


def phase2_dynamic(rows, registry):
    """DYNAMIC path through nginx: unique cache-busting URL per request (MISS).
    Frozen: 48 cells x 5 = 240 observations."""
    log("PHASE 2: DYNAMIC path through nginx (48x5=240, cache-busted URLs)")
    counts = {"total": 0, "correct": 0, "miss": 0, "hit": 0}
    for cell in registry.cells:
        gt = registry.manifest[cell]
        headers = {"User-Agent": "SPIDER-R2/1.0"}
        ae = cell_ae(cell)
        if ae:
            headers["Accept-Encoding"] = ae
        for rep in range(REPS):
            cb = uuid.uuid4().hex
            path = f"/dy/{cell}?cb={cb}"
            status, hdrs, body, ms, terr = raw_get("127.0.0.1", NGINX_PORT, path, headers)
            raw = make_raw(status, hdrs, body, ms, terr)
            derived = make_derived(gt, gt["plain_sha256"], body if not terr else b"")
            xcache = (hdrs.get("x-cache") or "?").upper()
            if xcache == "HIT":
                counts["hit"] += 1
            elif xcache == "MISS":
                counts["miss"] += 1
            rows.write("DYNAMIC", cell, rep, cell, "phase2", path, ae, raw, derived)
            counts["total"] += 1
            if derived["oracle_free_correct"] and not terr:
                counts["correct"] += 1
    log(f"PHASE 2: oracle-free correct {counts['correct']}/{counts['total']} "
        f"(MISS={counts['miss']} HIT={counts['hit']})")
    return counts


def phase3_hit(rows, registry):
    """HIT path: fixed URL per cell, populate(MISS)+test(HIT) x5 = 240 HIT obs.
    Frozen prereg: 1-3s delay between populate and test."""
    log("PHASE 3: HIT path through nginx cache (48x5, fixed URL populate+test)")
    counts = {"total": 0, "correct": 0, "test_hits": 0, "test_misses": 0}
    for cell in registry.cells:
        gt = registry.manifest[cell]
        headers = {"User-Agent": "SPIDER-R2/1.0"}
        ae = cell_ae(cell)
        if ae:
            headers["Accept-Encoding"] = ae
        path = f"/cache/{cell}"
        for rep in range(REPS):
            status, hdrs, body, ms, terr = raw_get("127.0.0.1", NGINX_PORT, path, headers)
            raw = make_raw(status, hdrs, body, ms, terr)
            derived = make_derived(gt, gt["plain_sha256"], body if not terr else b"")
            rows.write("HIT-POPULATE", cell, rep, cell, "phase3", path, ae, raw, derived)
            delay = 1.0 + random.uniform(0.0, 2.0)
            time.sleep(delay)
            status, hdrs, body, ms, terr = raw_get("127.0.0.1", NGINX_PORT, path, headers)
            raw = make_raw(status, hdrs, body, ms, terr)
            derived = make_derived(gt, gt["plain_sha256"], body if not terr else b"")
            xcache = (hdrs.get("x-cache") or "?").upper()
            rows.write("HIT", cell, rep, cell, "phase3", path, ae, raw, derived)
            counts["total"] += 1
            if xcache == "HIT":
                counts["test_hits"] += 1
            else:
                counts["test_misses"] += 1
            if derived["oracle_free_correct"] and not terr:
                counts["correct"] += 1
    log(f"PHASE 3: oracle-free correct {counts['correct']}/{counts['total']} "
        f"(test HIT={counts['test_hits']} MISS={counts['test_misses']})")
    return counts


def phase4_identity_dyn_vs_hit(rows, registry):
    """C8: last-rep DYNAMIC vs HIT wire bytes, per cell."""
    log("PHASE 4: C8 DYNAMIC-vs-HIT wire-byte identity")
    per_cell = []
    identical_cells = 0
    by_key = {(r["session_kind"], r["cell"], r["rep"]): r for r in rows.all_rows()}
    for cell in registry.cells:
        dyn = by_key.get(("DYNAMIC", cell, REPS - 1))
        hit = by_key.get(("HIT", cell, REPS - 1))
        d_raw, h_raw = dyn["raw"], hit["raw"]
        body_identical = (d_raw.get("body_sha256") == h_raw.get("body_sha256")
                          and d_raw.get("body_b64") == h_raw.get("body_b64"))
        ce_d = (d_raw.get("headers") or {}).get("content-encoding")
        ce_h = (h_raw.get("headers") or {}).get("content-encoding")
        ce_match = (ce_d or "") == (ce_h or "")
        cl_d = (d_raw.get("headers") or {}).get("content-length")
        cl_h = (h_raw.get("headers") or {}).get("content-length")
        cl_match = cl_d == cl_h
        identical = body_identical and ce_match and cl_match
        if identical:
            identical_cells += 1
        entry = {"cell": cell,
                 "bytes_identical": body_identical,
                 "content_encoding_match": ce_match,
                 "content_length_match": cl_match,
                 "body_sha_dynamic": d_raw.get("body_sha256"),
                 "body_sha_hit": h_raw.get("body_sha256"),
                 "ce_dynamic": ce_d, "ce_hit": ce_h,
                 "cl_dynamic": cl_d, "cl_hit": cl_h,
                 "x_cache_dynamic": (d_raw.get("headers") or {}).get("x-cache"),
                 "x_cache_hit": (h_raw.get("headers") or {}).get("x-cache"),
                 "identical": identical}
        per_cell.append(entry)
    rows_used = {"identical_cells_48": identical_cells,
                 "rate": round(identical_cells / 48, 4)}
    return per_cell, rows_used


def phase5_stability_and_identity(rows, registry):
    """C3: 6 stability groups x 3 consecutive requests; C4: 3 identity x5."""
    log("PHASE 5: C3 cache stability (6x3) + C4 identity (3x5)")
    stab = {"groups": [], "ok": 0}
    for pkey in registry.pkeys:
        if not pkey.startswith("STAB_"):
            continue
        gt = registry.manifest[pkey]
        path = f"/stab/{pkey}"
        shas = []
        decodes_ok = 0
        xcache_seq = []
        for i in range(3):
            status, hdrs, body, ms, terr = raw_get("127.0.0.1", NGINX_PORT, path, {})
            raw = make_raw(status, hdrs, body, ms, terr)
            derived = make_derived(gt, gt["plain_sha256"], body if not terr else b"")
            rows.write("STABILITY", pkey, i, pkey, "phase5", path, None, raw, derived)
            shas.append(raw.get("body_sha256"))
            xcache_seq.append((hdrs.get("x-cache") or "?").upper())
            if derived["oracle_free_correct"] and not terr:
                decodes_ok += 1
            time.sleep(1.0)
        byte_stable = len(set(shas)) == 1
        ok = byte_stable and decodes_ok == 3
        if ok:
            stab["ok"] += 1
        stab["groups"].append({"pkey": pkey, "byte_stable": byte_stable,
                               "decode_ok_count": decodes_ok,
                               "x_cache_seq": xcache_seq, "ok": ok})
    ident = {"total": 0, "correct": 0}
    for ct in CONTENT_TYPES:
        pkey = f"{ct}_IDENTITY"
        gt = registry.manifest[pkey]
        path = f"/iden/{pkey}"
        for rep in range(REPS):
            status, hdrs, body, ms, terr = raw_get("127.0.0.1", NGINX_PORT, path, {})
            raw = make_raw(status, hdrs, body, ms, terr)
            derived = make_derived(gt, gt["plain_sha256"], body if not terr else b"")
            rows.write("HIT-IDENTITY", pkey, rep, pkey, "phase5", path, None, raw, derived)
            ident["total"] += 1
            if derived["oracle_free_correct"] and not terr:
                ident["correct"] += 1
            time.sleep(1.5)
    log(f"PHASE 5: stability {stab['ok']}/6 groups ok; identity {ident['correct']}/{ident['total']}")
    return stab, ident


def phase6_depth(rows, registry):
    """C5: depth 3/4/5 x 3 types x 5 reps through nginx cache."""
    log("PHASE 6: C5 depth 3-5 through nginx cache (3x3x5=45)")
    counts = {"total": 0, "correct": 0, "hits": 0}
    for ct in CONTENT_TYPES:
        for depth in (3, 4, 5):
            pkey = f"{ct}_DEPTH{depth}"
            if pkey not in registry.manifest:
                continue
            gt = registry.manifest[pkey]
            path = f"/depth/{pkey}"
            for rep in range(REPS):
                status, hdrs, body, ms, terr = raw_get("127.0.0.1", NGINX_PORT, path, {})
                raw = make_raw(status, hdrs, body, ms, terr)
                derived = make_derived(gt, gt["plain_sha256"], body if not terr else b"")
                rows.write("HIT-DEPTH", pkey, rep, pkey, "phase6", path, None, raw, derived)
                counts["total"] += 1
                if (hdrs.get("x-cache") or "?").upper() == "HIT":
                    counts["hits"] += 1
                if derived["oracle_free_correct"] and not terr:
                    counts["correct"] += 1
                time.sleep(1.2)
    log(f"PHASE 6: depth oracle-free correct {counts['correct']}/{counts['total']} (HIT={counts['hits']})")
    return counts


def phase7_large(rows, registry):
    """C6: large >100KB payloads x 3 types x 2 orders x 5 reps."""
    log("PHASE 7: C6 large >100KB through nginx cache (3x2x5=30)")
    counts = {"total": 0, "correct": 0, "hits": 0}
    for ct in CONTENT_TYPES:
        for ok in ORDERS:
            pkey = f"{ct}_LARGE_{ok}"
            if pkey not in registry.manifest:
                continue
            gt = registry.manifest[pkey]
            path = f"/large/{pkey}"
            for rep in range(REPS):
                status, hdrs, body, ms, terr = raw_get("127.0.0.1", NGINX_PORT, path, {})
                raw = make_raw(status, hdrs, body, ms, terr)
                derived = make_derived(gt, gt["plain_sha256"], body if not terr else b"")
                rows.write("HIT-LARGE", pkey, rep, pkey, "phase7", path, None, raw, derived)
                counts["total"] += 1
                if (hdrs.get("x-cache") or "?").upper() == "HIT":
                    counts["hits"] += 1
                if derived["oracle_free_correct"] and not terr:
                    counts["correct"] += 1
                time.sleep(1.0)
    log(f"PHASE 7: large oracle-free correct {counts['correct']}/{counts['total']} (HIT={counts['hits']})")
    return counts


def phase8_baselines(rows, registry):
    """B-ORACLE-GUIDED-REGRESSION + B-FIXED-ORDER-CDN over DYNAMIC + HIT rows."""
    log("PHASE 8: regression baselines on same wire bytes (DYNAMIC+HIT, 480 rows)")
    counts = {"total": 0, "oracle_guided_ok": 0, "fixed_order_ok": 0}
    for row in rows.all_rows():
        if row["session_kind"] not in ("DYNAMIC", "HIT"):
            continue
        gt = registry.manifest.get(row["payload_key"])
        if gt is None:
            continue
        counts["total"] += 1
        if row["derived"].get("oracle_guided_correct"):
            counts["oracle_guided_ok"] += 1
        if row["derived"].get("fixed_order_correct"):
            counts["fixed_order_ok"] += 1
    log(f"PHASE 8: oracle-guided {counts['oracle_guided_ok']}/{counts['total']}; "
        f"fixed-order {counts['fixed_order_ok']}/{counts['total']}")
    return counts


def analyze(registry, results, rows):
    """Compute frozen metrics M-* and decision conditions C1-C8."""
    by = {(r["session_kind"], r["cell"], r["rep"]): r for r in rows.all_rows()}

    # M-HIT-RATE (frozen: % of test-phase requests with X-Cache: HIT across
    # all populate+test sessions, incl. HIT / HIT-IDENTITY / HIT-DEPTH / HIT-LARGE)
    hit_test_hits = sum(1 for k, v in by.items() if k[0] in ("HIT", "HIT-IDENTITY", "HIT-DEPTH", "HIT-LARGE")
                        and (v["raw"].get("headers") or {}).get("x-cache", "").upper() == "HIT")
    hit_test_total = sum(1 for k in by if k[0] in ("HIT", "HIT-IDENTITY", "HIT-DEPTH", "HIT-LARGE"))
    m_hit_rate = round(hit_test_hits / hit_test_total, 4) if hit_test_total else None

    # M-ORACLE-FREE-HIT-ACCURACY (C2): all cached-path observations
    cached_kinds = ("HIT", "HIT-IDENTITY", "HIT-DEPTH", "HIT-LARGE")
    cached_total = 0
    cached_correct = 0
    for k, v in by.items():
        if k[0] in cached_kinds:
            cached_total += 1
            if v["derived"].get("oracle_free_correct"):
                cached_correct += 1
    m_acc_all_cache = round(cached_correct / cached_total, 4) if cached_total else None

    # C1: all 48 primary cache HIT cells byte-identical (every rep correct)
    c1_cells_ok = 0
    c1_cells_total = 0
    c1_cell_detail = {}
    for cell in registry.cells:
        reps = [by.get(("HIT", cell, r)) for r in range(REPS)]
        if all(r is not None for r in reps):
            c1_cells_total += 1
            all_ok = all((r["derived"].get("oracle_free_correct") and
                          not r["raw"].get("transport_error")) for r in reps)
            if all_ok:
                c1_cells_ok += 1
            c1_cell_detail[cell] = {"all_reps_correct": all_ok,
                                    "n_ok": sum(1 for r in reps if r["derived"].get("oracle_free_correct")
                                                and not r["raw"].get("transport_error"))}
    c1_pass = c1_cells_ok == 48

    # C2: >=90% of cache HIT observations correct
    hit_correct = 0
    hit_total = 0
    for k, v in by.items():
        if k[0] in ("HIT", "HIT-IDENTITY", "HIT-DEPTH", "HIT-LARGE"):
            hit_total += 1
            if v["derived"].get("oracle_free_correct") and not v["raw"].get("transport_error"):
                hit_correct += 1
    c2_rate = round(hit_correct / hit_total, 4) if hit_total else None
    c2_pass = c2_rate is not None and c2_rate >= 0.90

    # C3: 6/6 stability groups
    # C4: 15/15 identity
    # C5: depth >=80%
    # C6: large >=80%
    # C7: no ambiguous tie-breaks across all cached + dynamic rows
    ambiguous = 0
    for v in by.values():
        if v["derived"].get("oracle_free_ambiguous"):
            ambiguous += 1

    # C8: DYNAMIC vs HIT wire bytes identical >=90% of cells
    c8_identical = sum(1 for e in results["phase4"]["per_cell"] if e["identical"])
    c8_rate = round(c8_identical / 48, 4)
    c8_pass = c8_rate >= 0.90

    stabs = results["phase5"]["stab"]
    c3_ok = stabs["ok"]
    c3_pass = c3_ok == 6
    ident = results["phase5"]["ident"]
    c4_pass = ident["correct"] == 15 and ident["total"] == 15
    d6 = results["phase6"]
    c5_rate = round(d6["correct"] / d6["total"], 4) if d6["total"] else None
    c5_pass = c5_rate is not None and c5_rate >= 0.80
    d7 = results["phase7"]
    c6_rate = round(d7["correct"] / d7["total"], 4) if d7["total"] else None
    c6_pass = c6_rate is not None and c6_rate >= 0.80
    c7_pass = ambiguous == 0

    conditions = {
        "C1": {"desc": "all 48 primary cache HIT cells recover ground truth (all reps)",
               "pass": c1_pass, "value": f"{c1_cells_ok}/48"},
        "C2": {"desc": ">=90% of cache HIT observations byte-identical",
               "pass": c2_pass, "value": f"{hit_correct}/{hit_total} = {c2_rate}"},
        "C3": {"desc": "6/6 cache stability groups byte-stable and correctly decoded",
               "pass": c3_pass, "value": f"{c3_ok}/6"},
        "C4": {"desc": "15/15 identity observations recover ground truth",
               "pass": c4_pass, "value": f"{ident['correct']}/{ident['total']}"},
        "C5": {"desc": "depth 3-5 >=80% correct", "pass": c5_pass,
               "value": f"{d6['correct']}/{d6['total']} = {c5_rate}"},
        "C6": {"desc": "large >100KB >=80% correct", "pass": c6_pass,
               "value": f"{d7['correct']}/{d7['total']} = {c6_rate}"},
        "C7": {"desc": "zero ambiguous tie-breaks", "pass": c7_pass, "value": f"{ambiguous}"},
        "C8": {"desc": "DYNAMIC vs HIT wire bytes identical >=90% of cells",
               "pass": c8_pass, "value": f"{c8_identical}/48 = {c8_rate}"},
    }
    all_pass = all(c["pass"] for c in conditions.values())
    if not c1_pass:
        verdict = "FALSIFIES"
    elif not (c2_pass and c8_pass):
        verdict = "MIXED"
    else:
        verdict = "SUPPORTS" if all_pass else "MIXED"

    metrics = {
        "M-HIT-RATE": m_hit_rate,
        "M-ORACLE-FREE-HIT-ACCURACY": m_acc_all_cache,
        "M-ORACLE-FREE-DYNAMIC-ACCURACY": results["phase2"]["correct"] / results["phase2"]["total"] if results["phase2"]["total"] else None,
        "M-ORACLE-FREE-LOCALHOST-ACCURACY": results["phase1"]["correct"] / results["phase1"]["total"] if results["phase1"]["total"] else None,
        "M-ORACLE-GUIDED-REGRESSION": results["phase8"]["oracle_guided_ok"] / results["phase8"]["total"] if results["phase8"]["total"] else None,
        "M-FIXED-ORDER-CDN": results["phase8"]["fixed_order_ok"] / results["phase8"]["total"] if results["phase8"]["total"] else None,
        "M-BYTES-IDENTICAL": c8_rate,
        "M-DEPTH-ACCURACY": c5_rate,
        "M-LARGE-ACCURACY": c6_rate,
        "M-STABILITY-GROUPS": c3_ok,
        "M-IDENTITY": ident["correct"] / ident["total"] if ident["total"] else None,
        "M-AMBIGUOUS": ambiguous,
    }
    return {"conditions": conditions, "verdict": verdict, "metrics": metrics,
            "all_pass": all_pass, "c1_cell_detail": c1_cell_detail,
            "c8_detail": results["phase4"]["per_cell"]}


def main():
    random.seed(SEED)
    RUN_LOG.write_text("", encoding="utf-8")
    log(f"=== {EXPERIMENT_ID} EXECUTE start ===")
    registry = PayloadRegistry()
    registry.build()
    log(f"payload registry: {len(registry.cells)} primary cells, "
        f"{len(registry.pkeys)} total payload keys, entropy range "
        f"{min(m['entropy'] for m in registry.manifest.values()):.2f}-"
        f"{max(m['entropy'] for m in registry.manifest.values()):.2f} bits/byte")
    MANIFEST_PATH.write_text(json.dumps(
        {"experiment_id": EXPERIMENT_ID, "seed": SEED, "auth_state": AUTH_STATE,
         "target_size": TARGET_SIZE, "max_depth": MAX_DEPTH, "reps": REPS,
         "cells": registry.cells, "payloads": registry.manifest},
        indent=2), encoding="utf-8")
    log(f"manifest written: {MANIFEST_PATH}")
    # sanity: gt must equal plain body for every payload
    bad_gt = [k for k, m in registry.manifest.items() if not m["gt_is_plain"]]
    if bad_gt:
        log(f"FATAL: ground-truth mismatch for {bad_gt[:5]}")
        sys.exit(2)

    origin = ThreadingOrigin(("127.0.0.1", ORIGIN_PORT), registry.serve)
    origin.serve_forever_thread = threading.Thread(target=origin.serve_forever, daemon=True)
    origin.serve_forever_thread.start()
    time.sleep(0.3)

    rows = RowWriter(ROWS_PATH)
    results = {}
    try:
        write_nginx_conf(NGINX_PREFIX, NGINX_PORT, ORIGIN_PORT, relaxed=False)
        infra, infra_ok = phase0_infra(rows, registry)
        results["phase0"] = infra
        results["phase0_ok"] = infra_ok
        if not infra_ok:
            log("PHASE 0: no cache HIT after standard config; retrying with "
                "proxy_ignore_headers relaxation")
            write_nginx_conf(NGINX_PREFIX, NGINX_PORT, ORIGIN_PORT, relaxed=True)
            stop_nginx()
            time.sleep(0.5)
            ok2, out2 = start_nginx()
            results["phase0_relaxed_nginx_t"] = out2.strip()
            time.sleep(0.5)
            hits2 = 0
            for i in range(10):
                warm_token = f"{registry.pkeys[0]}_WARM"
                actual_path = f"/cache/{warm_token}"
                status, hdrs, body, ms, terr = raw_get("127.0.0.1", NGINX_PORT, actual_path, {})
                if (hdrs.get("x-cache") or "").upper() == "HIT":
                    hits2 += 1
            results["phase0_relaxed_hits"] = hits2
            infra_ok = hits2 >= 1
        if not infra_ok:
            log("PHASE 0 FAILED: no cache HIT achievable locally -> infrastructure ceiling")
            results["infra_ceiling"] = True
            rows.close()
            stop_nginx()
            SUMMARY_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
            sys.exit(3)

        results["phase1"] = phase1_localhost_direct(rows, registry)
        results["phase2"] = phase2_dynamic(rows, registry)
        results["phase3"] = phase3_hit(rows, registry)
        results["phase4"] = {}
        results["phase4"]["per_cell"], results["phase4"]["rows"] = phase4_identity_dyn_vs_hit(rows, registry)
        results["phase5"] = {}
        results["phase5"]["stab"], results["phase5"]["ident"] = phase5_stability_and_identity(rows, registry)
        results["phase6"] = phase6_depth(rows, registry)
        results["phase7"] = phase7_large(rows, registry)
        results["phase8"] = phase8_baselines(rows, registry)
    finally:
        rows.close()

    analysis = analyze(registry, results, rows)
    results["analysis"] = analysis
    HVD_PATH.write_text(json.dumps(analysis["c8_detail"], indent=2), encoding="utf-8")
    SUMMARY_PATH.write_text(json.dumps(
        {"experiment_id": EXPERIMENT_ID, "phase0": results.get("phase0"),
         "phase1": results.get("phase1"), "phase2": results.get("phase2"),
         "phase3": results.get("phase3"), "phase4_rows": results.get("phase4", {}).get("rows"),
         "phase5_stab": results.get("phase5", {}).get("stab"),
         "phase5_ident": results.get("phase5", {}).get("ident"),
         "phase6": results.get("phase6"), "phase7": results.get("phase7"),
         "phase8": results.get("phase8"), "analysis": analysis,
         "dup_cell_rep_keys": rows.duplicates},
        indent=2), encoding="utf-8")
    log(f"VERDICT: {analysis['verdict']}")
    for k, v in analysis["conditions"].items():
        log(f"  {k}: pass={v['pass']} value={v['value']}")
    if rows.duplicates:
        log(f"WARNING: duplicate (session_kind, cell, rep) keys: {len(rows.duplicates)}")
    stop_nginx()
    log(f"=== {EXPERIMENT_ID} EXECUTE complete ===")


if __name__ == "__main__":
    main()