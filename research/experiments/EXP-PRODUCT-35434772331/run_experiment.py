#!/usr/bin/env python3
"""
EXP-PRODUCT-35434772331 — Single-process experiment.
Tests behavioral+structural signal orthogonality on real SPIDER kernel workflow patterns.

Frozen spec: C-PRODUCT-ECON closure + C-FRESHNESS integration test.
Positive control: HTTP fingerprint discrimination > 0.5 (replicates EXP-RUNTIME-33902315583).
Behavioral TP >= 0.85 on drift detection.
Orthogonality: TOST at delta=0.15, CI upper bound < 0.15.
Null control: FP <= 0.15 on structural noise.
"""
import hashlib
import json
import math
import os
import random
import sys
import time
import threading
import urllib.request
import urllib.error

import jwt as pyjwt
import numpy as np
from scipy import stats as scipy_stats

# ===== CONFIG =====
SEED = 42
N_SAMPLES = 60
PORT = 18936
BASE_URL = f"http://127.0.0.1:{PORT}"
SECRET_KEY = "test-secret-key-35434772331-exp-product-3543"

AUTH_STATES = ["no_auth", "valid_token", "expired_token", "invalid_token"]
DRIFT_PATTERNS = ["permission_boundary", "session_invalidation", "token_refresh"]
NOISE_PATTERNS = ["optional_field_addition", "description_change", "response_time_jitter", "field_type_normalization"]

COOCURRING = [{"drift": d, "noise": n} for d in DRIFT_PATTERNS for n in NOISE_PATTERNS]
NOISE_ONLY = [{"drift": None, "noise": n} for n in NOISE_PATTERNS]


# ===== INLINE FLASK SERVER =====
# We embed a minimal WSGI server to avoid Flask threading issues
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

# State
_state_lock = threading.Lock()
_server_state = {
    "drift_active": False, "drift_type": None,
    "noise_active": False, "noise_type": None,
    "extra_fields": {},
    "current_role": "admin",
    "session_valid": True,
}


def _make_jwt(state):
    now = time.time()
    if state == "no_auth":
        return None
    elif state == "valid_token":
        return pyjwt.encode({"sub": "alice", "role": _server_state["current_role"],
                             "iss": "spider", "iat": now, "exp": now + 3600,
                             "session_id": "sess-001"}, SECRET_KEY, algorithm="HS256")
    elif state == "expired_token":
        return pyjwt.encode({"sub": "alice", "role": "admin",
                             "iss": "spider", "iat": now - 7200, "exp": now - 3600,
                             "session_id": "sess-001"}, SECRET_KEY, algorithm="HS256")
    elif state == "invalid_token":
        return pyjwt.encode({"sub": "alice", "role": "admin",
                             "iss": "spider", "iat": now, "exp": now + 3600,
                             "session_id": "sess-001"}, "wrong-secret", algorithm="HS256")
    return None


def _validate_jwt(auth_header):
    if not auth_header:
        return 401, None, "login_required"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        return 401, None, "auth_failed"
    try:
        payload = pyjwt.decode(parts[1], SECRET_KEY, algorithms=["HS256"])
        if not _server_state["session_valid"]:
            return 401, None, "session_invalidated"
        return 200, payload, None
    except pyjwt.ExpiredSignatureError:
        return 401, None, "auth_failed"
    except pyjwt.InvalidTokenError:
        return 410, None, "auth_failed"


def _app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")

    # Parse body for POST
    body_len = int(environ.get("CONTENT_LENGTH", 0) or 0)
    body_data = environ["wsgi.input"].read(body_len) if body_len > 0 else b""
    post_data = {}
    if body_data:
        try:
            post_data = json.loads(body_data)
        except json.JSONDecodeError:
            pass

    # Extract auth header
    auth_header = environ.get("HTTP_AUTHORIZATION", "")

    # --- ROUTING ---
    if path == "/health":
        resp_code, resp_body = 200, json.dumps({"status": "ok", "port": PORT})

    elif path == "/api/drift" and method == "POST":
        drift_type = post_data.get("drift_type")
        with _state_lock:
            if drift_type is None or drift_type == "none":
                _server_state["drift_active"] = False
                _server_state["drift_type"] = None
                _server_state["current_role"] = "admin"
                _server_state["session_valid"] = True
            elif drift_type in ("permission_boundary", "session_invalidation", "token_refresh"):
                _server_state["drift_active"] = True
                _server_state["drift_type"] = drift_type
                if drift_type == "permission_boundary":
                    _server_state["current_role"] = "viewer"
                elif drift_type == "session_invalidation":
                    _server_state["session_valid"] = False
        resp_code, resp_body = 200, json.dumps({"status": "ok", "drift": drift_type})

    elif path == "/api/noise" and method == "POST":
        noise_type = post_data.get("noise_type")
        with _state_lock:
            if noise_type is None or noise_type == "none":
                _server_state["noise_active"] = False
                _server_state["noise_type"] = None
                _server_state["extra_fields"] = {}
            elif noise_type in NOISE_PATTERNS:
                _server_state["noise_active"] = True
                _server_state["noise_type"] = noise_type
                if noise_type == "optional_field_addition":
                    _server_state["extra_fields"] = {"debug": "trace_35434772331", "cache_key": "v2"}
        resp_code, resp_body = 200, json.dumps({"status": "ok", "noise": noise_type})

    elif path == "/api/data" and method == "GET":
        # Sleep for jitter simulation
        time.sleep(random.uniform(0.02, 0.06))

        status, payload, error = _validate_jwt(auth_header)
        with _state_lock:
            drift = _server_state["drift_active"]
            drift_type = _server_state["drift_type"]
            noise = _server_state["noise_active"]
            noise_type = _server_state["noise_type"]
            extra = _server_state["extra_fields"]
            current_role = _server_state["current_role"]

        if error == "login_required":
            status_code = 401
            resp_body = json.dumps({"error": "login_required", "message": "Authentication required"})
            cache_ctrl = "no-store"
            set_cookie = None
        elif error == "auth_failed":
            status_code = 401
            resp_body = json.dumps({"error": "authentication_failed"})
            cache_ctrl = "no-store"
            set_cookie = None
        elif error == "session_invalidated":
            status_code = 401
            resp_body = json.dumps({"error": "session_invalidated"})
            cache_ctrl = "no-store"
            set_cookie = None
        elif status == 200:
            status_code = 200
            data = {
                "user_id": payload["sub"],
                "role": payload.get("role", "admin"),
                "data": {"value": "test_data"},
                "session_id": payload.get("session_id"),
            }
            if drift and drift_type == "permission_boundary":
                data["role"] = current_role
                data["permissions"] = ["read"] if current_role == "viewer" else ["read", "write", "admin"]
            if drift and drift_type == "session_invalidation":
                status_code = 403
                resp_body = json.dumps({"status": "revoked", "session_valid": False})
                cache_ctrl = "no-store"
                set_cookie = None
            elif drift and drift_type == "token_refresh":
                data["status"] = "refreshed"
                data["new_token_issued"] = True
                resp_body = json.dumps(data)
                cache_ctrl = "no-cache"
                set_cookie = f"session={payload.get('session_id')}; HttpOnly; Secure"
            else:
                resp_body = json.dumps(data)
                cache_ctrl = "no-cache"
                set_cookie = f"session={payload.get('session_id')}; HttpOnly; Secure"
        else:
            status_code = status
            resp_body = json.dumps({"error": "unknown"})
            cache_ctrl = "no-store"
            set_cookie = None

        # Add noise to response body
        if noise and status_code == 200:
            try:
                d = json.loads(resp_body)
                if noise_type == "optional_field_addition":
                    d["metadata"] = extra
                elif noise_type == "description_change":
                    d["api_version"] = "2.1-updated"
                elif noise_type == "field_type_normalization":
                    d["field_types"] = {"user_id": "string", "role": "string"}
                resp_body = json.dumps(d)
            except json.JSONDecodeError:
                pass

        resp_code = status_code
        resp_headers_extra = {"Cache-Control": cache_ctrl}
        if set_cookie:
            resp_headers_extra["Set-Cookie"] = set_cookie
        if noise:
            if noise_type == "optional_field_addition":
                resp_headers_extra["X-Api-Metadata"] = json.dumps(extra)
            elif noise_type == "field_type_normalization":
                resp_headers_extra["X-Api-Version"] = "2.0-norm"
    else:
        resp_code, resp_body = 404, json.dumps({"error": "not_found"})
        resp_headers_extra = {}

    # Send response
    body_bytes = resp_body.encode("utf-8")
    headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(body_bytes))),
    ]
    for k, v in resp_headers_extra.items():
        headers.append((k, v))

    start_response(f"{resp_code} OK", headers)
    return [body_bytes]


def _start_server():
    server = make_server("127.0.0.1", PORT, _app)
    server.timeout = 1
    # Run in background thread
    t = threading.Thread(target=lambda: server.serve_forever(), daemon=True)
    t.start()
    return server


# ===== EXPERIMENT LOGIC =====
def fingerprint(status, headers_dict, body_str):
    body_sha = hashlib.sha256(body_str.encode()).hexdigest()[:8]
    filtered = {k: v for k, v in sorted(headers_dict.items())
                if k.lower() not in ("date", "server", "x-request-id", "connection")}
    vector = (status, tuple(sorted(filtered.items())), body_sha, "")
    return hashlib.sha256(repr(vector).encode()).hexdigest()[:16]


def http_get(path, auth_state=None):
    """Make GET request, return (status, headers_dict, body_str)."""
    url = f"{BASE_URL}{path}"
    headers = {}
    token = _make_jwt(auth_state)
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=5)
        body = resp.read().decode()
        h = {}
        for k in resp.headers:
            if k.lower() not in ("date", "server", "x-request-id"):
                h[k] = resp.headers[k]
        return resp.status, h, body
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        h = {}
        for k in e.headers:
            if k.lower() not in ("date", "server", "x-request-id"):
                h[k] = e.headers[k]
        return e.code, h, body
    except Exception as e:
        return 0, {}, str(e)


def http_post(path, data):
    """Make POST request."""
    url = f"{BASE_URL}{path}"
    body_bytes = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body_bytes, headers={"Content-Type": "application/json"}, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:
        return 0, str(e)


def set_drift(drift_type):
    return http_post("/api/drift", {"drift_type": drift_type})


def set_noise(noise_type):
    return http_post("/api/noise", {"noise_type": noise_type})


def behavioral_score(status, body_str):
    """Behavioral signal: detects auth drift from JWT/session/permission changes.
    Returns 0.0 to 1.0."""
    try:
        body = json.loads(body_str)
    except (json.JSONDecodeError, ValueError):
        return 0.0

    score = 0.0

    # Signal: session status
    if body.get("session_valid") is False:
        score += 0.4
    elif body.get("session_valid") is True:
        score += 0.1

    # Signal: role change
    if body.get("role") == "viewer":
        score += 0.3
    elif body.get("role") == "admin":
        score += 0.05

    # Signal: revocation
    if body.get("status") == "revoked" or body.get("error") == "session_invalidated":
        score += 0.3
    elif body.get("status") == "refreshed":
        score += 0.15

    # Signal: permission reduction
    perms = body.get("permissions", [])
    if isinstance(perms, list) and len(perms) <= 1:
        score += 0.2

    return min(score, 1.0)


def fisher_z(r):
    r_c = max(-0.9999, min(0.9999, r))
    return 0.5 * math.log((1 + r_c) / (1 - r_c))


def tost_test(r, n, delta):
    z_r = fisher_z(r)
    se = 1.0 / math.sqrt(n - 3) if n > 3 else 1.0
    z_upper = (z_r - fisher_z(delta)) / se
    z_lower = (z_r - fisher_z(-delta)) / se
    p_upper = 1 - scipy_stats.norm.cdf(z_upper)
    p_lower = scipy_stats.norm.cdf(z_lower)
    # CI via Fisher z
    z_lo = z_r - 1.96 * se
    z_hi = z_r + 1.96 * se
    ci_lo = (math.exp(2 * z_lo) - 1) / (math.exp(2 * z_lo) + 1)
    ci_hi = (math.exp(2 * z_hi) - 1) / (math.exp(2 * z_hi) + 1)
    return {
        "pass": p_upper < 0.05 and p_lower < 0.05,
        "p_upper": p_upper,
        "p_lower": p_lower,
        "ci_lower": ci_lo,
        "ci_upper": ci_hi,
        "n": n,
    }


def discrimination_from_groups(groups):
    """Compute discrimination: intra - mean(inter)."""
    # Intra: fraction of unique fingerprints that are identical within each group
    intra_scores = []
    for g in groups.values():
        unique = list(set(g))
        if len(unique) <= 1:
            intra_scores.append(1.0)
        else:
            total_pairs = len(unique) * (len(unique) - 1) / 2
            matches = sum(1 for i in range(len(unique)) for j in range(i+1, len(unique)) if unique[i] == unique[j])
            intra_scores.append(matches / total_pairs if total_pairs > 0 else 0.0)
    intra = sum(intra_scores) / len(intra_scores) if intra_scores else 0.0

    # Inter: fraction of fingerprints matching across different groups
    inter_scores = []
    gkeys = list(groups.keys())
    for i in range(len(gkeys)):
        for j in range(i+1, len(gkeys)):
            ui = set(groups[gkeys[i]])
            uj = set(groups[gkeys[j]])
            matches = len(ui & uj)
            total = len(ui) * len(uj)
            inter_scores.append(matches / total if total > 0 else 0.0)
    inter = sum(inter_scores) / len(inter_scores) if inter_scores else 0.0

    return intra - inter, intra, inter


def main():
    random.seed(SEED)
    np.random.seed(SEED)

    print("=" * 70)
    print("EXP-PRODUCT-35434772331")
    print("Behavioral+Structural Signal Orthogonality on SPIDER Kernel Workflows")
    print("=" * 70)

    # Start embedded server
    print("\nStarting embedded WSGI server...")
    server = _start_server()
    time.sleep(0.5)

    # Verify server
    try:
        s, _, b = http_get("/health")
        print(f"  Health check: status={s} body={b[:50]}")
    except Exception as e:
        print(f"  Health check FAILED: {e}")
        server.shutdown()
        return

    # ===== Phase 1: Auth-state discrimination (positive control C1) =====
    print("\n--- Phase 1: Auth-state discrimination (C1) ---")
    set_drift(None)
    set_noise(None)
    time.sleep(0.1)

    auth_fps = {st: [] for st in AUTH_STATES}
    auth_bodies = {}
    for st in AUTH_STATES:
        for _ in range(10):
            s, h, b = http_get("/api/data", st)
            fp = fingerprint(s, h, b)
            auth_fps[st].append(fp)
            if st not in auth_bodies:
                auth_bodies[st] = []
            auth_bodies[st].append({"status": s, "body": b[:200], "fp": fp})
            time.sleep(0.05)

    disc, intra, inter = discrimination_from_groups(auth_fps)
    print(f"  Full-vector discrimination: {disc:.4f} (intra={intra:.4f}, inter={inter:.4f})")
    for st in AUTH_STATES:
        fps = list(set(auth_fps[st]))
        sample = auth_bodies[st][0] if auth_bodies[st] else {}
        print(f"    {st}: {len(fps)} unique fp, sample_status={sample.get('status')}, body={sample.get('body','')[:60]}")

    # Baselines
    print("\n--- Phase 2: Baselines ---")
    # B-STATUS-ONLY
    status_groups = {st: [] for st in AUTH_STATES}
    for st in AUTH_STATES:
        for _ in range(10):
            s, h, b = http_get("/api/data", st)
            status_groups[st].append(hashlib.sha256(str(s).encode()).hexdigest()[:16])
            time.sleep(0.03)
    disc_status, _, _ = discrimination_from_groups(status_groups)
    print(f"  B-STATUS-ONLY: {disc_status:.4f}")

    # B-BODY-ONLY
    body_groups = {st: [] for st in AUTH_STATES}
    for st in AUTH_STATES:
        for _ in range(10):
            s, h, b = http_get("/api/data", st)
            body_groups[st].append(hashlib.sha256(b.encode()).hexdigest()[:16])
            time.sleep(0.03)
    disc_body, _, _ = discrimination_from_groups(body_groups)
    print(f"  B-BODY-ONLY: {disc_body:.4f}")

    # ===== Phase 3: Null FP rate =====
    print("\n--- Phase 3: Null FP rate (C4 null control) ---")
    set_drift(None)
    set_noise(None)
    time.sleep(0.1)

    null_fp = {}
    for st in AUTH_STATES:
        fps = []
        for _ in range(10):
            s, h, b = http_get("/api/data", st)
            fps.append(fingerprint(s, h, b))
            time.sleep(0.03)
        unique = len(set(fps))
        null_fp[st] = {"total": len(fps), "unique": unique, "fp": max(0, unique - 1)}

    total_fp = sum(v["fp"] for v in null_fp.values())
    total_n = sum(v["total"] for v in null_fp.values())
    null_fp_rate = total_fp / total_n if total_n else 0
    print(f"  Null FP rate: {null_fp_rate:.4f} ({total_fp}/{total_n})")

    # ===== Phase 4: Co-occurring conditions (drift x noise) =====
    print("\n--- Phase 4: Co-occurring conditions (drift x noise) ---")
    cooccur_samples = []
    for i, cond in enumerate(COOCURRING):
        drift, noise = cond["drift"], cond["noise"]
        set_drift(drift)
        set_noise(noise)
        time.sleep(0.1)

        samples = []
        for _ in range(N_SAMPLES):
            # Use valid_token to detect drift behavior
            s, h, b = http_get("/api/data", "valid_token")
            behav = behavioral_score(s, b)
            fp = fingerprint(s, h, b)
            # Structural: count distinctive features
            try:
                body_obj = json.loads(b)
                struct = len(body_obj) + len(h) + 1  # fields + headers + status
            except:
                struct = len(h) + 1
            samples.append({"drift": drift, "noise": noise, "status": s,
                           "fp": fp, "behav": behav, "struct": struct})
            time.sleep(0.03)

        cooccur_samples.extend(samples)
        behav_mean = np.mean([s["behav"] for s in samples])
        print(f"  [{i+1}/{len(COOCURRING)}] drift={drift}, noise={noise}: n={len(samples)}, behav_mean={behav_mean:.4f}")

    # ===== Phase 5: Noise-only conditions (null control) =====
    print("\n--- Phase 5: Noise-only conditions ---")
    noiseonly_samples = []
    for cond in NOISE_ONLY:
        noise = cond["noise"]
        set_drift(None)
        set_noise(noise)
        time.sleep(0.1)

        samples = []
        for _ in range(N_SAMPLES):
            s, h, b = http_get("/api/data", "valid_token")
            behav = behavioral_score(s, b)
            fp = fingerprint(s, h, b)
            try:
                body_obj = json.loads(b)
                struct = len(body_obj) + len(h) + 1
            except:
                struct = len(h) + 1
            samples.append({"noise": noise, "status": s, "fp": fp, "behav": behav, "struct": struct})
            time.sleep(0.03)

        noiseonly_samples.extend(samples)
        behav_mean = np.mean([s["behav"] for s in samples])
        fp_count = sum(1 for s in samples if s["behav"] >= 0.5)
        print(f"  noise={noise}: n={len(samples)}, behav_mean={behav_mean:.4f}, FP={fp_count}")

    # ===== Phase 6: Behavioral TP (drift detection) =====
    print("\n--- Phase 6: Behavioral TP (drift detection) ---")
    drift_tp = {}
    for drift_type in DRIFT_PATTERNS:
        set_drift(drift_type)
        set_noise(None)
        time.sleep(0.1)

        tp = 0
        for _ in range(N_SAMPLES):
            s, h, b = http_get("/api/data", "valid_token")
            behav = behavioral_score(s, b)
            if behav >= 0.5:
                tp += 1
            time.sleep(0.03)
        rate = tp / N_SAMPLES
        drift_tp[drift_type] = {"tp": tp, "total": N_SAMPLES, "rate": rate}
        print(f"  {drift_type}: TP={rate:.4f} ({tp}/{N_SAMPLES})")

    # ===== Phase 7: Orthogonality test =====
    print("\n--- Phase 7: Orthogonality test (C3) ---")
    behav_arr = np.array([s["behav"] for s in cooccur_samples])
    struct_arr = np.array([s["struct"] for s in cooccur_samples], dtype=float)

    behav_var = np.var(behav_arr)
    struct_var = np.var(struct_arr)
    print(f"  Behavioral variance: {behav_var:.6f}, Structural variance: {struct_var:.6f}")

    if behav_var == 0 or struct_var == 0:
        r_val = float('nan')
        p_val = float('nan')
        tost_result = {"pass": False, "p_upper": 1.0, "ci_lower": -1.0, "ci_upper": 1.0, "n": len(behav_arr)}
        print(f"  Pearson r: NaN (constant input)")
    else:
        r_val, p_val = scipy_stats.pearsonr(behav_arr, struct_arr)
        tost_result = tost_test(r_val, len(behav_arr), 0.15)
        print(f"  Pearson r (n={len(behav_arr)}): {r_val:.6f} (p={p_val:.6f})")
        print(f"  TOST at delta=0.15: pass={tost_result['pass']}, p_upper={tost_result['p_upper']:.6f}")
        print(f"  95% CI: [{tost_result['ci_lower']:.6f}, {tost_result['ci_upper']:.6f}]")

    # ===== Phase 8: Noise FP =====
    print("\n--- Phase 8: Noise FP rate (C4) ---")
    set_drift(None)
    set_noise(None)
    time.sleep(0.1)
    noise_fp_total = sum(1 for s in noiseonly_samples if s["behav"] >= 0.5)
    noise_fp_rate = noise_fp_total / len(noiseonly_samples) if noiseonly_samples else 0
    print(f"  Noise FP rate: {noise_fp_rate:.4f} ({noise_fp_total}/{len(noiseonly_samples)})")

    # ===== DECISION =====
    print("\n" + "=" * 70)
    print("DECISION")
    print("=" * 70)

    c1_pass = disc > 0.5
    mean_tp = np.mean([v["rate"] for v in drift_tp.values()])
    c2_pass = mean_tp >= 0.85
    c3_pass = (not math.isnan(r_val)) and tost_result.get("ci_upper", 1.0) < 0.15
    c4_pass = noise_fp_rate <= 0.15

    print(f"  C1 (discrimination > 0.5): {disc:.4f} -> {'PASS' if c1_pass else 'FAIL'}")
    print(f"  C2 (behavioral TP >= 0.85): mean={mean_tp:.4f} -> {'PASS' if c2_pass else 'FAIL'}")
    for dt, v in drift_tp.items():
        print(f"      {dt}: {v['rate']:.4f}")
    print(f"  C3 (orthogonality CI upper < 0.15): ci_upper={tost_result.get('ci_upper', 'NaN')} -> {'PASS' if c3_pass else 'FAIL'}")
    print(f"  C4 (noise FP <= 0.15): {noise_fp_rate:.4f} -> {'PASS' if c4_pass else 'FAIL'}")

    all_pass = c1_pass and c2_pass and c3_pass and c4_pass
    outcome = "SURVIVES" if all_pass else "FALSIFIED"
    print(f"\n  OUTCOME: {outcome}")
    print("=" * 70)

    # ===== SAVE RAW EVIDENCE =====
    raw = {
        "experiment_id": "EXP-PRODUCT-35434772331",
        "seed": SEED,
        "n_samples_per_condition": N_SAMPLES,
        "n_cooccurring": len(COOCURRING),
        "n_noise_only": len(NOISE_ONLY),
        "auth_discrimination": {"full": disc, "intra": intra, "inter": inter,
                                "fingerprints": {k: list(set(v)) for k, v in auth_fps.items()}},
        "auth_bodies": {k: v[:2] for k, v in auth_bodies.items()},
        "baselines": {"B_STATUS_ONLY": disc_status, "B_BODY_ONLY": disc_body},
        "null_fp": {"counts": null_fp, "overall_rate": null_fp_rate},
        "drift_tp": drift_tp,
        "orthogonality": {
            "r": None if math.isnan(r_val) else r_val,
            "p_value": None if math.isnan(p_val) else p_val,
            "n": len(behav_arr),
            "behav_variance": behav_var,
            "struct_variance": struct_var,
            "tost": tost_result,
        },
        "noise_fp_rate": noise_fp_rate,
        "noise_fp_total": noise_fp_total,
        "noiseonly_n": len(noiseonly_samples),
        "cooccur_samples_summary": {
            "total": len(cooccur_samples),
            "behav_mean": float(np.mean(behav_arr)),
            "behav_std": float(np.std(behav_arr)),
            "struct_mean": float(np.mean(struct_arr)),
            "struct_std": float(np.std(struct_arr)),
        },
        "decision": {"C1": c1_pass, "C2": c2_pass, "C3": c3_pass, "C4": c4_pass, "outcome": outcome},
    }

    out_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(out_dir, "raw_evidence", "experiment_data.json")
    with open(raw_path, "w") as f:
        json.dump(raw, f, indent=2, default=str)
    print(f"\nRaw evidence saved to {raw_path}")

    # Shutdown server
    server.shutdown()
    print("Server shut down.")


if __name__ == "__main__":
    main()
