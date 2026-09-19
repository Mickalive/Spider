#!/usr/bin/env python3
"""EXP-PRODUCT-35445596342 execution driver (C-FRESHNESS re-run).

Implements the three frozen fixes from the parent handoff
(EXP-PRODUCT-35434772331 / MEASUREMENT_INVALID):
  1) stochastic Flask+SQLite server (mock_server.py) instead of the
     deterministic WSGI server (behavioral_std was 0.0 / 720 samples);
  2) redesigned continuous severity-weighted behavioral_score with distinct
     non-overlapping ranges per drift type (parent scores collided at 0.5);
  3) full server state reset via set_drift(None) (parent had state
     carry-over between conditions).

Phases (real HTTP over localhost):
  A. C1 auth discrimination + baselines (no drift/noise, /api/data)
  B. C3 co-occurring drift x noise: 8 conditions x 60 paired samples
     (behavioral from /api/session/status, structural from /api/schema)
  C. C4 noise-only null: 4 conditions x 60
  D. C2 isolated drift TP: 3 drift types x 60
  E. C3 orthogonality (pooled Pearson r + Fisher-z TOST, delta = 0.15)

Raw evidence is dumped to raw_evidence/experiment_data.json and kept distinct
from derived metrics (metrics are computed after evidence collection only).
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
from datetime import datetime, timedelta, timezone
from werkzeug.serving import make_server

import numpy as np
from scipy import stats

import mock_server

# ===== Frozen experiment identity / parameters =====
EXPERIMENT_ID = "EXP-PRODUCT-35445596342"
LANE = "product"
SEED = 42
PORT = 18950
THRESHOLD = 0.25      # behavioral detection threshold (request.json 9/2 test)
TOST_DELTA = 0.15     # equivalence margin (replicates EXP-GRAPH-35353011131)
N_COOCCUR = 60        # samples per co-occurring condition
N_NOISE = 60          # samples per noise-only condition
N_TP = 60             # samples per isolated drift condition
N_DISC = 10           # probes per auth state

DRIFT_TYPES = ["permission_boundary", "session_invalidation", "token_refresh"]
NOISE_TYPES = ["optional_field_addition", "description_change",
               "response_time_jitter", "field_type_normalization"]
# 8 co-occurring conditions = 2 auth drifts x 4 noises (frozen spec table).
COOCCUR_PAIRS = [(d, n) for d in DRIFT_TYPES[:2] for n in NOISE_TYPES]
AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "raw_evidence")
os.makedirs(RAW_DIR, exist_ok=True)
RAW_DATA_PATH = os.path.join(RAW_DIR, "experiment_data.json")

# ===== Token fixtures =====
def _expired_token():
    now = datetime.now(timezone.utc)
    return mock_server.pyjwt.encode(
        {"sub": "alice", "role": "admin", "iss": "spider-kernel",
         "iat": now - timedelta(hours=2), "exp": now - timedelta(hours=1),
         "session_id": "sess-admin-001"},
        mock_server.SECRET_KEY, algorithm="HS256")


VALID_TOKEN = mock_server.make_token(role="admin")
EXPIRED_TOKEN = _expired_token()
INVALID_TOKEN = "eyJhbGciOiJIUzI1NiJ9.invalid.signature"

AUTH_HEADERS = {
    "no_auth": {},
    "valid_token": {"Authorization": "Bearer %s" % VALID_TOKEN},
    "expired_token": {"Authorization": "Bearer %s" % EXPIRED_TOKEN},
    "invalid_token": {"Authorization": "Bearer %s" % INVALID_TOKEN},
}

# ===== Client utilities (raw wire observables only) =====
def _http(method, path, headers=None, body=None, timeout=15):
    req = urllib.request.Request(
        "http://127.0.0.1:%d%s" % (PORT, path),
        data=body, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": resp.status,
                    "headers": dict(resp.headers.items()),
                    "text": resp.read().decode("utf-8")}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "headers": dict(e.headers.items()),
                "text": e.read().decode("utf-8")}


def http_get(path, headers=None, timeout=15):
    return _http("GET", path, headers=headers, timeout=timeout)


def http_post(path, payload, timeout=15):
    data = json.dumps(payload).encode("utf-8")
    resp = _http("POST", path,
                 headers={"Content-Type": "application/json"},
                 body=data, timeout=timeout)
    return resp["status"]


def set_drift(drift_type):
    code = http_post("/api/drift", {"drift_type": drift_type})
    assert code == 200, "set_drift(%r) -> %d" % (drift_type, code)
    time.sleep(0.2)


def set_noise(noise_type):
    code = http_post("/api/noise", {"noise_type": noise_type})
    assert code == 200, "set_noise(%r) -> %d" % (noise_type, code)
    time.sleep(0.2)


def reset_all():
    set_drift(None)   # full frozen state reset (incl. noise + DB restore)
    set_noise(None)


# ===== Structural / fingerprint observables =====
EXCLUDED_HEADERS = {"date", "server", "x-request-id", "connection",
                    "content-length", "transfer-encoding"}


def structural_signal(resp):
    """Body key count + semantic header count + status code (cardinality)."""
    try:
        n_keys = len(json.loads(resp["text"]))
    except Exception:
        n_keys = 1
    n_headers = len([k for k in resp["headers"]
                     if k.lower() not in EXCLUDED_HEADERS])
    return n_keys + n_headers + 1


def fingerprint(resp):
    body_keys = sorted(json.loads(resp["text"]).keys())
    hdr_keys = sorted(k for k in resp["headers"]
                      if k.lower() not in EXCLUDED_HEADERS)
    sig = json.dumps({"status": resp["status"], "body_keys": body_keys,
                      "headers": hdr_keys}, sort_keys=True)
    return hashlib.sha256(sig.encode()).hexdigest()[:16]


# ===== Redesigned behavioral score (frozen fix #2) =====
def behavioral_score(resp):
    """Continuous severity-weighted score from the /api/session/status
    response ONLY. Designed non-overlapping per-drift ranges:
      permission_boundary  [0.32, 0.545]   (severity x sampled perm count)
      token_refresh        0.65
      session_invalidation [0.75, 1.00]    (severity x graded status code)
      no-drift baseline    ~0.05
    """
    s = 0.0
    try:
        body = json.loads(resp["text"])
    except Exception:
        body = {}
    status = resp["status"]

    if body.get("session_valid") is False:
        s += 0.40
    if body.get("status") == "revoked" or \
            body.get("error") == "session_invalidated":
        s += 0.30
    if body.get("status") == "refreshed":
        s += 0.45
    if body.get("new_token_issued") is True:
        s += 0.15
    if body.get("role") == "viewer":
        perms = body.get("permissions") or []
        s += 0.30 + 0.30 * (1.0 - min(len(perms), 4) / 4.0)
    elif body.get("role") == "admin":
        s += 0.03
    if body.get("session_valid") is True:
        s += 0.02
    if status == 401:
        s += 0.30
    elif status == 403:
        s += 0.05
    elif status == 410:
        s += 0.15
    elif status == 500:
        s += 0.15
    return round(min(max(s, 0.0), 1.0), 4)


# ===== Metric functions =====
def discrimination(groups):
    """intra - mean(inter) over per-state fingerprint sets (parent method)."""
    intra = np.mean([len(g) == 1 for g in groups])
    n = len(groups)
    inter_hits = 0
    pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            pairs += 1
            if len(groups[i] & groups[j]) > 0:
                inter_hits += 1
    return round(intra - inter_hits / pairs, 4)


def wilson_lower(k, n, z=1.96):
    if n == 0:
        return 0.0
    p = k / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return round(max(0.0, (centre - half) / denom), 4)


def tost_equivalence(behav, struct, delta=TOST_DELTA):
    """Fisher-z TOST. Formula verified against EXP-GRAPH-35353011131
    (r=0.0463 -> tost_p_upper ~0.0110, tost_p_lower ~8e-06)."""
    r, pval = stats.pearsonr(behav, struct)
    n = len(behav)
    se = 1.0 / math.sqrt(n - 3)
    z_r = 0.5 * math.log((1 + r) / (1 - r))
    p_upper = stats.norm.cdf((z_r - math.atanh(delta)) / se)
    p_lower = 1.0 - stats.norm.cdf((z_r - math.atanh(-delta)) / se)
    ci_lo = math.tanh(z_r - 1.96 * se)
    ci_hi = math.tanh(z_r + 1.96 * se)
    return {"pearson_r": round(r, 6), "pearson_p": float(pval), "n": n,
            "se": round(se, 6), "z_r": round(z_r, 6),
            "ci_lower": round(ci_lo, 6), "ci_upper": round(ci_hi, 6),
            "tost_delta": delta, "tost_p_upper": float(p_upper),
            "tost_p_lower": float(p_lower),
            "tost_pass": bool(p_upper < 0.05 and p_lower < 0.05)}


# ===== Phase A: C1 auth discrimination + baselines =====
def phase_a():
    reset_all()
    probes = {}
    fps = {}
    bodies = {}
    statuses = {}
    for state in AUTH_STATES:
        fps[state] = []
        probes[state] = []
        for _ in range(N_DISC):
            resp = http_get("/api/data", AUTH_HEADERS[state])
            probes[state].append(resp)
            fps[state].append(fingerprint(resp))
        bodies[state] = set(
            json.dumps(json.loads(r["text"]), sort_keys=True)
            for r in probes[state])
        statuses[state] = set(r["status"] for r in probes[state])
    fp_sets = [set(v) for v in fps.values()]
    return {
        "discrimination_full_fingerprint": discrimination(fp_sets),
        "baseline_status_only": discrimination(list(statuses.values())),
        "baseline_body_only": discrimination(list(bodies.values())),
        "fingerprint_groups": {s: sorted(set(v)) for s, v in fps.items()},
        "n_unique_fingerprints": len(set().union(*fp_sets)),
        "n_states": len(AUTH_STATES),
        "raw_probes": probes,
    }


# ===== Phase B: C3 co-occurring paired samples =====
def collect_cooccur():
    reset_all()
    samples = []
    for (drift, noise) in COOCCUR_PAIRS:
        set_drift(drift)
        set_noise(noise)
        for _ in range(N_COOCCUR):
            resp_b = http_get("/api/session/status",
                              AUTH_HEADERS["valid_token"])
            resp_s = http_get("/api/schema")
            samples.append({
                "condition": "%s+%s" % (drift, noise),
                "drift": drift, "noise": noise,
                "behavioral_score": behavioral_score(resp_b),
                "structural_signal": structural_signal(resp_s),
                "status_code": resp_b["status"],
                "session_valid": json.loads(resp_b["text"]).get(
                    "session_valid"),
                "schema_cache_status": json.loads(resp_s["text"]).get(
                    "cache_status"),
            })
        reset_all()
    return samples


# ===== Phase C: C4 noise-only null =====
def collect_noise_only():
    reset_all()
    samples = []
    for noise in NOISE_TYPES:
        set_noise(noise)
        for _ in range(N_NOISE):
            resp_b = http_get("/api/session/status",
                              AUTH_HEADERS["valid_token"])
            resp_s = http_get("/api/schema")
            samples.append({
                "condition": "noise:%s" % noise,
                "drift": "none", "noise": noise,
                "behavioral_score": behavioral_score(resp_b),
                "structural_signal": structural_signal(resp_s),
                "status_code": resp_b["status"],
            })
        set_noise(None)
    return samples


# ===== Phase D: C2 isolated drift TP =====
def collect_tp():
    reset_all()
    samples = []
    for drift in DRIFT_TYPES:
        set_drift(drift)
        for _ in range(N_TP):
            resp_b = http_get("/api/session/status",
                              AUTH_HEADERS["valid_token"])
            samples.append({
                "condition": "drift:%s" % drift,
                "drift": drift, "noise": "none",
                "behavioral_score": behavioral_score(resp_b),
                "status_code": resp_b["status"],
            })
        reset_all()
    return samples


# ===== Server lifecycle =====
def start_server():
    srv = make_server("127.0.0.1", PORT, mock_server.app, threaded=False)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    for _ in range(100):
        try:
            s = socket.create_connection(("127.0.0.1", PORT), timeout=1.0)
            s.close()
            return srv
        except OSError:
            time.sleep(0.05)
    raise RuntimeError("server did not start")


# ===== Evidence dump + derived metrics + decision =====
def main():
    random.seed(SEED)
    np.random.seed(SEED)
    status = "COMPLETE"
    start = time.time()
    srv = start_server()
    try:
        print("[1/5] Phase A: C1 auth discrimination + baselines", flush=True)
        pa = phase_a()
        print("[2/5] Phase B: co-occurring 8x60 paired samples", flush=True)
        cooccur = collect_cooccur()
        print("[3/5] Phase C: noise-only 4x60", flush=True)
        noise_only = collect_noise_only()
        print("[4/5] Phase D: isolated drift TP 3x60", flush=True)
        tp_samples = collect_tp()
        print("[5/5] Phase E: orthogonality + decision", flush=True)
    finally:
        srv.shutdown()
        mock_server.shutdown()

    # ---------- RAW EVIDENCE (distinct from derived metrics) ----------
    raw = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "seed": SEED, "port": PORT, "threshold": THRESHOLD,
        "delta": TOST_DELTA,
        "phase_a_raw": pa["raw_probes"],
        "phase_b_cooccurring": cooccur,
        "phase_c_noise_only": noise_only,
        "phase_d_isolated_tp": tp_samples,
        "server": "mock_server.py (stochastic Flask+SQLite, TTL cache, "
                  "jitter, HS256/RS256 JWT)",
    }
    with open(RAW_DATA_PATH, "w") as f:
        json.dump(raw, f, indent=1, sort_keys=True)
    raw_sha = hashlib.sha256(
        open(RAW_DATA_PATH, "rb").read()).hexdigest()

    # ---------- DERIVED METRICS ----------
    c1_disc = pa["discrimination_full_fingerprint"]
    c1_pass = c1_disc > 0.5

    per_condition = {}
    for (d, n) in COOCCUR_PAIRS:
        key = "%s+%s" % (d, n)
        rows = [x for x in cooccur if x["condition"] == key]
        b = np.array([x["behavioral_score"] for x in rows])
        st = np.array([x["structural_signal"] for x in rows])
        per_condition[key] = {
            "n": len(rows),
            "behavioral_mean": round(float(b.mean()), 4),
            "behavioral_std": round(float(b.std(ddof=1)), 4),
            "structural_mean": round(float(st.mean()), 4),
            "structural_std": round(float(st.std(ddof=1)), 4),
            "tp_rate": round(float((b >= THRESHOLD).mean()), 4),
            "tp_rate_wilson_lower": wilson_lower(
                int((b >= THRESHOLD).sum()), len(b)),
        }
    n_variance_pass = sum(1 for v in per_condition.values()
                          if v["behavioral_std"] > 0.05
                          and v["structural_std"] > 0.05)

    behav_all = np.array([x["behavioral_score"] for x in cooccur])
    struct_all = np.array([x["structural_signal"] for x in cooccur])
    orth = tost_equivalence(behav_all, struct_all)
    c3_pass = (n_variance_pass >= 6 and orth["tost_pass"]
               and orth["ci_upper"] < TOST_DELTA)

    per_drift_tp = {}
    for d in DRIFT_TYPES:
        rows = [x for x in tp_samples if x["drift"] == d]
        b = np.array([x["behavioral_score"] for x in rows])
        per_drift_tp[d] = {
            "tp_rate": round(float((b >= THRESHOLD).mean()), 4),
            "tp_rate_wilson_lower": wilson_lower(
                int((b >= THRESHOLD).sum()), len(b)),
            "behavioral_mean": round(float(b.mean()), 4),
            "behavioral_std": round(float(b.std(ddof=1)), 4),
        }
    isolated_tp_pass = all(v["tp_rate"] >= 0.85
                           for v in per_drift_tp.values())
    cooccur_tp_pass = all(v["tp_rate"] >= 0.85
                          for v in per_condition.values())
    c2_pass = isolated_tp_pass and cooccur_tp_pass

    fp_rows = [x for x in noise_only if x["behavioral_score"] >= THRESHOLD]
    noise_fp_rate = round(len(fp_rows) / len(noise_only), 4)
    c4_pass = noise_fp_rate <= 0.15
    per_noise_fp = {}
    for n in NOISE_TYPES:
        rows = [x for x in noise_only if x["noise"] == n]
        hits = sum(1 for x in rows if x["behavioral_score"] >= THRESHOLD)
        per_noise_fp[n] = {
            "fp_rate": round(hits / len(rows), 4),
            "behavioral_mean": round(float(np.mean(
                [x["behavioral_score"] for x in rows])), 4),
        }

    # ---------- DECISION (frozen prereg rule) ----------
    variance_ok = n_variance_pass >= 6
    if c1_pass and c2_pass and c3_pass and c4_pass:
        outcome = "SURVIVES"
    elif not variance_ok and all(v["behavioral_std"] <= 0.05
                                 for v in per_condition.values()):
        outcome = "MEASUREMENT_INVALID"
    elif c1_pass and c2_pass and c4_pass:
        outcome = "MIXED"
    else:
        outcome = "FALSIFIED"

    metrics = {
        "c1_auth_discrimination": c1_disc,
        "c1_pass": c1_pass,
        "baseline_status_only": pa["baseline_status_only"],
        "baseline_body_only": pa["baseline_body_only"],
        "c2_isolated_tp": per_drift_tp,
        "c2_cooccurring_tp": {k: v["tp_rate"]
                              for k, v in per_condition.items()},
        "c2_pass": c2_pass,
        "c3_per_condition": per_condition,
        "c3_variance_conditions_pass": n_variance_pass,
        "c3_variance_pass_required": 6,
        "c3_orthogonality": orth,
        "c3_pass": c3_pass,
        "c4_noise_fp_rate": noise_fp_rate,
        "c4_pass": c4_pass,
        "c4_per_noise": per_noise_fp,
        "decision_source": "frozen prereg decision rule",
    }
    observations = {
        "phase_a": {k: v for k, v in pa.items() if k != "raw_probes"},
        "cooccur_n": len(cooccur),
        "noise_only_n": len(noise_only),
        "tp_n": len(tp_samples),
        "detection_threshold": THRESHOLD,
        "delta": TOST_DELTA,
        "runtime_seconds": round(time.time() - start, 2),
        "raw_evidence_sha256": raw_sha,
    }
    return {"experiment_id": EXPERIMENT_ID, "lane": LANE, "outcome": outcome,
            "status": status, "metrics": metrics,
            "observations": observations,
            "generated_at": datetime.now(timezone.utc).isoformat()}


def _clean(o):
    """Normalize numpy 2.x scalars (np.bool_/np.float64/np.int64) to Python
    natives so the result packet is strictly JSON-serializable."""
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.integer):
        return int(o)
    return o


if __name__ == "__main__":
    result = _clean(main())
    out_path = os.path.join(HERE, "result_draft.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, sort_keys=True)
    print("WROTE %s" % out_path)
    print("OUTCOME=%s" % result["outcome"])
    for k, v in sorted(result["metrics"].items()):
        if not isinstance(v, dict):
            print("  %s=%s" % (k, v))