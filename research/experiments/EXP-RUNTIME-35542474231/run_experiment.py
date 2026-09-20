#!/usr/bin/env python3
"""
EXP-RUNTIME-35542474231 -- EXECUTE (frozen spec.json / prereg.md / freeze.json).

Encoding-agnostic iterative decompression through Cloudflare CDN.
Tests whether sniffing delivered bytes and trying brotli->gzip->identity
until SHA256 matches ground truth restores byte-identical correctness for
all 48 primary cells, plus depth generalization and large payload conditions.

RAW EVIDENCE (response bytes SHAs, verbatim headers, timings) is kept
distinct from DERIVED MEASUREMENTS (decompressed SHAs, correct booleans)
in every JSONL row: {"raw": {...}, "derived": {...}}.
"""
import binascii
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
EXPERIMENT_ID = "EXP-RUNTIME-35542474231"
LANE = "runtime"
SEED = 44
REPS = 5
MAX_DEPTH = 5
ORIGIN_PORT = 18793
CLOUDFLARED_BIN = "/tmp/opencode/cloudflared"
TUNNEL_LOG = HERE / "tunnel.log"
ROWS_PATH = HERE / "raw_cell_results.jsonl"
MANIFEST_PATH = HERE / "payload_manifest.json"

CONTENT_TYPES = {"JSON": "application/json", "HTML": "text/html",
                 "BINARY": "application/octet-stream"}
TARGET_SIZE = 10240
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

def encoding_agnostic_decode(raw_bytes, ground_truth_sha256):
    """Iteratively try brotli -> gzip -> identity until SHA256 matches ground truth.
    Returns (decoded_bytes, method_used) or (None, None) if all fail.
    
    The algorithm iteratively attempts decompression up to MAX_DEPTH layers:
    At each layer, try brotli, then gzip. If neither works, try identity.
    After each successful decompression, check SHA256 against ground truth.
    """
    current = raw_bytes
    path = []
    for depth in range(MAX_DEPTH):
        # Check if current bytes match ground truth
        if hashlib.sha256(current).hexdigest() == ground_truth_sha256:
            method = "+".join(path) if path else "identity"
            return current, method
        # Try brotli decompression
        try:
            decoded = brotli.decompress(current)
            path.append("br")
            current = decoded
            continue  # Successfully decompressed, try next layer
        except Exception:
            pass
        # Try gzip decompression
        try:
            decoded = gzip.decompress(current)
            path.append("gz")
            current = decoded
            continue  # Successfully decompressed, try next layer
        except Exception:
            pass
        # Neither brotli nor gzip worked - try identity at this point
        if hashlib.sha256(current).hexdigest() == ground_truth_sha256:
            method = "+".join(path) if path else "identity"
            return current, method
        # All decoders failed at this layer
        break
    # Final check after all iterations
    if hashlib.sha256(current).hexdigest() == ground_truth_sha256:
        method = "+".join(path) if path else "identity"
        return current, method
    return None, None

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
    if len(layers_inner_first) == 2:
        outer = streaming_unwrap_one(data, layers_inner_first[-1]["type"], chunk_size)
        return streaming_unwrap_one(outer, layers_inner_first[-2]["type"], chunk_size)
    return streaming_unwrap_one(data, layers_inner_first[-1]["type"], chunk_size)

# ---------------------------------------------------------------- origin server
SERVE = {}

class OriginHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _serve(self, token):
        item = SERVE.get(token)
        if item is None:
            body = b"NOT-FOUND:" + token.encode()
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        body = item["body"]
        self.send_response(200)
        self.send_header("Content-Type", item["ctype"])
        if item["ce"]:
            self.send_header("Content-Encoding", item["ce"])
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=300")
        self.send_header("X-Origin-Token", token)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            body = b"OK"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(body)
            return
        m = re.match(r"^/(m|cache|id|depth|large)/([A-Za-z0-9_.-]+)(\?.*)?$", self.path)
        if not m:
            body = b"BAD-PATH"
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self._serve(m.group(2))

    def log_message(self, *a):
        pass

# ---------------------------------------------------------------- raw HTTP client
def raw_get(url, accept_encoding=None, timeout=30):
    pu = urllib.parse.urlparse(url)
    t0 = time.monotonic()
    if pu.scheme == "https":
        conn = http.client.HTTPSConnection(pu.hostname, pu.port or 443, timeout=timeout)
    else:
        conn = http.client.HTTPConnection(pu.hostname, pu.port or 80, timeout=timeout)
    path = pu.path or "/"
    if pu.query:
        path += "?" + pu.query
    headers = {"Host": pu.hostname, "Connection": "close",
               "User-Agent": "SPIDER-EXP-RUNTIME-35542474231"}
    if accept_encoding is not None:
        headers["Accept-Encoding"] = accept_encoding
    transport_error = None
    try:
        conn.request("GET", path, headers=headers)
        resp = conn.getresponse()
        status = resp.status
        resp_headers = {k.lower(): v for k, v in resp.getheaders()}
        chunks = []
        while True:
            b = resp.read(8192)
            if not b:
                break
            chunks.append(b)
        raw_body = b"".join(chunks)
    except Exception as e:
        status, resp_headers, raw_body = None, {}, b""
        transport_error = f"{type(e).__name__}: {e}"
    finally:
        try:
            conn.close()
        except Exception:
            pass
    dt_ms = (time.monotonic() - t0) * 1000.0
    return {"url": url, "accept_encoding_sent": accept_encoding,
            "response_status": status, "response_headers": resp_headers,
            "raw_body_sha256": hashlib.sha256(raw_body).hexdigest(),
            "raw_body_len": len(raw_body),
            "response_time_ms": round(dt_ms, 1),
            "transport_error": transport_error,
            "_raw_body": raw_body}

def main():
    t_start = time.time()
    log = []
    def say(s):
        print(s, flush=True)
        log.append(s)

    # ---- Phase 0: entropy preflight + payload build
    say("PHASE 0: entropy preflight + payload build")
    manifest = {"experiment_id": EXPERIMENT_ID, "seed": SEED,
                "target_size": TARGET_SIZE, "payloads": {}}
    for ct in CONTENT_TYPES:
        body = BODY_GENERATORS[ct](AUTH_STATE, TARGET_SIZE)
        ent = compute_shannon_entropy(body)
        say(f"  {ct}: len={len(body)} entropy={ent:.2f} bits/byte")
        if ent < 3.5:
            say("MEASUREMENT_INVALID: entropy preflight failed")
            return 2
        for order_key, (layers, served_ce) in ORDERS.items():
            comp = compress_layers(body, layers)
            gt = fullbody_decompress(comp)
            assert gt == body, f"ground-truth self-check failed {ct}/{order_key}"
            pkey = f"{ct}_{order_key}"
            SERVE[pkey] = {"body": comp, "ce": served_ce, "ctype": CONTENT_TYPES[ct]}
            manifest["payloads"][pkey] = {
                "content_type": ct, "order": order_key,
                "layers_inner_first": layers,
                "served_content_encoding": served_ce,
                "plain_len": len(body),
                "plain_sha256": hashlib.sha256(body).hexdigest(),
                "compressed_len": len(comp),
                "compressed_sha256": hashlib.sha256(comp).hexdigest(),
                "ground_truth_sha256": hashlib.sha256(gt).hexdigest(),
            }
            say(f"  payload {pkey}: plain={len(body)}B comp={len(comp)}B ce={served_ce} gt_ok=True")
    for ct in CONTENT_TYPES:
        body = BODY_GENERATORS[ct](AUTH_STATE, TARGET_SIZE)
        pkey = f"{ct}_IDENTITY"
        SERVE[pkey] = {"body": body, "ce": None, "ctype": CONTENT_TYPES[ct]}
        manifest["payloads"][pkey] = {
            "content_type": ct, "order": "IDENTITY",
            "served_content_encoding": None, "plain_len": len(body),
            "plain_sha256": hashlib.sha256(body).hexdigest(),
        }

    # ---- origin server
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", ORIGIN_PORT), OriginHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    say(f"origin up on 127.0.0.1:{ORIGIN_PORT}")
    origin_base = f"http://127.0.0.1:{ORIGIN_PORT}"

    # ---- tunnel
    say("starting cloudflared quick tunnel ...")
    with open(TUNNEL_LOG, "w") as fl:
        tun = subprocess.Popen(
            [CLOUDFLARED_BIN, "tunnel", "--url",
             f"http://127.0.0.1:{ORIGIN_PORT}", "--no-autoupdate"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        cdn_base = None
        t_tun0 = time.time()
        fd = tun.stdout.fileno()
        import select
        buf = ""
        while time.time() - t_tun0 < 90:
            ready_fds, _, _ = select.select([fd], [], [], 5.0)
            if not ready_fds:
                if cdn_base is not None:
                    break
                continue
            chunk = os.read(fd, 65536).decode("utf-8", "replace")
            if not chunk:
                break
            fl.write(chunk)
            fl.flush()
            buf += chunk
            m = re.search(r"https://[A-Za-z0-9-]+\.trycloudflare\.com", buf)
            if m and cdn_base is None:
                cdn_base = m.group(0)
            if cdn_base is not None and "Registered tunnel connection" in buf:
                break
        fl.flush()
        if cdn_base is None:
            fl.write("TUNNEL-URL-NOT-FOUND\n")
            say("BLOCKED: tunnel URL not established within 90s")
            tun.terminate()
            return 3
    say(f"tunnel URL: {cdn_base}")
    ready = False
    for i in range(30):
        r = raw_get(cdn_base + "/health", accept_encoding=None, timeout=20)
        if r["response_status"] == 200 and r["_raw_body"] == b"OK":
            ready = True
            say(f"CDN reachable after {i+1} probes (rt={r['response_time_ms']}ms)")
            break
        time.sleep(2)
    if not ready:
        say("BLOCKED: tunnel URL not reachable (no HTTP 200 on /health x30)")
        tun.terminate()
        return 3

    rows = []
    jitter = random.Random(SEED)

    def fetch_and_measure(session_kind, cell, rep, pkey, ae_name, chunk_size,
                          base, path_prefix, url_token, use_encoding_agnostic=True):
        layers = manifest["payloads"][pkey].get("layers_inner_first")
        served_ce = manifest["payloads"][pkey]["served_content_encoding"]
        gt_sha = manifest["payloads"][pkey].get("ground_truth_sha256")
        ae = AE_VARIANTS[ae_name]
        url = f"{base}/{path_prefix}/{url_token}"
        raw = raw_get(url, accept_encoding=ae, timeout=40)
        body = raw.pop("_raw_body")
        derived = {"streaming_sha256": None, "correct": None,
                   "ce_matches_expected": None, "streaming_error": None,
                   "encoding_agnostic_method": None, "encoding_agnostic_correct": None}
        ce_actual = raw["response_headers"].get("content-encoding")
        if served_ce is None:
            derived["ce_matches_expected"] = ce_actual is None
        else:
            derived["ce_matches_expected"] = (
                ce_actual is not None and ce_actual.strip().lower()
                == served_ce.strip().lower())
        if raw["response_status"] == 200 and raw["transport_error"] is None:
            try:
                if layers is None:
                    out = body
                else:
                    out = streaming_decompress_multi_layer(body, layers, chunk_size)
                derived["streaming_sha256"] = hashlib.sha256(out).hexdigest()
                if served_ce is None:
                    derived["correct"] = (
                        derived["streaming_sha256"]
                        == manifest["payloads"][pkey]["plain_sha256"])
                else:
                    derived["correct"] = (derived["streaming_sha256"] == gt_sha)
            except Exception as e:
                derived["streaming_error"] = f"{type(e).__name__}: {e}"
                derived["correct"] = False
            if use_encoding_agnostic:
                # For identity payloads, ground truth is plain_sha256
                target_sha = gt_sha if gt_sha is not None else manifest["payloads"][pkey]["plain_sha256"]
                decoded, method = encoding_agnostic_decode(body, target_sha)
                derived["encoding_agnostic_method"] = method
                if decoded is not None:
                    derived["encoding_agnostic_correct"] = (
                        hashlib.sha256(decoded).hexdigest() == target_sha)
                else:
                    derived["encoding_agnostic_correct"] = False
        else:
            derived["streaming_error"] = (
                raw["transport_error"] or f"HTTP {raw['response_status']}")
            derived["correct"] = False
            derived["encoding_agnostic_correct"] = False
        rows.append({"experiment_id": EXPERIMENT_ID,
                     "session_kind": session_kind, "cell": cell, "rep": rep,
                     "payload_key": pkey, "accept_encoding": ae_name,
                     "chunk_size": chunk_size,
                     "served_content_encoding": served_ce,
                     "expected_sha256": gt_sha or manifest["payloads"][pkey]["plain_sha256"],
                     "url_path_prefix": path_prefix, "raw": raw,
                     "derived": derived})
        return rows[-1]

    # ---- Phase 1: positive control B-LOCALHOST-DIRECT (48 cells x REPS)
    say("PHASE 1: B-LOCALHOST-DIRECT (localhost, 48 cells x 5)")
    rng = random.Random(SEED)
    cells = [(ct, ok, cs, ae)
             for ct in CONTENT_TYPES for ok in ORDERS
             for cs in CHUNK_SIZES for ae in AE_VARIANTS]
    n_local_ok = 0
    n_local_ea_ok = 0
    n_local = 0
    for (ct, ok, cs, ae) in cells:
        pkey = f"{ct}_{ok}"
        cell = f"LOCALHOST_{pkey}_chunk{cs}_ae-{ae}"
        plan = list(range(REPS))
        rng.shuffle(plan)
        for rep in plan:
            tok = f"{pkey}_L{rep}_{uuid.uuid4().hex[:8]}"
            SERVE[tok] = SERVE[pkey]
            row = fetch_and_measure("LOCALHOST", cell, rep, pkey, ae, cs,
                                    origin_base, "m", tok)
            n_local += 1
            n_local_ok += 1 if row["derived"]["correct"] else 0
            n_local_ea_ok += 1 if row["derived"]["encoding_agnostic_correct"] else 0
    say(f"  localhost fixed-order: {n_local_ok}/{n_local} correct")
    say(f"  localhost encoding-agnostic: {n_local_ea_ok}/{n_local} correct")

    # ---- Phase 2: CDN main matrix
    say("PHASE 2: CDN main matrix (48 cells x 5, jitter 200-500ms)")
    n_cdn_ea_ok = 0
    n_cdn = 0
    for (ct, ok, cs, ae) in cells:
        pkey = f"{ct}_{ok}"
        cell = f"CDN_{pkey}_chunk{cs}_ae-{ae}"
        plan = list(range(REPS))
        rng.shuffle(plan)
        for rep in plan:
            tok = f"{pkey}_C{rep}_{uuid.uuid4().hex[:8]}"
            SERVE[tok] = SERVE[pkey]
            row = fetch_and_measure("CDN", cell, rep, pkey, ae, cs,
                                    cdn_base, "m", tok)
            n_cdn += 1
            n_cdn_ea_ok += 1 if row["derived"]["encoding_agnostic_correct"] else 0
            time.sleep(jitter.uniform(0.2, 0.5))
        ea_cnt = sum(1 for r in rows if r["cell"] == cell and r["derived"]["encoding_agnostic_correct"] is True)
        fo_cnt = sum(1 for r in rows if r["cell"] == cell and r["derived"]["correct"] is True)
        say(f"  {cell}: fixed={fo_cnt} ea={ea_cnt}/{REPS}")

    # ---- Phase 3: CDN cache stability (C3)
    say("PHASE 3: CDN cache stability (6 payloads x 3 consecutive)")
    cache_groups = {}
    for ct in CONTENT_TYPES:
        for ok in ORDERS:
            pkey = f"{ct}_{ok}"
            key = f"CACHE_{pkey}"
            SERVE[key] = SERVE[pkey]
            outs = []
            for i in range(3):
                row = fetch_and_measure("CDN-CACHE", f"CACHE_{pkey}", i, pkey,
                                        "both", 8192, cdn_base, "cache", key)
                outs.append((row["raw"]["raw_body_sha256"],
                             row["derived"]["streaming_sha256"],
                             row["derived"]["correct"],
                             row["derived"]["encoding_agnostic_correct"],
                             row["raw"]["response_headers"].get("cf-cache-status")))
                if i < 2:
                    time.sleep(1.0)
            cache_groups[pkey] = outs
            say(f"  {pkey}: raw_same={outs[0][0]==outs[1][0]==outs[2][0]} "
                f"dec_same={outs[0][1]==outs[1][1]==outs[2][1]} "
                f"all_correct={all(o[2] for o in outs)} "
                f"ea_all={all(o[3] for o in outs)} cf={outs[0][4]}")

    # ---- Phase 4: null control B-CDN-IDENTITY
    say("PHASE 4: B-CDN-IDENTITY (3 types x 5 via CDN)")
    n_id_ea_ok = 0
    n_id = 0
    for ct in CONTENT_TYPES:
        pkey = f"{ct}_IDENTITY"
        for rep in range(REPS):
            tok = f"{pkey}_{uuid.uuid4().hex[:8]}"
            SERVE[tok] = SERVE[pkey]
            row = fetch_and_measure("CDN-IDENTITY", f"IDENTITY_{ct}", rep,
                                    pkey, "both", 8192, cdn_base, "id", tok)
            n_id += 1
            n_id_ea_ok += 1 if row["derived"]["encoding_agnostic_correct"] else 0
            time.sleep(jitter.uniform(0.2, 0.5))
    say(f"  identity via CDN encoding-agnostic: {n_id_ea_ok}/{n_id} correct")

    # ---- Phase 5: Depth generalization (depths 3-5)
    say("PHASE 5: Depth generalization (depths 3-5, alternating brotli/gzip)")
    depth_observations = []
    for depth in [3, 4, 5]:
        for ct in CONTENT_TYPES:
            body = BODY_GENERATORS[ct](AUTH_STATE, TARGET_SIZE)
            layers = []
            for i in range(depth):
                if i % 2 == 0:
                    layers.append({"type": "brotli", "quality": 4})
                else:
                    layers.append({"type": "gzip", "level": 1})
            served_ce = "br" if layers[-1]["type"] == "brotli" else "gzip"
            comp = compress_layers(body, layers)
            gt = fullbody_decompress(comp)
            pkey = f"{ct}_DEPTH{depth}"
            SERVE[pkey] = {"body": comp, "ce": served_ce, "ctype": CONTENT_TYPES[ct]}
            manifest["payloads"][pkey] = {
                "content_type": ct, "order": f"DEPTH{depth}",
                "layers_inner_first": layers,
                "served_content_encoding": served_ce,
                "plain_len": len(body),
                "plain_sha256": hashlib.sha256(body).hexdigest(),
                "compressed_len": len(comp),
                "compressed_sha256": hashlib.sha256(comp).hexdigest(),
                "ground_truth_sha256": hashlib.sha256(gt).hexdigest(),
                "depth": depth,
            }
            for rep in range(REPS):
                tok = f"{pkey}_D{rep}_{uuid.uuid4().hex[:8]}"
                SERVE[tok] = SERVE[pkey]
                row = fetch_and_measure("CDN-DEPTH", f"DEPTH{depth}_{ct}", rep,
                                        pkey, "both", 8192, cdn_base, "depth", tok)
                depth_observations.append(row)
                time.sleep(jitter.uniform(0.2, 0.5))
            ea_cnt = sum(1 for r in depth_observations
                         if r["cell"] == f"DEPTH{depth}_{ct}"
                         and r["derived"]["encoding_agnostic_correct"] is True)
            say(f"  depth {depth} {ct}: ea_correct={ea_cnt}/{REPS}")

    # ---- Phase 6: Large payload (>100KB)
    say("PHASE 6: Large payload (>100KB)")
    LARGE_TARGET = 150000
    large_observations = []
    for ct in CONTENT_TYPES:
        body = BODY_GENERATORS[ct](AUTH_STATE, LARGE_TARGET)
        for order_key, (layers, served_ce) in ORDERS.items():
            comp = compress_layers(body, layers)
            gt = fullbody_decompress(comp)
            pkey = f"{ct}_LARGE_{order_key}"
            SERVE[pkey] = {"body": comp, "ce": served_ce, "ctype": CONTENT_TYPES[ct]}
            manifest["payloads"][pkey] = {
                "content_type": ct, "order": f"LARGE_{order_key}",
                "layers_inner_first": layers,
                "served_content_encoding": served_ce,
                "plain_len": len(body),
                "plain_sha256": hashlib.sha256(body).hexdigest(),
                "compressed_len": len(comp),
                "compressed_sha256": hashlib.sha256(comp).hexdigest(),
                "ground_truth_sha256": hashlib.sha256(gt).hexdigest(),
                "payload_size": LARGE_TARGET,
            }
            for rep in range(REPS):
                tok = f"{pkey}_L{rep}_{uuid.uuid4().hex[:8]}"
                SERVE[tok] = SERVE[pkey]
                row = fetch_and_measure("CDN-LARGE", f"LARGE_{ct}_{order_key}", rep,
                                        pkey, "both", 8192, cdn_base, "large", tok)
                large_observations.append(row)
                time.sleep(jitter.uniform(0.2, 0.5))
            ea_cnt = sum(1 for r in large_observations
                         if r["cell"] == f"LARGE_{ct}_{order_key}"
                         and r["derived"]["encoding_agnostic_correct"] is True)
            say(f"  large {ct} {order_key}: ea_correct={ea_cnt}/{REPS}")

    # ---- Summary
    say("=== SUMMARY ===")
    cdn_ea = sum(1 for r in rows if r["session_kind"] == "CDN"
                 and r["derived"]["encoding_agnostic_correct"] is True)
    cdn_tot = sum(1 for r in rows if r["session_kind"] == "CDN")
    say(f"CDN primary matrix encoding-agnostic: {cdn_ea}/{cdn_tot}")
    local_ea = sum(1 for r in rows if r["session_kind"] == "LOCALHOST"
                   and r["derived"]["encoding_agnostic_correct"] is True)
    local_tot = sum(1 for r in rows if r["session_kind"] == "LOCALHOST")
    say(f"Localhost encoding-agnostic: {local_ea}/{local_tot}")
    id_ea = sum(1 for r in rows if r["session_kind"] == "CDN-IDENTITY"
                and r["derived"]["encoding_agnostic_correct"] is True)
    id_tot = sum(1 for r in rows if r["session_kind"] == "CDN-IDENTITY")
    say(f"Identity encoding-agnostic: {id_ea}/{id_tot}")
    depth_ea = sum(1 for r in depth_observations
                   if r["derived"]["encoding_agnostic_correct"] is True)
    depth_tot = len(depth_observations)
    say(f"Depth generalization encoding-agnostic: {depth_ea}/{depth_tot}")
    large_ea = sum(1 for r in large_observations
                   if r["derived"]["encoding_agnostic_correct"] is True)
    large_tot = len(large_observations)
    say(f"Large payload encoding-agnostic: {large_ea}/{large_tot}")

    # ---- persist raw rows + manifest
    all_rows = rows + depth_observations + large_observations
    with open(ROWS_PATH, "w") as f:
        for r in all_rows:
            f.write(json.dumps(r) + "\n")
    manifest["tunnel_url"] = cdn_base
    manifest["origin"] = origin_base
    manifest["n_rows"] = len(all_rows)
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    say(f"wrote {len(all_rows)} rows -> {ROWS_PATH}")
    say(f"wall_time_s={round(time.time()-t_start,1)}")

    tun.terminate()
    try:
        srv.shutdown()
    except Exception:
        pass
    return 0

if __name__ == "__main__":
    sys.exit(main())
