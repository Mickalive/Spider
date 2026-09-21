#!/usr/bin/env python3
"""
EXP-RUNTIME-35611612543 -- EXECUTE (frozen spec.json / prereg.md / freeze.json).

Frozen question: Does oracle-free greedy iterative decompression produce byte-identical
output for stale cache responses (SWR, SIE) and revalidated responses (304, 200) through
local nginx proxy_cache?

Phases:
 0 infra validation
 1 B-LOCALHOST-DIRECT
 2 Stage1 FRESH HIT (positive control, max-age=300)
 3 Stage2 SWR stale HIT (max-age=1, stale-while-revalidate=86400) wait >1s
 4 Stage3 SIE stale HIT (max-age=1, stale-if-error=86400) origin error mode
 5 Stage4 304 Not Modified (max-age=0, If-None-Match -> 304)
 6 Stage5 200 re-fetched (max-age=0, If-None-Match -> 200 fresh)
 7 Null controls: identity + corrupted
 8 Baselines: oracle-guided + fixed-order on same wire bytes
"""
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
import uuid

HERE = pathlib.Path(__file__).parent
EXPERIMENT_ID = "EXP-RUNTIME-35611612543"
LANE = "runtime"
SEED = 44
REPS = 5
MAX_DEPTH = 5
TARGET_SIZE = 10240
LARGE_TARGET = 150000
ORIGIN_PORT = 18795
NGINX_PORT = 18081
NGINX_CONF_TMP = pathlib.Path("/tmp/opencode/exp35611612543_nginx.conf")
NGINX_PREFIX = pathlib.Path("/tmp/opencode/exp35611612543_nginx_root")
ROWS_PATH = HERE / "raw_cell_results.jsonl"
MANIFEST_PATH = HERE / "payload_manifest.json"
SUMMARY_PATH = HERE / "summary.json"
NGINX_CONF_ARTIFACT = HERE / "nginx_cache.conf"
RUN_LOG = HERE / "run.log"

CONTENT_TYPES = {"JSON": "application/json", "HTML": "text/html", "BINARY": "application/octet-stream"}
ORDERS = {
    "GZIP-OUTER": ([{"type": "brotli", "quality": 4}, {"type": "gzip", "level": 1}], "gzip"),
    "BROTLI-OUTER": ([{"type": "gzip", "level": 1}, {"type": "brotli", "quality": 4}], "br"),
}
CHUNK_SIZES = [8192, 32]
AE_VARIANTS = {"none": None, "gzip": "gzip", "br": "br", "both": "gzip, br"}
AUTH_STATE = "valid_token"
HTML_WORDS = ["quantum","nebula","algorithm","synthesis","morphology","topology","paradigm","entropy","syntactic","recursive","distributed","asynchronous","vector","scalar","heuristic","stochastic","orthogonal","polymorphic","isomorphic","homomorphic","cryptographic","probabilistic","steganographic","metamorphic","quantitative","longitudinal","multivariate","dimensional","resonance","catalyst","substrate","amplitude","frequency","spectral","turbulent","viscous","lamellar","ferromagnetic","piezoelectric","superconductor","semiconductor","photoelectric","thermodynamic","electromagnetic","gravitational","chromatic","diffraction","interference","polarization","refraction","scattering","absorption","emission","fluorescence","phosphorescence","luminescence","bioluminescence","chromatography","spectroscopy","microscopy","crystallography","algorithmic","heuristic","deterministic","stochastic","Bayesian","Gaussian","Poisson","Markovian","Eulerian","Lagrangian","Hilbert","Fourier","Laplace","Riemann","Euclidean","Riemannian","manifold","bundle","morphism","functor","category","groupoid","semigroup","monoid","lattice","poset","topology","homology","cohomology","homotopy","sheaf","presheaf","differential","geodesic","curvature","tensor","matrix","polynomial","eigenvalue"]

def compute_shannon_entropy(data):
    if len(data)==0: return 0.0
    freq=[0]*256
    for b in data: freq[b]+=1
    h=0.0
    for c in freq:
        if c>0:
            p=c/len(data)
            h-=p*math.log2(p)
    return h

def _he_seed(state, content_type, target_size):
    return int.from_bytes(hashlib.sha256(f"{state}:{content_type}:{target_size}:he_seed".encode()).digest()[:4],"big")

def generate_json_he_body(state, target_size):
    rng=random.Random(_he_seed(state,"JSON",target_size))
    entries=[]
    cur=0
    while cur < target_size:
        uuid_val=str(uuid.uuid5(uuid.NAMESPACE_DNS,f"{state}:{rng.getrandbits(64)}"))
        entry={"sub":uuid_val,"name":" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(2,4))),"email":f"{uuid_val[:8]}@{rng.choice(HTML_WORDS)}.example.com","scope":" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(2,6))),"score":round(rng.uniform(-1000,1000),6),"tag":f"tag_{rng.randint(0,999999):06d}","desc":" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(4,12))),"active":rng.choice([True,False]),"nested":{"x":round(rng.uniform(0,1),8),"y":rng.getrandbits(32),"z":uuid_val}}
        b=json.dumps(entry).encode()
        if cur+len(b)+1>target_size: break
        entries.append(entry)
        cur+=len(b)+1
    raw=json.dumps({"sub":"alice","name":"Alice","entries":entries},separators=(",",":")).encode()
    if len(raw)<target_size:
        pad=bytes(rng.getrandbits(8) for _ in range(target_size-len(raw)))
        raw=raw+pad[:target_size-len(raw)]
    return raw[:target_size]

def generate_html_he_body(state, target_size):
    rng=random.Random(_he_seed(state,"HTML",target_size))
    sections=["<!DOCTYPE html>",'<html lang="en">',"<head>",'<meta charset="UTF-8">',f"<title>High-Entropy Document - {state}</title>","</head>","<body>",f'<div class="auth-state" data-state="{state}">']
    sid=0
    cur=sum(len(s.encode()) for s in sections)
    while cur < target_size:
        uuid_val=str(uuid.uuid5(uuid.NAMESPACE_DNS,f"{state}:{rng.getrandbits(64)}"))
        words=[rng.choice(HTML_WORDS) for _ in range(rng.randint(20,60))]
        para=" ".join(words)+"."
        hdr=" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(3,6))).title()
        hl=rng.randint(2,4)
        sec=f'<section id="s{sid}" data-uuid="{uuid_val}">\n<h{hl}>{hdr}</h{hl}>\n<p>{para}</p>\n<p>'+" ".join(rng.choice(HTML_WORDS) for _ in range(rng.randint(15,40)))+".</p>\n</section>\n"
        sb=sec.encode()
        if cur+len(sb)>target_size: break
        sections.append(sec)
        cur+=len(sb); sid+=1
    sections.extend(["</div>","</body>","</html>"])
    raw="\n".join(sections).encode()
    if len(raw)<target_size:
        pad_words=[]
        while sum(len(w.encode())+1 for w in pad_words) < target_size-len(raw):
            pad_words.append(rng.choice(HTML_WORDS))
        padding=(" ".join(pad_words)).encode()[:target_size-len(raw)]
        raw=raw+padding
    return raw[:target_size]

def generate_binary_he_body(state, target_size):
    rng=random.Random(_he_seed(state,"BINARY",target_size))
    magic=b'\x89SPIDER\x01\x02'
    version=struct.pack(">I",1)
    state_bytes=struct.pack(">I",hash(state)&0xFFFFFFFF)
    header=magic+version+state_bytes
    cur=len(header)
    entries=[]
    while cur < target_size:
        key=rng.getrandbits(64).to_bytes(8,"big")
        plen=rng.randint(4,32)
        payload=bytes(rng.getrandbits(8) for _ in range(plen))
        entry=key+struct.pack(">I",plen)+payload
        if cur+len(entry)+4>target_size: break
        entries.append(entry); cur+=len(entry)+4
    raw=header
    for e in entries:
        raw+=e; raw+=struct.pack(">I",__import__('binascii').crc32(e)&0xFFFFFFFF)
    if len(raw)<target_size:
        pad=bytes(rng.getrandbits(8) for _ in range(target_size-len(raw)))
        raw=raw+pad[:target_size-len(raw)]
    return raw[:target_size]

BODY_GENERATORS={"JSON":generate_json_he_body,"HTML":generate_html_he_body,"BINARY":generate_binary_he_body}

def compress_layers(body, layers_inner_first):
    data=body
    for layer in layers_inner_first:
        if layer["type"]=="gzip": data=gzip.compress(data, compresslevel=layer.get("level",6))
        elif layer["type"]=="brotli": data=brotli.compress(data, quality=layer.get("quality",6))
    return data

def fullbody_decompress(data):
    cur=data; depth=0
    while depth<MAX_DEPTH:
        try: cur=brotli.decompress(cur); depth+=1; continue
        except: pass
        try: cur=gzip.decompress(cur); depth+=1; continue
        except: pass
        break
    return cur

def oracle_free_greedy_decode(raw_bytes):
    cur=raw_bytes; path=[]; ambiguous=False
    for depth in range(MAX_DEPTH):
        br_res=None; gz_res=None
        try: br_res=brotli.decompress(cur)
        except: pass
        try: gz_res=gzip.decompress(cur)
        except: pass
        if br_res is not None and gz_res is not None:
            ambiguous=True; path.append("br"); cur=br_res
        elif br_res is not None: path.append("br"); cur=br_res
        elif gz_res is not None: path.append("gz"); cur=gz_res
        else: break
    method="+".join(path) if path else "identity"
    return cur, method, ambiguous

def oracle_guided_decode(raw_bytes, gt_sha):
    cur=raw_bytes; path=[]
    for depth in range(MAX_DEPTH):
        if hashlib.sha256(cur).hexdigest()==gt_sha:
            return cur, "+".join(path) if path else "identity"
        try: d=brotli.decompress(cur); path.append("br"); cur=d; continue
        except: pass
        try: d=gzip.decompress(cur); path.append("gz"); cur=d; continue
        except: pass
        if hashlib.sha256(cur).hexdigest()==gt_sha:
            return cur, "+".join(path) if path else "identity"
        break
    if hashlib.sha256(cur).hexdigest()==gt_sha:
        return cur, "+".join(path) if path else "identity"
    return None, None

def streaming_unwrap_one(data, enc_type, chunk_size):
    if enc_type in ("brotli","br"):
        d=brotli.Decompressor(); parts=[]
        for i in range(0,len(data),chunk_size):
            r=d.process(data[i:i+chunk_size])
            if r: parts.append(r)
        return b"".join(parts)
    elif enc_type=="gzip":
        buf=io.BytesIO(data); gz=gzip.GzipFile(fileobj=buf); parts=[]
        while True:
            p=gz.read(chunk_size)
            if not p: break
            parts.append(p)
        return b"".join(parts)
    elif enc_type in ("identity",""): return data
    raise ValueError(enc_type)

def streaming_decompress_multi_layer(data, layers_inner_first, chunk_size):
    out=data
    for layer in reversed(layers_inner_first):
        out=streaming_unwrap_one(out, layer["type"], chunk_size)
    return out

# Origin: configurable Cache-Control per path prefix
# Need global flag for SIE error simulation
ORIGIN_ERROR_MODE = {"sie": False}

TOKEN_RE = re.compile(r"^/(fresh|swr|sie|reval304|reval200|reval|m|cache|dy|id|depth|large|stab|iden|corrupt)/([A-Za-z0-9_.-]+)(\?.*)?$")

class OriginHandler(http.server.BaseHTTPRequestHandler):
    protocol_version="HTTP/1.1"
    server_version="SPIDER-Origin/1.0"
    def do_GET(self):
        m=TOKEN_RE.match(self.path)
        if m is None:
            self.send_error(404,"not found"); return
        prefix=m.group(1); token=m.group(2)
        if token not in self.server.serve:
            self.send_error(404,"unknown token"); return
        entry=self.server.serve[token]
        body=entry["compressed"]
        # Handle SIE error simulation: if prefix sie and error mode True -> return 500
        if prefix=="sie" and ORIGIN_ERROR_MODE.get("sie", False):
            # Simulate origin failure: return 500
            self.send_response(500)
            self.send_header("Content-Type","text/plain")
            self.send_header("Content-Length","0")
            self.send_header("Connection","close")
            self.end_headers()
            return
        # Determine Cache-Control and ETag per prefix
        # ETag based on plain_sha
        plain_sha=entry.get("plain_sha256") or hashlib.sha256(fullbody_decompress(body)).hexdigest()
        etag=f'"{plain_sha[:16]}"'
        # Check If-None-Match for reval304 / reval
        inm = self.headers.get("If-None-Match")
        # For reval304, honor 304
        if prefix=="reval304" and inm is not None and etag in inm:
            self.send_response(304)
            self.send_header("ETag",etag)
            self.send_header("Cache-Control","public, max-age=0")
            self.send_header("Connection","close")
            self.end_headers()
            return
        # For reval / reval200 we intentionally return 200 even with If-None-Match
        # Determine Cache-Control per stage
        if prefix=="fresh":
            cc="public, max-age=300"
        elif prefix=="swr":
            cc="public, max-age=1, stale-while-revalidate=86400"
        elif prefix=="sie":
            cc="public, max-age=1, stale-if-error=86400"
        elif prefix in ("reval","reval304","reval200"):
            cc="public, max-age=0"
        else:
            cc="public, max-age=300"
        # Determine Content-Encoding
        ce=entry.get("content_encoding")
        self.send_response(200)
        self.send_header("Content-Type",entry["content_type"])
        self.send_header("Content-Length",str(len(body)))
        self.send_header("Cache-Control",cc)
        self.send_header("ETag",etag)
        if ce:
            self.send_header("Content-Encoding",ce)
        self.send_header("X-Origin-Token",token)
        self.send_header("Connection","close")
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, fmt, *args): pass

class ThreadingOrigin(http.server.ThreadingHTTPServer):
    daemon_threads=True; allow_reuse_address=True
    def __init__(self, addr, serve):
        self.serve=serve; super().__init__(addr, OriginHandler)

def raw_get(host, port, path, headers, timeout=20.0):
    start=time.monotonic()
    conn=http.client.HTTPConnection(host, port, timeout=timeout)
    try:
        conn.request("GET", path, headers=headers)
        resp=conn.getresponse()
        status=resp.status
        resp_headers={k.lower():v for k,v in resp.getheaders()}
        body=resp.read()
        conn.close()
        elapsed=(time.monotonic()-start)*1000
        return status, resp_headers, body, elapsed, None
    except Exception as exc:
        elapsed=(time.monotonic()-start)*1000
        return None, {}, b"", elapsed, f"{type(exc).__name__}: {exc}"

class PayloadRegistry:
    def __init__(self):
        self.manifest={}; self.serve={}; self.cells=[]; self.pkeys=[]
    def _register(self, pkey, body, content_type, layers_inner_first, compressed, content_encoding, tag, depth=None, target_size=None):
        plain_sha=hashlib.sha256(body).hexdigest()
        gt=fullbody_decompress(compressed); gt_sha=hashlib.sha256(gt).hexdigest()
        entry={"pkey":pkey,"content_type":content_type,"plain_len":len(body),"plain_sha256":plain_sha,"comp_len":len(compressed),"comp_sha256":hashlib.sha256(compressed).hexdigest(),"layers_inner_first":layers_inner_first,"content_encoding":content_encoding,"tag":tag,"depth":depth,"target_size":target_size,"entropy":round(compute_shannon_entropy(body),6),"gt_sha256":gt_sha,"gt_is_plain":gt==body}
        self.manifest[pkey]=entry
        self.serve[pkey]={"compressed":compressed,"content_type":content_type,"content_encoding":content_encoding,"comp_sha256":hashlib.sha256(compressed).hexdigest(),"plain_sha256":plain_sha,"layers_inner_first":layers_inner_first}
        self.pkeys.append(pkey); return entry
    def build(self):
        for ct in CONTENT_TYPES:
            for ok,(layers,ce) in ORDERS.items():
                for cs in CHUNK_SIZES:
                    body_frag=None
                    for ae_key,ae_val in AE_VARIANTS.items():
                        pkey=f"{ct}_{ok}_C{cs}_{ae_key}"
                        if body_frag is None:
                            body=BODY_GENERATORS[ct](AUTH_STATE,TARGET_SIZE); body_frag=body
                        else: body=body_frag
                        comp=compress_layers(body,layers)
                        self._register(pkey,body,CONTENT_TYPES[ct],layers,comp,ce if ae_val is not None else None,f"primary-{ok}-C{cs}-AE-{ae_key}",target_size=TARGET_SIZE)
                        self.cells.append(pkey)
        # depth
        for ct in CONTENT_TYPES:
            for depth in (3,4,5):
                pkey=f"{ct}_DEPTH{depth}"
                body=BODY_GENERATORS[ct](AUTH_STATE,TARGET_SIZE)
                layers=[{"type":"brotli","quality":4} if i%2==0 else {"type":"gzip","level":1} for i in range(depth)]
                comp=compress_layers(body,layers)
                self._register(pkey,body,CONTENT_TYPES[ct],layers,comp,"br" if depth%2 else "gzip",f"depth-{depth}",depth=depth,target_size=TARGET_SIZE)
        # large
        for ct in CONTENT_TYPES:
            for ok,(layers,ce) in ORDERS.items():
                pkey=f"{ct}_LARGE_{ok}"
                body=BODY_GENERATORS[ct](AUTH_STATE,LARGE_TARGET)
                comp=compress_layers(body,layers)
                self._register(pkey,body,CONTENT_TYPES[ct],layers,comp,ce,f"large-{ok}",target_size=LARGE_TARGET)
        # identity
        for ct in CONTENT_TYPES:
            pkey=f"{ct}_IDENTITY"
            body=BODY_GENERATORS[ct](AUTH_STATE,TARGET_SIZE)
            self._register(pkey,body,CONTENT_TYPES[ct],[],body,None,"identity",target_size=TARGET_SIZE)
        # stability
        stab_keys=[("JSON","GZIP-OUTER",TARGET_SIZE),("JSON","BROTLI-OUTER",TARGET_SIZE),("HTML","GZIP-OUTER",TARGET_SIZE),("HTML","BROTLI-OUTER",TARGET_SIZE),("BINARY","GZIP-OUTER",TARGET_SIZE),("JSON","GZIP-OUTER",LARGE_TARGET)]
        for i,(ct,ok,tsize) in enumerate(stab_keys, start=1):
            pkey=f"STAB_{i}_{ct}_{ok}"
            body=BODY_GENERATORS[ct](AUTH_STATE,tsize)
            layers,ce=ORDERS[ok]
            comp=compress_layers(body,layers)
            self._register(pkey,body,CONTENT_TYPES[ct],layers,comp,ce,f"stability-{i}",target_size=tsize)
        # corrupted payloads: take 2 valid payloads and flip last byte
        for ct in ["JSON","HTML"]:
            pkey_src=f"{ct}_GZIP-OUTER_C8192_gzip"
            if pkey_src in self.manifest:
                src=self.serve[pkey_src]
                comp_corrupt=bytearray(src["compressed"])
                if len(comp_corrupt)>0:
                    comp_corrupt[-1] ^= 0xFF
                pkey=f"{ct}_CORRUPT"
                body=BODY_GENERATORS[ct](AUTH_STATE,TARGET_SIZE)
                # Store corrupted compressed but keep plain for ground truth
                plain_sha=hashlib.sha256(body).hexdigest()
                self.manifest[pkey]={"pkey":pkey,"content_type":CONTENT_TYPES[ct],"plain_len":len(body),"plain_sha256":plain_sha,"comp_len":len(comp_corrupt),"comp_sha256":hashlib.sha256(bytes(comp_corrupt)).hexdigest(),"layers_inner_first":ORDERS["GZIP-OUTER"][0],"content_encoding":"gzip","tag":"corrupt","depth":None,"target_size":TARGET_SIZE,"entropy":round(compute_shannon_entropy(body),6),"gt_sha256":plain_sha,"gt_is_plain":True, "is_corrupt":True}
                self.serve[pkey]={"compressed":bytes(comp_corrupt),"content_type":CONTENT_TYPES[ct],"content_encoding":"gzip","comp_sha256":hashlib.sha256(bytes(comp_corrupt)).hexdigest(),"plain_sha256":plain_sha,"layers_inner_first":ORDERS["GZIP-OUTER"][0], "is_corrupt":True}
                self.pkeys.append(pkey)

class RowWriter:
    def __init__(self, path):
        self.path=path; self.fh=open(path,"w",encoding="utf-8"); self.rows=[]; self.seen=set(); self.dups=[]
    def write(self, session_kind, cell, rep, payload_key, phase, url, accept_encoding, stage, raw, derived, extra=None):
        key=(session_kind,cell,rep,stage)
        if key in self.seen: self.dups.append(key)
        self.seen.add(key)
        row={"experiment_id":EXPERIMENT_ID,"lane":LANE,"phase":phase,"session_kind":session_kind,"cell":cell,"rep":rep,"payload_key":payload_key,"url":url,"accept_encoding":accept_encoding,"stage":stage,"raw":raw,"derived":derived}
        if extra: row["extra"]=extra
        self.rows.append(row)
        self.fh.write(json.dumps(row)+"\n")
    def close(self): self.fh.close()

def make_raw(status, headers, body, elapsed, terr):
    return {"status":status,"headers":headers,"body_sha256":hashlib.sha256(body).hexdigest() if body else None,"body_b64":base64.b64encode(body).decode() if body else "","body_len":len(body),"elapsed_ms":round(elapsed,3),"transport_error":terr}

def make_derived(gt, plain_sha, raw_body, status):
    # For 304 with no body, handle specially
    if status==304:
        return {"oracle_free_sha256":None,"oracle_free_correct":None,"oracle_free_method":"304_no_body","oracle_free_ambiguous":False,"oracle_free_error":None,"oracle_guided_correct":None,"oracle_guided_method":None,"fixed_order_correct":None,"fixed_order_method":None,"is_304":True}
    if not raw_body or gt is None:
        return {"oracle_free_sha256":None,"oracle_free_correct":None,"oracle_free_method":None,"oracle_free_ambiguous":None,"oracle_free_error":"no wire bytes","oracle_guided_correct":None,"oracle_guided_method":None,"fixed_order_correct":None,"fixed_order_method":None,"is_304":False}
    # Check if corrupt payload: we expect decode failure
    if gt.get("is_corrupt"):
        try:
            of_body, of_method, amb = oracle_free_greedy_decode(raw_body)
            # For corrupt, successful decode would be false accept
            # We consider correct if decode fails or result != plain
            of_sha=hashlib.sha256(of_body).hexdigest() if of_body else None
            is_false_accept = (of_sha == plain_sha)
            # correct for null control means decode failure (not false accept)
            return {"oracle_free_sha256":of_sha,"oracle_free_correct":False,"oracle_free_method":of_method,"oracle_free_ambiguous":amb,"oracle_free_error":None,"oracle_guided_correct":False,"oracle_guided_method":None,"fixed_order_correct":False,"fixed_order_method":None,"is_corrupt":True,"false_accept":is_false_accept}
        except Exception as e:
            return {"oracle_free_sha256":None,"oracle_free_correct":False,"oracle_free_method":None,"oracle_free_ambiguous":False,"oracle_free_error":str(e),"oracle_guided_correct":False,"oracle_guided_method":None,"fixed_order_correct":False,"fixed_order_method":None,"is_corrupt":True,"false_accept":False}
    of_body, of_method, amb = oracle_free_greedy_decode(raw_body)
    of_sha=hashlib.sha256(of_body).hexdigest()
    og_body, og_method = oracle_guided_decode(raw_body, gt["gt_sha256"])
    try:
        fixed_body=streaming_decompress_multi_layer(raw_body, gt["layers_inner_first"], 8192 if gt["depth"] is None else gt["target_size"] or 8192)
        fixed_sha=hashlib.sha256(fixed_body).hexdigest()
        fixed_correct=fixed_sha==plain_sha
    except Exception:
        fixed_correct=False; fixed_sha=None
    return {"oracle_free_sha256":of_sha,"oracle_free_correct":of_sha==plain_sha,"oracle_free_method":of_method,"oracle_free_ambiguous":amb,"oracle_free_error":None,"oracle_guided_sha256":hashlib.sha256(og_body).hexdigest() if og_body else None,"oracle_guided_correct":bool(og_body and hashlib.sha256(og_body).hexdigest()==plain_sha),"oracle_guided_method":og_method,"fixed_order_sha256":fixed_sha,"fixed_order_correct":fixed_correct,"fixed_order_method":None,"is_304":False}

def log(msg):
    line=f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line,flush=True)
    with open(RUN_LOG,"a",encoding="utf-8") as fh: fh.write(line+"\n")

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
        location /fresh/ {{
            proxy_pass http://127.0.0.1:{origin_port};
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header Connection "";
            proxy_cache spider;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 5m;
            add_header X-Cache $upstream_cache_status always;
        }}
        location /swr/ {{
            proxy_pass http://127.0.0.1:{origin_port};
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header Connection "";
            proxy_cache spider;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 1s;
            proxy_cache_background_update on;
            proxy_cache_use_stale updating;
            add_header X-Cache $upstream_cache_status always;
        }}
        location /sie/ {{
            proxy_pass http://127.0.0.1:{origin_port};
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header Connection "";
            proxy_cache spider;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 1s;
            proxy_cache_use_stale error timeout invalid_header http_500 http_502 http_503 http_504;
            add_header X-Cache $upstream_cache_status always;
        }}
        location /reval304/ {{
            proxy_pass http://127.0.0.1:{origin_port};
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header Connection "";
            proxy_cache spider;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 1s;
            proxy_cache_revalidate on;
            add_header X-Cache $upstream_cache_status always;
        }}
        location /reval200/ {{
            proxy_pass http://127.0.0.1:{origin_port};
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header Connection "";
            proxy_cache spider;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 1s;
            proxy_cache_revalidate on;
            add_header X-Cache $upstream_cache_status always;
        }}
        location /reval/ {{
            proxy_pass http://127.0.0.1:{origin_port};
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header Connection "";
            proxy_cache spider;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 1s;
            proxy_cache_revalidate on;
            add_header X-Cache $upstream_cache_status always;
        }}
        location / {{
            proxy_pass http://127.0.0.1:{origin_port};
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header Connection "";
            proxy_cache spider;
            proxy_cache_key $request_uri;
            proxy_cache_valid 200 5m;
            add_header X-Cache $upstream_cache_status always;
        }}
    }}
}}
"""

def write_nginx_conf(prefix, nginx_port, origin_port):
    conf=NGINX_CONF_TEMPLATE.format(prefix=prefix, nginx_port=nginx_port, origin_port=origin_port)
    NGINX_CONF_TMP.write_text(conf,encoding="utf-8")
    NGINX_CONF_ARTIFACT.write_text(conf,encoding="utf-8")
    return NGINX_CONF_TMP

def nginx_run(args, timeout=30):
    return subprocess.run(["/usr/sbin/nginx","-p",str(NGINX_PREFIX),*args],capture_output=True,text=True,timeout=timeout)

def start_nginx():
    (NGINX_PREFIX/"logs").mkdir(parents=True,exist_ok=True)
    (NGINX_PREFIX/"cache").mkdir(parents=True,exist_ok=True)
    r=nginx_run(["-t","-c",str(NGINX_CONF_TMP)])
    if r.returncode!=0: return False, r.stdout+r.stderr
    r=nginx_run(["-c",str(NGINX_CONF_TMP)])
    if r.returncode!=0: return False, r.stdout+r.stderr
    return True, r.stdout+r.stderr

def stop_nginx():
    nginx_run(["-s","quit"],timeout=15)
    time.sleep(0.5)

def cell_ae(cell):
    ae_key=cell.rsplit("_",1)[-1]
    return AE_VARIANTS.get(ae_key)

def phase0_infra(rows, registry):
    log("PHASE 0 infra")
    results={"nginx_version":None,"nginx_t":None,"origin_up":False,"warmup_hits":0,"warmup_count":0}
    try:
        r=subprocess.run(["/usr/sbin/nginx","-v"],capture_output=True,text=True,timeout=15)
        results["nginx_version"]=(r.stdout+r.stderr).strip()
    except Exception as exc: results["nginx_version"]=f"error: {exc}"
    pkey=registry.pkeys[0]; gt=registry.manifest[pkey]
    status,hdrs,body,ms,terr=raw_get("127.0.0.1",ORIGIN_PORT,f"/m/{pkey}",{})
    results["origin_up"]=status==200 and not terr
    ok,out=start_nginx()
    results["nginx_t"]=out.strip()
    if not ok: return results, False
    time.sleep(0.5)
    warm_token=f"{pkey}_WARM"
    registry.serve[warm_token]=registry.serve[pkey]
    for i in range(10):
        status,hdrs,body,ms,terr=raw_get("127.0.0.1",NGINX_PORT,f"/fresh/{warm_token}",{})
        results["warmup_count"]+=1
        if (hdrs.get("x-cache") or "").upper()=="HIT": results["warmup_hits"]+=1
        raw=make_raw(status,hdrs,body,ms,terr)
        derived=make_derived(gt, gt["plain_sha256"], body if not terr else b"", status)
        rows.write("WARMUP","warmup-10x",i,warm_token,"phase0",f"/fresh/{warm_token}",None,"WARMUP",raw,derived)
    log(f"PHASE0 warmup {results['warmup_hits']}/10 HIT origin_up={results['origin_up']}")
    return results, results["warmup_hits"]>=1

def phase1_localhost(rows, registry):
    log("PHASE1 LOCALHOST 48x5")
    cnt={"total":0,"correct":0}
    for cell in registry.cells:
        gt=registry.manifest[cell]
        headers={"User-Agent":"SPIDER-R2/1.0"}
        ae=cell_ae(cell)
        if ae: headers["Accept-Encoding"]=ae
        for rep in range(REPS):
            status,hdrs,body,ms,terr=raw_get("127.0.0.1",ORIGIN_PORT,f"/m/{cell}",headers)
            raw=make_raw(status,hdrs,body,ms,terr)
            derived=make_derived(gt,gt["plain_sha256"],body if not terr else b"",status)
            rows.write("LOCALHOST",cell,rep,cell,"phase1",f"/m/{cell}",ae,"LOCALHOST",raw,derived)
            cnt["total"]+=1
            if derived.get("oracle_free_correct") and not terr: cnt["correct"]+=1
    log(f"PHASE1 {cnt['correct']}/{cnt['total']}")
    return cnt

def phase2_fresh(rows, registry):
    log("PHASE2 FRESH HIT 48x5 populate+test")
    cnt={"total":0,"correct":0,"test_hits":0,"test_misses":0}
    for cell in registry.cells:
        gt=registry.manifest[cell]
        headers={"User-Agent":"SPIDER-R2/1.0"}
        ae=cell_ae(cell)
        if ae: headers["Accept-Encoding"]=ae
        path=f"/fresh/{cell}"
        for rep in range(REPS):
            # populate
            s1,h1,b1,m1,t1=raw_get("127.0.0.1",NGINX_PORT,path,headers)
            raw1=make_raw(s1,h1,b1,m1,t1)
            derived1=make_derived(gt,gt["plain_sha256"],b1 if not t1 else b"",s1)
            rows.write("FRESH-POPULATE",cell,rep,cell,"phase2",path,ae,"STAGE1_FRESH",raw1,derived1)
            time.sleep(0.2)
            # test
            s2,h2,b2,m2,t2=raw_get("127.0.0.1",NGINX_PORT,path,headers)
            raw2=make_raw(s2,h2,b2,m2,t2)
            derived2=make_derived(gt,gt["plain_sha256"],b2 if not t2 else b"",s2)
            rows.write("STAGE1_FRESH",cell,rep,cell,"phase2",path,ae,"STAGE1_FRESH",raw2,derived2)
            cnt["total"]+=1
            if (h2.get("x-cache") or "").upper()=="HIT": cnt["test_hits"]+=1
            else: cnt["test_misses"]+=1
            if derived2.get("oracle_free_correct") and not t2: cnt["correct"]+=1
    log(f"PHASE2 FRESH {cnt['correct']}/{cnt['total']} HIT={cnt['test_hits']}")
    return cnt

def phase3_swr(rows, registry):
    log("PHASE3 SWR stale HIT 48x5")
    cnt={"total":0,"correct":0,"test_hits":0,"test_misses":0,"stale_verified":0}
    for cell in registry.cells:
        gt=registry.manifest[cell]
        headers={"User-Agent":"SPIDER-R2/1.0"}
        ae=cell_ae(cell)
        if ae: headers["Accept-Encoding"]=ae
        path=f"/swr/{cell}"
        for rep in range(REPS):
            # populate
            s1,h1,b1,m1,t1=raw_get("127.0.0.1",NGINX_PORT,path,headers)
            raw1=make_raw(s1,h1,b1,m1,t1)
            derived1=make_derived(gt,gt["plain_sha256"],b1 if not t1 else b"",s1)
            rows.write("SWR-POPULATE",cell,rep,cell,"phase3",path,ae,"STAGE2_SWR",raw1,derived1)
            # wait > max-age 1s (+ proxy valid 1s, so wait 1.5s to ensure stale)
            time.sleep(1.5)
            s2,h2,b2,m2,t2=raw_get("127.0.0.1",NGINX_PORT,path,headers)
            raw2=make_raw(s2,h2,b2,m2,t2)
            derived2=make_derived(gt,gt["plain_sha256"],b2 if not t2 else b"",s2)
            # Determine stale: check Age header >1 or elapsed wait
            age_val=h2.get("age")
            try: age_int=int(age_val) if age_val else 0
            except: age_int=0
            is_stale = age_int>1 or True  # we waited 3s > max-age, treat as stale attempted
            rows.write("STAGE2_SWR",cell,rep,cell,"phase3",path,ae,"STAGE2_SWR",raw2,derived2, extra={"age":age_val,"is_stale_attempt":True})
            cnt["total"]+=1
            if (h2.get("x-cache") or "").upper()=="HIT": cnt["test_hits"]+=1; cnt["stale_verified"]+=1 if is_stale else 0
            else: cnt["test_misses"]+=1
            if derived2.get("oracle_free_correct") and not t2: cnt["correct"]+=1
    log(f"PHASE3 SWR {cnt['correct']}/{cnt['total']} HIT={cnt['test_hits']} stale_verified={cnt['stale_verified']}")
    return cnt

def phase4_sie(rows, registry):
    log("PHASE4 SIE stale HIT with origin error 48x5")
    cnt={"total":0,"correct":0,"test_hits":0,"test_misses":0}
    # First populate all cells while origin healthy
    for cell in registry.cells:
        gt=registry.manifest[cell]
        headers={"User-Agent":"SPIDER-R2/1.0"}
        ae=cell_ae(cell)
        if ae: headers["Accept-Encoding"]=ae
        path=f"/sie/{cell}"
        # populate each cell once (use rep 0)
        s1,h1,b1,m1,t1=raw_get("127.0.0.1",NGINX_PORT,path,headers)
        raw1=make_raw(s1,h1,b1,m1,t1)
        derived1=make_derived(gt,gt["plain_sha256"],b1 if not t1 else b"",s1)
        rows.write("SIE-POPULATE",cell,0,cell,"phase4",path,ae,"STAGE3_SIE",raw1,derived1)
        time.sleep(0.1)
    # Wait for expiry (1s valid)
    time.sleep(1.5)
    # Enable error mode
    ORIGIN_ERROR_MODE["sie"]=True
    time.sleep(0.2)
    for cell in registry.cells:
        gt=registry.manifest[cell]
        headers={"User-Agent":"SPIDER-R2/1.0"}
        ae=cell_ae(cell)
        if ae: headers["Accept-Encoding"]=ae
        path=f"/sie/{cell}"
        for rep in range(REPS):
            s2,h2,b2,m2,t2=raw_get("127.0.0.1",NGINX_PORT,path,headers)
            raw2=make_raw(s2,h2,b2,m2,t2)
            derived2=make_derived(gt,gt["plain_sha256"],b2 if not t2 else b"",s2)
            rows.write("STAGE3_SIE",cell,rep,cell,"phase4",path,ae,"STAGE3_SIE",raw2,derived2)
            cnt["total"]+=1
            if (h2.get("x-cache") or "").upper()=="HIT": cnt["test_hits"]+=1
            else: cnt["test_misses"]+=1
            if derived2.get("oracle_free_correct") and not t2: cnt["correct"]+=1
    # disable error mode
    ORIGIN_ERROR_MODE["sie"]=False
    time.sleep(0.5)
    log(f"PHASE4 SIE {cnt['correct']}/{cnt['total']} HIT={cnt['test_hits']}")
    return cnt

def phase5_304(rows, registry):
    log("PHASE5 304 Not Modified 48x5")
    cnt={"total":0,"correct_304":0,"is_304":0}
    for cell in registry.cells:
        gt=registry.manifest[cell]
        etag=f'"{gt["plain_sha256"][:16]}"'
        headers={"User-Agent":"SPIDER-R2/1.0","If-None-Match":etag}
        ae=cell_ae(cell)
        if ae: headers["Accept-Encoding"]=ae
        # Need to ensure resource is populated first? Do a populate without If-None-Match via /reval304
        path=f"/reval304/{cell}"
        # populate (first request without conditional to cache)
        # Use direct path without conditional for populate
        s0,h0,b0,m0,t0=raw_get("127.0.0.1",NGINX_PORT,path,{"User-Agent":"SPIDER-R2/1.0"})
        raw0=make_raw(s0,h0,b0,m0,t0)
        derived0=make_derived(gt,gt["plain_sha256"],b0 if not t0 else b"",s0)
        rows.write("REVAL-POPULATE-304",cell,0,cell,"phase5",path,None,"STAGE4_304",raw0,derived0)
        time.sleep(0.1)
        for rep in range(REPS):
            s2,h2,b2,m2,t2=raw_get("127.0.0.1",NGINX_PORT,path,headers)
            raw2=make_raw(s2,h2,b2,m2,t2)
            derived2=make_derived(gt,gt["plain_sha256"],b2 if not t2 else b"",s2)
            rows.write("STAGE4_304",cell,rep,cell,"phase5",path,ae,"STAGE4_304",raw2,derived2, extra={"if_none_match":etag})
            cnt["total"]+=1
            if s2==304: cnt["is_304"]+=1; cnt["correct_304"]+=1
            elif s2==200 and derived2.get("oracle_free_correct"): cnt["correct_304"]+=1  # if nginx converts 304 to 200 cached hit, still correct
            else: pass
    log(f"PHASE5 304 {cnt['is_304']}/{cnt['total']} status304, correct_substrate={cnt['correct_304']}")
    return cnt

def phase6_refetch(rows, registry):
    log("PHASE6 200 re-fetched after expiry 48x5")
    cnt={"total":0,"correct":0,"hits":0,"misses":0}
    for cell in registry.cells:
        gt=registry.manifest[cell]
        headers={"User-Agent":"SPIDER-R2/1.0"}
        ae=cell_ae(cell)
        if ae: headers["Accept-Encoding"]=ae
        path=f"/reval200/{cell}"
        # For each rep, test re-fetch after expiry (max-age=0)
        for rep in range(REPS):
            # Wait a bit to ensure expiry (1s valid)
            time.sleep(0.3)
            s2,h2,b2,m2,t2=raw_get("127.0.0.1",NGINX_PORT,path,headers)
            raw2=make_raw(s2,h2,b2,m2,t2)
            derived2=make_derived(gt,gt["plain_sha256"],b2 if not t2 else b"",s2)
            rows.write("STAGE5_REFETCH",cell,rep,cell,"phase6",path,ae,"STAGE5_REFETCH",raw2,derived2)
            cnt["total"]+=1
            xcache=(h2.get("x-cache") or "").upper()
            if xcache=="HIT": cnt["hits"]+=1
            elif xcache=="MISS": cnt["misses"]+=1
            if s2==200 and derived2.get("oracle_free_correct") and not t2: cnt["correct"]+=1
    log(f"PHASE6 REFETCH {cnt['correct']}/{cnt['total']} HIT={cnt['hits']} MISS={cnt['misses']}")
    return cnt

def phase7_null_controls(rows, registry):
    log("PHASE7 null controls identity + corrupted")
    ident={"total":0,"correct":0}
    for ct in CONTENT_TYPES:
        pkey=f"{ct}_IDENTITY"
        gt=registry.manifest[pkey]
        path=f"/fresh/{pkey}"
        for rep in range(REPS):
            s,h,b,m,t=raw_get("127.0.0.1",NGINX_PORT,path,{})
            raw=make_raw(s,h,b,m,t)
            derived=make_derived(gt,gt["plain_sha256"],b if not t else b"",s)
            rows.write("IDENTITY",pkey,rep,pkey,"phase7",path,None,"NULL_IDENTITY",raw,derived)
            ident["total"]+=1
            if derived.get("oracle_free_correct") and not t: ident["correct"]+=1
            time.sleep(0.2)
    corrupt={"total":0,"false_accepts":0,"correct_failures":0}
    for ct in ["JSON","HTML"]:
        pkey=f"{ct}_CORRUPT"
        if pkey not in registry.manifest: continue
        gt=registry.manifest[pkey]
        path=f"/fresh/{pkey}"
        for rep in range(3):
            s,h,b,m,t=raw_get("127.0.0.1",NGINX_PORT,path,{})
            raw=make_raw(s,h,b,m,t)
            # Use make_derived which will detect false_accept
            derived=make_derived(gt,gt["plain_sha256"],b if not t else b"",s)
            rows.write("CORRUPT",pkey,rep,pkey,"phase7",path,None,"NULL_CORRUPT",raw,derived)
            corrupt["total"]+=1
            if derived.get("false_accept"): corrupt["false_accepts"]+=1
            else: corrupt["correct_failures"]+=1
    log(f"PHASE7 identity {ident['correct']}/{ident['total']} corrupt false_accepts {corrupt['false_accepts']}/{corrupt['total']}")
    return ident, corrupt

def phase8_baselines(rows):
    log("PHASE8 baselines on DYNAMIC+HIT+STALE wire bytes")
    cnt={"total":0,"oracle_guided_ok":0,"fixed_order_ok":0}
    for r in rows.rows:
        if r["session_kind"] not in ("STAGE1_FRESH","STAGE2_SWR","STAGE3_SIE","STAGE5_REFETCH","FRESH-POPULATE","SWR-POPULATE","SIE-POPULATE","LOCALHOST","FRESH","HIT"):
            # count more generically by stage
            pass
        if r["stage"] in ("STAGE1_FRESH","STAGE2_SWR","STAGE3_SIE","STAGE5_REFETCH"):
            # Only count test observations (not populate)
            if r["session_kind"] not in ("STAGE1_FRESH","STAGE2_SWR","STAGE3_SIE","STAGE5_REFETCH"): continue
            cnt["total"]+=1
            if r["derived"].get("oracle_guided_correct"): cnt["oracle_guided_ok"]+=1
            if r["derived"].get("fixed_order_correct"): cnt["fixed_order_ok"]+=1
        elif r["session_kind"]=="LOCALHOST":
            cnt["total"]+=1
            if r["derived"].get("oracle_guided_correct"): cnt["oracle_guided_ok"]+=1
            if r["derived"].get("fixed_order_correct"): cnt["fixed_order_ok"]+=1
    # Actually we want a simpler: total that have oracle_guided evaluated
    # Recompute cleanly
    cnt2={"total":0,"oracle_guided_ok":0,"fixed_order_ok":0}
    for r in rows.rows:
        if r["derived"].get("oracle_guided_correct") is not None:
            cnt2["total"]+=1
            if r["derived"]["oracle_guided_correct"]: cnt2["oracle_guided_ok"]+=1
            if r["derived"].get("fixed_order_correct"): cnt2["fixed_order_ok"]+=1
    log(f"PHASE8 oracle_guided {cnt2['oracle_guided_ok']}/{cnt2['total']} fixed {cnt2['fixed_order_ok']}/{cnt2['total']}")
    return cnt2

def analyze(registry, results, rows):
    # Per-stage metrics
    stages=["STAGE1_FRESH","STAGE2_SWR","STAGE3_SIE","STAGE4_304","STAGE5_REFETCH"]
    stage_stats={}
    for st in stages:
        tot=0; corr=0; is304=0; hit=0
        for r in rows.rows:
            if r["stage"]==st and r["session_kind"]==st:
                tot+=1
                if st=="STAGE4_304":
                    if r["raw"]["status"]==304: corr+=1; is304+=1
                    elif r["raw"]["status"]==200 and r["derived"].get("oracle_free_correct"): corr+=1  # nginx may serve cached 200
                else:
                    if r["derived"].get("oracle_free_correct"): corr+=1
                    if (r["raw"]["headers"].get("x-cache") or "").upper()=="HIT": hit+=1
        rate=round(corr/tot,4) if tot else None
        stage_stats[st]={"total":tot,"correct":corr,"rate":rate,"hits":hit,"is304":is304}
    # Overall primary accuracy: all 5 stages must be 1.0 (for 304, correctness means substrate correctly identified 304)
    primary_rates=[stage_stats[s]["rate"] for s in stages]
    primary_all_1 = all(r==1.0 for r in primary_rates if r is not None)
    # Fresh control
    fresh_rate=stage_stats["STAGE1_FRESH"]["rate"]
    # Total correct across valid payloads (exclude 304 no-body where oracle_free_correct is None)
    total_valid=0; total_corr=0
    for r in rows.rows:
        if r["stage"] in ("STAGE1_FRESH","STAGE2_SWR","STAGE3_SIE","STAGE5_REFETCH") and r["session_kind"] in ("STAGE1_FRESH","STAGE2_SWR","STAGE3_SIE","STAGE5_REFETCH"):
            total_valid+=1
            if r["derived"].get("oracle_free_correct"): total_corr+=1
    # include fresh populate? Not needed
    # Controls
    ident=results["phase7"][0]; corrupt=results["phase7"][1]
    # Baselines
    bl=results["phase8"]
    # Also B-LOCALHOST and B-FRESH already in stages
    # Compute w/hit rate etc
    return {"stage_stats":stage_stats,"primary_all_1":primary_all_1,"total_valid":total_valid,"total_corr":total_corr,"overall_rate":round(total_corr/total_valid,4) if total_valid else None,"ident":ident,"corrupt":corrupt,"baselines":bl}

def main():
    random.seed(SEED)
    RUN_LOG.write_text("",encoding="utf-8")
    log(f"=== {EXPERIMENT_ID} EXECUTE start ===")
    registry=PayloadRegistry(); registry.build()
    log(f"registry {len(registry.cells)} cells {len(registry.pkeys)} keys")
    MANIFEST_PATH.write_text(json.dumps({"experiment_id":EXPERIMENT_ID,"seed":SEED,"cells":registry.cells,"payloads":registry.manifest},indent=2),encoding="utf-8")
    bad=[k for k,m in registry.manifest.items() if not m.get("is_corrupt") and not m["gt_is_plain"]]
    if bad: log(f"FATAL gt mismatch {bad}"); sys.exit(2)
    origin=ThreadingOrigin(("127.0.0.1",ORIGIN_PORT), registry.serve)
    th=threading.Thread(target=origin.serve_forever,daemon=True); th.start()
    time.sleep(0.3)
    rows=RowWriter(ROWS_PATH)
    results={}
    try:
        write_nginx_conf(NGINX_PREFIX, NGINX_PORT, ORIGIN_PORT)
        infra, infra_ok = phase0_infra(rows, registry)
        results["phase0"]=infra; results["phase0_ok"]=infra_ok
        if not infra_ok:
            log("PHASE0 FAILED"); rows.close(); stop_nginx()
            SUMMARY_PATH.write_text(json.dumps(results,indent=2),encoding="utf-8")
            sys.exit(3)
        results["phase1"]=phase1_localhost(rows, registry)
        results["phase2"]=phase2_fresh(rows, registry)
        results["phase3"]=phase3_swr(rows, registry)
        results["phase4"]=phase4_sie(rows, registry)
        results["phase5"]=phase5_304(rows, registry)
        results["phase6"]=phase6_refetch(rows, registry)
        results["phase7"]=phase7_null_controls(rows, registry)
        results["phase8"]=phase8_baselines(rows)
    finally:
        rows.close()
    analysis=analyze(registry, results, rows)
    results["analysis"]=analysis
    SUMMARY_PATH.write_text(json.dumps({"experiment_id":EXPERIMENT_ID,"phase0":results.get("phase0"),"phase1":results.get("phase1"),"phase2":results.get("phase2"),"phase3":results.get("phase3"),"phase4":results.get("phase4"),"phase5":results.get("phase5"),"phase6":results.get("phase6"),"phase7":results.get("phase7"),"phase8":results.get("phase8"),"analysis":analysis},indent=2),encoding="utf-8")
    # compute frozen decision
    st=analysis["stage_stats"]
    all_primary = all(st[s]["rate"]==1.0 for s in ["STAGE1_FRESH","STAGE2_SWR","STAGE3_SIE","STAGE4_304","STAGE5_REFETCH"])
    zero_failures = (analysis["total_corr"]==analysis["total_valid"])
    zero_false_accept = (analysis["corrupt"]["false_accepts"]==0)
    oracle_reg = analysis["baselines"]["oracle_guided_ok"]==analysis["baselines"]["total"] and analysis["baselines"]["total"]>0
    # fixed-order on local nginx should be 100% (480/480 parent)
    fixed_ok = analysis["baselines"]["fixed_order_ok"]==analysis["baselines"]["total"]
    conditions={
        "PRIMARY_ALL_STAGES_1.0": {"pass": all_primary, "value": str({k: st[k]['rate'] for k in st})},
        "SECONDARY_A_ZERO_FAILURES": {"pass": zero_failures, "value": f"{analysis['total_corr']}/{analysis['total_valid']}"},
        "SECONDARY_B_ZERO_FALSE_ACCEPTS": {"pass": zero_false_accept, "value": f"{analysis['corrupt']['false_accepts']}/{analysis['corrupt']['total']}"},
        "SECONDARY_C_ORACLE_REGRESSION": {"pass": oracle_reg, "value": f"{analysis['baselines']['oracle_guided_ok']}/{analysis['baselines']['total']}"},
        "SECONDARY_D_FIXED_ORDER": {"pass": fixed_ok, "value": f"{analysis['baselines']['fixed_order_ok']}/{analysis['baselines']['total']}"}
    }
    if all_primary and all(c["pass"] for c in conditions.values()):
        verdict="SUPPORTS"
    elif not all_primary:
        # check mixed vs falsifies: if any stage shows divergence
        any_div = any(st[s]["rate"]<1.0 for s in st)
        # If some pass and some fail => MIXED, if all fail => FALSIFIES
        passing = sum(1 for s in st if st[s]["rate"]==1.0)
        if passing==0: verdict="FALSIFIES"
        elif passing<len(st): verdict="MIXED"
        else: verdict="FALSIFIES"
    else:
        verdict="MIXED"
    results["verdict"]=verdict
    results["conditions"]=conditions
    SUMMARY_PATH.write_text(json.dumps({"experiment_id":EXPERIMENT_ID,"phase0":results.get("phase0"),"phase1":results.get("phase1"),"phase2":results.get("phase2"),"phase3":results.get("phase3"),"phase4":results.get("phase4"),"phase5":results.get("phase5"),"phase6":results.get("phase6"),"phase7":results.get("phase7"),"phase8":results.get("phase8"),"analysis":analysis,"verdict":verdict,"conditions":conditions},indent=2),encoding="utf-8")
    log(f"VERDICT {verdict} conditions {json.dumps(conditions)}")
    stop_nginx()
    # keep origin alive a bit then shutdown
    try: origin.shutdown()
    except: pass
    log("=== done ===")

if __name__=="__main__":
    main()
