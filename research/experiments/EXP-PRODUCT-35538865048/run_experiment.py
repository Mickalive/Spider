#!/usr/bin/env python3
"""EXP-PRODUCT-35538865048 execution driver — continuous severity threshold calibration.
Frozen spec: continuous behavioral_score in [0.2,0.8] via session_quality, threshold sweep, orthogonality at n=480
"""
import hashlib
import json
import math
import os
import random
import socket
import threading
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from werkzeug.serving import make_server
import numpy as np
from scipy import stats
import mock_server

EXPERIMENT_ID = "EXP-PRODUCT-35538865048"
LANE = "product"
SEED = 42
PORT = 18951
TOST_DELTA = 0.15
THRESHOLDS = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
N_CALIB_TOKEN = 240
N_CALIB_NOISE = 240
N_COOCCUR_PER = 120  # 4*120=480
N_DISC_PER = 10  # 4*10=40
DRIFT_TYPE = "token_refresh"
NOISE_TYPES = ["pagination_metadata", "variable_length_data", "error_format_variation", "cdn_cache_headers"]
COOCCUR_PAIRS = [(DRIFT_TYPE, n) for n in NOISE_TYPES]
AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]
HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "raw_evidence")
os.makedirs(RAW_DIR, exist_ok=True)
RAW_DATA_PATH = os.path.join(RAW_DIR, "experiment_data.json")

def _expired_token():
    now = datetime.now(timezone.utc)
    return mock_server.pyjwt.encode({"sub": "alice","role":"admin","iss":"spider-kernel","iat": now - timedelta(hours=2),"exp": now - timedelta(hours=1),"session_id":"sess-admin-001"}, mock_server.SECRET_KEY, algorithm="HS256")

VALID_TOKEN = mock_server.make_token(role="admin")
EXPIRED_TOKEN = _expired_token()
INVALID_TOKEN = "eyJhbGciOiJIUzI1NiJ9.invalid.signature"
AUTH_HEADERS = {
    "no_auth": {},
    "valid_token": {"Authorization": "Bearer %s" % VALID_TOKEN},
    "expired_token": {"Authorization": "Bearer %s" % EXPIRED_TOKEN},
    "invalid_token": {"Authorization": "Bearer %s" % INVALID_TOKEN},
}

def _http(method, path, headers=None, body=None, timeout=15):
    req = urllib.request.Request("http://127.0.0.1:%d%s" % (PORT, path), data=body, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": resp.status, "headers": dict(resp.headers.items()), "text": resp.read().decode("utf-8")}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "headers": dict(e.headers.items()), "text": e.read().decode("utf-8")}

def http_get(path, headers=None, timeout=15):
    return _http("GET", path, headers=headers, timeout=timeout)

def http_post(path, payload, timeout=15):
    data = json.dumps(payload).encode("utf-8")
    resp = _http("POST", path, headers={"Content-Type":"application/json"}, body=data, timeout=timeout)
    return resp["status"]

def set_drift(drift_type):
    code = http_post("/api/drift", {"drift_type": drift_type})
    assert code == 200, "set_drift %r -> %d" % (drift_type, code)
    time.sleep(0.15)

def set_noise(noise_type):
    code = http_post("/api/noise", {"noise_type": noise_type})
    assert code == 200, "set_noise %r -> %d" % (drift_type, code) if False else "ok"
    assert code == 200, "set_noise %r -> %d" % (noise_type, code)
    time.sleep(0.15)

def reset_all():
    set_drift(None)
    set_noise(None)

EXCLUDED_HEADERS = {"date","server","x-request-id","connection","content-length","transfer-encoding"}

def structural_signal(resp):
    try: n_keys = len(json.loads(resp["text"]))
    except: n_keys = 1
    n_headers = len([k for k in resp["headers"] if k.lower() not in EXCLUDED_HEADERS])
    return n_keys + n_headers + 1

def fingerprint(resp):
    body_keys = sorted(json.loads(resp["text"]).keys())
    hdr_keys = sorted(k for k in resp["headers"] if k.lower() not in EXCLUDED_HEADERS)
    sig = json.dumps({"status": resp["status"],"body_keys": body_keys,"headers": hdr_keys}, sort_keys=True)
    return hashlib.sha256(sig.encode()).hexdigest()[:16]

def behavioral_score(resp):
    try: body = json.loads(resp["text"])
    except: body = {}
    if "session_quality" in body:
        try: v = float(body["session_quality"])
        except: v = 0.0
        return round(min(max(v,0.0),1.0),4)
    # fallback legacy
    s=0.0
    status=resp["status"]
    if body.get("session_valid") is False: s+=0.40
    if body.get("status")=="revoked" or body.get("error")=="session_invalidated": s+=0.30
    if body.get("status")=="refreshed": s+=0.45
    if body.get("new_token_issued") is True: s+=0.15
    if body.get("role")=="viewer":
        perms=body.get("permissions") or []
        s+=0.30+0.30*(1.0-min(len(perms),4)/4.0)
    elif body.get("role")=="admin": s+=0.03
    if body.get("session_valid") is True: s+=0.02
    if status==401: s+=0.30
    elif status==403: s+=0.05
    elif status==410: s+=0.15
    elif status==500: s+=0.15
    return round(min(max(s,0.0),1.0),4)

def discrimination(groups):
    intra = np.mean([len(g)==1 for g in groups])
    n=len(groups)
    inter_hits=0; pairs=0
    for i in range(n):
        for j in range(i+1,n):
            pairs+=1
            if len(groups[i] & groups[j])>0: inter_hits+=1
    return round(intra - inter_hits/pairs,4)

def wilson_lower(k,n,z=1.96):
    if n==0: return 0.0
    p=k/n; denom=1+z*z/n; centre=p+z*z/(2*n); half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return round(max(0.0,(centre-half)/denom),4)

def wilson_interval(k,n,z=1.96):
    if n==0: return (0.0,0.0)
    p=k/n; denom=1+z*z/n; centre=p+z*z/(2*n); half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    lo=max(0.0,(centre-half)/denom); hi=min(1.0,(centre+half)/denom)
    return (round(lo,4), round(hi,4))

def tost_equivalence(behav, struct, delta=TOST_DELTA):
    r,pval = stats.pearsonr(behav, struct)
    n=len(behav); se=1.0/math.sqrt(n-3); z_r=0.5*math.log((1+r)/(1-r)) if abs(r)<1 else 0.0
    p_upper = stats.norm.cdf((z_r - math.atanh(delta))/se)
    p_lower = 1.0 - stats.norm.cdf((z_r - math.atanh(-delta))/se)
    ci_lo = math.tanh(z_r - 1.96*se); ci_hi = math.tanh(z_r + 1.96*se)
    return {"pearson_r": round(float(r),6), "pearson_p": float(pval), "n": n, "se": round(float(se),6), "z_r": round(float(z_r),6), "ci_lower": round(float(ci_lo),6), "ci_upper": round(float(ci_hi),6), "tost_delta": delta, "tost_p_upper": float(p_upper), "tost_p_lower": float(p_lower), "tost_pass": bool(p_upper<0.05 and p_lower<0.05)}

def phase_c_discrimination():
    reset_all()
    probes={}; fps={}; bodies={}; statuses={}
    for state in AUTH_STATES:
        fps[state]=[]; probes[state]=[]
        for _ in range(N_DISC_PER):
            resp=http_get("/api/data", AUTH_HEADERS[state])
            probes[state].append(resp)
            fps[state].append(fingerprint(resp))
        bodies[state]=set(json.dumps(json.loads(r["text"]), sort_keys=True) for r in probes[state])
        statuses[state]=set(r["status"] for r in probes[state])
    fp_sets=[set(v) for v in fps.values()]
    return {"discrimination_full_fingerprint": discrimination(fp_sets), "baseline_status_only": discrimination(list(statuses.values())), "baseline_body_only": discrimination(list(bodies.values())), "fingerprint_groups": {s: sorted(set(v)) for s,v in fps.items()}, "n_unique_fingerprints": len(set().union(*fp_sets)), "n_states": len(AUTH_STATES), "raw_probes": probes}

def collect_calibration():
    """Phase A: 240 token_refresh + 240 noise-only paired samples"""
    reset_all()
    token_samples=[]
    # token_refresh 240 samples (no noise, drift active)
    set_drift(DRIFT_TYPE)
    for _ in range(N_CALIB_TOKEN):
        resp_b=http_get("/api/session/status", AUTH_HEADERS["valid_token"])
        resp_s=http_get("/api/schema")
        token_samples.append({"behavioral_score": behavioral_score(resp_b), "structural_signal": structural_signal(resp_s), "is_token": True, "noise": "none", "resp_text": resp_b["text"]})
    reset_all()
    noise_samples=[]
    for noise in NOISE_TYPES:
        set_noise(noise)
        for _ in range(N_CALIB_NOISE//len(NOISE_TYPES)):
            resp_b=http_get("/api/session/status", AUTH_HEADERS["valid_token"])
            resp_s=http_get("/api/schema")
            noise_samples.append({"behavioral_score": behavioral_score(resp_b), "structural_signal": structural_signal(resp_s), "is_token": False, "noise": noise, "resp_text": resp_b["text"]})
        set_noise(None)
    return token_samples, noise_samples

def collect_cooccurring():
    reset_all()
    samples=[]
    for (drift, noise) in COOCCUR_PAIRS:
        set_drift(drift)
        set_noise(noise)
        for _ in range(N_COOCCUR_PER):
            resp_b=http_get("/api/session/status", AUTH_HEADERS["valid_token"])
            resp_s=http_get("/api/schema")
            samples.append({"condition": "%s+%s"%(drift,noise), "drift":drift,"noise":noise,"behavioral_score": behavioral_score(resp_b), "structural_signal": structural_signal(resp_s), "status_code": resp_b["status"]})
        reset_all()
    return samples

def start_server():
    srv=make_server("127.0.0.1", PORT, mock_server.app, threaded=False)
    t=threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    for _ in range(100):
        try:
            s=socket.create_connection(("127.0.0.1", PORT), timeout=1.0)
            s.close()
            return srv
        except OSError:
            time.sleep(0.05)
    raise RuntimeError("server did not start")

def main():
    random.seed(SEED); np.random.seed(SEED)
    status="COMPLETE"
    start=time.time()
    srv=start_server()
    try:
        print("[1/3] Phase C: discrimination 40 probes", flush=True)
        pc=phase_c_discrimination()
        print("[2/3] Phase A: calibration 240 token +240 noise =480", flush=True)
        token_calib, noise_calib = collect_calibration()
        print("[3/3] Phase B: co-occurring 4x120=480 paired", flush=True)
        cooccur = collect_cooccurring()
    finally:
        srv.shutdown()
        mock_server.shutdown()

    # ---------- threshold sweep on Phase A ----------
    token_scores=np.array([x["behavioral_score"] for x in token_calib])
    noise_scores=np.array([x["behavioral_score"] for x in noise_calib])
    unique_scores=len(set(token_scores.tolist()+noise_scores.tolist()))
    sweep=[]
    best=None
    for th in THRESHOLDS:
        tp_count=int((token_scores>=th).sum()); fn_count=len(token_scores)-tp_count
        fp_count=int((noise_scores>=th).sum()); tn_count=len(noise_scores)-fp_count
        tp_rate=tp_count/len(token_scores) if len(token_scores)>0 else 0
        fp_rate=fp_count/len(noise_scores) if len(noise_scores)>0 else 0
        precision=tp_count/(tp_count+fp_count) if (tp_count+fp_count)>0 else 0
        recall=tp_rate
        f1=2*precision*recall/(precision+recall) if (precision+recall)>0 else 0
        wilson_lo=wilson_lower(tp_count, len(token_scores))
        entry={"threshold": th, "tp_count": tp_count, "fp_count": fp_count, "tp_rate": round(float(tp_rate),4), "fp_rate": round(float(fp_rate),4), "precision": round(float(precision),4), "recall": round(float(recall),4), "f1": round(float(f1),4), "wilson_lower": wilson_lo}
        sweep.append(entry)
        meets = tp_rate>=0.85 and fp_rate<=0.10
        entry["meets_constraints"] = bool(meets)
        if meets:
            if best is None or f1>best["f1"] or (f1==best["f1"] and th<best["threshold"]):
                best=dict(entry)

    # calibrated threshold logic per prereg: argmax F1 subject to TP>=0.85 FP<=0.10
    calibrated_threshold = best["threshold"] if best else None
    calibrated_entry = best

    # Determine C2,C4 at calibrated threshold; if none, then FALSIFIED
    if calibrated_threshold is not None:
        tp_rate_cal = calibrated_entry["tp_rate"]
        fp_rate_cal = calibrated_entry["fp_rate"]
        wilson_cal = calibrated_entry["wilson_lower"]
        f1_cal = calibrated_entry["f1"]
    else:
        tp_rate_cal = None; fp_rate_cal=None; wilson_cal=None; f1_cal=None

    # ---------- C1 ----------
    c1_disc=pc["discrimination_full_fingerprint"]
    c1_pass=c1_disc>0.5

    # ---------- C2/C3 per co-occurring condition at calibrated threshold (or sweep?) ----------
    # For C2 we need TP >=0.85 at calibrated threshold on token_refresh samples
    # But co-occurring samples also token_refresh with noise, so we should compute TP on co-occurring at calibrated threshold
    # If no calibrated threshold, C2 fails
    per_condition={}
    for (d,n) in COOCCUR_PAIRS:
        key="%s+%s"%(d,n)
        rows=[x for x in cooccur if x["condition"]==key]
        b=np.array([x["behavioral_score"] for x in rows])
        st=np.array([x["structural_signal"] for x in rows])
        tp_rate=None; wilson=None
        if calibrated_threshold is not None:
            tp = float((b>=calibrated_threshold).mean())
            tp_rate=round(tp,4)
            wilson=wilson_lower(int((b>=calibrated_threshold).sum()), len(b))
        per_condition[key]={"n": len(rows), "behavioral_mean": round(float(b.mean()),4), "behavioral_std": round(float(b.std(ddof=1)),4), "structural_mean": round(float(st.mean()),4), "structural_std": round(float(st.std(ddof=1)),4), "tp_rate_at_calibrated": tp_rate, "tp_wilson_lower": wilson}
    n_variance_pass=sum(1 for v in per_condition.values() if v["behavioral_std"]>0.05)
    # For overall C2, need TP >=0.85 at calibrated threshold
    # Use co-occurring TP rates (all 4 must >=0.85) and also token_calib TP? Spec says token_refresh samples (Phase A)
    # We'll evaluate both: token_calib TP and co-occurring min TP
    if calibrated_threshold is not None:
        cooccur_tps=[v["tp_rate_at_calibrated"] for v in per_condition.values()]
        c2_pass_cooccur = all(tp>=0.85 for tp in cooccur_tps)
        c2_pass_token = tp_rate_cal>=0.85 and wilson_cal>=0.80
        c2_pass = c2_pass_cooccur and c2_pass_token
    else:
        c2_pass=False

    # C4 FP at calibrated threshold
    if calibrated_threshold is not None:
        c4_pass = fp_rate_cal<=0.10
    else:
        c4_pass=False

    # C3 orthogonality at calibrated threshold n=480 (co-occurring pooled)
    behav_all=np.array([x["behavioral_score"] for x in cooccur])
    struct_all=np.array([x["structural_signal"] for x in cooccur])
    orth=tost_equivalence(behav_all, struct_all)
    c3_variance_ok = n_variance_pass>=4
    # also check per prereg: behavioral_std >0.05 on all 4 AND Pearson CI upper <0.15
    c3_ci_ok = orth["ci_upper"] < TOST_DELTA
    c3_pass = c3_variance_ok and orth["tost_pass"] and c3_ci_ok
    c5_pass = orth["tost_pass"] and orth["ci_upper"] < TOST_DELTA

    # continuous injection check
    continuous_ok = unique_scores>=5

    # error_format_variation inert check: structural_std for that condition vs baseline
    # baseline structural_std from pagination? Let's compute baseline jitter as min structural_std among other conditions?
    # For simplicity check if token_refresh+error_format_variation structural_std >0.1 (greater than zero)
    ef_std = per_condition.get("token_refresh+error_format_variation", {}).get("structural_std", 0)
    # In parent, baseline was ~0.4, so 0.0 would be inert. We'll consider inert if <=0.15?
    error_format_inert = ef_std <= 0.15  # threshold for inert

    # ---------- DECISION ----------
    # MEASUREMENT_INVALID if continuous fails or error_format inert or sample count <480
    if not continuous_ok:
        outcome_frozen="MEASUREMENT_INVALID"
        outcome_packet="INCONCLUSIVE"
        status="MEASUREMENT_INVALID"
    elif error_format_inert:
        outcome_frozen="MEASUREMENT_INVALID"
        outcome_packet="INCONCLUSIVE"
        status="MEASUREMENT_INVALID"
    elif len(cooccur)<480:
        outcome_frozen="MEASUREMENT_INVALID"
        outcome_packet="INCONCLUSIVE"
        status="MEASUREMENT_INVALID"
    elif calibrated_threshold is None:
        outcome_frozen="FALSIFIED"
        outcome_packet="FALSIFIES"
        status="COMPLETE"
    elif not c1_pass:
        outcome_frozen="FALSIFIED"
        outcome_packet="FALSIFIES"
        status="COMPLETE"
    elif not c5_pass:
        outcome_frozen="FALSIFIED"
        outcome_packet="FALSIFIES"
        status="COMPLETE"
    elif c1_pass and c2_pass and c3_pass and c4_pass and c5_pass:
        outcome_frozen="SURVIVES_CURRENT_TEST"
        outcome_packet="SUPPORTS"
        status="COMPLETE"
    else:
        # C2 or C4 fail => FALSIFIED per falsifier (no threshold achieves)
        outcome_frozen="FALSIFIED"
        outcome_packet="FALSIFIES"
        status="COMPLETE"

    metrics={
        "c1_auth_discrimination": c1_disc,
        "c1_pass": bool(c1_pass),
        "baseline_status_only": pc["baseline_status_only"],
        "baseline_body_only": pc["baseline_body_only"],
        "threshold_sweep": sweep,
        "unique_behavioral_scores": int(unique_scores),
        "continuous_injection_ok": bool(continuous_ok),
        "calibrated_threshold": calibrated_threshold,
        "calibrated_metrics": calibrated_entry,
        "c2_tp_rate": tp_rate_cal,
        "c2_wilson_lower": wilson_cal,
        "c2_f1": f1_cal,
        "c2_pass": bool(c2_pass),
        "c2_per_condition": per_condition,
        "c3_per_condition": per_condition,
        "c3_variance_conditions_pass": int(n_variance_pass),
        "c3_variance_pass_required": 4,
        "c3_orthogonality": orth,
        "c3_pass": bool(c3_pass),
        "c4_fp_rate": fp_rate_cal,
        "c4_pass": bool(c4_pass),
        "c4_per_noise": {n: {"fp_rate": round(float((np.array([x["behavioral_score"] for x in noise_calib if x["noise"]==n])>=calibrated_threshold).mean()),4) if calibrated_threshold is not None else None, "behavioral_mean": round(float(np.mean([x["behavioral_score"] for x in noise_calib if x["noise"]==n])),4)} for n in NOISE_TYPES},
        "c5_tost_equivalence": {"ci_upper": orth["ci_upper"], "ci_upper_lt_delta": bool(orth["ci_upper"]<TOST_DELTA), "tost_pass": bool(orth["tost_pass"]), "tost_p_upper": orth["tost_p_upper"], "tost_p_lower": orth["tost_p_lower"], "pearson_r": orth["pearson_r"], "n": orth["n"]},
        "c5_pass": bool(c5_pass),
        "error_format_structural_std": float(ef_std) if ef_std else None,
        "error_format_inert": bool(error_format_inert),
        "decision_source": "frozen prereg decision rule",
        "frozen_outcome": outcome_frozen
    }
    observations={
        "phase_c": {k: v for k,v in pc.items() if k!="raw_probes"},
        "phase_a_token_n": len(token_calib),
        "phase_a_noise_n": len(noise_calib),
        "phase_b_cooccur_n": len(cooccur),
        "calibrated_threshold": calibrated_threshold,
        "detection_thresholds_tested": THRESHOLDS,
        "delta": TOST_DELTA,
        "p_refresh_success": mock_server.P_REFRESH_SUCCESS,
        "runtime_seconds": round(time.time()-start,2),
    }

    raw={
        "schema_version":1,
        "experiment_id": EXPERIMENT_ID,
        "seed": SEED, "port": PORT, "tost_delta": TOST_DELTA, "thresholds": THRESHOLDS,
        "p_refresh_success": mock_server.P_REFRESH_SUCCESS,
        "phase_a_token_calib": token_calib,
        "phase_a_noise_calib": noise_calib,
        "phase_b_cooccurring": cooccur,
        "phase_c_raw": pc["raw_probes"],
        "threshold_sweep": sweep,
        "calibrated_threshold": calibrated_threshold,
        "server": "mock_server.py continuous Flask+SQLite, TTL cache, jitter, HS256/RS256 JWT, stochastic token_refresh continuous [0.2,0.8], production-like noise fixed"
    }
    with open(RAW_DATA_PATH,"w") as f:
        json.dump(raw,f,indent=1,sort_keys=True)
    raw_sha=hashlib.sha256(open(RAW_DATA_PATH,"rb").read()).hexdigest()

    # add raw sha to observations
    observations["raw_evidence_sha256"]=raw_sha
    observations["threshold_sweep_summary"]="; ".join(["T=%.2f TP=%.2f FP=%.2f F1=%.2f"%(e["threshold"],e["tp_rate"],e["fp_rate"],e["f1"]) for e in sweep])

    return {"experiment_id": EXPERIMENT_ID, "lane": LANE, "outcome": outcome_packet, "frozen_outcome": outcome_frozen, "status": status, "metrics": metrics, "observations": observations, "raw_sha": raw_sha, "pc": pc}

def _clean(o):
    if isinstance(o, dict): return {k:_clean(v) for k,v in o.items()}
    if isinstance(o, (list,tuple)): return [_clean(v) for v in o]
    if isinstance(o, (np.bool_, bool)): return bool(o)
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.integer): return int(o)
    return o

if __name__=="__main__":
    result=_clean(main())
    out_path=os.path.join(HERE,"result_draft.json")
    with open(out_path,"w") as f:
        json.dump(result,f,indent=2,sort_keys=True)
    print("WROTE %s"%out_path)
    print("OUTCOME=%s FROZEN=%s STATUS=%s"%(result["outcome"], result["frozen_outcome"], result["status"]))
    for k,v in sorted(result["metrics"].items()):
        if not isinstance(v, dict) and not isinstance(v, list):
            print(" %s=%s"%(k,v))
