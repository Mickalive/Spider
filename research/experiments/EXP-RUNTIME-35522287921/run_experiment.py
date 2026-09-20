#!/usr/bin/env python3
"""
EXP-RUNTIME-35522287921 - Streaming Incremental Decompression Correctness
Frozen from spec.json and prereg.md
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

EXPERIMENT_ID = "EXP-RUNTIME-35522287921"
LANE = "runtime"
SEED = 44
REPS = 5
BASE_PORT = 18700
STREAM_PROXY_PORT_BASE = 18800
BUFFERED_PROXY_PORT_BASE = 18900
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
MULTI_LAYER_MODES = {
    "GZIP-THEN-BROTLI": {
        "layers": [{"type": "gzip", "level": 1}, {"type": "brotli", "quality": 4}],
        "use_chunked": True,
    },
    "BROTLI-THEN-GZIP": {
        "layers": [{"type": "brotli", "quality": 4}, {"type": "gzip", "level": 1}],
        "use_chunked": True,
    },
}
REGRESSION_MODES = {
    "GZIP-SINGLE": {"layers": [{"type": "gzip", "level": None}], "use_chunked": True},
    "BROTLI-SINGLE": {"layers": [{"type": "brotli", "quality": 6}], "use_chunked": True},
}
AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]
SHANNON_ENTROPY_MIN = 3.5
STREAM_CHUNK_SIZES = [8192, 32]

HTML_WORDS = [
    "quantum","nebula","algorithm","synthesis","morphology","topology","paradigm","entropy","syntactic","recursive","distributed","asynchronous","vector","scalar","heuristic","stochastic","orthogonal","polymorphic","isomorphic","homomorphic","cryptographic","probabilistic","steganographic","metamorphic","quantitative","longitudinal","multivariate","dimensional","resonance","catalyst","substrate","amplitude","frequency","spectral","turbulent","viscous","lamellar","ferromagnetic","piezoelectric","superconductor","semiconductor","photoelectric","thermodynamic","electromagnetic","gravitational","chromatic","diffraction","interference","polarization","refraction","scattering","absorption","emission","fluorescence","phosphorescence","luminescence","bioluminescence","chromatography","spectroscopy","microscopy","crystallography","algorithmic","heuristic","deterministic","stochastic","Bayesian","Gaussian","Poisson","Markovian","Eulerian","Lagrangian","Hilbert","Fourier","Laplace","Riemann","Euclidean","Riemannian","manifold","bundle","morphism","functor","category","groupoid","semigroup","monoid","lattice","poset","topology","homology","cohomology","homotopy","sheaf","presheaf","differential","geodesic","curvature","tensor","matrix","polynomial","eigenvalue",
]

def compute_shannon_entropy(data):
    if len(data)==0:
        return 0.0
    freq=[0]*256
    for b in data:
        freq[b]+=1
    length=len(data)
    h=0.0
    for count in freq:
        if count>0:
            p=count/length
            h -= p*math.log2(p)
    return h

def _he_seed(state, content_type, target_size):
    seed_str=f"{state}:{content_type}:{target_size}:he_seed"
    digest=hashlib.sha256(seed_str.encode("utf-8")).digest()
    return int.from_bytes(digest[:4],"big")

def generate_json_he_body(state, target_size):
    rng=random.Random(_he_seed(state,"JSON",target_size))
    if state in ("no_auth","expired_token","invalid_token"):
        entries=[]
        current_size=0
        header=json.dumps({"error":"invalid_token","entries":[]}).encode("utf-8")
        current_size=len(header)
        while current_size < target_size:
            uuid_val=str(uuid.uuid5(uuid.NAMESPACE_DNS,f"{state}:{rng.getrandbits(64)}"))
            entry={"id":uuid_val,"key":rng.getrandbits(64).to_bytes(8,"big").hex(),"score":round(rng.uniform(-1000.0,1000.0),6),"tag":f"tag_{rng.randint(0,999999):06d}","desc":" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(3,8))),"active":rng.choice([True,False]),"nested":{"a":round(rng.uniform(0.0,1.0),8),"b":rng.getrandbits(32),"c":uuid_val}}
            entry_json=json.dumps(entry)
            entry_bytes=entry_json.encode("utf-8")
            if current_size+len(entry_bytes)+1>target_size:
                break
            entries.append(entry)
            current_size+=len(entry_bytes)+1
        base={"error":"invalid_token","entries":entries}
        raw=json.dumps(base, separators=(",",":")).encode("utf-8")
    else:
        entries=[]
        current_size=0
        while current_size < target_size:
            uuid_val=str(uuid.uuid5(uuid.NAMESPACE_DNS,f"{state}:{rng.getrandbits(64)}"))
            entry={"sub":uuid_val,"name":" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(2,4))),"email":f"{uuid_val[:8]}@{rng.choice(HTML_WORDS)}.example.com","scope":" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(2,6))),"score":round(rng.uniform(-1000.0,1000.0),6),"tag":f"tag_{rng.randint(0,999999):06d}","desc":" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(4,12))),"active":rng.choice([True,False]),"nested":{"x":round(rng.uniform(0.0,1.0),8),"y":rng.getrandbits(32),"z":uuid_val}}
            entry_json=json.dumps(entry)
            entry_bytes=entry_json.encode("utf-8")
            if current_size+len(entry_bytes)+1>target_size:
                break
            entries.append(entry)
            current_size+=len(entry_bytes)+1
        base={"sub":"alice","name":"Alice","entries":entries}
        raw=json.dumps(base, separators=(",",":")).encode("utf-8")
    if len(raw)<target_size:
        padding_needed=target_size-len(raw)
        pad_bytes=bytes(rng.getrandbits(8) for _ in range(padding_needed))
        raw=raw+pad_bytes[:padding_needed]
    return raw[:target_size]

def generate_html_he_body(state, target_size):
    rng=random.Random(_he_seed(state,"HTML",target_size))
    sections=[]
    sections.append("<!DOCTYPE html>")
    sections.append('<html lang="en">')
    sections.append("<head>")
    sections.append('<meta charset="UTF-8">')
    sections.append(f'<title>High-Entropy Document - {state}</title>')
    sections.append("</head>")
    sections.append("<body>")
    sections.append(f'<div class="auth-state" data-state="{state}">')
    section_id=0
    current_size=sum(len(s.encode("utf-8")) for s in sections)
    while current_size < target_size:
        uuid_val=str(uuid.uuid5(uuid.NAMESPACE_DNS,f"{state}:{rng.getrandbits(64)}"))
        word_count=rng.randint(20,60)
        words=[rng.choice(HTML_WORDS) for _ in range(word_count)]
        paragraph=" ".join(words)+"."
        header_text=" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(3,6))).title()
        section=(f'<section id="s{section_id}" data-uuid="{uuid_val}">\n<h{rng.randint(2,4)}>{header_text}</h{rng.randint(2,4)}>\n<p>{paragraph}</p>\n<p>'+" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(15,40)))+".</p>\n</section>\n")
        section_bytes=section.encode("utf-8")
        if current_size+len(section_bytes)>target_size:
            break
        sections.append(section)
        current_size+=len(section_bytes)
        section_id+=1
    sections.append("</div>")
    sections.append("</body>")
    sections.append("</html>")
    raw="\n".join(sections).encode("utf-8")
    if len(raw)<target_size:
        padding_needed=target_size-len(raw)
        pad_words=[]
        while sum(len(w.encode("utf-8"))+1 for w in pad_words)<padding_needed:
            pad_words.append(rng.choice(HTML_WORDS))
        padding=(" ".join(pad_words)).encode("utf-8")[:padding_needed]
        raw=raw+padding
    return raw[:target_size]

def generate_binary_he_body(state, target_size):
    rng=random.Random(_he_seed(state,"BINARY",target_size))
    magic=b'\x89SPIDER\x01\x02'
    version=struct.pack(">I",1)
    state_bytes=struct.pack(">I",hash(state)&0xFFFFFFFF)
    header=magic+version+state_bytes
    current_size=len(header)
    entries=[]
    while current_size < target_size:
        key=rng.getrandbits(64).to_bytes(8,"big")
        payload_len=rng.randint(4,32)
        payload=bytes(rng.getrandbits(8) for _ in range(payload_len))
        entry=key+struct.pack(">I",payload_len)+payload
        if current_size+len(entry)+4>target_size:
            break
        entries.append(entry)
        current_size+=len(entry)+4
    raw=header
    for entry in entries:
        raw+=entry
        crc=binascii.crc32(entry)&0xFFFFFFFF
        raw+=struct.pack(">I",crc)
    if len(raw)<target_size:
        padding_needed=target_size-len(raw)
        pad_bytes=bytes(rng.getrandbits(8) for _ in range(padding_needed))
        raw=raw+pad_bytes[:padding_needed]
    return raw[:target_size]

BODY_GENERATORS={"JSON":generate_json_he_body,"HTML":generate_html_he_body,"BINARY":generate_binary_he_body}

def validate_entropy_pre_flight():
    results={}
    for ct_name in CONTENT_TYPES:
        entropies=[]
        for state in AUTH_STATES:
            for size_name,target_size in TARGET_SIZES.items():
                gen=BODY_GENERATORS[ct_name]
                body=gen(state,target_size)
                h=compute_shannon_entropy(body)
                entropies.append(h)
        mean_ent=sum(entropies)/len(entropies) if entropies else 0.0
        min_ent=min(entropies) if entropies else 0.0
        max_ent=max(entropies) if entropies else 0.0
        results[ct_name]={"mean_entropy":mean_ent,"min_entropy":min_ent,"max_entropy":max_ent,"all_above_threshold":all(h>=SHANNON_ENTROPY_MIN for h in entropies)}
    return results

def make_valid_token():
    now=datetime.now(timezone.utc)
    payload={"sub":"alice","name":"Alice","email":"alice@example.com","iat":int(now.timestamp()),"exp":int((now+timedelta(hours=1)).timestamp()),"realm_access":{"roles":["user"]}}
    return jwt.encode(payload,CLIENT_SECRET,algorithm="HS256")
def make_expired_token():
    now=datetime.now(timezone.utc)
    payload={"sub":"alice","name":"Alice","email":"alice@example.com","iat":int((now-timedelta(hours=2)).timestamp()),"exp":int((now-timedelta(hours=1)).timestamp()),"realm_access":{"roles":["user"]}}
    return jwt.encode(payload,CLIENT_SECRET,algorithm="HS256")
def make_invalid_token():
    return "invalid-token-12345"

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address=True

class MockOAuthHandler(BaseHTTPRequestHandler):
    body_size=1024
    content_type="JSON"
    layers=[]
    use_chunked=True
    chunk_size=32
    def log_message(self,format,*args): pass
    def _get_auth_state(self):
        auth=self.headers.get("Authorization","")
        if not auth.startswith("Bearer "): return "no_auth"
        token=auth[7:]
        try:
            jwt.decode(token,CLIENT_SECRET,algorithms=["HS256"])
            return "valid_token"
        except jwt.ExpiredSignatureError: return "expired_token"
        except jwt.InvalidTokenError: return "invalid_token"
        return "no_auth"
    def _get_body(self,state,size):
        gen=BODY_GENERATORS.get(self.content_type,generate_json_he_body)
        return gen(state,size)
    def _get_mime_type(self):
        return CONTENT_TYPES.get(self.content_type,"application/json")
    def _apply_layers(self,body):
        current_data=body
        ce_parts=[]
        for layer in MockOAuthHandler.layers:
            if layer["type"]=="gzip":
                if layer.get("level") is not None:
                    current_data=gzip.compress(current_data,compresslevel=layer["level"])
                else:
                    current_data=gzip.compress(current_data)
                ce_parts.append("gzip")
            elif layer["type"]=="brotli":
                quality=layer.get("quality",6)
                current_data=brotli.compress(current_data,quality=quality)
                ce_parts.append("br")
        ce_header=", ".join(ce_parts) if ce_parts else "identity"
        return current_data, ce_header
    def do_GET(self):
        if self.path==USERINFO_PATH:
            state=self._get_auth_state()
            body=self._get_body(state,self.body_size)
            status=200 if state=="valid_token" else 401
            if MockOAuthHandler.layers:
                compressed,ce_header=self._apply_layers(body)
                self.send_response(status)
                self.send_header("Content-Type",self._get_mime_type())
                self.send_header("Content-Encoding",ce_header)
                self.send_header("Cache-Control","private")
                self.send_header("Vary","Authorization")
                if self.use_chunked:
                    self.send_header("Transfer-Encoding","chunked")
                    self.end_headers()
                    chunk_size=self.chunk_size
                    offset=0
                    while offset < len(compressed):
                        chunk=compressed[offset:offset+chunk_size]
                        self.wfile.write(("{:x}\r\n".format(len(chunk))).encode())
                        self.wfile.write(chunk)
                        self.wfile.write(b"\r\n")
                        offset+=chunk_size
                    self.wfile.write(b"0\r\n\r\n")
                else:
                    self.send_header("Content-Length",len(compressed))
                    self.end_headers()
                    self.wfile.write(compressed)
            else:
                self.send_response(status)
                self.send_header("Content-Type",self._get_mime_type())
                self.send_header("Content-Length",len(body))
                self.send_header("Cache-Control","private")
                self.send_header("Vary","Authorization")
                self.end_headers()
                self.wfile.write(body)
            self.wfile.flush()
        else:
            self.send_error(404)
    def do_POST(self): self.send_error(404)

def start_mock_server(port, body_size=1024, content_type="JSON", layers=None, use_chunked=True, chunk_size=32):
    MockOAuthHandler.body_size=body_size
    MockOAuthHandler.content_type=content_type
    MockOAuthHandler.layers=layers or []
    MockOAuthHandler.use_chunked=use_chunked
    MockOAuthHandler.chunk_size=chunk_size
    server=ReusableHTTPServer(("127.0.0.1",port),MockOAuthHandler)
    server.timeout=0.5
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    return server
def stop_mock_server(server):
    if server:
        server.shutdown()
        server.server_close()
        time.sleep(0.2)

# Buffered proxy (parent behavior)
class BufferedProxyHandler(BaseHTTPRequestHandler):
    upstream_host="127.0.0.1"
    upstream_port=5400
    chunk_size=32
    def log_message(self,format,*args): pass
    def _proxy_request(self,method="GET"):
        content_length=int(self.headers.get("Content-Length",0))
        req_body=self.rfile.read(content_length) if content_length>0 else None
        headers={}
        for key in self.headers:
            if key.lower() not in ("host","connection"):
                headers[key]=self.headers[key]
        if "Accept-Encoding" not in headers and "accept-encoding" not in headers:
            headers["Accept-Encoding"]="br, gzip, identity"
        try:
            conn=HTTPConnection(BufferedProxyHandler.upstream_host,BufferedProxyHandler.upstream_port,timeout=30)
            conn.request(method,self.path,body=req_body,headers=headers)
            upstream_resp=conn.getresponse()
            resp_status=upstream_resp.status
            resp_headers=dict(upstream_resp.getheaders())
            resp_body=upstream_resp.read()
            conn.close()
            self.send_response(resp_status)
            for key,value in resp_headers.items():
                if key.lower() not in ("content-length","transfer-encoding","connection"):
                    self.send_header(key,value)
            self.send_header("X-Proxy-Mode","BUFFERED-PROXY")
            self.send_header("X-Cache","MISS")
            self.send_header("Transfer-Encoding","chunked")
            self.end_headers()
            chunk_size=BufferedProxyHandler.chunk_size
            offset=0
            while offset < len(resp_body):
                chunk=resp_body[offset:offset+chunk_size]
                self.wfile.write(("{:x}\r\n".format(len(chunk))).encode())
                self.wfile.write(chunk)
                self.wfile.write(b"\r\n")
                offset+=chunk_size
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
        except Exception as e:
            self.send_error(502,f"Proxy error: {e}")
    def do_GET(self): self._proxy_request("GET")
    def do_POST(self): self._proxy_request("POST")

def start_buffered_proxy(port, upstream_port, chunk_size=32):
    BufferedProxyHandler.upstream_port=upstream_port
    BufferedProxyHandler.chunk_size=chunk_size
    server=ReusableHTTPServer(("127.0.0.1",port),BufferedProxyHandler)
    server.timeout=0.5
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    return server
def stop_buffered_proxy(server):
    if server:
        server.shutdown()
        server.server_close()
        time.sleep(0.2)

# Streaming proxy (new)
class StreamingProxyHandler(BaseHTTPRequestHandler):
    upstream_host="127.0.0.1"
    upstream_port=5400
    stream_chunk_size=8192
    def log_message(self,format,*args): pass
    def _proxy_request(self,method="GET"):
        content_length=int(self.headers.get("Content-Length",0))
        req_body=self.rfile.read(content_length) if content_length>0 else None
        headers={}
        for key in self.headers:
            if key.lower() not in ("host","connection"):
                headers[key]=self.headers[key]
        if "Accept-Encoding" not in headers and "accept-encoding" not in headers:
            headers["Accept-Encoding"]="br, gzip, identity"
        try:
            conn=HTTPConnection(StreamingProxyHandler.upstream_host,StreamingProxyHandler.upstream_port,timeout=30)
            conn.request(method,self.path,body=req_body,headers=headers)
            upstream_resp=conn.getresponse()
            resp_status=upstream_resp.status
            resp_headers=dict(upstream_resp.getheaders())
            self.send_response(resp_status)
            for key,value in resp_headers.items():
                if key.lower() not in ("content-length","transfer-encoding","connection"):
                    self.send_header(key,value)
            self.send_header("X-Proxy-Mode","STREAMING-PROXY")
            self.send_header("X-Cache","MISS")
            self.send_header("Transfer-Encoding","chunked")
            self.end_headers()
            # Stream incrementally without buffering full body
            while True:
                chunk=upstream_resp.read(StreamingProxyHandler.stream_chunk_size)
                if not chunk:
                    break
                self.wfile.write(("{:x}\r\n".format(len(chunk))).encode())
                self.wfile.write(chunk)
                self.wfile.write(b"\r\n")
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
            conn.close()
        except Exception as e:
            try:
                self.send_error(502,f"Proxy error: {e}")
            except: pass
    def do_GET(self): self._proxy_request("GET")
    def do_POST(self): self._proxy_request("POST")

def start_streaming_proxy(port, upstream_port, stream_chunk_size=8192):
    StreamingProxyHandler.upstream_port=upstream_port
    StreamingProxyHandler.stream_chunk_size=stream_chunk_size
    server=ReusableHTTPServer(("127.0.0.1",port),StreamingProxyHandler)
    server.timeout=0.5
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    return server
def stop_streaming_proxy(server):
    if server:
        server.shutdown()
        server.server_close()
        time.sleep(0.2)

def decompress_body(raw_body, content_encoding):
    MAX_DEPTH=5
    current_data=raw_body
    depth=0
    while depth<MAX_DEPTH:
        try:
            current_data=brotli.decompress(current_data)
            depth+=1
            continue
        except Exception: pass
        try:
            current_data=gzip.decompress(current_data)
            depth+=1
            continue
        except Exception: pass
        break
    return current_data

def get_auth_header(state, auth_token):
    if state=="no_auth": return None
    elif state=="valid_token": return f"Bearer {auth_token}"
    elif state=="expired_token": return f"Bearer {make_expired_token()}"
    elif state=="invalid_token": return f"Bearer {make_invalid_token()}"
    return None

def make_request_streaming(url, auth_header=None, stream_chunk_size=8192, timeout=30):
    headers={"Accept-Encoding":"br, gzip, identity"}
    if auth_header:
        headers["Authorization"]=auth_header
    start=time.monotonic()
    try:
        resp=requests.get(url,headers=headers,timeout=timeout,allow_redirects=True,stream=True)
        # incremental read
        chunks=[]
        while True:
            chunk=resp.raw.read(stream_chunk_size)
            if not chunk:
                break
            chunks.append(chunk)
        raw_bytes=b"".join(chunks)
        resp_status=resp.status_code
        resp_headers=dict(resp.headers)
        elapsed=time.monotonic()-start
        return {"url":url,"status":resp_status,"headers":resp_headers,"body":raw_bytes,"elapsed":elapsed,"timestamp":time.time()}
    except Exception as e:
        elapsed=time.monotonic()-start
        return {"url":url,"status":0,"headers":{},"body":str(e).encode("utf-8"),"elapsed":elapsed,"timestamp":time.time(),"error":str(e)}

def make_request_buffered(url, auth_header=None, timeout=30):
    headers={"Accept-Encoding":"br, gzip, identity"}
    if auth_header:
        headers["Authorization"]=auth_header
    start=time.monotonic()
    try:
        resp=requests.get(url,headers=headers,timeout=timeout,allow_redirects=True,stream=True)
        raw_bytes=resp.raw.read(decode_content=False)
        resp_status=resp.status_code
        resp_headers=dict(resp.headers)
        elapsed=time.monotonic()-start
        return {"url":url,"status":resp_status,"headers":resp_headers,"body":raw_bytes,"elapsed":elapsed,"timestamp":time.time()}
    except Exception as e:
        elapsed=time.monotonic()-start
        return {"url":url,"status":0,"headers":{},"body":str(e).encode("utf-8"),"elapsed":elapsed,"timestamp":time.time(),"error":str(e)}

def run_single_cell_comparison(port_idx, ct_name, comp_mode, comp_config, target_size, stream_chunk_size, auth_token, rng):
    layers=comp_config["layers"]
    use_chunked=comp_config.get("use_chunked",True)
    chunk_size_for_origin=32  # origin always chunked at 32 as parent
    origin_port=BASE_PORT+port_idx
    mock_server=start_mock_server(origin_port,target_size,ct_name,layers=layers,use_chunked=use_chunked,chunk_size=chunk_size_for_origin)
    time.sleep(0.4)
    stream_proxy_port=STREAM_PROXY_PORT_BASE+port_idx
    buffered_proxy_port=BUFFERED_PROXY_PORT_BASE+port_idx
    stream_proxy=start_streaming_proxy(stream_proxy_port,origin_port,stream_chunk_size=stream_chunk_size)
    buffered_proxy=start_buffered_proxy(buffered_proxy_port,origin_port,chunk_size=32)
    time.sleep(0.4)
    # connectivity test
    try:
        test_resp=requests.get(f"http://127.0.0.1:{stream_proxy_port}{USERINFO_PATH}",headers={"Authorization":f"Bearer {auth_token}","Accept-Encoding":"br, gzip, identity"},timeout=10)
        test_resp2=requests.get(f"http://127.0.0.1:{buffered_proxy_port}{USERINFO_PATH}",headers={"Authorization":f"Bearer {auth_token}","Accept-Encoding":"br, gzip, identity"},timeout=10)
    except Exception as e:
        stop_streaming_proxy(stream_proxy)
        stop_buffered_proxy(buffered_proxy)
        stop_mock_server(mock_server)
        return None, f"Connectivity failed: {e}"
    plan=[]
    for state in AUTH_STATES:
        for rep in range(REPS):
            plan.append((state,rep))
    rng.shuffle(plan)
    # storage
    cell_observations=[]
    per_state_streaming_hashes=defaultdict(list)
    per_state_buffered_hashes=defaultdict(list)
    per_state_expected_hashes={}
    correctness_streaming=[]
    correctness_buffered=[]
    streaming_equals_buffered_list=[]
    silent_fallbacks_streaming=0
    decompression_errors_streaming=[]
    decompression_errors_buffered=[]
    compressed_sizes=[]
    latencies_streaming=[]
    latencies_buffered=[]
    streaming_proxy_mode_ok=True
    buffered_proxy_mode_ok=True
    for state,rep in plan:
        auth_header=get_auth_header(state,auth_token)
        gen=BODY_GENERATORS.get(ct_name,generate_json_he_body)
        expected_body=gen(state,target_size)
        expected_hash=hashlib.sha256(expected_body).hexdigest()
        if state not in per_state_expected_hashes:
            per_state_expected_hashes[state]=expected_hash
        url_stream=f"http://127.0.0.1:{stream_proxy_port}{USERINFO_PATH}"
        url_buf=f"http://127.0.0.1:{buffered_proxy_port}{USERINFO_PATH}"
        obs_s=make_request_streaming(url_stream,auth_header=auth_header,stream_chunk_size=stream_chunk_size)
        obs_b=make_request_buffered(url_buf,auth_header=auth_header)
        # record sizes
        compressed_sizes.append(len(obs_s["body"]))
        # decompress streaming
        ce_s=obs_s["headers"].get("Content-Encoding","none")
        start=time.monotonic()
        try:
            decomp_s=decompress_body(obs_s["body"],ce_s)
            lat_s=(time.monotonic()-start)*1000
            decomp_hash_s=hashlib.sha256(decomp_s).hexdigest()
            err_s=None
        except Exception as e:
            lat_s=(time.monotonic()-start)*1000
            decomp_hash_s=hashlib.sha256(obs_s["body"]).hexdigest()
            err_s=str(e)
            decompression_errors_streaming.append({"state":state,"rep":rep,"error":err_s})
        # decompress buffered
        ce_b=obs_b["headers"].get("Content-Encoding","none")
        start=time.monotonic()
        try:
            decomp_b=decompress_body(obs_b["body"],ce_b)
            lat_b=(time.monotonic()-start)*1000
            decomp_hash_b=hashlib.sha256(decomp_b).hexdigest()
            err_b=None
        except Exception as e:
            lat_b=(time.monotonic()-start)*1000
            decomp_hash_b=hashlib.sha256(obs_b["body"]).hexdigest()
            err_b=str(e)
            decompression_errors_buffered.append({"state":state,"rep":rep,"error":err_b})
        latencies_streaming.append(lat_s)
        latencies_buffered.append(lat_b)
        per_state_streaming_hashes[state].append(decomp_hash_s)
        per_state_buffered_hashes[state].append(decomp_hash_b)
        # checks
        streaming_match_expected=(decomp_hash_s==expected_hash)
        buffered_match_expected=(decomp_hash_b==expected_hash)
        streaming_equals_buffered=(decomp_hash_s==decomp_hash_b)
        correctness_streaming.append(streaming_match_expected)
        correctness_buffered.append(buffered_match_expected)
        streaming_equals_buffered_list.append(streaming_equals_buffered)
        # silent fallback detection for streaming
        is_compressed_s=ce_s in ("br","gzip","br, gzip","gzip, br")
        # more robust: check if ce contains br or gzip
        if ce_s != "none" and ce_s != "identity":
            # streaming decompressed equals raw compressed?
            body_hash_compressed=hashlib.sha256(obs_s["body"]).hexdigest()
            if decomp_hash_s==body_hash_compressed:
                silent_fallbacks_streaming+=1
        # proxy mode check
        if obs_s["headers"].get("X-Proxy-Mode")!="STREAMING-PROXY":
            streaming_proxy_mode_ok=False
        if obs_b["headers"].get("X-Proxy-Mode")!="BUFFERED-PROXY":
            buffered_proxy_mode_ok=False
        # observation record
        body_hash_s=hashlib.sha256(obs_s["body"]).hexdigest()
        body_hash_b=hashlib.sha256(obs_b["body"]).hexdigest()
        cell_observations.append({
            "state":state,"rep":rep,"expected_hash":expected_hash,
            "streaming_body_hash":body_hash_s,"buffered_body_hash":body_hash_b,
            "streaming_decompressed_hash":decomp_hash_s,"buffered_decompressed_hash":decomp_hash_b,
            "streaming_match_expected":streaming_match_expected,"buffered_match_expected":buffered_match_expected,
            "streaming_equals_buffered":streaming_equals_buffered,
            "streaming_decompression_error":err_s,"buffered_decompression_error":err_b,
            "streaming_compressed_size":len(obs_s["body"]),"buffered_compressed_size":len(obs_b["body"]),
            "streaming_ce":ce_s,"buffered_ce":ce_b,
            "streaming_latency_ms":lat_s,"buffered_latency_ms":lat_b,
        })
        # jitter
        jitter=rng.uniform(0.02,0.08)
        time.sleep(jitter)
    # aggregate per-state variation for streaming
    streaming_hash_variation={}
    for state in AUTH_STATES:
        hashes=per_state_streaming_hashes[state]
        streaming_hash_variation[state]={"unique_count":len(set(hashes)),"total":len(hashes),"all_same":len(set(hashes))==1}
    buffered_hash_variation={}
    for state in AUTH_STATES:
        hashes=per_state_buffered_hashes[state]
        buffered_hash_variation[state]={"unique_count":len(set(hashes)),"total":len(hashes),"all_same":len(set(hashes))==1}
    correctness_by_state_streaming={}
    correctness_by_state_buffered={}
    for state in AUTH_STATES:
        # filter observations for state
        obs_for_state=[o for o in cell_observations if o["state"]==state]
        correctness_by_state_streaming[state]={"pass_count":sum(1 for o in obs_for_state if o["streaming_match_expected"]),"fail_count":sum(1 for o in obs_for_state if not o["streaming_match_expected"]),"total":len(obs_for_state),"all_pass":all(o["streaming_match_expected"] for o in obs_for_state)}
        correctness_by_state_buffered[state]={"pass_count":sum(1 for o in obs_for_state if o["buffered_match_expected"]),"fail_count":sum(1 for o in obs_for_state if not o["buffered_match_expected"]),"total":len(obs_for_state),"all_pass":all(o["buffered_match_expected"] for o in obs_for_state)}
    # compressed size stats from streaming
    mean_size=sum(compressed_sizes)/len(compressed_sizes) if compressed_sizes else 0
    cell_key=f"{ct_name}_{comp_mode}_{target_size}B_chunk{stream_chunk_size}"
    cell_data={
        "content_type":ct_name,"comp_mode":comp_mode,"target_size":target_size,"stream_chunk_size":stream_chunk_size,
        "total_requests":len(cell_observations),
        "streaming_correctness_match_count":sum(correctness_streaming),
        "streaming_correctness_match_rate":sum(correctness_streaming)/len(correctness_streaming) if correctness_streaming else 0,
        "buffered_correctness_match_count":sum(correctness_buffered),
        "buffered_correctness_match_rate":sum(correctness_buffered)/len(correctness_buffered) if correctness_buffered else 0,
        "streaming_equals_buffered_count":sum(streaming_equals_buffered_list),
        "streaming_equals_buffered_rate":sum(streaming_equals_buffered_list)/len(streaming_equals_buffered_list) if streaming_equals_buffered_list else 0,
        "silent_fallback_count_streaming":silent_fallbacks_streaming,
        "decompression_error_count_streaming":len(decompression_errors_streaming),
        "decompression_error_count_buffered":len(decompression_errors_buffered),
        "decompression_errors_streaming":decompression_errors_streaming,
        "decompression_errors_buffered":decompression_errors_buffered,
        "streaming_hash_variation":streaming_hash_variation,
        "buffered_hash_variation":buffered_hash_variation,
        "correctness_by_state_streaming":correctness_by_state_streaming,
        "correctness_by_state_buffered":correctness_by_state_buffered,
        "compressed_size_bytes":{"mean":mean_size,"min":min(compressed_sizes) if compressed_sizes else 0,"max":max(compressed_sizes) if compressed_sizes else 0},
        "decompression_latency_ms_streaming":{"mean":sum(latencies_streaming)/len(latencies_streaming) if latencies_streaming else 0,"min":min(latencies_streaming) if latencies_streaming else 0,"max":max(latencies_streaming) if latencies_streaming else 0},
        "decompression_latency_ms_buffered":{"mean":sum(latencies_buffered)/len(latencies_buffered) if latencies_buffered else 0,"min":min(latencies_buffered) if latencies_buffered else 0,"max":max(latencies_buffered) if latencies_buffered else 0},
        "proxy_mode_ok":{"streaming":streaming_proxy_mode_ok,"buffered":buffered_proxy_mode_ok},
        "observations":cell_observations,
    }
    stop_streaming_proxy(stream_proxy)
    stop_buffered_proxy(buffered_proxy)
    stop_mock_server(mock_server)
    time.sleep(0.2)
    return cell_key, cell_data

def run_single_identity(port_idx, ct_name, target_size, auth_token, rng):
    # identity baseline through streaming proxy (also tests buffered)
    layers=[]
    origin_port=BASE_PORT+port_idx
    mock_server=start_mock_server(origin_port,target_size,ct_name,layers=layers,use_chunked=False,chunk_size=1024)
    time.sleep(0.4)
    # use streaming proxy with 8192 chunk
    stream_proxy_port=STREAM_PROXY_PORT_BASE+port_idx
    buffered_proxy_port=BUFFERED_PROXY_PORT_BASE+port_idx
    stream_proxy=start_streaming_proxy(stream_proxy_port,origin_port,stream_chunk_size=8192)
    buffered_proxy=start_buffered_proxy(buffered_proxy_port,origin_port,chunk_size=32)
    time.sleep(0.4)
    plan=[(s,r) for s in AUTH_STATES for r in range(REPS)]
    rng.shuffle(plan)
    observations=[]
    correctness_streaming=[]
    correctness_buffered=[]
    streaming_hash_variation_data=defaultdict(list)
    buffered_hash_variation_data=defaultdict(list)
    compressed_sizes=[]
    for state,rep in plan:
        auth_header=get_auth_header(state,auth_token)
        expected_body=BODY_GENERATORS[ct_name](state,target_size)
        expected_hash=hashlib.sha256(expected_body).hexdigest()
        obs_s=make_request_streaming(f"http://127.0.0.1:{stream_proxy_port}{USERINFO_PATH}",auth_header=auth_header,stream_chunk_size=8192)
        obs_b=make_request_buffered(f"http://127.0.0.1:{buffered_proxy_port}{USERINFO_PATH}",auth_header=auth_header)
        decomp_s=decompress_body(obs_s["body"],obs_s["headers"].get("Content-Encoding","none"))
        decomp_b=decompress_body(obs_b["body"],obs_b["headers"].get("Content-Encoding","none"))
        hash_s=hashlib.sha256(decomp_s).hexdigest()
        hash_b=hashlib.sha256(decomp_b).hexdigest()
        correctness_streaming.append(hash_s==expected_hash)
        correctness_buffered.append(hash_b==expected_hash)
        streaming_hash_variation_data[state].append(hash_s)
        buffered_hash_variation_data[state].append(hash_b)
        compressed_sizes.append(len(obs_s["body"]))
        observations.append({"state":state,"rep":rep,"expected_hash":expected_hash,"streaming_hash":hash_s,"buffered_hash":hash_b,"streaming_match":hash_s==expected_hash,"buffered_match":hash_b==expected_hash})
        time.sleep(rng.uniform(0.02,0.05))
    streaming_variation={s:{"unique_count":len(set(v)),"total":len(v),"all_same":len(set(v))==1} for s,v in streaming_hash_variation_data.items()}
    buffered_variation={s:{"unique_count":len(set(v)),"total":len(v),"all_same":len(set(v))==1} for s,v in buffered_hash_variation_data.items()}
    # correctness by state
    c_by_state_stream={}
    c_by_state_buf={}
    for state in AUTH_STATES:
        obs_states=[o for o in observations if o["state"]==state]
        c_by_state_stream[state]={"pass_count":sum(1 for o in obs_states if o["streaming_match"]),"fail_count":sum(1 for o in obs_states if not o["streaming_match"]),"total":len(obs_states),"all_pass":all(o["streaming_match"] for o in obs_states)}
        c_by_state_buf[state]={"pass_count":sum(1 for o in obs_states if o["buffered_match"]),"fail_count":sum(1 for o in obs_states if not o["buffered_match"]),"total":len(obs_states),"all_pass":all(o["buffered_match"] for o in obs_states)}
    cell_key=f"{ct_name}_IDENTITY-{target_size}_{target_size}B"
    cell_data={
        "total_requests":len(observations),
        "streaming_correctness_match_count":sum(correctness_streaming),
        "streaming_correctness_match_rate":sum(correctness_streaming)/len(correctness_streaming) if correctness_streaming else 0,
        "buffered_correctness_match_count":sum(correctness_buffered),
        "buffered_correctness_match_rate":sum(correctness_buffered)/len(correctness_buffered) if correctness_buffered else 0,
        "streaming_hash_variation":streaming_variation,
        "buffered_hash_variation":buffered_variation,
        "correctness_by_state_streaming":c_by_state_stream,
        "correctness_by_state_buffered":c_by_state_buf,
        "compressed_size_bytes":{"mean":sum(compressed_sizes)/len(compressed_sizes) if compressed_sizes else 0,"min":min(compressed_sizes) if compressed_sizes else 0,"max":max(compressed_sizes) if compressed_sizes else 0},
        "observations":observations,
    }
    stop_streaming_proxy(stream_proxy)
    stop_buffered_proxy(buffered_proxy)
    stop_mock_server(mock_server)
    time.sleep(0.2)
    return cell_key, cell_data

def run_experiment():
    all_results={}
    all_observations_desc=[]
    errors=[]
    all_results["entropy_preflight"]=validate_entropy_pre_flight()
    print("Entropy preflight:", all_results["entropy_preflight"])
    entropy_fail=any(not v["all_above_threshold"] for v in all_results["entropy_preflight"].values())
    if entropy_fail:
        print("MEASUREMENT_INVALID entropy")
        sys.exit(1)
    auth_token=make_valid_token()
    rng=random.Random(SEED)
    port_idx=0
    print("PHASE MAIN: multi-layer streaming cells (24 cells)")
    main_cells={}
    for size_name,target_size in TARGET_SIZES.items():
        for ct_name in CONTENT_TYPES.keys():
            for comp_mode,comp_config in MULTI_LAYER_MODES.items():
                for chunk_size in STREAM_CHUNK_SIZES:
                    cell_key,cell_data=run_single_cell_comparison(port_idx,ct_name,comp_mode,comp_config,target_size,chunk_size,auth_token,rng)
                    port_idx+=1
                    if cell_data is None:
                        errors.append(cell_key)
                        continue
                    all_results[cell_key]=cell_data
                    main_cells[cell_key]=cell_data
                    print(f"  {cell_key}: streaming_correct={cell_data['streaming_correctness_match_rate']:.3f} buffered_correct={cell_data['buffered_correctness_match_rate']:.3f} equals={cell_data['streaming_equals_buffered_rate']:.3f} size_mean={cell_data['compressed_size_bytes']['mean']:.0f}")
    print("PHASE REGRESSION: single-layer 6 cells x 2 chunk sizes = 12 cells")
    regression_cells={}
    for ct_name in CONTENT_TYPES.keys():
        for comp_mode,comp_config in REGRESSION_MODES.items():
            for chunk_size in STREAM_CHUNK_SIZES:
                cell_key,cell_data=run_single_cell_comparison(port_idx,ct_name,comp_mode,comp_config,10240,chunk_size,auth_token,rng)
                port_idx+=1
                if cell_data is None:
                    errors.append(cell_key)
                    continue
                all_results[cell_key]=cell_data
                regression_cells[cell_key]=cell_data
                print(f"  {cell_key}: streaming={cell_data['streaming_correctness_match_rate']:.3f} buffered={cell_data['buffered_correctness_match_rate']:.3f} equals={cell_data['streaming_equals_buffered_rate']:.3f}")
    print("PHASE IDENTITY: 6 cells")
    identity_cells={}
    for size_name,target_size in TARGET_SIZES.items():
        for ct_name in CONTENT_TYPES.keys():
            cell_key,cell_data=run_single_identity(port_idx,ct_name,target_size,auth_token,rng)
            port_idx+=1
            if cell_data is None:
                errors.append(cell_key)
                continue
            all_results[cell_key]=cell_data
            identity_cells[cell_key]=cell_data
            print(f"  {cell_key}: streaming={cell_data['streaming_correctness_match_rate']:.3f} buffered={cell_data['buffered_correctness_match_rate']:.3f}")
    # Controls evaluation per spec
    # C1 streaming == buffered for all multi-layer streaming cells
    c1_pass=all(v["streaming_equals_buffered_rate"]==1.0 for v in main_cells.values())
    # C2 streaming == expected for all multi-layer
    c2_pass=all(v["streaming_correctness_match_rate"]==1.0 for v in main_cells.values())
    # C3 regression controls pass 100% in both paths
    # Need GZIP-SINGLE and BROTLI-SINGLE pass 100% in both buffered and streaming
    gzip_cells={k:v for k,v in regression_cells.items() if "GZIP-SINGLE" in k}
    brotli_cells={k:v for k,v in regression_cells.items() if "BROTLI-SINGLE" in k}
    c3_gzip_pass=all(v["streaming_correctness_match_rate"]==1.0 and v["buffered_correctness_match_rate"]==1.0 for v in gzip_cells.values())
    c3_brotli_pass=all(v["streaming_correctness_match_rate"]==1.0 and v["buffered_correctness_match_rate"]==1.0 for v in brotli_cells.values())
    c3_pass=c3_gzip_pass and c3_brotli_pass
    # C4 null_control all_same true for all states in all streaming cells (main + regression)
    c4_pass=True
    for cell_key,cell_data in {**main_cells,**regression_cells}.items():
        for state,hv in cell_data["streaming_hash_variation"].items():
            if not hv["all_same"]:
                c4_pass=False
        for state,hv in cell_data["buffered_hash_variation"].items():
            if not hv["all_same"]:
                c4_pass=False
    # C5 compressed target range: at least 2/3 types achieve mean >=2000 at 10KB and >=5000 at 100KB for streaming multi-layer
    compressed_target={}
    for ct_name in CONTENT_TYPES:
        sizes_10k=[]
        sizes_100k=[]
        for k,v in main_cells.items():
            if k.startswith(ct_name+"_") and "GZIP-THEN-BROTLI" in k or k.startswith(ct_name+"_") and "BROTLI-THEN-GZIP" in k:
                # but filter by content type prefix
                pass
        # simpler: collect per type correctly
    # recompute correctly
    compressed_target={}
    for ct_name in CONTENT_TYPES:
        vals_10k=[]
        vals_100k=[]
        for k,v in main_cells.items():
            if not k.startswith(ct_name+"_"): continue
            if "_10240B_" in k:
                vals_10k.append(v["compressed_size_bytes"]["mean"])
            elif "_102400B_" in k:
                vals_100k.append(v["compressed_size_bytes"]["mean"])
        mean_10k=sum(vals_10k)/len(vals_10k) if vals_10k else 0
        mean_100k=sum(vals_100k)/len(vals_100k) if vals_100k else 0
        compressed_target[ct_name]={"mean_compressed_10KB":mean_10k,"mean_compressed_100KB":mean_100k,"meets_10KB":mean_10k>=2000,"meets_100KB":mean_100k>=5000}
    meets_10k=sum(1 for r in compressed_target.values() if r["meets_10KB"])
    meets_100k=sum(1 for r in compressed_target.values() if r["meets_100KB"])
    c5_pass=meets_10k>=2 and meets_100k>=2
    # Also check identity baseline fails -> measurement invalid
    identity_pass=all(v["streaming_correctness_match_rate"]==1.0 and v["buffered_correctness_match_rate"]==1.0 for v in identity_cells.values())
    print(f"C1 streaming==buffered: {c1_pass}")
    print(f"C2 streaming==expected: {c2_pass}")
    print(f"C3 regression gzip {c3_gzip_pass} brotli {c3_brotli_pass} => {c3_pass}")
    print(f"C4 null_control: {c4_pass}")
    print(f"C5 compressed target 10k {meets_10k}/3 100k {meets_100k}/3 => {c5_pass} details {compressed_target}")
    print(f"identity_pass: {identity_pass}")
    # decision
    if not c5_pass or not identity_pass:
        status="MEASUREMENT_INVALID"
        outcome="NOT_APPLICABLE"
    elif c1_pass and c2_pass and c3_pass and c4_pass and c5_pass:
        status="COMPLETE"
        outcome="SUPPORTS"
    elif not c1_pass or not c2_pass:
        status="COMPLETE"
        outcome="FALSIFIES"
    elif not c3_pass:
        status="COMPLETE"
        outcome="FALSIFIES"
    else:
        status="COMPLETE"
        outcome="MIXED"
    print(f"FINAL status={status} outcome={outcome}")
    # Build metrics per spec
    total_streaming_requests=sum(v["total_requests"] for v in main_cells.values())
    total_all_requests=sum(v["total_requests"] for v in all_results.values() if "total_requests" in v)
    # Save JSON artifacts
    import pathlib, hashlib
    out_dir = pathlib.Path(__file__).parent
    # separate raw observations dump?
    # write all_results to debug
    with open(out_dir/"raw_cell_results.json","w") as f:
        json.dump(all_results,f,indent=2)
    # Return needed for main writer
    return {
        "all_results":all_results,
        "main_cells":main_cells,
        "regression_cells":regression_cells,
        "identity_cells":identity_cells,
        "c1_pass":c1_pass,"c2_pass":c2_pass,"c3_pass":c3_pass,"c3_gzip_pass":c3_gzip_pass,"c3_brotli_pass":c3_brotli_pass,"c4_pass":c4_pass,"c5_pass":c5_pass,"identity_pass":identity_pass,
        "compressed_target":compressed_target,"meets_10k":meets_10k,"meets_100k":meets_100k,
        "status":status,"outcome":outcome,
        "total_streaming_requests":total_streaming_requests,
        "errors":errors,
    }

if __name__=="__main__":
    result=run_experiment()
    # also print summary for provenance
    print(json.dumps({"status":result["status"],"outcome":result["outcome"],"c1":result["c1_pass"],"c2":result["c2_pass"],"c3":result["c3_pass"],"c4":result["c4_pass"],"c5":result["c5_pass"]},indent=2))

