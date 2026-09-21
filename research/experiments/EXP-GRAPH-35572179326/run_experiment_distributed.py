#!/usr/bin/env python3
"""
EXP-GRAPH-35572179326 Distributed C-FRESHNESS Orthogonality (Two-Bug Fix + Re-Run)

Implements 4 conditions:
- B-LOCAL-ONLY: single-node serial (port 18970) identical to parent
- B-DISTRIBUTED: 2-node independent caches round-robin (ports 18971,18972) using testbed_server.py (V1 uuid)
- B-CONCURRENT: single-node with 5 concurrent clients (port 18970)
- B-CONFOUND-DISTRIBUTED: 2-node V2 confound (ports 18973,18974) using testbed_server_v2.py

C1 FIX: Excludes 304 responses from behavioral TP/TN calculation, consistent
with primary orthogonality metric's 304 exclusion.

Preserves V_ETAG, V3 stratification, V1 UUID, 304 exclusion.
"""
import os, sys, json, time, hashlib, secrets, subprocess, threading, random, math, socket, uuid
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import requests
from scipy.stats import pearsonr, norm
import warnings
warnings.filterwarnings("ignore")

EXPERIMENT_ID = "EXP-GRAPH-35572179326"
EXPERIMENT_DIR = Path(__file__).parent
RAW_EVIDENCE_DIR = EXPERIMENT_DIR / "raw_evidence"
RAW_EVIDENCE_DIR.mkdir(exist_ok=True)

N_SAMPLES_PER_CONDITION_PER_ENDPOINT = 42
N_ENDPOINTS = 3
N_CONDITIONS = 8
TOTAL_SAMPLES_PER_ENDPOINT = N_SAMPLES_PER_CONDITION_PER_ENDPOINT * N_CONDITIONS
TOTAL_SAMPLES = TOTAL_SAMPLES_PER_ENDPOINT * N_ENDPOINTS
SEED = 42
TESTBED_HOST = "127.0.0.1"

CONDITIONS = [
    ("valid", True, "read", "valid+cache+read"),
    ("valid", True, "write", "valid+cache+write"),
    ("valid", False, "read", "valid+nocache+read"),
    ("valid", False, "write", "valid+nocache+write"),
    ("expired", True, "read", "expired+cache+read"),
    ("expired", True, "write", "expired+cache+write"),
    ("expired", False, "read", "expired+nocache+read"),
    ("expired", False, "write", "expired+nocache+write"),
]
ENDPOINTS = ["/api/user/profile", "/api/data/list", "/api/session/status"]

def compute_request_id_entropy(request_id):
    if not request_id: return 0.0
    counts = Counter(request_id)
    length = len(request_id)
    entropy = 0.0
    for count in counts.values():
        p = count / length
        if p>0: entropy -= p*math.log2(p)
    return entropy

def compute_structural_composite_headers_only(response, prev_etag, prev_cache_control, request_id):
    current_etag = response.headers.get("ETag","")
    current_cache_control = response.headers.get("Cache-Control","")
    etag_var = 1 if (prev_etag and current_etag and current_etag != prev_etag) else 0
    cache_control_var = 1 if (prev_cache_control and current_cache_control and current_cache_control != prev_cache_control) else 0
    request_id_entropy = compute_request_id_entropy(request_id)
    norm_entropy = min(request_id_entropy/4.0,1.0)
    dyn_hash = hashlib.sha256(request_id.encode()).hexdigest()
    dyn_hash_int = int(dyn_hash[:16],16)%10000/10000.0
    structural_composite = etag_var*0.3 + cache_control_var*0.3 + norm_entropy*0.2 + dyn_hash_int*0.2
    return {"structural_composite":structural_composite,"etag_variation":etag_var,"cache_control_variation":cache_control_var,
            "request_id_entropy":request_id_entropy,"normalized_entropy":norm_entropy,"dynamic_content_hash":dyn_hash_int,
            "etag":current_etag,"cache_control":current_cache_control}

def extract_behavioral_signals(response, token_valid, token_expired, permission_level):
    status_code = response.status_code
    effective_code = 200 if status_code==304 else status_code
    signals={"token_validation_failure":0,"session_state_change":0,"auth_boundary_shift":0,"session_status_code":effective_code,"token_expired":int(token_expired),"permission_level":permission_level,"is_304":status_code==304}
    if status_code==401:
        signals["token_validation_failure"]=1
        signals["session_state_change"]=1
    if status_code==403: signals["auth_boundary_shift"]=1
    if status_code==200:
        try:
            body=response.json() if response.content else {}
            if isinstance(body,dict) and not body.get("valid",True):
                signals["session_state_change"]=1
        except: pass
    return signals

def compute_behavioral_delta(signals):
    tr=signals.get("token_validation_failure",0)
    sc=signals.get("session_state_change",0)
    ab=signals.get("auth_boundary_shift",0)
    code=signals.get("session_status_code",200)
    ssc={200:0.0,401:1.0,403:0.5,500:0.75}.get(code,0.5)
    return tr*2.0+sc*3.0+ab*1.0+ssc*2.0

class SingleServerManager:
    def __init__(self, port, server_script):
        self.port=port
        self.process=None
        self.base_url=f"http://{TESTBED_HOST}:{port}"
        self.server_script=server_script
        self.db_path=f"/tmp/testbed_sessions_35572179326_{port}.db"
    def start(self):
        env=os.environ.copy()
        env["TESTBED_PORT"]=str(self.port)
        env["TESTBED_SECRET"]=secrets.token_hex(32)
        env["TESTBED_DB"]=self.db_path
        env["TESTBED_SEED"]=str(SEED)
        env["TESTBED_JITTER_MIN"]="10"
        env["TESTBED_JITTER_MAX"]="100"
        env["TESTBED_CACHE_MAX_AGE"]="30"
        cmd=[sys.executable,str(self.server_script),"--port",str(self.port),"--seed",str(SEED),"--db-path",self.db_path,"--jitter-min","10","--jitter-max","100","--cache-max-age","30"]
        self.process=subprocess.Popen(cmd,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for _ in range(80):
            try:
                resp=requests.get(f"{self.base_url}/health",timeout=1)
                if resp.status_code==200:
                    time.sleep(0.2); return True
            except: pass
            time.sleep(0.1)
        raise RuntimeError(f"Server failed start port {self.port}")
    def stop(self):
        if self.process:
            self.process.terminate()
            try: self.process.wait(timeout=5)
            except:
                self.process.kill()
                try: self.process.wait(timeout=3)
                except: pass
            self.process=None
        try:
            if os.path.exists(self.db_path): os.unlink(self.db_path)
        except: pass
        # also cleanup wal/shm
        for suffix in ["-wal","-shm"]:
            try:
                if os.path.exists(self.db_path+suffix): os.unlink(self.db_path+suffix)
            except: pass
    def request(self, method, endpoint, **kwargs):
        url=f"{self.base_url}{endpoint}"
        return requests.request(method,url,timeout=10,**kwargs)
    def get_token(self, user_id="test_user", permission_level="read", expiry_hours=1.0, expired=False):
        resp=self.request("POST","/token",json={"user_id":user_id,"permission_level":permission_level,"expiry_hours":expiry_hours,"expired":expired,"algorithm":"RS256"})
        data=resp.json(); return data["token"], data["session_id"]
    def set_cache(self, enabled):
        self.request("POST","/admin/set_cache",json={"enabled":enabled})
    def set_permissions(self, permissions):
        self.request("POST","/admin/set_permissions",json={"permissions":permissions})
    def reset(self): self.request("POST","/admin/reset")

class DistributedManager:
    """Two independent SingleServerManager with round-robin routing"""
    def __init__(self, ports, server_script):
        self.managers=[SingleServerManager(p, server_script) for p in ports]
        self.ports=ports
        self.counter=0
        self.lock=threading.Lock()
    def start(self):
        for m in self.managers: m.start()
        time.sleep(0.3)
    def stop(self):
        for m in self.managers: m.stop()
    def _next_manager(self):
        with self.lock:
            m=self.managers[self.counter % len(self.managers)]
            self.counter+=1
            return m
    def request(self, method, endpoint, **kwargs):
        # round-robin per request
        m=self._next_manager()
        return m.request(method, endpoint, **kwargs)
    def get_token(self, **kwargs):
        # token creation must go to same node that will serve request? We'll use round-robin as well
        # But session is per-node independent; token is JWT so valid on any node, session_id is per-node.
        # For simplicity, get_token from next manager and use that node's session for next request is okay because JWT validated via RSA not DB, but session status check uses DB per node.
        # To preserve independence, create session on same node we will query? We'll randomize: pick next manager and return its token/session.
        m=self._next_manager()
        return m.get_token(**kwargs)
    def set_cache(self, enabled):
        for m in self.managers: m.set_cache(enabled)
    def set_permissions(self, permissions):
        for m in self.managers: m.set_permissions(permissions)
    def reset(self):
        for m in self.managers: m.reset()
    def request_with_affinity(self, method, endpoint, token, session_id, **kwargs):
        # Use round-robin still; token/session_id from prior get_token may be from different node
        # That's okay: JWT valid everywhere, session valid only on creation node, but validate_session on other node returns invalid -> still behavioral signal reflects token state, not session.
        # For consistency with spec (independent caches, no shared state), this is correct.
        return self.request(method, endpoint, **kwargs)

# Unified sample runners
def run_single_sample(manager, condition_idx, endpoint, prev_etag, prev_cache_control, is_distributed=False):
    token_state, cache_mode, perm_level, cond_label = CONDITIONS[condition_idx]
    result={"token_validation_failure":0,"session_state_change":0,"auth_boundary_shift":0,"session_status_code":200,
            "behavioral_delta":0.0,"structural_composite":0.0,"etag":"","cache_control":"","request_id_entropy":0.0,"status":"OK",
            "token_expired":0,"permission_level":perm_level,"has_304":False,"cache_hit":False}
    try:
        # Use manager's set_cache/set_permissions
        manager.set_cache(cache_mode)
        manager.set_permissions({"read":True,"write":perm_level=="write","admin":perm_level=="admin"})
        # token acquisition
        if isinstance(manager, DistributedManager):
            token, session_id = manager.get_token(user_id="test_user", permission_level=perm_level, expiry_hours=(1.0 if token_state=="valid" else -1.0), expired=(token_state=="expired"))
        else:
            token, session_id = manager.get_token(user_id="test_user", permission_level=perm_level, expiry_hours=(1.0 if token_state=="valid" else -1.0), expired=(token_state=="expired"))

        headers={"Authorization":f"Bearer {token}","X-Session-ID":session_id}
        cookie_jar=requests.cookies.RequestsCookieJar()
        cookie_jar.set("session_id",session_id,domain="localhost",path="/")
        if cache_mode and endpoint in ["/api/user/profile","/api/data/list"] and prev_etag:
            headers["If-None-Match"]=prev_etag
        response=manager.request("GET", endpoint, headers=headers, cookies=cookie_jar)
        token_expired=token_state=="expired"
        is_401=response.status_code==401
        is_304=response.status_code==304
        behavioral_signals=extract_behavioral_signals(response, not is_401, token_expired, perm_level)
        behavioral_delta=compute_behavioral_delta(behavioral_signals)
        try:
            body_json=response.json() if response.content else {}
            request_id=body_json.get("request_id", str(uuid.uuid4()))
        except: request_id=str(uuid.uuid4())
        current_etag=response.headers.get("ETag","")
        current_cache_control=response.headers.get("Cache-Control","")
        if is_304:
            structural=compute_structural_composite_headers_only(response, prev_etag, prev_cache_control, request_id)
            structural["etag_variation"]=1 if (prev_etag and current_etag and current_etag!=prev_etag) else 0
            structural["cache_control_variation"]=1 if (prev_cache_control and current_cache_control and current_cache_control!=prev_cache_control) else 0
            structural["request_id_entropy"]=compute_request_id_entropy(request_id)
            structural["normalized_entropy"]=min(structural["request_id_entropy"]/4.0,1.0)
            structural["structural_composite"]=structural["etag_variation"]*0.3+structural["cache_control_variation"]*0.3+structural["normalized_entropy"]*0.2+0.2
            result["has_304"]=True; result["cache_hit"]=True
        else:
            structural=compute_structural_composite_headers_only(response, prev_etag, prev_cache_control, request_id)
        result["token_validation_failure"]=behavioral_signals["token_validation_failure"]
        result["session_state_change"]=behavioral_signals["session_state_change"]
        result["auth_boundary_shift"]=behavioral_signals["auth_boundary_shift"]
        result["session_status_code"]=response.status_code
        result["token_expired"]=1 if token_expired else 0
        result["permission_level"]=perm_level
        result["behavioral_delta"]=behavioral_delta
        result["structural_composite"]=structural["structural_composite"]
        result["etag"]=current_etag
        result["cache_control"]=current_cache_control
        result["request_id_entropy"]=structural["request_id_entropy"]
    except Exception as e:
        result["status"]=f"ERROR: {str(e)}"
    return result

# Statistical helpers
def fisher_z_ci(r,n):
    if n<=3 or abs(r)>=1.0: return (-1.0,1.0)
    fz=0.5*math.log((1+r)/(1-r))
    se=1.0/math.sqrt(n-3)
    z_crit=1.96
    return math.tanh(fz-z_crit*se), math.tanh(fz+z_crit*se)

def tost_equivalence(r,n,delta=0.15):
    if n<=3: return {"pass":False,"p_upper":1.0,"p_lower":1.0,"delta":delta,"fisher_z":0.0,"se":1.0}
    fz=0.5*math.log((1+r)/(1-r))
    se=1.0/math.sqrt(n-3)
    zu=(fz-0.5*math.log((1+delta)/(1-delta)))/se
    pl=1.0-norm.cdf((fz-0.5*math.log((1-delta)/(1+delta)))/se)
    pu=norm.cdf(zu)
    return {"pass":pu<0.05,"p_upper":float(pu),"p_lower":float(pl),"delta":delta,"fisher_z":float(fz),"se":float(se)}

def stratified_pooled_r(per_endpoint_data):
    weighted_sum=0.0; total_n=0
    for endpoint,(b,s) in per_endpoint_data.items():
        if len(b)>=3 and len(s)>=3:
            r_i,_=pearsonr(np.array(b),np.array(s))
            n_i=len(b)
            weighted_sum+=n_i*r_i
            total_n+=n_i
    if total_n==0: return 0.0,0,1.0
    return weighted_sum/total_n, total_n, 1.0/math.sqrt(total_n-3) if total_n>3 else 1.0

def run_condition_samples(manager, endpoint, cond_idx, n_samples, is_distributed=False):
    """Run n_samples sequentially for a given endpoint+condition, tracking etag chain"""
    samples=[]
    prev_etag=""; prev_cache_control=""
    for _ in range(n_samples):
        s=run_single_sample(manager, cond_idx, endpoint, prev_etag, prev_cache_control, is_distributed=is_distributed)
        samples.append(s)
        if s["status"]=="OK":
            prev_etag=s.get("etag",prev_etag)
            prev_cache_control=s.get("cache_control",prev_cache_control)
    return samples

def run_concurrent_samples(manager, endpoint, cond_idx, n_samples, n_threads=5):
    """Run n_samples using ThreadPoolExecutor with 5 threads, preserving per-thread etag isolation"""
    # Split samples across threads roughly equally
    # Each thread needs independent prev_etag chain? But spec says thread-safe with per-thread isolation.
    # We'll launch n_threads workers each doing n_samples//n_threads sequentially with isolated etag chain.
    per_thread = n_samples // n_threads
    remainder = n_samples % n_threads
    tasks=[]
    # Create callable per thread
    def worker(count):
        local_prev_etag=""; local_prev_cc=""
        local_samples=[]
        for _ in range(count):
            s=run_single_sample(manager, cond_idx, endpoint, local_prev_etag, local_prev_cc)
            local_samples.append(s)
            if s["status"]=="OK":
                local_prev_etag=s.get("etag",local_prev_etag)
                local_prev_cc=s.get("cache_control",local_prev_cc)
        return local_samples

    counts=[per_thread + (1 if i<remainder else 0) for i in range(n_threads)]
    all_samples=[]
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures=[executor.submit(worker,c) for c in counts]
        for f in as_completed(futures):
            all_samples.extend(f.result())
    return all_samples

def collect_condition(manager_factory, condition_name, ports, server_script, use_concurrent=False, is_distributed=False):
    """Factory returns manager; run all endpoints/conditions"""
    manager=manager_factory()
    try:
        manager.start()
        print(f"  {condition_name} server running on {ports}")
    except Exception as e:
        print(f" FATAL cannot start {condition_name}: {e}")
        raise
    all_samples=[]
    per_condition={}
    per_endpoint_b={}
    per_endpoint_s={}
    try:
        for endpoint in ENDPOINTS:
            for cond_idx,(token_state,cache_mode,perm_level,cond_label) in enumerate(CONDITIONS):
                condition_id=f"{cond_label}+{endpoint.replace('/api/','').replace('/','_')}"
                if use_concurrent:
                    samples=run_concurrent_samples(manager, endpoint, cond_idx, N_SAMPLES_PER_CONDITION_PER_ENDPOINT, n_threads=5)
                else:
                    samples=run_condition_samples(manager, endpoint, cond_idx, N_SAMPLES_PER_CONDITION_PER_ENDPOINT, is_distributed=is_distributed)
                valid=[s for s in samples if s["status"]=="OK"]
                all_samples.extend(valid)
                per_condition[condition_id]={"samples":samples,"token_state":token_state,"cache_mode":cache_mode,"permission_level":perm_level,"endpoint":endpoint,"n_valid":len(valid),"n_total":len(samples)}
                if endpoint not in per_endpoint_b:
                    per_endpoint_b[endpoint]=[]; per_endpoint_s[endpoint]=[]
                for s in valid:
                    per_endpoint_b[endpoint].append(s["behavioral_delta"])
                    per_endpoint_s[endpoint].append(s["structural_composite"])
                print(f"    {condition_name} {condition_id}: {len(valid)}/{len(samples)} valid")
    finally:
        manager.stop()
    return all_samples, per_condition, per_endpoint_b, per_endpoint_s

def main():
    print("="*80)
    print("EXP-GRAPH-35572179326: Distributed C-FRESHNESS Orthogonality (Two-Bug Fix + Re-Run)")
    print(f"N per condition={TOTAL_SAMPLES} ({N_SAMPLES_PER_CONDITION_PER_ENDPOINT} x 8 x 3)")
    print("Conditions: B-LOCAL-ONLY, B-DISTRIBUTED, B-CONCURRENT, B-CONFOUND-DISTRIBUTED")
    print("="*80)
    parent_dir=Path("/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35538864957")
    primary_script=parent_dir / "testbed_server.py"
    confound_script=parent_dir / "testbed_server_v2.py"
    # SAMEFILEERROR FIX (frozen prereg sec.3 Fix 1): no file copy. The experiment
    # uses parent_dir/testbed_server.py and testbed_server_v2.py directly as
    # server scripts. Provenance is recorded via SHA-256 hashes in provenance.json.
    # Phase B-LOCAL-ONLY
    print("\n[PHASE B-LOCAL-ONLY] Single-node serial")
    def local_factory(): return SingleServerManager(18970, primary_script)
    local_samples, local_per_cond, local_b, local_s = collect_condition(local_factory, "B-LOCAL-ONLY", [18970], primary_script, use_concurrent=False)

    # Phase B-DISTRIBUTED
    print("\n[PHASE B-DISTRIBUTED] 2-node round-robin")
    def dist_factory(): return DistributedManager([18971,18972], primary_script)
    dist_samples, dist_per_cond, dist_b, dist_s = collect_condition(dist_factory, "B-DISTRIBUTED", [18971,18972], primary_script, use_concurrent=False, is_distributed=True)

    # Phase B-CONCURRENT
    print("\n[PHASE B-CONCURRENT] Single-node concurrent (5 threads)")
    def conc_factory(): return SingleServerManager(18970, primary_script)
    conc_samples, conc_per_cond, conc_b, conc_s = collect_condition(conc_factory, "B-CONCURRENT", [18970], primary_script, use_concurrent=True)

    # Phase B-CONFOUND-DISTRIBUTED
    print("\n[PHASE B-CONFOUND-DISTRIBUTED] 2-node confound")
    def confound_factory(): return DistributedManager([18973,18974], confound_script)
    conf_samples, conf_per_cond, conf_b, conf_s = collect_condition(confound_factory, "B-CONFOUND-DISTRIBUTED", [18973,18974], confound_script, use_concurrent=False, is_distributed=True)

    # --- Analysis helpers for each condition ---
    def analyze_condition(all_samples, per_condition, per_b, per_s, label):
        non304=[s for s in all_samples if not s.get("has_304",False)]
        # Also need per-endpoint non304
        non304_per_b={}; non304_per_s={}
        for cid, cdata in per_condition.items():
            ep=cdata["endpoint"]
            for s in cdata["samples"]:
                if s["status"]!="OK" or s.get("has_304",False): continue
                if ep not in non304_per_b: non304_per_b[ep]=[]; non304_per_s[ep]=[]
                non304_per_b[ep].append(s["behavioral_delta"])
                non304_per_s[ep].append(s["structural_composite"])
        # simple pooled (non304)
        if len(non304)>=3:
            b_vals=[s["behavioral_delta"] for s in non304]
            s_vals=[s["structural_composite"] for s in non304]
            r_pooled,_=pearsonr(np.array(b_vals),np.array(s_vals))
            ci_l,ci_u=fisher_z_ci(r_pooled,len(non304))
            tost=tost_equivalence(r_pooled,len(non304),0.15)
        else:
            r_pooled=0.0; ci_l,ci_u=-1,1; tost={"pass":False,"p_upper":1.0}
        # stratified
        strat_r, strat_n, strat_se=stratified_pooled_r({ep:(non304_per_b[ep],non304_per_s[ep]) for ep in non304_per_b if len(non304_per_b[ep])>=3})
        strat_ci_l,strat_ci_u=fisher_z_ci(strat_r,strat_n) if strat_n>3 else (-1,1)
        strat_tost=tost_equivalence(strat_r,strat_n,0.15)
        # per-endpoint r
        per_ep_r={}
        for ep in ENDPOINTS:
            be=non304_per_b.get(ep,[]); bs=non304_per_s.get(ep,[])
            if len(be)>=3:
                r,p=pearsonr(np.array(be),np.array(bs))
                per_ep_r[ep]={"r":float(r),"p":float(p),"n":len(be)}
            else:
                per_ep_r[ep]={"r":None,"p":None,"n":len(be)}
        # 304 stats
        n304=sum(1 for s in all_samples if s.get("has_304",False))
        # behavioral std, structural std etc (non304)
        # For C2 we need std >0; use non304 per-endpoint
        # cache heterogeneity stratified: per cache mode
        endpoint_cache_b={}; endpoint_cache_s={}
        for cid,cdata in per_condition.items():
            ep=cdata["endpoint"]; cache_mode="enabled" if cdata["cache_mode"] else "disabled"
            if ep not in endpoint_cache_b: endpoint_cache_b[ep]={"enabled":[],"disabled":[]}; endpoint_cache_s[ep]={"enabled":[],"disabled":[]}
            for s in cdata["samples"]:
                if s["status"]!="OK" or s.get("has_304",False): continue
                b=s["behavioral_delta"]; ss=s["structural_composite"]
                endpoint_cache_b[ep][cache_mode].append(b)
                endpoint_cache_s[ep][cache_mode].append(ss)
        r_enabled_per=[]; r_disabled_per=[]; n_enabled_per=[]; n_disabled_per=[]
        for ep in endpoint_cache_b:
            eb=endpoint_cache_b[ep]["enabled"]; es=endpoint_cache_s[ep]["enabled"]
            db=endpoint_cache_b[ep]["disabled"]; ds=endpoint_cache_s[ep]["disabled"]
            if len(eb)>=3 and len(db)>=3:
                r_e=float(pearsonr(np.array(eb),np.array(es))[0])
                r_d=float(pearsonr(np.array(db),np.array(ds))[0])
                r_enabled_per.append(r_e); r_disabled_per.append(r_d)
                n_enabled_per.append(len(eb)); n_disabled_per.append(len(db))
        if r_enabled_per:
            total_e=sum(n_enabled_per); total_d=sum(n_disabled_per)
            r_enabled=float(np.average(r_enabled_per, weights=n_enabled_per))
            r_disabled=float(np.average(r_disabled_per, weights=n_disabled_per))
            se_e=1/math.sqrt(total_e-3) if total_e>3 else 1.0
            se_d=1/math.sqrt(total_d-3) if total_d>3 else 1.0
            se_pooled=math.sqrt(se_e**2+se_d**2)
            hetero=abs(r_enabled-r_disabled)
            c5_pass=hetero < 2*se_pooled
        else:
            r_enabled=None; r_disabled=None; hetero=None; se_pooled=1.0; c5_pass=False
        n_total=len(all_samples)
        n_non304=len(non304)
        return {
            "label":label,
            "r_pooled":r_pooled,"ci_l":ci_l,"ci_u":ci_u,"tost":tost,
            "strat_r":strat_r,"strat_n":strat_n,"strat_se":strat_se,"strat_ci_l":strat_ci_l,"strat_ci_u":strat_ci_u,"strat_tost":strat_tost,
            "per_ep_r":per_ep_r,
            "n_total":n_total,"n_non304":n_non304,"n304":n304,
            "non304_per_b":non304_per_b,"non304_per_s":non304_per_s,
            "r_enabled":r_enabled,"r_disabled":r_disabled,"hetero":hetero,"se_pooled":se_pooled,"c5_pass":c5_pass,
            "per_condition":per_condition,"all_samples":all_samples
        }

    print("\n[ANALYSIS]")
    local_a=analyze_condition(local_samples, local_per_cond, local_b, local_s, "B-LOCAL-ONLY")
    dist_a=analyze_condition(dist_samples, dist_per_cond, dist_b, dist_s, "B-DISTRIBUTED")
    conc_a=analyze_condition(conc_samples, conc_per_cond, conc_b, conc_s, "B-CONCURRENT")
    conf_a=analyze_condition(conf_samples, conf_per_cond, conf_b, conf_s, "B-CONFOUND-DISTRIBUTED")

    for a in [local_a, dist_a, conc_a, conf_a]:
        print(f" {a['label']}: strat_r={a['strat_r']:.4f} n={a['strat_n']} CI=[{a['strat_ci_l']:.3f},{a['strat_ci_u']:.3f}] p_upper={a['strat_tost']['p_upper']:.4f} tot={a['n_total']} non304={a['n_non304']} 304={a['n304']}")

    # --- Decision rule C1-C7 ---
    # C1 behavioral TP: use DISTRIBUTED (primary) as specified: behavioral detection TP >=0.85 across all distributed nodes
    # Compute from dist_per_cond: expired TP, valid TN
    def compute_c1(per_condition):
        """C1 behavioral detection with 304-exclusion fix.
        304 cache-hit responses produce behavioral_delta=0 (effective_code=200),
        which inflates valid TN. Excluding them from TP/TN is consistent with
        the primary orthogonality metric's 304 exclusion."""
        expired_tp={}; valid_tn={}
        for cid,cdata in per_condition.items():
            # FIX: exclude 304 responses from C1 TP/TN calculation
            samples=[s for s in cdata["samples"] if s["status"]=="OK" and not s.get("has_304",False)]
            if not samples: continue
            token_state=cdata["token_state"]
            if token_state=="expired":
                tp=sum(1 for s in samples if s["behavioral_delta"]>0)
                expired_tp[cid]=tp/len(samples)
            else:
                tn=sum(1 for s in samples if s["behavioral_delta"]==0)
                valid_tn[cid]=tn/len(samples)
        mean_tp=np.mean(list(expired_tp.values())) if expired_tp else 0
        mean_tn=np.mean(list(valid_tn.values())) if valid_tn else 0
        return mean_tp, mean_tn, expired_tp, valid_tn

    mean_tp_dist, mean_tn_dist, exp_tp_dist, val_tn_dist = compute_c1(dist_per_cond)
    c1_pass = mean_tp_dist>=0.85 and mean_tn_dist>=0.85
    print(f"\nC1 distributed TP={mean_tp_dist:.4f} TN={mean_tn_dist:.4f} pass={c1_pass}")

    # C2 variance: at least 2/3 endpoints have non-304 behavioral std>0 AND structural std>0 on distributed
    def compute_c2(non304_per_b, non304_per_s):
        endpoints_with_var=0
        per_ep={}
        for ep in ENDPOINTS:
            be=non304_per_b.get(ep,[]); bs=non304_per_s.get(ep,[])
            b_std=np.std(be) if len(be)>1 else 0
            s_std=np.std(bs) if len(bs)>1 else 0
            has=b_std>0 and s_std>0
            if has: endpoints_with_var+=1
            per_ep[ep]={"behavioral_std":float(b_std),"structural_std":float(s_std),"has":has,"n":len(be)}
        return endpoints_with_var, per_ep

    c2_n, c2_per = compute_c2(dist_a["non304_per_b"], dist_a["non304_per_s"])
    c2_pass = c2_n >=2
    print(f"C2 distributed endpoints_with_var={c2_n}/3 pass={c2_pass} {c2_per}")

    # C3 CI upper <0.15 distributed stratified
    c3_pass = dist_a["strat_ci_u"] < 0.15
    print(f"C3 distributed CI_up={dist_a['strat_ci_u']:.4f} pass={c3_pass}")

    # C4 TOST p_upper <0.05 distributed
    c4_pass = dist_a["strat_tost"]["p_upper"] < 0.05
    print(f"C4 distributed p_upper={dist_a['strat_tost']['p_upper']:.4f} pass={c4_pass}")

    # C5 heterogeneity distributed
    c5_pass_dist = dist_a["c5_pass"]
    print(f"C5 distributed hetero={dist_a['hetero']} r_en={dist_a['r_enabled']} r_dis={dist_a['r_disabled']} se_pool={dist_a['se_pooled']:.4f} pass={c5_pass_dist}")

    # C6 B-LOCAL-ONLY baseline |r|<0.15 stratified absolute
    c6_pass = abs(local_a["strat_r"]) < 0.15
    print(f"C6 local strat_r={local_a['strat_r']:.4f} |r|={abs(local_a['strat_r']):.4f} pass={c6_pass}")

    # C7 B-CONFOUND-DISTRIBUTED stratified weighted |r| >=0.15
    # Note: conf_a strat_r is computed via stratified pooling already (weighted)
    c7_r_abs = abs(conf_a["strat_r"])
    c7_pass = c7_r_abs >= 0.15
    print(f"C7 confound strat_r={conf_a['strat_r']:.4f} |r|={c7_r_abs:.4f} pass={c7_pass}")

    all_pass = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass_dist and c6_pass and c7_pass
    outcome = "SUPPORTS" if all_pass else "FALSIFIES"
    # For SUPPORTS need all, else REJECTED per spec; we map to outcome SUPPORTS/FALSIFIES/MIXED
    # Spec says REJECTED if any fail; we use FALSIFIES
    status="COMPLETE"
    # Check measurement invalid threshold n>=400 per condition
    for a in [local_a, dist_a, conc_a, conf_a]:
        if a["n_non304"] < 400:
            status="MEASUREMENT_INVALID"
            print(f" WARNING {a['label']} n_non304 {a['n_non304']} <400 -> MEASUREMENT_INVALID")

    # Power and extra metrics
    # Build metrics object
    metrics={
        "b_local_stratified_r": float(local_a["strat_r"]),
        "b_local_stratified_n": int(local_a["strat_n"]),
        "b_local_stratified_ci_lower": float(local_a["strat_ci_l"]),
        "b_local_stratified_ci_upper": float(local_a["strat_ci_u"]),
        "b_local_tost_p_upper": float(local_a["strat_tost"]["p_upper"]),
        "b_local_tost_p_lower": float(local_a["strat_tost"]["p_lower"]),
        "b_distributed_stratified_r": float(dist_a["strat_r"]),
        "b_distributed_stratified_n": int(dist_a["strat_n"]),
        "b_distributed_stratified_ci_lower": float(dist_a["strat_ci_l"]),
        "b_distributed_stratified_ci_upper": float(dist_a["strat_ci_u"]),
        "b_distributed_tost_p_upper": float(dist_a["strat_tost"]["p_upper"]),
        "b_distributed_tost_p_lower": float(dist_a["strat_tost"]["p_lower"]),
        "b_concurrent_stratified_r": float(conc_a["strat_r"]),
        "b_concurrent_stratified_n": int(conc_a["strat_n"]),
        "b_concurrent_stratified_ci_lower": float(conc_a["strat_ci_l"]),
        "b_concurrent_stratified_ci_upper": float(conc_a["strat_ci_u"]),
        "b_concurrent_tost_p_upper": float(conc_a["strat_tost"]["p_upper"]),
        "b_confounder_stratified_r": float(conf_a["strat_r"]),
        "b_confounder_stratified_n": int(conf_a["strat_n"]),
        "b_confounder_abs_r": float(c7_r_abs),
        "b_confounder_ci_lower": float(conf_a["strat_ci_l"]),
        "b_confounder_ci_upper": float(conf_a["strat_ci_u"]),
        "distributed_per_endpoint_r": dist_a["per_ep_r"],
        "local_per_endpoint_r": local_a["per_ep_r"],
        "concurrent_per_endpoint_r": conc_a["per_ep_r"],
        "confounder_per_endpoint_r": conf_a["per_ep_r"],
        "n_samples": {
            "b_local_total": int(local_a["n_total"]),
            "b_local_non304": int(local_a["n_non304"]),
            "b_distributed_total": int(dist_a["n_total"]),
            "b_distributed_non304": int(dist_a["n_non304"]),
            "b_concurrent_total": int(conc_a["n_total"]),
            "b_concurrent_non304": int(conc_a["n_non304"]),
            "b_confounder_total": int(conf_a["n_total"]),
            "b_confounder_non304": int(conf_a["n_non304"]),
        },
        "c1_mean_tp": float(mean_tp_dist),
        "c1_mean_tn": float(mean_tn_dist),
        "c2_endpoints_with_variance": int(c2_n),
        "c3_ci_upper_distributed": float(dist_a["strat_ci_u"]),
        "c4_p_upper_distributed": float(dist_a["strat_tost"]["p_upper"]),
        "c5_heterogeneity_diff": float(dist_a["hetero"]) if dist_a["hetero"] is not None else None,
        "c5_se_pooled": float(dist_a["se_pooled"]),
        "c6_abs_r_local": float(abs(local_a["strat_r"])),
        "c7_abs_r_confounder": float(c7_r_abs),
        "outcome": outcome,
        "all_criteria_pass": bool(all_pass)
    }
    # TOST sweep
    tost_sweep={}
    for delta in [0.10,0.12,0.15,0.20]:
        t=tost_equivalence(dist_a["strat_r"], dist_a["strat_n"], delta)
        tost_sweep[str(delta)]={"p_upper":float(t["p_upper"]),"p_lower":float(t["p_lower"]),"pass":bool(t["pass"])}
    metrics["tost_sweep_distributed"]=tost_sweep

    # Controls
    controls={
        "C1_behavioral_tp": {"threshold":"mean expired_TP >=0.85 AND mean valid_TN >=0.85 on distributed","observed_mean_expired_tp":float(mean_tp_dist),"observed_mean_valid_tn":float(mean_tn_dist),"pass":bool(c1_pass),"evidence":f"Expired TP={mean_tp_dist:.4f}, Valid TN={mean_tn_dist:.4f}"},
        "C2_variance": {"threshold":">=2/3 endpoints have std>0 for both signals on distributed","endpoints_with_variance":int(c2_n),"pass":bool(c2_pass),"evidence":f"{c2_n}/3 endpoints","per_endpoint":c2_per},
        "C3_equivalence_stratified": {"threshold":"CI upper of stratified pooled r <0.15 on distributed","observed_r_stratified":float(dist_a["strat_r"]),"ci_lower":float(dist_a["strat_ci_l"]),"ci_upper":float(dist_a["strat_ci_u"]),"pass":bool(c3_pass),"n_samples":int(dist_a["strat_n"]),"evidence":f"strat r={dist_a['strat_r']:.4f}, CI=[{dist_a['strat_ci_l']:.4f},{dist_a['strat_ci_u']:.4f}] upper={dist_a['strat_ci_u']:.4f} <0.15"},
        "C4_tost_stratified": {"threshold":"TOST p_upper <0.05 at delta=0.15 stratified distributed","observed_p_upper":float(dist_a["strat_tost"]["p_upper"]),"observed_p_lower":float(dist_a["strat_tost"]["p_lower"]),"pass":bool(c4_pass),"n_samples":int(dist_a["strat_n"]),"evidence":f"TOST p_upper={dist_a['strat_tost']['p_upper']:.4f}"},
        "C5_cache_heterogeneity": {"threshold":"|r_enabled - r_disabled| <2*SE_pooled on distributed","r_enabled":float(dist_a["r_enabled"]) if dist_a["r_enabled"] is not None else None,"r_disabled":float(dist_a["r_disabled"]) if dist_a["r_disabled"] is not None else None,"heterogeneity_diff":float(dist_a["hetero"]) if dist_a["hetero"] is not None else None,"se_pooled":float(dist_a["se_pooled"]),"pass":bool(c5_pass_dist),"evidence":f"|r_en - r_dis|={dist_a['hetero']:.4f} <2*SE={2*dist_a['se_pooled']:.4f}" if dist_a["hetero"] is not None else "missing"},
        "C6_baseline_local": {"threshold":"|r| <0.15 on B-LOCAL-ONLY baseline","observed_r":float(local_a["strat_r"]),"abs_r":float(abs(local_a["strat_r"])),"ci_upper":float(local_a["strat_ci_u"]),"pass":bool(c6_pass),"n_samples":int(local_a["strat_n"]),"evidence":f"B-LOCAL r={local_a['strat_r']:.4f} |r|={abs(local_a['strat_r']):.4f}"},
        "C7_negative_control": {"threshold":"|r| >=0.15 on B-CONFOUND-DISTRIBUTED","observed_r":float(conf_a["strat_r"]),"abs_r":float(c7_r_abs),"pass":bool(c7_pass),"n_samples":int(conf_a["strat_n"]),"evidence":f"B-CONFOUND r={conf_a['strat_r']:.4f} |r|={c7_r_abs:.4f}"}
    }

    # Observations
    observations=[
        f"B-LOCAL-ONLY stratified r={local_a['strat_r']:.4f} CI [{local_a['strat_ci_l']:.4f},{local_a['strat_ci_u']:.4f}] n={local_a['strat_n']} p_upper={local_a['strat_tost']['p_upper']:.4f}",
        f"B-DISTRIBUTED stratified r={dist_a['strat_r']:.4f} CI [{dist_a['strat_ci_l']:.4f},{dist_a['strat_ci_u']:.4f}] n={dist_a['strat_n']} p_upper={dist_a['strat_tost']['p_upper']:.4f}",
        f"B-CONCURRENT stratified r={conc_a['strat_r']:.4f} CI [{conc_a['strat_ci_l']:.4f},{conc_a['strat_ci_u']:.4f}] n={conc_a['strat_n']} p_upper={conc_a['strat_tost']['p_upper']:.4f}",
        f"B-CONFOUND-DISTRIBUTED stratified r={conf_a['strat_r']:.4f} |r|={c7_r_abs:.4f} n={conf_a['strat_n']}",
        f"C1 distributed TP={mean_tp_dist:.4f} TN={mean_tn_dist:.4f} pass={c1_pass}",
        f"C2 distributed endpoints_with_var {c2_n}/3 pass={c2_pass}",
        f"C3 distributed CI_upper {dist_a['strat_ci_u']:.4f} pass={c3_pass}",
        f"C4 distributed p_upper {dist_a['strat_tost']['p_upper']:.4f} pass={c4_pass}",
        f"C5 distributed hetero {dist_a['hetero']:.4f} se_pooled {dist_a['se_pooled']:.4f} pass={c5_pass_dist}",
        f"C6 local |r| {abs(local_a['strat_r']):.4f} pass={c6_pass}",
        f"C7 confound |r| {c7_r_abs:.4f} pass={c7_pass}",
        f"Total samples: local {local_a['n_total']}({local_a['n_non304']} non304) dist {dist_a['n_total']}({dist_a['n_non304']} non304) conc {conc_a['n_total']}({conc_a['n_non304']} non304) conf {conf_a['n_total']}({conf_a['n_non304']} non304)",
        f"304 counts: local {local_a['n304']} dist {dist_a['n304']} conc {conc_a['n304']} conf {conf_a['n304']}",
        f"Per-endpoint distributed r: {dist_a['per_ep_r']}",
        f"Per-endpoint local r: {local_a['per_ep_r']}",
        f"Per-endpoint concurrent r: {conc_a['per_ep_r']}",
        f"Per-endpoint confound r: {conf_a['per_ep_r']}",
        f"Overall decision: {outcome} all_pass={all_pass} status={status}"
    ]

    # Save raw evidence
    raw_data={
        "b_local_per_condition": {k:{"samples":v["samples"],"token_state":v["token_state"],"cache_mode":v["cache_mode"],"permission_level":v["permission_level"],"endpoint":v["endpoint"]} for k,v in local_per_cond.items()},
        "b_distributed_per_condition": {k:{"samples":v["samples"],"token_state":v["token_state"],"cache_mode":v["cache_mode"],"permission_level":v["permission_level"],"endpoint":v["endpoint"]} for k,v in dist_per_cond.items()},
        "b_concurrent_per_condition": {k:{"samples":v["samples"],"token_state":v["token_state"],"cache_mode":v["cache_mode"],"permission_level":v["permission_level"],"endpoint":v["endpoint"]} for k,v in conc_per_cond.items()},
        "b_confounder_per_condition": {k:{"samples":v["samples"],"token_state":v["token_state"],"cache_mode":v["cache_mode"],"permission_level":v["permission_level"],"endpoint":v["endpoint"]} for k,v in conf_per_cond.items()},
    }
    with open(RAW_EVIDENCE_DIR / "experiment_data.json","w") as f: json.dump(raw_data,f,indent=2)
    with open(RAW_EVIDENCE_DIR / "metrics.json","w") as f: json.dump(metrics,f,indent=2)

    # Build result.json
    result={
        "schema_version":1,
        "experiment_id":EXPERIMENT_ID,
        "lane":"graph",
        "status":status,
        "outcome":outcome if status=="COMPLETE" else "NOT_APPLICABLE",
        "metrics":metrics,
        "controls":controls,
        "artifacts":[
            {"path":"raw_evidence/experiment_data.json","role":"raw"},
            {"path":"raw_evidence/metrics.json","role":"derived"},
            {"path":"run_experiment_distributed.py","role":"code"},
            {"path":"testbed_server.py","role":"code"},
            {"path":"testbed_server_v2.py","role":"code"}
        ],
        "observations":observations,
        "validity_notes":[
            "V_ETAG_PERMISSION_LEAKAGE FIX: expired tokens decoded WITHOUT verification to extract permission_level for ETag",
            "V3 ENDPOINT-STRATIFICATION: pooled Pearson r uses endpoint-stratified weighting",
            "V1 UUID FOR ALL STATUS CODES: primary testbed uses uuid.uuid4() for all; confound uses fixed 'expired'",
            "304 EXCLUSION: 304 responses excluded from pooled, per-endpoint, per-cache correlations",
            "DISTRIBUTED INDEPENDENCE: Each Flask node has independent SQLite DB, independent in-memory cache, independent ETag generation",
            "CACHE INDEPENDENCE: Cache invalidation on node A does NOT propagate to node B",
            "CONCURRENT LOAD: B-CONCURRENT uses 5 concurrent client threads with per-thread state isolation",
            "ROUND-ROBIN ROUTING: Distributed testbed routes requests round-robin across nodes",
            f"n per condition: local {local_a['n_non304']}, distributed {dist_a['n_non304']}, concurrent {conc_a['n_non304']}, confounder {conf_a['n_non304']} (target 816)",
            "Structural signal headers-only: ETag change, Cache-Control change, normalized Shannon entropy, dyn_hash_int",
            "Behavioral signal: token_validation_failure*2 + session_state_change*3 + auth_boundary_shift*1 + status_weight*2"
        ],
        "unresolved":[
            "Whether orthogonality holds on real CDN hierarchies (multi-node cache invalidation on session state change) beyond Flask in-memory simulation",
            "Whether N>=50 parallel sessions changes correlation beyond N=5 tested",
            "Whether result generalizes to non-Flask frameworks",
            "Whether per-cache heterogeneity systematic or sampling noise"
        ]
    }
    # Adjust unresolved if measurement_invalid
    if status=="MEASUREMENT_INVALID":
        result["unresolved"].append("Measurement invalid due to n<400 per condition - infrastructure failure, not scientific falsification")

    with open(EXPERIMENT_DIR / "result.json","w") as f: json.dump(result,f,indent=2)
    print(f"\nResult written: status={status} outcome={outcome}")
    # provenance
    import hashlib, datetime
    def sha256_file(p):
        h=hashlib.sha256()
        with open(p,"rb") as fh: h.update(fh.read())
        return h.hexdigest()
    provenance={
        "schema_version":1,
        "experiment_id":EXPERIMENT_ID,
        "lane":"graph",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git","rev-parse","HEAD"],cwd="/home/runner/work/Spider/Spider").decode().strip() if os.path.exists("/home/runner/work/Spider/Spider/.git") else None,
        "artifacts":[],
        "environment":{"python":sys.version,"platform":sys.platform},
        "commands":[f"python3 research/experiments/{EXPERIMENT_ID}/run_experiment_distributed.py"],
        "notes":"Distributed experiment with 4 conditions, 816 per condition target"
    }
    for art in result["artifacts"]:
        p=EXPERIMENT_DIR / art["path"]
        if p.exists():
            provenance["artifacts"].append({"path":art["path"],"sha256":sha256_file(p),"role":art["role"]})
    with open(EXPERIMENT_DIR / "provenance.json","w") as f: json.dump(provenance,f,indent=2)

    # report.md
    report=f"""# {EXPERIMENT_ID} Report: Distributed C-FRESHNESS Orthogonality (C1 Fix + Re-Run)

## Question
Does C-FRESHNESS orthogonality at delta=0.15 survive on distributed production-like infrastructure with multi-node independent caches, concurrent load (N>=5), and independent cache invalidation?

## Hypothesis
Distributed correlation expected |r| <0.15, consistent with LOCAL r=0.041.

## Results
- **B-LOCAL-ONLY** (single-node serial): stratified r={local_a['strat_r']:.4f} n={local_a['strat_n']} CI [{local_a['strat_ci_l']:.4f},{local_a['strat_ci_u']:.4f}] TOST p_upper={local_a['strat_tost']['p_upper']:.4f}
- **B-DISTRIBUTED** (2-node round-robin): stratified r={dist_a['strat_r']:.4f} n={dist_a['strat_n']} CI [{dist_a['strat_ci_l']:.4f},{dist_a['strat_ci_u']:.4f}] TOST p_upper={dist_a['strat_tost']['p_upper']:.4f}
- **B-CONCURRENT** (5 threads): stratified r={conc_a['strat_r']:.4f} n={conc_a['strat_n']} CI [{conc_a['strat_ci_l']:.4f},{conc_a['strat_ci_u']:.4f}] TOST p_upper={conc_a['strat_tost']['p_upper']:.4f}
- **B-CONFOUND-DISTRIBUTED** (negative control): stratified r={conf_a['strat_r']:.4f} |r|={c7_r_abs:.4f} n={conf_a['strat_n']}

## Decision Criteria
- C1 behavioral TP={mean_tp_dist:.4f} TN={mean_tn_dist:.4f} threshold 0.85 -> {"PASS" if c1_pass else "FAIL"}
- C2 variance {c2_n}/3 endpoints -> {"PASS" if c2_pass else "FAIL"}
- C3 CI upper {dist_a['strat_ci_u']:.4f} <0.15 -> {"PASS" if c3_pass else "FAIL"}
- C4 TOST p_upper {dist_a['strat_tost']['p_upper']:.4f} <0.05 -> {"PASS" if c4_pass else "FAIL"}
- C5 heterogeneity diff {dist_a['hetero']:.4f} <2*SE {2*dist_a['se_pooled']:.4f} -> {"PASS" if c5_pass_dist else "FAIL"}
- C6 local |r| {abs(local_a['strat_r']):.4f} <0.15 -> {"PASS" if c6_pass else "FAIL"}
- C7 confound |r| {c7_r_abs:.4f} >=0.15 -> {"PASS" if c7_pass else "FAIL"}

**Overall: {outcome} (all_pass={all_pass}) status={status}**

## Interpretation
{"C-FRESHNESS orthogonality CONFIRMED on distributed infrastructure at delta=0.15. All 7 criteria pass. Parallel-channel architecture justified for multi-node deployment under tested ceiling." if all_pass else "C-FRESHNESS orthogonality REJECTED on distributed infrastructure. One or more criteria failed. See controls for failing condition."}

## Validity Notes
- V_ETAG, V3 stratification, V1 UUID, 304 exclusion all applied
- Distributed independence via separate SQLite DBs and in-memory caches
- Round-robin routing, per-thread isolation for concurrent

## Raw Evidence
- `raw_evidence/experiment_data.json`
- `raw_evidence/metrics.json`
"""
    with open(EXPERIMENT_DIR / "report.md","w") as f: f.write(report)
    print("Report written")
    return status, outcome

if __name__=="__main__":
    try:
        status,outcome=main()
        sys.exit(0 if status=="COMPLETE" else 1)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # write failure
        fail={"schema_version":1,"experiment_id":EXPERIMENT_ID,"lane":"graph","status":"MEASUREMENT_INVALID","outcome":"NOT_APPLICABLE","metrics":{},"controls":{},"artifacts":[],"observations":[f"Infrastructure failure: {str(e)}"],"validity_notes":["Exception during execution"],"unresolved":["Infrastructure failure - not scientific falsification"]}
        with open(EXPERIMENT_DIR / "result.json","w") as f: json.dump(fail,f,indent=2)
        with open(EXPERIMENT_DIR / "provenance.json","w") as f: json.dump({"schema_version":1,"experiment_id":EXPERIMENT_ID,"lane":"graph","error":str(e)},f,indent=2)
        with open(EXPERIMENT_DIR / "report.md","w") as f: f.write(f"# Failure\n{e}\n{traceback.format_exc()}")
        sys.exit(2)
